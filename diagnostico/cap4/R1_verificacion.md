# Capítulo 4 · R1 (errores) · verificación independiente

2026-11-22. Verificador de contexto limpio, sin el registro del redactor (`R1_cambios.md`) ni sus salidas `r1_*`
hasta terminar la comprobación propia; después se cotejaron. Objeto: el diff sin commit contra `7e9bc58` en
`ensamblado/cap4/`, `precalculo/genera_cap4.R` y sus salidas, y las diapositivas del cap. 4.

**Entorno:** R 4.6.0 · forecast 9.0.2 · tseries 0.10.62 | Python 3.10 (mambaforge) · statsmodels 0.14.6 · numpy 2.2.6 ·
scipy 1.15.3 (`MPLBACKEND=Agg`). Servidor propio en 8764, cerrado al acabar.

**Guiones y salidas** (`diagnostico/cap4/comprobaciones/`):

| guion | salida | qué comprueba |
|---|---|---|
| `v1_comprobaciones.R` | `v1_comprobaciones.out` | cada cifra nueva o cambiada de la prosa y los bloques de R: 32.8; residual 1 y Ljung–Box de R con y sin él; cociente de varianzas, 2(1 − r₁) y r₁ de las diferencias (Nilo, BJsales, log(lynx)); ACF del Nilo, rezagos 1–20; Monte Carlo de PP/ADF con la semilla del generador y con otra; coeficientes con deriva y c; la media del ARIMA(1,0,1) con tres estimadores; el ARIMA(2,1,2) con CSS-ML, ML de `Arima()` y ML de `stats::arima`; σ̂² y el factor 99/97; la forma del ARIMA(1,1,1) sin constante y su límite, contra la fórmula paso a paso; la TRM desde la copia (cotas, asimetría, cobertura del 80 %, cuadrados medios); AIC de R |
| `v1_aic_r.out` | — | AIC y AICc de R con 12 cifras |
| `v1_python.py` | `v1_python.out` | statsmodels: coeficientes, Ljung–Box con y sin y₁, pronóstico; cociente y r₁; `f.aicc`, AIC, `nobs_effective` y el efecto de n; t del escalón; TRM desde la copia |
| `v1_trm_bloques.py` | `v1_trm_bloques.out` | los dos bloques de la TRM, extraídos del HTML y ejecutados en una carpeta vacía (leen de la página del curso) y con la copia en la carpeta |
| `v1_quiz_simulacro.py` | `v1_quiz_simulacro.out` | `SIMULACROS['cap4-simulacro']` (md5) y claves, posiciones y numéricas de `AUTOEVALUACIONES['cap4']` frente a `7e9bc58` |
| `v1_literales.py` | `v1_literales.out` | 7-gramas de las líneas añadidas en `bibliografia/_local/texto` y `web` |
| — | `v1_ensambla.out`, `v1_md5_antes.out`, `v1_md5_despues.out` | reensamblado 4 → 5 → 6 |
| — | `v1_verifica_todo.out`, `v1_verifica_bloques.out`, `v1_verifica_cifras_cap4.out`, `v1_cap6_cobertura.out` | verificadores del proyecto y el 89.6 % del cap. 6 |

## Resumen

**Los dos errores de la especificación quedaron corregidos y la corrección es verdad.** La forma del pronóstico del
ARIMA(1,1,1) sin constante (M9) se comprobó paso a paso: las diferencias pronosticadas por `forecast()` coinciden con
$\hat\phi^{h-1}(\hat\phi\nabla y_T+\hat\theta\hat\varepsilon_T)$ en los cinco primeros pasos, y el nivel converge al límite
de la fórmula (740 → 816.18 → 842.17). La varianza deja de decidir $d$ en todo el capítulo (M1, M2, M3, M4, M8, M10,
resumen, ejercicios 1 y 2) y en las diapositivas, con la misma razón que el cap. 2 (`c2-m7-08`); en el Nilo y en
log(lynx) los cocientes frente a 2(1 − r₁) se reproducen. Las 7 imprecisiones y los 7 menores del par están
atendidos y son correctos: σ̂² de `Arima()` es SCR/97 también con `method = "ML"` (no es CSS-ML frente a ML); el
ARIMA(2,1,2) da log L y raíces distintas con CSS-ML y ML, y el ML de `Arima()` es el mismo de `stats::arima` (el del
explorador); el AICc de statsmodels con `f.aicc` y la atribución a la log-verosimilitud son ciertos (n mueve 0.0026);
el 89.6 % del cap. 6 es la cobertura de 37 orígenes × 12 horizontes (444 errores); la deriva del ítem 4 del quiz es
$\mu_w$, no $c$. Las cifras que no tenían generador salen ahora de `genera_cap4.R` (100 % y 51.3 %, reproducidos con la
misma semilla; con la semilla 7, 100 % y 55.4 %) o de un bloque bajo `#>` (83.9 %, 0.76, 1.10/1.14/1.07).

**Pero la ronda introduce un problema nuevo con el capítulo 2**, del mismo tipo que el que corrigió: la tercera
«evidencia» para $d$ (el $\hat\rho_1$ de la serie diferenciada cerca de −0.5) se presenta sin la salvedad que el cap. 2
pone a ese mismo síntoma («es un indicio, no una regla, y falla en los dos sentidos»), y en el ejercicio 1 se usa en el
sentido en que falla: «r1 positivo: no sobra nada». El contraejemplo está en el propio capítulo: en log(lynx), donde
$d = 1$ sobra, el $\hat\rho_1$ de la diferencia es positivo (hallazgos 2 y 3). Además, el M11 afirma que el quiz de
Brightspace «ya se aplicó» y «duró 40 minutos», y no hay registro de que se aplicara (hallazgo 1).

**Reproducibilidad, sin problemas:** `verifica_todo.py` 11 en verde; verificador de bloques **760 de 760** (0
discrepancias); `ensambla_cap4.py` deja el HTML idéntico y `ensambla_cap5.py` y `ensambla_cap6.py` dejan los caps. 5 y 6
sin cambios (md5 antes = después, e iguales a `7e9bc58`); `cap4_arima.json` solo cambia en `generado`, la `nota` de
`metodos_estimacion` y la clave nueva `sim_raiz_unitaria`. Los bloques de la TRM dan la misma salida en carpeta vacía y
con el archivo, y cuadran con sus `#>`. `SIMULACROS['cap4-simulacro']` es byte a byte el de `7e9bc58`; las 25 marcas
`correcta` del quiz y sus dos claves numéricas, también. Diapositivas: `verifica_cifras_cap4.py` da 469 claims, 467
verificados, 2 `[SIN VERIFICAR]` (los de antes), 0 que no coinciden; reconstruir el deck con `construir.py` desde
`capitulo_4.md` da el HTML publicado salvo la ruta de los enlaces al capítulo (la de la carpeta de salida). Por HTTP,
los módulos 1–3, 5 y 7–12 sin `.katex-error` ni errores de consola; la lectura de `sobrediferenciacion` (d = 1) y la de
`forma-pronostico` dicen lo nuevo. Ningún 7-grama de las 387 líneas añadidas aparece en los 1634 archivos de
`bibliografia/_local/`.

## Hallazgos

Gravedad: **error** (enseña o afirma algo falso), **imprecisión** (cierto a medias o contradice otra parte), **menor**.
Líneas: las de la fuente en `ensamblado/cap4/` (o el archivo que se nombra).

| # | Gravedad | Dónde | Qué está mal | Evidencia | Corrección propuesta | Lo que hizo la sesión maestra |
|---|---|---|---|---|---|---|
| 1 | error | `templates_11.html` l. 15 y 22–29 (M11, objetivo y primer párrafo) | Afirma que el quiz del cap. 3 y los módulos 4.1–4.4 «ya se aplicó, se presentó en Brightspace, duró 40 minutos», que «fueron diez preguntas» y que «cada estudiante recibió una variante». No consta: el `LEEME.md` de `Quiz Cap3-Cap4 (20948)/` (última edición, 5 oct) dice «Nada de esta carpeta se ha importado todavía», deja la fecha y los 40 o 45 minutos como pendientes del profesor, y la nota del curso en el vault compone el Corte 2 con Parcial 2, Taller 2 y Quiz 2 (del banco del Taller 2), sin este quiz. Tampoco es coherente con el cap. 3, cuyo M11 sigue en presente («se presenta en Brightspace y dura 30 minutos») | `Quiz Cap3-Cap4 (20948)/LEEME.md` l. 8–9, 316–321; `Vault/Cursos/20948 Series de Tiempo.md` l. 85–91; `capitulo-3-modelos-ar-ma-arma.html` l. 7480–7490 | No afirmar que se aplicó: «Se escribió como ensayo de un quiz de Brightspace sobre el cap. 3 y los módulos 4.1–4.4 (diez preguntas, 40 minutos, calculadora y fórmulas, sin R) y sigue sirviendo de repaso». Confirmar con Javier si se aplicó; decidir a la vez el M11 del cap. 3 | |
| 2 | error | `templates_10.html` l. 712 (ej. 1, solución) y l. 692–693 (pista) | La solución concluye «con d = 1, r1 positivo: no sobra nada» y la pista manda a comprobar que con $d = 1$ el $\hat\rho_1$ de la diferencia queda «lejos de −0.5». Es una inferencia falsa: en log(lynx), donde el capítulo demuestra que $d = 1$ sobra (las tres pruebas y la raíz MA = 1), el $\hat\rho_1$ de la diferencia es **positivo** y lejos de −0.5. El cap. 2 lo dice expresamente: el síntoma «es un indicio, no una regla, y falla en los dos sentidos», con una serie estacionaria a la que la diferencia le sobra y $r_1 = -0.148$ | `v1_comprobaciones.out` § E2 (`r1 de diff(log lynx), d = 1 y 2: 0.5649 0.0498`; `ndiffs: 0 0 0`; raíz MA del (2,1,1) = 1) y § E1 (`0.3118 -0.4756`); cap. 2, recuadro «Sobrediferenciación», l. 4337–4356 | Solución: «con d = 1, r1 positivo: ningún indicio de diferencia de más; la diferencia la piden ADF y `ndiffs`»; pista: «…y comprueba que con $d = 1$ no aparece el indicio de haber diferenciado de más (que no lo descarta: Módulo 2.7)» | |
| 3 | imprecisión | `templates_1_3.html` l. 322–324 (M2, ciclo), l. 513–518 (M3, fila 3 de la tabla), `templates_7_9.html` l. 320–321 (M8, recuadro), `templates_10.html` l. 111–112 (M10, nota de las dos lecciones) y l. 644–646 (resumen); diapositivas `capitulo_4.md` l. 243 y l. 796 | La tercera «evidencia» para elegir $d$ (el $\hat\rho_1$ de la serie diferenciada cerca de −0.5) entra sin la salvedad del cap. 2 y se usa como si decidiera. El resumen dice «Antes de ajustar ya avisa el $\hat\rho_1$…»; el M8, «hay que mirar siempre las raíces, junto con el $\hat\rho_1$ de la serie diferenciada» en el recuadro de log(lynx), justo el caso en que el $\hat\rho_1$ no avisa; el M10 cuenta el $-0.402$ como pista de que $d = 1$ podía sobrar, cuando el cap. 2 muestra una serie con raíz unitaria, a la que la diferencia le hace falta, con $r_1 = -0.483$, y el propio M4 lee ese $-0.402$ como la firma del MA(1). El cap. 4 vuelve a enseñar como criterio algo que el cap. 2 llama indicio | `v1_comprobaciones.out` § E2 y § M3 (`-0.4020 -0.6264 -0.7188`); cap. 2 l. 4337–4356 y l. 5452–5460 | Llamarlo «indicio» y decir, con el cap. 2, que falla en los dos sentidos; en el M8, decir que en log(lynx) el $\hat\rho_1$ de la diferencia es positivo y no avisa, y que solo la raíz lo detecta; en el M10, citar el $-0.402$ como compatible con las dos lecturas. En el resumen y en la diapositiva de cierre, «indicios de haber diferenciado de más» | |
| 4 | imprecisión | `templates_1_3.html` l. 518 (M3, fila 3) | «La raíz MA del modelo con $d = 1$ queda en $1.144$, cerca del círculo (Módulo 8)». El M8 no da 1.144: su tabla da, para $d = 1$, $1.364$ y la rotula «fuera del círculo» (es el MA(1), no el ARIMA(1,1,1)). El lector que siga la remisión encuentra otra cifra con la lectura contraria | `v1_comprobaciones.out` § M3 (`raiz MA (1,1,1): 1.144 · raiz MA de MA(1) con d=1: 1.3644`); 1.144 aparece en el M1, el M6 y el M10 (HTML l. 2974, 4004, 4999), no en el M8 (l. 4362–4602) | «La del ARIMA($1,1,1$) queda en $1.144$ (Módulos 1 y 10); la del MA(1) del Módulo 8, en $1.364$» y una sola lectura para las dos (fuera del círculo, la primera más cerca) | |
| 5 | menor | `templates_10.html` l. 866–869 (ej. 3, pista) | «`Arima()` divide la suma de cuadrados de los residuales entre $n^* - k$». Con el $k$ del capítulo ($k = p + q + 1$, M6, HTML l. 3969) daría $99 - 3 = 96$; `forecast` divide entre $n^* - p - q = 97$. El comentario del M9 en Python y la `nota` del JSON lo aclaran con «k = 2», la pista no | `v1_comprobaciones.out` § sigma^2 (`SCR_97 = 20176.91 = Arima_CSSML`; `Arima_ML = 20176.92`; `2/97 = 0.02062`) | «entre $n^* - p - q$ (97 en el Nilo)» | |
| 6 | menor | `templates_7_9.html` l. 209 (M7, bloque de Python) | «el AIC ya difiere (1267.219 aqui, 1267.254 en R)»: el AIC de R es 1267.2548, que a tres decimales es 1267.255 (el par lo dio como 1267.2544) | `v1_aic_r.out` (`1267.25476355`); `v1_python.out` (`AIC 1267.219`) | «1267.255 en R» | |
| 7 | menor | `chapter.js` l. 1270 (quiz, ítem 6, retro de la opción 1) | «pasado el rezago 3, sigue rondando $0.2$ hasta el 20»: entre los rezagos 4 y 20 la ACF va de 0.090 (rezago 10) a 0.300 (rezago 8) y termina en 0.114. Mejor que el «sin acercarse a cero» de antes, pero no «ronda 0.2» | `v1_comprobaciones.out` § M3 (ACF del Nilo, rezagos 1–20; banda 0.196) | «sigue fuera de la banda en 11 de los 20 rezagos (aún $0.237$ en el 13)», que es la cifra de la diapositiva | |
| 8 | menor | `templates_1_3.html` l. 459–460 (M2, bloque de Python) | «R da 0.7997: sus residuales no son los mismos (el primero, 1.12, es el rastro de su propio arranque)»: el paréntesis sugiere que el primer residual explica la diferencia; sin él, R da 0.8118, todavía lejos de 0.8225. El resto viene de coeficientes que difieren en el cuarto decimal | `v1_comprobaciones.out` § M2 (`0.7997371`, sin el primero `0.8117996`; residual 1 = 1.12); `v1_python.out` § M2 (`0.8225`; coeficientes 0.254947 / −0.874873) | «R da 0.7997 (0.8118 sin su primer residual, 1.12): ni los coeficientes ni el arranque son idénticos. La conclusión no cambia» | |
| 9 | menor | `templates_4_6.html` l. 512 (M6, bloque de R) | T1.2 pedía llevar el 0.76 a un bloque o al generador. Sigue como comentario a mano («BIC prefiere (0,1,1) por 0.76», y el 1.71 igual), no bajo `#>`. Es la resta de dos salidas impresas (1275.04 − 1274.28), así que la cifra es correcta | salida del bloque en `v1_verifica_bloques.out` (760/760 no lo cuenta: no está en `#>`) | Imprimirlo: `with(subset(...), c(aicc = diff(aicc), bic = diff(bic)))`, o aceptarlo como aritmética de dos `#>` | |
| 10 | menor | `Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap4.py` l. 358, 612–614 y 923–926 | (a) Los claims nuevos de 0.8225, 0.785, 0.430 y 0.416 usan `CH_`, que solo comprueba que la cadena aparece en algún sitio del capítulo: no calculan la cifra. El 0.416 se puede calcular con lo que ya hay (`RD["m8.lynx_var_d0a3"]`: 0.6871/1.6532). (b) Dos notas del informe quedaron desfasadas: la 12 dice que la diapositiva del M8 «se dejó "Mínimo de varianza"» (ahora dice «Raíz MA en 1.364») y la 11, que el 83.9 % viene del cap. 6 (es la cobertura dentro de muestra de la TRM y ahora la calcula el bloque del M10; la cob80 del naïve en el cap. 6 es otra, 70.5) | `v1_verifica_cifras_cap4.out`; `directo_cap4.json` › `m8.lynx_var_d0a3`; `v1_cap6_cobertura.out` | (a) `CALC_` para 0.416 desde `RD`; para los otros tres, dejar dicho en la nota que la comprobación es de presencia y que la cifra la verifica `verifica_bloques_cap6.py`. (b) Reescribir las notas 11 y 12 | |
| 11 | menor (para la R4) | `templates_7_9.html` l. 46–52 (M7) y §1 del plan | El texto dice «su menor raíz AR tiene módulo $1.001$»; el valor es 1.0009, que queda **por debajo** también del 1.001 del artículo, y la menor raíz MA del mismo ajuste (1.0064) también está por debajo de 1.01. La frase del plan («el ejemplo depende del umbral del código, no del del artículo») no es cierta: lo descartarían los dos umbrales. Nada de esto está mal en el texto de la R1, pero la R4, al citar el 1.001 del artículo, no debe dar a entender que el ejemplo está en el borde | `v1_comprobaciones.out` § M7 (`min|raiz AR| = 1.0009 · min|raiz MA| = 1.0064`; `1.0009 < 1.001 ? TRUE`) | En la R4: «1.0009, por debajo de cualquiera de los dos umbrales» o dar la cifra con cuatro decimales | |

## Comprobado y correcto (sin hallazgo)

- **M9, forma del pronóstico**: `forecast()` da 816.18, 835.56, 840.49 y 842.17 en h = 30 y 60; el límite de la fórmula,
  842.17; las cinco primeras diferencias pronosticadas coinciden con la fórmula a 4 decimales. La lectura del simulador
  (`forma-pronostico`, d1) da 816.18 → 842.17 y el selector dice «se aplana».
- **σ̂²**: `arima(ML)` 19769.29; `Arima()` 20176.91 con CSS-ML y 20176.92 con ML; SCR/97 = 20176.91; diferencia
  relativa 0.02062 = 2/97; los coeficientes de CSS-ML y ML difieren en 1e−6.
- **ARIMA(2,1,2) del Nilo**: CSS-ML log L −630.169, raíz AR 1.0009; ML (de `Arima()` y de `stats::arima`, idénticos)
  −630.445, 2.2407; AICc del ML 1271.54, el del explorador.
- **Media del ARIMA(1,0,1)**: `arima` ML 920.70, `Arima` CSS-ML 920.56, `Arima` ML 920.70: aquí sí es el estimador.
- **M5**: con deriva, ar1 0.2707, ma1 −0.9054, drift −2.8827 (e.e. 2.0167); c = −2.102.
- **M3**: r₁ 0.4984; cociente 0.9871 frente a 2(1 − r₁) = 1.0032; r₁ de las diferencias −0.402 y −0.626, en R y en
  Python. Monte Carlo con semilla 2026: PP 100 %, `adf.test` 51.3 %.
- **M7 en Python**: (1,1,1), AICc 1267.471, 16 modelos, AIC 1267.219, `nobs_effective` 99; con n = 100 o 99 el AICc
  cambia 0.0026.
- **M8 en Python**: −247.78, 27.77, t −8.92.
- **TRM**: cotas 4080.285 (impresa 4080.28 por R y Python), error de `forecast()` 0, asimetría 0.7605, cobertura del 80 %
  0.8394, cuadrados medios 1.0967 / 1.1443 / 1.0686 (con solo ρ̂₁ saldría 1.1167–1.1605: la prosa ya no lo deduce de ρ̂₁),
  11 de 126 fuera a doce meses. El 89.6 % es `cob95` del naïve sobre 37 orígenes y 12 horizontes.
- **Ejercicios**: BJsales 0.3118 y −0.4756; log(lynx) r₁ 0.7851, cociente 0.4156, 2(1 − r₁) 0.4298.
- **Quiz, ítem 4**: deriva −2.883, c −2.102, media muestral de las diferencias −3.838; la opción nueva y la retro son
  correctas (la deriva es la media poblacional de las diferencias).
- **M12**: el Parcial 2 del 14 de octubre consta como aplicado (registro del curso); el texto en pasado es correcto.
- **Coherencia de la varianza con el cap. 2**: ninguna frase del cap. 4 la usa ya para decidir $d$, salvo el ítem 10 del
  simulacro, que no se toca y queda anotado para el banco.

## No se pudo comprobar

- `verifica_directo_cap4.R` no se ejecutó (solo vale con R 4.3.3), por instrucción.
- La revisión visual a 375 px y las capturas: solo se comprobó por HTTP la ausencia de errores de KaTeX y de consola y
  las lecturas de dos simuladores, no la maquetación.
- Si el quiz del hallazgo 1 se aplicó: no hay registro en el repo, en la carpeta del quiz ni en el vault; solo Javier
  puede confirmarlo.

## Cotejo con el registro del redactor

Leído después de la comprobación. Sus cifras coinciden con las de aquí en todo lo comprobado. El registro no menciona
los hallazgos 1 a 11; en el 1 toma «ya se aplicó» como dato, y en el 3 sigue la redacción de D3 del plan («síntomas de
sobrediferenciar»), sin la salvedad del cap. 2.

## Qué hizo la sesión maestra (2026-11-22)

Correcciones en `comprobaciones/r1_ediciones_maestra.py` (11 sustituciones únicas en `ensamblado/cap4/` y en la
fuente de las diapositivas) y cifras en `comprobaciones/r1_maestra.{R,out}`.

| # | Qué se hizo |
|---|---|
| 1 | `templates_11.html` vuelve a su texto de `7e9bc58`: describe el quiz como está diseñado, sin fecha y sin decir si se aplicó, igual que el M11 del cap. 3. El M12 sí queda en pasado: el Parcial 2 del 14 de octubre consta como aplicado |
| 2 | Pista del ejercicio 1: el $\hat\rho_1$ de la diferenciada es un indicio que falla en los dos sentidos (Módulo 2.7). Comentario de la solución: «un indicio, no una regla: con d = 1 no avisa; con d = 2 ronda −0.5» |
| 3 | La tercera evidencia pone primero la raíz MA del modelo ajustado y presenta el $\hat\rho_1$ como indicio, con la remisión al Módulo 2.7: tabla del M3, recuadro de `log(lynx)` del M8 (con su $r_1 = 0.565$, que no avisa) y resumen; la diapositiva de las tres evidencias, igual. El ciclo del M2 y la nota de las dos lecciones del M10 ya lo presentaban como síntoma entre otros: sin cambio |
| 4 | M3: «la raíz MA del ARIMA(1,1,1) queda en 1.144 (Módulo 6), más cerca del círculo que la del MA(1) del Módulo 8, en 1.364; ninguna está sobre él» |
| 5 | «entre $n^* - p - q$ (97 en el Nilo)» |
| 6 | «1267.255 en R» |
| 7 | Quiz, ítem 6: «sigue fuera de la banda en 8 de los 17 rezagos que quedan hasta el 20 (aún 0.237 en el 13)» (`r1_maestra.out`). Clave y posición, sin cambio |
| 8 | «R da 0.7997 (0.8118 sin su primer residual, 1.12): ni los coeficientes ni el arranque son idénticos» |
| 9 | El bloque de R del M6 imprime la diferencia bajo `#>` (aicc 1.71, bic 0.76) |
| 10 | El claim de 0.416 se calcula de `m8.lynx_var_d0a3`; las notas del 83.9 %, del 1.07–1.14 y de la tabla del M8, al día. **Sin cambio** el 0.785 y el 0.430: siguen como `CH_`, porque el bloque del ejercicio 2 que los imprime lo comprueba `verifica_bloques_cap6.py` |
| 11 | El §1 del plan corregido. El 1.0009 frente a los dos umbrales, para la R4 |
