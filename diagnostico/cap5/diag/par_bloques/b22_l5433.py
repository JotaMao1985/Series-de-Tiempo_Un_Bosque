import numpy as np, pandas as pd, statsmodels.api as sm, warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
warnings.filterwarnings("ignore")

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
idx = pd.date_range("1949-01", periods=len(ap), freq="MS")
s = pd.Series(ap, index=idx)

dias = idx.days_in_month.values.astype(float)
print(dias.min(), dias.max())
#> 28.0 31.0

def pascua(anio):
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    f, g = (b + 8) // 25, (b - ((b + 8) // 25) + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    return ((h + l - 7*m + 114) // 31, ((h + l - 7*m + 114) % 31) + 1)

print([pascua(a) for a in range(1949, 1953)])
#> [(4, 17), (4, 9), (3, 25), (4, 13)]
es_pascua = np.array([1.0 if pascua(t.year)[0] == t.month else 0.0 for t in idx])
print(int(es_pascua.sum()))
#> 12

X = np.column_stack([np.log(dias), es_pascua])
f2 = SARIMAX(s, exog=X, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n",
             simple_differencing=True).fit(disp=False)
print(f2.params[["x1", "x2"]].round(4).values,
      f2.bse[["x1", "x2"]].round(4).values,
      f2.tvalues[["x1", "x2"]].round(4).values)
#> [1.0764 0.029 ] [0.4069 0.009 ] [2.6457 3.2195]
# R da coef [1.0840 0.0290], ee [0.4462 0.0111], t [2.4291 2.6026]. Los
# COEFICIENTES coinciden en el segundo decimal; los ERRORES ESTANDAR no (los
# de Python son un 9 % y un 19 % menores), porque las dos implementaciones no
# tratan igual la diferenciacion de los regresores. La conclusion no cambia:
print(round(float((f2.params["x1"] - 1) / f2.bse["x1"]), 4))
#> 0.1879     R da 0.1882: tampoco aqui se rechaza beta = 1