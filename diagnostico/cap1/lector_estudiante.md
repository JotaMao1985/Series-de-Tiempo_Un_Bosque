# Capítulo 1 leído como estudiante · hilo narrativo y comprensión

Archivo leído: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (los nueve `<template>`
enteros, en orden), más la apertura del capítulo 2 (`capitulo-2-estacionariedad-acf-pacf.html`,
líneas 2180–2300 y 2425–2455) y la tarjeta de `index.html` (642–663). Las líneas citadas son del
HTML del capítulo 1 salvo indicación. Lente: comprensión y hilo; no se juzga corrección técnica ni
fuentes. No se editó nada.

Las cifras de carga salen de `scratchpad/diag/cuenta_cap1_v2.py` (quita `<pre>`, `<script>`,
`<canvas>`, botones, pies de fuentes, matemática en bloque; cada fórmula en línea cuenta como una
palabra; las derivaciones plegadas se cuentan aparte).

---

## 1. Mapa del arco

| Mód. | Pregunta que abre | Con qué cierra | Transición de entrada | Declarado | Estimado |
|---|---|---|---|---|---|
| M1 | ¿Qué es una serie de tiempo y qué la distingue de datos transversales? | `AirPassengers` como mezcla (tendencia + patrón anual que crece); promete «separar esa mezcla» (2353) | — (primero) | 8 | 5,0 |
| M2 | ¿Cómo le digo al software qué es mi serie? (índice, frecuencia, clave) | «La frecuencia no es un detalle administrativo» (2499) | **débil**: «Nada de eso…» (2396) no tiene antecedente | 8 | 6,6 |
| M3 | ¿Cómo se mira una serie antes de modelarla? | «Cómo leer el abanico»: promete M4 (medirlo) y M6 (decidirlo) (2609–2614) | ✓ «Con la serie ya declarada, el paso siguiente no es modelar: es mirarla» (2527) | 10 | 7,8 |
| M4 | ¿Qué hay dentro de la serie y cómo se combina (suma o producto)? | «Nombrar no es separar… empezando por la tendencia» (2818–2820) | ✓ «Los patrones que revelan esos gráficos tienen nombre» (2640) | 12 | 19,4 |
| M5 | ¿Cómo se aísla la tendencia? | «Ya es el primer paso de un método completo… tiene nombre propio» (2940–2942) | ✓ «En el gráfico de AirPassengers… la tendencia queda tapada» (2845) | 10 | 9,9 |
| M6 | ¿Cómo se separan las tres piezas con el método clásico y cuándo falla? | Aviso de las tres limitaciones → «STL (Módulo 7) corrige estas tres» (3342–3347) | ✓ «Ese encadenamiento se llama descomposición clásica» (2967) | 12 | 17,0 (18,5 con derivación) |
| M7 | ¿Cómo corrige STL esas tres debilidades? | Nota «STL no se agota aquí… pronóstico» (3688–3692): apunta al curso, no al M8 | ✓ «responde a esas tres debilidades una por una» (3382) | 10 | 17,6 (20,1) |
| M8 | ¿Qué se hace con los componentes: quitar uno, medir cuánto pesa cada uno? | «Una serie entera en dos números» (3795–3798) | **débil**: «Con componentes en los que se puede confiar…» (3728); el M7 no lo anunciaba | 10 | 4,4 (5,4) |
| M9 | ¿Qué queda dicho y qué viene? | Lecturas (4068–4083); el puente al capítulo 2 está al principio (3842–3846) | ✓ «El capítulo empezó con una mezcla y termina con las piezas separadas» (3834) | 8 | 12,6 + autoevaluación ≈ 7 = ≈ 20 |

Declarado: 88 min. Estimado: 100,5 min (105,4 con las derivaciones abiertas), más ≈ 7 min de
autoevaluación. Es decir, ≈ 110 min frente a 88.

### Lectura del arco

El arco es bueno, con costuras flojas en los dos extremos: la cadena M3 → M4 → M5 → M6 → M7 está
atada con promesas explícitas y cumplidas (el abanico de M3 se mide en M4 y se paga en pasajeros en
M6; los «mismos pasajeros de más en julio» de M4 reaparecen en M6; «ese encadenamiento tiene nombre
propio» de M5 abre M6; «estas tres debilidades» de M6 abren M7). Juntas dan al estudiante la
sensación de un solo argumento.

Donde el hilo afloja:

- **M1 → M2.** M1 cierra con una nota de «Conexión con ciencia de datos» y M2 abre con «Nada de eso
  lo deduce el software por su cuenta» (2396). «Eso» no remite a nada de M1. M2 además no responde a
  una pregunta que el lector ya se haga: es el primer código del capítulo y llega antes de que el
  lector haya visto por qué le importaría la frecuencia.
- **M7 → M8.** El cierre de M7 mira hacia el curso («más adelante… estrategia de pronóstico»), no hacia
  el módulo que sigue. M8 abre con una frase de trámite (3728).
- **La promesa de M1 sin cobrar en el resumen.** M1 promete «saber cuándo la separación es de fiar,
  su parte difícil» (2353–2354). Se cumple en M6 («el residuo no se mira para confirmar que todo fue
  bien, se mira para descubrir en qué paso hay que volver a entrar», 3339–3340), pero el resumen de
  M9 (3851–3858) no la recoge: ni el bucle ni el criterio de «residuo sin forma» aparecen entre sus
  seis viñetas.
- **M9: el puente al capítulo 2 está lejos del final.** El mejor párrafo de cierre (3842–3846) queda
  antes del resumen, de la autoevaluación, de los tres ejercicios y de las lecturas. Lo último que
  lee el estudiante es una lista de referencias.

---

## 2. Dónde me pierdo, módulo por módulo

Etiquetas: **P** = pérdida de comprensión; **N** = dicho pero no mostrado; **D** = decoración o
repetición; **C** = carga.

### M1 · ¿Qué es una serie de tiempo? (2316–2373)

- **N 2345–2349 · la dependencia temporal solo se afirma.** «Las observaciones cercanas tienden a
  parecerse… es justamente lo que no capturan los métodos construidos sobre observaciones
  independientes» es el objetivo declarado del módulo (2328) y la primera viñeta del resumen (3851),
  y en todo el capítulo no hay un gráfico, una cifra ni un ejemplo que la haga ver (ver M3).
- **P 2353–2354 · «saber cuándo la separación es de fiar, su parte difícil».** Frase críptica en un
  primer módulo: el lector no sabe qué es «de fiar» ni cuál es la «separación». Se explica 4 módulos
  después.
- **P 2358–2360 · el simulador de apertura ya dice tendencia, patrón de 12 meses y amplitud que crece
  con el nivel.** Funciona como gancho, pero adelanta tres conceptos sin que el lector tenga dónde
  mirar cada uno (el gráfico es una sola línea). Correcto como adelanto; no pide nada al estudiante.
- **D 2366–2371 · la nota «Conexión con ciencia de datos»** se repite casi igual al abrir el M9
  (3834–3840). Como pareja de principio y fin funciona; sola en M1, es una promesa sin evidencia.

### M2 · Series de tiempo en software (2378–2504)

- **P 2396 · «Nada de eso lo deduce el software».** Sin antecedente (ver arco).
- **P 2397–2399 · «período estacional» y «frecuencia (12 para datos mensuales con estacionalidad
  anual)»** se usan antes de que exista la palabra «estacionalidad» (M3–M4). El lector lo toma en
  confianza.
- **P 2481, 2485 · «si le pasas… declaras»**: el módulo salta a la segunda persona dentro de la
  prosa expositiva (la convención es impersonal fuera de simuladores y ejercicios).
- **P 2488–2493 · `ventas` y `tienda` salen de la nada.** Es la única serie del módulo distinta de
  `AirPassengers`, no se define ni se vuelve a usar en el capítulo; el bloque no se puede ejecutar.
- **N 2499–2501 · «declararla mal… produce descomposiciones y pronósticos sin sentido».** Es la tesis
  del módulo y no se enseña: dos líneas con un `frequency` equivocado (o el error que da
  `decompose()` con frecuencia 1) bastarían para verla.
- **N 2441 · la salida de Python no se muestra** (`print(pasajeros.head())`) mientras la de R sí
  (2422–2427).

### M3 · Visualización de series (2509–2617)

- **N 2527–2538 y 2521–2522 · se anuncian cuatro gráficos y se lee uno.** Del gráfico de tiempo se
  dice «es el del Módulo 1»; del estacional hay mapa, simulador y código; de **subseries** (2535) y
  de **rezagos** (2536–2537) solo hay una viñeta y una línea de código (2588–2589), sin figura. El
  objetivo del módulo («usar… el de subseries y el de rezagos para leer los patrones») no se
  consigue con lo que se ve.
- **N 2536–2537 + 2589 · el gráfico de rezagos es el único sitio donde la dependencia temporal de M1
  podía verse** (y el capítulo 2 lo da por visto, ver §4). Nunca se dibuja.
- **N 2535 · el gráfico de subseries es la imagen que hace inteligible dos pasajes posteriores:** los
  once cocientes de julio de M6 (3233) y la «subserie de ciclo» de M7 (3528–3534). Ninguno de los dos
  lo recuerda.
- **P 2540–2551 · la nota sobre varias estacionalidades va antes de que el lector haya visto un
  gráfico estacional.** Pide elegir «qué ciclo» con `gg_season(consumo, period = "day")` sobre una
  serie, `consumo`, que no existe en el capítulo ni tiene figura. Mejor después del gráfico estacional
  de `AirPassengers`.
- **P 2553–2560 · el mapa mes × año aparece sin una frase de prosa que lo presente** y no está entre
  los «cuatro gráficos» anunciados; su nota (generada, 5967–5970) sí dice qué mirar. Luego el
  simulador siguiente (2562–2571) cuenta lo mismo con otro formato: dos figuras para una sola
  pregunta, sin decir en qué se diferencian.
- **P ciclo (2532, 2541–2547)**: «una línea por **ciclo**», «qué **ciclo** se quiere ver». Aquí «ciclo»
  es el periodo de repetición; en el módulo siguiente será otra cosa (ver §3, polisemia).
- **P 2610–2614 · «abanico» y «multiplicativo» aparecen por primera vez en la nota final,** ya
  cerrados los gráficos. Funciona (y es la mejor transición del capítulo), pero el simulador
  inmediatamente anterior (2564–2566) no usa la palabra.

### M4 · Los cuatro componentes (2622–2821)

- **C 1 338 palabras, 4 simuladores, 0 subtítulos `<h3>`.** El único módulo largo sin una sola
  articulación visible. Tiene cuatro tramos distintos (componentes · suma o producto · medir cuál ·
  el logaritmo) y el lector no los ve.
- **P 2646–2654 vs 2532 y 3074 · «ciclo ≠ estacionalidad»** se declara aquí con recuadro de «Error
  común»… y desde M3 y hasta M9 la palabra se usa también en el sentido de periodo estacional y de
  bucle (ver §3).
- **P 2654 · $T_t$ pasa a significar «tendencia-ciclo»** en la misma frase en que antes era
  «tendencia»: el lector llevará el símbolo con dos significados durante cinco módulos (la aclaración
  llega en 2657–2662).
- **P 2664, 2667, 3054 · «ruido» y «residuo»** se usan como sinónimos y $R_t$ pasa a $\hat R_t$ en M6
  sin decir que el primero es lo no observable y el segundo, lo estimado.
- **P 2686–2688 · $a = A/T_0$** aparece en la intro del comparador con $T_0$ sin definir ($A$ se ve
  en el control, 4841); se entiende por contexto, pero obliga a releer.
- **D 2736–2738 + 4949–4953 + 2760–2763 · las cifras 44 → 232 y 35 % → 49 % se dicen tres veces**
  en un tramo de 25 líneas: la tabla, la lectura del simulador (generada) y el párrafo. Es el patrón
  de «cifra repetida a tres líneas» que el criterio manda recortar.
- **P 2770–2771 · «aplicarle STL, que solo sabe sumar»**: primera mención de STL para un lector que no
  sabe qué es. Se repite en M5 (2879, 2889). Aceptable como pagaré; hay que saber que hay tres.
- **P 2806–2816 · «construye tu serie» llega al final,** tras cuatro simuladores sobre suma-o-producto,
  y es solo aditivo, sin ciclo y sin forma multiplicativa. Responde a «¿cómo se ven los componentes
  sumados?», que es la pregunta del principio del módulo (2640–2649). Sus símbolos ($\beta$, $A$,
  $\sigma$, $\varepsilon_t$, 2808) no están mapeados a $T_t$, $S_t$, $R_t$.
- **N 2657–2662 · «un ciclo de siete u ocho años cabría una vez y media, indistinguible de una
  tendencia»**: el componente $C_t$ nunca se ve en el capítulo (ni en simulador ni en figura). Se
  declara y se descarta en un párrafo; razonable, pero el lector solo tiene la palabra.
- **N 2722–2766 · ✓ bien resuelto** (ver §6).

### M5 · Medias móviles (2827–2944)

- **P 2879 · «una de las tres limitaciones que acaben empujando hacia STL»**: nombra un trío que nadie
  ha enumerado. Se enumera al final de M6 (3343–3346: huecos, estacionalidad fija, atípicos).
- **P 2881–2891 · párrafo para releer dos veces.** «Vale la pena separar qué parte de ese precio la
  impone promediar vecinos y qué parte, tres decisiones…» está mal armado (la frase no cierra) y
  anticipa en un solo bloque a STL, a una regresión local sin nombrarla («otro suavizador») y a un
  simulador de dos módulos más adelante. Es un salto de nivel dentro de M5. Además, los «tres» de aquí
  (cercanía, nivel, ventana completa) no son los «tres» de 2879 ni los de M6/M7 (huecos, fija,
  atípicos): dos tríos distintos en 12 líneas.
- **P 2850 vs 3074 · $k$ cambia de significado:** semiancho de la ventana en M5 ($m = 2k+1$), posición
  dentro del ciclo en M6 ($k = 1,\dots,m$).
- **P 2924–2927 y 2931 · el código no hace lo que la fórmula explica.** La fórmula (2859–2860) da
  media ración a los dos extremos; `slide_dbl(.before = 6, .after = 6)` y `rolling(window=12, center=True)`
  promedian con pesos iguales (13 y 12 puntos). Lo verá un lector que compare la ventana de la fórmula
  con la del código. (Cuestión técnica; se anota por lo que desorienta.)
- **N 2872–2873 · «con $m=5$ o $m=7$… la curva seguiría ondulando al ritmo del año».** Se afirma y el
  simulador (2899–2908) lo permite ver, pero su intro no pide hacerlo: dice «al llegar a $m=12$
  desaparece», no «compara 11, 12 y 13» ni «prueba 6 o 24». La idea central del módulo (la ventana del
  tamaño del periodo) queda a la iniciativa del lector.
- **✓ 2869–2874** bien: «cada mes exactamente una vez: un julio alto y un noviembre bajo».

### M6 · Descomposición clásica (2949–3359) · el módulo con más prosa del capítulo (2 162 palabras)

- **P orden de presentación 2973–3198.** Primero los cuatro pasos en abstracto (el componente de
  pestañas, 2973–3065), luego la tabla de símbolos (3081–3128), luego la normalización (3139–3183) y
  **solo después** la primera salida real (3188). El lector pasa ~190 líneas sin ver el resultado de
  un método que ya le han explicado dos veces.
- **P 3008, 2974 · el componente se llama «ciclo» y su pie dice «Descomponer no es una fórmula sino un
  ciclo»,** mientras la prosa de al lado lo llama «bucle» (2969, 3062). Tercer sentido de «ciclo».
- **P 3016 vs 2612–2614 · «La decisión es visual, no hay prueba automática».** M3 prometió que M6
  «convierte esa medida en la primera decisión», y el paso 1 no menciona la medida de M4
  (amplitud contra nivel) ni su simulador. El lector cree que se le quita lo que acaba de aprender.
- **P 3067–3079 · muro de notación antes de la tabla:** $m$, $k$, $J_k$, $n_k$, $\bar s$, $\tilde s_j$
  en diez líneas; $\tilde s$ se usa en 3079 antes de que 3b (3104) lo defina. La explicación de por qué
  $n_k = 11$ y no 12 (3076–3078) es buena; el bloque en conjunto es lo más denso del capítulo antes
  del M7.
- **P 3093 · la tabla empieza en el paso 2:** el paso 1 (escala) no está en ella y no se dice por qué.
- **N 3232–3234, 3318–3320, 3331–3333 · tres filas de números en cajas de fórmula** hacen el trabajo
  de tres figuras: los once cocientes de julio (1,167 … 1,272), el exceso de julio por año
  (21,3 … 145,8) y la desviación del residuo aditivo por año (30,5 … 25,4, «una U inconfundible»).
  Ninguna se dibuja. La U no se ve.
- **N 3299–3340 · la descomposición aditiva nunca se dibuja.** «Qué habría pasado con la otra escala»
  se argumenta entero con cifras; el módulo tiene un simulador solo para la multiplicativa. Un
  conmutador aditiva/multiplicativa en el mismo simulador (3188) y el panel de residuo habrían
  mostrado la U.
- **N 3343–3346 · «es sensible a valores atípicos»**: aquí es solo una frase con cita; la primera vez
  que se mide es en la solución plegada del ejercicio 3 del M9 (4046).
- **P 3345–3347 · el cierre del módulo es un recuadro de aviso seguido del pie de fuentes**; lo que
  se lleva el lector es un recuadro, no la idea del bucle (que está tres párrafos más arriba).
- **✓** 3208–3254 y 3299–3340, ver §6.

### M7 · Descomposición STL (3364–3704) · el más denso: ≈ 1 730 palabras + 445 en derivaciones, ~12 términos nuevos

- **C términos nuevos:** Loess, span, `t.window`, `s.window`, `t.degree`, `s.degree`, tricúbica,
  bicuadrada, subserie de ciclo, bucle interior, bucle exterior, `robust`, `"periodic"`. El lector
  los recibe en ~330 líneas.
- **P 3395–3401 · cinco nombres de argumento de R en un solo párrafo,** y el lector aún no sabe que
  lo estacional se ajusta sobre subseries (se dice en 3528–3534). `s.degree = 0` se justifica sin que
  haya contexto.
- **P 3440 · «la serie gris es la desestacionalizada en logaritmos, que es exactamente lo que STL
  suaviza para sacar la tendencia»** (intro del simulador del Loess). La mecánica de STL (quitar la
  estacionalidad estimada, suavizar la tendencia, repetir) solo se insinúa después, en 3551–3552
  («el interior alterna estacionalidad y tendencia hasta que se estabilizan»). **El capítulo nunca
  enuncia STL como secuencia de pasos,** que sí hizo con el método clásico (el componente de cuatro
  pasos en M6). Un lector sale de M7 sabiendo qué es Loess y qué es el bucle robusto, no qué hace STL
  en orden.
- **P 3455–3462 · tres lecturas del simulador con cifras que solo se reproducen en puntos concretos**
  (0,0498; 6,2043 frente a 6,2048; 5,5482). Claro para quien tiene el simulador abierto; opaco para
  quien lee de corrido. Piden decir en qué posición de los controles se obtiene cada una.
- **P 3505–3512 (derivación plegada) · `10n+1 = 1441` y el techo del impar.** Es un salto de nivel,
  pero va plegado y es opcional. Correcto.
- **N 3531–3533 · la flexibilidad se dice con una cifra** («de +20,4 % en 1949 a +27,9 % en 1960 con
  `s.window = 11`») y no se ve. Es una de las tres ventajas anunciadas y no tiene figura.
- **N 3572–3591 · la robustez se muestra como la tabla de pesos que «vería el bucle exterior si se le
  dejara correr»,** no como el efecto en los componentes. El efecto (+4,02 % contra −0,82 %) está en
  la solución plegada del ejercicio 3 del M9 (4046–4049). Dos de las tres ventajas con las que se
  abre el módulo (3382, 3523) no tienen imagen en el módulo.
- **P 3597–3606 + 3673–3686 · la figura estrella de STL está calculada con `"periodic"` y sin
  `robust`,** y el aviso que lo dice (3674: «Dos de las tres ventajas están apagadas en la figura de
  arriba») llega **después** del gráfico, de la lectura en log, de la comparación con el clásico y del
  bloque de código. El lector se entera al final de que la imagen que acaba de leer no ilustra lo que el
  módulo prometió.
- **P 3656 vs 3668 · las dos pestañas de código no hacen lo mismo:** R sin `robust` y con `"periodic"`
  (como la figura); Python con `robust=True` y sin período fijo. Quien cambie de pestaña obtiene otro
  índice de julio sin que se avise.
- **P 3608–3639 · «Cómo se leen los componentes en escala logarítmica»** es útil y trae el mejor
  detalle del módulo (exp(0,2164) = 1,2416, un 24,2 % y no 21,6 %), pero compite con la figura del
  STL por la atención y no responde a una pregunta del módulo de STL: responde a «¿cómo uso lo que STL
  da?», que es la pregunta del M8.
- **P 3688–3693 · el cierre mira hacia el pronóstico y no hacia el M8.**

### M8 · Ajuste estacional y fuerza (3709–3810) · el más corto: ≈ 260 palabras + 173 en derivación

- **P 3735–3742 · el simulador usa los índices del método clásico** (`y / S` con la `S` de
  `decompose()`, 5349) y la fuerza se calcula con STL en logaritmos (3744–3747); el módulo no dice cuál
  es cuál. Venimos de un módulo entero sobre STL y la lectura natural es la contraria.
- **N 3791–3793 · «$F_T = 0{,}994$ y $F_S = 0{,}937$: muy fuertes».** Sin un punto de comparación el
  número no significa nada. El contraste útil (`co2` 0,9997 / 0,9841, `USAccDeaths` 0,7991 / 0,9426) y
  las dos advertencias («no compares $F_T$ con $F_S$ dentro de una serie», «no es porcentaje de
  varianza») están en la solución plegada del ejercicio 2 (3975–3999).
- **N 3731–3733 · «Es lo que reportan muchas estadísticas oficiales»**: se afirma y no se ilustra con
  una serie oficial ni con el diente de sierra que el ajuste quita (el simulador sí lo muestra,
  3735–3742, con una frase de intro correcta).
- **N sin código:** ningún bloque en R ni Python (`components()`, `season_adjust`, `seasadj`).
  Es el único módulo con una operación nueva y sin la instrucción para hacerla.
- **D 3795–3798 · la nota «una serie entera en dos números… miles de series»** es una promesa sin
  demostración (no hay una segunda serie en el módulo).
- **P 3762–3764 (derivación) · «compara… si además le quitas la tendencia»:** otra vez tú en prosa
  expositiva; convención del curso.

### M9 · Cierre, resumen y lecturas (3815–4083)

- **P 3856 · «STL (flexible y robusta)» en el resumen** vuelve a la formulación que M7 (3674–3686) y el
  ejercicio 3 (4060) rectifican expresamente («STL no es intrínsecamente resistente, lo es la
  opción»). El estudiante que solo lea el resumen se lleva la versión que el capítulo corrige.
- **P 3851–3858 · el resumen no recoge** el bucle (M6), la lección «ningún modelo describe la serie
  exactamente» (M4) ni el paso por logaritmo y `exp` (M4, M7); recoge todo lo que es nombre.
- **P 3864 · «Seis preguntas»** pero el arreglo `AUTOEVALUACIONES['cap1']` (5993–6177) trae **ocho**.
  Además solo hay preguntas de M4 a M8: nada de M1–M3 y ninguna sobre el bucle del residuo.
- **P 3902–3917 · el ejercicio 1 resuelve con una regresión log–log de la elasticidad** ($b$, IC del
  95 %, $R^2$), técnica nueva que M4 no enseñó (M4 usó la horizontal y el rayo). Falta una línea que
  traduzca: «la horizontal es $b = 0$ y el rayo es $b = 1$».
- **P 3995 · «su estructura es sobre todo el ciclo anual»**: otro «ciclo» por estacionalidad, justo en
  el cierre.
- **P 4031–4038 · tres índices de julio de STL (1,2416; 1,2562; y, en M7, 1,2405 con ventana 21)** más
  el clásico (1,2266): el ejercicio 3 lo explica bien, pero el lector arrastra cuatro números parecidos.
- **P 4071–4075 · lecturas «caps. 1–3»** y el M8 apoya la fuerza en una sección que está fuera de ese
  rango. (Fuente; solo se anota por el efecto en un lector que siga la lectura.)
- **N 4024–4063 · la demostración de la robustez de STL vive aquí,** en una solución plegada que solo
  ve quien primero hace el ejercicio y luego pulsa el botón.
- **✓ 3842–3846** el puente al capítulo 2 es limpio.

---

## 3. Problemas transversales

**Polisemia de «ciclo».** Tres significados en 12 módulos, dos de ellos contradiciendo la advertencia
de M4:
1. periodo de repetición estacional: M3 (2532, 2541–2547), M6 (3074, «un ciclo completo» 3179),
   M7 («más ancha que un ciclo completo» 3511, «subserie de ciclo» 3529), M9 (3995 «ciclo anual»);
2. el componente $C_t$ de duración variable: M4 (2646–2662), resumen (3852), pregunta 1 del quiz;
3. el bucle de la descomposición: M6 (el componente `.ciclo`, 2973; «un ciclo», 3008).
M4 dedica un recuadro entero a que «ciclo ≠ estacionalidad»; el resto del capítulo llama «ciclo» al
periodo estacional.

**Dos tríos distintos.** «Las tres debilidades» (huecos, estacionalidad fija, atípicos: 3343–3346,
3382, 3523) y «las tres decisiones» (peso por cercanía, nivel en vez de recta, ventana completa y
centrada: 2881–2891, 3461). El lector tiene que llevar ambos y la correspondencia no es uno a uno.

**La dependencia temporal y los gráficos de subseries y rezagos nunca se enseñan.** Es el hueco más
grande entre lo prometido y lo mostrado (ver M1, M3 y §4).

**Recursos que sí responden una pregunta del módulo (no decoran):** los cuatro simuladores de M4
(escala, amplitud-nivel, serie-vs-log, construye-tu-serie), el de media móvil, los dos de M7, el
de desestacionalizada. La única pareja redundante es mapa + gráfico estacional en M3.

**Voz.** Segunda persona en prosa: M2 (2481, 2485), derivación de M8 (3762–3781). El capítulo 2
cambia a primera persona del plural («descompusimos», «damos», 2199–2205); la convención del curso es
impersonal. No es del lente de comprensión, pero el cambio de voz en la costura se nota.

---

## 4. Carga

Método y números en el cuadro; la fórmula pedida es palabras/180 + 3 por simulador + 2 por bloque de
código (el par R/Python cuenta como uno).

| Mód. | Palabras de prosa | Derivación plegada | Simuladores | Bloques de código | Lectura pura (min) | Con la fórmula (min) | Con derivaciones (min) | Declarado (min) | Razón (fórmula / declarado) |
|---|---|---|---|---|---|---|---|---|---|
| M1 | 363 | — | 1 | 0 | 2,0 | 5,0 | 5,0 | 8 | 0,6 |
| M2 | 474 | — | 0 | 2 | 2,6 | 6,6 | 6,6 | 8 | 0,8 |
| M3 | 512 | — | 1 (+ mapa) | 1 | 2,8 | 7,8 | 7,8 | 10 | 0,8 |
| M4 | 1 338 | — | 4 | 0 | 7,4 | 19,4 | 19,4 | 12 | **1,6** |
| M5 | 882 | — | 1 | 1 | 4,9 | 9,9 | 9,9 | 10 | 1,0 |
| M6 | 2 162 | 266 | 1 (+ componente de pasos) | 1 | 12,0 | 17,0 | 18,5 | 12 | **1,4–1,5** |
| M7 | 1 733 | 445 | 2 | 1 | 9,6 | 17,6 | 20,1 | 10 | **1,8–2,0** |
| M8 | 259 | 173 | 1 | 0 | 1,4 | 4,4 | 5,4 | 10 | **0,4–0,5** |
| M9 | 1 182 | — | 0 | 3 | 6,6 | 12,6 | 12,6 (+≈7 autoevaluación) | 8 | **1,6 (2,5 con quiz)** |
| **Total** | 8 905 | 884 | 11 | 9 | | **100,5** | **105,4** | **88** | 1,14 (≈ 1,2 con quiz) |

Notas sobre la medición: M6 incluye las cuatro pestañas del componente de pasos (≈ 310 palabras) y la
tabla de símbolos (≈ 120); el 9 de la columna de código corresponde a un bloque con pestañas R/Python por módulo (M3, M5,
M6, M7), el de M2 (pestañas + el error del `tsibble`) y las tres soluciones de M9. Las cifras de
la autoevaluación (8 preguntas, ≈ 380 palabras de enunciados y opciones, ≈ 630 de retroalimentación)
dan ≈ 7 min. Los tres ejercicios del M9 no se cuentan como lectura: son trabajo (30–60 min).

### Qué se desbalancea

- **El M7 no es el más largo en palabras (lo es el M6),** pero sí el más sobrecargado respecto de su
  duración declarada (el doble) y el más denso en términos nuevos. Si lo que preocupa es que «creció
  mucho», es verdad: son ≈ 18–20 min en lugar de 10, con ~12 términos nuevos y dos figuras.
- **M4 es el segundo sobrecargado** pero por simuladores (12 de sus 19 min son los cuatro simuladores
  por la regla de 3 min); su problema es la falta de articulación (cero `<h3>`), no el volumen.
- **M1, M2, M3 y M8 están por debajo de lo declarado (0,4–0,8×).** Son los módulos donde caben las
  figuras que faltan (rezagos, subseries, un segundo juego de fuerzas) sin romper la duración.

### Dónde partiría o movería (sin renumerar; de mayor a menor rendimiento)

1. **De M5 a M7: el párrafo de las «tres decisiones» (2881–2891).** Allí no puede entenderse
   (STL y Loess aún no existen); en el arranque de M7 sí, y M7 ya lo cita (3461–3462). M5 se queda con
   una frase gancho. Quita ≈ 200 palabras y el trío confuso de M5 (≈ −1 min); en M7 la mayor parte ya
   está dicha (3461–3462), así que el aumento es pequeño.
2. **De M7 a M8: «Cómo se leen los componentes en escala logarítmica» (3608–3639),** ≈ 245 palabras.
   Es la lección de «usar lo que STL da» y en M8 sirve para construir la serie ajustada de STL
   ($y / \exp(S)$), que hoy el módulo hace solo con el método clásico. M7 baja ≈ 1,4 min y M8 sube de
   4,4 a ≈ 6.
3. **De M9 a M8: el contraste `co2` / `USAccDeaths` / `AirPassengers` y las dos advertencias de
   $F_T$ / $F_S$ (3975–3999, ≈ 165 palabras),** como una tabla de tres filas, más un bloque de código
   para `components()` / `seasadj`. Convierte 0,994 en un número con referencia. M8 llega a ≈ 8–9 min
   (cerca de su duración declarada); el ejercicio 2 conserva el código y la tabla.
4. **En M6: reordenar sin recortar.** Después del componente de pasos, mostrar primero el
   simulador y el julio de 1955 (3185–3254) y solo después la tabla de símbolos y la normalización
   (3067–3183); la «otra escala» (3299–3340) queda con su imagen. Mismas palabras, mejor orden.
5. **En M4: añadir `<h3>`** (componentes · suma o producto · ¿cuál?: medirlo · el logaritmo) y mover
   «construye tu serie» (2806–2816) a justo después de la lista de componentes. Es una partición
   visual, no de contenido.
6. **Si se admite renumerar** (cuesta: `courseData`, los campos `modulo:` del quiz, las referencias
   «Módulo N» del capítulo y de otros archivos, las cifras de la portada, las diapositivas): partir M4
   en «Los cuatro componentes» y «¿Aditivo o multiplicativo? Medirlo y transformar». Esa segunda parte
   es literalmente el paso 1 de M6 («elegir la escala»), y quedaría con el mismo título que el paso que
   alimenta. M7 no necesita partirse si se hacen las moves 1–2.

Tras 1–3 el reparto queda: M4 19, M5 ≈ 9, M6 17, M7 ≈ 16–17, M8 ≈ 8–9. M7 sigue siendo el más
cargado respecto de lo declarado y no se arregla solo con mover: ahí lo que ayuda es añadir lo que
falta (la figura con conmutadores y el recorrido de STL en cuatro pasos, §7, puntos 3 y 6), de modo
que el módulo siga largo pero cada tramo tenga su imagen. Con M4 articulada y M6 reordenada, los dos
módulos pesados son pesados por lo que enseñan, no por desorden. Si no se mueve nada, el declarado
debería corregirse (M4 ≈ 17–19, M6 ≈ 17, M7 ≈ 17–20, M8 ≈ 5, M9 ≈ 20 con quiz).

---

## 5. Empalme con el capítulo 2 y con la portada

### Lo que deja el M9 y lo que recoge el capítulo 2

El puente es limpio y de doble vía:

- M9 (3842–3846): «Aquí la tendencia y la estacionalidad se quitaron *para poder verlas*. Los modelos
  que vienen después… piden quitarlas por un motivo distinto… estacionariedad».
- Capítulo 2, M1 (2199–2201): «En el Capítulo 1 descompusimos una serie… para *modelar* la
  dependencia temporal necesitamos que las reglas del juego no cambien con el tiempo».

Lo que el capítulo 2 da por sabido en su apertura, y si el capítulo 1 lo enseñó:

| El capítulo 2 supone… | ¿Lo enseñó el capítulo 1? |
|---|---|
| tendencia, estacionalidad, residuo (2199) | Sí, a fondo. |
| `AirPassengers` y su nivel que sube y su dispersión que crece con el nivel (2203–2205, 2253) | Sí (M1, M3, M4). |
| «dependencia temporal» («misma forma de depender del pasado», 2204) | **Se nombra, no se muestra.** M1 la define de palabra; no hay ni un gráfico de rezagos ni una cifra de autocorrelación. |
| **«el gráfico de rezagos que vimos al final del Capítulo 1» (2440)** | **No.** El gráfico de rezagos aparece en M3 (no al final), como una viñeta (2536–2537) y una línea de código (2589); **no se dibuja.** El estudiante no lo vio. |
| «una serie con estacionalidad no es estacionaria… significan cosas opuestas» (2285–2289) | El capítulo 1 enseña «estacionalidad» durante nueve módulos y M9 introduce «estacionariedad» dos líneas después, sin avisar de la cercanía de las palabras. El capítulo 2 sí lo avisa. |
| «ruido blanco» como serie estacionaria (2268–2270) | El capítulo 1 llama «ruido» al residuo y pide que no tenga forma (2664–2668, 3054), sin mencionar que ese criterio se volverá una prueba (ruido blanco, ACF). M9 no pega los dos extremos. |

Conclusiones: el empalme *narrativo* funciona; el empalme *probatorio* tiene un hueco concreto (el
gráfico de rezagos) y una frase del capítulo 2 que hoy es falsa para el lector (2440). Arreglo mínimo:
una figura del gráfico de rezagos de `AirPassengers` (y de una serie sin dependencia, para
contraste) en M3 — haría verdadera la frase del capítulo 2 y daría a M1 la evidencia que le falta. Si
el gráfico se coloca en M3, la frase «al final del Capítulo 1» debería decir «en el Módulo 3».

### La tarjeta de la portada (`index.html` 655–659)

Texto: «Qué es una serie de tiempo y cómo se representa en software; gráficos estacionales y de
rezagos; los cuatro componentes…; medias móviles, descomposición clásica y STL, desestacionalización
y fuerza de cada componente». Meta: «9 módulos · 11 simuladores».

- **Cifras:** 9 módulos y 11 simuladores son correctas (11 `data-simulador` en el capítulo).
- **«gráficos estacionales y de rezagos»:** el de rezagos no se muestra (ver arriba). La tarjeta
  promete más de lo que hay.
- **Lo que el capítulo más desarrolla y la tarjeta no dice:** la decisión **aditivo o
  multiplicativo** (cuatro simuladores en M4, el «otra escala» de M6 y todo el logaritmo) y la
  **versión robusta de STL** con los dos casos del ejercicio 3. La tarjeta describe el temario; el
  capítulo gira en torno a un argumento (¿suma o producto?, ¿cómo lo mide el residuo?).
- **«los cuatro componentes»:** exacto, aunque el capítulo advierte que el ciclo casi no volverá a
  aparecer.
- No menciona autoevaluación ni ejercicios; por convención de la portada no hace falta.

---

## 6. Lo que funciona (no romper al revisar)

1. **M4 2710–2720 · la lectura del comparador y su promesa a M6.** «En el aditivo lo constante es la
   oscilación *en unidades*… en el multiplicativo, *en porcentaje*, y por eso en unidades crece» y
   «los mismos pasajeros de más en julio no es una manera de hablar»: la frase que prepara a M6. Es el
   punto donde la diferencia entre los dos modelos deja de ser un signo.
2. **M4 2722–2766 · del ojo al número, y del número a dos predicciones.** El abanico del M3 «ya
   apuntaba… conviene desconfiar de eso y convertirlo en un número»; la tabla de tres años; el
   gráfico con la horizontal (aditivo) y el rayo (multiplicativo) como predicciones rivales; y la
   frase que lo cierra: «ningún modelo describe la serie exactamente, se elige el que menos se
   equivoca». Es la mejor pieza de método del capítulo.
3. **M6 3208–3254 · el julio de 1955 como hilo.** «Ninguna de las tres cifras es un dato observado»;
   cada una con su origen (la ventana de trece meses con los once números a la vista; el promedio de
   once cocientes y su reescalado); los once cocientes que «empiezan cerca de 1,16 y acaban cerca de
   1,28» y la identidad que «se cumple siempre» y no es prueba de nada. El mismo julio vuelve en M7
   (3615–3639) y en el ejercicio 3: es lo que da unidad al segundo tramo del capítulo.
4. **M6 3299–3340 · «Qué habría pasado con la otra escala».** Cumple la promesa de M4, enseña un
   residuo con estructura y cierra con la frase que debería citar el resumen: «el residuo no se mira
   para confirmar que todo fue bien, se mira para descubrir en qué paso hay que volver a entrar».
5. **M7 3403–3462 · pesos tricúbicos, bordes y el simulador del ajuste local.** La tabla de pesos con
   «50 veces menos», la respuesta a los bordes con «12 de las 144 frente a ninguna» y el simulador cuya
   intro dice exactamente qué hacer (mueve el foco; lleva el foco a enero de 1949; baja los dos últimos
   controles a 0 y la curva *vuelve a ser* la media móvil de M5). El único lugar donde una afirmación
   de M5 (las tres decisiones) se prueba apretando un control.

También conviene no tocar: M5 2869–2874 («cada mes exactamente una vez»), M2 2478–2496 (índice más
clave identifica una fila, con el error a la vista), M3 2609–2614 («Cómo leer el abanico» como puente
a M4 y a M6) y la honestidad de 3674–3686 y 4056–4063 (con el argumento por defecto que decide el
resultado), aunque el primero deba cambiar de sitio.

---

## 7. Los ocho problemas que más dañan la comprensión (orden de daño)

1. **La dependencia temporal y el gráfico de rezagos nunca se muestran** (2328, 2345–2349, 2536–2537,
   2589, 3851; capítulo 2, 2440 dice «que vimos»).
2. **M3 anuncia cuatro gráficos y enseña uno;** subseries y rezagos son una línea de código (2521,
   2535–2537, 2588–2589), y faltan donde después harían falta (3233, 3528–3534).
3. **M7: la figura de STL no ilustra lo que el módulo promete** (3597 con `"periodic"` y sin `robust`;
   el aviso va después, 3674; la robustez es una tabla de pesos, 3572–3585, y su efecto está en el
   ejercicio 3, 4046–4049; la flexibilidad, una cifra, 3531–3533).
4. **«Ciclo» significa tres cosas** y el recuadro de M4 (2652) queda desmentido por M3 (2532), M6
   (2973, 3008, 3074), M7 (3511, 3529) y M9 (3995).
5. **M6 muestra el resultado a las 190 líneas y argumenta «la otra escala» con tres filas de números**
   (3188; 3232–3234, 3318–3320, 3331–3333); la descomposición aditiva y la U nunca se ven.
6. **M7 nunca enuncia STL como secuencia de pasos y carga ~12 términos nuevos** (3395–3401, 3440,
   3551–3552); el párrafo de M5 que lo anticipa es de los que se releen (2881–2891).
7. **M8: «0,994 y 0,937, muy fuertes» sin referencia,** con la ajustada hecha con el método clásico y
   la fuerza con STL sin decirlo; sin código; y el contraste está en un ejercicio plegado (3735–3742,
   3791–3793, 3975–3999).
8. **Costuras y cierre:** M1 → M2 sin antecedente (2396), M7 → M8 de trámite (3728), el resumen que
   repite «STL robusta» (3856) y omite el bucle (3851–3858), «Seis preguntas» sobre ocho (3864), y el
   puente al capítulo 2 enterrado antes del quiz (3842–3846).
