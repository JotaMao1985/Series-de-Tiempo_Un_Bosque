# Cap. 2 · Diagnóstico de ejercicios, autoevaluación y práctica

Archivo: `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (commit `4b71366`, worktree
`course-content-improvement-227f2c`, 2026-11-16). Diagnóstico, sin ediciones en el repo.

Leído entero: objetivos de los nueve módulos (2191, 2316, 2432, 2588, 2770, 2935, 3249, 3568,
3704), los cinco `ejercicio-guiado` (4019, 4084, 4124, 4194, 4229), `AUTOEVALUACIONES['cap2']`
(5893–6075), el motor del quiz (5033–5399), los **ocho** `data-simulador` con su
`simulador-intro` y su JS (2242–3608; 5544–5887) —el encargo hablaba de nueve; hay ocho—, los
bloques `code-tabs` y el precálculo incrustado `DATOS_CAP2` (4310). Contraste con el texto guía:
FPP3 §9.11 (`bibliografia/_local/web/hyndman2021forecasting/arima.txt` 1023–1043), §2.10
(`graphics.txt` 722–739) y §3.7 (`decomposition.txt` 496–511).

Escala de veredictos: **sirve** (publicable con retoques cosméticos) · **se puede mejorar**
(núcleo sano, arreglos puntuales) · **hay que rehacer** (no mide lo que dice medir, se responde
sin entender, o enseña algo incorrecto).

Guiones y salidas (todo en `diagnostico/cap2/diag/`):

| Guion | Qué hace | Salida |
|---|---|---|
| `ejercicios_cap2.R` | reproduce E1–E5 y las claves del quiz con el código del capítulo | `ejercicios_cap2.out` |
| `e4_trm_actualizada.R` | E4 con la TRM descargada hoy (`trm_descarga/trm.json`, URL del M6) | `e4_trm_actualizada.out` |
| `longitud_opciones.js` | prueba de «la más larga» (extrae el quiz del HTML con node) | `longitud_opciones.out` |
| `series_candidatas.R` | series de R base medidas para los huecos (§8) | `series_candidatas.out` |
| — | tolerancia de la numérica Q2 en coma flotante (node) | `tolerancias.out` |
| `datos_cap2.json` | `DATOS_CAP2` extraído de la línea 4310 | — |

(En `diag/` hay otros archivos —`v1.R`, `chrome.js`, `cuenta_cap2.py`…— que no son míos:
otra sesión trabaja en la misma carpeta.)

---

## 0. Resultado de las ejecuciones

### 0.1 Verificador de bloques

`MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html`

```
Bloques encontrados: 11 de R, 8 de Python
=== 0 de 0 cifras anunciadas aparecen en la salida real (0 bloques con discrepancias) ===
```

El capítulo no lleva ni una línea `#>`: todas sus cifras (bloques de los módulos y de las
soluciones) van en comentarios `# …`, así que **el verificador no contrasta nada** en este
capítulo. Lo que sigue lo sustituye.

### 0.2 Soluciones de los ejercicios (Rscript 4.6.0; forecast 9.0.2, tseries 0.10.62, feasts 0.5.0)

| Ej. | Cifra escrita | Salida real | ¿Coincide? |
|---|---|---|---|
| 1 | rango rel. 0.159; λ = −0.0343; `nsdiffs` = 1; `ndiffs(∇₁₂)` = 1 | 0.1592; −0.0343; 1; 1 | sí |
| 1 | r₁ = 0.9909, r₁₂ = 0.9284, banda ±0.091 | 0.9909, 0.9284, 0.0906 | sí |
| 1 | var. tras ∇₁₂ por d: 0.3882 0.1543 0.4023 1.3123 | 0.3882 0.1543 0.4023 1.312 | sí |
| 1 | final: n = 455, var 0.154, r₁ = −0.302, 5 de 24 fuera, KPSS p > 0.10 | 455, 0.1543, −0.302, 5, 0.1 | sí |
| 2 | 4.6 % (5 %), 9.2 % (10 %), potencia 93.8 % | 4.6, 9.2, 93.8 | sí |
| 3 | `ndiffs` 0, `nsdiffs` 1, `ndiffs(∇₁₂)` 1 | 0, 1, 1 | sí |
| 3 | tabla (n, varianza, r₁, r₁₂, fuera, Ljung–Box) de las cuatro series | idéntica (LB de ∇₁₂∇ = 0.0333) | sí |
| 4 | TRM: ADF −1.978 p 0.586, KPSS 2.243 p < 0.01; ∇TRM: ADF −3.880 p 0.017, KPSS 0.242 p > 0.10; `ndiffs` 1 | −1.9783 / 0.5855, 2.2427 / 0.01; −3.8801 / 0.0172, 0.2415 / 0.1; 1 | sí |
| 5 | ADF de log AP: −6.42 (k = 5) → −1.53 (k = 12) | −6.4215 → −1.5325 | sí |

**Todas las cifras de las cinco soluciones son reproducibles.** Los problemas están en lo que
el enunciado pide frente a lo que la solución hace, en lo que la pista adelanta y en dos
afirmaciones de la interpretación (fichas §3).

### 0.3 Otras comprobaciones medidas

| Qué | Resultado |
|---|---|
| E1: `preparar(co2)` del M9 (3856–3873), que es lo que el enunciado pide aplicar | λ = −0.034 → \|λ\| < 0.25 → **toma el logaritmo**; d = 1, D = 1. La solución dice «Se trabaja sin transformar» (4046–4047) |
| E1: criterio de Guerrero sobre co2 | CV(−0.5) 0.0723 · CV(0) 0.0692 · CV(0.5) 0.0732 · CV(1) 0.0833: curva plana, el log es casi el óptimo |
| E1: regla de la varianza del M7 (3398–3399) aplicada a co2 **cruda** | 224 → 1.456 → **0.855** → 1.226: mínimo en d = 2. Solo la pista (4036–4037) avisa de que no se haga así |
| E1: ∇₁₂ sola (la evidencia de correlograma que falta) | r₁ = 0.800, 15 de 24 fuera; KPSS p < 0.01 |
| E1: ACF/PACF finales (el enunciado pide PACF) | ACF fuera en 1, 3, 9, 11, 12 (r₁₂ = −0.420); PACF fuera en 1, 3, 9, 11, 12, 13, 24. La solución no calcula la PACF |
| `preparar(AirPassengers)` del M9 | usa **Box–Cox con λ = −0.2947**, no el logaritmo que recomiendan el M8 (3622–3633) y la clave de Q8 |
| E2: el mismo experimento del M6 con amplitud 0 (T = 144, `set.seed(7)`) | 3.2 % — ya está en la gráfica del M6 (3131) |
| E2: error Monte Carlo de una tasa con R = 500 | ±0.97 pp; IC 95 % binomial de 23/500: [2.94 %, 6.82 %]; 20 semillas: 2.6 %–5.2 %, media 4.14 % |
| E3: ∇₁₂ sola | KPSS p < 0.01, ADF p = 0.314: las pruebas también piden la regular |
| E3: con 24 rezagos, bandas que se salen por azar | 1.2 esperadas; ∇₁₂∇ deja 2 |
| E4 con la TRM de hoy (descargada el 16 nov 2026, n = 142, hasta 2026-10) | TRM: ADF −1.354 p 0.845, KPSS 2.055 p < 0.01; ∇TRM: ADF −3.892 p 0.0166, KPSS 0.323 p > 0.10; `ndiffs` 1. Los 138 meses comunes coinciden al centavo con los del capítulo. **El veredicto no cambia** |
| E4: ADF sobre ∇TRM según la ventana (fin entre 2022-12 y 2026-06; inicio entre 2015 y 2019) | p entre 0.010 y 0.028 en todas: la conclusión es estable en esta muestra |
| Q2: tolerancia 0.0006 sobre 0.1633 (node) | acepta 0.163 … 0.1639 y 0.1627; rechaza 0.164, 0.16 y 0.0136. No castiga el redondeo razonable |
| Q3: correlograma de ∇log AP | n = 143, banda 0.1639, r₁ = 0.1998, r₁₂ = 0.8414; **10 de 24** fuera (1, 4, 8, 11, 12, 13, 16, 20, 23, 24) |
| Q6: caminata (`set.seed(2026)`, 200) | r₁ = 0.9612, r₁₂ = 0.4877, mínimo −14.84; 0.5¹² = 0.000244 |
| Q8: criterio de Guerrero en AirPassengers | 0.53032 / 0.15308 / 0.08149; exceso del log 87.9 % («88 %»), mejora captada 84.0 % |

---

## 1. Cobertura: objetivo de módulo × dónde se practica

| Mód. | Objetivo declarado (resumen) | Ejercicio | Quiz | Simulador | Práctica real |
|---|---|---|---|---|---|
| M1 | Estricta vs débil; reconocer a simple vista una no estacionaria; por qué la teoría la exige | — | Q1 | `panel-estacionariedad` (estático, sin tarea) | Reconocer: un caso (estacionalidad), que repite el aviso 2286. **Estricta vs débil: NADA** |
| M2 | Definir el ruido blanco, reconocer su correlograma, bloque y meta | E3 lo usa como criterio, con Ljung–Box no enseñado | Q2 (la banda; etiquetada M3) | `ruido-blanco` (estático) | Banda: una división. **Incorrelación ≠ independencia (2336–2341): NADA**; ruido blanco como meta (2409–2414): solo E3 |
| M3 | Definir γ_k y ρ_k, **calcularlas**, leer un correlograma (tendencia, estacionalidad, no estacionariedad) | E1, E3 (`acf` como instrumento) | Q2, Q3, Q6 | `correlogramas-comparados` (estático) | Leer: Q3 y Q6, sobre gráficos que el capítulo ya mostró. **Calcular r_k (divisor T, 2453–2462): NADA**. Lectura de la banda con 24 rezagos (2360–2362): solo implícita en E3 |
| M4 | Qué mide la PACF, en qué difiere de la ACF, usarlas juntas para identificar | E1 la pide (4021) y la solución **no la usa** | — | `explorador-acf-pacf` (selector; tarea implícita en el intro) | **NADA** |
| M5 | φ separa estacionariedad de no estacionariedad; raíz unitaria; qué añade la deriva | — | Q6 | `ar1-phi` (φ + interruptor ∇; **tarea explícita**, 2813–2816 y 2828–2838, con las respuestas escritas) | φ y raíz unitaria: Q6 + simulador. **Deriva y tendencia determinista vs estocástica (2841–2861): NADA**; raíz del polinomio (2804–2808): NADA |
| M6 | Aplicar e interpretar ADF y KPSS; nulas opuestas; reconocer cuándo una prueba miente | E2, E4, E5 | Q5 | `montecarlo-adf` (estático) | Interpretar: sí (Q5, E4). «Miente»: sí (E2, E5). **Aplicar a una serie nueva y elegir la especificación (KPSS de nivel o de tendencia, k del ADF): NADA**; las filas «no rechaza / no rechaza» y «rechaza / rechaza» de la tabla 2973–3004: nunca |
| M7 | Diferencias regulares y estacionales; cuántas; sobrediferenciación | E1, E3 | Q3, Q4, Q7 | `diferenciacion` (serie + d; **solo regulares**; la lectura da el «d de varianza mínima») | La mejor cubierta. La trampa de aplicar la regla de la varianza a la serie estacional cruda solo aparece en la pista del E1 |
| M8 | Estabilizar la varianza con log o Box–Cox; elegir λ con criterio; **deshacer** la transformación | E1 (decidir no transformar; la pista lo decide) | Q8 | `box-cox` (λ; la lectura da el λ óptimo) | Elegir λ en una serie donde importe: NADA. **Deshacer (`InvBoxCox`, mediana vs media, 3636–3641): NADA** |
| M9 | Encadenar todo en un procedimiento reproducible; situarlo en ciencia de datos; autoevaluar | E1 | el quiz | `ciclo` del pipeline (no es simulador) | Pipeline: E1, cuya solución no sigue el `preparar()` del módulo. **Fuga de información (3937–3940): NADA** |

Reparto del quiz por etiqueta `modulo`: M1 1 · M3 1 · M5 1 · M6 1 · M7 3 · M8 1 · **M2, M4, M9: 0**.
Reparto de los ejercicios: M6 tres (E2, E4, E5), M7 dos (E1, E3), M8 y M9 dentro de E1.
**Tres de los cinco ejercicios son sobre el ADF.**

**Objetivos sin ninguna práctica dentro del capítulo:** el M4 entero (PACF); y como
sub-objetivos declarados: estricta vs débil (M1), incorrelación vs independencia (M2), calcular
la ACF (M3), deriva y tendencia determinista vs estocástica (M5), aplicar ADF/KPSS a una serie
nueva eligiendo la especificación (M6), deshacer la transformación (M8) y la fuga de información
(M9).

---

## 2. Fichas del quiz (`AUTOEVALUACIONES['cap2']`, 5893–6075)

Comportamiento del motor que condiciona las fichas: en `opcion` y `grafico` el primer fallo
deshabilita la opción elegida, muestra la `pista` y deja reintentar (5372–5376); en `multiple` el
primer fallo dice además **cuántas de las marcadas están bien y cuántas faltan** (5331–5335); el
resultado suma los aciertos al primer y al segundo intento (5115–5119, 5129). Una pista que da
el criterio convierte el segundo intento en gratuito.

**Claves: las ocho son correctas** (comprobadas en §0.3; ninguna clave incorrecta).

Hallazgos transversales:

- **El aviso dice «Seis preguntas» (4002) y hay ocho** (el mismo error que el cap. 1).
- **Tamaño: en los cinco ítems de una sola respuesta la correcta es la opción más larga**
  (caracteres visibles; `longitud_opciones.out`): Q1 55 vs ≤ 45 · Q3 90 vs ≤ 57 · Q5 50 vs ≤ 49 ·
  Q6 83 vs ≤ 51 · Q8 126 vs ≤ 66. **Elegir siempre la más larga da 5 de 5.** En Q4 (múltiple)
  marcar las tres más largas falla (c, d, e), pero ahí la pista da el número.
- **Posición**: repartida y vigilada. `audita_posicion_correcta.py`: orden 3 1 4 2 4, ninguna
  posición por encima del 40 %, racha máxima 1, las tres correctas de Q4 no seguidas ([1, 3, 4]).
- **Pistas: las ocho dan el criterio o la operación**, no por dónde entrar (detalle en cada ficha).
- **Recuerdo, no transferencia**: Q2, Q5, Q6, Q7 y Q8 se contestan con una cifra o una frase que
  el capítulo ya escribió para la misma serie (detalle en cada ficha). Nada pasa de
  **comprender**; Q3 y Q6 son lectura de gráfico, sobre gráficos ya vistos.
- **Filtraciones**: la respuesta de Q2 está en pantalla en el M4 (la lectura del explorador,
  5626, muestra «banda = ±0.1633» con la serie por defecto, AirPassengers, n = 144); la de Q7 está
  en el M7 (3355–3358, misma T, misma suma). La retro de Q3 (5944) da el patrón ∇₁₂∇ para una
  serie mensual estacional, que es la respuesta del E1 y del E3.
- **Numéricas**: Q2 (tolerancia 0.0006) acepta 0.163 y 0.1633 y rechaza 0.164; Q7 es un entero
  con tolerancia 0. Ninguna castiga el redondeo razonable.

| # | Línea | Tipo · etiqueta | Nivel | Veredicto |
|---|---|---|---|---|
| Q1 | 5894 | opción · M1 | recordar (aviso 2286) | se puede mejorar |
| Q2 | 5922 | numérica · M3 | aplicar (una división) | **hay que rehacer** |
| Q3 | 5932 | gráfico · M7 | comprender | se puede mejorar |
| Q4 | 5963 | múltiple · M7 | comprender | se puede mejorar |
| Q5 | 5978 | opción · M6 | comprender (los números son los de la TRM) | se puede mejorar |
| Q6 | 6006 | gráfico · M5 | comprender (el gráfico ya se vio dos veces) | se puede mejorar |
| Q7 | 6037 | numérica · M7 | recordar (la suma está en 3355–3358) | **hay que rehacer** |
| Q8 | 6047 | opción · M8 | recordar (lista de 3629–3633) | **hay que rehacer** |

**Q1 · ¿es estacionaria una serie estacional? (5894–5921).** Clave correcta. Los distractores
a) y b) son errores reales con buena retro; d) («sin aplicar una prueba ADF») es plausible y su
retro enlaza con el M6. Pero la pregunta repite el aviso del M1 (2286–2289) y la pista (5898)
termina con «¿Es la misma esperanza en diciembre que en febrero?», que es la respuesta. La
correcta es la más larga (+10). *Mejora*: dar una serie (o un correlograma) y pedir qué condición
falla; o confrontar estricta y débil, que nadie practica.

**Q2 · semiancho de la banda con T = 144 (5922–5931).** Clave 0.1633 = 1.96/12 (0.16333),
tolerancia adecuada. Mide una división; la pista (5926) da √144 = 12 y dice «Solo tienes que
dividir»; la cifra está en pantalla en la lectura del explorador del M4. La retro del fallo es
buena (diagnostica 0.0136). *Rehacer*: preguntar algo que exija entender la banda —p. ej. con
T = 144 y 24 rezagos, cuántas barras se esperan fuera por azar (1.2), o si r₅ = 0.15 es evidencia
de algo— en vez de calcularla.

**Q3 · correlograma de ∇log AP (5932–5962).** Clave correcta (r₁₂ = 0.841, banda ±0.164,
verificado). Buenos distractores: c) («falta otra regular») y d) son confusiones reales y su
retro las desmonta con cifras. Defectos: la correcta es la más larga por 33 caracteres y es la
única con un mecanismo; la pista (5938) señala «alguno que signifique algo especial para una
serie mensual», o sea el 12; la retro de b) (5949) dice que con ruido blanco se saldrían «una o
dos de 24 —, no ninguna» y que lo que delata a esta «no es que se salga»: confuso, cuando el
argumento simple está a mano (se salen **10 de 24**, medido). El gráfico es el de la opción
`d_log_airpassengers` del explorador del M4. *Mejora*: longitudes, pista sin el criterio, retro
de b) con el 10 de 24.

**Q4 · señales de sobrediferenciación (5963–5977).** Clave defendible con un reparo: la opción d)
(«Queda inducido un MA(1) con θ = −1, que además no es invertible») no es una *señal* que se
observe en los datos sino la consecuencia teórica (M7, 3458–3462); para verla habría que
ajustar un modelo, que es del cap. 3. b) y e) son buenos distractores. Defectos: **ninguna opción
lleva `retro` propio** (5969–5973), contra la regla del motor (5048–5053), así que el desglose del
fallo muestra «La marcaste y no va: <texto>» sin explicación; la pista (5967) dice «Son tres» y
enumera los tres temas en el orden de las correctas (dispersión, autocorrelación, modelo), y el
motor añade cuántas faltan: el segundo intento es gratuito. *Mejora*: retro por opción; cambiar d)
por una señal observable (p. ej. «la PACF decae despacio y con todos los valores negativos»: la
teórica de ∇ de un ruido blanco es −1/(k+1), −0.500, −0.333, −0.250…, medido con `ARMAacf`) o declararla
consecuencia; pista sin conteo ni enumeración.

**Q5 · ADF p = 0.58 y KPSS p < 0.01 (5978–6005).** Clave correcta. Los tres distractores son las
otras tres filas de la tabla 2973–3004: buen diseño. Pero los números son los de la TRM del M6
(p = 0.586 y < 0.01, 3027–3029) y la retro de la correcta lo dice; la pista (5982) termina en
«"no rechazar" en una y "rechazar" en la otra puede significar lo mismo», que es la respuesta. La
correcta es la más larga por un carácter (empate práctico). *Mejora*: otros p-valores (p. ej. el
caso «rechaza / rechaza» que nadie practica) y pista que pida escribir las dos H₀ sin resolver.

**Q6 · ACF de la caminata (6006–6036).** Clave correcta (r₁ = 0.961, r₁₂ = 0.488, verificado). El
gráfico es el mismo que el M3 muestra en `correlogramas-comparados` (2477–2481) con las mismas
cifras en la tabla (2507) y en el M4 (2688): se responde reconociéndolo. La correcta es la más
larga (+32) y nombra el mecanismo; la pista (6012) describe la forma y pregunta «¿A qué proceso
del Módulo 5 corresponde?». La retro de c) argumenta con que «esta serie toma valores negativos»
(cierto: mínimo −14.84), algo que el estudiante no puede ver en una ACF. *Mejora*: una ACF de una
serie no mostrada (p. ej. un AR(1) con φ = 0.95, el «caso difícil» de 2832–2834, frente a una
caminata) y pedir qué falta para decidir.

**Q7 · cuántas observaciones deja ∇₁₂∇ (6037–6046).** Clave 131 correcta, tolerancia 0 bien. El
M7 hace la misma cuenta con la misma T (3355–3358: «deja 144 − 12 − 1 = 131») y la pista (6041) da
la regla. La `retroFallo` sí es buena (diagnostica 143, 132 y 120). *Rehacer*: transferir
(trimestral con ∇₄∇ y T = 40; o mensual con T = 36, la fila del 36 % de 3366) o preguntar qué
fracción se pierde.

**Q8 · por qué el log y no λ = −0.295 (6047–6074).** Clave correcta y cifras verificadas (88 %,
84 %). Es una paráfrasis de la nota del M8 (3629–3633); la correcta es la más larga por 60
caracteres y la única con tres partes; la pista (6051) descarta a) y apunta a d) («quién tiene que
*entender* el resultado y qué pasa al deshacer»). Además, la premisa «este capítulo recomienda
usar el logaritmo» choca con el `preparar()` del M9, que sobre AirPassengers aplica Box–Cox con
λ = −0.2947 (3858–3859, 3877; medido). *Rehacer*: dar el criterio de Guerrero de otra serie
(p. ej. `UKgas`, λ = −0.446, o `JohnsonJohnson`, 0.154; §8) y pedir la decisión; y alinear el M9
con el M8.

---

## 3. Fichas de los ejercicios guiados (M9)

Todos están en el M9, después del quiz; todos se pueden resolver con lo enseñado antes salvo la
prueba de Ljung–Box del E3. La consigna general (4015–4017) promete que «la pista te dice por
dónde entrar sin darte la respuesta».

| # | Línea | Nivel (enunciado / solución) | ¿Dice qué entregar? | Pista | Reproducible | Veredicto |
|---|---|---|---|---|---|---|
| E1 | 4019 | aplicar + evaluar / aplicar | sí (d, D y tres señales) | toma las dos decisiones por el estudiante | sí | se puede mejorar |
| E2 | 4084 | aplicar + explicar / aplicar | sí (un %) | buena (pide predecir) | sí | se puede mejorar |
| E3 | 4124 | analizar / analizar | sí (cuál y por qué) | da el criterio; remite a una caja ambigua | sí | se puede mejorar |
| E4 | 4194 | aplicar (copiar y correr) / — | sí (sí/no) | adelanta la respuesta | sí (hoy: n = 142, no cambia) | se puede mejorar |
| E5 | 4229 | evaluar / criterios | parcial | da el experimento | n/a (abierto) | se puede mejorar |

**E1 · co2: cuántas diferencias (4019–4082).**
- *Enunciado*: grafica, ACF **y PACF**, «aplica el pipeline del Módulo 9», d y D, justifica con
  las tres señales. Claro y con entregable.
- *Enunciado y solución no hablan de lo mismo en tres puntos*: (1) el pipeline del M9
  (`preparar()`, 3856–3873) **toma el logaritmo** de co2 (λ = −0.034, \|λ\| < 0.25; medido) y la
  solución dice «Se trabaja sin transformar» (4046–4047); las decisiones d = 1 y D = 1 salen
  iguales, pero el estudiante que obedece el enunciado obtiene otra serie final (varianza
  1.38 × 10⁻⁶ en log frente a 0.154). (2) La PACF se pide y nunca se calcula. (3) La señal del
  correlograma solo se da sobre la serie cruda (r₁, r₁₂; 4058, 4069–4070), que justifica «hay que
  diferenciar» pero no «una regular más tras ∇₁₂»; la que lo justifica, ∇₁₂ sola con r₁ = 0.800 y
  15 de 24 fuera (medido), no aparece.
- *La pista (4033–4037) decide por el estudiante*: dice que Guerrero «no te va a servir» y que la
  varianza se compara tras ∇₁₂. Lo segundo **enseña algo que el capítulo no enseña**: la regla
  del M7 («El mínimo señala el d correcto», 3398–3399), aplicada a co2 cruda, da d = 2 (224 → 1.456
  → 0.855 → 1.226; medido). Esa limitación de la regla debería estar en el M7, no escondida en una
  pista.
- *Interpretación*: «λ queda mal identificado» es defendible —la curva de Guerrero es plana
  entre −0.5 y 0.5 (0.072 a 0.073)—, pero el mínimo cae en λ ≈ 0, así que lo que muestra es que el
  log y la serie sin transformar dan casi lo mismo, no que Guerrero «no sirva». La lectura de r₁ =
  −0.302 como huella MA es correcta; no comenta r₁₂ = −0.420, que también se sale y es la huella
  del MA estacional.
- *Veredicto*: **se puede mejorar** (alinear con `preparar()` o cambiar el enunciado; pedir la
  PACF o quitarla; pista que pregunte en vez de decidir; llevar al M7 la advertencia de la
  varianza en series estacionales).

**E2 · 500 caminatas y el ADF (4084–4122).**
- *Enunciado*: claro; pide un porcentaje y una explicación. El estudiante tiene que escribir un
  Monte Carlo que el capítulo no modela (el del M6 vive en `genera_cap2.R`, no en la página).
- *Pista*: la mejor del capítulo: pide predecir antes de correr y nombra la diferencia a buscar
  sin darla.
- *Solución*: cifras exactas. Dos problemas de interpretación: (1) «La única diferencia entre los
  dos experimentos es que a aquellas caminatas se les sumó un componente estacional» (4118) es
  falso: T = 100 frente a 144 y semillas 2026 frente a 7; el control limpio ya está en el propio
  M6, la barra de amplitud 0 (3.2 %, 3131), así que el ejercicio repite un resultado publicado.
  (2) Compara 4.6 % con 5 % sin el error Monte Carlo (±0.97 pp; IC 95 % [2.9 %, 6.8 %]; con otras
  20 semillas sale entre 2.6 % y 5.2 %), que es justo la lección estadística que esa comparación
  pide.
- *Veredicto*: **se puede mejorar** (otro T o la variante con tendencia/deriva, el IC de la tasa,
  y comparar con la barra 0 del M6).

**E3 · USAccDeaths: ∇, ∇₁₂, ∇₁₂∇ (4124–4192).**
- *Enunciado*: claro, con criterio (varianza y correlograma). Habla de «residuales» (4126) cuando
  son series diferenciadas: no hay modelo ni residuos todavía.
- *Solución*: cifras exactas. Usa **Ljung–Box** (`Box.test`, 4159, 4171, 4187), que el capítulo no
  enseña en ningún módulo: es su primera aparición. Con LB p = 0.033 también ∇₁₂∇ rechaza ruido
  blanco al 5 %; la solución lo dice a medias («el único que no está pegado a cero»).
- *Pista (4137–4140)*: da el criterio (mirar r₁₂ y los rezagos fuera) y remite a «la caja de
  advertencia del Módulo 7», que tiene tres (3272, 3452, 3476); la pertinente es la del orden
  (3272) o el párrafo 3467–3473.
- *Filtración*: la «advertencia» final (4185–4190: el r₁ negativo es huella MA y no
  sobrediferenciación) ya la dio la solución del E1 (4077–4080), que el estudiante abre antes.
- *Veredicto*: **se puede mejorar** (enseñar Ljung–Box en el M2 o quitarlo; «series
  diferenciadas»; pista con la caja concreta y sin el criterio).

**E4 · TRM actualizada (4194–4227).**
- *Enunciado*: claro. La tarea es copiar y correr el bloque del M6 (la pista lo dice: «listo para
  copiar», 4208); demanda cognitiva mínima.
- *Pista*: «los tipos de cambio son el ejemplo clásico de caminata aleatoria con deriva, así que
  ¿esperas que…?» da la respuesta.
- *Comprobado hoy*: con la descarga del 16 nov 2026 (n = 142, hasta 2026-10) el veredicto no
  cambia (cifras en §0.3), y el ADF sobre ∇TRM queda entre p = 0.010 y 0.028 en todas las
  ventanas probadas. La frase «la conclusión sobre una raíz unitaria es una propiedad estructural
  de la serie, no un accidente de la ventana» (4221–4223) se sostiene en esta muestra, pero es más
  fuerte de lo que un solo ejercicio prueba.
- *Veredicto*: **se puede mejorar** (que el estudiante elija y justifique la especificación
  —KPSS de nivel o de tendencia, k—, o que pruebe la ventana, que es lo que daría contenido a la
  pregunta).

**E5 · IA como tutor (4229–4267).**
- *Enunciado*: pide contrastar y separar lo verificado de lo no verificado; el entregable está
  implícito (no dice formato ni extensión).
- *Pista*: da el experimento falsable (k = 12), que es la primera evidencia del M6 (3071–3107):
  «verificar ejecutando código» queda en re-correr la tabla del módulo.
- *Criterios*: buenos y concretos; la cifra citada (−6.42 → −1.53) coincide. El punto 4
  (4259–4261, errores «frecuentes» del asistente) es una afirmación sin fuente: no es una cita,
  pero tampoco se puede contrastar.
- *Veredicto*: **se puede mejorar** (aplicarlo a una serie que el capítulo no resolvió, p. ej.
  `nottem`, estacional sin tendencia, donde el ADF rechaza y KPSS no; §8).

---

## 4. Simuladores como práctica

| id | Línea (HTML · JS) | Mód. | Controles | Tarea que plantea | Nivel |
|---|---|---|---|---|---|
| `panel-estacionariedad` | 2242 · 5544 | M1 | ninguno | ninguna | — |
| `ruido-blanco` | 2343 · 5556 | M2 | ninguno | ninguna; la lectura cuenta las barras dentro | — |
| `correlogramas-comparados` | 2468 · 5574 | M3 | ninguno | ninguna; las etiquetas dan la lectura | — |
| `explorador-acf-pacf` | 2668 · 5597 | M4 | selector de 8 series | implícita («Fíjate en…»); la lectura da banda, r₁, fuera, `ndiffs`, `nsdiffs` | comprender |
| `ar1-phi` | 2811 · 5644 | M5 | φ (0–1.05) + interruptor ∇ | **explícita** (2813–2816) y tres pruebas en 2828–2838, con sus respuestas | comprender/analizar |
| `montecarlo-adf` | 3120 · 5720 | M6 | ninguno | ninguna | — |
| `diferenciacion` | 3378 · 5747 | M7 | serie (3) + d (0–3) | implícita; la lectura **da el «d de varianza mínima»** (5796) | comprender |
| `box-cox` | 3593 · 5814 | M8 | λ (−1–2) | implícita; la lectura da el λ óptimo de R | comprender |

Cuatro de ocho son estáticos; cuatro tienen controles; uno (`ar1-phi`) plantea una tarea
concreta. Ninguno pide una predicción antes de mover. `diferenciacion` solo hace diferencias
regulares (el objetivo del M7 incluye las estacionales) y su lectura resuelve la pregunta que el
estudiante debería hacerse. El explorador del M4 es el único sitio con PACF interactiva, y no pide
nada sobre ella.

## 5. Bloques de código como práctica

Ejemplos resueltos, ninguno con un «ahora tú». Lo que afecta a la práctica:

- **M9 `preparar()` (3856–3873)** usa Box–Cox con el λ de Guerrero cuando \|λ\| ≥ 0.25, así que
  sobre AirPassengers no usa el log que recomiendan el M8 y Q8; el E1 pide aplicarlo y su
  solución no lo sigue.
- **Ningún bloque modela un Monte Carlo** (E2 lo exige), ni Ljung–Box (E3 lo usa), ni
  `InvBoxCox` en un pronóstico (el M8 solo deshace sobre la misma serie, 3655–3658).
- Ningún bloque lleva `#>`: el verificador de bloques no ve sus cifras (§0.1).

## 6. Progresión

- **Toda la práctica escrita está al final.** Entre el M1 y el M8 no hay una sola pregunta de
  control; solo simuladores, de los que uno pide algo concreto. El quiz y los cinco ejercicios
  están en el M9.
- **Orden de los ejercicios**: E1 (el más integrador: M3–M7–M8–M9) va primero; luego E2 (M6), E3
  (M7), E4 (M6), E5 (M6). No va de lo simple a lo integrado, y tres de cinco giran sobre el ADF.
- **Quiz**: etiquetas 1, 3, 7, 7, 6, 5, 7, 8: casi en orden de módulos, sin ítems de
  integración y con el M7 sobrerrepresentado.
- **Integración**: solo E1 recorre el pipeline, y su solución se aparta de él.

## 7. Frente al texto guía (FPP3)

| FPP3 | Tipo de tarea | ¿Equivalente en el cap. 2? |
|---|---|---|
| 9.11 ej. 1 (arima.txt 1025–1031) | ACF de ruido blanco con 36, 360 y 1000 datos: por qué la banda y las barras cambian | Parcial: Q2 calcula la banda con un T; no compara tamaños ni explica la variación muestral |
| 9.11 ej. 2 (1033) | Precios de acciones: serie, **ACF y PACF**, explicar por qué no es estacionaria | No: la PACF no se practica en ninguna parte |
| 9.11 ej. 3 (1035–1039) | Box–Cox **y** orden de diferenciación para tres series | Parcial: E1 una sola serie, donde la transformación no importa |
| 9.11 ej. 4 (1041) | Escribir las diferencias elegidas con el operador B | No: B se enseña (2804–2808, 3261–3268) y no se practica |
| 9.11 ej. 5 (1043) | Serie personal: orden de diferenciación tras transformar | No: todos trabajan las mismas series |
| 2.10 ej. 9 (graphics.txt 722) | Emparejar gráficos de tiempo con ACF | No |
| 2.10 ej. 10 (726) | ¿En qué se diferencia del ruido blanco? ¿Qué pasa con la ACF si se alarga la muestra? | No |
| 2.10 ej. 11 (728–739) | Cambios diarios de una acción: ¿parecen ruido blanco? | No (el aviso del M2 sobre rendimientos, 2338–2340, no se practica) |
| 3.7 ej. 2, 4, 5 (decomposition.txt 500–511) | Decidir si transformar y con qué λ en series dadas | No (solo Q8, de recuerdo) |
| 3.7 ej. 3 (507) | Por qué Box–Cox **no ayuda** en una serie concreta | No, aunque es el argumento del E1, decidido por la pista |

Tipos de tarea ausentes: emparejar serie ↔ correlograma, leer una PACF, escribir con B,
serie por estudiante, decidir λ donde importe, y cualquier comparación entre tamaños de muestra.

## 8. Datos

- Módulos, simuladores y quiz giran sobre **AirPassengers**, la **TRM** y las dos series
  simuladas (`set.seed(2026)`); los ejercicios añaden `co2` y `USAccDeaths`. El quiz se responde
  con cifras del texto (0.1633, 131, 0.961/0.488, 0.58/<0.01, −0.295) y E4/E5 re-corren el M6.

Series de R base medidas aquí (`series_candidatas.out`), con dónde convendrían:

| Serie | Medido | Dónde |
|---|---|---|
| `lh` (48) | PACF fuera solo en 1; r₁ = 0.576; ADF p = 0.046, KPSS p > 0.10 | M4: ACF que decae y PACF que se corta, corta y real |
| `LakeHuron` (98) | PACF fuera en 1, 2; ADF p = 0.254, KPSS nivel p = 0.010; sin la recta: KPSS nivel p = 0.10 y ADF sigue en 0.254 | M4 (PACF en 2) y M5/M6: tendencia determinista frente a estocástica, caso no limpio |
| `WWWusage` (100) | KPSS nivel p = 0.054, de tendencia p = 0.017; ADF p = 0.311 | M6: la especificación cambia la decisión |
| `nottem` (240, mensual) | ADF p = 0.010, KPSS p > 0.10, `ndiffs` 0, `nsdiffs` 1; λ = 0.042 | M6/E5: estacional sin tendencia, donde el ADF rechaza y el KPSS no, pero `nsdiffs` pide una estacional |
| `UKgas`, `JohnsonJohnson` | λ = −0.446 y 0.154 | M8/Q8: decidir λ donde no da igual |
| `sunspot.month` | mínimo 0: Guerrero avisa «strictly positive data» (λ = 0.449 igualmente) | M9 paso 2: el caso «ceros o negativos» (3791) |
| rendimientos del DAX (`EuStockMarkets`, 1859) | rendimientos: 2 de 24 fuera, LB p = 0.515; cuadrados: 10 de 24 fuera, LB p ≈ 0 | M2: incorrelación no es independencia |
| `log(UKgas)` (108, trimestral) | ADF p = 0.570, `ndiffs` 1, `nsdiffs` 1 | M7/Q7: ∇₄∇ trimestral, para transferir la cuenta de observaciones |

## 9. Lista de huecos (por prioridad)

1. **M4 — PACF: cero práctica.** Ni quiz, ni ejercicio (E1 la pide y no la usa), ni tarea en el
   explorador. Tipo FPP3 9.11 ej. 2 y 2.10 ej. 9: emparejar series con su par ACF/PACF; `lh`,
   `LakeHuron`. Nivel aplicar/analizar.
2. **M6 — aplicar ADF y KPSS a una serie nueva eligiendo la especificación** (nivel/tendencia, k),
   y las dos filas de la tabla que nadie toca (las dos no rechazan; las dos rechazan). Hoy E2, E4 y
   E5 re-corren los ejemplos del módulo. `WWWusage`, `nottem`.
3. **M5 — deriva y tendencia determinista vs estocástica.** El aviso 2855–2861 dice que exigen
   tratamientos opuestos y que distinguirlas «es justamente el trabajo» del M6; nadie lo practica.
4. **M8 — elegir λ donde importe y deshacer la transformación** (FPP3 3.7 ej. 2–5): `UKgas`,
   `JohnsonJohnson`; y el sesgo de la vuelta (mediana) del aviso 3636–3641.
5. **M2 — incorrelación ≠ independencia** con rendimientos reales (DAX, medido) y **Ljung–Box**,
   que el E3 usa sin haberlo enseñado.
6. **M7 — la regla de la varianza en series estacionales** (co2 cruda daría d = 2) debería estar
   en el módulo y no solo en la pista del E1; el simulador `diferenciacion` no tiene diferencia
   estacional y su lectura da el d.
7. **M1 — estricta vs débil**, y **M3 — calcular r_k** a mano (divisor T) y la lectura de la banda
   con muchos rezagos (FPP3 9.11 ej. 1, distintos T).
8. **M9 — fuga de información** (estimar λ solo con entrenamiento): nada; y alinear `preparar()`
   con la recomendación del log del M8.
9. **Práctica intermedia**: una pregunta de control al final de M3, M4, M6 y M7.
10. **Quiz**: «Seis» → ocho (4002); igualar longitudes (5 de 5 con «la más larga»); pistas que no
    den el criterio (las ocho); retro por opción en Q4 y sacar de ahí la señal no observable;
    rehacer Q2, Q7 y Q8 como transferencia; retro de b) en Q3 con el 10 de 24.
11. **Ejercicios**: E1 alineado con el pipeline y con la PACF; E2 comparado con la barra 0 del M6
    y con su IC; E3 sin «residuales», con Ljung–Box enseñado y la caja concreta; E4 con una
    decisión de especificación; E5 sobre una serie no resuelta.
12. **Verificación**: las cifras de los bloques y de las soluciones no están al alcance de
    `verifica_bloques_cap6.py` (van en `# …`, no `#>`): 0 de 0 contrastadas.
