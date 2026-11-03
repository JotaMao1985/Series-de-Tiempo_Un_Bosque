# Auditoría de las diapositivas del capítulo 5 · SARIMA

Versión auditada: `ddfecc3` (77 diapositivas, `capitulo-5-sarima.html`). Fecha: 2026-10-28.

**Cómo se hizo.**

- Lectura completa de `fuentes/capitulo_5.md`, contrastada con el capítulo y con los capítulos 1–4 y 6.
- Captura de las 77 diapositivas en Chrome sin ventana: todas caben a ≥ 88 % de escala.
- Un corrector independiente leyó la ortografía y la redacción (sección 6).
- Un cálculo nuevo en R 4.6 / forecast 9.0.2 para la afirmación del Módulo 10 (A2).

Las referencias son «diap. N» (número en el visor) y «L» (línea de la fuente) **de la versión auditada**. Después de la corrección el deck tiene 82 diapositivas, y los números ya no coinciden.

> **Estado al 2026-11-03.** En el deck se aplicaron las secciones 1, 2, 3, 4 y 6, sin gráficos nuevos y sin commit todavía.
>
> **Resultado.**
> - 82 diapositivas, un divisor por módulo (01–11).
> - Todas caben a ≥ 88 %.
> - `verifica_cifras_cap5.py`: 668/668, y los 4 bloques de R coinciden.
> - El recálculo en R (`verifica_directo_cap5.R`) reprodujo todo lo anterior y añadió tres cifras: el `auto.arima` sobre un seno anual (A2), su `nsdiffs` y los rezagos fuera con la banda de 131 (A4).
> - `verifica_docs_cap5.R` guarda ahora la ayuda de `ets`, `nsdiffs` y `snaive`, de donde salen las glosas nuevas.
> - Las fotos m1-1, m6-1, m7-1 y m11-1 se rehicieron con `recaptura_cap5.py`: los datos del simulador no cambian, solo el eje, los colores o la leyenda.
>
> **Lo que no se aplicó, y por qué.**
> - **Sección 5** (gráficos nuevos, `m8-1`/`m10-1`, diapositivas de respaldo): no se pidió.
> - **Cursivas de *airline*** en el objetivo de la portada, en los títulos de sección y en el título del bloque de código: el constructor no procesa Markdown ahí y mostraba los asteriscos.
> - **«Estación» frente a «estacionalidad»**: solo se unificó el par de la misma sección (diap. 68 y 75 de la versión auditada); el resto es una decisión de estilo.
> - **«Lo que se llevan…»** se conserva: es el cierre que fija la skill y el que usa el deck del capítulo 4.
> - **El capítulo no se tocó.** A1, A2, A5 y T12 están corregidos en el deck y anotados en las notas y en las observaciones de `verificacion_cifras_cap5.md`.

Prioridades:

- **Alta**: la diapositiva dice algo falso o que induce a error.
- **Media**: un término aparece antes de definirse, o hay una incoherencia entre diapositivas.
- **Baja**: forma.

---

## 1. Contenido: afirmaciones que no se sostienen (prioridad alta)

| # | Diap. · L | Qué dice | Problema | Propuesta |
|---|---|---|---|---|
| A1 | 50 · L774 (también 27 · L422) | Raíces MA: «módulo inverso máximo 0.9524 · Invertible, aunque justo» | Ese 0.9524 es \|Θ̂\|^(1/12) = 0.5569^(1/12). La raíz duodécima acerca a 1 cualquier SMA(1): con Θ = 0.1 ya da 0.825. Así, «aunque justo» lee como alarma lo que es aritmética; Θ̂ = −0.557 (e.e. 0.073) está lejos de −1. **El capítulo dice lo mismo (Módulo 7).** | Leer la invertibilidad en Θ̂ (−0.557 frente a −1) y explicar una vez por qué el módulo de las raíces de 1 + ΘB¹² se pega a 1. En la tabla de sobrediferenciación (diap. 27), la columna \|raíz MA\|⁻¹ dice lo mismo que Θ̂ con menos claridad: quitarla o explicarla. |
| A2 | 64 · L982 | «Con frecuencia 365, `auto.arima` devuelve un ARIMA(0,0,0) sin parte estacional, y lo hace en silencio» | La serie del ejemplo es `ts(rnorm(800), frequency = 365)`: ruido blanco sin estación, y para ella ARIMA(0,0,0) es la respuesta **correcta**. Comprobación nueva: con una estación real (`3*sin(2*pi*t/365) + rnorm(800)`, semilla 1), `auto.arima` da **ARIMA(0,0,0)(0,1,0)[365]** y `nsdiffs` = 1: sí ve la estación, y paga 365 de 800 observaciones sin estimar ningún Φ ni Θ. **El capítulo usa el mismo ejemplo (Módulo 10).** | Cambiar el ejemplo por una serie con estación y la lección por «gasta 365 observaciones en una diferencia y no puede poner Φ ni Θ», que es la primera fila de la tabla. |
| A3 | 18 · L265 | Título: «el error llega al 33 %» | La tabla llega a −54.9 % (φ = 0.95) | «…y el error pasa del 50 %», o «33 % con φ = 0.9» |
| A4 | 48 · L739–740 frente a 50–51 · L773, L787 | La diap. 48 insiste: «La banda usa las 131 observaciones que quedan tras diferenciar, no las 144» (±0.171) | Dos diapositivas después, los residuales se juzgan con ±0.163, que es 1.96/√144. La foto del simulador (m6-1) también usa 144. | Una línea que explique por qué (R devuelve 144 residuales, los 13 primeros casi nulos) o rehacer la banda con 131: el 23 (0.220) sigue fuera con las dos. |
| A5 | 56 · L856, L860 | «con el doble de error estándar»; «los errores estándar son el doble» | Los cocientes son 0.1228/0.0896 = **1.37** (θ) y 0.1784/0.0731 = **2.44** (Θ). Con n efectivos de 59 y 131, la teoría da √(131/59) ≈ 1.49. **El capítulo dice lo mismo (Módulo 8).** | «entre 1.4 y 2.4 veces mayores» |
| A6 | 60 · L921 y 61 · L943 | «β̂ = 1.084: justo lo que predice la aritmética»; «es el que predice la aritmética» | Con e.e. 0.4462 el IC95 es ≈ [0.21, 1.96]: no rechazar β = 1 no confirma β = 1. | «compatible con lo que predice la aritmética (β = 1), aunque con mucha incertidumbre» |
| A7 | 67 · L1025–1031 | La pregunta da el AICc de K = 5 (−521.2) y la opción 3 cuenta «16» parámetros | 16 es el total de K = 6; K = 5 tiene 15 (`n_par_total`). | Usar 15, o bien el AICc de K = 6 (−521.45) |
| A8 | 37 · L579 | «ψ_j = 1 + θ = 0.5982 hasta j = 11» | ψ₀ = 1, y el gráfico lo muestra (barra en j = 0) | «para j = 1, …, 11» |
| A9 | 44 · L674 | «Con 10 o 20 rezagos, una barra en 12 y otra en 24 apenas pesan» | Con 10 rezagos ni el 12 entra; con 20, el 24 queda fuera. No es que pesen poco: no están. | «Con 10 rezagos el 12 ni entra; con 20, el 24 tampoco» |
| A10 | 14 · L206–208 | Fórmula con **+φΦB¹³** y, debajo, «el 13 vale −φΦ» | Los dos signos son correctos en convenciones distintas (polinomio frente a y_t = Σ a_k y_{t−k}), pero la diapositiva no lo dice. Además, «los rezagos 2 a 11 valen cero» habla de coeficientes, y cinco diapositivas después la pregunta usa como trampa «la ACF es cero en 2 a 11». | «el coeficiente AR del rezago 13 en y_t = … es −φΦ»; «los **coeficientes** de 2 a 11 valen cero» |
| A11 | 64 · L973 | Título: «el SARIMA se rompe por tres sitios» | La tabla muestra dos problemas y una ventaja de Fourier. El tercer problema (365.25 no es un número entero de rezagos) solo está en las notas. | Poner el tercero en la diapositiva y la fila de Fourier aparte, o cambiar el título |
| A12 | 59 · L911 | <kbd>Definición</kbd> «su error estándar es mayor que el de un MCO ingenuo» | No es una definición ni vale siempre: lo que pasa es que el e.e. de MCO ignora la autocorrelación y suele **subestimar**. | Etiquetarlo como <kbd>Interpretación</kbd>: «el de MCO ignora la autocorrelación y suele quedarse corto» |

## 2. Términos que aparecen antes de definirse (coherencia narrativa)

Se comprobó en el texto de los capítulos 1–4 si cada término ya se había visto.

| # | Término | Primera aparición | Dónde se define | Propuesta |
|---|---|---|---|---|
| T1 | ***airline*** | diap. 5 (L60). Antes de definirse sale en las diap. 17, 20, 31 y 32 (una opción de pregunta) | diap. 35 (L542, Módulo 5) | Glosa en la diap. 5, «el *airline*, SARIMA(0,1,1)(0,1,1)₁₂, que es el Módulo 5», y nombrarlo en la diap. 20, cuyo código lo ajusta |
| T2 | **ETS**, ETS(M,A,M), ETS(M,A\_d,M) | diap. 69 (L1070), y gana la comparación | **Nunca**: 0 apariciones en los caps. 1–4; el cap. 5 solo lo nombra en la tabla final; se enseña en el cap. 6 | Una diapositiva «Quiénes compiten» antes de la pregunta de la diap. 69, una línea por método: ETS (y la lectura de M,A,M), naïve estacional, STL + ARIMA, regresión armónica |
| T3 | **MAPE**, **naïve estacional** | diap. 69–70 | Nunca (RMSE y MAE sí se usaron en el cap. 4, caso del Nilo) | La misma diapositiva, con las tres fórmulas |
| T4 | **∇ₘ, ∇∇₁₂** | diap. 16 (L236) y 17 (L254) | diap. 22 (L338, Módulo 3) | En el Módulo 2, escribir (1−B)ᵈ(1−Bᵐ)ᴰ, o adelantar la definición |
| T5 | **`nsdiffs()`**, `seas`, OCSB | diap. 25 (L392, en código) | La diap. 28 explica su cambio de prueba, pero nunca qué estima | Una línea: «`nsdiffs()` estima D como `ndiffs()` estima d». Y una glosa: `seas` = fuerza estacional de la descomposición STL (así lo dice el capítulo); OCSB = Osborn–Chui–Smith–Birchenhall |
| T6 | **satélites** | diap. 15 (L218), en el título | diap. 30 (L472), quince diapositivas después, como idea | Una línea de <kbd>Definición</kbd> en la diap. 15 |
| T7 | **espacio de estados**, ***prior* difuso** | diap. 46 (L708) | Nunca en el curso | Pasar el mecanismo a las notas y dejar en la diapositiva la consecuencia (`nobs = 144`) |
| T8 | **competencias M4 y M5**, Prophet, LSTM, Transformers | diap. 75 (L1164) | Nunca. «M4/M5» se confunde con los módulos 4 y 5 | «competencias M4 y M5 de Makridakis»; una línea de glosa por método en las notas |
| T9 | **origen móvil** | diap. 71 (L1099) | Una línea en la diap. 71; el método es del cap. 6 | Un esquema del origen que avanza (ver G11) |
| T10 | **STL** | diap. 68 | Cap. 1 (bien) | Recordarlo: «la descomposición del capítulo 1» |
| T11 | **SFC** | diap. 6 (L77) | Nunca | Superintendencia Financiera de Colombia |
| T12 | **Numeración de pasos** | diap. 47–53: «Pasos 0 y 1», «Paso 2», «Paso 3», «Paso 4» | diap. 33: el protocolo tiene etapas **1 a 5** | Alinear con el protocolo («Etapas 1–3», «Etapa 4»…) o decir que el caso numera distinto. **El capítulo usa «Paso 0…4».** |
| T13 | **Números de los divisores** | diap. 34: «**04** · Módulo 5»; diap. 42: «05 · Módulos 6–7»; diap. 55: «06 · Módulos 8–9»; diap. 63: «07 · Módulos 10–11» | — | El constructor numera las secciones en secuencia (`{k + 1:02d}`, construir.py:686). Hay dos salidas: una sección por módulo (01–11, cuatro divisores más), o un atributo `numero=` en la skill |

Otros detalles de coherencia:

- **Decimales de ρ̂₁₂ de ∇TRM.** La tabla de la diap. 9 da −0.002; la respuesta de la diap. 10 y la tabla de la diap. 57, −0.0025. Conviene una sola precisión.
- **Varianzas sin nombre.** La diap. 47 (L728) compara «0.002102, frente a 0.003800 y 0.011354» sin decir de qué son: solo ∇₁₂ y solo ∇.
- **Modelo «simple» sin nombre.** La diap. 57 (L876) no dice cuál es: es la caminata aleatoria, ARIMA(0,1,0).
- **«Por defecto».** La diap. 72 (L1122) dice «los 24 errores son por **defecto**», que se lee como «por omisión». Mejor: «todos por debajo de lo observado».
- **Leyenda con [12].** La foto de la diap. 69 escribe «(0,1,1)(0,1,1)[12]», a la manera de R; el resto del deck usa el subíndice ₁₂.
- **El rango relativo.** En la diap. 47, (máx − mín)/media = 1.848 mide cuánto se mueve el nivel, no que la amplitud crezca con él. La evidencia real está en el mapa mes × año o en el `ggseasonplot`, que el deck no muestra (ver G11).

## 3. Preguntas para la clase

| # | Diap. | Problema | Propuesta |
|---|---|---|---|
| Q1 | 24 | El enunciado no dice que la serie es **USAccDeaths**: solo lo dice la línea pequeña. Viene justo después del gráfico de AirPassengers, y en AirPassengers `ndiffs` crudo da 1 (diap. 28). | Nombrar la serie en el enunciado |
| Q2 | 32 | «Picos de 0.70, 0.49 y 0.34…» son los mismos números de la diap. 29, tres diapositivas antes: se responde copiando. | Moverla antes de la diap. 29, o usar otro Φ (habría que verificar los valores) |
| Q3 | 61 | Pregunta «¿Cuánto vale el t…?» y la respuesta se titula «No se rechaza» | Titular la respuesta «t = 0.188 · no se rechaza» |
| Q4 | 67 | La mezcla de K = 5 y K = 6 (A7) | — |

## 4. Gráficos

| # | Diap. | Observación | Propuesta |
|---|---|---|---|
| G1 | 8 (m1-1) | El eje y va de −1 a 1 y la mitad inferior queda vacía. Las barras de 12, 24 y 36, que son el mensaje de la diapositiva, no se distinguen del decaimiento. | Recapturar con y ∈ [−0.2, 1] y los rezagos estacionales en naranja, o hacerlo gráfico propio desde J `firma` |
| G2 | 51 (m6-1) | El mismo eje de −1 a 1 deja las barras diminutas. El rezago 16 (−0.157) roza la banda y la diapositiva no lo menciona. La banda es la de n = 144 (A4). | y ∈ [−0.3, 0.3]; mencionar el 16 |
| G3 | 53 (m7-1) | La leyenda tiene dos cuadros grises sin rótulo (los bordes de las bandas) | Recapturar filtrando la leyenda |
| G4 | 37 (escalones) | «σ_h (escala logarítmica)» se lee como «eje logarítmico», y el eje es lineal | «σ_h (en unidades de log y)» |
| G5 | 15 (satélites) | La etiqueta «satélites ≈ ρ₁·ρ₁₂ = 0.6016 × 0.7011» no da el resultado | Añadir «= 0.4218» |
| G6 | 37 | El pie de figura muestra guiones bajos literales: «ψ_j», «σ_h» | Escribir ψⱼ y σₕ en Unicode |
| G7 | 13 y 35 | La fórmula dentro de la etiqueta de definición sale mal: «SARIMA( p,d,q )( P,D,Q ) m», «EL MODELO AIRLINE , SARIMA(0,1,1)(0,1,1) ₁₂» | Escribir la etiqueta en texto plano: SARIMA(p,d,q)(P,D,Q)ₘ |
| G8 | 69 (m11-1) | El pie dice «cinco de los ocho métodos» y la tabla siguiente tiene siete filas | «cinco de los métodos de la tabla siguiente» |
| G9 | 51 | El título parte «Ljung–» / «Box» en dos líneas | Guion de no separación (U+2011) o «Ljung–Box» sin corte |
| G10 | 28 | La negrita marca cosas distintas: en AirPassengers y USAccDeaths, el 0 que engaña; en la TRM, el 0 correcto | Negrita solo para lo que contradice al correlograma |
| G11 | conjunto | Solo 7 de 77 diapositivas tienen gráfico, y la clase 2 (36 diapositivas) solo 3. **Dos fotos ya capturadas no se usan**: `m8-1.png` (ACF de ∇ log AirPassengers, ρ̂₁₂ = 0.84) y `m10-1.png` (patrón de Fourier con K = 3 frente a K = 6). | Ver la sección 5 |

## 5. Sugerencias para mejorar el material

1. **Usar las dos fotos huérfanas.**
   - `m10-1.png` va en la diap. 65 («Fourier modela la estación con 2K parámetros»), que hoy es solo fórmula.
   - `m8-1.png` va en la diap. 23 o en la diap. 57: junto a una ACF de ∇TRM, sería la comparación visual que hoy es una tabla.
2. **Gráfico de pendientes, animado: «cuarto → primero».** Va en las diap. 70–71 y muestra el puesto de cada método con una partición y con 61 orígenes. Es el giro narrativo del capítulo, y hoy son dos tablas seguidas. Las cifras ya están en J (`comparativa`).
3. **Esquema del origen móvil** (diap. 71): cinco o seis franjas de entrenamiento y prueba que avanzan. Hace entendible el «61».
4. **`ggseasonplot` o mapa mes × año en el Módulo 1.** La diap. 11 escribe el código de `ggseasonplot()` y el deck nunca muestra el resultado. Servirían también para el «Paso 0» (amplitud que crece con el nivel).
5. **Diapositiva «Quiénes compiten»** antes de la pregunta de la diap. 69 (T2, T3).
6. **Diapositivas de respaldo.** La clase 1 tiene 41 diapositivas (5 preguntas y 3 animaciones), la 2 tiene 36. A 2–3 min por diapositiva, la clase 1 va justa. Candidatas a pasar a un apéndice o marcarse como opcionales:
   - diap. 18 (tabla de φ);
   - diap. 28 (`seas` frente a `ocsb`);
   - diap. 46 (statsmodels).

## 6. Ortografía y redacción

Lo revisó un corrector independiente, que leyó la fuente entera. Encontró limpias estas categorías:

- las tildes (diacríticas e interrogativos);
- «componente», que no aparece en femenino;
- las comillas latinas, salvo en la L453;
- ACF/PACF, «rezago», AICc, «periodo», ψ, y ∇₁₂ en LaTeX.

**Errores (norma o convención del curso)**

| L | Actual | Corrección |
|---|---|---|
| 6, 7, 535, 828 | «modelo airline» en texto que se proyecta (objetivo, temas, título de sección, título del bloque R) | *airline* en cursiva |
| 1090, 1108 | «Naïve estacional», sin cursiva | *Naïve* estacional, o «ingenuo estacional» |
| 858 | «Decidido \(D=1\) y luego \(d=1\)» | «Tras decidir \(D=1\) y luego \(d=1\)» |
| 77, 880 | «ene 2015–jun 2026» | «ene. 2015–jun. 2026», o «2015-01 a 2026-06» |
| 365 | «(ρ̂₁ cae a 0.20) pero la estación…» | «…0.20), pero…» |
| 446 | «mira primero **qué prueba** usa» (*tú* en prosa expositiva) | «conviene mirar primero qué prueba usa cada una» |
| 654 | «Donde quedamos:» (*nosotros* en un título) | «Lo que dejó la clase 1:» |
| 549 | «que sea «el SARIMA más usado del mundo»» es una oración sin predicado | «Se dice que es «el SARIMA más usado del mundo»» |
| 1110 | «Corte avanzando mes a mes…: le gana…» (gerundio adjetivo, sin sujeto) | «Con un corte que avanza mes a mes desde 1954-12…, el SARIMA le gana…» |
| 613, 949 (notas) | «El error típico es…» quiere decir «el error frecuente», y se confunde con el error estándar | «El error más común es…» |
| 320 | Viñeta sin etiqueta («La forma no multiplicativa necesita 13 parámetros…») | <kbd>Definición</kbd> |
| 95 | La fuente «J3» no está en la leyenda de fuentes (L19, L41) | Añadirla |

**Inconsistencias de terminología**

1. ***airline*.**
   - Le falta la cursiva en el texto proyectado (arriba) y en los textos alternativos de las imágenes (L576, 785, 815).
   - «*Airline*» va con mayúscula en las L484 y L1088, y con minúscula en la L925.
2. **Error estándar.** Se escribe de tres formas: «error estándar» (856, 860, 911, 940), «e.e.» (422, 769, 770, 858, 865, 875) y «error típico» (804). Además, «error típico» también aparece con el sentido de «error frecuente» (613, 949).
3. **El AICc entre distintos \(D\).** Hay cinco fórmulas:
   - «no cruza distintos \(D\)» (668);
   - «tampoco cruza \(D\)» (671);
   - «**no** compara entre distintos \(D\)» (1176);
   - «el AICc sí compara» (1021);
   - «comparar AICc entre distintos D» (613).

   Unificar en «el AICc no se compara entre distintos \(D\)».
4. **La banda.** Va como ±1.96/√n (104, 127) y como ±2/√n (492, en las notas).
5. **Pascua o Semana Santa.** El regresor se llama «Pascua» (892, 923, 929) y «Semana Santa» (927).
6. **Estación o estacionalidad.** «Estación», como sinónimo, aparece unas doce veces. Hay «varias estaciones» (1159) y «varias estacionalidades» (1051) en la misma sección. Es una preferencia de estilo: decidir una forma.

**Sugerencias de estilo (las más útiles)**

- **Comas.** Falta la coma tras el condicional antepuesto («Si \(m\) es conocido, se impone», L93; «Si \(q\) alcanza a \(m\), los pesos chocan», L256). La sobra en la L585 («el salto en el rezago 12, y el segundo año»).
- **L619.** «los operadores conmutan, las pruebas no» → «los operadores conmutan; las pruebas, no» (como en la L415).
- **«A escalones» → «en escalones»** (L574, 621, 822).
- **L817.** «165 por arriba» → «por encima».
- **L787 (43 palabras).** Arranca con «<kbd>Interpretación</kbd> Una barra aislada sin interpretación» y repite «es lo que» dos veces. Propuesta: «Una barra aislada y sin explicación es esperable por azar: perseguirla con parámetros es lo que el capítulo desaconseja».
- **L404.** «sobre la desestacionalizada»: ∇₁₂ no desestacionaliza en el sentido de STL → «sobre \(\nabla_{12}y_t\)».
- **L585 (nota).** «Cuatro pulsaciones:» enumera solo tres: falta «y la conclusión».
- **Tono.**
  - «Jorobas» (106, 111) → «picos», como en el resto.
  - Hay tres variantes de «que nadie pidió» (204, 218, 285): dejar una.
  - «se pega a −1» (420) → «se acerca a −1».
  - «frenazo» (1119) → «desaceleración».
- **Viñetas de más de 30 palabras.** Están en las L1122 y L1137: partirlas.
- **L712.** «vuelve a coincidir con R (−0.4303 y −0.5527)»: los paréntesis traen el valor de statsmodels; R da −0.5528 (L563). O se cita el de R, o se dice «a la tercera cifra».

No se recoge aquí la sugerencia del corrector de cambiar «Lo que se llevan…» por «Ideas clave…»: el título es de la convención de cierre de la skill y es una decisión de estilo del docente.

## 7. Lo que hay que corregir también en el capítulo

Estas observaciones nacen en el texto del capítulo y la diapositiva solo las hereda: A1 («aunque justo»), A2 (el ejemplo de m = 365), A5 («el doble»), T12 («Paso 0…4»). Para corregirlas hay que editar `ensamblado/cap5/`, no el HTML (ver la memoria sobre el riesgo de reensamblado), y luego realinear el verificador, como en `ddfecc3`.
