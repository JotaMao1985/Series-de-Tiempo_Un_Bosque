# Capítulo 1 · ronda R3 («estructura») · cambios

## Primera mitad · T3.1 (gráficos del Módulo 3) y Loess alineado con `stl()`

Fecha: 2026-11-11. Un solo redactor; sin commit. La segunda mitad de la ronda añade su parte debajo.

- Archivo tocado: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (488 líneas más, 47 menos). Nada más,
  salvo guiones y salidas en `diagnostico/cap1/comprobaciones/r3a_*` y `diagnostico/cap1/herramientas/r3*`.
- Módulos con cambios: **3** y **7**. Los módulos 1, 2, 4, 5, 6, 8 y 9 quedan byte a byte como estaban (comprobado
  contra la copia de antes). `DATOS_CAP1` no cambió; `precalculo/genera_datos.R` no se ejecutó.
- No se tocó ningún `<cite>`, ningún marcador `<!--…-->` ni ningún `data-afirma`: los cinco `data-afirma` conservan
  su texto exacto (**ninguno hay que volver a contrastar**).
- No hay clases nuevas de Tailwind (`compila_tailwind.py --comprobar` sale en 0). Hay una regla nueva de CSS propio:
  `.grafico-wrapper--cuadrado` (l. 1902).
- Capturas (ignoradas por git): `diagnostico/cap1/capturas/r3/`, con sufijos `-escritorio` (1200 px), `-800` y
  `-movil` (375 px).

### 1. Lo que se añadió al Módulo 3

Orden nuevo del módulo (l. 2788–3001): apertura con los cuatro gráficos → **mapa estacional presentado** («La serie
como tabla: mes × año») → gráfico estacional → nota del abanico → nota de las varias estacionalidades → **gráfico de
subseries** → **gráfico de rezagos** → nota «De la nube al número» → código → cierre «Lo que cada gráfico deja
abierto». El hilo es la tabla de doce años por doce meses: leída por filas da el gráfico estacional y leída por
columnas, el de subseries; el de rezagos quita el tiempo del eje.

| Qué | Dónde | Detalle |
|---|---|---|
| Lista de los cuatro gráficos | l. 2808–2819 | Las viñetas de subseries y de rezagos dicen ahora qué deja ver cada uno. Las de tiempo y estacional, sin cambios (la palabra «ciclo» es de T3.5) |
| Párrafo puente | l. 2821–2823 | El gráfico de tiempo ya se leyó en el M1; los otros tres salen de reordenar los 144 datos en una tabla 12 × 12 |
| **Mapa estacional, presentado** | l. 2825–2839 | `<h3>` y un párrafo antes del mapa: filas = años, columnas = meses, el color hace de eje vertical; «no es uno de los cuatro gráficos, sino la tabla de la que salen dos de ellos». El marcado y la nota del mapa no cambian |
| Gráfico estacional | l. 2841–2858 | `<h3>` y un párrafo que lo liga al mapa (cada fila, una línea) y al gráfico de tiempo. El simulador no cambia |
| Nota «Cómo leer el abanico» | l. 2859–2866 | **Movida** (antes cerraba el módulo), texto idéntico: ahora va pegada al gráfico que lee |
| Nota de las varias estacionalidades | l. 2868–2879 | **Movida** de antes del primer gráfico a después del estacional (lo pedía el lector estudiante), texto idéntico |
| **Simulador `subseries-estacionales`** (nuevo, estático) | HTML l. 2890–2901 · JS l. 5433 | Un lienzo, eje vertical compartido (100–700, «Miles de pasajeros»): doce paneles, uno por mes, cada uno con sus doce años (verde oscuro) y una raya en la media del mes (turquesa, el color del componente estacional). Leyenda en HTML, `role="img"`, `aria-label` que dice lo que se ve, lectura calculada en JS. Iniciales de mes y título de eje en dos líneas en lienzos estrechos |
| Prosa de subseries | l. 2883–2888 y 2903–2907 | Qué corta (columnas del mapa), qué muestran las medias y qué muestra el interior de cada panel; lectura sobre AirPassengers (todos suben; julio +474 y noviembre +286); se define **subserie** y se anuncia el M7 |
| **Simulador `grafico-rezagos`** (nuevo, con control) | HTML l. 2918–2930 · JS l. 5570 | Dispersión de $y_t$ (vertical) contra $y_{t-k}$ (horizontal), con deslizador «Rezago (k), en meses» de 1 a 12 (arranca en 1). Lienzo **cuadrado** y ejes con los mismos límites (100–700), de modo que la recta de valores iguales es la diagonal (gris, discontinua). Los puntos cuyo $y_t$ es julio o agosto van en turquesa. Leyenda en HTML; lectura con `aria-live="polite"` y `aria-label` que cambian con $k$; títulos de eje con «miles de pasajeros», en dos líneas en lienzos estrechos |
| Prosa de rezagos | l. 2911–2916 y 2932–2940 | Qué es el gráfico; lectura de $k = 6$ (estación opuesta, nube abierta, 0.784) y de $k = 12$ (mismo mes, nube cerrada, 0.991; 127 de 132 puntos sobre la diagonal = tendencia). Aquí se ve por primera vez la «dependencia temporal» del M1 |
| Nota «De la nube al número» | l. 2942–2948 | Puente al capítulo 2: la cifra de la lectura es la correlación de la nube; el coeficiente de autocorrelación $r_k$ se calcula con la media de la serie entera y **no da lo mismo** (en $k = 12$, 0.760 y no 0.991). El 0.760 es el que ya publica el capítulo 2 (su l. 2512 y 2533) |
| Código | l. 2966 y 2982–2989 | R: `gg_lag(…, geom = "point", lags = 1:12)`, para que dibuje puntos como la figura. Python: se añaden el gráfico de subseries (`statsmodels…month_plot`) y el de rezagos (`plt.figure()` + `pd.plotting.lag_plot(pasajeros, lag=12)`), que el bloque no tenía |
| Cierre | l. 2993–2999 | Nota «Lo que cada gráfico deja abierto»: qué dejó cada uno de los cuatro y dónde sigue (M4, M7, capítulo 2) |
| Remisión en el M7 | l. 3978 | En «subserie de ciclo»: «Son los doce paneles del gráfico de subseries del Módulo 3.» |

El objetivo del módulo no se cambió: ya nombraba los cuatro gráficos y ahora los cuatro están.

**Lo que muestra la lectura de cada simulador** (leído con Chrome sin ventana, `comprobaciones/r3a_m3_simulador.out`):

- Subseries: «Las medias, en miles de pasajeros: la más alta es la de julio (351.3) y la más baja, la de noviembre
  (232.8). Dentro de cada panel: julio pasa de 148 en 1949 a 622 en 1960 (+474); noviembre pasa de 104 en 1949 a 390
  en 1960 (+286).»
- Rezagos, $k = 6$: «138 puntos, cada uno un mes frente al de 6 meses antes. Su correlación es 0.784, la más baja de
  los doce rezagos. Los julios y los agostos (turquesa) se comparan con los eneros y los febreros: 24 de 24 quedan
  por encima de la diagonal.»
- Rezagos, $k = 12$: «132 puntos […]. Su correlación es 0.991, la más alta de los doce rezagos. Cada mes se compara
  con el mismo mes del año anterior: 127 de los 132 puntos quedan por encima de la diagonal.»

**Cifras nuevas del M3 y su evidencia.** Todas se calculan en JavaScript sobre `DATOS_CAP1.observado` y se recalculan
en R sobre `datasets::AirPassengers` (`comprobaciones/r3a_m3.R` → `r3a_m3.out`; la serie incrustada es idéntica a la
de R). `comprobaciones/r3a_m3_compara.py` → `r3a_m3_compara.out` compara las dos fuentes: **100 comprobaciones, 0
fallos**.

| Cifra | Dónde aparece | R |
|---|---|---|
| Correlación de la nube, $k = 1 \dots 12$: 0.960 0.896 0.837 0.798 0.786 0.784 0.785 0.792 0.828 0.883 0.950 0.991 | lectura y `aria-label` del simulador; 0.784 y 0.991 también en la prosa | `cor(y[(k+1):n], y[1:(n-k)])`, §2. Baja sin excepción de 1 a 6 y sube sin excepción de 6 a 12 |
| Puntos por rezago: 143, 142, …, 132 | lectura | $n - k$ |
| Julios y agostos por encima de la diagonal: 17 de 24, 24 de 24 (k = 2…6), 23 de 23, 22 de 22 (k = 8…11) | lectura | §2, «puntos con y_t en julio o agosto» |
| $k = 6$: los eneros y febreros, frente a julios y agostos, todos por debajo | prosa | 22 de 22, §2 |
| $k = 12$: 127 de 132 por encima (3 por debajo, 2 iguales) | lectura y prosa | §2; los cinco que no suben son feb, mar y abr de 1954 (bajan) y abr y sep de 1958 (iguales) |
| $r_{12} = 0.760$ | nota «De la nube al número» | `acf(y)`: 0.7604 |
| Medias: julio 351.3 (la más alta), noviembre 232.8 (la más baja) | lectura de subseries | §1 |
| Julio 148 → 622 (+474); noviembre 104 → 390 (+286) | lectura y prosa («474 mil», «286 mil») | §1 |
| «todos suben» | prosa | §1: los doce meses valen más en 1960 que en 1949; solo hay 3 bajadas de un año al siguiente en 132 (feb, mar y abr de 1954) |
| Los cuatro gráficos en R y las líneas nuevas de Python corren | bloque de código | `r3a_m3.out` §3 (con `feasts`; `fpp3` no está instalado) y `r3a_m3_python.py` → `.out` (statsmodels 0.14.6, pandas 2.3.3): `month_plot` dibuja las 12 medias de R; `lag_plot(lag=12)` dibuja 132 puntos con correlación 0.9905 |

**Frases de FPP3 leídas que respaldan cada afirmación nueva (para R4).** Fuente:
`bibliografia/_local/web/hyndman2021forecasting/graphics.txt` (capítulo 2, «Time series graphics»). No se añadió
ningún `<cite>`.

| Afirmación del M3 | Sección · línea del archivo | Frase leída |
|---|---|---|
| El gráfico estacional son los mismos datos del gráfico de tiempo, con los años superpuestos | §2.4 Seasonal plots · l. 373 y 381 | «A seasonal plot is similar to a time plot except that the data are plotted against the individual “seasons” in which the data were observed.» · «This is the same data as was shown earlier, but now the data from each year overlap.» |
| …y eso permite comparar la forma de un año con la de otro | §2.4 · l. 381 | «…allows the underlying seasonal pattern to be seen more clearly, and is especially useful in identifying years in which the pattern changes.» |
| (Nota movida, texto sin cambios) varias estacionalidades y `period` | §2.4, «Multiple seasonal periods» · l. 387 | «Where the data has more than one seasonal pattern, the period argument can be used to select which seasonal plot is required.» |
| Subseries: los datos de cada mes, reunidos en una serie pequeña en su propio panel | §2.5 Seasonal subseries plots · l. 413 | «…the data for each season are collected together in separate mini time plots.» |
| Una raya en la media de cada mes | §2.5 · l. 424 | «The blue horizontal lines indicate the means for each month.» |
| Las doce medias son el patrón estacional; dentro de cada panel se ve cómo cambia ese mes con los años | §2.5 · l. 424 | «This form of plot enables the underlying seasonal pattern to be seen clearly, and also shows the changes in seasonality over time. It is especially useful in identifying changes within particular seasons.» |
| Rezagos: $y_t$ contra $y_{t-k}$, con el valor rezagado en el eje horizontal, un gráfico por $k$ | §2.7 Lag plots · l. 563 | «…where the horizontal axis shows lagged values of the time series. Each graph shows y_{t} plotted against y_{t-k} for different values of k.» |
| `gg_lag(…, geom = "point")` | §2.7 · l. 568 | `gg_lag(Beer, geom = "point")` |
| Color según la estación del valor del eje vertical (aquí, solo julio y agosto) | §2.7 · l. 573 | «Here the colours indicate the quarter of the variable on the vertical axis.» |
| En el rezago estacional la relación es más fuerte; en el de media estación se enfrentan picos con valles | §2.7 · l. 573 | «The relationship is strongly positive at lags 4 and 8, reflecting the strong seasonality in the data. The negative relationship seen for lags 2 and 6 occurs because peaks (in Q4) are plotted against troughs (in Q2)» |
| La correlación en $k = 6$ sigue siendo alta por la tendencia | §2.8, «Trend and seasonality in ACF plots» · l. 617 | «When data have a trend, the autocorrelations for small lags tend to be large and positive because observations nearby in time are also nearby in value.» (apoyo parcial: la frase del capítulo es una lectura propia de las cifras) |
| El capítulo 2 resume cada nube en un coeficiente de autocorrelación, uno por rezago | §2.8 Autocorrelation · l. 577 y 579 | «…autocorrelation measures the linear relationship between lagged values of a time series.» · «There are several autocorrelation coefficients, corresponding to each panel in the lag plot.» |
| …y los dibuja juntos en el correlograma | §2.8 · l. 600 | «We usually plot the ACF to see how the correlations change with the lag k. The plot is sometimes known as a correlogram.» |
| $r_k$ resta a todos los valores la media de la serie entera | §2.8 · l. 581 | La fórmula de $r_k$: numerador $\sum_{t=k+1}^{T}(y_t-\bar y)(y_{t-k}-\bar y)$ y denominador $\sum_{t=1}^{T}(y_t-\bar y)^2$ |

Sin respaldo en FPP3 (son **propias** y así habría que declararlas en R4): el mapa estacional como «tabla de la que
salen dos gráficos» (filas y columnas); la lectura de AirPassengers en los dos gráficos (todas sus cifras salen de
R); que en AirPassengers la relación en $k = 6$ no sea negativa, a diferencia del ejemplo de la cerveza del libro; y
que la diferencia entre la correlación de la nube y $r_k$ se deba a la media con la que se centra (FPP3 da la fórmula,
no la comparación).

### 2. Loess alineado con `stl()`: cifras del M7, antes → después

Cambio de cálculo, uno solo: en `ajusteLocal` (JS l. 6156–6158) el radio pasa de
`Math.max(…|i − foco|) + 1` a `Math.max(…|i − foco|)`. Se actualizaron los dos comentarios del código. No se tocó nada
más del simulador (controles, colores, dos lienzos, textos de la lectura).

Evidencia, con dos fuentes que coinciden:
- **Simulador**, leído con Chrome sin ventana: `comprobaciones/r3a_loess_simulador.json` → `.out`.
- **Réplica en R** del ajuste local sobre los mismos vectores incrustados: `comprobaciones/r3a_loess.R` → `.out`.
- `comprobaciones/r3a_loess_compara.py` → `.out`: la curva del simulador y la de R, a 4 decimales, **144 de 144
  iguales**.

| Cifra | Antes | Después | Dónde aparece | Evidencia |
|---|---|---|---|---|
| Radio de la ventana centrada de 19 | 10 meses («un paso más») | 9 meses | párrafo antes de la tabla (l. 3835) | R §1 |
| $u$ a 3, 6 y 9 meses | 0.3 · 0.6 · 0.9 | $3/9$ · $6/9$ · $9/9$ | tabla de pesos (l. 3846–3849) | R §1 |
| Peso a 3 meses | 0.9212 | **0.8930** | tabla | R §1 · simulador (pesos de la ventana) |
| Peso a 6 meses | 0.4819 | **0.3485** | tabla | ídem |
| Peso en el borde | 0.0199 | **0** | tabla, prosa, comentario del JS | ídem |
| «el mes del borde cuenta unas 50 veces menos» | 50 | **retirada**; en su lugar: «de los 19 meses solo 17 pesan algo; y el que queda a seis meses cuenta ya casi tres veces menos» | l. 3853–3857 | R §1: 17 de 19 con peso > 0; $1/w(6/9) = 2.87$ |
| «cae hasta casi desvanecerse en el borde» | — | «cae hasta anularse en el borde» | l. 3829 | — |
| Dic. 1960, recta − nivel | 0.0498 | **0.0475** | segunda lectura (l. 3895) y paso 4 de la derivación (l. 3949) | simulador: 6.2048 y 6.1573 · R §2 |
| Dic. 1960, ajuste local (recta) | 6.2043 | **6.2048** | segunda lectura | simulador · R §2 |
| Dic. 1960, tendencia de `stl()` | 6.2048 | 6.2048 (sin cambio; ahora «la misma cifra que `stl()`») | segunda lectura | dato incrustado |
| Dic. 1954, grado 0 y pesos planos = media móvil | 5.5482 | 5.5482 (sin cambio: con pesos planos el radio no interviene) | tercera lectura | simulador · R §2 |
| Dic. 1954, ajuste local (estado inicial del simulador) | 5.5439 | **5.5428** | antes solo en la lectura del simulador; ahora también en la prosa (l. 3903) | simulador · R §2 |
| Dic. 1954, tendencia de `stl()` | 5.5432 | 5.5432 (sin cambio) | lectura; ahora también en la prosa | dato incrustado |
| Dic. 1954, nivel y recta «el mismo número hasta el cuarto decimal» | sí | sí (idénticos con todos los decimales) | segunda lectura | R §2 |
| Ene. 1949, ajuste local | 4.8266 | **4.8294** (= `stl()`, 4.8294) | solo en la lectura del simulador | simulador · R §2 |
| «le faltan nueve meses de un lado», «12 de las 144 sin estimar» | — | sin cambio (no dependen del radio) | primera lectura y prosa | R §2 |

Buscadas en todo el archivo y **ya no aparecen**: 0.0199, «50 veces», 6.2043, 0.0498, 0.9212, 0.4819, «un paso
más», «10 meses». 5.5439 nunca estuvo en la prosa (salía en la lectura). 5.5432 y 6.2048 siguen: son la tendencia
de `stl()`.

**Ejercicio 3 y quiz:** ninguna de sus cifras sale del simulador ni de la convención del radio (todas vienen de
`stl()` con y sin `robust`); no se cambió nada. Tampoco el comentario del bloque Python del M7 («menor de 0.001 en el
componente estacional y de 0.003 en la tendencia»), que sigue siendo cierto.

**Texto que cambia además de las cifras** (M7):
- La declaración de las dos convenciones que puso R1 (antes y después de la tabla) se quitó; queda una sola: el radio
  es la distancia al vecino más lejano, «así lo toma `stl()` y así lo toma el simulador».
- Intro del simulador: se añade «(los del borde de la ventana se quedan en un punto: pesan 0)», porque ahora los
  vecinos del borde se dibujan con el tamaño mínimo.
- Tercera lectura: se dice en qué foco se obtiene («con el foco de nuevo en diciembre de 1954»), que pedía el lector.
- Derivación, paso 4: se añade «y uno de vecinos que están todos hacia el pasado, algo demasiado bajo», porque el
  ejemplo que sigue es diciembre de 1960, donde el nivel queda por debajo de la recta (R §2: −0.0475; en enero de
  1949, +0.0096).
- Párrafo nuevo tras las tres lecturas (l. 3901–3909), con la explicación de por qué el simulador y `stl()` no dan
  siempre la misma cifra (ver §3).

### 3. Con qué exactitud coincide ahora el simulador con `stl()`

`comprobaciones/r3a_loess.out`, §3 y §4. La comparación es con la tendencia incrustada, que es
`stl(log(AirPassengers), s.window = "periodic")` redondeada a 4 decimales (comprobado: idéntica).

| | Antes (radio + 1) | Ahora (radio de `stl()`) |
|---|---|---|
| Máxima diferencia en los 144 meses | 0.0045 (mar. 1953) | **0.0024** (oct. 1949) |
| Diferencia media | 0.0015 | 0.0002 |
| Meses iguales a 4 decimales | 5 de 144 | 71 de 144 |
| En los **73 meses en que `stl()` ajusta** | — | máx. 0.000064; 66 iguales a 4 decimales y 7 a una unidad del cuarto decimal (redondeo de los datos incrustados) |
| En los **71 meses que `stl()` interpola** | — | máx. 0.0024, media 0.0005; 5 iguales a 4 decimales |

**Por qué no del todo:** `stl()` no ajusta en todos los instantes. Con la ventana de 19 su `t.jump` vale 2
(`$jump`: 145, 2, 2): ajusta en las observaciones 1, 3, …, 143 —enero, marzo, mayo, julio, septiembre y noviembre de
cada año— y en la última, la 144, e interpola las demás. Que interpola en línea recta se ve en que, en los meses
pares, su tendencia es la media de los dos ajustes vecinos del simulador (máx. diferencia 0.000058). El estado
inicial del simulador, diciembre de 1954, es un mes interpolado: 5.5428 frente a 5.5432.

**Comprobado con `t.jump = 1`:** la tendencia de `stl(…, t.jump = 1)` y el ajuste local de su propia serie
desestacionalizada difieren como mucho en **2.9e-08** (con la convención anterior, 0.0048). Lo mismo pasa con el
`stl()` por defecto en los 73 meses en que ajusta (2.9e-08, sin redondear). El simulador no puede coincidir del todo
con `stl(t.jump = 1)` porque parte de la desestacionalizada del `stl()` por defecto: frente a esa otra tendencia la
diferencia máxima es 0.0002 (114 de 144 iguales a 4 decimales).

**Dónde quedó en la prosa:** la frase del radio, antes de la tabla (donde estaba la declaración de las dos
convenciones), y la explicación completa en un párrafo nuevo después de las tres lecturas del simulador, que es donde
el estudiante ve las dos cifras distintas. El primer párrafo de «Qué hace una regresión local» ya decía que `stl()`
ajusta cada `t.jump` e interpola; el párrafo nuevo remite a él.

### 4. `data-afirma` cuyo texto cambió

Ninguno. `c1-m6-01`, `c1-m7-01`, `c1-m7-02`, `c1-m7-03` y `c1-m8-01` conservan su texto exacto.
`python3 precalculo/audita_citas.py` termina en `OK auditoría de citas` (sin F09).

### 5. Simuladores y lienzos: para la portada y el README (no se tocaron)

| | Antes | Después |
|---|---|---|
| Contenedores `data-simulador` en el marcado (todos distintos) | 11 | **13** (nuevos: `subseries-estacionales`, `grafico-rezagos`) |
| Apariciones de `data-simulador="…"` en el archivo (una más: el ejemplo `mi-id` de un comentario del JS) | 12 | 14 |
| `<canvas>` en el marcado | 20 | **22** |
| Lienzos contando el del quiz, que se crea en JS | 21 | **23** |
| Apariciones de `<canvas` en el archivo (una más: un comentario del JS) | 21 | 23 |
| M3: simuladores · lienzos | 1 · 1 | 3 · 3 |

`python3 precalculo/cuenta_sitio.py` ya lo acusa: «tarjeta del capítulo 1: dice 11 simuladores y son 13», «README,
capítulo 1: dice 11 y son 13», y los totales del sitio pasan a **72** (la portada dice 68 y el README 70, que ya
estaban mal antes de esta ronda).

### 6. Lo que se miró

- Los dos gráficos nuevos, el mapa, el gráfico estacional y el módulo 3 entero, a 1200, 800 y 375 px; el deslizador
  del rezago en $k = 1$, 6 y 12 (capturas `m3-subseries-*`, `m3-rezagos-k{1,6,12}-*`, `m3-pagina-*`). Sin desbordes:
  `scrollWidth` del documento igual al ancho en los tres; el lienzo de rezagos mide 406, 282 y 236 px de lado.
  Dos defectos vistos y arreglados: a 375 px el título del eje vertical del gráfico de rezagos se cortaba y el del eje
  horizontal del de subseries se comprimía (ahora van en dos líneas).
- El simulador de Loess a los tres anchos y en siete estados (inicial, foco en enero de 1949 y en diciembre de 1960,
  grado 0 en el borde, grado 0 con pesos planos, span 61 y span 7), y la tabla de pesos (capturas
  `m7-loess-local-*`, `m7-tabla-pesos-*`). La curva Loess queda ahora encima de la tendencia de `stl()`; los vecinos
  del borde se ven como un punto.
- **Pasada completa de los nueve módulos a 1200, 800 y 375 px** (`herramientas/r3a_pasada_completa.json` →
  `comprobaciones/r3a_pasada_completa.out`, 27 cargas): ninguna excepción ni `console.error`/`warn` (`eventos []`),
  **0 `.katex-error`**, `scrollWidth` del documento igual al ancho en las 27, ningún simulador ni lienzo fuera de la
  página o de su caja, ningún lienzo sin gráfico y ninguna lectura vacía. Recuento en pantalla: 13 simuladores y 23
  lienzos (con el del quiz).

### 7. Comprobaciones finales (desde la raíz del worktree)

| Comprobación | Resultado |
|---|---|
| `python3 precalculo/genera_referencias.py --comprobar \| head -2` | `OK capitulo-1-…: 3 citas, sin cambios` · `OK capitulo-2-…: 0 citas, sin cambios` |
| `python3 precalculo/audita_citas.py \| tail -3` | `citas literales comprobadas contra la fuente: 9 …` · `[A01] 74 apellidos … sin <cite>` (aviso que ya estaba) · `OK auditoría de citas` |
| `python3 precalculo/audita_posicion_correcta.py \| tail -1` | `Ningún instrumento concentra las correctas.` |
| `python3 precalculo/compila_tailwind.py --comprobar \| tail -1` | `hojas: páginas 12.9 KB · portada 11.0 KB`, salida 0 |
| `Rscript precalculo/verifica_cap1_descomposicion.R \| tail -1` | `>>> TODAS LAS CIFRAS COINCIDEN` |

### 8. Decisiones que tomó esta mitad y que el docente debería conocer

1. **La cifra del gráfico de rezagos es la correlación de la nube, no $r_k$.** Es lo que deja ver que la nube se
   cierra en $k = 12$ (0.991, la más alta), cosa que $r_k$ no dice (0.948 en $k = 1$, 0.760 en $k = 12$). Como el
   capítulo 2 publica $r_{12} = 0.760$, se añadió la nota «De la nube al número», que avisa de que no es el mismo
   número y por qué. Si se prefiere mostrar $r_k$, basta cambiar `correlacion()` en el simulador, pero entonces la
   lectura contradice lo que se ve.
2. **Julio y agosto en turquesa** en el gráfico de rezagos (el libro colorea todas las estaciones; con doce meses
   serían doce colores). Es lo que permite leer por qué la nube se abre en $k = 6$.
3. **El mapa estacional pasa a ser el eje del módulo** (la tabla de la que salen el gráfico estacional y el de
   subseries), en lugar de una figura sin presentar.
4. **Dos notas cambiaron de sitio** sin cambiar de texto: la del abanico (ya no cierra el módulo; el cierre es la
   nota nueva) y la de las varias estacionalidades.
5. **El bloque Python del M3 gana dos gráficos** y la línea de `gg_lag` gana `geom = "point"`. Las cuatro líneas
   están ejecutadas (ver §1).
6. **La explicación de la exactitud frente a `stl()` va después del simulador**, no junto a la tabla (ver §3).

### 9. Lo que quedó sin hacer, y por qué

1. **El capítulo 2 sigue diciendo «el gráfico de rezagos que vimos al final del Capítulo 1»** (su l. 2440). Ahora el
   gráfico existe, pero está en el Módulo 3, no al final. No se tocó: es otro archivo y es la base del capítulo 3
   (hay que reensamblar).
2. **Duración del M3.** Su prosa pasa de unas 470 a unas 1 490 palabras y de uno a tres simuladores; declara 10 min y
   con el criterio del lector estudiante rondará los 15. Las duraciones y la tarjeta de la portada son de T3.5.
3. **Portada y README**: cifras de simuladores sin actualizar, por encargo (§5). La tarjeta del capítulo dice
   «gráficos estacionales y de rezagos»: ahora es cierto, y podría nombrar también el de subseries.
4. **«Ciclo» en la viñeta del gráfico estacional y en la nota de las varias estacionalidades**, y el subtítulo en
   inglés del módulo («Time plots & seasonal plots»): sin tocar (vocabulario, T3.5).
5. **La nota de las varias estacionalidades sigue usando `consumo`**, una serie que el capítulo no tiene (lo señaló
   el lector estudiante): solo se movió.
6. **Los once cocientes de julio del M6** no remiten al gráfico de subseries (lo sugería el lector): el M6 es de la
   segunda mitad.
7. **Deslizadores 0–1 de grado y pesos** del ajuste local (P6 de su ficha): el encargo pide no cambiar los controles.
8. **El estado inicial del simulador de Loess cae en un mes que `stl()` interpola** (5.5428 frente a 5.5432). Se
   explica en la prosa. Que coincidieran exigiría incrustar la tendencia de `stl(t.jump = 1)`, es decir, regenerar
   datos, o cambiar el foco inicial, que es cambiar el simulador.
9. **`gg_season()`, `gg_subseries()` y `gg_lag()` avisan de que están obsoletas** en la versión de `feasts` de este
   equipo (desde la 0.4.2 las funciones gráficas se mudaron al paquete `ggtime`). Corren y dibujan, pero el aviso
   sale; `fpp3` no está instalado aquí, así que no se comprobó qué ve un estudiante con `library(fpp3)`. Para T5.4.
10. **Las lecturas nuevas van justificadas** como las demás del capítulo; a 375 px dejan huecos entre palabras. Es la
    regla común de `.simulador-lectura` y afecta a todas.
11. **`herramientas/r2_elemento.js` tiene una carrera**: llama a `loadModule()` sin esperar a KaTeX y falla de forma
    intermitente con la caché desactivada. Se corrigió solo en la copia `r3_elemento.js`.
12. No se miraron tooltips, teclado, modo oscuro ni impresión.

---

## Segunda mitad · T3.2–T3.5 (M7, M8, M6, hilo, vocabulario y cierre)

Fecha: 2026-11-11. Un solo redactor; sin commit. Especificación: `lector_estudiante.md`.

- Archivos tocados: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (8 003 líneas; antes 7 445),
  `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (una frase), `Htmls_Series/index.html` y
  `Htmls_Series/README.md` (cifras y la tarjeta del capítulo 1). Nuevos: `precalculo/genera_cap1_stl_variantes.R` y
  sus salidas `precalculo/salidas/cap1_stl_variantes.{json,js}`; guiones y salidas `comprobaciones/r3b_*`;
  `herramientas/r3b_*`.
- `DATOS_CAP1` no cambió ni un carácter y `precalculo/genera_datos.R` no se ejecutó. Los datos nuevos van en una
  constante aparte, `DATOS_CAP1_STL` (36.5 KB, l. 4956), copia literal de la salida del guion nuevo.
- Siguen siendo nueve módulos, con su número. Simuladores: 13 → **14** (nuevo `escala-aditiva`, en el M6). Lienzos en
  el marcado: 22 → **26** (27 con el del quiz).
- Los cinco `data-afirma` conservan su texto exacto (comprobado contra la copia de antes); los tres `<cite>` y los
  marcadores `<!--…-->` siguen en su módulo. `audita_citas.py` sale en verde, sin F09.
- Sin clases nuevas de Tailwind. CSS propio nuevo (solo en el capítulo, l. 1935–2040): `.control-opciones*`,
  `ol.pasos-metodo`, `.simulador-lectura code`, y la lectura alineada a la izquierda en el teléfono. No se cambió
  ninguna regla que esté en la plantilla, así que la guía del proyecto no se reensambló.
- Capturas (ignoradas por git): `capturas/r3/m{2,4,5,6,7,8,9}-*-{escritorio,800,movil}.png`, 66 archivos.

### 1. Qué cambió, por módulo

**M1.** Nada.

**M2.** Primera frase reescrita: ya no empieza por «Nada de eso…» sin antecedente, y la frecuencia se define sin usar
«período estacional» ni «estacionalidad», que aún no existen (l. 2790). Dos frases en segunda persona pasan a
impersonal.

**M3.** Solo vocabulario: «una línea por ciclo» → «por cada período estacional»; en la nota de las varias
estacionalidades, «ciclo» → «período» (tres veces); «$k$ periodos» → «períodos».

**M4.** Cuatro subtítulos (`<h3>`): «Suma o producto», «Medirlo en lugar de mirarlo», «El logaritmo convierte el
producto en suma», «Los componentes, uno a uno». Ni una palabra de prosa cambia.

**M5.** *Sale* el párrafo-anticipo («Vale la pena separar qué parte de ese precio…», unas 200 palabras): queda una
frase gancho de tres líneas (l. 3402) y su contenido va al M7. «Será una de las tres limitaciones que acaben
empujando hacia STL» → «la primera de las limitaciones que el Módulo 6 le anote al método clásico» (el trío no
estaba enumerado todavía). «A lo largo del ciclo» → «del período».

**M6.** *Reordenado, sin recortar.* Orden nuevo: introducción → componente de pasos → **resultado** (los cuatro
paneles; antes llegaba tras unas 190 líneas) → «Cómo se lee una descomposición multiplicativa» → código → «El método
en símbolos» (notación, tabla, normalización) → nota de los doce índices → «Qué habría pasado con la otra escala» →
aviso de limitaciones.
- *Añadido:* el simulador estático `escala-aditiva` (l. 3872; JS l. 7004), «La aditiva junto a la multiplicativa, en
  miles de pasajeros»: cuatro paneles —estacionalidad y residuo de cada una— con ejes compartidos dos a dos. La
  multiplicativa va traducida a miles: $\hat T_t(\hat S_t - 1)$ e $y_t - \hat T_t \hat S_t$ (identidad exacta:
  $y = T + T(S-1) + (y - TS)$). En dos columnas si caben (1200 px) y en una si no. Lectura con la desviación típica
  del residuo de 1949, 1954 y 1960 en las dos.
- *Añadido:* una frase, **fuera** de `c1-m6-01`, con la cuarta limitación (l. 3938); una frase que anuncia que el
  capítulo 2 da una herramienta mejor que mirar los paneles, la autocorrelación del residuo (l. 3928, sin cifras);
  una frase que dice por qué la tabla empieza en el paso 2; una remisión («el porqué de ese reescalado está más
  abajo, en el paso 3c») porque la normalización queda ahora después del julio de 1955.
- *Textos visibles del componente de pasos:* «Etapas del ciclo» → «Pasos del bucle»; «no es una fórmula sino un
  ciclo» → «sino un bucle»; «sin ciclos ni abombamientos» → «sin ondas ni abombamientos»; «STL lo hace variar en el
  tiempo» → «STL, con una ventana estacional finita, lo deja variar» (lo dejó anotado R1). Clases e identificadores,
  sin tocar.
- *No se tocó:* el pasaje del julio de 1955 (salvo la remisión) ni el argumento de «la otra escala» (salvo
  «ponerla al lado de la multiplicativa»): las tres filas de cifras siguen donde estaban.

**M7.** Orden nuevo: introducción (con `c1-m7-01`) → **«El método, paso a paso»** → «Qué hace una regresión local» →
«La versión robusta, y por qué no viene puesta» → **«Las tres respuestas, a la vista»** (simulador con interruptores)
→ código → nota de paso al M8.
- *Añadido:* STL como cinco pasos numerados (l. 3985), redactados conforme a la ayuda de `stl()` (§4) y a lo
  comprobado ejecutando; un párrafo que casa cada cambio respecto del método clásico con una debilidad; el anticipo
  del M5 en tres líneas, al abrir la regresión local; tres interruptores en `descomp-stl` (ventana estacional
  `"periodic"` | 11 · julio de 1955 real | inflado · `robust` FALSE | TRUE: ocho variantes, todas calculadas en R),
  con el patrón de partida en línea discontinua en el panel estacional, lectura con `aria-live` y `aria-label` que
  siguen a los interruptores; dos párrafos que leen la figura («La ventana estacional», «El atípico»); en el código,
  las dos llamadas que encienden lo apagado, en R y en Python.
- *Movido al M8:* «Cómo se leen los componentes en escala logarítmica» entero (unas 250 palabras, con sus dos
  fórmulas) y la mención de la estrategia de pronóstico.
- *Movido a desarrollos plegados (no se pierde nada):* la función bicuadrada, la mediana y el seis, la tabla de la
  primera vuelta y el recuento de pesos (desarrollo nuevo «Ver cómo reparte los pesos el bucle exterior»); y el
  atajo de `t.jump` con sus cifras (paso 6 del desarrollo del ajuste local). En el cuerpo queda una frase de cada uno.
- *Quitado:* el párrafo de los cinco argumentos de R (`t.degree` y `s.degree` quedan solo en el desarrollo, donde ya
  se explicaban); la lista «Con la herramienta a la vista…» (la sustituye el párrafo que sigue a los pasos); el aviso
  «Dos de las tres ventajas están apagadas en la figura de arriba», que llegaba después de la figura: ahora lo dice
  la introducción del simulador, antes, y los interruptores las encienden; «subserie de ciclo» → «subserie».
- *No se tocó:* la tabla de pesos tricúbicos, el párrafo de los bordes, el simulador `loess-local` ni sus tres
  lecturas (salvo «las tres decisiones que el Módulo 5 dejó señaladas» → «de la media móvil»).

**M8.** Orden nuevo: transición → **«De logaritmos a miles de pasajeros»** (del M7) → «La serie desestacionalizada»
→ «La fuerza de cada componente» (con `c1-m8-01`, fórmulas y desarrollo) → **tabla de referencia** → **código** → nota.
- *Recibe* del M7 la lectura en escala logarítmica, y del ejercicio 2 el contraste entre series y las dos
  advertencias (no comparar $F_T$ con $F_S$ dentro de una serie; no es porcentaje de varianza). El ejercicio 2
  conserva su solución tal cual: la tabla del M8 usa otras series (`nottem`, `sunspots`, ruido simulado) para no
  resolverlo.
- *Añadido:* bloque de código R/Python que construye la desestacionalizada y calcula $F_T$ y $F_S$; la frase que
  dice por qué se usa STL y cuánto cambia respecto del índice clásico.
- *Cambiado:* el simulador `desestacionalizada` dibuja $y_t / \exp(\hat S_t)$ con la STL de partida (antes, $y_t /
  \hat S_t$ con el índice clásico). «Muy fuertes» → «altas», y con la referencia al lado. Derivación: «compara… le
  quitas» → impersonal.

**M9.** El resumen pasa de seis a siete viñetas: entran el bucle del método («el residuo no se mira para confirmar,
sino para saber a qué paso hay que volver»), «ninguno describe la serie exactamente» y el paso por el logaritmo;
STL queda como «sin huecos; flexible si `s.window` es un número; resistente a los atípicos solo con `robust =
TRUE`». El puente al capítulo 2 baja al final («Lo que sigue: de la estacionalidad a la estacionariedad», l. 4899),
después de los ejercicios y antes de las lecturas, y gana el aviso de que las dos palabras se parecen y un párrafo
que ata el gráfico de rezagos y el «residuo sin forma» con la autocorrelación y el ruido blanco del capítulo 2.
Ejercicio 2: «ciclo anual» → «patrón anual».

**Quiz.** «periodo» → «período» (siete veces); la retroalimentación de la pregunta de STL remite al simulador del M7.
Opciones, orden y correctas, sin tocar.

**Capítulo 2.** «…del gráfico de rezagos que vimos al final del Capítulo 1» → «…que vimos en el Módulo 3 del
Capítulo 1». `python3 ensamblado/ensambla_cap3.py` → «reproducible byte a byte».

**Portada y README.** Cifras que señalaba `cuenta_sitio.py` (9, incluidas las que ya estaban mal): 64 → 65 módulos,
68/70 → 73 simuladores, capítulo 1 de 11 a 14. Tarjeta del capítulo 1 reescrita. `cuenta_sitio.py` → «Las cifras
escritas coinciden con las contadas».

### 2. Los problemas del lector estudiante, uno por fila

R = resuelto · P = en parte · N = no tocado. «R3a» = lo resolvió la primera mitad; «R1» = la ronda R1.

| Mód. | Problema del lector | Estado | Qué quedó, o por qué no |
|---|---|---|---|
| M1 | La dependencia temporal solo se afirma | R (R3a) | Gráfico de rezagos del M3; el resumen del M9 lo recoge ahora |
| M1 | «saber cuándo la separación es de fiar», críptica | P | La frase no cambia; el resumen del M9 la cobra por fin (el bucle) |
| M1 | El simulador adelanta tres conceptos | N | El lector lo da por correcto |
| M1 | Nota «Conexión con ciencia de datos», promesa sin evidencia | N | Fuera de T3.2–T3.5 |
| M2 | «Nada de eso…» sin antecedente | R | Frase nueva |
| M2 | «período estacional» y «estacionalidad» antes de definirse | R | La frecuencia se define con «el patrón que se repite» |
| M2 | Segunda persona en la prosa | R | Dos frases |
| M2 | `ventas` y `tienda` salen de la nada | N | Es rehacer el ejemplo: R5 |
| M2 | «Declararla mal…» no se enseña; no se ve la salida de Python | N | Contenido nuevo: R5 |
| M3 | Cuatro gráficos anunciados y uno leído; subseries; rezagos; mapa sin presentar | R (R3a) | — |
| M3 | «ciclo» por período | R | — |
| M3 | La nota de varias estacionalidades usa `consumo`, que no existe | N | Solo se movió (R3a) y se le cambió el vocabulario |
| M4 | 1 338 palabras y ningún subtítulo | R | Cuatro `<h3>` |
| M4 | «construye tu serie» al final, símbolos sin mapear | P | Tiene subtítulo; no se movió ni se reescribió (la lectura y el eje son de R2/R5) |
| M4 | $T_t$ con dos significados; «ruido»/«residuo»; $a = A/T_0$; cifras repetidas; $C_t$ nunca se ve | N | Fuera de T3.2–T3.5; el pasaje vecino es de los que no hay que romper |
| M5 | «una de las tres limitaciones», trío sin enumerar | R | — |
| M5 | Párrafo que obliga a releer; dos tríos en doce líneas | R | Al M7, en tres líneas |
| M5 | $k$ cambia de significado (M5 y M6) | N | Notación: tocarla exige revisar la tabla del M6 |
| M5 | La intro del simulador no pide comparar 11, 12 y 13 | N | No se comprobó qué muestra el simulador con 11 y 13 |
| M6 | El resultado llega tras 190 líneas | R | Va tras el componente de pasos |
| M6 | El componente se llama «ciclo» | R | «bucle» |
| M6 | Muro de notación; $\tilde s$ antes de definirse | P | Ahora va después del resultado y remite a la fila 3b; la densidad es la misma |
| M6 | La tabla empieza en el paso 2 sin decir por qué | R | — |
| M6 | Tres filas de números hacen de figuras; la U no se ve | P | La U y la banda fija se ven en la figura nueva; los once cocientes de julio siguen siendo una fila |
| M6 | La descomposición aditiva nunca se dibuja | R | `escala-aditiva` |
| M6 | «Es sensible a atípicos» solo se afirma | R (en el M7) | El interruptor del atípico |
| M6 | El módulo cierra con un recuadro | P | Antes del recuadro va el anuncio del capítulo 2; el recuadro sigue cerrando, porque es lo que abre el M7 |
| M7 | ~12 términos nuevos | P | Del cuerpo salen `t.degree`, `s.degree`, bicuadrada, `t.jump`, «subserie de ciclo» y «bucle interior»; quedan Loess, span, `t.window`, `s.window`, tricúbica, subserie, bucle exterior, `robust`, `"periodic"` |
| M7 | Cinco argumentos de R en un párrafo | R | Uno por paso |
| M7 | Nunca se enuncia STL como secuencia de pasos | R | — |
| M7 | La flexibilidad es una cifra; la robustez, una tabla de pesos | R | Interruptores |
| M7 | La figura va con `"periodic"` y sin `robust`, y el aviso llega después | R | El aviso va antes, en la introducción |
| M7 | La lectura en logaritmos compite con la figura | R | Al M8 |
| M7 | El cierre mira al pronóstico y no al M8 | R | — |
| M8 | El simulador usa el índice clásico | R | STL |
| M8 | «0.994 y 0.937, muy fuertes» sin referencia | R | Tabla de cuatro series |
| M8 | Sin código | R | — |
| M8 | «Estadísticas oficiales» sin ilustrar | N | Pide una serie oficial: R4/R5 |
| M8 | Nota «una serie entera en dos números», promesa | P | La tabla enseña cuatro series; no hay colección |
| M8 | Segunda persona en la derivación | R | — |
| M9 | El resumen omite el bucle, la lección del M4 y el logaritmo | R | — |
| M9 | El puente al capítulo 2, antes del quiz | R | Al final |
| M9 | «ciclo anual» | R | — |
| M9 | Solo hay preguntas de M4 a M8; el ejercicio 1 usa una técnica nueva | N | R5 |
| M9 | Cuatro índices de julio parecidos | N | El M7 habla ahora en porcentajes (+24.2 %, +28.1 %…); el ejercicio 3, en índices (1.2416, 1.2806): son las mismas cifras, pero el lector tiene que traducir |
| — | «Ciclo» significa tres cosas | R | Solo el componente cíclico (§5) |
| — | Dos tríos distintos | P | El M5 ya no enumera ninguno; el M7 presenta las tres respuestas y, aparte, las tres decisiones |
| — | Voz: el capítulo 2 habla en primera persona del plural | N | Otro capítulo |
| — | Capítulo 2: «que vimos al final del Capítulo 1» | R | — |
| — | «Estacionalidad» / «estacionariedad» sin aviso; el residuo y el ruido blanco | R | Puente del M9 |
| — | Tarjeta de la portada | R | — |

### 3. Cifras nuevas y su evidencia

Todas salen de R. Guiones: `precalculo/genera_cap1_stl_variantes.R` (→ `comprobaciones/r3b_genera_variantes.out`) y
`comprobaciones/r3b_cifras.R` (→ `r3b_cifras.out`). `comprobaciones/r3b_compara.py` (→ `r3b_compara.out`) comprueba
que cada cifra está en el capítulo y en la salida de R que la respalda: **77 comprobaciones, 0 fallos**.

| Cifra | Dónde | Evidencia |
|---|---|---|
| Julio estacional, `"periodic"`: +24.2 % los doce años | M7, prosa y lectura | `r3b_cifras.out`, «la ventana estacional» |
| Julio, `s.window = 11`: +20.4 % (1949), +25.0 % (1955), +27.9 % (1960) | M7 | ídem |
| Residuo de julio, `"periodic"`: negativo 1949–1953, positivo 1954–1960 | M7 | ídem |
| Desviación típica media del residuo por tramos, `"periodic"`: 0.040 · 0.019 · 0.036 | M7, prosa y lectura | ídem (0.0396, 0.0188, 0.0360) |
| Ídem con `s.window = 11`: 0.029 · 0.016 · 0.024 | M7 | ídem (0.0289, 0.0160, 0.0239) |
| «Tampoco con ventanas más estrechas» | M7 | ídem: con 7, 0.0240 · 0.0138 · 0.0195 (razón extremos/centro 1.61; con 11, 1.69; `"periodic"`, 2.04) |
| log(1.5) = 0.4055 | M7 | «el atípico» |
| Sin `robust`: julio +28.1 %, tendencia de jul-1955 294.3 mil (283.2 sin atípico), residuo 0.3708 | M7 | ídem |
| Con `robust`: +24.6 %, 282.2 mil, residuo 0.4404, peso 0 para el julio inflado, 5 observaciones con peso 0 | M7 | ídem |
| Lecturas de las otras variantes (p. ej. `s.window = 11` con atípico y sin `robust`: +23.9 / +33.3 / +33.1 %) | M7, lectura | `r3b_genera_variantes.out`, tabla de las ocho variantes |
| 12 observaciones sin estimar frente a ninguna; dos pasadas; 15 vueltas con una pasada | M7 | `r3b_cifras.out`, «los pasos de stl()» |
| Julio 1.204 y 1.279; 4 observaciones sin peso | M7, código R y Python | `r3b_bloques_publicados.out` |
| Estacionalidad aditiva entre −54 y +64 mil; desviación típica anual del residuo en miles, aditiva 30.5 … 25.4 y multiplicativa 4.2 … 22.3; la aditiva, mayor los doce años | M6, figura | `r3b_cifras.out`, «la aditiva junto a la multiplicativa» |
| $364 / 1.2416 = 293.2$; con el índice clásico, 296.8; diferencia máxima 6.1 mil (1.2 %) en julio de 1960 | M8 | «M8» |
| $F_T$, $F_S$: `nottem` 0.205 y 0.944; `sunspots` 0.907 y 0.005; ruido puro, medianas 0.12 y 0.08 (200 series de 144 normales, semilla 20948; mínimos 0.025 y 0.015) | M8, tabla | ídem |
| 0.994 y 0.937; 0.997 y 0.964 | M8 (ya estaban) | ídem y `r3b_bloques_publicados.out` |

Otras comprobaciones (`r3b_compara.out`): `DATOS_CAP1_STL` es carácter a carácter la salida del guion; su variante
de partida es `DATOS_CAP1.stl_log` (432 valores); la desestacionalizada incrustada coincide punto a punto con
`AirPassengers / exp(S)` recalculada (144 de 144); la aditiva y la multiplicativa en miles, con `decompose()`
recalculada (576 valores). Los cuatro bloques de código cambiados o nuevos se ejecutaron tal como están publicados
(`r3b_bloques_publicados.py` → `.out`: 0 errores; R 4.6.0 con `feasts`, sin `fpp3`; statsmodels 0.14.6).

**Por qué el residuo de la STL periódica es más disperso en los extremos** (lo dejó pendiente R2). Comprobado:
(1) el residuo de julio es negativo los cinco primeros años y positivo los siete últimos; (2) el patrón mensual medio
del residuo de 1949–1953 y el de 1958–1960 son casi espejo (correlación −0.93); (3) al dejar variar la estacionalidad,
la dispersión baja un 27 % y un 34 % en los extremos y un 15 % en el centro. Pero la forma **no desaparece**: la
razón extremos/centro pasa de 2.04 a 1.69, y a 1.61 con la ventana de 7. Por eso el capítulo dice «es una de las
razones» y «explica una parte de esa forma, no toda», y no más.

### 4. Frases leídas que respaldan cada afirmación nueva (para R4)

No se añadió ningún `<cite>`. «FPP3» = `bibliografia/_local/web/hyndman2021forecasting/`; «ayuda» =
`comprobaciones/r3b_ayuda_stl.txt` (la página `?stl` de R 4.6.0, guardada en esta sesión).

| Afirmación | Fuente · línea | Frase leída |
|---|---|---|
| M6 · cuarta limitación: la media móvil suaviza de más subidas y caídas rápidas | FPP3 `decomposition.txt`, §3.4 «Comments on classical decomposition», l. 398 | «The trend-cycle estimate tends to over-smooth rapid rises and falls in the data.» |
| M6 · STL la atenúa: deja elegir la suavidad de la tendencia | FPP3 `decomposition.txt`, §3.6, l. 470 (y l. 494) | «The smoothness of the trend-cycle can also be controlled by the user.» · «…the default trend window setting produces a trend-cycle component that is too rigid. […] Selecting a shorter trend window […] improves this.» |
| M7 · paso 1: se suaviza cada subserie; con `"periodic"`, la media | ayuda, Details, l. 69–71 | «The seasonal component is found by loess smoothing the seasonal sub-series (the series of all January values, ...); if s.window = "periodic" smoothing is effectively replaced by taking the mean.» |
| M7 · `s.window`, impar y en años; 7 como mínimo recomendado | ayuda, l. 26–28 · FPP3 §3.6, l. 492 | «…the span (in lags) of the loess window for seasonal extraction, which should be odd and at least 7…» · «season window is the number of consecutive years to be used in estimating each value in the seasonal component» |
| M7 · paso 2: se quitan los valores estacionales y se suaviza lo que queda | ayuda, l. 72–73 | «The seasonal values are removed, and the remainder smoothed to find the trend.» |
| M7 · paso 3: el nivel pasa a la tendencia | ayuda, l. 73–74 | «The overall level is removed from the seasonal component and added to the trend component.» |
| M7 · paso 4: se repite unas pocas veces (dos) | ayuda, l. 74–75 y 60–61 | «This process is iterated a few times.» · «inner: […] usually very few (2) iterations suffice.» |
| M7 · paso 5: el residuo | ayuda, l. 75 | «The remainder component is the residuals from the seasonal plus trend fit.» |
| M7 · `stl()` interpola en línea recta entre ajustes | ayuda, l. 53–55 | «Linear interpolation happens between every *.jump-th value.» |
| M7 · la estacionalidad puede cambiar; la robustez es una opción | FPP3 §3.6, l. 469 y 471 | «The seasonal component is allowed to change over time, and the rate of change can be controlled by the user.» · «It can be robust to outliers (i.e., the user can specify a robust decomposition)…» |
| M8 · la serie ajustada conserva el residuo; uso oficial | FPP3 §3.2, l. 179 y 181 | (ya respaldaban el texto anterior) |
| M8 · las fuerzas sirven para encontrar series en una colección | FPP3 `features.txt`, §4.3, l. 101 | «These measures can be useful, for example, when you have a large collection of time series, and you need to find the series with the most trend or the most seasonality.» |
| M8 · qué son `nottem` y `sunspots` | `?nottem`, `?sunspots` (títulos, en `r3b_cifras.out`) | «Average Monthly Temperatures at Nottingham, 1920–1939» · «Monthly Sunspot Numbers, 1749–1983» |

**Sin fuente, propias** (así habría que declararlas en R4): que en la segunda pasada el paso 1 parte de la serie sin
la tendencia (la ayuda no lo dice; comprobado con `inner = 1` y `2`, diferencia 1.9e-08, solo para `"periodic"`);
que el reparto del nivel deja la estacionalidad alrededor de cero (comprobado); toda la lectura de las variantes
sobre `AirPassengers`; la traducción de la multiplicativa a miles; la tabla de referencia de las fuerzas y la
lectura «ni el ruido puro da cero»; la frase del M6 sobre el diagnóstico por la autocorrelación (es un anuncio del
capítulo 2). El desarrollo «*locally estimated scatterplot smoothing*» sigue sin contrastar (R1, hallazgo 26).

### 5. Vocabulario

«Ciclo» queda solo para el componente cíclico (M4, resumen del M9, pregunta 1 del quiz). Para el período estacional,
**«período»** (M3, M5, M6, M7; y con tilde también en el quiz). Para el bucle del método, **«bucle»** (M4, M6, M9) y
«recorrido» para la secuencia de pasos, como ya estaban. En STL, «pasadas» para las del paso 4 y «bucle exterior»
para el de la robustez. Búsqueda final de «ciclo» en el texto visible: solo el componente cíclico y
«tendencia-ciclo». Las clases CSS `.ciclo*`, `data-ciclo` e `iniciarCiclos()` no se tocaron.

### 6. Carga por módulo y duraciones

`cuenta_cap1_v2.py` tal como está (`comprobaciones/r3b_carga.out`). «Antes» es el capítulo al empezar esta mitad.

| Mód. | Prosa antes → después | Plegado antes → después | Simuladores | Min (fórmula) antes → después | Declarado antes → ahora |
|---|---|---|---|---|---|
| M1 | 365 → 365 | — | 1 | 5.0 → 5.0 | 8 → **5** |
| M2 | 521 → 552 | — | 0 | 6.9 → 7.1 | 8 → **7** |
| M3 | 1 590 → 1 593 | — | 3 | 19.8 → 19.9 | 10 → **20** |
| M4 | 1 464 → 1 484 | — | 4 | 20.1 → 20.2 | 12 → **20** |
| M5 | 1 034 → 882 | — | 1 | 10.7 → 9.9 | 10 → **10** |
| M6 | 2 288 → 2 526 | 336 → 336 | 1 → 2 | 17.7 → **22.0** | 12 → **22** |
| M7 | 2 222 → 2 173 | 458 → 907 | 2 | 20.3 → 20.1 | 10 → **20** |
| M8 | 349 → 947 | 173 → 175 | 1 | 4.9 → 10.3 | 10 → **10** |
| M9 | 1 312 → 1 469 | — | 0 | 13.3 → 14.2 (+ ≈ 7 del quiz) | 8 → **20** |
| Total | | | 13 → 14 | 118.9 → 128.6 | 88 → **134** |

- **Pasan de 20 min:** el M6 (22.0) y, por décimas, el M4 (20.2) y el M7 (20.1). El M6 sube 4.3 min: 3 son la regla
  de «3 min por simulador» aplicada a la figura nueva, que es estática.
- **El M7 queda más corto, pero poco.** En el cuerpo, 49 palabras menos con el guion del lector y 129 menos de prosa
  si no se cuenta el código (2 007 → 1 878), que crece unas 80 palabras por las cuatro llamadas nuevas. Lo plegado se
  dobla (458 → 907): es lo que salió del cuerpo. Con los desarrollos abiertos el módulo tarda 25 min.
- **Un defecto del guion del lector**, que no se corrigió: no quita los `<pre>`, y el `$` de un `x$y` del código se
  empareja con el de una fórmula y se come la prosa de en medio. `comprobaciones/r3b_cuenta_sin_codigo.py` es la
  variante que sí los quita; con ella los minutos son 5.0 · 6.3 · 19.2 · 20.2 · 9.1 · 21.6 · 18.4 · 10.2 · 15.2, y
  las duraciones declaradas distan menos de 3 min de las dos cuentas.
- **M9:** se declaran 20 min porque el lector estima el módulo con su autoevaluación (≈ 7 min), que el guion no
  cuenta. Sin el quiz serían 14.

### 7. `data-afirma` cuyo texto cambió

Ninguno. Lo añadido alrededor está fuera de los elementos: la frase de la cuarta limitación va después del `</span>`
de `c1-m6-01`; en el M7 cambian las frases que rodean a `c1-m7-01` y `c1-m7-02`; `c1-m8-01` queda bajo un `<h3>` nuevo.

### 8. Lo que se miró

- Los simuladores nuevos y cambiados a 1200, 800 y 375 px, con los interruptores en seis combinaciones (partida;
  ventana de 11; atípico sin y con `robust`; ventana de 11 con atípico; ventana de 11 con `robust`), los dos
  desarrollos del M7 abiertos, y las páginas enteras de los módulos 2, 4, 5, 6, 7, 8 y 9. `scrollWidth` igual al
  ancho en todas las cargas; ningún simulador, interruptor ni lista fuera de la página.
- Pasada completa (`herramientas/r3b_pasada_completa.json` → `comprobaciones/r3b_pasada_completa.out`): 27 cargas,
  ninguna excepción ni `console.error`/`warn`, 0 `.katex-error`, ningún lienzo sin gráfico ni fuera de su caja,
  ninguna lectura vacía; 14 simuladores y 27 lienzos.
- Defectos vistos y arreglados: el cero del eje del residuo salía como «−0.0» (error de coma flotante; arreglado en
  el formateador común de los ejes); el margen de la lista de pasos; los espacios estirados dentro de un `<code>` de
  la lectura; la lectura justificada con huecos en el teléfono (ahora a la izquierda: afecta a **todas** las
  lecturas del capítulo, también a las de R2 y R3a); la etiqueta «546, inflado un 50 %», que partía en dos líneas.
- En `r3b_capturas.out` la tanda de 1200 px se cortó por un tiempo de espera del CDN; se repitió entera y terminó
  sin incidencias. En el teléfono las páginas enteras se capturan hasta 7 500 px de alto.
- No se miraron tooltips, teclado, modo oscuro ni impresión.

### 9. Comprobaciones finales (`comprobaciones/r3b_verifica_todo.out`)

`python3 precalculo/verifica_todo.py` → **11 verificadores en verde** (incluidos «ninguna cita de memoria», sin F09,
«cifras del sitio contadas», «capítulo 3 reproducible» y «Tailwind compilado al día»).
`Rscript precalculo/verifica_cap1_descomposicion.R | tail -1` → `>>> TODAS LAS CIFRAS COINCIDEN`.

### 10. Decisiones de esta mitad que el docente debería conocer

1. **Tres interruptores y no dos**, con las ocho combinaciones. El atípico es un interruptor aparte: así la figura
   de partida es la de siempre y `robust` se puede probar también sobre la serie limpia, donde deja 4 observaciones
   sin peso y mueve el julio de +24.2 % a +25.6 %.
2. **`s.window = 11` es la llamada tal cual**, `stl(log(AirPassengers), s.window = 11)`: R calcula entonces una
   ventana de tendencia de 21 y no de 19. Cambian dos cosas a la vez, pero es lo que obtiene un estudiante (con la
   de 19, julio de 1949 da +20.6 % en vez de +20.4 %).
3. **El patrón de partida solo se dibuja en el panel estacional.** En el de tendencia la diferencia es de 2 px y en
   el de residuo dos líneas quebradas no se leen; ahí lo dicen la lectura y la prosa.
4. **El eje del residuo cambia al inflar el dato** (de ±0.15 a −0.2…0.5) y solo entonces; los demás ejes son fijos.
5. **La robustez sale del cuerpo del M7**: fórmula bicuadrada, tabla de pesos y recuento van a un desarrollo
   plegado. En el cuerpo quedan el mecanismo, «15 vueltas frente a cero» y el efecto en la figura.
6. **El simulador del M8 pasa a STL**, porque el módulo sigue al de STL y las fuerzas salen de esa misma
   descomposición. La serie viene calculada de R, no se divide en el navegador.
7. **La tabla de referencia del M8 no usa `co2` ni `USAccDeaths`**, para no resolver el ejercicio 2. El ruido puro es
   una simulación con semilla; si se prefiere no publicar una cifra simulada, se quita esa fila.
8. **La aditiva se dibuja al lado de la multiplicativa traducida a miles**, no como una segunda pila de cuatro
   paneles: en unidades distintas no se comparan. En miles, el residuo de la multiplicativa crece al final de la
   serie (22.3 en 1960), y la lectura lo dice.
9. **El M4 gana cuatro subtítulos** aunque no estaba en T3.2–T3.5: lo pedía el lector y no cambia una palabra.
10. **Las duraciones suman 134 min** (antes 88). El M6 declara 22.
11. **El guion de carga del lector tiene el defecto de §6**; no se tocó para que las cifras sean comparables.

### 11. Lo que quedó sin hacer

1. Los problemas marcados N o P en §2. Los de más peso: el muro de notación del M6, `ventas`/`consumo` (series que
   no existen), los once cocientes de julio sin gráfico y los términos que aún carga el M7.
2. `precalculo/README.md` no menciona el guion nuevo.
3. Las reglas CSS nuevas están solo en el capítulo 1 (como las de R2): se llevan a la plantilla cuando toque.
4. La descripción del capítulo 1 en el README («gráficos estacionales…») no se cambió: el encargo era solo cifras.
5. El bloque de R del M8 termina con `library(fpp3)`, que no está instalado aquí: se ejecutó con los paquetes que
   `fpp3` adjunta (T5.4).

## Correcciones tras la verificación (2026-11-11 … 13)

Tres verificadores independientes revisaron la ronda: corrección (Opus 5.5), gráficos a tres anchos
(Opus 5.5) y una relectura completa como estudiante (Sonnet 5.5). De sus informes salió una lista
cerrada de 16 puntos. El corrector que los aplicó se quedó sin red a mitad y la sesión que dirige
terminó y **comprobó uno por uno** el estado final; las medidas de abajo son suyas.

| # | Qué pasaba | Estado |
|---|---|---|
| A1 | La nota «De la nube al número» (M3) daba una causa errónea: decía que el coeficiente de autocorrelación difiere porque resta la media de la serie entera. Medido: con la media global y el denominador de la nube sale 0.950; casi toda la caída la pone el denominador | corregido |
| A2 | El M6 prometía que el capítulo 2 da «una herramienta mejor» para detectar una escala mal elegida; el cálculo no lo respalda en esta serie (ACF del residuo en el rezago 12: 0.674 aditiva, 0.294 multiplicativa, banda ±0.171) | corregido: anuncio neutro |
| A3 | «Los tres salen de reordenar la tabla» era falso para el gráfico de rezagos y contradecía al párrafo siguiente | corregido |
| A4 | La apertura del M8 decía que las dos tareas piden devolver los componentes a las unidades de la serie; el módulo calcula las fuerzas en logaritmos | corregido |
| A5 | «Así lo describe la ayuda de `stl()`» atribuía dos detalles que no están en ella | corregido: «Así lo describe, en lo esencial» |
| A6 | «Admite una vuelta más» contra las 15 vueltas que el módulo da después | corregido |
| A7 | `aria-label`: el residuo «algo mayor al final» cuando la desviación típica anual pasa de 4.2 a 22.3 | corregido |
| A8 | El M9 declaraba 20 min y el criterio da 15 | corregido |
| A9 | «Frecuencia» (M2) y «período $m$» nunca se igualaban | corregido: aposición donde $m$ aparece |
| B1 | La tabla de fuerzas del M8 se cortaba a 800 px sin poder desplazarse | corregido: a 800 px la tabla mide 375 px en una caja de 348 y se desplaza dentro de ella; ninguna celda truncada; la página no desborda |
| B2 | Doble redondeo: la lectura mostraba 0.028 donde R da 0.027479 | corregido de raíz: el generador escribe un bloque `lectura` con los decimales de pantalla, redondeados una sola vez desde el valor completo, y el simulador solo lee de ahí. Las ocho variantes comprobadas |
| B3 | El área de dibujo de `grafico-rezagos` no era cuadrada (hasta un 6.4 % de diferencia) | **en parte**: baja a 191×194 px a 800 px (1.5 %). La diagonal queda a 45° a simple vista, pero no es exacta |
| B4 | Los puntos de julio y agosto solo se distinguían por el matiz (contraste 1.23:1) | corregido: círculos y triángulos |
| B5 | La línea del «patrón de partida» de `descomp-stl` casi no se veía y no tenía leyenda | corregido: 1.6 px, color oscuro y entrada de leyenda que aparece cuando la línea se dibuja |
| B6 | Lecturas y lista de pasos justificadas con huecos en pantallas estrechas | corregido: alineadas a la izquierda a 800 y 375 px |
| B7 | Dos fórmulas del desarrollo de $F_T$ se cortaban sin pista de desplazamiento | corregido: ninguna fórmula desborda ya sin su caja desplazable |

**Registro de contraste.** La frase que la ronda añadió sobre la cuarta limitación atribuía a FPP3
sin estar marcada: ahora es la afirmación `c1-m6-02`, con dos citas literales de §3.4 y §3.6
comprobadas contra la instantánea. El registro del capítulo pasa de 5 a 6 afirmaciones.

**Comprobación final (2026-11-13):** `verifica_todo.py` en verde, los 11 verificadores, incluido
`cuenta_sitio.py`, que llevaba en rojo desde antes de esta línea de trabajo. `audita_citas.py`:
11 citas literales comprobadas contra la fuente. Nueve módulos cargados a 1200, 800 y 375 px sin
errores de consola, sin fórmulas rotas y sin desbordes de página.
