# par_verifica.py — afirmaciones del capítulo 5 sobre statsmodels (commit f807b40):
# convergencia del SARIMAX con d y D en el espacio de estados (M6, M7, M8),
# errores estándar con regresores (M9) y el AIC de Fourier (M10).
# Uso: MPLBACKEND=Agg python3 par_verifica.py > par_verifica_py.out 2>&1
import warnings, numpy as np, pandas as pd, statsmodels, statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))
uad = sm.datasets.get_rdataset("USAccDeaths").data["value"].values
su = pd.Series(uad, index=pd.date_range("1973-01", periods=len(uad), freq="MS"))

def sec(t): print(f"\n==================== {t} ====================")

sec("M6/M7 · airline con simple_differencing=False: ¿converge?")
mod = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n")
for kw in [dict(), dict(maxiter=1000), dict(method="nm", maxiter=5000), dict(method="powell", maxiter=5000),
           dict(start_params=[-0.4018, -0.5569, 0.00137], maxiter=1000)]:
    f = mod.fit(disp=False, **kw)
    print(f"{str(kw):60s} conv={f.mle_retvals.get('converged')} ma1={f.params.iloc[0]:+.5f} sma1={f.params.iloc[1]:+.5f} "
          f"llf={f.llf:.5f}")
f0 = mod.fit(disp=False); f1 = mod.fit(disp=False, maxiter=1000)
for nm, f in [("por defecto", f0), ("maxiter=1000", f1)]:
    fc = f.get_forecast(24); ci = fc.conf_int(alpha=0.05)
    print(nm, "h=24 exp:", np.round(np.exp([fc.predicted_mean.iloc[-1], ci.iloc[-1,0], ci.iloc[-1,1]]), 2),
          " LB24 p:", round(sm.stats.acorr_ljungbox(f.resid, lags=[24], model_df=2)["lb_pvalue"].iloc[0], 4),
          " sin 13:", round(sm.stats.acorr_ljungbox(f.resid[13:], lags=[24], model_df=2)["lb_pvalue"].iloc[0], 4),
          " sigma2:", round(f.params["sigma2"], 6))
fs = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n", simple_differencing=True).fit(disp=False)
print("simple_differencing=True: ", np.round(fs.params.values, 5), " llf", round(fs.llf, 5))
print("diferencia de coeficientes (maxiter=1000 frente a R -0.401828 -0.556945):",
      np.round(f1.params.values[:2] - np.array([-0.401828, -0.556945]), 5))

sec("M6/M8 · USAccDeaths sin simple_differencing")
mu = SARIMAX(su, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n")
for kw in [dict(), dict(maxiter=1000), dict(method="nm", maxiter=5000), dict(method="powell", maxiter=5000),
           dict(start_params=[-0.4303, -0.5528, 102860.0], maxiter=1000)]:
    f = mu.fit(disp=False, **kw)
    print(f"{str(kw):60s} conv={f.mle_retvals.get('converged')} ma1={f.params.iloc[0]:+.4f} sma1={f.params.iloc[1]:+.4f} llf={f.llf:.4f}")
fsu = SARIMAX(su, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n", simple_differencing=True).fit(disp=False)
print("simple_differencing=True:", np.round(fsu.params.values[:2], 4))

sec("M9 · regresores: ¿por qué difieren los errores estándar?")
idx = s.index; dias = idx.days_in_month.values.astype(float)
def pascua(anio):
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    f, g = (b + 8) // 25, (b - ((b + 8) // 25) + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    return (h + l - 7*m + 114) // 31
es_p = np.array([1.0 if pascua(t.year) == t.month else 0.0 for t in idx])
X = np.column_stack([np.log(dias), es_p])
m2 = SARIMAX(s, exog=X, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n", simple_differencing=True)
print("exog que ve el modelo (primeras filas): está diferenciada =", not np.allclose(m2.exog[:3, 0], np.log(dias)[:3]),
      np.round(m2.exog[:3], 4).tolist())
for kw in [dict(), dict(maxiter=1000), dict(method="nm", maxiter=20000)]:
    f = m2.fit(disp=False, **kw)
    print(f"{str(kw):30s} conv={f.mle_retvals.get('converged')} coef={np.round(f.params.values, 4)} llf={f.llf:.4f}")
f2 = m2.fit(disp=False, maxiter=1000)
for ct in ["opg", "oim", "approx", "robust"]:
    g = m2.fit(disp=False, maxiter=1000, cov_type=ct)
    print(f"cov_type={ct:7s} ee(x1, x2) = {np.round(g.bse[['x1','x2']].values, 4)}  t = {np.round(g.tvalues[['x1','x2']].values, 4)}"
          f"  (beta-1)/ee = {(g.params['x1'] - 1) / g.bse['x1']:.4f}")
# llf de statsmodels evaluada en los coeficientes de R
pR = np.array([1.0840, 0.0290, -0.3337, -0.5206, f2.params["sigma2"]])
print("llf en los coeficientes de R (orden x1,x2,ma,sma,sigma2):", round(m2.loglike(pR), 4), " llf propia:", round(f2.llf, 4))
print("orden de parámetros:", list(f2.params.index))

sec("M10 · Fourier K = 3 con ARIMA(0,1,4)")
from statsmodels.tsa.deterministic import Fourier, DeterministicProcess
X3 = DeterministicProcess(s.index, constant=False, additional_terms=[Fourier(12, order=3)]).in_sample()
for kw in [dict(), dict(maxiter=1000)]:
    f = SARIMAX(s, exog=X3, order=(0,1,4), trend="n").fit(disp=False, **kw)
    print(kw, "conv", f.mle_retvals.get("converged"), "aic", round(f.aic, 3))

sec("M7 · pronóstico a 24 meses con el ajuste difuso CONVERGIDO")
for kw in [dict(method="nm", maxiter=5000), dict(start_params=[-0.4018, -0.5569, 0.00137], maxiter=1000)]:
    f = mod.fit(disp=False, **kw); fc = f.get_forecast(24); ci = fc.conf_int(alpha=0.05)
    print(kw, np.round(np.exp([fc.predicted_mean.iloc[-1], ci.iloc[-1,0], ci.iloc[-1,1]]), 2),
          " LB24 sin 13:", round(sm.stats.acorr_ljungbox(f.resid[13:], lags=[24], model_df=2)["lb_pvalue"].iloc[0], 4))
