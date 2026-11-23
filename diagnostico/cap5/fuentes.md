# Capítulo 5 · Afirmaciones que exigen fuente (diagnóstico, 2026-11-23)

Archivo leído: `Htmls_Series/capitulo-5-sarima.html` (worktree en `f807b40`): los doce módulos (`<template id="module-N">`), el pie, los
metadatos de la cabecera, el JS con los datos (`DATOS_CAP5`, `SERIES_CAP5`) y sus comentarios que atribuyen algo, `TABLAS_RANKING['comparativa']`,
`AUTOEVALUACIONES['cap5']` (8 preguntas), `SIMULACROS['cap5-simulacro']` (una versión, 12 preguntas), las lecturas y los tres ejercicios.
Inventario completo, una fila por afirmación: `bibliografia/contraste/cap5_inventario.tsv` (281 filas, mismas columnas que los del capítulo 4;
`hallado` y `r4` vacíos por encargo). No se inventariaron las cifras que calcula R ni las derivaciones que el capítulo muestra paso a paso
(propias); sí las frases que las enmarcan, y en las pocas cifras que no tienen generador se anota `[SIN GENERADOR]`.
El capítulo no tiene ningún `data-afirma` ni `cite.cita` (0 ocurrencias) ni los marcadores `PIE-REFERENCIAS`: el pie está tecleado a mano
(la sección 0 de `ensamblado/ensambla_cap5.py` impide que herede las citas del capítulo 4, que sí las tiene).
**Los capítulos 3 a 6 se ensamblan:** la fuente es `ensamblado/cap5/` (`templates_*.html`, `chapter.js`, `simulacro.js`); las líneas del TSV son las del
HTML final. Lo repetido (resumen, autoevaluación, simulacro, ejercicios) va en filas con `REPITE c5-…`; lo ya registrado en los capítulos 1 a 4,
con `= c1-…` / `= c2-…` / `= c3-…` / `= c4-…`.

## Recuentos

| tipo | alta | media | baja | total |
|---|---:|---:|---:|---:|
| definicion | 8 | 1 | 0 | 9 |
| resultado | 34 | 44 | 6 | 84 |
| regla | 59 | 45 | 4 | 108 |
| dato | 4 | 26 | 24 | 54 |
| atribucion | 14 | 5 | 7 | 26 |
| historica | 0 | 0 | 0 | 0 |
| **total** | **119** | **121** | **41** | **281** |

Por módulo: pie, metadatos y comentarios del JS 13 (pie 4, JSON de datos 6, JS 3) · M1 16 · M2 25 · M3 24 · M4 26 · M5 11 · M6 12 · M7 18 · M8 14 ·
M9 15 · M10 16 · M11 75 (panorama y comparación 30, resumen 9, ejercicios 12, libro de Excel 1, lecturas 5, autoevaluación y tabla ordenable 18) ·
M12 16 (prosa 2, simulacro 14).

Estado de la búsqueda (clasificación del inventariante a partir de lo que dice `donde_buscar`, por `python3 diagnostico/cap5/diag/fuentes_cuenta.py`;
precedencia de arriba abajo en el guion: discrepa, matiz o tensión, no comprobable, no hallada, sin generador, parcial, respaldada, propia):

| estado | alta | media | baja | total |
|---|---:|---:|---:|---:|
| respaldada en lo leído | 31 | 42 | 12 | 85 |
| parcial | 15 | 21 | 1 | 37 |
| con matiz o tensión | 34 | 15 | 4 | 53 |
| discrepa o error | 2 | 0 | 0 | 2 |
| no hallada en lo leído | 22 | 11 | 2 | 35 |
| no comprobable aquí (obra sin texto en disco o sin documentación) | 10 | 9 | 7 | 26 |
| sin generador (norma 1) | 3 | 2 | 0 | 5 |
| propia o sin fuente necesaria | 2 | 21 | 15 | 38 |

«Respaldada» = un pasaje leído respalda la afirmación; según la norma lo verifica alguien que no la redactó. Las rutas son `ruta:línea` bajo
`bibliografia/_local/` (`texto/<clave>/pNNNN.txt` es el archivo de página y «impr.» la página impresa; `web/…` es FPP3 o una ayuda de R).
Etiquetas de `donde_buscar`: `[DISCREPA]` 2 filas, `[CON-MATIZ]` 40, `[TENSIÓN]` 16 (9 de ellas con la ronda R4 del capítulo 4), `[NO HALLADO]` 43,
`[PARCIAL]` 46, `[NO COMPROBABLE]` 30, `[SIN GENERADOR]` 9 (seis propias y tres heredadas por repetición), `[EJEMPLAR]` 2; 70 filas llevan `[= cN-…]`
(c1 8, c2 15, c3 20, c4 39; una fila puede citar varias) y 76 repiten otra fila de este inventario (las que solo repiten heredan sus etiquetas).
Las dos etiquetas de matiz con más peso son las que miran a la R4 del capítulo 4: el capítulo 5 sigue diciendo a la antigua lo que el 4 corrigió.

Qué había en la caché y qué se leyó (todo en esta sesión; de FPP3 y de las ayudas, los pasajes que cita el TSV): FPP3 §9.1, §9.9, §9.10 y §9.12 (`arima.txt` y su ejemplo de H02), §2.3-2.4 y §2.9, §3.1 y §3.6,
§4.3, §5.4-5.8 y §5.10, §7.4-7.5, §8.3-8.4, §10.1-10.5, §12.1, §12.2 y §12.4, §1.1; **Cryer y Chan, capítulo 10 entero** (pp. 227-248 impresas, `p0237`-`p0258`);
**Shumway y Stoffer 3.ª ed., §3.9** (pp. 154-162, `p0167`-`p0175`) y la lista de problemas con la serie `birth`; Hyndman y Khandakar (2008), pp. 10 y 12 y un pasaje de la p. 8; las ayudas de R
`AirPassengers`, `USAccDeaths`, `co2`, `arima`, `acf`, `diff`, `ARMAacf`, `ndiffs` y la de `Arima`; y, ejecutándolas (no están en `_local/web/`), las de `nsdiffs`, `fourier`, `stlm`,
`BoxCox.lambda`, `auto.arima`. Las rutas de las filas son de esta caché. Quedaron fuera de lectura Hamilton (no trata SARIMA), Cryer fuera del cap. 10 y los capítulos 11-12 de Cryer,
y las secciones de FPP3 que el capítulo no usa.

## Lo que más pesa (ordenado por daño al estudiante)

1. **La varianza mínima como regla para elegir `d` y `D`** — `c5-m3-11`, `c5-m3-17`, `c5-m4-19`, `c5-m4-20`, `c5-m7-03`, `c5-m11-41` y, en el simulacro, las
   retros de la pregunta 1 (l. 10000-10004). [TENSIÓN con la R4 del cap. 4]. El M3 dice que «la regla de la varianza mínima» señala `(1,1)` y «acierta», y que «falla en casos
   reales» (el 58 % de `log(lynx)`); el ciclo del M4 la lista como evidencia de `d`; el M7 la pone de «comprobación»; la pista del Ejercicio 1 pide calcular las cuatro varianzas
   «antes de mirar ninguna prueba». El capítulo 4, tras su R4, enseña lo contrario: la columna de la varianza describe y no decide (en una serie estacionaria
   `Var(∇y)/Var(y) → 2(1−r₁)`: `c2-m7-08`, `c4-m3-60`, `c4-m8-60`). Ninguna fuente leída (Cryer cap. 10, Shumway §3.9, FPP3 §9.1, H&K) propone el mínimo de la varianza como criterio;
   H&K (p. 10) eligen `d` y `D` con pruebas de raíz unitaria y advierten de que sobrediferenciar daña el pronóstico. Es lo que el estudiante aplicaría en el quiz.
2. **La firma de la sobrediferenciación estacional** («`Θ̂` se pega a −1 y la raíz del MA cae sobre el círculo unitario») — `c5-m3-15`, `c5-m4-17`, `c5-m5-10`, el Resumen (`c5-m11-34`),
   la autoevaluación 4 (`c5-m11-66`), el simulacro (`c5-m12-05`). [CON-MATIZ]. Cryer (pp. 126-127) la da para la diferencia regular, y el cap. 4 ya la marcó con matiz
   por su dirección (`c4-m1-25`: sobrediferenciar crea la raíz, no se sigue que una raíz cerca de 1 delate la sobrediferenciación); ninguna fuente leída trata el caso estacional.
   Es extensión por analogía, presentada como «la señal fiable».
3. **«Primero `D`, después `d`»: el orden está respaldado, el mecanismo y la historia de la función no** — `c5-m3-13`, `c5-m3-14`, `c5-m3-21`, `c5-m3-22`, `c5-m8-02`, `c5-m11-33`, `c5-m11-46/-47`,
   `c5-m11-65`, `c5-m12-04`. El orden lo respaldan FPP3 §9.1 (`arima.txt:119`: los operadores conmutan y conviene la estacional primero) y H&K (p. 10: `d` se elige tras `D`). Pero el
   «porque la estacionalidad domina la varianza y esconde la tendencia» (M3, M8, autoevaluación 4, Ejercicio 2) [NO HALLADO]: la razón de FPP3 es otra (la serie diferenciada estacionalmente a veces ya es
   estacionaria). Y la «trampa de versión» (M3, Ejercicio 2): `nsdiffs()` usa `"seas"` por defecto «desde forecast 8.x» y «las versiones anteriores usaban OCSB»: la ayuda actual (ejecutada) confirma
   `"seas"` por defecto, el umbral 0.64 y que `"ocsb"` se puede pedir, pero no menciona versión alguna; y el artículo de H&K (2008) eligía `D` con la prueba de Canova–Hansen (p. 10), no con OCSB
   [DISCREPA parcial]. Es dato de versión sin fuente que el Ejercicio 2 convierte en criterio («con ocsb —la antigua— te habrías equivocado más»).
4. **El modelo airline y sus atribuciones** — `c5-m5-02` («Box y Jenkins lo llamaron así porque lo ajustaron precisamente a `log(AirPassengers)`»), `c5-m5-03` («el SARIMA más usado del mundo»), `c5-m5-04` («casi cualquier
   serie mensual»), `c5-m5-06` y el Resumen `c5-m11-35` («punto de partida por defecto»), `c5-m11-10` («un modelo de 1970»), `c5-m11-57` («Cap. 9» de Box et al., «con la serie que le da nombre»).
   Cryer (pp. 240-241) liga el modelo con la serie, dice que «llegó a conocerse» como airline y que lo popularizó la primera edición de Box y Jenkins, a la que fecha en 1976; FPP3 §9.12 fecha en 1970 el texto
   que popularizó el ARIMA. Las dos fuentes **discrepan en el año** y ninguna dice que sean ellos quienes lo nombraron; las ediciones están en la biblioteca sin texto. «El más usado del mundo» y
   «casi cualquier serie mensual» no los dice nadie (Cryer y Shumway dicen que ajusta bien a muchas series con pocos parámetros). Es una atribución a personas y a una obra, con año.
5. **La tabla «dónde brilla / dónde falla» del M11 y su atribución a «las competencias M4 y M5 y la literatura»** — `c5-m11-11` a `c5-m11-30`. Seis métodos y dieciocho celdas con afirmaciones de rendimiento sin cifra
   y sin fuente. Lo que FPP3 sostiene: Prophet rinde peor que ETS y ARIMA *en dos ejemplos* y «rara vez» mejora la exactitud (`advanced.txt:217`, `:228`), no «en competencias estándar»; la regresión armónica
   supone estacionalidad fija (§10.5); las redes no dan intervalos directos y se simulan (§12.4). Sin hallar: «ETS no admite regresores ni modela la autocorrelación residual», «quiebres estructurales y muchas series a la vez»
   como fallo del SARIMA, todo lo de LSTM y transformers (FPP3 solo cita un balance de redes recurrentes) y **todo lo atribuido a M4 y M5** (`c5-m11-30`): ninguna obra de la biblioteca ni FPP3 los nombra. Y H&K (2008, p. 12) dicen que en la
   competencia M3 los modelos de suavizamiento exponencial rindieron mejor que los ARIMA en datos estacionales: [TENSIÓN] con «sigue ganando en el régimen para el que fue diseñado» (`c5-m11-10`). El párrafo que la
   acompaña (`c5-m11-29`) afirma que poner cifras «de memoria» es lo que el material enseña a no hacer, mientras la tabla pone afirmaciones de memoria: [TENSIÓN con la norma 2].
6. **La regla de los dos puntos de AICc sin declararla convención** — `c5-m6-07` («dentro de 1.7 puntos… la evidencia no separa mucho»), `c5-m11-49` («a menos de dos puntos de AICc»). [TENSIÓN con la R4 del cap. 4], que la declaró
   convención del capítulo (`c4-m6-08`, `c4-m7-14/-15`); ni Cryer, ni FPP3 ni H&K dan umbral. Aquí aparece como si fuera de las fuentes.
7. **Ljung–Box «con al menos 2m rezagos»** — `c5-m4-24`, `c5-m6-04`, `c5-m11-36`, `c5-m12-09` (pregunta 5 del simulacro). FPP3 §5.4 sugiere `ℓ = 2m` para datos estacionales **con tope en `T/5`** (`toolbox.txt:359`); no dice «al menos». Con series cortas el estudiante
   que pida 36 rezagos con `n` pequeño sobrepasa el tope. Cryer usó 22 g. l. con el airline de CO2 (p. 239 impr.), es decir, 24 rezagos y dos parámetros. [CON-MATIZ].
8. **El argumento financiero de la TRM y la «volatilidad con patrón de calendario»** — `c5-m8-10`, `c5-m8-11`, `c5-m8-12`. El M8 explica por qué una serie financiera no tiene estación con un argumento de arbitraje y de «mercado razonablemente eficiente»,
   sin cita ni nombre, justo lo que el cap. 4 reescribió atribuyéndolo a FPP3 §1.1 (`c4-m10-24`, que solo cubre el pronóstico de los tipos de cambio, no la ausencia de patrón mensual); añade que «el volumen o la volatilidad sí suelen tener patrón de
   calendario» [NO HALLADO]. Y «cuatro evidencias independientes» (también en el Ejercicio 3 y la autoevaluación 1): las cuatro se calculan sobre la misma serie de 138 meses.
9. **Las lecturas recomendadas** — `c5-m11-54` [DISCREPA]: la tabla remite a FPP3 §12.1 para «TBATS», y TBATS no aparece en ninguna de las diez secciones extraídas de la 3.ª ed. (0 ocurrencias); §12.1 trata STL con varios periodos y regresión armónica
   dinámica. `c5-m11-56` [EJEMPLAR]: «Shumway y Stoffer, Cap. 3.9, el caso birth»: la 4.ª ed. no se puede leer; en la 3.ª, §3.9 existe con ese título (impr. 154) y desarrolla el SARIMA (ejemplos 3.43-3.46), pero `birth` solo aparece como problema 3.38 y en la lista
   de datos. `c5-m11-57`: Box et al., «Cap. 9»: sin texto. El cap. 4 ya halló que la numeración de Shumway difiere entre ediciones (`c4-m10-77`).
10. **Periodos y Fourier** — `c5-m1-04`, `c5-m10-01`, `c5-m10-03`, `c5-m10-07`. FPP3 §12.1 dice que la serie semanal tiene un periodo anual no entero (≈ 52.179); el capítulo da 52 sin matiz en el M1 y atribuye el 365.25 a las diarias; el «m = 336» de las de media hora
   no está en FPP3 (la 10.5 da 48). «El máximo útil es `K = m/2`; ahí los términos son tantos como meses y equivalen a `m − 1` indicadoras»: con `K = 6` hay once columnas útiles, no doce (el propio capítulo lo documenta; `?fourier` dice 2K y devuelve 11, comprobado).
11. **Regresores de calendario** — `c5-m9-03` (Pascua: FPP3 §7.4 reparte la indicadora entre meses cuando la fiesta cruza el mes; el capítulo la pone en «el mes que contiene el Domingo de Pascua»), `c5-m9-07` («su error estándar es mayor que el de un MCO ingenuo»: FPP3 §10.1 dice que
    los valores p tienden a ser demasiado pequeños, no la frase del capítulo), `c5-m9-13` («el criterio de información y el error de pronóstico responden preguntas distintas»: FPP3 §7.5 presenta el AICc como criterio con el pronóstico por objetivo),
    `c5-m9-14` (el algoritmo de la fecha de Pascua atribuido a «Meeus/Butcher» sin obra) y `c5-m11-72` («un coeficiente significativo y además igual a su valor teórico es una confirmación fuerte»: no rechazar `β = 1` con un error estándar de 0.446 no la confirma).
12. **Avisos sobre statsmodels sin documentación en la biblioteca** — `c5-m2-25`, `c5-m6-10`, `c5-m6-12`, `c5-m7-17`, `c5-m9-08`, `c5-m9-15`, `c5-m10-14`, `c5-m10-15`. Ninguno tiene obra; **todos los comprobables se reprodujeron ejecutando statsmodels 0.14.6**
    (`simple_differencing` da `nobs` 144 frente a 131; con la opción por defecto el pronóstico es el de la serie original y con `True` el de la diferenciada; `K = 6` da 12 columnas de rango 11; `plot_acf` tiene `lags=None`; statsmodels no trae `ndiffs/nsdiffs`),
    salvo una explicación que se contradice: el comentario del M9 atribuye la diferencia de errores estándar a que «no tratan igual la diferenciación de los regresores», cuando el mismo módulo dice que SARIMAX con `d > 0` diferencia también los regresores (y FPP3 dice lo mismo de `ARIMA()` de fable).
13. **Derivaciones presentadas como resultados generales** — `c5-m2-18` (la factorización de `γ0` y de la ACF cuando solo hay parte MA y `q < m`: Cryer la prueba solo para `q = Q = 1`; el ejemplo de `q ≥ m` con 2.300 frente a 1.700 no tiene generador) y `c5-m2-20` («con parte AR no hay factorización»:
    sin fuente; la tabla de `φ = 0.6, 0.8, 0.9, 0.95` con 3.073…20.111 y el 1.5217 tampoco tienen generador, salvo la fila de 0.9). También `c5-m5-07` (los pesos ψ del airline no están en ninguna fuente; el método general sí: FPP3 §9.8, Cryer §9.3).
14. **Cifras sin generador (norma 1)** — `c5-m2-18`, `c5-m2-20` (arriba); `c5-m3-20` (el valor crítico 0.463 del KPSS está tecleado en un comentario; es el que da statsmodels, comprobado, y el que atribuye a Kwiatkowski et al. el cap. 2); `c5-m11-07` (las cifras de la explicación del corte en 1958: 3.4 %, 6.2-21.8 %, 4.7 y 6.9 %, 12.4 y 11.2 %, 9.4 y 12.8 %,
    10.6 y 13.1 %, «14 orígenes, 12 entre 1957-05 y 1959-01»: no están en `genera_cap5.R`, `genera_cap6.R` ni en los JSON de salidas, y la autoevaluación 8 repite la explicación, `c5-m11-73`); `c5-m11-44` y `c5-m11-50` (178.2089, 176.9982, 180.200 y 467 tecleados en bloques de R del Ejercicio 1 y 3 en lugar de salir de los ajustes).
    Un diagnóstico paralelo de cifras (`diag/lector_cifras.*`) cubre el resto; aquí solo se anota lo que aparece junto a una afirmación.

Lo que sí sostienen las fuentes y conviene citar en la ronda de fuentes (candidatas con su localizador, todas en el TSV):
la definición del SARIMA con regulares en minúscula, estacionales en mayúscula y términos multiplicados (FPP3 `arima.txt:644-648`; Shumway Def. 3.13, `p0170`; Cryer §10.3, `p0244`);
la tabla de ACF y PACF de los SARMA puros (Shumway Tabla 3.3, `p0168`; FPP3 `arima.txt:652-662`; Cryer §10.1, `p0239-p0240`) y las lecturas de los rezagos intermedios y de que lo habitual es combinar parte regular y estacional (Cryer `p0240`);
el modelo multiplicativo como ARMA con coeficientes restringidos y su parsimonia (Cryer `p0241`; Shumway ej. 3.45, `p0171`, que muestra el producto en el rezago 13);
las autocorrelaciones del MA×SMA (Cryer ec. 10.2.2-10.2.5; el convenio de signo de Cryer es el contrario al del capítulo) y del P = q = 1 (ec. 10.2.11);
la diferencia estacional y su coste de `s` datos (Cryer `p0243`; FPP3 `:77`), que `∇∇m` es el producto de polinomios y conmuta (FPP3 `:119`, `:200`) y que conviene la estacional primero (`:119`; H&K p. 10);
que el AICc exige los mismos órdenes de diferenciación (FPP3 `:851`, `:1187`) y que entre clases solo vale la comparación fuera de muestra (FPP3 `:887-926`);
el diagnóstico con `ℓ = 2m` y tope `T/5` (FPP3 `toolbox.txt:359-361`) y 22 g. l. en el ejemplo de Cryer (`p0249`);
los pronósticos del airline por recursión y su forma tendencia más componentes periódicas (Cryer ec. 10.5.20-10.5.23, `p0253-p0254`), la mediana al retrotransformar y los intervalos que se transforman (FPP3 `toolbox.txt:601-613`);
la regresión armónica y sus límites (FPP3 `regression.txt:494-531`, `dynamic-regression.txt:283-302`), STL + ARIMA (FPP3 `toolbox.txt:640-680`, `?stlm`), los ajustes de calendario y la Pascua (FPP3 `decomposition.txt:15-19`, `regression.txt:476-492`),
la relación ARIMA/ETS (FPP3 `arima.txt:865-891`; H&K p. 12) y Prophet y las redes (FPP3 `advanced.txt:199-228`, `:362-420`).

## Atribuciones que el capítulo hace hoy sin cita

- **Box y Jenkins**: el nombre del modelo airline y su serie (`c5-m5-02`), «el de 1970» (`c5-m11-10`), la lectura «Cap. 9» (`c5-m11-57`), «ciclo de Box–Jenkins» (`c5-m4-11`, [= c4-m2-02]).
- **Hyndman y Athanasopoulos, Shumway y Stoffer, Box et al., Brockwell y Davis**: solo en el pie y las lecturas (`c5-m0-01` a `-04`, `c5-m11-53` a `-57`); Brockwell y Davis ni siquiera está en las lecturas.
- **Competencias M4 y M5 y «la literatura de forecasting»** (`c5-m11-30`), **Prophet** (`c5-m11-20`, `-22`), **LSTM y transformers** (`c5-m11-24` a `-28`).
- **Holt–Winters**, **Fourier**, **STL**: nombrados sin autor ni año (STL tiene texto en la caché: `texto/cleveland1990stl`; Holt y Winters, Taylor y Letham y Hewamalage et al. los cita FPP3).
- **Ljung–Box** (42 menciones, ninguna con cita; Cryer pp. 183-184 y FPP3 §5.4 lo respaldan), **Shapiro–Wilk**, **KPSS y ADF**, **OCSB** (`c5-m3-22`), **Durbin–Levinson** y **Guerrero (1993)** (comentarios del JS, `c5-m0-12`, `c5-m0-13`).
- **Meeus/Butcher** (`c5-m9-14`), **Box–Muller y mulberry32** (`c5-m0-11`): epónimos de algoritmos sin obra.
- **A una teoría o un estatus**: «mercado razonablemente eficiente» (`c5-m8-11`), «el SARIMA más usado del mundo» (`c5-m5-03`), «el error más caro del capítulo» (`c5-m8-06`), «el error de conteo más frecuente» (`c5-m4-06`), «el paso que más se hace en el orden equivocado» (`c5-m4-18`), «la regla de la varianza» (punto 1),
  «la convención para series estacionales es `h = 2m`» (punto 7).

## Obras que faltan

- **En la biblioteca pero sin texto en caché** (hoy no se pueden contrastar): `box1970time`, `box1976time`, `box2016time` (nombre del airline, «Cap. 9», año); `shumway2017time` (la 4.ª ed., la que se cita; la caché es la 3.ª, que sí trae §3.9);
  `brockwell2016introduction` (pie); `kwiatkowski1992testing` (valor crítico 0.463 del KPSS, tecleado); `ljung1978measure` (nombrado 42 veces); `guerrero1993timeseries` (comentario del JS); `wang2006characteristic` (la «fuerza estacional» de `nsdiffs(test = "seas")`);
  `hyndman2018forecasting` (FPP2: no consta en qué obra está lo que las lecturas atribuyen a §12.1 sobre TBATS).
- **No están en la biblioteca** y las fuentes leídas las nombran: Brockwell y Davis (1991), fuente de `?USAccDeaths`; Osborn, Chui, Smith y Birchenhall (1988) (OCSB), Canova y Hansen (1995) y Hylleberg, Engle, Granger y Yoo (1990) (HEGY), citadas en `?nsdiffs`;
  Taylor y Letham (2018) (Prophet) y Hewamalage et al. (2021) (redes recurrentes), citadas en FPP3; Holt (1957) y Winters (1960), citadas en FPP3 §8.3; Keeling y Whorf (Scripps) para `co2`.
- **Sin ninguna obra identificable**: las competencias M4 y M5, la «literatura de forecasting», una obra de finanzas con patrón de calendario en el volumen y la volatilidad, el algoritmo de la fecha de Pascua (Meeus/Butcher) y Box–Muller/mulberry32.
- **Datos y software** (colección «4 Datos y software»: hoy solo figura R): la TRM de datos.gov.co (conjunto 32sa-8pi3; `c5-m0-10`, `c5-m1-13`, `c5-m8-07`); `statsmodels` (diez filas, comprobadas por ejecución, sin documentación); `forecast` (las ayudas de `nsdiffs`, `fourier`, `stlm` y `BoxCox.lambda`
  no están en `_local/web/`; sí `Arima`, `ndiffs`); `pmdarima` (no instalado) y la documentación de `tseries`/`urca` si se llegara a citar la prueba KPSS.
- **Epónimos que el encargo listaba y el capítulo no nombra**: Canova–Hansen y X-13 (0 menciones; Canova–Hansen es, sin embargo, la prueba que el artículo de H&K usa para `D`), y HEGY.

## Hallazgos colaterales (no son de fuentes)

- **Logística vencida** (`c5-m12-01`, `c5-m12-02`): el Módulo 12 describe en presente un quiz en Brightspace de «cincuenta minutos y doce preguntas» que se aplicó el 11 de noviembre de 2026; hoy es 23 de noviembre. Confirmar si se reescribe en pasado.
- **El pie omite las obras con las que más se contrastó**: no lista Cryer y Chan ni Hyndman y Khandakar (2008) ni Hamilton, y sí Brockwell y Davis, que no se usa. Las lecturas tampoco traen Cryer y Chan, cuyo capítulo 10 es la fuente más completa del SARIMA en la caché.
- **Mojibake en el JSON de datos** (no visible en pantalla): `SERIES_CAP5` y `DATOS_CAP5` llevan `<c3><ad>` en «aerolíneas», «vía» y «Concentración» (l. 6301-6302); el capítulo 4 no lo tiene (lo escribe `genera_cap5.R` con otra configuración de la codificación que `genera_cap4.R`).
- **Tres fechas para la TRM**: el JSON dice «consulta: 2026-07-24», el cap. 4 dice 2026-07-26 y los bloques cortan en 2026-06 (`c5-m0-10`).
- **Remisión interna dudosa**: el comentario de Python del M2 dice que el reparto de grados de libertad del `σ²` es el que el M6 «discute para el AIC», y el M6 discute el n efectivo y el prior difuso (`c5-m2-22`).
- **Dos cifras de la banda del correlograma**: el M4 la nombra `±2/√n` y el resto del capítulo `1.96/√n` (`c5-m4-10`).

## Método y límites

Cada fila se construyó con una comprobación de que `texto` es subcadena de la línea indicada del HTML (sin etiquetas, con los espacios normalizados) y de que las claves están en `referencias.json` (`diag/fuentes_valida.py`: 281 filas, 0 problemas;
`diag/fuentes_construye.py` resuelve cada `ruta:línea` buscando el patrón en la caché y falla si no lo halla). Las cifras de comprobación citadas se recalcularon (`diag/fuentes_comprobaciones.R`, R 4.6.0 y forecast 9.0.2; `diag/fuentes_comprobaciones.py`,
statsmodels 0.14.6); de las ayudas solo se imprimen booleanos. Ningún libro se cita literalmente en el TSV ni aquí: las filas parafrasean y dan la ruta.

Límites: «hallado» es la lectura de quien inventarió y los pasajes los verifica otra persona. Cryer es un PDF con capa de texto de buena calidad; Shumway, la 3.ª ed. y parcial; el «impr.» de Cryer se tomó de la regla página del archivo − 10 y el de Shumway, − 13 (las
dos comprobadas con el encabezado de cada página). No se pudo leer ninguna edición de Box y Jenkins, Kwiatkowski et al., Ljung y Box, Brockwell y Davis, FPP2 ni la documentación de statsmodels. El inventario no juzga la corrección matemática, el estilo ni las gráficas; las señales de «matiz» y
«tensión» son de fuente (o de coherencia con el capítulo 4), no de corrección. Las filas que repiten a otras heredan sus etiquetas, de modo que el recuento de `[SIN GENERADOR]` cuenta tres heredadas. No se editó el capítulo ni nada fuera de
`bibliografia/contraste/cap5_inventario.tsv` y `diagnostico/cap5/` (`fuentes.md` y `diag/fuentes_*`); en `diagnostico/cap5/` hay archivos de otras sesiones (ejercicios, gráficas, lector, cifras) que no se tocaron.

Reproducir (desde la raíz del repo): `python3 diagnostico/cap5/diag/fuentes_construye.py` (escribe el TSV desde `fuentes_filas_{a,b,c,d}.py`), `python3 diagnostico/cap5/diag/fuentes_valida.py`,
`python3 diagnostico/cap5/diag/fuentes_cuenta.py`, `Rscript diagnostico/cap5/diag/fuentes_comprobaciones.R`, `python3 diagnostico/cap5/diag/fuentes_comprobaciones.py`.
