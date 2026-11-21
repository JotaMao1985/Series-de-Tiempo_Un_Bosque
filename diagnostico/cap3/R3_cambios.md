# Capítulo 3 · ronda R3 («estructura») · cambios

Ronda R3 del `PLAN_Mejora_Cap3.md` (tareas T3.1–T3.3; decisiones D4, D6 y D7). Fecha: 2026-11-21. Un solo redactor; sin
commit. Especificación: `diagnostico/cap3/lector_estudiante.md`, leída contra el capítulo tal como lo dejaron la R1 y la R2
(`a5e7f58`); los pasajes se localizaron por su texto, no por la línea.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/cap3/cap3_modulos.html` | la fuente de los once módulos: +754 / −425 líneas |
| `ensamblado/cap3/cap3_js.js` | una línea: el pie de la tabla ordenable del Módulo 8 dice «el mismo $T$» (era `$n$`). Ningún simulador, ni `AUTOEVALUACIONES` ni el simulacro |
| `ensamblado/ensambla_cap3.py` | solo `courseData`: los minutos medidos, su comentario de convenio y el título del Módulo 10 |
| `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` | reensamblado (reproducible byte a byte) |
| `Htmls_Series/preparcial-corte-2.html` | **una línea**: el título del módulo 3.10 en `MODULOS_DEL_CORTE`. Esa tabla dice de sí misma «los títulos son los de la barra lateral de cada capítulo; si uno cambia allí, cambia aquí». No estaba en el encargo; si se prefiere dejarla como estaba, se revierte sola |
| `diagnostico/cap3/comprobaciones/r3_*` | guiones y salidas de la ronda |

Los capítulos 2 y 4 a 6 **no cambian**: se corrieron `ensambla_cap4.py`, `ensambla_cap5.py` y `ensambla_cap6.py` (escriben) tras
el 3 y `git diff --stat` no los muestra. No se tocó el armazón ni la plantilla. No se añadió ningún `<cite>`, ningún
`data-afirma`, ningún autor, año ni sección nuevos. No hay clases nuevas de Tailwind (`compila_tailwind.py --comprobar` en verde).

**Cómo se editó.** `r3_edita.py` más una lista por módulo (`r3_ediciones_m1.py` … `m10.py`, `r3_ediciones_minutos.py`): 80
sustituciones y 5 traslados, cada texto que sale y cada texto que entra, literales, y cada uno debe aparecer exactamente una
vez. **Es reejecutable**: siempre parte de `HEAD` (o de `--base`), no del archivo de trabajo; `--comprobar` verifica que el
árbol es `HEAD` + ediciones. La única excepción a la sustitución literal es el bloque de código del Módulo 9, que sale entero
(`entre()`, 214 líneas, quedan en `HEAD`) porque se parte en dos. El código nuevo está escrito sin escapar en las listas y pasa por
`html.escape`.

---

## T3.1 · Orden sin renumerar (D4)

Ningún módulo cambia de número ni de id.

| Módulo | Qué se hizo | Dónde |
|---|---|---|
| **M1** | Empieza por los polinomios y las raíces. **Los convenios de signo y las diferencias R/Python pasan a una sección al final** («Convenios de signo y diferencias entre R y Python»), con una frase en el sitio original que lo anuncia. El primer bloque ya no estima un ARMA(1,1): usa el MA(1) del Capítulo 2 (θ = +0.7), imprime solo ρ₁, r₁ y `ma1` (sin `s.e.`, ni verosimilitud, ni AIC), y el estimador se declara «del Módulo 7, por ahora solo importa su signo». El bloque de Python es autosuficiente (genera su propia serie, sin `serie.csv`) y ya no deja ningún archivo; el AR negado de `ArmaProcess` se muestra con el AR(1). «De contrabando» sale; «diferenciar es dividir por (1−B)» pasa a «multiplicar la serie por ese mismo factor» | h3 «Convenios…», último del módulo |
| **M2** | La PACF en el rezago p vale φ_p, dicho en el recuadro de la firma (y en el comentario del bloque: 0.3000 es φ₂). «El caso real del Módulo 9» (dos veces) pasa a «las manchas solares, que entran en el Módulo 7 y se cierran en el 9». «Los intervalos del Capítulo 6» pasa a «que deduce el Capítulo 4» (como dice el M4). ρ_k = 0 de la PACF pasa a φ_kk = 0. RB(0, σ²) se presenta | recuadros y párrafos citados |
| **M3** | «Invertible» se dice (y qué es: el único con que se reconstruye cada choque) en el párrafo anterior al simulador, no solo en el plegado. **θ = −1**: párrafo nuevo tras la definición de invertibilidad que conecta el MA(1) de la sobrediferenciación del Capítulo 2 con la frontera del simulador (ρ₁ = −0.5, raíz sobre el círculo), y su comprobación en los dos bloques. El ARMA se nombra al remitir al M4 | tras «Condición de invertibilidad» |
| **M4** | El ARMA se presenta en un párrafo al comienzo («lo define y estudia el Módulo 5; con q = 0 es el AR…»). **La recursión de ψ y π sale del plegado** (en prosa, con fórmulas, antes del ejemplo a mano que la usa). La guarda `if (j - i >= 0)` y los «ocho procesos… 6.7×10⁻¹⁶» salen (código y cifra que el lector no ve). **Las dos notas de los capítulos 4 a 6 pasan a una sección propia** («Para qué sirven los ψ en los capítulos siguientes»), tras el código y antes de «Dos ideas que hereda el Módulo 5»; el control `h` del simulador remite a ella | h3 nueva, penúltima |
| **M5** | **Orden: tabla → laboratorio → ciclo** (antes ciclo → tabla → … → laboratorio, 370 líneas más tarde). Cada traslado con una frase de enlace. El ciclo anuncia, en un párrafo, qué son AICc/BIC, Ljung–Box y `fitdf` («los desarrolla el Módulo 8»); Bartlett se explica en una frase (leída en el código de `statsmodels.tsa.stattools.acf`); el bloque de la redundancia anuncia que el AICc es del Módulo 8. γ₁ = 3.1765σ² y ρ₁ = 0.8308 salen del plegado (a la vista, con la aritmética). El título «Media, varianza y autocorrelación» (igual al del M2) pasa a «… y autocovarianzas» | tabla, laboratorio y ciclo |
| **M6** | Solo las promesas: «medir cuánto se separa» y «aquí lo cuantificamos» pasan a «ver» / «aquí se ve», porque el simulador muestra tres realizaciones y no calcula ninguna distancia | objetivo y párrafo del simulador |
| **M7** | El código ya no cita «el paso 6 del desarrollo»: lo que cita (CSS puede salirse de la región estacionaria, ML no, con T = 40 y φ = 0.95) se dice en un párrafo antes del plegado y el comentario del bloque dice lo que muestra | párrafo tras «Los tres métodos» |
| **M8** | El código ya no cita «el paso 4»: **el porqué de `fitdf` y el Monte Carlo (4.9 % frente a 2.6 %) pasan a un párrafo a la vista** tras la definición de Ljung–Box. El comentario de la rejilla ya no dice que «lo justifica la lectura de los correlogramas» (los once candidatos son una elección del capítulo) | párrafo tras la definición |
| **M9** | Ver T3.2 | |
| **M10** | Ver T3.3 | |

**`auto.arima`** se presenta en su primera aparición, que es el Módulo 9 (no está ni en el 5 ni en el 8): «del paquete `forecast`,
ajusta por sí sola varios modelos ARIMA y se queda con el de menor AICc (el Capítulo 4 detalla cómo busca)». Se comprobó en R
(`forecast` 9.0.2) que el criterio por defecto es `aicc`.

### Plegados y maquinaria que el lector no ve

| Dónde | Qué guardaba el plegado o qué citaba | Qué se hizo |
|---|---|---|
| M3 | por qué «invertible» | párrafo previo al simulador; el plegado no se toca |
| M4 | recursión de ψ y π | prosa a la vista; el plegado queda con la derivación |
| M5 | γ₀ y γ₁ del ARMA(1,1) | la cifra y la aritmética pasan al párrafo que las cita |
| M7 | «paso 6» | párrafo propio + comentario del bloque reescrito |
| M8 | «paso 4» | párrafo propio + comentario del bloque reescrito |
| M10 | «`precalculo/genera_soluciones.R`», «puedes contrastar las tuyas contra ellas» | «las cifras de cada solución salen de ejecutar el código que la acompaña» |
| M4 | «el precálculo en R», la guarda, los «ocho procesos» | se quitan (el último bloque de código del módulo hace la cuenta que sí se ve) |

---

## T3.2 · Módulo 9

**La elasticidad amplitud–nivel: se presenta, no se retira.** Decisión: el pivote del módulo es que los datos piden
transformar pero **no dicen cuál** (los tres intervalos excluyen b = 0 y se contradicen entre 0.5 y 1), y que lo decide el cero
de 1810. Sin saber qué es b̂ ese argumento no se entiende, y retirar la tabla quitaba la mitad de la honestidad del
paso. Se presenta en un párrafo (qué es: la pendiente de log(desviación) contra log(media) por bloques; qué dice b = 0, 1 y 0.5;
λ = 1 − b, que es lo que el criterio de Guerrero del Capítulo 2 hace implícito con s_i/ȳ_i^{1−λ}; y que es la pregunta del gráfico de
amplitud frente a nivel del Capítulo 1 con un número). La atribución «el mismo diagnóstico del Capítulo 1» sale. La tabla pasa
a tres decimales (0.816, 0.766, 0.703) para que coincida con lo que imprime el bloque, que la produce.

**Código partido por caso.** El bloque único de 214 líneas, al final del módulo, pasa a dos: el del caso 1 tras «Lo que sigue sin
estar bien» (una sección «El código del caso 1») y el del caso 2 al final. Cada uno corre solo (el del caso 2 repite
`library(forecast)` y `aicc()`). Por eso el módulo tiene dos grupos de pestañas.

**Cifras que no tenían código (todas salen de R, en un bloque, bajo `#>`)**

| Cifra de la prosa | Bloque |
|---|---|
| tabla de b̂ (3 tamaños de bloque; IC; R²) | `elasticidad()` en el caso 1 (R y Python); igual a la de `genera_cap3.R` (`all.equal`) |
| «en la serie completa 1700–1988 hay tres» ceros | `sum(sunspot.year == 0)` |
| rezagos de la PACF fuera de la banda, cruda (1, 2) y en raíz (1, 2, 6, 9, 16) con 0.200, 0.198, −0.199 | `fuera()` (R y Python) |
| la rejilla «exactamente la misma» sobre la raíz: 324.00, 325.35, 325.41, 327.42; BIC 334.00; LB(12); mínimo de AICc **y de BIC** = AR(2) | `compara()` con los once candidatos |
| errores estándar 0.0727 y 0.0724; σ̂² = 1.341; t = 19.31 y −9.46 (los cita el M10) | caso 1 |
| «con el λ de Guerrero 11.39 y p = 0.4892; sobre la desplazada 11.28 y 0.2216» | `ajusta()` |
| polinomio con el signo de φ₂ sin cambiar: raíces 0.5598 y −2.6066 | `polyroot(c(1, -phi[[1]], phi[[2]]))` |
| «la otra fórmula del periodo» 11.84 (11.8356) | una línea |
| PACF teórica del AR(2) final en 2 = −0.6853 (la cita el M10) | `ARMAacf(..., pacf = TRUE)` |
| ARMA(2,1) de la serie cruda: θ̂ = 0.3732, t = 2.78, raíz MA −2.6795, raíces AR 1.092 ± 0.7661i, módulo 1.3339 | `a21` |
| envolvente: R = 0.8278, 1/sin ω = 1.882, mitad cada 3.67 años, ceros en 5.61 | una línea |
| columnas de la tabla de ψ: Σψ², error estándar y semiancho de las 12 filas | `cumsum()`, `ee` |
| techo 5.62 y «a los seis años el 94 %» | `techo`, `fraccion_h6` |
| límites inferiores −0.209 y −0.114 en h = 7 y 8, y sus cuadrados 0.044 y 0.013 | `forecast(..., h = 8)` |
| asimetría de los residuales 0.791 → 0.573 y Shapiro–Wilk 0.0007 → 0.0470 | `asimetria()`, `shapiro.test()` (solo R: ver abajo) |
| rezagos de la TRM fuera de la banda (5 y 8: 0.193 y −0.198) | `acf()` (R y Python) |
| «ρ₁ ≈ 0.25 (0.249 con 21 días)» y «a 1.7 errores estándar por debajo» | pesos de los 21 choques (R y Python); 1.683 |

Ya tenían código y no se tocaron: la media de la TRM (0.2681, e.e. 0.3195, t = 0.84), los cuatro AICc con y sin media, el
`auto.arima` por defecto y exhaustivo, y Ljung–Box de r_t y r_t².

**Se quitó** del bloque el «comparación directa con la serie cruda» (`aicc(arima(...), 100)`, 838.3012, 834.7292, 323.9970,
325.4128): lo cubre la rejilla.

**Python**: se añadieron la elasticidad, los ceros, las PACF y las dos cifras de la TRM. **No** se añadió Python para la rejilla,
las variantes de λ ni la normalidad: statsmodels devuelve sin estandarizar los dos primeros residuales (lo dice el M8) y, medido, da
otra asimetría (0.962 frente a 0.791) y otro Shapiro (0.0001 frente a 0.0007). Un comentario al final del bloque lo dice.

**Otros arreglos del módulo.** (1) Una frase antes de la tabla de las dos columnas de AICc: cada columna se lee por separado
(la serie cruda y su raíz son datos distintos). (2) Una frase antes de la tabla de ψ: la fila j = 5 es el horizonte h = 6.
(3) `auto.arima()` se presenta (arriba). (4) «Donde sí hay estructura: en el cuadrado» **ya no existe**: el encabezado vigente
(«¿Y en el cuadrado? Aquí tampoco.») dice lo mismo que su texto; nada que hacer. (5) T en lugar de n para los 137 log-retornos.

---

## T3.3 · Módulo 10 en tres partes (D6)

| Parte | Contenido | |
|---|---|---|
| 1 · el puente y el material nuevo | «El AR es la idea original» (con el puente a la RNN), «Cuándo el modelo pequeño sigue ganando», el aviso del uso de asistentes, y **«Elegir el modelo y fijar sus órdenes»** (la tabla con PACF(p) = φ_p, «Qué confirma el orden elegido», el aviso del ARMA(2,2)), que antes iba tras el resumen | |
| 2 · el resumen | «Resumen del capítulo», **lo último antes de la evaluación** | |
| 3 · la evaluación | Autoevaluación, Ejercicios propuestos, Lecturas, la práctica de repaso y «Lo que viene» | |

Una frase al comienzo dice las tres partes. El objetivo las nombra. La frase «Esta la completa…» (cuyo antecedente era ambiguo) se
reescribe («La tabla de identificación del Módulo 5 … Esta nueva tabla la completa…»). PACF(p) = φ_p queda dicho en el M2 y la
fila del M10 remite a él (y el M9 ahora imprime el −0.6853).

**Un solo nombre: «Cierre: redes, resumen y evaluación».** Encabezado (`3.10 Cierre: redes, resumen y evaluación / Closing:
sequence models, summary & assessment`), `courseData` (el que ve la barra lateral y el resumen de la autoevaluación) y el comentario
del marcado. Antes: «Autorregresión, redes neuronales y cierre», «Cierre, resumen y autoevaluación» y «Cierre: ciencia de datos,
resumen y evaluación». El `shortTitle` («Cierre») no cambia. **Se verificó en la página**: el botón de la barra lateral dice
«Cierre: redes, resumen y evaluación» y el h2 coincide. El único otro sitio con el título es la lista de módulos de
`preparcial-corte-2.html` (ver arriba).

**La actividad del Parcial 2** se llama ahora **«Práctica de repaso · capítulo 2 y módulos 3.1–3.4»** (el h3 y el h4 del recuadro,
los dos sitios). El párrafo de presentación ya no dice «para preparar el Parcial 2»: dice «para repasar», que se escribieron como
preparación del Parcial 2, que ya se aplicó, y que siguen sirviendo de repaso. **Sus preguntas no se tocaron**
(`AUTOEVALUACIONES['parcial2']`, su id y los comentarios del JS quedan como estaban).

**«Lo que viene»** dice dónde vuelve `AirPassengers`: «la dependencia que quedó en ∇∇₁₂ log y_t vuelve en el Capítulo 5, que
extiende las herramientas de este a la estacionalidad y le ajusta el modelo *airline* (módulos 5.5 y 5.7)». Leído en
`capitulo-5-sarima.html`: el 5.5 es «El modelo *airline*» (lo ajusta a `log(AirPassengers)`) y el 5.7 es «Caso completo:
log(AirPassengers)», con ρ̂₁ = −0.341 y ρ̂₁₂ = −0.387 sobre ∇∇₁₂ log y_t, que es la serie con que cierra el Capítulo 2. No se
escribió esa cifra en el capítulo 3.

## T3.3 · Notación: una convención y se aplica

| Costura (§7.10) | Convención | Dónde se aplicó |
|---|---|---|
| `T` frente a `n` | **`T` es la longitud de la serie** (como el Capítulo 2 y el resto del 3: banda ±1.96/√T, laboratorio, Ljung–Box). `n` queda como argumento de `arima.sim` y como variable del código | banda del ciclo (M5), fórmulas de AIC/AICc/BIC y su nota (M8), pie de la tabla ordenable (JS), manchas solares (M7, M10), 137 log-retornos (M9), divisores de Yule–Walker (M7), M10 |
| «identificado» / «identificación» | **«identificable»** es un parámetro (θ y 1/θ; M3, y los cuatro coeficientes del ARMA(2,2), M10); **«identificación»** es proponer p y q (M5). Cada módulo lo dice una vez | M3, M5, M10 |
| «abanico» (dos sentidos) | En el capítulo 3 es **la banda de un pronóstico que se abre con el horizonte** (como en los capítulos 4 a 6); se dice en su primera aparición (M4) que no es el abanico de amplitud de los capítulos 1 y 2 | nota del M4 |
| «caminata» / «paseo» | **«caminata aleatoria»** | dos usos en el M4 |
| pseudo-ciclo / pseudo-periodo / periodo | **pseudo-ciclo** es el fenómeno; **pseudo-periodo** su longitud (como las lecturas de los simuladores y el quiz); «periodo» a secas solo en sentido llano (un periodo de tiempo) o para el «periodo medio» de FPP3. La fórmula del M2 pasa a P = 2π/arccos(…) (poner «pseudo-periodo» dentro de la fórmula la hacía desbordar 8 px a 375 px) | M2, nota del M9, M10 |
| `j` y `h = j + 1` | Se dice una vez donde se usan: el horizonte h usa los h pesos ψ₀…ψ_{h−1}, y el peso ψ_j es el último del horizonte h = j+1 | nota del M4 y frase antes de la tabla del M9 |
| «Módulo N» / «3.N» | **«Módulo N»** en la prosa, hablando de este capítulo; **«3.N»** en rótulos (las filas de la tabla del M9 son los títulos de los módulos) y cuando el módulo se cita junto a otro capítulo («capítulo 2 y módulos 3.1–3.4»). Ya era así: no hizo falta cambiar nada | — |
| `ρ_k = 0` de la PACF | φ_kk = 0 | M2 |

---

## Minutos medidos (D7)

**La herramienta del lector subestimaba cuatro módulos.** `diag/lector_carga.py` quita las etiquetas HTML con `<[^>]+>` *antes*
de las fórmulas, y un `<` crudo dentro de una fórmula en línea (`$|w| < 1$`, que el capítulo escribe así) hace que esa fórmula se coma todo hasta el
siguiente `>`. Midiendo `HEAD` con ella, el M10 sale de 726 palabras (el de `58bdfc5` salía de 1 539) y el M2, de 497. La copia
**`r3_minutos.py`** quita las fórmulas antes que las etiquetas, no deja que el `$` de un `<code>` (`pacf(y)$acf`) abra una fórmula, y solo toma
por etiqueta un `<` seguido de letra, `/` o `!`. La fórmula de minutos y el resto del convenio son los mismos (palabras/180 + 3 por
simulador + 2 por bloque de código; pista y solución abiertas; sin plegados ni quizzes). Con ella, «antes» y «después» son comparables.

| Mód. | Palabras antes → después | Medido antes (herramienta original / corregida) | Medido después | Declarado antes → ahora | Distancia |
|---|---|---|---|---|---|
| M1 | 957 → 1 088 | 9.0 / 9.3 | 10.0 | 12 → **10** | 0.0 |
| M2 | 1 055 → 1 136 | 10.8 / 13.9 | 14.3 | 14 → **14** | 0.3 |
| M3 | 1 089 → 1 237 | 11.7 / 14.1 | 14.9 | 12 → **15** | 0.1 |
| M4 | 1 227 → 1 460 | 11.7 / 11.8 | 13.1 | 12 → **13** | 0.1 |
| M5 | 1 741 → 1 967 | 11.2 / 16.7 | 17.9 | 14 → **18** | 0.1 |
| M6 | 338 → 338 | 6.9 / 6.9 | 6.9 | 10 → **7** | 0.1 |
| M7 | 600 → 692 | 8.3 / 8.3 | 8.8 | 14 → **9** | 0.2 |
| M8 | 919 → 1 045 | 9.4 / 10.1 | 10.8 | 14 → **11** | 0.2 |
| M9 | 2 988 → 3 244 | 27.6 / 27.6 | 31.0 | 19 → **31** | 0.0 |
| M10 | 2 696 → 2 828 (abierto) | 10.7 / 21.0 | 21.7 | 14 → **22** | 0.3 |
| M11 | 377 | 2.1 | 2.1 | 30 → **30** (el reloj del ensayo) | — |
| M1–M10 | | 139.7 (corregida) | 149.4 | 135 → **150** | |

Se declara la columna «abierto» (convenio del Capítulo 2), con el comentario correspondiente en `courseData`: no incluye el
tiempo de resolver los ejercicios, los desarrollos plegados (1 692 palabras, unos 9 min entre siete módulos) ni los quizzes del
M10 (autoevaluación 17.4 min de lectura; práctica de repaso 29.2). Distancia máxima: 0.3 min; el objetivo era < 3. Con los
números declarados antes (135 en M1–M10) y medidos con la herramienta corregida (139.7) el capítulo ya estaba cerca en el total, pero
no por módulo (M9 8.6 min más de lo declarado, M10 7.0, M7 5.7 menos). **Lo que más pesa ahora:** el M9, con 31 min (el bloque
de código nuevo suma 2 min por la fórmula, aunque se lea sin leer cada línea) y el M5, con 18. La portada (`Htmls_Series/index.html`) no
muestra minutos ni títulos de módulos; `cuenta_sitio.py` sigue en verde.

---

## Lo que no se tocó, y por qué

| Qué | Por qué |
|---|---|
| `AUTOEVALUACIONES['cap3']`, `['parcial2']`, el simulacro del M11, los simuladores, `precalculo/genera_*.R` | fuera del encargo (R5, banco, R2). Ninguna cifra nueva exigió tocar un generador |
| Los ejercicios 1 a 3 y sus pistas | son de la R5. Siguen con `n` (el ejercicio 1) y «periodo» (el 3); el quiz dice «el modelo no queda identificado» en una retro: queda para la R5 |
| «el envolvente» (M9 y el JS de la lectura del simulador) | no está en la lista del encargo y arreglarlo exige tocar texto de un simulador |
| El M6 como módulo débil (proceso rotulado, sin «adivinar») | cambiaría el simulador; solo se corrigieron sus promesas |
| «Retomemos la TRM» (log-retornos frente a la diferencia) y el aparte R/Python de Ljung–Box del M8 | no están en D4, D6 ni D7; anotados |
| El puente a la RNN (`x_t` es una entrada, no un ruido blanco) | no está en el encargo; anotado |
| Voz: el M10 tutea en prosa expositiva | el encargo pide respetar el tuteo donde ya se dirige al lector; lo nuevo va impersonal |
| ARMA(2,2) del M10 (φ = (1.1, −0.28), θ = (0.1, −0.20)) | son cifras que no cambiaron; las verificó el par (`diag/par_verifica.R`: misma ACF que el ARMA(1,1)). **No tienen bloque en la página** |

## Lo que se encontró

1. **La herramienta de carga del lector subestimaba el M2, el M3, el M5 y el M10** (arriba). Los «declarados por encima de lo
   medido» del diagnóstico (M1–M8: 102 frente a 78) eran en buena parte un efecto de medida: con la corrección M1–M8 miden 91.1.
2. **El M1 dejaba un archivo sin seguimiento** (`serie.csv`) al correr el verificador de bloques. Ya no.
3. **El bloque de la TRM se escribió primero con 1.684** (la distancia calculada con la r₁ ya redondeada); el verificador de
   bloques dio 727 de 728 y la salida real es 1.683. Es el caso típico de las cifras con dos redondeos; con la corrección, 732 de 732.
4. **El periodo con otro nombre desbordaba una fórmula a 375 px** (8 px): lo cazó el recorrido por Chrome, no la lectura del texto.
5. **Con el orden tabla → laboratorio → ciclo**, la primera frase del ciclo puede decir por qué la tabla no alcanza (la tercera
   fila; la muestra ruidosa) porque ya se mostraron; antes lo tenía que afirmar.
6. **El «periodo medio» de FPP3 (11.84), que la R1 añadió en el M9, no tenía código**; ahora lo tiene.

## Para la R4 (fuentes) y la R5 (práctica)

**R4.** Afirmaciones nuevas o movidas que necesitan `propia` o fuente: (1) λ = 1 − b (aproximación delta; propia); (2) el ρ₁
inducido por promediar una caminata (la cifra sale de los pesos de los choques; el resultado es conocido, sin atribución escrita);
(3) la banda de Bartlett de `statsmodels` (leída en el código de `acf`, `statsmodels` 0.14.6); (4) el criterio por defecto de
`auto.arima` (`formals`, `forecast` 9.0.2); (5) «la raíz de 1 − B sobre el círculo; ρ₁ = −0.5» (propia, a partir de la fórmula del
M3 y del adelanto del Capítulo 2); (6) lo que se afirma del Capítulo 5 en «Lo que viene» (leído en ese archivo); (7) el recuadro de
Yule («inventó en 1927…»), las atribuciones de FPP3 9.5 y del algoritmo de Hyndman–Khandakar y la ayuda de `?arima` sobre S-PLUS,
que ya estaban y siguen sin cita. La sección «Convenios» del M1 contiene la mayoría de las atribuciones a Box–Jenkins y S-PLUS.

**R5.** (1) El ejercicio 1 usa `n`, el 3 usa «periodo» y una retro del quiz dice «el modelo no queda identificado»: los tres chocan
con las convenciones de arriba. (2) La práctica por módulo (D9) sigue como estaba: esta ronda no añadió ningún ejercicio. Dos
sitios nuevos donde el lector puede rehacer algo: la elasticidad (`elasticidad()` con otra serie) y la comprobación de convenios
del M1. (3) Series ya usadas en el capítulo: `sunspot.year`, `lh`, la TRM y las del Capítulo 2.

---

## Comprobaciones finales

Tras la última edición. Salidas en `diagnostico/cap3/comprobaciones/`.

| Comprobación | Resultado | Salida |
|---|---|---|
| `python3 precalculo/verifica_todo.py` | **11 verificadores en verde** (Tailwind al día, capítulo 3 reproducible, cifras del sitio, posición de la correcta, ninguna cita de memoria) | `r3_verifica_todo.out` |
| Verificador de bloques, capítulo 3 | **732 de 732, 0 bloques con discrepancias** (antes 557/557); 15 bloques de R y 12 de Python (antes 14 y 11) | `r3_bloques_cap3.out` |
| Bloques de Python, uno por uno, con sus comentarios | los 12 corren con código de salida 0 (el del caso 2 del M9, desde la carpeta de trabajo y desde la página); las cifras con decimales de los comentarios que no aparecen en la salida citan a R o son parámetros (la banda, θ = 0.7) | `r3_bloques_python.out` |
| `r2b_sintaxis.py` | cinco «OK», ninguna declaración repetida | `r3_sintaxis.out` |
| `audita_posicion_correcta.py` | «Ningún instrumento concentra las correctas» | `r3_posicion.out` |
| `verifica_preparcial2.py` (por el título copiado) | 502 comprobaciones, 0 fallos | — |
| Cadena | `ensambla_cap3.py` «reproducible byte a byte»; `ensambla_cap4/5/6.py` corridos en orden: `git diff --stat` no los muestra; `r3_edita.py --comprobar`: árbol = `HEAD` + ediciones | — |
| Once módulos por HTTP (`htmls-series`, Chrome sin ventana, 1200 y 375 px) | **22 módulos × ancho: 0 errores de KaTeX, 0 «$» sin componer, 0 fórmulas desbordadas, 0 lienzos sin pintar, 0 excepciones; un solo evento de consola: el `favicon.ico` 404 de siempre**. h3 en el orden de arriba; la barra lateral dice «Cierre: redes, resumen y evaluación» | `r3_recorrido.out`, `.json` |
| Cada cifra de la prosa, recalculada | las de este informe salen de `r3_cifras.R` → `r3_cifras.out` y de los bloques | `r3_cifras.out` |

`precalculo/serie.csv` ya no se crea (el bloque que lo escribía se reescribió); no hay nada que borrar.
El servidor del puerto 8731 no estaba en marcha al empezar: se arrancó con `preview_start` (`htmls-series`) y se detuvo al terminar.
