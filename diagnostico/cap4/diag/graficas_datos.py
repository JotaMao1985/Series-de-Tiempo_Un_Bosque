#!/usr/bin/env python3
"""Contrasta los datos que dibujan los simuladores del cap. 4 con lo que afirman la prosa y las lecturas.

Lee DATOS_CAP4 y SERIES_CAP4 tal como van incrustados en el HTML final (no recalcula nada en R).
Uso: python3 diagnostico/cap4/diag/graficas_datos.py > diagnostico/cap4/diag/graficas_datos.out
"""
import json, math, os, re
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
html = open(os.path.join(RAIZ, 'Htmls_Series', 'capitulo-4-modelos-arima.html'), encoding='utf-8').read().split('\n')
def constante(nombre):
    for l in html:
        s = l.strip()
        if s.startswith(f'const {nombre} = '):
            return json.loads(s[len(f'const {nombre} = '):].rstrip(';'))
D = json.loads(json.dumps(constante('DATOS_CAP4')))
S = constante('SERIES_CAP4')
N = D['nilo']
print('claves DATOS_CAP4:', list(D))
print('claves nilo:', list(N))
banda = lambda n: 1.96 / math.sqrt(n)

print('\n== M4 identificación: barras fuera de banda')
for k, v in N['identificacion'].items():
    b = v['banda']
    fa = [i + 1 for i, r in enumerate(v['acf']) if abs(r) > b]
    fp = [i + 1 for i, r in enumerate(v['pacf']) if abs(r) > b]
    print(f"  {k}: n={v['n']} banda={b:.4f} (1.96/sqrt(n)={banda(v['n']):.4f}) ACF fuera {fa} PACF fuera {fp}")
    print('    ACF ', [round(x, 3) for x in v['acf']])
    print('    PACF', [round(x, 3) for x in v['pacf']])
cr = N['identificacion']['cruda']
print('  último rezago de la ACF cruda dentro de banda:', [i + 1 for i, r in enumerate(cr['acf']) if abs(r) <= cr['banda']])

print('\n== M6 rejilla')
R = N['rejilla']
mej = N['mejor_por_d']
print('  mejor_por_d:', json.dumps(mej)[:400])
rojos = [m['etiqueta'] for m in R.values() if m.get('convergio') and m['ljung_box_p'] <= 0.05]
print('  Ljung–Box p <= 0.05 (barras rojas):', len(rojos), rojos)
print('  no convergen:', [m['etiqueta'] for m in R.values() if not m.get('convergio')])
for d in (0, 1, 2):
    best = mej[f'd{d}']['valor_aicc']
    her = sorted([m for m in R.values() if m['d'] == d and m.get('convergio')], key=lambda m: m['aicc'])
    print(f'  d={d}: ' + '; '.join(f"{m['etiqueta']} +{m['aicc']-best:.2f} LB={m['ljung_box_p']:.3f} AR={m.get('raices',{}).get('min_ar')} MA={m.get('raices',{}).get('min_ma')} deg={m.get('raices',{}).get('degenerado')}" for m in her))
    print(f'     a menos de 2 del mejor (sin contarlo): {sum(1 for m in her if 0 < m["aicc"]-best < 2)}')

print('\n== M7 traza')
HK = N['hyndman_khandakar']
for modo in ('escalonada', 'exhaustiva'):
    pasos = HK[modo]['pasos']
    vals = [p['aicc'] for p in pasos if not p.get('infinito') and p['aicc'] is not None]
    print(f"  {modo}: {len(pasos)} pasos; AICc {min(vals):.3f}..{max(vals):.3f}; infinitos {[i+1 for i,p in enumerate(pasos) if p.get('infinito')]}; mejoras {[i+1 for i,p in enumerate(pasos) if p.get('mejora')]}")
    print('    por encima del TECHO 1302:', [(i + 1, p['etiqueta'], p['aicc']) for i, p in enumerate(pasos) if not p.get('infinito') and p['aicc'] is not None and p['aicc'] > 1302])
    print('    por debajo de 1265:', [(i + 1, p['etiqueta'], p['aicc']) for i, p in enumerate(pasos) if not p.get('infinito') and p['aicc'] is not None and p['aicc'] < 1265])
    print('    primeros:', [(p['etiqueta'], p['aicc'], p.get('mejor_hasta_aqui')) for p in pasos[:4]])

print('\n== M8 sobrediferenciación')
for f in N['sobrediferenciacion']:
    print('  ', {k: f[k] for k in f if not isinstance(f[k], list)})

print('\n== M9 formas e intervalos')
H = D['horizonte']
for k, f in N['formas_pronostico'].items():
    print(f"  {k}: {f['etiqueta']} media[0]={f['media'][0]:.2f} media[-1]={f['media'][-1]:.2f} lo95 {min(f['lo95']):.1f} hi95 {max(f['hi95']):.1f}")
I = N['intervalos']
print('  sigma', I['sigma'], 'len sigma_h', len(I['sigma_h']), 'len psi', len(I['psi']), 'psi[:5]', [round(x, 4) for x in I['psi'][:5]], 'psi[-1]', I['psi'][-1])
print('  sigma_h[0], [1], [29]:', I['sigma_h'][0], I['sigma_h'][1], I['sigma_h'][-1], ' sigma*sqrt(30)=', I['sigma'] * math.sqrt(30))
nilo = S['nilo']['valores']
print('  rango del Nilo observado', min(nilo), max(nilo))

print('\n== M10 TRM')
T = D['trm']
for k in ('cruda', 'd1'):
    v = T['identificacion'][k]
    print(f"  {k}: n={v['n']} banda={v['banda']:.4f} fuera {[i+1 for i,r in enumerate(v['acf']) if abs(r) > v['banda']]} acf[:3]={[round(x,3) for x in v['acf'][:3]]}")
trm = S['trm']
print('  TRM inicio', trm['inicio'], 'n', len(trm['valores']), 'sigma2', T['caminata']['sigma2'])
P = D['puente_estacional']
for k in ('no_estacional', 'estacional'):
    v = P[k]['acf_residuales']
    print(f"  puente {k}: {len(v)} rezagos, fuera {[i+1 for i,r in enumerate(v) if abs(r) > P['no_estacional']['banda']]}, rho12={v[11]:.4f} rho24={v[23]:.4f}")
print('  banda puente', P['no_estacional']['banda'], '1.96/sqrt(n)', banda(P['n']), 'n', P['n'])

print('\n== M3 malla KPSS')
m = N['cambio_nivel']['malla_delta']
print('  ', {k: m[k] for k in m if k != 'puntos'})
for p in m['puntos']:
    print('   ', p)
