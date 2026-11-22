#!/usr/bin/env python3
"""R5 del capítulo 3 · aplica la ronda de práctica sobre los archivos del commit base.

Reejecutable: no parte de los archivos de trabajo sino de `git show <BASE>:...`, así que correrlo
dos veces da el mismo resultado. Pasos:
  r5_ediciones_cortos    los ocho «Para practicar» (T5.1)            -> cap3_modulos.html
  r5_ediciones_m10       los ejercicios 1, 2 y 3 (T5.2)              -> cap3_modulos.html
  NOTACION               «el envolvente» -> «la envolvente» (R3)     -> cap3_modulos.html
  r5_ediciones_quiz      AUTOEVALUACIONES['cap3'] y el simulador psi -> cap3_js.js
  r5_ediciones_minutos   los minutos declarados (D7)                 -> ensambla_cap3.py

Archivos que toca: ensamblado/cap3/cap3_modulos.html, ensamblado/cap3/cap3_js.js y
ensamblado/ensambla_cap3.py (solo `courseData.modules` y su comentario).

Uso (desde la raíz del repo):
    python3 diagnostico/cap3/comprobaciones/r5_edita.py
Después, en este orden:
    python3 ensamblado/ensambla_cap3.py --escribir
    python3 ensamblado/ensambla_cap4.py; python3 ensamblado/ensambla_cap5.py; python3 ensamblado/ensambla_cap6.py
y `git diff --stat` no debe mostrar los capítulos 4 a 6.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI))
import r5_ediciones_cortos, r5_ediciones_m10, r5_ediciones_quiz, r5_ediciones_minutos  # noqa: E402

BASE = "5c2fdb3"
MOD = "ensamblado/cap3/cap3_modulos.html"
JS = "ensamblado/cap3/cap3_js.js"
ENS = "ensamblado/ensambla_cap3.py"

NOTACION = [
    ("el módulo manda en la amplitud —el\n        envolvente $\\pm R^{\\,j}/\\sin\\omega",
     "el módulo manda en la amplitud —la\n        envolvente $\\pm R^{\\,j}/\\sin\\omega"),
    ('<p class="simulador-intro">Los pesos $\\psi_j$ de la tabla, con el envolvente\n',
     '<p class="simulador-intro">Los pesos $\\psi_j$ de la tabla, con la envolvente\n'),
]


def base(ruta):
    return subprocess.run(["git", "show", f"{BASE}:{ruta}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout


def marcadas(texto):
    """Las líneas que llevan `data-afirma` o `<cite`: no deben cambiar (firma de la R4)."""
    return [l for l in texto.splitlines() if "data-afirma" in l or "<cite" in l]


mod0 = base(MOD)
mod = r5_ediciones_cortos.aplica(mod0)
mod = r5_ediciones_m10.aplica(mod)
for antes, despues in NOTACION:
    assert mod.count(antes) == 1, antes
    mod = mod.replace(antes, despues)
js0 = base(JS)
js = r5_ediciones_quiz.aplica(js0)
ens0 = base(ENS)
ens = r5_ediciones_minutos.aplica(ens0)

# Ninguna frase marcada cambia y no se añade ningún data-afirma. Se compara elemento a elemento
# (los seis de los ejercicios, que se copian byte a byte) y línea a línea (todo lo demás): las
# únicas líneas con `data-afirma` que pueden diferir son las tres en que la prosa NO marcada de
# la misma línea cambió (c3-m10-33, c3-m10-90 y c3-m10-34). La comprobación que manda es F09 de
# `audita_citas.py`, que compara la huella del texto de cada elemento.
a0, a1 = marcadas(mod0), marcadas(mod)
distintas = sorted(set(a0) ^ set(a1))
ids = sorted({i for l in distintas for i in re.findall(r'data-afirma="([^"]+)"', l)})
print(f"líneas con data-afirma o <cite>: {len(a0)} antes, {len(a1)} después; ids en líneas que cambian: {ids}")
assert ids == ["c3-m10-33", "c3-m10-34", "c3-m10-90"], ids
for i in ("c3-m10-31", "c3-m10-33", "c3-m10-90", "c3-m10-34", "c3-m10-46"):
    assert r5_ediciones_m10.marcado(mod0, i) == r5_ediciones_m10.marcado(mod, i), i
li = lambda t: t[t.index('<li data-afirma="c3-m10-35">'):t.index("</li>", t.index('<li data-afirma="c3-m10-35">'))]
assert li(mod0) == li(mod)
assert sorted(re.findall(r'data-afirma="([^"]+)"', mod0)) == sorted(re.findall(r'data-afirma="([^"]+)"', mod)), "cambió el conjunto de ids"
assert "data-afirma" not in js and "data-afirma" not in js0
print("los seis elementos marcados de los ejercicios, idénticos byte a byte; mismo conjunto de ids")

for ruta, antes, despues in ((MOD, mod0, mod), (JS, js0, js), (ENS, ens0, ens)):
    (RAIZ / ruta).write_text(despues, encoding="utf-8")
    print(f"{ruta}: {len(antes.splitlines())} -> {len(despues.splitlines())} líneas · md5 {hashlib.md5(despues.encode()).hexdigest()[:12]}")
