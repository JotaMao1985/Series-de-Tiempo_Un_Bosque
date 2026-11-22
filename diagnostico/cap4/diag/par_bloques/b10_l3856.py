import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

nilo = sm.datasets.nile.load_pandas().data["volume"].values

# d = 0: trend="c" da la media del proceso, igual que el "intercept" de R
f0 = ARIMA(nilo, order=(1, 0, 1), trend="c").fit()
print(f0.param_names, np.round(f0.params, 4))
#> ['const', 'ar.L1', 'ma.L1', 'sigma2'] [ 9.19350500e+02  8.61000000e-01
#>                                        -5.17600000e-01  1.98070486e+04]
#   919.35 es EXACTAMENTE la media muestral de la serie; R devuelve
#   920.7037, el valor que maximiza la verosimilitud junto al resto de
#   parametros. statsmodels no se aleja del valor inicial porque la
#   verosimilitud es muy plana en la media (e.e. = 46.67 en R).
#   0.15 % de diferencia: no cambia ninguna conclusion.

# d = 1 con deriva: trend="t" (un termino lineal en t)
f1 = ARIMA(nilo, order=(1, 1, 1), trend="t").fit()
i = f1.param_names.index("x1")
print(round(f1.params[i], 4), round(f1.bse[i], 4), round(f1.params[i] / f1.bse[i], 3))
#> -2.8518 2.124 -1.343       R: -2.8827, 2.0167, t = -1.429
#   distinto numero, misma conclusion: no es significativa

# d = 2: statsmodels TAMPOCO la ajusta, y ademas lo explica mejor que R
try:
    ARIMA(nilo, order=(1, 2, 1), trend="t").fit()
except ValueError as e:
    print(str(e)[:78])
#> In models with integration (`d > 0`) or seasonal integration (`D > 0`), tre
#   ...un termino de orden MENOR que d lo elimina la propia diferenciacion.
#   Lo unico admisible con d = 2 es un termino cuadratico:
f2 = ARIMA(nilo, order=(1, 2, 1), trend=[0, 0, 1]).fit()
print(f2.param_names)
#> ['x1', 'ar.L1', 'ma.L1', 'sigma2']