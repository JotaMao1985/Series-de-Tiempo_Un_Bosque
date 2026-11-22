# Capítulo 3 · ronda R4 «fuentes» · verificación independiente, lote B (M7–M10)

Fecha: 2026-11-21. Verificador independiente (subagente, contexto limpio): no redactó nada de esta ronda.
Leyó `CLAUDE.md`, `bibliografia/README.md` y `diagnostico/cap2/R4_verificacion.md`. No leyó
`diagnostico/cap3/R4_cambios.md` hasta terminar las secciones 1 a 5; la 6 es la comparación.

No toqué nada fuera de `diagnostico/cap3/`: ni la prosa, ni `cap3.yml` (no escribí `verificado_por`: la firma
está en `comprobaciones/v4_firmas_B.txt`), ni el JS. Sin commits. Ningún literal de fuente en este archivo: los
pasajes se señalan por obra, página y línea de la caché.

## 1. Resultado

| | entradas |
|---|---|
| Lote B (`c3-m7-*` a `c3-m10-*`) | 116 |
| **Firmadas** | **110**: 52 `respaldada`, 29 `con-matiz`, 25 `propia`, 4 `pendiente` |
| **Sin firmar** | **6**: c3-m7-02, c3-m7-35, c3-m8-09, c3-m8-36, c3-m9-20 (`con-matiz`) y c3-m9-23 (`propia`) |

Qué significa la firma: leí el pasaje en la caché (todas las citas literales están en su página o sección; la
única que cae en la página siguiente es la 2.ª de c3-m10-20, dentro de su rango `pp. 114–115`) y el veredicto, el
localizador y la nota son correctos; en las `propia` repetí la cuenta o la derivación; en las `pendiente`, el
motivo es cierto (no hay en la biblioteca obra de aprendizaje profundo; Guerrero, 1993, y Shumway y Stoffer 4.ª
están en `referencias.json` sin texto en `_local/texto`).

`git diff HEAD -- ensamblado/cap3/cap3_js.js` está vacío: la ronda no tocó el quiz, la práctica de repaso ni el
simulacro.

## 2. Hallazgos

### 2.1 Graves (algo falso o una cita que no dice lo que se le atribuye)

| id o lugar | qué está mal | propuesta |
|---|---|---|
| **c3-m7-02** (nota y 5.ª fuente) | La nota dice que Cryer y Chan (p. 66) hacen de **este** trabajo el origen de los procesos AR y que lo «fechan en 1926» porque se recibió en diciembre de 1926. Falso: su «Yule (1926)» es **otro artículo**, *Why do we sometimes get nonsense-correlations between time-series?*, JRSS 89(1), 1–63 (bibliografía de Cryer y Chan, `cryer2008time/p0495.txt`). Ninguna obra leída atribuye el AR al artículo de 1927. La frase visible («propuso en 1927 lo que hoy se llama un modelo autorregresivo») no queda falsa —Yule ajusta en la Sección III la regresión de uᵪ sobre uᵪ₋₁ y uᵪ₋₂ con constante, ec. (31), p. 281, que es un AR(2)—, pero esa equivalencia es lectura del capítulo, no de Cryer y Chan | Quitar Cryer y Chan p. 66 de `fuentes` (o dejarla diciendo que cita el artículo de 1926) y reescribir la nota: «que la ec. (31) de Yule sea un AR(2) es lectura del capítulo al compararla con la definición del Módulo 2». Además el localizador de los años es la p. 275, que está en la Sección II (método armónico); la regresión con los mismos años, 1749–1924, es la **p. 281**: mejor `p. 281` o `pp. 275, 281` |
| **Referencias (M7, M9, M10 y lista del capítulo)** | El título de Yule sale **sin la palabra «in»**: «…investigating periodicities disturbed series…». La portada leída (p. 267, `yule1927method/p0001.txt:2`) dice «Periodicities in Disturbed Series»; el error viene de Crossref (`referencias.json`, `obras.tsv`). Lo ve el estudiante cuatro veces | Enmienda con evidencia (portada, p. 267) en `enmiendas.yml` o corrección en Zotero, y `genera_referencias.py`. Lo mismo arrastraría cualquier capítulo que cite a Yule |
| **c3-m9-20** | La cita visible de Hyndman y Khandakar (2008, p. 16) cierra la frase «…se queda con el de menor **AICc**». El artículo elige por **AIC** en todo el algoritmo (pp. 9–11; `hyndman2008automatic/p0010.txt:36–47`, `p0011.txt:12–25`). La nota lo reconoce, pero la cita va justo sobre el dato que la fuente no dice (el criterio del cap. 2 en c2-m5-01) | Mover la cita tras «ajusta por sí sola varios modelos ARIMA» y escribir «y se queda con el de menor AICc —el artículo original usaba el AIC; el AICc es el criterio por defecto del paquete actual—». Lo del AICc por defecto lo comprobé (`formals(auto.arima)$ic`, forecast 9.0.2) |

### 2.2 Juicios (el veredicto o la redacción deberían cambiar; discutibles)

| id o lugar | qué falla | propuesta |
|---|---|---|
| **c3-m8-09, c3-m8-36** · notación Q / Q* | Comprobado: FPP3 §5.4 (`toolbox.txt`) y Cryer y Chan pp. 183–184 llaman **Q** a Box–Pierce y **Q\*** a Ljung–Box; el capítulo, al revés (Q(h) = Ljung–Box en el recuadro; Q*(h) = Box–Pierce en el desarrollo). Confunde justo donde se cita: c3-m8-36 dice que «con el factor T, **Q\*** sale pequeño» y cita la p. 184, donde se lee **Q\* > Q** con los símbolos opuestos. En el resto del curso solo el cap. 4 escribe el estadístico, como Q_LB(24) y Q = 222.4 para Ljung–Box (el Q del cap. 6 es la escala del MASE), y nadie usa Q* | No tocar Q(h) de Ljung–Box (coincide con el cap. 4). Renombrar el de Box–Pierce del desarrollo plegado como **Q_BP(h)** (dos fórmulas y el «Q\*» de c3-m8-36) y añadir una línea: «FPP3 y Cryer y Chan escriben Q para este y Q\* para el de Ljung–Box». Cambia la huella de c3-m8-09 y c3-m8-36: volverían a pedir firma, que daría |
| **c3-m7-35** | «CSS es más barato y sirve para arrancar; **ML es más preciso**» con Hamilton p. 123 al final. Hamilton (`p0138.txt`) dice que el condicional es trivial de calcular, que los dos tienen la misma distribución en muestra grande y que, con \|φ\| > 1, el condicional sigue siendo consistente y el exacto no. «Más preciso» no está y la cita cubre la frase entera. La nota lo declara, pero la frase lo afirma sin condición | Mover la cita tras «más barato» y escribir «…ML usa además la densidad de las primeras observaciones, que pesa con series cortas (Cryer y Chan, p. 158)», o «más preciso con series cortas» como frase del capítulo, sin la cita de Hamilton encima |
| **c3-m9-23** (`propia`) | «El mejor pronóstico de la variación del mes que viene es la media histórica», y dos párrafos más abajo el capítulo elige, por AICc, el ruido blanco **sin** media (pronóstico 0; la media estimada, 0.2681 % con e.e. 0.3195, `v4B_software.out`). El estudiante recibe dos respuestas | «…es una constante: la media histórica, o cero si, como aquí, la media no se distingue de cero» |
| **Pie de la tabla ordenable (`cap3_js.js:1433`)**, M8, visible | «El AR(2) **de Yule** —la fila marcada—» sobre el ajuste a 1770–1869 crudo (φ̂ = 1.4059, −0.7111). Yule ajustó a 1749–1924 (y a los números graduados de 1753–1920) y obtuvo 1.34254 y −0.65504 con constante (ec. 31, p. 281). Sugiere que Yule ajustó esa ventana, lo mismo que la ronda corrigió en cuatro sitios del M10 | «El AR($2$) —la fila marcada, el que proponía la identificación—…» (regenera el HTML; el JS es fuente del ensamblado) |
| **«número de Wolf» (`cap3_js.js:1060`, `:1252`)**, rótulos visibles de dos simuladores | Ninguna obra leída usa el término (grep en toda la caché: cero apariciones; la ayuda de `sunspot.year` dice solo «Yearly numbers of sunspots»). Además choca con el «Wolfer» del recuadro del M7: el estudiante lo leerá como errata. Es la atribución que la ronda retiró de la prosa (c3-m7-01) | «Manchas solares (número anual)» y «original». Arrastre no visible: `genera_cap3.R:566–571` (`descripcion` «(Wolf)», `unidad` «numero de Wolf») y el comentario de `:200` («el primer modelo autorregresivo», misma falta de fuente que c3-m7-02) |
| **Comentario de código visible, M9** (bloque R del caso 1, `cap3_modulos.html:3022`) | «el ciclo solar documentado es ~11»: la ronda quitó de la prosa «documentado por los astrónomos» por no tener obra, y sigue en el código que se muestra | «# la estimación habitual del periodo es algo más de 11 años (Módulo 9)» |

### 2.3 Observaciones sobre entradas firmadas (no impiden la firma)

- **c3-m8-24 frente al M10.** El M8 dice «Añadir parámetros **siempre** mejora la verosimilitud»; el M10 (sin marca),
  «**casi siempre** mejora». Las dos se sostienen (con el máximo exacto y datos continuos, la mejora es estricta casi
  seguro; nunca empeora: `v4B_software.out`), pero el estudiante ve dos versiones. Unificar en «nunca empeora».
- **c3-m7-09.** «Aprovecha toda la información de los datos» se apoya en Cryer y Chan p. 158, que lo dicen frente a
  usar solo los dos primeros momentos (mínimos cuadrados), no frente a ignorar la primera observación; y p. 158 no es
  cita visible. Se lee bien; la nota podría decirlo.
- **c3-m7-15 y todas las citas a la ayuda de R.** El localizador visible «(R Core Team, 2026, §Details)» no dice de
  qué página de ayuda (aquí `?ar`, en c3-m8-13 `?Box.test`, en c3-m7-09 `?arima`). Quien abra la cita no sabe dónde
  buscar. Es del diseño del generador, no de esta ronda: «§Details de `?ar`» o el nombre de la función en el `title`.
- **c3-m7-03 / c3-m9-06.** Correctas. Yule da el periodo de su ajuste por regresión sobre 1749–1924 en 10.60 años
  (p. 281) y sobre los graduados en 11.16 (p. 282); el capítulo no lo usa, y está bien así.
- **c3-m7-02 (frase).** Fiel en lo demás: serie usada entera (p. 275), regresión sobre los dos anteriores y el
  péndulo con impulsos al azar (pp. 268 y 294). No dice que Yule también trabajó con números graduados (1753–1920);
  no hace falta.
- **c3-m9-45.** Repetida: pico 11.8361, fórmula de FPP3 11.8364, ángulo 11.2185; con R → 1 se juntan (0.999:
  11.2183). La nota da 11.8362 para R = 0.828; a mí me sale 11.8346 con R redondeado. Irrelevante.
- **c3-m9-50.** Forma cerrada (m²−1)/(2(2m²+1)) = 0.2492 con m = 21, igual a la suma de pesos; la simulación da
  r₁ medio 0.234 (el redactor anota 0.237 y 0.254 en distintas corridas: es el sesgo muestral de r₁ hacia abajo,
  no contradice el 0.25 teórico).
- **c3-m10-41, c3-m10-39.** Fichas tecleadas con «&» y sin año (Box et al. 5.ª; Shumway y Stoffer 4.ª), mientras
  las generadas usan «y». Las dos obras están en `referencias.json` (`box2016time`, `shumway2017time`); podrían ir
  por `genera_referencias.py` como en el cap. 2.
- **Objetivo del M10** (sin marca): «Situar el AR como el **punto de partida** de los métodos secuenciales…». Se
  puede leer como punto de partida didáctico, que es lo que el módulo hace; si se lee como genealogía, vuelve la
  afirmación histórica que la ronda retiró del cuerpo (c3-m10-02).
- **Cita fuera de la vista a 375 px.** Solo una en mis módulos: c3-m10-20, en la columna «De dónde sale el orden» de
  la tabla de identificación del M10 (`right = 466` dentro de `table.tabla-sigue-der`, que se desplaza en su
  contenedor y marca que sigue a la derecha). Es la columna entera la que queda fuera, no la cita; la página no
  desborda (375/375). No importa. (La captura `v4B_m10_tabla_375.png` salió de la primera tabla con cita, la del
  puente con las redes: muestra el mismo patrón, la tercera columna asoma a la derecha.)

## 3. Lo que comprobé ejecutando (`comprobaciones/v4B_software.R` → `.out`; `v4B_software.py` → `_py.out`)

R 4.6.0, forecast 9.0.2, statsmodels 0.14.6. Todas las cifras de las `propia` se reproducen:

| entradas | resultado |
|---|---|
| c3-m7-11, -33, -34 | set.seed(1): CSS 1.0086, ML 0.9808. 12 semillas × 1000: CSS > 1 entre 2.5 y 4.6 %; **ML > 1 en ninguna**; ML ≥ 0.999 entre 12.59 y 16.57 %; ML sin estimación de 4 a 13 por mil |
| c3-m7-13 | Otra semilla, 1000 réplicas del AR(2) de las manchas, T = 100: media YW (1.3448, −0.6668), ML (1.389, −0.705); módulo medio de la raíz YW 1.231 > ML 1.196 > verdadero 1.186. AR(1) φ = 0.95: media YW 0.893 |
| c3-m7-16, -17 | firma `yule_walker(x, order=1, method='adjusted', …)`; docstring: n para «mle», n−k para «adjusted»; adjusted (1.3616, −0.6719), mle (1.3173, −0.6338) = `ar()` de R |
| c3-m8-24 | logLik de las once: las cadenas anidadas no decrecen |
| c3-m8-15, -35 | set.seed(8), 3000 réplicas: sin fitdf 0.0257, con fitdf 0.0490; cociente 0.524 |
| c3-m8-11 | 20 000 series de ruido blanco, T = 50: varianzas de r_k 0.0188, 0.0183, 0.0172, 0.0155, 0.0117 frente a (T−k)/(T(T+2)) 0.0189, 0.0185, 0.0173, 0.0154, 0.0115 y 1/T = 0.02 |
| c3-m8-18 | R: residuales 21.056, −6.911, 8.728, −15.396; γ₀/σ² = 6.226; 21.056·√6.226 = 52.538; factor del 2.º 1.422. statsmodels: 52.536, −9.829, 8.727, −15.397. LB(12): R 0.0461, statsmodels 0.1085; sin los dos primeros, 0.0232 en los dos |
| c3-m10-14 | LB(12) del AR(2) crudo: 0.0461 con fitdf = 2, 0.0996 sin él |
| c3-m9-05, -43 | un cero en 1770–1869 y tres en 1700–1988; sin desplazar 0.3333 con el aviso de «strictly positive data»; con +1, 0.3062; `guer.cv` toma `nonseasonal.length = 2` |
| c3-m9-08, -47 | periodo/LB: raíz 11.2178/0.1644, Guerrero 11.3883/0.4892, desplazada 11.2759/0.2216. Σψ² = 6.136, σ² = 1.341, producto 8.228, varianza muestral 8.149, semiancho límite 5.62 |
| c3-m9-41 | derivación delta: sd(y^λ) ∝ μ^(λ−1+b), constante si y solo si λ = 1 − b (no hacía falta simular) |
| c3-m9-20, -24, -52 | `ic` por defecto «aicc», `stepwise = TRUE`, `approximation = (length > 150 ‖ frequency > 12)` → FALSE con 137 datos mensuales; por defecto ARIMA(0,0,0) sin media (AICc 722.663); exhaustiva, con y sin `approximation`, MA(1) sin media, θ = 0.1326 (722.653); con media 723.804 y 724.046 |
| c3-m10-28 | máx \|ΔACF\| = 1.1·10⁻¹⁶; raíces AR 1.4286 y 2.5, MA 2.5 y −2 |
| c3-m10-24 (nota) | PACF del ARMA(1,2) de la nota: 0.717, −0.257, −0.109, 0.163… (no se corta tras p) |
| c3-m10-35 | 190 ventanas: pasan 52, fallan 138, 49 de ellas antes de 1900; inicios que pasan 1700–1785, el único fuera de 1734–1785 es 1700; ninguna que llegue a 1900 pasa. p = 0.000668 (1870–1988), 0.00102 (1900–1988), 0.000601 (1889–1988), 2.6·10⁻⁷ (completa) |
| c3-m10-25 | t = 19.31 y −9.46 (AR(2) sobre la raíz); θ̂ = 0.3732, t = 2.78 (ARMA(2,1) crudo) |
| c3-m9-17, -49, c3-m10-33, -92, -94 | remisiones internas leídas: cap. 2 (ADF y KPSS sobre la TRM y su diferencia; `aggregate(valor ~ mes, …, FUN = mean)`), cap. 4 (4.1, 4.2, 4.3, 4.6 «El AIC no cruza la frontera de d», 4.7), cap. 5 (5.5, 5.7), cap. 6 (6.7); AirPassengers aparece una sola vez en `cap3_modulos.html` y ninguna en `cap3_js.js` |

## 4. Navegador (`comprobaciones/v4B_recorrido.js` → `.out`, `.json`)

Servidor `python3 -m http.server 8857` sobre `Htmls_Series/` (md5 servido = md5 del archivo), Chrome sin ventana por
CDP (puerto 9261), módulos 7–11 a 1200 y 375 px, con todos los `<details>` abiertos. Servidor y Chrome detenidos.

- Citas visibles: M7 22, M8 21, M9 31, M10 26 (100); 0 vacías, **0 enlaces sin destino** (todos llevan a la lista
  del módulo abierto), 0 `.katex-error`, 0 «$» sin componer, `scrollWidth` 375/375 y 1200/1200 en todos, sin
  excepciones ni errores de consola (solo el 404 de `favicon.ico` del servidor de prueba).
- Fuera del ancho a 375 px: solo c3-m10-20 dentro de la tabla desplazable (§2.3). El M11 no tiene citas.
- La fórmula `$|w| < 1$` de c3-m10-08 lleva un «<» sin escapar en la fuente; el navegador lo trata como texto y
  KaTeX la compone (0 errores). Escaparlo como `&lt;` sería más seguro, no urgente.

## 5. Atribuciones sin marca (`comprobaciones/v4B_sin_marca.py` → `.out`)

Fuera de las marcas, en M7–M10, solo quedan nombres repetidos de métodos (Yule–Walker, Ljung–Box, Box–Cox,
Shapiro–Wilk, «de Guerrero»), código y las listas de referencias. Las que importan ya están en §2.2–2.3: el comentario
«ciclo solar documentado», el «casi siempre» del M10 y el objetivo del M10. «Guerrero exige datos estrictamente
positivos» (M9, sin marca) repite c3-m9-05 y es comportamiento de forecast, comprobado.

## 6. Comparación con `R4_cambios.md` (leído al terminar)

**Coincidimos** en: el recuadro de Yule (1749–1924, la regresión de orden 2, el péndulo, los 11 años) y el cambio de
«la ventana de Yule» por «la ventana 1770–1869»; las cuatro `pendiente` y sus motivos; las `propia` (todas las cifras se
reproducen); y en los restos que el redactor deja abiertos: el pie «El AR(2) de Yule» y los rótulos «número de Wolf»
de `cap3_js.js`, la notación Q/Q* al revés (su punto 3), la tensión de c3-m9-23 (su punto 5) y la cita en la celda de
tabla a 375 px (su punto 8). En la notación propongo una salida concreta y barata (Q_BP solo en el desarrollo), y en
c3-m9-23 una frase.

**Difiero o añado:**

1. **c3-m7-02, nota falsa.** El redactor da a Cryer y Chan (p. 66) como respaldo de que el artículo de 1927 es el origen
   del AR, «fechado en 1926». Su Yule (1926) es el artículo de las correlaciones sin sentido en el JRSS, no este. No lo
   menciona.
2. **Título de Yule sin «in»** en las cuatro listas de referencias (error de Crossref). No lo menciona.
3. **c3-m9-20.** La cita de Hyndman y Khandakar cae sobre «menor AICc», que el artículo no dice (usa AIC). El redactor
   lo deja en la nota; propongo mover la cita y decirlo en la frase.
4. **c3-m7-35.** «ML es más preciso» con Hamilton p. 123 encima. El propio redactor anota que Cryer y Chan dan a ML y a
   mínimos cuadrados las mismas propiedades de muestra grande (p. 160), lo que agrava la frase en vez de sostenerla.
5. **Comentario visible «ciclo solar documentado»** en el bloque R del M9 y el **«siempre / casi siempre»** entre el M8 y
   el M10: no los menciona.
6. **Localizador de los años de Yule.** p. 275 es la Sección II (método armónico); la regresión que el recuadro describe
   usa los mismos años en la p. 281. Propongo `p. 281` o los dos.
7. **F07 de Yule** (su punto 1): `ejemplares.yml` lleva ahora «Revised February 17, 1927» en `edicion_comprobada`;
   es asunto del lote A y de la cadena, no lo verifiqué.

## 7. Segunda lectura (tras la «Segunda pasada» del redactor)

Fecha: 2026-11-21. Releí las 7 entradas contra la caché con `v4B_extrae.py` (todas las citas, en su página o sección).
**Firmo las 7** (`comprobaciones/v4_firmas_B2.txt`).

- **c3-m7-02** · firmo. La p. 281 es la correcta para los años: la cita queda sobre la frase que describe la regresión,
  y en la p. 281 está la ec. (31) bajo el rótulo «1749–1924» (`yule1927method/p0015.txt`). La p. 275 da los mismos
  años, pero para el método armónico; sigue en `fuentes`, y está bien así. La nota ya no atribuye a Cryer y Chan el
  origen del AR (su Yule, 1926, es otro trabajo).
- **c3-m7-35** · firmo. «Más barato» con Hamilton p. 123 («sirve para arrancar» es del capítulo, y la nota lo dice).
  Lo de las primeras observaciones en series de longitud moderada va con Cryer y Chan p. 158. Matiz menor que la nota
  podría precisar: Cryer y Chan hablan de los valores de arranque de los errores, no de las primeras observaciones.
- **c3-m8-09** · firmo. El desarrollo llama ahora Q_BP(h) al estadístico de Box–Pierce, y la nota da la correspondencia
  con la notación de las fuentes.
- **c3-m8-24** · firmo. «Nunca empeora» es exacto (logLik de las once, `v4B_software.out`). La nota conserva una frase
  vieja («“Siempre mejora” debe leerse…») que ya no corresponde a la prosa. Es limpieza, no cambia el veredicto.
- **c3-m8-36** · firmo. «Q_BP sale pequeño» y el paréntesis que da la notación de Cryer y Chan quitan el choque con
  «Q* > Q» de la p. 184.
- **c3-m9-20** · firmo. La cita de Hyndman y Khandakar va ahora tras «ajusta… varios modelos ARIMA» (p. 16), y la frase
  dice que el artículo usaba el AIC y el paquete, hoy, el AICc (comprobado: `formals(auto.arima)$ic`).
- **c3-m9-23** · firmo. «Una constante: la media histórica, o cero si… no se distingue de cero» coincide con el modelo
  sin media del párrafo siguiente (media 0.2681, e.e. 0.3195). La nota aún habla de la «tensión interna», que ya se
  resolvió: limpieza, sin efecto en el veredicto.
- **Notación en el M8** · coherente: Q(h) = Ljung–Box (recuadro, c3-m8-33 y «con ellas, Q»). Q_BP(h) = Box–Pierce en el
  desarrollo. $Q$ y $Q^{*}$ solo aparecen en el paréntesis que explica la notación de Cryer y Chan. El M9 y el M10 no
  usan el símbolo.
- **`cap3_js.js`** · `git diff HEAD` muestra solo 3 líneas: los dos rótulos pasan a «número anual» y el pie pasa a «El
  AR(2) —la fila marcada, el que proponía la identificación—». Las tres son correctas. El quiz, la práctica de repaso
  y el simulacro no se tocaron.
- **Comentario del código R del caso 1 (M9)** · ahora «la estimacion habitual del periodo es algo mas de 11 (Modulo 9)»
  (línea 3099): coincide con c3-m9-06. No queda «documentado» en los módulos. «Ciclo solar» sigue en la prosa sin
  marca (líneas 2841 y 2959) como nombre del fenómeno, sin atribución; no lo exige ninguna fuente.
- **Título de Yule** · «periodicities in disturbed series» en las 7 apariciones de la fuente ensamblada y del HTML
  final, y ninguna sin «in». La enmienda está en `enmiendas.yml`.
- **`genera_cap3.R`, sección 3** · el comentario es fiel: regresión sobre los dos valores anteriores (p. 281, ec. 31),
  la serie de Wolfer entera 1749–1924 (p. 275), no esta ventana. «(un AR(2))» es lectura del capítulo, como en
  c3-m7-02. Matiz menor: «un siglo de la serie a la que Yule…» da por hecho que `sunspot.year` (fuente: Tong, 1996) es
  la serie de Wolfer, y eso no se ha contrastado. «Un siglo de números anuales de manchas, la magnitud a la que…»
  sería más exacto. Las etiquetas `descripcion` y `unidad` ya no llevan «Wolf».
