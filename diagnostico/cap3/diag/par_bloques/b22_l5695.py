import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima_process import arma2ma
from scipy import stats

## ---- Caso 1: manchas solares en raiz cuadrada -------------------------
datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values

print(manchas.min(), (manchas == 0).sum())   # 0.0  1   -> log imposible

ar2s = ARIMA(np.sqrt(manchas), order=(2, 0, 0), trend="c").fit()
print(np.round(ar2s.arparams, 4))            # [ 1.4027 -0.6853]

lb = acorr_ljungbox(ar2s.resid, lags=[12], model_df=2)
print(round(float(lb["lb_pvalue"].iloc[0]), 4))   # 0.1780
# R daba 0.1644, por la inicializacion de residuales del Modulo 8.
# Descartando los 2 primeros, los dos programas dan 0.1682.

phi = ar2s.arparams
raices = np.roots(np.r_[1, -phi][::-1])
print(round(2 * np.pi / np.angle(raices[0]), 4))  # 11.2178

print(np.round(ar2s.polynomial_ar, 4))       # [ 1.     -1.4027  0.6853]
print(round(abs(raices[0]), 4), round(float(np.angle(raices[0])), 4))
# 1.208 0.5601        modulo y angulo: estacionariedad y pseudo-periodo

# arma2ma es la misma recursion del Modulo 4, pero pide los coeficientes
# del POLINOMIO: el AR va negado, igual que en ArmaProcess (Modulo 1).
psi = arma2ma(np.r_[1, -phi], np.r_[1], lags=12)
print(np.round(psi, 4))
# [ 1.      1.4027  1.2822  0.8372  0.2957 -0.159  -0.4256 -0.4881 -0.3929
#  -0.2167 -0.0346  0.0999]
# El septimo peso sale -0.4256 y en R -0.4257: los dos optimizadores no dan
# exactamente el mismo phi. Es diferencia de estimacion, no de formula.

s2 = ar2s.params[-1]                  # ['const', 'ar.L1', 'ar.L2', 'sigma2']
ee = np.sqrt(s2 * np.cumsum(psi**2))
print(np.round(1.959964 * ee[:6], 4))
# [2.2697 3.9098 4.8739 5.2312 5.2741 5.2864]
ci = np.asarray(ar2s.get_forecast(6).conf_int(alpha=0.05))
print(np.round((ci[:, 1] - ci[:, 0]) / 2, 4))
# [2.2697 3.9098 4.8739 5.2312 5.2741 5.2864]   <- lo mismo

## ---- Caso 2: log-retornos de la TRM -----------------------------------
url = ("https://www.datos.gov.co/resource/32sa-8pi3.json"
       "?$select=vigenciadesde,valor&$limit=50000")
crudo = pd.read_json(url)
crudo["fecha"] = pd.to_datetime(crudo["vigenciadesde"]).dt.tz_localize(None)
crudo = crudo[crudo["fecha"] >= "2015-01-01"].sort_values("fecha")
trm = (crudo.set_index("fecha")["valor"].resample("MS").mean()
            .loc[:"2026-06-01"])

ret = 100 * np.diff(np.log(trm.values))
print(len(ret), round(1.96 / np.sqrt(len(ret)), 4))    # 137 0.1675
print(np.round(acf(ret, nlags=6, fft=False)[1:], 3))
# [ 0.105 -0.077 -0.078  0.006  0.193  0.123]

print(np.round(acorr_ljungbox(ret, lags=[6, 12, 20])["lb_pvalue"].values, 4))
# [0.0931 0.0601 0.0599]

ma1 = ARIMA(ret, order=(0, 0, 1), trend="n").fit()
rb  = ARIMA(ret, order=(0, 0, 0), trend="n").fit()
print(round(ma1.aicc, 4), round(rb.aicc, 4))   # practicamente iguales

print(round(float(acorr_ljungbox(ret**2, lags=[12])["lb_pvalue"].iloc[0]), 4))
# 0.9166