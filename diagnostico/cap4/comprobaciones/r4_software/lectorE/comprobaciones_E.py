# Lector E · comprobaciones de los comentarios del bloque Python de la TRM (c4-m10-41, -42, -44)
# python3 -I comprobaciones_E.py   (desde Htmls_Series/datos: lee la copia fija, no descarga nada)
import inspect, warnings
import numpy as np, pandas as pd
import statsmodels
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
y = pd.read_csv("trm_mensual_2015-01_2026-06.csv")["trm"].values

print("\n== c4-m10-41: ¿de dónde sale el p del ADF de statsmodels? ==")
src = inspect.getsource(adfuller)
print("adfuller llama a mackinnonp:", "mackinnonp" in src, "| importa adfvalues:", "adfvalues" in src)

print("\n== c4-m10-42: por defecto, ¿ARIMA impone estacionariedad e invertibilidad? ==")
sig = inspect.signature(ARIMA.__init__)
print({k: sig.parameters[k].default for k in ("enforce_stationarity", "enforce_invertibility", "trend")
       if k in sig.parameters})
f = ARIMA(y, order=(2, 1, 2)).fit()
n = f.nobs_effective; k = len(f.params)
print("params:", np.round(f.params, 4), "| AICc:", round(f.aicc, 2), "| |raíces MA|:", np.round(np.abs(f.maroots), 3),
      "| |raíces AR|:", np.round(np.abs(f.arroots), 3))
# ¿se puede llegar a la solución de R (ar 0.6612 -0.9917, ma -0.6226 0.99996) con statsmodels si no se impone nada?
r_ar = [0.6612, -0.9917]; r_ma = [-0.6226, 0.9999632]
mod_libre = ARIMA(y, order=(2, 1, 2), enforce_stationarity=False, enforce_invertibility=False)
sp = np.r_[r_ar, r_ma, 14756.38]                      # ar1 ar2 ma1 ma2 sigma2 (sin constante, d = 1)
g = mod_libre.fit(start_params=sp)
print("sin imponer, desde los parámetros de R -> AICc:", round(g.aicc, 2), "| params:", np.round(g.params, 4),
      "| |raíces MA|:", np.round(np.abs(g.maroots), 5), "| |raíces AR|:", np.round(np.abs(g.arroots), 4))
print("loglik en los parámetros de R (smooth):", round(float(mod_libre.loglike(sp)), 2),
      "| loglik del ajuste con restricciones:", round(f.llf, 2), "| del libre:", round(g.llf, 2))
# ¿llega la versión restringida a una raíz sobre el círculo si se le da buen arranque?
h = ARIMA(y, order=(2, 1, 2)).fit(start_params=sp)
print("con restricciones y arranque de R -> AICc:", round(h.aicc, 2), "| |raíces MA|:", np.round(np.abs(h.maroots), 5))
r010 = ARIMA(y, order=(0, 1, 0)).fit()
print("AICc (0,1,0):", round(r010.aicc, 2), "| (2,1,2) restringido menos (0,1,0):", round(f.aicc - r010.aicc, 2))

print("\n== c4-m10-44: covarianza por defecto y errores estándar de la deriva ==")
fd_opg = ARIMA(y, order=(0, 1, 0), trend="t").fit()
fd_oim = ARIMA(y, order=(0, 1, 0), trend="t").fit(cov_type="oim")
print("cov_type por defecto:", fd_opg.cov_type, "| e.e. OPG:", round(fd_opg.bse[0], 2), "| e.e. oim:", round(fd_oim.bse[0], 2))
# Gaussianos frente a colas pesadas: ¿coinciden OPG y la información observada?
rng = np.random.default_rng(20948)
def cociente(gen, reps=200, n=138):
    r = []
    for _ in range(reps):
        e = gen(n); x = np.cumsum(8 + e)
        m = ARIMA(x, order=(0, 1, 0), trend="t")
        a = m.fit(); b = m.fit(cov_type="oim")
        r.append(a.bse[0] / b.bse[0])
    return np.mean(r), np.std(r)
print("OPG/oim, errores normales (media, sd en 200 réplicas):", np.round(cociente(lambda n: rng.normal(0, 120, n)), 3))
print("OPG/oim, errores t3 escalados:", np.round(cociente(lambda n: 120 * rng.standard_t(3, n) / np.sqrt(3)), 3))
print("OPG/oim observado en la TRM:", round(fd_opg.bse[0] / fd_oim.bse[0], 3))
