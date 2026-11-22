"""Verificador B · R4 cap. 3 · lado Python de c3-m7-16, c3-m7-17 y c3-m8-18 (statsmodels)."""
import inspect, warnings
import numpy as np, statsmodels, statsmodels.api as sm
from statsmodels.regression.linear_model import yule_walker
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__)
d = sm.datasets.sunspots.load_pandas().data
m = d.loc[(d.YEAR >= 1770) & (d.YEAR <= 1869), "SUNACTIVITY"].values
print("n =", len(m))
print("c3-m7-17 firma:", inspect.signature(yule_walker))
doc = yule_walker.__doc__
i = doc.find("method :"); print("docstring:", " ".join(doc[i:i + 400].split()))
print("adjusted (defecto):", np.round(yule_walker(m - m.mean(), order=2)[0], 4))
print("mle:", np.round(yule_walker(m - m.mean(), order=2, method="mle")[0], 4))
res = ARIMA(m, order=(2, 0, 0), trend="c").fit()
print("c3-m8-18 resid[:4]:", np.round(res.resid[:4], 3), "| arparams", np.round(res.arparams, 4))
print("LB(12) model_df=2 statsmodels:", round(float(acorr_ljungbox(res.resid, lags=[12], model_df=2)["lb_pvalue"].iloc[0]), 4))
print("LB(12) sin los dos primeros:", round(float(acorr_ljungbox(res.resid[2:], lags=[12], model_df=2)["lb_pvalue"].iloc[0]), 4))
