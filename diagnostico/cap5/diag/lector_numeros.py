#!/usr/bin/env python3
"""Lector-estudiante (cap. 5; copia sin cambios de logica de diagnostico/cap4/diag) · densidad de cifras en la prosa (numeros con parte decimal o de 3+ cifras) por modulo.

Uso:  python3 -I lector_numeros.py ruta/capitulo-N-....html

Cuenta, en el texto de cada modulo SIN <pre>, SIN el JS y SIN desarrollos plegados ni paneles de ejercicio,
los numeros con parte decimal o de tres o mas cifras (incluidos los de las formulas en linea y en bloque), y los
da por cada 100 palabras de prosa (formula en linea = 1 palabra). Sirve para comparar cuanto numero tiene que
sostener el lector en cada modulo y entre capitulos (misma regla en el 3 y en el 4).
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
TOK = re.compile(r"<div\b|</div>")


def balanceados(h, patron):
    out = []
    for m in re.finditer(patron, h):
        prof = 0
        for t in TOK.finditer(h, m.start()):
            prof += 1 if t.group(0) == "<div" else -1
            if prof == 0:
                out.append((m.start(), t.end()))
                break
    return out


def quita(h, patron):
    for a, b in reversed(balanceados(h, patron)):
        h = h[:a] + " " + h[b:]
    return h


tot_w = tot_n = 0
print("mod | palabras | numeros | numeros por 100 palabras")
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1))
    h = m.group(2)
    for pat in (r'<div class="quiz"', r'<div class="simulacro"', r'<div class="derivacion"', r'<div class="ejercicio-panel'):
        h = quita(h, pat)
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<(script|style|canvas|svg)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h).replace("\xa0", " ")
    nums = len(re.findall(r"(?<![\w])\d+[.,]\d+|(?<![\w.,])\d{3,}(?![\w])", h))
    h2 = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    h2 = re.sub(r"\$[^$]*\$", " M ", h2)
    w = len(h2.split())
    tot_w += w
    tot_n += nums
    print(f"M{k} | {w} | {nums} | {100 * nums / max(w, 1):.1f}")
print(f"TOTAL | {tot_w} | {tot_n} | {100 * tot_n / max(tot_w, 1):.1f}")
