# Precálculos del material de Series de Tiempo

Esta carpeta **no se publica**: contiene el script que genera los datos y ajustes
que los capítulos HTML incrustan (los capítulos son autocontenidos, sin `fetch`).

## Uso

```bash
Rscript genera_datos.R    # series base + capítulos 1, 4 y 6
Rscript genera_cap2.R     # capítulo 2 (lee la salida del anterior)
```

`genera_datos.R` requiere R base + `jsonlite` (sin `forecast` ni `fpp3`, a
propósito). La descarga de la TRM necesita internet; si falla, el script lo
avisa y genera el resto.

`genera_cap2.R` necesita además **`tseries` y `forecast`**, porque el capítulo 2
enseña `adf.test`, `kpss.test`, `ndiffs`, `nsdiffs` y `BoxCox.lambda`, y las
cifras del material deben salir de las mismas funciones que correrán los
estudiantes. Va en un script aparte a propósito: `genera_datos.R` vuelve a
descargar la TRM y a reajustar los 37 modelos del origen móvil del capítulo 6,
y no hay razón para pagar eso cada vez que se toca un correlograma.
`genera_cap2.R` no descarga nada: lee la TRM de `salidas/datos_series.json`.

## Salidas (`salidas/`)

| Archivo | Contenido | Se incrusta en |
|---|---|---|
| `datos_series.js` | `const SERIES_DATOS = {...}` con AirPassengers, co2, Nile, USAccDeaths y TRM mensual (promedio, SFC vía datos.gov.co) | Todos los capítulos (solo las series que cada uno use) |
| `datos_series.json` | Lo mismo en JSON puro (validación / otros usos) | — |
| `cap2_estacionariedad.json` / `cap2_datos.js` | 8 series de trabajo con su ACF y PACF (24 rezagos), ADF y KPSS (nivel y tendencia), `ndiffs`/`nsdiffs`, λ de Guerrero, tabla de sobrediferenciación y el Monte Carlo de la trampa del ADF estacional | Capítulo 2 |
| `cap4_rejilla_arima.json` | Rejilla ARIMA(p,d,q), p,d,q ∈ {0,1,2}, sobre el Nilo: AICc/BIC, Ljung–Box, ACF de residuales. **El AICc solo se compara dentro del mismo d** (`mejor_aicc_por_d`) | Capítulo 4 (explorador de modelos) |
| `cap6_pronostico.json` | Modelo airline SARIMA(0,1,1)(0,1,1)[12] sobre log(AirPassengers): pronóstico con bandas 80/95, métricas vs. referencia (naive, snaive, media, deriva) y origen móvil (37 orígenes, h=12) | Capítulo 6 (simuladores de horizonte y backtesting) |

## Notas metodológicas

- **`ndiffs()` no usa `tseries::kpss.test`.** Llama por dentro a `urca::ur.kpss`
  con truncamiento ⌊3√n/13⌋, mientras que `kpss.test` usa ⌊4(n/100)^¼⌋. Sobre
  ∇₁₂log(AirPassengers) eso da d = 1 y d = 0 respectivamente. No es un bug de
  ninguna de las dos: al comparar salidas, mira siempre qué truncamiento usan.
- **El ADF de R y el de statsmodels dan el mismo estadístico y distinto
  p-valor.** `tseries::adf.test` interpola en las tablas de Banerjee et al.
  (1993); `statsmodels.adfuller`, en la superficie de respuesta de MacKinnon.
  Para reproducir R desde Python hay que pedir `regression="ct"`,
  `maxlag=trunc((n-1)^(1/3))` y `autolag=None`.
- **`diff(x, differences = 0)` es un error en R**, no la identidad. Cualquier
  bucle sobre d = 0, 1, 2… tiene que tratar el caso d = 0 aparte.
- El λ de Guerrero descarta las observaciones **iniciales** sobrantes cuando n
  no es múltiplo de m (`x[(n - nyr*m + 1):n]`). Con la TRM (n = 138, m = 12) eso
  cambia el resultado de 0.2296 a 0.1288.
- AICc = AIC + 2k(k+1)/(n−k−1) con k = nº de coeficientes + 1 (σ²) y n efectivo = n − d.
- Intervalos del capítulo 6 construidos en escala log y transformados con `exp`
  (el pronóstico puntual es la mediana en la escala original).
- TRM: se descarta el mes en curso (incompleto); la fecha de consulta queda en
  los metadatos del archivo.
- Para regenerar tras cada semestre basta volver a correr el script; los números
  incrustados en los capítulos deben actualizarse copiando las salidas nuevas.
