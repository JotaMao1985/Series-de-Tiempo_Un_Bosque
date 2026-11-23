# Capítulo 4 · ronda R5 «práctica» · cambios

Fecha: 2026-11-23. Un solo redactor (subagente redactor R5, Fable 5.2). **Sin commits ni push.**
Alcance: T5.1 y T5.2 del plan (`PLAN_Mejora_Cap4.md`), decisión **D9**. Base: `b53fdcb`.
Fuente: `diagnostico/cap4/ejercicios.md` (del 22 nov, sobre `71c42d8`), contrastado con el estado
actual tras R1–R4 (§0), y las 28 notas que la R4 dejó para esta ronda (§4).

Archivos tocados:

- `ensamblado/cap4/templates_1_3.html`, `templates_4_6.html`, `templates_7_9.html`: nueve bloques
  `.exercise` «Para practicar», uno al final de cada módulo del 1 al 9; en `templates_7_9.html`,
  además, dos frases sin marca (M8 y M9, §2.4).
- `ensamblado/cap4/templates_10.html`: los ejercicios 1, 2 y 3.
- `ensamblado/cap4/chapter.js`: `AUTOEVALUACIONES['cap4']` entero y dos constantes nuevas delante
  (`ACF_P6`, `N_P6`). Nada más: ni el simulacro ni el motor.
- `ensamblado/ensambla_cap4.py`: los minutos de `courseData.modules` y su comentario, **y la
  comprobación final del número de ejercicios** (exigía 3 `.ejercicio-guiado`; ahora 12, con sus
  paneles `c4mN-*`). Esto último se sale de «solo los minutos», pero sin ello el ensamblado aborta.
- `Htmls_Series/capitulo-4-modelos-arima.html`: reensamblado (662 → 717 KB; 677 423 bytes antes).
- `Htmls_Series/index.html` y `Htmls_Series/README.md`: «40 ejercicios» → «49 ejercicios»
  (`cuenta_sitio.py`).
- `diagnostico/cap4/comprobaciones/r5_*`: guiones y salidas (§9).

No se tocó: `SIMULACROS['cap4-simulacro']`, `preparcial-corte-2.html`, el motor del quiz y el de los
ejercicios, el CSS, los simuladores, los capítulos 1–3, 5 y 6, `precalculo/`, `bibliografia/`.
Ninguna clase nueva de Tailwind, ningún CSS nuevo. **Ninguna frase con `data-afirma` cambió, ninguna
se añadió y ninguna desapareció** (§7).

**Cómo está hecha la edición.** `r5_edita.py` parte de `git show b53fdcb:…` y aplica cuatro pasos
(`r5_ediciones_cortos.py`, `_m10.py`, `_quiz.py`, `_minutos.py`): es reejecutable. El código de las
soluciones no está escrito en los guiones: cada bloque vive en `r5_bloques/<id>.R`, `r5_reprex.R` lo
ejecuta y escribe cada salida real bajo su línea tras `#> ` (`r5_bloques/<id>.out`), y eso es lo que
se pega. Las cifras de prosa, pistas, retros y claves que no salen bajo un `#>` del capítulo están en
`r5_cifras.out`, con etiqueta.

---

## 0 · Lo que ya estaba resuelto al empezar

| Hallazgo del diagnóstico (`ejercicios.md`) | Estado en `b53fdcb` |
|---|---|
| E1 y E2 usaban la varianza como criterio de $d$ (§3, plan §1) | Resuelto por la R1: los dos ya dicen que la varianza repite $r_1$. Quedaba todo lo demás de §3 |
| Q4: «con $d = 1$ la constante es la media de las diferencias» (plan §1) | Resuelto por la R1 («la deriva, $\mu_w = c/\phi(1)$…»). Quedaban las retro y «Son tres» |
| Q6: «sin acercarse a cero» con $r_{10} = 0.09$ | Resuelto por la R1 (la retro ya daba el recuento de barras). El ítem se rehace ahora con otra serie |
| Q5: «70.8 %» frente a 0.720 según el orden del generador (§0.3) | La R1 llevó la cifra a `genera_cap4.R`; el ítem desaparece ahora |
| Introducciones de simulador que daban el resultado (§1.1, §4) | Resuelto por la R3 en M1, M3, M4, M6, M8 y M10 |
| `aria-label` y `descripcionGrafico` del quiz | Resuelto por la R2 |
| «el modelo de libro» del E1 | Resuelto por la R4 (c4-m10-61) |
| Preparcial y simulacro (§5, §6, §8 bis) | Fuera del repo; sin cambio (ver §8) |

Seguía vigente: ninguna práctica antes del final del M10; E2 resuelto en el M8 y con `lynx`; E3
resuelto en el M9; E1 sin demostrar lo que concluía; en el quiz, la más larga acierta 4 de 5, 8 pistas
con el criterio, 7 de 8 sobre el Nilo, Q4 sin retro, la retro de Q1 con la respuesta del E1.

---

## 1 · T5.1 · Nueve «Para practicar» (M1–M9)

Uno al final de cada módulo, justo antes de la lista de fuentes. Forma del capítulo 3:
`<div class="exercise">` con `.ejercicio-guiado` (enunciado, tres entregables con letras, pista,
solución con R y lectura por apartados). Ids `c4mN-pista` y `c4mN-sol`. Solo R.

**Series.** `grep -lw` de cada candidata en `Htmls_Series/*.html`: ninguna aparece (salvo `gold`, que no
se usa). Lo que dice cada enunciado de su serie sale de la ayuda de R leída en esta sesión
(`r5_ayuda_datasets.out`). Cada bloque corre solo (`r5_bloques_sueltos.out`, 35 de 35).

| Mód. | Serie | Por qué esa | Qué practica (hueco de §1.2) | Palabras del enunciado |
|---|---|---|---|---|
| M1 | `tcm1y` (tseries) | Sin tendencia; el AR(2) libre deja una raíz en 1.028 | Raíz unitaria estimada frente a impuesta, y lo que cambia en el pronóstico | 41 |
| M2 | Simulada, ARIMA(2,1,0), semilla 2026 | Con el modelo conocido se ve qué delata cada ajuste | Tres hallazgos, a qué etapa devuelve cada uno | 55 |
| M3 | Simulada, AR(1) + escalón, semilla 43 | `beaver2` no es un caso limpio (duda 1) | Decidir $d$ con las tres evidencias en una serie con escalón | 68 |
| M4 | Importaciones de Colombia, `global_economy` (tsibbledata) | ACF y PACF con una sola barra: la tabla no elige | Proponer candidatos, no uno | 48 |
| M5 | `log(airmiles)` | Deriva clara ($t = 4.47$), al revés que el Nilo | ¿Lleva deriva?; el M5 gana su actividad | 40 |
| M6 | GOOG 2018, `gafa_stock` (tsibbledata) | El mínimo de los 18 cae en $d = 2$ con $\hat\theta = -1$ | La trampa del AICc entre distintos $d$, mordiendo | 62 |
| M7 | `NelPlo[, "ip"]` (tseries) | Escalonada ≠ exhaustiva, por 6.1 puntos | Abrir la traza y explicar dónde paró | 29 |
| M8 | Simulada, AR(1) con $\phi = 0.8$, semilla 2026 | La firma solo aparece con parte AR suficiente | Firma de la sobrediferenciación y cuándo no salta | 34 |
| M9 | `BJsales.lead` | IMA(1,1): los $\psi$ salen a mano de la forma cerrada | Intervalo desde los $\psi$; forma con y sin deriva | 29 |

Cifras fuera de `#>`: M1 `[M1-01]`, `[M1-02]`; M2 `[M2-01]` a `[M2-03]`; M3 `[M3-01]`, `[M3-02]`;
M4 `[M4-01]` a `[M4-03]`; M5 `[M5-01]`; M6 `[M6-01]`; M7 `[M7-01]`; M8 `[M8-01]`, `[M8-02]`;
M9 `[M9-01]`.

**`BJsales.lead` (decisión pedida).** Se usa en el M9. Es otra serie (el indicador adelantado), no
aparece en el sitio y su IMA(1,1) es el caso más simple en que los $\psi$ se deducen a mano; el
enunciado dice que la ayuda la documenta junto a `BJsales`. Riesgo: que se confunda con la `BJsales`
de los ejercicios 1 y 3.

**Descartadas** (`r5_explora.out`): `beaver2` para M3 y M8 (duda 1); `austres` y
`aus_airpassengers` para el M6 (el $d = 2$ ganador no es degenerado: no hay respuesta limpia);
`NelPlo gnp.real` para el M4 (necesita deriva, que llega en el M5); `USeconomic rl` (ningún candidato
pasa Ljung–Box); Niño 3.4 para el E2 (hay que quitar la estacionalidad, que es del capítulo 5).

---

## 2 · T5.2 · Ejercicios 1 a 3

Los tres ganan entregables con letras (cuatro cada uno) y la discusión va por apartados.

### 2.1 · E1 (`BJsales`)

- El enunciado pide explícitamente comparar **el IMA(1,1) con el mejor modelo de $d = 2$**, donde el
  error sí lleva a elegir mal (17.489 puntos, bajo `#>`); desaparece «su AICc».
- La pista ya no da cifras ni rezagos.
- El bloque imprime las dos rejillas con la raíz MA de cada modelo.
- La discusión dice lo que se mide: el IMA es el 8.º de 9 por AICc (`[E1-01]`) y no pasa Ljung–Box;
  **criterio y diagnóstico coinciden sobre él**. La lección «un criterio de información no sustituye
  al diagnóstico» (c4-m10-65, intacta) se demuestra con el ARIMA(1,2,2): mejor AICc de $d = 2$, pasa
  Ljung–Box y su MA es $(1-B)(1-0.625B)$ (`[E1-02]`).

### 2.2 · E2 (`log(pelt$Hare)` en lugar de `log(lynx)`)

- Serie nueva: pieles de liebre de `tsibbledata::pelt`, 1845–1935. Mismas tres evidencias, y (c)
  pide las raíces MA de cuatro modelos para ver cuáles delatan la diferencia.
- La pista ya no da el criterio ni el modelo.
- **Las siete marcas del E2 antiguo se conservan** (§7): c4-m10-69 y -67 van en la discusión de la
  liebre, donde siguen siendo ciertas; las del lince (c4-m10-151, -66, -150, -68, -70) pasan a un
  párrafo final de la solución, «El mismo patrón en otra serie», con su bloque (`e2b`), que es
  además de donde salen ahora las cifras de `lynx` del M8 (58 %, 1.653 → 0.687, 0.565, 1.000).

### 2.3 · E3 (`BJsales`)

- (a) pide predecir $\psi_\infty$ con la forma cerrada antes de expandir; el bloque lo calcula primero.
- La pista (c4-m10-71) y c4-m10-72 no cambian.

### 2.4 · Las frases de M8 y M9 que los resolvían

| Dónde | Antes | Después |
|---|---|---|
| M8, final del aviso de la varianza (sin marca) | «(Es el ejercicio 2 de este capítulo.)» | «(El bloque que lo calcula está al final de la solución del ejercicio 2.)» |
| M9, nota del peso límite (sin marca) | «Sobre `BJsales` (ejercicio 3) el mismo tipo de modelo da $\psi_\infty = 2.99$: a doce pasos $\sigma_h$ ya es $1.96$ veces…» | «Cuando $\phi + \theta > 0$, $\psi_\infty$ es mayor que $1$ y cada choque acaba pesando más que cuando llegó: el ejercicio 3 lo mide sobre otra serie.» |

El aviso del M8 sobre `log(lynx)` (c4-m8-10, -11, -61) se queda: con el E2 en otra serie ya no lo
resuelve; es el ejemplo del módulo (duda 3).

---

## 3 · El quiz, ítem por ítem

Ocho preguntas, los cuatro tipos (el texto del M10, «Ocho preguntas de los cuatro tipos», cuadra).
Posición de la correcta: 2, 3, 2, 4, 3, 1; la múltiple, {1, 3, 4}.

| # | Mód. | Tipo | Antes | Ahora | Cifras |
|---|---|---|---|---|---|
| P1 | 6 | opción | AICc del Nilo, $d = 1$ frente a $d = 2$ | Lo mismo sobre los pasajeros aéreos de Australia; la retro ya no dice con qué decidir $d$ | `[P1-01]`–`[P1-03]` |
| P2 | 9 | numérica | $\sigma_2$ del Nilo, fórmula en la pista | $\sigma_3$ de un ARIMA(1,1,0) con $\phi = 0.5$, $\sigma = 2$: hay que obtener $\psi_2$; 5.02 ± 0.006 | `[P2-01]`–`[P2-03]` |
| P3 | 10 | gráfico | Puente al cap. 5 | El mismo gráfico; sin negrita en «mensual», pista nueva, opciones parejas | las del puente |
| P4 | 5 | múltiple | Sin retro; «Son tres»; dos opciones de memoria de funciones | Retro en las cinco; dos opciones sobre la forma del pronóstico | Nilo, M9 |
| P5 | 3 | opción | **Rehecha.** Recordar el experimento de KPSS | `beaver2`: qué hacer antes de fijar $d$ con un salto a la vista | `[P5-01]`–`[P5-03]` |
| P6 | 4 | gráfico | ACF del Nilo sin diferenciar | ACF de las exportaciones de Chile (`ACF_P6`) | `[P6-01]`, `[P6-02]` |
| P7 | 7 | opción | Siete modelos del Nilo a menos de 2 | Chile: escalonada ≠ exhaustiva, tres modelos a menos de 2 | `[P7-01]`–`[P7-03]` |
| P8 | 8 | opción (antes numérica) | **Rehecha.** Dividir $-1$ entre $-1$ | Importaciones de Perú: MA(1) sobre $\nabla y$ y $\nabla^2 y$; decidir $d$ | `[P8-01]`–`[P8-04]` |

Series: Australia, proceso teórico, AirPassengers (puente), —, castor, Chile, Chile, Perú. **Ninguna
sobre el Nilo** (la P4 lo cita en una retro). Ninguna cifra del quiz está en un «Para practicar» ni
en un ejercicio.

**Longitudes** (`r5_longitudes.out`, caracteres visibles; ✔ = correcta):

| Ítem | Antes | Después |
|---|---|---|
| P1 | 42 · 86✔ · 74 · 63 | 83 · 84✔ · 86 · 83 |
| P3 | 51 · 75 · 81✔ · 87 | 77 · 80 · 79✔ · 78 |
| P4 | 97✔ · 53✔ · 59 · 53✔ · 99 | 88✔ · 93 · 93✔ · 72✔ · 88 |
| P5 | 91✔ · 72 · 71 · 65 | 82 · 78✔ · 81 · 76 |
| P6 | 67 · 59 · 58 · 92✔ | 71 · 67 · 77 · 73✔ |
| P7 | 82 · 85 · 109✔ · 98 | 87 · 88 · 87✔ · 92 |
| P8 | (numérica) | 83✔ · 84 · 86 · 78 |

La más larga acertaba 4 de 5; ahora 0 de 6, y la más corta, 0 de 6. En la múltiple, ni las tres más
largas ni las tres más cortas son las correctas.

**Pistas:**

| # | Antes | Después |
|---|---|---|
| P1 | «pregúntate si están calculados sobre los mismos datos…» | «Mira de dónde sale un AICc: vuelve a su fórmula en el Módulo 6 y sigue qué cambia en ella al pasar de $d = 1$ a $d = 2$.» |
| P2 | La fórmula y «entran solo dos términos» | «…escríbelo primero sobre $y_t$, como en el desarrollo del Módulo 1, y cuenta cuántos pesos entran en $\sigma_3$. Conserva al menos tres decimales…» |
| P3 | «¿Tienen algo en común los números 12 y 24…?» | «No te quedes en cuántas barras salen de la banda: fíjate en cuáles son.» |
| P4 | «Son tres. Piensa en…» | «Para cada afirmación, piensa qué grado tiene la tendencia que genera la constante con ese $d$, y qué le pasa al pronóstico cuando la constante no está.» |
| P5 | El mecanismo de las sumas parciales | «Repasa en el Módulo 3 qué contrasta cada prueba y qué le pasó a cada una en el experimento del cambio de nivel.» |
| P6 | «¿Qué condición exige la tabla…?» | «Antes de contar barras, mira la forma en que bajan, y repasa el primer párrafo del Módulo 4.» |
| P7 | «Compara ese umbral con la distancia entre el primero y el séptimo» | «Mide primero cuánto separa el AICc a esos tres modelos, y busca en el Módulo 7 qué hace el capítulo con distancias de ese tamaño.» |
| P8 | «$B = -1/\theta$. Sustituye…» | «Los dos modelos pasan el diagnóstico de residuales, así que la respuesta no está ahí. Repasa qué más enseña a comprobar el Módulo 8.» |

**Tolerancia de la P2** (por HTTP, `r5_recorrido.out`): aciertan 5.02, 5,02, 5.025, 5.0249 y 5.024;
fallan 5.03, 5.01, 5.0, 5 y los siete tropiezos que nombra la retro (2.29, 3.46, 4.61, 4.12, 6.27,
2.51; 5.00 por redondear la raíz a 2.5).

---

## 4 · Las notas de la R4 que tocan el quiz

| Nota | Qué pedía | Qué se hizo |
|---|---|---|
| 7, 20 | La retro de la P1 negaba la parsimonia en la elección de $d$ | Retro nueva de esa opción: no diferenciar de más es una cautela razonable (Módulo 8), pero no sale de esa comparación |
| 10, 21 | «el umbral habitual de 2» | P7 y M9: «los 2 que este capítulo toma por convención» |
| 22 | «el algoritmo es consistente» | La frase desaparece |
| 23 | $n\beta^2/\hat\sigma^2_{LP}$ sin comprobar | Desaparece con la P5 antigua |
| 14 | «exactamente sobre el círculo unitario» | P8: «de módulo $1.000$ con tres decimales… en la práctica, $(1 - B)$» |
| 26 | «aplicarla aquí no informa de nada» | P6: «La tabla de identificación se lee sobre la serie ya estacionaria» |
| 27 | «decae geométricamente» | P6: «decae, de forma exponencial u oscilante (Capítulo 3)», como la tabla del cap. 3 |
| 6 | Regla de la varianza; KPSS por defecto | La P8 usa la varianza como distractor y su retro la desmiente; ya no hay ítem sobre `ndiffs()` |
| 9 | PACF de ∇Nilo en 7 y 10 | Ningún ítem lee ya esa PACF |
| 11, 18b | Umbral 1.01 / 1.001 | Ningún ítem del quiz lo menciona |
| 12, 15 | Constante; «prácticamente nunca se quiere» | P4: «el Módulo 5 explica por qué no conviene extrapolarla» |
| 2 | «la forma la deciden $d$ y la constante» sin $p$ | La P4 no lo afirma en general |
| 3, 4, 5, 13, 17, 19, 28 | Frases que no deben repetirse | No están en el quiz nuevo (28: la raíz 1.03 del Nilo desaparece con la P1 antigua) |
| 1, 8, 24, 25 | Simulacro | **[fuera del repo]**, §8 |

---

## 5 · Minutos

Convenio de la R3: lectura con pista y solución abiertas (columna «abierto» de `r3_minutos.py`).

| Módulo | Declarado antes | Medido antes | Medido ahora, cerrado | Medido ahora, abierto | Declarado ahora |
|---|---|---|---|---|---|
| M1 | 12 | 11.6 | 12.2 | 15.8 | **16** |
| M2 | 8 | 7.8 | 8.4 | 12.1 | **12** |
| M3 | 14 | 14.2 | 15.0 | 18.4 | **18** |
| M4 | 9 | 9.3 | 9.8 | 13.5 | **14** |
| M5 | 6 | 6.3 | 7.0 | 10.3 | **10** |
| M6 | 10 | 10.2 | 10.7 | 14.1 | **14** |
| M7 | 10 | 10.2 | 10.7 | 14.2 | **14** |
| M8 | 12 | 11.8 | 12.3 | 15.8 | **16** |
| M9 | 15 | 15.1 | 15.7 | 19.2 | **19** |
| M10 | 46 | 46.4 | 36.6 | 51.3 | **51** |

Distancia máxima 0.5 (M4). El capítulo crece unos 42 min de lectura con todo abierto (M1–M10: 142 →
184 declarados). La autoevaluación pasa de 18 a 23 min de lectura; el comentario de `courseData` lo dice.

---

## 6 · Verificación

| Qué | Resultado | Salida |
|---|---|---|
| `verifica_todo.py` | 11 en verde | `r5_verifica_todo.out` |
| Verificador de bloques | **1326 de 1326**, 0 discrepancias (antes 822); no hubo URLError | `r5_bloques_cap4.out` |
| Cada bloque solo, proceso nuevo, carpeta vacía | 35 de 35 (24 de R, 11 de Python) | `r5_bloques_sueltos.out` |
| `audita_citas.py` | OK, ningún F03 ni F09; 612 afirmaciones | dentro de `verifica_todo` |
| `data-afirma` | 262 elementos en las cuatro plantillas antes y después, mismo contenido byte a byte; mismo número de `<cite>` (lo afirma `r5_edita.py` al escribir) | `r5_edita.out` |
| `audita_posicion_correcta.py` | en verde (orden 232431; múltiple {1,3,4}) | `r5_posicion.out` |
| `cuenta_sitio.py` | al día (49 ejercicios) | dentro de `verifica_todo` |
| `ensambla_cap4.py` dos veces | mismo md5 (`51454d9b…`) | — |
| Caps. 5 y 6 | reensamblados; `git status` no los muestra | — |
| `r4_sin_literales.py` | 474 literales en 106 archivos, 0 hallados (no cubre `r5_*`, que solo llevan ayuda de R y texto propio) | — |
| `node --check chapter.js` | limpio | — |
| Por HTTP (puerto 8795, Chrome sin ventana en el 9288), 1200 y 375 px | M1–M10 sin errores de KaTeX, sin «$» sueltos, sin desborde, lienzos pintados; los 12 ejercicios con pista y solución a la vista y código coloreado; quiz hecho en cuatro pasadas (todo bien, fallo y acierto, dos fallos con el desglose de la múltiple, bordes de la numérica). Único evento: el 404 de `favicon.ico`. Servidor y Chrome cerrados | `r5_recorrido.out`, `.json`; capturas en `capturas/r5/` |

---

## 7 · Frases marcadas

**Ningún id cambió de texto, ninguno se añadió y ninguno se quitó.** Lo que cambió es dónde están siete:

| id | Antes | Ahora |
|---|---|---|
| c4-m10-61 | enunciado del E1 | igual |
| c4-m10-65 | discusión del E1 | discusión del E1, apartado (d) |
| c4-m10-69 | discusión del E2 (lince) | discusión del E2, (a), **dicha de la liebre** |
| c4-m10-67 | pista del E2 (lince) | discusión del E2, (b), **dicha de la liebre** |
| c4-m10-151, -66, -150 | enunciado del E2 | párrafo final de la solución del E2 («El mismo patrón en otra serie») |
| c4-m10-68 | pista del E2 | ese mismo párrafo final |
| c4-m10-70 | discusión del E2 | ese mismo párrafo final |
| c4-m10-71, -72 | pista y discusión del E3 | igual |

c4-m10-69 y c4-m10-67 son frases generales (un ciclo de longitud no fija vuelve a su media; en una
serie estacionaria la caída de la varianza repite $r_1$) cuya huella no cambia, pero **el contexto
sí**: la fuente de la -69 (FPP3 §9.1) se contrastó hablando del lince. Si el verificador prefiere,
basta moverlas al párrafo del lince. Frases marcadas que un ejercicio nuevo pone a prueba sin
tocarlas: c4-m1-65 y -08 (M1), c4-m2-10, -11 (M2), c4-m3-16, -17 (M3), c4-m4-14, -16 (M4),
c4-m5-05, -20 (M5), c4-m6-05, -06 (M6), c4-m7-13, -17 (M7), c4-m8-03, -61 (M8), c4-m9-12, -21
(M9). No vi ninguna contradicha.

Frases nuevas sin marca que quizá pidan registro (no añadí `data-afirma`): la descripción de cada
serie (ayuda de R, en `r5_ayuda_datasets.out`); «para un AR(1) diferenciado el valor teórico es
$-(1-\phi)/2$» (M8, cuenta propia comprobada con `ARMAacf`, `[M8-02]`); la forma cerrada del
IMA(1,1) (M9, cuenta propia comprobada contra `forecast()`).

---

## 8 · Lo que más dudas me deja (para el verificador) y lo que dejé

**Dudas, de más a menos:**

1. **`beaver2`.** El diagnóstico la daba por «limpia» para el escalón. No lo es: quitado el escalón,
   lo que queda tiene $r_1 = 0.78$, KPSS rechaza dentro de cada tramo y la comparación fuera de
   muestra cambia de signo según el corte (`r5_explora.out`). Por eso el M3 usa una serie simulada y
   `beaver2` solo aparece en la P5, que pregunta por el procedimiento y cuya retro dice que la duda
   sobre $d$ sigue abierta. La retro aplica KPSS a los residuales de una regresión (`[P5-03]`): los
   valores críticos no son exactamente los de la prueba.
2. **M3: probar por tramos.** El módulo no enseña a aplicar `ndiffs()` a cada lado del salto; lo
   introduce el ejercicio. Con 500 semillas, en el 35 % algún tramo pide $d = 1$ (`[M3-01]`): la
   semilla 43 se eligió porque reproduce el reparto del Nilo, y el texto da la frecuencia.
3. **La caja de `lynx` del M8 se queda.** El E2 ya no es sobre `lynx`, pero el patrón es el mismo y
   la caja enseña el método; lo considero exposición, no la respuesta. El plan decía «retirada o
   movida»: moverla exigía cambiar tres marcas (c4-m8-10, -11, -61).
4. **E2: el párrafo final del lince.** Existe para conservar cinco marcas y dar bloque a las cifras
   del M8; alarga la solución y vuelve a traer `lynx`, que es práctica del cap. 3.
5. **Tres series simuladas de nueve** (M2, M3, M8) y tres paquetes más allá de `forecast` y
   `tseries` (`tsibbledata` en M4, M6 y E2; el quiz cita `fpp3::aus_airpassengers` solo en cifras).
   El cap. 1 ya usa `library(fpp3)`.
6. **Semillas elegidas.** M3 (43) y M8 ($\phi = 0.8$ en vez de 0.6, para que $\hat\rho_1$ quedara
   lejos de $-0.5$); el M8 dice que la firma sale limpia en el 78 % de 200 semillas (`[M8-01]`).
7. **M7.** «De sus cinco modelos iniciales… después solo evaluó uno más» describe la traza
   impresa, no el código de `auto.arima`. `NelPlo`: la ayuda no dice país, unidades ni que esté en
   logaritmos, y el enunciado tampoco.
8. **M9 (c) y M5 (c)** terminan con un juicio («lo prudente es…», «la afirmación contra la que
   previene el módulo»): opinión, no cifra. En el M5, «no es exactamente la media… porque se estima
   a la vez que $\theta$» es explicación propia.
9. **P1.** En esa serie la duda sobre $d$ es real (KPSS 2; ADF y PP 1) y la retro lo dice; la opción
   de la parsimonia es «incorrecta» solo porque no sale de la comparación.
10. **P6 y P7 comparten serie** (Chile) y la P7 dice «esa misma serie».
11. **P8** deja de ser numérica: queda una sola numérica (P2).
12. **Pistas de P1, P6 y P8** remiten a un módulo concreto; pueden leerse como media respuesta.
13. **`ensambla_cap4.py`**: toqué la comprobación del número de ejercicios, fuera de lo autorizado
    a la letra.
14. **P4**, opción «se aplana en un nivel»: no recoge la salvedad de los ciclos (nota 2 de la R4);
    con raíces complejas también se aplana, oscilando antes.

**Lo que dejé:**

- **[fuera del repo]** Simulacro: «método de Holt» frente a «modelo» (notas 1 y 25), la nula de cada
  prueba en la P9 (nota 8), la columna de varianza de la P10 (nota 24, plan §7.1). Preparcial: S5,
  B10, «25.6 veces», ningún ítem del escalón.
- Los rótulos del selector del M9 (R3, pendiente): no es un ejercicio ni el quiz.
- El motor: «Resultado: 8 de 8 · impecable» tras acertar todo al segundo intento, junto a «Te
  costaron…» (`r5_recorrido.out`, pasada B).
- El gráfico de la P3 sigue siendo el del simulador del puente.
- Soluciones solo en R; ningún «Para practicar» en el M10.
- Sin atribuciones nuevas: ningún autor, año ni página en el texto añadido.
- Voz: enunciados, pistas y quiz en imperativo de segunda persona, como los del cap. 3; la lectura
  de las soluciones, impersonal.

---

## 9 · Guiones y salidas (`diagnostico/cap4/comprobaciones/`)

| Archivo | Qué es |
|---|---|
| `r5_edita.py` · `.out` | aplica la ronda sobre `b53fdcb`; importa los cuatro siguientes |
| `r5_ediciones_cortos.py`, `_m10.py`, `_quiz.py`, `_minutos.py` | el texto de cada tanda |
| `r5_reprex.R` | ejecuta un bloque y escribe cada salida bajo su línea, tras `#> ` |
| `r5_bloques/{m1…m9,e1,e2,e2b,e3}.R` y `.out` | el código de cada solución y su ejecución |
| `r5_cifras.R` · `.out` | cifras de prosa, pistas, retros y claves, con etiqueta |
| `r5_explora.R` · `.out` | exploración previa (series candidatas y descartadas; no es fuente de cifras) |
| `r5_ayuda_datasets.R` · `.out` | la ayuda de R de cada serie nombrada |
| `r5_longitudes.py` · `.out` | la prueba de la opción más larga y más corta, antes y después |
| `r5_posicion.out` | `audita_posicion_correcta.py` |
| `r5_minutos_antes.out` · `r5_minutos_despues.out` | `r3_minutos.py` antes y después |
| `r5_bloques_cap4.out` | el verificador de bloques |
| `r5_bloques_sueltos.py` · `.out` | cada bloque, solo |
| `r5_recorrido.js` · `.out` · `.json` | recorrido por HTTP a 1200 y 375 px y el quiz hecho a mano |
| `r5_verifica_todo.out` | la pasada completa |

---

## 10 · Correcciones tras la verificación (2026-11-23)

Tras `R5_verificacion_A.md` y `R5_verificacion_B.md`, con las decisiones de la sesión maestra. Todo
se aplicó en los guiones `r5_ediciones_*.py` (la ronda sigue siendo reejecutable desde `b53fdcb`).
**Lo que sigue sustituye a lo dicho arriba** donde difiera: la práctica del M9 (§1), el E3 (§2.3),
la frase del M8 (§2.4), la tolerancia de la P2 (§3) y los minutos (§5).

| Hallazgo | Qué se hizo |
|---|---|
| **A1** · M6, «caminata aleatoria» | Respuesta y (c): es una caminata **con deriva** escrita con una diferencia de más; el bloque `m6` imprime ahora la $\hat\sigma^2$ del ARIMA(0,1,0) sin constante (371.23) |
| **A2** · M3, «la semilla no es especial» | «La semilla está elegida para que salga el caso completo», con las frecuencias: 100 %, 65 %, 52 % (reparto del Nilo) y 33 % (`[M3-01]`, `[M3-03]`) |
| **A3** · M2, sin frecuencia | Frase al final de (c): 99.5 %, 65.5 % y 53 % los cinco rasgos a la vez (`[M2-04]`, 200 semillas) |
| **A4** · M9, «el ejercicio 3 lo mide» | Quitado |
| **A5 + A8 + B11** · el c4m9 duplicaba el E3 | **Práctica del M9 nueva**, sobre `austres` (residentes en Australia, en miles, 89 trimestres; no aparece en el sitio): tres modelos con el mismo MA(1) —ARIMA(0,1,1) sin deriva, con deriva y ARIMA(0,2,1)— y tres entregables: forma del pronóstico, de dónde sale cada pendiente (0; 52.11, la deriva; 43.23, el tramo final) y ancho del intervalo a 1 y 40 trimestres (402.0 frente a 2587.0). Bloque `m9`; `[M9-01]` a `[M9-03]`. `BJsales.lead` ya no se usa. Los $\psi$ quedan para el E3, y **el apartado (d) del E3 (la deriva) se quitó**, con su parte del bloque |
| **A6** · M8 (c), la regla que respondía E2 (c) | «Aquí, la raíz MA solo delató la diferencia sobrante en el modelo que tenía sitio para la parte AR.» |
| **A7** · el paréntesis del M8 | El bloque `e2b` pasa a un `<pre>` justo después del aviso «La columna de la varianza no decide $d$» del M8, y el paréntesis dice «(El bloque de abajo lo calcula.)». El párrafo del lince del E2 conserva sus marcas y remite a ese bloque |
| **A9** · M4, «¿cuál corta y cuál decae?» | «¿corta alguna?, ¿decae alguna?» |
| **A10** · pista del M1 | «Para (b), una vez ajustado el ARIMA(1,1,0), no hace falta nada más» |
| **A11** · `NelPlo ip` sin unidades | El enunciado dice que va «en la escala que trae el paquete (la ayuda no da unidades; sus valores van de −0.105 a 5.229)» (`[M7-02]`) |
| **A12** · M7, $q = 3, 4$ sin imprimir | El bloque `m7` imprime los seis ARIMA(0,1,q) con deriva |
| **A13** · coma suelta a 375 px | Desaparece con el M9 nuevo |
| **B1** · P5, «KPSS deja de rechazar» | Retro de la correcta rehecha: lo que queda tiene $r_1 = 0.78$ y, en cada tramo, las tres pruebas siguen pidiendo una diferencia (`[P5-04]`). Además, en la retro de la cuarta opción «El salto explica que KPSS rechace» → «puede bastar para que KPSS rechace» (por la misma razón; no lo pedía nadie) |
| **B2** · pista del E2 | La redacción de la sesión maestra; el M3 dice de la varianza que «no decide $d$» (c4-m3-60), así que la pista remite al M3 |
| **B3** · c4-m10-69 | Opción (b): la marca vuelve, intacta, al párrafo del lince; el apartado (a) de la liebre dice solo «según las tres, la serie es estacionaria» |
| **B4** · E1, doble redondeo | $-0.641$ (e.e. $0.103$) (`[E1-03]`) |
| **B5** · tolerancia de la P2 | 0.011. Por HTTP: aciertan 5.02, 5,02, 5.025, 5.0249, 5.026, 5.03 y 5.01; fallan 5.04, 5.0, 5 y los tropiezos (2.29, 3.46, 4.61, 4.12, 6.27, 2.51, 12.62) |
| **B6** · `<U+00BF>` | `r5_reprex.R` fija el locale y escribe en UTF-8; los 13 bloques se volvieron a pasar; 0 apariciones de «U+00» en la página |
| **B7** · E2 frente a la caja del lince | Sin cambio (decisión de la maestra: transferencia) |
| **B8** · pistas del E3 y la P2 | E3: «Los $\psi$ salen de la forma cerrada del Módulo 9, o de expandir…: las dos vías dan lo mismo» (la frase estaba fuera de c4-m10-71, que no cambia). P2: «Para los pesos $\psi$, escribe primero el modelo sobre $y_t$…» |
| **B9** · «empeora el AICc» | Desaparece con el apartado (d) del E3 |
| **B10** · pistas de P6, P8 y E1 (d) | Las tres, con la redacción propuesta |
| **B12, B13** · notas del registro | Sin tocar (son de la maestra). Para la -150: **el AR(2) de `log(lynx)` no se imprime en ningún bloque del capítulo 4**; el bloque `e2b` (ahora en el M8) ajusta solo el ARIMA(2,1,1). Sigue donde decía el verificador B (`r4_software/lectorF/sigma2_y_lince.R`) |
| **B14** · P1 | «el mejor ARIMA sin constante de la rejilla» |
| **B15** · P7 | «el mejor según el AICc de los que la búsqueda pudo ajustar» |
| **B16** · P8 | «Un MA(1) sin media ajustado a…» |
| **B17** · E2 (d) | «la búsqueda exhaustiva de `auto.arima`» |
| **B18** · retro de la P2 | Quitada la frase de la caminata |

**Minutos tras las correcciones** (medido abierto → declarado): M1 15.9 → 16 · M2 12.4 → 12 ·
M3 18.6 → 19 · M4 13.5 → 14 · M5 10.3 → 10 · M6 14.2 → 14 · M7 14.3 → 14 · M8 17.8 → 18 ·
M9 19.6 → 20 · M10 49.2 → 49. Distancia máxima 0.5. Quiz: 22.8 min.

**Verificación tras las correcciones:** `verifica_todo.py`, 11 en verde (incluye `audita_citas`,
`cuenta_sitio` con 49 ejercicios y la posición: 232431, múltiple {1,3,4}); bloques **1347 de 1347**,
0 discrepancias; 35 de 35 bloques corren solos; `ensambla_cap4.py` dos veces, mismo md5
(`ba810788…`); caps. 5 y 6 sin diff; longitudes: la más larga y la más corta aciertan 0 de 6.
`r5_afirma.py` (nuevo; `.out`): 286 = 286 `data-afirma` (262 en `<span>`, 24 en otros elementos),
ningún contenido cambia, 252 = 252 `<cite>` idénticos; respecto de `b53fdcb` solo cambia de sitio
en el orden de la página la c4-m10-67 (las demás del E2 vuelven a ir juntas). Por HTTP (8795, CDP
9288), 1200 y 375 px: M1–M10 sin errores de KaTeX, sin «$» sueltos ni desborde, los 12 ejercicios
con sus paneles, quiz en cuatro pasadas; único evento, el 404 del favicon. Una primera pasada se
cortó en una captura (`Page.captureScreenshot sin respuesta`); la segunda terminó. Servidor y Chrome
cerrados.

**Dudas nuevas:** (1) el M9 nuevo ajusta a `austres` dos modelos con $d = 1$ que no pasan
Ljung–Box (lo dice); es un ejercicio sobre la forma, no sobre la elección. Su ayuda fecha la serie de
marzo de 1971 a marzo de 1994 y su `tsp` va de 1971 T2 a 1993 T2: el enunciado solo dice «desde
1971». (2) «con $d = 2$ la pendiente sale del tramo final de la serie» se apoya en una sola
comparación (43.23 frente a 46.19 de las ocho últimas diferencias y 52.21 de todas). (3) La P2
acepta ahora 5.01. (4) c4-m10-67 se queda en el apartado de la liebre (B13 es de la maestra).
(5) El `<pre>` del M8 va suelto, sin pestañas R/Python ni botón de copiar.

---

## 11 · Qué hizo la sesión maestra (2026-11-23)

**Decisiones sobre los hallazgos de la primera lectura** (las dos verificaciones están en
`R5_verificacion_A.md` y `R5_verificacion_B.md`):

- **B3 → opción (b)**: c4-m10-69 volvió al párrafo del lince. **B7**: el E2 frente a la caja del lince
  del M8 se acepta como transferencia (con B2, A6 y A7); queda para Javier.
- **A5 + A8 + B11**: el «Para practicar» del M9 pasa a practicar la **forma** del pronóstico sobre
  `austres`. Los ψ y el intervalo se quedan para el E3, que pierde su apartado (d), y B9 desaparece.

**Lo que hizo la maestra:**

- **c4-m10-69, retirada.** Devuelta al párrafo del lince, quedaba inmediatamente detrás de c4-m10-68,
  que dice lo mismo con la misma cita (FPP3 §9.1). La página dice ahora «las tres pruebas piden
  $d = 0$: la serie es estacionaria.»
  - La entrada pasa de `entradas` a `fuera` en `r4_entradas.json`, con su motivo, y la columna `r4`
    del inventario dice «retirada en la R5 (repetía c4-m10-68)».
  - Lo hace `r5_registro_maestra.py`, que es idempotente.
  - `r5_edita.py` admite esa única marca retirada, con su `<cite>`.
  - Quedan 285 entradas, 261 `data-afirma` en `<span>` y 251 `<cite>`; ninguna otra marca cambia
    de texto (`r5_afirma.py`).
- **Notas rehechas de c4-m10-65, -67 y -150** (B12 y B13, en `r5_registro_maestra.py`). Al cambiar la
  nota, `r4_registro.py` retiró su firma, y el verificador B de la R5, que no redactó las notas, las
  volvió a firmar tras leer el pasaje en la caché (`v5_firmas_B.txt`). `r4_firmas.py` tiene un lote
  `R5B` e ignora las firmas viejas de entradas retiradas. Hay 283 entradas firmadas de 285; las dos sin
  firma son los pendientes de KPSS.
- **Segunda lectura.** A da la ronda por aceptable (§«Segunda lectura» de su informe) y B, por
  correcta. Sus tres hallazgos menores se aplicaron en los guiones de edición, no en las plantillas,
  para que `r5_edita.py` los reproduzca:
  - A14: Ljung–Box(20) en el M9; C pasa con $p = 0.07$.
  - A15: la pendiente de C como suavizamiento exponencial de las diferencias, con
    $\alpha = 0.408$; las ocho últimas pesan el $98.5\,\%$, con su `#>`.
  - B19: «Las cifras de las pruebas, de la varianza, de $r_1$ y del ARIMA($2,1,1$) son las del
    bloque…».
- `r5_edita.py`, corrido de nuevo desde la base, reproduce las plantillas byte a byte salvo esos tres
  cambios.

**Comprobaciones finales:**

| Comprobación | Resultado |
|---|---|
| `verifica_todo.py` | 11 en verde (`r5_maestra_verifica_todo.out`) |
| Verificador de bloques | 1348/1348 (`r5_maestra_bloques.out`) |
| `audita_citas.py` | OK |
| Ensamblado | dos veces el mismo md5; caps. 5 y 6 sin diff |
| Minutos | declarados = medidos (≤ 0.5) |
| HTTP a 1200 y 375 px (`r5_revisa.js`) | sin errores de consola ni de KaTeX; 0 citas vacías y 0 enlaces rotos |

Ningún literal de cita de los caps. 2–4 está en los archivos de la ronda. La única coincidencia está en
`r5_ayuda_datasets.out`, que guarda la ayuda de R, no un libro; el cap. 3 versionó el mismo tipo de
archivo.

**Queda para Javier:** B7 (el E2 frente a la caja del lince del M8) y, como en el cap. 3, el motor que
cuenta como acierto el segundo intento. Fuera del repo: el simulacro (notas 1, 8, 24 y 25 de la R4) y
el preparcial.
