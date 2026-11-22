import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

nilo = sm.datasets.nile.load_pandas().data["volume"].values

# Etapa 1: statsmodels no trae ndiffs() (pmdarima si); aqui se decide
# con las pruebas y el grafico
w = np.diff(nilo)

# Etapa 2
ajuste = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()

# Etapa 3: model_df descuenta los parametros, como fitdf en R
lb = acorr_ljungbox(ajuste.resid, lags=[20], model_df=2)
print(round(float(lb["lb_pvalue"].iloc[0]), 4))
#> 0.761     (R da 0.7997: cada programa inicializa el filtro a su manera y
#>            los primeros residuales difieren. La conclusion no cambia.)

# Etapa 4
print(np.round(ajuste.get_forecast(3).predicted_mean, 2))
#> [816.3  835.75 840.71]     R: 816.18 835.56 840.49