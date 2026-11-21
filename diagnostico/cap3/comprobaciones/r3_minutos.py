#!/usr/bin/env python3
"""R3 del capitulo 3 · minutos medidos (copia corregida de `diag/lector_carga.py`).

Lo unico que cambia respecto de `lector_carga.py` es `texto()`: la herramienta original quita
las etiquetas HTML con `<[^>]+>` ANTES de quitar las formulas, y un `<` crudo dentro de una
formula en linea (p. ej. `$|w| < 1$`, que el capitulo escribe asi desde la R1) hace que esa
expresion se coma todo hasta el siguiente `>`: con eso, el modulo 10 medido al principio de
la ronda salia de 726 palabras cuando tiene mas de 1 400. Aqui (1) las formulas se quitan antes
que las etiquetas, (2) el `$` de un `<code>` (p. ej. `pacf(y)$acf`) no cuenta como delimitador
de formula, y (3) solo es etiqueta un `<` seguido de letra, `/` o `!`. La formula de minutos y
el resto del convenio son los mismos.

Lector-estudiante · carga de un capitulo (palabras, formulas, bloques y minutos).

Uso:  python3 -I lector_carga.py ruta/capitulo-3-modelos-ar-ma-arma.html
      python3 -I lector_carga.py ruta/capitulo-2-estacionariedad-acf-pacf.html   (para comparar)

Formula de minutos (la misma de `diagnostico/cap2/diag/cuenta_cap2.py`, que a su vez es la
de `cuenta_cap1_v2.py` / `r5_minutos.py` del capitulo 1; no se toca):
    minutos = palabras de prosa / 180  +  3 por simulador  +  2 por bloque de codigo
(un par de pestanas R/Python cuenta como UN bloque; cada <pre> suelto, como uno).

Convenio de palabras (una palabra = una cadena entre espacios):
  * se quitan <pre>, <script>, <style>, <canvas>, <svg>, <button>, el <caption class="sr-only">,
    el pie de fuentes y los contenedores dinamicos del quiz/simulacro;
  * se quita la matematica en bloque ($$...$$) y cada formula en linea $...$ cuenta como UNA palabra;
  * «cerrado» deja sin contar la pista y la solucion de los ejercicios y los desarrollos plegados;
    «abierto» cuenta la pista y la solucion; los desarrollos plegados van aparte siempre.

Ademas de los minutos, para cada modulo se cuentan: formulas en bloque ($$), formulas en linea ($),
cuadros (note/warning/definition/formula/diagram), tablas, simuladores, bloques de codigo (y lineas),
desarrollos plegados, componentes (ciclo, tabla ordenable), subtitulos <h3>.

Los quizzes y el simulacro viven en el JS: se cuentan aparte (palabras de enunciados y opciones,
y de pista y retroalimentacion).
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
INLINE = r"(?:code|strong|em|a|span|cite|sub|sup|i|b|kbd)"
TOK = re.compile(r"<div\b|</div>")


def divs_balanceados(h, patron_ini):
    """Devuelve la lista de (ini, fin) de cada <div ...> que empieza con `patron_ini`, cerrado en su </div>."""
    salida = []
    for m in re.finditer(patron_ini, h):
        prof = 0
        for t in TOK.finditer(h, m.start()):
            prof += 1 if t.group(0) == "<div" else -1
            if prof == 0:
                salida.append((m.start(), t.end()))
                break
    return salida


def quita(h, patron_ini):
    """Quita del HTML cada <div> balanceado que empiece con patron_ini."""
    for ini, fin in reversed(divs_balanceados(h, patron_ini)):
        h = h[:ini] + " " + h[fin:]
    return h


def texto(h):
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<(script|style|canvas|svg)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r'<aside class="fuentes-modulo".*?</aside>', " ", h, flags=re.S)
    h = re.sub(r'<caption class="sr-only".*?</caption>', " ", h, flags=re.S)
    h = re.sub(r"<button\b.*?</button>", " ", h, flags=re.S)
    # el $ de un <code> no delimita formulas
    h = re.sub(r"<code\b[^>]*>.*?</code>", lambda m: m.group(0).replace("$", "\u00a4"), h, flags=re.S)
    h = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    h = re.sub(r"\$[^$]*\$", " M ", h)
    h = re.sub(r"<(/?)" + INLINE + r"\b[^>]*>", "", h)
    h = re.sub(r"</?[A-Za-z!][^>]*>", " ", h)
    h = html.unescape(h).replace("\xa0", " ").replace("\u00a4", "$")
    return h


def n(h):
    return len(texto(h).split())


def mate(h):
    """(formulas en bloque, formulas en linea) de un trozo de HTML (sin contar el codigo)."""
    h = re.sub(r"<pre\b.*?</pre>", " ", h, flags=re.S)
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S)
    bloques = re.findall(r"\$\$.*?\$\$", h, flags=re.S)
    resto = re.sub(r"\$\$.*?\$\$", " ", h, flags=re.S)
    enlinea = re.findall(r"\$[^$\n]+?\$", resto)
    return len(bloques), len(enlinea)


decl = {int(k): int(v) for k, v in
        re.findall(r'\{ id: (\d+), title: "[^"]*", shortTitle: "[^"]*", duration: "(\d+) min" \}', src)}
titulos = {int(k): t for k, t in
           re.findall(r'\{ id: (\d+), title: "([^"]*)", shortTitle', src)}

filas = []
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1))
    h = m.group(2)
    # contenedores dinamicos (se pintan por JS): fuera
    h = quita(h, r'<div class="quiz"')
    h = quita(h, r'<div class="simulacro"')
    ders = divs_balanceados(h, r'<div class="derivacion"')
    h_der = " ".join(h[i:f] for i, f in ders)
    h_sin = quita(h, r'<div class="derivacion"')
    pan = divs_balanceados(h_sin, r'<div class="ejercicio-panel')
    h_pan = " ".join(h_sin[i:f] for i, f in pan)
    h_cerr = quita(h_sin, r'<div class="ejercicio-panel')

    def codigo(hh):
        tabs = len(re.findall(r'<div class="code-tabs"', hh))
        pres = len(re.findall(r"<pre\b", hh))
        sueltos = pres - 2 * tabs
        lineas = sum(len(x.splitlines()) for x in re.findall(r"<pre\b.*?</pre>", hh, flags=re.S))
        return tabs + sueltos, lineas

    sims = len(re.findall(r'data-simulador="(?!cap3-simulacro)', h))
    cod_c, lin_c = codigo(h_cerr)
    cod_a, lin_a = codigo(h_sin)
    w_c, w_a, w_d = n(h_cerr), n(h_sin), n(h_der)
    min_c = w_c / 180 + 3 * sims + 2 * cod_c
    min_a = w_a / 180 + 3 * sims + 2 * cod_a
    # matematica: solo la que esta fuera del desarrollo plegado, y la de los desarrollos aparte
    f_blq, f_lin = mate(h_sin)
    d_blq, d_lin = mate(h_der)
    cuadros = {c: len(re.findall(r'<div class="' + c + r'"', h)) for c in
               ("note", "warning", "definition", "formula", "diagram")}
    filas.append(dict(
        k=k, w_c=w_c, w_a=w_a, w_d=w_d, sims=sims, cod_c=cod_c, cod_a=cod_a, lin_a=lin_a,
        min_c=min_c, min_a=min_a, d=decl.get(k),
        f_blq=f_blq, f_lin=f_lin, d_blq=d_blq, d_lin=d_lin,
        cuadros=cuadros, tablas=len(re.findall(r"<table\b", h)),
        folds=len(ders), ciclos=len(re.findall(r"data-ciclo=", h)),
        rank=len(re.findall(r"data-ranking=", h)),
        h3=len(re.findall(r"<h3>", h)),
        ejercicios=len(re.findall(r'class="ejercicio-guiado"', h)),
        quizzes=len(re.findall(r'data-quiz="', m.group(2))),
        simulacro=len(re.findall(r'class="simulacro"', m.group(2))),
    ))


# --- quizzes y simulacro (JS) ---------------------------------------------------------
def bloque_js(prefijo):
    i = src.find(prefijo)
    if i < 0:
        return ""
    j = src.find("\n    ];", i)
    j2 = src.find("\n    };", i)
    cand = [x for x in (j, j2) if x > 0]
    return src[i:min(cand)] if cand else src[i:i + 60000]


def cuenta_js(blk):
    # cadenas de JS entre comillas simples con escapes; se tratan como HTML
    pat = r"(\w+):\s*'((?:[^'\\]|\\.)*)'"
    retro, resto = 0, 0
    nq = len(re.findall(r"^\s+tipo:", blk, flags=re.M))
    for clave, val in re.findall(pat, blk):
        val = val.replace("\\\\", "\\")
        w = len(re.sub(r"\\\(.*?\\\)|\$[^$]*\$", " M ", html.unescape(re.sub(r"<[^>]+>", " ", val))).split())
        if clave in ("retro", "retroAcierto", "retroFallo", "pista"):
            retro += w
        elif clave in ("tipo", "modulo", "etiqueta", "variante"):
            continue
        else:
            resto += w
    # opciones del simulacro: cadenas sueltas dentro de opciones: [ ... ]
    for lista in re.findall(r"opciones:\s*\[(.*?)\]", blk, flags=re.S):
        for val in re.findall(r"'((?:[^'\\]|\\.)*)'", lista):
            resto += len(re.sub(r"\\\(.*?\\\)", " M ", val).split())
    return nq, resto, retro


quizzes = {}
for id_ in [x for x in re.findall(r"AUTOEVALUACIONES\['(\w+)'\] = \[", src) if x != "id"]:
    blk = bloque_js(f"AUTOEVALUACIONES['{id_}'] = [")
    if blk:
        quizzes[f"autoevaluacion '{id_}'"] = cuenta_js(blk)
for id_ in [x for x in re.findall(r"SIMULACROS\['([\w-]+)'\] = \{", src) if x != "id"]:
    blk = bloque_js(f"SIMULACROS['{id_}'] = {{")
    if blk:
        quizzes[f"simulacro '{id_}'"] = cuenta_js(blk)


def fmt_fila(f):
    c = f["cuadros"]
    cu = c["note"] + c["warning"] + c["definition"] + c["formula"] + c["diagram"]
    return (f"M{f['k']:<2}| {f['w_c']:>5} {f['w_a']:>5} {f['w_d']:>4} | {f['f_blq']:>3} {f['f_lin']:>4} "
            f"{f['d_blq']:>3} | {cu:>2} ({c['note']}n {c['warning']}w {c['definition']}d {c['formula']}f "
            f"{c['diagram']}g) | {f['tablas']:>2} | {f['sims']:>2} | {f['cod_a']:>2} {f['lin_a']:>4} | "
            f"{f['folds']:>2} | {f['ciclos'] + f['rank']:>2} | {f['h3']:>2} | {f['ejercicios']:>2} | "
            f"{f['min_c']:5.1f} {f['min_a']:5.1f} | {f['d'] if f['d'] is not None else '-':>3}")


print("mod| palabras: cerrado abierto plegado | formulas: bloque linea (bloque en plegados) | "
      "cuadros | tablas | sim | codigo: bloques lineas | plegados | ciclo/rank | h3 | ejerc. | min cerr. abierto | declarado")
tot = dict(w_c=0, w_a=0, w_d=0, f_blq=0, f_lin=0, d_blq=0, cod=0, sims=0, mc=0, ma=0, dec=0, cu=0, tablas=0)
for f in filas:
    print(fmt_fila(f))
    tot["w_c"] += f["w_c"]; tot["w_a"] += f["w_a"]; tot["w_d"] += f["w_d"]
    tot["f_blq"] += f["f_blq"]; tot["f_lin"] += f["f_lin"]; tot["d_blq"] += f["d_blq"]
    tot["cod"] += f["cod_a"]; tot["sims"] += f["sims"]
    tot["mc"] += f["min_c"]; tot["ma"] += f["min_a"]; tot["dec"] += f["d"] or 0
    tot["cu"] += sum(f["cuadros"].values()); tot["tablas"] += f["tablas"]
print(f"TOTAL | palabras cerrado {tot['w_c']} abierto {tot['w_a']} plegado {tot['w_d']} | "
      f"formulas en bloque {tot['f_blq']} (+{tot['d_blq']} plegadas) en linea {tot['f_lin']} | "
      f"cuadros {tot['cu']} | tablas {tot['tablas']} | simuladores {tot['sims']} | codigo {tot['cod']} | "
      f"min cerrado {tot['mc']:.1f} abierto {tot['ma']:.1f} | declarado {tot['dec']}")
print()
print("Densidad de formulas en bloque por 100 palabras de prosa (cerrado):",
      ", ".join(f"M{f['k']} {100 * f['f_blq'] / max(f['w_c'], 1):.1f}" for f in filas))
print("Formulas en linea por 100 palabras de prosa (cerrado):",
      ", ".join(f"M{f['k']} {100 * f['f_lin'] / max(f['w_c'], 1):.1f}" for f in filas))
print("Razon abierto/declarado por modulo:",
      ", ".join(f"M{f['k']} {f['min_a'] / f['d']:.2f}" for f in filas if f["d"]))
print("Razon cerrado/declarado por modulo:",
      ", ".join(f"M{f['k']} {f['min_c'] / f['d']:.2f}" for f in filas if f["d"]))
print()
print("Quizzes y simulacro (JS): preguntas, palabras de enunciados y opciones, palabras de pista y retro, minutos de lectura")
for nombre, (nq, resto, retro) in quizzes.items():
    print(f"  {nombre}: {nq} preguntas; {resto} palabras de enunciado/opciones; {retro} de pista/retro "
          f"-> {(resto + retro) / 180:.1f} min de lectura")
print()
print("Modulos del sidebar:")
for k, t in titulos.items():
    print(f"  M{k}: {t} ({decl.get(k)} min)")
