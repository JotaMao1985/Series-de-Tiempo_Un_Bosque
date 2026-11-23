"""Verificador B · R4 cap. 4: listas de fuentes de los módulos 7-12, lista del capítulo y pie.

Para cada <template id="module-N">: claves de las <cite> frente a los <li id="ref-mN-clave"> de su
aside; que cada enlace de cita apunte a un id del mismo módulo; que el `title` de la cita sea la
ficha de la lista. Lista del capítulo = unión de las claves citadas en todo el capítulo. Pie.
python3 diagnostico/cap4/comprobaciones/v4B_listas.py > diagnostico/cap4/comprobaciones/v4B_listas.out
"""
import html as H
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
t = (RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html").read_text("utf-8")

def texto(s):
    return " ".join(H.unescape(re.sub(r"<[^>]+>", "", s)).split())

mods = [(m.group(1), m.start()) for m in re.finditer(r'<template id="module-(\d+)">', t)]
todas = set()
for i, (n, ini) in enumerate(mods):
    fin = mods[i + 1][1] if i + 1 < len(mods) else len(t)
    bloque = t[ini:fin]
    cites = re.findall(r'<cite class="cita" data-ref="([^"]+)" data-loc="([^"]+)"[^>]*><a href="#([^"]+)" title="([^"]*)">([^<]*)</a></cite>', bloque)
    vacias = len(re.findall(r'<cite class="cita"[^>]*></cite>', bloque))
    claves = {c[0] for c in cites}
    todas |= claves
    lista = dict(re.findall(r'<li id="ref-m%s-([^"]+)">(.*?)</li>' % n, bloque, re.S))
    malos = [c for c in cites if c[2] != f"ref-m{n}-{c[0]}" or c[0] not in lista]
    titulos = [c for c in cites if c[0] in lista and texto(c[3]) != texto(lista[c[0]])]
    print(f"M{n}: {len(cites)} citas · {len(claves)} obras · lista {sorted(lista)}"
          f" · iguales: {claves == set(lista)} · enlaces rotos {len(malos)} · title≠ficha {len(titulos)} · vacías {vacias}")
    for c in titulos[:3]:
        print("   title:", texto(c[3])[:150], "\n   ficha:", texto(lista[c[0]])[:150])
    if int(n) >= 7:
        locs = sorted({f"{c[0]} {c[1]}" for c in cites})
        print("   localizadores:", "; ".join(locs))
cap = re.search(r"<!--REFERENCIAS-CAPITULO:inicio-->(.*?)<!--REFERENCIAS-CAPITULO:fin-->", t, re.S).group(1)
ids = re.findall(r'<li id="([^"]+)">', cap)
print("\nlista del capítulo:", ids)
print("claves citadas en todo el capítulo:", sorted(todas))
print("coinciden:", {i.split("-", 1)[1] if i.startswith("ref-") else i for i in ids} == todas
      or sorted(todas))
for li in re.findall(r"<li[^>]*>(.*?)</li>", cap, re.S):
    print("  ·", texto(li)[:200])
pie = re.search(r"<!--PIE-REFERENCIAS:inicio-->(.*?)<!--PIE-REFERENCIAS:fin-->", t, re.S).group(1)
print("\npie:")
for li in re.findall(r"<li[^>]*>(.*?)</li>", pie, re.S):
    print("  ·", texto(li)[:200])
