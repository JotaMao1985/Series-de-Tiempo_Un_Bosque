# R1 · Registro de cambios · Capítulo 1 «Componentes y descomposición»

Ronda R1 del `PLAN_Mejora_Cap1.md` («corregir lo que está mal»). Fecha: 2026-11-10. Un solo redactor.
Especificación: `diagnostico/cap1/par_academico.md` (41 hallazgos). Sin commit.

**Archivos editados:** `Htmls_Series/capitulo-1-componentes-descomposicion.html` (77 tramos), y la cadena
`descripcion` de `DATOS_CAP1` en `precalculo/genera_datos.R`, `precalculo/salidas/cap1_datos.js` y
`precalculo/salidas/cap1_descomposicion.json` (una línea en cada uno, a mano; `genera_datos.R` no se ejecutó).

**Recuento:** 34 corregidos · 5 declarados · 2 no tocados. De los 13 errores: 12 corregidos y 1 declarado
(los pesos tricúbicos, por la decisión 2 del encargo).

**Entorno:** R 4.6.0 (`tsibble`, `slider`, `feasts`, `fabletools`, `dplyr`, `ggplot2`; `fpp3` no está) y Python 3
con pandas 2.3.3, statsmodels 0.14.6 y numpy 2.2.6.

**Guiones de esta ronda** (en `diagnostico/cap1/comprobaciones/`; cada `.out` es la salida íntegra de su guion):

| guion | salida | qué comprueba |
|---|---|---|
| `r1_medias_moviles.R` | `r1_medias_moviles.out` | M5 (R) y M6: la 2×12 en dos pasos y el filtro de `decompose()`; 285.75 y 12 `NA` |
| `r1_medias_moviles.py` | `r1_medias_moviles_py.out` | M5 (pandas): 285.75 y 12 huecos, 6 y 6 |
| `r1_stl.R` | `r1_stl.out` | M7: pesos tricúbicos, pasadas de los bucles, 19 frente a 21, `t.jump`, pesos de robustez; M8: fuerzas |
| `r1_stl.py` | `r1_stl_py.out` | M7: qué argumentos de `statsmodels` reproducen la figura (variantes A–E) |
| `r1_m2_m4_m6.R` | `r1_m2_m4_m6.out` | M2 (`mts`), M4 (unidades, proporción, amplitud en log), M6 (clásica, normalización, residuo) |
| `r1_ejercicio1.R` | `r1_ejercicio1.out` | M9, ejercicio 1: cada cifra de la conclusión y de la tabla |
| `r1_bloques_publicados.py` | `r1_bloques_publicados.out` | extrae del HTML los bloques de código cambiados y los ejecuta tal como quedaron publicados |

Las fuentes se leyeron en `bibliografia/_local/web/hyndman2021forecasting/` (`graphics.txt`, `decomposition.txt`,
`features.txt`); se dan archivo, sección y línea. No se añadió ningún `<cite>`.

Las líneas «orig.» son las del informe del par; «ahora» es la línea tras la edición.

---

## Los 41 hallazgos, en el orden del informe

| # | módulo | línea orig. | severidad | estado | qué quedó escrito | evidencia | notas |
|---|---|---|---|---|---|---|---|
| 1 | M2 | 2472, 2479 | error | corregido | Tabla: «matriz `mts`, una columna por serie / `key =` de `tsibble`». Prosa: «Un `ts` le fía el "cuándo" a `start` y `frequency`; si recibe una matriz guarda varias series (un objeto `mts`), pero en formato ancho: una columna por serie y **un único índice** para todas. Un `tsibble` […] admite **varias series a la vez** en formato largo, cada una con sus propias fechas […]» | `r1_m2_m4_m6.out`: `class(ts(matrix(1:48, 24, 2), frequency = 12))` → `mts ts matrix array`; `EuStockMarkets` → igual, `dim` 1860 × 4; un `tsibble` con clave y fechas distintas por serie se construye (5 filas, 2 claves) | ahora 2473 y 2479–2484 |
| 2 | M2 | 2461–2463 | imprecisión | corregido | Celda de Python: «`period=12`, que se pasa a cada función; `freq="MS"` solo declara que el dato es mensual» | El propio capítulo pasa `period=12` en M6 y M7; `r1_bloques_publicados.out` ejecuta `seasonal_decompose(…, period=12)` y `STL(…, period=12)` | ahora 2463–2464. El rótulo de la fila («Frecuencia estacional») no cambia |
| 3 | M4 y M6 | 2713, 2719, 2760; 3202, 3208, 3216, 3225, 3313–3326 | error | corregido | «se cobra en miles de pasajeros» · «con el nivel y la amplitud en miles de pasajeros» · «de 44 a 232 mil pasajeros» · «las unidades de la serie —miles de pasajeros—» · «364 mil pasajeros» · «286 mil pasajeros» · «…278 y 284, en miles de pasajeros» · «una cantidad, en miles de pasajeros, **fija**» · «28.7 mil pasajeros de más en 1949 y 107.9 mil en 1960» | `r1_m2_m4_m6.out`: `?AirPassengers` → «Format: A monthly time series, in thousands.» | Además, fuera de las líneas del par: M1 2358 («…internacionales, en miles»), M7 3569 («de 364 a 546 mil pasajeros») y 3610 («no están medidos en miles de pasajeros»), y dos rótulos del JS: `unidad: 'mil pasajeros'` del mapa estacional (leyenda «622 mil pasajeros», título «Ene 1949: 112 mil pasajeros», comprobado en el navegador) y `'log(miles de pasajeros)'` en `serie-vs-log`. **No se tocó** la frase «los mismos pasajeros de más en julio» (2713 y su eco entrecomillado en 2717): no lleva cifra y está citada literalmente dos veces |
| 4 | M4 | 2675–2676 | divergencia | corregido | «El modelo aditivo conviene cuando la amplitud estacional —o la variación alrededor de la tendencia— *no depende del nivel* de la serie; el multiplicativo, cuando es *proporcional al nivel*.» | `decomposition.txt`, §3.2, l. 101 (criterio de proporcionalidad, con la variación alrededor de la tendencia-ciclo) | Por coherencia: resumen del M9 («**aditivo** si la amplitud no depende del nivel; **multiplicativo** (o log) si es proporcional a él») y ficha del paso 1 del M6 («Si crece más o menos en proporción a él, el modelo es multiplicativo»). No se tocaron la nota del M3 ni el enunciado de la P2 del quiz |
| 5 | M4 | 2724–2727 | laguna | declarado | «Es una medida aproximada, porque el máximo menos el mínimo de un año recoge también lo que la tendencia sube dentro de ese año, pero basta para enfrentar las dos hipótesis.» | razonamiento del par; comentario del JS (l. 4816–4819 orig.) | ahora 2728–2730. La medida no se cambia: eso sería rehacer la tabla y el simulador |
| 6 | M4 | 2763–2764 | imprecisión | corregido | «la proporción tampoco es estable —va del 35 % de 1949 al 49 % de 1960, con un mínimo del 32 % en 1951 y un máximo del 51 % en 1958—, […] pero después de 1949 todos menos el de 1951 se le quedan por encima» | `r1_m2_m4_m6.out`: pct = 34.7 40.1 31.7 36 40.9 47.7 46.1 43.3 45.1 51.2 50.7 48.7; por debajo del rayo solo 1951; mínimo 1951 (31.7), máximo 1958 (51.2) | Lectura del simulador `amplitud-nivel`: «sube del» → «pasa del» (JS, ahora 5024) |
| 7 | M4 | 2800–2801 | imprecisión | corregido | «la amplitud pasa de multiplicarse por más de cinco a hacerlo por 1.32: el logaritmo no vuelve la serie perfectamente aditiva —la amplitud todavía crece cerca de un tercio—, la acerca lo bastante…» | `r1_m2_m4_m6.out`: amplitud en log 0.3528 → 0.4668, razón 1.323; amplitud 1960/1949 = 5.27 | Coincide con la lectura del simulador (×1.32, vista en el navegador) |
| 8 | M5 | 2920–2925 | error | corregido | Bloque R en dos pasos, como FPP3 §3.3: `12-MA` con `.before = 5, .after = 6` y, sobre ella, `tendencia` con `.before = 1, .after = 0`; cierra con el control `pasajeros \|> filter(index == yearmonth("1955 Jul")) \|> pull(tendencia)` → `#> [1] 285.75` | `r1_bloques_publicados.out` (el bloque tal como está en el HTML): salida `[1] 285.75`, 12 `NA`. `r1_medias_moviles.out`: `NA` en 1–6 y 139–144; máx. diferencia con `decompose()$trend` = 1.1e-13. Fuente: `decomposition.txt`, §3.3, l. 310–326 | ahora 2931–2946. Antes daba 284. La frase de cierre del módulo pasa de «cabe en una línea» a «cabe en un par de líneas» |
| 9 | M5 | 2930–2931 | error | corregido | `ma12 = pasajeros.rolling(window=12).mean()` y `tendencia = ma12.rolling(window=2).mean().shift(-6)`; dos controles: `print(tendencia["1955-07-01"])  # 285.75` y `print(tendencia.isna().sum())  # 12` | `r1_bloques_publicados.out`: 285.75 y 12. `r1_medias_moviles_py.out`: `NaN` en 1–6 y 139–144; máx. diferencia con los pesos explícitos 1/24, 1/12 × 11, 1/24 = 1.1e-13 | ahora 2949–2959. Antes: 284.0 y 11 huecos. La etiqueta del gráfico pasa a «media movil 2x12» |
| 10 | M5 | 2869–2874 | laguna | corregido | «La compensación es exacta cuando los efectos estacionales suman cero a lo largo del ciclo —la condición que el Módulo 6 impone al normalizar— y la tendencia es una recta dentro de la ventana; si la tendencia se curva, o si los componentes se multiplican en vez de sumarse, es solo aproximada.» | razonamiento del par: la 2×12 de $T_t + S_t$ da $\mathrm{MA}(T)_t + \frac{1}{12}\sum_k S_k$ | ahora 2879–2882 |
| 11 | M5 | 2869 | divergencia (menor) | corregido | «elegir $m$ igual al período —o a un múltiplo suyo, como 24 o 36— y no un número cualquiera» | `decomposition.txt`, §3.3, l. 334 | ahora 2875–2876 |
| 12 | M5 | 2889–2891 | imprecisión (menor) | corregido | «…es, otra vez, una media móvil: la simple de orden impar de la primera fórmula de este módulo, porque ese simulador solo admite anchuras impares.» | JS: `{ clave: 'span', … min: 7, max: 61, paso: 2 }` | Por coherencia, «la media móvil **simple** del Módulo 5» en la intro del simulador `loess-local` (M7) y en su lectura (JS, ahora 5307). El JS de cálculo no se tocó |
| 13 | M6 | 3030 | error | corregido | «Con $m$ par, `stats::filter(y, c(0.5, rep(1, m - 1), 0.5) / m)` —los pesos de la $2\times m$—, o directamente `decompose()`, que aplica ese mismo filtro; en Python, `seasonal_decompose()`.» | `r1_bloques_publicados.out`: el filtro, leído del HTML, da 285.75 en jul-1955, 12 `NA` y es igual a `decompose()$trend`. `r1_medias_moviles.out`: `body(decompose)` → `c(0.5, rep_len(1, f - 1), 0.5)/f`. `seasonal_decompose()` da también 285.75 y 12 `NaN` | ahora 3053. Antes: 287.5 y 11 `NA` |
| 14 | M6 | 3280–3283 | error | corregido | Comentario: `# Version tidyverts de la misma descomposicion multiplicativa` | `r1_m2_m4_m6.out`: `classical_decomposition(value, type = "multiplicative")` da julio = 1.2266, diferencia 0 con `decompose()`; la aditiva sobre log daría 1.2347 y tendencias que difieren hasta 6.85 | ahora 3304 |
| 15 | M6 | 3016 | imprecisión | corregido | «Se empieza por mirar, pero conviene respaldarlo con un número: la amplitud de cada año frente a su nivel, como en el Módulo 4.» | coherencia interna (M4 y ejercicio 1) | ahora 3039. No se nombra `guerrero` (`decomposition.txt` §3.1, l. 80): sería contenido nuevo y pediría cita → R4 si se quiere |
| 16 | M6 | 3094 | imprecisión | corregido | «$\hat{T}_t$, la media móvil centrada del Módulo 5: la $2\times m$ si $m$ es par, la de orden $m$ si es impar.» | `decomposition.txt`, §3.4, l. 351 (paso 1) | ahora 3117–3118. En la ficha del paso 2 (3026 orig.) se añadió «con $m$ impar basta la media móvil de orden $m$, que cuesta $(m-1)/2$» |
| 17 | M6 | 3168 | imprecisión (menor) | corregido | «Dividir cada índice por $\bar s$ saca ese factor constante de los índices —la tendencia no se toca: sigue siendo la media móvil del paso 2— y los deja midiendo solo la desviación respecto del año medio.» | `r1_m2_m4_m6.out`: $\bar s$ = 0.998236; julio bruto 1.224391 → 1.2266 | ahora 3191–3193. **Ojo:** el par propone que la normalización «deja $\hat R$ centrado en 1»; en R ocurre lo contrario (ver «Roto y fuera del informe», n.º 1). Por eso la frase no dice adónde va el factor |
| 18 | M6 | 3325–3326, 3328–3332 | imprecisión (menor) | corregido | «…porque se aplica sobre un nivel que crece: sobre el nivel medio de cada año, 28.7 mil pasajeros de más en 1949 y 107.9 mil en 1960.» · «…calculada año por año —en 1949 y en 1960, con los seis meses que tienen residuo—, dibuja una U inconfundible.» | `r1_m2_m4_m6.out`: `(S_julio − 1) × nivel medio` de 1949 y 1960 = 28.7 y 107.9; `dc$trend[139]` = `NA`; residuos disponibles por año: 6 12 … 12 6 | ahora 3350–3351 y 3354–3355. Las cifras no cambian; cambia a qué se atribuyen |
| 19 | M7 | 3403–3428 (+ JS 5063–5068) | error | **declarado** | Antes de la tabla: «La tabla —igual que el simulador de más abajo— toma como radio un paso más que la distancia al vecino más lejano, 10 meses en lugar de 9, para que el mes del borde conserve un peso pequeño y se vea que sigue dentro de la ventana». Después: «Con ese radio, el mes del borde cuenta unas **50 veces menos** […]. `stl()` es todavía más tajante: toma como radio la distancia al vecino más lejano —9 meses—, de modo que $u$ vale $3/9$, $6/9$ y $9/9$ y los pesos son 0.8930 a 3 meses, 0.3485 a 6 y **exactamente 0** en el borde.» | `r1_stl.out` §1: tabla (radio 10) → 0.9212 0.4819 0.0199, 1/w = 50.2; `stl()` (radio 9) → 0.8930 0.3485 0.0000. El ajuste local reimplementado reproduce la tendencia de `stl()` con máx. diferencia 8.4e-08 con radio = distancia máxima, y 0.00695 con radio + 1 | Decisión 2 del encargo: **no se tocó** el JS del simulador, la tabla ni las cifras que dependen de él (6.2043, 0.0498, 5.5482). **Queda para R3** decidir si el simulador se alinea con `stl()` |
| 20 | M7 | 3551–3552 | error | corregido | «el interior alterna estacionalidad y tendencia un número fijo de pasadas, sin esperar a que se estabilicen —en `stl()`, dos sin la opción robusta y una con ella—, y el exterior es el que reparte desconfianza. […] con `robust = TRUE` el bucle exterior da 15 vueltas; sin ella, **cero**.» | `r1_stl.out` §2: `formals(stl)` → `inner = if (robust) 1 else 2`, `outer = if (robust) 15 else 0`; sin robust `inner` 2, `outer` 0; con robust 1 y 15 | ahora 3586–3589 |
| 21 | M7 y M9 | 3587–3588 (y 4059) | error | corregido | M7: «En esa primera vuelta, de las 144 observaciones el procedimiento expulsa exactamente una […]. El ajuste completo no se queda ahí: con `robust = TRUE` las vueltas son 15, y al terminar las observaciones con peso 0 son cinco —el julio contaminado y otras cuatro (febrero de 1949, de 1951 y de 1952, y marzo de 1960), que quedan fuera igualmente cuando la serie no lleva ningún atípico añadido—, y 15, contando esas cinco, pesan menos de 0.5.» La frase que presenta la tabla dice ahora «en su primera vuelta». M9, ej. 3: «(No es el único: el ajuste robusto deja también sin peso otras cuatro observaciones, con atípico o sin él, y por eso su índice "limpio", 1.2562, no coincide con el 1.2416 del ajuste sin robustez.)» | `r1_stl.out` §4: primera pasada → peso 0 solo en la 79, \|R\| 0.3708, umbral 0.115, u 3.22, mediana 0.9461; ajuste completo → peso 0 en 2 26 38 79 135 (Feb 1949, Feb 1951, Feb 1952, Jul 1955, Mar 1960), 15 con peso < 0.5; serie limpia → 2 26 38 135; índices 1.2562, 1.2458, 1.2416, 1.2806 | ahora 3623–3628 y 4129–4131. La tabla de la primera pasada no cambia |
| 22 | M7 | 3664–3669 | error | corregido | `STL(np.log(pasajeros), period=12, seasonal=10 * n + 1, seasonal_deg=0, trend=19, robust=False)` y `.fit(inner_iter=2, outer_iter=0)`; cierra con `print(round(res.seasonal["1955-07-01"], 4))  # 0.2164, el julio de la figura` | `r1_bloques_publicados.out` (bloque leído del HTML): imprime 0.2164. `r1_stl_py.out`, variante B: julio 0.2164 constante (recorrido 0), tendencia jul-1955 5.6460, máx\|S − S_R\| 7.2e-04, máx\|T − T_R\| 2.4e-03. Antes (publicado): julio de 0.1647 a 0.2724 | ahora 3707–3719. La diferencia que queda con R viene de los saltos: con `seasonal_jump=145, trend_jump=2, low_pass_jump=2` (variante C) baja a 1e-07. No se publicaron esos tres argumentos para no recargar el bloque; **decisión que el docente puede revertir**. Sin `seasonal_deg=0` (variante D) o sin fijar las pasadas (variante A, julio 0.2153) no se reproduce |
| 23 | M7 | 3389–3393 | imprecisión | declarado | «(Para ahorrar cálculo, `stl()` no hace el ajuste en todos los instantes: por defecto lo hace cada `t.jump` —cada dos, con la ventana de este capítulo— e interpola entre ellos.)» | `r1_stl.out` §3 y §6: `$jump` → 145 2 2; máx. diferencia entre `t.jump` 2 y 1 = 0.00238; `?stl`: los saltos son para ganar velocidad y entre ellos hay interpolación lineal | ahora 3420–3422 |
| 24 | M7 | 3398–3399; 3654 | imprecisión | corregido | Prosa: «Sobre `AirPassengers`, y con la estacionalidad fijada con `s.window = "periodic"` como en este capítulo, `stl()` calcula por su cuenta una ventana de **19 meses**». Comentario del bloque R: «window = 19 es justo lo que STL calcula solo con m = 12 y season(window = "periodic") […]. Con la ventana estacional por defecto de STL(), que es 11, calcularia 21; y con trend(window = 21) esta figura sale distinta: S_julio = 1.2405.» y «R base tambien trae STL, y ahi, con s.window = "periodic", el 19 sale solo» | `r1_stl.out` §3: `stl(lx, "periodic")$win` → 1441 19 13; `stl(lx, s.window = 11)$win` → 11 21 13; `feasts`: `season("periodic")` sin `trend()` da la misma tendencia que con 19 (dif. 0); `STL(value)` por defecto = `stl(s.window = 11)` con ventana 21 (dif. 8.9e-16); `trend(window = 21)` + periodic → S_julio 1.2405. Fuente: `decomposition.txt`, §3.6, l. 494 | Decisión 4: el código no cambió, solo los comentarios (el bloque se volvió a ejecutar: S julio 0.2164 / 1.2416) |
| 25 | M7, M6, M9 | 3376, 3382–3383; 3347; 3856–3857 | imprecisión | corregido | Objetivo del M7: «…por qué es más flexible que la clásica y, cuando se activa su opción robusta, más resistente a los atípicos». 3382: «responde a esas tres debilidades una por una —a la tercera, solo si se le pide—». M6: «La descomposición STL (Módulo 7) responde a las tres, la última solo cuando se activa su opción robusta.» Resumen: «**STL** (flexible y, con `robust = TRUE`, resistente a los atípicos)» | `decomposition.txt`, §3.6, l. 471; `formals(stl)$robust` → `FALSE` | La frase del M6 está **fuera** del `<span data-afirma="c1-m6-01">`; la del M7, fuera de `c1-m7-01` |
| 26 | M7 | 3389 | divergencia / sin comprobar | **no tocado** | — | En `bibliografia/_local/` no hay texto de Cleveland (1979) ni de Cleveland y Devlin (1988) | Pasa a **R4** (T4.1/T4.2): contrastar «*locally estimated scatterplot smoothing*» o declararlo. No se rellena de memoria |
| 27 | M8 | 3744–3747, 3791–3792 | divergencia | declarado | «Para `AirPassengers`, con la STL de este capítulo —sobre el logaritmo y con `s.window = "periodic"`—, resultan $F_T = 0.994$ y $F_S = 0.937$ […]. Las cifras dependen de esa elección: con `feat_stl` de `feasts`, que deja variar el componente estacional (`s.window = 11`), sobre la misma serie en logaritmos salen 0.997 y 0.964.» | `r1_stl.out` §5: periodic → 0.994 y 0.9368; `feat_stl` sobre `log(AP)` → 0.9966 y 0.96445; `formals(feat_stl)$s.window` → 11 | ahora 3844–3849. Se escribió en el párrafo de las cifras, **fuera** del `<p data-afirma="c1-m8-01">`, que no cambió |
| 28 | M8 | 3737–3738 (JS 5349) | imprecisión | corregido | «La línea desestacionalizada ($y_t/\hat{S}_t$, con el índice $\hat{S}_t$ de la descomposición clásica multiplicativa del Módulo 6) elimina el diente de sierra mensual y deja la tendencia-ciclo junto con el residuo: por eso no es una curva suave.» | JS: `S = DATOS_CAP1.clasica_multiplicativa.estacional`; `decomposition.txt`, §3.2, l. 181 | ahora 3787–3789. Que el simulador pase a usar el índice de STL es de R3 (T3.3) |
| 29 | M8 | 3749–3751, 3762–3781 | imprecisión (notación) | declarado | «En las dos fórmulas, $T_t$, $S_t$ y $R_t$ son los componentes *estimados* —los $\hat{T}_t$, $\hat{S}_t$ y $\hat{R}_t$ de los módulos anteriores, escritos sin gorro para aligerar—.» | `features.txt`, §4.3, l. 97–99 (la fuente también los escribe sin gorro) | ahora 3842–3843. Las fórmulas y la derivación no se reescribieron |
| 30 | M9, ej. 1 | 3900, 3916, 3929–3940 | error | corregido | Cabecera: «**Respuesta: con `co2` el criterio apunta a la multiplicativa, pero elegir una u otra cambia muy poco** — y distinguir esas dos cosas es justamente el aprendizaje.» Veredicto de `co2`: «Descarta la aditiva; compatible con la multiplicativa». Prosa: «En `co2` el intervalo es mucho más ancho —va de 0.58 a 1.59, con un $R^2$ de 0.335—, pero deja fuera el 0 y contiene el 1: **los datos descartan la aditiva y son compatibles con la multiplicativa**. […] **la elección importa poco**: no porque los datos no distingan, sino porque la diferencia entre las dos es pequeña.» | `r1_ejercicio1.out`: b = 1.083, IC [0.575, 1.591], R² 0.335; excluye 0 → TRUE; contiene 1 → TRUE. «Importa poco»: máx. diferencia entre la desestacionalizada aditiva y la multiplicativa de `co2` = 0.26 ppm sobre una amplitud estacional de 6.25 ppm (en `AirPassengers`, 51.1 sobre 117.4) | ahora 3959–3960, 3990 y 3996–4007. Enunciado, pista y código sin tocar |
| 31 | M9, ej. 1 | 3941–3945 | error | corregido | «la amplitud estacional del CO₂ **sí** crece, a razón de $+0.024$ ppm por año ($p = 0.0002$), y ese crecimiento es el que predice la proporcionalidad: una amplitud que fuera siempre la misma fracción del nivel crecería $+0.023$ ppm por año, y el cociente entre amplitud y nivel no muestra tendencia ($p = 0.85$). Una descomposición aditiva de índices fijos no puede recogerlo; una multiplicativa sí, porque aplica sus índices fijos sobre un nivel que sube. También lo recoge **STL** con una ventana estacional finita, […] pero aquí no es un argumento para preferirla: a la multiplicativa le basta.» | `r1_ejercicio1.out`: pendiente 0.0239 ppm/año (p = 0.00021); pendiente bajo proporcionalidad 0.0226; cociente: pendiente 3.3e-06, p = 0.85; la multiplicativa de índices fijos implica una amplitud de 5.86 → 6.75 ppm; `stl(co2, s.window = 11)` → 5.85 → 6.72 ppm; con `"periodic"`, 6.17 fija | ahora 4008–4014. El cierre «buen argumento para preferir STL aquí» **no seguía en pie** y se reescribió |
| 32 | M9, ej. 1 | 3935–3936 | imprecisión | corregido | «…la aditiva queda descartada. Pero el intervalo excluye también el 1: la amplitud crece *más* que en proporción al nivel, que es el "tampoco es un multiplicativo de manual" del Módulo 4.» Veredicto de `AirPassengers`: «Descarta la aditiva y la multiplicativa exacta: la amplitud crece más que el nivel» | `r1_ejercicio1.out`: b = 1.291, IC [1.149, 1.432]; excluye 1 → TRUE | No se menciona Box–Cox con λ < 0 (sugerencia del par): es contenido nuevo → R5 |
| 33 | M9, ej. 1 | 3919–3921, 3938–3939 | imprecisión (menor) | corregido | Comentario del código: «# La clave esta en cuanto recorre cada serie en proporcion a su media / # (maximo menos minimo de toda la serie: tendencia y vaiven estacional juntos):». Prosa: «el nivel medio anual del CO₂ solo sube un 15 % en 39 años (de 315.8 a 363.8 ppm), mientras que el de `AirPassengers` se multiplica por 3.76; las dos últimas líneas del código lo resumen con el recorrido total de cada serie frente a su media, 16 % y 185 %.» | `r1_ejercicio1.out`: medias anuales 315.8 → 363.8, +15.2 %, 39 años; AP ×3.76; `(max − min)/mean` = 0.159 y 1.848 | Solo cambió el comentario, no el código (decisión 6). La prosa responde ya a la pregunta de la pista con la cifra correcta |
| 34 | M9, ej. 2 | 3962 | imprecisión (menor) | corregido | «`USAccDeaths` (estacionalidad marcada y una tendencia bastante más débil)» | `r1_stl.out` §5: FT 0.7991, FS 0.9426 | ahora 4031–4032 |
| 35 | M9 | 3864–3865 | error (impacto bajo) | corregido | «Ocho preguntas para comprobar lo esencial. En las de respuesta única cada opción tiene su explicación; en las numéricas y en la de selección múltiple la explicación es una para el acierto y otra para el fallo. Si te equivocas, la retroalimentación te dice dónde estuvo el razonamiento.» | `AUTOEVALUACIONES['cap1']`: 8 objetos (4 `opcion`, 1 `grafico`, 2 `numerica`, 1 `multiple`); en el navegador, «Respondidas 0 de 8» | ahora 3921–3924 |
| 36 | quiz P2 | 6031 | imprecisión | corregido | «El residuo delataría el problema: su dispersión, medida año por año, dibuja una U —grande en los dos extremos de la serie y mínima hacia 1954 y 1955—, como muestra el Módulo 6.» | `r1_m2_m4_m6.out`: sd anual 30.5 20.7 22.4 17 14.5 5.6 6.1 10 17.2 29.4 29.4 25.4; mínimas 1954 y 1955 | ahora 6103. Opciones, orden y correcta sin tocar |
| 37 | quiz P3 | 6058 | imprecisión | corregido | «Con $m$ par, la media móvil centrada $2\times m$ necesita $m/2$ observaciones a cada lado, así que se pierden $m$ en total: aquí, 6 al principio y 6 al final.» | `decomposition.txt`, §3.3, l. 220 (la 5-MA pierde dos por lado) y §3.4, l. 397 | ahora 6130 |
| 38 | quiz P8 | 6164 | divergencia | corregido | «Ajustada, la comparación ya no arrastra el patrón anual. Pero la serie ajustada conserva el residuo, así que una subida o una bajada de un mes al siguiente todavía puede engañar: para leer cambios de rumbo conviene mirar la tendencia-ciclo.» | `decomposition.txt`, §3.2, l. 181 | ahora 6236 |
| 39 | M9 | 4071–4072 | laguna (menor) | corregido | «**caps. 1–3** — patrones temporales y descomposición—, y la **sección 4.3** para las fuerzas $F_T$ y $F_S$.» | `features.txt`, l. 93 («4.3 STL Features») y l. 97–99 (definiciones) | ahora 4143–4144. No es un `<cite>`. Las secciones exactas del resto de la lista son de R4 (T4.2) |
| 40 | M9 y quiz P2 | 3835; 6041 | imprecisión (menor) | corregido (3835) | «transformar con logaritmos o, más en general, con una transformación de Box–Cox (una familia de transformaciones que incluye al logaritmo y a las potencias)» | `decomposition.txt`, §3.1, l. 70 | ahora 3891–3892. La retro de la P2 (6041) **no se tocó** (decisión 10: en el quiz, solo las tres frases señaladas); el quiz está en el M9, después de esa glosa |
| 41 | M9 | 4074–4075 | sin comprobar | **no tocado** | — | En `bibliografia/_local/texto/` solo está `shumway2011time` (3.ª ed.) | Pasa a **R4**; depende de la decisión abierta sobre la edición de Shumway y Stoffer (plan, §7.4) |

---

## Fuera de los 41: decisiones 7, 8 y 9 del encargo

| asunto | línea orig. | qué quedó escrito | evidencia |
|---|---|---|---|
| Ciclos económicos, M4 | 2658–2659 | «las fluctuaciones cíclicas no tienen una duración fija y suelen durar al menos dos años, de modo que en una serie tan corta caben pocas, y un ciclo largo del que solo se ve un tramo es indistinguible de una tendencia que sube» (antes: «un ciclo económico de siete u ocho años cabría ahí una vez y media») | `graphics.txt`, §2.3 «Time series patterns», l. 356 (definición de *Cyclic*) y l. 367 (ejemplo de las letras del Tesoro: una tendencia que sería parte de un ciclo largo) |
| Ciclos económicos, quiz P1 | 6008 | «las subidas y bajadas de un ciclo económico no tienen duración fija —suelen durar al menos dos años—, y no se sabe de antemano cuánto durará la siguiente» (antes: «puede durar 4 años o 9») | la misma |
| `DATOS_CAP1.descripcion` | 4108 y tres archivos de `precalculo/` | «…segun FPP3 seccion 4.3, calculada sobre STL.» en los cuatro sitios | `grep -c 'segun FPP3 seccion 3.6'` → 0 en los cuatro; `…4.3` → 1 en cada uno; `git diff --numstat` → 1/1 en los tres de `precalculo/` |
| «Seis preguntas» | 3864 | ver fila 35 | — |

**Frase leída para que R4 la cite (ciclos):** FPP3 §2.3, definición de *Cyclic*, `graphics.txt` l. 356:
«The duration of these fluctuations is usually at least 2 years.» El mismo párrafo dice que las subidas y bajadas
no tienen frecuencia fija y que suelen deberse a las condiciones económicas (el «business cycle»); la l. 358
añade que, en general, los ciclos son más largos que el patrón estacional y de magnitud más variable. El
ejemplo 1 de la figura 2.3 (l. 366) habla de un comportamiento cíclico de entre 6 y 10 años en una serie
concreta: no se usó, porque es un caso y no una regla.

---

## Cifras que cambiaron (antes → después, y dónde)

| cifra | antes | después | dónde |
|---|---|---|---|
| Tendencia de jul-1955 que calcula el bloque R del M5 | 284 | 285.75 | salida del bloque (ahora impresa como control) |
| Tendencia de jul-1955 del bloque pandas del M5; huecos | 284.0; 11 | 285.75; 12 | comentarios de control del bloque |
| Filtro del paso 2 del M6 en jul-1955; `NA` | 287.5; 11 | 285.75; 12 | ficha «Con qué» del paso 2 |
| Julio estacional del bloque Python de STL | de 0.1647 (1949) a 0.2724 (1960) | 0.2164 fijo | bloque Python del M7 (control impreso) |
| Proporción amplitud/nivel | «sube del 35 % al 49 %» | 35 % (1949) y 49 % (1960), mínimo 32 % (1951), máximo 51 % (1958) | M4, prosa tras `amplitud-nivel` |
| Factor de la amplitud en logaritmos | «poco más de uno» | 1.32 | M4, prosa tras `serie-vs-log` |
| Pesos tricúbicos de `stl()` (nuevos) | — | 0.8930, 0.3485 y 0 a 3, 6 y 9 meses | M7, tras la tabla (la tabla conserva 0.9212, 0.4819, 0.0199) |
| Pasadas de los bucles (nuevas) | «hasta que se estabilizan» | interior: 2 sin robust, 1 con; exterior: 15 con robust, 0 sin | M7 |
| Observaciones con peso 0 | «exactamente una» | una en la primera vuelta; cinco al terminar (15 con peso < 0.5) | M7; eco en la solución del ej. 3 |
| $F_T$ y $F_S$ con `feat_stl` (nuevas) | — | 0.997 y 0.964 (junto a 0.994 y 0.937, que no cambian) | M8 |
| Subida del nivel del CO₂ | «16 % en 39 años» | 15 % (315.8 → 363.8 ppm); el 16 % queda como recorrido/media | M9, ej. 1 |
| Nivel de `AirPassengers` | «casi cuatro» | 3.76 | M9, ej. 1 |
| Crecimiento de la amplitud bajo proporcionalidad; p del cociente (nuevas) | — | +0.023 ppm/año; p = 0.85 | M9, ej. 1 |
| Número de preguntas | Seis | Ocho | M9, intro del quiz |
| Duración de los ciclos | «siete u ocho años», «una vez y media»; «4 años o 9» | «al menos dos años» | M4 y retro de la P1 |
| Sección de FPP3 en `descripcion` | 3.6 | 4.3 | HTML y tres archivos de `precalculo/` |
| Unidades | «pasajeros» | «mil / miles de pasajeros» | fila 3 |

No cambió ninguna cifra del M6 (285.75, 1.2266, 1.0386, 63.83, 14.42, 28.7, 107.9, las series de once y de doce
valores), ni las del simulador de Loess, ni las tablas de los ejercicios 2 y 3.

## Afirmaciones `data-afirma` cuyo texto cambió

- **`c1-m6-01`** (M6, aviso de limitaciones): «los primeros y últimos $m/2$ valores» → «los primeros y últimos
  $m/2$ valores si $m$ es par, y $(m-1)/2$ si es impar». `audita_citas.py` lo detecta: **F09**, huella actual
  `6e395a989b440d73`, pasa a `por-reverificar`. Hay que volver a verificar la entrada en
  `bibliografia/contraste/cap1.yml` (R4). No se tocó `bibliografia/`.
- `c1-m7-01`, `c1-m7-02`, `c1-m7-03` y `c1-m8-01`: sin cambios (lo añadido en el M7 y en el M8 está fuera de
  esos elementos).

## Roto y fuera del informe del par

1. **M6, desarrollo de la normalización, paso 2 (l. 3155–3160 orig.; sin corregir).** Dice que, si el factor
   $\bar s$ se dejara en los índices, «El residuo dejaría de oscilar alrededor de 1 para hacerlo alrededor de
   1.0018». En R es al revés: el residuo **sin** normalizar promedia exactamente 1 (cada índice bruto es la media
   de su propio mes) y el residuo **normalizado**, el que devuelve `decompose()`, promedia 0.998236
   (`r1_m2_m4_m6.out`: «media del residuo CON normalizar: 0.998236 · SIN normalizar: 1»). La igualdad de la
   fórmula es correcta; la lectura que se hace de ella, no. El paso 3 (la desestacionalizada desplazada un
   0.18 %) y el resultado final sí se sostienen. La corrección del par a la l. 3168 («deja $\hat R$ centrado en
   1») tiene el mismo defecto. No se arregló porque no está en la especificación y pide rehacer el argumento del
   paso. Propuesta: «Sin normalizar, el residuo promediaría exactamente 1 y serían los índices los que no
   promediarían 1; al normalizar, el factor pasa al residuo, cuya media queda en 0.9982».
2. **Quiz P2, opción correcta:** «Multiplicativa, o equivalentemente aditiva sobre el logaritmo». Es la misma
   equivalencia que se corrigió en el comentario del M6 (fila 14): vale para el modelo, no para el estimador
   clásico (1.2347 frente a 1.2266). No se tocó (decisión 10); R5 rehace la P2.
3. **M9, ej. 2, solución:** «las muertes accidentales suben y bajan sin una dirección clara» con $F_T$ = 0.80.
   El par solo señaló la pista; la solución no se tocó. R5.
4. **M9, ej. 1:** el enunciado pide «Justifica con el gráfico estacional» y la solución no muestra ninguno; la
   pista pregunta cuánto sube el nivel y el código calcula recorrido/media. La prosa da ya las dos cifras. R5
   rehace el ejercicio.
5. **M6, ficha del paso 3:** «STL lo hace variar en el tiempo», sin la condición (solo con `s.window` finito;
   la figura del capítulo usa `"periodic"`). R3.
6. **`autoplot()` sobre un `tsibble`:** con `fabletools` 0.6.0 avisa de que está en desuso y remite a `ggtime`.
   Los bloques funcionan; el aviso aparece en todos los bloques R que dibujan. A tener en cuenta en T5.4.
7. **Hallazgos del piloto que siguen abiertos** (no eran de esta ronda): el desarrollo del acrónimo STL en
   `c1-m7-01` y la cuarta limitación del método clásico que da FPP3 §3.4.

## Comprobaciones finales (desde la raíz del worktree)

| orden | resultado |
|---|---|
| `python3 precalculo/genera_referencias.py --comprobar` | OK en los seis capítulos; cap. 1: «3 citas, sin cambios» |
| `python3 precalculo/cuenta_sitio.py` | FALLA con las mismas 8 cifras que antes (68/70 simuladores y 12/14 del cap. 5). Comparado con `HEAD` (`git archive`): la única diferencia en la salida es el tamaño del cap. 1, 287 → 295 KB |
| `python3 precalculo/audita_posicion_correcta.py` | «17 quizzes auditados en 12 archivos. Ningún instrumento concentra las correctas.» |
| `python3 precalculo/audita_citas.py` | FALLA, 1 hallazgo: **F09** en `c1-m6-01` (el esperado) |
| `python3 precalculo/verifica_todo.py` | 9 de 11 en verde; fallan las dos anteriores. `compila_tailwind.py --comprobar` en verde (no hay clases nuevas) |
| Navegador, `http://localhost:8731/capitulo-1-componentes-descomposicion.html` | Los 9 módulos cargan sin errores de consola ni de KaTeX (0 `.katex-error`), con derivaciones, pistas y soluciones abiertas; 8 preguntas en el quiz |


## Después de la verificación independiente (2026-11-11)

Un verificador que no redactó (Opus 5.5, contexto limpio) revisó el diff entero, reejecutó los bloques
publicados y buscó restos de las versiones viejas en todo el capítulo. Encontró siete problemas; la
sesión que dirige confirmó sus cifras en R (`comprobaciones/r1_verificacion_maestra.out`,
`r1_normalizacion.out`) y los corrigió:

| Dónde | Qué estaba mal | Qué quedó |
|---|---|---|
| M6, derivación de la normalización | **Error que el diagnóstico no vio** (lo encontró el redactor): «sin normalizar, el residuo oscilaría alrededor de 1.0018». Es al revés: sin normalizar promedia 1; normalizado, 0.9982 | La derivación dice qué componente carga el factor constante y por qué conviene que sea el residuo |
| M6, párrafo que introduce el paso 3c | Resto de la versión vieja: «los dos pasos siguientes salen desplazados» | Se desplazan los índices y lo que se calcule dividiendo por ellos |
| M7, robustez | «Las demás siguen contando casi por entero» era falso: en la primera vuelta otras 12 observaciones quedan por debajo de 0.5 | Se dicen las dos cosas: 12 por debajo de 0.5 y la mitad de las demás por encima de 0.94 |
| M9, ejercicio 3 | Atribuía la diferencia 1.2562 / 1.2416 a cuatro observaciones sin peso | El ajuste robusto reparte pesos entre todas (4 sin peso y 18 por debajo de 0.5 en la serie limpia) |
| M9, ejercicio 1 | «Descarta la multiplicativa exacta» dependía de la medida máx − mín | «Con esta medida»; y la cifra con la amplitud sobre la serie sin tendencia: b = 1.18, [0.95, 1.41] |
| M9, ejercicio 2 | «Suben y bajan sin una dirección clara» contradecía F_T = 0.80 | La tendencia existe, es más débil y cambia de sentido (medias anuales 9652 → 8395 → 8802) |
| M2, tabla | «`freq="MS"` solo declara que el dato es mensual» | statsmodels deduce de ahí el período 12 |
| M7, bloque Python de STL | «Con los mismos ajustes que el bloque de R» | «Equivalentes», con la diferencia medida: < 0.001 en lo estacional y < 0.003 en la tendencia |
| Lecturas | Raya de inciso asimétrica | Corregida |

Se deja como está, a sabiendas: la opción correcta de la P2 del quiz («o equivalentemente aditiva sobre el
logaritmo») es cierta para el modelo, que es de lo que habla la pregunta; la P2 se rehace en R5.

El verificador reverificó además contra FPP3 la afirmación `c1-m6-01`, cuya prosa cambió: sigue `con-matiz`
y su entrada en `bibliografia/contraste/cap1.yml` lleva la huella nueva y dos citas de §3.3.
