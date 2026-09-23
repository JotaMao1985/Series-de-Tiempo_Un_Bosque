---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-05 Modelos SARIMA]]"
fecha: 2026-09-22
estado: ejecutado
---

# Plan — La varianza del SARIMA en el Capítulo 5

**Objetivo:** el encargo fue una auditoría —«mira si el SARIMA del capítulo 5 escribe su
varianza»— y la respuesta fue que no, en ninguna parte. Este plan cubre los tres arreglos
que el usuario autorizó después de leerla.

**Alcance:** una sección nueva en el M2, un párrafo y un aviso en el M4, y un símbolo
renombrado en el M10. Nada más del capítulo.

## 1. El hueco

| # | Carencia | Dónde se notaba |
|---|---|---|
| C1 | **La varianza no se escribe en ningún sitio** | Cero apariciones de `gamma_0` en los once módulos |
| C2 | **Una sola caja `.formula` en todo el capítulo** | Y es el *airline* ya ajustado, no una fórmula de momentos. Cap. 1 tiene 13; cap. 3, 23; cap. 5, una |
| C3 | **El motor usa la fórmula y no la enseña** | `acfDesdePsi()` lleva el comentario `gamma_k = sigma^2 * sum psi_j psi_{j+k}`, que el lector nunca ve. El capítulo ejecuta lo que no explica |
| C4 | **El «aproximadamente» de la tabla de satélites no distingue** | Tres filas descritas por igual: la del *airline* es exacta hasta el último decimal de la máquina; las otras dos, que llevan parte AR, solo se parecen |
| C5 | **Colisión de notación** | En el M10, $\gamma_k$ es el coeficiente del coseno de los términos de Fourier. Choca con la autocovarianza del resto del material, y el choque empeoró al hacerla prominente en el cap. 3 |

C4 y C5 son defectos; C1–C3 son carencias.

## 2. Restricciones verificadas antes de planear

- **Se editan las fuentes de `ensamblado/cap5/`**, no el HTML publicado
  ([[series-tiempo-riesgo-reensamblado]]). Reproducibilidad comprobada byte a byte antes de
  tocar nada: `ensambla_cap5.py` y `ensambla_cap6.py` reescribieron sus capítulos idénticos.
- **`ensambla_cap5.py` no tiene modo de solo verificar**: escribe siempre. De ahí la copia
  de seguridad previa de los cuatro capítulos de la cadena.
- **El script cuenta las derivaciones y los ejercicios** (3 y 3) y aborta si el número
  cambia. Eso descartó añadir una caja de derivación, y es la razón de D4.
- **Ninguna cifra a mano**; verificación **por HTTP** ([[verificar-html-por-http-no-file]]).

## 3. Decisiones de esta ronda

- **D1 · La sección va en el M2, no en el M5 ni en el M7.** El M2 es donde vive la
  derivación del polinomio multiplicativo, y los momentos son consecuencia directa de esa
  expansión. En el M5 habrían competido con los pesos $\psi$ del *airline*; en el M7, con el
  caso aplicado.
- **D2 · Se abre con la advertencia de $d = D = 0$, no se cierra con ella.** Preguntar por
  la varianza del *airline* tal como se escribe no significa nada: el modelo tiene dos
  raíces unitarias. La serie con momentos es $w_t = \nabla^d\nabla_m^D y_t$, y decirlo
  después de dar las fórmulas habría invitado a aplicarlas mal.
- **D3 · El contenido nuevo es la factorización, no las fórmulas generales.** $\gamma_k =
  \sigma^2\sum\psi_j\psi_{j+k}$ ya está publicada en el M5 del cap. 3 ([[PLAN_Momentos_ARMA]]);
  repetirla sola no valía una sección. Lo que justifica escribirla es lo que se factoriza y
  lo que no.
- **D4 · Sin caja de derivación.** El ensamblador aborta si el capítulo no tiene exactamente
  tres. El argumento —los rezagos del MA no se pisan y los del AR sí— es de una frase y cabe
  en prosa.
- **D5 · El peaje se tabula, no se enuncia.** «La factorización del AR es aproximada» es una
  advertencia que nadie recuerda; cuatro filas con el error creciendo del $0.3\,\%$ al
  $54.9\,\%$ se leen una vez y se quedan.
- **D6 · El M4 recibe el resultado, no la demostración.** Allí importa para identificar, y
  para identificar la distinción es invisible: entre $0.42298$ y $0.42180$ no hay
  correlograma estimado que decida. El aviso dice exactamente eso y remite al M2.
- **D7 · El coeficiente de Fourier pasa a $\delta_k$**, no a $b_k$ ni a $\beta_k$. $\beta_0$
  ya es el intercepto de esa misma ecuación y $\alpha_k$ es el coeficiente del seno;
  $\delta$ no aparecía en ninguna de las cuatro plantillas del capítulo.

## 4. Cifras verificadas en R antes de escribir

**El regalo.** MA multiplicativo con $q < m$:

| Cantidad | Camino | Valor |
|---|---|---|
| $\gamma_0/\sigma^2$ del *airline* | $\sum\psi_j^2$ sobre el polinomio expandido | $1.521650470604$ |
| $\gamma_0/\sigma^2$ del *airline* | $(1+\theta^2)(1+\Theta^2)$ | $1.521650470604$ |
| Diferencia | — | $0$ a precisión de máquina |
| $\gamma_0$ con $\hat\sigma^2 = 0.001371$ | Teórica de $\nabla\nabla_{12}\log y_t$ | $0.002087$ |
| Varianza muestral de $\nabla\nabla_{12}\log y_t$ | $n = 131$ | $0.002102$ |
| $\rho_{11} = \rho_{13} = \rho_1\rho_{12}$ | *Airline* | $0.1470524436$, las tres |

Regla del producto $\rho_{i+jm} = \rho^{\text{reg}}_i\rho^{\text{est}}_j$, probada además en
un MA(2)$\times$SMA(2)$_{12}$: exacta en los doce rezagos comprobados, error máximo
$1.1\times10^{-16}$. Y el límite: con $q = m$ los rezagos chocan y se rompe —$\theta_{12} =
0.5$, $\Theta = 0.6$ dan $2.300\,\sigma^2$ frente a los $1.700\,\sigma^2$ de la
factorización—.

**El peaje.** AR($1$)$\times$SAR($1$)$_{12}$ con $\Phi = 0.7$:

| $\phi$ | $\phi^{12}$ | Exacta | Factorizada | Error |
|---|---|---|---|---|
| $0.6$ | $0.002$ | $3.073$ | $3.064$ | $-0.3\,\%$ |
| $0.8$ | $0.069$ | $5.997$ | $5.447$ | $-9.2\,\%$ |
| $0.9$ | $0.282$ | $15.406$ | $10.320$ | $-33.0\,\%$ |
| $0.95$ | $0.540$ | $44.580$ | $20.111$ | $-54.9\,\%$ |

Causa comprobada exactamente: $\psi_{11} = \phi^{11}$, $\psi_{12} = \phi^{12} + \Phi$,
$\psi_{13} = \phi^{13} + \phi\Phi$. El término de colisión es $\phi^m$.

**Las cinco filas de la tabla del M4** se recalcularon y reproducen las publicadas. La
media, $\mu = c/[\phi_p(1)\Phi_P(1)]$, se contrastó por simulación: $16.6667$ teórica contra
$16.6618$ en $400\,000$ observaciones.

**El divisor de $\hat\sigma^2$.** `forecast::Arima` informa $\text{SSR}/(n-2) = 0.00137126$ y
`statsmodels` el de máxima verosimilitud, $0.00134803$. De ahí que el bloque de R diga
$0.002087$ y el de Python $0.002051$ para la misma varianza teórica. Comprobado que la
diferencia es exactamente el reparto de grados de libertad, y anotado en el propio código
para que no parezca un error.

## 5. Tareas

| # | Tarea | Tamaño | Depende de |
|---|---|---|---|
| T1 | Sección «Media, varianza y autocorrelación» en el M2 | L | D1, D2, D3 |
| T2 | Caja de la factorización exacta y su condición $q < m$ | M | §4 |
| T3 | Nota del *airline* como caso exacto | S | T2 |
| T4 | Tabla del peaje del AR y la causa $\psi_{12} = \phi^{12}+\Phi$ | M | D5, §4 |
| T5 | Bloques R y Python, con la nota del divisor | M | §4 |
| T6 | M4: distinguir exacto de aproximado, y aviso de dónde importa | M | D6 |
| T7 | M10: $\gamma_k \rightarrow \delta_k$ | S | D7 |
| T8 | Objetivo del M2, que no prometía momentos | S | T1 |
| T9 | Reensamblar, cadena 5 → 6 y comprobación en el navegador | M | T1–T8 |

## 6. Criterios de aceptación

- La cadena 5 → 6 **reproducible byte a byte** antes de tocar nada, y después con el
  capítulo 6 idéntico.
- Los capítulos 3 y 4 sin cambios en `git status`.
- Las diferencias caen **todas** en los módulos 2, 4 y 10.
- Cero `.katex-error`; ninguna caja `.formula`, `.note`, `.warning` o `.diagram` desbordando
  a $1280$ px, medido con `scrollWidth` contra `clientWidth`.
- Cero `$…$` sin renderizar en el contenido nuevo.
- `\gamma` no vuelve a aparecer como coeficiente de Fourier en las fuentes.
- Las cifras de los bloques de código, pegadas de una ejecución.
- `cuenta_sitio.py` en verde.

## 7. Riesgos

- **El ensamblador escribe siempre.** A diferencia de `ensambla_cap3.py`, no tiene
  `--escribir`. Mitigado copiando los cuatro capítulos de la cadena antes de ejecutarlo y
  comparando después.
- **Las cuentas duras del script.** Tres derivaciones y tres ejercicios exactos. Mitigado
  con D4: la sección no añade ninguna de las dos cosas.
- **Sesión concurrente en el mismo árbol** ([[sesiones-concurrentes-mismo-arbol]]). El
  capítulo 5 es justamente el que la otra sesión tocó en `3d84a7a`, sobre
  `templates_7_9.html`. Esta ronda toca `templates_1_3.html`, `templates_4_6.html` y
  `templates_10_11.html`: ningún archivo en común. Comprobado antes de commitear, no
  supuesto.
- **Publicar una regla más fuerte de lo que es.** La factorización exacta vale con $q < m$ y
  se rompe en cuanto $q$ alcanza a $m$. Mitigado escribiendo la condición dentro de la caja
  y dando el contraejemplo numérico en la prosa.

## 8. Enlaces

- Capítulo: [[20948-05 Modelos SARIMA]]
- Bitácora: [[2026-09-22]]
- Fórmula general que esta ronda reutiliza: [[PLAN_Momentos_ARMA]]
- Serie que la abrió: [[PLAN_Momentos_AR]]
- Ronda de otra sesión sobre el mismo capítulo: [[PLAN_Casos_Aplicados_456]]
