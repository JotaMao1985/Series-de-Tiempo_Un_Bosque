#!/usr/bin/env python3
"""Lector-estudiante (cap. 5) · forma del simulacro del Modulo 12.

Uso:  python3 -I lector_simulacro.py ruta/capitulo-5-sarima.html

El simulacro vive en el JS como `SIMULACROS['cap5-simulacro'] = {...};` (JSON valido).
Lo extrae y lista: versiones, tipo de cada pregunta, la etiqueta que dice a que modulos
corresponde, las palabras del enunciado y de las opciones y de la 'cuenta' (la solucion
paso a paso), y las remisiones «modulo 5.N» que hacen sus retros.
Sirve para dos comprobaciones del lente de comprension: (1) lo que declara el texto del
Modulo 12 (numero de preguntas, cifras/selecciones, versiones) frente a lo que hay;
(2) que cada modulo citado exista y trate lo que el simulacro dice que trata.
"""
import html
import json
import re
import sys
from collections import Counter

src = open(sys.argv[1], encoding="utf-8").read()
ini = src.index("SIMULACROS['cap5-simulacro'] = ") + len("SIMULACROS['cap5-simulacro'] = ")
# el objeto es JSON valido: se corta en el primer «};» que cierra a nivel 0
prof = 0
fin = None
en_cadena = False
esc = False
for i in range(ini, len(src)):
    c = src[i]
    if en_cadena:
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == '"':
            en_cadena = False
        continue
    if c == '"':
        en_cadena = True
    elif c == "{":
        prof += 1
    elif c == "}":
        prof -= 1
        if prof == 0:
            fin = i + 1
            break
sim = json.loads(src[ini:fin])


def txt(h):
    h = re.sub(r"<[^>]+>", " ", h or "")
    return re.sub(r"\s+", " ", html.unescape(h)).strip()


print("minutos:", sim["minutos"], "| etapas:", sim["etapas"], "| versiones:", len(sim["versiones"]))
for v in sim["versiones"]:
    print(f"\n== version {v['numero']} == caso: {len(txt(v['caso']).split())} palabras")
    print("   caso (primeras 400 car.):", txt(v["caso"])[:400])
    tipos = Counter(p["tipo"] for p in v["preguntas"])
    print("   preguntas:", len(v["preguntas"]), dict(tipos))
    figuras = [p["n"] for p in v["preguntas"] if "grafico" in json.dumps(p, ensure_ascii=False)[:2000].lower()
               or p.get("figura") or p.get("dibujar")]
    print("   con figura (por clave):", [p["n"] for p in v["preguntas"] if p.get("figura") or p.get("dibujar") or p.get("grafico")])
    tot_w = 0
    for p in v["preguntas"]:
        w_en = len(txt(p["enunciado"]).split())
        w_op = sum(len(txt(o["texto"]).split()) for o in p.get("opciones", []))
        w_cu = len(txt(p.get("cuenta", "")).split()) + sum(len(txt(o.get("retro", "")).split()) for o in p.get("opciones", []))
        tot_w += w_en + w_op
        remite = sorted(set(re.findall(r"m[oó]d(?:ulos?|\.)\s*([0-9.,y ]+)", txt(p.get("cuenta", "")) + " " +
                                       " ".join(o.get("retro", "") for o in p.get("opciones", [])))))
        print(f"   {p['n']:>2} {p['id']:<3} {p['tipo']:<6} etapa {p['etapa']} | enun {w_en:>3} op {w_op:>3} sol/retro {w_cu:>3} | {p['etiqueta']}")
    print(f"   palabras de enunciados y opciones (sin caso): {tot_w}")
