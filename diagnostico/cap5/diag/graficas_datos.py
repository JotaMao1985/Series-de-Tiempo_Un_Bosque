#!/usr/bin/env python3
"""Contraste de los datos incrustados del cap. 5 (DATOS_CAP5, SERIES_CAP5) con lo que afirman la prosa, las
intros de los simuladores y sus lecturas. Solo lee el HTML final; no calcula nada que no esté en él salvo
transformaciones elementales (log, diferencias, ACF muestral como la de calcularACF()).

Uso: python3 diagnostico/cap5/diag/graficas_datos.py > diagnostico/cap5/diag/graficas_datos.out
"""
import json, math, os
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
L = open(os.path.join(RAIZ, 'Htmls_Series', 'capitulo-5-sarima.html'), encoding='utf-8').read().split('\n')
def obj(pref):
    for i, l in enumerate(L):
        t = l.strip()
        if t.startswith(pref):
            return json.loads(t[len(pref):].rstrip(';')), i + 1
D, lD = obj('const DATOS_CAP5 = ')
S, lS = obj('const SERIES_CAP5 = ')
print(f'DATOS_CAP5 en HTML l. {lD}; SERIES_CAP5 en l. {lS}\n')
AP = D['airpassengers']

def acf(x, K):
    n = len(x); m = sum(x) / n; c = [v - m for v in x]; g0 = sum(v * v for v in c) / n
    return [sum(c[t] * c[t + k] for t in range(n - k)) / n / g0 for k in range(1, K + 1)]
def dif(x): return [x[t] - x[t - 1] for t in range(1, len(x))]
def difm(x, m=12): return [x[t] - x[t - m] for t in range(m, len(x))]
def fuera(a, n):
    b = 1.96 / math.sqrt(n); return b, [k + 1 for k, v in enumerate(a) if abs(v) > b]

print('== M1 mapa-firma: «AirPassengers con log y las dos diferencias … la ACF se queda con dos barras, en 1 y 12»')
y = [math.log(v) for v in S['airpassengers']['valores']]
for nombre, z in [('log', y), ('∇ log', dif(y)), ('∇12 log', difm(y)), ('∇∇12 log', dif(difm(y)))]:
    a = acf(z, min(36, len(z) - 2)); b, f = fuera(a, len(z))
    print(f'  {nombre:10s} n={len(z)} banda={b:.4f} fuera de banda ({len(f)}): {f}')
    if nombre == '∇∇12 log':
        print('    valores fuera:', {k: round(a[k - 1], 4) for k in f})
print('\n== M1 tabla «Dónde mirar la ACF» frente a lo que el simulador calcula (log por defecto activado)')
for se, lg in [('airpassengers', True), ('usaccdeaths', False), ('usaccdeaths', True), ('co2', False), ('trm', False)]:
    z = S[se]['valores']; z = [math.log(v) for v in z] if lg else z
    a = acf(z, 36); b = 1.96 / math.sqrt(len(z))
    print(f'  {se:14s} log={lg!s:5s} ρ1={a[0]:.4f} ρ12={a[11]:.4f} ρ24={a[23]:.4f} ρ36={a[35]:.4f} banda={b:.4f}')
z = dif(S['trm']['valores']); a = acf(z, 36); b = 1.96 / math.sqrt(len(z))
print(f'  ∇TRM (sin log)  ρ1={a[0]:.4f} ρ12={a[11]:.4f} ρ24={a[23]:.4f} ρ36={a[35]:.4f} banda={b:.4f}  (tabla: 0.088, −0.002, −0.067, 0.071, 0.167)')
for lg in (True, False):
    for nombre, f in [('∇', lambda x: dif(x)), ('∇12', lambda x: difm(x)), ('∇∇12', lambda x: dif(difm(x)))]:
        z = S['trm']['valores']; z = [math.log(v) for v in z] if lg else z; z = f(z)
        a = acf(z, 36); b, ff = fuera(a, len(z))
        print(f'  TRM log={lg!s:5s} {nombre:5s}: estacionales fuera {[k for k in (12, 24, 36) if k in ff]}; todas las fuera {ff}')

print('\n== M3 cuatro-combinaciones: cifras de la intro y de la tabla')
for k, c in AP['combinaciones'].items():
    print(f"  {k}: n={c['n']} var={c['varianza']} ρ1={c['acf1']} ρ12={c['acf12']} etiqueta={c['etiqueta']!r} fechas {c['fechas'][0]}..{c['fechas'][-1]} ({len(c['fechas'])}/{len(c['valores'])})")
print('\n== M3 sobrediferenciación: varianza (R) frente a la calculada en el navegador')
for info in AP['sobrediferenciacion_estacional']:
    Dd = info['D']; z = y
    for _ in range(Dd): z = difm(z)
    z = dif(z); m = sum(z) / len(z); v = sum((t - m) ** 2 for t in z) / (len(z) - 1)
    print(f"  D={Dd}: n R={info['n']} JS={len(z)}  var R={info['varianza']} JS={v:.6f}  Θ̂={info['theta_est']} raíz={info['raiz_ma']}")

print('\n== M2 receta / M4 firma: ρ1, ρ11, ρ12, ρ13 de AR(1)×SAR(1) φ=0.6 Φ=0.7 (prosa: 0.6016, 0.4230, 0.7011, 0.4218)')
t = D['teoricas']['ar1_sar1']['acf']; print('  teoricas.ar1_sar1:', t[0], t[10], t[11], t[12])

def psi_airline(th, Th, H=37):
    # (1+θB)(1+ΘB^12) / ((1-B)(1-B^12))
    c = lambda j: (j // 12 + 1) if j >= 0 else 0
    return [c(j) + th * c(j - 1) + Th * c(j - 12) + th * Th * c(j - 13) for j in range(H)]
print('\n== M5 airline-pesos: «Lleva Θ hacia 0 y el escalón del rezago 12 desaparece»; «hacia −1 … los pesos se aplanan»')
for th, Th in [(-0.40, -0.56), (-0.40, 0.0), (-0.40, -0.95), (0.5, 0.5), (-0.95, 0.5), (0, 0)]:
    p = psi_airline(th, Th)
    print(f'  θ={th:+.2f} Θ={Th:+.2f}: ψ1..11={p[1]:.3f} ψ12={p[12]:.3f} ψ13={p[13]:.3f} ψ24={p[24]:.3f} ψ35={p[35]:.3f}  salto en 12 = {p[12]-p[11]:+.3f}  máx(ψ0..35)={max(p[:36]):.3f}')
print('  psi del precálculo:', AP['pronostico']['psi'][:14])

print('\n== M7 pronóstico: el abanico «se ensancha de golpe al cruzar cada rezago estacional»')
sh = AP['pronostico']['sigma_h']; inc = [round(sh[i] - sh[i - 1], 5) for i in range(1, len(sh))]
print('  σh:', sh); print('  incrementos σh(h)−σh(h−1), h=2..24:', inc)
o = AP['pronostico']['original']; lg = AP['pronostico']['log']
print('  claves original:', list(o.keys()), ' log:', list(lg.keys()))
print(f"  h=24 original: media={o['media'][23]} lo95={o['lo95'][23]} hi95={o['hi95'][23]}  (prosa: 525.46, 399.66, 690.85)")
anch = [round(lg['hi95'][i] - lg['lo95'][i], 4) for i in range(24)]
print('  ancho IC95 log por h:', anch)

print('\n== M8 contraejemplo: «los tres múltiplos de 12 salen de la banda» / «ninguno de los tres se acerca a la banda»')
c = AP['combinaciones']['d1_D0']; b = 1.96 / math.sqrt(c['n'])
print(f"  ∇log AP n={c['n']} banda={b:.4f} ρ12={c['acf'][11]} ρ24={c['acf'][23]} ρ36={c['acf'][35]}")
C = D['trm_contraejemplo']['correlogramas']; b = 1.96 / math.sqrt(C['n'])
print(f"  ∇TRM n={C['n']} banda={b:.4f} ρ12={C['acf'][11]} ρ24={C['acf'][23]} ρ36={C['acf'][35]}; fuera en todos: {fuera(C['acf'], C['n'])[1]}")

print('\n== M9 calendario')
cal = AP['calendario']
print('  pascuas:', cal['pascuas']); print('  meses_pascua_marzo =', cal['meses_pascua_marzo'], ' rango_dias', cal['rango_dias'])
print('  len fechas', len(cal['fechas']), 'len dias', len(cal['dias_mes']), 'len log', len(AP['log']))
for k, m in cal['modelos'].items():
    print(f"  {k}: {m.get('nombre')} aicc={m['aicc']} bic={m['bic']} coef={[ (x['nombre'], x['valor'], x.get('ee'), x.get('t')) for x in m['coeficientes']]}")

print('\n== M10 armónicos: «hasta K=4 … conservan estructura; hace falta K=5»')
for r in D['airpassengers']['fourier']['resultados']:
    print(f"  K={r['K']} términos={r['n_terminos']} par={r['n_par_total']} nobs={r['nobs']} errores={r['modelo_errores']!r} aicc={r['aicc']} lb24_p={r['lb24_p']} acf12={r['acf12']}")
cur = AP['fourier']['curvas']
print('  amplitud de cada curva (máx−mín) en los dos primeros años:', [round(max(c[:24]) - min(c[:24]), 4) for c in cur])
print('  mes del máximo de cada curva (1949):', [AP['fechas'][max(range(12), key=lambda i: c[i])] for c in cur])

print('\n== M11 comparativa')
comp = AP['comparativa']
for k in comp['orden_rmse']:
    m = comp['modelos'][k]
    print(f"  {k:12s} nombre={m['nombre']!r} ({len(m['nombre'])} car.) → [:34]={m['nombre'][:34]!r} [:26]={m['nombre'][:26]!r}  rmse={m['rmse']} mae={m['mae']} mape={m['mape']}")
pa = comp['modelos'].get('sarima', {}).get('pronostico'); pb = comp['modelos'].get('auto_arima', {}).get('pronostico')
print('  claves:', list(comp['modelos'].keys()))
for k1 in comp['modelos']:
    for k2 in comp['modelos']:
        if k1 < k2 and comp['modelos'][k1]['pronostico'] == comp['modelos'][k2]['pronostico']:
            print(f'  pronósticos idénticos: {k1} = {k2}')
for met in ('rmse', 'mae', 'mape'):
    orden = sorted(comp['orden_rmse'], key=lambda k: comp['modelos'][k][met])
    print(f'  orden por {met}: {orden}  → SARIMA en el puesto {orden.index("sarima") + 1}')

print('\n== Quiz (M4 en el registro, se dibuja en el quiz del M11): SAR(1) Φ=0.7 → ρ12, ρ24, ρ36 = 0.7, 0.49, 0.343')
print('  teoricas.sar1_pos:', [D['teoricas']['sar1_pos']['acf'][k - 1] for k in (11, 12, 13, 24, 36)])

print('\n== M6 explorador: modelos de la rejilla sin acf o con huecos')
for k, m in AP['rejilla'].items():
    if not m.get('acf') or len(m['acf']) != 24 or any(v is None for v in m['acf']) or m.get('aicc') is None:
        print('  ', k, {kk: (vv if not isinstance(vv, list) else len(vv)) for kk, vv in m.items()})
print('  mejores_aicc:', AP['mejores_aicc'], ' mejor_bic:', AP['mejor_bic'])
nul = [k for k, m in AP['rejilla'].items() if m.get('raiz_ma') is None]
print('  raiz_ma nula en:', nul)
lbr = [k for k, m in AP['rejilla'].items() if m['lb_p'] < 0.05]
print('  Ljung–Box rechaza en', len(lbr), ':', lbr)
