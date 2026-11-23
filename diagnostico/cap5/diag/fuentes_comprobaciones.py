#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprobaciones en Python detrás del inventario de fuentes del capítulo 5 (statsmodels no tiene obra en la biblioteca).
No escribe nada fuera de la salida estándar. Necesita R en el PATH (para sacar log(AirPassengers) sin red).
Uso:  python3 diagnostico/cap5/diag/fuentes_comprobaciones.py > diagnostico/cap5/diag/fuentes_comprobaciones_py.out
"""
import inspect
import io
import subprocess
import warnings

import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, " · numpy", np.__version__)

r = subprocess.run(["Rscript", "-e", 'cat(paste(as.numeric(log(AirPassengers)), collapse=","))'], capture_output=True, text=True)
ap = np.array([float(x) for x in r.stdout.split(",")])
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))

print("\n== simple_differencing y nobs (l. 3747-3750, 4756-4789 del capítulo)")
for sd in (False, True):
    f = SARIMAX(s, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n", simple_differencing=sd).fit(disp=False)
    print(f"simple_differencing={sd!s:5}  nobs={int(f.nobs)}  ma1={f.params['ma.L1']:+.4f}  sma1={f.params['ma.S.L12']:+.4f}  llf={f.llf:.4f}")

print("\n== get_forecast con simple_differencing=True (l. 5041-5046)")
mal = SARIMAX(s, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n", simple_differencing=True).fit(disp=False)
bien = SARIMAX(s, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit(disp=False)
print("pronóstico a 24 meses con simple_differencing=True:", round(float(mal.get_forecast(steps=24).predicted_mean.iloc[-1]), 4),
      " · con la opción por defecto:", round(float(bien.get_forecast(steps=24).predicted_mean.iloc[-1]), 4))

print("\n== plot_acf: lags por defecto y divisor (l. 3225-3227)")
from statsmodels.graphics.tsaplots import plot_acf
sig = inspect.signature(plot_acf)
print("lags por defecto:", sig.parameters["lags"].default, " · adjusted por defecto:", sig.parameters["adjusted"].default)

print("\n== statsmodels no trae ndiffs / nsdiffs (l. 4190)")
import statsmodels.tsa.stattools as st
print("ndiffs en stattools:", hasattr(st, "ndiffs"), " · nsdiffs en stattools:", hasattr(st, "nsdiffs"))

print("\n== KPSS: valor crítico del 5 % (l. 4196 y 5105; el bloque lo teclea)")
from statsmodels.tsa.stattools import kpss
x = np.arange(200.0) + np.random.default_rng(1).normal(size=200)
est, p, lags, crit = kpss(x, regression="c", nlags=4)
print("valores críticos de statsmodels (regression='c'):", crit)

print("\n== Fourier en statsmodels (l. 5650-5674)")
from statsmodels.tsa.deterministic import DeterministicProcess, Fourier
for K in (5, 6):
    X = DeterministicProcess(s.index, constant=False, additional_terms=[Fourier(12, order=K)]).in_sample()
    print(f"K={K}: columnas={X.shape[1]}  rango={np.linalg.matrix_rank(X.values)}  columnas idénticamente cero={[c for c in X.columns if X[c].abs().max() < 1e-12]}")
print("DeterministicProcess y Fourier existen; auto_arima en statsmodels:", hasattr(statsmodels.tsa, "auto_arima"))
try:
    import pmdarima  # noqa: F401
    print("pmdarima instalado")
except ImportError:
    print("pmdarima no instalado")

print("\n== SARIMAX con exog y d > 0: ¿se diferencian los regresores? (l. 5323-5324)")
dias = s.index.days_in_month.values.astype(float)
f = SARIMAX(s, exog=np.log(dias), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n", simple_differencing=True).fit(disp=False)
print("con simple_differencing=True: nobs =", int(f.nobs), " · coef log(días) =", round(float(f.params.iloc[0]), 4), " · e.e. =", round(float(f.bse.iloc[0]), 4))
f2 = SARIMAX(s, exog=np.log(dias), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit(disp=False)
print("con la opción por defecto:    nobs =", int(f2.nobs), " · coef log(días) =", round(float(f2.params.iloc[0]), 4), " · e.e. =", round(float(f2.bse.iloc[0]), 4))
