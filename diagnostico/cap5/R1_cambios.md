# R1 · Registro de cambios · Capítulo 5 «Modelos SARIMA»

Ronda R1 del `PLAN_Mejora_Cap5.md` (tareas T1.1–T1.3; decisiones D2, D3, D4 y D11, y las cuatro correcciones del deck
de §7.2). Fecha: 2026-11-23. Un solo redactor. Especificación: `diagnostico/cap5/par_academico.md` (tabla «Resumen»),
`lector_estudiante.md`, `graficas.md` (Altas de lectura), `ejercicios.md` (E3(b)) y la tabla de §1 del plan.
Base: `7686d33`. Sin commit ni push.

**Archivos tocados**

| archivo | qué |
|---|---|
| `ensamblado/cap5/templates_1_3.html` | M1 (remisión al Módulo 6, intro del `mapa-firma`, TRM congelada, salida del bloque Python), M2 (la ACF factoriza con $2q < m$; el bloque R imprime 1.5217, 2.300/1.700 y la tabla de $\phi$; Python converge), M3 (párrafo de la varianza, intro y tabla de la sobrediferenciación, párrafo de la raíz, bloque R, umbral de KPSS fuera de `#>`) |
| `ensamblado/cap5/templates_4_6.html` | M4 ($\rho_{11}$/$\rho_{13}$ frente al producto, `unname()` y salidas reales del bloque R, salida de numpy), M5 (resultado de la derivación, intro del `airline-pesos`, párrafo nuevo del largo plazo con la remisión al M2, **bloque R/Python nuevo** de los pesos $\psi$), M6 (manchas solares, Ljung–Box sin los 13 residuales de arranque, fila $(0,1,0)(0,1,0)$, bloque Python que converge, «cuatro primeras cifras») |
| `ensamblado/cap5/templates_7_9.html` | M7 (fila «Comprobación» de la tabla, párrafo de la invertibilidad, salida real de R, pesos $\psi$ sin redondear, Python que converge), M8 (TRM congelada en R y Python y en la prosa, $t = 0.0146$, matiz del arbitraje), M9 (definición SARIMAX, intro del simulador, bloque Python con BFGS y OPG frente a la hessiana) |
| `ensamblado/cap5/templates_10_11.html` | M10 (el ARIMA$(0,0,0)(0,1,0)_{365}$ por $n < 3m$, «$m-1$ términos», AIC/AICc de `stlm`, Python con `maxiter`), M11 (salvedad del $K$ de la armónica), resumen, ejercicios 1 y 3 |
| `ensamblado/cap5/templates_12.html` | M12 en pasado |
| `ensamblado/cap5/chapter.js` | lecturas de `sobrediferenciacion-estacional`, `airline-pesos` y `calendario-regresores`; quiz ítems 6 (opción 3) y 8 (retro de la opción 3). Se retiró `varianzaDe()`, que ya no usaba nadie. **`simulacro.js` no se tocó** |
| `ensamblado/ensambla_cap5.py` | **solo** el texto de las etapas 2, 3 y 5 del ciclo (`ETAPAS_CICLO`), que vive en el ensamblador y no en `cap5/`: sin él, el hallazgo de la varianza seguía en el M4 |
| `Htmls_Series/capitulo-5-sarima.html` | reensamblado; reproducible byte a byte (md5 de dos ensamblados seguidos idéntico) |
| `Htmls_Series/capitulo-6-pronostico-evaluacion.html` | **sin cambios**: `ensambla_cap6.py` lo reescribe idéntico a HEAD |
| `precalculo/genera_cap5.R` → `salidas/cap5_sarima.json`, `cap5_datos.js` | guarda contra tildes rotas; modelo `con_pascua`; `a_menos_1_en_ee` en la sobrediferenciación; `armonica_K_sin_fuga`. El resto, idéntico campo a campo (`comprobaciones/r1_compara_json.out`) |
| `Htmls_Series/diapositivas/fuentes/capitulo_5.md`, `diapositivas/capitulo-5-sarima.html` | 13 diapositivas (las cuatro pedidas y las que repetían lo mismo); reconstruido con `construir.py` |
| `Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap5.py`, `verificacion_cifras_cap5.md` | una clave re-anclada por título, claims nuevos y retirados, claims «capítulo» al texto nuevo; observaciones al día; el informe, regenerado |
| `diagnostico/cap5/comprobaciones/r1_*` | guiones y salidas de esta ronda |
| `diagnostico/cap5/capturas/r1/` | capturas del capítulo y 84 del deck (ignoradas por git) |

`genera_soluciones.R` no se tocó (no hizo falta: los ejercicios del 5 no leen de él).

**Verificadores al cerrar**

- `python3 precalculo/verifica_todo.py` → 11 verificadores en verde (`r1_verifica_todo.out`).
- `verifica_bloques_cap6.py --html …capitulo-5…` → **1335 de 1335 cifras, 0 bloques con discrepancias** (antes 1199 de
  1212). Los bloques de la TRM leyeron la copia de GitHub Pages (el verificador corre en `/tmp`). El «write failed» de R de
  la línea base ya no aparece. `r1_verifica_bloques.out`.
- Los 13 bloques de Python, cada uno solo en una carpeta vacía y **sin silenciar avisos en el arnés**
  (`r1_bloques_python.py`, adaptado del cap. 4): todos terminan con código 0 y **ningún `ConvergenceWarning`**; el de la
  TRM, dos veces (copia de la página del curso y de la carpeta de trabajo), con la misma salida. Quedan avisos
  `RuntimeWarning` de numpy (`matmul`) en los dos bloques del M2, que no filtran nada, y el `InterpolationWarning` de KPSS
  del M3 (ya estaba). Las cifras de comentarios que no salen del bloque son las de R citadas a propósito en líneas `#`
  (no `#>`). `r1_bloques_python.out`.
- Diapositivas: `verifica_cifras_cap5.py` → 774 claims, 774 verificados (62 definiciones o convenciones), 5 marcados
  [SIN VERIFICAR] (los de antes), 0 que no coinciden, «todo verificado y cubierto»; los 4 bloques de R proyectados,
  2/2, 4/4, 4/4, 2/2. `revisar.py` → 84 diapositivas, todas a escala ≥ 88 % (`r1_revisar_deck.out`). Los avisos de
  `construir.py` son los mismos que da la fuente de HEAD (la diapositiva de $m$ grande pasa de 100 a 103 palabras).
  `verifica_directo_cap5.R`, `verifica_python_cap5.py` y `verifica_docs_cap5.R` no se ejecutaron: los claims nuevos salen
  de J (regenerado), de los coeficientes sin redondear que ya guardaba `directo_cap5.json` o del texto del capítulo.
- `audita_posicion_correcta.py` en verde (ninguna opción correcta cambió de sitio).
- `sin_literales_diagnostico.py` → 0 coincidencias.
- Por HTTP (servidor propio en 8765 y Chrome sin ventana en 9278, cerrados al acabar; `r1_revisa.js`, adaptado del cap. 4):
  los doce módulos a 1200 y 375 px con derivaciones, pistas y soluciones abiertas: 0 errores ni avisos de consola, 0
  `.katex-error`, 0 `$` sin renderizar, ningún KaTeX dentro de `<pre>`, sin desbordamiento horizontal, todos los lienzos
  con su gráfico. Lecturas: `sobrediferenciacion-estacional` D = 0 y 1 «Θ̂ lejos de −1» (28.53 y 6.06 e.e.), D = 2 el
  aviso (0.03 e.e.); `airline-pesos` salto 0.4400 en el estado inicial (θ = −0.40, Θ = −0.56), 1.0000 con Θ = 0 y 0.0500
  con Θ = −0.95; `calendario-regresores` con solo Semana Santa lee «airline + Semana Santa», AICc −487.2305. 41 capturas
  en `capturas/r1/` (las de los elementos largos se recortan bajo la cabecera fija; a 375 px no se capturan las soluciones
  ni el M11 entero, demasiado altos para el volcado de Chrome). `r1_revisa.out`.

**Entorno:** R 4.6.0, forecast 9.0.2; Python 3.10 (mambaforge), statsmodels 0.14.6, numpy 2.2.6; Node.

**Guiones** (`diagnostico/cap5/comprobaciones/`)

| guion | salida | qué comprueba |
|---|---|---|
| `r1_comprobaciones.R` | `r1_comprobaciones.out` | $\psi_j$ y $\sigma_h/\sigma$ del *airline* frente a $\sqrt h$ hasta $h = 240$; el salto $\psi_{12}-\psi_{11} = 1+\Theta$; MA(7)×SMA(1) con $m = 12$ (varianza factoriza, $\rho_5$ no); $D = 0,1,2$ con la distancia de $\hat\Theta$ a $-1$ y $|\hat\Theta|^{1/12}$; $\rho_{11}$, $\rho_{13}$ y el producto con siete decimales; residuales de arranque de R y Ljung–Box/Shapiro con y sin ellos; la fila $(0,1,0)(0,1,0)$; la salida real del M7; Semana Santa sola; el tope `floor(n/3/m)` en el código de `auto.arima`; AIC y AICc de `stlm`; el $K$ de la armónica con y sin la prueba; las evidencias del E1 sin varianzas; parámetros de la armónica con $K = 5$ y $6$ |
| `r1_compara_json.py` | `r1_compara_json.out` | `cap5_sarima.json` y `cap5_datos.js` regenerados frente a HEAD, hoja a hoja |
| — | `r1_genera_cap5.out` | la regeneración |
| `r1_bloques_python.py` | `r1_bloques_python.out` | los 13 bloques de Python, cada uno solo |
| — | `r1_verifica_bloques.out`, `r1_verifica_todo.out`, `r1_revisar_deck.out` | los verificadores al cerrar |
| `r1_revisa.js` | `r1_revisa.out` | la revisión por HTTP |

No se añadió ningún `<cite>`, `data-afirma`, autor, año ni página. Las remisiones nuevas («Capítulo 2 (Módulo 2.7)»,
«Capítulo 4», «Módulo 2», «Módulo 3») son internas. Se **quitó** una atribución falsa: «La regla de la varianza mínima —del
Capítulo 4—».

Líneas: «orig.» son las de `f807b40` (las del informe del par); «ahora», las del HTML ensamblado tras la ronda.

---

## T1.1 · Los errores de §1

| # | módulo | orig. → ahora | qué decía | qué dice ahora | evidencia |
|---|---|---|---|---|---|
| 1 | M5 | 4590–4593 → 4608–4612, 4649–4658 y bloque nuevo 4661 | el *airline* «acumula incertidumbre más despacio que una sola caminata… el mismo mecanismo que el $\psi_\infty = 0.169$ del Nilo» | La derivación se queda en lo cierto: $\sigma_{12}/\sigma_1 = 2.22$ frente a $3.46$, «en el primer año». Párrafo nuevo, fuera del plegado: la raíz unitaria en $B = 1$ es **doble**, los $\psi_j$ suben $(1+\theta)(1+\Theta) = 0.265$ al año sin límite ($\psi_{240} = 6.08$), la varianza crece como $h^3$ y **desde $h = 42$** el *airline* acumula más que una caminata con la misma $\sigma$ ($53.98\,\sigma$ frente a $15.49\,\sigma$ a veinte años); el Nilo, con raíz simple, es el contraste. **Remisión al M2** en una frase (la suma de $\psi_j^2$ que allí se lleva al infinito no converge con $y_t$; por eso los momentos son de $w_t$); la subsección del M2 no se movió ni se plegó. Bloque R/Python nuevo que imprime todas esas cifras | `r1_comprobaciones.out` § E1; el bloque (R y Python, 42 y 53.980/53.981) |
| 2 | M5 | intro del `airline-pesos` | con $\Theta \to 0$ «el escalón del rezago 12 desaparece» | «El salto… vale exactamente $\psi_{12}-\psi_{11} = 1+\Theta$. Lleva $\Theta$ a $0$ y el escalón vale $1$… Llévalo hacia $-1$ y el escalón casi desaparece». La lectura del simulador gana «salto ψ₁₂ − ψ₁₁ = 1+Θ». La intro no describe ningún estado inicial | `r1_comprobaciones.out` § E2 (1.0000, 0.4431, 0.0500, 0.0100); `r1_revisa.out` (Θ = 0 → 1.0000; Θ = −0.95 → 0.0500) |
| 3 | M3, ciclo del M4, M7, resumen, E1 | 4067, 4404, 4408, 4829, 5926 → 4083, ciclo, 4967, 6052, 6093 | «La regla de la varianza mínima —del Capítulo 4— señala $d=1, D=1$»; «la varianza de las cuatro combinaciones» como herramienta y «si la varianza sube al diferenciar, también [sobra]» como señal; «Comprobación: Varianza mínima… Coherente»; la pista del E1 manda a calcular las cuatro varianzas «antes de mirar ninguna prueba» | **M3**: la columna de la varianza «describe… pero no decide $d$ ni $D$», con la razón del Capítulo 2 (Módulo 2.7) —el cociente se acerca a $2(1-\hat\rho_1)$ y, por la misma cuenta, el de $\nabla_{12}$ a $2(1-\hat\rho_{12})$— y «por eso el Capítulo 4 no la cuenta como evidencia»; lo que decide son la ACF y las pruebas. La tabla de las cuatro combinaciones se queda. **Ciclo** (etapa 3): herramientas `ndiffs(diff(y, lag = m))`, KPSS o ADF sobre la serie ya diferenciada estacionalmente y su ACF; vuelta: «$\hat\theta$ pegado a $-1$… La varianza de las cuatro combinaciones no sirve de señal: repite lo que dice la ACF»; etapas 2 y 5, con $\hat\Theta$/$\hat\theta$ pegados a $-1$. **M7**: la fila pasa a «Señal de vuelta (etapa 5): $\hat\Theta = -0.5569$ (e.e. $0.0731$) y $\hat\theta = -0.4018$ (e.e. $0.0896$), lejos de $-1$ · No sobra ninguna diferencia». **Resumen**: «$\hat\Theta$ (o $\hat\theta$) pegado a $-1$, indistinguible de $-1$ con su error estándar; la varianza no decide». **E1**: pista con el orden del M3 y la señal de $-1$; en la solución, la línea de las varianzas («mínimo en (d=1, D=1)») se sustituye por la ACF de `diff(co2)` en 12, 24, 36 ($0.9219$, $0.8902$, $0.8686$, banda $0.0907$) y se añade la señal de vuelta ($\hat\theta = -0.3501$, $\hat\Theta = -0.8506$, a $13.09$ y $5.82$ e.e. de $-1$). El simulador `sobrediferenciacion-estacional` deja de mostrar la varianza. Títulos de módulo sin cambios. Quedan, porque no son la regla: la tabla descriptiva del M3 y su simulador `cuatro-combinaciones`, y las frases «la varianza estacional tapa la tendencia» (M3, M8, E2, quiz 4), que explican por qué `ndiffs()` falla sobre la serie cruda | cap. 2 `c2-m7-08`; cap. 4 M3 y M8; `r1_comprobaciones.out` § Ejercicio 1; bloque del E1 |
| 4 | M3, M4, M7 | 4085–4107, 4394, 5885, 4900–4904 → 4110–4136, ciclo, 5038 | $\lvert\text{raíz MA}\rvert^{-1}$ cerca de 1 como firma; umbral 0.99 en el simulador sin decirlo; el M7 matizaba al M3 | **M3**: intro del simulador y tabla en la escala de $\Theta$: columnas $D$, $n$, $\hat\Theta$, e.e. y «Distancia a $-1$, en e.e.» ($28.53$, $6.06$, $\mathbf{0.03}$); el párrafo explica que $\lvert\text{raíz}\rvert^{-1} = \lvert\hat\Theta\rvert^{1/12}$ se acerca a $1$ con casi cualquier $\Theta$ ($0.9524$ con $D = 1$, $0.9752$ con $D = 0$, del bloque). **Simulador**: el umbral ahora es la escala de $\Theta$ y se dice en la intro —aviso cuando $-1$ cae dentro de $\hat\Theta \pm 1.96$ e.e.—; lee `a_menos_1_en_ee`, que calcula el generador. **M7**: el párrafo deja de matizar («se lee en $\hat\Theta$… a $6.06$ errores estándar de $-1$… con la diferencia de más del Módulo 3 quedaba a $0.03$… $0.9524 = \lvert\hat\Theta\rvert^{1/12}$ no sirve para esto, por la razón que da el Módulo 3»); sale el ejemplo $\Theta = 0.1 \to 0.825$. El bloque R del M3 imprime las dos escalas | `r1_comprobaciones.out` § M3; JSON `sobrediferenciacion_estacional[*].a_menos_1_en_ee`; `r1_revisa.out` (D = 0, 1: «lejos de −1»; D = 2: aviso) |
| 5 | E3(b) | 6084 y ss. → 6261, 6340–6352 | solución: el error es responder «el armónico, por dos puntos» | Respuesta: «El *airline*, pero no por el AICc: esos dos AICc no son comparables. Lo que lo decide es el diagnóstico: el mejor armónico por AICc no pasa Ljung–Box y el *airline* sí». La discusión dice que la lectura ingenua elige aquí el *airline* por casualidad y que lo legítimo entre familias es Ljung–Box ($K = 4$: $p = 0.0439$; *airline*: $p = 0.4081$). El bloque ya no escribe `180.200` y `467` a mano: guarda los seis ajustes y los lee; e imprime los dos Ljung–Box. El enunciado no cambia (sigue siendo cierto: 1.991 puntos); la pista añade «busca un criterio que no dependa de él». En el E1, la frase que remitía al E3 («ahí la lectura ingenua sí engaña») pasa a «allí la comparación tampoco vale, aunque el menor señale el mismo modelo que el diagnóstico» | `maestra_diagnostico.out` bloque 3; `r1_comprobaciones.out` § E1; bloque del E3 |
| 6 | M6 | 4693 → 4814 | «en el Capítulo 3 los dos criterios discrepaban sobre las manchas solares» | «que no siempre pasa: el BIC castiga más cada parámetro y puede quedarse con un modelo más pequeño que el AICc». No se inventa ningún ejemplo del cap. 3 | cap. 3, l. 5731 y 6011 |
| 7a | M1 | 3109–3110 → 3110 | «la ACF se queda con dos barras, en los rezagos 1 y 12» | «quedan dos barras grandes, en los rezagos $1$ y $12$, y unas pocas menores sin patrón, que el Módulo 7 discute» | par § M1 (1, 3, 9, 12, 23 y 32) |
| 7b | M1 | 3080 | «Al final del Módulo 5 el modelo *airline*… deja $\hat\rho_{12} = -0.0515$ y pasa Ljung–Box(24) con $p = 0.233$» | «En el Módulo 6…» (la tabla de la rejilla da las dos cifras) | lector §1 |
| 7c | M7 | 4996–4997 | `#> -0.401800 -0.556900  0.001371 -483.2101` | la salida real, `-0.401828   -0.556945    0.001371 -483.210085` | `r1_comprobaciones.out` § M7; verificador |
| 7d | M9 | simulador `calendario-regresores` | con solo «Semana Santa» mostraba AICc, BIC, mejora y coeficientes del modelo con días **y** Pascua | lee su propio ajuste, `con_pascua`, que ahora calcula el generador: AICc $-487.2305$, BIC $-476.0471$, $\hat\beta = 0.0298$ (e.e. $0.0116$). La intro dice «cada combinación está ajustada en R» y «todos los modelos comparten $d=1$ y $D=1$». La tabla del M9 no cambia (sigue con los tres modelos que discute) | `r1_genera_cap5.out`; `r1_comprobaciones.out` § M9; `r1_revisa.out` |

## T1.2 · Imprecisiones, menores y dudosos del par

| par | módulo | antes | después | evidencia |
|---|---|---|---|---|
| imprecisión | M2 | «si $q < m$ … se factoriza exactamente, y con ella toda la ACF» | la varianza con $q < m$; la ACF con $2q < m$; frase nueva con el porqué ($q = 7$, $m = 12$: el rezago 5 se alcanza como $5 + 0\cdot12$ y $-7 + 1\cdot12$) y «el *airline*, con $q = 1$, cumple las dos condiciones de sobra». Sin cifras nuevas en prosa | `r1_comprobaciones.out` § M2 (γ₀ 3.74 = 3.74; ρ₅ 0.4439 frente a 0.3636) |
| imprecisión | M6 Py | «R da 0.2330. La diferencia son los primeros residuales, que statsmodels produce…» | «R da 0.2330 con sus 144 residuales y 0.3515 sin los 13 primeros. Ninguno de los dos programas da innovaciones en el arranque…»; el bloque R imprime ahora el $0.3515$ con un comentario. Las cifras de la tabla y del quiz (0.2330, 0.1674, 0.2969) se dejan: ninguna conclusión cambia | `r1_comprobaciones.out` § M6 (desv. 0.0049 frente a 0.0368; LB24 0.2330/0.3515; LB36 0.2969/0.4616; Shapiro 0.1674/0.6043) |
| imprecisión | M6/M7 Py (D11) | `warnings.filterwarnings("ignore")` y un ajuste que no converge (−0.4019, −0.5571; 400.62, 689.21) | `method="bfgs", maxiter=1000`, `mle_retvals["converged"]` impreso (`True`), solo se silencian los `RuntimeWarning` de numpy; salidas reales: −0.4018/−0.5569 con y sin `simple_differencing`; 525.46 [400.59, 689.25]; la caja de aviso dice «coinciden con los de R en las cuatro primeras cifras» (antes «diferencia $6\times10^{-5}$»). Lo mismo en los dos bloques del M2 (que tampoco convergían con `simple_differencing=True`) y en el del M5 nuevo | `r1_bloques_python.out` |
| imprecisión | M9 | «en `statsmodels`… cuando $d > 0$ diferencia también los regresores» (como si R no lo hiciera); Python: SE «un 9 % y un 19 % menores… porque las dos implementaciones no tratan igual la diferenciación» | definición: «ajusta este mismo modelo, igual que `Arima(…, xreg = )` en R; con $d$ o $D$ mayores que $0$, los dos diferencian a la vez la serie y los regresores». Bloque: BFGS (llega a $1.0844$; el optimizador por defecto se paraba en $1.0764$), y la diferencia de SE se atribuye a `cov_type="opg"` frente a la hessiana; con `cov_type="approx"` imprime $0.4462$ y $0.0111$, **los de R**, y $t$ contra $\beta = 1$ $0.1892$ (R $0.1882$) | `r1_bloques_python.out`; exploración en el bloque |
| imprecisión | M10 | ARIMA$(0,0,0)(0,1,0)_{365}$ atribuido a $m = 365$ | «con una serie de frecuencia $365$ de poco más de dos años ($n = 800$)… No es que los descarte: ni los prueba, porque su código limita $P$ y $Q$ a $\lfloor n/(3m)\rfloor$, que aquí vale $0$. Haría falta… $n \ge 3m = 1095$». El bloque R imprime `floor(length(z) / (3 * 365))` → 0 | `r1_comprobaciones.out` § M10 (líneas `max.P <- min(max.P, floor(serieslength/3/m))` del código de `auto.arima`) |
| imprecisión | M1 (Altas de gráficas) | «dos barras» | véase 7a | |
| menor | M4 | «ninguno coincide con el producto» | «no pueden ser los dos iguales al producto $\rho_1\rho_{12} = 0.4218029$: el $\rho_{13}$ ($0.4218011$) se le queda a dos millonésimas, y el $\rho_{11}$ se aparta en la tercera cifra»; el bloque R lo imprime | `r1_comprobaciones.out` § M4 |
| menor | M4 | `#> [1] 0.0000 0.0000 0.7000 0.0000 0.4900` (R imprime un vector con nombres) | `acf_sarima()` devuelve `unname(...)` y el `#>` es la salida real, `[1] 0.00 0.00 0.70 0.00 0.49`; numpy, `[0.   0.   0.7  0.   0.49]` | verificador |
| menor | M5/M7 | prosa $1.0412$/$0.8632$, bloque del M7 $1.0413$/$0.8633` | el bloque del M7 usa `th`, `TH` sin redondear: `1.0412 0.8632` y $\sigma_h$ `0.037031 0.082270 0.139621` (la prosa, a cuatro cifras, no cambia) | verificador |
| menor | M10 | «los términos son tantos como meses» | «el seno de frecuencia $m/2$ vale cero en todos los periodos, quedan $m-1$ términos» | par |
| menor | M10 Py | `-414.34` | `-414.35` (salida real); además `maxiter=2000` y una columna `conv` (`True` en los seis; con 50 iteraciones, tres no convergían) y el STL igual (`True -643.05`) | `r1_bloques_python.out` |
| menor | M10 Py | «R da −542.95» junto al AIC | «el ARIMA de `stlm()` en R da un AIC de −543.24 (−542.95 es su AICc)»; el bloque R imprime los dos | `r1_comprobaciones.out` § M10 |
| menor | M11 | $K$ de la armónica elegido con la prueba dentro | salvedad tras la presentación de la tabla: con solo el entrenamiento el AICc elige $K = 5$, con RMSE $19.58$ en vez de $19.51$; «no cambia el orden de la tabla». Cifras del generador (`armonica_K_sin_fuga`). No se recalculó la tabla | `r1_genera_cap5.out` |
| menor | quiz 6 | opción 3: «$2$ parámetros frente a $16$» (los de $K = 6$) | «frente a $15$» ($K = 5$, el del AICc $-521.2$ del enunciado). Misma posición | `r1_comprobaciones.out` § Quiz 6 |
| menor | M9 simulador | véase 7d | | |
| dudoso | M8 | arbitraje sobre un promedio mensual | «La TRM sale de un precio de mercado… lo que se espera de un precio en un mercado razonablemente eficiente, con un matiz: aquí se modela el promedio mensual, que no es exactamente el precio con que se negocia» (como en el cap. 4) | — |
| dudoso | quiz 8 | retro de la opción 3: «eso es varianza, no sesgo» | «el sesgo que el Módulo 11 mide en esos $24$ meses es del tramo, no de la especificación» | — |

Además:

- **Falsos positivos del verificador.** El `0.463` del M3 (valor crítico en una línea `#>`) pasa a su propia línea de
  comentario, como hizo el cap. 4: una línea `#>` solo trae lo que imprime el bloque. El `0.1882` del M9 ya está en una línea
  `#`. No se tocó ningún otro para contentar al verificador.
- **$t$ del ajuste forzado de la TRM**: la tabla del M8 decía $t = 0.01$ y el bloque (en vivo) $0.0147$; con la copia fija R
  imprime $0.0146$, y la tabla dice ahora $0.0146$.
- El M1 y el M4 de Python tenían `#>` con otro espaciado que la salida real; se igualaron.

## T1.2 · Cifras de la prosa sin bloque ni generador

Con bloque o generador desde esta ronda: $\gamma_0/\sigma^2 = 1.5217$, $2.300$/$1.700$ y la tabla de $\phi$ (bloque del M2);
los $\psi$, $\sigma_h$, $0.265$, $42$, $53.98$, $15.49$ y $\psi_{240}$ (bloque del M5); la fila $(0,1,0)(0,1,0)$
($-434.8$, LB $2.31\times10^{-8}$; bloque del M6); $\rho_{11}$/$\rho_{13}$/producto (M4); las distancias a $-1$ (M3,
bloque y JSON); el AIC/AICc de `stlm` y el tope de $P$, $Q$ (M10); Semana Santa sola y la salvedad del $K$ (JSON); los
Ljung–Box del E3 y la señal de vuelta del E1 (bloques).

Quedan para la R3 (D6/D7), sin bloque propio: el ARIMA(0,1,5) del cap. 4 en el M1 ($0.7245$, $0.6727$) y el $Q = 222.4$ del
M7; el rango relativo $1.848$ del M7; $\sigma_{12}/\sigma_1 = 2.22$ frente a $3.46$ en la derivación del M5 (sale del
bloque nuevo como cociente, no impreso); las cifras de la discusión del M11 (49 orígenes, $26.00$…, sesgo $39.45$) y lo que
solo está en el JSON (tablas del M1, M4, M9, M11).

## T1.3 · TRM congelada (D2), acentos y M12 en pasado

- **TRM**: los cuatro bloques (M1 R; M8 R y Python; E3 R) leen `trm_mensual_2015-01_2026-06.csv` de la carpeta de trabajo
  o, si no está, de `https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/`, con el comentario del cap. 4. La
  prosa del M8 dice de dónde salen los datos y que los bloques no los descargan. `#>` ajustados a la copia: $\hat\rho_{12}$
  de $\nabla$TRM `-0.0025` (antes `-0.0024`, y se retira el comentario del «cuarto decimal que baila») y $t$ `0.0146`.
- **Acentos**: el JSON y el `.js` de julio traían «aerol\<c3\>\<ad\>neas», «Concentraci\<c3\>\<b3\>n» y «v\<c3\>\<ad\>a»
  (dos). Con R 4.6.0 la configuración regional que fuerza el generador ya funciona y la regeneración los escribe bien; el
  arreglo en el generador es una **guarda** (`sin_tildes_rotas()`): si alguna cadena sale con bytes literales, aborta antes
  de escribir, y vuelve a comprobar el `.js` escrito. Al regenerar, la `fuente` de la TRM toma la fecha de consulta de
  `datos_series.json` (2026-07-26; antes 2026-07-24, con los mismos 138 valores).
- **Regeneración**: `cap5_sarima.json` y `DATOS_CAP5` ganan 29 hojas (`con_pascua`, `a_menos_1_en_ee`,
  `armonica_K_sin_fuga`); las 9026 de antes son idénticas salvo `generado` y esa `fuente`; `SERIES_CAP5`, idéntico salvo
  las tres cadenas con tilde. Ninguna cifra existente cambió con R 4.6.0 / forecast 9.0.2.
- **M12**: «se presentó… el miércoles 11 de noviembre, y duró», «Tuvo doce preguntas», «seguían», «eran», «pedían… se
  tecleaba», «recibió», «no se usó en Brightspace, y sigue sirviendo de ensayo», «En el quiz de Brightspace se veía…». Título
  sin cambios; el simulacro, intacto.

## Diapositivas del cap. 5

| diapositiva (título) | antes | después |
|---|---|---|
| «Cuatro filas se parecen…» (notas) | el código «descarga la serie en vivo, imprime −0.0024» | lee la copia fija e imprime −0.0025, como la tabla del M8 |
| «Ver y medir la estacionalidad…» (notas) | la TRM «descarga la serie de datos.gov.co» | «lee la copia fija» |
| «Cada operador hace su trabajo…» | «Las dos: varianza mínima, 0.002102»; notas: «La regla de la varianza del capítulo 4 acierta aquí» | «La varianza de cada combinación describe; no decide D ni d»; notas con la razón del cap. 2 y del 4 |
| «Diferenciar de más deja la firma… Θ̂ se acerca a −1» (título igual) | columna Varianza; «la raíz MA cae sobre el círculo… la regla de la varianza falla» | columna «Distancia a −1, en e. e.» (28.53, 6.06, **0.03**); «la alarma se lee en la escala de Θ, no en la varianza»; notas: el aviso del simulador y por qué no sirve el módulo de las raíces |
| «El protocolo tiene cinco etapas…» | «raíz sobre el círculo → 2 o 3» | «Θ̂ o θ̂ pegados a −1 → 2 o 3» |
| «Los pesos ψ suben en escalones…» (notas) | el M7 imprime 1.0413 y 0.8633 | los bloques del M5 y del M7 imprimen 1.0412 y 0.8632 |
| **título nuevo**: «Frente a una caminata, menos incertidumbre a corto plazo y más a largo plazo» (antes «El *airline* acumula incertidumbre más despacio que una sola caminata aleatoria») | «los dos MA… amortiguan»; «Con Θ→0, el escalón del 12 desaparece»; notas: «el mismo mecanismo que el ψ∞ = 0.169 del Nilo» | 2.22/3.46 «el primer año»; raíz doble, 0.265 al año, desde h = 42, 53.98σ frente a 15.49σ; «El salto en el rezago 12 vale 1 + Θ: 1 con Θ = 0; casi nada con Θ → −1»; notas con el contraste del Nilo y la remisión al M2. Clave del verificador re-anclada |
| «Lo que se llevan de la clase 1» | «Θ̂→−1 y la raíz sobre el círculo» | «Θ̂ pegado a −1, a la vista de su error estándar; la varianza no decide» |
| «En la rejilla de 36 modelos…» (notas) | manchas solares | el BIC castiga más cada parámetro |
| «statsmodels no diferencia la serie…» (notas) | «difieren en 6×10⁻⁵; con 0.14.6, 2.4×10⁻⁴» | sin la opción y con L-BFGS no converge (2.4×10⁻⁴); con BFGS coincide en cuatro cifras |
| «Etapas 1 a 3…» | fila «Comprobación · Varianza 0.002102… · Coherente» | «Señal de vuelta (etapa 5) · Θ̂ = −0.5569 (e. e. 0.0731) y θ̂ = −0.4018, lejos de −1 · No sobra ninguna diferencia» |
| «Etapa 5…» (notas) | 0.9524 explicado con Θ = 0.1 → 0.825 | Θ̂ a 6.06 e. e. de −1 (D = 2: 0.03); 0.9524 no sirve (Módulo 3) |
| «La TRM es mensual…» | $t = 0.01$; arbitraje sin matiz | $t = 0.015$ (J; el capítulo imprime 0.0146); «La TRM mensual es un promedio, no el precio con que se negocia, pero hereda esa falta de patrón» |
| «SARIMAX es una regresión…» | «con d > 0 diferencia también los regresores» | «igual que `Arima(…, xreg = )` en R: con d o D > 0, los dos diferencian la serie y los regresores» |
| «Con m grande el SARIMA falla…» | — | «no prueba ningún Φ ni Θ: los limita a ⌊n/(3m)⌋ = 0» |

Claims (`verifica_cifras_cap5.py`): retirados los de la varianza en «Cada operador», «Diferenciar de más» y «Etapas 1 a
3», los de 1.0413/0.8633 y los de 0.825/0.1/−0.557/0.073; nuevos: las tres distancias a −1 (J), 0.265 (CALC), 42 y 53.98
(CALC con los coeficientes sin redondear de `directo_cap5.json`, función `SIGMA_AIR`), 15.49 (√240), 240 (parámetro),
6.06 y 0.03 en «Etapa 5», −0.5569/0.0731/−0.4018 en «Etapas 1 a 3», 0.015 (J) y 1.96. Las de tipo «capítulo» exigen
ahora el texto nuevo (la salida `[1] -0.0025 -0.0672 0.0714`, «Distancia a $-1$, en e.e.», «Señal de vuelta (etapa 5)» y
que «Varianza mínima en» ya no esté, «$0.9524 = |\hat\Theta|^{1/12}$», «a $6.06$ errores estándar», «$t = 0.0146$», las
cuatro cifras del largo plazo, la salida `1.0412 0.8632` del M7 y que `1.0413` ya no esté). Ningún claim se relajó con
`permite` (el único `permite` tocado solo cambia su motivo). Al reconstruir, el HTML del deck recoge también los cambios de
plantilla que la skill ha tenido desde la publicación (CSS de los temas; la fuente de HEAD, reconstruida, da los mismos).

## Lo que no se hizo, y por qué

- **El simulacro** (`simulacro.js`) no se tocó. Para el banco: la pregunta 1 usa la varianza junto con $\hat\rho_1$ y
  $\hat\rho_{12}$ (no como regla), la ruta «las noches» de la 2 y el «2.4 veces» de la 9 (par).
- **Las cifras del diagnóstico del airline** (0.2330, 0.1674, 0.2969, banda ±0.163) siguen calculándose con los 144
  residuales de R, incluidos los 13 de arranque: cambiarlas mueve la tabla del M6, el M7, el M1, el quiz y el simulacro, y
  ninguna conclusión cambia. Se dice en el bloque del M6 y queda anotado.
- **La tabla del M11 con $K = 5$** no se recalculó: se dice la fuga y su tamaño (generador).
- **El bloque del M8 en Python** quedaba con `filterwarnings("ignore")`; lo corrigió la sesión maestra (abajo).
- **Remisiones y estados iniciales de la R3**: la remisión del M11 al «código del capítulo» (D7), el `biasadj` que el cap. 6
  busca en el 5 (D6) y las intros del M4 (`firma-teorica`, «Empieza con todo en cero») y del M7, que describen un estado que
  no es el inicial. La intro del `airline-pesos`, la que tocaba aquí, ya no describe ningún estado.
- **La historia de `nsdiffs()`** («antes OCSB») y el resto de atribuciones: R4.
- La M7 sigue diciendo «la etapa 5 lo comprueba» y los «Para practicar» no existen: R3 y R5.

## Correcciones de la sesión maestra, tras los verificadores

Dos verificadores independientes: A, el contenido del capítulo (`R1_verificacion_A.md`: 2 imprecisiones, 12 menores);
B, el deck, el generador, la reproducibilidad y el aspecto (`R1_verificacion_B.md`: 1 imprecisión, 6 menores). Ningún
error. Las correcciones están en `comprobaciones/r1_ediciones_maestra.py` (32 ediciones, idempotente) y la columna «Lo que
hizo la sesión maestra» de los dos informes dice qué se hizo con cada hallazgo. Lo que pesa:

- **El criterio del error estándar es una señal, no un veredicto** (A1). Re-medido (`r1_maestra.R`): con
  SARIMA(0,1,1)(0,1,1)₁₂, $n = 144$ y $\Theta = -0.85$, sin ninguna diferencia de más, $-1$ cae dentro de
  $\hat\Theta \pm 1.96$ e.e. en 137 de 200 series (el verificador A, con otra semilla, 211 de 300). La lectura del simulador
  dice «señal de que puede sobrar una diferencia estacional; vuelve a mirar D», y con $D = 0$, «no sobra nada, pero falta
  ∇₁₂». Igual la intro, el párrafo de la tabla del M3, las etapas 2 y 3 del ciclo, el resumen y el deck.
- **E3(b)** (A2): el diagnóstico inclina sin cerrar. Los armónicos quedan en el borde de Ljung–Box (0.0439, 0.0516,
  0.0515), el p-valor no ordena modelos y la decisión firme es fuera de muestra.
- **SARIMAX** (B1): es el mismo modelo que `Arima(…, xreg = )`, que equivale a diferenciar la serie y los regresores.
  statsmodels solo lo hace así con `simple_differencing=True`. Corregido en el M9 y en la diapositiva 64, sin contradecir
  al M6 ni a la diapositiva 49.
- **El bloque del M8 en Python** (A10) ya no silencia los avisos de convergencia e imprime `True True`.
- **`verifica_bloques_cap6.py`** (B6) usa un dispositivo gráfico nulo en R y sale con 1 si una sesión termina con
  código ≠ 0. Se volvió a pasar sobre los caps. 3 a 6 (`r1_maestra_bloques_verificador.out`).
- **El rediseño del deck** (B4) viene de la skill (cambiada el 14 nov). El deck del cap. 4, publicado el 22 nov, ya se
  construyó con ella. Queda como observación la fuente a 12.5 px en el pie.

**Para el banco** (no se toca `simulacro.js`): las retros de la pregunta de la tabla de diferencias usan la varianza como
evidencia, la de la correcta incluida (A13). Se suma a los tres hallazgos del simulacro de arriba.
**Para la R4:** la prosa del M8 atribuye la serie a la Superintendencia Financiera y a datos.gov.co, una fuente de datos
sin alta (A14).

**Verificadores tras las correcciones:**
- Reensamblado reproducible: md5 `95c95ac2…` dos veces. El cap. 6 queda idéntico a `7686d33`.
- `verifica_bloques_cap6.py` da 1335/1335 (`r1_maestra_bloques.out`).
- Los 13 bloques de Python, cada uno solo, sin `ConvergenceWarning` (`r1_maestra_bloques_python.out`).
- `verifica_todo.py` da 11 en verde (`r1_maestra_verifica_todo.out`).
- `audita_posicion_correcta.py` en verde, y `sin_literales_diagnostico.py` da 0.
- Deck: `verifica_cifras_cap5.py` da 774/774 (`r1_maestra_deck.out`). `revisar.py` deja las 84 a ≥ 88 %
  (`r1_maestra_revisar_deck.out`).
- Por HTTP: `r1_revisa.js`, los 12 módulos a 1200 y 375 px, con 0 errores de consola, 0 `.katex-error` y 0 `$` sueltos,
  sin desbordamiento, y las tres lecturas nuevas del simulador del M3 (`r1_maestra_revisa.out`).
- Con el verificador de bloques arreglado, los caps. 3, 4 y 5 dan 1084/1084, 1348/1348 y 1335/1335, con código 0. El
  cap. 6 da 415/434 y código 1, lo mismo que con el verificador de `7686d33`
  (`r1_maestra_bloques_cap6_head.out`): es anterior a esta ronda y le toca a la R1 del cap. 6.
