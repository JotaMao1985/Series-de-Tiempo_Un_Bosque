import warnings; warnings.filterwarnings("ignore")
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
nilo = sm.datasets.nile.load_pandas().data["volume"].values
f = ARIMA(nilo, order=(1,1,1), trend="n").fit()
print("statsmodels ajuste: ", [f"{x:.6f}" for x in f.params], "llf =", f"{f.llf:.6f}", "aic =", f"{f.aic:.6f}")
pR = np.array([0.2544, -0.8741, 19769.29])   # estimados por R (ML), redondeados como en el capítulo
print("statsmodels evaluado en los parámetros de R (ar, ma, sigma2 de arima ML): llf =", f"{f.model.loglike(pR) if hasattr(f.model,'loglike') else None}")
