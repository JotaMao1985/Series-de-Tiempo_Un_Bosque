import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings; warnings.filterwarnings("ignore")

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
print(len(ap))
#> 144

# El ARIMA(0,1,5) que elige auto.arima en R. statsmodels no trae auto.arima, ni
# por tanto la busqueda amplia (p, q <= 8): aqui se ajusta el orden que R eligio
f = ARIMA(ap, order=(0, 1, 5), trend="n").fit()
e = f.resid[1:]                       # el primer residual es el dato: se descarta
r = acf(e, nlags=24, fft=False)
print(np.round([r[12], r[24], 1.96 / np.sqrt(len(e))], 4).tolist())
#> [0.7218, 0.6676, 0.1639]
#   R da 0.7245, 0.6727 y 0.1633: coeficientes casi iguales, residuales algo distintos
lb = acorr_ljungbox(e, lags=[24], model_df=5)
print(round(float(lb["lb_stat"].iloc[0]), 1), float(lb["lb_pvalue"].iloc[0]) < 1e-6)
#> 219.3 True
#   R da Q = 222.4: la misma lectura, rechaza

# El modelo estacional "airline", solo como avance
air = ARIMA(ap, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit()
e2 = air.resid[13:]                   # los 13 primeros residuales son del arranque (1 + 12)
r2 = acf(e2, nlags=24, fft=False)
lb2 = acorr_ljungbox(e2, lags=[24], model_df=2)
print(round(r2[12], 4), round(float(lb2["lb_pvalue"].iloc[0]), 4))
#> -0.0525 0.3676
#   R da -0.0515 y 0.2330: el mismo veredicto, no rechaza

# Los AICc no se comparan: sus verosimilitudes usan distinto numero de datos
print(f.nobs_effective, air.nobs_effective)
#> 143 131