"""Verificador B · R4 cap. 4: las cifras de M8-M10 que el capítulo también da en Python.

python3 diagnostico/cap4/comprobaciones/v4B_software.py > diagnostico/cap4/comprobaciones/v4B_software_py.out
"""
import pathlib
import warnings

import numpy as np
import pandas as pd
import statsmodels
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import statsmodels.api as sm

warnings.filterwarnings("ignore")
RAIZ = pathlib.Path(__file__).resolve().parents[3]
print("statsmodels", statsmodels.__version__)

trm = pd.read_csv(RAIZ / "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")["trm"].values
d1 = np.diff(trm)
print(f"TRM n={len(trm)} · curtosis simple {stats.kurtosis(d1, fisher=False):.2f}"
      f" · exceso {stats.kurtosis(d1):.2f} · asimetría {stats.skew(d1):.3f}")
d12 = trm[12:] - trm[:-12]
print(f"curtosis a 12 meses {stats.kurtosis(d12, fisher=False):.2f}")
s = np.sqrt(np.mean(d1 ** 2))  # sigma^2 ML de la caminata sin deriva
print(f"sigma ML {s:.2f} · fuera 95 % {np.sum(np.abs(d1) > 1.959964 * s)} · arriba {np.sum(d1 > 1.959964 * s)}")
print(f"Shapiro p {stats.shapiro(d1).pvalue:.5f}")

nilo = sm.datasets.get_rdataset("Nile").data["value"].values if False else None
# Nilo desde R no está en statsmodels sin red: se lee de los precálculos del capítulo
import json
datos = json.loads((RAIZ / "precalculo/salidas/cap4_arima.json").read_text("utf-8"))
nilo = None
for clave in ("serie", "valores", "datos"):
    if isinstance(datos.get("nilo"), dict) and clave in datos["nilo"]:
        nilo = np.array(datos["nilo"][clave], dtype=float)
if nilo is None:
    txt = (RAIZ / "precalculo/salidas/cap4_datos.js").read_text("utf-8")
    i = txt.index('"valores":[') + len('"valores":[')
    nilo = np.array([float(v) for v in txt[i:txt.index("]", i)].split(",")])
anios = np.arange(1871, 1971)
print(f"Nilo n={len(nilo)} · media antes de 1899 {nilo[anios < 1899].mean():.2f} · desde {nilo[anios >= 1899].mean():.2f}")
esc = (anios >= 1899).astype(float).reshape(-1, 1)
fe = ARIMA(nilo, order=(0, 0, 0), exog=esc, trend="c").fit()
print(f"escalón statsmodels: beta {fe.params[1]:.2f} e.e. {fe.bse[1]:.2f}"
      f" · LB(20) p {acorr_ljungbox(fe.resid, lags=[20])['lb_pvalue'].iloc[0]:.3f}")
f111 = ARIMA(nilo, order=(1, 1, 1)).fit()
print(f"ARIMA(1,1,1) statsmodels: phi {f111.params[0]:.4f} theta {f111.params[1]:.4f}")

# --- Comentarios del bloque Python de la TRM que cambió la ronda ---------------
y = trm
r00 = ARIMA(y, order=(0, 1, 0)).fit()
f212 = ARIMA(y, order=(2, 1, 2)).fit()
print(f"(2,1,2) arranque por defecto: AICc {f212.aicc:.2f} · |raíces MA| {np.round(np.abs(f212.maroots), 3)}"
      f" · (0,1,0) AICc {r00.aicc:.2f} · diferencia {f212.aicc - r00.aicc:.2f}")
arr = [0.6612, -0.9917, -0.6226, 0.99996, 121.48 ** 2]
f212r = ARIMA(y, order=(2, 1, 2)).fit(start_params=arr)
print(f"(2,1,2) arranque en R: AICc {f212r.aicc:.2f} · |raíces MA| {np.round(np.abs(f212r.maroots), 6)}"
      f" · |raíces AR| {np.round(np.abs(f212r.arroots), 4)}")
for cov in ("opg", "oim"):
    fd = ARIMA(y, order=(0, 1, 0), trend="t").fit(cov_type=cov)
    print(f"deriva {fd.params[0]:.2f} e.e. ({cov}) {fd.bse[0]:.2f}")
