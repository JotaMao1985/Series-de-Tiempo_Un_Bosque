# statsmodels NO trae el algoritmo de Hyndman-Khandakar. Con solo statsmodels
# la alternativa es la rejilla a mano, que para d fijo es corta y ademas se ve
# lo que hace, que es justo el objetivo de este modulo.
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import warnings; warnings.filterwarnings("ignore")

nilo = sm.datasets.nile.load_pandas().data["volume"].values

mejor, mejor_aicc, evaluados = None, float("inf"), 0
for p in range(4):
    for q in range(4):
        try:
            f = ARIMA(nilo, order=(p, 1, q), trend="n").fit()
        except Exception:
            continue
        evaluados += 1
        k = len(f.params)
        a = f.aic + 2*k*(k+1)/(f.nobs-k-1)
        if a < mejor_aicc:
            mejor, mejor_aicc = (p, 1, q), a
print(mejor, round(mejor_aicc, 3), f"({evaluados} modelos)")
#> (1, 1, 1) 1267.469 (16 modelos)
#   mismo ganador que auto.arima; el AICc difiere en 0.04 porque statsmodels
#   no descuenta d en nobs (ver el modulo 6)

# ---- Alternativa con una dependencia extra ------------------------------
# pmdarima.auto_arima es una traduccion directa del algoritmo de R.
# NO viene con statsmodels: hay que instalarlo aparte, y no se ejecuta en
# este material, asi que su salida no se reproduce aqui.
#
#   pip install pmdarima
#
#   import pmdarima as pm
#   modelo = pm.auto_arima(nilo, seasonal=False, trace=True,
#                          information_criterion="aicc", stepwise=True)
#   modelo.order