"""V3 · dos afirmaciones del informe del redactor sobre statsmodels y el airline (no están en la página, sino en su informe)."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from statsmodels.stats.diagnostic import acorr_ljungbox
ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
air = ARIMA(ap, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit()
for corte in (1, 13):
    e = air.resid[corte:]
    print(f"airline: residuales desde la posición {corte}: Ljung-Box(24, model_df=2) p =", round(float(acorr_ljungbox(e, lags=[24], model_df=2)['lb_pvalue'].iloc[0]), 6),
          " rho12 =", round(acf(e, nlags=24, fft=False)[12], 4))
print("primeros 14 residuales del airline (statsmodels):", np.round(air.resid[:14], 3))
f = ARIMA(ap, order=(8, 1, 3), trend="t").fit()
e = f.resid[1:]
print("ARIMA(8,1,3)+deriva en statsmodels: rho12 =", round(acf(e, nlags=24, fft=False)[12], 3), "(R: 0.437)")
