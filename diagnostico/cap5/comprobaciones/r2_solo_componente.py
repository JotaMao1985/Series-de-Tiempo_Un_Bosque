#!/usr/bin/env python3
"""R2 del cap. 5 · los capítulos 1 y 6, la plantilla y la guía del proyecto cambian SOLO en el componente.

Para cada archivo toma su versión en HEAD, sustituye los dos bloques del componente `.mapa-estacional`
(el CSS, del comentario «Componente .mapa-estacional» al cierre de su media query de 640 px, y el JS,
del rótulo del componente al cierre de `iniciarMapasEstacionales`) por los de
`ensamblado/componentes/`, y compara el resultado con el archivo de trabajo: si son idénticos byte a
byte, no ha cambiado nada más. Es la misma operación que `retropropaga_mapa.py --actualiza`, hecha
aquí aparte sobre HEAD.

Uso: python3 diagnostico/cap5/comprobaciones/r2_solo_componente.py [--base REV]
"""
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
ARCHIVOS = ["Htmls_Series/capitulo-1-componentes-descomposicion.html",
            "plantilla/plantilla-capitulo.html",
            "Htmls_Series/capitulo-6-pronostico-evaluacion.html",
            "Htmls_Series/proyecto-pronostico-corte-iii.html"]
INICIO_CSS = ("    /* ------------------------------------------------------------------\n"
              "       Componente .mapa-estacional — mapa de calor mes x año")
FIN_CSS, CIERRE_CSS = "    @media (max-width: 640px) {\n      .mapa-estacional-rejilla {", "\n      }\n    }"
INICIO_JS = ("    // ================================================================\n"
             "    // Componente .mapa-estacional — mapa de calor mes x año")
FIN_JS, CIERRE_JS = "    function iniciarMapasEstacionales() {", "\n    }"

rev = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "HEAD"
css = (RAIZ / "ensamblado/componentes/mapa_estacional.css").read_text(encoding="utf-8").strip("\n")
js = (RAIZ / "ensamblado/componentes/mapa_estacional.js").read_text(encoding="utf-8").rstrip("\n")


def bloque(html, inicio, fin, cierre):
    assert html.count(inicio) == 1, inicio[:60]
    i = html.index(inicio)
    j = html.index(cierre, html.index(fin, i)) + len(cierre)
    return i, j


fallos = 0
for archivo in ARCHIVOS:
    viejo = subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                           text=True, check=True).stdout
    nuevo = (RAIZ / archivo).read_text(encoding="utf-8")
    i, j = bloque(viejo, INICIO_CSS, FIN_CSS, CIERRE_CSS)
    esperado = viejo[:i] + css + viejo[j:]
    a, b = bloque(esperado, INICIO_JS, FIN_JS, CIERRE_JS)
    esperado = esperado[:a] + js + esperado[b:]
    igual = esperado == nuevo
    fallos += not igual
    cambia = viejo != nuevo
    print(f"{archivo}: {'cambia' if cambia else 'NO cambia'}; "
          f"{'idéntico a ' + rev + ' con el componente nuevo y nada más' if igual else 'DIFIERE de ' + rev + ' + componente'}")
sys.exit(1 if fallos else 0)
