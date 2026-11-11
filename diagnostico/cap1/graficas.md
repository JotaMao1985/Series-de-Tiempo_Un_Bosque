# Capítulo 1 · revisión de gráficas y simuladores (dibujados)

Archivo: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (worktree `course-content-improvement-227f2c`), servido por
`http://localhost:8731/`. Revisado el 2026-11-10 con Chrome sin ventana por CDP (arnés propio en
`diag/harness/cdp.js`, `extra.js`, `tablas.js`; no se tocó el repo).

- Anchos: **escritorio 1200 px** (área de contenido 822 px), **teléfono 375 px** (`mobile:true`, dsf 2; área 345 px) y
  **800 px** (solo medidas + algunas capturas; ahí la barra lateral se come 280 px y el área queda en **438 px**).
- En las capturas por elemento se desactivó la cabecera fija para que no tapara el gráfico. Las vistas `mN-vista-movil.png`
  son la pantalla real del teléfono (cabecera y botón «subir» incluidos).
- Sin excepciones ni `console.error/warn` en ninguno de los 9 módulos y los 3 anchos.
- Medidas crudas: `diag/medidas.json` y `diag/medidas-extra.json`.
- Capturas: `diag/capturas/` (ruta completa al final de cada ficha).

Ruta base de capturas:
`diagnostico/cap1/capturas/`
(abreviada abajo como `…/capturas/`).

Contraste sobre blanco de la paleta de los gráficos (`COLORES_GRAFICO`, l. 4514): primario `#012820` 15.8:1 ·
terciario `#0e7490` 5.4:1 · **secundario `#FF6600` 2.94:1** · **gris `#94a3b8` 2.56:1**. Los dos últimos quedan por
debajo del 3:1 que pide WCAG 1.4.11 para objetos gráficos.

---

## M1 · `serie-airpassengers` — canvas l. 2362 (JS l. 4676)

- **Pretende**: el gráfico de tiempo; «se ve una tendencia creciente y un patrón que se repite cada 12 meses cuya amplitud
  aumenta con el nivel».
- **Se ve (escritorio)**: los tres rasgos se ven sin esfuerzo. Eje y 100–700, marcas de enero `1949-01 … 1960-01`.
- **Problemas**
  1. **A 375 px las fechas se montan**: `1949-011951-06 1953-11 1956-041958-09` (marcas cada 29 meses, en meses
     arbitrarios y pegadas). Defecto común a todas las series de 144 meses.
  2. Sin título de ejes; la unidad solo aparece en la leyenda («Pasajeros (miles)»), y una leyenda de una sola serie es
     ruido. La prosa del capítulo habla de «364 pasajeros», «de 44 a 232 pasajeros» y el mapa dice «622 pasajeros»:
     la unidad no es la misma en todo el capítulo.
  3. `aria-label` solo nombra («Serie mensual de pasajeros…»): no dice tendencia ni abanico.
- Capturas: `…/capturas/m1-serie-airpassengers-escritorio.png`, `…/capturas/m1-serie-airpassengers-movil.png`,
  `…/capturas/m1-vista-movil.png`

## M3 · mapa estacional `data-mapa="cap1-airpassengers"` — HTML l. 2553 (JS l. 5961, pintor l. 5871)

- **Pretende**: «las bandas verticales de julio y agosto son la estacionalidad; que se oscurezcan hacia abajo es la
  tendencia; que la diferencia crezca es lo que la hace multiplicativa».
- **Se ve (escritorio)**: rejilla 12×12 con la cifra en cada celda; el oscurecimiento hacia abajo es evidente. Las bandas
  de julio-agosto **solo destacan de 1954 en adelante**: la escala secuencial va de 104 a 622 y la tendencia se come casi
  todo el rango, así que en 1949-1953 todas las celdas son del mismo verde pálido y la estacionalidad hay que leerla en
  las cifras, no en el color.
- **Problemas**
  1. **A 375 px y a 800 px la rejilla se corta en julio** (`scrollWidth` 476 de 303 visibles a 375 px): agosto —una de
     las dos bandas que la nota manda mirar— y el resto del año quedan fuera, con desplazamiento horizontal pero sin
     ninguna pista de que lo hay.
  2. Unidad «pasajeros» en la leyenda frente a «Pasajeros (miles)» del M1 y «miles de pasajeros» del M4.
  3. Ninguna frase de la prosa presenta el mapa: aparece antes del gráfico estacional y no está entre los «cuatro
     gráficos» de la lista del módulo.
  4. Letra pequeña (celdas 0.63 rem ≈ 10 px, leyenda 0.64 rem en gris `#64748b`).
- **Bien resuelto**: `role="table"` con `columnheader`/`rowheader` y una etiqueta accesible por celda («Jul 1955: 364
  pasajeros»); el color nunca es el único canal; el número cambia a blanco por luminancia.
- Capturas: `…/capturas/m3-mapa-estacional-escritorio.png`, `…/capturas/m3-mapa-estacional-movil.png`,
  `…/capturas/m3-mapa-estacional-800.png`

## M3 · `grafico-estacional` — canvas l. 2568 (JS l. 4689)

- **Pretende**: una línea por año; «el pico de mediados de año se repite y crece año tras año»; la nota siguiente:
  «un abanico que se abre … indica que la estacionalidad crece con el nivel».
- **Se ve**: el pico de julio y el abanico se ven bien a los dos anchos.
- **Problemas**
  1. **No hay forma de saber qué línea es qué año**: leyenda apagada (`display:false`), sin rótulos en los extremos ni
     barra de color. El degradado naranja (1949) → verde (1960) no se explica en ningún sitio, y los años centrales
     (1953-1957) son marrones casi iguales entre sí. Se deduce «arriba = después» solo porque hay tendencia.
  2. Sin título del eje y ni unidad.
  3. Título del simulador **desordenado a 375 px**: «Gráfico / estacional / de» en columna con `AirPassengers` al lado
     (ver «Defectos repetidos», punto 4).
  4. `aria-label` describe la construcción («una línea por año…, meses en el eje horizontal»), no lo que se ve.
- Capturas: `…/capturas/m3-grafico-estacional-escritorio.png`, `…/capturas/m3-grafico-estacional-movil.png`

## M4 · `comparador-escala` — canvas l. 2695 (aditivo) y l. 2702 (multiplicativo) (JS l. 4731)

- **Pretende**: misma tendencia y misma forma estacional; a la izquierda la banda conserva la anchura, a la derecha se
  ensancha; los paneles comparten eje vertical.
- **Se ve (escritorio)**: el contraste es claro y responde a los controles: con β = 4, A = 40 el abanico multiplicativo es
  enorme; con β = 0 los dos paneles son idénticos y la lectura da ×1.00 en ambos. Eje y compartido de verdad.
- **Problemas**
  1. **A 800 px el panel multiplicativo desaparece fuera de la página** (solo asoma «Mult…»): el `.grafico-par` pasa a
     dos columnas por `min-width: 768px` de *viewport*, pero el área de contenido mide 438 px; las columnas salen de
     326 px cada una (668 px en 308) y `main` las recorta. Es el tamaño de una tableta en vertical o media pantalla de
     portátil. Ver `m4-vista-800.png`.
  2. **A 375 px los dos paneles se salen de la caja del simulador** (columna de rejilla de 323 px en un contenedor de
     259 px: `1fr` sin `minmax(0, …)` deja que el lienzo imponga su ancho mínimo). En la pantalla real
     (`m4-vista-movil.png`) el gráfico atraviesa el borde de la caja, llega al canto de la tarjeta y esta le recorta
     ~10 px (los últimos meses del año 8). Las capturas por elemento `…-movil.png`, recortadas a la caja, exageran la
     pérdida: valen para ver el desborde, no para medir cuánto se pierde.
  3. **Marcas del eje x pegadas en escritorio**: «Año 1Año 2Año 3Año 4…» (`autoSkip:false` con 8 rótulos en 255 px).
  4. Extremos del eje y con cifras raras: `63.9 … 364.08` (dos decimales en un eje de enteros), `23.3 … 708.7`,
     `77.6 … 122.4`: son los `min`/`max` explícitos, que Chart.js rotula.
  5. **La lectura parece contradecir al texto**: la intro dice que las dos oscilaciones «valen lo mismo al nivel de
     partida», y la lectura inicial da «año 1: aditiva 20.0, multiplicativa 23.6». La lectura mide el máximo de todo el
     año 1, cuando el nivel ya subió de 100 a 122; el estudiante ve 20 ≠ 23.6 y no sabe por qué.
  6. Leyenda repetida en los dos paneles; la etiqueta HTML ya dice cuál es cuál.
  7. `aria-label` describe el resultado (bien), pero es fijo: con β = 0 sigue diciendo que la banda «se ensancha».
- Capturas: `…/capturas/m4-comparador-escala-escritorio.png`, `…/capturas/m4-comparador-escala-beta4-A40-escritorio.png`,
  `…/capturas/m4-comparador-escala-beta0-escritorio.png`, `…/capturas/m4-comparador-escala-movil.png`,
  `…/capturas/m4-comparador-escala-beta4-A40-movil.png`, `…/capturas/m4-comparador-escala-beta0-movil.png`,
  `…/capturas/m4-comparador-escala-800.png`, `…/capturas/m4-vista-800.png`, `…/capturas/m4-vista-movil.png`

## M4 · `amplitud-nivel` — canvas l. 2754 (JS l. 4867)

- **Pretende**: los 12 años como puntos (nivel, amplitud) frente a la horizontal (aditivo) y el rayo (multiplicativo);
  «los puntos abandonan la horizontal desde el primer año … acompañan al rayo, sí, pero se le quedan por encima».
- **Se ve**: exactamente eso, a los dos anchos. Es el único gráfico del capítulo con **títulos en los dos ejes**, y el eje
  y empieza en 0 como debe. La lectura da las razones (×3.76, ×5.27; 34.7 % → 48.7 %).
- **Problemas**
  1. El año de cada punto solo sale al pasar el cursor; en el teléfono no hay cursor. Rotular al menos 1949 y 1960.
  2. Eje y sin unidad («Amplitud estacional (máx − mín)»), eje x en «miles de pasajeros»: la misma magnitud con dos
     unidades distintas en un mismo gráfico.
  3. Eje x con última marca irregular (`450 → 520`) y, a 375 px, `100 · 200 · 400 · 520` (se salta el 300).
  4. La referencia aditiva es gris `#94a3b8` discontinua (2.56:1).
  5. A 375 px la leyenda ocupa tres líneas (73 px) y el área útil queda en 168 × 156 px.
- Capturas: `…/capturas/m4-amplitud-nivel-escritorio.png`, `…/capturas/m4-amplitud-nivel-movil.png`

## M4 · `serie-vs-log` — canvas l. 2785 (original) y l. 2792 (log) (JS l. 4959, usa `panelComponente` l. 5288)

- **Pretende**: «a la izquierda el vaivén crece con el nivel; a la derecha … se mantiene casi igual de ancho».
- **Se ve (escritorio)**: el rasgo se ve. La lectura da ×5.27 frente a ×1.32.
- **Problemas**
  1. **Mismo desbordamiento que el comparador**: a 800 px el panel logarítmico queda fuera (`m4-serie-vs-log-800.png`
     muestra solo el original); a 375 px los dos se salen de la caja del simulador y la tarjeta les recorta los últimos
     meses (mismo mecanismo y misma salvedad sobre las capturas por elemento que en el comparador).
  2. **Marcas del eje x montadas en escritorio**: `1949-011950-101952-071954-041956-011957-10 1959-07` (cada 21 meses,
     sin espacio).
  3. Eje y con solo 3-4 rótulos y valores no redondos (`62.6 · 500 · 663.4`; `4.5 · 5 · 6 · 6.6`), herencia de
     `panelComponente` (`maxTicksLimit: 4` + `min`/`max` explícitos).
  4. La misma serie cambia de color (verde oscuro → turquesa) solo por estar en log; leyendas redundantes con la etiqueta
     del panel.
- Capturas: `…/capturas/m4-serie-vs-log-escritorio.png`, `…/capturas/m4-serie-vs-log-movil.png`,
  `…/capturas/m4-serie-vs-log-800.png`

## M4 · `construye-tu-serie` — canvas l. 2814 (JS l. 4599)

- **Pretende**: mover β, A y σ «para aislar el efecto de cada componente … Haz clic en la leyenda para ocultar
  componentes».
- **Se ve**: responde bien a los tres controles (β = 2, A = 30, σ = 0 da una onda limpia sobre una recta; β = −1, σ = 20
  da una serie decreciente y ruidosa). Etiquetas con símbolo y valor visible.
- **Problemas**
  1. **Estado inicial poco elocuente**: con A = 10 y σ = 5 el patrón de 12 meses apenas se distingue del ruido, y la
     curva «Estacionalidad» arranca **oculta** (tachada), al revés de lo que dice la intro («para ocultar»).
  2. **Marcas del eje x cada 10 meses** (`2016-01, 2016-11, 2017-09…`): en el simulador que enseña un período de 12, las
     marcas no caen nunca en el mismo mes. A 375 px, cada 30 meses.
  3. El eje y se reescala en cada movimiento: al subir σ el dibujo «encoge», y la comparación entre estados se hace
     contra un eje que cambia.
  4. Sin lectura numérica: solo se mueve el dibujo.
  5. Fechas 2016-2025 inventadas sin aviso (menor).
- Capturas: `…/capturas/m4-construye-tu-serie-escritorio.png`,
  `…/capturas/m4-construye-tu-serie-beta2-A30-sigma0-escritorio.png`,
  `…/capturas/m4-construye-tu-serie-beta-neg-sigma20-escritorio.png`, `…/capturas/m4-construye-tu-serie-movil.png`,
  `…/capturas/m4-construye-tu-serie-beta2-A30-sigma0-movil.png`, `…/capturas/m4-construye-tu-serie-beta-neg-sigma20-movil.png`

## M5 · `media-movil` — canvas l. 2906 (JS l. 5000)

- **Pretende**: «con m pequeño la curva sigue el ruido; al llegar a m = 12 desaparece la estacionalidad … órdenes muy
  grandes también recortan los extremos».
- **Se ve**: los tres rasgos. m = 5 ondula al ritmo del año; m = 12 sale lisa; m = 24 se acorta un año por cada lado.
- **Problemas**
  1. **Sin lectura numérica**: el texto del módulo apoya el argumento en «de las 144 quedan 132», y el simulador no dice
     cuántas observaciones se pierden ni cuánta estacionalidad queda.
  2. A 375 px, marcas montadas (`1949-011951-06 …`) y título desordenado: «Simulador: / media móvil `AirPassengers` /
     sobre» (el orden de lectura queda cambiado).
  3. La leyenda arranca como «Media móvil» y pasa a «Media móvil (m=5)» al primer movimiento.
  4. La observada es gris de 1 px (2.56:1): como fondo vale, pero en el teléfono casi desaparece.
  5. `aria-label` fijo, sin el orden m.
- Capturas: `…/capturas/m5-media-movil-escritorio.png`, `…/capturas/m5-media-movil-m5-escritorio.png`,
  `…/capturas/m5-media-movil-m24-escritorio.png`, `…/capturas/m5-media-movil-movil.png`,
  `…/capturas/m5-media-movil-m5-movil.png`, `…/capturas/m5-media-movil-m24-movil.png`

## M6 · componente «ciclo» `data-ciclo="descomposicion"` — HTML l. 2973 (JS l. 5788)

- **Pretende**: «no forman una receta sino un bucle; el último … dicta si hay que volver atrás».
- **Se ve**: cuatro tarjetas-pestaña; al pulsar la 4 cambia el panel (probado). A 375 px se apilan con flechas ↓.
- **Problemas**
  1. **No se dibuja como un ciclo**: en escritorio (822 px) el paso 4 cae a una segunda fila, con una flecha «→» colgando
     al final de la primera, y la vuelta 4 → 1 solo existe como frase («↺ Descomponer no es una fórmula…»).
  2. **Contradicción con el propio capítulo**: el paso 1 dice «La decisión es visual, no hay prueba automática», pero el
     M4 pide «desconfiar de eso y convertirlo en un número» (tabla y gráfico de amplitud/nivel) y el M9 trae un «Criterio
     cuantitativo: elasticidad amplitud-nivel» (l. 3902).
  3. Paso 2, «Con qué»: `stats::filter(y, rep(1/m, m))` es la media móvil simple de m términos, no la 2×m centrada que el
     mismo panel dice necesaria con m par (a revisar por quien redacta).
  4. Paneles `role="tabpanel"` sin `aria-labelledby` (sin nombre accesible). Teclado (flechas, con vuelta) bien resuelto
     en código; no lo probé pulsando teclas.
  5. A 375 px el texto justificado del panel abre huecos grandes.
- Capturas: `…/capturas/m6-ciclo-escritorio.png`, `…/capturas/m6-ciclo-paso4-escritorio.png`,
  `…/capturas/m6-ciclo-movil.png`, `…/capturas/m6-ciclo-paso4-movil.png`

## M6 · `descomp-clasica` — canvas l. 3194 (observada), 3195 (tendencia), 3196 (estacional), 3197 (residuo) (JS l. 5323)

- **Pretende**: los cuatro componentes; «estacional y residuo oscilan alrededor de 1»; el aviso final remite a «los huecos
  en el panel de tendencia»; la prosa manda «leer el panel estacional»: noviembre, 0.8012, el mes más flojo.
- **Se ve**: el orden, los huecos de la tendencia (empieza en jul-1949 y acaba en jun-1960) y la oscilación alrededor de 1.
  Pero todo está **aplastado**.
- **Problemas**
  1. **Área de dibujo de 35 px de alto** por panel (contenedor de 120 px menos leyenda de 32 px y eje x): la observada
     parece casi plana y el abanico que justifica el modelo multiplicativo no se aprecia.
  2. **Ejes y casi sin rótulos y con cifras no redondas**: observada `62.6 / 663.4` (solo dos marcas, sin nada entre
     medias), tendencia `98.9 / 502.9`, estacional `0.8 / 1.0 / 1.3`. No se puede leer un valor; y el 0.8012 de
     noviembre que cita la prosa no es localizable en el panel (marcas solo en enero).
  3. **Los paneles no comparten el eje de tiempo**: el área de dibujo de observada y tendencia mide 619 px y la de
     estacional y residuo 632 px, así que la misma fecha cae 13 px más a la izquierda en los dos de abajo (≈3 meses en
     escritorio, ≈9 meses a 375 px). En una descomposición, la alineación vertical de fechas es lo que se lee.
  4. Cuatro leyendas y cuatro ejes x repetidos ocupan más que los datos.
  5. A 375 px: fechas montadas (`1949-011951-061953-111956-04958-09`), `663.4` pegado a `500`, y el título roto
     («Descomposición / multiplicativa / de» + `AirPassengers` a un lado).
  6. Residuo en gris `#94a3b8` (2.56:1): el panel que, según el M4, «juzga el trabajo» es el de menos contraste.
  7. `aria-label` = «Componente observado», «Componente tendencia»…: nombran, no describen.
  8. Observada y tendencia están en las mismas unidades pero con escalas distintas (62.6-663.4 frente a 98.9-502.9).
- La prosa describe la U del residuo aditivo y la deriva de los once cocientes de julio con listas de cifras, sin gráfico
  que lo muestre: candidatos naturales a un panel.
- Capturas: `…/capturas/m6-descomp-clasica-escritorio.png`, `…/capturas/m6-descomp-clasica-movil.png`,
  `…/capturas/m6-descomp-clasica-800.png`

## M7 · `loess-local` — canvas l. 3449 (JS l. 5092)

- **Pretende**: mover el foco y ver la ventana (tamaño del punto = peso), la recta local y «el punto verde» que se
  guarda; llevar el foco a 1949-01 o 1960-12 y ver que la media móvil desaparece; bajar grado y pesos a 0 y comprobar
  que vuelve a ser la media móvil.
- **Se ve**: el foco mueve la ventana (con foco 1949-01 la ventana se apoya solo hacia adelante); grado 0 + pesos planos
  aplana la curva en los bordes; span 61 la vuelve casi recta. **La lectura es la mejor del capítulo**: cambia con cada
  control y da exactamente las cifras que cita la prosa (5.5482 = 5.5482; 6.2043 frente a 6.2048; «la media móvil no da
  nada aquí»).
- **Problemas**
  1. **Lo que hay que mirar no se ve a esta escala**: cuatro curvas (desestacionalizada, tendencia de stl(), media móvil,
     Loess) se superponen en una banda de 1-2 px sobre un eje 4.6-6.4; las diferencias que el texto discute (0.0005 en
     el centro, 0.0498 en el borde) son invisibles. Que la media móvil «desaparece» en los extremos se lee en la lectura,
     no en el dibujo. Falta un zoom alrededor del foco o un segundo panel.
  2. **«El punto verde» no se distingue**: el rombo `#012820` queda tapado por los círculos naranjas de la ventana (en
     escritorio y teléfono la ventana es una mancha naranja). Además, el «verde» del texto se ve negro.
  3. A 375 px la leyenda ocupa **5 líneas (118 px) y el área útil queda en 194 × 91 px**; el valor del foco («1954-12»)
     se parte en dos líneas dentro de su insignia; marcas de fecha montadas.
  4. Dos grises casi iguales (desestacionalizada y tendencia de stl()) que solo distingue el punteado.
  5. El naranja cambia de significado respecto del resto del capítulo (aquí ventana/recta; en M5, M6 y M7-STL la
     tendencia), y la media móvil pasa de naranja (M5) a turquesa discontinuo.
  6. Grado y pesos son conmutadores de dos posiciones presentados como deslizadores 0-1 (funcionan, pero un interruptor
     o dos botones se leerían mejor).
- Capturas: `…/capturas/m7-loess-local-escritorio.png`, `…/capturas/m7-loess-local-foco1-escritorio.png`,
  `…/capturas/m7-loess-local-foco144-escritorio.png`, `…/capturas/m7-loess-local-grado0-planos-escritorio.png`,
  `…/capturas/m7-loess-local-span61-escritorio.png`, `…/capturas/m7-loess-local-movil.png` (y sus `-movil` por estado)

## M7 · `descomp-stl` — canvas l. 3602 (log observada), 3603 (tendencia), 3604 (estacional), 3605 (residuo) (JS l. 5335)

- **Pretende**: «la tendencia llega hasta los extremos y el residuo no tiene estructura visible»; el aviso posterior: «el
  tercer panel es una onda perfectamente regular».
- **Se ve**: la tendencia sí llega a los extremos y la onda estacional es regular. Mismos defectos de forma que el M6.
- **Problemas**
  1. Los mismos 35 px de área por panel, ejes con 2-3 marcas no redondas (`4.5 / 6 / 6.6` con 6 y 6.6 casi encimados;
     tendencia `4.7 / 6.3`), desalineación de 6.6 px entre paneles, leyendas repetidas, fechas montadas a 375 px.
  2. **«El residuo no tiene estructura visible» merece una segunda mirada**: en el panel se ve más dispersión al principio
     y al final que en el centro. Con los datos incrustados (`DATOS_CAP1.stl_log.residuo`, cálculo mío de diagnóstico,
     no para pantalla) la desviación típica por año va de ≈0.035-0.045 en 1949-1953 a ≈0.013-0.016 en 1955-1957 y
     vuelve a ≈0.024-0.040 en 1958-1960: la misma forma de U que el M6 llama «estructura en el residuo». Que lo juzgue
     quien redacta y, si se cita alguna cifra, que salga de R.
  3. `aria-label` = «log observado», «tendencia STL»…: solo nombran.
- Capturas: `…/capturas/m7-descomp-stl-escritorio.png`, `…/capturas/m7-descomp-stl-movil.png`

## M8 · `desestacionalizada` — canvas l. 3740 (JS l. 5348)

- **Pretende**: «la línea desestacionalizada (y/Ŝ) elimina el diente de sierra mensual y deja la tendencia-ciclo más un
  residuo suave».
- **Se ve**: la observada en gris y la ajustada en verde, mucho más lisa. Bien a los dos anchos salvo las fechas.
- **Problemas**
  1. **El gráfico no dice con qué Ŝ se calculó, y es el clásico** (`clasica_multiplicativa.estacional`), mientras el
     módulo arranca «con componentes en los que se puede confiar» tras el STL y calcula F_T, F_S sobre STL. Por eso
     quedan picos de julio en 1958-1960 (índice fijo que subestima los julios finales, lo que el M6 explica): no es un
     «residuo suave».
  2. A 375 px, fechas montadas; leyenda en dos líneas.
  3. `aria-label` solo nombra.
- Capturas: `…/capturas/m8-desestacionalizada-escritorio.png`, `…/capturas/m8-desestacionalizada-movil.png`

## M9 · gráfico del quiz (pregunta 4, `tipo:'grafico'`) — creado por JS (registro l. 6061; contenedor `data-quiz="cap1"` l. 3862)

- **Pretende**: que se vea que la tendencia 2×12 no llega a los extremos.
- **Se ve**: se ve, a los dos anchos; a 375 px las marcas salen cada 3 años y no se montan.
- **Problemas**: el enunciado identifica la curva por el color («la línea naranja»), aunque la leyenda la nombra;
  naranja 2.94:1. Su `aria-label` sí describe el rasgo (el mejor del capítulo junto con los del M4).
- Capturas: `…/capturas/m9-quiz-grafico-escritorio.png`, `…/capturas/m9-quiz-grafico-movil.png`,
  `…/capturas/m9-quiz-grafico-solo-movil.png`

---

## Fórmulas y tablas

- **M8, F_T y F_S** (l. 3748): una sola línea de 617-641 px. A 800 px (contenedor de 356 px) y a 375 px (301 px) se ve
  **solo F_T**; F_S queda entera fuera, dentro de una caja con desplazamiento horizontal y sin pista visual de que lo
  hay. `…/capturas/m8-formula-FT-FS-800.png`, `…/capturas/m8-formula-FT-FS-movil.png`,
  `…/capturas/m8-formula-FT-FS-escritorio.png` (en escritorio cabe).
- Otras que desbordan su caja a 800 px y a 375 px (mismo patrón, menos grave): M4 aditivo/multiplicativo con
  `\underbrace` (391/356 px), M5 media 2×12 (446/356 px), M7 tricúbica (430/356) y bicuadrada (429/356).
- M9: fórmula en línea `F_T = 1 − Var/Var` dentro de un enunciado del quiz sobresale 20 px a 800 px y la recorta `main`.
- **Tablas a 375 px** (se desplazan dentro de su caja, sin pista): M2 conceptos (363/303 px, se corta la columna Python),
  M4 amplitud (326/303, se corta «Amplitud / nivel»), **M6 pasos aditivo/multiplicativo** (370/303: la columna
  multiplicativa queda fuera, justo la tabla que pide leerse «en horizontal», y las fórmulas en línea se parten a mitad,
  p. ej. «d_t = y_t − / T̂_t»). `…/capturas/m2-tabla-conceptos-movil.png`, `…/capturas/m4-tabla-amplitud-movil.png`,
  `…/capturas/m6-tabla-pasos-movil.png`.

## Defectos repetidos (arreglo de una sola vez)

1. **`.grafico-par` desborda** (CSS l. 1742): `grid-template-columns: 1fr` sin `minmax(0, 1fr)` y el paso a dos columnas
   por *viewport* ≥ 768 px aunque el área de contenido mida 438 px. Rompe los dos pares del M4 a 375 y a 800 px.
2. **Marcas de fecha**: todas las series de 144 meses usan etiquetas `AAAA-MM` y `maxTicksLimit: 12` con autoSkip de
   Chart.js, que elige meses arbitrarios y las pega a 375 px (M1, M5, M6×4, M7×5, M8) y en escritorio en los paneles
   estrechos (M4). Un callback común en `crearGraficoLinea`/`panelComponente` que rotule solo eneros como «1949» y salte
   años según el ancho lo arregla en todos; en el comparador, quitar `autoSkip:false`.
3. **`panelComponente`** (l. 5288), usado por 10 lienzos: área de 35 px, `maxTicksLimit: 4` con `min`/`max` explícitos
   (rótulos tipo 62.6/663.4), una leyenda por panel y un eje x por panel, y ancho de eje y variable que desalinea las
   fechas. Arreglo: panel más alto (≥ 160 px), título en vez de leyenda, eje x solo en el último, `grace`/redondeo en vez
   de min/max crudos y ancho fijo del eje y (`afterFit`).
4. **Títulos `.simulador h4`** (CSS l. 826, `display:flex`): el texto y el `<code>` son ítems flex separados; en pantalla
   estrecha el texto se parte en columna y el código queda centrado a su lado, cambiando el orden de lectura (M3, M5, M6;
   «Simulador: media móvil `AirPassengers` sobre»).
5. **Contraste**: gris `#94a3b8` (2.56:1) en 8 series y naranja `#FF6600` (2.94:1) en todas las tendencias. `#64748b`
   (4.76:1) para el gris y un naranja algo más oscuro (p. ej. `#e05a00`, 3.73:1) pasan el 3:1.
6. **Accesibilidad**: 9 de 19 lienzos solo nombran («Componente residuo», «log observado»); ninguno actualiza su
   `aria-label` con los controles; las `.simulador-lectura` no llevan `aria-live`, así que un lector de pantalla no oye
   el resultado al mover un control. Los deslizadores sí tienen `<label for>` y valor visible.
7. **Sin títulos de eje ni unidades** salvo en `amplitud-nivel`; y la unidad cambia («pasajeros», «Pasajeros (miles)»,
   «miles de pasajeros»).
8. **Leyendas de una sola serie** (M1, M4 log, 8 paneles) que repiten la etiqueta del panel y, a 375 px, comen hasta la
   mitad del lienzo (loess: 118 px de 237).
9. **Colores por papel, no por serie**: la observada es verde oscuro (M1, M4, M6, M7-STL) o gris (M5, M8, quiz); la media
   móvil es naranja (M5) o turquesa (M7); la tendencia de STL es naranja (M7-STL) o gris punteado (M7-loess). Es una
   convención defendible («gris = contexto»), pero no está dicha en ningún sitio.
10. Formato de números: punto decimal en todo el capítulo (bien, `Chart.defaults.locale = 'en-US'`); solo desentonan los
    extremos de eje con 1-2 decimales sueltos (63.9, 364.08, 502.9).

## Lo que NO pude capturar o mirar, y por qué

- **Información emergente (tooltips)**: no simulé el paso del cursor; su contenido lo juzgo solo por el código (modo
  `index` en las series, desactivado en el comparador y en loess, propio en `amplitud-nivel`).
- **Teclado del componente ciclo**: comprobado el clic sobre el paso 4; las flechas solo por código.
- **Tablas del M9**: están dentro de soluciones plegadas (ancho 0 al cargar); no las desplegué ni medí.
- **Modo oscuro / impresión**: fuera de la revisión.
- **Gráficos de subseries y de rezagos** que enumera el M3: no existen en el capítulo, así que no hay nada que mirar
  (la prosa los presenta entre los «cuatro gráficos que hacen casi todo el trabajo»).
- De las 70 capturas abrí y miré 51; las restantes son estados en teléfono de simuladores ya vistos en escritorio y en
  teléfono en otro estado (`m4-comparador-escala-beta*-movil`, `m4-construye-tu-serie-movil` y `-beta-neg-…-movil`,
  `m5-media-movil-movil` y `-m24-movil`, `m7-loess-local-foco1/foco144/grado0-planos/span61-movil`,
  `m6-ciclo-paso4-movil`, `m9-quiz-grafico-movil`, `m4-comparador-escala-800`, y las `mN-vista-movil` de M3 y M5-M9).
  Sus medidas sí están en `medidas.json`.
