# Lector B · M3 y M4: comportamiento de statsmodels/numpy comprobado ejecutando
import inspect, warnings
import numpy as np, statsmodels, statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
warnings.simplefilter("ignore")
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values
n = len(nilo)

print("\n== adfuller")
est, p, usedlag, nobs, crit = adfuller(nilo, regression="ct", autolag=None, maxlag=int((n-1)**(1/3)))
print("adfuller ct, maxlag=4:", round(est, 4), round(p, 4), "usedlag", usedlag, "nobs", nobs)
doc = adfuller.__doc__
print("docstring cita MacKinnon:", "MacKinnon" in doc)
i = doc.find("MacKinnon"); print("   ...", " ".join(doc[max(0, i-200):i+120].split()))
print("(la prueba PP no esta en statsmodels.tsa.stattools:", not hasattr(__import__('statsmodels.tsa.stattools', fromlist=['x']), 'pp'), ")")

print("\n== kpss")
for nl in ("auto", "legacy", 4):
    s, pv, lags, crit = kpss(nilo, regression="c", nlags=nl)
    print(f"nlags={nl!r}: stat {s:.4f} p {pv:.4f} lags usados {lags}  crit {crit}")
k = kpss.__doc__
for pal in ("legacy", "auto", "Hobijn", "Newey", "Bartlett", "ceil"):
    j = k.find(pal)
    print(f"[{pal}]", " ".join(k[max(0, j-150):j+250].split()) if j >= 0 else "no aparece")
src = inspect.getsource(kpss)
print("fórmulas en el código de kpss:")
for ln in src.splitlines():
    if "12" in ln and ("nobs" in ln or "power" in ln or "ceil" in ln): print("   ", ln.strip())
    if "legacy" in ln and ("lags" in ln or "nlags" in ln): print("   ", ln.strip())

print("\n== kpss: función de truncamiento 'auto'")
from statsmodels.tsa import stattools
for nm in ("_kpss_autolag",):
    if hasattr(stattools, nm):
        print(inspect.getsource(getattr(stattools, nm))[:1500])

print("\n== acf / pacf de la serie diferenciada")
w = np.diff(nilo)
print("acf(adjusted=False) 1..6:", np.round(acf(w, nlags=6)[1:], 4))
print("acf(adjusted=True) 1..6:", np.round(acf(w, nlags=6, adjusted=True)[1:], 4))
print("acf rezago 0 primero:", acf(w, nlags=2)[0])
print("firma de acf:", inspect.signature(acf))
print("pacf defecto  :", np.round(pacf(w, nlags=6)[1:], 4), " firma method =", inspect.signature(pacf).parameters["method"].default)
print("pacf ldb      :", np.round(pacf(w, nlags=6, method="ldb")[1:], 4))
print("pacf ld       :", np.round(pacf(w, nlags=6, method="ld")[1:], 4))
print("pacf ywm      :", np.round(pacf(w, nlags=6, method="ywm")[1:], 4))
doc = pacf.__doc__
for pal in ("ywadjusted", "ldb", "Durbin", "Levinson"):
    j = doc.find(pal); print(f"[{pal}]", " ".join(doc[max(0, j-60):j+200].split()) if j >= 0 else "no aparece")

print("\n== ARIMA(0,1,1): primer residual")
ma1 = ARIMA(nilo, order=(0, 1, 1), trend="n").fit()
print("theta", round(ma1.params[0], 4), " primer residual", round(float(ma1.resid[0]), 2), " y_1", nilo[0])
print("LB(20), model_df=1, sin el primero:", round(float(acorr_ljungbox(ma1.resid[1:], lags=[20], model_df=1)["lb_pvalue"].iloc[0]), 4))

print("\n== numpy.diff(n=0) es la identidad")
print(np.array_equal(np.diff(nilo, n=0), nilo))

print("\n== varianza (ddof=1) por d")
for d in range(4):
    x = np.diff(nilo, n=d) if d else nilo
    print(d, len(x), round(x.var(ddof=1), 2))
