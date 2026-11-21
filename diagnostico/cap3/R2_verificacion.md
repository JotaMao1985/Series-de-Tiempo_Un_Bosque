# Capítulo 3 · R2 (gráficas) · verificación independiente y correcciones

2026-11-21. Verificador de contexto limpio (Opus), sin el registro del redactor hasta terminar su propia
comprobación. Recorrió el cap. 3 en Chrome sin ventana (11 módulos, unos 75 estados, a 1200, 800 y 375 px) y
los caps. 2, 4, 5 y 6 de humo, con los deslizadores en los extremos, frente a HEAD servido aparte. Recalculó
en R las cifras nuevas (rezagos que se asoman en el MA(1) del M6, p-valores de Ljung–Box del M8, π en la
frontera |θ| = 1).

**Los 5 problemas graves del diagnóstico quedan resueltos** (3 en esta ronda, 2 en la R1). Cadena: el cap. 3
reproducible; los caps. 4–6 reciben el mismo diff, solo del armazón (`marcasLegibles`, signo menos en las
lecturas, traslado de `cifra` y `descripcionCorrelograma`); `r2b_sintaxis.py` limpio; bloques iguales a la
referencia en los cinco capítulos; ni el quiz ni la actividad del Parcial 2 ni el simulacro cambian de clave.

## Hallazgos y qué se hizo

| # | Dónde | Hallazgo | Corrección |
|---|---|---|---|
| 1 | M6, ARMA(1,1) | **Error nuevo:** la lectura decía que la PACF teórica se anula en 2 rezagos; es el redondeo del JSON (4.07·10⁻⁵ y −2.03·10⁻⁵) | Redactor: los rezagos nulos los decide el modelo (MA(q) puro tras q, AR(p) puro tras p, ninguno en un mixto): «ninguno — esta PACF nunca se corta» |
| 2 | `marcasLegibles`, cap. 5 M5 σₕ a 1200 | **Regresión:** anteponer el 1 pasaba del tope y Chart.js saltaba la mitad de las marcas | Redactor: el 1 cuenta para el tope y se quita la marca siguiente, nunca un múltiplo de 12; prueba sintética de 3850 ejes sin fallos; ningún eje de los caps. 2–6 pierde rótulos frente a HEAD. Al medir apareció y se corrigió una pérdida propia en el panel de Ljung–Box |
| 3 | `marcasLegibles`, ejes de 60 px | Dejaba «1, 24» donde HEAD no tocaba el eje | Redactor: si del paso no salen dos marcas, el eje no se toca, como en HEAD |
| 4 | M6, MA(1) a 1200 | El eje no bajaba a ±0.5 y lo que se asoma se distinguía solo por el rojo (1.59:1) | Redactor: eje fijo en ±0.5 con marcas y un rombo sobre las barras que se asoman, con su entrada en la leyenda |
| 5 | Gris de la muestral | 3.04:1, en el límite; frente a la teórica de la PACF se separa sobre todo por el tono | **Sin cambio**: cumple 3:1 y se distingue por forma y tono |
| 6 | M4, eje logarítmico | Rótulos solo en 0, ±100 y ±10 000; la nota sin «en valor absoluto» | Redactor: rejilla y rótulo en cada década; nota corregida; el panel sube a 250 px |
| 7 | `aria-label` | «los 1 que entran… a 1 pasos»; «la envolvente» | Redactor: concordancia; «el envolvente», como el capítulo |
| 8 | `altoEnEstrecho` | Mide el ancho una sola vez | **Sin cambio**: solo afecta a quien estrecha la ventana después de cargar |
| 9 | M8 a 375 | Ejes de Ljung–Box que empiezan en 2 o 4; leyenda de 3 renglones | **Sin cambio**: ya estaba; el área sigue en 105 px |

Corrección de la sesión maestra en la segunda pasada: la lectura del M6 decía «rezagos con ACF teórica nula:
15», que se lee como el rezago 15; ahora dice «del 2 al 16 (15 rezagos)»
(`comprobaciones/r2_ediciones_maestra.py`).

## Después de corregir

- `verifica_todo.py`: 11 en verde; cap. 3 reproducible; caps. 4–6 con el mismo diff del armazón.
- Bloques: 487/487, 557/557, 713/735, 1199/1212, 415/434 (iguales a la referencia).
- `r2b_sintaxis.py` limpio en los cinco; consola sin errores (solo el 404 del favicon).
- Comprobado por HTTP: el panel de Ljung–Box del M8 con el AR(2) (0.0461 bajo la línea, en rojo) y el M6
  con el MA(1) y el ARMA(1,1).

## Queda

- Caps. 4–6: sus `aria-label` siguen fijos y dos `descripcionGrafico` del quiz del cap. 4 dan la respuesta
  (es de sus fuentes en `ensamblado/cap{4,5,6}/`).
- Tooltips, teclado, modo oscuro e impresión, sin revisar.
- El rombo del M6 cae unos píxeles a la izquierda de la barra muestral.
