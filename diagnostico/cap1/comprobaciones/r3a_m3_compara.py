#!/usr/bin/env python3
"""R3 · T3.1 · compara las cifras que muestran los dos simuladores nuevos del Módulo 3 (leídas con
Chrome sin ventana: r3a_m3_simulador.out) con las de R (r3a_m3.out)."""
import json, re, pathlib
aqui = pathlib.Path(__file__).parent
js = [json.loads(l) for l in (aqui / 'r3a_m3_simulador.out').read_text(encoding='utf-8').splitlines() if l.startswith('{')]
r = (aqui / 'r3a_m3.out').read_text(encoding='utf-8')
fallos = 0
def comprueba(que, a, b):
    global fallos
    ok = a == b
    fallos += not ok
    print(('OK   ' if ok else 'MAL  ') + f'{que}: simulador {a} · R {b}')

# --- rezagos: tabla de R (k pares cor encima igual debajo dist verano_n verano_encima r_k)
tabla = {}
for l in r.splitlines():
    m = re.match(r'\s*(\d+)\s+(\d+)\s+(\d\.\d{4})\s+(\d+)\s+(\d+)\s+(\d+)\s+[\d.]+\s+(\d+)\s+(\d+)\s+\d\.\d{4}\s*$', l)
    if m:
        k, pares, cor, enc, ig, deb, vn, ve = m.groups()
        tabla[int(k)] = dict(pares=int(pares), cor=float(cor), encima=int(enc), debajo=int(deb), vn=int(vn), ve=int(ve))
assert len(tabla) == 12, len(tabla)
cor3 = dict(zip(range(1, 13), re.search(r'correlación a 3 decimales, k = 1\.\.12: (.*)', r).group(1).split()))
for d in js:
    if 'k' not in d:
        continue
    k, t = d['k'], tabla[d['k']]
    L, A = d['lectura'], d['aria']
    comprueba(f'k={k} pares', int(re.search(r': (\d+) puntos', L).group(1)), t['pares'])
    comprueba(f'k={k} puntos dibujados', d['puntos'], t['pares'])
    comprueba(f'k={k} correlación', re.search(r'correlación es (\d\.\d{3})', L).group(1), cor3[k])
    comprueba(f'k={k} turquesa', d['turquesa'], t['vn'])
    if k == 12:
        comprueba('k=12 por encima', int(re.search(r'(\d+) de los 132', L).group(1)), t['encima'])
    else:
        m = re.search(r': (\d+) de (\d+) quedan', L)
        comprueba(f'k={k} julios y agostos por encima', (int(m.group(1)), int(m.group(2))), (t['ve'], t['vn']))
    m = re.search(r'; (\d+) puntos quedan por encima de la diagonal y (\d+) por debajo', A)
    comprueba(f'k={k} aria encima/debajo', (int(m.group(1)), int(m.group(2))), (t['encima'], t['debajo']))
    comprueba(f'k={k} «la más alta»', 'la más alta' in L, k == int(re.search(r'correlación más alta: k = (\d+)', r).group(1)))
    comprueba(f'k={k} «la más baja»', 'la más baja' in L, k == int(re.search(r'más baja: k = (\d+)', r).group(1)))

# --- subseries
S = js[0]['subseries']
m = re.search(r'la de (\w+) \(([\d.]+)\) y la más baja, la de (\w+) \(([\d.]+)\)', S)
ra = re.search(r'mes de media más alta: (\w+) ([\d.]+) ; de media más baja: (\w+) ([\d.]+)', r)
comprueba('subseries · media más alta', (m.group(1)[:3].lower(), m.group(2)), (ra.group(1).lower(), ra.group(2)))
comprueba('subseries · media más baja', (m.group(3)[:3].lower(), m.group(4)), (ra.group(3).lower(), ra.group(4)))
for mes, abrev in (('julio', 'Jul'), ('noviembre', 'Nov')):
    m = re.search(mes + r' pasa de (\d+) en 1949 a (\d+) en 1960 \(\+(\d+)\)', S)
    f = re.search(r'^\s*' + abrev + r'\s+[\d.]+\s+(\d+)\s+(\d+)\s+(\d+)\s', r, flags=re.M)
    comprueba(f'subseries · {mes} 1949, 1960 y subida', m.groups(), f.groups())
print('\nfallos:', fallos)
