"""Verificador A · R4 cap. 4: comprobación estática de las citas visibles de
M1–M6 en el HTML final: texto compuesto no vacío con el loc de su data-loc,
enlace a un id que existe en la lista «Fuentes citadas en este módulo» del
MISMO módulo, la lista con exactamente las obras citadas en él, y sin espacio
antes de la puntuación que sigue a una cita."""
import re, pathlib, html
RAIZ = pathlib.Path(__file__).resolve().parents[3]
t = (RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html").read_text("utf-8")
partes = re.split(r'<template id="module-(\d+)"', t)
mods = {int(partes[i]): partes[i+1] for i in range(1, len(partes), 2)}
total = 0; malos = 0
for m in range(1, 7):
    s = mods[m]
    cites = re.findall(r'<cite class="cita" data-ref="([^"]+)" data-loc="([^"]*)"([^>]*)><a href="#([^"]+)"[^>]*>(.*?)</a></cite>(.?)', s)
    ids = set(re.findall(r'<li id="(ref-m%d-[^"]+)"' % m, s))
    lista = {i.split("-", 2)[2] for i in ids}
    citadas = {c[0] for c in cites}
    print(f"M{m}: {len(cites)} citas · obras citadas {sorted(citadas)} · lista {sorted(lista)} · {'IGUALES' if lista == citadas else '!!! DISTINTAS'}")
    for ref, loc, resto, href, txt, sig in cites:
        total += 1
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
        prob = []
        if href not in ids: prob.append("enlace sin destino en la lista del módulo")
        if not txt.strip(): prob.append("cita vacía")
        if loc and loc not in txt: prob.append(f"loc {loc} no aparece en «{txt}»")
        if prob:
            malos += 1; print("   ", ref, loc, "→", txt, "|", "; ".join(prob))
    sueltas = len(re.findall(r'<cite class="cita"', s))
    if sueltas != len(cites): print(f"   !!! {sueltas} <cite> y {len(cites)} reconocidas")
print(f"TOTAL {total} citas en M1–M6 · con problemas: {malos}")
for m in range(1, 7):
    print(f"M{m} espacios antes de puntuación tras </cite>:", len(re.findall(r"</cite>(?:</span>)?\s+[.,;:)]", mods[m])))
