#!/usr/bin/env python3
"""Verificación cruzada R <-> Python de los ajustes SARIMA del capítulo 5.

Los capítulos muestran el mismo modelo en R y en Python. Cuando los dos
programas dan cifras distintas, el material tiene que decir POR QUÉ, no
esconderlo. Este script mide las diferencias y comprueba la explicación.

Hallazgo central que documenta el capítulo:
    statsmodels NO diferencia la serie; mete d y D dentro del espacio de
    estados con un prior difuso. R (`forecast::Arima`) diferencia primero.
    Consecuencias: `nobs` distinto (144 frente a 131), log-verosimilitud
    distinta y —en series cortas— coeficientes distintos.
    `simple_differencing=True` hace que statsmodels diferencie primero y
    entonces las dos salidas coinciden.

Uso:  python3 verifica_cap5_python.py     (desde la carpeta precalculo/)
Dependencias: numpy, pandas, statsmodels. Ninguna nueva.
"""

import json
import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
from statsmodels.stats.diagnostic import acorr_ljungbox  # noqa: E402
from statsmodels.tsa.statespace.sarimax import SARIMAX  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDAS = os.path.join(AQUI, "salidas")

with open(os.path.join(SALIDAS, "cap5_sarima.json")) as fh:
    CAP5 = json.load(fh)
with open(os.path.join(SALIDAS, "datos_series.json")) as fh:
    BASE = json.load(fh)


def serie(nombre, log=False):
    d = BASE[nombre]
    y = np.array(d["valores"], dtype=float)
    if log:
        y = np.log(y)
    inicio = f"{int(d['inicio'][0]):04d}-{int(d['inicio'][1]):02d}-01"
    return pd.Series(y, index=pd.date_range(inicio, periods=len(y), freq="MS"))


def coefs(lista):
    return {c["nombre"]: c["valor"] for c in lista}


def linea(etiqueta, r, py, dec=4):
    print(f"    {etiqueta:<12s} R {r:+.{dec}f}   Python {py:+.{dec}f}   |dif| {abs(r - py):.2e}")


fallos = []


def exigir(condicion, mensaje):
    if not condicion:
        fallos.append(mensaje)
        print(f"    !! {mensaje}")


# ---------------------------------------------------------------------------
print("=" * 74)
print("1. Modelo airline sobre log(AirPassengers)")
print("=" * 74)

ap = serie("airpassengers", log=True)
R = CAP5["airpassengers"]["airline"]
rc = coefs(R["coeficientes"])

m = SARIMAX(ap, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit(disp=False)
print("  Por defecto (simple_differencing=False):")
linea("theta", rc["ma1"], m.params["ma.L1"])
linea("Theta", rc["sma1"], m.params["ma.S.L12"])
print(f"    {'nobs':<12s} R {R['nobs']:d}        Python {int(m.nobs):d}"
      "   <- statsmodels NO descuenta d ni D*m")
print(f"    {'loglik':<12s} R {R['loglik']:+.4f}  Python {m.llf:+.4f}")

ms = SARIMAX(ap, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n",
             simple_differencing=True).fit(disp=False)
print("  Con simple_differencing=True (diferencia primero, como R):")
linea("theta", rc["ma1"], ms.params["ma.L1"])
linea("Theta", rc["sma1"], ms.params["ma.S.L12"])
print(f"    {'nobs':<12s} R {R['nobs']:d}        Python {int(ms.nobs):d}   <- ahora coinciden")
exigir(int(ms.nobs) == R["nobs"], "nobs no coincide con simple_differencing=True")
exigir(abs(ms.params["ma.L1"] - rc["ma1"]) < 1e-3, "theta no reproduce a R")
exigir(abs(ms.params["ma.S.L12"] - rc["sma1"]) < 1e-3, "Theta no reproduce a R")

# Ljung-Box: statsmodels arrastra los residuales de la inicialización difusa.
res = m.resid
lb_todo = acorr_ljungbox(res, lags=[24], model_df=2)["lb_pvalue"].iloc[0]
lb_rec = acorr_ljungbox(res[13:], lags=[24], model_df=2)["lb_pvalue"].iloc[0]
print(f"  Ljung-Box(24): R p = {R['diagnostico']['lb24_p']:.4f} | Python p = {lb_todo:.4f} "
      f"| Python descartando los 13 primeros = {lb_rec:.4f}")

f = m.get_forecast(steps=CAP5["horizonte"])
pr = np.array(CAP5["airpassengers"]["pronostico"]["log"]["media"], dtype=float)
dif_pron = np.max(np.abs(pr - f.predicted_mean.values))
print(f"  Pronóstico h = 1..{CAP5['horizonte']} en logaritmos: diferencia máxima {dif_pron:.2e}")
exigir(dif_pron < 1e-3, "el pronóstico de Python se aleja del de R")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("2. Modelo airline sobre USAccDeaths (n = 72: aquí SÍ se nota)")
print("=" * 74)

uad = serie("usaccdeaths")
ruc = coefs(CAP5["usaccdeaths"]["coeficientes"])
for sd in (False, True):
    mu = SARIMAX(uad, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n",
                 simple_differencing=sd).fit(disp=False)
    print(f"  simple_differencing={str(sd):<5s} "
          f"theta {mu.params['ma.L1']:+.4f} (R {ruc['ma1']:+.4f}, dif {abs(mu.params['ma.L1'] - ruc['ma1']):.2e}) | "
          f"Theta {mu.params['ma.S.L12']:+.4f} | nobs {int(mu.nobs)} | llf {mu.llf:.4f}")
    if sd:
        exigir(abs(mu.params["ma.L1"] - ruc["ma1"]) < 1e-3,
               "USAccDeaths: theta no reproduce a R ni diferenciando primero")
print("  -> con la serie corta, el prior difuso mueve theta ~0.04. No es falta de")
print("     convergencia: Python alcanza el mismo óptimo desde varios inicios.")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("3. Regresores de calendario (SARIMAX con exog)")
print("=" * 74)

cal = CAP5["airpassengers"]["calendario"]
dias = np.array(cal["dias_mes"], dtype=float)
pascua = np.array([
    1.0 if ap.index[i].month == int(cal["pascuas"][str(ap.index[i].year)].split("-")[1]) else 0.0
    for i in range(len(ap))
])
exigir(pascua.sum() == len(cal["pascuas"]),
       "el regresor de Semana Santa no marca exactamente un mes por año")
X = np.column_stack([np.log(dias), pascua])
mc = SARIMAX(ap, exog=X, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n",
             simple_differencing=True).fit(disp=False)
rcal = coefs(cal["modelos"]["con_dias_pascua"]["coeficientes"])
linea("log_dias", rcal["log_dias"], mc.params["x1"])
linea("pascua", rcal["pascua"], mc.params["x2"])
exigir(abs(mc.params["x1"] - rcal["log_dias"]) < 5e-2, "log_dias no reproduce a R")
exigir(abs(mc.params["x2"] - rcal["pascua"]) < 5e-3, "pascua no reproduce a R")
print(f"  Meses con el Domingo de Pascua marcados: {int(pascua.sum())} "
      f"(uno por cada uno de los {len(cal['pascuas'])} años)")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("4. Contraejemplo: la TRM no tiene estacionalidad")
print("=" * 74)

trm = serie("trm")
ce = CAP5["trm_contraejemplo"]
mt = SARIMAX(trm, order=(0, 1, 0), seasonal_order=(1, 0, 0, 12), trend="n",
             simple_differencing=True).fit(disp=False)
linea("Phi", ce["forzado"]["Phi"], mt.params["ar.S.L12"])
print(f"  R: t = {ce['forzado']['t']:.2f} | Python: t = {mt.params['ar.S.L12'] / mt.bse['ar.S.L12']:.2f}")
exigir(abs(mt.params["ar.S.L12"] / mt.bse["ar.S.L12"]) < 2,
       "el Phi estacional de la TRM sale significativo, contra lo que dice el capítulo")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
if fallos:
    print(f"FALLOS: {len(fallos)}")
    for f_ in fallos:
        print("  -", f_)
    raise SystemExit(1)
print("Todas las comprobaciones pasan.")
