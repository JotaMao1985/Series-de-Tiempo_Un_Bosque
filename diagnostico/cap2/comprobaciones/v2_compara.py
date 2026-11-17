# Verificador independiente R2: compara el recorrido de HEAD con el del árbol de trabajo
# (v2_recorrido_head.json frente a v2_recorrido_ahora.json) y lista regresiones y arreglos.
# Uso: python3 v2_compara.py > v2_compara.out
import json, re, os
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
H = json.load(open(os.path.join(AQUI, 'v2_recorrido_head.json')))
A = json.load(open(os.path.join(AQUI, 'v2_recorrido_ahora.json')))

cuenta = Counter()
lineas = defaultdict(list)

def escala(cv, horiz):
    for e in cv.get('escalas', []):
        if e['horiz'] == horiz and e['id'] in ('x', 'y'):
            return e
    return None

def es_rezagos(x):
    return x and x.get('titulo') and re.search(r'rezago', x['titulo'], re.I) and x.get('etiquetas')

print('Eventos de consola  HEAD:', len(H.get('eventos') or []), ' ahora:', len(A.get('eventos') or []))
for e in (A.get('eventos') or [])[:30]:
    print('   ahora:', e)
for e in (H.get('eventos') or [])[:10]:
    print('   HEAD :', e)

for cap in sorted(A['r'], key=int):
    for ancho in sorted(A['r'][cap], key=int, reverse=True):
        ma = A['r'][cap][ancho]['modulos']; mh = H['r'][cap][ancho]['modulos']
        for n in sorted(ma, key=int):
            a = ma[n]; h = mh.get(n)
            pre = f'cap{cap} {ancho:>4} M{n:<2}'
            if a['docSw'] > int(ancho) + 1:
                lineas['pagina'].append(f'{pre} la página desborda: scrollWidth {a["docSw"]}')
            if a.get('anunciosCarga'):
                lineas['aria-live'].append(f'{pre} {a["anunciosCarga"]} actualizaciones de una lectura viva durante la carga')
            # Lienzos
            for i, cv in enumerate(a['canv']):
                ch = h['canv'][i] if h and i < len(h['canv']) else {}
                nom = f'{pre} lienzo {i} ({cv.get("sim")})'
                xa, xh = escala(cv, True), escala(ch, True) if ch else None
                ya, yh = escala(cv, False), escala(ch, False) if ch else None
                if xa is None:
                    continue
                cuenta['lienzos'] += 1
                if es_rezagos(xa):
                    et = xa['etiquetas']
                    for k in ('12', '24', '36'):
                        if k in et:
                            cuenta[f'rezago {k} posible'] += 1
                            if k not in xa['rotulos']:
                                lineas['rezagos sin rotular (ahora)'].append(f'{nom}: falta {k}; rótulos {xa["rotulos"]}')
                            else:
                                cuenta[f'rezago {k} rotulado'] += 1
                            if xh and k not in xh['rotulos']:
                                cuenta[f'rezago {k} faltaba en HEAD'] += 1
                if xa.get('solapes'):
                    tag = 'NUEVO' if not (xh and xh.get('solapes')) else 'ya estaba'
                    lineas['rótulos x solapados'].append(f'{nom} [{tag}]: {xa["solapes"][:4]}')
                if xh and xh.get('solapes') and not xa.get('solapes'):
                    cuenta['solapes x arreglados'] += 1
                if xa.get('fuera'):
                    tag = 'NUEVO' if not (xh and xh.get('fuera')) else 'ya estaba'
                    lineas['rótulos x fuera del lienzo'].append(f'{nom} [{tag}]: {xa["fuera"]}')
                if len(xa['rotulos']) < 2 and (not xh or len(xh['rotulos']) >= 2):
                    lineas['eje x con menos de 2 rótulos'].append(f'{nom}: ahora {xa["rotulos"]}, HEAD {xh["rotulos"] if xh else None}')
                if xh and xa['rotulos'] != xh['rotulos'] and not es_rezagos(xa):
                    lineas['rótulos x cambiados (no rezagos)'].append(
                        f'{nom} [{xa.get("titulo")}]: HEAD {xh["rotulos"][:14]} → ahora {xa["rotulos"][:14]}')
                if ya:
                    if ya.get('tieneCero') is False:
                        tag = 'NUEVO' if not (yh and yh.get('tieneCero') is False) else 'ya estaba'
                        lineas['eje y sin 0'].append(f'{nom} [{tag}]: {ya["rotulos"]}')
                    if yh and yh.get('tieneCero') is False and ya.get('tieneCero'):
                        cuenta['0 del eje y arreglado'] += 1
                    if ya.get('solapes'):
                        tag = 'NUEVO' if not (yh and yh.get('solapes')) else 'ya estaba'
                        lineas['rótulos y solapados'].append(f'{nom} [{tag}]: {ya["solapes"][:4]}')
                    if yh and len(ya['rotulos']) < len(yh['rotulos']) - 2 and len(ya['rotulos']) <= 3:
                        lineas['eje y con muchos menos rótulos'].append(f'{nom}: HEAD {yh["rotulos"]} → ahora {ya["rotulos"]}')
                lg, lgh = cv.get('leyenda'), ch.get('leyenda') if ch else None
                if lg:
                    if lg['fuera']:
                        tag = 'NUEVO' if not (lgh and lgh['fuera']) else 'ya estaba'
                        lineas['leyenda que se sale'].append(f'{nom} [{tag}]: {lg["items"]}')
                    if lgh and lg['h'] > lgh['h'] + 12:
                        lineas['leyenda más alta'].append(f'{nom}: {lgh["h"]} → {lg["h"]} px; {lg["items"]}')
                    if lgh and lg['items'] != lgh['items']:
                        lineas['leyenda con otros textos'].append(f'{nom}: {lgh["items"]} → {lg["items"]}')
                if ch and cv.get('area') and ch.get('area') and cv['area']['h'] < ch['area']['h'] - 15:
                    lineas['área de dibujo más baja'].append(f'{nom}: {ch["area"]["h"]} → {cv["area"]["h"]} px')
            # Tablas
            for t in a['tablas']:
                th = h['tablas'][t['i']] if h and t['i'] < len(h['tablas']) else None
                cuenta['tablas'] += 1
                if t['display'] == 'block' and t['vacio'] > 24 and t['sw'] <= t['cw'] + 1:
                    tag = 'NUEVO' if th and th['display'] != 'block' else 'ya estaba'
                    lineas['tabla que no llena su caja'].append(
                        f'{pre} tabla {t["i"]} [{tag}] «{t["cabecera"]}»: caja {t["cw"]} px, filas {t["trW"]} px (vacío {t["vacio"]}){" ranking" if t["enRanking"] else ""}')
                if t['sw'] > t['cw'] + 1:
                    cuenta['tablas desplazables'] += 1
            ra, rh = a['recortados'], (h['recortados'] if h else [])
            if ra:
                lineas['recortado por <main> (ahora)'].append(f'{pre}: {[(x["tag"], x["sobra"], x["txt"][:30]) for x in ra[:4]]}')
            if rh and not ra:
                cuenta['módulos que dejaron de recortar'] += 1
                lineas['recortes de HEAD resueltos'].append(f'{pre}: {[(x["tag"], x["sobra"], x["txt"][:30]) for x in rh[:3]]}')
            for d in a['desplazables']:
                lineas['cajas/fórmulas con desplazamiento (ahora)'].append(f'{pre} {d["cls"]} {d["sw"]}/{d["cw"]}: {d["txt"]}')
            for p in a['partes']:
                if p['desborda'] or p['sw'] > p['cw'] + 1:
                    lineas['fórmula en partes que desborda'].append(f'{pre} {p}')
            for k, s in enumerate(a['sims']):
                sh = h['sims'][k] if h and k < len(h['sims']) else None
                if sh and s['h4'] and sh['h4'] and abs(s['h4']['h'] - sh['h4']['h']) > 2:
                    lineas['título de simulador cambia de alto'].append(f'{pre} {s["sim"]}: {sh["h4"]["h"]} → {s["h4"]["h"]} px «{s["h4"]["txt"][:40]}»')
                if sh and s['columnas'] != sh['columnas']:
                    lineas['columnas de controles'].append(f'{pre} {s["sim"]}: {sh["columnas"]} → {s["columnas"]} (controles {s["controles"]})')
                if s['controles'] and min(s['controles']) < 180 and s['columnas'] and s['columnas'] > 1:
                    lineas['controles estrechos (ahora)'].append(f'{pre} {s["sim"]}: {s["controles"]}')

print('\nCuentas:', dict(cuenta))
for k, v in lineas.items():
    print(f'\n## {k} ({len(v)})')
    for x in v:
        print('  ' + x)
