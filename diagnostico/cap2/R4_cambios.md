# Capítulo 2 · ronda R4 «fuentes» · cambios

Fecha: 2026-11-17. Redactor único de la ronda: subagente redactor R4 (Fable 5.2). Sin commits ni push.
Parte del commit `31bfbb6`, en el que el capítulo no tenía ninguna cita marcada.

> **Los veredictos de este documento son la propuesta del redactor.** Ninguna entrada de
> `bibliografia/contraste/cap2.yml` lleva `verificado_por`: lo firma el verificador, que no redactó. Por eso
> `audita_citas.py` falla hoy con un F08 por cada entrada citable, y con un F11 que no depende del verificador
> (el tope de palabras de FPP3; ver «Lo que no cierra»).

## Resultado

- **74 afirmaciones marcadas y registradas** (había 0): **46 `respaldada`**, **11 `con-matiz`**, **9 `propia`**,
  **8 `pendiente`**. Las 57 citables llevan cita visible; ninguna queda con el aviso «respaldada sin cita».
- **72 citas visibles**: 37 de FPP3, 25 de Cryer y Chan (2008), 9 de Hamilton (1994) y 1 de la ayuda de R.
  Shumway y Stoffer no se cita en ningún sitio: solo hay la 3.ª edición y el curso cita la 4.ª.
- **131 citas literales** en el registro, todas copiadas de la caché y comprobadas antes de escribir
  (`r4_registro.py` usa las funciones F05 y F07 del auditor, y el auditor las vuelve a comprobar: 220 con las 89
  del capítulo 1).
- **17 cambios de prosa** (y un punto añadido tras una cita), todos porque la fuente leída decía otra cosa o no decía nada (lista abajo). Ninguna
  cifra, gráfico, simulador ni dato tocado: el verificador de bloques sigue en 277 de 277.
- **Ninguna obra nueva** en Zotero ni en `referencias.json`. Seis páginas de ayuda de R nuevas en la caché.
- Los capítulos 3–6 quedan **byte a byte iguales a `HEAD`** tras reensamblar.

Por módulo:

| módulo | afirmaciones | respaldada | con-matiz | propia | pendiente |
|---|---:|---:|---:|---:|---:|
| M1 | 7 | 6 | 0 | 0 | 1 |
| M2 | 7 | 5 | 1 | 0 | 1 |
| M3 | 9 | 5 | 2 | 1 | 1 |
| M4 | 11 | 7 | 1 | 1 | 2 |
| M5 | 8 | 6 | 2 | 0 | 0 |
| M6 | 9 | 4 | 0 | 4 | 1 |
| M7 | 12 | 9 | 1 | 2 | 0 |
| M8 | 6 | 4 | 1 | 0 | 1 |
| M9 | 5 | 0 | 3 | 1 | 1 |
| **total** | **74** | **46** | **11** | **9** | **8** |

## Cómo se hizo (y cómo se rehace)

Tres guiones en `diagnostico/cap2/comprobaciones/`, reejecutables:

| guion | qué hace |
|---|---|
| `r4_marca.py` | parte del capítulo 2 **en el commit `31bfbb6`**, aplica los 17 cambios de prosa y las 79 marcas (cada una exige que su texto aparezca exactamente una vez), instala el CSS de las citas, los marcadores del pie, la lista de cada módulo y la del capítulo, y llama a `genera_referencias.genera()` |
| `r4_registro.py` | escribe `cap2.yml` desde su tabla de entradas: comprueba cada cita contra la caché (página o sección del localizador, y que la página impresa sea la de esa página del PDF) y calcula la huella. Si algo no está, no escribe. Conserva los `verificado_por` que el verificador ponga, mientras la huella no cambie |
| `r4_inventario.py` | rehace el inventario contra el texto de hoy |
| `r4_software.R`, `r4_software.py` | comprueban ejecutando lo que el capítulo dice del software (las 9 `propia`) |
| `r4_resumen.py` | saca del registro la tabla de abajo |

En `r4_registro.py` cada cita está **dos veces**: arriba, como se leyó (el pasaje entero, hasta 25 palabras), y en
la tabla `RECORTES`, el subtramo que va al registro. Hubo que recortar para acercarse al tope F11: leídas enteras
sumaban 665 palabras de FPP3 y 616 de Cryer y Chan; registradas, 397 y 376.

## Una fila por afirmación

| id | tipo | veredicto | obra y localizador (en **negrita**, la cita visible) |
|---|---|---|---|
| c2-m1-01 | definicion | respaldada | **FPP3 §9.1**; Cryer y Chan p. 16 |
| c2-m1-03 | definicion | respaldada | **Cryer y Chan p. 16**; Hamilton p. 46 |
| c2-m1-04 | resultado | pendiente | — |
| c2-m1-06 | definicion | respaldada | **Cryer y Chan p. 17**; Hamilton p. 45 |
| c2-m1-07 | resultado | respaldada | **Hamilton p. 46**; Cryer y Chan p. 17 |
| c2-m1-13 | resultado | respaldada | **FPP3 §9.1** |
| c2-m1-15 | resultado | respaldada | **Cryer y Chan p. 16** |
| c2-m2-01 | definicion | respaldada | **Hamilton p. 47**; Cryer y Chan p. 17 |
| c2-m2-02 | definicion | respaldada | **Hamilton pp. 47–48** |
| c2-m2-03 | resultado | respaldada | **Hamilton p. 48**; **Cryer y Chan p. 285** |
| c2-m2-06 | resultado | respaldada | **Cryer y Chan p. 110**; **FPP3 §2.9** |
| c2-m2-08 | regla | con-matiz | **FPP3 §2.9** |
| c2-m2-09 | regla | respaldada | **FPP3 §5.4** |
| c2-m2-10 | resultado | pendiente | — |
| c2-m3-01 | definicion | respaldada | **FPP3 §2.8** |
| c2-m3-05 | resultado | respaldada | **Cryer y Chan p. 46** |
| c2-m3-06 | dato | propia | — |
| c2-m3-07 | definicion | respaldada | **FPP3 §2.8** |
| c2-m3-09 | regla | con-matiz | **FPP3 §2.9**; **Cryer y Chan p. 128**; **FPP3 §2.8**; **FPP3 §9.1** |
| c2-m3-13 | resultado | con-matiz | **Cryer y Chan pp. 263–264**; **Hamilton pp. 557–558** |
| c2-m3-15 | resultado | pendiente | — |
| c2-m3-16 | resultado | respaldada | **Cryer y Chan p. 46** |
| c2-m3-17 | atribucion | respaldada | **FPP3 §5.4**; ayuda de R §Description |
| c2-m4-01 | definicion | respaldada | **FPP3 §9.5** |
| c2-m4-02 | definicion | respaldada | **Cryer y Chan p. 112**; **FPP3 §9.5**; Hamilton p. 111 |
| c2-m4-04 | atribucion | respaldada | **Cryer y Chan p. 115**; FPP3 §9.5; ayuda de R §Details |
| c2-m4-05 | resultado | respaldada | **Cryer y Chan p. 114** |
| c2-m4-06 | resultado | respaldada | **Cryer y Chan p. 115** |
| c2-m4-07 | resultado | pendiente | — |
| c2-m4-08 | resultado | con-matiz | **Cryer y Chan p. 115** |
| c2-m4-09 | dato | propia | — |
| c2-m4-11 | regla | respaldada | **FPP3 §9.5**; Cryer y Chan p. 116 |
| c2-m4-12 | regla | respaldada | **Cryer y Chan p. 115**; Hamilton p. 112 |
| c2-m4-14 | dato | pendiente | — |
| c2-m5-01 | resultado | con-matiz | **FPP3 §9.3**; **Cryer y Chan p. 67**; Cryer y Chan p. 71; **Cryer y Chan p. 89** |
| c2-m5-04 | resultado | respaldada | **Cryer y Chan p. 13**; **Hamilton p. 443** |
| c2-m5-05 | definicion | respaldada | **Cryer y Chan p. 71**; Cryer y Chan p. 128 |
| c2-m5-07 | resultado | respaldada | **Hamilton p. 445** |
| c2-m5-09 | definicion | respaldada | **FPP3 §9.1**; Hamilton p. 436 |
| c2-m5-10 | resultado | con-matiz | **Hamilton p. 442**; FPP3 §9.1; Cryer y Chan p. 27 |
| c2-m5-11 | atribucion | respaldada | **FPP3 §9.1**; **FPP3 §5.4** |
| c2-m5-12 | regla | respaldada | **Hamilton pp. 435–436** |
| c2-m6-01 | regla | respaldada | **FPP3 §9.1**; Cryer y Chan p. 129 |
| c2-m6-04 | definicion | respaldada | **Cryer y Chan pp. 128–129**; Cryer y Chan p. 130; Hamilton p. 475 |
| c2-m6-05 | definicion | pendiente | — |
| c2-m6-06 | regla | propia | — |
| c2-m6-09 | dato | propia | — |
| c2-m6-10 | dato | propia | — |
| c2-m6-11 | resultado | propia | — |
| c2-m6-16 | resultado | respaldada | **FPP3 §9.1** |
| c2-m6-17 | resultado | respaldada | **Cryer y Chan pp. 129–130** |
| c2-m7-01 | definicion | respaldada | **FPP3 §9.1** |
| c2-m7-02 | definicion | respaldada | **FPP3 §9.2**; **FPP3 §9.1**; Cryer y Chan p. 233 |
| c2-m7-05 | atribucion | respaldada | **FPP3 §9.1** |
| c2-m7-06 | regla | respaldada | **FPP3 §9.1** |
| c2-m7-07 | regla | respaldada | **FPP3 §9.1** |
| c2-m7-08 | resultado | propia | — |
| c2-m7-09 | resultado | respaldada | **FPP3 §9.1**; Cryer y Chan p. 126 |
| c2-m7-11 | resultado | respaldada | **Cryer y Chan pp. 126–127**; Cryer y Chan p. 57; FPP3 §9.4; **FPP3 §9.1** |
| c2-m7-14 | atribucion | respaldada | **Cryer y Chan pp. 240–241**; Cryer y Chan p. 247 |
| c2-m7-15 | dato | propia | — |
| c2-m7-18 | dato | con-matiz | **FPP3 §9.1** |
| c2-m7-19 | dato | respaldada | **ayuda de R §Description; §Format**; ayuda de R §Format |
| c2-m8-01 | resultado | respaldada | **FPP3 §9.1** |
| c2-m8-02 | resultado | respaldada | **FPP3 §3.1**; Cryer y Chan p. 98 |
| c2-m8-03 | definicion | respaldada | **Cryer y Chan p. 101**; **FPP3 §3.1** |
| c2-m8-04 | definicion | pendiente | — |
| c2-m8-05 | regla | con-matiz | **FPP3 §3.1**; **Cryer y Chan p. 101** |
| c2-m8-08 | resultado | respaldada | **FPP3 §5.6** |
| c2-m9-01 | regla | con-matiz | **FPP3 §9.7** |
| c2-m9-11 | regla | con-matiz | **FPP3 §5.10**; FPP3 §5.3 |
| c2-m9-12 | regla | con-matiz | **FPP3 §5.10** |
| c2-m9-13 | resultado | propia | — |
| c2-m9-24 | atribucion | pendiente | — |

## Frases reescritas porque la fuente decía otra cosa

Son las que el verificador debe leer con más cuidado: la frase nueva es del redactor.

| id | decía | dice | por qué |
|---|---|---|---|
| c2-m4-12 | «La banda ±1.96/√T de la PACF vale bajo la hipótesis de que la serie es ruido blanco.» | «…vale para los rezagos mayores que *p* cuando la serie sigue un AR(*p*); el ruido blanco es el caso *p* = 0.» | Cryer y Chan p. 115 y Hamilton p. 112 dan la banda de la PACF bajo un AR(p), para rezagos mayores que p. Es lo que hace legible la regla «se corta tras el rezago p» del recuadro de arriba |
| c2-m5-11 | «Es el modelo por defecto para precios de activos, índices y tipos de cambio, y explica por qué el pronóstico ingenuo… es tan difícil de batir en esos casos.» | «Las caminatas aleatorias se usan mucho para datos financieros y económicos, y eso explica por qué en precios e índices bursátiles el pronóstico ingenuo… suele ser el mejor método.» | FPP3 §9.1 y §5.4 no dicen «por defecto» ni nombran los tipos de cambio |
| c2-m7-05 | «La recomendación de FPP3 es aplicar primero la diferencia estacional: a veces con ella basta…, y se ahorra una diferencia regular que solo añadiría ruido.» | «Hyndman y Athanasopoulos (2021, §9.1) recomiendan aplicar primero la diferencia estacional cuando el patrón estacional es marcado: a veces con ella basta…, y se ahorra una diferencia regular.» | FPP3 la da con una condición ([literal fuera de git: `_local/citas/cap2.yml`, c2-m7-05 · fuente 2]); «solo añadiría ruido» no es suyo |
| c2-m4-04 | «…la recursión de Durbin–Levinson, que es lo que hace `pacf()` en R.» | «…(Cryer y Chan, 2008, p. 115), que da los mismos valores que `pacf()` en R.» | la ayuda de `pacf()` no nombra la recursión y su código no se ha leído; que los valores coinciden sí se comprobó (4e-14) |
| c2-m4-09 | «Esta es la recursión que implementan `pacf()` de R, el método `ldb` de statsmodels y la función `calcularPACF()`…» | «Con esta recursión coinciden `pacf()` de R y el método `ldb` de statsmodels, y es la que implementa la función `calcularPACF()`…» | lo mismo; `calcularPACF()` sí es código del repo |
| c2-m1-04 | «en la práctica, imposible de verificar con una sola realización» | «en la práctica, difícil de verificar…» | lo leído (Shumway y Stoffer, 3.ª ed., p. 23) dice «difficult». La entrada sigue `pendiente`: esa edición no se cita |
| c2-m8-02 | «y la más frecuente es el logaritmo» | «y a menudo sirve el logaritmo» | FPP3 §3.1: «often useful» |
| c2-m8-05 (titular) | «En la práctica casi siempre se usa el logaritmo» | «En este curso se usa el logaritmo» | «casi siempre» no tiene fuente; es la decisión D6. Lo mismo en la fila «Box–Cox» de la tabla de resumen del M9 |
| c2-m8-08 | «(que `fable` aplica sola y `statsmodels` no)» | «(que `fable` aplica sola)» | lo de statsmodels no tiene pasaje |
| c2-m6-01 | «Las dos más usadas son ADF y KPSS» | «Aquí se usan dos, ADF y KPSS» | «las más usadas» no tiene fuente |
| c2-m6-06 | «Datos poco informativos (muestra corta). Ninguna prueba concluye.» | «Datos poco informativos: ninguna prueba concluye.» | la causa no tiene fuente |
| M7, sobrediferenciación | «Ese es el indicio más frecuente» | «Ese es el indicio» | «más frecuente» no tiene fuente |
| M6, comentario de Python | «R interpola en las tablas de Banerjee et al. (1993) y statsmodels usa la superficie de respuesta de MacKinnon» | «R lo interpola en una tabla de valores criticos y statsmodels lo aproxima con una superficie de respuesta» | ni Banerjee et al. ni MacKinnon se han leído. Lo que el comentario decía coincide con las ayudas de `adf.test` (tseries) y `adfuller` (statsmodels), leídas en esta sesión, pero ninguna es obra de la biblioteca y un comentario de código no admite marca |
| M9, ejercicio 4 (pista) | «los tipos de cambio son el ejemplo clásico de caminata aleatoria con deriva» | «el Módulo 6 encontró en la TRM una raíz unitaria» | «el ejemplo clásico» no tiene fuente |
| M9, lecturas (FPP3) | «secc. 9.1 … y secc. 3.1–3.2 (transformaciones y Box–Cox)» | «secc. 9.1–9.2 (estacionariedad, diferenciación y el operador B), secc. 2.8–2.9 (autocorrelación y ruido blanco) y secc. 3.1 (transformaciones y Box–Cox)» | la 3.2 es «Time series components»; títulos leídos en la caché |
| c2-m9-24 | «(4.ª ed.), secc. 1.4–1.6 (autocovarianza y estacionariedad) y 2.1 (diferenciación)» | «(4.ª ed.): medidas de dependencia, series estacionarias, estimación de la correlación y diferenciación. En la 3.ª edición (2011) son las secc. 1.4–1.6 y 2.3; la numeración de la 4.ª puede ser otra.» | en la 3.ª la 2.1 es «Introduction» y la diferenciación está en la 2.3; la 4.ª no se ha leído |
| c2-m2-02 | «…i.i.d.» | «…i.i.d. (Hamilton, 1994, pp. 47–48).» | un punto tras la cita, para que no quede sin cerrar |

## Los `pendiente` (8) y por qué

| id | qué afirma | qué falta |
|---|---|---|
| c2-m1-04 | la estacionariedad estricta es difícil de verificar con una realización | **4.ª ed. de Shumway y Stoffer**: solo leído en la 3.ª (p. 23) |
| c2-m3-15 | dividir entre T garantiza una matriz semidefinida positiva, con un sesgo hacia cero | **4.ª ed.**: leído en la 3.ª (p. 29), que además no habla de sesgo «hacia cero» |
| c2-m4-07 | el denominador de la recursión es la varianza del error de predicción; v_k = v_{k−1}(1 − φ_kk²) | **4.ª ed.**: en la 3.ª es la Propiedad 3.4 (p. 112) |
| c2-m9-24 | la lectura de Shumway y Stoffer | **4.ª ed.**: su numeración no se puede comprobar |
| c2-m6-05 | qué descompone el KPSS y cuál es su nula; sus dos variantes | **Kwiatkowski et al. (1992)**, en la biblioteca sin texto. La nula «la serie es estacionaria» sí está respaldada por FPP3 (c2-m6-16) |
| c2-m8-04 | cómo funciona el criterio de Guerrero | **Guerrero (1993)**, en la biblioteca sin texto. La descripción coincide con el código de `forecast:::guer.cv` y reproduce su λ (`r4_software.out`) |
| c2-m2-10 | con ruido incorrelado pero no independiente la varianza de r_k puede no ser 1/T | ningún pasaje leído lo dice |
| c2-m4-14 | la TRM: qué es y de dónde sale | la serie de datos.gov.co no es una obra de la biblioteca: hay que darla de alta en «4 Datos y software» |

Ninguno lleva localizador ni fuente en el registro, como pide la norma; lo leído en la 3.ª edición va en la `nota`.

## Las `propia` (9)

Todas son afirmaciones sobre el software o conclusiones del capítulo que ninguna obra de la biblioteca respalda.
Se comprobaron ejecutando (`r4_software.R` → `.out`; `r4_software.py` → `r4_software_py.out`):

| id | qué | comprobación |
|---|---|---|
| c2-m3-06 | `acf()` de R y de statsmodels dividen entre T | diferencia con la fórmula: 2e-15 y 2e-16 |
| c2-m4-09 | `pacf()`, `ldb` y `ywm` coinciden con la recursión | 4e-14 (R) y 1e-14 (statsmodels) |
| c2-m6-09 | `adf.test` y `kpss.test` interpolan en tablas y avisan | cuerpo de las funciones y los tres avisos |
| c2-m6-10 | k por defecto de `adf.test` | firma de la función: `trunc((length(x) - 1)^(1/3))` = 5 |
| c2-m7-15 | 4 rezagos frente a 2; 0.368 frente a 0.537; crítico 0.463 | código de `kpss.test` y `ndiffs`, y `ur.kpss@cval` |
| c2-m6-06 | la tabla de las cuatro combinaciones ADF/KPSS | se sigue de las dos nulas; ninguna fuente la da |
| c2-m6-11 | por qué el ADF se equivoca con la estacionalidad | las tres evidencias del propio módulo |
| c2-m7-08 | Var(∇y) = 2(1 − ρ₁)Var(y) y los dos contraejemplos | identidad + `r1_errores.R`, `maestra_r1.R` |
| c2-m9-13 | el árbol de hojas constantes ante una tendencia | es un argumento; **no hay ejemplo calculado ni fuente** |

## Los `con-matiz` (11)

| id | el matiz |
|---|---|
| c2-m2-08 | FPP3 habla de barras grandes o de bastante más del 5 % fuera; «un patrón» es del capítulo |
| c2-m3-09 | la tabla de patrones: «exponencial», «memoria corta» y «no queda estructura lineal» son glosa del capítulo |
| c2-m3-13 | Cryer y Chan: correlación espuria «a veces», no siempre; el capítulo dice «tendrán» |
| c2-m4-08 | el costo O(k) frente a O(k³) no está en la fuente |
| c2-m5-01 | Cryer y Chan llaman a φ = 1 «más razonable» que el caso explosivo; «rara vez sirve» es más fuerte |
| c2-m5-10 | «tendencia estocástica» no tiene, según Cryer y Chan, una definición generalmente aceptada |
| c2-m7-18 | FPP3 describe `unitroot_ndiffs()` y `unitroot_nsdiffs()`; el capítulo habla de las de `forecast` |
| c2-m8-05 | Cryer y Chan: no suele justificarse estimar λ con precisión; «tiene su propia incertidumbre» es del capítulo |
| c2-m9-01 | el procedimiento de FPP3 §9.7 es para datos no estacionales y sigue hasta el ajuste |
| c2-m9-11 | FPP3 no habla de «fuga de información» ni de parámetros de una transformación |
| c2-m9-12 | FPP3 describe el origen móvil; no dice que la validación cruzada estándar «no sirve» |

No reescribí estas frases: el matiz está en la `nota` y lo decide el verificador (o Javier).

## Las atribuciones que no tenían cita

| nombre | qué se hizo |
|---|---|
| Dickey–Fuller (ADF) | c2-m6-04: Cryer y Chan pp. 128–129 (visible) y Hamilton p. 475, que la atribuye a Dickey y Fuller (1979). El artículo no está en la biblioteca y no se cita |
| KPSS | el nombre y la nula, FPP3 §9.1 (c2-m6-16); la descomposición y las variantes, `pendiente` (c2-m6-05) |
| Yule–Walker | c2-m4-05: Cryer y Chan p. 114 |
| Durbin–Levinson | c2-m4-04: Cryer y Chan p. 115 («Levinson (1947) and Durbin (1960)») |
| Guerrero | FPP3 §3.1 atribuye el método sin describirlo; la descripción, `pendiente` (c2-m8-04). El nombre aparece además en la prosa del simulador y del recuadro de cifras, sin marca |
| Banerjee et al., MacKinnon | reescrito sin nombres (comentario de código) |
| Ljung–Box | c2-m3-17: FPP3 §5.4 (visible) y la ayuda de `Box.test()` |
| «modelo airline» | c2-m7-14: Cryer y Chan pp. 240–241 (visible) y ejercicio 10.9, p. 247. Las otras cuatro menciones (ejercicio 3, cierre, dos comentarios de código) remiten al mismo nombre y no llevan marca |
| la recomendación de FPP3 | c2-m7-05, con su condición |
| Box–Cox | c2-m8-03: Cryer y Chan p. 101 ([literal fuera de git: `_local/citas/cap2.yml`, c2-m8-03 · fuente 1]); el artículo no se cita |

## Lecturas del M9, listas por módulo, pie y cadena

- **Lecturas.** La de FPP3, corregida con secciones leídas (9.1–9.2, 2.8–2.9, 3.1). La de Shumway y Stoffer, con los
  temas y la numeración de la 3.ª edición, declarada como tal (`pendiente`). Las de Kwiatkowski et al. (1992) y
  Guerrero (1993) coinciden con `referencias.json` (volumen, número y páginas, de Crossref) y con la bibliografía
  de FPP3; siguen tecleadas y los artículos no se han leído. Debajo, «Referencias citadas en este capítulo»
  (marcadores `REFERENCIAS-CAPITULO`): cuatro obras.
- **Listas por módulo.** Los nueve módulos llevan su `<aside class="fuentes-modulo">` generado (de 1 a 3 obras).
- **Pie.** La lista tecleada se sustituyó por los marcadores `PIE-REFERENCIAS`; la escribe el generador con las
  cuatro obras de rol `basica`, como en el capítulo 1.
- **CSS.** El bloque de las citas se copia tal cual del capítulo 1 (`.cita`, `.fuentes-modulo`, `.lista-fuentes`),
  en el mismo sitio. Ninguna clase nueva de Tailwind: `compila_tailwind.py --comprobar` en verde.
- **Cadena.** `ensamblado/ensambla_cap3.py` tiene una sección nueva, «1b», que retira ese CSS y devuelve al pie la
  lista tecleada que el capítulo 3 tiene hoy (guardada en el propio guion), y que aborta si no encuentra los
  marcadores. Tras `ensambla_cap3.py --escribir` y `ensambla_cap4|5|6.py`, `git diff --stat -- Htmls_Series`
  solo lista el capítulo 2. **Cuando el capítulo 3 haga su ronda de fuentes, esa sección se borra.**
- `r2b_sintaxis.py`: cinco «OK», ninguna declaración repetida.

## El inventario

`bibliografia/contraste/cap2_inventario.tsv` pasa de 136 a **119 filas**, y cada `texto` existe literal en el
capítulo de hoy (de una afirmación marcada se toma el tramo hasta su primera cita). Lleva una columna nueva,
`r4`, con el destino de cada fila:

- 74 `registrada` (36 de prioridad alta, 38 de media);
- 45 `sin marcar`, con su motivo (11 de alta, 27 de media, 7 de baja), entre ellas 3 que el inventario viejo no
  tenía;
- 29 filas viejas salen: 19 absorbidas por otra afirmación, 1 trasladada (la TRM, al M4) y 9 retiradas porque la
  frase ya no existe (`r4_inventario.out` las lista una por una).

De las 11 de prioridad alta sin marcar: seis son propias o remiten a otra ya registrada (c2-m5-08, c2-m6-12,
c2-m7-13, c2-m9-04, c2-m9-05, c2-m9-06); dos son de software sin obra en la biblioteca (c2-m6-14, c2-m8-09); una
vive en JavaScript (c2-m8-10); una es la lectura de FPP3 ya corregida (c2-m9-23); y **una no tiene pasaje**:
c2-m1-16, «los coeficientes estimados no significan lo que parecen, los errores estándar están mal y los
pronósticos heredan el problema».

## Cambios fuera del capítulo y del registro

- `bibliografia/instantaneas.yml`: seis ayudas de R nuevas (`acf`, `plot.acf`, `Box.test`, `diff`, `UKgas`, `ar`),
  con `extrae_fuente.py --doc`. Se citan tres (`acf`, `Box.test`, `UKgas`); `plot.acf` se menciona en una nota;
  `diff` y `ar` se leyeron y no hicieron falta.
- `bibliografia/uso_fuentes.json`: regenerado con `--uso` (27 obras, 6 en uso).
- `ensamblado/ensambla_cap3.py`: la sección 1b.
- **`precalculo/audita_citas.py` no se tocó**, ni el vocabulario de localizadores (no hizo falta: `§9.7`, `§5.10`,
  `pp. 47–48` ya eran válidos) ni `prueba_audita_citas.py` (24 de 24).

## Comprobaciones

| qué | resultado |
|---|---|
| `python3 precalculo/genera_referencias.py --comprobar` | sin cambios: el HTML es el que el generador escribiría |
| `python3 precalculo/audita_citas.py` (`r4_audita.out`) | **58 hallazgos: 57 × F08** (falta `verificado_por`, una por cada entrada citable) **y 1 × F11** (FPP3, 790 palabras). Ningún F01–F07, F09 ni F12; ningún aviso F03. 108 citas visibles y 106 afirmaciones en los seis capítulos; 220 citas literales comprobadas |
| `python3 precalculo/audita_citas.py --cierre` | además, «quedan 8 afirmaciones pendientes» |
| `python3 precalculo/prueba_audita_citas.py` | 24 inyecciones, todas con su código |
| `python3 precalculo/audita_citas.py --uso-comprobar` | al día |
| `python3 precalculo/verifica_todo.py` | 10 de 11 en verde; falla «ninguna cita de memoria», por lo de arriba |
| verificador de bloques, capítulo 2 (`r4_bloques_cap2.out`) | 277 de 277, 0 bloques con discrepancias; no quedó `precalculo/serie.csv`. Los de 3–6 no se volvieron a correr: sus HTML son idénticos a `HEAD` |
| `ensambla_cap3.py` | «reproducible byte a byte» |
| navegador por HTTP, 1200 y 375 px, los nueve módulos | consola limpia, 0 `.katex-error`, el documento no desborda, las 72 citas dentro del ancho y con destino, las listas de fuentes caben. Las 72 se leyeron en su frase: ninguna cae entre sujeto y verbo ni entre un sustantivo y su complemento |

El servidor de `localhost:8731` **no estaba en marcha** al empezar (el puerto no respondía); se levantó con la
configuración `htmls-series` de `.claude/launch.json` y se dejó corriendo.

## Lo que no cierra, para la sesión maestra y para Javier

1. **F11 · el tope de 400 palabras por obra es global y FPP3 ya iba en 393 con el capítulo 1.** El capítulo 2
   añade 397: 790. Es el punto que el informe de la R4 del capítulo 1 dejó abierto («la próxima afirmación que se
   contraste con FPP3 obliga a recortar otra o a revisar el tope»). No toqué el auditor: intenté hacer el tope
   por capítulo —la cabecera del guion lo lista bajo «Qué comprueba, por capítulo»— y el entorno bloqueó el
   cambio, con razón: relajar un control no le corresponde al redactor. Las alternativas: (a) tope por obra y
   capítulo, con lo que este capítulo pasa (397 y 376); (b) subir el tope; (c) recortar más, que con 37 citas
   visibles de FPP3 dejaría subtramos de tres o cuatro palabras, poco útiles como evidencia. Cryer y Chan queda
   en 388 sumando los dos capítulos: al borde.
2. **Los 57 veredictos citables esperan firma.** Donde reescribí, la frase es mía y la nota lo dice.
3. **Lo que desbloquea el acceso institucional**: la 4.ª de Shumway y Stoffer (cuatro pendientes), Kwiatkowski et
   al. (1992) y Guerrero (1993).
4. **Cryer y Chan (2008) y Hamilton (1994) pasan a citarse a la vista** (25 y 9 citas). Son obras de rol
   `complementaria` cuyo PDF tiene la procedencia sin confirmar en `ejemplares.yml`. Sin ellas no hay respaldo
   leído para ADF, Yule–Walker, Durbin–Levinson, la regresión espuria ni las definiciones formales.
5. **c2-m9-13 (árboles)** queda como argumento sin fuente ni ejemplo calculado.
6. **c2-m1-16** (alta, sin marcar) y **c2-m2-10** (`pendiente`): dos frases sobre consecuencias para la inferencia
   sin pasaje leído.
7. **La autoevaluación y los comentarios de código no admiten marca** (viven en JavaScript o en `<pre>`): nueve
   filas del inventario quedan «sin marcar» por eso.
8. **TRM**: falta la ficha de datos (c2-m4-14).
9. **En `r4_registro.py` las citas leídas son más largas que las registradas**; si se revisa el tope, basta vaciar
   `RECORTES` para registrar los pasajes enteros.

---

# Tras la verificación (2026-11-17)

El verificador independiente (`R4_verificacion.md`) firmó 51 entradas y dejó 23 sin firmar: 7 errores y 16
juicios. Esta sección dice qué se hizo con cada una y **manda sobre lo anterior**: los recuentos de arriba son
los de la primera pasada. Sin commits.

## Estado vigente

- **80 afirmaciones**: 51 `respaldada`, 12 `con-matiz`, 9 `propia`, 8 `pendiente`. **79 citas visibles**: 40 de
  FPP3, 27 de Cryer y Chan, 11 de Hamilton y 1 de la ayuda de R. 152 citas literales en el registro.
- **Las 51 entradas firmadas no se tocaron**: comparadas campo a campo con la copia firmada, ninguna cambia y
  las 51 conservan su `verificado_por`.
- **29 entradas esperan lectura y firma**: las 23 que el verificador no firmó, todas cambiadas, y 6 nuevas.
- Los cambios viven en una capa aparte de cada guion, para que se lean juntos: `PROSA_V` y `MARCAS_V` en
  `r4_marca.py`; `CAMBIOS_V`, `NUEVAS_V` y `RECORTES_V` en `r4_registro.py`. Las notas de las entradas
  cambiadas empiezan por «TRAS LA VERIFICACIÓN».

## Los 7 errores

| id | qué se hizo |
|---|---|
| c2-m4-05 | **Reescrita**: «Los coeficientes φ_k1, …, φ_kk de la definición satisfacen el sistema de Yule–Walker de orden k…». Ya no habla de ajustar una regresión |
| c2-m3-13 | **Reescrita**: «Dos series no estacionarias independientes pueden mostrar una correlación cruzada alta sin tener ninguna relación real». Propuesta: `respaldada` |
| c2-m4-02 | **Reescrita**, siguiendo a Hamilton p. 111: «con el proceso centrado…, es el último coeficiente, φ_kk, de la mejor predicción lineal de y_t a partir de sus k valores anteriores (Hamilton, 1994, p. 111):». La cita va antes de los dos puntos y «regresión» desaparece. FPP3 §9.5 queda como fuente sin cita visible |
| c2-m1-06 | cita movida: «es débilmente estacionario (Cryer y Chan, 2008, p. 17) si cumple las tres condiciones:» |
| c2-m5-01 | **Reescrita**: «Rara vez sirve para modelar datos reales» → «Es una no estacionariedad menos razonable que la de φ = 1 (Cryer y Chan, 2008, p. 89)». Propuesta: `respaldada` |
| c2-m5-09 | cita visible → Hamilton p. 436; FPP3 §9.3 añadida a las fuentes |
| c2-m6-04 | segunda cita visible, p. 130, sobre una frase reescrita: «La regresión con constante y tendencia es la que corresponde cuando la alternativa es una tendencia lineal más un error estacionario (Cryer y Chan, 2008, p. 130), y es la que `adf.test()` de R estima siempre» |

## Los 16 juicios

| id | resolución |
|---|---|
| c2-m2-09 | **frase**: «Un buen modelo… ha exprimido toda la estructura predecible…, y lo que sobra… es indistinguible del ruido blanco» |
| c2-m2-01 | `con-matiz` (más general que las dos fuentes) |
| c2-m4-01 | **frase**: «aparecerán» → «pueden aparecer» |
| c2-m7-01 | **frase**: «la herramienta estándar para eliminar» → «una manera de eliminar» |
| c2-m7-06 | Cryer y Chan p. 128 añadido a las fuentes |
| c2-m4-04 | **frase**: «En la práctica la PACF muestral se calcula a partir de la ACF: se sustituyen las autocorrelaciones teóricas ρ_k por las muestrales r_k y se aplica la recursión de Durbin–Levinson (…), que da los mismos valores que `pacf()` en R. Por eso no coincide exactamente con el último coeficiente de una regresión por mínimos cuadrados sobre k rezagos.» `con-matiz`: las dos cosas que dice del software se comprobaron ejecutando (`r4_software.R`, `maestra_r4.R`), no vienen de la fuente |
| c2-m1-15 | Cryer y Chan p. 55 añadido (los ARMA como modelos para series estacionarias) |
| c2-m5-07 | `con-matiz` |
| c2-m8-01 | **frase**: «La diferenciación estabiliza la media; para la varianza hace falta una transformación» |
| c2-m2-08 | **frase**: «no es evidencia de nada» → «no basta como evidencia»; sigue `con-matiz` por «un patrón» |
| c2-m3-01 | **frase**: «mide cuánto se parece» → «mide la relación lineal entre una serie y una copia de sí misma…» |
| c2-m5-11 | **frase**: «…; como su pronóstico es el último valor observado, en precios e índices bursátiles el pronóstico ingenuo… suele ser el mejor método». Añadida la cita de FPP3 §9.1 que lo dice |
| c2-m7-11 | **frase**: «En la duda, conviene diferenciar de menos» → «No conviene diferenciar más de lo necesario» |
| c2-m8-05 | cita movida a «variaciones porcentuales»; sigue `con-matiz` |
| c2-m9-01 | nota completada (ni «siempre» ni el «porque» son de la fuente); sigue `con-matiz`. La cita no se movió: tras «secuencia de decisiones» habría partido el sustantivo de su relativa |
| c2-m7-08 | **frase acotada** (`propia`): «en una muestra de una serie estacionaria el cociente de varianzas se acerca a 2(1−r_1)» |

## Atribuciones que seguían sin marca

| dónde | qué se hizo |
|---|---|
| título «KPSS — Kwiatkowski, Phillips, Schmidt y Shin» | **c2-m6-18**, nueva, con la cita en el título: FPP3 §9.1 y Hamilton p. 532 |
| lectura de FPP3 | **c2-m9-23**, nueva: la obra y la primera sección las escribe el generador; las citas del registro son los títulos de las cinco secciones |
| lectura de Kwiatkowski et al. (1992) | **c2-m9-25**, nueva. «El artículo original de la prueba KPSS» → «el artículo al que se atribuye la prueba KPSS (FPP3 §9.1)». La ficha sigue tecleada; coincide con la bibliografía de FPP3 y con `referencias.json` |
| lectura de Guerrero (1993) | **c2-m9-26**, nueva, con cita a FPP3 §3.1; ficha tecleada, coincide con FPP3 §3.8 |
| «criterio de Guerrero» en la prosa | **c2-m8-13**, nueva, en su primera aparición (la introducción del simulador), con un inciso: «—el que Hyndman y Athanasopoulos (2021, §3.1) ofrecen para elegirla—». Las otras menciones repiten el nombre y no llevan marca |
| «se trabaja casi siempre con una versión más manejable» | **c2-m1-05**, nueva: se quitó «casi siempre»; Cryer y Chan p. 17 y Hamilton p. 46 |

Las tres lecturas marcadas como `respaldada` lo son por lo que FPP3 dice de esas obras, no por haber leído los
artículos: qué hace el KPSS (c2-m6-05) y qué hace el criterio de Guerrero (c2-m8-04) siguen `pendiente`.

## Lo que el verificador tiene que volver a leer y firmar (29)

Cambiadas (23): c2-m1-06, c2-m1-15, c2-m2-01, c2-m2-08, c2-m2-09, c2-m3-01, c2-m3-13, c2-m4-01, c2-m4-02,
c2-m4-04, c2-m4-05, c2-m5-01, c2-m5-07, c2-m5-09, c2-m5-11, c2-m6-04, c2-m7-01, c2-m7-06, c2-m7-08, c2-m7-11,
c2-m8-01, c2-m8-05, c2-m9-01.

Nuevas (6): c2-m1-05, c2-m6-18, c2-m8-13, c2-m9-23, c2-m9-25, c2-m9-26.

En seis de las cambiadas la prosa marcada no cambió (misma huella) y solo cambian fuentes, cita visible, nota o
veredicto: c2-m1-15, c2-m2-01, c2-m5-07, c2-m5-09, c2-m7-06, c2-m9-01.

## Fuera del capítulo y del registro

- El inventario pasa a 121 filas: 80 registradas y 41 sin marcar.
- Para que Cryer y Chan no pasara del tope al añadir fuentes se recortaron o retiraron ocho de sus citas, todas en entradas
  sin firmar (`RECORTES_V` y las fuentes de `CAMBIOS_V`): queda en 381 palabras en el capítulo, 393 en el curso.
- `audita_citas.py` y el tope F11 no se tocaron. FPP3 sube a 509 palabras en el capítulo (902 en el curso).

## Comprobaciones tras la corrección

| qué | resultado |
|---|---|
| `audita_citas.py` (`r4_audita.out`) | 29 hallazgos: **28 × F08** (las 22 cambiadas citables y las 6 nuevas; c2-m7-08 es `propia`) **y 1 × F11** (FPP3, 902). Nada más; 241 citas literales comprobadas |
| `--cierre` | además, 8 pendientes |
| `prueba_audita_citas.py` | 24 de 24 |
| `genera_referencias.py --comprobar`, `--uso-comprobar` | sin cambios; al día |
| verificador de bloques del capítulo 2 | 277 de 277, sin `precalculo/serie.csv`. La primera pasada dio 273 de 277: el bloque del ejercicio 4, que descarga la TRM viva, recibió un 503 de datos.gov.co (`r4b_bloques_cap2_sin_red.out`); repetida, pasó |
| capítulos 3–6 tras reensamblar | idénticos a `HEAD`; `ensambla_cap3.py`, reproducible; `r2b_sintaxis.py`, cinco «OK» |
| HTTP, 1200 y 375 px, nueve módulos | consola limpia, 0 `.katex-error`, sin desborde, 79 citas con destino y dentro del ancho |

## Observaciones del verificador sobre entradas firmadas, sin aplicar

Para no tocar entradas firmadas quedan como están dos notas que el verificador encontró inexactas (no cambian
el veredicto): la de c2-m5-05 (Cryer y Chan sí escriben el caso AR(1) con raíz 1/φ, en una nota al pie de la
p. 71) y la de c2-m3-05 (la ec. 3.6.2 escribe r_k, no γ̂_k). Y c2-m3-15, `pendiente`: aunque llegue la 4.ª
edición, «sesgo pequeño hacia cero» probablemente habrá que ajustarlo.
