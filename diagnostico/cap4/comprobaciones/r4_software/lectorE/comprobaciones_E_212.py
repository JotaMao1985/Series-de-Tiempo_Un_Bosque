# ¿Qué (2,1,2) encuentra statsmodels? (c4-m10-42). Desde Htmls_Series/datos.
import warnings, numpy as np, pandas as pd
from statsmodels.tsa.arima.model import ARIMA
warnings.filterwarnings("ignore")
y = pd.read_csv("trm_mensual_2015-01_2026-06.csv")["trm"].values
def resumen(nombre, r):
    print(f"{nombre:48s} llf={r.llf:9.2f} AICc={r.aicc:8.2f} params={np.round(r.params[:4],4)} sigma2={r.params[4]:.0f} "
          f"|MA|={np.round(np.abs(r.maroots),5)} |AR|={np.round(np.abs(r.arroots),4)}")
m = ARIMA(y, order=(2, 1, 2))
resumen("restringido, arranque por defecto", m.fit())
sp = np.r_[[0.6612, -0.9917, -0.6226, 0.9999632], 14756.38]
resumen("restringido, arranque de R", m.fit(start_params=sp))
mlibre = ARIMA(y, order=(2, 1, 2), enforce_stationarity=False, enforce_invertibility=False)
resumen("sin imponer, arranque de R", mlibre.fit(start_params=sp))
print("loglike en los params de R:  restringido", round(float(m.loglike(sp)), 2), " libre", round(float(mlibre.loglike(sp)), 2))
g = mlibre.fit(start_params=sp)
print("loglike del 'libre' evaluado con el modelo restringido:", round(float(m.loglike(g.params)), 2))
print("nobs_effective:", m.fit().nobs_effective, " nobs:", m.fit().nobs)
