# Capítulo 5 · revisión de gráficas y simuladores (dibujados)

Archivo: `Htmls_Series/capitulo-5-sarima.html` (commit `f807b40`, worktree `course-content-improvement-227f2c`, árbol
limpio salvo `diagnostico/cap5/`). Se levantó `python3 -m http.server 8765 --bind 127.0.0.1 --directory Htmls_Series`
y se comprobó que entregaba el mismo archivo (md5 `ff6b52cb334da6792c5a4628fc1053bf` en disco y por HTTP); se cerró al
terminar. Revisado el 2026-11-23 con Chrome sin ventana por CDP (puerto de depuración 9278, perfil temporal), con el
cliente `chrome.js` copiado del cap. 4. No se tocó el capítulo.

- **Qué se miró**: los **14 simuladores** con `data-simulador` más el simulacro `cap5-simulacro` (15 en total, no 16: la
  l. 6695 que aparece al buscar `data-simulador` es un comentario del armazón). Tienen **15 lienzos** de Chart.js; dos
  simuladores no tienen lienzo y dibujan con HTML: `receta-mes` (tabla) y `tienda-cuadricula` (`.mapa-estacional`).
  Además: el `.mapa-estacional` de `mapa-firma`, el **gráfico del quiz** (`AUTOEVALUACIONES['cap5']`, `tipo:'grafico'`,
  registrado como módulo 4 pero dibujado en el quiz del M11) y las **4 figuras SVG** del simulacro (M12).
  `TABLAS_RANKING['comparativa']` es una tabla y no se dibuja: solo se contrasta su texto con el simulador de al lado.
- **Anchos**: **1200 px** (lienzo 666 px), **800 px** (lienzo 282 px; la barra lateral sigue abierta) y **375 px**
  (`mobile:true`, dsf 2; lienzo 236 px).
- **Estados**, cada simulador en su estado inicial y en sus extremos:
  - **M1 `mapa-firma`**: las **32** combinaciones serie × logaritmo × diferenciación (4 × 2 × 4), medidas todas y 11
    capturadas.
  - **M2 `receta-mes`**: (φ, Φ) = (0, 0), (0.6, 0), (0, 0.7), (1, 1), (−1, −1), (1, −1), (−0.5, 0.3), (−1, 1).
  - **M2 `constructor-polinomio`**: todo en 0, D = 0, (0,0,0)(2,2,0), todo en 2, (2,2,0)(0,0,0).
  - **M3 `tienda-cuadricula`**: los 8 casos (2 escenarios × 4 restas).
  - **M3 `cuatro-combinaciones`**: las 4 combinaciones.
  - **M3 `sobrediferenciacion-estacional`**: D = 0, 1, 2.
  - **M4 `firma-teorica`**: 10 estados (todo en 0; Φ = ±0.85; φ con Φ; solo Θ; θ y Θ; todo en ±0.85; solo φ).
  - **M5 `airline-pesos`**: 6 estados (Θ = 0; Θ = −0.95; los dos en −0.95; los dos en 0.5; los dos en 0; θ = −0.95 con
    Θ = 0.5).
  - **M6 `explorador-sarima`**: **los 36 modelos**, medidos todos y 8 capturados.
  - **M7 `pronostico-estacional`**: h = 1, 12, 13 y 24, en escala original y en logaritmos.
  - **M8 `contraejemplo-trm`**: las dos series.
  - **M9 `calendario-regresores`**: los 4 estados de los interruptores.
  - **M10 `armonicos-K`**: K = 1…6.
  - **M11 `comparativa-particion`**: RMSE, MAE y MAPE; los 8 métodos encendidos; todos apagados.
- **Cómo**: el método del cap. 4 (`Chart.defaults.animation = false`, `loadModule(n)`, `Runtime/Log.enable`, captura por
  elemento con la cabecera fija desactivada; las `mN-vistaK-800/375.png` son la pantalla real). Lo nuevo respecto del
  cap. 4:
  - Medidas del `.mapa-estacional`: si la rejilla se desplaza, cuántos meses se ven sin desplazar, el contraste de
    **cada** celda con número, los guiones y la leyenda.
  - El texto de la tabla de la receta.
  - Un recorrido aparte de las figuras SVG del simulacro (`graficas_simulacro.js`).
  - Un contraste de los datos incrustados (`DATOS_CAP5` l. 6301, `SERIES_CAP5` l. 6302) con lo que afirman las intros,
    las lecturas y la prosa (`graficas_datos.py`).
- **Consola**: ninguna excepción ni `console.error/warn` en 12 módulos × 3 anchos × ~150 estados. Solo el 404 de
  `/favicon.ico` del servidor de pruebas. Ningún dato NaN ni no finito. Ningún marcador recortado por el borde. Ningún
  guion en los ejes de Chart.js. Nada asoma fuera de `<main>` sin un contenedor desplazable (`recortados` vacío en los
  36 módulo-ancho). `docSw` es igual al ancho de la ventana en los tres anchos.
- **Red**: ningún dibujo depende de datos.gov.co. La TRM va incrustada (`SERIES_CAP5.trm`,
  `DATOS_CAP5.trm_contraejemplo`) y el JS no hace ningún `fetch`. Solo los bloques de código R/Python (l. 3180, 5202,
  5258, 6088) descargan la serie, y eso no se ejecuta en la página.
- **Recuento**: 42 problemas: **4 Altas, 13 Medias, 25 Bajas** (tres Medias y una Baja son del componente `.mapa-estacional`, contadas en la causa común E); 8 defectos de causa común al final.
- **Gravedad** (la de los caps. 2–4): **Alta** = oculta contenido o hace que el gráfico diga otra cosa que la prosa o la
  lectura; **Media** = cuesta leerlo o deja fuera a alguien (lector de pantalla, teléfono, 800 px); **Baja** = acabado.

**Guiones y datos**, en `diagnostico/cap5/diag/`:

- `chrome.js`: cliente CDP.
- `graficas_revisa.js`: el recorrido, adaptado de `cap4/diag/graficas_revisa.js`.
- `graficas_resumen.py` → `graficas_resumen.out`: todo, por estado.
- `graficas_tabla.py` → `graficas_tabla.out`: un renglón por lienzo y ancho.
- `graficas_datos.py` → `graficas_datos.out`: datos frente a prosa.
- `graficas_iconos.js` → `graficas_iconos.out`.
- `graficas_simulacro.js` → `graficas_simulacro.out`, y `graficas_simulacro_captura.js`.
- Medidas crudas en `graficas_medidas.json`.

Capturas en `diagnostico/cap5/capturas/` (385 PNG; abreviado `…/` abajo).

**Líneas**: «HTML l.» es el capítulo final; «fuente» es donde hay que corregir, porque el capítulo se reensambla:
- El JS sale de `ensamblado/cap5/chapter.js`, con fuente = HTML − 8284 en la zona de simuladores.
- Las intros y los lienzos salen de `ensamblado/cap5/templates_*.html`.
- El `.mapa-estacional` sale de `ensamblado/componentes/mapa_estacional.{js,css}`.
- El armazón de gráficos (HTML l. 6699–7500) viene del cap. 2 por la cadena 2 → 6.

**Lo que funciona**:

- **Las cifras de las lecturas y de las tablas cuadran con los datos incrustados.**
  - Las del M1, el M3 y el M8: ρ̂₁, ρ̂₁₂, ρ̂₂₄ y ρ̂₃₆ de las 5 filas de «Dónde mirar la ACF»; varianzas y ρ̂ de las 4
    combinaciones; 0.002102 / 0.005960 y Θ̂ = −0.9973 de la sobrediferenciación, con la varianza calculada en el
    navegador idéntica a la de R.
  - Las del M2 y el M4: 0.6016 / 0.4230 / 0.7011 / 0.4218 del AR(1)×SAR(1).
  - Las del M7: 525.46 [399.66, 690.85] a h = 24.
  - Las del M9: −483.21 / −486.54 / −490.72 y los β̂.
  - Las del M10: las 6 filas armónicas; Ljung–Box deja de rechazar en K = 5, como dice la intro.
  - Las del M11: los 8 métodos; el SARIMA queda cuarto por las tres métricas.
- **La cuadrícula de la tienda cumple lo que dice la prosa**: −11 en enero y 5 en diciembre con ∇; todo 12 con ∇₁₂;
  14 → 36 al acelerar; 2 en 2024 y 0 fuera.
- **El arreglo del cap. 4 llega bien**:
  - La muestra de la leyenda de `crearGraficoLinea` dibuja rayas para las líneas (con su discontinuidad), cajas para las
    bandas del abanico y un círculo para los puntos de Pascua.
  - Los correlogramas de `crearGraficoBarras` rotulan el 12, el 24 y el 36 a los tres anchos, con el 1 siempre y el 0
    oscuro.
  - Las series mensuales que no pasan `scales` propios rotulan años redondos («1951…1960»), y las cortas, meses
    («1959 · mar · may…»).
  - Signo menos tipográfico en todos los ejes y en todas las lecturas.

---

## M1 · `mapa-firma` — canvas HTML l. 3124 (fuente `templates_1_3.html` l. 67) · JS HTML l. 8464 (fuente l. 180)

- **Pretende**: «Prueba AirPassengers con logaritmo y las dos diferencias: las bandas verticales desaparecen y la ACF se
  queda con dos barras, en los rezagos 1 y 12. Y prueba la TRM en cualquier combinación: nunca hay bandas. Con la TRM
  sin logaritmo y una diferencia regular, la lectura reproduce exactamente la última fila de la tabla».
- **Se ve**: con ∇∇₁₂ log, el mapa sin bandas y las barras grandes en 1 y 12. Con la TRM sin log y ∇, ρ̂₁ = 0.0876,
  ρ̂₁₂ = −0.0025, ρ̂₂₄ = −0.0672 y banda 0.1675, como la tabla.
- **Problemas**
  1. **[Alta]** **La ACF no «se queda con dos barras»**. Con log y ∇∇₁₂ salen de la banda ±0.1712 **seis**: los
     rezagos 1 (−0.341), 3 (−0.202), 9 (0.176), 12 (−0.387), 23 (0.223) y 32 (0.196). Las seis cruzan la raya
     discontinua en el dibujo a los tres anchos. Quien siga la instrucción y cuente barras fuera de la banda no
     encuentra lo que la intro promete. Intro HTML l. 3109–3110 (fuente `templates_1_3.html` l. 52–53).
     `…/m1-mapa-firma-airpassengers-log-d1D1-1200.png`; cifras en `graficas_datos.out`.
  2. **[Media]** **La lectura señala la TRM como estacional** en dos combinaciones: con ∇₁₂ (con y sin log) y con ∇∇₁₂.
     Allí dice «rezagos estacionales fuera de banda: **12**», con ρ̂₁₂ = −0.354 y −0.360. Es la huella de diferenciar
     de más una serie sin estación, pero la intro acaba de decir «la TRM en cualquier combinación: nunca hay bandas», y
     el renglón de la lectura se rotula como evidencia de estacionalidad. JS HTML l. 8521 y 8528–8531 (fuente l. 237,
     244–247). `graficas_resumen.out`, estados `trm-*-D1` y `trm-*-d1D1`.
  3. **[Baja]** «La lectura reproduce **exactamente** la última fila»: no muestra ρ̂₃₆ (la fila tiene 0.071), y da 4
     decimales donde la tabla da 3.
  4. **[Baja]** `aria-label` fijo («Correlograma de la serie transformada»): no dice qué serie ni qué diferencias.
     Común B.
  5. El mapa tiene sus propios defectos (contraste, guiones, rejilla cortada a 800/375 y ARIA): causa común E.
- Capturas: `…/m1-mapa-firma-{airpassengers-log-ninguna,airpassengers-log-d1D1,trm-nolog-d1,…}-{1200,800,375}.png`

## M2 · `receta-mes` — tabla HTML l. 3343 (fuente `templates_1_3.html` l. 279) · JS HTML l. 8560 (fuente l. 276)

- **Pretende**: «Las dos rutas de la lectura siempre dan lo mismo».
- **Se ve**: lo dicho en los 8 estados; con φ = Φ = 1, «pesos +1, +1 y −1».
- **Problemas**
  1. **[Baja]** Las celdas de la tabla escriben los negativos con **guion** («× -0.42 = -6.30», «-45.00»): `celda()`
     usa `fmt()` sin `conSignoMenos()`. La lectura de debajo sí lleva el signo menos, así que la misma cifra sale con
     dos signos distintos. JS HTML l. 8567 y 8599 (fuente l. 283, 315). `…/m2-receta-mes-phi-1-Phi-1-1200.png`
  2. **[Baja]** Con φ = −1 el rótulo del modelo dice «un factor vale ±1: **es una diferencia**», pero (1 + B) no es una
     diferencia. JS HTML l. 8575–8576 (fuente l. 291–292).

## M2 · `constructor-polinomio` — canvas HTML l. 3534 (fuente `templates_1_3.html` l. 470) · JS HTML l. 8626 (fuente l. 342)

- **Pretende**: los parámetros libres frente al rezago más lejano; «Sube D a 1 y verás cuántas observaciones cuesta».
- **Se ve**: 8 barras no nulas en (1,1,1)(1,1,1), como la lectura; el eje rotula 12, 24 y 26.
- **Problemas**
  1. **[Baja]** La intro dice «Sube D a 1», pero el estado inicial ya tiene D = 1 (`params`, JS HTML l. 8627 / fuente
     l. 343; intro HTML l. 3529 / fuente l. 465).
  2. **[Baja]** Con todos los órdenes en 0, el lienzo queda **vacío**: sin barras, sin marcas en el eje x y sin
     mensaje. `…/m2-constructor-polinomio-todo0-1200.png`
  3. **[Baja]** Con todo en 2, la escala llega a ±10 y los coeficientes pequeños de los rezagos 37–52 no se ven. La
     lectura dice «24 no nulos» y el dibujo enseña unos 14. `…/m2-constructor-polinomio-todo2-1200.png`

## M3 · `tienda-cuadricula` — mapa HTML l. 3860 · JS HTML l. 8693 (fuente l. 409)

- **Se ve**: las 8 cuadrículas cuadran con la prosa (ver arriba). La lectura usa «−» en las cuentas.
- **Problemas**: los del componente (común E). Con ∇ y crecimiento fijo, **las 19 celdas con número tienen contraste
  < 3:1** (2.92:1, blanco sobre gris verdoso); con «acelera» y ∇, 17 de 47. A 800 y 375 px solo se ven enero a junio.
  `…/m3-tienda-cuadricula-fijo-d1-1200.png`, `…/m3-tienda-cuadricula-375.png`

## M3 · `cuatro-combinaciones` — canvas HTML l. 4044, 4048 · JS HTML l. 8777 (fuente l. 493)

- **Se ve**: lo que dicen la intro y la tabla (0.762 → 0.841 con ∇; las cuatro filas).
- **Problemas**: solo el `aria-label` fijo de los dos lienzos (común B).

## M3 · `sobrediferenciacion-estacional` — canvas HTML l. 4091 · JS HTML l. 8820 (fuente l. 536)

- **Se ve**: D = 0, 1, 2 con la tabla; con D = 2, «⚠ raíz sobre el círculo».
- **Problemas**
  1. **[Baja]** La leyenda escribe el exponente con acento circunflejo: «∇ ∇₁₂^0 log(AirPassengers)», «∇₁₂^2». JS
     HTML l. 8839 (fuente l. 555). `…/m3-sobrediferenciacion-estacional-D0-800.png`

## M4 · `firma-teorica` — canvas HTML l. 4310, 4314 (fuente `templates_4_6.html` l. 97, 101) · JS HTML l. 8865 (fuente l. 581)

- **Pretende**: «sube solo Φ: picos limpios en 12, 24, 36… añade φ y brotan los satélites en 11 y 13».
- **Se ve**: lo dicho en los 10 estados, sin inestabilidad numérica en los extremos ±0.85.
- **Problemas**
  1. **[Media]** **El área de cada correlograma mide 85 px de alto a 1200 px** (marco de 190 px menos leyenda y eje), y
     86–89 px a 800/375. En ella caben los picos de 0.70, 0.49 y 0.34, pero las barras de 0.05–0.15 de los satélites
     apenas se distinguen. Común D. `…/m4-firma-teorica-phi05-Phi07-1200.png`
  2. **[Baja]** «Empieza con todo en cero»: el estado inicial es Φ = 0.7, no cero (JS HTML l. 8866 / fuente l. 582).

## M5 · `airline-pesos` — canvas HTML l. 4606, 4610 (fuente `templates_4_6.html` l. 279, 283) · JS HTML l. 8914 (fuente l. 630)

- **Pretende**: «Lleva Θ hacia 0 y el **escalón del rezago 12 desaparece** —sin término estacional, el modelo no
  distingue el mes—. Llévalo hacia −1 y los pesos se aplanan».
- **Se ve**: lo contrario en la primera mitad.
  - Con θ = −0.40 y Θ = 0: ψ₁…₁₁ = 0.60 y **ψ₁₂ = 1.60**. El salto es de +1.00, el **mayor** posible; en el estado
    inicial es de +0.44.
  - Con Θ = −0.95, el salto es de +0.05.
  - Sin MA estacional queda la diferencia estacional desnuda, cuyos pesos suben un escalón entero cada año: es Θ → −1
    lo que borra el escalón, no Θ → 0.
- **Problemas**
  1. **[Alta]** **La intro dice lo contrario de lo que se dibuja** con Θ = 0. La lectura lo confirma: «ψ₁₂ 1.6000». La
     glosa «sin término estacional, el modelo no distingue el mes» tampoco se sostiene: el modelo sigue teniendo ∇₁₂.
     Intro HTML l. 4600–4602 (fuente `templates_4_6.html` l. 273–275). `…/m5-airline-pesos-Theta0-1200.png`; cifras en
     `graficas_datos.out`.
  2. **[Media]** El eje de σₕ se reescala solo. Con θ = Θ = −0.95, σₕ va de 0.0370 a 0.0390 (σ₁₂/σ₁ = 1.014), pero el
     eje 0.037–0.0395 lo dibuja como una rampa tan empinada como la del estado inicial. El «se aplanan» de la intro no
     se ve en la curva de abajo. `lineaSimple` sin `min: 0`, JS HTML l. 8943–8945 (fuente l. 659–661).
     `…/m5-airline-pesos-theta-095-Theta-095-1200.png`
  3. **[Baja]** El rótulo «σₕ (escala logarítmica)» se lee como un eje logarítmico. El eje es lineal: lo logarítmico es la
     escala de la serie. HTML l. 4608 (fuente l. 281).
  4. **[Baja]** El área de ψⱼ mide 95 px a 1200 (común D). Con θ = Θ = 0.5 el eje llega a 6 sin aviso (es
     `suggestedMax`), lo que está bien, pero el gráfico cambia de escala entre estados vecinos.

## M6 · `explorador-sarima` — canvas HTML l. 4674 · JS HTML l. 8970 (fuente l. 686)

- **Se ve**: los 36 modelos existen en `AP.rejilla` (la rama «no convergió» nunca se dispara), y la ACF residual se
  dibuja con la banda 0.163. El airline, marcado ★, deja una barra fuera (rezago 23, 0.220).
- **Problemas**
  1. **[Baja]** La tabla de al lado pone «—» en BIC y en ρ̂₁₂ para (0,1,0)(0,1,0)₁₂. El simulador da BIC −431.9548 y
     ρ̂₁₂ −0.3907 para ese mismo modelo (tabla HTML l. 4688, fuente `templates_4_6.html` l. 361).
     `…/m6-explorador-sarima-pqPQ0000-1200.png`
  2. **[Baja]** A 375 px la leyenda pasa a 2 líneas y el área baja a 98 px. Común D.

## M7 · `pronostico-estacional` — canvas HTML l. 4952 (fuente `templates_7_9.html` l. 159) · JS HTML l. 9026 (fuente l. 742)

- **Pretende**: «en logaritmos el abanico se abre **a escalones** —se ensancha de golpe al cruzar cada rezago
  estacional—».
- **Se ve**: un abanico que se abre de forma continua.
  - En 24 meses solo se cruza un rezago estacional (h = 13).
  - Allí el ancho del IC 95 % pasa de 0.3225 a 0.3561 (+0.034), frente a +0.019–0.024 en los meses vecinos.
  - Sobre el patrón estacional del pronóstico, el escalón no se percibe a ningún ancho.
  - La asimetría en escala original (125.80 / 165.39) sí se ve y cuadra con el aviso de la prosa.
- **Problemas**
  1. **[Media]** El dibujo no muestra los «escalones» que la intro manda ver. Intro HTML l. 4947–4949 (fuente
     `templates_7_9.html` l. 154–156). `…/m7-pronostico-estacional-log-h24-1200.png`,
     `…/m7-pronostico-estacional-log-h13-1200.png`
  2. **[Baja]** A 800/375 px la leyenda pasa a 2 líneas (54 px); el área sigue en 173–176 px.

## M8 · `contraejemplo-trm` — canvas HTML l. 5145 (fuente `templates_7_9.html` l. 352) · JS HTML l. 9092 (fuente l. 808)

- **Se ve**: ∇ log AP con ρ̂₁₂ = 0.84, ρ̂₂₄ = 0.74 y ρ̂₃₆ = 0.66, muy fuera de la banda; ∇TRM con las tres dentro, como
  la tabla.
- **Problemas**
  1. **[Media]** El renglón **«fuera de banda»** de la lectura solo mira 12, 24 y 36, y el rótulo no lo dice. Con la TRM
     dice «**ninguno**», pero el dibujo saca la barra del rezago 8 (ρ̂₈ = −0.190 frente a ±0.1675). Con AirPassengers
     dice «12, 24, 36», y hay **14** barras fuera. En el M1 el mismo renglón se llama «rezagos estacionales fuera de
     banda». JS HTML l. 9124 y 9132 (fuente l. 840, 848). `…/m8-contraejemplo-trm-trm-1200.png`
  2. **[Baja]** A 800/375 px la leyenda pasa a 2 líneas y el área baja a 105–108 px. Común D.

## M9 · `calendario-regresores` — canvas HTML l. 5343 (fuente `templates_7_9.html` l. 550) · JS HTML l. 9149 (fuente l. 865)

- **Se ve**: las tres filas de la tabla en sus estados; la línea de días entre 28 y 31 en el eje derecho, y los puntos
  de Pascua.
- **Problemas**
  1. **[Alta]** **Con «Semana Santa» encendida y «log(días)» apagado**, la lectura escribe «modelo: Semana Santa sola:
     no precalculada». Debajo da **las cifras del modelo con los dos regresores**:
     - AICc −490.7221, «mejora sobre el airline 7.5120 puntos» y BIC −476.8261;
     - **β̂ log(días) 1.0840**, aunque ese regresor está apagado y el gráfico no lo dibuja;
     - β̂ Semana Santa 0.0290.

     El código elige `con_dias_pascua` para ese caso (JS HTML l. 9165–9167, fuente l. 881–883) y solo cambia el nombre
     (l. 9200, fuente l. 916). `…/m9-calendario-regresores-dias0-pascua1-1200.png`
  2. **[Media]** El simulador pasa sus propios `scales` (JS HTML l. 9192–9196, fuente l. 908–912) y con ellos pierde
     `marcasLegibles`. El eje x rotula `AAAA-MM` crudo: a 1200 «1949-01, 1950-01…». A 800 px se pisa en cinco pares
     (`1949-01|1951-01` −1.2 px…), y a 375 px sale irregular («1949-01, 1951-06, 1953-11, 1956-04, 1958-09») y se
     pisa (−6.8 px). Común A. `…/m9-calendario-regresores-dias1-pascua1-800.png`
  3. **[Baja]** Los puntos de Pascua se dibujan en «31» del eje de días (`v ? 31 : null`, l. 9184). El eje derecho no
     tiene título, y un mes de abril con Pascua aparece en «31 días». Ninguno de los dos ejes lleva título.
  4. **[Baja]** «meses con Pascua en marzo: 2 de 12»: son 2 **años** de 12 (l. 9213, fuente l. 929).

## M10 · `armonicos-K` — canvas HTML l. 5546 (fuente `templates_10_11.html` l. 68) · JS HTML l. 9229 (fuente l. 945)

- **Se ve**: las 6 curvas con la K = 6 de referencia, rayada. Ljung–Box rechaza hasta K = 4 y no desde K = 5, como la
  intro. El eje rotula «1949 · mar · may…».
- **Problemas**: solo el `aria-label` fijo («…con K términos de Fourier»; no dice qué K). Común B.

## M11 · `comparativa-particion` — canvas HTML l. 5733 (fuente `templates_10_11.html` l. 250) · JS HTML l. 9274 (fuente l. 990)

- **Se ve**: por defecto, observado más 4 métodos. El ranking de la lectura coincide con la tabla y con
  `TABLAS_RANKING['comparativa']`: el SARIMA cuarto por las tres métricas.
- **Problemas**
  1. **[Alta]** **Con los 8 métodos encendidos, a 800 y 375 px la leyenda no cabe y se corta.** Chart.js la limita a
     media altura (127–128 px para 9 entradas en 9 líneas), y a 375 px se leen 5 entradas. La quinta,
     «auto.arima sobre el log…», queda partida por el eje, y «SARIMA + calendario», «ETS sobre la serie cruda» y
     «Naive estacional» desaparecen. Sus líneas siguen dibujadas, sin nombre. A 1200 px caben (4 líneas, área de
     129 px). `…/m11-comparativa-particion-todos-375.png`, `…-todos-800.png`
  2. **[Media]** **Colores casi iguales** (JS HTML l. 9282–9283, fuente l. 998–999):
     - la regresión armónica `#0e7490` frente a auto.arima `#0f766e` (dos verdes azulados);
     - STL `#7c3aed` frente a ETS crudo `#9333ea` (dos violetas);
     - ETS log `#FB6400` frente a SARIMA + calendario `#a16207`.

     Todos van con la misma raya discontinua. Con los 8 encendidos no se sabe qué línea es cuál.
     `…/m11-comparativa-particion-todos-1200.png`
  3. **[Media]** **Rótulos cortados a media palabra y sin puntos suspensivos**:
     - los interruptores, a 26 caracteres: «ETS sobre el logaritmo: ET», «SARIMA airline (0,1,1)(0,1», «auto.arima sobre el
       log: A», «SARIMA airline + calendari», «ETS sobre la serie cruda: » (l. 9327, fuente l. 1043);
     - la leyenda, a 34: «auto.arima sobre el log: ARIMA(0,1» (l. 9294, fuente l. 1010);
     - la lectura, a 38: «Regresión armónica K = 6 + errores ARI», «auto.arima sobre el log: ARIMA(0,1,1)(» (l. 9312,
       fuente l. 1028).
  4. **[Baja]** SARIMA y auto.arima tienen el mismo pronóstico (`graficas_datos.out`): encendidos a la vez, una línea
     tapa a la otra.
  5. **[Baja]** La intro pide «antes de leer el párrafo siguiente, apunta cuál dirías que es el mejor», pero la lectura,
     encima del gráfico, ya ordena los ocho con «← el SARIMA» en cuarto lugar. La tabla ordenable, justo antes del
     simulador, lo dice en su descripción.
  6. **[Baja]** Con «MAPE (%)» los valores salen sin «%» («3.151»; l. 9313).
  7. **[Baja]** El icono del `<h4>`, `fa-ranking-star`, **no existe en Font Awesome 6.0.0** y no se dibuja: el título
     queda con un hueco a la izquierda (HTML l. 5726, fuente `templates_10_11.html` l. 243). Común G.
     `graficas_iconos.out`

## M11 · gráfico del quiz (`AUTOEVALUACIONES['cap5']`, pregunta 5) — JS HTML l. 9462–9472 (fuente l. 1178–1188)

- **Se ve**: ACF teórica de un SAR(1)₁₂ con Φ = 0.7: picos de 0.70, 0.49 y 0.343 y ceros en el resto, que es lo que
  dicen la opción correcta y las retros.
- **Problemas**
  1. **[Media]** **Sin `descripcionGrafico`**: el lienzo se anuncia como «Gráfico de la pregunta» (armazón, HTML
     l. 7678). Quien usa lector de pantalla no puede responder una pregunta que solo se responde mirando. Los caps. 2, 3
     y 4 sí la llevan en sus preguntas de gráfico (`describirBarrasQuiz` / `descripcionCorrelogramaQuiz`).
  2. **[Baja]** A 375 px el área mide 113 px y las barras, 1.6 px de ancho. `…/m11-quiz-grafico1-375.png`

## M12 · `cap5-simulacro` — figuras SVG (registro `ensamblado/cap5/simulacro.js`, CSS `componentes/simulacro_correccion.css` l. 208, 248)

- **Se ve**: 4 figuras SVG (ACF/PACF de ∇∇₁₂ log y, residuales, ACF residual) con `role="img"` y `aria-label`. Sin
  guiones; el simulacro no desborda a ningún ancho.
- **Problemas**
  1. **[Media]** **A 800 px las figuras se encogen a 266 px** (escala 0.58 del `viewBox` de 460), y los rótulos de los
     ejes quedan en **~7 px** de cuerpo (caja de texto de 9 px). `graficas_simulacro.out`;
     `…/m12-cap5-simulacro-figura1-800.png`
  2. **[Baja]** A 375 px la figura mide 350 px dentro de una caja de 256 px que se desplaza. Sin desplazar se ven los
     rezagos 1–27, y el pie dice «de los rezagos 1 a 36». `…/m12-cap5-simulacro-figura1-375.png`
  3. **[Baja]** La banda va en azul (`#2563eb`), cuando en el resto del capítulo es la raya naranja `#e05a00`.

---

## Causas comunes

- **A. Un simulador que pasa `scales` propios pierde los ejes del armazón.** `crearGraficoLinea` fusiona `scales` con
  `Object.assign` superficial (lo advierte el propio armazón, HTML l. 7005–7012). En el cap. 5 solo lo hace
  `calendario-regresores` (M9): fechas `AAAA-MM` crudas y solapes a 800/375. El resto usa los ejes por defecto y sale
  bien, así que el arreglo es del cap. 5 (fuente), no del armazón.
- **B. Ningún `aria-label` cambia con el estado.** Los **15 lienzos** llevan la descripción fija del HTML, la misma en
  los ~150 estados medidos. El armazón trae `descripcionCorrelograma()` (HTML l. 7495), que el cap. 4 adoptó, pero el
  cap. 5 no la llama nunca: lo arreglado en el 4 **no llega** al 5, porque vive en el JS propio de cada capítulo. Los
  correlogramas (M1, M3, M4 ×2, M6, M8 y el quiz) podrían usarla tal cual.
- **C. Muestra de la leyenda: arreglo heredado que llega bien.** `etiquetasDeLeyendaLinea` (HTML l. 7210) y
  `etiquetasDeLeyendaBarras` (l. 7188) dibujan rayas, cajas y puntos según lo que sea cada serie, en todos los
  gráficos del cap. 5. El defecto C del cap. 4 no se reproduce.
- **D. Marcos de altura fija sin compensar la leyenda.** Las alturas de `grafico-wrapper` (190–230 px) dejan áreas de
  85–105 px a 1200 en M2, M3, M4 y M5. A 800/375, las leyendas de 2 líneas bajan el área a 98–108 px (M6, M8), y la
  de 5 líneas de la comparativa, a 107–110 px. Con 9 entradas la leyenda se trunca (Alta del M11). No hay `compactar()`
  en este capítulo.
- **E. Componente `.mapa-estacional`** (`ensamblado/componentes/mapa_estacional.js` y `.css`; HTML l. 8001–8056 y
  2187–2280). Lo comparten los caps. 1 y 5 y la plantilla:
  1. `textoSobre()` cambia a texto blanco por debajo de una luminancia de 0.42 (`.js` l. 48). Así, los fondos medios
     gris verdosos y naranjas quedan con **contraste de 2.24–2.9:1**: en AirPassengers log, 42 de 144 celdas por
     debajo de 4.5:1 y 19 por debajo de 3:1. **[Media]**
  2. La rejilla tiene `min-width: 34rem` (`.css` l. 40). A 800 y 375 px se desplaza dentro de su caja y **solo se ven
     enero a junio**, sin indicio de que haya más. Las «bandas verticales» que la prosa manda buscar quedan a medias.
     **[Media]**
  3. Las cifras de las celdas y los extremos de la leyenda se escriben con `toFixed()` y **guion** («-0.141»,
     «-470.2»; `.js` l. 78 y 96). Hay hasta 71 guiones por estado. **[Baja]**
  4. `role="table"` contiene `columnheader`, `rowheader` y `cell` **sin ningún `role="row"`** (`.js` l. 62–83): la
     tabla no es navegable como tal con lector de pantalla. Además, el `aria-label` de la rejilla no dice qué serie ni
     qué transformación. **[Media]**
- **F. `fmt()` del cap. 5 no pone signo menos** (JS HTML l. 8346, fuente l. 62). En las lecturas lo arregla
  `actualizarLectura` → `conSignoMenos`, pero todo lo que escribe `fmt()` fuera de una lectura sale con guion: la tabla
  de la receta (M2).
- **G. Font Awesome 6.0.0** (HTML l. 18; la cadena 2 → 6): en el cap. 5 queda vacío un icono, `fa-ranking-star`
  (M11). Los dos del cap. 4 no se repiten.
- **H. Intros escritas para un estado que no es el inicial** (cap. 5): «Empieza con todo en cero» (M4, Φ = 0.7),
  «Sube D a 1» (M2, D = 1 ya), y la del M5 sobre Θ → 0, que además es falsa. Conviene revisar cada intro frente a
  `params` y frente a los extremos.

## Lo que no se midió

- Los barridos completos de los deslizadores continuos: se tomaron los extremos y 3–10 puntos intermedios por
  simulador. Del M2 `receta-mes` no se probaron las 441 parejas (φ, Φ), y del M4 no se probaron todas las
  combinaciones de cuatro deslizadores (se tomaron 10).
- El simulacro más allá de sus figuras: no se respondió ni se corrigió. Su contenido es de la revisión de ejercicios.
- Tooltips (no se pasó el ratón), el giro del teléfono, el modo oscuro y el zoom del navegador.
- Un lector de pantalla real: solo se leyeron `aria-label`, `role` y la región viva común.
- Las fórmulas y tablas que se desplazan dentro de su caja (M1, M5, M7 y M12 a 800/375): son de prosa, fuera de esta
  lente.
