"""V3 · V4: el ARIMA(0,1,5) del bloque Python del M1. Los coeficientes de statsmodels frente a los de R (que
imprime v3_python_m1.R) y los primeros residuales de cada uno: la diferencia de ACF esta en el arranque."""
import subprocess, warnings, numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
warnings.simplefilter("ignore")
ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
f = ARIMA(ap, order=(0, 1, 5), trend="n").fit()
print("statsmodels: coef", np.round(f.params[:5], 4), "converge", f.mle_retvals["converged"])
print("statsmodels: primeros residuales", np.round(f.resid[:6], 4))
for k in (1, 7, 13):
    print(f"statsmodels: ACF 12 y 24 sin los {k} primeros", np.round(sm.tsa.acf(f.resid[k:], nlags=24, fft=False)[[12, 24]], 4))
print(subprocess.run(["Rscript", "-e", "suppressMessages(library(forecast)); m <- Arima(log(AirPassengers), order = c(0,1,5)); "
    "cat('R: coef', round(coef(m), 4), '\\nR: primeros residuales', round(head(as.numeric(residuals(m)), 6), 4), '\\n')"],
    capture_output=True, text=True).stdout)
