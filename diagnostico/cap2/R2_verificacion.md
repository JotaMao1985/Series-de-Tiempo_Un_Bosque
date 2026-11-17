# Capítulo 2 · R2 («gráficas») · verificación independiente

Fecha: 2026-11-16. Objeto: los cambios sin commit respecto a `HEAD` (`33dc80f`) en los capítulos 2 a 6. Revisado sin
leer `R2_cambios.md` hasta el final (§5). No se editó ningún archivo del repo fuera de este informe, los guiones `v2_*`
y las capturas.

**Cómo:** Chrome sin ventana por CDP (cliente `diag/chrome.js`), con `Chart.defaults.animation = false`,
`loadModule(n)` y `Runtime.enable` + `Log.enable`. El árbol de trabajo, servido por `:8731` (md5 del cap. 2 idéntico al
del disco); `HEAD`, extraído con `git archive` a una carpeta del scratch y servido en `127.0.0.1:8813` (ya detenido).
Los **5 capítulos × todos sus módulos × 1200, 1024, 800 y 375 px** (375 con `mobile: true`, dsf 2), en las dos
versiones: 400 lienzos × ancho y 360 tablas × ancho por versión. Se compara DOM y medidas (rótulos que Chart.js pinta de
verdad, con `getLabelItems` y `measureText`), no píxeles.

**Guiones** (`diagnostico/cap2/comprobaciones/`): `v2_recorrido.js` (recorrido y medidas; salida
`v2_recorrido_{head,ahora}.json`), `v2_compara.py` → `v2_compara.out`, `v2_doce_perdido.py` → `v2_doce_perdido.out`,
`v2_estados_cap2.js` (estados de los simuladores del cap. 2 y rejilla de φ) → `v2_estados_cap2_1200.json`,
`v2_aria.py` → `v2_aria_1200.out`, `v2_ar1_decaimiento.out`, `v2_quiz.js` → `v2_quiz_ahora.json`, `v2_formulas.js` →
`v2_formulas_cap{2,5,6}.out`, `v2_tablas.js`, `v2_contraste.py` → `v2_contraste.out`, `v2_bloques.sh` →
`v2_bloques_{head,ahora}_*.out`.
**Capturas** (`diagnostico/cap2/capturas/r2v/`): `head/` y `ahora/` (280 cada una: cada simulador, gráfico del quiz y
lienzo suelto, a los cuatro anchos), `estados/`, `quiz/`, `formulas/`, `tablas/` y los pares `par-*.png` (HEAD arriba
o a la izquierda, ahora abajo o a la derecha).

## 1. Problemas

Gravedad: **bloquea publicar** = enseña algo falso o deja contenido inaccesible · **corregir** = regresión visible o
arreglo prometido que no se cumple · **menor** = acabado.

| # | Cap. | Módulo | Ancho | Qué se ve | Evidencia | Gravedad |
|---|---|---|---|---|---|---|
| 1 | 5 | M5 · `airline-pesos` (pesos ψⱼ) | 800, 375 | **Regresión: el eje j deja de rotular el 12 y el 24.** HEAD rotulaba `0, 3, 6, 9, 12 … 33`; ahora `0, 5, 10 … 35`. El simulador se titula «escalón a escalón», su intro habla de «el escalón del rezago 12» y la lectura da ψ₁₂ y σ₁₂/σ₂₄: el escalón queda entre el 10 y el 15 sin número. Causa: el eje se titula `j`, no «Rezago», así que `marcasLegibles()` elige múltiplos de 5. A 1200 y 1024 sí salen (`0, 2, 4 … 26`). El eje σₕ de abajo (h = 1…36) tampoco rotula 12 ni 24 a ningún ancho (en HEAD tampoco). | `capturas/r2v/par-c5-m5-airline-pesos-800.png`; `v2_doce_perdido.out` | **corregir** |
| 2 | 2–6 | tablas | 1024, 800 | **Regresión de aspecto: entre 769 y 1199 px las tablas estrechas dejan de llenar el área.** Con `display:block` (umbral nuevo de 1199 px) la caja sigue a `width:100%` pero las filas se encogen al contenido: la cabecera verde se corta y queda una franja vacía con la sombra de la caja. 22 tablas × ancho nuevas, la mayoría a 1024 px (el ancho de portátil más común): cap. 4 M11 «Modelo», 168 px de filas en una caja de 474 (306 vacíos); cap. 5 M2, las dos tablas a media anchura (≈ 240 px vacíos); cap. 5 M12, cinco tablas; cap. 2 M7 «d / varianza», 139 px vacíos; también las tablas ordenables (`.tabla-ranking`) del cap. 3 M8 y cap. 5 M11. A cambio, los 49 recortes de `<main>` de HEAD desaparecen (0 ahora). | `tablas/par-c2-m7-tabla1-1024.png`, `par-c4-m11-tabla1-1024.png`, `par-c5-m12-tabla3-1024.png`, `par-c3-m8-tabla0-1024.png`; `v2_compara.out` § «tabla que no llena su caja» | **corregir** |
| 3 | 2–6 | tablas anchas | 800, 375 | Las tablas ya se desplazan (ninguna recortada), pero **sin pista**: con barras de desplazamiento superpuestas (macOS, teléfonos) la columna «Veredicto» del M6 sigue fuera de la vista sin que nada lo indique. Las cajas y fórmulas sí llevan sombra. | `tablas/par-c2-m6-tabla1-800.png` (las dos versiones se ven igual) | menor |
| 4 | 3, 4 | cap. 3 M9 `manchas-impulso` (j, años desde el choque; h, años de pronóstico) · cap. 4 M9 `pesos-psi-sigma` (j) | 800, 375 | Los ejes j pierden el 12 y el 24 (HEAD: `0, 2, 4…` o `0, 3, 6…`; ahora `0, 5, 10…`) y el eje h pierde el 1 (ahora `2, 4…` o `5, 10…`). Series anuales o no estacionales: el 12 no significa nada aquí, pero el primer horizonte sí. | `v2_doce_perdido.out`; `v2_compara.out` § «rótulos x cambiados» | menor |
| 5 | 4 | M6 · `explorador-modelos` (ACF de los residuales) | 375 | La leyenda de dos entradas pasa de una línea a dos (26 → 42 px) y el área de dibujo baja de 154 a 138 px. En HEAD cabía en una. | `capturas/r2v/par-c4-m6-375.png` | menor |
| 6 | 2 | M1, M2, M5 (series simuladas) | todos | El título «t» del eje x cuesta unos 21 px: el área baja de 115 a 94 px (M1) y de 135 a 114 (M2, M5), un 16-18 %. En el M1 el eje y del ruido blanco pasa de `−3 … 3` a `−2, 0, 2` a 1200, 1024 y 800 px. | `v2_compara.out` § «área de dibujo más baja», «eje y con muchos menos rótulos» | menor |
| 7 | 5, 6 | cap. 5 M10 `armonicos-K`, M11 `comparativa-particion`; cap. 6 M2 `benchmarks` | 375 (y 800 en cap. 5 M10) | Series de dos o tres años: antes cinco marcas mensuales, ahora solo «1949 · 1950» o «1959 · 1960». Legible, pero no se ubica ningún mes. | `v2_compara.out` líneas 100, 107, 108, 115 | menor |
| 8 | 2–6 | todos los correlogramas | todos | Formato desigual en el eje y: `−1.0, −0.5, 0, 0.5, 1.0` (el 0 sin decimal). | `quiz/ahora-quiz1-375.png`; `v2_quiz_ahora.json` | menor |
| 9 | 3–6 | lecturas de los simuladores | — | `aria-live="polite"` en una lectura que se reescribe entera (`innerHTML`) en cada evento `input` del deslizador: al arrastrar, un lector de pantalla puede encolar muchas lecturas largas. Al **cargar** no anuncia nada (medido: 0 reescrituras de una lectura ya viva durante la carga en los 5 capítulos × 4 anchos). No probado con un lector real. | `v2_recorrido_ahora.json` (`anunciosCarga`) | menor |
| 10 | 4, 5, 6 | gráficos con `scales` propias (cap. 6 M1 `residual-vs-error` y M7 `origen-movil`; cap. 5 M9 `calendario-regresores`; cap. 4 Nilo M1/M9 y TRM M10) | 1024, 800, 375 | **Ya estaba, no lo arregla la ronda:** fechas pisadas (cap. 6 M1 y M7: rótulos montados 21 px a 800 y 375, y 7 px a 1024; «1949-01» fuera del lienzo). No pasan por los ejes por defecto. No es regresión; se anota porque el arreglo de «fechas legibles» no llega a ellos. | `v2_compara.out` § «rótulos x solapados» (todos «ya estaba») | menor |

**Recuento: 0 bloquean publicar · 2 corregir · 8 menores.**

## 2. Lo que se pidió comprobar y se cumple

- **Rezagos 12 y 24 en los correlogramas:** en los 5 capítulos × 4 anchos, el 12 aparece rotulado en **168 de 168**
  correlogramas × ancho que lo tienen, el 24 en **80 de 80** y el 36 en **24 de 24** (en HEAD faltaban 80, 46 y 18).
  Incluida la pregunta 3 del quiz: `4, 8, 12 … 24` a 375 y `3, 6 … 24` a 800 (`quiz/ahora-quiz1-{800,375}.png`).
- **El 0:** ningún eje y de ningún lienzo cruza el 0 sin rotularlo, en ninguna versión de ancho (14 lienzos × ancho
  arreglados respecto a HEAD); la línea del 0 va en `#64748b`.
- **Fechas en el cap. 2:** años redondos sin solapes a los 4 anchos y sin deriva al diferenciar (M7 con d = 0…3:
  `2016 · 2019 · 2022 · 2025` a 800). Ningún solape nuevo de rótulos x en los capítulos 2–6; 21 arreglados.
- **Contraste** (`v2_contraste.out`): banda `#e05a00` 3.73:1, `#FB6400` 3.03:1, `#8795A9` 3.04:1, línea del 0 4.76:1
  sobre el blanco del lienzo (`.grafico-wrapper` y `.quiz-grafico` tienen fondo blanco). Todas las bandas de los
  correlogramas usan `#e05a00`.
- **Tablas a 800 px:** 0 elementos recortados por `<main>` sin contenedor desplazable, a ningún ancho (HEAD: 49
  módulos × ancho con recortes, en 1024 y 800). Las 8 tablas anchas del cap. 2 se desplazan a 800 y 375 (ver #3).
- **Fórmulas a 375 px en el cap. 2:** las ocho partidas (`.formula-partes`) caben sin desplazamiento a 800 y 375
  (`formulas/capitulo-2--m*-375.png`); la tercera condición del ruido blanco y «−1 ≤ ρₖ ≤ 1, ρ₀ = 1» se ven. Las cajas
  y fórmulas que siguen desbordando (cap. 5 M5 y M7, cap. 6 M3, M4, M5, M9) muestran la sombra en el borde
  (`formulas/capitulo-6--m5-definition0-375.png`); las que caben no enseñan sombra. HEAD: 68 cajas o fórmulas
  desbordadas × ancho; ahora 31, todas en los capítulos 5 y 6.
- **`aria-label` dinámicos** (`v2_aria_1200.out`): **70 de 70** correlogramas contrastados con los datos del lienzo
  (barras fuera de la banda, banda, r₁ y r₁₀) en el explorador (7 series), el AR(1) (φ = 0…1.05 con y sin ∇), la
  diferenciación (3 series × d = 0…3) cuadran. Box-Cox: el CV del λ del deslizador y el del mínimo cuadran con la
  lectura en los 6 λ. M6: los cinco porcentajes son los de los datos (3.2, 3.6, 5, 11.2, 17.6).
- **Quiz:** los dos `aria-label` dan las 24 autocorrelaciones con dos decimales y la banda (±0.164 y ±0.139); no
  nombran el proceso ni el pico (el diagnóstico queda para quien lee). Es la misma información que el gráfico.
- **Nota y intro del M5, contra el simulador** (`v2_ar1_decaimiento.out`, rejilla de φ de 0.05 en 0.05 más 0.97, 0.98,
  0.99): «decae cada vez más despacio a medida que φ se acerca a 1» — el primer rezago dentro de la banda va 1, 2, 3,
  4, 6, 7, 8, 9, 12, 21 y ninguno desde φ = 0.98; «con φ = 1 baja casi en línea recta» — R² de una recta sobre los 24
  rezagos, 0.997; «compara r₁₀»: 0.2299 con φ = 0.95 y 0.7693 con φ = 1, en la lectura; nota 3: −0.252 (φ = 0.5) y
  −0.506 (φ = 0) con ∇, −0.044 con φ = 0.95 (dentro de la banda ±0.139: «demasiado pequeña para verse»), con φ = 1.05
  y ∇ r₁ = 0.951 y la lectura dice «primera diferencia de una serie explosiva». Todo cierto en el simulador tal como
  está.
- **Datos intactos:** `verifica_bloques_cap6.py --html` da en HEAD y ahora 226/226, 533/534, 713/735, 1199/1212 y
  415/434; salidas idénticas salvo, en el cap. 3, la cola del «Error: write failed» de R al cerrar la sesión, que
  apareció en la pasada de HEAD y no en la de ahora (transitorio; mismos recuentos y mismas discrepancias).
  `verifica_todo.py`: 11 verificadores en verde. Las leyendas y valores de las rectas de los capítulos 3–6 no
  cambian (ninguna diferencia de textos de leyenda fuera del cap. 2).
- **Reensamblado:** copia de `Htmls_Series`, `ensamblado`, `precalculo` y `plantilla` en el scratch; `ensambla_cap3.py
  --escribir` y `ensambla_cap4|5|6.py`: md5 de los cuatro idénticos a los del árbol. Los diff de los capítulos 3–6
  respecto a HEAD son idénticos entre sí (mismo md5 de las líneas cambiadas).
- **Consola:** ninguna excepción ni `console.error/warn` en los 5 capítulos × 4 anchos × todos los módulos (solo el 404
  de `/favicon.ico` del servidor de pruebas, también en HEAD).

## 3. Los cambios compartidos no pedidos

| Cambio | ¿Rompe o empeora algo? |
|---|---|
| Paleta `#FB6400` / `#8795A9` | No se aprecia diferencia de tono. Convive con intervalos pintados a mano en `rgba(255,102,0,…)` (cap. 4 M9-M10, cap. 5 M7, cap. 6 M7) sin que se note. Nada roto. |
| `.simulador h4` de flex a bloque | Solo mejora: 4 títulos × ancho bajan de alto (cap. 3 M4 a 375: 47 → 24 px; cap. 5 M5 a 375: 95 → 48), ninguno sube. El espacio entre icono y texto es ahora el margen de 0.5rem más el espacio literal del marcado (un poco mayor que antes); no se ve como defecto. |
| Umbral de tablas 768 → 1199 px | Resuelve los recortes, pero produce la regresión #2 (tablas que no llenan el área entre 769 y 1199 px) y deja sin pista el desplazamiento (#3). |
| Sombras en `.formula` y en las cajas | Funcionan: aparecen solo cuando la caja desborda y en el lado donde queda contenido; los colores de `--fondo-caja` coinciden con los fondos de `.definition`, `.note`, `.warning` y `.exercise` en los cinco capítulos (ninguna caja tiene otro fondo ni otra `background-image`). En las cajas la sombra cubre toda la altura, prosa incluida: aceptable. |
| Controles a una columna (`auto-fill` con mínimo de 15rem o 40 %) | 55 simuladores × ancho pasan de 2 a 1 columna a 800 px (controles de 308 px); a 1024 y 1200 siguen en dos. Los simuladores son más altos a 800 (6 deslizadores apilados en cap. 3 M5 y cap. 5 M2), sin nada roto. |

## 4. Lo que no se pudo comprobar

- Un lector de pantalla real (VoiceOver/NVDA): el comportamiento de `aria-live` al arrastrar (#9) y la lectura de «yₜ»,
  «∇²» se juzgan por el DOM.
- Teclado, tooltips, modo oscuro, impresión, Safari y Firefox (`background-attachment: local` y las barras de
  desplazamiento superpuestas se vieron solo en Chrome sin ventana, con `--hide-scrollbars`).
- El escenario de fuentes lentas (M1-P4), no tocado por la ronda.

**Incidencias de esta verificación.** (1) Al detener mi servidor de HEAD con `pkill -f "http.server 8799"` detuve
también un servidor ajeno en `localhost:8799` (pid 32924, que servía este mismo `Htmls_Series`); lo relancé enseguida
con el mismo directorio y `--bind 127.0.0.1` (pid nuevo 76395, responde con el md5 actual). Si era de otra sesión,
conviene que su dueño lo sepa. (2) `verifica_bloques_cap6.py` sobre el cap. 3 dejó `precalculo/serie.csv` sin seguir en
git; lo borré.

## 5. Contraste con `R2_cambios.md` (leído al terminar)

- **Coincide** en lo comprobable: recuentos del verificador de bloques, reensamblado idéntico, `verifica_todo` en
  verde, 0 correlogramas sin 12/24, 0 ejes sin el 0, 0 recortes de `<main>`, consola limpia, cifras del simulador del
  M5 (0.2299/0.7693; 0.501 y 0.642 con φ = 0.98 y 0.99), `aria-label` del quiz con datos y no con el diagnóstico.
- **No lo declara:** la pérdida del 12 y el 24 en los ejes j de los pesos ψ (#1, #4). El redactor dice que en los
  capítulos 3–6 «cambian marcas de eje» y mide solo los correlogramas; el del cap. 5 M5 es el único de ellos en el que el
  12 es el contenido del gráfico, y antes salía rotulado a 800 y 375.
- **Lo declara con menos peso:** las tablas que no llenan el área (#2) aparecen como «efecto lateral … como ya se veía
  en el teléfono» (§5.1). Medido, son 22 tablas × ancho nuevas, casi todas a 1024 px, con hasta 306 px vacíos; lo
  califico de *corregir*, no de efecto lateral aceptable.
- **Discrepa en un detalle:** «Siguen pasando a dos líneas las leyendas de dos entradas a 375 px» (§2, fila 5). La del
  cap. 4 M6 no seguía: en HEAD cabía en una línea y ahora pasa a dos (#5).
- **Coincide** en lo que deja abierto: tablas sin pista (#3), gráficos con `scales` propias sin las marcas nuevas (#10),
  plantilla y motores de otros documentos sin el cambio, fuentes lentas.
- El redactor no midió 1024 px en su pasada con capturas («1024 y 900 sin capturas»); es justo el ancho donde aparece #2.
