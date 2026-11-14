# Capítulo 1 · ronda R5 «práctica» · cambios

Fecha: 2026-11-14. Un solo redactor (subagente redactor R5, Fable 5.2). **Sin commits.**
Alcance: decisión **D8** del plan, en dos encargos y una corrección.

> **Este documento tiene tres capas.** §0–§5 cuentan el primer encargo y §8 el segundo, tal como se
> entregaron. **§9 los corrige en 16 puntos, tras la verificación independiente, y es la que manda**
> donde difieran: cambian los enunciados y las soluciones del M6 y del M7, la pregunta 6, tres
> `retro`, cuatro pistas, la entradilla del quiz, un párrafo del M7, un párrafo nuevo en el M2 y los
> minutos declarados. §6 (verificación) está puesta al día con el estado final.

- **Primer encargo (§0–§5):** rehacer el ejercicio 1, mejorar el 2 y el 3, rehacer las preguntas 2,
  3 y 6 del quiz, los defectos transversales del quiz y el bloque de código del Módulo 2.
- **Segundo encargo (§8):** cinco ejercicios cortos, uno al final de los módulos 2, 3, 6, 7 y 8.
- **Corrección (§9):** los 16 puntos del verificador independiente.

Archivos tocados:

- `Htmls_Series/capitulo-1-componentes-descomposicion.html`.
  Primer encargo: bloque R del M2, una frase del M7, la entradilla del quiz, los tres ejercicios del
  M9, `AUTOEVALUACIONES['cap1']`, el motor del quiz (un campo opcional) y una regla CSS.
  Segundo encargo: cinco bloques `.exercise` nuevos y un selector del motor de ejercicios.
  Corrección: lo que detalla §9. **Los números de línea de §0–§5 son los del final del primer
  encargo**; en el archivo final los cinco ejercicios nuevos están en las l. 3075, 3396, 4326, 4840 y
  5185, y el M9 empieza en la l. 5273.
- `Htmls_Series/index.html` y `Htmls_Series/README.md`: «20 ejercicios» → «25 ejercicios» (segundo
  encargo; lo exige `cuenta_sitio.py`).
- `diagnostico/cap1/comprobaciones/r5_ejercicios_quiz.R` y `.out`: el guion de cifras del primer
  encargo. `r5_ejercicios_cortos.R` y `.out`: el del segundo. Cada línea de las salidas lleva una
  etiqueta (`[E1-09]`, `[Q2-03]`, `[M6-03]`…); abajo se cita la etiqueta de la que sale cada cifra.
- `diagnostico/cap1/comprobaciones/r5_longitudes.py` y `.out`: la medida de las opciones.
- `diagnostico/cap1/herramientas/r5_tareas.py` y `comprobaciones/r5_navegador.out`: el quiz hecho
  entero y los ejercicios del M9 abiertos, a 1200 y 375 px (Chrome sin ventana, con el arnés
  `r3bis_elemento.js`). `r5_tareas_cortos.py` y `r5_navegador_cortos.out`: lo mismo para los cinco
  ejercicios nuevos. Capturas en `capturas/r5/` (ignoradas por git, como las demás).
- `diagnostico/cap1/comprobaciones/r5_minutos.py` y `.out`: los minutos de lectura por módulo, con la
  fórmula de la R3 (corrección).
- `diagnostico/cap1/comprobaciones/r5_verifica_todo.out`: la pasada completa, tras la corrección.

No se tocó: los capítulos 2 a 6, la plantilla, `Vault/`, `bibliografia/`, `precalculo/`.

---

## 0 · Lo que ya estaba arreglado (y no se tocó, o solo se comprobó)

El diagnóstico es del 2026-11-10. Comprobado contra el archivo del 14:

| Hallazgo del diagnóstico | Estado al empezar la R5 |
|---|---|
| «Seis preguntas» cuando hay ocho | **Ya arreglado por la R1** («Ocho preguntas»). El número no se toca; sí la segunda mitad de la frase, porque la pregunta 5 gana explicación por opción y solo queda una numérica (ver §4) |
| Q2, retro del distractor 1: «embudo» | **Ya arreglado por la R1** (decía «dibuja una U»). La pregunta se rehízo entera; la U sigue, ahora con cifras |
| E1: lectura invertida del intervalo; «16 %» | **Ya arreglado por la R1**: la solución decía ya «descarta la aditiva», 15 % y 16 % cada uno en su sitio. Quedaba el desajuste enunciado/solución |
| E2: «casi pura estacionalidad» para `USAccDeaths` | **Ya arreglado por la R1** («una tendencia bastante más débil») |
| E3: no decía que `robust = TRUE` mueve la línea base | **A medias**: la R1 añadió un paréntesis con 1.2562 frente a 1.2416, sin el porcentaje ni la consecuencia. Ahora es un apartado propio |
| Q7: cifras con `s.window = "periodic"` sin declarar | El M8 lo declara desde la R3; faltaba en el enunciado de la pregunta, que decía «obtuvimos». Añadido |
| Bloques R/Python del M5 y «Con qué» del M6 que no calculaban la 2×12; Python del M5 con 133 valores | **Ya arreglado por la R1** (control 285.75 y 12 `NA` en los dos lenguajes) |
| M8 sin código para la desestacionalizada ni para las fuerzas | **Ya arreglado por la R3** |
| Funciones gráficas del M3 «deprecadas» | **No aplica ya**: con `fpp3` 1.0.3 y `ggtime` 0.2.0, `gg_season()` corre sin aviso (`[E1-04c]`). Nada que migrar |
| Verificador de bloques que no corría | Corre entero. Daba 13 de 14 por el bloque del M2 (§5) |

---

## 1 · Ejercicio 1 — rehecho

**Camino elegido: llevar el enunciado y la solución al mismo sitio con un enunciado en cuatro
apartados** (mirar, medir, descomponer, veredicto), en vez de recortar el enunciado al criterio
cuantitativo o de reescribir la solución entera.

Por qué: el criterio cuantitativo que ya estaba resuelto es bueno, pero solo, dejaba fuera las
herramientas del capítulo (el gráfico estacional del M3, la descomposición clásica del M6, la serie
desestacionalizada del M8). Y lo que el ejercicio enseña —que el criterio y la consecuencia práctica
son dos preguntas distintas— solo se ve con los tres pasos en fila: a ojo parece aditiva, medida
apunta a la multiplicativa, y descompuesta da casi lo mismo.

| | Antes | Ahora |
|---|---|---|
| Enunciado | «Con `fpp3`, grafica y descompone (clásica y STL) la serie `co2` o una serie de demanda de energía. ¿Aditiva o multiplicativa? Justifica con el gráfico estacional.» | Una sola serie, `co2`, descrita (ppm, 1959–1997). «Entrega cuatro cosas»: (a) gráfico de tiempo y estacional, con una frase; (b) la tabla del M4 para 1959, 1978 y 1997 y la pendiente $b$ con su intervalo, con el significado de $b \approx 0$ y $b \approx 1$ escrito en el enunciado; (c) las dos descomposiciones clásicas, la serie ajustada con cada una, la mayor diferencia entre las dos en ppm y la desviación típica de cada residuo; (d) el veredicto en dos frases |
| Serie | `co2` «o una serie de demanda de energía», sin solución para la segunda | Solo `co2` |
| Pista | «"A ojo" no basta…», contra un enunciado que pedía justificar con el gráfico | El gráfico da la primera impresión y el apartado (b) pide medir: ya no se contradicen. **Conserva la pregunta** de cuánto varía el nivel del CO₂, y añade el contraste con el ×3.76 de `AirPassengers` |
| Solución | Regresión en R base; sin gráficos ni descomposiciones; tabla con `AirPassengers` como segunda serie | Código que hace los cuatro apartados (`autoplot`, `gg_season`, la tabla, `lm`, dos `decompose`, las dos series ajustadas), con la salida real tras `#>`; una tabla «apartado · resultado · apunta a»; un párrafo por apartado; y un «Para ir más lejos» con lo que ya había sobre el crecimiento de la amplitud |
| STL | Pedida en el enunciado, ausente en la solución | Fuera del enunciado; queda como apunte final, rotulado «Para ir más lejos» |

Se conserva: el matiz de que elegir una u otra cambia poco («no porque los datos no distingan, sino
porque la diferencia entre las dos es pequeña»), la pregunta sobre el nivel del CO₂ y el párrafo
sobre el crecimiento de la amplitud. Sale: el detalle sobre `AirPassengers` sin tendencia
($b = 1.18$, $[0.95, 1.41]$), que era de otra serie; `AirPassengers` queda como referencia de escala
en dos frases.

Cifras (todas de `r5_ejercicios_quiz.out`):

| Cifra en el capítulo | Etiqueta |
|---|---|
| Tabla del código: 315.83 / 4.95 / 1.57 · 335.34 / 5.46 / 1.63 · 363.82 / 6.60 / 1.81 | bloque E1 (l. 89–92 de la salida) |
| $b = 1.083$, intervalo 0.575 a 1.591; $R^2 = 0.335$; deja fuera el 0 y contiene el 1 | bloque E1 (l. 93–94) y `[E1-09]` |
| 0.26 ppm entre las dos series ajustadas, en octubre de 1997 | bloque E1 (l. 95) y `[E1-17]` |
| Residuo: 0.265 ppm la aditiva, 0.238 la multiplicativa | bloque E1 (l. 96–97) y `[E1-19]` |
| Máximo en mayo 38 de 39 años; mínimo en septiembre u octubre | `[E1-03]`, `[E1-04]` |
| 39 años, 1959–1997 | `[E1-01]` |
| La amplitud pasa de 4.95 a 6.60 ppm: 1.65 ppm más, un 33.3 % | `[E1-06]` |
| La serie recorre 53.66 ppm | `[E1-04b]` |
| El nivel sube un 15.2 % (315.83 → 363.82) | `[E1-05]` |
| Amplitud/nivel entre 1.52 % y 2.02 % | `[E1-07]` |
| `AirPassengers`: nivel ×3.76; $b = 1.291$, intervalo 1.149 a 1.432 | `[E1-23]`, `[E1-22]` |
| Vaivén aditivo 6.25 ppm, de −3.25 (octubre) a +3.00 (mayo) | `[E1-14]` |
| Vaivenes de 5.86 y 6.75 ppm con los índices multiplicativos | `[E1-16]` |
| 0.26 ppm = 4.2 % del vaivén | `[E1-18]` |
| `AirPassengers`: 51.1 mil sobre 117.4, el 43.5 % | `[E1-24]` |
| Residuo aditivo: 0.29 ppm en 1959–1964 y en 1992–1997, 0.19 en 1975–1981 | `[E1-20]` |
| +0.024 ppm/año, $p = 0.0002$ | `[E1-10]` |
| +0.023 ppm/año si fuera proporcional | `[E1-11]` |
| $p = 0.85$ para la tendencia de amplitud/nivel | `[E1-12]` |
| STL con `s.window = 11`: 5.85 → 6.72 ppm | `[E1-25]` |
| Qué es `co2` (Mauna Loa, ppm) | `[ENT-04 ?co2]`, la ayuda de R |

---

## 2 · Ejercicio 2 — mejorado

| | Antes | Ahora |
|---|---|---|
| Enunciado | «Calcula $F_T$ y $F_S$ para dos series distintas y compáralas.» | Cuatro casos nombrados y descritos (`nottem`, `USAccDeaths`, `AirPassengers` en logaritmos y sin transformar), el ajuste (`s.window = "periodic"`, fórmula del M8) y tres entregables: (a) tabla de ocho cifras a tres decimales; (b) una frase que ordene los casos por $F_T$ y diga qué se ve en cada serie; (c) una frase sobre lo que le pasa a $F_S$ al quitar el logaritmo, y por qué |
| Pista | Elegía las series (`co2` y `USAccDeaths`) | Pide una apuesta antes de calcular, recuerda el $\max(0,\cdot)$ y orienta el apartado (c) hacia lo que supone `"periodic"`, sin decir la respuesta |
| Solución | Tres series cuando se pedían dos; sin `nottem`; nada sobre la escala | Los cuatro casos, con la salida real tras `#>`; el orden por $F_T$ explicado con las medias anuales; el efecto de la escala con su mecanismo y su cifra; y la lección: «$F_T$ y $F_S$ describen la descomposición, no solo la serie». Las dos advertencias que había se conservan |

`co2` sale de este ejercicio (es la serie del 1 y reaparece en la pregunta 6).

| Cifra en el capítulo | Etiqueta |
|---|---|
| `nottem` 0.205 / 0.944 · `USAccDeaths` 0.799 / 0.943 · log(`AirPassengers`) 0.994 / 0.937 · `AirPassengers` 0.968 / 0.783 | bloque E2 (l. 134–138) y `[E2-01]`–`[E2-04]` |
| Dispersión anual del residuo sin logaritmo: 26.5 … 5.1 … 37.2 | bloque E2 (l. 139–140) y `[E2-08]` |
| `USAccDeaths`: 9652 (1973), 8395 (1976), 8802 (1978) | `[E2-07]` |
| `nottem`: veinte medias anuales entre 47.3 y 50.7 °F | `[E2-06]`; la unidad, `[ENT-04 ?nottem]` |
| Var(R) es el 21.7 % de Var(S+R) sin logaritmo y el 6.3 % con él | `[E2-04]`, `[E2-03]` (última columna) |
| Qué son `nottem` y `USAccDeaths` | `[ENT-04 ?nottem]`, `[ENT-04 ?USAccDeaths]` |

Las cifras que daba el encargo (0.994/0.937 y 0.968/0.783; `nottem` 0.205) **se confirman**.

---

## 3 · Ejercicio 3 — mejorado

| | Antes | Ahora |
|---|---|---|
| Enunciado | «Con IA como tutor, pide un contraejemplo donde la descomposición clásica falle (un atípico) y verifica en R que STL lo maneja mejor.» | Igual de partida, pero el experimento se hace **dos veces**: julio de 1955 (obs. 79, el del M7) y julio de 1960 (obs. 139, al final). Tres entregables: (a) la petición y el código recibido, sin retocar; (b) la tabla 3 métodos × 3 series; (c) tres frases: qué confirma la tabla de lo que dijo el asistente, qué desmiente o matiza, y qué cambia con el atípico al final |
| Pista | Daba el argumento («STL tiene un argumento que hay que activar…») | Pide que cada método se compare consigo mismo, pide una apuesta sobre dónde hará más daño el atípico a la clásica, y manda a repasar qué julios entran en el índice. No nombra `robust` ni dice el resultado |
| Solución | Solo el centro; «cinco veces menos» | Centro y final; por qué la clásica casi no se mueve al final (no ve ese dato: sin tendencia no hay cociente ni residuo); las dos líneas base de la STL como apartado propio (+1.17 %); y qué mirar en la respuesta del asistente, que es el entregable (c) |
| Errata | «reponderea» | Desaparece con el párrafo |

En el enunciado se nombra «la opción robusta» porque la tabla la exige; lo que queda por descubrir ya
no es ese argumento (que el M7 enseña y el resumen del M9 repite), sino el resultado del final de la
serie y las dos líneas base.

Además, en el M7 (l. 4276–4277), la remisión «El **Ejercicio 3** del cierre compara estas cifras con
las del método clásico» gana «, y repite la prueba con el atípico al final de la serie». El párrafo
no lleva `data-afirma`.

| Cifra en el capítulo | Etiqueta |
|---|---|
| Tabla de índices: 1.2266 / 1.2416 / 1.2562 · 1.2758 / 1.2806 / 1.2458 · 1.2292 / 1.2810 / 1.2440 | bloque E3 (l. 160–163) |
| Distorsiones: +4.02, +3.14, −0.82 (centro) · +0.21, +3.17, −0.97 (final) | bloque E3 (l. 164–166) |
| Tendencia y residuo clásicos de la obs. 139: `NA`, `NA` | bloque E3 (l. 167–168) |
| 364 → 546 y 622 → 933; obs. 79 = julio de 1955, obs. 139 = julio de 1960 | `[E3-01]` |
| «cinco veces menos que la clásica» (4.9) | `[E3-04]` |
| «diecinueve veces menos» (18.9) | `[E3-03]` |
| Sin tendencia en los seis últimos meses (obs. 139–144) | `[E3-05]` |
| El índice de julio se promedia con los once julios de 1949 a 1959 | `[E3-06]` |
| La tendencia de enero a junio de 1960 sube hasta 25.9 mil | `[E3-07]` |
| Esos seis índices bajan entre 0.04 % y 0.27 %; los otros seis suben todos 0.21 % | `[E3-08]` |
| STL robusta al final: peso 0; residuo 0.4565 frente a 0.0371 | `[E3-13]` |
| La opción robusta sobre la serie limpia: 1.2416 → 1.2562, +1.17 % | `[E3-02]` |
| Cuatro observaciones sin peso y 18 por debajo de 0.5 en la serie limpia | `[E3-13b]` |
| `robust = FALSE` es el valor por defecto | `[E3-14]` |

Las cifras que daba el encargo (+0.21 %, −0.97 %, +1.17 %) **se confirman**. Añadida, medida aquí:
la STL sin opción robusta con el atípico al final, +3.17 %.

---

## 4 · El quiz

### Entradilla

Antes: «…en las numéricas y en la de selección múltiple la explicación es una para el acierto y otra
para el fallo.» Ahora: «…en la de selección múltiple se explica cada opción que se haya juzgado mal,
y en la numérica la explicación es una para el acierto y otra para el fallo.» Dos motivos: la
pregunta 5 tiene ya `retro` por opción, y con la 6 convertida en opción queda una sola numérica.
«Ocho preguntas» no cambia.

### El motor: un campo opcional, `datos`

Las preguntas 2 y 6 enseñan datos antes de preguntar. Una tabla dentro del `<p>` del enunciado no es
HTML válido y dejaba la etiqueta del tipo de pregunta debajo de la tabla, así que el motor gana un
campo opcional `datos` (HTML) que se pinta entre el enunciado y las opciones: siete líneas en
`renderAutoevaluacion()` y tres de comentario en la cabecera. Es compatible hacia atrás (si no hay
`datos` no hace nada). **Es un cambio solo del motor del capítulo 1**: los de los capítulos 2 a 6 no
lo tienen; si otro capítulo quiere preguntas con datos habrá que llevarlo. Con él va una regla CSS
(`.quiz-datos`, l. 1596–1626) que reutiliza `.tabla-desplazable`; ninguna clase nueva de Tailwind.

La pregunta 6 empezó con una tabla de tres columnas; a 375 px la tercera quedaba fuera de la vista
(había que desplazarla), y era la que hacía falta. Se cambió por una lista de tres líneas, que parte
línea sin esconder nada.

### Ítem por ítem

**Q1 · ciclo y estacionalidad** (opción, M4). Se conserva la pregunta, la pista y la correcta en la
posición 2.
- Opciones reescritas a longitud pareja (71 / 75✔ / 80 / 81; antes 63 / 107✔ / 67 / 54).
- Distractor 4, de relleno («Son sinónimos…»), sustituido por un error real, el que proponía el
  diagnóstico: «Son lo mismo a dos escalas: un vaivén que vuelve cada 12 meses es un ciclo anual.»
  Su `retro` separa el uso corriente de «ciclo anual» del componente.
- `retro` del distractor 3: añade que al descomponer el ciclo ni siquiera sale aparte (va en la
  tendencia-ciclo).
- Sin cifras nuevas.

**Q2 · qué descomposición conviene** (opción) — **rehecha**.
- Antes: «En `AirPassengers`, la amplitud de las oscilaciones anuales **crece** con el nivel de la
  serie. ¿Qué descomposición conviene?» (la regla, enunciada al revés).
- Ahora: una tabla con el nivel medio y la amplitud de la producción trimestral de gas en Australia
  (`Gas`, de `aus_production`, que viene con `fpp3`) en 1960, 1975, 1990 y 2005, **sin** la columna
  amplitud/nivel: hay que calcularla. La premisa ya no está en el enunciado, y la serie no es
  `AirPassengers`.
- Distractores, los tres errores reales: «Aditiva: la amplitud sube más o menos lo mismo de una fila
  a la siguiente» (confundir «sube» con «suma»; los saltos son 14, 22 y 13); «Cualquiera de las
  dos…» (lo que sí pasa en `co2`, ejercicio 1, y no aquí); «Ninguna todavía: antes hay que
  diferenciar…».
- **`retro` del distractor 1**: ya decía «U» (R1), no «embudo». Ahora da las cifras: la dispersión
  anual del residuo aditivo de `Gas` es 12.1 (1960), 1.7 (1985), 11.9 (2005), y es «la misma forma
  que el Módulo 6 mide en `AirPassengers` (30.5 en 1949, 5.6 en 1954, 25.4 en 1960)». Las tres
  cifras del M6 están en el capítulo (l. 4124, la fórmula con las doce desviaciones) y en R (`[Q2-12]`, `[Q2-13]`).
- `retro` del distractor 3: ya no apela a Box–Cox, sino al logaritmo.
- La correcta ya no dice «o equivalentemente aditiva sobre el logaritmo» (aproximado en la clásica,
  1.2266 frente a 1.2347): dice «Multiplicativa: la amplitud se mantiene cerca del 30 % del nivel
  medio», y la equivalencia producto ↔ suma de logaritmos va en su `retro`, como estaba.
- **`modulo: 6 → 4`**. Comprobado en el navegador: fallando solo la Q2, el resumen manda al
  «Módulo 4: Los cuatro componentes» (`r5_navegador.out`).
- Pista nueva: «Que la amplitud suba no decide nada todavía. Compara dos filas: ¿por cuánto se
  multiplica el nivel de una a otra, y por cuánto la amplitud?»

| Cifra | Etiqueta |
|---|---|
| Tabla: 7.25 / 2 · 47.50 / 16 · 140.25 / 38 · 194.25 / 51 | `[Q2-02]`–`[Q2-05]` |
| 27.6, 33.7, 27.1 y 26.3 % | `[Q2-02]`–`[Q2-05]` |
| El nivel se multiplica por 26.8 y la amplitud por 25.5 | `[Q2-06]` |
| Vaivén fijo de la aditiva, 28.9 petajulios | `[Q2-09]` |
| U del residuo aditivo de `Gas`: 12.1 · 1.7 · 11.9 | `[Q2-10]` |
| U del M6: 30.5 · 5.6 · 25.4 | `[Q2-13]` |
| `Gas` en petajulios, trimestral | `[Q2-00]` (ayuda de `aus_production`), `[Q2-01]` |

**Q3 · media móvil** (numérica, M5) — **rehecha**.
- Antes: cuántos valores de tendencia deja la 2×12 sobre `AirPassengers` (132, escrito en el M5).
- Ahora: «Una serie **trimestral** se suaviza con la media móvil centrada **2×4**. En cada valor de
  la tendencia, ¿qué peso recibe la observación **más alejada del centro** de la ventana?»
  Respuesta 0.125, tolerancia 0.0005 (acepta coma o punto).
- Transfiere a otro período, como pedía el encargo, y cambia de pregunta: ya no cobra los huecos de
  los extremos sino **cómo está construida la 2×m** (por qué los extremos pesan la mitad), que es lo
  que el M5 explica y nadie preguntaba.
- `retroFallo`: **se conserva la forma** —diagnostica el error por la cifra escrita—, con el
  contenido nuevo: 0.25 (el peso de los centrales; los cinco sumarían 1.25), 0.2 (reparto igual; el
  trimestre repetido pesaría el doble), 0.042 (el 1/24 de la 2×12 copiado).
- Pista nueva: describe la construcción y pide contar; no calcula.

| Cifra | Etiqueta |
|---|---|
| Pesos 1/8, 1/4, 1/4, 1/4, 1/8, que suman 1 | `[Q3-01]`, `[Q3-02]` |
| Es el filtro que usa `decompose()` en una serie trimestral | `[Q3-03]` |
| Los dos extremos reúnen 1/4, como cada uno de los otros tres | `[Q3-04]` |
| 0.25, 0.2 y 0.042 | `[Q3-05]` |
| La 2×4 borra un patrón trimestral de suma cero sobre una recta | `[Q3-06]` |

**Q3 y Q4: ¿siguen midiendo lo mismo?** No, y por eso **no se quita ni se fusiona ninguna**. Con
una Q3 que transfiriera el *conteo* (104 de 108 con la 2×4) las dos seguían cobrando la misma idea,
los valores que se pierden en los bordes; el diagnóstico contaba tres ítems de ocho sobre ella. Al
cambiar la Q3 a la construcción de la ventana, queda la Q4 sola con los bordes (más una opción de la
Q5). Quitar la Q4 no era opción: con la Q2 reetiquetada al M4, es el único ítem del M6. Y se evita
tocar el número de preguntas, que arrastra la entradilla.
Alternativa descartada, por si se prefiere: una serie diaria con patrón semanal (orden 7, impar, se
pierden 3 por lado) castiga a quien memorizó «se pierden $m$», pero vuelve a los bordes.

**Q4 · por qué la tendencia no llega a los extremos** (gráfico, M6).
- Opciones a longitud pareja (78✔ / 74 / 70 / 75; antes 103✔ / 52 / 75 / 57).
- Distractor 4, de relleno («el gráfico está recortado»), sustituido por un error real que **el
  gráfico desmiente**: «Porque cada punto promedia los doce meses anteriores, y en 1949 no los hay»
  (la media de un solo lado, que es además lo que hace `rolling()` por defecto). Su `retro`: dejaría
  11 huecos al principio y ninguno al final. Con esto el gráfico deja de ser decorativo.
- Pista: añade «mira en el gráfico dónde falta: ¿en un extremo o en los dos?».
- Cifras: 12 `NA`, 132 de 144 (`[Q4-01]`); 11 huecos al principio y ninguno al final con la media de
  un solo lado (`[Q4-02]`); 2 por lado con la 2×4 (`[Q3-03]`: 4 `NA` en `UKgas`).

**Q5 · ventajas reales de STL** (múltiple, M7).
- **`retro` en las cinco opciones**, que no tenían ninguna. Comprobado en el navegador: al fallar,
  el desglose muestra «La marcaste y no va: …» y «Te faltó marcarla: …» cada una con su explicación.
- **Pista**: antes «Son tres. Piensa en qué le pasa al patrón estacional año tras año, qué ocurre en
  los extremos de la serie, y qué pasa si hay un dato disparatado» (contaba y enumeraba, en el orden
  de las correctas). Ahora: «Repasa cada opción con dos preguntas: ¿la clásica ya lo hacía?, ¿STL lo
  sigue necesitando? Una ventaja real es algo que cambia de un método al otro.» (El motor sigue
  diciendo cuántas faltan; eso es suyo y no se tocó.)
- `retroFallo` acortado: ya no repite lo que ahora dice el desglose.
- Opciones a longitud pareja: 64 / 63✔ / 58✔ / 65 / 60✔ (antes 52 / 62✔ / 58✔ / 75 / 48✔).
- Cifras de los `retro`: el mensaje de error de `stl()` sin frecuencia (`[Q5-01]`); 144 valores
  frente a 132 (`[Q5-02]`); julio de +20.4 % a +27.9 % con ventana 11 (`[Q5-02b]`, las del M7);
  peso 0 (`[Q5-02c]`); $F_S$ de 0.937 a 0.783 (`[E2-03]`, `[E2-04]`).

**Q6 · fuerza de la tendencia** (antes numérica, ahora opción, M8) — **rehecha**.
- Antes: Var(R) = 0.0012 y Var(T+R) = 0.20, calcular $F_T$; la pista daba la división. Los insumos no
  eran los de `AirPassengers` aunque el `retroAcierto` lo decía (`[Q6-05]`: los reales son 0.001074
  y 0.1793).
- Ahora: las varianzas **reales** de tres descomposiciones —`USAccDeaths`, `log(AirPassengers)`,
  `co2`— y la pregunta de cuál tiene la tendencia más fuerte. El trío está elegido para que las dos
  intuiciones fáciles fallen: la mayor Var(T+R) es la de `USAccDeaths` y el menor Var(R) el de
  `log(AirPassengers)`, pero el mayor $F_T$ es el de `co2` (`[Q6-04]`). La cuarta opción es otro
  error real: «No se puede saber: las tres series están en unidades distintas».
- Pista: «$F_T$ no mira ninguna de las dos varianzas por separado. Vuelve a la fórmula del Módulo 8:
  ¿qué operación hace con ellas, y en qué unidades queda el resultado?» No da ningún número.
- Se conserva, en el `retro` de la correcta, la advertencia de que $F_T$ no es «el porcentaje de
  varianza que explica la tendencia».
- La variante «qué le pasa a $F_S$ al cambiar de escala» se dejó para el ejercicio 2, donde es el
  entregable (c); repetirla aquí habría sido cobrarla dos veces.

| Cifra | Etiqueta |
|---|---|
| `USAccDeaths`: 44 960 y 223 800; cociente 0.201; $F_T$ = 0.799 | `[Q6-01]` |
| `log(AirPassengers)`: 0.001074 y 0.1793; cociente 0.0060; $F_T$ = 0.994 | `[Q6-02]` |
| `co2`: 0.06768 y 220.7; cociente 0.0003; $F_T$ = 0.9997 | `[Q6-03]` |

**Q7 · cómo se leen 0.994 y 0.937** (opción, M8).
- Enunciado: «obtuvimos» → «Para `AirPassengers`, en logaritmos y con la STL de partida del
  Módulo 7, resultan…» (voz impersonal y el ajuste declarado).
- Distractor 4, absurdo («conviene descartar el componente estacional»), sustituido por un error
  real: «La descomposición es correcta: con fuerzas así, el residuo es solo ruido.» Su `retro` lo
  desmiente con la misma serie sin logaritmo: $F_T = 0.968$, $F_S = 0.783$ y un residuo en U
  (26.5 · 5.1 · 37.2) (`[Q7-02]`, `[Q7-03]`).
- `retro` de la correcta: «exactamente lo que se ve en el gráfico» pasa a compararse con las
  referencias del M8 (0.205 en `nottem`, 0.005 en `sunspots`; cifras ya publicadas allí, `[E2-01]`
  para la primera).
- Pista: ya no menciona los denominadores distintos, que descartaba dos opciones.
- Longitudes: 64 / 64 / 69✔ / 73 (antes 64 / 63 / 103✔ / 69).

**Q8 · para qué sirve la serie desestacionalizada** (opción, M8).
- **Pista**: antes apuntaba a la correcta («el desempleo cayó respecto al mes pasado… ¿qué habría
  que quitar?»). Ahora: «Empieza por lo que hace la operación: ¿qué componente quita, y cuáles deja
  como estaban? Después pregúntate para qué querría alguien justo esa serie.»
- Distractor 4, débil («Para eliminar los valores atípicos»), sustituido por una confusión real:
  «Para quedarse solo con la tendencia: una curva suave, sin sobresaltos» (la serie ajustada
  conserva el residuo; lo dice el simulador del M8). Su `retro` recoge también lo de los atípicos.
- Longitudes: 64 / 61✔ / 66 / 70 (antes 75 / 93✔ / 39 / 35).
- Sin cifras nuevas. Los `retro` de las opciones 1 y 2 no se tocaron (el de la 2 lo corrigió la R1 y
  la R4 lo revisó).

### Longitud de las opciones, antes y después

Medida con `diagnostico/cap1/comprobaciones/r5_longitudes.py`, en caracteres de texto visible (sin
etiquetas, entidades resueltas, fórmulas contadas como se leen: `$\operatorname{Var}(T_t + R_t)$`
cuenta «Var(Tt + Rt)»). «Antes» es `git show HEAD:…`; coincide con el diagnóstico (107, 62, 103,
103, 93). La salida entera, con el texto de cada opción, está en `r5_longitudes.out`.

| Ítem | Tipo | Antes (✔ = correcta) | ¿Correcta = más larga? | Después | ¿Correcta = más larga? |
|---|---|---|---|---|---|
| Q1 | opción | 63 · **107✔** · 67 · 54 | sí | 71 · 75✔ · 80 · 81 | no |
| Q2 | opción | 32 · 49 · 46 · **62✔** | sí | 74 · 70 · 74 · 71✔ | no |
| Q3 | numérica | — | — | — | — |
| Q4 | gráfico | **103✔** · 52 · 75 · 57 | sí | **78✔** · 74 · 70 · 75 | sí, por 3 caracteres |
| Q5 | múltiple | 52 · 62✔ · 58✔ · 75 · 48✔ | — (medias: 56.0 ✔, 63.5 ✗) | 64 · 63✔ · 58✔ · 65 · 60✔ | — (medias: 60.3 ✔, 64.5 ✗) |
| Q6 | numérica → opción | — | — | 58 · 55 · 59✔ · 63 | no |
| Q7 | opción | 64 · 63 · **103✔** · 69 | sí | 64 · 64 · 69✔ · 73 | no |
| Q8 | opción | 75 · **93✔** · 39 · 35 | sí | 64 · 61✔ · 66 · 70 | no |

**Elegir siempre la opción más larga acertaba 5 de 5; ahora acierta 1 de 6** (el azar daría 1.5).
Elegir siempre la más corta acierta 1 de 6 (Q8). La mayor distancia entre la correcta y la media de
sus distractores es de 5.7 caracteres (antes, hasta 45.7).

### Posición de la correcta

`audita_posicion_correcta.py`: orden 2 · 4 · 1 · 3 · 3 · 2 en los seis ítems de una respuesta
(reparto 1→1, 2→2, 3→2, 4→1; la peor posición se lleva el 33 %; racha más larga, 2). En la Q5, las
correctas siguen en 2, 3 y 5.

---

## 5 · Bloque de código del Módulo 2

| | Antes | Ahora |
|---|---|---|
| Orden | `pasajeros` | `print(pasajeros, n = 2)    # sin n = 2, R imprime las diez primeras filas` |
| Salida | cabecera con otros anchos, `1949 ene`, `1949 feb`, y `#  # ... 142 mas`, que R no escribe | La que R imprime, copiada: cabecera, `1 1949 Jan   112`, `2 1949 Feb   118`, `# ℹ 142 more rows` |
| Nota | — | Un comentario: los meses salen en el idioma del sistema («ene.» si R está en español) |

De dónde sale: `[M2-02 en_US.UTF-8]` (l. 62–67 de la salida). En la consola de este equipo (locale
`C`) la última línea sale como `# i 142 more rows`; en una sesión UTF-8, que es la de RStudio, sale
con el símbolo `ℹ`, y es lo que copia el capítulo. Con R en español los meses son «ene.», «feb.»
(`[M2-02 es_ES.UTF-8]`); por eso el comentario. Sin `n = 2`, R imprime diez filas y «134 more rows»
(l. 45–59).

---

## 6 · Verificación (estado final, tras los dos encargos y la corrección)

| Comprobación | Resultado |
|---|---|
| `MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-1-componentes-descomposicion.html` | **206 de 206 cifras, 0 bloques con discrepancias** (15 bloques de R, 6 de Python). Tras el segundo encargo eran 192; tras el primero, 86; antes de la ronda, 13 de 14 |
| `python3 precalculo/verifica_todo.py` | **«OK 11 verificadores en verde»** (`comprobaciones/r5_verifica_todo.out`), con `compila_tailwind.py --comprobar` incluido: ninguna clase nueva |
| `python3 precalculo/audita_citas.py` | OK; 36 citas visibles, 32 afirmaciones (28 `respaldada`, 4 `con-matiz`), como antes. Sigue el aviso informativo `[A01]` (77 apellidos sin `<cite>`), que ya estaba y no cambia de número |
| `python3 precalculo/audita_posicion_correcta.py` | OK: orden 2 · 4 · 1 · 3 · 3 · 2, la peor posición con el 33 % |
| `python3 precalculo/cuenta_sitio.py` | «Las cifras escritas coinciden con las contadas»: 8 preguntas y 8 ejercicios en el capítulo 1; 25 en el sitio |
| `r5_longitudes.py` | Elegir siempre la opción más larga acierta 1 de 6 (Q4, por 3 caracteres). Q2: 75 · 70 · 74 · 71✔. Q6: 56 · 58 · 57✔ · 51 |
| Navegador, 1200 y 375 px, quiz y ejercicios del M9 (`r5_navegador.out`) | Quiz hecho cuatro veces por ancho. (1) Con fallos y aciertos en todos los tipos: 6 de 8; en la pregunta 3, 0.25 da la pista y **0.13 acierta**. (2) Fallando solo la Q2 y **escribiendo «1/8» en la Q3: acierta al primer intento**; 7 de 8, repaso «Módulo 4». (3) Todo bien, con 0.13 en la Q3: 8 de 8 · impecable. (4) La Q3 fallada dos veces, con 12.5 y 0.042: se cierra en rojo y el `retroFallo` termina en «si respondiste 12.5, eso es el porcentaje». Los rótulos en pantalla son los que nombra la entradilla. La Q6 muestra cuatro series y cuatro opciones que solo las nombran. 0 `.katex-error`, 0 errores de consola, `docSw` 1200 y 375 |
| Navegador, 1200 y 375 px, los cinco ejercicios de módulo (`r5_navegador_cortos.out`) | Los nueve módulos cargan sin `.katex-error` ni identificadores repetidos; en los módulos 2, 3, 6, 7 y 8 la pista y la solución se abren y se cierran; 0 errores de consola; `docSw` 1200 y 375. A 1200 px el código de las cinco soluciones cabe sin desplazamiento, salvo dos líneas que son salida de R (el mensaje de error del M2); a 375 px se desplaza dentro de su caja, como en todo el capítulo |

**Por qué el verificador de bloques no dice «14 de 14».** El bloque del M2 era la única cifra que
faltaba (13 de 14) y ya aparece. El total sube porque las soluciones enseñan su salida tras `#>` —la
que R imprime, copiada— en vez de en comentarios `# …` escritos a mano, y el verificador las
contrasta todas. Era el hueco 12 del diagnóstico («las cifras de las soluciones no están al alcance
de `verifica_bloques_cap6.py`»).

---

## 7 · Lo que queda sin hacer, y por qué

1. ~~Los cinco ejercicios cortos (T5.3)~~: hechos en el segundo encargo (§8).
2. **`precalculo/genera_soluciones.R` y `salidas/soluciones_ejercicios.json`** siguen con las tres
   soluciones antiguas del capítulo 1 (y el veredicto «INDISTINGUIBLE» del ejercicio 1, que la R1
   ya había corregido en el capítulo sin tocar el guion). No lo toqué: el encargo pedía un solo
   guion, ese archivo calcula además los capítulos 3 a 6, y nada lo consume (ningún verificador lee
   el JSON). Habría que decidir si se retira su sección del capítulo 1 o se pone al día.
3. **`precalculo/salidas/inventario_items.json`** (el oráculo del preparcial del Corte I) guarda los
   enunciados antiguos del quiz y de los ejercicios. No se regeneró: es una instantánea de cuando se
   construyó el preparcial, ya aplicado, y no entra en `verifica_todo.py`. La Q3 nueva toca la 2×4,
   que el preparcial también pregunta (allí se calcula un valor; aquí, un peso): no es el mismo
   enunciado, pero conviene saberlo si se rehace el preparcial.
4. **Descripciones de las series sin registrar como afirmaciones.** Lo que el capítulo dice ahora de
   `co2`, `nottem`, `USAccDeaths`, `Gas`, `UKgas`, `mdeaths` y `fdeaths` (qué miden, en qué unidades,
   de qué años) está leído en la ayuda de R en esta sesión y copiado en las salidas (`[ENT-04]`,
   `[Q2-00]` y, en la del segundo encargo, `[ENT-05]`), pero va como texto
   propio, sin `data-afirma` ni `<cite>`: no se atribuye a nadie, y `tsibbledata` no está en la
   biblioteca. Si se quiere tratarlas como la de `AirPassengers` (`c1-m1-04`), hace falta el alta de
   `tsibbledata` en Zotero y un verificador que no sea quien redactó.
5. **El campo `datos` del motor y la regla `.quiz-datos`** viven solo en el capítulo 1. La plantilla
   no se tocó, por instrucción.
6. **La pista de la Q1** («si puedes decir de antemano cuánto va a durar») da el criterio, según el
   diagnóstico. No estaba en la lista del encargo (Q5, Q6, Q8) y se dejó.
7. **Serie por estudiante, M1, M4 y M5 sin ejercicio propio, preguntas de control intermedias**:
   huecos 6 (en parte), 7, 8 y 9 del diagnóstico; fuera de D8. Con el segundo encargo la práctica ya
   no está toda al final: hay un ejercicio en cinco módulos intermedios.
8. **Verificación independiente**: nadie más ha leído esta ronda. Por D9, toca un verificador de
   contexto limpio antes de publicar.

---

## 8 · Segundo encargo: cinco ejercicios cortos de módulo

Uno al final de cada módulo que no tenía práctica: **M2, M3, M6, M7 y M8**. Todos con la misma
forma: un `<div class="exercise">` titulado «Para practicar» con un solo `.ejercicio-guiado` dentro
—enunciado con entregables en lista, una pista y una solución con código y lectura—, colocado al
final del módulo, justo antes de la lista de fuentes (en el M2, que no tiene, al final). Van sin
número, para no chocar con los ejercicios 1, 2 y 3 del M9, a los que remiten el M7 y el quiz; entre
ellos se nombran por su módulo («el ejercicio del Módulo 6»).

**Ninguna clase nueva de Tailwind y ninguna regla CSS nueva.** Se reutilizan `.exercise`,
`.ejercicio-guiado`, `.ejercicio-acciones`, `.ejercicio-boton` y `.ejercicio-panel`; la lista de
entregables y un margen del M2 van con `style` en línea, como en los ejercicios del M9.

**Un cambio en el motor de ejercicios**, de un selector: `iniciarEjerciciosGuiados()` desplegaba el
código de `.ejercicio-panel`; ahora despliega el de todo `.ejercicio-guiado`. Hace falta porque el
ejercicio del M2 da código de partida en el enunciado, y `wrapCodeBlocks()` lo dejaba recortado a
150 px con un degradado.

**Ningún ejercicio obligó a tocar prosa de su módulo.** Lo único que cambia fuera de los cinco
bloques es ese selector, y las dos cifras de la portada y del README.

**Sin red.** Las cuatro series (`UKgas`, `nottem`, `mdeaths`, `fdeaths`) son de `datasets`
(`[ENT-04]`); el guion y los bloques corren sin conexión, y el verificador de bloques los encadena
sin romperse. El único error que el capítulo provoca a propósito (M2) va dentro de `try()`,
precisamente para que la sesión siga.

**El hilo entre ejercicios**, que el encargo pedía y que se amplió: M2 → M8 (se construye el objeto
con `mdeaths` y `fdeaths`, y el M8 desestacionaliza la serie de hombres) y M6 → M7 (el residuo de
`UKgas` manda al paso 1 y después al paso 3, que no tiene arreglo dentro del método clásico; el M7
retoma la serie con STL). Cada ejercicio se puede hacer sin haber hecho el anterior: describe su
serie y no usa objetos de otro.

### 8.1 · M6 — leer el residuo y decidir a qué paso volver (hueco 1 del diagnóstico)

- **Serie:** `UKgas`.
- **Qué pide:** descomponer con la clásica aditiva y mirar solo el residuo.
- **Qué entrega el estudiante** (cuatro frases): (a) la desviación típica del residuo en 1961, 1975
  y 1985 y el nombre de lo que dibujan; (b) a cuál de los cuatro pasos devuelve ese residuo y qué
  cambia en él; (c) la misma medida tras el cambio, con el residuo en unidades de la serie; (d) el
  residuo del primer trimestre en la descomposición nueva y, si tiene forma, qué paso lo explica.
- **Pista:** dibujar el residuo antes de calcular y buscar en las fichas del recorrido la línea «Qué
  te devuelve atrás» que describa lo que se ve. No dice qué paso es.
- **Lo que enseña la solución:** el residuo manda de vuelta **dos veces**. Primero al paso 1 (la U y
  la forma estacional: escala mal elegida); y, ya con la multiplicativa, al paso 3 (el índice del
  primer trimestre queda grande al principio y corto al final: la estacionalidad cambia). La solución
  cita literalmente las dos fichas del recorrido del M6.
- Se usan 1961, 1975 y 1985 porque 1960 y 1986 solo tienen dos residuos cada uno (`[M6-01]`).

| Cifra en el capítulo | Etiqueta |
|---|---|
| Residuo aditivo: 114.1 · 18.8 · 210.6 | bloque M6 (l. 109–110 de la salida) |
| Residuo multiplicativo en unidades: 16.5 · 20.0 · 120.3 | bloque M6 (l. 111–112) |
| Residuo del primer trimestre: 0.90 · 0.93 · 1.03 · 1.08 · 1.08 · 1.11 | bloque M6 (l. 113–114) |
| «seis veces» (1961 frente a 1975) y «once veces» (1985 frente a 1975) | `[M6-03]` (6.1 y 11.2) |
| Primer trimestre aditivo: negativo los 15 años de 1961 a 1975 (−138 en 1961), positivo los 9 de 1978 a 1986 (+259 en 1985) | `[M6-06]` |
| Vaivén fijo de la aditiva, 344.1 | `[M6-04]` |
| Amplitud de la serie: 75.3 en 1961, 805.2 en 1985 | `[M6-05]` |
| «casi siete veces menos en 1961» | `[M6-08]` (6.9) |
| «El residuo de 1985 sigue siendo seis veces el de 1975» | `[M6-08b]` |
| Por debajo de 1 los diez años de 1961 a 1970 y por encima los nueve de 1978 a 1986 | `[M6-13]` |
| Tercer trimestre: 1.24 en 1961, 0.74 en 1985 | `[M6-14]` |
| Índice del primer trimestre, 1.454 | `[M6-11]` |
| 27 años; consumo trimestral de gas, en millones de *therms* | `[ENT-04]`, `[ENT-05 ?UKgas]` |

Las cifras del encargo se confirman: 115.3 en 1960, 18.8 en 1975 y 245.5 en 1986 (`[M6-03]`). Un
matiz sobre «con la multiplicativa se queda entre 0.16 y 0.23»: como cociente, la desviación típica
anual está entre 0.16 y 0.24 en 19 de los 27 años, pero baja a 0.06–0.12 en 1971–1978 y salta a
0.43 en 1970 (`[M6-09]`, `[M6-10]`): no queda plana, y eso es justo lo que el apartado (d) hace leer.
Se dejó la unidad en inglés (*therms*), que es como la da la ayuda de R: «termia» es otra unidad.

### 8.2 · M3 — gráfico de subseries y de rezagos (hueco 2)

- **Serie:** `nottem`.
- **Qué pide:** dibujar los dos gráficos y leer en cada uno algo que el gráfico de tiempo no deja ver.
- **Qué entrega:** (a) del de subseries, los dos datos más alejados de la media de su mes, uno por
  debajo y otro por encima, y cuál de los dos se habría visto también en el gráfico de tiempo; (b) del
  de rezagos, un rezago en que la nube sube, uno en que baja y uno en que no hace ni lo uno ni lo
  otro, con su forma y la explicación.
- **Pista:** qué es la raya de cada panel; qué mes tiene enfrente cada mes con $k$ = 12, 6 y 3; y el
  contraste con `AirPassengers`, que tenía tendencia.
- **Lo que enseña la solución:** diciembre de 1934 (45.8 °F) es rarísimo *para un diciembre* y
  corriente en la serie: solo lo muestra su panel. Y en una serie sin tendencia la nube del rezago 6
  se pone boca abajo, mientras que la del rezago 3 es un anillo: correlación casi cero con
  dependencia perfecta. Las dos formas se comprobaron dibujando los gráficos (capturas en el
  scratchpad de la sesión; `[M3-01]` da fe de que corren sin aviso).

| Cifra en el capítulo | Etiqueta |
|---|---|
| Febrero de 1929: 31.3, −7.9; diciembre de 1934: 45.8, +6.3 | bloque M3 (l. 88–90) |
| Correlaciones −0.018 · −0.896 · 0.921 | bloque M3 (l. 91) y `[M3-07]` |
| Media de febrero 39.2 | `[M3-04]` |
| Febrero de 1929 es el mínimo de toda la serie | `[M3-03]` |
| Media de diciembre 39.5; media de abril 46.3 | `[M3-05]` |
| Abril y octubre: 46.3 y 49.5 de media | `[M3-02]` |
| En `AirPassengers`, rezago 6 = 0.784 | `[M3-09]` (y el propio M3) |
| Sin tendencia (medias anuales entre 47.3 y 50.7) | `[M3-08]` |
| Temperatura media mensual en Nottingham, 1920–1939, en grados Fahrenheit | `[ENT-05 ?nottem]` |

### 8.3 · M7 — aplicar STL con una decisión (hueco 3)

- **Serie:** `log(UKgas)`.
- **Qué pide:** dos STL, con `s.window = "periodic"` y con `s.window = 7`, y elegir.
- **Qué entrega:** (a) el factor estacional del primer trimestre en 1960 y en 1986 con cada ajuste,
  ya sin logaritmos; (b) la desviación típica del residuo con cada uno y la media del residuo del
  primer trimestre antes y después de 1973; (c) cuál elige y por qué, en dos frases; (d) el primer
  trimestre de 1986 en logaritmos y en porcentaje sobre la tendencia.
- **Pista:** `exp()` deshace el logaritmo; y para decidir, mirar la forma del residuo y no su tamaño.
- **Lo que enseña la solución:** se elige el número porque el patrón fijo se equivoca con signo —no
  porque el residuo sea más pequeño—; el *valor* del número importa poco (de 5 a 13 la lectura es la
  misma); y la vuelta por `exp()`: 0.615 en logaritmos es un +85.0 %, no un +61.5 %.
- La vuelta por logaritmos cupo. Se adelanta así a la «trampa» que el M8 explica; la pista da lo que
  hace falta y la solución termina remitiendo al M8.

| Cifra en el capítulo | Etiqueta |
|---|---|
| Factores: 1.542 / 1.542 (periodic) y 1.362 / 1.850 (ventana 7) | bloque M7 (l. 159–161) |
| Dispersión del residuo: 0.152 y 0.054 | bloque M7 (l. 162–163) |
| Medias del residuo del T1: −0.094 / 0.090 y −0.003 / 0.002 | bloque M7 (l. 164–166) |
| 0.615 en logaritmos, 1.850 como factor | bloque M7 (l. 167–168) |
| «un 36 % más» y «un 85 % más» | de 1.362 y 1.850 |
| Tercer trimestre: de 0.703 a 0.460 | `[M7-03]` |
| «casi tres veces menos disperso» | `[M7-04]` (2.8) |
| 0.044 con ventana 5, 0.066 con 13; factor de 1986 entre 1.811 y 1.855 | `[M7-05]` |
| +85.0 % frente a +61.5 % | `[M7-02]` |
| 27 primeros trimestres; el 1.º es 1960 y el 27.º, 1986 | `[M7-01]` |

### 8.4 · M8 — construir la serie desestacionalizada (hueco 4)

- **Serie:** `mdeaths`, la de hombres del ejercicio del M2.
- **Qué pide:** construirla de dos maneras, restando $\hat{S}_t$ de una STL sobre la serie y
  dividiendo entre $\exp(\hat{S}_t)$ con una STL sobre el logaritmo.
- **Qué entrega:** (a) la observada y las dos ajustadas de noviembre de 1975 a febrero de 1976; (b) la
  mayor diferencia entre las dos, el mes en que cae y por qué ahí; (c) dos lecturas: cuánto queda de
  la subida de noviembre a diciembre de 1975, y si febrero de 1976 sigue destacando.
- **Pista:** las dos fórmulas del módulo, y dos apuestas antes de mirar la tabla.
- **Lo que enseña la solución:** para qué sirve la serie (de una subida de 521 quedan 97 o 37), qué
  no hace (febrero de 1976 sigue siendo el máximo: el atípico se queda en el residuo), y dónde pesa
  la elección de escala (en el mes extraordinario: 229 de diferencia, cuando la mitad de los meses
  se separan menos de 55).

| Cifra en el capítulo | Etiqueta |
|---|---|
| Tabla de cuatro meses: 1545 / 1652 / 1613 · 2066 / 1749 / 1650 · 2020 / 1398 / 1379 · 2750 / 2175 / 1946 | bloque M8 (l. 188–192) |
| Diferencia máxima 229, en febrero de 1976 | bloque M8 (l. 193–194) |
| Restar quita 575; dividir, entre 1.413, quita 804 | `[M8-06]` |
| La mitad de los 72 meses se separan menos de 55; solo dos, más de 100 | `[M8-08]` |
| +521 observada, +97 restando, +37 dividiendo | `[M8-04]` |
| El patrón anual pone 424 muertes más en diciembre que en noviembre | `[M8-05]` |
| 2750 es el máximo de la serie; 2175 y 1946 siguen siendo el máximo de cada ajustada; segundos valores, 1818 y 1729 | `[M8-01]`, `[M8-09]` |
| Muertes mensuales de hombres por enfermedades pulmonares, Reino Unido, 1974–1979 | `[ENT-05 ?UKLungDeaths]` |

La ayuda de R dice «bronchitis, emphysema and asthma»; el capítulo lo resume en «enfermedades
pulmonares», que es el título de la página («Lung Diseases»).

### 8.5 · M2 — construir el objeto desde datos crudos (hueco 5)

- **Series:** `mdeaths` y `fdeaths`, en una tabla cruda de 144 filas que el enunciado da hecha (cinco
  líneas de código, a la vista).
- **Qué pide:** convertirla en un `tsibble`.
- **Qué entrega:** (a) lo que responde `as_tsibble(crudo, index = mes)` y por qué; (b) la cabecera
  cuando se declara la clave sin tocar `mes`, con su intervalo y lo que contesta `has_gaps()`; (c) el
  objeto bien declarado, y una frase que diga qué cambió.
- **Pista:** la regla del módulo, cuántas filas son de enero de 1974, de qué clase es `mes`, y que
  `yearmonth()` convierte una fecha en un mes (el módulo no la nombra; sin ese dato no se puede
  llegar).
- **Lo que enseña la solución:** las tres declaraciones del encargo —índice, clave y frecuencia— con
  un fallo distinto para cada una. Sin clave, el objeto se niega. Con clave pero con el mes como
  fecha de día, **se construye sin protestar** y queda mal: `[1D]` y huecos. Es la nota del módulo
  («declararla mal no produce un error») hecha ejecutable.

| Cifra en el capítulo | Etiqueta |
|---|---|
| El error de `as_tsibble()` sin clave, y las dos cabeceras (`144 x 3 [1D]`, `144 x 3 [1M]`, `Key: sexo [2]`, 2134 y 1863) | `[M2-00 en_US.UTF-8]` (l. 55–73), que es la sesión UTF-8; el bloque en la consola de este equipo, l. 33–51 |
| `has_gaps()`: `TRUE TRUE` y `FALSE FALSE` | las mismas líneas |
| 144 filas = 72 meses × 2 sexos; dos filas por mes | `[M2-01]`, `[M2-02]` |
| 2161 días entre el 1 de enero de 1974 y el 1 de diciembre de 1979; 72 datos por serie | `[M2-04]` |
| Una STL sobre el objeto `[1D]` avisa de los huecos y devuelve un modelo vacío | `[M2-08]`; sobre el `[1M]` se ajusta, `[M2-09]` |
| `cbind(mdeaths, fdeaths)` es un `mts` de frecuencia 12 | `[M2-06]` |

**El bloque no ejecutable del M2 (`ventas`, cinco tiendas) se deja como está.** Es una ilustración
dentro de la exposición: lleva `class="lang-r"`, así que el verificador no lo ejecuta, y su mensaje
es el que da `tsibble` (comprobado: `[M2-00]`, segunda línea del error; el real añade delante la
llamada y detrás una línea sobre `duplicates()`). Cambiarlo por `mdeaths` y `fdeaths` habría dejado
el ejercicio resuelto dos párrafos antes de plantearlo; así, el texto enseña la regla con un caso
inventado y el ejercicio la hace reproducir con datos de verdad. Queda a criterio del docente.

### 8.6 · Cuánto creció el capítulo

| | Antes de la R5 | Tras el primer encargo | Tras el segundo |
|---|---|---|---|
| Líneas del archivo | 8252 | 8483 | 8898 |
| Tamaño (bytes) | 453 325 | 470 835 | 498 726 |
| Palabras dentro de los nueve módulos (sin código) | 14 317 | 15 530 | 18 042 |
| Líneas de código en bloques | 245 | 286 | 431 |
| Ejercicios (`.ejercicio-guiado`) | 3 | 3 | 8 |

El segundo encargo añade unas 2500 palabras y 145 líneas de código, repartidas así (palabras del
módulo antes → después): M2 437 → 917, M3 1551 → 2072, M6 3069 → 3623, M7 3304 → 3832,
M8 1266 → 1695. Casi todo va dentro de la pista y la solución, que están cerradas hasta que se
piden: lo que se lee de corrido en cada módulo es el enunciado, de 117 a 135 palabras.

**Las duraciones declaradas de los módulos no se tocaron** (`courseData`: 7, 20, 22, 20 y 10 min
para los cinco). Miden la lectura, y un ejercicio hecho de verdad lleva bastante más que leerlo; si
se quiere que la portada o el índice digan cuánto, es una decisión del docente.

### 8.7 · Lo que deja abierto el segundo encargo

1. **Verificación independiente** de los cinco ejercicios: nadie más los ha leído (D9).
2. **El M2 pasa de 437 a 917 palabras**: es el módulo que más crece en proporción, por la salida de
   R de las tres cabeceras. Si pesa, lo primero que se puede recortar es la impresión de `diario`.
3. **`inventario_items.json`** tampoco recoge estos cinco enunciados (§7, punto 3).
4. **El selector del motor de ejercicios** cambió solo en el capítulo 1, como el campo `datos` del
   quiz (§7, punto 5).

---

## 9 · Corrección tras la verificación independiente (16 puntos)

Se aplicaron los 16. Lo que sigue dice, punto por punto, qué había y qué queda. Las cifras nuevas
salen de los dos guiones de la ronda, vueltos a ejecutar: `r5_ejercicios_quiz.out` (etiquetas `E…`,
`Q…`) y `r5_ejercicios_cortos.out` (`M…`).

### A · Lo que el estudiante ya sabía antes de llegar al ejercicio

**1. El quiz regalaba el resultado de dos ejercicios.** Las tres remisiones quedan sin el resultado:

| Dónde | Antes | Ahora |
|---|---|---|
| Q7, opción 4 | Daba 0.968 y 0.783 y las tres cifras de la U: el apartado (c) del ejercicio 2 | «…una descomposición puede dar fuerzas altas y dejar un residuo lleno de estructura. El ejercicio 2 lo mide con esta misma serie.» |
| Q5, opción 4 | «…$F_S$ baja de 0.937 a 0.783 (ejercicio 2)» | «Lo que pasa cuando no se hace lo mide el ejercicio 2.» |
| Q2, distractor 2 | «Ajustan casi lo mismo cuando el nivel apenas cambia, que es el caso del ejercicio 1» | «Que den casi lo mismo no se puede dar por hecho: hay que medirlo, y eso es lo que hace el ejercicio 1 con otra serie. Aquí no lo dan…», y siguen las cifras de `Gas` |

El Módulo 9 no se reordenó. Y **el enunciado del ejercicio 2 reconoce lo que ya está impreso**:
«Cuatro de las ocho cifras están ya en la tabla del Módulo 8, las de `nottem` y las de
`AirPassengers` en logaritmos: compruébalas y completa las que faltan.» De las otras cuatro, el
0.799 de `USAccDeaths` sigue saliendo en un `retro` de la pregunta 6 (es el de la opción que lo
nombra, y hace falta ahí); las dos de `AirPassengers` sin transformar ya no aparecen antes del
ejercicio.

**2. Las pistas del ejercicio 1 y del M8 eran la respuesta en forma de pregunta.**
- Ejercicio 1: sale «Si el nivel casi no cambia, ¿cuánta diferencia puede haber…?». Queda la medida
  del nivel (se conserva la pregunta sobre el CO₂ y el ×3.76 de `AirPassengers`) y una apuesta:
  «antes de descomponer, apuesta cuántas ppm separarán a las dos series ajustadas; después compara
  tu apuesta con el apartado (c)».
- M8: salen las dos preguntas retóricas. Queda: «apuesta dos cosas: cuánto de la subida de 521
  muertes entre noviembre y diciembre de 1975 sobrevive al ajuste, y si febrero de 1976 sigue siendo
  el máximo. Después compara tu apuesta con la tabla.»

**3. La pista del M3 enumeraba los tres rezagos.** Ahora solo da el de 12, resuelto: «pregúntate qué
mes tiene enfrente cada mes: con $k = 12$, el mismo mes del año anterior. Hazte la misma pregunta en
los demás paneles.» La comparación con `AirPassengers` ya no dice «con $k = 6$».

**4. El enunciado y la pista del M7 contestaban su apartado (c).** El enunciado ya no abre con «una
estacionalidad que cambia de forma»: dice «aplica STL… dos veces… y decide con cuál de los dos
ajustes te quedas». La pista dice dónde mirar y no qué se va a encontrar: «para decidir no basta el
tamaño del residuo: sepáralo por trimestre y míralo año por año, que es donde se ve si le queda
forma».

**5. El M2.**
- El apartado (a) pide además lo que devuelve `duplicates(crudo, index = mes)`, la función que el
  propio error recomienda y que el capítulo no había mostrado: «¿cuántas filas señala, y por qué
  esas?». Respuesta: las 144, todas; con la clave, ninguna (`[M2-10]`).
- **`yearmonth()` entra en la prosa del M2** (l. 3049–3053), en un párrafo nuevo tras el de la clave:
  la clase del índice dice cada cuánto se midió la serie (`<mth>` y `[1M]` en la salida de arriba),
  `yearmonth()` convierte una fecha en un mes, y para datos trimestrales o semanales están
  `yearquarter()` y `yearweek()` (`[M2-11]`: las tres existen; el índice de
  `as_tsibble(AirPassengers)` es de clase `yearmonth` e intervalo `1M`). Sin `data-afirma`: es
  descripción del software, comprobada ejecutando.
- La pista ya no nombra `yearmonth()`: manda a comparar la clase de `mes` con la del índice de
  `pasajeros`, el objeto del módulo.
- De la solución sale la frase sobre `cbind(mdeaths, fdeaths)`, que no respondía a ningún apartado.

**6. El apartado (b) del M6 se resolvía emparejando frases.** Ahora pide además una predicción:
«qué esperas que les pase a las tres cifras si ese era el único fallo», y el (c) la contrasta. La
predicción de la solución: el residuo multiplicativo es un cociente alrededor de 1, así que debería
ser igual de disperso en los tres años. No se cumple: 0.162, 0.072 y 0.195 (`[M6-09b]`); la U sigue,
menos honda (2.7 veces entre 1985 y 1975, frente a 11.2 en la aditiva). Por eso el residuo
multiplicativo se mide ahora como cociente, y no traducido a unidades de la serie como en la primera
versión (16.5 · 20.0 · 120.3, que salen del ejercicio).

### B · Lo que estaba mal dicho

**7. Los años del apartado (c) del M7 no cuadraban.** Medido (`[M7-06]`, `[M7-06b]`, `[M7-06c]`): con
`"periodic"` el residuo del primer trimestre es negativo 16 años y positivo 11; negativo los once de
1960 a 1970, positivo los nueve de 1978 a 1986, y entre medias todavía negativo en 1972, 1973, 1974,
1975 y 1977. Coincide con la medida del coordinador.
- El enunciado ya no da el corte de 1973: el apartado (b) pregunta «¿cambia de signo a lo largo de
  la serie? Si cambia, ¿desde qué año?».
- La solución dice lo medido: negativo los once años de 1960 a 1970 y positivo los nueve de 1978 a
  1986; la media pasa de −0.094 en los trece primeros años a +0.090 en los catorce últimos; «el
  cambio no es de golpe: entre 1971 y 1977 todavía es negativo cinco años, y desde 1978 no vuelve a
  serlo». El código lo cuenta por tramos (11 · 5 · 0 con `"periodic"`, 7 · 4 · 4 con la ventana
  de 7).
- El apartado (c) dice ahora «once años seguidos hacia un lado y nueve seguidos hacia el otro», que
  es lo que hay (`[M7-06c]`), en lugar de «trece… y catorce».

**8. El Módulo 7 y el ejercicio 3 se contradecían.** El párrafo «El atípico» del M7 (l. 4529–4532)
leía el +24.6 % de la STL robusta contra la línea base no robusta. Ahora: «La comparación buena es
con su propia línea base, el ajuste robusto de la serie sin inflar, que ya no da +24.2 % y 283.2 mil
sino +25.6 % y 283.1 mil: frente a ella, el julio estacional queda en +24.6 % y la tendencia en
282.2 mil.» Cifras: `[E3-13c]`; contra su línea base el índice baja un 0.82 % (`[E3-13d]`), que es
lo que dice el ejercicio 3. El `retro` de la opción 5 de la Q5 dice ahora «los otros dos componentes
apenas se mueven frente a su propia línea base, que es el ajuste robusto de la serie sin inflar». El
párrafo no lleva `data-afirma`.

**9. Comentario de código engañoso (M7).** `# los 27 primeros trimestres` → `# el primer trimestre
de cada anio`.

**10. «La nube sube / baja» (M3).** En el enunciado, la solución y la pista: «se inclina hacia
arriba», «se inclina hacia abajo», «no se inclina hacia ningún lado». «Se cierra sobre la diagonal»
se conserva: es el vocabulario del módulo.

**11. El ejercicio 2 usaba `nottem` sin decir de dónde venía.** El enunciado la presenta como «la
serie del ejercicio del Módulo 3», y el apartado (b) pide algo que allí no se dio: «el ejercicio del
Módulo 3 ya mostró que ninguno de sus paneles sube ni baja con los años; ¿qué añade a eso su $F_T$,
puesto junto al del ruido puro de la tabla del Módulo 8?». La solución ya no repite las veinte medias
anuales: dice que 0.205 queda mucho más cerca del 0.12 del ruido puro que del 0.799 de
`USAccDeaths`, y que ni una serie sin tendencia da cero. El 0.12 es la cifra publicada en la tabla
del M8 (R3: `r3b_cifras.out`, l. 70); no se recalculó. La pista del ejercicio cambia de apuesta,
porque la de antes («¿en cuál esperas el $F_T$ más bajo?») ya la contesta la tabla del M8.

### C · El quiz

**12. La entradilla usaba nombres que el motor no pinta.** Ahora (l. 5325–5329): «Ocho preguntas
para comprobar lo esencial; cada una lleva su rótulo. Las de «Opción múltiple» y la de «Lectura de
gráfico» tienen una sola respuesta correcta, y cada opción trae su explicación. En la de «Varias
respuestas» se explica cada opción que se haya juzgado mal, y en la de «Respuesta numérica» la
explicación es una para el acierto y otra para el fallo.» Comprobado en el navegador contra los
rótulos pintados.

**13. La pregunta 6 se acertaba sin leer los datos.** Rehecha:
- Cuatro series en lugar de tres (entra `nottem`, cuyo $F_T$ ya está en la tabla del M8), y **las
  cuatro opciones solo nombran la serie**, con una aposición que no dice nada de las varianzas:
  «`USAccDeaths`, las muertes accidentales en Estados Unidos», «`log(AirPassengers)`, los pasajeros
  de avión, en logaritmos», «`co2`, la concentración de CO₂ medida en Mauna Loa, en ppm» (correcta,
  sigue en la posición 3), «`nottem`, la temperatura media mensual en Nottingham». Sale la opción
  «No se puede saber: … unidades distintas».
- Sin dividir no se puede elegir: los cuatro cocientes son 0.201, 0.0060, 0.0003 y 0.795
  (`[Q6-04b]`, calculados con las cifras tal como las ve el estudiante).
- El razonamiento va en los `retro`: el de `USAccDeaths` explica por qué no decide la varianza más
  grande; el de `log(AirPassengers)`, por qué no decide el residuo más pequeño; el de `nottem`, que
  dos varianzas pequeñas y parecidas hacen una serie que es casi puro residuo.
- La pista ya no pregunta por las unidades: «Ninguna de las dos varianzas decide por separado.
  Aplica la fórmula del Módulo 8 a las cuatro series, una por una, antes de elegir.»
- `nottem` se da con cinco cifras (4.0613 y 5.1117) para que la cuenta del estudiante dé el 0.205 de
  la tabla del M8; con cuatro daba 0.206.

| Cifra | Etiqueta |
|---|---|
| `USAccDeaths`: 44 960 y 223 800 → 0.201 → 0.799 | `[Q6-01]`, `[Q6-04b]` |
| `log(AirPassengers)`: 0.001074 y 0.1793 → 0.0060 → 0.994 | `[Q6-02]`, `[Q6-04b]` |
| `co2`: 0.06768 y 220.7 → 0.0003 → 0.9997 | `[Q6-03]`, `[Q6-04b]` |
| `nottem`: 4.0613 y 5.1117 → 0.795 → 0.205 | `[Q6-04]`, `[Q6-04b]` |
| Mayor Var(T+R), menor Var(R), mayor y menor $F_T$ | `[Q6-07]` |

**14. La pregunta 3 rechazaba el redondeo.**
- **`tolerancia: 0.0051`, no 0.005.** Con 0.005 exacto, 0.13 seguía fallando: en coma flotante
  `|0.13 − 0.125|` vale 0.0050000000000000044 (`[Q3-04b]`). Con 0.0051 entran 0.12 y 0.13 y siguen
  fuera 0.25, 0.2, 0.042 y 12.5. Lleva un comentario en el código que lo explica.
- **«1/8» ya no se lee como 1.** El motor lee ahora una fracción «a/b» como fracción (cuatro líneas
  en `comprobarNumerica()`, l. 8266–8270): era la respuesta exacta y fallaba en silencio. El
  enunciado dice «Escríbelo en decimales o como fracción». Es un cambio del motor del capítulo 1.
- La línea del 0.13 va en el **`retroAcierto`** y no en el `retroFallo`, porque 0.13 ahora acierta:
  «Si escribiste 0.13 o 0.12, redondeaste: el peso exacto es 1/8». La del 12.5 va en el `retroFallo`:
  «si respondiste 12.5, eso es el porcentaje: el peso es 0.125».
- Comprobado en el navegador: 0.13 acierta (al primer y al segundo intento), «1/8» acierta, y 12.5
  seguido de 0.042 cierra en rojo con la línea del porcentaje.

**15. Q2, distractor 1.** La opción dice ahora la creencia: «Aditiva: la amplitud no depende del
nivel, que es lo que supone ese modelo», y la cifra va en el `retro` («En la tabla sí depende: la
amplitud pasa de 2 a 51 mientras el nivel pasa de 7.25 a 194.25…»). La U se da **en los cuatro años
de la tabla**: 12.1, 6.9, 7.1 y 11.9 (`[Q2-10b]`); sale el 1.7 de 1985, que no estaba en la tabla.

### D · Tamaño y minutos

**16. Tamaño.** El M6 y el M7 bajan a **tres entregables**, y el enunciado del M6 ya no promete
«de una frase cada una».

| Ejercicio | Entregables antes → ahora | Palabras (enunciado, pista y solución, sin código) antes → ahora |
|---|---|---|
| M2 | 3 → 3 | 478 → 477 |
| M3 | 2 → 2 | 519 → 534 |
| M6 | 4 → 3 | 552 → 503 |
| M7 | 4 → 3 | 526 → 494 |
| M8 | 3 → 3 | 427 → 429 |

Siguen sin ser cortos: lo que se ve de corrido es el enunciado (117 a 136 palabras), pero el trabajo
que piden no baja de tres apartados. Recortar más ya es quitar contenido, y eso es decisión del
docente.

**Los minutos declarados, puestos al día.** Hallazgo previo: **`duration` no se pinta en ninguna
parte del capítulo**; es un dato de `courseData` que solo leen los guiones de medida. Aun así se
cuadró, para que no quede una cifra falsa. Medido con la fórmula de la R3, sin tocarla (palabras de
prosa / 180 + 3 min por simulador + 2 min por bloque de código), con `r5_minutos.py`. Hay que elegir
si la pista y la solución cuentan. La R3 las contaba —su 15 del M9 solo sale con las soluciones
abiertas—, así que se mantiene ese convenio: **minutos de lectura con la pista y la solución leídas;
no incluyen el tiempo de resolver el ejercicio ni el de la autoevaluación.** Va escrito en un
comentario sobre `courseData.modules` (l. 5737–5741).

| Módulo | Declarado antes | Medido, paneles cerrados | Medido, paneles abiertos | Declarado ahora |
|---|---|---|---|---|
| M1 | 5 | 5.5 | 5.5 | 5 |
| M2 | 7 | 9.3 | 13.2 | **13** |
| M3 | 20 | 20.2 | 24.4 | **24** |
| M4 | 20 | 20.4 | 20.4 | 20 |
| M5 | 10 | 9.2 | 9.2 | 10 |
| M6 | 22 | 22.4 | 26.5 | **27** |
| M7 | 20 | 20.5 | 24.6 | **25** |
| M8 | 10 | 11.1 | 14.7 | **15** |
| M9 | 15 | 6.2 | 22.3 | **22** |
| Total | 129 | 124.9 | 160.8 | 161 |

El M9 también se cuadró: no era uno de los cinco, pero el primer encargo le alargó los tres
ejercicios y con el mismo convenio su 15 ya era falso. Los módulos 1, 4 y 5 no cambiaron y conservan
lo que declaró la R3.

**El reparto de las dos sesiones no se tocó**: ni el corte tras el M5 ni la posición de ningún
ejercicio. Con los minutos nuevos, lo declarado queda en 72 min la sesión 1 y 89 la sesión 2 (45 % y
55 %); con los paneles cerrados, 64.7 y 60.2 (52 % y 48 %). El verificador mide 33 % y 67 % con otra
cuenta; la decisión es del docente.

### Lo que la corrección tocó fuera de los ejercicios y del quiz

- **Prosa de módulo:** el párrafo nuevo del M2 sobre el índice (punto 5) y el párrafo «El atípico»
  del M7 (punto 8). Nada más.
- **Motor:** la lectura de fracciones en la respuesta numérica (punto 14).
- **`courseData`:** seis duraciones y un comentario (punto 16).

### Cifras nuevas de los ejercicios del M6 y del M7, tras la corrección

| Cifra en el capítulo | Etiqueta en `r5_ejercicios_cortos.out` |
|---|---|
| M6 · residuo aditivo: 114.1 · 18.8 · 210.6 | bloque M6 (l. 115–116) |
| M6 · residuo multiplicativo, como cociente: 0.162 · 0.072 · 0.195 | bloque M6 (l. 117–118) y `[M6-09b]` |
| M6 · primer trimestre: 0.90 · 0.93 · 1.03 · 1.08 · 1.08 · 1.11 | bloque M6 (l. 119–120) |
| M6 · «2.7 veces el de 1975, no once» | `[M6-09b]` |
| M6 · el resto (seis y once veces, 15 y 9 años, 344.1, 75.3 y 805.2, 10 y 9 años, 1.454) | las mismas de §8.1 |
| M7 · factores 1.542 / 1.542 y 1.362 / 1.850 | bloque M7 (l. 166–168) |
| M7 · 0.615 en logaritmos, 1.850 como factor | bloque M7 (l. 169–170) |
| M7 · años negativos por tramos: 11 · 5 · 0 y 7 · 4 · 4 | bloque M7 (l. 171–173) |
| M7 · medias −0.094 / 0.090 y −0.003 / 0.002 | bloque M7 (l. 174–176) |
| M7 · once años seguidos negativos desde 1960 y nueve seguidos positivos hasta 1986 | `[M7-06c]` |
| M7 · 16 negativos y 11 positivos; negativos después de 1970: 1972–1975 y 1977 | `[M7-06b]` |
| M7 · desviación típica del residuo: 0.044 (5), 0.054 (7), 0.066 (13), 0.152 (`"periodic"`) | `[M7-05]` y §8.3 |
| M2 · `duplicates()`: 144 filas, y 0 con la clave | bloque M2 (l. 36–37) y `[M2-10]` |

### Lo que la corrección deja abierto

1. **El reparto de las dos sesiones**, que el coordinador está consultando.
2. **Los cinco ejercicios siguen sin ser cortos** (punto 16).
3. **Tres cambios viven solo en el motor del capítulo 1**: el campo `datos`, el selector que
   despliega el código de los enunciados y la lectura de fracciones.
4. **La corrección no la ha leído nadie más** que quien la escribió.

