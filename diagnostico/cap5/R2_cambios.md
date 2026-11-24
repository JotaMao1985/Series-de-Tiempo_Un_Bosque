# R2 · Registro de cambios · Capítulo 5 «Modelos SARIMA» · gráficas y simuladores

Ronda R2 del `PLAN_Mejora_Cap5.md` (tareas T2.1–T2.2; decisión D5 y §7, pregunta 3). Fecha: 2026-11-24. Un solo redactor.
Especificación: `diagnostico/cap5/graficas.md` (42 problemas: 4 Altas, 13 Medias, 25 Bajas; 8 causas comunes A–H). Base: `e084436`
(la R1 publicada). Sin commit ni push.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/componentes/mapa_estacional.js` | contraste por razón WCAG, signo menos, filas `role="row"`, `aria-label` de la rejilla con la serie y la transformación, los doce meses siempre a la vista (`ajustarMapaEstacional`) y la línea del valor señalado (§2) |
| `ensamblado/componentes/mapa_estacional.css` | columnas sin ancho mínimo, `.mapa-estacional-fila`, cuerpo menor de cifra, modo sin cifras, `.mapa-estacional-valor`; la nota alineada a la izquierda (lo que el cap. 1 tenía a mano) |
| `ensamblado/retropropaga_mapa.py` | modo `--actualiza` / `--comprobar`: sustituye el bloque instalado entre sus marcas, comprueba que fuera de ellas nada cambia y que reejecutarlo no cambia nada. Sin opciones instala, como antes |
| `ensamblado/cap5/chapter.js` | ayudantes (`escalasLinea`, `compactar`/`barrasCompactas`/`lineaCompacta`, `ariaLienzo`, `fueraDeBanda`, `rangoDe`, `sub`, `acfQuiz`), `fmt()` con signo menos, los `pintar()` de los 13 simuladores con lienzo o mapa, y la `descripcionGrafico` y el `alto` del gráfico del quiz. Nada de enunciados, opciones, orden, clave ni retros del quiz |
| `ensamblado/cap5/templates_1_3.html`, `_4_6`, `_7_9`, `_10_11` | alto inicial de 14 marcos, el icono del M11, la fila (0,1,0)(0,1,0) de la tabla del M6, el rótulo de σₕ, y cinco frases de intro (M1, M2, M4, M7, M11) |
| `Htmls_Series/capitulo-5-sarima.html` | reensamblado (`ensambla_cap5.py`); reproducible byte a byte (md5 `73d54cd5…` en dos pasadas) |
| `Htmls_Series/capitulo-6-pronostico-evaluacion.html` | reensamblado (`ensambla_cap6.py`, md5 `d6a949f6…` en dos pasadas): cambia **solo** el componente heredado |
| `Htmls_Series/capitulo-1-componentes-descomposicion.html`, `plantilla/plantilla-capitulo.html` | `retropropaga_mapa.py --actualiza`: **solo** el componente |
| `Htmls_Series/proyecto-pronostico-corte-iii.html` | `precalculo/ensambla_proyecto.py` tras cambiar la plantilla: **solo** el componente |
| `diagnostico/cap5/comprobaciones/r2_*` | guiones y salidas de la ronda |
| `diagnostico/cap5/capturas/r2/` | capturas (git las ignora) |

`r2_solo_componente.py` comprueba lo de «solo el componente»: toma cada uno de esos cuatro archivos en HEAD, le pone los dos bloques del
componente nuevo y lo compara byte a byte con el de trabajo: idénticos los cuatro.

No se tocó: el armazón común (cap. 2), `simulacro.js`, `componentes/simulacro_correccion.css`, el banco, `Htmls_Series/preparcial-corte-2.html`,
el deck, ningún bloque de código R o Python, `DATOS_CAP5`/`SERIES_CAP5` ni `genera_cap5.R` (no hizo falta regenerar), el orden de los
módulos. Ninguna clase nueva de Tailwind (la hoja compilada sale idéntica: §5). Ninguna cita, autor, año ni fuente nuevos.

**Guiones** (`diagnostico/cap5/comprobaciones/`)

| guion | salida | qué hace |
|---|---|---|
| `r2_edita.py` | — | reaplica sobre HEAD las 99 sustituciones de las ocho fuentes (cada «antes» único en HEAD y cada «después» único en el resultado); `--comprobar` compara; una sustitución ya aplicada se reconoce y se salta (probado sobre el árbol de trabajo: 99 de 99 reconocidas); `--ensambla` regenera lo derivado (retropropaga, cap. 5, cap. 6, guía) |
| `r2_genera_edita.py` | `r2_edita.py` | escribe `r2_edita.py` desde la diferencia con HEAD |
| `r2_cifras.R` | `r2_cifras.out` | las cifras nuevas recalculadas en R desde `datasets::AirPassengers` y la copia fija de la TRM: la fila (0,1,0)(0,1,0) del M6, el ancho del IC del M7 por horizonte, las Pascuas de 1949–1960, la ACF del gráfico del quiz, las barras fuera de banda del M1 y del M8, el polinomio con todo en 2, ψ y σₕ del estado inicial del M5, la igualdad SARIMA = auto.arima, y el contraste de las paletas del mapa con la regla nueva y la vieja |
| `r2_revisa.js` | `r2_medidas.json`, `r2_revisa.log` | cap. 5 por HTTP: los 14 simuladores y el quiz en los 151 estados del informe a 1200, 800 y 375 px (375 con `mobile:true`, dsf 2), con captura; mide áreas, ejes, solapes, leyendas (también las entradas cortadas), `aria-label`, marcadores recortados, y en cada mapa: meses visibles, filas ARIA, contraste de cada cifra visible, guiones, desbordes |
| `r2_resumen.py` | `r2_resumen.out` | resumen de esas medidas |
| `r2_tabla.py` | `r2_tabla.out` | una línea por lienzo y ancho, en el formato de `diag/graficas_tabla.out` |
| `r2_recorrido.js` | `r2_recorrido_{antes,despues}.json` y `.log` | humo de los caps. 1–6 y la plantilla, todos los módulos, a 1200, 800 y 375 px, con las medidas del mapa; «antes» es HEAD servido desde `git archive` |
| `r2_compara.py` | `r2_compara.out` | antes frente a después: consola, lienzos sin gráfico, desbordes, y qué cambia fuera del cap. 5 (y los mapas de las tres páginas) |
| `r2_solo_componente.py` | `r2_solo_componente.out` | caps. 1 y 6, plantilla y guía: HEAD + componente nuevo = archivo de trabajo |
| `r2_iconos.js` | `r2_iconos.out` | qué iconos de Font Awesome 6.0.0 se dibujan, y que ningún icono del cap. 5 queda vacío |
| — | `r2_bloques_cap5.out`, `r2_verifica_todo.out`, `r2_verifica_cifras_deck.out` | los verificadores al cerrar |

Capturas: `capturas/r2/mN-<simulador>[-<estado>]-{1200,800,375}.png` y `mN-vistaK-{800,375}.png` (pantalla real);
`capturas/r2/recorrido-{antes,despues}/` las del humo (`cN-mM-mapaK-<ancho>.png` son los mapas). El sistema de archivos no distingue
mayúsculas: `…-fijo-d1-…` y `…-fijo-D1-…` (y los del M1 `…-d1` / `…-D1`) se pisan y queda la segunda; las medidas sí son de cada estado.

---

## 1. Los 42 problemas, uno por fila

Estados: **A** arreglado · **P** en parte · **R1** lo resolvió la ronda R1 (comprobado que dibujo y prosa casan) · **N** no tocado, con motivo.
«Antes», las medidas del informe; «ahora», las de `r2_resumen.out` y `r2_tabla.out`.

| Ficha | Problema | Estado | Qué se hizo, o por qué no | Captura |
|---|---|---|---|---|
| M1 · `mapa-firma` | 1 **[Alta]** «dos barras» y salen seis | **R1** | La intro dice ya «dos barras grandes, en los rezagos 1 y 12, y unas pocas menores sin patrón». Con log y ∇∇₁₂ el dibujo saca 1 (−0.341) y 12 (−0.387) muy por fuera de ±0.1712 y 3, 9, 23 y 32 cerca de la banda; la lectura nueva las lista: «múltiplos de 12 fuera de banda 12 (…) · otros 1, 3, 9, 23, 32» (`r2_cifras.out` §5, igual) | `m1-mapa-firma-airpassengers-log-d1D1-1200` |
| | 2 [Media] la lectura señala la TRM como estacional con ∇₁₂ | **A** (tras V1) | El renglón se llama «múltiplos de 12 fuera de banda» y un renglón aparte, «otros rezagos fuera de banda», da el resto. La glosa que la primera versión añadía tras ∇₁₂ se retiró (V1): era falsa en las series estacionales. La lectura da las cifras y la interpretación es de la prosa (M3, M4, M7). TRM ∇₁₂: ρ̂₁₂ = −0.3542; ∇∇₁₂: −0.3965 (R: igual) | `…-trm-nolog-d1D1-1200` |
| | 3 [Baja] «reproduce exactamente» sin ρ̂₃₆ y con un decimal más | **A** | La lectura da ρ̂₃₆ (0.0714 con la TRM y ∇; tabla 0.071) y la intro dice «reproduce la última fila de la tabla de más abajo, con un decimal más» | `…-trm-nolog-d1-1200` |
| | 4 [Baja] `aria-label` fijo | **A** | `descripcionCorrelograma()`: «ACF muestral de AirPassengers (pasajeros/mes) en logaritmos, con las dos diferencias, ∇ ∇₁₂, rezagos 1 a 36: 6 de 36 barras fuera de la banda ±0.171; la del rezago 1 vale −0.341». 32 textos distintos en los 32 estados | — |
| | 5 el mapa (común E) | **A** | §2 | `…-airpassengers-log-ninguna-{1200,800,375}` |
| M2 · `receta-mes` | 1 [Baja] guion en la tabla | **A** | `fmt()` con signo menos (común F): «× −0.42 = −6.30». `r2_resumen.out`: ningún guion en la receta ni en las lecturas | `m2-receta-mes-phi-1-Phi-1-1200` |
| | 2 [Baja] φ = −1 «es una diferencia» | **A** | Solo un factor que vale +1 es una diferencia; con −1: «un factor vale −1: no es una diferencia, pero su raíz cae sobre el círculo unitario y el proceso ya no es estacionario» | `…-phi-1-Phi-1-1200` |
| M2 · `constructor-polinomio` | 1 [Baja] «Sube D a 1» con D = 1 ya | **A** | Intro: «Baja $D$ a $0$ y vuelve a subirlo: la lectura dice también cuántas observaciones cuesta». El estado inicial no cambia (lo menos invasivo: la prosa sigue enseñando lo mismo) | `m2-constructor-polinomio-1200` |
| | 2 [Baja] lienzo vacío con todo en 0 | **A** | Con p = d = P = D = 0 aparece debajo del lienzo «Con p = d = P = D = 0 el polinomio autorregresivo es 1: no toca ningún rezago y no hay barras que dibujar», y el `aria-label` lo dice | `…-todo0-{1200,375}` |
| | 3 [Baja] con todo en 2 se ven ~14 de 24 | **A** | Los ceros exactos no llevan barra y las demás miden al menos 3 px (`minBarLength`): se ven las 24 (rezagos 1–4, 12–16, 24–28, 36–40, 48–52); el mayor, 8.20 en el 25, y el menor no nulo, 0.0225 (`r2_cifras.out` §6) | `…-todo2-1200` |
| M3 · `tienda-cuadricula` | (común E) contraste < 3:1, enero–junio a 800/375 | **A** | §2. Con ∇ y crecimiento fijo, contraste mínimo de una cifra 4.98:1 (antes 2.92:1); los doce meses a los tres anchos, con cifra (enteros de 1–3 caracteres) | `m3-tienda-cuadricula-fijo-d1-375` |
| M3 · `cuatro-combinaciones` | (común B) `aria-label` fijos | **A** | Serie: «Serie ∇∇₁₂ log(AirPassengers), de 1950-02 a 1960-12 (n = 131): valores entre … y …»; ACF: `descripcionCorrelograma`. Marcos 220/210 → 240/250 px | — |
| M3 · `sobrediferenciacion-estacional` | 1 [Baja] «∇₁₂^0», «∇₁₂^2» | **A** | «∇ log(AirPassengers)», «∇ ∇₁₂ log(…)», «∇ ∇₁₂² log(…)»; `aria-label` con la serie y su rango | `m3-sobrediferenciacion-estacional-D{0,2}-800` |
| M4 · `firma-teorica` | 1 [Media] áreas de 85–89 px | **A** | Marcos de 190 a 250 px (260 en el teléfono): área mínima 144.8 / 160.8 / 163.8 px a 1200 / 800 / 375 en los 10 estados (antes 85 / 86 / 89) | `m4-firma-teorica-phi05-Phi07-1200` |
| | 2 [Baja] «Empieza con todo en cero» con Φ = 0.7 | **A** | Intro: «Al abrir, el único distinto de cero es $\Phi$: picos limpios en 12, 24, 36 y nada más». Se corrigió la intro y no el estado: con todo en cero el lienzo se abre vacío. El `aria-label` da los cuatro parámetros y ρ en 1, 11, 12, 13, 24 y 36 | — |
| M5 · `airline-pesos` | 1 **[Alta]** la intro dice lo contrario con Θ → 0 | **R1** | La intro ya dice «el salto vale exactamente ψ₁₂ − ψ₁₁ = 1 + Θ. Lleva Θ a 0 y el escalón vale 1… hacia −1 casi desaparece». Dibujo y lectura casan: salto 1.0000 con Θ = 0, 0.0500 con Θ = −0.95, 0.4400 al abrir (`r2_cifras.out` §7: ψ₁₂ − ψ₁₁ = 0.440) | `m5-airline-pesos-Theta0-1200`, `…-Theta-095-1200` |
| | 2 [Media] el eje de σₕ se reescala | **A** | El eje de σₕ arranca en 0 (`escalasLinea`, y `min: 0`): con θ = Θ = −0.95 la curva queda casi plana en 0.037–0.039 y en el estado inicial sube hasta ~0.20 | `…-theta-095-Theta-095-800` |
| | 3 [Baja] «σₕ (escala logarítmica)» se lee como eje logarítmico | **A** | Rótulo: «… $\sigma_h$, medida sobre el logaritmo de la serie (el eje es lineal y empieza en $0$)» | — |
| | 4 [Baja] área de 95 px; el eje de ψ cambia de escala | **P** | Marco de 200 a 250 px: 144.8 / 160.8 / 163.8 px de área (antes 95 / 96 / 99). El eje de ψ sigue creciendo cuando los pesos pasan de 1.4 (θ = Θ = 0.5 llega a 6): fijarlo en el máximo del rango dejaría los pesos del estado inicial (≈1) en una sexta parte del alto. El `aria-label` da ψ₁, ψ₁₁, ψ₁₂, el salto, ψ₂₄ y ψ₃₅ | — |
| M6 · `explorador-sarima` | 1 [Baja] «—» en la tabla para (0,1,0)(0,1,0) | **A** | La fila da BIC $-431.95$ y ρ̂₁₂ $-0.3907$, las cifras del simulador (`r2_cifras.out` §1: BIC −431.95; ρ̂₁₂ −0.3907 con los 144 residuales, la convención de las otras filas: el *airline* da −0.0515 así) | `m6-explorador-sarima-pqPQ0000-1200` |
| | 2 [Baja] leyenda de 2 líneas y 98 px a 375 | **A** | Leyenda compacta: una línea; 163.8 px de área a 375. `aria-label` con `descripcionCorrelograma` (36 textos en los 36 modelos) | `…-pqPQ0011-375` |
| M7 · `pronostico-estacional` | 1 [Media] la intro manda ver «escalones» que no se ven | **A** | Intro: «en logaritmos el abanico se abre de forma continua —al cruzar el rezago estacional, en $h = 13$, se ensancha algo más deprisa, pero no a escalones visibles—». `r2_cifras.out` §2: el ancho del IC 95 % crece 0.0337 en h = 13, el mayor salto de los 24 (0.012–0.024 en los demás) | `m7-pronostico-estacional-log-h24-1200` |
| | 2 [Baja] leyenda de 2 líneas a 800/375 | **A** | Leyenda compacta y marco de 300 px en el teléfono: 1 línea a 800, área mínima 207.8 px a 375. `aria-label` con el horizonte, el pronóstico y el IC 95 % | `…-h24-375` |
| M8 · `contraejemplo-trm` | 1 [Media] «fuera de banda» solo mira 12, 24, 36 | **A** | Dos renglones: «múltiplos de 12 fuera de banda» y «otros rezagos fuera de banda». TRM: ninguno / 8 (ρ̂₈ = −0.190); AirPassengers: 12, 24, 36 / 1, 4, 8, 11, 13, 16, 20, 23, 25, 28, 32 (R: igual, §5) | `m8-contraejemplo-trm-trm-1200` |
| | 2 [Baja] área de 105–108 px | **A** | Marco de 230 a 250 px (260 en el teléfono): 144.8 / 160.8 / 147.8 px (antes 125 / 105 / 108; a 375 la leyenda del AirPassengers ocupa dos líneas aún compacta) | `…-ap-375` |
| M9 · `calendario-regresores` | 1 **[Alta]** Semana Santa sola con las cifras de otro modelo | **R1** | Lee su propio ajuste `con_pascua`: «airline + Semana Santa», AICc −487.2305, sin β̂ log(días); el gráfico no dibuja los días (`r2_medidas.json`, estado `dias0-pascua1`) | `m9-calendario-regresores-dias0-pascua1-1200` |
| | 2 [Media] `scales` propios: `AAAA-MM` crudo y solapes | **A** | `escalasLinea` (común A) con el segundo eje aparte: `1949 1950 … 1960` a 1200, `1950 1953 1956 1959` a 800 y a 375; ningún solape en ningún estado; área de 175–184 px; signo menos y línea del 0 del armazón | `…-dias1-pascua1-{800,375}` |
| | 3 [Baja] Pascua en el «31» del eje de días; ejes sin título | **A** (tras V7) | Los meses con Pascua se marcan **sobre la serie**, en su valor (y `clip: false`: el de 1949-04 cae junto al borde y sale entero). Títulos cortos a todo ancho, «log» a la izquierda y «días» a la derecha (este, solo con los días encendidos), y la leyenda dice «Días del mes (eje derecho)» | `…-dias1-pascua1-{1200,800,375}` |
| | 4 [Baja] «meses con Pascua en marzo: 2 de 12» | **A** | «años con Pascua en marzo: 2 de 12», contados en el navegador desde `cal.pascuas` (R: 1951-03-25 y 1959-03-29, §3) | — |
| M10 · `armonicos-K` | (común B) `aria-label` fijo | **A** | Dice K, el número de términos, las fechas y el rango de la curva frente al de K = 6 | — |
| M11 · `comparativa-particion` | 1 **[Alta]** con los 8 métodos la leyenda se corta a 800 y 375 | **A** | Rótulos de la leyenda sin la especificación tras «:» y, en el teléfono, cortos («ETS (log)», «Armónica K = 6», «STL + ARIMA», «SARIMA», «auto.arima (= SARIMA)», «SARIMA + cal.», «ETS (cruda)», «Naive est.»); marco de 280 a 320 px (400 en el teléfono). Con los 8: 4 líneas a 1200 y 800 y 5 a 375, **0 entradas cortadas** a los tres anchos (`r2_resumen.out`); área mínima 168.8 / 272.8 / 259.8 px (antes 129 / 107 / 110) | `m11-comparativa-particion-todos-{800,375}` |
| | 2 [Media] colores casi iguales | **A** | Ocho tonos distintos (naranja, azul, violeta, carmín, verde azulado, ocre, rosa, pizarra) y cuatro trazos que se alternan (raya, continuo, punteado, raya-punto) | `…-todos-1200` |
| | 3 [Media] rótulos cortados a media palabra | **A** | Interruptores y lectura con el nombre completo (sin `slice`); la leyenda, como en la fila 1 | `…-todos-375` |
| | 4 [Baja] SARIMA y auto.arima se tapan | **A** | Se detecta en el navegador que los dos pronósticos son idénticos (R: §8): el segundo se rotula «(= SARIMA …)» y va punteado y más grueso, asomando bajo el primero | `…-todos-1200` |
| | 5 [Baja] «apunta cuál dirías que es el mejor» con el ranking ya a la vista | **A** | Se quitó esa frase de la intro (la tabla ordenable de justo antes ya da el orden) | — |
| | 6 [Baja] MAPE sin «%» | **A** | «3.151 %» (espacio que no se parte) | `…-mape-1200` |
| | 7 [Baja] `fa-ranking-star` vacío | **A** | `fa-trophy`, que 6.0.0 dibuja (`r2_iconos.out`; ningún icono vacío en los 12 módulos) | `m11-comparativa-particion-1200` |
| M11 · quiz | 1 [Media] sin `descripcionGrafico` | **A** | «Función de autocorrelación teórica, rezagos 1 a 36: rezago 12, 0.70; rezago 24, 0.49; rezago 36, 0.34; los otros 33 rezagos valen 0.00.», calculada con la misma función que el dibujo (`acfQuiz`; R: §4). Dice lo que se ve, no el modelo. Enunciado, opciones, orden, clave y retros, intactos | `m11-quiz-grafico1-{1200,800,375}` |
| | 2 [Baja] 113 px a 375 | **A** | `alto: 250`: 150 / 150 / 153 px de área | las mismas |
| M12 · simulacro | 1 [Media] figuras a 266 px a 800 (rótulos de ~7 px) | **N** | Instrumento aplicado: `simulacro.js` y `simulacro_correccion.css` no se tocan. Para el banco: el `viewBox` de 460 a 800 px necesita rótulos más grandes o una figura que no se encoja | — |
| | 2 [Baja] a 375 se ven los rezagos 1–27 | **N** | Igual; para el banco | — |
| | 3 [Baja] banda azul | **N** | Igual; para el banco: `#2563eb` frente al `#e05a00` del resto del capítulo | — |
| Común E (componente) | 1 [Media] contraste 2.24–2.9:1 | **A** | §2 | — |
| | 2 [Media] solo enero–junio a 800/375 | **A** | §2 | — |
| | 3 [Baja] guiones | **A** | §2 | — |
| | 4 [Media] sin `role="row"`, `aria-label` sin serie | **A** | §2 | — |

**Recuento:** 42 problemas (los numerados del informe: las filas de `tienda-cuadricula`, `cuatro-combinaciones` y `armonicos-K` son de las causas
comunes B y E y el informe no las cuenta aparte) = **35 arreglados (A), 1 en parte (P: la escala del eje de ψ del M5), 3 de la R1 (las Altas del
M1, el M5 y el M9, con dibujo y prosa comprobados) y 3 no tocados (N: las figuras del simulacro, instrumento aplicado)**. Por gravedad: de las
4 Altas, 1 A (M11) y 3 R1; de las 13 Medias, 12 A y 1 N (M12-1); de las 25 Bajas, 22 A, 1 P y 2 N. Por ficha: 4 + 2 + 3 + 1 + 2 + 4 + 2 + 2 + 2
+ 4 + 7 + 2 + 3 + 4 (componente) = 42.

Las 8 causas comunes: **A** (M9, `escalasLinea`), **B** (los 15 lienzos y el quiz: ninguno con `aria-label` fijo, `r2_resumen.out`), **C** (llega
bien; no se tocó), **D** (marcos y leyendas: área mínima de todos los lienzos y estados **144.8 / 160.8 / 147.8 px a 1200 / 800 / 375**, antes 85 / 86 / 89; ninguna leyenda cortada), **E** (§2), **F** (`fmt()`),
**G** (el icono) y **H** (las intros del M2 y el M4; revisadas las demás frente a `params` y los extremos: no hay más intros escritas para otro
estado).

## 2. El componente `.mapa-estacional`

Arreglado en `ensamblado/componentes/` y propagado: el cap. 5 lo recibe al reensamblarse; el cap. 6 lo hereda del 5 (sin usarlo: su
verificación, `.mapa-estacional {` y `function pintarMapaEstacional`, sigue en verde); el cap. 1 y la plantilla, con
`retropropaga_mapa.py --actualiza`; la guía del proyecto, con `ensambla_proyecto.py`.

| defecto | qué se hizo |
|---|---|
| 1 · contraste | `textoSobre()` elige el color de la cifra por la razón de contraste WCAG 2, en **dos tonos**: blanco o negro, el que dé más contraste; el peor caso de los dos es 4.58:1 (`r2_cifras.out` §9). La primera versión usaba tres (pizarra, negro y blanco) y dos celdas vecinas podían llevar la cifra de colores distintos (V10). El mínimo medido pasa de 2.24:1 a 4.6:1 |
| 2 · meses visibles | **Decisión: los doce meses a la vista siempre**, sin desplazar. Lo que el mapa enseña son las bandas verticales (la prosa manda buscarlas). Si la cifra no cabe en su celda (los mapas con decimales a 800 y 375 px), el mapa se queda con el color y hay dos maneras de leer los valores, las dos por teclado (V2, V3): (a) la línea del valor, bajo la rejilla, da el de la celda que se toca, se señala o se recorre con las flechas: la rejilla es una sola parada del tabulador, con foco visible, y las flechas, Inicio y Fin mueven la celda señalada; (b) el botón «Ver las cifras» (`aria-pressed`) pasa a la rejilla con cifras, más ancha que su caja y desplazable, con un degradado y una flecha en el borde derecho mientras quedan meses por ver; pulsado otra vez, vuelve. Los meses de la cabecera pasan a la inicial si la abreviatura no cabe. Un `ResizeObserver` lo reajusta si cambia el ancho. El paso intermedio de «cifras chicas» se quitó: no se activaba nunca (V4). La variante `--entero` del cap. 1 se queda y sigue mandando en su mapa (sus cifras caben a los tres anchos) |
| 3 · signo menos | `cifraMapa()`: «−0.141» en celdas, nombres accesibles, títulos y leyenda; un redondeo a cero no lleva signo |
| 4 · estructura | cada fila de la rejilla va en un `role="row"` sin caja propia (`display: Contents`, con mayúscula para que el compilador de Tailwind no lo tome por su clase `contents`); la esquina es un `columnheader` «Año». La rejilla dice qué serie y qué transformación se ve (`datos.descripcion`, que el cap. 5 pasa en cada repintado; sin ella, el título del mapa), cuántos años, el rango y si la escala es divergente |

Además, la nota del mapa va alineada a la izquierda (`text-align: left`), como la tenía el cap. 1 a mano desde su R2: justificada, en el
teléfono abría huecos. Al pasar al componente, el bloque del cap. 1 queda idéntico al del componente y `retropropaga_mapa.py` no necesita
ajustes locales.

**Antes y después** (`r2_compara.out`, recorrido de humo; `r2_resumen.out` para todos los estados del cap. 5):

| página · mapa | ancho | meses a la vista sin desplazar | filas `role="row"` | cifras visibles | contraste mínimo de una cifra visible | guiones |
|---|---|---|---|---|---|---|
| cap. 1 · `cap1-airpassengers` (M3) | 1200 / 800 / 375 | 12 → 12 (ya los tenía: variante `--entero`) | 0 → 13 | 144 → 144 | 2.24:1 (44 celdas < 4.5) → **4.54:1** (0) | 0 → 0 |
| cap. 5 · `firma` (M1, estado inicial, log) | 1200 | 12 → 12 | 0 → 13 | 144 → 144 | 2.24:1 (42 < 4.5) → **4.54:1** | — |
| | 800 / 375 | **6 → 12** | 0 → 13 | 144 (la mitad fuera de la vista) → 0: solo color, línea del valor | 2.24:1 → (sin cifras) | — |
| cap. 5 · `tienda` (M3, estado inicial) | 1200 / 800 / 375 | 12 / **6 → 12** / **6 → 12** | 0 → 5 | 48 → 48 | 2.24:1 (14 < 4.5) → **4.6:1** | — |
| plantilla · `demo-mapa` | 1200 | 12 → 12 | 0 → 9 | 96 → 96 | 2.24:1 (43 < 4.5) → **4.54:1** | — |
| | 800 / 375 | **7 → 12** | 0 → 9 | 96 → 0: solo color, línea del valor | 2.24:1 → (sin cifras) | — |

En todos los estados del cap. 5 (`r2_resumen.out`, 32 del M1 y 8 del M3 por ancho): doce meses a la vista y sin desplazar en todos; ninguna
cifra visible por debajo de 4.5:1 (la peor, 4.50:1); ningún guion en celdas, nombres accesibles ni leyenda; ninguna cifra que desborde su
celda. El M1 lleva cifras a 1200 px en todos sus estados; a 800 y 375 px, las lleva cuando caben (AirPassengers sin logaritmo, 3 cifras) y
si no, solo el color; con co2 (40 años) nunca las llevó. La tienda las lleva en los 8 estados a los tres anchos. El nombre accesible de la
rejilla cambia con el estado (40 textos en los 42 estados medidos a cada ancho; repiten el estado inicial y su gemelo).

La guía del proyecto trae el CSS y el JS del componente pero ningún mapa: solo cambia ese código (`r2_solo_componente.out`).

## 3. Lo propio del capítulo 5 (`chapter.js`)

- **A · `escalasLinea`** (la del cap. 4, con un `y` que se mezcla clave a clave): el M9 (dos ejes, el segundo aparte) y σₕ del M5 (`min: 0`).
- **B · `aria-label`** en cada `pintar()`, con signo menos, en los 15 lienzos y el quiz: los correlogramas muestrales con
  `descripcionCorrelograma()` del armazón (M1, M3, M6, M8); los teóricos del M4 con los valores de 1, 11, 12, 13, 24 y 36; las series con
  fechas, n y rango; el resto con lo que dibujan. Todas las cifras salen de `DATOS_CAP5`/`SERIES_CAP5` en el navegador.
- **D · marcos**: altos nuevos en las plantillas y, por debajo de 420 px, leyenda compacta y alto de teléfono (`compactar`, del cap. 4).
- **F · `fmt()`** con signo menos y sin «−0.00».
- **Lecturas**: «múltiplos de 12 fuera de banda» y «otros rezagos fuera de banda» (M1, M8), ρ̂₃₆ (M1), «años con Pascua en marzo» (M9), «%»
  del MAPE (M11), el rótulo del modelo con φ o Φ = −1 (M2).

## 4. Quiz del M11

Solo la `descripcionGrafico` (y `alto: 250`) de la pregunta 5; `dibujar` usa la misma `acfQuiz()` que la descripción. `AUTOEVALUACIONES['cap5']`
queda igual en enunciados, opciones, orden, clave y retros; `audita_posicion_correcta.py` en verde.

## 5. Verificación al cierre

- `python3 diagnostico/cap5/comprobaciones/r2_edita.py --comprobar`: las ocho fuentes idénticas a HEAD + las 99 sustituciones.
- `ensambla_cap5.py` reproducible byte a byte (md5 `73d54cd50dd265228ebaa95525e76f96` en dos pasadas seguidas), `ensambla_cap6.py`
  también (`d6a949f65cee1941b5fb612e4fb2870f`) y la guía (`daca8f4f52a9ed2e3fc67b0b5fcfbd22`); el 6 pasa sus comprobaciones del componente heredado.
- `retropropaga_mapa.py --comprobar` → «AL DÍA» el cap. 1 y la plantilla (`r2_retropropaga_comprobar.out`); su identidad sobre HEAD con el
  componente viejo se probó en una copia aparte (los dos «AL DÍA»), y la segunda pasada de `--actualiza` no cambia nada.
- `r2_solo_componente.py`: caps. 1 y 6, plantilla y guía del proyecto = HEAD + componente, byte a byte (`r2_solo_componente.out`).
- `python3 precalculo/verifica_todo.py` → **11 verificadores en verde** (`r2_verifica_todo.out`), incluidos la guía del proyecto
  (reproducible y auditada) y Tailwind al día. Una primera pasada dio Tailwind desfasado en las doce páginas: `display: contents` del CSS y
  cuatro cortes `[i2:j2]`… de `retropropaga_mapa.py` (el compilador lee `ensamblado/**`) creaban clases nuevas; se reescribieron (§2 y
  `trozo()`), y la hoja compilada vuelve a ser idéntica (ninguna regla nueva ni perdida). No se recompiló nada.
- `MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-5-sarima.html` → **1335 de 1335** cifras, 0 bloques
  con discrepancias (`r2_bloques_cap5.out`; ningún bloque se tocó).
- `audita_posicion_correcta.py` en verde (`r2_audita_posicion.out`); `sin_literales_diagnostico.py` → 0 coincidencias (`r2_sin_literales.out`).
- Diapositivas: `verifica_cifras_cap5.py` → 774 de 774, «todo verificado y cubierto» (`r2_verifica_cifras_deck.out`); su informe no cambia.
- Por HTTP (servidor propio en 8768 desde la raíz —el de 8765 lo cerró otra sesión a media ronda: se vio en su registro una petición ajena
  de `/muestreo/`—, HEAD desde `git archive` en 8769; Chrome sin ventana en 9278; todo cerrado al acabar):
  - **Cap. 5, 151 estados × 1200, 800 y 375 px** (`r2_resumen.out`): solo el 404 del favicon en la consola; ningún lienzo sin gráfico, dato
    no finito, solape, rótulo fuera, guion en ejes, lecturas, receta o `aria-label`, marcador recortado ni entrada de leyenda cortada;
    ningún `aria-label` fijo; área mínima 144.8 / 160.8 / 147.8 px; ningún elemento recortado por `<main>`; en los mapas, doce meses a la
    vista, ninguna cifra visible < 4.5:1 y ningún guion en los 42 estados por ancho.
  - **Árbol de accesibilidad** del mapa del M1 a 375 px (`r2_arbol_accesible.js` → `.out`): `table` con su nombre, 13 `row`; la primera con
    `columnheader` «Año», «Ene»…, las demás con `rowheader` «1949» y `cell` «Ene 1949: 4.72»…
  - **Caps. 1–6 y la plantilla, antes y después** (`r2_compara.out`): mismos lienzos, ninguno nuevo sin gráfico, ningún desborde ni recorte
    nuevo; **fuera del cap. 5 solo cambian los mapas** (cap. 1 y plantilla, 3 anchos cada uno); en los caps. 2, 3, 4 y 6, 0 cambios en
    `aria-label`, rótulos, áreas, leyendas, lecturas y tablas. Lo que ya estaba en HEAD sigue igual: el lienzo sin gráfico y los solapes del
    cap. 6 a 800/375 y dos recortados del cap. 1 a 800. En el cap. 5 los 4 y 5 solapes de HEAD a 375/800 (el M9) pasan a 0.
  - Iconos (`r2_iconos.out`): `fa-ranking-star` vacío en 6.0.0, `fa-trophy` se dibuja; ningún icono vacío en los 12 módulos.
- Capturas miradas: el mapa del M1 a 1200 y 375 (cifras con la regla nueva; solo color y línea del valor), la tienda a 375 y 800, el mapa
  del cap. 1 a 375 (cifras en tres colores, todas legibles), el constructor con todo en 0 (375) y en 2 (1200, 24 barras), σₕ con
  θ = Θ = −0.95 (800, plana desde 0), el calendario con los dos regresores (375, antes de quitar los títulos de eje en el teléfono) y la
  comparativa con los 8 métodos (375, las nueve entradas). El resto se juzgó por las medidas.
- Cifras nuevas: `r2_cifras.out` las recalcula en R (§1–§9) y coinciden con lo que escribe la página.

## 6. Lo que no se pudo comprobar, y lo que queda

- **Un lector de pantalla real**: no. Se leyeron `role`, `aria-label` y el árbol de accesibilidad de Chrome (las filas llegan como `row`,
  `r2_arbol_accesible.out`); Safari y VoiceOver no se probaron.
- **Tocar una celda en un teléfono de verdad** (la línea del valor): se probó el pase del ratón en Chrome sin ventana, no un toque. Los
  tooltips de Chart.js, el giro del teléfono (el `ResizeObserver` del mapa y el `onResize` de los lienzos), el modo oscuro, el zoom del
  navegador y otros navegadores: no.
- **Cifras del mapa a 375 px**: donde caben (enteros de hasta 3 caracteres) van a ~7.7 px de cuerpo, el mismo del componente antes de
  la ronda; el cap. 1, con su variante, las da a ~8.8 px. Agrandarlas obligaría a dejar más mapas sin cifra.
- **Del armazón (cadena 2 → 6), anotado y no tocado**: la salida de los deslizadores escribe «-0.95» con guion (`crearControles`); los
  lienzos de los caps. 2–6 lo heredan igual.
- **Para el banco** (simulacro del M12, instrumento aplicado; no se tocó): figuras de 266 px a 800 px con rótulos de ~7 px, a 375 px solo
  los rezagos 1–27 sin desplazar, y la banda en azul `#2563eb` frente al `#e05a00` del capítulo.
- **El eje de ψ del M5** sigue reescalándose cuando los pesos pasan de 1.4 (P en la tabla).
- **Las prosas tocadas** (intros del M1, M2, M4, M7 y M11, rótulo de σₕ, fila del M6, la línea del valor del mapa, el aviso del polinomio
  vacío y los rótulos de las lecturas) no pasaron por el par académico; las cifras que llevan están en `r2_cifras.out`.
- **Los PNG de los estados `d1` y `D1`** se pisan en un disco que no distingue mayúsculas (ver Guiones); las medidas no.

## 7. Correcciones tras el verificador

Un verificador independiente revisó la ronda (`R2_verificacion.md`, guiones `comprobaciones/v2_*`). A petición de la sesión maestra se
corrigieron sus diez hallazgos, con las mismas reglas (solo fuentes en `ensamblado/`; componente propagado con `retropropaga_mapa.py
--actualiza`; `ensambla_proyecto.py` por la plantilla; ninguna cifra a mano). `r2_edita.py` se regeneró: 99 sustituciones.

| V | grav. | lo que dijo el verificador | lo que se hizo | comprobación |
|---|---|---|---|---|
| V1 | **Alta** | la glosa «negativo tras ∇₁₂: huella de la propia diferencia, no estacionalidad que quede» es falsa en las series estacionales (en AirPassengers log con ∇∇₁₂ esa barra es la que el M7 lee como «pide Q = 1») | retirada, sin sustituirla: la lectura del M1 da las cifras («múltiplos de 12 fuera de banda», «otros rezagos fuera de banda») y la prosa las interpreta | `r2_resumen.out` (lecturas del M1) |
| V2 | Media | sin cifras, el teclado no llega a ningún valor | la rejilla es una sola parada del tabulador (`tabindex="0"` solo cuando las cifras no caben enteras), con foco visible hacia dentro del marco; flechas, Inicio y Fin mueven la celda señalada (anillo blanco y naranja) y la línea del valor la nombra; al salir, se desmarca | `r2_mapa_teclado.out`: Tab llega a la rejilla en el M1 y la plantilla a 800 y 375 px; → → ↓ y Fin dan «Mar 1950: 4.95» y «Dic 1950: 4.94» |
| V3 | Media | a 800 px el M1 (23 de 32 estados) y la plantilla se quedan sin cifras: se pierde lo que antes se leía desplazando | botón «Ver las cifras» (`<button>`, `aria-pressed`, Intro y Espacio) que pasa a la rejilla con cifras, de columnas tan anchas como la cifra más ancha y desplazable, con un degradado y una flecha naranja en el borde derecho mientras quedan meses a la derecha; pulsado otra vez vuelve al color. Con la rejilla con cifras enfocada, las flechas desplazan la caja hasta la celda. El estado inicial a 800 px sigue siendo el de color | `r2_mapa_teclado.out`: Intro → `aria-pressed=true`, 144 cifras, desplaza (0/150 px a 800), señal visible; desplazado al final, la señal se va; Espacio → vuelve. Capturas `teclado-*-{sin,con}-cifras-{800,375}.png` |
| V4 | Baja | el paso «cifras chicas» no se activa nunca | quitado (CSS y JS) | — |
| V5 | Baja | el nombre del mapa de la tienda no dice escenario ni resta | `descripcion`: «La tienda inventada (crece una unidad al mes), mes × año; se resta ∇: la celda de la izquierda…» | `r2_resumen.out` (aria de la rejilla) |
| V6 | Baja | los `aria-label` de `cuatro-combinaciones` dicen «Ambas diferencias» | el nombre se compone con `c.d` y `c.D`: «Serie ∇ ∇₁₂ log(AirPassengers)…», «ACF muestral de ∇ ∇₁₂ log(AirPassengers)…» | `r2_medidas.json` |
| V7 | Baja | el M9 sin títulos de eje a 800 px | títulos cortos a todo ancho («log» y, con los días encendidos, «días») y la entrada «Días del mes (eje derecho)» en la leyenda | `r2_tabla.out`, `r2_resumen.out` |
| V8 | Baja | la intro del M7 describe el interruptor al revés del estado inicial | «Se abre en la escala original y con el horizonte al máximo. El deslizador mueve el horizonte, y al desmarcar el interruptor se pasa a la escala logarítmica.» (= `params`: `h: 24` y `original: true`) | — |
| V9 | Baja | la intro del M11 no dice el estado inicial | «Se abre con lo observado y los cuatro primeros métodos por RMSE; con todos apagados queda solo lo observado.» (= `params`: los tres primeros de `orden_rmse` y el SARIMA, que es el cuarto) | — |
| V10 | Baja | la cifra alterna pizarra, negro y blanco en celdas vecinas | dos tonos, blanco o negro, el de más contraste (peor caso 4.58:1) | `r2_mapa_teclado.out`: 2 tonos en todos los mapas; contraste mínimo 4.6:1 |

Lo que se volvió a pasar, con todo ya corregido:

- `verifica_todo.py` → 11 verificadores en verde (`r2_verifica_todo.out`); `compila_tailwind.py --comprobar` → salida 0, ninguna página
  desfasada (`r2_tailwind.out`). Una palabra del JS nuevo (`inline` en `scrollIntoView`) habría añadido la clase `.inline` a la hoja de las
  doce páginas: el desplazamiento hasta la celda se hace a mano.
- Bloques del cap. 5: 1335 de 1335 (`r2_bloques_cap5.out`); diapositivas: 774 de 774, «todo verificado y cubierto»; `audita_posicion_correcta.py`
  en verde; `sin_literales_diagnostico.py` → 0.
- Reproducibles byte a byte: cap. 5 `73d54cd5…`, cap. 6 `d6a949f6…`, guía `daca8f4f…` (dos pasadas). `retropropaga_mapa.py --comprobar` →
  «AL DÍA» los dos; `r2_solo_componente.py`: caps. 1 y 6, plantilla y guía = HEAD + componente, y nada más. `r2_edita.py --comprobar` → idéntico;
  99 de 99 sustituciones se reconocen como aplicadas sobre el árbol de trabajo.
- Por HTTP (8768 propio; HEAD en 8769; Chrome en 9278; cerrados al acabar):
  - `r2_mapa_teclado.js` → `r2_mapa_teclado.out`: los mapas del cap. 5 (M1, M3), del cap. 1 y de la plantilla a 1200, 800 y 375 px; teclado,
    botón, desplazamiento, clic y toque emulado como en la tabla de arriba; consola vacía. Donde las cifras caben (1200 px; la tienda y el
    cap. 1 a todos los anchos) no hay botón ni parada de tabulador: la rejilla se comporta como antes.
  - `r2_revisa.js` (cap. 5, 151 estados × 3 anchos) → `r2_resumen.out`: solo el 404 del favicon; ningún `aria-label` fijo; área mínima
    144.8 / 160.8 / 147.8 px; ningún solape, guion ni leyenda cortada; en los mapas, doce meses a la vista y ninguna cifra visible < 4.5:1
    (mínimo 4.6:1). Un aviso del arnés: a 375 px, con los dos regresores, el punto de Pascua de 1949-04 cae a menos de su radio del borde
    izquierdo; con `clip: false` se dibuja entero. El área del M9 a 375 px vuelve a 133 px de ancho, el precio de los títulos de eje (V7).
  - `r2_recorrido.js` antes y después sobre los caps. 1, 5 y 6, la plantilla y la guía a los tres anchos (`r2_compara2.out`): consola limpia;
    fuera del cap. 5 solo cambian los mapas del cap. 1 y de la plantilla; en el 6 y en la guía, nada (los 4 recortados de la guía a 800 px
    estaban en HEAD).
- Capturas miradas: `teclado-cap5-firma-con-cifras-375.png` (botón pulsado, cifras, degradado y flecha a la derecha) y
  `teclado-plantilla-demo-mapa-sin-cifras-800.png` (foco y celda señalada).

## Comprobación de la sesión maestra

- Diff limitado a las fuentes del cap. 5, el componente, `retropropaga_mapa.py`, y los HTML de los caps. 1, 5 y 6, la
  plantilla y la guía, que se regeneran.
- Reensamblar 5 → 6, regenerar la guía y correr `retropropaga_mapa.py --comprobar` deja los cinco archivos con el mismo
  md5 («AL DÍA»).
- La glosa del M1 ya no está en el HTML, y `simulacro.js` queda intacto.
- Verificadores:
  - `verifica_todo.py`: 11 en verde (`r2_maestra_verifica_todo.out`).
  - `compila_tailwind.py --comprobar`: código 0 (`r2_maestra_tailwind.out`).
  - Bloques del cap. 5: 1335/1335, código 0 (`r2_maestra_bloques.out`).
  - `audita_posicion_correcta.py`: verde.
  - `sin_literales_diagnostico.py`: 0.
- Capturas del mapa a 800 px revisadas, sin y con cifras: la celda señalada lleva foco visible y la línea del valor, y la
  caja desplazable lleva la señal de que hay más meses.
- **Decisión de diseño para el docente:** a 800 y 375 px, los mapas con decimales abren en color y piden «Ver las cifras».
  Los mapas con enteros (la tienda, el cap. 1) conservan las cifras.
