import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf
from statsmodels.tsa.arima.model import ARIMA

# Redundancia exacta: phi = -theta colapsa a ruido blanco
print(np.round(arma_acf(np.r_[1, -0.5], np.r_[1, -0.5], lags=6)[1:], 6))
# [0. 0. 0. 0. 0.]

# Redundancia CASI exacta: phi = 0.5, theta = -0.45
print(np.round(arma_acf(np.r_[1, -0.5], np.r_[1, -0.45], lags=6)[1:], 4))
# [0.0515 0.0257 0.0129 0.0064 0.0032]

# Simular ese proceso y ajustarle un ARMA(1,1): los coeficientes se van
# lejos de los verdaderos, con errores estandar grandes, pero su SUMA
# reproduce la cancelacion. La semilla no coincide con la de R, asi que
# las cifras exactas difieren; el sintoma es el mismo.
proceso = ArmaProcess(np.r_[1, -0.5], np.r_[1, -0.45])
y = proceso.generate_sample(nsample=200, distrvs=np.random.default_rng(11).standard_normal)
res = ARIMA(y, order=(1, 0, 1)).fit()
print(res.summary().tables[1])
#   ar.L1  -0.0798   std err 1.534
#   ma.L1   0.1254   std err 1.531
print("suma ar1 + ma1 =", round(res.arparams[0] + res.maparams[0], 4))
# suma ar1 + ma1 = 0.0457

# R estimo (0.83, -0.80) y Python (-0.08, 0.13): dos parejas muy distintas
# con casi la misma suma. Es la verosimilitud plana de la que habla el aviso.
