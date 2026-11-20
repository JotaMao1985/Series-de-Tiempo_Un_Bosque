import numpy as np, pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import ArmaProcess

x = pd.read_csv("serie.csv")["x"].to_numpy()          # LA MISMA serie de R
fit = ARIMA(x, order=(1, 0, 1), trend="n").fit()

print(fit.param_names, fit.params.round(4))
# ['ar.L1', 'ma.L1', 'sigma2'] [0.5999 0.6925 0.9992]
# Identico a R hasta el cuarto decimal, y con el mismo signo positivo.

print(fit.polynomial_ar)     # [ 1.  -0.5999]  ->  phi(B)   = 1 - 0.5999 B
print(fit.polynomial_ma)     # [ 1.   0.6925]  ->  theta(B) = 1 + 0.6925 B

# PERO al SIMULAR, statsmodels no pide los coeficientes del modelo sino
# los del POLINOMIO. Como phi(B) = 1 - phi1*B, el AR va NEGADO:
bien = ArmaProcess(ar=np.array([1, -0.6]), ma=np.array([1, 0.7]))
mal  = ArmaProcess(ar=np.array([1,  0.6]), ma=np.array([1, 0.7]))

print(bien.arcoefs, np.round(bien.acf(5)[1:], 4))
# [0.6]  [0.7923 0.4754 0.2852 0.1711]    <- lo que se queria
print(mal.arcoefs,  np.round(mal.acf(5)[1:], 4))
# [-0.6] [ 0.0892 -0.0535  0.0321 -0.0193]  <- otro modelo, sin avisar