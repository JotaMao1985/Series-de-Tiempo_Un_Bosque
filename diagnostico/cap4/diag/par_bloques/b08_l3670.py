import numpy as np, statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

nilo = sm.datasets.nile.load_pandas().data["volume"].values
w = np.diff(nilo)
print(round(1.96 / np.sqrt(len(w)), 4))
#> 0.197

# statsmodels divide por n y, como R, pone el rezago 0 en la primera posicion
print(np.round(acf(w, nlags=6)[1:], 4))
#> [-0.402  -0.0443  0.0274 -0.0879  0.0005  0.0465]

# ojo: el metodo por defecto de pacf NO es Durbin-Levinson (es "ywadjusted");
# para reproducir R hay que pedir method="ldb" (Levinson-Durbin, sesgado)
print(np.round(pacf(w, nlags=6, method="ldb")[1:], 4))
#> [-0.402  -0.2456 -0.1187 -0.1733 -0.1554 -0.0737]

ma1 = ARIMA(nilo, order=(0, 1, 1), trend="n").fit()
print(round(ma1.params[0], 4))
#> -0.7334   (R: -0.7329)
# el primer residual es y_1 = 1120 (inicializacion difusa), no un error: se descarta
print(round(float(acorr_ljungbox(ma1.resid[1:], lags=[20], model_df=1)["lb_pvalue"].iloc[0]), 4))
#> 0.6984    (R: 0.6737; misma conclusion, no rechaza)