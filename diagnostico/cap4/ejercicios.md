# Cap. 4 · Diagnóstico de ejercicios, autoevaluación y práctica

Archivo: `Htmls_Series/capitulo-4-modelos-arima.html` (commit `71c42d8`, worktree
`course-content-improvement-227f2c`, 2026-11-22). Diagnóstico, sin ediciones en el repo. Las líneas
citadas son las del HTML ensamblado; el capítulo se ensambla desde `ensamblado/cap4/`, y cualquier
arreglo tiene que ir allí. Fuera de esta lente: la prosa expositiva, las fuentes (p. ej. «el modelo de
libro» del E1, 5492) y el diseño de las gráficas.

**Tres correcciones al encargo, medidas.** Hay **3** `ejercicio-guiado` (5489, 5577, 5653), no 5;
**10** `code-tabs` (20 bloques: 10 de R y 10 de Python); y las 13 líneas con `data-simulador="` son
**11 simuladores** (2866–5389), el simulacro (5816) y un comentario del JS (6362).

Leído: objetivos de los doce módulos (2761, 3010, 3226, 3548, 3716, 3911, 4100, 4314, 4550, 4851,
5787, 5857), los tres ejercicios (5489–5733), `AUTOEVALUACIONES['cap4']` (8887–9097), el motor del
quiz (7105–7470; corrección de la múltiple en 7403–7410), `TABLAS_RANKING['rejilla-nilo']` (8855), el simulacro (9403–9541) y la página
`preparcial-corte-2.html` (bloques A–D 5341–5860, su simulacro 5861–5929, el termómetro 6192–6300).

Escala de veredictos (la de los caps. 2 y 3): **sirve** (publicable con retoques cosméticos) · **se
puede mejorar** (núcleo sano, arreglos puntuales) · **hay que rehacer** (no mide lo que dice medir, se
responde sin entender, o enseña algo incorrecto).

**Lo que se marca aparte.** El simulacro del M11 lo escribe `exporta_simulacro.py` fuera del repo
(comentario 9389–9402) y es la variante 9 de un quiz de Brightspace ya aplicado; los ítems del
preparcial viven fuera del repo. Todo cambio sobre ellos va marcado **[fuera del repo]** y es una
decisión de Javier.

Guiones y salidas (todo en `diagnostico/cap4/diag/`, prefijo `ejercicios_`):

| Guion | Qué hace | Salida |
|---|---|---|
| `ejercicios_cap4.R` | reproduce E1–E3, recalcula las 8 claves del quiz y calcula las 10 del simulacro (sin clave en la página) | `ejercicios_cap4.out` |
| `ejercicios_vuelca.js` | evalúa los seis instrumentos (quiz, simulacro, bloques A–D, simulacro del preparcial) y los vuelca con texto visible, clave, pista, retro y tolerancia | `ejercicios_vuelca.json` |
| `ejercicios_longitud_opciones.js` | «la más larga / la más corta», posición, retros ausentes, tolerancias con la comparación exacta del motor | `ejercicios_longitud_opciones.out` |
| `ejercicios_extrae_preparcial.py` + `ejercicios_preparcial.R` | copia `PREPARCIAL_DATOS` (19 series publicadas) y recalcula las 38 claves del preparcial desde el enunciado o desde la serie | `ejercicios_preparcial_datos.json`, `ejercicios_preparcial.out` |
| `ejercicios_carga.py` | palabras de prosa, líneas de código, simuladores y duración declarada por módulo; dónde está la primera tarea | `ejercicios_carga.out` |
| `ejercicios_cobertura.py` | reparto por módulo de los cuatro instrumentos; series nombradas | `ejercicios_cobertura.out` |
| `ejercicios_en_pantalla.py` | busca en el capítulo la cifra de cada clave del quiz y lo que muestran los simuladores | `ejercicios_en_pantalla.out` |
| `ejercicios_series_candidatas.R` | series de R para los huecos (§7), medidas | `ejercicios_series_candidatas.out` |
| — | `grep -c` de las candidatas en `Htmls_Series/*.html` | `ejercicios_series_grep.out` |

Versiones: R 4.6.0; forecast 9.0.2; tseries 0.10.62 (cabecera de `ejercicios_cap4.out`).

---

## 0. Resultado de las ejecuciones

### 0.1 Soluciones de los ejercicios

| Ej. | Cifra escrita | Salida real | ¿Coincide? |
|---|---|---|---|
| 1 | varianzas 461.3769 · 2.0851 · 2.8823 · 8.5626; ADF p 0.5302; ndiffs 1 | idénticas | sí |
| 1 | rejilla de 9 (AICc, BIC, LB(20)) | idéntica | sí |
| 1 | ACF residual del (0,1,1): 0.0142 0.2483 0.1185 0.2087; banda 0.16 | idénticas | sí |
| 1 | φ 0.8799 (ee 0.0644), θ −0.6415 (ee 0.1035); Shapiro 0.6294597; auto.arima ARIMA(1,1,1) | idénticas | sí |
| 1 | AICc 514.902 (d = 1) y 515.859 (d = 2); \|raíz MA\| 1 | idénticas | sí |
| 2 | ndiffs 0/0; KPSS p 0.10, ADF p 0.01; varianzas 1.6532 · 0.6871 · 0.6026 · 1.1532 | idénticas | sí |
| 2 | \|raíz MA\| 1.0000 (2,1,1), 1.5076 (0,1,1); AR(2) 1.3776 −0.7399, módulo 1.1626, periodo 9.7839; LB p 0.009434283; auto.arima ARIMA(2,0,3) | idénticas | sí |
| 3 | ψ 1 1.2385 1.4485 1.6332 1.7958; σₕ y semianchos; error 2.398082e−14 | idénticas | sí |
| 3 | σ₁₂/σ₁ 6.7963; frente a la caminata 1.9619; ψ₁₂ 2.5593, límite 2.9883 | idénticas | sí |
| 3 | deriva 0.4001 (ee 0.2557, t 1.5644); AICc 515.062 / 514.902; h = 12: 266.99 / 263.76 | idénticas | sí |

**Todas las cifras de las tres soluciones son reproducibles.** Los problemas están en lo que el
ejercicio demuestra (E1), en dónde aparece ya la respuesta (E2, E3) y en la serie que usa (E2).

### 0.2 Claves

| Instrumento | Resultado |
|---|---|
| Quiz `cap4`, 8 preguntas | **las 8 claves son correctas**. Q2: σ₂ = 151.9673 (ψ₁ = 0.3802 sin redondear); Q1: 1267.507 / 1264.598 y \|raíz MA\| 1.032; Q3: ARIMA(0,1,5), r₁₂ 0.7245, r₂₄ 0.6727, banda 0.1633, Q(24) 222.3979; Q4: intercept 920.7037, `names(coef)` = ar1 ma1, aviso de Arima, ∇²ŷ(30) = 0; Q6: 0.498 0.385 0.328 0.239; Q7: el 7.º a 1.841; Q8: θ̂ = −1, raíz 1 |
| Simulacro M11 (sin clave en la página), calculadas | P1 ρ₂ = **0.3963** · P2 **a, c, e** · P3 A→AR(2), B→ARMA(1,1), C→MA(2), D→AR(1) · P4 **c** (1.1309, −0.5301) · P5 MA(2) 114.785 < MA(1) 115.587 < ARMA(1,1) 115.999 < AR(1) 125.047 · P6 **107.18** · P7 SES / «sobra la diferencia» (raíz 1.0417) / AR(2) 1.65 −0.65 / caminata con deriva / Holt (\|raíz\| 1.4907) · P8 **a** (gl 13, crítico 22.362, p 0.0379) · P9 **a, d, e** · P10 **d** |
| Preparcial, 38 ítems | **las 38 claves son correctas** (`ejercicios_preparcial.out`); las de datos salen de la serie publicada en la propia página |

### 0.3 Otras comprobaciones medidas

| Qué | Resultado |
|---|---|
| E1: puesto del IMA(1,1) por AICc entre los 9 de d = 1 | **8.º** (533.348; solo el (0,1,0) es peor); está 18.446 por encima del mejor |
| E1: LB del IMA a 10 rezagos | p = 0.0026 (a 20, 0.0340) |
| E1: rejilla completa con d = 2 | mejor (1,2,2) 515.859, \|raíz MA\| 1.0000; **el menor AICc de d = 2 no es menor que el de d = 1** (FALSE) |
| E1: lectura literal del enunciado («su AICc», el del IMA) | 533.348 frente a 515.859: el d = 2 «gana» por 17.489 |
| E2: otros órdenes con d = 1 | ARIMA(3,1,1) también da \|raíz MA\| = 1; ARIMA(1,1,1), 2.098; auto.arima por defecto, ARIMA(2,0,4) |
| E3: `Arima` (CSS-ML) frente a `arima(ML)` | φ 0.8800 / 0.8799, θ −0.6415 / −0.6415, AICc 514.9016 en los dos |
| Q5: KPSS, 1000 réplicas, semilla 2026, en el orden β = 0, 100, 247.78 | 0.048 · **0.720** · 1.000 (el capítulo y la retro dicen 70.8 % para β = 100: depende del orden de las llamadas al generador; no afecta a la clave) |
| Q2 en pantalla | `DATOS_CAP4.nilo.intervalos.sigma_h` = [142.045, **151.967**, 155.221]: el simulador `pesos-psi-sigma` la imprime al poner h = 2 (lectura en 8627–8637) |
| Preparcial D6 (`usuarios`) | `arima(ML)`: semiancho 5.010 → 128.013, razón **25.549** (la página dice «25.6 veces», cociente de los redondeados); con `Arima` (CSS-ML), 5.07 → 129.46 |

---

## 1. Cobertura: objetivo × dónde se practica, y cuánto se lee sin hacer nada

### 1.1 La primera tarea llega al final del M10

`ejercicios_carga.out`:

| Mód. | Palabras de prosa | Líneas de código | Simuladores | Duración declarada |
|---|---|---|---|---|
| M1 | 1047 | 70 | 1 | 12 min |
| M2 | 818 | 42 | 0 (el ciclo de pestañas) | 10 |
| M3 | 1628 | 78 | 1 | 16 |
| M4 | 648 | 50 | 1 | 14 |
| M5 | 839 | 65 | **0** | 12 |
| M6 | 699 | 62 | 1 | 16 |
| M7 | 680 | 70 | 1 | 14 |
| M8 | 888 | 77 | 1 | 16 |
| M9 | 1409 | 79 | 2 | 16 |
| M10 | 3845 | 343 | 3 | 24 |

- **La primera tarea con respuesta comprobable es el quiz, en la línea 5473**, dentro del M10, después
  de la TRM y del puente. Los tres ejercicios van detrás (5489, 5577, 5653).
- Antes de ella hay **11 324 palabras** de prosa (8656 de M1–M9 y 2668 del M10 hasta el quiz): **57 min a
  200 palabras por minuto, 75 min a 150**, sin contar los bloques de código ni los simuladores. Con
  la duración que el propio capítulo declara, **126 min (M1–M9) más la mayor parte de los 24 del M10**.
- Lo único que pide algo antes son las consignas de los simuladores («Empieza en |β| = 0… busca dónde
  cruza la curva el 50 %», 3323–3324; «Cambia el orden y lee», 3566; «Empieza en d = 1… mira…», 3953–3957;
  «Cambia al modo exhaustivo», 4147; «Sube el orden d», 4339; «Cambia el modelo y observa», 4563; «Mueve
  el horizonte», 4640; «Cambia de serie y compara», 4969). **Ninguna recoge respuesta y casi todas la
  dicen en la misma frase**: la del M4 anuncia qué se verá en cada d (3566–3575), la del M6 que «cuatro
  modelos quedan a menos de 2 puntos» (3953–3955), la del M8 que «el θ̂ se clava en −1» (4339–4341).
- **El M5 no tiene ningún elemento interactivo**: 839 palabras y 65 renglones de código, sin simulador,
  sin consigna y sin pregunta retórica que se responda después.

### 1.2 Objetivo × práctica

Reparto del quiz por etiqueta `modulo`: M3 1 · M4 1 · M5 1 · M6 1 · M7 1 · M8 1 · M9 1 · M10 1 ·
**M1 y M2: 0** (`ejercicios_cobertura.out`).

| Mód. | Objetivo (resumen) | Quiz `cap4` | Ejercicio | Simulacro M11 / preparcial | Práctica real dentro del capítulo |
|---|---|---|---|---|---|
| M1 | d es parte del modelo; qué le hace al polinomio | — | — (E3 usa la expansión en su pista) | P7 / B7, C4 | **NADA.** Escribir un ARIMA como ARMA(p+d, q), ver la raíz impuesta frente a la estimada, la equivalencia IMA ↔ SES: solo fuera del capítulo |
| M2 | recorrer el ciclo y saber qué hallazgo obliga a volver | — | E1 (implícito: el IMA falla y hay que volver) | P8 / A4 | Solo E1, y la vuelta atrás está dada en la pista (5505–5506) |
| M3 | decidir d con tres evidencias; por qué las pruebas engañan | Q5 (recuerda el experimento) | E1 (d trivial), E2 (la varianza miente) | P9, P10 / C5 | **Decidir d sobre una serie nueva con un escalón: NADA.** Q5 pregunta el resultado del experimento, no la decisión |
| M4 | ACF/PACF sobre la serie diferenciada; candidatos | Q6 (el gráfico del simulador) | E1 | P10 / D5 | E1 |
| M5 | qué es c según d; por qué el software cambia | Q4 (comportamiento de funciones) | E3 (deriva de BJsales) | — / B8, C6, S4 | Decidir la deriva: E3. Q4 pide recordar valores por defecto |
| M6 | la rejilla; el AICc no cruza d | Q1 (las cifras de la tabla del M6) | E1 (la trampa no muerde, §3) | — / B9, C7, S5 | E1, débil |
| M7 | auto.arima: reglas, búsqueda, límite | Q7 (las cifras de la tabla del M7) | E1 (una llamada) | — / A5 | **Abrir la traza, comparar escalonada y exhaustiva sobre otra serie: NADA** |
| M8 | firma de la sobrediferenciación; cerrar el Nilo (escalón) | Q8 (se le da θ = −1) | E2 | — / A4 (raíz MA), C8 (normalidad) | Firma: E2, con la respuesta impresa en 4384–4389. **Escalón frente a raíz unitaria en otra serie: NADA** (tampoco en el preparcial) |
| M9 | d y c deciden la forma; el intervalo desde los ψ | Q2 (la cifra la imprime el simulador) | E3 | — / B10, B11, D6, S6 | E3, con la respuesta impresa en 4662–4665 |
| M10 | ciclo completo en otra serie; aceptar «no hay señal»; el puente | Q3 (el puente) | E1 (ciclo completo) | — / A6, B12 | **Aceptar una caminata aleatoria en una serie nueva: NADA** |

**Módulos sin ninguna práctica dentro del capítulo: M1.** El M2 solo a través de E1. **Sub-objetivos
centrales sin práctica:** el escalón frente a la raíz unitaria (M3/M8, la lección que vertebra el
capítulo), la búsqueda de auto.arima sobre otra serie (M7) y el resultado «no hay nada que modelar»
(M10). Los tres los cubre solo el Nilo o la TRM, que el estudiante ve resueltos.

---

## 2. Fichas del quiz (`AUTOEVALUACIONES['cap4']`, 8887–9097)

**Motor** (7105–7470). En `opcion` y `grafico`, el primer fallo deshabilita la opción, muestra la
`pista` y deja reintentar; el segundo marca la correcta y muestra la `retro` de la elegida. En
`multiple`, el primer fallo dice «De las N que marcaste, X están en la respuesta, y te faltan Y» y añade
la pista (7403–7410); el segundo, el `retroFallo` y un desglose por opción con la `retro` de cada una
(`desgloseMultiple`, 7239). La numérica acepta `Math.abs(dada − respuesta) <= tolerancia` (7326).
**El «Resultado: X de 8» suma los aciertos al segundo intento** (`alPrimero + alSegundo`, 7202): con
cuatro opciones, la pista y una descartada, el segundo intento es casi gratuito.

**Claves: las ocho son correctas** (§0.2).

Las cuatro formas de contestarse solo (`ejercicios_longitud_opciones.out`):

- **(a) Posición** — sana: 2 3 1 4 3 en las cinco de una sola; reparto 1→1, 2→1, 3→2, 4→1.
- **(b) Tamaño** — **la más larga acierta 4 de 5**: Q1 (86 frente a ≤ 74), Q5 (91 frente a ≤ 72), Q6
  (93 frente a ≤ 67), Q7 (109 frente a ≤ 98). Solo Q3 se libra (81 frente a 87). En Q4 (múltiple) ni las
  tres más largas ni las tres más cortas aciertan.
- **(c) Pistas** — **las ocho dan el criterio o el cálculo**, no por dónde entrar: Q1 «pregúntate si están
  calculados sobre los mismos datos»; Q2 la fórmula con «entran solo dos términos: ψ₀ = 1 y ψ₁»; Q3
  «¿Tienen algo en común los números 12 y 24 en una serie mensual?»; Q4 «**Son tres**» y los tres temas;
  Q5 el mecanismo de las sumas parciales; Q6 «¿Qué condición exige la tabla?»; Q7 «Compara ese umbral
  con la distancia entre el primero y el séptimo»; Q8 «B = −1/θ. Sustituye θ = −1». En Q4 el motor añade
  cuántas faltan: con «Son tres» y «te falta 1», el segundo intento es aritmética.
- **(d) Filtraciones** — **las ocho respuestas están en pantalla en el propio capítulo**
  (`ejercicios_en_pantalla.out`): Q1 en la tabla del M6 (3986) y en 3993, 4037, 4903; Q2 en la lectura
  del simulador `pesos-psi-sigma` con h = 2 (151.967); Q3 es el gráfico del simulador `puente-estacional`
  y sus cifras están en 5402–5407; Q4 (920.7037) en 3829; Q5 (100 %) en 3299, 3345, 4397, 5448; Q6 es la
  opción d = 0 del simulador `identificacion-nilo` y sus cifras están en 3559, 3659, 4360; Q7 en la tabla
  del M7 (4187); Q8 en la tabla del M8 (4363) y en el bloque 4460. Además, **la retro de la correcta de
  Q1 (8902) responde la última parte del E1** («Para decidir entre distintos d hay que usar…»), y el quiz
  está antes que los ejercicios.
- **Recuerdo, no transferencia**: siete preguntas usan el Nilo y la octava (Q3) el AirPassengers del
  puente. Ninguna pide aplicar una decisión a una serie o a unas cifras que el estudiante no haya visto
  resueltas.
- **Retro por opción**: **Q4 no lleva `retro` en ninguna de sus 5 opciones** (5 de 25 en el quiz), así
  que el desglose del segundo fallo lista las opciones sin explicar ninguna. Contradice la regla del motor
  (7121) y dos promesas al estudiante: «Cada opción trae su explicación, también las incorrectas»
  (5476–5477) y «La autoevaluación del Módulo 10 sí lleva pista y explicación de cada opción» (5812).
- **Tolerancias**: no castigan el redondeo. Q2 (151.97 ± 0.4) acepta 151.6, 151.66 y 152, y rechaza los errores
  típicos 54.0 (sin ψ₀), 166.88 (sin cuadrado) y 200.88 (caminata). Q8 (1 ± 0.002) acepta 0.999 y 1,
  rechaza −1 y 0; con θ = −1 dado, no hay nada que redondear.

| # | Línea | Tipo · etiqueta | Nivel | Veredicto |
|---|---|---|---|---|
| Q1 | 8889 | opción · M6 | comprender (cifras del M6) | se puede mejorar |
| Q2 | 8917 | numérica · M9 | aplicar una fórmula dada en la pista | se puede mejorar |
| Q3 | 8927 | gráfico · M10 | comprender (gráfico ya visto) | se puede mejorar |
| Q4 | 8963 | múltiple · M5 | recordar valores por defecto | se puede mejorar |
| Q5 | 8978 | opción · M3 | recordar un resultado del módulo | **hay que rehacer** |
| Q6 | 9006 | gráfico · M4 | comprender (gráfico ya visto) | se puede mejorar |
| Q7 | 9040 | opción · M7 | comprender (cifras del M7) | se puede mejorar |
| Q8 | 9068 | numérica · M8 | sustituir un número | **hay que rehacer** |

**Q1 · AICc de d = 1 frente a d = 2.** Mide la trampa central del capítulo y los distractores son buenos
(c acierta por la razón equivocada, d prueba que el BIC no salva). Pero las cifras son las de la tabla
del M6, la correcta es la más larga y la pista dice el criterio. *Mejora*: dar otra serie (p. ej. el
caso de `austres` o `aus_airpassengers`, §7, donde KPSS y ADF no coinciden en d) y pedir la decisión, con
opciones de longitud pareja y una pista que pregunte qué cambia entre las dos verosimilitudes sin
responderlo.

**Q2 · σ₂ del Nilo.** La cifra y el ψ₁ son los que el simulador imprime; la pista da la fórmula y dice
qué dos términos entran. Con eso solo queda multiplicar. *Mejora*: otro proceso (p. ej. un ARIMA(1,1,0)
con φ dado) y h = 3, que obliga a obtener ψ₂ de la expansión del M1, que es lo que el módulo enseña.

**Q3 · residuales con picos en 12 y 24.** Clave bien, posición y tamaño sanos. Pero el enunciado pone
«mensual» en negrita, la pista pregunta qué tienen en común 12 y 24, y el gráfico es el del simulador. Y
mide el puente al cap. 5, no el objetivo del M10 (recorrer el ciclo en otra serie, aceptar «no hay
señal»). *Mejora*: quitar la negrita y la pista que responde; añadir un ítem del M10 propiamente dicho
(§7, `GOOG 2018`).

**Q4 · la constante (múltiple).** Clave a, b, d correcta. Faltan las cinco `retro`; la pista anuncia
«Son tres». Dos de las tres correctas (b, d) son comportamientos de funciones concretas
(`include.mean` ignorado, aviso de `Arima`): miden memoria de la documentación, no la idea del módulo
(qué significa c según d y qué forma da al pronóstico). *Mejora*: escribir las cinco retro, quitar «Son
tres», y cambiar b o d por una afirmación sobre la forma del pronóstico con y sin constante.

**Q5 · KPSS con escalón.** Pregunta el resultado numérico del experimento del M3, con su mismo diseño
(posición 29, el Nilo); la correcta es la más larga y cita la cifra del módulo; la pista explica el
mecanismo. Se contesta recordando, y no mide la decisión que el módulo pide (decidir d cuando las
evidencias discrepan). *Rehacer*: dar las tres evidencias de otra serie con escalón —`beaver2`, §7, donde
las tres pruebas piden d = 1 y un AR(1) con escalón pasa Ljung–Box— y pedir qué se hace antes de
diferenciar.

**Q6 · ACF sin diferenciar.** Buen ítem (el distractor c acierta por la razón equivocada). Pero el
gráfico es el del simulador en d = 0, la correcta es la más larga (93 frente a ≤ 67) y la pista dice la
condición. *Mejora*: otra serie, opciones de longitud pareja.

**Q7 · siete modelos a menos de 2.** La lección es la buena (comunicar el empate); las cifras son las de
la tabla del M7 y la pista hace la comparación. *Mejora*: la traza de otra serie (§7, `BJsales.lead`: 8
modelos a menos de 2), sin dar el umbral en la pista.

**Q8 · módulo de la raíz con θ = −1.** Da hecho lo único que había que descubrir (θ̂ = −1); la pista da
la fórmula y la sustitución; la cifra está en la tabla del M8. No mide la firma de la sobrediferenciación,
mide dividir −1 entre −1. *Rehacer*: dar las varianzas por d, ρ₁ y el θ̂ de un MA(1) ajustado a cada
diferencia de una serie nueva (como la tabla 4357–4366, pero de otra serie) y pedir d con su argumento.

---

## 3. Fichas de los ejercicios guiados (M10, 5489–5733)

Comunes a los tres: el enunciado no fija entregables (qué entregar, con qué forma); las soluciones solo
están en R (3 bloques `language-r`, 0 de Python), en un capítulo que da todo en los dos lenguajes; y los
tres van después del quiz, en el último módulo.

| Ej. | Serie | Módulos | Veredicto |
|---|---|---|---|
| E1 | BJsales | M2, M3, M4, M6, M8 | **se puede mejorar** |
| E2 | log(lynx) | M3, M8 | **hay que rehacer** |
| E3 | BJsales (ARIMA(1,1,1) del E1) | M9, M5 | **se puede mejorar** |

**E1 · el ciclo completo sobre BJsales (5489).** Es el único ejercicio de ciclo completo y sus cifras se
reproducen todas. Tres problemas:
1. **La pista da los resultados**: «la varianza cae de 461.4 a 2.1» y «mira… en particular los rezagos 2
   y 4» (5504–5506) es el hallazgo, no por dónde entrar.
2. **La lección que la discusión saca no la demuestra el ejercicio.** «Un criterio de información no
   sustituye al diagnóstico» (5566–5567): pero el IMA es el **8.º de 9 por AICc** (533.348, 18.446 por
   encima del mejor). El AICc ya lo descarta; diagnóstico y criterio dicen lo mismo.
3. **La trampa de d = 2 no muerde.** El mejor de d = 2 (515.859) tiene más AICc que el de d = 1
   (514.902): la comparación ilegítima lleva a la misma conclusión que la legítima. Y el enunciado es
   ambiguo: «comparas **su** AICc» (5494) se refiere al IMA, y en esa lectura (533.348 frente a 515.859)
   la trampa sí muerde, por 17.489; la solución compara otra cosa. Además, la retro de la correcta de Q1
   ya da la respuesta.
*Mejora*: pista que pregunte, sin cifras; enunciado que pida explícitamente comparar el IMA con el mejor
de d = 2 (donde el error lleva a elegir mal); dejar la lección «criterio frente a diagnóstico» para un
caso donde el mejor por AICc no pase Ljung–Box.

**E2 · ¿hay que diferenciar log(lynx)? (5577).** Cifras reproducibles, pero:
1. **La respuesta está impresa en el M8**, con sus cifras y su nombre: «sobre log(lynx), diferenciar
   reduce la varianza un 58 % (1.653 → 0.687) y aun así d = 1 sobra, como coinciden en señalar ADF, KPSS y
   Phillips–Perron… el ARIMA(2,1,1) sobre esa serie da |raíz MA| = 1.000… (Es el ejercicio 2 de este
   capítulo.)» (4384–4389).
2. **La pista también la da**: «aquí el criterio de la varianza te va a mentir… ajusta… un ARIMA(2,1,1)
   y mira el módulo de la raíz» (5591–5595).
3. **`lynx` ya es práctica del cap. 3.**
Queda nada por descubrir. *Rehacer* con otra serie y sin la frase del M8 (o moviéndola tras el
ejercicio). Candidata medida (§7): las anomalías de `nino3.4`, donde la varianza cae de 0.7742 a 0.11 y
las tres pruebas dicen d = 0, pero **la firma de la raíz MA no aparece** (mínimo 1.1434 en la rejilla con
d = 1): el ejercicio tendría que decidir con las pruebas y con ρ₁ (0.926), y enseña que la firma no siempre
salta. Para la firma, una AR(2) simulada con semilla, como `pedidos` del preparcial.

**E3 · el intervalo desde los ψ (5653).** Cifras exactas; la pista dice por dónde entrar (expandir como
ARMA(2,1) y no mezclar `arima` con `Arima`), que es lo que debe hacer una pista. Pero:
1. **La respuesta está en el M9**: «Sobre BJsales (ejercicio 3) el mismo tipo de modelo da ψ∞ = 2.99: a
   doce pasos σₕ ya es 1.96 veces el de una caminata» (4662–4665).
2. La solución es el bloque del M9 (4767–4784) con la serie cambiada: transcribir, no construir.
*Mejora*: quitar la frase del M9 (o dejarla sin cifras); pedir algo que el bloque no hace, por ejemplo
predecir el ψ∞ con la fórmula cerrada antes de calcular, o comparar con un ARIMA(0,1,1) de la misma
serie (un modelo cuyos ψ no hay que expandir).

---

## 4. Simuladores como práctica

Once simuladores, todos sobre el Nilo, la TRM o AirPassengers. Ninguno tiene una tarea con respuesta
que el estudiante deba producir antes de leerla: las consignas de §1.1 vienen con el resultado dicho. Dos
de ellos son además la fuente literal de preguntas del quiz (Q2, Q3, Q6). La tabla ordenable
`rejilla-nilo` (8855) dice en su descripción y en su pie cuál es la ordenación inválida y cuáles son los
mejores por d.

---

## 5. [fuera del repo] Simulacro del M11 (`SIMULACROS['cap4-simulacro']`, 9403–9541)

Variante 9, sin clave ni retro por diseño (5809–5813). Claves calculadas en §0.2.

- **Una sola respuesta defendible por ítem**: sí en los diez con las reglas de los módulos (en P3, B tiene
  la PACF que decae alternando y C la ACF que corta tras el 2; «sobran dos» deja MA(1) y ruido blanco).
- **Posición**: 3, 1, 4 en las tres de una sola (P4, P8, P10). **Tamaño**: ninguna correcta es la más
  larga ni la más corta (P4 y P10 tienen las cuatro opciones de igual longitud; P8, 111 frente a
  111–116). **Las múltiples no anuncian cuántas** (P2 y P9: tres correctas de cinco cada una).
- **Etiquetas**: dicen el módulo, como promete el texto (5811–5812); la de P8 («Ljung-Box y grados de
  libertad») apunta a la trampa del ítem.
- **Cobertura del cap. 4**: P7–P10, solo 4.1–4.4, como el quiz real.
- **P6** (107.18) se calcula elevando al cuadrado: el redondeo intermedio de 10.3529 a 10.35 cambia la
  segunda cifra decimal; la tolerancia de Brightspace no está en la página y no se puede comprobar aquí.

Veredicto: **sirve** como ensayo. El sesgo que sí tiene es de diseño: sin clave, quien no sepa
contrastarlo con el material no sabe si acertó; el texto lo dice y remite a los módulos.

---

## 6. [fuera del repo] Preparcial del Corte II (`preparcial-corte-2.html`)

32 ítems en cuatro bloques más un simulacro de 6; 19 del cap. 4 (4.1: 2 · 4.2: 1 · 4.3: 1 · 4.4: 1 ·
4.5: 3 · 4.6: 3 · 4.7: 1 · 4.8: 1 · 4.9: 4 · 4.10: 2). Corre sobre 19 series generadas, ninguna del
material.

- **Claves: las 38 son correctas**, recalculadas desde el enunciado o desde la serie publicada en la
  página (`ejercicios_preparcial.out`). Cosmético: D6 dice «25.6 veces» y el cociente sin redondear es
  25.549.
- **Posición** sana: 1→6, 2→5, 3→5, 4→5 en 21 ítems de una sola; racha máxima 1 en cada bloque.
- **Tamaño** sano: la más larga acierta 0 de 5 (A), 2 de 8 (C: C2, C3), 0 de 6 (D) y 0 de 2 (simulacro); la
  más corta, 1 de 8 (C6) y 1 de 6 (D2).
- **Retro por opción**: completas (0 ausentes de 25, 32, 24 y 8 opciones en A, C, D y el simulacro).
- **Pistas**: varias dan el criterio (D1 da la condición φ₁² + 4φ₂ < 0 y el signo de ρ₁; C4 «suma φ₁ +
  φ₂ y recuerda la firma»; A4 da las dos reglas de la raíz), pero **el termómetro cuenta solo el primer
  intento** (6219, 6232), así que no inflan el diagnóstico. La múltiple A5 no anuncia cuántas, aunque el
  motor dice cuántas faltan (4612–4617).
- **Tolerancias**: casi todas aceptan el redondeo honesto. Tres bordes:
  - **S5 (BIC, 395.67 ± 0.015) acepta el error que el ítem quiere detectar**: con n = 101 en lugar de
    n* = 100 y log redondeado a 4.6 sale 395.66, aceptado. Usar n o n* cambia el BIC en 0.02: el ítem no
    puede separar las dos cosas.
  - B10 (99.33 ± 0.01) rechaza 99.34, que es lo que da φ redondeado a 0.49 (99.339), y 99.32: solo
    acepta la cifra exacta.
  - B3 (4.19 ± 0.01) rechaza 4.18 y acepta 4.20 (borde asimétrico por coma flotante); S4 rechaza 73.11,
    el intercept truncado.
- **Hueco**: ningún ítem sobre el escalón frente a la raíz unitaria (el núcleo del M8); el único
  etiquetado 4.8 (C8) mide normalidad e intervalos, que es contenido del M9 (4729–4739).
- **Fecha**: el M12 del capítulo dice «el Parcial 2 es el miércoles 14 de octubre» en futuro (5863); la
  sesión es del 22 de noviembre de 2026.

Veredicto: **sirve**. Es el instrumento mejor construido de los cuatro.

---

## 7. Datos: qué series usa la práctica y cuáles faltan

**Series de la práctica del cap. 4**: BJsales (E1, E3; nueva), **log(lynx) (E2; repetida del cap. 3)**,
Nilo (7 preguntas del quiz), AirPassengers (Q3). Simulacro y preparcial: sintéticas. Ninguna de las
candidatas de abajo aparece en `Htmls_Series/` (`ejercicios_series_grep.out`) ni en las listas de los
caps. 2–3. Todas las cifras, de `ejercicios_series_candidatas.out`.

| Hueco | Candidata | Lo medido que la hace servir |
|---|---|---|
| **M1** · raíz estimada frente a impuesta | `NelPlo[, "gnp.real"]` (tseries; ya en logaritmos, rango 4.76–7.09; n = 80) | AR(2) en niveles: φ* = (1.4659, −0.4685), suma 0.9974, \|raíz\| 1.0050; ARIMA(1,1,0): φ = 0.4663 frente a −φ₂* = 0.4685 |
| | `NelPlo[, "ip"]` (n = 129) | suma 0.9990, \|raíz\| 1.0012; φ = 0.1910 frente a 0.1919 |
| **M1** · IMA(1,1) = SES | `BJsales.lead` (n = 150) | 1 + θ = 0.5525, α de `ses()` 0.5502, mismo pronóstico 13.514 |
| **M3/M8** · escalón frente a raíz unitaria | `ts(beaver2$temp)` (n = 100; actividad desde la obs. 39) | KPSS p 0.01, ADF p 0.5696, PP p 0.4556: **las tres piden d = 1** y auto.arima da ARIMA(0,1,0); con escalón: β 0.6139 (ee 0.1381), φ 0.8733, LB(10) p 0.5351; KPSS rechaza en el 96.5 % de 400 réplicas de ese AR(1) con escalón. Solo se halló una serie real limpia; la segunda, una simulación con semilla |
| **M7** · auto.arima sobre otra serie | `austres` (n = 89) | ndiffs KPSS 2, ADF 1, PP 1; **escalonada ARIMA(0,2,1) ≠ exhaustiva ARIMA(3,2,0)**; 7 frente a 21 modelos; 4 a menos de 2 |
| | `tcm1y` (tseries, n = 558) | escalonada ARIMA(4,1,3) ≠ exhaustiva ARIMA(0,1,5); 31 frente a 42 modelos |
| | `BJsales.lead` | 8 modelos a menos de 2 del mejor en la exhaustiva |
| **M5** · ¿lleva deriva? | `log(airmiles)` (n = 24) | deriva t = 4.47; AICc −20.89 con, −11.13 sin |
| | `aus_airpassengers` (tsibbledata/fpp3, n = 47) | t = 4.81; AICc 202.86 / 215.89; y KPSS pide d = 2 frente a ADF/PP d = 1 |
| | `BJsales.lead` | caso frontera: t = 1.94; AICc 49.04 / 50.49 |
| **M10** · «no hay nada que modelar» | GOOG 2018 (`gafa_stock`, n = 251) | auto.arima ARIMA(0,1,0); una barra fuera de 20, en el rezago 8 (−0.1434), como la TRM; LB(20) p 0.0382; Shapiro p 7.1e−05; curtosis 4.0 |
| | FB (`gafa_stock`, n = 1258) | auto.arima ARIMA(1,1,1) con AR 0.8151 y MA −0.8637 (raíces 1.2269 y 1.1578, casi se cancelan); LB(20) de las diferencias p 0.4080 |
| | `NelPlo[, "stock.prices"]` (n = 118) | auto.arima ARIMA(0,1,1) con deriva; LB(20) p 0.0900; Shapiro p 0.00045 |
| **Sustituto del E2** · la varianza miente | `nino3.4` menos su media mensual (n = 598) | varianza d0/d1/d2 0.7742 / 0.11 / 0.2112; KPSS/ADF/PP → d = 0; nsdiffs 0; **la raíz MA no delata** (mínimo 1.1434 en la rejilla con d = 1). `nino3` en bruto **no** sirve: nsdiffs 1, r₁₂ 0.406 |

---

## 8. Lista de huecos (por prioridad)

1. **E2 se responde leyendo el M8** (4384–4389) y su pista; además repite `lynx`. Rehacer con otra serie
   y retirar la frase del M8 o moverla tras el ejercicio.
2. **El quiz se contesta recordando**: 8 de 8 respuestas en pantalla, 7 de 8 sobre el Nilo, la más larga
   acierta 4 de 5, 8 pistas dan el criterio, y la retro de Q1 responde el E1. Rehacer Q5 y Q8; en las
   demás, otra serie, opciones parejas y pistas que pregunten.
3. **Q4 sin retro en sus 5 opciones**, contra lo que prometen 5476–5477 y 5812; y «Son tres» en la pista.
4. **No hay ninguna tarea antes del final del M10**: 11 324 palabras (57–75 min; 126 min declarados para
   M1–M9) sin una respuesta comprobable. Las consignas de los simuladores dicen el resultado. Cada módulo
   necesita al menos una pregunta corta con respuesta antes de seguir; el M5 no tiene ni un simulador.
5. **Sin práctica sobre otra serie** para el escalón (M3/M8), auto.arima (M7) y «no hay señal» (M10); el
   M1 no tiene ninguna. Candidatas medidas en §7.
6. **E1 no demuestra lo que concluye**: el IMA ya pierde por AICc (8.º de 9) y la trampa de d = 2 no
   muerde en la comparación que hace la solución; la pista da los resultados; «su AICc» es ambiguo.
7. **E3 está resuelto en el M9** (4662–4665) y repite su bloque.
8. El «Resultado: X de 8» cuenta los aciertos al segundo intento como aciertos (7186).
9. Las soluciones no tienen versión en Python.

### 8 bis. [fuera del repo]

- Preparcial: S5 acepta el error de n frente a n* (395.66); B10 solo acepta la cifra exacta; ningún ítem
  sobre el escalón; C8 etiquetado 4.8 mide contenido del M9; «25.6 veces» frente a 25.549.
- M12 anuncia en futuro un parcial del 14 de octubre.
- Simulacro M11: sin sesgos de posición ni de tamaño; la etiqueta de P8 señala la trampa.
