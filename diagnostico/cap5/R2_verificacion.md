# R2 · Verificación independiente · Capítulo 5 «Modelos SARIMA» · gráficas y simuladores

Verificador que no redactó la ronda. Base `e084436`; objeto: el diff sin commit (13 archivos). Fecha: 2026-11-24. No se editó ningún
archivo del repo fuera de este informe, `diagnostico/cap5/comprobaciones/v2_*` y `diagnostico/cap5/capturas/v2/`. El informe del
redactor (`R2_cambios.md`) se leyó solo al final, para la última sección.

**Cómo.** Servidores propios: `python3 -m http.server 8769` sobre `Htmls_Series/` (md5 por HTTP = md5 en disco), 8770 sobre `plantilla/`
y 8771 sobre una copia de HEAD (caps. 1 y 5 y plantilla) para el «antes». Chrome sin ventana por CDP en 9281, con el cliente
`diag/chrome.js`. Todo cerrado al terminar. Cifras recalculadas en R 4.6.0 con forecast 9.0.2.

| guion | salida | qué hace |
|---|---|---|
| `v2_solo_componente.py` | `v2_solo_componente.out` | recorta en HEAD y en el árbol los bloques CSS y JS del componente y compara el resto |
| `v2_mapas.js` | `v2_mapas.json`, `v2_mapas.log` | los mapas del cap. 1 (M3), del cap. 5 (M1, los 32 estados; M3, los 8) y de la plantilla, a 1200, 800 y 375 px (375 con `mobile:true`, dsf 2), en el árbol y en HEAD: contraste de cada cifra visible, meses sin desplazar, ajuste aplicado, guiones, filas ARIA, nombre accesible; árbol de accesibilidad de Chrome; ratón, toque (`Input.dispatchTouchEvent`) y Tab |
| `v2_mapas_resumen.py` | `v2_mapas_resumen.out` | resumen de lo anterior |
| `v2_revisa.js` | `v2_medidas.json`, `v2_revisa.log` | copia adaptada de `diag/graficas_revisa.js`: los 14 simuladores y el quiz en los estados del informe (más «8 métodos + MAPE») a los tres anchos; añade la detección de entradas de leyenda cortadas |
| `v2_resumen.py` | `v2_resumen.out` | áreas, leyendas, ejes, `aria-label` y lecturas por estado |
| `v2_consola.js` | `v2_consola.json`, `v2_consola.out` | consola y lienzos de los caps. 1–6 y la guía, módulo a módulo, a 1200 y 375 px; el icono del M11; el quiz de HEAD frente al del árbol; el mapa del M1 al cerrar la barra lateral y al cambiar el ancho |
| `v2_regresiones.py` | `v2_regresiones.out` | bloques `<pre>`, orden de módulos, registro del quiz en la fuente, `simulacro.js` |
| `v2_cifras.R` | `v2_cifras.out` | la fila nueva del M6, las 32 ACF del M1 (y dónde salta la nota nueva), el IC del M7, ψ y σₕ del M5, el quiz, las Pascuas, el `aria-label` del M6 |
| `v2_colores_m11.py` | `v2_colores_m11.out` | CIEDE2000 entre las líneas del M11, antes y ahora |
| — | `v2_verifica_todo.out`, `v2_tailwind.out`, `v2_verifica_cifras_deck.out`, `v2_sin_literales.out`, `v2_bloques_cap5.out` | los cinco verificadores pedidos |

Capturas en `diagnostico/cap5/capturas/v2/` (`mapa-*` y `antes-mapa-*` del componente; `mN-<simulador>-<estado>-<ancho>.png` del resto).

---

## 1. Problemas encontrados

Gravedad como en `graficas.md`: **Alta** = el gráfico o la lectura dicen otra cosa que la prosa; **Media** = cuesta leerlo o deja fuera a
alguien; **Baja** = acabado.

| # | Grav. | Problema | Fuente | Cómo reproducirlo | Corrección propuesta | Lo que hizo la sesión maestra |
|---|---|---|---|---|---|---|
| V1 | **Alta** | **La nota nueva de la lectura del M1 contradice al M7 en la serie central.** «(negativo tras ∇₁₂: huella de la propia diferencia, no estacionalidad que quede)» salta en 10 de los 32 estados (los mismos en R y en la página, `v2_cifras.out` §2 y `v2_resumen.out`): las 4 de la TRM con $D = 1$, pero también AirPassengers log con ∇₁₂ y con ∇∇₁₂, co2 con ∇∇₁₂ (con y sin log) y USAccDeaths con ∇∇₁₂ (con y sin log). Con log y ∇∇₁₂, ρ̂₁₂ = −0.3866 es justo la barra que la tabla del M7 lee como «El pico estacional: pide $Q = 1$» y que el *airline* recoge con Θ̂ = −0.5569 (e.e. 0.0731; IC 95 % [−0.7002, −0.4137], que no toca −1: no es sobrediferenciación). Decirle al estudiante que es «huella de la propia diferencia, no estacionalidad que quede» en la serie del capítulo le enseña a ignorar la barra que identifica $Q$. Solo es exacta con la TRM y ∇∇₁₂ (una caminata con ∇∇₁₂ da ρ₁₂ = −0.5, `v2_cifras.out`). | `ensamblado/cap5/chapter.js` l. 325 (`negativos`) y l. 336 (el texto) | M1: AirPassengers, logaritmo, «Ambas: ∇ ∇₁₂»; lectura, renglón «múltiplos de 12 fuera de banda» | Quitar la glosa de la lectura y, si se quiere conservar la idea, ligarla a la escala de −0.5: por ejemplo «12 (negativo tras ∇₁₂: lo recoge un MA estacional, Módulos 4 y 7; cerca de −0.5, señal de que la diferencia sobra, Módulo 3)», o mostrar la glosa de la TRM solo con `params.serie === 'trm'`. Que la vea el par académico | corregido por el redactor a petición de la maestra: glosa retirada; la lectura del M1 da solo las cifras («múltiplos de 12 fuera de banda» / «otros rezagos fuera de banda»), sin interpretación |
| V2 | Media | **Con el mapa sin cifras, el teclado no llega a ningún valor.** A 800 y 375 px las celdas van solo con color y la línea del valor responde a `pointerover` y `click`; ninguna celda es enfocable (0) y Tab salta del último control del simulador a la tabla siguiente (`v2_mapas_resumen.out`, «interacciones»). Ratón y toque sí funcionan (la línea da «Jul 2016: −197.6», «Mar 2026: 36.3»). El lector de pantalla no pierde nada (cada celda lleva su `aria-label`), pero quien navega con teclado y ve la pantalla se queda sin valores, que antes leía desplazando. | `ensamblado/componentes/mapa_estacional.js` l. 189–214 (`prepararLecturaMapa`), l. 116–119 (celdas sin `tabindex`) | M1 a 800 px, estado inicial: Tab desde «Tomar logaritmo» | Una sola parada de tabulación en la rejilla (`tabindex="0"` en la celda activa, `-1` en las demás) con flechas para moverse, y `focusin` que escriba la línea del valor; o un botón «ver las cifras» que vuelva a la rejilla desplazable | corregido por el redactor a petición de la maestra: sin cifras, la rejilla es una sola parada del tabulador con foco visible; flechas, Inicio y Fin mueven la celda señalada y la línea del valor (`r2_mapa_teclado.out`) |
| V3 | Media | **A 800 px el M1 se queda sin cifras en 23 de sus 32 estados, también en el inicial, y la plantilla en su único estado.** Antes se veían todas desplazando (6 meses a la vista); ahora se ven los 12 meses, pero ninguna cifra salvo con AirPassengers sin log y sin diferenciar (co2 nunca las tuvo). 800 px es el ancho de una tableta o portátil pequeño con la barra lateral abierta: la celda mide 19.5 px. La leyenda solo da los extremos. Es una decisión de diseño razonable para ver las bandas, pero pierde información respecto de HEAD y el informe del redactor la cuenta como arreglo completo. | `ensamblado/componentes/mapa_estacional.css` l. 39–44 y 159–168; `.js` l. 168–186 | `v2_mapas_resumen.out`: «estados con cifras ocultas»; capturas `mapa-cap5-mapa-firma-airpassengers-log-ninguna-800.png` frente a `antes-…-800.png` | Llevar al componente lo que ya funciona en el cap. 1 (variante `--entero`: columna del año más estrecha y cuerpo en `cqw`, que a 375 px conserva sus 144 cifras), y en modo estrecho escribir un decimal menos; dejar el modo sin cifras solo para lo que siga sin caber | corregido por el redactor a petición de la maestra: botón «Ver las cifras» (`aria-pressed`, teclado) que pasa a la rejilla con cifras desplazable, con degradado y flecha en el borde derecho mientras quedan meses; el estado inicial a 800 px sigue siendo el de color |
| V4 | Baja | **El paso «cifras chicas» no se activa nunca.** En los 130 casos mapa × estado × ancho medidos, 0 lo usan: a ≤ 640 px la celda ya tiene `font-size: 0.55rem` (el mismo cuerpo que el paso intermedio) y a 800 px la cifra no cabe ni así. | `mapa_estacional.css` l. 94–95 y l. 166; `.js` l. 179–185 | `v2_mapas_resumen.out`, «estados con cifras chicas»: vacío | Darle un cuerpo menor real o quitar el paso | corregido por el redactor a petición de la maestra: el paso «cifras chicas» se quitó |
| V5 | Baja | **El nombre accesible del mapa de la tienda no dice el escenario ni la resta.** No pasa `descripcion` y usa el título fijo: «La tienda inventada, mes × año: 3 años (2023–2025) … valores de 12 a 12» es igual en «crece una unidad» que en otra combinación con el mismo rango. Solo el M1 dice serie y transformación (E.4, en parte). | `ensamblado/cap5/chapter.js` l. 575–583 | M3, cualquier cambio de los dos selectores; `v2_mapas_resumen.out`, «nombres accesibles» | `descripcion: 'La tienda inventada (' + ESCENARIOS[params.escenario].toLowerCase() + '), ' + r.texto` | corregido por el redactor a petición de la maestra: el nombre accesible del mapa de la tienda dice escenario y resta |
| V6 | Baja | **Los `aria-label` de `cuatro-combinaciones` no nombran la serie ni el operador:** «Serie Ambas diferencias, de 1950-02 a 1960-12 (n = 131)…» y «ACF muestral de Ambas diferencias…». `R2_cambios.md` afirma que dice «Serie ∇∇₁₂ log(AirPassengers)…»: no es lo que escribe la página (la etiqueta sale de `DATOS_CAP5…combinaciones[*].etiqueta`). | `chapter.js` l. 646–648 | M3, «Las cuatro combinaciones», cualquier estado; `v2_resumen.out` | Componer el nombre con `c.d` y `c.D`: «∇ ∇₁₂ log(AirPassengers)», como hace el M3 de la sobrediferenciación | corregido por el redactor a petición de la maestra: «∇ ∇₁₂ log(AirPassengers)» compuesto con `c.d` y `c.D` en los dos `aria-label` |
| V7 | Baja | **El M9 sigue sin títulos de eje a 800 px**, no solo en el teléfono: `conTitulos` exige un marco de 420 px y a 800 px, con la barra lateral, mide menos. La leyenda nombra las series pero no dice cuál va en el eje derecho. `conTitulos` se evalúa al pintar, no al cambiar el ancho. | `chapter.js` l. 1102–1103 | M9 a 800 px: `v2_resumen.out`, «M9: ejes» (título `None` a 800 y 375) | Rótulo corto en el eje derecho («días») a todo ancho, o la entrada de la leyenda «Días del mes (eje derecho)» | corregido por el redactor a petición de la maestra: títulos cortos «log» y «días» a todo ancho y leyenda «Días del mes (eje derecho)» |
| V8 | Baja | **La intro del M7 describe el interruptor al revés del estado inicial.** «el interruptor pasa de la escala logarítmica a la original», pero se abre en escala original (interruptor «Escala original (en vez de logarítmica)» marcado) y con h = 24, que la intro no dice. Causa H. | `ensamblado/cap5/templates_7_9.html` l. 152–155; `params` en `chapter.js` l. 918 | M7 al abrir | «Se abre en escala original y a 24 meses; desmarca el interruptor para ver los logaritmos…» | corregido por el redactor a petición de la maestra: «Se abre en la escala original y con el horizonte al máximo… al desmarcar el interruptor se pasa a la escala logarítmica» |
| V9 | Baja | **La intro del M11 no dice el estado inicial** (lo observado y 4 métodos) ni lo que pasa con todo apagado (solo lo observado). Causa H. | `templates_10_11.html` l. 260–262 | M11 al abrir | Una frase: «Se abre con los cuatro mejores por RMSE; enciende los demás…» | corregido por el redactor a petición de la maestra: «Se abre con lo observado y los cuatro primeros métodos por RMSE; con todos apagados queda solo lo observado» |
| V10 | Baja | **Mapa: la cifra alterna pizarra, negro y blanco en celdas vecinas de tono parecido** (cap. 1 a 375 px, fila 1956: «413» en blanco junto a «405» en negro). Todas pasan 4.5:1; es acabado. | `mapa_estacional.js` l. 60–72 (`textoSobre`) | `capturas/v2/mapa-cap1-M3-unico-375.png` | Un solo oscuro (negro o `#0f172a`) en vez de pizarra + negro | corregido por el redactor a petición de la maestra: dos tonos, blanco o negro (peor caso 4.58:1) |

No se encontró ninguna cifra visible nueva que no coincida con R (§3), ningún error de consola, ningún lienzo en blanco, ningún bloque de
código tocado y ningún cambio de enunciado, opción, orden, clave ni retro del quiz.

---

## 2. Reproducibilidad y alcance

- `ensambla_cap5.py`, `ensambla_cap6.py` y `ensambla_proyecto.py` reejecutados: los md5 de los 1973 archivos de `Htmls_Series/`,
  `plantilla/`, `precalculo/`, `bibliografia/` y `ensamblado/` quedan **idénticos** y `git status` no cambia.
- `retropropaga_mapa.py --comprobar`: «AL DÍA» el cap. 1 y la plantilla, salida 0.
- **Solo el componente** (`v2_solo_componente.out`): recortados los dos bloques del componente, el resto del cap. 1, del cap. 6, de la
  plantilla y de la guía es idéntico a HEAD (0 líneas distintas en los cuatro). El cap. 5 cambia además en su JS y sus plantillas (445
  líneas fuera del componente), como corresponde.
- Los cinco verificadores pedidos, en verde: `verifica_todo.py` «11 verificadores en verde»; `compila_tailwind.py --comprobar` salida 0;
  `verifica_cifras_cap5.py` «774 · verificados: 774 … no coinciden: 0 … todo verificado y cubierto»; `sin_literales_diagnostico.py`
  «0 con coincidencias»; `verifica_bloques_cap6.py --html …cap5` «1335 de 1335 … 0 bloques con discrepancias». **Escrituras:**
  `verifica_cifras_cap5.py` reescribe `Htmls_Series/diapositivas/fuentes/verificacion/verificacion_cifras_cap5.md` con el mismo
  contenido (md5 igual, `git status` igual); ningún otro archivo del repo cambió.

## 3. Cifras nuevas, recalculadas en R (`v2_cifras.out`)

- **M6, fila (0,1,0)(0,1,0)₁₂**: AICc −434.7990, **BIC −431.9548**, **ρ̂₁₂ residual −0.3907** con los 144 residuales (la convención de
  las otras filas; sin los 13 primeros sería −0.3866), Ljung–Box(24) p = 2.31e-08 (< 10⁻⁴). La tabla (−431.95, −0.3907) es correcta.
  El `aria-label` del simulador con ese modelo («5 de 24 barras fuera de la banda ±0.163; la del rezago 1 vale −0.343») también.
- **M7**: ancho del IC 95 % en logaritmos: incremento de +0.0337 en h = 13 frente a +0.0119 en h = 12 y +0.0214 en h = 14. La intro
  nueva («se abre de forma continua —al cruzar el rezago estacional, en h = 13, se ensancha algo más deprisa, pero no a escalones
  visibles—») es verdad.
- **M1**: las 32 combinaciones de ρ̂₁, ρ̂₁₂, ρ̂₂₄, ρ̂₃₆, banda y rezagos fuera coinciden con las lecturas y los `aria-label`; la TRM sin log
  y con ∇ da 0.0876 / −0.0025 / −0.0672 / 0.0714 y banda 0.1675, la última fila de la tabla con un decimal más, como dice la intro. La nota
  nueva: ver V1.
- **M5** (`aria-label` nuevos): con θ = −0.40 y Θ = −0.56, ψ₁ 0.600, ψ₁₁ 0.600, ψ₁₂ 1.040, salto 0.440, ψ₂₄ 1.304, ψ₃₅ 1.128 y σ₁ 0.0370,
  σ₁₂ 0.0825, σ₂₄ 0.1398, σ₃₆ 0.2026; con θ = Θ = −0.95, σ de 0.0370 a 0.0390. Igual que la página.
- **Quiz**: la ACF de un SAR(1)₁₂ con Φ = 0.7 tiene 0.70, 0.49 y 0.34 en 12, 24 y 36 y 33 rezagos nulos: la `descripcionGrafico` es exacta,
  y es el `aria-label` que el lienzo lleva dibujado.
- **M9**: Pascuas 1949–1960 por el algoritmo de Meeus: en marzo, 2 de 12 (1951-03-25 y 1959-03-29), igual que `cal.pascuas` y la lectura.
  Las fechas del calendario y las de la serie coinciden una a una (los puntos de Pascua caen sobre su mes).

## 4. El componente, medido (`v2_mapas_resumen.out`)

| | antes (HEAD) | ahora |
|---|---|---|
| contraste mínimo de una cifra visible, M1 a 1200 (32 estados) | 2.24:1, 568 cifras < 4.5:1 | **4.50:1, 0 < 4.5:1** |
| ídem cap. 1 / plantilla / tienda a 1200 | 2.24:1 (44 / 43 / 63 < 4.5) | 4.54 / 4.54 / 4.50:1 (0) |
| meses a la vista sin desplazar, M1 y tienda a 800 y 375 | 6 | **12** (ningún mapa se desplaza a ningún ancho) |
| meses a la vista, plantilla a 800 y 375 | 7 | 12 |
| cifras visibles, M1 a 800 / 375 (32 estados) | 2676 / 2676 (la mitad fuera de la vista) | **144 / 144** (solo AP sin log ni ∇; V3) |
| cifras visibles, cap. 1 a 375 | 144 | 144 (8.8 px de cuerpo) |
| guiones en cifras, nombres accesibles y leyenda (M1, 1200) | 809 / 809 / 24 estados | 0 / 0 / 0 |
| `role="row"` | 0 | 1 por fila + cabecera; el árbol de Chrome expone `table` 1, `row` 13, `columnheader` 13, `rowheader` 12, `cell` 144 (cap. 1) |
| nombre accesible | fijo | M1: serie, logaritmo y diferencias en los 32 estados; cap. 1 y plantilla: su título; tienda: sin transformación (V5) |
| sin cifras: ratón / toque / teclado | — | sí / sí (toque emulado por CDP) / **no** (V2) |
| al cambiar el ancho sin recargar | — | el `ResizeObserver` reajusta: a 800 px, al cerrar la barra lateral, la celda pasa de 19.5 a 42.9 px y vuelven las cifras; a 375, otra vez sin cifras |

## 5. Regresiones

- **Consola**: caps. 1–6 y guía, todos los módulos, a 1200 y 375 px: ninguna excepción ni `console.error/warn`; solo el 404 de
  `/favicon.ico`. Los 254 lienzos dibujados tienen gráfico y datos (`v2_consola.out`). En el recorrido del cap. 5 a tres anchos, lo mismo;
  `docSw` igual al ancho y 0 elementos recortados por `<main>` (`v2_resumen.out`).
- **Quiz** (`v2_consola.out`, HEAD frente al árbol en el navegador): 8 preguntas; solo cambian `alto` y `descripcionGrafico` de la
  pregunta 5. En la fuente (`v2_regresiones.out`), además, `dibujar` llama a `acfQuiz()` con la misma cuenta.
- `ensamblado/cap5/simulacro.js` idéntico; los 29 bloques `<pre>` del cap. 5 y los de las cinco plantillas fuente, idénticos y en orden;
  12 módulos con el mismo orden y título.
- **Icono**: `fa-trophy` existe en la hoja 6.0.0 (`.fa-trophy:before{content:"\f091"}`), se dibuja (20.3 px de ancho) y
  `fa-ranking-star` no aparece en esa hoja.

---

## 6. Las 42 fichas de `graficas.md`

**C** confirmado · **P** en parte · **N** no arreglado · **NC** no comprobado. Las líneas de `cuatro-combinaciones`, `armonicos-K` y
`tienda-cuadricula` caen en las causas B y E, que el informe no cuenta aparte; se comprobaron igualmente (B: ningún lienzo con
`aria-label` fijo; 32, 36, 11, 7 y 6 textos distintos en el M1, M6, M4, M5 y M10).

| Ficha | Grav. | Veredicto | Evidencia |
|---|---|---|---|
| M1.1 «dos barras» | Alta | C (R1) | Intro: «dos barras grandes… y unas pocas menores»; con log y ∇∇₁₂ salen 1 y 12 y, menores, 3, 9, 23 y 32 (R y página) |
| M1.2 TRM leída como estacional | Media | **P** | Renglones «múltiplos de 12» y «otros» correctos; la glosa nueva es falsa para las series estacionales (V1) |
| M1.3 «exactamente» | Baja | C | ρ̂₃₆ 0.0714 en la lectura; «con un decimal más» |
| M1.4 `aria-label` fijo | Baja | C | 32 textos distintos, cifras = R |
| M2 receta.1 guion | Baja | C | «× −1.00 = −15.00»; ningún guion en la receta |
| M2 receta.2 φ = −1 | Baja | C | «un factor vale −1: no es una diferencia, pero su raíz cae sobre el círculo unitario…» |
| M2 constructor.1 «Sube D a 1» | Baja | C | «Baja $D$ a $0$ y vuelve a subirlo»; la lectura da «observaciones que cuestan las diferencias» (13 → 1) |
| M2 constructor.2 lienzo vacío | Baja | C | Mensaje bajo el lienzo y `aria-label` «vale 1, sin ningún rezago» (captura `…-todo0-1200`) |
| M2 constructor.3 ~14 de 24 | Baja | C | 24 barras visibles con todo en 2 (captura `…-todo2-1200`) |
| M3 sobrediferenciación.1 «∇₁₂^2» | Baja | C | «∇ log», «∇ ∇₁₂ log», «∇ ∇₁₂² log» |
| M4.1 área 85 px | Media | C | 144.8 / 160.8 / 163.8 px a 1200 / 800 / 375 |
| M4.2 «todo en cero» | Baja | C | «Al abrir, el único distinto de cero es Φ» = `params` |
| M5.1 intro con Θ → 0 | Alta | C (R1) | Intro: escalón = 1 + Θ; R: salto 1.000 con Θ = 0, 0.050 con −0.95 |
| M5.2 eje de σₕ | Media | C | Eje y de 0 a 0.04 con θ = Θ = −0.95 y de 0 a 0.25 al abrir |
| M5.3 «escala logarítmica» | Baja | C | «…medida sobre el logaritmo de la serie (el eje es lineal y empieza en 0)» |
| M5.4 área 95 px; escala de ψ | Baja | P | Área 144.8 px; con θ = Θ = 0.5 el eje de ψ sigue saltando a [−1, 6] |
| M6.1 «—» en la tabla | Baja | C | BIC −431.95 y ρ̂₁₂ −0.3907 = R |
| M6.2 leyenda a 375 | Baja | C | 1 línea, 163.8 px |
| M7.1 «escalones» | Media | C | Intro reescrita, verdadera según R (§3); ver V8 por el estado inicial |
| M7.2 leyenda a 800/375 | Baja | C | 1 línea a 800, 2 a 375; área mínima 207.8 px |
| M8.1 «fuera de banda» | Media | C | TRM: ninguno / 8; AP: 12, 24, 36 / 1, 4, 8, 11, 13, 16, 20, 23, 25, 28, 32 (= R) |
| M8.2 área 105 px | Baja | C | 160.8 / 147.8 px a 800 / 375 |
| M9.1 Semana Santa sola | Alta | C (R1) | «airline + Semana Santa», AICc −487.2305, sin β̂ de días; los días no se dibujan |
| M9.2 `AAAA-MM` y solapes | Media | C | Años redondos a los tres anchos, 0 solapes en los 4 estados |
| M9.3 Pascua en «31»; ejes sin título | Baja | P | Puntos sobre la serie, dentro del área; títulos solo con marco ≥ 420 px: faltan a 800 y 375 (V7) |
| M9.4 «meses» | Baja | C | «años con Pascua en marzo 2 de 12» = R |
| M11.1 leyenda cortada | Alta | C | 9 de 9 entradas, 0 cortadas, a 1200 / 800 / 375 (4 / 4 / 5 líneas); área 168.8 / 272.8 / 259.8 px |
| M11.2 colores | Media | C | Par más próximo: ΔE2000 12.4 con trazos distintos (antes 3.6 con el mismo trazo) |
| M11.3 rótulos cortados | Media | C | Interruptores y lectura completos; leyenda con nombre del método o forma corta |
| M11.4 SARIMA = auto.arima | Baja | C | «auto.arima (= SARIMA)», punteada y de 3 px |
| M11.5 «apunta cuál…» | Baja | C | Frase retirada; ver V9 |
| M11.6 MAPE sin «%» | Baja | C | «3.151 %» |
| M11.7 icono vacío | Baja | C | `fa-trophy` en 6.0.0, dibujado |
| Quiz.1 sin descripción | Media | C | `aria-label` del lienzo = descripción; cifras = R |
| Quiz.2 113 px a 375 | Baja | P | Área 152.8 px; las barras siguen en 1.6 px |
| M12.1 figuras a 266 px | Media | N | No tocado (`simulacro.js` y su CSS idénticos): instrumento aplicado |
| M12.2 rezagos 1–27 a 375 | Baja | N | Ídem |
| M12.3 banda azul | Baja | N | Ídem |
| E.1 contraste | Media | C | §4 |
| E.2 enero–junio a 800/375 | Media | **P** | 12 meses siempre; pero sin cifras a 800 en 23 de 32 estados y sin acceso por teclado (V2, V3) |
| E.3 guiones | Baja | C | §4 |
| E.4 filas ARIA y nombre | Media | P | Filas en el árbol de Chrome; el nombre dice la transformación en el M1, no en la tienda (V5) |

Recuento: 33 C (3 de ellas por la R1), 6 P, 3 N, 0 NC. De las 4 Altas, 4 C; de las 13 Medias, 9 C, 3 P (M1.2, E.2, E.4) y 1 N; de las
25 Bajas, 20 C, 3 P (M5.4, M9.3, Quiz.2) y 2 N.

## 7. Lo que no se pudo comprobar

- Un lector de pantalla real, y otros motores: solo el árbol de accesibilidad de Chrome. Las filas usan `display: contents`, que Safari
  ha expuesto mal en versiones anteriores; no se probó.
- Un toque en un teléfono de verdad (se emuló por CDP), los tooltips de Chart.js, el giro del teléfono, el modo oscuro y el zoom.
- La consola a 800 px en los caps. 1–4, 6 y la guía (se recorrieron a 1200 y 375; el cap. 5, a los tres anchos).
- Los elementos que sobresalen dentro de contenedores desplazables (`desbordan` en `v2_resumen.out`) no se compararon con HEAD; los
  recortados por `<main>` son 0.

## 8. Contraste con `R2_cambios.md`, fila a fila

Coinciden las cifras, los anchos, las áreas, la reproducibilidad y los verificadores. Diferencias:

- **M1.2**: el redactor la da por arreglada; la glosa que añadió es falsa en 6 de los 10 estados donde aparece (V1).
- **E.2**: «A» en el informe; aquí «en parte». El propio informe muestra el paso de 144 cifras a 0 a 800/375, pero no lo trata como
  pérdida ni menciona el teclado (V2, V3). Dice que el toque no se probó: emulado por CDP, funciona.
- **`cuatro-combinaciones`**: el informe cita el `aria-label` «Serie ∇∇₁₂ log(AirPassengers)…»; la página escribe «Serie Ambas
  diferencias…» (V6).
- **Nombre accesible de los mapas**: «cambia con el estado» es cierto para el M1; en la tienda cambian el número de años y el rango, no la
  transformación (V5).
- **M9.3**: los títulos de eje faltan también a 800 px, no solo «en el teléfono» (V7).
- **Causa H**: el informe dice que no quedan más intros escritas para otro estado; quedan la del M7 (V8) y, por omisión, la del M11 (V9).
