#!/usr/bin/env python3
"""Lector-estudiante · tamano de cada seccion (<h3>) de cada modulo y posicion del primer bloque de codigo.

Uso:  python3 -I lector_secciones.py ruta/capitulo-4-modelos-arima.html

Para cada modulo parte el marcado en <h3> y cuenta, con la regla de lector_carga.py (cada formula en linea =
1 palabra; sin <pre>, sin matematica en bloque, sin ejercicio-panel), las palabras de cada tramo; da ademas
cuantas palabras de prosa preceden al PRIMER bloque de codigo y al PRIMER simulador de cada modulo (para ver
cuanto se lee antes de que aparezca algo que se pueda mover o ejecutar).
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
INLINE = r"(?:code|strong|em|a|span|cite|sub|sup|i|b|kbd)"


def texto(h):
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<(script|style|canvas|svg)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<button\b.*?</button>", " ", h, flags=re.S)
    h = re.sub(r"<(/?)" + INLINE + r"\b[^>]*>", "", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h).replace("\xa0", " ")
    h = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    h = re.sub(r"\$[^$]*\$", " M ", h)
    return h


def n(h):
    return len(texto(h).split())


for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1))
    h = m.group(2)
    # tramos por <h3> (el primero es la cabecera y la introduccion)
    partes = re.split(r"(<h3>.*?</h3>)", h, flags=re.S)
    tramos = []
    cur_t, cur = "(introduccion)", ""
    for p in partes:
        if p.startswith("<h3>"):
            tramos.append((cur_t, cur))
            cur_t, cur = re.sub(r"<[^>]+>", "", p), ""
        else:
            cur += p
    tramos.append((cur_t, cur))
    # palabras antes del primer <pre> y del primer simulador
    ipre = h.find("<pre")
    isim = h.find('class="simulador"')
    w_pre = n(h[:ipre]) if ipre > 0 else None
    w_sim = n(h[:isim]) if isim > 0 else None
    print(f"M{k}: palabras antes del primer simulador: {w_sim if w_sim is not None else '—'}; "
          f"antes del primer bloque de codigo: {w_pre if w_pre is not None else '—'}")
    for t, c in tramos:
        c2 = re.sub(r'<div class="ejercicio-panel.*?</div>', " ", c, flags=re.S)
        print(f"     {n(c2):>5} palabras | {re.sub(chr(10), ' ', html.unescape(t))[:80]}")
