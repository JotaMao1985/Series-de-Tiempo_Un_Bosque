#!/usr/bin/env python3
"""
genera_referencias.py — las citas y las listas de referencias, generadas

Material de Series de Tiempo 2026-II (20948).

Nadie escribe a mano «(Cleveland et al., 1990, §2)» ni una entrada de la lista
de referencias: quien redacta deja en el HTML solo la clave de la obra y el
localizador, y este guion escribe el resto con pandoc `--citeproc` y el estilo
APA 7 en español (`bibliografia/apa-es.csl`) a partir de
`bibliografia/referencias.json`, que a su vez sale de Zotero.

Lo que escribe quien redacta:

    <cite class="cita" data-ref="cleveland1990stl" data-loc="§2"></cite>

  · `data-ref`   clave de la obra en referencias.json
  · `data-loc`   localizador, tal como debe leerse: «§3.6», «p. 15», «cap. 2»
  · `data-modo`  `parentesis` (por defecto) → (Cleveland et al., 1990, §2)
                 `narrativa`               → Cleveland et al. (1990, §2)
                 `suelta`                  → Cleveland et al., 1990, §2

Y tres pares de marcadores, que este guion rellena:

    <!--FUENTES-MODULO:inicio-->  … <!--FUENTES-MODULO:fin-->
        dentro de un <template id="module-N">: las obras citadas en ese módulo.
        Cada cita enlaza aquí, porque solo el módulo abierto está en el DOM.
    <!--REFERENCIAS-CAPITULO:inicio--> … <!--REFERENCIAS-CAPITULO:fin-->
        todas las obras citadas en el capítulo.
    <!--PIE-REFERENCIAS:inicio--> … <!--PIE-REFERENCIAS:fin-->
        la bibliografía básica del curso (rol `basica` en zotero.lock.json).

Es idempotente: volver a correrlo sobre un archivo ya generado no cambia nada.
`audita_citas.py` (F02) se apoya en eso para comprobar que el HTML publicado
es exactamente el que este guion escribiría.

Uso:  python3 precalculo/genera_referencias.py                 # los 6 capítulos
      python3 precalculo/genera_referencias.py ruta/al.html …
      python3 precalculo/genera_referencias.py --comprobar     # no escribe

Los capítulos 3–6 se ensamblan: ahí el guion hay que pasarlo sobre las fuentes
de `ensamblado/capN/` y reensamblar, no sobre el HTML final.
"""
from __future__ import annotations

import argparse
import copy
import html
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BIB = RAIZ / "bibliografia"
SITIO = RAIZ / "Htmls_Series"
CAPITULOS = sorted(SITIO.glob("capitulo-*.html"))

RE_CITA = re.compile(r'<cite class="cita"(?P<atributos>[^>]*)>(?P<dentro>.*?)</cite>', re.S)
RE_ATRIBUTO = re.compile(r'(data-[a-z]+)="([^"]*)"')
RE_MODULO = re.compile(
    r'(?P<abre><template id="module-(?P<n>\d+)">)(?P<cuerpo>.*?)(?P<cierra></template>)', re.S
)
MODOS = ("parentesis", "narrativa", "suelta")


def marcadores(nombre: str) -> re.Pattern:
    return re.compile(
        rf"(?P<abre><!--{nombre}:inicio-->)(?P<dentro>.*?)(?P<cierra><!--{nombre}:fin-->)", re.S
    )


RE_FUENTES_MODULO = marcadores("FUENTES-MODULO")
RE_REFS_CAPITULO = marcadores("REFERENCIAS-CAPITULO")
RE_PIE = marcadores("PIE-REFERENCIAS")


class ErrorDeCita(Exception):
    pass


# --------------------------------------------------------------------------- #
# Biblioteca
# --------------------------------------------------------------------------- #
def carga_biblioteca() -> tuple[dict[str, dict], dict[str, dict]]:
    referencias = json.loads((BIB / "referencias.json").read_text("utf-8"))
    candado = json.loads((BIB / "zotero.lock.json").read_text("utf-8"))["obras"]
    return {r["id"]: r for r in referencias}, candado


def para_pandoc(obras: list[dict]) -> list[dict]:
    """Copia de las obras con el rango de páginas en raya corta (3–73)."""
    salida = copy.deepcopy(obras)
    for o in salida:
        if isinstance(o.get("page"), str):
            o["page"] = re.sub(r"(?<=\d)\s*-+\s*(?=\d)", "–", o["page"])
    return salida


def pandoc(biblioteca: dict[str, dict], claves: list[str]) -> tuple[dict, dict, dict]:
    """Devuelve ({clave: autores}, {clave: año}, {clave: entrada HTML}).

    Todas las claves van en UNA pasada para que la desambiguación de citeproc
    (1990a, 1990b) sea la misma en las citas y en la lista.
    """
    if not claves:
        return {}, {}, {}
    obras = para_pandoc([biblioteca[c] for c in claves])
    cuerpo = "\n\n".join(f"@{c}\n\n[-@{c}]" for c in claves)
    documento = f'---\nlang: es\nnocite: "@*"\n---\n\n{cuerpo}\n'
    ruta_json = BIB / "_local" / "pandoc-entrada.json"
    ruta_json.parent.mkdir(parents=True, exist_ok=True)
    ruta_json.write_text(json.dumps(obras, ensure_ascii=False), "utf-8")
    proceso = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html", "--wrap=none", "--citeproc",
         "--bibliography", str(ruta_json), "--csl", str(BIB / "apa-es.csl")],
        input=documento, capture_output=True, text=True,
    )
    ruta_json.unlink()
    if proceso.returncode != 0:
        raise ErrorDeCita(f"pandoc falló: {proceso.stderr.strip()}")
    salida = proceso.stdout

    spans = re.findall(r'<span class="citation" data-cites="([^"]+)">(.*?)</span>', salida, re.S)
    autores, anios = {}, {}
    for clave, texto in spans:
        m = re.fullmatch(r"\((.*)\)", texto.strip(), re.S)
        if m:                                   # [-@clave] → «(1990)»
            anios[clave] = m.group(1)
        else:                                   # @clave → «Cleveland et al. (1990)»
            autores[clave] = re.sub(r"\s*\([^()]*\)\s*$", "", texto.strip())
    entradas = dict(re.findall(
        r'<div id="ref-([^"]+)" class="csl-entry"[^>]*>\s*(.*?)\s*</div>', salida, re.S
    ))
    faltan = [c for c in claves if c not in autores or c not in anios or c not in entradas]
    if faltan:
        raise ErrorDeCita(f"pandoc no devolvió cita o entrada para: {', '.join(faltan)}")
    return autores, anios, entradas


def enlaces_nuevos(entrada: str) -> str:
    """Los enlaces de una entrada abren en pestaña nueva."""
    return entrada.replace('<a href="', '<a target="_blank" rel="noopener" href="')


# --------------------------------------------------------------------------- #
# Citas
# --------------------------------------------------------------------------- #
def atributos_de(texto: str) -> dict[str, str]:
    return {k: html.unescape(v) for k, v in RE_ATRIBUTO.findall(texto)}


def texto_cita(autores: str, anio: str, loc: str, modo: str) -> str:
    cola = f", {html.escape(loc, quote=False)}" if loc else ""
    if modo == "narrativa":
        return f"{autores} ({anio}{cola})"
    if modo == "suelta":
        return f"{autores}, {anio}{cola}"
    return f"({autores}, {anio}{cola})"


def claves_citadas(texto: str) -> list[str]:
    vistas: list[str] = []
    for m in RE_CITA.finditer(texto):
        clave = atributos_de(m.group("atributos")).get("data-ref", "")
        if clave and clave not in vistas:
            vistas.append(clave)
    return vistas


def lista(entradas: dict[str, str], claves: list[str], prefijo: str, sangria: str) -> str:
    orden = sorted(claves, key=lambda c: re.sub(r"<[^>]+>", "", entradas[c]).lower())
    filas = "".join(
        f'\n{sangria}  <li id="{prefijo}{c}">{enlaces_nuevos(entradas[c])}</li>' for c in orden
    )
    return f'\n{sangria}<ul class="lista-fuentes">{filas}\n{sangria}</ul>\n{sangria}'


def sangria_de(texto: str, posicion: int) -> str:
    inicio = texto.rfind("\n", 0, posicion) + 1
    return re.match(r"[ \t]*", texto[inicio:posicion]).group(0)


def genera(texto: str, biblioteca: dict[str, dict], candado: dict[str, dict]) -> str:
    """El HTML con citas, listas de módulo, lista de capítulo y pie regenerados."""
    citadas = claves_citadas(texto)
    desconocidas = [c for c in citadas if c not in biblioteca]
    if desconocidas:
        raise ErrorDeCita(f"claves que no están en referencias.json: {', '.join(desconocidas)}")
    autores, anios, entradas = pandoc(biblioteca, citadas)

    def modulo(m: re.Match) -> str:
        n, cuerpo = m.group("n"), m.group("cuerpo")

        def cita(c: re.Match) -> str:
            a = atributos_de(c.group("atributos"))
            clave, loc = a.get("data-ref", ""), a.get("data-loc", "")
            modo = a.get("data-modo", "parentesis")
            if modo not in MODOS:
                raise ErrorDeCita(f"data-modo desconocido en la cita de {clave}: «{modo}»")
            titulo = html.escape(re.sub(r"<[^>]+>", "", entradas[clave]).strip(), quote=True)
            visible = texto_cita(autores[clave], anios[clave], loc, modo)
            return (f'<cite class="cita"{c.group("atributos")}>'
                    f'<a href="#ref-m{n}-{clave}" title="{titulo}">{visible}</a></cite>')

        cuerpo = RE_CITA.sub(cita, cuerpo)
        del_modulo = claves_citadas(cuerpo)

        def fuentes(f: re.Match) -> str:
            if not del_modulo:
                return f.group("abre") + f.group("cierra")
            s = sangria_de(cuerpo, f.start())
            return (f.group("abre") + lista(entradas, del_modulo, f"ref-m{n}-", s)
                    + f.group("cierra"))

        cuerpo = RE_FUENTES_MODULO.sub(fuentes, cuerpo)
        return m.group("abre") + cuerpo + m.group("cierra")

    texto = RE_MODULO.sub(modulo, texto)

    def capitulo(m: re.Match) -> str:
        if not citadas:
            return m.group("abre") + m.group("cierra")
        s = sangria_de(texto, m.start())
        return m.group("abre") + lista(entradas, citadas, "ref-", s) + m.group("cierra")

    texto = RE_REFS_CAPITULO.sub(capitulo, texto)

    if RE_PIE.search(texto):
        basicas = [c for c, o in candado.items() if o["rol"] == "basica"]
        _, _, del_pie = pandoc(biblioteca, basicas)

        def pie(m: re.Match) -> str:
            s = sangria_de(texto, m.start())
            return m.group("abre") + lista(del_pie, basicas, "pie-", s) + m.group("cierra")

        texto = RE_PIE.sub(pie, texto)
    return texto


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("archivos", nargs="*", type=pathlib.Path)
    ap.add_argument("--comprobar", action="store_true",
                    help="no escribe; sale con 1 si algún archivo quedaría distinto")
    args = ap.parse_args()

    biblioteca, candado = carga_biblioteca()
    falla = False
    for ruta in (args.archivos or CAPITULOS):
        original = ruta.read_text("utf-8")
        try:
            nuevo = genera(original, biblioteca, candado)
        except ErrorDeCita as e:
            print(f"FALLA  {ruta.name}: {e}")
            falla = True
            continue
        n = len(RE_CITA.findall(nuevo))
        if nuevo == original:
            print(f"OK     {ruta.name}: {n} citas, sin cambios")
        elif args.comprobar:
            print(f"FALLA  {ruta.name}: las citas o las listas no están regeneradas")
            falla = True
        else:
            ruta.write_text(nuevo, "utf-8")
            print(f"OK     {ruta.name}: {n} citas, regenerado")
    return 1 if falla else 0


if __name__ == "__main__":
    sys.exit(main())
