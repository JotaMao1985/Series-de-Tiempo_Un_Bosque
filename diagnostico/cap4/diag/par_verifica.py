# Par académico cap. 4 · comprobaciones de las afirmaciones sobre statsmodels
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, statsmodels, statsmodels.api as sm
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
print("statsmodels", statsmodels.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values

print("\n== KPSS nlags='auto' (M3)")
r = kpss(nilo, regression="c", nlags="auto"); print("estadístico", round(r[0],4), "rezagos usados", r[2])

print("\n== Bloque M2: Ljung-Box con y sin el primer residual")
aj = ARIMA(nilo, order=(1,1,1), trend="n").fit()
print("resid[0] =", round(aj.resid[0],2), " y_1 =", nilo[0])
for nombre, e in (("con resid[0]", aj.resid), ("sin resid[0]", aj.resid[1:])):
    print(nombre, round(float(acorr_ljungbox(e, lags=[20], model_df=2)["lb_pvalue"].iloc[0]),4))
print("params", np.round(aj.params,4), " llf", round(aj.llf,3))

print("\n== M5: const de ARIMA(1,0,1) frente a la media muestral y a R")
f0 = ARIMA(nilo, order=(1,0,1), trend="c").fit()
print("const", repr(round(f0.params[0],6)), " media muestral", nilo.mean(), " llf", round(f0.llf,4))
# verosimilitud de statsmodels evaluada en los valores de R (920.7037, 0.8610, -0.5177) con su sigma2 óptima
mod = ARIMA(nilo, order=(1,0,1), trend="c")
best = -np.inf
for s2 in np.linspace(19000, 20500, 301):
    best = max(best, mod.loglike(np.array([920.7037, 0.8610, -0.5177, s2])))
print("llf de statsmodels en los coeficientes de R (sigma2 optimizada en rejilla):", round(best,4))
f0b = ARIMA(nilo, order=(1,0,1), trend="c").fit(start_params=[920.7037, 0.8610, -0.5177, 19800.0])
print("arrancando en los valores de R: const", round(f0b.params[0],4), " llf", round(f0b.llf,4))

print("\n== M7, bloque Python: de dónde sale la diferencia de AICc con R (1267.507)")
f = ARIMA(nilo, order=(1,1,1), trend="n").fit()
k = len(f.params)
print("nobs", f.nobs, " nobs_effective", f.nobs_effective, " llf", round(f.llf,4))
print("aicc a mano con nobs=100:", round(f.aic + 2*k*(k+1)/(f.nobs-k-1),4),
      " con nobs_effective=99:", round(f.aic + 2*k*(k+1)/(f.nobs_effective-k-1),4), " f.aicc:", round(f.aicc,4))
print("AIC statsmodels", round(f.aic,4), " (R: AIC = AICc - 24/95 =", round(1267.507 - 24/95,4), ")")

print("\n== M10 TRM: error estándar de la deriva, OPG frente a OIM")
trm = pd.read_csv("../../../Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")["trm"].values
fo = ARIMA(trm, order=(0,1,0), trend="t").fit()
fi = ARIMA(trm, order=(0,1,0), trend="t").fit(cov_type="oim")
print("OPG", np.round([fo.params[0], fo.bse[0]],2), " OIM", np.round([fi.params[0], fi.bse[0]],2))
d1 = np.diff(trm); print("media de las diferencias", round(d1.mean(),4), " sd/sqrt(n-1) (MLE)", round(np.sqrt(np.mean((d1-d1.mean())**2)/len(d1)),4))
