# Precálculos del material de Series de Tiempo

Esta carpeta **no se publica**: contiene el script que genera los datos y ajustes
que los capítulos HTML incrustan (los capítulos son autocontenidos, sin `fetch`).

## Uso

```bash
Rscript genera_datos.R      # series base + capítulos 1, 4 y 6
Rscript genera_cap2.R       # capítulo 2 (lee la salida del anterior)
Rscript genera_cap3.R       # capítulo 3 (lee la TRM de la salida del primero)
Rscript genera_cap4.R       # capítulo 4 (lee Nilo, TRM y AirPassengers del primero)
Rscript genera_cap5.R       # capítulo 5 (lee AirPassengers, USAccDeaths, co2 y TRM del primero)
Rscript genera_soluciones.R # soluciones de los ejercicios propuestos
python3 verifica_cap5_python.py   # verificación cruzada R <-> Python del capítulo 5
```

**Todos los scripts fuerzan una configuración regional UTF-8 al arrancar.** R empieza con
`LC_CTYPE = "C"` y entonces `jsonlite` escribe las tildes como `<c3><ad>`; el navegador lee
eso como marcado desconocido y **se come la letra** («log(das del mes)»). El fallo se
encontró en la auditoría del capítulo 5 y afecta a cualquier cadena con tilde que viaje
al JSON. Si el aviso de `Sys.setlocale` salta, ejecuta con `LC_ALL=en_US.UTF-8 Rscript ...`.

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
| `cap3_arma.json` / `cap3_datos.js` | ACF y PACF **teóricas** (`ARMAacf`) y pesos ψ/π de 8 procesos canónicos; manchas solares 1770–1869 con AR(2) por Yule-Walker, CSS y ML, raíces y pseudo-periodo, rejilla de 11 modelos, diagnóstico de 4 candidatos y el análisis sobre √; log-retornos mensuales de la TRM | Capítulo 3 |
| `soluciones_ejercicios.json` | Soluciones **resueltas de verdad** de los ejercicios propuestos de los capítulos 1 y 2. El texto de las cajas "Solución" del HTML se contrasta contra este archivo; ninguna cifra se escribe de memoria | Capítulos 1 y 2 |
| `cap4_arima.json` / `cap4_datos.js` | Todo el capítulo 4: identificación del Nilo (correlogramas por d, ADF/KPSS/PP, `ndiffs` con las tres pruebas), rejilla de 27 modelos con AICc/BIC/Ljung–Box/ACF residual **y el módulo de las raíces** de cada uno, diagnóstico del ARIMA(1,1,1), el cambio de nivel de 1899 con su Monte Carlo y su malla de δ, sobrediferenciación, las trazas de `auto.arima` (18 pasos escalonada, 42 exhaustiva), las cuatro formas del pronóstico con bandas 80/95, los pesos ψ y σ_h, el caso TRM en niveles y el puente estacional sobre log(AirPassengers) | Capítulo 4 |
| `cap4_rejilla_arima.json` | Rejilla ARIMA(p,d,q) de la Fase 0, sobre el Nilo. **Superada por `cap4_arima.json`**, que la recalcula con más información; se conserva porque `genera_cap4.R` la usa como verificación cruzada (diferencia máxima de AICc: 0.0000 en los 27 modelos) | — (verificación) |
| `cap5_sarima.json` / `cap5_datos.js` | Todo el capítulo 5: firma estacional de 6 series con ACF/PACF a 36 rezagos, mapas mes × año de `AirPassengers` en cinco transformaciones, las cuatro combinaciones $(d, D)$, la sobrediferenciación estacional, ACF/PACF **teóricas** de 6 procesos estacionales canónicos, rejilla SARIMA de 36 modelos (todos con $d=1$, $D=1$) **con la ACF residual de cada uno**, el modelo *airline* con diagnóstico, pesos $\psi$ y pronóstico a 24 meses con bandas, `USAccDeaths` completo, la TRM como contraejemplo, regresores de calendario (días del mes y Semana Santa por el algoritmo de Meeus), regresión armónica $K=1..6$ y STL, y la comparativa de 8 métodos sobre una partición fija **más la verificación de 61 orígenes que la desmiente** | Capítulo 5 |
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
- **Ljung–Box no da lo mismo en R y en statsmodels sobre el mismo ajuste.** Los
  coeficientes, el AICc y el BIC coinciden hasta el último decimal, pero los
  residuales difieren en las `max(p,q)` primeras posiciones porque cada
  programa inicializa el filtro a su manera (sobre el AR(2) de las manchas, el
  primer residual es 21.06 en R y 52.54 en statsmodels). Como Q pondera mucho
  los primeros rezagos, el p-valor pasa de 0.0461 a 0.1085 y la conclusión se
  invierte. Descartando los `max(p,q)` primeros residuales, los dos dan 0.0232.
  Al comparar contrastes sobre residuales, compara primero los **residuales**.
- **`ar()` de R y `yule_walker()` de statsmodels usan divisores distintos**:
  R usa n y statsmodels `method="adjusted"` (n−k) por defecto. Para reproducir
  R hay que pedir `method="mle"`, que no es máxima verosimilitud: solo indica
  el divisor.
- **`BoxCox.lambda` exige datos estrictamente positivos.** Las manchas solares
  tienen un cero (1810), así que el λ se calcula sobre la serie desplazada una
  unidad: 0.3062 en vez del 0.3333 que sale —con aviso— sin desplazar.
- **`pacf(x)$acf` devuelve un array de tres dimensiones**, no un vector: si vas
  a citar la salida en el material, envuélvelo en `as.numeric()`.
- El λ de Guerrero descarta las observaciones **iniciales** sobrantes cuando n
  no es múltiplo de m (`x[(n - nyr*m + 1):n]`). Con la TRM (n = 138, m = 12) eso
  cambia el resultado de 0.2296 a 0.1288.
- AICc = AIC + 2k(k+1)/(n−k−1) con k = nº de coeficientes + 1 (σ²) y n efectivo = n − d.
- Intervalos del capítulo 6 construidos en escala log y transformados con `exp`
  (el pronóstico puntual es la mediana en la escala original).
- TRM: se descarta el mes en curso (incompleto); la fecha de consulta queda en
  los metadatos del archivo.
- **KPSS no usa el mismo truncamiento en R y en Python.** `tseries::kpss.test` usa
  ⌊4(n/100)^¼⌋ (= 4 con n = 100) y `statsmodels.kpss` con `nlags="legacy"` usa
  ⌊12(n/100)^¼⌋ (= 12). Sobre el Nilo eso da 0.9654 y 0.5497. Con `nlags=4`
  coinciden hasta el último decimal. Es la misma clase de trampa que la de
  `ndiffs`: al comparar dos programas, mira primero el truncamiento.
- **KPSS no distingue una raíz unitaria de un cambio de nivel.** Monte Carlo de
  1000 réplicas de ruido blanco estacionario: sin escalón rechaza el 4.8 % (su
  tamaño nominal); con un escalón de 1.95 desviaciones típicas, el 100 %. El ADF
  solo cae en el 0.5 % de los casos. Como `auto.arima` elige d con KPSS, una serie
  con un salto de nivel acaba diferenciada.
- **La firma algebraica de la sobrediferenciación es una raíz MA sobre el círculo
  unitario**, y es más fiable que la regla de la varianza: sobre `log(lynx)`
  diferenciar *reduce* la varianza un 58 % y aun así d = 1 sobra.
- **`statsmodels` no descuenta d en `nobs`**: informa 100 observaciones para todos
  los d, así que sus AIC/BIC parecen comparables entre distintos d cuando no lo
  son. En R el n efectivo sí baja (100, 99, 98).
- **`residuals()` de un ajuste con d ≥ 1 devuelve n valores, no n − d.** La banda
  del correlograma de residuales se calcula sobre esa longitud.
- **`jsonlite` escribe los `Inf` como `null`** (con `na = "null"`). Cualquier JS que
  lea esos campos tiene que tratar el `null` aparte: `Number(null)` es 0.
- **El AICc tampoco compara entre distintos $D$, y ahí el error es mayor que con $d$:**
  cada diferencia estacional cuesta $m$ observaciones, no una. Sobre `log(AirPassengers)`,
  un modelo con $D=0$ se evalúa sobre 143 observaciones y uno con $D=1$ sobre 131. La
  rejilla del capítulo 5 fija $d=1$ y $D=1$ en los 36 modelos por esa razón.
- **`nsdiffs()` cambió de prueba por defecto.** Desde `forecast` 8.x usa `test = "seas"`
  (fuerza estacional de STL); antes usaba OCSB. Sobre `log(AirPassengers)` y sobre
  `USAccDeaths`, `"seas"` devuelve 1 y `"ocsb"` devuelve 0. El test `"ch"` necesita el
  paquete `uroot`, que **no está instalado**.
- **Los operadores de diferencia conmutan; las pruebas que los eligen, no.**
  $\nabla\nabla_{12}y$ es idéntica en cualquier orden (diferencia máxima: 0), pero
  `ndiffs(USAccDeaths)` devuelve 0 sobre la serie cruda y 1 tras $\nabla_{12}$. Se decide
  **primero $D$ y después $d$**.
- **`statsmodels` no diferencia la serie**: mete $d$ y $D$ en el espacio de estados con un
  prior difuso. Informa `nobs` sin descontarlos (144 en vez de 131) y, en series cortas,
  mueve los coeficientes: sobre `USAccDeaths` ($n = 72$) $\hat\theta$ pasa de −0.4303 a
  −0.3924, y no es falta de convergencia. `simple_differencing=True` reproduce a R al cuarto
  decimal — pero entonces `get_forecast()` devuelve el pronóstico de la serie **diferenciada**:
  esa opción sirve para estimar como R, no para pronosticar.
- **`fourier()` de R y `Fourier` de `statsmodels` difieren en $K = m/2$:** R emite $m-1$
  columnas y Python $m$, y la de más (el seno de frecuencia $m/2$) es idénticamente cero.
  La matriz de Python queda con rango $m-1$ y hay que quitar esa columna a mano.
- **Una sola partición no decide entre métodos.** Sobre los últimos 24 meses de
  `AirPassengers` el SARIMA *airline* queda cuarto (RMSE 43.18); sobre 61 orígenes con
  $h = 12$ queda primero (16.81) y le gana a cada rival en más del 85 % de ellos.
- **`ets()` elige un modelo distinto según la escala.** Sobre la serie cruda selecciona
  ETS(M,A_d,M), con tendencia amortiguada; sobre los logaritmos, ETS(M,A,M). A 24 meses eso
  cambia el RMSE por un factor de 3.7. Al comparar con ETS hay que decir sobre qué escala.
- Para regenerar tras cada semestre basta volver a correr el script; los números
  incrustados en los capítulos deben actualizarse copiando las salidas nuevas.


## `genera_cap6.R` — Capítulo 6 (pronóstico y evaluación)

Genera `salidas/cap6_evaluacion.json` y `cap6_datos.js`. Contiene el motor de
**origen móvil** (`origen_movil` / `resume_om`), las siete métricas implementadas
a mano —verificadas contra `forecast::accuracy` con diferencia 0—, el puntaje de
**Winkler**, la prueba de **Diebold–Mariano** con respaldo a `varestimator =
"bartlett"`, y los tres casos (AirPassengers, TRM y Nilo).

Dos cosas que conviene saber antes de tocarlo:

- **Reconcilia con el capítulo 5 a propósito.** El ETS y el STL se ajustan
  exactamente como en `genera_cap5.R` (`ets(log x)` y `stlm` con
  `s.window = "periodic"`), porque aquel capítulo publica el RMSE medio de esos
  mismos métodos sobre estos mismos 61 orígenes. El script lo comprueba y lo
  imprime: si alguna vez deja de coincidir, una de las dos cifras está mal.
- **Dos maneras de agregar que no dan lo mismo.** `rmse` junta los 732 errores;
  `rmse_medio_origenes` promedia los 61 RMSE de cada origen. La segunda es menor
  por la desigualdad de Jensen. El capítulo 5 citó la segunda y el 6 usa la
  primera, y ambos lo dicen.

## `verifica_bloques_cap6.py` — el verificador de comentarios `#>`

Extrae los bloques `language-r` y `language-python` de las plantillas de
`ensamblado/cap6/` (o de cualquier HTML con `--html ruta`), los ejecuta
**encadenados** —como los ejecutaría un estudiante que sigue el capítulo de
arriba abajo— y comprueba que cada número anunciado en un comentario `#>`
aparezca en la salida real de ese bloque.

Se escribió porque, al auditar el capítulo 6, **11 de las 22 cifras escritas a
mano en esos comentarios estaban mal**, algunas por un factor de dos. El capítulo
se publicó con 390 de 390 verificadas. Sirve para cualquier capítulo:

```bash
python3 verifica_bloques_cap6.py --html ../Htmls_Series/capitulo-5-sarima.html
```
