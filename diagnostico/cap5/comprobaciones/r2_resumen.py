#!/usr/bin/env python3
"""R2 del cap. 5 · resumen de r2_medidas.json (lo escribe r2_revisa.js): lo que la ronda tenía que dejar
arreglado, medido en todos los estados a 1200, 800 y 375 px.

Uso: python3 diagnostico/cap5/comprobaciones/r2_resumen.py > diagnostico/cap5/comprobaciones/r2_resumen.out
"""
import json
import os
import re
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(AQUI, 'r2_medidas.json')))
GUION = re.compile(r'(^|[\s(\[=:,;±×|])-\.?\d')

print('Base:', d['base'], '·', d['fecha'])
for ancho, est in d['estados'].items():
    print(f'\n################ {ancho} px · {len(est)} estados')
    areas = defaultdict(list)           # (sim, k) -> [(h, estado)]
    arias = defaultdict(set)
    problemas = []
    sin_datos = []
    leyendas = defaultdict(int)
    mapas = []
    for nombre, e in est.items():
        sim = nombre.split(':')[0]
        if e.get('lectura') and GUION.search(e['lectura']):
            problemas.append(f'{nombre}: guion en la lectura')
        if e.get('receta') and GUION.search(e['receta']['txt']):
            problemas.append(f'{nombre}: guion en la receta: {e["receta"]["txt"][:80]}')
        for k, g in enumerate(e['graficos']):
            if 'tipo' not in g:
                sin_datos.append(f'{nombre} lienzo {k}: sin gráfico')
                continue
            areas[(sim, k)].append((g['area']['h'], nombre.split(':')[1]))
            arias[(sim, k)].add(g['aria'])
            if g['aria'] and GUION.search(g['aria']):
                problemas.append(f'{nombre} lienzo {k}: guion en el aria-label')
            lg = g['legend']
            leyendas[(sim, k)] = max(leyendas[(sim, k)], lg['lineas'])
            if lg.get('cortadas'):
                problemas.append(f'{nombre} lienzo {k}: {lg["cortadas"]} entradas de la leyenda cortadas')
            for ds in g['datasets']:
                if ds.get('rango') and (ds['rango'][0] is None or ds['rango'][1] is None):
                    problemas.append(f'{nombre} lienzo {k}: datos no finitos en «{ds.get("label")}»')
            for s in g['escalas']:
                if s.get('solapes'):
                    problemas.append(f'{nombre} lienzo {k} eje {s["id"]}: solapes {s["solapes"]}')
                if s.get('fuera'):
                    problemas.append(f'{nombre} lienzo {k} eje {s["id"]}: rótulos fuera {s["fuera"]}')
                if s.get('guion'):
                    problemas.append(f'{nombre} lienzo {k} eje {s["id"]}: guion {s["guion"]}')
            for p in g.get('puntos') or []:
                if any(p['recorte']):
                    problemas.append(f'{nombre} lienzo {k}: {sum(p["recorte"])} marcadores de «{p["label"]}» recortados')
        for mp in e.get('mapas') or []:
            mapas.append((nombre, mp))

    print('\n· Área de dibujo mínima por lienzo (todos sus estados) y número de aria-label distintos')
    for (sim, k), v in sorted(areas.items()):
        h, cual = min(v)
        n_est = len(v)
        print(f'  {sim:32} lienzo {k}: área mín {h:6.1f} px ({cual}) · leyenda máx {leyendas[(sim, k)]} renglón(es)'
              f' · aria distintos {len(arias[(sim, k)])} de {n_est} estados')
    minimo = min(min(v)[0] for v in areas.values())
    print(f'  ÁREA MÍNIMA DE TODOS LOS LIENZOS Y ESTADOS: {minimo:.1f} px')
    fijos = [f'{s} {k}' for (s, k), a in arias.items() if len(a) == 1 and len(areas[(s, k)]) > 1]
    print(f'  lienzos cuyo aria-label no cambia entre estados: {fijos or "ninguno"}')

    print('\n· Mapas estacionales')
    peor = None
    for nombre, mp in mapas:
        linea = (f'  {nombre:42} {mp["modo"]:13} meses visibles {len(mp["mesesVisibles"])}/12'
                 f'{" DESPLAZA" if mp["desplaza"] else ""} · filas ARIA {mp["filasARIA"]} (celdas por fila {mp["celdasPorFila"]})'
                 f' · cifras visibles {len(mp["peores"]) and mp["conNumero"]} · contraste mín {mp["contrasteMin"]}'
                 f' · <4.5: {mp["bajo45"]} · desbordan {mp["desbordaCelda"]} · guiones {mp["guiones"]} · cabecera {mp["cabeceras"]!r}'
                 f' · cifra {mp["fuenteCifra"]}')
        print(linea)
        if mp['contrasteMin'] is not None and (peor is None or mp['contrasteMin'] < peor[0]):
            peor = (mp['contrasteMin'], nombre)
        if mp['bajo45'] or mp['desplaza'] or len(mp['mesesVisibles']) < 12 or mp['guiones'] or mp['desbordaCelda']:
            problemas.append(f'{nombre}: mapa con defecto (contraste {mp["contrasteMin"]}, meses {len(mp["mesesVisibles"])}, guiones {mp["guiones"]}, desbordan {mp["desbordaCelda"]})')
    if mapas:
        print(f'  aria de la rejilla (estados distintos): {len({mp["aria"] for _, mp in mapas})} de {len(mapas)}')
        print(f'  ejemplo: {mapas[0][1]["aria"]!r}')
        print(f'  peor contraste de una cifra visible: {peor}')

    print('\n· Problemas')
    for p in problemas + sin_datos:
        print('  ', p)
    if not problemas and not sin_datos:
        print('   ninguno')

print('\n################ MEDIDAS POR MÓDULO (estado inicial)')
for ancho, mods in d['medidas'].items():
    for n, m in mods.items():
        # «desbordan» del recorrido cuenta también lo que cae dentro de una caja desplazable (tablas,
        # código, fórmulas): lo que importa es «recortados», lo que asoma sin caja que lo recoja.
        extra = [k for k in ('recortados',) if m[k]]
        if extra or m['docSw'] != int(ancho):
            print(f'  {ancho} M{n}: docSw {m["docSw"]} {", ".join(f"{k}={m[k][:3]}" for k in extra)}')
print('  (nada más que decir de los módulos si no hay líneas encima)')

print('\n################ CONSOLA')
for ev in d['eventos'] or []:
    print('  ', ev)
