---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-01 Componentes y descomposición]]"
fecha: 2026-08-12
estado: aprobado
---

# Plan — Formalización del método de descomposición · Capítulo 1, Módulo 6

**Objetivo:** escribir en símbolos el algoritmo que el Módulo 6 hoy solo describe en prosa,
en las dos escalas, y darle al caso aditivo el ejemplo numérico que nunca tuvo.

## 1. El hueco

El Módulo 6 (`1.6 Descomposición clásica`) enuncia el método dentro del componente `.ciclo`:
«quitar la tendencia —restando en el aditivo, dividiendo en el multiplicativo—», «promediar
todos los eneros». Es la receta **descrita, nunca escrita**.

Lo único formalizado en todo el recorrido:

| Fórmula | Dónde | Escala |
|---|---|---|
| $\hat T_t$, media móvil centrada $2\times m$ | Módulo 5 | ambas |
| $\hat R_t = y_t / (\hat T_t \hat S_t)$ | Módulo 6 | solo multiplicativa |

Carencias:

| # | Carencia | Dónde |
|---|---|---|
| C1 | No existe fórmula para la serie sin tendencia $d_t$, ni para el índice bruto $\tilde s_k$ («promediar todos los eneros»), ni para la normalización, en **ninguna** de las dos escalas | tras el `.ciclo` |
| C2 | El caso aditivo son **tres frases sueltas** en 230 líneas —paso 3 del ciclo, «se miden en pasajeros y se suman», «la condición equivalente es que sumen 0»— sin una fórmula ni un número | disperso |
| C3 | La nota afirma el reescalado sin escribirlo: «el método los reescala dividiéndolos por su media» | nota final del módulo |
| C4 | El Paso 1 del ciclo promete una flecha de retorno —«si el residuo conserva la forma estacional, la escala estaba mal elegida»— que el capítulo nunca demuestra | panel `escala` del ciclo |

## 2. Restricciones verificadas antes de planear

| Restricción | Estado |
|---|---|
| ¿Existe `ensamblado/cap1/`? | **No.** El capítulo 1 se edita directo (ver [[series-tiempo-riesgo-reensamblado]]) |
| ¿Algún ensamblador escribe este archivo? | **No.** La cadena es 2 → 3 → 4 → 5 → 6. El capítulo 1 es *origen* de `retropropaga.py` e `instala_ciclo.py`, nunca destino |
| ¿`instala_ciclo.py` puede volver a tocar el `.ciclo`? | Aborta si ya existe (`"ya tiene el componente .ciclo"`). Aun así, **el bloque nuevo va fuera del `.ciclo`** |
| ¿Componente para el desarrollo largo? | Sí: `.derivacion` plegable, ya instalado en el módulo 8 (`der-fuerza-ft`) |
| ¿CSS nuevo? | **Ninguno.** `table` ya trae `overflow-x: auto` en móvil; `.formula` y `.derivacion` existen |
| ¿Datos nuevos? | **Ninguno.** Todas las cifras del contraejemplo salen de `decompose(AirPassengers, "additive")`, verificado en R |

## 3. Decisiones de esta ronda

| # | Decisión | Elección |
|---|---|---|
| D1 | Ancla numérica del caso aditivo | **Contraejemplo sobre la serie cruda**, no sobre `log`: las cifras quedan en pasajeros y comparables con la lectura multiplicativa, y no se solapa con la caja casi gemela del Módulo 7 (STL sobre log, mismo julio de 1955) |
| D2 | ¿Gráfico de la descomposición aditiva? | **No.** El módulo ya carga con un simulador de cuatro paneles; el contraejemplo se sostiene en cifras |
| D3 | Forma del bloque formal | **Tabla de tres columnas** `Paso · Aditivo · Multiplicativo`, con `colspan` en los pasos que no dependen de la escala. Hace visible que la única diferencia es restar/dividir |
| D4 | Dónde va el porqué de la normalización | En un `.derivacion` plegable, no en el cuerpo: es el paso que más se pregunta y el que más estorba si se cuenta en línea |
| D5 | Matemáticas en celdas | Solo `$…$` en línea (con `\dfrac` donde haga falta). Nunca `$$…$$` dentro de `<td>` |

## 4. Cifras verificadas en R antes de escribir

`Rscript` sobre `decompose()`, contrastadas con lo que ya dice el capítulo:

| Cifra | Valor | Estado |
|---|---|---|
| Multiplicativo, julio 1955 | $364 = 285.75 \times 1.2266 \times 1.0386$ | ya en el texto ✓ |
| Once cocientes de julio | 1.1673 … 1.2723 | coinciden uno a uno ✓ |
| Índice bruto / media / reescalado | $1.224391 / 0.998236 = 1.2266$ | ya en el texto ✓ |
| $n_k$ | 11 para los doce meses | nuevo |
| **Aditivo, julio 1955** | $364 = 285.75 + 63.83 + 14.42$ | nuevo |
| Exceso real de julio sobre el nivel del año | 21.3 (1949) → 145.8 (1960) | nuevo |
| Traducción del 1.2266 a pasajeros | 28.7 (1949) → 107.9 (1960) | nuevo |
| Desviación del residuo aditivo por año | 30.5 · 20.7 · 22.4 · 17 · 14.5 · 5.6 · 6.1 · 10 · 17.2 · 29.4 · 29.4 · 25.4 | nuevo |

La U de esa última fila es C4 resuelta: el aditivo solo ajusta en mitad de la muestra.

## 5. Tareas

| # | Tarea | Tamaño | Depende de |
|---|---|---|---|
| 1 | Bloque «El método en símbolos»: prosa de notación ($m$, $k$, $J_k$, $n_k$) + tabla de tres columnas con los pasos 2, 3a–3d y 4 más la condición de normalización | S | — |
| 2 | `.derivacion` plegable: por qué se normaliza y qué se rompe sin ello (el residuo oscilaría en torno a 1.0018 y la serie desestacionalizada quedaría un 0.18 % alta) | S | 1 |
| 3 | Contraejemplo aditivo sobre `AirPassengers`, tras la nota de los índices | S | 1 |
| 4 | Retoques de coherencia: la nota pasa a remitir al paso 3c en vez de afirmarlo | XS | 1, 3 |
| 5 | Verificación en navegador y cotejo final con R | XS | 1–4 |

### Criterios de aceptación

- [ ] Las dos escalas tienen escritos los cuatro pasos, no solo el residuo multiplicativo
- [ ] El caso aditivo tiene fórmula **y** ejemplo numérico
- [ ] Toda cifra nueva en pantalla sale de `decompose()` y está verificada en R
- [ ] KaTeX renderiza dentro de las celdas; la tabla no desborda en móvil
- [ ] El bloque nuevo queda **fuera** del `.ciclo`
- [ ] Consola del navegador sin errores
- [ ] Prosa en voz impersonal y «el componente» en masculino ([[series-tiempo-convenciones-prosa]])

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| `$$…$$` dentro de `<td>` rompe la maquetación | Medio | D5: solo matemáticas en línea en celdas |
| Tres columnas desbordan en móvil | Bajo | La regla de `@media (max-width: 768px)` ya da `overflow-x: auto` a `table` |
| El contraejemplo alarga un módulo ya largo | Medio | D2: sin gráfico nuevo; el contraejemplo son dos párrafos y dos recuadros |
| Redundancia con la caja de julio 1955 del Módulo 7 | Bajo | D1: contraejemplo en escala original, no en `log` |

## 7. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Ronda anterior sobre el mismo capítulo: [[PLAN_Graficos_Aditivo_Multiplicativo]]
- Capítulo: [[20948-01 Componentes y descomposición]]
