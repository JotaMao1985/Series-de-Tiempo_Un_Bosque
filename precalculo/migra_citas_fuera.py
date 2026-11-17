#!/usr/bin/env python3
"""
migra_citas_fuera.py — saca de git los literales del registro de contraste

Material de Series de Tiempo 2026-II (20948).

El repo es público. Hasta el 2026-11-17 cada fuente de contraste/capN.yml
llevaba en `cita` el literal del pasaje leído (≤ 25 palabras). La norma común de
los cuatro cursos recomienda guardar en git solo el puntero y la huella, y
dejar el literal fuera; Javier lo decidió el 2026-11-17. Este guion:

  1. pasa cada `cita` del registro a bibliografia/_local/citas/capN.yml (fuera
     de git), indexada por id de la afirmación y posición de la fuente (1, 2…);
  2. en el registro, cambia esa línea por `cita_sha256` (sha256 del literal
     normalizado con la `normaliza()` del auditor) y `cita_palabras`;
  3. no toca nada más: cambia solo esas líneas (y la frase de la cabecera que
     decía dónde estaba la cita), y antes de escribir compara campo a campo el
     registro de antes y el de después.

Es reejecutable. Sobre un registro ya migrado no escribe nada: comprueba que
cada fuente tiene su literal local con la huella y el recuento del registro. Una
entrada nueva puede escribirse con `cita:` como antes; al correr este guion sale
del registro (y mientras no salga, el auditor falla con F13).

Uso:  python3 precalculo/migra_citas_fuera.py              # migra lo que haya
      python3 precalculo/migra_citas_fuera.py --comprobar  # no escribe; 1 si
                                                           # queda algo por migrar
Devuelve 1 si algo no cuadra (y entonces no escribe nada).
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import audita_citas as A  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
NUEVOS = ("cita_sha256", "cita_palabras")
RE_LINEA_CITA = re.compile(r"^(?P<sangria>\s+)cita: (?P<valor>.*)$")

CABECERA_VIEJA = """\
# `data-afirma`) con el pasaje LEÍDO que la respalda. La `cita` es literal y
# `precalculo/audita_citas.py` la busca en el texto de la fuente, en la sección
# o página que dice `loc`. Quien verifica no es quien redactó.
"""
CABECERA_NUEVA = """\
# `data-afirma`) con el pasaje LEÍDO que la respalda. La cita literal vive
# fuera de git, en `bibliografia/_local/citas/cap{n}.yml`; aquí quedan su huella
# (`cita_sha256`, del literal normalizado) y su número de palabras, y
# `precalculo/audita_citas.py` busca el literal en el texto de la fuente, en la
# sección o página que dice `loc`. Quien verifica no es quien redactó.
"""

CABECERA_LOCAL = """\
# Literales de las citas del registro de contraste del capítulo {n}
# (bibliografia/contraste/cap{n}.yml). FUERA DE GIT: el repo es público y solo
# guarda la huella de cada literal (`cita_sha256`) y su número de palabras.
# Clave: id de la afirmación → posición de la fuente en su lista (1, 2…).
# Lo escribe precalculo/migra_citas_fuera.py; lo lee precalculo/audita_citas.py (F05, F11).
# No se regenera desde ninguna parte: es dato primario, y hay que copiarlo a
# cada copia de trabajo que audite el registro.
"""


class NoCuadra(Exception):
    pass


def q(texto: str) -> str:
    return json.dumps(texto, ensure_ascii=False)


def sin_cita(f: dict) -> dict:
    return {k: v for k, v in f.items() if k != "cita" and k not in NUEVOS}


def compara(antes: dict, despues: dict, literales: dict[str, dict[int, str]]) -> list[str]:
    """Campo a campo: lo único que cambia es `cita` → `cita_sha256` + `cita_palabras`."""
    p: list[str] = []
    if {k: v for k, v in antes.items() if k != "afirmaciones"} != \
            {k: v for k, v in despues.items() if k != "afirmaciones"}:
        p.append("cambió algo fuera de `afirmaciones`")
    ea, ed = antes.get("afirmaciones") or [], despues.get("afirmaciones") or []
    if [e.get("id") for e in ea] != [e.get("id") for e in ed]:
        return p + ["cambiaron los ids o su orden"]
    for a, d in zip(ea, ed):
        ident = a.get("id")
        if {k: v for k, v in a.items() if k != "fuentes"} != {k: v for k, v in d.items() if k != "fuentes"}:
            campos = sorted(k for k in set(a) | set(d) if k != "fuentes" and a.get(k) != d.get(k))
            p.append(f"{ident}: cambió {campos}")
        fa, fd = a.get("fuentes") or [], d.get("fuentes") or []
        if len(fa) != len(fd):
            p.append(f"{ident}: cambió el número de fuentes")
            continue
        for n, (x, y) in enumerate(zip(fa, fd), start=1):
            if sin_cita(x) != sin_cita(y):
                p.append(f"{ident} · fuente {n}: cambió un campo que no es la cita")
            if "cita" in y:
                p.append(f"{ident} · fuente {n}: el literal sigue en el registro")
            literal = (literales.get(ident) or {}).get(n)
            if literal is None:
                p.append(f"{ident} · fuente {n}: no hay literal local")
                continue
            if "cita" in x and x["cita"] != literal:
                p.append(f"{ident} · fuente {n}: el literal local no es el que había en el registro")
            if y.get("cita_sha256") != A.huella_cita(literal):
                p.append(f"{ident} · fuente {n}: `cita_sha256` no es la huella del literal local")
            if y.get("cita_palabras") != A.palabras_cita(literal):
                p.append(f"{ident} · fuente {n}: `cita_palabras` no es el recuento del literal local")
    return p


def escribe_local(n: int, literales: dict[str, dict[int, str]], orden: list[str]) -> str:
    salida = [CABECERA_LOCAL.format(n=n), f"capitulo: {n}\ncitas:\n"]
    ids = [i for i in orden if i in literales] + sorted(i for i in literales if i not in orden)
    for ident in ids:
        if not literales[ident]:
            continue
        salida.append(f"  {ident}:\n")
        for pos in sorted(literales[ident]):
            salida.append(f"    {pos}: {q(literales[ident][pos])}\n")
    return "".join(salida)


def migra_capitulo(ruta: pathlib.Path, dir_local: pathlib.Path) -> tuple[str | None, str | None, list[str]]:
    """(texto nuevo del registro o None, texto nuevo del archivo local o None, informe)."""
    n = int(re.search(r"cap(\d+)", ruta.name).group(1))
    texto = ruta.read_text("utf-8")
    antes = yaml.safe_load(texto) or {}
    ruta_local = dir_local / f"cap{n}.yml"
    previo = (yaml.safe_load(ruta_local.read_text("utf-8")) or {}) if ruta_local.exists() else {}
    if previo and previo.get("capitulo") != n:
        raise NoCuadra(f"{ruta_local}: dice ser del capítulo {previo.get('capitulo')}")
    literales: dict[str, dict[int, str]] = {str(k): {int(p): str(v) for p, v in (d or {}).items()}
                                            for k, d in (previo.get("citas") or {}).items()}
    literales_previos = copy.deepcopy(literales)

    # 1. Los literales que siguen en el registro, en el orden en que aparecen.
    pendientes: list[tuple[str, int, str]] = []
    for e in antes.get("afirmaciones") or []:
        for pos, f in enumerate(e.get("fuentes") or [], start=1):
            if "cita" not in f:
                continue
            ident, literal = str(e["id"]), str(f["cita"])
            if any(k in f for k in NUEVOS):
                raise NoCuadra(f"{ruta.name} · {ident} · fuente {pos}: tiene `cita` y además huella o "
                               "recuento; decidir a mano cuál vale")
            ya = (literales.get(ident) or {}).get(pos)
            if ya is not None and ya != literal:
                raise NoCuadra(f"{ruta.name} · {ident} · fuente {pos}: el literal local ya existe y es otro")
            literales.setdefault(ident, {})[pos] = literal
            pendientes.append((ident, pos, literal))

    # 2. El cambio en el texto: cada línea `cita:` de una fuente, en ese mismo orden.
    lineas = texto.split("\n")
    nuevas: list[str] = []
    cola = list(pendientes)
    for linea in lineas:
        m = RE_LINEA_CITA.match(linea)
        if not m:
            nuevas.append(linea)
            continue
        if not cola:
            raise NoCuadra(f"{ruta.name}: hay más líneas `cita:` que citas en el registro")
        ident, pos, literal = cola.pop(0)
        valor = m.group("valor")
        if valor.strip()[:1] in (">", "|") or (yaml.safe_load("x: " + valor) or {}).get("x") != literal:
            raise NoCuadra(f"{ruta.name} · {ident} · fuente {pos}: la línea `cita:` no es de una sola línea "
                           "o no es la cita que lee YAML; migrarla a mano")
        s = m.group("sangria")
        nuevas.append(f'{s}cita_sha256: "{A.huella_cita(literal)}"')
        nuevas.append(f"{s}cita_palabras: {A.palabras_cita(literal)}")
    if cola:
        raise NoCuadra(f"{ruta.name}: {len(cola)} citas sin su línea `cita:` en el texto")
    texto_nuevo = "\n".join(nuevas)
    if CABECERA_VIEJA in texto_nuevo:
        texto_nuevo = texto_nuevo.replace(CABECERA_VIEJA, CABECERA_NUEVA.format(n=n), 1)

    # 3. Campo a campo, antes y después.
    despues = yaml.safe_load(texto_nuevo) or {}
    problemas = compara(antes, despues, literales)
    if problemas:
        raise NoCuadra(f"{ruta.name}: " + "; ".join(problemas[:10]))
    orden = [str(e["id"]) for e in despues.get("afirmaciones") or []]
    texto_local = escribe_local(n, literales, orden)
    releido = {str(k): {int(p): v for p, v in d.items()}
               for k, d in ((yaml.safe_load(texto_local) or {}).get("citas") or {}).items()}
    if releido != {k: v for k, v in literales.items() if v}:
        raise NoCuadra(f"cap{n}.yml local: al releerlo no da los mismos literales")

    total = sum(len(e.get("fuentes") or []) for e in despues.get("afirmaciones") or [])
    huerfanos = sorted(f"{i}#{p}" for i, d in literales.items() for p in d
                       if not any(str(e["id"]) == i and p <= len(e.get("fuentes") or [])
                                  for e in despues.get("afirmaciones") or []))
    informe = [f"{ruta.name}: {total} fuentes · {len(pendientes)} literales salen del registro · "
               f"{total - len(pendientes)} ya estaban fuera y cuadran"]
    if huerfanos:
        informe.append(f"  aviso: {len(huerfanos)} literales locales sin fuente en el registro: {huerfanos[:5]}")
    cambia_registro = texto_nuevo != texto
    cambia_local = literales != literales_previos or not ruta_local.exists()
    return (texto_nuevo if cambia_registro else None,
            texto_local if cambia_local else None, informe)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--comprobar", action="store_true", help="no escribe; sale con 1 si queda algo por migrar")
    ap.add_argument("--bib", type=pathlib.Path, default=RAIZ / "bibliografia")
    args = ap.parse_args()
    dir_local = args.bib / "_local" / "citas"

    planes = []
    try:
        for ruta in sorted((args.bib / "contraste").glob("cap*.yml")):
            planes.append((ruta, *migra_capitulo(ruta, dir_local)))
    except NoCuadra as e:
        print(f"FALLA  {e}\n       no se escribió nada")
        return 1

    pendiente = False
    for ruta, registro, local, informe in planes:
        print("OK     " + "\n".join(informe))
        n = int(re.search(r"cap(\d+)", ruta.name).group(1))
        ruta_local = dir_local / f"cap{n}.yml"
        if registro is None and local is None:
            continue
        pendiente = True
        if args.comprobar:
            print(f"       por migrar: {'el registro ' if registro else ''}{'el archivo local' if local else ''}")
            continue
        # Primero el literal, fuera de git; después el registro sin él.
        if local is not None:
            dir_local.mkdir(parents=True, exist_ok=True)
            ruta_local.write_text(local, "utf-8")
            print(f"       escrito {ruta_local.relative_to(args.bib.parent)}")
        if registro is not None:
            ruta.write_text(registro, "utf-8")
            print(f"       escrito {ruta.relative_to(args.bib.parent)}")

    if args.comprobar:
        print("FALLA  quedan literales por migrar" if pendiente else "OK     nada por migrar")
        return 1 if pendiente else 0
    # Reejecución inmediata: ya no debe quedar nada por hacer.
    if pendiente:
        for ruta in sorted((args.bib / "contraste").glob("cap*.yml")):
            registro, local, _ = migra_capitulo(ruta, dir_local)
            if registro is not None or local is not None:
                print(f"FALLA  {ruta.name}: tras escribir, una segunda pasada aún cambiaría algo")
                return 1
        print("OK     segunda pasada: nada por migrar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
