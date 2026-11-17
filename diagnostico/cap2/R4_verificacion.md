# Capítulo 2 · ronda R4 «fuentes» · verificación independiente

Fecha: 2026-11-17. Verificador independiente (subagente, contexto limpio): no redactó nada de esta ronda.
Leyó `CLAUDE.md`, `bibliografia/README.md` y `diagnostico/cap1/R4_cambios.md`. No leyó
`diagnostico/cap2/R4_cambios.md` hasta terminar las secciones 1 a 6; la 7 es la comparación.

Único cambio en el repo fuera de esta carpeta: el campo `verificado_por` de 51 entradas de
`bibliografia/contraste/cap2.yml`, puesto por `comprobaciones/v4_firma.py` (inserta una línea tras
`redactado_por`; el `diff` contra la copia previa da 51 líneas añadidas y 0 borradas). Sin commits.

## 1. Resultado

| | entradas |
|---|---|
| Registradas | 74 |
| **Firmadas** | **51**: 29 `respaldada`, 6 `con-matiz`, 8 `propia`, 8 `pendiente` |
| **Sin firmar** | **23** (17 `respaldada`, 5 `con-matiz`, 1 `propia`): 7 errores (§2) y 16 juicios (§3) |

Firmadas (51): c2-m1-01, -03, -04, -07, -13 · c2-m2-02, -03, -06, -10 · c2-m3-05, -06, -07, -09, -15,
-16, -17 · c2-m4-06, -07, -08, -09, -11, -12, -14 · c2-m5-04, -05, -10, -12 · c2-m6-01, -05, -06, -09,
-10, -11, -16, -17 · c2-m7-02, -05, -07, -09, -14, -15, -18, -19 · c2-m8-02, -03, -04, -08 ·
c2-m9-11, -12, -13, -24.

En las
`pendiente` firmo que el motivo es cierto (comprobé en la caché lo que dicen sus notas: la 3.ª ed. de
Shumway y Stoffer pp. 23, 29 y 112; el índice de la 3.ª ed.; Hamilton p. 532; FPP3 §3.1 sobre Guerrero),
no que la frase esté respaldada. En las `propia` firmo que lo repetí ejecutando o derivando.

Comprobaciones generales:

- `python3 precalculo/audita_citas.py` tras firmar: **FALLA, 23 hallazgos** = 22 F08 (las 22 entradas
  citables sin firma; la 23.ª sin firma, c2-m7-08, es `propia`) + **1 F11** (ver §4, error E0). F05 limpio:
  las 220 citas literales del curso están en su localizador; F02, F03, F04, F06, F07 y F09 limpios.
  Salida en `comprobaciones/v4_audita.out`.
- Ninguna cita está en la página siguiente a la indicada salvo en los rangos `pp. N–N+1`, donde es lo
  esperado (`comprobaciones/v4_extrae.out`, marcas «PÁGINA SIGUIENTE»).
- `git diff --stat -- Htmls_Series`: solo el capítulo 2 (371+, 211−). `ensamblado/ensambla_cap3.py`:
  «reproducible byte a byte».
- HTTP en `http://localhost:8731/` (sirve este worktree: misma huella md5 que el archivo), 375 px, nueve
  módulos: `scrollWidth == clientWidth` en todos, 0 citas fuera del viewport, 0 enlaces de cita sin destino,
  0 signos de puntuación huérfanos en línea aparte tras una cita, 0 `.katex-error`, consola sin errores;
  72 citas visibles (3 de ellas dentro del desarrollo de Durbin–Levinson). Ninguna cita rompe la
  maquetación; la única que rompe la *frase* es la de c2-m4-02 (captura en `v4_navegador.out`).

## 2. Errores (la frase o el localizador dicen algo que la fuente no dice)

| id | qué dice la frase | qué dice la fuente | qué falla | propuesta |
|---|---|---|---|---|
| **c2-m4-05** | «**Ajustar la regresión** del rezago k **equivale** a resolver el sistema de Yule–Walker de orden k» | Cryer y Chan p. 114 (`texto/cryer2008time/p0125.txt:22–24`): «For a given lag k, it can be shown that [literal fuera de git: `_local/citas/cap2.yml`, c2-m4-05 · fuente 1], para «any stationary process with autocorrelation function ρk»: es la PACF **teórica**. La muestral sale de sustituir ρ por r (p. 115, `p0126.txt:37–38`) | Con datos no equivale. Sobre log(AirPassengers), el último coeficiente de k regresiones por MCO difiere de `pacf()` hasta en **0.35** (k = 2: −0.221 frente a −0.118; k = 5: 0.306 frente a 0.116), y `pacf(method="ols")` de statsmodels hasta en **0.60** (`comprobaciones/v4_software.out`, `v4_software_py.out`). La frase enseña algo falso sobre la PACF que calcula R | **Reescribir**: «En la población, los coeficientes de esa regresión satisfacen el sistema de Yule–Walker de orden k… (Cryer y Chan, p. 114); la PACF muestral resuelve ese mismo sistema con las r en lugar de las ρ (p. 115), y por eso no coincide exactamente con el último coeficiente de una regresión por MCO». Arrastra a c2-m4-04 (juicio J6) |
| **c2-m3-13** | «Dos series con tendencia creciente **tendrán** autocorrelaciones altas y correlación cruzada alta… (Cryer y Chan, pp. 263–264)» | Cryer y Chan pp. 263–264 (`p0273.txt:20–22`, `p0274.txt:12–14`): con dos IMA(1,1) **independientes** la correlación cruzada muestral se dispersa entre −1 y 1, y «we **sometimes** obtain nonsense (spurious) correlation» | La nota lo reconoce («a veces», no siempre) y aun así deja `con-matiz` sobre una frase **más fuerte** que la fuente. Además, la fuente habla de tendencias estocásticas sin deriva, no de «tendencia creciente» | **Reescribir**: «Dos series no estacionarias independientes **pueden** mostrar correlación cruzada alta sin ninguna relación real». Con eso, `con-matiz` (Hamilton nombra la regresión espuria; Cryer y Chan, la correlación espuria) o `respaldada` |
| **c2-m4-02** | «…es el coeficiente φkk de la regresión (Hyndman y Athanasopoulos, 2021, §9.5)» y, debajo, la ecuación | FPP3 §9.5 (`arima.txt:336`) respalda el contenido | **Colocación**: la cita separa «la regresión» de su ecuación, que es su complemento (comprobado a 375 px) | **Mover la cita** al final de la ecuación o tras «Equivalentemente»; además arrastra el problema de c2-m4-05 si «la regresión» se lee como ajuste muestral |
| **c2-m1-06** | «es débilmente estacionario si cumple **las tres condiciones** (Cryer y Chan, 2008, p. 17):» | Cryer y Chan p. 17 (`p0030.txt:4–7`) numeran **dos** condiciones (media constante; γ que depende solo del rezago) | La cita está pegada a «las tres condiciones»: quien abra la p. 17 encuentra dos. La nota explica la equivalencia, pero la cita afirma otra cosa | **Mover la cita** tras «débilmente estacionario», o `con-matiz` con la cita al final de la lista |
| **c2-m5-01** | «…los choques se amplifican sin límite. Rara vez sirve para modelar datos reales (Cryer y Chan, 2008, p. 89).» | Cryer y Chan p. 89 (`p0101.txt:48–49`): [literal fuera de git: `_local/citas/cap2.yml`, c2-m5-01 · fuente 4] such that \|φ\| > 1. A [literal fuera de git: `_local/citas/cap2.yml`, c2-m5-01 · fuente 5] | La nota declara que «rara vez sirve» es más fuerte que la fuente, pero la cita visible va **exactamente** sobre esa oración | **Mover la cita** tras «se amplifican sin límite» y dejar «rara vez sirve…» como frase del capítulo, o reescribirla: «Cryer y Chan lo consideran un tipo de no estacionariedad menos razonable que φ = 1» |
| **c2-m5-09** | «Al añadir una constante se obtiene la caminata aleatoria con deriva (*random walk with drift*) (Hyndman y Athanasopoulos, 2021, §9.1)» | FPP3 §9.1 (`arima.txt:67`) describe el modelo y dice «will tend to drift upwards», pero **no lo nombra**; el nombre está en §9.3 (`arima.txt:216`) y en Hamilton p. 436 (`p0451.txt:12`: [literal fuera de git: `_local/citas/cap2.yml`, c2-m5-09 · fuente 1]) | **Localizador**: la frase introduce un nombre y la cita visible manda a una sección donde ese nombre no está | **Cambiar el localizador visible** a Hamilton p. 436 (ya es fuente de la entrada) o añadir FPP3 §9.3 |
| **c2-m6-04** | Recuadro del ADF con «∇yt = α + βt + γ yt−1 + …», cita visible «(Cryer y Chan, 2008, pp. 128–129)» | La regresión de pp. 128–129 (`p0140.txt:4–9`) no lleva constante ni tendencia; [literal fuera de git: `_local/citas/cap2.yml`, c2-m6-04 · fuente 4] está en la **p. 130** (`p0141.txt:9`), que es fuente de la entrada pero no cita visible | **Localizador** incompleto: el estudiante no encuentra en pp. 128–129 la regresión que ve escrita | **Añadir** una segunda cita visible «(Cryer y Chan, 2008, p. 130)» tras el paréntesis de H1 |

## 3. Juicios (el veredicto o la redacción deberían cambiar; discutible)

El criterio común: cuando la propia `nota` de una entrada `respaldada` dice que la frase va más allá de
la fuente, el veredicto que pide el README es `con-matiz` («la fuente apoya la idea pero difiere en un
detalle; la nota dice cuál»), o la frase se ajusta a la fuente.

| id | qué dice la frase | qué dice la fuente | qué falla | propuesta |
|---|---|---|---|---|
| J1 · c2-m2-09 | «Un modelo… **es bueno cuando**… los residuales son indistinguibles del ruido blanco» | FPP3 §5.4 (`toolbox.txt:292–295`): son propiedades que un buen método cumple, y «that does not mean that forecasting methods that satisfy these properties cannot be improved» | La frase la presenta como criterio suficiente; la nota dice que es solo necesaria y aun así el veredicto es `respaldada` | **Reescribir** «Un buen modelo deja residuales indistinguibles del ruido blanco», o acotar la marca a la segunda oración (esa sí está respaldada) |
| J2 · c2-m2-01 | «Es el ladrillo con el que se construyen **todos los modelos del curso**» | Hamilton p. 47 (`p0062.txt:43`): «all the processes considered **in this chapter**»; Cryer y Chan p. 17 (`p0030.txt:18`): «**many** useful processes» | Más general que las dos fuentes; la nota lo admite | **`con-matiz`** (la nota ya sirve) |
| J3 · c2-m4-01 | «hoy y anteayer **aparecerán** correlacionados» | FPP3 §9.5 (`arima.txt:334`): «y_t and y_{t-2} **might** be correlated» | Más fuerte; la nota lo admite | «**pueden aparecer**» (y queda `respaldada`) o `con-matiz` |
| J4 · c2-m7-01 | «La diferenciación es **la herramienta estándar**…» | FPP3 §9.1 (`arima.txt:25`): «one way to make a non-stationary time series stationary» | La nota dice que «estándar» es del capítulo | **`con-matiz`**, o «una herramienta para…» |
| J5 · c2-m7-06 | «Si la ACF decae despacio **y casi en línea recta**, falta diferenciar» | FPP3 §9.1 (`arima.txt:29`): «decreases slowly» | La nota atribuye «casi en línea recta» a Cryer y Chan, pero Cryer y Chan **no están en `fuentes`** | **Añadir** Cryer y Chan p. 128, [literal fuera de git: `_local/citas/cap2.yml`, c2-m3-09 · fuente 2] (`p0139.txt:28`), ya registrada en c2-m3-09 |
| J6 · c2-m4-04 | «En la práctica **no se corren k regresiones**: se obtiene la PACF a partir de la ACF con la recursión…» | Cryer y Chan p. 115: método eficiente para resolver (6.2.8), el sistema con las ρ o las r | Sugiere que las k regresiones darían lo mismo; con datos no (E-c2-m4-05) | «En la práctica la PACF muestral se calcula a partir de la ACF con la recursión…» |
| J7 · c2-m1-15 | «los modelos ARMA del Capítulo 3 —y la teoría de estimación e inferencia…— suponen estacionariedad (Cryer y Chan, p. 16)» | p. 16 (`p0029.txt:5–8`): para la inferencia «we must **usually** make… assumptions… The most important… is that of stationarity». No menciona ARMA | La cita respalda la mitad de la frase | **Añadir** Cryer y Chan p. 55 (`p0068.txt:1–6`: «Models for stationary time series… [literal fuera de git: `_local/citas/cap2.yml`, c2-m1-15 · fuente 3]), o `con-matiz` |
| J8 · c2-m5-07 | «…distinguir φ = 0.95 de φ = 1 acaba siendo casi imposible (Hamilton, p. 445)» | Hamilton p. 445 (`p0460.txt:3–5`): para cada T existe un proceso estacionario, con raíz suficientemente cercana a 1, indistinguible del de raíz unitaria | Ni el 0.95 ni la dependencia monótona en T ni los correlogramas están en la fuente; la nota lo dice | **`con-matiz`** |
| J9 · c2-m8-01 | «La diferenciación arregla la media, **pero no la varianza**» | FPP3 §9.1 (`arima.txt:27`): los logaritmos estabilizan la varianza; la diferenciación «can help stabilise the mean» | La fuente reparte papeles; no dice que diferenciar no arregle la varianza | **`con-matiz`** con esa nota, o «La diferenciación estabiliza la media; para la varianza hace falta una transformación» |
| J10 · c2-m2-08 | «Una barra que apenas asoma fuera de la banda **no es evidencia de nada**…» | FPP3 §2.9 (`graphics.txt:647`): una o más barras **grandes**, o bastante más del 5 %, indican que no es ruido blanco | La nota declara «un patrón», no «no es evidencia de nada», que es más fuerte que lo que se sigue de la fuente | «no basta como evidencia» o completar la nota |
| J11 · c2-m3-01 | «La autocorrelación mide **cuánto se parece** una serie a una copia de sí misma…» | FPP3 §2.8 (`graphics.txt:577`): «measures the **linear** relationship between lagged values» | Más general (cualquier parecido, no solo lineal); la nota lo admite | «mide la relación lineal entre la serie y una copia…», o `con-matiz` |
| J12 · c2-m5-11 | «Las caminatas aleatorias se usan mucho para datos financieros… (§9.1), **y eso explica** por qué en precios… el ingenuo suele ser el mejor método (§5.4)» | FPP3 §9.1 (`arima.txt:65`): «the random walk model **underpins naïve forecasts**»; §5.4: «For stock market prices and indexes, [literal fuera de git: `_local/citas/cap2.yml`, c2-m5-11 · fuente 3] | Tras la reescritura, «eso» (que el modelo se use mucho) pasa a ser la causa; la causa en la fuente es que el pronóstico de una caminata es el último valor | «…y como el pronóstico de una caminata aleatoria es el último valor observado, en precios e índices bursátiles el ingenuo suele ser el mejor método» |
| J13 · c2-m7-11 | «En la duda, conviene diferenciar de menos (Hyndman y Athanasopoulos, §9.1)» | FPP3 §9.1 (`arima.txt:121`): [literal fuera de git: `_local/citas/cap2.yml`, c2-m7-11 · fuente 5] to obtain a stationary series» | La fuente no habla de la duda; la regla asimétrica es del capítulo (la apoya más Cryer y Chan p. 128, `p0139.txt:23`: «To avoid overdifferencing, we recommend… parsimony») | **`con-matiz`**, o «no conviene diferenciar más de lo necesario» |
| J14 · c2-m8-05 | «…mientras que λ = −0.295 no significa nada para nadie (Hyndman y Athanasopoulos, §3.1)» | FPP3 §3.1 (`decomposition.txt:66–68`): los cambios en logaritmos son relativos; otras transformaciones son «not so interpretable» | La cita va pegada a la hipérbole, no a la interpretabilidad del logaritmo | **Mover la cita** tras «variaciones porcentuales—» |
| J15 · c2-m9-01 | «…conviene ejecutar **siempre** en este orden, **porque cada paso condiciona el diagnóstico del siguiente** (§9.7)» | FPP3 §9.7 (`arima.txt:451`): «a useful general approach» para datos no estacionales | La nota declara lo no estacional y los pasos añadidos, pero no el «siempre» ni el «porque», que van pegados a la cita | Completar la nota, o mover la cita tras «secuencia de decisiones» |
| J16 · c2-m7-08 (`propia`) | «en **una muestra cualquiera** el cociente de varianzas **sigue de cerca** a 2(1−r1)» | Derivación del capítulo | Falso en muestras no estacionarias: log(AirPassengers), cociente 0.058 frente a 2(1−r1) = 0.093; caminatas con deriva simuladas, 0.001 frente a 0.03 (`v4_software.out` y una prueba suelta). Sí vale en series estacionarias (AR(0.5): 1.216 frente a 1.217) y el **signo** del cambio sí lo da r1 | «…y en una muestra estacionaria el cociente se acerca a 2(1−r1)…»; la conclusión del párrafo no cambia |

## 4. Fuera de las entradas

**E0 · F11 a nivel de curso.** `audita_citas.py` suma las palabras citadas de cada obra en **todo el
curso**: FPP3 llega a **790** (393 del cap. 1 + 397 del cap. 2) con tope 400. Es una FALLA del auditor
que esta ronda introduce; Cryer y Chan quedan en 388. O se recortan citas o Javier decide si el tope es
por capítulo o por curso.

**Atribuciones que siguen sin marca** (`comprobaciones/v4_sin_marca.py` sobre la prosa fuera de todo
`data-afirma`):

1. `capitulo-2…html:3355` · título del recuadro «KPSS — **Kwiatkowski, Phillips, Schmidt y Shin**»: atribuye la
   prueba a cuatro autores, fuera de c2-m6-05. FPP3 §9.1 respalda la atribución (ya registrada en c2-m6-16):
   basta con meter el título en una marca o citar ahí.
2. `:5152–5160` · **«Lecturas de este capítulo»**: solo el ítem de Shumway y Stoffer lleva marca (c2-m9-24). Los
   otros tres están escritos a mano y sin marca: FPP3 «secc. 9.1–9.2… 2.8–2.9… 3.1» (las secciones existen y
   tratan eso: comprobado en la caché); Kwiatkowski et al. (1992) con revista, volumen y páginas, y «el
   artículo original de la prueba KPSS»; Guerrero (1993) y «el criterio de selección de λ del Módulo 8». Los
   metadatos coinciden con `referencias.json`, pero no los escribió `genera_referencias.py`, y las dos
   últimas son atribuciones (FPP3 §3.1, `decomposition.txt:80`, y §9.1, `arima.txt:126`, las respaldan).
3. «**criterio de Guerrero**» / «el λ de Guerrero» en `:4261`, `:4268`, `:4289` y `:4799`, fuera de la marca
   de c2-m8-04 (que además está `pendiente`).
4. `:2393` · «Por eso **se trabaja casi siempre** con una versión más manejable» (la estacionariedad débil):
   afirmación sobre la práctica, sin marca. Cryer y Chan p. 17 (`p0030.txt:9–10`) dicen que en su libro
   «stationary» designa siempre la débil; no dicen «casi siempre» de la práctica en general.

No son atribuciones y no las cuento: los nombres de métodos dentro de recuadros ya marcados (Box–Cox,
Ljung–Box, Durbin–Levinson, Yule–Walker), el código, y las convenciones del propio curso («este curso
aplica siempre el mismo orden»).

**Listas de referencias.** La lista «Referencias citadas en este capítulo» contiene exactamente las cuatro
obras con cita visible (Cryer y Chan, Hamilton, FPP3, ayuda de R), y las de módulo, las de cada módulo
(F02 limpio). El **pie** lista las cuatro obras básicas del curso (Box et al. 2015, Brockwell y Davis 2016,
FPP3, Shumway y Stoffer 2017), por diseño de `genera_referencias.py` (`basicas`), igual que en el cap. 1:
no son las obras citadas. Si el encargo quiere que el pie contenga exactamente las citadas, eso es un
cambio de diseño, no de esta ronda.

## 5. Observaciones sobre entradas firmadas (no impiden la firma)

- **c2-m5-05**: la nota dice que el caso del AR(1), con raíz 1/φ, «lo escribe el capítulo». Lo escribe también
  Cryer y Chan en la nota al pie de la p. 71 (`p0084.txt:46–47`): «It also applies in the first-order case…
  with root 1/φ». La nota infravalora la fuente.
- **c2-m3-05**: la nota dice que la ec. (3.6.2) de Cryer y Chan es «la misma que el capítulo escribe arriba».
  No lo es: Cryer y Chan escriben r_k (suma de n − k productos entre una suma de n cuadrados); el capítulo
  escribe γ̂_k con 1/T. Son equivalentes y la cita respalda la frase.
- **c2-m3-15** (`pendiente`): aunque llegue la 4.ª ed., la 3.ª no respalda «sesgo pequeño hacia cero» ni «que
  los algoritmos de estimación necesitan» (`shumway2011time/p0042.txt:20–29` habla de función definida no
  negativa y de que ningún divisor da un estimador insesgado). El motivo es cierto; la frase probablemente
  tendrá que ajustarse igual.
- **c2-m4-06**: la cita va sobre «Eso permite pasar de la solución de orden k−1 a la de orden k»; el «eso»
  (Toeplitz) es del capítulo y la nota lo dice. Es una observación matemática evidente sobre la matriz
  escrita; firmo.
- **c2-m9-24** (`pendiente`): la frase escribe en prosa «En la 3.ª edición (2011) son las secc. 1.4–1.6 y 2.3».
  Comprobado en el índice de la 3.ª ed. (`shumway2011time/p0010.txt:12–22`). Es una edición que el curso no
  cita, con año, sin `<cite>`.
- **c2-m7-14**: la marca empieza a mitad de frase («la serie del modelo airline…») y la cita queda tras «el
  Capítulo 5»; se lee bien.

## 6. Guiones

| guion | qué hace |
|---|---|
| `comprobaciones/v4_extrae.py` → `.out` | por entrada: texto marcado con las citas en su sitio; cada cita literal localizada en la caché (archivo, línea, página o sección, contexto) |
| `comprobaciones/v4_software.R` → `.out` | divisor de `acf()`; `pacf()` frente a Durbin–Levinson y frente a k regresiones MCO; `k` de `adf.test` y su regresión; avisos de tablas; KPSS 0.368 / 0.537 y 0.463; `ndiffs`/`nsdiffs`; 2(1−r1); `BoxCox` con negativos; λ de Guerrero |
| `comprobaciones/v4_software.py` → `_py.out` | `acf(adjusted=False)`; `pacf` ywm, ldb y ols frente a Durbin–Levinson (statsmodels 0.14.6) |
| `comprobaciones/v4_sin_marca.py` → `.out` | apellidos y giros de atribución en la prosa fuera de toda marca |
| `comprobaciones/v4_firma.py` → `.out` | escribe `verificado_por` en las 51 firmadas; no toca otro campo |
| `comprobaciones/v4_audita.out` | auditor, `git diff --stat -- Htmls_Series` y `ensambla_cap3.py` tras firmar |
| `comprobaciones/v4_navegador.out` | medidas a 375 px por HTTP |

## 7. Dónde difiere mi lectura de `R4_cambios.md` (leído al terminar)

**Coincidimos** en las 8 `pendiente` y sus motivos, en 8 de las 9 `propia`, en las frases reescritas de
c2-m4-12, c2-m7-05, c2-m4-09, c2-m1-04, c2-m8-02, c2-m8-08, c2-m6-01, c2-m6-06 y c2-m9-24 (las firmé), y en el
F11: el redactor ya lo había dejado como primer punto abierto («Lo que no cierra», 1).

**Difiero en:**

1. **Colocación.** El redactor dice que leyó las 72 citas en su frase y que «ninguna cae… entre un sustantivo y su
   complemento». Dos sí lo hacen: **c2-m4-02** (la cita entre «la regresión» y su ecuación, visible a 375 px) y
   **c2-m1-06** (la cita pegada a «las tres condiciones», cuando la página citada da dos). Y en **c2-m5-01** y
   **c2-m8-05** la cita va sobre la parte de la frase que la fuente no dice («Rara vez sirve…», «no significa nada
   para nadie»).
2. **`con-matiz` con la nota, o frase corregida.** El redactor dejó en `con-matiz` frases que dicen más que la
   fuente, con el matiz en la nota («No reescribí estas frases»). Para **c2-m3-13** («tendrán» frente a
   «sometimes») eso no basta: es la afirmación central de la frase, y propongo reescribirla. Y en siete entradas
   `respaldada` (c2-m2-01, c2-m2-09, c2-m3-01, c2-m4-01, c2-m5-07, c2-m7-01, c2-m8-01) la propia nota del redactor
   reconoce que la frase va más allá de la fuente: por el README, eso es `con-matiz` o una frase ajustada.
3. **Hallazgo nuevo, no tocado por el redactor: c2-m4-05.** «Ajustar la regresión del rezago k equivale a resolver
   Yule–Walker» es cierto en la población, no con datos (hasta 0.35 de diferencia en log(AirPassengers) con MCO;
   0.60 con `pacf(method="ols")`). Arrastra la frase de c2-m4-04 y la «regresión» de c2-m4-02.
4. **Hallazgo nuevo en una `propia`: c2-m7-08.** «En una muestra cualquiera el cociente sigue de cerca a 2(1−r1)»
   no se cumple en series no estacionarias. El redactor la dio por comprobada con la identidad poblacional.
5. **c2-m5-11.** El redactor la reescribió para quitar «por defecto» y los tipos de cambio; la frase nueva hace de la
   popularidad del modelo la causa de que el ingenuo gane. Propongo enlazarlo con «underpins naïve forecasts».
6. **Localizadores.** c2-m5-09 (FPP3 §9.1 no nombra «random walk with drift»; §9.3 sí) y c2-m6-04 (la regresión con
   constante y tendencia está en la p. 130, no en pp. 128–129). El redactor no los menciona.
7. **c2-m7-06.** La nota atribuye «casi en línea recta» a Cryer y Chan, que no figuran en sus `fuentes`.
8. **Atribuciones sin marca.** El redactor ya nombra el criterio de Guerrero en la prosa, las menciones del
   «modelo airline» y las lecturas tecleadas de Kwiatkowski et al. y Guerrero. Añado el **título del recuadro KPSS
   con los cuatro apellidos** (línea 3355), que nadie menciona, y «**se trabaja casi siempre** con una versión más
   manejable» (línea 2393).
9. **Notas inexactas en entradas firmadas** (no cambian el veredicto): c2-m5-05 (Cryer y Chan sí escriben el caso
   AR(1) con raíz 1/φ, nota al pie de la p. 71) y c2-m3-05 (la ec. 3.6.2 escribe r_k, no γ̂_k).

## 8. Segunda lectura (tras la corrección del redactor)

Fecha: 2026-11-17. Leí las 29 entradas cambiadas o nuevas con el mismo criterio que en la primera lectura.
No leí la sección «Tras la verificación» de `R4_cambios.md` antes de terminar.

**Resultado: firmo las 29.** El registro queda con **80 entradas firmadas de 80**. `audita_citas.py` sale
solo con **F11** (FPP3, ahora **902** palabras en el curso: las seis entradas nuevas añaden FPP3), sin F08
ni F09 ni ningún otro hallazgo (`comprobaciones/v4_audita_2.out`). El `diff` del registro contra la copia
previa da 29 líneas añadidas y 0 borradas.

**Comprobaciones previas**

- **Las 51 firmadas en la primera lectura no cambiaron.** Comparé campo a campo cada entrada contra la
  copia que guardé antes de firmar, quitando solo `verificado_por`: no hay ninguna diferencia, y F09 no
  salta, así que la prosa marcada tampoco cambió.
- Las 29 citas literales están en su localizador. Las que caen en la página siguiente son todas rangos
  `pp. N–N+1` (`comprobaciones/v4_extrae_2.out`; `v4_extrae.py` admite ahora una lista de ids).
- **Se dibujan bien a 375 px por HTTP**, en los nueve módulos con los desarrollos abiertos: 79 citas visibles,
  `scrollWidth` 375 en todos, 0 citas fuera del ancho, 0 enlaces sin destino, 0 `.katex-error`. Miré tres
  dibujadas:
  - c2-m4-02: la cita va ahora antes de los dos puntos y la ecuación queda debajo;
  - c2-m6-18: la cita va en el título del recuadro del KPSS y toma su tipografía, sin desbordar;
  - c2-m1-06: la cita va tras «débilmente estacionario».
- **No hay atribuciones nuevas sin marca.** `v4_sin_marca.py` (`v4_sin_marca_2.out`) ya no encuentra el título
  del KPSS, «se trabaja casi siempre» ni las lecturas tecleadas. Siguen sin marca, como nombre repetido,
  las menciones del «criterio de Guerrero» / «λ de Guerrero» en la prosa (líneas 4262, 4283, 4483 y 4793) y en el código. La primera mención ya lleva la
  atribución (c2-m8-13). Lo doy por suficiente.
- `git diff --stat -- Htmls_Series`: solo el capítulo 2. `ensambla_cap3.py`: «reproducible byte a byte».

**Lo que comprobé ejecutando** (`comprobaciones/v4_software_2.R` → `.out`)

- **c2-m4-04**: la frase dice que la PACF muestral «no coincide exactamente» con el último coeficiente por
  mínimos cuadrados. La distancia máxima (k = 1…24) entre `pacf()` y ese coeficiente es esta:

  | serie | diferencia máxima |
  |---|---|
  | log(AirPassengers) | 0.35 |
  | ∇∇12 log(AirPassengers) | 0.063 |
  | AR(1) simulado, φ = 0.5, n = 144 | 0.016 (mediana) |
  | AR(1) simulado, φ = 0.8, n = 144 | 0.025 (mediana) |
  | AR(1) simulado, n = 500 | menos de 0.01 |

  «No coincide exactamente» es justo para las series estacionarias, que es donde se usa la PACF. El
  valor de `maestra_r4.out` que cita la nota (0.602 en k = 12, statsmodels `ols`) es el que ya vi.
  `con-matiz` es el veredicto justo, porque lo del software no sale de la fuente.
- **c2-m7-08**: en muestras de series estacionarias simuladas (n = 200, 500 réplicas por φ ∈ {0, 0.5, 0.8,
  0.95}), la mediana de |cociente − 2(1−r1)| va de 0.004 a 0.008 y el máximo de 0.045 a 0.090. El signo
  coincide siempre salvo 12 de 500 casos con φ = 0.5, donde r1 ronda 0.5. La frase acotada es cierta. Los
  dos contraejemplos del párrafo siguen sirviendo: el segundo tiene raíz unitaria y muestra que la varianza
  puede subir con la diferencia que hace falta.

**Las lecturas y la atribución del KPSS.** En c2-m6-18, c2-m9-23, c2-m9-25 y c2-m9-26, el veredicto
`respaldada` se apoya en lo que FPP3 y Hamilton dicen de esas obras, no en haber leído los artículos.
Eso basta para lo que las frases afirman ahora, que es solo esto:

- el nombre de la prueba y sus cuatro autores: FPP3 §9.1, «Kwiatkowski-Phillips-Schmidt-Shin [literal fuera de git: `_local/citas/cap2.yml`, c2-m6-16 · fuente 2]; Hamilton p. 532;
- que el artículo es aquel «al que se atribuye» la prueba (ya no «el artículo original»);
- que Guerrero (1993) es el criterio que el Módulo 8 usa para elegir λ (FPP3 §3.1, `decomposition.txt:77`);
- que FPP3 tiene esas secciones con esos temas (títulos leídos en la caché);
- la ficha bibliográfica: está en la bibliografía de FPP3 y en `referencias.json`, que viene de Crossref.
  Las páginas 159–178 del KPSS salen ilegibles en la caché y coinciden con Crossref.

Nada de eso dice qué contienen los artículos: lo que dependería de leerlos sigue `pendiente` en c2-m6-05 y
c2-m8-04.

Un detalle de los localizadores `§9.12` y `§3.8` de las fichas: la instantánea es la página del capítulo
entero, y la lista de referencias va al final, después de «Further reading». Ahí la encuentra quien abra la
página. Ninguno de los dos es una cita visible: las visibles son §9.1 y §3.1, que son las correctas.

**Firmadas en esta lectura (29), con lo que cambió**

| id | qué cambió | por qué ahora se sostiene |
|---|---|---|
| c2-m1-05 *(nueva)* | «se trabaja casi siempre» → «se trabaja», con Cryer y Chan p. 17 y Hamilton p. 46 | los dos manuales llaman «estacionaria» a la versión débil; «más manejable» es una valoración obvia, declarada en la nota |
| c2-m1-06 | cita movida tras «débilmente estacionario» | ya no dice que la p. 17 enumere tres condiciones |
| c2-m1-15 | se añade Cryer y Chan p. 55 (cap. 4, ARMA = modelos para series estacionarias) | el registro cubre ya las dos mitades; la cita visible sigue en p. 16 (observación: podría añadirse la p. 55 a la vista) |
| c2-m2-01 | `con-matiz` | la nota declara el matiz |
| c2-m2-08 | «no es evidencia de nada» → «no basta como evidencia» | `con-matiz` con la nota completa |
| c2-m2-09 | «es bueno cuando…» → «Un buen modelo… ha exprimido… y lo que sobra es indistinguible del ruido blanco» | condición necesaria, como en FPP3 §5.4 |
| c2-m3-01 | «cuánto se parece» → «la relación lineal» | literal de FPP3 §2.8 |
| c2-m3-13 | «tendrán» → «Dos series no estacionarias independientes **pueden** mostrar…» | coincide con Cryer y Chan («sometimes», dos IMA(1,1) independientes). Observación: «con series no estacionarias, los estadísticos habituales mienten» generaliza la regresión espuria de Hamilton (que excluye el caso cointegrado), pero Cryer y Chan p. 263 lo sostienen para la correlación cruzada; lo acepto en un capítulo que aún no ha presentado la cointegración |
| c2-m4-01 | «aparecerán» → «pueden aparecer» | «might», FPP3 §9.5 |
| c2-m4-02 | ahora «último coeficiente de la mejor predicción lineal… (Hamilton, 1994, p. 111):» | definición poblacional de Hamilton; cita antes de los dos puntos (comprobado dibujado) |
| c2-m4-04 | reescrita: PACF muestral = recursión con r; coincide con `pacf()`; no coincide exactamente con MCO; `con-matiz` | comprobado arriba |
| c2-m4-05 | «Ajustar la regresión equivale…» → «Los coeficientes de la definición satisfacen el sistema de Yule–Walker» | es la afirmación poblacional de Cryer y Chan p. 114 |
| c2-m5-01 | «Rara vez sirve…» → «Es una no estacionariedad menos razonable que la de φ = 1» | paráfrasis directa de la p. 89. Lo que el capítulo enseñaba (el caso explosivo no es el útil) sigue ahí |
| c2-m5-07 | `con-matiz` | la nota declara que el 0.95, la monotonía en T y los correlogramas son del capítulo |
| c2-m5-09 | cita visible → Hamilton p. 436; FPP3 §9.3 añadida | Hamilton nombra «random walk with drift» |
| c2-m5-11 | «y eso explica» → «como su pronóstico es el último valor observado» | FPP3 §9.1, [literal fuera de git: `_local/citas/cap2.yml`, c2-m5-11 · fuente 2] |
| c2-m6-04 | segunda cita visible (Cryer y Chan, p. 130) sobre una frase nueva | p. 130: «linear trend plus stationary error… we include [literal fuera de git: `_local/citas/cap2.yml`, c2-m6-04 · fuente 4]. `adf.test()` con esa regresión: comprobado en la primera lectura (−7.3186 en las dos) |
| c2-m6-18 *(nueva)* | título del recuadro KPSS con cita | FPP3 §9.1 da los cuatro apellidos; Hamilton p. 532 lo lista |
| c2-m7-01 | «la herramienta estándar» → «una manera» | «one way», FPP3 §9.1 |
| c2-m7-06 | Cryer y Chan p. 128 añadido a `fuentes` | sostiene «casi en línea recta» |
| c2-m7-08 (`propia`) | «en una muestra cualquiera… sigue de cerca» → «en una muestra de una serie estacionaria… se acerca» | comprobado arriba |
| c2-m7-11 | «En la duda, conviene diferenciar de menos» → «No conviene diferenciar más de lo necesario» | [literal fuera de git: `_local/citas/cap2.yml`, c2-m7-11 · fuente 5], FPP3 §9.1. Se pierde el matiz asimétrico, pero lo que queda es cierto y sigue enseñando lo esencial |
| c2-m8-01 | «arregla la media, pero no la varianza» → «estabiliza la media; para la varianza hace falta una transformación» | reparto de papeles de FPP3 §9.1 |
| c2-m8-05 | cita de FPP3 movida a «variaciones porcentuales» | la hipérbole queda sin cita; `con-matiz` |
| c2-m8-13 *(nueva)* | «el criterio de Guerrero… —el que Hyndman y Athanasopoulos (2021, §3.1) ofrecen para elegirla—» | FPP3 §3.1: «The guerrero feature… can be used to choose a value of lambda». Observación: «elegirla» (la lambda) convive en la misma frase con «el λ que elige R»; el resto del capítulo dice «el λ». Es concordancia, no fuente; si se cambia a «elegirlo», la huella cambia y vuelve a pedir firma |
| c2-m9-01 | nota completada («siempre» y «porque…» son del capítulo) | `con-matiz` con la nota completa |
| c2-m9-23 *(nueva)* | lectura de FPP3 con cita generada y títulos de sección como citas | las secciones existen con esos temas |
| c2-m9-25 *(nueva)* | lectura de Kwiatkowski et al.: «el artículo al que se atribuye la prueba KPSS» | ver arriba. Observación de estilo: la ficha tecleada usa «&» y la del generador, «y» |
| c2-m9-26 *(nueva)* | lectura de Guerrero (1993) | ver arriba; misma observación |

**Sin firmar en esta lectura: ninguna.**

**Queda abierto, fuera de las firmas**

1. **F11.** FPP3 suma 902 palabras citadas en el curso frente a un tope de 400. Decide Javier si el tope es
   por capítulo o por curso, o si hay que recortar.
2. Las observaciones de las secciones 5 y 8: notas inexactas en c2-m5-05 y c2-m3-05; la concordancia de
   c2-m8-13; las fichas tecleadas con «&». Ninguna cambia un veredicto.

**Comparación con «Tras la verificación» de `R4_cambios.md` (leída al terminar).** Lo que el redactor dice
coincide con lo que leí: 80 entradas, 79 citas visibles, las 51 firmadas intactas, y FPP3 en 902 palabras en el
curso. No señala dos cosas que anoto como observaciones: la concordancia «elegirla» de c2-m8-13 y la
generalización de la segunda frase de c2-m3-13. Sobre c2-m9-01 explica por qué no movió la cita (habría
separado el sustantivo de su relativa); con la nota completa, la acepto.
