# Revisión de par académico · Capítulo 1 «Componentes y descomposición»

Archivo: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (las líneas remiten a ese archivo).
Lente: corrección y rigor. No se repiten los tres hallazgos del piloto (localizador §4.3/§3.6 de F_T/F_S,
desarrollo del acrónimo STL, cuarta limitación del método clásico) ni el «m/2 solo con m par» del recuadro
de limitaciones (l. 3343); cuando un hallazgo comparte raíz con ellos pero está en otro sitio, se indica.

Entorno de comprobación: R 4.6.0 (stats, tsibble, fabletools, feasts, slider instalados; `fpp3` no), Python
3 con pandas 2.3.3 y statsmodels 0.14.6. Los guiones completos están junto a este archivo:
`diag/v1.R` (M2, M4, M5, M6), `diag/v2.R` (STL, Loess, robustez, fuerzas), `diag/v3.R` (feasts),
`diag/v4.R` (ejercicio 1). En la evidencia se pone la orden mínima y la salida pertinente.

Abreviaturas: `AP <- AirPassengers`; `lx <- log(AP)`; `ap_out` = AP con la obs. 79 (jul-1955) × 1.5.

---

## M1 · ¿Qué es una serie de tiempo? (2316–2373)

Sin hallazgos. Definición, contraste con corte transversal y descripción de AirPassengers correctos.

---

## M2 · Series de tiempo en software (2378–2504)

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2472, 2479 | error | «`key =` de `tsibble` (`ts` no puede)»; «Un `ts` guarda **una** serie» | `ts()` sobre una matriz crea un objeto `mts` con varias series que comparten índice (p. ej. `EuStockMarkets`). La diferencia real es formato ancho con índice común (`mts`) frente a formato largo con clave e índices propios (`tsibble`). | R: `class(ts(matrix(1:48,24,2), frequency=12)); class(EuStockMarkets)` → `"mts" "ts" "matrix" "array"` (las dos) |
| 2461–2463 | imprecisión | Fila «Frecuencia estacional»: R `frequency()` (= 12) ↔ Python `freq="MS"` | `freq="MS"` es la frecuencia de muestreo (inicio de mes), no el período estacional; en Python el 12 se pasa aparte (`period=12`, como hace el propio código del M6 y M7). La tabla equipara dos conceptos distintos que el párrafo 2397–2399 sí separa. | razonamiento + docstring de statsmodels `STL`: «period : Periodicity of the sequence. If None and endog is a pandas Series … attempts to determine from endog» (el período es un argumento propio) |

---

## M3 · Visualización (2509–2617)

Sin hallazgos. Las definiciones de gráfico estacional, de subseries y de rezagos y el uso de `period` en
`gg_season()` coinciden con FPP3 §2.4–2.5 y §2.7.

---

## M4 · Los cuatro componentes; aditivo y multiplicativo (2622–2822)

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2713, 2719, 2760; y M6: 3202, 3208, 3216, 3225, 3313–3326 | error | «los mismos pasajeros de más en julio», «pasa de 44 a 232 pasajeros», «la serie marcó 364 pasajeros», «rondaba los 286 pasajeros», «63.83 … una cantidad de pasajeros», «28.7 pasajeros de más» | AirPassengers está en **miles** de pasajeros: 364 son 364 000. El propio capítulo rotula «Pasajeros (miles)» en los gráficos (JS l. 4678, 4934) y «Miles de pasajeros» en el código Python (l. 2596), así que la prosa contradice sus ejes. | R: `tools::Rd2txt(utils:::.getHelpFile(help("AirPassengers")))` → «Format: A monthly time series, in thousands.» |
| 2675–2676 | divergencia | «El modelo aditivo conviene cuando la amplitud estacional es constante; el multiplicativo, cuando la amplitud crece con el nivel» | FPP3 pide proporcionalidad («proportional to the level»), no solo crecimiento, e incluye también la variación alrededor de la tendencia-ciclo, no solo la amplitud estacional. Con el criterio laxo del capítulo, una amplitud que crece más que proporcionalmente (lo que pasa en AP, ver M9) también «es multiplicativa». | FPP3 `decomposition.txt` §3.2: «When the variation in the seasonal pattern, or the variation around the trend-cycle, appears to be proportional to the level» |
| 2724–2727 | laguna | Amplitud de cada año = «el mes más alto menos el más bajo», frente al nivel medio | El máx − mín del año calendario incluye lo que sube la tendencia dentro del año, de modo que la razón amplitud/nivel no aísla la estacionalidad (y bajo un modelo multiplicativo exacto con tendencia lineal no es constante). El propio código del capítulo lo reconoce para el comparador y por eso allí mide la desviación respecto a la tendencia. Falta al menos declararlo como aproximación. | razonamiento; el comentario del JS, l. 4816–4819: «no como máx − mín del año: así el número aísla el componente estacional en vez de mezclarlo con lo que sube la tendencia» |
| 2763–2764 | imprecisión (menor) | «la proporción … sube del 35 % al 49 %»; los puntos «se le quedan por encima» del rayo | La proporción no es monótona: 1951 queda por debajo del rayo (31.7 % < 34.7 %) y el máximo es 51.2 % en 1958. Decirlo como subida de extremo a extremo oculta la dispersión. | R (`v1.R`): `round(100*amp/niv,1)` → 34.7 40.1 **31.7** 36.0 40.9 47.7 46.1 43.3 45.1 **51.2** 50.7 48.7 |
| 2800–2801 | imprecisión | Con el logaritmo «la amplitud pasa de multiplicarse por más de cinco a hacerlo por poco más de uno» | En logaritmos la amplitud de 1960 es 1.32 veces la de 1949: no «poco más de uno». Es coherente con b = 1.29 > 1 (M9, ej. 1): la amplitud crece más que proporcionalmente y el log no la estabiliza del todo. Conviene dar la cifra, que además el simulador muestra (l. 4970–4971). | R: `la <- tapply(log(AP), floor(time(AP)), function(z) max(z)-min(z)); la[12]/la[1]` → 0.3528 → 0.4668, **×1.323** |

---

## M5 · Medias móviles (2827–2944)

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2920–2925 | error | Comentario «Media movil centrada de orden 12 (2x12)» con `slider::slide_dbl(value, mean, .before = 6, .after = 6, .complete = TRUE)` | Eso es una 13-MA de pesos iguales (1/13), no la 2×12: cuenta enteros los dos eneros y no anula la estacionalidad. FPP3 construye la 2×12 con dos pasos: 12-MA (`.before = 5, .after = 6`) y luego 2-MA (`.before = 1, .after = 0`). En jul-1955 da 284.00 frente a los 285.75 que el M6 atribuye a esta misma media; la diferencia llega a 9.9. | R: `filter(AP, rep(1/13,13))[79]` → 284; `filter(AP, c(.5,rep(1,11),.5)/12)[79]` → 285.75; máx. dif. 9.897. FPP3 §3.3: «`2x12-MA` = slider::slide_dbl(`12-MA`, mean, .before = 1, .after = 0» |
| 2930–2931 | error | «Media movil centrada de orden 12 con pandas»: `rolling(window=12, center=True).mean()` | Con ventana par, pandas centra una 12-MA asimétrica: no es la 2×12 del texto. En jul-1955 da 284.0 (la media de ene–dic 1955) en vez de 285.75, y deja 11 NaN, no 12, en contra de lo que dicen la prosa y el quiz. | Python: `s.rolling(window=12, center=True).mean()` → jul-1955 = 284.0; NaN = 11; primer válido 1949-07, último 1960-07 |
| 2869–2874 | laguna | La ventana del período contiene cada mes una vez y «los efectos estacionales se compensan entre sí y lo que sobrevive es el nivel» | Se compensan solo si los efectos suman 0 en el ciclo (la normalización, que se introduce después, en el M6) y si la tendencia es localmente lineal (una MA simétrica conserva rectas, no curvatura). En el caso multiplicativo, MA(T·S) ≈ T solo de forma aproximada. Falta una línea con esos supuestos. | razonamiento: la 2×12 aplicada a T_t + S_t da MA(T)_t + (1/12)·Σ_k S_k, que es igual a T_t solo si Σ S_k = 0 y T es lineal en la ventana |
| 2869 | divergencia (menor) | «elegir m igual al período y no un número cualquiera» | FPP3 precisa que también valen los múltiplos (24, 36…), y el simulador llega hasta m = 24, donde la estacionalidad también desaparece. | FPP3 §3.3: «Any other choice for the order of the moving average (except for 24, 36, etc.) would have resulted in a smooth line that showed some seasonal fluctuations.» |
| 2889–2891 | imprecisión (menor) | El simulador del M7 «permite volver a apretarlas para comprobar que lo que queda … es, otra vez, una media móvil como esta» | El deslizador de span solo admite impares (7–61, paso 2), así que se recupera una media simple de orden impar, nunca la 2×12 de este módulo. | JS l. 5258: `{ clave: 'span', … min: 7, max: 61, paso: 2 }` |

---

## M6 · Descomposición clásica (2949–3359)

Todas las cifras del módulo se reprodujeron exactamente con `decompose()`: s̄ = 0.998236; julio bruto 1.224391
y normalizado 1.2266; n_k = 11; suma de índices 12.0001; T̂(jul-55) = 285.75; R̂ = 1.0386; los 11 cocientes
de julio; aditivo 63.83 y 14.42; excesos de julio 21.3…145.8; desviaciones típicas 30.5…25.4; noviembre 0.8012.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 3030 | error | Paso 2, «Con qué»: «`stats::filter(y, rep(1/m, m))` o directamente `decompose()`» (y en la misma ficha: «Con $m$ par hace falta la media móvil $2\times m$») | Con m par ese filtro no está centrado: «more of the filter is forward in time». Es la 12-MA desplazada medio mes, no la 2×12 que usa `decompose()` (`c(0.5, rep_len(1, f - 1), 0.5)/f`). En jul-1955 da 287.5, no 285.75, y deja 11 NA. | R: `stats::filter(AP, rep(1/12,12))[79]` → 287.5; `sum(is.na(...))` → 11; `body(decompose)` → `c(0.5, rep_len(1, f - 1), 0.5)/f` |
| 3280–3283 | error | Comentario «# Version tidyverts (aditiva sobre log = multiplicativa)» sobre `classical_decomposition(value, type = "multiplicative")` | El código no es aditivo sobre log, y en la descomposición clásica las dos cosas no son equivalentes: la media móvil del log no es el log de la media móvil (media geométrica frente a aritmética). La equivalencia de FPP3 §3.2 vale para el modelo, no para el estimador clásico. | R: `exp(decompose(log(AP))$figure[7])` → 1.2347 frente a `decompose(AP,"multiplicative")$figure[7]` → 1.2266; las tendencias difieren hasta 6.85 |
| 3016 | imprecisión | Paso 1, «Con qué»: «La decisión es visual, no hay prueba automática.» | Contradice el propio capítulo: el M4 dice «Conviene desconfiar de eso y convertirlo en un número» y el ejercicio 1 propone una regresión con IC. FPP3 además ofrece una elección automática de λ (λ = 0 es el log) con la característica `guerrero`. | FPP3 §3.1: «The guerrero feature (Guerrero, 1993) can be used to choose a value of lambda for you.» |
| 3094 | imprecisión | Tabla, paso 2: «$\hat{T}_t$, la media móvil centrada de orden $2\times m$» (sin condición; m se define como «el período» en general, l. 3074) | Para m impar el paso 1 es una m-MA, no una 2×m. Comparte raíz con el «m/2» ya detectado, pero está en otro sitio, la tabla «en símbolos», que debería ser la versión exacta. | FPP3 §3.4, Step 1: «If m is an odd number, compute the trend-cycle component \hat{T}_t using an m-MA.» |
| 3168 | imprecisión (menor) | Normalizar «devuelve ese factor constante a donde pertenece —la tendencia—» | T̂ no se toca en ningún paso: dividir por s̄ saca el factor de Ŝ y, por el paso 4, deja R̂ centrado en 1. El factor no pasa a la tendencia, simplemente desaparece del producto Ŝ·R̂. | razonamiento: Ŝ_k = s̃_k/s̄ ⇒ R̂ = y/(T̂ Ŝ) = s̄·y/(T̂ s̃), con T̂ idéntico antes y después |
| 3325–3326, 3328–3332 | imprecisión (menor) | «su único 1.2266 se traduce … porque se aplica sobre una tendencia que crece: 28.7 … en 1949 y 107.9 en 1960»; desviación típica del residuo «calculada año por año» | 107.9 = 0.2266 × nivel medio de 1960, no × T̂: en jul-1960 la descomposición clásica no tiene tendencia (NA). Y las desviaciones de 1949 y 1960 se calculan con 6 residuos, no con 12. Ninguna de las dos cosas se declara. | R: `(dc$figure[7]-1)*mean(AP[133:144])` → 107.88; `dc$trend[139]` → NA |

---

## M7 · STL y Loess (3364–3704)

Reproducidas: t.window = 19 con «periodic», 21 con s.window = 11; julio con s.window = 11 de +20.4 % a +27.9 %
(recorrido 0.0602); julio-1955 en log 5.6460 / 0.2164 / 0.0347; 6.2043 frente a 6.2048 y diferencia 0.0498;
5.5482; |R| = 0.3708, umbral 0.1150, u = 3.22 y peso mediano 0.9461 en la primera pasada; S_julio 1.2405 con
`trend(window = 21)`.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 3403–3428 (+ JS 5063–5068) | error | Tabla de pesos «en esa ventana de 19 meses» (la de `stl()`): 3 meses → 0.9212, 6 → 0.4819, «9 meses — el borde» → 0.0199; «El mes del borde cuenta unas 50 veces menos» | `stl()` toma como radio la distancia al vecino más lejano de la ventana, así que el borde (9 meses) pesa **0**, a 6 meses 0.348 y a 3 meses 0.893. El capítulo usa un radio de «distancia + 1» (lo declara solo en un comentario del JS) y lo presenta como el peso de STL. | R (`v2.R`): con `stl(lx,"periodic",inner=1,outer=0,t.jump=1)` y el ajuste local reimplementado, radio = dist. máx. reproduce la tendencia de stl con máx\|dif\| = **8.4e-08**; radio = dist. máx. + 1 (el del capítulo) da 0.0070 |
| 3551–3552 | error | Bucle interior: «alterna estacionalidad y tendencia **hasta que se estabilizan**» | En `stl()` el bucle interior da un número fijo de pasadas, sin criterio de convergencia: 2 sin robustez y 1 con ella. El exterior da 0 o 15. | R: `args(stl)` → `inner = if (robust) 1 else 2, outer = if (robust) 15 else 0`; `stl(lx,"periodic")$inner` → 2 |
| 3587–3588 (y 4059) | error | «De las 144 observaciones, el procedimiento expulsa exactamente una … Las demás siguen contando casi por entero» | Eso vale solo para la primera pasada del bucle exterior, que es la que muestra la tabla. El ajuste que de verdad hace `robust = TRUE` (15 pasadas), y que usa el ejercicio 3, deja con peso 0 las observaciones 2, 26, 38, 79 y 135 (cinco), y 15 por debajo de 0.5. En la serie limpia anula 4 (2, 26, 38, 135). Por eso el índice robusto de julio en la serie limpia (1.2562) ya se separa un 1.2 % del no robusto (1.2416). | R: `which(stl(log(ap_out),"periodic",robust=TRUE)$weights==0)` → 2 26 38 79 135; `sum(w<0.5)` → 15; limpia: 2 26 38 135; primera pasada (`robust=TRUE, inner=2, outer=1`): solo la 79 |
| 3664–3669 | error | Python «# STL sobre log(AirPassengers)»: `STL(np.log(pasajeros), period=12, robust=True).fit()` | No reproduce la figura ni el código de R (periodic, no robusto, s.degree = 0). statsmodels usa por defecto `seasonal=7` y `seasonal_deg=1`, y aquí se activa `robust`: el julio estacional va de 0.165 (1949) a 0.272 (1960), frente al 0.2164 constante del capítulo. | Python: docstring `STL(endog, period=None, seasonal=7, …, seasonal_deg=1, trend_deg=1, …)`; `res.seasonal` jul-49 = 0.1647, jul-60 = 0.2724 |
| 3389–3393 | imprecisión | Loess «estima la tendencia un instante a la vez … Después repite la operación en $t+1$» | Por defecto `stl()` evalúa la regresión local solo cada `t.jump = ceiling(t.window/10) = 2` instantes e interpola linealmente entre ellos. Es una de las causas de que el simulador no coincida exactamente con `stl()` (6.2043 frente a 6.2048). | R: `stl(lx,"periodic")$jump` → s 145, **t 2**, l 2; máx\|tendencia(t.jump=2) − tendencia(t.jump=1)\| = 0.0024 |
| 3398–3399; 3654 | imprecisión | «Sobre AirPassengers, `stl()` calcula por su cuenta una ventana de 19 meses»; comentario «window = 19 es justo lo que STL calcula solo con m = 12» | El 19 depende también de s.window: sale con «periodic». Con s.window = 11 (el valor por defecto de `STL()` en FPP3) sale 21, que es lo que FPP3 da como valor por defecto mensual. La condición se dice en la derivación (3508), pero no en la afirmación ni en el comentario. | R: `stl(lx, s.window=11)$win` → s 11, **t 21**; FPP3 §3.6: «The default setting for monthly data is trend(window=21).» |
| 3376, 3382–3383; 3347; 3856–3857 | imprecisión | Objetivo: «por qué es más flexible y robusta que la clásica»; «responde a esas tres debilidades»; M6: «STL corrige estas tres debilidades»; resumen: «STL (flexible y robusta)» | El propio capítulo concluye (4060–4061) «STL no es intrínsecamente resistente, lo es la opción», y FPP3 lo formula como posibilidad del usuario. El objetivo y el resumen afirman la robustez sin la condición. | FPP3 §3.6: «It can be robust to outliers (i.e., the user can specify a robust decomposition)» |
| 3389 | divergencia / sin comprobar | «**Loess** (*locally estimated scatterplot smoothing*)» | Ninguna fuente disponible respalda ese desarrollo. Shumway y Stoffer desarrollan *lowess* como «locally weighted scatterplot smoothing», y FPP3 no desarrolla «loess». Hay que contrastarlo con Cleveland (1979) o Cleveland y Devlin (1988), que están en `obras.tsv` sin texto. Es distinto del hallazgo del piloto sobre el acrónimo STL. | Shumway y Stoffer 3.ª ed., `p0077.txt` (p. impresa 64): «locally weighted scatterplot smoothing (lowess) lines» |

---

## M8 · Ajuste estacional y fuerza (3709–3810)

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 3744–3747, 3791–3792 | divergencia | F_T y F_S «a partir de las varianzas de los componentes STL (aquí, sobre la escala log)»: para AP, 0.994 y 0.937 | Las cifras salen de `stl(s.window = "periodic")` (lo muestra el código del ej. 2), no de la STL con la que FPP3 calcula estas fuerzas (`feat_stl`, ventana estacional por defecto). Con `feat_stl` salen 0.997 y 0.964. La elección es defendible, pero hay que declararla, porque el párrafo atribuye la medida a FPP3. | R (`v3.R`): `features(as_tsibble(log(AP)), value, feat_stl)` → trend_strength 0.997, seasonal_strength_year 0.964; con `s.window="periodic"` → 0.994 y 0.937 |
| 3737–3738 (JS 5349) | imprecisión | Simulador: «La línea desestacionalizada ($y_t/\hat{S}_t$) … deja la tendencia-ciclo más un residuo **suave**», tras «Con componentes en los que se puede confiar» | (i) Ŝ_t es el de la descomposición **clásica** multiplicativa, la criticada en el M6, y no el de STL, y no se dice. (ii) La serie desestacionalizada contiene el residuo y no es suave. | JS l. 5349: `S = DATOS_CAP1.clasica_multiplicativa.estacional`; FPP3 §3.2: «Seasonally adjusted series contain the remainder component as well as the trend-cycle. Therefore, they are not “smooth”» |
| 3749–3751, 3762–3781 | imprecisión (notación) | F_T y F_S con $T_t$, $R_t$, $S_t$ sin gorro | Son componentes estimados. El M6 los escribe con gorro ($\hat{T}_t$, $\hat{R}_t$), y en el M4 $R_t$ era el «Ruido», un componente no observable. La notación cambia de módulo a módulo sin aviso. FPP3 tampoco pone gorro aquí, pero el capítulo sí los había distinguido. | razonamiento: compárense l. 2648 («Ruido ($R_t$)»), 3119 ($\hat{R}_t$) y 3749 |

---

## M9 · Cierre, ejercicios, lecturas y quiz (3815–4084; quiz 5993–6178)

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 3900, 3916, 3929–3940 | error | Ej. 1: «con `co2` los datos no permiten decidir»; tabla: b = 1.083, IC95 [0.575, 1.591] → «Indistinguible» | Con el criterio que fija el propio código (b ≈ 0 aditiva, b ≈ 1 multiplicativa), un IC que **excluye el 0 y contiene el 1** rechaza la aditiva al 5 % y es compatible con la multiplicativa. La conclusión está invertida. Que la elección «importe poco» por lo estrecho del rango de nivel es otro argumento, válido, pero no es lo que dice el IC. | R (`v4.R`): b = 1.083, IC [0.575, 1.591]; `0.575 > 0` → TRUE; contiene 1 → TRUE |
| 3941–3945 | error | «la amplitud estacional del CO₂ sí crece, a razón de +0.024 ppm por año (p = 0.0002). **No es proporcional al nivel; es un fenómeno propio.** Eso no lo captura bien ninguna descomposición de índices fijos» | El crecimiento es justo el que predice la proporcionalidad: amplitud = c·nivel, con c = media(amp)/media(nivel), da una pendiente de 0.0226 ppm/año. La razón amplitud/nivel no tiene tendencia (p = 0.85). Una descomposición **multiplicativa** de índices fijos sí recoge una amplitud proporcional al nivel. | R (`v4.R`): `lm(a ~ yrs)` pendiente 0.02394 (p = 0.00021); pendiente implícita por proporcionalidad 0.02262; `lm(I(a/n) ~ yrs)` pendiente 3.3e-06, p = 0.847 |
| 3935–3936 | imprecisión | AP: «el intervalo es estrecho y excluye el 0 con holgura … multiplicativa sin discusión» | El IC [1.149, 1.432] también excluye el 1: con el mismo criterio, los datos rechazan el multiplicativo exacto (la amplitud crece más que proporcionalmente, lo que el M4 llama «no es un multiplicativo de manual»). «Sin discusión» exagera, y el siguiente paso natural sería un Box–Cox con λ < 0. | R: b = 1.291, IC [1.149, 1.432]; `1.149 > 1` → TRUE |
| 3919–3921, 3938–3939 | imprecisión (menor) | «La clave esta en cuanto varia el NIVEL»: `(max - min)/mean` → 16 % y 185 %; «el de AirPassengers se multiplica por casi cuatro» | (máx − mín)/media no mide cuánto sube el nivel: incluye el vaivén estacional. Por medias anuales, el nivel del CO₂ sube un 15.2 % y el de AP se multiplica por 3.76. La prosa interpreta la cifra del código como algo que no es. | R: medias anuales co2 315.83 → 363.82 (+15.2 %); AP 126.7 → 476.2 (×3.76); `(max-min)/mean` = 0.159 y 1.848 |
| 3962 | imprecisión (menor) | Pista del ej. 2: `USAccDeaths` «(casi pura estacionalidad)» | Su F_T = 0.80 es una tendencia nada despreciable; la solución misma la describe como «claramente más débil», no ausente. | R: `fuerzas(USAccDeaths)` → FT 0.7991, FS 0.9426 |
| 3864–3865 | error (impacto bajo) | «**Seis** preguntas … Cada opción tiene su explicación» | El quiz tiene **ocho** preguntas, y la de respuesta múltiple (6098–6110) y las dos numéricas no tienen explicación por opción. | lectura de `AUTOEVALUACIONES['cap1']`, l. 5993–6178 (8 objetos); el motor no muestrea (l. 5402–5410) |
| 6031 | imprecisión | Quiz P2, opción aditiva: «El residuo delataría el problema con un patrón en forma de **embudo**» | El M6 muestra con cifras que la desviación típica anual del residuo aditivo dibuja una **U** (alta en los extremos, mínima en 1954–55), no un embudo que se abre. | R: `tapply(decompose(AP)$random, floor(time(AP)), sd, na.rm=TRUE)` → 30.5 20.7 22.4 17.0 14.5 5.6 6.1 10.0 17.2 29.4 29.4 25.4 |
| 6058 | imprecisión | Quiz P3, retroFallo: «Una ventana centrada de orden $m$ necesita $m/2$ observaciones a cada lado, así que se pierden $m$ en total» | Con m impar son (m − 1)/2 por lado y m − 1 en total. Es la misma raíz que lo ya detectado en l. 3343, en otra ubicación que habría que corregir a la vez. | FPP3 §3.3 (5-MA): «There are no values for either the first two years or the last two years» |
| 6164 | divergencia | Quiz P8, retro: «Ajustada, la comparación revela el cambio real.» | FPP3 advierte lo contrario para la comparación entre meses: la serie ajustada arrastra el residuo, y sus subidas y bajadas pueden engañar; para leer giros recomienda la tendencia-ciclo. | FPP3 §3.2: «“downturns” or “upturns” can be misleading. If the purpose is to look for turning points … it is better to use the trend-cycle component» |
| 4071–4072 | laguna (menor) | Lecturas: FPP3 «caps. 1–3» | F_T y F_S (M8 y ej. 2) están en el cap. 4 (§4.3, «STL Features»). Las lecturas no cubren lo que se evalúa. | FPP3 `features.txt` §4.3: «So we define the strength of trend as: F_T = …» |
| 3835; 6041 | imprecisión (menor) | «transformar con logaritmos o Box–Cox»; quiz P2: «la transformación logarítmica o Box–Cox» | Se nombra Box–Cox, pero el capítulo no la define en ningún módulo. | razonamiento (búsqueda en el capítulo: solo aparece en esas dos líneas) |
| 4074–4075 | sin comprobar | Shumway y Stoffer, «(4.ª ed.), cap. 1 — panorama y ejemplos» | En `_local` solo está el texto de la 3.ª ed. (caps. 1–3); la 4.ª figura en `obras.tsv`, pero no se ha podido leer su cap. 1. No afirmo que esté mal. | — |

---

## Recuento

| módulo | error | imprecisión | laguna | divergencia | sin comprobar | total |
|---|---|---|---|---|---|---|
| M1 | 0 | 0 | 0 | 0 | 0 | 0 |
| M2 | 1 | 1 | 0 | 0 | 0 | 2 |
| M3 | 0 | 0 | 0 | 0 | 0 | 0 |
| M4 | 1 | 2 | 1 | 1 | 0 | 5 |
| M5 | 2 | 1 | 1 | 1 | 0 | 5 |
| M6 | 2 | 4 | 0 | 0 | 0 | 6 |
| M7 | 4 | 3 | 0 | 0 | 1 | 8 |
| M8 | 0 | 2 | 0 | 1 | 0 | 3 |
| M9 (ejercicios, quiz, lecturas) | 3 | 6 | 1 | 1 | 1 | 12 |
| **total** | **13** | **19** | **3** | **4** | **2** | **41** |
