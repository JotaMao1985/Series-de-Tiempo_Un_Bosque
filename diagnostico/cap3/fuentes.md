# Capítulo 3 · Afirmaciones que exigen fuente (diagnóstico, 2026-11-19)

Archivo leído: `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` (commit `58bdfc5`; el archivo coincide con HEAD): los once
módulos (`<template id="module-N">`), las introducciones de simuladores, `AUTOEVALUACIONES['cap3']` (10 preguntas) y
`['parcial2']` (10), los tres ejercicios, las lecturas, el pie y los metadatos del JS (el JSON de datos y los comentarios
que citan a alguien). Inventario completo, una fila por afirmación:
`bibliografia/contraste/cap3_inventario.tsv` (254 filas, mismas columnas que los del capítulo 1 y 2; `hallado` y `r4`
vacíos por encargo). No se inventariaron las cifras que calcula R ni las derivaciones que el capítulo muestra paso a paso
(propias); sí las frases que las enmarcan. Lo repetido (resumen, quiz, Módulo 10) va en filas con `REPITE c3-…`.
El capítulo no tiene ningún `data-afirma` ni `cite.cita` (0 ocurrencias): todo lo que sigue va sin cita visible.
**Los capítulos 3 a 6 se ensamblan:** la fuente es `ensamblado/cap3/cap3_modulos.html` y `cap3_js.js`; las líneas del TSV
son las del HTML final.

## Recuentos

| tipo | alta | media | baja | total |
|---|---:|---:|---:|---:|
| definicion | 2 | 13 | 0 | 15 |
| resultado | 48 | 38 | 7 | 93 |
| regla | 14 | 26 | 11 | 51 |
| dato | 39 | 17 | 4 | 60 |
| atribucion | 16 | 13 | 1 | 30 |
| historica | 0 | 5 | 0 | 5 |
| **total** | **119** | **112** | **23** | **254** |

Por módulo: pie y datos 8 · M1 21 · M2 19 · M3 15 · M4 15 · M5 20 · M6 8 · M7 20 · M8 24 · M9 29 · M10 70 (prosa 47,
autoevaluación 12, actividad del Parcial 2 11) · M11 5.

Estado de la lectura (columna `hallado` vacía; esta es la clasificación del inventariante a partir de lo que dice `donde_buscar`,
por `python3 diagnostico/cap3/diag/fuentes_cuenta.py`):

| estado | alta | media | baja | total |
|---|---:|---:|---:|---:|
| respaldada en lo leído | 46 | 52 | 3 | 101 |
| parcial | 12 | 11 | 0 | 23 |
| con matiz o tensión | 22 | 9 | 3 | 34 |
| discrepa o error | 8 | 1 | 1 | 10 |
| no hallado en lo leído | 14 | 11 | 0 | 25 |
| no comprobable aquí (falta leer, extraer o generar) | 6 | 3 | 0 | 9 |
| propia o sin fuente necesaria | 0 | 5 | 12 | 17 |
| localizada, sin veredicto | 11 | 20 | 4 | 35 |

«Respaldada» = un pasaje leído respalda la afirmación; según la norma lo verifica alguien que no la redactó. Las rutas son
`ruta:línea` bajo `bibliografia/_local/` (`texto/<clave>/pNNNN.txt` es el archivo de página, «impr.» la página impresa de su
encabezado; `web/…` es FPP3 o una ayuda de R). Los `[…]` de `donde_buscar` son: `[DISCREPA]` 6 filas, `[ERROR]` 4,
`[CON-MATIZ]` 28, `[TENSIÓN]` 5, `[NO HALLADO]` 27, `[PARCIAL]` 23, `[NO COMPROBABLE/LOCALIZADOR/SIN LEER/SIN EXTRAER/SIN GENERADOR]` 7.

## Lo que más pesa (prioridad alta, ordenado por daño al estudiante)

1. **Todo lo que se atribuye a Yule** — `c3-m7-02` («inventó en 1927 el modelo autorregresivo… en la ventana centenaria»),
   `c3-m0-05` (el JSON dice «ventana centenaria de Yule (1927)»), `c3-m8-17` («el que hizo famoso a Yule»), `c3-m10-37`.
   `yule1927method` está en la biblioteca **sin PDF**: no se ha leído, y ninguna caché dice que Yule usara 1770–1869 ni que ajustara
   un AR(2) a las manchas (Cryer solo cita a Yule 1926, por correlaciones espurias). Con él, el «ciclo solar de unos once años»
   no tiene fuente (`c3-m7-03`, `c3-m9-06`, `c3-m10-55`, `c3-m10-46`, `c3-m10-18`).
2. **La condición de estacionariedad del AR, enunciada de más** — `c3-m1-15` [DISCREPA]: «si |φ|≥1… no existe una solución
   estacionaria». Para |φ|>1 sí existe, no causal (Shumway Ej. 3.2–3.3, PDF p0100–0101; Cryer Ej. 4.16); solo para φ=1 no. El quiz
   del propio módulo lo dice bien («y_t depende solo de los choques hasta t», `c3-m10-70`). Igual `c3-m2-17` (el triángulo «es
   exactamente el conjunto con varianza finita»: con φ=(0,2) la fórmula da −σ²/3) y `c3-m2-02` [DISCREPA]: «la teoría asintótica no
   es la de la regresión clásica» contradice a Hamilton, Tabla 8.1 caso 4 (PDF p0224): en un AR estacionario los t y F usuales son
   asintóticamente válidos.
3. **El periodo del pseudo-ciclo** — `c3-m2-12`: la fórmula del capítulo (ángulo de la raíz) es la de Cryer y Shumway, pero FPP3 §9.5
   (arima.txt:328) da otra para el «periodo medio de los ciclos» (paráfrasis). Con el AR(2) de las manchas: 11.22 frente a 11.84 (con φ=(1,−0.5):
   8.00 frente a 8.69, `c3-m10-76`). El capítulo compara 11.22 con el ciclo solar sin decir cuál es la noción ni citar al ciclo.
4. **AICc con y sin media** — `c3-m9-24` y `c3-m10-15` [DISCREPA]: «el AICc no compara modelos… con y sin media». FPP3 §9.7
   (arima.txt:424–432) decide la constante comparando AICc, y §9.6 (l. 398) cuenta k=1 si c≠0. El aviso con distinto d (l. 404) sí es suyo.
5. **El puente con las redes neuronales** — `c3-m10-08` [ERROR]: «|w|<1 para que el gradiente no explote **ni se desvanezca**»; con |w|<1
   el gradiente w^k **se desvanece**, y la frase siguiente del capítulo lo dice. `c3-m10-07`: h_t=w h_{t−1}+u x_t es un filtro de la
   entrada, no un AR(1) salvo que x_t sea ruido blanco. `c3-m10-10` [TENSIÓN]: «intervalos calibrados» frente a FPP3 (arima.txt:629:
   «tend to be too narrow») y al propio Módulo 9; `c3-m10-12` [TENSIÓN]: los benchmarks de FPP3 son media, ingenuo, ingenuo estacional y
   deriva, no el ARMA; `c3-m10-04/05/06` atribuyen LSTM, GRU y Transformers sin obra; `c3-m10-14`: «suele estar mal» es empírica sin medición.
6. **Software afirmado** — comprobado en esta sesión (`diag/fuentes_comprobaciones_*.out`): `c3-m6-03` [ERROR] «para simular una caminata
   aleatoria hay que usar cumsum»: `arima.sim(list(order=c(0,1,0)))` la simula y la ayuda de R lo ejemplifica. `c3-m8-18` [ERROR de
   explicación]: R devuelve en `residuals()` las innovaciones **estandarizadas** (21.056 = 52.538/√6.22) y statsmodels las crudas
   (52.536); no «inicializan distinto». `c3-m3-13` (y `c3-m4-05`, `c3-m10-53`, `c3-m10-78`): «arima() devuelve **siempre** la
   invertible» solo vale con `transform.pars=TRUE`. `c3-m5-06`/`c3-m10-21`: aconseja `bartlett_confint=False` y la banda ±1.96/√n para
   hallar el corte de un MA(q), pero Cryer §6.1 (ec. 6.1.11) da Var(r_k)≈(1+2Σρ²)/n para k>q: la banda blanca es la estrecha. Las demás
   afirmaciones de software (`c3-m1-07/-11/-12/-18/-20`, `c3-m6-01/-04`, `c3-m7-16/-17/-18`) **sí** las respaldan la ayuda de R o la firma
   de statsmodels, pero ninguna tiene instantánea ni obra de software en la biblioteca (16 filas citan «statsmodels (documentación)»).
7. **Lecturas del Módulo 10** — `c3-m10-39/-40`: «Shumway cap. 3, secciones 3.1 a 3.5… con las manchas solares entre sus ejemplos»: la
   3.ª ed. (la única en caché) numera ARMA=3.2…estimación=3.6 y no tiene «sunspot» en su cap. 3 (ni la 4.ª, citada, está en disco).
   `c3-m10-41/-42`: Box et al. (5.ª ed. de 2015) como «la fuente original de la prueba de Ljung–Box» y «capítulos 3 y 6»: no es la fuente
   original (Ljung y Box 1978; Box y Pierce 1970 según Cryer §8.1) y la obra no está en disco. Las secciones de FPP3 (9.3, 9.4, 5.4)
   **sí** coinciden (`c3-m10-38`); §12.4 (NNETAR) no se pudo comprobar (cap. 12 sin extraer, `c3-m10-43`).
8. **Ljung–Box y Box–Pierce** — `c3-m8-10/-11`: `ljung1978measure` sin texto en caché; Cryer §8.1 (PDF p0194) respalda Q* y que Ljung y
   Box mejoraron a Box y Pierce, pero la fórmula Var(r̂_k)≈(T−k)/(T(T+2)) que justifica el factor **no aparece** en ninguna fuente leída.
9. **Cifras de simulación sin generador (norma 1)** — `c3-m7-11` (CSS pasa de 1 en un 4 % de mil simulaciones) y `c3-m8-15` (3000 series:
   4.9 % frente a 2.6 %) están solo en los bloques de código; ni `genera_cap3.R` ni `cap3_arma.json` las producen.
10. **La TRM** — `c3-m0-06`/`c3-m9-19`: sin ficha (mismo hueco que `c2-m6-08`), y la fecha de consulta del JSON (julio) no es la del bloque
    (junio). `c3-m9-17`: «allí quedó establecido que tiene una raíz unitaria» (Hamilton §15.4 sostiene que con muestra finita no se distingue una raíz unitaria de una cercana a 1).
    `c3-m9-22`: «coincide con la teoría de mercados eficientes para una tasa de cambio» (atribución a una teoría; FPP3 habla de bolsa).
    `c3-m9-26`: «en datos diarios de la misma tasa…»: el ejemplo de Cryer es un fondo (CREF), no una tasa de cambio.
11. **Las manchas solares** — `c3-m7-01`/`c3-m9-01`: «Wolf number» y «conteos». R ?sunspot.year no dice «Wolf» y Cryer p. 392 (PDF p0402) las
    define como índice ponderado; `c3-m9-03` «la transformación estabilizadora clásica para conteos» sin obra.
12. **Yule–Walker** — `c3-m7-06` y `c3-m10-59`: «solo sirve para AR puros»; Shumway (PDF p0136) dice «óptimo» para AR y Cryer (PDF p0162)
    «muy ineficiente» con términos MA: no que no sirva. `c3-m7-13`: «sesgado hacia el interior de la región estacionaria»: sin pasaje.
13. **El techo de ρ1 en un MA(q)** — `c3-m3-12`: cos(π/(q+2)) es verdad (comprobado numéricamente para q=1…4) y ninguna caché lo trae
    (todas dan solo q=1): derivarlo (propia) o citarlo.

## Atribuciones que el capítulo hace hoy sin cita

- **Yule y Walker**: las ecuaciones (`c3-m2-18`, `c3-m7-05`) y todo lo de las manchas (punto 1). `yule1927method` sin PDF; Walker (1931) no está.
- **Box y Jenkins**: el convenio de resta (`c3-m1-08/-09`), la parsimonia (`c3-m4-10`), el ciclo identificar-estimar-diagnosticar
  (`c3-m5-04`), «la metodología completa de Box–Jenkins» (`c3-m10-44`), el «modelo airline» (`c3-m1-04`, `c3-m4-15`; FPP3 no lo nombra).
  Las cuatro ediciones (1970, 1976, 1994, 2015) están en la biblioteca sin texto.
- **Ljung–Box y Box–Pierce**: `c3-m6-08`, `c3-m8-08/-09/-10`, `c3-m10-42`. **Hyndman–Khandakar**: `c3-m9-20`, `c3-m10-45` (FPP3 §9.7 lo respalda).
- **Guerrero** (`c3-m0-08`, `c3-m9-05`), **Shapiro–Wilk** (`c3-m9-14`), **ARCH/GARCH** (`c3-m9-28`; Cryer p. 285 nombra a Engle 1982),
  **Durbin–Levinson** (`c3-m0-07` y el comentario de la línea 7302; Cryer p. 115 lo respalda), **Bartlett** (`c3-m5-06`, sin nombrarlo).
- **No nombrados, aunque su resultado se usa**: Akaike, Schwarz y Hurvich–Tsai (el AIC, el BIC y el AICc de `c3-m8-01`; Cryer §6.5 atribuye
  los dos últimos), **Wold** (la MA(∞) de `c3-m4-01`; Hamilton Prop. 4.1, PDF p0124, «first proved by Wold (1938)»), Dickey–Fuller y
  Kwiatkowski et al. en el quiz (`c3-m10-72/-73`, `c3-m11-05`, repiten `c2-m6-xx`).
- **A una teoría o un estatus**: «mercados eficientes» (`c3-m9-22`), LSTM/GRU/Transformer (`c3-m10-04/-05`), «el ciclo solar documentado
  por los astrónomos» (cinco filas), «la transformación clásica para conteos» (`c3-m9-03`), «el AR es la idea original» (`c3-m10-47`).

## Obras que faltan

- **En la biblioteca pero sin texto en caché** (hoy no se pueden contrastar): `yule1927method`, `box1970time`/`box1976time`/`box1994time`/
  `box2016time`, `ljung1978measure`, `brockwell2016introduction`, `hyndman2008automatic`, `guerrero1993timeseries`,
  `kwiatkowski1992testing`. **Ejemplar equivocado**: Shumway y Stoffer, 4.ª ed. (la que se cita y se recomienda; la caché es la 3.ª, parcial).
- **No están en la biblioteca** (los nombres y años de las marcadas † son de memoria del inventariante: verificar en Crossref antes de dar
  de alta): Walker 1931†; Box y Pierce 1970 y Hurvich y Tsai 1989 (los cita Cryer, p. 131 y 183); Bartlett 1946 (Cryer, p. 110);
  Engle 1982 (Cryer, p. 285) y Bollerslev 1986†; Box y Cox 1964†; Shapiro y Wilk 1965†; Fama 1970† y literatura sobre tipos de cambio y
  caminata aleatoria; una fuente astronómica del ciclo solar (p. ej. SILSO†); Tong (1996) y Andrews y Herzberg (1985), que cita R para
  las manchas, y Diggle (1991) para `lh`; para el Módulo 10: Hochreiter y Schmidhuber 1997†, Cho et al. 2014†, Vaswani et al. 2017†,
  Pascanu, Mikolov y Bengio 2013† y Bengio et al. 1994†; una obra sobre la cota de ρ1 en un MA(q) (o declararla propia).
- **Datos y software** (colección «4 Datos y software»: hoy solo figura R): la TRM de datos.gov.co (conjunto 32sa-8pi3); `forecast`, `tseries`;
  `statsmodels` y `numpy` (16 y 1 filas). De las ayudas de R en `_local/web/rcoreteam2026r/` están `acf`, `ar`, `Box.test`, `plot.acf`,
  `sunspots`; **faltan** `arima`, `arima.sim`, `ARMAacf`, `ARMAtoMA`, `polyroot`, `lh`, `sunspot.year` y `shapiro.test`.
- **En caché y sin leer**: Cryer §8.3 (sobreajuste) y cap. 9 más allá de la ec. 9.3.45; Hamilton cap. 4–5 (pronóstico, máxima verosimilitud)
  y §15.3–15.4. **Sin extraer**: FPP3 caps. 7 (§7.5, AIC) y 12 (§12.4, NNETAR).

## Hallazgo colateral (no son de fuentes)

- **Encabezado que contradice el texto** (`c3-m9-27`, líneas 5558–5559): «Donde sí hay estructura: en el cuadrado», y el párrafo concluye que
  en la serie mensual **no** hay (p=0.9166).
- **El pie está escrito a mano** (líneas 2632–2660); en el capítulo 2 lo escribe `genera_referencias.py` desde `referencias.json`.
- **La TRM mensual es un promedio de diarios** (Módulo 9, caso 2; la serie es la del Capítulo 2), y el capítulo concluye «ruido blanco» y «mercado
  eficiente» sin mencionar el efecto del promedio: promediar un paseo aleatorio induce autocorrelación positiva en las primeras diferencias
  (ρ1≈0.25 con 21 días; simulado 0.254, `diag/fuentes_comprobaciones_r.out`), y el r1 observado es 0.105. No se afirma que el caso falle; la
  conclusión se apoya en una serie que ya no es el precio. La referencia habitual (Working 1960†) es de memoria: no entra sin leerla.
- **Redacción**: «diferenciar es dividir por el factor (1−B)» (`c3-m1-17`: es multiplicar, y el factor sale del polinomio); «ε_t es independiente
  de todo lo anterior» (`c3-m2-19`) frente al ruido blanco incorrelado del capítulo 2; «Q pondera mucho r̂1» (`c3-m8-19`: el peso de r̂1
  es el menor); «cada medición conserva el 57 % de la anterior» (`c3-m10-32`: de la desviación respecto de la media); «la prueba gana
  potencia» (`c3-m10-35`: no se aísla de que las ventanas largas cambian de régimen).
- **Logística del Módulo 11** (`c3-m11-01…03`): 30 minutos, diez preguntas, 35 %/65 % y variantes por estudiante son datos del curso, no de obra:
  confirmarlos contra el quiz real (el código del simulacro dice `minutos: 30`).
- **El quiz `cap3` y la actividad `parcial2`** están bien en lo aritmético (se comprobaron las cifras de los distractores a mano), salvo el
  «unos 8 periodos» de `c3-m10-76` (8.00 con la fórmula del capítulo, 8.69 con la de FPP3) y las opciones que dependen de «siempre
  invertible» (`c3-m10-53`) y de «solo sirve para AR» (`c3-m10-59`).

## Método y límites

Se leyeron en esta sesión: el HTML entero (módulos, JS con datos y comentarios, quizzes); la caché local de Cryer (502 páginas), Hamilton (815),
Shumway 3.ª ed. (203) y FPP3 caps. 1–5 y 9, con `grep` y lectura de los pasajes que cito; las ayudas de R 4.6.0 (`arima`, `arima.sim`,
`ARMAacf`, `ARMAtoMA`, `polyroot`, `Box.test`, `lh`, `sunspot.year`, `auto.arima`) y las firmas y docstrings de statsmodels 0.14.6, ejecutándolos.
De las ayudas solo se imprimen booleanos o firmas (`diag/fuentes_comprobaciones_r.out`, `_py.out`): no se copió texto. Cada fila se generó con
`fuentes_genera.py` (fuera de git, en `bibliografia/_local/herramientas/cap3/`, porque sus filas llevan citas literales), que **comprueba que `texto` sea subcadena exacta de una línea** y da `linea`; ids únicos, vocabulario cerrado y claves
de `referencias.json`. Las cifras numéricas de comprobación (λ de Guerrero, ceros de `sunspot.year`, residuales de R y statsmodels, cos(π/(q+2)),
periodos del AR(2), ARMA(2,2)≡ARMA(1,1)) se recalcularon en R/Python, no se tomaron de la prosa.

Límites: «hallado» es la lectura de quien inventarió y los pasajes los verifica otra persona. No se pudo leer Yule (1927), ninguna edición de Box y
Jenkins, Brockwell y Davis, Shumway 4.ª ed., ni FPP3 cap. 12: lo que depende de ellas va marcado `[NO COMPROBABLE]`, `[SIN LEER]` o `[SIN EXTRAER]`.
Los nombres y años de obras no leídas (†) son pistas, no citas. «Retirado en statsmodels 0.13» (`c3-m7-19`) no es verificable con la 0.14.6 instalada.
En `diagnostico/cap3/diag/` hay archivos de otras sesiones (ejercicios, gráficas, lector, par académico) que no se tocaron. No se editó el capítulo ni nada fuera de
`bibliografia/contraste/cap3_inventario.tsv`, este informe y `diag/fuentes_*`.
Reproducir: `python3 bibliografia/_local/herramientas/cap3/fuentes_genera.py` (con `--comprobar` no escribe), `fuentes_cuenta.py`, `Rscript …/fuentes_comprobaciones.R`,
`python3 …/fuentes_comprobaciones.py`.


> **Nota de la sesión maestra (2026-11-19).** Las citas literales en inglés que el inventario traía entre «» se
> sustituyeron por «[literal en _local]», como pide la norma de citas fuera de git del 17 de noviembre. El inventario
> completo está en `bibliografia/_local/herramientas/cap3/cap3_inventario_con_literales.tsv`, junto con los generadores.
