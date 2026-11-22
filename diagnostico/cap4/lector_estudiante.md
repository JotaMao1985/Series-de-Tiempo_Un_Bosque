# Capítulo 4 leído como estudiante · hilo narrativo y comprensión

Archivo leído: `Htmls_Series/capitulo-4-modelos-arima.html` (árbol limpio en `71c42d8`; los doce
`<template id="module-N">` enteros y en orden, líneas 2749–5944), más el JavaScript que genera lo que el
estudiante ve en cada simulador (7936–8847: los once `SIMULADORES[...]`, selectores, rótulos y textos de
«lectura»; la tabla ordenable `TABLAS_RANKING['rejilla-nilo']`, 8855), la autoevaluación `AUTOEVALUACIONES['cap4']`
(8887–9078, enunciados, opciones, pistas y retroalimentación) y la forma del simulacro (9403–9545, de los enunciados
solo el encabezado). Para el empalme: el cierre del capítulo 3 (`capitulo-3-modelos-ar-ma-arma.html`, su módulo 10, 6887–7461,
con «Lo que viene» en 7435–7445), la apertura del 5 (`capitulo-5-sarima.html`, módulo 1 desde 3058, y sus remisiones al 4:
3076, 3564, 4067, 4086, 4111, 4321, 4586–4593, 4616, 4646, 4933–4938, 5166, 5570), la apertura del capítulo 6 donde remite
al 4 (4515–4596) y la tarjeta del 4 en `Htmls_Series/index.html` (719–745). Las líneas son del capítulo 4 salvo indicación.
Lente: comprensión e hilo; no se juzga corrección técnica, fuentes ni diseño de gráficas. **No se renderizó la página
ni se ejecutó ningún simulador:** la lectura es del marcado y del JS (qué texto genera cada simulador, no cómo se
ve ni cómo responde). No se ejecutó el código R ni el Python; cuando se dice que una cifra «no sale de ningún bloque»
es una búsqueda de la cadena en los `<pre>` (ver §3). No se editó nada fuera de `diagnostico/cap4/`.

Cómo distingo lo medido de lo opinado: cada hallazgo lleva al final **(M)** si se comprobó con un recuento, un `grep`,
una lectura literal de dos líneas que se contradicen o la comparación con otro archivo, y **(O)** si es juicio de
lector sobre dónde se pierde alguien. Las cifras de carga salen de `diagnostico/cap4/diag/lector_carga.py` (salida en
`lector_carga.out`; la misma medición sobre el capítulo 3 actual, en `lector_carga_cap3.out`); las de términos,
remisiones, notación y voz, de `lector_terminos.py`; las de «dicho pero no mostrado», de `lector_cifras.py`; las de la
autoevaluación, de `lector_quiz.py`; el tamaño de cada sección, de `lector_secciones.py`; las introducciones de
simulador y los párrafos más largos, de `lector_intros.py`; y la densidad de cifras, de `lector_numeros.py` (con su
versión del capítulo 3).

Etiquetas de la §2: **P** = pérdida de comprensión; **N** = dicho pero no mostrado (o mostrado donde no puede
reproducirse); **D** = decoración, ruido o repetición; **C** = carga.

Qué trae el estudiante: viene del capítulo 3 ya revisado. Sabe AR, MA y ARMA con sus raíces, la invertibilidad, los
pesos ψ y π, la tabla de identificación (con «la tercera fila es la débil»), tres estimadores (Yule–Walker, CSS, ML),
AIC/AICc/BIC, Ljung–Box con `fitdf`, el abanico que se abre y «se para» en un proceso estacionario (manchas solares),
la TRM como ruido blanco en log-retornos, `RB(0, σ²)` (definido en 3133–3135 del capítulo 3), `auto.arima` nombrado en
«Lo que viene» y la advertencia «La trampa que reaparecerá en el Capítulo 4» (AICc entre distintos `d`). Del 2 trae ADF y
KPSS, `ndiffs()`/`nsdiffs()` (cap. 2, 4120–4130) y el operador `B`. No trae: Phillips–Perron (el cap. 2 solo nombra a
Phillips como autor del KPSS), suavizamiento exponencial ni Holt (0 líneas en los capítulos 1–3), `RMSE`/`MAE`
como medidas (el 6 las desarrolla), «fuera de muestra» (0 líneas en los capítulos 1–3), el Nilo, `BJsales`.

---

## 1. Mapa del arco

| Mód. | Pregunta que abre | Con qué cierra | Transición de entrada | Declarado | Medido (cerrado / abierto) |
|---|---|---|---|---|---|
| M1 · 4.1 De ARMA a ARIMA (2749–2996) | ¿Qué cambia si la diferencia entra en el modelo? | «el módulo siguiente presenta el procedimiento» (2992–2994), tras el aviso del signo de θ | ✓ «El Capítulo 3 terminó con un límite explícito» (2767) | 12 | 9,9 |
| M2 · 4.2 Box–Jenkins (2998–3212) | ¿Qué hallazgo obliga a volver a la etapa anterior? | «El módulo siguiente se dedica entero a ella» (3208–3210) | ✓ «El Módulo 1 dejó definido el modelo» (3016) | 10 | 6,5 |
| M3 · 4.3 Elegir d (3214–3534) | ¿Cómo se decide `d` y por qué pueden engañar las pruebas? | Mapa del resto: M4, M5–M7, M8 (3528–3532) | ✓ «El ciclo de Box–Jenkins empieza por d» (3232) | 16 | 12,8 |
| M4 · 4.4 Identificar p y q (3536–3702) | ¿Qué sugiere la ACF/PACF de la serie ya diferenciada? | «queda una decisión… la constante… Módulo 5» (3698–3700) | ✓ «El Módulo 3 dejó d = 1» (3554) | 14 | 8,9 |
| M5 · 4.5 La constante (3704–3897) | ¿Qué significa `c` según `d` y qué hace cada programa con ella? | «queda estimarlos y compararlos… Módulo 6» (3893–3895) | ✓ «la decisión que el Módulo 4 dejó pendiente» (3722) | 12 | 6,5 |
| M6 · 4.6 Estimar y comparar (3899–4085) | ¿Por qué el mínimo global de AICc no es la respuesta? | «no escala… Módulo 7» (4081–4083) | débil: «La estimación es la del Capítulo 3» (3917) | 16 | 9,2 |
| M7 · 4.7 Dentro de auto.arima (4087–4300) | ¿Qué hace la caja negra y dónde se equivoca? | «el Nilo guarda una sorpresa» (4297–4298) | ✓ «el explorador del Módulo 6» (4106) | 14 | 9,1 |
| M8 · 4.8 Diagnóstico y errores comunes (4302–4536) | ¿Cuál es la firma de la sobrediferenciación y qué pasó con el Nilo? | «tema del Módulo 9» (4532–4534) | ✓ «el del Capítulo 3 y no cambia» (4320) | 16 | 10,3 |
| M9 · 4.9 Pronóstico (4538–4837) | ¿Qué fija la forma del pronóstico y de dónde sale el ancho del intervalo? | «El Módulo 10 reúne las piezas… y recorre el ciclo» (4832–4835) | ✓ «Aquí es donde la elección de d deja de ser un tecnicismo» (4556) | 16 | 13,5 |
| M10 · 4.10 La TRM, el puente y el cierre (4839–5773) | ¿Funciona el ciclo entero, también donde no hay nada que modelar, y qué falta? | Nota «Y en el Capítulo 5…» (5762–5770) | ✓ «Nueve módulos han desmontado el ciclo» (4857) | 24 | 29,4 / 39,5 (+17,5 de autoevaluación) |
| M11 · Simulacro (5775–5843) | ¿Salen solas las decisiones del cap. 3 y de 4.1–4.4? | Nota «Cómo aprovecharlo» (5831–5840) | «Este módulo no añade contenido: es un ensayo» (5794) | 40 | 2,5 de lectura (40 es el reloj del ensayo) |
| M12 · Preparcial (5845–5944) | ¿Qué módulo de los caps. 3 y 4 falta? | Botón al preparcial (5941) | frío: abre con el Parcial 2 (5863) | 5 | 2,4 |

Declarado: 195 min (150 en M1–M10). Medido de lectura cerrada en M1–M10: 116,1 min; de lectura abierta (con pista
y solución de los ejercicios): 126,2; más 17,5 de leer enunciados, opciones y retros de la autoevaluación. El total
parece razonable; el reparto no (ver §4).

### Lectura del arco

El capítulo se cuenta en cuatro tramos que el lector percibe, y que siguen el orden del ciclo que el M2 dibuja:
**definir y enmarcar** (M1–M2), **decidir cada pieza** (M3 el `d`, M4 `p` y `q`, M5 la constante, M6 comparar, M7 la
automatización), **comprobar y usar** (M8 diagnóstico, M9 pronóstico) y **cerrar** (M10, con la TRM, el puente al 5 y la
evaluación). Cada módulo tiene su «Objetivo» (12 de 12) y los diez primeros cierran con un párrafo que apunta al
siguiente (los diez; ver tabla). Es un arco firme, y el hilo que más rinde es uno solo: **la pregunta del Nilo**.
Se planta en el M1 («Una anomalía que vale la pena guardar», 2963–2981: integrar la serie del Nilo casi no mueve la
varianza), se alimenta en el M3 (dos de tres pruebas dicen «no diferenciar»; KPSS se engaña con un escalón), en el M4
(el −0,402 es también «lo que deja diferenciar una serie que no lo necesitaba», 3573–3575), en el M5 (la deriva no sale),
en el M6 (ningún `d` sale limpio) y se cierra en el M8 («El caso del Nilo, cerrado», 4392–4418, con «la parte incómoda»
del fuera de muestra) y en el M10 («Leído de corrido, el caso deja dos lecciones», 4946–4953). Es el mejor recurso del
capítulo.

Donde el hilo afloja:

- **El M10 hace cuatro cosas** (su objetivo lo dice: reunir el Nilo, recorrer el ciclo con la TRM, aceptar un
  resultado incómodo, ver por qué hace falta el 5): 3 308 palabras de prosa cerrada, más que cualquier módulo de
  M1–M9 (de 704 a 1 400), tres simuladores y un bloque de código de 111 líneas R y 94 Python; el primer simulador llega
  tras 872 palabras y el primer bloque tras 2 162. (M)
- **El Nilo se resume tres veces en el mismo módulo**: la tabla «El Nilo, de principio a fin» (4862–4931: siete filas,
  693 palabras con la fórmula y la nota), «Leído de corrido, el caso deja dos lecciones» (4946–4953) y las doce viñetas
  de «Resumen del capítulo» (5436–5469); y el M9 acaba de cerrar con otro cierre (4832–4835). (M/O)
- **El M8 se anuncia once veces antes de llegar**: 11 líneas de los módulos 1–7 remiten al Módulo 8 (2979, 3118, 3151,
  3277, 3531, 3555, 3802, 3938, 3960, 3996, 4298; `lector_terminos.out`); diez de ellas anuncian el caso del Nilo o la
  sobrediferenciación y una (3118) el diagnóstico. El pago es bueno, pero el lector lleva siete módulos con «el Módulo 8 lo
  destapa» y los números 0,2544 y −0,8741 como constantes (ver M1). (M)
- **No hay práctica hasta el M10.** Los tres ejercicios con pista y solución y la autoevaluación están todos en el M10;
  M1–M9 no piden nada al lector salvo mover deslizadores (0 `ejercicio-guiado` y 0 `quiz` en esos nueve módulos). El
  capítulo 3 actual tiene un ejercicio guiado en nueve de sus diez módulos de contenido (11 en total; ver
  `lector_carga_cap3.out`). (M)
- **El capítulo termina con material de otra naturaleza tras el resumen**: autoevaluación, tres ejercicios, lecturas
  y la nota «Y en el Capítulo 5…». El resumen (5436) no es lo último que se lee, pero la nota final (5762–5770) cierra
  bien. (O)

### Promesas: hechas, cumplidas, incumplidas

| # | Dónde se promete | Qué | ¿Se cumple? |
|---|---|---|---|
| 1 | Cap. 3, 7435–7440 («Lo que viene») | «se añade la pieza que falta —la integración, el orden `d`—», Box–Jenkins, Hyndman–Khandakar y «la advertencia sobre comparar criterios con distinto `d`» | **Sí** (M1; M2; M7; M6). |
| 2 | Cap. 3, 7440 | `AirPassengers` «no aparece en este capítulo»; vuelve en el 5 | **Sí**, y el 4 la usa en el puente (5384–5434), que el 3 no anunciaba pero que el 5 retoma con las mismas cifras (cap. 5, 3076–3082, 4933–4938). (M) |
| 3 | Cap. 3, 6196–6204 y 4216 | «Los ψ darán su forma de abanico… a partir del Capítulo 4»; con raíz unitaria «el abanico se abre sin techo» | **Sí** (M9, 4608–4666; M10, 5119–5142). |
| 4 | M1, 2831–2833 | La expansión del ARIMA como ARMA(p+d, q) «es la que usará el Módulo 9» para los ψ | **Sí** (4623–4624; y la pista del ejercicio 3, 5667). |
| 5 | M1, 2979 | «El Módulo 3 explica por qué el software decidió que sí, y el Módulo 8 cierra el caso» | **Sí** el M3 (KPSS es el valor por defecto de `ndiffs()`, 3290–3291) y el M8, pero «el software» no tiene antecedente en el M1. (M/O) |
| 6 | M2, 3151 / M3, 3277 / M5, 3802 | El Módulo 8 «muestra un caso real… en la propia serie del Nilo», «lo destapa», «lo ajusta como escalón» | **Sí** (4392–4411). |
| 7 | M5, 3743–3744 | El simulador «La forma del pronóstico según d» del M9 «dibuja cuatro de estos seis casos» | **Sí** (título en 4562; cuatro modelos en el selector, 8541–8544). |
| 8 | M6, 3938 | «la comparación válida es fuera de muestra (Módulo 8)» | **Sí**, con una sola partición (4420–4441), y M8 remite al capítulo 6 para hacerla bien (4440–4441). |
| 9 | M6, 3996 | «cuatro de los nueve modelos con d = 2 tienen una raíz MA exactamente sobre el círculo» | **Sí** (4376–4379; los cuatro coinciden con el JSON de precálculos). (M) |
| 10 | M9, 4734–4735 | «en la TRM, a un mes, el intervalo del 80 % cubre el 83,9 %… El Módulo 10 lo mide» | **No.** El M10 mide el 95 % (5150–5156: 4,4 % fuera a un mes; 8,7 % a doce); el 80 % y el 83,9 % no aparecen en ningún otro sitio (`grep`). (M) |
| 11 | M8, 4389 | «(Es el ejercicio 2 de este capítulo.)» | **Sí** el ejercicio existe (5578), pero la caja ya da su respuesta (ver M8). (M) |
| 12 | M9, 4662 | «Sobre `BJsales` (ejercicio 3)» | **Parcial:** la serie se presenta en el ejercicio 1 (5490), y el ejercicio 3 se nombra antes que el 1. (M) |
| 13 | M10, 5155–5156 | «el Capítulo 6 lo confirma fuera de la muestra, con una cobertura del 89,6 %» | **Sí** (cap. 6, 4539 y 4592: naïve, 95 %, TRM a doce meses, 89,6 %). (M) |
| 14 | M10, 5056–5057 | «En el Capítulo 6 la caminata aleatoria reaparece… el método *naïve*… referencia que hay que batir» | **Sí** (cap. 6, «Caso 2 · TRM: nadie vence al naïve»). |
| 15 | M10, 5767 | «La TRM no lo necesita, y el Capítulo 5 enseña también a comprobarlo» | **Sí** (cap. 5, 3110–3111). |
| 16 | M11, 5794–5797 y M12, 5863–5864 | Un quiz de 40 min y un Parcial 2 «el miércoles 14 de octubre» | **Vencido o ambiguo** (ver §5). (M, por la fecha) |

---

## 2. Dónde me pierdo, módulo por módulo

### M1 · De ARMA a ARIMA (2749–2996)

- **P 2837–2857 · «Casos particulares ya conocidos».** La tabla nombra cinco objetos: ARMA, caminata, caminata con
  deriva, IMA(1,1) con «suavizamiento exponencial simple» y IMA(2,2) con «método de Holt». Los tres últimos no
  son «ya conocidos»: «suavizamiento exponencial» y «Holt» no están en los capítulos 1–3 (0 líneas) ni se definen en
  el 4 (Holt aparece solo aquí, 2853, y como opción del simulacro); el pie dice «con restricciones sobre los
  coeficientes» sin decir cuáles. El simulacro pregunta por ambos (opciones en 9492 y 9494). (M)
- **N 2850–2852 y 3625 · «Equivale al suavizamiento exponencial simple… α = 1 + θ».** Es la frase que le da sentido
  al IMA(1,1), y el M4 ajusta un IMA(1,1) con θ̂ = −0,7329 (3624–3626) sin decir que eso es α = 0,267: la cadena
  «0.267» no aparece en el capítulo. El lector recibe la equivalencia como dato. (M)
- **P 2894, 2906, 2971, 2972 · «0,2544» y «−0,8741».** Entran como constantes del código del primer bloque y la nota
  los llama «los coeficientes reales del Nilo» (2966–2967), pero el capítulo no estima ese modelo hasta el M10, que
  los da por primera vez con sus errores estándar (4942); y **ningún bloque de código del capítulo imprime el ajuste
  ARIMA(1,1,1) del Nilo** (M2 lo ajusta y solo muestra la p de Ljung–Box y el pronóstico; M9 lo ajusta y no imprime los
  coeficientes). Son 2 048 líneas entre el primer uso y la primera vez que se justifican. (M)
- **N 2888, 2929 · `data(Nile)` y `nilo`.** El bloque carga la serie, imprime `length`, y nunca más la usa: todo lo
  siguiente son constantes y `arima.sim`. El primer bloque del capítulo no toca los datos que anuncia. (M)
- **P 2910, 2957, 2965–2981 · el primer resultado del capítulo es una anomalía** («`<- ?! integrar NO disparo la
  varianza`»; R da 1,006 y Python 1,363 por el generador, comentado en 2958–2959). Funciona como gancho (✓), pero
  la nota usa «cancelación casi exacta de raíces» y «sobrediferenciación» (la firma se presenta en 4325–4335) antes
  de definirlas, y manda al M3 y al M8. (M)
- **P 2979 · «el software decidió que sí».** En el M1 nadie ha dicho que un software decida `d`; el antecedente
  aparece en 3290–3291. (O)
- **P 2781 · `c` en la fórmula de definición sin una palabra** (solo la fila de la caminata con deriva, 2848, lo
  glosa); la explica el M5, 941 líneas después. (M)
- **✓ 2790–2794 y 2992–2994.** «Un ARIMA no es un ARMA cualquiera: es un ARMA al que se le imponen `d` raíces
  unitarias» y «Con el modelo definido queda la pregunta práctica».

### M2 · La metodología de Box–Jenkins (2998–3212)

- **P 3075–3077, 3095–3096, 3116–3118 · el ciclo nombra funciones que nadie usa.** `checkresiduals()` aparece solo
  aquí (3116: 1 línea en todo el capítulo); `Arima()` frente a `arima()` se presenta como equivalentes (3095) y la
  diferencia llega en el M5 (3750–3761). El panel «Con qué» es una lista de nombres, no un uso. (M)
- **N 3161–3180 · el bloque «esqueleto».** `d <- ndiffs(Nile)` no se imprime (el valor de `d` solo se conoce
  por 3283–3288, un módulo después); `acf(w); pacf(w)` dibujan sin decir qué mirar; en Python, `w <- np.diff(nilo)` se
  calcula y no se usa (3191). La etapa 1 no muestra ninguna cifra. (M)
- **P 3208–3210 · «despacha la etapa 1 en una línea… la decisión más consecuente».** Cierra con una frase que
  llama «decisión» a una línea cuyo resultado no se mostró. (O)
- **D/C · el módulo no tiene simulador ni ejercicio** (el ciclo es su único componente); 804 palabras de prosa, 6,5
  min medidos, el más corto del capítulo después del M5. (M)
- **✓ 3023–3025 y 3062–3064.** «La palabra clave es *iterativo*» y «Las etapas 2, 3 y 4 pueden mandar de vuelta»
  (el componente `ciclo` repite el patrón «Qué haces / Con qué / Qué te devuelve atrás» del capítulo 3, 4454 ss.).

### M3 · Elegir d (3214–3534) · 1 400 palabras, el módulo de prosa más largo de M1–M9

- **P 3239–3257 y 3259–3271 · la tabla da los veredictos antes de decir qué contrasta cada prueba.** La tercera fila
  trae ADF, PP y KPSS con sus estadísticos y p-valores; solo después se lee que ADF y PP parten de la raíz unitaria y KPSS
  invierte la nula. **PP** no está en el capítulo 2 y aquí se usa con la sigla; el nombre completo, Phillips–Perron,
  solo está en 4387 (M8), 1 136 líneas después. (M)
- **P 3236 y 3281 · dos «tres» en el mismo módulo.** «Tres evidencias complementarias» (gráfico, varianza, pruebas) y,
  45 líneas más abajo, «Tres pruebas, tres respuestas». La tercera evidencia contiene las tres pruebas, y el resumen
  (5446) repite «tres evidencias». (M)
- **C/N 3283–3302 · un recuadro con un párrafo de 199 palabras** (3290–3302; el más largo de todo el capítulo) que
  mezcla la especificación del ADF de `ndiffs()` (τμ = −4,05; −2,89), un Monte Carlo (1 000 réplicas: PP 100 %, ADF con
  `k = 4` 51,3 %) y la conclusión «la respuesta no está en la prueba sino en el gráfico». Ninguna de esas cifras sale
  de un bloque de código (`lector_cifras.out`). (M)
- **P 3313–3315 y 3532 · «el modelo de dos medias del Nilo».** Se usa para fijar σ̂ = 127,0 del experimento, y el
  cierre del módulo lo llama «la alternativa que este módulo dejó planteada»; el modelo `y = μ + β·1{t ≥ 1899} + ε` solo se
  escribe en 4404–4406 (M8), 1 090 líneas más abajo, y la hipótesis del escalón sí está en 3307. (M)
- **P 3342–3351 · 1 000 réplicas frente a 400.** El texto da 4,8 % (1 000 réplicas) y el recuadro mismo avisa de que
  «la malla de 400 réplicas del simulador y del bloque de código da 4,5 %»: dos cifras para el mismo experimento. Las demás
  de ese bloque (86,4 %; 5,4 %; 0,5 %; 100 % de `ndiffs`; 70,8 %; 44,5 %) no salen de ningún bloque. (M)
- **C 3320–3328 y 3500–3520 · la introducción del simulador (151 palabras) presenta `ℓ = 4`, `ℓ = 12` y
  `nlags="legacy"` de Python** y remite al recuadro «R y Python no calculan el mismo KPSS», que llega 180 líneas
  después, con tres fórmulas. Una diferencia entre lenguajes ocupa el espacio de una de las decisiones del módulo. (M/O)
- **N 3365–3402 · el plegado** (287 palabras, 4 fórmulas): «puente browniano», `S_t ∼ t^{3/2}`, `1,07` y `1,23`; la
  conclusión («KPSS no distingue raíz unitaria de cambio de nivel») sale de nuevo en el resumen (5447). Nada del
  desarrollo se cita después. (M)
- **✓ 3307–3316, 3404–3407 y 3528–3532.** «Sospecha razonable… Se puede comprobar» (un experimento con hipótesis, simulación
  y desmentido), «el error es traducir su rechazo por "hay que diferenciar"» y el mapa del resto del capítulo.

### M4 · Identificar p y q (3536–3702)

- **P 3566–3575 · la introducción del simulador (205 palabras, 7 cifras) dice lo que el simulador va a mostrar**
  (0,231 en el rezago 8; −0,626 en `d = 2`; −0,402; «La tabla elige p y q; no confirma d»), y la «lectura» del JS
  (8137–8144) muestra después «ACF fuera de banda x de 20» y la varianza. El lector lee la conclusión antes de mover
  el selector. Es la más larga de las once introducciones (`lector_intros.out`). (M)
- **N 3625–3626 · «Es el IMA(1,1) del Módulo 1, el equivalente del suavizamiento exponencial simple».** No se calcula
  el α (ver M1). (M)
- **P 3692 · «el primer residual es y_1 = 1120 (inicialización difusa)»**: jerga de comentario de código sin explicación en
  el texto; reaparece en 4062–4065 y en 5338. (O)
- **✓ 3573–3575, 3629–3634 y 3698–3700.** «También es lo que deja diferenciar una serie que no lo necesitaba» (el mismo
  número se lee dos veces, y el módulo lo dice), «Pero no se propone uno: se proponen varios» y el empalme con la
  constante.

### M5 · La constante: media y deriva (3704–3897)

- **P 3806–3814 · la TRM entra en una nota** («Sobre la tasa de cambio mensual, añadiendo deriva a la caminata aleatoria
  que elige `auto.arima`… 8,00 pesos/mes, e.e. 10,36, t = 0,77») **antes de que el capítulo la presente** (4960) y antes
  de que se sepa que `auto.arima` la deja en una caminata (5008–5009, 5048). El M10 repite casi literal las tres cifras
  (5050–5052). Ninguna sale de un bloque del M5. (M)
- **P 3795–3803 · dos medias de las diferencias.** La fórmula (3785) dice `E[∇y] = δ`, el ajuste da `δ̂ = −2,883`, y el
  texto calcula «la media de las diferencias es −3,84» (3799) para repartirla entre una caída de 1899 (−2,50) y el resto.
  No se dice por qué la media muestral (−3,84) no es `δ̂`; y `φ̂ = 0,271` de la ecuación (3796) no es el `0,2544` del M1 ni
  sale de ningún bloque. (M/O)
- **C 3747–3775 · tabla de «valores por defecto» de cuatro funciones** (`arima`, `Arima`, `auto.arima`, `statsmodels`).
  Es la primera vez en el capítulo que se dice que `arima()` y `Arima()` difieren, tras cuatro módulos de usarlas
  indistintamente. (M)
- **D/C · el módulo no tiene simulador ni figura:** tres fórmulas, una tabla, dos notas y un bloque de 65 líneas;
  6,5 min medidos frente a 12 declarados. (M)
- **✓ 3740–3744.** «Cada diferencia sube en un grado el polinomio de la tendencia» con las seis combinaciones y la
  remisión al simulador del M9.

### M6 · Estimar y comparar (3899–4085)

- **P 3921–3926 · notación.** El AICc se escribe con `n* = n − d` y `n`; el capítulo 3 lo escribía con `T`
  (cap. 3, 5581: `T − k − 1`). El cambio de símbolo en la fórmula que el lector ya conoce no se avisa. (M)
- **D 3942–4044 · los 27 modelos se muestran cuatro veces:** la tabla ordenable (3942), el explorador (3949), la tabla
  «Los mejores de cada d» (3976–3990) y la salida del código (4034–4037), que imprime exactamente las mismas tres filas. (M)
- **P 3951–3961 · la introducción (170 palabras) dice «descarta ocho modelos».** El JSON de precálculos da 8 modelos con
  Ljung–Box(20) < 0,05 en los 27, pero con `d = 1` (donde se empieza) solo rechaza uno, el (0,1,0); la frase sigue a
  «Empieza en `d = 1`». Y «cuatro modelos quedan a menos de 2 puntos del mejor» (3954) es 4 más el mejor sin deriva; el
  M7 dirá «siete» (4193) contando las variantes con deriva, sin recordarlo. (M)
- **P 4062–4065 y 4280–4281 · dos explicaciones de la misma diferencia.** El M6 dice que `f.aicc` de statsmodels «ya
  usa» el `n` efectivo y aun así imprime 1267,47 frente a 1267,51 de R; el M7 explica los 0,04 con «statsmodels no
  descuenta d en nobs (ver el módulo 6)». Un `n` de 100 frente a 99 en el término de corrección mueve el AICc unas
  milésimas, no 0,04. (M)
- **✓ 3929–3940 y 3942–3947.** «El AIC no cruza la frontera de d» y una tabla ordenable que **muestra el error**: el
  mínimo de AICc del capítulo sale con `d = 2` y el `n efectivo` a la vista (JS 8864–8867).

### M7 · Dentro de auto.arima (4087–4300)

- **P 4145–4161 · «escalonada» y «exhaustiva» se usan antes de nombrarse.** La introducción del simulador habla de
  `stepwise = FALSE` y «modo exhaustivo» (4148–4149), el paso 3 del algoritmo describe la búsqueda por vecindario sin
  llamarla escalonada (4120–4123), y el nombre llega en el título 4159. (M)
- **D 4163–4170 · un bloque `$$` con las dos líneas idénticas** («escalonada: ARIMA(1,1,1), AICc = 1267,507; exhaustiva:
  ARIMA(1,1,1), AICc = 1267,507»), que el código imprime otra vez (4243–4245). (M)
- **N 4175–4190 · el podio de siete modelos** sale de la búsqueda exhaustiva, pero el código solo imprime el ganador y
  los dos conteos (18, 42); ni 1268,210 ni 1269,348 aparecen en un bloque. (M)
- **P 4257–4293 · el módulo cuyo objeto es una traza no se puede reproducir en Python:** statsmodels no trae el
  algoritmo, la pestaña ajusta una rejilla de 16 modelos (R evalúa 18) y `pmdarima` «no se ejecuta en este material».
  El comentario lo dice con honestidad. (M)
- **✓ 4106–4110 y 4192–4198.** «Dos razones opuestas» (funciona bien; no es exhaustiva) y «siete candidatos
  indistinguibles… `trace = TRUE` no cuesta nada».

### M8 · Diagnóstico y errores comunes (4302–4536)

- **P título frente a contenido.** El título y la barra lateral prometen «Diagnóstico»; el diagnóstico de residuales es
  un párrafo (4320–4323) que remite al capítulo 3, y el resto es sobrediferenciación, un cierre del caso del Nilo y un
  fuera de muestra. (M/O)
- **P 4382–4389 · `log(lynx)` entra en un recuadro de aviso con cifras** (1,653 → 0,687; raíz MA 1,000; ADF, KPSS y
  Phillips–Perron) y «(Es el ejercicio 2 de este capítulo.)»: el recuadro **da la respuesta del ejercicio 2** (5599–5649:
  «no hay que diferenciarla», «la regla de la varianza falla», `ARIMA(2,1,1)` con raíz 1,000). El ejercicio resulta una
  confirmación. Las cifras de `lynx` solo salen de un bloque en el ejercicio (5613–5627). (M)
- **N 4322, 4371–4374, 4400–4411 · cifras sin bloque:** Shapiro p = 0,731; σ̂² = 28 268,34 y 80 055,05 del MA(1) en
  `d = 2` y 3; las medias 1 097,75 y 849,97 («que coincide con la construcción de la presa baja de Asuán»); el AICc del
  escalón, 1 257,91. El bloque de código del módulo (4450–4497) imprime θ̂, el escalón y su p de Ljung–Box, no estas. (M)
- **P 4404–4411 · el modelo `y = μ + β·1{t ≥ 1899} + ε` se escribe aquí por primera vez** como «un modelo con d = 0 y un solo
  regresor»; el lector lo ha usado como «modelo de dos medias» desde 3313. (M)
- **P 4421–4441 · la tabla de fuera de muestra** trae RMSE y MAE (el código calcula solo el RMSE, 4488); «Naïve» se usa
  sin decir que es la caminata (se dirá en 5056–5057); y «el abanico completo va de 123 a 133» (4437) usa «abanico»
  para un intervalo de valores, mientras en M9–M10 es la banda del pronóstico. (M)
- **D 4354–4369 · la tabla repite lo que muestra el simulador** (`d`, varianza, ρ̂₁, θ̂ del MA(1), «raíz unitaria en el
  MA»; JS 8429–8439) y el código imprime tres de las mismas filas (4459–4461): tres veces los mismos números. (M)
- **✓ 4325–4335, 4392–4418 y 4420–4441.** «La sobrediferenciación tiene una firma exacta… no es una metáfora, es
  álgebra», «El caso del Nilo, cerrado» (recoge las dos piezas del M1 y del M3 en una explicación) y «Y ahora la parte
  incómoda»: el escalón gana por 25 puntos de AICc y no pronostica mejor.

### M9 · Pronóstico: forma e intervalos (4538–4837)

- **P 4591–4606 · una nota de 132 palabras antes de la teoría** que usa «la fórmula de abajo» (4614), «no
  invertibilidad», ψ → 0,72 «en vez de 0,169», 2 428 frente a 2 771 y «el abanico». La brecha entre 2 428 y 2 771 se
  deja a «el desarrollo del final del módulo» (4605), pero el plegado está a mitad (paso 2, 4689–4692) y tras él vienen
  una caja de aviso, el código y el cierre. (M)
- **P 4579, 3829 y 8974 · dos cifras para «la media» del ARIMA(1,0,1):** 920,70 (M5, salida de `arima(…, method = "ML")`,
  3829, y la retro de la autoevaluación, 8974) y 920,56 (tabla del M9, «Vuelve a la media»). Una tercera, 919,35, es la media
  muestral que el comentario de Python del M5 llama exacta (3866); el simulador da 918,99 a `h = 30` y «distancia a la media»
  0,36. La de la tabla del M9 no sale de ningún bloque. (M)
- **N 4576–4587 · la columna «Ancho 95 %: h=1 → h=30»** (561 → 677; 557 → 781; 555 → 708) sale del JSON y se ve en la
  «lectura» del simulador; el código solo imprime las diferencias primera y segunda y el caso `d = 2`. (M)
- **N 4623–4629 · la forma cerrada de ψ_j** ni se deduce ni se comprueba: el código usa `ARMAtoMA` (4772). (M)
- **P 4662–4665 · `BJsales` aparece en una nota con ψ∞ = 2,99 y «1,96 veces la caminata»,** que es la solución del
  ejercicio 3 (5674–5732); la serie no se ha presentado. (M)
- **N 4732–4735 · el 83,9 %.** Ver promesa 10: nunca se mide. (M)
- **✓ 4556–4559 y 4621–4622.** «Los coeficientes ARMA gobiernan los primeros pasos; a largo plazo lo único que queda
  en pie es `d` y la constante» y «a un paso, el intervalo lo determina solo la desviación de los residuales».

### M10 · La TRM, el puente y el cierre (4839–5773) · 3 308 palabras, 24 declarados

- **C · cuatro objetivos en un módulo** (4851–4852) y siete `<h3>`: el Nilo de principio a fin (693 palabras), la TRM
  (1 342), el puente (349), el resumen (327), la autoevaluación (36), los ejercicios (160 palabras de enunciado y 138 líneas de
  solución R) y las lecturas (310). (M)
- **D/C 4864–4931, 4946–4953, 5436–5469 · tres resúmenes del Nilo** en el módulo (ver §1). La tabla de siete filas va
  **al principio**, antes de la serie nueva; un lector que llega de leer el M9 recibe un recuento de lo ya leído antes de
  nada nuevo. (M/O)
- **P 4942 · el modelo del ciclo, con sus coeficientes y errores estándar, aparece aquí por primera vez** (ver M1). (M)
- **P 5008–5009 · «192 modelos (con la parte estacional permitida; sin ella son 42)».** La «parte estacional» no se ha
  presentado y el 192 no sale de ningún bloque; el código llama `auto.arima(trm, stepwise = FALSE, approximation = FALSE)`
  con la parte estacional por defecto y solo imprime el orden (5224–5226). (M)
- **P 5056–5057 · «la caminata aleatoria reaparece con otro nombre —el método *naïve*—»**, cuando el *naïve* ya
  se ha usado dos veces como etiqueta en el M8 (4427, 4920). (M)
- **D 5060–5078 · se vuelve a deducir `σ_h² = hσ²` para la caminata,** deducido ya en la introducción del simulador del
  M9 (4638–4640) y en el paso 5 del plegado (4713–4716). (M)
- **P 5134–5135 · «con d = 1, un θ = −1 da ψ∞ = 0, el caso límite del Módulo 9»;** el M9 muestra `d = 2` con
  ψ → 0,72 (4600–4602, 4718–4719), no ese caso. (M)
- **C 5144–5160 (184 palabras en 5150–5160) · cobertura:** normalidad, curtosis, asimetría, 6 de 137, 5 por arriba, 11 de
  126, 8,7 %, 89,6 % del capítulo 6 y la razón 1,07–1,14 de la varianza real, en un párrafo. (M)
- **N 5381–5434 · el puente no tiene bloque de código.** Ninguna de sus cifras (ρ̂₁₂ = 0,7245, ρ̂₂₄ = 0,6727, banda
  0,1633, Q = 222,4, ARIMA(0,1,5), ARIMA(8,1,3) con ρ̂₁₂ = 0,437, airline con ρ̂₁₂ = −0,0515 y p = 0,233, 143 y 131
  observaciones…) sale de un bloque; casi todas están en el JSON de precálculos, y **Q = 222,4 ni siquiera ahí**. «Con
  p + q ≤ 5… el mejor es un ARIMA(0,1,5)» y «con una búsqueda más amplia gana un ARIMA(8,1,3)» son afirmaciones sin
  código, en el experimento que justifica el capítulo siguiente. El quiz y el capítulo 5 las dan por sentadas
  (cap. 5, 3076–3082, 4933–4938). (M)
- **P 5489–5651, 5654–5732 · los tres ejercicios.** Dos de sus resultados están dados antes (ver M8 y M9); el 3 pide
  «el ARIMA(1,1,1) de `BJsales` del ejercicio 1» y quien no hizo el 1 no tiene dónde empezar. Cada solución es un bloque R
  largo y no hay pestaña Python. (M/O)
- **N 8887–9078 · la autoevaluación no toca el M1 ni el M2, ni la TRM.** Etiquetas `modulo`: 6, 9, 10, 5, 3, 4, 7, 8 (una
  por módulo del 3 al 10); la de «10» es el puente, no la TRM. (M)
- **P 9030 · retro del ítem 6: «La conclusión sobre d es correcta pero el argumento no».** El ítem pregunta por una ACF de
  la serie sin diferenciar y una de las opciones dice «que d = 1»; el capítulo entero (3307–3316, 4414–4418, 4947–4953)
  sostiene que, para el Nilo, `d = 1` es provisional y posiblemente sobra. La retro afirma lo que el capítulo pone en
  duda. (M/O)
- **✓ 4955–4956, 5047–5058, 5119–5142 y 5762–5770.** «El ciclo encontró estructura y dejó abierta la duda sobre `d`. La
  serie siguiente invierte la situación», «El resultado, aceptado tal cual», la comparación TRM / Nilo / cualquier ARMA del
  capítulo 3 («el abanico tiene techo») y «Y en el Capítulo 5…».

### M11 · Simulacro del quiz (5775–5843)

- **P 5794–5797 · el quiz se describe en presente** («se presenta en Brightspace, dura 40 minutos») sin fecha; no se
  puede saber desde la página si ya se aplicó (O).
- **✓ 5794, 5801–5806 y 5809–5840.** «Este módulo no añade contenido: es un ensayo», «lo que se repite de una variante a
  otra es la *decisión*» y «Aquí no se corrige», con su razón. Las cuentas (cinco de opción, tres con una respuesta…)
  coinciden con las diez preguntas del JS. (M)

### M12 · Preparcial del Corte II (5845–5944)

- **P 5863–5864 · «Con este módulo se cierra lo que entra al Parcial 2: el miércoles 14 de octubre, en Brightspace, unos
  70 minutos».** La fecha del sistema es el 22 de noviembre de 2026; el capítulo 3 ya dice del Parcial 2 que «ya se
  aplicó» (cap. 3, 7413) y la portada conserva «Antes del Parcial 2» (index, 928). El módulo habla de un examen
  futuro que ya pasó. (M)

---

## 3. Problemas transversales

### Lo que se usa antes de definirse

| Término | Primer uso (línea, módulo) | Presentación | Distancia |
|---|---|---|---|
| «modelo de dos medias» / el escalón como modelo | 3314 (M3) | 4404 (M8) | 1 090 (la hipótesis sí está en 3307) |
| PP (la sigla) / Phillips–Perron | 3251 (M3) | 4387 (M8), solo el nombre | 1 136 |
| «cancelación de raíces», «sobrediferenciación» | 2977–2978 (M1) | 4327 (M8) | 1 349 |
| `auto.arima` | 3291 (M3) | 4094 (M7) | 803 (el cap. 3 ya lo nombra) |
| 0,2544 y −0,8741 como «coeficientes reales del Nilo» | 2894, 2966 (M1) | 4942 (M10) | 2 048 |
| la TRM y «la caminata que elige `auto.arima`» | 3806 (M5) | 4960 y 5048 (M10) | 1 154 |
| *naïve* | 4427 (M8) | 5057 (M10), como la caminata | 630 |
| `lynx` | 4386 (M8) | 5578 (ejercicio 2) | 1 192 |
| `BJsales` | 4662 (M9) | 5490 (ejercicio 1) | 828 |
| `c` de la ecuación | 2781 (M1) | 3722 (M5) | 941 |
| «escalonada» / «exhaustiva» | 4148–4149 (M7) | 4159 (M7) | 10 |
| RMSE / MAE; «cobertura» | 4425 (M8); 4733 (M9) | no se definen en el cap. 4 (el 6 los trata) | — |
| `checkresiduals()` | 3116 (M2) | nunca | — |
| Holt; «suavizamiento exponencial» | 2850–2853 (M1) | Holt nunca; la recursión simple en 2851 | — |
| «parte estacional» de `auto.arima` | 5009 (M10) | nunca (el puente la nombra en 5413) | — |

Cada uno por separado se soporta. Juntos hacen que el lector atraviese el M3 sin saber qué es PP, lea el M5 con una serie
(la TRM) y un resultado (caminata) que no ha visto, y use el escalón como modelo cuatro módulos antes de leerlo escrito. (M)

### Vocabulario y notación que cambian

- **`T` frente a `n`.** El capítulo 3 escribe el AICc con `T` (5581) y la banda con `1,96/√T` (4417, 5084); el 4 escribe `n` y
  `n* = n − d` (3920–3926) y reserva `T` para el origen del pronóstico (`y_{T+h}`, M9). Es el cambio de símbolo en una
  fórmula que el lector ya conoce y no se avisa. (M)
- **«abanico».** Cap. 3: la banda del pronóstico. En el 4: la banda (M9 4602; M10, 13 usos) y, una vez, el intervalo de
  valores de una tabla (M8 4437). (M)
- **«tres evidencias» frente a «tres pruebas»** en el M3 (3236 y 3281; resumen 5446). (M)
- **«cuatro modelos a menos de 2 puntos» (M6 3954) frente a «siete» (M7 4193, M10 4902, ítem 7 de la autoevaluación).** La
  diferencia es la deriva; no se dice. (M)
- **«identificación»** es la etapa 1 del ciclo (M2, M4, M10); «los coeficientes no están identificados» (M10 5042) es el otro
  sentido que ya tenía el capítulo 3; aquí aparece una sola vez. (M)
- **«pronóstico a largo plazo» y `h = 30`.** Sin problema; se anota solo que el M9 numera con `h` y la «lectura» del
  simulador rotula `ψₕ₋₁` mientras el eje dice `j`. (M)
- **«período» (3 usos en prosa: 3123, 3735, 5387) frente a «periodo»** del capítulo 5 (3081). Anotado, no más. (M)
- **«Módulo N» en prosa (71 líneas) frente a «4.N» como cita** (M11 y M12: 22); la portada llama «Módulo III» al capítulo 4 y
  el capítulo habla de «Módulo 3». (M)
- **Inglés sin traducir.** En la prosa: *drift*, glosado (2736), y *airline*, que el capítulo 5 explica; «Naïve» con
  diéresis es el nombre del método. Los títulos de módulo llevan el subtítulo en inglés (convención). **No hay anglicismos
  en la prosa** (`lector_terminos.out`). Las advertencias de R se citan en inglés entre comillas (3760, 4596), lo cual es
  honesto. (M)
- **Coherencia que sí hay:** «residuales» en las 28 apariciones (0 de «residuos»), «caminata aleatoria» en las 23 (0 de
  «paseo aleatorio»), `n` para el tamaño de muestra en todo el capítulo, «Capítulo N» siempre con el mismo número, y el
  convenio de signo de θ avisado donde importa (2983–2990). (M)

### Dicho pero no mostrado

`lector_cifras.py` toma 50 cifras citadas en la prosa y busca cada cadena en los `<pre>` del mismo módulo, de los demás y en
el JSON de precálculos. **36 de 50 no están impresas en ningún bloque de código del capítulo** (20 de ellas están en el JSON
de precálculos, que no siempre se pinta en un simulador). Por módulo:

- **M3:** el Monte Carlo de ADF/PP (51,3 %; 86,4 %; 5,4 %; 0,5 %; 100 %), el estadístico de PP (−6,690), `τμ = −4,05`, el valor
  crítico −2,89, el 4,8 % de 1 000 réplicas, 70,8 %, 44,5 %, 1,07 y 1,23. Solo el KPSS con 400 réplicas sale del código.
- **M1, M5, M8, M9, M10:** los coeficientes (0,2544; −0,8741 y sus e.e.), `φ̂ = 0,271`, Shapiro 0,731, σ̂² de los MA(1),
  1 097,75, 849,97, 1 257,91, el MAE de la tabla, 920,56, φ̂ = −0,39, 778,0, la media del puente y el 83,9 %.
- **M10, el puente:** las cinco cifras o grupos de cifras revisados, sin bloque.

La TRM, en cambio, es el caso mejor mostrado: ADF, KPSS, ACF, rejilla, raíces, Ljung–Box, Shapiro, deriva, intervalos,
conteos fuera de banda y curtosis salen de un solo bloque (5171–5281). Es el modelo a seguir. (M)

### Introducciones de simulador que dicen el resultado

Once introducciones suman 993 palabras. Las de M4 (205), M6 (170) y M3 (151) traen siete, cinco y tres cifras y las
conclusiones («Ningún `d` sale limpio, y el Módulo 8 explica por qué», 3960–3961; «La tabla elige p y q; no confirma d»,
3575). Los rótulos del selector del M9 (8541–8544) contestan la pregunta que su introducción plantea («vuelve a la media»,
«se queda plano», «recta», «recta, e intervalo enorme»); el del M4 rotula «una de más» (8152). En cambio las del M8, M9
(forma) y el puente (38, 40, 29 palabras) piden hacer algo y no adelantan. (M)

### Plegados que cargan con lo importante

Tres módulos tienen «Ver el desarrollo paso a paso» (M1, M3, M9; 137, 287 y 364 palabras). En dos, algo que el texto cita
después vive solo dentro:

| Plegado | Qué vive solo dentro | Quién lo cita |
|---|---|---|
| M1, 2796–2835 | la expansión del ARIMA(1,1,1) como ARMA(2,1) y `φ₁* + φ₂* = 1` | 2898 (código), 4623–4624 (M9), pista del ejercicio 3 (5667–5668) |
| M9, 4668–4726 | por qué `forecast()` da 2 771 y la fórmula 2 428 (paso 2, 4689–4692: la no invertibilidad) | la nota 4604–4605, que manda «al final del módulo» |
| M3, 3356–3409 | por qué KPSS se dispara con un escalón (sumas parciales) | nada; la conclusión se repite en el resumen (5447) |

Los tres plegados son del tipo «desarrollo paso a paso» y los dos primeros están bien enlazados; el del M9 tiene un nombre
en la nota («el desarrollo del final del módulo») que no corresponde a su posición. (M)

### Convenios y advertencias entre lenguajes

Hay avisos entre R y Python en casi cada módulo: el signo de θ (M1 2983–2990), `np.roots` (2939), el generador (2945–2946,
2957–2959), `ndiffs` ausente (3189), el KPSS (3480–3486, 3500–3520), `pacf(..., method="ldb")` (3684–3686), el primer residual
(3692), el intercept (3866–3870), `nobs` frente a `nobs_effective` (4062–4065), `pmdarima` (4283–4293), θ = −0,9988
(4518–4519), σ² por grados de libertad (4823–4826), el (2,1,2) de la TRM y OPG (5330–5351). Cada uno es un «fallo silencioso»
bien elegido y está dicho en el comentario del código; la carga está en la suma: son entre 10 y 20 notas de «R da X, Python
Y» que el estudiante que trabaja en un solo lenguaje no necesita, repartidas sin jerarquía entre cinco módulos. (M/O)

### Voz

La prosa expositiva de M1–M10 es impersonal en lo esencial. La segunda persona del singular se concentra en cuatro sitios:
(a) las introducciones de simulador (imperativos «Cambia», «Empieza», «Recuerda», «Mueve», «Sube», «mira», «fíjate»: 10 de las 11), (b)
el componente del ciclo («Qué te devuelve atrás» ×4, «mandarte» 3143), (c) los ejercicios y la autoevaluación (8 formas
en los ejercicios, «puedes reintentar» en 5477), y (d) M11 y M12 (16 formas: «hazlo», «relee», «tus fórmulas»). No hay
primera persona del plural en la prosa. Recuento aproximado por expresión regular sobre formas inequívocas
(`lector_terminos.out`). Es un asunto de otro lente; se anota por coherencia con la regla de voz impersonal. (M)

---

## 4. Carga

Convenio y números: `diagnostico/cap4/diag/lector_carga.py` (la fórmula del cap. 1, 2 y 3: palabras de prosa / 180 + 3 por
simulador + 2 por bloque de código, con un par R/Python como un bloque; se quitan `<pre>`, scripts, canvas, botones, el pie
de fuentes y la matemática en bloque; cada fórmula en línea es una palabra). «Cerrado» deja sin contar pista y solución;
«abierto» las cuenta; los plegados van aparte; los quizzes (JS) van aparte.

| Mód. | Palabras (cerrado) | `$$` | `$` | Cuadros | Tablas | Sim. | Bloques (líneas) | Plegado (palabras) | Cerrado (min) | Abierto (min) | Declarado | Razón abierto/declarado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 874 | 2 | 53 | 5 | 1 | 1 | 1 (70) | 137 | 9,9 | 9,9 | 12 | 0,82 |
| M2 | 804 | 0 | 19 | 1 | 0 | 0 | 1 (42) | — | 6,5 | 6,5 | 10 | 0,65 |
| M3 | 1 400 | 4 | 91 | 5 | 1 | 1 | 1 (78) | 287 | 12,8 | 12,8 | 16 | 0,80 |
| M4 | 704 | 2 | 55 | 3 | 1 | 1 | 1 (50) | — | 8,9 | 8,9 | 14 | 0,64 |
| M5 | 810 | 5 | 55 | 5 | 1 | 0 | 1 (65) | — | 6,5 | 6,5 | 12 | 0,54 |
| M6 | 757 | 3 | 53 | 4 | 1 | 1 | 1 (62) | — | 9,2 | 9,2 | 16 | 0,58 |
| M7 | 744 | 2 | 46 | 6 | 1 | 1 | 1 (70) | — | 9,1 | 9,1 | 14 | 0,65 |
| M8 | 955 | 3 | 87 | 6 | 2 | 1 | 1 (77) | — | 10,3 | 10,3 | 16 | 0,64 |
| M9 | 997 | 3 | 90 | 6 | 1 | 2 | 1 (79) | 364 | 13,5 | 13,5 | 16 | 0,85 |
| M10 | 3 308 (4 045 abierto) | 11 | 330 | 11 | 3 | 3 | 4 (343) | — | 29,4 | 39,5 | 24 | **1,64** |
| M11 | 457 | 0 | 1 | 2 | 0 | 0 | 0 | — | 2,5 | 2,5 | 40 | (el ensayo) |
| M12 | 432 | 0 | 6 | 1 | 1 | 0 | 0 | — | 2,4 | 2,4 | 5 | 0,48 |
| **Total** | 12 242 (12 979) | 35 (+11 plegadas) | 886 | 55 | 13 | 11 | 13 | 788 | 121,0 | 131,1 | 195 | |

Los plegados suman 4,4 min si se abren. La autoevaluación (8 preguntas) pesa 17,5 min de lectura de enunciados, opciones,
pistas y retros; el simulacro (10 preguntas), 6,8. Ninguna columna incluye el tiempo de hacer los ejercicios, de contestar
los quizzes ni de ejecutar el código. (M)

**Comparación con el capítulo 3 actual (misma medición, `lector_carga_cap3.out`).** El 3 declara en M1–M10 196 min y mide
131,9 cerrado y 171,7 abierto (razón abierto/declarado 0,88; por módulo, de 0,72 a 1,03; en M4, M6, M7, M8 y M9 entre 0,94 y
1,03, es decir calibrado). El 4 declara 150 y mide 116,1 cerrado y 126,2 abierto (0,84 en conjunto), pero ese promedio
esconde el reparto: **M1–M9 declaran 126 y miden 86,7 (0,69; de 0,54 a 0,85) y M10 declara 24 y mide 29,4 cerrado o 39,5
abierto (1,22 y 1,64)**, más 17,5 de autoevaluación. Con la convención del capítulo 2 y 3 los declarados saldrían: M1 10, M2 7,
M3 13, M4 9, M5 7, M6 9, M7 9, M8 10, M9 14, M10 29 (40 si se leen las soluciones), M12 2, y el simulacro, 40 (el reloj del
ensayo). (M)

**El capítulo es menos denso en fórmulas y en cifras que el 3.** 35 fórmulas en bloque (más 11 plegadas) frente a 45 (más 29),
y 4,2 cifras por 100 palabras de prosa frente a 7,3 del 3 (`lector_numeros.out`, `lector_numeros_cap3.out`); por módulo,
de 0,2 (M2) a 6,8 (M8) y 6,0 (M10). La carga del 4 no está en la matemática de cada módulo sino en tres sitios: el M10, el M3
(recuadro de 199 palabras y experimento de 1 058 palabras) y la acumulación de avisos R/Python. (M/O)

### Qué se desbalancea

- **M10 pesa 1,22 veces lo declarado con la lectura cerrada y 1,64 con las soluciones abiertas, y arrastra 17,5 min de
  autoevaluación:** 46,9 min si se cuenta el cuestionario y no las soluciones, y 57,0 si se cuentan las dos cosas. Es el módulo con
  más cosas distintas (§2). (M)
- **M2 y M5 miden 6,5 min** (declarados 10 y 12): son los dos módulos sin simulador (el M2 tiene el componente del ciclo); el M5
  es una tabla de valores por defecto, un recuadro de definiciones y un bloque de código. (M)
- **M4, M6, M7 y M8 miden entre 0,58 y 0,65 de lo declarado.** Son módulos con un simulador y un bloque de código que
  la fórmula valora en 5 min; la lectura de una salida de R o de un ejercicio en el simulador cuesta más, y no se mide. (O)
- **M3 es el único módulo de M1–M9 con prosa mayor de 1 000 palabras** (1 400), con el primer bloque de código tras 1 403
  palabras y el primer simulador tras 760. (M)

### Dónde partiría o movería (sin renumerar; de mayor a menor rendimiento)

1. **Declarar lo medido** (convención del capítulo 2 y 3, `lector_carga.out`): M1 10, M2 7, M3 13, M4 9, M5 7, M6 9, M7 9, M8
   10, M9 14, M10 29 + 18 de la autoevaluación (o un tiempo para el módulo y otro para el cuestionario). No cuesta nada.
2. **Mostrar lo que se dice:** imprimir el ajuste del ARIMA(1,1,1) del Nilo con sus e.e. en el M2 o el M6 y fundar con él los
   `0,2544` del M1; poner el código del puente (un bloque de 15 líneas basta: `auto.arima` no estacional con `p + q ≤ 5` y el
   airline, con las ρ̂₁₂ y el Ljung–Box(24)); o declarar «precalculado» donde la cifra sale de un JSON. Hacer lo mismo con el
   Monte Carlo ADF/PP del M3.
3. **M10: partir en dos módulos,** «Caso: la TRM» (4958–5281, con el abanico) y «Cierre: puente al Capítulo 5, resumen,
   autoevaluación y ejercicios»; y mover la tabla «El Nilo, de principio a fin» (4862–4931) al **final** del M9 o a
   «Resumen del capítulo» (que ya recoge sus ideas), de modo que el M10 empiece por la serie nueva.
4. **Una práctica por módulo** como en el capítulo 3 actual, al menos en M3 (leer un recuadro de pruebas y decidir `d`),
   M5 (constante según `d`), M6 (descartar un ajuste por sus raíces) y M8 (reconocer una sobrediferenciación): hoy el capítulo
   termina con tres ejercicios que resumen todo el curso de `d` y no ejercitan M1–M2.
5. **Quitar la respuesta de los ejercicios de los módulos previos:** sustituir la caja del `lynx` del M8 (4382–4389) por una
   frase sin cifras o por «ver el ejercicio 2», y la nota de `BJsales` del M9 (4662–4665) por una referencia a la solución del
   ejercicio 3; y mover la nota de la TRM del M5 (3806–3814) al M10.
6. **Reescribir las introducciones de M3, M4 y M6** en 40–60 palabras, como las de M8 y M9, y pasar las cifras a la «lectura»
   o a un recuadro posterior a la actividad.
7. **Presentar lo que se usa:** PP con su nombre completo en la fila de 3251 y una línea en 3259; «el modelo de dos medias»
   (la ecuación de 4404–4406) en el M3; `RMSE`/`MAE`/`naïve` con una frase en 4421–4423; α = 1 − 0,7329 = 0,267 en el M4; y la
   fila de Holt de 2853 con su definición o sin la fila.
8. **Bajar los avisos R/Python a un recuadro por módulo** con el patrón «qué difiere / por qué / qué hacer», en lugar de
   comentarios dispersos.
9. **Autoevaluación:** una pregunta del M1 (la expansión ARMA(p + d, q)) y una de la TRM; corregir la retro de 9030
   (el módulo dice que `d = 1` es provisional).
10. **Cifras y notación:** `T` o `n` (y avisar del cambio respecto del 3); un solo «abanico»; «tres evidencias» frente a
    «tres pruebas»; el 83,9 % (o quitarlo del M9); 920,56 / 920,70.

---

## 5. Empalme con el capítulo 3, con el 5 y con la portada

### Lo que el cap. 4 supone del 3, y si el 3 lo da

| El cap. 4 supone… | ¿Lo da el cap. 3? |
|---|---|
| `φ(B)` y `θ(B)` «exactamente los del capítulo anterior» (2784–2785) | **Sí** (M1). |
| `RB(0, σ²)` (2782) | **Sí** (cap. 3, 3133–3135). |
| ARMA como el caso `d = 0` (2845) | **Sí** (M5). |
| La tabla ACF/PACF «del Capítulo 3» (3548, 5002) | **Sí** (M5). |
| «La estimación es la del Capítulo 3» (3917) | **Sí** (M7). |
| El AICc y el BIC, con `T` | **Sí**, pero el 4 los reescribe con `n*` sin avisar (M6). |
| «El diagnóstico… es el del Capítulo 3» (4320), Ljung–Box con `fitdf` | **Sí** (M8). |
| Los pesos ψ de la representación MA(∞) «que se construyó en el Capítulo 3» (4610) | **Sí** (M4). |
| Invertibilidad «en el sentido preciso del Capítulo 3» (5041) | **Sí** (M3). |
| «El Capítulo 3 mostró que sus log-retornos son, a efectos prácticos, ruido blanco» (4961) | **Sí** (M9, TRM). |
| El abanico de un ARMA estacionario «tiene techo» (5130–5133) | **Sí** (M9, «El abanico se abre, y se para»). |
| ADF, KPSS, `ndiffs()` y el truncamiento de la varianza de largo plazo (3515) | **Sí** (cap. 2, 4120–4130, 4425). |
| Phillips–Perron (3251, 3259) | **No**; el cap. 2 solo nombra a Phillips como autor del KPSS. |
| Suavizamiento exponencial, Holt (2850–2854) | **No** (0 líneas en los caps. 1–3). |
| «fuera de muestra», RMSE y MAE (3938, 4425) | **No**; los trata el 6. |

El empalme narrativo funciona: «Lo que viene» del 3 se cumple punto por punto (promesas 1–3), el cap. 3 dice «el Capítulo 4
va a contrastar» y el 4 contrasta. Lo abierto: PP, suavizamiento exponencial/Holt, el símbolo `T`/`n` y el módulo 11 del 3, que
va entre el cierre y la apertura del 4 (la apertura «El Capítulo 3 terminó con un límite explícito» es del M10, no del
final, pero se lee como cierto). (M)

### Lo que el 5 y el 6 toman del 4

El 5 abre con «El Capítulo 4 terminó con un fracaso deliberado» y repite las cifras del puente (3076–3082) y del 4933–4938;
cita la regla de la varianza (4067), la firma de la sobrediferenciación (4086), `log(lynx)` (4111), el ciclo de
Box–Jenkins (4321), los pesos ψ y «el Módulo 9» (4586), `ψ∞ = 0,169` (4593), «Frontera con el Capítulo 4» (4616) y el AICc
entre `D` (4646, 5166, 5570). El 6 cita «el Capítulo 4 que en niveles se comporta como una caminata» (4529–4530) y la cobertura
del 89,6 %. **Todas las remisiones que se leyeron se cumplen.** Una consecuencia de la §2: las cifras del puente que el 5 da por
sentadas (ρ̂₁₂ = 0,7245, Q = 222,4, 143 y 131) no tienen código en el 4. (M)

### La tarjeta de la portada (`Htmls_Series/index.html`, 719–745)

Texto: «De ARMA a ARIMA, el ciclo de Box–Jenkins recorrible, cómo elegir el orden de integración, la constante y la deriva, el
algoritmo de Hyndman–Khandakar por dentro, sobrediferenciación y la construcción del intervalo de pronóstico desde los pesos
ψ.» Etiquetas: «Semanas 8–9», «Capítulo 4 · Módulo III» y «12 módulos · 11 simuladores».

- **Cifras:** 12 módulos y 11 simuladores son correctas (11 `data-simulador` de simulador; el simulacro y el preparcial
  son los otros dos módulos). (M)
- **Lo que el capítulo más desarrolla y la tarjeta no nombra:** el hilo del Nilo (el escalón frente a la raíz unitaria), la
  TRM como caso en el que el modelo dice «no hay señal» y el puente al SARIMA. La tarjeta lista el temario, no el argumento. (O)
- **«Módulo III»:** en la portada es el módulo del curso; dentro del capítulo, «Módulo 3» es 4.3. Dos niveles con el
  mismo nombre. (O)
- **Preparcial · Corte II (index, 925–945: «Antes del Parcial 2», «8 módulos · 38 ítems»):** la tarjeta y el M12 del capítulo
  4 conservan el tiempo futuro del Parcial 2 (14 de octubre); el capítulo 3 ya habla en pasado. Los 38 ítems se
  corresponden con el M12 (32 de diagnóstico + 6 del simulacro). (M)

---

## 6. Lo que funciona (no romper al revisar)

1. **El hilo del Nilo, de la anomalía del M1 (2963–2981) al cierre del M8 (4392–4441).** Una pregunta planteada con
   honestidad, alimentada en cada módulo con una pieza (varianza, pruebas, ACF, deriva, rejilla, traza) y cerrada con
   dos explicaciones que encajan y con una parte incómoda («no pronostica mejor»). Cada módulo la recoge con una frase corta.
2. **M3 3305–3316, 3341–3354 y 3404–3407 · el experimento del escalón:** una hipótesis, un simulador que la prueba y la frase
   «el error es traducir su rechazo por "hay que diferenciar"».
3. **M6 3929–3947 · «El AIC no cruza la frontera de d» con la tabla ordenable que muestra el error.** Es de lo poco del
   capítulo que se aprende viéndolo, no leyéndolo.
4. **M7 4192–4198 · «siete candidatos indistinguibles según el propio criterio»**, con `trace = TRUE` como remedio, y
   la lista de «tres cosas que `auto.arima` no hace» (4201–4214).
5. **M8 4325–4335 · «No es una metáfora, es álgebra»** y 4420–4441 «Y ahora la parte incómoda».
6. **M9 4556–4559 y 4621–4622 · «los coeficientes ARMA gobiernan los primeros pasos… lo único que queda en pie es `d` y la
   constante»** y «a un paso, el intervalo lo determina solo la desviación de los residuales».
7. **M10 5047–5058 y 5119–5142 · el resultado aceptado tal cual y la comparación de las tres series** (TRM, Nilo, cualquier
   ARMA del 3) con una sola fórmula: es la síntesis más clara del capítulo.
8. **M10 5171–5281 · un solo bloque para la TRM entera, con todas las cifras que cita la prosa.** Es el modelo de «lo que se
   dice se muestra».
9. **M10 5762–5770 · «Y en el Capítulo 5…»:** cierra sobre lo que viene sin añadir material.
10. **Los empalmes con los vecinos:** «Lo que viene» del 3 se cumple (§1), y el 5 y el 6 citan el 4 con exactitud.
11. **Cada módulo abre diciendo qué dejó el anterior y cierra diciendo qué sigue** (M1–M9: 3016, 3232, 3554, 3722, 3917, 4106,
    4320, 4556, 4857 y los diez cierres).

---

## 7. Los diez problemas que más dañan la comprensión (orden de daño)

1. **El M10 hace cuatro cosas** (3 308 palabras, declarado 24, medido 29,4 / 39,5 + 17,5 de autoevaluación): resume el Nilo
   tres veces, tiene la TRM entera, el puente, el resumen, la autoevaluación, los ejercicios y las lecturas; y es el
   único módulo con práctica de todo el capítulo. (M)
2. **No hay práctica antes del M10:** M1–M9 no piden nada; los tres ejercicios y la autoevaluación (que no toca el M1 ni el
   M2) están al final, y dos ejercicios llegan con la respuesta dada por los módulos 8 y 9. (M)
3. **El modelo central del capítulo no se estima a la vista:** los `0,2544` y `−0,8741` entran en el M1 como constantes y
   se justifican 2 048 líneas después, en el M10, sin que ningún bloque imprima el ajuste. (M)
4. **36 de 50 cifras de la prosa no salen de ningún bloque** (M3: el Monte Carlo de ADF/PP; M8: Shapiro, medias, AICc del
   escalón; M10: todo el puente al capítulo 5). El experimento que justifica el capítulo siguiente no tiene código. (M)
5. **Se usan antes de presentarse** PP (1 136 líneas), el «modelo de dos medias» (1 090), la TRM y `auto.arima` en el M5
   (1 154), *naïve*, `lynx` y `BJsales`; y la tabla de «casos conocidos» del M1 incluye suavizamiento exponencial y Holt
   que el curso no ha presentado. (M)
6. **Las introducciones de M3, M4 y M6 dan el resultado antes de la actividad** (205, 170, 151 palabras con 7, 5 y 3 cifras) y
   los rótulos del selector del M9 dicen la respuesta. (M)
7. **Los minutos declarados no están medidos:** M1–M9 declaran 126 y miden 86,7 (0,69); M10 declara 24 y mide 29,4 / 39,5 (más
   17,5). El capítulo 3 actual sí está calibrado (0,94–1,03 en cinco módulos). (M)
8. **El M12 (y el M11) hablan de un parcial que ya pasó,** con fecha, en presente: 14 de octubre frente a la fecha de hoy,
   22 de noviembre; el capítulo 3 ya lo dice en pasado. (M)
9. **La promesa del M9 «El Módulo 10 lo mide» (80 % cubre el 83,9 %) no se cumple;** el M10 mide otra cosa (95 %). Y las
   cuentas «cuatro» (M6) y «siete» (M7) modelos a menos de 2 puntos se contradicen a primera vista. (M)
10. **Costuras de notación y carga:** `T`/`n` entre el 3 y el 4, AICc con `n*`, «abanico» con un tercer sentido, «tres
    evidencias» frente a «tres pruebas», 920,56 frente a 920,70, y 10–20 notas «R da X, Python Y» repartidas sin jerarquía. (M)

---

## 8. Lo que no se pudo comprobar

- **No se renderizó la página ni se ejecutó ningún simulador:** el texto de cada «lectura» y de cada selector se leyó en el JS
  (7936–8847). No se sabe cómo se ve cada gráfica ni si el valor inicial de un deslizador coincide con lo que dice su introducción
  (se leyeron los `params` iniciales y coinciden con «Empieza en…» en M1, M4, M6, M8; en el M3 el deslizador arranca en
  `|β| = 100` y la introducción dice «Empieza en `|β| = 0»`, 3323).
- **No se ejecutó R ni Python:** «cifra sin bloque» es una búsqueda de la cadena. Una cifra que el código calcula pero no
  imprime sale como «sin bloque» (por eso los casos se revisaron a ojo); el JSON de precálculos guarda más de lo que los
  simuladores pintan.
- **La fórmula de minutos (180 palabras/min, +3 por simulador, +2 por bloque) es la del curso,** no una medición con
  lectores: es un suelo para los módulos con derivaciones y un techo para los de prosa corta; no incluye hacer los
  ejercicios, contestar los cuestionarios ni ejecutar el código.
- **La fecha de aplicación del quiz del M11** (¿ya ocurrió?) y el tiempo de 40 min no se pudieron confirmar desde el
  repositorio; solo la del Parcial 2 (14 de octubre) frente a la fecha del sistema.
- **Corrección técnica, fuentes y diseño de gráficas** quedan fuera de este lente; las únicas observaciones de ese tipo son
  inconsistencias entre dos frases del propio texto (4062–4065 y 4280–4281; 920,56 y 920,70; 3342–3351), anotadas en la §2.
- **Las diapositivas del capítulo 4** (`diapositivas/capitulo-4-modelos-arima.html`) no se leyeron.
