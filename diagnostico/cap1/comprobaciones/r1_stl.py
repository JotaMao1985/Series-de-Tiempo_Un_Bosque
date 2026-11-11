# R1 · T1.2 · Bloque Python de STL del M7: que argumentos de statsmodels
# reproducen la figura y el bloque de R (estacionalidad periodica, sin robustez).
# Referencia: stl(log(AirPassengers), s.window = "periodic") de R.
import subprocess, inspect
import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import STL

def r(expr):
    out = subprocess.run(["Rscript", "-e", f"cat({expr})"], capture_output=True, text=True, check=True).stdout.split()
    return np.array([float(v) for v in out])

ap = r("as.numeric(AirPassengers)")
pasajeros = pd.Series(ap, index=pd.date_range("1949-01-01", periods=len(ap), freq="MS"), name="pasajeros")
Rs = r("stl(log(AirPassengers), s.window='periodic')$time.series[, 'seasonal']")
Rt = r("stl(log(AirPassengers), s.window='periodic')$time.series[, 'trend']")
print("R: julio estacional =", round(Rs[6], 4), " tendencia jul-1955 =", round(Rt[78], 4))
print("firma de STL:", inspect.signature(STL.__init__))
print("firma de fit:", inspect.signature(STL.fit))

def informe(nombre, res):
    s = res.seasonal.values; t = res.trend.values
    jul = s[6::12]
    print(f"{nombre}\n   julio estacional: 1949 {jul[0]:.4f}  1955 {jul[6]:.4f}  1960 {jul[-1]:.4f}"
          f"  recorrido {jul.max()-jul.min():.6f} | exp(jul-1955) {np.exp(jul[6]):.4f}"
          f" | tendencia jul-1955 {t[78]:.4f}\n   max|S - S_R| {np.abs(s-Rs).max():.2e}  max|T - T_R| {np.abs(t-Rt).max():.2e}"
          f"  NaN en tendencia {int(np.isnan(t).sum())}")

y = np.log(pasajeros)
informe("ANTES (publicado): STL(y, period=12, robust=True).fit()", STL(y, period=12, robust=True).fit())
informe("por defecto: STL(y, period=12).fit()", STL(y, period=12).fit())
n = len(y)
informe("A: STL(y, period=12, seasonal=10*n+1, seasonal_deg=0, trend=19).fit()",
        STL(y, period=12, seasonal=10*n+1, seasonal_deg=0, trend=19).fit())
informe("B: A + .fit(inner_iter=2, outer_iter=0)",
        STL(y, period=12, seasonal=10*n+1, seasonal_deg=0, trend=19).fit(inner_iter=2, outer_iter=0))
informe("C: B + saltos de R (seasonal_jump=145, trend_jump=2, low_pass_jump=2)",
        STL(y, period=12, seasonal=10*n+1, seasonal_deg=0, trend=19,
            seasonal_jump=145, trend_jump=2, low_pass_jump=2).fit(inner_iter=2, outer_iter=0))
informe("D: seasonal=1441 sin seasonal_deg=0 (queda en 1)",
        STL(y, period=12, seasonal=10*n+1, trend=19).fit(inner_iter=2, outer_iter=0))
informe("E: sin trend=19 (statsmodels lo calcula)",
        STL(y, period=12, seasonal=10*n+1, seasonal_deg=0).fit(inner_iter=2, outer_iter=0))
e = STL(y, period=12, seasonal=10*n+1, seasonal_deg=0)
print("   ventana de tendencia que calcula statsmodels en E:", e.config["trend"], " low_pass:", e.config["low_pass"])
