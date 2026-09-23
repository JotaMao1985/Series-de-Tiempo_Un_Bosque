---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-09-23
estado: ejecutado
---

# Plan — La tabla de decisión en el cierre del capítulo 3

**Objetivo:** el encargo fue añadir al Módulo 10 una tabla con los criterios para elegir
entre AR, MA y ARMA y para fijar $p$ y $q$ en cada caso, validando la información antes de
escribirla.

**Alcance:** una sección nueva en el M10, entre el resumen numerado y la autoevaluación.
Ningún otro módulo del capítulo, y ningún otro capítulo.

## 1. Qué faltaba, y qué no

El capítulo **sí tiene** una tabla de identificación: está en el M5, con tres columnas
—Modelo, ACF, PACF— y la advertencia de que la tercera fila es la débil. Repetirla en el
cierre no valía una sección. Lo que no estaba en ninguna parte:

| # | Carencia | Dónde se notaba |
|---|---|---|
| C1 | **La lectura del correlograma y la fijación del orden viven separadas** | El M5 dice qué forma tiene cada firma; el M8 dice cómo se compara y se diagnostica. Nada los junta, y el resumen del M10 los reparte en dos viñetas distintas (la 2 y la 6) |
| C2 | **El corte se describe como cualitativo** | «Se corta tras el rezago $p$» no dice que la PACF teórica valga **cero exacto** desde $p+1$. El estudiante lee «pequeña» |
| C3 | **La asimetría AR/MA no se enuncia** | La última barra de la PACF de un AR($p$) *estima* $\phi_p$. En un MA no hay lectura análoga, y el material nunca lo dice |
| C4 | **El factor común se advierte sin un caso** | El M4 y el M5 dicen que un factor compartido se cancela. Ninguno muestra dos modelos concretos con la misma ACF |

## 2. Restricciones verificadas antes de planear

- **Se edita `ensamblado/cap3/cap3_modulos.html`**, no el HTML publicado
  ([[series-tiempo-riesgo-reensamblado]]).
- **`ensambla_cap3.py` verifica por defecto** y solo escribe con `--escribir`, así que la
  comprobación de reproducibilidad es previa y gratuita.
- El guion **cuenta simuladores, derivaciones, ejercicios y bloques de código** y aborta si
  cambian. Esta ronda no toca ninguno de esos: la sección es tabla y prosa.
- **Ninguna cifra a mano.** Todo lo numérico, de una ejecución de R contrastada con
  statsmodels.
- Verificación **por HTTP** ([[verificar-html-por-http-no-file]]).

## 3. Decisiones de esta ronda

- **D1 · Va después del resumen numerado, no antes.** El resumen recorre el capítulo en
  orden; la tabla es la herramienta que el estudiante se lleva al quiz. Ponerla justo antes
  de la autoevaluación la deja donde se usa.
- **D2 · Cuatro columnas, y la cuarta es la que justifica la sección.** Modelo, ACF y PACF
  reproducen la lectura del M5 —hace falta para que la tabla se sostenga sola—; «De dónde
  sale el orden» es lo nuevo.
- **D3 · La fila del ARMA dice que no hay lectura.** No se inventa un procedimiento que el
  capítulo no enseña: se remite a la rejilla y al AICc o BIC del M8, que es exactamente lo
  que hizo el caso del M9.
- **D4 · El aviso del muestreo va inmediatamente después de la tabla.** Las dos primeras
  filas describen la teoría. Sin ese aviso la tabla invita a buscar ceros en un
  correlograma, que es el error que el M6 ya combate con la regla del $5\,\%$.
- **D5 · El caso del factor común se escribe con números, y sin simulación.** La igualdad de
  las dos ACF es una propiedad exacta del proceso: no necesita semilla ni tamaño de muestra.
- **D6 · No se afirma que el criterio elija mal.** Con el factor exacto la verosimilitud
  máxima es la misma, así que el AICc penaliza al grande. Lo que se rompe es la estimación.
  La comprobación en doce semillas dio $10$ aciertos de $12$: de ahí «suele acertar».
- **D7 · Sin bloque de código.** El M10 no tiene ninguno y no es donde se aprende a calcular.

## 4. Cifras verificadas antes de escribir

Todo en R 4.6.0 y contrastado con `statsmodels.tsa.arima_process`.

| Comprobación | Resultado |
|---|---|
| PACF de un AR($p$) para $k > p$, con $p = 1,2,3,4$ | Máximo $\lvert\text{PACF}\rvert = 5.3\times10^{-16}$ |
| $\phi_{pp}$ frente a $\phi_p$, mismos cuatro casos | Coinciden: $0.7$, $-0.6853$, $-0.3$, $0.25$ |
| PACF del AR(2) del M9 en el rezago 2 | $-0.6853$, el coeficiente ajustado |
| ACF de un MA(2), $\theta = (0.5, 0.3)$, para $k > 2$ | Cero exacto en R y en statsmodels |
| ARMA(1,1) $\phi = 0.7$, $\theta = 0.5$ | Ninguna de las dos corta: ACF $0.8308\ldots$, PACF $0.8308, -0.3506, 0.1687\ldots$ |
| ARMA(2,2) $\phi = (1.1, -0.28)$, $\theta = (0.1, -0.20)$ frente a ese ARMA(1,1) | Diferencia máxima de ACF $2.8\times10^{-16}$ |
| $t$ del AR(2) final del M9, de sus errores estándar publicados | $19.29$ y $-9.47$ |
| Sobreparametrizar: e.e. de $\hat\phi_1$, ARMA(1,1) → ARMA(2,2) | De $0.051$ a $1.469$; $t$ de $14.90$ a $0.51$; una semilla da varianza negativa |
| AICc elige el modelo pequeño | $10$ de $12$ semillas |

La última fila es la razón de D6, y las dos últimas **no se publican**: sustentan la
redacción del aviso, no aparecen en el capítulo.

## 5. Tareas

| # | Tarea | Tamaño | Depende de |
|---|---|---|---|
| T1 | Sección «Elegir el modelo y fijar sus órdenes» y su entradilla | S | D1 |
| T2 | Tabla de cuatro columnas y cuatro filas | L | D2, D3, §4 |
| T3 | Aviso «Las dos primeras filas describen la teoría» | M | D4 |
| T4 | Caja «Qué confirma el orden elegido» | M | §4 |
| T5 | Aviso del factor común | M | D5, D6, §4 |
| T6 | Duración del M10, $12 \rightarrow 14$ min | S | T1–T5 |
| T7 | Reensamblar, cadena completa y comprobación en el navegador | M | T1–T6 |

## 6. Criterios de aceptación

- `ensambla_cap3.py` **reproducible byte a byte** antes y después.
- Los capítulos 4, 5 y 6 sin cambios en `git status` tras reejecutar sus guiones.
- Las diferencias caen **todas** dentro del M10.
- Cero `.katex-error` y cero `$…$` sin renderizar.
- La tabla nueva **no desborda** a $1280$ px; en móvil se desplaza dentro de su caja como
  las demás tablas del sitio, y la página no gana barra horizontal.
- Ninguna etiqueta `AR($p$)`, `MA($q$)` o `ARMA($p,q$)` parte el paréntesis de cierre.
- `cuenta_sitio.py` en verde.

## 7. Riesgos

- **Duplicar el M5.** Mitigado por D2: la entradilla dice explícitamente qué añade esta
  tabla, y la columna nueva es la mitad de su superficie.
- **Que el aviso del factor común se lea como «el AICc falla».** Mitigado por D6: se dice lo
  contrario, con la reserva que dieron las doce semillas.
- **El paréntesis fuera de la matemática en línea.** Materializado: en la columna estrecha,
  `AR($p$)` partía el `)` a la línea siguiente. Resuelto con `white-space:nowrap`; es un
  patrón que el capítulo usa por todas partes y que solo se rompe en celdas angostas.

## 8. Enlaces

- Bitácora: [[2026-09-23]]
- Nota del capítulo: [[20948-03 Modelos AR, MA y ARMA]]
- La tabla de identificación que esta completa: M5, auditada en [[PLAN_Auditoria_Cap3]]
- Los momentos que dan el corte exacto: [[PLAN_Momentos_ARMA]]
- El caso que aplica el procedimiento entero: [[PLAN_Cierre_Algebraico_M9]]
- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
