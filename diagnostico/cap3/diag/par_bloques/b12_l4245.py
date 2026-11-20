import numpy as np
from statsmodels.tsa.arima_process import arma_acf

# ACF de un ARMA(1,1): rho_1 por la formula y despues rho_k = phi * rho_{k-1}
phi, theta = 0.7, 0.5
rho1 = (1 + phi * theta) * (phi + theta) / (1 + 2 * phi * theta + theta**2)
print(np.round(rho1 * phi ** np.arange(5), 4))
# [0.8308 0.5815 0.4071 0.285  0.1995]
print(np.round(arma_acf(np.r_[1, -phi], np.r_[1, theta], lags=6)[1:], 4))
# [0.8308 0.5815 0.4071 0.285  0.1995]    <- coinciden

# Un AR(1) con el mismo phi decae al mismo ritmo, desde otro arranque
print(np.round(arma_acf(np.r_[1, -phi], np.r_[1], lags=6)[1:], 4))
# [0.7    0.49   0.343  0.2401 0.1681]

# Para k > q la recursion del AR vale en cualquier ARMA: un ARMA(2,1)
r = arma_acf(np.r_[1, -0.5, -0.3], np.r_[1, 0.4], lags=6)
print(np.round(r[2:6], 4))                        # rho_2 a rho_5
# [0.7307 0.6238 0.5311 0.4527]
print(np.round(0.5 * r[1:5] + 0.3 * r[0:4], 4))   # phi1 rho_{k-1} + phi2 rho_{k-2}
# [0.7307 0.6238 0.5311 0.4527]

# ...pero NO para k = q: aqui q = 1 y la recursion se equivoca
print(round(0.5 * r[0] + 0.3 * r[0], 4), "frente a", round(r[1], 4))
# 0.8 frente a 0.8614

# VARIANZA del proceso: gamma_k = s2 * sum(psi_j * psi_{j+k})
from statsmodels.tsa.arima_process import arma2ma
sigma2 = 1.0
psi = arma2ma(np.r_[1, -0.7], np.r_[1, 0.5], lags=4001)
print(round(sigma2 * (psi**2).sum(), 4))          # gamma_0 -> 3.8235

# La misma, por la formula cerrada del ARMA(1,1)
phi, theta = 0.7, 0.5
print(round(sigma2 * (1 + 2*phi*theta + theta**2) / (1 - phi**2), 4))
# 3.8235

# Y gamma_1 / gamma_0 devuelve la rho_1 de la formula de arriba
g1 = sigma2 * (psi[:-1] * psi[1:]).sum()
print(round(g1, 4), round(g1 / (sigma2 * (psi**2).sum()), 4))
# 3.1765 0.8308
