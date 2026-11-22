#!/usr/bin/env python3
"""Resumen legible de graficas_medidas.json (lo escribe graficas_revisa.js).

Uso: python3 diagnostico/cap4/diag/graficas_resumen.py > diagnostico/cap4/diag/graficas_resumen.out
"""
import json
import os
import sys

DIAG = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(DIAG, 'graficas_medidas.json')))


def eje(e):
    t = ','.join(e['ticks'][:26])
    extra = ''
    if e.get('solapes'):
        extra += ' SOLAPES=' + '; '.join(e['solapes'])
    if e.get('fuera'):
        extra += ' FUERA=' + ','.join(e['fuera'])
    if e.get('guion'):
        extra += ' GUION=' + ','.join(e['guion'][:4])
    if e.get('fuenteCargada') is False:
        extra += ' FUENTE-NO-CARGADA'
    return f"{e['id']}[{e['type']}{' «' + e['title'] + '»' if e['title'] else ''} {fmt(e['min'])}..{fmt(e['max'])} gap={e.get('minGap')}]: {t}{extra}"


def fmt(x):
    return f'{x:.4g}' if isinstance(x, (int, float)) else str(x)


def grafico(g, sangria='    '):
    out = []
    if 'tipo' not in g:
        out.append(f"{sangria}(sin Chart) aria={g.get('aria')!r}")
        return out
    lg = g['legend']
    out.append(f"{sangria}{g['tipo']} {g['w']}x{g['h']} área {g['area']['w']}x{g['area']['h']} · aria={g['aria']!r}")
    out.append(f"{sangria}  leyenda ({lg['lineas']} línea(s), {lg['h']} px): {' | '.join(lg['items'])}")
    for e in g['escalas']:
        out.append(f"{sangria}  {eje(e)}")
    for ds in g['datasets']:
        if ds.get('rango'):
            lo, hi = ds['rango']
            ys = [e for e in g['escalas'] if not e['id'].startswith('x')]
            clip = ''
            if lo is None or hi is None:
                clip = '  ¡DATOS NO FINITOS (NaN)!'
            elif ys and isinstance(ys[0]['min'], (int, float)) and isinstance(ys[0]['max'], (int, float)):
                if lo < ys[0]['min'] - 1e-9 or hi > ys[0]['max'] + 1e-9:
                    clip = f"  ¡SE SALE DEL EJE {fmt(ys[0]['min'])}..{fmt(ys[0]['max'])}!"
            out.append(f"{sangria}  ds «{ds.get('label')}» ({ds['type']}, n={ds['n']}, color={ds.get('color') or (ds.get('bg') if not isinstance(ds.get('bg'), list) else 'por barra')}) rango {fmt(lo)}..{fmt(hi)}{clip}")
            if ds.get('datos') and ds['type'] == 'bar':
                out.append(f"{sangria}     {ds['datos'][:24]}")
    for r in g.get('rectas', []) or []:
        out.append(f"{sangria}  recta «{r['label']}» = {fmt(r['valor'])} x {r['x0']}..{r['x1']} y={r['y']} color={r['color']}")
    if g.get('anchoBarra') is not None:
        out.append(f"{sangria}  ancho de barra {g['anchoBarra']} px")
    for p in g.get('puntos', []) or []:
        if any(p['recorte']) or not all(p['dentro']):
            out.append(f"{sangria}  puntos «{p['label']}»: {len(p['px'])} dibujados, {sum(p['recorte'])} recortados por el borde, {sum(1 for x in p['dentro'] if not x)} fuera; px recortados={[q for q, r in zip(p['px'], p['recorte']) if r][:6]}")
    return out


for ancho, mods in d['medidas'].items():
    print(f'\n################ {ancho} px')
    for n, m in mods.items():
        print(f"\n=== M{n} · área {m['mainW']} px · docSw {m['docSw']}")
        for k in ('recortados', 'tablas', 'katex', 'katexLinea', 'desbordan'):
            if m[k]:
                print(f'  {k}:')
                for x in m[k][:12]:
                    print('    ', x)
        for s in m['sims']:
            print(f"  [sim {s['sim']}] ancho {s['w']} sw/cw {s['sw']}/{s['cw']} h4={s['h4']['txt'] if s['h4'] else None!r} ({s['h4']['h'] if s['h4'] else ''} px)")
            for c in s['controles']:
                print(f"     control {c['tipo']} «{(c['label'] or '').strip()}» {c.get('min')}..{c.get('max')} paso {c.get('step')} = {c.get('value')} ancho {c['w']}")
            if s['lectura']:
                print(f"     lectura ({s['lectura']['h']} px, aria-live={s['lectura']['ariaLive']}): {s['lectura']['txt']}")
            print(f"     etiquetas: {s['etiquetas']} alturas {s['alturas']}")
        for g in m['canv']:
            print(f"  lienzo {g['i']} (sim {g['sim']})")
            print('\n'.join(grafico(g)))

print('\n\n################ ESTADOS')
for ancho, est in d['estados'].items():
    print(f'\n######## {ancho} px')
    for nombre, e in est.items():
        print(f"\n--- {nombre}")
        print(f"  outputs: {e['outputs']}")
        print(f"  lectura: {e['lectura']}")
        for g in e['graficos']:
            print('\n'.join(grafico(g, '  ')))

print('\n\n################ CONSOLA')
for ev in d['eventos'] or []:
    print(ev)
