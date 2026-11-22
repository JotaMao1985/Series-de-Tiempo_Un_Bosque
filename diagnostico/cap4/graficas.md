# Capítulo 4 · revisión de gráficas y simuladores (dibujados)

Archivo: `Htmls_Series/capitulo-4-modelos-arima.html` (commit `71c42d8`, worktree `course-content-improvement-227f2c`,
árbol limpio salvo `diagnostico/cap4/`). Se levantó `python3 -m http.server 8762 --bind 127.0.0.1 --directory Htmls_Series`
y se comprobó que entregaba el mismo archivo (md5 `07cb16b363791f74f7fb696e762556b3` en disco y por HTTP); se cerró al
terminar. Revisado el 2026-11-22 con Chrome sin ventana por CDP (puerto de depuración 9275, perfil temporal), con el
cliente `chrome.js` copiado del cap. 3. No se tocó el capítulo.

- **Qué se miró**: los 11 simuladores con lienzo (`data-simulador`; el duodécimo, `cap4-simulacro` del M11, no tiene
  gráficos: solo se midió que no desborde) con sus **18 lienzos**, más los **2 gráficos del quiz** del M10
  (`AUTOEVALUACIONES['cap4']`, `tipo:'grafico'`, preguntas sobre el puente estacional y la ACF cruda del Nilo). M2, M5 y
  M12 no tienen gráficos. `TABLAS_RANKING['rejilla-nilo']` es una tabla, no se dibuja: fuera de esta lente.
- **Anchos**: **1200 px** (lienzo 666 px), **800 px** (lienzo 282 px) y **375 px** (`mobile:true`, dsf 2; lienzo 236 px).
- **Estados** (por defecto y extremos de cada control): Nilo y diferencia d = 0, 1, 2; escalón |β| = 0, 5, 100, 150,
  245, 250, 300; identificación d = 0, 1, 2; explorador **los 27 (p, d, q)** medidos (10 capturados: 000, 111, 011, 101,
  020, 122, 222, 202, 212, 021); traza paso 1, 9, 18, exhaustiva con paso 18, 1, 21, 42 y vuelta a la escalonada;
  sobrediferenciación d = 0…3; forma del pronóstico los 4 modelos, sin bandas con d = 2 y d = 0; pesos ψ h = 1, 2, 15,
  30; TRM niveles y ∇; abanico h = 1, 12, 24, 36; puente no estacional y airline.
- **Cómo**: el método del cap. 3 (`Chart.defaults.animation = false`, `loadModule(n)`, `Runtime/Log.enable`, captura por
  elemento con la cabecera fija desactivada; las `mN-vistaK-800/375.png` son la pantalla real). Medidas nuevas respecto
  del cap. 3: marcadores recortados por el borde del área en **cualquier** gráfico (no solo dispersión), rótulos con
  guion en vez de signo menos, y un contraste de los datos incrustados (`DATOS_CAP4`, `SERIES_CAP4`) con lo que afirman la
  prosa, las lecturas y las descripciones del quiz (`graficas_datos.py`). Iconos de Font Awesome que no se dibujan:
  `graficas_iconos.js`.
- **Consola**: ninguna excepción ni `console.error/warn` en 12 módulos × 3 anchos × todos los estados. Solo el 404 de
  `/favicon.ico` del servidor de pruebas. Fuentes Montserrat y Fira Code cargadas en todos los ejes. Ninguna fórmula ni
  tabla desborda sin contenedor desplazable; `docSw` = ancho de la ventana en los tres anchos.
- **Recuento**: 44 problemas: **2 Altas, 10 Medias, 32 Bajas**; 7 defectos de causa común al final.
- **Gravedad** (la de los caps. 2 y 3): **Alta** = oculta contenido o hace que el gráfico diga otra cosa que la prosa o
  la lectura; **Media** = cuesta leerlo o deja fuera a alguien (lector de pantalla, teléfono, 800 px); **Baja** = acabado.

Guiones y datos en `diagnostico/cap4/diag/`: `chrome.js` (cliente CDP), `graficas_revisa.js` (recorrido, adaptado de
`cap3/diag/graficas_revisa.js`), `graficas_resumen.py` → `graficas_resumen.out` (todo, por estado),
`graficas_tabla.py` → `graficas_tabla.out` (un renglón por lienzo y ancho), `graficas_datos.py` → `graficas_datos.out`
(datos frente a prosa), `graficas_iconos.js` → `graficas_iconos.out`; medidas crudas en `graficas_medidas.json`.
Capturas en `diagnostico/cap4/capturas/` (258 PNG; abreviado `…/` abajo).

Líneas: «HTML l.» es el capítulo final; «fuente» es `ensamblado/cap4/chapter.js` (JS; fuente = HTML − 7750 en la zona
de simuladores) o `ensamblado/cap4/templates_*.html` (lienzos e intros), que es donde hay que corregir: el capítulo se
reensambla. El armazón común (ayudantes de Chart.js, HTML l. 6355–7110) viene de la cadena 2 → 6.

**Lo que funciona**: todas las cifras de las lecturas coinciden con los datos incrustados y con las de la prosa
(media, varianza y ρ̂₁ del M1; 4.5 % y 70.8 % del M3; 11/1, 2/4 y 2/7 barras fuera de banda del M4; los 4 modelos a
menos de 2 puntos, los 8 rojos de Ljung–Box y las raíces 1.161 / 1.144 / 1.000–1.048 del M6; 18 y 42 pasos del M7;
θ̂ = −1 en d = 2 y 3 del M8; anchos 561 → 677 … 613 → 2771 del M9; σ₃₀ = 199.4 frente a 778.0; 0.964, una barra
(ρ̂₈ = −0.190) y el abanico de la tabla en el M10; ρ̂₁₂ y ρ̂₂₄ del puente). Ningún dato NaN ni fuera del eje. Los
correlogramas hechos con `crearGraficoBarras` rotulan el 1 y el 12 (y el 24 en el puente) a los tres anchos, con el 0
oscuro y la banda como raya discontinua en la leyenda. El ΔAICc del M6 se tumba bien por debajo de 420 px. El escalón
del M3 cae en 1899 (posición 29). Ningún TECHO de la traza deja fuera un AICc finito (máximo 1298.77 < 1302).

---

## M1 · `nilo-y-diferencia` — canvas HTML l. 2877 (fuente `templates_1_3.html` l. 129) · JS HTML l. 7936 (fuente l. 186)

- **Pretende**: «su nivel parece caer de golpe hacia 1899»; con d la media cae a casi cero, la varianza apenas baja con
  d = 1 y casi se triplica con d = 2; ρ̂₁ cambia de signo y queda por debajo de −0.5.
- **Se ve**: lo que dice, con las cifras de la intro en la lectura (28 637.95 → 28 268.34 → 80 055.01; −0.6264).
- **Problemas**
  1. **[Baja]** Eje x con años sin redondear (`1873, 1882, 1891…` en d = 2; `1872, 1881…` en d = 1) y, a 800 px, seis
     pares de rótulos a menos de 3 px (`1871|1883` 2.8 px, `1883|1895` 1.6 px…). Común A.
  2. **[Baja]** Eje y de las diferencias con guion (`-400`, `-800`) y sin la línea del 0 oscura. Común A.
  3. **[Baja]** `aria-label` fijo («…en el nivel de diferenciación seleccionado»): no dice qué d ni qué se ve. Común B.
- Capturas: `…/m1-nilo-y-diferencia-{d0,d1,d2}-{1200,800,375}.png`

## M3 · `escalon-vs-raiz` — canvas HTML l. 3332, 3336 (fuente `templates_1_3.html` l. 584, 588) · JS HTML l. 7977 (fuente l. 227)

- **Pretende**: «Empieza en |β| = 0: KPSS rechaza cerca del 5 % nominal… busca dónde cruza la curva el 50 %; la línea
  vertical marca… 247.8»; con |β| = 100, 70.8 %.
- **Se ve**: la curva de ℓ = 4 cruza el 50 % hacia β ≈ 77, la vertical del Nilo en 247.8, el marcador sobre la curva y
  las cifras en la lectura (4.5 %, 70.8 %, 100 %).
- **Problemas**
  1. **[Media]** **A 1200 px el área de la tasa mide 94 px de alto** (marco de 200 px, `ALTOS_CURVA.ancho`, HTML l. 8008 /
     fuente l. 258, menos leyenda y eje): la recta del 5 % nominal queda a **4.7 px** del 0 y no se distingue del eje,
     justo donde la intro manda empezar. A 375 px el área mide 151 px (marco de 280 px): el teléfono lo ve mejor que el
     escritorio. Común D. `…/m3-escalon-vs-raiz-beta0-1200.png`
  2. **[Baja]** El marcador «β elegido» (radio 6) sale **recortado** por el borde en los extremos: en β = 0 (esquina
     inferior izquierda) y en β ≥ 200 (borde superior, 100 %), a los tres anchos (17 casos en `graficas_resumen.out`).
     Común E. `…/m3-escalon-vs-raiz-beta300-1200.png`
  3. **[Baja]** La leyenda dibuja las rectas como cajas: «Nivel nominal 5 %» y «Nilo (247.8)» son rectángulos grises
     punteados y «β elegido» una caja negra; a 375 px ocupa 3 líneas (58 px). Común C.
  4. **[Baja]** Eje x de la realización a 375 px: `1871 1886 1901…` sin aire; eje y de la serie sin la línea del 0 (no
     la necesita) pero con escalas de `escalasLinea`. Común A.
  5. **[Baja]** `aria-label` fijos: la tasa no anuncia el β ni el porcentaje. Común B.

## M4 · `identificacion-nilo` — canvas HTML l. 3579, 3583, 3587 (fuente `templates_4_6.html` l. 44, 48, 52) · JS HTML l. 8106 (fuente l. 356)

- **Pretende**: en d = 0 la ACF decae despacio y la PACF solo saca el rezago 1; en d = 1 la ACF corta en 1 y el rezago
  8 (0.231) se sale por poco; en d = 2, ρ̂₁ = −0.626.
- **Se ve**: los datos lo confirman (d = 0: ACF fuera en 1–8 y 11–13, PACF solo en 1; d = 1: ACF fuera en 1 y 8).
- **Problemas**
  1. **[Media]** **A 1200 px la ACF y la PACF tienen un área de 75 px de alto** (marco de 180 px, `ALTOS_BARRAS.ancho`,
     HTML l. 8115 / fuente l. 365). Con la banda en ±0.196, las barras de d = 0 entre 0.21 y 0.24 (rezagos 4–7, 11–13)
     se separan de ella **1–2 px**: el «ACF fuera de banda 11 de 20» de la lectura no se puede comprobar en el dibujo, y
     el 0.231 del rezago 8 en d = 1 tampoco. A 375 px el área mide 144 px. Común D.
     `…/m4-identificacion-nilo-d0-1200.png`
  2. **[Baja]** El `<h4>` empieza con un hueco: `fa-magnifying-glass-chart` no existe en Font Awesome 6.0.0 (HTML l. 3565,
     fuente `templates_4_6.html` l. 30). Común G.
  3. **[Baja]** La serie: años sin redondear y, a 375 px, tres pares de rótulos a < 3 px; eje y con guion. Común A.
  4. **[Baja]** `aria-label` fijos («Función de autocorrelación de la serie seleccionada»): no dicen qué d ni cuántas
     barras salen; `descripcionCorrelograma()` (HTML l. 7100) existe y no se usa. Común B.

## M6 · `explorador-modelos` — canvas HTML l. 3966, 3970 (fuente `templates_4_6.html` l. 426, 430) · JS HTML l. 8163 (fuente l. 413)

- **Pretende**: «el segundo gráfico, donde el modelo elegido sale resaltado» compara con el mejor de su d; en d = 1,
  cuatro modelos a menos de 2 puntos; las barras de la ACF se vuelven rojas cuando Ljung–Box rechaza (ocho modelos).
- **Se ve**: los 27 estados sin errores; las cifras de la intro coinciden con los datos; el ΔAICc tumbado a 800 y
  375 px rotula los nueve modelos.
- **Problemas**
  1. **[Alta]** **A 1200 px el ΔAICc rotula solo 5 de sus 9 barras** (Chart.js se salta una de cada dos): en d = 1
     faltan `(0,1,1)`, `(1,1,0)`, `(1,1,2)` y `(2,1,1)`; en d = 2 faltan `(0,2,1)`, `(1,2,0) ↑74`, `(2,2,1)` y
     **`(1,2,2)`, el mejor de su d** —la barra de 3 px—. No se puede saber qué barra es qué modelo, y desaparece el
     rótulo `↑74` de una barra recortada. El código ya tumba el gráfico por debajo de 420 px para evitarlo (HTML
     l. 8215–8231 / fuente l. 465–481); por encima no lleva `autoSkip: false`. `…/m6-explorador-modelos-pdq020-1200.png`
  2. **[Baja]** La muestra de la leyenda «ΔAICc sobre el mejor de d» toma el color de la primera barra: naranja si el
     elegido es (0, d, 0), gris en los demás; no explica naranja = elegido, verde = mejor. Común F.
  3. **[Baja]** La barra del mejor (Δ = 0) es una raya de 3 px (`minBarLength`) verde casi negra, pegada al eje.
  4. **[Baja]** El `aria-label` del segundo lienzo dice «AICc de los nueve modelos» (es ΔAICc) y no cambia con d. Común B.

## M7 · `traza-auto-arima` — canvas HTML l. 4154 (fuente `templates_7_9.html` l. 68) · JS HTML l. 8287 (fuente l. 537)

- **Pretende**: «La línea verde marca el mejor AICc… los puntos naranjas son los modelos que lo mejoraron, y los
  descartados (AICc = ∞) aparecen como marcas en el borde superior».
- **Se ve**: la escalera verde y los puntos de mejora en naranja, con las cifras de la lista y la lectura.
- **Problemas**
  1. **[Media]** **Las cruces de AICc = ∞ salen cortadas por la mitad**: se dibujan en y = `TECHO` = 1302, que es el
     máximo del eje (HTML l. 8302, 8333, 8341 / fuente l. 552, 583, 591), y el recorte del área se come la mitad de
     arriba: se ven como «^», en los pasos 1 y 18 de la escalonada y 21, 27–30 de la exhaustiva, a los tres anchos (18
     registros en `graficas_resumen.out`). La leyenda las anuncia con un cuadrado rojo, no con una cruz. Común E.
     `…/m7-traza-auto-arima-exh-paso42-1200.png`
  2. **[Media]** **La muestra de la leyenda «AICc del modelo evaluado» cambia de color con el modo**: verde oscuro en la
     escalonada y **naranja** en la exhaustiva, porque toma el color del primer punto y en la exhaustiva el primero es
     una mejora (HTML l. 8320 / fuente l. 570). En la exhaustiva la leyenda dice que el naranja es «el modelo evaluado»
     y la intro que es una mejora; 33 de los 37 puntos finitos son verdes. Común F.
  3. **[Media]** A 800 y 375 px la leyenda ocupa **3 líneas (73 px)** y el área queda en **78–81 px** de alto para el
     rango 1260–1302. Común D.
  4. **[Baja]** Eje x con los rótulos inclinados 45° (la escala propia no lleva `maxRotation: 0`); eje y que salta de
     1295 a 1302 (paso irregular); el primer y el último punto quedan medio cortados en los bordes laterales.
- Capturas: `…/m7-traza-auto-arima-{paso1,paso9,paso18,exh-paso1,exh-paso21,exh-paso42}-{1200,800,375}.png`

## M8 · `sobrediferenciacion` — canvas HTML l. 4346, 4350 (fuente `templates_7_9.html` l. 260, 264) · JS HTML l. 8392 (fuente l. 642)

- **Pretende**: «En d = 2 y d = 3 el θ̂ se clava en −1 y |raíz MA| = 1».
- **Se ve**: la lectura lo da (θ̂ = −1.0000, ⚠ raíz unitaria); la barra elegida en naranja sobre eje logarítmico.
- **Problemas**
  1. **[Baja]** Eje logarítmico rotulado solo con **10 000, 100 000 y 200 000**: el `callback` pide también 20 000 y
     50 000, pero Chart.js no genera esas marcas, así que las barras de d = 0 y d = 1 (≈ 28 000) caen en una zona de
     rejillas sin número (HTML l. 8419–8423 / fuente l. 669–673). `…/m8-sobrediferenciacion-d3-1200.png`
  2. **[Baja]** La serie: años sin redondear, guion en `-1500`, a 375 px tres pares de rótulos a < 3 px. Común A.
  3. **[Baja]** `aria-label` fijos. Común B.

## M9 · `forma-pronostico` — canvas HTML l. 4568 (fuente `templates_7_9.html` l. 482) · JS HTML l. 8454 (fuente l. 704)

- **Pretende**: la tabla de debajo (HTML l. 4581, fuente `templates_7_9.html` l. 495): ARIMA(1,1,1) sin constante,
  «**Constante** en el último nivel»; ARIMA(1,2,1) «recta también… intervalo enorme».
- **Se ve**: las cuatro formas; anchos y pendientes de la lectura iguales a la tabla.
- **Problemas**
  1. **[Alta]** **El pronóstico sin constante no se queda en el último nivel**: el último caudal observado (1970) es
     **740** y la línea naranja salta a **816.18** en 1971 y sube hasta **842.17**; se aplana, pero ~100 unidades por
     encima del último nivel, y el enganche al último observado (HTML l. 8504) lo hace muy visible. El dibujo contradice
     la fila de la tabla (se refiere al nivel filtrado, no al observado, y la prosa no lo dice).
     `…/m9-forma-pronostico-d1-1200.png`
  2. **[Media]** A 375 px la leyenda ocupa **4 líneas (98 px)** de un lienzo de 257 y el área queda en 132 px; a 800,
     2 líneas. «Pronóstico» aparece como caja gris de borde naranja. Comunes C y D.
  3. **[Baja]** Con d = 2 la banda del 95 % baja a **−776** (caudal negativo) y el eje y llega a −1000 (`-500`, `-1000`
     con guion): la serie observada queda comprimida en un tercio del alto, y la prosa no comenta el caudal negativo.
  4. **[Baja]** Eje x a 375 px: seis pares de rótulos a < 3 px (`1890|1909` 0.8 px). Común A.

## M9 · `pesos-psi-sigma` — canvas HTML l. 4645, 4649 (fuente `templates_7_9.html` l. 559, 563) · JS HTML l. 8558 (fuente l. 808)

- **Pretende**: «en naranja, los ψ₀…ψ_{h−1}… Mueve el horizonte: el marcador recorre las dos curvas y la lectura da
  cuánto se separan».
- **Se ve**: lo dicho; en h = 30, σ_h = 199.363 frente a 778.013, como la prosa.
- **Problemas**
  1. **[Media]** El gráfico de σ_h tiene un área de **74 px** a 1200, **52 px** a 800 y **55 px** a 375 (marco fijo de
     180 px y leyenda de 2 líneas): la curva naranja casi plana que hay que comparar con la discontinua ocupa una
     franja de unos 20 px. Común D. `…/m9-pesos-psi-sigma-h30-800.png`
  2. **[Baja]** Los marcadores de h = 1 y h = 30 salen cortados por los bordes izquierdo y derecho. Común E.
  3. **[Baja]** El eje de los ψ llega a **1.5** con datos ≤ 1 (`min/max` de `crearGraficoBarras` son *suggested*,
     HTML l. 8576 / fuente l. 826): un tercio del área vacío.
  4. **[Baja]** Eje x de σ_h: `1, 4, 7 … 28`, sin el 30 que es el máximo del deslizador (escala propia sin
     `marcasLegibles`). Común A.
  5. **[Baja]** El `<h4>` empieza con un hueco: `fa-arrows-left-right-to-line` no existe en Font Awesome 6.0.0 (HTML
     l. 4635, fuente `templates_7_9.html` l. 549). Común G.

## M10 · `trm-identificacion` — canvas HTML l. 4974, 4978 (fuente `templates_10.html` l. 136, 140) · JS HTML l. 8651 (fuente l. 901)

- **Pretende**: ACF en niveles que «arranca en 0.964 y decae lentísimo»; tras diferenciar «solo una barra de veinte se
  sale, y por poco: ρ̂₈ = −0.190 frente a ±0.167».
- **Se ve**: los datos lo confirman (20 de 20 fuera; en ∇, solo el 8).
- **Problemas**
  1. **[Media]** A 1200 px la ACF tiene un área de **75 px** (marco de 180 px sin `barrasCompactas`): el «por poco»
     de ρ̂₈ son **~1 px** entre la barra y la banda. Común D.
  2. **[Baja]** Eje x con la fecha cruda `AAAA-MM` en meses sueltos: `2015-02, 2016-02…` con ∇; a 800 px
     `2015-01, 2017-05, 2019-09, 2022-01, 2024-05` (solape de 1.9 px); a 375, `2017-12, 2020-11, 2023-10`. El armazón
     sabe rotular eneros con el año y no se usa. Común A.
  3. **[Baja]** Eje y de ∇TRM con guion (`-400`) y sin la línea del 0. Común A.
  4. **[Baja]** `aria-label` fijos. Común B.

## M10 · `trm-abanico` — canvas HTML l. 5114 (fuente `templates_10.html` l. 276) · JS HTML l. 8710 (fuente l. 960)

- **Pretende**: recta horizontal y un abanico que se abre como √h, sin techo; lectura con el intervalo de la tabla.
- **Se ve**: lo dicho; h = 24 da [2330.70, 4663.48] como la tabla.
- **Problemas**
  1. **[Media]** A 375 px la leyenda ocupa **4 líneas (98 px)** y el área queda en **112 px**. Comunes C y D.
     `…/m10-trm-abanico-h36-375.png`
  2. **[Baja]** Eje x `AAAA-MM` irregular (`2022-07, 2023-03, 2023-11…` a 1200; tres solapes a 375). Común A.
  3. **[Baja]** `aria-label` fijo: no dice el horizonte. Común B.

## M10 · `puente-estacional` — canvas HTML l. 5396 (fuente `templates_10.html` l. 558) · JS HTML l. 8805 (fuente l. 1055)

- **Pretende**: «Fíjate en los rezagos 12 y 24»; ρ̂₁₂ = 0.7245, ρ̂₂₄ = 0.6727.
- **Se ve**: el 12 y el 24 rotulados y destacados a los tres anchos; el airline deja una sola barra fuera (rezago 23).
- **Problemas**
  1. **[Baja]** `aria-label` fijo: no nombra el modelo ni el veredicto. Común B.
  2. **[Baja]** A 800 y 375 px la leyenda (rótulo largo «ACF residual · ARIMA(0,1,1)(0,1,1)[12]») pasa a 2 líneas y el
     área baja a 95–98 px.

## M10 · gráficos del quiz (`AUTOEVALUACIONES['cap4']`) — HTML l. 8927–8939 y 9006–9015 (fuente l. 1177–1189, 1256–1265)

- **Problemas**
  1. **[Media]** Pregunta de la ACF «sin diferenciar» (la del Nilo): `descripcionGrafico` dice «decaen despacio desde 0.50
     **sin llegar a cortarse en veinte rezagos**» y la retro de la opción a, «esta lleva veinte rezagos sin acercarse a
     cero». El dibujo muestra **9 de 20 barras dentro de la banda** (rezagos 9 y 10 —ρ̂₁₀ = 0.090— y del 14 al 20). La
     conclusión (no estacionariedad) se sostiene; la descripción del dibujo, no del todo.
     `…/m10-quiz-grafico2-1200.png`
  2. **[Baja]** Pregunta del correlograma mensual: la descripción dice «pequeñas en el resto», pero los rezagos 2, 5
     (−0.288), 7, 14, 19 y 26 también salen de la banda ±0.163.
  3. **[Baja]** A 375 px los dos gráficos (alto fijo de 200 px) quedan con un área de **82 px**; el del puente con la
     leyenda en 2 líneas.

## M11 · `cap4-simulacro` y M12

Sin lienzos. Nada desborda a ningún ancho.

---

## Causas comunes

- **A. `escalasLinea()` reemplaza los ejes del armazón** (HTML l. 7880 / fuente l. 130). `crearGraficoLinea` fusiona
  `scales` con `Object.assign` superficial (el propio armazón lo advierte, HTML l. 6664–6667), y `escalasLinea` no
  reinstala `marcasLegibles`/`rotuloLegible` (x) ni `marcasVerticales`/`rotuloVertical`/`rejillaConCero` (y). De ahí,
  en las 7 series de línea (M1, M3, M4, M8, M9 forma, M10 ×2): años sin redondear y solapes a 800/375, fechas `AAAA-MM`
  crudas en la TRM, guion en lugar de signo menos y el 0 sin la línea oscura. Las escalas escritas a mano (traza, σ_h,
  tasa KPSS) tienen el mismo efecto. Arreglarlo es del cap. 4 (fuente), no del armazón.
- **B. Ningún `aria-label` cambia con el estado.** Los 18 lienzos de los simuladores llevan una descripción fija del
  HTML; el armazón trae `descripcionCorrelograma()` (HTML l. 7100) y el cap. 4 no la llama.
- **C. La leyenda de `crearGraficoLinea` dibuja las líneas como cajas** (HTML l. 6676): bandas, rectas de referencia y
  la recta del pronóstico salen como rectángulos; el arreglo del cap. 3 (`etiquetasDeLeyendaBarras`, HTML l. 6825)
  solo cubre los gráficos de barras. Viene del armazón: lo hereda la cadena 2 → 6.
- **D. Marcos de altura fija pensados para el teléfono**: `compactar()` (HTML l. 7909) da más alto al lienzo estrecho
  que al ancho (`ALTOS_*`: 180–200 px «ancho» frente a 240–280 px «estrecho»), y los gráficos sin `compactar` tienen
  marcos de 180 px. A 1200 px quedan áreas de 74–94 px (M3, M4 ×2, M9 σ_h y ψ, M10 ACF); a 800/375, leyendas de 3–4
  líneas dejan 52–132 px (M7, M9 ×2, M10 abanico, quiz).
- **E. Marcadores sobre el borde del área se recortan** (`clip` por defecto de Chart.js): β elegido del M3, cruces y
  extremos del M7, h = 1 y h = 30 del M9 (67 registros en `graficas_resumen.out`).
- **F. Leyendas con `backgroundColor` por elemento** toman el color del primero (M6 ΔAICc, M7 traza, M8 varianza):
  la muestra cambia según el estado y no explica el código de colores.
- **G. Font Awesome 6.0.0** (`plantilla/plantilla-capitulo.html` l. 18, y los caps. 2–6): los iconos de 6.1+ quedan
  vacíos; en el cap. 4, dos `<h4>` de simulador.

## Lo que no se midió

- La traza de la exhaustiva paso a paso (se midieron 1, 18, 21 y 42) y el escalón en todos los pasos de 5 (se tomaron 7).
- El comportamiento al girar el teléfono (el repintado del ΔAICc al cruzar 420 px) y los tooltips (no se pasó el ratón).
- Un lector de pantalla real: solo se leyeron `aria-label`, `role` y la región viva común.
- Modo oscuro y zoom del navegador.
