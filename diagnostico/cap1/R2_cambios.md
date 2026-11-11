# Capítulo 1 · ronda R2 («gráficas») · cambios

Fecha: 2026-11-11. Especificación: `diagnostico/cap1/graficas.md`. Un solo redactor; sin commit.

- Archivos tocados: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (CSS, `<script>` de los gráficos y
  marcado de los simuladores), `plantilla/plantilla-capitulo.html` (solo CSS: las reglas de la plantilla que cambian,
  idénticas) y, regenerado por `precalculo/ensambla_proyecto.py`, `Htmls_Series/proyecto-pronostico-corte-iii.html`
  (58 líneas más y 13 menos, todas dentro de su `<style>`).
- No se tocó `DATOS_CAP1`, ni un `<cite>`, ni un `data-afirma`, ni un marcador `<!--…-->`; no hay clases nuevas de
  Tailwind; siguen siendo 9 módulos y los mismos `data-simulador`.
- Capturas de después: `diagnostico/cap1/capturas/r2/` (ignorada por git), mismo esquema de nombres del diagnóstico con
  tres sufijos: `-escritorio` (1200 px), `-800` y `-movil` (375 px). Medidas: `capturas/r2/medidas-r2.json`.
- Arnés: `diagnostico/cap1/herramientas/r2_capturas.js` (todo), `r2_elemento.js` (un elemento suelto) y
  `r2_resumen.py` (resumen de las medidas). Comprobaciones en R: `comprobaciones/r2_graficas.R` y `.out`.
- Última pasada completa (9 módulos × 3 anchos): sin excepciones ni `console.error`, ningún elemento fuera de la página
  salvo fórmulas, código y tablas (que se desplazan dentro de su caja), ninguna etiqueta de eje x pisada, ningún lienzo
  fuera de su caja, todos los lienzos con título en el eje y.

## 1. Los 22 gráficos, uno por fila

«P1…» son los problemas de cada ficha, en su orden. Estados: **A** arreglado · **P** arreglado en parte · **R1** ya lo
resolvió la ronda R1 · **N** no tocado (con motivo). Las capturas son `capturas/r2/<nombre>-{escritorio,800,movil}.png`.

| # | Gráfico | Problemas de la ficha | Estado | Qué se cambió | Capturas después |
|---|---|---|---|---|---|
| 1 | M1 · `serie-airpassengers` | P1 fechas montadas a 375 · P2 sin títulos de eje, leyenda de una serie, unidad desigual · P3 `aria-label` solo nombra | P1 **A** · P2 **A** (la unidad de la prosa la unificó R1) · P3 **A** | Eje x con `ejeAnual()` (solo eneros, «1949»); eje y «Miles de pasajeros»; leyenda fuera; `aria-label` que dice tendencia, pico anual y abanico | `m1-serie-airpassengers-*` |
| 2 | M3 · mapa estacional | P1 se corta en julio a 375 y 800 · P2 unidad «pasajeros» · P3 la prosa no lo presenta · P4 letra pequeña | P1 **A** · P2 **R1** («mil pasajeros») · P3 **N** (es estructura: R3) · P4 **A** | Variante `.mapa-estacional--entero`: columnas `minmax(0,1fr)` sin ancho mínimo, letra que sigue al ancho del mapa (`cqw`, 0.52–0.72 rem); `scrollWidth` = `clientWidth` en los tres anchos; leyenda y nota más grandes y en `#475569` | `m3-mapa-estacional-*` |
| 3 | M3 · `grafico-estacional` | P1 no se sabe qué línea es qué año · P2 sin título de eje y · P3 título desordenado a 375 · P4 `aria-label` describe la construcción | los cuatro **A** | Rampa de un tono, de `#5F9F90` (1949) a `#012820` (1960); el primer año, el último y los intermedios que caben, rotulados al final de su línea; ejes «Mes» y «Miles de pasajeros»; iniciales de mes en lienzos estrechos; la intro explica el color; `aria-label` con lo que se ve | `m3-grafico-estacional-*` |
| 4 | M4 · `comparador-escala`, panel aditivo | P1 a 800 el segundo panel fuera de la página · P2 a 375 los paneles fuera de la caja · P3 «Año 1Año 2…» · P4 extremos del eje «63.9 … 364.08» · P5 la lectura parece contradecir al texto · P6 leyenda repetida · P7 `aria-label` fijo | los siete **A** | `.grafico-par` por ancho de contenedor; eje x «1…8» con título «Año»; límites redondos compartidos (`ejeRedondo`, 2 % de aire); una sola leyenda en HTML sobre el par; la lectura añade por qué 23.6 ≠ 20.0 (ver §4); `aria-label` que sigue a los controles; lectura con `aria-live` | `m4-comparador-escala-*`, `…-beta4-A40-*`, `…-beta0-*`, `m4-vista-800`, `m4-vista-movil` |
| 5 | M4 · `comparador-escala`, panel multiplicativo | los mismos | los siete **A** | lo mismo; con β = 0 su `aria-label` ya no dice que la banda se ensancha | las mismas |
| 6 | M4 · `amplitud-nivel` | P1 el año solo sale con el cursor · P2 eje y sin unidad · P3 última marca irregular (450 → 520) · P4 referencia aditiva en gris 2.56:1 · P5 leyenda de 3 líneas dentro del lienzo | los cinco **A** | 1949 y 1960 rotulados sobre el punto; «Amplitud: máx − mín (miles)»; eje x 100–500 de 100 en 100 (las dos rectas de referencia terminan en 500); gris `#8795A9`; leyenda en HTML; título del eje x en dos líneas si el lienzo es estrecho | `m4-amplitud-nivel-*` |
| 7 | M4 · `serie-vs-log`, escala original | P1 desborde a 800 y 375 · P2 fechas montadas en escritorio · P3 eje y con 3-4 rótulos no redondos · P4 la misma serie cambia de color; leyenda redundante | los cuatro **A** | `.grafico-par`; `ejeAnual()`; eje 100–700 con todas sus marcas; verde oscuro; título de eje en vez de leyenda | `m4-serie-vs-log-*` |
| 8 | M4 · `serie-vs-log`, escala logarítmica | los mismos | los cuatro **A** | lo mismo; eje 4.5–6.5; mismo verde oscuro que el panel original | las mismas |
| 9 | M4 · `construye-tu-serie` | P1 estado inicial poco elocuente y «Estacionalidad» oculta · P2 marcas cada 10 meses · P3 el eje y se reescala · P4 sin lectura · P5 fechas inventadas sin aviso | P1 **P** · P2 **A** · P3 **N** · P4 **N** · P5 **A** | La estacionalidad arranca visible (la intro dice «ocultar»); eje x anual; título «Valor simulado»; la intro avisa de que las fechas son ficticias; `aria-label` con el estado de los tres controles. **No** se cambiaron A = 10 y σ = 5 iniciales (es el estado del simulador, no su presentación); fijar el eje y aplastaría el estado inicial (el rango posible va de −200 a 330); una lectura numérica sería contenido nuevo: las tres cosas quedan para R3 | `m4-construye-tu-serie-*`, `…-beta2-A30-sigma0-*`, `…-beta-neg-sigma20-*` |
| 10 | M5 · `media-movil` | P1 sin lectura numérica · P2 fechas montadas y título desordenado a 375 · P3 la leyenda cambia al primer movimiento · P4 observada gris de 1 px · P5 `aria-label` fijo | los cinco **A** | Lectura nueva (`aria-live`): «Con m = 12 (media centrada 2×12) la curva tiene 132 de los 144 valores: faltan 6 al principio y 6 al final», contada sobre la curva dibujada (ver §5, punto 1); `ejeAnual()`; leyenda «Media móvil (m=12)» desde el inicio; observada en verde oscuro; `aria-label` con m y los meses que faltan | `m5-media-movil-*`, `…-m5-*`, `…-m24-*` |
| 11 | M6 · componente `ciclo` | P1 no se dibuja como ciclo (el paso 4 cae a otra fila) · P2 «no hay prueba automática» · P3 `stats::filter(y, rep(1/m, m))` · P4 `tabpanel` sin nombre · P5 justificado con huecos a 375 | P1 **A** · P2 **R1** · P3 **R1** · P4 **A** · P5 **A** | Rejilla de columnas iguales por ancho de contenedor (4 en una fila a 1200, 2×2 a 800, 1 a 375) y «↺» tras la última etapa; `aria-labelledby` en los cuatro paneles; texto a la izquierda a ≤ 640 px | `m6-ciclo-*`, `m6-ciclo-paso4-*`, `m6-ciclo-movil-arriba` |
| 12 | M6 · `descomp-clasica`, observada | P1 área de 35 px · P2 ejes sin rótulos y no redondos · P3 paneles sin eje de tiempo común · P4 cuatro leyendas y cuatro ejes x · P5 a 375 fechas montadas y título roto · P6 residuo en gris 2.56:1 · P7 `aria-label` nombra · P8 observada y tendencia con escalas distintas | P1–P8 **A** (P2 con una salvedad: ver fila 14) | Pila `.grafico-pila`: área de 130 px por panel (116 en el teléfono); eje 100–700 de 100 en 100; eje y de 62 px fijos (las cuatro áreas empiezan y acaban en el mismo píxel: medido); sin leyenda, con título «Observada (miles)»; eje x solo en el último panel | `m6-descomp-clasica-*`, `m6-vista-800`, `m6-vista-movil` |
| 13 | M6 · `descomp-clasica`, tendencia | los mismos | **A** | Misma escala que la observada (100–700); «Tendencia (miles)»; `aria-label` con los huecos de los extremos | las mismas |
| 14 | M6 · `descomp-clasica`, estacional | los mismos | **A**; de P2 queda una parte **N** | Eje 0.8–1.3; línea de la rejilla resaltada en 1; «Estacional (factor)». El 0.8012 de noviembre se lee con el cursor, pero sigue sin marca propia en el eje: señalarlo exige una anotación, que es contenido (R3) | las mismas |
| 15 | M6 · `descomp-clasica`, residuo | los mismos | **A** | Eje 0.85–1.10; referencia en 1; gris `#8795A9` (3.04:1); único panel con eje de tiempo | las mismas |
| 16 | M7 · `loess-local` | P1 las cuatro curvas montadas en 1-2 px · P2 «el punto verde» tapado · P3 a 375 leyenda de 118 px, «1954-12» partido, fechas montadas · P4 dos grises casi iguales · P5 el naranja y la media móvil cambian de color respecto del capítulo · P6 grado y pesos como deslizadores 0-1 | P1 **A** · P2 **A** · P3 **A** · P4 **A** · P5 **N** (excepción declarada, §3) · P6 **N** (cambiar el tipo de control no es presentación: R3) | Dos lienzos en el mismo simulador: arriba la serie entera con la franja de la ventana, abajo la ventana ampliada (ventana + 12 meses a cada lado; + 5 en lienzos estrechos) con el eje y ceñido a lo visible; `order` para que el rombo quede encima, con borde blanco y `clip` para que no se corte en los extremos; discos con el tamaño máximo ajustado a lo que mide un mes; leyenda en HTML con las siete series; la desestacionalizada pasa a morado; insignia del control sin partir; la intro nombra los colores que se ven; lectura con `aria-live`; `aria-label` de los dos lienzos con el foco y la ventana. Los cálculos (`ajusteLocal`, `calcular`, `curvaLoess`) y las cifras de la lectura no se tocaron | `m7-loess-local-*`, `…-foco1-*`, `…-foco144-*`, `…-grado0-planos-*`, `…-span61-*`, `m7-vista-*` |
| 17 | M7 · `descomp-stl`, log observada | P1 los defectos del M6 · P2 «el residuo no tiene estructura visible» · P3 `aria-label` nombra | P1 **A** · P2 **A** (prosa corregida, §4) · P3 **A** | Como el M6: pila, eje 4.5–6.5, «log(Observada)» | `m7-descomp-stl-*` |
| 18 | M7 · `descomp-stl`, tendencia | los mismos | **A** | Misma escala que la observada (4.5–6.5); `aria-label`: llega de enero de 1949 a diciembre de 1960 | las mismas |
| 19 | M7 · `descomp-stl`, estacional | los mismos | **A** | Eje −0.3–0.3 con el signo menos tipográfico; referencia en 0 | las mismas |
| 20 | M7 · `descomp-stl`, residuo | los mismos | **A** | Eje −0.15–0.10; referencia en 0; gris `#8795A9`; `aria-label` con la dispersión mayor en los extremos | las mismas |
| 21 | M8 · `desestacionalizada` | P1 el gráfico no dice con qué Ŝ · P2 fechas montadas a 375 · P3 `aria-label` nombra | P1 **R1** (la intro ya lo dice) · P2 **A** · P3 **A** | `ejeAnual()`; «Miles de pasajeros»; observada en verde oscuro fino y desestacionalizada en morado | `m8-desestacionalizada-*` |
| 22 | M9 · gráfico del quiz | P1 el enunciado identifica la curva por el color; naranja 2.94:1 | **P** | Naranja `#FB6400` (3.03:1); observada en verde oscuro; eje anual y título de eje. El enunciado sigue diciendo «la línea naranja» (la leyenda la nombra): la pregunta se rehace en R5 | `m9-quiz-grafico-*` |

**Fórmulas y tablas** (sección aparte de la especificación):

| Elemento | Estado | Qué se cambió | Capturas |
|---|---|---|---|
| M8 · $F_T$ y $F_S$ | **A** | Dos fórmulas en una caja `.formula-par`: lado a lado si caben (1200), una debajo de otra si no (800 y 375); a ≤ 640 px, KaTeX a 1em. Ya no hay desplazamiento | `m8-formula-FT-FS-*` |
| M4 `\underbrace`, M5 2×12, M7 tricúbica y bicuadrada | **P** | Siguen desplazándose dentro de su caja, pero ahora `.formula` enseña una sombra en el borde hacia el que queda fórmula (pista de desplazamiento, solo CSS) | `m7-formula-tricubica-movil`, `m7-formula-tricubica-desplazada-movil` |
| M9 · fórmula en línea del quiz que sobresale 20 px a 800 | **N** | Es texto de una pregunta que R5 va a rehacer | — |
| Tablas a 375 px (M2, M4, M6) | **N** | Son tablas, no gráficos; el arreglo (pista de desplazamiento o reorganizar columnas) toca la regla `table` de la plantilla y a los seis capítulos: se propone para R3 | `m6-tabla-pasos-movil` (estado actual) |

**Recuento sobre los 63 problemas de las 14 fichas:** 52 arreglados, 2 arreglados en parte (estado inicial de
`construye-tu-serie`; quiz), 4 que ya había resuelto R1, 5 no tocados (mapa P3; `construye` P3 y P4; `loess` P5 y P6).

## 2. Arreglos de una vez

| # | Regla | Antes → después | ¿A la plantilla? |
|---|---|---|---|
| 1 | `.grafico-par` (CSS) | `grid-template-columns: 1fr` + dos columnas por `@media (min-width: 768px)` → `repeat(auto-fit, minmax(min(100%, 18rem), 1fr))` y `> * { min-width: 0 }`. Dos columnas solo si cada una llega a 18rem **en el contenedor**. Medido: 1200 → `338px 338px`; 800 → `308px` (antes 668 px en 308); 375 → `259px` (antes 323 en 259) | No: la regla nació en el capítulo 1 y la plantilla no la tiene |
| 2 | Marcas de fecha · `ejeAnual()` (JS) | `maxTicksLimit: 12` con salto automático («1949-011951-06…») → marcas fijadas en `afterBuildTicks`: solo eneros, rotulados «1949», y tantos como quepan (40 px por rótulo). 1200: los 12 años; 800 y 375: 1949 · 1952 · 1955 · 1958. La usan M1, M4 (×3 simuladores), M5, M6, M7, M8 y el quiz; el comparador, con «1…8» | No (JS) |
| 3 | `panelComponente()` + `.grafico-pila` | Lienzo de 120 px con leyenda, área de 35 px, `maxTicksLimit: 4` y min/max crudos, un eje x por panel, eje y de ancho variable (13 px de desfase) → panel de 150 px (136 en teléfono) sin leyenda, área de 130 px (116), eje entre cifras redondas con todas sus marcas (`ejeRedondo`), eje x solo en el último panel, eje y de 62 px fijos (`afterFit`), título de eje con la unidad, línea de referencia (1 o 0) resaltada, y misma escala para la serie y su tendencia. Medido: las cuatro áreas van del mismo píxel al mismo píxel en los tres anchos | No (JS y regla nueva) |
| 4 | `.simulador h4` (CSS) | `display: flex; align-items: center; gap: .5rem` → `display: block` y `.simulador h4 > i { margin-right: .5rem }`. El título se lee en su orden («Simulador: media móvil sobre AirPassengers») | **Sí** |
| 5 | Contraste · `COLORES_GRAFICO` (JS) | gris `#94a3b8` → `#8795A9`; naranja `#FF6600` → `#FB6400`; se añade `violeta: '#7c3aed'` (ver §3). El naranja de marca de botones, cabeceras, texto y deslizadores no cambia | No (JS) |
| 6 | Títulos de eje y unidades (JS) | Solo `amplitud-nivel` los tenía → los 21 lienzos llevan título en el eje y, con «miles de pasajeros» donde es AirPassengers (D6); punto decimal (ya estaba) y signo menos tipográfico en los ejes | No (JS) |
| 7 | `.simulador-controles` (CSS) | `1fr` + `1fr 1fr` por `@media (min-width: 768px)` → `repeat(auto-fill, minmax(min(100%, max(15rem, 40%)), 1fr))`: dos columnas como mucho y solo si el simulador las aguanta. A 800 px cada etiqueta ocupaba cuatro líneas | **Sí** |
| 8 | `.control-slider output` (CSS) | + `white-space: nowrap; flex-shrink: 0` («1954-12» se partía en dos líneas) | **Sí** |
| 9 | `.formula` (CSS) | + cuatro capas de fondo (`background-attachment: local, local, scroll, scroll`): sombra en el borde hacia el que queda fórmula sin ver | **Sí** |
| 10 | `.ciclo-etapas`, `.ciclo-etapa`, `::after`, y su `@media (max-width: 640px)` (CSS) | `flex-wrap` → rejilla `repeat(auto-fit, minmax(min(100%, 9.5rem), 1fr))`; «↺» tras la última etapa; en el teléfono, una columna y texto de los paneles a la izquierda | **Sí** (la guía del proyecto no tiene ningún `.ciclo`: sin efecto visible allí) |
| 11 | Leyendas (JS + CSS nuevo) | Cajas de color dentro del lienzo → muestra de línea con el trazo de cada serie (`etiquetasDeLeyenda`); fuera en los gráficos de una sola serie; en HTML (`crearLeyenda`, `.grafico-leyenda`) en comparador, amplitud-nivel y ajuste local, donde se comía el lienzo | No (nuevo) |
| 12 | `crearGraficoLinea()` (JS) | `Object.assign` superficial (cada llamada repetía fuentes y rejilla) → mezcla recursiva (`fusionarOpciones`) y un quinto argumento para complementos locales | No (JS) |

Reglas **nuevas** del capítulo que no están en la plantilla (para llevarlas cuando toque a los capítulos 2–6):
`.grafico-leyenda*`, `.grafico-pila*`, `.formula-par`, `.mapa-estacional--entero`, y `.grafico-par`.

**Plantilla y guía del proyecto.** En `plantilla/plantilla-capitulo.html` cambian solo las seis reglas marcadas «Sí»,
copiadas literalmente del capítulo. `python3 precalculo/ensambla_proyecto.py` reescribió
`Htmls_Series/proyecto-pronostico-corte-iii.html` (231 KB): `git diff` son 8 tramos, todos entre las líneas 584 y 2181,
dentro de su `<style>` (que cierra en la 2790). `python3 proyecto/audita_proyecto.py` → «Todo limpio». La guía no tiene
`.simulador` ni `.ciclo`, así que de las seis reglas solo le alcanza la de `.formula` (tiene dos): la del módulo
que se abre al cargar cabe entera a 1200 px (740/740) y no enseña sombra; a otros anchos no se miró.

## 3. Colores y contraste

Contraste sobre blanco con la fórmula de WCAG 2.x, calculado (no estimado):

| Papel | Antes | Después | Contraste |
|---|---|---|---|
| Serie observada ($y_t$ o $\log y_t$) | `#012820` o gris `#94a3b8` según el gráfico | `#012820` siempre | 15.84:1 |
| Tendencia estimada (media móvil, clásica, STL) | `#FF6600` (2.94:1) | `#FB6400` | 3.03:1 |
| Estacional | `#0e7490` | sin cambio | 5.36:1 |
| Residuo y referencias (envolvente, hipótesis aditiva) | `#94a3b8` (2.56:1) | `#8795A9` | 3.04:1 |
| Desestacionalizada | `#012820` (M8) o gris (M7) | `#7c3aed` (nuevo) | 5.70:1 |
| Rampa del gráfico estacional | naranja → verde | `#5F9F90` (1949) → `#012820` (1960) | 3.07:1 → 15.84:1 |

- **Cómo se eligieron.** El naranja y el gris son los tonos más próximos al original que llegan a 3:1 oscureciendo sin
  cambiar de tinte: escalando el RGB, el primero que llega es `#FB6500` (3.016) y `#8896AA` (3.004); se tomó un paso más
  (`#FB6400`, 3.033; `#8795A9`, 3.043) para no quedar a tres milésimas del umbral. `#FC6500` se queda en 2.9998.
- **La misma serie, el mismo color.** La observada es verde oscuro en M1, M4, M5, M6, M7, M8 y el quiz (antes, gris en
  M5, M8 y el quiz); cuando hace de fondo va más fina (1 px), no más clara. La tendencia es naranja en M4, M5, M6, M7 y
  el quiz. La desestacionalizada es morada en M8 y en el ajuste local. Como la observada pasa a ser verde oscuro en el
  M8, la desestacionalizada necesitaba un color propio; el turquesa habría sido engañoso (es justo el componente que se
  le ha quitado), de ahí el quinto color.
- **Excepción declarada: `loess-local`.** Ese simulador compara tres estimaciones de una misma tendencia (Loess, media
  móvil, `stl()`) y las tres no pueden ir en naranja: en el interior coinciden y se taparían. Conserva su código propio
  —verde oscuro la curva Loess y el valor guardado, naranja la ventana y la recta, turquesa discontinuo la media móvil,
  gris punteado la tendencia de `stl()`—, que su intro y su leyenda explican. Es el P5 de su ficha y queda **sin
  resolver**: lo decide el docente (ver §5).

## 4. Contradicciones entre la prosa y el gráfico, comprobadas

Evidencia completa: `diagnostico/cap1/comprobaciones/r2_graficas.R` → `r2_graficas.out`.

1. **Comparador (M4): «valen lo mismo al nivel de partida» frente a la lectura «20.0 … 23.6».** La prosa **no está
   mal**. Con $T_t = 100 + 2t$, $A = 20$ y $a = A/T_0 = 0.2$: al nivel de partida las dos oscilaciones valen 20.0
   ($A$ y $a \cdot T_0$). Lo que la lectura mide es el máximo de todo el año 1, que en la multiplicativa cae en el mes
   10 ($t = 9$), cuando el nivel ya vale 118: $0.2 \times 118 = 23.6$. Dentro del año 1 el nivel sube de 100 a 122.
   Cambio: no se tocó la intro ni ninguna cifra de la lectura; se le añadió una frase que el propio simulador calcula
   (`d.T[0]`, `d.T[11]`, `A`): «La multiplicativa ya queda por encima en el año 1 porque dentro de ese año el nivel sube
   de 100 a 122: las dos oscilaciones valen lo mismo, 20.0, solo al nivel de partida.» Con β = 0 la frase no sale
   (las dos dan 20.0). Capturas: `m4-comparador-escala-escritorio`, `…-beta4-A40-…` (100 a 144), `…-beta0-…`.
2. **STL (M7): «el residuo no tiene estructura visible».** La prosa **estaba mal**. Con
   `stl(log(AirPassengers), s.window = "periodic")`, la desviación típica del residuo por año es 0.0370, 0.0416, 0.0471,
   0.0372, 0.0350 (1949–1953), 0.0245 (1954), 0.0171, 0.0141, 0.0194 (1955–1957) y 0.0407, 0.0252, 0.0421 (1958–1960):
   de media 0.040 al principio, 0.017 en el centro y 0.036 al final, la misma U que el M6 llama «estructura». Además,
   el residuo de julio es negativo los cinco primeros años y positivo los siete últimos (−0.060 … +0.055), y la
   autocorrelación en los rezagos 1 y 12 es 0.371 y 0.341 (banda de ruido blanco: ±0.163). Con los paneles altos se ve
   a simple vista (`m7-descomp-stl-escritorio`). Cambio mínimo en la intro del simulador, sin cifras: «Nota que la
   tendencia llega hasta los extremos. El residuo oscila alrededor de 0 sin tendencia, pero no es ruido puro: es más
   disperso en los primeros y en los últimos años que en los centrales.» **Para el docente:** la causa (un patrón
   estacional fijo, `periodic`, que no puede seguir a una estacionalidad que cambia) no se ha escrito; es materia de
   T3.2.
3. **Lo que afirman los `aria-label` nuevos**, comprobado en R: el máximo de cada año cae en julio (7 años) o en agosto
   (5); solo 1954 tiene meses por debajo del mismo mes del año anterior («casi siempre por encima»); el índice clásico
   y el estacional de STL tienen el máximo en julio y el mínimo en noviembre; el residuo clásico multiplicativo también
   es más disperso en los extremos (0.028–0.048) que en el centro (0.013–0.022); la 2×12 da 132 valores con 6 `NA` por
   extremo, m = 5 da 140 y la 2×24, 120 (lo mismo que la lectura nueva del M5).

## 5. Lo que queda sin tocar o para decidir

1. **Lectura nueva en el M5.** La ficha la pedía (P1), pero es una frase con cifras que antes no estaba en pantalla.
   Las cuenta el simulador sobre la curva que dibuja y coinciden con R y con la prosa («de las 144 quedan 132»). Si
   se considera que excede «solo presentación», se quita borrando el `<p class="simulador-lectura">` del simulador
   `media-movil`: el código lo tolera.
2. **`loess-local` pasa de uno a dos lienzos** dentro del mismo `data-simulador` (el contador de la portada cuenta
   `data-simulador`, no lienzos: `cuenta_sitio.py` no se mueve). Es un cambio de encuadre, no de cálculo, pero es el
   más visible de la ronda.
3. **Colores del ajuste local** (§3): la excepción queda declarada, no resuelta.
4. **Quinto color** (`#7c3aed`, morado) para la desestacionalizada: no es de la paleta de la casa.
5. **`construye-tu-serie`**: valores iniciales A = 10, σ = 5; eje y que se reescala; sin lectura (R3).
6. **Deslizadores 0-1 de grado y pesos** en el ajuste local (R3, junto con la convención de pesos de `stl()`).
7. **El 0.8012 de noviembre** no tiene marca en el panel estacional del M6; **la U del residuo aditivo y los cocientes
   de julio** siguen sin gráfico (R3, T3.4).
8. **Tablas a 375 px** y **la fórmula en línea del quiz** (R3 y R5).
9. **El mapa estacional sigue sin presentación en la prosa** y las bandas de julio-agosto solo destacan desde 1954
   (la escala la manda la tendencia): es de R3.
10. **La plantilla solo recibió CSS.** Su `COLORES_GRAFICO`, su `crearGraficoLinea` y su `panelComponente` siguen
    como estaban; los capítulos 2–6 no se tocaron (D3: se llevan en la ronda de cada uno).
11. **Modo oscuro, impresión y tooltips** siguen fuera de la revisión, como en el diagnóstico.

## 6. Accesibilidad (T2.3)

- Los 21 `<canvas>` del capítulo (20 en el marcado —uno más que antes, por el segundo lienzo del ajuste local— y el del quiz) tienen un `aria-label` que dice lo que se ve. Los de
  `comparador-escala`, `construye-tu-serie`, `media-movil` y `loess-local` se reescriben al mover un control. Ninguno
  lleva una cifra que no esté en la prosa, en los datos o en los controles.
- `aria-live="polite"` en las tres lecturas que cambian con un control: `comparador-escala`, `media-movil` (nueva) y
  `loess-local`. Las de `amplitud-nivel` y `serie-vs-log` son estáticas y no lo llevan.
- Los cuatro paneles del ciclo tienen `aria-labelledby` hacia su pestaña.
- Las leyendas en HTML son listas con `aria-label="Leyenda del gráfico"`; las muestras de color van con
  `aria-hidden`.

## 7. Comprobaciones finales (desde la raíz del worktree)

| Comprobación | Resultado |
|---|---|
| `python3 precalculo/genera_referencias.py --comprobar \| head -2` | `OK capitulo-1-…: 3 citas, sin cambios` · `OK capitulo-2-…: 0 citas, sin cambios` |
| `python3 precalculo/audita_citas.py \| tail -2` | `[A01] 74 apellidos … sin <cite>` (aviso que ya estaba) · `OK auditoría de citas` |
| `python3 precalculo/cuenta_sitio.py \| grep -c MAL` | `5` (igual que antes de la ronda) |
| `python3 precalculo/audita_posicion_correcta.py \| tail -1` | `Ningún instrumento concentra las correctas.` |
| `python3 precalculo/compila_tailwind.py --comprobar \| tail -2` | `hojas: páginas 12.9 KB · portada 11.0 KB`, salida 0 (igual que antes) |
| `python3 proyecto/audita_proyecto.py \| tail -3` | `Todo limpio.` |
| `python3 precalculo/verifica_todo.py` | 10 de 11 en verde; falla solo `cuenta_sitio.py`, con las mismas 5 cifras de la portada que ya fallaban antes de la ronda (64/65 módulos, 68/70 simuladores) |

## Después de la verificación independiente (2026-11-11)

Un verificador que no hizo los cambios (Opus 5.5, contexto limpio) volvió a capturar los gráficos a 1200,
800 y 375 px, midió desbordes y alturas, comparó las series y las lecturas de cada lienzo contra la versión
anterior (idénticas, salvo las dos frases añadidas y los extremos de dos rectas de referencia) y recalculó
en R las afirmaciones nuevas (exactas). Encontró cinco problemas, corregidos por la sesión que dirige:

| Dónde | Qué pasaba | Qué quedó |
|---|---|---|
| Ciclo del M6 (capítulo y plantilla) | Entre 667 y 1000 px las etapas quedaban en 3+1 o en 2×2 con una flecha colgando; el panel, justificado con huecos | El ciclo decide por el ancho de SU contenedor: una fila si mide más de 640 px, en vertical si no. Comprobado a 375, 667, 800, 1000, 1024 y 1400 px |
| Ciclo a 375 px | «↺» dos veces | En vertical la vuelta solo la dice la frase de debajo |
| Línea de referencia de los paneles | 2.88:1 | 3.59:1 |
| Franja de la ventana (Loess) | Relleno de 1.25:1, sin borde | Con sus dos bordes dibujados |
| `amplitud-nivel` | Las dos rectas de hipótesis, mismo trazo y misma luminancia | La aditiva punteada, la multiplicativa discontinua (también en la leyenda) |
| Media móvil con m = 2 | «faltan 1», «le faltan 1 meses» | «falta 1», «le falta 1 mes» |
| Nota del mapa a 375 px | Justificada, con huecos | Alineada a la izquierda |
| Textos | El comentario de la paleta y un `aria-label` («tamaño proporcional al peso») decían de más | Ajustados a lo que el código hace |

Queda como está: las cifras de las celdas del mapa miden 8.8 px a 375 px. Caben las doce columnas sin
desplazamiento, que era el defecto grave; agrandarlas obliga a desplazar o a rediseñar el mapa.

No miró: tooltips, teclado del ciclo, modo oscuro, impresión, y anchos distintos de los tres (salvo el ciclo).
