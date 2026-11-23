# lectorD_comprobaciones.py · comprobaciones en Python (statsmodels) del lector D (cap. 4, M8 y M9).
# Uso: python3 -I lectorD_comprobaciones.py
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import arma2ma
import statsmodels, warnings
warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values
f = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
print("sigma2 statsmodels (ARIMA(1,1,1)) =", round(float(f.params[-1]), 1))
# comentario de c4-m9-30: arma2ma pide los polinomios completos con el signo ya aplicado
print("arma2ma(ar=[1,-0.5], ma=[1], lags=4) =", np.round(arma2ma([1, -0.5], [1], lags=4), 4).tolist())
# comentario de c4-m8-21: optimizador de statsmodels y el borde
for d in (1, 2, 3):
    x = np.diff(nilo, n=d)
    g = ARIMA(x, order=(0, 0, 1), trend="n").fit()
    print(f"d={d} theta={g.params[0]:.4f}  |raiz MA|={abs(np.roots([g.params[0], 1])[0]):.4f}")
