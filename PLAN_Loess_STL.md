---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-01 Componentes y descomposición]]"
fecha: 2026-08-17
estado: aprobado
---

# Plan — Qué es Loess · Capítulo 1, Módulos 5 y 7

**Objetivo:** explicar la regresión local, que hoy el material solo **nombra**, para que las
tres ventajas de STL dejen de ser afirmaciones, `s.window` y `trend(window=)` dejen de ser
números mágicos y el Ejercicio 3 tenga por fin su mecanismo.

## 1. El hueco

Loess aparece **tres veces en todo el material**, siempre como nombre propio:

| Dónde | Qué dice | ¿Lo ve el estudiante? |
|---|---|---|
| M7, línea 3239 | «STL (*Seasonal-Trend decomposition using Loess*)» | sí, como sigla |
| M7, línea 3241 | «ajusta curvas locales por regresión ponderada (Loess)» | sí, como paréntesis |
| `precalculo/genera_soluciones.R:286` | «(pesos de Loess reponderados)» | **no** |

Los capítulos 2–6 no lo mencionan. No hay `lowess`, ni «regresión local», ni «suavizado
local» en ningún otro sitio del repositorio.

Por el [[Criterio de contenido]] —«si una idea está *dicha* pero no *mostrada*, hay un
hueco»— esto está un escalón por debajo: está **nombrada** y ni siquiera dicha. Lo que
arrastra:

| # | Carencia | Dónde |
|---|---|---|
| C1 | La definición no existe. El estudiante termina el capítulo sin saber qué ajusta una regresión local, sobre qué vecindario ni con qué pesos | M7, tras la sigla |
| C2 | Las **tres ventajas** de STL se afirman, no se derivan. «La regresión local no exige vecinos a ambos lados» es exactamente la frase que solo se entiende si ya se sabe qué es | las tres viñetas del M7 |
| C3 | El **span** —el parámetro central de Loess— no se nombra nunca, y sin embargo gobierna los dos argumentos que sí aparecen: `s.window` y `trend(window = 21)` | bloque de código del M7 |
| C4 | El **Ejercicio 3** remata con «STL no es intrínsecamente resistente: la resistencia la trae `robust = TRUE`». El mecanismo (reponderación por el tamaño del residuo) solo vive en un comentario de R que el estudiante no lee | cierre del capítulo |
| C5 | El M5 construye la media móvil como «promediar cada punto con sus vecinos» y muere en la pérdida de extremos —anunciando ya STL—, pero el puente (ponderar en vez de promediar, recta en vez de nivel) no está tendido | cierre del M5 |
| C6 | **Hallazgo lateral:** el bloque de código usa `trend(window = 21)`, pero la figura y todas las cifras de la prosa se calcularon con el `t.window` por defecto, **19**. Quien corra el código mostrado obtiene $\hat S_{\text{julio}} = 0.2155$, no el **0.2164** que cita el texto tres párrafos antes | M7, pestaña R |

## 2. Restricciones verificadas antes de planear

| Restricción | Estado |
|---|---|
| ¿Existe `ensamblado/cap1/`? | **No.** El capítulo 1 se edita directo (ver [[series-tiempo-riesgo-reensamblado]]) |
| ¿Algún ensamblador escribe este archivo? | **No.** La cadena es 2 → 3 → 4 → 5 → 6. El capítulo 1 es *origen* de `retropropaga.py` e `instala_ciclo.py`, nunca destino |
| ¿Hay que renumerar módulos? | **No.** El contenido entra en el 5 y el 7, que ya existen. El quiz, el `.ciclo` y las remisiones cruzadas quedan intactos |
| ¿CSS nuevo? | **Ninguno.** `.derivacion` ya está instalado (M6 y M8), y `.simulador`, `.warning`, `.note` y `.formula` existen desde el primer commit |
| ¿Datos nuevos incrustados? | **Ninguno.** El simulador calcula el Loess en el navegador desde `DATOS_CAP1`, que ya trae `observado` y los tres componentes `stl_log` |
| ¿Hay que tocar `precalculo/genera_datos.R`? | **No.** Las cifras del texto se verifican en R, no se incrustan |
| ¿Se retropropaga a los capítulos 2–6? | **No.** Loess solo se usa aquí |

## 3. Decisiones de esta ronda

| # | Decisión | Elección |
|---|---|---|
| D1 | Ubicación | **El grueso en el M7**, antes del simulador STL —donde se cobra el rendimiento— más un **puente de un párrafo en el M5**. Decidido con Javier el 2026-08-17, frente a un módulo 6 propio, que habría obligado a renumerar 6→7, 8→9, 9→10 y a rehacer quiz, `.ciclo` y remisiones |
| D2 | Profundidad | **Mecánica completa** en el cuerpo (vecindario, span, recta local ponderada, pesos tricúbicos, bucle robusto con pesos bicuadrados); el estimador formal y las iteraciones, en `.derivacion` plegable |
| D3 | Dónde se engancha el puente del M5 | Al **párrafo de la pérdida de extremos**, que ya anuncia STL («será una de las tres limitaciones que acaben empujando hacia STL»), **no** al párrafo final del módulo: ese cierre («ese encadenamiento tiene nombre propio») es la transición al M6 y se rompería |
| D4 | Sobre qué serie trabaja el simulador | Sobre $\log y_t - \hat S_t$, la **desestacionalizada en log**, que es exactamente lo que STL suaviza en su paso de tendencia. Se obtiene en JS sumando dos vectores ya incrustados (`stl_log.tendencia + stl_log.residuo`). Sobre la serie cruda el vaivén anual taparía los pesos, que son lo que hay que ver |
| D5 | Qué demuestra el simulador | Un punto focal móvil: la ventana resaltada, los pesos tricúbicos, la recta local ajustada y el punto resultante. **Con la media móvil centrada superpuesta**, que desaparece al llevar el foco a los extremos mientras la recta local sigue existiendo. Es C2 mostrada en vez de afirmada |
| D6 | ¿El simulador reproduce `stl()`? | **Sí, con desvío máximo de 0.0045 en los 144 meses** (corregido el 2026-08-17 al implementarlo; ver D14). El simulador dibuja **también** la tendencia real de STL, ya incrustada: lo que se pensó como una declaración de discrepancia acabó siendo la comprobación de que el método enseñado es el método usado |
| D7 | Robustez: ¿simulador o cifras? | **Cifras.** Un simulador de robustez duplicaría el Ejercicio 3. Se cierra con la tabla de pesos bicuadrados sobre el mismo atípico del ejercicio (obs. 79), que es lo que le da el mecanismo que le falta |
| D8 | Orden dentro del M7 | Explicación → simulador → `.derivacion` → robustez → simulador STL de 4 paneles. Primero se ve, después se formaliza |
| D9 | Grados del polinomio local | Se dicen, con su porqué y medidos: `stl()` usa `t.degree = 1` para la tendencia y `s.degree = 0` para lo estacional. Dato verificado, no generalidad |
| D10 | `trend(window = 21)` | **Se corrige a 19** (C6). Así el código reproduce la figura, y de paso el número deja de ser mágico: 19 sale de una fórmula que a partir de esta ronda sí se puede explicar. **Confirmado por Javier el 2026-08-17** |
| D11 | Matemáticas en celdas | Solo `$…$` en línea. Nunca `$$…$$` dentro de `<td>`, como en la ronda anterior |
| D12 | Controles del simulador | **Grado (0/1) y pesos (planos/tricúbicos)**, además del span. Confirmado por Javier el 2026-08-17, pero **reencuadrado tras medirlo**: el motivo que se argumentó al proponerlo —«el sesgo de la constante en los extremos»— solo se sostiene a medias (ver D13). El titular pasa a ser la identidad con la media móvil |
| D13 | Qué demuestra el control de grado | **Dos cosas, las dos limpias.** (a) Bajar los dos controles a su posición más simple **devuelve exactamente la media móvil**: grado 0 con pesos planos da 5.5482 en $t=72$ y la media móvil de la misma anchura da 5.5482. Es el puente del M5 hecho ejecutable. (b) **El grado solo importa en los extremos**: 0.0000 de diferencia en el centro y **0.0498** en diciembre de 1960, donde el grado 1 clava la tendencia de `stl()` (6.2043 contra 6.2048) y el grado 0 se queda 0.05 por debajo. *Corregida el 2026-08-17: ver D14* |
| D14 | **Corrección de D6 y D13** | Las cifras con las que se escribieron D6 y D13 salían de una comprobación en R que **truncaba la ventana en los bordes** en vez de desplazarla. Loess toma los $span$ puntos *más próximos*: en enero de 1949 la ventana no encoge a 10 puntos, se apoya en los 19 primeros. Con la regla correcta —la que implementa el simulador, verificada contra R hasta el cuarto decimal— las dos conclusiones que se habían sacado se dan la vuelta: el ajuste a mano **sí** reproduce `stl()` (0.0045, no 0.023) y el grado **sí** se separa en los extremos (0.0498, no −0.0017). El motivo original para pedir el control de grado era correcto; lo que estaba mal era la medición que lo desmintió |

## 4. Cifras verificadas en R antes de escribir

`Rscript` sobre `stats::stl` y `AirPassengers`, R 4.6.0. Ninguna cifra a mano (D10 del plan
maestro).

**Los parámetros por defecto, que hoy no se explican**

| Cifra | Valor | Para qué sirve |
|---|---|---|
| `t.window` por defecto con `s.window = "periodic"` | **19** | Desmagificar el `window` del código. Sale de `nextodd(ceiling(1.5 m / (1 - 1.5/s.window)))` con $m=12$ |
| `s.window` efectivo de `"periodic"` | 1441 $= 10n+1$ | Por qué «periodic» congela lo estacional: la ventana abarca toda la serie |
| `s.degree` / `t.degree` | 0 / 1 | D9: constante local para lo estacional, recta local para la tendencia |
| `inner` / `outer` con `robust = TRUE` | 1 / 15 | El bucle externo **es** la robustez; sin ella `outer = 0` |
| `inner` / `outer` con `robust = FALSE` | 2 / 0 | Cero iteraciones de reponderación: C4 en una cifra |

**Los extremos, que hoy solo se afirman**

| Cifra | Valor |
|---|---|
| Media móvil centrada $2\times12$: observaciones sin estimar | **12** de 144 (primera válida $t=7$, última $t=138$) |
| Tendencia de `stl()`: observaciones sin estimar | **0** |
| En $t=1$ — recta local ponderada / media simple de la misma ventana / `stl()` | 4.8608 / 4.8305 / **4.8294** |
| En $t=144$ — recta local ponderada / media simple / `stl()` | 6.1818 / 6.1643 / **6.2048** |

**El tricubo, que hoy no se nombra**

| Cifra | Valor |
|---|---|
| Peso del punto central, ventana de 19 | 1 |
| Peso del punto del borde | **0.0199** — cuenta unas **50 veces menos** que el central |
| Suma de los 19 pesos | 11.5718 |

**La robustez, sobre el atípico del Ejercicio 3 (obs. 79, julio de 1955, inflado un 50 %)**

| Cifra | Valor |
|---|---|
| Residuo del punto contaminado | 0.4404 |
| Umbral $h = 6\,\mathrm{mediana}\lvert r\rvert$ | 0.1041 |
| **Peso bicuadrado del atípico** | **0** — queda literalmente fuera del ajuste |
| Peso mediano del resto de puntos | 0.9469 |
| Puntos que reciben peso 0 en total | 5 |

**Grado y pesos (D12, D13)** — sobre $\log y_t - \hat S_t$, ventana de 19.
Rehecha el 2026-08-17 con la regla de ventana correcta (D14) y **verificada dos veces**: R y el
JS del simulador coinciden hasta el cuarto decimal.

| Foco | Grado 1 | Grado 0 | Diferencia | Grado 0 + planos | `stl()` |
|---|---|---|---|---|---|
| $t=1$ (ene 1949) | 4.8266 | 4.8409 | 0.0143 | 4.8595 | 4.8294 |
| $t=5$ | 4.8354 | 4.8436 | 0.0082 | 4.8595 | 4.8354 |
| $t=72$ (centro) | 5.5439 | 5.5439 | **0.0000** | 5.5482 | 5.5432 |
| $t=140$ | 6.1698 | 6.1486 | 0.0212 | 6.1296 | 6.1701 |
| $t=144$ (dic 1960) | **6.2043** | 6.1545 | **0.0498** | 6.1296 | **6.2048** |

| Cifra | Valor |
|---|---|
| Grado 0 **con pesos planos** en $t=72$ | 5.5482 |
| Media móvil de 19 meses en $t=72$ | **5.5482** — coinciden exactamente (D13a) |
| Desvío máximo del Loess del simulador frente a `stl()`, en los 144 meses | **0.0045** (D6) |

Tres lecturas de esta tabla, y las tres entran en el material:

- **El grado solo importa en los extremos.** En el centro los dos grados dan el mismo número
  hasta el cuarto decimal; en diciembre de 1960 se separan **0.0498**, y es el grado 1 el que
  acierta: 6.2043 contra los 6.2048 de `stl()`. Es la ventaja de la recta sobre el nivel cuando
  la ventana se apoya de un solo lado, y ahora sí está medida.
- **Grado 0 con pesos planos deja de ser Loess y vuelve a ser la media móvil**, con la misma
  cifra hasta el cuarto decimal. El puente del M5 se ejecuta en vez de leerse.
- **El ajuste local reproduce `stl()`**: 0.0045 de desvío máximo. Lo que el simulador enseña no
  es una maqueta del método, es el método.

**El hallazgo lateral C6**

| Cifra | Valor |
|---|---|
| $\hat S_{\text{julio}}$ con `t.window = 19` (la figura y el texto) | **0.2164** |
| $\hat S_{\text{julio}}$ con `t.window = 21` (el código mostrado) | 0.2155 |
| Diferencia máxima en la tendencia entre ambos | 0.00681 (media 0.00184) |

**Sin verificar todavía:** `fable` no está instalado en esta máquina, así que la equivalencia
`trend(window = n)` ⟷ `t.window = n` se da por buena pero **no está comprobada**. La línea de
R base del mismo bloque —`plot(stl(log(AirPassengers), s.window = "periodic"))`— sí usa el
defecto 19 y sí reproduce la figura; C6 afecta solo al fragmento de `fable`. La tarea 6 debe
comprobarlo antes de tocar nada.

## 5. Tareas

| # | Tarea | Archivos | Tamaño | Depende de |
|---|---|---|---|---|
| 1 | **Puente en el M5**: un párrafo enganchado al de la pérdida de extremos (D3). La media móvil es el caso plano de una familia mayor —pesos iguales, nivel constante, ventana que exige vecinos a los dos lados—; aflojar las tres cosas da Loess | HTML cap. 1, M5 | XS | — |
| 2 | **Bloque «Qué hace Loess»** en el M7, antes del simulador STL: vecindario y span, recta local en vez de nivel, pesos tricúbicos con la tabla centro/borde (1 contra 0.0199) | HTML cap. 1, M7 | S | — |
| 3 | **Simulador `loess-local`**: HTML + `SIMULADORES['loess-local']`. Loess en JS sobre la desestacionalizada en log (D4), foco móvil, ventana y pesos visibles, media móvil superpuesta y tendencia de `stl()` como referencia (D5, D6). **Tres controles: span, grado (0/1) y pesos (planos/tricúbicos)** (D12) | HTML cap. 1, M7 + bloque JS | M | 2 |
| 3b | **Cierre del círculo con el M5**: la lectura del simulador nombra que grado 0 + pesos planos **es** la media móvil, con las dos cifras (5.5436 y 5.5427), y el puente de la tarea 1 remite al simulador (D13) | HTML cap. 1, M5 y M7 | XS | 1, 3 |
| 4 | **`.derivacion` plegable**: el estimador de mínimos cuadrados ponderados, de dónde salen los 19 puntos de la ventana y por qué `s.degree = 0` frente a `t.degree = 1` (D9) | HTML cap. 1, M7 | S | 2 |
| 5 | **El bucle robusto**: prosa del bucle interno/externo más la tabla de pesos bicuadrados sobre la obs. 79, con remisión explícita al Ejercicio 3 y desde él (D7) | HTML cap. 1, M7 y cierre | S | 2 |
| 6 | **Reparación C6**: comprobar primero la equivalencia `trend(window = n)` ⟷ `t.window = n` con `fable` instalado; después `trend(window = 21)` → `19` y la frase que lo justifica | HTML cap. 1, M7 pestaña R | XS | 4 |
| 7 | **Retoques de coherencia**: las tres viñetas de ventajas pasan a remitir al mecanismo en vez de afirmarlo; el aviso de `s.window = "periodic"` se reescribe en términos del span | HTML cap. 1, M7 | XS | 2, 5 |
| 8 | **Verificación** en navegador y cotejo con R | — | XS | 1–7 |
| 9 | **Documentación en el vault**: bitácora, actualización de [[20948-01 Componentes y descomposición]] y registro de este plan | `Vault/Bitacora/`, `Vault/Capitulos/` | S | 8 |

### Checkpoint · tras las tareas 1–4

- [ ] El estudiante puede decir qué ajusta Loess, sobre qué vecindario y con qué pesos
- [ ] El simulador se registra y sus gráficos se destruyen al salir del módulo
- [ ] El `.derivacion` abre y cierra, y KaTeX renderiza dentro del panel plegado

### Criterios de aceptación

- [ ] Las tres ventajas del M7 quedan **derivadas** del mecanismo, no afirmadas (C2)
- [ ] El span está nombrado y `s.window` / `window` explicados a partir de él (C3)
- [ ] El Ejercicio 3 tiene su mecanismo en el cuerpo del capítulo, no en un comentario de R (C4)
- [ ] El simulador muestra la media móvil **desapareciendo** en los extremos mientras la recta local sigue
- [ ] Grado 0 + pesos planos **reproduce la media móvil del M5** en el propio simulador (D13a)
- [ ] El sesgo por grado se enuncia como lo que se midió: 0.0000 en el centro y 0.0498 en
      diciembre de 1960, con el grado 1 clavando `stl()` (D13b)
- [ ] La ventana toma los $span$ puntos **más próximos** y se desplaza en los bordes, no se
      trunca. Es lo que separa un Loess de verdad de la aproximación que invalidó D6 y D13 (D14)
- [ ] La diferencia entre el Loess del simulador y el de `stl()` está **medida** (D6)
- [ ] La equivalencia `trend(window=)` ⟷ `t.window` está **comprobada**, no supuesta, antes de la tarea 6
- [ ] El código de la pestaña R reproduce las cifras que cita la prosa (C6)
- [ ] Ninguna cifra nueva escrita a mano; todas salen de `stl()` y están verificadas
- [ ] El párrafo de cierre del M5 sigue siendo la transición al M6, sin desplazar (D3)
- [ ] Consola sin errores ni `Simulador no registrado`
- [ ] Prosa en voz impersonal y «el componente» en masculino ([[series-tiempo-convenciones-prosa]])

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El Loess en JS no coincide con `stl()` y el simulador «miente» | **Cerrado** | Medido: **0.0045** de desvío máximo en los 144 meses, y la tendencia de `stl()` se dibuja al lado para que se vea. El riesgo era real pero no se materializó — lo que sí falló fue la comprobación previa, ver la fila siguiente |
| Verificar el método con una aproximación en vez de con el método | **Alto, y ya mordió** | La comprobación en R que sostenía D6 y D13 truncaba la ventana en los bordes en vez de desplazarla, y las dos decisiones salieron invertidas (D14). Regla: cuando la cifra vaya a decidir un diseño, el guion de R tiene que replicar **la misma regla** que el código que se va a escribir, y contrastarse contra él |
| El puente del M5 pisa la transición hacia el M6 | Medio | D3: se engancha al párrafo de la pérdida de extremos, dos párrafos antes del cierre, que no se toca |
| El M7 ya carga con un simulador de 4 paneles; añadir otro lo recarga | Medio | El nuevo va **antes** y es de un solo panel. El M7 dura hoy 10 min declarados; habrá que revisar la cifra |
| `Object.assign` de `crearGraficoLinea` es superficial: pasar `scales` o `plugins` los reemplaza enteros | Medio | Reespecificar las fuentes en cada `scales` que se pase. Ya mordió en el M3 y en la ronda de los gráficos |
| Tocar `trend(window = 21)` es contenido existente fuera del alcance estricto | Bajo | D10 **confirmado**. Es la única tarea del plan que modifica algo que hoy funciona, y la tarea 6 lo condiciona a comprobar antes la equivalencia con `fable`, que aquí no se pudo verificar |
| Un tercer y cuarto control recargan el simulador | Medio | Los tres van en la misma fila de controles y el de pesos es un interruptor, no un deslizador. Si el módulo queda pesado, el que se sacrifica es el de grado: el de pesos es el que sostiene D13 |
| Crecimiento del archivo (hoy 234 KB) | Bajo | Es una medida, no un presupuesto ([[Criterio de contenido]]). Sin datos nuevos incrustados |

## 7. Preguntas abiertas — RESUELTAS (2026-08-17)

1. **¿Se confirma D10?** → **Sí.** `trend(window = 21)` se corrige a `19`. Condicionado a
   comprobar antes la equivalencia `trend(window=)` ⟷ `t.window` con `fable` instalado, que
   en esta máquina no se pudo verificar (tarea 6).
2. **¿El simulador lleva control de grado?** → **Sí**, y además de pesos (D12). Con una
   corrección sobre el motivo que se argumentó al preguntarlo: al medirlo, el sesgo por grado
   en los extremos **no** es el fenómeno limpio que se prometió —0.0246 en $t=1$ pero −0.0017
   en $t=144$—. El titular del control pasa a ser la identidad con la media móvil, que sí está
   limpia (5.5436 contra 5.5427), y el grado se enseña como lo que la medición dice: solo
   importa donde la ventana es de un lado *y* la serie tiene pendiente local (D13).

No quedan preguntas abiertas. El plan está listo para la tarea 1.

## 8. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Rondas anteriores sobre el mismo capítulo: [[PLAN_Graficos_Aditivo_Multiplicativo]] · [[PLAN_Formalizacion_Descomposicion]]
- Capítulo: [[20948-01 Componentes y descomposición]]
- Criterio que motiva la ronda: [[Criterio de contenido]]
- Bitácora: [[2026-08-17]]
