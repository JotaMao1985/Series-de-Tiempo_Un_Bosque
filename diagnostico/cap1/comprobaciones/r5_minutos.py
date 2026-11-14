#!/usr/bin/env python3
"""R5 · minutos de lectura por módulo del capítulo 1, con la fórmula de la R3.

Es `r3b_cuenta_sin_codigo.py` (R3) con dos cambios: lee `courseData` con el
campo `sesion` que añadió la R3-bis, y separa lo que la R5 añadió, para que se
vea de dónde sale cada minuto.

Fórmula de la R3, sin tocar:
    minutos = palabras de prosa / 180  +  3 por simulador  +  2 por bloque de código
(los desarrollos plegables, `.derivacion-panel`, no cuentan; un par de pestañas
R/Python cuenta como un bloque).

Columnas:
  «cerrado»  — el módulo con las pistas y las soluciones de sus ejercicios sin
               abrir: del ejercicio solo se lee el enunciado (y, en el M2, su
               código de partida).
  «abierto»  — además se leen la pista y la solución, con su código.
Ninguna de las dos incluye el tiempo de HACER el ejercicio.

Uso:  python3 diagnostico/cap1/comprobaciones/r5_minutos.py [ruta.html ...]
"""
import html
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
RUTA = "Htmls_Series/capitulo-1-componentes-descomposicion.html"
INLINE = r'(?:code|strong|em|a|span|cite|sub|sup|i|b|kbd)'


def texto(h):
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r'<(script|style|canvas|svg)\b.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<aside class="fuentes-modulo".*?</aside>', ' ', h, flags=re.S)
    h = re.sub(r'<caption class="sr-only".*?</caption>', ' ', h, flags=re.S)
    h = re.sub(r'<button\b.*?</button>', ' ', h, flags=re.S)
    h = re.sub(r'<div class="quiz".*?<div class="quiz-marcador">.*?</div>\s*</div>', ' ', h, flags=re.S)
    h = re.sub(r'<(/?)' + INLINE + r'\b[^>]*>', '', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = html.unescape(h).replace('\xa0', ' ')
    h = h.replace('$seasonal', 'seasonal')
    h = re.sub(r'\$\$.*?\$\$', ' ', h, flags=re.S)
    h = re.sub(r'\$[^$]*\$', ' M ', h)
    return h


def n(h):
    return len(texto(h).split())


def mide(src):
    decl = {int(k): int(v) for k, v in
            re.findall(r'\{ id: (\d+),(?: sesion: \d+,)? title: "[^"]*", shortTitle: "[^"]*", duration: "(\d+) min" \}', src)}
    filas = {}
    for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
        k = int(m.group(1)); h = m.group(2)
        for d in re.findall(r'<div class="derivacion-panel".*?</p>\s*</div>', h, flags=re.S):
            h = h.replace(d, ' ')
        paneles = re.findall(r'<div class="ejercicio-panel (?:pista|solucion)".*?\n          </div>', h, flags=re.S)
        h_cerrado = h
        for p in paneles:
            h_cerrado = h_cerrado.replace(p, ' ')

        def minutos(hh):
            tabs = len(re.findall(r'<div class="code-tabs"', hh))
            sueltos = len(re.findall(r'<pre\b', hh)) - 2 * tabs
            sims = len(re.findall(r'data-simulador=', hh))
            return n(hh), sims, tabs + sueltos, n(hh) / 180 + 3 * sims + 2 * (tabs + sueltos)
        filas[k] = (minutos(h_cerrado), minutos(h), decl.get(k), len(paneles))
    return filas


def informe(nombre, src):
    print(f"\n=== {nombre} ===")
    print("mód | cerrado: palabras, sim., bloques -> min | abierto: palabras, bloques -> min | paneles de ejercicio | declarado")
    tc = ta = td = 0
    for k, (c, a, d, p) in sorted(mide(src).items()):
        print(f"M{k}  | {c[0]:>5} {c[1]:>2} {c[2]:>2} -> {c[3]:5.1f} | {a[0]:>5} {a[2]:>2} -> {a[3]:5.1f} | {p} | {d}")
        tc += c[3]; ta += a[3]; td += d or 0
    print(f"total: cerrado {tc:.1f} min · abierto {ta:.1f} min · declarado {td} min")
    s1c = sum(v[0][3] for k, v in mide(src).items() if k <= 5); s2c = tc - s1c
    s1d = sum(v[2] or 0 for k, v in mide(src).items() if k <= 5)
    print(f"sesión 1 (M1-M5): cerrado {s1c:.1f} min ({100*s1c/tc:.0f} %), declarado {s1d} · "
          f"sesión 2 (M6-M9): cerrado {s2c:.1f} min ({100*s2c/tc:.0f} %), declarado {td - s1d}")


if len(sys.argv) > 1:
    for r in sys.argv[1:]:
        informe(r, open(r, encoding="utf-8").read())
else:
    antes = subprocess.run(["git", "show", f"HEAD:{RUTA}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    informe("ANTES de la R5 (HEAD)", antes)
    informe("AHORA (archivo de trabajo)", (RAIZ / RUTA).read_text(encoding="utf-8"))
