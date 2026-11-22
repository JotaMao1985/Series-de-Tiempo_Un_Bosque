# R1 · Registro de cambios · Capítulo 4 «Modelos ARIMA y Box–Jenkins»

Ronda R1 del `PLAN_Mejora_Cap4.md` (tareas T1.1–T1.3; decisiones D2, D3 y D10, y las tres diapositivas de §7.2).
Fecha: 2026-11-22. Un solo redactor. Especificación: `diagnostico/cap4/par_academico.md` y la tabla de §1 del plan.
Base: `7e9bc58`. Sin commit ni push.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/cap4/templates_1_3.html` | M1 (intro del simulador, el `33`, bloque Python), M2 (ciclo, salvedad de la cancelación, Ljung–Box de Python), M3 (tabla de evidencias, párrafo de la varianza, los dos bloques) |
| `ensamblado/cap4/templates_4_6.html` | M4 (primera frase, bloque Python), M5 (el φ̂ del modelo con deriva, «se aplana», «EXACTAMENTE», bloques) |
| `ensamblado/cap4/templates_7_9.html` | M7 (umbral del código, el ARIMA(2,1,2) según el estimador, «seis», bloques), M8 (tabla, recuadro de la varianza, bloque Python), M9 (tabla de formas, límite del pronóstico, numpy, bloque R) |
| `ensamblado/cap4/templates_10.html` | cuadro del Nilo, TRM congelada, arbitraje, 89.6 %, 1.07–1.14, resumen, ejercicios 1, 2 y 3 |
| `ensamblado/cap4/templates_11.html`, `templates_12.html` | M11 y M12 en pasado (D10) |
| `ensamblado/cap4/chapter.js` | selector de `forma-pronostico`, lectura de `sobrediferenciacion`, quiz ítems 4 y 6. Nada de `SIMULACROS` |
| `Htmls_Series/capitulo-4-modelos-arima.html` | reensamblado con `ensambla_cap4.py`; reproducible byte a byte (md5 `90d3892c…`) |
| `precalculo/genera_cap4.R` → `salidas/cap4_arima.json`, `cap4_datos.js` | sección 11b nueva (Monte Carlo de PP y ADF con raíz unitaria verdadera → `nilo.sim_raiz_unitaria`) y la nota de `metodos_estimacion` corregida. El resto del JSON, idéntico campo a campo salvo `generado` (`comprobaciones/r1_compara_json.out`) |
| `Htmls_Series/diapositivas/fuentes/capitulo_4.md`, `diapositivas/capitulo-4-modelos-arima.html` | 9 diapositivas (las tres pedidas y las que repetían lo mismo); reconstruido con `construir.py` |
| `Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap4.py`, `verificacion_cifras.md` | una clave re-anclada por título y 19 claims nuevos; el informe, regenerado |
| `diagnostico/cap4/comprobaciones/r1_*` | guiones y salidas de esta ronda |
| `diagnostico/cap4/capturas/r1/` | 32 capturas (ignoradas por git) |

`genera_soluciones.R` no se tocó: sus cifras del cap. 4 no se leen en ningún sitio y el texto de los ejercicios vive en
`templates_10.html`. Los capítulos 5 y 6 se reensamblaron después y quedan **idénticos a HEAD** (`git status` no los lista).

**Verificadores al cerrar**

- `python3 precalculo/verifica_todo.py` → 11 verificadores en verde (`r1_verifica_todo.out`).
- `verifica_bloques_cap6.py --html …capitulo-4…` → **760 de 760 cifras, 0 bloques con discrepancias** (antes 713 de 735).
  Los dos bloques de la TRM leyeron la copia de GitHub Pages (el verificador corre en `/tmp`). `r1_verifica_bloques.out`.
- Los 10 bloques de Python, cada uno solo en una carpeta vacía (`r1_bloques_python.py`): todos terminan con código 0; el
  de la TRM, dos veces (copia de la página del curso y de la carpeta de trabajo), con la misma salida. Las cifras de los
  comentarios que no salen del bloque son las de R citadas a propósito en líneas `#` (ya no en líneas `#>`) y tres
  afirmaciones sobre statsmodels comprobadas en `r1_python.out` (AIC 1267.2187, distancia al borde 0.0012/0.0020) o por
  el par (OPG 11.17, que con la copia congelada sigue dando 11.17).
- Diapositivas: `verifica_cifras_cap4.py` → 469 claims, 467 verificados, 2 marcados [SIN VERIFICAR] (los de antes), 0 que
  no coinciden, «todo verificado y cubierto»; `revisar.py` → 50 diapositivas, todas a escala ≥ 88 %.
  `verifica_directo_cap4.R` no se ejecutó.
- Por HTTP (servidor propio en 8763 y Chrome sin ventana en 9276, cerrados al acabar; `r1_revisa.js`): los doce módulos a
  1200 y 375 px con derivaciones, pistas y soluciones abiertas: 0 errores ni avisos de consola, 0 `.katex-error`, 0 `$`
  sin renderizar, ningún KaTeX dentro de `<pre>`, sin desbordamiento horizontal. Lecturas comprobadas: `sobrediferenciacion`
  con d = 1 dice «raíz MA fuera del círculo»; `forma-pronostico` (d1) da 816.18 → 842.17. `r1_revisa.out`.
- `audita_posicion_correcta.py` en verde (ninguna opción correcta cambió de sitio).

**Entorno:** R 4.6.0, forecast 9.0.2, tseries 0.10.62; Python 3.10, statsmodels 0.14.6, numpy 2.2.6; Node 26.

**Guiones** (`diagnostico/cap4/comprobaciones/`)

| guion | salida | qué comprueba |
|---|---|---|
| `r1_comprobaciones.R` | `r1_comprobaciones.out` | el pronóstico del ARIMA(1,1,1) y su límite; el cociente de varianzas frente a 2(1 − r₁) en el Nilo, log(lynx) y BJsales; r₁ de las series diferenciadas; raíces del (2,1,2) de la TRM; el factor 99/97 de σ̂²; el (2,1,2) del Nilo por CSS-ML y ML; deriva frente a c; la media del ARIMA(1,0,1) por estimador; el Monte Carlo de PP/ADF; cobertura del 80 %, asimetría y razón de cuadrados medios de la TRM; efecto Working |
| `r1_python.py` | `r1_python.out` | Ljung–Box con y sin y₁; AIC, AICc y `nobs_effective`; cociente y r₁ en Python; t del escalón; formato de numpy |
| `r1_bloques_python.py` | `r1_bloques_python.out` | los 10 bloques de Python publicados, cada uno solo |
| — | `r1_genera_cap4.out`, `r1_compara_json.out` | la regeneración del JSON y su comparación campo a campo con HEAD |
| — | `r1_verifica_bloques.out`, `r1_verifica_todo.out` | los verificadores al cerrar |
| `r1_revisa.js` | `r1_revisa.out` | la revisión por HTTP |

No se añadió ningún `<cite>`, `data-afirma`, autor, año ni página. La remisión «Capítulo 2 (Módulo 2.7)» es interna.
Se **quitó** una atribución implícita: el 1.01 de `auto.arima` se dice ahora «del código de `forecast`», sin atribuirlo
al artículo (que se contrastará en la R4).

Líneas: «orig.» son las de `71c42d8` (las del informe del par); «ahora», las del HTML ensamblado tras la ronda.

---

## T1.1 · Los dos errores

| # | módulo | orig. → ahora | qué decía | qué dice ahora | evidencia |
|---|---|---|---|---|---|
| 1 | M9 | 4581 → 4646–4672 | El ARIMA(1,1,1) sin constante pronostica «**Constante** en el último nivel» | «**Se aplana** en 842.17: no en el último dato (740), sino en el nivel al que lo lleva la parte ARMA», y un párrafo nuevo con la trayectoria 740 → 816.18 → 842.17 y el límite ŷ = y_T + (φ̂∇y_T + θ̂ε̂_T)/(1 − φ̂). El bloque R del M9 lo calcula (`ultimo 740.00 · h1 816.18 · h30 842.17 · limite 842.17`). Selector del simulador: «se queda plano» → «se aplana». En el M5, «d = 1 se queda plano» → «se aplana (no necesariamente en el último dato…)» | `r1_comprobaciones.out` § E1 (a 0.005 del límite desde h = 8); JSON `nilo.formas_pronostico.d1.media` |
| 2 | M1, M2, M3, M4, M8, M10, resumen, quiz, ej. 1 y 2 | 2872, 3255–3266, 3287–3294, 3591, 4422, 4442–4452, cuadro del Nilo, 5558–5575, 5620, 5731–5774 | La varianza es una de las «tres evidencias»; «si al diferenciar la varianza sube, te has pasado» es «la regla habitual»; d = 1 «Mínimo de varianza»; «la regla de la varianza es solo un primer aviso» | Las tres evidencias son **el gráfico con la ACF, las pruebas y los síntomas de haber diferenciado de más** (r̂₁ de la serie diferenciada cerca de −0.5 o por debajo; raíz MA cerca de 1). La varianza se sigue mostrando como descripción, con la razón de que no decide y la remisión al Capítulo 2 (Módulo 2.7): en el Nilo 2(1 − 0.498) = 1.003 frente a un cociente medido de 0.987; en log(lynx), 0.430 frente a 0.416. Detalle abajo | `r1_comprobaciones.out` § E2; bloques del M3 y del ej. 2 |

Detalle del hallazgo 2 (D3):

- **M1**, intro del simulador: «fíjate sobre todo en ρ̂₁ … La varianza … no es una pista aparte: el Módulo 3 explica por
  qué repite lo que ya dice ρ̂₁».
- **M2**, ciclo (identificación): «mirando el gráfico y la ACF, las pruebas de raíz unitaria y, si ya se diferenció, los
  síntomas de haberlo hecho de más».
- **M3**: tabla con las tres evidencias nuevas (filas: «El gráfico y la ACF», «Las pruebas», «Los síntomas de haber
  diferenciado de más», con −0.402, −0.626 y la raíz MA 1.144 del Módulo 8); el párrafo «¿Y la varianza de ∇ᵈy?» sustituye
  al que leía el mínimo como aviso. Bloque R: la sección de la varianza pasa a «describe, pero no decide», imprime
  `cociente 0.987 · dos_por_1_menos_r1 1.003`, y una «Evidencia 3» nueva imprime `-0.402 -0.626`. Bloque Python, igual
  (`0.987 1.003`, `[-0.402, -0.626]`). El objetivo del módulo («tres evidencias complementarias») y su título no cambian.
- **M4**: «es el orden que minimiza la varianza y el que pide KPSS» → «es el orden que pide KPSS, la prueba que usa
  `auto.arima`».
- **M8**: la fila d = 1 de la tabla, «Mínimo de varianza.» → «Raíz MA en 1.364, fuera del círculo.» (1/0.7329, en el
  bloque); la lectura del simulador, «mínimo de varianza» → «raíz MA fuera del círculo»; el recuadro «El criterio de la
  varianza no siempre dispara» → «La columna de la varianza no decide d», con el argumento del Capítulo 2, el caso de
  log(lynx) que ya traía y «hay que mirar siempre las raíces, junto con el ρ̂₁ de la serie diferenciada».
- **M10**: el cuadro del Nilo (etapa 1) deja la varianza y dice «la ACF decae despacio desde 0.498»; la nota de las dos
  lecciones cambia «la varianza que casi no baja» por «el ρ̂₁ = −0.402 de la serie diferenciada».
- **Resumen**: «tres evidencias —el gráfico con la ACF, las pruebas y los síntomas de haber diferenciado de más— … La
  varianza por orden de diferencia no es una evidencia más: repite lo que dice r₁ (Módulo 2.7)»; la viñeta de la
  sobrediferenciación pierde «La regla de la varianza es solo un primer aviso» y gana el aviso del ρ̂₁ y «sin pareja en el AR».
- **Ejercicio 1** (BJsales): la pista ya no manda a mirar la varianza sino el gráfico, las pruebas y el ρ̂₁ de la serie
  diferenciada; en la solución, la línea de las varianzas («mínimo en d = 1») se sustituye por el r̂₁ de las diferencias
  (`0.3118 -0.4756`).
- **Ejercicio 2** (log(lynx)): enunciado, pista, respuesta, bloque y discusión dejan de tratar la varianza como un
  criterio que «falla» y explican por qué baja: el bloque imprime `r1 0.785 · cociente 0.416 · dos_por_1_menos_r1 0.430`.
- **Quiz**: ningún ítem usaba la varianza para decidir d; no hubo que tocarlo por esto.

## T1.2 · Imprecisiones, menores y dudosos del par

| par | módulo | ahora | antes | después | evidencia |
|---|---|---|---|---|---|
| I1 | M2 Py | 3200–3210 | Ljung–Box sobre `ajuste.resid` completo (y₁ = 1120 como residual), 0.761, «cada programa inicializa el filtro a su manera» | `ajuste.resid[1:]`, como en los M4 y M10: **0.8225**; comentario: R da 0.7997 con sus residuales (el primero, 1.12, rastro de su arranque) | `r1_python.out` § M2 |
| I2 | M2 | 3103–3110 | «si es del MA, … hay que bajar d» | añade la salvedad: si el AR tiene una raíz casi igual, se cancelan y lo que sobra son p y q, no la diferencia; remite al ARIMA(2,1,2) de la TRM. El recuadro de la TRM del M10 lo recuerda | `r1_comprobaciones.out` § I·M2 (AR 1.0042, MA 1.0000) |
| I3 | M7 | 4176–4183; bloque R 4302–4312 | el ARIMA(2,1,2) «tiene una raíz AR de módulo 1.001» (y el explorador del M6 lo muestra con 2.241 sin aviso) | 1.001 con el CSS-ML de `Arima()`, el que usa `auto.arima`; por ML exacta (el explorador) es otro óptimo, algo peor (log L −630.445 frente a −630.169), con la raíz en 2.241; «la raíz depende del estimador». El bloque R imprime las dos | `r1_comprobaciones.out` § I·M7 |
| I4 | M7 Py | 4330–4342 | AICc a mano con `nobs` y «no descuenta d en nobs» | usa `f.aicc` (que ya usa `nobs_effective`, como dice el M6): **1267.471**; la diferencia con R está en la log-verosimilitud (AIC 1267.219 frente a 1267.254); el n mueve 0.003 | `r1_python.out` § M7 (fila `c4-m7-22`) |
| I5 | M10 | 5248–5252 | «el Capítulo 6 lo confirma … con una cobertura del 89.6 %» (a doce meses) | «el intervalo del 95 % del naïve cubre el 89.6 %, contando juntos los horizontes de 1 a 12 meses» | par (`cap6_evaluacion.json`, `cob95`) |
| I6 | quiz 4 | 9097, 9104 | «Con d = 1 la constante es la media de las diferencias» | «Con d = 1 la deriva, μ_w = c/φ(1), es la media de las diferencias»; la retro de fallo dice que no es la c salvo con p = 0. La opción sigue en su sitio | `r1_comprobaciones.out` § quiz 4 (deriva −2.88, c −2.10) |
| I7 | quiz 6 | 9149–9170 | «veinte rezagos sin acercarse a cero»; «La conclusión sobre d es correcta»; «hay que diferenciar antes de leer p y q» | «baja despacio y, pasado el rezago 3, sigue rondando 0.2 hasta el 20 (aún 0.237 en el 13)»; «Que la serie no sea estacionaria es razonable, pero de ahí no sale d = 1»; la clave dice «hay que resolver d» y su retro añade «raíz unitaria o cambio de nivel como el de 1899 (Módulos 3 y 8)» | JSON `nilo.identificacion.cruda.acf` |
| M1 | M5 Py | 3910 | «EXACTAMENTE la media muestral» | «prácticamente» | par (919.350541) |
| M2 | M7 | 4244 | «detrás de él hay siete candidatos» | «seis» | par |
| M3 | M8 Py | 4581 | «a 0.001 del borde» | «a 0.0012 y 0.0020 del borde» | salida del bloque |
| M4 | M9 | 4643–4644 | «Vuelve a la media 920.56» sin aviso | «(con el ajuste CSS-ML de `Arima()`; por máxima verosimilitud, la del Módulo 5, es 920.70)» | `r1_comprobaciones.out` § M·M9 |
| M5 | M9 Py | 4910 | `print(np.round(...))` → `[1.40599e+02 …]` frente al comentario | `.tolist()`: `[140.599, 140.599, 196.925, 0.168]` | salida del bloque |
| M6 | M10 | 5248–5253 | «con ρ̂₁ = 0.088 la varianza real … es entre 1.07 y 1.14 veces» | «los cambios mensuales tienen ρ̂₁ = 0.088: medido en la muestra, el cuadrado medio de los cambios a 3, 6 y 12 meses es entre 1.07 y 1.14 veces hσ̂²»; ya no se presenta como deducido de ρ̂₁. El bloque R lo calcula (`1.10 1.14 1.07`) | `r1_comprobaciones.out` § N2–N4 (con solo ρ̂₁ saldría 1.117–1.161) |
| M7 | resumen | 5563–5566 | «con d ≥ 2 el software se niega» | «`forecast::Arima` se niega …(statsmodels admite un término cuadrático si se le pide)» | bloque del M5 |
| D1 | M10 | 5145–5150 | arbitraje aplicado a la TRM sin matiz | «…lo que predice la teoría financiera para el precio con que se negocia…, aunque aquí se modela su promedio mensual, que no es exactamente ese precio». Se matiza sin afirmar más (no se dice nada del efecto Working, que sí se comprobó: ρ₁ 0.2695 simulado) | `r1_comprobaciones.out` § Working |
| D2 | simulacro | — | ítem 7, fila 2 | **no se toca** (banco) | — |

Del inventario de fuentes, además:

| fila | módulo | qué cambió | evidencia |
|---|---|---|---|
| `c4-m10-71`, `c4-m9-31` | ej. 3 (pista); `genera_cap4.R` | La pista atribuía la diferencia de σ̂² a que `Arima()` «usa CSS-ML». Ahora: «sobre todo porque `Arima()` divide la suma de cuadrados de los residuales entre n* − k y `arima()` da la de máxima verosimilitud, que divide entre n*». En el generador, el comentario y la `nota` de `metodos_estimacion` dicen lo mismo (el comentario del M9 en Python ya lo decía bien) | `r1_comprobaciones.out` § sigma2: Arima(method = "ML") da 20176.92, igual que por defecto; SCR/97 = 20176.91, SCR/99 = 19769.30; razón 1.02062 = 99/97. En BJsales la razón es 1.01376 frente a 149/147 = 1.01361 (los coeficientes difieren algo), de ahí «sobre todo» |
| `c4-m7-22` | M7 Py | véase I4 | `r1_python.out` |
| — | M5 | «c = −2.883 × (1 − 0.271)» sin decir de dónde sale 0.271 → «con el φ̂₁ = 0.271 del propio modelo con deriva, que no es el 0.254 del modelo sin ella»; el bloque R imprime `round(coef(f1b), 4)` (`0.2707 -0.9054 -2.8827`) | salida del bloque |

## T1.2 · Cifras sin generador (norma 1)

| fila | cifra | de dónde sale ahora |
|---|---|---|
| `c4-m3-15` | 100 % (PP) y 51.3 % (`adf.test`, k = 4) con raíz unitaria verdadera | `genera_cap4.R` § 11b → `nilo.sim_raiz_unitaria` (`pp_rechaza 1`, `adf_k4_rechaza 0.513`), al final del guion y con su propia semilla 2026, así que no mueve ninguna cifra anterior. Reproduce `verifica_directo_r46_cap4.R` |
| `c4-m9-26` | 83.9 % (el 80 % a un mes en la TRM) | bloque R del M10: `cubre_80_a_un_mes 0.839` (115 de 137); también en el de Python |
| `c4-m10-33` | asimetría 0.76 | bloque R del M10: `asimetria_1 0.76`; Python, `stats.skew` 0.76 |
| `c4-m10-37` | 1.07–1.14 | bloque R del M10: `1.10 1.14 1.07` (y Python) |

## T1.3 · TRM congelada (D2) y M11/M12 en pasado (D10)

- **TRM**: los dos bloques del M10 leen `trm_mensual_2015-01_2026-06.csv` de la carpeta de trabajo o, si no está, de
  `https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/`, como el cap. 3. La prosa dice de dónde salen los datos
  («Los bloques de código no la descargan: leen la copia fija del curso…, la misma de los Capítulos 2 y 3») y la frase que
  presentaba el bloque («de la descarga en datos.gov.co…») pasa a «de la lectura de la copia fija». `#>` ajustados a la
  copia: la cota 4080.28 (antes 4080.29, y se retira el comentario que explicaba esa discrepancia), el error de
  `forecast()` frente a la fórmula 0 (antes 4.5e−13), el de `get_forecast` 4.5e−13 (antes 9.1e−13) y la raíz MA del
  (2,1,2) de statsmodels 4.208 (antes 4.231). El resto de cifras de la TRM no cambia.
- **M11**: el quiz «se presentó», «duró», «fueron diez preguntas», «ya se aplicó»; el simulacro «sigue sirviendo de
  repaso». **M12**: «Con este módulo se cerraba lo que entraba al Parcial 2, que se aplicó el miércoles 14 de octubre…; el
  preparcial se escribió para prepararlo y sigue sirviendo de repaso»; «Qué pesaba cada cosa en el parcial». Títulos de
  módulo sin cambios. El simulacro, el preparcial y su enlace, intactos.

## Verificador de bloques: de 713/735 a 760/760

Cada una de las 22 discrepancias de la línea base se resolvió en lo que ve el lector, no en el verificador:

- **Cifras de R dentro de líneas `#>` de Python** (M1, M2, M3, M4, M5, M8): pasan a una línea de comentario aparte
  («R da …»), de modo que una línea `#>` solo trae lo que imprime el bloque.
- **Umbrales en líneas `#>`** (`0.05` del M2, `0.01` del M3): el comentario pasa a su propia línea.
- **El `33` del M1**: era un redondeo en prosa de 32.8; comentario y nota dicen ahora «32.8».
- **numpy** (M9): `.tolist()` (véase M5).
- **El `-8.9` del M8**: el bloque imprime ahora el t (`-8.92`), y el de R queda en el comentario.
- **M2 y M7 de Python**: cambian de cálculo (I1, I4), no solo de comentario.

El total de cifras anunciadas sube de 735 a 760 porque los bloques ganaron líneas (M3, M5, M7, M9, M10 y los ejercicios 1 y 2); salen todas.

## Diapositivas del cap. 4

| diapositiva (título) | antes | después |
|---|---|---|
| «En el Nilo, diferenciar una vez casi no reduce la varianza» | «¿Hacía falta diferenciar? Los Módulos 3 y 8 lo responden» | «… La varianza sola no lo dice; los Módulos 3 y 8 lo responden» |
| «El ciclo completo cabe en un esqueleto corto de R» (notas) | statsmodels 0.761 «cada programa inicializa el filtro a su manera» | 0.761 con y₁ = 1120 como residual, 0.8225 sin él, como el material |
| «Tres evidencias miran la serie desde ángulos distintos» (título igual) | gráfico, varianza, pruebas | gráfico y ACF (0.498), pruebas, síntomas de diferenciar de más (−0.402, −0.626); la varianza, a las notas con 1.003 frente a 0.987 y la remisión al Módulo 2.7 |
| «`auto.arima` es un algoritmo…» | «módulo < 1.01 se descartan» | «módulo < 1.01 (el umbral del código de `forecast`) se descartan» |
| «Diferenciar de más deja una firma algebraica en el MA» | d = 1 «Mínimo de varianza» | «Raíz MA en 1.364» (y la nota de verificación, al día) |
| «La regla de la varianza es un aviso, no un teorema…» | título y notas que tratan la varianza como regla | **título nuevo**: «La varianza no decide d: en log(lynx) baja al diferenciar y aun así sobra»; notas con 0.785, 0.430 y 0.416. Clave del verificador re-anclada |
| «La forma del pronóstico…» (notas) | «se queda plana en el último nivel» | «se aplana, pero no en el último dato: parte de 740, pasa a 816.18 y se queda en 842.17» |
| «Con d = 2 el intervalo a 30 años es 3.5 veces más ancho…» | «**Constante** en el último nivel» | «**Se aplana** en 842.17, no en el último dato (740)» |
| «El mínimo de AICc es un modelo degenerado…» y la de la TRM (notas) | «descarta … menor que 1.01»; el arbitraje sin matiz | «…1.01, el umbral de su código»; el arbitraje, con el mismo matiz que el capítulo |
| «Lo que se llevan hoy» | «tres evidencias —gráfico, varianza y pruebas—» | «—gráfico y ACF, pruebas, síntomas de diferenciar de más—» |
| «Para seguir…» | ej. 2: «Si la varianza y las pruebas discrepan, decide con las raíces» | «La varianza baja al diferenciar; decide con las pruebas y las raíces» |
| «La constante c significa cosas distintas…» (notas) | «d = 1 se queda plano» | «se aplana (no necesariamente en el último dato)» |

Claims nuevos en `verifica_cifras_cap4.py`: 1120, 0.8225 (C); 0.498, −0.402, −0.626 (J); 0.987, 1.003, 1.364 (CALC); 0.5 y
−0.5 (definición); 0.733 (J); 0.785, 0.430, 0.416 (C, ej. 2); 740 (CALC), 816.18 y 842.17 (J y regenerado). Ninguna cifra
nueva se calculó en `verifica_directo_r46_cap4.R` (no hizo falta).

## Lo que no se hizo, y por qué

- **El simulacro** (`SIMULACROS['cap4-simulacro']`) no se tocó. Para el banco, fuera de esta fase: el ítem 10 usa la
  varianza de ∇ᵈy como dato para decidir d (contradice D3), y el ítem 7, fila 2, es una lectura heurística (dudoso del par).
- **`genera_soluciones.R`** no se tocó: la `nota` de `cap4_ej2$regla_varianza` («la regla heurística no dispara») sigue
  diciendo lo de antes, pero ese JSON no se muestra en ningún sitio. Queda anotado.
- **El dudoso del arbitraje** se matizó, no se resolvió: el efecto Working se comprobó en R (0.2695 simulado; 0.2492
  teórico con 21 días) pero no se escribió, porque llevaría a discutir si 0.088 es compatible con 0.25, y eso es más de lo
  que el capítulo necesita aquí.
- **La P4 del quiz** sigue diciendo «Son tres» en la pista y sin retro por opción, y las pistas siguen dando el criterio:
  es la D9, de la R5.
- **El 1.001 del artículo** de Hyndman y Khandakar no se menciona: no se leyó en esta sesión; la R4 lo citará.
- **«Tres evidencias»** sigue siendo la forma de decirlo (ahora con otras tres): la notación es de la R3 (T3.2).
- **La promesa del M9** («El Módulo 10 lo mide», 83.9 %) ahora se cumple en el bloque del M10, pero la prosa del M10 no
  la retoma: es la D6, de la R3.
