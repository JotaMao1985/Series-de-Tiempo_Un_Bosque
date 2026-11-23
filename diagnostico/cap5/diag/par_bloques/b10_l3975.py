import numpy as np, pandas as pd

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
t = np.arange(1, 49)
patron = np.array([-6, -8, -4, -2, 0, 4, 6, 4, 0, -2, 2, 6])
fechas = pd.period_range("2022-01", periods=48, freq="M")
y = pd.Series(100 + (t - 1) + patron[(t - 1) % 12], index=fechas)

def cuadricula(s):
    """Un ano por fila y un mes por columna, como imprime R."""
    s = s.dropna()
    tabla = s.groupby([s.index.year, s.index.month]).first().unstack()
    return tabla.astype("Int64").rename(columns=dict(enumerate(MESES, 1)))

print(cuadricula(y))
#>       Ene  Feb  Mar  Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic
#> 2022   94   93   98  101  104  109  112  111  108  107  112  117
#> 2023  106  105  110  113  116  121  124  123  120  119  124  129
#> 2024  118  117  122  125  128  133  136  135  132  131  136  141
#> 2025  130  129  134  137  140  145  148  147  144  143  148  153
print(cuadricula(y.diff(12)))          # nabla_12: menos la celda de arriba
#>       Ene  Feb  Mar  Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic
#> 2023   12   12   12   12   12   12   12   12   12   12   12   12
#> 2024   12   12   12   12   12   12   12   12   12   12   12   12
#> 2025   12   12   12   12   12   12   12   12   12   12   12   12
print(cuadricula(y.diff()))            # nabla: menos la celda de la izquierda
#>        Ene  Feb  Mar  Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic
#> 2022  <NA>   -1    5    3    3    5    3   -1   -3   -1    5    5
#> 2023   -11   -1    5    3    3    5    3   -1   -3   -1    5    5
#> 2024   -11   -1    5    3    3    5    3   -1   -3   -1    5    5
#> 2025   -11   -1    5    3    3    5    3   -1   -3   -1    5    5
print(cuadricula(y.diff(12).diff()))   # las dos
#>        Ene  Feb  Mar  Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic
#> 2023  <NA>    0    0    0    0    0    0    0    0    0    0    0
#> 2024     0    0    0    0    0    0    0    0    0    0    0    0
#> 2025     0    0    0    0    0    0    0    0    0    0    0    0
print((y.diff(12).diff() - y.diff().diff(12)).abs().max())   # orden: da igual
#> 0.0

# Desde enero de 2024 la tienda crece tres unidades al mes
tend2 = np.where(t <= 24, t - 1, 23 + 3 * (t - 24))
y2 = pd.Series(100 + tend2 + patron[(t - 1) % 12], index=fechas)
print(cuadricula(y2.diff(12)))
#>       Ene  Feb  Mar  Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic
#> 2023   12   12   12   12   12   12   12   12   12   12   12   12
#> 2024   14   16   18   20   22   24   26   28   30   32   34   36
#> 2025   36   36   36   36   36   36   36   36   36   36   36   36
print(cuadricula(y2.diff(12).diff()))
#>        Ene  Feb  Mar  Abr  May  Jun  Jul  Ago  Sep  Oct  Nov  Dic
#> 2023  <NA>    0    0    0    0    0    0    0    0    0    0    0
#> 2024     2    2    2    2    2    2    2    2    2    2    2    2
#> 2025     0    0    0    0    0    0    0    0    0    0    0    0