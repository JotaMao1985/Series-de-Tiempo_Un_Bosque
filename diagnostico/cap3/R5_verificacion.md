# Capítulo 3 · R5 (práctica) · verificación independiente

2026-11-21. Verificador de contexto limpio (Opus 5.5), que no redactó nada de la ronda. Comprobación propia
completa **antes** de leer `R5_cambios.md`; después, contraste con las dudas del redactor (§4). Base:
`HEAD` = `5c2fdb3` más el árbol de trabajo sin commit. No se editó el capítulo ni sus fuentes.

**Veredicto: ninguna clave mal puesta ni cifra que no salga de R; un ejercicio (M7) contradice el aviso del módulo, el quiz repite en la P4 la cifra resuelta de la práctica del M4, y hay seis puntos de pedagogía y cuatro menores: publicable tras corregir 1–6.**

## 1 · Qué se comprobó y cómo

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Los ocho «Para practicar», resueltos de nuevo con código propio (otras variables, cuentas cerradas a mano frente a `ARMAtoMA`/`ARMAacf`, error de reconstrucción teórico $\lvert\theta\rvert^t\lvert\varepsilon_0\rvert$, correlaciones teóricas 0.5 y 0.75 del M3 deducidas aparte, AICc frente a `forecast::Arima()$aicc`) | Todas las cifras coinciden | `comprobaciones/v5_practicas.R` · `.out` |
| Robustez de las simulaciones con otra semilla (M6: 2026 y 99; M7: 4242; P5: 200 semillas) | Mismas conclusiones; la cifra de cada semilla es típica | ídem; `v5_m10_quiz.out` |
| Ejercicios 1–3 del M10 y los 10 ítems del quiz: clave, distractores numéricos, retros, la semilla 329 de la P6, $p$ de Ljung–Box con y sin `fitdf`, las 8 barras fuera de la P9 | Claves correctas; cada distractor numérico es el tropiezo que dice | `v5_m10_quiz.R` · `.out` |
| Cada bloque de solución (8 prácticas + E1–E3) ejecutado **solo**, en sesión limpia | 11 de 11 corren (exit 0) y todas sus líneas `#>` aparecen | `v5_sueltos.py` · `.out` |
| Páginas de ayuda de `WWWusage`, `treering`, `lynx` | Lo que dice cada enunciado (qué mide, longitud, años, unidades) está en la ayuda | `v5_ayuda.R` · `.out` |
| Tolerancias, con redondeo intermedio | Ver hallazgo 4 | `v5_tolerancia_p7.R` · `.out` |
| Frases marcadas: `git diff` y contenido de los 213 elementos `data-afirma` (parser HTML, HEAD frente a ahora) | 213 = 213, **ningún texto marcado cambia**; 3 líneas físicas con `data-afirma` sí aparecen en el diff (hallazgo 13) | `v5_afirma.py` · `.out` |
| `parcial2` y simulacro del M11 | Idénticos (md5 del tramo de `cap3_js.js` desde `AUTOEVALUACIONES['parcial2']` y del de `cap3_modulos.html` desde «Simulacro del quiz») | — |
| `ensambla_cap3.py` y luego `_cap4/5/6.py` | Cap. 3 reproducible byte a byte; caps. 4–6 sin cambios (md5 de `Htmls_Series/capitulo-*.html` igual antes y después; `git diff --stat -- Htmls_Series` solo muestra cap. 3, `index.html` y `README.md`). No hubo nada que restaurar | — |
| `verifica_todo.py` | 11 en verde (incluye `audita_posicion_correcta`, `cuenta_sitio`, `audita_alineacion_modulos`, Tailwind) | `v5_verifica_todo.out` |
| `verifica_bloques_cap6.py --html` sobre el cap. 3 | **1087 de 1087**, 0 bloques con discrepancias (el «write failed» de la sesión de R viene de rondas anteriores: está en los `.out` de R1–R4) | `v5_bloques.out` |
| Minutos (`r3_minutos.py`) | Declarado frente a medido con paneles abiertos: diferencia ≤ 0.5 min en M1–M10 | `v5_minutos.out` |
| Longitud de opciones y posición de la correcta | La más larga no acierta **ninguna** pregunta (P1–P10); razón máx./mín. ≤ 1.22; posiciones 4, 2, {2,4}, 4, 3, 1, {1,3,5}; el auditor de posición, en verde | longitudes medidas con script propio sobre `cap3_js.js` |
| Texto literal de libro en archivos para git | Ninguno en el diff ni en `r5_*`/`v5_*` (solo la ayuda de R, que no es un libro) | `grep` |
| Series de la práctica | Ninguna de la lista prohibida; `WWWusage` y `treering` no salen en otra página; `lynx`, sí en el cap. 4 (duda 1 del redactor) | — |
| Por HTTP (`python3 -m http.server 8793`, Chrome sin ventana por CDP en el 9297), 1200 y 375 px | Los 8 «Para practicar» y E1–E3 abiertos: 0 errores de KaTeX, 0 «$» sin componer, 0 fórmulas que desbordan, página 1200/1200 y 375/375. Quiz hecho en 7 pasadas (todo bien; un fallo y bien; dos fallos; cuatro de valores límite): cierra y puntúa como debe; 1.7, 5.5, 7.1, 7.11 y 1.687 se rechazan, 1,68 (coma), 1.6849, 5.4549, 7.132 y 7.1359 se aceptan. Único evento de consola: el 404 de `favicon.ico`. Servidor y Chrome cerrados al terminar | `v5_recorrido.js` · `.out` · `.json` |

## 2 · Hallazgos

Gravedad: **E** error que enseña algo falso o choca con el módulo · **C** cifra · **P** pedagogía · **m** menor.
Las líneas son de `ensamblado/cap3/cap3_modulos.html` (M) o `ensamblado/cap3/cap3_js.js` (J).

| # | Dónde | Qué dice | Qué es | Evidencia | Grav. |
|---|---|---|---|---|---|
| 1 | M 2723, 2762, 2786, 2787 · práctica del M7 | Pide «las tres $\hat\sigma^2$» y concluye: «Lo mismo pasa con las $\hat\sigma^2$: la de Yule–Walker es aquí un 3 % mayor que la de máxima verosimilitud; en las manchas lo era un 30 %» | Hace justo la comparación que el módulo prohíbe unas líneas antes («**No compares un $\hat\sigma^2$ de Yule–Walker con uno de ML** … no salen del mismo cálculo», c3-m7-14) y que la P10 da por falsa («sus $\hat\sigma^2$ no miden lo mismo»). Las cifras son ciertas (1.0336 y 1.3031); la lectura que sugiere (la brecha de $\hat\sigma^2$ como síntoma del mismo sesgo) es la que el módulo desautoriza | `v5_practicas.out` §M7 | **E** |
| 2 | J 1523–1528 (P4) frente a M 1549–1550 (práctica del M4) | P4: ARMA(1,1) con $\phi = 0.6$, $\theta = -0.3$, $\sigma^2 = 5$ → $5\,(1 + 0.3^2) = 5.45$ | La práctica del M4 (mismo módulo) usa $\phi = 0.8$, $\theta = -0.5$: **el mismo $\psi_1 = 0.3$**, y su solución escribe «$1.09\,\sigma^2$ a dos» pasos. La P4 es esa cifra por 5: quien leyó la solución la contesta sin calcular | `v5_m10_quiz.out` («M4 practica … => P4 = 5 x 1.09») | **P** |
| 3 | J 1483 (retroAcierto de la P2) | «Dos observaciones separadas por más de dos periodos ya no comparten ninguno: es la memoria finita del MA.» | Adelanta el criterio de la P3, que viene justo después (una ACF que se corta en 2 → MA(2)). Criterio del plan: «ninguna retro adelanta un ejercicio» | lectura | **P** |
| 4 | J 1598–1602 (P7) | Tolerancia 0.006 sobre 7.13; la pista pide ir «por partes» | Quien redondea los pasos intermedios a dos decimales —lo natural al ir «por partes»— obtiene 7.06 (todo a 2 decimales), 7.10 ($\sqrt{0.5} \to 0.71$) o 7.17 (cociente → 0.64) y falla sin que la retro le diga por qué; la retro solo nombra 0.12, 13.93 y 7.57. Con 3 o más decimales sale 7.13. Es «la tolerancia que castiga el redondeo»: el fallo no está en el concepto | `v5_tolerancia_p7.out`; por HTTP, 7.11 rechazado | **P** |
| 5 | M 4050 y 4114 · práctica del M9 | «…ni arregla Ljung–Box»; «Ljung–Box, en cambio, no mejora … La transformación … arregló lo que era de escala; la autocorrelación que queda en los residuales no es de escala» | Dicho a medias: en la serie cruda **pasan** el AR(4) que elige el AICc ($p = 0.064$) y el ARMA(2,2) ($p = 0.114$); en logaritmos no pasa ninguno, y el AR(4) cae a $p = 0.009$. Para el modelo elegido, el logaritmo **empeora** Ljung–Box. «No es de escala» es una interpretación que los datos no prueban (y que el redactor reconoce como opinión) | `v5_practicas.out` §M9 (tablas completas) | **P** |
| 6 | M 4075 · práctica del M9 | `aj <- suppressWarnings(arima(...))`, con la pista «sirven tal cual cambiando la serie» | La `compara()` del módulo (M 3556) no lleva `suppressWarnings`: el estudiante que la usa tal cual ve «possible convergence problem: optim gave code = 1» (el ARMA(2,1) sobre la serie cruda) y la solución lo esconde sin decirlo | `v5_m10_quiz.out` §lynx | **P** |
| 7 | M 2416 · práctica del M6 (c) | «$\pm 1.96\sqrt{(1 + 2\rho_1^2)/T}$» | Resultado afirmado sin fuente ni marca. Es correcto y tiene fuente en la biblioteca: Cryer y Chan (2008), ec. (6.1.9), $c_{kk} = 1 + 2\rho_1^2$ para $k > 1$ en el MA(1) (leído en la caché, `bibliografia/_local/texto/cryer2008time/p0122.txt`, página impresa 111); la simulación del bloque lo respalda (0.79 barras) | lectura de la fuente; `v5_practicas.out` §M6 | **m** (fuente) |
| 8 | M 1549 · práctica del M4 (a) | «un promedio de las observaciones pasadas con pesos que … suman $0.6$» | Unos pesos que suman 0.6 no forman un promedio. Lo que enseña la cifra es otra cosa: el pronóstico se encoge hacia la media (0) | `v5_practicas.out` («suma de -pi: 0.6») | **m** |
| 9 | M 2787 · práctica del M7 (b) | «El módulo decía que … Yule–Walker está sesgado hacia el interior de la región estacionaria: con las raíces lejos de la frontera, ese sesgo apenas se nota» | El módulo (c3-m7-13) ata ese sesgo a «muestras cortas», no a la frontera; la práctica añade, con su simulación, que a igual $T$ manda la cercanía de las raíces. No es falso, pero atribuye al módulo algo que no dice | lectura de M 2598; `v5_practicas.out` §M7 | **m** |
| 10 | J 1595 (P7, `modulo: 2`) | Reparto de módulos del quiz: 1, 3, 5, 4, 3, 5, 2, 8, 8, 7 | Antes la P7 era del M9; ahora el M9 (37 min, el más largo) y el M6 no tienen ítem, y el resumen final nunca manda a repasarlos. M3, M5 y M8 tienen dos cada uno | `audita_alineacion_modulos` en verde; lectura | **m** |
| 11 | J 1530–1563 (P5) frente a M 1145 (práctica del M3) y M 4552 (E2 c) | P5: MA(1) con $\theta = -2.5$; ¿qué devuelve `arima()` y qué $\hat\sigma^2$? | Es el experimento de la práctica del M3 ($\theta = 2$ → `arima()` da $0.45$ y $\hat\sigma^2 = 4.03$) con otro número, y el E2 (c) lo repite una tercera vez. Transferencia legítima, pero la P5 discrimina poco | lectura | **m** |
| 12 | M 4567–4568 (E3) | «…y 1889–1988, que tiene los mismos cien años que la ventana del módulo» | El enunciado ya entrega el control que (c) pide descubrir, y la pista lo repite | lectura | **m** |
| 13 | M, líneas de c3-m10-33, c3-m10-90 y c3-m10-34 | — | La regla «`git diff` no cambia ninguna línea con `data-afirma` o `<cite>`» se incumple en la letra: tres líneas físicas cambian. El texto de los 213 elementos marcados es idéntico y `audita_citas.py` pasa | `v5_afirma.out` | **m** (sin acción) |

Fuera del alcance de la ronda (motor compartido con el cap. 2, no lo cambió la R5): tras acertar todo al
**segundo** intento, el resumen dice «Resultado: 10 de 10 · impecable» y a la vez «Te costaron preguntas de
estos módulos» (`v5_recorrido.out`, pasada B): «impecable» se decide por `fallidas.length`, no por los
intentos.

## 3 · Correcciones propuestas (exactas)

**1 (M7, σ̂²).** Tres cambios en `cap3_modulos.html`:
- l. 2723: «Los coeficientes por Yule–Walker, por CSS y por máxima verosimilitud, y las tres $\hat\sigma^2$.» → «Los coeficientes por Yule–Walker, por CSS y por máxima verosimilitud.»
- l. 2762–2764: quitar `round(c(YW = yw$var.pred, CSS = css$sigma2, ML = ml$sigma2), 4)   # las tres sigma^2` y sus dos líneas `#>`.
- l. 2786: «… y máxima verosimilitud, $(0.1388,\ 0.2140)$. Las $\hat\sigma^2$ son $0.0658$, $0.0647$ y $0.0637$.» → «… y máxima verosimilitud, $(0.1388,\ 0.2140)$.»
- l. 2787: quitar «Lo mismo pasa con las $\hat\sigma^2$: la de Yule–Walker es aquí un $3\,\%$ mayor que la de máxima verosimilitud; en las manchas lo era un $30\,\%$.» (Si se quiere conservar el tema: «Las $\hat\sigma^2$ no entran en la comparación: como advierte el módulo, la de Yule–Walker y la de máxima verosimilitud no salen del mismo cálculo.»)

**2 (P4).** Cambiar el proceso para que $\psi_1 \ne 0.3$. Con $\phi = 0.6$, $\theta = -0.2$, $\sigma^2 = 5$ (R, `v5_m10_quiz.out` §Propuesta): `respuesta: 5.80`; retroAcierto «$\psi_1 = \theta + \phi = 0.4$, así que $\operatorname{Var}(e_{T+2}) = 5\,(1 + 0.4^2) = 5 \times 1.16 = 5.80$. …»; retroFallo con los tropiezos recalculados: «$1.16$ es olvidar $\sigma^2$; $0.80$, olvidar $\psi_0 = 1$; $6.80$, tomar $\psi_1 = \phi$; $8.20$, perder el signo de $\theta$ y tomar $\psi_1 = 0.8$; $7.00$, sumar los $\psi$ sin elevarlos al cuadrado; y $6.09$, sumar hasta $j = h$». Los siete valores son distintos entre sí. Actualizar la etiqueta [Q4-0x] de `r5_cifras.R`.

**3 (P2).** J 1483, retroAcierto: quitar la última frase, «Dos observaciones separadas por más de dos periodos ya no comparten ninguno: es la memoria finita del MA.»

**4 (P7).** Mantener la tolerancia y decirlo: J 1598, pista: «… después el arcocoseno— y comprueba que la calculadora trabaja en <strong>radianes</strong>.» → «… después el arcocoseno—, conserva cuatro decimales en cada paso y comprueba que la calculadora trabaja en <strong>radianes</strong>.» J 1602, retroFallo, antes de «Y hace falta la precisión pedida»: «Si te sale $7.06$, $7.10$ o $7.17$, redondeaste un paso intermedio a dos decimales.»

**5 (M9, Ljung–Box).** l. 4050: «… ni arregla Ljung–Box; lo que arregla es la normalidad de los residuales.» → «… ni arregla Ljung–Box —en logaritmos no lo pasa ningún candidato, y el AR(4), que lo pasaba en la serie cruda, deja de pasarlo—; lo que arregla es la normalidad de los residuales.» l. 4114: «Ljung–Box, en cambio, no mejora: … (el AR(4) da $p = 0.009$). La transformación era necesaria y arregló lo que era de escala; la autocorrelación que queda en los residuales no es de escala, y ningún ARMA de la rejilla la recoge.» → «Ljung–Box, en cambio, no mejora, y en el modelo que elige el AICc empeora: el AR(2) da $p = 0.031$ en la serie cruda y $p = 0.013$ en logaritmos; el AR(4) pasa en la serie cruda ($p = 0.064$) y deja de pasar en logaritmos ($p = 0.009$), y en logaritmos ninguno de los once candidatos pasa la prueba. La transformación era necesaria y arregló la normalidad; la autocorrelación que queda en los residuales de la serie transformada no la recoge ningún ARMA de la rejilla.» (Las cifras, en `v5_practicas.out` §M9.)

**6 (M9, aviso).** l. 4075: quitar `suppressWarnings(…)` y añadir tras la definición de `compara` el comentario `# en la serie cruda, el ARMA(2,1) avisa de un posible problema de convergencia (optim code = 1); no lo elige ningún criterio`. Alternativa: dejar `suppressWarnings` y poner ese mismo comentario encima.

**7 (M6, fuente).** l. 2416: marcar el fragmento «$\pm 1.96\sqrt{(1 + 2\rho_1^2)/T}$» como afirmación nueva (c3-m6-XX) con `<cite>` a `cryer2008time`, localizador «p. 111» —**a confirmar** al registrar: la caché pone la ec. (6.1.9) en la página impresa 111, y c3-m5-30 cita la banda de Bartlett general en la p. 112—, entrada en `contraste/cap3.yml` con la huella del literal, y la verifica alguien que no la redactó. Si no se quiere abrir el registro en esta ronda: «…ensanchándola con $\rho_1$ —es la varianza de $r_k$ para $k > 1$ en un MA(1), y la simulación de abajo la pone a prueba—…».

**8 (M4).** l. 1549: «un promedio de las observaciones pasadas con pesos que se reducen a la mitad a cada paso atrás y que suman $0.6$.» → «una suma ponderada de las observaciones pasadas, con pesos que se reducen a la mitad a cada paso atrás y que suman $0.6$, no $1$: el pronóstico se encoge hacia la media del proceso, que aquí es $0$.»

**9 (M7).** l. 2787: «El módulo decía que CSS y máxima verosimilitud se separan con $T$ pequeña o con los coeficientes cerca de la frontera, y que Yule–Walker está sesgado hacia el interior de la región estacionaria: con las raíces lejos de la frontera, ese sesgo apenas se nota.» → «El módulo decía que CSS y máxima verosimilitud se separan con $T$ pequeña o con los coeficientes cerca de la frontera, y que Yule–Walker está sesgado hacia el interior de la región estacionaria con muestras cortas. Aquí la muestra es igual de corta y el sesgo apenas se nota: lo que cambia es lo lejos que están las raíces de la frontera, y (c) lo comprueba.»

**10 (cobertura).** Decisión de Javier: o se acepta (M9 y M6 se practican en sus «Para practicar»), o se cambia `modulo: 2` por un ítem del M9 que no repita la cuenta de 11.22 que ya está en pantalla.

**11–12.** Opcionales. P5: si se quiere más discriminación, preguntar por $\hat\sigma^2$ con $\theta = -2.5$ y $\sigma^2 = 4$ (respuesta $4 \times 6.25 = 25$), para que no baste copiar el 4 de la práctica. E3: quitar «que tiene los mismos cien años que la ventana del módulo» del enunciado y dejarlo solo en la pista.

**13.** Sin acción: el contenido firmado no cambió.

## 4 · Respuestas a las dudas del redactor (§7 de `R5_cambios.md`)

1. **`lynx` en el M9.** Aceptable. El cap. 4 la usa para otra pregunta (¿diferenciar?) y su respuesta ($d = 0$) es coherente con modelar `log(lynx)` como estacionaria aquí; la práctica no responde a esa pregunta ni la discute. Se adelanta la serie, no la respuesta.
2. **M9, el resultado.** Coincido y lo elevo a hallazgo 5: el texto omite que en la serie cruda pasan dos modelos, y para el AR(4) elegido el logaritmo empeora Ljung–Box. La última frase («diciéndolo») puede quedarse; la que sobra es «no es de escala».
3. **M6 (c), la banda ensanchada.** Es correcta (Cryer y Chan, ec. 6.1.9, leída en la caché) y la simulación la confirma (0.79; con otra semilla, el MA(1) da 1.71 frente a 1.78, mismo orden). Hallazgo 7. El apoyo de (b) en c3-m8-11, dentro de un plegado, está bien: la cuenta aproximada con $\operatorname{Var}(r_k) = (T-k)/(T(T+2))$ y media $-1/T$ da 0.54, 0.87 y 0.97 barras, la misma escalera que la simulación (`v5_practicas.out`).
4. **M7.** Lo de que el AR(2) no es buen modelo está bien avisado. La comparación de medias de valores absolutos con dos distancias con signo es aceptable como dirección. El problema del M7 es otro: el $\hat\sigma^2$ (hallazgo 1).
5. **Pistas de P2 y P7.** Dan el método, no el criterio de la respuesta: aceptables. Lo que adelanta un criterio es la **retro** de la P2 (hallazgo 3), y lo que castiga es la tolerancia de la P7 (hallazgo 4).
6. **P6, la semilla.** Elegida y declarada en el comentario: aceptable. Comprobé la 329: $-0.5986$ (0.3806) y $0.6727$ (0.3475); $t = -1.57$ y $1.94$, los dos por debajo de 1.96 también sin redondear; AICc 270.43, 272.43, 272.46 y 273.88.
7. **P7 con etiqueta M2.** El problema no es la etiqueta, que es correcta (la fórmula está en el M2), sino que el M9 queda sin ítem: hallazgo 10. Cambiar `modulo: 2` por `9` sería etiquetar mal.
8. **P5, dos de cinco.** Motor compartido; ya anotado en el cap. 2. Sin cambio en esta ronda.
9. **Ejercicio 1.** La discusión nueva es correcta y coherente con la lista «Qué confirma el orden elegido» (M 4299–4310); cifras verificadas (t = 2.907, ACF teóricas 0.329 y 0.235, Shapiro 0.0083 y 0.0264, `auto.arima` (1,0,0) y (0,0,2)).
10. **Ejercicio 2 (c).** «Cuatro en total» es correcto: invertir la raíz $-2.5$ da $\theta = (3,\ 1.25)$ y invertir las dos, $(4.5,\ 5)$, los dos con la ACF 0.5838 y 0.1081 (`v5_m10_quiz.out`). «Unas cuatro veces»: $2^2 = 4$, medido 4.035.
11. **M3 (c).** Las teóricas 0.5 y 0.75 son correctas: en $u_t = (1+2B)(1+0.5B)^{-1}\varepsilon_t$, $\psi_0 = 1$, $\psi_1 = 1.5$ y $\operatorname{Var}(u_t) = 4$, luego $1/2$ y $1.5/2$. Al ser una cuenta, puede quedarse sin fuente.
12. **Variantes del banco.** No puedo comprobar las 2–8 desde aquí; tampoco yo vi coincidencias con la 1 y la 9.
13. **M5.** `diff(WWWusage)` como estacionaria: la propia ayuda de R hace esa diferencia y `auto.arima(WWWusage)` da ARIMA(1,1,1); aceptable sin prueba en un ejercicio del M5. **516.00 es correcto**: el AICc es 516.0047, que a dos decimales es 516.00 (el bloque lo imprime a tres, 516.005).

## 5 · Guiones de esta verificación (`diagnostico/cap3/comprobaciones/`)

`v5_ayuda.R` · `.out` (ayuda de las tres series) · `v5_practicas.R` · `.out` (las ocho prácticas, con semillas
alternativas) · `v5_m10_quiz.R` · `.out` (E1–E3, quiz, aviso de `lynx`, propuesta para la P4) ·
`v5_tolerancia_p7.R` · `.out` · `v5_sueltos.py` · `.out` (cada bloque solo) · `v5_afirma.py` · `.out` ·
`v5_recorrido.js` · `.out` · `.json` (HTTP, 1200 y 375 px) · `v5_verifica_todo.out` · `v5_posicion.out` ·
`v5_bloques.out` · `v5_minutos.out`.

## 6 · Qué hizo la sesión maestra con cada hallazgo

Correcciones en `comprobaciones/r5_ediciones_maestra.py` (sustituciones únicas, en `cap3_modulos.html`, `cap3_js.js`,
`r5_bloques/m7.R`, `r5_bloques/m9.R` y `r5_cifras.R`); cifras vueltas a medir en `comprobaciones/maestra_r5.R` · `.out`.

| # | Qué se hizo |
|---|---|
| 1 | M7: fuera el entregable, el bloque y las frases de las $\hat\sigma^2$; en su lugar, que no entran en la comparación porque el módulo advierte que no salen del mismo cálculo |
| 2 | P4 con $\phi = 0.6$, $\theta = -0.2$: respuesta 5.80 y tropiezos 1.16, 0.80, 6.80, 8.20, 7.00 y 6.09, medidos (`maestra_r5.out`, [Q4]) |
| 3 | Retro de la P2 sin la frase que adelantaba la P3 |
| 4 | P7: la pista pide cuatro decimales en cada paso; la retro nombra 7.06, 7.10 y 7.17 (medidos, [Q7]). Tolerancia sin cambio |
| 5 | M9: Ljung–Box dicho entero, en la respuesta y en (c); comprobado que en la serie cruda pasan dos candidatos y en logaritmos ninguno |
| 6 | M9: comentario sobre el aviso de convergencia. **Corrección a la propuesta:** el aviso sale en `log(lynx)`, no en la serie cruda (`maestra_r5.out`); el verificador lo confirmó |
| 7 | M6 (c): afirmación nueva **c3-m6-09** con cita a Cryer y Chan (2008, p. 111; ec. 6.1.9), entrada en `contraste/cap3.yml` redactada por la maestra y **firmada por este verificador**, que leyó el pasaje |
| 8 | M4 (a): «una suma ponderada … que suman 0.6, no 1: el pronóstico se encoge hacia la media» |
| 9 | M7 (b): el sesgo de Yule–Walker atado a las muestras cortas, como dice el módulo, y la cercanía de las raíces como lo que (c) comprueba |
| 10 | Sin cambio: decisión de Javier (el M6 y el M9 se practican en sus «Para practicar») |
| 11 | Sin cambio (opcional; la P5 discrimina poco, anotado) |
| 12 | E3: el enunciado ya no entrega el control de los cien años |
| 13 | Sin acción |

Después: verificador de bloques **1084 de 1084** (las tres cifras de las $\hat\sigma^2$ salen); `m7.R` y `m9.R` corren
solos; `verifica_todo.py` 11 en verde tras regenerar `uso_fuentes.json` (`audita_citas.py --uso`); `audita_citas.py`
OK (214 afirmaciones, 214 firmadas); capítulo 3 reproducible y caps. 4–6 sin diff; por HTTP la cita compone
«(Cryer y Chan, 2008, p. 111)», Cryer entra en las fuentes del M6, sin errores de consola ni de KaTeX.
