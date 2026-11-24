# Capítulo 5 · ronda R3 («estructura») · cambios

Ronda R3 del `PLAN_Mejora_Cap5.md` (tareas T3.1 y T3.2; decisiones D6, D7 y D8). Fecha: 2026-11-24. Un solo redactor; sin commit
ni push. Base: `ad84aa7` (la R1 y la R2 publicadas). Especificación: `diagnostico/cap5/lector_estudiante.md`, leída contra el capítulo
tal como lo dejaron la R1 y la R2 (los pasajes se localizaron por su texto), más lo que `R1_cambios.md` dejó para esta ronda.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/cap5/templates_1_3.html` | M1 (apertura, convención de ρ̂ₖ y de la banda, bloque R/Python del ARIMA(0,1,5)), M2 («Cómo se escribe» trasladado tras la definición, σ̂² impreso, el satélite una vez, comentario de Python, cierre, voz), M3 (intro de `cuatro-combinaciones`, `nsdiffs` con las dos pruebas en el bloque, cierre) |
| `ensamblado/cap5/templates_4_6.html` | M4 (banda ±1.96/√n, el ciclo frente al del cap. 4, cierre), M5 (cierre, voz), M6 (intro del explorador, cierre) |
| `ensamblado/cap5/templates_7_9.html` | M7 (las etapas son las del M4, rango relativo, banda de los residuales, remisión al M1, `biasadj`, bloque R, cierre), M8 (intro, «cuatro comprobaciones, tres evidencias», cierre), M9 («dos clases», η_t, intro, RMSE y «fuera de muestra», bloques R y Python, cierre) |
| `ensamblado/cap5/templates_10_11.html` | M10 («media horarios», η_t, intro de `armonicos-K`, «Parámetros totales», cierre), M11 (la comparación reescrita, una sola tabla, h3 nuevo, bloque R/Python del clímax, remisión de la nota, voz) |
| `ensamblado/cap5/chapter.js` | solo el M11: el simulador `comparativa-particion` (sin selector de métrica; la lectura da el sesgo medio) y `TABLAS_RANKING['comparativa']` (columnas Escala y k, métricas sin doble redondeo, descripción y pie que no adelantan). Nada del quiz |
| `ensamblado/ensambla_cap5.py` | una glosa de «rejilla» en la etapa 5 del ciclo; `courseData` con los minutos medidos y su convenio |
| `precalculo/genera_cap5.R` | `metricas()` devuelve además `exactas` (las tres métricas sin redondear); nada más |
| `precalculo/salidas/cap5_sarima.json`, `cap5_datos.js` | regenerados: 27 hojas nuevas (`…exactas.{rmse,mae,mape}` de los 8 métodos y de la salvedad de la armónica) y `generado`; **las 9 055 hojas de antes, idénticas** (`r3_compara_json.out`) |
| `Htmls_Series/capitulo-5-sarima.html` | reensamblado; reproducible byte a byte (md5 `93ee838b…` en dos pasadas) |
| `diagnostico/cap5/comprobaciones/r3_*` | guiones y salidas (abajo) |
| `diagnostico/cap5/capturas/r3/` | capturas a 1200 y 375 px (git las ignora) |

El capítulo 6 se reensambló y queda **idéntico a HEAD** (`git status` no lo lista). No se tocó: los caps. 1–4, el armazón, el
componente `.mapa-estacional`, la plantilla, `simulacro.js` ni el M12, las preguntas, opciones, pistas y retros del quiz, el
enunciado y la solución de los ejercicios 1–3, la nota del Excel, las diapositivas ni `bibliografia/`. **Ningún título de módulo ni
id cambia.** No se añadió ningún `<cite>`, `data-afirma`, autor, año, sección ni DOI. Ninguna clase nueva de Tailwind (una primera
versión del bloque de Python del M11 usaba `np.resize`, y `resize` es una utilidad de Tailwind: la hoja de las doce páginas salía
distinta; se cambió por un índice y `--comprobar` vuelve a dar verde).

**Cómo se editó.** `r3_edita.py` (copia del del cap. 4, con un tercer tipo de edición, `despues()`, que se aplica tras los
traslados) más siete listas: `r3_ediciones_m1.py`, `_m2.py`, `_m3.py`, `_m4_6.py`, `_m7_9.py`, `_m10_11.py`, `_voz.py`,
`_minutos.py` y `_genera.py`. **61 sustituciones literales y 1 traslado**, cada «antes» único en HEAD; una de ellas (`entre()`)
sustituye el bloque del M11 que va de su primer párrafo a la cabecera de la tabla de los 61 orígenes. Parte siempre de HEAD;
`--comprobar` da «idéntico a HEAD + ediciones» en los siete archivos. El código nuevo va sin escapar en las listas y pasa por
`html.escape`. Después: `Rscript precalculo/genera_cap5.R`, `python3 ensamblado/ensambla_cap5.py` y `python3 ensamblado/ensambla_cap6.py`.

---

## T3.1 · Orden sin renumerar (D6), módulo por módulo

| Mód. | Qué se hizo | Por qué (lector) |
|---|---|---|
| **M1** | La apertura dice que el bloque del módulo vuelve a ajustar el ARIMA(0,1,5) del cap. 4, y nombra el *airline* con sus órdenes y con los módulos que lo escriben (M2), lo estudian (M5) y lo diagnostican (M6). **El bloque de R** ajusta `Arima(ap, order = c(0,1,5))` e imprime ρ̂₁₂ = 0.7245, ρ̂₂₄ = 0.6727, Q(24) = 222.4 y p < 10⁻⁶; **el de Python**, con `statsmodels` (converge; 0.7218, 0.6676, 219.3, y una línea con las cifras de R). Un párrafo nuevo fija las dos convenciones del capítulo (ver Notación) | promesa 1; N «ARIMA(0,1,5) sin código»; P «el *airline* entra como sabido» |
| **M2** | **«Cómo se escribe en la práctica» pasa de última sección a primera**, justo tras la definición, con un párrafo que dice qué trae; su bloque imprime ahora también σ̂² = 0.001371. Así el *airline* ajustado (θ̂, Θ̂, σ̂², B13) está a la vista antes de que lo usen la derivación plegada y la nota «El *airline* es el caso exacto», y el primer `Arima(…, seasonal = …)` del capítulo es el que se explica. La derivación remite al bloque «al principio del módulo». Cierre hacia el M3 | P «el *airline* ajustado se usa 320 líneas antes de mostrarse»; P «el primer `Arima()` está en Momentos» |
| **M3** | Intro de `cuatro-combinaciones`: dice que se abre con las dos diferencias y pregunta (¿baja ρ̂₁₂ con solo ∇?) en vez de dar el 0.841 y la frase que no se entendía. La «Trampa de versión» tiene ya su bloque: `sapply(… nsdiffs(x), nsdiffs(x, test = "ocsb"))` sobre log(AP) y `USAccDeaths` imprime 1/0 y 1/0. Cierre hacia el M4 | intro que adelanta; N «ocsb devuelve 0 sin bloque»; P 4040 |
| **M4** | «Con dos etapas insertadas» → el ciclo del cap. 4 tenía cuatro etapas (identificación, estimación, diagnóstico y uso); aquí la identificación se abre en cuatro, estimar y diagnosticar van juntas en la quinta y el uso va después del ciclo (M7). «Rejilla» se glosa en la etapa 5 del ciclo (`ensambla_cap5.py`). Cierre hacia el M5 | promesa 7; P «rejilla» |
| **M5** | Cierre hacia el M6 | sin cierre |
| **M6** | Intro del explorador: se abre en el (0,1,1)(0,1,1)₁₂ y pregunta si el mínimo de AICc y el de BIC son el mismo (antes lo afirmaba). Cierre hacia el M7 | intro que adelanta |
| **M7** | Un párrafo de entrada: las cinco etapas son las del ciclo del M4. El «rango relativo 1.848» se define (recorrido entre media) y lo calcula el bloque. La banda ±0.163 de los residuales se explica (144 residuales). «El problema del Capítulo 4, cerrado» remite al bloque del M1. **`biasadj`**: el aviso de la mediana dice que, con el logaritmo dentro del modelo (`lambda = 0`), `forecast()` devuelve la mediana y con `biasadj = TRUE` una aproximación de la media (525.46 → 530.58 a 24 meses), y que cuál conviene depende de la métrica, que es del cap. 6; el bloque lo calcula y deja de rotular «media» lo que es la mediana. Cierre hacia el M8 | P «etapas sin decirlo»; N 1.848; P dos bandas; remisión rota del cap. 6 |
| **M8** | Intro: se abre con log(AirPassengers). «Cuatro evidencias independientes» → cuatro comprobaciones que son tres evidencias (la 3.ª y la 4.ª miran el mismo Φ̂). Cierre hacia el M9 | P «cuatro / tres evidencias» |
| **M9** | «Dos clases» con cuatro filas → la tabla repasa cuatro y dice cuáles construye el módulo. **RMSE y «fuera de muestra» se presentan aquí**, donde aparecen por primera vez, y los bloques de R y de Python calculan los dos RMSE (43.18 y 45.48; Python converge y coincide). Intro: estado inicial. «Algo bonito» → «algo más». Cierre hacia el M10 | P «dos clases»; P/N RMSE sin presentar y sin bloque |
| **M10** | «Media horarios» → «tomados cada media hora con un patrón diario y otro semanal». Intro de `armonicos-K`: se abre en K = 3 y pregunta desde qué K dejan de rechazar (antes daba K = 5). Una línea explica «Parámetros totales» (términos + coeficientes del ARIMA + σ²). Cierre hacia el M11 | P «media horarios»; intro que adelanta; N «Parámetros totales» |
| **M11** | Ver D7 abajo | |

**Remisiones rotas (las cuatro del diagnóstico):** M1 → «Módulo 5» (la R1 ya la llevó al M6); M6 → manchas solares (la R1 la quitó);
**M11 → «el código del capítulo»**: la nota dice ahora que las cifras «las reproduce el bloque de código de la comparación», que existe;
**cap. 6 → `biasadj`**: el cap. 6 dice «Esto explica el `biasadj` del Capítulo 5» y explica que `forecast()` devuelve la mediana salvo
con `biasadj = TRUE`; el M7 lo nombra ahora junto a la media lognormal, en esos términos. El cap. 6 no se tocó.

**Cierres.** M1 y M11 ya cerraban; **M2 a M10 ganan un párrafo final que apunta al siguiente** (`r3_revisa.out`, «último elemento»).

**Intros de simulador frente al estado inicial.** La R2 arregló M2, M4, M7 y M11; revisadas las demás contra los `params` de
`chapter.js`: M3 `cuatro-combinaciones`, M6, M8, M9 y M10 dicen ahora con qué se abren (y las tres que adelantaban el resultado, M3,
M6 y M10, preguntan). M1, M2 (`receta-mes`), M3 (`tienda`, `sobrediferenciacion`) y M5 no describían ningún estado distinto del inicial.

## T3.1 · El M11, ordenado (D7), sin partirlo

Orden de las secciones (`h3`) y palabras de prosa con el convenio de `r3_minutos.py` (`r3_secciones_m11.py`):

| Sección | Antes | Después |
|---|---|---|
| (apertura) | 36 | 36 |
| La comparación, hecha mal a propósito | 896 · tabla ordenable + simulador + tabla estática + tabla de 61 orígenes · 0 `<pre>` | 545 · tabla ordenable + simulador |
| **La misma comparación, desde 61 orígenes** (nueva) | — | 597 · tabla de 61 orígenes · **2 `<pre>`** (R y Python) |
| SARIMA frente a lo que se usa hoy | 383 | 384 |
| Resumen del capítulo | 200 | 200 |
| Autoevaluación · Ejercicios · Excel · Lecturas · Lo que viene | 345 · 162 | 345 · 160 |
| **Total** | **2 022** | **2 267** |

Qué cambia:

- **Presentaciones en su primer uso.** El párrafo de entrada define fuera de muestra, RMSE, MAE y MAPE; el siguiente presenta los
  ocho métodos: los cinco de la familia ARIMA (ya vistos) y los tres nuevos, el **ETS** (extiende el suavizamiento exponencial simple y
  el método de Holt del cap. 4, M1, con estación; sus letras: error, tendencia, estación; A, A_d, M) y el **naïve estacional** (el mismo
  mes del último año observado, sin estimar nada). La columna k se explica ahí.
- **La comparación se muestra una vez.** Queda la **tabla ordenable** (la única con las tres métricas de los ocho), con las columnas
  Escala y k que tenía la estática; **sale la tabla estática**, y **la lectura del simulador ya no repite el ranking**: el selector de
  métrica desaparece (la tabla ya ordena) y la lectura da el **sesgo medio** de cada método encendido, que es lo que explica el
  párrafo del crecimiento de 1958 (el SARIMA, 39.45 = su MAE). La descripción y el pie de la tabla ya no dicen «las tres dejan al SARIMA
  cuarto» ni «sobre 61 orígenes el SARIMA pasa a primero»: dicen cómo se ordena, el corte, la prueba y qué es k.
- **Doble redondeo, arreglado.** La tabla ordenable formateaba a 2 decimales las métricas que el JSON guarda a 3: mostraba **16.13**
  (MAE del ETS sobre el log) y **77.00** (RMSE del naïve), cuando R da 16.12 y 76.99 (la tabla estática, que salía, sí decía esos). El
  generador guarda ahora también las métricas sin redondear (`exactas`) y la tabla las usa: las 24 cifras coinciden con las del bloque
  de R (`r3_revisa.out`).
- **El clímax gana su sección y su código.** h3 nuevo antes del aviso «Esa conclusión es falsa», que ya no dice «demostrarlo es la
  razón de ser del Capítulo 6» y sí cómo se construyen los 61 orígenes (de 1954-12 a 1959-12) y que la tabla promedia los 61 RMSE (la
  convención que el cap. 6 cita con su 16.81). **Bloque de R** (94 líneas, menos de un minuto): la partición con siete métodos y su
  sesgo, `auto.arima` = *airline*, el crecimiento de los totales anuales y lo que pronostican el SARIMA, el ETS y la armónica para
  1959 y 1960, y los orígenes móviles a h = 12 (61) y h = 24 (49), con los porcentajes, los 14 orígenes en que el SARIMA no es el
  mejor y el error del mes 12. Cada origen se ajusta una vez y se pronostica a 24 (los 12 primeros sirven para h = 12): 45 s en vez de
  77. **Bloque de Python** (58 líneas, 3 s): el SARIMA y el naïve estacional en la partición, el crecimiento y los 61 orígenes; se
  estima con `simple_differencing=True` (converge en los 62 ajustes) y se pronostica con el modelo en niveles; coincide con R en las
  cifras impresas. Lo dice: `statsmodels` no trae `ets()` ni la elección de `auto.arima`.
- **«Once módulos» → «diez»**; «demoledora» → «un veredicto»; el puente con el cap. 6 se dice dos veces (la nota y «Lo que viene»),
  no cuatro. **El resumen sigue siendo lo último antes de la evaluación.**
- **Las palabras suben** (2 022 → 2 267): las presentaciones y la entrada del bloque. Lo que se ahorra es leer tres veces la misma
  tabla, no palabras.

## T3.2 · El satélite en el M2 y la notación

**El satélite, una vez.** La heladería es la explicación (no se toca). La primera viñeta deja de repetir el peso; la apertura de
«Multiplicar no es sumar» deja de contarlo otra vez y remite a la heladería (y sale la frase-puente que la duplicaba); el paso 4 de su
desarrollo remite a la ACF de la tercera viñeta en vez de repetir 0.6016, 0.7011, 0.4230 y 0.4218. La derivación de la parte MA
(signo +θΘ) se queda: es lo único que el resto no dice, y ahora remite al bloque que ya está arriba. El satélite en M4 y M7 no se tocó.

| Costura | Convención | Dónde |
|---|---|---|
| `n_t` frente a `n` | El error de la regresión es **η_t** («una letra distinta de la n del tamaño de la muestra»); `n` sigue siendo el número de observaciones | M9 (definición), M10 (definición) |
| ρ̂ₖ frente a r_k | **ρ̂ₖ** en la prosa; se avisa una vez que la salida de R y otros textos la escriben r_k (el simulacro usa r₁₂) | M1 |
| La banda | **±1.96/√n, con n las observaciones de la serie a la que se le mide la ACF** (si se diferenció, las que quedan). El M4 decía ±2/√n; el M7 explica su ±0.163 (144 residuales) frente al ±0.171 (131 observaciones) | M1, M4, M7 |
| «tres»/«cuatro» evidencias | El M8 tiene **cuatro comprobaciones que son tres evidencias**: la prueba, el correlograma y el ajuste forzado, que se lee por su t y por su AICc. Casa con el enunciado del E3 («tres evidencias independientes»). La varianza no vuelve | M8 |
| Voz | Las cuatro formas en primera persona del plural que quedaban («Tomamos», «Multiplicamos», «Escribimos», «hemos construido») pasan a impersonales | M2, M5, M11 |

## Minutos medidos (D8)

Medido de nuevo tras las correcciones del verificador. Herramienta: `r3_minutos.py`, copia de la del cap. 4 sin cambiar fórmula ni convenio (palabras/180 + 3 por simulador + 2 por
bloque; pista y solución abiertas; sin plegados ni quizzes). Antes = HEAD; se declara la columna «abierto», como en los caps. 2–4,
con su comentario en `courseData`.

| Mód. | Palabras antes → después | Medido antes | Medido después | Declarado antes → ahora | Distancia ahora |
|---|---|---|---|---|---|
| M1 | 690 → 800 | 8.8 | 9.4 | 14 → **9** | 0.4 |
| M2 | 1 528 → 1 647 | 20.5 | 21.1 | 12 → **21** | 0.1 |
| M3 | 1 437 → 1 481 | 21.0 | 21.2 | 16 → **21** | 0.2 |
| M4 | 1 154 → 1 264 | 11.4 | 12.0 | 16 → **12** | 0.0 |
| M5 | 566 → 605 | 8.1 | 8.4 | 14 → **8** | 0.4 |
| M6 | 588 → 636 | 8.3 | 8.5 | 16 → **9** | 0.5 |
| M7 | 1 107 → 1 300 | 11.2 | 12.2 | 21 → **12** | 0.2 |
| M8 | 668 → 767 | 8.7 | 9.3 | 16 → **9** | 0.3 |
| M9 | 679 → 807 | 8.8 | 9.5 | 14 → **10** | 0.5 |
| M10 | 793 → 880 | 9.4 | 9.9 | 16 → **10** | 0.1 |
| M11 | 1 986 → 2 358 (abierto 2 708 → 3 080) | 14.0 cerrado · 24.0 abierto | 18.1 · 28.1 | 20 → **28** | 0.1 |
| M12 | 578 | 3.2 | 3.2 | 50 → **50** (el reloj) | — |
| M1–M11 | | 140.2 | 149.6 | 175 → **149** | |

Distancia máxima: **0.5 min** (el objetivo era < 3). El comentario de `courseData` dice lo que no se cuenta: resolver los ejercicios
y ejecutar el código, los plegados (unos 4 min en M2, M3 y M5), la autoevaluación del M11 (unos 17 min de lectura) y, en el M12, la
lectura: sus 50 min son el reloj. **La portada no declara minutos del cap. 5** (la tarjeta dice «12 módulos · 14 simuladores», que
sigue siendo cierto): nada que decidir ahí.

## Cifras de la prosa y de dónde sale cada una

`r3_cifras.R` (→ `r3_cifras.out`) recalcula en R, aparte de la página, **48 cifras** que la ronda escribe, mueve o deja en la prosa:
**48 coinciden, 0 no**.

| Cifras | Salen de |
|---|---|
| ARIMA(0,1,5): ρ̂₁₂ 0.7245, ρ̂₂₄ 0.6727, Q 222.4, p < 10⁻⁶ (M1, M7) | **bloque del M1 (líneas nuevas, R y Python)**; antes solo del cap. 4 |
| Bandas 0.163, 0.231, 0.091, 0.167, 0.171 (M1, M7) | 1.96/√n con el n de cada serie; los bloques de M1, M7 y M8 imprimen las suyas |
| θ̂, Θ̂, σ̂² = 0.001371, B13 = 0.2238 (M2) | bloque «Cómo se escribe» (σ̂², nuevo) |
| `nsdiffs` seas/ocsb = 1/0 en log(AP) y `USAccDeaths` (M3) | **bloque R del M3 (líneas nuevas)** |
| 35 candidatos (M5) | la rejilla de 36 del JSON |
| Rango relativo 1.848; mediana 525.46 y `biasadj` 530.58 (M7) | **bloque R del M7 (líneas nuevas)** |
| RMSE 43.18 y 45.48 (M9) | **bloques R y Python del M9 (líneas nuevas)** |
| Parámetros totales 8, 9, 11, 14, 15, 16 (M10) | JSON (`fourier.resultados`); `r3_cifras.R` comprueba la suma |
| Tabla de la partición (8 × 3), 14.69/16.12, «más del doble», «cuarto con las tres»; sesgos | **bloque del M11 (nuevo)**; la tabla ordenable, de `exactas` (JSON) |
| 61 y 49 orígenes, 1954-12/1959-12, 16.81…41.24, 8.2…14.8 %, 14 y 12 orígenes, 26.00…28.30, 49.0 %, 18.22/15.96 | **bloque del M11 (nuevo)**; antes, nada (las de h = 24 y el mes 12 ni siquiera estaban en el JSON) |
| Crecimiento 3.4 %, 6.2–21.8 %, 4.7/6.9, 12.4/11.2, 9.4/12.8, 10.6/13.1; sesgo 39.45 = MAE | **bloque del M11 (nuevo)** |
| Salvedad de la armónica: K = 5, RMSE 19.58 | JSON (`armonica_K_sin_fuga`, de la R1) |

De lo que la R1 dejó para aquí, **sin bloque ni generador ya no queda nada**: el ARIMA(0,1,5) y el Q del M7 (M1), el 1.848 (M7),
σ₁₂/σ₁ = 2.22 frente a 3.46 (ya estaba en el bloque del M5 como 2.222 y 3.464) y todas las cifras del M11. `diag/lector_cifras.py`
sobre el capítulo nuevo (`r3_lector_cifras.out`): de los 64 grupos del diagnóstico, **15 siguen sin código** (eran 32 en `f807b40` y 25
en HEAD), **0 en el M11** (eran 6 en HEAD). De esos 15, 14 están en el JSON del generador, que la regla admite: las filas de
`USAccDeaths` y `co2` de la tabla del M1; las medias 0.032 y 0.201 y el 58 % de `lynx` (cap. 4) del M3; 0.343, −0.4412 y la fila
AR(1)×SMA(1) del M4; ψ∞ = 0.169 del Nilo (cap. 4) en el M5; las barras 3, 9 y 23 de los residuales y los t = −4.48 y −7.62 del M7; el
BIC, el β̂ = 1.1157 y la Pascua 2/10 del M9. Los dos que la herramienta marca «ni en el JSON» o del M7 (0.825) son falsos positivos de su
lista fija: el −0.4019 del M6 y el 0.825 del M7 ya no están en la prosa (la R1 los quitó) y el `nobs = 144` del M6 lo imprime su bloque
de Python. La salvedad 19.58 del M11 sale del JSON (`armonica_K_sin_fuga`). No quedan cifras de la prosa que no salgan de un bloque o
del generador.

## Lo que no se hizo, y por qué

| Qué | Por qué |
|---|---|
| La retro de la pregunta 1 del quiz dice «Cuatro evidencias independientes (Módulo 8)»; el deck, «cuatro evidencias coinciden» (título y nota de la l. 130) | El quiz y el deck están fuera de alcance. El M8 dice ahora tres evidencias en cuatro comprobaciones, que casa con el E3. Pregunta 1 |
| El deck escribe $n_t$ (`capitulo_5.md` l. 1011, 1100, 1103) | Fuera de alcance; el capítulo pasa a η_t. Pregunta 2 |
| Partir el M11 (sigue en 28 min y 2 394 palabras) | D7 lo descarta: renumera. Pregunta 3 |
| El M2 (21 min) y el M3 (21 min) siguen siendo largos; la subsección de momentos se queda | La decidió Javier (§7.6); el M2 ganó un párrafo de entrada y perdió tres repeticiones del satélite |
| El satélite repetido en M4 y M7 («Los satélites, comprobados», en una caja de definición que no define) | T3.2 pide el M2; queda anotado |
| «Python alcanza ese mismo óptimo desde varios puntos de partida» (M6) sin evidencia a la vista; el M4 sin identificación sobre datos ni PACF con cifras; STL + ARIMA sin cifras en el M10 | Contenido, no estructura; no están en D6–D8 |
| La nota del M11 que atribuye «dónde brilla / dónde falla» a las competencias M4 y M5 y su «lleva cinco capítulos enseñando a no hacer» | R4 (atribución). Solo se cambió la remisión al código |
| El simulacro: «cómo se despeja el *airline*», r₁₂ | Instrumento aplicado; fuera de alcance |

## Preguntas para el docente

1. **¿Tres o cuatro evidencias?** El M8 dice «cuatro comprobaciones, tres evidencias» (la 3.ª y la 4.ª miran el mismo Φ̂), como el
   E3. La retro de la pregunta 1 del quiz y el deck dicen «cuatro evidencias». ¿Se alinean en la R5 (quiz) y en el deck?
2. **η_t en el deck.** ¿Se cambia también allí el $n_t$ (tres líneas), con su verificador?
3. **El M11 en 28 min** (más 17 de autoevaluación) y el M2/M3 en 21. ¿Se acepta, o se piensa para 2027-I partir el M11 (comparación /
   cierre y práctica)?
4. **El simulador del M11 perdió el selector de métrica**, porque la tabla ordenable ya ordena por las tres; la lectura da el sesgo
   medio. ¿De acuerdo, o se prefiere quitar la tabla ordenable y dejar el selector?
5. **`exactas` en el JSON.** El libro de Excel sigue leyendo `rmse`, `mae` y `mape` a tres decimales (no se regeneró: no cambian). ¿Se
   le pasan también las exactas en su próximo rediseño?

---

## Guiones y comprobaciones

| Guion | Salida | Qué hace / resultado |
|---|---|---|
| `r3_edita.py` + `r3_ediciones_*.py` | — | reaplica sobre HEAD 61 sustituciones y 1 traslado; `--comprobar`: los siete archivos «idéntico a HEAD + ediciones» |
| `r3_minutos.py` | `r3_minutos_antes.out`, `r3_minutos_despues.out` | minutos medidos antes y después (tabla de arriba) |
| `r3_secciones_m11.py` | `r3_secciones_m11_antes.out`, `…_despues.out` | palabras por sección del M11 |
| `r3_cifras.R` | `r3_cifras.out` | **48 de 48** cifras recalculadas coinciden |
| `Rscript precalculo/genera_cap5.R` | `r3_genera_cap5.out`, `r3_compara_json.out` | 27 hojas nuevas; las 9 055 de antes idénticas salvo `generado`; `SERIES_CAP5` idéntico |
| `precalculo/verifica_bloques_cap6.py --html …` | `r3_verifica_bloques.out` | **1512 de 1512** cifras (antes 1335 de 1335); 17 bloques de R y 14 de Python (antes 16 y 13: un par R/Python nuevo, el del M11; en M1, M2, M3, M7 y M9 se añadieron líneas a los bloques que ya había); 0 con discrepancias; código 0. Tarda ~95 s (el bloque del M11, ~45) |
| `r3_bloques_python.py` (copia de `r1_`) | `r3_bloques_python.out` | los 14 bloques de Python, cada uno solo en una carpeta vacía: código 0, ningún `ConvergenceWarning`, 0 líneas `#>` sin su par. Los avisos que quedan (matmul en dos del M2, `InterpolationWarning` de KPSS en el M3) ya estaban en HEAD; el del M1 nuevo se filtra como los demás («solo avisos de coma flotante de numpy») |
| `precalculo/verifica_todo.py` | `r3_verifica_todo.out` | 11 verificadores en verde, Tailwind incluido (`compila_tailwind.py --comprobar`) |
| `verifica_cifras_cap5.py` (deck) | `r3_verifica_cifras_deck.out` | 774 de 774, 0 que no coinciden: ningún claim de tipo «capítulo» se rompió (el «$16.12$» de la tabla estática sigue en la prosa nueva) |
| `precalculo/audita_posicion_correcta.py` | `r3_audita_posicion.out` | en verde |
| `sin_literales_diagnostico.py` | `r3_sin_literales.out` | 0 coincidencias |
| `r3_revisa.js` | `r3_revisa.out` | por HTTP (servidor propio en 8765, Chrome sin ventana en 9278, cerrados al acabar), los 12 módulos a 1200 y 375 px con plegados abiertos: 0 errores o avisos de consola, 0 `.katex-error`, 0 «$» sin componer, 0 KaTeX en `<pre>`, ningún desbordamiento de página, todos los lienzos con gráfico, `typeof tailwind` = `undefined`; el orden de los h3; el último elemento de cada módulo; las intros y lecturas iniciales; la tabla ordenable (7 columnas, 8 filas, 16.12 y 76.99, orden por MAE); 0 selectores en el simulador del M11 y su lectura con los ocho y con ninguno; las pestañas R/Python del bloque nuevo (Prism aplicado). A 375 px la tabla ordenable se desplaza dentro de su marco (`overflow: auto`), sin ensanchar la página. 24 capturas en `capturas/r3/` |
| `ensambla_cap5.py` dos veces | — | md5 idéntico (`93ee838b…`); `ensambla_cap6.py` deja el cap. 6 igual a HEAD |

---

## Correcciones tras el verificador

Verificador independiente: `R3_verificacion.md` (2 Altos, 3 Medios, 10 Bajos). Todo se corrigió con las mismas reglas: las ediciones
están en las listas de `r3_edita.py` (ahora **78 sustituciones y 1 traslado** sobre HEAD, en nueve archivos; `--comprobar` en verde),
que gana dos listas: `r3_ediciones_deck.py` (la fuente del deck y un claim nuevo de su verificador, autorizados por la maestra) y las
correcciones del generador en `r3_ediciones_genera.py`. La columna «Lo que hizo la sesión maestra» de `R3_verificacion.md` dice, fila a
fila, «corregido por el redactor a petición de la maestra: …».

| # | Arreglo |
|---|---|
| V1 (Alto) | El `\t` de `\text` en el cierre del M6 era un tabulador: la cadena va cruda. **`r3_control.py`** barre (1) las listas de ediciones buscando cadenas no crudas con `\t`, `\n`, `\b`, `\f`, `\r`, `\v`, `\a` pegadas a letras y (2) el HTML ensamblado, las plantillas, `chapter.js` y la fuente del deck buscando caracteres de control y restos de comandos sin barra dentro de fórmulas («ext{», «rac{», «ar{», «abla», «heta», «imes»…), frente a HEAD: 0 y «igual» en todo (`r3_control.out`) |
| V2 (Alto) | El +1 de «Parámetros totales» es la **deriva**, no σ²: la frase lo dice y añade que σ² no se cuenta; `r3_cifras.R` ajusta los seis modelos y comprueba deriva y `length(coef)` |
| V3 | M8: «Cuatro comprobaciones de tres tipos… No son independientes: salen de los mismos 138 meses, y el Φ̂ del ajuste forzado mide casi lo mismo que ρ̂₁₂»; cabecera «Comprobación»; comentario del bloque. Retro de la pregunta 1 del quiz → «Las comprobaciones del Módulo 8…» (solo esa frase). Deck: título «…cuatro comprobaciones coinciden» (el ancla del verificador es el prefijo, no hubo que reanclar), nota del M1 y $n_t$ → $\eta_t$ en tres líneas |
| V4 | El bloque de R imprime los coeficientes del ARIMA(0,1,5) y sus tres primeros residuales; el de Python, los suyos: los coeficientes coinciden y lo que difiere son los residuales de arranque (4.7185 frente a 0.0047), y así lo dice el comentario |
| V5 | `genera_cap5.R` calcula también la armónica de los 61 orígenes con búsqueda exhaustiva (`origen_movil.armonica_exhaustiva`: 21.056 a h = 12, 28.251 a h = 24, 16.625 en el mes 12); la prosa, la fila de la tabla y el comentario del bloque dicen que en los orígenes se busca por pasos (por tiempo), que con la exhaustiva baja a **21.06** y queda por delante del ETS-log (21.42), y que el SARIMA sigue primero con las dos. La frase falsa con una de las dos búsquedas salió. `r3_cifras.R` recalcula el 21.06 aparte. **Deck**: la nota de «Con 61 orígenes, el SARIMA pasa de cuarto a primero» decía lo mismo; corregida, con un claim nuevo (J) para el 21.06. Ninguna cifra de la tabla ni del clímax cambia |
| V6 | M7: `biasadj` multiplica la mediana por 1 + σ_h²/2 (530.58, una aproximación); la media exacta es 530.61; el bloque de R calcula las dos y el comentario de Python explica su 530.52 por el σ² de máxima verosimilitud. **Para la ronda del cap. 6**: su nota dice que `biasadj` «le suma σ_h²/2 para dar la media»; no es así (multiplica por 1 + σ_h²/2 y da una aproximación) |
| V7 | «el código del capítulo, el simulacro y el Capítulo 3 la escriben $r_k$» |
| V8 | La intro del explorador pregunta qué modelos quedan a menos de 2 puntos de AICc y si alguno mejora el diagnóstico |
| V9 | La banda de 144 residuales, con los 13 de arranque nombrados y la de 131 (±0.171): la lectura no cambia (`r3_cifras.R`: −0.127, 0.115, 0.218) |
| V10 | Escala y k, detrás de las tres métricas |
| V11 | «La columna k cuenta los parámetros estimados, sin la varianza σ²…» |
| V12 | «…reproduce todo lo anterior salvo la salvedad del K de la armónica y su búsqueda exhaustiva»; la salvedad dice que la calcula el generador; «la tabla anterior» → «la tabla de la partición» |
| V13 | La frase del M9 dice qué no se repite en la misma posición (Semana Santa, febreros bisiestos, días hábiles) y por qué la cuarta fila no hace falta. **Para la R4/R5**: el β de los días se identifica solo con los febreros bisiestos |
| V14 | «El desarrollo de la sección siguiente…». Lo demás de V14 queda: el satélite pasó de cuatro explicaciones a dos con remisiones, no a una (T3.2 en parte) |
| V15 | «Naïve estacional» en el generador y «Naïve est.» en la leyenda corta |

Dos tropiezos de esta pasada, ya resueltos: `ensambla_cap5.py` exige que «genera_cap5.R» aparezca una sola vez en la página (la
prosa nueva decía «el generador de los datos del capítulo» con el nombre del archivo; ahora sin él), y la nota nueva del deck traía
una cifra sin claim (el verificador lo marcó «pendiente» hasta añadirlo).

**Verificadores tras las correcciones** (sustituyen a los de la tabla «Guiones y comprobaciones» de arriba): `r3_edita.py
--comprobar` «idéntico a HEAD + ediciones» en los nueve archivos; reensamblado reproducible (md5 `c6f5af6b…` dos veces) y cap. 6
idéntico a HEAD; `r3_control.py` en orden; `verifica_todo.py` 11 en verde y `compila_tailwind.py --comprobar` código 0; bloques del
cap. 5 **1536 de 1536**, código 0; los 14 bloques de Python sueltos con código 0 y ningún `ConvergenceWarning`; `r3_cifras.R` **66 de
66**; deck reconstruido con `construir.py` (cambian solo las líneas tocadas), `verifica_cifras_cap5.py` **775 de 775** («todo verificado
y cubierto») y `revisar.py` 84 láminas, todas a escala ≥ 88 %; `audita_posicion_correcta.py` y `sin_literales_diagnostico.py` (0) en
verde; minutos con distancia máxima 0.5 (M9 y M11 declaran ahora 10 y 28); `r3_revisa.js` por HTTP a 1200 y 375 px: «TODO EN ORDEN»,
sin errores de consola, servidores cerrados. JSON: 34 hojas nuevas y dos distintas (`generado` y el nombre «Naïve estacional»).

## Comprobación de la sesión maestra

- `r3_edita.py --comprobar`: idéntico; 78 sustituciones y 1 traslado sobre HEAD.
- Reensamblado reproducible: md5 `c6f5af6b…` dos veces. El cap. 6 y `simulacro.js` quedan intactos.
- Sin tabuladores en el HTML ni restos de `\text`.
- El quiz cambia solo en la retro autorizada de la pregunta 1; el `opciones` que desaparece de `chapter.js` es el del
  selector de métrica del simulador del M11.
- Verificadores:
  - `verifica_todo.py`: 11 en verde.
  - `compila_tailwind.py --comprobar`: código 0.
  - Bloques del cap. 5: 1536/1536, código 0.
  - Deck: 775/775.
  - `audita_posicion_correcta.py`: verde.
  - `sin_literales_diagnostico.py`: 0.

  Las salidas están en `r3_maestra_*.out`.
- El 21.06 frente a 21.42 de la búsqueda exhaustiva lo midieron dos agentes por separado (el verificador y el generador).
- **Para la R1 del cap. 6:** el cap. 6 dice que `biasadj` «suma σ²/2», y es inexacto (V6).
- **Para la R5:** el β de los días del M9 depende de los febreros bisiestos (V13).
