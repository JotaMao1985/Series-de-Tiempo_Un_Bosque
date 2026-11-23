# Capítulo 5 leído como estudiante · hilo narrativo y comprensión

Archivo leído: `Htmls_Series/capitulo-5-sarima.html` (árbol limpio en `f807b40`; los doce `<template id="module-N">` enteros y
en orden, líneas 3058–6279), más el JavaScript que genera lo que el estudiante ve en cada simulador (8464–9332: los catorce
`SIMULADORES[...]`, selectores, rótulos y textos de «lectura»), la tabla ordenable `TABLAS_RANKING['comparativa']` (9339),
la autoevaluación `AUTOEVALUACIONES['cap5']` (9365–9564: enunciados, opciones, pistas y retroalimentación), la forma y las
doce preguntas del simulacro (`SIMULACROS['cap5-simulacro']`, 9974 en adelante) y los minutos declarados en `courseData`
(6281–6296). Las líneas son del HTML final, no de `ensamblado/cap5/`. Para el empalme: el cierre del capítulo 4
(`capitulo-4-modelos-arima.html`, el puente al 5 en 6331–6466 y «Y en el Capítulo 5…» en 6858–6862, con su ciclo en 3207–3300),
las remisiones al 5 desde el capítulo 6 (2637, 2670, 2717, 2922, 3052, 3617, 3634–3636, 3970, 4053), las atribuciones del 5 a los
capítulos 1, 2 y 3 (comprobadas en el destino) y la tarjeta del 5 en `Htmls_Series/index.html` (741–774).
Lente: comprensión e hilo; no se juzga corrección técnica, fuentes ni diseño de gráficas. **No se renderizó la página ni se
ejecutó ningún simulador ni ningún bloque de código:** la lectura es del marcado y del JS (qué texto genera cada simulador, no
cómo se ve ni cómo responde). Cuando se dice que una cifra «no sale de ningún bloque» es una búsqueda de la cadena en los `<pre>`
(ver §3). No se editó nada fuera de `diagnostico/cap5/`.

Cómo se distingue lo medido de lo opinado: cada hallazgo lleva al final **(M)** si se comprobó con un recuento, un `grep`, la
lectura literal de dos líneas que se contradicen o la comparación con otro archivo, y **(O)** si es juicio de lector sobre dónde se
pierde alguien. Las cifras de carga salen de `diagnostico/cap5/diag/lector_carga.py` (copia de `r3_minutos.py` del capítulo 4, con la
lectura del simulacro en JSON y la posición del primer simulador y del primer bloque; salida en `lector_carga.out`, y la misma
medición sobre el capítulo 4 actual en `lector_carga_cap4.out`); las de términos, remisiones, notación, registro y voz, de
`lector_terminos.py`; las de «dicho pero no mostrado», de `lector_cifras.py`; las de la autoevaluación y del simulacro,
de `lector_quiz.py` y `lector_simulacro.py`; el tamaño de cada sección, de `lector_secciones.py`; las introducciones de simulador y
los párrafos largos, de `lector_intros.py`; y la densidad de cifras, de `lector_numeros.py` (con su versión del capítulo 4).

Etiquetas de la §2: **P** = pérdida de comprensión; **N** = dicho pero no mostrado (o mostrado donde no puede reproducirse);
**D** = decoración, ruido o repetición; **C** = carga.

Qué trae el estudiante: viene del capítulo 4 ya revisado. Sabe ARIMA con `d`, el ciclo de Box–Jenkins de cuatro etapas
(identificación, estimación, diagnóstico, uso), la regla de la varianza mínima y por qué falla (`log(lynx)`), la firma de la
sobrediferenciación (θ̂ pegado a −1), AICc con `n*` y por qué no cruza la frontera de `d`, Ljung–Box con `fitdf`, los pesos ψ y
el intervalo `σ_h² = σ² Σ ψ_j²`, el Nilo y la TRM (ARIMA(0,1,0)), y **el puente al 5 ya dado con código** (cap. 4, 6331–6466: el mejor
ARIMA no estacional sobre `log(AirPassengers)` es un ARIMA(0,1,5), ρ̂₁₂ = 0,7245, Q(24) = 222,4, y el *airline* como «avance» con
ρ̂₁₂ = −0,0515 y p = 0,233). Del 2 trae ADF/KPSS, `ndiffs()`/`nsdiffs()`, ∇ y ∇₁₂ (cap. 2, 3150) y Box–Cox; del 3, la tabla de
identificación ACF/PACF, la fórmula de Ljung–Box, AICc/BIC y el AR(2) de las manchas con «0 de 20 barras fuera de banda» (cap. 3,
5757); del 1, STL. **No trae:** «ETS» (0 líneas en los capítulos 1–4; el 4 sí presenta el suavizamiento exponencial simple, 2914, y lo da como IMA(1,1),
2931, pero no el esquema error–tendencia–estación ni Holt–Winters), «naïve estacional» (0 líneas en 1–4; 61 en el 6), RMSE/MAE/MAPE como
medidas, «fuera de muestra» como procedimiento, «origen móvil», `USAccDeaths`, `co2`.

---

## 1. Mapa del arco

| Mód. | Pregunta que abre | Con qué cierra | Transición de entrada | Declarado | Medido (cerrado / abierto) |
|---|---|---|---|---|---|
| M1 · 5.1 La firma de la estacionalidad (3058–3238) | ¿Dónde se ve la estacionalidad, y cuándo no está? | «Lo que falta es el lenguaje para escribirla, y de eso va el módulo siguiente» (3232–3235) | ✓ «El Capítulo 4 terminó con un fracaso deliberado» (3076) | 14 | 8,7 |
| M2 · 5.2 Notación SARIMA (3240–3754) | ¿Qué significa multiplicar los polinomios? | Termina en un bloque de código (3752); **sin cierre** | débil: abre con «La idea es de una economía notable» (3259), sin recoger el cierre del M1 | 12 | **20,1** |
| M3 · 5.3 Diferenciación estacional (3756–4212) | ¿Cuántas diferencias y en qué orden se deciden? | Termina en una advertencia («Trampa de versión», 4202–4210); **sin cierre** | ninguna: abre con la definición de ∇ₘ (3774) | 16 | **19,3** |
| M4 · 5.4 Identificar los órdenes (4214–4507) | ¿Cómo se leen P y Q, y qué no se cuenta? | Termina en un bloque de código (4505); **sin cierre** | «no hay teoría nueva que aprender» (4232); no nombra el M3 | 16 | 11,0 |
| M5 · 5.5 El modelo *airline* (4509–4622) | ¿Por qué aparece en todas partes y qué le hace a la incertidumbre? | Nota «Frontera con el Capítulo 4» (4615–4620): mira atrás, no adelante | ninguna: abre con la caja de definición (4527) | 14 | **5,1** |
| M6 · 5.6 Estimar, comparar, diagnosticar (4624–4792) | ¿Qué cambia al estimar y comparar con estacionalidad? | Termina en el aviso R/Python (4780–4790); **sin cierre** | ✓ «La estimación no cambia… Lo que cambian son dos hábitos» (4642) | 16 | 8,2 |
| M7 · 5.7 Caso completo (4794–5075) | ¿Funciona el ciclo entero sobre una serie? | Termina en un bloque de código; **sin cierre** | implícita: sus «Etapas» 1–5 repiten las del ciclo del M4 sin decirlo | 21 | 11,1 |
| M8 · 5.8 Segundo caso y contraejemplo (5077–5279) | ¿Qué pasa cuando las pruebas engañan o no hay estación? | Termina en un bloque de código; **sin cierre** | ✓ el objetivo dice «Repetir el recorrido» (5089) | 16 | 8,3 |
| M9 · 5.9 Calendario y SARIMAX (5281–5477) | ¿Qué no puede absorber la estacionalidad? | Termina en un bloque de código; **sin cierre** | ninguna: salta de «descartar la estacionalidad» a «efectos de calendario» (5299) | 14 | 8,4 |
| M10 · 5.10 Cuando m es grande (5479–5688) | ¿Dónde deja de servir el SARIMA? | Termina en un bloque de código; **sin cierre** | ✓ «Todo lo anterior descansa en que m = 12 sea pequeño» (5497) | 16 | 9,1 |
| M11 · 5.11 Panorama y cierre (5690–6195) | ¿Por qué una sola partición no decide? | «Lo que viene» (6188–6193) | ✓ «el Módulo 10 acaba de mostrar…» (5710) | 20 | 13,6 / 22,7 (+16,5 de autoevaluación) |
| M12 · 5.12 Simulacro (6197–6279) | ¿Salen solas las cuentas y las decisiones? | Nota «Cómo aprovecharlo» (6258–6277) | ✓ «Este módulo no añade contenido: es un ensayo» (6218) | 50 (el reloj del ensayo) | 3,2 de lectura |

Declarado: 225 min (175 en M1–M11). Medido de lectura cerrada en M1–M11: 122,9 min; de lectura abierta (con pista y solución de
los tres ejercicios): 132,0; más 16,5 de leer enunciados, opciones y retros de la autoevaluación. El reparto no es razonable (ver §4). (M)

### Lectura del arco

El capítulo se cuenta en cuatro tramos que el lector percibe: **ver y escribir** (M1–M2), **decidir cada pieza** (M3 las diferencias,
M4 los órdenes, M5 el modelo que resulta, M6 estimar y comparar), **recorrer el ciclo** (M7 el caso, M8 el contraejemplo) y **ampliar
y cerrar** (M9 calendario, M10 `m` grande, M11 comparar con otras familias). Es un arco firme y su hilo es uno solo: **el *airline*
que cierra el problema del Capítulo 4** (el ARIMA(0,1,5) con ρ̂₁₂ = 0,7245). Se planta en el M1 (3076–3081), se construye en el M2 (el
polinomio que multiplica y el satélite), el M3 (las dos diferencias), el M4 (la tabla de identificación) y el M5 (su nombre y su
abanico en escalones), se estima en el M6, se cierra en el M7 («El problema del Capítulo 4, cerrado», 4932–4940) y se pone a prueba
en el M8 (otra serie con los mismos coeficientes; una serie sin estación) y el M11 (queda cuarto en una partición, primero en 61
orígenes). Es el mejor recurso del capítulo.

Donde el hilo afloja:

- **Solo dos de los once módulos de contenido cierran apuntando al siguiente** (el M1 y el M11). M2 a M10 terminan en un bloque
  de código o en un cuadro de advertencia, sin una frase que diga qué sigue ni para qué; el estudiante pasa de «cómo se escribe en
  la práctica» (M2) a «diferenciación estacional» (M3), de «el diagnóstico de la TRM» (M8) a «regresores de calendario» (M9) y de
  ahí a «Fourier y STL» (M10) sin puente. El capítulo 4 actual cierra con esa frase cada uno de sus módulos 1 a 9 (comprobado: «El módulo siguiente…», «el Módulo 4 identifica…», «De eso se ocupa el Módulo 8…») y el 10 con el puente al 5. (M)
- **El M11 hace cuatro cosas** (su objetivo dice dos): la comparación de ocho métodos y la de 61 orígenes, la tabla de alternativas
  modernas, el resumen, y la práctica de todo el capítulo (autoevaluación de ocho preguntas, tres ejercicios con 144 líneas de R, el
  libro de Excel). 1 899 palabras de prosa (2 469 abiertas), cinco tablas, y ningún bloque de código antes de los ejercicios (el
  primero llega tras 1 590 palabras). (M)
- **La práctica llega toda en el M11, y repite lo ya dicho.** M1–M10 no piden nada al lector salvo mover deslizadores (0
  `ejercicio-guiado` y 0 `quiz`; el capítulo 4 actual trae un ejercicio guiado en cada uno de sus módulos 1 a 9 y tres en el 10, `lector_carga_cap4.out`); el ejercicio 2 es el truco de `ndiffs(USAccDeaths)` del M3 y del M8, y el ejercicio 3(a) es el
  bloque de la TRM del M8 copiado. La autoevaluación no tiene pregunta de los módulos 5, 7, 8 ni 10. (M)
- **El *airline* se usa mucho antes de definirse con nombre** (M1 3080; caja de definición en M5, 4527): lo salva que el capítulo 4 ya
  lo dio como avance. (M/O)

### Promesas: hechas, cumplidas, incumplidas

| # | Dónde se promete | Qué | ¿Se cumple? |
|---|---|---|---|
| 1 | Cap. 4, 6858–6862 y 6363–6371 | El puente: SARIMA «añade un segundo juego de polinomios»; el *airline* deja ρ̂₁₂ = −0,0515 y p = 0,233; «el Capítulo 5 enseña también a comprobar» que la TRM no tiene estación | **Sí** (M2, M6–M7, M8). |
| 2 | M1, 3079–3081 | «Al final del Módulo 5 el modelo *airline*… deja ρ̂₁₂ = −0,0515 y pasa Ljung–Box(24) con p = 0,233» | **No.** El M5 no contiene esas cifras (4509–4622, `grep`); aparecen por primera vez en el M6 (tabla 4684, bloque 4735 y 4745) y en el M7 (4891–4894). (M) |
| 3 | M1, 3155 | «El Módulo 8 vuelve sobre este caso» (la TRM con ρ̂₁₂ grande en niveles) | **Sí** (5129–5175). |
| 4 | M2, 3360–3361 | ∇∇₁₂ «del Módulo 3, que allí aparece como las cuatro esquinas del mismo cuadrado» | **Sí** (3906, 3918). |
| 5 | M2, 3520 y 3624 | «El Módulo 4 usa esto para identificar»; «vuelve sobre esta misma frontera desde el lado de la ACF» | **Sí** (4262–4298). |
| 6 | M2, 3681 | La diferencia de σ̂² entre R y Python es «el mismo reparto de grados de libertad que el Módulo 6 discute para el AIC» | **Parcial.** El M6 discute `nobs` y el prior difuso (4756–4789), no el divisor de σ̂². (O) |
| 7 | M4, 4321 | «el ciclo de Box–Jenkins del Capítulo 4 con dos etapas insertadas» | **Parcial.** El ciclo del 4 tiene cuatro etapas (3212–3237: identificación, estimación, diagnóstico, uso); el del 5 tiene cinco con otros nombres y sin «uso»: no se obtiene sumando dos. (M) |
| 8 | M4, 4298 | «El Módulo 2 lo tabula» (el error de la varianza factorizada, 33 % con φ = 0,9) | **Sí** (3608–3620). |
| 9 | M6, 4693–4694 | «en el Capítulo 3 los dos criterios [AICc y BIC] discrepaban sobre las manchas solares» | **No.** En la rejilla de manchas del capítulo 3 (tabla en 5708–5726; JSON `manchas/rejilla`) el mínimo de AICc (834,73) y el de BIC (847,12) son el mismo ARMA(2,1); con la raíz cuadrada, los dos son el AR(2) (cap. 3, 10646). La discrepancia AICc/BIC está en un ejercicio de otra serie (cap. 3, 4949). (M) |
| 10 | M6, 4658 | «el Capítulo 3 dejó el caso contrario, un modelo con 0 de 20 barras fuera de banda que Ljung–Box rechazaba igual» | **Sí** (cap. 3, 5757). |
| 11 | M7, 4814–4815 | «El Capítulo 2 dejó zanjado que AirPassengers pide logaritmo… y el rango relativo de la serie es 1,848» | **Parcial.** El 2 sí lo deja (3152, 3789); el 1,848 no está en el 2 ni en ningún bloque, y «rango relativo» no se define. (M) |
| 12 | M8, 5166 | ARIMA(0,1,0) para la TRM «es también la conclusión a la que llegó el Capítulo 4 por otro camino» | **Sí** (cap. 4, 5936–5958). |
| 13 | M9, 5372 | «en la comparación fuera de muestra del Módulo 11 sale *peor* que el *airline* desnudo (RMSE 45,48 frente a 43,18)» | **Sí** (5746–5748); pero RMSE y «fuera de muestra» no se han presentado todavía. (M) |
| 14 | M10, 5575 y 5592 | «Entre familias, solo fuera de muestra, que es el Módulo 11»; «el SARIMA sigue ganando» | **Sí**, pero solo en la segunda tabla del M11 (5767–5781); la primera (5737–5753) dice lo contrario. (M) |
| 15 | M11, 5867–5871 | «las cifras de la comparación de arriba… se pueden reproducir con el código del capítulo» | **No.** Ningún bloque contiene `ets(`, `snaive`, `tsCV`, ni la regresión armónica sobre la partición, ni los 61 orígenes (`grep` en los `<pre>`; solo `stlm` aparece, en el M10). El libro de Excel recalcula RMSE/MAE/MAPE de las 24 filas a partir de los pronósticos de R copiados como datos, y da los 61 orígenes como datos. (M) |
| 16 | M11, 5760 | «demostrarlo es la razón de ser del Capítulo 6» | **Sí, y el capítulo 6 lo cita** (3970: «el que citó el Módulo 11 del Capítulo 5»; 16,81 coincide). |
| 17 | M12, 6229–6231 | La decisión que se repite incluye «cómo se despeja el *airline* para pronosticar» | **No se enseña.** La única línea es «al despejar y_t sus términos cambian de signo» (3393); la pregunta 7 del simulacro pide el pronóstico puntual a mano con residuales (clave 561,07). (M) |
| 18 | Cap. 6, 3052 | «Esto explica el `biasadj` del Capítulo 5» | **No.** `biasadj` aparece 0 veces en el capítulo 5 (ni en markup ni en JS); la idea (exp del pronóstico = mediana) está en 4958–4963 y 5068–5071 sin ese nombre. (M) |
| 19 | Cap. 6, 3970, 4053, 2637, 2922 | 16,81 «citado en el Módulo 11»; «inicialización difusa… que el Capítulo 5 documentó»; «abanico escalonado»; «mapa mes × año y la ACF» | **Sí** (5773; 4756–4789; 4597–4613; 3105–3127). |

---

## 2. Dónde me pierdo, módulo por módulo

### M1 · La firma de la estacionalidad (3058–3238) · 667 palabras, 14 declarados, 8,7 medidos

- **P 3079–3081 · «Al final del Módulo 5…»** apunta a un módulo que no tiene esas cifras: están en el M6 (ver promesa 2). Quien las
  busca al terminar el M5 no las encuentra. (M)
- **P 3080, 3085–3089 · «el modelo *airline*, con solo dos parámetros»** y «ARIMA(0,1,5)», «Ljung–Box(24)» entran como sabidos. El capítulo
  4 dio el *airline* como avance, pero el M1 no lo recuerda (no escribe sus órdenes) y su caja de definición está 1 447 líneas más
  abajo (4527). (M/O)
- **N 3138–3146 · la tabla de cinco series.** `USAccDeaths` y `co2` aparecen sin presentarse (se describen en 4549 y en 5912, a
  1 400 y 2 770 líneas), y los ρ̂ de sus filas no los calcula ningún bloque (el bloque solo hace `AirPassengers` y ∇TRM: 3164–3199);
  los de TRM en niveles (0,636; 0,490; 0,225) tampoco. Salen del JSON de precálculos. Además la tabla no enseña el contraste que
  importa: una serie estacional *ya sin tendencia*. La quinta fila es la TRM (que «no tiene nada»); ese contraste solo lo da el
  simulador. (M/O)
- **P 3109–3112 · «la ACF se queda con dos barras, en los rezagos 1 y 12»** frente a 4864–4872, que cuenta **tres barras más** fuera de
  banda en la misma serie (el 3, el 9 y el 23, con la banda ±0,171). Dos descripciones de la misma ACF que no coinciden (la de 4864 las llama «azar», pero el estudiante que mira el correlograma ve cinco barras, no dos). (M/O)
- **D 3195–3197 · comentario de código que avisa que «el cuarto decimal baila (−0.0024 aquí, −0.0025 en las tablas del capítulo)».**
  El capítulo reconoce, dentro del bloque que el estudiante ejecuta, que su propia tabla (M8, 5157) y su quiz (9390) no coinciden con
  lo que el bloque imprime (M8, 5224). Ruido de mantenimiento en la vista del estudiante. (M)
- **D/C 3180–3191 · 12 líneas de descarga de la TRM**, que reaparecen en R en el M8 (5204–5213) y en la solución del ejercicio 3 (6090–6099), y
  en Python en el M8 (5259–5265): tres copias en R y una en Python. (M)
- **Lo que sí encaja · 3231–3236, el cierre** es la excepción y funciona («Lo que este módulo deja montado… de eso va el módulo siguiente»).
- ∇ y ∇₁₂ se usan en la tabla (3145) y en los selectores del simulador sin recordar su definición; el estudiante la trae de los
  capítulos 2 y 4, y la de ∇ₘ llega en 3776. Se anota como detalle. (O)

### M2 · Notación SARIMA y el polinomio multiplicativo (3240–3754) · 1 459 palabras, 12 declarados, 20,1 medidos (1,68)

Es el módulo de lectura más larga de M1–M10 y el único de ellos que supera con mucho su tiempo: 3 bloques de código (163 líneas de
R y Python), dos simuladores, dos desarrollos plegados (329 palabras), 6 fórmulas en bloque y 138 en línea.

- **D 3331–3335, 3350–3358, 3364–3399, 3477–3521 · el satélite se explica cuatro veces antes de que el texto diga «aquí está lo único
  genuinamente nuevo» (3477).** La heladería lo hace con tres números (3331–3335), las viñetas lo repiten con ρ₁₁ = 0,4230 y ρ₁₃ = 0,4218
  (3355–3358), la derivación plegada lo hace en la parte MA (3364–3399) y la sección «Multiplicar no es sumar» lo vuelve a decir con los
  mismos ρ (3512–3514). «Satélite» aparece 16 veces en el módulo y 33 en el capítulo (M2 16, M4 5, M7 10, M11 1, M12 1). El ejemplo
  inventado es lo mejor del capítulo; las tres repeticiones siguientes son ruido. (M)
- **P 3386–3389 y 3588–3592 · el *airline* ajustado se usa antes de mostrarse.** La derivación plegada y la nota del γ₀ citan θ̂ = −0,4018
  y Θ̂ = −0,5569 y σ̂² = 0,001371; el ajuste se imprime 320 líneas después (3710–3715), en la última sección. La derivación remite además
  al «bloque de “Cómo se escribe en la práctica”» (3388), que llega al final del módulo. (M)
- **P 3634 y 3695–3708 · el primer `Arima(..., seasonal = list(order = …, period = 12))` del capítulo está en el bloque de «Momentos»
  (3634)**, y el comentario que explica por qué el período va en `seasonal` (3706) está 74 líneas después, en la sección que cierra el
  módulo. El objetivo del módulo dice «leer y escribir un SARIMA»: la sección que dice cómo se escribe en R y Python es la última (3695),
  440 líneas después de la definición. (M/O)
- **N 3582–3583 y 3588 · «2,300σ²» frente a «1,700σ²» y «1,5217σ²»** no salen de ningún bloque; tampoco 3 de las 4 filas de la tabla del peaje
  (3614–3617: φ = 0,6; 0,8; 0,95): el bloque calcula solo φ = 0,9 (15,406 frente a 10,320, 3652–3656). (M)
- **C/D 3538–3624 · «Media, varianza y autocorrelación»** (584 palabras y un bloque de 52 líneas en dos lenguajes) enseña a calcular γ₀ y su
  factorización; el resto del capítulo solo reutiliza que el *airline* factoriza exacto (ρ₁₁ = ρ₁₃ = ρ₁·ρ₁₂, en M4 y M7) y el M4 resume
  «para identificar, da igual; para calcular, no» (4294–4298). Está en el objetivo («calcular los momentos»), pero ninguna decisión
  posterior depende del peaje (la tabla de −0,3 % a −54,9 %). (O)
- **P 3681 · «el mismo reparto de grados de libertad que el Módulo 6 discute para el AIC»:** el M6 no discute el divisor de σ̂² (promesa 6).
- **N 3725–3726 · «La forma no multiplicativa se pediría con `fixed=`, y necesita 13 parámetros… Casi nunca compensa»:** una afirmación sin
  código ni cifra. (O)
- **Sin cierre:** termina en el bloque de 3752. (M)

### M3 · Diferenciación estacional (3756–4212) · 1 139 palabras, 16 declarados, 19,3 medidos (1,21)

- **P 4085–4088, 4099–4107, 4394, 5885 contra 4900–4904 · el criterio «raíz MA sobre el círculo» se enseña y 800 líneas después se
  desmiente.** El M3 presenta la columna |raíz MA|⁻¹ como firma de la sobrediferenciación estacional y su tabla da 0,9752 (D = 0), 0,9524
  (D = 1) y 0,9998 (D = 2); el ciclo del M4 («raíz MA sobre el círculo unitario», 4394) y el resumen (5885) la repiten; pero el M7
  dice que ese módulo inverso «no avisa… se acerca a 1 con casi cualquier Θ (con Θ = 0,1 ya vale 0,825)» y que «la invertibilidad se lee en Θ̂
  mismo». El simulador marca «⚠ sobrediferenciada» solo cuando |raíz|⁻¹ > 0,99 (8842), un umbral que ninguna línea de prosa da, y el
  estudiante ve en la tabla que el valor del modelo correcto (0,9524) y el del subdiferenciado (0,9752) están casi tan cerca de 1 como el
  del sobrediferenciado. (M)
- **D 4075–4080, 4125–4129, 4194–4198 · el truco de `ndiffs(USAccDeaths)` = 0 → 1 se cuenta aquí por primera vez** y se repite en el M8
  (5100–5106, 5187–5189, mismos KPSS 0,8672 y 0,0713), en el ejercicio 2 (6014–6024) y en la pregunta 4 de la autoevaluación (9436–9443):
  cuatro lugares. «Primero D, después d» aparece 7 veces en el marcado (M3 3, M4 1, M7 1, M8 1, M11 1). (M)
- **N 4203–4209 · «con `test = "ocsb"` devuelve 0»** sobre `log(AirPassengers)` y `USAccDeaths` no sale de ningún bloque del M3
  (el único `nsdiffs(uad)` del bloque, 4125, usa la prueba por defecto); el `ocsb` aparece en un bloque solo en el M8 (5216) y en el
  ejercicio 2 (6052). (M)
- **P 4208–4209 y 4827 · «aquí manda la evidencia del correlograma, no el número que devuelve la función»** y, tres módulos después, la
  tabla del M7 (4827) cita `nsdiffs()` = 1 como evidencia de `D` (la de la prueba por defecto) sin la salvedad. El módulo promete «decidir
  D y d con criterio» (3768) y deja el criterio de `D` repartido entre la varianza mínima, la ACF y dos pruebas que discrepan. (O)
- **N 3884–3885 · «su media va de 0,032 en 1958 a 0,201 en 1951»:** ninguna cifra de ese tipo sale de un bloque. (M)
- **P 4040–4041 · «concentrarla es incluso más fácil de ver después»** no se entiende (la frase sigue a «sube»); (O)
- **Sin cierre:** termina en el cuadro de «Trampa de versión». (M)

### M4 · Identificar los órdenes estacionales (4214–4507) · 1 074 palabras, 16 declarados, 11,0 medidos

- **N 4226–4227 y 4441–4505 · el módulo no identifica nada sobre datos.** El objetivo es «leer P y Q… con la misma tabla del Capítulo 3»;
  el bloque de código es `acf_sarima` (ACF teóricas de tres procesos), y el protocolo de cinco etapas (4319–4439) es un diagrama que el M7
  aplica después. La PACF no aparece con cifras en ningún módulo: el M7 identifica «q = 1» y «Q = 1» solo con la ACF (4836–4839) y
  nunca muestra que la PACF «decae» (lo que la tabla de 4239–4246 dice del SMA). (M/O)
- **P 4321 · «con dos etapas insertadas»:** el ciclo del 4 tiene 4 etapas y el del 5, 5 (promesa 7).
- **P 4428 · «La rejilla de candidatos solo se ordena por AICc si todos comparten d y D»** usa una palabra que el M6 presenta 222 líneas después
  (4650). (M)
- **P 4304 · «Empieza con todo en cero y sube solo Φ»:** el simulador arranca con Φ = 0,7 (8866: `params = { phi: 0, theta: 0, Phi: 0.7, Theta: 0 }`);
  la primera tarea es poner Φ a cero. (M)
- **P 4295 · «banda de ±2/√n»** frente a 1,96/√n en 3176, 4743 y 4983; el mismo objeto con dos constantes. (M)
- **N 4249–4251 y 4276 · 0,343 y −0,4412, y la fila AR(1)×SMA(1)** no salen de un bloque (el bloque imprime 0,7000, 0,4900 y no el 36). (M)
- **C 4319–4439 · el protocolo** son unas 450 palabras (con su párrafo de entrada), la mayoría escondidas en cinco pestañas, sobre las 1 074 del módulo; de los
  tres campos por etapa, «Qué te devuelve atrás» repite lo que dicen M3 y M6. La voz pasa a segunda persona («Qué haces», «te
  devuelve», 7 formas) igual que en el capítulo 4. (O)
- **Sin cierre:** termina en el bloque de código. (M)

### M5 · El modelo *airline* (4509–4622) · 383 palabras, 14 declarados, 5,1 medidos (0,37)

- **N 4580–4587 · el módulo que enseña la escalera de los ψ no tiene un solo bloque de código** (0 `<pre>`). Los números 0,5982, 1,0412,
  0,8632, σ₁ = 0,0370, σ₁₂ = 0,0823 y σ₂₄ = 0,1396 se reproducen por primera vez en el bloque del M7 (5026–5031), que imprime 1,0413 y 0,8633: **dos
  líneas del capítulo que no coinciden en la cuarta cifra** (4581 frente a 5029). «σ₁₂/σ₁ = 2,22» no sale de ningún bloque. (M)
- **N 4532, 4538, 4556 · «el SARIMA más usado del mundo», «deja estacionaria a casi cualquier serie mensual con tendencia y estación»,
  «el punto de partida razonable de casi cualquier serie mensual»:** el capítulo lo muestra con dos series (`AirPassengers`,
  `USAccDeaths`), mientras que su tercera serie (la TRM) no es estacional y su cuarta (`co2`, ejercicio 1) elige por AICc un
  (0,1,3)(0,1,1) (5963). (O)
- **D 4549 · `USAccDeaths` se describe aquí («Muertes accidentales en EE. UU., 1973–1978») y otra vez en el M8 (5097).** (M)
- **D 4602 · «que le acabamos de imponer»:** primera persona del plural en la introducción de un simulador. (M)
- **Sin cierre hacia delante:** el último cuadro («Frontera con el Capítulo 4», 4615–4620) apunta atrás; el M6 abre sin enlace con él. (M)
- El módulo más corto y el más ligero (la desviación del pronóstico en escalones es una idea limpia); declara 14 minutos y miden 5,1. (M)

### M6 · Estimar, comparar y diagnosticar (4624–4792) · 582 palabras, 16 declarados, 8,2 medidos

- **P 4693–4694 · atribución al capítulo 3 que no está** (promesa 9).
- **P · aquí aparecen por primera vez las cifras que el M1 promete para el M5** (promesa 2).
- **N 4688 · última fila de la tabla ((0,1,0)(0,1,0): AICc −434,80, BIC «—», Ljung–Box < 10⁻⁴)** no la imprime ningún bloque (el bloque
  muestra las cuatro primeras filas, 4721–4728) y el guion del BIC no se explica. (M)
- **N 4786–4788 · «Python alcanza ese mismo óptimo desde varios puntos de partida, con varios optimizadores»:** la evidencia no se muestra;
  la cifra −0,3924 solo se ve como comentario en el M8 (5254–5255). (M)
- **D 4756–4767 y 4780–4790 · el mismo aviso R/Python tres veces:** comentario del bloque (4756–4759), comentario siguiente (4767) y el
  cuadro de 125 palabras (el párrafo más largo del módulo). (M)
- **Sin cierre:** termina en el aviso R/Python. (M)

### M7 · Caso completo: log(AirPassengers) (4794–5075) · 1 098 palabras, 21 declarados, 11,1 medidos (0,53)

- **C 4812–4955 · el primer simulador llega tras 958 palabras** (el máximo de M1–M10; los otros, entre 222 y 556), 5 `<h3>`, 4 tablas y 98
  líneas de código. (M)
- **P 4836–4838 contra 4894 · dos bandas para la misma serie en el mismo módulo:** ±0,171 «que aquí se calcula con las 131 observaciones
  que quedan *después* de diferenciar, no con las 144» (4837–4838), y «dentro de ±0,163» para los residuales (4894; el bloque del M6 usa
  1,96/√144, 4743). El texto explica la primera y no la segunda. (M)
- **P 4900–4904 · el módulo inverso de las raíces MA «no avisa»** (ver M3): retracta lo que el M3 enseña.
- **N 4814–4815, 4865–4869 · «rango relativo 1,848»** (sin definición ni bloque; resulta ser (máx − mín)/media) y las barras 3, 9 y 23
  de la ACF (−0,202; 0,176; 0,223; en los residuales −0,125; 0,117; 0,220): el bloque imprime r₁₂, r₂₄ y los satélites 11 y 13, no estos. (M)
- **D 4906–4930 · «Los satélites, comprobados» está dentro de una caja de *definición*** que no define nada; es la cuarta vez que el
  capítulo dice que el satélite es exactamente ρ₁·ρ₁₂ en un *airline* (M2 3355–3358, M4 4285–4291, M7 4841–4862 y esta). (M)
- **D 4932–4940 · tercera vez** que se cuenta el ARIMA(0,1,5) con Q = 222,4 y ρ̂₁₂ = 0,7245 (cap. 4 puente, M1 3076–3081, aquí); la cifra
  Q = 222,4 no sale de ningún bloque del capítulo 5 (sí del capítulo 4). Cierra bien el hilo, pero el estudiante lleva siete apariciones de
  −0,0515 (M1, M6 ×2, M7 ×2, y en el 4, texto y bloque). (M)
- **P 4944–4949 · «el interruptor pasa de la escala logarítmica a la original»:** el simulador arranca en escala original (9027:
  `original: true`); los escalones del abanico solo se ven en logaritmos, es decir, después de apagar el interruptor. (M)
- **Lo que sí encaja:** sus «Etapas» 1–5 repiten, una por una, las del ciclo del M4 (4325–4439), y «Y los rezagos que sobran» (4864–4873) maneja
  con honestidad el rezago 23. Sería mejor decir en 4812 que es el ciclo del M4. (O)
- **Sin cierre:** termina en el bloque de código. (M)

### M8 · Segundo caso y contraejemplo (5077–5279) · 601 palabras, 16 declarados, 8,3 medidos

- **D 5100–5127 · «El resultado que hay que explicar»** presenta como nuevo el truco de `ndiffs(USAccDeaths)` y los KPSS en Python que el
  M3 ya dio (4075–4080, 4194–4198); la tabla de 16 casillas (5112–5118) solo tiene bloque para la TRM y `USAccDeaths`; `AirPassengers` y `co2`
  no (el de `co2` se ve en la solución del ejercicio 1, 5943). (M)
- **P 5164 contra 6065 y 9375 · «cuatro evidencias independientes»** (M8, y la retro de la pregunta 1) frente a «tres evidencias
  independientes» (ejercicio 3). Las dos últimas del M8 (t de Φ̂ = 0,01 y AICc forzado frente a simple) contrastan el mismo parámetro
  añadido; «independientes» se afirma y no se argumenta. (M cuenta; O la independencia)
- **N 5157 y 5158 · la tabla dice −0,0025 y t = 0,01; el bloque de 50 líneas más abajo imprime −0,0024 y 0,0147** (5224, 5231). (M)
- **N 5169–5175 · «Por qué una serie financiera… no tiene estación»:** el argumento (arbitraje, mercado eficiente, «el volumen… sí suele
  tener patrón») es una afirmación sin cifra ni referencia visible. (O)
- **Sin cierre:** el siguiente módulo (regresores de calendario) no se anuncia. (M)

### M9 · Regresores de calendario y SARIMAX (5281–5477) · 616 palabras, 14 declarados, 8,4 medidos

- **P 5299–5312 · «Hay dos clases de efectos de calendario»** y la tabla siguiente lista **cuatro** filas; la de «Días hábiles» nunca se construye
  (solo `log(días)` y Pascua) y la de «Fiestas fijas» dice «Ninguno». (M)
- **N 5366 · «que en estos 12 años cayó en marzo solo 2 veces y en abril las otras 10»:** el bloque imprime las fechas de Pascua de 1949 a 1952
  y `sum(es_pascua)` = 12 (5404–5410); el 2/10 solo está en la lectura del simulador (9213). (M)
- **N 5354 · BIC −475,35 y −476,83, y β̂ = 1,1157 (t = 2,39) del modelo con solo los días:** el bloque imprime el AICc de los tres modelos y el
  coeficiente del tercero (5417–5425); lo demás está en el JSON. (M)
- **P 5360–5364 · «es el que predice la aritmética… no se rechaza β = 1»** con e.e. 0,4462 (intervalo del 95 % ≈ 0,2 a 2,0): lo que el lector se
  lleva es que no rechazar confirma. La retro de la pregunta 7 lo dice con todas las letras («una confirmación fuerte», 9533). (O)
- **P 5371–5377 · la advertencia que desmiente el módulo** («el modelo con calendario sale *peor* fuera de muestra») usa RMSE y «fuera de muestra»,
  que el lector ve por primera vez aquí y que el M11 presenta 340 líneas después. Es honesta; el efecto es que el módulo termina de enseñar
  los regresores y a la vez dice que empeoran el pronóstico. (M/O)
- **P (simulador, JS 9165–9211) · al encender solo «Semana Santa»** la lectura dice «modelo: Semana Santa sola: no precalculada» y a la vez
  muestra AICc, BIC y los dos β̂ del modelo con días y Pascua (porque `clave` cae en `con_dias_pascua`). (M)
- **D 5396–5403 y 5445–5453 · el algoritmo de Pascua** (nueve líneas de aritmética entera, sin explicación) en R y en Python. (O)
- **P 5319 y 5529 · `n_t` para el proceso de errores**, mientras que `n` es el tamaño de muestra en todo el capítulo (28 usos). (M)
- **Sin cierre y sin enlace de entrada.** (M)

### M10 · Cuando m es grande: Fourier y STL (5479–5688) · 736 palabras, 16 declarados, 9,1 medidos

- **P 5497–5499 · «media horarios (m = 48 y m = 336 a la vez)»:** no se explica qué serie es ni de dónde salen 48 y 336. (M/O)
- **N 5624–5633 y todo el módulo · lo que se muestra con `m` grande son tres conteos con series simuladas** (104 observaciones; 6 columnas;
  ARIMA(0,0,0)(0,1,0)[365]). Ninguna regresión armónica ni STL se ajusta a una serie con `m` grande; todo lo demás se hace sobre
  `AirPassengers` (m = 12), donde el módulo mismo dice que gana el SARIMA (5591–5593). (M)
- **N 5554–5562 · la columna «Parámetros totales» (8, 9, 11, 14, 15, 16)** no la imprime el bloque y no se explica (incluye los del ARIMA de
  errores y σ²). (M)
- **N 5683 · «R da −542.95»:** el bloque de R imprime solo el orden del modelo (5636–5638). (M)
- **P 5540–5542 · la introducción del simulador dice el resultado** («hasta K = 4… hace falta llegar a K = 5»). (M)
- **N 5578–5585 · STL + ARIMA** son 173 palabras sin una cifra («admite cualquier m, tolera que el patrón cambie despacio y es rápido»; «su
  incertidumbre no incluye la del propio patrón estacional»). (O)
- **Sin cierre.** (M)

### M11 · Panorama comparativo y cierre (5690–6195) · 1 899 palabras (2 469 abiertas), 20 declarados, 13,6 / 22,7 medidos

- **P 5712–5716, 5743, 5749, 5750, 5832–5833 · ETS y «naïve estacional» se usan sin presentarse.** «El ETS, en las dos escalas» (5712) es la
  primera vez que el estudiante lee la sigla; la notación ETS(M,A,M) y ETS(M,A_d,M), y la columna `k` (16, 17, «2 + 11»), no se explican; «suavizamiento
  exponencial» y «Holt–Winters» aparecen solo en la tabla de 5832–5833 (el 4 dio el suavizamiento simple, no la estación). El capítulo 6 es quien usa ambas
  etiquetas con soltura (16 y 61 líneas). RMSE, MAE y MAPE tampoco se definen aquí. (M)
- **D 5718–5753 y 9306–9362 · la misma comparación se muestra tres veces seguidas:** la tabla ordenable (5718–5723: RMSE, MAE y MAPE de los
  ocho métodos), la lectura del simulador (9306–9315: el ranking por la métrica elegida, con los mismos números) y la tabla estática de 5737–5753
  (los mismos 8 × 3 números). (M)
- **P 5729, 9342–9344 y 9359–9361 · la sorpresa se estropea antes de la actividad.** El simulador pide «Antes de leer el párrafo siguiente,
  apunta cuál dirías que es el mejor método» (5729); la tabla ordenable que está encima ya dice, en su descripción y en su pie, que «las tres
  dejan al SARIMA cuarto», que «aun así es engañoso» y que «sobre 61 orígenes… el SARIMA pasa a primero». El párrafo siguiente («La tabla es
  demoledora… un lector razonable cerraría el capítulo concluyendo que el SARIMA no vale», 5755–5757) construye una sorpresa que el pie ya
  deshizo; la advertencia de 5759–5765 y la pregunta 8 la repiten. (M)
- **N 5755–5802 · el clímax del capítulo no tiene código.** Las dos tablas (8 métodos; 61 orígenes) y ~25 cifras de dos párrafos (el 3,4 % de 1958; 4,7 % y
  6,9 % pronosticados frente a 12,4 % y 11,2 %; 9,4/12,8 y 10,6/13,1; «14 orígenes… 12 entre 1957-05 y 1959-01»; 26,00/26,61/27,80/28,30; 49,0 %;
  18,22 frente a 15,96) salen de precálculos de R que no se muestran, y la nota de 5866–5871 afirma lo contrario (promesa 15). La afirmación central
  del capítulo («el SARIMA pasa de cuarto a primero») descansa en cifras que el estudiante no puede reproducir con lo que ve. (M)
- **P 5755 · «el modelo que ha ocupado once módulos»:** hay diez antes del 11. (M)
- **D 5866–5871 · «sería justo lo que este material lleva cinco capítulos enseñando a no hacer»:** comentario del autor sobre el propio material.
  Y la tabla de Prophet, LSTM y *Transformers* (5844–5859) llega sin presentar «las competencias M4 y M5» (5869). (O)
- **D · el puente al capítulo 6 se dice cuatro veces** (5760, 5805–5808, 5890, 6189–6192) más el pie de la tabla. (M)
- **N/D · práctica.**
  - Ejercicio 1 (5911–5986): su solución anticipa el ejercicio 3 («En el Ejercicio 3 los dos AICc quedan a dos puntos y ahí la lectura ingenua sí
    engaña», 5984). Sus líneas «round(178.2089 - 176.9982, 3)» (5968) restan dos números escritos a mano en el código. (M)
  - Ejercicio 2 (5988–6061): repite por cuarta vez el truco del M3; su pista dice «los operadores conmutan, así que ∇ y ∇₁₂ aplicados en cualquier orden dan
    la misma serie» (6003–6004), y la respuesta correcta a la primera pregunta del enunciado («¿Producen la misma serie diferenciada?») es que no: (a) llega a
    d = 0 y (b) a d = 1 (6029). (O)
  - Ejercicio 3 (6063–6151): la parte (a) es el bloque de la TRM del M8 copiado (6090–6121 frente a 5204–5239); en (b) `round(c(armonico_K4 = 180.200, …` (6138)
    escribe a mano la cifra que dice calcular, y «el p = 0,4081 del *airline*» (6147) no lo imprime ningún bloque. (M)
- **C · el módulo carga con** comparación, alternativas, resumen, autoevaluación (16,5 min de lectura), tres ejercicios (144 líneas de R), el libro de
  Excel (6153–6169), las lecturas y «Lo que viene». Declara 20 min; con la autoevaluación sumaría 39. (M)
- **Lo que sí encaja:** el resumen «Idea → Dónde queda» (5874–5893) mapea cada idea a sus módulos y es lo más útil de la segunda mitad; «Lo que viene»
  (6188–6193) cierra sobre el 6 sin añadir material. (O)

### M12 · Simulacro del quiz (6197–6279) · 568 palabras, 50 declarados (el reloj), 3,2 de lectura

- **P 6229–6231 · «cómo se despeja el *airline* para pronosticar»** figura entre las decisiones que «se repiten de una versión a otra», y la pregunta
  7 (N7: pronóstico puntual de enero con tres residuales y θΘ, clave 561,07) lo exige; el capítulo no lo enseña (promesa 17). La pregunta 5 (N5) pide el
  estadístico Q(24) de Ljung–Box con la fórmula n(n+2)Σ r²/(n−k), que sale del capítulo 3 (5612) y no se repite en el 5; el resto del simulacro sí cita los
  módulos que lo preparan (etiquetas `mód. 5.1 … 5.11`, los once). (M)
- **P 6222 y 6232 · «El quiz del capítulo 5 se presenta en Brightspace, en clase… antes de entrar»:** el texto no lleva fecha. Según la memoria del
  proyecto el quiz fue el 11 de noviembre; a hoy (23 de noviembre) el «antes de entrar» ya no se dice de algo futuro. No se puede comprobar desde el
  repositorio. (O)
- **D/P · 6258–6277 y 6246–6256 · voz:** segunda persona (9 formas: «Hazlo», «Teclea», «pulsa», «sales», «cierres»), como en el capítulo 4. (M)
- **Lo que sí encaja:** 12 preguntas, 6 de cifra y 6 de selección (6219–6221, 9974ss; `lector_simulacro.out`), 1 versión, con las 4 opciones de cada selección
  de tamaño parecido (la correcta es la más larga en 0 de 6; posiciones 3, 2, 4, 1, 3, 2), cada pregunta con su «cuenta» y sus rutas de error nombradas. (M)

---

## 3. Problemas transversales

### Lo que se usa antes de definirse

| Término | Primer uso | Presentación | Distancia |
|---|---|---|---|
| ETS, ETS(M,A,M), `k` | M11 5712 | ninguna (glosa parcial en 5832–5833; el cap. 4 solo da el suavizamiento exponencial simple, 2914; la sigla la usa el cap. 6) | — |
| «naïve estacional» | M11 5750 | ninguna (cap. 6) | — |
| RMSE / MAE / MAPE | M9 5373 | ninguna en el 5 (cap. 4 usa RMSE/MAE; cap. 6 las desarrolla) | — |
| «fuera de muestra» | M9 5372 | M11 5711 | 339 líneas |
| «rango relativo» (1,848) | M7 4815 | ninguna | — |
| *airline* (con nombre) | M1 3080 | M5 4527 (el cap. 4 ya lo dio como avance) | 1 447 líneas |
| `USAccDeaths` | M1 3142 | M5 4549 (y otra vez M8 5097) | 1 407 líneas |
| `co2` | M1 3143 | M11 5912 | 2 769 líneas |
| «rejilla» (de candidatos) | M4 4428 | M6 4650 | 222 líneas |
| `SARIMAX(...)` (la clase) | M2 3663 | M9 5318 | 1 655 líneas |
| Prophet, LSTM, *Transformers*, «competencias M4 y M5» | M11 5844–5869 | ninguna | — |
| «media horarios» (m = 48, 336) | M10 5498 | ninguna | — |

`lector_terminos.out` da la tabla completa. ∇ y ∇ₘ vienen de los capítulos 2 y 4 (cap. 4 2849: «∇ ≡ 1 − B»; cap. 2 3150: ∇₁₂); en el 5 se usan sin recordar
y solo ∇ₘ se redefine (3776). No se cuentan como defecto.

### Vocabulario y notación que cambian

- **Tamaño de muestra:** `n` en todo el capítulo (28 usos en fórmulas con `lector_terminos.py`, 0 de `T`; 39 y 0 con una búsqueda más laxa), como en el capítulo 4 (45 de `n`, 6 de `T`, con la
  búsqueda laxa); el capítulo 3 usa `T` (74 frente a 24). No hay aviso del cambio. Dentro del 5, `n_t` designa el proceso de errores en M9 y M10 (4 usos), y es el único choque. (M)
- **Autocorrelación muestral:** ρ̂ₖ en la prosa y las tablas (29 usos de `\hat\rho`) y `r_k` en el código, en la pregunta 5 del simulacro («r₁₂ = −0,0801») y en el
  capítulo 3 (Ljung–Box con r̂ₖ). Dos símbolos para el mismo objeto sin aviso. (M)
- **Banda:** ±2/√n (4295) y 1,96/√n (3176, 4743, 4983). (M)
- **«Evidencias», «pruebas»:** «cuatro evidencias» (M8, retro 9375), «tres evidencias» (ejercicio 3), y en el capítulo 4 «tres pruebas»; el M8 cuenta como evidencia el
  AICc forzado frente al simple, que no es una prueba. (M)
- **Modelo, serie, caso:** «el *airline*» (cursiva 39 veces, sin cursiva 14), «el SARIMA *airline*» en las tablas del M11, `auto.arima (elige el airline)`: sin
  ambigüedad, pero la tipografía varía. (M)
- **Cita de módulo:** «Módulo N» en la prosa (44) y «5.N» en títulos, etiquetas del simulacro y retros (31); en la portada, «Capítulo 5 · Módulo III» es el módulo del curso. (M/O)
- **Variantes léxicas:** «diferencia doble» / «doble diferencia» / «las dos diferencias»; «estacionalidad» (44) / «estación» (7); «peaje», «regalo»: metáforas bien elegidas (no
  se cuentan como defecto). (M)
- **Inglés sin traducir en la prosa:** *airline* (nombre propio), *naïve* (3), *forecasting* (títulos de lecturas), «brilla» (calco de *shines*, 5822 y 5869), «tuneo»
  (5846). Los títulos bilingües son una convención del curso. (M)
- **Registro:** «algo bonito» (5361), «de otro planeta» (5933), «demoledora» (5755): salen del tono del resto del capítulo; «de cabeza» (3294) es de uso corriente y no se cuenta. (M)

### Dicho pero no mostrado

`lector_cifras.py` revisa 64 grupos de cifras citadas en la prosa y busca su cadena en los `<pre>` de todos los módulos y en el JSON de precálculos. **32 de los 64 grupos
no salen de ningún bloque** (28 si se descuentan los cuatro que vienen del capítulo 4: ρ̂₁₂ = 0,7245, Q = 222,4, ψ∞ = 0,169, el 58 % de `lynx`); 22 de esos 32 están en el JSON
(es decir, se ven al mover un simulador, si el simulador las pinta, pero no se reproducen con el código del estudiante: la búsqueda por prefijo es floja con cadenas cortas,
por lo que esa columna se lee como «quizá»). Por módulo, sin código: M1 3 de 5, M2 3 de 5, M3 2 de 5, M4 3 de 5, M5 3 de 5, M6 1 de 4, M7 5 de 8, M8 0 de 6, M9 4 de 6, M10 0 de 3, M11 8 de 12. (M)
Los casos de más peso están en la §2: la escalera de ψ y los σ_h del M5; el 2,300σ² y la tabla del peaje del M2; las barras 3, 9 y 23 del M7; las dos tablas y los dos párrafos de cifras del
M11. El M8 y el M10 son los módulos que muestran lo que dicen. (M)

### Repeticiones (D)

- **El satélite:** 4 explicaciones en el M2, y de nuevo en M4 (4285–4291), M7 (4841–4862, 4906–4930), la pregunta 2 y la 4 del simulacro. 33 menciones. (M)
- **El truco `ndiffs(USAccDeaths)`** y «Primero D, después d»: M3, M8, ejercicio 2, pregunta 4. (M)
- **La TRM sin estación:** M1 (tabla y bloque de 12 líneas), M8 (simulador, tabla y bloque), ejercicio 3 (el bloque otra vez), pregunta 1 de la autoevaluación (que cita las
  cifras del M8). (M)
- **El diagnóstico del *airline*** (−0,0515; p = 0,2330): M1, M6 (tabla y bloque), M7 (tabla, nota y bloque), cap. 4 (puente). (M)
- **La comparación de ocho métodos:** tres veces en M11 (ver §2). (M)
- **El puente al capítulo 6:** cuatro veces en M11. (M)

### Introducciones de simulador

Cortas y con pocas cifras (de 39 a 95 palabras, 0 a 2 cifras, 787 palabras en 14 simuladores; `lector_intros.out`); el capítulo 4 actual tiene 29 a 146 palabras y 0 a 9 cifras (771 palabras en 11; `lector_intros_cap4.out`),
así que ninguna del 5 pasa de 95 palabras ni de 2 cifras. Las que adelantan el resultado: M3 `cuatro-combinaciones` («baja de 0,762 a… 0,841, es decir *sube*», 4038–4040), M6 `explorador-sarima` («el mínimo de AICc y el de BIC coinciden aquí», 4668–4669),
M10 `armonicos-K` («hasta K = 4… hace falta llegar a K = 5», 5540–5542) y M11 (la tabla de arriba, ver §2). Desajustes entre la introducción y el estado inicial del simulador: M4 (4304) y
M7 (4946); en M9 el interruptor de Pascua muestra datos de otro modelo. (M)

### Plegados

Cinco desarrollos plegados en tres módulos (739 palabras: M2 329, M3 262, M5 148). Ninguno carga con lo imprescindible, excepto el del M5 (la escalera de ψ y σ_h: 148 palabras que son *la*
explicación de la figura que el módulo anuncia). Los dos del M2 (el satélite en la parte MA y en la AR) son los de la repetición. (O)

### Convenios y avisos entre lenguajes

Menos ruido que en el 4: 13 líneas de aviso «R da X, Python Y» (M2 2, M3 1, M6 4, M7 2, M9 2, M10 2) más el cuadro de 4780–4790. Los tres ejercicios son solo de R; el estudiante que
trabaja en Python no tiene solución. (M/O)

### Voz

La prosa expositiva es impersonal en lo esencial. La segunda persona se concentra en las introducciones de simulador (los imperativos «Elige», «Mueve», «Prueba», «Empieza», «Lleva»: 26 formas
en M1–M6 y M10), el ciclo del M4 (7), los ejercicios (4) y el M12 (9). La primera persona del plural aparece en las derivaciones («Tomamos», «Multiplicamos», 3491, 3496; «Escribimos», 4567), en 4602 («acabamos
de imponer») y en 6191 («hemos construido»). (M)

---

## 4. Carga

Convenio y números: `diagnostico/cap5/diag/lector_carga.py` (la fórmula del capítulo 4: palabras de prosa / 180 + 3 por simulador + 2 por bloque de código, con un par R/Python como un
bloque; se quitan `<pre>`, scripts, canvas, botones, el pie de fuentes y la matemática en bloque; cada fórmula en línea es una palabra). «Cerrado» deja sin contar pista y solución;
«abierto» las cuenta; los plegados van aparte; los quizzes (JS) van aparte.

| Mód. | Palabras (cerrado) | `$$` | `$` | Cuadros | Tablas | Sim. | Bloques (líneas) | Plegado (palabras) | Cerrado (min) | Abierto (min) | Declarado | Razón abierto/declarado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 667 | 0 | 58 | 5 | 1 | 1 | 1 (62) | — | 8,7 | 8,7 | 14 | 0,62 |
| M2 | 1 459 | 6 | 138 | 8 | 2 | 2 | 3 (163) | 329 (2) | 20,1 | 20,1 | 12 | **1,68** |
| M3 | 1 139 | 2 | 134 | 6 | 3 | 3 | 2 (173) | 262 (2) | 19,3 | 19,3 | 16 | **1,21** |
| M4 | 1 074 | 0 | 130 | 4 | 2 | 1 | 1 (55) | — | 11,0 | 11,0 | 16 | 0,69 |
| M5 | 383 | 1 | 34 | 3 | 1 | 1 | 0 (0) | 148 (1) | **5,1** | 5,1 | 14 | **0,37** |
| M6 | 582 | 0 | 85 | 4 | 1 | 1 | 1 (70) | — | 8,2 | 8,2 | 16 | 0,51 |
| M7 | 1 098 | 4 | 142 | 7 | 4 | 1 | 1 (98) | — | 11,1 | 11,1 | 21 | 0,53 |
| M8 | 601 | 0 | 70 | 4 | 2 | 1 | 1 (91) | — | 8,3 | 8,3 | 16 | 0,52 |
| M9 | 616 | 1 | 54 | 5 | 2 | 1 | 1 (86) | — | 8,4 | 8,4 | 14 | 0,60 |
| M10 | 736 | 1 | 113 | 5 | 2 | 1 | 1 (81) | — | 9,1 | 9,1 | 16 | 0,57 |
| M11 | 1 899 (2 469 abierto) | 0 | 164 | 10 | 5 | 1 | 3 (144) | — | 13,6 | 22,7 | 20 | 1,14 (1,96 con autoevaluación) |
| M12 | 568 | 0 | 4 | 2 | 0 | 0 | 0 | — | 3,2 | 3,2 | 50 | (el ensayo) |
| **Total** | 10 822 (11 392) | 15 (+11 plegadas) | 1 126 | 63 | 25 | 14 | 15 | 739 | 126,1 | 135,3 | 225 | |

La autoevaluación (8 preguntas) pesa 16,5 min de lectura de enunciados, opciones, pistas y retros; el simulacro (12 preguntas), 16,5 (1 484 palabras de enunciado y opciones y 1 485 de
soluciones; la versión única, con el caso). Ninguna columna incluye el tiempo de hacer los ejercicios, contestar los cuestionarios ni ejecutar el código. (M)

**Comparación con el capítulo 4 actual (misma medición, `lector_carga_cap4.out`).** El 4 declara en M1–M10 186 min y mide 140,3 cerrado y 186,0 abierto: **calibrado** (razón
abierto/declarado de 0,97 a 1,03 en los diez módulos; el capítulo 4 se recalibró en su R3). El 5 declara en M1–M10 155 y mide 109,3 (0,71; **de 0,37 a 1,68 por módulo**), y en M1–M11 declara 175 y mide
132,0 abiertos (0,75; 0,85 con la autoevaluación). Con la convención del capítulo 4 (declarado = minutos de lectura abierta) los declarados saldrían: M1 9, M2 20, M3 19, M4 11, M5 5, M6 8, M7 11,
M8 8, M9 8, M10 9, M11 23 (39 con la autoevaluación) y el simulacro, 50 (el reloj). (M)

**El capítulo 5 es más ligero que el 4 en fórmulas, en cifras y en párrafos largos.** 15 fórmulas en bloque (más 11 plegadas) frente a 35 (más 11); 4,8 cifras por 100 palabras de
prosa frente a 6,7 del 4 (`lector_numeros.out`, `lector_numeros_cap4.out`); seis párrafos de más de 120 palabras frente a 21 (el más largo, 170 frente a 249). Pero tiene más tablas (25 frente a 13), más
simuladores (14 frente a 11) y módulos más desiguales: de 383 palabras (M5) a 1 899 (M11). La carga del 5 no está en la matemática de cada módulo sino en tres sitios: el M2, el M3 y el M11. (M/O)

### Qué se desbalancea

- **M2 pesa 1,68 veces lo declarado y M3, 1,21.** Son los dos módulos que enseñan la notación y las diferencias; el M2 llega a 20 min de lectura con una sola idea nueva (el
  satélite) repetida cuatro veces y una subsección de momentos que el resto del capítulo no usa. (M/O)
- **M5, M6, M7, M8, M9 y M10 miden entre 0,37 y 0,60 de lo declarado.** Son módulos de un simulador y un bloque; la lectura de una salida de R o de un ejercicio en el simulador cuesta más
  y no se mide, pero el capítulo 4 usa la misma fórmula y sale en 1,0. El M5 declara 14 y mide 5,1. (M)
- **M11 pesa 1,14 abierto y 1,96 con la autoevaluación**, y es el módulo con más cosas distintas (§2). (M)
- **El primer simulador del M7 llega tras 958 palabras** (en los demás, entre 175 y 556); el primer bloque del M4 tras 1 074. (M)

### Dónde partiría o movería (sin renumerar; de mayor a menor rendimiento)

1. **Declarar lo medido** (convención del 4): M1 9, M2 20, M3 19, M4 11, M5 5, M6 8, M7 11, M8 8, M9 8, M10 9, M11 23 + 16 de la autoevaluación (o un tiempo para el módulo y otro para el
   cuestionario). No cuesta nada.
2. **Corregir cuatro remisiones:** M1 3080 («Al final del Módulo 5» → el M6/M7), M6 4693–4694 (quitar la frase de las manchas solares o llevarla al ejercicio del capítulo 3 donde sí
   ocurre), M11 5867–5871 (decir que las cifras son precálculos, o dar el código en el capítulo 6) y la remisión al `biasadj` del capítulo 6 (3052; nombrar `biasadj` en 4958–4963).
3. **Cerrar cada módulo con una frase que apunte al siguiente** (M2–M10), como el 4 y como el M1.
4. **M11: separar** la comparación (con una sola tabla; quitar la ordenable o la estática; sin pie que revele) del resumen y la práctica; presentar ETS, «naïve estacional» y RMSE/MAE/MAPE en una
   línea cada uno; o hacer del M11 «Comparar» y de la práctica un módulo aparte, como hace el 4 con el simulacro.
5. **Mostrar lo que se dice:** código para la escalera de ψ y los σ_h dentro del M5 (hoy está en el M7); las barras 3, 9 y 23 y los residuales en el bloque del M7; un bloque de 10 líneas para la
   comparación de la partición (ETS, `snaive`, armónica) o declarar «precalculado» donde la cifra sale de un JSON.
6. **M2: recortar** a una explicación del satélite (la de la heladería) más una derivación, mover «Cómo se escribe en la práctica» justo tras la definición y decidir si el peaje (la tabla de φ) se queda.
7. **Reconciliar el criterio de la raíz MA** (M3 4085–4107, 4394, 5885 frente a M7 4900–4904): enseñar Θ̂ → −1 y su e.e. como firma y dejar la columna |raíz|⁻¹ como caso de contraste, o dar el umbral del simulador.
8. **Práctica:** preguntas para M5, M7, M8 y M10 en la autoevaluación (hoy 0); sustituir el ejercicio 2 (cuarta repetición del truco) por una serie nueva; quitar de la solución del ejercicio 1 la
   anticipación del 3; que las cifras de los ejercicios salgan del código y no estén escritas a mano (`180.200`, `178.2089`).
9. **M4/M7:** una identificación sobre datos, con la PACF a la vista, en el M4 o en la «Etapa 4» del M7; decir en 4812 que las etapas del M7 son las del ciclo del M4.
10. **Pulir:** `n_t` → otro símbolo; ±2/√n → 1,96/√n; r_k → ρ̂ₖ en el simulacro; «once módulos» → «diez»; «media horarios»; los tres bloques de descarga de la TRM en uno.

---

## 5. Empalme con el capítulo 4, con el 6 y con la portada

### Lo que el cap. 5 supone del 4, y si el 4 lo da

| El cap. 5 supone… | ¿Lo da el cap. 4? |
|---|---|
| El problema abierto: ARIMA(0,1,5), ρ̂₁₂ = 0,7245, ρ̂₂₄ = 0,6727, Q(24) = 222,4 (3076–3079, 4933–4935) | **Sí**, con código (cap. 4, 6392–6440). |
| El *airline* como avance: ρ̂₁₂ = −0,0515, p = 0,233 (3079–3081, 4936) | **Sí**, con código (cap. 4, 6426–6430). |
| La regla de la varianza mínima y su fallo con `lynx` (58 %) (4067–4070, 4111–4112) | **Sí** (cap. 4, 5128). |
| La firma de la sobrediferenciación (θ̂ pegado a −1, raíz sobre el círculo) (4086–4088) | **Sí** (cap. 4 M8). |
| AICc no comparable entre distintos `d` (4646, 5570) | **Sí** (cap. 4 M6; y el puente, 6381–6384). |
| `σ_h² = σ² Σψ_j²` (3564, 4586) y ψ∞ = 0,169 del Nilo (4593) | **Sí** (cap. 4 M9). |
| «la TRM… ARIMA(0,1,0)» (5164–5166) | **Sí** (cap. 4, 5936–5958). |
| `nobs` frente al `n` efectivo de statsmodels (4784) | **Sí** (cap. 4 M6). |
| «El ciclo de Box–Jenkins del Capítulo 4 con dos etapas insertadas» (4321) | **Parcial:** 4 etapas frente a 5 (promesa 7). |
| El *airline* con su nombre y su fórmula | **Parcial:** el 4 lo da como «avance» (6363–6371); el 5 lo define en el M5 (4527). |
| ETS como familia (5712, 5743, 5832) | **No:** el 4 presenta el suavizamiento exponencial simple y lo da como IMA(1,1) (cap. 4, 2914, 2931), pero «ETS», la notación (M,A,M) y Holt–Winters no aparecen. |

El empalme de entrada funciona: el cierre del 4 («el modelo *airline*… Con solo esos dos parámetros alcanza los rezagos 1, 12 y 13, deja ρ̂₁₂ = −0,0515 y pasa Ljung–Box(24) con p = 0,233»)
se cumple al pie de la letra en el M6 y el M7. Lo que se pierde es la fuente de la promesa: el M1 cita el *airline* como un resultado propio del capítulo («Al final del Módulo 5…») y repite casi textualmente
el cierre del 4 en lugar de apoyarse en él. (M)

### Lo que el 6 toma del 5

El 6 abre diciendo que «el Capítulo 5 lo usó para dibujar el abanico escalonado» (2637; ✓ M5, M7), cita la rejilla de 36 modelos (3617; ✓ M6), el 16,81 «que citó el Módulo 11 del Capítulo 5» (3970; ✓ 5773),
el 43,18 del *airline* sobre el bloque nuevo (3636; ✓ 5746), la inicialización difusa de statsmodels (4053; ✓ M6), el mapa mes × año y la ACF (2922; ✓ M1) y la cuarta posición sobre 24 meses (2717; ✓ M11).
**Una remisión no se cumple:** «Esto explica el `biasadj` del Capítulo 5» (3052): el 5 no nombra `biasadj`. (M)

### La tarjeta de la portada (`Htmls_Series/index.html`, 741–774)

Texto: «La firma de la estacionalidad en la ACF, notación SARIMA(p,d,q)(P,D,Q)ₘ y su polinomio multiplicativo, diferenciación estacional, el modelo *airline*, regresores de calendario y SARIMAX, y qué hacer cuando
el periodo es grande: términos de Fourier y STL.» Etiquetas: «Semanas 10–11», «Capítulo 5 · Módulo III», «12 módulos · 14 simuladores», y «Clase 1» (módulos 1 a 5, `#1`) y «Clase 2» (módulos 6 a 11, `#45`).

- **Cifras:** 12 módulos y 14 simuladores son correctas (14 `data-simulador` de simulador; el simulacro es el otro). (M)
- **Lo que el capítulo más desarrolla y la tarjeta no nombra:** el problema que cierra (el ARIMA(0,1,5) del 4), la TRM como contraejemplo, el criterio de comparación entre familias y la comparación
  de una partición con 61 orígenes. La tarjeta lista el temario, no el argumento. (O)
- **«Módulo III»:** en la portada es el módulo del curso; dentro del capítulo, «Módulo 3» es 5.3. Dos niveles con el mismo nombre. (O)
- Las diapositivas (`diapositivas/capitulo-5-sarima.html`) no se leyeron.

---

## 6. Lo que funciona (no romper al revisar)

1. **El ejemplo inventado de la heladería (3280–3362) y el de la tienda (3818–3889).** Números que se comprueban de cabeza, un simulador y un bloque de código cada uno, y la imagen de «cada diferencia es
   una dirección de resta» (3841–3852). Es lo que más se aprende leyéndolo.
2. **M1 3076–3103 y 3150–3156 · «Verla antes de medirla» y «La trampa de la tabla»:** arranca del fallo del capítulo 4, enseña el mapa y la regla de las dos condiciones, y la advertencia sobre la TRM
   en niveles prepara el contraejemplo del M8.
3. **M3 4074–4080 · «Los operadores conmutan; las pruebas no»:** una frase que ordena todo el módulo.
4. **M5 4558–4613 · la escalera de ψ y σ_h** con su simulador: la idea más limpia de la segunda mitad.
5. **M7 · «Etapas 1 a 5» y «Y los rezagos que sobran» (4864–4873):** recorrido honesto, con el rezago 23 que sobrevive y con la razón para no perseguirlo.
6. **M8 5136–5162 · el contraejemplo de la TRM** (simulador lado a lado y cuatro evidencias) y su remate de mercado (5169–5175, aunque sin cifra).
7. **M10 5567–5576 · «La trampa de esta tabla»** (AICc entre familias) y **M11 5787–5795** (el corte justo después del año en que no creció): explicaciones que cierran de verdad el hilo.
8. **M11 5874–5893 · el resumen «Idea → Dónde queda»** y **6188–6193 · «Lo que viene»**.
9. **Las introducciones de simulador son cortas** (39 a 95 palabras, 0 a 2 cifras; las del 4 llegan a 146 y a 9 cifras) y los párrafos largos son pocos (6 de más de 120 palabras frente a 21 del 4).
10. **El simulacro:** opciones sin sesgo de tamaño, cuenta paso a paso, rutas de error nombradas y módulo de referencia en cada pregunta; **M12 6218** «Este módulo no añade contenido: es un ensayo».
11. **El cierre del M1 (3231–3236)** y **la apertura del M10 (5497)** y **del M11 (5710)**: transiciones que dicen de dónde se viene y adónde se va.
12. **Cada módulo trae su «Objetivo» (12 de 12)** y cada uno se corresponde con su contenido.
13. **Los empalmes con el 4, el 6 y las atribuciones al 2 y al 3** salvo las cuatro remisiones de la §1.

---

## 7. Los diez problemas que más dañan la comprensión (orden de daño)

1. **El M11 hace cuatro cosas, usa sin presentar ETS/«naïve estacional»/RMSE y muestra tres veces la misma comparación con un pie que ya revela el resultado**; su clímax («el SARIMA pasa de cuarto a primero»)
   descansa en dos tablas y en ~25 cifras de prosa sin código, y la nota de 5866–5871 afirma que se pueden reproducir con el código del capítulo. 1 899 palabras (2 469 abiertas) + 16,5 min de autoevaluación + 144 líneas
   de R de ejercicios; declarado 20. (M)
2. **Los minutos declarados no están medidos:** M2 1,68 y M3 1,21 por encima de lo declarado; M5 0,37 y M6–M10 de 0,51 a 0,60 por debajo; M1–M10 declaran 155 y miden 109,3 (0,71), cuando el capítulo 4, con la misma
   fórmula, sale en 1,0 por módulo. (M)
3. **Solo el M1 y el M11 cierran apuntando al módulo siguiente;** M2 a M10 terminan en un bloque o en una advertencia, y varios abren sin recoger el anterior (M2, M3, M5, M9). El hilo del *airline* que une
   todo el capítulo se narra al principio (M1) y al final (M7), no entre medias. (M)
4. **Cuatro remisiones a otros módulos o capítulos no se cumplen** (M1 3080 → M5; M6 4693 → manchas solares del cap. 3; M11 5870 → «código del capítulo»; cap. 6 3052 → `biasadj` del 5), y una tercera
   cuenta («dos etapas insertadas», 4321) no cuadra con el ciclo del 4. (M)
5. **El criterio «raíz MA sobre el círculo» se enseña en el M3 (y en el ciclo y el resumen) y el M7 lo desmiente 800 líneas después;** el umbral que usa el simulador (0,99) no está en ninguna línea de prosa. (M)
6. **La práctica llega toda al final y repite lo dicho:** M1–M10 no piden nada; la autoevaluación no toca los módulos 5, 7, 8 ni 10 (y la correcta es la opción más larga en las cinco de opción única); el ejercicio 2
   repite por cuarta vez el truco de `ndiffs`, el 3(a) es el bloque del M8, el 1 anticipa el 3, y dos cifras de los bloques están escritas a mano. El simulacro pide a mano el pronóstico del *airline* y el estadístico de
   Ljung–Box, que el capítulo no enseña. (M)
7. **El M2 explica cuatro veces el satélite y suma una subsección de momentos que nada posterior usa;** el *airline* ajustado se usa 320 líneas antes de mostrarse, y la sección «Cómo se escribe en la práctica»
   (el objetivo del módulo) es la última. (M/O)
8. **El M5, el módulo que define el *airline* y su escalera de ψ, no tiene código;** sus cifras llegan en el M7 con una diferencia en la cuarta cifra (1,0412 frente a 1,0413). (M)
9. **Cifras de la prosa sin bloque:** 32 de 64 grupos revisados (M1 3 de 5, M7 5 de 8, M11 8 de 12); y dos pares de cifras que no coinciden entre el texto y el bloque (−0,0025/−0,0024 en M8 y M1; 0,0147/0,01).
   El comentario que lo reconoce está dentro del bloque del M1 (3195–3197). (M)
10. **El mismo objeto con dos símbolos o dos constantes:** `n_t` frente a `n`; ρ̂ₖ frente a r_k; ±2/√n frente a 1,96/√n; dos bandas para la misma serie en el M7 (±0,171 y ±0,163), «dos clases» de efectos de calendario con
    cuatro filas, y «tres» frente a «cuatro» evidencias para la TRM. (M)

---

## 8. Lo que no se pudo comprobar

- **No se renderizó la página ni se ejecutó ningún simulador:** el texto de cada «lectura» y de cada selector se leyó en el JS (8464–9332). No se sabe cómo se ve cada gráfica ni cómo responde cada deslizador; sí se
  leyeron los `params` iniciales y las dos discrepancias con las introducciones (M4 `Φ = 0,7`; M7 `original: true`) y el caso del interruptor de Pascua (9165–9211).
- **No se ejecutó R ni Python:** «cifra sin bloque» es una búsqueda de la cadena en los `<pre>` (y, por prefijo, en el JSON de precálculos). Una cifra que el código calcula y no imprime sale como «sin bloque»;
  la columna «está en el JSON» es floja con cadenas cortas (3,4; 8,2; 0,125) y se lee como «quizá». No se verificó que los números del JSON sean los que el código del estudiante reproduciría.
- **La fórmula de minutos (180 palabras/min, +3 por simulador, +2 por bloque) es la del curso,** no una medición con lectores: es un suelo para los módulos con derivaciones y un techo para los de prosa corta; no
  incluye hacer los ejercicios, contestar los cuestionarios ni ejecutar el código. El capítulo 4 declara con esa fórmula y sale calibrado; que el 5 se haya declarado con otra regla (por ejemplo, tiempo de estudio
  guiado) no se puede saber desde el repositorio.
- **La fecha del quiz del capítulo 5:** el texto del M12 no la da; que ya se aplicó el 11 de noviembre figura solo en la memoria del proyecto, no en el repositorio.
- **Corrección técnica, fuentes y diseño de gráficas** quedan fuera de este lente; las únicas observaciones de ese tipo son inconsistencias entre dos líneas del propio texto (1,0412 y 1,0413; −0,0025 y −0,0024; ±0,171 y ±0,163),
  la inferencia «no se rechaza β = 1 ⇒ confirmación» (5361–5364, 9533) y las dos atribuciones a otros capítulos comprobadas en el destino (manchas solares; `biasadj`).
- **El libro de Excel** (`ejercicios/capitulo-5-sarima-solucion.xlsx`) se leyó solo en la hoja «M11 Métricas» (que recalcula RMSE/MAE/MAPE desde los pronósticos de R y da los 61 orígenes como datos); el resto de sus hojas
  y la afirmación de 6159–6161 («Cada resultado trae una comprobación que se pone en verde») no se comprobaron.
- **Las diapositivas** (`diapositivas/capitulo-5-sarima.html`) y el capítulo 6 entero no se leyeron: del 6 solo las remisiones al 5.
