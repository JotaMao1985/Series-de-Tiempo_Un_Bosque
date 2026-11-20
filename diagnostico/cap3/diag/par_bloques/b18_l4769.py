import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.regression.linear_model import yule_walker

datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values
print(len(manchas))   # 100

# 1. Yule-Walker. OJO: statsmodels usa por defecto el divisor n-k ("adjusted");
#    para reproducir ar() de R hay que pedir method="mle", que usa el divisor n.
rho, sigma = yule_walker(manchas - manchas.mean(), order=2, method="mle")
print(np.round(rho, 4))     # [ 1.3173 -0.6338]

# 2. CSS: la API nueva de ARIMA NO lo ofrece. Sus method= son statespace,
#    innovations_mle, hannan_rissanen, burg, innovations y yule_walker;
#    fit(method="css") lanza ValueError: "css" is not a valid estimator.
#    El antiguo tsa.arima_model.ARMA, que si tenia method="css", fue
#    retirado en statsmodels 0.13. El CSS de R (1.4032, -0.7099) no tiene
#    equivalente directo aqui.

# 3. Maxima verosimilitud. statespace (el defecto) e innovations_mle son
#    AMBOS verosimilitud exacta y dan el mismo punto:
ml  = ARIMA(manchas, order=(2, 0, 0), trend="c").fit()
mle = ARIMA(manchas, order=(2, 0, 0), trend="c").fit(method="innovations_mle")
print(np.round(ml.arparams, 4))    # [ 1.4059 -0.7111]
print(np.round(mle.arparams, 4))   # [ 1.4059 -0.7111]  identico

# Raices y pseudo-periodo
phi = ml.arparams
raices = np.roots(np.r_[1, -phi][::-1])
print(np.round(np.abs(raices), 4))                 # [1.1859 1.1859]
print(round(2 * np.pi / np.angle(raices[0]), 4))   # 10.7365
# R daba 10.7369: los optimizadores convergen a puntos ligerisimamente
# distintos. La diferencia es de 4 diezmilesimas de anio, irrelevante aqui.