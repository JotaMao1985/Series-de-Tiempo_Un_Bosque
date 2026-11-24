"""Resume v2_medidas.json (v2_revisa.js): áreas, leyendas, ejes, aria-label y lecturas por estado y ancho."""
import json, re, collections
from pathlib import Path
d = json.loads((Path(__file__).parent / 'v2_medidas.json').read_text())
print('eventos de consola:', [e['txt'][:100] for e in d['eventos'] if 'favicon' not in e['txt']], '· total', len(d['eventos']))
for an, mods in d['medidas'].items():
    rec = sum(len(m['recortados']) for m in mods.values()); des = sum(len(m['desbordan']) for m in mods.values())
    print(f"{an}: docSw={sorted(set(m['docSw'] for m in mods.values()))} recortados={rec} desbordan={des}")
print('\n== Área mínima de dibujo por lienzo, leyenda (líneas, cortadas), por simulador y ancho')
area = collections.defaultdict(lambda: [1e9, None, 0, set(), set(), 0])
arias = collections.defaultdict(set)
guiones = []
for an, est in d['estados'].items():
    for k, e in est.items():
        sim, nombre = k.split(':', 1)
        for i, g in enumerate(e['graficos']):
            a = area[(sim, i, an)]
            if 'area' in g and g['area']['h'] < a[0]: a[0] = g['area']['h']; a[1] = nombre
            if 'legend' in g:
                a[2] = max(a[2], g['legend']['lineas'])
                for t in g['legend'].get('cortadas', []): a[3].add(f"{nombre}:{t}")
            arias[(sim, i)].add(g['aria'])
            for s in g.get('escalas', []):
                if s['guion']: guiones.append((an, k, s['id'], s['guion'][:3]))
for (sim, i, an), a in sorted(area.items()):
    print(f"  {sim:32} lienzo{i} {an:>4}: área mín {a[0]:6} px ({a[1]}), leyenda hasta {a[2]} líneas, cortadas: {sorted(a[3]) or '—'}")
print('\nguiones en ejes:', guiones or 'ninguno')
print('\n== aria-label distintos por lienzo (en todos los estados y anchos)')
for (sim, i), s in sorted(arias.items()):
    print(f"  {sim} lienzo{i}: {len(s)} distintos; ejemplo: {sorted(s)[0][:230]}")
def L(an, k): return d['estados'][an].get(k, {}).get('lectura')
print('\n== Lecturas y aria-label seleccionados (1200)')
for k in ['mapa-firma:inicial', 'mapa-firma:airpassengers-log-d1D1', 'mapa-firma:airpassengers-log-D1', 'mapa-firma:co2-log-d1D1',
          'mapa-firma:trm-nolog-d1', 'mapa-firma:trm-nolog-D1', 'receta-mes:phi1-Phi1', 'receta-mes:phi-1-Phi-1', 'receta-mes:phi1-Phi-1',
          'constructor-polinomio:inicial', 'constructor-polinomio:D0', 'constructor-polinomio:todo0', 'constructor-polinomio:todo2',
          'airline-pesos:inicial', 'airline-pesos:theta-095-Theta-095', 'firma-teorica:inicial', 'sobrediferenciacion-estacional:D0',
          'sobrediferenciacion-estacional:D2', 'cuatro-combinaciones:d1D1',
          'explorador-sarima:pqPQ0000', 'pronostico-estacional:inicial', 'pronostico-estacional:log-h13', 'contraejemplo-trm:trm', 'contraejemplo-trm:ap',
          'calendario-regresores:dias0-pascua1', 'calendario-regresores:dias1-pascua1', 'armonicos-K:inicial', 'armonicos-K:K6',
          'comparativa-particion:inicial', 'comparativa-particion:mape', 'comparativa-particion:todos', 'comparativa-particion:ninguno']:
    e = d['estados']['1200'].get(k)
    if not e: print('  (falta)', k); continue
    print(f"--- {k}\n    lectura: {e['lectura']}")
    for g in e['graficos']:
        print(f"    aria: {g['aria']}")
        if 'legend' in g: print(f"    leyenda: {g['legend']['items']}")
    if e.get('receta'): print(f"    receta: {e['receta']['txt'][:400]}")
print('\n== M9: ejes por ancho y estado')
for an in d['estados']:
    for k, e in d['estados'][an].items():
        if k.startswith('calendario-regresores'):
            g = e['graficos'][0]
            for s in g['escalas']:
                print(f"  {an:>4} {k:42} {s['id']:3} título={s['title']!r} marcas={s['ticks'][:14]} solapes={s.get('solapes')} minGap={s.get('minGap')} área={g['area']}")
            pts = g.get('puntos') or []
            for p in pts: print(f"       puntos {p['label']}: {len(p['dentro'])}, fuera del área: {p['dentro'].count(False)}, recortados: {p['recorte'].count(True)}")
print('\n== M11 todos: leyenda por ancho')
for an in d['estados']:
    for k in ['comparativa-particion:todos', 'comparativa-particion:todos-mape', 'comparativa-particion:inicial']:
        e = d['estados'][an].get(k)
        if not e: continue
        g = e['graficos'][0]
        print(f"  {an:>4} {k}: área {g['area']} leyenda {g['legend']['lineas']} líneas, {g['legend']['cajas']} cajas de {len(g['legend']['items'])}, cortadas {g['legend']['cortadas']}, fuente {g['legend'].get('fuente')}")
        print(f"       items: {g['legend']['items']}")
        print(f"       colores: {[(x['label'], x['color'], x['dash'], x['bw']) for x in g['datasets']]}")
print('\n== Interruptores del M11 (1200)')
s = [x for x in d['medidas']['1200']['11']['sims'] if x['sim'] == 'comparativa-particion'][0]
for c in s['controles']: print('   ', c['tipo'], repr(c['label']))
print('\n== h4 de los simuladores con hijos (iconos)')
for an in ['1200']:
    for n, m in d['medidas'][an].items():
        for x in m['sims']:
            if x['h4']: print(f"   M{n} {x['sim']}: {x['h4']['txt'][:60]!r} h={x['h4']['h']}")
