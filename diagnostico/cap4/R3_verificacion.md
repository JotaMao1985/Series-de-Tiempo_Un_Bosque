# Capítulo 4 · R3 («estructura») · verificación independiente

Verificador: sesión distinta de la que redactó. Fecha: 2026-11-22. Base: `531b907` (`HEAD`) más los cambios sin commit del árbol de
trabajo (6 archivos: `Htmls_Series/capitulo-4-modelos-arima.html`, `ensamblado/cap4/templates_{1_3,4_6,7_9,10}.html`,
`ensamblado/ensambla_cap4.py`). Leí el diff completo (`git diff HEAD`) antes que el informe del redactor
(`R3_cambios.md`), recalculé las cifras con guiones propios (`v3_*`) y recorrí el capítulo por HTTP. **No edité ninguna fuente, ni el
HTML, ni el informe del redactor**; solo creé `diagnostico/cap4/comprobaciones/v3_*` y este archivo. No hubo commit, stash, restore ni push.

**Veredicto:** la ronda cumple D6 y D7 y cumple D5 en lo que el encargo nombra (PP, «dos medias», TRM, `auto.arima`, Holt, el ARIMA(1,1,1)
del Nilo a la vista, las introducciones del M3, M4 y M6). **0 hallazgos Altos, 2 Medios, 8 Bajos.** Ninguna cifra nueva o movida está mal; los
dos Medios son una frase que quedó inexacta al moverla (V1) y una afirmación del informe que no se sostiene más una parte de D5 que sigue
incumplida (V2). Hay trabajo de corrección antes de publicar, pero ninguna se enseñaría como error de cifra.

---

## 1. Hallazgos

Gravedad: **Alto** = error que se enseña o algo roto; **Medio** = confunde o incumple el plan; **Bajo** = forma. Las líneas son de
`ensamblado/cap4/templates_*.html` (el HTML se reensambla desde ahí).

| Id | Grav. | Mód. | Lugar | Qué está mal | Evidencia | Propuesta |
|---|---|---|---|---|---|---|
| **V1** | **Medio** | M10 | `templates_10.html:208-210`, nota «El resultado, aceptado tal cual»: «…aunque a ojo la serie «claramente sube». **Como en el Nilo (Módulo 5), esa deriva es la media de las diferencias**, $(y_n - y_1)/(n-1)$: depende solo del primer mes y del último.» | Es la nota de la TRM que salió del M5, reescrita. En el original el sujeto era «esa media» (la media de las diferencias, que telescopa en el Nilo y en la TRM); al pasar a «esa deriva» la frase afirma que **en el Nilo la deriva estimada es la media de las diferencias, y no lo es**: en el ARIMA(1,1,1) con deriva del M5, δ̂ = −2.883, y la media de las diferencias es −3.84 (el propio M5 las distingue: «equivaldría a… con el φ̂ = 0.271 del propio modelo con deriva»). Solo en el ARIMA(0,1,0) de la TRM coinciden. Un estudiante que lee los dos módulos ve dos cifras para «la deriva del Nilo». | `v3_cifras.out`, sección «M5/M10»: `Nilo ARIMA(1,1,1)+deriva: delta = -2.883`; `media de las diferencias Nilo = -3.838 = (740-1120)/99`; `>>> delta-hat del ARIMA(1,1,1)+deriva NO es la media de las diferencias: -2.883 vs -3.838`; `TRM RW+deriva: delta = 8.001 ee = 10.356 t = 0.77`; `media de diff(TRM) = 8.001 = (y_n - y_1)/(n-1) = 8.001`. | Escribir: «En un ARIMA($0,1,0$) esa deriva es exactamente la media de las diferencias, $(y_n-y_1)/(n-1)$ (en el ARIMA($1,1,1$) del Nilo, no: allí δ̂ = −2.883 y la media vale −3.84, Módulo 5): depende solo del primer mes y del último.» |
| **V2** | **Medio** | M8 (también M1 y M10) | M8: `templates_7_9.html:269-272`, introducción de `sobrediferenciacion`: «En $d = 2$ y $d = 3$ el $\hat\theta$ se clava en $-1$ y $|\text{raíz MA}| = 1$: el término MA está deshaciendo la diferencia que acabas de imponer.» M1: `templates_1_3.html:131-137`, intro de `nilo-y-diferencia` («La media cae a casi cero… $\hat\rho_1$ cambia de signo, y con $d = 2$ queda por debajo de $-0.5$… La varianza apenas baja con $d = 1$ y casi se triplica con $d = 2$»). M10: `templates_10.html:121-124`, intro de `trm-identificacion` («arranca en $0.964$… solo una barra de veinte se sale… $\hat\rho_8 = -0.190$»). | D5 dice «las introducciones de simulador dejan de dar el resultado». Las del M3, M4 y M6 ya no lo dan (bien). Pero **el informe afirma que la del M8 «pide hacer y no adelanta»**, y no es así: la lectura del simulador (JS, `SIMULADORES['sobrediferenciacion']`) pinta justo `θ̂ de un MA(1)`, `|raíz MA|` y «⚠ diagnóstico: raíz unitaria en el MA: sobrediferenciado»; la introducción lo da antes de mover el selector. La del M1 lo reconoce el informe («se anota»); la del M10-TRM no se menciona. | `v3_intros.out` (texto actual de las 13 introducciones); lectura del JS de `sobrediferenciacion`. | Reescribir la del M8 como las del M4 y M6 («Sube $d$… ¿qué hace $\hat\theta$ al pasar de 1 a 2? ¿Y $|\text{raíz MA}|$?») y mover la frase actual a un recuadro posterior; decidir si la R3 cierra también M1 y M10-TRM o si D5 se da por cumplido solo en M3, M4 y M6 y el resto queda anotado para la R5. **Corregir la frase del informe en cualquier caso.** |
| V3 | Bajo | M1 / M8 | M1 cambió «coeficientes reales» por «coeficientes **estimados**» (`templates_1_3.html:248`, nota de la anomalía). M8 conserva `templates_7_9.html:330`: «integrar la serie del Nilo con sus **coeficientes reales** casi no cambia la varianza (razón $1.006$)». | Misma cosa, dos nombres. Si «estimados» corrige «reales» en el M1, el M8 lo repite. | `v3_varianza.out` (búsqueda de «coeficientes»). | Cambiar «reales» por «estimados» en `templates_7_9.html:330`. |
| V4 | Bajo | M3 | `templates_1_3.html:591-594`, recuadro «Una misma serie, tres respuestas de `ndiffs()`»: «el valor por defecto de `ndiffs()` —y por tanto el que usa `auto.arima()`, la función de `forecast` que ajusta sola varios ARIMA y se queda con el de menor AICc, y que el Módulo 7 abre— es KPSS». | La presentación de `auto.arima` queda enterrada en un inciso de 33 palabras entre guiones que parte la oración principal (sujeto «el valor por defecto de `ndiffs()`», predicado «es KPSS»). El contenido es correcto (el criterio por defecto de `auto.arima` es AICc y elige $d$ con KPSS); la forma no deja que el estudiante vea la presentación. | Lectura del M3. | Dos oraciones: «…es KPSS, la única que dice que sí. Es también el que usa `auto.arima()`, la función de `forecast` que ajusta sola varios ARIMA y se queda con el de menor AICc; el Módulo 7 la abre.» |
| V5 | Bajo | M3 | `templates_1_3.html:549`, fila 3 de la tabla de evidencias: «La raíz MA del ARIMA($1,1,1$) queda en $1.144$ **(Módulo 6)**». | Ahora el M1 es el primero que imprime 1.144 (bloque nuevo) y el M1 ya dice «B=1.144». La remisión sigue siendo cierta (el M6 la muestra otra vez), pero el estudiante la vio tres módulos antes. | `v3_orden.out`; `v3_remisiones.out`. | «(Módulos 1 y 6)». |
| V6 | Bajo | M4 | La trampa de la PACF que corta en 1 («como la firma de un AR(1) con $\phi \approx 0.5$ es confundir la no estacionariedad con dinámica») está en el párrafo **previo** al simulador (`templates_4_6.html:25`, sin cambios) y el recuadro nuevo «Lo que enseña el simulador» (`:53`) la repite («la trampa está en la PACF: solo se sale el rezago 1, como en un AR(1) con $\phi \approx 0.5$…»). | La introducción ya no adelanta el resultado, pero el párrafo de arriba sí lo da y el recuadro lo vuelve a decir. Redundante, no incorrecto. | `v3_alcance.out` §6 (el recuadro se cuenta como contenido movido; el párrafo no cambió). | Quitar la mitad del recuadro (dejar el −0.626, el −0.402 y «la tabla elige $p$ y $q$; no confirma $d$») o la del párrafo. |
| V7 | Bajo | M3 | `templates_1_3.html:769`, bloque de R nuevo: `round(c(antes = …, despues = …, beta = …, sigma = sd(residuals(dos_medias))), 2)` imprime `sigma 127.03`; la prosa (`:618`) lo escribe $\hat\sigma = 127.0$. | La etiqueta `sigma` es la **desviación típica muestral de los residuales** (divisor $n-1$). El `arima` que acaba de ajustarse guarda otra: `dos_medias$sigma2` es la de máxima verosimilitud, $\hat\sigma = 126.39$; la de regresión (divisor $n-2$) es 127.67. Un estudiante que inspeccione `dos_medias$sigma2` encontrará otra cifra bajo el mismo símbolo. La cifra 127.03 es la correcta para lo que el experimento necesita («desviación de sus residuales») y es la que ya usaba el generador. | `v3_cifras.out`: `sd(residuals) = 127.03  sqrt(sigma2 ML) = 126.39  sigma OLS (n-2) = 127.67`. | Rotular `sd_resid` (o comentar «desviación típica de los residuales, divisor n−1») y escribir «desviación típica de sus residuales, 127.0» sin sombrero. |
| V8 | Bajo | M4 | `templates_4_6.html:96`: «el equivalente del suavizamiento exponencial simple con $\alpha = 1 + \hat\theta = 0.267$». | La equivalencia es de modelo y es cierta (con $\alpha = 1+\hat\theta$ el pronóstico a un paso de `ses()` coincide con el del IMA(1,1): 798.37 los dos), pero **`ses(Nile)` estima su propio α: 0.2457** (y `ets(ANN)`, 0.2455), con pronóstico 805.34. Quien lo ejecute para comprobar no ve 0.267. | `v3_ses.out`. | «…con $\alpha = 1 + \hat\theta = 0.267$ (el α implícito; `ses()` lo estima por su cuenta y da otro, 0.246)». |
| V9 | Bajo | M10 | (a) `templates_10.html:562`: «La TRM no tenía estacionalidad… **El capítulo termina con un experimento** que muestra por qué hace falta el siguiente.» (preexistente) (b) `:311`: «A un mes, **los dos intervalos se cumplen** dentro de la muestra: el 95 % deja fuera solo 6 de los 137… y el 80 % del Módulo 9 cubre el 83.9 %.» | (a) Tras el puente siguen el resumen, la autoevaluación, los ejercicios y las lecturas: «termina» ya no es exacto con el orden que D6 fija. (b) El M9 dice que con colas pesadas «la cobertura real **se separa** de la nominal —en la TRM, a un mes, el intervalo del 80 % cubre el 83.9 %—»; el M10 dice que «se cumplen». Las dos lecturas del mismo 83.9 son compatibles (cubre de más), pero con verbos opuestos. | `v3_cifras.out`: `cobertura del 80% a 1 mes: 0.8394 (n dentro: 115)`; `fuera 95% a 1 mes: 6 por arriba: 5 de: 137 -> % = 4.4`. | (a) «El puente termina con un experimento…» o «Antes del resumen, un experimento…». (b) «ninguno de los dos queda corto: el 95 % deja fuera… y el 80 % cubre el 83.9 %, de más». |
| V10 | Bajo | — | `R3_cambios.md` §Minutos y `ensambla_cap4.py` (`courseData`): «los minutos de la barra lateral». | La barra lateral del capítulo **no pinta `duration`** (`renderNavigation()` escribe solo `module.title`); el valor solo vive en `courseData`. No hay otro lugar del sitio que declare duraciones del cap. 4 (portada, preparcial, verificadores). No es un defecto del capítulo, pero el informe lo presenta como visible. | `v3_barra.out` (0 entradas con «N min» en el DOM); lectura del JS. | Corregir la frase del informe; si se quiere que el estudiante vea la duración, es trabajo de armazón (no de esta ronda). |

---

## 2. Lo que el informe del redactor afirma, y si lo confirmo

| Afirmación (`R3_cambios.md`) | ¿Confirmada? | Cómo |
|---|---|---|
| `r3_edita.py --comprobar`: árbol = `HEAD` + 48 sustituciones, en los cinco archivos | **Sí** | `v3_edita_comprobar.out`: «idéntico a HEAD + ediciones» ×5; «48 sustituciones y 0 traslados» (9 + 21 + 11 + 6 + 1). |
| El HTML es reproducible byte a byte (md5 `5d041667…`) y los caps. 5 y 6 quedan idénticos a `HEAD` | **Sí** | `v3_reensamblado.out`: cap. 4 `5d041667f5f7e706fbea738c33aec9d1` antes y después de `ensambla_cap4.py`; `ensambla_cap5.py` y `ensambla_cap6.py` no cambian nada (`git status` solo lista los 6 archivos); caps. 1–3 tampoco. |
| Ningún número, id ni título de módulo cambia | **Sí** (con una nota) | `v3_alcance.out` §2: 32 ids HTML = 32 (0 añadidos, 0 quitados); `data-simulador` igual (13); `<h2>` de módulo iguales; `courseData` ids/títulos/`shortTitle` iguales. Cambia un `<h3>` interno del M1 («Casos particulares ya conocidos» → «Casos particulares»), que el informe menciona. |
| El simulacro, el texto del quiz, los ejercicios 1–3, M11 y M12, `SIMULADORES`, `DATOS_CAP4` no cambian | **Sí** | `v3_alcance.out` §3 y §4: md5 de `SIMULACROS['cap4-simulacro']` (`ce5374881b`), `AUTOEVALUACIONES['cap4']` (`48705a469f`), `SIMULADORES` (`990ba511d8`) y `DATOS_CAP4` (`dcef0863e4`) idénticos; el bloque de ejercicios 1–3, la sección «Autoevaluación», las «Lecturas» + la nota «Y en el Capítulo 5…», M11 y M12, byte a byte iguales. |
| Ningún `<cite>`, `data-afirma`, autor, año, sección ni DOI nuevo; no se toca `bibliografia/`, deck, preparcial | **Sí** | `v3_alcance.out` §5: 0 añadidos de cada patrón en las 305 líneas añadidas; `git status` sin archivos de esos árboles. Además `verifica_cifras_cap4.py` del deck: 469 claims, 0 no coinciden (`v3_deck_cifras.out`). |
| Sin clases nuevas de Tailwind | **Sí** | `compila_tailwind.py --comprobar` en verde dentro de `verifica_todo.py`. |
| `verifica_todo.py`: 11 verificadores en verde | **Sí** | `v3_verifica_todo.out` (11/11, `exit=0`; 114.7 s el de Tailwind). |
| `verifica_bloques_cap6.py`: 822 de 822 cifras; 14 bloques de R y 11 de Python; 0 discrepancias | **Sí** | `v3_verifica_bloques.out`: idéntico. Además mis dos ejecutores independientes (§4). |
| 66 cifras recalculadas, 0 «NO» (`r3_cifras.R`) | **Sí** | Lo reejecuté: 66 `[ok]`, 0 `[NO]`, salida idéntica a su `.out`. Mi propio guion (`v3_cifras.R`) las recalcula sin mirar el suyo. |
| El M10: palabras 3 538 → 3 560 (no baja) | **Sí** | Con un analizador HTML propio: 3 467 → 3 489 (+22, el mismo aumento); con el suyo, +22. |
| Minutos medidos y declarados con distancia máxima 0.5 min; convenio «abierto» | **Sí** (distancia 0.6 con mi medida, M7) | `v3_minutos.out` frente a `courseData`. Ver §4. |
| Los desarrollos plegados suman «unos 4 min entre tres módulos» y la autoevaluación «unos 18 min» | **Sí** | 137 + 287 + 364 = 788 palabras = 4.4 min (M1, M3, M9); autoevaluación 18.1 min (3 254 palabras, herramienta del redactor revisada). |
| `r3_revisa.js`: 0 errores de consola, 0 `.katex-error`, sin desbordes, 0 simuladores sin pintar, `typeof tailwind = undefined` | **Sí** | Mi `v3_revisa.js`, servidor propio 8771 y Chrome 9301, 12 módulos × 1200 y 375 px: «TODO EN ORDEN» (`v3_revisa.out`). |
| «Los minutos de la barra lateral (11, 7, 14, …)» | **Parcial** | Los valores son los de `courseData`, ciertos; la barra no los muestra (V10). |
| «Las introducciones de simulador del M8, el M9 (forma) y el puente piden hacer y no adelantan» | **No, para el M8** | V2. M9 (forma) y puente sí son neutras. |
| «El contenido de la nota de la TRM del M5 va al recuadro del M10, reescrito» (sin pérdida) | **Parcial** | El contenido se conserva, pero la frase sobre la media de las diferencias cambió de sentido (V1). |
| El «(8,1,3) con deriva» de la búsqueda amplia no se reproduce en statsmodels (ρ̂12 = 0.515) | **Sí** (no está en la página) | `v3_airline_py.out`: `rho12 = 0.515` frente a 0.437 en R. |
| En statsmodels, si se incluyen los residuales del arranque del *airline* (`resid[1:]`), Ljung–Box da p = 0.999977 en vez de 0.37 | **Sí** | `v3_airline_py.out`: 0.999977 con `[1:]`, 0.367587 con `[13:]`. |
| «Cuatro» modelos (M6) y «siete» (M7) son las dos ciertas; «8 modelos» es «8 de los 27» (con $d = 1$ solo rechaza el (0,1,0)) | **Sí** | `v3_cifras.out` §M6: con $d = 1$, 4 más; LB(20) < 0.05 en 8 (por $d$: 3, 1, 4); con $d = 1$ solo el (0,1,0); ninguno de los cercanos al mejor de su $d$ rechaza; podio exhaustivo de 7 = el ganador + 4 sin constante + 2 con deriva. |
| La nota «Y en el Capítulo 5…» queda al final «como en el cap. 3» | **Sí** | En el cap. 3, «Lo que viene» también va después de las lecturas (posición 548 de ~560 líneas del M10). |

---

## 3. Criterios de D5, D6 y D7

### D5 · Orden sin renumerar

| Criterio | ¿Se cumple? | Dónde / evidencia |
|---|---|---|
| PP se presenta en su primer uso | **Sí** | `v3_orden.out`: primera aparición en prosa **M3** (antes: M8:87 el nombre completo); fila de «Las pruebas» («PP (Phillips–Perron; H₀: hay raíz unitaria)»), el bloque R imprime `PP.test` (−6.690051, p = 0.01) y el de Python avisa que statsmodels no la trae. Cifra −6.690 recalculada. |
| «Modelo de dos medias» se escribe donde se usa | **Sí** | Primera aparición M3 (la definición misma); el bloque lo ajusta (1097.75, 849.97, β̂ = −247.78, 127.03); el M8 lo remite al M3. |
| La TRM se anuncia donde aparece por primera vez | **Sí** | Todas las menciones en M1–M9 dicen «la TRM del Módulo 10» (M2:108, M9:210, M9:322); la nota que la usaba sin presentarla (M5) salió. |
| `auto.arima` se presenta en su primer uso | **Sí, con V4** | M3 (recuadro de `ndiffs()`); la presentación existe pero en un inciso largo. |
| Holt y el suavizamiento exponencial, en una frase o fuera | **Sí** | Párrafo nuevo antes de la tabla (M1), cuyas dos definiciones son correctas; la fila de Holt dice qué suaviza; el M4 usa α = 0.267 (V8 sobre la forma). Ningún capítulo anterior los presentaba (caps. 1–3: 0 apariciones). |
| El ARIMA(1,1,1) del Nilo se ajusta en un bloque visible la primera vez que se usa | **Sí** | M1: el primer bloque (R y Python) estima el modelo, imprime coeficientes y errores estándar y la raíz MA; `phi`/`theta` salen de ahí. R: 0.2544, −0.8741, e.e. 0.1194 y 0.0605, raíz 1.144 (todo recalculado). Python da 0.2549 y −0.8749 (corrido) y la página lo dice. |
| Las introducciones de simulador del **M3, M4 y M6** ya no adelantan el resultado | **Sí** | `v3_intros.out`: M3 151→120 palabras, M4 206→62, M6 175→111; piden hacer y apuntan a la lectura del simulador, que muestra lo que dicen (ρ̂₁, «ACF/PACF fuera de banda», «diferencia», raíces). Los resultados pasaron a recuadros **posteriores** al simulador; sus cifras verificadas (8 de 27, 4 más, 1.161 / 1.144 / 1.000–1.048). |
| Las demás introducciones de simulador (D5 literal) | **En parte** | M1, M8 y M10-TRM siguen dando el resultado (V2). |
| Notación (`T`/`n`, `n*`, «abanico», «tres evidencias») | **Sí** | `T` vs `n` avisado una vez donde el AICc cambia de símbolo (M6; correcto: los caps. 2 y 3 llaman `T` a la longitud); ningún `y_{n+h}` queda (`v3_orden`/búsqueda); «abanico» se define en su primer uso (M9) y el uso de rango pasa a «rango» (M8); el recuadro de `ndiffs()` ya no choca con «tres evidencias». |

### D6 · El M10, ordenado

| Criterio | ¿Se cumple? | Evidencia |
|---|---|---|
| El Nilo se resume una vez | **Sí** (en lo esencial) | De cuatro resúmenes seguidos a la tabla (más corta), una frase sobre el modelo y la nota de las dos lecciones; la fórmula del modelo ya no se repite (queda en el M1). Subsisten en la sección de la TRM dos citas sueltas de cifras del Nilo (ψ∞ y σ₃₀/σ₁ en el recuadro «Un abanico sin techo»), que sirven a la comparación de tres series. |
| Orden: Nilo → TRM → puente → resumen | **Sí** | `v3_revisa.out`, h3 del M10: «El Nilo, de principio a fin · Caso: la tasa representativa del mercado · El puente al Capítulo 5 · Resumen del capítulo · Autoevaluación · Ejercicios propuestos · Lecturas». |
| El resumen es lo último antes de la evaluación | **Sí** | Resumen → Autoevaluación. La nota «Y en el Capítulo 5…» queda después de las lecturas, como «Lo que viene» del cap. 3 (V9a sobre el verbo «termina»). |
| El puente al cap. 5 lleva su código | **Sí** | Bloque nuevo R y Python (`auto.arima(log(AirPassengers), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)` → ARIMA(0,1,5); ρ̂₁₂ = 0.7245, ρ̂₂₄ = 0.6727, banda 0.1633, Q = 222.4; búsqueda amplia → ARIMA(8,1,3) con deriva, ρ̂₁₂ = 0.437; airline ρ̂₁₂ = −0.0515, p = 0.233; 143 y 131). Todo recalculado en R; el Python corre (219.3, 0.3676 y los comentarios «R da…»). Coincide con las cifras que ya usa el cap. 5. |
| La promesa del M9 sobre el 83.9 % se cumple donde se promete | **Sí** | El M9 dice «El Módulo 10 lo mide»; el M10 retoma «el 80 % del Módulo 9 cubre el 83.9 %» y el bloque lo imprime (`0.839`, 115 de 137). Ver V9b sobre el verbo. |
| Ningún resumen reintroduce la varianza como evidencia de $d$ | **Sí** | `v3_varianza.out`: el resumen dice «La varianza por orden de diferencia no es una evidencia más: repite lo que dice $r_1$ (Módulo 2.7)»; los ejercicios 1 y 2 (sin cambios) la tratan igual. |
| No se parte el módulo | **Sí** | Sin renumerar. Sigue siendo el más largo (43 min abierto), ya señalado por el redactor. |

### D7 · Minutos medidos

Medidos por mí con un analizador HTML (`html.parser`), no por expresiones regulares, con la misma fórmula (palabras / 180 + 3 por simulador + 2 por
bloque de código), con pista y solución abiertas; sin desarrollos plegados, autoevaluación ni simulacro. `v3_minutos.out`
(y `v3_minutos_antes.out` sobre `HEAD`).

| Mód. | Antes: declarado → medido | Ahora: medido (el redactor) | Declarado ahora | Distancia (mi medida) |
|---|---|---|---|---|
| M1 | 12 → 9.9 | 10.5 (10.6) | 11 | −0.5 |
| M2 | 10 → 6.8 | 6.8 (6.8) | 7 | −0.2 |
| M3 | 16 → 13.6 | 13.7 (13.7) | 14 | −0.3 |
| M4 | 14 → 8.9 | 8.9 (9.0) | 9 | −0.1 |
| M5 | 12 → 6.6 | 5.9 (5.9) | 6 | −0.1 |
| M6 | 16 → 9.2 | 9.7 (9.8) | 10 | −0.3 |
| M7 | 14 → 9.3 | 9.4 (9.6) | 10 | −0.6 |
| M8 | 16 → 10.5 | 10.7 (10.9) | 11 | −0.3 |
| M9 | 16 → 13.9 | 14.1 (14.4) | 14 | +0.1 |
| M10 | 24 → 40.8 | 42.9 (43.0) | 43 | −0.1 |
| M11 | 40 (reloj del ensayo) | 2.5 de lectura | 40 | — |
| M12 | 5 → 2.5 | 2.5 (2.5) | 3 | −0.5 |
| M1–M10 | 150 → 129.4 | 132.7 | 135 | |

Cumple D7: la distancia máxima es **0.6 min** (objetivo del redactor, < 3) con ambas herramientas; la herramienta del redactor es la del cap. 3 sin más cambio
que la exclusión del simulacro (`diff` con `diagnostico/cap3/comprobaciones/r3_minutos.py`), y el cap. 3 declara con el mismo convenio (su razón
abierto/declarado ronda 1.00). **No queda una duración vieja en otro sitio**: `duration` solo existe en `courseData`
(`ensambla_cap4.py`), y la portada `index.html`, `preparcial-corte-2.html` y los verificadores no declaran duraciones del cap. 4. Los «40 minutos» del
M11 y los «70 minutos» del M12 son el reloj del quiz y del parcial, no lecturas, y no cambian. Ver V10.

---

## 4. Comprobaciones ejecutadas (con cifras)

| # | Comprobación | Resultado | Salida |
|---|---|---|---|
| 1 | Reproducibilidad: `r3_edita.py --comprobar`; `ensambla_cap4/5/6.py`; md5 | 5/5 archivos idénticos; md5 cap. 4 `5d041667…` antes y después; caps. 5 y 6 sin cambios | `v3_edita_comprobar.out`, `v3_reensamblado.out` |
| 2 | `precalculo/verifica_todo.py` | 11 de 11 en verde, `exit=0` | `v3_verifica_todo.out` |
| 3 | `verifica_bloques_cap6.py --html …capitulo-4…` | 822 de 822 cifras; 14 R + 11 Python; 0 con discrepancias | `v3_verifica_bloques.out` |
| 4 | Ejecutor propio de los 14 bloques de R (cada uno en carpeta vacía con la copia de la TRM), cruzando cada `#>` | 14/14 con código 0; 0 números esperados ausentes (2 falsos positivos: avisos de R, que van por stderr) | `v3_bloques_r.py` / `.out` |
| 5 | Ejecutor propio de los 11 bloques de Python, ídem | 11/11 con código 0; 0 números esperados ausentes (incluido el puente, que baja `AirPassengers` con `get_rdataset`) | `v3_bloques_python.py` / `.out` |
| 6 | Recálculo independiente en R de cifras nuevas o movidas: M1 (ajuste, raíces, 1.006, 32.8, 201), M2 (`d`, 0.7997, 816.18…), M3 (PP, dos medias, `ndiffs`, 0.045 / 1.000), M4 (α), M5/M10 (deriva Nilo y TRM), M6 (27 modelos), M7 (podio de 42 / 18 modelos), M8 (RMSE/MAE, AICc 1257.91), M9 (842.17, ψ∞, σ₃₀/σ₁), M10 (TRM completa, 83.9 %, 6/137, 11/126, curtosis, marzo 2020 y julio 2022, puente) | **Todas coinciden** con la página; las únicas discrepancias son V1 (frase) y V7/V8 (rótulos) | `v3_cifras.R` / `v3_cifras.out` |
| 7 | La rejilla de 27 modelos del explorador (JSON de `genera_cap4.R`) frente a mi rejilla | 27/27 con ΔAICc < 0.005 y ΔLB < 0.0005 | `v3_json.py` / `v3_json.out` |
| 8 | Alcance: ids, títulos, simulacro, quiz, simuladores, datos, ejercicios, M11/M12, atribuciones, frases que desaparecen o se duplican | Sin cambios fuera de lo declarado; 0 frases repetidas literalmente; de las 72 frases quitadas literalmente, las 16 de parecido bajo se revisaron una a una: son frases movidas o reescritas (nota de la TRM, intros de simulador) o recortes deliberados; lo único que deja de estar en la prosa es la lista de vecinos «(1,1,1), (0,1,2) y (1,1,0)» y los semianchos ±278 / ±391 del cuadro del Nilo (el Shapiro 0.731 sigue en el M8) | `v3_alcance.py` / `.out` |
| 9 | Orden de primeras apariciones (27 términos), antes y después | Ver §3 D5 | `v3_orden.py` / `.out` |
| 10 | Remisiones («Módulo N», «más abajo», «de abajo», «el recuadro «…»»): las 37 nuevas o con contexto nuevo en M1–M10, una por una | Todas apuntan a algo que está donde dicen, salvo la matización de V1 y V5 | `v3_remisiones.out` |
| 11 | Equilibrio de etiquetas y escapes en `<pre>` por módulo | 0 sin cerrar, 0 cierres sobrantes, 0 etiquetas ni `&` sueltos en `<pre>`, antes y después | `v3_html.py` / `.out` |
| 12 | Visual por HTTP (servidor 8771, Chrome CDP 9301, cerrados al acabar), 12 módulos × 1200 y 375 px, con derivaciones, pistas y soluciones abiertas | 0 errores o avisos de consola; 0 `.katex-error`; 0 «$» sin componer; 0 fórmulas en `<pre>`; 0 desbordes (ancho de página = ventana); gráficos pintados 1/1 (M1), 2/2 (M3), 3/3 (M4), 2/2 (M6), 1/1 (M7), 2/2 (M8), 3/3 (M9), 6/6 (M10), 0 simuladores sin pintar, 0 lecturas vacías; 11 pares de pestañas R/Python (9 + 2 del M10) cambian bien; `typeof tailwind` = `undefined` | `v3_revisa.js` / `.out`; capturas en `diagnostico/cap4/capturas/v3/` (ignorada por git) |
| 13 | Verificador de cifras del deck del cap. 4, que lee el texto del capítulo como una de sus fuentes | 469 claims, 0 no coinciden (el deck no se ve afectado por la R3) | `v3_deck_cifras.out` |
| 14 | Minutos por módulo con analizador propio | Ver §3 D7 | `v3_minutos.py` / `.out`, `v3_minutos_antes.out` |
| 15 | `ses()` frente al α implícito del IMA(1,1); statsmodels y el *airline* | V8; confirma los hallazgos 5 y 6 del informe | `v3_ses.out`, `v3_airline_py.out` |

Las capturas se hicieron con el encabezado fijo de la página encima del elemento (artefacto de `scrollIntoView` + captura de región; el mismo del redactor); no es un defecto de la página
y no se usó como evidencia. La comprobación visual se apoya en las medidas del DOM de la fila 12.

## 5. Lectura como estudiante de 6.º semestre (M1, M3, M10)

- **M1.** Entra bien: definición → desarrollo plegado → «Casos particulares» con la frase que presenta el suavizamiento exponencial y Holt **antes** de la tabla → simulador →
  bloque que ahora estima el ARIMA(1,1,1) → nota de la anomalía con la fórmula del modelo (única copia que queda) → aviso del signo → puente al M2. La declaración de que `c` la trata el M5 y «hasta
  entonces el modelo va sin ella» es cierta en M2 a M4 (ningún ajuste lleva constante). El salto menor es que la introducción del simulador sigue contando el resultado (V2).
- **M3.** El orden queda: tres evidencias (PP ya presentado en la fila) → qué contrasta cada prueba → varianza → recuadro de `ndiffs()` (V4) → experimento con «dos medias» definido en el
  párrafo anterior al simulador → resultado → plegado → bloque (que ajusta el modelo de dos medias y de ahí saca el 127.03) → KPSS en R y Python → regla práctica → cierre. Sin saltos; solo el inciso de V4 se lee mal.
- **M10.** Cuatro tiempos anunciados en la apertura y cumplidos en ese orden. La tabla del Nilo es más corta y apila bien a 375 px (capturada); la nota de las dos lecciones sigue siendo la mejor
  pieza. La TRM ya no repite lo que el M5 decía; el bloque respalda cada cifra, incluido el 83.9 %. El puente tiene ahora la tabla de cifras **antes** del bloque que las produce
  (fórmula de ρ̂₁₂, ρ̂₂₄, Q, y luego el código al final de la sección): se lee, pero el estudiante tiene que esperar a bajar para verlas salir. Las dos únicas frases que remiten a algo que ya no está donde dicen son V1 («Como en el Nilo (Módulo 5)…») y,
  marginalmente, el «El capítulo termina con un experimento» de V9.

## 6. Archivos creados

Todos en `diagnostico/cap4/comprobaciones/` salvo este informe y las capturas:

`v3_modulos.py` (utilidades), `v3_orden.py` / `v3_orden.out`, `v3_cifras.R` / `v3_cifras.out`, `v3_bloques_r.py` / `v3_bloques_r.out`,
`v3_bloques_python.py` / `v3_bloques_python.out`, `v3_json.py` / `v3_json.out`, `v3_alcance.py` / `v3_alcance.out`, `v3_intros.py` / `v3_intros.out`,
`v3_html.py` / `v3_html.out`, `v3_minutos.py` / `v3_minutos.out` / `v3_minutos_antes.out`, `v3_revisa.js` / `v3_revisa.out`, `v3_barra.js` / `v3_barra.out`,
`v3_ses.R` / `v3_ses.out`, `v3_airline_py.py` / `v3_airline_py.out`, `v3_remisiones.out`, `v3_varianza.out`, `v3_edita_comprobar.out`, `v3_reensamblado.out`,
`v3_verifica_todo.out`, `v3_verifica_bloques.out`, `v3_deck_cifras.out`; capturas en `diagnostico/cap4/capturas/v3/` (ignorada por git).
Servidores (8771, Chrome 9301) cerrados; `git status` no muestra nada nuevo fuera de `diagnostico/`.

---

## Qué hizo la sesión maestra (2026-11-22)

`diagnostico/cap4/comprobaciones/r3_ediciones_maestra.py`, 16 sustituciones únicas sobre las fuentes, aplicadas
**después** de `r3_edita.py` (por eso `r3_edita.py --comprobar` dice ahora que el árbol difiere; `r3_ediciones_maestra.py
--comprobar` da OK).

| Hallazgo | Qué se hizo |
|---|---|
| V1 | La frase de la deriva se restringe al ARIMA($0,1,0$): ahí es exactamente la media de las diferencias; se añade que en el ARIMA($1,1,1$) del Nilo no coinciden y que el Módulo 5 lo muestra. Sin cifra nueva |
| V2 | Las introducciones del M1, el M8 y el M10-TRM pasan a preguntas. Lo que daban va después de la actividad: en el M8, un párrafo tras la tabla («En $d = 2$ y $d = 3$ el $\hat\theta$ se clava en $-1$…»); en el M10, el $0.964$ abre la fila «Identificación de $d$» de la tabla del ciclo (el $\hat\rho_8 = -0.190$ y la banda ya estaban en la fila siguiente); en el M1, las respuestas están en la tabla del M8 y en el M3 |
| V3 | «coeficientes reales» → «coeficientes estimados» en el M8 |
| V4 | `auto.arima()` se presenta en su propia oración |
| V5 | «(Módulos 1 y 6)» |
| V6 | El recuadro del M4 remite a la trampa «del párrafo de arriba» y solo añade por qué no es un AR(1) |
| V7 | El bloque imprime `sd_resid` (salida regenerada en R 4.6.0) y la prosa dice «desviación típica $127.0$», sin $\hat\sigma$ |
| V8 | El $\alpha = 0.267$ se declara el implícito en el modelo; `ses()` estima el suyo (sin cifra nueva) |
| V9 | «El puente es un experimento…»; «ninguno de los dos intervalos queda corto» |
| V10 | Corregida la frase del informe del redactor (los minutos viven en `courseData`; la barra lateral no los pinta) |

**Al cerrar** (salidas `r3_maestra_*`): `verifica_todo.py` 11 en verde; bloques 822/822 (14 de R, 11 de Python);
`ensambla_cap4.py` dos veces, md5 `02edfaf7…` las dos; caps. 5 y 6 idénticos a HEAD; minutos medidos frente a declarados,
distancia máxima 0.5 (M1 10.5/11, M8 11.0/11, M9 14.4/14, M10 43.1/43 abierto); `r3_revisa.js` por HTTP a 1200 y 375 px:
0 errores o avisos de consola, 0 `.katex-error`, 0 desbordes, 0 simuladores sin pintar.

**Cuenta final de D5–D7:** D5 cumplido (todas las introducciones de simulador del M1, M3, M4, M6, M8 y M10-TRM piden
hacer; los rótulos del selector del M9 quedan para la R5); D6 cumplido salvo el tamaño del M10 (3 560 palabras, 43 min),
que no baja sin partirlo; D7 cumplido.
