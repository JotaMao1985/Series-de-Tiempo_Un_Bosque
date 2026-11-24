"""Resume v2_mapas.json: por versión, ancho y mapa."""
import json, collections
from pathlib import Path
d = json.loads((Path(__file__).parent / 'v2_mapas.json').read_text())
print('eventos de consola:', [e['txt'][:90] for e in d['eventos']])
g = collections.defaultdict(list)
for e in d['estados']:
    g[(e['version'], e['ancho'], e['pagina'], e['sim'] or 'M')].append(e)
for k, es in g.items():
    ms = [e['mapa'] for e in es]
    cls = collections.Counter(m['clases'].replace('mapa-estacional--entero', '').replace('mapa-estacional', '').strip() or '(normal)' for m in ms)
    ks = [m['contrasteMin'] for m in ms if m['contrasteMin'] is not None]
    print(f"{k[0]:6} {k[1]:>4} {k[2]:9} {k[3][:18]:18} n={len(es):2} clases={dict(cls)} desplaza={sum(m['desplaza'] for m in ms)} "
          f"mesesMin={min(m['mesesSinDesplazar'] for m in ms)} cifrasVis={sum(m['cifrasVisibles'] for m in ms)}/{sum(m['conCifra'] for m in ms)} "
          f"kmin={min(ks) if ks else None} bajo45={sum(m['bajo45'] for m in ms)} cuerpo={min((m['cuerpoMin'] for m in ms if m['cuerpoMin']), default=None)}-{max((m['cuerpoMax'] for m in ms if m['cuerpoMax']), default=None)} "
          f"noCabenVis={sum(m['nNoCabenVisibles'] for m in ms)} guionCifra={sum(m['guionesCifra'] for m in ms)} guionAria={sum(m['guionesAria'] for m in ms)} "
          f"guionLey={sum(bool(m['guionLeyenda']) for m in ms)} celdaW={min(m['celda']['w'] for m in ms if m['celda'])} cab={ms[0]['cabecera'][:24]!r} filas={sorted(set(m['filas'] for m in ms))} hijosNoFila={max(m['hijosNoFila'] for m in ms)}")
print()
print('--- estados con cifras ocultas (actual) ---')
for e in d['estados']:
    if e['version'] == 'actual' and 'sin-cifras' in e['mapa']['clases']:
        print(f"  {e['ancho']:>4} {e['pagina']} {e['sim']} {e['estado']}: celda {e['mapa']['celda']} valor={e['mapa']['valor']}")
print('--- estados con cifras chicas (actual) ---')
for e in d['estados']:
    if e['version'] == 'actual' and 'cifras-chicas' in e['mapa']['clases']:
        print(f"  {e['ancho']:>4} {e['pagina']} {e['sim']} {e['estado']}: cuerpo {e['mapa']['cuerpoMin']} px")
print('--- interacciones ---')
for i in d['interacciones']:
    print(' ', json.dumps(i, ensure_ascii=False))
print('--- árbol de accesibilidad ---')
for a in d['arboles']:
    print(' ', a['ancho'], a['pagina'], a['sim'], json.dumps(a['arbol'], ensure_ascii=False))
print('--- nombres accesibles (actual, 1200) ---')
for e in d['estados']:
    if e['version'] == 'actual' and e['ancho'] == '1200':
        print(f"  {e['pagina']} {e['sim']} {e['estado']}: {e['mapa']['aria']}")
        print(f"        leyenda: {e['mapa']['leyenda']} | nota: {e['mapa']['nota'][:110]}")
