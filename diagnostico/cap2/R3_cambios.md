# Capítulo 2 · ronda R3 («estructura») · cambios

Ronda R3 del `PLAN_Mejora_Cap2.md` (tareas T3.1–T3.4; decisiones D5, D6 y D7), más las promesas incumplidas y la
pista de las tablas que dejó pendiente la R2. Fecha: 2026-11-17. Un solo redactor; sin commit. Especificación:
`diagnostico/cap2/lector_estudiante.md`, leída contra el archivo tal como lo dejaron la R1 y la R2 (`cda761c`).

**Archivos tocados**

| archivo | qué |
|---|---|
| `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` | 491 líneas más, 155 menos. Contenido en los nueve `<template id="module-N">`; los minutos de `courseData.modules`; y **armazón**: 22 líneas de CSS y 18 de JavaScript para la pista de las tablas |
| `Htmls_Series/capitulo-{3,4,5,6}-*.html` | 40 líneas más cada uno, ninguna menos: solo el armazón de la pista, llegado por reensamblado (`ensambla_cap3.py --escribir` y los tres siguientes) |
| `diagnostico/cap2/comprobaciones/r3_*` | guiones y salidas de la ronda |
| `diagnostico/cap2/capturas/r3/` | diez capturas de la pista (ignoradas por git) |

No se tocaron `AUTOEVALUACIONES['cap2']`, `DATOS_CAP2`, los simuladores, la portada ni la plantilla. No se añadió
ningún `<cite>`, ningún `data-afirma`, ningún autor, año ni sección. No hay clases nuevas de Tailwind.

**Cómo se editó.** Cada cambio es una sustitución exacta que debe aparecer una sola vez
(`r3_edita.py` + `r3_ediciones_*.py`, una lista por módulo): quedan como registro literal de qué texto salió y cuál
entró. No son reejecutables (la segunda vez el texto de partida ya no está), y eso es deliberado.

**Verificadores al cerrar** (segunda pasada, posterior a la última edición)

Ver la sección «Comprobaciones finales», al final.

Las líneas «ahora» son las del archivo tras la ronda.

---

## T3.1 · Definir antes de usar (D7)

Barrido propio sobre la tabla «Lo que se usa antes de definirse» del lector, más lo que apareció al releer.

| Término | Primer uso | Qué se hizo | Ahora |
|---|---|---|---|
| ruido blanco, caminata aleatoria | M1, simulador y tabla | Párrafo antes del simulador: las dos se dicen en una línea y se remiten a los Módulos 2 y 5. `AirPassengers` se presenta (miles de pasajeros de aerolíneas internacionales por mes, 1949–1960; leído en la ayuda de R) | 2338 |
| `Var(y_t) = tσ²` y por qué falla la condición 3 | M1, tabla | La celda remite al M5 y dice por qué falla la (3): la covarianza entre dos instantes crece con la varianza | tabla del M1 |
| correlograma, banda, `r_k` | M2, simulador y nota | Párrafo antes del simulador: qué es cada barra, qué son las dos líneas, y que el M3 lo define | 2450 |
| «diferenciar», `∇`, «raíz unitaria» | M3, tabla (fila 2) | Párrafo «Tres avisos sobre la tabla»: diferenciar es restar a cada valor el anterior, `∇y_t = y_t − y_{t−1}`, y el M7 lo desarrolla; raíz unitaria, adelanto del M5 | 2655 |
| `ρ_k` definido para una serie estacionaria y leído sobre dos que no lo son | M3 | Tercer aviso del mismo párrafo: en una caminata o en `AirPassengers` las `r_k` no estiman ninguna cantidad fija; el correlograma se lee como huella | 2655 |
| TRM | M4, explorador | Párrafo antes del explorador: qué es, unidad (pesos por dólar), periodo (enero de 2015 a junio de 2026, 138 meses), de dónde sale (promedio mensual de la serie diaria de datos.gov.co). Sin cita: es de la R4. El M6 ya no la presenta: remite al M4 | 2857 · M6 |
| `∇` y `∇₁₂` delante de un nombre; `log(AirPassengers)`; `ndiffs`, `nsdiffs` | M4, selector y lectura del explorador | El mismo párrafo: `∇` remite al M3, `∇₁₂` se dice (`y_t − y_{t−12}`) y remite al M7, el logaritmo remite al Capítulo 1 («cerró el abanico», su M4) y al M8, y las dos funciones se dicen en una línea con remisión al M7 | 2857 |
| AR(1) | M3 (tabla), M4 (anticipo), quiz | El M5 nombra ahora el proceso: «autorregresivo de primer orden, o **AR(1)**» | apertura del M5 |
| «primera diferencia» | M5, simulador | La intro del simulador la dice (`∇y_t = y_t − y_{t−1}`, del M3) | M5 |
| operador `B`, raíz fuera del círculo | M5, definición | Se añadió que el Capítulo 3 vuelve sobre los dos. La definición no se desplegó: el lector la marca como juicio (O) y el capítulo 3 la explica con calma | M5 |
| `∇` y `γ` en la regresión del ADF | M6 | Ver T3.4 | 3211 |
| `log(AirPassengers)` en el M6 y el M7 | M6 | El M6 dice por qué se usa (la amplitud crece con el nivel; Capítulo 1 y M8) y el M8 lo recoge («es la razón por la que los Módulos 6 y 7 trabajaron con `log(AirPassengers)`») | M6 · apertura del M8 |
| «diferencia estacional» | M6, regla de trabajo | La regla de trabajo ya no la explica: remite a la regla del orden del M7 | 3426 |
| MA(1), `θ`, «no invertible» | M7, recuadro de sobrediferenciación | Párrafo propio, rotulado **«Adelanto del Capítulo 3»**. El `−0.5` ya no depende de ese vocabulario: sale de la cuenta (covarianza `−σ²`, varianza `2σ²`) en el párrafo anterior | 3837 |
| ARIMA(0,1,1) en el código | M7, ejemplo (b) | El comentario del bloque dice que es un modelo del Capítulo 4 (lo anotó la R1 para esta ronda) | bloque R del M7 |
| `d` y `D` | M7, M9 | Definidos en la caja del operador de diferencia («en todo el curso…») y recordados en el paso 6 del M9 | M7 · M9 |
| Ljung–Box | M9, ejercicio 3 | Nombrado y dicho en una línea en el M3 (resume todas las barras en un p-valor; lo define el Capítulo 3). El ejercicio no se tocó: es de la R5 | 2664 |
| «pronóstico ingenuo» | M5 | **No tocado**: ya lo define el paréntesis («mañana será como hoy») | — |
| «semidefinida positiva» | M3, nota del divisor | **No tocado**: el lector lo marca como juicio (O) y la nota es correcta; desplegarla es más prosa en un pasaje secundario | — |

## T3.2 · Una sola regla para el orden de las diferencias (D5)

- **La regla se escribe una vez, en el M7** (caja «Regla del orden: la diferencia estacional, primero», 3606): cuatro
  pasos (transformar; `nsdiffs()` y `∇_m`; `ndiffs()` **sobre lo que dejó el paso anterior** y `∇`; comprobar), qué
  hace cada función y por qué el orden importa. Sustituye a la advertencia «El orden no da lo mismo en la
  práctica».
- **Las dos razones.** (1) A veces con la estacional basta —la frase y su atribución a FPP3 son las que ya estaban,
  sin añadirle nada—, y se da la explicación algebraica, en voz propia: `1 − B^m = (1 − B)(1 + B + … + B^{m−1})`,
  la diferencia estacional ya lleva dentro una regular. (2) Las pruebas de raíz unitaria regular no son fiables
  sobre una serie todavía estacional (M6).
- **Lo que dice la caja del software, leído en esta sesión en el código de `forecast` 9.0.2** (`r3_explora.out`
  y la sesión): `ndiffs()` repite el KPSS mientras rechaza; `nsdiffs()` por defecto (`test = "seas"`) calcula
  `1 − Var(R)/Var(S + R)` sobre una STL —el `F_S` del Capítulo 1— y pide la diferencia si pasa de 0.64.
- **El caso en que el orden cambia la cuenta, que el capítulo no tenía.** Sección «El orden, en dos series» (3848,
  antes «Diferenciación estacional en la práctica»). En `log(AirPassengers)` los dos órdenes llegan a `d = 1`,
  `D = 1` (se dice: «aquí se llega al mismo sitio»). En `log(UKgas)` (trimestral, 108 datos; la serie es del
  Capítulo 1) no: con la regla, `D = 1`, `d = 0`, 104 observaciones y `r₁ = −0.178`; preguntando primero por la
  regular, `d = 1`, `D = 1`, 103 observaciones y `r₁ = −0.576`, el indicio de sobrediferenciación del recuadro.
  Tabla nueva de cinco filas; el bloque de R lo calcula bajo `#>`.
  - La serie no se eligió mirando el resultado deseado sin más: `r3_explora.R` §5 y §8 recorre 21 series de R y de
    `forecast`. El orden cambia la cuenta en cinco: `USAccDeaths` (en el otro sentido: `ndiffs` da 0 sobre la serie
    cruda y 1 tras `∇₁₂`), que se dejó para el ejercicio 3, y `UKDriverDeaths`, `woolyrnq`, `log(JohnsonJohnson)` y
    `log(UKgas)`. Se tomó `log(UKgas)` por ser la más limpia (tras `∇₄`, 1 de 8 rezagos fuera de la banda y KPSS
    lejos del umbral con los dos truncamientos) y porque el Capítulo 1 ya la usa.
- **El M6 cita.** La «Regla de trabajo» (3426) dice lo que es del M6 (ni ADF ni KPSS sobre la serie estacional
  cruda) y remite a la regla del M7 para el orden completo. Ya no promete que `ndiffs()` y `nsdiffs()` automaticen
  nada.
- **El M9 cita.** La apertura dice que los pasos 2 a 4 son la regla del M7. El paso 3 ya no dice «es la trampa del
  orden del Módulo 7»: dice «es la regla del orden del Módulo 7» y da la razón que el M7 ahora sí muestra, con
  `log(UKgas)`. El pipeline lleva la remisión en un comentario.
- **La varianza no se reintrodujo.** No aparece en la regla, en el caso nuevo ni en el pipeline (del que se quitó
  `var_final`, ver T3.3). El recuadro del KPSS del M7 no se tocó.
- **La nota del costo** («el costo es absoluto») enlazaba con «la advertencia anterior», que ya no existe: enlaza con
  la regla («una diferencia que se ahorra son datos que se conservan»).

## T3.3 · Pipeline del M9 con logaritmo (D6)

- **R.** `preparar(y, logaritmo = TRUE, m = frequency(y))` (4391). El umbral `abs(lambda) < 0.25` **se retiró**: no
  salía del M8 y hacía que `AirPassengers` (λ = −0.2947) tomara Box–Cox. Que se transforme o no lo decide quien
  mira el gráfico (paso 1), y entra como argumento; así el ejercicio 1 (`co2`, «se trabaja sin transformar») es
  `logaritmo = FALSE` y no contradice al pipeline. El λ de Guerrero se sigue calculando, fuera de la función y con
  su comentario: se anota para comparar y no decide.
- **Python.** La misma firma (4456). Ya usaba el logaritmo; se le quitó el comentario que explicaba por qué su
  varianza no coincidía con la de R, que dejó de ser cierto: ahora las dos versiones dan la misma serie.
- **Numeración.** Los comentarios del código dicen «Paso 2 … Paso 5», como el componente de pestañas, y una
  cabecera dice dónde están el 1 y el 6 (el lector: «el código numera cuatro pasos y el componente seis»).
- **`var_final` salió de las dos versiones.** Era el resto de la regla de la varianza. En su lugar el bloque
  imprime lo que el cierre del capítulo usa: `r₁` y `r₁₂` de la serie final y cuántos de 24 rezagos salen de la
  banda.
- **Salidas rehechas** (copiadas de la ejecución, `r3_bloques_publicados.out`):

  | | antes | ahora |
  |---|---|---|
  | R: `d`, `D` | 1, 1 | 1, 1 |
  | R: λ | −0.2947 (decidía Box–Cox) | −0.2947 (solo se anota) |
  | R: varianza final | 9.17e-05, en escala Box–Cox | — (retirada) |
  | R: p del KPSS, `n` | 0.1, 131 | 0.1, 131 |
  | R: `r₁`, `r₁₂`, fuera de la banda | — | −0.341, −0.387, 5 |
  | Python | `1 1 0.0021 0.1` | `1 1 0.1 131`, `[-0.341 -0.387]`, `5` |

- **Componente de pestañas.** Paso 2: el logaritmo como práctica y cuándo no se transforma («si el nivel apenas
  cambia de escala…»), que era el criterio que el ejercicio 1 aplicaba sin que el módulo lo dijera; «Con qué»
  empieza por `log(y)`. «Abombado» y «abombamiento» pasan a «la amplitud sigue creciendo con el nivel» (el
  tercer nombre para el abanico); «período» pasa a «periodo estacional». Las etiquetas en segunda persona («Qué
  haces», «Qué te devuelve atrás») no se tocaron: los textos del componente están fuera del alcance de la revisión
  de voz.
- **Resumen.** De 7 filas a 13. Entran: la banda; **ADF y KPSS con sus nulas contrarias**; **el ADF con
  estacionalidad**; la regla del orden; la sobrediferenciación; el pipeline. La fila «Raíz unitaria» ya no tiene
  las dos pruebas como «En R»; «Diferenciación» incluye `∇_m` y el costo; «Box–Cox» dice que en la práctica se usa
  el logaritmo.
- **Cierre.** «Lo que sigue: de la serie estacionaria al modelo» (4962), tras los ejercicios y antes de las
  lecturas, donde lo tiene el Capítulo 1. Dos párrafos: la serie del pipeline no es ruido blanco (las tres cifras
  de arriba) y qué cuatro piezas vuelven en el Capítulo 3. Lo que afirma del 3 y del 5 se leyó en esos archivos:
  Ljung–Box se define en el M8 del 3; la TRM vuelve en su M9 («Dos casos reales») como log-retornos; el 5 estima
  el *airline* sobre `log(AirPassengers)`.

## T3.4 · M6 y carga

- **Sobre qué serie se calcula cada cifra.** El −7.32 es de `AirPassengers` **sin transformar** (lo dice la frase
  que lo presenta, 3337, y de nuevo la primera evidencia: «sobre la misma serie sin transformar»). La tabla de `k`
  es de **`log(AirPassengers)`**: lo dicen la frase que la introduce —con el porqué del logaritmo— y, a la vista,
  la cabecera de su columna («ADF de `log(AirPassengers)`»; antes solo lo decía el `caption` oculto). La segunda
  evidencia dice «esa serie en logaritmos». El −6.42 de la tabla se contrapone expresamente al −7.32.
- **`γ` y `k`.** Párrafo nuevo en la definición del ADF (3211): `γ` no es la autocovarianza `γ_k` de los M1 y M3
  sino el coeficiente de `y_{t−1}`, y vale `φ − 1` (se resta `y_{t−1}` en los dos lados del proceso del M5); `k` es
  el número de términos aumentados —el argumento `k` de `adf.test()`—, no el rezago de un correlograma, «y en todo
  este módulo significa eso». **No se renombró ninguna de las dos**: `γ` es también la letra del ADF en el capítulo
  4 (l. 3237 de ese archivo) y `k` es el nombre del argumento en R; cambiarlas aquí habría abierto otra
  discrepancia.
- **«Ciclo» por «periodo estacional»** en el M6 (prosa y comentario del código) y en la definición de `∇_m` del M7.
  «Estacionaria en tendencia» queda nombrada en la definición del ADF. «Amplitud creciente» del Monte Carlo pasa
  a «amplitud `A` fija, probando amplitudes cada vez mayores: 0, 0.5, 1, 2 y 4» (las cinco de `DATOS_CAP2`).
- **Minutos.** Ver la tabla de más abajo. La portada no muestra la duración del capítulo (ni la de ninguno), así
  que `index.html` no se tocó; `cuenta_sitio.py` sigue en verde.

## Promesas

| # del lector | Promesa | Qué se hizo |
|---|---|---|
| 1 | Cap. 1: «el Capítulo 2 vuelve sobre el residuo con la autocorrelación» / «una manera de comprobarlo» | **Cumplida.** Sección nueva en el M3, «El residuo del Capítulo 1, ahora con número» (2664): el residuo de la descomposición clásica multiplicativa de `AirPassengers` (132 valores) tiene `r₁ = 0.403`, `r₁₂ = 0.294` y 14 de 24 barras fuera de la banda ±0.171: no es ruido blanco. Se dice que la prueba formal (Ljung–Box) es del Capítulo 3. En el código, en R y en Python (statsmodels da las mismas cifras) |
| 2, 3, 9 | Ya cumplidas | — |
| 4 | Objetivo del M4: «usar las dos juntas como instrumento de identificación» | **Reformulada y cumplida en un caso.** El objetivo dice «leer las dos juntas en un primer caso: es el instrumento de identificación que desarrolla el Capítulo 3». El caso (2908): la serie de memoria corta del M3 tiene ACF que decae (0.474, 0.235, 0.106) y PACF que se corta tras el rezago 1 (0.474; 0.014; −0.014; 0.033), con el rezago 9 asomando por azar. En el bloque de R. Además se lee la PACF de `AirPassengers`, la serie con que abre el explorador (seis barras fuera, nada que identificar todavía). **No** se añadió una serie AR al explorador: es tocar el simulador y sus datos |
| 5 | M5: distinguir tendencia determinista de estocástica es «el trabajo de las pruebas del Módulo 6» | **Cumplida.** Párrafo nuevo en el M6 (3321): con las dos pruebas en su variante de tendencia, la nula del ADF es la tendencia estocástica y la del KPSS, la determinista. TRM: el ADF no rechaza y el KPSS de tendencia rechaza (cifras que ya estaban). Una recta con ruido de 138 valores, simulada en el bloque de R: el ADF rechaza (−5.744, p < 0.01) y el KPSS de tendencia no (0.052, p > 0.10). La semilla es la 1, la primera; las cinco siguientes dan el mismo veredicto (`r3_cifras.out`). La frase del M5 dice ahora que allí «se aplican a un caso de cada clase» |
| 6 | «`ndiffs()` y `nsdiffs()` automatizan ese orden» | Ya corregida en la R1; ahora la frase vive en la regla del M7 («cada una decide una sola clase de diferencia: el orden lo pone quien las usa») |
| 7 | El `length()` «en el código de más abajo» | Ya cumplida en la R1: el bloque de R del M7 imprime `length(dd)` → 131. Comprobado |
| 8 | M9: «es la trampa del orden del Módulo 7» | **Reformulada y respaldada**: ver T3.2 |
| 10 | Pista del ejercicio 3: «la caja de advertencia del Módulo 7» | La R1 la cambió a «la Regla de trabajo del Módulo 6»; ahora dice **«la regla del orden del Módulo 7»**, que existe, es una sola y dice lo que la pista necesita. No regala el resultado: el caso del M7 es `log(UKgas)`, no `USAccDeaths` |
| 11 | «Seis preguntas» | Ya corregida en la R1 |
| 12 | Tarjeta de la portada: «y por qué pueden contradecirse» | **Cumplida en el capítulo; la tarjeta no se tocó.** `AirPassengers` sin transformar es el caso (3337): el ADF rechaza la raíz unitaria (−7.32) y el KPSS de nivel rechaza la estacionariedad (2.739, p < 0.01). Es la cuarta fila de la tabla de combinaciones, que ahora remite a él. Con el KPSS de tendencia la contradicción desaparece (0.096, p > 0.10) y queda un acuerdo falso, que es lo que el resto del pasaje explica. Las dos cifras nuevas están en el bloque de R |

## Hilo: lo demás del lector, uno por uno

| Dónde | Hallazgo | Estado |
|---|---|---|
| Arco | M3 → M4 y M4 → M5 sin puente | **Hecho.** El M4 abre desde el correlograma del M3 («tiene un punto ciego»); el M5, desde lo que falta («enseñaron a leer la dependencia; falta un proceso que la produzca») |
| Arco | M5–M8 terminan en un bloque de código | **Hecho.** Una frase de cierre tras el código en cada uno, que deja planteado el módulo siguiente |
| Arco | El capítulo no se despide | **Hecho** (T3.3) |
| Arco | El orden de los módulos es el inverso del orden del procedimiento | **No tocado**: no se renumera. Lo palía que la regla del orden esté ahora en el M7 y que el M6 y el M9 la citen |
| M1 | Dos definiciones antes de la primera imagen | **No tocado** (O): mover la figura delante de las definiciones rehace el módulo |
| M1 | «estacionalidad ≠ estacionariedad» dicho y no mostrado | **No tocado** (O): pide una serie nueva en el simulador |
| M2 | El aviso de incorrelación va antes del simulador | **No tocado**: la nota de la banda, que la R1 reescribió, remite a «la advertencia de arriba» |
| M2 | «El ladrillo de todos los modelos», afirmado en una línea | **En parte**: se dice dónde aparece el primero (M5) |
| M3 | Fila 4 de la tabla | Resuelto en la R1 |
| M3 | Regresión espuria y correlación cruzada, sin figura | **No tocado** (O) |
| M4 | La caja «Verificación» habla de cómo se construyó la página | **Hecho**: salió del cuerpo y entró, con el mismo texto y la misma cifra, al final del desarrollo plegado |
| M4 | El anticipo no se ve en ningún caso; nadie lee la PACF de `AirPassengers` | **Hecho** (promesa 4) |
| M5 | La raíz unitaria en cinco líneas | **En parte**: remisión al Capítulo 3 |
| M5 | El simulador no dibuja PACF | **No tocado**: es el simulador |
| M6 | «Estacionaria» cambia de sentido | **En parte**: «estacionaria en tendencia» queda nombrada; el párrafo de la R1 bajo la tabla sigue |
| M6 | La tabla de cuatro combinaciones, sin rehacer (lo dejó la R1) | **En parte**: la cuarta fila dice qué pasa («las dos rechazan: se contradicen») y remite a su caso. Las otras tres no se tocaron |
| M7 | «Las tres señales» son dos tríos | Resuelto en la R1 |
| M7 | La diferencia estacional es la menos mostrada | **En parte**: remisión al explorador del M4, que trae `∇₁₂∇ log(AirPassengers)`; y el caso de `log(UKgas)`. El simulador del M7 sigue diferenciando solo de forma regular |
| M7 | El recuadro de las dos funciones «KPSS» es la pasada más técnica | **No tocado**: la R1 lo corrigió y lo dejó vigilado por el código |
| M8 | La nota de las nueve cifras | **No tocado** (O) |
| M8 | La franja del 20 % y la recta en λ = 0 en el gráfico (pendiente de la R2) | **No tocado**: es el simulador, y no estaba en el encargo de esta ronda |
| M9 | El título del índice no menciona los ejercicios | **No tocado**: cambiar el título de un módulo es de Javier |
| M9 | La autoevaluación no toca M2, M4 ni M9; ejercicios 1 y 3 | **R5** |
| Vocabulario | «ciclo», «abombado», «período» | **Hecho** donde se dice arriba. «Ciclo» queda en el M9 solo para el bucle del pipeline |
| Vocabulario | `T` y `n`; «serie», «proceso», «realización»; cuatro nombres para el pipeline | **No tocado** |
| Voz | Primera persona del plural en M1–M8 | **Hecho en la prosa expositiva**: no queda ninguna forma en «-amos / -emos / -imos» dentro de los nueve módulos salvo un comentario de código («esperamos ~5 %»). Las intros de simuladores, el componente de pestañas, los avisos en imperativo y las soluciones siguen en segunda persona, como fija la convención |

## La pista de las tablas (pendiente de la R2)

- **Qué es.** Una tabla que se desplaza y todavía tiene columnas por enseñar **se desvanece hacia ese lado**: a la
  derecha al principio, a los dos lados a medio camino, a la izquierda al llegar al final. Es una máscara
  (`mask-image`, con su prefijo `-webkit-`) sobre la caja de la tabla; una sombra no servía porque las celdas tienen
  fondo y la tapan, que es por lo que la R2 lo dejó.
- **Cómo.** En tiempo de ejecución y **sin tocar el marcado de ningún capítulo**: `ajustarTablas()` llama a una
  función nueva, `avisarContinuacion(tabla)`, que pone o quita `tabla-sigue-der` y `tabla-sigue-izq`, y le
  engancha una sola vez un oyente de `scroll`. Vale para la tabla ancha (`tabla-ancha`) y, por debajo de 768 px,
  para cualquiera que no quepa. Las `.tabla-ranking` se siguen saltando: tienen su propio marco.
- **Es armazón**, así que se siguió el procedimiento de la cadena: `ensambla_cap3.py` mostró +40 / −0 líneas, se
  escribió, y lo mismo el 4, el 5 y el 6. Reensamblar dos veces da md5 idénticos; `r2b_sintaxis.py`, cinco «OK»
  (el nombre nuevo no existía en ningún capítulo).
- **Un fallo que se encontró y se corrigió antes de propagar.** La primera versión marcaba también tablas que no se
  desplazan: con bordes colapsados una tabla corriente da `scrollWidth > clientWidth`. Ahora solo avisa la que
  es un bloque desplazable (`r3_ediciones_armazon2.py`).
- **Medido** (`r3_tablas.js` → `r3_tablas.out`, Chrome sin ventana, por HTTP): los cinco capítulos, módulo a
  módulo, a 1200, 1024, 800 y 375 px. Por cada tabla que se desplaza se comprueba que lleva la pista, que la pierde
  al llegar al final y gana la del otro lado, y que al volver queda como estaba; y por cada una que no se desplaza,
  que no lleva nada. Cifras en «Comprobaciones finales». Capturas en `capturas/r3/`, una por capítulo a 800 y a
  375 px.
- **La plantilla no se tocó**, igual que en la R2: sigue un paso más lejos del capítulo 2.

## Minutos

`diagnostico/cap2/diag/cuenta_cap2.py` (el convenio de `diagnostico/cap1/comprobaciones/r5_minutos.py`), antes y
después: `r3_minutos_antes.out` y `r3_minutos_despues.out`. Se declara la columna «abierto» —leyendo también la
pista y la solución de cada ejercicio—, que es lo que declara el capítulo 1; no incluye el desarrollo plegado del M4
(2.0 min) ni la autoevaluación (8.6 min). `courseData` lleva el mismo comentario que el del capítulo 1.

| Mód. | Palabras antes → después | Medido antes | Medido después | Declarado antes → ahora | Distancia |
|---|---|---|---|---|---|
| M1 | 521 → 603 | 5.9 | 6.3 | 10 → **6** | 0.3 |
| M2 | 387 → 466 | 7.2 | 7.6 | 8 → **8** | 0.4 |
| M3 | 395 → 659 | 7.2 | 8.7 | 12 → **9** | 0.3 |
| M4 | 471 → 746 | 7.6 | 9.1 | 10 → **9** | 0.1 |
| M5 | 715 → 823 | 9.0 | 9.6 | 12 → **10** | 0.4 |
| M6 | 1 088 → 1 477 | 11.0 | 13.2 | 14 → **13** | 0.2 |
| M7 | 1 441 → 1 987 | 13.0 | 16.0 | 12 → **16** | 0.0 |
| M8 | 536 → 585 | 8.0 | 8.2 | 10 → **8** | 0.2 |
| M9 | 2 228 → 2 684 (abierto) | 24.4 | 26.9 | 10 → **27** | 0.1 |
| Total | | 93.2 | 105.7 | 98 → **106** | |

- La ronda **añade 12.5 minutos**: es el precio de definir antes de usar, de la regla con su caso y de cumplir
  cuatro promesas en lugar de retirarlas. Casi la mitad está en el M6 y el M7, que ya eran los más cargados.
- **El M7 queda en 16 min y es el módulo más largo de los ocho primeros.** Lleva la regla, la tabla de
  `log(UKgas)` y el adelanto del Capítulo 3, además de lo que le dejó la R1.
- **El M9 mide 27 min con las soluciones abiertas** (10.6 sin abrirlas) y, con la autoevaluación, unos 36. El
  reparto del módulo —cinco ejercicios con solución larga en el «cierre»— es de la R5 (D9 reparte práctica por
  módulos).

## Cifras nuevas y su evidencia

Todas salen de R (4.6.0; `forecast` 9.0.2, `tseries` 0.10.62) y están **en un bloque del capítulo bajo `#>`**, de
modo que el verificador de bloques las vigila, salvo las que se indican. `r3_cifras.R` → `r3_cifras.out` las
recalcula una por una con ocho cifras; `r3_explora.R` → `r3_explora.out` es la exploración de la que salieron.

| Dónde | Cifra en la prosa | Valor exacto | Bloque |
|---|---|---|---|
| M3 | residuo: n 132, banda ±0.171, `r₁` 0.403, `r₁₂` 0.294, 14 de 24 fuera | 132 · 0.17060 · 0.40338 · 0.29389 · 14 | M3, R y Python |
| M4 | PACF de la serie corta: 0.474, 0.014, −0.014, 0.033; fuera, el 1 y el 9 | 0.47400 · 0.01394 · −0.01397 · 0.03334 | M4, R |
| M4 | ACF de la serie corta: 0.474, 0.235, 0.106 | las imprimía ya el M3 | M3, R |
| M4 | PACF de `AirPassengers`: seis barras fuera | rezagos 1, 2, 9, 10, 11, 13 | **no** (sale de `DATOS_CAP2`; es lo que marca la lectura del explorador) |
| M6 | recta: ADF −5.744; KPSS de tendencia 0.052 | −5.74409 · 0.051544 | M6, R |
| M6 | `AirPassengers`: KPSS de nivel 2.739; de tendencia 0.096 | 2.73947 · 0.096150 | M6, R |
| M7 | `log(UKgas)`: 1, 0 / 1, 1; 104 y 103; `r₁` −0.178 y −0.576 | −0.17825 · −0.57596 | M7, R |
| M7 | `UKgas`: trimestral, 1960–1986, 108 datos | leído en la ayuda de R y comprobado | — |
| M7 | umbral 0.64 de `nsdiffs()` | leído en `body(nsdiffs)` | — |
| M9 | serie final: `r₁` −0.341, `r₁₂` −0.387, 5 de 24 fuera; n 131 | −0.34112 · −0.38661 | M9, R y Python |

El 2.739 del KPSS de nivel se redondeó desde el valor exacto (2.73947) y no desde la salida de R (2.7395, que daría
2.740): es el doble redondeo que la R1 encontró en cinco cifras.

## Lo que se encontró de nuevo

1. **El caso tramposo del M6 era, sin decirlo, el único caso del capítulo en que ADF y KPSS se contradicen**, y con
   el KPSS de tendencia las dos pruebas *coinciden* en el diagnóstico equivocado (0.096, p > 0.10: no rechaza).
   La prosa lo dice ahora. El mecanismo por el que el KPSS de tendencia no rechaza con la estacionalidad dentro
   **no se explica**: solo se muestra que al desestacionalizar pasa a rechazar (0.386, que ya estaba). Explicarlo
   exigiría una afirmación sobre el estimador de la varianza de largo plazo que no se comprobó.
2. **La razón de fondo de «estacional primero» no estaba en el capítulo**: `∇_m` contiene a `∇`. Es una identidad y
   se comprobó numéricamente (`r3_cifras.out`: diferencia máxima 0). **La R4 debe declararla `propia` o darle
   fuente**, y contrastar la frase de FPP3, que se conservó tal como estaba.
3. **`ndiffs()` sobre la serie cruda no «falla» en `log(UKgas)`**: devuelve 1 y hay una raíz unitaria; lo que
   ocurre es que `∇₄` ya se la lleva. Por eso la prosa no dice que esa primera respuesta fuera errónea, sino que
   preguntar primero por la regular acaba en una diferencia de más. En `USAccDeaths` (ejercicio 3) el mecanismo es
   el otro: la prueba sobre la serie cruda sí se equivoca.
4. **El residuo «sin forma» del Capítulo 1 no es ruido blanco** (14 de 24 barras fuera). El Capítulo 1 no afirma
   que lo sea, pero su M9 dice que «un residuo sin forma» tiene nombre, ruido blanco. Para la ronda que vuelva
   sobre el capítulo 1.
5. **El verificador de bloques deja `precalculo/serie.csv`** al correr sobre el capítulo 3. Se borró.
6. **El panel de vista previa mide mal cuando está oculto**: `requestAnimationFrame` no corre en una página en
   segundo plano y `ajustarTablas()` no se repasa al redimensionar. Las medidas de la ronda son de Chrome sin
   ventana.

## Para la sesión maestra

- **Los capítulos 3–6 cambian** (40 líneas cada uno) y hay que commitearlos con el 2. Su diff es solo el armazón de
  la pista.
- **La pista es un desvanecido, no un rótulo.** Si se prefiere un texto («desliza →»), hay que insertarlo desde
  `ajustarTablas()`; cambia la altura del módulo. `mask-image` sin prefijo existe desde Chrome 120; el prefijo cubre
  Safari y los Chrome anteriores.
- **M6: tres párrafos nuevos en el pasaje que el lector llamó «el que más obliga a releer».** Cumplen dos promesas
  (5 y 12) y dicen sobre qué serie va cada cifra, pero el módulo sube 2.2 min. Es lo que más conviene leer entero.
- **M7: la caja de la regla afirma dos cosas del software** (qué repite `ndiffs()`, el 0.64 de `nsdiffs()`) leídas
  en el código de `forecast` 9.0.2, sin cita. Para la R4.
- **`UKgas` entra en el capítulo 2** como segunda serie del orden. Su descripción sale de la ayuda de R; la fuente
  que esa ayuda nombra no se citó.
- **La pista del ejercicio 3** remite ahora al M7. Si la R5 rehace el ejercicio, que lo tenga presente.
- **El quiz no se tocó** y nada de lo cambiado lo contradice: se releyeron las ocho preguntas contra el texto nuevo.
  La P4 sigue usando «MA(1) no invertible», que ahora está marcado como adelanto.
- **Los capítulos 4 y 5** siguen hablando del mínimo de varianza (lo anotó la R1) y el 4 usa `γ` para el ADF sin la
  aclaración que ahora lleva el 2.

## Comprobaciones finales

Segunda pasada completa, posterior a la última edición del capítulo (tras el corte de red). Salidas en
`diagnostico/cap2/comprobaciones/`.

| Comprobación | Resultado | Salida |
|---|---|---|
| `python3 precalculo/verifica_todo.py` | **11 verificadores en verde** (Tailwind al día, capítulo 3 reproducible, cifras del sitio, posición de la correcta) | `r3_verifica_todo.out` |
| Verificador de bloques, capítulo 2 | **277 de 277, 0 discrepancias** (antes 226 de 226): 12 bloques de R y 9 de Python | `r3_bloques_cap2.out` |
| Cada línea `#>` del capítulo 2, literal en la salida de su bloque | **118 de 118** (antes 93) | `r3_bloques_publicados.out` |
| Verificador de bloques, capítulos 3 a 6 | 533/534 · 713/735 · 1199/1212 · 415/434: **igual que antes** | `r3_bloques_cap{3,4,5,6}.out` |
| Cadena | `ensambla_cap3.py` «reproducible byte a byte»; reensamblar 3–6 dos veces da **md5 idénticos** a los del árbol | `r3_cadena.out` |
| `r2b_sintaxis.py` | cinco «OK», ninguna declaración repetida | `r3_cadena.out` |
| `audita_posicion_correcta.py` | «Ningún instrumento concentra las correctas» | `r3_cadena.out` |
| `cuenta_sitio.py` | las cifras escritas coinciden con las contadas | `r3_cadena.out` |
| Los nueve módulos del capítulo 2, por HTTP (Chrome sin ventana, 1280 px) | 452 fórmulas, **0 errores de KaTeX, 0 `$` sin componer, 0 excepciones, 0 `console.error`** | `r3_render_katex.out` |
| Paridad de `$` | 0 elementos con `$` impar | — |
| Pista de las tablas, capítulos 2–6 a 1200, 1024, 800 y 375 px | **336 tablas × ancho; 169 se desplazan; pista incoherente en 0; cortadas por `<main>`, 0; errores de KaTeX, 0; eventos de consola, 0** (58 módulos × 4 anchos) | `r3_tablas.out`, `capturas/r3/` |
| Cada cifra nueva de la prosa, recalculada | coincide con lo publicado | `r3_cifras.out` |

`precalculo/serie.csv` se borró tras la última pasada del verificador de bloques. El servidor del puerto 8731 no
estaba en marcha al empezar: se arrancó con `preview_start` (`htmls-series`) y sigue arriba.

---

## Tras la verificación

Correcciones a los 18 problemas de `diagnostico/cap2/R3_verificacion.md` (5 a corregir, 13 menores). **Esta sección
manda sobre lo anterior** donde lo contradice: lo que arriba se dice de la caja de la regla del M7 («`ndiffs()` repite
el KPSS»), del cierre del M5, de la pista de las tablas (ancho fijo de 3.5rem, «+40 líneas» en los capítulos 3–6),
del paso 4 y del resumen del M9, y la tabla de minutos, describen textos y cifras que ya no son los del árbol.

Guiones: `r3b_ediciones.py` (17 sustituciones de contenido), `r3b_ediciones_armazon.py` y `r3b_ediciones_armazon2.py`
(la pista), `r3b_cifras.R` → `.out` (lo que respalda cada frase corregida; ninguna de esas cifras se publica),
`r3b_tablas.js` → `.out`, y las salidas de cierre `r3b_*.out`. Capturas en `capturas/r3b/`.

### Los cinco que había que corregir

| # | Qué pasaba | Qué quedó | Evidencia |
|---|---|---|---|
| 1 | M7, caja de la regla: `ndiffs()` «repite el KPSS del Módulo 6» | «La segunda repite una prueba KPSS —diferenciar, volver a probar— hasta que deja de rechazar o llega a dos diferencias, y devuelve cuántas hicieron falta. No es el `kpss.test()` del Módulo 6: usa la versión del paquete `urca`, con otro truncamiento de rezagos, y las dos pueden no coincidir, como muestra el recuadro del final de este módulo». La viñeta de «¿Cuántas diferencias?», que ya estaba, dice ahora «Es lo que hace `ndiffs()`, con su propia versión del KPSS» | `r3b_cifras.out` §1: `kpss_wrap <- function(..., use.lag = trunc(3 * sqrt(length(x))/13))`, `while (dodiff && d < max.d)`, `max.d = 2`; sobre ∇₁₂ log y, 0.3682 con 4 rezagos frente a 0.5367 con 2 |
| 2 | M5, cierre: «El Módulo 6 le pone un número» | «El Módulo 6 cambia el ojo por pruebas, que deciden con una regla y con un margen de error declarado. No vuelven fácil el caso difícil —con φ tan cerca de 1 y doscientos datos, lo habitual es que tampoco ellas lo separen de la raíz unitaria—, pero sí dicen cuándo la evidencia alcanza y cuándo no». **Sin cifras en la prosa**, así que no hizo falta bloque | `r3b_cifras.out` §2: en 1000 series AR(1) con φ = 0.95 y n = 200, el ADF rechaza la raíz unitaria en el 15.2 % y el KPSS de nivel rechaza la estacionariedad en el 72.8 % (el verificador midió 14.5 % con 400) |
| 3 | La pista de las tablas apagaba cifras que cabían casi enteras (34 de 169 casos) | El ancho del desvanecido ya no es fijo. `avisarContinuacion()` lo calcula y lo deja en `--sigue-der` y `--sigue-izq`: es **el menor de tres**: 3.5rem; lo que falta por enseñar hacia ese lado; y la distancia del borde al texto de celda más cercano que está **entero** a la vista. Así nunca apaga un texto que cabe, y si a la tabla le faltan 13 px se apagan 13 px. Ver «La pista, medida otra vez» | `r3b_tablas.out`; `capturas/r3b/c5-m12-t5-800.png` (la columna MAPE se lee), `c5-m7-t3-375.png`, `c4-m8-t1-800.png`, `c3-m8-t1-800.png` |
| 4 | M9, resumen: el ADF «rechaza la raíz unitaria sin motivo», como regla | «…**puede** rechazar la raíz unitaria sin motivo, tanto más cuanto más marcada es la estacionalidad» | `DATOS_CAP2`: 3.2 · 3.6 · 5.0 · 11.2 · 17.6 % con amplitud 0, 0.5, 1, 2 y 4 |
| 5 (7 del informe) | M9, paso 4: «∇ si queda tendencia» y «Comprobar si queda tendencia o raíz unitaria y aplicar ∇» | Botón: «∇ si queda raíz unitaria». Panel: «Comprobar si queda una raíz unitaria y, si queda, aplicar ∇. Una tendencia determinista —una recta con ruido— no se diferencia: se le resta la recta, y el Módulo 6 enseña a distinguir los dos casos» | lectura contra el párrafo del M6 y la advertencia del M5 |

### Los menores, uno por uno

| # del informe | Qué | Estado | Qué se hizo, o por qué no |
|---|---|---|---|
| 5 | M3: «por azar se esperaría una o dos» barras del residuo | **Corregido** | «Son demasiadas para el azar, incluso contando con que la media móvil con que se calcula ese residuo ya le deja algo de autocorrelación propia». `r3b_cifras.out` §5: en 1000 series multiplicativas con error i.i.d., el residuo de `decompose()` saca 2.68 barras de media, 6 en el percentil 95 y 11 como máximo; `AirPassengers`, 14 |
| 6 | M7: `nsdiffs()` y «el F_S del Capítulo 1» | **Corregido** | «…con la fórmula del F_S del Capítulo 1, calculada sobre su propia descomposición STL». `seas.heuristic(log AP)` = 0.964, frente al 0.937 del capítulo 1 |
| 8 | M9, cierre: la misma serie mandada al capítulo 3 y al 5 | **Corregido** | «…es dependencia que queda por describir, de un mes al siguiente y de un año al siguiente. El Capítulo 3 da las herramientas para la primera; el Capítulo 5 las extiende a la segunda y las aplica a esta serie» |
| 9 | M9, apertura: «los pasos 2 a 4 son la regla» | **Corregido** | «Los pasos 2 a 5 son la regla del orden del Módulo 7; el 1 y el 6 la rodean…: mirar antes y dejar constancia». Coincide con la cabecera del código |
| 10 | M7, Python: «(Modulo 9)» | **Corregido** | «primero la estacional (la regla de este modulo; el Modulo 9 la programa)» |
| 11 | M6: el KPSS de tendencia en el acuerdo falso, sin explicación | **En parte** | «Tres evidencias de que el problema es la estacionalidad y no otra cosa» (antes, «ese y no otro», que solo valía para el ADF), y en la segunda evidencia: el KPSS rechaza al desestacionalizar, «cosa que no hacía con la estacionalidad dentro: también al KPSS lo confundía la oscilación anual, aunque por un camino distinto del de los rezagos del ADF, que aquí no se desarrolla». `r3b_cifras.out` §11: 0.1127 (p > 0.10) en logaritmos y 0.3864 (p < 0.01) desestacionalizada. **El mecanismo sigue sin explicarse**: exige una afirmación sobre el estimador de la varianza de largo plazo que no se comprobó |
| 12 | La identidad 1 − Bᵐ y el r₁ = −0.341 de la serie final | **Corregido** | En el cierre del M9: «Ese r₁ negativo no es el rastro de una diferencia de más —las pruebas pedían las dos, y con ellas dejaron de pedir—». `r3b_cifras.out` §12 |
| 13 | M3: diferenciar «es el remedio de la segunda fila» | **Corregido** | «…cuando lo que hay es una raíz unitaria —una tendencia que es una recta fija se trata de otro modo, como explican los Módulos 5 y 6—». La fila de la tabla, que ya estaba, no se tocó |
| 14 | M8: «los Módulos 6 y 7 trabajaron con `log(AirPassengers)`» | **Corregido** | «la tabla de rezagos del Módulo 6 y todo el Módulo 7» |
| 15 | M4: nueve definiciones en un párrafo | **Corregido** | Una frase de entrada («para consultar mientras se mueve el selector») y cuatro viñetas, con el mismo texto |
| 16 | M7: «por eso la recomendación de FPP3…» | **Corregido** | Se quitó el «por eso»: la viñeta vuelve a la redacción que había («La recomendación de FPP3 es aplicar primero la diferencia estacional: a veces con ella basta…») y la identidad va después, como explicación propia. El último párrafo de la caja se partió en dos viñetas, como sugería el verificador. La atribución sigue sin cita: R4 |
| 17 | M9, cierre: sin enlace al capítulo 3 | **No tocado** | Es la convención del curso: ningún capítulo enlaza al siguiente desde su cierre |
| 18 | M7: `UKgas` ya salió en el capítulo 1 | **Corregido** | «`UKgas`, la serie de un ejercicio del Capítulo 1» (su M6, l. 4329 de ese archivo) |

### La pista, medida otra vez

`r3b_tablas.js` es `r3_tablas.js` con dos medidas más: el ancho del desvanecido de cada tabla y cuántos textos de
celda enteros a la vista quedan debajo, al principio, a mitad de recorrido y al final. Cinco capítulos, 58 módulos, a
1200, 1024, 800 y 375 px:

- 336 tablas × ancho; **169 se desplazan**; pista incoherente en 0; cortadas por `<main>`, 0; errores de KaTeX, 0;
  eventos de consola, 0.
- **Textos enteros bajo el desvanecido: 0** (antes, 34 casos según el verificador). Ningún desvanecido mide más que lo
  que falta por enseñar.
- Los cuatro casos que señaló el informe: cap. 5 M12 a 800 px, faltan 13 y se apagan 13 px; cap. 5 M7 a 375 px,
  faltan 5 y se apagan 3; cap. 4 M8 a 800 px, 19 y 13; cap. 3 M8 a 800 px, 19 y 1.
- **El precio.** El ancho mediano al principio es de 22 px (antes, 56 fijos), y en **38 de las 169** el desvanecido
  mide menos de 8 px aunque falten 8 o más por enseñar: son tablas en las que el borde cae justo entre dos columnas,
  sin texto cortado a la vista y sin hueco que apagar. Ahí la pista casi no se ve al principio (sí en cuanto se
  desplaza). Es la consecuencia directa de no apagar texto entero. Si se quiere una señal también en esos casos tiene
  que ser otra cosa que un desvanecido (una raya en el borde, un rótulo): no se hizo.
- La primera versión de esta corrección (`r3b_ediciones_armazon.py` sola) todavía apagaba la columna MAPE del cap. 5
  M12, porque sus cifras están cortadas por unos píxeles y no cuentan como «enteras»; por eso se añadió el tope de
  «lo que falta» (`r3b_ediciones_armazon2.py`).
- Cadena: los capítulos 3–6 llevan ahora **74 líneas más** cada uno respecto a `HEAD` (CSS y JavaScript de la
  pista), ninguna menos.

### Minutos, tras las correcciones

`r3b_minutos.out`. Lo declarado no cambia; la distancia mayor es 0.4 min.

| Mód. | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Medido | 6.3 | 7.6 | 8.9 | 9.2 | 9.8 | 13.4 | 16.3 | 8.3 | 27.4 | 107.2 |
| Declarado | 6 | 8 | 9 | 9 | 10 | 13 | 16 | 8 | 27 | 106 |

### Verificadores al cerrar esta pasada

| Comprobación | Resultado | Salida |
|---|---|---|
| `verifica_todo.py` | 11 verificadores en verde | `r3b_verifica_todo.out` |
| Bloques, capítulo 2 | 277 de 277, 0 discrepancias; 118 de 118 líneas `#>` literales | `r3b_bloques_cap2.out`, `r3b_bloques_publicados.out` |
| Bloques, capítulos 3–6 | 533/534 · 713/735 · 1199/1212 · 415/434, igual que antes | `r3b_bloques_cap{3..6}.out` |
| Cadena | capítulo 3 reproducible; reensamblar 3–6 dos veces, md5 idénticos | `r3b_cadena.out` |
| `r2b_sintaxis.py` | cinco «OK» | `r3b_cadena.out` |
| `audita_posicion_correcta.py` | ningún instrumento concentra las correctas | `r3b_cadena.out` |
| Nueve módulos por HTTP | 0 errores de KaTeX, 0 `$` sin componer, 0 excepciones, 0 `console.error` | `r3b_render_katex.out` |
| Pista de las tablas, cinco capítulos a cuatro anchos | ver arriba | `r3b_tablas.out` |

`precalculo/serie.csv` se borró tras la última pasada del verificador de bloques.
