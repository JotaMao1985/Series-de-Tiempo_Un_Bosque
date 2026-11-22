import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import warnings; warnings.filterwarnings("ignore")

nilo = sm.datasets.nile.load_pandas().data["volume"].values

filas = []
for d in range(3):
    for p in range(3):
        for q in range(3):
            try:
                f = ARIMA(nilo, order=(p, d, q),
                          trend="c" if d == 0 else "n").fit()
            except Exception:
                continue
            # CUIDADO: f.nobs vale 100 para TODOS los d, pero la verosimilitud
            # descarta las d primeras observaciones (f.loglikelihood_burn = d,
            # inicializacion difusa) y f.nobs_effective SI vale n - d.
            # f.aicc y f.bic ya usan ese n efectivo; no hay que rehacerlos a mano.
            filas.append(dict(d=d, modelo=f"ARIMA({p},{d},{q})",
                              nobs=f.nobs, n_ef=f.nobs_effective,
                              aicc=round(f.aicc, 2), bic=round(f.bic, 2)))
tabla = pd.DataFrame(filas)
print(tabla.loc[tabla.groupby("d")["aicc"].idxmin(), ["d","modelo","nobs","n_ef","aicc"]]
      .to_string(index=False))
#>  d       modelo  nobs  n_ef    aicc
#>  0 ARIMA(1,0,1)   100   100 1282.50
#>  1 ARIMA(1,1,1)   100    99 1267.47     <- nobs no baja; n_ef si
#>  2 ARIMA(1,2,2)   100    98 1264.67
# Los tres ganadores coinciden con R (1282.50 / 1267.51 / 1264.60), y el
# n efectivo es el mismo: los AICc de distinto d tampoco son comparables aqui.