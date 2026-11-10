#!/usr/bin/env python3
"""
verifica_todo.py — todos los verificadores del sitio, de una sola vez

Material de Series de Tiempo 2026-II (20948).

El repo tenía una docena de verificadores y ningún sitio desde donde correrlos
todos: cada ronda ejecutaba los que recordaba. Este guion los corre en orden,
dice cuál falla y enseña las últimas líneas de su salida. No arregla nada.

Solo incluye verificadores que NO escriben. Quedan fuera, a propósito:

  · ensambla_cap4.py, ensambla_cap5.py, ensambla_cap6.py: son reejecutables,
    pero escriben el capítulo. Para comprobarlos: correrlos y mirar que
    `git status` no cambie.
  · verifica_bloques_cap6.py, verifica_cap5_python.py, verifica_excel_cap5.py:
    ejecutan R, Python y Excel de verdad y tardan minutos. Se piden con --lento.

Uso:  python3 precalculo/verifica_todo.py            # lo rápido (segundos)
      python3 precalculo/verifica_todo.py --lento    # además, los que ejecutan código
      python3 precalculo/verifica_todo.py --red      # además, DOI y enlaces externos
      python3 precalculo/verifica_todo.py --zotero   # además, que el repo coincida
                                                     # con Zotero (tiene que estar abierto)

Devuelve 1 si alguno falla.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent

RAPIDOS = [
    ("el auditor de citas atrapa sus defectos", ["precalculo/prueba_audita_citas.py"]),
    ("ninguna cita de memoria", ["precalculo/audita_citas.py"]),
    ("citas y listas regeneradas", ["precalculo/genera_referencias.py", "--comprobar"]),
    ("contrato curso → vault al día", ["precalculo/audita_citas.py", "--uso-comprobar"]),
    ("cifras del sitio contadas", ["precalculo/cuenta_sitio.py"]),
    ("reparto de la opción correcta", ["precalculo/audita_posicion_correcta.py"]),
    ("alineación de ítems y módulos", ["precalculo/audita_alineacion_modulos.py"]),
    ("Tailwind compilado al día", ["precalculo/compila_tailwind.py", "--comprobar"]),
    ("capítulo 3 reproducible", ["ensamblado/ensambla_cap3.py"]),
    ("guía del proyecto reproducible", ["precalculo/ensambla_proyecto.py", "--revisar"]),
    ("auditoría de la guía del proyecto", ["proyecto/audita_proyecto.py"]),
]
LENTOS = [
    ("bloques de código del capítulo 6", ["precalculo/verifica_bloques_cap6.py"]),
    ("SARIMA en R y en Python", ["precalculo/verifica_cap5_python.py"]),
    ("libros de Excel del capítulo 5", ["precalculo/verifica_excel_cap5.py"]),
]


def corre(nombre: str, orden: list[str]) -> bool:
    inicio = time.time()
    p = subprocess.run([sys.executable, *orden], cwd=RAIZ, capture_output=True, text=True)
    segundos = time.time() - inicio
    bien = p.returncode == 0
    print(f"{'OK    ' if bien else 'FALLA '} {nombre:<38} {' '.join(orden):<52} {segundos:5.1f} s")
    if not bien:
        cola = (p.stdout + p.stderr).strip().splitlines()[-12:]
        for linea in cola:
            print(f"         │ {linea[:150]}")
    return bien


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--lento", action="store_true", help="incluye los que ejecutan R, Python y Excel")
    ap.add_argument("--red", action="store_true", help="incluye DOI y enlaces externos")
    ap.add_argument("--zotero", action="store_true", help="comprueba el repo contra Zotero abierto")
    args = ap.parse_args()

    lista = list(RAPIDOS)
    if args.red:
        lista.append(("DOI y enlaces externos", ["precalculo/audita_citas.py", "--red"]))
    if args.zotero:
        lista.append(("el repo coincide con Zotero", ["precalculo/exporta_zotero.py", "--comprobar"]))
    if args.lento:
        lista += LENTOS

    fallas = [nombre for nombre, orden in lista if not corre(nombre, orden)]
    print()
    if fallas:
        print(f"FALLA  {len(fallas)} de {len(lista)}: " + "; ".join(fallas))
        return 1
    print(f"OK     {len(lista)} verificadores en verde")
    return 0


if __name__ == "__main__":
    sys.exit(main())
