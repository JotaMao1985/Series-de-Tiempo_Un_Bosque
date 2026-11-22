"""Diagnóstico cap. 4 · reparto por módulo de los instrumentos (de ejercicios_vuelca.json).
    python3 diagnostico/cap4/diag/ejercicios_cobertura.py > diagnostico/cap4/diag/ejercicios_cobertura.out
"""
import json, pathlib, re, collections
J = json.loads((pathlib.Path(__file__).parent / 'ejercicios_vuelca.json').read_text(encoding='utf8'))
print('Quiz cap4, etiqueta `modulo` por pregunta:', [q['modulo'] for q in J['cap4']])
c = collections.Counter(q['modulo'] for q in J['cap4'])
print('  por módulo:', {m: c.get(m, 0) for m in range(1, 11)})
H = (pathlib.Path(__file__).resolve().parents[3] / 'Htmls_Series/capitulo-4-modelos-arima.html').read_text(encoding='utf8')
eti = re.findall(r"etiqueta: '([^']*)'", H[H.index("SIMULACROS['cap4-simulacro']"):])
print('Simulacro M11, etiquetas:'); [print('  ', i + 1, e) for i, e in enumerate(eti)]
prep = [q for b in ['bloque-a', 'bloque-b', 'bloque-c', 'bloque-d', 'prep-simulacro'] for q in J[b]]
c = collections.Counter(q['modulo'] for q in prep if str(q['modulo']).startswith('4.'))
print('Preparcial, ítems por módulo del cap. 4 (bloques A-D y su simulacro):')
for m in [f'4.{k}' for k in range(1, 11)]:
    print(f'  {m}: {c.get(m, 0)}  ', [f"{q['instrumento']}#{q['n']}" for q in prep if q['modulo'] == m])
print('  total cap. 4:', sum(c.values()), 'de', len(prep))
# ¿Qué instrumento usa cada serie con nombre?
series = ['Nile', 'Nilo', 'AirPassengers', 'TRM', 'BJsales', 'lynx', 'lince']
for k, Q in J.items():
    usa = collections.Counter(s for q in Q for s in series
                              if s in (q['pregunta'] + ' '.join(o['texto'] + ' ' + (o['retro'] or '') for o in q['opciones'])
                                       + (q['retroAcierto'] or '') + (q['retroFallo'] or '') + (q['pista'] or '')))
    print(f'Series nombradas en {k}:', dict(usa))
