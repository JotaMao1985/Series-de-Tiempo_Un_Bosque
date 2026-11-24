# Capítulo 5 · R1 (errores) · verificación independiente B

2026-11-24. Verificador B, de contexto limpio, sin leer el registro del redactor (`R1_cambios.md`) ni sus salidas `r1_*`
hasta terminar la comprobación propia; después se cotejaron (última sección). Objeto: el diff sin commit contra
`7686d33`, en lo que toca a **las diapositivas, el generador de datos, la reproducibilidad y el aspecto por HTTP**. El
contenido del capítulo lo revisa en paralelo el verificador A.

**Entorno:** R 4.6.0 · forecast 9.0.2 · tseries 0.10.62 · jsonlite 2.0.0 | Python 3.10.14 · statsmodels 0.14.6 ·
numpy 2.2.6 (`MPLBACKEND=Agg`) | Node 26 · Chrome 158 sin ventana (CDP en 9279). Servidor propio en 8767 (y en 8768,
para servir el deck de `7686d33` desde una copia fuera del repo); los dos y Chrome, cerrados al acabar. No se corrió
`verifica_directo_cap5.R`: ningún claim nuevo depende de una clave nueva de `directo_cap5.json` (los nuevos leen
`R["m2"]`, que ya existía), y `directo_cap5.json` no cambió.

**Guiones y salidas** (`diagnostico/cap5/comprobaciones/`; capturas en `diagnostico/cap5/capturas/v1b/`):

| guion | salida | qué comprueba |
|---|---|---|
| `v1b_cifras_deck.R` | `v1b_cifras_deck.out` | recálculo desde los datos, sin leer el JSON, de cada cifra nueva del deck: Θ̂, e. e. y distancia a −1 con $D = 0, 1, 2$; θ̂ y su e. e.; los pesos ψ del *airline* por recursión y con `ARMAtoMA`; σ₁₂/σ₁, la subida anual 0.265, ψ₂₄₀, el primer $h$ en que supera a la caminata, σ₂₄₀/σ y √240; el salto ψ₁₂ − ψ₁₁ con Θ = 0, −0.5569 y −0.99; la TRM congelada (ACF, banda, SAR(1) forzado con su $t$, AICc); el tope de $P$ y $Q$ en el código de `auto.arima` y el ejemplo de $m = 365$ |
| `v1b_compara_json.py` | `v1b_compara_json.out` | hoja a hoja: `cap5_sarima.json` y `cap5_datos.js` de `7686d33` frente al árbol y frente a una regeneración hecha fuera del repo; `SERIES_CAP5` y `DATOS_CAP5` del HTML; los otros 25 datos incrustados del HTML; secuencias `<c3>…` literales |
| — | `v1b_genera_cap5_regenerado.out` | `genera_cap5.R` del árbol, ejecutado con Rscript 4.6.0 en una copia fuera del repo (solo con `salidas/datos_series.json`) |
| `v1b_guarda_tildes.R` | `v1b_guarda_tildes.out` | que la guarda nueva del generador aborte con `LC_CTYPE = C` y no con UTF-8 |
| `v1b_compara_deck.py` | `v1b_compara_deck.out` | deck construido de `7686d33` frente al árbol: CSS, JS, armazón y diapositivas que cambian |
| `v1b_compara_deck_texto.py` | `v1b_compara_deck_texto.out` | el texto visible de cada diapositiva que cambia, palabra a palabra, y sus clases |
| `v1b_escalas_deck.js` | `v1b_escalas_deck.json`, `v1b_escalas_deck.out` | por HTTP a 1280×720, la escala de las 84 diapositivas en los dos decks, dónde va la línea de la fuente y a qué tamaño |
| — | `v1b_revisar_deck.out` | `revisar.py` de la skill sobre el deck del árbol y sobre el de `7686d33` |
| — | `v1b_construir_deck.out` | `construir.py` de la skill sobre `capitulo_5.md`, con salida fuera del repo, comparada con el deck del árbol |
| `v1b_revisa.js` | `v1b_revisa.json`, `v1b_revisa.out` | por HTTP: M1, M3, M4, M5, M6, M7, M9, M10, M11 (ejercicios) y M12 a 1200 y 375 px con los plegados abiertos (consola, `.katex-error`, `$`, `\(` o `\[` sin renderizar fuera de código, desbordamiento); los simuladores `sobrediferenciacion-estacional`, `airline-pesos` y `calendario-regresores` en cada estado; 13 diapositivas a 1280×720 |
| — | `v1b_reensamblado.out` | md5 de los doce HTML y de `simulacro.js` antes y después de `ensambla_cap5.py` y `ensambla_cap6.py` |
| — | `v1b_verifica_todo.out`, `v1b_verifica_bloques.out`, `v1b_audita_posicion.out`, `v1b_write_failed.out` | verificadores del proyecto; el «write failed» de la sesión de R del verificador de bloques |

## Resumen

**Las cuatro correcciones pedidas al deck son verdad, dicen lo mismo que el capítulo corregido y no queda otra
diapositiva que repita los errores.** Recalculadas en R 4.6 desde los datos: la tabla de sobrediferenciación (Θ̂, e. e. y
distancia a −1 de 28.53, 6.06 y 0.03; −1 dentro de Θ̂ ± 1.96 e. e. solo con $D = 2$); el *airline* frente a la caminata
(2.22 frente a 3.46 en $h = 12$; subida anual 0.265; ψ₂₄₀ = 6.08; cruce en $h = 42$; 53.98 σ frente a 15.49 σ en
$h = 240$; los pesos por recursión y por `ARMAtoMA` coinciden exactamente); el salto en el rezago 12 igual a 1 + Θ (1 con
Θ = 0, 0.01 con Θ = −0.99); la TRM congelada ($t = 0.0146$, que da 0.015 a tres decimales y 0.0146 en el capítulo); el
tope $\lfloor n/(3m)\rfloor$ de `auto.arima`, leído en su código (`max.P <- min(max.P, floor(serieslength/3/m))`, igual
para `max.Q`), que con $n = 800$ y $m = 365$ vale 0 y deja el ARIMA(0,0,0)(0,1,0)₃₆₅ con 365 observaciones perdidas. La
búsqueda de los cuatro errores en la fuente del deck (varianza como regla, caminata, Θ → 0, manchas solares, raíz sobre el
círculo, «más despacio») no deja ninguna repetición: lo que queda de varianza describe (el animado del M3 la sigue
rotulando, ahora con la interpretación «describe; no decide»), y la remisión a las manchas solares del M1 es la del ciclo,
que es correcta.

**El verificador del deck pasa (774/774, 0 sin respaldo) y cada claim nuevo comprueba la cifra que dice**: ningún
`permite` nuevo (el único tocado cambia su motivo y quita un exponente que ya no aparece); la clave re-anclada («menos
incertidumbre a corto plazo») encaja con un solo título; las cifras nuevas se contrastan contra J, contra el recálculo con
los coeficientes de R y contra el texto del capítulo; los claims retirados lo son porque su cifra salió de la diapositiva.
Su informe `.md` es reproducible (md5 igual tras volver a correrlo).

**El generador reproduce byte a byte salvo la marca de tiempo.** Regenerado fuera del repo con R 4.6.0, el JSON solo
difiere del árbol en `generado`; frente a `7686d33`, cambian `generado`, la fuente de la TRM (tilde y fecha de consulta
2026-07-24 → 2026-07-26) y entran 29 hojas en tres grupos, todas usadas: `sobrediferenciacion_estacional[].a_menos_1_en_ee`
(simulador del M3 y deck), `calendario.modelos.con_pascua` (simulador del M9) y `armonica_K_sin_fuga` (la salvedad de la
prosa del M11: $K = 5$ con solo el entrenamiento y RMSE 19.58). `SERIES_CAP5` cambia solo en sus tres cadenas con tilde,
ya sin ninguna secuencia `<c3>…`; los otros 25 datos incrustados del HTML son idénticos. La guarda aborta con
`LC_CTYPE = C` y no con UTF-8.

**Reproducibilidad en verde.** `verifica_todo.py`: 11 verificadores en verde. Verificador de bloques sobre el cap. 5:
1335 de 1335 (antes 1199/1212). `ensambla_cap5.py` y `ensambla_cap6.py` dejan los doce HTML con el mismo md5; el cap. 6 es
idéntico al de `7686d33`; `simulacro.js` no cambió; el cambio de `ETAPAS_CICLO` solo lo lee `ensambla_cap5.py` (el 6 tiene
su propia lista). `audita_posicion_correcta.py`: ningún instrumento concentra las correctas. El deck se reconstruye desde
`capitulo_5.md` con la skill actual y sale idéntico salvo las rutas de los 11 enlaces al material (efecto de escribir la
salida en otra carpeta).

**Por HTTP, sin defectos**: en los diez módulos y a los dos anchos, 0 mensajes de consola (salvo el `favicon.ico`), 0
`.katex-error`, 0 delimitadores sin renderizar fuera de código, 0 desbordamiento horizontal. Los tres simuladores leen lo
que dibujan en todos los estados, igual a 1200 y a 375 px: el de sobrediferenciación da las tres filas de la tabla y la
alarma solo con $D = 2$; el de los pesos ψ da el salto 1.0000 con Θ = 0 y 0.0500 en el tope de −0.95, y el eje se
ensancha para que los ψ de 1.6 o 3.75 no se recorten; el del calendario con Semana Santa sola lee su propio ajuste (AICc
−487.2305, β̂ 0.0298, $t$ = 2.56). Las 13 diapositivas capturadas no tienen errores de MathJax, delimitadores crudos ni
elementos fuera de la lámina; `revisar.py` da las 84 a escala ≥ 88 %.

**Hallazgos: 0 errores, 1 imprecisión, 6 menores.** La imprecisión es una contradicción interna sobre statsmodels que el
deck hereda del capítulo. Los menores son de forma, salvo el n.º 4, que es una decisión de publicación: al reconstruir, el
deck recoge un rediseño de la skill que cambia las 84 láminas y no lo pidió la ronda.

## Hallazgos

| # | Gravedad | Dónde | Qué está mal | Evidencia | Corrección propuesta | Lo que hizo la sesión maestra |
|---|---|---|---|---|---|---|
| 1 | imprecisión | Deck, `capitulo_5.md` l. 1015 (diapositiva 64, «SARIMAX es una regresión…»); en el capítulo, `templates_7_9.html` l. 537 (M9) | Dice que `SARIMAX` con `exog` «ajusta este mismo modelo, igual que `Arima(…, xreg = )`» y que, con $d$ o $D$ > 0, «los dos diferencian la serie y los regresores». El mismo deck (diapositiva 49, l. 794: «statsmodels no diferencia la serie») y el M6 del capítulo (`templates_4_6.html` l. 533) dicen lo contrario: por defecto statsmodels mete $d$ y $D$ en el espacio de estados con un *prior* difuso, informa `nobs = 144` y da otra verosimilitud (en USAccDeaths θ̂ pasa de −0.4303 a −0.3924). El modelo es el mismo; la estimación por defecto, no; y diferenciar literalmente solo ocurre con `simple_differencing=True` | Lectura cruzada de las diapositivas 49 y 64 y de los templates 4_6 (l. 533) y 7_9 (l. 537); las cifras de USAccDeaths están en la diapositiva 49 y las contrasta el verificador del deck (PY) | Decir que los dos estiman el mismo modelo —regresión con errores SARIMA, que equivale a regresar $\nabla^d\nabla_m^D y$ sobre $\nabla^d\nabla_m^D x$—; que R diferencia y statsmodels lo hace dentro del espacio de estados salvo con `simple_differencing=True`, que es como el capítulo lo ajusta en el M9. Mismo cambio en el capítulo (verificador A) |  Corregido en el M9 y en la diapositiva 64: el mismo modelo; equivale a diferenciar serie y regresores; statsmodels solo lo hace así con `simple_differencing=True`, sin esa opción lo lleva al espacio de estados (Módulo 6) y con series cortas la estimación se mueve (Módulo 8) |
| 2 | menor | Deck, diapositiva 51 (`capitulo_5.md` l. 817–826) | El pie de la tabla del M7 cita J `firma`, `orden_pruebas`, `combinaciones`: `combinaciones` ya no aporta ninguna cifra (la fila de la varianza salió) y la fila nueva sale de J `airline`, que no se cita. Además el título dice «Etapas 1 a 3» y la fila nueva es «Señal de vuelta (etapa 5)», con Θ̂ y θ̂ que el caso estima después | `v1b_compara_deck_texto.out` (diapositiva 51); los claims nuevos del verificador leen `AIR + ".coeficientes"` | Pie: J `firma`, `orden_pruebas`, `airline`. Título que no prometa solo 1 a 3 (p. ej., «… y la señal de vuelta de la etapa 5 lo confirma»), o la fila en la diapositiva de la etapa 5 |  Corregido: pie con `airline` en vez de `combinaciones`; la fila pasa a «Comprobación al estimar (etapa 5)» y «Ninguna señal de diferencia de más». El título se deja (la tabla es de las etapas 1 a 3 más la comprobación), sin re-anclar |
| 3 | menor | Deck, diapositiva 41, l. 682 | La etiqueta `Definición` va sobre «El salto en el rezago 12 vale 1 + Θ», que es un resultado derivado de los pesos ψ (heredado de la versión anterior, que también la usaba) | `v1b_cifras_deck.out`: el salto se obtiene de la recursión, no se define | `<kbd>Dato</kbd>` o `<kbd>Interpretación</kbd>`, como en el resto del deck |  Corregido: `Interpretación` |
| 4 | menor (decisión de publicación) | Deck construido, todas las láminas | La reconstrucción no se limita a las 13 diapositivas corregidas: trae 136 líneas de CSS y 58 de JS nuevas de la skill. Efectos medidos por HTTP a 1280×720: (a) en 28 láminas la línea «Fuente: …» sale del cuerpo al pie, a 12.5 px (antes, en el cuerpo, entre 16.9 y 19.2 px), y el pie pierde el sello «Capítulo 5 · Modelos SARIMA / Series de Tiempo · UnBosque»; las 33 cuya línea empieza por «Contexto:» la conservan en el cuerpo, así que la fuente queda en dos sitios según la lámina; (b) la línea pequeña del cuerpo baja a 0.74 em (mínimo medido 15.0 px, antes 16.9); (c) 46 láminas crecen hasta 1.24 por el nuevo relleno automático (antes, ninguna por encima de 1); (d) los 11 divisores llevan «Parte N de 11» y otra maqueta; (e) barra de progreso con muescas y ritmo en el panel del presentador. Nada se rompe (`revisar.py` en verde, 0 fuera de lámina), pero la fuente a 12.5 px no se lee proyectada y el cambio de aspecto llega a láminas que la R1 no tocó | `v1b_compara_deck.out`, `v1b_compara_deck_texto.out`, `v1b_escalas_deck.out`; capturas `deck-07.png`, `deck-36.png`, `deck-41.png` frente a `deck-29.png` | Que Javier decida si el deck se publica con el rediseño. Si se acepta: que la skill mueva también al pie la fuente de las láminas con «Contexto: … Fuente: …», o que ninguna la mueva, para que haya un solo sitio; y revisar el tamaño de 12.5 px para proyectar. Si no: publicar solo las 13 láminas corregidas sobre la plantilla de la publicación |  Comprobado: la skill cambió el 14 nov y el deck del cap. 4, publicado el 22 nov, ya se construyó con ella; se mantiene. La fuente a 12.5 px en el pie queda como observación sobre la skill, para decidir con Javier |
| 5 | menor | Deck, diapositiva 25 («Cada operador hace su trabajo…», l. 430–435) | Con la interpretación nueva la lámina baja de 0.94 a 0.88: queda justo en el umbral de la skill (≥ 88 %) y es la única que empeora | `v1b_escalas_deck.out` («escala menor que antes: (25, 0.94, 0.88)») | Acortar la línea, p. ej. «<kbd>Interpretación</kbd> La varianza describe; no decide \(D\) ni \(d\)» |  Corregido: «La varianza describe; no decide D ni d». `revisar.py` en verde (`r1_maestra_revisar_deck.out`) |
| 6 | menor | `precalculo/verifica_bloques_cap6.py` (comportamiento, no del diff) y su salida sobre el cap. 5 | En este entorno la sesión de R termina con código 1 y «Error: write failed» al salir, porque los bloques dibujan y el dispositivo por defecto escribe `precalculo/Rplots.pdf`, que aquí no se puede escribir. Los bloques corren completos (con una carpeta escribible, código 0) y el recuento 1335/1335 no cambia; pero el verificador solo imprime el aviso y devuelve 0 si cuadran las cifras, así que un bloque que fallara después de su última línea `#>` pasaría. El registro del redactor dice que el «write failed» «ya no aparece»: depende del entorno | `v1b_verifica_bloques.out`, `v1b_write_failed.out` (misma sesión: código 1 con `cwd = precalculo/`, 0 en una carpeta temporal) | En la cabecera de R del verificador, `pdf(NULL)` o `options(device = function(...) pdf(NULL))`; y que el verificador falle si alguna sesión termina con código ≠ 0 |  Corregido en `verifica_bloques_cap6.py`: dispositivo gráfico nulo en la cabecera de R y salida 1 si alguna sesión termina con código ≠ 0 |
| 7 | menor | Deck, diapositiva 29, notas (l. 513) y verificador l. 558 | El claim de `1.96` es una convención (`DEF_`) y no comprueba que el simulador del M3 use ese umbral, que es lo que afirman las notas («avisa cuando −1 cae dentro de Θ̂ ± 1.96 e. e.»). El simulador sí lo usa (`chapter.js`: `info.a_menos_1_en_ee < 1.96`; por HTTP, alarma solo con $D = 2$) | `v1b_revisa.json` (estados `D0`, `D1`, `D2`); diff de `chapter.js` | Añadir un `CH_` al texto del capítulo que lo dice (`\hat\Theta \pm 1.96\,\text{e.e.}`) |  Corregido: el claim de 1.96 añade `CH_` con el texto del capítulo y un `BOOL_` que busca el umbral en el simulador |

## Comprobado y correcto (sin hallazgo)

- **Diapositivas cambiadas frente al capítulo**: la 25 (la varianza describe, no decide; igual que el ciclo del M4 y el
  M3), la 29 (tabla con la distancia a −1, igual que la del M3, con las mismas cifras y negritas), la 36 (vueltas atrás
  con Θ̂ o θ̂ pegados a −1, igual que `ETAPAS_CICLO`), la 41 (corto frente a largo plazo, con las cifras del bloque del M5:
  `2.222`, `42`, `53.980`, `15.492`), la 43 (resumen sin la raíz ni la varianza), la de la rejilla, «En la rejilla de 36 modelos…» (las
  manchas solares salen de las notas: el BIC castiga más, igual que la prosa del M6), la 49 (notas con BFGS, igual que los bloques del M6), la 51 (Θ̂ =
  −0.5569, e. e. 0.0731; θ̂ = −0.4018, e. e. 0.0896 en el capítulo y en R), la 61 ($t$ = 0.015; la frase del promedio
  mensual es la misma salvedad del M8), la 69 (el tope de `auto.arima` del M10) y las notas de las 10 y 11 (la TRM leída
  de la copia fija, −0.0025). La copia publicada de la TRM en `origin/gh-pages` tiene el mismo md5 que la local.
- **El 58 % de log(lynx)** de las notas de la 29 está en el capítulo 4 (1.653 → 0.687) y en el 5.
- **Generador**: el cálculo de `a_menos_1_en_ee` es $(\hat\Theta + 1)/\text{e.e.}$ con los valores sin redondear; el ajuste
  `cal_pascua` usa la misma especificación que los otros tres; las hojas nuevas no alteran ninguna existente. El comentario
  «se aborta antes de escribir nada» no es exacto para la última comprobación (se hace sobre `cap5_datos.js` ya escrito),
  pero las dos anteriores ya cubren las mismas cadenas: sin efecto.
- **Plegados**: se abrieron los 2 del M3, el del M5 y los 6 del M11 (soluciones); ningún botón quedó cerrado.
- **Escala del deck**: las 84 a ≥ 0.88 en los dos decks; ninguna por debajo.

## No se pudo comprobar

- El aspecto **proyectado** (contraste y tamaño reales en un aula): solo capturas a 1280×720.
- La **hoja de contactos** completa de las 84 láminas: se capturaron 13 (las cambiadas y cuatro de muestra del rediseño).
- El **simulador de los pesos ψ** solo llega a $h = 36$, así que no puede mostrar el cruce de $h = 42$; la prosa lo
  anuncia «como se ve a continuación» justo antes del simulador y lo muestra el párrafo de después. Es contenido del
  capítulo (verificador A): se anota, sin hallazgo propio.

## Cotejo con el registro del redactor

Leído después de terminar. Coincide en los recuentos (774/774, 1335/1335, 11 en verde, ≥ 88 %) y en que el deck se
reconstruyó con `construir.py`. Dos matices: el registro describe los cambios de la skill como «CSS de los temas», y además
hay 58 líneas de JS y el cambio de sitio de la fuente en 28 láminas (hallazgo 4); y dice que el «write failed» de R ya no
aparece, cuando depende de si `precalculo/` admite escribir `Rplots.pdf` (hallazgo 6).
