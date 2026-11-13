#!/usr/bin/env python3
"""R3 · T3.1 · El bloque Python del Módulo 3 (las líneas nuevas: subseries y rezagos) corre.

`pasajeros` se construye como en el bloque del Módulo 2, pero con la serie de R exportada a
mano (sin red): los 144 valores de DATOS_CAP1.observado del propio capítulo.
Uso (desde la raíz del repo): python3 diagnostico/cap1/comprobaciones/r3a_m3_python.py
"""
import json, re, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

html = pathlib.Path("Htmls_Series/capitulo-1-componentes-descomposicion.html").read_text(encoding="utf-8")
linea = next(l for l in html.splitlines() if "const DATOS_CAP1 = " in l)
datos = json.loads(linea[linea.index("{"):linea.rindex("}") + 1])
pasajeros = pd.Series(
    [float(v) for v in datos["observado"]],
    index=pd.date_range("1949-01-01", periods=144, freq="MS"),
    name="pasajeros",
)

# --- líneas del bloque del capítulo -------------------------------------------------
# Grafico de subseries: un panel por mes, con la media de cada mes
from statsmodels.graphics.tsaplots import month_plot
month_plot(pasajeros, ylabel="Miles de pasajeros")

# Grafico de rezagos: cada valor contra el de 12 meses antes
plt.figure()
pd.plotting.lag_plot(pasajeros, lag=12)
# -------------------------------------------------------------------------------------

fig_sub, fig_lag = [plt.figure(n) for n in plt.get_fignums()][:2]
ax = fig_sub.axes[0]
print("month_plot: figuras abiertas =", len(plt.get_fignums()), "; líneas en el eje =", len(ax.lines),
      "; rótulos del eje x =", [t.get_text() for t in ax.get_xticklabels()])
# month_plot dibuja la media de cada mes con hlines (una LineCollection por mes)
medias = sorted(round(float(seg[0][1]), 1) for col in ax.collections for seg in col.get_segments())
print("month_plot: medias dibujadas =", medias)
print("medias por mes (pandas)     =", sorted(round(float(v), 1) for v in pasajeros.groupby(pasajeros.index.month).mean()))
ax2 = fig_lag.axes[0]
pts = ax2.collections[0].get_offsets()
print("lag_plot(lag=12): puntos =", len(pts), "; eje x =", ax2.get_xlabel(), "; eje y =", ax2.get_ylabel())
print("correlación de esos puntos =", round(float(pd.Series(pts[:, 0]).corr(pd.Series(pts[:, 1]))), 4))
