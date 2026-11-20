# Par academico, cap. 3: comprobaciones en Python de afirmaciones de la prosa
import warnings; warnings.filterwarnings("ignore")
import numpy as np, statsmodels, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_process import ArmaProcess
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
datos = sm.datasets.sunspots.load_pandas().data
m = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values

print("\n== M7: CSS de un AR(2) = MCO condicional: AutoReg da el CSS de R (1.4032, -0.7099)?")
ar = AutoReg(m, lags=2, trend="c").fit()
print("AutoReg params:", np.round(ar.params, 4), " sigma2:", round(ar.sigma2, 2))

print("\n== M7: fit(method='css') en la API nueva")
try:
    ARIMA(m, order=(2, 0, 0), trend="c").fit(method="css")
except Exception as e:
    print(type(e).__name__, ":", str(e)[:200])

print("\n== M8: primeros residuales de statsmodels (crudos) para el AR(2) de la serie cruda")
r = ARIMA(m, order=(2, 0, 0), trend="c").fit()
print(np.round(r.resid[:4], 3))
print("residuales estandarizados del filtro (forecasts_error_cov):",
      np.round(r.resid[:2] / np.sqrt(r.filter_results.forecasts_error_cov[0, 0, :2] / r.params[-1]), 3))

print("\n== M9: AR(2) sobre la raiz: LB recortado en Python")
s = ARIMA(np.sqrt(m), order=(2, 0, 0), trend="c").fit()
print("LB12 completo:", round(float(acorr_ljungbox(s.resid, lags=[12], model_df=2)["lb_pvalue"].iloc[0]), 4),
      " recortado:", round(float(acorr_ljungbox(s.resid[2:], lags=[12], model_df=2)["lb_pvalue"].iloc[0]), 4))
ph = s.arparams; raiz = np.roots(np.r_[1, -ph][::-1])
print("periodo:", 2 * np.pi / np.angle(raiz[0]), " t:", np.round(s.params[1:3] / s.bse[1:3], 2))

print("\n== M1: polynomial_ar impreso")
print(ArmaProcess(np.r_[1, -0.6], np.r_[1, 0.7]).arcoefs)
