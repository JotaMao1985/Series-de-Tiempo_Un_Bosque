import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma2ma
import warnings; warnings.filterwarnings("ignore")

nilo = sm.datasets.nile.load_pandas().data["volume"].values
f = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
phi, th = f.params[0], f.params[1]
s = np.sqrt(f.params[-1])

# arma2ma pide los polinomios COMPLETOS y con el signo ya aplicado
psi = arma2ma(np.r_[1, -(1 + phi), phi], np.r_[1, th], lags=31)
sigma_h = s * np.sqrt(np.cumsum(psi**2))[:30]

ic = f.get_forecast(30).conf_int(alpha=0.05)
semiancho = (ic[:, 1] - ic[:, 0]) / 2
print(f"{np.max(np.abs(semiancho - 1.959964 * sigma_h)):.3e}")
#> 3.044e-06        la formula reproduce el intervalo tambien aqui

print(np.round([s, sigma_h[0], sigma_h[29], psi[30]], 3))
#> [140.599 140.599 196.925   0.168]
#   R da [142.045 142.045 199.363 0.169]. La diferencia viene sobre todo de
#   sigma^2: forecast::Arima la corrige por grados de libertad (SCR / (n* - k),
#   con n* = 99 y k = 2) y statsmodels da la de maxima verosimilitud, sin esa
#   correccion (19768 frente a 20177).
#   El peso limite psi (lo que decide como crece el intervalo) coincide hasta
#   el segundo decimal: 0.1679 frente a 0.1688.