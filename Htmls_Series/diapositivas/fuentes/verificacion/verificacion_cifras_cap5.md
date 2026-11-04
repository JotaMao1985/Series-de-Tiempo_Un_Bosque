# Verificación de cifras · Capítulo 5 (diapositivas)

Generado por `verifica_cifras_cap5.py`. Cada fila es una cifra (o afirmación) de las diapositivas o de sus notas, con las fuentes contra las que se contrastó.

## Cómo se verificó

- **J** · `precalculo/salidas/cap5_sarima.json`, el precálculo del capítulo. **J4** · `cap4_arima.json`. **J3** · `cap3_arma.json`.
- **R** · recálculo directo sobre los datos congelados, `verifica_directo_cap5.R` → `directo_cap5.json`, en R version 4.6.0 (2026-04-24) (forecast 9.0.2, tseries 0.10.62). Incluye lo que J no guarda: la tabla de varianzas con parte AR, el horizonte de 24 meses, el error del mes 12 y los crecimientos anuales del Módulo 11.
- **PY** · statsmodels 0.14.6, `verifica_python_cap5.py` → `directo_python_cap5.json`.
- **DOC** · ayuda de R de `AirPassengers`, `USAccDeaths`, `co2`, `ets`, `nsdiffs` y `snaive`, y el NEWS de forecast, `verifica_docs_cap5.R` → `docs_cap5.json`.
- **CALC** · aritmética sobre los datos (ACF con divisor n, bandas 1.96/√n) o sobre las fuentes anteriores. **C** · texto del capítulo. **DEF** · definición o convención.
- La fuente se redondea a los decimales que muestra la diapositiva, a la mitad hacia arriba. Las ACF y las bandas se recalculan desde los datos para no redondear dos veces.
- La TRM es la copia congelada de `datos_series.json`; **no** se cotejó con datos.gov.co.
- Los tres gráficos animados se comprueban como idénticos a lo que `genera_animados_cap5.py` construye desde J.

## Resumen

- Cifras y afirmaciones registradas: **768**
- Verificadas contra al menos una fuente: **707**
- Definiciones o convenciones: **61**
- Comprobadas a mano en una fuente pública fuera del repositorio (`WEB`, con fecha): **7**
- Marcadas `[SIN VERIFICAR]`: **5**
- No coinciden: **0**

Contrastes por tipo de fuente: C 101, CALC 193, DOC 17, J 331, J3 2, J4 6, PY 10, R 223, WEB 7.

## Código proyectado, ejecutado

Cada bloque `r` se ejecutó en R version 4.6.0 (2026-04-24) y sus líneas `#>` se compararon con la salida real.

| Bloque (primera línea) | Salidas esperadas | Encontradas | Estado |
|---|---|---|---|
| `library(forecast)` | 2 | 2 | coincide |
| `library(forecast)` | 4 | 4 | coincide |
| `library(forecast)` | 4 | 4 | coincide |
| `library(forecast)` | 2 | 2 | coincide |

## Lo que no se pudo verificar (`[SIN VERIFICAR]`)

| Diapositiva | Qué | Por qué |
|---|---|---|
| Cada afirmación es un dato, una definición, una interpretaci | origen de la TRM · nombre y difusión del airline · tabla de métodos modernos · secciones de las lecturas | ver la lista en las notas y en este informe |
| Cuatro series conducen el capítulo, y la cuarta es un contra | origen de la TRM en datos.gov.co | solo se comprobó la copia congelada de datos_series.json |
| El *airline*: dos diferencias y dos MA para una serie con te | que Box y Jenkins lo bautizaran así · «el SARIMA más usado del mundo» | el libro no está en el repositorio; afirmación del capítulo |
| El SARIMA frente a lo que se usa hoy: cuándo, no cuál es mej | la tabla entera (dónde brilla y dónde falla cada método) | el capítulo la resume de M4, M5 y la literatura sin citar resultados concretos |
| Para seguir: tres ejercicios y las lecturas {columnas=1:1 .a | Shumway y Stoffer, cap. 3.9 · Box, Jenkins, Reinsel y Ljung, cap. 9 | los libros no están en el repositorio |

## Observaciones sobre el material (no corregidas en silencio)

1. Módulo 5: ψ₁₂ = 1.0412 y ψ₁₃…₂₃ = 0.8632 en el texto; el bloque de R del Módulo 7 imprime 1.0413 y 0.8633. Es redondeo: el bloque usa los coeficientes redondeados (−0.4018, −0.5569). Las diapositivas usan los del texto, que coinciden con J.
2. Módulo 4: el capítulo da ρ₁₁ = ρ₁₃ = 0.14705 «del modelo ajustado». Con los coeficientes sin redondear es 0.14707; 0.14705 sale con −0.4018 y −0.5569. A cuatro decimales los dos son 0.1471.
3. Autoevaluación, pregunta 2: la explicación dice «ρ₂ = ρ₁² ≈ 0.36» para el AR(1)×SAR(1). En el proceso multiplicado ρ₂ = 0.3637 y ρ₁² = 0.3619: no es una igualdad, aunque los dos redondean a 0.36.
4. Autoevaluación, pregunta 6: está etiquetada «módulo 6» y su explicación remite a la lección del Módulo 10. Menor.
5. Módulo 3: «∇ solo reduce la varianza a la vigésima parte» y «∇₁₂ sola la reduce cincuenta veces». Los cocientes son 17.2 y 51.3. «La vigésima parte» es una aproximación generosa.
6. Módulo 6, advertencia final: «los coeficientes casi coinciden con los de R (diferencia 6 × 10⁻⁵)» con statsmodels sin `simple_differencing`. Con statsmodels 0.14.6 la diferencia máxima es 2.4 × 10⁻⁴ (−0.4021 y −0.5571 frente a −0.4018 y −0.5569). Sigue siendo despreciable; depende de la versión. No se proyecta.
7. Las dos copias de la TRM llevan fechas de consulta distintas: `cap5_sarima.json` dice «consulta: 2026-07-24» y `datos_series.json` (y el capítulo 4) «2026-07-26». No afecta a ninguna cifra (las dos son la misma copia de 138 meses), pero conviene unificarlo.
8. Resueltas en el capítulo el 2026-10-27 (`114b910`) cinco observaciones de la primera pasada: los ocho dobles redondeos (M1, M4, M7, M11 y las preguntas 1 y 8), los «%» de crecimiento del Módulo 11, que eran 100·Δlog y ahora son porcentajes, la nota del puente del Módulo 7, que ahora usa el ARIMA(0,1,5) y no compara AICc entre distintos D, el enunciado y dos explicaciones de la pregunta 8, y las secciones de FPP3 de las lecturas. Capítulo y diapositivas dan ahora las mismas cifras, y las comprobaciones de tipo «capítulo» lo exigen. Siguen en J dos textos que el capítulo embebe pero no muestra: `puente_cap4` (el ARIMA(0,1,1) con AICc −238.64) y `origen_movil.nota` («corona a la regresión armónica»).
9. Resueltas en el capítulo el 2026-11-03 las cuatro observaciones de la auditoría del 2026-10-28 (`auditoria_cap5.md`): la invertibilidad del Módulo 7 («aunque justo»), el `auto.arima` con m = 365 del Módulo 10 (ilustrado con ruido blanco), los errores estándar «el doble» del Módulo 8 y los «Paso 0…4» del Módulo 7. El capítulo lee ahora la invertibilidad en Θ̂ y explica que 0.9524 = 0.5569^(1/12); el ejemplo de m = 365 usa un seno anual (ARIMA(0,0,0)(0,1,0)[365]); los cocientes son 1.4 y 2.4; y el caso sigue las etapas 1–5 del protocolo. Las comprobaciones de tipo «capítulo» exigen el texto nuevo.

## Tabla de cifras

### Cada afirmación es un dato, una definición, una interpretación o una opinión

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `24` | horizonte | J: cap5_sarima.json › horizonte = 24 | verificado |

### El capítulo 4 dejó toda la estructura sobrante en los múltiplos de 12

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.7245` | dato | J4: cap4_arima.json › puente_estacional.no_estacional.acf_12 = 0.7245 | verificado |
| `0.6727` | dato | J4: cap4_arima.json › puente_estacional.no_estacional.acf_24 = 0.6727 | verificado |
| `0.163` | dato | J4: cap4_arima.json › puente_estacional.no_estacional.banda = 0.1633<br>CALC: 1.96/√144 = 0.163333 | verificado |
| `222.4` | dato | J4: cap4_arima.json › puente_estacional.no_estacional.ljung_box_24.Q = 222.398<br>C: capítulo 5 contiene «$Q = 222.4$» | verificado |
| `0,1,5` | capítulo | C: capítulo 5 contiene «ARIMA($0,1,5$): cinco términos MA»<br>C: la nota del Módulo 7 ya no cita el AICc del ARIMA(0,1,1) | verificado |
| `-0.0515` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.11 = -0.0515<br>R: directo_cap5.json › m7.res_r12 = -0.051463 | verificado |
| `0.233` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.lb24_p = 0.233<br>R: directo_cap5.json › m7.lb24 = 0.233033 | verificado |
| `1949` | dato | R: directo_cap5.json › datos.ap_inicio = 1949<br>DOC: docs_cap5.json › airpassengers contiene «1949 to 1960» | verificado |
| `1960` | dato | R: directo_cap5.json › datos.ap_fin = 1960<br>DOC: docs_cap5.json › airpassengers contiene «1949 to 1960» | verificado |
| `144` | dato | R: directo_cap5.json › datos.ap_n = 144<br>J: cap5_sarima.json › airpassengers.n = 144 | verificado |
| `143` | dato | CALC: n − d con d = 1 = 143 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.airline.nobs = 131<br>R: directo_cap5.json › m2.n_w = 131 | verificado |

### Cuatro series conducen el capítulo, y la cuarta es un contraejemplo

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1949` | dato | R: directo_cap5.json › datos.ap_inicio = 1949 | verificado |
| `1960` | dato | R: directo_cap5.json › datos.ap_fin = 1960 | verificado |
| `1973` | dato | R: directo_cap5.json › datos.uad_inicio = 1973 | verificado |
| `1978` | dato | R: directo_cap5.json › datos.uad_fin = 1978 | verificado |
| `1959` | dato | R: directo_cap5.json › datos.co2_inicio = 1959 | verificado |
| `1997` | dato | R: directo_cap5.json › datos.co2_fin = 1997 | verificado |
| `144` | dato | R: directo_cap5.json › datos.ap_n = 144 | verificado |
| `72` | dato | R: directo_cap5.json › datos.uad_n = 72<br>J: cap5_sarima.json › usaccdeaths.n = 72 | verificado |
| `468` | dato | R: directo_cap5.json › datos.co2_n = 468<br>DOC: docs_cap5.json › co2 contiene «468 observations» | verificado |
| `138` | dato | R: directo_cap5.json › datos.trm_n = 138<br>J: cap5_sarima.json › trm_contraejemplo.n = 138 | verificado |
| `2015` | dato | R: directo_cap5.json › datos.trm_inicio = 2015-1 | verificado |
| `2026` | dato | R: directo_cap5.json › datos.trm_fin = 2026-6 | verificado |
| `1994` | documentación | DOC: docs_cap5.json › airpassengers contiene «Reinsel GC (1994)» | verificado |
| `1991` | documentación | DOC: docs_cap5.json › usaccdeaths contiene «Davis RA (1991)» | verificado |
| `R` | datos = datasets de R | R: directo_cap5.json › datos.ap_igual_datasets | verificado |
| `R` | datos = datasets de R | R: directo_cap5.json › datos.uad_igual_datasets | verificado |
| `R` | datos = datasets de R | R: directo_cap5.json › datos.co2_igual_datasets | verificado |

### La estacionalidad tiene un periodo fijado por el calendario; el ciclo, no

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `11.22` | dato | J3: cap3_arma.json › manchas.transformacion.sqrt.periodo = 11.2178<br>C: capítulo 5 contiene «11.22» | verificado |
| `11.2178` | dato | J3: cap3_arma.json › manchas.transformacion.sqrt.periodo = 11.2178 | verificado |

### Con datos mensuales la estacionalidad está en 12, 24 y 36, no en los primeros rezagos

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.762` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.11 = 0.7619<br>CALC: ACF de log(AirPassengers), rezago 12 = 0.761943 | verificado |
| `0.520` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.23 (empate: decide el exacto) = 0.5205<br>CALC: rezago 24 = 0.52049 | verificado |
| `0.520` | capítulo | C: capítulo 5 contiene «$0.520$» | verificado |
| `0.5205` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.23 = 0.5205 | verificado |
| `0.52049` | dato | CALC: ACF exacta en 24 = 0.52049 | verificado |
| `0.319` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.35 = 0.3193<br>CALC: rezago 36 = 0.319293 | verificado |
| `0.163` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.banda = 0.1633<br>CALC: 1.96/√144 = 0.163333 | verificado |
| `144` | dato | R: directo_cap5.json › datos.ap_n = 144 | verificado |
| `1.96` | convención | DEF: cuantil 0.975 de la normal | definición (no se mide) |

### Cuatro filas se parecen y solo tres de esas series son estacionales

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.954` | dato | CALC: ACF de airpassengers_log en el rezago 1, desde datos_series.json = 0.953703<br>J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.0 = 0.9537 | verificado |
| `0.762` | dato | CALC: ACF de airpassengers_log en el rezago 12, desde datos_series.json = 0.761943<br>J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.11 = 0.7619 | verificado |
| `0.520` | dato | CALC: ACF de airpassengers_log en el rezago 24, desde datos_series.json = 0.52049<br>J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.23 (empate: decide el exacto) = 0.5205 | verificado |
| `0.319` | dato | CALC: ACF de airpassengers_log en el rezago 36, desde datos_series.json = 0.319293<br>J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.35 = 0.3193 | verificado |
| `0.163` | dato | CALC: 1.96/√144 = 0.163333 | verificado |
| `0.707` | dato | CALC: ACF de usaccdeaths en el rezago 1, desde datos_series.json = 0.707471<br>CALC: ídem = 0.707471 | verificado |
| `0.629` | dato | CALC: ACF de usaccdeaths en el rezago 12, desde datos_series.json = 0.628589<br>J: cap5_sarima.json › airpassengers.firma.usaccdeaths.acf.11 = 0.6286 | verificado |
| `0.450` | dato | CALC: ACF de usaccdeaths en el rezago 24, desde datos_series.json = 0.450301<br>J: cap5_sarima.json › airpassengers.firma.usaccdeaths.acf.23 = 0.4503 | verificado |
| `0.302` | dato | CALC: ACF de usaccdeaths en el rezago 36, desde datos_series.json = 0.302041<br>J: cap5_sarima.json › airpassengers.firma.usaccdeaths.acf.35 = 0.302 | verificado |
| `0.231` | dato | CALC: 1.96/√72 = 0.230988 | verificado |
| `0.991` | dato | CALC: ACF de co2 en el rezago 1, desde datos_series.json = 0.990937<br>J: cap5_sarima.json › airpassengers.firma.co2.acf.0 = 0.9909 | verificado |
| `0.928` | dato | CALC: ACF de co2 en el rezago 12, desde datos_series.json = 0.928386<br>J: cap5_sarima.json › airpassengers.firma.co2.acf.11 = 0.9284 | verificado |
| `0.855` | dato | CALC: ACF de co2 en el rezago 24, desde datos_series.json = 0.855458<br>J: cap5_sarima.json › airpassengers.firma.co2.acf.23 (empate: decide el exacto) = 0.8555 | verificado |
| `0.783` | dato | CALC: ACF de co2 en el rezago 36, desde datos_series.json = 0.783179<br>J: cap5_sarima.json › airpassengers.firma.co2.acf.35 = 0.7832 | verificado |
| `0.091` | dato | CALC: 1.96/√468 = 0.090601 | verificado |
| `0.964` | dato | CALC: ACF de trm en el rezago 1, desde datos_series.json = 0.963663<br>J: cap5_sarima.json › airpassengers.firma.trm.acf.0 = 0.9637 | verificado |
| `0.636` | dato | CALC: ACF de trm en el rezago 12, desde datos_series.json = 0.63649<br>J: cap5_sarima.json › airpassengers.firma.trm.acf.11 (empate: decide el exacto) = 0.6365 | verificado |
| `0.490` | dato | CALC: ACF de trm en el rezago 24, desde datos_series.json = 0.489548<br>J: cap5_sarima.json › airpassengers.firma.trm.acf.23 = 0.4895 | verificado |
| `0.225` | dato | CALC: ACF de trm en el rezago 36, desde datos_series.json = 0.225218<br>J: cap5_sarima.json › airpassengers.firma.trm.acf.35 = 0.2252 | verificado |
| `0.167` | dato | CALC: 1.96/√138 = 0.166846 | verificado |
| `0.088` | dato | CALC: ACF de trm_diff en el rezago 1, desde datos_series.json = 0.08756<br>J: cap5_sarima.json › airpassengers.firma.trm_diff.acf.0 = 0.0876 | verificado |
| `-0.002` | dato | CALC: ACF de trm_diff en el rezago 12, desde datos_series.json = -0.002453<br>J: cap5_sarima.json › airpassengers.firma.trm_diff.acf.11 (empate: decide el exacto) = -0.0025 | verificado |
| `-0.067` | dato | CALC: ACF de trm_diff en el rezago 24, desde datos_series.json = -0.067215<br>J: cap5_sarima.json › airpassengers.firma.trm_diff.acf.23 = -0.0672 | verificado |
| `0.071` | dato | CALC: ACF de trm_diff en el rezago 36, desde datos_series.json = 0.071383<br>J: cap5_sarima.json › airpassengers.firma.trm_diff.acf.35 = 0.0714 | verificado |
| `0.167` | dato | CALC: 1.96/√137 = 0.167454 | verificado |
| `0.16745` | dato | CALC: 1.96/√137 = 0.167454 | verificado |
| `0.1675` | dato | J: cap5_sarima.json › airpassengers.firma.trm_diff.banda = 0.1675 | verificado |
| `137` | dato | J: cap5_sarima.json › airpassengers.firma.trm_diff.n = 137 | verificado |
| `1.96` | convención | DEF: cuantil 0.975 de la normal | definición (no se mide) |
| `0.52049` | dato | CALC: ACF exacta en 24 = 0.52049 | verificado |
| `0.70747` | dato | CALC: ACF exacta en 1 = 0.707471 | verificado |
| `0.85546` | dato | CALC: ACF exacta en 24 = 0.855458 | verificado |
| `0.63649` | dato | CALC: ACF exacta en 12 = 0.63649 | verificado |
| `0.520` | capítulo | C: capítulo 5 contiene «$0.520$» | verificado |
| `0.707` | capítulo | C: capítulo 5 contiene «$0.707$» | verificado |
| `0.855` | capítulo | C: capítulo 5 contiene «$0.855$» | verificado |
| `0.636` | capítulo | C: capítulo 5 contiene «$0.636$» | verificado |
| `-0.002` | capítulo | C: capítulo 5 contiene «{-0.002}» | verificado |
| `-0.00245` | dato | CALC: ACF de ∇TRM en 12 = -0.002453<br>R: directo_cap5.json › m1.trm_diff.1 = -0.002453 | verificado |
| `-0.0024` | capítulo (código en vivo) | C: capítulo 5 contiene «-0.0024» | verificado |
| `-0.0025` | dato | J: cap5_sarima.json › trm_contraejemplo.acf12 = -0.0025 | verificado |

### ¿Es estacional una serie con \(\hat\rho_{12}=0.636\) en niveles? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.636` | dato | J: cap5_sarima.json › airpassengers.firma.trm.acf.11 (empate: decide el exacto) = 0.6365<br>CALC: ACF de la TRM en 12 = 0.63649 | verificado |
| `0.636` | capítulo | C: capítulo 5 (autoevaluación) contiene «= 0.636$, muy por encima» | verificado |
| `0.6365` | dato | J: cap5_sarima.json › airpassengers.firma.trm.acf.11 = 0.6365 | verificado |
| `0.63649` | dato | CALC: ACF exacta de la TRM en 12 = 0.63649 | verificado |
| `138` | dato | R: directo_cap5.json › datos.trm_n = 138 | verificado |
| `0.167` | dato | CALC: 1.96/√138 = 0.166846<br>J: cap5_sarima.json › airpassengers.firma.trm.banda = 0.1668 | verificado |
| `0.964` | dato | J: cap5_sarima.json › airpassengers.firma.trm.acf.0 = 0.9637<br>CALC: rezago 1 = 0.963663 | verificado |
| `0.225` | dato | J: cap5_sarima.json › airpassengers.firma.trm.acf.35 = 0.2252<br>CALC: rezago 36 = 0.225218 | verificado |
| `-0.0025` | dato | J: cap5_sarima.json › trm_contraejemplo.acf12 = -0.0025 | verificado |
| `-0.002` | dato | CALC: ACF de ∇TRM en 12, exacta = -0.002453<br>J: cap5_sarima.json › airpassengers.firma.trm_diff.acf.11 (empate: decide el exacto) = -0.0025 | verificado |
| `-0.00245` | dato | CALC: ACF exacta de ∇TRM en 12 = -0.002453 | verificado |
| `-0.067` | dato | J: cap5_sarima.json › trm_contraejemplo.acf24 = -0.0672<br>CALC: ∇TRM, 24 = -0.067215 | verificado |
| `0.071` | dato | J: cap5_sarima.json › trm_contraejemplo.acf36 = 0.0714<br>CALC: ∇TRM, 36 = 0.071383 | verificado |
| `1.96` | convención | DEF: cuantil 0.975 de la normal, convención | definición (no se mide) |

### Multiplicar es preguntar dos veces: primero al mes anterior, después al año anterior {columnas=2:3}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `2024` | ejemplo inventado | DEF: año del ejemplo inventado del capítulo | definición (no se mide) |
| `2025` | ejemplo inventado | DEF: año del ejemplo inventado del capítulo | definición (no se mide) |
| `15` | ejemplo inventado | C: capítulo 5 contiene «2024 $15$ $20$»<br>C: capítulo 5 contiene «2025 $10$ $?$» | verificado |
| `20` | ejemplo inventado | C: capítulo 5 contiene «2024 $15$ $20$»<br>C: capítulo 5 contiene «2025 $10$ $?$» | verificado |
| `10` | ejemplo inventado | C: capítulo 5 contiene «2024 $15$ $20$»<br>C: capítulo 5 contiene «2025 $10$ $?$» | verificado |
| `0.6` | parámetro | DEF: φ del capítulo | definición (no se mide) |
| `0.7` | parámetro | DEF: Φ del capítulo | definición (no se mide) |
| `11` | dato | CALC: 20 − 0.6·15 = 11.0<br>C: capítulo 5 contiene «$20 - 0.6 \cdot 15 = 11$» | verificado |
| `7.7` | dato | CALC: 0.7·11 = 7.7<br>C: capítulo 5 contiene «$0.7 \cdot 11 = 7.7$» | verificado |
| `13.7` | dato | CALC: 0.6·10 + 7.7 = 13.7<br>C: capítulo 5 contiene «$0.6 \cdot 10 + 7.7 = 13.7$» | verificado |

### Multiplicar no es sumar: el rezago 13 aparece sin un parámetro propio

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.6` | parámetro | DEF: φ del capítulo | definición (no se mide) |
| `0.7` | parámetro | DEF: Φ del capítulo | definición (no se mide) |
| `0.42` | dato | CALC: φΦ = 0.42<br>C: capítulo 5 contiene «$-0.42 = -0.6 \cdot 0.7$» | verificado |
| `-0.42` | dato | CALC: −φΦ, el peso del satélite = -0.42<br>C: capítulo 5 contiene «$-0.42 = -0.6 \cdot 0.7$» | verificado |
| `10` | ejemplo inventado | C: capítulo 5 contiene «2024 $15$ $20$»<br>C: capítulo 5 contiene «2025 $10$ $?$» | verificado |
| `15` | ejemplo inventado | C: capítulo 5 contiene «2024 $15$ $20$»<br>C: capítulo 5 contiene «2025 $10$ $?$» | verificado |
| `20` | dato | CALC: 0.6·10 + 0.7·20, sin satélite = 20.0<br>C: capítulo 5 contiene «$0.6 \cdot 10 + 0.7 \cdot 20 = 20$» | verificado |
| `13.7` | dato | CALC: 0.6·10 + 0.7·20 − 0.42·15 = 13.7<br>C: capítulo 5 contiene «$$0.6 \cdot 10 + 0.7 \cdot 20 - 0.42 \cdot 15 = 13.7$$» | verificado |
| `6.3` | dato | CALC: 20 − 13.7 = 6.3<br>CALC: 0.7·9 = 0.42·15 = 6.3<br>C: capítulo 5 contiene «$20 - 13.7 = 6.3$» | verificado |
| `2024` | ejemplo inventado | DEF: año del ejemplo inventado del capítulo | definición (no se mide) |

### Con \(\phi=0.6\) y \(\Phi=0.7\) brotan satélites en 11 y 13 que nadie pidió

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.4230` | dato | J: cap5_sarima.json › teoricas.ar1_sar1.acf.10 = 0.423<br>R: directo_cap5.json › m4.ar1_sar1.r11 = 0.422983 | verificado |
| `0.4218` | dato | J: cap5_sarima.json › teoricas.ar1_sar1.acf.12 = 0.4218<br>R: directo_cap5.json › m4.ar1_sar1.r13 = 0.421801 | verificado |
| `0.6016` | dato | J: cap5_sarima.json › teoricas.ar1_sar1.acf.0 = 0.6016<br>R: directo_cap5.json › m4.ar1_sar1.r1 = 0.601623 | verificado |
| `0.7011` | dato | J: cap5_sarima.json › teoricas.ar1_sar1.acf.11 = 0.7011<br>R: directo_cap5.json › m4.ar1_sar1.r12 = 0.701108 | verificado |
| `0.42298` | dato | R: directo_cap5.json › m4.ar1_sar1.r11 = 0.422983 | verificado |
| `0.42180` | dato | R: directo_cap5.json › m4.ar1_sar1.r13 = 0.421801<br>R: directo_cap5.json › m4.ar1_sar1.producto = 0.421803 | verificado |
| `0.6` | parámetro | DEF: φ del capítulo | definición (no se mide) |
| `0.7` | parámetro | DEF: Φ del capítulo | definición (no se mide) |
| `animado` | gráfico animado | CALC: recursos/cap5/satelites.json es idéntico a lo que genera genera_animados_cap5.py desde J | verificado |

### La varianza se pide a la serie diferenciada, y solo se factoriza si el modelo es MA puro

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1.5217` | dato | R: directo_cap5.json › m2.factor_airline = 1.521739 | verificado |
| `0.001371` | dato | J: cap5_sarima.json › airpassengers.airline.sigma2 = 0.001371<br>R: directo_cap5.json › m2.sigma2 = 0.001371 | verificado |
| `0.002087` | dato | R: directo_cap5.json › m2.gamma0_airline = 0.002087 | verificado |
| `0.002102` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.varianza = 0.002102<br>R: directo_cap5.json › m2.var_muestral_w = 0.002102 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.n = 131<br>R: directo_cap5.json › m2.n_w = 131 | verificado |
| `0.5` | parámetro | DEF: θ₁₂ del ejemplo del capítulo | definición (no se mide) |
| `2.300` | dato | R: directo_cap5.json › m2.choque_exacta = 2.3 | verificado |
| `1.700` | dato | R: directo_cap5.json › m2.choque_factorizada = 1.7 | verificado |
| `0.00137126` | dato | R: directo_cap5.json › m2.sigma2 = 0.001371 | verificado |
| `0.6` | parámetro | R: directo_cap5.json › m2.tabla_phi.0.phi = 0.6 | verificado |
| `-0.3` | dato | R: directo_cap5.json › m2.tabla_phi.0.error_pct = -0.304286 | verificado |
| `0.8` | parámetro | R: directo_cap5.json › m2.tabla_phi.1.phi = 0.8 | verificado |
| `-9.2` | dato | R: directo_cap5.json › m2.tabla_phi.1.error_pct = -9.179175 | verificado |
| `0.9` | parámetro | R: directo_cap5.json › m2.tabla_phi.2.phi = 0.9 | verificado |
| `-33.0` | dato | R: directo_cap5.json › m2.tabla_phi.2.error_pct = -33.01337 | verificado |
| `0.95` | parámetro | R: directo_cap5.json › m2.tabla_phi.3.phi = 0.95 | verificado |
| `-54.9` | dato | R: directo_cap5.json › m2.tabla_phi.3.error_pct = -54.888663 | verificado |
| `15.406` | dato | R: directo_cap5.json › m2.tabla_phi.2.exacta = 15.405936 | verificado |
| `10.320` | dato | R: directo_cap5.json › m2.tabla_phi.2.factorizada = 10.319917 | verificado |
| `0.7` | parámetro | DEF: Φ fijo del capítulo | definición (no se mide) |
| `20000` | cálculo | DEF: número de pesos ψ que suma verifica_directo_cap5.R | definición (no se mide) |

### En un SARIMA(1,0,0)(1,0,0)\(_{12}\), ¿cuáles son ciertas? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.364` | dato | J: cap5_sarima.json › teoricas.ar1_sar1.acf.1 = 0.3637 | verificado |
| `0.3637` | dato | J: cap5_sarima.json › teoricas.ar1_sar1.acf.1 = 0.3637 | verificado |
| `0.3619` | dato | CALC: ρ₁² con ρ₁ de J = 0.361923 | verificado |
| `0.36` | dato | C: capítulo 5 (autoevaluación) contiene «0.36» | verificado |
| `0.6` | parámetro | DEF: φ | definición (no se mide) |
| `0.7` | parámetro | DEF: Φ | definición (no se mide) |

### En R el periodo va en `seasonal`, y el coeficiente de \(B^{13}\) sale del producto {columnas=3:2}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.2238` | dato | R: directo_cap5.json › m2.coef_b13 = 0.223796<br>CALC: θ·Θ con J = 0.223762 | verificado |

### \(\nabla_{12}\) resta la celda de arriba y \(\nabla\), la de la izquierda

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `fila 2022` | cuadrícula del capítulo | C: capítulo 5 contiene «2022 94 93 98 101 104 109 112 111 108 107 112 117» | verificado |
| `94` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 94 = 94 | verificado |
| `93` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 93 = 93 | verificado |
| `98` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 98 = 98 | verificado |
| `101` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 101 = 101 | verificado |
| `104` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 104 = 104 | verificado |
| `109` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 109 = 109 | verificado |
| `112` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 112 = 112 | verificado |
| `111` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 111 = 111 | verificado |
| `108` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 108 = 108 | verificado |
| `107` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 107 = 107 | verificado |
| `117` | ejemplo inventado | CALC: la fila 2022 de la tienda recalculada contiene 117 = 117 | verificado |
| `fila 2023` | cuadrícula del capítulo | C: capítulo 5 contiene «2023 106 105 110 113 116 121 124 123 120 119 124 129» | verificado |
| `106` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 106 = 106 | verificado |
| `105` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 105 = 105 | verificado |
| `110` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 110 = 110 | verificado |
| `113` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 113 = 113 | verificado |
| `116` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 116 = 116 | verificado |
| `121` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 121 = 121 | verificado |
| `124` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 124 = 124 | verificado |
| `123` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 123 = 123 | verificado |
| `120` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 120 = 120 | verificado |
| `119` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 119 = 119 | verificado |
| `129` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 129 = 129 | verificado |
| `fila 2024` | cuadrícula del capítulo | C: capítulo 5 contiene «2024 118 117 122 125 128 133 136 135 132 131 136 141» | verificado |
| `118` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 118 = 118 | verificado |
| `122` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 122 = 122 | verificado |
| `125` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 125 = 125 | verificado |
| `128` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 128 = 128 | verificado |
| `133` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 133 = 133 | verificado |
| `136` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 136 = 136 | verificado |
| `135` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 135 = 135 | verificado |
| `132` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 132 = 132 | verificado |
| `131` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 131 = 131 | verificado |
| `141` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 141 = 141 | verificado |
| `fila 2025` | cuadrícula del capítulo | C: capítulo 5 contiene «2025 130 129 134 137 140 145 148 147 144 143 148 153» | verificado |
| `130` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 130 = 130 | verificado |
| `134` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 134 = 134 | verificado |
| `137` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 137 = 137 | verificado |
| `140` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 140 = 140 | verificado |
| `145` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 145 = 145 | verificado |
| `148` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 148 = 148 | verificado |
| `147` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 147 = 147 | verificado |
| `144` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 144 = 144 | verificado |
| `143` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 143 = 143 | verificado |
| `153` | ejemplo inventado | CALC: la fila 2025 de la tienda recalculada contiene 153 = 153 | verificado |
| `100` | ejemplo inventado | C: capítulo 5 contiene «con $100$ unidades» | verificado |
| `122` | dato | CALC: marzo de 2024 (t = 27) = 122 | verificado |
| `110` | dato | CALC: marzo de 2023 (t = 15) = 110 | verificado |
| `12` | dato | CALC: ∇₁₂ en marzo de 2024 = 12<br>C: capítulo 5 contiene «$122 - 110 = 12$» | verificado |
| `2022` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |
| `2023` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |
| `2024` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |
| `2025` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |

### \(\nabla\) deja el patrón; \(\nabla_{12}\) quita patrón y tendencia; las dos, todo

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `fila 2024` | cuadrícula del capítulo | C: capítulo 5 contiene «2024 -11 -1 5 3 3 5 3 -1 -3 -1 5 5» | verificado |
| `-11` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene -11 = -11 | verificado |
| `fila 2025` | cuadrícula del capítulo | C: capítulo 5 contiene «2025 -11 -1 5 3 3 5 3 -1 -3 -1 5 5» | verificado |
| `fila 2024` | cuadrícula del capítulo | C: capítulo 5 contiene «2024 12 12 12 12 12 12 12 12 12 12 12 12» | verificado |
| `12` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 12 = 12 | verificado |
| `fila 2024` | cuadrícula del capítulo | C: capítulo 5 contiene «2024 0 0 0 0 0 0 0 0 0 0 0 0» | verificado |
| `2024` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |
| `2025` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |

### Si la tienda acelera en 2024, \(\nabla_{12}\) deja una rampa y hace falta \(\nabla\)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `fila 2023` | cuadrícula del capítulo | C: capítulo 5 contiene «2023 12 12 12 12 12 12 12 12 12 12 12 12» | verificado |
| `12` | ejemplo inventado | CALC: la fila 2023 de la tienda recalculada contiene 12 = 12 | verificado |
| `fila 2024` | cuadrícula del capítulo | C: capítulo 5 contiene «2024 14 16 18 20 22 24 26 28 30 32 34 36» | verificado |
| `14` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 14 = 14 | verificado |
| `16` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 16 = 16 | verificado |
| `18` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 18 = 18 | verificado |
| `20` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 20 = 20 | verificado |
| `22` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 22 = 22 | verificado |
| `24` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 24 = 24 | verificado |
| `26` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 26 = 26 | verificado |
| `28` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 28 = 28 | verificado |
| `30` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 30 = 30 | verificado |
| `32` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 32 = 32 | verificado |
| `34` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 34 = 34 | verificado |
| `36` | ejemplo inventado | CALC: la fila 2024 de la tienda recalculada contiene 36 = 36 | verificado |
| `fila 2024` | cuadrícula del capítulo | C: capítulo 5 contiene «2024 2 2 2 2 2 2 2 2 2 2 2 2» | verificado |
| `2023` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |
| `2024` | ejemplo inventado | DEF: año del ejemplo inventado | definición (no se mide) |
| `0.032` | dato | CALC: media de ∇₁₂ log AP en 1958 = 0.03221<br>C: capítulo 5 contiene «$0.032$ en 1958» | verificado |
| `0.201` | dato | CALC: media de ∇₁₂ log AP en 1951 = 0.200586<br>C: capítulo 5 contiene «$0.201$ en 1951» | verificado |
| `1958` | año | CALC: 1958 es el año de menor crecimiento medio | verificado |
| `1951` | año | CALC: 1951 es el de mayor crecimiento medio | verificado |
| `0.714` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D1.acf1 = 0.7137 | verificado |

### Cada operador hace su trabajo y solo el suyo

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.762` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D0.acf12 = 0.7619 | verificado |
| `0.841` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D0.acf12 = 0.8414 | verificado |
| `0.714` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D1.acf1 = 0.7137 | verificado |
| `0.002102` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.varianza = 0.002102<br>R: directo_cap5.json › m3.ap_var.3 = 0.002102 | verificado |
| `144` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D0.n = 144 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D0.n = 143 | verificado |
| `132` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D1.n = 132 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.n = 131 | verificado |
| `0.20` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D0.acf1 = 0.1998 | verificado |
| `0.71` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D1.acf1 = 0.7137 | verificado |
| `17.2` | dato | CALC: 0.194884/0.011354 = 17.164347 | verificado |
| `51.3` | dato | CALC: 0.194884/0.003800 = 51.285263 | verificado |
| `animado` | gráfico animado | CALC: recursos/cap5/diferencias.json es idéntico a lo que genera genera_animados_cap5.py desde J | verificado |

### `ndiffs()` da 0 en la serie cruda y 1 tras \(\nabla_{12}\): ¿qué significa? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.8672` | dato | PY: directo_python_cap5.json › kpss_uad_D1 = 0.867204 | verificado |
| `0.463` | dato | PY: directo_python_cap5.json › kpss_critico_5 = 0.463 | verificado |
| `0.0713` | dato | PY: directo_python_cap5.json › kpss_uad_d1D1 = 0.071324 | verificado |
| `5` | convención | DEF: nivel de la prueba | definición (no se mide) |
| `-0.4303` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.0.valor = -0.4303<br>PY: directo_python_cap5.json › uad_simple.ma1 = -0.430274 | verificado |
| `1973` | dato | R: directo_cap5.json › datos.uad_inicio = 1973 | verificado |
| `1978` | dato | R: directo_cap5.json › datos.uad_fin = 1978 | verificado |
| `72` | dato | R: directo_cap5.json › datos.uad_n = 72 | verificado |

### Los operadores conmutan: \(\nabla\nabla_{12}y_t\) es la misma serie en cualquier orden {columnas=3:2}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `128` | dato | CALC: tienda que acelera, t = 27 = 128<br>C: capítulo 5 contiene «$128 - 121 - 110 + 105 = 2$» | verificado |
| `121` | dato | CALC: tienda que acelera, t = 26 = 121<br>C: capítulo 5 contiene «$128 - 121 - 110 + 105 = 2$» | verificado |
| `110` | dato | CALC: tienda que acelera, t = 15 = 110<br>C: capítulo 5 contiene «$128 - 121 - 110 + 105 = 2$» | verificado |
| `105` | dato | CALC: tienda que acelera, t = 14 = 105<br>C: capítulo 5 contiene «$128 - 121 - 110 + 105 = 2$» | verificado |

### Diferenciar de más deja la firma del capítulo 4: \(\hat\Theta\) se acerca a −1

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `143` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.0.n = 143 | verificado |
| `0.011354` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.0.varianza = 0.011354 | verificado |
| `0.7397` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.0.theta_est = 0.7397 | verificado |
| `0.0610` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.0.ee = 0.061 | verificado |
| `0.9752` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.0.raiz_ma = 0.9752 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.1.n = 131 | verificado |
| `0.002102` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.1.varianza = 0.002102 | verificado |
| `-0.5569` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.1.theta_est = -0.5569 | verificado |
| `0.0731` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.1.ee = 0.0731 | verificado |
| `0.9524` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.1.raiz_ma = 0.9524 | verificado |
| `119` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.2.n = 119 | verificado |
| `0.005960` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.2.varianza = 0.00596 | verificado |
| `-0.9973` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.2.theta_est = -0.9973 | verificado |
| `0.0830` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.2.ee = 0.083 | verificado |
| `0.9998` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.2.raiz_ma = 0.9998 | verificado |
| `58` | capítulo (lynx, del capítulo 4) | C: capítulo 5 contiene «58» | verificado |

### `nsdiffs()` cambió de prueba por defecto: `seas` y `ocsb` no dan lo mismo

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `8.3` | documentación | DOC: docs_cap5.json › news_cambio_D.version = 8.3<br>DOC: formals(nsdiffs)$test empieza por "seas" | verificado |
| `tabla` | tabla (enteros < 10) | J: las 16 celdas de la tabla = orden_pruebas de J | verificado |
| `9.0.2` | versión | DOC: docs_cap5.json › entorno.forecast | verificado |
| `ocsb` | documentación | DOC: docs_cap5.json › nsdiffs contiene «Osborn-Chui-Smith-Birchenhall (1988) test» | verificado |
| `seas` | documentación | DOC: docs_cap5.json › nsdiffs contiene «a measure of seasonal strength is used»<br>C: capítulo 5 contiene «fuerza estacional de la descomposición STL» | verificado |

### Los rezagos estacionales se leen con la misma tabla del capítulo 3

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.700` | dato | J: cap5_sarima.json › teoricas.sar1_pos.acf.11 = 0.7<br>R: directo_cap5.json › m4.sar1.r12 = 0.7 | verificado |
| `0.490` | dato | J: cap5_sarima.json › teoricas.sar1_pos.acf.23 = 0.49<br>R: directo_cap5.json › m4.sar1.r24 = 0.49 | verificado |
| `0.343` | dato | J: cap5_sarima.json › teoricas.sar1_pos.acf.35 = 0.343<br>R: directo_cap5.json › m4.sar1.r36 = 0.343 | verificado |
| `-0.4412` | dato | J: cap5_sarima.json › teoricas.sma1.acf.11 = -0.4412<br>R: directo_cap5.json › m4.sma1.r12 = -0.441176 | verificado |
| `0.7` | parámetro | DEF: Φ | definición (no se mide) |
| `-0.6` | parámetro | DEF: Θ | definición (no se mide) |

### En el *airline*, el producto es exacto; con parte AR solo se parece

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.602` | dato | R: directo_cap5.json › m4.ar1_sar1.r1 = 0.601623 | verificado |
| `0.423` | dato | R: directo_cap5.json › m4.ar1_sar1.r11 = 0.422983 | verificado |
| `0.701` | dato | R: directo_cap5.json › m4.ar1_sar1.r12 = 0.701108 | verificado |
| `0.422` | dato | R: directo_cap5.json › m4.ar1_sar1.r13 = 0.421801 | verificado |
| `0.491` | dato | R: directo_cap5.json › m4.ar1_sar1.r24 = 0.490778 | verificado |
| `-0.346` | dato | R: directo_cap5.json › m4.airline.r1 = -0.345967 | verificado |
| `0.147` | dato | R: directo_cap5.json › m4.airline.r11 = 0.147066 | verificado |
| `-0.425` | dato | R: directo_cap5.json › m4.airline.r12 = -0.425088 | verificado |
| `0.147` | dato | R: directo_cap5.json › m4.airline.r13 = 0.147066 | verificado |
| `0.500` | dato | R: directo_cap5.json › m4.ar1_sma1.r1 = 0.499828 | verificado |
| `-0.234` | dato | R: directo_cap5.json › m4.ar1_sma1.r11 = -0.234465 | verificado |
| `-0.470` | dato | R: directo_cap5.json › m4.ar1_sma1.r12 = -0.469662 | verificado |
| `-0.235` | dato | R: directo_cap5.json › m4.ar1_sma1.r13 = -0.234831 | verificado |
| `0.4018` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.valor = 0.4018 | verificado |
| `-0.4018` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.valor = -0.4018 | verificado |
| `-0.5569` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.valor = -0.5569 | verificado |
| `0.42298` | dato | R: directo_cap5.json › m4.ar1_sar1.r11 = 0.422983 | verificado |
| `0.42180` | dato | R: directo_cap5.json › m4.ar1_sar1.r13 = 0.421801 | verificado |
| `-0.23446` | dato | R: directo_cap5.json › m4.ar1_sma1.r11 = -0.234465 | verificado |
| `-0.23483` | dato | R: directo_cap5.json › m4.ar1_sma1.r13 = -0.234831 | verificado |
| `-0.234` | capítulo | C: capítulo 5 contiene «{-0.234}» | verificado |
| `0.14707` | dato | R: directo_cap5.json › m4.airline.r11 = 0.147066 | verificado |
| `0.14705` | dato | R: directo_cap5.json › m4.airline_redondeado.r11 = 0.147052<br>C: capítulo 5 contiene «0.14705» | verificado |
| `1.96` | convención | DEF: cuantil 0.975 de la normal | definición (no se mide) |
| `0.1471` | dato | R: directo_cap5.json › m4.airline.producto = 0.147066 | verificado |
| `0.6` | parámetro | DEF: φ | definición (no se mide) |
| `0.7` | parámetro | DEF: Φ | definición (no se mide) |
| `0.5` | parámetro | DEF: φ | definición (no se mide) |
| `-0.7` | parámetro | DEF: Θ | definición (no se mide) |

### Picos de 0.80, 0.64 y 0.51 en 12, 24 y 36, y cero en lo demás: ¿qué modelo es? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.80` | definición | CALC: Φ^1 con Φ = 0.8: ACF de un SAR(1) en 12·1 = 0.8 | verificado |
| `0.64` | definición | CALC: Φ^2 con Φ = 0.8: ACF de un SAR(1) en 12·2 = 0.64 | verificado |
| `0.51` | definición | CALC: Φ^3 con Φ = 0.8: ACF de un SAR(1) en 12·3 = 0.512 | verificado |
| `0.512` | definición | CALC: Φ^3 con Φ = 0.8: ACF de un SAR(1) en 12·3 = 0.512 | verificado |
| `0.8` | parámetro | DEF: Φ = 0.8, elegido para no repetir el 0.7 del Módulo 2 | definición (no se mide) |
| `0.7` | parámetro | DEF: Φ = 0.7 del material | definición (no se mide) |

### El *airline*: dos diferencias y dos MA para una serie con tendencia y estación

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `Box & Jenkins airline` | documentación | DOC: docs_cap5.json › airpassengers contiene «The classic Box & Jenkins airline data» | verificado |
| `airline model` | documentación | DOC: docs_cap5.json › airpassengers contiene «The classic 'airline model'» | verificado |
| `log10` | documentación | DOC: docs_cap5.json › airpassengers contiene «log10(AirPassengers)» | verificado |

### Dos series sin nada en común eligen el mismo modelo y casi los mismos coeficientes

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `144` | dato | J: cap5_sarima.json › airpassengers.n = 144 | verificado |
| `72` | dato | J: cap5_sarima.json › usaccdeaths.n = 72 | verificado |
| `-0.4018` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.valor = -0.4018 | verificado |
| `-0.5569` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.valor = -0.5569 | verificado |
| `-0.4303` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.0.valor = -0.4303 | verificado |
| `-0.5528` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.1.valor = -0.5528 | verificado |
| `auto` | modelo | J: auto.arima exhaustivo = airline en las dos | verificado |
| `1949` | dato | R: directo_cap5.json › datos.ap_inicio = 1949 | verificado |
| `1960` | dato | R: directo_cap5.json › datos.ap_fin = 1960 | verificado |
| `1973` | dato | R: directo_cap5.json › datos.uad_inicio = 1973 | verificado |
| `1978` | dato | R: directo_cap5.json › datos.uad_fin = 1978 | verificado |

### Los pesos \(\psi\) suben en escalones: la incertidumbre salta al cruzar el rezago 12

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.5982` | dato | J: cap5_sarima.json › airpassengers.pronostico.psi.1 = 0.598172<br>CALC: 1 + θ̂ (R) = 0.598172 | verificado |
| `1.0412` | dato | J: cap5_sarima.json › airpassengers.pronostico.psi.12 = 1.041227 | verificado |
| `0.8632` | dato | J: cap5_sarima.json › airpassengers.pronostico.psi.13 = 0.863195 | verificado |
| `0.0370` | dato | J: cap5_sarima.json › airpassengers.pronostico.sigma_h.0 = 0.037031 | verificado |
| `0.0823` | dato | J: cap5_sarima.json › airpassengers.pronostico.sigma_h.11 = 0.08227 | verificado |
| `0.1396` | dato | J: cap5_sarima.json › airpassengers.pronostico.sigma_h.23 = 0.139621 | verificado |
| `1.0413` | dato | CALC: ψ₁₂ = 2 + θ + Θ con los coeficientes redondeados = 1.0413<br>C: capítulo 5 contiene «1.0413» | verificado |
| `0.8633` | dato | CALC: ψ₁₃ = 2 + 2θ + Θ + θΘ, redondeados = 0.863262<br>C: capítulo 5 contiene «0.8633» | verificado |
| `animado` | gráfico animado | CALC: recursos/cap5/escalones.json es idéntico a lo que genera genera_animados_cap5.py desde J | verificado |

### El *airline* acumula incertidumbre más despacio que una sola caminata aleatoria

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `2.22` | dato | CALC: σ₁₂/σ₁ (J) = 2.221652 | verificado |
| `3.46` | dato | CALC: √12 = 3.464102 | verificado |
| `0.082270` | dato | J: cap5_sarima.json › airpassengers.pronostico.sigma_h.11 = 0.08227 | verificado |
| `0.037031` | dato | J: cap5_sarima.json › airpassengers.pronostico.sigma_h.0 = 0.037031 | verificado |
| `3.4641` | dato | CALC: √12 = 3.464102 | verificado |
| `0.169` | dato | J4: cap4_arima.json › nilo.intervalos.psi_limite = 0.1688 | verificado |

### Un *airline* sobre 96 meses: ¿cuántas observaciones quedan tras las dos diferencias? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `96` | enunciado | DEF: enunciado de la pregunta 3 | definición (no se mide) |
| `83` | dato | CALC: 96 − 1 − 12 = 83<br>C: capítulo 5 contiene «83» | verificado |

### Para la próxima clase {columnas=1:1 .arriba}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `36` | dato | CALC: número de modelos de la rejilla (J) = 36<br>CALC: 3 × 3 × 2 × 2 = 36 | verificado |

### Lo que dejó la clase 1: dos parámetros en el rezago 12 corrigen lo que cinco MA no

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.0515` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.11 = -0.0515 | verificado |
| `0.7245` | dato | J4: cap4_arima.json › puente_estacional.no_estacional.acf_12 = 0.7245 | verificado |

### Dos hábitos nuevos: el AICc no se compara entre distintos \(D\), y Ljung–⁠Box con \(2m\)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `143` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.0.n = 143 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.1.n = 131 | verificado |
| `24` | convención | CALC: 2m con m = 12 = 24 | verificado |
| `20` | convención | DEF: rezagos del ejemplo del capítulo | definición (no se mide) |
| `10` | convención | DEF: rezagos del ejemplo del capítulo | definición (no se mide) |

### En la rejilla de 36 modelos, el *airline* gana por AICc y por BIC

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-483.21` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(0,1,1)[12].aicc = -483.2101 | verificado |
| `-474.77` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(0,1,1)[12].bic = -474.7735 | verificado |
| `0.2330` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(0,1,1)[12].lb_p = 0.233 | verificado |
| `-0.0515` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(0,1,1)[12].acf12 = -0.0515 | verificado |
| `-481.79` | dato | J: cap5_sarima.json › airpassengers.rejilla.(2,1,1)(0,1,1)[12].aicc = -481.7923 | verificado |
| `-467.90` | dato | J: cap5_sarima.json › airpassengers.rejilla.(2,1,1)(0,1,1)[12].bic = -467.8963 | verificado |
| `0.1371` | dato | J: cap5_sarima.json › airpassengers.rejilla.(2,1,1)(0,1,1)[12].lb_p = 0.1371 | verificado |
| `-0.0307` | dato | J: cap5_sarima.json › airpassengers.rejilla.(2,1,1)(0,1,1)[12].acf12 = -0.0307 | verificado |
| `-481.60` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(1,1,1)[12].aicc = -481.5957 | verificado |
| `-470.41` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(1,1,1)[12].bic = -470.4123 | verificado |
| `0.2271` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(1,1,1)[12].lb_p = 0.2271 | verificado |
| `-0.0163` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,1)(1,1,1)[12].acf12 = -0.0163 | verificado |
| `-481.58` | dato | J: cap5_sarima.json › airpassengers.rejilla.(1,1,1)(0,1,1)[12].aicc = -481.582 | verificado |
| `-470.40` | dato | J: cap5_sarima.json › airpassengers.rejilla.(1,1,1)(0,1,1)[12].bic = -470.3987 | verificado |
| `0.2453` | dato | J: cap5_sarima.json › airpassengers.rejilla.(1,1,1)(0,1,1)[12].lb_p = 0.2453 | verificado |
| `-0.0459` | dato | J: cap5_sarima.json › airpassengers.rejilla.(1,1,1)(0,1,1)[12].acf12 = -0.0459 | verificado |
| `-434.80` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,0)(0,1,0)[12].aicc = -434.799 | verificado |
| `-431.95` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,0)(0,1,0)[12].bic = -431.9548 | verificado |
| `-0.3907` | dato | J: cap5_sarima.json › airpassengers.rejilla.(0,1,0)(0,1,0)[12].acf12 = -0.3907 | verificado |
| `0.0001` | cota | J: LB p del (0,1,0)(0,1,0) < 0.0001 | verificado |
| `36` | dato | CALC: modelos en la rejilla = 36 | verificado |
| `131` | dato | J: nobs = 131 en los 36 | verificado |
| `1.7` («a menos de 1.7»: 1.63) | dato | CALC: distancia del 4.º al 1.º = 1.6281 | verificado |
| `1.63` | dato | CALC: −481.582 − (−483.210) = 1.6281 | verificado |
| `144` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.n_residuales = 144 | verificado |

### statsmodels no diferencia la serie: sus AIC parecen comparables, pero no lo son

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `144` | dato | PY: directo_python_cap5.json › ap_difuso.nobs = 144 | verificado |
| `131` | dato | PY: directo_python_cap5.json › ap_simple.nobs = 131<br>J: cap5_sarima.json › airpassengers.airline.nobs = 131 | verificado |
| `72` | dato | J: cap5_sarima.json › usaccdeaths.n = 72 | verificado |
| `-0.4303` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.0.valor = -0.4303<br>PY: directo_python_cap5.json › uad_simple.ma1 = -0.430274 | verificado |
| `-0.3924` | dato | PY: directo_python_cap5.json › uad_difuso.ma1 = -0.392397 | verificado |
| `-0.5475` | dato | PY: directo_python_cap5.json › uad_difuso.sma1 = -0.547514 | verificado |
| `-0.5527` | dato | PY: directo_python_cap5.json › uad_simple.sma1 = -0.55272 | verificado |
| `-0.5528` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.1.valor = -0.5528 | verificado |
| `2.4` | dato | CALC: diferencia máxima × 10⁴ (PY) = 2.438557 | verificado |

### Etapas 1 a 3: logaritmo, después \(D=1\) y, sobre la serie sin estación, \(d=1\)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `etapas` | capítulo | C: capítulo 5 contiene «Etapas 2 y 3 · $D$ y luego $d$»<br>C: capítulo 5 contiene «Etapa 5 · Estimación y diagnóstico»<br>C: el capítulo ya no numera «Paso 0…4» | verificado |
| `1.848` | dato | R: directo_cap5.json › m7.rango_relativo = 1.848029<br>C: capítulo 5 contiene «1.848» | verificado |
| `0.762` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.11 = 0.7619 | verificado |
| `0.520` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.23 (empate: decide el exacto) = 0.5205<br>CALC: ACF exacta en 24 = 0.52049 | verificado |
| `0.520` | capítulo | C: capítulo 5 contiene «\hat\rho_{24}=0.520$» | verificado |
| `0.52049` | dato | CALC: ACF exacta en 24 = 0.52049 | verificado |
| `0.319` | dato | J: cap5_sarima.json › airpassengers.firma.airpassengers_log.acf.35 = 0.3193 | verificado |
| `0.714` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D1.acf1 = 0.7137 | verificado |
| `0.002102` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.varianza = 0.002102 | verificado |
| `0.003800` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d0_D1.varianza = 0.0038 | verificado |
| `0.011354` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D0.varianza = 0.011354 | verificado |
| `622` | dato | CALC: máximo de AirPassengers = 622 | verificado |
| `104` | dato | CALC: mínimo de AirPassengers = 104 | verificado |
| `280.30` | dato | CALC: media de AirPassengers = 280.298611 | verificado |
| `1949` | dato | R: directo_cap5.json › datos.ap_inicio = 1949 | verificado |
| `1960` | dato | R: directo_cap5.json › datos.ap_fin = 1960 | verificado |

### Etapa 4: un pico en 1 y otro en 12 piden \(q=1\) y \(Q=1\)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.341` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf1 = -0.3411<br>R: directo_cap5.json › m7.r1 = -0.341124 | verificado |
| `-0.387` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf12 = -0.3866<br>R: directo_cap5.json › m7.r12 = -0.386613 | verificado |
| `0.171` | dato | R: directo_cap5.json › m7.banda_w = 0.171246 | verificado |
| `0.1712` | dato | R: directo_cap5.json › m7.banda_w = 0.171246 | verificado |
| `131` | dato | R: directo_cap5.json › m7.n_w = 131 | verificado |
| `144` | dato | R: directo_cap5.json › datos.ap_n = 144 | verificado |
| `-0.202` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.2 = -0.2021<br>R: directo_cap5.json › m7.r3 = -0.202139 | verificado |
| `0.176` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.8 = 0.1764<br>R: directo_cap5.json › m7.r9 = 0.176369 | verificado |
| `0.223` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.22 = 0.2233<br>R: directo_cap5.json › m7.r23 = 0.223269 | verificado |
| `95` | convención | DEF: nivel de la banda | definición (no se mide) |
| `24` | convención | DEF: rezagos mirados | definición (no se mide) |
| `1.96` | convención | DEF: cuantil 0.975 de la normal | definición (no se mide) |

### En 11 y 13 aparecen 0.064 y 0.152: ¿se añaden parámetros? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.064` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.10 = 0.0644<br>R: directo_cap5.json › m7.r11 = 0.064384 | verificado |
| `0.152` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.12 = 0.1516<br>R: directo_cap5.json › m7.r13 = 0.151602 | verificado |
| `0.171` | dato | R: directo_cap5.json › m7.banda_w = 0.171246 | verificado |
| `0.0644` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.10 = 0.0644 | verificado |
| `0.1516` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.12 = 0.1516 | verificado |
| `0.06438` | dato | R: directo_cap5.json › m7.r11 = 0.064384 | verificado |
| `0.15160` | dato | R: directo_cap5.json › m7.r13 = 0.151602 | verificado |

### Etapa 5: los dos coeficientes son significativos y el diagnóstico pasa

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.4018` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.valor = -0.4018 | verificado |
| `0.0896` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.ee = 0.0896<br>R: directo_cap5.json › m7.ee.0 = 0.089644 | verificado |
| `-4.48` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.t = -4.482<br>R: directo_cap5.json › m7.t.0 = -4.482499 | verificado |
| `-0.5569` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.valor = -0.5569 | verificado |
| `0.0731` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.ee = 0.0731<br>R: directo_cap5.json › m7.ee.1 = 0.0731 | verificado |
| `-7.62` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.t = -7.619<br>R: directo_cap5.json › m7.t.1 = -7.618985 | verificado |
| `0.2330` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.lb24_p = 0.233<br>R: directo_cap5.json › m7.lb24 = 0.233033 | verificado |
| `0.2969` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.lb36_p = 0.2969<br>R: directo_cap5.json › m7.lb36 = 0.296923 | verificado |
| `0.1674` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.shapiro_p = 0.1674<br>R: directo_cap5.json › m7.shapiro = 0.16743 | verificado |
| `-0.0515` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.11 = -0.0515<br>R: directo_cap5.json › m7.res_r12 = -0.051463 | verificado |
| `0.0124` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.23 = 0.0124<br>R: directo_cap5.json › m7.res_r24 = 0.012364 | verificado |
| `0.163` | dato | R: directo_cap5.json › m7.banda_res = 0.163333 | verificado |
| `0.9524` | dato | J: cap5_sarima.json › airpassengers.airline.raices.ma_max = 0.9524<br>R: directo_cap5.json › m7.raiz_ma = 0.952396 | verificado |
| `0.001371` | dato | J: cap5_sarima.json › airpassengers.airline.sigma2 = 0.001371 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.airline.nobs = 131 | verificado |
| `-0.9973` | dato | J: cap5_sarima.json › airpassengers.sobrediferenciacion_estacional.2.theta_est = -0.9973 | verificado |
| `0.5569` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.valor = 0.5569 | verificado |
| `0.9524 = Θ^(1/12)` | cálculo | CALC: |Θ̂|^(1/12) = módulo inverso máximo de J (a 10⁻⁴) | verificado |
| `0.825` | dato | CALC: 0.1^(1/12) = 0.825404 | verificado |
| `0.1` | parámetro | DEF: Θ del ejemplo | definición (no se mide) |
| `-0.557` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.valor = -0.5569 | verificado |
| `0.073` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.ee = 0.0731 | verificado |
| `capítulo` | capítulo | C: capítulo 5 contiene «es $|\hat\Theta|^{1/12} = 0.5569^{1/12}$»<br>C: el capítulo ya no dice «aunque justo» | verificado |

### En los residuales solo el rezago 23 sale de la banda, y Ljung–⁠Box no rechaza

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.125` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.2 = -0.1254<br>R: directo_cap5.json › m7.res_r3 = -0.125418 | verificado |
| `0.117` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.8 = 0.1166<br>R: directo_cap5.json › m7.res_r9 = 0.116585 | verificado |
| `0.220` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.22 = 0.2196<br>R: directo_cap5.json › m7.res_r23 = 0.219622 | verificado |
| `0.163` | dato | R: directo_cap5.json › m7.banda_res = 0.163333 | verificado |
| `0.1633` | dato | R: directo_cap5.json › m7.banda_res = 0.163333 | verificado |
| `1.96` | convención | DEF: cuantil 0.975 de la normal | definición (no se mide) |
| `0.233` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.lb24_p = 0.233 | verificado |
| `144` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.n_residuales = 144 | verificado |
| `-0.157` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.acf.15 = -0.1573 | verificado |
| `0.171` | dato | R: directo_cap5.json › m7.banda_w = 0.171246 | verificado |
| `131` | dato | R: directo_cap5.json › m7.n_w = 131 | verificado |
| `solo el 23` | dato | R: directo_cap5.json › m7.res_fuera_131 = 23 (con la banda de 131) | verificado |

### Los satélites, comprobados: el modelo predice 0.1471 y la muestra da 0.064 y 0.152

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.1471` | dato | R: directo_cap5.json › m4.airline.producto = 0.147066<br>J: cap5_sarima.json › teoricas.ma1_sma1.acf.10 = 0.1471 | verificado |
| `0.064` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.10 = 0.0644 | verificado |
| `0.152` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf.12 = 0.1516 | verificado |
| `-0.3460` | dato | R: directo_cap5.json › m4.airline.r1 = -0.345967 | verificado |
| `-0.341` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf1 = -0.3411 | verificado |
| `-0.4251` | dato | R: directo_cap5.json › m4.airline.r12 = -0.425088<br>J: cap5_sarima.json › teoricas.ma1_sma1.acf.11 = -0.4251 | verificado |
| `-0.387` | dato | J: cap5_sarima.json › airpassengers.combinaciones.d1_D1.acf12 = -0.3866 | verificado |
| `131` | dato | R: directo_cap5.json › m7.n_w = 131 | verificado |
| `0.087` | dato | R: directo_cap5.json › m7.ee_aprox = 0.08737 | verificado |
| `0.0874` | dato | R: directo_cap5.json › m7.ee_aprox = 0.08737 | verificado |
| `-0.34597` | dato | R: directo_cap5.json › m4.airline.r1 = -0.345967 | verificado |
| `-0.42509` | dato | R: directo_cap5.json › m4.airline.r12 = -0.425088 | verificado |
| `0.14707` | dato | R: directo_cap5.json › m4.airline.r11 = 0.147066 | verificado |
| `-0.3459` | dato | J: cap5_sarima.json › teoricas.ma1_sma1.acf.0 = -0.3459 | verificado |

### El exp() del pronóstico en logaritmos es la mediana, y el intervalo no es simétrico

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `525.46` | dato | J: cap5_sarima.json › airpassengers.pronostico.original.media.23 = 525.46<br>R: directo_cap5.json › m7.pron24.0 = 525.460045 | verificado |
| `399.66` | dato | J: cap5_sarima.json › airpassengers.pronostico.original.lo95.23 = 399.66<br>R: directo_cap5.json › m7.pron24.1 = 399.662821 | verificado |
| `690.85` | dato | J: cap5_sarima.json › airpassengers.pronostico.original.hi95.23 = 690.85<br>R: directo_cap5.json › m7.pron24.2 = 690.853002 | verificado |
| `126` | dato | CALC: 525.46 − 399.66 = 125.8 | verificado |
| `165` | dato | CALC: 690.85 − 525.46 = 165.39 | verificado |
| `125.80` | dato | CALC: 525.46 − 399.66 = 125.8 | verificado |
| `165.39` | dato | CALC: 690.85 − 525.46 = 165.39 | verificado |
| `530.52` | capítulo (statsmodels) | C: capítulo 5 contiene «530.52» | verificado |
| `530.61` | dato | R: directo_cap5.json › m7.media24 = 530.606782 | verificado |
| `95` | convención | DEF: nivel del intervalo | definición (no se mide) |
| `80` | convención | DEF: nivel del intervalo | definición (no se mide) |
| `24` | dato | J: cap5_sarima.json › horizonte = 24 | verificado |
| `1960` | fecha | J: el pronóstico empieza en 1961-01 | verificado |
| `1962` | fecha | J: el horizonte 24 es 1962-12 | verificado |

### El caso completo cabe en seis líneas de R

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `26.446` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.lb24_Q = 26.4458 | verificado |
| `24` | convención | DEF: rezagos de Ljung–Box | definición (no se mide) |
| `22` | dato | CALC: 24 − 2 = 22 | verificado |

### USAccDeaths vuelve a elegir el *airline*, con errores estándar 1.4 y 2.4 veces mayores

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.4303` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.0.valor = -0.4303 | verificado |
| `0.1228` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.0.ee = 0.1228 | verificado |
| `-0.5528` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.1.valor = -0.5528 | verificado |
| `0.1784` | dato | J: cap5_sarima.json › usaccdeaths.coeficientes.1.ee = 0.1784 | verificado |
| `857.32` | dato | J: cap5_sarima.json › usaccdeaths.aicc = 857.3164 | verificado |
| `0.2477` | dato | J: cap5_sarima.json › usaccdeaths.diagnostico.lb24_p = 0.2477 | verificado |
| `72` | dato | J: cap5_sarima.json › usaccdeaths.n = 72 | verificado |
| `144` | dato | J: cap5_sarima.json › airpassengers.n = 144 | verificado |
| `0.0896` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.0.ee = 0.0896 | verificado |
| `0.0731` | dato | J: cap5_sarima.json › airpassengers.airline.coeficientes.1.ee = 0.0731 | verificado |
| `1.4` | dato | CALC: 0.1228/0.0896 = 1.370536 | verificado |
| `2.4` | dato | CALC: 0.1784/0.0731 = 2.440492 | verificado |
| `1.37` | dato | CALC: 0.1228/0.0896 = 1.370536 | verificado |
| `2.44` | dato | CALC: 0.1784/0.0731 = 2.440492 | verificado |
| `59` | dato | CALC: 72 − 1 − 12 = 59 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.airline.nobs = 131 | verificado |
| `1.49` | dato | CALC: √(131/59) = 1.49008 | verificado |
| `capítulo` | capítulo | C: capítulo 5 contiene «entre $1.4$ y $2.4$ veces mayores» | verificado |

### La TRM es mensual y no tiene estacionalidad: cuatro evidencias coinciden

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.0025` | dato | J: cap5_sarima.json › trm_contraejemplo.acf12 = -0.0025 | verificado |
| `-0.002` | dato | CALC: ACF exacta de ∇TRM en 12 = -0.002453<br>J: cap5_sarima.json › airpassengers.firma.trm_diff.acf.11 (empate: decide el exacto) = -0.0025 | verificado |
| `-0.00245` | dato | CALC: ACF exacta de ∇TRM en 12 = -0.002453 | verificado |
| `-0.067` | dato | J: cap5_sarima.json › trm_contraejemplo.acf24 = -0.0672<br>CALC: ∇TRM, 24 = -0.067215 | verificado |
| `0.071` | dato | J: cap5_sarima.json › trm_contraejemplo.acf36 = 0.0714<br>CALC: ∇TRM, 36 = 0.071383 | verificado |
| `0,1,0` | modelo | J: el modelo simple es la caminata aleatoria | verificado |
| `-0.0672` | dato | J: cap5_sarima.json › trm_contraejemplo.acf24 = -0.0672<br>CALC: ∇TRM, 24 = -0.067215 | verificado |
| `0.0714` | dato | J: cap5_sarima.json › trm_contraejemplo.acf36 = 0.0714<br>CALC: ∇TRM, 36 = 0.071383 | verificado |
| `0.167` | dato | CALC: 1.96/√137 = 0.167454 | verificado |
| `0.16745` | dato | CALC: 1.96/√137 = 0.167454 | verificado |
| `0.1675` | dato | J: cap5_sarima.json › trm_contraejemplo.banda = 0.1675 | verificado |
| `0.0013` | dato | J: cap5_sarima.json › trm_contraejemplo.forzado.Phi = 0.0013 | verificado |
| `0.0899` | dato | J: cap5_sarima.json › trm_contraejemplo.forzado.ee = 0.0899 | verificado |
| `0.01` | dato | CALC: t = 0.0147 que imprime el código del capítulo = 0.0147<br>C: capítulo 5 contiene «0.0147» | verificado |
| `1708.00` | dato | J: cap5_sarima.json › trm_contraejemplo.forzado.aicc = 1708.001 | verificado |
| `1705.94` | dato | J: cap5_sarima.json › trm_contraejemplo.simple.aicc = 1705.941 | verificado |
| `nsdiffs` | dato | J: nsdiffs = 0 con seas y con ocsb | verificado |
| `2015` | dato | R: trm_inicio | verificado |
| `2026` | dato | R: trm_fin | verificado |
| `138` | dato | J: cap5_sarima.json › trm_contraejemplo.n = 138 | verificado |
| `137` | dato | J: cap5_sarima.json › airpassengers.firma.trm_diff.n = 137 | verificado |
| `1.96` | convención | DEF: cuantil 0.975 de la normal | definición (no se mide) |
| `auto` | modelo | J: auto.arima = ARIMA(0,1,0) | verificado |

### El SARIMA no ve lo que el calendario cambia de sitio de un año a otro

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `28` | calendario | DEF: días de febrero (calendario) | definición (no se mide) |
| `29` | calendario | DEF: días de febrero bisiesto | definición (no se mide) |
| `31` | calendario | DEF: días de julio | definición (no se mide) |
| `22` | calendario | DEF: ejemplo del capítulo | definición (no se mide) |
| `23` | calendario | DEF: ejemplo del capítulo | definición (no se mide) |
| `rango` | dato | J: rango de días del mes en la serie: 28 a 31 | verificado |

### Los días del mes entran con \(\hat\beta=1.084\), compatible con la aritmética

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1.084` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.2.valor = 1.084<br>R: directo_cap5.json › m9.beta_dias = 1.083962 | verificado |
| `-483.21` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.sin_regresores.aicc = -483.2101 | verificado |
| `-474.77` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.sin_regresores.bic = -474.7735 | verificado |
| `-486.54` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias.aicc = -486.538 | verificado |
| `-475.35` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias.bic = -475.3547 | verificado |
| `1.1157` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias.coeficientes.2.valor = 1.1157 | verificado |
| `2.39` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias.coeficientes.2.t = 2.386 | verificado |
| `-490.72` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.aicc = -490.7221 | verificado |
| `-476.83` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.bic = -476.8261 | verificado |
| `1.0840` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.2.valor = 1.084 | verificado |
| `2.43` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.2.t = 2.429 | verificado |
| `0.0290` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.3.valor = 0.029 | verificado |
| `2.60` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.3.t = 2.603 | verificado |
| `2.9` | dato | R: directo_cap5.json › m9.pascua_pct = 2.942731<br>J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.3.valor = 2.9 | verificado |
| `2.94` | dato | R: directo_cap5.json › m9.pascua_pct = 2.942731 | verificado |
| `12` | dato | CALC: años con Pascua en la serie = 12 | verificado |
| `10` | dato | R: directo_cap5.json › m9.pascuas_abril = 10 | verificado |
| `10.7` | dato | J: cap5_sarima.json › airpassengers.calendario.variacion_pct = 10.7<br>R: directo_cap5.json › m9.variacion_dias_pct = 10.714286 | verificado |
| `31` | dato | DEF: días | definición (no se mide) |
| `28` | dato | DEF: días | definición (no se mide) |

### ¿Cuánto vale el \(t\) de \(H_0:\beta=1\)? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1.0840` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.2.valor = 1.084 | verificado |
| `0.4462` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.coeficientes.2.ee = 0.4462<br>R: directo_cap5.json › m9.ee_dias = 0.446239 | verificado |
| `0.188` | dato | R: directo_cap5.json › m9.t_beta1 = 0.188155<br>CALC: (1.0840 − 1)/0.4462 = 0.188256 | verificado |
| `0.1883` | dato | CALC: (1.0840 − 1)/0.4462 = 0.188256<br>C: capítulo 5 (autoevaluación) contiene «0.1883» | verificado |
| `0.1882` | dato | R: directo_cap5.json › m9.t_beta1 = 0.188155 | verificado |
| `0.18816` | dato | R: directo_cap5.json › m9.t_beta1 = 0.188155 | verificado |
| `0.18826` | dato | CALC: (1.0840 − 1)/0.4462 = 0.188256 | verificado |
| `0.21` | dato | CALC: 1.0840 − 1.96 × 0.4462 = 0.209448 | verificado |
| `1.96` | dato | CALC: 1.0840 + 1.96 × 0.4462 (el límite superior coincide con el cuantil) = 1.958552 | verificado |
| `0.2094` | dato | CALC: límite inferior = 0.209448 | verificado |
| `1.9586` | dato | CALC: límite superior = 1.958552 | verificado |
| `95` | convención | DEF: nivel del intervalo | definición (no se mide) |

### Ganar 7.5 puntos de AICc no es pronosticar mejor

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `7.5` | dato | R: directo_cap5.json › m9.delta_aicc = 7.512012<br>CALC: J = 7.512 | verificado |
| `7.51` | dato | R: directo_cap5.json › m9.delta_aicc = 7.512012 | verificado |
| `45.48` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima_calendario.rmse = 45.477 | verificado |
| `43.18` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima.rmse = 43.184 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.airline.nobs = 131 | verificado |
| `24` | dato | J: cap5_sarima.json › airpassengers.comparativa.n_prueba = 24 | verificado |
| `1958` | fecha | J: corte = 1958-12 | verificado |
| `-483.21` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.sin_regresores.aicc = -483.2101 | verificado |
| `-490.72` | dato | J: cap5_sarima.json › airpassengers.calendario.modelos.con_dias_pascua.aicc = -490.7221 | verificado |

### Con \(m\) grande el SARIMA falla por tres motivos

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `12` | dato | J: cap5_sarima.json › airpassengers.fourier.costo_m.0.observaciones_perdidas = 12<br>J: cap5_sarima.json › airpassengers.fourier.costo_m.0.rezago_maximo_sma1 = 12 | verificado |
| `52` | dato | J: cap5_sarima.json › airpassengers.fourier.costo_m.1.observaciones_perdidas = 52<br>J: cap5_sarima.json › airpassengers.fourier.costo_m.1.rezago_maximo_sma1 = 52 | verificado |
| `365` | dato | J: cap5_sarima.json › airpassengers.fourier.costo_m.3.observaciones_perdidas = 365<br>J: cap5_sarima.json › airpassengers.fourier.costo_m.3.rezago_maximo_sma1 = 365 | verificado |
| `156` | dato | R: directo_cap5.json › m10.n_semanal = 156 | verificado |
| `104` | dato | R: directo_cap5.json › m10.queda_tras_52 = 104 | verificado |
| `800` | simulación | DEF: longitud de la serie simulada (verifica_directo_cap5.R) | definición (no se mide) |
| `365.25` | calendario | DEF: días del año medio (calendario) | definición (no se mide) |
| `0,0,0` | modelo | R: auto.arima con un seno anual y frecuencia 365 | verificado |
| `ruido` | modelo | R: auto.arima sobre rnorm(800) con frecuencia 365 (el ejemplo del capítulo) | verificado |
| `nsdiffs` | modelo | R: nsdiffs del seno anual = 1 | verificado |
| `capítulo` | capítulo | C: capítulo 5 contiene «ARIMA$(0,0,0)(0,1,0)_{365}$»<br>C: capítulo 5 contiene «3 * sin(2 * pi * (1:800) / 365) + rnorm(800)» | verificado |
| `K3` | dato | J: 6 términos con K = 3 para todo m | verificado |

### Fourier modela la estación con \(2K\) parámetros, sea cual sea \(m\)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `11` | dato | CALC: m − 1 con m = 12 = 11 | verificado |
| `12` | convención | DEF: m | definición (no se mide) |

### Hace falta \(K=5\) para que Ljung–⁠Box deje de rechazar

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-359.18` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.0.aicc = -359.1791 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.0.nobs = 143 | verificado |
| `-409.18` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.1.aicc = -409.1814 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.1.nobs = 143 | verificado |
| `-460.96` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.2.aicc = -460.9633 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.2.nobs = 143 | verificado |
| `-495.24` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.3.aicc = -495.2436 | verificado |
| `0.0001` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.3.lb24_p = 0.0001 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.3.nobs = 143 | verificado |
| `-521.22` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.aicc = -521.2191 | verificado |
| `0.1341` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.lb24_p = 0.1341 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.nobs = 143 | verificado |
| `-521.45` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.5.aicc = -521.4512 | verificado |
| `0.1100` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.5.lb24_p = 0.11 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.5.nobs = 143 | verificado |
| `0.0001` | cota | J: LB p < 0.0001 para K = 1, 2, 3 (J guarda 0) | verificado |
| `10` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.n_terminos = 10 | verificado |
| `11` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.5.n_terminos = 11 | verificado |
| `errores` | modelo | J: modelos de error de J | verificado |

### Regresión armónica con AICc −521.2 y *airline* con −483.2: ¿cuál eliges? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-521.2` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.aicc = -521.2191 | verificado |
| `-483.2` | dato | J: cap5_sarima.json › airpassengers.airline.aicc = -483.2101 | verificado |
| `38` | dato | CALC: −483.21 − (−521.22) = 38.009 | verificado |
| `38.0` | dato | CALC: ídem = 38.009 | verificado |
| `143` | dato | J: cap5_sarima.json › airpassengers.fourier.comparabilidad.nobs_armonicos = 143 | verificado |
| `131` | dato | J: cap5_sarima.json › airpassengers.fourier.comparabilidad.nobs_airline = 131 | verificado |
| `15` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.n_par_total = 15 | verificado |
| `0.1341` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.lb24_p = 0.1341 | verificado |
| `0.2330` | dato | J: cap5_sarima.json › airpassengers.airline.diagnostico.lb24_p = 0.233 | verificado |
| `521.22` | dato | J: cap5_sarima.json › airpassengers.fourier.resultados.4.aicc = 521.2191 | verificado |
| `483.21` | dato | J: cap5_sarima.json › airpassengers.airline.aicc = 483.2101 | verificado |

### SARIMA, Fourier o STL: depende de \(m\) y de cómo cambia el patrón

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `stl` | modelo | J: STL + ARIMA = ARIMA(1,1,1) con deriva | verificado |

### Antes de comparar: qué hace cada rival y cómo se mide el error

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `100` | definición | DEF: MAPE en porcentaje | definición (no se mide) |
| `MAM` | documentación | DOC: docs_cap5.json › ets contiene «is multiplicative Holt-Winters' method with multiplicative errors» | verificado |
| `letras` | documentación | DOC: docs_cap5.json › ets contiene «The first letter denotes the error type» | verificado |
| `Ad` | documentación | DOC: docs_cap5.json › ets contiene «use a damped trend»<br>J: el ETS de la serie cruda es (M,Ad,M) en J | verificado |
| `snaive` | documentación | DOC: docs_cap5.json › snaive contiene «seasonal random walk» | verificado |
| `ETS nuevo` | capítulos 1–4 | C: «ETS» no aparece en los capítulos 1 a 4 | verificado |

### Con los últimos 24 meses como prueba, ¿qué método gana? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `19.43` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets_log.rmse = 19.429 | verificado |
| `14.69` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.armonica.mae = 14.69 | verificado |
| `3.15` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.armonica.mape = 3.151 | verificado |
| `43.18` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima.rmse = 43.184 | verificado |
| `120` | dato | J: cap5_sarima.json › airpassengers.comparativa.n_entrenamiento = 120 | verificado |
| `24` | dato | J: cap5_sarima.json › airpassengers.comparativa.n_prueba = 24 | verificado |
| `1958` | fecha | J: corte | verificado |
| `1959` | fecha | J: primera fecha de prueba | verificado |
| `1960` | fecha | J: última fecha de prueba | verificado |
| `orden` | orden | J: orden por RMSE: ETS log, armónica, STL, SARIMA | verificado |
| `pregunta 8` | capítulo | C: capítulo 5 (autoevaluación) contiene «segunda por RMSE ($19.51$» | verificado |

### Con una sola partición, el modelo de todo el capítulo queda cuarto

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `16` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets_log.n_par = 16 | verificado |
| `19.43` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets_log.rmse = 19.429<br>R: directo_cap5.json › m11.particion.ets_log.rmse = 19.428748 | verificado |
| `16.12` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets_log.mae (empate: decide el exacto) = 16.125<br>R: directo_cap5.json › m11.particion.ets_log.mae = 16.124863 | verificado |
| `3.55` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets_log.mape = 3.547<br>R: directo_cap5.json › m11.particion.ets_log.mape = 3.546884 | verificado |
| `16` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.armonica.n_par = 16 | verificado |
| `19.51` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.armonica.rmse = 19.505<br>R: directo_cap5.json › m11.particion.armonica.rmse = 19.50522 | verificado |
| `14.69` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.armonica.mae = 14.69<br>R: directo_cap5.json › m11.particion.armonica.mae = 14.689928 | verificado |
| `3.15` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.armonica.mape = 3.151<br>R: directo_cap5.json › m11.particion.armonica.mape = 3.151167 | verificado |
| `35.48` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.stl_arima.rmse = 35.481<br>R: directo_cap5.json › m11.particion.stl_arima.rmse = 35.481402 | verificado |
| `30.29` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.stl_arima.mae = 30.291<br>R: directo_cap5.json › m11.particion.stl_arima.mae = 30.290657 | verificado |
| `6.33` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.stl_arima.mape = 6.33<br>R: directo_cap5.json › m11.particion.stl_arima.mape = 6.330028 | verificado |
| `43.18` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima.rmse = 43.184<br>R: directo_cap5.json › m11.particion.sarima.rmse = 43.183666 | verificado |
| `39.45` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima.mae = 39.447<br>R: directo_cap5.json › m11.particion.sarima.mae = 39.447258 | verificado |
| `8.52` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima.mape = 8.516<br>R: directo_cap5.json › m11.particion.sarima.mape = 8.516316 | verificado |
| `45.48` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima_calendario.rmse = 45.477<br>R: directo_cap5.json › m11.particion.sarima_calendario.rmse = 45.477392 | verificado |
| `41.45` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima_calendario.mae = 41.452<br>R: directo_cap5.json › m11.particion.sarima_calendario.mae = 41.452159 | verificado |
| `8.95` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima_calendario.mape = 8.949<br>R: directo_cap5.json › m11.particion.sarima_calendario.mape = 8.949317 | verificado |
| `17` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets.n_par = 17 | verificado |
| `72.55` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets.rmse = 72.548<br>R: directo_cap5.json › m11.particion.ets.rmse = 72.547909 | verificado |
| `63.21` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets.mae = 63.213<br>R: directo_cap5.json › m11.particion.ets.mae = 63.212974 | verificado |
| `13.30` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets.mape = 13.303<br>R: directo_cap5.json › m11.particion.ets.mape = 13.303447 | verificado |
| `76.99` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.snaive.rmse (empate: decide el exacto) = 76.995<br>R: directo_cap5.json › m11.particion.snaive.rmse = 76.994589 | verificado |
| `71.25` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.snaive.mae = 71.25<br>R: directo_cap5.json › m11.particion.snaive.mae = 71.25 | verificado |
| `15.52` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.snaive.mape = 15.523<br>R: directo_cap5.json › m11.particion.snaive.mape = 15.523355 | verificado |
| `auto` | dato | J: auto.arima = airline (mismo RMSE) | verificado |
| `11` | dato | CALC: valores libres de la estacionalidad (m − 1) = 11<br>C: capítulo 5 contiene «valores de la estacionalidad» | verificado |
| `stl 2` | dato | J: n_par del STL + ARIMA = 2 en J<br>R: n_par = 2 en R | verificado |
| `16.12` | capítulo | C: capítulo 5 contiene «$16.12$» | verificado |
| `16.125` | dato | J: cap5_sarima.json › airpassengers.comparativa.modelos.ets_log.mae = 16.125 | verificado |
| `16.1249` | dato | R: directo_cap5.json › m11.particion.ets_log.mae = 16.124863 | verificado |
| `1,1,0` | modelo | R: STL + ARIMA sobre el entrenamiento | verificado |

### Con 61 orígenes, el SARIMA pasa de cuarto a primero

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `16.81` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.sarima = 16.812<br>R: directo_cap5.json › m11.om12.rmse_medio.sarima = 16.812296 | verificado |
| `21.42` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.ets_log = 21.416<br>R: directo_cap5.json › m11.om12.rmse_medio.ets_log = 21.415974 | verificado |
| `8.2` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.porcentaje_gana_al_sarima.ets_log = 8.2<br>R: directo_cap5.json › m11.om12.gana_al_sarima_pct.ets_log = 8.196721 | verificado |
| `21.85` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.stl = 21.848<br>R: directo_cap5.json › m11.om12.rmse_medio.stl = 21.848249 | verificado |
| `8.2` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.porcentaje_gana_al_sarima.stl = 8.2<br>R: directo_cap5.json › m11.om12.gana_al_sarima_pct.stl = 8.196721 | verificado |
| `22.38` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.armonica (empate: decide el exacto) = 22.385<br>R: directo_cap5.json › m11.om12.rmse_medio.armonica = 22.384699 | verificado |
| `9.8` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.porcentaje_gana_al_sarima.armonica = 9.8<br>R: directo_cap5.json › m11.om12.gana_al_sarima_pct.armonica = 9.836066 | verificado |
| `26.38` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.ets_orig = 26.384<br>R: directo_cap5.json › m11.om12.rmse_medio.ets_orig = 26.384012 | verificado |
| `14.8` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.porcentaje_gana_al_sarima.ets_orig = 14.8<br>R: directo_cap5.json › m11.om12.gana_al_sarima_pct.ets_orig = 14.754098 | verificado |
| `41.24` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.snaive = 41.238<br>R: directo_cap5.json › m11.om12.rmse_medio.snaive = 41.238047 | verificado |
| `11.5` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.porcentaje_gana_al_sarima.snaive = 11.5<br>R: directo_cap5.json › m11.om12.gana_al_sarima_pct.snaive = 11.47541 | verificado |
| `61` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.n_origenes = 61<br>R: directo_cap5.json › m11.om12.n = 61 | verificado |
| `1954` | fecha | J: primer origen 1954-12<br>R: R | verificado |
| `85` («más del 85 %»: 85.2) | dato | CALC: 100 − el peor porcentaje = 85.2 | verificado |
| `85.2` | dato | CALC: 100 − 14.8 = 85.2 | verificado |
| `12` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.horizonte = 12 | verificado |
| `22.38` | capítulo | C: capítulo 5 contiene «$22.38$»<br>C: capítulo 5 (autoevaluación) contiene «frente a $22.38$» | verificado |
| `22.385` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.rmse_medio.armonica = 22.385 | verificado |
| `22.3847` | dato | R: directo_cap5.json › m11.om12.rmse_medio.armonica = 22.384699 | verificado |

### La partición cayó justo después de la desaceleración de 1958, y el *airline* la extrapoló

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1958` | fecha | J: corte 1958-12 | verificado |
| `3.4` | dato | R: directo_cap5.json › m11.crecimiento_anual.1958 = 3.4155 | verificado |
| `6.2` | dato | R: directo_cap5.json › m11.crec_otros_min = 6.185185 | verificado |
| `21.8` | dato | R: directo_cap5.json › m11.crec_otros_max = 21.837709 | verificado |
| `4.7` | dato | R: directo_cap5.json › m11.sarima_pron.f59_vs_obs58 = 4.711362 | verificado |
| `6.9` | dato | R: directo_cap5.json › m11.sarima_pron.f60_vs_f59 = 6.94445 | verificado |
| `12.4` | dato | R: directo_cap5.json › m11.crecimiento_anual.1959 = 12.4234 | verificado |
| `11.2` | dato | R: directo_cap5.json › m11.crecimiento_anual.1960 = 11.1673 | verificado |
| `39.45` | dato | R: directo_cap5.json › m11.sesgo_sarima = 39.447258<br>R: directo_cap5.json › m11.mae_sarima = 39.447258<br>J: cap5_sarima.json › airpassengers.comparativa.modelos.sarima.mae = 39.447 | verificado |
| `24` | dato | R: directo_cap5.json › m11.errores_positivos = 24 | verificado |
| `14` | dato | R: directo_cap5.json › m11.om12.sarima_no_es_el_mejor = 14 | verificado |
| `12` | dato | CALC: orígenes entre 1957-05 y 1959-01 = 12 | verificado |
| `1957` | fecha | R: 1957-05 es uno de los orígenes en que el SARIMA no es el mejor | verificado |
| `1959` | fecha | R: 1959-01 es uno de los orígenes en que el SARIMA no es el mejor | verificado |
| `61` | dato | R: directo_cap5.json › m11.om12.n = 61<br>J: cap5_sarima.json › airpassengers.comparativa.origen_movil.n_origenes = 61 | verificado |
| `1960` | fecha | DEF: año pronosticado | definición (no se mide) |
| `9.4` | dato | R: directo_cap5.json › m11.ets_log_pron.f59_vs_obs58 = 9.352941 | verificado |
| `12.8` | dato | R: directo_cap5.json › m11.ets_log_pron.f60_vs_f59 = 12.814548 | verificado |
| `10.6` | dato | R: directo_cap5.json › m11.armonica_pron.f59_vs_obs58 = 10.586101 | verificado |
| `13.1` | dato | R: directo_cap5.json › m11.armonica_pron.f60_vs_f59 = 13.147799 | verificado |
| `3.4` | capítulo | C: capítulo 5 contiene «$3.4\,\%$» | verificado |
| `6.2` | capítulo | C: capítulo 5 contiene «$6.2$» | verificado |
| `21.8` | capítulo | C: capítulo 5 contiene «$21.8\,\%$» | verificado |
| `4.7` | capítulo | C: capítulo 5 contiene «$4.7\,\%$» | verificado |
| `6.9` | capítulo | C: capítulo 5 contiene «$6.9\,\%$» | verificado |
| `12.4` | capítulo | C: capítulo 5 contiene «$12.4$» | verificado |
| `11.2` | capítulo | C: capítulo 5 contiene «$11.2\,\%$» | verificado |
| `9.4` | capítulo | C: capítulo 5 contiene «$9.4$» | verificado |
| `12.8` | capítulo | C: capítulo 5 contiene «$12.8\,\%$» | verificado |
| `10.6` | capítulo | C: capítulo 5 contiene «$10.6$» | verificado |
| `13.1` | capítulo | C: capítulo 5 contiene «$13.1\,\%$» | verificado |

### A 24 meses, SARIMA y ETS sobre el logaritmo son indistinguibles

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `49` | dato | R: directo_cap5.json › m11.om24.n = 49 | verificado |
| `26.00` | dato | R: directo_cap5.json › m11.om24.rmse_medio.sarima = 26.001385 | verificado |
| `26.61` | dato | R: directo_cap5.json › m11.om24.rmse_medio.ets_log = 26.608126 | verificado |
| `27.80` | dato | R: directo_cap5.json › m11.om24.rmse_medio.stl = 27.799806 | verificado |
| `28.30` | dato | R: directo_cap5.json › m11.om24.rmse_medio.armonica = 28.295716 | verificado |
| `49.0` | dato | R: directo_cap5.json › m11.om24.gana_al_sarima_pct.ets_log = 48.979592 | verificado |
| `18.22` | dato | R: directo_cap5.json › m11.om12.error_mes_h_abs.sarima = 18.222774 | verificado |
| `15.96` | dato | R: directo_cap5.json › m11.om12.error_mes_h_abs.ets_log = 15.962692 | verificado |
| `cuarto` | orden | R: el SARIMA es 4.º por |e₁₂| | verificado |
| `61` | dato | R: directo_cap5.json › m11.om12.n = 61 | verificado |
| `24` | dato | J: cap5_sarima.json › horizonte = 24 | verificado |
| `12` | dato | J: cap5_sarima.json › airpassengers.comparativa.origen_movil.horizonte = 12 | verificado |
| `26.0014` | dato | R: directo_cap5.json › m11.om24.rmse_medio.sarima = 26.001385 | verificado |
| `26.6081` | dato | R: directo_cap5.json › m11.om24.rmse_medio.ets_log = 26.608126 | verificado |
| `27.7998` | dato | R: directo_cap5.json › m11.om24.rmse_medio.stl = 27.799806 | verificado |
| `28.2957` | dato | R: directo_cap5.json › m11.om24.rmse_medio.armonica = 28.295716 | verificado |
| `48.98` | dato | R: directo_cap5.json › m11.om24.gana_al_sarima_pct.ets_log = 48.979592 | verificado |
| `18.2228` | dato | R: directo_cap5.json › m11.om12.error_mes_h_abs.sarima = 18.222774 | verificado |
| `15.9627` | dato | R: directo_cap5.json › m11.om12.error_mes_h_abs.ets_log = 15.962692 | verificado |
| `26.00` | capítulo | C: capítulo 5 contiene «26.00» | verificado |
| `26.61` | capítulo | C: capítulo 5 contiene «26.61» | verificado |
| `27.80` | capítulo | C: capítulo 5 contiene «27.80» | verificado |
| `28.30` | capítulo | C: capítulo 5 contiene «28.30» | verificado |
| `49.0` | capítulo | C: capítulo 5 contiene «49.0» | verificado |
| `18.22` | capítulo | C: capítulo 5 contiene «18.22» | verificado |
| `15.96` | capítulo | C: capítulo 5 contiene «15.96» | verificado |

### El SARIMA frente a lo que se usa hoy: cuándo, no cuál es mejor

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `144` | dato | R: directo_cap5.json › datos.ap_n = 144 | verificado |

### Para seguir: tres ejercicios y las lecturas {columnas=1:1 .arriba}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `9.9` | sección de FPP3 | C: capítulo 5 contiene «§ 9.9»<br>WEB: otexts.com/fpp3: § 9.9 «Seasonal ARIMA models» (comprobado a mano el 2026-10-27) | verificado |
| `12.1` | sección de FPP3 | C: capítulo 5 contiene «§ 12.1»<br>WEB: otexts.com/fpp3: § 12.1 «Complex seasonality» (comprobado a mano el 2026-10-27) | verificado |
| `7.4` | sección de FPP3 | C: capítulo 5 contiene «§ 7.4»<br>WEB: otexts.com/fpp3: § 7.4 «Some useful predictors» (comprobado a mano el 2026-10-27) | verificado |
| `10.5` | sección de FPP3 | C: capítulo 5 contiene «§ 10.5»<br>WEB: otexts.com/fpp3: § 10.5 «Dynamic harmonic regression» (comprobado a mano el 2026-10-27) | verificado |
| `3.9` | capítulo (sin contrastar con el libro) | C: capítulo 5 contiene «Cap. 3.9» | verificado |
| `10.1` | sección de FPP3 | WEB: otexts.com/fpp3: § 10.1 «Estimation» y § 10.2 «Regression with ARIMA errors using fable» (2026-10-27) | verificado |
| `10.2` | sección de FPP3 | WEB: ídem | verificado |
| `9.1` | sección de FPP3 | WEB: otexts.com/fpp3: el ejemplo A10 (antidiabéticos) está en § 9.1, «Seasonal differencing» (2026-10-27) | verificado |
| `H02` | capítulo | C: capítulo 5 contiene «el caso de los corticoides (H02)» | verificado |
| `armónica dinámica` | capítulo | C: capítulo 5 contiene «§ 7.4, § 10.5 Regresores de calendario y regresión armónica dinámica» | verificado |
| `2026` | fecha | DEF: año de la consulta | definición (no se mide) |
