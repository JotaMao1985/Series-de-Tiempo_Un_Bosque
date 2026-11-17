# Revisión de par académico · Capítulo 2 «Estacionariedad, ACF y PACF»

Archivo: `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` en el commit `4b71366`. Las líneas remiten a
ese archivo.
Lente: corrección y rigor. Se revisan las definiciones y los enunciados, las fórmulas, la lógica del JS de los
simuladores, los bloques de R y Python, las cifras de la prosa, las tablas, los ejercicios y el quiz
(`AUTOEVALUACIONES['cap2']`, l. 5893–6075), y las interpretaciones de las pruebas.

Entorno de comprobación: R 4.6.0 (tseries 0.10.62, forecast 9.0.2, urca 1.3.4, feasts 0.5.0; `fpp3` instalado).
Python 3 (statsmodels 0.14.6, pandas 2.3.3, scipy 1.15.3); `pmdarima` **no** está instalado. node para el JS.
Los guiones están en `diag/`, junto a este archivo, y cada uno tiene su salida en un `.out`:

- `diag/v1.R`: M2–M8, desde cero.
- `diag/v2.py`: los bloques de Python, ejecutados con `MPLBACKEND=Agg`.
- `diag/v3.R`: el pipeline del M9, los ejercicios 1–3, las cifras del quiz y las referencias leídas en la ayuda de R.
- `diag/v4_simulador_ar1.js`: el simulador «El deslizador de φ», con las funciones extraídas del propio HTML.
- `diag/v5_trm_descarga.R`: el código de descarga del M6 tal cual y el ejercicio 4. Necesita internet.

`diag/datos_cap2_incrustado.json` es el `DATOS_CAP2` de la l. 4310. Es idéntico a
`precalculo/salidas/cap2_estacionariedad.json`, y todas sus cifras se reprodujeron recalculando desde cero.

Abreviaturas: `AP <- AirPassengers`; `lx <- log(AP)`; `trm` = la serie de `precalculo/salidas/datos_series.json`
(138 meses, 2015-01 a 2026-06); `d1 <- diff(lx)`; `d12 <- diff(lx, lag = 12)`.
En la columna «evidencia», **R/Py/JS** marca lo que se comprobó ejecutando. **fuente** marca una cita leída.
**razonamiento** marca lo que es juicio.

---

## M1 · Estacionariedad (2180–2300)

M1 está limpio. Las definiciones de estacionariedad estricta y débil, la relación entre ellas (estricta + varianza
finita ⇒ débil; coinciden en el caso gaussiano), la tabla de condiciones que falla cada serie
(Var = tσ² en la caminata) y la advertencia «estacional ≠ estacionaria» son correctas. La advertencia coincide
con FPP3 (`arima.txt:9`: «time series with trends, or with seasonality, are not stationary»).

---

## M2 · Ruido blanco (2305–2416)

Reproducido: banda ±0.1386 con T = 200; 0 de 24 rezagos fuera; 24 × 0.05 = 1.2 (v1).

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2358–2360 | imprecisión | «Si la serie es realmente ruido blanco, cada autocorrelación muestral se distribuye aproximadamente N(0, 1/T)» | Ese resultado pide ruido blanco **i.i.d.** (con cuarto momento finito), no solo incorrelado. El propio módulo acaba de advertir (2336–2340) que incorrelación no es independencia y que en un ARCH los cuadrados tienen estructura. En ese caso la varianza de r_k no es 1/T y la banda no vale. Falta la condición. | fuente: Shumway y Stoffer 3.ª ed., p. 29 (`shumway2011time/p0042.txt:53`): «The general conditions are that xt is iid with finite fourth moment.» |
| 2361–2362 | divergencia (menor) | «Una barra fuera de la banda no es evidencia de nada; un patrón sí.» | FPP3 considera evidencia una sola barra **grande** fuera de la banda. El capítulo tiene razón para una barra que apenas se asoma, pero la frase absoluta contradice el criterio de la lectura recomendada. | fuente: FPP3 §2.9 (`graphics.txt:647`): «If one or more large spikes are outside these bounds, or if substantially more than 5% of spikes are outside these bounds, then the series is probably not white noise.» |

---

## M3 · Autocorrelación y correlograma (2421–2572)

Reproducido: r₁ = −0.0776 en el ruido; r₁ = 0.9612 y r₁₂ = 0.4877 en la caminata; AP r₁, r₂, r₁₂ = 0.9480, 0.8756,
0.7604 en R y en Python (`adjusted=False`). r₁₂ es un pico local en AP (r₁₁ = 0.743, r₁₃ = 0.713). Las fórmulas de
γ̂_k y r_k y el divisor T coinciden con el JS `calcularACF` (l. 4779).

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2515–2517 | error | Fila «Decaimiento rápido (exponencial)»: «∇TRM: r₁ = 0.088, **todo lo demás dentro de la banda**» | (i) Es falso: r₈ = −0.190 se sale de la banda ±0.1675. (ii) Además, r₁ = 0.088 está **dentro** de la banda: el ejemplo no ilustra un decaimiento exponencial, sino un correlograma casi de ruido blanco con un pico suelto en k = 8. | R (`v3.R`): `acf(diff(trm),24)` → r₈ = −0.1903; `which(abs(r) > 1.96/sqrt(137))` → **8** |

---

## M4 · PACF (2577–2754)

Reproducido: las fórmulas de Durbin–Levinson (φ_kk, v_{k−1} = γ₀(1 − Σφρ), v_k = v_{k−1}(1 − φ_kk²) y la
actualización de φ_kj) son correctas. La recursión, reimplementada, coincide con `stats::pacf` hasta 9e-15. La
diferencia máxima de 6.2e-5 de la nota de 2661–2665 sale exacta: 6.19e-5, en `dd_log_airpassengers`. El JS
`calcularPACF` (l. 4946) es la misma recursión. La PACF de la caminata roza la banda en k = 4 (−0.140 frente a
±0.139), así que «prácticamente nada después» es justo.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2654–2656; 2665; 2742 | imprecisión | «Esta es **exactamente la recursión** que implementan `pacf()` de R, el método `ywm` de statsmodels…»; «# method="ywm" reproduce la recursion de Durbin-Levinson» | `ywm` da los mismos números, pero no por la recursión: `pacf_yw` resuelve Yule–Walker orden por orden. El método de statsmodels que implementa Levinson–Durbin es `ldb`. La coincidencia numérica, que el capítulo verifica, es cierta. Lo que no lo es es la afirmación sobre el algoritmo. | Py (`v2.py`): `inspect.getsource(pacf_yw)` contiene `yule_walker(` y no `levinson_durbin`; docstring de `pacf`: «"ldb" or "ldbiased" : Levinson-Durbin recursion without bias»; máx\|ywm − pacf R\| en AP = 4.9e-5 |
| 2697–2699 | divergencia (menor) | Regla de identificación: «las dos decaen sin cortarse → modelo **ARMA(p,q)**» | FPP3 advierte que, con p y q positivos, los gráficos no ayudan a elegir los órdenes. La tercera viñeta, puesta en paralelo con las dos primeras, sugiere una identificación que no da. Basta añadir «sin indicar p ni q». | fuente: FPP3 §9.5 (`arima.txt:356`): «If p and q are both positive, then the plots do not help in finding suitable values of p and q.» |

---

## M5 · Caminata aleatoria y raíz unitaria (2759–2919)

Reproducido: `all.equal(ar1(1, e), cumsum(e))` → TRUE en R y en Python. La raíz del polinomio característico y la
condición |φ| < 1 son correctas. El simulador (l. 5644) corre de 0 a 1.05 con el mismo ruido, como dice la prosa.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2835–2837 | error | «Con la primera diferencia activada, **cualquier φ** produce algo que *ya* se parece a ruido blanco… y con φ pequeño produce autocorrelación negativa en el rezago 1» | Para un AR(1) estacionario, ρ₁(∇y) = −(1 − φ)/2. Con φ = 0 eso es −0.5, que no se parece a ruido blanco. Con φ = 1.05, que el deslizador permite, la diferencia sigue siendo explosiva. La frase solo vale cerca de φ = 1. | JS (`v4`, mismas funciones y semilla que el simulador): con ∇, φ = 0 → r₁ = **−0.506**, 3 rezagos fuera; φ = 1.05 → r₁ = **0.951**, **24 de 24** fuera, últimos valores ≈ −9e2 |
| 2850–2852 | imprecisión | «El término $ct$ produce una tendencia lineal, pero se trata de una **tendencia estocástica**: la serie sube en promedio $c$ por periodo mientras deambula alrededor de esa pendiente» | $ct$ es la parte **determinista**; la tendencia estocástica es $\sum\varepsilon_i$. La desviación respecto a la recta, $y_t - y_0 - ct$, es una caminata con varianza $t\sigma^2$, que no vuelve a la recta. «Deambula alrededor» sugiere la reversión que caracteriza justo a la tendencia determinista que el aviso siguiente contrapone. | razonamiento, a partir de la fórmula de l. 2847 |
| 2858–2860 | imprecisión | «Aplicar el tratamiento equivocado **deja la serie tan mal como estaba**» | Vale para quitar una recta a una caminata. En la otra dirección no: diferenciar una serie con tendencia determinista da una serie **estacionaria**, aunque con una raíz unitaria en la parte MA (no invertible). Es el problema de sobrediferenciación del M7, no «tan mal como estaba». | fuente: Hamilton, p. 444 (`hamilton1994time/p0459.txt:25–30`): «This is a stationary time series, but a unit root has been introduced into the moving average representation.» |

---

## M6 · Pruebas ADF y KPSS (2924–3233)

Reproducido todo: TRM T = 138; ADF −1.9783 (p 0.5855), KPSS 2.2427 (p < 0.01); ∇TRM −3.8801 (p 0.0172) y 0.2415
(p > 0.10); ADF de AP crudo −7.3186; k = 5; tabla de k sobre log AP: −6.4215, −0.4398 (0.9833), −1.5325 (0.7711),
−2.147 (0.5152); desestacionalizada: ADF −2.1524 (0.513), KPSS-T 0.3864 (p < 0.01); Monte Carlo 3.2, 3.6, 5, 11.2
y 17.6 %. En Python, `adf_como_en_r` da −1.9783/0.6132 y −3.8801/0.0129, y `kpss` da 2.2427 con p = 0.01.
El código de descarga de R y el de Python reproducen los 138 meses, con una diferencia máxima de 0 y 0.01
(v5, v2). La referencia a Banerjee et al. (1993) y la interpolación que se le atribuye coinciden con la ayuda de
`adf.test`. Que statsmodels use MacKinnon coincide con su docstring. **Apoyo al mecanismo:** con `k = 12`, el
falso rechazo del Monte Carlo con amplitud 4 baja del 17.6 % al 2.8 % (v1).

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 2949–2953; 2984–2986; 3057–3058 | imprecisión | ADF con $\alpha + \beta t$: «$H_1$: $\gamma < 0$ (**estacionaria**)»; tabla «Rechaza / No rechaza → Estacionaria»; el ADF de AP «proclama que la serie es estacionaria» | Con tendencia en la regresión, que es lo que hace `adf.test`, la alternativa es estacionariedad **alrededor de una tendencia determinista**, no estacionariedad en nivel. Además, la tabla de la TRM cruza el ADF con tendencia y el KPSS **de nivel**, cuyas hipótesis no son las complementarias. Para la TRM el veredicto no cambia: el KPSS de tendencia también rechaza. Pero el capítulo, que en el M5 insiste en distinguir los dos tipos de tendencia, no dice qué alternativa contrasta. | fuente: Hamilton, p. 501 (`p0516.txt:43–46`), caso 4: «a deterministic time trend added to a stationary AR(1)»; R (`v5`): `kpss.test(trm, null="Trend")` → 0.273, p = 0.01 |
| 3056–3058 frente a 3071–3107 | laguna (menor) | El texto da el ADF de **AirPassengers** (−7.32) y la tabla de k «que se da la vuelta» es de **log(AirPassengers)** (−6.422 con k = 5) | El cambio de serie no se dice. El lector compara −7.32 con −6.42 y no sabe de dónde sale la diferencia. Sobre AP en nivel la conclusión es la misma: con k = 12 da −1.509 (p 0.781). | R (`v1`): `adf.test(AP, k=12)` → −1.5094, p 0.7807; `adf.test(lx, k=5)` → −6.4215 |
| 3137–3138 | imprecisión (menor) | «Las funciones `ndiffs()` y `nsdiffs()` del Módulo 7 **automatizan** justamente ese orden» | Son dos funciones independientes. El orden (primero `nsdiffs`, diferenciar, luego `ndiffs` sobre lo diferenciado) lo aplica el usuario, y ninguna estabiliza la varianza, que es el primer paso del orden que se cita. | fuente: FPP3 §9.1 (`arima.txt:190`): «Because unitroot_nsdiffs() returns 1 …, we apply the unitroot_ndiffs() function to the seasonally differenced data.» |
| 3217–3221 | error (menor) | Comentario Python: «De ahi 0.6132 frente a 0.5855, y 0.0129 frente a 0.0172. La conclusion es la misma en los dos casos; **solo cambia el tercer decimal**.» | En el primer par cambia ya el primer decimal (0.6… frente a 0.5…). La conclusión, en efecto, es la misma. | Py (`v2`) y R (`v1`): 0.6132 frente a 0.5855 |

---

## M7 · Diferenciación (3238–3552)

Reproducido: la tabla de AP (112, 118, 132 … 104, 118, 115, 126); 143, 132 y 131 observaciones; el primer valor
de ∇∇₁₂ es 8 − 3 = 5; 9 %, 22 % y 36 %; la tabla de varianzas y r₁ (0.19488, 0.01135, 0.01823 y 0.04691; 0.9537 a
−0.5335; TRM 338 834, 14 800, 26 813 y 75 469; 0.9637 a −0.6023); `ndiffs`/`nsdiffs` sobre lx (1, 1), d1 (0, 1) y
∇∇₁₂ (0, 0). Sobre d1: KPSS p > 0.10 y r₁₂ = 0.8414. Sobre d12: `kpss.test` 0.3682 (p 0.0909, 4 rezagos),
`ur.kpss` con 2 rezagos 0.5367 > 0.463, y `ndiffs` llama a `ur.kpss` con `trunc(3*sqrt(n)/13)`, como dice el
recuadro. `diff(x, differences = 0)` da error. El bucle de Python da las mismas cifras.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 3398–3399; 3455; quiz 5975 | error | «Cada diferencia útil la reduce; **la primera diferencia de más la aumenta. El mínimo señala el $d$ correcto.**»; «Diferenciar de más… infla la varianza»; quiz P4: las tres señales «van juntas y son la misma cosa vista de tres formas» | Es falso en general. Para una serie estacionaria, Var(∇y)/Var(y) = 2(1 − ρ₁), que es menor que 1 si ρ₁ > 0.5: diferenciar **de más** una serie estacionaria persistente **reduce** la varianza. El mínimo de varianza es una heurística útil, no un criterio. Lo fiable es el sentido inverso: si la varianza sube, te pasaste (el M9, l. 3819, lo dice así y está bien). | R (`v1`): AR(1) φ = 0.8, n = 2000, `ndiffs` = 0 → var 2.955 → **1.204** → 2.687 (mínimo en d = 1, que sobra). JS (`v4`): en el simulador del M5, con su φ inicial de 0.7, var(∇y)/var(y) = **0.72** |
| 3478–3490 | error | Recuadro: «Sobre **esa misma serie** $\nabla_{12}\log y_t$ … `kpss.test()` … no rechaza … o sea $d = 0$ … `ndiffs()` devuelve 1». Moraleja: «Aquí las tres apuntan a lo mismo: el pico de $r_{12} = 0.841$ pide la diferencia estacional, y tras aplicarla la serie ya está lista.» | (i) La serie no tiene antecedente: el párrafo anterior trata de ∇ log y y de ∇₁₂∇ log y, no de ∇₁₂ log y. (ii) La moraleja resuelve el conflicto con una señal de **otra** serie: el r₁₂ = 0.841 es de ∇ log y. (iii) Sobre ∇₁₂ log y, que es la serie en disputa, las tres señales apuntan a **d = 1**, no a d = 0: la ACF decae despacio desde 0.714, la varianza baja de 0.0038 a 0.0021 al diferenciar y `ndiffs` = 1. «Tras aplicarla la serie ya está lista» contradice el pipeline del M9 (d = 1, D = 1) y el modelo *airline*. | R (`v3`): ACF de d12 → 0.714 0.623 0.48 0.441 0.387 0.319; `var(d12)` 0.0038, `var(diff(d12))` 0.0021; `ndiffs(d12)` 1; `acf(d1)` r₁₂ = 0.8414 |
| 3467–3473 | imprecisión (menor) | «Diferenciación estacional en la práctica»: primero una diferencia **regular**, luego `nsdiffs()` y luego la estacional | Es el orden contrario al que el capítulo recomienda tres veces: l. 3273–3276, la «Regla de trabajo» de 3135–3138 y el paso 3 del M9. Puede servir para enseñar justo eso, que tras ∇ sigue la estacionalidad, que es lo que dice FPP3, pero el texto no lo presenta como contraejemplo, sino como el camino al modelo *airline*. | fuente: FPP3 §9.1 (`arima.txt:119`): «If first differencing is done first, there will still be seasonality present.» |
| 3459–3460; quiz 5972 | imprecisión (menor) | «$\nabla y_t = \varepsilon_t - \varepsilon_{t-1}$, que es un MA(1) con $\theta = -1$» | El signo de θ depende de la convención del MA, que el capítulo no declara: con $y_t = \varepsilon_t + \theta\varepsilon_{t-1}$, θ = −1; con la de Cryer y Chan, $e_t - \theta e_{t-1}$, θ = 1. Un estudiante que lea a Cryer verá el signo contrario. | fuente: Cryer y Chan, p. 126 (`cryer2008time/p0137.txt:42`): «which is an MA(1) model but with θ = 1» |
| 3531; 3678 | laguna (menor) | Los bloques de Python del M7 y del M8 usan `pasajeros` | No se define en esos bloques, sino en los del M3 y el M4. Copiado solo, el bloque falla con `NameError`. | lectura de los bloques |
| 3537–3540 | sin comprobar | `pmdarima`: `ndiffs(lap, test="kpss") -> 1`, `nsdiffs(lap, m=12, test="ocsb") -> 1` | `pmdarima` no está instalado en el entorno y no se ha instalado nada. No afirmo que esté mal. | — |

---

## M8 · Logaritmo y Box–Cox (3557–3688)

Reproducido: λ = −0.2947 en AP y 0.1288 en la TRM. El criterio vale 0.53032 sin transformar, 0.15308 con el
logaritmo y 0.08149 en el óptimo. El exceso es del 87.9 %, que redondea a 88. La mejora captada es del 84 %. La
zona dentro del 20 % va de −0.41 a −0.175. La definición del criterio (l. 3612–3617) y el JS `cvGuerrero` (l. 5005),
que descarta las observaciones iniciales, son exactamente `forecast:::guer.cv`. `InvBoxCox` es exacta (1.8e-12).
scipy da λ = 0.148.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 3674–3677 | error | «el equivalente a BoxCox.lambda(method="guerrero") es: `from pmdarima.preprocessing import BoxCoxEndogTransformer`» | `BoxCoxEndogTransformer` estima λ con `scipy.stats.boxcox`, es decir, por máxima verosimilitud, que es justo lo que el comentario acaba de descartar. No es el criterio de Guerrero. | fuente: código de pmdarima (rama `master`, `pmdarima/preprocessing/endog/boxcox.py`, l. 76): `_, lam1 = stats.boxcox(y + lam2, lmbda=None, alpha=None)`. Leído, no ejecutado. |
| 3633; quiz 6050 | divergencia | «**FPP3 hace la misma recomendación**» (usar log aunque el óptimo sea λ = −0.295); quiz P8: «FPP3 y este capítulo recomiendan usar el logaritmo» | FPP3 dice que el log es útil por interpretable y que las otras potencias lo son menos. Pero también que un buen λ es el que iguala la variación estacional, y en su ejemplo toma λ = 0.10, junto al de Guerrero (0.11). No recomienda el log cuando el óptimo está lejos de 0. Respalda la razón (1), no la recomendación entera. | fuente: FPP3 §3.1 (`decomposition.txt:66, 78, 80`): «Logarithms are useful because they are interpretable»; «A good value of λ is one which makes the size of the seasonal variation about the same across the whole series… λ = 0.10 works quite well» |
| 3588 | divergencia (menor) | Box–Cox «Exige $y_t > 0$» | Es la definición clásica. FPP3 y `forecast::BoxCox` usan la versión modificada con `sign(y)`, que admite negativos cuando λ > 0. Conviene decirlo, porque el estudiante usará esas funciones. | fuente: FPP3 §3.1 (`decomposition.txt:70`): «which allows for negative values of y_t provided λ > 0»; R (`v3`): `BoxCox(c(-2,4), 0.5)` → −4.83, 2.00 |
| 3632; quiz 6069 | imprecisión (menor) | Razón (3) para preferir el log: «deshacer la transformación es trivial» | Deshacer Box–Cox con cualquier λ es igual de trivial (`InvBoxCox`, exacta), así que no distingue el log del óptimo. Además choca con el aviso siguiente (3637–3640): la vuelta de un pronóstico no es trivial. | R (`v1`): `max(abs(InvBoxCox(BoxCox(AP, lam), lam) - AP))` = 1.8e-12 |
| 3683; 3637–3638 | imprecisión (menor) | `y2 = np.exp(w)  # ...y la vuelta da la MEDIANA, no la media`, con `w = np.log(pasajeros)`; «lo que obtenemos es la mediana del pronóstico» | Sobre los datos, exp(log y) devuelve y exactamente. Lo de la mediana se aplica a un **pronóstico** y, según FPP3, si la distribución en la escala transformada es simétrica. El comentario lo pone en el sitio equivocado y la prosa omite la condición. | Py (`v2`): máx\|exp(log y) − y\| = 2.3e-13; FPP3 §5.6 (`toolbox.txt:609`): «it will usually be the median … (assuming that the distribution on the transformed space is symmetric)» |

---

## M9 · Pipeline, resumen, quiz, ejercicios y lecturas (3693–4287; quiz 5893–6075)

Reproducido: pipeline R d = 1, D = 1, λ −0.2947, var 9.17e-05, p del KPSS 0.1 y n = 131; pipeline Python 1 1
0.0021 0.1, con KPSS tras ∇₁₂ de 0.5367 (p 0.033). Ejercicio 1: 0.159, λ −0.0343, `nsdiffs` 1 y `ndiffs` 1; r₁
0.9909 y r₁₂ 0.9284 con banda 0.0906; varianzas 0.3882, 0.1543, 0.4023 y 1.3123; n 455, var 0.154, r₁ −0.302 y
5 de 24 fuera. Ejercicio 2: 4.6 %, 9.2 % y 93.8 %. Ejercicio 3: la tabla entera (917 290 … 154 530; r₁ y r₁₂;
14, 6, 6 y 2 de 24; Ljung–Box). Ejercicio 4: TRM, `ndiffs` 1. Hoy, con 142 meses, el veredicto se mantiene:
ADF p 0.845 y KPSS p < 0.01; en la diferencia, 0.0166 y > 0.10 (v5). Quiz: 1.96/12 = 0.1633; 0.0136 (12 veces);
banda 0.164 con n = 143; 0.5¹² = 0.0002; 131; la caminata toma valores negativos (mínimo −14.84). Las claves
de P1 a P8 son correctas. Las referencias de KPSS (J. Econometrics 54(1–3), 159–178) y Guerrero (J. Forecasting 12,
37–48) coinciden con la ayuda de `kpss.test` y `BoxCox.lambda` y con `obras.tsv`.

| línea | severidad | qué dice el capítulo | qué es lo correcto o lo que falta | evidencia |
|---|---|---|---|---|
| 4002–4003 | error (impacto bajo) | «**Seis** preguntas … **Cada opción tiene su explicación**» | El quiz tiene **ocho** preguntas. P2 y P7, que son numéricas, y P4, que es de respuesta múltiple, no tienen explicación por opción. Es el mismo defecto que en el capítulo 1. | lectura de `AUTOEVALUACIONES['cap2']`, l. 5893–6075 (8 objetos) |
| 3859; 3876–3878 | imprecisión | Pipeline R: `w <- if (abs(lambda) < 0.25) log(y) else BoxCox(y, lambda)` | Con AP, como \|λ\| = 0.2947 ≥ 0.25, el pipeline usa Box–Cox con λ = −0.2947, justo lo que el M8 y el quiz P8 desaconsejan en favor del log. El umbral de 0.25 no se justifica. El bloque de Python reconoce la diferencia de escala (3923–3926), pero no la contradicción con el M8. | R (`v3`): `abs(lambda) < 0.25` → FALSE; var_final 9.17e-05 en escala Box–Cox |
| 3787 | imprecisión | Paso 2, «Con qué»: «en Python, `scipy.stats.boxcox`» | Ese λ se estima por máxima verosimilitud (lo advierte el M8, 3674–3675) y en AP da 0.148, al **otro lado** del log respecto al −0.295 de Guerrero. Recomendarlo sin aviso en el resumen operativo del capítulo lleva a otra transformación. | Py (`v2`): `boxcox(pasajeros.values)` → λ = 0.148 |
| 3905; 3921 | imprecisión | Pipeline Python: `D = 1 if m > 1 else 0`; «→ las mismas d y D que la version en R» | D no se decide, se impone: cualquier serie mensual, estacional o no, recibe ∇₁₂, y tampoco se elige λ. Que coincidan con R en AP es un resultado puesto a mano, no una comprobación. | lectura del bloque; `v2.py` |
| 3944–3946 | sin comprobar | «las redes recurrentes y los modelos basados en árboles también funcionan **mucho mejor** sobre series diferenciadas» | Es una afirmación empírica general sin fuente ni prueba en el capítulo. Para los árboles hay un argumento (no extrapolan una tendencia), pero «mucho mejor» para las RNN no está respaldado. Habría que declararla `propia` o darle una fuente. | — |
| 4043–4044 (ej. 1) | imprecisión (menor) | «El nivel del CO2 solo varia un 15.9%»: `(max(co2) - min(co2)) / mean(co2)` | (máx − mín)/media mezcla la subida del nivel con el vaivén estacional. Por medias anuales, el nivel sube un 15.2 %. La cifra es parecida, pero mide otra cosa. Es la misma raíz que en el ejercicio 1 del capítulo 1. | R (`v3`): medias anuales 315.83 → 363.82 (+15.2 %); (máx − mín)/media = 0.1592 |
| 4116–4119 (ej. 2) | imprecisión (menor) | «**La única diferencia** entre los dos experimentos es que a aquellas caminatas se les sumó un componente estacional» | También cambian T (100 frente a 144) y la semilla. La comparación limpia es con la amplitud 0 del propio Monte Carlo del M6 (3.2 %). La conclusión de fondo sí se sostiene: con k = 12 el falso rechazo a amplitud 4 baja al 2.8 %. | R (`v1`): Monte Carlo con amplitud 0 → 3.2 %; con `k = 12`, amplitudes 0 y 4 → 3.0 % y 2.8 % |
| 4139–4140 (ej. 3, pista) | imprecisión (menor) | «si consultas `ndiffs(USAccDeaths)` … relee la caja de advertencia del **Módulo 7**» | El recuadro del M7 trata del truncamiento de rezagos del KPSS. El motivo por el que `ndiffs` falla sobre la serie cruda es la estacionalidad, y eso está en la «Regla de trabajo» del M6 (3134–3139). | lectura; R (`v3`): `ndiffs(y)` 0, `nsdiffs(y)` 1, `ndiffs(diff(y,12))` 1 |
| 4221–4223 (ej. 4) | imprecisión (menor) | «la conclusión sobre una raíz unitaria es una **propiedad estructural de la serie, no un accidente de la ventana de datos**» | El resultado de la prueba sí depende de la ventana, y el propio M5 (2833–2834) dice que con muestras cortas φ = 0.95 y φ = 1 son casi indistinguibles. Hoy el veredicto se mantiene, pero con la ventana desde 2022 el ADF da p = 0.071. | R (`v5`): ADF por ventana: desde 2015 p 0.585; desde 2018 0.912; desde 2020 0.843; desde 2022 **0.071** |
| 5949 (quiz P3) | imprecisión (menor) | Retro de «Ya es ruido blanco»: «la banda dejaría fuera … una o dos de 24 —, **no ninguna**. Lo que delata a esta no es que se salga, sino cuánto y dónde» | La serie tiene **10** de 24 rezagos fuera, así que «no ninguna» no tiene sentido aquí, y el número de barras fuera sí es en sí una señal. | R (`v3`): ∇ log AP fuera de banda en k = 1 4 8 11 12 13 16 20 23 24 |
| 6066 (quiz P8) | imprecisión | Retro: «Con series anuales sin ciclo **habría que fijar el tamaño de bloque a mano**» | `BoxCox.lambda(method = "guerrero")` usa por defecto bloques de 2 cuando la frecuencia es 1 (`nonseasonal.length = 2`). No hay que fijar nada. | R (`v1`): `body(forecast:::guer.cv)` → `period <- round(max(nonseasonal.length, frequency(x)))`; `BoxCox.lambda(Nile, method="guerrero")` → 0.9989 sin más argumentos |
| 4274–4275 | imprecisión | Lecturas: FPP3 «secc. 3.1–3.2 (transformaciones y Box–Cox)» | La §3.2 de FPP3 es «Time series components». Las transformaciones y Box–Cox están solo en la §3.1. | fuente: `decomposition.txt:11` «3.1 Transformations and adjustments», `:97` «3.2 Time series components» |
| 4272–4283 | laguna | Las lecturas cubren estacionariedad, diferenciación y Box–Cox | Faltan la ACF y el ruido blanco (FPP3 §2.8–2.9) y la PACF (§9.5), que son los módulos 2 a 4 y entran en el quiz. | fuente: `graphics.txt:575` «2.8 Autocorrelation», `:630` «2.9 White noise»; `arima.txt:330–338` (PACF en §9.5) |
| 4277–4278 | sin comprobar | Shumway y Stoffer «(4.ª ed.), secc. 1.4–1.6 … y **2.1 (diferenciación)**» | En `_local` solo está la 3.ª ed. Allí las §1.4–1.6 sí son dependencia, estacionariedad y estimación de la correlación, pero la §2.1 es «Introduction» y la diferenciación está en la §2.3. No puedo confirmar la numeración de la 4.ª. | fuente: Shumway y Stoffer 3.ª ed., índice (`shumway2011time/p0010.txt`) |

---

## Recuento

| módulo | error | imprecisión | laguna | divergencia | sin comprobar | total |
|---|---|---|---|---|---|---|
| M1 | 0 | 0 | 0 | 0 | 0 | 0 |
| M2 | 0 | 1 | 0 | 1 | 0 | 2 |
| M3 | 1 | 0 | 0 | 0 | 0 | 1 |
| M4 | 0 | 1 | 0 | 1 | 0 | 2 |
| M5 | 1 | 2 | 0 | 0 | 0 | 3 |
| M6 | 1 | 2 | 1 | 0 | 0 | 4 |
| M7 | 2 | 2 | 1 | 0 | 1 | 6 |
| M8 | 1 | 2 | 0 | 2 | 0 | 5 |
| M9 (pipeline, quiz, ejercicios, lecturas) | 1 | 10 | 1 | 0 | 2 | 14 |
| **total** | **7** | **20** | **3** | **4** | **3** | **37** |

Lo que da peso al diagnóstico: **ninguna cifra publicada está mal calculada**. Todas las que presentan la prosa,
las tablas, los comentarios `#` de los bloques, los ejercicios y el quiz salen idénticas en R 4.6.0 y en
statsmodels 0.14.6. Los errores están en enunciados generales (M5, M7), en lo que se afirma a partir de una
cifra correcta (M3, M6, M7) y en una afirmación sobre una herramienta (`BoxCoxEndogTransformer`).
