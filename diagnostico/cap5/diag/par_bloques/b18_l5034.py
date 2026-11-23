import numpy as np, pandas as pd, statsmodels.api as sm, warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
warnings.filterwarnings("ignore")

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))

# CUIDADO: simple_differencing=True reproduce la ESTIMACION de R, pero el
# modelo pasa a operar sobre la serie ya diferenciada y get_forecast() devuelve
# entonces el pronostico de nabla nabla_12 y_t, no el de y_t:
mal = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n",
              simple_differencing=True).fit(disp=False)
print(round(float(mal.get_forecast(steps=24).predicted_mean.iloc[-1]), 4))
#> 0.0     el pronostico de la serie diferenciada, no el nivel

# Para PRONOSTICAR se deja la opcion por defecto.
fit = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n").fit(disp=False)
f = fit.get_forecast(steps=24)
ci = f.conf_int(alpha=0.05)
print(np.round(np.exp([f.predicted_mean.iloc[-1], ci.iloc[-1,0], ci.iloc[-1,1]]), 2))
#> [525.46 400.62 689.21]
# R da 525.46, 399.66 y 690.85: el pronostico puntual coincide y el intervalo
# es un 1 % mas estrecho, porque sigma^2 sale 0.001348 en vez de 0.001371.

# Los satelites, con arma_acf: el polinomio MA lleva el termino cruzado
# th*TH en el rezago 13, y de ahi sale rho_11 = rho_13 = rho_1 * rho_12.
from statsmodels.tsa.arima_process import arma_acf
th, TH = -0.4018, -0.5569
ma = np.zeros(14); ma[0] = 1; ma[1] = th; ma[12] = TH; ma[13] = th * TH
r = arma_acf(np.r_[1.0], ma, lags=14)[1:]
print(np.round(r[[0, 10, 11, 12]], 4), round(float(r[0] * r[11]), 4))
#> [-0.3459  0.1471 -0.4251  0.1471] 0.1471
# rho_1 sale -0.3459 y en R -0.3460: es el redondeo de -0.34595.

# exp() del pronostico es la MEDIANA. Si se quiere la MEDIA:
sigma_h = (ci.iloc[-1,1] - f.predicted_mean.iloc[-1]) / 1.959964
print(round(float(np.exp(f.predicted_mean.iloc[-1] + sigma_h**2 / 2)), 2))
#> 530.52     un 1 % por encima de la mediana