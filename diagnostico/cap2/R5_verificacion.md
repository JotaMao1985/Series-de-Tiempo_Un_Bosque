# Capítulo 2 · R5 (práctica) · verificación independiente y correcciones

2026-11-18. Verificador de contexto limpio (Opus), sin el informe del redactor hasta terminar su propia
comprobación. Resolvió en R los siete «Para practicar», los ejercicios 1, 2, 3 y 5 del Módulo 9 y las
cifras del 4 sobre la copia fija de la TRM. Sus guiones: `comprobaciones/v5_*`.

**Sin errores que enseñen algo falso ni claves mal puestas.** Cada cifra bajo `#>` coincide con R; los 11
bloques de solución corren solos; las líneas con `data-afirma` o `<cite>` no cambian en el diff.

## Hallazgos y qué se hizo

| # | Dónde | Hallazgo | Corrección (sesión maestra) |
|---|---|---|---|
| 1 | M8 (c) | «5.15 y 7.70» restaban valores ya redondeados | 5.16 y 7.69 (R: 5.1571 y 7.6934) |
| 2 | M8 (c) | «33 centavos más», sin decir respecto de qué | «unos 31 centavos por encima» de la mediana (R: 0.309) |
| 3 | M9 E2 | «3.0 % y 3.2 % caen en el borde» de [3.1, 6.9] | 3.0 queda justo por debajo; 3.2, justo dentro |
| 4 | Quiz P5 | La retro del distractor «tendencia lineal» daba un motivo que choca con el M6 (b) | Explica el motivo real: el rechazo del ADF no es fiable con k = 4 < 12 |
| 5 | Quiz P6 | La pista remitía a la fila del M3 con los mismos números del gráfico | Pista nueva: cómo baja la ACF y qué serie conserva memoria a 12 rezagos |
| 6 | Quiz P2 | Tolerancia 0.5: quien no redondea (170.7) acertaba, contra lo que pide la pista | Tolerancia 0.2 y retro para 170.7; probado por HTTP: 170.7 falla, 171 acierta |
| 7 | M3 (d) | «el azar solo puede fabricar» se lee como «como mucho» | «el azar, por sí solo, puede fabricar» |
| 8 | M6 (a) | Cita entre comillas que no era literal de la tabla | Texto literal de la fila |
| 9 | comentario JS | «salvo el 7»: el M9 tampoco trae «Para practicar» | «salvo el 7 y el 9» |
| 10 | M9 E4 | «`nsdiffs()` devuelve 0» sin salida bajo `#>` | `forecast::nsdiffs(trm)` con `#> [1] 0` |
| 11 | M4 | Titular daba `LakeHuron` por AR(2) antes de comprobar la estacionariedad | «un AR(2) si resulta estacionaria»; «la PACF sugiere un AR(2)» |
| 12 | M9 E1 | «no hay nada que estabilizar» en `co2` (la dispersión crece algo: λ de Guerrero −0.034) | «el logaritmo cambiaría poco la serie» |
| 13 | M6 (d) | `ndiffs(nhtemp)` por defecto pide 1 diferencia y la solución resta la recta | Frase nueva: con KPSS de nivel pide 1; con `type = "trend"`, 0; decide el analista y lo escribe |
| 14 | Quiz P4 | Las retros anticipan el criterio del E3 (c) del M9 | **Sin cambio**: es contenido del M7, riesgo bajo |

Las correcciones están en `comprobaciones/r5_ediciones_maestra.py` (15 sustituciones, cada una única) y
sus cifras en `comprobaciones/maestra_r5.R` · `.out`, que además vuelve a medir de forma independiente
Guerrero de `AirPassengers`, `JohnsonJohnson` y `UKgas`, la P2, los rezagos del DAX, el ADF de
`UKDriverDeaths`, el Monte Carlo del E2 y r₁ y r₂ de `discoveries` a mano: todo coincide.

## Después de corregir

- `verifica_todo.py`: 11 en verde. Capítulo 3 reproducible; `r2b_sintaxis.py` limpio.
- `verifica_bloques_cap6.py --html` sobre el capítulo 2: **487 de 487**, 0 discrepancias (antes de la ronda, 277).
- `audita_posicion_correcta.py` y `cuenta_sitio.py` en verde (32 ejercicios).
- Por HTTP: sin errores de consola ni de KaTeX; las frases nuevas presentes.

## Queda anotado, sin resolver en esta ronda

- El M7 toma `UKgas` en logaritmos sin decir que deja amplitud sin estabilizar (lo dice la retro de la P8).
- La frase sin marcar del M6 «3.2 %, cerca del 5 % nominal»: el E2 la matiza (4.3 % con 5000 series).
- Motor del quiz: tras el primer fallo de la múltiple dice cuántas faltan; con dos correctas de cinco, acota el segundo intento.
- El gráfico de la P6 repite el correlograma de la caminata del M3 y el M4.
