# R1 · Registro de cambios · Capítulo 3 «Modelos AR, MA y ARMA»

Ronda R1 del `PLAN_Mejora_Cap3.md` (tareas T1.1–T1.4; decisiones D2 y D5). Fecha: 2026-11-20. Un solo redactor.
Especificación: `diagnostico/cap3/par_academico.md` y la tabla C1 del plan. Base: `ce69262`. Sin commit ni push.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/cap3/cap3_modulos.html` | 46 sustituciones (módulos 1, 2, 5, 6, 7, 8, 9 y 10, y el ejercicio 3) |
| `ensamblado/cap3/cap3_js.js` | 3 sustituciones, todas en `SIMULADORES['manchas-impulso']` (la envolvente). Nada del quiz, de `AUTOEVALUACIONES['parcial2']` ni del simulacro |
| `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` | reensamblado con `ensambla_cap3.py --escribir`; reproducible byte a byte |
| `precalculo/genera_cap3.R` → `salidas/cap3_arma.json`, `cap3_datos.js` | campos nuevos: el MA(1) sin media (θ, e.e., t), `auto_arima_defecto`, los argumentos de la búsqueda exhaustiva y el error de la ACF con 600 términos. Ninguna cifra anterior cambia (solo la fecha `generado`) |
| `precalculo/genera_soluciones.R` → `salidas/soluciones_ejercicios.json` | solo `cap3_ej3`: la ventana 1889–1988, el recuento de ventanas de cien años y la nota, que repetía la explicación falsa. El resto del JSON, idéntico (más la fecha) |
| `diagnostico/cap3/comprobaciones/r1_*` | guiones y salidas de esta ronda |
| `diagnostico/cap3/capturas/r1/` | 18 capturas (ignoradas por git) |

Los capítulos 4, 5 y 6 se reensamblaron en ese orden y quedan **idénticos a HEAD** (md5 `c7d46031…`, `72aac580…`,
`c8e24776…`; `git status` no los lista). El capítulo 2 no se tocó.

**Verificadores al cerrar**

- `python3 precalculo/verifica_todo.py` → 11 verificadores en verde.
- `verifica_bloques_cap6.py --html …capitulo-3…` → **557 de 557 cifras, 0 bloques con discrepancias** (antes 533 de 534).
  Salida en `r1_verifica_bloques.out`. El «la sesión de r terminó con código 1» del principio ya salía en HEAD
  (`diag/ejercicios_verifica_bloques.out`): es el `try(arima.sim(ar = 1))` del M6. `precalculo/serie.csv`, borrado.
- Los 11 bloques de Python, cada uno solo en una carpeta vacía: todos terminan con código 0 y cada cifra de sus
  comentarios está en la salida, salvo las que citan a propósito el valor de R (`r1_bloques_python.out`). El del M9
  corrió dos veces: leyendo la TRM de GitHub Pages y de la carpeta de trabajo.
- `r2b_sintaxis.py` limpio en los caps. 2–6 · `audita_posicion_correcta.py` en verde · `ensambla_cap3.py` reproducible.
- Por HTTP (servidor propio en 8767, cerrado al acabar; Chrome sin ventana con `diag/chrome.js`): los once módulos a
  1200 y 375 px, 0 errores de consola, 0 `.katex-error`, 0 `$` sin renderizar, ningún KaTeX dentro de `<pre>`, sin
  desbordamiento horizontal; en el M9, 0 de 25 barras fuera de la envolvente y la envolvente dentro del eje
  (`r1_revisa.out`).
- No se copió texto de `bibliografia/_local/`. De FPP3 se leyó la §9.5 (`arima.txt`, l. 328) y se usa solo su fórmula.

**Entorno:** R 4.6.0, forecast 9.0.2; Python con statsmodels 0.14.6 y numpy 2.2.6; Node 26.

**Guiones** (`diagnostico/cap3/comprobaciones/`)

| guion | salida | qué comprueba |
|---|---|---|
| `r1_errores.R` | `r1_errores.out` | todas las cifras nuevas de la prosa: ventanas del ejercicio 3, recursión en ρ₁, envolvente, TRM (`auto.arima`, los cuatro AICc, el ρ₁ que induce promediar), PACF cruda y en raíz, límites negativos, causalidad, residuales, CSS frente a ML, elasticidades, `arima.sim`, las dos nociones de periodo y los menores |
| `r1_python.py` | `r1_python.out` | `AutoReg` frente al CSS; residuales crudos y estandarizados de statsmodels; `generate_sample` sin `burnin` |
| `r1_bloques_python.py` | `r1_bloques_python.out` | los 11 bloques de Python publicados, con su salida íntegra |
| `r1_revisa.js` | `r1_revisa.out` | la revisión por HTTP a 1200 y 375 px |
| `r1_edita.py` | — | reaplica sobre HEAD las 49 sustituciones de `ensamblado/cap3/` (cada una única); `--comprobar` dice si el árbol coincide |
| `r1_edita_generador.py` | `r1_genera_cap3.out`, `r1_genera_soluciones.out` | reaplica sobre HEAD las 8 + 4 sustituciones de los dos generadores |
| — | `r1_verifica_bloques.out` | el verificador de bloques al cerrar |

No se añadió ningún `<cite>`, `data-afirma`, autor ni año. La única referencia nueva a una fuente es «FPP3 (sección
9.5)», pedida por la D5 y leída en esta sesión; queda sin marcar para la R4. Se **quitó** una atribución sin fuente
(«la teoría de mercados eficientes»).

Las líneas son las del HTML ensamblado: «orig.» en `58bdfc5`/HEAD (las del informe del par), «ahora» tras la ronda.
Las de «ahora» señalan dónde empieza cada cambio; los finales de rango son aproximados.

---

## T1.1 · Los siete errores de C1

| # | módulo | orig. → ahora | qué decía | qué dice ahora | evidencia |
|---|---|---|---|---|---|
| 1 | Ej. 3 | 6163–6194 → 6237–6279 | El diagnóstico falla fuera de 1770–1869 porque «la prueba gana potencia»; «p < 0.001 en las tres»; moraleja: pasar depende de cuántos datos haya | Falla en las ventanas que llegan al siglo XX, con más datos o con menos: 0.0007 (n = 119), 0.0010 (n = 89), < 0.0001 (n = 289) y, como control, **1889–1988 (n = 100): 0.0006**, añadida al código y a la salida. De las 190 ventanas de cien años pasan 52, todas menos una con inicio entre 1734 y 1785; ninguna de las que alcanzan 1900. Pista, respuesta corta y moraleja reescritas | `r1_errores.out` § E1 y E1b; `r1_genera_soluciones.out` |
| 2 | M5 | 4173–4176, 4221–4225, 4267–4269 → 4183–4186, 4231–4236, 4279–4281 | «aplicada a ρ₁ daría 0.8»; código `0.5*r[1] + 0.3*r[1]` | En k = 1 la recursión dice ρ₁ = 0.5 + 0.3 ρ₁ (ρ₋₁ = ρ₁) y con ρ₁ = 0.8614 el lado derecho da **0.7584**. R: `0.5*r[1] + 0.3*r[2]`; Python: `0.5*r[0] + 0.3*r[1]` | § E2; `r1_python.out`; salida de los dos bloques |
| 3 | M9 + JS | 5371–5377, 5430; JS 8996, 9013 → 5417–5418, 5476; JS 9077–9083, 9098, 9128 | Envolvente ±0.8278ʲ | ±Rʲ/sin ω = ±1.882 × 0.8278ʲ, en la prosa, en la intro del simulador, en el dibujo, en la leyenda y en la lectura. ω se calcula en el navegador con `acos(φ₁/(2R))` | § E3: 16 de 25 barras fuera de Rʲ, 0 fuera de Rʲ/sin ω; `r1_revisa.out`; `capturas/r1/m9-impulso-*.png` |
| 4 | M9, M10 | 5552–5554, 5873 → 5612–5619, 5951 | El AICc no compara modelos con y sin media | Sí los compara (mismos datos, un parámetro más): ruido blanco con media 723.804 y sin ella 722.663; es lo que hace `auto.arima()`. No compara otro d ni otra escala. El bloque de R imprime los cuatro AICc | § E4/E6 (incluye la traza de `auto.arima`) |
| 5 | M10 | 5842 → 5916–5920 | \|w\| < 1 «para que el gradiente no explote ni se desvanezca» | \|w\| < 1 evita que el estado explote; la derivada respecto al estado de k pasos atrás es wᵏ: con \|w\| < 1 se desvanece y con \|w\| > 1 explota | álgebra de h_t = w h_{t−1} + u x_t |
| 6 | M9 | 5532–5536, 5550 → 5577–5590, 5612, 5733–5760 | «el MA(1) que sugiere auto.arima: θ̂ = 0.1262 (e.e. 0.0912, t = 1.38)» | Por defecto `auto.arima(ret)` devuelve ARIMA(0,0,0) con media cero; con `stepwise = FALSE, approximation = FALSE`, un MA(1) sin media con **θ̂ = 0.1326 (e.e. 0.0905, t = 1.47)**. El bloque muestra las dos llamadas; el 0.1262 queda rotulado como el MA(1) con media | § E4/E6; `r1_genera_cap3.out`; `cap3_arma.json` (`sin_media.ma1_*`, `auto_arima_defecto`) |
| 7 | M9 | 5212 → 5239–5242 | En la raíz «la PACF se corta más limpiamente» | No queda más limpia: en la cruda salen de la banda solo los rezagos 1 y 2; en la raíz, además el 6, el 9 y el 16 (0.200, 0.198, −0.199 frente a ±0.196) | § E7 |

## T1.2 · Imprecisiones y menores del par

| par | módulo | ahora | antes | después | evidencia |
|---|---|---|---|---|---|
| 7 | M9 | 5492–5499 | «la transformación es monótona» | El cuadrado es creciente sobre valores no negativos; un límite inferior negativo (h = 7 y 8: −0.209 y −0.114) se trunca en cero antes de elevarlo (su cuadrado, 0.044 y 0.013, sería una cota falsa) | § I1 |
| 8 | M1, M2 | 2837–2840, 2873–2876, 3039, 3131–3132 | «no existe una solución estacionaria» si \|φ\| ≥ 1; «si y solo si»; «varianza finita» | «Estacionario» se declara causal en la definición; con \|φ\| > 1 existe la solución con choques futuros, que no sirve para pronosticar; el triángulo es «estacionario y causal»; la nota de la varianza habla del proceso que depende de los choques pasados | § I2 (φ = 2: la solución cumple la ecuación, varianza 0.336 frente a 1/3) |
| 9 | M8 | 5024–5036; Py 5789–5790 | «cada programa inicializa de otra forma el filtro» | Mismo filtro; R devuelve el primer residual dividido entre √(γ₀/σ²) (52.54/√6.226 = 21.06) y statsmodels lo da crudo; lo mismo el segundo. Lo que relaja la prueba son los residuales sin estandarizar de statsmodels | § I3; `r1_python.out` (estandarizados: 21.056 y −6.911; LB 0.0461) |
| 10 | M7 | 4670–4675 | CSS pasa de 1 «en un 4 %»; ML no, porque la verosimilitud cae a −∞ | «Entre un 3 y un 5 %, según la semilla»; ML no pasa por el sumando y porque `arima()` reparametriza (`transform.pars = TRUE`); en un 13 % de las réplicas ML ≥ 0.999 | § I4: 4.6, 4.4, 2.8 y 3.3 %; 13.0–13.7 %; texto de `?arima` |
| 11 | M7 Py | 4791, 4805–4811 | «El CSS de R no tiene equivalente directo aquí» | `AutoReg(manchas, lags=2, trend="c")` lo reproduce: `[ 1.4032 -0.7099]`, ejecutado en el bloque | `r1_python.out`; `r1_bloques_python.out` |
| 12 | M9 | 5224–5228 | «los intervalos contienen los dos valores o casi» | Las tres particiones se contradicen: con 10 años contiene el 1 y no el 0.5; con 5, al revés; con 11, ninguno por poco | § I5 |
| 13 | M9 | 5623 | «Donde sí hay estructura: en el cuadrado» | «¿Y en el cuadrado? Aquí tampoco» (p = 0.9166) | § E4/E6 |
| 14 | M9 | 5419–5421 | «deja 1.40 de exceso», «traducido a manchas» | Un choque de una unidad en √manchas deja 1.40 unidades; «al quinto» año ha cambiado de signo (ψ₅ = −0.159) | § E3 |
| 15 | M1 | 2892–2896 | «\|B\| = 1, es decir φ = 1» | En el AR(1), φ = 1 o φ = −1; la caminata aleatoria es el primero | § I2 |
| 16 | M6 | 4514–4518 | Sin `burnin` «mete una tendencia espuria» (dudoso) | **Decidido con evidencia:** no hay tendencia (media ≈ 0 en todo t); la serie arranca en cero con varianza reducida: 4.1 en t = 5 frente a 10.3 en régimen (φ = 0.95) | § I4 (final) y `r1_python.out` |
| 17 | M9 | 5421–5423 | Cruces por cero en j = 4.61 y 10.22: «medio ciclo y un ciclo» | Se anulan cuando (j+1)ω es múltiplo de π: j + 1 = 5.61 y 11.22 | § E3 |
| — | M6 R | 4478–4482 | «Para simular una caminata hay que usar `cumsum(rnorm(n))`» | También con `order = c(0, 1, 0)`, que devuelve n + 1 valores; el bloque lo ejecuta (`#> [1] 101`) | § I6 |
| — | M9 | 5600–5610; 5594–5595 | «ruido blanco… coincide con lo que predice la teoría de mercados eficientes» | Se quita la atribución y se añade el aviso: la serie es un promedio de diarios; una caminata diaria promediada daría ρ₁ ≈ 0.25 (0.249 con 21 días); el r₁ observado es 0.105, a 1.7 errores estándar | § E6b (cálculo exacto y simulación: 0.237) |
| 18 | M9 | 5306 | p = 0.2217 | 0.2216 | § Menores (0.22164) |
| 18 | M9 R | 5655 | `#> [1] 0.1643575` | `0.1643997` (el bloque que fallaba) | § Menores; verificador |
| 18 | M9 Py | 5788, 5794 | `# 0.1780`, `# 11.2178` | `# 0.178`, `# 11.218 (en R, 11.2178)` | `r1_bloques_python.out` |
| 18 | M9 Py | 5835–5837 | `# practicamente iguales` | θ y los dos AICc con su salida: `[0.1326]`, `722.653 722.663` | ídem |
| 18 | M1 Py | 2797–2798 | `print(fit.polynomial_ar)  # [ 1. -0.5999]` | `np.round(…, 4)`, con la salida real | ídem |
| 18 | M10 | 6047 | t = 19.29 y −9.47 | 19.31 y −9.46 | § Menores |
| 18 | M10 | 5931 | «el AR(2) tiene tres» | «cuatro, contando la media y σ²» | § Menores |
| 18 | M9 | 5537–5538 | «una muestra de 100 datos» | «una muestra finita (allí, de 200 datos)» | texto del M6 |
| 18 | M9 | 5461–5463 | «hasta el cuarto decimal, lo que imprime `forecast(ar2s, h = 6)`» | Son lo que imprime `forecast()`; el código lo comprueba en las seis primeras filas | bloque de R |
| 18 | Ej. 1 | 6159 | «conserva el 57 % de la anterior» | «…de la desviación de la anterior respecto a la media» | — |

## T1.3 · D2, la TRM congelada

Los bloques de R (5712–5719) y de Python (5817–5823) del M9 ya no descargan de datos.gov.co: leen
`trm_mensual_2015-01_2026-06.csv` de la carpeta de trabajo y, si no está, de
`https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/`, con la misma construcción que el M6 del cap. 2.
Todas las salidas siguen coincidiendo (n = 137, banda 0.1675, ACF, Ljung–Box, AICc, 0.9166). Probado por las dos
vías en Python; en R, por la copia local (el enlace simbólico de `precalculo/`).

## T1.4 · D5, el periodo

Nota nueva tras la fórmula 2π/ω (5357–5367): FPP3 §9.5 da 2π/arccos(−φ₁(1−φ₂)/(4φ₂)), el periodo medio de los ciclos,
que aquí vale **11.84** y no **11.22**. El capítulo conserva la suya. Por qué no coinciden, medido en `r1_errores.out`
§ D5: 11.2178 es el periodo con que oscilan la ACF y los ψ; 11.8356 coincide, hasta el cuarto decimal, con el
periodo en que es máxima la densidad espectral del AR(2). Con el módulo de la raíz cerca de 1 las dos se juntan
(φ = (1.6, −0.99): 9.868 y 9.868).

---

## Lo que no se hizo, y por qué

1. **«6.7 × 10⁻¹⁶» con 600 términos (M4 y comentario del JS).** No se cambia. El par midió 7.2e−16; el generador,
   que ahora lo calcula también con 600 términos, da 6.66e−16 con 600 y con 2000 (`r1_genera_cap3.out`). La frase
   queda respaldada. La diferencia con el 7.2e−16 del par (probablemente medido con el JS) no la investigué.
2. **El quiz `AUTOEVALUACIONES['cap3']`, la actividad del Parcial 2 y el simulacro:** sin tocar. Ninguna clave ni
   retro afirma algo de lo que esta ronda corrige.
3. **La «ventana de Yule» 1770–1869** y «retirado en statsmodels 0.13» (comentario del M7): no se pueden
   contrastar con lo que hay en disco; quedan para la R4. No las amplié.
4. **«siempre dentro de un error estándar o dos» (ej. 3)** se conserva: con la ventana nueva sigue siendo cierto
   (φ̂₂ va de −0.685 a −0.756, e.e. ≈ 0.07).
5. **La reescritura completa del ejercicio 3** (enunciado incluido) es de la R5. El enunciado sigue pidiendo solo
   1700–1988 y 1900–1988; la solución añade 1870–1988 (ya estaba) y 1889–1988.
6. **`auto.arima` sin presentar** y la «elasticidad del Capítulo 1»: son de la R3. Aquí solo se dice qué devuelve.
7. **Gráficas:** solo la envolvente. El eje del gráfico de ψ es automático y ahora va de −2 a 2, con la envolvente
   dentro; el resto es de la R2.
8. **Voz:** los párrafos reescritos van en impersonal; no se cambió el tuteo de los que no se tocaron.

## Para el verificador

- El aviso de la TRM promediada usa el error estándar aproximado 1/√n = 0.085 para decir «a 1.7 errores estándar».
- «La búsqueda por pasos no llega» al MA(1) sin media: sale de la traza de `auto.arima(ret, trace = TRUE)`, que
  prueba el MA(1) solo con media.
- «Densidad espectral» aparece una vez, declarada fuera del curso; si se prefiere, la R3 puede acortar la nota.
- Con `transform.pars = FALSE` el ejemplo de `set.seed(1)` da el mismo 0.9808: la frase atribuye el no pasar de 1 a
  las dos causas juntas, no solo a la reparametrización.
