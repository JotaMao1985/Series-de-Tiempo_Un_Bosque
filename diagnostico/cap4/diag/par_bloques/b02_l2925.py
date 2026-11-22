import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima_process import ArmaProcess

nilo = sm.datasets.nile.load_pandas().data["volume"].values
print(len(nilo))
#> 100

# El mismo polinomio expandido
phi = 0.2544
ar_expandido = np.array([1 + phi, -phi])
print(np.round(ar_expandido, 4), ar_expandido.sum())
#> [ 1.2544 -0.2544] 1.0

# np.roots recibe los coeficientes en orden DESCENDENTE, al reves que polyroot
coef = np.r_[1.0, -ar_expandido]              # orden ascendente
print(np.round(np.abs(np.roots(coef[::-1])), 4))
#> [3.9308 1.    ]     mismas raices que R, en el orden contrario

# Simular: ArmaProcess pide los polinomios con el signo YA aplicado.
# El generador de numeros aleatorios NO es el de R, asi que una realizacion
# suelta no coincide; se promedian 500 para que la comparacion signifique algo.
proceso  = ArmaProcess(ar=np.r_[1, -0.2544], ma=np.r_[1, -0.8741])
proceso0 = ArmaProcess(ar=np.r_[1, -0.2544], ma=np.r_[1])      # sin termino MA
rng = np.random.default_rng(7)
razon  = np.mean([np.cumsum(w).var() / w.var()
                  for w in (proceso.generate_sample(200, distrvs=rng.standard_normal)
                            for _ in range(500))])
razon0 = np.mean([np.cumsum(w).var() / w.var()
                  for w in (proceso0.generate_sample(200, distrvs=rng.standard_normal)
                            for _ in range(500))])
print(round(razon, 3), round(razon0, 1))
#> 1.363 56.7      con theta = -0.8741 integrar casi no cambia la varianza;
#>                 sin el termino MA la multiplica por decenas
#   (en R, con su propio generador, sale 1.006 y 32.8: el mensaje es el mismo)