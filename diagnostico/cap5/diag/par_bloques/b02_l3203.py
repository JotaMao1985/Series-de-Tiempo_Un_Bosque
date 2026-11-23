import numpy as np, pandas as pd
import statsmodels.api as sm

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
idx = pd.date_range("1949-01", periods=len(ap), freq="MS")
s = pd.Series(ap, index=idx)

# 1. Vista: la tabla mes x anio ES el mapa de calor del simulador
tabla = s.groupby([s.index.year, s.index.month]).first().unstack()
print(tabla.round(2).iloc[:3, :4])
#>         1     2     3     4
#> 1949 4.72  4.77  4.88  4.86
#> 1950 4.74  4.84  4.95  4.91
#> 1951 4.98  5.01  5.18  5.09

# 2. Medida: acf con nlags = 36
acf = sm.tsa.acf(ap, nlags=36, fft=False)
print(np.round(acf[[1, 12, 24, 36]], 4))
#> [0.9537 0.7619 0.5205 0.3193]
print(round(1.96 / np.sqrt(len(ap)), 4))
#> 0.1633

# statsmodels usa el mismo divisor n que R, asi que los numeros coinciden
# hasta el ultimo decimal. Ojo: plot_acf() dibuja por defecto lags=None,
# que se queda muy corto para una serie mensual.