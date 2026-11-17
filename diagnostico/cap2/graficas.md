# Capítulo 2 · revisión de gráficas y simuladores (dibujados)

Archivo: `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (commit `4b71366`, worktree
`course-content-improvement-227f2c`), servido por `http://localhost:8731/` (se comprobó que el servidor entrega el mismo
archivo: md5 idéntico). Revisado el 2026-11-16 con Chrome sin ventana por CDP, sin puppeteer. No se tocó el capítulo.

- **Qué se miró**: los 8 simuladores (`data-simulador`) con sus 18 lienzos, más los 2 gráficos que dibuja el quiz del M9
  (`tipo:'grafico'`): **20 lienzos en 9 fichas**. El M9 no tiene simulador propio.
- **Anchos**: **1200 px** (área de contenido 822 px), **800 px** (la barra lateral se queda y el área baja a **438 px**;
  el simulador mide 358 px y el lienzo 282 px) y **375 px** (`mobile:true`, dsf 2; área 345 px, lienzo 236 px).
- **Estados**: por defecto y en los extremos de cada control. Explorador: las 8 series. AR(1): φ = 0, 0.50, 0.95, 1.00,
  1.05, y φ = 0, 1.00, 1.05 con ∇. Diferenciación: las 3 series × d = 0, 1, 2, 3. Box-Cox: λ = −1, −0.30, 0, 0.50, 1, 2.
  En cada estado se guardó la lectura, la leyenda, las escalas, los rótulos y las rectas de la banda.
- **Cómo**: `Chart.defaults.animation = false`, `loadModule(n)` y espera; `Runtime.enable` + `Log.enable` para excepciones
  y consola; captura por elemento con `clip` y `captureBeyondViewport`, con la cabecera fija y el botón «subir»
  desactivados. Las `mN-vista-800/375.png` son la pantalla real (cabecera incluida).
- **Medidas propias** que no traía el arnés del cap. 1: solape real de los rótulos del eje x (con `getLabelItems()` y
  `measureText`), fuente con la que se pintó cada eje y si estaba cargada (`document.fonts.check`), valor y extensión de
  las rectas de la banda, y **lo que `<main>` (overflow:hidden) recorta sin barra de desplazamiento** — a 800 px
  `scrollWidth` del documento da 800 y no delata nada.
- **Consola**: ninguna excepción ni `console.error/warn` en los 9 módulos × 3 anchos × todos los estados. Solo el 404 de
  `/favicon.ico`, que es del servidor de pruebas.
- **Recuento**: 49 problemas en las fichas y en «Fórmulas y tablas»: **4 Altas, 27 Medias, 18 Bajas**; 11 defectos
  de causa común al final.
- **Gravedad**: **Alta** = oculta contenido o hace que el gráfico diga otra cosa que la prosa; **Media** = cuesta leerlo o
  deja fuera a alguien (lector de pantalla, teléfono, 800 px); **Baja** = acabado.

Guiones y datos en `diagnostico/cap2/diag/`: `chrome.js` (cliente CDP), `revisa.js` (recorrido), `fuentes.js` (prueba de
fuentes), `tabla800.js` (vista real de una tabla recortada), `resumen.py` → `resumen.out`; medidas crudas en
`medidas.json` y `fuentes.json`.
Capturas en `diagnostico/cap2/capturas/` (183 PNG; abreviado `…/capturas/` abajo).

Contraste sobre blanco de la paleta (`COLORES_GRAFICO`, l. 4714): primario `#012820` 15.8:1 · terciario `#0e7490` 5.4:1 ·
**secundario `#FF6600` 2.94:1**, por debajo del 3:1 de WCAG 1.4.11. Aquí el naranja no es una serie de contexto: es **la
banda ±1.96/√T de todos los correlogramas** (rayada, 1.5 px), la caminata del M1, las barras del M6 y el punto del M8.
El gris `#94a3b8` del cap. 1 no se usa en este capítulo.

---

## M1 · `panel-estacionariedad` — canvas l. 2247, 2250, 2253 (JS l. 5544, `serieDe` l. 5527)

- **Pretende**: «solo la primera es estacionaria»; «la caminata aleatoria es literalmente la *suma acumulada* del ruido
  blanco de arriba».
- **Se ve (1200)**: los tres comportamientos sin esfuerzo: ruido alrededor de 0 (−3…3), caminata que deambula
  (−15…10), AirPassengers con tendencia y abanico. Comprobado con los datos incrustados: la caminata es la suma acumulada
  del ruido (diferencia máx. 5·10⁻⁵, el redondeo del JSON). Los `aria-label` describen el rasgo, no solo nombran.
- **Problemas**
  1. **[Media]** A 375 px las fechas de AirPassengers se montan: `1949-011951-06 1953-11 1956-041958-09` (solapes de
     1.3, 2.3 y −1.4 px; marcas cada 29 meses en meses arbitrarios). A 800 px quedan a 3 px.
  2. **[Baja]** El eje de las dos series simuladas rotula `1, 18, 35, 52…` (paso 17, elegido por Chart.js); a 375 px
     `1, 20, 39…` con `134|153` a 2.9 px. Sin título de eje (t) ni unidades (AirPassengers en miles).
  3. **[Baja]** Cada serie tiene su color (verde, naranja, turquesa) y el M3, que dice ser «las mismas tres series»,
     las pinta las tres en verde oscuro. La caminata va en naranja 2.94:1.
  4. **[Baja]** Si Google Fonts tarda más de 3 s, este módulo de arranque se queda con la leyenda en letra con remates
     (Times) hasta cambiar de módulo: `fuentesDeLosLienzos()` (l. 4341) corta a los 3 s y Chart.js no repinta cuando la
     fuente llega (`fuentes.js`, escenario con las fuentes retrasadas 8 s; el lienzo no cambia tras cargar la fuente).
     Con la red normal la fuente ya está cuando se crean los gráficos (`document.fonts.check` = true en los ejes de los
     20 lienzos, a los tres anchos).
- Capturas: `…/capturas/m1-panel-estacionariedad-1200.png`, `…/capturas/m1-panel-estacionariedad-800.png`,
  `…/capturas/m1-panel-estacionariedad-375.png`, `…/capturas/m1-vista-375.png`, `…/capturas/m1-vista-800.png`,
  `…/capturas/m1-fuente-fuentes-lentas-inicial-1200.png` (leyenda con remates) frente a
  `…/capturas/m1-fuente-fuentes-lentas-repintado-1200.png`

## M2 · `ruido-blanco` — canvas l. 2349 (serie), 2352 (ACF) (JS l. 5556)

- **Pretende**: «todas las barras deberían caer dentro de la banda, salvo alguna por puro azar»; la nota: «con T = 200
  la banda vale ± 0.139».
- **Se ve**: la serie y un correlograma con las 24 barras dentro. La banda está bien: ±0.1386 = 1.96/√200, la misma
  cifra en la lectura, en la prosa (0.139) y en el `aria-label` («todas las barras dentro de la banda»: 24 de 24).
- **Problemas**
  1. **[Media]** **El correlograma no tiene el 0 en el eje**: con 250 px de alto Chart.js elige paso 0.4 y rotula
     `−1.0, −0.6, −0.2, 0.2, 0.6, 1.0`; las barras cuelgan de una línea que no está rotulada ni dibujada. Es el único
     correlograma con esa altura; los de 200-230 px sí sacan el 0.
  2. **[Media]** Con la escala fija en ±1 las barras (máx. |r| = 0.115) miden unos 8 px de alto en escritorio, y a
     375 px 2.9 px de ancho: se ve «todo dentro», pero la prueba visual es diminuta. Es una decisión (la escala fija
     permite comparar con el M3), que convendría tomar a sabiendas.
  3. **[Media]** La lectura numérica no tiene `aria-live` (defecto común 7).
  4. **[Baja]** Eje de la serie `1, 18, 35…`, sin título.
- Capturas: `…/capturas/m2-ruido-blanco-1200.png`, `…/capturas/m2-ruido-blanco-800.png`,
  `…/capturas/m2-ruido-blanco-375.png`, `…/capturas/m2-vista-375.png`

## M3 · `correlogramas-comparados` — canvas l. 2475, 2480, 2485 (JS l. 5574, `correlogramaDe` l. 5515)

- **Pretende**: tres huellas: «sin estructura», «decae muy despacio y casi en línea recta», «decaimiento lento *y*
  ondulación cada 12 rezagos».
- **Se ve (1200)**: las tres huellas; cada correlograma lleva la banda de su propia T (0.1386, 0.1386, 0.1633). Las
  cifras de la tabla de al lado salen de los mismos datos (r₁ = −0.078; 0.961 y r₁₂ = 0.488; r₁₂ = 0.760).
- **Problemas**
  1. **[Media]** **A 800 y 375 px el eje solo rotula impares (`1, 3, 5, …, 23`)**: el 12 y el 24 —los rezagos de la
     «ondulación cada 12» que anuncia la etiqueta— se quedan sin número. Defecto común 1.
  2. **[Media]** La ondulación es tenue: en AirPassengers la ACF solo sube de 0.656 (k = 8) a 0.760 (k = 12) sobre un eje
     de −1 a 1 con 95 px de área: unos 5 px a 1200 y menos a 375. Se ve si se sabe qué buscar.
  3. **[Baja]** Eje y sin título (r_k); la leyenda de cada panel repite «Banda ±1.96/√T · ACF» tres veces.
- Capturas: `…/capturas/m3-correlogramas-comparados-1200.png`, `…/capturas/m3-correlogramas-comparados-800.png`,
  `…/capturas/m3-correlogramas-comparados-375.png`, `…/capturas/m3-vista-375.png`

## M4 · `explorador-acf-pacf` — canvas l. 2675 (serie), 2679 (ACF), 2683 (PACF) (JS l. 5597)

- **Pretende**: «la caminata aleatoria (ACF que no baja, PACF con **un solo** pico) y AirPassengers (ondulación
  estacional en la ACF)»; la prosa siguiente: PACF de la caminata con «un único pico grande en el rezago 1».
- **Se ve**: el selector cambia las tres gráficas y la lectura. **La banda se recalcula bien con la T de cada serie**
  (0.1633, 0.1386, 0.1639 en ∇log, 0.1712 en ∇₁₂∇log, 0.1668 en la TRM, 0.1675 en ∇TRM), en la ACF y en la PACF. La
  PACF de la caminata es, efectivamente, un pico en 1 (0.961); el rezago 4 (−0.140) roza la banda (±0.1386) sin que se
  note.
- **Problemas**
  1. **[Media]** **A 375 px la leyenda del panel de la serie se corta por los dos lados** con los nombres largos:
     «rencia regular y estacional de log(AirPas» (la serie ∇₁₂∇log); y las fechas se montan
     (`1950-021952-051954-081956-111959-02`).
  2. **[Media]** Eje de rezagos en impares a 800/375 px: el 12 y el 24 de la ondulación sin número (común 1).
  3. **[Media]** La lectura «rezagos fuera de la banda: 24 de 24» cuenta **solo la ACF**, en un simulador que enseña dos
     correlogramas con la misma banda; no lo dice.
  4. **[Media]** Los tres `aria-label` son fijos («Serie seleccionada», «Función de autocorrelación de la serie
     seleccionada»): no nombran la serie elegida ni lo que muestra. Lectura sin `aria-live`.
  5. **[Baja]** La intro dice «ACF que no baja»; baja de 0.961 a ≈0.20 en el rezago 24, y el M3 lo dice bien («decae muy
     despacio»).
  6. **[Baja]** En las series diferenciadas las marcas de fecha derivan de mes (`1950-02, 1951-01, 1951-12, 1952-11…`).
- Capturas: `…/capturas/m4-explorador-acf-pacf-1200.png` y un archivo por serie
  (`…-ruido_blanco-`, `…-caminata-`, `…-log_airpassengers-`, `…-d_log_airpassengers-`, `…-dd_log_airpassengers-`,
  `…-trm-`, `…-d_trm-` × `1200/800/375.png`), `…/capturas/m4-vista-375.png`

## M5 · `ar1-phi` — canvas l. 2819 (serie), 2822 (ACF) (JS l. 5644)

- **Pretende** (intro): «Fíjate en el instante en que la ACF deja de decaer: ahí aparece la raíz unitaria». Nota
  siguiente: con φ = 0.5 la ACF «cae a plomo»; «con φ = 0.95 … la ACF baja tan despacio que cuesta distinguirla de una
  raíz unitaria»; con ∇ y φ pequeño, «autocorrelación negativa en el rezago 1».
- **Se ve**: φ = 0.5 cae rápido (r₁ = 0.436); con ∇ y φ = 0, r₁ = −0.506 (lo que anuncia la nota 3); con φ = 1 y ∇,
  r₁ = −0.032: ruido blanco, como pide la pregunta 6 del quiz. La banda pasa a 0.1389 al diferenciar (n = 199): bien.
- **Problemas**
  1. **[Alta]** **El simulador desmiente la nota 2.** Con el ruido fijo del simulador, φ = 0.95 da r₁₀ = 0.230 y barras
     dentro de la banda desde el rezago 12-13; φ = 1 da r₁₀ = 0.769 y las 24 barras muy por fuera. Los dos correlogramas
     son claramente distintos: quien haga lo que la nota propone ve lo contrario de lo que se le dice. (Que la serie
     «parece tener tendencia» sí se ve.) O se cambia la frase, o se dice que con *esta* muestra se distinguen y con otras
     no.
  2. **[Media]** «El instante en que la ACF deja de decaer» no existe en el dibujo: con φ = 1 la ACF baja de 0.975 a
     ≈0.48 en el rezago 24, y con φ = 1.05 también decae. Lo que cambia es la velocidad (lenta y casi recta).
  3. **[Media]** Con φ > 1 el panel de la serie es una exponencial que se va a −20 000 y todo lo demás queda plano; la
     lectura dice `varianza = 16760012.970` (sin separador y con tres decimales), mientras el eje escribe `−20 000`.
  4. **[Media]** A 800 px los controles van en dos columnas de unos 150 px (la regla es por ancho de *ventana*): «Coeficiente
     / φ» se parte y el interruptor «Aplicar primera diferencia ∇» ocupa tres líneas (común 3).
  5. **[Media]** Lectura sin `aria-live`; `aria-label` fijo («…según el valor de phi», en ASCII).
  6. **[Baja]** Leyenda con guion bajo literal: «y_t con φ = 0.70», «∇y_t con φ = …» (el lienzo no pasa por KaTeX).
     El título usa la ϕ de KaTeX y el control la φ de texto.
  7. **[Baja]** «proceso: ∇ de una serie caminata aleatoria (φ = 1): raíz unitaria»: la frase se compone pegando
     cadenas.
  8. **[Baja]** En algunos estados el eje y no rotula el 0 (φ = 0.95: `−7, −5, −3, −1, 1, 3`).
- Capturas: `…/capturas/m5-ar1-phi-1200.png`, `…-phi0-`, `…-phi050-`, `…-phi095-`, `…-phi100-`, `…-phi105-`,
  `…-phi0-dif-`, `…-phi100-dif-`, `…-phi105-dif-` (× `1200/800/375.png`), `…/capturas/m5-vista-800.png`

## M6 · `montecarlo-adf` — canvas l. 3127 (JS l. 5720)

- **Pretende**: «La línea marca el 5 % que debería observarse si la prueba estuviera bien calibrada»; después: «3.2 % de
  rechazos … con amplitud 4 falla 17.6 % de las veces: más del triple».
- **Se ve**: barras crecientes que cruzan la línea en A = 1; las cifras (3.2, 3.6, 5.0, 11.2, 17.6) son las de
  `DATOS_CAP2` y las de la prosa.
- **Problemas**
  1. **[Media]** **Eje x categórico con amplitudes 0, 0.5, 1, 2, 4 equiespaciadas**: el salto de 2 a 4 ocupa lo mismo que
     de 0 a 0.5, y la forma de la subida depende de esa elección. Un eje lineal, o decir que las categorías no están a
     escala.
  2. **[Media]** **A 375 px la leyenda se trunca**: «% de falsos rechazos de la raíz unitar»; y ocupa 54 px.
  3. **[Baja]** Eje y sin título ni «%»: la unidad solo está en la leyenda. «Nivel nominal 5%» frente a «5 %» de la prosa.
  4. **[Baja]** Barras naranja 2.94:1; la línea de referencia, en cambio, va en verde oscuro (aquí el naranja no es la
     banda, al revés que en el resto del capítulo).
  5. **[Baja]** En la intro, «el 5 %» se parte entre «5» y «%» a 800 px (falta espacio duro). `aria-label` genérico: no
     dice que se pasa de 3.2 a 17.6.
- Capturas: `…/capturas/m6-montecarlo-adf-1200.png`, `…/capturas/m6-montecarlo-adf-800.png`,
  `…/capturas/m6-montecarlo-adf-375.png`

## M7 · `diferenciacion` — canvas l. 3385 (serie), 3388 (ACF) (JS l. 5747)

- **Pretende**: «Observa las tres señales a la vez: la forma de la serie, el correlograma y —sobre todo— la varianza»;
  la tabla siguiente da varianza y r₁ por d.
- **Se ve**: las lecturas coinciden con la tabla (log: 0.1949 → 0.01135 → 0.01823 → 0.04691, r₁ 0.954 → 0.200 → −0.293 →
  −0.534; TRM: 338 834 → 14 800 → 26 813 → 75 469, r₁ 0.964 → 0.088 → −0.415 → −0.602). La banda se recalcula con
  n − d (0.1668 → 0.1687 en la TRM). «d de varianza mínima = 1» en las tres series, como `ndiffs`. Con d = 2-3 la ACF
  muestra el r₁ ≈ −0.5 de la sobrediferenciación.
- **Problemas**
  1. **[Media]** **La intro y la lista no hablan de las mismas tres señales**: la intro dice forma de la serie,
     correlograma y varianza; la lista numerada que sigue al simulador dice correlograma, pruebas (`ndiffs`) y varianza.
  2. **[Media]** A 800 px los dos controles van en dos columnas: «Número de diferencias regulares (d)» ocupa cuatro
     líneas y el selector queda estrecho (común 3).
  3. **[Media]** Fechas: a 375 px `2015-01, 2017-12, 2020-11, 2023-10`; a 800 px `2015-01, 2017-05, 2019-09…`; y al
     diferenciar el mes de las marcas se corre (`2015-04, 2016-04…` con d = 3). Común 2.
  4. **[Media]** Lectura sin `aria-live`; `aria-label` fijos («Serie tras aplicar d diferencias regulares»).
  5. **[Baja]** Leyenda «∇^2 de la serie», «∇^3 de la serie» (circunflejo literal) y «Serie original» sin decir cuál
     (ni COP/USD).
  6. **[Baja]** Formato: la lectura escribe `varianza = 338834.24`; la tabla de al lado, `338 834`, y los ejes agrupan.
  7. **[Baja]** El eje y de una serie diferenciada no siempre rotula el 0 (log con d = 1: `−0.25, −0.15, −0.05, 0.05…`;
     caminata con d = 2: `−5, −3, −1, 1, 3`).
- Capturas: `…/capturas/m7-diferenciacion-1200.png` y un archivo por estado (`…-trm-d0…d3-`, `…-log_airpassengers-d0…d3-`,
  `…-caminata-d0…d3-` × `1200/800/375.png`), `…/capturas/m7-vista-800.png`

## M8 · `box-cox` — canvas l. 3600 (serie), 3605 (criterio de Guerrero) (JS l. 5814)

- **Pretende**: «observa cómo la amplitud estacional deja de crecer … el punto naranja marca dónde estás y el mínimo de la
  curva es el λ que elige R»; la nota: 0.530 sin transformar, 0.153 con el logaritmo, 0.081 en el óptimo λ = −0.295; la
  franja del 20 % es [−0.41, −0.17] «y el 0 *no* está dentro».
- **Se ve**: con λ = 0 y λ = −0.30 la amplitud deja de crecer; con λ = −1 se invierte (sobretransforma). La lectura da
  0.53032, 0.15308 y 0.08152/0.08149: las cifras de la nota. El mínimo de la curva está donde dice.
- **Problemas**
  1. **[Media]** **La leyenda llama «λ elegido» al punto del deslizador**, que es «dónde estás»; se lee como el λ que
     elige R, que no está marcado.
  2. **[Media]** **Eje x del criterio sin los λ que importan**: a 1200 px `−1.00, −0.70, −0.40, −0.10, 0.20, 0.50…`; a 375
     px `−1.00, −0.55, −0.10, 0.35…` (y sin el 2.00). Ni el 0 (logaritmo), ni el 1 (sin transformar), ni el óptimo
     aparecen rotulados. A 800 px los rótulos se montan (`−1.00|−0.65|−0.30` a 1.4-2.7 px).
  3. **[Media]** Lo que la nota discute no se ve: sobre un eje 0-1, la distancia entre 0.153 (log) y 0.081 (óptimo) son
     unos 8 px, y no hay marca en λ = 0 ni en la franja [−0.41, −0.17]. Una recta en λ = 0 y otra en λ̂ (o sombrear la
     franja) harían visible el argumento.
  4. **[Media]** A 800 px el deslizador mide unos 140 px para 300 pasos (0.02 por píxel): llegar a 0 o a −0.30 es
     cuestión de suerte; la etiqueta se parte (común 3).
  5. **[Media]** Lectura sin `aria-live`; `aria-label` fijos.
  6. **[Baja]** Con λ = −1 el punto queda medio cortado en el borde izquierdo del área. La lectura escribe «−1.00» con
     guion (`-1.00`) y la prosa con signo menos.
- Capturas: `…/capturas/m8-box-cox-1200.png`, `…-lam-1-`, `…-lam-030-`, `…-lam0-`, `…-lam050-`, `…-lam2-`
  (× `1200/800/375.png`), `…/capturas/m8-vista-800.png`

## M9 · gráficos del quiz (preguntas 3 y 6, `tipo:'grafico'`) — creados por JS (l. 5206; preguntas l. 5933 y 6007)

- **Pretende**: pregunta 3, «Mira *dónde* está la barra grande»: el pico de ∇log en el rezago 12; pregunta 6, la «forma
  del decaimiento» de la caminata.
- **Se ve (1200)**: los dos rasgos; banda de 0.1639 y 0.1386, como dice la retroalimentación («±0.164»).
- **Problemas**
  1. **[Alta]** **Pregunta 3 a 800 y 375 px: el rezago 12 no tiene número** (`1, 3, 5…` y `1, 4, 7, 10, 13…`). La
     pregunta consiste en localizar esa barra; hay que contar barras de 2.5 px. Común 1.
  2. **[Media]** **Los `aria-label` dan la respuesta**: «…con un pico marcado en el rezago 12» y «…decae muy lentamente
     desde valores cercanos a uno». Quien usa lector de pantalla recibe el diagnóstico que la pregunta pide hacer.
  3. **[Baja]** A 375 px el área útil es de 166 × 112 px y las barras de 2.5 px de ancho.
- Capturas: `…/capturas/m9-quiz-grafico1-1200.png`, `…/capturas/m9-quiz-grafico1-800.png`,
  `…/capturas/m9-quiz-grafico1-375.png`, `…/capturas/m9-quiz-grafico2-1200.png`, `…/capturas/m9-quiz-grafico2-375.png`

---

## Fórmulas y tablas (fuera de pantalla)

- **[Alta] Tablas cortadas a 800 px sin forma de verlas.** `table { display:block; overflow-x:auto }` solo se aplica
  con `max-width: 768px` (l. 1096); a 800 px las tablas conservan su ancho y `<main>` (`overflow-hidden`, l. 2126) las
  corta sin barra. Medido (`recortados` en `medidas.json`): M1 condiciones (46 px fuera), M3 patrones del correlograma
  (56 px), **M6 resultados de ADF y KPSS sobre la TRM (118 px: la columna «Veredicto» desaparece entera)**, M6
  combinaciones (29 px: se corta la «Contradicción…»), M6 ADF por rezagos (41 px), M7 varianzas por d (25 px), M9
  conceptos (75 px). `…/capturas/m6-tabla1-vista-800.png` es la pantalla real. A 375 px las mismas tablas se desplazan
  dentro de su caja, sin pista de que hay más.
- **[Alta] La definición de ruido blanco pierde su condición central a 800 y 375 px** (M2, l. 2328-2330; 567 px de
  fórmula en 306 a 800, 496 en 257 a 375): se ve `E[ε_t] = 0, Var(ε_t) = σ²,` y la tercera condición,
  `Cov(ε_t, ε_{t+k}) = 0 para todo k ≠ 0`, queda fuera, en una caja con desplazamiento horizontal y sin pista.
  `…/capturas/m2-formula0-375.png`, `…/capturas/m2-formula0-800.png`.
- **[Media]** Otras siete fórmulas en bloque con el mismo patrón a 800 y 375 px (a 1200 caben todas): M3 γ_k (358/308 px
  a 800), **ρ_k (457/308: se pierde `−1 ≤ ρ_k ≤ 1, ρ_0 = 1`)**, γ̂_k y r_k (398/308); M4 regresión de la PACF (355/306);
  M5 AR(1) con «ε_t ∼ ruido blanco(0, σ²)» (372/308) y caminata con deriva (395/308); M6 regresión del ADF (338/306).
  `…/capturas/m3-formula0…2-375.png`, `…/capturas/m4-formula0-375.png`, `…/capturas/m5-formula0…1-375.png`,
  `…/capturas/m6-formula0-375.png` (y sus `-800`).

## Defectos que comparten causa (arreglo de una sola vez)

1. **Eje de rezagos sin el 12** — `crearGraficoBarras` (l. 4857) deja el autoSkip de Chart.js: en lienzos de menos de unos 600 px
   rotula `1, 3, 5…` o `1, 4, 7…`. Afecta a **los 10 correlogramas** (M2, M3 ×3, M4 ×2, M5, M7 y los 2 del quiz)
   a 800 y 375 px, y es grave en la pregunta 3 y en la «ondulación cada 12» del M3/M4. Arreglo: `autoSkip:false` y un
   `ticks.callback` que muestre 1 y los múltiplos de 6 (o de 12) cuando falte sitio.
2. **Marcas de fecha** — `crearGraficoLinea` (l. 4721) con `maxTicksLimit: 12` y etiquetas `AAAA-MM`: Chart.js elige
   meses arbitrarios, que se montan a 375 px (AirPassengers en M1, M4, M8; series diferenciadas) y derivan de mes al
   diferenciar (M4, M7). Es el defecto 2 del cap. 1, con el mismo ayudante: un `ticks.callback` común que rotule solo
   eneros como «1949» y salte años según el ancho arregla los dos capítulos. Para las series simuladas, un paso redondo
   (`stepSize` 25 o 50) en lugar de `1, 18, 35…`.
3. **Reglas por ancho de ventana en un área que no lo tiene** — a 800 px el área mide 438 px, pero
   `.simulador-controles` pasa a dos columnas con `min-width: 768px` (l. 851) y las tablas solo se vuelven desplazables
   con `max-width: 768px` (l. 1096). Resultado: controles apretados en M5, M7 y M8, y siete tablas cortadas por `<main>`.
   Es la misma causa que el `.grafico-par` del cap. 1. Arreglo: consultas de contenedor sobre `#content-area`, o
   `display:block; overflow-x:auto` para toda tabla a cualquier ancho.
4. **Fórmulas que desbordan sin pista** — `.formula` (l. 585) y `.definition/.note/.warning` (l. 1105) con
   `overflow-x:auto`: el corte no se ve como corte. Ocho fórmulas a 800 y 375 px. Arreglo de contenido
   (`\begin{aligned}` o partir en dos líneas las tres del M3 y la del ruido blanco) o, como mínimo, una sombra de
   desplazamiento en el borde derecho.
5. **Leyendas** — mismo ayudante para todo: la banda (recta) aparece como un rectángulo gris con borde naranja
   (`usePointStyle` + `pointStyle:'line'` lo dibujaría como raya); a 375 px los textos largos se truncan (M4 serie, M6) y
   las leyendas de dos entradas pasan a dos líneas (54 px de 207 en M5 y M7); en los paneles de una sola serie con
   `grafico-etiqueta` encima (M3, M4) la leyenda repite lo que dice la etiqueta.
6. **El cero del eje y** — en `crearGraficoBarras` el `suggestedMin/Max` ±1 sin `stepSize` deja que Chart.js elija un
   paso que se salta el 0 (M2, 250 px); en las series diferenciadas de M5 y M7 pasa lo mismo. Para un correlograma, el 0
   es la referencia: `ticks.stepSize: 0.5` y una línea de rejilla más oscura en 0 (callback de `grid.color`).
7. **Accesibilidad de los simuladores** — ninguna de las 5 `.simulador-lectura` lleva `aria-live` (4 cambian con los
   controles: explorador, AR(1), diferenciación, Box-Cox); 9 de los 18 lienzos de simulador cambian de contenido con
   un `aria-label` fijo; los dos del quiz dicen la respuesta. `actualizarLectura()` (l. 5027) es
   el sitio para poner `aria-live="polite"` una vez y para reescribir el `aria-label` del lienzo con la serie y el
   parámetro. El nombre accesible del deslizador concatena etiqueta y valor sin espacio («Coeficiente φ0.70»): menor.
8. **Texto matemático en el lienzo** — Chart.js no pasa por KaTeX: «y_t», «∇y_t», «∇^2», «∇^3». Unicode basta: «yₜ»,
   «∇yₜ», «∇²», «∇³».
9. **Contraste del naranja** `#FF6600` (2.94:1): en este capítulo es **la banda de confianza de los 10 correlogramas**,
   rayada y de 1.5 px. `#e05a00` da 3.73:1 y `#c2410c` 5.18:1 sin cambiar de familia.
10. **Formato de cifras en las lecturas** — `actualizarLectura` no agrupa miles ni usa el signo menos: `338834.24`,
    `16760012.970`, `-1.00`, frente a `338 834` en las tablas y `−20 000` en los ejes (que sí pasan por `agrupaMiles`,
    l. 4691). Aplicar el mismo `agrupaMiles` y `−` en `actualizarLectura`.
11. **Fuente del módulo de arranque** — `fuentesDeLosLienzos()` resuelve el caso normal; si la fuente llega después del
    tope de 3 s, nada repinta. Un `document.fonts.ready.then(() => graficosActivos.forEach(g => g.update('none')))`
    tras el primer `loadModule` lo cierra.

## Lo que está bien resuelto

- **Bandas**: todas en ±1.96/√n con la n de lo que se dibuja, recalculadas al cambiar de serie, al diferenciar
  (n − d) y al activar ∇ (n = 199); coinciden con las lecturas, la prosa y las retroalimentaciones del quiz.
- **Lo que dicen las lecturas coincide con la prosa** en M2, M4, M6, M7 y M8 (cifras comprobadas contra `DATOS_CAP2`).
- Ningún desborde horizontal de la página a ningún ancho (`scrollWidth` = ancho de la ventana en los 27 casos); ningún
  lienzo se sale de su simulador (el `.grafico-par` del cap. 1 no existe aquí).
- Los títulos `h4` de los simuladores se parten bien a 375 px (no llevan `<code>`, a diferencia del cap. 1).
- Con la red normal todos los ejes se pintan con Montserrat / Fira Code ya cargadas.

## Lo que no se miró, y por qué

- **Tooltips** (paso del cursor): no simulados; modo `index` en todos los gráficos, juzgado solo por el código.
- **Teclado**: los controles son `<input type=range>`, `<select>` y una casilla dentro de `<label>`; no se probaron con
  teclas.
- **Modo oscuro / impresión**: fuera de la revisión.
- De las 183 capturas se abrieron unas 40 (todos los simuladores a 1200 en estado inicial y en los extremos que dan los
  problemas, todos a 375 en estado inicial o en el estado problemático, y M5, M6, M7, M8 y una tabla a 800). El resto
  son estados ya vistos a otro ancho; sus medidas están en `medidas.json` y `resumen.out`.
