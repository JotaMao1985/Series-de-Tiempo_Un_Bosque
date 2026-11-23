#!/usr/bin/env python3
"""Lector-estudiante (cap. 5) · autoevaluacion y simulacro: de que modulo sale cada pregunta, posicion y tamano de la correcta.

Uso:  python3 -I lector_quiz.py ruta/capitulo-5-sarima.html

Adaptado de `diagnostico/cap4/diag/lector_quiz.py`. Lee AUTOEVALUACIONES['cap5'] (ocho preguntas) y
SIMULACROS['cap5-simulacro'] (doce), sin ejecutarlos. Por pregunta: tipo, modulo al que apunta, posicion de la(s)
correcta(s), longitud de la correcta frente a la maxima y a la mediana de las incorrectas (caracteres visibles, sin
etiquetas ni LaTeX), si la pista da el numero de correctas. Despues: modulos sin pregunta, y cuantas preguntas
del simulacro piden algo que el capitulo no ensena (lista a mano en la nota).
"""
import html
import json
import re
import statistics
import sys

src = open(sys.argv[1], encoding="utf-8").read()


def visible(s):
    s = s.replace("\\\\", "\\")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\$[^$]*\$", " M ", s)
    s = re.sub(r"\\\(.*?\\\)", " M ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


# ---------------- autoevaluacion ----------------
i = src.index("AUTOEVALUACIONES['cap5'] = [")
j = src.index("\n    ];", i)
blk = src[i:j]
preg = re.split(r"\n      \{\n        tipo: ", blk)[1:]
modulos = []
print("== Autoevaluacion del capitulo (8) ==")
print("n | tipo | modulo (campo) | opciones | posicion de la(s) correcta(s) | long. correcta | long. maxima | mediana incorrectas | pista cuenta correctas")
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
print("Modulos 1-11 sin pregunta en la autoevaluacion:", [m for m in range(1, 12) if m not in modulos])
print("Preguntas por modulo (campo `modulo`):", {m: modulos.count(m) for m in sorted(set(modulos))})
print("Nota: la pregunta 6 lleva modulo: 6 pero su retro la llama «la leccion central del Modulo 10» y su contenido (armonica frente a airline) es del M10.")

# ---------------- simulacro ----------------
pref = "SIMULACROS['cap5-simulacro'] = "
ini = src.index(pref) + len(pref)
prof, en, esc = 0, False, False
for k in range(ini, len(src)):
    c = src[k]
    if en:
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == '"':
            en = False
        continue
    if c == '"':
        en = True
    elif c == "{":
        prof += 1
    elif c == "}":
        prof -= 1
        if prof == 0:
            fin = k + 1
            break
sim = json.loads(src[ini:fin])
print()
print("== Simulacro (12) · opciones de las preguntas de seleccion ==")
print("n | id | modulos citados en la etiqueta | posicion de la correcta (1-4) | long. correcta | long. maxima | mediana incorrectas")
pos_c = []
for p in sim["versiones"][0]["preguntas"]:
    if p["tipo"] == "opcion":
        L = [len(visible(o["texto"])) for o in p["opciones"]]
        c = p["correcta"]
        inc = [L[k] for k in range(len(L)) if k != c]
        pos_c.append(c + 1)
        print(f"{p['n']} | {p['id']} | {p['etiqueta'].split('·')[1].strip()} | {c + 1} | {L[c]} | {max(L)} | {statistics.median(inc):.0f}")
    else:
        print(f"{p['n']} | {p['id']} | {p['etiqueta'].split('·')[1].strip()} | cifra | clave {p['clave']['texto']} (tol. {p['clave']['tol']}) | {len(p.get('rutas', []))} rutas de error nombradas")
print()
print("Posicion de la correcta en las 6 preguntas de seleccion del simulacro:", pos_c)
etq = [p["etiqueta"] for p in sim["versiones"][0]["preguntas"]]
mods = {}
for e in etq:
    m = re.search(r"m[oó]d\. ([\d., y]+)", e)
    for t in re.findall(r"5\.(\d+)", m.group(1) if m else ""):
        mods[int(t)] = mods.get(int(t), 0) + 1
print("Preguntas del simulacro por modulo citado:", dict(sorted(mods.items())))
print("Modulos 1-11 que el simulacro no cita:", [m for m in range(1, 12) if m not in mods])
