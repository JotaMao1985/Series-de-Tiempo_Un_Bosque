import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values

# La misma lista de once candidatos que en R, no un producto cartesiano.
rejilla = [(1,0), (2,0), (3,0), (4,0),
           (0,1), (0,2), (0,3),
           (1,1), (2,1), (1,2), (2,2)]

filas = []
for p, q in rejilla:
    res = ARIMA(manchas, order=(p, 0, q), trend="c").fit()
    # model_df descuenta los parametros estimados, igual que fitdf en R
    lb = acorr_ljungbox(res.resid, lags=[12], model_df=p + q)
    filas.append({"modelo": f"ARMA({p},{q})", "AICc": round(res.aicc, 2),
                  "BIC": round(res.bic, 2),
                  "LB12": round(float(lb["lb_pvalue"].iloc[0]), 4)})

print(pd.DataFrame(filas).sort_values("AICc").to_string(index=False))
#    modelo   AICc    BIC   LB12
# ARMA(2,1) 834.73 847.12 0.3211
# ARMA(3,0) 836.52 848.91 0.3176
# ARMA(2,2) 836.63 851.36 0.1939
# ARMA(4,0) 836.78 851.51 0.1677
# ARMA(2,0) 838.30 848.30 0.1085   <- en R da 0.0461
# AICc y BIC coinciden con R hasta el ultimo decimal. Los p-valores de
# Ljung-Box NO: ver la advertencia de abajo.

# Reconciliacion: descartando los max(p,q) primeros residuales, los dos
# programas coinciden.
for p, q in [(2, 0), (2, 1), (2, 2)]:
    r = ARIMA(manchas, order=(p, 0, q), trend="c").fit()
    corte = max(p, q)
    lb = acorr_ljungbox(r.resid[corte:], lags=[12], model_df=p + q)
    print(f"ARMA({p},{q}) recortado: {float(lb['lb_pvalue'].iloc[0]):.4f}")
# ARMA(2,0) recortado: 0.0232      (R: 0.0232)
# ARMA(2,1) recortado: 0.1420      (R: 0.1424)
# ARMA(2,2) recortado: 0.1051      (R: 0.1057)

# statsmodels SI trae aicc; R no lo trae en arima() y hay que calcularlo.
# Cuidado tambien con model_df: por defecto vale 0 y la prueba se relaja.