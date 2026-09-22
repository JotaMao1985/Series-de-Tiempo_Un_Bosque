---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-09-22
estado: ejecutado
---

# Plan — Los momentos del ARMA($p,q$) en el Módulo 5 del Capítulo 3

**Objetivo:** cerrar la serie que abrió [[PLAN_Momentos_AR]]. El M2 ya escribe los momentos
del AR($p$) y el M3 los del MA($q$); el M5 no escribía los del ARMA.

**Alcance:** una sección nueva dentro del M5, una caja de derivación, la corrección de una
fórmula publicada sin su condición y la ampliación de sus dos bloques de código. Nada fuera
del M5.

## 1. El hueco

Era el pendiente que dejó anotado la ronda anterior, y el encargo fue literal: «ahora haz
lo mismo con el ARMA($p,q$) del módulo 5».

| # | Carencia | Dónde se notaba |
|---|---|---|
| C1 | **La media del ARMA no se escribía** | El M2 la da para el AR; el M5 definía el proceso con $c$ y nunca dijo qué vale $\mu$ |
| C2 | **La varianza tampoco** | Tercer módulo de la serie sin su $\gamma_0$, después de arreglar los otros dos |
| C3 | **No había autocovarianza general** | El módulo daba $\rho_k$ para $k > q$ y $\rho_1$ del ARMA(1,1); los rezagos $2 \le k \le q$ de un ARMA cualquiera no estaban cubiertos por nada |
| C4 | **La recursión se publicaba sin su condición** | La caja decía $\rho_k = \phi_1\rho_{k-1}+\cdots$ a secas. La prosa de encima sí enunciaba el $k > q$, pero la fórmula —que es lo que se copia— no lo llevaba |
| C5 | **Un denominador sin origen** | La $\rho_1$ del ARMA(1,1) trae un $1+2\phi\theta+\theta^2$ que el módulo usaba sin decir qué es. Es la varianza del proceso, salvo el factor $\sigma^2/(1-\phi^2)$ |

C4 es un defecto, no una carencia: la fórmula publicada era falsa para $k \le q$ y nada en
la caja lo advertía.

## 2. Restricciones verificadas antes de planear

- **Se edita `ensamblado/cap3/cap3_modulos.html`**, no el HTML publicado
  ([[series-tiempo-riesgo-reensamblado]]). Comprobado «reproducible» antes de tocar nada.
- **`ensambla_cap4.py` parte del capítulo 3**, así que la cadena 4 → 5 → 6 se reejecuta y se
  comprueba que no arrastra nada del M5 nuevo.
- **Otra sesión estaba trabajando en el mismo árbol** ([[sesiones-concurrentes-mismo-arbol]]).
  Ver §7.
- **Ninguna cifra a mano**; verificación **por HTTP** ([[verificar-html-por-http-no-file]]).

## 3. Decisiones de esta ronda

- **D1 · La autocovarianza general va por los $\psi$**, no por los $\phi$ y $\theta$. Para
  $p \ge 1$ no existe forma corta en función de los parámetros, y decirlo es la mitad del
  contenido: el ARMA es el primero de los tres que no se deja escribir así.
- **D2 · La sección va después de la tabla de identificación**, no antes. El Objetivo del
  módulo es identificar; la teoría entra cuando toca explicar por qué la tabla falla, y
  entonces los momentos son el preámbulo natural de esa explicación.
- **D3 · Del ARMA(1,1) se dan $\gamma_0$ y $\gamma_1$, no $\rho_1$.** La $\rho_1$ ya estaba
  en el módulo; repetirla habría sido duplicar. Dando las dos autocovarianzas con su
  denominador común, el lector ve que al dividirlas sale la que ya conocía — y de paso se
  resuelve C5.
- **D4 · El contraejemplo de C4 se calcula, no se enuncia.** Decir «la recursión no vale
  para $k \le q$» es una regla más que memorizar; enseñar que daría $0.8$ donde el valor es
  $0.8614$ la vuelve comprobable.
- **D5 · Caja de derivación nueva**, la séptima del capítulo. El M5 no tenía ninguna, y la
  cuenta —emparejar choques iguales dentro de la MA($\infty$)— es corta y explica de una vez
  las tres fórmulas.
- **D6 · El caso $p = 0$ se menciona como suma vacía.** Que el corte exacto de la ACF de un
  MA salga de que los productos $\psi_j\psi_{j+k}$ llevan factor nulo es el mejor argumento
  de que la fórmula general es la buena.

## 4. Cifras verificadas en R antes de escribir

Con el ARMA(1,1) de $\phi = 0.7$, $\theta = 0.5$ y $\sigma^2 = 1$, que es el que el capítulo
arrastra desde el M4:

| Cantidad | Camino | Valor |
|---|---|---|
| $\gamma_0$ | $\sigma^2\sum\psi_j^2$, 4000 términos | $3.823529$ |
| $\gamma_0$ | Forma cerrada $(1+2\phi\theta+\theta^2)/(1-\phi^2)$ | $3.823529$ |
| $\gamma_1$ | $\sigma^2\sum\psi_j\psi_{j+1}$ | $3.176471$ |
| $\gamma_1$ | Forma cerrada $(1+\phi\theta)(\phi+\theta)/(1-\phi^2)$ | $3.176471$ |
| $\rho_1$ | $\gamma_1/\gamma_0$ | $0.830769$, la cifra que ya publicaba el módulo |
| $\psi_j$ | `ARMAtoMA` frente a $(\phi+\theta)\phi^{j-1}$ | $1.2,\,0.84,\,0.588,\,0.4116$ en los dos |

Casos límite, que son la comprobación de que la fórmula general contiene a las otras dos:

| Proceso | $\sigma^2\sum\psi_j^2$ | Fórmula del módulo correspondiente |
|---|---|---|
| AR(1), $\phi = 0.8$ | $2.777778$ | $\sigma^2/(1-\phi^2) = 2.777778$ (M2) |
| MA(1), $\theta = 0.5$ | $1.25$ | $\sigma^2(1+\theta^2) = 1.25$ (M3) |
| ARMA(1,1) redundante, $0.5/-0.5$ | $1$ | Ruido blanco, como dice el final del módulo |

Y el contraejemplo de C4, con el ARMA(2,1) de $\phi = (0.5,\,0.3)$ y $\theta = 0.4$: la
recursión reproduce $\rho_2$ a $\rho_5$ —$0.7307$, $0.6238$, $0.5311$, $0.4527$— y aplicada
a $\rho_1$ da $0.8$ frente al verdadero $0.8614$.

## 5. Tareas

| # | Tarea | Tamaño | Depende de |
|---|---|---|---|
| T1 | Sección «Media, varianza y autocorrelación» con la caja general | M | D1, D2 |
| T2 | Nota de los casos $q = 0$ y $p = 0$ | S | T1, D6 |
| T3 | Caja cerrada del ARMA(1,1) con $\gamma_0$ y $\gamma_1$, y el párrafo de C5 | M | D3 |
| T4 | Caja de derivación desde la MA($\infty$) | M | D5 |
| T5 | Añadir $k > q$ a la fórmula publicada y escribir el contraejemplo | S | D4, §4 |
| T6 | Bloques R y Python: varianza por los dos caminos y el contraejemplo | M | §4 |
| T7 | Objetivo del módulo, que solo prometía identificar | S | T1 |
| T8 | Reensamblar, cadena 4 → 5 → 6 y comprobación en el navegador | M | T1–T7 |

## 6. Criterios de aceptación

- `ensambla_cap3.py`, **reproducible byte a byte**; la cadena 4 → 5 → 6 sin cambios en
  `git status`.
- Las diferencias contra el archivo anterior caen **todas** dentro del M5.
- Cero `.katex-error`; las **cinco** cajas `.formula` del módulo sin desbordar en escritorio.
- La derivación abre y trae sus cinco pasos.
- Las cifras de los bloques de código son las de §4, pegadas de una ejecución.
- `cuenta_sitio.py` en verde.

## 7. Riesgos

- **Duplicar la $\rho_1$ que el módulo ya tenía.** Mitigado con D3: se dan las
  autocovarianzas y se deja el cociente como enlace entre las dos secciones.
- **Romper el hilo de identificación.** El módulo es el de la tabla, y meterle teoría por el
  medio puede enterrar su Objetivo. Mitigado con D2, colocando la sección donde la teoría ya
  hacía falta.
- **Sesión concurrente en el mismo árbol.** Mientras se escribía esta ronda, otra sesión
  commiteó cuatro veces sobre los capítulos 4, 5 y 6
  ([[PLAN_Casos_Aplicados_456]]). Reejecutar aquí la cadena 4 → 5 → 6 regeneró **sus**
  capítulos desde **sus** fuentes ya commiteadas y el resultado salió idéntico, así que no
  hubo pérdida; pero la comprobación que lo demostró fue `git status`, no la suposición.
  Verificado además que ninguno de sus cuatro commits toca el capítulo 3, que es lo que
  autorizaba a commitear esta ronda sin fusionar nada.

## 8. Enlaces

- Capítulo: [[20948-03 Modelos AR, MA y ARMA]]
- Bitácora: [[2026-09-22]]
- Ronda que abrió la serie: [[PLAN_Momentos_AR]]
- Ronda paralela de otra sesión: [[PLAN_Casos_Aplicados_456]]
