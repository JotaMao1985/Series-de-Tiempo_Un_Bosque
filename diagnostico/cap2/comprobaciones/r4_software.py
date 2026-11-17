"""R4 del capítulo 2 · lo que el capítulo dice de statsmodels (c2-m3-06, c2-m4-09).

Se comprueba ejecutando: acf(adjusted=False) divide entre T, y los métodos
`ywm` y `ldb` de pacf dan lo mismo que la recursión de Durbin-Levinson
aplicada a esa ACF. La serie es log(AirPassengers), leída de R.
"""
import subprocess
import numpy as np
import statsmodels
from statsmodels.tsa.stattools import acf, pacf

print("statsmodels", statsmodels.__version__)
y = np.array(subprocess.run(["Rscript", "-e", "cat(log(AirPassengers))"],
                            capture_output=True, text=True).stdout.split(), float)
n = len(y); d = y - y.mean()
r_T = np.array([np.sum(d[:n - k] * d[k:]) / n for k in range(25)]); r_T /= r_T[0]
print("max |acf(adjusted=False) - divisor T|:", np.abs(acf(y, nlags=24, adjusted=False) - r_T).max())


def durbin_levinson(rho):
    pk, phi = [], np.array([])
    for k in range(1, len(rho) + 1):
        if k == 1:
            pkk = rho[0]; phi = np.array([pkk])
        else:
            pkk = (rho[k - 1] - phi @ rho[k - 2::-1][:k - 1]) / (1 - phi @ rho[:k - 1])
            phi = np.append(phi - pkk * phi[::-1], pkk)
        pk.append(pkk)
    return np.array(pk)


dl = durbin_levinson(r_T[1:])
for metodo in ("ywm", "ldb"):
    print(f"max |pacf(method='{metodo}') - Durbin-Levinson|:",
          np.abs(pacf(y, nlags=24, method=metodo)[1:] - dl).max())
doc = pacf.__doc__
for clave in ('"ywm" or "ywmle"', '"ldb" or "ldbiased"'):
    i = doc.find(clave); print("docstring:", " ".join(doc[i:i + 90].split()))
