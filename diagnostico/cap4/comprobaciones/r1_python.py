"""R1 del capítulo 4 · comprobaciones en Python de los bloques que cambian (2026-11-22).

Uso, desde la raíz del repositorio:
  MPLBACKEND=Agg python3 diagnostico/cap4/comprobaciones/r1_python.py > diagnostico/cap4/comprobaciones/r1_python.out 2>&1
"""
import warnings

import numpy as np
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf

warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, "· numpy", np.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values

print("\n== M2 · Ljung-Box del ARIMA(1,1,1) con y sin el primer residual")
f = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
print("primer residual:", round(float(f.resid[0]), 2))
for nombre, r in (("con y_1", f.resid), ("sin y_1", f.resid[1:])):
    p = float(acorr_ljungbox(r, lags=[20], model_df=2)["lb_pvalue"].iloc[0])
    print(nombre, round(p, 4))

print("\n== M7 · AICc de statsmodels: nobs, nobs_effective y la log-verosimilitud")
k = len(f.params)
print("nobs =", f.nobs, "· nobs_effective =", f.nobs_effective, "· k =", k)
print("aic =", round(f.aic, 4), "· llf =", round(f.llf, 4))
print("aicc (atributo, usa nobs_effective) =", round(f.aicc, 4))
print("aicc a mano con nobs =", round(f.aic + 2 * k * (k + 1) / (f.nobs - k - 1), 4))

print("\n== M3 · varianza por d, cociente y 2(1 - r1); r1 de las diferencias")
r1 = acf(nilo, nlags=1)[1]
print("r1 =", round(r1, 4), "· 2(1 - r1) =", round(2 * (1 - r1), 3),
      "· Var(dy)/Var(y) =", round(np.diff(nilo).var(ddof=1) / nilo.var(ddof=1), 3))
print("r1 de d = 1 y d = 2:", [round(acf(np.diff(nilo, n=d), nlags=1)[1], 3) for d in (1, 2)])

print("\n== M8 · el escalon: coeficiente, e.e. y t")
anios = np.arange(1871, 1971)
esc = (anios >= 1899).astype(float).reshape(-1, 1)
fe = ARIMA(nilo, order=(0, 0, 0), exog=esc, trend="c").fit()
print(round(fe.params[1], 2), round(fe.bse[1], 2), round(fe.params[1] / fe.bse[1], 2))

print("\n== M9 · formato de numpy")
s = np.sqrt(f.params[-1])
print(np.round([s, s, 1.0, 0.1679], 3), "->", np.round([s, s, 1.0, 0.1679], 3).tolist())
print("sigma2 de statsmodels:", round(f.params[-1], 2))
