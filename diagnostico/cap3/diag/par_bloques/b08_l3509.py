import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf
from statsmodels.tsa.arima.model import ARIMA

# Dos MA(1) con la misma ACF
for theta in (0.5, 2.0):
    acf = arma_acf(np.r_[1], np.r_[1, theta], lags=4)[1:]
    proc = ArmaProcess(np.r_[1], np.r_[1, theta])
    print(f"theta={theta}: acf={np.round(acf, 4)}  invertible={proc.isinvertible}")
# theta=0.5: acf=[0.4 0.  0. ]  invertible=True
# theta=2.0: acf=[0.4 0.  0. ]  invertible=False

# MA(2): el triangulo, contra las raices
for th1, th2 in ((1.5, 0.6), (0.5, -0.6)):
    proc = ArmaProcess(np.r_[1], np.r_[1, th1, th2])
    print(f"theta=({th1}, {th2}): |raices|={np.round(np.abs(proc.maroots), 4)}  invertible={proc.isinvertible}")
# theta=(1.5, 0.6): |raices|=[1.291 1.291]  invertible=True
# theta=(0.5, -0.6): |raices|=[0.9399 1.7732]  invertible=False

# El maximo de |rho_1| de un MA(1)
th = np.arange(-3, 3, 0.01)
print(np.max(np.abs(th / (1 + th**2))))   # 0.5

# statsmodels tambien devuelve la version invertible, con sigma2 reescalado
y = ArmaProcess(np.r_[1], np.r_[1, 2.0]).generate_sample(   # theta = 2, sigma2 = 1
    nsample=1000, distrvs=np.random.default_rng(1).standard_normal)
res = ARIMA(y, order=(0, 0, 1)).fit()
print(np.round(res.maparams, 4), np.round(res.params[-1], 4))
# [0.5051] 3.8888     <- theta ~ 1/2 y sigma2 ~ 2^2 = 4: el mismo proceso
