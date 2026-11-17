# Verificador independiente R2: contrasta cada aria-label dinámico del cap. 2 con los datos del lienzo.
import json, re, sys
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'v2_estados_cap2_1200.json'))
num = lambda s: float(s.replace('−', '-').replace(' ', ''))
pat = re.compile(r'(\d+) de (\d+) barras fuera de la banda ±([\d.]+); la del rezago 1 vale ([−\-\d.]+)(?: y la del rezago 10, ([−\-\d.]+))?')
malos = 0; total = 0
def revisa(clave, l):
    global malos, total
    a = l.get('aria') or ''
    m = pat.search(a)
    if not m or 'verdad' not in l or l['verdad'].get('fuera') is None: return
    total += 1
    v = l['verdad']
    ok = (int(m.group(1)) == v['fuera'] and int(m.group(2)) == v['n'] and abs(num(m.group(3)) - v['banda']) < 6e-4
          and abs(num(m.group(4)) - v['r1']) < 6e-4 and (m.group(5) is None or abs(num(m.group(5)) - v['r10']) < 6e-4))
    if not ok:
        malos += 1
        print('NO CUADRA', clave, '|', a, '| verdad', v)
for k, e in d['estados'].items():
    for i, l in enumerate(e['lienzos']):
        revisa(f'{k}[{i}]', l)
        print(f'{k}[{i}]: {l.get("aria")}')
for p in d['phi']:
    if 'aria' in p:
        l = {'aria': p['aria'][1], 'verdad': p['verdad']}
        revisa(f"ar1 φ={p['phi']} dif={p['dif']}", l)
print(f'\ncorrelogramas con aria contrastado: {total}; no cuadran: {malos}')
print('\nAR(1), aria de la serie en algunos estados:')
for p in d['phi']:
    if 'aria' in p and p['phi'] in (0, 0.95, 1, 1.05): print(' ', p['dif'], p['aria'][0], '|', p['aria'][1])
print('\nQuiz:')
for q in d['quiz']:
    print(' aria:', q['aria']); print('  acf:', q['acf']); print('  banda:', q['banda'], 'rotulosX:', q['rotulosX'], 'rotulosY:', q['rotulosY'])
