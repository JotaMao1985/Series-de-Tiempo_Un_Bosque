#!/usr/bin/env python3
"""
exporta_zotero.py — la biblioteca del curso, congelada en el repo

Material de Series de Tiempo 2026-II (20948).

Zotero es la puerta de entrada de toda obra que el material cita: los metadatos
los escriben sus traductores a partir de un DOI o un ISBN, nunca un modelo de
memoria. Pero un auditor no puede depender de que Zotero esté abierto. Este
guion lee la colección del curso por la API local de Zotero (solo lectura,
`http://localhost:23119/api`) y deja en `bibliografia/` la instantánea que todo
lo demás consume:

  · referencias.json   — CSL-JSON, una entrada por obra, con `id` = clave de cita
  · claves.json        — clave de Zotero → clave de cita. Una clave asignada NO
                         cambia nunca, aunque en Zotero se corrija el título o
                         el año: el HTML la lleva escrita en `data-ref`
  · zotero.lock.json   — de dónde salió la instantánea: versión de Zotero,
                         colección, rol de cada obra y sus adjuntos (nombre y
                         sha256, nunca el archivo)

La clave de cita se forma como `apellido + año + primera palabra del título`
(`cleveland1990stl`), en minúsculas y ASCII. Si Zotero trae su propia clave en
el campo `citationKey`, manda esa.

Dos arreglos se hacen al exportar, y solo esos dos:

  · La edición se normaliza a número («Fifth edition», «3rd ed» → 5, 3), que es
    lo que el estilo APA necesita para escribir «5.ª ed.». Lo que no es un
    ordinal («Rev. ed») se deja como viene.
  · `bibliografia/enmiendas.yml` corrige campos que el traductor de Zotero no
    trajo (Crossref no registra el número de edición de los libros de
    Springer). Cada enmienda lleva su evidencia: una URL consultada y la fecha.
    Si Zotero ya trae ese valor, el guion avisa de que la enmienda sobra. Lo
    correcto a la larga es llevar el dato a Zotero y borrar la enmienda.

Un adjunto titulado «Table of Contents PDF» no es el libro: el traductor por
ISBN lo descarga solo de un catálogo de biblioteca, y se ignora.

El rol sale de la subcolección: «1 Básica» → basica, «2 Complementaria» →
complementaria, «3 Fuentes primarias» → primaria, «4 Datos y software» → datos.

Uso:  python3 precalculo/exporta_zotero.py            # escribe
      python3 precalculo/exporta_zotero.py --comprobar # sale con 1 si el repo
                                                       # no coincide con Zotero

Requiere Zotero abierto y, en Ajustes → Avanzado, marcada la casilla «Allow
other applications on this computer to communicate with Zotero».
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BIB = RAIZ / "bibliografia"
API = "http://localhost:23119/api/users/0"
RUTA_COLECCION = ["Docencia", "20948 Series de Tiempo"]
ALMACEN = pathlib.Path.home() / "Zotero" / "storage"

ROLES = {"1": "basica", "2": "complementaria", "3": "primaria", "4": "datos"}
ORDINALES = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
    "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
}
NO_SON_EL_LIBRO = {"Table of Contents PDF"}
VACIAS = {
    "a", "an", "the", "on", "of", "for", "and", "in", "to", "with",
    "el", "la", "los", "las", "un", "una", "de", "del", "y", "en", "para",
}


def pide(ruta: str, **parametros) -> tuple[object, dict]:
    """GET a la API local. Devuelve (json, cabeceras)."""
    url = f"{API}{ruta}"
    if parametros:
        url += "?" + urllib.parse.urlencode(parametros)
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.loads(r.read().decode("utf-8")), dict(r.headers)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:200]
        sys.exit(f"FALLA  la API local respondió {e.code}: {cuerpo}")
    except (urllib.error.URLError, OSError) as e:
        sys.exit(
            "FALLA  no hay respuesta en localhost:23119 "
            f"({e}). ¿Está Zotero abierto y la API local activada?"
        )


def pide_todo(ruta: str, **parametros) -> list:
    """Recorre la paginación de la API (100 por página)."""
    todo, inicio = [], 0
    while True:
        pagina, _ = pide(ruta, limit=100, start=inicio, **parametros)
        todo.extend(pagina)
        if len(pagina) < 100:
            return todo
        inicio += 100


def ascii_minus(texto: str) -> str:
    plano = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", plano.lower())


def clave_nueva(csl: dict, usadas: set[str]) -> str:
    autores = csl.get("author") or csl.get("editor") or []
    primero = autores[0] if autores else {}
    apellido = ascii_minus(primero.get("family") or primero.get("literal") or "anonimo")
    partes = (csl.get("issued") or {}).get("date-parts") or [[None]]
    anio = str(partes[0][0]) if partes[0] and partes[0][0] else "sf"
    palabras = [ascii_minus(p) for p in re.split(r"[\s:,\-–—]+", csl.get("title", ""))]
    palabra = next((p for p in palabras if p and p not in VACIAS), "")
    base = f"{apellido}{anio}{palabra}"
    clave, n = base, 1
    while clave in usadas:
        n += 1
        clave = f"{base}{n}"
    return clave


def edicion_normal(valor) -> str | None:
    """«Fifth edition», «3rd ed», «2nd edition», 4 → «5», «3», «2», «4»."""
    if valor in (None, ""):
        return None
    texto = str(valor).strip()
    m = re.fullmatch(r"(\d+)\s*(?:st|nd|rd|th|\.ª|ª|a)?\.?\s*(?:ed\.?|edition|edición)?\.?", texto, re.I)
    if m:
        return m.group(1)
    m = re.fullmatch(r"([a-z]+)\s+(?:ed\.?|edition)\.?", texto, re.I)
    if m and m.group(1).lower() in ORDINALES:
        return str(ORDINALES[m.group(1).lower()])
    return texto


def aplica_enmiendas(referencias: list[dict]) -> list[str]:
    """Aplica bibliografia/enmiendas.yml. Devuelve los avisos."""
    ruta = BIB / "enmiendas.yml"
    if not ruta.exists():
        return []
    enmiendas = yaml.safe_load(ruta.read_text("utf-8")) or {}
    por_clave = {r["id"]: r for r in referencias}
    avisos = []
    for clave, campos in enmiendas.items():
        if clave not in por_clave:
            avisos.append(f"enmienda para «{clave}», que no está en la colección")
            continue
        for campo, e in campos.items():
            if not (isinstance(e, dict) and "valor" in e and e.get("evidencia") and e.get("consulta")):
                sys.exit(f"FALLA  enmiendas.yml · {clave}.{campo}: hacen falta `valor`, `evidencia` y `consulta`")
            if str(por_clave[clave].get(campo)) == str(e["valor"]):
                avisos.append(f"la enmienda {clave}.{campo} sobra: Zotero ya trae «{e['valor']}»")
            por_clave[clave][campo] = e["valor"]
    return avisos


def sha256(ruta: pathlib.Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def coleccion_del_curso() -> tuple[str, dict[str, str]]:
    """Clave de la colección del curso y {clave de subcolección: rol}."""
    todas = pide_todo("/collections")
    padre = False
    for nombre in RUTA_COLECCION:
        hallada = [
            c for c in todas
            if c["data"]["name"] == nombre and c["data"].get("parentCollection") == padre
        ]
        if len(hallada) != 1:
            sys.exit(f"FALLA  no hay exactamente una colección «{nombre}» en Zotero")
        padre = hallada[0]["key"]
    roles = {padre: "sin-rol"}
    for c in todas:
        if c["data"].get("parentCollection") == padre:
            roles[c["key"]] = ROLES.get(c["data"]["name"][:1], "sin-rol")
    return padre, roles


def adjuntos_de(clave_zotero: str) -> list[dict]:
    hijos = pide_todo(f"/items/{clave_zotero}/children")
    salida = []
    for h in hijos:
        d = h["data"]
        if d.get("itemType") != "attachment" or d.get("contentType") != "application/pdf":
            continue
        if d.get("title") in NO_SON_EL_LIBRO:
            continue
        if d.get("linkMode") == "linked_file":
            ruta = pathlib.Path(d.get("path", ""))
        else:
            ruta = ALMACEN / h["key"] / d.get("filename", "")
        salida.append({
            "zotero": h["key"],
            "archivo": d.get("filename") or ruta.name,
            "modo": d.get("linkMode"),
            "sha256": sha256(ruta) if ruta.is_file() else None,
        })
    return sorted(salida, key=lambda a: a["archivo"])


def construye() -> tuple[list, dict, dict]:
    raiz, roles = coleccion_del_curso()
    _, cabeceras = pide("/items", limit=1)
    ruta_claves = BIB / "claves.json"
    claves = json.loads(ruta_claves.read_text("utf-8")) if ruta_claves.exists() else {}
    usadas = set(claves.values())

    obras: dict[str, dict] = {}
    for col, rol in roles.items():
        for item in pide_todo(f"/collections/{col}/items/top", include="csljson,data"):
            z = item["key"]
            if z in obras:
                continue
            csl = item["csljson"]
            csl = json.loads(csl) if isinstance(csl, str) else csl
            csl = csl[0] if isinstance(csl, list) else csl
            if z not in claves:
                propia = (item["data"].get("citationKey") or "").strip()
                claves[z] = propia if propia and propia not in usadas else clave_nueva(csl, usadas)
                usadas.add(claves[z])
            csl["id"] = claves[z]
            csl.pop("abstract", None)      # texto de la editorial: no hace falta y el repo es público
            if edicion_normal(csl.get("edition")):
                csl["edition"] = edicion_normal(csl["edition"])
            obras[z] = {
                "csl": csl,
                "rol": rol,
                "tipo": item["data"].get("itemType"),
                "version": item.get("version"),
                "etiquetas": sorted(t["tag"] for t in item["data"].get("tags", [])),
            }

    referencias = sorted((o["csl"] for o in obras.values()), key=lambda c: c["id"])
    for aviso in aplica_enmiendas(referencias):
        print(f"AVISO  {aviso}")
    candado = {
        "zotero": cabeceras.get("X-Zotero-Version"),
        "coleccion": "/".join(RUTA_COLECCION),
        "coleccion_clave": raiz,
        "obras": {
            claves[z]: {
                "zotero": z,
                "rol": o["rol"],
                "tipo": o["tipo"],
                "etiquetas": o["etiquetas"],
                "adjuntos": adjuntos_de(z),
            }
            for z, o in sorted(obras.items(), key=lambda par: claves[par[0]])
        },
    }
    return referencias, claves, candado


def serializa(dato) -> str:
    return json.dumps(dato, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--comprobar", action="store_true",
                    help="no escribe; sale con 1 si el repo no coincide con Zotero")
    args = ap.parse_args()

    referencias, claves, candado = construye()
    salidas = {
        BIB / "referencias.json": serializa(referencias),
        BIB / "claves.json": serializa(claves),
        BIB / "zotero.lock.json": serializa(candado),
    }

    if args.comprobar:
        distintos = [
            r.name for r, texto in salidas.items()
            if not r.exists() or r.read_text("utf-8") != texto
        ]
        for nombre in distintos:
            print(f"FALLA  bibliografia/{nombre} no coincide con Zotero")
        if not distintos:
            print(f"OK     {len(referencias)} obras; el repo coincide con Zotero")
        return 1 if distintos else 0

    BIB.mkdir(exist_ok=True)
    for ruta, texto in salidas.items():
        ruta.write_text(texto, "utf-8")
    con_pdf = sum(1 for o in candado["obras"].values() if o["adjuntos"])
    print(f"OK     {len(referencias)} obras exportadas ({con_pdf} con PDF) → bibliografia/")
    for clave, o in candado["obras"].items():
        print(f"       {clave:<34} {o['rol']:<15} {'pdf' if o['adjuntos'] else '—'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
