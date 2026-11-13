# Capítulo 1 · ronda R4 «fuentes» · cambios

Fecha: 2026-11-13. Redactor único de la ronda: subagente redactor R4 (Fable 5.2). Sin commits.

Los veredictos son de dos verificadores de contexto limpio (lote R4a: FPP3, Cryer y Chan, Shumway y
Stoffer, Hamilton; lote R4b: Cleveland et al., 1990, y la ayuda de R). Este documento dice qué se hizo
con ellos: qué se marcó, qué cita quedó a la vista, qué prosa cambió y qué citas literales hubo que
sustituir.

> **Este documento tiene dos capas.** Lo que sigue hasta «Corrección tras la verificación independiente»
> es la primera pasada, tal como se entregó. La sección final la corrige en 21 puntos y es la que manda:
> el estado vigente es **31 afirmaciones (24 `respaldada`, 7 `con-matiz`, 0 `pendiente`) y 36 citas
> visibles**.

## Resultado de la primera pasada

- **32 afirmaciones registradas** en `bibliografia/contraste/cap1.yml` (había 6): **24 `respaldada`**,
  **8 `con-matiz`**, **0 `pendiente`**. De las 32, 28 son de esta ronda: 26 nuevas y las dos que estaban
  `pendiente` desde el piloto (`c1-m7-01`, `c1-m7-02`).
- **33 citas visibles** en el capítulo (había 3): 21 de FPP3, 7 de la ayuda de R, 5 de Cleveland et al.
  (1990). Cryer y Chan y Shumway y Stoffer respaldan afirmaciones en el registro, sin cita visible.
- **Ningún veredicto se subió.** Donde se ajustó la prosa para quitar el matiz, el veredicto sigue en
  `con-matiz` y la nota dice que la frase nueva no la ha leído el verificador.
- Ninguna cifra nueva ni cambiada. No se tocaron gráficos, simuladores ni datos.

## Una fila por afirmación

| id | veredicto | obra y localizador (en **negrita**, el de la cita visible) | cita visible | cambio en la prosa |
|---|---|---|---|---|
| c1-m1-01 | respaldada | **FPP3 §1.4**; Shumway y Stoffer p. 11, §1.3 | sí | «(cada mes, cada día, cada hora)» pasó a «: cada mes, cada día, cada hora», para no pegar la cita a otro paréntesis |
| c1-m1-04 | con-matiz | **ayuda de R, AirPassengers §Description**; §Format; Cryer y Chan p. 247, ejercicio 10.9 | sí | «en miles (1949–1960)» → «en miles, de 1949 a 1960» (misma razón) |
| c1-m3-08 | con-matiz | **FPP3 §3.2** | sí, tras «modelo multiplicativo» | ninguno; la marca se extendió hasta esa frase |
| c1-m4-02 | respaldada | **FPP3 §2.3**; Cryer y Chan p. 28, §3.1 | sí | ninguno |
| c1-m4-03 | respaldada | **FPP3 §2.3** | sí | «(12 meses, 7 días…)» pasó a rayas |
| c1-m4-04 | respaldada | **FPP3 §2.3** | sí | «(p. ej. ciclos económicos de varios años)» pasó a rayas |
| c1-m4-06 | con-matiz | **FPP3 cap. 3** (narrativa) | sí | **ajustada**: «Muchos textos agrupan tendencia y ciclo en un solo término…» → «Al descomponer una serie, Hyndman y Athanasopoulos (2021, cap. 3) agrupan tendencia y ciclo en un solo componente…» |
| c1-m4-07 | respaldada | **FPP3 §2.3** | sí | ninguno; el texto del inventario (el ciclo de «siete u ocho años») ya no existía: se marcó la frase vigente |
| c1-m4-10 | respaldada | **FPP3 §3.2** | sí | ninguno |
| c1-m4-11 | respaldada | **FPP3 §3.2** | sí | ninguno (se marcó la redacción vigente, distinta de la del inventario) |
| c1-m5-01 | respaldada | **FPP3 §3.3**; Shumway y Stoffer p. 71, §2.4, ec. 2.50 | sí | ninguno |
| c1-m5-02 | respaldada | **FPP3 §3.3** | sí | ninguno |
| c1-m6-09 | respaldada | **FPP3 §3.4** | sí | ninguno |
| c1-m6-13 | con-matiz | **FPP3 §3.4** | sí, en el párrafo «Leída en horizontal…» | ninguno; la marca es un `div` que envuelve la tabla y ese párrafo |
| c1-m6-14 | respaldada | **FPP3 §3.4** | sí | ninguno |
| c1-m6-20 | respaldada | **FPP3 §3.4**; §3.3 | sí | ninguno. **Es el c1-m6-02 del inventario**: ese id ya estaba ocupado desde la R3 |
| c1-m7-01 | con-matiz | **FPP3 §3.6** (suelta); Cleveland et al. p. 3; ayuda de R, stl §Description | sí | **corregida**: «Seasonal-Trend decomposition using Loess» → «Seasonal and Trend decomposition using Loess» |
| c1-m7-02 | respaldada | **Cleveland et al. §3.3**; §2.2; **ayuda de R, stl §Usage** | sí, dos | ninguno (la huella cambia por el espacio que deja la cita en mitad de la frase) |
| c1-m7-05 | respaldada | **Cleveland et al. §2.1**; p. 5; Shumway y Stoffer p. 75, fig. 2.14 | sí | **corregida**: «(locally estimated scatterplot smoothing)» → «—regresión local ponderada, locally weighted regression—» |
| c1-m7-06 | respaldada | **ayuda de R, stl §Arguments** | sí | ninguno; frase del inventario desaparecida: se marcó el paso 2 de «El método, paso a paso» |
| c1-m7-07 | respaldada | **ayuda de R, stl §Usage**; Cleveland et al. §2.3 | sí, tras «los dos grados por defecto» | ninguno; se marcó el párrafo de cierre del desarrollo |
| c1-m7-08 | respaldada | **Cleveland et al. §2.1** | sí | ninguno |
| c1-m7-10 | respaldada | **ayuda de R, stl §Arguments**; Cleveland et al. p. 20 | sí | ninguno |
| c1-m7-15 | respaldada | **Cleveland et al. §2.2**; §2.3; **ayuda de R, stl §Details**; §Arguments | sí, dos | ninguno; se marcó el paso 1 de «El método, paso a paso» |
| c1-m7-16 | con-matiz | **ayuda de R, stl §Arguments**; Cleveland et al. §2.2, §2.3 | sí | ninguno; frase del inventario desaparecida: se marcó el paso 4 |
| c1-m7-18 | respaldada | **Cleveland et al. §2.4** | sí | ninguno |
| c1-m8-02 | respaldada | **FPP3 §3.2** | sí | ninguno |
| c1-m8-03 | con-matiz | **FPP3 §3.2**; §3.5 | sí | **ajustada**: «—desempleo, producción—» → «—las de desempleo, por ejemplo—» |

Las cuatro que ya estaban y no se tocaron: `c1-m6-01`, `c1-m6-02`, `c1-m7-03`, `c1-m8-01`.

## Los `con-matiz`: nota o ajuste

| id | matiz | decisión |
|---|---|---|
| c1-m1-04 | Cryer y Chan fechan su archivo en 1960–1971; el rango 1949–1960 solo lo da la ayuda de R | resuelto con la ayuda de R (punto 5); queda la nota sobre las fechas de Cryer y Chan |
| c1-m3-08 | FPP3 respalda la conclusión (multiplicativo), no la lectura visual del abanico | nota; la cita va pegada a lo que la fuente sostiene |
| c1-m4-06 | la fuente habla de su propia práctica, no de «muchos textos» | **prosa ajustada** |
| c1-m6-13 | la numeración de los pasos difiere y las fórmulas de normalización son del capítulo | nota: el capítulo no atribuye la tabla a nadie |
| c1-m7-01 | ninguna fuente escribía la forma del capítulo | **prosa corregida** (punto 5) |
| c1-m7-16 | «hasta que se estabilizan» (frase vieja) sugería un criterio de parada | nota: la frase vigente ya no lo dice |
| c1-m8-03 | FPP3 no dice nada de la «producción» | **prosa ajustada** |

## Lo resuelto del punto 5

**`c1-m1-04` · el rango 1949–1960.** La ayuda de R (`AirPassengers`, R 4.6.0 · datasets 4.6.0) lo dice
en su sección Description: «Monthly totals of international airline passengers, 1949 to 1960», y «in
thousands» en Format. Esas citas las localizó el redactor por indicación de la sesión maestra y las
comprobó con `grep`; **no pasaron por el verificador R4a**, que solo leyó Cryer y Chan. Por eso el
veredicto se queda en `con-matiz`.

**`c1-m7-01` · el acrónimo.** Qué dice cada fuente:

- Cleveland et al. (1990): nunca lo desarrollan en prosa; solo el título, «STL: A Seasonal-Trend
  Decomposition Procedure Based on Loess».
- FPP3 §3.6: «STL is an acronym for “Seasonal and Trend decomposition using Loess”».
- Ayuda de `stl()`: «…components using ‘loess’, acronym STL».

El capítulo copia ahora la forma de FPP3 y la cita: «STL (*Seasonal and Trend decomposition using
Loess*; Hyndman y Athanasopoulos, 2021, §3.6)».

**«Loess» desarrollado como «locally estimated scatterplot smoothing».** Seguía en el capítulo y no está
en ninguna fuente leída. Cleveland et al., p. 5: «locally-weighted regression, or loess» (en el OCR,
«locally-» cae a final de renglón). Shumway y Stoffer: «locally weighted regression (lowess)» en el pie
de la figura 2.14 (p. 75) y «locally weighted scatterplot smoothing (lowess)» en la p. 64. El capítulo
dice ahora «**Loess** —regresión local ponderada, *locally weighted regression*—».

## Citas sustituidas, recortadas o añadidas

Todas las citas del registro se comprobaron con `grep -c -F` contra la caché y con la normalización del
auditor: `diagnostico/cap1/comprobaciones/r4_comprueba_citas.py` y su `.out` (77 citas, 0 con problema).

| id | la que dio el verificador | la que quedó | motivo |
|---|---|---|---|
| c1-m7-10 | «chosen to be 35; the right side of the inequal-» | «chosen to be 35; the right side of the» | acaba en guion de corte de renglón; el auditor une la palabra partida y no la encuentra |
| c1-m7-16 | «loop followed by a computation of robust-» | «loop followed by a computation of» | lo mismo |
| c1-m7-02 | «the robustness iterations and set ,,,= 0;in» | retirada | está en la caché, pero el subíndice n_o sale destrozado del OCR; lo cubren las otras dos de §3.3 |
| c1-m7-16 | «inner: integer; the number of 'inner' (backfitting) iterations;» | la misma, más «usually very few (2) iterations suffice.» | la continuación de la misma entrada de la ayuda es la que dice lo de las dos pasadas |
| c1-m7-01, -10, -15, -16 | citas de la ayuda de R con comillas rectas | las mismas, con las comillas tipográficas de la instantánea | copiadas de `_local/web/rcoreteam2026r/stl.txt`; el ajuste de línea coincidió en todas |
| todas las de R | `clave: rdoc`, `loc: "§3.6"`, `tema: stl` | `clave: rcoreteam2026r`, `loc: "§Usage"` (etc.), `instantanea: stl` | la clave de la biblioteca y el localizador por sección |
| c1-m1-04 | (ninguna para el rango) | tres de la ayuda de R | punto 5 |
| c1-m7-05 | (en su nota, no en su lista) | Cleveland et al. p. 5, «weighted regression, or loess (Cleveland and» | sostiene el desarrollo corregido de Loess |
| c1-m7-05 | — | Shumway y Stoffer p. 75, fig. 2.14 | **añadida por el redactor, sin verificador**: sostiene la forma sin guion |
| c1-m7-15 | «lags) of the loess window for seasonal extraction, which» (la dio para c1-m7-06) | la misma, movida aquí | lo de `s.window` quedó en el paso 1 |
| c1-m5-01 | `loc: "§3.3; ec. 3.2"` | `loc: "§3.3"` | cita visible más corta; la ec. 3.2 está en §3.3 |
| c1-m5-02 | dos citas de FPP3 | una | tope F11 |
| c1-m6-14 | dos citas de FPP3 | una (la multiplicativa) | la frase marcada solo habla de ese caso; tope F11 |
| 26 citas de FPP3 | tramos de 7 a 23 palabras | subtramos de 4 a 14 palabras de esos mismos pasajes | **tope F11: 400 palabras citadas por obra**; con las citas completas FPP3 llegaba a 598. Quedó en 398 |

## Cambios fuera del capítulo y del registro

- **`precalculo/audita_citas.py`**: el vocabulario cerrado no admitía `§Details`. Se añadieron los
  nombres de sección de una ayuda de R (`§Description`, `§Usage`, `§Arguments`, `§Format`, `§Details`,
  `§Value`, `§Source`, `§References`) y `seccion_de()` acota la búsqueda a esa sección de la
  instantánea, igual que hace con «§3.6» en FPP3. `prueba_audita_citas.py` sigue dando 24 de 24.
  **Es una extensión local de la norma común de los cuatro cursos**: hay que decidir si sube a la norma.
- `bibliografia/README.md`: una frase que documenta esos localizadores.
- `bibliografia/uso_fuentes.json`: regenerado con `--uso` (27 obras, 5 en uso).

## Listas de fuentes de módulo

Se añadió el `<aside class="fuentes-modulo">` con sus marcadores a los módulos **1, 3, 4 y 5**. Los
módulos 2 y 9 no llevan ninguna cita y se dejaron sin él. M6, M7 y M8 ya lo tenían; la lista del M7 pasó
de una obra a tres.

## Lo que queda `pendiente`

Nada entre lo registrado. Fuera de esta ronda quedan sin marcar ni registrar las otras **75 filas del
inventario** (prioridad media y baja), entre ellas `c1-m8-13`, la retroalimentación de la autoevaluación
que dice «las cifras oficiales de empleo o PIB»: el PIB tampoco está en FPP3, y es la misma promesa que
se retiró de `c1-m8-03`.

## Comprobaciones

- `python3 precalculo/audita_citas.py`: OK · 33 citas visibles · 32 afirmaciones · 88 citas literales
  comprobadas. Un aviso heredado: `c1-m6-02` está respaldada y no lleva cita visible (así la dejó la R3).
- `python3 precalculo/verifica_todo.py`: 11 verificadores en verde.
- Chrome sin ventana, 1200 y 375 px, los nueve módulos: consola limpia, 0 `.katex-error`, el documento no
  desborda, ninguna cita se sale ni apunta a una entrada inexistente, y las listas de fuentes caben. El
  espaciado de la tabla del Módulo 6 es idéntico al de antes de envolverla (16/32 px y 14/28 px).

## Para la mirada del docente

1. **`c1-m7-07`**: el párrafo explica `s.degree = 0` con una razón del capítulo («pedirles una pendiente
   sería pedirle demasiado a doce puntos»). El artículo original suaviza las subseries con grado 1: el 0
   es una decisión de R. La fuente respalda los valores, no la razón.
2. **Cómo se lee «(R Core Team, 2026, §Details)»**: el localizador es la sección de la página de ayuda, y
   la cita no dice de qué página (`stl`, `AirPassengers`); se deduce del contexto.
3. **La entrada de R en las listas** sale como «…Statistical Computing: 4.6.0 (Versión 4.6.0)»: la
   versión está dos veces en los metadatos de Zotero.
4. **El tope de 400 palabras por obra** deja a FPP3 en 398: la próxima afirmación que se contraste con
   FPP3 no cabe sin recortar otra o sin revisar el tope.
5. Las tres frases reescritas (`c1-m4-06`, `c1-m7-01` con el desarrollo de Loess en `c1-m7-05`, y
   `c1-m8-03`) y el veredicto de `c1-m1-04`, que esperan al verificador posterior.

---

# Corrección tras la verificación independiente (2026-11-13)

Un verificador de contexto limpio leyó las fuentes y las 28 afirmaciones; la sesión maestra comprobó los
hallazgos decisivos y encargó aplicarlos. Sin commits.

## Estado vigente

- **31 afirmaciones**: 24 `respaldada`, 7 `con-matiz` (`c1-m3-08`, `c1-m4-06`, `c1-m6-13`, `c1-m7-01`,
  `c1-m7-05`, `c1-m7-16` y la heredada `c1-m6-01`), 0 `pendiente`.
- **36 citas visibles**: 22 de FPP3, 7 de la ayuda de R, 7 de Cleveland et al. (1990).
- Veredictos movidos, todos por encargo: suben `c1-m1-04` y `c1-m8-03` (los comprobó la sesión maestra);
  baja `c1-m7-05`.
- Identificadores: `c1-m4-02` absorbe a `c1-m4-03` y `c1-m4-04`, que salen del registro; nace `c1-m7-23`.
- `audita_citas.py` sale sin ningún aviso; `verifica_todo.py`, 11 en verde.
- Ninguna cifra, gráfico, simulador ni dato tocado.

## Punto por punto

| # | id | qué pedía | qué se hizo |
|---|---|---|---|
| 1 | c1-m4-06 | la frase atribuía a dos autores lo que la fuente da como práctica habitual, y la cita recortaba «we usually» | voz impersonal: «Al descomponer una serie suele agruparse tendencia y ciclo en un solo componente *tendencia-ciclo* $T_t$, al que a menudo se llama simplemente tendencia (Hyndman y Athanasopoulos, 2021, cap. 3)». Cita registrada entera, con «we usually» y «(often just called the trend for simplicity)». Sigue `con-matiz`: la frase es del redactor y la comprueba la sesión maestra |
| 2 | c1-m7-05 | localizador del nombre en p. 5; retirar a Shumway y Stoffer; bajar a `con-matiz` por «recta por mínimos cuadrados» | Shumway y Stoffer fuera de `fuentes` (la nota dice que su figura glosa *lowess*). Veredicto `con-matiz`, con el matiz en la nota: polinomio de grado 1 o 2, mínimos cuadrados **ponderados**. El localizador p. 5 va con el nombre, que cambió de párrafo (punto 3) |
| 3 | c1-m7-05 | la glosa nueva adelantaba «ponderada» y estropeaba la revelación | la primera mención dice solo «**Loess** —una regresión local—». El nombre completo pasó al párrafo que revela *ponderada*: «Con su nombre completo, Loess es una regresión local ponderada (*locally weighted regression*; Cleveland et al., 1990, p. 5)». Como una cita tiene que ir dentro de una afirmación y ese párrafo no tenía marca para el nombre, **nace `c1-m7-23`** (`respaldada`, Cleveland p. 5). `c1-m7-05` conserva su cita visible en §2.1, que es donde está el mecanismo que afirma |
| 4 | c1-m7-07 | la marca envolvía las razones y la fuente solo respalda los valores | el `</span>` cierra tras «responden a dos problemas distintos». Sigue `respaldada`. La nota deja escrito que Cleveland §2.3, paso 2, suaviza las subseries con d = 1 y que el 0 es decisión de R. La derivación no se reescribió |
| 5 | c1-m7-16 | matiz vivo: las dos pasadas son el defecto solo con `robust = FALSE` | prosa: «—dos pasadas por defecto, con la opción robusta apagada—». Cita visible en `§Usage`, con la cita literal `inner = if(robust)  1 else 2,`. Nota reescrita con ese matiz. Sigue `con-matiz` |
| 6 | c1-m1-04 | «in thousands» está en §Format; sacar a Cryer y Chan; subir a `respaldada` | localizador visible `§Description; §Format`. Cryer y Chan fuera de `fuentes`: va en la nota, con sus fechas. `respaldada`, `verificado_por` la sesión maestra |
| 7 | c1-m8-03 | subir a `respaldada`; dejar la reserva real en la nota | hecho. La nota recoge que la fuente da como finalidad «highlight variation due to the underlying state of the economy» |
| 8 | c1-m8-13 | quitar «o PIB» de la retroalimentación y registrarla | «las cifras oficiales de empleo: sin ajustar…». **No se pudo registrar**: la frase vive en una cadena de JavaScript (el banco de la autoevaluación) y el auditor no lee `data-afirma` dentro de `<script>`; una entrada sin marca legible haría fallar F03. Queda anotado en la nota de `c1-m8-03` |
| 9 | c1-m3-08 | la cita respaldaba a la vista dos oraciones y la fuente solo sostiene la segunda | la marca empieza en «Esa forma es la señal…» |
| 10 | c1-m7-15 | el localizador debía cubrir §2.2 y §2.3; «el patrón queda fijo» es de FPP3 §3.6 | cita visible `§2.2; §2.3`; la de R §Details se quedó junto a «la media de la subserie» y se añadió la de FPP3 §3.6 tras «el patrón queda fijo», con la cita literal «periodic season(window='periodic') (i.e., identical across years)» |
| 11 | c1-m6-20 | lo de la media móvil es §3.3 | cita visible `§3.3; §3.4` |
| 12 | c1-m6-09 | faltaba la cita multiplicativa; el mecanismo es del capítulo | añadida «detrended series: y_t / \hat{T}_t.»; la nota lo dice |
| 13 | c1-m6-14 | cerrar la marca en «…de la última fila de la tabla» | hecho; la cita visible va ahí y lo del paso 3c queda fuera |
| 14 | c1-m4-04 / -07 | «varios años» frente a «al menos dos años» | a la viñeta se le quitó la cifra: «(p. ej. los ciclos económicos)» |
| 15 | c1-m1-01 | reescribir la nota | reescrita: la cita de FPP3 es una declaración de alcance, y lo univariante no lo cubre ninguna |
| 16 | c1-m7-10 | la cita partía «la regla» de su complemento | «…con la regla que da su ayuda (R Core Team, 2026, §Arguments): tomar el impar inmediato de». La frase acaba en «de» y le sigue la fórmula, así que la cita no podía ir al final literal: quedó antes de los dos puntos |
| 17 | c1-m7-07 | la cita partía sujeto y verbo | inciso: «Los dos grados por defecto —los que trae la línea de uso de `stl()` (R Core Team, 2026, §Usage)— responden a dos problemas distintos» |
| 18 | M4, lista | fundir las tres viñetas en `c1-m4-02` | ver abajo |
| 19 | c1-m7-01 | dos formas del acrónimo a dos pantallas | inciso tras el paréntesis: «—el título del artículo original lo escribe con guion y «based on»: *A Seasonal-Trend Decomposition Procedure Based on Loess* (Cleveland et al., 1990, p. 3)—» |
| 20 | c1-m6-13 | reindentar el bloque del `div` | hecho: lo contenido va dos espacios más adentro |
| 21 | c1-m6-02 | el aviso F03 heredado | dos citas visibles: §3.4 tras «las caídas rápidas de la serie» y §3.6 al final. La prosa no cambió; la huella sí (espacio antes del punto), y se actualizó en su entrada |

## Punto 18 · la estructura elegida

`<ul data-afirma="c1-m4-02">` envuelve las cuatro viñetas; la única cita visible, «(Hyndman y
Athanasopoulos, 2021, §2.3)», va al final de la viñeta de la **tendencia**. Las viñetas de
estacionalidad y ciclo recuperan sus paréntesis originales, que la primera pasada había cambiado por
rayas para acomodar las citas. La entrada única conserva las citas literales de las tres definiciones
(más la de las condiciones económicas del ciclo y la de Cryer y Chan sobre la palabra *tendencia*).
`c1-m4-03` y `c1-m4-04` salen del registro, y la `afirmacion` y la nota dicen que FPP3 §2.3 define los
tres primeros componentes y que **el ruido lo define el capítulo**: la huella lo vigila porque está en
la lista, pero ninguna cita lo cubre. No se añadió la cita opcional del cap. 3 sobre el «remainder».

## Palabras citadas por obra (tope F11: 400)

| obra | antes | ahora |
|---|---|---|
| FPP3 | 398 | **393** |
| Cleveland et al. (1990) | 192 | 192 |
| ayuda de R | 103 | 109 |
| Shumway y Stoffer | 44 | 36 |
| Cryer y Chan | 26 | 12 |

FPP3 ganó tres citas (la entera del cap. 3, la multiplicativa de §3.4 y la de §3.6) y hubo que recortar
ocho para hacerles sitio, siempre a un subtramo del mismo pasaje: `c1-m8-02` («the resulting values are
the “seasonally adjusted” data.»), las dos de `c1-m4-11` («does not vary with the level», «proportional
to the level»), `c1-m5-02`, `c1-m7-01`, `c1-m4-07`, `c1-m6-13` y la aditiva de `c1-m6-09`. Quedan 7
palabras de margen.

## Comprobaciones de la corrección

- Las 78 citas del registro de esta ronda, con `grep -c -F` y con la normalización del auditor:
  `comprobaciones/r4_comprueba_citas.out`, 0 con problema.
- `audita_citas.py`: OK, sin avisos · 36 citas visibles · 31 afirmaciones · 89 citas literales comprobadas.
- `verifica_todo.py`: 11 en verde.
- Chrome sin ventana, 1200 y 375 px, los nueve módulos: consola limpia, 0 `.katex-error`, el documento
  no desborda, ninguna cita se sale ni queda sin destino, las listas de fuentes caben.

## Lo que queda para la sesión maestra y el docente

1. Frases escritas por el redactor y sin verificador: `c1-m4-06`, `c1-m7-16`, `c1-m7-23`, el inciso de
   `c1-m7-01` y la glosa «una regresión local» de `c1-m7-05`.
2. `c1-m7-23` es una entrada que el encargo no nombraba: la exige la regla de que toda cita vaya dentro
   de una afirmación. Está como `respaldada` con el verificador del lote R4b, que fue quien halló el
   pasaje; si se prefiere otro veredicto hasta comprobarla, es una línea.
3. `c1-m8-13` corregida y sin registrar, por la limitación del auditor con las cadenas de JavaScript.
4. La derivación de `s.degree = 0` (`c1-m7-07`), que se plantea a Javier.

---

# Cierre de la R4 · lo que hizo la sesión maestra

Después de la corrección, la sesión maestra comprobó por su cuenta las fuentes y cerró cinco cosas que
el redactor dejó esperando verificación. Nada de esto lo escribió el redactor salvo donde se dice.

## La ficha de R en las listas de referencias

La lista imprimía «R: A Language and Environment for Statistical Computing**: 4.6.0** (Versión 4.6.0)».
El campo Extra de Zotero se quedó con `volume: 4.6.0` al importar el RIS —la etiqueta `VL` de un ítem
«Programa informático» no tiene campo propio y Zotero la deja ahí—, pandoc lo lee como la variable CSL
`volume` y el estilo APA lo pega al título. Enmienda nueva en `bibliografia/enmiendas.yml`
(`rcoreteam2026r.note: ""`), con la evidencia y la nota de que lo correcto a la larga es vaciar el campo
Extra en Zotero y borrar la enmienda. Comprobado fuera del repo con pandoc antes de aplicarlo.

## La apertura del Módulo 7

El inciso del punto 19 quedó dentro de la primera frase del módulo: entre el sujeto «STL» y su verbo
«responde» había cuarenta y cuatro palabras y tres incisos encadenados. Es la frase que anuncia qué hace
STL. La sesión maestra lo sacó a frase propia, después de «…por regresión ponderada (Loess)», con su
marca y su cita: **entrada nueva `c1-m7-24`**, `respaldada`, el título comprobado contra la portada del
PDF (página 1 del escaneo, página impresa 3; el OCR lo parte en dos renglones, de ahí las dos citas).
`c1-m7-01` se queda solo con el desarrollo del acrónimo y su huella se recalculó.

## Cuatro veredictos cerrados

| id | antes | ahora | qué se comprobó |
|---|---|---|---|
| `c1-m7-01` | con-matiz | **respaldada** | FPP3 `decomposition.txt:464`: «STL is an acronym for “Seasonal and Trend decomposition using Loess”». El matiz que tenía —el título del artículo— ya vive en `c1-m7-24` |
| `c1-m4-06` | con-matiz | **respaldada** | FPP3 `decomposition.txt:5`: «we usually combine the trend and cycle into a single trend-cycle component (often just called the trend for simplicity)». La frase vigente lo dice en voz impersonal y con el «se le llama simplemente tendencia» |
| `c1-m7-16` | con-matiz | **respaldada** | ayuda de `stl()`, `stl.txt:17`: `inner = if(robust)  1 else 2`. La condición que faltaba está escrita en la prosa |
| `c1-m7-23` | respaldada | respaldada | `verificado_por` corregido: la frase es nueva y el verificador del lote R4b no la leyó. Comprobada contra `p0003.txt` (página impresa 5) |

## Estado al cerrar

- **32 afirmaciones**: 28 `respaldada`, 4 `con-matiz`, 0 `pendiente`. **36 citas visibles.**
- `audita_citas.py`: OK y **sin ningún aviso**; 89 citas literales comprobadas.
- `verifica_todo.py`: 11 verificadores en verde.
- Navegador a 1200 y 375 px: consola limpia, 0 `.katex-error`, `scrollWidth == clientWidth` en las dos
  anchuras, ninguna cita sin destino.

## Lo que queda abierto, para Javier

1. **`c1-m7-07`, la razón de `s.degree = 0`.** El capítulo la explica con una razón propia («pedirles una
   pendiente sería pedirle demasiado a doce puntos»). Cleveland et al. §2.3, paso 2, suavizan las
   subseries con grado 1: el 0 es decisión de R, no del artículo. La huella se recortó para que la marca
   cubra solo los valores, y la nota lo deja escrito. **La derivación no se reescribió**: es decisión del
   docente si el capítulo debe decirlo.
2. **`c1-m8-13` no se puede registrar.** Se retiró «o PIB» de la retroalimentación de la autoevaluación,
   pero esa frase vive en una cadena de JavaScript y el auditor no lee `data-afirma` dentro de `<script>`:
   la afirmación quedó corregida y sin marca. Es un hueco del mecanismo, no de esta ronda.
3. **La extensión del vocabulario de localizadores** (`§Description`, `§Usage`, `§Arguments`…) es local de
   Series. Hay que decidir si sube a la norma común de los cuatro cursos, que escribe la sesión de Muestreo.
4. **El tope F11 de 400 palabras por obra** deja FPP3 en 393: la próxima afirmación que se contraste con
   FPP3 obliga a recortar otra o a revisar el tope.
5. **Las 75 filas restantes del inventario** (prioridad media y baja) siguen sin marcar ni registrar.
