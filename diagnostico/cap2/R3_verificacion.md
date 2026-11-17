# Capítulo 2 · R3 («estructura») · verificación independiente

Verificador que no redactó la ronda. Objeto: los cambios sin commitear respecto a `HEAD` (`cda761c`) en
`Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` y en los capítulos 3–6 (armazón de la pista de las tablas).
Fecha: 2026-11-17. No se editó ningún archivo del repo salvo este informe, los guiones `comprobaciones/v3_*` y las
capturas de `capturas/r3v/`. Se borró `precalculo/serie.csv`, que dejó el verificador de bloques. `R3_cambios.md` se
leyó solo al final (última sección).

Líneas: las del capítulo 2 tal como está en el árbol, salvo indicación.

## Resumen

| Gravedad | Número |
|---|---|
| **Bloquea publicar** | 0 |
| **Corregir** | 5 |
| **Menor** | 13 |

Todas las cifras nuevas de la prosa y de los `#>` se reproducen con R 4.6.0 (`forecast` 9.0.2, `tseries` 0.10.62) y
con Python (`statsmodels` 0.14.6). Los verificadores dan lo que el redactor declara. Los problemas no están en las cifras,
sino en lo que tres frases nuevas dan a entender (qué hace `ndiffs()`, qué consigue el ADF frente a φ = 0.95 y el
paso 4 del pipeline frente a la tendencia determinista) y en el coste de la pista de las tablas cuando a la tabla le
falta poco por enseñar.

## Comprobaciones de oficio

| Comprobación | Resultado | Salida |
|---|---|---|
| `verifica_bloques_cap6.py --html`, cap. 2 | **277 de 277**, 0 discrepancias (12 bloques de R y 9 de Python) | `v3_bloques_cap2.out` |
| Ídem, caps. 3 · 4 · 5 · 6 | **533/534 · 713/735 · 1199/1212 · 415/434**: lo mismo que antes | `v3_bloques_cap{3..6}.out`, `v3_bloques_resumen.out` |
| `precalculo/serie.csv` tras el verificador | apareció sin seguir en git y **se borró** | — |
| `verifica_todo.py` | **11 verificadores en verde** | `v3_verifica_todo.out` |
| `r2b_sintaxis.py` | cinco «OK», ninguna declaración repetida | `v3_sintaxis.out` |
| Reensamblar 3–6 en una **copia** del worktree (`ensambla_cap3.py --escribir`, luego 4, 5 y 6) | **md5 idénticos** a los del árbol en los cuatro | copia en el scratchpad; orden y salida abajo |
| KaTeX en los nueve módulos, 1200 y 375 px, por HTTP | 0 errores, 0 `$` sin componer, 0 eventos de consola | `v3_katex.out` |
| Minutos (`cuenta_cap2.py`) | declarado − medido ≤ 0.4 min en los nueve módulos; total 106 frente a 105.7 | `v3_minutos.out` |

Reensamblado: `rsync` del worktree a una copia, `md5 -q` de los cuatro HTML, `python3 ensamblado/ensambla_cap3.py
--escribir` y `ensambla_cap{4,5,6}.py`, `md5 -q` de nuevo y `diff`: «IDENTICOS».

## Cifras nuevas, rehechas

`v3_cifras.R` → `v3_cifras.out` y `v3_python.py` → `v3_python.out`.

| Dónde | Cifra publicada | Rehecha | ¿Coincide? |
|---|---|---|---|
| M1 | `AirPassengers`: miles de pasajeros al mes, 1949–1960 | ayuda de R: «monthly totals… 1949 to 1960», «in thousands»; 144 datos | sí |
| M3 | residuo de `decompose(…, "multiplicative")`: n 132, banda ±0.171, r₁ 0.403, r₁₂ 0.294, 14 de 24 fuera | 132 · 0.171 · 0.403 · 0.294 · 14 (rezagos 1, 3–8, 11–13, 18, 19, 23, 24); Python, igual | sí |
| M4 | PACF de `AirPassengers`: seis fuera | rezagos 1, 2, 9, 10, 11, 13 | sí |
| M4 | serie corta: ACF 0.474, 0.235, 0.106; PACF 0.474, 0.014, −0.014, 0.033; fuera el 1 y el 9 | igual | sí |
| M6 | recta con ruido: ADF −5.744, KPSS de tendencia 0.052 | −5.7441 · 0.051544. En 300 semillas: el ADF rechaza en el 100 %, el KPSS no rechaza en el 98 % | sí, y no depende de la semilla |
| M6 | TRM: KPSS de tendencia 0.273 y 0.070 en la diferencia | 0.27297 · 0.069899; 138 meses, 2015-01 a 2026-06 (copia fija) | sí |
| M6 | `AirPassengers`: KPSS nivel 2.739, tendencia 0.096; ADF −7.32; log: −6.42 | 2.7395 · 0.09615 · −7.3186 · −6.4215 | sí |
| M6 | Monte Carlo con «amplitud A fija»: 0, 0.5, 1, 2, 4 | `genera_cap2.R` l. 290: `amplitud*sin(2*pi*t/12)` con la amplitud fija en cada serie | sí (el texto viejo, «creciente», era el inexacto) |
| M7 | `log(AirPassengers)`: con la regla 1 y 1; al revés, ndiffs 0 tras ∇, r₁₂ 0.841, nsdiffs 1 | igual; KPSS de ∇ log: 0.028, p > 0.10 | sí |
| M7 | `UKgas`: trimestral, 1960–1986, 108 | ayuda de R: «1960Q1 to 1986Q4»; 108 | sí |
| M7 | `log(UKgas)`: 1, 0 / 1, 1; 104 y 103; r₁ −0.178 y −0.576 | igual | sí |
| M7 | umbral 0.64 de `nsdiffs()` | `body(nsdiffs)`: `seas.heuristic(x) > 0.64` | sí |
| M7 | identidad 1 − Bᵐ = (1 − B)(1 + B + … + Bᵐ⁻¹) | álgebra directa (suma telescópica) | sí |
| M9 | pipeline con log: d 1, D 1, KPSS p 0.1, n 131; r₁ −0.341, r₁₂ −0.387, 5 de 24 fuera; λ −0.2947 | igual en R y en Python (fuera: rezagos 1, 3, 9, 12, 23) | sí |

**Casos límite de las afirmaciones generales**, también en `v3_cifras.out`:

- `log(UKgas)`: la conclusión aguanta otras pruebas. Tras ∇₄, `ndiffs` con `test = "adf"`, `"pp"` y `alpha = 0.1`
  da 0; `nsdiffs(test = "ocsb")` da 1; `auto.arima(log(UKgas))` elige d = 0, D = 1. Solo `ndiffs(type = "trend")`
  pide 1, y no es lo que el capítulo usa.
- El pipeline de R con `logaritmo = FALSE` sobre `co2` da d = 1, D = 1 (lo que trae el ejercicio 1). Sobre `Nile`
  (m = 1), D = 0 sin error.

## Problemas

### Comprobados ejecutando

| # | Módulo y línea | Qué dice | Qué está mal o qué cuesta | Evidencia | Gravedad |
|---|---|---|---|---|---|
| 1 | M7, caja «Regla del orden», l. 3617 (y la viñeta previa, l. 3753, que ya estaba) | «La segunda [`ndiffs()`] repite el KPSS del Módulo 6 —diferenciar, volver a probar— hasta que deja de rechazar» | `ndiffs()` no usa el KPSS del M6: llama a `urca::ur.kpss` con `use.lag = trunc(3√n/13)`, compara con los valores críticos y para en `max.d = 2`. El M6 usa `tseries::kpss.test` con ⌊4(n/100)^¼⌋ rezagos. Sobre la serie de la propia regla (∇₁₂ log y) dan veredictos opuestos, y **lo dice el mismo módulo 290 líneas más abajo** (l. 3906–3918, «Dos funciones de R que dicen "KPSS" y no dan lo mismo»). Quien lee la caja aprende una cosa que el recuadro siguiente desmiente. Basta con «repite una prueba KPSS (la de `urca`, no la de `tseries` del Módulo 6: ver el recuadro de más abajo)» | `Rscript -e 'print(body(forecast::ndiffs))'`: `kpss_wrap <- function(..., use.lag = trunc(3 * sqrt(length(x))/13))`, `while (dodiff && d < max.d)`. `v3_cifras.out` §«KPSS de ndiffs»: truncamiento 2 frente a 4; estadístico 0.5367 frente a 0.36816 | **corregir** |
| 2 | M5, cierre, l. 3168–3169 | «Con φ = 0.95 y con φ = 1 las series se parecen […]: a ojo la decisión es frágil. El Módulo 6 le pone un número.» | Da a entender que las pruebas del M6 resuelven lo que el ojo no puede. No lo resuelven, y el M6 no habla de la potencia. Con la serie del propio simulador para φ = 0.95, **las dos pruebas dicen «raíz unitaria»**: el ADF no rechaza y el KPSS rechaza la estacionariedad. En 400 réplicas de un AR(1) con φ = 0.95 y n = 200, el ADF rechaza la raíz unitaria el 14.5 % de las veces. La nota del mismo módulo (l. 3066–3070) dice lo contrario: «distinguir φ = 0.95 de φ = 1 acaba siendo casi imposible» | `v3_ar1_adf.js` reproduce el ruido del simulador (`generarRuidoNormal(200, 20260726)`); R: φ = 0.95 → ADF −2.995, p = 0.16; KPSS 0.849, p < 0.01. φ = 1 → ADF −2.784, p = 0.248 (`v3_ar1_adf.out`). Potencia: `v3_cifras.out` §M5, 0.145 | **corregir** |
| 3 | Armazón, caps. 2–6, l. 1169–1180 (CSS) y `avisarContinuacion()` | El desvanecido mide siempre 3.5rem (56 px; 49 px a 375) | Cuando a la tabla le falta menos que eso por enseñar, el desvanecido tapa texto que cabe entero: la última columna se lee al 8–50 % de opacidad para esconder unos pocos píxeles. Pasa en **34 de los 169** casos de tabla × ancho que se desplazan. Los peores son columnas de cifras. Cap. 5 M12, tabla 5, a 800 px: faltan **13 px** y la columna MAPE entera (5.09, 5.38, 2.95, 4.72) queda casi ilegible. Cap. 5 M7, tabla 3, a 375 px: faltan **5 px** y las últimas cifras de «Muestral» (−0.3**41**, −0.3**87**) se apagan. Antes de la ronda se leían. Arreglo sencillo: un ancho de desvanecido igual a `min(3.5rem, resto + 1rem)`, puesto por `avisarContinuacion()` en una variable CSS | `v3_tablas.js` → `v3_tablas.out` (línea por tabla con su resto y los caracteres visibles bajo el desvanecido); capturas `capturas/r3v/c5-m12-t5-800-resto13.png`, `c5-m7-t3-375-resto5.png`, `c4-m8-t1-800-resto19.png`, `c3-m8-t1-800-resto19.png` | **corregir** |
| 4 | M9, resumen, fila «El ADF con estacionalidad», l. 4561 | «Con menos rezagos que el periodo estacional rechaza la raíz unitaria sin motivo» | Dicho como regla. El Monte Carlo del propio M6 lo desmiente para estacionalidades débiles: con A = 0.5 rechaza el 3.6 % y con A = 1 el 5.0 %, lo nominal. La pestaña del paso 4 sí dice «**puede** rechazar». El resumen es lo que el estudiante se lleva: «puede rechazar» o «tiende a rechazar» | `DATOS_CAP2.trampa_estacionalidad.montecarlo.resultados` (incrustado): 3.2 · 3.6 · 5.0 · 11.2 · 17.6 | **corregir** |
| 5 | M3, l. 2669 | «14 de sus 24 barras salen de la banda ±0.171, cuando por azar se esperaría una o dos» | La referencia se queda corta para *este* objeto. El residuo de `decompose()` sale de un filtro, y aunque el residuo verdadero fuera i.i.d., el filtro le añade autocorrelación: en 500 series con tendencia, estacionalidad fija y error i.i.d., el residuo de `decompose` saca en promedio **2.7** barras, y 6 en el percentil 95 (r₁ medio −0.105). La conclusión no cambia, porque 14 sigue lejos, pero «una o dos» no es lo que se espera aquí | `v3_cifras.out` §M3: «barras fuera (media, p95): 2.73 6» | menor |
| 6 | M7, caja de la regla, l. 3615–3616 | `nsdiffs()` «mide la fuerza de la estacionalidad, el F_S del Capítulo 1» | La fórmula es la misma, pero la STL no: `seas.heuristic()` usa `mstl()` y da **0.964** para log(`AirPassengers`); la cifra del Capítulo 1 es 0.937, con su STL de partida, y el propio Capítulo 1 dice que con `s.window = 11` sale 0.964. Un estudiante que compare cifras no las encuentra iguales. Convendría «calculado sobre su propia STL» | `v3_cifras.out`: `seas.heuristic(log AP) = 0.964`; cap. 1, l. 5078–5082 | menor |

### De juicio (lectura como estudiante y como par)

| # | Módulo y línea | Qué dice | Qué está mal o qué cuesta | Evidencia | Gravedad |
|---|---|---|---|---|---|
| 7 | M9, pestaña del paso 4, l. 4277 («∇ si queda tendencia») y l. 4343 | «Comprobar si queda tendencia o raíz unitaria y aplicar ∇» | La ronda añadió en el M6 (l. 3321–3327) que una tendencia **determinista** «se corrige restando la recta», y el M5 advierte que diferenciarla sobrediferencia. El paso del pipeline, que es lo que el estudiante aplica, sigue mandando diferenciar ante cualquier tendencia. El texto ya estaba, pero la ronda volvió explícita la contradicción. Basta con «si queda raíz unitaria» y una remisión al M6 para la tendencia determinista | lectura literal de las dos líneas | **corregir** |
| 8 | M9, «Lo que sigue», l. 4966 frente a l. 4975 | «Queda dependencia, y describirla es el trabajo del Capítulo 3» … «`AirPassengers` espera al Capítulo 5» | La dependencia que queda es en buena parte estacional (r₁₂ = −0.387), que el Capítulo 3 (ARMA) no modela y el 5 sí. Las dos frases, a cuatro líneas, mandan la misma serie a dos capítulos. Propuesta: «el Capítulo 3 da las herramientas; el 5 las aplica a esta serie» | lectura; cap. 3 sin SARIMA | menor |
| 9 | M9, apertura, l. 4242 | «Los pasos 2 a 4 son la regla del orden del Módulo 7; los otros tres la rodean…: mirar antes, comprobar después y dejar constancia» | La regla del M7 tiene cuatro pasos y el cuarto es «se comprueba el resultado», que es el paso 5 del M9. El código dice, bien, «los pasos 2 a 5». Es la misma regla contada con dos cortes | M7, l. 3606–3614; código del M9 | menor |
| 10 | M7, bloque de Python, l. 4036 | «El orden se pone a mano, como en R: primero la estacional (Modulo 9).» | La regla está en el M7. Remite al módulo equivocado (o a los dos sin decirlo) | lectura | menor |
| 11 | M6, l. 3338–3346 | El KPSS de tendencia «no rechaza» y queda «un acuerdo peor»; luego, «Eso es falso, y conviene entender exactamente por qué», y solo se explica el ADF, «el problema es ese y no otro» | Al KPSS, que ahora entra en el acuerdo falso, no le pasa lo de k < m. El lector ve que al desestacionalizar rechaza, pero no por qué no rechazaba. El redactor lo declara | lectura; `R3_cambios.md` §«Lo que se encontró», 1 | menor |
| 12 | M7, caja de la regla, l. 3625, y cierre del M9 | «La diferencia estacional ya lleva dentro una regular, porque 1 − Bᵐ = (1 − B)(1 + B + … + B^{m−1})» | Llevado un paso más allá por un estudiante atento: ∇∇₁₂ = (1 − B)²·S(B) lleva **dos** diferencias regulares, y la serie final tiene r₁ = −0.341, camino del −0.5 que el mismo M7 da como indicio de sobrediferenciación. Nada en el M7 ni en «Lo que sigue» dice por qué no lo es (la solución de un ejercicio lo atribuye al MA(1) del *airline*). Una frase en el cierre lo evita | lectura; M7, l. 3829–3832 | menor |
| 13 | M3, «Tres avisos», l. 2656 | Diferenciar «es el remedio de la segunda fila» | La segunda fila es «Tendencia **o** raíz unitaria: hay que diferenciar». Para la tendencia determinista no es el remedio (M5, y ahora M6). La frase nueva refuerza una fila que ya generalizaba de más | tabla del M3, l. 2636–2638 | menor |
| 14 | M8, apertura, l. 4080 | «Es la razón por la que los Módulos 6 y 7 trabajaron con `log(AirPassengers)`» | El caso principal del M6 (−7.32, KPSS 2.739 y 0.096, k = 12) es sobre la serie **sin** transformar, y el texto lo subraya. Solo la tabla de k y la STL van en logaritmos. Valdría «la mayor parte de los Módulos 6 y 7» | M6, l. 3337 y 3350 | menor |
| 15 | M4, l. 2857–2866 | Un párrafo con nueve definiciones (TRM, unidad, periodo, fuente, ∇, ∇₁₂, logaritmo, `ndiffs`, `nsdiffs`) antes del explorador | Cumple D7, pero es un glosario en prosa: 120 palabras sin una idea que las ate. Como lista de cinco viñetas se consultaría mientras se mueve el selector. La ronda sube el M4 de 7.6 a 9.1 min, y este párrafo es buena parte | lectura; `v3_minutos.out` | menor |
| 16 | M7, l. 3624–3625 | «por eso la recomendación de FPP3 es aplicar primero la estacional» | Atribución **que ya estaba**, sin `data-afirma` ni cita. Ahora está en una caja de definición y lleva un «por eso» que le atribuye un motivo. No es nueva: queda para la R4, como dice el redactor. Ninguna atribución nueva sin cita en el resto del diff | `grep` de las líneas añadidas: ningún autor, año, sección ni `cite` nuevos | menor |
| 17 | M9, l. 4962–4976 | El cierre nombra el Capítulo 3 | No hay enlace al archivo (`capitulo-3-modelos-ar-ma-arma.html`). Es la convención del curso, porque el Capítulo 1 tampoco enlaza al 2, pero el contenido sí empalma con el M1 del 3: el 3 abre con «En el Capítulo 2 apareció, casi de contrabando, el operador B», que es la tercera pieza del cierre | cap. 3, l. 2692 | menor |
| 18 | M7, l. 3861 | «`UKgas`, que viene con R, es el consumo trimestral…» | La serie ya salió en un ejercicio del Capítulo 1 (l. 4329 de ese archivo); decirlo ataría el caso nuevo a algo conocido | `grep -c UKgas` en el cap. 1: 10 | menor |

### Lo que funciona (comprobado)

- **D5, una sola regla.** El M6 (l. 3426) la cita y no la repite. El M7 la escribe en una caja con cuatro pasos. El
  ejemplo de `log(UKgas)` la aplica en los dos órdenes con el mismo vocabulario. La pestaña 3 y el código del M9
  (R y Python) hacen `nsdiffs` → ∇ₘ → `ndiffs` sobre lo que queda. No encontré una cuarta versión: solo el corte de
  pasos del punto 9.
- **D6.** El umbral |λ| < 0.25 salió del código y de todo el capítulo (`grep`). R y Python dan ahora la misma serie
  final, y la pregunta del quiz sobre Guerrero sigue de acuerdo con el M8.
- **D7.** Barrido de primeros usos en los nueve módulos (`grep` por término): ∇, TRM, raíz unitaria, `ndiffs` y
  `nsdiffs`, el logaritmo, MA(1), la banda, el correlograma, Ljung–Box y STL se definen o se anuncian en su primera
  aparición. `D` queda definido en el M7. Ya no queda «ciclo completo», «abombado» ni «período».
- **Promesas.** La tarjeta de `index.html` («y por qué pueden contradecirse») se cumple con `AirPassengers` (M6),
  y sus «9 módulos · 8 simuladores» siguen siendo ciertos (el noveno `data-simulador`, `mi-id`, está en un comentario). El objetivo del M4 se cumple en un caso. La distinción
  determinista frente a estocástica (M5 → M6) se cumple, con una recta que no depende de la semilla. Los «Módulo X»
  nuevos apuntan a lo que dicen. La TRM vuelve en el M9 del cap. 3 como log-retornos, «la variación porcentual
  mensual» en sus palabras. Ljung–Box se define en el M8 del 3.
- **La pista de las tablas, en lo que dice hacer.** Mido de otra manera que el redactor y obtengo lo mismo: 336
  tablas × ancho, 169 se desplazan y **todas** llevan pista. Ninguna la lleva sin desplazarse. Ninguna se desplaza
  por un contenedor sin pista. Al abrir paneles plegados con tablas, la marca se pone bien. A la vista se entiende que
  la tabla sigue (`c2-m1-t0-375-inicio.png`, `c4-m11-t4-1200-inicio.png`), y a mitad de recorrido se desvanece por
  los dos lados (`c5-m1-t0-375-mitad.png`). El fallo es solo el del punto 3.
- **El M7 crece de 13 a 16 min.** La subida se justifica: es la primera vez que el capítulo muestra un caso en que el
  orden cambia la cuenta, que era lo que pedía D5. La parte que más cuesta es el último párrafo de la caja de la
  regla (dos razones, FPP3, la identidad y una remisión, todo en un párrafo). Se entiende con una segunda lectura;
  partirlo en dos viñetas lo aligeraría.

## Lo que no pude comprobar

- El desvanecido en Safari/WebKit (solo Chrome sin ventana) y con desplazamiento táctil real.
- Una carrera de fuentes lentas: si KaTeX o Montserrat terminan de cargar sin que cambie el tamaño de `<main>`, la
  clase puede quedar desfasada. No lo forcé.
- La R4 (fuentes) y la R5 (ejercicios y quiz) quedan fuera; solo comprobé que el quiz no contradice el texto nuevo
  en `nsdiffs`, λ y sobrediferenciación.
- El código de Python que depende de `pmdarima` (solo comentado en el capítulo).

## Dónde difiere mi lectura de `R3_cambios.md`

1. **«Lo que dice la caja del software, leído en el código de `forecast` 9.0.2: `ndiffs()` repite el KPSS mientras
   rechaza».** En el informe es cierto, pero la caja publicada dice «repite el KPSS **del Módulo 6**», y eso es lo que
   el código no hace y lo que el recuadro del mismo módulo desmiente (problema 1).
2. **Pista de las tablas: «pista incoherente en 0».** Coincido. Pero el redactor midió si la pista aparece, no qué
   tapa: en 34 de 169 casos el desvanecido apaga cifras que caben casi enteras (problema 3).
3. **El cierre del M5** («el Módulo 6 le pone un número») no figura en el informe. Sobre la serie del propio
   simulador, el número dice lo contrario de la verdad (problema 2).
4. **Recta con ruido.** El redactor comprobó cinco semillas más y yo 300: 100 % y 98 %. Coincidimos.
5. **El mecanismo del KPSS de tendencia** no se explica. El redactor lo declara, y lo dejo en menor (problema 11).
6. **«El M8 lo recoge (…los Módulos 6 y 7 trabajaron con `log(AirPassengers)`)».** Es cierto solo en parte: el
   caso principal del M6 es la serie sin transformar (problema 14).
7. **Paso 4 del pipeline y resumen del M9.** No se mencionan. La pestaña sigue mandando diferenciar ante cualquier
   tendencia (problema 7) y el resumen convierte «puede rechazar» en «rechaza» (problema 4).
8. Todas las cifras, minutos, verificadores y md5 que declara se reproducen.

## Guiones y salidas

`diagnostico/cap2/comprobaciones/`: `v3_cifras.R`/`.out`, `v3_python.py`/`.out`, `v3_ar1_adf.js`/`.out`,
`v3_bloques.sh`, `v3_bloques_cap{2..6}.out`, `v3_bloques_resumen.out`, `v3_verifica_todo.out`, `v3_sintaxis.out`,
`v3_minutos.out`, `v3_katex.js`/`.out`, `v3_tablas.js`/`.out`. Capturas: `diagnostico/cap2/capturas/r3v/` (42 PNG).
