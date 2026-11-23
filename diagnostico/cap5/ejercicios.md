# Cap. 5 · Diagnóstico de ejercicios, autoevaluación y práctica

Archivo: `Htmls_Series/capitulo-5-sarima.html` (commit `f807b40`, worktree
`course-content-improvement-227f2c`, 2026-11-23). Diagnóstico, sin ediciones en el repo. Las líneas
citadas son las del HTML ensamblado; el capítulo se ensambla desde `ensamblado/cap5/` y cualquier
arreglo va allí. Fuera de esta lente: la prosa expositiva, las fuentes y el diseño de las gráficas.

Leído: objetivos de los doce módulos (3069, 3251, 3767, 4225, 4520, 4635, 4805, 5088, 5292, 5490, 5701,
6208), las consignas de los 14 simuladores de M1–M11, el quiz (`AUTOEVALUACIONES['cap5']`, 9365–9564), su
motor (7501–7850), los tres ejercicios (5911, 5988, 6063), la nota del Excel (6155–6169), los dos libros
de Excel (leídos con openpyxl, sin recalcular), `TABLAS_RANKING['comparativa']` (9339) y el simulacro
(`SIMULACROS['cap5-simulacro']`, 9974; motor 9600–9880).

Escala de veredictos (la de los caps. 2–4): **sirve** (publicable con retoques) · **se puede mejorar**
(núcleo sano, arreglos puntuales) · **hay que rehacer** (no mide lo que dice, se responde sin entender, o
enseña algo incorrecto).

**Lo que se marca aparte.** El simulacro del M12 lo escribe `exporta_simulacro.py` desde un banco fuera del
repo (fuente ensamblada: `ensamblado/cap5/simulacro.js`) y es la variante de un quiz de Brightspace ya
aplicado: sus hallazgos van marcados **[fuera del repo]** y son decisión de Javier.

Guiones y salidas (todo en `diagnostico/cap5/diag/`, prefijo `ejercicios_`):

| Guion | Qué hace | Salida |
|---|---|---|
| `ejercicios_carga.py` | palabras de prosa, código, simuladores y duración por módulo; primera tarea; consignas | `ejercicios_carga.out` |
| `ejercicios_vuelca.js` | evalúa el quiz y el simulacro del HTML y los vuelca con texto visible, clave, pista, retro, tolerancia y rutas | `ejercicios_vuelca.json` |
| `ejercicios_longitud_opciones.js` | posición, «la más larga / la más corta», pistas, retros ausentes, tolerancias con la comparación exacta de cada motor | `ejercicios_longitud_opciones.out` |
| `ejercicios_cap5.R` | reproduce E1–E3, recalcula las 8 claves del quiz (Q8 con los 61 orígenes) y las 6 claves numéricas del simulacro | `ejercicios_cap5.out` |
| `ejercicios_comprueba.R` | Q7 con Semana Santa, el SARIMA + calendario del M11, más decimales de la TRM, variantes del simulacro | `ejercicios_comprueba.out`, `ejercicios_variantes.json` |
| `ejercicios_simulacro_figuras.py` | lee los valores dibujados en los SVG de S8 y S9 | `ejercicios_simulacro_figuras.out` |
| `ejercicios_en_pantalla.py` | busca en M1–M11, antes del quiz, las cifras y frases que responden cada ítem y cada ejercicio | `ejercicios_en_pantalla.out` |
| `ejercicios_cobertura.py` | reparto por módulo del quiz y del simulacro; series nombradas | `ejercicios_cobertura.out` |
| `ejercicios_excel.py` | compara los dos libros celda a celda: qué se pide, cómo se instruye, qué se comprueba | `ejercicios_excel.out` |
| `ejercicios_series_candidatas.R`, `ejercicios_series_barrido.R`, `ejercicios_series_barrido2.R` | series estacionales candidatas (§7) y barrido de 211 + 235 series mensuales | `ejercicios_series_candidatas.out`, `ejercicios_series_barrido.out`, `ejercicios_series_barrido2.out` |
| — | `grep` de las candidatas en `Htmls_Series/*.html` | `ejercicios_series_grep.out` |

Versiones: R 4.6.0, forecast 9.0.2, tseries 0.10.62, fpp3 1.0.3. co2, USAccDeaths y AirPassengers de
`datasets` coinciden con `precalculo/salidas/datos_series.json`; la TRM (n = 138) se lee de ese JSON.

---

## 0. Resultado de las ejecuciones

### 0.1 Soluciones de los ejercicios (`ejercicios_cap5.out`, `ejercicios_comprueba.out`)

| Ej. | Cifra escrita | Salida real | ¿Coincide? |
|---|---|---|---|
| 1 | varianzas 223.9877 · 1.4555 · 0.3882 · 0.1543; nsdiffs 1, ndiffs tras D 1 | idénticas | sí |
| 1 | 47 de 48 convergen; mejor AICc (0,1,3)(0,1,1)₁₂ 176.9982 (n 455, LB 0.631); mejor BIC el airline; diferencia 1.211 | idénticas | sí |
| 1 | sin D: AICc 988.100 (n 467), LB p ≈ 0; con D: 178.209 (n 455) | idénticas (LB 0.0000000) | sí |
| 2 | (a) d 0, D 1; (b) D 1, d 1; diferencia máxima 0; LB 0.0000 / 0.2477; AICc 905.963 (60) / 857.316 (59); auto.arima airline; −0.4303, −0.5528; seas 1, ocsb 0 | idénticas (LB de (a): 0.000050) | sí |
| 3a | nsdiffs 0 y 0; r12 −0.0024, r24 −0.0672, r36 0.0714, banda 0.1675; Φ 0.0013, ee 0.0899, **t 0.0147**; AICc 1708.001 / 1705.941; auto.arima (0,1,0) | r12 = **−0.0024532** (redondeado a cuatro: **−0.0025**); t = **0.0146251**; el resto idéntico | casi: dos salidas `#>` no son lo que imprime R 4.6 |
| 3b | K = 1…6: AICc 435.509 · 268.475 · 223.402 · 180.200 · 181.494 · 183.624; LB; airline 178.209 (n 455), LB 0.4081 | idénticas | sí |

**Todas las cifras se reproducen**, salvo dos salidas impresas del E3(a): `round(r12, 4)` da −0.0025 (no
−0.0024; la tabla del M8 y la retro de Q1 sí dicen −0.0025) y el t del SAR forzado es 0.0146 (no 0.0147).
Cosmético. **El problema del E3 no son las cifras sino lo que la solución dice de ellas** (§3).

### 0.2 Claves

| Instrumento | Resultado |
|---|---|
| Quiz `cap5`, 8 preguntas | **las 8 claves son correctas**. Q1: TRM en niveles r1 0.9637, r12 0.6365 (0.63649), r36 0.2252, banda 0.1668; ∇TRM −0.00245, −0.06721, 0.07138. Q2: el polinomio toca 1, 12 y 13; ρ2 teórica 0.3637 (≠ 0) → a, b, d. Q3: 96 − 1 − 12 = 83. Q4: ndiffs 0 → 1, θ̂ −0.4303. Q5: ACF 0.700 / 0.490 / 0.343, cero en 11 y 13. Q6: armónica K = 6 AICc −521.4512 (n 143, 16 coeficientes), airline −483.2101 (n 131). Q7: con log(días) **y Semana Santa**, β̂ 1.0840, ee 0.4462, t(β = 1) 0.1882 (0.188256 con las cifras redondeadas del enunciado). Q8: partición única ETS-log 19.429, armónica 19.505 (primera por MAE 14.690 y MAPE 3.151), SARIMA 43.184 (cuarto, empatado con auto.arima, que elige el mismo modelo; el SARIMA + calendario da 45.477); 61 orígenes: SARIMA 16.812, armónica 22.385 (cuarta); el SARIMA gana a cada rival en 85.2–91.8 % de los orígenes (90.2 % a la armónica) |
| Simulacro M12, 12 preguntas **[fuera del repo]** | **las 12 claves son correctas**. Numéricas desde el enunciado: N2 −0.047393; N4 0.158046; N5 18.3720; N6 0.135695 (los ψ del enunciado coinciden con la expansión); N7 561.0685; N10 2.803110. Selección: S1 y S3 desde su tabla; S8 desde las barras del SVG (ACF corta tras 1, −0.5; en 12/24/36 −0.648, 0.378, −0.167; PACF 12 −0.492, 24 0.039 → (0,1,1)(1,1,0)₁₂); S9 desde el SVG (ninguna barra fuera de ±0.16; desviación por tercios 0.582 · 0.706 · 1.447); S11 menor AICc dentro de D = 0 en K = 5; S12 menor RMSE medio en ETS |

### 0.3 Otras comprobaciones medidas

| Qué | Resultado |
|---|---|
| E1: puesto del airline por AICc entre los 47 | 4.º, a 1.211 del mejor; **6** modelos a menos de 2; **26 de 47** no pasan LB(24) al 5 % |
| E1: la «trampa» de D | AICc sin D 988.100 frente a 178.209: la lectura ingenua elige bien (la propia solución lo admite) |
| E3(b): ¿qué elige la lectura ingenua? | **el airline** (178.209 < 180.200, diferencia 1.991), no el armónico; y el airline gana también por la comparación legítima (LB 0.4081 frente a ≤ 0.0516) |
| Q6: K del ítem | el enunciado usa −521.2 (K = 5, 15 parámetros en la tabla del M10, l. 5561) y la opción c dice «16 parámetros» (K = 6, AICc −521.45) |
| Simulacro S9: «2.4 veces» en la retro | el dibujo da 1.447 / 0.582 = 2.49 (medido sobre el SVG, con coordenadas redondeadas a 0.1 px) |

---

## 1. Cobertura: objetivo × dónde se practica, y cuánto se lee sin hacer nada

### 1.1 La primera tarea llega al final del M11

`ejercicios_carga.out`:

| Mód. | Palabras de prosa | Líneas de código | Simuladores | Duración declarada |
|---|---|---|---|---|
| M1 | 628 | 62 | 1 | 14 min |
| M2 | 1795 | 163 | 2 | 12 |
| M3 | 1321 | 173 | 3 | 16 |
| M4 | 1046 | 55 | 1 | 16 |
| M5 | 539 | 0 | 1 | 14 |
| M6 | 501 | 70 | 1 | 16 |
| M7 | 1022 | 98 | 1 | 21 |
| M8 | 551 | 91 | 1 | 16 |
| M9 | 594 | 86 | 1 | 14 |
| M10 | 645 | 81 | 1 | 16 |
| M11 | 2331 (con quiz y ejercicios) | 144 | 1 | 20 |

- **La primera tarea con respuesta comprobable es el quiz, en la línea 5895**, dentro del M11, después del
  panorama comparativo y del resumen. Los tres ejercicios van detrás (5911, 5988, 6063) y el Excel se
  anuncia después de ellos (6155).
- Antes de esa tarea hay **9912 palabras** de prosa (8642 en M1–M10 y 1270 del M11 hasta el quiz): **50 min
  a 200 palabras por minuto, 66 a 150**, sin contar 879 líneas de código ni 13 simuladores. Con la duración
  que el propio capítulo declara, **155 min (M1–M10)** más la mayor parte de los 20 del M11.
- **El capítulo no tiene ningún «Para practicar»** (0), frente a los 9 del capítulo 4 que acaba de fijar la
  forma. Ningún módulo de M1 a M10 tiene una tarea con respuesta dentro de él.
- Lo único que pide algo antes son las consignas de los simuladores, y **ninguna recoge respuesta; casi
  todas dicen el resultado en la misma frase**: «las bandas verticales desaparecen y la ACF se queda con dos
  barras» (M1, 3105); «con solo la diferencia regular baja de 0.762 a… 0.841, es decir sube» (M3, 4036);
  «cuando sobra una diferencia, Θ̂ se pega a −1» (M3, 4083); «verás picos limpios en 12, 24, 36» (M4,
  4301); «fíjate en que el mínimo de AICc y el de BIC coinciden aquí» (M6, 4664); «hasta K = 4 los
  residuales conservan estructura… hace falta llegar a K = 5» (M10, 5536). La única que pide una predicción
  antes de leer —«apunta cuál dirías que es el mejor método» (M11, 5729)— no la recoge.
- Las «dos formas de seguir a mano» del M2 (la heladería, 3280) y del M3 (la tienda, 3818) son ejemplos
  resueltos, no tareas: dan la cuenta y el resultado.

### 1.2 Objetivo × práctica

Reparto por etiqueta (`ejercicios_cobertura.out`): quiz M1 1 · M2 2 · M3 1 · M4 1 · M6 1 · M9 1 · M11 1 ·
**M5, M7, M8, M10: 0** (Q6 lleva la etiqueta 6 pero su retro dice «Es la lección central del Módulo 10» y
sus cifras son las de la tabla del M10).

| Mód. | Objetivo (resumen) | Quiz `cap5` | Ejercicio | Excel | Práctica real dentro del capítulo |
|---|---|---|---|---|---|
| M1 | la firma en m, 2m, 3m, y no verla cuando no está | Q1 (la fila TRM de la tabla del M1) | E3(a) | hoja M1 | Q1, que es recuerdo; **ver la firma en una serie nueva: NADA** |
| M2 | leer y escribir el SARIMA; el producto; momentos | Q2 (el mismo modelo y los mismos φ, Φ del módulo), Q3 | — | hoja M2 (la heladería) | Q3 es la única cuenta con un número nuevo |
| M3 | decidir D y d; el orden importa | Q4 (el caso del M8) | E1, E2 | hoja M3 (la tienda) | E2, con la respuesta impresa en el M8 (§3) |
| M4 | P y Q en m, 2m, 3m; satélites | Q5 (el SAR(1) del módulo) | E1 («identifica») | hoja M4 | **Identificar sobre un correlograma muestral nuevo: solo E1** |
| M5 | por qué el airline; σₕ a escalones | — | — | hoja M5 (2 fórmulas) | **NADA en el capítulo**; solo el Excel y el N6 del simulacro |
| M6 | rejilla sin comparar entre D; LB con 2m | Q6 (las cifras del M10) | E1, E3(b) | hoja M6 | E1 y E3(b), **y en los dos la trampa no muerde** (§3) |
| M7 | el ciclo completo, de la transformación al pronóstico | — | E1 (sin log ni pronóstico) | hoja M7 | **Transformación y pronóstico (bandas, exp → mediana): NADA**; solo Excel y N7 del simulacro |
| M8 | repetir donde las pruebas engañan; descartar estación | (Q4, etiqueta M3) | E2, E3(a) | hoja M8 | E2 y E3(a) son las dos series del módulo, resueltas en él |
| M9 | calendario como regresor | Q7 (la cuenta está en 5363) | — | hoja M9 | Q7: una resta y una división |
| M10 | dónde deja de servir el SARIMA: Fourier, STL | (Q6, etiqueta M6) | E3(b) | hoja M10 | E3(b), sobre co2 (m = 12): **m grande: NADA** |
| M11 | una partición no decide | Q8 (la tabla de arriba) | — | hoja M11 | Q8, recuerdo |

**Módulos sin ninguna práctica en el capítulo: M5.** M7 y M10 solo de refilón: nadie transforma ni
pronostica, y nadie trabaja con m grande. **Ningún módulo tiene práctica dentro de él** (0 «Para
practicar»).

---

## 2. Fichas del quiz (`AUTOEVALUACIONES['cap5']`, 9365–9564)

**Motor** (7501–7850; el mismo del cap. 4). En `opcion` y `grafico` el primer fallo deshabilita la opción,
muestra la pista y deja reintentar; el segundo marca la correcta y muestra la `retro` de la elegida. En
`multiple`, el primer fallo dice «De las N que marcaste, X están en la respuesta, y te faltan Y» más la pista
(7800–7803); el segundo, el desglose por opción. La numérica acepta `Math.abs(dada − respuesta) <=
tolerancia` (7721). **El «Resultado: X de 8» suma los aciertos al segundo intento** (`alPrimero +
alSegundo`, 7597).

**Claves: las ocho son correctas** (§0.2). Retros: **24 de 24** opciones con la suya; la promesa de 5897–5898
se cumple.

Las formas de contestarse solo (`ejercicios_longitud_opciones.out`, `ejercicios_en_pantalla.out`):

- **(a) Posición** — sana: 4 1 3 2 1 en las cinco de una sola (1→2, 2→1, 3→1, 4→1).
- **(b) Tamaño** — **la más larga acierta 5 de 5**: Q1 (129 frente a 70–79), Q4 (94 frente a 53–70), Q5
  (75 frente a 56–64), Q6 (106 frente a 67–76), Q8 (136 frente a 63–74). La correcta mide entre 1.24 y 1.96
  veces la media de las otras. La múltiple (Q2) no cae: ni las tres más largas ni las tres más cortas
  aciertan.
- **(c) Pistas** — **las ocho dan el criterio o la fórmula**: Q1 «Fíjate en qué vale ρ̂1… y en qué le pasa a
  la ACF de cualquier serie con tendencia»; Q2 «Expande… y cuenta… cuántos de ellos se estiman» (las opciones
  a, b y d, una por una); Q3 «la estacional cuesta D × m, no D»; Q4 «Los operadores conmutan. Piensa qué
  cambia entre las dos llamadas»; Q5 «Mira si los picos decaen o se cortan»; Q6 «pregúntate sobre cuántas
  observaciones se ha evaluado la verosimilitud»; Q7 «el valor bajo la hipótesis nula es 1»; Q8 «cuántos
  números independientes hay detrás». Q2 no anuncia cuántas son, pero con 3 correctas de 4 y el «te falta 1»
  del motor el segundo intento es casi gratuito.
- **(d) Respuestas en pantalla — 8 de 8**: Q1 es la fila «TRM (niveles)» de la tabla del M1 (3144) y su
  advertencia (3153: «la TRM tiene ρ̂12 = 0.636 y no tiene ninguna estacionalidad»); Q2 usa el mismo modelo y
  los mismos φ = 0.6, Φ = 0.7 que el M2, que dice «AR(13) con dos parámetros libres» (3351, 3508) y da ρ2 ≠ 0;
  Q3 aplica la regla de 4647 («cada D cuesta m observaciones»); Q4 es el recuadro del M8 (5100–5106); Q5 son
  las cifras de 4249–4250 («0.700 en el rezago 12, 0.490 en el 24 y 0.343 en el 36»), que la correcta
  repite; Q6 es la tabla del M10 (5561) y la advertencia de 5566–5570 («concluir que la regresión armónica con
  K = 5 lo supera por 38 puntos» es el distractor a); **Q7 está hecho en 5363**: «t = (1.084 − 1)/0.446 =
  0.19», y la tolerancia acepta 0.19; Q8 es la tabla del M11 (5744–5783), justo encima del quiz.
- **(e) Retros que filtran los ejercicios** — el quiz va antes que los ejercicios y cuatro retros los
  responden: Q1 (retro de b: «nsdiffs() devuelve 0 con las dos pruebas»; retro de d: «sobre ∇TRM los tres
  múltiplos de 12 valen −0.0025, −0.067 y 0.071, todos dentro de la banda») son dos de las tres evidencias
  del E3(a); Q3 (retroAcierto: «por eso el AICc de un modelo con D = 1 no se puede comparar con el de uno con
  D = 0») es la última parte del E1; Q4 (retros de a, c y d: los operadores conmutan con «diferencia máxima
  medida 0», «el modelo final es (0,1,1)(0,1,1)₁₂», θ̂ = −0.4303) es el E2 entero; Q6 (retros de b y d:
  «entre familias solo se puede comparar fuera de muestra», «el diagnóstico sí es comparable entre familias»)
  es el E3(b).
- **Recuerdo, no transferencia**: Q1 y Q4 nombran series del propio capítulo (TRM, USAccDeaths); Q5, Q6, Q7
  y Q8 dan cifras o procesos del capítulo sin nombrarlos. Solo Q3 pide aplicar una regla a un número nuevo.
- **Tolerancias**: no castigan el redondeo. Q3 (83 ± 0.5) acepta solo 83 y rechaza 94 y 84, que la
  retroFallo nombra. Q7 (0.1883 ± 0.005) acepta 0.188, 0.19, 0.185 y 0.1926; rechaza 0.18, el t contra 0
  (2.4294) y el signo cambiado. Para una cifra que se pide «con cuatro decimales», ±0.005 deja pasar dos
  decimales: no es un error, pero el enunciado pide más de lo que se exige.

| # | Línea | Tipo · etiqueta | Nivel | Veredicto |
|---|---|---|---|---|
| Q1 | 9367 | opción · M1 | recordar la tabla del M1 | se puede mejorar |
| Q2 | 9395 | múltiple · M2 | recordar el desarrollo del M2 (mismo modelo) | se puede mejorar |
| Q3 | 9423 | numérica · M2 | aplicar una regla (dada en la pista) | sirve |
| Q4 | 9434 | opción · M3 | recordar el recuadro del M8 | **hay que rehacer** |
| Q5 | 9462 | gráfico · M4 | recordar las cifras de 4249 | se puede mejorar |
| Q6 | 9498 | opción · M6 | recordar la advertencia del M10 | se puede mejorar |
| Q7 | 9526 | numérica · M9 | sustituir; la cuenta está en 5363 | **hay que rehacer** |
| Q8 | 9537 | opción · M11 | recordar la tabla de arriba | se puede mejorar |

**Q1 · ρ̂12 de la TRM en niveles.** Buen distractor c (la banda está bien). Pero es la fila de la tabla del
M1 con su advertencia, la correcta es la más larga (129 frente a ≤ 79) y la pista dice el criterio. Las
retros de b y d responden el E3(a). *Mejora*: una serie mensual nueva sin estación —`Seatbelts[, "PetrolPrice"]`
(§7: ρ̂12 en niveles 0.498 > banda 0.142, en ∇ todo dentro, nsdiffs 0 y 0)— y opciones de longitud pareja.

**Q2 · SARIMA(1,0,0)(1,0,0)₁₂.** Clave a, b, d correcta (ρ2 teórica 0.3637). Es el modelo del M2 con sus
mismos parámetros, y las tres correctas repiten frases del módulo. *Mejora*: otro producto —p. ej.
(0,0,1)(1,0,0)₁₂ o (1,0,0)(0,0,1)₁₂— donde haya que expandir de verdad, y una correcta que no se lea en el
texto.

**Q3 · n efectivo tras dos diferencias.** El único ítem de aplicación: número nuevo, retroFallo que nombra
los dos errores (94 y 84). La pista da la regla, pero el cálculo sigue siendo del estudiante. *Retoque*: que
la pista pregunte cuántos datos se pierden al restar «la celda de arriba» en vez de dar D × m.

**Q4 · ndiffs 0 → 1 en USAccDeaths.** Es el recuadro del M8 (5100–5106), con la serie del módulo; la
correcta es la más larga; la pista elimina b («los operadores conmutan»); y tres de sus cuatro retros
responden el E2. *Rehacer*: la trampa del orden con una serie nueva. Ninguna de 420 series mensuales reales
barridas la reproduce (§7), así que tiene que ser una simulada con semilla, como el peaje del simulacro.

**Q5 · ACF de un SAR(1)₁₂.** Buen gráfico y buenos distractores (a y d prueban corte frente a decaimiento y
satélites). Pero es el proceso y la cifra de 4249–4250 que la correcta repite («0.70, 0.49, 0.34»), y es la
más larga. *Mejora*: quitar las cifras de la opción correcta y dibujar otro Φ (p. ej. negativo, como el S8 del
simulacro, que alterna).

**Q6 · AICc entre familias.** La lección es la central del capítulo y los distractores son buenos (d va por
buen camino pero no desempata). Pero es la tabla y la advertencia del M10 casi literales, la correcta es la
más larga, la pista dice el criterio, la etiqueta (M6) no es el módulo de las cifras (M10), y mezcla K = 5
(−521.2) con los «16 parámetros» de K = 6. *Mejora*: otra serie (§7: `us_gasoline`, Fourier K = 12 con n
1354 frente a un SARIMA₅₂ con n 1302; o `aus_retail` Australia del Sur, cafés, donde un D = 0 gana por AICc y
no pasa Ljung–Box).

**Q7 · t contra β = 1.** La cuenta está hecha en 5363 con el resultado (0.19) que la tolerancia acepta, y la
pista dice cuál es el valor nulo. Mide restar 1 y dividir. *Rehacer*: dar el β̂ y el ee de otra serie (§7:
`vic_cafes`, β̂ log(días) 0.7056, ee 0.3011, t contra 1 −0.98) y pedir la conclusión, no la cuenta; o pedir
qué regresor añadir a una serie de nacimientos y por qué.

**Q8 · una partición frente a 61 orígenes.** Clave bien (85.2–91.8 % de victorias; 90.2 % frente a la
armónica, como dice la retro de d). Pero la tabla está justo encima, la correcta es la más larga (136 frente a
≤ 74) y la pista apunta a la respuesta. *Mejora*: opciones parejas y otra serie; el caso de `wineind` (§7)
sirve para otra pregunta: el airline tiene el menor RMSE medio y el ETS gana más orígenes (40.6 % frente a
29.0 %).

---

## 3. Fichas de los ejercicios guiados (M11, 5911–6150)

Comunes a los tres: el enunciado no fija entregables (forma, cifras a entregar); las soluciones solo están en
R; los tres van después del quiz, en el último módulo de contenido; y **los tres usan series ya vistas**:
co2 (práctica del cap. 2), USAccDeaths (práctica del cap. 2 y caso del M8), la TRM (práctica del cap. 3 y
caso del M8).

| Ej. | Serie | Módulos | Veredicto |
|---|---|---|---|
| E1 | co2 | M3, M4, M6, (M7) | **se puede mejorar** |
| E2 | USAccDeaths | M3, M8 | **hay que rehacer** |
| E3 | TRM (a), co2 (b) | M1, M8, M10, M6 | **hay que rehacer** |

**E1 · ciclo completo sobre co2 (5911).** Todas las cifras se reproducen, y la rejilla tiene una decisión
real que el enunciado deja abierta: el ganador por AICc (0,1,3)(0,1,1)₁₂ y el airline quedan a 1.211, y el
BIC elige el airline; con 6 modelos a menos de 2 y 26 de 47 que no pasan LB, hay que diagnosticar. Pero:
1. **La pista da los resultados de la primera etapa** («caen de 223.99 a 1.4555… 0.3882… 0.1543») y la
   receta de la última («no compares… hasta haber apuntado el `$nobs`… mira además su Ljung–Box»). Además,
   d = D = 1 para co2 está en la tabla del M8 (5117).
2. **La trampa de D no muerde**: el modelo sin D tiene AICc 988.10 frente a 178.21; la solución lo admite
   («la lectura ingenua acierta por casualidad»). Y remite al E3 como el caso en que «sí engaña», que tampoco
   lo es (abajo).
3. co2 repite la práctica del cap. 2, y no pide transformación ni pronóstico, así que no cubre el M7.
*Mejora*: otra serie donde la comparación ilegítima elija mal —§7: `aus_retail` Australia del Sur, cafés
(log): el (0,1,1)(1,0,1)₁₂ con D = 0 tiene AICc −1426.68 frente a −1395.98 del airline y **no pasa** LB
(0.0209 frente a 0.0629)—, pista que pregunte sin cifras y un pronóstico al final.

**E2 · el orden de ndiffs y nsdiffs en USAccDeaths (5988).** Cifras exactas, pero:
1. **La respuesta está impresa en el M8**: el recuadro (5100–5106: ndiffs 0 y 1, «Primero D, después d»), la
   tabla con `seas` y `ocsb` (5112–5117), el airline con −0.4303 / −0.5528 y LB 0.2477 (5123–5125) y el
   bloque de R con el mismo código (5180–5200).
2. **La pista lo dice**: «los operadores conmutan… Lo que no conmuta es la decisión… mira su d».
3. **Las retros de Q4 lo responden** antes de llegar (§2).
4. USAccDeaths es caso del módulo y práctica del cap. 2.
*Rehacer* con una serie nueva y sin la respuesta en la pista. Como ninguna de las 420 series barridas
reproduce la trampa del orden (§7), el ejercicio tiene que usar una serie simulada con semilla —o cambiar de
objetivo: en 8 de las 10 candidatas estacionales `nsdiffs` da 1 con `seas` y 0 con `ocsb` (§7, tabla 1), que
es la otra trampa que el E2 menciona al final y nadie practica.

**E3 · tres evidencias en la TRM y armónicos en co2 (6063).** Cifras reproducibles (§0.1), pero:
1. **(a) es la tabla del M8 copiada** (5156–5159: prueba, correlograma, ajuste forzado y AICc, con las mismas
   cifras) y su bloque de R (5205–5238); dos de las evidencias las dan además las retros de Q1. Y la TRM es
   práctica del cap. 3 y caso del capítulo.
2. **(b) da en el enunciado lo que hay que hallar** («el mejor armónico y el airline quedan a menos de dos
   puntos») y la pista da la clave («la pregunta no es cuál tiene el AICc menor: es si esa comparación se
   puede hacer»).
3. **La solución de (b) describe mal el error que dice corregir**: «responder "el armónico, por dos puntos"
   es el error». Pero el armónico tiene el AICc **mayor** (180.200 frente a 178.209): la lectura ingenua elige
   el airline, no el armónico, y el airline es también lo que da la comparación legítima (LB 0.4081 frente a
   ≤ 0.0516). Ni aquí ni en el E1 la comparación ilegítima lleva a una decisión distinta de la correcta,
   aunque el E1 lo afirma («En el Ejercicio 3… ahí la lectura ingenua sí engaña», 5984).
4. (b) usa m = 12: no practica lo que el M10 enseña (m grande).
*Rehacer*: (a) con una serie mensual sin estación nueva (§7: `PetrolPrice`, que reproduce el patrón de la
TRM, o `sunspot.month`, donde auto.arima mete un SMA espurio); (b) con m grande y un caso donde el error
muerda (§7: `us_gasoline` semanal: Fourier K = 12, AICc −25.72 con n 1354, frente al SARIMA(0,1,1)(0,1,1)₅₂,
AICc 193.17 con n 1302; o `ice.river` diario, m = 365).

---

## 4. El ejercicio en Excel (`ejercicios/capitulo-5-sarima-*.xlsx`)

`ejercicios_excel.out` (lectura con openpyxl; no se recalculó: eso lo hace `verifica_excel_cap5.py` con
Excel real).

- **13 hojas** (portada, datos y una por módulo M1–M11). El libro del estudiante deja en blanco **6580 de
  14 622 celdas con fórmula (45.0 %)**, que se reducen a **77 fórmulas distintas con instrucción** (el resto
  se arrastra). **116 celdas de comprobación** se ponen en verde cuando la cifra coincide con la del capítulo.
- **Sirve como práctica de mecánica, y es la única práctica por módulo que tiene el capítulo**: ∇₁₂ como «la
  celda de arriba», la ACF por fórmula, los ψ del airline y σₕ a escalones (la única práctica del M5), Ljung–Box
  y el AICc de la rejilla, el pronóstico con exp → mediana y media (la única del M7), la Pascua de Meeus, la
  regresión armónica con LINEST y las métricas.
- **Pero no pide ninguna decisión.** Las 20 marcas «¿…?» de las hojas son rótulos de comprobación («¿= R?»,
  «¿fuera?», «¿= celda de arriba?»), no preguntas. No hay ninguna celda donde el estudiante elija d, D, P, Q o
  un modelo.
- **Reproduce, no transfiere**: usa las tres series del capítulo (AirPassengers, USAccDeaths, TRM) y los dos
  ejemplos inventados (heladería, tienda), y cada comprobación da el número objetivo, el del capítulo.
- **La instrucción da la ecuación de cada fórmula**; en **28 de 77** da además las celdas o la llamada a
  función literal (p. ej. «=C48-C47», «DAY(EOMONTH(A60, 0))», «SQRT(SUMXMY2(observado, pronóstico)/n)»).
  En M9 son 7 de 9 y en M11, 4 de 4: ahí la tarea es transcribir.
- **Está al final**: se anuncia una sola vez, en el M11 (6155–6169), después de los ejercicios. Ningún módulo
  remite a su hoja.

Veredicto: **se puede mejorar**. *Mejora*: enlazar cada hoja desde su módulo; en cada hoja, una celda de
decisión con su comprobación (p. ej. en M3 «¿D = ?» y «¿d = ?» con validación de datos; en M6 «¿qué modelo?»);
y una hoja de transferencia con una serie nueva, donde la comprobación no sea «= capítulo» sino una propiedad
(«la ACF en 12 queda dentro de la banda»).

---

## 5. Simuladores como práctica

Catorce simuladores en M1–M11, todos sobre AirPassengers, USAccDeaths, co2, la TRM o los dos ejemplos
inventados. Ninguno recoge una respuesta, y las consignas de §1.1 dicen el resultado. La tabla ordenable
`comparativa` (9339) dice en su descripción y en su pie quién gana con cada métrica y que «las tres dejan al
SARIMA cuarto»: es la respuesta de Q8.

---

## 6. [fuera del repo] Simulacro del M12 (`SIMULACROS['cap5-simulacro']`, 9974–10367)

Una versión, 12 preguntas, 50 minutos, **se corrige al entregar** (a diferencia del cap. 4): cifra frente a
clave con tolerancia, «rutas» de errores frecuentes y la retro de la elegida y de la correcta. Series
inventadas (peaje, camiones, estación de servicio, cajeros, aseguradora, mensajería): ninguna de la lista de
práctica (`ejercicios_cobertura.out`).

- **Claves: las 12 son correctas** (§0.2), y **una sola respuesta defendible** en 11. La excepción es
  **S11**: la clave (la armónica K = 5) se justifica por la regla del M10 («con m grande, Fourier»), pero la
  retro de d dice que «entre familias distintas solo decide la comparación fuera de muestra», y ninguna opción
  dice «con esta tabla no se puede decidir entre las dos familias». Quien marque d con ese argumento tiene
  razón a medias.
- **Posición**: 3 2 4 1 3 2 (1→1, 2→2, 3→2, 4→1). **Tamaño**: la más larga acierta 0 de 6; la más corta,
  1 de 6 (S9: 69 frente a 72–79). S1 y S8 tienen las cuatro opciones de igual longitud.
- **Pistas**: no hay, por diseño. **Retros**: 24 de 24.
- **Etiquetas**: dicen el módulo; la de S3 («La rejilla por AICc») no delata la trampa.
- **Tolerancias**: **0.8 % de la clave** en las seis numéricas (`ejercicios_longitud_opciones.out`). Acepta
  los redondeos honestos (N2 con logaritmos a cuatro decimales; N5 18.4; N6 0.136; N7 con el logaritmo a dos
  decimales, 561.16; N10 2.8) y ninguna ruta cae dentro. Pero **acepta dos errores que el ítem quiere
  detectar**:
  - **N7 acepta olvidar el satélite θΘε₍t−13₎**: 556.774, a 4.296 de la clave con tolerancia 4.489. Es justo
    el término que el N4 enseña a no olvidar.
  - **N5 acepta dividir entre n en vez de n − k** en los dos términos que hay que calcular: 18.279, a 0.091
    con tolerancia 0.147. Como los otros 22 términos vienen sumados en el enunciado, el ítem no puede
    separar las dos cosas.
  - N6: el enunciado da los ψ con el escalón ya escrito (ψ₁₂ = (1 + θ) + (1 + Θ)), así que la ruta «no vio el
    escalón» solo puede darse sin leer el enunciado: el ítem mide sumar cuadrados, no saber qué pesos entran,
    que es lo que el M12 dice que se repite entre versiones.
- **Texto que no es de esta serie**: la ruta de N2 dice «no tomó logaritmos: diferenció **las noches** en
  miles» (10030; fuente `ensamblado/cap5/simulacro.js`, 465): son vehículos, no noches. Lo ve el estudiante
  tras entregar.
- **S9**: la retro dice que la dispersión del último tercio es «2.4 veces» la del primero; el dibujo da
  2.49 (medida aproximada, sobre el SVG).

Veredicto: **sirve**, con los dos bordes de tolerancia (N5, N7), la ambigüedad de S11 y la palabra «noches»
como arreglos del banco. Es el instrumento mejor construido del capítulo: series nuevas, opciones parejas,
posiciones repartidas y una corrección que nombra el error.

---

## 7. Datos: qué series usa la práctica y cuáles faltan

**Series de la práctica del cap. 5**: co2 (E1, E3b; **repetida del cap. 2**), USAccDeaths (E2, Q4;
**repetida del cap. 2** y caso del M8), la TRM (E3a, Q1; **repetida del cap. 3** y caso del M8), AirPassengers
(Q6, Q7, Q8 por sus cifras). El Excel usa las mismas tres del capítulo. Solo el simulacro trae series nuevas
(inventadas). Ninguna de las candidatas de abajo aparece en `Htmls_Series/` (`ejercicios_series_grep.out`);
se descartaron `nottem`, `mdeaths`, `fdeaths` (práctica del cap. 1), `ldeaths` (su suma) y la columna Gas de
`aus_production` (quiz del cap. 1). Cifras de `ejercicios_series_candidatas.out` y de los dos barridos.

Propiedades base (tabla 1 de `ejercicios_series_candidatas.out`): `wineind` (forecast, n 176, pide log:
cor(media, desviación anual) 0.681); `Seatbelts[, "kms"]` (n 192, aditiva: −0.213); `souvenirs` (fpp3, n 84,
0.993); `aus_retail` Victoria cafés (`vic_cafes`, n 441, 0.946). En las cuatro, nsdiffs 1 y la ACF de ∇y en 12
fuera de banda (0.782, 0.733, 0.770, 0.757).

| Módulo | Candidata | Lo medido que la hace servir |
|---|---|---|
| **M1** · ver la firma, y no verla | `wineind` · `Seatbelts[, "kms"]` | ∇y: r12/r24/r36 = 0.782 / 0.691 / 0.623 y 0.733 / 0.643 / 0.590, banda 0.148 y 0.142; la primera pide log, la segunda no |
| | `Seatbelts[, "PetrolPrice"]` (sin estación) | ρ̂12 en niveles 0.498 (> 0.142); en ∇y −0.034 / 0.013 / 0.066, todo dentro; nsdiffs 0 con `seas` y con `ocsb`; SAR forzado Φ −0.0321, t −0.45; auto.arima (0,1,0). Reproduce el caso TRM. Nota: es otra columna del conjunto de `UKDriverDeaths` |
| **M2** · escribir el producto y sus satélites | `wineind` | auto.arima (1,1,1)(0,1,1)₁₂: regular × estacional, con satélites en 11, 13 por expandir |
| | `souvenirs` (log) | auto.arima (2,0,0)(0,1,1)₁₂ con deriva: AR(2) × SMA, otro producto |
| **M3** · decidir D, d; sobrediferenciar | `wineind` · `Seatbelts[, "kms"]` · `vic_cafes` | `seas` 1 frente a `ocsb` 0 en las tres; con D = 2, Θ̂ −0.998 (raíz 1.0002), −0.998 (1.0001), −1.000 (1.0000). **La trampa del orden de USAccDeaths no aparece en ninguna de 185 series en log ni de 235 en escala cruda** (`ejercicios_series_barrido*.out`): para ella, una serie simulada con semilla |
| **M4** · identificar P y Q | `wineind` · `Seatbelts[, "kms"]` | auto.arima con SMA y sin SAR ((1,1,1)(0,1,1) y (2,0,1)(0,1,1)) |
| | SAR | ninguna serie real limpia: `aus_livestock` Victoria, cerdos, da (4,1,0)(2,0,0) con LB 0.0000; `nino3`, (2,0,2)(1,1,0) con LB 0.0000. Para el SAR, una simulada (como el S8 del simulacro) |
| **M5** · el airline y σₕ a escalones | `souvenirs` (log) | airline θ −0.563, Θ −0.484, LB 0.5023; σ₁₃/σ₁₂ = 1.1369 frente a σ₁₂/σ₁₁ = 1.0323 |
| | `wineind` (log) | θ −0.892, Θ −0.653, LB 0.0680; σ₁₃/σ₁₂ 1.0878 frente a 1.0052: el escalón casi es todo el crecimiento |
| | `Seatbelts[, "kms"]` | θ −0.709, Θ −0.790, LB 0.2235; σ₁₃/σ₁₂ 1.0631 frente a 1.0227 |
| **M6** · la trampa del AICc entre D | `aus_retail` Australia del Sur, cafés, restaurantes y comida para llevar (log) | (0,1,1)(1,0,1)₁₂ con D = 0: AICc −1426.68 frente a −1395.98 del airline, y **no pasa** LB (0.0209 frente a 0.0629): la comparación ilegítima elige mal |
| | `aus_retail` Victoria / Australia del Sur, muebles y textiles (log) | lo mismo: −1186.51 / −1163.79 (LB 0.0373 / 0.0661) y −1074.63 / −1049.18 (LB 0.0460 / 0.1607) |
| | `aus_retail` Nueva Gales del Sur, comida para llevar (log) | D = 0 gana por AICc (−1536.67 / −1502.13) y **los dos pasan** LB (0.1741 / 0.2566): caso donde solo la partición decide |
| **M7** · ciclo completo con log y pronóstico | `souvenirs` | cor 0.993 (log obligado); airline pasa LB; auto.arima elige d = 0 con deriva: decisión de d discutible |
| | `vic_cafes` | cor 0.946; airline LB 0.3893; n 441 |
| **M8** · las pruebas engañan / descartar la estación | `Seatbelts[, "PetrolPrice"]` | ver M1: el contraejemplo limpio |
| | `sunspot.month` 1950–2013 | nsdiffs 0 con las dos pruebas y ∇y dentro de banda, pero auto.arima devuelve (1,0,4)(0,0,1)₁₂ y el SAR forzado da t 1.74: la búsqueda automática encuentra una estación que no hay |
| **M9** · calendario | `vic_cafes` (log) | β̂ log(días) 0.7056 (ee 0.3011): t contra 0 2.34, contra 1 −0.98 (como AirPassengers); ΔAICc −2.63 |
| | `canadian_gas` · `aus_births` NSW (escala cruda) | t contra 0 de log(días) 5.15 y 3.21; ΔAICc −21.77 y −7.24 |
| **M10** · m grande | `us_gasoline` (fpp3, semanal, n 1355) | Fourier: AICc mínimo en K = 12 (−25.72, n 1354), LB(104) < 0.05 en K = 1…12; SARIMA(0,1,1)(0,1,1)₅₂: AICc 193.17 con n 1302, se ajusta en 2.1 s. La trampa de D otra vez |
| | `ice.river` (tseries, `flow.jok` diario, log, n 1096) | Fourier: mínimo en K = 2 (−1923.07); LB(30) < 0.01 en K = 1…5; un ∇₃₆₅ gastaría 365 de 1096 datos |
| | `taylor` (forecast, semihoraria, m = 48 y 336, n 4032) | Fourier K = (10, 10): 38 términos; un ∇₃₃₆ gasta 336 datos |
| **M11** · una partición frente a muchas | `wineind` (log) | una partición y 69 orígenes coinciden en el airline (RMSE medio 2676.94), pero el ETS gana en más orígenes (40.6 % frente a 29.0 %): otra lección («el mejor medio no es el que más gana») |
| | `vic_cafes` (log) | coinciden (airline); no sirve para la inversión. **No se halló una serie real donde el orden se invierta**; el S12 del simulacro la inventa |

---

## 8. Lista de huecos (por prioridad)

1. **No hay ninguna tarea antes del quiz del M11**: 9912 palabras (50–66 min; 155 min declarados para
   M1–M10), 0 «Para practicar», y consignas de simulador que dicen el resultado. Cada módulo necesita su
   «Para practicar» como el cap. 4, con una serie nueva (§7).
2. **E2 y E3(a) se responden leyendo el M8**, y las retros de Q1 y Q4 los responden antes de llegar. Rehacer
   con series nuevas; la del orden, simulada.
3. **La solución del E3(b) describe mal el error** («el armónico, por dos puntos» tiene el AICc mayor), y el
   E1 afirma que en el E3 la lectura ingenua engaña. En ninguno de los dos la trampa de D muerde: §7 da cuatro
   series de `aus_retail` donde sí.
4. **El quiz se contesta recordando**: 8 de 8 respuestas en pantalla (Q7 con la cuenta hecha en 5363), la
   más larga acierta 5 de 5, 8 pistas dan el criterio, 4 retros filtran ejercicios. Rehacer Q4 y Q7; en el
   resto, otra serie, opciones parejas, pistas que pregunten.
5. **Las tres series de los ejercicios repiten capítulos anteriores** (co2, USAccDeaths, TRM).
6. **Sin práctica**: M5 (el airline y σₕ) en el capítulo; M7 (transformación y pronóstico) y M10 (m grande)
   solo de refilón. Hoy los cubren el Excel y el simulacro.
7. **El Excel no pide decisiones** y está escondido al final del M11; 28 de sus 77 instrucciones dictan la
   fórmula.
8. [fuera del repo] Simulacro: N7 acepta olvidar el satélite y N5 acepta dividir entre n; S11 admite dos
   lecturas; «las noches» en la ruta de N2.
9. Cosmético: E3(a) imprime −0.0024 y t 0.0147 donde R 4.6 da −0.0025 y 0.0146; Q6 mezcla K = 5 y los 16
   parámetros de K = 6, y su etiqueta (M6) no es el módulo de sus cifras (M10).
