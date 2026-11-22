#!/usr/bin/env python3
"""Lector-estudiante · autoevaluacion del cap. 4: de que modulo sale cada pregunta, posicion y tamano de la opcion correcta.

Uso:  python3 -I lector_quiz.py ruta/capitulo-4-modelos-arima.html

Lee AUTOEVALUACIONES['cap4'] (enunciados, opciones, pista y retroalimentacion), no la ejecuta. Para cada
pregunta: tipo, modulo al que apunta (campo `modulo`), posicion de la(s) correcta(s), longitud de la
correcta frente a la mas larga y a la mediana de las incorrectas (caracteres de texto visible, sin
etiquetas ni LaTeX), si la pista da el numero de correctas, y si el enunciado repite cifras que el modulo
ya dio. Despues, las preguntas que el capitulo contesta por adelantado y los modulos sin pregunta.
"""
import html
import re
import statistics
import sys

src = open(sys.argv[1], encoding="utf-8").read()
i = src.index("AUTOEVALUACIONES['cap4'] = [")
j = src.index("\n    ];", i)
blk = src[i:j]
preg = re.split(r"\n      \{\n        tipo: ", blk)[1:]


def visible(s):
    s = s.replace("\\\\", "\\")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\$[^$]*\$", " M ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


modulos = []
print("n | tipo | modulo | opciones | posicion de la(s) correcta(s) | long. correcta | long. maxima | mediana incorrectas | pista cuenta las correctas")
for n, p in enumerate(preg, 1):
    tipo = re.match(r"'(\w+)'", p).group(1)
    mod = int(re.search(r"modulo:\s*(\d+)", p).group(1))
    modulos.append(mod)
    ops = re.findall(r"texto:\s*'((?:[^'\\]|\\.)*)',\s*correcta:\s*(true|false)", p)
    pista = re.search(r"pista:\s*'((?:[^'\\]|\\.)*)'", p)
    pista = visible(pista.group(1)) if pista else ""
    if ops:
        L = [len(visible(t)) for t, _ in ops]
        pos = [k + 1 for k, (_, c) in enumerate(ops) if c == "true"]
        corr = [L[k - 1] for k in pos]
        inc = [L[k] for k, (_, c) in enumerate(ops) if c == "false"]
        cuenta = bool(re.search(r"\b(Son|son) (dos|tres|cuatro|\d)\b", pista))
        print(f"{n} | {tipo} | M{mod} | {len(ops)} | {pos} | {corr} | {max(L)} | {statistics.median(inc):.0f} | {'SI' if cuenta else 'no'}")
    else:
        r = re.search(r"respuesta:\s*([\d.]+)", p).group(1)
        tol = re.search(r"tolerancia:\s*([\d.]+)", p).group(1)
        dec = re.search(r"Da (\w+) decimales", p)
        print(f"{n} | {tipo} | M{mod} | respuesta {r}, tolerancia {tol} | «Da {dec.group(1) if dec else '?'} decimales» | — | — | — | no")

print()
print("Modulos del capitulo sin pregunta en la autoevaluacion:", [m for m in range(1, 11) if m not in modulos])
print("Preguntas por modulo:", {m: modulos.count(m) for m in sorted(set(modulos))})
