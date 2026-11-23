# Capítulo 4 · ronda R4 «fuentes» · verificación independiente, lote A (M1–M6)

Fecha: 2026-11-23. Verificador independiente A (subagente, contexto limpio): no redactó nada de esta ronda. Leyó
`CLAUDE.md`, `bibliografia/README.md` y `diagnostico/cap3/R4_verificacion_A.md`. **No leyó
`diagnostico/cap4/R4_cambios.md` ni `bibliografia/_local/herramientas/cap4/` hasta terminar las secciones 1 a 6**; la 7
es la comparación (de `_local/herramientas/cap4/` no leyó nada).

No tocó nada fuera de `diagnostico/cap4/`: ni prosa, ni `bibliografia/contraste/cap4.yml` (sin `verificado_por`; las
firmas van en `comprobaciones/v4_firmas_A.txt`). Sin commits. Reejecutó la cadena de ensamblado 4 → 5 → 6, que dejó los
cuatro HTML de los caps. 3–6 con la misma huella md5 que antes.

## 1. Resultado

| | entradas |
|---|---|
| Lote (c4-m1-* a c4-m6-*) | 141: 65 `respaldada`, 36 `con-matiz`, 38 `propia`, 2 `pendiente` |
| **Firmadas** | **137**: 65 `respaldada`, 35 `con-matiz`, 37 `propia` |
| **Sin firmar** | **4**: c4-m1-29 y c4-m6-08 (juicios, §3); c4-m3-62 y c4-m3-69 (`pendiente`: no hay fuente que leer; el motivo es correcto, §3) |

No encontré ningún **error** en el sentido del §2 (una frase con cita visible que enseña lo contrario de su fuente).

Método por entrada (`comprobaciones/v4A_vuelca.py` → `v4A_vuelca.out`): el texto de la afirmación **tal como está hoy**
en el HTML con su huella (**los 141 `hash_texto` coinciden**), sus citas visibles, el literal de `_local/citas/cap4.yml`
y ±500 caracteres de la fuente alrededor, en la página del PDF indicada (y, si no está, en la siguiente) o en la sección
de FPP3 o de la ayuda de R/forecast/tseries/urca acotada como la acota el auditor. **Todos los literales están en su
sitio**; el único que cae en la página siguiente es la fuente 2 de c4-m6-11, cuyo localizador es `pp. 126–127`. Leí cada
pasaje y lo comparé con la afirmación **en su párrafo** (`comprobaciones/v4A_texto.py`: texto plano del HTML con las
marcas a la vista). Comprobé el número impreso de todas las páginas de PDF citadas (cabecera o pie de Cryer y Chan,
Hamilton —desfase 15 en todo el tramo citado, incluidas pp. 475, 513, 515, 516, 518, 524 y la tabla B.6 de la p. 763—,
Hyndman y Khandakar y Shumway y Stoffer 3.ª): todas coinciden. Las dos páginas de Cryer y Chan sin número (p. 55 y
p. 109, aperturas de capítulo) caen entre las vecinas numeradas (54/56 y 107/110, con la blanca 108 ausente).

Las 38 `propia` (y las cifras de R de las citables) las repetí ejecutando con guiones propios, sin llamar a
`genera_cap4.R` ni a los de los lectores: `comprobaciones/v4A_software.R` → `.out` (R 4.6.0, forecast 9.0.2, tseries
0.10.62, urca 1.3.4) y `v4A_software.py` → `v4A_software_py.out` (statsmodels 0.14.6). Todo coincide: §4.

## 2. Errores (la frase, con su cita visible, enseña algo que la fuente no dice)

Ninguno en M1–M6.

## 3. Juicios (el veredicto, el localizador, la nota o la prosa deberían cambiar)

| id | qué dice la frase | qué dicen la fuente y el capítulo | qué falla | propuesta |
|---|---|---|---|---|
| J1 · **c4-m1-29** (`con-matiz`) | «El Capítulo 3 terminó con un límite explícito: los modelos ARMA **solo** describen series estacionarias (Cryer y Chan, 2008, p. 55).» | Cryer y Chan p. 55 (`p0068.txt`): el capítulo se titula «modelos para series estacionarias» y presenta los ARMA; no dice «solo». La misma obra, p. 201 (`p0211.txt`, fuente de c4-m1-08), escribe el ARIMA(p,1,q) como un **ARMA(p+1,q) no estacionario**, y el propio M1, 60 líneas después, enseña «Un ARIMA(p,d,q) es un ARMA(p+d,q) no estacionario» (c4-m1-08) | La frase marcada dice más que su cita visible (la nota lo reconoce: «ninguna de las dos dice solo») y contradice dentro del mismo módulo a c4-m1-08, que es correcta. La `afirmacion` del registro está bien («se plantean para series estacionarias»); la prosa no | «…con un límite explícito: los modelos ARMA del Capítulo 3 se plantean para series estacionarias.» Con eso, `respaldada`, o `con-matiz` con la nota actual |
| J2 · **c4-m6-08** (`propia`) | «Con d = 1 cuatro modelos más quedan a menos de 2 puntos del mejor (umbral…; el Módulo 7 contará siete, **porque cuenta también las variantes con deriva**)» | Repetido en R (`v4A_software.out`, últimas secciones): con d = 1 hay 4 modelos además del ganador a menos de 2 puntos (0,1,2 · 0,1,1 · 2,1,1 · 1,1,2) y, con las variantes con deriva, **2** más (1,1,1 y 0,1,2 con deriva). El M7 (c4-m7-14) cuenta siete **incluyendo al ganador**: 1 + 4 + 2 | El «cuatro» y el «siete» son ciertos, pero la razón que da el paréntesis no cuadra: 4 + variantes con deriva = 7 haría pensar en tres variantes con deriva, y son dos; la otra unidad es que el M7 cuenta al ganador y el M6 no | «…el Módulo 7 contará siete, porque incluye al propio ganador y dos variantes con deriva» |
| c4-m3-62, c4-m3-69 (`pendiente`) | La descomposición de KPSS (nivel que pasea + ruido) y H0: σ_v² = 0 | La ayuda de `kpss.test` (`web/trapletti2026tseries/kpss.test.txt`) solo da la nula (estacionariedad en nivel o tendencia) y el estimador de Newey–West; FPP3 §9.1 solo la nula; Hamilton cita a Kwiatkowski et al. (1992) en una lista (p. 532 impresa) sin describir la prueba | El motivo es correcto: sin texto de Kwiatkowski et al. no hay qué contrastar. No las firmo porque no hay fuente que leer, no por un defecto | Mantener `pendiente` hasta que entre el artículo |

## 4. Propias repetidas (y cifras de R dentro de entradas citables)

Todas coinciden con lo impreso. Salidas: `comprobaciones/v4A_software.out` y `v4A_software_py.out`.

| entradas | lo que repetí | resultado |
|---|---|---|
| c4-m1-07, -65, -09 | ARIMA(1,1,1) ML del Nilo; AR expandido y sus raíces | 0.2544 / −0.8741 (e.e. 0.1194, 0.0605); (1.2544, −0.2544), suma 1, raíces 1 y 3.9308; raíz MA 1.144 |
| c4-m1-23 | razón Var(y)/Var(w), set.seed(2026), n = 200, con y sin MA | 1.006 y 32.8 |
| c4-m1-66 | varianza de largo plazo / γ0 del ARMA(1,1) frente al AR(1) | 0.0202 frente a 1.68; (1+θ)² = 0.0159: la causa es θ |
| c4-m1-12 (cifras) | `ses()` frente a 1 + θ̂ del ARIMA(0,1,1) | α = 0.2457 frente a 0.2671 (próximos, no iguales); la recursión de `ses` se cumple con error 2e-13 |
| c4-m1-16 | el nivel alrededor de 1899 | 1898: 1100 → 1899: 774; medias 1097.75 y 849.97 |
| c4-m1-27, -28 | convenio de signo en R y statsmodels | `ARMAacf(ma = ±0.5)` → ±0.4; `arima` sobre MA(1) con θ = +0.6 → 0.59; `ArmaProcess(ma=[1,.5])` → ρ1 = 0.4; `ARIMA(0,0,1)` → 0.62 |
| c4-m2-62 | un escalón sin modelar sube d o infla σ̂² | `ndiffs(Nile)` = 1; σ̂² del ARMA(1,1) 19 891.7 sin el escalón y 15 552.9 con él como regresor |
| c4-m3-60 | varianzas por d, r1, 2(1−r1), cociente | 28 637.95 / 28 268.34 (−1.29 %) / 80 055.01 (×2.83); r1 = 0.4984; 1.003; 0.987 |
| c4-m3-09, -10, -11, -12, -13 (cifras) | `adf.test`, `kpss.test`, `PP.test`, `ndiffs`, cuerpo de `ndiffs`, `ur.df` | −3.3657 (p 0.0642, k = 4); 0.9654; −6.690; ndiffs 1/0/0; `ndiffs` llama a `ur.df(x, type = "drift")` sin fijar `lags` (por defecto 1); τ = −4.0487 y valor crítico −2.89; ρ̂1 con d = 1 y 2: −0.402, −0.626 |
| c4-m3-15 | 1000 réplicas del ARIMA(1,1,1) con raíz unitaria, semilla 2026 | PP.test 100 %, adf.test(k = 4) 51.3 % |
| c4-m3-18, -66 | Monte Carlo de 1000 réplicas sin y con escalón (β = −247.78, σ = 127.03, β/σ = 1.951) | sin: KPSS 4.8 %, adf.test no rechaza 5.4 %, ndiffs(adf) 0 %; con: KPSS 100 %, ndiffs(kpss) 100 %, adf.test no rechaza 86.4 %, ndiffs(adf) 0.5 % |
| c4-m3-67, -34 | malla de 400 réplicas, deltas en orden | δ = 0: 4.5 %; δ = 100 (0.787 σ): 70.75 % con ℓ = 4 y 44.5 % con ℓ = 12; KPSS medio 1.07 (δ = 200) y 1.23 (δ = 300) |
| c4-m3-19, -64, -31 | KPSS a mano (Σ S_t² / n² σ̂²_LP, pesos 1 − j/(ℓ+1)) | 0.9654349 (ℓ = 4, σ̂²_LP 74 193.51) = tseries; 0.5497197 (ℓ = 12, 130 301) = tseries con `lshort = FALSE`; 1.315226 (ℓ = 2) = `ur.kpss(use.lag = 2)`; `ndiffs` usa trunc(3√n/13) = 2; ACF 1–12 del Nilo, todas positivas |
| c4-m3-71 | puente browniano por simulación propia (n = 400, 4000 réplicas, otra semilla) | Var(S_t/√n) 0.086, 0.184, 0.250, 0.191 frente a r(1−r) 0.09, 0.1875, 0.25, 0.1875; S_n = 0 |
| c4-m3-20, -22 | caminatas aleatorias (500 réplicas, otra semilla) | max\|S_t\|/n^{3/2} ≈ 0.14 estable con n = 100, 400, 1600; KPSS medio 1.11 → 3.59 → 8.85; rechazo 85 %, 99 %, 100 % (el registro, con otra semilla, 89/99/100) |
| c4-m3-21 | tabla del cuerpo de `kpss.test` | `c(0.739, 0.574, 0.463, 0.347)` frente a `c(0.01, 0.025, 0.05, 0.1)`; statsmodels da también 0.463 |
| c4-m3-29, -64 | `statsmodels.kpss` | 'auto': 0.8691 con 5 rezagos; 'legacy': 0.5497 con 12 (`int(np.ceil(12·(n/100)^{1/4}))`, el ⌈·⌉ del capítulo); nlags = 4: 0.96543490775266 = tseries |
| c4-m4-02, -04, -05, -07, -11, -12, -13, -15, -16 (cifras) | ACF/PACF del Nilo y de su diferencia; ARIMA(0,1,1); vecinos | ACF 0.498, 0.385, 0.328, 0.239; PACF fuera de ±0.196 solo en el 1; ACF de ∇Nilo fuera de ±0.197 en 1 y 8 (−0.402, 0.231); PACF −0.402, −0.246, −0.119; θ̂ = −0.7329 (e.e. 0.1143, t = −6.41), σ̂² = 20 599.87, LB(20) p = 0.674, 1 + θ̂ = 0.267; AICc 1269.216 / 1267.507 / 1268.210 / 1281.605 |
| c4-m5-04, -10, -11, -12, -13, -17, -18, -19 | `arima` con media y diferencias; `Arima` con deriva; aviso con d = 2; código y trazas de `auto.arima` | coeficiente «intercept» = 920.70 (media 919.35); con d = 1 `include.mean` no deja coeficiente ni aviso; deriva −2.883 (e.e. 2.017, t = −1.43), igual con `xreg = seq_along`; el cuerpo de `Arima` construye `drift = seq_along(x)`; aviso literal «No drift term fitted as the order of difference is 2 or more.»; `allowdrift && (d + D) == 1`, `allowmean && (d + D) == 0`; trazas: d = 0 con media, d = 1 con deriva (el mismo orden con y sin), d = 2 sin ninguna; c = −2.10; AICc 1268.06 frente a 1267.51; (740 − 1120)/99 = −3.84 = media de las diferencias; −247.78/99 = −2.50 |
| c4-m5-14 | `trend` de statsmodels | por defecto `const` con d = 0 y nada con d = 1; `trend='t'` con d = 1 da `x1`; con d = 2, ValueError (los términos de orden menor que d + D los elimina la diferenciación) |
| c4-m6-02, -05 (cifras) | AICc y BIC a mano frente a `Arima`; `nobs`; log-verosimilitud | AICc a mano con n* = 99: 1267.5074 = `Arima` (con n = 100: 1267.5048); BIC igual con log 99; `nobs` 99 y 98; logL del ARIMA(0,1,1) = la del MA(1) sobre `diff(Nile)` (−632.5456); el BIC de statsmodels usa `nobs_effective` = 99 |
| c4-m6-08, -09, -10, -11, -60 y la tabla «Los mejores de cada d» | rejilla de 27 modelos con `forecast::Arima` (ruta distinta de la del generador) | a menos de 2 del mejor: 3 / **4** / 2 por d; mejores AICc 1282.50 / 1267.51 / 1264.60 y BIC 1292.50 / 1274.28 (0,1,1) / 1273.50 (0,2,2); raíz AR del (1,0,1) 1.1614, MA del (1,1,1) 1.144, MA del (1,2,2) 1.0316; con d = 2, raíz MA de módulo 1.000 en **4 de 9** (0,2,1 · 0,2,2 · 1,2,1 · 2,2,1), 1.032 y 1.048 en los otros dos con MA; LB(20) rechaza en 8 de 27 y ninguno cerca del mejor de su d |
| c4-m1-64, -65, -07, -09, c4-m2-60, -63, c4-m3-33, c4-m5-15 | deducciones y consejos | se siguen de lo que dicen las entradas citables que las preceden; ninguna se atribuye a una obra |

## 5. Cambios de prosa revisados (M1–M6)

`comprobaciones/v4A_difprosa.py` → `v4A_difprosa.out`: prosa de las plantillas en `21b311b` contra la de hoy, sin marcas
ni citas, por líneas y por palabras. Leí cada cambio. Todos acercan la frase a la fuente (retiran «esqueleto de todo»,
«la familia ya existía», «Box & Jenkins original», «enorme», «casi siempre», «en series económicas casi nunca de 1»,
«constantemente», «la recomendación habitual»…) y ninguno cambia el sentido de algo correcto. La única cifra nueva en
M1–M6 no entra ninguna cifra nueva: «siete», «1.000» y «2 puntos» ya estaban. No hay segunda persona nueva. Dos
observaciones:

- **c4-m2-62** (`propia`, firmada; Bajo): la frase nueva «se modelan aparte, y mientras no se haga el ajuste puede
  absorberlos» se lee primero como «mientras no se haga el ajuste» (la estimación), cuando quiere decir «mientras no se
  modelen aparte, el ajuste puede absorberlos». Propuesta: «…se modelan aparte; si no se modelan, el ajuste puede
  absorberlos, por ejemplo subiendo $d$ o inflando $\hat\sigma^2$.» El hecho está comprobado (§4).
- **c4-m2-11** (`con-matiz`, firmada; Bajo): «si es del MA, la serie se diferenció de más y hay que bajar $d$» es
  categórica, mientras el M1 (c4-m1-25: «pista», «quizá») y el M3 (c4-m3-61: «solo un indicio: falla en los dos
  sentidos») dicen lo mismo como indicio. La nota declara la inferencia; para que el capítulo no se contradiga:
  «…si es del MA, probablemente se diferenció de más y conviene probar a bajar $d$».

**Voz** (no es de esta ronda; para quien cierre el capítulo): fuera de las intros de simulador, el M2 conserva la
segunda persona en los paneles del ciclo («Qué te devuelve atrás», cuatro veces, y «que puede mandarte de vuelta al
principio»).

## 6. Observaciones sobre entradas firmadas y comprobaciones globales

- **c4-m1-26** (`respaldada`): la nota dice que ninguna fuente dice «algunos textos» en plural; lo que sostiene el plural
  es la frase anterior de la misma §Details de `?arima` («Different definitions of ARMA models have different signs…»),
  que no está entre los literales. Conviene añadirla como fuente o retocar la nota.
- **c4-m1-08**: la cita visible es Cryer y Chan p. 202, que da los p + d coeficientes; «no estacionario» está en la p. 201
  (fuente 2). `pp. 201–202` como localizador visible lo cubriría entero.
- **c4-m2-21**: «varianza estable» no tiene literal (FPP3 §5.4 la da como útil, no necesaria; la nota lo dice). Es parte
  de la definición de ruido blanco: firmo.
- **c4-m4-07**: «uno fuera por azar es lo esperable» vale para la barra del rezago 8 (0.231 frente a ±0.197), que no es
  una barra grande; FPP3 §2.9 dice que una barra grande fuera sí es señal. La frase no generaliza: firmo.
- `python3 precalculo/audita_citas.py` (`v4A_audita.out`, `v4A_audita_avisos.out`): **206 hallazgos, todos F08**; 101 son
  de M1–M6 (las 65 + 36 citables). Ningún otro código: 1068 citas literales comprobadas, 0 sin caché, 0 sin literal
  local. En M1–M6, los A01 son las listas de fuentes y un comentario de código («Phillips-Perron»); ninguna atribución
  sin marca en la prosa (`v4A_sin_marca.out`).
- **Cadena** (`v4A_cadena.out`): `ensambla_cap4.py`, `_cap5.py` y `_cap6.py`; md5 de los caps. 3–6 idéntico antes y
  después; `git status Htmls_Series` solo muestra el cap. 4 (el cambio de la ronda).
- **Citas visibles, estático** (`v4A_enlaces.py` → `.out`): 126 citas en M1–M6, todas con texto y con el loc de su
  `data-loc`, todas enlazadas a una entrada de la lista «Fuentes citadas en este módulo» **de su módulo**; cada lista
  tiene exactamente las obras citadas en el módulo; 0 espacios antes de puntuación tras una cita. La de c4-m6-14 va en
  modo narrativo («Hyndman y Athanasopoulos (2021, §9.6) prefieren el AICc»): la oración tiene sujeto.

## Lo que no pude comprobar

- **Recorrido visual por HTTP** (KaTeX, anchos de 375 px): no lo hice; la comprobación de citas y enlaces es estática.
- **c4-m3-62 y c4-m3-69**: sin texto de Kwiatkowski et al. (1992).
- No repetí el bloque de Python del M1 (1.363 y 56.7, fuera de las marcas) ni el verificador de bloques.

## 7. Comparación con `R4_cambios.md` (leído después de lo anterior)

- El registro de cambios dice que el redactor miró a mano 5 entradas y los 61 cambios de prosa, y que el resto es
  lectura de los lectores comprobada mecánicamente. En M1–M6 la lectura una a una halla 0 errores y 2 juicios en 141
  entradas; las 137 restantes las firmo tras leer cada pasaje y repetir cada cifra.
- **c4-m1-29**: la fila del registro dice «se plantean para series estacionarias», más suave que la prosa («solo
  describen»), y el registro de cambios no la trata como cambio de prosa. Es mi J1: se corrigió la `afirmacion`, no la
  frase (el mismo patrón que c3-m6-08 en el cap. 3).
- **c4-m6-08** (cambio 21): añadió «umbral que este capítulo toma por convención» y conservó «el Módulo 7 contará siete,
  porque cuenta también las variantes con deriva», cuya aritmética no cuadra (J2).
- **c4-m2-17/-62** (cambio 11): la reescritura es correcta en el fondo y el registro la justifica bien; la ambigüedad de
  «mientras no se haga el ajuste» (§5) no se menciona.
- **c4-m6-60** (cambio 22, fuera «exactamente»): lo confirmo (módulos de 1.000000 a 1.000014).
- **Punto 2 de «Lo que no cierra»** («R. J. Hyndman y Athanasopoulos» en las citas): hoy el HTML ya dice «Hyndman y
  Athanasopoulos» y «Hyndman et al.»: está resuelto (por la sesión maestra, según el propio documento).
- **Punto 7**: «Prácticamente nunca se quiere» (c4-m5-07) está declarado `con-matiz` con esa nota; lo firmo así.
- **Comprobaciones**: coinciden con las mías (206 F08 y ningún otro código; cadena byte a byte). Yo además repetí todas las
  `propia` de M1–M6 con guiones propios (el registro de cambios dice que el redactor solo reejecutó
  `sim_raiz_unitaria.R`), y la rejilla con `forecast::Arima` en vez de `stats::arima`, con el mismo resultado.

## 8. Guiones y salidas (todos en `comprobaciones/`)

`v4A_vuelca.py` / `.out` (afirmación, citas, literal y contexto de las 141 entradas) · `v4A_texto.py` (texto plano del
HTML con marcas) · `v4A_difprosa.py` / `.out` · `v4A_sin_marca.out` · `v4A_software.R` / `.out` · `v4A_software.py` /
`v4A_software_py.out` · `v4A_enlaces.py` / `.out` · `v4A_audita.out`, `v4A_audita_avisos.out` · `v4A_cadena.out` ·
`v4_firmas_A.txt` (137 ids).

## Segunda lectura (2026-11-23)

Releí las 4 entradas que la sesión maestra corrigió después de mi verificación (`comprobaciones/r4_ediciones_maestra.py`).
Usé el mismo volcado (`comprobaciones/v4A_vuelca.py` → `v4A2_vuelca.out`): el texto marcado de hoy, la huella
(`audita_citas.py --huella`: **coincide en las 4**), las citas visibles y el literal con su contexto en la caché. También
leí cada frase en su párrafo (`v4A_texto.py`) y volví a correr `v4A_software.R` (→ `v4A2_software.out`, idéntico a
`v4A_software.out` salvo los avisos). **Firmo las 4**; están añadidas al final de `comprobaciones/v4_firmas_A.txt`, que
queda con 141 ids: todo el lote menos los dos `pendiente`.

| id | qué cambió | lectura |
|---|---|---|
| c4-m1-29 | «solo describen» → «los modelos ARMA del Capítulo 3 se plantean para series estacionarias»; la nota nueva lo registra | J1 resuelto. La frase dice ahora lo que dicen Cryer y Chan p. 55 (el capítulo de los modelos estacionarios presenta los ARMA) y FPP3 §9.3, y ya no choca con c4-m1-08. `con-matiz` sigue siendo correcto. Hay un detalle de estilo, no de contenido: «el Capítulo 3» aparece dos veces en la misma oración. Firmo |
| c4-m6-08 | el paréntesis pasa a «porque incluye al propio ganador y dos variantes con deriva»; la afirmación del registro lo recoge | J2 resuelto. Repetido en R: con d = 1 hay 4 modelos además del ganador a menos de 2 puntos, y con las variantes con deriva son 7 contando el ganador (1 + 4 + 2). La nota no menciona el desglose del 7, pero la afirmación sí. Firmo |
| c4-m2-62 | «mientras no se haga el ajuste puede absorberlos» → «si se dejan fuera del modelo, el ajuste puede absorberlos» | Se lee sin ambigüedad. El hecho repetido no cambia: `ndiffs(Nile)` = 1 y σ̂² = 19 891.7 sin el escalón frente a 15 552.9 con él. Firmo |
| c4-m2-11 | «la serie se diferenció de más y hay que bajar d» → «lo más probable es que la serie se haya diferenciado de más y convenga bajar d»; nota nueva | La frase ya no es categórica y queda en línea con c4-m1-25 («pista») y c4-m3-61 («indicio»). FPP3 §9.7 y Cryer y Chan p. 127 están en su sitio. La nota declara la inferencia inversa. `con-matiz` es correcto. Firmo |

Tercera lectura de c4-m1-29 (2026-11-23): la prosa dice ahora «los modelos ARMA se plantean para series estacionarias»,
sin repetir «del Capítulo 3». La huella `847e84b4d12d9448` coincide con el `hash_texto`, y la frase es la misma que la
`afirmacion` del registro. En su párrafo, «El Capítulo 3 terminó con un límite explícito» deja claro de qué ARMA se
habla, y la frase sigue respaldada por Cryer y Chan, p. 55. Firmo de nuevo; queda añadida al final de `v4_firmas_A.txt`.
