# Capítulo 2 leído como estudiante · hilo narrativo y comprensión

Archivo leído: `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (commit `4b71366`; los nueve
`<template id="module-N">` enteros, en orden, líneas 2180–4287), más el JavaScript de los simuladores y
de la autoevaluación (5540–6060, para saber qué dice cada lectura numérica y qué series ofrece cada
selector), el cierre del capítulo 1 (`capitulo-1-componentes-descomposicion.html`, módulo 9, 5273–5700,
y los pasajes del capítulo 1 que prometen algo al 2: 2886–2900, 3303–3345, 3388–3395, 3456–3466,
4305–4316), la apertura del capítulo 3 (`capitulo-3-modelos-ar-ma-arma.html`, módulo 1, 2575–2838, y
sus remisiones al 2: 2889, 5071, 5403, 6114–6132) y la tarjeta de `Htmls_Series/index.html` (668–686).
Las líneas citadas son del capítulo 2 salvo indicación. Lente: comprensión y hilo; no se juzga corrección
técnica ni fuentes. No se editó nada fuera de `diagnostico/cap2/`. **No se renderizó la página:** la
lectura es del marcado y del JS (qué texto genera cada simulador, no cómo se ve).

Nota sobre el capítulo 1: su estado en `HEAD` ya no es el que describe `diagnostico/cap1/lector_estudiante.md`
(se le añadió el gráfico de rezagos del M3, una frase de puente en el M9 y minutos medidos con fórmula).
Todas las comprobaciones de empalme de este documento son contra el capítulo 1 actual.

Cómo distingo lo medido de lo opinado: cada hallazgo lleva al final **(M)** si se comprobó con un
recuento, un `grep`, una lectura literal de dos líneas que se contradicen o un cálculo sobre los datos
incrustados (`DATOS_CAP2`), y **(O)** si es juicio de lector sobre dónde se pierde alguien. Las cifras de
carga salen de `diagnostico/cap2/diag/cuenta_cap2.py` (salida en `cuenta_cap2.out`).

---

## 1. Mapa del arco

| Mód. | Pregunta que abre | Con qué cierra | Transición de entrada | Declarado | Estimado (abierto) |
|---|---|---|---|---|---|
| M1 | ¿Qué es que una serie sea estacionaria y por qué se exige? | «Dos preguntas: ¿es estacionaria? y, si no, ¿cómo la transformo?» (2296–2297) | ✓ explícita con el cap. 1 (2199–2205) | 10 | 5,9 |
| M2 | ¿Cuál es la serie estacionaria más simple y cómo se ve su correlograma? | «El ruido blanco es también la meta… el corazón del Capítulo 3» (2410–2413) | ✓ el ruido blanco ya salió en el simulador del M1 (2245) | 8 | 6,9 |
| M3 | ¿Cómo se mide la dependencia y cómo se lee? | Aviso de regresión espuria: «otra razón para volverlas estacionarias» (2565–2569) | ✓ «traducción cuantitativa del gráfico de rezagos del Módulo 3 del Capítulo 1» (2439–2440) | 12 | 7,0 |
| M4 | ¿Qué le falta a la ACF? (el doble conteo) | Aviso «la misma banda, la misma trampa» (2748–2752); antes, el «Anticipo del Capítulo 3» (2693–2701) | **débil**: M3 cierra en regresión espuria y M4 abre en «doble conteo» (2595); no hay hilo entre las dos | 10 | 7,5 (9,0 con la derivación) |
| M5 | ¿Cómo separa un solo parámetro lo estacionario de lo que no? | El aviso determinista/estocástica «trabajo de las pruebas del Módulo 6» (2855–2861) y luego código | **débil**: «Casi toda la no estacionariedad interesante cabe en una sola ecuación» (2777) abre de cero; la PACF queda atrás | 12 | 8,0 |
| M6 | ¿Cómo se decide con un número y cuándo miente la prueba? | «Regla de trabajo» (3134–3139) y luego código | ✓ «Mirar el correlograma es indispensable, pero es subjetivo» (2942) | 14 | 9,9 |
| M7 | ¿Cómo se quita una raíz unitaria y cuánto cuesta? | La moraleja de las dos funciones KPSS (3487–3490) y luego código | ✓ «La diferenciación es la herramienta estándar para eliminar una raíz unitaria» (3256) | 12 | 11,0 |
| M8 | ¿Cómo se arregla la varianza? | Aviso del sesgo al deshacer (3636–3640) y luego código | ✓ «La diferenciación arregla la media, pero no la varianza» (3575) | 10 | 7,8 |
| M9 | ¿En qué orden se aplica todo? | Lecturas (4270–4285). **No hay puente al capítulo 3** | ✓ «Todo el capítulo se resume en una secuencia de decisiones» (3711) | 10 | 19,4 (27,7 con la autoevaluación) |

Declarado: 98 min. Estimado de lectura abierta (con pista y solución de los ejercicios, sin la derivación
plegada ni la autoevaluación): 83,3 min; con derivación y autoevaluación: 93,1 min. El total parece
razonable; el reparto no (ver §4). Detalle del convenio en §4.

### Lectura del arco

El capítulo se cuenta en tres tramos que el lector percibe: **leer** (M1–M4: qué es estacionario, qué es
ruido, qué dicen ACF y PACF), **diagnosticar y corregir** (M5–M8: la caminata, las pruebas, la diferencia,
la transformación) y **encadenar** (M9). El arranque es bueno (el empalme con el capítulo 1 es explícito y
el gráfico de rezagos «que vimos» ahora sí se vio) y la cadena M6 → M7 → M8 está atada con frases de
paso que prometen y cumplen («la diferenciación arregla la media, pero no la varianza», 3575).

Donde el hilo afloja:

- **El orden de los módulos es el inverso del orden del procedimiento.** El capítulo enseña probar (M6)
  → diferenciar (M7) → transformar (M8), y el pipeline del M9 manda transformar → diferenciar
  estacionalmente → diferenciar regularmente → probar. La «Regla de trabajo» del M6 (3135–3138) enuncia
  el orden correcto cuando el lector aún no tiene dos de sus tres piezas (la diferencia estacional es
  del M7; la transformación, del M8, aunque el logaritmo ya viene del capítulo 1). (M/O)
- **Lo que se usa antes de definirse es mucho** (tabla en §3): el estudiante lee `∇`, `TRM`,
  `raíz unitaria`, `ndiffs`, `log(AirPassengers)`, `ACF`, `banda` y `caminata aleatoria` entre uno y
  cuatro módulos antes de que existan. Cada uno por separado se soporta; juntos hacen del M3–M6 un tramo
  de confianza prestada. (M)
- **M3 → M4 y M4 → M5 sin puente.** Son los dos saltos más secos del capítulo. (O)
- **M5–M8 terminan en un bloque de código,** no en una idea. La moraleja de cada uno está una pantalla
  más arriba (3134–3139, 3487–3490, 3636–3640). El lector sale de cada módulo con código en la cabeza. (O)
- **El capítulo no se despide.** El cap. 1 cerraba con «Lo que sigue» (5689–5699); el 2 termina en
  resumen, autoevaluación, cinco ejercicios y lecturas. La única frase hacia el 3 en todo el M9 está
  enterrada en la solución del ejercicio 1 (4078–4080). (M)

### Promesas: hechas, cumplidas, incumplidas

| # | Dónde se promete | Qué | ¿Se cumple? |
|---|---|---|---|
| 1 | Cap. 1, 5697–5699 y 4311 | «Un residuo sin forma… tiene nombre, ruido blanco, y una manera de comprobarlo» / «el Capítulo 2 vuelve sobre el residuo con la autocorrelación» | **Parcial.** El nombre sí (2323–2333). «Una manera de comprobarlo» es solo contar barras contra la banda (2357–2363), que es juzgar a ojo, justo lo que el cap. 1 dijo que se dejaba atrás. La prueba formal, Ljung–Box, solo aparece como una columna sin explicar en el ejercicio 3 (4159, 4171, 4187) y se define en el cap. 3 (4773 de ese archivo). Y **ningún residuo de una descomposición** se grafica en todo el cap. 2: ninguna de las 8 series del explorador lo es (5586–5594). (M) |
| 2 | Cap. 1, 3337–3338, 3392, 3462 | La nube del gráfico de rezagos se resume en un número, la ACF, y el correlograma los dibuja todos; «0,760 y no 0,991» | **Sí.** 2439–2440, 2453–2462, 2512. Falta el guiño de vuelta a la explicación del divisor del cap. 1 («132 pares, 144 observaciones»), pero la cifra coincide. (M) |
| 3 | 2293–2297 | Dos preguntas (¿es estacionaria? ¿cómo la transformo?) | **Sí**, en M6 y M7–M8. |
| 4 | Objetivo M4 (2589–2590) | «Usar las dos [ACF y PACF] juntas como instrumento de identificación» | **No en el capítulo.** Hay un «Anticipo del Capítulo 3» de tres viñetas (2693–2701) y el explorador no tiene ninguna serie estacionaria AR o MA donde se vea cortar una de las dos. Se cumple en el 3 (2889 de ese archivo). (M) |
| 5 | 2860 | «Distinguirlas [tendencia determinista y estocástica] es justamente el trabajo de las pruebas del Módulo 6» | **No.** El M6 nunca trabaja esa distinción: el único uso de una variante con tendencia es un `kpss.test(sa, null = "Trend")` sin explicar (3189). (M) |
| 6 | 3137–3138 | «`ndiffs()` y `nsdiffs()` del Módulo 7 automatizan justamente ese orden» (transformar → estacional → regular) | **No como está dicho.** Cada función decide una sola diferencia (3396–3397, 3470–3472). Quien automatiza el orden es `preparar()` del M9 (3856–3873). (M) |
| 7 | 3357 | «`length()` sobre la serie doblemente diferenciada en el código de más abajo» (=131) | **No en el M7,** cuyos bloques no tienen `length(`. Sí en el M9 (3882). Cumple en otro sitio. (M) |
| 8 | 3797 | «Es la trampa del orden del Módulo 7» | **No.** El aviso del M7 (3272–3277) dice que el orden es algebraicamente igual y que FPP3 recomienda el estacional primero; no muestra ninguna trampa ni que cambie el número de diferencias, y el ejemplo del M7 (3467–3473) va regular primero. (M) |
| 9 | 3637–3640 (M8) | «Volveremos a esto en el Capítulo 6» (sesgo al deshacer) | **Sí** (cap. 6, 2953). |
| 10 | 4139–4140 (pista del ej. 3) | «Relee la caja de advertencia del Módulo 7» | **Ambigua.** El M7 tiene tres cajas de advertencia (3272, 3452, 3475) y ninguna dice que `ndiffs` sobre la serie cruda da 0. (M) |
| 11 | 4002 | «Seis preguntas» | **No:** el arreglo `AUTOEVALUACIONES['cap2']` trae ocho (5895, 5923, 5933, 5964, 5979, 6007, 6038, 6048). (M) |
| 12 | Tarjeta de `index.html` (680–682) | «Las pruebas ADF y KPSS —y por qué pueden contradecirse—» | **Parcial.** Se explica que las nulas son opuestas (2942–2970) y la fila «rechaza/rechaza» (2998–3001) manda a «revisar la especificación»; nunca se muestra un caso en que las dos se contradigan de verdad. (M/O) |

---

## 2. Dónde me pierdo, módulo por módulo

Etiquetas: **P** = pérdida de comprensión; **N** = dicho pero no mostrado; **D** = decoración, ruido o
repetición; **C** = carga. Al final de cada punto, **(M)** o **(O)**.

### M1 · Estacionariedad (2180–2300)

- **C 2207–2238 · dos definiciones y una nota antes de la primera imagen.** La primera figura llega en
  2242, tras ~60 líneas con la definición estricta (que el propio texto llama «imposible de verificar»,
  2214–2215), la débil y la relación entre ambas. El lector lee una definición que le dicen que no usará.
  Es el precio del objetivo («distinguir estricta de débil», 2192) y no se arregla quitándola, pero sí
  moviéndola después de la figura. (O)
- **P 2244–2245 · «la caminata aleatoria es literalmente la suma acumulada del ruido blanco de arriba».**
  Ruido blanco y caminata se usan aquí y en la tabla (2270, 2273–2275) un módulo y cuatro módulos antes de
  definirse (M2: 2326; M5: 2798). La tabla afirma `Var(y_t) = tσ²` (2275) y que la caminata viola «(2) y
  (3)» sin que el lector pueda ver por qué viola la 3. Se deriva en 2801. (M)
- **N 2285–2290 · «estacionalidad ≠ estacionariedad».** Muy bien dicho, pero con el ejemplo de la tabla
  (`AirPassengers`) y no con la imagen de una serie estacional con media anual constante. La única vez que
  se pone a prueba es la primera pregunta del quiz (5895). (O)
- **✓** El panel de tres series con el mismo generador (2240–2255) y la tabla de «qué condición falla»
  (2257–2283) son lo que el objetivo promete: reconocer a simple vista.

### M2 · Ruido blanco (2305–2416)

- **P 2345–2347 · el simulador habla de «función de autocorrelación muestral» y «banda»** y el código
  (2377) llama `acf()`, cuando ACF, correlograma y banda se definen en el M3 (2439–2466). Aquí el
  lector solo tiene que creer que «todas las barras deberían caer dentro de la banda». (M)
- **D 2335–2341 · el aviso de incorrelación frente a independencia va antes del simulador** y se
  despide hacia ARCH/GARCH «que quedan fuera de este curso». Es un desvío en el módulo más corto
  (335 palabras de prosa) y antes de que el lector haya visto un solo correlograma; el ejemplo de
  `x_t²` no se muestra. Mejor después de la nota de la banda (2357–2363). (O)
- **P 2358–2362 · «cada autocorrelación muestral se distribuye aproximadamente N(0, 1/T)».** Se da sin
  justificar y sin notación (`r_k` aparece en 2454). No impide leer la banda, que es lo que importa. (O)
- **N 2323–2324 · «el ladrillo con el que se construyen todos los modelos del curso».** Se afirma en
  una línea. El primer modelo construido con él es el AR(1) del M5 (2781); ningún ejemplo del M2 lo
  muestra. Es la mitad del objetivo («bloque de construcción y objetivo final», 2317–2318). (O)
- **✓ 2357–2363 y 2409–2414.** «Una barra fuera de la banda no es evidencia de nada; un patrón sí» y
  «el ruido blanco es también la meta» son las dos frases que el lector se lleva.

### M3 · Autocorrelación y correlograma (2421–2572)

- **P 2514–2518 · la fila «Decaimiento rápido (exponencial)» ilustra otra cosa.** La etiqueta promete
  un decaimiento exponencial; el ejemplo es `∇TRM: r₁ = 0,088, todo lo demás dentro de la banda`. En los
  datos del propio capítulo (`DATOS_CAP2`) esa serie tiene n = 137, banda ±0,1675: `r₁` **también** cae
  dentro de la banda y solo el rezago 8 se sale. Es decir, el ejemplo de la fila 4 es lo que la fila 1
  llama ruido blanco, y el lector que abre el explorador del M4 y elige `∇ TRM` no ve decaimiento
  alguno. El decaimiento exponencial real aparece en el M5 (2789) y en su simulador. (M)
- **P 2506, 2517 · «raíz unitaria», «hay que diferenciar», `∇TRM` y `TRM`** se usan sin definirse: `∇`
  se define en 3264 (M7); `TRM`, en 3008 (M6); «raíz unitaria», en 2790–2808 (M5). Cada módulo de
  `TRM`/`∇` que se abre después lo da por sabido. (M)
- **P 2457–2463 · «semidefinida positiva» y «los algoritmos de estimación necesitan».** Jerga que se
  explica en el cap. 3; el cap. 1 (3337–3345) ya había dado el divisor de manera más llana. (O)
- **P 2439–2447 y 2465–2487 · se define ρ_k para un proceso estacionario y se lee su estimación sobre dos
  series que no lo son.** El módulo nunca dice que la `r_k` de una caminata o de `AirPassengers` no estima
  un `ρ_k` bien definido: es solo una huella descriptiva. Un estudiante cuidadoso se pregunta «¿qué mide
  la ACF de la caminata?». (O)
- **P 2565–2569 · «regresión espuria» y «correlación cruzada»** entran en un aviso final, sin nombre
  definido ni figura; el módulo no tiene más ejercicio que el simulador. (O)
- **✓ 2468–2487.** «Las mismas tres series del Módulo 1, ahora vistas por su ACF» (2470): el hilo con el
  M1 está a la vista.

### M4 · Autocorrelación parcial (2577–2754)

- **P 2660–2666 · la caja «Verificación»** habla de que el correlograma «no lo calcula el navegador»,
  de un JSON y de «una diferencia máxima de 6,2 × 10⁻⁵»; la derivación plegada termina remitiendo a
  «la función `calcularPACF()` que mueve los simuladores de los capítulos 3 y 5» (2654–2656). Es
  información sobre cómo se construyó la página, no sobre la PACF. Va justo antes del explorador. (M)
- **N 2693–2701 · el «Anticipo del Capítulo 3» da la regla (PACF que se corta → AR(p); ACF que se corta →
  MA(q))** sin que el explorador ofrezca una sola serie donde se vea. Las ocho series (5586–5594) son
  ruido blanco, caminata, `AirPassengers` en nivel, en log, diferenciada una y dos veces, `TRM` y `∇TRM`.
  Ninguna es un AR o un MA estacionario. La única PACF que se lee en el módulo es la de la caminata
  (2688–2691). (M)
- **P 2668–2686 · el explorador abre en `AirPassengers`,** y en esa serie la PACF tiene seis barras
  fuera de la banda (rezagos 1, 2, 9, 10, 11 y 13), en un módulo que acaba de decir «uno o dos picos
  fuera son lo normal» (2748–2752). Nadie la lee. La intro (2670–2672) manda al lector a comparar la
  caminata con `AirPassengers`, pero sobre la PACF de `AirPassengers` el módulo no dice nada. (M)
- **N 2715–2716 y 2744 · el código calcula `round(p[1:3], 4)` y `np.round(p[:3], 4)` sin decir el
  resultado,** cuando el bloque del M3 sí lo hacía (2533, 2561). El lector corre el código y no sabe
  qué valor esperar. (M)
- **P 2640–2646 · en la derivación plegada,** «Toeplitz», `O(k³)` y la varianza del error de predicción:
  opcional, plegada, correcto. (O)
- **P 2595–2597 · «doble conteo».** Es una buena intuición, pero la frase «hoy depende de ayer, y ayer
  de anteayer» describe un AR(1) sin nombrarlo, y el AR(1) no existe hasta el M5. El lector tiene la
  intuición sin el modelo. (O)
- **✓ 2688–2691.** «La ACF cuenta la historia acumulada; la PACF, la conexión directa».

### M5 · Caminata aleatoria y raíz unitaria (2759–2919)

- **P 2804–2808 · la raíz unitaria en cinco líneas.** Operador `B`, polinomio característico, raíz
  `z = 1/φ`, círculo unitario, todo dentro de una caja de definición y sin ejemplo. Es la compresión más
  alta del capítulo y se vuelve a explicar con calma en el cap. 3 (2737–2740 de ese archivo, que dice
  «la palabra *fuera* sorprende la primera vez»). El lector del cap. 2 la recibe primero en la versión
  corta. (O)
- **P 2835–2837 · «con la primera diferencia activada, cualquier φ produce algo que ya se parece a
  ruido blanco… y con φ pequeño produce autocorrelación negativa en el rezago 1».** En una sola frase,
  «se parece a ruido blanco» y «tiene autocorrelación negativa»; el lector no sabe en cuál confiar. Además
  «primera diferencia» (2815, 2835) se usa dos módulos antes de la definición de `∇` (3264). (M/O)
- **P 2852–2853 · «pronóstico ingenuo (naïve)»** sin definir; el cap. 1 no lo usa. (M)
- **N 2832–2834 · «con φ = 0,95… cuesta distinguirla de una raíz unitaria».** Es el caso difícil que
  justifica las pruebas del M6, pero el simulador no permite ver una PACF (solo hay serie y ACF; la ACF se crea en 5668 y no hay gráfico de PACF en 5644–5717),
  y por tanto tampoco la parte del «anticipo» del M4 que dice que el AR(1) tiene PACF de un solo pico. (M)
- **✓ 2813–2816 y 2827–2838.** Es el simulador mejor guiado del capítulo: la intro dice qué mover y qué
  mirar, y la caja «Tres cosas que vale la pena probar» da los valores exactos (0,5; 0,95; con diferencia).
- **P 2855–2861 · «Distinguirlas es justamente el trabajo de las pruebas del Módulo 6»:** ver promesa 5.

### M6 · Pruebas ADF y KPSS (2924–3233)

- **P 2949–2950 · `γ` es el coeficiente de la regresión del ADF** y `H₀: γ = 0`. Pero `γ_k` (2229, 2444)
  y `γ₀` son la autocovarianza desde el M1. El mismo símbolo con dos significados, a 700 líneas, y el
  texto no avisa que el del ADF es `γ = φ − 1` (solo dice «equivalente a φ = 1»). (M)
- **P 2949 y 3033 · `∇y_t` y `∇TRM` otra vez antes del M7.** (M)
- **P 2958 y 3110 · «estacionaria» cambia de sentido.** El M1 la define con media constante (2226); el
  KPSS contrasta «estacionaria (en nivel o alrededor de una tendencia, según la variante)» (2958–2960) y
  el ejemplo de `AirPassengers` desestacionalizada usa `null = "Trend"` (3189): una serie con tendencia
  determinista sería «estacionaria» aquí y no cumpliría la condición (1) del M1. La palabra
  «estacionaria en tendencia» nunca se nombra. (O)
- **P 3056–3058 vs 3084 · el −7,32 y el −6,422 del mismo caso (k = 5).** El texto dice que sobre
  `AirPassengers` el ADF devuelve «−7,32 con p < 0,01». La tabla de debajo da, para k = 5 (por defecto),
  `−6,422`. Son dos series distintas (la primera cruda, la segunda en logaritmos) pero la única palabra que
  lo dice es «log(AirPassengers)» en el `caption` oculto de la tabla (3072, `sr-only`); a la vista, las
  dos cifras compiten por el mismo caso. El código solo reproduce la cruda con k = 5 (3179), el k = 12
  en logaritmos (3183) y la desestacionalizada (3187–3188); las filas k = 11, 13 y la de −6,422 no tienen
  línea de código. Es el pasaje del capítulo que más obliga a releer. (M)
- **P 3109–3113 y 3187 · la tercera «evidencia» también es en logaritmos** (`stl(log(AirPassengers))`) y
  el texto no lo dice. El log llega a esta página sin explicación: se explica en el M8 (3575–3580) y en el
  cap. 1 (donde el lector ya lo vio). El M6 no remite a ninguno de los dos. (M)
- **P 3068–3069, 3182 · «ciclo completo»** significa aquí «periodo estacional»; el cap. 1 dedicó un
  recuadro entero a que ciclo ≠ estacionalidad (cap. 1, 3513). (M)
- **P 3115–3118 vs 3123 · «amplitud creciente».** El texto describe series «de amplitud creciente»; el
  simulador usa `A sin(2πt/12)` con `A` fija por barra (la amplitud crece entre barras, no dentro de
  cada serie). Un lector que lee 3116 espera el abanico del cap. 1. (O)
- **N 3135–3138 · la «Regla de trabajo» da el orden sin práctica,** con dos pasos que aún no se han
  enseñado (promesa 6). (M)
- **C 3148–3167 · el bloque de la TRM descarga datos vivos** (`datos.gov.co`, hasta el último mes
  cerrado) mientras el texto y los comentarios llevan cifras congeladas «al corte de junio de 2026,
  T = 138» (3008–3009, 3167, 3170–3175). Hoy (noviembre) quien lo corra obtendría unos cuatro meses más (n ≈ 142) y otras cifras,
  y no hay una frase que diga «las cifras pueden diferir de las de la página». El ejercicio 4 sí lo dice (4213–4214),
  tres módulos más tarde. No ejecuté la descarga; otro diagnóstico del mismo árbol (`diag/e4_trm_actualizada.out`, 2026-11-16) sí lo hizo y da n = 142 y un ADF de la TRM de −1,354 frente a los −1,978 de la página. (M)
- **✓ 3054–3132 y 4116–4120.** El caso tramposo es el mejor pasaje del capítulo como estructura:
  afirmación, mecanismo, tres evidencias, un número (3,2 % frente a 17,6 %) y un ejercicio que cierra
  contra el 4,6 %.

### M7 · Diferenciación (3238–3552) · el módulo con más prosa del capítulo (1 079 palabras)

- **P 3380–3382 vs 3393–3399 · «las tres señales» son dos tríos distintos a quince líneas.** La intro del
  simulador dice «la forma de la serie, el correlograma y la varianza»; la lista de debajo dice
  «el correlograma, las pruebas del Módulo 6 y la varianza». Y 3489 y 4022 repiten el segundo. El
  simulador no tiene panel de pruebas (solo imprime `ndiffs (R)` en la lectura, 5795). (M)
- **P 3272–3277 vs 3467–3473 · el orden de las diferencias se cuenta tres veces y no coincide.** El aviso
  dice «primero la estacional» (3274); la práctica del propio módulo aplica la regular primero (el
  KPSS no rechaza, `ndiffs` da 0) y descubre luego que `nsdiffs` sigue pidiendo 1 (3467–3470);
  el M9 vuelve a «primero la estacional» y lo llama «trampa» (3797). El lector concluye que el orden
  importa sin haber visto un solo caso en que cambie el resultado. (M)
- **P 3458–3462 · «MA(1) con θ = −1… no invertible»** en una caja de advertencia del M7, y la primera
  pregunta de selección múltiple sobre sobrediferenciación lo evalúa (5964–5970). MA(1), θ e
  invertibilidad son vocabulario del cap. 3; el M7 no lo marca como adelanto (el M4 sí marcó el suyo,
  2693). (M)
- **P 3475–3491 · «Dos funciones de R que dicen "KPSS" y no dan lo mismo».** Truncamiento de rezagos
  de la varianza de largo plazo, `urca::ur.kpss` frente a `tseries`, 0,368 / 0,091 frente a 0,537 y 0,463.
  Es la pasada más técnica del capítulo, y los números que cita no se pueden reproducir con el código del
  módulo: el bloque R solo llama `ndiffs(dd)` y `nsdiffs(dd)`, no `kpss.test(d12)` ni `ndiffs(d12)`
  (3499–3524). La moraleja («documenta cuál usaste») es buena y se entiende sin los números. (M/O)
- **N 3465–3473 · la diferencia estacional es la menos mostrada del capítulo.** El simulador del módulo
  solo diferencia de forma regular (`d` de 0 a 3, 5804); lo estacional vive en una tabla de siete
  filas (3290–3353), un párrafo y el código. El explorador del M4 sí trae `∇₁₂∇ log(AirPassengers)`
  (5592), pero el M7 no manda a verlo. (M)
- **P 3357 · `length()` «en el código de más abajo»:** ver promesa 7.
- **D 3360–3372 · la nota «el costo es absoluto, no proporcional»** vale (9 %, 22 %, 36 %), pero repite
  lo que 3355–3358 acaba de decir; el cuarto párrafo («Ese es el argumento cuantitativo detrás de la
  advertencia anterior…») conecta con el aviso de 3272 que quedó 90 líneas atrás. (O)
- **✓ 3279–3358.** «El precio de cada diferencia» es una tabla en la que se ve qué falta (`—` y la
  razón) y una cuenta que sale sola (131 = 144 − 12 − 1). Es la forma en que debería aparecer cada idea
  del capítulo.

### M8 · Logaritmo y Box–Cox (3557–3688)

- **P 3575–3577 · el módulo explica ahora por qué se usó el logaritmo en M6 y M7.** La dispersión
  «crece con el nivel» es la causa de todos los `log(AirPassengers)` anteriores. El lector ya los vio en
  M6 (3072, 3183, 3187) y en M7 (3407, 3467, 3502–3504, 3518) cuando se le explica. (M)
- **P 3622–3633 · una nota con nueve cifras:** 0,530; 0,153; 0,081; −0,295; 88 %; 20 %; el intervalo
  [−0,41; −0,17]; 84 %; más tres razones. «El logaritmo se queda un 88 % por encima del mínimo» y «capta el 84 % de la
  mejora» están en la misma frase. Para releer. (O)
- **P 3632 vs 3636–3640 · «(3) deshacer la transformación es trivial» y, a diez líneas, «Al deshacer la
  transformación aparece un sesgo… la vuelta atrás no es simétrica».** Las dos cosas son ciertas en
  sentidos distintos (código frente a estadística), pero juntas parecen una contradicción. El objetivo
  del módulo es «saber deshacer la transformación» (3570). (M/O)
- **P 3649–3686 · `pasajeros` (Python) no se define en este bloque.** Ni en M7 (3531), ni en M8 (3678),
  ni en M9 (3919); se crea solo en los bloques de M3 (2552) y M4 (2733). Quien abra el M7 para practicar
  sin haber corrido el M3 y el M4 encuentra un `NameError`. R no tiene el problema (`AirPassengers` viene
  con R). (M)
- **✓ 3593–3608.** El simulador de λ con la curva de Guerrero y el punto naranja de «dónde estás» da la
  intuición antes de la definición del criterio (3610–3618).

### M9 · El pipeline de preprocesamiento (3693–4287) · el módulo más pesado, titulado «Cierre»

- **C 3714–3846 + 3848–3928 + 3950–4285.** Seis pestañas de pipeline, dos bloques de código (R y
  Python), una nota de ciencia de datos, la tabla-resumen, la autoevaluación, cinco ejercicios con pista
  y solución (tres con código y tabla) y las lecturas. Son 1 040 palabras de prosa y 2 057 con las
  soluciones abiertas; con la autoevaluación se llega a 27,7 min frente a 10 declarados (§4). El título
  del sidebar («Pipeline, resumen y autoevaluación», 4304) tampoco menciona los ejercicios. (M)
- **P 3856–3886 vs 3714–3846 · el código numera cuatro pasos y el componente seis.** «1. Estabilizar la
  varianza» del código es el «Paso 2» del componente; «Graficar» y «Documentar» no están en el código. (M)
- **P 3859 · `if (abs(lambda) < 0.25) log(y) else BoxCox(y, lambda)`.** El umbral 0,25 sale de ninguna
  parte del M8, y con él `AirPassengers` (λ = −0,2947) **no** toma el logaritmo: toma `BoxCox` con
  λ = −0,2947. Es lo que M8 dice que «casi nunca» se hace (3623) y lo que M7 no hace en ningún bloque. La
  consecuencia visible es `var_final = 9,17e-05`, «NO comparable» con 0,01135 del M7 (3878–3879, 3427),
  y el bloque de Python (que sí usa el log, 3902) da 0,0021: el propio código lo reconoce en un
  comentario (3923–3926). Una misma serie, dos pipelines que difieren en el primer paso. (M)
- **P 3797, 3811 · «es la trampa del orden del Módulo 7», «el período»:** ver promesa 8; el resto de
  este capítulo escribe «periodo» (10 apariciones contra 1). (M)
- **P 3791, 3833 · «abombado», «Abombamiento».** Es la misma cosa que el cap. 1 llamó «abanico» (cap. 1,
  3253–3258) y que el M8 describe como «la dispersión crece con el nivel» (3576). El tercer nombre
  aparece por primera vez en el último módulo. (M)
- **P 3843, 4040 · `D`** (diferencias estacionales) no se define en ningún sitio; `d` sí (cabecera de la
  tabla del M7). (M)
- **N 3950–3998 · el resumen no recoge** el único mensaje que el M6 pidió «grabarse» (las dos nulas son
  contrarias, 2943–2944), ni el aviso del ADF sobre series estacionales, ni la sobrediferenciación, ni
  las bandas, ni el propio pipeline. Recoge nombres y comandos. (M)
- **P 4000–4011 y 5895–6060 · la autoevaluación no toca M2, M4 ni M9.** Cuenta: M1 ×1, M3 ×1, M5 ×1,
  M6 ×1, M7 ×3, M8 ×1. Nada sobre PACF ni sobre ruido blanco; tres sobre diferenciación. (M)
- **P 4020–4082 · ejercicio 1** pide «aplica el pipeline» sobre `co2` y la solución descarta el primer
  paso («se trabaja sin transformar», 4047), con un criterio (el nivel solo varía un 15,9 %) que ni el M8
  ni el M9 enseñan: ambos dicen «transformar si la dispersión crece», y esta es la única serie del capítulo
  donde la respuesta es no. Es un buen ejercicio, y justamente por eso la regla necesita estar dicha antes. (O)
- **P 4125–4192 · el ejercicio 3** usa una columna de Ljung–Box (4159, 4171, 4187) que el capítulo no
  define y pide «residuales» de series que solo se han diferenciado, sin modelo (4126). «Residuales» tiene
  aquí un cuarto sentido (ver §3). (M)
- **D 4263–4265 · el cierre del ejercicio 5 («un asistente es útil para generar hipótesis…») es la mejor
  frase de método del módulo y está en el último panel plegado, al final de la página.** (O)
- **✓ 3714–3846.** Las pestañas «Qué te devuelve atrás» son lo que une este capítulo con el bucle del
  residuo del cap. 1: cada paso dice qué hallazgo manda de vuelta a cuál. Es la pieza que el lector más
  se llevaría si el módulo no tuviera tanto alrededor.

---

## 3. Problemas transversales

### Lo que se usa antes de definirse

| Término | Primer uso (línea) | Definición (línea) | Distancia |
|---|---|---|---|
| ruido blanco | 2245, 2270 (M1) | 2326–2332 (M2) | 1 módulo |
| caminata aleatoria, `Var(y_t) = tσ²` | 2245, 2273–2275 (M1) | 2790–2803 (M5) | 4 módulos |
| ACF, correlograma, banda ±1,96/√T | 2345–2347, 2358–2362 (M2) | 2439–2466 (M3) | 1 módulo |
| `∇`, «primera diferencia», «diferenciar» | 2506, 2517 (M3); 2815, 2835 (M5); 2949 (M6) | 3264 (M7) | 4 módulos |
| `TRM` | 2517 (M3); explorador (5593) | 3008 (M6) | 3 módulos |
| «raíz unitaria» | 2506 (M3) | 2790–2808 (M5) | 2 módulos |
| `ndiffs`, `nsdiffs` | lectura del explorador (5629–5630, M4); 3138 (M6) | 3396–3397, 3470 (M7) | 3 módulos |
| `log(AirPassengers)` (el porqué) | 3072, 3183 (M6) | 3575–3580 (M8) y cap. 1 | 2 módulos |
| «diferencia estacional» | 3137 (M6) | 3265 (M7) | 1 módulo |
| `AR(p)`, `MA(q)` | 2697–2698 (M4, marcado «anticipo») | cap. 3 | — |
| `MA(1)`, `θ`, «no invertible» | 3459–3461 (M7, **no** marcado) | cap. 3 | — |
| `Ljung–Box` | 4159, 4171, 4187 (M9) | cap. 3 (4773) | otro capítulo |
| `D` (diferencias estacionales) | 3843 (M9) | — | nunca |

### Vocabulario que cambia de sentido o de nombre

- **«ciclo».** En el M6 y el M7 es el periodo estacional (3069, 3182, 3266), con el recuadro del
  cap. 1 («ciclo ≠ estacionalidad») aún vigente; en el M9 es el bucle del pipeline (3714–3846). Hereda
  las dos de las tres acepciones que el cap. 1 ya tenía. (M)
- **«residuo / residuales».** Componente `R_t` del cap. 1 (2199); residuo de una regresión interna del ADF
  («se queda en el residuo», 3064, 4252); residuales de un modelo ajustado (2411–2412, 3969); y los
  «residuales» de una serie solo diferenciada (4126). (M)
- **«estacionaria».** Media constante (M1, 2226) frente a «alrededor de una tendencia» (M6, 2958–2960,
  3110–3111). (O)
- **`γ`.** Autocovarianza `γ_k` (M1, M3) frente al coeficiente del ADF `γ` (M6, 2949–2950). (M)
- **`k`.** Rezago de la ACF (2229, 2444, tabla de 2507) frente al número de rezagos aumentados del ADF
  (3062, tabla de 3075, ejercicio 5, 4251–4254); y en el M1 el desplazamiento se llama `h` (2211) y en el
  M5 también (2788) mientras la covarianza usa `k` (2229). (M)
- **`T` y `n`.** `T` en M2, M3, M6, M7 (2360, 3009, 3123, 3286); `n` en el mismo M7 (3478), en la tabla
  y la solución del M9 (4076, 4169, 4214); y en los simuladores, `T =` en M2 y M4 (5561, 5625) y `n =`
  en M7 (5792). (M)
- **«abanico» / «dispersión que crece con el nivel» / «abombado».** Tres nombres para el mismo hecho
  (cap. 1, 3253; 3576; 3791, 3833). (M)
- **«primera diferencia» / «diferencia regular» / «de primer orden» / `∇`.** Cuatro nombres, dos de ellos
  en simuladores, antes de que el M7 los iguale. (M)
- **«pipeline» / «procedimiento» / «secuencia de decisiones» / «ciclo».** El M9 lo llama de las cuatro
  maneras (3699, 3705, 3711, 3714); el sidebar, «Pipeline, resumen y autoevaluación»; el resumen no lo
  menciona. (M)
- **«serie» / «proceso» / «realización».** El M1 define el proceso `{y_t}` (2210), habla de «una sola
  realización» (2215) y a la vez de «una serie es estacionaria» (2205). Sin avisar. (O)
- **«las tres señales».** Dos tríos distintos (M7, 3380–3382 y 3393–3399); ver M7. (M)

### Una nota sobre las cifras que se repiten

Las cifras de la TRM (T = 138; ADF −1,978; KPSS 2,243; ∇TRM con r₁ = 0,088; varianzas 338 834 y 14 800)
aparecen en M3, M6, M7, M9 y en la solución del ejercicio 4. Eso une el capítulo (la TRM es el hilo
numérico de la segunda mitad); es lo que el cap. 3 reutiliza (5403 de ese archivo) y funciona. El riesgo
es el que se señaló en el M6: el código descarga datos actuales y las cifras de la página no cambian. (O)

### Voz

La prosa de M1–M8 está en primera persona del plural («descompusimos», «damos», «Apliquemos»:
35 formas en los ocho módulos, con 17 de segunda persona sueltas) y la de M9 en segunda persona (55 entre imperativos y formas de
«tú»; recuento por expresión regular, aproximado). La convención del curso es impersonal fuera de simuladores y ejercicios; en el M9 el componente
de pestañas (3766–3845: «Qué haces», «Qué te devuelve atrás», «te pasaste», «no se lo puedes enseñar a
nadie») es prosa expositiva. No es de este lente; se anota porque el cambio de persona entre el M8 y el
M9 se oye. (M)

---

## 4. Carga

Convenio y números: `diagnostico/cap2/diag/cuenta_cap2.py` (adaptación de `cuenta_cap1_v2.py` con el
convenio de `r5_minutos.py`, que es el que usa hoy el cap. 1 para declarar sus minutos). Fórmula:
palabras de prosa / 180 + 3 por simulador + 2 por bloque de código (un par de pestañas R/Python cuenta
como un bloque). **Convenio de palabras:** se quitan `<pre>`, `<script>`, `<style>`, `<canvas>`, `<svg>`,
botones, el `caption` oculto, el pie de fuentes y el bloque del quiz; se quita la matemática en bloque;
cada fórmula en línea cuenta como **una** palabra; las celdas de las tablas cuentan como palabras; la
derivación plegada del M4 va aparte. **Diferencia con `cuenta_cap1_v2.py`:** aquel no quita `<pre>` y
cuenta el código como prosa (en este capítulo, 1 917 palabras de código); el convenio de `r5_minutos.py`
sí lo quita. «Cerrado» deja pista y solución de los ejercicios sin abrir; «abierto» las cuenta. La
autoevaluación (8 preguntas: 418 palabras de enunciados y opciones, 1 069 de pista y retroalimentación =
8,3 min) y los 262 palabras de la derivación del M4 (1,5 min) van fuera de ambas columnas. Ninguna
columna incluye el tiempo de hacer los ejercicios. El `data-ciclo` del M9 (seis pestañas) no se cuenta como
simulador, como hizo el cap. 1 con su componente equivalente; contarlo sumaría 3 min.

| Mód. | Palabras (cerrado) | Sim. | Bloques | Cerrado (min) | Abierto (min) | Abierto + deriv. (min) | Declarado (min) | Razón abierto / declarado |
|---|---|---|---|---|---|---|---|---|
| M1 | 521 | 1 | 0 | 5,9 | 5,9 | 5,9 | 10 | 0,59 |
| M2 | 335 | 1 | 1 | 6,9 | 6,9 | 6,9 | 8 | 0,86 |
| M3 | 352 | 1 | 1 | 7,0 | 7,0 | 7,0 | 12 | **0,58** |
| M4 | 453 | 1 | 1 | 7,5 | 7,5 | 9,0 | 10 | 0,75 (0,90) |
| M5 | 537 | 1 | 1 | 8,0 | 8,0 | 8,0 | 12 | 0,67 |
| M6 | 876 | 1 | 1 | 9,9 | 9,9 | 9,9 | 14 | 0,70 |
| M7 | 1 079 | 1 | 1 | 11,0 | 11,0 | 11,0 | 12 | 0,92 |
| M8 | 508 | 1 | 1 | 7,8 | 7,8 | 7,8 | 10 | 0,78 |
| M9 | 1 040 (2 057 abierto) | 0 (+1 ciclo) | 1 (+3 en soluciones) | 7,8 | **19,4** | 19,4 | 10 | **1,94** |
| **Total** | 5 701 (6 718) | 8 | 8 (+3) | 71,7 | 83,3 | 84,8 | 98 | 0,85 |
| Con autoevaluación | | | | | 91,6 | 93,1 | | 0,93 / 0,95 |

Para ver el reparto: M1–M8 suman 88 min declarados y 64,0 min medidos (cerrado = abierto, porque no tienen
ejercicios), el 73 %. M9 declara 10 y mide 19,4 (27,7 con la autoevaluación). El total (98 frente a 93,1)
parece correcto porque el exceso de M9 compensa el defecto de los ocho anteriores. Los minutos declarados
(10, 8, 12, 10, 12, 14, 12, 10, 10) son números redondos que no parecen medidos; el cap. 1 declara ahora lo
que mide su fórmula (`courseData`, líneas de comentario de la R5). Con la misma convención el cap. 2 tiene
5 701 palabras de prosa frente a las 12 036 del cap. 1 (según `diagnostico/cap1/comprobaciones/r5_minutos.out`):
es un capítulo de la mitad de prosa. (M)

### Qué se desbalancea

- **M9 pesa casi el doble de lo declarado** (y ≈ 2,8× con la autoevaluación), y es el último que el
  lector lee, cuando ya lleva ~85 min. Un módulo «de cierre» con cinco ejercicios, el pipeline,
  un bloque de ciencia de datos, el resumen y el quiz. (M)
- **M3 y M1 están muy por debajo de lo declarado** (0,58 y 0,59): M3 es el módulo de la herramienta central
  del capítulo (el correlograma) y tiene 352 palabras. Es donde caben los arreglos de §3: definir los
  símbolos, un ejemplo de decaimiento exponencial de verdad, el sentido de la `r_k` en una serie no
  estacionaria. (O)
- **M7 es el más cargado de los ocho** (11,0 min, 1 079 palabras, tres subtítulos, tres cajas de
  advertencia, dos tablas) y concentra dos de las pasadas más técnicas del capítulo (MA(1) no
  invertible, truncamiento del KPSS). El M6 es el segundo en prosa (876 palabras) y trae
  la trampa del ADF, el Monte Carlo y la descarga de la TRM. (M)
- **El título del capítulo promete ACF y PACF; el capítulo gasta su prosa en otra cosa.** M3 + M4 suman
  805 palabras (14 % de las 5 701); M5–M8 suman 3 000 (53 %). La tarjeta de la portada (680–682) lista el
  temario, no el argumento (hay que llegar a una serie estacionaria: probar, diferenciar, transformar, en
  este orden), y la tarjeta no menciona el pipeline. (M/O)

### Dónde partiría o movería (sin renumerar; de mayor a menor rendimiento)

1. **Declarar lo medido:** M1 6, M2 7, M3 7, M4 8 (9 con la derivación), M5 8, M6 10, M7 11, M8 8,
   M9 19 (27 con la autoevaluación). Es lo que hizo el cap. 1 y no cuesta nada.
2. **Añadir un «Lo que sigue» al M9** (lo que ya existe en el cap. 1: 5689–5699), antes del quiz o al
   final, con el hilo que el 3 retoma: la regla de la ACF y la PACF (2693–2701), `B` (3261), el residuo
   que debe ser ruido blanco (2410–2413) y la serie `∇₁₂∇ log` que el 5 ajustará (3472–3473).
3. **Definir `∇`, `TRM` y «raíz unitaria» en el punto donde se usan por primera vez** (M3, 2506 y 2517)
   con una línea y una remisión; es 20 palabras y quita la confianza prestada de M3–M6.
4. **Dar al M4 una serie donde se vea cortar la PACF** (un AR estacionario) y mostrar la ACF y la PACF
   del AR(1) en el simulador del M5: con una serie y un panel más se cumpliría el objetivo declarado
   del M4 (2589–2590). Y cambiar el ejemplo de la fila 4 de la tabla del M3 (2514–2518) por esa serie.
5. **M6: hacer visible el logaritmo** («en logaritmos», una vez en 3056 y otra en 3072) o recalcular el
   cuadro sobre la serie cruda; y mover el aviso de «El orden correcto» a después del M8.
6. **M7: unificar «las tres señales»** en un solo trío; escribir «el orden» una sola vez y con un caso
   donde cambie; o quitar la promesa del `length()` (3357) o añadirlo al bloque de código del módulo.
7. **M9: alinear `preparar()` con el M8** (umbral 0,25 de 3859 o λ = 0 con justificación) y numerar los
   pasos del código como los del componente; sacar «Verificación» (2660–2666) y `calcularPACF()`
   (2654–2656) de la prosa del estudiante.
8. **Autoevaluación:** «Ocho preguntas» (4002) y al menos una sobre PACF y otra sobre ruido blanco o el
   orden del pipeline.

---

## 5. Empalme con el capítulo 1, con el 3 y con la portada

### Lo que el capítulo 2 da por sabido del 1, y si el 1 lo da

| El cap. 2 supone… | ¿Lo enseñó el cap. 1? |
|---|---|
| tendencia, estacionalidad, residuo (2199) | Sí, a fondo. |
| `AirPassengers`: nivel que sube, dispersión que crece con el nivel (2203–2205, 2253, 3575–3577) | Sí (M1, M3, M4). |
| el gráfico de rezagos «que vimos en el Módulo 3» (2440) | **Sí, ahora.** El M3 del cap. 1 lo dibuja (cap. 1, 3303–3340), explica por qué la nube da 0,991 y la ACF 0,760, y remite al cap. 2 tres veces. La frase del cap. 2 es verdadera. |
| «dependencia temporal» (2200, 2204) | Sí (M1 y el gráfico de rezagos). |
| «una serie con estacionalidad no es estacionaria» (2285–2289) | El cap. 1 lo avisa al cerrar (cap. 1, 5689–5694) y el cap. 2 lo reitera. Bien. |
| `log(AirPassengers)` sin explicación en M6–M7 (3072, 3183, 3407) | El logaritmo sí se enseñó (cap. 1, M4 y M7), pero el cap. 2 no lo recuerda ni remite hasta el M8. |
| `gg_lag(y)`, `gg_season(y)` como paso de graficar (3773) | Sí: son el M3 del cap. 1. |
| STL (3109, 3187) | Sí (M7 del cap. 1). El cap. 2 solo lo usa de herramienta en una frase. |
| «un residuo sin forma» ≈ ruido blanco (2410–2413) | **Se nombra pero no se une:** el cap. 2 no vuelve al residuo de una descomposición (promesa 1). |
| ¿Por qué diferenciar estacionalmente si ya sé desestacionalizar? | **Sin respuesta.** El cap. 1 enseñó a quitar la estacionalidad con STL y a restarla del cociente; el cap. 2 la quita con `∇ₘ` sin decir en qué se distingue de aquello ni cuándo conviene cada una. (O) |

**Conclusión:** el empalme narrativo funciona y el probatorio mejoró (el hueco que el diagnóstico del cap. 1
señalaba, el gráfico de rezagos, se cerró). Lo que sigue abierto es el residuo («un residuo sin forma
deja de juzgarse a ojo» es verdad solo a medias, promesa 1) y el logaritmo sin remisión.

### Lo que deja preparado para el cap. 3

| El cap. 3 necesita… | ¿Lo deja el cap. 2? |
|---|---|
| `B` y `∇ = (1 − B)` (cap. 3, 2594–2596: «apareció, casi de contrabando») | Sí, **dos veces** (5: 2804–2808; 7: 3261–3268); el cap. 3 solo recoge la segunda. |
| «la raíz fuera del círculo» (cap. 3, 2737–2740: «la palabra *fuera* sorprende la primera vez») | Ya está en el M5 (2806–2808): el cap. 3 la presenta como nueva. Redundante, no roto. |
| la caminata como raíz unitaria y el KPSS que rechazaba (cap. 3, 2783–2786) | Sí (M5, M6). |
| «la PACF mide la correlación directa» (cap. 3, 2889) | Sí (M4, 2601–2607). La regla de corte la da el cap. 3: el cap. 2 solo la anticipa. |
| la TRM con raíz unitaria y primera diferencia estacionaria (cap. 3, 5403) | Sí (M6, 3043–3045). |
| `Box–Cox` y la prueba de la escala (cap. 3, 5071) | Sí (M8). |
| el ruido blanco como meta de los residuales (cap. 3, 3767, 4234) | Sí (M2, 2410–2413). La prueba formal (Ljung–Box) la define el cap. 3 (4773). |
| el ejercicio 1 anuncia «estructura ARMA que modelar… trabajo del Capítulo 3» (4078–4080) | Sí, pero ahí se queda: el M9 no tiene un puente propio. |

El cap. 3 también usa el material del 2 en su actividad preparatoria (6114–6132): estacionariedad débil,
caminata con deriva, ADF y KPSS, sobrediferenciación. Esos cuatro temas son del M1, M5, M6 y M7, es decir,
los módulos donde este documento encuentra los pasajes para releer (2804–2808, 2835–2837, 3054–3139,
3452–3491).

### La tarjeta de la portada (`Htmls_Series/index.html`, 668–686)

Texto: «Estacionariedad estricta y débil, ruido blanco, autocorrelación simple y parcial, caminata aleatoria
y raíz unitaria, las pruebas ADF y KPSS —y por qué pueden contradecirse—, diferenciación y
transformaciones de Box–Cox.» Meta: «9 módulos · 8 simuladores».

- **Cifras:** 9 módulos y 8 simuladores son correctas (8 `data-simulador` en M1–M8, ninguno en M9). El
  componente del pipeline del M9 no cuenta como simulador, igual que en el cap. 1. (M)
- **«y por qué pueden contradecirse»:** ver promesa 12. (M/O)
- **Lo que el capítulo más desarrolla y la tarjeta no dice:** la trampa del ADF con series estacionales
  (M6, tres evidencias y un Monte Carlo), el costo de datos de cada diferencia (M7) y el pipeline ordenado
  del M9. La tarjeta describe el temario; el capítulo gira en torno a un argumento (llegar a una serie
  estacionaria, en un orden que importa). (O)

---

## 6. Lo que funciona (no romper al revisar)

1. **M1 2240–2283 · tres series con el mismo generador y una tabla de «qué condición falla».** Es lo que
   el objetivo promete (reconocer a simple vista), y el M3 (2470) lo retoma con «las mismas tres series».
2. **M2 2357–2363 y 2409–2414 · «un patrón sí» y «el ruido blanco es también la meta».** Las dos frases
   que hay que llevarse del módulo.
3. **M5 2811–2838 · el deslizador de φ con la intro que dice qué mover y la caja de «tres cosas que vale
   la pena probar».** El patrón a replicar en los demás simuladores.
4. **M6 3054–3132 y 4116–4120 · el caso tramposo.** Afirmación → mecanismo → tres evidencias (rezagos,
   STL, Monte Carlo) → un número (3,2 % frente a 17,6 %) → el ejercicio 2 lo cierra contra un 4,6 %
   («el ADF no está roto»). Es la mejor estructura de método del capítulo.
5. **M7 3279–3372 · «El precio de cada diferencia».** Una tabla en la que lo que falta se ve (`—` con su
   razón), una cuenta que sale sola (131), una nota con tres porcentajes (9 %, 22 %, 36 %) y la misma cifra
   que el M9 devuelve (3882) y la autoevaluación pregunta (6038).
6. **M9 3714–3846 · «Qué te devuelve atrás».** El paralelo con el bucle del cap. 1 (el residuo manda de
   vuelta a un paso) es lo que une los dos capítulos en método.
7. **M9 4213–4225 y 4263–4265 · el ejercicio 4 que «no tiene una respuesta fija» y el cierre del 5**
   (verificar es ejecutar el código). Son las frases más honestas del capítulo; conviene que no queden
   solo en paneles plegados.
8. **Los empalmes explícitos con el cap. 1:** 2199–2205 (apertura) y 2439–2440 (rezagos) son verdad y
   se verifican en el otro archivo.

---

## 7. Los diez problemas que más dañan la comprensión (orden de daño)

1. **Lo que se usa antes de definirse (∇, TRM, raíz unitaria, ACF/banda, ndiffs, log) en M2–M6**
   (tabla de §3): cada módulo da por conocido algo que el siguiente define.
2. **M6, la trampa del ADF contada con dos series sin avisarlo** (−7,32 en 3057 y −6,422 en 3084;
   «log» solo en un `caption` oculto, 3072; la tercera evidencia también en log, 3187) y con `k` y `γ`
   cambiando de sentido (3062, 2949).
3. **El orden de las diferencias dicho tres veces** (3135–3138, 3272–3277, 3467–3473) y el M9 que lo llama
   «trampa» (3797) sin que el capítulo la muestre; con un pipeline de R que no usa el logaritmo
   (3859, `|−0,2947| ≥ 0,25`) que el M7 y el M8 usan.
4. **M3, fila 4 de la tabla del correlograma** (2514–2518): la etiqueta es «decaimiento exponencial» y el
   ejemplo (`∇TRM`) tiene todas las barras dentro de la banda salvo una. El decaimiento exponencial
   solo se ve en M5.
5. **La regla de identificación de M4 (2693–2701) nunca se ve en un caso:** las ocho series del
   explorador no incluyen un AR o MA estacionario, el simulador del M5 no dibuja PACF y el objetivo
   «usar las dos juntas como instrumento de identificación» (2589–2590) queda para el cap. 3.
6. **M7, tres pasajes técnicos adelantados sin marcar:** MA(1) con θ = −1 no invertible (3458–3462),
   las dos funciones KPSS (3475–3491), y una moraleja que se entiende sin ellos. La autoevaluación evalúa
   el primero (5964–5970).
7. **«Un residuo sin forma» (cap. 1) se queda a ojo:** no hay residuo de descomposición en todo el
   capítulo, la banda sigue siendo visual y Ljung–Box aparece sin definir en el ejercicio 3 (4159–4187).
8. **M9 pesa 1,9× lo declarado (2,8× con la autoevaluación), no tiene puente al cap. 3, dice «seis
   preguntas» sobre ocho y cierra con un resumen que no recoge las dos nulas contrarias, la trampa del
   ADF ni la sobrediferenciación** (3950–3998, 4002).
9. **Reproducibilidad:** la TRM se descarga viva y la página lleva cifras congeladas (3148–3175,
   4213–4214); y los bloques Python de M7, M8 y M9 dependen de `pasajeros`, que solo se crea en M3 y M4
   (2552, 2733).
10. **Costuras sin hilo y capítulo sin despedida:** M3 → M4 y M4 → M5 (2595, 2777), cuatro módulos que
    terminan en código (M5–M8) y cinco nombres para el pipeline y tres para el abanico (§3).
