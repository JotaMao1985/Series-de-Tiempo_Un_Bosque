# Plan · Bloque E, los gráficos de series de FPP3 §2

Series de Tiempo 2026-II (20948) · Universidad El Bosque

**Fecha del plan:** 2026-09-01
**Encargo:** que el banco de preguntas evalúe el capítulo 2 de FPP3
(*Time series graphics*, <https://otexts.com/fpp3/graphics.html>), que hoy
cubre solo a medias.
**Estado:** 🟢 Fases 0, 1, 2 y 4 completas. Queda la 3 —que espera la pregunta
abierta 1, qué par de series para §2.6— y la 5 (cierre).

> El parcial del Corte I es **hoy**. Nada de esto lo toca: el bloque E se
> publica después, y su público son el Corte II, un supletorio o el repaso.
> Eso quita la prisa y es la razón de que se pueda hacer bien.

---

## 0 · El hueco, medido

Se cruzaron los 38 ítems del preparcial contra las nueve secciones de FPP3 §2.
El Corte I está construido alrededor de descomposición y estacionariedad, así
que **cae de lleno en la segunda mitad del capítulo y se salta la primera**.

| FPP3 §2 | Hoy en el banco | Ítems |
|---|---|---|
| 2.1 `tsibble` objects | ✗ | B01 existe pero es numérica (fuera), y evalúa `ts()`, no `tsibble` |
| 2.2 Time plots (`autoplot`) | ✗ | ninguno |
| 2.3 Patrones: tendencia / estacional / **ciclo** | parcial | A02 y S01 van de componentes; nada de ciclo vs estacionalidad |
| 2.4 Seasonal plots (`gg_season`) | débil | D03 usa un `gg_season`, pero pregunta por STL robusto |
| 2.5 Seasonal subseries (`gg_subseries`) | ✓ | D02 |
| 2.6 Scatterplots (dos series) | ✗ | ninguno — todo el Corte I es univariado |
| 2.7 Lag plots (`gg_lag`) | ✓✓ | D06, S04 |
| 2.8 Autocorrelación (ACF) | ✓✓✓ | C05, D01, D05, D07 |
| 2.9 Ruido blanco | débil | D04 (B04 se quedó fuera por numérica) |

Los capítulos 1 y 2 **sí** enseñan lo que falta —el módulo 1.4 se titula
*«Trend, seasonality, cycle & noise»* y usa `as_tsibble`, `autoplot`,
`gg_season`, `gg_subseries` y `gg_lag`—. El hueco es de evaluación, no de
material.

---

## 1 · Decisiones tomadas

| Decisión | Elegido | Consecuencia |
|---|---|---|
| Dónde viven las preguntas nuevas | **En el preparcial, bloque E** | Entran con precálculo en R, los dos auditores y el rasterizador. Más trabajo por ítem, pero las cifras y las figuras salen de R como todo lo demás |
| Alcance | **Todo, §2.6 incluido** | Hay que añadir un par de series relacionadas al precálculo: es la única parte que necesita datos nuevos |
| Cosecha de los capítulos 1 y 2 | **Sí, sin los de varias respuestas** | +10 ítems ya escritos y verificados, sin meter el Multi-Select que nunca se ha importado a un Brightspace real |

### Decisiones de arquitectura

0. **CORRECCIÓN (2026-09-01, al implementar): el bloque E queda FUERA del
   diagnóstico.** El plan lo metía en `BLOQUES` sin mirar la §6 del
   verificador: el termómetro calca el blueprint del parcial, cuyos pesos
   publicados —15/20/15/20/20/10— se cumplen hoy con **1.9 puntos de margen**
   sobre los 2 que esa sección tolera. Un solo ítem más movería el reparto
   fuera de la banda y el diagnóstico dejaría de medir lo que dice medir. El
   bloque E evalúa gráficos que están en el material pero no en el blueprint:
   es práctica, como el simulacro, y como él vive fuera del termómetro. Esto
   además **desbloquea el resto del plan**, que si no habría tenido que añadir
   los seis ítems de golpe para no descuadrar los pesos.

1. **El bloque E es un módulo propio (`module-6`), no un segundo quiz dentro
   del D.** `BLOQUES` codifica «un bloque, un módulo» y el diagnóstico lee de
   ahí. Obliga a renumerar 6→7, 7→8, 8→9, que es mecánico y está acotado:
   nadie enlaza a un `#modulo-N` concreto del preparcial y la navegación se
   genera sola desde `courseData.modules`.
2. **El rasterizador pasa a capturar por `[data-quiz]`, no por módulo.** Hoy
   asume un quiz por módulo; funcionó de milagro con el simulacro porque está
   solo en el suyo. Sin esto, el mapa imagen↔ítem se rompe en silencio en
   cuanto un módulo tenga dos quizzes, y ese defecto no da síntoma.
3. **CORRECCIÓN (2026-09-01): el bloque E no lo cubren §3 ni §4 del
   verificador de R**, que recorren `1:32` —los ítems del blueprint— y son las
   que exigen que cada cifra impresa tenga origen en el precálculo. E04 no
   trae cifras del material y no lo necesita, pero **el primer ítem del bloque
   E que publique una cifra tiene que entrar antes en esas dos secciones**.
   Va como criterio de aceptación de la Tarea 4.

4. **El ítem de ciclo vs estacionalidad NO se escribe.** Ya existe en la
   autoevaluación del capítulo 1, y `verifica_preparcial.R` §7 rechaza los
   casi-duplicados de los 56 ítems que el estudiante ya vio. Lo cubre la
   cosecha, que es justo para lo que sirve.
5. **La cosecha no reescribe ítems: los lee.** El exportador aprende la forma
   de capítulo (`modulo: N` en vez de `clave: '1.4'`) y filtra `multiple`.

---

## 2 · El grafo de dependencias

```
genera_preparcial.R  (par bivariado + series de E02/E03)
        │
        └── salidas/preparcial_datos.json ── PREPARCIAL_DATOS en el HTML
                        │
                        └── bloque E en el HTML (ítems + funciones de dibujo)
                                 │
                                 ├── verifica_preparcial.R  §3 §4 §5 §6 §7
                                 ├── audita_preparcial.py   (afirmación pedagógica)
                                 ├── audita_posicion_correcta.py
                                 │
                                 └── rasteriza_graficos.js  (por [data-quiz])
                                          │
                                          └── exporta_brightspace.py
                                                   ├── audita_paquete.py  (skill)
                                                   ├── audita_brightspace.py
                                                   └── exporta_qti.py → verifica_qti.py

cosecha de cap1/cap2 ── lector de forma de capítulo ──┘   (independiente hasta aquí)
```

---

## 3 · Las preguntas

**Bloque E · Gráficos de series — 6 ítems**

| | FPP3 | Qué evalúa | Necesita |
|---|---|---|---|
| E01 | 2.1 | `as_tsibble(index=, key=)` sobre datos con clave duplicada: qué distingue índice de clave y por qué falla | — |
| E02 | 2.2 | Un gráfico de tiempo: qué patrón se ve en él y cuál **no** puede verse ahí | figura |
| E03 | 2.4 | `gg_season` con un año que se despega: qué muestra que el gráfico de tiempo esconde | figura |
| E04 | 2.4 | `gg_season(period=)` y la estacionalidad múltiple | — |
| E05 | 2.6 | Dispersión de dos series con $r = 0.8$ y relación en U: por qué el coeficiente engaña | figura + datos |
| E06 | 2.6 | Correlación espuria entre dos series con tendencia | figura + datos |

**Dos conversiones** (de numérica a opción múltiple, en el material):

| | FPP3 | Por qué | Distractor que el material ya nombra |
|---|---|---|---|
| B01 | 2.1 | Es el ítem de construcción del índice temporal, y está fuera del banco solo por ser numérica | 2022 (sumar 30 en vez de 29) |
| B04 | 2.9 | Es *el* ítem de ruido blanco: bandas ±2/√T con T = 200 y 36 rezagos | 0 (creer que la banda contiene todo) |

Las dos necesitan **dos distractores más cada una**, calculados en R, no
escritos a mano.

**Cosecha:** 10 ítems de una sola respuesta de `AUTOEVALUACIONES['cap1']` y
`['cap2']` (5 y 5; quedan fuera 4 numéricas y 2 de varias respuestas).

**Tamaño final del banco:** 28 + 6 + 2 + 10 = **46 ítems**. Hoy van **44**:
faltan E05 y E06, que son los de §2.6.

---

## 4 · Tareas

### Fase 0 · El terreno

#### Tarea 1: El rasterizador captura por quiz, no por módulo  ✅ *hecha, `b43763e`*

**Descripción:** `rasteriza_graficos.js` recorre módulos y captura todos los
`.quiz-grafico canvas` que encuentre. Pasa a recorrer contenedores
`[data-quiz]` / `[data-simulacro]`, de modo que el nombre del PNG derive del
bloque al que pertenece el ítem y no del módulo que lo contiene.

**Criterios de aceptación:**
- [ ] Los ocho PNG actuales salen con el mismo nombre que hoy
- [ ] Un módulo con dos quizzes produce nombres distintos por bloque
- [ ] Si un bloque declara N ítems de tipo `grafico` y aparecen M ≠ N lienzos, para

**Verificación:** `node precalculo/rasteriza_graficos.js` · el inventario
lista `bloque-d_1..7` y `simulacro_1` igual que antes; `python3
precalculo/exporta_brightspace.py` y los dos auditores siguen limpios.

**Dependencias:** ninguna · **Archivos:** `precalculo/rasteriza_graficos.js` ·
**Tamaño:** S

#### Tarea 2: Módulo 6 vacío para el bloque E  ✅ *hecha, `b43763e`*

**Descripción:** Insertar `<template id="module-6">` con el encabezado del
bloque E y su `<div data-quiz="bloque-e">`, renumerar 6→7, 7→8, 8→9, y añadir
la entrada a `BLOQUES` y a `courseData.modules`.

**Criterios de aceptación:**
- [ ] La navegación muestra nueve módulos en orden y todos cargan
- [ ] El diagnóstico y el termómetro siguen funcionando con el bloque E vacío
- [ ] `AUTOEVALUACIONES['bloque-e'] = []` no rompe `estadoDeObjetivos()`

**Verificación:** servidor `htmls-series`, recorrer los nueve módulos y
comprobar consola sin errores; `python3 precalculo/audita_posicion_correcta.py`
sigue pasando.

**Dependencias:** ninguna · **Archivos:** `Htmls_Series/preparcial-corte-1.html`
· **Tamaño:** M

### ✅ Punto de control · Terreno
- [ ] El preparcial se ve igual que antes, con un módulo más vacío
- [ ] El banco se regenera con los mismos 28 ítems y las cuatro auditorías limpias

### Fase 1 · Lo que no necesita datos nuevos

#### Tarea 3: E01 y E04, y las dos conversiones  ✅ *hecha* (`bd62c85` y E01 aparte)

**Descripción:** Escribir E01 (`as_tsibble` índice vs clave) y E04
(`gg_season(period=)`), y convertir B01 y B04 de numérica a opción múltiple
con cuatro opciones cada una. Los distractores que faltan se calculan en
`genera_preparcial.R`, no se escriben a mano.

**Criterios de aceptación:**
- [ ] Cuatro opciones por ítem, con explicación por opción de por qué falla cada distractor
- [ ] Toda cifra de las opciones sale de `PREPARCIAL_DATOS`, ninguna escrita a mano
- [ ] La correcta no cae siempre en la misma posición

**Verificación:** `Rscript precalculo/genera_preparcial.R` ·
`Rscript precalculo/verifica_preparcial.R` (§3, §4, §5, §7) ·
`python3 precalculo/audita_preparcial.py` ·
`python3 precalculo/audita_posicion_correcta.py`

**Dependencias:** Tarea 2 · **Archivos:** `preparcial-corte-1.html`,
`precalculo/genera_preparcial.R` · **Tamaño:** M

### Fase 2 · Los que necesitan figura

#### Tarea 4: E02 y E03, con sus gráficos  ✅ *hecha*

**Descripción:** El gráfico de tiempo de E02 y el `gg_season` de E03, dibujados
con Chart.js sobre series que ya existen en el precálculo, más los dos ítems.

**Criterios de aceptación:**
- [ ] Las dos figuras se dibujan desde `PREPARCIAL_DATOS`, sin datos incrustados en la función de dibujo
- [ ] Cada figura tiene su `descripcionGrafico`, que es el `alt` que viaja al banco
- [ ] La afirmación de cada ítem se sostiene sobre los datos: lo que el ítem dice que se ve, se ve

**Verificación:** las de la Tarea 3, más `node precalculo/rasteriza_graficos.js`
(los dos PNG con más del 1 % de píxeles con tinta) y la vista previa.

**Dependencias:** Tarea 3 · **Archivos:** `preparcial-corte-1.html`,
`genera_preparcial.R`, `audita_preparcial.py` · **Tamaño:** M

### ✅ Punto de control · Sin datos nuevos  ✅ *superado*
- [x] Banco de **34 ítems** · 401 comprobaciones de R · los tres auditores del paquete en 421 / 490 / 285
- [x] FPP3 §2.1, §2.2, §2.4 y §2.9 cubiertos
- [x] Las seis afirmaciones de E02 y E03 comprobadas contra el dato en `audita_preparcial.py`
- [ ] Revisar con el humano antes de tocar los datos

### Fase 3 · §2.6, el caro

#### Tarea 5: El par de series relacionadas

**Descripción:** Añadir a `genera_preparcial.R` dos pares bivariados: uno con
relación en U y correlación lineal alta (el clásico demanda contra
temperatura), y otro de dos series con tendencia y correlación espuria. Con su
comprobación de que la afirmación pedagógica se sostiene: que $r$ salga
efectivamente alto **y** que la relación sea claramente no lineal.

**Criterios de aceptación:**
- [ ] Las dos parejas viajan en `PREPARCIAL_DATOS.series` con su descripción y unidad
- [ ] `verifica_preparcial.R` §2 las acepta como series de forma válida
- [ ] Una comprobación nueva exige $r > 0.75$ y una prueba de no linealidad que la delate

**Verificación:** `Rscript precalculo/genera_preparcial.R` y
`Rscript precalculo/verifica_preparcial.R`

**Dependencias:** Tarea 4 · **Archivos:** `genera_preparcial.R`,
`verifica_preparcial.R` · **Tamaño:** M

#### Tarea 6: E05 y E06, con sus dispersiones

**Descripción:** Los dos ítems de §2.6 y sus dos gráficos de dispersión.

**Criterios de aceptación:**
- [ ] E05 castiga leer la correlación sin mirar la nube; E06, correlacionar dos tendencias
- [ ] Cuatro opciones y explicación por opción en los dos
- [ ] Ninguno duplica un ítem de los capítulos (§7)

**Verificación:** las de la Tarea 4 · **Dependencias:** Tarea 5 ·
**Archivos:** `preparcial-corte-1.html`, `audita_preparcial.py` ·
**Tamaño:** M

### ✅ Punto de control · Bloque E completo
- [ ] 38 ítems en el banco, las nueve secciones de FPP3 §2 con al menos uno
- [ ] La tabla de especificaciones publicada concuerda con el reparto real (§6)

### Fase 4 · La cosecha

#### Tarea 7: El exportador lee también los capítulos  ✅ *hecha*

**Descripción:** Enseñar a `exporta_brightspace.py` la forma de ítem de
capítulo (`modulo: N`, sin `clave`) y añadir `--capitulos` para incluirlos,
filtrando los de tipo `multiple`.

**Criterios de aceptación:**
- [ ] Los 10 ítems de una sola respuesta de cap1 y cap2 entran con su título de módulo
- [ ] Los de varias respuestas quedan fuera y el informe los nombra
- [ ] Ningún `qid` choca con los del preparcial

**Verificación:** las cuatro auditorías sobre el banco combinado; el informe
declara 0 Multi-Select.

**Dependencias:** Tarea 6 · **Archivos:** `precalculo/exporta_brightspace.py`,
`precalculo/audita_brightspace.py` · **Tamaño:** M

### Fase 5 · Cierre

#### Tarea 8: La prosa, el reparto y los cuatro paquetes

**Descripción:** Actualizar las ocho apariciones de «32 ítems» en la prosa, la
tabla de especificaciones publicada, y regenerar los cuatro paquetes (D2L y
QTI, banco y sonda).

**Criterios de aceptación:**
- [ ] Ninguna cifra de la prosa contradice el reparto real
- [ ] Los cuatro ZIP se regeneran y las cuatro auditorías salen limpias
- [ ] Una reconstrucción desde cero da el mismo `questiondb.xml` y el mismo `questestinterop.xml`

**Verificación:** todo el encadenado, más `git status` limpio salvo lo ignorado.

**Dependencias:** Tarea 7 · **Tamaño:** S

### ✅ Punto de control · Listo
- [ ] 46 ítems · FPP3 §2 cubierto de 2.1 a 2.9 · cero Multi-Select
- [ ] Revisado con el humano antes de publicar

---

## 5 · Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Renumerar módulos rompe anclas externas | Bajo | Comprobado: nadie enlaza a un `#modulo-N` del preparcial y la navegación se genera sola |
| El mapa imagen↔ítem se descuadra al haber más gráficos | **Alto** — la pregunta importa bien con la figura de otra | Tarea 1: capturar por `[data-quiz]` y parar si el número de lienzos no cuadra con el de ítems |
| Los ítems nuevos duplican los de los capítulos | Medio | `verifica_preparcial.R` §7 ya lo comprueba contra los 56 vistos; por eso el de ciclo no se escribe |
| El par bivariado no sostiene la afirmación (r alto y relación en U) | Medio | Comprobación explícita en R antes de escribir el ítem (Tarea 5) |
| Añadir ítems descuadra la tabla de especificaciones publicada | Medio | §6 de `verifica_preparcial.R` lo caza; se actualiza en la Tarea 8 |
| La cosecha mete Multi-Select sin querer | Medio | Filtro explícito y el informe declara cuántos hay; hoy son 0 |
| El preparcial está publicado y en uso | Bajo | El parcial es hoy; el bloque E se publica después |

---

## 6 · Preguntas abiertas

1. **¿Qué par de series para §2.6?** La propuesta es demanda eléctrica contra
   temperatura, que es el ejemplo de FPP3 y hace evidente la U. Alternativa con
   sabor local: consumo contra temperatura en una ciudad de altura, donde la U
   es asimétrica.
2. **¿El simulacro crece?** Hoy tiene seis ítems, uno por objetivo. Si el
   bloque E añade una dimensión de lectura de gráficos, quizá quiera un séptimo.
3. ~~**¿Los ítems de `tsibble` encajan con lo que enseñas?**~~ **RESUELTA
   (2026-09-01): `tsibble`.** E01 evalúa la regla del formato —índice y clave
   identifican una fila y solo una— sobre el error que R lanza cuando falta la
   clave. Queda de pareja con B01, que evalúa `ts()`: el módulo 1.2 enseña las
   dos herramientas y ahora el instrumento pregunta por las dos.
