# Cap. 1 · Diagnóstico de ejercicios y autoevaluación

Archivo: `Htmls_Series/capitulo-1-componentes-descomposicion.html` (worktree
`course-content-improvement-227f2c`, 2026-11-10). Diagnóstico, sin ediciones en el repo.

Leído entero: objetivos de los nueve módulos, los tres `ejercicio-guiado` (3881, 3949,
4003), `AUTOEVALUACIONES['cap1']` (5993–6178) y el motor del quiz (5374–5700), los once
`data-simulador` con su `simulador-intro` y su JS (4599–5360), los bloques `code-tabs`.
Contraste: FPP3 §2.10 y §3.7 (`bibliografia/_local/web/hyndman2021forecasting/graphics.txt`
líneas 651–750, `decomposition.txt` 496–575), §4.3 (`features.txt` 97–99), la nota del Vault
`20948-01 Componentes y descomposición.md` (§Pendiente) y `Estandar/Criterio de contenido.md`.

Escala de veredictos: **sirve** (publicable con retoques cosméticos) · **se puede mejorar**
(núcleo sano, arreglos puntuales) · **hay que rehacer** (no mide lo que dice medir, se responde
sin entender, o enseña algo incorrecto).

---

## 0. Resultado de las ejecuciones

### 0.1 Verificador de bloques (literal)

`python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-1-componentes-descomposicion.html`

```
Bloques encontrados: 8 de R, 5 de Python

--- bloque #0 (r, capitulo-1-componentes-descomposicion.html) ---
    empieza por: # Objeto ts clasico (R base)
    NO aparecen en la salida: ['144', '112', '118', '142']
    salida real:
      [1] 12
      [1] 1949    1
      Error in library(fpp3) : there is no package called 'fpp3'
      Execution halted

!! la sesión de r terminó con código 1
!! la sesión de python terminó con código -15

=== 6 de 10 cifras anunciadas aparecen en la salida real (1 bloques con discrepancias) ===
```

**Falla por el entorno, en las dos sesiones; no se arregló nada:**

- **R**: el metapaquete `fpp3` no está instalado (sí lo están `tsibble` 1.2.0, `feasts` 0.5.0,
  `fable` 0.5.0, `fabletools` 0.8.0, `slider` 0.3.3). Como el verificador encadena los bloques en
  una sesión, se detiene en el bloque 0 y **ningún otro bloque R corre** (ni las soluciones).
- **Python**: la sesión se quedó colgada en el primer `plt.show()`: el backend de matplotlib es
  `macosx` y abrió una ventana (el proceso figuraba como app en primer plano en `lsappinfo`).
  Tras ~5.5 min sin avance **terminé ese proceso hijo** (SIGTERM, de ahí el −15) para que el
  verificador pudiera imprimir su informe; si no, habría muerto por `timeout=1800` sin informe.
  Aparte: `sm.datasets.get_rdataset("AirPassengers")` (bloque Python del M2) necesita red; en
  este sandbox, probado aparte, da `URLError [Errno 8]`.
- **Alcance real de la herramienta en este capítulo**: solo el bloque R del M2 lleva líneas `#>`
  (10 números; los 6 «encontrados» son coincidencias con `[1] 12` y `[1] 1949 1`). Las cifras de
  las tres soluciones van en comentarios `# …`, no `#>`, así que **aunque el entorno funcionara
  el verificador no las contrastaría**. El bloque de `key` del M2 (2488) usa `class="lang-r"` y
  un objeto `ventas` que no existe: no se ejecuta ni se puede ejecutar.

Comprobación adicional (copia en el scratchpad, sin tocar el repo): sustituyendo
`library(fpp3)` por sus componentes, **los 8 bloques R corren sin error**. Avisos: `gg_season()`,
`gg_subseries()`, `gg_lag()` (feasts 0.4.2) y `autoplot.tbl_ts()`/`autoplot.dcmp_ts()`
(fabletools 0.6.0) están **deprecados** y remiten al paquete `ggtime`: son justo las funciones que
el M3 enseña.

### 0.2 Soluciones de los ejercicios (Rscript 4.6.0, código literal)

Script: `scratchpad/diag/ejercicios_cap1.R`; salida: `scratchpad/diag/ejercicios_cap1.out`.

| Ej. | Cifra escrita | Salida real | ¿Coincide? |
|---|---|---|---|
| 1 | co2: b = 1.083, IC95 [0.575, 1.591], R² = 0.335 | 1.0830870, [0.5752301, 1.5909440], 0.3354005 | sí |
| 1 | AirPassengers: b = 1.291, IC95 [1.149, 1.432], R² = 0.976 | 1.2907695, [1.1494815, 1.4320574], 0.9764348 | sí |
| 1 | rango relativo 0.159 / 1.848 | 0.1592032 / 1.848029 | sí |
| 1 | amplitud del CO₂ +0.024 ppm/año, p = 0.0002 | 0.02394, p = 0.00021 | sí |
| 2 | co2 0.9997 / 0.9841 · USAccDeaths 0.7991 / 0.9426 · log AP 0.9940 / 0.9368 | idénticas | sí |
| 3 | julio: clásica 1.2266→1.2758; STL robusto 1.2562→1.2458; STL sin robust 1.2416→1.2806 | 1.226556→1.275811; 1.256166→1.245817; 1.241599→1.280584 | sí |
| 3 | distorsión +4.02 % / −0.82 % / +3.14 % | 4.02 / −0.82 / 3.14 | sí |

**Las tres soluciones son reproducibles y todas sus cifras coinciden.** Los problemas están en el
enunciado y en la interpretación (fichas §3), no en los números.

### 0.3 Otras comprobaciones medidas

| Qué | Resultado |
|---|---|
| Q3/Q4: valores de tendencia no NA en `decompose(AirPassengers)` | 132 (12 NA) — correcto |
| Q6: varianzas reales de `stl(log(AP), "periodic")` | Var(R) = 0.001074, Var(T+R) = 0.1793 (el ítem usa 0.0012 y 0.20) |
| F_T/F_S de log AP con `feasts::feat_stl` (la herramienta de fpp3) | 0.997 / 0.964 (el capítulo y Q7: 0.994 / 0.937, con `s.window = "periodic"` no declarado en el M8) |
| F_T/F_S de AirPassengers **sin** log | 0.968 / 0.783 |
| Bloque R del M5 (`slide_dbl(.before = 6, .after = 6, mean)`) | media de 13 pesos iguales, no 2×12: julio 1955 = 284 (2×12 = 285.75); desvío máx. 9.897 |
| Bloque Python del M5 (`rolling(window=12, center=True)`) | 133 valores no NA (Q3 dice 132); julio 1955 = 284.0; desvío máx. 3.083 |
| M6 «Con qué» (`stats::filter(y, rep(1/m, m))`) | julio 1955 = 287.5 (no es la 2×m que pide el mismo panel) |
| `statsmodels.seasonal_decompose` | tendencia julio 1955 = 285.75, índice 1.2266 — sí coincide con el R |
| Q2 «equivalentemente aditiva sobre el log» (clásica) | julio: multiplicativa 1.2266 vs exp(aditiva sobre log) 1.2347 — aproximada, no equivalente |
| E3: efecto de `robust = TRUE` sobre la serie **limpia** | mueve el índice de julio +1.17 % (1.2416 → 1.2562) |
| E3 con el atípico **al final** (jul-1960, obs. 139) | clásica +0.21 %, STL robusto −0.97 %: el atípico cae en la zona sin tendencia de la media móvil |
| Variación del nivel anual de co2 1959→1997 (lo que pide la pista del E1) | 15.2 % (la solución dice «16 %», que es (máx − mín)/media = 15.9 %) |

---

## 1. Cobertura: objetivo de módulo × dónde se practica

| Mód. | Objetivo declarado (resumen) | Ejercicio | Quiz | Simulador | Código | Práctica real |
|---|---|---|---|---|---|---|
| M1 | Reconocer una serie; dependencia temporal vs corte transversal; ubicarla en ciencia de datos | — | — | `serie-airpassengers` (gráfico estático, sin tarea) | — | **NADA** |
| M2 | Representar la serie como `ts`, `tsibble` y `pandas` | — (las soluciones usan objetos `ts` ya hechos) | — | — | 1 bloque R/Py (ejemplo resuelto); ejemplo de `key` no ejecutable | **NADA** |
| M3 | Usar gráfico de tiempo, estacional, de subseries y de rezagos | E1 pide «justifica con el gráfico estacional» (la solución no lo usa) | — | `grafico-estacional` (estático) + mapa mes×año | una línea por gráfico | Estacional: nominal. **Subseries y rezagos: NADA** |
| M4 | Separar T, S, C, R; aditivo vs multiplicativo | E1 | Q1, Q2 (etiquetada M6) | `comparador-escala` (2 deslizadores), `amplitud-nivel`, `serie-vs-log`, `construye-tu-serie` (3 deslizadores) | — | La mejor cubierta. Reconocer un **ciclo** en datos reales y el ruido como residuo: nada |
| M5 | Estimar la tendencia con media móvil; compromiso suavidad/detalle | — | Q3 (y Q4) | `media-movil` (deslizador m) | bloque R/Py (no calculan la 2×12) | Parcial: el estudiante nunca calcula una media móvil ni justifica un m; Q3/Q4 solo preguntan por los NA |
| M6 | Descomposición clásica y sus limitaciones | E3 (índice clásico con atípico); E1 la pide y no la hace | Q4, Q2 | `descomp-clasica` (estático) | bloque | Limitaciones: sí. Ejecutarla y **leer el residuo para decidir a qué paso volver (paso 4, «el bucle»): NADA** |
| M7 | Aplicar STL; explicar por qué es más flexible y robusta | E3, E2 (usa `stl`) | Q5 | `loess-local` (4 controles, con tarea explícita), `descomp-stl` (estático) | bloque | «Explicar»: sí. «Aplicar» con una decisión (`s.window`, `t.window`): nada; leer componentes en log y volver con exp: nada |
| M8 | Construir la desestacionalizada; cuantificar F_T y F_S | E2 | Q6, Q7, Q8 | `desestacionalizada` (estático) | **ninguno** | F_T/F_S: sí. **Construir la desestacionalizada: NADA** (no hay ni una línea de código para hacerlo en todo el capítulo) |
| M9 | Conectar con el flujo de ciencia de datos; fijar conceptos | E3 («IA como tutor») | el quiz entero | — | — | Fijar conceptos: sí. Conexión (F como *features* sobre muchas series, descomposición como preprocesamiento): nada |

Reparto del quiz por etiqueta `modulo`: M4 1 · M5 1 · M6 2 · M7 1 · M8 3 · **M1, M2, M3: 0**.
La etiqueta alimenta el «qué repasar» del resumen; Q2 está etiquetada 6 pero su contenido es del
M3–M4, así que quien la falla es enviado al módulo equivocado.

**Objetivos sin ninguna práctica dentro del capítulo:** M1 y M2 completos; y como sub-objetivos
declarados: subseries y rezagos (M3), construir la serie desestacionalizada (M8), y el análisis
del residuo como criterio de vuelta atrás (M6), que el propio capítulo presenta como el núcleo
del método (3008, 3339–3340).

Lo que se evalúa fuera (Vault, §Pendiente): el Taller 1 cobra el índice estacional del M6 (T2) y
los gráficos estacional y de rezagos del M3 (T4) sobre otra serie; los módulos 1, 5, 7 y 9 no
entran al escrito y solo los cubre el banco de la defensa; el gráfico de subseries no aparece en
el taller ni en su banco y se llevó al Parcial 1 / preparcial. Es decir, los huecos del capítulo
coinciden con lo que tampoco se practicó en la evaluación del corte.

---

## 2. Fichas del quiz (`AUTOEVALUACIONES['cap1']`)

Comportamiento del motor que condiciona las fichas (5382–5384, 5450–5470): la `pista` aparece
**tras el primer fallo** y se deja reintentar; el resultado suma aciertos al primer y al segundo
intento. Una pista que regala la respuesta convierte el segundo intento en gratuito.

Hallazgos transversales:

- **El aviso dice «Seis preguntas» (3864) y hay ocho.**
- **En los cinco ítems de una sola respuesta la correcta es la opción más larga** (caracteres de
  texto visible): Q1 107 vs ≤ 67 · Q2 62 vs ≤ 49 · Q4 103 vs ≤ 75 · Q7 103 vs ≤ 65 · Q8 93 vs
  ≤ 75. La posición está repartida (2 4 1 3 2, vigilada por `audita_posicion_correcta.py`), pero
  la longitud no la vigila nadie: elegir siempre la más larga da 5/5.
- Tres de ocho ítems cobran la misma idea (los 12 NA de la media móvil): Q3, Q4 y la opción 3 de
  Q5, más los dos `retroAcierto`.
- Nivel: nada pasa de **comprender** salvo Q6, que es **aplicar** en su forma mínima (una resta).

| # | Línea | Tipo · etiqueta | Nivel | Veredicto |
|---|---|---|---|---|
| Q1 | 5994 | opción · M4 | recordar | se puede mejorar |
| Q2 | 6022 | opción · M6 (real: M3–M4) | recordar (la premisa está en el enunciado) | **hay que rehacer** |
| Q3 | 6050 | numérica · M5 | recordar (la cifra está escrita en el M5) | **hay que rehacer** |
| Q4 | 6060 | gráfico · M6 | comprender | se puede mejorar |
| Q5 | 6097 | múltiple · M7 | comprender | se puede mejorar |
| Q6 | 6112 | numérica · M8 | aplicar (mínimo) | **hay que rehacer** |
| Q7 | 6122 | opción · M8 | comprender | se puede mejorar |
| Q8 | 6150 | opción · M8 | comprender | sirve |

**Q1 · ciclo vs estacionalidad (5994–6021).** Una sola respuesta defendible. El distractor 1
(«el ciclo dura más de un año») es un error real y su retro lo trata con matiz correcto (las
duraciones típicas sí son esas, pero no lo definen; coincide con lo que dice FPP3 §2.3,
`graphics.txt` 358). El 3 es plausible; el 4 («son sinónimos») es relleno. La correcta repite casi
literal el aviso del M4 («período fijo y conocido», 2652) y es la más larga por 40 caracteres; la
pista («si puedes decir de antemano cuánto va a durar») da el criterio. Se responde sin haber
entendido. *Mejora*: igualar longitudes, cambiar el 4 por un error real (p. ej. «si una
oscilación dura 12 meses en datos mensuales es ciclo»), o plantearlo sobre una serie que el
estudiante tenga que clasificar.

**Q2 · qué descomposición conviene (6022–6049).** El enunciado afirma «la amplitud **crece** con
el nivel», que es la regla del M4 enunciada al revés: la pregunta se responde recordando una
frase, no leyendo datos. La correcta es la más larga y la única con dos partes. **La retro del
distractor 1 (6031) dice que el residuo aditivo tendría «un patrón en forma de embudo»; el M6 mide
otra cosa: la desviación típica anual del residuo aditivo dibuja una U (30.5 … 5.6 … 25.4,
3331–3333), justo porque el índice fijo acierta a mitad de muestra.** La retro contradice el
capítulo. Además: «equivalentemente aditiva sobre el log» es aproximado (julio 1.2266 frente a
1.2347, medido); la retro del distractor 3 apela a Box–Cox, que el capítulo no enseña; y la
etiqueta `modulo: 6` desvía el «qué repasar». *Rehacer*: mostrar la serie o la tabla amplitud/nivel
de otra serie y pedir la decisión; corregir «embudo» → U.

**Q3 · cuántos valores deja la 2×12 (6050–6059).** Respuesta 132, verificada. Pero el M5 lo
escribe literalmente («De las 144 observaciones de AirPassengers quedan 132», 2877–2878) y la pista
lo calcula casi entero. La `retroFallo` es buena (diagnostica 138 y 144). Redundante con Q4.
Además, **el bloque Python del propio M5 da 133**, no 132 (§0.3): quien compruebe con el código
del capítulo encuentra otra cifra. *Rehacer*: transferir (p. ej. 2×4 sobre datos trimestrales, o
qué m elimina una estacionalidad de período 7) o fusionar con Q4.

**Q4 · por qué la tendencia no llega a los extremos (6060–6096).** Correcta y bien retroalimentada
(la del distractor 4 da la comprobación `sum(is.na(...))` = 12, verificada; la del 3 transfiere a
2×4 trimestral). Pero el gráfico es decorativo (el enunciado ya dice que la línea no llega), la
correcta es la más larga (103 vs ≤ 75) y es la única con un mecanismo; el distractor 4 («el
gráfico está recortado») es relleno. Mide lo mismo que Q3. *Mejora*: usar el gráfico para algo que
solo él muestre (p. ej. cuántos meses faltan, o por qué la STL sí llega).

**Q5 · ventajas reales de STL (6097–6111).** Buenos distractores: «evita transformar» es un error
real que el capítulo combate, y «no necesita el período» también. 3 correctas de 5. Defectos: la
pista (6101) dice «Son tres» y enumera los tres temas en el orden de las opciones correctas, de modo
que el segundo intento es gratuito; **las opciones no llevan `retro` propio**, contra la regla del
motor (5386–5388): el desglose muestra «La marcaste y no va: <texto>» sin explicación, y solo la
`retroFallo` general dice por qué. *Mejora*: retro por opción, pista que no cuente ni enumere.

**Q6 · calcular F_T (6112–6121).** Dos números y una resta; la pista (6116) da el resultado de la
división (0.006), así que el segundo intento solo exige 1 − 0.006. Los insumos no son los de
AirPassengers (los reales son 0.001074 y 0.1793; medido), aunque la `retroAcierto` dice «Es justo el
valor de AirPassengers»: es un par elegido a mano para que salga 0.994. El enunciado omite el
max(0, ·), inocuo aquí. No mide comprensión de F_T. *Rehacer*: dar una descomposición (o sus
varianzas reales) y pedir decidir qué serie tiene la tendencia más fuerte, o qué pasa con F_S si se
cambia la escala (0.937 en log frente a 0.783 sin log, medido).

**Q7 · cómo se leen F_T = 0.994 y F_S = 0.937 (6122–6149).** El distractor 1 («explica el 99.4 % de
la varianza total») es un error real y bien explicado. El 2 es plausible. El 4 («descartar el
componente estacional») es absurdo. La correcta es la más larga (103 vs ≤ 65) y la pista («si tiene
sentido comparar una con la otra cuando sus denominadores son distintos») elimina 2 y 4. Las cifras
dependen de `s.window = "periodic"`, que el M8 no declara: con `feat_stl`, la herramienta de fpp3,
salen 0.997 y 0.964 (medido). No afecta a la respuesta, pero «obtuvimos» no es reproducible con la
herramienta del curso sin ese dato. *Mejora*: longitudes, sustituir el 4, declarar el ajuste en
el M8.

**Q8 · para qué sirve la desestacionalizada (6150–6177).** Buen contenido: el distractor 1
(pronosticar sin modelar la estacionalidad) y el 3 (confundirla con quitar la tendencia) son
confusiones reales, y sus retros explican por qué. El 4 es débil. La correcta es la más larga
(93 vs ≤ 75) y la pista apunta a ella. *Sirve*, con el retoque de longitudes.

---

## 3. Fichas de los ejercicios guiados (M9)

| # | Línea | Nivel (enunciado / solución) | ¿Dice qué entregar? | Pista | Reproducible | Veredicto |
|---|---|---|---|---|---|---|
| E1 | 3881 | evaluar / aplicar + leer un IC | parcial | útil, pero contradice el enunciado | sí | **hay que rehacer** |
| E2 | 3949 | aplicar / aplicar + comparar | no | elige las series por el estudiante | sí | se puede mejorar |
| E3 | 4003 | analizar / analizar | no | regala la clave | sí | se puede mejorar |

**E1 · co2: aditiva o multiplicativa (3881–3947).**
- *Enunciado*: «Con fpp3, grafica y descompone (clásica y STL) la serie co2 o una serie de demanda
  de energía. ¿Aditiva o multiplicativa? Justifica con el gráfico estacional.» Dice qué decidir,
  no qué entregar (¿qué gráficos?, ¿qué componentes?, ¿qué argumento?).
- *La solución no resuelve lo que se pide*: no grafica, no hace la descomposición clásica ni la STL,
  no usa el gráfico estacional ni fpp3 (es R base). Sustituye todo por una regresión
  log-amplitud ~ log-nivel. La opción «serie de demanda de energía» no tiene solución, y la
  candidata natural (`vic_elec`, semihoraria) tiene varias estacionalidades, que el M3 menciona
  (2541–2550) pero que ni la clásica ni la STL de un período resuelven.
- *Mensajes contradictorios*: el enunciado dice «justifica con el gráfico estacional»; la pista,
  «"A ojo" no basta» (3894); el M6, «La decisión es visual, no hay prueba automática» (3016).
- *Interpretación con un error de lectura*: con el criterio de la propia solución (b ≈ 0 ⇒
  aditiva, b ≈ 1 ⇒ multiplicativa), **el IC de co2 [0.575, 1.591] excluye el 0** —rechaza la
  aditiva— e incluye el 1; la tabla lo rotula «Indistinguible» (3929–3930) y el texto dice «los
  datos no distinguen una descomposición de la otra» (3937–3938). Lo que es cierto, y es el
  argumento bueno, es práctico: el nivel varía tan poco que las dos dan casi lo mismo (índice
  aditivo de julio 3.0 ppm frente a 2.81–3.23 ppm del multiplicativo al nivel mínimo y máximo de
  la tendencia, medido). Simétricamente, **el IC de AirPassengers [1.149, 1.432] excluye el 1** y
  la solución dice «multiplicativa sin discusión» (3935–3937), mirando solo que excluye el 0 —
  justo el matiz que el M4 sí había hecho («tampoco es un multiplicativo de manual», 2764–2765).
  Y «No es proporcional al nivel; es un fenómeno propio» (3942–3943) no lo puede demostrar este
  análisis: en co2 nivel y tiempo crecen juntos.
- *Pista*: la pregunta que plantea (variación del nivel 1959→1997) es buena; la respuesta escrita
  («16 %») es (máx − mín)/media, 15.9 %; la variación de la media anual es 15.2 %.
- *Veredicto*: **hay que rehacer**: la solución modelo enseña una lectura de IC incorrecta y no
  responde al enunciado. Lo aprovechable: la pregunta de la pista y la cifra del rango relativo.

**E2 · F_T y F_S de dos series (3949–4001).**
- *Enunciado*: «Calcula F_T y F_S para dos series distintas y compáralas.» No dice cuáles, en qué
  escala, con qué ajuste de STL ni qué es «comparar». La pista elige las series (co2 y
  USAccDeaths), con lo que lo único que queda es teclear.
- *Solución*: reproducible, cifras exactas. La interpretación sí va más allá de leer: dos
  advertencias buenas (no leer F_T como varianza explicada; comparar entre series). Pero la pista
  llama a USAccDeaths «casi pura estacionalidad» y la solución le da F_T = 0.80, lo bastante alto
  para que la etiqueta no se sostenga; da tres series cuando se piden dos; y no dice que las cifras
  dependen de la escala (AP: 0.994/0.937 en log, 0.968/0.783 sin log) ni de `s.window`
  (`feat_stl`: 0.997/0.964). Esa dependencia es lo más instructivo que podía sacar el ejercicio.
  `genera_soluciones.R` cita «FPP3 3.6» para F_T/F_S; el capítulo, §4.3 (que es donde está en
  `features.txt` 97–99).
- *Veredicto*: **se puede mejorar** (enunciado con entregable; incluir una serie con F_T bajo, p. ej.
  `nottem`, F_T = 0.205; pedir el efecto de la escala).

**E3 · atípico: clásica vs STL, «con IA como tutor» (4003–4065).**
- *Enunciado*: pide un contraejemplo a una IA y verificarlo en R. No dice qué entregar (¿el
  prompt?, ¿la respuesta de la IA?, ¿la tabla?, ¿un juicio sobre lo que dijo la IA?): la parte de
  IA no deja rastro evaluable.
- *Ya está resuelto antes*: el M7 hace exactamente el mismo experimento (julio de 1955 inflado un
  50 %, tabla de pesos con peso 0, 3568–3591) y anuncia el resultado («El ejercicio 3 del cierre
  mide exactamente cuánto cambia esa segunda opción», 3684–3685; también 3590–3591). La pista
  (4017–4020) da la clave (`robust`). No queda nada por descubrir.
- *Solución*: reproducible, cifras exactas; la lección sobre el argumento por defecto es valiosa.
  No menciona que `robust = TRUE` cambia el índice de julio también en la serie **limpia** (+1.17 %,
  1.2416 → 1.2562), así que las dos STL se miden contra líneas base distintas; ni que mide solo
  julio (el generador calcula la distorsión máxima de los doce meses y no se muestra). La
  pregunta de FPP3 3.7 ej. 7f (¿y si el atípico está al final?) daría un resultado
  contraintuitivo y medido: la clásica apenas se mueve (+0.21 %) porque el atípico cae en la zona
  sin tendencia.
- *Errata*: «reponderea» (4054).
- *Veredicto*: **se puede mejorar** (otra serie u otra posición del atípico, entregable explícito
  para la parte de IA, pista que no dé el argumento).

---

## 4. Simuladores como práctica

| id | Línea | Mód. | Controles | Tarea que plantea | Nivel |
|---|---|---|---|---|---|
| `serie-airpassengers` | 2356 | M1 | ninguno | ninguna; el intro dice qué se ve | — |
| `grafico-estacional` | 2562 | M3 | ninguno | ninguna; el intro da la lectura | — |
| `comparador-escala` | 2682 | M4 | β (0–4), A (4–40) | implícita: subir β y ver qué panel cambia; respuesta en 2710–2715 | comprender |
| `amplitud-nivel` | 2746 | M4 | solo tooltip | implícita: ¿qué referencia siguen los puntos?; respuesta en 2760–2766 | comprender |
| `serie-vs-log` | 2776 | M4 | ninguno | ninguna; lectura con cifras | — |
| `construye-tu-serie` | 2806 | M4 | β, A, σ | «aislar el efecto de cada componente», abierta y sin pregunta; solo aditiva | comprender |
| `media-movil` | 2899 | M5 | m (2–24) | implícita: encontrar el m que borra la estacionalidad; el intro lo dice (m = 12) | comprender |
| `descomp-clasica` | 3188 | M6 | ninguno | ninguna | — |
| `loess-local` | 3438 | M7 | foco, span, grado, pesos | **explícita**: llevar el foco a los bordes; bajar grado y pesos a 0; respuestas en 3455–3462 | comprender/analizar |
| `descomp-stl` | 3597 | M7 | ninguno | «nota que la tendencia llega…» | — |
| `desestacionalizada` | 3735 | M8 | ninguno | ninguna | — |

Siete de once son gráficos estáticos; cuatro tienen controles; uno (`loess-local`) plantea una tarea
concreta. Ninguno pide una **predicción antes de mover** ni comprueba nada; en todos la respuesta
está escrita en el intro o en el párrafo siguiente. Como práctica intermedia valen para
«comprender», no para comprobar que se comprendió.

## 5. Bloques de código como práctica

Son ejemplos resueltos; ninguno va acompañado de un «ahora tú». Defectos que afectan a la práctica:

- **M5 (2920–2936)**: el R (`slide_dbl(.before = 6, .after = 6, mean)`) es una media de 13 pesos
  iguales y el Python (`rolling(12, center=True)`) una de 12 descentrada; los dos se rotulan como la
  2×12 del módulo. Cifras en §0.3.
- **M6 «Con qué» (3030)**: `stats::filter(y, rep(1/m, m))` tampoco es la 2×m que pide ese mismo panel.
- **M6 (3280)**: el comentario dice «aditiva sobre log = multiplicativa» y el código usa
  `type = "multiplicative"`.
- **M8**: no hay bloque. Ni la desestacionalizada ni F_T/F_S se calculan en el módulo; F_T/F_S solo
  aparecen en la solución del E2.
- **M2 (2488)**: el ejemplo de `key` no es ejecutable (`ventas` no existe) y no hay práctica de clave.
- Funciones gráficas del M3 deprecadas en las versiones instaladas (§0.1); el Python del M2 necesita
  red.

## 6. Progresión

- **Toda la práctica escrita está al final.** Entre el M1 y el M8 (ocho módulos, el M7 muy largo según
  el Vault) no hay ni una pregunta de control; solo simuladores sin pregunta. El quiz y los tres
  ejercicios están en el M9.
- **Orden de los ejercicios**: E1 (el más abierto, escala, M3–M4–M6–M7) → E2 (el más mecánico, M8) →
  E3 (M6–M7). No van de lo simple a lo integrado, ni siguen el orden de los módulos.
- **Integración**: E1 integra varios módulos en el enunciado, pero su solución se queda en uno (una
  regresión). Ninguno recorre el flujo completo que el capítulo enseña —mirar, elegir escala,
  descomponer, leer el residuo, volver, desestacionalizar, medir fuerzas— sobre una serie nueva.
- **Quiz**: ordenado por módulos (4, 6, 5, 6, 7, 8, 8, 8), sin ítems de integración.

## 7. Frente al texto guía (FPP3 §2.10 y §3.7)

| FPP3 | Tipo de tarea | ¿Equivalente en el cap. 1? |
|---|---|---|
| 2.10 ej. 1 | Averiguar el intervalo/frecuencia de varias series y graficarlas | No (M2 sin práctica) |
| 2.10 ej. 2 | Filtrar un tsibble para localizar un máximo | No |
| 2.10 ej. 3 | Leer un CSV, convertirlo en tsibble (`yearquarter`, `index =`) y graficar varias series | No: nunca se construye un objeto desde datos crudos |
| 2.10 ej. 4–5 | Tsibble con **clave**, filtrar y agregar | No (la clave se explica en el M2 y no se practica) |
| 2.10 ej. 6 | Comparar cuatro series con `autoplot`, `gg_season`, `gg_subseries`; observaciones inusuales | No (subseries nunca; comparación entre series nunca) |
| 2.10 ej. 7 | Serie **personal** elegida por semilla y explorada con todos los gráficos | No: todos trabajan la misma serie |
| 2.10 ej. 8 | Detectar tendencia, **ciclo** y estacionalidad en cinco series; años inusuales | No (el ciclo solo se define; Q1 es de definición) |
| 2.10 ej. 9 | Emparejar gráficos de tiempo con ACF | No (la ACF es del cap. 2; pero tampoco hay emparejamiento serie ↔ gráfico estacional/rezagos) |
| 2.10 ej. 10–11 | ACF y ruido blanco | Fuera de alcance (cap. 2) |
| 3.7 ej. 1 | Ajuste per cápita | No (los ajustes de población/inflación/calendario no se enseñan) |
| 3.7 ej. 2–5 | Box–Cox | Fuera de alcance (cap. 2), aunque Q2 la nombra en su retro |
| 3.7 ej. 6 | **Demostrar** que una 3×5 equivale a una media ponderada de 7 términos | No: los pesos de la 2×12 se dan y no se derivan |
| 3.7 ej. 7a–c | Descomposición clásica multiplicativa y contrastarla con lo visto en el gráfico | No (E1 la pide, la solución no la hace) |
| 3.7 ej. 7d | Calcular y graficar la **desestacionalizada** | No |
| 3.7 ej. 7e | Atípico y su efecto | Sí, parcial (E3, sobre el índice, no sobre la desestacionalizada) |
| 3.7 ej. 7f | Atípico **al final** frente al centro | No |
| 3.7 ej. 8 | X-11 | No (X-11/SEATS no se enseñan) |
| 3.7 ej. 9 | **Redactar** la interpretación de una descomposición dada, atendiendo a las escalas | No (el capítulo lo modela con julio de 1955, pero nunca lo pide) |
| 3.7 ej. 10 | STL **eligiendo la ventana estacional** para una estacionalidad cambiante; ver cómo cambia | No (todo el capítulo usa `"periodic"`) |

Tipos de tarea ausentes por completo: construir y manipular el objeto (2.10 ej. 1, 3–5), comparar
varias series (2.10 ej. 6, 8), serie personal (2.10 ej. 7), demostración (3.7 ej. 6), redacción
interpretativa sobre una figura dada (3.7 ej. 9) y elección de un parámetro con consecuencias
(3.7 ej. 10).

## 8. Datos

- Todos los módulos, los nueve simuladores con datos reales y las ocho preguntas usan
  **AirPassengers**; dos simuladores son sintéticos. Los ejercicios añaden `co2` y `USAccDeaths`, y
  el E3 vuelve a AirPassengers (el mismo julio de 1955 que el M6 y el M7).
- Consecuencia: el quiz se puede responder con las cifras del texto (132, 0.994, 0.937, la U) en vez
  de razonando, y el estudiante nunca ve un caso en que la respuesta del capítulo no valga (aditiva,
  sin tendencia, sin estacionalidad, estacionalidad que cambia de forma).

Series de `datasets` (R base) medidas aquí, con dónde convendrían:

| Serie | Medido | Dónde |
|---|---|---|
| `nottem` (mensual, temperaturas) | F_T = 0.205, F_S = 0.944; el nivel anual varía un 7 % | M4/M8: estacionalidad estable sin tendencia; contraste de F_T bajo, que ninguna serie actual tiene (la mínima es 0.80) |
| `UKgas` (trimestral) | b = 1.44, IC [1.38, 1.51], R² = 0.99; aun en log, el factor del T1 pasa de 1.36 a 1.85 y el del T3 de 0.70 a 0.46 (STL, `s.window = 7`) | M3 (subseries), M6 (escala sin la respuesta escrita), M7 (elegir `s.window`: el log no cierra el abanico) |
| `lynx` (anual) | frecuencia 1; picos altos separados 9–10 años | M4: ciclo sin estacionalidad, para Q1 sobre datos y no sobre definiciones |
| `mdeaths` + `fdeaths` | `as_tsibble(cbind(...))` da un tsibble con `Key: key [2]` | M2: practicar la clave |
| `JohnsonJohnson` (trimestral) | b = 0.82, IC [0.65, 0.98] | M4/M6: multiplicativa trimestral (la 2×4 que Q4 menciona) |
| `UKDriverDeaths` / `Seatbelts` | la ayuda de R documenta el cinturón obligatorio desde el 31 ene 1983 | M7: robustez y ruptura de nivel reales, no inyectadas |

## 9. Lista de huecos (por prioridad)

1. **M6 — leer el residuo y decidir a qué paso volver.** El capítulo lo llama el núcleo del método y
   nadie lo practica. Tipo FPP3 3.7 ej. 9 (interpretar una descomposición dada); con una
   descomposición mal elegida de una serie distinta de AirPassengers. Nivel analizar/evaluar.
2. **M3 — gráfico de subseries y de rezagos**: cero práctica, igual que en el Taller 1. Tipo FPP3
   2.10 ej. 6/8 (comparar series, años inusuales), con `UKgas` o `nottem`.
3. **M7 — aplicar STL con una decisión**: elegir `s.window` ante una estacionalidad cambiante y ver
   la diferencia (FPP3 3.7 ej. 10), con `UKgas`. Incluye leer los componentes en log y volver con exp
   (la «trampa» del 0.2164 → 1.2416, que se explica y no se practica).
4. **M8 — construir la desestacionalizada** (no hay código en todo el capítulo) y ver el atípico al
   final frente al centro (FPP3 3.7 ej. 7d–f).
5. **M2 (y M1) — construir el objeto**: declarar índice, frecuencia y clave desde datos crudos (FPP3
   2.10 ej. 1, 3–4), con `mdeaths` + `fdeaths`. El M1 tampoco tiene práctica (dependencia temporal).
6. **Práctica intermedia**: una o dos preguntas de control al final de M4–M7, en vez de concentrar
   todo en el M9.
7. **M4 — reconocer un ciclo en datos** (`lynx`), no solo su definición (FPP3 2.10 ej. 8).
8. **M5 — derivar pesos de una media móvil compuesta** (2×4 o 3×3; FPP3 3.7 ej. 6) y elegir m con
   criterio en una serie no estacional.
9. **Serie por estudiante** (FPP3 2.10 ej. 7): el quiz y los ejercicios tienen sus respuestas escritas
   en el texto.
10. **Quiz**: igualar longitudes; pistas que no regalen (Q5, Q6, Q8); retro por opción en Q5; corregir
    «Seis preguntas» y el «embudo»; etiquetar Q2 como M4; quitar una de Q3/Q4.
11. **Código**: que el bloque del M5 (R y Python) y el «Con qué» del M6 calculen la 2×12 que
    nombran; declarar `s.window = "periodic"` en el M8.
12. **Verificación**: las cifras de las soluciones no están al alcance de `verifica_bloques_cap6.py`
    (van en `# …`, no `#>`); el verificador necesita `fpp3` instalado y un backend no interactivo
    para no colgarse en `plt.show()`.
