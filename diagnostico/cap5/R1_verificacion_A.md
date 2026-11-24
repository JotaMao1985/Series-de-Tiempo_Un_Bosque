# Capítulo 5 · R1 (errores) · verificación independiente A (contenido)

2026-11-23/24. Verificador de contexto limpio, sin el registro del redactor (`R1_cambios.md`) ni sus salidas `r1_*`
hasta terminar la comprobación propia; después se cotejaron. Objeto: el diff sin commit contra `7686d33` en
`ensamblado/cap5/`, `ensamblado/ensambla_cap5.py` y `precalculo/genera_cap5.R` con sus salidas, leído en el HTML
reensamblado. Las diapositivas, el generador como programa y la reproducibilidad byte a byte son del verificador B.

**Entorno:** R 4.6.0 · forecast 9.0.2 · tseries 0.10.62 | Python 3.10 (mambaforge) · statsmodels 0.14.6 · numpy 2.2.6 ·
pandas 2.3.3 · scipy 1.15.3 (`MPLBACKEND=Agg`). Servidor propio en 8766, cerrado al acabar.

**Guiones y salidas** (`diagnostico/cap5/comprobaciones/`):

| guion | salida | qué comprueba |
|---|---|---|
| `v1a_comprobaciones.R` | `v1a_comprobaciones.out` | cada cifra nueva o cambiada en R: barras fuera de banda del M1; TRM desde la copia (r₁₂, t, AICc, `nsdiffs`); 1.5217, 2.300/1.700 y la tabla φ del M2; la condición 2q < m con un MA(7)×SMA(1) y un MA(5)×SMA(1); ρ̂₁₂ = 0.8414, Θ̂, e.e., distancia a −1 y \|raíz\|⁻¹ = \|Θ̂\|^(1/12) del M3; cocientes de varianza frente a 2(1 − r); el criterio del e.e. sobre el Nilo y log(lynx) del cap. 4 y en 200 caminatas con D sobrante; ρ₁₁, ρ₁₃ y producto del M4; ψ, salto 1 + Θ, subida anual, σ_h/σ frente a √h, primer cruce y permanencia, cociente σ²_h/h³ del M5; Ljung–Box sin arranque, residuales de arranque y el modelo sin ARMA del M6; salida de R del M7; Semana Santa sola con `timeDate::Easter` (independiente del algoritmo del generador) y t de β = 1 del M9; tope ⌊n/(3m)⌋ en el código de `auto.arima` y `stlm` del M10; parámetros de la armónica K = 5 (quiz 6); E1 y E3(b) |
| `v1a_criterio_ee.R` | `v1a_criterio_ee.out` | falsas alarmas del criterio «−1 dentro de Θ̂ ± 1.96 e.e.» cuando no sobra nada (Θ = −0.6, −0.85, −0.95; n = 144; 300 réplicas) |
| `v1a_python_cifras.py` | `v1a_python_cifras.out` | statsmodels: optimizador por defecto frente a BFGS (avisos y `converged`), Ljung–Box 0.2261/0.3675, pronóstico y anchura del M7, ψ y σ_h del M5, OPG frente a hessiana (`approx`, `oim`, `robust`) del M9, Fourier con 50 y 2000 iteraciones del M10 |
| `v1a_m8_python.py` | `v1a_m8_python.out` | los dos ajustes del bloque de Python del M8, sin silenciar avisos |
| `v1a_bloques.py` | `v1a_bloques.out` | cada bloque de Python del capítulo y los de R que leen la TRM, extraídos del HTML y ejecutados solos en una carpeta vacía (y, los de la TRM, también con el CSV), con `-W default`; compara sus `#>` y busca `ConvergenceWarning` |
| `v1a_literales.py` | `v1a_literales.out` | 7-gramas de las 509 líneas añadidas en `bibliografia/_local/texto` y `web` |
| — | `v1a_verifica_todo.out` | `verifica_todo.py` |

## Resumen

**Los errores y las imprecisiones de la especificación quedaron corregidos, y lo que se escribió en su lugar es
cierto en casi todo.** Las cifras nuevas se reproducen todas, en R y en Python: el *airline* del M5 (ψ₁₂ − ψ₁₁ = 1 + Θ
exacto; subida anual (1 + θ)(1 + Θ) = 0.265 **exacta** desde j = 13, no aproximada; ψ₂₄₀ = 6.08; σ₂₄₀/σ = 53.98 frente a
15.49; cruce en h = 42 y el *airline* queda por encima de la caminata en todos los h de 42 a 601); el salto del
simulador `airline-pesos` (0.4400, 1.0000 con Θ = 0, 0.0500 con Θ = −0.95, leído por HTTP); la condición 2q < m del M2
(con q = 7, ρ₅ exacto 0.3757 frente a 0.2945 del producto; con q = 5 coinciden); ρ₁₁, ρ₁₃ y el producto del M4; el
Ljung–Box de R sin los 13 de arranque (0.3515); el AICc −434.8 y p = 2.31·10⁻⁸ del modelo sin ARMA; la salida real del
M7; OPG frente a hessiana del M9 (`cov_type="approx"` da 0.4462 y 0.0111, los de R); la Semana Santa sola (AICc
−487.2305, β̂ = 0.0298, t = 2.56, idéntico al calcularla con `timeDate::Easter` y a lo que muestra el simulador); el tope
`max.P <- min(max.P, floor(serieslength/3/m))` del código de `auto.arima`; AIC −543.24 / AICc −542.95 de `stlm`; K = 5
con solo el entrenamiento y RMSE 19.58, sin cambiar el orden; los 15 coeficientes de la armónica K = 5 (10 armónicos,
4 MA y la deriva, sin σ²: la misma cuenta que los 2 del *airline*; el 16 de antes contaba σ²). La regla de la varianza
ya no decide en ningún sitio del capítulo (M3, ciclo, M7, resumen, E1, lecturas); queda solo en el simulacro, que no
se toca. El M12 está en pasado y es coherente con el del cap. 4 (el 11 de noviembre de 2026 fue miércoles).

**Lo que no está bien es el criterio nuevo de sobrediferenciar cuando se usa al revés.** «Si sobra una diferencia,
Θ̂ queda pegado a −1» es cierto (en 200 caminatas con D sobrante, Θ̂ mediano −0.9999 y aviso en 184). Pero el simulador
del M3 afirma lo recíproco —«−1 dentro de Θ̂ ± 1.96 e.e.: sobra una diferencia estacional»— y eso es falso a menudo:
con Θ verdadero −0.85 y n = 144, **donde no sobra nada**, el criterio avisa en 211 de 300 réplicas (con −0.95, en 264).
Cerca de −1 el intervalo de Wald con el e.e. de la hessiana no es fiable y no separa −0.85 de −1 con 130 datos
(hallazgo 1). La otra imprecisión es la nueva solución del E3(b), que decide entre familias con un Ljung–Box al filo del
5 % y ordena modelos por su p-valor (hallazgo 2). El resto son menores.

**Reproducibilidad del contenido:** los 13 bloques de Python, solos y en carpeta vacía, dan sus `#>` y **ningún
`ConvergenceWarning`**; los tres bloques de R con la TRM dan la misma salida sin el CSV (leen de la página del curso) y
con él. Es cierto que el optimizador por defecto no converge en el *airline* (`ConvergenceWarning`, `converged=False`
con y sin `simple_differencing`) y que, en Fourier, K = 3, 4 y 6 no convergen con 50 iteraciones y sí con 2000.
`verifica_todo.py`: 11 en verde. `simulacro.js` sin cambios frente a `7686d33`. Ningún `<cite>` ni `data-afirma` nuevo;
las únicas coincidencias de 7-gramas con `_local/` son la sintaxis de `Arima(…, order = c(0, 1, 1), seasonal = list(…))`
(código, no prosa); `sin_literales_diagnostico.py`: 0. Por HTTP, módulos 3, 5 y 9 sin `.katex-error` ni errores de
consola.

## Hallazgos

Gravedad: **error** (enseña o afirma algo falso), **imprecisión** (cierto a medias o contradice otra parte), **menor**.
Líneas: las de la fuente en `ensamblado/cap5/` (o el archivo que se nombra).

| # | Gravedad | Dónde | Qué está mal | Evidencia | Corrección propuesta | Lo que hizo la sesión maestra |
|---|---|---|---|---|---|---|
| 1 | imprecisión | `chapter.js` l. 555–561 (lectura del simulador `sobrediferenciacion-estacional`); `templates_1_3.html` l. 1036–1040 (intro) y l. 1060–1067 (lectura de la tabla); `ensambla_cap5.py` l. 312–313 (ciclo, etapa 2); `templates_10_11.html` l. 418 (resumen) | El criterio se enuncia en el sentido correcto («cuando sobra una diferencia, Θ̂ se pega a −1»), pero el simulador lo aplica al revés y en tono de veredicto: «−1 dentro de Θ̂ ± 1.96 e.e.: **sobra** una diferencia estacional». Con n ≈ 130 el intervalo de Wald no separa un Θ de −0.85 de −1, y en la frontera de invertibilidad el e.e. de la hessiana no tiene la distribución que justifica el 1.96. Ni la prosa ni la lectura lo advierten. Además, con D = 0 la lectura dice «Θ̂ lejos de −1: no sobra ninguna diferencia», que es cierto pero calla que ahí **falta** la estacional (Θ̂ = +0.74) | `v1a_criterio_ee.out`: sin diferencia sobrante, alarma en 5/300 con Θ = −0.6, **211/300 con Θ = −0.85** y 264/300 con Θ = −0.95. `v1a_comprobaciones.out` § cap. 4: con D sobrante, aviso en 184/200 y 16 sin aviso (distancia hasta 4.31 e.e.); Nilo d = 2, θ̂ = −0.99999 a 0.0005 e.e. El co2 del E1 (Θ̂ = −0.8506, n = 455) queda a 5.82 e.e. solo porque n es grande. Lectura por HTTP: D = 0 «no sobra ninguna diferencia» | Lectura: «⚠ Θ̂ compatible con −1: posible diferencia de más; contrástalo con `nsdiffs()` y la ACF (etapa 2)» y, para D = 0, «Θ̂ lejos de −1; aquí lo que falta es ∇₁₂ (ACF en 12, 24, 36)». En la prosa del M3, una frase: es una señal para volver a la etapa 2, no una prueba; cerca de −1 el error estándar no es fiable y, con unos 130 datos, un Θ de −0.85 tampoco se distingue de −1. El resumen y el ciclo pueden quedarse con «pegado a −1» y quitar «indistinguible con su error estándar» como definición |  Corregido (`r1_ediciones_maestra.py`, A1). Re-medido en `r1_maestra.R`: con Θ = −0.85 y sin diferencia de más, alarma en 137 de 200. La lectura dice ahora «señal de que puede sobrar…; vuelve a mirar D», y con D = 0 «no sobra nada, pero falta ∇₁₂». La intro, el párrafo de la tabla, el ciclo (etapas 2 y 3), el resumen y el deck (diapositiva 29 y cierre de la clase 1) la llaman señal, no veredicto, sin cifras nuevas |
| 2 | imprecisión | `templates_10_11.html` l. 626–628 (respuesta del E3) y l. 690–699 (lo que hay que entender) | La respuesta decide la parte (b) por el diagnóstico: «el mejor armónico por AICc no pasa Ljung–Box y el *airline* sí. Por eso se elige el *airline*». Pero el «no pasa» es p = 0.0439, y los armónicos K = 5 y K = 6 (AICc a 1.3 y 3.4 puntos del K = 4) lo pasan con 0.0516 y 0.0515: la familia no queda descartada por el diagnóstico, solo su ganador por AICc, y por cinco milésimas. «Ninguno de los seis llega al p = 0.4081 del *airline*» enseña a ordenar modelos por el p-valor de Ljung–Box, que no mide cuál es mejor. (El 0.4081 incluye los 13 residuales de arranque; sin ellos, 0.4993; no cambia nada.) Sí es cierto que los dos AICc no son comparables: diferencian distinto (d = 1 frente a d = D = 1) y la verosimilitud se evalúa sobre 467 y 455 datos distintos | `v1a_comprobaciones.out` § E3(b): K = 4 LB 0.0439, K = 5 0.0516, K = 6 0.0515; *airline* 0.4081 (sin arranque 0.4993) | Respuesta: «(b) No por el AICc, que no es comparable. El diagnóstico inclina hacia el *airline*: sus residuales pasan con holgura y los armónicos quedan en el borde del 5 % (0.044 a 0.052). Decidir de verdad entre familias pide comparar fuera de muestra (Capítulo 6)». Quitar «ninguno llega al p = 0.4081» o decirlo sin hacer del p-valor una escala |  Corregido (A2): respuesta y «Lo que hay que entender» dicen que el diagnóstico inclina sin cerrar; los armónicos quedan en el borde (0.0439, 0.0516, 0.0515, del bloque); el p-valor no ordena modelos; la decisión firme es fuera de muestra (Capítulo 6). Comentario del bloque, igual |
| 3 | menor | `templates_4_6.html` l. 298 (M5) | «La varianza del error crece entonces como $h^3$» es el orden asintótico; a veinte años todavía no: σ²₂₄₀/σ²₁₂₀ = 6.31 (h³ daría 8) y σ²_h/h³ sigue bajando en h = 600 hacia su límite | `v1a_comprobaciones.out` § M5: cocientes 4.0·10⁻⁴, 2.7·10⁻⁴, 2.1·10⁻⁴, 1.8·10⁻⁴ en h = 60, 120, 240, 600; límite 1.6·10⁻⁴ | «crece, a la larga, como $h^3$» |  Corregido: «crece, a la larga, como h³» (capítulo y notas del deck) |
| 4 | menor | `templates_4_6.html` l. 295–296 (M5) | «$(1-B^{12})$ ya contiene a $(1-B)$ (Módulo 3)»: el M3 dice que $1 - B^{12}$ tiene doce raíces distintas sobre el círculo, no que una sea $B = 1$; la remisión no da lo que se le atribuye | `templates_1_3.html` (definición de la diferencia estacional, HTML l. 3793–3797) | «$(1-B^{12}) = (1-B)(1+B+\dots+B^{11})$» aquí mismo, o añadir en el M3 «una de ellas, $B = 1$» |  Corregido: la factorización se escribe en el M5; sin remisión al M3. Notas del deck, igual |
| 5 | menor | `templates_4_6.html` l. 502 y l. 556 (M6, comentarios de R y de Python) | «Los d + D·m = 13 primeros residuales de R son de arranque, casi nulos» / «R deja 13 residuales casi nulos»: los 12 primeros están por debajo de 0.003 en valor absoluto, pero el 13.º vale −0.0168, casi media σ̂ (0.037) | `v1a_comprobaciones.out` § M6 (residuales 1–14) | «son de arranque (los doce primeros, casi nulos)» |  Corregido en los dos comentarios: «de arranque (los doce primeros, casi nulos)» |
| 6 | menor | `templates_1_3.html` l. 1007 (M3, tabla de las cuatro combinaciones) | La tabla sigue marcando en negrita la varianza mínima (0.002102), que es la señal visual de la regla que la prosa de debajo retira | lectura de la fuente | Quitar la negrita de la varianza (la del 0.8414 de ρ̂₁₂, que es lo que el texto comenta, se queda) |  Corregido: sin negrita en la varianza |
| 7 | menor | `templates_1_3.html` l. 1013–1016 (M3) | «el cociente se acerca a $2(1-\hat\rho_1)$ —y el de $\nabla_{12}$ a $2(1-\hat\rho_{12})$—» se dice «en una serie estacionaria», pero va pegado a una tabla cuya serie no lo es, y en ella no se cumple: 0.0583 frente a 0.0926 y 0.0195 frente a 0.4761. Quien lo compruebe con la tabla de arriba creerá que la cuenta está mal | `v1a_comprobaciones.out` § M3 | Añadir «(con esta serie, que no es estacionaria, la cuenta no cuadra; el argumento es que la varianza no aporta una evidencia aparte de la ACF)», o remitir solo al cap. 2 sin la fórmula del rezago 12 |  Corregido: sin la fórmula del rezago 12 y con «la cuenta es para series estacionarias, y por eso no cuadra con las filas de esta tabla» |
| 8 | menor | `templates_1_3.html` l. 1115 (M3, comentario de R) | «\|raiz MA\|⁻¹ = \|Theta\|^(1/12): cerca de 1 en las tres filas, no separa nada». En esta tabla sí separa con el umbral de antes (0.9998 frente a 0.9752 y 0.9524); el problema es que comprime la escala (Θ = −0.9 ya da 0.991), que es lo que dice bien la prosa | `v1a_comprobaciones.out` § M3 | «comprime la escala: con Θ = −0.9 ya vale 0.991» |  Corregido: «comprime la escala hacia 1 y separa mal; Theta no» |
| 9 | menor | `templates_7_9.html` l. 677–678 (M9, Python) | «Con el optimizador por defecto se detiene antes del máximo». Cierto (log L 250.6002 frente a 250.6004, β̂ 1.0764 frente a 1.0844), pero ese ajuste declara `converged=True` y no avisa; el M6 acaba de recomendar mirar `mle_retvals`, y aquí no lo detecta | `v1a_python_cifras.out` § M9 (`defecto: conv True avisos []`) | Añadir «y aun así `mle_retvals` dice que convergió: el aviso no basta, conviene repetir con otro optimizador y comparar la verosimilitud» |  Corregido: el comentario dice que `mle_retvals` declaró convergencia y que el aviso no basta |
| 10 | menor | `templates_7_9.html` l. 455 (M8, Python) | El bloque conserva `warnings.filterwarnings("ignore")`, que silencia también `ConvergenceWarning`, contra D11. Sus dos ajustes convergen; lo que silencia son `RuntimeWarning` de numpy | `v1a_m8_python.out` (los tres ajustes, `converged=True`, sin aviso de convergencia) | Igualarlo a los demás: `warnings.simplefilter("ignore", RuntimeWarning)` y un `print(f.mle_retvals["converged"])` |  Corregido: `simplefilter("ignore", RuntimeWarning)` y `print` de la convergencia de los dos ajustes (`#> True True`, comprobado en `r1_maestra_bloques_python.out`) |
| 11 | menor | `templates_1_3.html` l. 53–54 (M1, intro del simulador) | «unas pocas [barras] menores sin patrón, que el Módulo 7 discute»: hay cuatro fuera de banda además de 1 y 12 (3, 9, 23 y 32); el M7 discute las tres de los primeros 24 rezagos, y el simulador dibuja hasta 36 | `v1a_comprobaciones.out` § M1 (rezagos 1, 3, 9, 12, 23, 32, con las dos bandas) | «… que el Módulo 7 discute (la del 32 queda fuera de los 24 que mira Ljung–Box)», o dejarlo así |  Corregido: «el Módulo 7 discute las que caen dentro de los 24 rezagos que mira Ljung–Box» |
| 12 | menor | `templates_1_3.html` l. 605 (M2, comentario de R) | «# el caso de la fila en negrita»: en la tabla del M2 hay dos filas en negrita (φ = 0.9 y 0.95) | HTML l. 3605–3610 | «# el caso φ = 0.9 de la tabla» |  Corregido: «el caso phi = 0.9 de la tabla» |
| 13 | menor (para el banco) | `simulacro.js` l. 435–443 (pregunta de la tabla de diferencias) | Las retros siguen usando la varianza como evidencia, la de la correcta incluida: «con las dos, la varianza es la menor de la tabla … la huella de dos diferencias justas», y «una diferencia regular de más sube la varianza …: es sobrediferenciar». Es la regla que la R1 retira (D3), no un dato al lado de ρ̂₁ y ρ̂₁₂ | HTML l. 10179–10187 | No se toca (`simulacro.js` es instrumento aplicado); anotarlo para el banco junto a los otros tres hallazgos del simulacro |  No se toca `simulacro.js`. Anotado para el banco en `R1_cambios.md` (sección de la sesión maestra) |
| 14 | menor (para la R4) | `templates_7_9.html` l. 344–347 (M8) | La prosa nueva atribuye la serie a la Superintendencia Financiera y a datos.gov.co; antes solo estaba en comentarios de código. No es una cita bibliográfica, pero es una fuente de datos sin alta en la biblioteca (§2 del plan) | lectura del diff | Registrarla en la R4 con la alta de la TRM |  Anotado para la R4 (alta de la TRM como fuente de datos) |

## Comprobado y correcto (sin hallazgo)

- **(a) *Airline* frente a la caminata (M5).** σ₁₂/σ₁ = 2.2217 frente a √12; la derivación ya no generaliza («en el primer
  año», que es prudente: la ventaja dura hasta h = 41). Subida anual exacta desde j = 13 (mín. = máx. = 0.2650229 en
  j = 13…600); ψ₂₄, ψ₆₀, ψ₁₂₀, ψ₂₄₀ = 1.31, 2.10, 3.43, 6.08; tabla σ_h/σ idéntica a cuatro cifras; primer cruce h = 42 y
  ningún h posterior por debajo. El bloque de Python reproduce todo (21.482 y 53.981 frente a 21.481 y 53.980 de R, por
  coeficientes que difieren en la sexta cifra, como dice). La frase sobre la suma de ψ² del M2 es correcta.
- **(b) Salto ψ₁₂ − ψ₁₁ = 1 + Θ**, exacto (0.443055 = 0.443055); la intro nueva dice lo que dibuja el simulador (1.0000
  con Θ = 0, 0.0500 con Θ = −0.95). El eje de los ψ usa `suggestedMax`, así que con Θ = 0 las barras no se cortan.
- **(c) Regla de la varianza.** Retirada del M3, del ciclo (etapa «elegir d»), del M7 (fila «Señal de vuelta»,
  θ̂ e.e. 0.0896 correcto), del resumen y de la pista y la solución del E1 (ACF de ∇co2: 0.9219, 0.8902, 0.8686, banda
  0.0907; a −1: 13.09 y 5.82 e.e.). La razón que da el M3 coincide con `c2-m7-08` y con la nota del cap. 4. La lectura del
  simulador `cuatro-combinaciones` muestra la varianza sin interpretarla. El lynx del 58 % es el del cap. 4.
- **(e) E3(b), comparabilidad.** Los AICc 180.200 (n = 467) y 178.209 (n = 455) no son comparables; la frase nueva del E1
  («allí la comparación tampoco vale, aunque el menor señale el mismo modelo») es correcta.
- **(f) Manchas solares.** La frase nueva sobre el BIC es cierta y no remite a nada.
- **(g) M7.** La salida `-0.401828 -0.556945 0.001371 -483.210085` y las σ_h 0.037031, 0.082270, 0.139621 son las de R;
  `th` y `TH` se definen en el mismo bloque. Python con BFGS: 525.46, 400.59, 689.25; anchura un 0.87 % menor («casi un
  1 %»).
- **(h) M9 y M2.** OPG por defecto en statsmodels y hessiana en R: con `cov_type="approx"` salen 0.4462 y 0.0111 y t
  2.4301 y 2.6026; t de β = 1, 0.1892 (Python, β̂ = 1.0844) y 0.1882 (R). La factorización de la varianza con q < m y la
  de la ACF con 2q < m, y el ejemplo de q = 7, son correctos. «Los dos diferencian a la vez la serie y los regresores»
  vale para `Arima(xreg=)` y para `SARIMAX(exog=)`.
- **(i) Calendario.** La combinación «solo Semana Santa» lee `con_pascua`; sus cifras coinciden con un ajuste
  independiente (12 meses con Pascua; AICc −487.2305, BIC −476.0471; 0.0298, e.e. 0.0116, t 2.5621).
- **(j) Quiz.** Ítem 6: 15 coeficientes es la cuenta coherente con los 2 del *airline*. Ítem 8: la retro nueva remite al
  «sesgo medio» que el M11 sí calcula (39.45). Claves y posiciones de las correctas sin cambios en el diff; ítem 1 con
  −0.0025, coherente con la copia congelada.
- **M10.** ⌊800/1095⌋ = 0 y el código de `auto.arima` limita P y Q a ⌊n/(3m)⌋ (para m = 1 los pone a 0); K = m/2 deja
  m − 1 términos. Fourier en statsmodels: con 50 iteraciones no convergen K = 3, 4 y 6; con 2000, todos, y los AIC son los
  del bloque (−414.35, −470.59).
- **M11.** K = 5 con solo el entrenamiento (AICc −434.304 frente a −433.789 de K = 6), RMSE 19.58 frente a 19.505; ETS
  sobre el log sigue primero (19.429) y la armónica, segunda por RMSE y primera por MAE (14.708) y MAPE (3.146).
- **TRM congelada.** El CSV tiene 138 meses; r₁₂ = −0.002453 (de ahí −0.0025), t = 0.0146, AICc 1708.001 y 1705.941,
  `nsdiffs` 0 y 0; la URL de respaldo responde 200 y los caps. 2–4 leen el mismo archivo.
- **M12.** En pasado, con la fecha correcta, sin cambiar `simulacro.js`; coherente con el M12 del cap. 4.

## Cotejo con `R1_cambios.md` (después de la comprobación propia)

El redactor anota el bloque del M8 con `filterwarnings` (hallazgo 10) y el simulacro (hallazgo 13, aunque lo describe
como «la varianza junto con ρ̂₁ y ρ̂₁₂, no como regla»; la retro de la opción que sube la varianza sí la usa como regla).
No registra la tasa de falsas alarmas del criterio del e.e. (hallazgo 1) ni que K = 5 y K = 6 pasan Ljung–Box en el E3
(hallazgo 2). Sus cifras coinciden con las mías.

## No comprobado

- El render a 800 y 375 px y los demás simuladores (solo se leyeron por HTTP las lecturas del M3, el M5 y el M9).
- Las diapositivas, el generador como programa (guarda de tildes) y el reensamblado byte a byte de los caps. 5 y 6:
  verificador B.
- Que el quiz de Brightspace durara cincuenta minutos y tuviera tres versiones: no se encontró registro en el repo; el
  diff solo cambió el tiempo verbal.
