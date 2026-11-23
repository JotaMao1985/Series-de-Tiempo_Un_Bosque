import numpy as np, pandas as pd, statsmodels.api as sm, warnings
from statsmodels.tsa.deterministic import Fourier, DeterministicProcess
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import STL
warnings.filterwarnings("ignore")

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))

# Fourier: statsmodels los genera con DeterministicProcess. Fijamos los errores
# en ARIMA(0,1,4) para que la comparacion entre K sea limpia (statsmodels no
# trae auto.arima).
for K in range(1, 7):
    dp = DeterministicProcess(s.index, constant=False,
                              additional_terms=[Fourier(12, order=K)])
    X = dp.in_sample()
    f = SARIMAX(s, exog=X, order=(0, 1, 4), trend="n").fit(disp=False)
    print(f"K={K}  terminos={X.shape[1]:2d}  aic={f.aic:9.2f}")
#> K=1  terminos= 2  aic=  -306.95
#> K=2  terminos= 4  aic=  -389.88
#> K=3  terminos= 6  aic=  -414.34
#> K=4  terminos= 8  aic=  -470.58
#> K=5  terminos=10  aic=  -502.38
#> K=6  terminos=12  aic=  -501.62

# TRAMPA: con K = m/2, statsmodels emite 12 columnas y R solo 11. La de mas es
# el seno de frecuencia m/2, que es IDENTICAMENTE CERO: la matriz de diseno
# queda con rango 11 y una columna sobra.
X = DeterministicProcess(s.index, constant=False,
                         additional_terms=[Fourier(12, order=6)]).in_sample()
print(X.shape[1], np.linalg.matrix_rank(X.values),
      [c for c in X.columns if X[c].abs().max() < 1e-12])
#> 12 11 ['sin(6,12)']
# Hay que quitarla a mano: X = X.drop(columns="sin(6,12)")

# STL: aqui se descompone y se modela el resto a mano
res = STL(s, period=12, robust=False).fit()
desestacionalizada = s - res.seasonal
f = SARIMAX(desestacionalizada, order=(1, 1, 1), trend="t").fit(disp=False)
print(round(f.aic, 2))
#> -643.05
# Cuidado: este AIC no se compara con NINGUNO de los anteriores. Ni siquiera
# modela la misma serie: modela la desestacionalizada. Y R da -542.95 porque
# su stlm() estima el componente estacional de otra forma.