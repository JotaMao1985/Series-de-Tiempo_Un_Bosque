# Capítulo 1 · R3-bis · el M7 reordenado y las dos sesiones de lectura

Ronda del 2026-11-13. Un solo redactor. Sin commits. Archivos tocados:

- `Htmls_Series/capitulo-1-componentes-descomposicion.html` (M7, apertura del M1, `courseData`,
  `renderNavigation()` y dos reglas CSS nuevas).
- `Htmls_Series/index.html` (una frase en la tarjeta del capítulo 1).
- `diagnostico/cap1/herramientas/r3bis_elemento.js` y tres `r3bis_*.json` (arnés y tareas).
- `diagnostico/cap1/capturas/r3bis/` (13 capturas).

Ninguna cifra nueva: no hay guion `r3bis_*` en `comprobaciones/` porque no hizo falta.

## 1 · El orden del Módulo 7

Los bloques se movieron enteros (por rangos de líneas, con un guion), sin tocar su interior salvo las
cinco frases de enlace de la sección siguiente.

### Antes

| # | Bloque | Primera frase |
|---|---|---|
| A | Apertura (`c1-m7-01`) | «**STL** (*Seasonal-Trend decomposition using Loess*) responde a esas tres debilidades una por una…» |
| B | h3 «El método, paso a paso» + los cinco pasos | «Igual que el método clásico, STL parte de un período $m$ conocido y devuelve tres series.» |
| C | Lo que cambia frente al clásico | «Frente al recorrido del Módulo 6 cambian tres cosas, una por debilidad.» |
| D | h3 «Qué hace una regresión local»: Loess, span, tricúbica, tabla de pesos, bordes | «La media móvil del Módulo 5 tomó tres decisiones sin discutirlas…» |
| E | Simulador `loess-local` | «El ajuste local, punto a punto» |
| F | Tres lecturas + desarrollo `der-loess-ajuste` | «Del simulador salen tres lecturas que conviene no dejar pasar.» |
| G | h3 «La versión robusta, y por qué no viene puesta» (`c1-m7-02`) + desarrollo `der-robustez` | «Las dos primeras respuestas salen solas del ajuste local. La tercera, no.» |
| H | h3 «Las tres respuestas, a la vista» (`c1-m7-03`) + simulador `descomp-stl` + «La ventana estacional» + «El atípico» + código R/Python | «Dos apuntes antes de verlo funcionar.» |
| I | Nota de cierre | «Lo que queda por hacer con los componentes…» |
| J | Fuentes del módulo (`<!--FUENTES-MODULO-->`) | — |

### Después

| # | Bloque | Qué es |
|---|---|---|
| A | Apertura (`c1-m7-01`) | (a) qué es STL |
| B | «El método, paso a paso» + cinco pasos | (a) qué hace y qué devuelve |
| C | «Frente al recorrido del Módulo 6 cambian tres cosas…» | (b) qué se gana frente al clásico — íntegro |
| H | «Las tres respuestas, a la vista»: los dos apuntes, simulador `descomp-stl`, «La ventana estacional», «El atípico», código | (b) la descomposición a la vista |
| — | **Párrafo de enlace nuevo** | puente a «por dentro» |
| D | «Por dentro: qué hace una regresión local» | (c) Loess, pesos, bordes |
| E | Simulador `loess-local` | (c) |
| F | Tres lecturas + `der-loess-ajuste` | (c) |
| G | «La versión robusta, y por qué no viene puesta» + `der-robustez` | (c) robustez — íntegro |
| I | Nota de cierre | puente al M8 |
| J | Fuentes del módulo | — |

El simulador `descomp-stl` pasa de estar a unas 1 450 palabras del inicio a quedar justo después de los cinco
pasos y del párrafo C. Los tres `data-afirma` del módulo se leen ahora en el orden 01, 03, 02 (cada uno viajó
con su párrafo; su texto no cambió). El módulo sigue teniendo 2 simuladores, 6 lienzos, 2 desarrollos, 4 h3,
un bloque de código y una lista de fuentes.

## 2 · Frases de enlace cambiadas (cinco) y una añadida

1. **Apertura (A), última frase**, fuera del `data-afirma`.
   Antes: «Antes de abrir esa herramienta conviene saber qué hace el método con ella, y en qué orden.»
   Ahora: «Antes de abrir esa herramienta conviene saber qué hace el método con ella y verlo funcionar: el
   módulo enseña primero la descomposición, y deja para después el ajuste local, sus pesos y la opción
   robusta.» — Por qué: anuncia el orden nuevo; la frase vieja prometía abrir la herramienta enseguida.
2. **«El atípico» (H)**: tras «acaba con peso 0» se inserta «—el último apartado del módulo explica cómo—».
   Por qué: el peso de robustez se explicaba antes de este párrafo y ahora se explica después.
3. **Párrafo nuevo entre el código y «Por dentro»**: «Hasta aquí, lo que STL hace y lo que se gana con él.
   Queda cómo lo consigue: qué es ese Loess que los pasos 1 y 2 dan por sabido, por qué su tendencia llega a
   los extremos, y de dónde sale el peso 0 con que la opción robusta aparta al julio inflado. El resto del
   módulo abre el método por dentro, en ese orden.» — Es la única prosa nueva del módulo.
4. **Título del h3 de D**: «Qué hace una regresión local» → «Por dentro: qué hace una regresión local».
   Ningún verificador ni otro archivo cita ese título (comprobado con grep).
5. **`der-robustez`, paso 3**: «Sirve el caso que el capítulo usa hasta el final.» → «Sirve el caso del
   simulador de STL, que el capítulo usa hasta el final.» — Por qué: el julio inflado se presentaba aquí por
   primera vez y ahora el lector ya lo movió en el simulador.
6. **Nota de cierre (I)**: «los paneles están en logaritmos» → «los paneles de STL están en logaritmos». —
   Por qué: la nota seguía a los paneles y ahora sigue al desarrollo de la robustez.

## 3 · Remisiones revisadas

Leído el módulo de corrido tras mover. Arregladas: las de los puntos 1, 2, 5 y 6. Revisadas y dejadas, porque
siguen apuntando bien:

- «el `t.window` del paso 2» y «las pasadas del paso 4»: los cinco pasos siguen yendo antes.
- «así lo toma el simulador de más abajo» (D): `loess-local` sigue inmediatamente debajo.
- «Del simulador salen tres lecturas» y «el desarrollo de abajo lo mide» (F): adyacentes, como antes.
- «La primera cierra el módulo anterior», «la diferencia de fondo con el módulo anterior», «la media móvil del
  Módulo 5», «los once cocientes del Módulo 6», «el gráfico de subseries del Módulo 3»: no dependen del orden
  interno.
- «Las dos primeras respuestas salen solas del ajuste local. La tercera, no.» (G): sigue yendo tras Loess.
- «Dos apuntes antes de verlo funcionar» (H): ahora es literal; antes llegaba al final del módulo.
- Las 13 menciones del «Módulo 7» en el resto del capítulo (M3, M5, M6, M8, M9, quiz): ninguna depende del
  orden interno.

## 4 · Las dos sesiones de lectura

**Capítulo, índice lateral.** `courseData` gana un campo `sesion` por módulo (1 para los módulos 1–5, 2 para
los 6–9) y un diccionario `sesiones` con los rótulos «Sesión 1 · Describir» y «Sesión 2 · Descomponer».
`renderNavigation()` pinta un `<div class="nav-sesion">` delante del primer módulo de cada sesión. No es un
botón ni un módulo: `courseData.modules.length`, `loadModule`, los anclajes `#modulo-N`, el progreso (los
vistos buenos) y «Anterior/Siguiente» no lo miran. CSS propio en el `<style>` del capítulo (`.nav-sesion` y
`.nav-sesion:not(:first-child)`, con la misma línea gris que separa el título «Contenido»); ninguna clase de
Tailwind nueva; la plantilla no se tocó porque no se cambió ninguna regla compartida.

**Capítulo, apertura (M1).** Párrafo nuevo tras «Separar esa mezcla es el asunto de este capítulo…»: «El
capítulo está pensado para leerse en **dos sesiones**, con el corte tras el Módulo 5: los módulos 1 a 5
describen la serie y preparan las herramientas —…—, y los módulos 6 a 9 la descomponen —el método clásico,
STL, el ajuste estacional y el cierre—.»

**Portada.** En la tarjeta del capítulo 1, al final de la descripción: «Se lee en dos sesiones: módulos 1 a 5
y módulos 6 a 9.» Nada más cambió en `index.html`; ninguna cifra tocada.

## 5 · Lo que se miró

Chrome sin ventana por CDP (`r3bis_elemento.js`, que pone el `?v=` antes del ancla: el arnés de R3 lo ponía
detrás y `#modulo-7?v=…` abría el Módulo 1). A 1200, 800 y 375 px:

- Entrada directa por `#modulo-7`: carga el 7. «Siguiente» → 8; tres «Anterior» → 5; «Siguiente» → 6 (el
  cruce del separador); clic en el índice al 9 y al 1; `hashchange` a `#modulo-7`. Todo bien.
- Los nueve módulos cargan; 0 `.katex-error`; consola sin errores ni avisos; `scrollWidth` del documento igual
  al ancho en los 27 casos; 9 botones y 2 rótulos en el índice.
- A 800 px dos tablas (M2 y M6) rozan el borde dentro de su propio desplazamiento: ya estaban, no son de esta
  ronda.
- A 375 px el índice lateral no se muestra (ya era así: `.sidebar-container` es `display:none` bajo 768 px);
  en el teléfono la señal de las dos sesiones es la frase de la apertura.

Capturas en `capturas/r3bis/`: `indice-{1200,800}.png`, `indice-m7-activo-{1200,800}.png`,
`m7-entero-{1200,800,375}.png`, `m1-entero-{1200,800,375}.png`, `portada-tarjeta-{1200,800,375}.png`.

## 6 · Lo que se dejó sin tocar

- Cifras, datos, gráficos, simuladores, código R y Python, desarrollos plegados (siguen plegados).
- El texto de los seis `data-afirma`, los `<cite class="cita">` y los marcadores; los tres pares
  `<!--FUENTES-MODULO-->` siguen cada uno dentro de su módulo (M6, M7, M8).
- El párrafo C («Frente al recorrido del Módulo 6…») y el apartado de la robustez (G1 y G2), íntegros.
- Duraciones de los módulos, número de módulos, simuladores, ejercicios y preguntas.
- La plantilla y la guía del proyecto.

## 7 · Para que lo mire el docente

- **El 19 del código aparece antes de explicarse.** El bloque de R dice «window = 19 es justo lo que STL
  calcula solo» y el de Python «R evalua el ajuste local a saltos e interpola»; el porqué de las dos cosas
  está ahora más abajo (D y `der-loess-ajuste`). Son comentarios de código y se entienden solos; no se
  tocaron porque el encargo excluye el código.
- **El código se quedó con la figura** (bloque b), no al final del módulo: el objetivo dice «aplicar».
- **Los rótulos** «Describir» y «Descomponer» son una propuesta corta; se cambian en `courseData.sesiones`.
- **El teléfono no tiene índice**, así que allí no hay separador. Si se quiere una señal al terminar el
  Módulo 5 (junto al botón «Siguiente»), es un cambio pequeño que no entraba en el encargo.
