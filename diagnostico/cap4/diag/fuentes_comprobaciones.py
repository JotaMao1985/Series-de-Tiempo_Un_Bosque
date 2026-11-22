#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprobaciones en Python detrás del inventario de fuentes del capítulo 4 (statsmodels 0.14.6).
No escribe nada fuera de la salida estándar. De las docstrings solo se imprimen booleanos, nunca el texto.
Uso:  python3 diagnostico/cap4/diag/fuentes_comprobaciones.py > diagnostico/cap4/diag/fuentes_comprobaciones_py.out
"""
import inspect, warnings
import numpy as np
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa import stattools
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma2ma, ArmaProcess
from statsmodels.stats.diagnostic import acorr_ljungbox
warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, "· numpy", np.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values

print("\n== statsmodels no trae el algoritmo de Hyndman–Khandakar (c4-m7)")
import statsmodels.tsa as tsa, pkgutil
mods = [m.name for m in pkgutil.walk_packages(tsa.__path__, tsa.__name__ + ".")]
print("módulos de statsmodels.tsa cuyo nombre contiene 'auto_arima' o 'autoarima':", [m for m in mods if "auto" in m.lower() and "arima" in m.lower()])
print("pmdarima importable aquí:", end=" ")
try:
    import pmdarima  # noqa
    print(True)
except Exception:
    print(False, "(no se puede comprobar su documentación ni su ndiffs)")
print("statsmodels.tsa.stattools tiene 'ndiffs':", hasattr(stattools, "ndiffs"))

print("\n== ARIMA: trend por defecto y deriva con d >= 1 (c4-m5)")
for d, tr in ((0, None), (1, None), (1, "t"), (2, "t")):
    try:
        kw = {} if tr is None else {"trend": tr}
        f = ARIMA(nilo, order=(1, d, 1), **kw).fit()
        print(f"ARIMA(1,{d},1) trend={tr!r}: parámetros {f.param_names}")
    except Exception as e:
        print(f"ARIMA(1,{d},1) trend={tr!r}: {type(e).__name__}")
try:
    f = ARIMA(nilo, order=(1, 2, 1), trend=[0, 0, 1]).fit(); print("ARIMA(1,2,1) trend=[0,0,1]:", f.param_names)
except Exception as e:
    print("trend=[0,0,1] con d=2:", type(e).__name__)

print("\n== nobs, nobs_effective, aicc (c4-m6, m7)")
f = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
print("nobs =", f.nobs, "· nobs_effective =", getattr(f, "nobs_effective", None), "· loglikelihood_burn =", f.loglikelihood_burn)
k = len(f.params); a_nobs = f.aic + 2 * k * (k + 1) / (f.nobs - k - 1); a_eff = f.aic + 2 * k * (k + 1) / (f.nobs_effective - k - 1)
print(f"aicc con nobs = {a_nobs:.3f} · con nobs_effective = {a_eff:.3f} · f.aicc = {f.aicc:.3f}")

print("\n== kpss: truncamiento (c4-m3)")
print("firma de kpss:", inspect.signature(stattools.kpss))
for nl in ("auto", "legacy", 4):
    print(f"kpss(nilo, 'c', nlags={nl!r}) = {stattools.kpss(nilo, regression='c', nlags=nl)[0]:.4f}")
kd = stattools.kpss.__doc__ or ""
print("docstring de kpss habla de 'legacy' y de 'auto':", "legacy" in kd and "auto" in kd)
print("valor crítico 5 % del kpss de nivel (statsmodels):", stattools.kpss(nilo, regression="c", nlags=4)[3]["5%"])

print("\n== pacf: método por defecto y 'ldb' (c4-m4)")
print("firma de pacf:", inspect.signature(stattools.pacf))
print("docstring de pacf habla de 'ldb' y 'ywadjusted':", "ldb" in (stattools.pacf.__doc__ or "") and "ywadjusted" in (stattools.pacf.__doc__ or ""))
w = np.diff(nilo)
print("pacf(w, 6, 'ldb')   =", np.round(stattools.pacf(w, nlags=6, method="ldb")[1:], 4))
print("pacf(w, 6, defecto) =", np.round(stattools.pacf(w, nlags=6)[1:], 4))

print("\n== acorr_ljungbox: model_df (c4-m2, m4)")
print("firma:", inspect.signature(acorr_ljungbox))
print("docstring habla de model_df 'degrees of freedom ... model':", "model_df" in (acorr_ljungbox.__doc__ or ""))

print("\n== arma2ma y ArmaProcess: polinomios completos con el signo ya aplicado (c4-m1, m9)")
print("arma2ma(ar=[1,-0.5], ma=[1], lags=4):", np.round(arma2ma(np.r_[1, -0.5], np.r_[1], lags=4), 4), " (ψ_j = 0.5^j si el AR va con signo ya cambiado)")
print("docstring de arma2ma habla de 'lag polynomial' con el cero:", "polynomial" in (arma2ma.__doc__ or ""))
p = ArmaProcess(ar=np.r_[1, -0.2544], ma=np.r_[1, -0.8741]); print("ArmaProcess(ar=[1,-.2544], ma=[1,-.8741]).arroots módulo:", np.round(np.abs(p.arroots), 4), "· maroots módulo:", np.round(np.abs(p.maroots), 4))

print("\n== adfuller: p-valor por MacKinnon (c4-m3, m10)")
est, p, *_ = stattools.adfuller(nilo, regression="ct", autolag=None, maxlag=int((len(nilo) - 1) ** (1 / 3)))
print(f"adfuller(nilo, 'ct', maxlag=4) = {est:.4f}  p = {p:.4f}")
ad = stattools.adfuller.__doc__ or ""
print("docstring de adfuller cita a MacKinnon:", "MacKinnon" in ad)

print("\n== ARIMA con d = 2 y trend='t': el mensaje del ValueError (c4-m5)")
try:
    ARIMA(nilo, order=(1, 2, 1), trend="t").fit()
except ValueError as e:
    m = str(e)
    print("el mensaje habla de términos de orden menor que d + D eliminados por la diferenciación:", "lower order than `d + D`" in m and "eliminated due to the differencing" in m)
