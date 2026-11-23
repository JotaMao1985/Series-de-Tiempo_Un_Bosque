import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))
fit = SARIMAX(s, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12),
              trend="n", simple_differencing=True).fit(disp=False)
th, Th, s2 = fit.params["ma.L1"], fit.params["ma.S.L12"], fit.params["sigma2"]

print(round(s2 * (1 + th**2) * (1 + Th**2), 6))
#> 0.002051
d1 = np.diff(ap); w = d1[12:] - d1[:-12]
print(round(w.var(ddof=1), 6))
#> 0.002102

# OJO al divisor: statsmodels informa el sigma2 de maxima verosimilitud
# (0.001348) y forecast::Arima lo corrige por los parametros estimados,
# SSR/(n-2) = 0.001371. De ahi que R diga 0.002087 y Python 0.002051 para la
# MISMA varianza teorica. No es un error de ninguno de los dos: es el mismo
# reparto de grados de libertad que el Modulo 6 discute para el AIC.

# El AR no se factoriza: psi_12 = phi^12 + Phi.
from statsmodels.tsa.arima_process import ArmaProcess
phi, Phi = 0.9, 0.7
ar = np.r_[1, -np.r_[phi, np.zeros(10), Phi, -phi * Phi]]
psi = ArmaProcess(ar, np.r_[1]).arma2ma(lags=20000)
print(round(float((psi**2).sum()), 3), round(1 / ((1 - phi**2) * (1 - Phi**2)), 3))
#> 15.406 10.32
print(round(float(psi[12]), 5), round(phi**12 + Phi, 5))
#> 0.98243 0.98243