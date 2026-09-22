---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-09-22
estado: ejecutado
---

# Plan — Los momentos del AR($p$) en el Módulo 2 del Capítulo 3

**Objetivo:** que el M2 escriba la **varianza** y las **autocorrelaciones** de un AR($p$),
que no aparecían por ninguna parte, con las mismas fórmulas cerradas que el M3 ya da para
el MA($q$).

**Alcance:** una sección nueva dentro del M2, un paso más en su derivación de
Yule–Walker y la ampliación de sus dos bloques de código. Nada fuera del M2.

## 1. El hueco

El encargo fue literal: «en el módulo 2 no se habla de varianza ni autocorrelación de un
AR($p$), ni hay fórmulas». Comprobado línea a línea, y es exacto. El módulo definía el
proceso, daba la firma cualitativa de la PACF, el triángulo de estacionariedad y la
recursión de Yule–Walker **dentro de una caja de derivación plegada**, y nada más.

| # | Carencia | Dónde se notaba |
|---|---|---|
| C1 | **La varianza $\gamma_0$ no se escribía nunca** | El M3 sí da $\gamma_0 = \sigma^2(1+\sum\theta_j^2)$ para el MA($q$) en una caja `.formula`; el AR no tenía equivalente |
| C2 | **No había forma cerrada de la ACF** | La prosa decía «son las potencias de $0.8$» sin escribir $\rho_k = \phi^k$ |
| C3 | **La derivación de Yule–Walker excluía $k = 0$** | Sus cuatro pasos exigían $k \ge 1$ «para que el ruido se anule»: justo el caso que produce la varianza |
| C4 | **El M7 cita una ecuación que el capítulo no tiene** | El aviso «no compares un $\hat\sigma^2$ de Yule–Walker con uno de ML» dice que el primero sale «de la ecuación de la varianza del proceso». Esa ecuación no estaba escrita en ningún módulo |
| C5 | **El triángulo del M2 era solo álgebra de raíces** | Nada conectaba sus tres lados con que la varianza se vuelva infinita |

C4 es el que mejor mide el hueco: un módulo posterior se apoyaba en una fórmula que el
lector nunca había visto.

## 2. Restricciones verificadas antes de planear

- **El capítulo 3 tiene generador** y es reproducible byte a byte: se edita
  `ensamblado/cap3/cap3_modulos.html`, no el HTML publicado. Ver
  [[series-tiempo-riesgo-reensamblado]]. Comprobado antes de tocar nada
  (`ensambla_cap3.py` sin argumentos: «reproducible»).
- **`ensambla_cap4.py` lee el capítulo 3 como base**, así que la cadena 4 → 5 → 6 se
  reejecuta y se comprueba que deja esos tres capítulos idénticos.
- **Ninguna cifra se escribe a mano** (`Vault/Estandar/Criterio de contenido.md`).
- **Se verifica por HTTP, no por `file://`** ([[verificar-html-por-http-no-file]]).

## 3. Decisiones de esta ronda

- **D1 · La sección va después del triángulo, no antes.** Así la varianza del AR(2) puede
  decir que su denominador **son** las tres desigualdades del triángulo, y el orden de
  lectura no obliga a adelantar nada.
- **D2 · Dos cajas `.formula`, no una.** La primera da los tres momentos del AR($p$)
  general —$\mu$, $\gamma_0$ y la recursión—; la segunda, las formas cerradas del AR(1) y
  del AR(2), que son los dos órdenes que el capítulo usa de verdad.
- **D3 · La $\gamma_0$ del AR se escribe en función de las $\rho_k$**, no de los $\phi$.
  Para $p$ general no hay forma cerrada corta, y decir en voz alta que el orden de cálculo
  es obligatorio —primero la recursión, después la varianza— es justamente el contraste con
  el MA, donde no lo es.
- **D4 · El paso $k = 0$ entra en la derivación existente**, como quinto paso, en vez de
  abrir una caja nueva. La cuenta es la misma; lo único que cambia es que el término del
  ruido ya no se anula.
- **D5 · La varianza del AR(2) se da en las dos formas**, con el corchete y factorizada.
  La factorizada es la que hace visible el triángulo.
- **D6 · Fórmulas repartidas en líneas.** La primera versión del bloque del AR(2)
  desbordaba su caja en escritorio; partida en `gathered` + `aligned`, las cuatro cajas del
  módulo miden `scrollWidth == clientWidth`. El desborde en móvil es anterior a esta ronda
  y se deja como estaba, igual que en la ronda del M9.

## 4. Cifras verificadas en R antes de escribir

Con `phi <- c(0.5, 0.3)` y $\sigma^2 = 1$, que es el AR(2) que el módulo ya usaba:

| Cantidad | Camino | Valor |
|---|---|---|
| $\rho_1,\rho_2$ | `ARMAacf(ar = phi, lag.max = 2)` | $0.7143$, $0.6571$ |
| $\gamma_0$ | $\sigma^2\sum_j\psi_j^2$ con `ARMAtoMA`, 2000 términos | $2.24359$ |
| $\gamma_0$ | Yule–Walker, $\sigma^2/(1-\sum\phi_k\rho_k)$ | $2.24359$ |
| $\gamma_0$ | Forma cerrada del AR(2) | $2.24359$ |
| $\gamma_0$ del AR(1) $\phi = 0.8$ | Suma de $\psi^2$ / $\sigma^2/(1-\phi^2)$ | $2.77778$ en los dos |
| $\gamma_0$ del AR(2) $(1.4,-0.75)$ | Suma de $\psi^2$ / forma cerrada | $6.34921$ en los dos |
| $\rho_k$ de $\phi = 0.8$ y $\phi = -0.7$ | `ARMAacf` | $0.800, 0.640, 0.512$ · $-0.700, 0.490, -0.343$ |

Los tres caminos a $\gamma_0$ coinciden a cinco cifras, que es lo que autoriza a escribir
la fórmula general y las dos cerradas en la misma caja. Lo mismo en Python con
`arma_acf` de statsmodels: $2.2436$ por los dos caminos.

## 5. Tareas

| # | Tarea | Tamaño | Depende de |
|---|---|---|---|
| T1 | Sección «Media, varianza y autocorrelación» con las dos cajas `.formula` | M | D1, D2, D3 |
| T2 | Prosa: $\rho_k = \phi^k$ explica las cifras del simulador; $\gamma_0$ crece al acercarse a 1 | S | T1 |
| T3 | Nota «El denominador es el triángulo» | S | T1, D5 |
| T4 | Quinto paso ($k = 0$) en la derivación de Yule–Walker | M | D4 |
| T5 | Cierre de la derivación: $\gamma_0 = 2.244\,\sigma^2$ para el ejemplo corriente | S | T4, §4 |
| T6 | Bloques R y Python: varianza por los dos caminos | M | §4 |
| T7 | Objetivo del módulo, que prometía solo firma y estacionariedad | S | T1 |
| T8 | Reensamblar, verificar la cadena 4 → 5 → 6 y comprobar en el navegador | M | T1–T7 |

## 6. Criterios de aceptación

- `ensambla_cap3.py` vuelve a decir **reproducible byte a byte**, y la cadena 4 → 5 → 6
  deja los otros tres capítulos sin cambios en `git status`.
- Las diferencias contra el archivo anterior caen **todas** dentro del M2.
- Cero `.katex-error` en el módulo; las cuatro cajas `.formula` no desbordan en escritorio.
- Las cifras impresas en los bloques de código son las de §4, pegadas de una ejecución.
- `cuenta_sitio.py` en verde.

## 7. Riesgos

- **Repetir al M3 en vez de contrastarlo.** El MA da su varianza en función de sus propios
  parámetros y el AR no puede; si la sección no dice eso, parecen la misma fórmula mal
  escrita. Mitigado con el párrafo de D3.
- **Adelantar Yule–Walker.** La caja de fórmulas llega antes que la derivación que la
  justifica. Mitigado enlazando las dos con la frase de apertura de la sección siguiente,
  que pasa de «¿de dónde sale la ACF teórica?» a «¿de dónde salen esas fórmulas?».
- **Duplicar el M1.** El M1 ya obtiene $\sigma^2/(1-\phi^2)$ sumando la serie geométrica
  del MA($\infty$). Se deja dicho en el paso nuevo que es el mismo resultado por otro
  camino, en vez de fingir que es nuevo.

## 8. Enlaces

- Capítulo: [[20948-03 Modelos AR, MA y ARMA]]
- Bitácora: [[2026-09-22]]
- Ronda anterior del mismo día: [[PLAN_Cierre_Algebraico_M9]]
- Auditoría módulo por módulo: [[PLAN_Auditoria_Cap3]]
