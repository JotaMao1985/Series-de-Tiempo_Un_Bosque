#!/usr/bin/env python3
"""R5 del capítulo 4 · aplica la ronda de práctica sobre los archivos del commit base.

Reejecutable: no parte de los archivos de trabajo sino de `git show <BASE>:...`, así que correrlo
dos veces da el mismo resultado. Pasos:
  r5_ediciones_cortos    los nueve «Para practicar» de M1 a M9 (T5.1)   -> templates_1_3, _4_6, _7_9
  r5_ediciones_m10       los ejercicios 1, 2 y 3 (T5.2) y las dos frases de M8 y M9 que los resolvían
                                                                        -> templates_10, templates_7_9
  r5_ediciones_quiz      AUTOEVALUACIONES['cap4']                        -> chapter.js
  r5_ediciones_minutos   minutos declarados (D7) y recuento de ejercicios -> ensambla_cap4.py

Uso (desde la raíz del repo):
    python3 diagnostico/cap4/comprobaciones/r5_edita.py
Después, en este orden:
    python3 ensamblado/ensambla_cap4.py; python3 ensamblado/ensambla_cap5.py; python3 ensamblado/ensambla_cap6.py
y `git diff --stat` no debe mostrar los capítulos 5 y 6.

Comprueba al escribir que los elementos con `data-afirma` (firma de la R4) son los mismos, con el
mismo contenido byte a byte, y que no hay ninguno nuevo.
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

BASE = "b53fdcb"
PLANTILLAS = ["templates_1_3.html", "templates_4_6.html", "templates_7_9.html", "templates_10.html"]
JS = "ensamblado/cap4/chapter.js"
ENS = "ensamblado/ensambla_cap4.py"
MINUTOS_QUIZ = 23       # lectura de la autoevaluación, de r5_minutos_despues.out


def base(ruta):
    return subprocess.run(["git", "show", f"{BASE}:{ruta}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout


def marcas(texto):
    """{id: elemento entero} de cada `<span data-afirma="...">…</span>`."""
    salida = {}
    for m in re.finditer(r'<span data-afirma="([^"]+)">', texto):
        salida[m.group(1)] = r5_ediciones_m10.marca(texto, m.group(1))
    return salida


antes = {n: base(f"ensamblado/cap4/{n}") for n in PLANTILLAS}
despues = r5_ediciones_cortos.aplica(dict(antes))
despues = r5_ediciones_m10.aplica(despues)

m0, m1 = {}, {}
for n in PLANTILLAS:
    m0.update(marcas(antes[n])); m1.update(marcas(despues[n]))
# La maestra retiró una marca en la R5: c4-m10-69 quedaba pegada a c4-m10-68, que dice lo mismo con la
# misma cita (ver r5_registro_maestra.py). Es la única que puede faltar, y con ella, su <cite>.
RETIRADAS = {"c4-m10-69"}
assert set(m0) - RETIRADAS == set(m1), (set(m0) ^ set(m1))
cambiadas = [k for k in m1 if m0[k] != m1[k]]
assert not cambiadas, cambiadas
assert sum(t.count("<cite") for t in antes.values()) - len(RETIRADAS) == sum(t.count("<cite") for t in despues.values())

js = r5_ediciones_quiz.aplica(base(JS))
ens = r5_ediciones_minutos.aplica(base(ENS), MINUTOS_QUIZ)

for n in PLANTILLAS:
    (RAIZ / "ensamblado" / "cap4" / n).write_text(despues[n], encoding="utf-8")
(RAIZ / JS).write_text(js, encoding="utf-8")
(RAIZ / ENS).write_text(ens, encoding="utf-8")

print(f"marcas data-afirma en las cuatro plantillas: {len(m0)} antes, {len(m1)} después; ninguna cambia de contenido")
for ruta in [f"ensamblado/cap4/{n}" for n in PLANTILLAS] + [JS, ENS]:
    t = (RAIZ / ruta).read_text(encoding="utf-8")
    print(f"  {hashlib.md5(t.encode()).hexdigest()}  {len(t.splitlines()):>5} líneas  {ruta}")
