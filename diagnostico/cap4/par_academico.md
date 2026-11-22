# Capítulo 4 · revisión del par académico

- **Archivo:** `Htmls_Series/capitulo-4-modelos-arima.html` en el commit `71c42d8` (doce `<template id="module-N">`, l. 2749–5900; motor y simuladores l. 6240–8860; `AUTOEVALUACIONES['cap4']` l. 8887, `SIMULACROS['cap4-simulacro']` l. 9403). Las líneas citadas son de ese archivo; entre corchetes, la fuente editable en `ensamblado/cap4/` (`T13` = `templates_1_3.html`, `T46`, `T79`, `T10`, `JS` = `chapter.js`).
- **Lente:** corrección y rigor (definiciones, fórmulas, lógica del JS, código R y Python, cifras, claves de ejercicios, quiz y simulacro, interpretaciones). No se revisan estilo, fuentes ni diseño de gráficas.
- **Entorno:** R 4.6.0 · forecast 9.0.2 · tseries 0.10.62 · urca 1.3.4 | Python 3.10.14 · statsmodels 0.14.6 · numpy 2.2.6 · scipy 1.15.3 · pandas 2.3.3 · matplotlib 3.10.8 (`MPLBACKEND=Agg`) | node (solo para extraer el preparcial). Los dos bloques de la TRM se ejecutaron contra la API de datos.gov.co, que respondió con las 138 observaciones; los recálculos propios usan `Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv`.
- **Guiones** (en `diagnostico/cap4/diag/`):
  - `par_extrae_bloques.py` extrae los 23 bloques de código de los módulos (13 de R, 10 de Python) del HTML en `71c42d8` a `par_bloques/bNN_lLLLL.{R,py}`; cada uno se ejecutó tal cual y su salida está en `par_bloques/bNN_lLLLL.out`.
  - `par_compara_bloques.py` → `par_compara_bloques.out`: cruza cada cifra de los comentarios `#>` con la salida real.
  - `par_verifica.R` → `par_verifica.out`: M1 y M3 (raíces, pruebas, `ur.df`/`ur.pp`/`ur.kpss`, modelo de dos medias, Monte Carlo propio con semillas 2026 y 7).
  - `par_verifica_mc.R` → `par_verifica_mc.out`: réplica exacta (misma semilla y mismo orden de consumo) del Monte Carlo del escalón de `precalculo/genera_cap4.R`.
  - `par_verifica2.R` → `par_verifica2.out`: M4–M10, ejercicios, quiz y simulacro (rejilla de 27 modelos con raíces y Ljung–Box, traza exhaustiva, sobrediferenciación, escalón, fuera de muestra, `log(lynx)`, formas y pesos ψ, BJsales, TRM, AirPassengers).
  - `par_verifica3.R` → `par_verifica3.out`: el ARIMA(2,1,2) con `Arima()` (CSS-ML) frente a `arima()` (ML) en la TRM y el Nilo; efecto Working.
  - `par_verifica.py` → `par_verifica_py.out`: afirmaciones sobre statsmodels (rezagos de KPSS `auto`, primer residual, constante del ARIMA(1,0,1), origen de la diferencia de AICc, OPG frente a OIM, método por defecto de `pacf`).
  - `par_verifica_preparcial.R` → `par_verifica_preparcial.out` y `par_preparcial2_verificador.out` (salida de `precalculo/verifica_preparcial2.py`, solo lectura).
- **Convenio de signos:** el capítulo usa el de R en todas partes ($\theta(B)=1+\theta_1B+\cdots$), igual que el capítulo 3. Lo cumplen la prosa, las raíces ($1/0.8741 = 1.144$), la forma cerrada de $\psi_j$ (coincide con `ARMAtoMA` con error 5e−16, `par_verifica2.out` § M9), el JS (`|raíz MA| = 1/|θ|`), los `ArmaProcess`/`arma2ma` de Python (polinomios con el signo ya aplicado), el quiz, el simulacro (fila «(1 + 0.25B)(1 − B) yₜ = (1 − 0.96B) εₜ» declara el convenio) y el preparcial (ítem a#1, que traduce el de Box–Jenkins). No hay mezclas.

**Resultado global.** Los 23 bloques corren y reproducen sus cifras. Todas las cifras de la prosa recalculadas salen iguales, incluido el Monte Carlo del escalón, que se reproduce exactamente. No se encontró ninguna cifra incorrecta ni ningún error de fondo. Los hallazgos son explicaciones de discrepancias R/Python mal atribuidas, una inconsistencia entre el explorador del M6 y el M7 sobre el ARIMA(2,1,2), dos opciones del quiz con matices que contradicen el propio capítulo, una regla del M2 sin la salvedad que el M10 necesita, y detalles menores.

---

## Línea base del verificador (713 de 735)

`diagnostico/cap4/comprobaciones/linea_base_bloques.out` numera los bloques desde 0; aquí se dan con el nombre de `par_bloques/`. Ninguna de las 22 cifras «no halladas» es un error del capítulo:

| Bloque (verificador) | Cifras | Explicación | Evidencia |
|---|---|---|---|
| #0 · `b01_l2888.R` | `33` | Redondeo en prosa del `32.8` impreso («la multiplica por 33»). | `b01_l2888.out` |
| #1 · `b02_l2925.py` | `-0.8741` | Es el parámetro que se cita en el comentario, no una salida. Falso positivo. | `b02_l2925.py` |
| #2 · `b03_l3161.R`, #4 · `b05_l3417.R` | `0.05`, `0.01` | Umbrales («> 0.05», «p < 0.01»). Falsos positivos. | — |
| #3 · `b04_l3183.py`, #5 · `b06_l3460.py`, #7 · `b08_l3670.py`, #9 · `b10_l3856.py`, #15 · `b16_l4500.py` | 0.7997, 816.18…, 0.045, 1.000, −0.7329, 0.6737, −2.8827, 2.0167, −1.429, 28.15, −8.8 | Cifras **de R** citadas en comentarios de Python. Todas coinciden con la salida de su bloque R. El `-8.9` es $-247.78/27.77 = -8.92$. | `b03`, `b05`, `b07`, `b09`, `b15` `.out` |
| #17 · `b18_l4802.py` | 140.599, 196.925, 0.168 | Las cifras son las mismas, pero numpy las imprime en notación científica (`[1.40599e+02 …]`): formato (véase M9, menores). | `b18_l4802.out` |

El comparador propio añade, por el mismo motivo (referencias cruzadas a R), `b12`, `b14`, `b19` y `b20`; todas cuadran con R o con `par_verifica_py.out`. Dos de esas referencias van acompañadas de una explicación incorrecta (M2 y M7, abajo).

## Módulo 4.1 · De ARMA a ARIMA (l. 2749–2997)

- **Correcto:** la definición; la expansión $(1-\phi B)(1-B) = 1-(1+\phi)B+\phi B^2$ con $\phi_1^*+\phi_2^*=1$; las raíces $1.0000$ y $3.9308$; la equivalencia IMA(1,1) ↔ SES con $\alpha = 1+\theta$ (convenio de R); ARIMA(0,2,2) ↔ Holt con restricciones; el signo de $\rho_1$ igual al de $\theta$ en el MA(1). Las afirmaciones del simulador del Nilo se cumplen: varianzas $28\,637.95 \to 28\,268.34 \to 80\,055.01$ (razón $d=2/d=1$: 2.832) y $\hat\rho_1(d=2) = -0.6264 < -0.5$ (`par_verifica.out` § M1). La «anomalía» (razón 1.006 frente a 32.8) está bien explicada: la varianza de largo plazo de $w_t$ es $\sigma^2(1+\theta)^2/(1-\phi)^2 = 0.0285\,\sigma^2$, y por eso integrar casi no la dispara.
- Sin hallazgos.

## Módulo 4.2 · Box–Jenkins (l. 2998–3213)

- **Correcto:** el ciclo; comparar AICc y BIC dentro del mismo $d$; normalidad necesaria para los intervalos, no para las estimaciones; `fitdf = p + q`. El bloque R reproduce Ljung–Box(20) $p = 0.7997$ y el pronóstico $816.18,\ 835.56,\ 840.49$.
- **l. 3197–3200 [T13:449–452] · imprecisión (código y explicación; confirmada).** El bloque Python aplica Ljung–Box a `ajuste.resid` **completo**, cuyo primer elemento es el dato crudo $y_1 = 1120$ (el arranque difuso de statsmodels), y atribuye el $0.761$ frente al $0.7997$ de R a que «cada programa inicializa el filtro a su manera». Sin ese primer «residual», el mismo bloque da $p = 0.8225$ (`par_verifica_py.out` § Bloque M2). El capítulo enseña dos prácticas opuestas: el bloque del M4 (l. 3692) y el de la TRM (l. 5338) lo descartan expresamente («el primer residual es y_1 … se descarta»). Basta con usar `ajuste.resid[1:]` y corregir el comentario.
- **l. 3100–3104 [T13:352–357] · imprecisión (juicio, ilustrado con una ejecución).** La regla dice: «si [la raíz cerca del círculo] es del MA, la serie se diferenció de más y hay que **bajar** $d$». Le falta la salvedad que el propio M10 necesita. En el ARIMA(2,1,2) de la TRM, las raíces MA valen $1.0000$, pero las AR, $1.0042$ (`b19_l5171.out`; `par_verifica3.out`): es una cancelación de factores AR y MA casi comunes, no una sobrediferenciación. Bajar $d$ sería un error en una serie donde «sobre $d$ no hay discusión» (l. 4956). La regla solo vale cuando la raíz unitaria del MA no tiene pareja en el AR. El ítem a#4 del preparcial usa la misma regla, pero ahí el enunciado aísla el caso y es correcto.

## Módulo 4.3 · Elegir $d$ (l. 3214–3535)

- **Correcto (todo confirmado por ejecución, `par_verifica.out`):**
  - Pruebas: ADF $-3.3657$ ($p = 0.0642$, $k = 4$); KPSS $0.9654$ ($p < 0.01$); `PP.test` $Z(t_\alpha) = -6.6901$ (es $Z(t_\alpha)$, con constante y tendencia, como dice el texto).
  - `ndiffs`: 1 / 0 / 0. El ADF de `ndiffs` es `ur.df(type = "drift", lags = 1)`, $\tau_\mu = -4.0487$ frente al crítico $-2.89$. Los truncamientos son $\ell_R = 4$ y $\ell_{legacy} = 12$, y `nlags = "auto"` usa 5 rezagos (`par_verifica_py.out`).
  - Modelo de dos medias: $\hat\sigma = 127.03$, $\beta = -247.78$ (1.951 desviaciones), escalón en la posición 29 ($\tau = 0.28$); $100/\hat\sigma = 0.787$.
  - La derivación del KPSS con escalón ($e_t$ por tramos, $\max|S_t| \approx \tau(1-\tau)n|\beta|$, $\mathrm{KPSS} \sim n\beta^2/\hat\sigma^2_{LP}$) y la fórmula de Bartlett.
- **Monte Carlo del escalón, réplica exacta (`par_verifica_mc.out`):** KPSS rechaza el 4.8 % sin escalón y el 100 % con él; `ndiffs(kpss)` pide diferenciar el 100 % de las veces y `ndiffs(adf)`, el 0.5 %; `adf.test` no rechaza en el 86.4 % frente al 5.4 %. En la malla: 4.5 % con $|\beta| = 0$; 70.75 % con $\ell=4$ y 44.5 % con $\ell=12$ para $|\beta| = 100$; KPSS medio 1.0677 y 1.2288 con 200 y 300. Las réplicas independientes con otra semilla dan cifras compatibles (p. ej., 69.25 % y 70.5 % en $|\beta| = 100$).
- **Simulación PP/ADF con raíz unitaria verdadera (l. 3291–3296):** el texto dice 100 % y 51.3 %. La cifra sale de `Htmls_Series/diapositivas/fuentes/verificacion/verifica_directo_r46_cap4.R`. Una variante propia (sd de los residuales, $n = 99$ + 1) da 100 % y 51.2 % (`par_verifica.out`). Se confirma.
- Sin hallazgos.

## Módulo 4.4 · Identificar $p$ y $q$ (l. 3536–3703)

- **Correcto:** las ACF/PACF de $d = 0, 1, 2$; la banda $\pm 0.197$; el rezago 8 ($0.2312$), único fuera además del 1; el AR(1) con $\phi = 0.5$ entra en la banda desde el rezago 3 ($0.125 < 0.196$). Los recuentos del comentario JS (2 de 20 en la ACF de $d = 1$ y de $d = 2$; 4 frente a 7 en la PACF; 1 en $d = 0$) coinciden con el JSON. El MA(1) da $\hat\theta = -0.7329$ (e.e. $0.1143$, $t = -6.41$), $\hat\sigma^2 = 20\,599.87$ y Ljung–Box $p = 0.6737$. El AICc favorece al $(1,1,1)$ por $1.71$ y el BIC al $(0,1,1)$ por $0.76$ (`par_verifica2.out` § M4, M6). El método por defecto de `pacf` es `ywadjusted`, como dice el comentario.
- Sin hallazgos.

## Módulo 4.5 · La constante (l. 3704–3898)

- **Correcto:** $\mu_w = c/\phi(1)$ y su lectura según $d$; el comportamiento de `stats::arima` (ignora `include.mean` con $d \ge 1$), de `Arima` (avisa con $d \ge 2$, mensaje literal confirmado en `b09_l3823.out`), de `auto.arima` y de statsmodels (`trend="t"` con $d = 2$ lanza `ValueError`, `b10_l3856.out`). $\hat\delta = -2.8827$ (e.e. $2.0167$, $t = -1.43$), $\hat\phi = 0.2707$ y $c = -2.102$; AICc $1268.06$ frente a $1267.51$; $(740-1120)/99 = -3.838$ y $247.78/99 = 2.503$. En la TRM, $\hat\delta = 8.00$ (e.e. $10.36$), que es exactamente la media de las diferencias, $8.0009$ (`par_verifica_py.out`).
- **l. 3866–3869 [T46:331] · menor.** El comentario dice «919.35 es EXACTAMENTE la media muestral». statsmodels devuelve $919.350541$ (`par_verifica_py.out`). La explicación de fondo es correcta: en los valores de R la verosimilitud es mayor ($-637.0388$ frente a $-637.0397$), y arrancando ahí statsmodels se queda en $920.7037$. Basta con «prácticamente».

## Módulo 4.6 · Estimar y comparar (l. 3899–4086)

- **Correcto (`par_verifica2.out` § M6):**
  - Fórmulas de AIC, AICc y BIC con $k = p+q+1$ (más la constante) y $n^* = n - d$. El argumento de que el AICc no cruza la frontera de $d$ es correcto.
  - Mejores por $d$: 1282.50/1292.50, 1267.51/1274.28, 1264.60/1273.50.
  - Con $d = 1$, cuatro modelos quedan a menos de 2 puntos, y todos pasan Ljung–Box. Ljung–Box(20) rechaza **ocho** modelos.
  - Raíces: AR 1.1614 (mejor de $d=0$), MA 1.144 (mejor de $d=1$), MA 1.0316 y 1.0483 en los buenos de $d=2$.
  - Cuatro modelos con $d=2$ y $|\text{raíz MA}| \le 1.001$: (0,2,1), (0,2,2), (1,2,1) y (2,2,1).
  - `f.aicc` de statsmodels usa `nobs_effective`.
- El hallazgo del ARIMA(2,1,2) que muestra el explorador va en el M7.

## Módulo 4.7 · Dentro de `auto.arima` (l. 4087–4301)

- **Correcto:** los pasos del algoritmo (cuatro modelos iniciales más (0,d,0) sin constante, vecindario $|p'-p|\le1$, $|q'-q|\le1$, con o sin constante, reinicio en la primera mejora); el umbral de 1.01; que `approximation` no se activa con $n = 100$. Escalonada, 18 modelos; exhaustiva, 42; las dos eligen (1,1,1) con 1267.507. El podio de siete modelos tiene las diferencias $0.556, 0.703, 1.462, 1.709, 1.815, 1.841$; el octavo está a $2.126$ (`par_verifica2.out` § M7).
- **l. 4133–4134 [T79:46–48] frente al explorador del M6 · imprecisión (confirmada).** El texto dice que el ARIMA(2,1,2) del Nilo «tiene una raíz AR de módulo 1.001». Es cierto **para el ajuste CSS-ML de `Arima()`**, que es el que usa `auto.arima`: $0.0009$ por encima de 1 sin deriva, igual con deriva. Pero el explorador del M6, construido con `stats::arima(method = "ML")`, muestra ese mismo modelo con raíces mínimas AR $2.241$ y MA $1.122$, AICc $1271.54$ y sin aviso (`precalculo/salidas/cap4_arima.json`, clave `212`). Además, ese ajuste ML es un óptimo local: su $\log L = -630.445$ es peor que el $-630.169$ de CSS-ML (`par_verifica3.out`). Quien pase del explorador al M7 ve dos versiones incompatibles del mismo modelo. Conviene decir que la raíz depende del estimador, o rehacer la casilla del explorador con el óptimo global.
- **l. 4193–4196 [T79:107–110] · menor.** «detrás de él hay siete candidatos indistinguibles». Los siete modelos a menos de 2 puntos **incluyen** al ganador: detrás de él hay seis. El encabezado de la nota («Siete modelos a menos de 2 puntos») y el quiz (ítem 7) lo dicen bien.
- **l. 4278–4281 [T79:192–195] · imprecisión (explicación; confirmada).** El bloque Python atribuye la diferencia de AICc con R ($0.04$) a que «statsmodels no descuenta $d$ en nobs». Usar 100 o 99 en la corrección mueve el AICc en $0.0026$ ($1267.4687$ frente a $1267.4713$). La diferencia está en la log-verosimilitud: el AIC de statsmodels es $1267.2187$ y el de R, $1267.2544$ (`par_verifica_py.out` § M7). La explicación correcta es la que el propio capítulo da en el M2: cada programa inicializa el filtro a su manera.

## Módulo 4.8 · Diagnóstico (l. 4302–4537)

- **Correcto (`par_verifica2.out` § M8):**
  - Diagnóstico del ARIMA(1,1,1): Ljung–Box(20) $p = 0.7997$, Shapiro $p = 0.7312$, raíces 3.9313 y 1.144, e.e. 0.1194 y 0.0605.
  - Tabla de sobrediferenciación: $\hat\theta = 0.3783, -0.7329, -1.0000, -1.0000$; $\rho_1(d=3) = -0.7188$; con $\hat\theta = -1$, $\hat\sigma^2 = 28\,268.34$ y $80\,055.05$, que reproducen $\operatorname{Var}(\nabla^{d-1}y)$. La firma $\nabla^2 y = \varepsilon_t - \varepsilon_{t-1}$ es correcta.
  - `log(lynx)`: varianza $1.653 \to 0.687$ ($-58.4$ %); ADF, KPSS y PP coinciden en $d = 0$ (también `ndiffs` con las tres pruebas); el ARIMA(2,1,1) tiene $|\text{raíz MA}| = 1$.
  - Escalón: medias 1097.75 y 849.97; $\hat\beta = -247.78$ (e.e. 28.15, $t = -8.80$); AICc 1257.91; Ljung–Box 0.8124.
  - Tabla fuera de muestra: RMSE y MAE de los cinco modelos exactos; desviación típica de los residuales, 139.67.
- **l. 4518 [T79:432] · menor.** «se queda a 0.001 del borde»: la distancia es 0.0012 con $d = 2$ y 0.0020 con $d = 3$ (`b16_l4500.out`).

## Módulo 4.9 · Pronóstico (l. 4538–4838)

- **Correcto (`par_verifica2.out` § M9; `b17_l4748.out`):**
  - Tabla de formas: anchos 561→677, 557→781, 555→708 y 613→2771; pendientes 0.254, 0, −2.883 y −4.049.
  - En el ARIMA(1,2,1), la segunda diferencia del pronóstico decae exactamente como $\hat\phi^h$ (cociente $-0.3924$ en cada paso), $1/(1-\hat\phi) = 0.7182$, ancho por la fórmula 2427.96 frente a 2771.45 de `forecast()`. La explicación por la no invertibilidad es correcta: con $\hat\theta = -1$ el estado no se recupera de los datos y la incertidumbre de la pendiente añade varianza que crece como $h^2$.
  - Pesos y bandas: la forma cerrada de $\psi_j$; $\psi_\infty = 0.1688$; $\sigma_{30} = 199.363$ frente a $778.02$; error de reconstrucción 9.08e−11. En BJsales, $\psi_\infty = 2.9883$ y a doce pasos el cociente frente a la caminata es 1.9619.
  - Las seis consecuencias de la derivación, incluido $h^{3/2}$ con dos raíces unitarias. $z_{0.90} = 1.282$. En la TRM, el 80 % cubre el 83.9 % a un mes (`par_verifica2.out` § M10).
  - El JS de `pesos-psi-sigma` y `forma-pronostico` usa $\psi_{0..h-1}$ y el $\sigma$ del mismo ajuste CSS-ML.
- **l. 4579 [T79:493] frente a l. 3829/3867 y el quiz (l. 8974) · menor.** La media del ARIMA(1,0,1) aparece como $920.56$ en el M9 (ajuste `Arima`, CSS-ML) y como $920.7037$ / $920.70$ en el M5 y en el quiz (ajuste `arima`, ML). Las dos son correctas para su estimador (`par_verifica2.out` § M9, § M5), pero el capítulo no avisa de que el mismo modelo da dos «medias». Es el mismo fenómeno que el capítulo explica para $\sigma^2$ en el ejercicio 3.
- **l. 4822 [T79:736] · menor (formato).** El comentario muestra `[140.599 140.599 196.925 0.168]`, pero numpy imprime `[1.40599e+02 1.40599e+02 1.96925e+02 1.68000e-01]` (`b18_l4802.out`). Las cifras coinciden; basta con `np.round(...).tolist()` o con ajustar el comentario.

## Módulo 4.10 · TRM, puente y cierre (l. 4839–5774)

- **Correcto (`b19_l5171.out`, `b20_l5284.out`, `par_verifica2.out` § M10, `par_verifica3.out`):**
  - Cuadro del Nilo: las cifras repetidas coinciden; el pronóstico a largo plazo es 842.17; el semiancho pasa de ±278.40 a ±390.74.
  - TRM, identificación y rejilla: pruebas; ACF en niveles 0.9637; $\hat\rho_8 = -0.190$ con banda 0.167; rejilla; ventaja de 2.56 del (2,1,2) con raíces AR 1.0042 y MA 1.0000. `auto.arima` también lo marca `Inf` con su ajuste CSS-ML, que es el mismo óptimo, así que el «aquí acierta» es exacto.
  - Búsquedas exhaustivas: 192 modelos con la parte estacional permitida y 42 sin ella.
  - Diagnóstico de la caminata: Ljung–Box 0.189/0.206, Shapiro 0.0006, residuales al cuadrado 0.857. El primer residual de R es 2.401, y sin él R da exactamente las cifras de Python.
  - OPG 11.17 frente a OIM 10.35. Tabla del abanico. 6 de 137 cambios fuera (5 por arriba) y 11 de 126 a doce meses. Curtosis 5.09 y 2.8; asimetría 0.761 (residuales 0.764). Los saltos mayores son los de marzo de 2020 y julio de 2022.
  - Puente: ARIMA(0,1,5); $\rho_{12} = 0.7245$, $\rho_{24} = 0.6727$, banda 0.1633, $Q = 222.4$. Con $p, q \le 8$ gana el ARIMA(8,1,3) con deriva ($\rho_{12} = 0.437$). El *airline* da $\rho_{12} = -0.0515$ y Ljung–Box $p = 0.233$, con $n^*$ de 143 y 131.
  - Ejercicios 1–3: todas las cifras de los bloques y de las discusiones (`b21`, `b22`, `b23` `.out`).
- **l. 5155–5156 [T10:317] · imprecisión (confirmada).** «A doce meses … $8.7\,\%$; el Capítulo 6 lo confirma fuera de la muestra, con una cobertura del $89.6\,\%$». Ese 89.6 % es `cob95` del naïve en `casos/trm` de `precalculo/salidas/cap6_evaluacion.json`: la cobertura **promediada sobre los horizontes 1 a 12** de los orígenes móviles, no la cobertura a doce meses. Dentro de la muestra, a doce meses la cobertura es 91.3 % (`par_verifica2.out`). La comparación mezcla dos medidas distintas. Basta con decir «sumando los horizontes de 1 a 12».
- **l. 5156–5158 [T10:318–320] · menor.** «con $\hat\rho_1 = 0.088$ la varianza real de los cambios a 3–12 meses es entre 1.07 y 1.14 veces esa cifra». El intervalo 1.07–1.14 sale de la razón **empírica** de cuadrados medios (1.097, 1.144 y 1.069 para $h$ = 3, 6 y 12). Con solo $\hat\rho_1$, la razón sería $1 + 2\hat\rho_1(h-1)/h$, es decir, 1.117–1.161 (`par_verifica2.out` § M10). Las cifras son correctas, pero no se deducen de $\hat\rho_1$ como sugiere la frase.
- **l. 5452 [T10:614] · menor.** El resumen dice: «con $d \ge 2$ el software se niega a [ajustar la constante]». Se niega `forecast::Arima`; statsmodels admite el término cuadrático, y el propio bloque del M5 lo ajusta (`trend=[0, 0, 1]`, `b10_l3856.out`). La tabla del M5 lo dice bien.
- **l. 5053–5056 [T10:215–218] · dudoso (juicio).** El argumento «si el tipo de cambio fuera predecible, alguien ya habría arbitrado» se aplica a la TRM **promedio del mes**. El promedio mensual de una caminata diaria no es una caminata: sus diferencias tienen $\rho_1 \to 0.25$ (efecto Working; 0.2492 con $m = 21$ días, 0.2608 simulado), y la TRM da $\hat\rho_1 = 0.0876$ con error estándar aproximado de $0.0854$ (`par_verifica3.out`). La conclusión de que la serie es compatible con una caminata no cambia, pero la justificación financiera vale para el dato diario, no para el promedio. Puede dejarse; se señala por rigor.

## Autoevaluación del capítulo (`AUTOEVALUACIONES['cap4']`, l. 8887–9093 [JS:1137–1343])

Ocho ítems de cuatro tipos, como anuncia l. 5475. Las claves de los ítems 1, 2 (151.97; recalculado 151.965, tolerancia 0.4), 3, 5, 7 y 8 son correctas, y sus retroalimentaciones también (`par_verifica2.out` § Quiz).

- **Ítem 4 (l. 8968 [JS:1218]) · imprecisión (confirmada).** Se marca como cierta la opción «Con $d = 1$ la constante es la media de las *diferencias*». Con la notación del propio M5, la constante es $c$, y $c = \mu_w\,\phi(1)$: en el Nilo, $c = -2.10$ frente a $\mu_w = \hat\delta = -2.88$ (l. 3796; `par_verifica2.out` § M5). Solo es cierta para la **deriva** de `forecast` o con $p = 0$. Se arregla escribiendo «la deriva ($\mu_w$)» o «$c/\phi(1)$».
- **Ítem 6 (l. 9008–9040 [JS:1258–1290]) · imprecisión (en parte confirmada).**
  1. La retroalimentación de la primera opción dice que la ACF de la gráfica «lleva veinte rezagos sin acercarse a cero». Pero la gráfica es `NILO.identificacion.cruda.acf`, con $r_{10} = 0.0898$ y nueve de los veinte rezagos dentro de la banda $\pm 0.196$ (9, 10 y 14–20; `par_verifica2.out` § M4). La `descripcionGrafico` («sin llegar a cortarse») es defendible; «sin acercarse a cero», no.
  2. La retroalimentación de la tercera opción afirma: «La conclusión sobre $d$ es correcta». La clave, por su parte, dice «hay que diferenciar antes de leer $p$ y $q$». Las dos frases dan por bueno el $d = 1$ que el M8 y el M10 ponen en duda: «El ARIMA(1,1,1) probablemente está diferenciando una serie que no tiene raíz unitaria» (l. 4414–4416). La lección del ítem sigue siendo válida (con esa ACF no se leen $p$ y $q$), pero conviene decir «no es estacionaria alrededor de una media fija: raíz unitaria o cambio de nivel», como hace el M4 (l. 3559–3560).

## Módulo 4.11 · Simulacro (l. 5775–5845; datos l. 9403–9530) — no se edita aquí

La página no incluye la clave, a propósito. Se resolvió cada ítem para comprobar que tiene una respuesta única y defendible y que los datos son coherentes (`par_verifica2.out` § Quiz y simulacro):

- 1: $\rho_2 = 0.3963$.
- 2: las afirmaciones correctas son la 1, la 3 y la 5. La 2 es falsa porque $c = 67.1246 \times 0.1434 = 9.6257$ está bien calculada; las raíces correctas son 1.441 y 1.8816.
- 3: A → AR(2), B → ARMA(1,1), C → MA(2) ($|r_1| = 0.605 > 0.5$ descarta el MA(1)), D → AR(1); sobran MA(1) y ruido blanco.
- 4: Yule–Walker da $1.1309, -0.5301$, que es la tercera opción.
- 5: el orden es MA(2) 114.785, MA(1) 115.587, ARMA(1,1) 115.999 y AR(1) 125.047.
- 6: 107.18.
- 7: SES, «sobra la diferencia» (raíz 1.0417), AR(2) con 1.65/−0.65, caminata con deriva 1.4 y Holt ($\alpha = 0.55$, $\beta = 0.3636$, admisible).
- 8: 13 grados de libertad, crítico 22.36, $p = 0.0379$: se rechaza, primera opción.
- 9: son ciertas «ADF apunta a diferenciar», «ADF y KPSS coinciden» y «PP y KPSS opuestas».
- 10: ARIMA(0,1,1).

Los recuentos de forma que da la prosa (l. 5797–5800: tres de opción única, dos múltiples, dos de emparejar, una de ordenar y dos numéricas) y la tabla de módulos coinciden con los datos. **Sin hallazgos de corrección.** En el ítem 7, la fila $(1 + 0.25B)(1 - B)y_t = (1 - 0.96B)\varepsilon_t$ hace competir «sobra la diferencia» con «raíz en 1.042, fuera del círculo: no sobra nada». La clave es la que el capítulo enseña (M1, l. 2963–2981), pero es una lectura heurística: **dudoso** menor, sin acción necesaria.

## Módulo 4.12 · Preparcial (l. 5845–5900; `preparcial-corte-2.html`) — no se edita aquí

- El verificador del proyecto (`precalculo/verifica_preparcial2.py`, solo lectura) da 502 comprobaciones y 1 fallo (`par_preparcial2_verificador.out`). El fallo es de §8 (casi duplicados): el ítem b#6 se parece a una pregunta del capítulo 3 (Jaccard 0.143). Es un problema de solapamiento con material que el estudiante ya vio, no de corrección.
- Recálculo independiente de todas las claves numéricas y de las cifras que sostienen las claves de opción (`par_verifica_preparcial.out`): a#1 −0.3742; a#2 factores 0.5 y 0.3; a#6 0.9953; b#1 0.4; b#2 −0.4851; b#3 4.187; b#4 −0.7; b#5 9.0327; b#6 7.491 ($p = 0.0236$; el texto dice 0.0237 «en R», por las cifras sin redondear); b#7 281.626; b#8 3.6559; b#9 1253.511; b#10 99.3275; b#11 6.259; b#12 83.099; c#1 1.2515/1.2517; c#4 0.9882; c#5 148.41 teórico frente a 148.18 publicado (coherente). En el simulacro del preparcial: 2.8402, −0.36, $t = 0.98$, 395.670 y 9.104. Las claves de opción a#4, a#5, c#2, c#3, c#6, c#7 y c#8 son correctas por razonamiento. Las de los ítems de gráfico (d#1–d#6) solo se comprobaron con el verificador del proyecto, no de forma independiente.
- **Sin hallazgos de corrección.** Fuera de esta lente: el M12 sigue anunciando el Parcial 2 del «miércoles 14 de octubre» (l. 5863–5864), ya aplicado.

---

## Resumen

| Clase | N.º | Dónde |
|---|---|---|
| **Error** | 0 | — |
| **Cifra incorrecta** | 0 | — |
| **Imprecisión** | 7 | M2 Python, Ljung–Box con $y_1$ como residual (l. 3197); M2, regla «raíz MA ⇒ bajar $d$» sin la salvedad de la cancelación (l. 3100); M7 frente a M6, el ARIMA(2,1,2) con dos versiones según el estimador (l. 4134); M7 Python, la diferencia de AICc mal atribuida a nobs (l. 4280); M10, el 89.6 % del cap. 6 presentado como cobertura a 12 meses (l. 5155); quiz ítem 4, «la constante es la media de las diferencias» (l. 8968); quiz ítem 6, «sin acercarse a cero» y «la conclusión sobre $d$ es correcta» (l. 9020, 9030) |
| **Menor** | 7 | M5 «EXACTAMENTE» (l. 3866); M7 «detrás de él hay siete» (l. 4195); M8 «0.001 del borde» (l. 4518); M9 920.56 frente a 920.70 sin aviso (l. 4579); M9 formato de numpy (l. 4822); M10 razón 1.07–1.14 atribuida a $\hat\rho_1$ (l. 5157); resumen «el software se niega» (l. 5452) |
| **Dudoso** | 2 | M10, argumento de arbitraje aplicado a un promedio mensual (l. 5054); simulacro ítem 7, fila 2 (lectura heurística) |

Todas las imprecisiones y los menores, salvo la regla del M2 y el ítem 6 (en parte), están confirmados con una ejecución guardada. La regla del M2, el argumento financiero y el ítem 7 del simulacro son juicio. **No se pudo comprobar de forma independiente:** las claves de los seis ítems de gráfico del preparcial (d#1–d#6), que solo pasó el verificador del proyecto; la lógica de render del JS más allá de las fórmulas (lecturas, interpolación, ejes), que no se ejecutó en el navegador; y el simulador `traza-auto-arima`, del que solo se contrastaron los datos (18 y 42 modelos, podio), no el recorrido paso a paso.
