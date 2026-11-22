import numpy as np, pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss, acf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings; warnings.filterwarnings("ignore")

# TRM mensual (promedio del mes, SFC via datos.gov.co); necesita internet.
url = ("https://www.datos.gov.co/resource/32sa-8pi3.json"
       "?$select=vigenciadesde,valor&$limit=50000")
crudo = pd.read_json(url)
crudo["fecha"] = pd.to_datetime(crudo["vigenciadesde"]).dt.tz_localize(None)
crudo = crudo[crudo["fecha"] >= "2015-01-01"]
mensual = crudo.set_index("fecha")["valor"].resample("MS").mean()
y = mensual.loc[:"2026-06-01"].values
print(len(y))
#> 138

# Etapa 1: d. ADF con tendencia y 5 rezagos, KPSS con 4, como tseries
for nombre, x in (("nivel", y), ("d1", np.diff(y))):
    a = adfuller(x, regression="ct", maxlag=5, autolag=None)
    k = kpss(x, regression="c", nlags=4)
    print(nombre, round(a[0], 3), round(a[1], 3), round(k[0], 3), k[1])
#> nivel -1.978 0.613 2.243 0.01
#> d1 -3.88 0.013 0.241 0.1
# Los estadisticos coinciden con R; el p del ADF no (0.613 y 0.013 frente a
# 0.585 y 0.017): statsmodels usa la aproximacion de MacKinnon y tseries
# interpola en una tabla. La decision es la misma: d = 1.

# Etapa 1: p y q
r = acf(np.diff(y), nlags=20, fft=False)[1:]
banda = 1.96 / np.sqrt(len(y) - 1)
print(np.round([r[0], r[7], banda], 3), np.where(np.abs(r) > banda)[0] + 1)
#> [ 0.088 -0.19   0.167] [8]

# Etapa 2: la rejilla con d = 1
rej = {(p, q): ARIMA(y, order=(p, 1, q)).fit()
       for p in range(3) for q in range(3)}
for (p, q), f in sorted(rej.items(), key=lambda kv: kv[1].aicc)[:3]:
    print((p, 1, q), round(f.aicc, 2), round(f.bic, 2))
#> (0, 1, 0) 1705.94 1708.83
#> (0, 1, 1) 1706.7 1712.45
#> (1, 1, 0) 1706.8 1712.55
f212 = rej[(2, 2)]
print(round(f212.aicc, 2), np.round(np.abs(f212.maroots), 3))
#> 1712.91 [1.088 4.231]
# El (2,1,2) degenerado que gana en R no aparece: statsmodels impone
# estacionariedad e invertibilidad mientras estima, asi que no puede llegar a
# una raiz sobre el circulo, y su (2,1,2) es otro optimo, 7 puntos peor que el
# (0,1,0). auto.arima descarta esas raices despues de estimar; aqui ni se
# alcanzan. statsmodels no trae auto.arima: la rejilla hace su papel.

# Etapa 3: diagnostico de la caminata aleatoria
rw = ARIMA(y, order=(0, 1, 0)).fit()
e = rw.resid[1:]                  # el primer residual es y_1: se descarta
p_lb = acorr_ljungbox(e, lags=[20, 12])["lb_pvalue"].values
p_lb2 = acorr_ljungbox(e**2, lags=[12])["lb_pvalue"].values[0]
print(np.round([*p_lb, stats.shapiro(e).pvalue, p_lb2], 4).tolist())
#> [0.194, 0.2096, 0.0007, 0.8395]
# R da 0.189, 0.206, 0.0006 y 0.857 porque conserva un primer residual
# minusculo (2.40, el rastro del arranque difuso). Quitandoselo, R da estas
# mismas cifras. La lectura no cambia: pasa Ljung-Box y no es normal.
fd = ARIMA(y, order=(0, 1, 0), trend="t").fit(cov_type="oim")
print(np.round([fd.params[0], fd.bse[0]], 2))
#> [ 8.   10.35]
# Con la covarianza por defecto (OPG) el error estandar sale 11.17. OPG y la
# informacion observada solo coinciden si los residuales son normales, y
# estos no lo son. Con la observada, 10.35 frente al 10.36 de R.

# Etapa 4: el abanico, y_T +- z * sigma * sqrt(h)
s = np.sqrt(rw.params[-1]); z = stats.norm.ppf(0.975)
h = np.array([1, 3, 6, 12, 24]); sh = s * np.sqrt(h)
tabla = pd.DataFrame({"h": h, "sigma_h": sh, "semiancho": z * sh,
                      "inf": y[-1] - z * sh, "sup": y[-1] + z * sh})
print(tabla.round(2).to_string(index=False))
#>  h  sigma_h  semiancho     inf     sup
#>  1   121.48     238.09 3259.00 3735.18
#>  3   210.40     412.38 3084.71 3909.47
#>  6   297.55     583.19 2913.90 4080.29
#> 12   420.80     824.76 2672.33 4321.85
#> 24   595.11    1166.39 2330.70 4663.48
ic = rw.get_forecast(24).conf_int(alpha=0.05)
print(f"{np.max(np.abs(ic[h - 1, 1] - tabla['sup'].values)):.1e}")
#> 9.1e-13        get_forecast da el mismo abanico

# Cuantos cambios reales caen fuera del 95 %
d1 = np.diff(y); d12 = y[12:] - y[:-12]
print(np.sum(np.abs(d1) > z * s), np.sum(d1 > z * s), len(d1))
#> 6 5 137
print(np.sum(np.abs(d12) > z * s * np.sqrt(12)), len(d12))
#> 11 126
curtosis = lambda x: stats.kurtosis(x, fisher=False)
print(np.round([curtosis(d1), curtosis(d12)], 1))
#> [5.1 2.8]