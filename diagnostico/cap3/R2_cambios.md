# R2 · Registro de cambios · Capítulo 3 «Modelos AR, MA y ARMA» · gráficas y simuladores

Ronda R2 del `PLAN_Mejora_Cap3.md` (tareas T2.1–T2.3; decisión D3). Fecha: 2026-11-21. Un solo redactor.
Especificación: `diagnostico/cap3/graficas.md` (42 problemas, 9 defectos de causa común). Base: `5e082d2`. Sin commit ni push.

**Archivos tocados**

| archivo | qué |
|---|---|
| `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` | armazón, a mano: 5 sustituciones y 2 traslados (§2). Ninguna prosa, ningún dato |
| `ensamblado/cap3/cap3_js.js` | 27 sustituciones: ayudantes nuevos, `simularARMA`, `correlogramaDoble`/`actualizarDoble`, los `pintar()` de diez simuladores, dos `descripcionGrafico` y un color del quiz. Nada de las claves del quiz, de `AUTOEVALUACIONES['parcial2']` ni del simulacro |
| `ensamblado/cap3/cap3_modulos.html` | 8 sustituciones: cuatro frases (M2, M4, M5, M6), un `aria-label`, una etiqueta de panel, dos alturas del M8 y la del panel de los π del M4 |
| `Htmls_Series/capitulo-3-…html` | reensamblado (`ensambla_cap3.py --escribir`); reproducible byte a byte |
| `Htmls_Series/capitulo-{4,5,6}-…html` | reensamblados en cadena; reciben **las mismas 69 líneas** cada uno (md5 del diff idéntico en los tres), todas de la región heredada (§2) |
| `diagnostico/cap3/comprobaciones/r2_*` | guiones y salidas de la ronda |
| `diagnostico/cap3/capturas/r2/` | 244 capturas (git las ignora) |

No se tocó `plantilla/plantilla-capitulo.html` (ningún arreglo lo exigía), ni el orden de los módulos, ni `DATOS_CAP3`,
ni ningún bloque de R o de Python. Ninguna clase nueva de Tailwind (`compila_tailwind.py --comprobar` en verde dentro de
`verifica_todo.py`). Ninguna cita, autor ni año nuevos; nada copiado de `bibliografia/_local/`.

**Guiones** (`diagnostico/cap3/comprobaciones/`)

| guion | salida | qué hace |
|---|---|---|
| `r2_edita.py` | — | reaplica sobre HEAD las 40 sustituciones y los 2 traslados (cada marcador, único); `--comprobar` dice si el árbol coincide. Después hay que reensamblar 3 → 4 → 5 → 6 |
| `r2_cifras.R` | `r2_cifras.out` | las cifras que la ronda hace aparecer: pesos π en la frontera y fuera de ella, el umbral del eje logarítmico, los rezagos del M6 que se asoman, los recuentos de Ljung–Box del M8, los valores que leen los `aria-label` del quiz y los contrastes de color |
| `r2_revisa.js` | `r2_medidas.json`, `r2_revisa.log` | cap. 3 por HTTP (Chrome sin ventana, `diag/chrome.js`): 13 simuladores × 70 estados × 1200, 800 y 375 px, con captura de cada uno |
| `r2_resumen.py` | `r2_resumen.out` | resumen de esas medidas: datos no finitos, series constantes, lienzos vacíos, área mínima, marcas de los ejes de dispersión, `aria-label` que no cambian, guiones en las lecturas |
| `r2_recorrido.js` | `r2_recorrido_{antes,despues}.json` y `.log` | recorrido de humo de los caps. 2–6, todos los módulos, a 1200, 800 y 375 px (copia de `cap2/comprobaciones/v2_recorrido.js`); «antes» es HEAD servido desde `git archive` |
| `r2_compara.py` | `r2_compara.out` | antes frente a después: consola, lienzos sin gráfico, desbordes, el 1, el 12 y el 24 en los ejes de rezagos, solapes; y qué cambia fuera del cap. 3 |
| `r2_marcas.js` | `r2_marcas.out` | `marcasLegibles` de HEAD frente a la nueva en 3850 ejes sintéticos (1..n, de 30 a 900 px, con y sin tope de 12 marcas): ninguno pierde marcas ni un múltiplo de 12, ninguno pasa del tope, y si HEAD no tocaba el eje ahora tampoco |
| — | `r2_bloques_cap{2..6}.out` | el verificador de bloques al cerrar |

Las capturas son `capturas/r2/mN-<simulador>[-<estado>]-{1200,800,375}.png`; las `mN-vistaK-{800,375}.png` son la pantalla
real con la cabecera fija.

---

## 1. Los 42 problemas, uno por fila

Estados: **A** arreglado · **P** en parte · **R1** lo resolvió la ronda R1 · **N** no tocado (con motivo).

| Ficha | Problema | Estado | Qué se hizo, o por qué no | Captura |
|---|---|---|---|---|
| M2 · `panel-ar-teorico` | 1 [Media] rezagos 1 y 2 sin número a 800/375 | **A** | Armazón (§2, fila 1): 800 `1 2 4 6 … 16`; 375 `1 2 4 6 … 16` | `m2-panel-ar-teorico-*-{800,375}` |
| | 2 [Baja] «cae a cero en el rezago p» | **A** | «…cae a cero de golpe después del rezago $p$ —la barra de $p$ es la última distinta de cero—» | `m2-panel-ar-teorico-ar2_real-1200` |
| | 3 [Baja] `aria-label` fijo | **A** | Se reescribe en `pintar()`: proceso, cuántas barras no nulas y las tres primeras | — |
| M2 · `triangulo-ar2` | 1 **[Alta]** lo explosivo sale plano | **A** | `simularARMA` (§3): sin calentamiento si no es estacionario y corte al pasar de ±10⁶. En (2.2, 1.2) se ve la curva despegar en 17 pasos; en (−2.2, −1.2), el zigzag que crece hasta t = 75. La lectura lo dice | `m2-triangulo-ar2-fuera-max-2.2-1.2-*`, `…-fuera-min-…` |
| | 2 [Media] eje φ₁ `−2.4, 0, 2.4` | **A** | `ejeDispersion()`: 1200 `−2.0 … 2.0` de 0.5 en 0.5; 800 y 375 `−2 −1 0 1 2`; φ₂ `−1.0 −0.5 0.0 0.5 1.0` | `m2-triangulo-ar2-{800,375}` |
| | 3 [Media] leyenda de 3 líneas a 375 | **P** | Rótulos cortos («Estacionario», «Debajo: raíces complejas») y muestra pequeña: 2 líneas a 375 y 800 (antes 3 y 2); el panel sube a 300 px en estrecho. Área: 175 px de alto (antes 134) | `m2-triangulo-ar2-375` |
| | 4 [Baja] menos con guion en ejes y lectura | **A** | Ejes con `cifra()`; lecturas, en el armazón (§2, fila 2) | las mismas |
| | 5 [Baja] punto cortado en el borde | **A** | `clip: false` | `…-fuera-max-…` |
| | 6 [Baja] el punto como rectángulo; su color cambia sin explicación | **P** | La leyenda dibuja círculo, raya y caja (`usePointStyle`). El cambio de color sigue sin leyenda: lo dice la lectura («Estacionario: NO») | — |
| M3 · `panel-ma-teorico` | 1 [Media] rezagos 1 y 2 sin número | **A** | Armazón | `m3-panel-ma-teorico-ma2-{800,375}` |
| M3 · `rho1-theta-ma1` | 1 [Media] eje θ `−5, 0, 5` | **A** | 1200: de 1 en 1; 800 y 375: `−5 −3 −1 1 3 5` (el ±1 siempre) | `m3-rho1-theta-ma1-theta1-{800,375}` |
| | 2 [Media] el eje ρ₁ no rotula ±0.5 | **A** | `−0.50 −0.25 0.00 0.25 0.50` a los tres anchos | las mismas |
| | 3 [Baja] círculo cortado con θ = ±5 | **A** | `clip: false` | `…-theta5-375` |
| | 4 [Baja] colores sin leyenda; menos con guion | **P** | El signo, sí. Los colores los sigue explicando solo la intro | — |
| M4 · `dualidad-psi-pi` | 1 [Media] «los pesos crecen» con θ = 1 | **A** | Tres casos: invertible; frontera («NO — frontera, \|θ\| = 1», «los pesos no decaen»); \|θ\| > 1 («los pesos crecen»). La nota de debajo añade la frontera. `r2_cifras.out` §1: con θ = ±1, \|πⱼ\| constante | `m4-dualidad-psi-pi-theta1-frontera-*` |
| | 2 [Media] con θ = 2 solo se ve π₁₂ | **A** | Si máx \|πⱼ\| > 20, eje logarítmico con signo, con una línea de rejilla por década y rótulos ±10, ±100, ±1000, ±10 000 (el panel sube a 250 px para que quepan; si no cupieran, se rotula una década sí y otra no): se ven los doce pesos. La leyenda, la lectura y la nota lo dicen | `m4-dualidad-psi-pi-theta2-phi0.95-*` |
| | 3 [Baja] el gris de los ψ sin leyenda | **P** | La lectura dice «(barras oscuras)»; la leyenda sigue con una sola muestra | — |
| M5 · `laboratorio-arma` | 1 **[Alta]** recta en 10⁶ y correlogramas vacíos | **A** | La serie despega y se corta (φ₁ = 1.5: 36 valores; todo al máximo: 21); la ACF y la PACF muestrales se calculan con los valores que hay y la banda con esa n. Si quedaran menos de 18 valores o la varianza no fuera finita, no se dibujan y la lectura lo dice. 0 datos no finitos en 70 estados × 3 anchos | `m5-laboratorio-arma-phi1-1.5-*`, `…-max-todo-*` |
| | 2 [Media] «ACF teórica» dibujada como ceros | **A** | Si no es estacionario, el juego teórico no se dibuja ni sale en la leyenda | `m5-laboratorio-arma-phi1-1.0-*` |
| | 3 [Media] 65–68 px de dibujo a 800/375 | **A** | 240 px en estrecho y leyenda en un renglón («Teórica · Muestral · Banda»): 136 y 139 px | `m5-laboratorio-arma-{800,375}` |
| | 4 [Media] muestral 1.75:1 y de la familia de la banda | **A** | `COLORES_GRAFICO.gris` (3.04:1). La intro dice «barras oscuras» y «barras grises» | las mismas |
| | 5 [Baja] muestra verde con borde rojo; eje sin el 10⁶ | **A** | Se cambia también `backgroundColor`; la recta ya no existe | `…-phi1-1.5-*` |
| M6 · `teorica-vs-muestral` | 1 [Media] lo que se asoma no se distingue | **A** | Las barras muestrales fuera de la banda donde la teórica es cero van en rojo **y con un rombo en la punta** (entrada «Se asoma» en la leyenda), y la lectura las nombra: en el MA(1), los rezagos 6 y 15, como da R. Qué rezagos son nulos lo decide el modelo (ACF de un MA(q) tras q, PACF de un AR(p) tras p; en el ARMA(1,1), ninguno), no el dato redondeado. Con el MA(1) el eje queda fijo en ±0.5, rotulado `−0.50 −0.25 0.00 0.25 0.50` | `m6-teorica-vs-muestral-ma1_pos-*`, `…-arma11-*` |
| | 2 [Media] color y leyenda en dos líneas | **A** | Como M5-3 y M5-4: 146 y 149 px a 800/375 | las mismas |
| | 3 [Baja] «theta = 0.8» en la lectura | **A** | `nombreProceso()`: «MA(1), θ = 0.8» | las mismas |
| M7 · `manchas-identificacion` | 1 [Baja] serie anual con marcas de 3 en 3 | **N** | Pedir pasos de 5 exige una opción nueva en `marcasLegibles` para un solo panel; ahora rotula `1 3 6 9 …` | `m7-manchas-identificacion-375` |
| | 2 [Baja] `-0.634` | **A** | Armazón | — |
| M8 · `diagnostico-residuales` | 1 **[Alta]** 0.0461 a 0.3 px de la recta | **A** | Eje ampliado de 0 a 0.10 con el 0.05 rotulado, puntos en vez de barras (rojos bajo 0.05), triángulos en el borde para lo que pasa de 0.10. El 0.0461 queda a 4.8 px de la recta a 1200 y a 5.8 a 375. La etiqueta del panel dice el eje | `m8-diagnostico-residuales-arma20-*` |
| | 2 [Media] vacío con el AR(1) | **A** | 19 puntos rojos sobre el eje; la lectura, «19 de 19» | `…-arma10-*` |
| | 3 [Media] barras rojas sin explicación | **A** | Ya no cambian de color | `…-arma20-*` |
| | 4 [Media] 58 px a 375; selector cortado | **A** | 98 y 148 px; textos del selector más cortos | `…-arma20-375` |
| | 5 [Baja] eje `0.0, 0.4, 0.8` | **A** | `0.00, 0.05, 0.10` | las mismas |
| M9 · `manchas-transformada` | 1 **[Alta]** «se corta más limpiamente» | **R1** | — | — |
| | 2 [Baja] panel de la serie sin etiqueta | **N** | Acabado; no afecta a la lectura | — |
| M9 · `manchas-impulso` | 1 **[Alta]** los ψ fuera de la envolvente | **R1** | No se tocó | — |
| | 2 [Media] abanico de 65–68 px | **A** | 240 px en estrecho: 115 y 118 px | `m9-manchas-impulso-h6-{800,375}` |
| | 3 [Baja] barra del horizonte del color del techo | **A** | Va en el color oscuro | las mismas |
| | 4 [Baja] ψ del navegador frente a la tabla, cuarta cifra | **N** | Exige pasar los φ sin redondear por `genera_cap3.R`: toca el precálculo, fuera de esta ronda | — |
| M9 · `trm-retornos` | 1 [Baja] 3.03:1 y 81–84 px | **N** | Acabado; 80.8 px es ahora el área mínima del capítulo | — |
| M10 · quiz | 1 [Media] los `aria-label` responden | **A** | Dan las barras en orden y la banda (`describirBarrasQuiz`), no el corte ni el veredicto | — |
| | 2 [Media] el 1 sin número en la P3 | **A** | Armazón: 800 `1 2 4 … 16`; 375 `1 3 6 9 12 15` | `m10-quiz-grafico1-*` |
| | 3 [Baja] P9 en rojo; 82 px a 375 | **P** | Barras en el color de siempre. El alto no: la tarjeta aún no está en el documento cuando se dibuja | `m10-quiz-grafico2-*` |

**Recuento:** 30 arreglados, 5 en parte, 2 que resolvió la R1, 5 no tocados (todos de prioridad baja). De los 5 graves:
3 arreglados aquí y 2 en la R1.

## 2. Armazón (capítulo 2 → 3, 4, 5 y 6)

| # | Cambio | Dónde | Qué mueve en la cadena |
|---|---|---|---|
| 1 | **El rezago 1, siempre.** `marcasLegibles` elige el paso como antes y antepone el 1; quita la marca que se le montaría (la del 2 o la del 3) y, si con el 1 se pasa del tope de marcas del eje (`maxMarcas`, 12 en los gráficos de líneas), la siguiente; nunca un múltiplo de 12. Si del paso elegido no salen dos marcas, no toca el eje, como antes | cap. 2, `marcasLegibles` | Eje a eje, rótulos realmente pintados a 1200/800/375 (`r2_compara.out`, sección final): **ningún eje de rezagos u horizontes de los caps. 2–6 tiene menos rótulos que en HEAD ni pierde el 12, el 24 o el 36**. Ejemplos: 1..24 a 375, `3 6 … 24` → `1 3 6 … 24`; 1..20 a 800, `2 4 … 20` → `1 2 4 … 20`; 1..36 a 1200 con tope (cap. 5, σₕ del M5), `3 6 9 … 36` → `1 6 9 … 36` (12 marcas antes y ahora); 1..36 a 800, `4 8 12 … 36` → `1 4 8 12 … 36`. Solapes de rótulos: los mismos que en HEAD |
| 2 | **Signo menos en las lecturas.** `conSignoMenos()` dentro de `actualizarLectura`: solo el guion que abre una cifra | cap. 2, junto a `actualizarLectura` | Lecturas que cambian: cap. 2, 0 (ya usaba `cifra`); cap. 4, 6; cap. 5, 18; cap. 6, 12. `r2_compara.py` comprueba que en todas la única diferencia es `-` → `−` |
| 3 | `cifra()` y `descripcionCorrelograma()` pasan del JS propio del cap. 2 a la región heredada | cap. 2 (traslado, sin cambiar una letra) | Los caps. 3–6 las reciben. Ningún choque de nombres (`r2b_sintaxis.py`). El cap. 3 las usa para sus `aria-label`; los caps. 4–6 todavía no |

`git diff` de los caps. 4, 5 y 6: 69 líneas cada uno, idénticas, solo estas tres piezas. Ningún `aria-label`, leyenda,
escala ni área de dibujo cambia en los caps. 2, 4, 5 y 6 (`r2_compara.out`).

## 3. Lo propio del capítulo 3 (`cap3_js.js`)

- `simularARMA`: calentamiento solo si el proceso es estacionario; sin tope; corte en el primer valor que pasa de ±10⁶.
  **Las realizaciones estacionarias no cambian** (misma semilla y mismo calentamiento). Cambian las no estacionarias,
  que ahora arrancan de cero; la prosa no cita ninguna cifra de ellas.
- `correlogramaDoble` / `actualizarDoble`: gris para la muestral, leyenda corta, juegos que se ocultan, colores por barra.
- Ayudantes nuevos: `ROJO_GRAFICO`, `UMBRAL_EXPLOSION`, `COLOR_MUESTRAL`, `nombreProceso`, `describirBarras`,
  `describirBarrasQuiz`, `altoEnEstrecho`, `ejeDispersion`, `avisoDeCorte`.
- `aria-label` reescritos en cada `pintar()`: los 21 lienzos que cambian. `r2_resumen.out`: «lienzos cuyo aria-label no
  cambia entre estados: ninguno» a los tres anchos.
- Alturas (`altoEnEstrecho`, bajo 640 px de contenedor): área mínima de los paneles señalados, de 58–68 px a 98–149 px.
  En el escritorio solo cambian el Ljung–Box (180 → 230 px) y la ACF de residuales (180 → 200 px) del M8.

## 4. Frases (punto 4 del encargo)

| módulo | antes | ahora |
|---|---|---|
| M2 | la PACF cae a cero «en el rezago $p$» | «después del rezago $p$ —la barra de $p$ es la última distinta de cero—» |
| M4 (nota) | solo \|θ\| > 1 | añade la frontera (ni crecen ni se desvanecen) y que, cuando el mayor pasa de 20 en valor absoluto, el simulador los dibuja en un eje logarítmico, que deja ver los doce a la vez |
| M4 (lectura) | «los pesos crecen» también con θ = 1 | «los pesos no decaen» en la frontera |
| M5 | «barras sólidas» / «barras claras» | «barras oscuras» / «barras grises» |
| M6 | «alguno se asoma fuera de la banda» | añade «(va en rojo y con un rombo, y la lectura dice en qué rezago)» |
| M8 (etiqueta) | «$p$-valor de Ljung–Box por rezago» | añade «(eje ampliado: de $0$ a $0.10$)» |

Las dos del M9 las corrigió la R1.

## 5. Verificación al cerrar

- `python3 precalculo/verifica_todo.py` → 11 verificadores en verde. `ensambla_cap3.py` → reproducible.
- `r2b_sintaxis.py` limpio en los cinco (atrapó un `varianzaMuestral` repetido durante la ronda: se usa el del armazón).
- `audita_posicion_correcta.py` en verde.
- Verificador de bloques (`r2_bloques_cap{2..6}.out`): cap. 2, 487/487; cap. 3, 557/557; cap. 4, 713/735; cap. 5, 1199/1212; cap. 6, 415/434. Las mismas cifras de referencia: ninguno empeora. `precalculo/serie.csv`, borrado.
- Por HTTP (servidor propio en 8773 y HEAD en 8774, los dos cerrados al acabar; el 8731 no respondía): cap. 3, 70 estados
  × 3 anchos, 0 excepciones y 0 `console.error/warn`, 0 datos no finitos, 0 series constantes, 0 lienzos sin datos,
  0 lecturas con guion. Caps. 2–6 a 1200, 800 y 375: solo el 404 del `favicon.ico`; ningún módulo con desborde;
  el lienzo «sin gráfico» del cap. 6 ya estaba en HEAD.
- Se abrieron 9 capturas (M2 fuera-max, M3 θ = 5 a 375, M4 θ = 2 a 1200 y 800, M5 φ₁ = 1.5 y todo al máximo, M6 MA(1) a
  800, M8 AR(1) a 375 y AR(2) a 1200); el resto se juzgó por las medidas.

## 6. Lo que queda

- **Caps. 4–6:** sus `aria-label` siguen fijos y los dos `descripcionGrafico` del quiz del cap. 4 dan la respuesta
  («barras muy altas en los rezagos 12 y 24», «decaen despacio… sin llegar a cortarse»). Las piezas ya están en el
  armazón; aplicarlas es editar `ensamblado/cap{4,5,6}/`, fuera de esta ronda.
- **Cap. 4, frágil y anterior a esta ronda:** `barrasCompactas` fija el alto de dos paneles según el ancho que mide al
  crearse; con la máquina cargada midió ancho de escritorio en el teléfono (áreas de 84 px en vez de 144). Repetido sin
  carga, igual que HEAD.
- Los cinco no tocados de la tabla (M7-1, M9 transformada-2, M9 impulso-4, M9 TRM, y el alto del gráfico de la P9).
- La leyenda no explica el color del punto del triángulo, de θ y 1/θ, ni el gris de los ψ: lo dice la lectura o la intro.
- Con el eje ampliado del M8, los p-valores sobre 0.10 no se distinguen entre sí en el dibujo (sí en el tooltip): es el
  precio de ver el 0.05.
- Tooltips, teclado, modo oscuro e impresión: no revisados, como en el diagnóstico.

## 7. Tras la verificación independiente (2026-11-21)

| # | Hallazgo | Qué se hizo |
|---|---|---|
| 1 | **[Grave]** M6, ARMA(1,1): la lectura decía «rezagos con PACF teórica nula: 2» (los dos últimos, que el precálculo redondea a 0.0000; valen 4.07e-5 y −2.03e-5) | Los rezagos nulos los decide el modelo: `p.p` y `p.q` del precálculo. ARMA(1,1): «ninguno — esta PACF nunca se corta». `r2_cifras.R` §2 hace la misma cuenta y avisa del redondeo |
| 2 | **[Regresión]** `marcasLegibles`: 1..36 a 1200 con tope de 12 marcas pasaba de `3 6 … 36` a `1 6 12 … 36`; ejes muy estrechos pasaban de no tocarse a «1, 24» | El 1 cuenta para el tope (se quita la marca siguiente, no una de cada dos) y se restaura el «menos de dos marcas: no se toca». Medido eje a eje en los caps. 2–6 y en 3850 ejes sintéticos (`r2_marcas.out`): 0 fallos |
| 2b | (hallado al medir) El panel de Ljung–Box del M8, rehecho como gráfico de puntos, rotulaba menos rezagos que cuando era de barras (19 → 10 a 1200) | Su eje usa la letra y la regla de los correlogramas de barras: los mismos rótulos que en HEAD a los tres anchos |
| 3 | **[Medio]** M6 con MA(1): el eje se quedaba en ±0.6 y la señal dependía solo del rojo | `min`/`max` fijos en ±0.5 con marcas `−0.50 … 0.50`; rombo sobre las barras señaladas y entrada «Se asoma» en la leyenda |
| 4 | **[Leve]** Nota del M4 y eje logarítmico | «en valor absoluto»; se quita «sube a paso constante»; rejilla y rótulos en todas las décadas (±10 … ±10 000) |
| 5 | **[Leve]** Castellano de los `aria-label` | «el único que entra… a 1 paso» / «los 4 que entran… a 4 pasos»; «1 año» / «6 años»; «el envolvente», como el resto del capítulo |
