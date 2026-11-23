import warnings; warnings.filterwarnings("ignore")
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
nilo = sm.datasets.nile.load_pandas().data["volume"].values
for d in range(3):
    f = ARIMA(nilo, order=(1, d, 1), trend="c" if d == 0 else "n").fit()
    k = len(f.params)
    bic_ef = -2 * f.llf + k * np.log(f.nobs_effective); bic_n = -2 * f.llf + k * np.log(f.nobs)
    print(f"d={d}: f.bic = {f.bic:.4f} · con log(n_ef) = {bic_ef:.4f} · con log(n=100) = {bic_n:.4f}  -> usa n_ef: {abs(f.bic-bic_ef) < 1e-6}")
