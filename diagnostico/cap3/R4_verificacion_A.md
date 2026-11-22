# Capítulo 3 · ronda R4 «fuentes» · verificación independiente, lote A (M1–M6)

Fecha: 2026-11-21. Verificador independiente A (subagente, contexto limpio): no redactó nada de esta ronda.
Leyó `CLAUDE.md`, `bibliografia/README.md` y `diagnostico/cap2/R4_verificacion.md`. **No leyó
`diagnostico/cap3/R4_cambios.md` hasta terminar las secciones 1 a 6**; la 7 es la comparación.

No tocó nada fuera de `diagnostico/cap3/`: ni prosa, ni `bibliografia/contraste/cap3.yml` (no puse
`verificado_por`; las firmas van en `comprobaciones/v4_firmas_A.txt`). Sin commits. Reejecuté la cadena de
ensamblado (escribe los HTML de los caps. 3–6), que dejó los cuatro archivos con la misma huella md5 que antes.

## 1. Resultado

| | entradas |
|---|---|
| Lote (c3-m1-* a c3-m6-*) | 97: 67 `respaldada`, 19 `con-matiz`, 11 `propia`, 0 `pendiente` |
| **Firmadas** | **93**: 64 `respaldada`, 18 `con-matiz`, 11 `propia` |
| **Sin firmar** | **4**: c3-m6-07 (error, §2), c3-m1-15, c3-m5-13 y c3-m6-08 (juicios, §3) |

Método por entrada (`comprobaciones/v4A_vuelca.py` → `v4A_vuelca.out`): el texto de la afirmación **tal como
está hoy** en el HTML (con su `hash_texto`: los 97 coinciden), sus citas visibles, el literal de
`_local/citas/cap3.yml` y ±500 caracteres de la fuente alrededor del literal, en la página del PDF indicada (y,
si no está ahí, en la siguiente) o en la sección de FPP3 o de la ayuda de R acotada como la acota el auditor. Leí
cada pasaje y lo comparé con la afirmación en su párrafo. Los cuatro literales que caen en la página siguiente son
todos de rangos `pp. N–N+1` (c3-m1-04, c3-m2-12, c3-m2-15, c3-m2-16): es lo esperado. Comprobé además el número
de página impreso de las 56 páginas de PDF citadas (cabecera de Cryer y Chan y de Shumway y Stoffer; pie de
Hamilton, desfase 15): todas coinciden con el localizador.

Las 11 `propia` las repetí ejecutando (R 4.6.0; Python 3 con statsmodels 0.14.6, numpy 2.2.6, scipy 1.15.3):
`comprobaciones/v4A_software.R` → `.out` y `v4A_software.py` → `v4A_software_py.out`. También recalculé las cifras
de las entradas citables (pseudo-periodos, γ0 del AR(2), PACF del MA(1), pesos π, cifras del ARMA(1,1) y del
ARMA(2,1)). Todo coincide con lo impreso: ver §5.

## 2. Errores (la frase, con su cita visible, enseña algo que la fuente no dice)

| id | qué dice la frase | qué dice la fuente | qué falla | propuesta |
|---|---|---|---|---|
| **c3-m6-07** (`con-matiz`) | «Ver uno o dos picos fuera de la banda no basta como evidencia (Hyndman y Athanasopoulos, 2021, §2.9);» | FPP3 §2.9 (`web/hyndman2021forecasting/graphics.txt`, el párrafo del ruido blanco): si **una o más barras grandes** quedan fuera de la banda, o bastante más del 5 %, la serie probablemente no es ruido blanco | La fuente citada dice lo contrario para un pico grande: un solo pico grande **sí** es evidencia. La frase no distingue tamaño y la cita va pegada a ella; un estudiante con r₁ = 0.5 y T = 200 concluiría que «no basta». La nota lo reconoce («no habla de la gravedad del pico, que es lo que FPP3 distingue») y aun así deja la cita. El registro de cambios dice «misma corrección que c2-m2-08», pero c2-m2-08 quedó «Una barra que **apenas asoma** fuera de la banda no basta como evidencia; **una barra muy grande, o un patrón, sí**»: aquí faltan las dos piezas | **Reescribir** como en el cap. 2: «Uno o dos picos que apenas asoman fuera de la banda no bastan como evidencia; uno muy grande, o muchos más del 5 %, sí». Con eso, `respaldada` |

## 3. Juicios (el veredicto o el localizador deberían cambiar)

Criterio: el del verificador del cap. 2 y del README. `con-matiz` cuando la fuente apoya la idea pero difiere en un
detalle; cada parte de la frase con su obra en `fuentes`; la cita visible tiene que llevar al lector a un pasaje
que diga lo que la frase dice.

| id | qué dice la frase | qué dice la fuente | qué falla | propuesta |
|---|---|---|---|---|
| J1 · **c3-m1-15** (`respaldada`) | «Con \|φ\| > 1 existe otra, estacionaria pero escrita con los choques futuros, …: no sirve para pronosticar y por eso queda fuera (Cryer y Chan, 2008, ejercicio 4.16). Con \|φ\| = 1 no hay ninguna.» | Cryer y Chan, ejercicio 4.16 (`texto/cryer2008time/p0095.txt`): (b) pide demostrar que es estacionaria y (c) **pregunta** «In what way is this solution unsatisfactory?»; no da la respuesta. «Inútil porque exige conocer el futuro para predecir el futuro» está en Shumway y Stoffer **3.ª**, p. 88, que no puede citarse a la vista. Lo de \|φ\| = 1 es el ejercicio **4.15**, que la nota invoca pero **no está en `fuentes`** | La cita visible manda a una pregunta, no a la afirmación «no sirve para pronosticar»; y la última oración no tiene obra en `fuentes` | **`con-matiz`** con esa nota («la razón —dependencia del futuro— es de Shumway y Stoffer 3.ª; Cryer y Chan solo la plantean como pregunta»), y **añadir** el ejercicio 4.15 (ya registrado como fuente 2 de c3-m1-35) con cita visible tras «no hay ninguna» |
| J2 · **c3-m5-13** (`respaldada`) | Recuadro «Media y autocovarianzas de un ARMA(p,q) estacionario: μ = c/(1−φ1−…−φp), γk = σ²Σψjψj+k, γ0 = σ²Σψj² (Cryer y Chan, 2008, p. 56)» | Cryer y Chan p. 56 (`p0069.txt`): γk del proceso lineal general **con media cero** (un proceso de media μ distinta de cero se obtiene sumándole μ); Hamilton p. 52 (fuente 2): media μ del MA(∞). La fórmula **μ = c/(1−Σφ)** del ARMA está en Hamilton **p. 60** (`p0075.txt`, antes de la ec. 3.5.4), que la nota menciona pero **no está en `fuentes`** | Localizador incompleto: la primera línea del recuadro no está en ninguna de las dos páginas registradas | **Añadir** Hamilton p. 60 a `fuentes` (el pasaje ya está registrado en c3-m5-01, fuente 2) y su cita visible junto a la cita de Cryer y Chan |
| J3 · **c3-m6-08** (`respaldada`) | «por eso existe la prueba de Ljung–Box del Módulo 8, que evalúa **todos los rezagos** a la vez (Hyndman y Athanasopoulos, 2021, §5.4)» | FPP3 §5.4 (`toolbox.txt`): la prueba de grupo contrasta «the **first ℓ** autocorrelations»; recomienda ℓ = 10 o 2m y avisa de que no funciona bien con ℓ grande | «Todos los rezagos» es más que la fuente (y que la propia `afirmacion` del registro, que dice «las primeras autocorrelaciones»). Un estudiante puede creer que la prueba mira cualquier rezago | «…que evalúa a la vez los primeros ℓ rezagos» (o «esos 20 rezagos a la vez»). Con eso, `respaldada` |

## 4. Fuera de las entradas

**Atribuciones sin marca en M1–M6** (`comprobaciones/v4A_sin_marca.py`: prosa fuera de todo `data-afirma` con
nombres de autores, software, «se llama», «siempre», «en la práctica»…; 52 líneas revisadas a mano, la mayoría
código o listas de fuentes). No encontré ninguna atribución a una obra sin marca. Quedan sin marca, y son
aceptables como convenciones o consejo del capítulo:

- `capitulo-3…html:2946`: «el de este capítulo, el de R y el de statsmodels» (convenio de suma); repite lo que
  marca c3-m1-07 unas líneas antes.
- `:4148`: «En la práctica se propone un modelo pequeño, se diagnostica y se compara por criterios de información»
  (la nota de c3-m5-12 lo declara consejo del capítulo; FPP3 §9.7 lo respaldaría si se quisiera marcar).
- `:3432`: el titular «Un MA siempre es estacionario» repite c3-m3-03.

**Cambios de prosa de la ronda en M1–M6** (`comprobaciones/v4A_difprosa.py`: prosa de HEAD contra la de hoy, sin
marcas ni citas). Leí los cambios uno por uno: todos acercan la frase a la fuente y ninguno introduce un error, salvo
c3-m6-07 (§2), que quedó a medio camino. La única cifra nueva es la de la PACF del MA(1) en el M3 (0.4878, −0.3123,
0.2215, −0.1652 con θ = 0.8 y las mismas magnitudes, todas negativas, con θ = −0.8): **sale igual de
`ARMAacf(ma = ±0.8, pacf = TRUE)`** y de la fórmula de Cryer y Chan (6.2.6) con el signo cambiado. Ningún cambio
pasa a la segunda persona; lo que la ronda modificó («el software, por defecto, te devuelve…», c3-m4-31) ya tuteaba.

**Voz** (no es de esta ronda; para quien cierre el capítulo): siguen en segunda persona, dentro de afirmaciones
marcadas de prosa expositiva, c3-m1-04 («que verás»), c3-m2-30 («si sustituyes… tienes»), c3-m3-11 («ves…
quisieras»), c3-m4-31 («te devuelve»), c3-m5-08 («envuélvelo»), c3-m5-18 («veas… recuerda»), c3-m5-20 («Si ves…
prueba») y c3-m6-06 («Si miras… esperas»). La convención (voz impersonal; el «tú» solo en intros de simuladores y
enunciados) las deja fuera de lo permitido salvo las que están en intros de simulador.

## 5. Observaciones sobre entradas firmadas (no impiden la firma)

- **c3-m3-15**: «…o, lo que es lo mismo, el último coeficiente de la regresión de y_t sobre sus k valores
  anteriores (Hamilton, 1994, p. 111)». Hamilton habla de la **proyección lineal** poblacional, y la nota lo dice; es
  la misma frase que el verificador del cap. 2 marcó en c2-m4-05 (con datos, el último coeficiente de una regresión
  por MCO no coincide con `pacf()`). Aquí el párrafo es teórico y firmo, pero «proyección lineal (la regresión
  poblacional)» evitaría la lectura muestral.
- **c3-m1-07**: la cita visible «(R Core Team, 2026, §Details)» no dice de qué página de ayuda es, y la frase no
  nombra `arima()`: el estudiante no puede encontrar el pasaje. Lo mismo, con menos daño, en c3-m1-12 y c3-m5-10,
  donde la frase sí nombra las funciones. Es un límite del vocabulario de localizadores (§Sección sin página), no
  de esta entrada.
- **c3-m5-20**: el pasaje que respalda «φ̂1 ≈ −θ̂1» es Hamilton p. 60 («If we are using an ARMA(1,1) model in
  which θ1 is close to −φ1…»), que está en `fuentes` pero no a la vista; la cita visible es Cryer y Chan p. 187,
  que da el consejo general. Convendría la segunda cita visible.
- **c3-m1-01**: la `afirmacion` del registro menciona la letra L de Hamilton, pero el texto marcado no la nombra
  (solo el titular «(lag operator)», fuera de la marca). Es inocuo.
- **c3-m1-16**: `tipo: historica`, pero la frase ya no afirma el origen del nombre; sería `definicion`.
- **c3-m5-32** (`propia`): además de repetir el ajuste (ar1 0.8300 ± 0.2307, ma1 −0.7953 ± 0.2477, aviso
  `optim code = 1`, suma 0.0347), comprobé «la verosimilitud es casi plana» y «valores muy distintos de (φ,θ) dan
  ajustes casi idénticos»: fijando φ en −0.5, 0, 0.3, 0.5 y 0.83 y optimizando el resto, el log-verosímil va de
  −273.44 a −273.07, y el del ruido blanco es −273.44.
- **c3-m1-15** (sin firmar) arrastra la observación de su nota sobre Hamilton p. 53: es cierta
  (`p0068.txt:12–13`: para |φ| ≥ 1 «there does not exist a covariance-stationary process»), y contradice el
  ejercicio 4.16 de Cryer y Chan; el capítulo sigue a Cryer y Chan, bien.

## 6. Comprobaciones globales

| Comprobación | Resultado | Salida |
|---|---|---|
| `python3 precalculo/audita_citas.py` | **Falla solo con F08: 172 hallazgos, todos F08** (las 172 entradas citables del cap. 3 sin `verificado_por`). Ningún otro código: F05 limpio, 586 citas literales comprobadas contra la fuente, 0 sin caché, 0 sin literal local. Los 6 F07 de Yule que cuenta `R4_cambios.md` ya no salen (la ficha se corrigió después). A01 = 78 y A02 = 10 son avisos; en M1–M6 los A01 son solo las listas de fuentes y el titular «Las ecuaciones de Yule–Walker» | `v4A_audita.out`, `v4A_audita_avisos.out` |
| Cadena: `ensambla_cap3.py` y luego 4, 5 y 6 | `ensambla_cap3.py`: «reproducible byte a byte». Tras los cuatro, **md5 idéntico** en los caps. 3–6 al de antes de correrlos, y `git diff --stat HEAD -- Htmls_Series` muestra **solo el capítulo 3** | `v4A_cadena.out` |
| Retirada de la «1b» de `ensambla_cap3.py` y protección en `ensambla_cap4.py` | **Correcta.** La «1b» ya no recorta el CSS ni teclea el pie: solo comprueba que el armazón del cap. 2 traiga una vez cada pieza (CSS `.cita`, `.fuentes-modulo`, `.lista-fuentes` y los marcadores PIE-REFERENCIAS) y aborta si no; la 9b pasa `genera_referencias.genera()` y exige marcas `c3-`, citas, listas de módulo, una sola lista del capítulo y ninguna cita vacía. La sección 0 de `ensambla_cap4.py` hace lo que hacía la «1b» (mismo pie tecleado, mismos marcadores, aborta si faltan o están en orden inverso), y su comentario dice cuándo se borra: **«CUANDO EL CAPÍTULO 4 HAGA SU RONDA DE FUENTES, esta sección se borra… y la protección baja a `ensambla_cap5.py`»**. La prueba de que basta es la de la fila anterior: caps. 4–6 iguales byte a byte | `git diff HEAD -- ensamblado/ensambla_cap3.py ensamblado/ensambla_cap4.py` |
| `verifica_bloques_cap6.py --html capitulo-3…` | **732 de 732 cifras, 0 bloques con discrepancias**; el «write failed» final es el previo; `precalculo/serie.csv` no apareció | `v4A_bloques_cap3.out` |
| HTTP: `python3 -m http.server 8853` sobre `Htmls_Series/` (misma md5 que el disco) + Chrome sin ventana por CDP (puerto 9353), M1–M6 a 1200 y 375 px, arnés propio `v4A_recorrido.js` | En los 12 casos: **todas las citas compuestas «(Autor, año, loc)» con el loc de su `data-loc`** (109 citas por ancho: 23, 20, 22, 15, 24 y 5), **0 enlaces sin destino, 0 destinos fuera de la lista «Fuentes citadas en este módulo» de ese módulo**, y cada lista tiene exactamente las obras citadas en su módulo (4, 4, 3, 3, 4 y 2); 0 espacios antes de puntuación tras una cita; 0 `.katex-error`, 0 «$» sin componer; `scrollWidth` 1200/1200 y **375/375** (medido contra el ancho fijado, no contra `innerWidth`); pie generado con las 4 obras básicas. La lista del capítulo está en el M10 (lote B). Único evento de consola: el 404 de `favicon.ico` del servidor. Servidor y Chrome detenidos al terminar | `v4A_recorrido.out`, `.json` |

## 7. Comparación con `R4_cambios.md` (leído después de lo anterior)

- **c3-m6-07**: el registro de cambios presenta la reescritura como «misma corrección que c2-m2-08». No lo es: la
  del cap. 2 conserva «que apenas asoma» y añade «una barra muy grande, o un patrón, sí». Por eso la frase sigue
  contradiciendo la fuente citada (§2).
- **c3-m1-15**: el registro de cambios lo deja `respaldada` con Shumway y Stoffer 3.ª como fuente adicional y anota
  en «pendiente» que la 4.ª ed. pasaría a cita visible lo que hoy respalda la 3.ª. Coincide con mi J1: hoy la
  cita visible (ejercicio 4.16) no dice «no sirve para pronosticar»; mientras no llegue la 4.ª, `con-matiz`.
- **c3-m5-13** y **c3-m6-08**: no aparecen en el registro de cambios como problema. En c3-m6-08 la `afirmacion` del
  registro («las primeras autocorrelaciones») está bien y la prosa («todos los rezagos») no: la ronda corrigió el
  registro y no la frase.
- **Punto 11 del registro de cambios** («no revisé una a una, contra la caché, las 213 propuestas de los
  lectores»): en M1–M6 la revisión una a una encuentra 1 error y 3 juicios en 97 entradas. Las 93 restantes las
  firmo tras leer cada pasaje.
- **Punto 6** (techo cos(π/(q+2)), c3-m3-12): lo repetí por valores propios en R (q = 1…4) y por optimización
  numérica en Python; coincide. Sigue sin derivación en el capítulo, como dice el registro.
- **Comprobaciones**: coinciden con las mías (732/732, cadena byte a byte, recorrido limpio), salvo el
  `audita_citas.py`, que hoy da 172 F08 y ningún F07 (el registro de cambios contaba 6 F07 de Yule, ya resueltos).
  Mi recorrido mide el desborde contra el ancho fijado y comprueba que cada enlace caiga en la lista **de su
  módulo**, no solo que exista; el resultado es el mismo.
- El registro de cambios dice «ninguna cifra calculada nueva» en la prosa. En M1–M6 entran las cuatro cifras de la
  PACF del MA(1) en el M3. Ya estaban en el simulador y en la nota de c3-m3-14, salen de `ARMAacf` y las repetí: no
  es un error, pero son cifras que la ronda llevó a la prosa.

## 8. Guiones y salidas (todos en `comprobaciones/`)

`v4A_vuelca.py` / `.out` (afirmación, citas, literal y contexto de la fuente de las 97 entradas) ·
`v4A_difprosa.py` / `.out` (cambios de prosa de M1–M6) · `v4A_sin_marca.py` / `.out` · `v4A_software.R` / `.out`
· `v4A_software.py` / `v4A_software_py.out` · `v4A_audita.out`, `v4A_audita_avisos.out` · `v4A_cadena.out` ·
`v4A_bloques_cap3.out` · `v4A_recorrido.js` / `.out` / `.json` · `v4_firmas_A.txt` (93 ids).

## Segunda lectura (2026-11-21, tras la «Segunda pasada» de `R4_cambios.md`)

Las 13 entradas que se me pidió volver a leer, tal como están hoy. Usé el mismo volcado
(`comprobaciones/v4A_vuelca.py` → `v4A2_vuelca.out`): el texto marcado, el `hash_texto` (coincide en las 13), las
citas visibles, el literal y su contexto en la caché. Comprobé también el texto renderizado del HTML final.
`audita_citas.py` da hoy solo F08 (17, las entradas sin firma). **Firmo las 13** (`comprobaciones/v4_firmas_A2.txt`).

| id | qué cambió | lectura |
|---|---|---|
| c3-m1-04 | «que verás» → «que se verá» | Voz; mismo sentido. Firmo |
| c3-m1-15 | `con-matiz`; nueva fuente, ejercicio 4.15, con cita visible tras «no hay ninguna»; nota nueva | J1 resuelto: el ej. 4.15 (`p0095.txt`) pide demostrar que con \|φ\| = 1 no puede ser estacionario. La nota dice ahora que el 4.16 solo pregunta y que la razón «depende del futuro» es de Shumway y Stoffer 3.ª p. 88. Firmo |
| c3-m2-30 | «Si sustituyes… tienes» → «Si se sustituye… queda» | Voz; mismo sentido. Firmo |
| c3-m3-11 | «Si en un correlograma muestral ves… y quisieras» → «Si un correlograma muestral da… y se quisiera» | Voz; mismo sentido. Firmo |
| c3-m3-15 | «regresión» → «proyección lineal (la regresión poblacional)»; «esa regresión» → «esa proyección» | Ahora dice lo mismo que Hamilton p. 111 («last coefficient in a linear projection»): queda resuelta la observación de §5. Firmo |
| c3-m4-31 | «te devuelve» → «devuelve» | Voz; mismo sentido («por defecto» se mantiene). Firmo |
| c3-m5-08 | «envuélvelo» → «conviene envolverlo» | Voz; mismo sentido. `dim(pacf()$acf)` = 20 1 1, ya repetido. Firmo |
| c3-m5-13 | Hamilton p. 60 en `fuentes` y a la vista, junto a Cryer y Chan p. 56 | J2 resuelto: en `hamilton1994time/p0075.txt` la fórmula μ = c/(1 − φ1 − … − φp) precede al literal («Thus, stationarity of an ARMA process depends entirely…»). La nota lo describe bien. Firmo |
| c3-m5-18 | «veas… recuerda» → «aparezca… conviene recordar» | Voz; mismo sentido. Firmo |
| c3-m5-20 | «Si ves… prueba» → «Ante un ARMA… conviene probar»; segunda cita visible, Hamilton p. 60, tras «errores estándar grandes» | Voz con el mismo sentido. Con la nueva cita, la observación de §5 queda resuelta: Hamilton p. 60 dice «θ1 close to −φ1 → white noise». `con-matiz` sigue siendo correcto: «errores estándar grandes» es lectura del capítulo. Firmo |
| c3-m6-06 | «Si miras… esperas» → «Al mirar… lo esperable es» | Voz; mismo sentido. Firmo |
| c3-m6-07 | «Uno o dos picos que apenas asoman fuera de la banda no bastan como evidencia; uno muy grande, o bastantes más del 5 % de los rezagos fuera, sí»; pasa a `respaldada` | Error E resuelto: dice ahora lo mismo que FPP3 §2.9 (`graphics.txt`), igual que c2-m2-08. Veredicto y nota correctos. Firmo |
| c3-m6-08 | «todos los rezagos» → «esos 20 rezagos», en oración propia | J3 resuelto: la prueba de grupo contrasta los ℓ primeros (FPP3 §5.4), aquí los 20 de la frase anterior. Firmo |

No apareció ningún problema nuevo en estas 13. La cita del ejercicio 4.15 cierra bien la oración (`</cite></span>.`),
sin espacio antes del punto.
