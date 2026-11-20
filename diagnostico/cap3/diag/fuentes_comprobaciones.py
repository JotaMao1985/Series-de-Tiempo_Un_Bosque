#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fuentes_comprobaciones.py · comprobaciones en Python detrás del inventario de fuentes del capítulo 3.

Imprime firmas y booleanos de statsmodels 0.14.6 y comprueba, sobre la caché local de FPP3, que ciertas palabras
NO aparecen (no copia texto). Uso:  python3 diagnostico/cap3/diag/fuentes_comprobaciones.py > diagnostico/cap3/diag/fuentes_comprobaciones_py.out
"""
import inspect
import os

import numpy as np
import statsmodels
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.regression.linear_model import yule_walker
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from statsmodels.tsa.arima_process import ArmaProcess, arma2ar, arma2ma

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
print('statsmodels', statsmodels.__version__, '· numpy', np.__version__)

print('\n== Firmas (c3-m5-06, c3-m6-04, c3-m7-16/17, c3-m8-22, c3-m3-13)')
print('yule_walker          ', inspect.signature(yule_walker))
print('plot_acf bartlett    ', 'bartlett_confint=True' in str(inspect.signature(plot_acf)))
print('plot_pacf method     ', inspect.signature(plot_pacf).parameters['method'].default)
print('generate_sample      ', inspect.signature(ArmaProcess.generate_sample))
print('acorr_ljungbox       ', inspect.signature(acorr_ljungbox))
print('ARIMA enforce_invert.', inspect.signature(ARIMA.__init__).parameters['enforce_invertibility'].default)
print('ARIMAResults.aicc    ', hasattr(ARIMAResults, 'aicc'))

print('\n== ARIMA.fit(method=...) (c3-m7-18)')
doc = ARIMA.fit.__doc__
i = doc.find('method : str')
fragmento = ' '.join(doc[i:i + 520].split())
print('métodos citados en el docstring:', all(k in fragmento for k in ('statespace', 'innovations_mle', 'hannan_rissanen', 'burg', 'innovations', 'yule_walker')))
print("'yule_walker' solo para AR(p):", 'can only be used with AR(p) models' in ' '.join(doc.split()))
try:
    ARIMA(np.random.default_rng(1).standard_normal(100), order=(1, 0, 0)).fit(method='css')
except Exception as e:  # noqa: BLE001
    print("fit(method='css') lanza:", type(e).__name__, '·', str(e)[:60])

print('\n== ArmaProcess: signos del polinomio (c3-m1-11)')
print("docstring de ArmaProcess pide 'the signs from the lag polynomial representation':", 'signs from the lag polynomial' in ' '.join(ArmaProcess.__doc__.split()))
bien = ArmaProcess(ar=np.array([1, -0.6]), ma=np.array([1, 0.7])); mal = ArmaProcess(ar=np.array([1, 0.6]), ma=np.array([1, 0.7]))
print('arcoefs con [1,-0.6]:', bien.arcoefs, '· con [1,0.6]:', mal.arcoefs)
print('arma2ma devuelve psi_0 = 1 (c3-m4-09):', arma2ma(np.r_[1, -0.7], np.r_[1, 0.5], lags=3)[0] == 1.0)
print('numpy.roots usa orden descendente (c3-m1-18): np.roots([1,-0.5]) =', np.roots([1, -0.5]), '· np.roots([-0.5,1]) =', np.roots([-0.5, 1]), '(el polinomio 1 - 0.5x, de raíz 2, es el segundo; R: polyroot(c(1,-0.5)) = 2)')

print('\n== c3-m8-18: primer residual de statsmodels frente al de R')
d = sm.datasets.sunspots.load_pandas().data
x = d.loc[(d.YEAR >= 1770) & (d.YEAR <= 1869), 'SUNACTIVITY'].values
r = ARIMA(x, order=(2, 0, 0), trend='c').fit()
print('resid[:3] =', np.round(r.resid[:3], 3), '· y1 - mu =', round(x[0] - r.params[0], 3), '(R: 21.056, -6.911, 8.728; y1 - mu = 52.538)')

print('\n== Caché de FPP3: palabras que no aparecen (c3-m1-04)')
arima = open(os.path.join(RAIZ, 'bibliografia', '_local', 'web', 'hyndman2021forecasting', 'arima.txt'), encoding='utf-8').read().lower()
print("«airline» en arima.txt:", 'airline' in arima, '· «wold» en arima.txt:', 'wold' in arima)

print('\n== Caché de Shumway (3.ª ed.): ¿hay manchas solares en el cap. 3 (PDF p0096-p0160)? (c3-m10-40)')
hits = []
for n in range(96, 161):
    t = open(os.path.join(RAIZ, 'bibliografia', '_local', 'texto', 'shumway2011time', f'p{n:04d}.txt'), encoding='utf-8').read().lower()
    if 'sunspot' in t:
        hits.append(n)
print('páginas con «sunspot» entre p0096 y p0160:', hits if hits else 'ninguna')
