# Verificación independiente (Python) de cifras nuevas o cambiadas en la R1 del cap. 4
# MPLBACKEND=Agg python3 diagnostico/cap4/comprobaciones/v1_python.py > .../v1_python.out 2>&1
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, statsmodels, statsmodels.api as sm, scipy
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from statsmodels.stats.diagnostic import acorr_ljungbox
print("statsmodels", statsmodels.__version__, "numpy", np.__version__, "scipy", scipy.__version__)

nilo = sm.datasets.nile.load_pandas().data["volume"].values
print("\n== M2: coeficientes y Ljung-Box sin el primer residual ==")
aj = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
print("params", np.round(aj.params, 6), " R: 0.254370 -0.874135")
print("resid[0:3]", np.round(aj.resid[:3], 3))
for nombre, r in (("completo", aj.resid), ("sin y1", aj.resid[1:])):
    print(nombre, round(float(acorr_ljungbox(r, lags=[20], model_df=2)["lb_pvalue"].iloc[0]), 4))
print("pronostico", np.round(aj.get_forecast(3).predicted_mean, 2))

print("\n== M3: cociente y r1 ==")
r1 = acf(nilo, nlags=1)[1]
print(round(np.diff(nilo).var(ddof=1) / nilo.var(ddof=1), 3), round(2 * (1 - r1), 3))
print([round(float(acf(np.diff(nilo, n=d), nlags=1)[1]), 3) for d in (1, 2)])

print("\n== M7: AICc de statsmodels, rejilla d = 1 ==")
mejor, mejor_aicc, ev = None, np.inf, 0
for p in range(4):
    for q in range(4):
        try:
            f = ARIMA(nilo, order=(p, 1, q), trend="n").fit()
        except Exception:
            continue
        ev += 1
        if f.aicc < mejor_aicc:
            mejor, mejor_aicc, fm = (p, 1, q), f.aicc, f
print(mejor, round(mejor_aicc, 3), ev, "AIC", round(fm.aic, 3), "nobs_eff", fm.nobs_effective if hasattr(fm, "nobs_effective") else None)
k = len(fm.params)
for n in (100, 99):
    print("AICc con n =", n, round(fm.aic + 2 * k * (k + 1) / (n - k - 1), 4))

print("\n== M8: escalón, t ==")
anios = np.arange(1871, 1971)
esc = (anios >= 1899).astype(float).reshape(-1, 1)
fe = ARIMA(nilo, order=(0, 0, 0), exog=esc, trend="c").fit()
print(round(fe.params[1], 2), round(fe.bse[1], 2), round(fe.params[1] / fe.bse[1], 2))

print("\n== TRM desde la copia fija ==")
y = pd.read_csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")["trm"].values
d1 = np.diff(y); rw = ARIMA(y, order=(0, 1, 0), trend="n").fit()
s = np.sqrt(np.mean(d1**2))  # MLE de la caminata sin deriva
print("s", round(s, 4), "sigma2 statsmodels", round(rw.params[-1], 3))
print("skew", round(float(stats.skew(d1)), 4), "cubre80", round(float(np.mean(np.abs(d1) <= stats.norm.ppf(0.90) * s)), 4))
print([round(np.mean((y[h:] - y[:-h])**2) / (h * s**2), 4) for h in (3, 6, 12)])

print("\n== E2: log(lynx) r1 de la diferencia ==")
# lynx no está en statsmodels: se omite (se calcula en R)
