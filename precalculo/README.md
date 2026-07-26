# Precálculos del material de Series de Tiempo

Esta carpeta **no se publica**: contiene el script que genera los datos y ajustes
que los capítulos HTML incrustan (los capítulos son autocontenidos, sin `fetch`).

## Uso

```bash
Rscript genera_datos.R
```

Requiere R base + `jsonlite` (sin `forecast` ni `fpp3`, a propósito). La descarga
de la TRM necesita internet; si falla, el script lo avisa y genera el resto.

## Salidas (`salidas/`)

| Archivo | Contenido | Se incrusta en |
|---|---|---|
| `datos_series.js` | `const SERIES_DATOS = {...}` con AirPassengers, co2, Nile, USAccDeaths y TRM mensual (promedio, SFC vía datos.gov.co) | Todos los capítulos (solo las series que cada uno use) |
| `datos_series.json` | Lo mismo en JSON puro (validación / otros usos) | — |
| `cap4_rejilla_arima.json` | Rejilla ARIMA(p,d,q), p,d,q ∈ {0,1,2}, sobre el Nilo: AICc/BIC, Ljung–Box, ACF de residuales. **El AICc solo se compara dentro del mismo d** (`mejor_aicc_por_d`) | Capítulo 4 (explorador de modelos) |
| `cap6_pronostico.json` | Modelo airline SARIMA(0,1,1)(0,1,1)[12] sobre log(AirPassengers): pronóstico con bandas 80/95, métricas vs. referencia (naive, snaive, media, deriva) y origen móvil (37 orígenes, h=12) | Capítulo 6 (simuladores de horizonte y backtesting) |

## Notas metodológicas

- AICc = AIC + 2k(k+1)/(n−k−1) con k = nº de coeficientes + 1 (σ²) y n efectivo = n − d.
- Intervalos del capítulo 6 construidos en escala log y transformados con `exp`
  (el pronóstico puntual es la mediana en la escala original).
- TRM: se descarta el mes en curso (incompleto); la fecha de consulta queda en
  los metadatos del archivo.
- Para regenerar tras cada semestre basta volver a correr el script; los números
  incrustados en los capítulos deben actualizarse copiando las salidas nuevas.
