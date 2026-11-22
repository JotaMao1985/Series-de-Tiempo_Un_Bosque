import numpy as np, statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss

nilo = sm.datasets.nile.load_pandas().data["volume"].values

for d in range(4):
    x = np.diff(nilo, n=d) if d else nilo     # np.diff(x, n=0) SI es la identidad
    print(f"d = {d}  n = {len(x):3d}  var = {x.var(ddof=1):10.2f}")
#> d = 0  n = 100  var =   28637.95
#> d = 1  n =  99  var =   28268.34
#> d = 2  n =  98  var =   80055.01
#> d = 3  n =  97  var =  262507.29

# Para reproducir el estadistico de adf.test() de R hacen falta sus opciones:
est, p, *_ = adfuller(nilo, regression="ct", autolag=None,
                      maxlag=int((len(nilo) - 1) ** (1 / 3)))
print(round(est, 4), round(p, 4))
#> -3.3657 0.0561    mismo estadistico que R (-3.3657); el p-valor difiere
#>                   porque R interpola en tablas y statsmodels usa MacKinnon

# CUIDADO con el truncamiento de KPSS: no es el mismo por defecto.
print(round(kpss(nilo, regression="c")[0], 4))                   # 'auto': 5 rezagos
#> 0.8691        !=  0.9654 de R
print(round(kpss(nilo, regression="c", nlags="legacy")[0], 4))   # 12 rezagos
#> 0.5497
print(round(kpss(nilo, regression="c", nlags=4)[0], 4))          # como R
#> 0.9654        identico

# El experimento del escalon, ya con el truncamiento de R
rng = np.random.default_rng(2026)
escalon = (np.arange(100) >= 28).astype(float)
def simula(beta, reps=400):                   # beta = tamano del escalon
    return np.mean([kpss(1000 + beta * escalon + rng.normal(0, 127.03, 100),
                         regression="c", nlags=4)[1] <= 0.05
                    for _ in range(reps)])
print(simula(0.0), simula(-247.78))
#> 0.035 1.0     (R: 0.045 y 1.000)