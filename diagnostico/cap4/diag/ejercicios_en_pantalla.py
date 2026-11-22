"""Diagnóstico cap. 4 · ¿la respuesta del quiz está ya en pantalla? Busca en el HTML las
cifras de cada clave y lo que muestran los simuladores (datos precalculados de DATOS_CAP4).
    python3 diagnostico/cap4/diag/ejercicios_en_pantalla.py > diagnostico/cap4/diag/ejercicios_en_pantalla.out
"""
import json, re, pathlib
H = (pathlib.Path(__file__).resolve().parents[3] / 'Htmls_Series/capitulo-4-modelos-arima.html').read_text(encoding='utf8')
L = H.split('\n')
lin = next(l for l in L if l.strip().startswith('const DATOS_CAP4 = '))
D = json.loads(lin.strip()[len('const DATOS_CAP4 = '):].rstrip(';'))
def busca(patron, hasta=8880):
    return [i + 1 for i, l in enumerate(L[:hasta]) if re.search(patron, l) and 'DATOS_CAP4' not in l]
print('Claves de primer nivel de DATOS_CAP4:', list(D.keys()))
def camino(d, pref=''):
    for k, v in (d.items() if isinstance(d, dict) else []):
        if k in ('sigma_h', 'psi', 'sigma') and isinstance(v, (list, float, int)):
            yield pref + k, v
        else:
            yield from camino(v, pref + k + '.')
for k, v in camino(D):
    print(k, v[:3] if isinstance(v, list) else v)
print('Q1 (1264.60 y 1267.51 juntos en una tabla o frase):', busca(r'1264\.60'))
print('Q2 (151.97 escrito):', busca(r'151\.9'), '· el simulador pesos-psi-sigma muestra σₕ con fmt(…, 3) al mover h a 2')
print('Q3 (0.7245 / 0.72 en rezago 12):', busca(r'0\.7245|0\.72\b'))
print('Q4 (920.70):', busca(r'920\.70'))
print('Q5 (100 % con el escalón del Nilo):', busca(r'100\\,\\%'))
print('Q6 (0.498, 0.385):', busca(r'0\.498'))
print('Q7 (1269.348 y +1.84):', busca(r'1269\.348|\+1\.84'))
print('Q8 (θ = -1.000 y raíz 1.000 en d = 2):', busca(r'-1\.000|1\.0000'))
