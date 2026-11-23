import numpy as np, pandas as pd, statsmodels.api as sm

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
uad = sm.datasets.get_rdataset("USAccDeaths").data["value"].values

def diferenciar(x, d=0, D=0, m=12):
    """Diferencia estacional D veces y luego regular d veces."""
    for _ in range(D):
        x = x[m:] - x[:-m]          # nabla_m: NO es np.diff(x, n=m)
    if d:
        x = np.diff(x, n=d)
    return x

for d in (0, 1):
    for D in (0, 1):
        w = diferenciar(ap, d, D)
        a = sm.tsa.acf(w, nlags=12, fft=False)
        print(f"d={d} D={D}  n={len(w):3d}  var={w.var(ddof=1):.6f}  "
              f"r1={a[1]:+.4f}  r12={a[12]:+.4f}")
#> d=0 D=0  n=144  var=0.194884  r1=+0.9537  r12=+0.7619
#> d=0 D=1  n=132  var=0.003800  r1=+0.7137  r12=-0.2430
#> d=1 D=0  n=143  var=0.011354  r1=+0.1998  r12=+0.8414
#> d=1 D=1  n=131  var=0.002102  r1=-0.3411  r12=-0.3866

# Los operadores conmutan tambien aqui
print(np.max(np.abs(diferenciar(uad, 1, 1) - np.diff(uad[12:] - uad[:-12]))))
#> 0

# statsmodels NO trae equivalentes de ndiffs()/nsdiffs(): la decision se toma
# a mano, y las pruebas de raiz unitaria del Capitulo 2 se aplican SIEMPRE a la
# serie ya sin estacionalidad. Sobre USAccDeaths eso reproduce el orden
# "primero D, despues d":
from statsmodels.tsa.stattools import kpss
print(round(kpss(diferenciar(uad, 0, 1), regression="c", nlags=4)[0], 4))
#> 0.8672     valor critico al 5 % = 0.463 -> RECHAZA: falta la diferencia regular
print(round(kpss(diferenciar(uad, 1, 1), regression="c", nlags=4)[0], 4))
#> 0.0713     ya no rechaza: con d = 1 y D = 1 se llega a la estacionariedad