# Capítulo 2 · ronda R5 «práctica» · cambios

Fecha: 2026-11-18. Un solo redactor (subagente redactor R5, Fable 5.2). **Sin commits ni push.**
Alcance: T5.1, T5.2 y T5.3 del plan (`PLAN_Mejora_Cap2.md`), decisión **D9**. Base: `51a5c88`.
Fuente: `diagnostico/cap2/ejercicios.md` (del 16 nov, sobre `4b71366`), contrastado con el archivo
actual, que las rondas R1–R4 cambiaron mucho (§0).

Archivos tocados:

- `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (7489 → 8025 líneas; 395 → 439 KB):
  siete bloques `.exercise` nuevos, uno al final de los módulos 1, 2, 3, 4, 5, 6 y 8; los cinco
  ejercicios del Módulo 9; `AUTOEVALUACIONES['cap2']` entero; los minutos de `courseData.modules` y
  su comentario. **Nada más**: ni el motor del quiz, ni el de los ejercicios, ni CSS, ni la prosa de
  ningún módulo, ni una sola frase con `data-afirma` (las líneas que llevan `data-afirma` o `<cite>`
  son idénticas a las de `51a5c88`, comprobado con `diff`).
- `Htmls_Series/index.html` y `Htmls_Series/README.md`: «25 ejercicios» → «32 ejercicios» (lo exige
  `cuenta_sitio.py`: el capítulo pasa de 5 a 12).
- `diagnostico/cap2/comprobaciones/r5_*`: los guiones y sus salidas (lista al final, §7).

No se tocó: los capítulos 1 y 3 a 6, la plantilla, `ensamblado/`, `precalculo/`, `bibliografia/`,
`Vault/`.

**Cómo está hecha la edición.** `r5_edita.py` parte de `git show 51a5c88:…` y aplica cuatro pasos
(`r5_ediciones_m9.py`, `_quiz.py`, `_cortos.py`, `_minutos.py`), así que es reejecutable: dos
pasadas dan el mismo md5. El código de las soluciones **no está escrito en los guiones de edición**:
cada bloque vive en `r5_bloques/<id>.R`, `r5_reprex.R` lo ejecuta y escribe cada salida real bajo su
línea tras `#> ` (`r5_bloques/<id>.out`), y eso es lo que se pega en el capítulo. Las cifras de la
prosa que no salen bajo un `#>` del propio capítulo están en `r5_cifras.out`, con etiqueta (`[Q2-01]`,
`[E2-01]`…); abajo se cita la etiqueta de cada una.

---

## 0 · Lo que ya estaba arreglado al empezar (y no se tocó, o solo se completó)

| Hallazgo del diagnóstico | Estado en `51a5c88` |
|---|---|
| «Seis preguntas» cuando hay ocho | Ya decía «Ocho preguntas» |
| Ningún bloque llevaba `#>`: el verificador contrastaba 0 de 0 | Resuelto por la R1 (277 de 277). Ahora, 485 de 485 |
| `preparar()` aplicaba Box–Cox con λ = −0.2947 a `AirPassengers` | Resuelto por la R3: el argumento `logaritmo` lo decide el paso 1 |
| E1: «Se trabaja sin transformar» contra un pipeline que tomaba el logaritmo | A medias: el pipeline ya admite `logaritmo = FALSE`, pero la solución no lo nombraba ni comprobaba qué pasa con el logaritmo; la PACF se pedía y no se calculaba. Hecho ahora (§3) |
| E1: la advertencia de la varianza en series estacionales, escondida en la pista | La R1 retiró la varianza como criterio en el M7; la pista ya no la nombra |
| E2: «la única diferencia es el componente estacional» | La R1 ya reconocía la longitud y la semilla y citaba la barra 0 (3.2 %). Faltaba el control de verdad y el error de Monte Carlo. Hecho ahora |
| E3: Ljung–Box sin presentar | El M3 lo anuncia desde la R3 como prueba del Capítulo 3 (frase marcada `c2-m3-17`). La solución lo seguía usando como criterio. Retirado ahora |
| E4: la conclusión «propiedad estructural de la serie» | La R1 ya la había cambiado por la ventana de 54 meses (p = 0.071) |
| Q3, retro de (b), confuso | Ya decía «se salen 10 de 24» |
| Q8: la premisa chocaba con `preparar()` | Ya no chocaba; la pregunta seguía siendo una paráfrasis de la nota del M8. Rehecha |

---

## 1 · T5.1 · Siete ejercicios cortos «Para practicar»

Uno al final de cada módulo que no tenía práctica: **M1, M2, M3, M4, M5, M6 y M8**, justo antes de
la lista de fuentes del módulo (líneas 2479, 2687, 2977, 3270, 3536, 3999 y 4740). La forma es la
del capítulo 1: un `<div class="exercise">` titulado «Para practicar» con un `.ejercicio-guiado`
—enunciado, entregables en lista con letras, una pista y una solución con código y lectura—. Van
sin número, para no chocar con los ejercicios 1 a 5 del M9.

**Ninguna clase nueva de Tailwind, ninguna regla CSS nueva y ningún cambio en el motor.** En el
capítulo 1 hubo que cambiar un selector del motor porque un enunciado llevaba un `<pre>`; aquí el
código de partida va en línea (`<code>`), y el selector `.ejercicio-panel pre.collapsed` sigue
bastando. `compila_tailwind.py --comprobar`, en verde.

**Sin red y sin depender de otro bloque.** Las series son de `datasets` (`EuStockMarkets`,
`discoveries`, `LakeHuron`, `nhtemp`, `JohnsonJohnson`) o simuladas con semilla. Lo que el enunciado
dice de cada serie se leyó en la ayuda de R (`r5_ayuda_datasets.out`). Cada bloque corre solo, en
proceso nuevo y carpeta vacía (`r5_bloques_sueltos.out`: 29 de 29).

| Mód. | Línea | Serie | Qué practica (hueco del diagnóstico) | Entregables | Palabras: enunciado · todo (sin código) |
|---|---|---|---|---|---|
| M1 | 2479 | Proceso construido: normal en los instantes impares, uniforme en los pares; y un millón de Cauchy | Estricta frente a débil, en los dos sentidos (hueco 7) | 4 | 193 · 515 |
| M2 | 2687 | Rendimientos diarios del DAX (`EuStockMarkets`), 1859 valores | Incorrelado no es independiente (hueco 5) | 3 | 127 · 388 |
| M3 | 2977 | `discoveries`, 1927–1936: diez valores | Calcular $r_k$ a mano; el divisor $T$; la banda con $T$ pequeña (hueco 7) | 4 | 121 · 375 |
| M4 | 3270 | Dos simuladas (recetas AR(2) y MA(1)) y `LakeHuron` | Leer ACF y PACF juntas e identificar (hueco 1) | 3 | 156 · 494 |
| M5 | 3536 | Recta con ruido y caminata con deriva, mismo ruido, `set.seed(37)` | Tendencia determinista frente a estocástica; la deriva (hueco 3) | 3 | 157 · 391 |
| M6 | 3999 | `nhtemp` (temperatura anual de New Haven, 60 años) | ADF y KPSS sobre una serie nueva eligiendo la especificación; la fila «ninguna rechaza» (hueco 2) | 4 | 143 · 471 |
| M8 | 4740 | `JohnsonJohnson` (84 trimestres) | Elegir λ donde importa y deshacer la transformación (hueco 4) | 3 | 160 · 405 |

### 1.1 · M1 — estricta frente a débil

Un proceso que cumple las tres condiciones de la débil (media 0, varianza 1, covarianza 0) y cambia
de distribución según el instante: débil sí, estricta no. Y el contrario, valores i.i.d. de Cauchy:
estricta sí, débil no, porque no hay varianza finita. Los dos casos juntos dan contenido a la nota
del módulo (`c2-m1-07`, sin tocar): «con varianza finita» y «no al revés».

- Pista: dice qué mira cada definición y manda a hacer dos listas y a releer la segunda condición.
- El código usa `cor()` entre valores vecinos, no `acf()`, que el M1 todavía no ha presentado.

| Cifra | De dónde |
|---|---|
| Varianza de la uniforme, $(2\sqrt{3})^2/12 = 1$ | `[M1-01]` |
| Medias 0.011 y 0.003; varianzas 0.987 y 0.994; correlación 0.003 | bloque `m1` |
| Proporción por encima de 2: 0.0225 y 0; teórica 0.0228; $\sqrt{3} = 1.732$ | bloque `m1` |
| Varianza muestral de Cauchy: 753, 3125, 182 823 | bloque `m1` |

### 1.2 · M2 — incorrelado no es independiente

Los rendimientos del DAX dejan 2 de 24 barras fuera (rezagos 11 y 17); sus cuadrados, 10 de 24. El
tercer apartado es lo que el capítulo no tenía: barajar los rendimientos conserva la distribución y
destruye el orden, y con él la estructura de los cuadrados (1 y 0 barras): era dependencia temporal.
La solución recuerda que, sin independencia, la banda ya no cubre exactamente el 95 % (`c2-m2-10`,
sin tocar). No usa Ljung–Box.

| Cifra | De dónde |
|---|---|
| 1860 días, 1859 rendimientos, banda ±0.0455 | bloque `m2`, `[M2-02]` |
| Rezagos fuera: 11 y 17; en los cuadrados, 1–7, 14, 15 y 24; $r_1, r_2, r_3$ = 0.079, 0.171, 0.074 | bloque `m2` |
| Barajados: 1 y 0 | bloque `m2` |
| «Algo más de una» barra por azar (1.2) | `[M2-01]` |

### 1.3 · M3 — calcular $r_k$ a mano

Diez valores reales con media entera (3), elegidos buscando en `discoveries` una ventana con media
entera y $r_1$ apreciable (la búsqueda está al final de `r5_explora.out`). Entregables: $\bar y$ y $\hat\gamma_0$; $\hat\gamma_1$, $\hat\gamma_2$, $r_1$,
$r_2$ contando los productos; lo que saldría con el divisor $T-k$ y cuál usa `acf()`; la banda.
Cierra con lo que el diagnóstico pedía sobre la banda: 0.471 es enorme con 200 datos y no sale de
la banda con 10.

| Cifra | De dónde |
|---|---|
| Los diez valores; media 3; $\hat\gamma$ = 3.4, 1.6, 0.2; $r$ = 0.4706, 0.0588 | bloque `m3` |
| Desviaciones, cuadrados (34), productos del rezago 1 (16) y del 2 (2) | `[M3-02]`–`[M3-04]` |
| Con $T-k$: 0.5229 y 0.0735; factores 10/9 y 10/8 | bloque `m3`, `[M3-05]` |
| Banda ±0.620; con 200 datos, ±0.139 | bloque `m3`, `[M5-01]` |

### 1.4 · M4 — identificar con ACF y PACF

Tres series, la misma tarea: rezagos fuera de la banda, qué línea de la regla del módulo
corresponde y qué barras son azar. `A` es un AR(2) cuya receta se da en palabras, para que la
definición de la PACF permita **predecir** el corte antes de calcular (es lo que pide la pista). `B`
es el caso que el capítulo no enseñaba en ningún sitio: la ACF que se corta. `LakeHuron` es la serie
real: PACF fuera en 1 y 2, ACF que decae, un AR(2); con la comprobación pendiente —que sea
estacionaria— dicha y remitida a los Módulos 5 y 6.

**Se descartó `lh`**, la candidata del diagnóstico: es la serie del ejercicio 1 del capítulo 3
(l. 6018 de ese capítulo), que pide exactamente esta lectura. Usarla aquí regalaba ese ejercicio.

| Cifra | De dónde |
|---|---|
| `A`: ACF fuera en 1–6; PACF en 1, 2, 13, 16; PACF 0.698, 0.230, −0.032 | bloque `m4` |
| `B`: ACF fuera en 1 y 15 (0.492, 0.013, 0.024); PACF 0.492, −0.302, 0.238, −0.083, 0.136 | bloque `m4` |
| `LakeHuron`: banda ±0.198; ACF fuera en 1–9; PACF en 1, 2, 10; 0.832, −0.267, 0.131 | bloque `m4` |

### 1.5 · M5 — tendencia determinista frente a estocástica

Las dos series suben 0.2 por periodo y comparten ruido. La tabla de cuatro filas (cada serie con
cada tratamiento) convierte en números el aviso del módulo (`c2-m5-12`, sin tocar): con el
tratamiento correcto queda el ruido ($r_1 = -0.014$, ninguna barra fuera, en las dos); diferenciar
la recta deja $r_1 = -0.517$; restar la recta a la caminata deja $r_1 = 0.959$ y 21 de 24 fuera. El
tercer apartado practica la deriva: se estima de dos maneras (0.235 y 0.205) y se mide qué serie
vuelve a su recta (2.7 frente a 12.0).

Semilla 37, elegida por dar una tabla limpia (`r5_explora.out` tiene las dos búsquedas, con
pendiente 0.3 y con 0.2). La pendiente, 0.2, y la semilla son distintas de las del
bloque del módulo (0.3, `set.seed(2026)`).

### 1.6 · M6 — ADF y KPSS sobre una serie nueva

`nhtemp` reúne lo que el diagnóstico echaba en falta: una serie que el módulo no toca, la elección
entre KPSS de nivel y de tendencia, el número de términos del ADF, y la fila «no rechaza / no
rechaza», que nadie practicaba.

- Tal como vienen: ADF p = 0.084 y KPSS de nivel p < 0.01 → segunda fila, «hay que diferenciar».
- Con el KPSS que corresponde a `adf.test()`, el de tendencia: p > 0.10 → tercera fila, datos poco
  informativos. El de nivel rechazaba la media constante, no la estacionariedad alrededor de una
  recta.
- Con k = 1…5 el p-valor del ADF es < 0.01, 0.045, 0.084, 0.053 y 0.370: la decisión al 5 %
  depende de k.
- Desempate con el correlograma, con los dos tratamientos del M5: restada la recta, $r_1 = 0.107$
  (banda ±0.253); diferenciada, $r_1 = -0.526$.

El veredicto no fuerza la mano: «lo razonable es tratar la tendencia como determinista —restar la
recta— y dejar dicho con qué especificación se decidió y que el ADF no fue concluyente».

Se probó antes `WWWusage`, la propuesta del diagnóstico (`r5_explora.out`): su primera diferencia
vuelve a caer en «ninguna rechaza» con el KPSS de nivel y en «rechaza» con el de tendencia, y el
ejercicio se alargaba hasta una segunda diferencia. `nhtemp` cabe en cuatro apartados.

### 1.7 · M8 — elegir λ y deshacer

- (a) Programar el criterio de Guerrero con la receta del módulo y comprobarlo con las tres cifras
  que el módulo da para `AirPassengers` (0.530, 0.153, 0.081): el estudiante sabe si su función está
  bien antes de usarla.
- (b) En `JohnsonJohnson` transformar sí importa (1.081 → 0.402) y el logaritmo capta el 92.1 % de
  la mejora (84 % en `AirPassengers`, `[Q8-04]`): se elige el logaritmo, con cifras.
- (c) Deshacer un pronóstico hipotético hecho en logaritmos (w = 2.75, error normal de desviación
  0.20, **dados como premisa en el enunciado**): $\exp(2.75) = 15.64$; el intervalo 10.49–23.34 es
  asimétrico (5.15 y 7.70, `[M8-01]`); la mediana de 100 000 simulados es 15.66 y la media, 15.97
  (0.33 más, `[M8-03]`). Es el aviso del módulo (`c2-m8-08`, sin tocar) visto con números, sin
  necesitar todavía un modelo de pronóstico.

`UKgas`, la otra candidata, se reservó para la pregunta 8 del quiz (§2).

---

## 2 · T5.2 · El quiz

El motor no se tocó. Las ocho preguntas se reescriben en el arreglo; cuatro conservan su asunto y su
clave (1, 3, 4 y 6) y cuatro cambian de pregunta (2, 5, 7 y 8).

### Las cuatro formas de contestarse solo, una por una

| | Antes (`51a5c88`) | Ahora |
|---|---|---|
| **Posición** | orden 3 1 4 2 4 | orden 3 1 4 2 4 (`r5_posicion.out`: ninguna posición > 40 %, racha 1); las dos correctas de la múltiple, en 2 y 4 |
| **Tamaño** | la más larga acierta **5 de 5** | la más larga acierta **1 de 5**; la más corta, 0 (`r5_longitudes.out`) |
| **Pistas** | las ocho dan el criterio o la operación | las ocho dicen por dónde entrar (tabla de abajo) |
| **Filtraciones** | Q2 y Q7 a la vista en el capítulo; la retro de Q3 da el patrón de los ejercicios 1 y 3 | ninguna respuesta está escrita en el capítulo; ninguna retro nombra `co2` ni `USAccDeaths` ni el resultado de un ejercicio del M9 |

### Longitud de las opciones (caracteres visibles; ✔ = correcta)

| Ítem | Antes | Ahora |
|---|---|---|
| Q1 | 45 · 42 · **55✔** · 45 | 79 · 74 · 73✔ · 66 |
| Q3 | **89✔** · 57 · 54 · 47 | 89✔ · 86 · 97 · 87 |
| Q5 | 35 · 20 · 49 · **50✔** | 81 · 78 · 74 · 79✔ |
| Q6 | 51 · **83✔** · 49 · 48 | 86 · 79✔ · 73 · 73 |
| Q8 | 49 · 37 · 66 · **85✔** | 79 · 77 · 77 · **80✔** |
| Múltiple (Q4) | correctas 66 de media, falsas 48 | correctas 65, falsas 62 |

En la primera pasada la correcta quedó como la más **corta** en tres ítems: igualar no puede
consistir en eso, y el guion mide ahora las dos cosas.

### Ítem por ítem

**P1 · ¿es estacionaria una serie estacional? (M1)** — se conserva. Opciones igualadas. La pista
terminaba con «¿Es la misma esperanza en diciembre que en febrero?», que era la respuesta; ahora:
«Relee la primera condición… y fíjate en para qué instantes se pide. Después compara dos meses
concretos de esta serie».

**P2 · la banda (numérica, ahora etiquetada M2) — rehecha.** Antes pedía $1.96/\sqrt{144}$, que está
en pantalla en el explorador del M4. Ahora pide darle la vuelta: con $r_5 = 0.15$, cuántas
observaciones hacen falta, como mínimo, para que la barra quede fuera. Respuesta 171
($(1.96/0.15)^2 = 170.7$, `[Q2-01]`). No está escrita en ningún sitio y exige entender que la banda
depende solo de $T$.
- Tolerancia 0.5: aciertan 171, 170.74, 170,7 y 170.5–171.5; no acierta 170, que no es un redondeo
  sino la respuesta equivocada (con 170 datos la banda vale 0.1503, `[Q2-02]`), ni 172.
- La `retroFallo` diagnostica el 13 (faltó elevar al cuadrado: 13.07) y el 170.
- Etiqueta `modulo: 2`: la banda se enseña en el M2, que no tenía ninguna pregunta.

**P3 · correlograma de ∇log AP (M7)** — se conserva. Opciones igualadas (la correcta ya no es la
única con un mecanismo). Pista: ya no dice «alguno que signifique algo especial para una serie
mensual». La retro de la correcta ya no termina en «aplicando además ∇₁₂ se llega a la serie del
modelo *airline*»: dice lo que el gráfico muestra. Cifras: `[Q3-01]`.

**P4 · indicios de sobrediferenciación (múltiple, M7)** — mejorada.
- **Cada opción lleva su `retro`** (no tenía ninguna): el desglose del fallo explica ahora cada
  opción mal juzgada.
- Sale la opción «queda inducido un MA(1) no invertible»: no es una señal que se observe en los
  datos, sino la consecuencia teórica. Entra un distractor que sí se observa y no distingue: «el
  KPSS de la serie diferenciada ya no rechaza» (pasa igual con la TRM, donde la diferencia hacía
  falta, `[Q4-03]`; y con un ruido blanco diferenciado, `[Q4-04]`).
- Quedan **dos** correctas de cinco, en las posiciones 2 y 4.
- La pista ya no dice «Son tres» ni enumera los temas. **El motor sigue anunciando cuántas faltan**
  («te falta 1»): es armazón y no se tocó (§6).
- Las retros generales nombran el contenido, no la casilla, como exige `audita_posicion_correcta.py`.

**P5 · ADF y KPSS (M6) — rehecha.** Antes: p = 0.58 y p < 0.01, los números de la TRM, y la pista
terminaba dando la respuesta. Ahora, el caso que nadie practicaba: una serie mensual de 120 datos
con tendencia y estacionalidad en la que **las dos rechazan**. La correcta es «se contradicen: hay
que revisar la especificación», y su retro dice qué revisar: el KPSS de nivel no admite tendencia y
`adf.test()` usa k = 4 con 120 datos (`[Q5-01]`), menos que el periodo. Los distractores son las
otras tres filas de la tabla. Pista: «Escribe la hipótesis nula de cada prueba y, debajo, qué se
concluye al rechazarla».

**P6 · ACF de la caminata (M5)** — se conserva, con el gráfico que ya había (§6). Opciones
igualadas. Pista: ya no describe la forma ni pregunta «¿a qué proceso corresponde?». Dos retros
corregidas:
- la del logaritmo argumentaba con que «esta serie toma valores negativos», algo que no se ve en
  una ACF; ahora: una dispersión que crece con el nivel se ve en la serie, no en su ACF;
- la de «nada: es estacionaria» comparaba solo con φ = 0.5. Eso era cierto y parcial: con φ = 0.95
  se tendría $0.95^{12} = 0.54$ (`[Q6-01]`), por encima del 0.488 del gráfico. Ahora reconoce el
  caso difícil del M5 y dice que ni entonces cabe quedarse sin hacer nada.

**P7 · lo que cuesta diferenciar (numérica, M7) — rehecha.** Antes: 144 − 12 − 1, la misma cuenta
con la misma $T$ que hace el M7. Ahora, trimestral con $T = 40$ y $\nabla\nabla_4$: qué
**porcentaje** se pierde. Respuesta 12.5 %; tolerancia 0.5 (aciertan 12, 12.5, 12,5 y 13; no 11.9
ni 13.1). La `retroFallo` diagnostica 32.5 (restó 12 y 1), 10 y 2.5 (una sola diferencia) y 35 (las
que quedan). Cifras: `[Q7-01]`.

**P8 · leer el criterio de Guerrero (M8) — rehecha.** Antes: por qué el logaritmo y no λ = −0.295,
una paráfrasis de la nota del M8. Ahora, tres cifras de otra serie, `UKgas` (0.792 sin transformar,
0.287 con el logaritmo, 0.084 en el óptimo λ = −0.446, `[Q8-01]`), y cuatro lecturas. La correcta:
el logaritmo capta el 71 % de la mejora (`[Q8-02]`) y deja amplitud sin estabilizar. Los
distractores son tres errores de lectura reales: comparar con el óptimo para decir que «empeora»,
confundir 0.287/0.792 = 0.36 con la mejora captada, y leer un λ negativo como «la dispersión baja».
La retro de la correcta lo comprueba en los datos: la desviación anual de log(`UKgas`) pasa de 0.26
en los tres primeros años a más de 0.5 en los tres últimos (`[Q8-03]`). **Ver §6, punto 2.**

### Las pistas, antes y ahora

| | Antes | Ahora |
|---|---|---|
| P1 | «…¿Es la misma esperanza en diciembre que en febrero?» | relee la condición; compara dos meses |
| P2 | «$\sqrt{144} = 12$. Solo tienes que dividir.» | plantea la condición, despeja, decide el redondeo |
| P3 | «…alguno que signifique algo especial para una serie mensual» | cuenta cuántas salen y dónde están las más altas |
| P4 | «Son tres. Piensa en…» (y los tres temas, en orden) | separa el antes del después; ¿ocurriría igual con una diferencia necesaria? |
| P5 | «…puede significar lo mismo» | escribe las dos $H_0$ y lo que se concluye al rechazarlas |
| P6 | describía la forma y remitía al proceso | compara dos barras, descríbelo, búscalo en la tabla del M3 |
| P7 | «∇ cuesta 1 y ∇₁₂ cuesta 12» | cuenta las que se quedan sin pareja; mira cada cuánto se mide la serie |
| P8 | descartaba (a) y apuntaba a (d) | ordena las tres cifras; con cuál comparar para decir si ayuda y con cuál para decir cuánto falta |

---

## 3 · T5.3 · Los cinco ejercicios del Módulo 9

Los cinco pasan a la forma de los cortos: enunciado con entregables en lista.

| Ej. | Qué había | Qué queda |
|---|---|---|
| **1 · `co2`** | Solución «sin transformar» sin decir qué paso lo decide; la PACF se pedía y no se calculaba; la pista decidía por el estudiante («Guerrero no te va a servir», «piensa cuánto varía el nivel») | Cuatro entregables: la decisión del paso 2 con una medida; $D$ y $d$ en el orden de la regla; el correlograma en cada etapa; ACF **y PACF** de la serie final. La solución nombra `preparar(co2, logaritmo = FALSE)`, mide (máximo 1.17 veces el mínimo; en `AirPassengers`, 5.98) y **comprueba que con el logaritmo las decisiones son las mismas** ($D = 1$, $d = 1$). PACF fuera en 1, 3, 9, 11, 12, 13 y 24; $r_{12} = -0.420$, que antes no se comentaba. La pista manda a releer el paso 2 y a buscar una medida. Sale el λ de Guerrero de la solución (−0.0343): el pipeline ya no lo usa para decidir |
| **2 · Monte Carlo** | 500 caminatas de 100, comparadas con un experimento de 144 y otra semilla; 4.6 % frente al 5 % sin error de Monte Carlo | 500 caminatas de **144**, la longitud del M6. (a) 3.0 %; (b) el error de Monte Carlo, calculado: ±0.97 puntos, intervalo 3.1–6.9 % si la prueba rechazara el 5 %; el 3.0 % y la barra 0 del M6 (3.2 %) caen en el borde de abajo, y con 5000 series sale 4.3 % (±0.3, `[E2-01]`): la prueba se queda algo corta. (c) **El control**: las mismas 500 caminatas más la oscilación de amplitud 4 → 21.6 %. El M6 dio 17.6 % con otras 500: la diferencia también es error de Monte Carlo (unos 2.5 puntos, `[E2-03]`). Con `set.seed(7)` el código devuelve el 3.2 % y el 17.6 % del módulo (`[E2-02]`). Potencia: 99.8 % |
| **3 · `USAccDeaths`** | «residuales» para series diferenciadas; Ljung–Box en la tabla y como criterio; columna de varianza; la pista daba el criterio y remitía a «la caja de advertencia del Módulo 7» (hay tres) | Tres entregables. «Series diferenciadas». **Sin Ljung–Box**: el criterio es el recuento de barras con la banda de cada serie (las cuatro tienen distinta $n$), contra las 1.2 que se esperan por azar; una frase dice que el Capítulo 3 lo cambia por la prueba que anunció el M3. Sale la varianza, que desde la R1 no decide. La pista nombra la caja («Regla del orden») y no el criterio. La advertencia sobre $r_1 = -0.353$ pasa a ser el apartado (c) |
| **4 · TRM al día** | Copiar y correr; la pista adelantaba el veredicto | Cuatro entregables: meses; **la especificación, justificada** (KPSS de nivel o de tendencia, y si hay que cambiar k); las pruebas y su fila; la ventana desde 2022. La solución gana un párrafo sobre la especificación (`nsdiffs` = 0 sobre la copia fija, k = 5; el KPSS de tendencia también rechaza, `[E4-01]`, `[E4-02]`) y tres líneas de código. La pista pide la predicción con su porqué y manda al «detalle de especificación» del M6. Los dos bloques largos de descarga, intactos |
| **5 · IA como tutor** | La pista daba el experimento (k = 12), que es la primera evidencia del M6: verificar era volver a correr el módulo. Entregable implícito | Sobre una serie que el capítulo no resolvió, `UKDriverDeaths`. Entregable explícito: tabla de dos columnas y un párrafo. La pista pide «una predicción que se pueda comprobar» sin decir cuál. Los criterios traen el código y la cifra: de −6.54 (p < 0.01) a −2.58 (p = 0.33) al pasar de k = 5 a k = 12. El punto 4 ya no afirma qué errores son «frecuentes» en un asistente (no era contrastable): los da como ejemplos, en condicional |

Lo que se conserva: el orden y la numeración de los cinco (el M6 remite al «ejercicio 4» en dos
comentarios de código), la serie de cada uno salvo la del 5, y las cifras que ya eran correctas
($r_1 = 0.991$, 0.800, −0.302; 14, 6, 6 y 2 barras de 24).

---

## 4 · Minutos

Convenio de la R3, sin tocarlo: minutos de **lectura** con la pista y la solución de cada ejercicio
leídas (columna «abierto» de `diag/cuenta_cap2.py`: palabras / 180 + 3 por simulador + 2 por bloque
de código); no incluyen resolver el ejercicio, el desarrollo plegado del M4 (2.1 min) ni la
autoevaluación (10.8 min de lectura; antes 8.6). Salidas: `r5_minutos_antes.out` y
`r5_minutos_despues.out`.

| Módulo | Declarado antes | Medido antes | Medido ahora, paneles cerrados | Medido ahora, abiertos | Declarado ahora |
|---|---|---|---|---|---|
| M1 | 6 | 6.5 | 7.6 | 11.4 | **11** |
| M2 | 8 | 7.8 | 8.5 | 11.9 | **12** |
| M3 | 9 | 9.3 | 10.0 | 13.4 | **13** |
| M4 | 9 | 9.6 | 10.5 | 14.4 | **14** |
| M5 | 10 | 10.2 | 11.1 | 14.4 | **14** |
| M6 | 13 | 13.7 | 14.5 | 18.3 | **18** |
| M7 | 16 | 16.6 | 16.6 | 16.6 | **17** |
| M8 | 8 | 8.5 | 9.4 | 12.8 | **13** |
| M9 | 27 | 28.1 | 13.6 | 34.0 | **34** |
| Total | 106 | 110.4 | 101.7 | 147.1 | 146 |

Lo declarado dista como mucho 0.4 min de lo medido en cada módulo. El M7 no cambió en esta ronda:
sube de 16 a 17 porque la R4 le añadió las citas (16.3 → 16.6). El comentario sobre
`courseData.modules` dice el convenio, la fecha y que «unos 11 min» de autoevaluación quedan fuera.

**El capítulo crece 37 minutos de lectura** (un tercio). Es el precio de siete ejercicios con
solución; lo que se ve sin abrir nada son 121 a 193 palabras por enunciado.

---

## 5 · Verificación

| Qué | Resultado | Salida |
|---|---|---|
| `verifica_todo.py` | 11 verificadores en verde | `r5_verifica_todo.out` |
| Verificador de bloques del capítulo 2 | 20 bloques de R y 9 de Python; **485 de 485**, 0 discrepancias (antes, 277) | `r5_bloques_cap2.out` |
| Cada bloque solo, en proceso nuevo y carpeta vacía | 29 de 29 | `r5_bloques_sueltos.out` |
| `audita_posicion_correcta.py` | en verde | `r5_posicion.out` |
| `audita_citas.py` | sin hallazgos; la salida con `--avisos` es la de `51a5c88` salvo el número de línea de cinco avisos A01 del capítulo 2; ningún F09 | — |
| `data-afirma` y `<cite>` | las líneas que llevan uno u otro son idénticas a las de `51a5c88` (81 con `data-afirma`) | `diff` (en la sesión) |
| `ensambla_cap3.py` | reproducible byte a byte | — |
| `r2b_sintaxis.py` | los cinco capítulos, `node --check` limpio | — |
| `cuenta_sitio.py` | cifras de la portada y del README, al día (32 ejercicios) | — |
| `compila_tailwind.py --comprobar` | al día (ninguna clase nueva) | dentro de `verifica_todo` |
| `r5_edita.py`, dos veces | el mismo md5 | — |
| Por HTTP, a 1200 y 375 px | nueve módulos sin errores de consola ni de KaTeX, sin desplazamiento horizontal; quiz hecho con aciertos y fallos; numéricas con el redondeo | `r5_navegador.out` |
| `precalculo/serie.csv` | no apareció | — |

---

## 6 · Lo que queda sin hacer, y lo que conviene mirar con cuidado

**Para el verificador independiente (lo que más dudas me deja):**

1. **Ejercicio del M6, el veredicto.** Con `nhtemp` las pruebas no concluyen y la solución se inclina
   por la recta con ruido apoyándose en dos $r_1$ (0.107 y −0.526). Es un argumento de correlograma
   con 60 datos; está dicho como inclinación y no como demostración, pero es el punto del capítulo
   donde una solución opina.
2. **Pregunta 8 y `UKgas`.** La retro dice que el logaritmo deja amplitud sin estabilizar en
   `UKgas` (desviación anual de 0.26 a más de 0.5 en logaritmos). El M7 toma esa serie en
   logaritmos «porque su amplitud crece con el nivel» y sigue adelante. No se contradicen —el M8
   prefiere el logaritmo aun sin ser el óptimo—, pero la pregunta enseña que en esa serie el precio
   es mayor que en `AirPassengers`, y el M7 no lo dice. No toqué el M7.
3. **Ejercicio 2: «la prueba se queda algo corta».** Con 5000 caminatas de 144 el ADF de `tseries`
   rechaza el 4.3 % (±0.3) al 5 %. El M6 dice «3.2 % de rechazos, cerca del 5 % nominal» (frase sin
   marcar). No la toqué; el ejercicio la matiza.
4. **Ejercicio 1: `logaritmo = FALSE` en `co2`.** Se justifica con que el nivel cambia un 17 %, que
   es el criterio que la R3 escribió en el paso 2, y se comprueba que con el logaritmo sale lo
   mismo. El ejercicio 1 del capítulo 1 midió que la amplitud del vaivén de `co2` sí crece con el
   nivel; aquí no se menciona, para no abrir otra discusión dentro de una solución.
5. **Ejercicio del M1.** Es el más largo (515 palabras) y el único con cuatro entregables y dos
   procesos. Si hay que recortar, el apartado (c) —la comprobación por simulación— es el
   prescindible.
6. **Ejercicio del M4: tres series.** `LakeHuron` se lee como AR(2) sin haber comprobado que sea
   estacionaria (ADF p = 0.254 en `r5_explora.out`); la solución lo dice y lo deja para los Módulos
   5 y 6, pero un lector estricto puede objetar que el M4 pide lo contrario dos párrafos antes.

**Frases marcadas (`data-afirma`) que no toqué y que rozan lo nuevo:** ninguna quedó contradicha.
Las que un verificador debería leer junto al ejercicio que las pone a prueba: `c2-m1-07` (M1),
`c2-m2-03` y `c2-m2-10` (M2), `c2-m3-05` y `c2-m3-15` (M3), `c2-m4-11` (M4), `c2-m5-12` (M5),
`c2-m6-06` (M6, la tabla de filas) y `c2-m8-08` (M8).

**Lo que dejé, y por qué:**

- **El motor del quiz.** En la de varias respuestas, el primer fallo sigue diciendo cuántas de las
  marcadas están bien y cuántas faltan. Con dos correctas de cinco, eso acota mucho el segundo
  intento. Cambiarlo es tocar el armazón de cinco capítulos; no era imprescindible.
- **El gráfico de la pregunta 6** es el mismo correlograma de la caminata que muestran el M3 y el
  M4. Cambiarlo por una serie no vista pide datos nuevos en `DATOS_CAP2` (`genera_cap2.R`).
- **Reparto del quiz por módulo:** 1, 2, 7, 7, 6, 5, 7, 8. El M2 gana una pregunta; el M3, el M4 y
  el M9 siguen sin ninguna con su etiqueta, aunque ahora tienen ejercicio propio.
- **El M7 no tiene ejercicio corto** (D9 no lo pedía: los ejercicios 1 y 3 del M9 son suyos).
- **Los simuladores**: sin cambios. Ninguno pide una predicción antes de mover (diagnóstico §4).
- **Tareas tipo FPP3 que siguen sin equivalente**: escribir diferencias con el operador $B$,
  emparejar series con correlogramas, serie por estudiante, la fuga de información del M9.
- **Las soluciones están solo en R**, como en el capítulo 1.
- **El ejercicio 4** sigue sin respuesta fija; sus dos bloques de descarga no llevan `#>` y el
  verificador solo comprueba que corren.
- **El ejercicio 5 sobre `UKDriverDeaths`** no dice que la serie tiene una intervención (la ley del
  cinturón de 1983, según la ayuda de R): no hace falta para la tarea.

---

## 7 · Guiones y salidas (`diagnostico/cap2/comprobaciones/`)

| Archivo | Qué es |
|---|---|
| `r5_edita.py` | aplica la ronda sobre `51a5c88`; importa los cuatro siguientes |
| `r5_ediciones_cortos.py`, `r5_ediciones_m9.py`, `r5_ediciones_quiz.py`, `r5_ediciones_minutos.py` | el texto de cada tanda |
| `r5_reprex.R` | ejecuta un bloque y escribe cada salida bajo su línea, tras `#> ` |
| `r5_bloques/{m1,m2,m3,m4,m5,m6,m8,e1,e2,e3,e5}.R` y `.out` | el código de cada solución y su ejecución |
| `r5_cifras.R` · `.out` | las cifras de la prosa y del quiz que no salen bajo un `#>`, con etiqueta |
| `r5_explora.R` · `.out` | la exploración previa: qué series sirven para cada hueco, y las descartadas |
| `r5_ayuda_datasets.R` · `.out` | lo que dice la ayuda de R de cada serie que nombran los enunciados |
| `r5_longitudes.py` · `.out` | la prueba de la opción más larga (y de la más corta), antes y después |
| `r5_posicion.out` | `audita_posicion_correcta.py` |
| `r5_minutos_antes.out` · `r5_minutos_despues.out` | `diag/cuenta_cap2.py` sobre `51a5c88` y sobre el archivo de trabajo |
| `r5_bloques_cap2.out` | el verificador de bloques |
| `r5_bloques_sueltos.py` · `.out` | cada bloque, solo |
| `r5_navegador.out` | lo visto por HTTP a 1200 y 375 px, y el quiz hecho a mano |
| `r5_verifica_todo.out` | la pasada completa |
