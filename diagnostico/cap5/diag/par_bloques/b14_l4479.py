import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess

def acf_sarima(phi=(), Phi=0.0, theta=(), Theta=0.0, m=12, lag_max=36):
    """ACF teorica de un SARIMA sin diferencias, expandiendo el polinomio."""
    def poli_est(c0):
        v = np.zeros(m + 1); v[0] = 1.0; v[m] = c0
        return v
    ar_pol = np.polymul(np.r_[1.0, -np.asarray(phi, float)],   poli_est(-Phi))
    ma_pol = np.polymul(np.r_[1.0,  np.asarray(theta, float)], poli_est(Theta))
    # ArmaProcess espera el polinomio AR con los signos ya cambiados
    proc = ArmaProcess(ar_pol, ma_pol)
    return proc.acf(lag_max + 1)[1:]

print(np.round(acf_sarima(Phi=0.7)[[0, 10, 11, 12, 23]], 4))
#> [0.  0.  0.7 0.  0.49]

print(np.round(acf_sarima(phi=[0.6], Phi=0.7)[[0, 10, 11, 12, 23]], 4))
#> [0.6016 0.423  0.7011 0.4218 0.4908]

print(np.round(acf_sarima(theta=[-0.4018], Theta=-0.5569)[[0, 10, 11, 12, 23]], 4))
#> [-0.3459  0.1471 -0.4251  0.1471  0.    ]

# np.polymul hace exactamente lo mismo que la funcion `mult` del bloque de R:
# la "estacionalidad" no es mas que un polinomio con ceros en medio.