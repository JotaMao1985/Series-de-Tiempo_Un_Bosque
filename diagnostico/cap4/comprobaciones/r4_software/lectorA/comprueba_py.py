# Lector A (M1, M2) · comprobaciones de software en Python (statsmodels 0.14.6, numpy 2.2.6)
import inspect
import numpy as np
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import statsmodels.tsa.stattools as st
import statsmodels.graphics.tsaplots as tp

print("statsmodels", statsmodels.__version__, "numpy", np.__version__)

# c4-m1-21: np.roots recibe los coeficientes en orden DESCENDENTE
# [1,-3,2] leido de mayor a menor grado es x^2-3x+2 (raices 2 y 1); leido en orden creciente seria 1-3x+2x^2 (raices 1 y .5)
print("np.roots([1,-3,2]) =", np.roots([1, -3, 2]), "  (descendente: x^2-3x+2 -> raices 2 y 1)")
print("np.roots([2,-3,1]) =", np.roots([2, -3, 1]), "  (si se leyera ascendente seria 2-3x+x^2 -> raices 1 y 2; descendente: 2x^2-3x+1 -> 1 y 0.5)")

# c4-m1-22: ArmaProcess pide los polinomios con el signo YA aplicado (ar=[1,-phi]; ma=[1,+theta])
proc = ArmaProcess(ar=np.r_[1, -0.6], ma=np.r_[1, 0.5])
print("ArmaProcess(ar=[1,-.6], ma=[1,.5]): acf(2) =", np.round(proc.acf(lags=2), 4),
      " arroots =", np.round(proc.arroots, 4), " maroots =", np.round(proc.maroots, 4))
# AR(1) con phi=+0.6 => ar=[1,-0.6] => raiz AR 1/0.6 = 1.667 (fuera del circulo); con ar=[1,0.6] seria phi=-0.6
print("  raiz AR con ar=[1,-.6]:", np.round(np.abs(proc.arroots), 4), " (1/0.6 = 1.6667: phi = +0.6)")
print("  rho1 del MA con ma=[1,+0.5] y sin AR:", np.round(ArmaProcess(ar=[1], ma=[1, 0.5]).acf(lags=2)[1], 4), "(theta/(1+theta^2) = 0.4: signo MAS)")

# c4-m1-27: ARIMA de statsmodels estima theta con signo MAS (convencion R)
rng = np.random.default_rng(11)
y = ArmaProcess(ar=[1], ma=[1, 0.6]).generate_sample(2000, distrvs=rng.standard_normal)
res = ARIMA(y, order=(0, 0, 1), trend="n").fit()
print("MA(1) simulado con theta = +0.6 (signo mas); ARIMA(0,0,1).fit() da ma.L1 =", np.round(res.params[0], 3))

# c4-m2-18: statsmodels no trae ndiffs
print("statsmodels.tsa.stattools tiene ndiffs:", hasattr(st, "ndiffs"))
import statsmodels.tsa.api as tsaapi
import statsmodels.tsa.arima_process as ap
import statsmodels.tsa.arima.model as am
print("objetos llamados ndiffs en tsa.api / arima_process / arima.model:",
      [hasattr(m, "ndiffs") for m in (tsaapi, ap, am)])

# c4-m2-19: acorr_ljungbox tiene model_df y su docstring habla de los grados de libertad del modelo
print("firma acorr_ljungbox:", inspect.signature(acorr_ljungbox))
doc = inspect.getdoc(acorr_ljungbox)
i = doc.find("model_df")
print("docstring (model_df):", " ".join(doc[i:i + 420].split()))

# c4-m2-22: nombres de funciones del panel "Con que"
for nombre, obj in [("adfuller", st.adfuller), ("kpss", st.kpss), ("plot_acf", tp.plot_acf), ("plot_pacf", tp.plot_pacf),
                    ("acorr_ljungbox", acorr_ljungbox)]:
    print(nombre, "existe:", callable(obj))
r = ARIMA(y, order=(0, 0, 1), trend="n").fit()
print("ARIMAResults.plot_diagnostics existe:", hasattr(r, "plot_diagnostics"),
      "| get_forecast existe:", hasattr(r, "get_forecast"),
      "| conf_int existe:", hasattr(r.get_forecast(2), "conf_int"))
