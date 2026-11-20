# Cap. 3 · Diagnóstico de ejercicios, autoevaluación y práctica

Archivo: `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` (commit `58bdfc5`, worktree
`course-content-improvement-227f2c`, 2026-11-19). Diagnóstico, sin ediciones en el repo. Las líneas
citadas son las del HTML ensamblado; el capítulo 3 se ensambla desde `ensamblado/cap3/`
(`cap3_modulos.html`, `cap3_js.js`), y cualquier arreglo tiene que ir allí.

Leído: objetivos de los once módulos (2688, 2956, 3279, 3583, 3887, 4431, 4551, 4832, 5162, 5785,
6269), los tres `ejercicio-guiado` (6017, 6088, 6142), `AUTOEVALUACIONES['cap3']` (9125–9338),
`AUTOEVALUACIONES['parcial2']` (9354–9631), el simulacro `SIMULACROS['cap3-simulacro']`
(9818–9944) con su motor (9666), el motor del quiz (7427–7790), los `data-simulador` con su intro
y su JS (2998–5530; 8281–9123) y los 25 bloques `code-tabs`. **Hay 13 `data-simulador`, no 14**
(`grep -c` cuenta 14 líneas porque una es un comentario del JS, 6735): 12 simuladores y el
simulacro. Aparte hay una tabla ordenable (`TABLAS_RANKING['criterios']`, M8) y un ciclo de
cuatro pasos (M5, 3922). Contraste con el texto guía: FPP3 §9.11 (`arima.txt` 1023–1100), §9.3 y
§9.5 (`arima.txt` 202–225, 328) y §5.11 (`toolbox.txt` 1012–1053).

Escala de veredictos (la del cap. 2): **sirve** (publicable con retoques cosméticos) · **se puede
mejorar** (núcleo sano, arreglos puntuales) · **hay que rehacer** (no mide lo que dice medir, se
responde sin entender, o enseña algo incorrecto).

**Lo que se marca aparte.** La actividad `parcial2` (final del M10) y el simulacro del M11 **no se
editan en el HTML**: los escriben `exporta_actividad.py` y `exporta_simulacro.py` desde el banco
del quiz adicional, fuera del repositorio (comentarios en 9341–9352 y 9658–9661). Son las
variantes 1 y 9 de un quiz de Brightspace **ya aplicado**. Todo cambio que se proponga sobre ellos
va marcado **[fuera del repo]** y es una decisión de Javier.

Guiones y salidas (todo en `diagnostico/cap3/diag/`):

| Guion | Qué hace | Salida |
|---|---|---|
| `ejercicios_cap3.R` | reproduce E1–E3, comprueba las claves del quiz `cap3`, las de `parcial2` y calcula las del simulacro (que no trae clave); potencia de Ljung–Box por simulación; fórmula del periodo de FPP3 | `ejercicios_cap3.out` |
| `ejercicios_longitud_opciones.js` | «la más larga / la más corta» sobre el texto visible de los tres instrumentos; posición en el simulacro; tolerancias con la comparación exacta del motor | `ejercicios_longitud_opciones.out` |
| `ejercicios_series_candidatas.R` | series de R base y procesos teóricos medidos para los huecos (§8–§9) | `ejercicios_series_candidatas.out` |
| — | `audita_posicion_correcta.py` sobre el capítulo | `ejercicios_posicion.out` |
| — | `verifica_bloques_cap6.py --html` (R) | `ejercicios_verifica_bloques.out` |
| — | los 11 bloques de Python, ejecutados aparte (el verificador no los contrasta) | `ejercicios_python_salida.out` |

Versiones: R 4.6.0; forecast 9.0.2, tseries 0.10.62. `precalculo/serie.csv`, que deja el
verificador al ejecutar el bloque del M1, se borró (no tiene seguimiento).

---

## 0. Resultado de las ejecuciones

### 0.1 Verificador de bloques

`MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-3-modelos-ar-ma-arma.html`

```
Bloques encontrados: 14 de R, 11 de Python
=== 533 de 534 cifras anunciadas aparecen en la salida real (1 bloques con discrepancias) ===
```

- **534 cifras contrastadas, 533 coinciden.** A diferencia del cap. 2 (0 de 0), aquí los bloques
  de R —también las tres soluciones— llevan la salida bajo `#>`.
- La discrepancia: bloque del M9 (5590), `Box.test(...)$p.value` anuncia `0.1643575` y R 4.6.0 da
  `0.1643997`. Coinciden a cuatro decimales (`0.1644`, que es lo que dice el resto del capítulo:
  5237, 5248, 5715, 6174). Es un cambio de optimizador entre versiones; basta escribir la salida
  real o redondear.
- La sesión encadenada de R termina con código 1 (`Error: write failed` al cerrar el dispositivo
  gráfico en `precalculo/`, donde el entorno no deja escribir `Rplots.pdf`). No afecta a la
  comparación. El `Error in arima.sim(... ar = 1)` es el `try()` deliberado del M6 (4464).
- **Los 14 bloques de R corren solos**, cada uno en una sesión limpia y sin la cabecera del
  verificador (comprobado bloque a bloque).
- **Python no lo contrasta el verificador** (sus cifras van en `# …`, no en `#>`). Ejecutados
  aparte los 11 (`ejercicios_python_salida.out`): todas las cifras coinciden salvo una, el
  pseudo-periodo del M9 en Python (5720), que imprime `11.218` y el comentario dice `11.2178` (lo
  de R). El bloque de Python del M1 **no corre solo**: lee `serie.csv`, que escribe el de R.

### 0.2 Soluciones de los ejercicios

| Ej. | Cifra escrita | Salida real | ¿Coincide? |
|---|---|---|---|
| 1 | banda 0.2829; ACF 0.5755 0.1818 −0.1448…; PACF 0.5755 −0.2234 −0.2269… | idénticas | sí |
| 1 | rejilla de 6 (AICc, BIC, LB(10)) | idéntica | sí |
| 1 | AR(1): φ 0.5739, ee 0.1161, media 2.4133; Shapiro p 0.008349 | idénticas | sí |
| 2 | \|raíces\| 1.5811; ρ = 0.5526, 0.2632; π₁… = −0.6, −0.04, 0.264… | idénticas | sí |
| 3 | cuatro ventanas: φ, \|raíz\|, periodo, LB12 | idénticas | sí |

**Todas las cifras de las tres soluciones son reproducibles.** Los problemas están en lo que se
interpreta (E1, E3) y en dónde aparece ya la respuesta (E2).

### 0.3 Otras comprobaciones medidas

| Qué | Resultado |
|---|---|
| E1: correlogramas de `lh` con 20 rezagos | ACF y PACF fuera **solo en el 1** |
| E1: el MA(2) que gana por AICc | θ = (0.673, 0.375), **t = 5.08 y 2.91**: el coeficiente de mayor orden es significativo |
| E1: teórica frente a muestral (paso 4 del ciclo del M5) | muestral r₂ = 0.182, r₃ = −0.145; AR(1): 0.329, 0.189; MA(2): 0.236, 0 — el MA(2) la reproduce mejor |
| E1: diagnóstico de los dos | LB(10) p 0.405 (AR(1)) frente a 0.849 (MA(2)); Shapiro 0.0083 frente a 0.0264 |
| E1: `auto.arima(lh)` | escalonado (por defecto): **AR(1)**, aunque usa el AICc; con `stepwise = FALSE`: **MA(2)** |
| E3: dos ventanas más | 1700–1769 (n = 70): LB12 p = 0.100, **pasa**; **1889–1988 (n = 100, el mismo n que Yule): LB12 p = 0.0006** |
| E3: si el AR(2) fuera el proceso | rechaza LB(12) al 5 % en **5.7 % (n = 89), 5.5 % (n = 100), 6.0 % (n = 289)** (1000 réplicas por n, φ de la serie completa) |
| E3: movimiento de φ entre 1770–1869 y 1900–1988 | +0.16 y −0.97 errores estándar |
| Q1 | \|raíces\| de 1 − 1.2B + 0.9B² = 1.0541 |
| Q4 | 2(1 + 1.2²) = 4.88; los cinco distractores de la `retroFallo` salen como dice (2.44, 2.88, 2.98, 4.40, 6.29) |
| Q6 | 0.64/0.38 = 1.68, 0.69/0.36 = 1.92, suma 0.05 |
| Q7 | 11.2185; con grados y 2π, 0.196; con los φ crudos (1.4059, −0.7111), 10.74 |
| Q8 | LB12 del AR(2) crudo: 0.04614 con `fitdf = 2`, 0.09957 sin él |
| Q9 | residuos del AR(1): r₁ = 0.5556, **8 de 20 fuera** (1, 3, 4, 5, 6, 9, 10, 11); del AR(2): ninguno fuera, máx. 0.1839 |
| Q10 | (YW − ML)/ee = −1.26, 1.10; σ² 298.96 frente a 229.43 |
| `parcial2`, las 10 claves | correctas (cifras en `ejercicios_cap3.out`) |
| Simulacro, claves calculadas | P1 b+e · P2 a · P3 b · P4 c · P5 d · P6 a · P7 b · P8 c · P9 d · P10 a; **cada ítem tiene exactamente una opción correcta** (o dos, en el P1) |
| Periodo del AR(2) final | fórmula del capítulo 11.2185; **la de FPP3 §9.5 (arima.txt 328) da 11.8364** (y 8.69 frente a 8.00 en el φ = (1, −0.5) de `parcial2`) |

---

## 1. Cobertura: objetivo de módulo × dónde se practica

`parcial2` cubre el cap. 2 y los módulos 3.1–3.4; el simulacro, lo mismo, sin corrección. Se
anotan porque son práctica de verdad para M1–M4, pero están **después** del quiz y de los
ejercicios de M5–M9.

| Mód. | Objetivo declarado (resumen) | Ejercicio | Quiz `cap3` | `parcial2` / simulacro | Simulador | Práctica real |
|---|---|---|---|---|---|---|
| M1 | Escribir un modelo como polinomio en B y leer en sus raíces si es estacionario | — | Q1 | P5 (producto de factores), P6 | — | Raíces → estacionariedad: Q1, P5, P6. **Escribir un modelo con B** (de la recursión al polinomio, con el convenio de signos que el módulo pide vigilar, 2738–2743, 2934–2937): **NADA**; solo el ejemplo resuelto del M9 (5283–5302) |
| M2 | Reconocer un AR(p) por su firma; cuándo es estacionario; **calcular media, varianza y autocorrelaciones** | E3 lo usa (ajuste) | **ninguna con etiqueta 2** (Q7, el periodo, va etiquetada 9) | P6 (triángulo), P7 (μ y c), P10 (Yule–Walker y PACF) | `panel-ar-teorico`, `triangulo-ar2` | ρₖ y μ: solo en `parcial2`. **γ₀ del AR (3076–3103): NADA**. Firma del AR sobre datos: E1 (`lh`) |
| M3 | Reconocer un MA(q) por su firma; invertibilidad y por qué la impone el software | E2 | Q2, Q5 (y Q3, etiquetada 5) | P3, P8 | `panel-ma-teorico`, `rho1-theta-ma1` | **La más cubierta**: y el mismo MA(2) θ = (0.6, 0.4) sale tres veces (simulador, Q3, E2) |
| M4 | AR ↔ MA; manejar los pesos ψ y π | — (E2 calcula π en la solución, sin pedirlo) | Q4 | P9 | `dualidad-psi-pi` | Varianza del pronóstico con ψ: Q4, P9. **Pesos π como pronóstico a un paso (3613–3624): NADA** |
| M5 | Momentos del ARMA y usar la tabla ACF/PACF para proponer (p, q), descubriendo que falla con datos | E1 (`lh`) | Q3, Q6 | — | `laboratorio-arma` (tarea explícita) | Identificar con datos: solo E1. **Momentos del ARMA (γ₀, ρ₁ del ARMA(1,1), 4093–4104): NADA**. «La tabla falla con datos»: solo el laboratorio |
| M6 | Generar procesos de orden conocido; medir cuánto se separa la ACF muestral de la teórica | — | — | — | `teorica-vs-muestral` (semilla fija, sin tarea) | **NADA.** Ni quiz, ni ejercicio. Es el objetivo de FPP3 9.11 ej. 1 y ej. 6 |
| M7 | Los tres estimadores; en qué difieren; cuánto se separan sobre datos reales | — | Q10 (recordar) | P10 (YW a mano) | `manchas-identificacion` (estático) | **Aplicar los tres a otra serie: NADA**. Q10 repite el módulo |
| M8 | Elegir entre candidatos y comprobar los residuales | E1, E3 | Q8, Q9 | — | `diagnostico-residuales`; tabla ordenable | Bien cubierto (Ljung–Box, AICc/BIC). **Comparar criterios con y sin media o con distinto d (4862–4865, 5550–5554): NADA** |
| M9 | Cerrar el caso de las manchas (el problema era la escala) y ver un caso sin nada que modelar | E3 (estabilidad de las ventanas, no la escala) | Q7 (recordar) | — | `manchas-transformada`, `manchas-impulso`, `trm-retornos` | **Transferir ninguna de las dos lecciones** —mirar la escala antes de añadir un parámetro; reconocer que no hay nada que modelar— a una serie nueva: NADA |
| M10 | El AR como antepasado de las redes; cuándo gana el modelo pequeño | — | — | — | — | **NADA** (ni el recuadro de uso crítico de la IA, 5868–5875, que el cap. 2 sí practicaba en su E5) |
| M11 | Ensayo con reloj del quiz de Brightspace | — | — | el simulacro | — | Es práctica por diseño, sin clave |

Reparto del quiz `cap3` por etiqueta `modulo`: M1 1 · M3 2 · M4 1 · M5 2 · M7 1 · M8 2 · M9 1 ·
**M2, M6, M10: 0**. Ejercicios: M5+M8 (E1), M3 (E2), M9/M8 (E3).

**Objetivos sin ninguna práctica dentro del capítulo:** M6 entero; M10 entero; y como
sub-objetivos declarados: escribir un modelo con B (M1), la varianza del AR (M2), los momentos del
ARMA (M5), aplicar los estimadores a otra serie (M7), las dos lecciones del M9 sobre una serie
nueva.

---

## 2. Fichas del quiz (`AUTOEVALUACIONES['cap3']`, 9125–9338)

Motor (7427–7790): en `opcion` y `grafico` el primer fallo deshabilita la opción elegida, muestra
la `pista` y deja reintentar; en `multiple` el primer fallo dice **«De las N que marcaste, X están
en la respuesta, y te faltan Y»** y añade la pista (7721–7727); la numérica acepta `Math.abs(dada −
respuesta) <= tolerancia` (7644). El resumen suma los aciertos al primer y al segundo intento.

**Claves: las diez son correctas** (§0.3).

Las cuatro formas de contestarse solo:

- **(a) Posición** — sana. `audita_posicion_correcta.py`: orden 4 2 4 3 1 en las cinco de una
  sola; reparto 1→1, 2→1, 3→1, 4→2 (40 %, en el límite); racha máxima 1; múltiples en [2, 4, 5] y
  [1, 3, 5], no seguidas.
- **(b) Tamaño** — **la más larga acierta 4 de 5** de una sola respuesta: Q1 (80 frente a ≤ 65),
  Q3 (59 frente a ≤ 55), Q8 (**101 frente a ≤ 63**), Q9 (79 frente a ≤ 73); solo Q6 se libra. En
  la **Q5** (múltiple, tres correctas) **marcar las tres más largas acierta**: 81, 89 y 79 frente a
  44 y 54. En Q10 falla (empate a 96).
- **(c) Pistas** — las diez dan el criterio o el procedimiento (detalle por ficha). Las dos
  múltiples dicen **«Son tres»** y enumeran los tres temas **en el orden de las correctas**
  (9211, 9327), y el motor añade cuántas faltan: el segundo intento es gratuito.
- **(d) Filtraciones** — **la retro de la correcta de Q3 (9183) imprime la solución del E2**:
  «MA(2) con θ = (0.6, 0.4): ρ₁ = 0.5526, ρ₂ = 0.2632 y a partir de ahí exactamente cero». El quiz
  está antes que los ejercicios (5997 frente a 6017). Además, cuatro respuestas están en pantalla
  en el propio capítulo: Q2 (0.4878 en 3561, y en la lectura de `panel-ma-teorico`, cuya opción
  por defecto es justo θ = 0.8), Q7 (11.22 en 5267, 5319, 5477 y en la lectura de
  `manchas-transformada`), Q9 (el gráfico es la opción AR(1) de `diagnostico-residuales`), Q8 (la
  retro repite 4990 y 5082).
- **Recuerdo, no transferencia**: Q2, Q3, Q4, Q7, Q9 y Q10 usan el proceso o la serie de un
  ejemplo resuelto (θ = 0.8; MA(2) θ = (0.6, 0.4); ARMA(1,1) φ = 0.7, θ = 0.5; el AR(2) de las
  manchas). **Cuatro de diez preguntas son sobre las manchas solares.**
- **Tolerancias**: aceptan el redondeo honesto y rechazan el error típico (tabla). La de Q7 tiene
  el borde asimétrico por coma flotante: acepta 11.28 y rechaza 11.16 (\|11.16 − 11.22\| =
  0.0600000000000005); cosmético, porque el valor honesto es 11.2185.

| Q | resp. · tol. | Acepta | Rechaza |
|---|---|---|---|
| Q2 | 0.4878 · 0.0006 | 0.4878, 0.488, 0.4872, 0.4884 | 0.487, 0.49, **0.8** (confundir θ con ρ₁), 0.4444 |
| Q4 | 4.88 · 0.006 | 4.88 | 4.874 y 4.886 (borde, coma flotante), 4.9, **2.44, 2.88, 2.98, 4.40, 6.29** |
| Q7 | 11.22 · 0.06 | 11.22, 11.2, 11.218, 11.28 | 11.16 (borde), 11.3, **0.196** (grados), **10.74** (φ crudos) |

| # | Línea | Tipo · etiqueta | Nivel | Veredicto |
|---|---|---|---|---|
| Q1 | 9127 | opción · M1 | comprender | se puede mejorar |
| Q2 | 9155 | numérica · M3 | aplicar (una fórmula) | **hay que rehacer** |
| Q3 | 9165 | gráfico · M5 | comprender | se puede mejorar |
| Q4 | 9198 | numérica · M4 | aplicar | se puede mejorar |
| Q5 | 9208 | múltiple · M3 | comprender | **hay que rehacer** |
| Q6 | 9223 | opción · M5 | analizar | se puede mejorar |
| Q7 | 9251 | numérica · M9 | recordar (la cifra es la del módulo) | **hay que rehacer** |
| Q8 | 9262 | opción · M8 | comprender | se puede mejorar |
| Q9 | 9290 | gráfico · M8 | comprender (gráfico ya visto) | se puede mejorar |
| Q10 | 9324 | múltiple · M7 | recordar | se puede mejorar |

**Q1 · ¿es estacionario un AR(2) con raíces de módulo 1.054? (9127).** Clave correcta. Buenos
distractores: a) es la confusión «dentro/fuera» de 2839–2842, b) un error de signos real. Pero la
pregunta ya da el módulo de las raíces, así que solo pide recordar la regla; la pista termina en
«¿dentro o fuera del círculo unitario?», que es la regla; la correcta es la más larga (+15).
*Mejora*: dar solo φ(B) y pedir el veredicto (que haya que calcular las raíces o usar el
triángulo), y distractores del mismo cuerpo.

**Q2 · ρ₁ de un MA(1) con θ = 0.8 (9155).** Clave 0.48780, tolerancia bien puesta. Mide una
sustitución; la pista da la fórmula y el primer paso («Calcula primero el denominador: 1 + 0.8²»);
la cifra está escrita en 3561 y en la lectura del simulador del mismo módulo, que arranca en θ =
0.8. *Rehacer*: pedir algo que exija entender la cota o la invertibilidad —p. ej. dado r₁ = 0.45,
los dos θ posibles y cuál devuelve el software (lo hace `parcial2` P8, que llega después)— o un θ
que no aparezca en el módulo.

**Q3 · ACF teórica que se corta en 2 (9165).** Clave correcta; buenos distractores (a y c son
confusiones reales). Defectos: **su retro filtra el E2** (arriba); el gráfico es la opción `ma2` de
`panel-ma-teorico` (3330), con las mismas barras; la pista dice qué contar y «fíjate en cuál de
las dos funciones es la que se corta», que es la regla; la correcta es la más larga por 4. Va
etiquetada M5 aunque es la firma del M3. *Mejora*: otro MA(q) (p. ej. un MA(3)) y quitar las
cifras del E2 de la retro.

**Q4 · Var(e_{T+2}) de un ARMA(1,1) (9198).** Clave 4.88; la `retroFallo` es la mejor del quiz
(diagnostica cinco tropiezos, todos medidos). Pero el proceso es el ejemplo resuelto del M4 (ψ₁ =
1.2 está en la tabla de 3737), y el simulador `dualidad-psi-pi` con φ = 0.7, θ = 0.5 y h = 2 da en
su lectura Σψ² = 2.44. La pista da la fórmula y dice que son dos términos y que ψ₀ = 1. *Mejora*:
otro ARMA(1,1) (p. ej. φ = 0.6, θ = −0.3, §8) y la pista sin la receta.

**Q5 · invertibilidad, múltiple (9208).** Clave correcta. **Se contesta sola dos veces**: marcar
las tres más largas acierta, y la pista dice «Son tres» y enumera los tres temas en el orden de
b, d, e. **Ninguna opción lleva `retro` propio** (9213–9217), contra la regla del motor (7439–7444).
*Rehacer*: retro por opción, opciones del mismo cuerpo, pista sin conteo ni enumeración.

**Q6 · ARMA(1,1) con φ̂ ≈ −θ̂ (9223).** La mejor del quiz: es de analizar, los cuatro
distractores son decisiones que se toman de verdad y la correcta no es la más larga. La pista
pregunta «¿Qué les pasa a φ(B) y θ(B) cuando φ₁ ≈ −θ₁?», que nombra el diagnóstico. La «salida de
`arima()`» (φ̂ = −0.64, ee 0.38; θ̂ = 0.69, ee 0.36) **no sale de ningún generador** (`genera_cap3.R`
y `genera_soluciones.R` no la contienen): es un escenario plausible escrito a mano; sus cocientes
sí son correctos. *Mejora*: pista que pida mirar los ee sin nombrar la cancelación; generar la
salida en R (una semilla) o presentarla como hipotética.

**Q7 · pseudo-periodo de las manchas (9251).** Clave 11.22 y tolerancia que rechaza los dos
errores típicos (grados, φ crudos). Pero φ = (1.4027, −0.6853) es el modelo final del M9 y 11.22 es
la cifra más repetida del capítulo; la pista da √0.6853 = 0.8278 y el cociente. *Rehacer*: otro
AR(2), p. ej. el de `log(lynx)` (φ = (1.3776, −0.7399), periodo 9.78; §8), y la pista solo con
«radianes».

**Q8 · `Box.test` sin `fitdf` (9262).** Clave correcta; b) es un distractor excelente (argumento
bien, dirección mal). Pero la correcta es la más larga por 38 caracteres —es la única con
explicación—, la pista reduce a «¿en qué dirección se equivoca?» (descarta a y d), y la retro
repite las dos cifras del M8. *Mejora*: igualar longitudes y dar a d) un argumento del mismo peso.

**Q9 · ACF de los residuos de un AR(1) (9290).** Clave correcta (r₁ = 0.556 y 8 de 20 fuera,
medido). El gráfico es la opción AR(1) de `diagnostico-residuales` (4937), que el módulo presenta
como «insuficiente sin discusión» (4940): se responde reconociéndolo. La correcta es la más larga
(+6). *Mejora*: residuos de un caso no mostrado y frontera (dos barras moderadas fuera, LB cerca
de 0.05), que es lo que el M8 dice que cuesta (5013–5019).

**Q10 · métodos de estimación, múltiple (9324).** Clave correcta. La pista dice «Son tres» y
enumera los temas en el orden de a, c, e; ninguna opción lleva `retro`; las cifras de la
`retroAcierto` son las del módulo. Es recordar. *Mejora*: retro por opción, pista sin conteo y, mejor,
una pregunta de aplicar (p. ej. qué método dio cuál fila de una tabla nueva).

---

## 3. Fichas de los ejercicios guiados (M10)

Están en el M10, **después** del quiz. La consigna (6013–6015) dice que las cifras salen de
`precalculo/genera_soluciones.R` (existe, 333 ss.). Las tres soluciones llevan `#>` y el
verificador las contrasta.

| # | Línea | Nivel (enunciado / solución) | ¿Dice qué entregar? | Pista | Reproducible | Veredicto |
|---|---|---|---|---|---|---|
| E1 | 6017 | analizar + evaluar / evaluar | sí (orden, ¿coinciden?, diagnóstico) | **contesta una de las tres preguntas** | sí | se puede mejorar |
| E2 | 6088 | aplicar / aplicar | sí | da la fórmula y el giro de la cota | sí | **hay que rehacer** |
| E3 | 6142 | analizar / analizar | sí (tres preguntas) | **adelanta los tres resultados** y orienta hacia una causa falsa | sí | **hay que rehacer** (la discusión) |

**E1 · `lh`: identificar, ajustar, elegir (6017–6086).**
- *Enunciado*: claro; serie corta (n = 48) bien elegida para mostrar que la tabla no decide.
- *Pista (6029–6034)*: dice la banda (bien) y luego «**aquí no lo hacen**, y esa discrepancia es el
  ejercicio»: responde a «¿Coinciden el AICc y el BIC?» antes de que el estudiante ajuste nada.
- *Solución*: cifras exactas. La elección final (AR(1) «por parsimonia») es defendible, pero la
  discusión no aplica los criterios que el propio capítulo da para eso en el M10 (5966–5977) y en
  el paso 4 del ciclo del M5 (4002–4011): el θ₂ del MA(2) es significativo (t = 2.91), la ACF
  teórica del MA(2) reproduce mejor la muestral (r₂ = 0.18: MA(2) 0.24, AR(1) 0.33), y «el mismo
  comportamiento en el diagnóstico» no es exacto (LB p 0.41 frente a 0.85; Shapiro 0.008 frente a
  0.026). Además, el capítulo dice «si buscas pronosticar, AICc» (4857–4858) y la solución, ante el
  pronóstico, remite al cap. 6. Falta el dato que más enseña aquí: **`auto.arima(lh)` elige el
  AR(1) con el AICc** (búsqueda escalonada) **y el MA(2) con `stepwise = FALSE`**.
- *Veredicto*: **se puede mejorar** (pista sin el resultado; discusión con los criterios del M10 y
  el contraste teórica/muestral; la nota de `auto.arima`).

**E2 · MA(2) θ = (0.6, 0.4) (6088–6140).**
- *Enunciado*: claro y con tres preguntas encadenadas.
- *Filtrado tres veces*: (1) `panel-ma-teorico` (M3) tiene ese mismo proceso como opción y su
  lectura da ρ₁ = 0.5526; (2) **la retro de la Q3 del quiz, que va antes, da ρ₁ y ρ₂**; (3) la
  última pregunta (¿vale la cota 0.5?) la contesta el M3 en 3461–3465 («la cota es propia del
  MA(1): en un MA(q) el techo… 0.707 con q = 2»). La pista, además, da la fórmula y pregunta «¿se
  dedujo para un MA cualquiera, o para uno concreto?».
- *Solución*: correcta; calcula los π sin que el enunciado los pida (está bien como extensión).
- *Veredicto*: **hay que rehacer**: otro MA(2) que no esté en el capítulo —p. ej. θ = (0.9, 0.2):
  raíces reales de módulo 2 y 2.5, ρ₁ = 0.5838 > 0.5; o θ = (1.2, 0.5): θ₁ > 1 e invertible, ρ₁ =
  0.6691 (§8)— y preguntar algo que el M3 no resuelva (p. ej. qué MA(1) daría ese r₁, si existe).
  Comprobar antes que no coincida con ninguna variante del banco.

**E3 · AR(2) de √manchas en otras ventanas (6142–6206).**
- *Enunciado*: bueno; pide tres lecturas separadas. La solución añade una ventana que el enunciado
  no pide (1870–1988).
- *Pista (6155–6161)*: «Puede pasar perfectamente que los coeficientes apenas se muevan, que el
  periodo sí lo haga y que el diagnóstico se derrumbe» es **la respuesta entera**; y «¿el modelo es
  peor, o la prueba tiene más con qué detectarlo?» empuja hacia una explicación que los datos no
  sostienen.
- *La discusión enseña una causa falsa.* Atribuye el rechazo de Ljung–Box a que «la prueba gana
  potencia: con n = 289 en vez de 100…». Medido: **1900–1988 tiene n = 89, menos que la ventana de
  Yule, y rechaza (p = 0.0010)**; **1889–1988 tiene n = 100, el mismo, y rechaza (p = 0.0006)**;
  1700–1769 (n = 70) pasa. Y si el AR(2) fuera el proceso, la prueba rechazaría en torno al 5–6 %
  con cualquier n (5.7 %, 5.5 %, 6.0 % simulados): la potencia solo crece contra un modelo mal
  especificado. Lo que separa a las ventanas no es n sino el periodo: el AR(2) en raíz cuadrada
  describe bien los siglos XVIII–XIX y no el XX. La moraleja «no rechazar H₀ nunca es aceptarla» es
  cierta, pero este ejercicio no la ilustra.
- *Resto*: «coeficientes estables» se sostiene (+0.16 y −0.97 ee); «el periodo se acorta un año»,
  también (11.22 → 10.13).
- *Veredicto*: **hay que rehacer la discusión y la pista** (el enunciado sirve).

---

## 4. Simuladores como práctica

| id | Línea (HTML · JS) | Mód. | Controles | Tarea que plantea | Lo que la lectura resuelve |
|---|---|---|---|---|---|
| `panel-ar-teorico` | 3000 · 8281 | M2 | selector de 4 AR | implícita («Fíjate en…») | ρ₁, PACF en p+1 = 0, raíces, periodo. Con `ar2_real` da ρ₁ = 0.7143: **el P10 del simulacro** |
| `triangulo-ar2` | 3039 · 8329 | M2 | φ₁, φ₂ (paso 0.01) | explícita (1.40, −0.69) **con la respuesta** («unos 11 periodos») | las tres desigualdades, el veredicto, el tipo de raíz: **resuelve P6 de `parcial2` y del simulacro** |
| `panel-ma-teorico` | 3330 · 8441 | M3 | selector de 3 MA | implícita | ρ₁: **0.4878 por defecto (Q2)** y 0.5526 con `ma2` (**E2**) |
| `rho1-theta-ma1` | 3366 · 8482 | M3 | θ (paso 0.05) | explícita (θ = 2, θ = 1), con lo que se verá | ρ₁, 1/θ, el σ² equivalente |
| `dualidad-psi-pi` | 3626 · 8611 | M4 | φ, θ, h | explícita en tres pasos; la caja 3647 explica después lo visto | Var(e_h)/σ²: **Q4** (φ 0.7, θ 0.5, h 2) y **P9 de `parcial2`** (φ 0.65, θ 0.40, h 3) |
| `laboratorio-arma` | 4290 · 8677 | M5 | φ₁, φ₂, θ₁, θ₂, T; «Otra realización» | explícita (T = 60 frente a 1000, redundancia) | la distancia media teórica–muestral; **el único con azar** |
| `teorica-vs-muestral` | 4511 · 8770 | M6 | selector de 3 | implícita | rezagos con ACF teórica nula; semilla fija, sin otra realización |
| `manchas-identificacion` | 4571 · 8823 | M7 | ninguno | ninguna | «dentro de la banda, luego p = 2» |
| `diagnostico-residuales` | 4937 · 8849 | M8 | selector de 4 modelos | explícita (AR(1) → AR(2)) y adelanta el resultado (4941) | LB, fuera de banda, Shapiro; el gráfico AR(1) es **la Q9** |
| `manchas-transformada` | 5208 · 8920 | M9 | cruda / raíz | implícita; el pie da el resultado | AICc, LB, periodo |
| `manchas-impulso` | 5429 · 8982 | M9 | h (1–24) | implícita | semiancho y techo |
| `trm-retornos` | 5510 · 9067 | M9 | ninguno | ninguna; el pie da la conclusión | fuera de banda, LB, AICc |
| `cap3-simulacro` | 6296 · 9666 | M11 | marcar, reloj de 30 min, borrar | el examen entero | nada: no hay clave (a propósito) |

Tres de doce son estáticos; nueve tienen controles; seis plantean una tarea explícita, pero **todas
dicen de antemano lo que se va a ver** y ninguno pide predecir antes de mover. El
`laboratorio-arma` es el mejor instrumento de práctica del capítulo (es lo que pide el objetivo del
M6) y no tiene ninguna pregunta asociada. Varias lecturas resuelven ítems: Q2, Q4, Q9, E2, y P6,
P9 y P10 de los instrumentos del M10–M11. Para un ensayo «con lápiz y calculadora» como el que pide
`parcial2` (6228) eso no estorba; para la autoevaluación, sí.

## 5. Bloques de código como práctica

- **14 de R y 11 de Python; 534 cifras de R bajo `#>`, 533 coinciden** (§0.1). Los tres bloques de
  solución están dentro del recuento: a diferencia del cap. 2, aquí las soluciones sí se contrastan
  solas en cada pasada del verificador.
- **Los 14 de R corren solos.** El de Python del M1 depende de `serie.csv`, que escribe el de R:
  no es autónomo en Python.
- Las cifras de Python (`# …`) quedan fuera del verificador: 1 discrepancia de 4.º decimal (§0.1).
- **Ningún bloque lleva un «ahora tú».** El del M6 (4447–4467) es exactamente la herramienta de
  FPP3 9.11 ej. 6 y no se pide modificarlo; el de la rejilla del M8 (5031–5094) es el que haría
  falta para aplicar el M8 a otra serie.
- El modelo de referencia del cap. 2 (un «Para practicar» por módulo, cada bloque ejecutable solo y
  con la salida real bajo `#>`) aquí solo se cumple en lo último: los bloques ya son ejecutables
  solos y con `#>`; falta la práctica por módulo.

## 6. Progresión

- **Toda la práctica escrita está al final.** Del M1 al M9 no hay una sola pregunta de control;
  solo simuladores, que enseñan pero no preguntan. En el M10 van, por este orden: quiz (M1–M9),
  ejercicios (M5–M9), actividad `parcial2` (cap. 2 y M1–M4). **La práctica de M1–M4 llega después
  que la de M5–M9**, y el simulacro del M11 la repite sin corrección.
- **Orden de los ejercicios**: E1 (el más integrador: M5 + M8 sobre datos) va primero; E2 (una
  cuenta del M3) segundo; E3 (M9) tercero. El orden natural sería E2 → E1 → E3.
- **Quiz**: etiquetas 1, 3, 5, 4, 3, 5, 9, 8, 8, 7: recorre el capítulo sin ítems de integración
  y sin M2, M6 ni M10.
- **Integración**: E1 es el único que recorre identificación → ajuste → criterio → diagnóstico
  sobre una serie que el capítulo no resolvió. Ningún ejercicio pide **transformar antes de
  modelar**, que es la conclusión del capítulo (5250–5252, 5498–5501).

## 7. Frente al texto guía (FPP3)

| FPP3 | Tipo de tarea | ¿Equivalente en el cap. 3? |
|---|---|---|
| 9.11 ej. 1 (arima.txt 1025–1031) | ACF de ruido blanco con 36, 360 y 1000 datos: por qué cambian banda y barras | No como ejercicio; el `laboratorio-arma` lo permite (T de 60 a 1000) sin pedirlo |
| 9.11 ej. 4 (1041) | Escribir con el operador B las diferencias elegidas | No; `parcial2` P5 hace lo inverso (desarrollar un producto) |
| 9.11 ej. 6 (1045–1066) | **Simular** AR(1) variando φ, MA(1) variando θ, ARMA(1,1) y un AR(2) no estacionario (φ = (−0.8, 0.3)); comparar | **No**: es el objetivo del M6, y el M6 no tiene práctica. (El AR(2) de FPP3 tiene una raíz de módulo 0.927; `arima.sim` lo rechaza, como el `try()` de 4464) |
| 9.11 ej. 7 b (1068–1075) | Escribir el modelo ajustado con B | No; solo el ejemplo resuelto del M9 (5283–5302) |
| 9.11 ej. 8 (1076–1083) | Transformar (Box–Cox), ajustar, probar otros órdenes, elegir, diagnosticar | Parcial: E1 sin transformación; ninguno con transformación, que es la lección del M9 |
| 5.11 ej. 3 (toolbox.txt 1029) | ¿Parecen ruido blanco los residuos? | Sí: Q9 y E1 |
| 5.11 ej. 6 (1047–1053) | Verdadero o falso sobre residuos (¿normalidad obligatoria?, ¿residuos pequeños = buen pronóstico?) | No |
| §9.5 (arima.txt 328) | Periodo de un AR(2) con raíces complejas | **Otra fórmula**: con el AR(2) final da 11.84 frente a 11.22 del capítulo (§0.3). Un estudiante que contraste la Q7 o el E3 con el texto guía encontrará otro número; el capítulo no lo advierte. Qué mide cada una queda **pendiente** de contrastar en las fuentes (FPP3 no lo explica en el pasaje leído) |

Donde el capítulo va **más allá** que FPP3: los pesos ψ y π con varianza del pronóstico (Q4,
`parcial2` P9), los tres estimadores (FPP3 no tiene ejercicio de esto), la redundancia de
parámetros (Q6). Tipos de tarea ausentes: simular, escribir con B, transformar antes de modelar,
aplicar estimadores a otra serie, y cualquier verdadero/falso sobre residuos.

## 8. Datos

- Módulos, simuladores y quiz giran sobre **procesos teóricos de ejemplo** y las **manchas solares
  1770–1869**; el M9 añade la **TRM**; los ejercicios, `lh` y otras ventanas de las manchas. Los
  procesos de ejemplo se reciclan en la práctica: MA(1) θ = 0.8 (M3, Q2); MA(2) θ = (0.6, 0.4) (M3,
  Q3, E2); ARMA(1,1) φ = 0.7, θ = 0.5 (M4, M5, M6, Q4); AR(2) φ = (0.5, 0.3) (M2, simulacro P10).

Medido aquí (`ejercicios_series_candidatas.out`), con dónde convendría cada uno:

| Serie / proceso | Medido | Dónde |
|---|---|---|
| `log(lynx)` (114) | PACF fuera en 1, 2 (y 4, 7, 10, 11); AR(2) el mejor por AICc y BIC; φ = (1.3776, −0.7399), periodo **9.78**; LB10 p = 0.025 (no pasa del todo). Cruda: AICc → ARMA(2,2), BIC → AR(2), LB10 del AR(2) p = 0.012; Guerrero λ = 0.15 | M9: transferir «la escala antes que el parámetro», con un final honesto (no queda limpio). Q7 con otros φ. M7: YW−ML = −0.44 y 0.32 ee (menos que en las manchas) |
| `LakeHuron` (98) | ACF decae; PACF fuera en 1, 2: la tabla propone AR(2); **gana ARMA(1,1) por AICc y por BIC** | M5: «la tabla propone, los criterios deciden» |
| `Nile` (100) | PACF fuera solo en 1 (parece AR(1)); **gana ARMA(1,1)** por AICc y BIC | M5, mismo propósito; serie de un solo vistazo |
| `diff(WWWusage)` (99) | PACF fuera en 1–3; AICc → AR(3), BIC → ARMA(1,1) | M8: AICc y BIC discrepan con una lectura de PACF limpia |
| `diff(Nile)` (99) | r₁ = −0.402; MA(1) θ = −0.76 | M3 / enlace con `parcial2` P3 (diferenciar de más deja un MA negativo) |
| rendimientos del DAX (`EuStockMarkets`, 1859) | nivel: 2 de 20 fuera, LB10 p = 0.78, el ruido blanco tiene el menor AICc; **cuadrados: LB12 p ≈ 0** | M9 caso 2: «nada que modelar» en otra serie, y la frase de 5559–5561 sobre datos diarios, comprobada |
| ruido blanco, 20 rezagos | barras fuera: media 0.51 / 0.85 / 0.96 con n = 50 / 200 / 1000; P(≥ 2) = 0.10 / 0.22 / 0.24 | M6: la regla del 5 % (4529–4532) y la opción b) de Q9 |
| AR(2) φ = (1.2, −0.5) | raíces complejas, \|B\| = 1.414; ρ = 0.8, 0.46, 0.152; γ₀/σ² = 3.7037; PACF 0.8, −0.5, 0 | M2: momentos a mano (γ₀, que nadie practica) |
| ARMA(1,1) φ = 0.6, θ = −0.3 | ρ₁ = 0.337; γ₀/σ² = 1.1406; ψ = 0.3, 0.18, 0.108 | M5 (momentos) y Q4 con otro proceso |
| MA(2) θ = (0.9, 0.2) · (1.2, 0.5) | ρ₁ = 0.5838 · 0.6691; invertibles (\|B\| 2 y 2.5 · 1.414) | E2 sin filtración |

(Todos los procesos propuestos deben cotejarse con las ocho variantes del banco del quiz adicional
antes de usarse: la lección del 16 sep fue que una variante no debe coincidir con un ejemplo
resuelto.)

## 9. Lista de huecos (por prioridad)

1. **M6 — cero práctica.** Un ejercicio corto tipo FPP3 9.11 ej. 6 + ej. 1: predecir y luego
   simular AR(1) con φ ∈ {0.3, 0.9, −0.7}, MA(1), ARMA(1,1) y ruido blanco con n = 50, 200 y 1000;
   contar barras fuera (≈ 1 de 20; P(≥ 2) ≈ 0.2, medido). Sobre el bloque del M6, como «ahora tú».
2. **E3: la discusión enseña una causa falsa** (potencia frente a periodo; §3). Rehacer pista y
   discusión, añadiendo la ventana 1889–1988 (n = 100, rechaza) como contraejemplo.
3. **Filtraciones y recuerdo en el quiz**: la retro de Q3 da el E2; Q2, Q7 y Q9 están en pantalla;
   Q4 usa el ejemplo resuelto. Rehacer Q2 y Q7 con procesos nuevos (Q7 con `log(lynx)`); cambiar el
   proceso de Q4 (φ = 0.6, θ = −0.3); E2 con otro MA(2).
4. **Tamaño y pistas del quiz**: la más larga acierta 4 de 5 y en Q5 las tres más largas son las
   tres correctas; las dos múltiples dicen «Son tres» y enumeran en orden; Q5 y Q10 sin `retro` por
   opción. Igualar cuerpos de las opciones (dar matiz a los distractores) y reescribir las diez
   pistas para que digan por dónde entrar.
5. **M9 — transferir las dos lecciones del capítulo** a series nuevas: un ejercicio con
   `log(lynx)` (¿transformar cambia el modelo elegido?, con resultado no limpio) y uno corto con
   los rendimientos del DAX (nivel ruido blanco, cuadrados no).
6. **M5 — identificar con datos y momentos del ARMA**: un ejercicio corto con `LakeHuron` o `Nile`
   (la tabla propone AR, ganan ARMA(1,1)); una cuenta a mano de ρ₁ y γ₀ de un ARMA(1,1) nuevo.
7. **M7 — aplicar los tres estimadores a otra serie** (`log(lynx)`: YW−ML 0.44/0.32 ee frente a
   1.26/1.10 en las manchas: ¿por qué menos?). Uno corto.
8. **M2 — la varianza del AR** (γ₀) y una pregunta etiquetada M2: un ejercicio a mano con φ = (1.2,
   −0.5).
9. **M1 — escribir con B** un modelo ajustado y leer sus raíces (FPP3 9.11 ej. 7b), con la trampa
   de signos del M1 (2738–2743). Uno corto.
10. **E1**: pista sin el resultado; discusión con los criterios del M10 (θ₂ significativo,
    teórica frente a muestral) y la nota de `auto.arima` escalonado/no escalonado.
11. **Práctica intermedia**: un «Para practicar» al final de cada módulo, como en el cap. 2, y
    mover hacia los M1–M4 la práctica de esos módulos (hoy llega en `parcial2`, al final).
12. **M10 — uso crítico de la IA**: un ejercicio que dé una interpretación de una salida de
    `arima()` con los cuatro errores de 5870–5874 para que el estudiante los encuentre. Baja.
13. **Cosmético**: tolerancia de Q7 (borde asimétrico por coma flotante; p. ej. 0.065); `0.1643575`
    → salida real en 5590; comentario de Python `11.2178` → `11.218` (5720); salida de Q6 generada
    en R; advertir de la fórmula del periodo de FPP3 §9.5.

**Cuántos ejercicios cortos propondría: siete**, todos sobre series de R base o procesos
teóricos ya medidos: M6 (simulación, procesos propios + ruido blanco), M9 (`log(lynx)`), M9
(rendimientos del DAX), M5 (`LakeHuron` o `Nile`), M7 (`log(lynx)`), M2 (AR(2) φ = (1.2, −0.5) a
mano), M1 (escribir con B el AR(2) de `log(lynx)`). Más rehacer E2 y la discusión de E3, y cinco
ítems del quiz (Q2, Q4, Q5, Q7 y la retro de Q3).

### 9 bis. [fuera del repo] Actividad `parcial2` y simulacro del M11

Son las variantes 1 y 9 del quiz adicional, ya aplicado; se generan desde el banco. Lo que sigue es
diagnóstico; cualquier cambio es decisión de Javier y se hace en el banco.

**`parcial2` (9354–9631) — sirve.** Las diez claves son correctas (medido). Todas las opciones
llevan `retro`, con la referencia al módulo. Diseño 2×2 en P4, P5, P6 y P10 (cada rasgo en dos
opciones), que neutraliza la mayoría. Posición: 4 1 2 3 2 1 2 3 4, sin rachas. Tamaño: la más larga
acierta **0 de 9**; la más corta, 1 (P2, 142 frente a 154–170). Lo mejorable: **seis pistas dan el
criterio** (P2 «compara los rezagos… con el periodo», P5 «basta una que no caiga fuera», P6
«\|φ\| < 1 es la condición del AR(1), no la del AR(2)», P7 «el `intercept` no es la constante», P8
«¿cuál de las dos toma el convenio?», P10 «¿cuánto vale ρ₋₁?… ¿en qué rezago se corta?»); y dos
ítems los resuelve un simulador del capítulo (P6 con `triangulo-ar2`, P9 con `dualidad-psi-pi`).

**Simulacro M11 (9818–9944) — se puede mejorar.** Sin clave por diseño (la página lo explica,
6289–6293), y la variante 1 con retro está en el M10 con las mismas plantillas: es una buena pareja.
Lo que medí, con las claves calculadas en R:
- **(a) La correcta recorre las posiciones en ciclo: 1 2 3 4 1 2 3 4 1** en los nueve ítems de una
  sola respuesta (P2–P10). El auditor no lo ve porque el simulacro no tiene `correcta`. Si el banco
  asigna la posición así en todas las variantes, el patrón es transferible a Brightspace; conviene
  comprobarlo en el banco.
- **(b)** La correcta es la más corta en P2 (142 frente a 154–170), igual que en la variante 1: el
  tamaño es de la plantilla, no de la variante.
- **(d)** **El P10 usa φ = (0.5, 0.3), el ejemplo resuelto del M2**: ρ₁ = 0.7143 y ρ₂ = 0.6571
  están en 3189 y 3206, la PACF 0.3, 0, 0 en 3209, y `panel-ar-teorico` lo trae como opción. Es lo
  que la lección del 16 sep pedía evitar.
