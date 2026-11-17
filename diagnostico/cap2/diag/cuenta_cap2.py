#!/usr/bin/env python3
"""Lector-estudiante · carga del capitulo 2 (minutos estimados frente a declarados).

Adaptacion de `diagnostico/cap1/comprobaciones/cuenta_cap1_v2.py` y de
`r5_minutos.py` (la formula con que el capitulo 1 declara hoy sus minutos).

Formula (la misma del capitulo 1, sin tocarla):
    minutos = palabras de prosa / 180  +  3 por simulador  +  2 por bloque de codigo
(un par de pestanas R/Python cuenta como un bloque; el desarrollo plegable
`.derivacion-panel` va aparte; la pista y la solucion de un ejercicio entran
solo en la columna «abierto»).

Convenio de palabras (una palabra = una cadena entre espacios):
  * se quitan <pre>, <script>, <style>, <canvas>, <svg>, <button>, el <caption
    class="sr-only">, el pie de fuentes y el bloque del quiz;
  * se quita la matematica en bloque ($$...$$);
  * cada formula en linea $...$ cuenta como UNA palabra;
  * las etiquetas en linea (code, strong, em, a, span, ...) se pegan al texto;
  * el resto de etiquetas separa palabras.

Diferencia con `cuenta_cap1_v2.py`: aquel NO quita <pre> (cuenta el codigo como
prosa); `r5_minutos.py` si lo quita. Aqui se usa el convenio de `r5_minutos.py`
y se imprime aparte cuantas palabras hay dentro de <pre> en cada modulo (lo que
la v2 habria contado como prosa).

El quiz (AUTOEVALUACIONES['cap2']) se cuenta aparte: palabras de enunciados y
opciones, y de retroalimentacion.

Uso:  python3 -I cuenta_cap2.py ruta/capitulo-2-estacionariedad-acf-pacf.html
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
INLINE = r"(?:code|strong|em|a|span|cite|sub|sup|i|b|kbd)"


def texto(h, quita_pre=True):
    if quita_pre:
        h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<(script|style|canvas|svg)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r'<aside class="fuentes-modulo".*?</aside>', " ", h, flags=re.S)
    h = re.sub(r'<caption class="sr-only".*?</caption>', " ", h, flags=re.S)
    h = re.sub(r"<button\b.*?</button>", " ", h, flags=re.S)
    h = re.sub(r'<div class="quiz".*?<div class="quiz-marcador">.*?</div>\s*</div>', " ", h, flags=re.S)
    h = re.sub(r"<(/?)" + INLINE + r"\b[^>]*>", "", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h).replace("\xa0", " ")
    h = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    h = re.sub(r"\$[^$]*\$", " M ", h)
    return h


def n(h, quita_pre=True):
    return len(texto(h, quita_pre).split())


decl = {int(k): int(v) for k, v in
        re.findall(r'\{ id: (\d+), title: "[^"]*", shortTitle: "[^"]*", duration: "(\d+) min" \}', src)}

filas = []
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1))
    h = m.group(2)
    ders = re.findall(r'<div class="derivacion-panel".*?</p>\s*</div>', h, flags=re.S)
    h_sin = h
    for d in ders:
        h_sin = h_sin.replace(d, " ")
    wd = sum(n(d) for d in ders)
    paneles = re.findall(r'<div class="ejercicio-panel (?:pista|solucion)".*?\n          </div>', h_sin, flags=re.S)
    h_cerr = h_sin
    for p in paneles:
        h_cerr = h_cerr.replace(p, " ")

    def mide(hh):
        tabs = len(re.findall(r'<div class="code-tabs"', hh))
        sueltos = len(re.findall(r"<pre\b", hh)) - 2 * tabs
        sims = len(re.findall(r"data-simulador=", hh))
        w = n(hh)
        return w, sims, tabs + sueltos, w / 180 + 3 * sims + 2 * (tabs + sueltos)

    c = mide(h_cerr)
    a = mide(h_sin)
    ciclos = len(re.findall(r"data-ciclo=", h))
    quiz = len(re.findall(r'<div class="quiz"', h))
    # palabras dentro de <pre> (en el modulo con las derivaciones fuera, con ejercicios abiertos)
    v2 = sum(len(html.unescape(re.sub(r"<[^>]+>", " ", x)).split())
             for x in re.findall(r"<pre\b.*?</pre>", h_sin, flags=re.S))
    # subtitulos <h3> propios del modulo (el del «Objetivo» lleva atributos y no cuenta)
    h3 = len(re.findall(r"<h3>", h))
    filas.append(dict(k=k, c=c, a=a, wd=wd, ciclos=ciclos, quiz=quiz, v2=v2, h3=h3,
                      paneles=len(paneles), d=decl.get(k)))

# --- quiz -------------------------------------------------------------------
i = src.index("AUTOEVALUACIONES['cap2'] = [")
j = src.index("\n    ];", i)
blk = src[i:j]
n_preg = len(re.findall(r"^\s+tipo:", blk, flags=re.M))
# retroalimentacion: claves retro*, pista; enunciado y opciones: el resto de textos
retro = re.findall(r"(?:retro|retroAcierto|retroFallo|pista):\s*'((?:[^'\\]|\\.)*)'", blk)
resto = re.findall(r"(?:pregunta|texto|descripcionGrafico):\s*'((?:[^'\\]|\\.)*)'", blk)
w_retro = sum(n(x) for x in retro)
w_resto = sum(n(x) for x in resto)
min_quiz = (w_retro + w_resto) / 180


def fila(f):
    c, a = f["c"], f["a"]
    return (f"M{f['k']} | {c[0]:>5} {c[1]:>2} {c[2]:>2} -> {c[3]:5.1f} | "
            f"{a[0]:>5} {a[2]:>2} -> {a[3]:5.1f} | {f['wd']:>4} | {f['ciclos']} | {f['h3']} | "
            f"{f['v2']:>5} | {f['paneles']} | {f['d']}")


print("mod | cerrado: palabras, sim., bloques -> min | abierto: palabras, bloques -> min | "
      "derivacion (palabras) | ciclo | subtitulos h3 | palabras en <pre> | paneles ej. | declarado")
tc = ta = td = 0
for f in filas:
    print(fila(f))
    tc += f["c"][3]
    ta += f["a"][3]
    td += f["d"] or 0
print(f"TOTAL cerrado {tc:.1f} min | abierto {ta:.1f} min | declarado {td} min")
td_der = sum(f["wd"] for f in filas) / 180
print(f"derivacion plegada: {sum(f['wd'] for f in filas)} palabras = {td_der:.1f} min (no entra en ninguna columna)")
print(f"quiz: {n_preg} preguntas; {w_resto} palabras de enunciado/opciones, {w_retro} de pista y retroalimentacion "
      f"=> {min_quiz:.1f} min de lectura (no entra en ninguna columna)")
print("razon abierto/declarado por modulo:",
      ", ".join(f"M{f['k']} {f['a'][3] / f['d']:.2f}" for f in filas))
print("razon cerrado/declarado por modulo:",
      ", ".join(f"M{f['k']} {f['c'][3] / f['d']:.2f}" for f in filas))
