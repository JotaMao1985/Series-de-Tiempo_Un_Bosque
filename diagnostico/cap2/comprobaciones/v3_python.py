# Verificador independiente R3 cap. 2: las cifras nuevas de Python, una por una.
import numpy as np, pandas as pd, statsmodels, statsmodels.api as sm
from statsmodels.tsa.stattools import acf, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
print("statsmodels", statsmodels.__version__)
d = sm.datasets.get_rdataset("AirPassengers").data
p = pd.Series(d["value"].values, index=pd.date_range("1949-01-01", periods=len(d), freq="MS"))
res = seasonal_decompose(p, model="multiplicative", period=12).resid.dropna()
rr = acf(res, nlags=24, adjusted=False)[1:]
print("M3 residuo:", len(res), np.round(rr[[0, 11]], 3), int(np.sum(np.abs(rr) > 1.96/np.sqrt(len(res)))))
w = np.log(p).diff(12).dropna()
nl = int(np.floor(3*np.sqrt(len(w))/13))
est, pv, *_ = kpss(w, regression="c", nlags=nl)
d_ = 1 if pv < 0.05 else 0
if d_: w = w.diff().dropna()
est, pv, *_ = kpss(w, regression="c", nlags=int(np.floor(3*np.sqrt(len(w))/13)))
r = acf(w, nlags=24, adjusted=False)[1:]
print("M9:", d_, round(float(pv), 3), len(w), np.round(r[[0, 11]], 3), int(np.sum(np.abs(r) > 1.96/np.sqrt(len(w)))))
