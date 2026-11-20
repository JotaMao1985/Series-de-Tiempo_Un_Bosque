# Capítulo 3 leído como estudiante · hilo narrativo y comprensión

Archivo leído: `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` (commit `58bdfc5`; los once
`<template id="module-N">` enteros y en orden, líneas 2677–6320), más el JavaScript que genera lo que el
estudiante ve en cada simulador (8200–9125: los doce `SIMULADORES[...]`, selectores, textos de «lectura»,
la tabla ordenable `TABLAS_RANKING['criterios']`), la autoevaluación `AUTOEVALUACIONES['cap3']`
(9125–9354, leída entera en enunciados y opciones; el resto, hasta 9850, ojeado) y la forma del simulacro
(9818 en adelante). Para el empalme: el cierre del capítulo 2 (`capitulo-2-estacionariedad-acf-pacf.html`:
las notas que prometen al 3 en 2684, 2892, 3188–3200, 3402–3405, 4103–4107, 4348–4352 y «Lo que sigue»,
5640–5655, más el módulo 8, 4600–4665, para el criterio de Guerrero), la apertura del capítulo 4
(`capitulo-4-modelos-arima.html`, 2749–2860 y las remisiones al 3 en 3548, 3917, 4320, 4551, 4961) y la
tarjeta de `Htmls_Series/index.html` (690–711, y la del preparcial, 923–945). Las líneas son del capítulo 3
salvo indicación. Lente: comprensión e hilo; no se juzga corrección técnica ni fuentes. No se editó nada
fuera de `diagnostico/cap3/`. **No se renderizó la página:** la lectura es del marcado y del JS (qué texto
genera cada simulador, no cómo se ve).

Cómo distingo lo medido de lo opinado: cada hallazgo lleva al final **(M)** si se comprobó con un recuento,
un `grep`, una lectura literal de dos líneas que se contradicen o la comparación con otro archivo, y
**(O)** si es juicio de lector sobre dónde se pierde alguien. Las cifras de carga salen de
`diagnostico/cap3/diag/lector_carga.py` (salida en `lector_carga.out`; la misma medición sobre el capítulo 2
actual, en `lector_carga_cap2.out`) y las de términos y notación de `lector_terminos.py`
(`lector_terminos.out`).

Etiquetas de la §2: **P** = pérdida de comprensión; **N** = dicho pero no mostrado (o mostrado donde no
puede reproducirse); **D** = decoración, ruido o repetición; **C** = carga.

Qué trae el estudiante: ha leído el 1 y el 2 ya revisados. Del 2 sabe: estacionariedad estricta y débil,
ruido blanco con su banda ±1,96/√T, ACF y PACF (con «la ACF cuenta la historia acumulada; la PACF, la
conexión directa»), la caminata y la raíz unitaria, ADF y KPSS, la diferencia `∇ = 1 − B` y `∇ₘ`, el
logaritmo y Box–Cox con el criterio de Guerrero, y un ejercicio «Para practicar» en casi cada módulo.
Del 2 también trae una promesa: «El Capítulo 3 da las herramientas» para la dependencia que queda en
`∇∇₁₂ log AirPassengers` (cap. 2, 5640–5648).

---

## 1. Mapa del arco

| Mód. | Pregunta que abre | Con qué cierra | Transición de entrada | Declarado | Medido (abierto) |
|---|---|---|---|---|---|
| M1 · 3.1 Operador de rezago (2677–2940) | ¿Cómo se escribe un modelo como polinomio en `B` y qué dicen sus raíces? | La advertencia del orden de coeficientes de `polyroot()`/`np.roots()` (2933–2937) y código | ✓ con el cap. 2, pero desactualizada: «apareció, casi de contrabando, el operador B» (2696) | 12 | 8,7 |
| M2 · 3.2 AR(p) (2945–3263) | ¿Cómo se reconoce un AR y cuándo es estacionario? | Bloque de código con la ACF/PACF teóricas (3196–3261) | ninguna: abre con la definición (2964) | 14 | 10,7 |
| M3 · 3.3 MA(q) (3268–3567) | ¿Por qué θ y 1/θ son el mismo modelo, y qué es invertible? | «El Módulo 4 generaliza esta reescritura a cualquier ARMA» (3565) | ✓ «El Módulo 2 construyó cada valor…» (3286–3290) | 12 | 11,7 |
| M4 · 3.4 Dualidad (3572–3871) | ¿Cómo se escribe un ARMA como MA(∞) y como AR(∞)? | «Dos ideas que hereda el Módulo 5» (3856–3869) | ✓ «En el Módulo 1… El Módulo 3 terminó…» (3590–3594) | 12 | 11,4 |
| M5 · 3.5 ARMA e identificación (3876–4416) | Dada una serie, ¿qué órdenes proponer, y por qué la tabla no basta? | Bloque de código de la redundancia (4347–4413) | ✓ resumen de M2–M4 (3895–3899) | 14 | 11,1 |
| M6 · 3.6 Simular y reconocer (4420–4535) | ¿Cuánto se parece una muestra a la teoría que la generó? | Nota de la regla del 5 % y remisión a Ljung–Box «del Módulo 8» (4528–4533) | débil: «La mejor forma de aprender a identificar es al revés» (4438) | 10 | 6,7 |
| M7 · 3.7 Estimación (4540–4815) | ¿Qué diferencia hay entre los tres estimadores y cuánto se separan? | Advertencia de `yule_walker()` R frente a Python (4807–4813) | ✓ «Hasta aquí los φ y los θ eran datos del problema» (4558) | 14 | 8,3 |
| M8 · 3.8 Criterios y diagnóstico (4820–5146) | ¿Cuál modelo elegir y pasa el elegido el examen de los residuales? | «Eso es lo que hace el módulo siguiente» (5022–5023), seguido de un bloque de código | débil: «Añadir parámetros siempre mejora la verosimilitud» (4841) | 14 | 9,0 |
| M9 · 3.9 Dos casos reales (5151–5769) | ¿Dónde estaba el problema del AR(2) que no pasaba? ¿Y cuándo no hay nada que modelar? | Bloque de código R/Python (5564–5766) | ✓ «Nos quedamos con un AR(2) que no pasaba Ljung–Box» (5172) | 19 | 25,0 |
| M10 · 3.10 «Autorregresión, redes neuronales y cierre» (5773–6253) | ¿De dónde viene el AR y cuándo gana el modelo pequeño? | «Lo que viene» → cap. 4 (6245–6250) | salto de tema: de los casos a las redes secuenciales (5792) | 14 | 18,1 (+17,6 autoevaluación +29,2 actividad Parcial 2) |
| M11 · «Simulacro del quiz» (6258–6320) | ¿Salen solas las decisiones del cap. 2 y de 3.1–3.4? | Nota «Cómo aprovecharlo» (6310–6317) | «Este módulo no añade contenido: es un ensayo» (6277) | 30 | 2,1 de lectura (los 30 son el tiempo del ensayo) |

Declarado: 165 min (135 sin el M11). Medido de lectura abierta (con pista y solución de los ejercicios, sin
los desarrollos plegados ni los quizzes): 122,9 min, de ellos 120,7 en M1–M10. El total declarado parece
razonable; el reparto no (ver §4).

### Lectura del arco

El capítulo se cuenta en tres tramos que el lector percibe bien: **construir los modelos** (M1–M5: notación,
AR, MA, dualidad, ARMA con su tabla), **usarlos con datos** (M6–M8: simular, estimar, diagnosticar) y
**cerrar** (M9 con dos casos; M10 con el contexto y el resumen; M11 con el ensayo). Es un arco más firme
que el del capítulo 2: tiene un nudo plantado en el M8 («el modelo "correcto" no pasa el examen», 4958) y
resuelto en el M9 («el parámetro que sobraba», 5170), y el M9 recoge además todo el capítulo en una tabla
(5463–5501) y en el hallazgo de que el 11,22 «es el ángulo de la raíz del polinomio» (5322–5325), que
ata el M1 con el M2. M3 → M4 → M5 se encadenan con frases que prometen y cumplen.

Donde el hilo afloja:

- **El primer módulo empieza por lo que menos hace falta para entender el segundo.** La mitad del M1
  (2737–2825: 406 palabras y 43 líneas de código) trata los convenios de signo y las diferencias entre R y
  Python; las raíces y la estacionariedad, que son el objetivo declarado (2689–2691), llegan después
  (2827–2938: 325 palabras). (M)
- **El M4 está construido sobre el ARMA, que se define en el M5** (3598, 3902): diez líneas del M4 usan
  «ARMA» como concepto antes de su definición. (M)
- **El M5 tarda en llegar a lo que promete su objetivo.** El laboratorio (4290) que deja «descubrir de
  primera mano» por qué la tabla funciona mejor en la teoría llega tras unas 1 500 palabras de prosa y 86
  líneas de código; el ciclo de identificación (3922) se lee antes que la tabla que cita (4016). (M)
- **El M6 es el eslabón más débil**: promete «reconocer» y «medir», y entrega una pantalla donde el proceso
  ya viene rotulado (ver §2). (M)
- **El M10 hace tres cosas** (puente con las redes, cierre, evaluación) y su «Resumen» (5878) no es lo
  último que el lector aprende: después vienen 639 palabras de material nuevo (5907–5990). (M)
- **No hay práctica hasta el M10.** El cap. 2 puso un «Para practicar» en casi cada módulo; el 3 no pide
  nada al lector (salvo mover deslizadores) en unos 120 minutos. (M)

### Promesas: hechas, cumplidas, incumplidas

| # | Dónde se promete | Qué | ¿Se cumple? |
|---|---|---|---|
| 1 | Cap. 2, 2684 y 2892 | El diagnóstico de residuales «es el corazón del Capítulo 3» y llega «una prueba formal, la de Ljung–Box» | **Sí** (M8, 4868–4883; M5 y M9 la usan). |
| 2 | Cap. 2, 5640–5655 («Lo que sigue») | Cuatro piezas «vuelven, convertidas en herramienta»: ruido blanco, ACF/PACF para identificar, `B` y la raíz fuera del círculo, y la TRM como variaciones porcentuales | **Sí, las cuatro** (M2–M3 y M8; M2, M3, M5; M1; M9 5503–5508). |
| 3 | Cap. 2, 5640–5648 | El 3 «da las herramientas» para la dependencia de `∇∇₁₂ log AirPassengers` (r₁ = −0,341) | **Parcial.** Las herramientas están; la serie no vuelve: `AirPassengers` aparece cero veces en los once módulos y ni el M10 («Lo que viene») le dice al lector que espere al cap. 5 por ella (solo 2721 lo insinúa). (M) |
| 4 | Cap. 2, 4348–4352 («Adelanto del Capítulo 3») | Lo fabricado al sobrediferenciar «es un MA(1) con θ = −1, no invertible, una propiedad que se define allí» | **Parcial.** El M3 define la invertibilidad y el simulador marca «NO — frontera» cuando el módulo de θ vale 1 (8582), pero «sobrediferenci» solo aparece en la actividad preparatoria (6223): el módulo nunca dice que θ = ±1 es lo que se obtiene al sobrediferenciar. El ítem 3 del simulacro sí lo pregunta (9851). (M) |
| 5 | Cap. 2, 3188–3200 | La regla PACF→AR, ACF→MA, «las dos decaen → ARMA» «allí se desarrolla en detalle» | **Sí** (M2, M3, M5). |
| 6 | M1 objetivo (2689–2691) | «Leer en sus raíces si el proceso es estacionario» | **Sí**, pero en la segunda mitad del módulo (2827 ss.) y en el simulador del M2 (3039). |
| 7 | M2, 3023 y 3044 | «El caso real del Módulo 9»: el AR(2) de las manchas solares | **Parcial.** La serie entra en el M7 («la serie que nos acompañará el resto del capítulo», 4558–4568), no en el 9, que la cierra. La remisión apunta al módulo equivocado. (M) |
| 8 | M2, 3128–3129 | Yule–Walker «será nuestro primer método de estimación en el Módulo 7» | **Sí** (4596). |
| 9 | M3, 3544 | «Queda sin justificar una afirmación del simulador» (la PACF del MA no se corta) | **Sí**, en 3549–3563. |
| 10 | M4 objetivo (3584–3585) | Manejar los pesos ψ y π | **Sí** (la tabla a mano, 3721–3746). |
| 11 | M5 objetivo (3888–3890) | «Descubriendo de primera mano por qué esa tabla funciona mucho mejor en la teoría que con datos reales» | **Sí, 370 líneas tarde** (laboratorio, 4290–4321). |
| 12 | M5, 4318–4320 | «Cuando en el Módulo 9 veas un correlograma real que no encaja…» | **Sí** (M9 5512–5515), aunque el primer correlograma real se ve en el M7 (4571). |
| 13 | M6 objetivo (4432–4433) | «Generar procesos de orden conocido para entrenar el ojo, y medir cuánto se separa una ACF muestral de la teórica» | **Parcial.** El proceso viene rotulado en el selector (8808–8813), no hay realizaciones repetidas y la «lectura» solo cuenta los rezagos nulos que se salen de la banda (8795–8801). La distancia media está en el laboratorio del M5 (8733), no aquí. «Aquí lo cuantificamos» (4507) es mucho decir. (M) |
| 14 | M7 objetivo (4552–4553) | Ver «cuánto» se separan los tres estimadores | **Sí, y bien**: 1,26 y 1,10 errores estándar frente a 0,04 y 0,02 (4694–4701). |
| 15 | M8, 4862 | «La trampa que reaparecerá en el Capítulo 4» (AICc entre distintos `d`) | **Sí** (cap. 4, 3933 y 4077). |
| 16 | M10, 6013–6015 | Las cifras de las soluciones salen de `precalculo/genera_soluciones.R` y «puedes contrastar las tuyas contra ellas» | **No para el lector:** el guion no está en la página ni en `Htmls_Series/`. (M) |
| 17 | M10, 6221–6226 y M11, 6277–6281 | Una «actividad preparatoria · Parcial 2» (cap. 2 + 3.1–3.4) y un «simulacro del quiz» de la misma materia | **Ambiguo:** dos nombres, un mismo alcance, y la portada anuncia un «Preparcial · Corte II» sobre los capítulos 3 y 4 (index 936). Ver §5. (M) |
| 18 | Tarjeta de `index.html` (703–705) | «Estimación por máxima verosimilitud, criterios de información y diagnóstico de residuales» | **Sí**, pero la tarjeta no nombra el caso de las manchas solares, el resultado «el parámetro que sobraba» ni el puente con las redes. |

---

## 2. Dónde me pierdo, módulo por módulo

### M1 · El operador de rezago (2677–2940)

- **C 2737–2825 · el bloque de signos es el más largo del módulo y va antes de las raíces.** Una
  advertencia con dos convenios (suma/resta, S-PLUS), un bloque R/Python de 43 líneas y una nota de «la
  regla que ahorra la tarde» preceden a la condición de estacionariedad (2832–2837), que es el objetivo
  (2689–2691). El lector llega a las raíces habiendo gastado 406 palabras y la mitad de su atención en un
  problema de software de dos lenguajes. (M)
- **P 2764–2775 · primer bloque de código: un ARMA(1,1) simulado y ajustado con `arima()`, con su salida
  (`s.e.`, `log likelihood`, `aic`).** ARMA se define en 3902, 1 138 líneas más abajo; estimar es el M7;
  AIC es el M8. Es un modelo nuevo, un estimador nuevo y una salida nueva en el primer ejemplo del
  capítulo. Lo que lo ancla es el «Adelanto» del cap. 2 (MA(1), «convención del signo contrario»), que
  prepara el signo de θ pero no el resto. (M/O)
- **P 2738–2741 y 2727 · «todos los modelos del capítulo», «un AR queda… un MA queda».** AR y MA no existen
  como modelos del capítulo hasta 2965 y 3293; solo se conocen por el AR(1) del cap. 2 y el MA(1) del
  adelanto. (M)
- **P 2767 y 2790 · el bloque R escribe `serie.csv` y el Python lo lee.** Quien trabaja solo en Python no
  puede ejecutar el bloque. (M)
- **P 2696 · «apareció, casi de contrabando».** El cap. 2 de hoy define `B` dos veces y de frente (cap. 2,
  3402–3405: «el nombre raíz unitaria viene de escribir el modelo con el operador de rezago B»; 4103–4107:
  `∇y_t = (1−B)y_t`). La frase es un eco del capítulo 2 anterior a su revisión. (M)
- **P 2885–2888 · «Diferenciar es justamente dividir por el factor (1−B) que produce esa raíz».**
  Diferenciar es multiplicar por `(1−B)` (2713–2715, cap. 2 4103); «dividir» invierte lo que el lector
  acaba de leer. El sentido correcto (el factor sale del polinomio) está a un paso, pero la palabra
  detiene a un lector atento. (O)
- **P 2899–2902 · `phi <- c(1.4, -0.75)` es un AR(2) con raíces complejas, antes del M2 (3025).** El
  vector está pensado para que el lector vea raíces complejas sin que nadie le diga qué es un AR(2). (M)
- **N · el módulo no tiene una sola figura ni simulador.** La condición de estacionariedad se ve solo en
  código y en un desarrollo plegado; el simulador que la hace visible es el triángulo del M2. El cap. 2
  abre con un simulador en el M1. (M)
- **✓ 2713–2722 y 2839–2842.** La nota de `(1−Bᵐ)(1−B)` ata el operador con el `∇ₘ∇` del cap. 2, y la
  explicación de por qué la raíz de `1 − φB` es `1/φ` vuelve intuitiva la palabra «fuera».

### M2 · Procesos AR(p) (2945–3263)

- **P 3110 · «el ρ_k = 0 exacto de la PACF».** La fórmula del recuadro (2996) escribe la PACF como
  `φ_kk`; `ρ_k` es la ACF, que decae. La frase dice que ese contraste «es toda la firma del AR» y mezcla
  los dos símbolos en el punto más importante del módulo. (M)
- **P 3017–3023 · «los cuatro casos merecen un comentario».** Los valores de dos aparecen en la prosa
  (φ = 0,8; φ = −0,7); del tercero («AR(2) con raíces reales») solo se sabe en el selector (8317) y dentro
  del plegado (3189) que es φ = (0,5; 0,3). (M)
- **P 3023 y 3044 · «el caso real del Módulo 9», «el modelo de las manchas solares del Módulo 9».** La
  serie entra en el M7; en el M2 es una serie desconocida a la que se remite sin contexto. (M)
- **P 3072 · «la varianza para los intervalos de pronóstico del Capítulo 6».** El M4 dice que los
  intervalos se deducen en el 4 (3770–3772) y que el 6 los evalúa. Dos capítulos distintos para la misma
  idea. (M)
- **C 3075–3104 · momentos del AR(p).** Cinco fórmulas en bloque en treinta líneas, con la varianza del
  AR(2) escrita dos veces (3101–3103), antes de que el lector haya visto un solo valor numérico de ellas.
  El módulo avisa del orden de cálculo (3086–3090), lo cual ayuda. (M/O)
- **N 3128–3194 · «¿De dónde salen esas fórmulas?» se contesta solo en el desarrollo plegado**, incluida la
  comprobación con φ = (0,5; 0,3) (3188–3192) que conecta con las cifras del simulador. Quien no despliega
  se queda con la pregunta. (M)
- **✓ 3118–3123 y 3039–3056.** «El denominador es el triángulo» y el simulador del triángulo con la
  realización que explota fuera de él. 3059–3064 (la fórmula del periodo con `arccos`) se queda sin
  derivar aquí, pero el M9 la cierra (5322–5325).

### M3 · Procesos MA(q) (3268–3567)

- **P 3281 y 3370 · «invertible» se usa en el objetivo y en la introducción del simulador de θ y 1/θ,**
  y se define en 3431. Qué quiere decir el nombre (poder reconstruir los choques desde lo observado) se
  dice dentro del plegado (3425–3427) y al final del módulo (3562). (M)
- **P 3363 y 3479 · «el modelo no está identificado».** «Identificado» (que los datos no distingan
  θ de 1/θ) y «identificación» (elegir p y q; título del M5 y 22 líneas del capítulo) comparten raíz y
  significan cosas distintas, a 555 líneas de distancia. (M/O)
- **N 3460–3466 · «el techo de ρ₁ es cos(π/(q+2))».** Se afirma en una nota sin deducirla ni citar de
  dónde sale, y el ejercicio 2 del M10 (6134–6138) se apoya en que el lector sepa que la cota del MA(1) no
  vale para el MA(2). (M)
- **D 3330–3345, 6089–6091 y 9165 · el panel de firmas del MA ya muestra el MA(2) con θ = (0,6; 0,4)**
  (selector 8471; su lectura da ρ₁ = 0,5526, 8460), que el ejercicio 2 del M10 y la pregunta gráfica de la
  autoevaluación vuelven a presentar como incógnita («ACF teórica que vale 0,5526 y 0,2632 y después es
  cero»). El lector que abrió el simulador la reconoce sin calcular. (M)
- **✓ 3304–3307, 3332–3334, 3349–3364, 3440–3458 y 3544.** «El nombre engaña» (frente a la media móvil
  del cap. 1), los «papeles intercambiados» del AR, el par θ = 0,5 / θ = 2 con la misma ρ₁ = 0,4, el triángulo
  del MA(2) obtenido cambiando signos del del AR(2) con dos ejemplos que desmienten dos intuiciones, y el
  «queda sin justificar una afirmación del simulador». Es el módulo mejor hilado del capítulo.

### M4 · Dualidad AR ↔ MA (3572–3871) · la prosa más densa de M1–M8 (1 154 palabras)

- **P 3598–3607 · «Un proceso ARMA admite dos escrituras…».** El módulo se llama «Dualidad AR ↔ MA» y se
  construye sobre el ARMA(1,1) (3623, 3627, 3708 y siguientes), que se define en el M5 (3902). Diez líneas
  del M4 usan «ARMA» como concepto antes de su definición. (M)
- **P 3616–3624 · el signo de los π.** `ε_t = Σ πⱼ y_{t−j}` con `π₀ = 1` obliga a `y_t = −Σ_{j≥1} πⱼ y_{t−j} + ε_t`,
  de modo que `π₁ = −1,2` significa «peso +1,2». Luego R pide los π con los argumentos cruzados y negados
  (`ARMAtoMA(ar = −θ, ma = −φ)`, 3804–3807) y Python «ya aplica el convenio» (3831–3835). Cuatro
  convenios de signo en un mismo módulo. (M)
- **P 3654–3706 · «Cómo se calculan los pesos» no tiene nada a la vista:** su contenido está entero en un
  plegado. Pero el ejemplo a mano (3714–3716) usa `ψⱼ = θⱼ + 0,7 ψ_{j−1}` y `πⱼ = −φⱼ − 0,5 π_{j−1}` sin
  haberlas escrito fuera de él (3679–3693). (M)
- **D/P 3683–3685 y 3701–3704 · detalles de la maquinaria de la página.** «La guarda `if (j - i >= 0)` que
  aparece en las dos implementaciones» y «trunca la serie en 600 términos… sobre los ocho procesos del
  capítulo, el error máximo es de 6,7×10⁻¹⁶»: la primera describe código que el estudiante no ve (el JS y
  el precálculo en R); la segunda cuenta «ocho procesos del capítulo» que el texto nunca enumeró. (M)
- **P 3632–3633 · la introducción del simulador explica el control `h`** («los pesos ψ₀…ψ_{h−1}, que son
  los que entran en la varianza del pronóstico a h pasos») antes de que exista la varianza del pronóstico
  (3763–3772). (M)
- **C 3762–3784 · dos notas de otros capítulos en el medio del módulo.** La varianza del error a `h` pasos y
  el abanico (que «reaparece en los capítulos 4, 5 y 6») y el paseo aleatorio con `ψⱼ = 1` ocupan unas 340
  palabras entre la tabla a mano y el código; son contenido de los caps. 4 y 6. (O)
- **P 3766 y 4129 · «abanico».** En el cap. 1 y el 2 es la dispersión que crece con el nivel (cap. 2,
  4600); aquí es la banda del pronóstico, y en el M9 vuelve a ser la banda (5417). Misma palabra, dos
  fenómenos. (M)
- **P 3778 y 3782 · «paseo aleatorio»** (dos usos) frente a «caminata aleatoria» (el cap. 2 y M1/M6 de
  este). (M)
- **D 3861–3864 · la parsimonia («siete coeficientes… el ARMA lo consigue con dos») se repite casi
  literal en el M5 (3914–3917).** La redundancia (ψ = θ/φ se cancela) se cuenta cuatro veces: M4
  (3866–3869), M5 (4323–4337), M9 (5344–5351) y M10 (5981–5989). (M)
- **✓ 3708–3746 y 3748–3760.** El ejemplo a mano del ARMA(1,1) con φ = 0,7 y θ = 0,5, en tabla y con
  «Cálculo», y las dos fórmulas cerradas que resumen lo que enseña el simulador. Es el mejor recurso del
  módulo; el ARMA(1,1) de esos números reaparece en M5, M6 y los simuladores como hilo conductor.

### M5 · ARMA e identificación (3876–4416) · 733 palabras, 111 fórmulas en línea, 144 líneas de código

- **P 3922–4014 y 4016–4049 · el ciclo de cuatro pasos se lee antes que la tabla que cita.** El paso 3
  dice «cruzar las dos lecturas en la tabla de identificación» (3989); la tabla llega noventa líneas
  después. El ciclo, además, trae vocabulario de tres módulos más adelante: `fitdf = p + q` y Ljung–Box
  (4007), AICc/BIC (3993), la banda de Bartlett (3965, que no se define en ningún sitio). (M)
- **P 4290–4321 · el laboratorio llega tras ~1 500 palabras y 86 líneas de código.** Es lo que el objetivo
  promete («de primera mano») y lo que hace tangible la nota de la tabla «la tercera fila es la débil»
  (4051–4056). Colocado antes de los momentos (4059) y de la demostración de que la tabla no da los
  órdenes (4159–4191), la haría visible antes de explicarla. (O)
- **C 4059–4157 · «Media, varianza y autocorrelación» (el mismo título que en el M2) trae solo
  autocovarianzas.** La ρ₁ del ARMA(1,1) aparece en 4181. El plegado de 189 palabras contiene las cifras
  que el texto de después (4151–4155) cita como «la primera de las cuatro cifras». (M)
- **P 4377 y 5035 · `aicc()` se define a mano en el M5 y se vuelve a definir en M8, M9 y M10.** En el M5 se
  usa antes de que se enseñe el criterio (4839). (M)
- **P 4365 y 4410–4411 · el ajuste del ARMA casi redundante cambia de sentido entre R y Python**
  (R: 0,83 y −0,80; Python: −0,08 y 0,13) y el módulo lo reconoce («dos parejas muy distintas con casi la
  misma suma»); el lector que no tiene presente que lo único estimable es la suma no sabe cuál usar. (O)
- **✓ 4188–4191 y 4316–4320.** «Un AR(1) con φ = 0,7 decae exactamente al mismo ritmo, desde ρ₁ = 0,7» (por
  qué la tabla no da los órdenes) y «lo que enseña el deslizador de T» (con T = 60 la banda vale ±0,253).
- **✓ 3958–4013 · «Qué te devuelve atrás».** Es el bucle del cap. 1 y del 2 en el lugar donde más lo
  necesita el lector: identificar es un ciclo de conjeturas.

### M6 · Simular y reconocer procesos (4420–4535) · el más corto (306 palabras)

- **N 4432–4433, 4507–4509, 8795–8813 · «reconocer», «entrenar el ojo», «medir».** El simulador muestra tres
  realizaciones fijas de longitud 200, con el proceso nombrado en el selector («AR(1), φ = 0,8»…). No hay
  ocultamiento del proceso, ni más de una realización, ni un número de distancia. El ejercicio de
  reconocer (adivinar qué es y luego ver la respuesta) no existe: el módulo se llama «reconocer». (M)
- **N 4447–4467 y 4483–4493 · el código dibuja una rejilla 3×3 y no imprime nada.** El lector no sabe qué
  mirar ni qué esperar de ella; el único texto que lo guía es el del simulador. (M)
- **D · no tiene ejercicio ni recapitulación;** el cierre es una nota de la regla del 5 % que remite al
  Ljung–Box del M8 (4529–4532). (M)
- **✓ 4529–4532 · «la regla del 5 %».** Es la frase que más rinde del módulo y la que el M9 recupera
  (5514).

### M7 · Estimación (4540–4815)

- **P 4571–4575 · el módulo de estimación abre identificando.** La serie de manchas solares trae primero su
  PACF (0,806 y −0,634) y la lectura «es un AR(2)»; el lector pasa de nuevo por la tabla del M5, esta vez
  con datos, antes de saber para qué los va a estimar. Es útil, y es la primera vez que se ve un
  correlograma real en el capítulo. (O)
- **N 4608–4663 y 4758–4766 · el argumento de por qué CSS y ML difieren vive en el plegado,** y el código
  lo cita: «El paso 6 del desarrollo: CSS puede salirse de la región estacionaria». Quien no desplegó
  encuentra un comentario que remite a un texto que no leyó. (M)
- **N 4783–4788 · la pestaña de Python no tiene el método 2** (CSS): trae un comentario que dice que no
  existe. Es honesto, pero la comparación de los tres métodos no se puede repetir en Python. (M)
- **P 4704–4709 · «No compares un σ̂² de Yule–Walker con uno de ML».** El lector queda con 298,96 frente a
  229,43 y la advertencia de que «no miden lo mismo», pero no con una regla de cuál usar para qué. (O)
- **P 4807–4813 · «es la misma clase de discrepancia que el ADF del Capítulo 2».** La remisión es correcta
  (cap. 2, 3991: `autolag='AIC'` frente a `autolag=None`) y evita decirlo otra vez. (M)
- **✓ 4694–4701.** Medir «cuánto es distinto» en errores estándar (1,26 y 1,10 frente a 0,04 y 0,02) es
  el modo de comparar que el lector se lleva a otros capítulos.

### M8 · Criterios de información y diagnóstico (4820–5146)

- **P 4930–4935 · la tabla ordenable aparece sin introducción en la prosa,** con un pie que da ya la
  conclusión del módulo («el AR(2) de Yule no es el mínimo de ninguno… no pasa el diagnóstico», 9119–9121)
  antes de que el texto la discuta (4958–4962), y la repite una tabla estática de siete filas. (M)
- **P 4997–5010 · el aparte R frente a Python en el punto de mayor tensión del módulo.** El texto acaba de
  decir que el AR(2) «no pasa el examen» (p = 0,0461), y lo siguiente son 149 palabras y nueve cifras
  sobre cómo inicializan el filtro R y statsmodels, hasta concluir que «el rechazo es real y se refuerza».
  La conclusión salva el aparte, pero el lector lo atraviesa sin saber todavía qué importa. (O)
- **N 4885–4928 · la regla práctica (`fitdf = p + q`), el mecanismo y el Monte Carlo de las 3 000 series
  están en el plegado,** y el código cita «el paso 4 del desarrollo» (5084). La regla se repite en el
  M10 (5871–5873, 5897, 5971), de modo que no se pierde, pero el porqué sí. (M)
- **P 4847–4851 y 4878 · `n` en el AIC y `T` en Ljung–Box,** dentro del mismo módulo. (M)
- **N 5043–5045 · «La rejilla no es un producto cartesiano… son los once candidatos de la tabla ordenable».**
  Se afirma que la rejilla la justifica «la lectura de los correlogramas», pero ningún candidato
  (por ejemplo (0,3), (4,0)) sale de la lectura que el M7 hizo (AR(2)): es una elección de los
  autores, no del método. (O)
- **✓ 4958–4995 y 5012–5020.** «Aquí hay un problema, y conviene no taparlo» y «Un detalle que justifica la
  prueba conjunta» (ninguna autocorrelación residual sale de la banda y aun así Ljung–Box rechaza): es la
  razón de ser del módulo, bien dicha, y con el gancho del M9 en 5022.

### M9 · Dos casos reales (5151–5769) · el módulo más pesado, 25,0 min frente a 19 declarados

- **P 5176–5178 y 5184–5199 · «elasticidad amplitud–nivel (la pendiente de log(desviación) contra
  log(media) por bloques, el mismo diagnóstico del Capítulo 1)».** El cap. 1 dibuja la amplitud
  estacional frente al nivel año a año (cap. 1, 3594–3632); el cap. 2 da el criterio de Guerrero por
  bloques (cap. 2, 4638–4643). «Elasticidad», `b̂`, el intervalo y el `R²` de una pendiente log–log no
  aparecen en ninguno de los dos. Que `b = 0,5` equivalga a la raíz y `b = 1` al logaritmo (5198) se dice
  sin vincularlo con `λ = 1 − b` de Guerrero. Es una herramienta nueva, atribuida al capítulo anterior. (M)
- **N 5184–5199, 5271–5278, 5456–5460, 5550–5554 · cifras que ningún bloque de código del módulo produce.**
  La tabla de `b̂` (0,8165; 0,7658; 0,7034), las variantes de λ (11,39 años y p = 0,4892; 11,28 y 0,2217),
  la asimetría y el Shapiro–Wilk (0,791 → 0,573; 0,0007 → 0,0470) y la media mensual de la TRM
  (0,2681 %, e.e. 0,3195, t = 0,84) están solo en la prosa; el código reproduce lo demás. (M)
- **P 5531–5533 y 5550 · `auto.arima`.** Aparece dos veces («el MA(1) que sugiere auto.arima»,
  «`auto.arima()` devuelve el MA(1) sin término constante») y en ninguna parte se presenta ni se llama en el
  código; el código ajusta el MA(1) directamente. Es la primera y única mención en el capítulo. (M)
- **P 5226–5243 · dos columnas de AICc, 838,30 y 324,00, una al lado de la otra.** El M8 acaba de decir
  (4862–4865) que los criterios solo comparan modelos con los mismos datos; la tabla pone dos
  transformaciones distintas lado a lado y nada advierte de que cada columna se lee por separado. (O)
- **P 5391–5414 · `j` y `h = j + 1` en la misma fila.** «Error estándar 2,70, semiancho ±5,29» es para
  `h = 6` y `j = 5`; un lector que busque `h = 5` y lea la fila de `j = 5` se equivoca de una. (M)
- **P 5558–5561 · el encabezado dice «Donde sí hay estructura: en el cuadrado» y el cuerpo, «p = 0,9166:
  tampoco hay agrupamiento de volatilidad detectable».** El título anuncia lo contrario de lo que dice la
  nota; la estructura está en los datos diarios, que el módulo no tiene. (M)
- **P 5503–5508 y 5512 · «Retomemos la TRM del Capítulo 2» y se pasa a los log-retornos.** La serie del
  cap. 2 era la diferencia de la TRM (r₁ = 0,088, cap. 2 4298); aquí r₁ = 0,105 y salen dos barras (rezagos 5
  y 8). No se dice que `100·∆log` y `∆` son series distintas. (M/O)
- **D 5377 y 5431 · «el envolvente».** En matemáticas es «la envolvente». (M)
- **C 5170–5461 · el caso 1 ocupa 1 814 palabras, 16 recuadros, tres tablas y dos simuladores.** Seis
  pasos (escala, raíz, rejilla, hallazgo, polinomio, pesos) y cada uno trae sus notas y avisos; los
  recuadros que no son el hallazgo (λ de Guerrero, signo de φ₂, ARMA(2,1) «impecable», bandas en escala de
  raíz, normalidad) son cinco desvíos antes de llegar a los pesos ψ. (M/O)
- **✓ 5172–5173, 5250–5252, 5322–5325, 5416–5426, 5463–5501 y 5541–5546.** La pregunta que conecta con el
  cap. 2 («¿la serie está en la escala adecuada?»), «parcheando un problema de escala», «el 11,22 es el
  ángulo de la raíz», «el abanico se abre, y se para», la tabla de «el capítulo entero, sobre una sola
  serie» y «la conclusión honesta». Es lo mejor del capítulo y lo que más conviene no romper.

### M10 · «Autorregresión, redes neuronales y cierre» (5773–6253)

- **P · el módulo tiene tres nombres.** El encabezado dice «3.10 Autorregresión, redes neuronales y
  cierre» (5779), la barra lateral «Cierre, resumen y autoevaluación» (6338) y el comentario del marcado
  «Cierre: ciencia de datos, resumen y evaluación» (5771). (M)
- **P 5878–5990 · después del resumen viene material nuevo.** La tabla «De dónde sale el orden»
  (5913–5955), que añade que la última barra de la PACF «estima φ_p» y que ninguna barra de la PACF
  estima un θ_j (5927–5938), la lista «Qué confirma el orden elegido» (5965–5979) y el aviso del ARMA(2,2)
  que tiene la misma ACF que el ARMA(1,1) (5981–5989) suman 639 palabras tras un resumen de 204. El
  hecho PACF(p) = φ_p no está en el M2, que es donde se describe la firma del AR. (M)
- **P 5909–5911 · «Esta la completa con lo que viene después».** El antecedente de «Esta» es la tabla
  del M5, nombrada en la oración anterior solo por «la tabla de identificación»; se lee como «esta
  [sección]». (O)
- **N 5840–5845 · «Un puente concreto»: el estado oculto de una RNN lineal con una unidad es un AR(1) y
  la condición |w| < 1 es «la misma» que la estacionariedad.** Para un estudiante de ciencia de datos es lo
  más atractivo del módulo; se enuncia en cuatro líneas sin el supuesto que lo separa de un AR (en la RNN
  `x_t` es una entrada, no un ruido blanco). (O)
- **D 6013–6015 · «el script `precalculo/genera_soluciones.R`».** Una ruta del repositorio en prosa para el
  estudiante, que no puede abrirla. (M)
- **N 6011–6196 · tres ejercicios: sobre `lh` (M5+M7+M8), sobre el MA(2) (M3) y sobre las manchas solares
  en otras ventanas (M9).** Ninguno sobre el AR(2) y el triángulo (M2), los pesos ψ y π (M4), ni los tres
  estimadores (M7). El ejercicio 2 pregunta por una cota (6089–6091) cuya respuesta ya adelantó la nota de
  3460–3466. (M)
- **N 9125–9354 · la autoevaluación no toca el M2, el M6 ni el M10.** Etiquetas `modulo`: 1, 3, 5, 4, 3, 5,
  9, 8, 8, 7. Nada sobre la firma del AR (PACF que se corta), el triángulo del AR(2), los momentos del AR
(M2) ni sobre simular y reconocer (M6). (M)
- **P 6219–6231 y 6277–6281 · «Actividad preparatoria · Parcial 2» y «Simulacro del quiz» (M11).** Dos
  nombres y dos módulos para una misma materia (cap. 2 y los cuatro primeros módulos de este), con una
  autoevaluación de diez preguntas en medio (5997). Por las notas del proyecto el Parcial 2 se aplicó el
  14 de octubre; la fecha de hoy es 19 de noviembre. Quien lea la página ahora lee «preparar el Parcial 2»
  como algo vigente. (M/O, por confirmar con el calendario)
- **✓ 5867–5876, 6193–6194 y 6245–6250.** El aviso del uso crítico de asistentes lleva cuatro puntos y cada
  uno remite al módulo donde se enseñó; la moraleja del ejercicio 3 («no rechazar H₀ nunca es lo mismo
  que aceptarla») contrapesa con acierto el «ahora sí pasa» del M9; y «Lo que viene» mira al cap. 4 con lo
  que de verdad vuelve (los criterios con distinto `d`).

### M11 · Simulacro del quiz (6258–6320)

- **P 6264 · el encabezado no lleva número** («Simulacro del quiz / Mock quiz»), mientras los otros diez
  son «3.N …» (el estudiante lo ve numerado como 11 en la barra lateral). (M)
- **✓ 6277, 6283–6286 y 6288–6293.** «Este módulo no añade contenido: es un ensayo», «lo que se repite de
  una variante a otra es la decisión» y «Aquí no se corrige» con su razón. Es claro y no promete lo que no
  da.

---

## 3. Problemas transversales

### Lo que se usa antes de definirse

| Término | Primer uso (línea, módulo) | Definición | Distancia |
|---|---|---|---|
| «un AR», «un MA» como modelos | 2739–2740 (M1) | 2965 (M2); 3293 (M3) | 226; 553 |
| ARMA(1,1) (y `arima()` con su salida) | 2764–2775 (M1) | 3902 (M5) | 1 138; diez líneas del M4 lo usan |
| MA(∞) / AR(∞) | 2880 (M1); 3426 (M3) | 3598 (M4) | 718 |
| invertible, invertibilidad | 3281, 3370 (M3) | 3431 (M3) | 150; el porqué del nombre, 3562 |
| pesos ψ y π | 3555 (M3, sin nombre) | 3585, 3610 (M4) | 30 |
| manchas solares | 3023, 3044 (M2) | 4563 (M7) | 1 540 |
| Ljung–Box y `fitdf` | 4007 (M5); 4532 (M6) | 4875, 4917 (M8) | 868; 910 |
| AICc, BIC | 3993, 4377 (M5); 4707 (M7) | 4839 (M8) | 846 |
| banda de Bartlett | 3965 (M5) | nunca | — |
| `auto.arima` | 5533, 5550 (M9) | nunca | — |
| identificado / identificación | 3363 (M3) | 3919 (M5) | 555 (y dos sentidos) |
| «la tabla» PACF(p) = φ_p | 5927 (M10) | (no aparece antes) | — |

Cada uno por separado se soporta. Juntos hacen que el M5 se lea con el vocabulario del M8 y el M4 con el
modelo del M5; el M1 empieza con una salida de `arima()` antes de que haya un modelo. (M)

### Vocabulario y notación que cambian

- **«identificado» frente a «identificación».** Dos sentidos (identificabilidad del parámetro; elección de
  p y q) con la misma raíz, el uno en M3 (3363, 3479) y el otro en M5 y M10. (M)
- **`T` y `n`.** La banda se escribe `±1,96/√T` en M5 (4295) y M6 (4529) y `±1,96/√n` en M5 (3965) y M10
  (5929); el AIC usa `n` (4847) y Ljung–Box `T` (4878) en el mismo módulo; los datos de las manchas y el
  ejercicio, `n` (4564, 5853, 6030). El cap. 2 usa `T`. (M)
- **«pseudo-ciclo», «pseudo-periodo» y «periodo».** M2 dice «pseudo-ciclo» (3023) y «periodo» (3043,
  3059); desde el M7 es «pseudo-periodo». El M10 usa las tres. (M)
- **«abanico».** Cap. 1 y cap. 2: la dispersión que crece con el nivel. Cap. 3: la banda del pronóstico
  (3766, 5417, 5891). (M)
- **«caminata aleatoria» frente a «paseo aleatorio».** El cap. 2 solo conoce «caminata»; el M4 usa
  «paseo» en dos lugares (3778, 3782). (M)
- **`ρ_k = 0` de la PACF** (3110) frente a `φ_kk` (2996). (M)
- **`ε_t ∼ RB(0, σ²)`.** La abreviatura «RB» no se presenta (2972) y el cap. 2 no la usa (cap. 2, 2589:
  `N(0, σ²) i.i.d.`; 3377: «ruido blanco»); el cap. 4 la hereda (cap. 4, 2782). (M)
- **«Módulo N» en prosa y «3.N» como cita.** La prosa dice «Módulo 4»; el resumen del M9 (5473 ss.), la
  actividad preparatoria (6230) y los ítems del simulacro dicen «3.4». Las dos formas coexisten en el
  mismo módulo (M9: 17 y 9 líneas). El cap. 4 usa «módulo 3.9» (cap. 4, 9419). (M)
- **j y h.** La tabla de los pesos de la TRM/manchas (5391–5414) numera `j` desde 0 y `h = j + 1`; el
  simulador del M4 y el del M9 usan `j` y `h`. (M)
- **«el envolvente»** (5377, 5431). (D)
- **«residuales» (29 líneas) frente a «residuos» (0).** El cap. 1 dijo «residuo»; el cap. 2 mezcla ambos.
  No se cambia, solo se anota. (M)
- **«Módulo» en dos niveles.** La tarjeta de la portada dice «Capítulo 3 · Módulo II» (index 696) y el
  capítulo habla de «Módulo 3» por 3.3. (M)

### Convenios y advertencias que se acumulan

Hay ocho avisos sobre discrepancias entre lenguajes, signos o argumentos: M1 (los signos del θ, 2737–2752;
el signo del AR al simular, 2812–2824; el orden de coeficientes, 2933–2937), M4 (el índice `j = 0`, 3848–3853),
M6 (burn-in, 4497–4503), M7 (Yule–Walker, 4807–4813), M8 (p-valores de Ljung–Box, 4997–5010) y M9 (el
signo del segundo coeficiente al escribir el polinomio, 5295–5303); a ellos se suman los comentarios del
M4 sobre los π con signos cambiados (3804–3810). Cada uno es un «fallo silencioso» bien elegido, y el M9
recoge dos como cierre. Cuatro de los ocho caen en M1 y M4, sobre un lector que aún no tiene el modelo en la
cabeza. (M/O)

### Plegados que cargan con lo importante

Siete módulos tienen un «Ver el desarrollo paso a paso» (M1, M2, M3, M4, M5, M7, M8). En cuatro de ellos
algo que el texto o el código usan después vive solo dentro:

| Plegado | Qué vive solo dentro | Quién lo cita |
|---|---|---|
| M4, 3656–3706 | la recursión de ψ y π | el ejemplo a mano (3714–3716) |
| M5, 4106–4157 | `γ₀` y `γ₁` del ARMA(1,1) | 4151–4155 y 4101–4104 |
| M7, 4608–4663 | por qué CSS y ML difieren y el ejemplo T = 40, φ = 0,95 | el código, «el paso 6 del desarrollo» (4758) |
| M8, 4885–4928 | por qué hace falta `fitdf` y el Monte Carlo de las 3 000 series | el código, «el paso 4 del desarrollo» (5084) y M10 (5871) |

Más 3425–3427 (M3), donde el plegado dice por qué se llama «invertible». (M)

### Voz

La prosa expositiva es en su mayor parte impersonal, con dos acentos: la segunda persona del singular
(«verás», «te», «comprueba», «tus», «puedes», «tienes») se concentra en el M10 (8 formas) y el M1 (4), y la
primera del plural («retomemos», «pongamos juntos», «volvamos») en el M9 (5). En el M10 el tuteo sí es prosa
expositiva y no solo ejercicio («Un asistente te dará…», 5868; «tú tienes que verificarlos», 5870).
Recuento aproximado por expresión regular sobre el texto de cada módulo, sin las introducciones de
simulador, el código ni los paneles de ejercicio. Es un asunto de otro lente; se anota porque el cambio de
persona entre el M9 y el M10 se oye. (M)

---

## 4. Carga

Convenio y números: `diagnostico/cap3/diag/lector_carga.py` (la fórmula del cap. 1 y del cap. 2: palabras de
prosa / 180 + 3 por simulador + 2 por bloque de código, con un par R/Python como un bloque; se quitan
`<pre>`, scripts, canvas, botones, el pie de fuentes y la matemática en bloque; cada fórmula en línea es una
palabra). «Cerrado» deja sin contar pista y solución; «abierto» las cuenta; los plegados van aparte; los
quizzes (JS) van aparte. Los doce simuladores son los de la tarjeta de la portada; el simulacro del M11 no
se cuenta como simulador.

| Mód. | Palabras (cerrado) | `$$` | `$` | Cuadros | Tablas | Sim. | Bloques (líneas) | Plegado (palabras) | Cerrado (min) | Abierto (min) | Declarado | Razón abierto/declarado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 850 | 6 | 48 | 8 | 0 | 0 | 2 (74) | 60 | 8,7 | 8,7 | 12 | 0,73 |
| M2 | 487 | 8 | 68 | 8 | 0 | 2 | 1 (56) | 266 | 10,7 | 10,7 | 14 | 0,76 |
| M3 | 666 | 5 | 90 | 7 | 0 | 2 | 1 (62) | 190 | 11,7 | 11,7 | 12 | 0,97 |
| M4 | 1 154 | 5 | 119 | 5 | 1 | 1 | 1 (51) | 201 | 11,4 | 11,4 | 12 | 0,95 |
| M5 | 733 | 6 | 111 | 10 | 1 | 1 | 2 (144) | 189 | 11,1 | 11,1 | 14 | 0,79 |
| M6 | 306 | 0 | 4 | 2 | 0 | 1 | 1 (45) | — | 6,7 | 6,7 | 10 | 0,67 |
| M7 | 600 | 0 | 37 | 5 | 1 | 1 | 1 (84) | 318 | 8,3 | 8,3 | 14 | 0,60 |
| M8 | 727 | 2 | 67 | 7 | 1 | 1 | 1 (110) | 307 | 9,0 | 9,0 | 14 | 0,65 |
| M9 | 2 515 | 11 | 214 | 20 | 4 | 3 | 1 (194) | — | 25,0 | 25,0 | 19 | **1,31** |
| M10 | 1 539 (2 184 abierto) | 1 | 115 | 9 | 2 | 0 | 3 (77) | — | 8,6 | 18,1 | 14 | **1,30** |
| M11 | 377 | 0 | 1 | 2 | 0 | 0 | 0 | — | 2,1 | 2,1 | 30 | (el ensayo) |
| **Total** | 9 954 (10 599) | 44 (+29 plegadas) | 874 | 83 | 10 | 12 | 14 | 1 531 | 113,3 | 122,9 | 165 | |

Los desarrollos plegados suman 8,5 min si se abren. La autoevaluación (10 preguntas) pesa 17,6 min de
lectura de enunciados, opciones, pistas y retroalimentación; la actividad preparatoria (10 preguntas), 29,2;
las dos se leen en el M10. Ninguna columna incluye el tiempo de hacer los ejercicios, de contestar los
quizzes ni de ejecutar el código.

**Comparación con el capítulo 2 (misma medición).** El cap. 2 declara lo que mide: su razón
abierto/declarado vale entre 0,98 y 1,04 en los nueve módulos (146 declarados, 147,5 medidos). El cap. 3
no pasó por esa medición: M1–M8 declaran 102 min y miden 77,6 (0,76; de 0,60 a 0,97), y M9–M10 declaran 33 y
miden 43,1 (1,31). Con la convención del cap. 2 los declarados saldrían: M1 9, M2 11, M3 12, M4 11, M5 11,
M6 7, M7 8, M8 9, M9 25, M10 18 y el simulacro, 30 (el reloj del ensayo). (M)

**El capítulo es mucho más matemático que el 2.** 44 fórmulas en bloque (más 29 plegadas) frente a 4 del
cap. 2 (más 4), y 8,8 fórmulas en línea por cada 100 palabras frente a 4,9. Por módulo, las fórmulas en
línea por 100 palabras (cerrado): M1 5,6; M2 14,0; M3 13,5; M4 10,3; M5 15,1; M6 1,3; M7 6,2; M8 9,2; M9 8,5;
M10 7,5. La fórmula de minutos (180 palabras por minuto) supone prosa; en M2–M5 las medidas son un suelo, no
una estimación. (M/O)

### Qué se desbalancea

- **M9 pesa 1,31 veces lo declarado y es el módulo que el lector lee con más acumulado** (78 min medidos, 102
  declarados, en los ocho anteriores). 2 515 palabras, 20 recuadros, 4 tablas, 3 simuladores, 194 líneas de
  código. (M)
- **M10 pesa 1,30 veces lo declarado con los ejercicios abiertos, y dos quizzes de diez preguntas que suman
  46,8 min más de lectura.** Es el módulo con más cosas distintas. (M)
- **M6 y M7 están en 0,67 y 0,60.** El M6 es un módulo de 306 palabras (6,7 min), y su declarado es 10. El M7
  declara 14 y mide 8,3 (10,1 con el plegado): es el módulo de la estimación, con la tabla comparativa que el
  objetivo pide, y el que más se beneficiaría de un ejercicio. (M/O)
- **M4 es el más cargado de prosa de M1–M8** (1 154 palabras, 119 fórmulas en línea, dos recuadros que
  anticipan otros capítulos). (M)
- **M1 y M2 son los módulos con menos que leer y más que descifrar:** el M2 tiene 487 palabras y 14 fórmulas
  en línea por 100; el M1 no tiene simulador. (O)

### Dónde partiría o movería (sin renumerar; de mayor a menor rendimiento)

1. **Declarar lo medido** (la convención del cap. 2): M1 9, M2 11, M3 12, M4 11, M5 11, M6 7, M7 8, M8 9,
   M9 25, M10 18; el M11, 30. No cuesta nada.
2. **M1: poner las raíces antes que los convenios de signo** (o dejar el bloque de signos como cierre,
   después de la condición de estacionariedad), y sustituir el ARMA(1,1) estimado con `arima()` por el MA(1) del
   adelanto del cap. 2; hacer autosuficiente la pestaña de Python (sin `serie.csv`). Cambiar «de contrabando».
3. **M5: tabla antes que ciclo, y laboratorio justo después de la tabla** (4290–4321 → tras 4056), antes de los
   momentos y de la demostración. El ciclo puede ir como cierre del módulo, con el vocabulario del M8 ya
   explicado o con una remisión («Ljung–Box, Módulo 8»).
4. **M4: sacar los dos recuadros de otros capítulos** (3762–3784) hacia el final y escribir la recursión de ψ y
   π fuera del plegado; anticipar el ARMA en una línea («un ARMA… se define en el Módulo 5»).
5. **M6: dar la oportunidad de reconocer:** un selector «proceso oculto» con un botón «¿cuál era?», o
   cambiar el título a «Teórica frente a muestral»; poner debajo del bloque de código «qué mirar».
6. **M9: definir `b̂`** (una línea: «`s ∝ ȳᵇ`; `λ = 1 − b`») o remitir a Guerrero; poner el código que falta
   (la tabla de `b̂`, las variantes de λ, Shapiro, la media de la TRM) o declarar que son de apoyo; presentar o
   quitar `auto.arima`; corregir el encabezado de 5558 y alinear `j` con `h`.
7. **M10: dividir en dos** (el puente con las redes y el aviso de los asistentes; el cierre) y mover 5907–5990
   antes del resumen; quitar la ruta `precalculo/genera_soluciones.R`; reunir en un solo sitio los nombres y el
   alcance de las tres evaluaciones (autoevaluación, actividad Parcial 2, simulacro) y confirmar la fecha.
8. **Un «Para practicar» por módulo**, como el cap. 2, al menos en M2, M4, M5 y M7.
9. **Notación:** `T` o `n`, y una sola; «caminata»; «la envolvente»; `φ_kk` en 3110; «identificado» →
   «no identificable» o similar.

---

## 5. Empalme con el capítulo 2, con el 4 y con la portada

### Lo que el cap. 3 supone del 2, y si el 2 lo da

| El cap. 3 supone… | ¿Lo da el cap. 2? |
|---|---|
| `∇ = 1 − B`, `B`, `∇ₘ` (M1 2696–2722) | **Sí, y de frente** (cap. 2, 3402–3405, 4103–4107); la frase «casi de contrabando» es un eco anterior. |
| «La PACF mide la correlación directa» (2991) | **Sí** (cap. 2, M4). |
| La regla PACF→AR, ACF→MA (objetivos de M2 y M3) | **Sí, anticipada** (cap. 2, 3188–3200). |
| La caminata, la raíz unitaria y el KPSS que rechazaba (2885–2888) | **Sí** (cap. 2, M5, M6). |
| Ruido blanco como material y como meta (M2, M8) | **Sí** (cap. 2, 2678–2684). La abreviatura «RB» no (2972). |
| La banda ±1,96/√T y la regla de «uno de cada veinte» (4295, 4529) | **Sí** (cap. 2, 2621–2627). El cap. 2 usa `T`; el 3 mezcla `T` y `n`. |
| Box–Cox y el criterio de Guerrero con `λ` (5204–5206) | **Sí** (cap. 2, M8, 4638–4643). El cap. 2 dice «en este curso se usa el logaritmo»; el M9 usa la raíz y lo explica con el cero de 1810 (5202–5203). |
| La elasticidad amplitud–nivel «del Capítulo 1» (5176–5178) | **No**; ni el cap. 1 ni el 2 la presentan (§2, M9). |
| La discrepancia entre R y Python en el ADF (4812) | **Sí** (cap. 2, 3991). |
| La TRM con raíz unitaria y `∇` estacionaria (5505–5508) | **Sí** (cap. 2, M6). Los log-retornos son otra serie (§2, M9). |
| Ljung–Box «se define en el cap. 3» | **Sí** (M8). |
| La sobrediferenciación como MA(1) con θ = −1 (adelanto del cap. 2) | **No se retoma en el módulo** (promesa 4). |
| `∇∇₁₂ log AirPassengers` y su r₁ = −0,341 | **No vuelve** (promesa 3); solo el cap. 5. |

**Conclusión:** el empalme narrativo funciona (las cuatro piezas de «Lo que sigue» aterrizan) y el cap. 3
cita de vuelta al cap. 2 con acierto en los puntos donde importa (Guerrero, el ADF, la TRM, la raíz fuera del
círculo). Lo abierto: el adelanto de la sobrediferenciación, la serie que no vuelve, la elasticidad atribuida
al capítulo anterior y el eco de «de contrabando».

### Lo que deja preparado para el cap. 4

| El cap. 4 necesita… | ¿Lo deja el cap. 3? |
|---|---|
| `φ(B)`, `θ(B)` «exactamente los del capítulo anterior» (cap. 4, 2784–2785) | **Sí** (M1). |
| El ARMA como caso `d = 0` (cap. 4, 2845) | **Sí** (M5). |
| «La tabla ACF/PACF del Capítulo 3» (cap. 4, 3548) | **Sí** (M5, 4018 y 5913). |
| «La estimación es la del Capítulo 3» (cap. 4, 3917) y «el diagnóstico… es el del Capítulo 3» (4320) | **Sí** (M7, M8). |
| Los pesos ψ para los intervalos (cap. 4, 4551, 4611) | **Sí** (M4); el cap. 4 los deduce. |
| «El Capítulo 3 mostró que sus log-retornos son, a efectos prácticos, ruido blanco» (cap. 4, 4961) | **Sí** (M9, 5541–5546). |
| Los AICc de distinto `d` no se comparan (cap. 4, 3933, 4077) | **Sí, avisado** (M8, 4862–4865). |
| El algoritmo de Hyndman–Khandakar (cap. 4, 4094) | **Anunciado** en «Lo que viene» (6249); el M9 nombra `auto.arima` sin presentarlo (5533), lo que prepara mal el terreno. |

El cap. 4 abre con «El Capítulo 3 terminó con un límite explícito» (cap. 4, 2767): el límite («todo este
capítulo ha supuesto que la serie ya era estacionaria», 6246) está en el M10, y después viene el M11, de
modo que «terminó» no es literal. Es una imprecisión menor.

### La tarjeta de la portada (`Htmls_Series/index.html`, 690–711)

Texto: «Operador de rezago y polinomios característicos, AR(p) y su triángulo de estacionariedad, MA(q) e
invertibilidad, dualidad AR↔MA, identificación con ACF y PACF, estimación por máxima verosimilitud,
criterios de información y diagnóstico de residuales.» Etiquetas: «Semanas 5–7», «Capítulo 3 · Módulo II» y
«11 módulos · 12 simuladores».

- **Cifras:** 11 módulos y 12 simuladores son correctas (12 `data-simulador` de simulador, más el simulacro
  del M11). (M)
- **Lo que el capítulo más desarrolla y la tarjeta no nombra:** los dos casos reales (las manchas solares
  y la TRM) y el resultado que da su sentido al capítulo, «el parámetro que sobraba» (el M9); la comparación
  de tres estimadores (M7, solo «máxima verosimilitud»); el puente con las redes y el uso crítico de los
  asistentes (M10); el ensayo del M11. La tarjeta lista el temario, no el argumento. (M/O)
- **Preparcial · Corte II (index 923–945):** «Autodiagnóstico sobre los capítulos 3 y 4», y la tarjeta del
  cap. 3 no lo menciona. El cap. 3 por su parte lleva su propia «actividad preparatoria · Parcial 2» (6219) sobre
  «el capítulo 2 y los cuatro primeros módulos de este». Dos «preparaciones» del mismo parcial con
  alcances distintos, y la fecha del Parcial 2 (14 de octubre, según las notas del proyecto) ya pasó. (M;
  la fecha, por confirmar)
- **«Módulo II»:** en la portada es el módulo del curso; dentro del capítulo, «Módulo 3» es 3.3. Dos
  niveles con el mismo nombre. (O)

---

## 6. Lo que funciona (no romper al revisar)

1. **M9 5170–5173, 5250–5252, 5322–5325, 5463–5501, 5541–5546 · el arco «el parámetro que sobraba».** El
   modelo que no pasa (M8) → la pregunta del cap. 2 («¿la serie está en la escala adecuada?») → la raíz
   cuadrada → «parcheando un problema de escala» → «el 11,22 es el ángulo de la raíz» → la tabla «el capítulo
   entero, sobre una sola serie» → «la conclusión honesta» de la TRM. Es la mejor secuencia del curso hasta
   aquí y vale tanto el capítulo como el resto junto.
2. **M8 4958–5023 · «Aquí hay un problema, y conviene no taparlo» con el gancho del módulo siguiente.**
   Plantea el nudo con honestidad y no lo cierra, para que el M9 lo cierre.
3. **M4 3708–3760 · el ejemplo a mano del ARMA(1,1)** (φ = 0,7; θ = 0,5), con tabla, columna de «Cálculo» y
   fórmulas cerradas; es el ejemplo que M5, M6 y los simuladores reciclan como hilo.
4. **M3 3304–3307, 3332–3334, 3349–3364, 3440–3458, 3544 · la línea del MA:** el nombre que engaña (con
   el cap. 1), los papeles intercambiados, θ = 0,5 frente a θ = 2, el triángulo del MA(2) por cambio de
   signos y «queda sin justificar».
5. **M2 3118–3123 · «El denominador es el triángulo».** Une la condición de las raíces, el triángulo y la
   varianza finita en una frase.
6. **M5 4051–4056, 4188–4191, 4316–4320 y 3958–4013 · «La tercera fila es la débil», el AR(1) que decae al mismo
   ritmo que el ARMA(1,1), «lo que enseña el deslizador de T» y el ciclo con su «Qué te devuelve atrás».**
7. **M7 4694–4701 · medir «cuánto es distinto» en errores estándar** (1,26; 1,10; 0,04; 0,02).
8. **M8 5012–5020 · el aviso de que ninguna autocorrelación residual sale de la banda y la prueba conjunta
   rechaza igual.**
9. **M10 5867–5876 y 6193–6194 · el aviso del uso crítico de asistentes con cuatro puntos que remiten a sus
   módulos y la moraleja «no rechazar H₀ nunca es lo mismo que aceptarla».**
10. **Los empalmes con los vecinos:** M1 2744–2751 cierra el «Adelanto» del cap. 2 con el convenio de suma y
    resta (y el cap. 4, 2850–2852, lo usa para `α = 1 + θ`); M9 5503–5508 cumple «Lo que sigue» del cap. 2; el cap.
    4, 4961, retoma «el cap. 3 mostró que son ruido blanco».
11. **Los avisos de «fallo silencioso»** (M1 2812–2824, 2933–2937; M9 5295–5303): bien elegidos y cerrados en
    el M9. El problema no es lo que dicen sino dónde caen (§3).

---

## 7. Los diez problemas que más dañan la comprensión (orden de daño)

1. **El M1 empieza por los convenios de signo y las diferencias entre lenguajes** (2737–2825; 406 palabras y
   43 líneas de código antes de las raíces, 2827) con un ARMA(1,1) estimado con `arima()` en el primer bloque
   (2764): modelo, estimador y salida nuevos antes de que exista el modelo.
2. **El M5 se lee en un orden que desordena lo que enseña:** el ciclo (3922) antes que la tabla (4016), y el
   laboratorio que cumple el objetivo (4290) tras ~1 500 palabras, con el vocabulario del M8 (`fitdf`,
   AICc, Bartlett) ya en el ciclo.
3. **El M4 se construye sobre el ARMA, que se define en el M5** (3598 frente a 3902), con la recursión de
   ψ y π en un plegado (3679–3693) que el ejemplo a mano usa y con cuatro convenios de signo del π.
4. **El M9 pesa 1,31 veces lo declarado y apoya su pivote en una herramienta que ningún capítulo previo
   presenta** («elasticidad amplitud–nivel… el mismo diagnóstico del Capítulo 1», 5176–5178), con cifras
   que ningún código reproduce (la tabla de `b̂`, las variantes de λ, Shapiro, la media de la TRM) y
   `auto.arima` nombrado dos veces sin presentarse ni llamarse.
5. **No hay práctica hasta el M10.** Unos 120 minutos sin que se pida nada, frente al «Para practicar» por
   módulo del cap. 2; y los tres ejercicios del final dejan sin cubrir el M2, el M4 y el M7.
6. **Los minutos declarados no están medidos:** M1–M8 declaran 102 y miden 77,6; M9–M10 declaran 33 y miden
   43,1 (más 46,8 de lectura de quizzes), frente a la razón 1,0 del cap. 2.
7. **M10 hace tres cosas y su resumen no es lo último:** el encabezado, la barra lateral y el marcado le dan
   tres nombres; 639 palabras de material nuevo (PACF(p) = φ_p; el aviso del ARMA(2,2)) van después del
   resumen; y tres evaluaciones (autoevaluación, actividad Parcial 2, simulacro) se solapan, una de ellas
   atada a un parcial cuya fecha, según las notas del proyecto, ya pasó.
8. **Los módulos prometen «reconocer» y «medir» y el M6 solo muestra:** proceso rotulado, tres realizaciones
   fijas, sin distancia, con el código sin salida (4432–4433, 4447–4467, 8795–8813).
9. **Lo que los plegados guardan y el resto cita:** la recursión de ψ y π, `γ₀` y `γ₁` del ARMA(1,1), el
   argumento CSS/ML (citado como «paso 6» en 4758), `fitdf` y el Monte Carlo (citado como «paso 4» en 5084), el
   porqué del nombre «invertible» (3425–3427); y referencias a maquinaria que el lector no ve (3683–3685,
   3701–3704, 6013–6015).
10. **Costuras de notación y de vocabulario:** `T` y `n` (incluso en la misma banda), «identificado» e
    «identificación», `ρ_k = 0` de la PACF (3110), «abanico» con dos sentidos, «caminata»/«paseo»,
    pseudo-ciclo/pseudo-periodo/periodo, `j` y `h = j + 1`, «el envolvente», «Módulo N» y «3.N»; y un encabezado
    («Donde sí hay estructura: en el cuadrado», 5558) que dice lo contrario de lo que sigue.
