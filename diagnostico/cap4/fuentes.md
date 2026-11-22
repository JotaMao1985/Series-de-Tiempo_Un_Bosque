# Capítulo 4 · Afirmaciones que exigen fuente (diagnóstico, 2026-11-22)

Archivo leído: `Htmls_Series/capitulo-4-modelos-arima.html` (worktree en `71c42d8`): los doce módulos (`<template id="module-N">`),
el pie, los metadatos de la cabecera, el JS con los datos (`DATOS_CAP4`, `SERIES_CAP4`) y sus comentarios que atribuyen algo,
`TABLAS_RANKING['rejilla-nilo']`, `AUTOEVALUACIONES['cap4']` (8 preguntas) y `SIMULACROS['cap4-simulacro']` (10 preguntas), las
lecturas y los tres ejercicios. Inventario completo, una fila por afirmación: `bibliografia/contraste/cap4_inventario.tsv`
(357 filas, mismas columnas que los del capítulo 3; `hallado` y `r4` vacíos por encargo). No se inventariaron las cifras que
calcula R ni las derivaciones que el capítulo muestra paso a paso (propias); sí las frases que las enmarcan. Lo repetido
(resumen, autoevaluación, simulacro, repeticiones entre módulos) va en filas con `REPITE c4-…`; lo que ya está registrado en
`contraste/cap2.yml` o `cap3.yml`, con `= c2-…` / `= c3-…`.
El capítulo no tiene ningún `data-afirma` ni `cite.cita` (0 ocurrencias): todo lo que sigue va sin cita visible. Tampoco tiene los
marcadores `PIE-REFERENCIAS`: el pie está tecleado a mano (los capítulos 2 y 3 lo escriben desde `referencias.json`).
**Los capítulos 3 a 6 se ensamblan:** la fuente es `ensamblado/cap4/` (`templates_*.html`, `chapter.js`); las líneas del TSV son
las del HTML final.

## Recuentos

| tipo | alta | media | baja | total |
|---|---:|---:|---:|---:|
| definicion | 8 | 10 | 0 | 18 |
| resultado | 59 | 38 | 3 | 100 |
| regla | 58 | 39 | 7 | 104 |
| dato | 39 | 35 | 22 | 96 |
| atribucion | 17 | 9 | 5 | 31 |
| historica | 7 | 0 | 1 | 8 |
| **total** | **188** | **131** | **38** | **357** |

Por módulo: pie y metadatos 13 · M1 29 · M2 23 · M3 34 · M4 21 · M5 21 · M6 17 · M7 22 · M8 22 · M9 31 · M10 105 (caso del Nilo y de la
TRM 44, puente y resumen 16, ejercicios 13, lecturas y cierre 12, autoevaluación y tabla ordenable 19, nota del puente 1) ·
M11 14 (prosa 5, simulacro 9) · M12 5.

Estado de la búsqueda (clasificación del inventariante a partir de lo que dice `donde_buscar`, por
`python3 diagnostico/cap4/diag/fuentes_cuenta.py`; precedencia de arriba abajo):

| estado | alta | media | baja | total |
|---|---:|---:|---:|---:|
| respaldada en lo leído | 94 | 49 | 9 | 152 |
| parcial | 10 | 7 | 1 | 18 |
| con matiz o tensión | 33 | 5 | 0 | 38 |
| discrepa o error | 2 | 0 | 0 | 2 |
| no hallada en lo leído | 13 | 4 | 1 | 18 |
| no comprobable aquí (obra sin texto en disco o sin leer) | 11 | 9 | 3 | 23 |
| sin generador (norma 1) | 3 | 1 | 0 | 4 |
| propia o sin fuente necesaria | 5 | 27 | 12 | 44 |
| localizada, sin veredicto | 17 | 29 | 12 | 58 |

«Respaldada» = un pasaje leído respalda la afirmación; según la norma lo verifica alguien que no la redactó. Las rutas son
`ruta:línea` bajo `bibliografia/_local/` (`texto/<clave>/pNNNN.txt` es el archivo de página, «impr.» la página impresa de su
encabezado; `web/…` es FPP3 o una ayuda de R). Etiquetas de `donde_buscar`: `[DISCREPA]` 2 filas, `[TENSIÓN]` 7, `[CON-MATIZ]` 31,
`[NO HALLADO]` 22, `[PARCIAL]` 18, `[NO COMPROBABLE]` 24, `[SIN GENERADOR]` 4, `[EJEMPLAR]` 2, `[SIN LEER]` 1; 77 filas repiten una ya
registrada en los capítulos 2 o 3 y 89 repiten otra fila de este inventario.

Cuatro novedades de la caché respecto del inventario del capítulo 3: ya hay texto de **Hyndman y Khandakar (2008)** (22 páginas,
`texto/hyndman2008automatic/`) y de **Yule (1927)** (sin uso en este capítulo), y están extraídas las ayudas de R `AirPassengers`
(que sí nombra el «modelo airline» en sus ejemplos), `arima`, `arima.sim`, `Box.test` y `diff`. FPP3 está en los caps. 1–5, 7, 9 y 12.

## Lo que más pesa (ordenado por daño al estudiante)

1. **El umbral de raíces de `auto.arima`** — `c4-m7-09` y `c4-m10-21` [DISCREPA]. El capítulo enseña que el algoritmo descarta los
   modelos con alguna raíz de módulo menor que **1.01** (AICc = ∞) y lo atribuye a Hyndman y Khandakar (2008), que figuran en las lecturas.
   El artículo (`texto/hyndman2008automatic/p0011.txt:36-38`, impr. 11) dice **1.001**. Lo que sí es cierto: el código instalado de
   forecast 9.0.2 usa `minroot < 1 + 0.01` (comprobado, `diag/fuentes_comprobaciones_r.out`). El capítulo coincide con el código, no con
   la fuente que cita; el ARIMA(2,1,2) del Nilo (raíz AR de módulo 1.001) depende de ese umbral; el de la TRM (raíz MA de 1.0000) se descarta con cualquiera de los dos. Hay que declarar la fuente
   (el código) o citar el artículo con su cifra.
2. **La regla de la varianza para elegir d** — `c4-m3-04`, `c4-m8-07`, `c4-m10-53/-64/-67`, el Resumen, los ejercicios 1 y 2 y la pregunta
   10 del simulacro. Se presenta como «la regla habitual» y como una de las «tres evidencias» de d, pero ninguna fuente de la caché
   (Cryer §5.2 y §6.4, Shumway §3.8, FPP3 §9.1, H&K 2008, Hamilton) propone el mínimo de la varianza como criterio; H&K (p. 10) advierte
   que elegir d por criterio de información lleva a sobrediferenciar. [TENSIÓN con `c2-m7-08`]: el Capítulo 2 la registró como propia y
   dice que la varianza «no decide». Es lo que el estudiante aplicaría en el examen.
3. **La «regla de referencia habitual» de 2 puntos de AICc** — `c4-m6-08`, `c4-m7-14/-15`, `c4-m10-102` y la pregunta 7 de la
   autoevaluación: «diferencias menores que 2 no distinguen modelos». Sin obra que la traiga (Cryer §6.5, FPP3 §9.6–9.7, H&K 2008:
   ninguna da el umbral); atribuida a «lo habitual». Decide la lectura de todo el Módulo 7 («siete candidatos indistinguibles»).
4. **El Nilo: la presa, 1899 y Cobb** — `c4-m8-13`, `c4-m0-06`, `c4-m8-12`, `c4-m10-83/-84`, `c4-m1-16`. «El descenso coincide con la
   construcción de la presa baja de Asuán» [NO HALLADO]: la ayuda `?Nile` (ejecutada) cita a Cobb (1978, tabla 1, p. 249) y habla de un
   cambio aparente «cerca de 1898», no menciona ninguna presa; Cobb no tiene texto en caché. El capítulo fija 1899 y dice que Cobb
   «estableció» ese cambio. Es un hecho histórico-causal que el estudiante repetiría; viaja además en el JSON de datos.
5. **Lo que se atribuye a Box–Jenkins sin haberlos leído** — `c4-m2-17` y `c4-m8-17` («Box–Jenkins no tiene una etapa para detectar
   intervenciones», «los absorbe subiendo d») [NO HALLADO; Cryer cap. 11 trata la intervención y los atípicos como extensión, sin decir
   eso]; `c4-m2-02/-03` («el esqueleto de todo», «la familia ya existía, ellos fijaron cómo identificarla con ACF y PACF»: FPP3 y
   Cryer solo dicen que el texto «popularizó» el modelado y el método); `c4-m10-61/-62/-63/-80` (BJsales = «la Serie M» del «libro
   original»; `?BJsales` cita a Box y Jenkins 1976, p. 537, y no dice «Serie M»; el «modelo de libro» es un IMA(1,1): sin fuente);
   `c4-m10-77/-78/-79` (lecturas: capítulos 4 a 8 de la 5.ª ed.; secciones 3.4, 3.6 y 3.7 de la 4.ª de Shumway, cuando la 3.ª ed. de la
   caché numera 3.5, 3.7 y 3.8; la «fuente original» sería la de 1970, no la 5.ª ed.). Las cuatro ediciones de Box y Jenkins están en la
   biblioteca sin texto.
6. **Cifras sin generador (norma 1)** — `c4-m3-15` (PP.test rechaza el 100 % y `adf.test` el 51.3 % con raíz unitaria verdadera),
   `c4-m9-26` (cobertura del 80 % a un mes en la TRM: 83.9 %), `c4-m10-33` (asimetría 0.76) y `c4-m10-37` (rango 1.07–1.14): ni
   `genera_cap4.R` ni `cap4_arima.json` las producen (coincide con `diag/lector_cifras.out`). Las demás cifras de simulación (4.8 %, 70.8 %,
   44.5 %, 86.4 %…) sí salen de `mc_escalon` y de la malla del generador.
7. **Software afirmado con una explicación que la comprobación no respalda** — `c4-m10-71` y `c4-m9-31` [TENSIÓN]: el capítulo atribuye
   la diferencia de σ̂² entre `arima()` y `Arima()` a «CSS-ML frente a ML», pero `Arima(method="ML")` da el mismo σ̂² que su valor por
   defecto (20176.9) y `arima()` da 19769.3: la razón es 99/97, el reescalado por grados de libertad. `c4-m7-22`: statsmodels con
   `nobs_effective` da un AICc de 1267.471, no 1267.507, así que el descuento de d no explica la diferencia. `c4-m7-18`: el tope
   p+q ≤ 5 es del código (`max.order`); el artículo habla de cotas de 5 para p y q por separado. `c4-m10-44` (OPG frente a información
   observada) no tiene obra. Respaldadas por ejecución, aunque sin instantánea ni obra de software en la biblioteca: `c4-m5-10` a
   `c4-m5-14` (defaults de `arima`, `Arima`, `auto.arima` y `ARIMA`), `c4-m3-10` a `c4-m3-13` (`ndiffs`, ADF de `urca`, −2.89),
   `c4-m3-28/-29` (KPSS de statsmodels y de tseries), `c4-m4-20` (`pacf`), `c4-m6-16` (`nobs_effective`).
8. **La teoría financiera** — `c4-m10-24` [NO HALLADO]: «coincide con lo que predice la teoría financiera: si el tipo de cambio fuera
   predecible, alguien ya habría arbitrado» es una atribución a una teoría sin nombre ni obra (FPP3 solo dice que las caminatas aleatorias
   se usan mucho con datos financieros; repite `c3-m9-22`). Con ella, `c4-m10-34` (marzo de 2020 y julio de 2022 como «devaluaciones»).
9. **«Cancelación casi exacta de raíces … síntoma clásico de sobrediferenciación»** — `c4-m1-24/-25` [CON-MATIZ], base de la «anomalía»
   del Módulo 1 que cierran los Módulos 8 y 10. Cryer (p. 126-127) liga la sobrediferenciación con la raíz del MA en 1 y Cryer §8.2 /
   Hamilton p. 60 definen la redundancia de parámetros (factor común), pero ninguna llama «síntoma clásico» al cuasi factor común.
10. **La forma del pronóstico «la deciden d y la constante, no los coeficientes ARMA»** — `c4-m2-15`, `c4-m9-01`, `c4-m10-59`. La
    tabla de c y d está en FPP3 §9.5 (`arima.txt:311-325`) y respalda el grueso; [CON-MATIZ] la misma sección dice que p importa si hay
    ciclos (l. 328), y el módulo la presenta sin esa salvedad.
11. **ARIMA y suavizamiento exponencial** — `c4-m1-12/-13/-14`: las equivalencias α = 1+θ y ARIMA(0,2,2) ↔ Holt están en FPP3 Tabla 9.4
    (con Holt = ETS(A,A,N)); «no hay dos teorías, hay una» y «las herramientas de este capítulo se aplican también a ellos» exceden el
    pasaje: FPP3 y H&K (2008, p. 11–12) dicen que las clases se solapan y son complementarias y que el AICc no compara ETS con ARIMA.
12. **Intervalos «sistemáticamente optimistas» y «la normalidad no hace falta para las estimaciones»** — `c4-m9-27`, `c4-m9-24`,
    `c4-m2-12`: FPP3 dice que «tienden a ser demasiado estrechos» por no contar la variación de los parámetros ni del orden
    (respaldada, con matiz de fuerza); que las estimaciones de un ARIMA no necesiten normalidad no lo afirma ninguna fuente leída [PARCIAL].
13. **Parsimonia y la elección de d** — `c4-m10-88`: la opción distractora dice que d no se elige por parsimonia; Cryer §6.4 (p. 128)
    invoca precisamente la parsimonia para no sobrediferenciar [CON-MATIZ].

Lo que sí sostienen las fuentes y conviene citar en la ronda de fuentes (candidatas con su localizador): la tabla de c y d
(FPP3 §9.5, `arima.txt:317-322`); que la verosimilitud no es comparable entre d (FPP3 §9.6, l. 404 y 851; `?arima`, l. 132-133 y 161-171,
dice que la verosimilitud es la de los datos diferenciados); las fórmulas de AIC/AICc/BIC (FPP3 §9.6; Cryer §6.5, p. 130-131); el
algoritmo de H&K (artículo, pp. 9-12; FPP3 §9.7); la sobrediferenciación (Cryer p. 126-127; Shumway §3.8, p. 145); los pesos ψ y la
varianza del pronóstico (Cryer §9.3, p. 201-202; FPP3 §9.8); la no invertibilidad en el pronóstico (Cryer §9.3, p. 197); el PP con θ
cercano a −1 (Hamilton p. 515-516); el valor crítico −2.89 (Hamilton Tabla B.6, p. 763); la ACF/PACF sobre datos diferenciados (FPP3
§9.5; Shumway §3.8); el BIC consistente y el AICc con n efectivo (Cryer §6.5).

## Atribuciones que el capítulo hace hoy sin cita

- **Box y Jenkins**: el año 1970 y el título (`c4-m2-01`; respaldado por FPP3 §9.12 y por el prefacio de Cryer), el «esqueleto» y las
  aportaciones (`c4-m2-02/-03`), el convenio de resta (`c4-m1-26`), el ciclo identificar-estimar-diagnosticar (`c4-m2-04`, resumen
  `c4-m10-52`), «no tiene etapa para intervenciones» (`c4-m2-17`, `c4-m8-17`), el modelo airline (`c4-m10-48`; `?AirPassengers` y Cryer
  p. 240 lo respaldan y lo ligan a Box y Jenkins), la Serie M/BJsales (`c4-m10-61/-62/-63`).
- **Hyndman y Khandakar (2008)**: el algoritmo y sus pasos (`c4-m7-01` a `-09`); el artículo ya está en caché y respalda casi todo salvo el
  umbral de las raíces (punto 1) y el «quinto» modelo inicial.
- **Cobb (1978)**: `c4-m0-05`, `c4-m1-16`, `c4-m8-12/-13`, `c4-m10-83/-84` (sin texto; `?Nile` lo cita).
- **Phillips y Perron, Dickey y Fuller, Kwiatkowski et al. (KPSS)**: se nombran las pruebas (ADF, PP, KPSS) sin una sola cita; PP, ADF y
  el −2.89 tienen respaldo en Hamilton (§17.6, Tabla B.6); KPSS no tiene texto (`c4-m3-05/-08/-17/-19/-21/-22/-30`).
- **Ljung y Box** (`c4-m2-21`; Cryer p. 183-184 y `?Box.test` lo respaldan), **Shapiro–Wilk** (`c4-m8-02`, [= c3-m9-14]),
  **Bartlett** (el estimador de la varianza de largo plazo, `c4-m3-30`), **Holt** (`c4-m1-13`, `c4-m11-09`), **Durbin–Levinson** (`c4-m0-10`),
  **Yule–Walker** (solo en el simulacro, `c4-m11-14`): epónimos sin cita.
- **Shumway y Stoffer, Box et al., Brockwell y Davis, FPP2** en el pie y las lecturas (`c4-m0-02` a `-04`, `c4-m10-75` a `-79`).
- **A una teoría o un estatus**: «teoría financiera» (`c4-m10-24`), «la regla habitual» de la varianza y la de 2 puntos de AICc
  (puntos 2 y 3), «el ciclo de unos 10 años» del lince (`c4-m10-66`: `?lynx` no da el periodo y FPP3 habla de ciclos aperiódicos),
  «la recomendación habitual es el AICc» (`c4-m6-14`: es la de FPP3), «el error de principiante más caro» (`c4-m4-04`).

## Obras que faltan

- **En la biblioteca pero sin texto en caché** (hoy no se pueden contrastar): `box1970time`, `box1976time`, `box1994time`, `box2016time`
  (lecturas, «Serie M», airline, convenio de resta, intervenciones); `cobb1978problem` (el cambio de nivel del Nilo y su causa);
  `kwiatkowski1992testing` (KPSS: estadístico, valor crítico 0.463, estimador de Bartlett); `ljung1978measure`; `brockwell2016introduction`;
  `hyndman2018forecasting` (FPP2, capítulo 8); `guerrero1993timeseries` (comentario del JS). **Ejemplar equivocado**: `shumway2017time`
  (4.ª ed.), la que se cita y se recomienda; la caché es la 3.ª ed. parcial.
- **No están en la biblioteca** y aparecen en lo leído: Phillips (1987) y Phillips y Perron (1988) (Hamilton §17.6); Fuller (1976)
  (Hamilton, Tabla B.6); Box y Pierce (1970) (`?Box.test`); Hurvich y Tsai (1989) (Cryer §6.5); Dickey y Fuller (1981) (H&K 2008, p. 10);
  Campbell y Perron (1991) y Schwert (1989) (Hamilton p. 516). Para el Módulo 10, si se quisiera nombrar la teoría financiera, una obra
  sobre ella, y para el Nilo y la presa, una fuente histórica (hoy el capítulo no la tiene).
- **Datos y software** (colección «4 Datos y software»: hoy solo figura R): la TRM de datos.gov.co (conjunto 32sa-8pi3; `c4-m0-07`,
  `c4-m5-21`, `c4-m10-09/-39`); `forecast` (24 filas), `tseries` (11), `statsmodels` (23), `urca` (3), `numpy` (1) y `pmdarima` (2, [NO
  COMPROBABLE]: no está instalado). Ayudas de R sin instantánea: `Nile`, `lynx`, `BJsales`, `auto.arima`, `Arima`, `ndiffs`, `nsdiffs`,
  `adf.test`, `kpss.test`, `pp.test`, `checkresiduals` (las de `arima`, `arima.sim`, `Box.test`, `diff`, `AirPassengers` y `shapiro.test` ya están).
  La numeración de FPP3: faltan por extraer el cap. 8 (suavizamiento exponencial: SES y Holt) y el cap. 10 (regresión dinámica).
- **En caché y sin leer en esta sesión**: Cryer cap. 12 más allá de lo citado (ARCH), Hamilton caps. 4–5 y §15.3–15.4, Shumway 3.ª ed.
  fuera de §3.7–3.8 y del índice; H&K 2008 §4 salvo la pág. 15–16.

## Hallazgos colaterales (no son de fuentes)

- **Logística vencida** (`c4-m11-01`, `c4-m12-01/-02`): el Módulo 11 describe en presente un quiz con «40 minutos» y el Módulo 12 el
  Parcial 2 «del miércoles 14 de octubre, unos 70 minutos»; hoy es 22 de noviembre. Los 40 minutos del quiz coinciden con el código del
  simulacro pero figuran como pendientes de confirmar en el seguimiento del quiz del capítulo: confirmarlos contra el quiz real.
- **Referencias del pie y de las lecturas**: Hyndman y Khandakar (2008) y Cobb (1978) se recomiendan en las lecturas y no están en el pie
  (que lista solo FPP3, Shumway y Stoffer, Box et al. y Brockwell y Davis).
- **El JSON de datos lleva la atribución de la presa** (`cambio_nivel.fuente` en `genera_cap4.R`); corregir el texto sin corregir el
  generador la devuelve al reensamblar.
- **Cifras de otro capítulo**: la cobertura del 89.6 % que `c4-m10-36` toma del Capítulo 6 se verificó en
  `capitulo-6-pronostico-evaluacion.html:4539` (naïve, TRM, h = 12).
- **El comentario de la línea 3199** («cada programa inicializa el filtro a su manera») y los de las líneas 3692 y 5344 hablan del primer
  residual de R frente al de statsmodels: está en el registro del capítulo 3 como propia (`c3-m8-18`).

## Método y límites

Se leyeron en esta sesión: el HTML entero (módulos, JS con datos y comentarios, quizzes, simulacro); en la caché local, FPP3 §9.1–9.10 y
§9.12 (`arima.txt` completo), §5.2–5.5 y §5.8 (`toolbox.txt`), §7.5 (`regression.txt`) y §2.9 (`graphics.txt`); Cryer §1.2, §5.2, §6.1,
§6.4–6.5, §8.2, §9.1–9.4, §10.4, el índice del cap. 11 y las páginas 281–285 del cap. 12; Hamilton §3.5, §17.6 (con el encabezado de §17.7) y la Tabla B.6; Shumway 3.ª ed. §3.7–3.8 y el índice;
Hyndman y Khandakar (2008) §3 y p. 15–16; las ayudas de R extraídas (`arima`, `arima.sim`, `Box.test`, `diff`, `AirPassengers`, `shapiro.test`,
`acf`) y, ejecutándolas, las de `Nile`, `lynx`, `BJsales`, `ndiffs`, `auto.arima`, `Arima`, `adf.test`, `kpss.test`, `pp.test`. Las
comprobaciones de software corrieron en R 4.6.0 (forecast 9.0.2, tseries 0.10.62, urca 1.3.4) y Python (statsmodels 0.14.6, numpy 2.2.6);
de las ayudas solo se imprimen booleanos o cifras (`diag/fuentes_comprobaciones_r.out`, `_py.out`): no se copió texto. Cada fila se
construyó con una comprobación de que `texto` es subcadena exacta de una línea del HTML (sin etiquetas) y de que las claves están en
`referencias.json` (`diag/fuentes_valida.py`, 357 filas, 0 problemas). Las cifras de comprobación citadas (umbral 1.01, razón 99/97,
AICc 1267.471, medias 1097.75 y 849.97, valor crítico −2.89, y el resto) se recalcularon, no se tomaron de la prosa.

Límites: «hallado» es la lectura de quien inventarió y los pasajes los verifica otra persona. Los ejemplares de Hamilton, Cryer y H&K
2008 son escaneos o PDF con erratas: ninguna cita literal va en el TSV ni aquí; los localizadores `pNNNN.txt:línea` son de la caché de esta
copia de trabajo. Las páginas de Cryer, Hamilton y Shumway que figuran en filas `= c2-…`/`= c3-…` se tomaron del registro de esos capítulos y no
se releyeron una a una. No se pudo leer ninguna edición de Box y Jenkins, Cobb, Kwiatkowski et al., Brockwell y Davis, FPP2, ni la
documentación de statsmodels, `tseries` y `urca` (solo se ejecutaron). El inventario no juzga la corrección matemática, el estilo ni las
gráficas; las señales de «matiz» y «tensión» son de fuente, no de corrección. No se editó el capítulo ni nada fuera de
`bibliografia/contraste/cap4_inventario.tsv` y `diagnostico/cap4/` (archivos `fuentes.md` y `diag/fuentes_*`); en `diagnostico/cap4/diag/` hay
archivos de otras sesiones (ejercicios, gráficas, lector, par académico) que no se tocaron.

Reproducir (desde la raíz del repo): `python3 diagnostico/cap4/diag/fuentes_valida.py`, `python3 diagnostico/cap4/diag/fuentes_cuenta.py`,
`Rscript diagnostico/cap4/diag/fuentes_comprobaciones.R`, `python3 diagnostico/cap4/diag/fuentes_comprobaciones.py`.
