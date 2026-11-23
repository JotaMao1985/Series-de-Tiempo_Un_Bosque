# Capítulo 4 · ronda R3 («estructura») · cambios

Ronda R3 del `PLAN_Mejora_Cap4.md` (tareas T3.1 y T3.2; decisiones D5, D6 y D7). Fecha: 2026-11-22. Un solo redactor; sin commit ni
push. Base: `531b907`. Especificación: `diagnostico/cap4/lector_estudiante.md`, leída contra el capítulo tal como lo dejaron la R1 y la R2;
los pasajes se localizaron por su texto, no por la línea.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/cap4/templates_1_3.html` | M1 (modelo ajustado a la vista, tabla de casos, `c`), M2 (`d` impreso), M3 (PP, dos medias, `auto.arima`, introducción del simulador, bloques) |
| `ensamblado/cap4/templates_4_6.html` | M4 (introducción y recuadro, α), M5 (T, la nota de la TRM sale), M6 (n/T, introducción y recuadro) |
| `ensamblado/cap4/templates_7_9.html` | M7 (los siete), M8 (dos medias, RMSE/MAE/naïve, «rango»), M9 («abanico», cierre) |
| `ensamblado/cap4/templates_10.html` | M10: apertura, un solo resumen del Nilo, TRM, bloque del puente (R y Python), resumen |
| `ensamblado/ensambla_cap4.py` | solo `courseData`: los minutos medidos y su comentario de convenio |
| `Htmls_Series/capitulo-4-modelos-arima.html` | reensamblado con `ensambla_cap4.py`; reproducible byte a byte (md5 `5d041667…`, dos corridas seguidas) |
| `diagnostico/cap4/comprobaciones/r3_*` | guiones y salidas de la ronda (abajo) |
| `diagnostico/cap4/capturas/r3/` | 32 capturas, a 1200 y 375 px (git las ignora) |

Los capítulos 5 y 6 se reensamblaron después y quedan **idénticos a HEAD** (`git status` no los lista). No se tocó `chapter.js`, el
armazón, la plantilla, el cap. 2 ni el 3, `Htmls_Series/preparcial-corte-2.html`, las diapositivas, `bibliografia/`,
`SIMULACROS['cap4-simulacro']`, la autoevaluación (enunciados, opciones, pistas y retros), el enunciado y la solución de los
ejercicios 1 a 3, ni los módulos 11 y 12. **Ningún título de módulo cambia** y ningún id. No se añadió ningún `<cite>`, `data-afirma`,
autor, año, sección ni DOI. «Phillips–Perron» (M3) es el nombre de la prueba, que el M8 ya escribía así. No hay clases nuevas de
Tailwind (`compila_tailwind.py --comprobar` en verde dentro de `verifica_todo.py`).

**Cómo se editó.** `r3_edita.py` más una lista por módulo (`r3_ediciones_m1.py` … `m10.py`, `r3_ediciones_minutos.py`): 48
sustituciones literales (texto que sale, texto que entra), cada una debe aparecer exactamente una vez en la base; dos de ellas
(`entre()`) sustituyen un bloque entre dos marcadores únicos: la nota de la TRM del M5 (12 líneas, que sale) y la apertura y el cuadro
del Nilo del M10 (101 líneas, reescritas). **Es reejecutable**: siempre parte de `HEAD` (o de `--base`), no del archivo de trabajo;
`--comprobar` verifica que el árbol es `HEAD` + ediciones (los cinco archivos: «idéntico a HEAD + ediciones»). El código nuevo va sin
escapar en las listas y pasa por `html.escape`. Después, `ensambla_cap4.py`, `ensambla_cap5.py` y `ensambla_cap6.py`, en ese orden.

---

## T3.1 · Orden sin renumerar (D5)

Ningún módulo cambia de número, de título ni de id.

| Módulo | Qué se hizo | Dónde |
|---|---|---|
| **M1** | **El ARIMA(1,1,1) del Nilo se ajusta a la vista la primera vez que se usa**: el primer bloque (R y Python) estima `arima(Nile, order = c(1,1,1), method = "ML")`, imprime los coeficientes y sus errores estándar (0.2544 y −0.8741; 0.1194 y 0.0605) y la raíz MA (1.144), y `phi`/`theta` salen de ahí (antes entraban como constantes y se justificaban en el M10, 2 048 líneas después). Todas las cifras que el bloque ya imprimía (1.006, 32.8, 1.363, 56.7…) salen iguales. En Python, el ajuste de statsmodels da 0.2549 y −0.8749 y se dice que abajo se usan los de R. La nota de la anomalía dice «coeficientes estimados» (no «reales»); «el software decidió que sí» pasa a «la regla automática que elige $d$ decidió que sí». **La tabla «Casos particulares»** (ya no «ya conocidos») gana un párrafo que presenta en una frase el suavizamiento exponencial simple y el método de Holt, dice que el capítulo no los usa más allá de la equivalencia, y la fila de Holt dice qué suaviza. La constante `c` de la definición se anuncia («la trata el Módulo 5; hasta entonces el modelo va sin ella») | bloque de código; nota «Una anomalía…»; h3 «Casos particulares»; párrafo tras la definición |
| **M2** | El esqueleto del ciclo imprime `d` (`d`, `#> [1] 1`), de modo que la etapa 1 muestra una cifra y el cierre («despacha la etapa 1 en una línea») habla de algo que se vio | bloque R |
| **M3** | **PP**: la fila de «Las pruebas» dice «PP (Phillips–Perron…)» en su primer uso y el bloque R imprime `PP.test(Nile)$statistic` (−6.690, `p = 0.01`, tope de su tabla): el −6.690 de la prosa ya sale de un bloque (en Python se dice que statsmodels no trae la prueba). **El «modelo de dos medias»** se escribe donde se usa por primera vez (`y_t = μ + β·1{t ≥ 1899} + ε_t`) y el bloque lo ajusta: imprime las medias (1097.75 y 849.97), β̂ = −247.78 y σ̂ = 127.03, de donde sale el 127.03 del experimento (antes constante). **`auto.arima`** se presenta en su primer uso (la función de `forecast` que ajusta sola varios ARIMA, se queda con el de menor AICc y abre el Módulo 7). **La introducción del simulador** pasa de 151 a 122 palabras (la parte que queda explica la segunda curva, ℓ = 12) y deja de decir que KPSS «funciona» en β = 0, que «rechaza menos pero no deja de engañarse» y el valor 247.8: pide recorrer β desde 0 y buscar el cruce con el 50 % (el resultado ya estaba en el recuadro «El resultado», que viene después). El recuadro de `ndiffs()` ya no se titula «Tres pruebas, tres respuestas» (chocaba con las «tres evidencias»): «Una misma serie, tres respuestas de `ndiffs()`» | tabla de evidencias; recuadro de `ndiffs()`; párrafo del experimento; introducción del simulador; bloques R y Python |
| **M4** | **La introducción del simulador** pasa de 205 a 63 palabras y pide hacer (qué corta, qué decae, el signo del rezago 1, qué barras salen de la banda). Lo que antes adelantaba (la trampa de la PACF del AR(1), el −0.626 de $d = 2$, el −0.402 de doble lectura, «la tabla elige $p$ y $q$; no confirma $d$») va a un recuadro **después** del simulador, «Lo que enseña el simulador»; lo del rezago 8 pasa al párrafo de la lectura de la tabla. El IMA(1,1) dice su α = 1 + θ̂ = 0.267 y el bloque lo calcula (R y Python) | introducción; recuadro tras el simulador; párrafo «La lectura es razonablemente clara»; bloques |
| **M5** | **La nota de la TRM sale** (usaba la serie y «la caminata que elige `auto.arima`» 1 154 líneas antes de presentarlas; su contenido, reescrito, va al recuadro «El resultado, aceptado tal cual» del M10, donde el bloque de la TRM lo respalda). Notación: `ŷ_{n+h}` → `ŷ_{T+h}` («con $T$ el último dato») | regla mnemotécnica |
| **M6** | **La introducción del explorador** pasa de 170 a 108 palabras y pide contar y mirar (cuántos modelos a menos de 2 puntos, cuáles rechaza Ljung–Box, qué raíces tiene el mejor de cada $d$); las respuestas van a un recuadro **tras** el explorador, «Lo que enseña el explorador». De paso se aclaran dos cuentas que se leían contradictorias: «cuatro más» (sin constante) frente a «siete» del Módulo 7 (con las variantes con deriva), y «ocho» modelos que rechazan Ljung–Box de los 27 (uno solo con $d = 1$; ninguno de los que quedan cerca del mejor de su $d$). Notación: se avisa que $n$ es la $T$ de los Capítulos 2 y 3 | nota de la fórmula del AICc; introducción; recuadro |
| **M7** | «Siete modelos a menos de 2 puntos»: se dice que son el ganador, otros cuatro sin constante (los del Módulo 6) y dos variantes con deriva | nota del podio |
| **M8** | El escalón es «el modelo de dos medias del Módulo 3»; `RMSE`, `MAE` y *naïve* se glosan donde la tabla fuera de muestra los usa por primera vez (el *naïve* «es la caminata aleatoria»); «el abanico completo va de 123 a 133» → «el rango completo» | párrafo del escalón; recuadro «Y ahora la parte incómoda» |
| **M9** | «Abanico» se define en su primer uso (la banda del pronóstico, que se abre con el horizonte). El cierre dice lo que mide el M10 (el 80 % y el 95 %) y que cierra con el puente y el resumen | nota del $d = 2$; último párrafo |

Lo que ya estaba bien y no se tocó: las tablas, las derivaciones plegadas y los demás simuladores; las introducciones de simulador del M8, el
M9 (forma) y el puente (piden hacer y no adelantan).

---

## T3.2 · El M10, ordenado (D6) · sin partirlo

Orden de las secciones (`h3`), antes y después. Palabras de prosa con la convención de `r3_minutos.py` (sin `<pre>`, sin fórmulas en
bloque, cada fórmula en línea cuenta como una palabra; sin pista ni solución de los ejercicios); `r3_secciones_m10.py`:

| Sección | Antes | Después |
|---|---|---|
| (apertura) | 115 | 145 |
| El Nilo, de principio a fin | 688 | **617** |
| Caso: la tasa representativa del mercado | 1 470 (2 `<pre>`) | 1 523 (2 `<pre>`) |
| El puente al Capítulo 5 | 354 (0 `<pre>`) | 369 (**2 `<pre>`**) |
| Resumen del capítulo | 397 | 392 |
| Autoevaluación · Ejercicios propuestos · Lecturas | 37 · 166 · 311 | 37 · 166 · 311 |
| **Total** | **3 538** | **3 560** |

El orden de los `h3` no cambia (el Nilo, la TRM, el puente, el resumen, la evaluación): ya era el pedido, y lo que fallaba era lo que
había **dentro** de cada parte. Qué cambia:

- **El Nilo se resume una sola vez.** Antes eran cuatro resúmenes seguidos: la tabla de siete filas, la fórmula del modelo con sus
  coeficientes (repetía la del M1), la nota de las dos lecciones y el empalme. Queda la tabla (con las filas más cortas y sin los
  números que ningún bloque imprimía: el Shapiro p = 0.731 y los semianchos ±278/±391, ahora σ_30/σ_1 solo en la comparación de las tres
  series), una frase sobre el modelo (el del Módulo 1, ya ajustado a la vista) y la nota de las dos lecciones. La apertura dice los
  cuatro tiempos y que el resumen cierra el módulo antes de la evaluación.
- **La TRM.** La tabla pierde el «192 modelos (con la parte estacional permitida; sin ella son 42)» (no salía de ningún bloque ni se
  había presentado la parte estacional): «auto.arima con búsqueda exhaustiva devuelve ARIMA(0,1,0)». «Los coeficientes no están
  identificados» → «no son identificables» (el otro sentido de «identificación» es proponer $p$ y $q$). La nota «El resultado, aceptado tal
  cual» recoge lo que decía la nota de la TRM del M5 (la deriva es la media de las diferencias, $(y_n − y_1)/(n−1)$; una tendencia visible que
  no se distingue de cero con $n = 138$ habla de la variabilidad). El *naïve* remite al M8. La presentación de la etapa 4 es más
  corta (la deducción de $σ_h^2 = hσ^2$ está en el M9).
- **La promesa del M9 se cumple.** El M9 dice «el Módulo 10 lo mide» (el 80 % cubre el 83.9 % a un mes en la TRM). La cifra salía del
  bloque de la TRM (R1) pero la prosa no la retomaba; ahora el párrafo de cobertura dice: «a un mes, los dos intervalos se cumplen dentro
  de la muestra: el 95 % deja fuera solo 6 de los 137 cambios, un 4.4 %, y el 80 % del Módulo 9 cubre el 83.9 %». El M9 no se retira.
- **El puente gana su código** (R y Python; antes ninguna cifra tenía bloque). El bloque de R: `auto.arima(log(AirPassengers),
  seasonal = FALSE, stepwise = FALSE, approximation = FALSE)` → ARIMA(0,1,5) con ρ̂12 = 0.7245, ρ̂24 = 0.6727, banda 0.1633 y Q = 222.4;
  la búsqueda con `max.p = max.q = 8, max.order = 16` → ARIMA(8,1,3) con deriva y ρ̂12 = 0.437; el modelo *airline* con ρ̂12 = −0.0515 y
  Ljung–Box(24) `p = 0.233`; y las 143 y 131 observaciones. El de Python ajusta el (0,1,5) y el *airline* con statsmodels
  (ρ̂12 = 0.7218 y −0.0525; Q = 219.3; `p = 0.3676`), con una línea que dice las cifras de R y que statsmodels no trae `auto.arima`, así
  que la búsqueda amplia se queda en R (el (8,1,3) de statsmodels es otro óptimo, ρ̂12 = 0.515, y no se mostró).
- **El resumen** sigue siendo lo último antes de la evaluación; la viñeta de las evidencias ya no repite el «100 % de las veces» del
  Monte Carlo del M3 (queda «un cambio de nivel como el del Nilo hace que KPSS lo lea como una raíz unitaria»). La nota «Y en el
  Capítulo 5…» queda al final, como «lo que viene» (después de las lecturas), como en el cap. 3.
- **Las palabras.** El módulo **no baja**: 3 538 → 3 560 palabras de prosa (3 490 → 3 512 con la herramienta del módulo). El Nilo baja 71,
  pero la TRM suma 53 (la nota de la deriva que vino del M5, el 80 %) y la apertura 30. El ahorro real está en lo que el lector ya no
  tiene que leer dos veces (cuatro resúmenes del Nilo → uno), no en el total. Sigue siendo el módulo más largo; ver las preguntas.

### Notación

| Costura | Convención | Dónde se aplicó |
|---|---|---|
| `T` frente a `n` | **En el cap. 4, `n` es el número de observaciones y `n* = n − d` el efectivo; `T` es el origen del pronóstico, el último dato (`T = n`).** Se avisa **una vez**, donde el AICc cambia de símbolo respecto del cap. 3 (que escribe `T − k − 1`): «lo que los Capítulos 2 y 3 llamaban $T$». `ŷ_{n+h}` del M5 pasa a `ŷ_{T+h}`. **No se cambió `n` por `T` en todo el capítulo**: la autoevaluación, el simulacro, el preparcial, las diapositivas y las etiquetas de los simuladores (`n`, `n efectivo`, `±1.96/√n`) usan `n` y `n*`, y están fuera de alcance; cambiarlos en la prosa los habría desalineado | M5 (T), M6 (aviso) |
| `n*` | Ya consistente (M6, M10); el aviso de arriba la cubre | M6 |
| «abanico» | Es **la banda de un pronóstico que se abre con el horizonte** (como en el cap. 3). Se define en su primer uso (M9). El otro uso, un intervalo de valores en la tabla del M8, pasa a «rango» | M8, M9 |
| «tres evidencias» | Son el gráfico con la ACF, las pruebas y los síntomas de diferenciar de más (la R1 retiró la varianza; **no se reintrodujo**). El recuadro de `ndiffs()` deja de titularse «Tres pruebas, tres respuestas» | M3 |
| «cuatro» frente a «siete» modelos a menos de 2 puntos | Cuatro (sin constante, más el mejor) en el M6; siete en el M7 (con dos variantes con deriva); se dice | M6, M7 |
| «identificación» / «identificable» | Se identifican $p$ y $q$ (etapa 1); un coeficiente es identificable o no | M10 |

---

## Minutos medidos (D7)

La herramienta es `r3_minutos.py`, la del cap. 3 adaptada al cap. 4 (la misma fórmula, palabras/180 + 3 por simulador + 2 por bloque
de código, pista y solución abiertas, sin plegados ni quizzes; `texto()` quita las fórmulas antes que las etiquetas, que es la
corrección que el cap. 3 hizo a `diag/lector_carga.py`). En el cap. 4 **la corrección no cambia nada**: medido sobre `HEAD`, la herramienta
original y la corregida dan lo mismo en los doce módulos (`r3_minutos_antes.out` frente a `r3_minutos_antes_herramienta_original.out`).
«Antes» es `HEAD` (la R1 y la R2 ya habían movido algo: el diagnóstico decía M1 9.9 y M10 29.4 cerrado; hoy el M10 mide 30.4).

| Mód. | Palabras antes → después | Medido antes (abierto) | Medido después | Declarado antes → ahora | Distancia ahora |
|---|---|---|---|---|---|
| M1 | 889 → 999 | 9.9 | 10.6 | 12 → **11** | 0.4 |
| M2 | 868 → 868 | 6.8 | 6.8 | 10 → **7** | 0.2 |
| M3 | 1 552 → 1 568 | 13.6 | 13.7 | 16 → **14** | 0.3 |
| M4 | 703 → 713 | 8.9 | 9.0 | 14 → **9** | 0.0 |
| M5 | 837 → 710 | 6.7 | 5.9 | 12 → **6** | 0.1 |
| M6 | 757 → 856 | 9.2 | 9.8 | 16 → **10** | 0.2 |
| M7 | 810 → 828 | 9.5 | 9.6 | 14 → **10** | 0.4 |
| M8 | 1 022 → 1 061 | 10.7 | 10.9 | 16 → **11** | 0.1 |
| M9 | 1 114 → 1 150 | 14.2 | 14.4 | 16 → **14** | 0.4 |
| M10 | 3 490 → 3 512 (abierto 4 300 → 4 322) | 30.4 cerrado · 40.9 abierto | 32.5 cerrado · 43.0 abierto | 24 → **43** | 0.0 |
| M11 | 457 | 2.5 | 2.5 | 40 → **40** (el reloj del ensayo) | — |
| M12 | 456 | 2.5 | 2.5 | 5 → **3** | 0.5 |
| M1–M10 | | 130.4 (abierto) | 133.7 | 150 → **135** | |

Se declara la columna «abierto» (convenio de los caps. 2 y 3), con su comentario en `courseData`: no incluye el tiempo de resolver
los ejercicios, los desarrollos plegados (unos 4 min entre M1, M3 y M9), la autoevaluación del M10 (18.1 min de lectura de enunciados,
opciones, pistas y retros) ni el simulacro (6.8 min de lectura; su reloj son los 40). Distancia máxima: **0.5 min** (el objetivo era
< 3). El diagnóstico tenía razón: M1–M9 declaraban 126 y medían 89.5 (en `HEAD`); el M10 declaraba 24 y medía 40.9 con las soluciones abiertas. **El
módulo que más pesa es el M10 con 43 min** (3 simuladores, 5 bloques de código y 3 ejercicios con solución). La portada no muestra
minutos de módulo; `cuenta_sitio.py` sigue en verde.

---

## Cifras de la prosa y de dónde sale cada una

`r3_cifras.R` (→ `r3_cifras.out`) recalcula en R, aparte de la página, **66 cifras** que la ronda escribe, mueve o deja en la prosa del
M10 y de los módulos que toca: las 66 coinciden con lo citado (0 «NO»). De dónde sale cada grupo:

| Cifras | Salen de |
|---|---|
| 0.2544, −0.8741, e.e. 0.1194 y 0.0605, raíz MA 1.144, AR 3.93 | bloque del M1 (nuevo) |
| PP −6.690 (`p = 0.01`) | bloque del M3 (nuevo) |
| medias 1097.75 y 849.97, β̂ = −247.78, σ̂ = 127.03 | bloque del M3 (nuevo) |
| α = 0.267 | bloque del M4 (nuevo) |
| 0.498, −0.402, δ̂ = −2.883 (t = −1.43), AICc 1268.06 y 1267.51, BIC 1274.28, AICc (1,2,2) 1264.60, 18 y 42 modelos, Ljung–Box 0.800, RMSE 125.05/127.99/123.06, 816.18, 842.17, 740, ψ∞ = 0.169, σ_30/σ_1 = 1.404 | bloques de los M2 a M9 (ya estaban) |
| 8 de 27 con Ljung–Box < 0.05; cuatro a menos de 2 puntos con $d = 1$; raíces 1.161, 1.144, 1.000–1.048 | datos del explorador (`genera_cap4.R` → `cap4_datos.js`); recalculadas aquí |
| ρ̂12 = 0.7245, ρ̂24 = 0.6727, banda 0.1633, Q = 222.4, ARIMA(0,1,5), ARIMA(8,1,3) con ρ̂12 = 0.437, *airline* con ρ̂12 = −0.0515 y `p = 0.233`, 143 y 131 observaciones | **bloque del puente (nuevo)**; antes, ninguna (Q = 222.4 ni siquiera estaba en el JSON) |
| TRM: ADF, KPSS, ρ̂1 = 0.088, ρ̂8 = −0.190, rejilla (1703.38, 1708.83), raíces (1.0042, 1.0000), Ljung–Box, Shapiro, deriva 8.00 (e.e. 10.36), semianchos, 6 y 5 de 137, 11 de 126, curtosis 5.1 y 2.8, asimetría 0.76, 1.07–1.14, 83.9 % | bloque de la TRM (ya estaba) |
| ACF de la TRM en niveles 0.964; σ̂² = 14 756.38 | datos del simulador (`genera_cap4.R`); recalculadas aquí |
| 89.6 % (cobertura del naïve a 1–12 meses) | datos del cap. 6 (`cap6_evaluacion.json`); lo verificó la R1 |

De las diez cifras del M10 que el diagnóstico listaba sin bloque (842.17, ±278 y ±391, 816.18, 192 modelos, ρ̂12/ρ̂24/banda, Q = 222.4,
ARIMA(0,1,5) y (8,1,3), *airline*, 143 y 131): **ninguna sigue sin bloque**; una se quitó (192), una se sustituyó por cifras que el M9 sí imprime
(±278/±391 → σ_30/σ_1) y el resto sale de un bloque. Lo que queda **sin bloque en el M10 y no se respaldó con uno**: los dos meses de mayor
devaluación de la TRM («marzo de 2020, julio de 2022»; `r3_cifras.out` los recalcula: +470.2 y +466.8) y las dos cifras de la introducción de los
simuladores de la TRM que salen del JSON (0.964 y 14 756.38).

**En los módulos que la ronda no tocaba y siguen con cifras sin bloque** (la parte «36 de 50» que no es del M10): M3 (Monte Carlo de ADF/PP,
4.8 %, 86.4 %, 70.8 %…: del generador), M8 (Shapiro 0.731, σ̂² de los MA(1) sobre $d = 2$ y 3, AICc del escalón 1257.91, MAE), M9 (920.56,
los anchos 561 → 677…, φ̂ = −0.39). Salen del JSON del generador o de la prosa, no de un bloque; es trabajo de la R4 (fuentes).

---

## Lo que no se hizo, y por qué

| Qué | Por qué |
|---|---|
| La caja del `lynx` del M8 (da la respuesta del ejercicio 2) y la nota de `BJsales` del M9 (la del ejercicio 3); `lynx` y `BJsales` se usan antes de presentarse | Es la D9 / R5 (el E2 con otra serie y la frase del M8 retirada o movida; el E3 sin el resultado en el M9). Tocarlas ahora dejaría a la R5 rehacer el trabajo |
| Los rótulos del selector del M9 («vuelve a la media», «se aplana», «recta»…) siguen contestando la pregunta de la introducción | El encargo nombra las introducciones del M3, M4 y M6. Cambiar el selector toca `chapter.js` y las diapositivas; queda anotado |
| La introducción del simulador del M1 aún adelanta algo («la media cae a casi cero», «con $d = 2$… por debajo de −0.5») | No estaba en la lista (el diagnóstico la deja como gancho); se anota |
| El cambio de `n` por `T` en todo el capítulo | Ver Notación: la autoevaluación, el simulacro, el preparcial y las diapositivas quedarían desalineados. Pregunta 1 |
| El M5 sigue sin elemento interactivo; `checkresiduals()` solo se nombra en el M2; los 10–20 avisos «R da X, Python Y» sin jerarquía | La práctica del M5 es de la R5 (D9); los dos últimos no están en D5–D7 |
| La tabla de «Los 27 modelos» y la salida del código del M6 repiten las mismas filas (D, el diagnóstico) | Es un ahorro de lectura, no de estructura; no hay una ronda que lo pida |
| `preparcial-corte-2.html` | No cambió ningún título de módulo. La tabla `MODULOS_DEL_CORTE` sigue al día |
| La R4 | Nada de lo que se movió llevaba atribución: no se movió ninguna frase con `<cite>` ni `data-afirma` |

## Lo que se encontró

1. **El M1 ya no necesita el M10 para justificarse.** Con el ajuste a la vista, «los coeficientes reales del Nilo» (2 048 líneas antes de
   su justificación) se leen estimados al primer uso. 
2. **La herramienta de medida del cap. 3 no cambia nada aquí** (ver Minutos): el cap. 4 no escribe `<` crudos en fórmulas en línea.
3. **Las cuentas «cuatro» (M6) y «siete» (M7) modelos a menos de 2 puntos son las dos ciertas**: cuatro más el mejor sin constante; siete
   con las dos variantes con deriva. Se leían contradictorias por una frase que faltaba.
4. **El «8 modelos» del explorador era «8 de los 27», no «de $d = 1$»**: con $d = 1$ solo rechaza uno, el (0,1,0). La frase original
   («descarta ocho modelos…») se leía mal después de «Empieza en $d = 1$».
5. **statsmodels y el *airline*:** los 13 primeros residuales son del arranque difuso; si se incluyen (`resid[1:]`) Ljung–Box da
   `p = 0.999977` en lugar de 0.37. El bloque descarta 13 (1 + 12), no 1.
6. **El (8,1,3) con deriva de la búsqueda amplia no se reproduce en statsmodels** (otro óptimo, ρ̂12 = 0.515 frente a 0.437): se dice y se deja en R.

## Preguntas para el docente

1. **¿`n` o `T`?** Se dejó `n` y `n*` en el cap. 4 con un aviso en el M6, porque la autoevaluación, el simulacro, el preparcial y las diapositivas
   los usan. Cambiar a `T` (como los caps. 2 y 3) toca todo lo anterior, y el simulacro del M11 es la variante 9 de un quiz ya aplicado.
2. **El M10 sigue en 43 min y 3 560 palabras.** ¿Se acepta, o se parte en dos módulos (el Caso de la TRM, y el puente con el resumen y la evaluación)? Partir
   renumera (D6 lo descarta), así que quedaría para 2027-I si se decide.
3. **La nota de la TRM se fue del M5 al M10**, donde el bloque la respalda. ¿Se prefiere dejarla en el M5 con un aviso («la serie se presenta en el Módulo 10»)?
4. **Los rótulos del selector del M9** contestan la pregunta de su introducción. ¿Entran en la R5 o se dejan?
5. **Los dos meses de devaluación de la TRM** («marzo de 2020, julio de 2022») no salen de un bloque. ¿Se añade una línea a los bloques de R y Python o se
   dejan como dato de contexto?

---

## Guiones y comprobaciones

| Guion | Salida | Qué hace |
|---|---|---|
| `r3_edita.py` + `r3_ediciones_*.py` | — | reaplica sobre `HEAD` las 48 sustituciones; `--comprobar` dice si el árbol coincide |
| `r3_minutos.py` | `r3_minutos_antes.out`, `r3_minutos_antes_herramienta_original.out`, `r3_minutos_despues.out` | minutos medidos antes y después |
| `r3_secciones_m10.py` | `r3_secciones_m10_antes.out`, `…_despues.out` | palabras por sección del M10 |
| `r3_cifras.R` | `r3_cifras.out` | 66 cifras recalculadas en R (0 «NO») |
| `precalculo/verifica_bloques_cap6.py --html …` | `r3_verifica_bloques.out` | **822 de 822 cifras** (antes 762 de 762); 14 bloques de R y 11 de Python (antes 13 y 10); 0 con discrepancias |
| `r3_bloques_python.py` | `r3_bloques_python.out` | los 11 bloques de Python, cada uno solo en una carpeta vacía: todos con código de salida 0; el de la TRM, dos veces (copia de la página y de la carpeta de trabajo). Las cifras con decimales de los comentarios que no salen del bloque citan a R (`R da …`) |
| `precalculo/verifica_todo.py` | `r3_verifica_todo.out` | 11 verificadores en verde |
| `r3_revisa.js` | `r3_revisa.out` | por HTTP (servidor propio en 8764, Chrome sin ventana en 9277, cerrados al acabar), los doce módulos a 1200 y 375 px con derivaciones, pistas y soluciones abiertas: **0 errores o avisos de consola, 0 `.katex-error`, 0 «$» sin componer, ninguna fórmula dentro de `<pre>`, ningún desbordamiento horizontal, 0 simuladores sin pintar (gráficos 1/1, 2/2, 3/3, 2/2, 1/1, 2/2, 3/3, 6/6 en M1, M3…M10), `typeof tailwind` = `undefined`**; el orden de los `h3` del M10; los minutos de `courseData` (11, 7, 14, 9, 6, 10, 10, 11, 14, 43, 40, 3; la barra lateral no los pinta, V10); el cambio de pestaña R/Python del puente |
| `ensambla_cap4.py` dos veces | — | md5 idéntico (`5d041667…`); `ensambla_cap5.py` y `ensambla_cap6.py` no cambian sus HTML |
