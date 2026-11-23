import numpy as np, pandas as pd, statsmodels.api as sm, warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
warnings.filterwarnings("ignore")

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
s = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))

# OJO: por defecto statsmodels NO diferencia la serie; mete d y D en el espacio
# de estados con un prior difuso, y entonces `nobs` sigue siendo 144 para todos
# los modelos. Sus AIC/BIC PARECEN comparables entre distintos (d, D) cuando no
# lo son. Con simple_differencing=True se comporta como R.
for sd in (False, True):
    f = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n",
                simple_differencing=sd).fit(disp=False)
    print(f"simple_differencing={sd!s:5s}  nobs={int(f.nobs):3d}  "
          f"ma1={f.params['ma.L1']:+.4f}  sma1={f.params['ma.S.L12']:+.4f}  llf={f.llf:.4f}")
#> simple_differencing=False  nobs=144  ma1=-0.4019  sma1=-0.5571  llf=244.6965
#> simple_differencing=True   nobs=131  ma1=-0.4018  sma1=-0.5569  llf=244.6965
# La segunda linea reproduce a R hasta el cuarto decimal.

fit = SARIMAX(s, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n").fit(disp=False)
print(acorr_ljungbox(fit.resid, lags=[24], model_df=2)["lb_pvalue"].round(4).iloc[0])
#> 0.2261
print(acorr_ljungbox(fit.resid[13:], lags=[24], model_df=2)["lb_pvalue"].round(4).iloc[0])
#> 0.3675
# R da 0.2330. La diferencia son los primeros residuales, que statsmodels
# produce con el filtro aun inicializandose: es la misma trampa del Capitulo 3.
# Descartando los d + D*m = 13 primeros, la conclusion no cambia en ningun caso.