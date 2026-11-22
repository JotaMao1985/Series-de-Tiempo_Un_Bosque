#!/usr/bin/env python3
"""Lector-estudiante · introduccion de cada simulador: palabras, cifras que adelanta y parrafos largos de prosa.

Uso:  python3 -I lector_intros.py ruta/capitulo-4-modelos-arima.html

(1) Para cada <p class="simulador-intro">: palabras (formula en linea = 1 palabra) y cuantas cifras (numeros
    con parte decimal o de 3+ cifras) trae. Una introduccion con cifras y conclusion dice el resultado antes de
    que el lector mueva nada.
(2) Los 12 parrafos <p> mas largos de los modulos 1 a 10 (palabras), con su linea.
"""
import html
import re
import sys

ruta = sys.argv[1]
src = open(ruta, encoding="utf-8").read()
lineas = src.split("\n")


def limpia(x):
    x = re.sub(r"<pre\b.*?</pre>", " ", x, flags=re.S)
    x = re.sub(r"<(/?)(code|strong|em|a|span|cite|sub|sup|i|b)\b[^>]*>", "", x)
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x).replace("\xa0", " ")
    x = re.sub(r"\$\$.*?\$\$", " ", x, flags=re.S)
    return x


def palabras(x):
    t = limpia(x)
    t = re.sub(r"\$[^$]*\$", " M ", t)
    return len(t.split())


def cifras(x):
    t = limpia(x)
    return len(re.findall(r"\$[^$]*\d+[.,]\d+[^$]*\$|(?<![\w.])\d{1,3}(?:[.,]\d+)?(?:\s?%)?(?![\w])", t)) // 1


print("simulador | linea | palabras de la introduccion | numeros que aparecen en ella")
tot = 0
for m in re.finditer(r'data-simulador="([^"]+)">\s*<h4>.*?</h4>\s*<p class="simulador-intro">(.*?)</p>', src, re.S):
    nom = m.group(1)
    if nom.endswith("simulacro"):
        continue
    ln = src[:m.start()].count("\n") + 1
    p = palabras(m.group(2))
    c = len(re.findall(r"\d+[.,]\d+|\b\d{3,}\b", limpia(m.group(2))))
    tot += p
    print(f"{nom} | {ln} | {p} | {c}")
print(f"total de palabras en introducciones de simulador: {tot}")

print()
print("== Los 12 parrafos <p> mas largos de los modulos 1-10 ==")
mods = [(int(m.group(1)), m.start(), m.group(2)) for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S)]
lista = []
for k, off, h in mods:
    if k > 10:
        continue
    for pm in re.finditer(r"<p(?:\s[^>]*)?>(.*?)</p>", h, re.S):
        if "simulador-intro" in h[max(0, pm.start() - 40):pm.start() + 30]:
            continue
        ini = limpia(pm.group(1)).split()[:4]
        ini = " ".join(ini)
        # la linea se busca por las primeras palabras (la posicion en el texto de la plantilla no es la del archivo)
        ln = next((i for i, l in enumerate(lineas, 1) if ini and ini.split()[0] in l and ini.split()[-1] in l
                   and i >= src[:off].count("\n") + 1), 0)
        lista.append((palabras(pm.group(1)), k, ln, ini))
for w, k, ln, ini in sorted(lista, reverse=True)[:12]:
    print(f"M{k} | linea ~{ln} | {w} palabras | empieza «{ini}»")
