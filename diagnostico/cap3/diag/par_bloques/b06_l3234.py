import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf, arma_pacf

phi = np.array([0.5, 0.3])
ar = np.r_[1, -phi]      # convenio de statsmodels: 1 - phi1 B - phi2 B^2
ma = np.r_[1]

print(np.round(arma_acf(ar, ma, lags=6)[1:], 4))
# [0.7143 0.6571 0.5429 0.4686 0.3971]

print(np.round(arma_pacf(ar, ma, lags=6)[1:], 4))
# [ 0.7143  0.3    -0.      0.     -0.    ]
#   los "-0." son ceros con signo negativo del punto flotante: la PACF
#   se corta igual de exactamente que en R

# Varianza del proceso: ecuacion de Yule-Walker con k = 0
sigma2 = 1.0
rho = arma_acf(ar, ma, lags=3)[1:]
print(round(sigma2 / (1 - phi @ rho), 4))          # 2.2436

# La misma, por la formula cerrada del AR(2)
print(round(sigma2 * (1 - phi[1]) /
            ((1 + phi[1]) * ((1 - phi[1])**2 - phi[0]**2)), 4))   # 2.2436

proceso = ArmaProcess(ar, ma)
print(proceso.isstationary)   # True