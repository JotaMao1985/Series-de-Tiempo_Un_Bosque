#!/usr/bin/env python3
"""Resume diag/medidas.json en texto legible (resumen.out) y compara las capturas de la prueba de fuentes."""
import json, math, sys
from pathlib import Path

DIAG = Path(__file__).resolve().parent
CAPT = DIAG.parent / 'capturas'
d = json.loads((DIAG / 'medidas.json').read_text())


def lum(hexa):
    hexa = hexa.lstrip('#')
    if len(hexa) != 6:
        return None
    rgb = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(hexa, fondo='#ffffff'):
    a, b = lum(hexa), lum(fondo)
    if a is None:
        return None
    return round((max(a, b) + 0.05) / (min(a, b) + 0.05), 2)


out = []
p = out.append
p('== Prueba de fuentes')
for f in json.loads((DIAG / 'fuentes.json').read_text()):
    p(json.dumps(f, ensure_ascii=False))
try:
    from PIL import Image, ImageChops
    for et in ('fuentes-normales', 'fuentes-lentas'):
        for ancho in (1200, 375):
            a = CAPT / f'm1-fuente-{et}-inicial-{ancho}.png'
            b = CAPT / f'm1-fuente-{et}-repintado-{ancho}.png'
            if a.exists() and b.exists():
                ia, ib = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
                if ia.size != ib.size:
                    p(f'{et} {ancho}: tamaños distintos {ia.size} {ib.size}')
                    continue
                bbox = ImageChops.difference(ia, ib).getbbox()
                p(f'{et} {ancho}: inicial vs repintado -> {"IGUALES" if bbox is None else "DISTINTAS en " + str(bbox)}')
except ImportError:
    p('PIL no disponible')

p('\n== Contraste sobre blanco de los colores usados')
colores = set()
for ancho, mods in d['medidas'].items():
    for n, m in mods.items():
        for cv in m['canv']:
            for ds in cv.get('datasets', []):
                for k in ('color', 'bg'):
                    if isinstance(ds.get(k), str):
                        colores.add(ds[k])
for c in sorted(colores):
    p(f'{c}: {contraste(c)}:1')

for ancho, mods in d['medidas'].items():
    p(f'\n==================== ancho {ancho}')
    for n, m in mods.items():
        p(f'\n-- M{n}  docSw={m["docSw"]} inner={m["innerWidth"]} main={m["mainW"]}/{m["mainCw"]}')
        for s in m['sims']:
            p(f'  SIM {s["sim"]}: w={s["w"]} right={s["right"]} sw/cw={s["sw"]}/{s["cw"]} h4={s["h4"]} alturas={s["alturas"]}')
            if s['lectura']:
                p(f'     lectura aria-live={s["lectura"]["ariaLive"]} role={s["lectura"]["role"]} h={s["lectura"]["h"]}: {s["lectura"]["txt"]}')
            for ctl in s['controles']:
                p(f'     control {ctl}')
        for cv in m['canv']:
            esc = cv.get('escalas', [])
            p(f'  [{cv["i"]}] {cv["sim"]} {cv.get("tipo")} {cv["w"]}x{cv["h"]} right={cv["right"]} area={cv.get("area")} '
              f'leyenda={cv.get("legend", {}).get("items")} h={cv.get("legend", {}).get("h")}')
            p(f'       aria="{cv["aria"]}"')
            for e in esc:
                extra = ''
                if 'minGap' in e:
                    extra = f' minGap={e["minGap"]} solapes={e["solapes"][:6]} fuera={e["fuera"]}'
                p(f'       {e["id"]}: titulo={e["title"]!r} rango=[{e["min"]}, {e["max"]}] n={e["nTicks"]} '
                  f'fuente={e.get("fuenteTicks")} cargada={e.get("fuenteCargada")} ticks={e["ticks"][:14]}{extra}')
            if cv.get('rectas'):
                p(f'       rectas={cv["rectas"]} anchoBarra={cv.get("anchoBarra")}')
        if m['katex']:
            p('  KATEX que desborda: ' + json.dumps(m['katex'], ensure_ascii=False))
        if m['katexLinea']:
            p('  katex en línea fuera de su caja: ' + json.dumps(m['katexLinea'][:8], ensure_ascii=False))
        if m['tablas']:
            p('  TABLAS que desbordan: ' + json.dumps(m['tablas'], ensure_ascii=False))
        if m.get('recortados'):
            p('  RECORTADOS por main: ' + json.dumps(m['recortados'][:8], ensure_ascii=False))
        if m['desbordan']:
            p('  DESBORDAN la ventana: ' + json.dumps(m['desbordan'][:8], ensure_ascii=False))

p('\n==================== estados de los simuladores')
for ancho, est in d['estados'].items():
    p(f'\n---- ancho {ancho}')
    for k, v in est.items():
        p(f'  {k}: {v["lectura"]}  outputs={v["outputs"]}')
        for j, g in enumerate(v['graficos']):
            esc = {e['id']: e for e in g.get('escalas', [])}
            y = esc.get('y', {})
            x = esc.get('x', {})
            linea = (f'     g{j}: area={g.get("area", {}).get("h")}h leyenda={g.get("legend", {}).get("items")} '
                     f'y=[{y.get("min")}, {y.get("max")}] yticks={y.get("ticks", [])[:10]} '
                     f'x solapes={len(x.get("solapes", []))} minGap={x.get("minGap")} xticks={x.get("ticks", [])[:8]}')
            if g.get('rectas'):
                linea += ' rectas=' + str([(r['label'], round(r['valor'], 4) if isinstance(r['valor'], (int, float)) else r['valor']) for r in g['rectas']])
                linea += f' barras={[(b["label"], round(b["max"], 3)) for b in g.get("barras", [])]}'
            p(linea)

p('\n==================== eventos de consola')
for e in d['eventos'] or []:
    p(f'  {e}')

(DIAG / 'resumen.out').write_text('\n'.join(out))
print('\n'.join(out[:40]))
print('...', len(out), 'líneas en resumen.out')
