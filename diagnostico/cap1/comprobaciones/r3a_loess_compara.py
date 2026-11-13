#!/usr/bin/env python3
"""R3 · compara, mes a mes, la curva que dibuja el simulador `loess-local` ya corregido
(leída con Chrome sin ventana: r3a_loess_simulador.out) con la réplica en R (r3a_loess.out, §5)."""
import json, re, pathlib
aqui = pathlib.Path(__file__).parent
js = None
for linea in (aqui / 'r3a_loess_simulador.out').read_text(encoding='utf-8').splitlines():
    if linea.startswith('{') and '"curva"' in linea:
        js = json.loads(linea)['curva'].split()
r = []
for linea in (aqui / 'r3a_loess.out').read_text(encoding='utf-8').splitlines():
    m = re.match(r'\s*(\d{4}-\d{2})\s+(\d\.\d{4})\s+(\d\.\d{4})\s', linea)
    if m:
        r.append(m.group(2))
assert js and len(js) == 144 and len(r) == 144, (len(js or []), len(r))
distintos = [(i + 1, a, b) for i, (a, b) in enumerate(zip(js, r)) if a != b]
print(f'curva del simulador (JS) frente a la réplica en R, a 4 decimales: {144 - len(distintos)} de 144 iguales')
for d in distintos:
    print('  distinto:', d)
