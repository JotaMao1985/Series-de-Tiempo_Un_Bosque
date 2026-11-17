# R1 · Registro de cambios · Capítulo 2 «Estacionariedad, ACF y PACF»

Ronda R1 del `PLAN_Mejora_Cap2.md` (tareas T1.1–T1.4; decisiones D2, D3 y D5). Fecha: 2026-11-16. Un solo
redactor. Especificación: `diagnostico/cap2/par_academico.md` (37 hallazgos) y la tabla de errores del plan. Sin
commit.

**Archivos tocados**

| archivo | qué |
|---|---|
| `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` | solo dentro de los `<template id="module-N">` (M2–M9) y de `AUTOEVALUACIONES['cap2']`. Nada del armazón: `ensambla_cap3.py` sigue diciendo «reproducible byte a byte» |
| `precalculo/genera_cap2.R` | 19 líneas nuevas: escribe la copia fija de la TRM. Sus otras dos salidas no cambian (ver T1.4) |
| `Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv` | **nuevo**, escrito por `genera_cap2.R`: 138 filas `mes,trm` |
| `precalculo/trm_mensual_2015-01_2026-06.csv` | **nuevo, enlace simbólico** al anterior: es lo que encuentra el verificador de bloques (ver T1.4) |
| `diagnostico/cap2/comprobaciones/r1_*` | guiones y salidas de esta ronda |

**Recuento sobre los 37 hallazgos del par:** 7 errores corregidos · 20 imprecisiones: 18 corregidas y 2 dejadas
(una para la R3, otra para la R4) · 3 lagunas: 2 corregidas y 1 para la R4 · 4 divergencias corregidas · 3 «sin
comprobar»: 1 comprobado, 1 reescrito y 1 para la R4. Más los dos del plan (truncamiento de `ndiffs`, `ywm`) y
**5 cifras con doble redondeo** que el diagnóstico no vio.

**Verificadores al cerrar**

- `MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-2-…html` →
  **210 de 210 cifras, 0 bloques con discrepancias** (antes: 0 de 0). 12 bloques de R y 9 de Python.
  Salida en `comprobaciones/r1_verifica_bloques.out`.
- `python3 precalculo/verifica_todo.py` → **11 verificadores en verde** (Tailwind tardó 113 s).
- `python3 ensamblado/ensambla_cap3.py` → reproducible byte a byte. `audita_posicion_correcta.py` → en verde.
- En el navegador, por HTTP (`htmls-series`, 8731): los nueve módulos cargan, 0 errores de consola, 0
  `.katex-error`, ningún `.katex` dentro de un `<pre>`, 8 preguntas en el quiz, y
  `datos/trm_mensual_2015-01_2026-06.csv` responde 200 con 139 líneas.

**Entorno:** R 4.6.0 (tseries 0.10.62, forecast 9.0.2, urca 1.3.4, fabletools 0.8.0, fpp3 1.0.3); Python 3 con
statsmodels 0.14.6, scipy 1.15.3, numpy 2.2.6, pandas 2.3.3. `pmdarima` no está en el entorno: para comprobar lo
que el capítulo dice de él se instaló la 2.1.1 en un entorno virtual desechable, fuera del repo.

**Guiones de esta ronda** (`diagnostico/cap2/comprobaciones/`; cada `.out` es la salida íntegra)

| guion | salida | qué comprueba |
|---|---|---|
| `r1_errores.R` | `r1_errores.out` | los siete errores y las imprecisiones con cifra: ∇TRM, AR(1) sobre el ruido del M2, ρ₁(∇y), varianza por d, la serie ∇₁₂ log y, KPSS de tendencia, ADF por k, Box–Cox, ejercicios y quiz |
| `r1_python.py` | `r1_python.out` | `ywm` frente a `ldb`; `scipy.stats.boxcox` frente al Guerrero de statsmodels; KPSS con los dos truncamientos; `pmdarima` (`ndiffs`, `nsdiffs`, `BoxCoxEndogTransformer`) |
| `r1_software.R` | `r1_software.out` | lo que la prosa afirma del software, leído en el código de R: la regresión de `adf.test`, los truncamientos, el `BoxCox` con signo, el bloque de `guer.cv` |
| `r1_redondeo.R` | `r1_redondeo.out` | 54 cifras publicadas a 3 decimales contra su valor exacto; y que el CSV publicado es idéntico a `datos_series.json` |
| `r1_simulador_ar1.js` | `r1_simulador_ar1.out` | las dos cifras del simulador del M5 que cita la nota, con las funciones extraídas del HTML |
| `r1_bloques_publicados.py` | `r1_bloques_publicados.out` | los 21 bloques tal como quedaron, con la salida íntegra de cada uno; exige que cada línea `#>` aparezca **literal**, no solo sus números: 86 de 86 |
| `r1_bloques_sueltos.py` | `r1_bloques_sueltos.out` | cada bloque de Python solo, en una carpeta vacía (8 de 8); y el bloque de R del M6 leyendo la TRM por HTTP (34 de 34) |
| — | `r1_genera_cap2.out` | la ejecución de `genera_cap2.R` con la que se escribió el CSV |
| — | `r1_verifica_bloques.out` | la salida del verificador de bloques al cerrar |

No se añadió ningún `<cite>`, ningún `data-afirma`, ningún autor, año ni sección. Se **quitaron** dos atribuciones
que no se sostenían (FPP3 en el M8 y en la P8).

Las líneas «orig.» son las del commit `e1ebf32`; «ahora», las del archivo tras la ronda.

---

## T1.1 · Los siete errores

| # | módulo | orig. | qué decía | qué dice ahora | evidencia |
|---|---|---|---|---|---|
| 1 | M3 | 2515–2517 | Fila «Decaimiento rápido (exponencial)»: «∇TRM: r₁ = 0.088, todo lo demás dentro de la banda» | «AR(1) con φ = 0.5 simulado sobre ese mismo ruido (Módulo 5): r₁ = 0.504, r₂ = 0.376, r₃ = 0.268, r₄ = 0.176, y r₅ = 0.078 ya está dentro de la banda ±0.139» (ahora 2526). El bloque de R del M5 imprime esas cinco cifras bajo `#>`, de modo que quedan vigiladas | `r1_errores.out` §E1: ∇TRM tiene r₈ = −0.1903 fuera de ±0.1675 y r₁ dentro; AR(1) φ = 0.5 sobre `set.seed(2026); rnorm(200)` → 0.5042 0.3759 0.2681 0.1760 0.0779 (teórico 0.5, 0.25, 0.125…). **Ojo:** en esa muestra los rezagos 20–24 vuelven a asomar (−0.15 a −0.19); por eso la celda no dice «todo lo demás dentro» |
| 2 | M5 | 2835–2837 | «Con la primera diferencia activada, cualquier φ produce algo que ya se parece a ruido blanco…» | «…el resultado depende de φ. Con φ = 1 queda el ruido de partida, porque ∇y_t = ε_t. Con φ < 1 la serie ya era estacionaria y la diferencia sobra; lo delata una autocorrelación negativa en el rezago 1, que en teoría vale −(1−φ)/2: −0.25 con φ = 0.5 y −0.5 con φ = 0 (el simulador marca −0.252 y −0.506). Con φ > 1 la diferencia no arregla nada…» (ahora 2857) | `r1_errores.out` §E2: `ARMAacf(ar = 0.5, ma = -1)` → −0.25; `diff(ar1(1, e))` es `e[-1]`. `r1_simulador_ar1.out`: el simulador (su propio ruido, JS) da −0.2522 y −0.5063; con φ = 1.05 y ∇, 24 de 24 rezagos fuera |
| 3 | M6 | 3217–3221 | Comentario Python: «La conclusion es la misma en los dos casos; solo cambia el tercer decimal» | «De ahi 0.6132 frente a 0.5855, y 0.0129 frente a 0.0172: la diferencia llega a las centesimas. La conclusion es la misma en los dos casos, pero un p-valor de R y uno de statsmodels no se comparan entre si» | `r1_bloques_publicados.out`, bloques #8 y #9: 0.5855 (R) y 0.6132 (statsmodels) |
| 4 | M7 | 3398–3399, 3455, quiz | «La varianza. Cada diferencia útil la reduce; la primera diferencia de más la **aumenta**. El mínimo señala el d correcto»; «Diferenciar de más… infla la varianza»; P4: «las tres van juntas y son la misma cosa» | (a) Señal 3: «La varianza, como señal de apoyo. […] si al diferenciar la varianza sube, esa diferencia sobraba. La señal no funciona al revés…» (3460). (b) Párrafo nuevo tras la tabla: Var(∇y) = 2(1−ρ₁)Var(y); el AR(1) con φ = 0.8: `ndiffs` = 0 y la varianza baja de 2.497 a 1.033 (3515). (c) Recuadro de sobrediferenciación: «introduce autocorrelación que no estaba […] y, salvo en series muy persistentes, infla la varianza»; el rastro es «una autocorrelación negativa en el rezago 1 que se acerca a −0.5»; y un tercer párrafo con el caso en que el rastro es débil (r₁ = −0.148) (3526–3540). (d) Quiz P4, `retroAcierto`: «Las tres salen de la misma cuenta […] Pero no pesan igual: una varianza que sube delata la diferencia de más, y una que baja no la descarta…». (e) Quiz P7: «además de fabricar autocorrelación que no estaba» en lugar de «además de inflar la varianza». (f) Ejercicio 3: «Cuando una diferencia sobra, lo habitual es que la varianza suba y que r₁ se acerque a −0.5; aquí la varianza baja y r₁ se queda en −0.353». (g) El simulador ya no dice «y —sobre todo— la varianza» | `r1_errores.out` §E4; el ejemplo está **en el bloque de R del M7**, con su salida: `set.seed(1); y <- arima.sim(list(ar = 0.8), n = 200)` → `ndiffs(y)` 0, varianzas 2.497 y 1.033, r₁(∇y) = −0.148 |
| 5 | M7 | 3467–3490 | Párrafo en orden regular → estacional y recuadro «Sobre esa misma serie ∇₁₂ log y […] el pico de r₁₂ = 0.841 pide la diferencia estacional, y tras aplicarla la serie ya está lista» | Párrafo partido en dos (3544–3552): primero el orden recomendado (`nsdiffs` 1 → ∇₁₂ log y → `ndiffs` 1 → ∇∇₁₂ log y), después «El orden contrario enseña por qué no basta con las pruebas» con lo que ya decía. Recuadro (3557–3575): «Sobre ∇₁₂ log y (n = 132), la serie que deja la diferencia estacional…»; la explicación del truncamiento no cambia; moraleja: «Aquí el correlograma desempata a favor de `ndiffs()`: la ACF de ∇₁₂ log y baja despacio (r₁ = 0.714, r₂ = 0.623, r₃ = 0.480, con los ocho primeros rezagos fuera de la banda) […] Al aplicar la diferencia regular la varianza cae de 0.0038 a 0.0021 y r₁ queda en −0.341, lejos de −0.5: la diferencia hacía falta. El resultado es d = 1 y D = 1, lo mismo que decide el pipeline del Módulo 9» | `r1_errores.out` §E5: `kpss.test(d12)` 0.3682, l = 4, p = 0.0909; `ndiffs(d12)` 1; `ur.kpss` con 2 rezagos 0.5367 > 0.463; ACF 0.7137 0.6231 0.4804…, fuera 1–8 y 12; varianzas 0.00380 y 0.00210; r₁ de ∇∇₁₂ = −0.3411. El bloque de R del M7 imprime ahora `nsdiffs(log AP)`, `ndiffs(d12)` y `kpss.test(d12)` |
| 6 | M8 | 3675–3677 | «el equivalente a BoxCox.lambda(method="guerrero") es: `from pmdarima.preprocessing import BoxCoxEndogTransformer`» | Se quitó. El bloque calcula ahora los dos λ y los imprime: `scipy.stats.boxcox` → 0.148 (máxima verosimilitud) y `BoxCox().transform_boxcox(pasajeros.values, method="guerrero", window_length=12)` de `statsmodels.base.transform` → **−0.2947**, el de R | `r1_python.out` §2 y §4: el Guerrero de statsmodels da −0.2947 (su `_guerrero_cv` está copiado en la salida); `BoxCoxEndogTransformer().fit(pasajeros).lam1_` = 0.148, igual que scipy, y su `fit` llama a `stats.boxcox` (pmdarima 2.1.1, ejecutado) |
| 7 | M9 | 4002–4003 | «Seis preguntas… Cada opción tiene su explicación» | «Ocho preguntas para comprobar lo esencial. En las de una sola respuesta, cada opción tiene su explicación […]. En las numéricas y en la de selección múltiple la explicación llega al comprobar la respuesta» (4167) | lectura de `AUTOEVALUACIONES['cap2']`: 8 objetos; P2 y P7 `numerica`, P4 `multiple`; en el navegador, 8 preguntas |

**Los dos del plan**

- **Truncamiento (orig. 3893).** El comentario Python decía «floor(3*sqrt(n)/13), el de urca::ur.kpss». Ahora:
  «el truncamiento de rezagos que ndiffs() le pasa a urca::ur.kpss: floor(3*sqrt(n)/13)» (4054).
  `r1_software.out`: `kpss_wrap <- function(..., use.lag = trunc(3 * sqrt(length(x))/13))`; `ur.kpss` por
  defecto usa `trunc(4 * (n/100)^0.25)`.
- **`ywm` (orig. 2654, 2742).** Resultado del desarrollo (2666): «Esta es la recursión que implementan `pacf()`
  de R, el método `ldb` de statsmodels y `calcularPACF()` […]. El método `ywm` de statsmodels, que es el que usa
  el código de este módulo, llega a los mismos valores por el otro camino: resuelve el sistema de Yule–Walker del
  paso 1 para cada rezago». El comentario del bloque Python dice lo mismo y el bloque imprime
  `np.allclose(ywm, ldb)` → `True`. `r1_python.out` §1: máx|ywm − ldb| = 1.1e-14; `pacf_yw` llama a
  `yule_walker` y no a `levinson_durbin`; `pacf(method="ldb")` sí. La nota «Verificación» (orig. 2665) no se
  tocó: solo dice que los números coinciden, y coinciden.

---

## T1.2 · Imprecisiones, lagunas, divergencias y «sin comprobar», una por una

En el orden del informe del par.

| módulo | orig. | severidad | estado | qué quedó | evidencia / motivo |
|---|---|---|---|---|---|
| M2 | 2358–2360 | imprecisión | corregido | «Si la serie es ruido blanco **independiente** —i.i.d., no solo incorrelado— […] Y si el ruido es incorrelado pero no independiente —el caso de la advertencia de arriba—, la varianza de r_k deja de ser 1/T y la banda ya no cubre el 95 %» | En voz propia, sin cita. El par leyó la condición en Shumway y Stoffer; **la R4 debe darle su fuente** |
| M2 | 2361–2362 | divergencia | corregido | «Una barra que apenas asoma fuera de la banda no es evidencia de nada; una barra muy grande, o un patrón, sí» | coherencia con lo que el par leyó en FPP3 §2.9; sin cita |
| M4 | 2654, 2665, 2742 | imprecisión | corregido | ver «Los dos del plan» | `r1_python.out` §1 |
| M4 | 2697–2699 | divergencia | corregido | «…→ modelo ARMA(p,q), y en ese caso los gráficos ya no dicen cuánto valen p y q» | — |
| M5 | 2850–2852 | imprecisión | corregido | «El término ct es una recta, y la suma Σε_i que se le añade es la **tendencia estocástica**: la serie sube en promedio c por periodo, pero no vuelve a esa recta, porque la distancia que la separa de ella es una caminata aleatoria cuya varianza, tσ², no deja de crecer» | sale de la fórmula de la línea anterior |
| M5 | 2858–2860 | imprecisión | corregido | «Aplicar el tratamiento equivocado tiene un costo en las dos direcciones: quitar una recta a una caminata deja los residuales igual de no estacionarios, y diferenciar una serie con tendencia determinista sí la vuelve estacionaria, pero sobrediferenciada —∇y_t = b + ε_t − ε_{t−1}, con el problema que describe el Módulo 7—» | álgebra: ∇(a + bt + ε_t) |
| M6 | 2949–2953, 2984–2986, 3057–3058 | imprecisión | corregido | Definición del ADF: «H₁: γ < 0 (estacionaria alrededor de la tendencia α + βt que la propia regresión incluye; sin el término βt, estacionaria en nivel) […] `adf.test()` de R estima siempre la regresión completa, con constante y tendencia». Párrafo nuevo tras la tabla de la TRM: «Un detalle de especificación: […] el KPSS de tendencia (`null = "Trend"`) también rechaza la estacionariedad de la TRM (0.273, p < 0.01) y tampoco la rechaza en su diferencia (0.070, p > 0.10)». AirPassengers: «proclama que la serie es estacionaria alrededor de una tendencia» | `r1_software.out`: `lm(yt ~ xt1 + 1 + tt + yt1)`; `r1_errores.out` §M6: 0.2730 (p 0.01) y 0.0699 (p 0.10). El bloque de R imprime `kpss.test(trm, null = "Trend")`. **No se tocó** la tabla de cuatro combinaciones (orig. 2973–3004): con el párrafo nuevo ya se dice qué alternativa contrasta cada una; rehacerla es estructura (R3) |
| M6 | 3056–3058 / 3071–3107 | laguna | corregido | «Sobre la serie sin transformar, con k = 12 el estadístico pasa de −7.32 a −1.51 (p = 0.781). La tabla lo recorre sobre `log(AirPassengers)`, que es la serie con la que se trabaja de aquí en adelante y en la que el k = 5 por defecto da −6.42» | `r1_errores.out`: `adf.test(AP, k = 12)` −1.5094 (0.7807); el bloque de R lo imprime |
| M6 | 3137–3138 | imprecisión | corregido | «Las funciones `nsdiffs()` y `ndiffs()` del Módulo 7 hacen esos dos contrastes, pero el orden lo pone quien las usa: primero `nsdiffs()`, se diferencia, y después `ndiffs()` sobre la serie ya diferenciada» | — |
| M7 | 3467–3473 | imprecisión | corregido | ver error 5 | — |
| M7 | 3459–3460; quiz | imprecisión | corregido | «un MA(1) —con la convención y_t = ε_t + θε_{t−1}, θ = −1; con la convención del signo contrario, θ = 1—». En la P4 la opción dice «Queda inducido un MA(1), ε_t − ε_{t−1}, que además no es invertible» (misma posición, sigue siendo correcta) | no se nombra a ningún autor |
| M7, M8 | 3531, 3678 | laguna | corregido | los bloques de Python de los M7, M8 y M9 crean `pasajeros` | `r1_bloques_sueltos.out`: los ocho bloques corren solos en una carpeta vacía |
| M7 | 3537–3540 | sin comprobar | comprobado | El comentario dice ahora «estan en pmdarima, que no forma parte del entorno del curso. Con pmdarima 2.1.1: `ndiffs(lap, test="kpss") -> 1`, `nsdiffs(lap, m=12, test="ocsb") -> 1`» | `r1_python.out` §4, ejecutado con pmdarima 2.1.1. Siguen siendo comentarios: el verificador no los ejecuta |
| M8 | 3633; quiz 6050 | divergencia | corregido | Se quitó «FPP3 hace la misma recomendación». P8: «pero este capítulo recomienda usar el logaritmo» | el par leyó FPP3 §3.1: no respalda la recomendación entera |
| M8 | 3588 | divergencia | corregido | «Así escrita exige y_t > 0; `BoxCox()` de `forecast` y `box_cox()` de `fpp3` usan una variante con el signo de y_t que admite valores negativos cuando λ > 0» | `r1_software.out`: los dos cuerpos, con `sign(x) * abs(x)^lambda`; el bloque de R imprime `BoxCox(c(-2, 4), 0.5)` → −4.83, 2.00 |
| M8 | 3632; quiz 6069 | imprecisión | corregido | «por dos razones»: se quitó «(3) deshacer la transformación es trivial». P8: la opción correcta es «Porque λ = 0 es interpretable y el óptimo es a su vez una estimación con incertidumbre» (misma posición) y la pista termina «…y en cuánto se puede confiar en un λ estimado con 12 bloques» | `r1_errores.out`: `InvBoxCox` es exacta (1.8e-12) con cualquier λ |
| M8 | 3683; 3637–3638 | imprecisión | corregido | Comentario: «Sobre los datos la vuelta con exp() es exacta; el sesgo aparece al deshacer un PRONOSTICO». Prosa: «…la mediana del pronóstico, no la media —siempre que la distribución del pronóstico en la escala transformada sea simétrica—» | `r1_python.out`: máx|exp(log y) − y| = 2.3e-13 |
| M9 | 3859; 3876–3878 | imprecisión | **dejado · R3** | El pipeline de R sigue con `if (abs(lambda) < 0.25) log(y) else BoxCox(y, lambda)` | Es la decisión D6 y la tarea T3.3. Sus salidas bajo `#>` (−0.2947, 9.17e-05, 0.1, 131) quedan vigiladas: cuando la R3 cambie el pipeline, el verificador obligará a actualizarlas |
| M9 | 3787 | imprecisión | corregido | Paso 2, «Con qué»: «en Python, `np.log()` o, para el λ de Guerrero, `BoxCox().transform_boxcox()` de statsmodels: `scipy.stats.boxcox` estima λ por máxima verosimilitud y da otro valor» | `r1_python.out` §2 |
| M9 | 3905; 3921 | imprecisión | corregido | Comentarios: «Aqui D no se decide con una prueba: se fija en 1 porque la serie es estacional (statsmodels no trae un equivalente de nsdiffs)» y «d coincide con la version en R; D tambien, pero aqui estaba puesto a mano» | — |
| M9 | 3944–3946 | sin comprobar | reescrito | «un modelo basado en árboles no puede predecir valores fuera del rango que vio al entrenarse, así que una serie con tendencia lo deja sin respuesta; diferenciarla antes le quita ese problema» | Se quitó lo de las redes recurrentes y el «mucho mejor». Lo que queda es un argumento, no un resultado empírico; **la R4 debe declararlo `propia` o darle fuente** |
| M9 ej. 1 | 4043–4044 | imprecisión | corregido | Comentario: «Entre el minimo y el maximo de toda la muestra hay solo un 15.9 % de la media: el nivel del CO2 apenas cambia de escala» | `r1_errores.out`: 0.1592; por medias anuales, +15.2 % |
| M9 ej. 2 | 4116–4119 | imprecisión | corregido | «La diferencia de fondo entre los dos experimentos es que […] (también cambian la longitud, 144 frente a 100, y la semilla; la comparación limpia está en el propio Monte Carlo del Módulo 6, que con amplitud 0 rechaza el 3.2 %)» | `cap2_estacionariedad.json`: amplitud 0 → 3.2 |
| M9 ej. 3 | 4139–4140 | imprecisión | corregido | «…relee la «Regla de trabajo» del Módulo 6» | `r1_errores.out`: `ndiffs(y)` 0, `nsdiffs(y)` 1, `ndiffs(diff(y, 12))` 1 |
| M9 ej. 4 | 4221–4223 | imprecisión | corregido | «Lo esperable es que unos meses más no cambien el veredicto: con 138 meses la evidencia de la raíz unitaria es abundante. Pero el resultado de una prueba sí depende de la ventana, sobre todo cuando es corta: con la misma copia recortada a los 54 meses que van desde enero de 2022, el ADF da p = 0.071…» | El bloque nuevo del ejercicio imprime 54 y 0.071 sobre la copia fija |
| quiz P3 | 5949 | imprecisión | corregido | «Si fuera ruido blanco, se esperaría que una o dos de las 24 barras asomaran fuera de la banda por puro azar. Aquí se salen 10 de 24, y la del rezago 12 muchísimo: r₁₂ = 0.841 frente a una banda de ±0.164» | `r1_errores.out`: fuera 1 4 8 11 12 13 16 20 23 24 |
| quiz P8 | 6066 | imprecisión | corregido | «Con series anuales, sin ciclo, `BoxCox.lambda()` toma bloques de 2 observaciones» | `r1_software.out`: `period <- round(max(nonseasonal.length, frequency(x)))`, `nonseasonal.length` = 2 |
| lecturas | 4274–4275 | imprecisión | **dejado · R4** | «secc. 3.1–3.2» sigue | Corregir una sección es escribir una sección: T4.2 («lecturas del M9 con secciones exactas») |
| lecturas | 4272–4283 | laguna | **dejado · R4** | — | añadir lecturas es añadir fuentes |
| lecturas | 4277–4278 | sin comprobar | **dejado · R4** | — | depende de la 4.ª edición de Shumway y Stoffer (T4.1) |

---

## T1.3 · Salidas bajo `#>`

Los 19 bloques llevan bajo cada línea que imprime su salida real; con los dos nuevos del ejercicio 4 son 21
(12 de R, 9 de Python) y 86 líneas `#>`. Criterios:

- La salida se copió de la ejecución encadenada del verificador, no se escribió. `r1_bloques_publicados.py` exige
  que cada línea `#>` esté literal en la salida de su bloque: 86 de 86.
- De las pruebas (`adf.test`, `kpss.test`) se copia **la línea del estadístico** y, si lo hay, el aviso, abreviado
  como `#> Warning: p-value smaller than printed p-value`. El bloque del M6 lo declara en un comentario. Copiar
  las cinco o seis líneas de cada `htest` habría triplicado el bloque.
- Para que la salida sea la que el comentario anunciaba se redondeó en el código lo que antes se redondeaba en el
  comentario: `round(1.96 / sqrt(length(e)), 4)`, `round(sapply(...), 5)`, etc. En Python, `round(float(est), 4)`:
  con numpy 2 un `np.float64` dentro de una tupla se imprime `np.float64(-1.9783)`.
- `max(abs(y2 - AirPassengers))` pasó a `… < 1e-9` → `TRUE` (en R y en Python): el residuo exacto (1.8e-12,
  2.3e-13) es ruido de máquina y no conviene publicarlo como cifra.
- El bloque de Python del M2 avisa de que `default_rng(2026)` no da los números de `set.seed(2026)` de R: allí
  sale 1 rezago fuera de la banda y en R, 0.

Añadidos al código que no eran salidas, todos para que una cifra de la prosa quede vigilada: en el M5 (R) la ACF
del AR(1) con φ = 0.5; en el M6 (R) `kpss.test(trm, null = "Trend")` y `adf.test(AirPassengers, k = 12)`; en el
M7 (R) `length(dd)`, `ndiffs(d12)`, `kpss.test(d12)` y el AR(1) con φ = 0.8; en el M7 (Python) `len(dd)`; en el
M8 (R) el `BoxCox` con negativos y en el M8 (Python) el λ de Guerrero; en el M4 (Python) `np.allclose(ywm, ldb)`.
Los ejercicios 1 a 3 conservan su código; solo cambian los redondeos y los comentarios que hacían de salida.

**Lo que el verificador no vigila.** (1) Las tablas y la prosa: el verificador compara las líneas `#>` con la
salida, no la prosa con las líneas `#>`. (2) Los comentarios de `pmdarima`. (3) Las dos cifras del simulador en
la nota del M5 (salen del JS; `r1_simulador_ar1.js`). (4) Las salidas del ejercicio 4 con la serie al día, que no
llevan `#>` a propósito.

---

## T1.4 · La TRM congelada (D3)

**Qué hace ahora el código.** El bloque del M6, en R y en Python, lee
`trm_mensual_2015-01_2026-06.csv`: de la carpeta de trabajo si el archivo está ahí y, si no, de
`https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/trm_mensual_2015-01_2026-06.csv` (la URL del sitio
está en `Htmls_Series/README.md`). La descarga de datos.gov.co se mudó entera al ejercicio 4 («Cómo
comprobarlo»), en R y en Python, con la comparación contra la copia fija; la pista del ejercicio ya no remite al
bloque del M6.

**De dónde sale el CSV.** Lo escribe `genera_cap2.R` (19 líneas nuevas, tras leer la TRM de
`salidas/datos_series.json`) en `Htmls_Series/datos/`. El nombre lleva el primer y el último mes, calculados de
la serie: si `genera_datos.R` trae una TRM más larga, el archivo cambia de nombre y el capítulo deja de
encontrarlo, que es lo que debe pasar. `r1_redondeo.out`: el CSV es idéntico a `datos_series.json` (138 valores).

**Las demás salidas del generador.** Tras ejecutarlo, `cap2_estacionariedad.json` y `cap2_datos.js` salieron
iguales a los del repo **salvo la fecha `generado`** (2026-07-26 → 2026-11-16; comprobado sustituyendo la fecha
y comparando el resto). Se restauraron con `git checkout --` para que queden byte a byte como estaban: el
`DATOS_CAP2` incrustado en el HTML lleva la fecha de julio y cambiarla era tocar el armazón.

**Cómo lo resuelve el verificador de bloques.** Ejecuta con `cwd = precalculo/`, y allí
`precalculo/trm_mensual_2015-01_2026-06.csv` es un **enlace simbólico** a `../Htmls_Series/datos/…`. Así el
verificador lee el mismo archivo que se publica, sin duplicarlo y sin tocar el verificador. El camino de la URL
no lo recorre nunca; `r1_bloques_sueltos.py` lo prueba sirviendo `Htmls_Series/` en un puerto local y
sustituyendo la base de la URL: el bloque de R da sus 34 cifras y el de Python sus 9.

**`pasajeros`.** Los bloques de Python de los M3, M4, M7, M8 y M9 lo crean. El único bloque de Python que depende
de otro es el del ejercicio 4, que usa `adf_como_en_r()` del M6 y lo dice en un comentario.

---

## Lo que el diagnóstico no vio

1. **Cinco cifras con doble redondeo.** El JSON guarda 4 decimales y la página redondeó ese valor, no el exacto.
   `r1_redondeo.out` compara 54 cifras; fallaban cinco, todas corregidas:

   | dónde | publicado | exacto | ahora |
   |---|---|---|---|
   | M6, tabla de la TRM, p del ADF (y ejercicio 4) | 0.586 | 0.585490 | 0.585 |
   | M6, tabla de la TRM, KPSS de ∇TRM | 0.242 | 0.241468 | 0.241 |
   | M6, tabla de k, k = 5 | −6.422 | −6.421458 | −6.421 |
   | M6, tabla de k, k = 12 | −1.533 | −1.532489 | −1.532 |
   | ejercicio 3, r₁ de la serie original | 0.708 | 0.707471 | 0.707 |

   (La salida marca una sexta línea, «ADF AP, k = 12», solo porque la prosa nueva la da a dos decimales, −1.51;
   el valor es −1.5094. Y se ejecutó antes de corregir: la columna «publicado» es la de `e1ebf32`.)
   La fuente de las diapositivas del capítulo 4 (`diapositivas/fuentes/capitulo_4.md`, l. 696) ya había notado
   las dos primeras. El «ninguna cifra publicada está mal calculada» del diagnóstico es cierto a 4 decimales.
2. **La prosa del M7 prometía un `length()` que el código no tenía** («la cifra que devuelve `length()` sobre la
   serie doblemente diferenciada en el código de más abajo», orig. 3357). El bloque imprime ahora `length(dd)`.
3. **El verificador de bloques atribuye los avisos al último bloque.** Junta `stdout + stderr`, y todo el stderr
   de la sesión cae tras el último separador. Un número que solo aparezca en un aviso no se comprobaría en su
   bloque. No se tocó el verificador; `r1_bloques_publicados.py` busca cada aviso en la sesión entera.
4. **`BoxCox()` imprime su atributo `lambda`**; el bloque usa `as.numeric()` para que la salida sea una línea.
5. **Con el ruido del capítulo, el AR(1) con φ = 0.8 no sirve de contraejemplo:** `ndiffs` devuelve 1 (KPSS
   p = 0.023), porque en 200 valores una serie tan persistente ya confunde a la prueba. Por eso el ejemplo del M7
   es el de la sesión maestra (`set.seed(1)`, `arima.sim`), donde `ndiffs` = 0. Es, de paso, el caso difícil que
   el M5 describe.
6. **`ndiffs` de pmdarima no decide como el de R sobre ∇₁₂ log y:** devuelve 0 donde R devuelve 1
   (`r1_python.out` §4). El capítulo no lo afirma; queda anotado por si la R3 quiere usar pmdarima en el pipeline.
7. **La señal «r₁ cerca de −0.5» tampoco es universal.** D5 la pone como señal de sobrediferenciación, y lo es
   cuando se diferencia algo parecido a ruido; en una serie estacionaria persistente ρ₁(∇y) = −(1−φ)/2 queda
   cerca de 0 (−0.148 en el ejemplo). El recuadro lo dice. **La R3 debería tenerlo presente al escribir la regla
   única.**

---

## Para la sesión maestra

- **El enlace simbólico** `precalculo/trm_mensual_2015-01_2026-06.csv`: hay que añadirlo al commit junto con
  `Htmls_Series/datos/`. Si se prefiere no versionar un enlace, la alternativa es que `genera_cap2.R` escriba el
  CSV dos veces.
- **La URL pública no existe hasta desplegar.** Tras el `subtree push`, comprobar que
  `…/datos/trm_mensual_2015-01_2026-06.csv` responde 200. Es la primera carpeta `datos/` del sitio.
- **La clave de la P4 no cambió:** «La varianza deja de bajar y vuelve a subir» sigue contando como señal
  correcta. Es coherente con D5 (señal, no criterio) y la retroalimentación lo matiza, pero es una decisión de
  redacción que la R5 puede revisar.
- **La nota del M5 cita dos cifras del simulador** (−0.252 y −0.506). La R2 va a tocar ese simulador (T2.3): si
  cambia su ruido o su lectura, hay que rehacer `r1_simulador_ar1.js`.
- **El ejercicio 4 ejecuta una descarga** cuando corre el verificador de bloques: sin red, la sesión de R
  termina con error en ese bloque (el último), aunque las cifras anteriores ya estén contadas.
- **`statsmodels.base.transform.BoxCox`** es lo que el M8 presenta como Guerrero en Python. Funciona y da el
  valor de R en la 0.14.6; no se comprobó en otras versiones.
- **El recuadro y el orden de las diferencias del M7** están corregidos, no reorganizados: T3.2 sigue pendiente.
- No se tocaron la estructura, los minutos, las pistas ni las longitudes de las opciones.

---

## Tras la verificación

Correcciones a los 15 problemas de `diagnostico/cap2/R1_verificacion.md` (1 que bloqueaba, 2 a corregir, 12
menores). **Esta sección manda sobre lo anterior** donde lo contradice: los errores 1, 4 y 5 de T1.1, la fila de
la P4, la del ejercicio 3 y la «clave de la P4» de «Para la sesión maestra» describen textos que ya no están.

**Verificadores al cerrar esta pasada**

- `verifica_bloques_cap6.py --html` → **226 de 226, 0 discrepancias** (`r1b_verifica_bloques.out`).
- `verifica_todo.py` → 11 en verde. `ensambla_cap3.py` → reproducible byte a byte.
  `audita_posicion_correcta.py` → en verde.
- `r1_bloques_publicados.py` → 93 de 93 líneas `#>` literales (`r1b_bloques_publicados.out`).
- `r1b_bloques_sueltos.py` → **los 21 bloques corren solos**, R y Python, cada uno en proceso nuevo y carpeta
  vacía, los dos del ejercicio 4 incluidos.
- `v1_paridad_dolar.py` → 0 `$` impares. `v1_render_katex.js` (Chrome sin ventana, por HTTP) → nueve módulos,
  0 errores de KaTeX, 0 excepciones (`r1b_render_katex.out`).

Cifras nuevas: `r1b_explora.R` / `.out`.

### 1 · La varianza no decide, en ningún sentido (bloqueaba)

Se quitó como señal de decisión de todo el capítulo. Lo que queda es la identidad y por qué no decide.

| dónde | qué dice ahora |
|---|---|
| M7, entrada de «¿Cuántas diferencias?» | «La decisión se apoya en dos cosas, el correlograma y las pruebas. La varianza, que a menudo se cita como tercera señal, cambia al diferenciar pero no decide, y conviene ver por qué» |
| M7, intro del simulador | «Observa la forma de la serie y el correlograma, y anota cómo cambia la varianza […]: después de la tabla se explica qué dice ese número y qué no» |
| M7, punto 3 de la lista | «**La varianza no es una tercera señal.** Que suba o baje al diferenciar depende solo de r₁, y eso no distingue la diferencia que hace falta de la que sobra» |
| M7, tras la tabla | «…no convierte el mínimo de la varianza en una regla, en ninguno de los dos sentidos. […] el cociente de varianzas sigue de cerca a 2(1−r₁): la varianza baja al diferenciar si r₁ > 0.5 y sube si r₁ < 0.5. Es decir, repite lo que ya dice r₁, y r₁ solo no dice si hay una raíz unitaria», con las dos series simuladas: la estacionaria (`ndiffs` 0, **baja** de 2.497 a 1.033) y la de raíz unitaria (`ndiffs` 1, **sube** de 1.096 a 1.513). Cierra: «la decisión la toman el correlograma y las pruebas, no la varianza» |
| M7, recuadro de sobrediferenciación | Ya no menciona la varianza. r₁ cerca de −0.5 es «el indicio más frecuente» y el último párrafo dice «Es un indicio, no una regla, y falla en los dos sentidos»: −0.148 donde la diferencia sobra, −0.483 donde hace falta |
| M7, bloque de R | Los dos ejemplos, (a) y (b), con `ndiffs`, las dos varianzas y r₁ bajo `#>` |
| M9, ciclo, paso 4 | «Si antes de diferenciar la ACF ya caía rápido y `ndiffs()` devolvía 0, esa diferencia sobraba […]. Un r₁ cercano a −0.5 tras diferenciar es un indicio de lo mismo, no una prueba (Módulo 7)» |
| M9, ciclo, paso 5 | Fuera «comprobar que la varianza no subió» y `var()` por cada d; «Una diferencia que las pruebas no pedían → paso 4 con una diferencia menos» |
| M9, pipeline de R | Comentario del paso 4: «Verificar: el KPSS de la serie final no debe rechazar». `var_final` sigue en la lista que devuelve (el pipeline es de la R3) |
| Quiz P4 | Pregunta: «Aplicaste una diferencia regular y sospechas que sobraba. Marca todos los indicios que apoyan esa sospecha». La opción 1, que sigue siendo correcta y en su sitio, es «Antes de diferenciar, la ACF ya caía rápido y `ndiffs()` devolvía 0». La opción 2, que sigue siendo falsa, es «La varianza subió al diferenciar». Claves {1, 3, 4}, como antes. Las dos retros y la pista, reescritas con las cifras del M7 |
| Ejercicio 1 | Enunciado: «Justifica con el correlograma y las pruebas». La solución ya no calcula la varianza por d: muestra la ACF tras ∇₁₂ (0.800, 0.720, 0.628), `ndiffs`/`nsdiffs` de la serie final (0 y 0), el KPSS y lo que queda (n 455, r₁ −0.302, 5 de 24 fuera). La fila «Varianza» de la tabla pasó a «Correlograma tras ∇₁₂» |
| Ejercicio 3 | Enunciado y pista sin la varianza. La explicación se apoya en `nsdiffs` 1, `ndiffs` 1 tras ∇₁₂, los rezagos fuera y el Ljung–Box; cierra: «Un r₁ negativo es un indicio de sobrediferenciación, no una prueba: decide si las pruebas pedían o no la diferencia». La columna «Varianza» de la tabla se queda, como descripción: es la salida del código |

Evidencia: `r1b_explora.out` §M7. AR con φ = 0.8 (`set.seed(1)`): `ndiffs` 0, 2.497 → 1.033, r₁(y) = 0.787,
2(1−r₁) = 0.427 frente a un cociente de 0.413, r₁(∇y) = −0.148. Serie con raíz unitaria y θ = −0.8
(`set.seed(4)`, la de la sesión maestra): `ndiffs` 1, 1.096 → 1.513, r₁ = 0.303, 2(1−r₁) = 1.394 frente a 1.380,
**r₁(∇z) = −0.483**. En log AP y en la TRM el cociente y 2(1−r₁) van juntos en los tres pasos. Búsqueda final en
los templates y el quiz: no queda «tres señales», «te pasaste», «varianza mínima» ni «infla la varianza».

### 2 · El recuadro del KPSS (corregir)

La moraleja ya no usa ni la varianza ni r₁ = −0.341. Dice: «Hay que mirar el correlograma junto a las pruebas y
documentar qué se usó. Aquí el correlograma desempata a favor de `ndiffs()`: la ACF de ∇₁₂ log y baja despacio
(r₁ = 0.714, r₂ = 0.623, r₃ = 0.480, con los ocho primeros rezagos fuera de la banda) […]. El resultado es
d = 1 y D = 1». `r1b_explora.out` confirma lo que señaló el verificador: 2(1−r₁)·var = 0.00218 frente a 0.00210.

### 3 · El ejemplo del M3 (corregir)

Fila «Decaimiento rápido»: «Serie simulada de 200 valores en la que cada uno es la mitad del anterior más un
ruido nuevo (está en el código de abajo; el Módulo 5 presenta este proceso): r₁ = 0.474, r₂ = 0.235, y del rezago
3 en adelante todo dentro de la banda ±0.139».

- **A la vista:** de 24 rezagos solo salen el 1 y el 2; el mayor |r_k| desde k = 4 es 0.094.
- **Sin remisión al simulador** ni a otro ruido: la serie se genera en el bloque de R del propio M3
  (`set.seed(1); arima.sim(list(ar = 0.5), n = 200)`), que imprime r₁…r₄ y los rezagos fuera de la banda.
- **Sin «AR(1)» ni φ:** dicho en palabras, con el M5 como adelanto.
- **La semilla no se eligió mirando:** el criterio está escrito en `r1b_explora.R` (la primera semilla con la que
  solo quedan fuera los primeros rezagos, seguidos) y la primera, la 1, ya lo cumple.
- Se quitó del bloque de R del M5 la línea que imprimía la ACF del ejemplo anterior.

### Menores

| # | qué | estado |
|---|---|---|
| 4 | M5: «lo delata» con φ cerca de 1 | corregido: «deja una autocorrelación negativa […]. Con φ cerca de 1 esa huella es demasiado pequeña para verse: es el caso difícil del punto anterior» (`r1_simulador_ar1.out`; el verificador midió −0.044 con φ = 0.95) |
| 5 | M2: «deja de ser 1/T» | corregido: «puede dejar de ser 1/T, y entonces la banda ya no cubre el 95 %». **No se añadió** el cuarto momento finito: es una condición con fuente, y va con la cita en la R4 |
| 6 | `#> Warning:` no es la salida literal | M6: el bloque lo declara ahora con todas las letras («Los avisos de R van abreviados: donde aqui dice "Warning: ...", R escribe "Warning message:" y, debajo, "In kpss.test(trm) : ..."»). Ejercicio 1: ya no hay aviso; usa `suppressWarnings(kpss.test(co2_sd))$p.value` y lo dice. No se copió el aviso literal porque su forma depende de `options(warn)` (el verificador corre con `warn = 1` y lo escribe distinto que una sesión normal) |
| 7 | los bloques del ejercicio 4 no corrían solos | corregido: el de R lee él mismo la copia fija y el de Python define `adf_como_en_r()`. `r1b_bloques_sueltos.out`: los 21 solos. **Sigue dependiendo de la red** (descarga de datos.gov.co): es el ejercicio |
| 8 | P8, «la única restricción de Box–Cox…» | corregido: «La restricción está en los datos, no en λ: con λ ≤ 0 tienen que ser estrictamente positivos» (cierto con la fórmula del M8 y con la variante con signo) |
| 9 | M9 Python, «porque la serie es estacional» | corregido: «se fija en 1 siempre que m > 1, sea o no estacional la serie» |
| 10 | M9, árboles «sin respuesta» | corregido: «un árbol de decisión de hojas constantes predice con promedios de lo que vio al entrenarse, así que ante una tendencia que sigue subiendo se queda en una meseta». Sigue sin fuente: R4 |
| 11 | M6, «de aquí en adelante» | corregido: «que es la serie del resto de este módulo» |
| 12 | M6, «estacionaria» a secas en el recuadro y en la tabla de combinaciones | corregido con un párrafo bajo la tabla: «…«estacionaria» se lee según la variante de cada prueba: con `adf.test()`, estacionaria alrededor de una tendencia; con el KPSS, en nivel o alrededor de una tendencia, según se pida». La tabla y el recuadro no se rehicieron (R3) |
| 13 | ejercicio 4: «evidencia de la raíz unitaria», «a un paso de rechazar» | corregido: «la evidencia contra la estacionariedad es abundante» y «p = 0.071, que ya rechaza la raíz unitaria al 10 % y se queda a un paso de hacerlo al 5 %» |
| 14 | lectura «d de varianza mínima =» del simulador del M7 | **no tocado: es armazón (R2).** Queda desmintiendo al módulo: la lectura (JS, hacia la l. 6040 antes de esta pasada) y su comentario «la señal práctica de cuántas veces diferenciar» deben quitarse o rotularse en la R2 (T2.3 es el sitio natural) y propagarse por la cadena. La intro del simulador ya avisa de que ese número no decide |
| 15 | primera persona e imperativo en frases reescritas | corregido en las tres señaladas: «en 24 rezagos lo esperable es…»; «La columna r₁ de la tabla lo muestra»; «se diferencia, se obtiene […] se fabrica […] conviene diferenciar de menos». El resto de la prosa antigua en primera persona no se tocó: no es de esta ronda |

### Para la sesión maestra, además

- El número de líneas `#>` pasó de 86 a 93 y las cifras vigiladas de 210 a 226.
- La P4 tiene ahora un distractor que afirma lo que el capítulo enseñaba antes («La varianza subió al
  diferenciar»). Es deliberado; la R5 puede cambiarlo.
- El ejemplo (b) del M7 es una serie del capítulo 4 dicha en palabras («una serie con raíz unitaria cuyos cambios
  se compensan en parte de un periodo al siguiente»); el código usa `order = c(0, 1, 1)`, que el estudiante aún
  no conoce. La R3 puede decidir si se presenta como adelanto.

## Sesión maestra, al cerrar la ronda (2026-11-16)

- **Lectura «d de varianza mínima =» del simulador del M7, retirada.** El redactor la dejó porque vive
  en el código del simulador, fuera de los `<template>`. Pero el capítulo 3 no la hereda (no aparece ni
  en el 3 ni en el 4), y `ensambla_cap3.py` sigue reproducible byte a byte tras quitarla. Publicar la R1
  con esa lectura habría dejado al simulador recomendando lo que el módulo acaba de desmentir. Se quitaron
  el cálculo de `dOptimo` y su fila de la lectura; la lectura conserva d, n, varianza, r₁ y `ndiffs`.
  Comprobado en el navegador por HTTP: el simulador pinta, la lectura se actualiza, sin errores de consola
  ni de KaTeX.
- **Recomprobado en R por la sesión maestra** (`comprobaciones/maestra_r1.R` y su `.out`): las cinco
  cifras de doble redondeo (0.585, 0.241, −6.421, −1.532, 0.707), que el CSV congelado es idéntico a
  `datos_series.json`, y el contraejemplo del verificador (ARIMA(0,1,1) con θ = −0.8: `ndiffs` 1 y la
  varianza sube de 1.096 a 1.513; en 500 series sube en el 58.8 %).
- **Costura con los capítulos 4 y 5, para sus rondas.** El capítulo 4 usa el mínimo de varianza como
  decisión de trabajo para el Nilo (l. 3452) y ya avisa de que la regla falla (l. 4282, 5513); el
  capítulo 5 (l. 3965) la atribuye «al Capítulo 4» y dice que en su caso acierta. Nada de eso es falso,
  pero ahora el capítulo 2 enseña que la varianza no decide: la ronda de cada uno debe alinear el
  lenguaje.
