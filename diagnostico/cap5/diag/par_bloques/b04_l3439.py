import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess

# Heladeria inventada: desvios de su promedio en tres meses conocidos
feb24, mar24, feb25 = 15, 20, 10
phi, Phi = 0.6, 0.7                    # SARIMA(1,0,0)(1,0,0)[12]

# Ruta 1: el polinomio ya multiplicado, con el satelite en el rezago 13
print(round(phi * feb25 + Phi * mar24 - phi * Phi * feb24, 4))
#> 13.7

# Ruta 2: primero la sorpresa regular, despues la pregunta estacional
sorpresa_mar24 = mar24 - phi * feb24   # lo que febrero no explica de marzo
print(round(sorpresa_mar24, 4), round(phi * feb25 + Phi * sorpresa_mar24, 4))
#> 11.0 13.7

# Si los dos modelos se sumaran, sin satelite
print(round(phi * feb25 + Phi * mar24, 4))
#> 20.0

# Multiplicar polinomios es convolucionar sus coeficientes
poli = np.convolve([1, -phi], np.r_[1, np.zeros(11), -Phi])
# 1 - phi B - Phi B^12 + phi Phi B^13: coeficientes de B^0, B^1, B^12 y B^13
print(np.round(poli[[0, 1, 12, 13]], 2))
#> [ 1.   -0.6  -0.7   0.42]

# En la ACF, el satelite es el producto de los dos caminos
acf = ArmaProcess(poli, [1]).acf(14)
print(np.round(acf[[1, 11, 12, 13]], 4), round(acf[1] * acf[12], 4))
#> [0.6016 0.423  0.7011 0.4218] 0.4218