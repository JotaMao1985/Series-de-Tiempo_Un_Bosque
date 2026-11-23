"""Verificador A · R4 cap. 4 · las `propia` de M1–M6 que hablan de statsmodels
(c4-m1-27, c4-m3-29, c4-m3-64, c4-m5-14) y el n efectivo del BIC (c4-m6-02)."""
import warnings, inspect
import numpy as np, statsmodels, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.stattools import kpss, acf
warnings.simplefilter("ignore")
print("statsmodels", statsmodels.__version__, "| numpy", np.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values.astype(float)
print("n =", len(nilo), "| primeros:", nilo[:3], "| igual a R (1120 1160 963):", list(nilo[:3]) == [1120, 1160, 963])

print("\n== c4-m1-27: convenio de signo del MA en statsmodels ==")
print("ArmaProcess(ma=[1, .5]).acf(2)[1] =", ArmaProcess(ar=[1], ma=[1, .5]).acf(2)[1])
rng = np.random.default_rng(3)
x = ArmaProcess(ar=[1], ma=[1, .6]).generate_sample(2000, distrvs=rng.standard_normal)
f = ARIMA(x, order=(0, 0, 1)).fit()
print("ARIMA(0,0,1) sobre MA(1) con theta = +0.6: ma.L1 =", round(f.params[1], 4))

print("\n== c4-m3-29 / c4-m3-64: KPSS de statsmodels sobre el Nilo ==")
for nl in ["auto", "legacy", 4]:
    st, p, lags, crit = kpss(nilo, regression="c", nlags=nl)
    print(f"nlags={nl!r}: estadístico {st:.14f} | rezagos usados {lags} | crit 5% {crit['5%']}")
src = inspect.getsource(kpss)
print("código de nlags='legacy':", [l.strip() for l in src.splitlines() if "np.ceil" in l])
print("ACF 1-12 positivas:", bool(np.all(acf(nilo, nlags=12)[1:] > 0)))

print("\n== c4-m5-14: argumento trend de statsmodels ARIMA ==")
print("ARIMA(1,0,1) por defecto:", ARIMA(nilo, order=(1, 0, 1)).fit().model.param_names)
print("ARIMA(1,1,1) por defecto:", ARIMA(nilo, order=(1, 1, 1)).fit().model.param_names)
print("ARIMA(1,1,1, trend='t'):", ARIMA(nilo, order=(1, 1, 1), trend="t").fit().model.param_names)
try:
    ARIMA(nilo, order=(1, 2, 1), trend="t")
    print("ARIMA(1,2,1, trend='t'): sin error")
except ValueError as e:
    print("ARIMA(1,2,1, trend='t'): ValueError:", str(e)[:200])

print("\n== c4-m6-02: el BIC de statsmodels usa el n efectivo ==")
r = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
k = r.df_model
print("nobs_effective =", r.nobs_effective, "| df_model =", k)
print("bic =", round(r.bic, 4), "| -2llf + k log(99) =", round(-2*r.llf + k*np.log(99), 4), "| con log(100) =", round(-2*r.llf + k*np.log(100), 4))
print("aicc =", round(r.aicc, 4), "| a mano n*=99:", round(-2*r.llf + 2*k + 2*k*(k+1)/(99-k-1), 4))
