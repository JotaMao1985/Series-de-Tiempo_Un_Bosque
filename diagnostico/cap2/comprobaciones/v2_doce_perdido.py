# Verificador independiente R2: lienzos cuyo eje x tiene la categoría 12 (o 24) y que la rotulaban
# en HEAD pero ya no la rotulan ahora (cualquier título de eje).
import json
H = json.load(open('v2_recorrido_head.json')); A = json.load(open('v2_recorrido_ahora.json'))
for cap in A['r']:
    for w in A['r'][cap]:
        for n, m in A['r'][cap][w]['modulos'].items():
            for i, cv in enumerate(m['canv']):
                xa = next((e for e in cv.get('escalas', []) if e['horiz'] and e['id'] == 'x'), None)
                try: ch = H['r'][cap][w]['modulos'][n]['canv'][i]
                except Exception: continue
                xh = next((e for e in ch.get('escalas', []) if e['horiz'] and e['id'] == 'x'), None)
                if not xa or not xh or not xa.get('etiquetas'): continue
                for k in ('12', '24'):
                    if k in xa['etiquetas'] and k in xh['rotulos'] and k not in xa['rotulos']:
                        print(f'cap{cap} {w} M{n} lienzo {i} ({cv.get("sim")}) [{xa.get("titulo")}]: pierde {k}; HEAD {xh["rotulos"][:12]} → ahora {xa["rotulos"]}')
