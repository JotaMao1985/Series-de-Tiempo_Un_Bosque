# Lector B · c4-m4-21 y c4-m3-29: inicialización de ARIMA(0,1,1) en statsmodels y kpss con 4 rezagos
import warnings, inspect
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import kpss
warnings.simplefilter("ignore")
nilo = sm.datasets.nile.load_pandas().data["volume"].values
m = ARIMA(nilo, order=(0, 1, 1), trend="n")
f = m.fit()
print("loglikelihood_burn:", f.loglikelihood_burn, " nobs:", f.nobs)
init = m.ssm.initialization
print("tipo de inicialización del modelo de estado:", getattr(init, "initialization_type", None))
print("primeros residuales:", np.round(f.resid[:3], 2), " y_1 =", nilo[0])
print("varianza de la inicialización difusa (primer elemento de P0):", getattr(m.ssm, "initial_variance", None))
print("kpss nlags=4 :", repr(kpss(nilo, regression="c", nlags=4)[0]))
print("kpss auto    :", kpss(nilo, regression="c", nlags="auto")[0:3:2])
doc = ARIMA.__doc__ or ""
i = doc.lower().find("diffuse")
print("docstring de ARIMA menciona 'diffuse':", i >= 0, "|", " ".join(doc[max(0, i-200):i+250].split()) if i >= 0 else "")
