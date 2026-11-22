import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings; warnings.filterwarnings("ignore")

nilo = sm.datasets.nile.load_pandas().data["volume"].values
anios = np.arange(1871, 1971)

# La firma de la sobrediferenciacion
for d in (1, 2, 3):
    x = np.diff(nilo, n=d)
    f = ARIMA(x, order=(0, 0, 1), trend="n").fit()
    th = f.params[0]
    print(f"d = {d}  var = {x.var(ddof=1):9.0f}  theta = {th:7.4f}  "
          f"|raiz MA| = {abs(np.roots([th, 1])[0]):.4f}")
#> d = 1  var =     28268  theta = -0.7329  |raiz MA| = 1.3644
#> d = 2  var =     80055  theta = -0.9988  |raiz MA| = 1.0012
#> d = 3  var =    262507  theta = -0.9980  |raiz MA| = 1.0020
#   El optimizador de statsmodels se queda a 0.001 del borde en vez de
#   clavarse en -1 como el de R. La lectura no cambia: raiz sobre el circulo.

# El escalon de 1899 como regresor externo
escalon = (anios >= 1899).astype(float).reshape(-1, 1)
fe = ARIMA(nilo, order=(0, 0, 0), exog=escalon, trend="c").fit()
print(round(fe.params[1], 2), round(fe.bse[1], 2))
#> -247.78 27.77     el coeficiente coincide con R; el error estandar no
#>                   exactamente (R da 28.15). t = -8.9 frente a -8.8.
print(round(float(acorr_ljungbox(fe.resid, lags=[20])["lb_pvalue"].iloc[0]), 4))
#> 0.8124