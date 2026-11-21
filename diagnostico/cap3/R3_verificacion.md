# Capítulo 3 · R3 (estructura) · verificación independiente y correcciones

2026-11-21. Verificador de contexto limpio (Opus), sin el registro del redactor hasta terminar su propia
comprobación. Recalculó en R con código propio cada cifra nueva o movida (`comprobaciones/v3_cifras.R`), ejecutó
por separado los bloques de Python tocados y cada uno de los 15 bloques de R en una sesión aislada (ninguno depende
de una variable que ahora se define después), midió los minutos con su propia copia corregida de la herramienta
(`v3_minutos.py`) y recorrió los 11 módulos por CDP a 1200 y 375 px con los plegados abiertos.

**No halló nada falso, ninguna regresión ni ninguna referencia colgada.** Todas las cifras coinciden; las
afirmaciones nuevas (elasticidad amplitud–nivel y λ = 1 − b, `auto.arima` por AICc, banda de Bartlett, θ = −1 y la
sobrediferenciación, `AirPassengers` en los módulos 5.5 y 5.7) son correctas. Confirmó el fallo de la herramienta
de carga del diagnóstico y halló una segunda causa: el `$` de `pacf(y)$acf` dentro de `<code>` desplazaba la paridad
de las fórmulas y restaba unos 6 min al M5. Con las dos correcciones, cada módulo queda a menos de 0.5 min de lo
declarado. Quiz, actividad de repaso y simulacro, idénticos byte a byte; los 14 simuladores, sus ids y atributos,
también; caps. 2 y 4–6 sin cambios.

## Hallazgos y qué se hizo

| # | Dónde | Hallazgo | Corrección |
|---|---|---|---|
| 1 | M1, «Convenios de signo» | «un MA(1) de θ = +0.7, el modelo que el Capítulo 2 adelantó»: el cap. 2 adelantó el MA(1) con θ = −1 | Maestra: la remisión sale |
| 2 | M7 y M8 | «El último bloque de código…»: cada módulo tiene un solo bloque, y el ejemplo de CSS (T = 40) y el Monte Carlo de `fitdf` solo están en la pestaña R | Maestra: «el código R de abajo» / «el código R de este módulo» |
| 3 | M5, momentos del ARMA(1,1) | ρ₁ = 0.8308 «la primera de las cuatro cifras del Módulo 4» dicho en el párrafo y repetido en el resultado del plegado | Maestra: el plegado da la cifra sin repetir el comentario |
| 4 | M8, `fitdf` | El Monte Carlo (4.9 % frente a 2.6 %), a la vista y otra vez dentro del plegado | Maestra: el plegado remite al párrafo anterior |
| 5 | Ejercicios 1 y 3 (`n`), M9 «el envolvente» | Restos de notación | **Sin cambio**: los ejercicios son de la R5; «el envolvente» (sustantivo femenino en el uso habitual, «la envolvente») toca también el texto de un simulador: R5 |
| 6 | `courseData` | El comentario cita `r3_minutos.py`, sin seguimiento | Entra en el commit |
| 7 | M9, «El código del caso 1» | Decía que las cifras de la serie cruda salen de los Módulos 7 y 8, y el bloque calcula también el ARMA(2,1), la asimetría y Shapiro–Wilk de la cruda | Maestra: lo dice |

Las correcciones: `comprobaciones/r3_ediciones_maestra.py` (6 sustituciones únicas en `ensamblado/cap3/`), aplicadas
después de `r3_edita.py`; por eso `r3_edita.py --comprobar` ya no da el árbol exacto (es HEAD + ediciones + las de
la maestra). Comprobación propia de la maestra en R: `comprobaciones/maestra_r3.R` · `.out` (elasticidad sobre
1770–1869: 0.8165, 0.7658, 0.7034; tres ceros en 1700–1988; ρ₁ inducido 0.2492; `ic` por defecto `aicc`).

## Después de corregir

- `verifica_todo.py`: 11 en verde (`r3b_verifica_todo.out`); cap. 3 reproducible; `ensambla_cap4/5/6.py` corridos y
  los caps. 4–6 sin cambios.
- Bloques del cap. 3: **732 de 732** (antes 557/557; `r3b_bloques_cap3.out`). El «write failed» del final de la
  sesión de R ya salía sobre HEAD.
- `r2b_sintaxis.py` limpio en los cinco; `audita_posicion_correcta.py` en verde.
- Por HTTP (`htmls-series`): M1, M5, M7, M8, M9 y M10 sin errores de KaTeX ni `$` sin componer fuera del código, con
  las frases corregidas presentes y la consola sin errores.

## Queda

- R5: `n` en los ejercicios 1 y 3, «periodo» en el 3, «no queda identificado» en una retro del quiz y «el envolvente».
- R4: lo que el redactor lista en `R3_cambios.md` (λ = 1 − b, ρ₁ inducido, Bartlett, `auto.arima`, «Lo que viene»,
  Yule, FPP3 9.5, Hyndman–Khandakar, S-PLUS).
- El M9 pasa a 31 min y el capítulo a unos 150 en M1–M10: lo medido es lo que hay; si se quiere aligerar, es decisión
  de contenido, no de esta ronda.
