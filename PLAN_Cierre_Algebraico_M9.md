---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-09-22
estado: ejecutado
---

# Plan — El cierre algebraico del Módulo 9 del Capítulo 3

**Objetivo:** que el caso de las manchas solares, que es el ejemplo aplicado del capítulo,
use también la **primera mitad** del capítulo —operador de rezago, invertibilidad y pesos
$\psi$— y no solo la segunda.

**Alcance:** dos tramos nuevos dentro del Caso 1 del M9, un simulador y la ampliación de
los dos bloques de código. Nada fuera del M9.

## 1. El hueco

La pregunta que abrió la ronda fue si el capítulo 3 tiene un ejemplo aplicado que recopile
lo visto en **todo** el capítulo. La respuesta corta era «casi»: el M9 cierra un hilo que
arranca en el M7 («la serie que nos acompañará el resto del capítulo») y recorre M7 → M8 →
M9 → M10, pero de los módulos 1 a 6 apenas entra la tabla de identificación del M5.

| # | Módulo | Qué enseñó | Dónde se aplicaba en el M9 |
|---|---|---|---|
| C1 | M1 · Operador de rezago | $\phi(B)$, raíces y círculo unitario | En ninguna parte; solo «raíces complejas de módulo 1.208», sin polinomio |
| C2 | M3 · MA e invertibilidad | Condición sobre $\theta(B)$ | La palabra no aparecía en el módulo |
| C3 | M4 · Dualidad y pesos $\psi$/$\pi$ | Respuesta al impulso y varianza del pronóstico | Una mención de paso |
| C4 | M5 · Redundancia de parámetros | Factor común entre $\phi(B)$ y $\theta(B)$ | No se comprobaba en el ARMA(2,1) que el módulo descarta |
| C5 | Cierre del caso | — | Nada decía, al terminar, cuánto del capítulo había hecho falta |

C4 es el más interesante de los cinco: el módulo concluye que al ARMA(2,1) «le sobraba un
parámetro», y un lector puede suponer que eso se ve en el modelo. No se ve.

## 2. Restricciones verificadas antes de planear

- **El capítulo 3 tiene generador** y es reproducible byte a byte: se edita
  `ensamblado/cap3/`, no el HTML publicado. Ver [[series-tiempo-riesgo-reensamblado]].
  Comprobado antes de tocar nada (`ensambla_cap3.py` sin argumentos: «reproducible»).
- **La cadena 3 → 4 → 5 → 6** tiene que seguir reproduciendo los otros tres capítulos.
- **`ensambla_cap3.py` lleva una lista blanca de simuladores**: añadir uno obliga a
  registrarlo en las dos listas de `obligatorios` o el ensamblado no lo exige.
- **`precalculo/cuenta_sitio.py` contrasta las cifras anunciadas** en la portada y en el
  README contra el marcado. Un simulador nuevo las descuadra las ocho.
- **`DATOS_CAP3` ya trae lo necesario** —`manchas.transformacion.sqrt` tiene `phi1`,
  `phi2`, `sigma2` y `periodo`—, así que los $\psi$ se calculan en el navegador con
  `pesosPsi()`, la función que ya usan el simulador del M4 y la ACF teórica. **No hace
  falta regenerar el JSON.**

## 3. Decisiones de esta ronda

- **D1.** Los dos tramos van **dentro del Caso 1**, entre la nota de Guerrero y el aviso
  sobre la normalidad. Así, cuando ese aviso dice que «los intervalos del Capítulo 6
  quedarán algo mal calibrados», los intervalos acaban de construirse tres párrafos antes.
- **D2.** El ángulo de la raíz se presenta como **el origen del pseudo-periodo**, no como
  un dato más: el $11.22$ que el módulo ya leía como «el ciclo solar» es $2\pi/\omega$.
  Es la pieza que faltaba para que el M1 y el M2 se toquen sobre datos reales.
- **D3.** Se comprueba explícitamente que el ARMA(2,1) de la serie cruda **era invertible y
  no tenía factor común** (C4). La moraleja del módulo se refuerza en vez de debilitarse:
  un parámetro puede estar bien estimado y aun así sobrar.
- **D4.** Las cifras de la prosa salen del ajuste a precisión plena; las del simulador, de
  los $\phi$ redondeados de `DATOS_CAP3`. Difieren en la cuarta cifra, así que **la lectura
  del simulador imprime dos decimales** en todo lo que también está en la tabla. Nada en
  pantalla se contradice.
- **D5.** El M6 entra en la tabla de cierre **declarando que no entra en ninguna cuenta**.
  Mentir por simetría habría sido peor que dejar el hueco.

## 4. Cifras verificadas en R antes de escribir

Todas contra R 4.6.0 (`stats`, `forecast`) y statsmodels 0.14.6, sobre
`arima(sqrt(window(sunspot.year, 1770, 1869)), c(2,0,0), method = "ML")`.

```
raices phi(B)      1.0234 +/- 0.6418i    |B| = 1.2080   arg = 0.5601
2*pi/arg           11.2178
R = sqrt(-phi2)    0.8278 = 1/|B|        semivida  3.67 anios
psi_0..psi_11      1.0000 1.4027 1.2822 0.8372 0.2957 -0.1590
                  -0.4257 -0.4881 -0.3929 -0.2167 -0.0346 0.0999
forma cerrada      psi_j = R^j sin((j+1)w)/sin(w)   max dif 3.1e-16
ceros de psi       j = 4.61  y  j = 10.22     (medio ciclo y un ciclo)
semiancho 95 %     2.2697 3.9098 4.8739 5.2312 5.2741 5.2864
forecast(ar2s,6)   2.2697 3.9098 4.8739 5.2312 5.2741 5.2864   identico
suma psi^2         6.1360    gamma0 = 8.2283    var muestral = 8.1490
semiancho techo    5.6224    en h = 6 va el 94 %
signo al reves     1 - 1.4027B - 0.6853B^2  ->  raices 0.5598 y -2.6066
ARMA(2,1) crudo    theta(B) raiz -2.6795 (|.| = 2.68, invertible)
                   phi(B) raices 1.0920 +/- 0.7661i (|.| = 1.3339)
                   sin factor comun: no hay redundancia
```

Y de paso quedó **reverificada la totalidad del M9** ya publicado: la rejilla de los ocho
AICc, los cuatro Ljung–Box, el BIC, la asimetría ($0.7913 \to 0.5734$), Shapiro–Wilk
($0.0007 \to 0.0470$) y $\lambda_{\text{Guerrero}} = 0.3062$. Todas reproducen.

## 5. Tareas

| # | Tarea | Fuente | Tamaño | Depende de |
|---|---|---|:--:|:--:|
| T1 | Tramo «El AR(2) final, escrito con los polinomios del Módulo 1» (C1, C2, C4) | `cap3_modulos.html` | M | — |
| T2 | Tramo «Los pesos $\psi$: qué deja un choque solar» con su tabla (C3) | `cap3_modulos.html` | M | T1 |
| T3 | Tabla de cierre «El capítulo entero, sobre una sola serie» (C5) | `cap3_modulos.html` | S | T1, T2 |
| T4 | Simulador `manchas-impulso`: $\psi$ con envolvente + abanico con techo | `cap3_js.js` | M | T2 |
| T5 | Registrar el simulador en las dos listas de `obligatorios` | `ensambla_cap3.py` | XS | T4 |
| T6 | Ampliar los bloques R y Python con el código de T1–T2 | `cap3_modulos.html` | M | T2 |
| T7 | Duración del M9: 16 → 19 min | `ensambla_cap3.py` | XS | T1–T4 |
| T8 | Recontar el sitio: 66 → 67 simuladores, capítulo 3 de 11 → 12 | `index.html`, `README.md` | XS | T4 |

## 6. Criterios de aceptación

- `ensambla_cap3.py` (modo verificación) dice **reproducible byte a byte** al terminar.
- Los capítulos 4, 5 y 6 salen **idénticos** al reejecutar la cadena.
- `cuenta_sitio.py`: «las cifras escritas coinciden con las contadas».
- Comprobado **por HTTP** ([[verificar-html-por-http-no-file]]), no por `file://`: sin
  errores de consola, los tres simuladores del M9 pintan, y la lectura de
  `manchas-impulso` dice lo mismo que la tabla de la prosa ($2.70$, $\pm 5.29$, $\pm 5.62$,
  $94\,\%$).
- Ninguna fórmula nueva desborda su caja en escritorio.

## 7. Riesgos

- **El que se materializó:** tres fórmulas con tres piezas separadas por `\qquad`
  desbordaban la caja. Partidas en dos `$$`. En móvil el material ya desbordaba antes de
  esta ronda —el propio M9 tenía una de dos—, y las cajas llevan barra horizontal: se deja
  como estaba, pero **medido** (`window.scrollX` no se mueve; la página no panea).
- **El que no:** perder el simulador en el siguiente reensamblado. T5 lo cubre.
- **Vigente:** la cuarta cifra de los $\psi$ difiere entre la prosa (ajuste a precisión
  plena) y el simulador ($\phi$ redondeados del JSON). D4 lo neutraliza bajando a dos
  decimales lo que se repite; si alguien sube la precisión de la lectura, reaparece.

## 8. Enlaces

- Auditoría anterior del capítulo (2026-09-02): [[PLAN_Auditoria_Cap3]]
- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- [[series-tiempo-riesgo-reensamblado]] · [[verificar-html-por-http-no-file]] ·
  [[series-tiempo-convenciones-prosa]]
- Sesión: [[2026-09-22]]
