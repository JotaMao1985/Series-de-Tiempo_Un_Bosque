import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))

# seasonal_order = (P, D, Q, m). trend="n" para que no anada constante.
fit = SARIMAX(s, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12),
              trend="n", simple_differencing=True).fit(disp=False)
print(fit.params.round(4))
#> ma.L1      -0.4018
#> ma.S.L12   -0.5569
#> sigma2      0.0013

th, Th = fit.params["ma.L1"], fit.params["ma.S.L12"]
print(np.round([th, Th, th * Th], 4))
#> [-0.4018 -0.5569  0.2238]

# simple_differencing=True hace que statsmodels DIFERENCIE la serie antes de
# ajustar, como R. Sin esa opcion mete d y D en el espacio de estados con un
# prior difuso: los coeficientes salen casi iguales aqui, pero `nobs` pasa a
# ser 144 en vez de 131. El Modulo 6 vuelve sobre esto, porque afecta al AIC.