#!/usr/bin/env python3
"""Tabla compacta por lienzo y ancho (estado inicial) a partir de graficas_medidas.json."""
import json, os
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graficas_medidas.json')))
for ancho in ('1200', '800', '375'):
    print(f'\n##### {ancho}')
    for n, m in d['medidas'][ancho].items():
        for g in m['canv']:
            if 'tipo' not in g: continue
            x = next(e for e in g['escalas'] if e['id'] == 'x')
            y = next(e for e in g['escalas'] if e['id'] == 'y')
            lg = g['legend']
            print(f"M{n} {g['sim'][:22]:22} {g['tipo']:7} lienzo {g['w']:.0f}x{g['h']:.0f} área {g['area']['w']:.0f}x{g['area']['h']:.0f} "
                  f"ley {lg['lineas']}l/{lg['h']:.0f}px barra {g.get('anchoBarra')} | x: {','.join(x['ticks'])}"
                  f"{' SOLAPES ' + str(x['solapes']) if x.get('solapes') else ''}{' FUERA ' + str(x['fuera']) if x.get('fuera') else ''} | y: {','.join(y['ticks'])}")
