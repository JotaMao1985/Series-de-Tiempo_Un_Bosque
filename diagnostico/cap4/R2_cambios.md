# R2 · Registro de cambios · Capítulo 4 «Modelos ARIMA» · gráficas y simuladores

Ronda R2 del `PLAN_Mejora_Cap4.md` (tareas T2.1–T2.2; decisión D4). Fecha: 2026-11-22. Un solo redactor.
Especificación: `diagnostico/cap4/graficas.md` (44 problemas, 7 defectos de causa común). Base: `b3e9042`. Sin commit ni push.

**Archivos tocados**

| archivo | qué |
|---|---|
| `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` | armazón, a mano: 3 sustituciones (§2). Ninguna prosa, ningún dato |
| `ensamblado/cap4/chapter.js` | 39 sustituciones: ayudantes nuevos, `escalasLinea`, los `pintar()` de los diez simuladores con gráficos, marcos, leyendas, `aria-label` y las dos `descripcionGrafico` del quiz. Nada de los enunciados, opciones, claves ni retros del quiz, ni de `SIMULACROS` |
| `ensamblado/cap4/templates_1_3.html`, `_4_6`, `_7_9`, `_10` | alto inicial de 17 marcos, dos iconos y el `aria-label` inicial del ΔAICc (una letra: «ΔAICc») |
| `Htmls_Series/capitulo-3-…html`, `-5-…`, `-6-…` | reensamblados (`ensambla_cap3.py --escribir`, luego 4, 5 y 6); reciben **las mismas 68 líneas añadidas y 6 quitadas** cada uno, y también el 2: md5 del diff idéntico en los cuatro (`b38db31a790ef3dd8c8038fc133147e5`), todas del armazón (§2) |
| `Htmls_Series/capitulo-4-modelos-arima.html` | reensamblado; 395 líneas añadidas y 100 quitadas = las 68/6 del armazón + las de `ensamblado/cap4/` |
| `diagnostico/cap4/comprobaciones/r2_*` | guiones y salidas de la ronda |
| `diagnostico/cap4/capturas/r2/` | capturas (git las ignora) |

No se tocó `plantilla/plantilla-capitulo.html`, ni `Htmls_Series/preparcial-corte-2.html`, ni el deck, ni `SIMULACROS['cap4-simulacro']`, ni el orden de los módulos, ni
`DATOS_CAP4`/`SERIES_CAP4`, ni ningún bloque de R o de Python, ni `verifica_directo_cap4.R`. Ninguna clase nueva de Tailwind
(`compila_tailwind.py --comprobar` en verde dentro de `verifica_todo.py`). Ninguna cita, autor ni año nuevos; nada copiado de
`bibliografia/_local/`. Ninguna prosa nueva salvo una frase de la lectura del M9 (la del caudal negativo) y rótulos de leyenda.

**Guiones** (`diagnostico/cap4/comprobaciones/`)

| guion | salida | qué hace |
|---|---|---|
| `r2_edita.py` | — | reaplica sobre HEAD las 60 sustituciones (cada marcador, único); `--comprobar` dice si el árbol coincide. Después hay que reensamblar 3 → 4 → 5 → 6 |
| `r2_iconos.js` | `r2_iconos_candidatos.out`, `r2_iconos.out` | qué iconos de Font Awesome 6.0.0 se dibujan, sobre la hoja que carga el capítulo; y que ya no queda ninguno vacío en los 12 módulos |
| `r2_cifras.R` | `r2_cifras.out` | las cifras que la ronda hace aparecer (cotas del eje de la traza, el límite inferior del 95 % de cada forma, ΔAICc por d y barras cortadas, los valores y la banda de los dos gráficos del quiz, media/varianza/ρ̂₁ por d, ψ y σ_h), recalculadas en R aparte de la página |
| `r2_revisa.js` | `r2_medidas.json`, `r2_revisa.log` | cap. 4 por HTTP (Chrome sin ventana, `diag/chrome.js`): 11 simuladores × 82 estados × 1200, 800 y 375 px, con captura de cada uno; mide área de dibujo, rótulos, solapes, leyenda, `aria-label`, marcadores recortados y si el lienzo está pintado |
| `r2_resumen.py` | `r2_resumen.out` | resumen de esas medidas |
| `r2_quiz.js` | `r2_quiz.out` | los dos gráficos del quiz a los tres anchos: píxeles pintados, área, leyenda y `aria-label` completo; captura de la pantalla real (las que hizo `r2_revisa.js` salieron en blanco o corridas con el recuadro del elemento) |
| `r2_tabla.py` | `r2_tabla.out` | una línea por lienzo y ancho (estado inicial), en el formato de `diag/graficas_tabla.out`, para compararla con la de antes |
| `r2_recorrido.js` | `r2_recorrido_{antes,despues}.json` y `.log` | recorrido de humo de los caps. 2–6, todos los módulos, a 1200, 800 y 375 px; «antes» es HEAD servido desde `git archive` |
| `r2_compara.py` | `r2_compara.out` | antes frente a después: consola, lienzos sin gráfico, desbordes, el 1, el 12 y el 24 en los ejes de rezagos, solapes; y qué cambia fuera del cap. 4 |
| — | `r2_bloques_cap{2..6}.out`, `r2_verifica_todo.out` | los verificadores al cerrar |

Las capturas son `capturas/r2/mN-<simulador>[-<estado>]-{1200,800,375}.png`; las `mN-vistaK-{800,375}.png` son la pantalla real con la
cabecera fija; `recorrido-despues/` son las del recorrido de los caps. 2–6.

---

## 1. Los 44 problemas, uno por fila

Estados: **A** arreglado · **P** en parte · **R1** lo resolvió la ronda R1 · **N** no tocado (con motivo). «Antes» son las medidas del
informe; «ahora», las de `r2_tabla.out` y `r2_resumen.out`.

| Ficha | Problema | Estado | Qué se hizo, o por qué no | Captura |
|---|---|---|---|---|
| M1 · `nilo-y-diferencia` | 1 [Baja] años sin redondear y solapes a 800/375 | **A** | `escalasLinea` reinstala `marcasLegibles`/`rotuloLegible`: 1200 `1880 … 1970` de 10 en 10; 800 `1880 … 1960`; 375 `1875 … 1950`; ningún solape en ningún estado | `m1-nilo-y-diferencia-d{0,1,2}-{1200,800,375}` |
| | 2 [Baja] guion y sin línea del 0 | **A** | `rotuloVertical` (signo menos) y `rejillaConCero`: d = 1 y 2 rotulan `−400 … 400` con el 0 oscuro | las mismas |
| | 3 [Baja] `aria-label` fijo | **A** | Dice la serie (d, años, n, media, varianza, ρ̂₁); cambia en cada estado | — |
| M3 · `escalon-vs-raiz` | 1 [Media] área de la tasa de 94 px a 1200 | **A** | Marco de 200 a 260 px (`ALTOS_CURVA.ancho`): 154 px de dibujo a 1200 (antes 94); 164 y 167 a 800 y 375. La recta del 5 % queda a ~8 px del 0. La serie de arriba, de 200 a 230 px (115 → 145) | `m3-escalon-vs-raiz-beta0-1200` |
| | 2 [Baja] marcador β recortado | **A** | `clip: false` en el conjunto «β elegido»: los 27 casos en el borde (β = 0, β ≥ 200) salen enteros | `…-beta300-{1200,375}` |
| | 3 [Baja] leyenda con cajas | **A** | Armazón (§2): raya continua, raya discontinua, punto y raya punteada, cada una con su trazo. A 375 px las cinco entradas, en dos renglones (antes tres), con rótulos más cortos (`KPSS ℓ = 4 (R)`, `5 % nominal`, `Nilo 247.8`) | `…-beta100-375` |
| | 4 [Baja] eje x a 375 sin aire | **A** | `1875 1900 1925 1950`; sin solapes | `…-beta100-375` |
| | 5 [Baja] `aria-label` fijos | **A** | La serie dice el descenso y la media; la tasa, el porcentaje con ℓ = 4 y con ℓ = 12 para el β elegido | — |
| M4 · `identificacion-nilo` | 1 [Media] ACF y PACF de 75 px a 1200 | **A** | `ALTOS_BARRAS.ancho` de 180 a 250: 145 px de dibujo (75 antes). Las barras de 0.21 a 0.24 de d = 0 (rezagos 4–7, 11–13) quedan a 2–3 px de la banda (antes 1–2) y la del rezago 8, a unos 7 px: el rango del eje sigue siendo de −1 a 1, como en todos los correlogramas del curso, y es lo que limita la separación | `m4-identificacion-nilo-d0-1200` |
| | 2 [Baja] icono vacío | **A** | `fa-magnifying-glass-chart` (6.1) → `fa-chart-column` (6.0). `r2_iconos.out`: ningún icono vacío en los 12 módulos | `m4-identificacion-nilo-d0-1200` |
| | 3 [Baja] serie con años sin redondear, guion | **A** | Como M1; el marco de la serie sube de 170 a 230 px (85 → 145 px de dibujo) | las mismas |
| | 4 [Baja] `aria-label` fijos | **A** | `descripcionCorrelograma()` del armazón: «ACF muestral de la serie del Nilo sin diferenciar, rezagos 1 a 20: 11 de 20 barras fuera de la banda ±0.196…»; la serie, su rango y su media | — |
| M6 · `explorador-modelos` | 1 **[Alta]** ΔAICc con 5 de 9 rótulos a 1200 | **A** | Sin salto automático (`autoSkip: false`) y rótulo de dos renglones (el modelo y, debajo, `↑74`): los nueve modelos con nombre, el `↑121`, `↑27`, `↑74` y `↑51` incluidos, en **los 27 estados a los tres anchos** (`r2_resumen.out`: «estados con menos rótulos que barras: 0 de 27» ×3). El marco sube de 200 a 250 px (154 px de dibujo). A 800 y 375 sigue tumbado, con los nueve a la izquierda | `m6-explorador-modelos-pdq020-{1200,800,375}` |
| | 2 [Baja] la muestra toma el color de la primera barra | **A** | `leyendaDeColores()`: la leyenda es el código, `Elegido` (naranja), `Mejor de su d` (verde), `Los demás` (gris), igual en todos los estados | `…-pdq000-1200`, `…-pdq111-1200`, `…-pdq122-1200` |
| | 3 [Baja] la barra del mejor, de 3 px | **P** | Sigue de 3 px (`minBarLength`), pero la leyenda ya nombra su color y el `aria-label` dice que el mejor está a +0.00. No se engrosó: la altura de una barra de valor 0 es una convención | `…-pdq122-1200` |
| | 4 [Baja] `aria-label` | **A** | ACF de residuales con `descripcionCorrelograma`; el ΔAICc dice «ΔAICc de los 9 modelos con d = 2 …, el elegido, ARIMA(0,2,0), está a +121.01; 4 barras se cortan en 20 y llevan su valor en el rótulo» | — |
| M7 · `traza-auto-arima` | 1 [Media] cruces de AICc = ∞ cortadas por la mitad | **A** | Las cruces van en una fila propia (`TECHO` = 5 por encima del último rótulo con cifra, calculado de los AICc finitos de las dos búsquedas) que el eje rotula «∞», y `clip: false`: se ven enteras en los pasos 1 y 18 de la escalonada y 21, 27–30 de la exhaustiva (`r2_resumen.out`: las 5 cruces dentro). La leyenda dibuja una cruz | `m7-traza-auto-arima-exh-paso42-{1200,800,375}` |
| | 2 [Media] la muestra cambia de color con el modo | **A** | Los puntos se parten en dos conjuntos con su entrada cada uno: `Modelo evaluado` (verde oscuro) y `Mejora del mejor AICc` (naranja, más grande). La leyenda es igual en los dos modos (`r2_resumen.out`) | `…-exh-paso1-1200`, `…-paso1-1200` |
| | 3 [Media] leyenda de 3 líneas y 78–81 px a 800/375 | **A** | Leyenda compacta (`lineaCompacta`) con rótulos cortos en el teléfono (`Evaluado`, `Mejora`, `Mejor hasta aquí`, `∞ (descartado)`): dos renglones; el marco, de 230 a 260/290 px: 175 y 178 px de dibujo (antes 78 y 81) | `…-exh-paso21-{800,375}` |
| | 4 [Baja] rótulos inclinados, paso irregular, puntos cortados | **A** | `marcasLegibles` con `maxRotation: 0` (`1 2 4 … 18` a 1200, `1 3 6 … 18` a 800 y 375; con la exhaustiva, `1 12 24 36` a 375); el eje y rotula de 5 en 5 (`1265 … 1300`) y el ∞ en la fila de arriba, en vez de saltar de 1295 a 1302; `offset: true` y `clip: false` dejan enteros el primer y el último punto | `…-paso18-{1200,375}` |
| M8 · `sobrediferenciacion` | 1 [Baja] eje logarítmico con 3 rótulos | **A** | Marcas explícitas en 1 y 3 por potencia de diez: `10 000 · 30 000 · 100 000 · 300 000`. Las barras de d = 0 y d = 1 (28 638 y 28 268) caen casi sobre el 30 000; la de d = 3 (262 507), cerca del 300 000. La leyenda explica los colores (`Orden elegido`, `Los demás`) | `m8-sobrediferenciacion-d3-1200` |
| | 2 [Baja] serie con años sin redondear y guion | **A** | Como M1 | `…-d2-375` |
| | 3 [Baja] `aria-label` fijos | **A** | La serie dice d, n, rango y varianza; la varianza dice las cuatro y cuál está elegida | — |
| M9 · `forma-pronostico` | 1 **[Alta]** el pronóstico sin constante no se queda en el último nivel | **R1** | La R1 lo dijo en la prosa (la tabla: «se aplana en 842.17, no en el último dato (740)»). Se comprobó que el dibujo casa: último caudal observado 740 (1970), ŷ(1971) = 816.18 y ŷ(2000) = 842.17, que son las cifras de la lectura, de la tabla y de la frase de debajo (`r2_cifras.out` §2). No se tocó el dibujo: el enganche al último observado es lo que el texto describe | `m9-forma-pronostico-d1-1200` |
| | 2 [Media] leyenda de 4 líneas a 375; «Pronóstico» como caja | **A** | `lineaCompacta` (tipografía compacta) y `Observado` en el teléfono: dos renglones, 208 px de dibujo (132 antes). «Pronóstico» es una raya naranja; los intervalos, cajas | `m9-forma-pronostico-d2-375` |
| | 3 [Baja] banda negativa con d = 2 | **A** | Basta una frase, y sale de los datos: con d = 2 y bandas visibles la lectura añade «límite inferior 95 % (h=30) −775.67 — por debajo de 0, y un caudal no puede ser negativo» (−775.67, de `r2_cifras.out` §2). El eje sigue llegando a −1000: es lo que dibuja el intervalo | `m9-forma-pronostico-d2-{1200,375}` |
| | 4 [Baja] x a 375 con seis solapes | **A** | `1900 1950 2000` a 375; `1880 … 2000` de 20 en 20 a 1200; sin solapes | `…-d1-375` |
| M9 · `pesos-psi-sigma` | 1 [Media] σ_h con 74/52/55 px | **A** | σ_h: marco de 180 a 240/260 px: 135/145/148 px de dibujo. ψ: de 180 a 240 px (75 → 135) | `m9-pesos-psi-sigma-h30-{1200,800,375}` |
| | 2 [Baja] marcadores h = 1 y h = 30 cortados | **A** | `clip: false` y `offset: true`: enteros en los tres anchos | `…-h30-375` |
| | 3 [Baja] eje de los ψ hasta 1.5 | **A** | `min: 0` y `max` = el máximo de los datos (1): `0.0 … 1.0`; la leyenda dice qué barras entran en σₕ (extra: el naranja y el gris no se explicaban) | `…-h15-1200` |
| | 4 [Baja] σ_h sin el 30 | **A** | `marcasLegibles` y, a 800 px, `marcasConUltimo` (el paso de 4 de `marcasLegibles` dejaba el eje en 28): `1 3 6 … 30` a 1200, `1 4 8 12 16 20 24 30` a 800, `1 6 12 18 24 30` a 375; el 30 sale a los tres anchos | `…-h30-{1200,800,375}` |
| | 5 [Baja] icono vacío | **A** | `fa-arrows-left-right-to-line` (6.1) → `fa-arrows-left-right` (6.0) | `…-h1-375` |
| M10 · `trm-identificacion` | 1 [Media] ACF de 75 px | **A** | `barrasCompactas` con `ALTOS_ACF` (250 px): 145 px de dibujo a 1200 y 141–144 a 800/375. La serie, de 190 a 230 px | `m10-trm-identificacion-d1-1200` |
| | 2 [Baja] fechas `AAAA-MM` crudas | **A** | Eneros con su año: `2015 … 2026` a 1200; `2016 2019 2022 2025` a 800 y 375; sin solapes | `…-d0-{1200,800,375}` |
| | 3 [Baja] ∇TRM con guion, sin línea del 0 | **A** | `−400 … 400` con el 0 oscuro | `…-d1-800` |
| | 4 [Baja] `aria-label` fijos | **A** | La serie dice el rango (meses, mín y máx); la ACF, `descripcionCorrelograma` | — |
| M10 · `trm-abanico` | 1 [Media] leyenda de 4 líneas a 375 y 112 px | **A** | Dos renglones y 208 px de dibujo | `m10-trm-abanico-h36-375` |
| | 2 [Baja] fechas irregulares | **A** | `2023 2024 … 2028` (según h), sin solapes | `…-h36-{1200,800,375}` |
| | 3 [Baja] `aria-label` | **A** | Dice el horizonte, el pronóstico y el intervalo del 95 % (los de la lectura) | — |
| M10 · `puente-estacional` | 1 [Baja] `aria-label` | **A** | `descripcionCorrelograma`: modelo, barras fuera de la banda, ρ̂₁ | — |
| | 2 [Baja] leyenda de 2 líneas y 95–98 px | **A** | Rótulo `ACF residual` a 800/375 (el modelo ya está en el selector y la lectura) y marco de 220 a 240 px: 141–144 px | `m10-puente-estacional-no-375` |
| M10 · quiz | 1 [Media] `descripcionGrafico` de la ACF del Nilo | **A** | Ahora da los datos que se ven: «Función de autocorrelación muestral de una serie sin diferenciar. Valores de los rezagos 1 a 20, en orden: 0.50, 0.38 … 0.11. Banda de referencia: ±0.196» (`r2_cifras.out` §4: 9 de 20 dentro de la banda; la descripción ya no afirma nada que el dibujo contradiga ni da el veredicto). Enunciado, opciones, orden, clave y retros, intactos | `m10-quiz-grafico2-{1200,800,375}` |
| | 2 [Baja] `descripcionGrafico` del correlograma mensual | **A** | Igual: los 26 valores y la banda ±0.163; 8 de 26 salen de la banda (rezagos 2, 5, 7, 12, 14, 19, 24 y 26) | `m10-quiz-grafico1-{1200,800,375}` |
| | 3 [Baja] 82 px a 375 | **A** | `alto: 250` (antes 200): 132 px a 375, 129–150 a 800 y 150 a 1200 | las mismas |

**Recuento:** 44 problemas = **42 arreglados (A), 1 en parte (P: la barra de 3 px del mejor del M6), 1 que resolvió la R1 (M9, el pronóstico sin constante) y 0 no
tocados (N)**. Por gravedad: de las 2 Altas, una arreglada aquí (M6, el ΔAICc) y una de la R1 (M9); de las 10 Medias, las 10 arregladas; de las 32 Bajas, 31
arregladas y 1 en parte. Por ficha (3 + 5 + 4 + 4 + 4 + 3 + 4 + 5 + 4 + 3 + 2 + 3 = 44).

Las 7 causas comunes, todas arregladas: **A** `escalasLinea` (§3), **B** los 18 lienzos más los 2 del quiz (§3, §4), **C** el armazón (§2), **D** los marcos (§3),
**E** `clip: false` (§3), **F** las leyendas de colores (§3) y **G** los dos iconos (filas M4-2 y M9ψ-5).

## 2. Armazón (capítulo 2 → 3, 4, 5 y 6)

Tres sustituciones en `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html`, la región heredada:

| # | Cambio | Qué mueve en la cadena |
|---|---|---|
| 1 | **`etiquetasDeLeyendaLinea`** (junto a `etiquetasDeLeyendaBarras`): en la leyenda de `crearGraficoLinea`, las series y las rectas de referencia salen como un trozo de su trazo (con su discontinuidad), las bandas (`fill` hacia otra serie: `'+1'`, `'-1'`, un índice) como una caja de su color y su borde, y los puntos sueltos (`showLine: false`) con su marca (círculo, cruz) | Todos los gráficos de línea de los caps. 2–6. En los barras no cambia nada |
| 2 | **`crearGraficoLinea` mezcla la muestra de la leyenda** con lo que el capítulo pase en `plugins.legend.labels`: quien pasaba su propio `plugins` (los tres abanicos del cap. 4, el cap. 5) perdía la muestra del armazón; ahora la conserva, y su fuente, `boxWidth` y filtro mandan | Igual |
| 3 | **Plugin `anchoDeLaMuestra`** también en los gráficos de línea (como el de barras): la raya y la caja miden `boxWidth` aunque el capítulo lo cambie al crear el gráfico; si la leyenda tiene un punto suelto, la muestra mide lo de siempre, porque Chart.js estira un círculo hasta hacer un óvalo cuando se le fija el ancho | Igual |

`git diff` de los caps. 2, 3, 5 y 6: 68 líneas añadidas y 6 quitadas cada uno, idénticas (md5 del diff igual): solo estas tres piezas. En el 4 se suman a las de
`ensamblado/cap4/`. `r2_compara.out` mide, en los caps. 2, 3, 5 y 6 antes y después, qué cambia fuera del 4: solo la muestra de la leyenda (sección «Lo que cambia fuera del capítulo 4»).

## 3. Lo propio del capítulo 4 (`chapter.js`)

- **`escalasLinea` (A):** reinstala `marcasLegibles`/`rotuloLegible` en x y `marcasVerticales`/`rotuloVertical`/`rejillaConCero` en y, y mezcla `x.ticks` clave a clave
  (antes un `ticks` propio de un capítulo sustituía todos los ayudantes). Los dos gráficos que pasaban `ticks` con `maxTicksLimit: 10` (forma y abanico) ya no lo
  pasan. Las escalas escritas a mano se rehicieron sobre ella: la traza (x con `marcasLegibles`; y con `marcasTraza`, de 5 en 5 y el ∞ arriba), σ_h (x con
  `marcasLegibles`, y desde 0) y la varianza (log con marcas explícitas). La de la tasa KPSS del M3 es numérica (0–300 de 50 en 50, con «%»): no necesitaba ayudantes.
- **`aria-label` (B):** `ariaLienzo()` los reescribe en cada `pintar()` en los 18 lienzos, con el signo menos; los correlogramas usan `descripcionCorrelograma()`. Todas
  las cifras salen de los datos incrustados (`r2_cifras.out` las recalcula en R). `r2_resumen.out`: «lienzos cuyo `aria-label` no cambia entre estados: ninguno» a los tres anchos.
- **Marcos (D):** nuevas alturas `ancho`/`estrecho` en `ALTOS_CURVA` (200/280 → 260/280), `ALTOS_BARRAS` (180/240 → 250/240), `ALTOS_RESIDUALES` (210 → 240), `ALTOS_AICC`
  (200 → 250), y `ALTOS_TRAZA` (260/290), `ALTOS_FORMA` (280/300), `ALTOS_PSI` (240), `ALTOS_SIGMA` (240/260), `ALTOS_ACF` (250/240), `ALTOS_ABANICO` (280/300) y
  `ALTOS_PUENTE` (240) para los que no tenían; los gráficos de línea usan `lineaCompacta` (la leyenda a la medida del ancho). **El área de dibujo mínima de todos los
  estados es de 134.8 px a 1200, 135.8 a 800 y 138.8 a 375** (antes 74, 52 y 55): `r2_resumen.out`, «lienzos con alguna área < 110 px: ninguno».
- **Leyendas (C, F):** `leyendaDeColores()` para los gráficos de barras con un color por barra (ΔAICc, varianza, ψ); la traza parte sus puntos en dos conjuntos.
- **Recorte (E):** `clip: false` en el marcador β, los puntos y cruces de la traza y los marcadores de σ_h.

## 4. Quiz del M10

Solo las dos `descripcionGrafico` (y `alto: 250` en las dos preguntas, que mide el lienzo): `describirBarrasQuiz()` da los valores en orden y la banda, sin el corte
ni el veredicto, como en el cap. 3. `AUTOEVALUACIONES['cap4']` queda igual en enunciados, opciones, orden, clave y retros.

## 5. Verificación al cierre

- `python3 diagnostico/cap4/comprobaciones/r2_edita.py --comprobar`: los seis archivos idénticos a HEAD + las 60 sustituciones (cada marcador, único).
  `ensambla_cap3.py` verifica «reproducible byte a byte»; el 4, el 5 y el 6 se reensamblaron en cadena y la copia de trabajo coincide.
- `python3 precalculo/verifica_todo.py` → **11 verificadores en verde** (`r2_verifica_todo.out`), el de Tailwind compilado y el de la guía del proyecto incluidos.
- Verificador de bloques (`r2_bloques_cap{2..6}.out`; antes y después, mismas cifras): cap. 2, **487/487**; cap. 3, 1084/1084 (HEAD, igual); cap. 4, **762/762**;
  cap. 5, 1199/1212 (HEAD, igual); cap. 6, 415/434 (HEAD, igual). El «Error: write failed» del cap. 3 sale también en HEAD. Ningún código de R ni de Python se tocó.
- Por HTTP (servidor propio en 8764 y HEAD desde `git archive` en 8765; Chrome sin ventana en 9277, 9278 y 9279; todo cerrado al acabar):
  - **Cap. 4, 11 simuladores × 82 estados × 1200, 800 y 375 px** (`r2_resumen.out`): 0 excepciones y 0 `console.error/warn` de la página (solo el 404 del favicon y el aviso de
    `getImageData` del propio arnés); 0 datos no finitos; 0 lienzos sin datos ni en blanco; 0 marcadores cortados; 0 guiones en ejes y lecturas; 0 solapes ni rótulos fuera
    del lienzo; ninguna leyenda de más de dos renglones; ningún `aria-label` que no cambie entre estados; ΔAICc con 9 rótulos en los 27 estados a los tres anchos; área de
    dibujo mínima 134.8 / 135.8 / 138.8 px a 1200 / 800 / 375 (antes 74 / 52 / 55).
  - **Caps. 2–6 a 1200, 800 y 375 px, antes y después** (`r2_compara.out`): solo el 404 del favicon; ningún lienzo sin gráfico nuevo, ningún desborde; **fuera del cap. 4 solo
    cambia la muestra de la leyenda** (caja → raya, caja o punto: 24, 18, 21 y 24 leyendas en los caps. 2, 3, 5 y 6); 0 ejes con otros rótulos, 0 lecturas, 0 `aria-label` y 0 áreas
    distintas. El lienzo «sin gráfico» del cap. 6 y sus solapes ya estaban en HEAD. Ningún eje de rezagos o de horizontes de los caps. 2–6 pierde marcas ni un múltiplo de 12, salvo los
    dos del cap. 4 que se rehicieron aquí (la traza y σ_h: antes se pisaban o se inclinaban; ahora, menos marcas, legibles y con el extremo).
  - Iconos (`r2_iconos.out`): ninguno vacío en los 12 módulos del cap. 4.
- Capturas abiertas y miradas: M3 (β = 0 a 1200, β = 300 a 375), M4 d = 0 a 1200, M6 (0,2,0) a 1200 y 375, M7 exhaustiva paso 42 a 1200 y paso 30 a 375,
  M8 d = 3 a 1200, M9 forma d = 2 a 375, M9 ψ y σ_h a 375 y 800, M10 TRM ∇ a 800, abanico a 375, puente a 375, y el gráfico 1 del quiz a 1200. Varias son de pasadas anteriores
  del arnés o de una herramienta de foto suelta, antes de los dos últimos cambios (el 30 de σ_h a 800 y el texto de tres `aria-label`); el resto se juzgó por las medidas.
  Dos capturas de `r2_revisa.js` salieron en blanco por tiempo (TRM ∇ a 800, y el quiz) con los lienzos pintados según la medida; se repitieron con espera larga
  (`r2_quiz.js`, y el arnés ahora espera 600 ms tras cada cambio y cuenta los píxeles pintados).
- Las cifras nuevas (`r2_cifras.out`, calculadas en R de otra fuente) coinciden con lo que escribe la página: cotas de la traza (1265, 1300; el ∞ en 1305), límite inferior
  del 95 % con d = 2 (−775.67), ΔAICc y barras cortadas por d (4 con d = 2), los valores y la banda de los dos gráficos del quiz (9 de 20 dentro de la banda en el del Nilo; 8 de 26
  fuera en el mensual), media/varianza/ρ̂₁ por d, ψ₀, ψ₁, ψ₂₉ y σ_h.

## 6. Lo que no se pudo comprobar, y lo que queda

- **Girar el teléfono** (el repintado al cruzar 420 px) y **los tooltips** (no se pasó el ratón; la traza ahora tiene cuatro conjuntos de datos y el tooltip lista los que tengan valor en
  ese paso: no se miró). Lo que se fija al crear —los rótulos cortos del M3 en el teléfono— no cambia si el ancho cruza el umbral después.
- Un lector de pantalla real: solo se leyeron los `aria-label` y su texto. Modo oscuro, zoom del navegador, impresión y otros navegadores que Chrome: no.
- **Copias viejas del armazón fuera de la cadena 2 → 6:** `plantilla/plantilla-capitulo.html`, los preparciales, los talleres y la guía del proyecto traen su propia copia de
  `crearGraficoLinea` y siguen dibujando las líneas como cajas. No se tocaron (la plantilla exige regenerar la guía del proyecto; `preparcial-corte-2.html` estaba excluido).
- El rango del eje de los correlogramas del M4 y del M10 sigue siendo de −1 a 1: con 145 px de dibujo el «por poco» del ρ̂₈ de la TRM y el 0.231 del M4 en d = 1 se ven, pero a 1–3 px de la
  banda (la tabla y la lectura dan la cifra). Acercar el eje sería una decisión de diseño de todo el curso.
- No se tocó la retro de la opción a de la pregunta de la ACF del Nilo (el informe citaba «veinte rezagos sin acercarse a cero»; la R1 ya dejó «8 de los 17 rezagos que quedan»):
  el encargo excluía las retros.
- El M9 ψ ganó una leyenda de colores que la especificación no pedía (el naranja y el gris de las barras no se explicaban).
