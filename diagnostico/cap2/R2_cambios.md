# Capítulo 2 · ronda R2 («gráficas») · cambios

> **Léase con la sección final, «Tras la verificación»:** corrige dos regresiones de esta ronda y sustituye lo que
> aquí se dice del umbral de las tablas (1199 px), del título «t», de `aria-live` sobre la lectura y de que el eje de
> rezagos se reconoce por su título. Las cifras de `git diff --stat` vigentes son las de esa sección.

Fecha: 2026-11-16. Especificación: `diagnostico/cap2/graficas.md` (49 problemas, 11 defectos de causa común) y las
tareas T2.1–T2.5 de `PLAN_Mejora_Cap2.md`, con la decisión D4. Un solo redactor; sin commit.

- **Archivos tocados:** `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (a mano: CSS, JS compartido, JS del
  capítulo y 14 tramos dentro de los `<template>`) y, **regenerados por sus scripts**, los capítulos 3, 4, 5 y 6
  (`ensambla_cap3.py --escribir`, `ensambla_cap4.py`, `ensambla_cap5.py`, `ensambla_cap6.py`, en ese orden).
  `git diff --stat`: capítulo 2, 651 líneas; capítulos 3–6, **375 líneas cada uno, las mismas 375** (comprobado: los
  cuatro `diff` son idénticos entre sí y todas sus líneas están en el del capítulo 2).
- **No se tocó:** `plantilla/plantilla-capitulo.html`, el capítulo 1, `ensamblado/capN/` ni los scripts de ensamblado,
  `DATOS_CAP2`, ningún bloque de código R o Python, ninguna `<cite>` ni `data-afirma`. No hay clases nuevas de Tailwind
  (`compila_tailwind.py --comprobar` en verde). Siguen siendo 9 módulos, 8 `data-simulador` y 20 lienzos.
- **Capturas de después:** `diagnostico/cap2/capturas/r2/despues/` (339 PNG, fuera de git): `capN-mM-<simulador>[-estado]-<ancho>.png`
  con ancho 1200, 800 o 375; del capítulo 2, además, cada tabla (`-tablaK-`) y cada fórmula partida (`-formula-partesK-`).
  Las de antes de tocar nada, con el mismo arnés, en `capturas/r2/antes/`. Medidas crudas: `capturas/r2/medidas-antes.json`,
  `medidas-despues.json` y `medidas-ancho1024.json`.
- **Guiones** (`diagnostico/cap2/comprobaciones/`): `r2_capturas.js` (recorre los cinco capítulos, módulo a módulo, a los
  anchos que se le pidan; reutiliza el cliente CDP de `diag/chrome.js`), `r2_resumen.py` (cuenta defectos en las medidas),
  `r2_compara.py` (antes frente a después, lienzo a lienzo), `r2_contraste.py`, `r2_simulador_ar1.js`, y sus `.out`.
- **Última pasada completa** (5 capítulos × todos sus módulos × 1200, 800 y 375 px, más 1024 y 900 sin capturas):
  ninguna excepción ni `console.error/warn` (solo el 404 del `favicon.ico` del servidor de pruebas); `scrollWidth` de la
  página igual al ancho de la ventana en los 5 × 5 anchos; nada cortado por `<main>` sin barra de desplazamiento; los 126
  correlogramas × ancho con el 12 y el 24 rotulados; ningún eje vertical que cruce el 0 sin rotularlo.

## 1. Los 49 problemas, uno por fila

Estados: **A** arreglado · **P** arreglado en parte · **R1** ya lo resolvió la ronda R1 · **N** no tocado (con motivo).
Las capturas son `capturas/r2/despues/cap2-<nombre>-{1200,800,375}.png`.

| Ficha | Problema del diagnóstico | Estado | Qué se hizo, o por qué no | Capturas |
|---|---|---|---|---|
| M1 · `panel-estacionariedad` | P1 fechas de AirPassengers montadas a 375 | **A** | `marcasLegibles()`: solo eneros, rotulados con el año. 1200: los 12 años; 800 y 375: 1950 · 1953 · 1956 · 1959 (separación mínima medida, 27 px) | `m1-panel-estacionariedad-*` |
| | P2 eje `1, 18, 35…`; sin título ni unidades | **P** | Paso redondo: `20, 40 … 200` a 1200 y `50, 100, 150, 200` a 800 y 375; título «t» en las dos series simuladas. **No** se puso la unidad de AirPassengers: el capítulo 2 no dice en ningún sitio que son miles de pasajeros, y escribirlo en el eje sería una afirmación nueva (R3 o R4) | las mismas |
| | P3 tres colores aquí, uno solo en el M3; caminata en naranja 2.94:1 | **P** | El naranja de los gráficos pasa a `#FB6400` (3.03:1). Los tres colores se conservan: es una decisión de diseño del módulo, no un defecto de lectura | las mismas |
| | P4 letra con remates si Google Fonts tarda más de 3 s | **N** | Solo ocurre con la red muy lenta, y repintar no basta: Chart.js guarda las medidas del texto con la fuente vieja. El arreglo es volver a cargar el módulo cuando llega la fuente, y eso toca el arranque de los once documentos que llevan el motor (plantilla, preparciales, talleres, guía): fuera de la D4 | — |
| M2 · `ruido-blanco` | P1 el correlograma no rotula el 0 | **A** | `marcasVerticales()`: un eje de −1 a 1 rotula −1, −0.5, 0, 0.5, 1; la línea del 0, más oscura (`#64748b`, 4.76:1) | `m2-ruido-blanco-*` |
| | P2 barras de 8 px sobre la escala fija ±1 | **N** | Es la decisión que el propio diagnóstico señala: la escala fija es la que permite comparar con el M3. Se deja a sabiendas | — |
| | P3 lectura sin `aria-live` | **A** | `actualizarLectura()` (ver §2, fila 7) | — |
| | P4 eje de la serie `1, 18, 35…`, sin título | **A** | Como M1-P2 | las mismas |
| M3 · `correlogramas-comparados` | P1 a 800 y 375 solo impares: el 12 y el 24 sin número | **A** | Eje de rezagos: 1200, los 24; 800 y 375, `3, 6, 9, 12, 15, 18, 21, 24` | `m3-correlogramas-comparados-*` |
| | P2 la ondulación es tenue | **N** | La misma decisión de la escala ±1 (M2-P2). Con el 12 y el 24 rotulados ya se sabe dónde mirar | — |
| | P3 eje y sin título; la leyenda se repite tres veces | **P** | La banda sale en la leyenda como raya discontinua, que es lo que es. No se añadió título al eje y (a 375 px se come 18 px de un área de 190) ni se quitó la leyenda: es la que nombra la banda | las mismas |
| M4 · `explorador-acf-pacf` | P1 a 375 la leyenda se corta por los dos lados; fechas montadas | **A** | La leyenda usa el nombre corto del selector («∇₁₂ ∇ log(AirPassengers)»), no el largo del precálculo; fechas por años | `m4-explorador-acf-pacf-*`, `…-dd_log_airpassengers-*` |
| | P2 rezagos impares a 800 y 375 | **A** | Como M3-P1 | las mismas |
| | P3 «rezagos fuera de la banda» cuenta solo la ACF y no lo dice | **A** | Dos campos, los dos calculados por el simulador: «ACF fuera de la banda: 24 de 24» y «PACF fuera de la banda: 6 de 24» | las mismas |
| | P4 `aria-label` fijos; lectura sin `aria-live` | **A** | Los tres `aria-label` se reescriben al cambiar de serie (§6) | — |
| | P5 la intro dice «ACF que no baja» | **A** | «ACF que baja muy despacio», como el M3 | las mismas |
| | P6 en las series diferenciadas las marcas derivan de mes | **A** | Los años rotulados son múltiplos del salto: los mismos con cualquier diferenciación | `…-d_log_airpassengers-*`, `…-d_trm-*` |
| M5 · `ar1-phi` | P1 **[Alta]** el simulador desmiente la nota 2 | **A** | Cambia la nota, no el simulador (§4, punto 1) | `m5-ar1-phi-phi095-*`, `…-phi100-*` |
| | P2 «el instante en que la ACF deja de decaer» no existe | **A** | Intro: «Fíjate en cómo la ACF decae cada vez más despacio a medida que φ se acerca a 1: con φ = 1 baja casi en línea recta, y esa es la huella de la raíz unitaria» | las mismas |
| | P3 con φ > 1, exponencial a −20 000; lectura `16760012.970` | **P** | La lectura escribe `16 760 013`. El panel sigue siendo una exponencial: es lo que la serie hace, y limitar φ o cambiar de escala es contenido | `m5-ar1-phi-phi105-*` |
| | P4 a 800 los controles en dos columnas de 150 px | **A** | Una columna de 308 px (§2, fila 3) | `m5-ar1-phi-800` |
| | P5 lectura sin `aria-live`; `aria-label` fijo | **A** | §6 | — |
| | P6 leyenda «y_t», «∇y_t»; ϕ del título y φ del control | **A** | «yₜ con φ = 0.70», «∇yₜ con φ = …». La ϕ del título la pinta KaTeX y la φ del control es texto: no se igualaron | las mismas |
| | P7 «∇ de una serie caminata aleatoria (φ = 1): raíz unitaria» | **A** | Seis frases enteras en vez de cadenas pegadas: «primera diferencia de una caminata aleatoria (φ = 1)», «serie explosiva (φ > 1)»… | `m5-ar1-phi-phi100-dif-*` |
| | P8 el eje y no siempre rotula el 0 | **A** | `marcasVerticales()`. Medido en los 9 estados × 3 anchos: siempre está | las mismas |
| M6 · `montecarlo-adf` | P1 eje categórico equiespaciado | **A** | La intro lo dice: «Las amplitudes van como categorías a la misma distancia: el eje horizontal no está a escala». Un eje lineal habría amontonado 0, 0.5 y 1 | `m6-montecarlo-adf-*` |
| | P2 a 375 la leyenda se trunca | **A** | Leyenda «Falsos rechazos»; la unidad pasa al eje | las mismas |
| | P3 eje y sin título ni «%»; «5%» | **A** | Título «% de rechazos»; «Nivel nominal 5 %», con espacio duro y la cifra tomada de los datos | las mismas |
| | P4 barras naranja 2.94:1; la referencia en verde | **P** | Barras en `#FB6400` (3.03:1). La referencia sigue en verde oscuro: aquí no es una banda de confianza sino el nivel nominal, y el verde la separa de las barras | las mismas |
| | P5 «5 %» partido a 800; `aria-label` genérico | **A** | `5&nbsp;%` en la intro; el `aria-label` da los cinco porcentajes, leídos de los datos | — |
| M7 · `diferenciacion` | P1 la intro y la lista no hablan de las mismas tres señales | **R1** | La R1 reescribió la intro y la lista | — |
| | P2 a 800 los dos controles en dos columnas | **A** | Una columna | `m7-diferenciacion-800` |
| | P3 fechas: meses arbitrarios, que se corren al diferenciar | **A** | 2016 · 2019 · 2022 · 2025 a 800 y 375 con cualquier d; los 12 años a 1200 | `m7-diferenciacion-trm-d0…d3-*` |
| | P4 lectura sin `aria-live`; `aria-label` fijos | **A** | §6 | — |
| | P5 «∇^2 de la serie»; «Serie original» sin decir cuál | **A** | «TRM (COP/USD)», «∇ TRM (COP/USD)», «∇² log(AirPassengers)», «∇³ Caminata aleatoria» | las mismas |
| | P6 `338834.24` frente a `338 834` de la tabla | **A** | `cifra()`: `338 834`, `14 800`, `26 813`, `75 469`, como la tabla de al lado | las mismas |
| | P7 el eje y de una serie diferenciada no siempre rotula el 0 | **A** | `marcasVerticales()`. Medido en los 12 estados × 3 anchos | las mismas |
| M8 · `box-cox` | P1 la leyenda llama «λ elegido» al punto del deslizador | **A** | «λ del deslizador» | `m8-box-cox-*` |
| | P2 el eje x no rotula ni el 0 ni el 1; a 800 se montan | **A** | 1200: `−1.00, −0.50, 0.00 … 2.00`; 800 y 375: `−1.00, 0.00, 1.00, 2.00` | las mismas |
| | P3 lo que la nota discute no se ve | **P** | El mínimo —el λ que elige R— lleva un rombo propio, con su entrada en la leyenda; la leyenda dibuja la curva con una raya, el deslizador con un punto y el mínimo con un rombo. **No** se sombreó la franja [−0.41, −0.17] ni se trazó una recta en λ = 0: son anotaciones nuevas (R3) | `m8-box-cox-lam0-*`, `…-lam-030-*` |
| | P4 a 800 el deslizador mide 140 px | **A** | 308 px | `m8-box-cox-800` |
| | P5 lectura sin `aria-live`; `aria-label` fijos | **A** | §6 | — |
| | P6 con λ = −1 el punto medio cortado; «-1.00» con guion | **A** | `clip: false` en los dos puntos; signo menos tipográfico en la lectura, en la leyenda y en la casilla del deslizador | `m8-box-cox-lam-1-*` |
| M9 · quiz | P1 **[Alta]** pregunta 3 a 800 y 375: el rezago 12 sin número | **A** | 1200: `2, 4 … 24`; 800: `3, 6, 9, 12 … 24`; 375: `4, 8, 12, 16, 20, 24` | `m9-quiz-grafico1-*` |
| | P2 los `aria-label` dan la respuesta | **A** | Dan los datos, no el diagnóstico: las 24 autocorrelaciones y la banda (§6). El segundo ya no dice que la serie es una caminata | — |
| | P3 a 375, área de 166 × 112 px y barras de 2.5 px | **N** | Es el ancho de la tarjeta de la pregunta en el teléfono. Con el 12 rotulado la barra se localiza | `m9-quiz-grafico1-375` |
| Fórmulas y tablas | **[Alta]** tablas cortadas a 800 sin forma de verlas | **P** | A 800 px (y a 900 y 1024) las ocho tablas anchas se desplazan dentro de su caja: `recortados` pasa de 7 a 0, y la columna «Veredicto» del M6 se alcanza. **Sigue sin pista** de que hay más a la derecha, a 800 y a 375 (§5, punto 2) | `m6-tabla1-*`, `m1-tabla0-*`… |
| | **[Alta]** la definición de ruido blanco pierde su tercera condición | **A** | Fórmula en partes (`.formula-partes`): a 1200 se lee en una línea, como antes; a 800 y 375 la covarianza nula baja al segundo renglón. Nada se desplaza | `m2-formula-partes0-*` |
| | **[Media]** otras siete fórmulas que desbordan | **A** | Las siete, en partes: M3 γ_k, ρ_k (ya no se pierde «−1 ≤ ρ_k ≤ 1, ρ₀ = 1») y γ̂_k con r_k; M4 regresión de la PACF; M5 AR(1) y caminata con deriva; M6 regresión del ADF. Medido: 0 fórmulas en bloque que desborden, a los tres anchos (antes 8 a 800 y 8 a 375) | `m3-formula-partes0…2-*`, `m4-…`, `m5-…`, `m6-…` |

**Recuento sobre los 49:** 37 arreglados, 7 en parte (M1-P2, M1-P3, M3-P3, M5-P3, M6-P4, M8-P3, tablas), 1 que ya había
resuelto la R1 (M7-P1) y 4 no tocados (M1-P4, M2-P2, M3-P2, M9-P3). Los cuatro graves (M5-P1, M9-P1, tablas, ruido
blanco): tres arreglados y uno en parte.

## 2. Los 11 defectos de causa común

«Compartido» quiere decir que el arreglo está en la región que los capítulos 3–6 heredan.

| # | Defecto | Antes → después | ¿Compartido? |
|---|---|---|---|
| 1 | Eje de rezagos sin el 12 | `crearGraficoBarras` dejaba el salto automático de Chart.js → `marcasLegibles(eje, {rezagos})` en `afterBuildTicks`: si el eje es de rezagos (`opciones.rezagos`, o un `tituloX` que diga «Rezago»), rotula los múltiplos del menor divisor de 12 que quepa (1, 2, 3, 4, 6, 12, 24…). Si las etiquetas no son números a paso constante (nombres de modelos, «mes 1», amplitudes) no toca nada | **Sí** |
| 2 | Marcas de fecha | `maxTicksLimit: 12` con salto automático → en `crearGraficoLinea`, `marcasLegibles()`: fechas `AAAA-MM` → eneros, rotulados con el año, de años múltiplos del salto (no se corren al diferenciar); con menos de cuatro eneros, por meses contados desde enero; números a paso constante → paso redondo (1, 2, 2.5 o 5 por una potencia de diez). Es la idea de `ejeAnual()` del capítulo 1, generalizada: allí se supone que la serie empieza en enero y aquí se buscan los eneros, porque las series diferenciadas empiezan en febrero. **Solo actúa en el eje por defecto**: quien pasa `scales` a `crearGraficoLinea` sustituye los ejes (el `Object.assign` es superficial y se dejó así a propósito; ver §3) | **Sí** |
| 3 | Reglas por ancho de ventana | `.simulador-controles`: dos columnas con `min-width: 768px` → `repeat(auto-fill, minmax(min(100%, max(15rem, 40%)), 1fr))`, la regla del capítulo 1 y de la plantilla; `.control-slider output` con `white-space: nowrap`. Tablas: `display:block; overflow-x:auto` con `max-width: 768px` → `max-width: 1199px` (§5, punto 1) | **Sí** |
| 4 | Fórmulas que desbordan sin pista | Las ocho del capítulo 2, partidas (`.formula-partes`, regla nueva). Además, `.formula` lleva la sombra de desplazamiento del capítulo 1, y las cajas `.definition`, `.note`, `.warning` y `.exercise` —que ya se desplazaban—, la misma sombra con el color de cada caja (`--fondo-caja`) | **Sí** |
| 5 | Leyendas | En `crearGraficoBarras`: la recta de referencia se dibuja como raya discontinua y las barras como caja (`etiquetasDeLeyendaBarras`); letra de 11 px si el lienzo mide menos de 420 px. Los textos largos del capítulo 2 se acortaron (M4, M6). Siguen pasando a dos líneas las leyendas de dos entradas a 375 px, y las de los paneles con `grafico-etiqueta` siguen repitiéndola | **Sí** (la raya); el resto, capítulo 2 |
| 6 | El cero del eje y | Chart.js generaba una marca por renglón y se quedaba con una de cada dos empezando por abajo → `marcasVerticales()` hace el mismo aclarado contando desde el 0 (`autoSkip: false` en el eje para que Chart.js no vuelva a aclarar); un eje de −1 a 1 rotula −1, −0.5, 0, 0.5, 1; rejilla del 0 en `#64748b`. Antes, 12 lienzos × ancho de los cinco capítulos cruzaban el 0 sin rotularlo; ahora, ninguno | **Sí** |
| 7 | Accesibilidad de los simuladores | `actualizarLectura()` pone `aria-live="polite"` **después** del primer llenado (para que al abrir el módulo no se lea una lectura que nadie pidió); `crearControles()` separa etiqueta y valor en el nombre accesible («Coeficiente φ 0.70»). Los `aria-label` que cambian, en el JS del capítulo 2 (§6) | **Sí** (`aria-live`, nombre del deslizador); el resto, capítulo 2 |
| 8 | Texto matemático en el lienzo | «yₜ», «∇yₜ», «∇²», «∇³» | Capítulo 2 |
| 9 | Contraste del naranja | `COLORES_GRAFICO`: `secundario` `#FF6600` (2.94:1) → `#FB6400` (3.03:1) y `gris` `#94a3b8` (2.56:1) → `#8795A9` (3.04:1), los del capítulo 1; clave nueva `banda: '#e05a00'` (**3.73:1**, comprobado en `r2_contraste.out`), que es el color por defecto de las rectas de `crearGraficoBarras`. El naranja de marca de botones, cabeceras y deslizadores no cambia | **Sí** |
| 10 | Formato de cifras en las lecturas | `cifra(x, decimales)`: punto decimal, miles con espacio fino desde cinco cifras enteras y signo menos tipográfico. La usan las lecturas del capítulo 2. En los ejes, `rotuloVertical` y `rotuloLegible` ponen el signo menos; la casilla del deslizador, también | `cifra`, capítulo 2; los ejes y la casilla, **sí** |
| 11 | Fuente del módulo de arranque | **No tocado** (M1-P4) | — |

Lo que entra de nuevo en la región compartida: `marcasLegibles`, `rotuloLegible`, `marcasVerticales`, `rotuloVertical`,
`rejillaConCero`, `tituloDeEje`, `etiquetasDeLeyendaBarras`; las opciones `tituloX`/`tituloY` de `crearGraficoLinea` y
`tituloY`/`rezagos` de `crearGraficoBarras`; y las reglas `.formula-partes`, `.formula-partes--seguidas`,
`.simulador h4 > i` y `--fondo-caja`. `.simulador h4` pasa de flex a bloque (es la regla del capítulo 1: con flex, un
título con fórmula se leía desordenado en el teléfono; ver `cap3-m6-teorica-vs-muestral-375` antes y después).

## 3. Qué cambió en cada capítulo de la cadena

Los capítulos 3–6 reciben exactamente las mismas 375 líneas (CSS y JS de la región heredada) y ninguna otra.
`r2_compara.py` comparó los 240 lienzos × ancho de antes y de después: **no cambia ninguna serie ni el valor de ninguna
recta de referencia**; cambian marcas de eje y el dibujo de la leyenda, ningún texto de leyenda.

| Capítulo | Lienzos × ancho | Marcas x | Marcas y (solo el signo menos) | Correlogramas sin 12 o 24, antes → después | Eje y sin el 0 | Rótulos x pisados | Cortado por `<main>` a 800 | Lecturas con `aria-live` |
|---|---|---|---|---|---|---|---|---|
| 2 | 60 | 47 | 45 (37) | 20 → 0 | 3 → 0 | 8 → 0 | 7 → 0 | 0 → 5 |
| 3 | 87 | 59 | 69 (58) | 24 → 0 | 3 → 0 | 6 → 0 | 6 → 0 | 0 → 12 |
| 4 | 60 | 17 | 21 (14) | 14 → 0 | 6 → 0 | 7 → 7 | 8 → 0 | 0 → 11 |
| 5 | 48 | 43 | 36 (35) | 16 → 0 | 0 → 0 | 12 → 2 | 20 → 0 | 0 → 14 |
| 6 | 45 | 6 | 12 (12) | — (no tiene) | 0 → 0 | 2 → 0 | 12 → 0 | 0 → 14 |

(Columnas de defectos: suma de los tres anchos; fuente, `r2_medidas_antes.out` y `r2_medidas_despues.out`.)

- **Capítulo 3.** Los 17 correlogramas rotulan el 12 y el 24 (los de 16 rezagos, `2, 4 … 16`). Series simuladas con
  paso redondo (`50, 100, 150` en vez de `1, 17, 33…`); manchas solares por años redondos (`1775, 1800, 1825, 1850`);
  retornos de la TRM por años. Título «Teórica frente a muestral, T = 200» en su orden a 375 px.
- **Capítulo 4.** Correlogramas del Nilo y de la TRM con el 0 (`−1.0, −0.6, −0.2, 0.2…` → `−1.0, −0.5, 0, 0.5, 1.0`).
  Sus gráficos de líneas pasan `scales` propias (`escalasLinea`) y **no** reciben las marcas nuevas: los 7 rótulos
  pisados que tenía los sigue teniendo (Nilo a 375 y 800, abanico de la TRM): son de su ronda.
- **Capítulo 5.** Correlogramas hasta el rezago 36 con `4, 8, 12 … 36` a 375 px. Series mensuales por años. Queda
  `calendario-regresores` (escalas propias) con las fechas pisadas a 375 y 800.
- **Capítulo 6.** No tiene correlogramas. Cambian las fechas de `benchmarks` y `comparativa` y el signo menos de sus
  ejes. Sus tablas anchas dejan de cortarse a 800 y a 1024 px.
- **En los cuatro:** las rectas de referencia pasan a `#e05a00` salvo las que fijan su color (nivel 0.05 del
  Ljung–Box, en rojo); el naranja de las series, a `#FB6400`; las lecturas escritas con `actualizarLectura` son regiones
  vivas; los deslizadores con valor negativo muestran «−0.50»; `.formula` y las cajas enseñan la sombra cuando se
  desplazan (siete fórmulas en bloque desbordan a 800 y 375 px, dos en el capítulo 5 y cinco en el 6: antes sin pista,
  ahora con ella).
- **Reensamblar dos veces da lo mismo:** md5 de los cuatro idéntico tras una segunda pasada; `ensambla_cap3.py` sin
  argumentos: «reproducible byte a byte».
- **Verificador de bloques** (`verifica_bloques_cap6.py --html`), antes y después de reensamblar: capítulo 2, 226 de
  226; capítulo 3, 533 de 534; capítulo 4, 713 de 735; capítulo 5, 1199 de 1212; capítulo 6, 415 de 434. **Los mismos
  recuentos y las mismas discrepancias, que ya estaban.** La salida es idéntica byte a byte en los capítulos 2, 4, 5 y
  6; en el 3 difiere solo en que la pasada de antes terminó con un «Error: write failed» de R al cerrar la sesión
  (transitorio, después de imprimir todas las cifras) y la de después no (`r2_bloques_{antes,despues}_capN.out`).

## 4. Prosa que cambió para coincidir con un gráfico

Todo dentro de los `<template>`, sin cifras nuevas y sin citas.

1. **M5, nota 2 (el caso φ = 0.95).** El diagnóstico tenía razón: con el ruido del simulador, φ = 0.95 da r₁₀ = 0.2299
   y 11 de 24 barras fuera de la banda; φ = 1 da r₁₀ = 0.7693 y las 24 fuera (`r2_simulador_ar1.out`). Se cambió la
   frase, no el ruido (cambiarlo habría movido las dos cifras que la nota 3 cita, −0.252 y −0.506, que siguen saliendo):
   «…y la ACF baja mucho más despacio que con φ = 0.5. Con el ruido del simulador todavía se distingue de la de φ = 1:
   pasa el deslizador de 0.95 a 1 y compara r₁₀ en la lectura. Este es el caso difícil: cuanto más corta es la muestra y
   más se acerca φ a 1, menos se diferencian los dos correlogramas, y distinguir φ = 0.95 de φ = 1 acaba siendo casi
   imposible.» La frase general se comprobó con las funciones del propio simulador sobre 400 semillas: la mediana de
   |r₁₀(φ=1) − r₁₀(φ=0.95)| baja de 0.306 con n = 400 a 0.233, 0.190, 0.147 y 0.033 con n = 200, 100, 50 y 25; y con el
   ruido del simulador r₁₀ vale 0.230, 0.501, 0.642 y 0.769 para φ = 0.95, 0.98, 0.99 y 1. Ninguna de esas cifras está
   en la prosa.
2. **M5, intro del simulador:** «el instante en que la ACF deja de decaer» → «cómo la ACF decae cada vez más despacio…».
3. **M4, intro:** «ACF que no baja» → «ACF que baja muy despacio».
4. **M6, intro:** `5&nbsp;%` y la frase del eje que no está a escala.
5. **M8, intro:** «el punto naranja marca dónde estás y el rombo, el mínimo de la curva, que es el λ que elige R».
6. **Ocho fórmulas** en partes (mismo contenido matemático, sin tocar un símbolo) y el segundo lienzo del M8 de 200 a
   230 px de alto.

**Para la R4:** `bibliografia/contraste/cap2_inventario.tsv` cita literalmente dos frases que ya no existen
(`c2-m5-06`, «el instante en que la ACF deja de decaer», y `c2-m5-07`, «cuesta distinguirla de una raíz unitaria»). No
se tocó el inventario.

## 5. Lo que queda sin tocar o para decidir

1. **Las tablas se desplazan por un umbral de ventana, no por el ancho real.** El umbral pasó de 768 a 1199 px porque
   a 1024 px seguían cortándose tablas de los capítulos 4, 5 y 6 (hasta 159 px fuera; medido). A 1200 px todas caben,
   pero la del M1 del capítulo 5 cabe por un píxel: una tabla más ancha que se escriba mañana volverá a cortarse a 1200.
   El arreglo de fondo es envolver cada tabla en una caja desplazable (o una consulta de contenedor), que cambia el
   marcado de cinco capítulos: se propone para la R3. Efecto lateral del umbral: entre 769 y 1199 px una tabla estrecha
   ya no se estira al 100 % del área (es como ya se veía en el teléfono).
2. **Ninguna tabla avisa de que sigue a la derecha** (ni a 800 ni a 375). La sombra de `.formula` no sirve aquí: las
   celdas tienen fondo y la tapan. Necesita la misma caja envolvente del punto 1.
3. **Los ayudantes de la plantilla quedan distintos de los del capítulo 2** (no se tocó, como se pidió):
   `plantilla/plantilla-capitulo.html` conserva `COLORES_GRAFICO` con `#FF6600` y `#94a3b8`, el `crearGraficoLinea` y el
   `crearGraficoBarras` de antes (sin marcas legibles, sin el 0, sin la raya de la banda), `actualizarLectura` sin
   `aria-live` y la regla de las tablas en 768 px. Sí coincide ya en `.simulador-controles`, `.simulador h4` y la sombra
   de `.formula`, que le llegaron con la R2 del capítulo 1. Los preparciales, los talleres y la guía del proyecto llevan
   su propia copia del motor y tampoco cambian.
4. **`crearGraficoLinea` sigue mezclando opciones con `Object.assign` superficial.** Los capítulos 4, 5 y 6 cuentan
   con ello (pasan `scales` enteras); cambiarlo a mezcla recursiva, como en el capítulo 1, les habría cambiado los ejes.
   Por eso sus gráficos con escalas propias no reciben las marcas nuevas (9 rótulos pisados y 6 leyendas más anchas que
   el lienzo, todos en los capítulos 4, 5 y 6 y todos de antes: `r2_medidas_despues.out`).
5. **El color de las series naranjas cambió en toda la cadena** (`#FF6600` → `#FB6400`). Es casi imperceptible y es el
   del capítulo 1, pero no estaba pedido expresamente: se hizo porque la caminata del M1 y las barras del M6 tenían el
   mismo 2.94:1 que la banda. Si se prefiere no tocarlo, es una línea de `COLORES_GRAFICO`.
6. **M8:** la franja del 20 % y la recta en λ = 0 (R3). **M1:** la unidad de AirPassengers (R3/R4). **M2 y M3:** la
   escala fija ±1 (decisión). **M1-P4:** fuentes lentas.
7. **Tooltips, teclado, modo oscuro e impresión** siguen sin mirarse, como en el diagnóstico.

## 6. Accesibilidad (T2.4)

- **`aria-live="polite"`** en las 5 lecturas del capítulo (y, por el ayudante, en las 51 de los capítulos 3–6 que se
  escriben con `actualizarLectura`). Medido: 168 lecturas × ancho sin el atributo antes, 0 después.
- **`aria-label` que cambia con los controles**, 9 lienzos: los tres del explorador («ACF de ∇ TRM, rezagos 1 a 24: 1
  de 24 barras fuera de la banda ±0.167; la del rezago 1 vale 0.088»), los dos del AR(1), los dos de la diferenciación y
  los dos de Box–Cox. Todas las cifras las calcula el simulador en el momento.
- **M6:** el `aria-label` da los cinco porcentajes y el nivel nominal, leídos de `DATOS_CAP2`.
- **Quiz:** los dos `aria-label` dan las 24 autocorrelaciones con dos decimales y la banda —lo que ve quien mira el
  gráfico—, no el diagnóstico. El de la pregunta 6 dice «la serie de la pregunta», no «una caminata aleatoria».
- Los 9 `aria-label` estáticos de M1, M2 y M3 no se tocaron: el diagnóstico comprobó que lo que afirman es cierto.
- **Unicode en el lienzo:** yₜ, ∇yₜ, ∇², ∇³, ∇₁₂; signo menos en ejes, leyendas, lecturas y deslizadores.

## 7. Lo que se encontró de nuevo

1. **A 1024 px se cortaban tablas en los capítulos 4, 5 y 6** (el diagnóstico solo miró 1200, 800 y 375): 10 elementos
   fuera de `<main>`, hasta 159 px. Resuelto con el umbral de 1199 px; `r2_medidas_1024_900.out` da 0.
2. **El aclarado vertical de Chart.js era la causa del 0 que faltaba**, no el paso elegido: genera una marca por
   renglón y descarta una de cada dos desde abajo. Fijar `stepSize`, como proponía el diagnóstico, no lo habría evitado.
3. **`verifica_bloques_cap6.py --html` sobre el capítulo 3 deja `precalculo/serie.csv`** sin seguir en git (lo escribe
   un bloque de R del capítulo). Se borró al terminar; conviene que el verificador lo limpie o que esté en `.gitignore`.
4. **Los títulos de simulador con fórmula se leían desordenados a 375 px en el capítulo 3** («Teórica frente a
   muestral,» y «T = 200» en dos columnas). Resuelto con la regla de bloque del capítulo 1.
5. **Siete fórmulas en bloque desbordan en los capítulos 5 y 6** a 800 y 375 px (dos y cinco; casi todas dentro de
   `.definition`). Ahora llevan la sombra; partirlas, como las del 2, es de la ronda de cada capítulo.

## 8. Comprobaciones finales (desde la raíz del worktree)

| Comprobación | Resultado |
|---|---|
| `python3 precalculo/verifica_todo.py` | 11 verificadores en verde (incluye capítulo 3 reproducible y Tailwind al día) |
| `MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html` sobre el capítulo 2 | 226 de 226, 0 bloques con discrepancias |
| Lo mismo sobre los capítulos 3, 4, 5 y 6, antes y después | 533/534 · 713/735 · 1199/1212 · 415/434, igual antes que después |
| `python3 precalculo/audita_posicion_correcta.py` | en verde |
| `node diagnostico/cap2/comprobaciones/r1_simulador_ar1.js` | misma salida que en la R1 (−0.5063 y −0.2522) |
| `node …/r2_capturas.js despues` + `r2_resumen.py despues` | 300 lienzos × ancho: 0 correlogramas sin 12 o 24, 0 ejes sin el 0, 0 desbordes de página, 0 cortes de `<main>`, 0 eventos de consola |
| `python3 …/r2_compara.py` | capítulos 3–6: «lo que no debía cambiar: sin cambios»; capítulo 2: solo el tercer conjunto de datos del M8 (el rombo), que es intencionado |

## Tras la verificación (2026-11-16)

Informe del verificador: `diagnostico/cap2/R2_verificacion.md` (0 bloquean, 2 a corregir, 8 menores). Mismo
procedimiento de cadena: se editó el capítulo 2 y se reensamblaron el 3, el 4, el 5 y el 6. `git diff --stat` final:
capítulo 2, 749 líneas; capítulos 3–6, **482 cada uno, las mismas** (el `diff` del 5 las ordena distinto en un tramo;
el conjunto de líneas es idéntico). Reensamblar dos veces da los mismos md5; `ensambla_cap3.py`: «reproducible byte a
byte». Guiones nuevos, `comprobaciones/r2b_*`. Para comparar con `HEAD` se usó el recorrido del propio verificador
(`v2_recorrido.js` sobre el árbol corregido → `v2_recorrido_r2b.json`, contra su `v2_recorrido_head.json`, con sus
`v2_compara.py` y `v2_doce_perdido.py` → `r2b_compara.out`, `r2b_doce_perdido.out`; capturas en `capturas/r2v/r2b/`) y,
para las tablas, `HEAD` extraído con `git archive` y servido en un puerto propio (8817, ya detenido).

### Los dos que había que corregir

| # | Qué pasaba | Qué quedó | Evidencia |
|---|---|---|---|
| 1 | Los ejes de rezagos que no se titulan «Rezago» (j de los pesos ψ en cap. 5 M5, cap. 3 M9 y cap. 4 M9) perdían el 12 y el 24 a 800 y 375 px: `marcasLegibles()` decidía por el título | **La regla ya no mira el título.** Un eje cuenta rezagos, retardos u horizontes si sus etiquetas son enteros seguidos que empiezan por debajo de 12 (k, j, h): en un gráfico de barras, siempre; en uno de líneas, hasta 60 valores (más son los instantes de una serie, que siguen con paso redondo; los años no entran porque empiezan en 1770 o 1871). Esos ejes rotulan los múltiplos de un divisor de 12, y el primer valor si hay sitio. `opciones.rezagos` (true/false) lo fuerza. Cap. 5 M5, eje j: `0, 4, 8, 12 … 32` a 800 y 375 (HEAD: `0, 3, 6 … 33`); el eje σₕ de debajo, que en HEAD no rotulaba ni el 12 ni el 24 a ningún ancho, ahora `1, 6, 12, 18, 24, 30, 36`. Cap. 3 M9 j: `0, 3, 6 … 24`; cap. 4 M9 j: `0, 3 … 27` y `0, 4 … 28`; cap. 3 M8, eje h del Ljung–Box (empieza en 2): `3, 6 … 18` | `r2b_doce_perdido.out` **vacío** (antes 13 líneas); `r2b_compara.out`: rezago 12 rotulado en 168 de 168, 24 en 80 de 80, 36 en 24 de 24, a 1200, 1024, 800 y 375; `capturas/r2v/r2b/c5-m5-sim0-airline-pesos-{800,375}.png` |
| 2 | Con el umbral de 1199 px, entre 769 y 1199 px las tablas estrechas dejaban de llenar el área (22 tablas × ancho, hasta 306 px vacíos) | **Sin umbral.** La regla de `HEAD` (`max-width: 768px`) vuelve a estar como estaba, y `ajustarTablas()` marca con `table.tabla-ancha` (bloque con desplazamiento) **solo la tabla que no cabe en su contenedor**, a cualquier ancho; la que cabe sigue siendo una tabla al 100 %. Se repasa al cargar el módulo y, con un `ResizeObserver` sobre el área de contenido, al redimensionar, plegar la barra lateral, abrir un desplegable o cuando KaTeX termina. Las `.tabla-ranking` (marco propio) se saltan. No se envuelve ninguna tabla: el marcado no cambia. `table.tabla-ancha` gana a `lg:table` de las dos tablas del cap. 4 que lo llevan | `r2b_tablas_compara.out`, 440 tablas × ancho a 1200, 1024, 900, 800 y 375: **cortadas por `<main>`, 90 → 0; más estrechas que en HEAD, 0; que no llenan su contenedor, 3 → 3** (las tres, a 375 px y ya en HEAD). `r2b_compara.out` § «tabla que no llena su caja»: 8, todas «ya estaba» (antes 30, 22 nuevas) |

Al hacerlo apareció un error que el arnés habría parado igual: la constante nueva `MESES_CORTOS` chocaba con una del
capítulo 5 y su `<script>` no cargaba. Renombrada (`MESES_DEL_EJE`) y, para que no vuelva a pasar,
`r2b_sintaxis.py` pasa `node --check` al `<script>` de los cinco capítulos y busca declaraciones de primer nivel
repetidas: cinco «OK» (`r2b_sintaxis.out`).

### Los menores, uno por uno

| # del informe | Qué | Estado | Qué se hizo, o por qué no |
|---|---|---|---|
| 3 | Ninguna tabla avisa de que sigue a la derecha | **Para la R3** | Las celdas tienen fondo y tapan cualquier sombra puesta en la tabla; hace falta envolverla, que es cambiar el marcado de cinco capítulos. Ahora es más fácil: la tabla que desborda ya lleva la clase `tabla-ancha` |
| 4 | Ejes j y h de cap. 3 M9 y cap. 4 M9 | **Corregido** con el punto 1. El 1 del eje h sale cuando cabe (cap. 5 M5 a 800: `1, 6, 12…`); en cap. 3 M9 a 375 no cabe y empieza en 3 |
| 5 | Leyenda de cap. 4 M6 a 375 px en dos líneas | **Corregido** | El capítulo 4 reduce `boxWidth` a 12 px en el teléfono y la muestra nueva tenía un ancho fijo de 18. Ahora la muestra mide lo que diga `boxWidth` (complemento `anchoDeLaMuestra`). Leyenda de 26 px y área de 153.8 px, como en HEAD. En `r2b_compara.out`, «leyenda más alta» solo lista el M8 del cap. 2 (la tercera entrada, intencionada; 54 px a 800 y 375, con los rótulos acortados a «Deslizador» y «Mínimo (el que elige R)») |
| 6 | El título «t» quitaba un 16–18 % de alto | **Corregido: se quitó** | Área del M1 de 114.8 px y de M2 y M5 de 134.8 px, como en HEAD; el eje y del ruido blanco vuelve a `−3 … 3`. M1-P2 del diagnóstico queda entonces en parte: paso redondo sí, título no. Las opciones `tituloX`/`tituloY` de `crearGraficoLinea` siguen existiendo, sin uso en el capítulo 2 |
| 7 | Series de dos años con solo dos rótulos | **Corregido** | Una serie con menos de cuatro eneros va por meses contados desde enero, con el año en enero y el mes abreviado en los demás: `1959 · jul · 1960 · jul` a 800 y 375, `1959 · mar · may … nov · 1960 …` a 1200 (cap. 5 M10 y M11, cap. 6 M2) |
| 8 | «0» junto a «−1.0» | **Corregido** | `rotuloVertical` escribe el 0 con los decimales de sus vecinos: `−1.0, −0.5, 0.0, 0.5, 1.0`. En los cinco capítulos |
| 9 | `aria-live` en ráfaga | **Corregido** | La lectura visible ya no es una región viva. Hay una sola región, fuera de la vista (`#anuncio-lectura`, `aria-live="polite"`, `aria-atomic`), y `actualizarLectura()` escribe en ella el texto de la lectura **0.7 s después del último cambio**. El primer llenado no se anuncia. `r2b_anuncio.out`, en cap. 2 M5, cap. 3 M5 y cap. 5 M2: región vacía al cargar; con 12 pasos seguidos del deslizador, 12 cambios visibles, 0 anuncios durante la ráfaga y 1 después, con el mismo texto que la lectura; la página no desborda. Sigue sin probarse con un lector real. (La columna `lecturas_sin_live` de `r2_resumen.py` mide el atributo sobre la lectura y ya no aplica) |
| 10 | Gráficos con `scales` propias | **No tocado** | Ya estaba y es de la ronda de cada capítulo (§5, punto 4) |

### Comprobaciones tras las correcciones

| Comprobación | Resultado |
|---|---|
| `python3 precalculo/verifica_todo.py` | 11 verificadores en verde |
| `verifica_bloques_cap6.py --html` sobre los capítulos 2 a 6 (`r2b_bloques_capN.out`) | 226/226 · 533/534 · 713/735 · 1199/1212 · 415/434, como en HEAD. `precalculo/serie.csv` borrado |
| `audita_posicion_correcta.py` · `r1_simulador_ar1.js` | en verde · misma salida que en la R1 |
| `v2_recorrido.js` sobre el árbol + `v2_compara.py` (`r2b_compara.out`) | consola: solo el 404 del favicon; «eje y con muchos menos rótulos» y «área de dibujo más baja», vacíos (antes 3 y 17); «rezagos sin rotular», vacío; los 14 solapes y las 5 leyendas que se salen, todos «ya estaba» |
| `r2_capturas.js despues` (5 capítulos a 1200, 800 y 375; 339 capturas nuevas en `capturas/r2/despues/`) | 0 eventos de consola, 0 desbordes de página, 0 recortes, 0 correlogramas sin 12 o 24, 0 ejes sin el 0; `r2_compara.py`: capítulos 3–6 «sin cambios» en series y rectas |
| `r2b_sintaxis.py` | los cinco `<script>` pasan `node --check`, sin declaraciones repetidas |
