#!/usr/bin/env python3
"""R5 del capítulo 2 · aplica la ronda entera sobre el capítulo de HEAD.

Reejecutable: no parte del archivo de trabajo sino de `git show <BASE>:...`, así que
correrlo dos veces da el mismo resultado. Orden: los siete ejercicios cortos (T5.1), los
cinco del Módulo 9 (T5.3), el quiz (T5.2) y los minutos declarados.

Desde la raíz del repo:  python3 diagnostico/cap2/comprobaciones/r5_edita.py
"""
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI))
import r5_ediciones_cortos, r5_ediciones_m9, r5_ediciones_quiz, r5_ediciones_minutos  # noqa: E402

BASE = "51a5c88"
RUTA = "Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html"
src = subprocess.run(["git", "show", f"{BASE}:{RUTA}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
n0 = len(src.splitlines())
for paso in (r5_ediciones_m9, r5_ediciones_quiz, r5_ediciones_cortos, r5_ediciones_minutos):
    src = paso.aplica(src)
(RAIZ / RUTA).write_text(src, encoding="utf-8")
print(f"{RUTA}: {n0} -> {len(src.splitlines())} líneas")
