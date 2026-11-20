# Capítulo 3 · revisión de gráficas y simuladores (dibujados)

Archivo: `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` (commit `58bdfc5`, worktree
`course-content-improvement-227f2c`, árbol limpio). `http://localhost:8731/` no respondía; se levantó
`python3 -m http.server 8761 --bind 127.0.0.1 --directory Htmls_Series` y se comprobó que entregaba el mismo archivo
(md5 `b9c2a11444b6fe4a654bc703f91905c2` en disco y por HTTP). Se cerró al terminar. Revisado el 2026-11-19 con Chrome sin
ventana por CDP (puerto de depuración 9273), con el cliente `chrome.js` copiado del cap. 2. No se tocó el capítulo.

- **Qué se miró**: los 13 simuladores con lienzo (`data-simulador`; el decimocuarto, `cap3-simulacro` del M11, no tiene
  gráficos: solo se midió que no desborde) con sus **27 lienzos**, más los **2 gráficos del quiz** del M10
  (`tipo:'grafico'`, preguntas 3 y 9). El M1 no tiene gráficos.
- **Anchos**: **1200 px** (área 822 px, lienzo 666 px), **800 px** (área 438, lienzo 282) y **375 px** (`mobile:true`,
  dsf 2; área 345, lienzo 236).
- **Estados** (por defecto y extremos): panel AR ×4 procesos; triángulo AR(2) ×9 (ruido, complejo, φ₁+φ₂ = 0.99, raíz
  unitaria, φ₂ = −1, esquina (2, −1), (2.2, 1.2), (−2.2, −1.2), (1.4, −1.05)); panel MA ×3; ρ₁(θ) ×9 (θ = 0, 0.05, 0.2,
  0.5, ±1, ±5, −0.25); dualidad ×8 (h = 1 y 12, redundante, θ = 1, 1.05, ±2 con φ = ±0.95, φ = 0.95); laboratorio ×12
  (T = 60 y 1000, redundante y casi, φ₁ = 1 y 1.5, φ₁ = 0.95 con T = 1000, AR(2) (1.5, −0.95), θ₁ = 1.5, todo al máximo,
  «Otra realización»); teórica-muestral ×3; diagnóstico ×4 modelos; escala ×2; impulso h = 1, 6, 11, 24.
- **Cómo**: el método del cap. 2 (`Chart.defaults.animation = false`, `loadModule(n)`, `Runtime/Log.enable`, captura por
  elemento con la cabecera fija desactivada; las `mN-vistaK-800/375.png` son la pantalla real). Medidas nuevas respecto
  del cap. 2: datos de cada conjunto y si se salen del eje o son NaN, posición en píxeles de los puntos de dispersión y
  si quedan recortados por el borde del área, y altura útil del área de dibujo en todos los estados.
- **Consola**: ninguna excepción ni `console.error/warn` en 11 módulos × 3 anchos × todos los estados. Solo el 404 de
  `/favicon.ico` del servidor de pruebas. Fuentes: Montserrat y Fira Code cargadas en todos los ejes.
- **Recuento**: 42 problemas: **5 Altas, 19 Medias, 18 Bajas**; 9 defectos de causa común al final.
- **Gravedad** (la del cap. 2): **Alta** = oculta contenido o hace que el gráfico diga otra cosa que la prosa o la
  lectura; **Media** = cuesta leerlo o deja fuera a alguien (lector de pantalla, teléfono, 800 px); **Baja** = acabado.

Guiones y datos en `diagnostico/cap3/diag/`: `chrome.js` (cliente CDP), `graficas_revisa.js` (recorrido, adaptado de
`cap2/diag/revisa.js`), `graficas_resumen.py` → `graficas_resumen.out` (todo, por estado), `graficas_tabla.py` →
`graficas_tabla.out` (un renglón por lienzo y ancho); medidas crudas en `graficas_medidas.json`.
Capturas en `diagnostico/cap3/capturas/` (264 PNG; git las ignora; abreviado `…/` abajo).

Líneas: «HTML l.» es `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html`; «fuente» es `ensamblado/cap3/cap3_modulos.html`
(lienzos) y `ensamblado/cap3/cap3_js.js` (JS), que es donde hay que corregir: el capítulo se reensambla.

**Lo que ya se arregló en la R2 del cap. 2 y aquí funciona**: el 12 sale rotulado en los 16 correlogramas a los tres
anchos (los de 20 rezagos: `2,4,…,12,…,20` a 800 y `3,6,9,12,15,18` a 375; la TRM, mensual, también); el 0 del eje y
siempre rotulado y con la línea oscura; la banda se dibuja como raya discontinua `#e05a00` en la leyenda; ningún solape
de rótulos del eje x (0 casos); los controles van en una columna de 308 px a 800; las tablas anchas se desplazan con el
desvanecido (`ajustarTablas`); ninguna fórmula en bloque desborda a ningún ancho; las lecturas se anuncian por la región
viva común.

---

## M2 · `panel-ar-teorico` — canvas HTML l. 3008, 3012 (fuente l. 335, 339) · JS HTML l. 8281 (fuente l. 213)

- **Pretende**: «la PACF cae a cero de golpe en el rezago $p$ y se queda ahí, mientras la ACF nunca termina de cortarse»;
  la nota: ACF de φ = 0.8 «0.800, 0.640, 0.512», de φ = −0.7 alternando, AR(2) real monótona, AR(2) complejo que oscila
  «0.800, 0.370, −0.082, −0.392».
- **Se ve**: las cuatro firmas, con las cifras de la nota en las barras (comprobado contra `DATOS_CAP3.procesos`). La
  lectura «PACF en el rezago p+1: 0.0000» coincide con lo dibujado.
- **Problemas**
  1. **[Media]** A 800 y 375 px el eje rotula `2, 4, 6…`: **los rezagos 1 y 2 —donde está todo lo que distingue un AR(1)
     de un AR(2)— no llevan número** (común 2).
  2. **[Baja]** La intro dice que la PACF cae a cero «en el rezago $p$»; lo dibujado (y la lectura) es que cae *después*
     de $p$: la barra de $p$ es la última distinta de cero.
  3. **[Baja]** `aria-label` fijo («…del proceso seleccionado»): no nombra el proceso (común 8).
- Capturas: `…/m2-panel-ar-teorico-{ar1_pos,ar1_neg,ar2_real,ar2_comp}-{1200,800,375}.png`, `…/m2-vista1-375.png`

## M2 · `triangulo-ar2` — canvas HTML l. 3049 (triángulo), 3053 (serie) (fuente l. 376, 380) · JS HTML l. 8329 (fuente l. 261)

- **Pretende**: «Dentro del triángulo el proceso es estacionario; bajo la parábola… pseudo-ciclo»; con (1.40, −0.69)
  «sale un ciclo de unos 11 periodos». El comentario del código (fuente l. 337): «Un proceso no estacionario explota:
  verlo explotar es la lección».
- **Se ve**: el punto cae donde dicen los deslizadores en los 10 estados; la lectura da 11.05 periodos; en la raíz
  unitaria (0.5, 0.5) la serie deriva hasta −20 y en (1.4, −1.05) explota oscilando hasta ±7 600: bien.
- **Problemas**
  1. **[Alta]** **Con los procesos más explosivos la serie no explota: es una recta.** En (2.2, 1.2) el panel dibuja una
     línea horizontal en −1 000 000 (los 160 valores iguales); en (−2.2, −1.2) un bloque rojo que salta entre ±1 000 000.
     La explosión ocurre en los 200 pasos de calentamiento que `simularARMA` descarta, y el tope de ±10⁶ la aplana: lo
     que se ve es una serie *constante*, lo contrario de lo que el simulador quiere enseñar. Común 1.
     `…/m2-triangulo-ar2-fuera-max-2.2-1.2-1200.png`
  2. **[Media]** **A 800 y 375 px el eje φ₁ rotula solo `−2.4, 0, 2.4`**: los vértices ±2 del triángulo no tienen
     número, y −2.4/2.4 son los bordes del eje, no valores con sentido. A 1200 rotula `−2.4, −2.0, −1.5…2.0, 2.4` (el
     primer y el último paso son de 0.4). El eje y, `−1.3, −1.0, …, 1.0, 1.3`. Común 4.
  3. **[Media]** A 375 px la leyenda ocupa **3 líneas (73 px)** de un lienzo de 257 y el área queda en 160 × 134 px:
     el triángulo sale alto y estrecho. A 800, 2 líneas.
  4. **[Baja]** Los ejes de este gráfico (hecho a mano con `new Chart`, no con los ayudantes) escriben el menos con
     guion (`-1.3`, `-2.4`) y la lectura también (`φ₂ − φ₁ = -2.090`). Común 7.
  5. **[Baja]** En (2.2, 1.2) y (−2.2, −1.2) el punto (radio 8 + borde 2) queda a menos de su radio del borde del área.
  6. **[Baja]** La leyenda dibuja el punto (φ₁, φ₂) como rectángulo, y su color (naranja o rojo) cambia con el estado
     sin que nada lo explique.
- Capturas: `…/m2-triangulo-ar2-{ruido,ar2comp-1.40-0.75,casi-raiz-0.50-0.49,raiz-unitaria-0.50-0.50,borde-phi2-1,`
  `esquina-2.0-1.0,fuera-max-2.2-1.2,fuera-min-2.2-1.2,fuera-complejo-1.4-1.05}-{1200,800,375}.png`, `…/m2-vista2-375.png`

## M3 · `panel-ma-teorico` — canvas HTML l. 3338, 3342 (fuente l. 665, 669) · JS HTML l. 8441 (fuente l. 373)

- **Pretende**: «es la ACF la que se corta en seco tras el rezago $q$, y la PACF la que decae sin fin».
- **Se ve**: exactamente eso en los tres procesos; ρ₁ = 0.4878 y −0.4878, ρ₁ = 0.5526 en el MA(2), como la lectura.
- **Problemas**
  1. **[Media]** Mismo eje que el M2: a 800/375 los rezagos 1 y 2 sin número; en el MA(2) hay que contar barras para
     ver dónde se corta (común 2).
- Capturas: `…/m3-panel-ma-teorico-{ma1_pos,ma1_neg,ma2}-{1200,800,375}.png`

## M3 · `rho1-theta-ma1` — canvas HTML l. 3377 (fuente l. 704) · JS HTML l. 8482 (fuente l. 414)

- **Pretende**: el rombo 1/θ «queda siempre a la misma altura»; «Ninguno sobrepasa las líneas de ±0.5»; «prueba θ = 1,
  donde la pareja se funde en un solo punto sobre la cota».
- **Se ve**: la misma altura en los 9 estados (comprobado en píxeles); con θ = ±1 los dos puntos coinciden sobre la
  cota; con θ = 0.05 el rombo cae fuera (1/θ = 20) y la lectura lo dice. Bien.
- **Problemas**
  1. **[Media]** **A 800 y 375 px el eje θ rotula solo `−5, 0, 5`**: el ±1, que es la frontera de invertibilidad y el
     valor que la intro manda probar, no tiene número, y la zona |θ| < 1 ocupa 32 px de 161 a 375. Común 4.
  2. **[Media]** **El eje ρ₁ rotula `−0.7, −0.4, −0.2, 0, 0.2, 0.4, 0.7`** (pasos de 0.3, 0.2 y 0.3): la cota ±0.5, que
     es el objeto del gráfico, no tiene número. Común 4.
  3. **[Baja]** Con θ = ±5 el círculo queda cortado por la mitad en el borde del área.
  4. **[Baja]** Los colores de θ y 1/θ se intercambian (turquesa = invertible, rojo = no) y la leyenda los dibuja con
     el color del estado, sin decir qué significa cada uno; lo explica solo la intro. Menos con guion en los ejes
     (común 7).
- Capturas: `…/m3-rho1-theta-ma1-theta{0,0.05,0.20,0.50,1,-1,5,-5,-0.25}-{1200,800,375}.png`

## M4 · `dualidad-psi-pi` — canvas HTML l. 3637, 3641 (fuente l. 964, 968) · JS HTML l. 8611 (fuente l. 543)

- **Pretende**: con φ = 0.8, θ = 0, «solo sobreviven π₀ = 1 y π₁ = −0.8»; «Lleva ahora θ más allá de 1… y mira lo que
  les pasa a los π»; la nota: «Los pesos π crecen sin límite».
- **Se ve**: lo primero, exacto; con φ = 0.5, θ = −0.5 se queda solo la barra de j = 0 (la redundancia que cita el M5);
  con θ = 1.05 los π crecen de 1.85 a 3.16 y con θ = 2 hasta 6 041.6, y la escala se abre (±10 000). Var a h pasos:
  1.0000 con h = 1, 2.7647 con h = 12 frente al límite 2.7778: bien.
- **Problemas**
  1. **[Media]** **Con θ = 1 la lectura dice «los pesos crecen: no invertible» y el gráfico muestra pesos que no
     crecen**: π alterna ±1.8 en los 12 rezagos (máx |πⱼ| = 1.8000). La frontera |θ| = 1 no es invertible, pero sus π
     no divergen; la frase es la de |θ| > 1 (fuente l. 589).
  2. **[Media]** Con θ = 2 la escala ±10 000 la fija π₁₂ = 6 041.6 y los once primeros pesos (|π| ≤ 3 020) no se ven
     o son una raya: se ve que «explota», no cómo crece.
  3. **[Baja]** El gris de los ψ que no entran en la varianza a h pasos no está en la leyenda (su muestra toma el color
     de la primera barra).
- Capturas: `…/m4-dualidad-psi-pi-{ar1-0.8-h1,ar1-0.8-h12,redundante-0.5-0.5,theta1-frontera,theta1.05,`
  `theta2-phi0.95,theta-2-phi-0.95,phi0.95-theta0}-{1200,800,375}.png`

## M5 · `laboratorio-arma` — canvas HTML l. 4302 (serie), 4306 (ACF), 4310 (PACF) (fuente l. 1629, 1633, 1637) · JS HTML l. 8677 (fuente l. 609; `correlogramaDoble` l. 184, `simularARMA` l. 155)

- **Pretende**: con T = 60 «el patrón teórico casi no se reconoce», con T = 1000 «emerge limpio»; banda ±0.253 y ±0.062;
  «Otra realización» cambia la muestra y no la teoría; con φ₁ = 0.5, θ₁ = −0.5 la ACF teórica es cero, con θ₁ = −0.45
  «casi».
- **Se ve**: todo eso. Bandas 0.2530 / 0.1386 / 0.0620; distancia media 0.2596 (T = 60), 0.0548 (200), 0.0158 (1000);
  redundante: ACF teórica 0 en los 16 rezagos; con −0.45, 0.0515 en el rezago 1; la realización 2 da otra muestra.
- **Problemas**
  1. **[Alta]** **Con φ₁ = 1.5 (o todo al máximo) la serie es una recta en 1 000 000 y los dos correlogramas se quedan
     vacíos**: la ACF y la PACF muestrales salen NaN (varianza cero de una serie constante) y Chart.js no dibuja nada.
     Lo que el estudiante ve es una línea plana y dos correlogramas en blanco. Común 1.
     `…/m5-laboratorio-arma-phi1-1.5-375.png`, `…-max-todo-…`
  2. **[Media]** **Cuando el proceso no es estacionario, la «ACF teórica» se dibuja como ceros** (fuente l. 639-640) y la
     leyenda sigue diciendo «ACF teórica»: el gráfico dice «ruido blanco» mientras la lectura dice «la ACF teórica no
     existe». Con φ₁ = 1 se ve la muestral en 0.96 → 0.41 junto a una teórica plana en cero.
  3. **[Media]** **Correlogramas de 65 px de alto a 800 y 68 a 375**: la leyenda de tres entradas pasa a dos líneas
     (52 px) en un lienzo de 164. La banda ±0.14 queda a 5 px del cero. Común 3.
  4. **[Media]** **La barra muestral `rgba(255,102,0,0.5)` tiene 1.75:1 sobre blanco** (y 2.13:1 frente a la banda, que es
     del mismo naranja). Barras de 2.2-2.7 px a 375/800. Común 5.
  5. **[Baja]** Con el proceso no estacionario la muestra de la leyenda de la serie sale verde oscuro con borde rojo: se
     cambia `borderColor` y no `backgroundColor`. El eje y de la recta rotula `940 000…1 060 000` sin el 1 000 000 en que
     está la línea.
- Capturas: `…/m5-laboratorio-arma-{T60,T1000,redundante-0.5-0.5,casi-redundante-0.5-0.45,phi1-1.0,phi1-1.5,`
  `phi1-0.95-T1000,ar2-1.5-0.95,ma-no-invertible-1.5,max-todo,inicial-otra-realizacion}-{1200,800,375}.png`,
  `…/m5-vista1-375.png`

## M6 · `teorica-vs-muestral` — canvas HTML l. 4519, 4523 (fuente l. 1846, 1850) · JS HTML l. 8770 (fuente l. 702)

- **Pretende**: «la muestra pone ahí valores pequeños pero no nulos, y alguno se asoma fuera de la banda».
- **Se ve**: las cifras de la lectura coinciden con lo dibujado (MA(1): 15 rezagos con ACF teórica nula, 2 fuera: 0.150
  en el 6 y −0.151 en el 15, banda 0.1386).
- **Problemas**
  1. **[Media]** **Lo que la intro pide mirar no se distingue**: las dos barras que «se asoman» superan la banda en
     0.012, unos 0.6 px a 1200 (escala fija ±1, área de 95 px; 75 px a 800). Es la decisión de la escala fija que el
     cap. 2 ya anotó, pero aquí la intro descansa en ella.
  2. **[Media]** Mismo color muestral de 1.75:1 y leyenda en dos líneas a 800/375 (comunes 3 y 5).
  3. **[Baja]** La lectura escribe el proceso con el nombre de R («MA(1), theta = 0.8», «phi = 0.7») mientras el selector
     dice «θ = 0.8».
- Capturas: `…/m6-teorica-vs-muestral-{ar1_pos,ma1_pos,arma11}-{1200,800,375}.png`

## M7 · `manchas-identificacion` — canvas HTML l. 4578, 4582, 4586 (fuente l. 1905, 1909, 1913) · JS HTML l. 8823 (fuente l. 755)

- **Pretende**: «La PACF tiene dos picos grandes (0.806 y −0.634) y a partir del tercero se mete dentro de la banda
  ±0.196. La ACF… ondula y cruza el cero».
- **Se ve**: exactamente eso (PACF máxima fuera del 2: 0.174 en el 6, dentro). Lectura coherente.
- **Problemas**
  1. **[Baja]** Serie anual con un ciclo de unos 11 años: a 375 px el eje de rezagos rotula `3, 6, 9, 12…` (divisores de
     12, pensados para series mensuales) y deja sin número el 10-11 donde la ACF vuelve a subir (0.411). Común 2.
  2. **[Baja]** La lectura escribe `-0.634` con guion (común 7).
- Capturas: `…/m7-manchas-identificacion-{1200,800,375}.png`, `…/m7-vista1-375.png`

## M8 · `diagnostico-residuales` — canvas HTML l. 4945, 4949, 4953 (fuente l. 2267, 2271, 2275) · JS HTML l. 8849 (fuente l. 781)

- **Pretende**: «Observa que su $p$-valor de Ljung–Box en el rezago 12 se queda **justo por debajo** de 0.05».
- **Se ve**: lecturas coherentes con las barras (8, 0, 0 y 2 de 20 fuera de la banda; p(12) = 0.0000, 0.0461, 0.1658,
  0.2246, como la tabla de la prosa).
- **Problemas**
  1. **[Alta]** **El panel de Ljung–Box no deja ver lo que la intro manda observar.** En un eje 0-1 de 75 px, el nivel
     0.05 está a 3.7 px del cero y el p = 0.0461 a 3.5: la diferencia es **0.3 px** a 1200 y 800, 0.2 a 375. Las barras
     de 3, 4 y 12 (todas bajo 0.05) son indistinguibles de las de 5, 6 y 11 (sobre 0.05).
     `…/m8-diagnostico-residuales-arma20-1200.png`
  2. **[Media]** **Con el AR(1) el panel de Ljung–Box está vacío**: los 19 p-valores son 0 y no hay barra que dibujar. El
     caso más claro de rechazo se ve como «sin datos». Un eje logarítmico (o −log₁₀ p con la recta en 1.30) arregla 1 y 2.
  3. **[Media]** Las barras de la ACF de residuales salen **rojas cuando Ljung–Box(12) rechaza** (fuente l. 811-812): en el
     AR(2) las 20 barras están dentro de la banda y son rojas. Nada en la leyenda ni en la intro dice qué significa el
     rojo.
  4. **[Media]** A 375 px la ACF y el Ljung–Box tienen **58 px de alto** (leyenda en dos líneas en lienzos de 157); el eje
     de la ACF rotula `−1, 0, 1`. El selector corta su texto («…la identificació»). Común 3.
  5. **[Baja]** El eje del p-valor rotula `0.0, 0.4, 0.8` a 1200/800: ni el 1.0 ni el 0.05 que importa.
- Capturas: `…/m8-diagnostico-residuales-{arma10,arma20,arma30,arma21}-{1200,800,375}.png`, `…/m8-vista1-375.png`

## M9 · `manchas-transformada` — canvas HTML l. 5215, 5219 (fuente l. 2537, 2541) · JS HTML l. 8920 (fuente l. 852)

- **Pretende**: «En la raíz, los ciclos se parecen mucho más entre sí y la PACF se corta más limpiamente en el
  rezago 2».
- **Se ve**: los ciclos, sí. La lectura da PACF(3), PACF(4) = 0.0334, −0.0155 en la raíz frente a 0.0767, −0.0587.
- **Problemas**
  1. **[Alta]** **La PACF de la raíz no se corta más limpiamente: tiene tres barras más allá del 2 que tocan o cruzan la
     banda ±0.196** —0.2003 (rezago 6), 0.1978 (9) y −0.1991 (16)— y la de la serie cruda ninguna (la mayor, 0.174 en el
     6). El dibujo dice lo contrario de la intro; la afirmación solo se sostiene mirando los rezagos 3 y 4, que es lo que
     da la lectura. O se acota la frase («en los rezagos 3 y 4») o se dice que aparecen esos tres picos marginales.
     `…/m9-manchas-transformada-raiz-1200.png`
  2. **[Baja]** El panel de la serie no lleva `grafico-etiqueta` ni unidad (el de la PACF sí).
- Capturas: `…/m9-manchas-transformada-{cruda,raiz}-{1200,800,375}.png`, `…/m9-vista1-375.png`

## M9 · `manchas-impulso` — canvas HTML l. 5438 (ψ), 5442 (abanico) (fuente l. 2760, 2764) · JS HTML l. 8982 (fuente l. 914)

- **Pretende**: «Los pesos $\psi_j$ de la tabla, con el envolvente $\pm 0.8278^{\,j}$ que los amortigua»; el semiancho
  «se detiene en ±5.62, y a los seis años ya ha recorrido el 94 %».
- **Se ve**: el abanico, bien: barra de h = 6 = 5.2868 = «±5.29» de la lectura; techo 5.6225 = «±5.62»; 94 % con h = 6,
  40 % con h = 1, 99 % con h = 11.
- **Problemas**
  1. **[Alta]** **Los ψ se salen del envolvente que «los amortigua»: 16 de las 25 barras** (j = 1, 2, 3, 6-9, 12-14,
     17-20, 23, 24). ψ₁ = 1.403 frente a 0.828, ψ₂ = 1.282 frente a 0.685, ψ₇ = −0.488 frente a 0.266. ±R^j da la
     *tasa* de amortiguamiento, no la cota: con raíces complejas ψⱼ = Rʲ·sen((j+1)ω)/sen ω, y la cota es ±Rʲ/sen ω.
     (Con los φ de la página, 1/sen ω ≈ 1.88: cálculo de diagnóstico; la cifra que se publique ha de salir de
     `genera_cap3.R`.) `…/m9-manchas-impulso-1200.png`
  2. **[Media]** Abanico de **65 px de alto a 800 y 68 a 375** (leyenda en dos líneas). Común 3.
  3. **[Baja]** La leyenda dice «±(0.83)ʲ» y la intro y la lectura 0.8278. La barra del horizonte elegido va en el
     mismo naranja que la recta del techo.
  4. **[Baja]** Los ψ que dibuja el navegador (desde φ redondeados a 4 decimales) difieren de la tabla de al lado en la
     cuarta cifra: 1.2823 frente a 1.2822, 0.8374 frente a 0.8372, −0.4256 frente a −0.4257 (la intro dice «los pesos de
     la tabla»; se nota en el tooltip).
- Capturas: `…/m9-manchas-impulso-{h1,h6,h11,h24}-{1200,800,375}.png`, `…/m9-vista2-375.png`

## M9 · `trm-retornos` — canvas HTML l. 5518, 5522, 5526 (fuente l. 2840, 2844, 2848) · JS HTML l. 9067 (fuente l. 999)

- **Pretende**: banda ±0.1675; «solo asoman dos barras, el rezago 5 (0.193) y el rezago 8 (−0.198)».
- **Se ve**: eso, y la lectura «2 de 20» y Ljung–Box(12) p = 0.0601 coinciden. Fechas por eneros (`2016…2026`; a 375
  `2016, 2019, 2022, 2025`). Serie mensual con el 12 rotulado a los tres anchos (no llega a 24: 20 rezagos).
- **Problemas**
  1. **[Baja]** Serie en `#FB6400` (3.03:1, al límite) y correlogramas de 81-84 px a 800/375. Sin título del eje y (%
     solo en la leyenda).
- Capturas: `…/m9-trm-retornos-{1200,800,375}.png`, `…/m9-vista3-375.png`

## M10 · gráficos del quiz (preguntas 3 y 9) — creados por JS (HTML l. 7595); preguntas HTML l. 9165 y 9290 (fuente l. 1097 y 1222)

- **Pretende**: P3, «Cuenta cuántas barras hay antes de que la función se haga exactamente cero»; P9, «mira cuánto se
  salen las barras de la banda».
- **Se ve (1200)**: los dos rasgos; banda 0.196, r₁ = 0.556 como la retroalimentación.
- **Problemas**
  1. **[Media]** **Los `aria-label` dan la respuesta**: P3 «…que vale 0.5526 y 0.2632 y después es exactamente cero» (el
     corte tras el rezago 2 es lo que la pregunta pide leer); P9 «…con varias barras muy fuera de la banda». Es el
     defecto del cap. 2, sin arreglar en el 3.
  2. **[Media]** P3 a 375 px rotula `3, 6, 9, 12, 15` y a 800 `2, 4…`: el 1 nunca tiene número en la pregunta que
     consiste en contar las primeras barras (común 2).
  3. **[Baja]** P9 pinta las barras en rojo `#dc2626`: el color ya sugiere «mal ajuste» antes de leer nada. A 375 la
     leyenda pasa a dos líneas y el área baja a 82 px.
- Capturas: `…/m10-quiz-grafico{1,2}-{1200,800,375}.png`, `…/m10-vista{1,2}-375.png`

## M11 · `cap3-simulacro`

- Sin gráficos. Ningún desbordamiento a ningún ancho (`sw = cw`), ninguna fórmula cortada. `…/m11-cap3-simulacro-375.png`

---

## Fórmulas y tablas

- **Ninguna fórmula en bloque desborda** a 1200, 800 ni 375 (0 casos; los «desbordes» que da el barrido son el MathML
  oculto de KaTeX y bloques de código dentro de su `<pre>` desplazable).
- **Ninguna tabla queda cortada por `<main>`** (`recortados` vacío en los 33 casos). Las 10 tablas que no caben
  (`tabla-ancha`) se desplazan con el desvanecido de `ajustarTablas`; p. ej. la de los ψ del M9 a 375
  (`…/m9-tabla2-375.png`). La cabecera «h = j + 1» se parte en tres renglones a 375: acabado, fuera de esta lente.

## Defectos que comparten causa (arreglo de una sola vez)

1. **El tope de ±10⁶ después de 200 pasos de calentamiento aplana lo explosivo** — `simularARMA` (fuente l. 155-169,
   solo `cap3_js.js`). Un proceso explosivo satura en el calentamiento y la parte visible es constante (triángulo, M2 1)
   o constante con correlogramas NaN y vacíos (laboratorio, M5 1). Arreglo: sin calentamiento cuando el proceso no es
   estacionario (que se vea despegar desde 0), cortar la serie en el primer valor que pase un umbral, y no dibujar la ACF
   muestral si la varianza es 0 (con un aviso). Junto con esto, ocultar el conjunto «ACF teórica» cuando no existe (M5 2)
   en vez de dibujar ceros.
2. **El rezago 1 nunca se rotula a 800 y 375 px** — `marcasLegibles` (HTML l. 6853, armazón compartido 2 → 6): solo
   antepone el primer valor si `marcas.length < caben`, y casi nunca sobra sitio. En este capítulo es grave porque la
   identificación vive en los rezagos 1-2 (M2, M3, quiz P3). Arreglo: reservar siempre el 1 (quitar una marca intermedia
   si hace falta: `1, 4, 8, 12, 16` o `1, 6, 12, 18`). Para series anuales (manchas), `opciones.rezagos` podría pedir
   pasos de 5.
3. **Áreas de dibujo de 58-68 px** — alturas fijas en línea en `cap3_modulos.html` (170-200 px) más una leyenda que a
   800/375 pasa a dos o tres líneas (52-73 px) y el título del eje x. Afecta a laboratorio, teórica-muestral, diagnóstico,
   abanico, quiz P9 y triángulo. Arreglo en el cap. 3 (alturas mayores bajo 640 px de contenedor) o en el armazón
   (`legend.labels` más compactas, o la banda fuera de la leyenda y explicada en la `grafico-etiqueta`).
4. **Ejes hechos a mano en los dos gráficos de dispersión** — `triangulo-ar2` y `rho1-theta-ma1` (fuente l. 304 y
   468, solo `cap3_js.js`) fijan `min/max` (±2.4, ±1.3, ±5, ±0.7) sin `stepSize` ni callback: Chart.js rotula los
   bordes con pasos desiguales, a 800/375 solo `−2.4, 0, 2.4` y `−5, 0, 5`, y faltan los valores con sentido (±2, ±1,
   ±0.5). Arreglo: `ticks.stepSize` (0.5 / 1 / 0.25) con `afterBuildTicks` que garantice ±2, ±1 y ±0.5, y el
   `rotuloVertical` de los ayudantes para el signo menos.
5. **Color de la muestral** — `correlogramaDoble` (fuente l. 191, solo cap. 3) usa el naranja de marca al 50 %
   (`rgba(255,102,0,0.5)`, 1.75:1) en lugar de un tono de `COLORES_GRAFICO`; además comparte familia con la banda. Un
   gris de 3:1 (`COLORES_GRAFICO.gris`) o un turquesa claro con borde lo resolverían.
6. **Paneles que no pueden mostrar el valor que la prosa señala** — Ljung–Box en 0-1 (M8 1-2), ±1 fijo para «asomarse»
   (M6 1), ±10 000 para los π (M4 2). Mismo criterio: la escala tiene que hacer visible la comparación que se pide.
7. **Formato de cifras en lecturas y en los ejes hechos a mano** — `actualizarLectura` (HTML l. 7407, armazón) no cambia
   el guion por «−» (`-2.090`, `-0.634`, `-0.0155`); los dos gráficos de dispersión tampoco. Es el común 10 del cap. 2,
   sin hacer.
8. **`aria-label` fijos o que responden** — 21 de los 27 lienzos de simulador cambian de contenido y todos llevan una etiqueta fija
   («…del proceso seleccionado», «…en la escala seleccionada», «(phi1, phi2)» en ASCII); los dos del quiz dan la
   respuesta. Las lecturas sí se anuncian (región viva común). Arreglo: reescribir `aria-label` en cada `pintar()` con
   el proceso y el parámetro; describir en el quiz el gráfico sin el diagnóstico.
9. **Afirmaciones de la prosa que el dibujo no sostiene** — M9 «se corta más limpiamente» (PACF de la raíz), M9 «el
   envolvente que los amortigua», M4 «los pesos crecen» con θ = 1, M2 «cae a cero en el rezago p». Son cuatro
   correcciones de texto o de dibujo, cada una en su sitio; las cifras que se añadan han de salir de R.

## Lo que está bien resuelto

- **Bandas**: ±1.96/√n con la n de lo que se dibuja (0.1386 con T = 200, 0.196 con n = 100, 0.1675 con n = 137, 0.253 y
  0.062 con T = 60 y 1000), recalculadas al mover T; coinciden con lecturas, prosa y retroalimentaciones.
- **Lecturas = dibujo** en los 71 estados revisados (13 iniciales y 58 extremos) salvo los anotados: ρ₁, PACF(p+1), barras fuera de la banda,
  Ljung–Box(12), semiancho y techo, ψ₁₂ y π₁₂, suma de ψ² frente al límite.
- **El 12 rotulado** en todos los correlogramas a los tres anchos; el 0 siempre en el eje y; rejilla del 0 oscura.
- Ningún solape de rótulos del eje x; ninguna fuente de respaldo; ningún desborde horizontal de la página
  (`scrollWidth` = ancho de la ventana en los 33 casos); ninguna fórmula ni tabla cortada.
- Controles en una columna de 308 px a 800 px (el común 3 del cap. 2, resuelto aquí).
- La redundancia φ = 0.5, θ = −0.5 se ve igual en el M4 (solo j = 0) y en el M5 (ACF teórica nula), como dice la prosa.

## Lo que no se miró, y por qué

- **Tooltips**: no simulados.
- **Teclado**: no se probaron los controles con teclas.
- **Modo oscuro / impresión**: fuera de la revisión.
- **Fuentes lentas** (escenario de `cap2/diag/fuentes.js`): no se repitió; `fuentesDeLosLienzos` es la misma del cap. 2.
- De las 264 capturas se abrieron unas 15 (los estados problemáticos a 1200 y 375, y el laboratorio a 800); el resto
  son estados ya vistos a otro ancho y sus medidas están en `graficas_medidas.json` y `graficas_resumen.out`.
