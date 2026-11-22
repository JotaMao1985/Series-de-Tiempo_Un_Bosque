# Capítulo 3 · ronda R5 «práctica» · cambios

Fecha: 2026-11-21. Un solo redactor (subagente redactor R5, Fable 5.2). **Sin commits ni push.**
Alcance: T5.1 y T5.2 del plan (`PLAN_Mejora_Cap3.md`), decisión **D9**. Base: `5c2fdb3`.
Fuente: `diagnostico/cap3/ejercicios.md` (del 19 nov, sobre `58bdfc5`), contrastado con el estado
actual, que las rondas R1–R4 cambiaron mucho (§0).

Archivos tocados:

- `ensamblado/cap3/cap3_modulos.html` (4124 → 4775 líneas): ocho bloques `.exercise` nuevos, uno al
  final de los módulos 1, 2, 3, 4, 5, 6, 7 y 9; los ejercicios 1, 2 y 3 del Módulo 10; y dos veces
  «el envolvente» → «la envolvente» en el Módulo 9 (prosa sin marcar e intro de un simulador).
- `ensamblado/cap3/cap3_js.js` (2262 → 2310): `AUTOEVALUACIONES['cap3']` entero y tres cadenas del
  simulador de los pesos ψ («la envolvente»: dos comentarios y la lectura).
- `ensamblado/ensambla_cap3.py`: **solo** los minutos de `courseData.modules` y su comentario (es
  donde viven; la R3 hizo lo mismo).
- `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html`: reensamblado (10 952 → 11 652 líneas; 663 → 721 KB).
- `Htmls_Series/index.html` y `Htmls_Series/README.md`: «32 ejercicios» → «40 ejercicios» (lo exige
  `cuenta_sitio.py`: el capítulo pasa de 3 a 11).
- `diagnostico/cap3/comprobaciones/r5_*`: guiones y salidas (lista en §8).

No se tocó: `AUTOEVALUACIONES['parcial2']` (la «Práctica de repaso»), el simulacro del Módulo 11, el
motor del quiz, el de los ejercicios, el CSS, los simuladores (salvo las tres cadenas dichas), los
capítulos 1, 2 y 4 a 6, `precalculo/`, `bibliografia/`. **Ninguna frase con `data-afirma` cambió y no
se añadió ninguna** (§6).

**Cómo está hecha la edición.** `r5_edita.py` parte de `git show 5c2fdb3:…` y aplica cinco pasos
(`r5_ediciones_cortos.py`, `_m10.py`, la lista `NOTACION`, `_quiz.py`, `_minutos.py`): es
reejecutable, y dos pasadas dan los mismos md5. El código de las soluciones **no está escrito en los
guiones de edición**: cada bloque vive en `r5_bloques/<id>.R`, `r5_reprex.R` lo ejecuta y escribe
cada salida real bajo su línea tras `#> ` (`r5_bloques/<id>.out`), y eso es lo que se pega. Las
cifras de prosa, pistas, retros y claves que no salen bajo un `#>` del capítulo están en
`r5_cifras.out`, con etiqueta (`[M3-03]`, `[Q6-01]`…); abajo se cita la de cada una.

---

## 0 · Lo que ya estaba arreglado al empezar

| Hallazgo del diagnóstico (`ejercicios.md`) | Estado en `5c2fdb3` |
|---|---|
| §0.1 · 533 de 534 cifras (`0.1643575`) | Resuelto por la R1. Al empezar la ronda, 733 de 733; ahora 1087 de 1087 |
| §0.1 · el bloque de Python del M1 no corre solo (`serie.csv`) y el comentario `11.2178` | Resueltos antes (R1/R3): hoy los 35 bloques corren solos (`r5_bloques_sueltos.out`) |
| §3 · E3: la discusión atribuye el rechazo a la potencia | Resuelto por la R1 (ventana 1889–1988, las 190 ventanas). Quedaban el enunciado, que no pedía las ventanas que la solución usa, y la pista, que seguía adelantando los tres resultados: hechos ahora |
| §7 · la otra fórmula del periodo (FPP3 §9.5) sin advertir | Resuelto por la R1 (nota del M9). La P7 nueva la usa como tropiezo diagnosticado |
| §2 · «ciclo solar documentado por los astrónomos» (retro de la P7) | La prosa lo corrigió en la R4; la cadena del quiz desaparece al rehacer la P7 |
| §4 · `aria-label` de los simuladores que regalaban ítems | Resuelto por la R2 |
| §9.13 · tolerancia de la P7 con borde asimétrico | Desaparece: la P7 es otra pregunta, con tolerancia 0.006 |
| §9.13 · la salida de la P6 no salía de ningún generador | Hecho ahora: es una salida real (`[Q6-01]`) |
| Ninguna cita marcada | La R4 marcó seis fragmentos dentro de los ejercicios 1 a 3; se conservan byte a byte |
| §6 · «periodo», `n`, «identificado», «el envolvente» (restos de la R3) | Hechos ahora, salvo `n` en el ejercicio 3 (§7) |

Lo demás del diagnóstico seguía vigente: ninguna práctica antes del M10; la más larga acierta 4 de 5;
en la P5 las tres más largas son las correctas; las diez pistas dan el criterio; la retro de la P3 da
el ejercicio 2; P2, P4 y P7 sobre procesos resueltos en pantalla.

---

## 1 · T5.1 · Ocho ejercicios cortos «Para practicar»

Uno al final de cada módulo sin práctica propia —**M1, M2, M3, M4, M5, M6, M7 y M9**—, justo antes
de la lista de fuentes del módulo. La forma es la del capítulo 2: un `<div class="exercise">`
titulado «Para practicar» con un `.ejercicio-guiado` —enunciado, entregables en lista con letras,
una pista y una solución con código y lectura—. Van sin número, para no chocar con los ejercicios
1 a 3 del M10. **Ninguna clase nueva de Tailwind, ninguna regla CSS nueva y ningún cambio en el motor.**

**Series.** Antes de elegir se buscó con `grep -lw` cada serie temporal de `datasets` en los seis
capítulos (el resultado está en la cabecera de `r5_explora.R`): quedan fuera
las del plan (`EuStockMarkets`, `discoveries`, `LakeHuron`, `nhtemp`, `JohnsonJohnson`,
`UKDriverDeaths`, `co2`, `USAccDeaths`, `UKgas`), las del capítulo 1 (`AirPassengers`, `nottem`,
`mdeaths`, `sunspots`), las del propio capítulo (`sunspot.year`, `lh`, la TRM) y, por no pisar el
capítulo 4, `Nile` y `BJsales`. Se usan **`WWWusage`** (M5), **`treering`** (M7) y **`lynx`** (M9;
ver §7.1), y procesos teóricos o simulados con semilla en M1, M2, M3, M4 y M6. Sin red. Lo que cada
enunciado dice de su serie se leyó en la ayuda de R (`r5_ayuda_datasets.out`). Cada bloque corre
solo, en proceso nuevo y carpeta vacía (`r5_bloques_sueltos.out`: 35 de 35).

| Mód. | Línea (fuente) | Serie o proceso | Qué practica (hueco del diagnóstico) | Entregables | Palabras: enunciado · todo (sin código) |
|---|---|---|---|---|---|
| M1 | 287 | Dos recursiones: un ARMA(2,1) y un AR(2) con raíz unitaria | Escribir un modelo con $B$, con los dos convenios de signo, y leer sus raíces (hueco 9) | 4 | 107 · 446 |
| M2 | 681 | AR(2) con $\phi = (0.8, -0.6)$, $c = 4$, $\sigma^2 = 3$ | $\mu$, $\rho_k$ y **$\gamma_0$** a mano (hueco 8) | 4 | 87 · 301 |
| M3 | 1086 | Dos MA(1) simulados con los mismos choques, $\theta = 0.5$ y $\theta = 2$ | Qué es la invertibilidad: reconstruir los choques, y qué devuelve el software | 3 | 144 · 448 |
| M4 | 1488 | ARMA(1,1) con $\phi = 0.8$, $\theta = -0.5$; 200 valores simulados | Los pesos $\pi$ como pronóstico a un paso; $\psi$ y varianza (hueco del M4) | 3 | 121 · 349 |
| M5 | 2127 | `diff(WWWusage)`, 99 valores | El ciclo de identificación con datos y la $\rho_1$ de un ARMA(1,1) a mano (hueco 6) | 3 | 145 · 498 |
| M6 | 2341 | Ruido blanco con $T$ = 50, 200 y 1000; MA(1) con $\theta = 0.8$ | Predecir y luego simular cuántas barras caen fuera de la banda (hueco 1) | 3 | 146 · 495 |
| M7 | 2718 | `treering`, 1880–1979 ($T = 100$) | Los tres estimadores sobre otra serie, y por qué aquí coinciden (hueco 7) | 3 | 142 · 491 |
| M9 | 4029 | `lynx`, 114 años | «La escala antes que el parámetro» sobre otra serie, con otro final (hueco 5) | 3 | 128 · 499 |

### 1.1 · M1 — escribir con $B$ y leer las raíces

A: $y_t = 1.1y_{t-1} - 0.3y_{t-2} + \varepsilon_t + 0.4\varepsilon_{t-1}$; B:
$y_t = 1.5y_{t-1} - 0.5y_{t-2} + \varepsilon_t$. (a) los dos polinomios; (b) raíces de A a mano
(discriminante 0.01: 1.667 y 2); (c) la trampa de signos: $1 - 1.1B - 0.3B^2$ tiene una raíz dentro
(0.754), y la del orden en `polyroot()` (salen 0.5 y 0.6); (d) $B$ se factoriza como
$(1-B)(1-0.5B)$: raíz unitaria, y $\nabla y_t$ sigue un AR(1). La pista dice cómo pasar de la
recursión al polinomio, no el resultado. Es la tarea inversa de la P5 de la práctica de repaso
(producto → AR(2)), con otros números.

| Cifra | De dónde |
|---|---|
| Raíces 1.6667 y 2; 0.7540 y −4.4207; 0.5 y 0.6; 1 y 2 | bloque `m1` |
| Discriminante 0.01; $\sqrt{2.41}$; raíz de $\theta(B)$, −2.5 | `[M1-01]`, `[M1-02]`, `[M1-03]` |

### 1.2 · M2 — los momentos de un AR(2)

Números elegidos para que la cuenta salga limpia a mano: $\rho_1 = 0.5$, $\rho_2 = -0.2$,
$\rho_3 = -0.46$, $\gamma_0 = 3/0.48 = 6.25$ por los dos caminos, $\mu = 4/0.8 = 5$ (la trampa de la
constante), pseudo-periodo 6.11. La comprobación por simulación da 5.01 y 6.31. `[M2-01]` a `[M2-06]`.

### 1.3 · M3 — la invertibilidad, con los choques en la mano

El módulo dice (c3-m3-08, sin tocar) que el MA(1) invertible es el único con el que se puede
reconstruir cada choque. El ejercicio lo hace: el error de reconstrucción es
$|\theta|^t|\varepsilon_0|$ —se demuestra restando dos ecuaciones— y la simulación lo enseña
(0.068 → 0.00013 con $\theta = 0.5$; 0.272 → 139 → 143 000 con $\theta = 2$). (c): `arima()` devuelve
$(0.451,\ 4.03)$ y sus residuales, que son ruido blanco, correlacionan 0.451 con $\varepsilon_t$ y
0.778 con $\varepsilon_{t-1}$ (teóricos 0.5 y 0.75, `[M3-03]`). No repite la P8 de la práctica de
repaso (de $\rho_1$ a $\theta$), que llega después.

### 1.4 · M4 — los $\pi$ como pronóstico

$\pi_j = -0.3 \times 0.5^{j-1}$ (todos negativos: con $\theta < 0$ no alternan, a diferencia del
ejemplo del módulo). El pronóstico con cuatro observaciones se hace a mano con valores **dados
redondeados** en el enunciado y el bloque lo calcula con esos mismos valores redondeados (−0.2756),
para que la cuenta a mano y la del código coincidan; con las 200, −0.2933, igual que `predict()` con
los coeficientes fijados. Varianza: 1, 1.09, 1.1476; techo 1.25. `[M4-01]` a `[M4-04]`.

### 1.5 · M5 — el ciclo sobre `diff(WWWusage)`

PACF fuera en 1, 2 y 3; ACF que decae: la tabla propone AR(3). A mano, la $\rho$ del ARMA(1,1)
ajustado y redondeado ($\phi = 0.63$, $\theta = 0.53$): 0.794, 0.500, 0.315, frente a 0.792, 0.520,
0.406. Paso 4: la teórica del AR(3) sigue a la muestral y la del ARMA(1,1), geométrica, se cae desde
el rezago 3. Último párrafo, como adelanto del M8: AICc → AR(3), BIC → ARMA(1,1) por 0.68.
Se descartaron `LakeHuron` (capítulo 2) y `Nile` (capítulo 4), las propuestas del diagnóstico.

### 1.6 · M6 — predecir y después simular

(a) binomial: 1 barra esperada, P(≥ 2) = 0.264. (b) 2000 ruidos blancos por longitud: 0.528, 0.845
y 0.984 barras; P(≥ 2) = 10.4 %, 20.6 % y 24.1 %: la banda es holgada con $T$ pequeña. (c) en los
rezagos 2 a 20 de un MA(1) con $\theta = 0.8$ salen 1.782 barras (0.95 si fuera ruido blanco); con la
banda ensanchada por $\rho_1$, 0.79. `[M6-01]`, `[M6-02]`.

### 1.7 · M7 — los tres estimadores con la misma $T$ que las manchas

En `treering` 1880–1979 los tres coinciden (Yule–Walker a 0.002 y 0.049 errores estándar de ML; en
las manchas, 1.26 y 1.10). $T$ es la misma: lo que cambia es el módulo de las raíces (1.86 y 2.51
frente a 1.19). El apartado (c) lo comprueba con 500 + 500 series simuladas (0.03 y 0.05 frente a
0.66 y 0.57). `[M7-01]`, `[M7-02]`.

### 1.8 · M9 — la lección del caso 1, con otro final

Elasticidad 0.904 (IC 0.542–1.266), mínimo 39, Guerrero 0.152: logaritmo. La rejilla del M8 elige
**lo mismo en las dos escalas** (AR(4) por AICc, AR(2) por BIC). La transformación arregla la
normalidad (Shapiro–Wilk de < 0.0001 a 0.640) y no Ljung–Box (0.031 → 0.013; en logaritmos ninguno
de los once candidatos lo pasa, `[M9-04]`). El ejercicio enseña a no dar por hecho que la historia
de las manchas se repite. `[M9-01]` a `[M9-05]`.

---

## 2 · T5.2 · El quiz

El motor no se tocó. Se rehacen **P2, P4, P5 y P7** con procesos nuevos; las otras seis conservan
asunto y clave, con opciones igualadas, pista nueva y, donde hacía falta, retro corregida.

### Las cuatro formas de contestarse solo

| | Antes (`5c2fdb3`) | Ahora |
|---|---|---|
| **Posición** | orden 4 2 4 3 1 | orden 4 2 4 3 1; múltiples en [2, 4] y [1, 3, 5] (`r5_posicion.out`) |
| **Tamaño** | la más larga acierta **4 de 5** | la más larga acierta **0 de 5**; la más corta, 0 (`r5_longitudes.out`) |
| **Múltiples** | P5: las 3 más largas son las 3 correctas | en ninguna de las dos las más largas (ni las más cortas) son las correctas |
| **Pistas** | las diez dan el criterio; las dos múltiples dicen «Son tres» | las diez dicen por dónde entrar (tabla de abajo) |
| **Filtraciones** | la retro de la P3 da el ejercicio 2; P2, P4 y P7 en pantalla | ninguna respuesta numérica está escrita en el capítulo; ninguna retro da el resultado de un ejercicio |

### Longitud de las opciones (caracteres visibles; ✔ = correcta)

| Ítem | Antes | Ahora |
|---|---|---|
| P1 | 65 · 36 · 33 · **80✔** | 84 · 77 · 82 · 81✔ |
| P3 | 55 · **59✔** · 53 · 38 | 58 · 59✔ · 61 · 59 |
| P6 | 104 · 84 · 85 · 85✔ | 97 · 95 · 91 · 93✔ |
| P8 | 61 · 63 · **101✔** · 52 | 77 · 71 · 77✔ · 79 |
| P9 | **79✔** · 73 · 68 · 67 | 80✔ · 79 · 83 · 82 |
| P5 (múltiple) | 44 · 77✔ · 53 · 86✔ · 79✔ | 63 · 56✔ · 61 · 66✔ · 70 |
| P10 (múltiple) | 96✔ · 83 · 76✔ · 87 · 96✔ | 81✔ · 99 · 83✔ · 81 · 94✔ |

(La medida de «antes» es la de `r5_longitudes.py`, que cuenta el texto visible; la del diagnóstico
difiere en algún carácter por cómo cuenta las fórmulas. El resultado, 4 de 5, es el mismo.)

### Ítem por ítem

**P1 · ¿es estacionario? (M1)** — se conserva. Opciones del mismo cuerpo; las retros, intactas.

**P2 · numérica (M3) — rehecha.** Antes: $\rho_1$ del MA(1) con $\theta = 0.8$ (0.4878, escrito en el
módulo y en la lectura del simulador, que arranca en ese $\theta$). Ahora: $\gamma_1$ del MA(2)
$y_t = \varepsilon_t + 0.6\varepsilon_{t-1} - 0.3\varepsilon_{t-2}$ con $\sigma^2 = 4$. Respuesta
**1.68** (`[Q2-01]`, comprobada con `ARMAacf`, `[Q2-02]`). No es sustituir en una fórmula de una
línea: hay que ver que $y_t$ e $y_{t-1}$ comparten dos choques. Tolerancia 0.006 (aciertan 1.68 y
1,68; fallan 1.7 y 1.69). La `retroFallo` diagnostica 2.40, 0.42, 3.12, 0.29 y −1.20 (`[Q2-03]`).

**P3 · gráfico (M5)** — se conserva el gráfico. La retro de la correcta ya no da
«$\theta = (0.6, 0.4)$: $\rho_1 = 0.5526$, $\rho_2 = 0.2632$» —y el ejercicio 2 ya no es ese
proceso—: explica por qué el corte es exacto. Opciones igualadas; «valores atípicos» sale del
distractor del ruido blanco (era una ACF teórica).

**P4 · numérica (M4) — rehecha.** Antes: $\phi = 0.7$, $\theta = 0.5$, el ejemplo del módulo
($\psi_1 = 1.2$ en la tabla, y el simulador daba 2.44). Ahora: $\phi = 0.6$, $\theta = -0.3$,
$\sigma^2 = 5$, $h = 2$: **5.45** (`[Q4-01]`). El $\theta$ negativo añade un tropiezo diagnosticado
(9.05, perder el signo). Seis cifras en la `retroFallo` (`[Q4-02]`). Distinto de las variantes
visibles del banco (0.65/0.40 y 0.93/−0.12, las dos con $h = 3$).

**P5 · múltiple (M3) — rehecha.** Antes: cinco afirmaciones generales, tres ciertas, sin retro por
opción, con «`arima()` devuelve **siempre** la invertible» y «el modelo no queda identificado».
Ahora, sobre un caso: MA(1) simulado con $\theta = -2.5$, $\sigma^2 = 1$, ajustado con `arima()`.
Dos ciertas (misma $\rho_1$ que $\theta = -0.4$; «con sus opciones por defecto» devolverá
$\hat\theta \approx -0.4$) y tres falsas que son confusiones reales (no estacionario; los $\pi$ se
apagan porque $|\rho_1| < 0.5$; $\hat\sigma^2 \approx 1$). **Cada opción lleva su `retro`**, con
cifras: −0.3448, 2.5, 6.25, 15.625; $\gamma_0 = 7.25$; y la simulación ($-0.405$ y $6.58$,
`[Q5-03]`). «No es identificable», como la convención de la R3.

**P6 · opción (M5)** — se conserva el asunto. La salida es ahora **real**: `set.seed(329)`,
`arima(rnorm(100), order = c(1,0,1), method = "ML")` da $-0.60$ (0.38) y $0.67$ (0.35), sin aviso
de convergencia (`[Q6-01]`), así que el enunciado ya no lo menciona y el distractor del ARMA(2,2)
argumenta con los errores estándar. La retro de la correcta da los cuatro AICc (`[Q6-04]`). Las
retros no dan los cocientes: con los valores redondeados salen 1.58 y 1.91, y sin redondear, 1.57 y
1.94 (`[Q6-02]`, `[Q6-03]`); dicen solo que ninguno llega a 1.96.

**P7 · numérica (ahora etiquetada M2) — rehecha.** Antes: el pseudo-periodo del AR(2) de las
manchas, 11.22, la cifra más repetida del capítulo, con una pista que daba dos pasos de la cuenta.
Ahora: $\phi = (0.9, -0.5)$, **7.13** periodos (`[Q7-01]`). Tolerancia 0.006: aciertan 7.13, 7,13,
7.132 y 7.1317; **falla 7.1**, que no es la precisión pedida, y la `retroFallo` lo dice. Tropiezos
diagnosticados: 0.12 (grados), 13.93 (sin la raíz) y 7.57 (la otra fórmula, la del periodo medio que
el M9 distingue), `[Q7-02]`. Etiqueta `modulo: 2`: la fórmula se enseña en el M2, que no tenía
ninguna pregunta (§7.7).

**P8 · opción (M8)** — se conserva. Opciones igualadas (la correcta era la única con explicación).
La retro del distractor del rezago ya no cita la regla «$h \approx 10$ o $\min(10, T/5)$», que no
está en la prosa ni tenía fuente.

**P9 · gráfico (M8)** — se conserva. Opciones igualadas. Las retros dicen cuántas barras salen
(ocho de veinte, `[Q9-01]`) en lugar de «hay más barras fuera».

**P10 · múltiple (M7)** — se conserva el asunto. **Retro por opción.** «Yule–Walker **solo sirve**
para modelos AR puros» → «estima bastante bien un AR puro y es muy ineficiente si hay parte MA» (la
prosa de c3-m7-06). Las cifras de las retros son las del módulo.

### Las pistas, antes y ahora

| | Antes | Ahora |
|---|---|---|
| P1 | «…¿dentro o fuera del círculo unitario?» | sitúa el módulo respecto del círculo; relee de qué lado, en la definición |
| P2 | daba la fórmula y el denominador | escribe $y_t$ e $y_{t-1}$ con sus choques y marca los comunes; signo y $\sigma^2$ |
| P3 | «cuenta cuántas barras… cuál de las dos funciones es la que se corta» | describe cada función con una frase y busca la fila de la tabla |
| P4 | daba la fórmula, «solo dos términos», $\psi_0 = 1$ | calcula los $\psi$ con la recursión, vigila el signo, decide cuántos entran |
| P5 | «Son tres. Piensa en:» y los tres temas, en orden | separa las dos propiedades y sus polinomios; escribe $\gamma_0$ y $\gamma_1$ y busca el otro par |
| P6 | «¿Qué les pasa a $\phi(B)$ y $\theta(B)$ cuando $\phi_1 \approx -\theta_1$?» | divide cada coeficiente entre su error estándar y súmalos: qué quedó determinado |
| P7 | daba $\sqrt{0.6853} = 0.8278$ y el cociente | dónde está la fórmula; por partes; radianes |
| P8 | «¿En qué dirección se equivoca?» | escribe los dos grados de libertad y mira qué le pasa al $p$-valor |
| P9 | «¿pico aislado y pequeño… o estructura de verdad?» | mide: cuántas barras, en qué rezagos, cuántas veces la banda; compara con el M6 |
| P10 | «Son tres. Piensa en:» y los tres temas, en orden | localiza en el módulo la frase o la cifra que respalda o desmiente cada una |

En las de varias respuestas el motor sigue diciendo cuántas faltan tras el primer fallo (§7).

---

## 3 · T5.2 · Los ejercicios 1, 2 y 3

| Ej. | Qué había | Qué queda |
|---|---|---|
| **1 · `lh`** | La pista contestaba una pregunta («aquí no lo hacen»); la discusión elegía el AR(1) «por parsimonia» diciendo «el mismo comportamiento en el diagnóstico»; `n` | Pista sin el resultado, que remite a la lista «Qué confirma el orden elegido». La solución gana cuatro salidas: $\hat\theta_2 = 0.375$ con $t = 2.91$; la ACF teórica de los dos finalistas frente a la muestral (0.329 y 0.235 frente a $r_2 = 0.182$); Shapiro–Wilk de los dos (0.0083 y 0.0264); y `auto.arima(lh)`, que devuelve el AR(1) por pasos y el MA(2) con la búsqueda exhaustiva. La discusión pone lo que pesa en cada lado y no cierra en falso: BIC/identificar → AR(1); AICc/pronosticar → MA(2). $T = 48$ en la prosa. El enunciado no cambia (lleva c3-m10-31) |
| **2 · MA(2)** | $\theta = (0.6, 0.4)$: opción del simulador del M3 y, con sus cifras, la retro de la P3; la última pregunta la contestaba el M3 | **Otro MA(2), $\theta = (0.9, 0.2)$**, con tres entregables. (a) invertible por el triángulo y por las raíces ($-2$ y $-2.5$: se factoriza a mano); (b) $\rho_1 = 0.5838$, $\rho_2 = 0.1081$, y la cota; (c) **nuevo**: el MA(2) con $\theta = (2.4, 0.8)$ tiene la misma ACF —es el anterior con una raíz invertida— y no es invertible; hay cuatro MA(2) con esa ACF (`[E2-03]`) y `arima()` devuelve por defecto el invertible (simulación: 0.904, 0.230 y $\hat\sigma^2 = 4.035$). Salen los pesos $\pi$, que el enunciado no pedía |
| **3 · ventanas** | El enunciado pedía dos ventanas y la solución usaba cuatro; la pista adelantaba los tres resultados; «periodo» | El enunciado pide las cuatro ventanas y tres lecturas, la tercera con la pregunta que corrigió la R1: «si el veredicto cambia, ¿lo explica el número de datos?». Pista sin resultados. «pseudo-periodo» en la respuesta y en el segundo punto. El código y los dos fragmentos marcados, intactos |

Orden y numeración, sin cambio.

---

## 4 · Minutos

Convenio de la R3, sin tocar: minutos de **lectura** con la pista y la solución de cada ejercicio
leídas (columna «abierto» de `r3_minutos.py`); no incluyen resolver, los desarrollos plegados ni los
quizzes. Salidas: `r5_minutos_antes.out` (sobre `5c2fdb3`) y `r5_minutos_despues.out`.

| Módulo | Declarado antes | Medido antes | Medido ahora, cerrado | Medido ahora, abierto | Declarado ahora |
|---|---|---|---|---|---|
| M1 | 10 | 10.7 | 11.3 | 15.2 | **15** |
| M2 | 14 | 15.0 | 15.5 | 18.6 | **19** |
| M3 | 15 | 15.7 | 16.6 | 20.2 | **20** |
| M4 | 13 | 13.5 | 14.2 | 17.5 | **18** |
| M5 | 18 | 18.9 | 19.8 | 23.7 | **24** |
| M6 | 7 | 7.1 | 7.9 | 11.9 | **12** |
| M7 | 9 | 9.7 | 10.5 | 14.4 | **14** |
| M8 | 11 | 11.2 | 11.2 | 11.2 | **11** |
| M9 | 31 | 32.5 | 33.2 | 37.3 | **37** |
| M10 | 22 | 23.8 | 13.8 | 25.9 | **26** |
| Total M1–M10 | 150 | 158.1 | 154.0 | 195.9 | 196 |

Lo declarado dista como mucho 0.5 min de lo medido. «Medido antes» ya no coincidía del todo con lo
declarado por la R3 porque la R4 añadió las citas (el M9 estaba a 1.5 min). **El capítulo crece unos
38 minutos de lectura** con todo abierto (un cuarto más); sin abrir nada, 154 frente a 148. La
autoevaluación pasa de 17 a 23 min de lectura (las retros por opción de las dos múltiples): el
comentario de `courseData.modules` lo dice.

---

## 5 · Verificación

| Qué | Resultado | Salida |
|---|---|---|
| `verifica_todo.py` | 11 verificadores en verde | `r5_verifica_todo.out` |
| Verificador de bloques del capítulo 3 | 23 bloques de R y 12 de Python; **1087 de 1087**, 0 discrepancias (antes, 733) | `r5_bloques_cap3.out` |
| Cada bloque solo, en proceso nuevo y carpeta vacía | 35 de 35 | `r5_bloques_sueltos.out` |
| `audita_posicion_correcta.py` | en verde | `r5_posicion.out` |
| `audita_citas.py` | en verde, ningún F09; 325 afirmaciones, las mismas | dentro de `verifica_todo` |
| `data-afirma` | mismo conjunto de ids; los seis elementos marcados de los ejercicios, idénticos byte a byte (lo afirma `r5_edita.py` al escribir) | salida de `r5_edita.py` |
| `ensambla_cap3.py` (sin argumentos) | reproducible byte a byte | — |
| Capítulos 4, 5 y 6 | reensamblados; `git diff --stat` no los muestra | — |
| `cuenta_sitio.py` | al día (40 ejercicios) | dentro de `verifica_todo` |
| `compila_tailwind.py --comprobar` | al día (ninguna clase nueva) | dentro de `verifica_todo` |
| `r4_sin_literales.py` | 353 literales buscados, 0 hallados | — |
| `node --check cap3_js.js` | limpio | — |
| `r5_edita.py`, dos veces | los mismos md5 | — |
| Por HTTP, a 1200 y 375 px | diez módulos sin errores de KaTeX, sin «$» sueltos, sin desborde horizontal, lienzos pintados; los once ejercicios con pista y solución a la vista y código coloreado; el quiz hecho cuatro veces pulsando (todo bien; fallo y acierto; dos fallos, con el desglose por opción; numéricas en el borde). Único evento de consola: el `favicon.ico` que el servidor de prueba no tiene | `r5_recorrido.out`, `.json` |
| `precalculo/serie.csv` | no apareció | — |

---

## 6 · Frases marcadas

**No toqué ninguna y no añadí ninguna.** Los seis fragmentos con `data-afirma` de los ejercicios
(c3-m10-31, -33, -90, -34, -46 y -35) se copian del archivo de partida; cambia la prosa de alrededor.
Tres de ellos comparten línea con texto que sí cambió (c3-m10-33, -90 y -34), y por eso un `diff` de
líneas los enseña; el elemento marcado es idéntico y F09 no salta.

Un caso que conviene leer: **c3-m10-34** («la cota $|\rho_1| \le 0.5$ se dedujo solo para el MA(1)…»)
vivía en la discusión del MA(2) antiguo. Sigue siendo cierta y pertinente con el nuevo
($\rho_1 = 0.5838 > 0.5$); lo que la rodea habla ahora de $r_1 = 0.58$ en vez de $0.55$.

Frases marcadas que no toqué y que un ejercicio nuevo pone a prueba: c3-m3-08 (M3), c3-m4-03 y
c3-m4-13 (M4), c3-m5-12 y c3-m5-17 (M5), c3-m6-06, c3-m6-07 y c3-m5-30 (M6), c3-m7-13 y c3-m7-31
(M7), c3-m8-11 (M6, apartado b), c3-m9-02, c3-m9-08 y c3-m9-51 (M9). Ninguna queda contradicha.

---

## 7 · Lo que más dudas me deja (para el verificador) y lo que dejé

**Dudas, de más a menos:**

1. **`lynx` en el M9.** No está en la lista prohibida del plan, y el diagnóstico la proponía; pero
   el **ejercicio 2 del capítulo 4** la usa después (para otra pregunta: si hay que diferenciarla),
   la presenta como nueva y ajusta el mismo AR(2) (9.78; allí Ljung–Box en el rezago 20, aquí en el
   12). No se contradicen, y el capítulo 4 dice lo mismo («el AR(2) tampoco basta»). Si se prefiere
   no adelantarla, no encontré en `datasets` otra serie estacionaria con amplitud que crezca con el
   nivel (`r5_explora.out`); la alternativa sería un proceso simulado.
2. **M9, el resultado.** No es el que anticipaba el diagnóstico («en logaritmos el AR(2) gana por
   los dos»): con la rejilla de once del M8, que incluye el AR(4), el AR(4) gana por AICc en las dos
   escalas. Y en logaritmos **ningún** candidato pasa Ljung–Box, mientras en la serie cruda dos sí
   (AR(4), 0.064; ARMA(2,2), 0.114). El ejercicio lo dice a medias: da las cifras del AR(2) y del
   AR(4) en logaritmos, no que en la cruda dos modelos pasan. La última frase («lo que se puede
   entregar es un modelo que describe el ciclo y no pasa el diagnóstico, diciéndolo») es una opinión.
3. **M6 (c), la banda ensanchada.** $\pm 1.96\sqrt{(1 + 2\rho_1^2)/T}$ va sin fuente: se comprueba
   por simulación en el bloque (0.79 barras) y se enlaza con lo que c3-m5-30 dice de la banda de
   `statsmodels`. No la atribuyo a nadie. Y (b) se apoya en c3-m8-11, que está en un desarrollo plegado.
4. **M7.** El AR(2) no es un buen modelo de esos cien años de `treering` (BIC: ruido blanco; AICc:
   ARMA(1,1), `r5_explora.out`); el ejercicio lo avisa en una frase. En (c) las distancias son medias
   de valores absolutos (0.66 y 0.57), y se comparan en el texto con los 1.26 y 1.10 de una sola
   serie, con signo: la dirección es clara, la magnitud no es comparable una a una.
5. **Pistas de P2 y P7.** La de la P2 da el método (choques compartidos); la de la P7 dice en qué
   nota está la fórmula. Las dejé porque sin ellas la pista no orienta; pueden leerse como «dar el
   criterio».
6. **P6, la semilla.** La 329 se eligió entre 28 que cumplen el patrón (`[Q6-00]`) por parecerse a
   la salida que traía el ítem. Es una salida real, elegida.
7. **P7 con etiqueta M2.** El quiz queda sin ninguna pregunta etiquetada M9 (ni M6); reparto:
   1, 3, 5, 4, 3, 5, 2, 8, 8, 7. Si se prefiere, basta cambiar `modulo: 2` por `9`.
8. **P5, dos correctas de cinco.** El motor dice «te falta 1» tras el primer fallo, y eso acota el
   segundo intento (como en la P4 del capítulo 2).
9. **Ejercicio 1.** La discusión ya no recomienda el AR(1) sin más. El titular («los dos son
   defendibles») no cambia.
10. **Ejercicio 2 (c).** «Cuatro en total» cuenta los MA(2) de coeficientes reales con esa ACF
    (`[E2-03]`); «unas cuatro veces» es $2^2$, medido 4.035.
11. **M3 (c).** Los valores teóricos 0.5 y 0.75 salen de mi cuenta en `[M3-03]`
    ($u_t = (1+2B)/(1+0.5B)\,\varepsilon_t$), no de una fuente.
12. **Variantes del banco.** Solo vi las dos que están en el repo (1 y 9). Ningún proceso nuevo
    coincide con ellas; con las variantes 2 a 8 no se puede comprobar desde aquí.
13. **M5.** `diff(WWWusage)` se toma como estacionaria sin prueba (el ejemplo de la ayuda de R hace
    esa misma diferencia; `ndiffs` = 1 en `r5_explora.out`). El AICc del ARMA(1,1) es 516.005 y la
    prosa escribe 516.00.

**Lo que dejé, y por qué:**

- **`n` en el ejercicio 3.** Está dentro de c3-m10-35 (marcada) y en la moraleja que la sigue;
  cambiarla solo en la moraleja dejaba el ejercicio con dos letras, y cambiarla en la marcada no era
  imprescindible. El código del ejercicio 3 sigue imprimiendo `periodo=`, como el del M9.
- **El motor del quiz** (el recuento de las múltiples) y **el orden de los ejercicios** (el
  diagnóstico sugería 2 → 1 → 3): no eran del encargo.
- **Los gráficos de la P3 y la P9** siguen siendo los de dos simuladores (`ma2` de las firmas del MA
  y el AR(1) del diagnóstico de residuales): se reconocen. Cambiarlos pide datos nuevos en
  `DATOS_CAP3` (`genera_cap3.R`).
- **M8 y M10**, sin ejercicio corto (D9); el hueco 12 del diagnóstico (uso crítico de la IA), sin hacer.
- **Los simuladores**: ninguno pide una predicción antes de mover.
- **Las soluciones están solo en R**, como en los capítulos 1 y 2.
- **`ensambla_cap3.py`**: no añadí los ocho ids nuevos a su lista de comprobaciones obligatorias.
- **Voz**: los enunciados, las pistas y el quiz van en imperativo de segunda persona, como los del
  capítulo 2 y los que ya había; la lectura de las soluciones, en impersonal.
- **Sin atribuciones nuevas**: ningún autor, año ni página en el texto añadido.

---

## 8 · Guiones y salidas (`diagnostico/cap3/comprobaciones/`)

| Archivo | Qué es |
|---|---|
| `r5_edita.py` | aplica la ronda sobre `5c2fdb3`; importa los cuatro siguientes |
| `r5_ediciones_cortos.py`, `r5_ediciones_m10.py`, `r5_ediciones_quiz.py`, `r5_ediciones_minutos.py` | el texto de cada tanda |
| `r5_reprex.R` | ejecuta un bloque y escribe cada salida bajo su línea, tras `#> ` (copia del del capítulo 2) |
| `r5_bloques/{m1,m2,m3,m4,m5,m6,m7,m9,e1,e2}.R` y `.out` | el código de cada solución y su ejecución |
| `r5_cifras.R` · `.out` | las cifras de prosa, pistas, retros y claves que no salen bajo un `#>`, con etiqueta |
| `r5_explora.R` · `.out` | la exploración previa: qué series sirven para cada hueco, y las descartadas |
| `r5_ayuda_datasets.R` · `.out` | lo que dice la ayuda de R de cada serie que nombran los enunciados |
| `r5_longitudes.py` · `.out` | la prueba de la opción más larga y de la más corta, antes y después, y la de las múltiples |
| `r5_posicion.out` | `audita_posicion_correcta.py` |
| `r5_minutos_antes.out` · `r5_minutos_despues.out` | `r3_minutos.py` sobre `5c2fdb3` y sobre el archivo de trabajo |
| `r5_bloques_cap3.out` | el verificador de bloques |
| `r5_bloques_sueltos.py` · `.out` | cada bloque, solo |
| `r5_recorrido.js` · `.out` · `.json` | el recorrido por HTTP a 1200 y 375 px y el quiz hecho a mano |
| `r5_verifica_todo.out` | la pasada completa |
