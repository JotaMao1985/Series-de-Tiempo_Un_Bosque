# R1 · T1.1 · Bloque pandas del M5: una forma en dos pasos que de la 2x12.
# Control: julio de 1955 = 285.75 y 12 huecos (6 y 6).
# AirPassengers se toma de R (datasets::AirPassengers) para no depender de la red.
import subprocess
import pandas as pd

vals = subprocess.run(["Rscript", "-e", "cat(as.numeric(AirPassengers))"],
                      capture_output=True, text=True, check=True).stdout.split()
pasajeros = pd.Series([float(v) for v in vals],
                      index=pd.date_range("1949-01-01", periods=len(vals), freq="MS"),
                      name="pasajeros")
print("n =", len(pasajeros), " jul-1955 observado =", pasajeros["1955-07-01"])

print("\n== ANTES (lo publicado) ==")
viejo = pasajeros.rolling(window=12, center=True).mean()
print("rolling(window=12, center=True): jul-1955 =", viejo["1955-07-01"],
      " NaN =", int(viejo.isna().sum()),
      " primero valido =", viejo.first_valid_index().date(),
      " ultimo valido =", viejo.last_valid_index().date())

print("\n== BLOQUE NUEVO ==")
ma12 = pasajeros.rolling(window=12).mean()               # media de los 12 meses que terminan en t
tendencia = ma12.rolling(window=2).mean().shift(-6)      # 2x12: dos ventanas seguidas, centradas en t
print("tendencia['1955-07-01'] =", tendencia["1955-07-01"])
print("tendencia.isna().sum() =", int(tendencia.isna().sum()))
nan_pos = [i + 1 for i, v in enumerate(tendencia.isna()) if v]
print("posiciones NaN:", nan_pos)

# Contra los pesos explicitos 1/24, 1/12 x 11, 1/24
import numpy as np
w = np.r_[0.5, np.ones(11), 0.5] / 12
ref = pd.Series(np.convolve(pasajeros.values, w, mode="valid"), index=pasajeros.index[6:-6])
print("max |tendencia - pesos explicitos| =", float((tendencia.dropna() - ref).abs().max()))

# El grafico del bloque (sin plt.show())
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
pasajeros.plot(label="observado")
tendencia.plot(label="media movil 2x12")
plt.legend()
print("grafico construido sin error")
