---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-04 Modelos ARIMA y Box-Jenkins]]"
fecha: 2026-10-27
estado: ejecutado
---

# Plan — Auditoría de las diapositivas del Capítulo 4

**Objetivo:** dejar por escrito qué se encontró al validar las diapositivas del Capítulo 4, qué se
corrigió, con qué evidencia, y qué sigue abierto, tanto en las diapositivas como en el capítulo del
que salen.

**Alcance:** la presentación `Htmls_Series/diapositivas/capitulo-4-modelos-arima.html`, su fuente
`fuentes/capitulo_4.md`, las gráficas de `fuentes/recursos/cap4/`, las notas del presentador y el
verificador de `fuentes/verificacion/`. **No** es la auditoría del capítulo: esa es
[[PLAN_Auditoria_Cap4]], que no menciona las diapositivas.

**Procedencia de este plan.** Se escribe el 2026-10-27, casi un mes después de la ronda (2026-09-29),
y no existía un registro previo de ella más allá de los mensajes de commit y de
`verificacion_cifras.md`. Está reconstruido de tres fuentes: los commits `fd92bd1`, `0856e22` y
`c3239a4`; el diff del texto de las diapositivas entre la primera versión (`90930b3`) y la actual; y
las comprobaciones que se repitieron el 2026-10-27 (sección 2). La sección 4 añade, además, lo que
consta de la sesión que produjo la primera versión. Donde esas fuentes no dicen quién decidió algo o
por qué, aquí tampoco se dice.

## 1. El hueco

**Estado general.** La primera versión (47 diapositivas; commits `c7f717d`, `14f33e8` y `90930b3`,
2026-09-29) se entregó con un verificador de 412 cifras y afirmaciones y «0 discrepancias». Esa
cifra era cierta y aun así engañosa: el verificador comprobaba que **cada cifra de la diapositiva
coincidiera con su fuente**, no que **la diapositiva dijera lo que la fuente permite decir**. La
validación posterior, el mismo día, encontró dos cifras mal, varias afirmaciones de más y varias
imprecisiones, sin cambiar la estructura del material. Todo lo que sigue sale de esa validación.

### Gravedad alta (errores que un estudiante puede ver o aprender mal)

| # | Dónde | Qué fallaba | Verificado |
|---|---|---|---|
| H1 | M10, «Sobre la TRM, las cuatro pruebas…» | ADF $p = 0.586$ y KPSS(∇) $= 0.242$ eran un **doble redondeo**: el JSON guarda 0.5855 y 0.2415 y se redondearon otra vez. Los exactos son 0.58549 y 0.24147, es decir **0.585 y 0.241**. El capítulo traía las mismas dos cifras | R 4.6: `directo_r46_cap4.json` (`trm.adf_nivel_p`, `trm.kpss_d1_stat`) |
| H2 | M7, «Cinco modelos quedan a 1.71 puntos» | Con la regla de 2 puntos son **siete**: faltaban el ARIMA(2,1,1), a 1.81, y el ARIMA(1,1,2), a 1.84. El JSON guarda solo los cinco primeros del ranking y la primera versión se verificó contra esa lista truncada. El capítulo y su autoevaluación también se detienen en el quinto | R 4.6: 7 de los 42 modelos evaluados a menos de 2 puntos |
| H3 | M8, título «un escalón en 1899 explica más que una raíz unitaria» | Los ≈ 25 puntos de AICc comparan el escalón con el **mejor ARMA** ($d = 0$), no con la raíz unitaria: contra el ARIMA(1,1,1) no son comparables (lo dice el propio módulo). Título nuevo: «El escalón de 1899 ajusta casi 25 puntos de AICc mejor que cualquier ARMA del Nilo», seguido de una pregunta fuera de muestra | $1282.50 - 1257.91 = 24.59$ (J) |
| H4 | M10, «A dos años, el intervalo del 95 % abarca un tercio del nivel» | Al acortar el título para que cupiera se perdió «hacia cada lado»: el **semiancho** es un tercio del nivel (33.4 %); el intervalo entero, de 2330.70 a 4663.48, abarca dos tercios | $1166.39 / 3497.09$ |
| H5 | M10, «La TRM es una caminata aleatoria» | Afirmaba más de lo que el diagnóstico permite: pasa a «**compatible con** una caminata aleatoria» | interpretación; el diagnóstico no la rechaza |
| H6 | M10, «búsqueda exhaustiva sobre 192 modelos» | Son 150 con parte estacional y 42 sin ella | R 4.6 (`trm.auto.*`) |
| H7 | M10, puente al Capítulo 5, «el mejor no estacional es un ARIMA(0,1,5)» | Lo es con $p + q \le 5$, el tope por defecto de `auto.arima`. Con una búsqueda más amplia gana el ARIMA(8,1,3) con deriva y $\hat\rho_{12}$ sigue siendo grande (0.437). El «haría falta $q = 24$» del capítulo no se reprodujo | R 4.6 (`puente.*`) |

### Gravedad media (precisión)

| # | Dónde | Qué fallaba | Verificado |
|---|---|---|---|
| H8 | M4, PACF de ∇Nilo | Mostraba −0.402, −0.246, −0.119… y decía que decae. La PACF sale de la banda en los rezagos **1, 2, 7 y 10**, todos negativos. [[PLAN_Auditoria_Cap4]] ya daba «4 de 20» y no se usó. Se añade la banda de Bartlett (±0.227 para $k > 1$) y se dice que el eje de la foto se recortó a ±0.45 | J (`identificacion.d1.pacf`); cálculo |
| H9 | M4, ACF sin diferenciar | «Retrato de una serie no estacionaria» → «compatible con» (o con un escalón); «veinte rezagos sin acercarse a cero» → «los veinte rezagos positivos y 11 fuera de la banda» | J (`identificacion.cruda.acf`) |
| H10 | M3, `ndiffs` y notas | «ADF y PP tienen potencias distintas» era impreciso. Simulando el ARIMA(1,1,1) con raíz unitaria verdadera (1 000 réplicas, semilla 2026), `PP.test` rechaza el 100 % y `adf.test` ($k = 4$) el 51.3 %: con un MA fuerte y negativo ($\hat\theta \approx -0.87$) el PP rechaza casi siempre y su −6.690 apenas informa | R 4.6 (`sim_raiz_unitaria`) |
| H11 | M1, raíz de 1/φ̂ | 3.9308 → **3.93**: venía de $\hat\phi$ redondeado a 4 decimales | R |
| H12 | M1, Holt y suavizamiento | «Equivale» → «**incluye**»: Holt es un caso particular del IMA(2,2), con restricciones sobre los coeficientes. $\alpha = 1 + \theta$ vale con el signo de R y $-1 < \theta < 0$ | razonamiento en las notas; sin cifra |
| H13 | M2, título | «Box y Jenkins aportaron el método, no el modelo» → «La aportación de Box y Jenkins fue el método»: también sistematizaron el ARIMA y la identificación con ACF/PACF | notas |
| H14 | M2 y M1, referencias | **1970** (Box y Jenkins) pasa de `[SIN VERIFICAR]` a comprobado a mano en Shumway y Stoffer (PDF, pp. 8, 15 y 75). **Reinsel (1994)** en lugar de 1976: la ayuda de `?AirPassengers` cita 1976 en R 4.3.3 y 1994 en R 4.6, y 1976 era un anacronismo (Reinsel entró en la tercera edición). Signo de θ: Cryer y Chan §4.2 (PDF p. 70) y Tsay (PDF p. 87) usan el menos; el de Box y Jenkins sigue sin comprobar | comprobación **manual** (clase `MAN`); R 4.6 (`doc.airpassengers`) |
| H15 | M5, deriva del Nilo | «El descenso de 247.8 aporta −2.50» → condicional («si el escalón fuera la única caída, aportaría −2.50 a esa media») | $-247.78 / 99$ |
| H16 | M5, nombres y valores por defecto | Lo que R devuelve como `intercept` o `drift`, y statsmodels como `const` o `x1`, es $\mu_w$, no $c$ ($c = \mu_w\,\phi(1)$). La tabla añade `include.mean = TRUE` (con $d = 0$) en `Arima` | R 4.6 (`Arima.include_*`) |
| H17 | M7, regla de 1.01 y raíz AR | Lo que se pone a ∞ es el criterio de selección, no el AICc del ajuste, y se aplica a las raíces del ARMA, no a las $d$ unitarias impuestas. La raíz AR del ARIMA(2,1,2) del Nilo es 1.0009 con y sin deriva en R 4.6 (1.0008 y 1.0005 en R 4.3.3): depende del optimizador, y con `arima(method = "ML")` sale 2.24 | R 4.3.3 y R 4.6 |
| H18 | M8, sobrediferenciación | «Firma exacta» → «firma **algebraica**»: $\nabla^2 y_t = \varepsilon_t - \varepsilon_{t-1}$ es exacta solo si $\nabla y$ es ruido blanco; con $\hat\rho_1 = -0.626$ o $-0.719$, $\hat\theta = -1$ es además la frontera del MA(1), porque $\lvert\rho_1\rvert \le 0.5$ | razonamiento en las notas |
| H19 | M9, forma e intervalo | «El intervalo ancho con $d = 2$ delata al $d$ equivocado» → «un intervalo más ancho no delata por sí solo un $d$ equivocado: es el precio de imponer una raíz más; aquí no se justifica porque $\hat\theta = -1$». El 3.5 es frente al ARIMA(1,1,1) sin constante (2771/781 = 3.55); frente al de deriva es 3.9 | J (`forma_medida`) |
| H20 | M9, «cancelar» y $\sigma_h/\sigma\sqrt h$ | «Cancelar» es una raíz unitaria exacta en el MA, $\theta(1) = 0$; con un $\hat\theta$ cercano a −1, como el del Nilo, solo cambia la constante de $\sigma_h$, no su ritmo. El cociente tiende a $\psi_\infty$ y a $h = 30$ todavía no llega | razonamiento en las notas |
| H21 | M4 y M8, matices menores | El AICc que prefiere el (1,1,1) por 1.71 es «menos de 2: no distingue»; KPSS y ADF del lince dan $p > 0.10$ y $p < 0.01$ (son las cotas de la tabla de `tseries`) | R |

### Gravedad baja (figuras y estructura)

| # | Qué | Detalle |
|---|---|---|
| F1 | Fotos de simuladores | Las nueve se recapturan con tipografía legible al proyectarlas (misma serie de datos) |
| F2 | ACF y PACF | Pasan a una sola figura (`m4-2-3.png`), con el eje $y$ recortado a ±0.45 para que se distingan las barras que salen de la banda (el simulador y el capítulo usan ±1; se dice en las notas) |
| F3 | Forma del pronóstico | Pasa de una tabla a cuatro paneles con $h = 30$ (`m9-1x.png`), en diapositiva propia **antes** de la tabla |
| F4 | Gráfica del KPSS | Entra dentro de la respuesta de la pregunta, «en lugar de regalarla» |
| F5 | Código proyectado | Resaltado corregido: `{resaltar=2,3-4,6,8}` |

| # | Estructura | Detalle |
|---|---|---|
| E1 | Leyenda | Pierde su divisor y va antes de la primera sección |
| E2 | «Tres series» | Entra en M1–2, justo antes del primer ejemplo con datos, y pierde la columna «Por qué importa» |
| E3 | Preguntas nuevas | Raíz MA de módulo 1 (¿se sube o se baja $d$?), escalón fuera de muestra, puente estacional |
| E4 | Ideas nuevas | «El diagnóstico manda sobre el criterio» y «"No hay señal" es un resultado» |
| E5 | Lince | Pasa tras el fuera de muestra; sus notas avisan de que se adelanta la respuesta del ejercicio 2 |
| E6 | Cierre | La sección «Fuentes y estado de verificación» ya no se proyecta; la última diapositiva ya no lista lecturas sino «Antes de la próxima sesión» (Módulo 11 y lecturas) y enlaza el informe |

### En las propias diapositivas, sigue abierto

| # | Qué | Por qué sigue abierto |
|---|---|---|
| P1 | Cuatro `[SIN VERIFICAR]`: la presa baja de Asuán como causa del descenso; el signo de θ en el libro original de Box y Jenkins; el origen de la TRM en datos.gov.co; las secciones y capítulos de las lecturas (FPP3 §9.5–9.8, Shumway y Stoffer cap. 3, Box et al. caps. 4–8) | Piden la fuente primaria o el libro. Las notas dan la Presa Baja hacia 1898–1902 como dato plausible no confirmado |
| P2 | Título de Cobb (1978): «conditional solutions» frente a «conditional solution» | `verificacion_cifras.md` lo deja como «comprobarlo». Volumen, número y páginas (*Biometrika* 65(2), 243–251) sí están confirmados en R 4.6 |
| P3 | Las cifras de R 4.6 viven en `directo_r46_cap4.json` | En un equipo con R 4.3.3 no se regeneran; solo se leen. El JSON registra el entorno (R 4.6.0, forecast 9.0.2, tseries 0.10.62) |

### Fuera de las diapositivas: el capítulo conserva lo que las diapositivas corrigieron

Comprobado en `capitulo-4-modelos-arima.html` el 2026-10-27. Las diapositivas no pueden contradecir el
capítulo sin decirlo, así que cada una de estas diferencias está dicha en las notas. Solo se corrigió
el capítulo en H1 (`c3239a4`).

| # | Dónde | Qué dice el capítulo | Frente a |
|---|---|---|---|
| Q1 | M7 | «Cinco modelos en 1.71 puntos de AICc» y «cinco candidatos indistinguibles»; su pregunta de autoevaluación, según las notas, se detiene en el quinto | Siete a menos de 2 puntos (H2) |
| Q2 | M1 | «Equivale al método de Holt» (IMA(2,2)) | «Incluye» (H12) |
| Q3 | M3 | «tienen potencias distintas» (ADF y PP) | H10 |
| Q4 | M10 | «Devuelve un ARIMA(0,1,5)» sin límite de búsqueda; «haría falta un $q = 24$» | H7: con $p + q \le 5$; el $q = 24$ no se reprodujo |
| Q5 | M10 | «La TRM es una caminata aleatoria»; «búsqueda exhaustiva sobre 192 modelos» | H5 y H6 |
| Q6 | M2 | «Su aportación no fue el modelo» | H13 |
| Q7 | Lecturas | El título de Cobb (1978) con «conditional solutions» en plural; el de *Biometrika* parece ser «conditional solution». El `65 (2)` del capítulo sí está confirmado | P2 |
| Q8 | M8 | La tabla rotula $d = 1$ «Mínimo de varianza. Correcto.» | Ya figura en [[PLAN_Auditoria_Cap4]] como pendiente |

## 2. Restricciones verificadas

Comprobadas el 2026-10-27, no copiadas de los commits:

- **El HTML se reproduce desde la fuente.** `construir.py` (skill `diapositivas-clase`) sobre
  `fuentes/capitulo_4.md` da 50 diapositivas, 5 secciones y 43 de contenido, todas con notas, y deja
  `git status` vacío: la versión publicada es la que sale de la fuente.
- **El verificador pasa.** `verifica_cifras_cap4.py`: 445 comprobaciones, 441 verificadas (13 son
  definiciones o convenciones que no se miden), 4 marcadas `[SIN VERIFICAR]`, **0 no coinciden**; el
  código R proyectado se ejecutó (2 bloques, 2/2 salidas). El informe regenerado no cambia.
- **Entre versiones de R.** El JSON publicado (R 4.6) y su regeneración en R 4.3.3: de 3 836 valores,
  13 difieren más de 1.5 unidades del último decimal, todos en modelos mal condicionados (ARIMA(2,1,2) y
  (2,2,2) del Nilo y (2,1,2) de la TRM). Ninguno se muestra.
- **El sitio sirve lo que hay en `main`.** `main` y `gh-pages` tienen el mismo árbol de `Htmls_Series/`
  (`780813e`).
- **No se pudo repetir aquí:** el cálculo en R 4.6 (el equipo de esta comprobación tiene R 4.3.3) y las
  comprobaciones manuales contra libros. Se confía en `directo_r46_cap4.json` y en lo que
  `verificacion_cifras.md` dice de las páginas.

## 3. Decisiones recogidas en `fd92bd1`

El mensaje del commit no dice quién las tomó; se listan tal como quedaron.

- **D1.** Cuando el capítulo se equivoca o se queda corto, la diapositiva dice lo correcto y la nota
  lo explica, en lugar de repetirlo: siete modelos, 0.585 y 0.241, Reinsel (1994), «incluye» para Holt.
- **D2.** Solo se corrigió el capítulo en las dos cifras de H1 (`c3239a4`). El resto de las
  diferencias queda en Q1–Q8 (comprobado el 2026-10-27).
- **D3.** Las comprobaciones manuales contra libros (clase `MAN`) se cuentan aparte, con página, porque
  ningún guion las ejecuta.
- **D4.** El informe calcula «No coinciden» en lugar de escribir 0.
- **D5.** La sección de fuentes deja de proyectarse; el informe sigue enlazado desde la última
  diapositiva.
- **D6.** Los títulos se matizan: «compatible con», «incluye», «hacia cada lado».

## 4. Por qué el primer verificador dejó pasar H1–H7

Es la parte del plan que más sirve para la próxima presentación.

| Fallo | Qué pasó | Qué se añadió o se propone |
|---|---|---|
| Doble redondeo | Un JSON a 4 decimales citado a 3 se redondeó otra vez. El verificador ya sabía de esta trampa (la banda ±0.167) y no la aplicó a H1 | **Hecho:** valores exactos en R 4.6. **Propuesta:** todo valor citado con menos decimales que su JSON se recalcula desde los datos crudos |
| Lista truncada | «Cinco modelos» se comprobó contra un ranking que el JSON ya había cortado en cinco | **Hecho:** ranking completo en R 4.6. **Propuesta:** una afirmación de recuento («cinco», «siete», «cuatro») se verifica contra la lista completa, nunca contra una que ya viene recortada |
| Fuentes que cambian de versión | `?AirPassengers` cita 1976 en R 4.3.3 y 1994 en R 4.6; la raíz del (2,1,2) varía en el cuarto decimal | **Hecho:** el JSON de R 4.6 registra su entorno y el informe nombra las dos versiones |
| Títulos acortados | Para que cupiera, «hacia cada lado» se perdió y el sentido cambió (H4) | **Propuesta:** al acortar un título, releer su nota; un título con cifra se verifica como una cifra |
| «Es» en vez de «compatible con» | Se copió la fuerza de la frase del capítulo (H5, H9) | **Propuesta:** revisar a mano los verbos de las interpretaciones; el guion no los ve |

Lo que el verificador **sí** cubría, y siguió cubriendo bien: cada cifra mostrada coincide con su fuente
(412 de 412 entonces); el código proyectado se ejecuta; una cifra inventada, cambiada o sin respaldo
hace fallar el guion (probado con mutaciones el 2026-09-29).

## 5. Tareas

| T | Qué | Archivos | Estado |
|---|---|---|---|
| T1 | H1: cifras exactas de la TRM, en la diapositiva y en el capítulo | `capitulo_4.md`, `templates_10.html`, capítulo | Hecho (`c3239a4`, `fd92bd1`) |
| T2 | Cálculo exacto en R 4.6 de lo que los JSON no traían | `verifica_directo_r46_cap4.R`, `directo_r46_cap4.json` | Hecho (`0856e22`) |
| T3 | H2–H21: títulos, cifras, notas | `capitulo_4.md` | Hecho (`fd92bd1`) |
| T4 | F1–F5 y E1–E6: gráficas y estructura | `capitulo_4.md`, `recursos/cap4/` | Hecho (`fd92bd1`) |
| T5 | Verificador: fuente R46, clase `MAN`, «No coinciden» calculado | `verifica_cifras_cap4.py`, `verificacion_cifras.md` | Hecho (`fd92bd1`): 445 comprobaciones |
| T6 | Reconstruir y publicar | HTML, `index.html` | Hecho (`fd92bd1`); `gh-pages` al día |
| T7 | Q1–Q8 en el capítulo | `ensamblado/cap4/templates_*.html` y reensamblado | **Pendiente**, decisión de Javier (ver sección 7) |
| T8 | P1–P2 | libros, datos.gov.co | **Pendiente**, requiere las fuentes |
| T9 | Propuestas de la sección 4 en el verificador | `verifica_cifras_cap4.py` | **Pendiente**, sin prioridad fijada |

## 6. Criterios de aceptación

- Ninguna cifra mostrada sin respaldo, y ninguna `[SIN VERIFICAR]` presentada como dato: **cumplido**
  (445 comprobaciones, 0 no coinciden, 4 marcadas).
- Cada diapositiva de contenido con notas y a ≥ 88 % de escala: **cumplido** según `fd92bd1` (50
  diapositivas, 43 de contenido con notas); la escala no se repitió el 2026-10-27, solo la
  reconstrucción.
- El HTML sale de la fuente sin diferencias: **cumplido** el 2026-10-27.
- Las diapositivas no contradicen el capítulo sin decirlo: **cumplido**; lo que difiere está en las
  notas y en Q1–Q8.
- Cero errores de consola y de MathJax en las 50: **no consta** en los commits; la comprobación de la
  primera versión (47 diapositivas, 2026-09-29) no se repitió sobre la actual.

## 7. Riesgos y decisiones abiertas

- **Q1–Q8 en el capítulo.** Mientras el capítulo diga «cinco modelos» y las diapositivas «siete», un
  estudiante que lea los dos verá una contradicción que solo explica la nota del presentador. La
  decisión es suya: corregir el capítulo (y la pregunta de autoevaluación de M7, que tiene la
  respuesta «cinco»), o dejarlo como está y que la clase lo diga. Las correcciones al capítulo pasan
  por `ensamblado/cap4/` y se reensamblan 4 → 5 → 6, como en [[PLAN_Auditoria_Cap4]].
- **Verificar no es auditar.** El verificador comprobó cifras y no la redacción, y H1–H7 aparecieron
  en una segunda lectura. Una tercera, hecha por alguien que no haya visto ni el capítulo ni las
  diapositivas, es la forma de comprobar que no queda un H8.
- **Dependencia de R 4.6.** Quien reconstruya el informe sin R 4.6 lee, no regenera, las cifras de
  H1, H2, H6, H7, H10, H14 y H17.

## 8. Resultado (2026-09-29, documentado el 2026-10-27)

Aplicado H1–H21, F1–F5 y E1–E6 en `fd92bd1`; la herramienta de verificación, en `0856e22`; la cifra
del capítulo, en `c3239a4`.

**Verificado:** el 2026-10-27, la reconstrucción y el verificador (sección 2). El 2026-09-29, según el
mensaje de `fd92bd1`, las 50 diapositivas a ≥ 88 % de escala.

**No aplicado, a propósito:**

- Q1–Q8 en el capítulo (sección 7).
- Cobb: el título en singular o plural queda como «comprobarlo» (P2).

**Pendiente, fuera de esta ronda:** P1, P2, Q1–Q8 (T7), T8 y T9. P3 es una limitación, no una tarea.

## 9. Enlaces

- Precedente: [[PLAN_Auditoria_Cap4]] (la auditoría del capítulo)
- Diapositivas: `Htmls_Series/diapositivas/` y su [README](Htmls_Series/diapositivas/README.md)
- Informe cifra por cifra: `Htmls_Series/diapositivas/fuentes/verificacion/verificacion_cifras.md`
- Commits: `c7f717d`, `14f33e8`, `90930b3` (primera versión); `c3239a4`, `0856e22`, `fd92bd1` (validación)
