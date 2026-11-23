"""Diagnóstico cap. 5 · reparto por módulo de los instrumentos de práctica y series que nombran.

    python3 diagnostico/cap5/diag/ejercicios_cobertura.py > diagnostico/cap5/diag/ejercicios_cobertura.out

Quiz: etiqueta `modulo`. Simulacro: módulos de su `etiqueta` («mód. 5.x»). Ejercicios: series
nombradas en el enunciado. Excel: hojas M1-M11 (ejercicios_excel.out). Series: las de la lista
de práctica de los caps. 2-4 y las del propio capítulo, buscadas en los enunciados.
"""
import re, json, pathlib, collections
aqui = pathlib.Path(__file__).resolve().parent
raiz = aqui.parents[2]
J = json.load(open(aqui / 'ejercicios_vuelca.json'))
html = (raiz / 'Htmls_Series/capitulo-5-sarima.html').read_text(encoding='utf8')
q = collections.Counter(p['modulo'] for p in J['cap5'])
s = collections.Counter()
for p in J['simulacro']:
    for m in re.findall(r'5\.(\d+)', p['etiqueta']): s[int(m)] += 1
print('Módulo | quiz cap5 (etiqueta) | simulacro (menciones en la etiqueta)')
for m in range(1, 12): print(f'  M{m:<2} | {q.get(m, 0)} | {s.get(m, 0)}')
ej = re.findall(r'<p class="ejercicio-enunciado"><span class="ejercicio-numero">(\d)\.</span>(.*?)</p>', html, flags=re.S)
previas = ['EuStockMarkets', 'discoveries', 'LakeHuron', 'nhtemp', 'JohnsonJohnson', 'UKDriverDeaths', 'co2', 'USAccDeaths', 'UKgas',
           'sunspot.year', 'lh', 'TRM', 'WWWusage', 'treering', 'lynx', 'tcm', 'global_economy', 'airmiles', 'gafa_stock', 'NelPlo',
           'austres', 'pelt', 'BJsales', 'AirPassengers']
print('\nSeries nombradas en los enunciados de los ejercicios guiados:')
for n, t in ej:
    t = re.sub(r'<[^>]+>', '', t)
    print(f'  E{n}:', [x for x in previas if re.search(r'\b' + re.escape(x) + r'\b', t)])
print('\nSeries nombradas en el quiz (pregunta + opciones):')
for p in J['cap5']:
    t = p['pregunta'] + ' ' + ' '.join(o['texto'] for o in p['opciones'])
    hits = [x for x in previas if re.search(r'\b' + re.escape(x) + r'\b', t)]
    print(f'  Q{p["n"]}: {hits or "— (sin serie nombrada; datos o proceso teórico)"}')
print('\nSimulacro: series inventadas del caso (peaje, camiones, estación de servicio, cajeros, aseguradora, mensajería); ninguna de la lista:',
      not any(re.search(r'\b' + re.escape(x) + r'\b', ' '.join(p['enunciado'] for p in J['simulacro'])) for x in previas))
