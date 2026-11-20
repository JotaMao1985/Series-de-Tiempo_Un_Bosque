# Capítulo 3 · R1 (errores) · verificación independiente y correcciones

2026-11-20. Verificador de contexto limpio (Opus), sin el registro del redactor hasta terminar su propia
comprobación. Recalculó en R cada cifra nueva o cambiada y demostró dos resultados que la ronda introduce:
que la envolvente ±Rʲ/sin ω es la cota correcta (|sin((j+1)ω)| ≤ 1; ninguna de las 25 barras queda fuera) y
que la fórmula de FPP3 §9.5 es el máximo de la densidad espectral del AR(2).

**Los 17 errores e imprecisiones del par quedaron corregidos**, salvo dos con matiz (hallazgos 1 y 2). El
quiz `cap3`, la actividad del Parcial 2 y el simulacro no cambian. Los caps. 4–6, idénticos a HEAD. Ningún
7-grama del diff aparece en los textos de `bibliografia/_local/`.

## Hallazgos y qué se hizo

| # | Dónde | Hallazgo | Corrección (sesión maestra) |
|---|---|---|---|
| 1 | Ej. 3, discusión | «Se derrumba en cuanto la ventana llega al siglo XX» sugiere que lo anterior pasa: 49 de las 101 ventanas que acaban antes de 1900 también rechazan | Dice que falla en 138 de 190, también en 49 que acaban antes de 1900, y en todas las que llegan al siglo XX |
| 2 | M7, CSS y ML | «Entre un 3 y un 5 %» y «13 %» medidos con 4 semillas; ML no da estimación en algunas réplicas | Con 12 semillas: CSS > 1 entre 2.5 y 4.6 %; ML ≥ 0.999 entre 13 y 17 %; ML sin estimación en 4 a 13 de cada mil, dicho en la prosa |
| 3 | M9, TRM | Atribuye el MA(1) a `stepwise = FALSE, approximation = FALSE`; lo decide solo el primero | Dice que `approximation = FALSE` ya es el valor por defecto con 137 datos |
| 4 | M9 y ej. 3 | «FPP3» antes de presentarse; una mención más de «la ventana de Yule»; inventario desfasado | «Hyndman y Athanasopoulos (FPP3, sección 9.5)». La atribución a Yule y el inventario, a la R4 |
| 5 | varias | Cifras nuevas que solo salen de un guion de diagnóstico | Se acepta `diagnostico/cap3/comprobaciones/` como su origen (T1.1); `r1_errores.R` y `maestra_r1.R` entran al repo |
| 6 | JS del M9 | «sen ω» en la lectura, `\sin\omega` en la prosa | «sin ω» |
| 7 | M9 | ARIMA(0,0,0) antes de que se presente ARIMA | **Sin cambio**: se aclara en el acto («es decir, ruido blanco»); `auto.arima` se presenta en la R3 |
| 8 | `genera_soluciones.R` | El `cat` de `cien_anios` da por hecho que la primera ventana favorable empieza en 1700 | **Sin cambio**: la salida es correcta hoy; anotado |

Las correcciones: `comprobaciones/r1_ediciones_maestra.py` (9 sustituciones únicas en `ensamblado/cap3/`); las
cifras: `comprobaciones/maestra_r1.R` · `.out`.

## Después de corregir

- `ensambla_cap3.py`: reproducible byte a byte. Caps. 4–6 sin cambios.
- `verifica_todo.py`: 11 en verde. Verificador de bloques del cap. 3: **557 de 557** (antes, 533 de 534).
- `r2b_sintaxis.py` limpio; `audita_posicion_correcta.py` en verde.
- Por HTTP: los módulos 7, 9 y 10 sin errores de consola ni de KaTeX, con las frases nuevas presentes.

## Para la R4

- La «ventana de Yule» (tres menciones) sigue sin fuente leída (c3-m10-37).
- Actualizar en el inventario las filas c3-m9-24, c3-m10-08, c3-m10-15 y c3-m10-35, cuyo texto cambió.
- «FPP3 (sección 9.5)» sin `data-afirma`.
