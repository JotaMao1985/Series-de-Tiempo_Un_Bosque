"""Verificador independiente R2 cap. 5: los caps. 1 y 6, la plantilla y la guía
cambian solo dentro de los bloques del componente .mapa-estacional.
Recorta en HEAD y en el árbol el bloque CSS (comentario del componente hasta el
cierre de su @media 640) y el JS (rótulo hasta el cierre de
iniciarMapasEstacionales) y compara el resto con difflib."""
import subprocess, difflib, re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
ARCH = ["Htmls_Series/capitulo-1-componentes-descomposicion.html",
        "Htmls_Series/capitulo-6-pronostico-evaluacion.html",
        "plantilla/plantilla-capitulo.html",
        "Htmls_Series/proyecto-pronostico-corte-iii.html",
        "Htmls_Series/capitulo-5-sarima.html"]
CSS_I = "Componente .mapa-estacional — mapa de calor mes x año\n       ----"
JS_I = "// Componente .mapa-estacional — mapa de calor mes x año\n    // ===="
def recorta(t):
    out = t
    # CSS: desde la línea de apertura del comentario hasta el cierre de la @media 640 que sigue
    i = out.find(CSS_I)
    if i >= 0:
        i = out.rfind("/* ----", 0, i)
        k = out.find("@media (max-width: 640px) {\n      .mapa-estacional-rejilla", i)
        j = out.find("\n      }\n    }", k) + len("\n      }\n    }")
        out = out[:i] + "<<CSS-COMPONENTE>>" + out[j:]
    i = out.find(JS_I)
    if i >= 0:
        i = out.rfind("// ====", 0, i)
        k = out.find("function iniciarMapasEstacionales() {", i)
        j = out.find("\n    }", k) + len("\n    }")
        out = out[:i] + "<<JS-COMPONENTE>>" + out[j:]
    return out
for a in ARCH:
    viejo = subprocess.run(["git", "show", "HEAD:" + a], cwd=RAIZ, capture_output=True, text=True).stdout
    nuevo = (RAIZ / a).read_text(encoding="utf-8")
    rv, rn = recorta(viejo), recorta(nuevo)
    d = [l for l in difflib.unified_diff(rv.splitlines(), rn.splitlines(), lineterm="", n=0)
         if not l.startswith(("---", "+++"))]
    print(f"== {a}: {len(viejo)} -> {len(nuevo)} chars; fuera del componente: "
          f"{sum(1 for l in d if l[:1] in '+-')} líneas distintas")
    if "capitulo-5" not in a:
        for l in d[:40]:
            print("   ", l[:160])
