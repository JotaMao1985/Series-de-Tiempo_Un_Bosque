#!/usr/bin/env python3
"""R3 del capitulo 5 · palabras de cada seccion (<h3>) del Modulo 11 (copia de la del capitulo 4,
que medía el Modulo 10), con la misma convencion de `r3_minutos.py`
(prosa cerrada: sin <pre>, sin formulas en bloque, cada formula en linea cuenta como una palabra, sin
pista ni solucion de los ejercicios). Uso: python3 -I r3_secciones_m11.py ruta/capitulo-5-sarima.html"""
import html, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<template id="module-11">(.*?)</template>', src, re.S)
h = m.group(1)
INLINE = r"(?:code|strong|em|a|span|cite|sub|sup|i|b|kbd)"


def texto(t):
    t = re.sub(r"<pre\b.*?</pre>", " ", t, flags=re.S)
    t = re.sub(r"<(script|style|canvas|svg)\b.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r'<div class="ejercicio-panel.*?</div>', " ", t, flags=re.S)
    t = re.sub(r"<button\b.*?</button>", " ", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<code\b[^>]*>.*?</code>", lambda k: k.group(0).replace("$", "¤"), t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " M ", t)
    t = re.sub(r"<(/?)" + INLINE + r"\b[^>]*>", "", t)
    t = re.sub(r"</?[A-Za-z!][^>]*>", " ", t)
    return html.unescape(t).replace("\xa0", " ").replace("¤", "$")


partes = re.split(r"(?=<h3>)", h)
tot = 0
for p in partes:
    t = re.match(r"<h3>(.*?)</h3>", p, re.S)
    nombre = re.sub(r"\s+", " ", t.group(1)) if t else "(apertura)"
    n = len(texto(p).split())
    tot += n
    cod = len(re.findall(r"<pre\b", p))
    tab = len(re.findall(r"<table\b", p)) + len(re.findall(r'class="tabla-ranking"', p))
    sim = len(re.findall(r'data-simulador="', p))
    print(f"{n:5d} palabras · {cod} <pre> · {tab} tablas · {sim} simuladores · {nombre}")
print(f"{tot:5d} palabras en total")
