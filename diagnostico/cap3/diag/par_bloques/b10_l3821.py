import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf

proceso = ArmaProcess(np.r_[1, -0.7], np.r_[1, 0.5])

# Pesos psi: aqui SI incluyen psi_0 = 1
psi = proceso.arma2ma(lags=9)
print(np.round(psi, 4))
# [1.     1.2    0.84   0.588  0.4116 0.2881 0.2017 0.1412 0.0988]

# Pesos pi: a diferencia de R, aqui no hay que intercambiar los polinomios,
# arma2ar ya aplica el convenio
pi_w = proceso.arma2ar(lags=9)
print(np.round(pi_w, 4))
# [ 1.     -1.2     0.6    -0.3     0.15   -0.075   0.0375 -0.0188  0.0094]

# ACF teorica a partir de los psi
psi0 = proceso.arma2ma(lags=2001)
g = np.array([np.dot(psi0[:2001 - k], psi0[k:2001]) for k in range(6)])
print(np.round((g / g[0])[1:], 4))
# [0.8308 0.5815 0.4071 0.285  0.1995]
print(np.round(arma_acf(np.r_[1, -0.7], np.r_[1, 0.5], lags=6)[1:], 4))
# [0.8308 0.5815 0.4071 0.285  0.1995]
