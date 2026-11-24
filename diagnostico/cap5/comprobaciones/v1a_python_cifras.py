"""Verificador A, R1 cap. 5: cifras nuevas de los bloques de Python, recalculadas aparte,
y la afirmación de que el optimizador por defecto no converge.
MPLBACKEND=Agg /opt/homebrew/Caskroom/mambaforge/base/bin/python3 -W default v1a_python_cifras.py
"""
import warnings
import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_process import arma2ma
from statsmodels.tsa.deterministic import Fourier, DeterministicProcess
import statsmodels
print("statsmodels", statsmodels.__version__)

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))

def ajusta(sd, **kw):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        f = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n",
                    simple_differencing=sd).fit(disp=False, **kw)
    avisos = [str(x.category.__name__) for x in w if "Convergence" in x.category.__name__]
    return f, avisos

print("\n== Optimizador por defecto frente a BFGS (airline) ==")
for sd in (False, True):
    f, av = ajusta(sd)
    g, av2 = ajusta(sd, method="bfgs", maxiter=1000)
    print(f"sd={sd}: defecto conv={f.mle_retvals['converged']} avisos={av} llf={f.llf:.6f} "
          f"ma={f.params['ma.L1']:+.6f} sma={f.params['ma.S.L12']:+.6f} | bfgs conv={g.mle_retvals['converged']} "
          f"avisos={av2} llf={g.llf:.6f} ma={g.params['ma.L1']:+.6f} sma={g.params['ma.S.L12']:+.6f}")

print("\n== M6: Ljung-Box con BFGS ==")
fit, _ = ajusta(False, method="bfgs", maxiter=1000)
print(acorr_ljungbox(fit.resid, lags=[24], model_df=2)["lb_pvalue"].round(4).iloc[0],
      acorr_ljungbox(fit.resid[13:], lags=[24], model_df=2)["lb_pvalue"].round(4).iloc[0])

print("\n== M7: pronostico a 24 con BFGS ==")
fc = fit.get_forecast(steps=24); ci = fc.conf_int(alpha=0.05)
print(np.round(np.exp([fc.predicted_mean.iloc[-1], ci.iloc[-1,0], ci.iloc[-1,1]]), 2),
      round(float(fit.params["sigma2"]), 6))
r_ancho = 690.85 - 399.66; p_ancho = float(np.exp(ci.iloc[-1,1]) - np.exp(ci.iloc[-1,0]))
print("anchura Python / R - 1 =", round(p_ancho / r_ancho - 1, 4))

print("\n== M5: psi y sigma_h ==")
fsd, _ = ajusta(True, method="bfgs", maxiter=1000)
th, TH = fsd.params["ma.L1"], fsd.params["ma.S.L12"]
psi = arma2ma(np.r_[1, -1, np.zeros(10), -1, 1], np.r_[1, th, np.zeros(10), TH, th*TH], lags=241)
sh = np.sqrt(np.cumsum(psi**2))
print(np.round(psi[[1,11,12,13]], 4), round(psi[12]-psi[11], 4), np.round(sh[[0,11,23,35,40,41,119,239]], 3))
print(int(np.argmax(sh > np.sqrt(np.arange(1, len(sh)+1)))) + 1)

print("\n== M9: calendario, OPG frente a hessiana ==")
idx = s.index
dias = idx.days_in_month.values.astype(float)
from dateutil.easter import easter
es_pascua = np.array([1.0 if (easter(d.year).month == d.month) else 0.0 for d in idx])
print("meses con Pascua:", int(es_pascua.sum()))
X = np.column_stack([np.log(dias), es_pascua])
mod = SARIMAX(s, exog=X, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n", simple_differencing=True)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    d0 = mod.fit(disp=False)
print("defecto: conv", d0.mle_retvals["converged"], "avisos", [x.category.__name__ for x in w if "Convergence" in x.category.__name__],
      d0.params[["x1","x2"]].round(4).values, round(d0.llf, 4))
f2 = mod.fit(disp=False, method="bfgs", maxiter=1000)
print("bfgs opg:", f2.mle_retvals["converged"], f2.params[["x1","x2"]].round(4).values, f2.bse[["x1","x2"]].round(4).values, round(f2.llf, 4))
for ct in ("approx", "oim", "robust"):
    fh = mod.fit(disp=False, method="bfgs", maxiter=1000, cov_type=ct)
    print(ct, fh.bse[["x1","x2"]].round(4).values, fh.tvalues[["x1","x2"]].round(4).values,
          round(float((fh.params["x1"]-1)/fh.bse["x1"]), 4))

print("\n== M10: Fourier con maxiter = 2000 y con 50 ==")
for K in range(1, 7):
    dp = DeterministicProcess(s.index, constant=False, additional_terms=[Fourier(12, order=K)])
    Xk = dp.in_sample()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a = SARIMAX(s, exog=Xk, order=(0,1,4), trend="n").fit(disp=False)
    b = SARIMAX(s, exog=Xk, order=(0,1,4), trend="n").fit(disp=False, maxiter=2000)
    c = SARIMAX(s, exog=Xk, order=(0,1,4), trend="n").fit(disp=False, method="bfgs", maxiter=2000)
    print(f"K={K} defecto conv={a.mle_retvals['converged']} aic={a.aic:.2f} | 2000 conv={b.mle_retvals['converged']} aic={b.aic:.2f} | bfgs conv={c.mle_retvals['converged']} aic={c.aic:.2f}")
