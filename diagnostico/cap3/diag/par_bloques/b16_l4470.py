import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

rng = np.random.default_rng(3)

procesos = {
    "ar1":  ArmaProcess(np.r_[1, -0.8], np.r_[1]),
    "ma1":  ArmaProcess(np.r_[1], np.r_[1, 0.8]),
    "arma": ArmaProcess(np.r_[1, -0.7], np.r_[1, 0.5]),
}

fig, ejes = plt.subplots(3, 3, figsize=(13, 8))
for fila, (nombre, proc) in enumerate(procesos.items()):
    x = proc.generate_sample(nsample=200, distrvs=rng.standard_normal)
    ejes[fila, 0].plot(x); ejes[fila, 0].set_title(nombre)
    plot_acf(x,  lags=16, ax=ejes[fila, 1], title="ACF")
    plot_pacf(x, lags=16, ax=ejes[fila, 2], title="PACF", method="ywm")
plt.tight_layout()

# generate_sample NO descarta calentamiento por defecto: se pide con burnin=
x = procesos["ar1"].generate_sample(nsample=200, burnin=100,
                                    distrvs=rng.standard_normal)