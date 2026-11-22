# Capítulo 3 · ronda R4 «fuentes» · cambios

Fecha: 2026-11-21. Redactor único de la ronda: subagente redactor R4 (Fable 5.2), con cinco lectores (subagentes de
solo lectura, uno por grupo de módulos) que propusieron marcas y citas; todo lo que hay en el repo lo escribió el
redactor. Sin commits ni push. Parte del commit `6fe8b18` (tras la R3), en el que el capítulo no tenía ninguna cita marcada.

> **Los veredictos de este documento son la propuesta del redactor.** Ninguna entrada de
> `bibliografia/contraste/cap3.yml` lleva `verificado_por`: lo firma el verificador, que no redactó. Por eso
> `audita_citas.py` falla hoy con un F08 por cada entrada citable (172), y con 6 F07 que no dependen del verificador
> (la ficha del ejemplar de Yule; ver «Lo que no cierra»).

> **Actualizado tras la segunda pasada (misma fecha).** Las tablas «Por módulo», «Citas visibles por obra», «Una
> fila por afirmación» y «Cambios de prosa» son las de hoy; el texto de «Resultado», «Lo que no cierra» y
> «Comprobaciones» es el de la primera pasada, y lo que cambió después está en la sección final, «Segunda pasada».

## Resultado

- **213 afirmaciones marcadas y registradas** (había 0): **119 `respaldada`**, **53 `con-matiz`**, **37 `propia`**,
  **4 `pendiente`**. Las 172 citables llevan cita visible; ninguna queda con el aviso «respaldada sin cita».
- **209 citas visibles**: 96 de Cryer y Chan (2008), 62 de FPP3, 23 de Hamilton (1994), 22 de la ayuda de R, 4 de
  Yule (1927) y 2 de Hyndman y Khandakar (2008). Shumway y Stoffer no se cita a la vista en ningún sitio (solo hay
  la 3.ª edición y el curso cita la 4.ª): es fuente adicional del registro en 9 citas literales.
- **349 citas literales** en el registro, todas copiadas de la caché y comprobadas antes de escribir
  (`r4_registro.py` usa las funciones F04, F05, F06, F07 y F11 del auditor, y el auditor las vuelve a comprobar: 586
  con las de los capítulos 1 y 2). Ningún literal en git: `r4_sin_literales.py` los busca en los 26 archivos de la ronda.
- **64 cambios de prosa**, todos porque la fuente leída decía otra cosa o no decía nada (lista abajo); dos son
  arrastres en el Módulo 10 de cambios de otros módulos y uno es un comentario de un bloque de código («siempre» →
  «por defecto»). **Ninguna cifra calculada nueva**: las únicas cifras que entran son las que da Yule (1927) con su
  cita (1749 y 1924) y la de la ayuda de R (1700 a 1988). Ningún gráfico, simulador ni dato tocado; `cap3_js.js`
  (quiz, práctica de repaso y simulacro) no tiene diff. El verificador de bloques sigue en 732 de 732.
- **Del inventario del diagnóstico (254 filas):** 179 quedan registradas (93 de prioridad alta, 78 de media, 8 de
  baja), 68 siguen sin marcar con su porqué (23 de alta: 2 del JSON de datos, 5 comentarios de bloques de código, 3
  repeticiones del resumen y 13 que viven en cadenas JS del quiz, la práctica o el simulacro) y 7 salen (la frase ya
  no existe o la absorbió otra). 44 afirmaciones son nuevas (texto que entró en R1–R3 o que esta ronda separó).
  **La media NO queda cerrada entera**: 32 filas de media siguen sin marcar (`r4_inventario.out`).
- **Ninguna obra nueva** en Zotero ni en `referencias.json`. En la caché: nueve páginas de ayuda de R más (`arima`,
  `arima.sim`, `ARMAacf`, `ARMAtoMA`, `polyroot`, `lh`, `sunspot.year`, `shapiro.test`, `tsdiag`) y dos capítulos
  más de FPP3 (`regression`, cap. 7, y `advanced`, cap. 12), registrados en `instantaneas.yml`. A mitad de la ronda
  la sesión maestra añadió el texto de **Yule (1927)** y de **Hyndman y Khandakar (2008)** (`ejemplares.yml`, que
  esta ronda no toca): con ellos se rehízo el recuadro de Yule y lo de `auto.arima()`.
- **Armazón:** la sección «1b» de `ensambla_cap3.py` ya no retira el CSS de las citas ni teclea el pie: el capítulo
  3 los hereda del 2 y `genera_referencias.genera()` corre al final del ensamblado (sección 9b). La protección pasó
  a `ensambla_cap4.py` (sección 0, con su aviso de cuándo borrarla). **Los capítulos 4–6 quedan byte a byte iguales
  a `HEAD`** tras reensamblar la cadena.

| módulo | afirmaciones | respaldada | con-matiz | propia | pendiente | citas visibles |
| M1 | 21 | 15 | 3 | 3 | 0 | 24 |
| M2 | 16 | 11 | 4 | 1 | 0 | 20 |
| M3 | 17 | 14 | 1 | 2 | 0 | 22 |
| M4 | 15 | 10 | 4 | 1 | 0 | 15 |
| M5 | 22 | 13 | 7 | 2 | 0 | 26 |
| M6 | 6 | 4 | 0 | 2 | 0 | 5 |
| M7 | 23 | 9 | 9 | 5 | 0 | 23 |
| M8 | 23 | 10 | 8 | 5 | 0 | 21 |
| M9 | 35 | 16 | 10 | 8 | 1 | 31 |
| M10 | 35 | 17 | 7 | 8 | 3 | 26 |
| **total** | **213** | **119** | **53** | **37** | **4** | **213** |

| obra | citas visibles | citas literales en el registro |
|---|---:|---:|
| Cryer y Chan (2008) | 98 | 145 |
| FPP3 | 62 | 104 |
| Hamilton (1994) | 25 | 51 |
| ayuda de R | 22 | 31 |
| Shumway y Stoffer 3.ª | 0 | 9 |
| Yule (1927) | 4 | 8 |
| Hyndman y Khandakar (2008) | 2 | 5 |
| **total** | **213** | **353** |

## Cómo se hizo (y cómo se rehace)

Guiones en `diagnostico/cap3/comprobaciones/`, reejecutables, en este orden:

| guion | qué hace |
|---|---|
| `bibliografia/_local/herramientas/cap3/r4_reune.py` (fuera de git: lleva literales) | reúne las propuestas de los cinco lectores (`propuestas/prop_[A-E].json`), aplica las decisiones del redactor (el recuadro de Yule, el ciclo de 11 años, `auto.arima()`, los arrastres) y escribe `r4_entradas.json` (fuera de git) y `r4_marcas.json` (en git, sin literales) |
| `r4_lib.py` | la notación de las marcas, la sustitución que exige que cada texto aparezca exactamente una vez, y `comprueba_fuente()`: lo que el auditor comprobará de una cita, antes de escribirla |
| `r4_marca.py` | parte de `ensamblado/cap3/cap3_modulos.html` **en el commit `6fe8b18`**, aplica los 64 cambios de prosa y las 225 piezas de marca de `r4_marcas.json`, pone la lista de fuentes al final de cada módulo que cita y la del capítulo tras las lecturas, y llama a `genera_referencias.genera()`. Escribe la fuente de ensamblado; `--comprobar` no escribe |
| `python3 ensamblado/ensambla_cap3.py --escribir` | ensambla el HTML final (y vuelve a pasar el generador) |
| `r4_registro.py` | escribe `cap3.yml` (huella y palabras) y `_local/citas/cap3.yml` (literales) desde `r4_entradas.json`; antes comprueba cada cita contra la caché. Si algo no está, no escribe. Conserva los `verificado_por` mientras la huella de la prosa no cambie. `--tolera-f07 yule1927method` solo deja escribir pese a la ficha del ejemplar de Yule |
| `r4_inventario.py` | rehace el inventario contra el texto de hoy, con la columna `r4` |
| `r4_software.R`, `r4_software.py` | comprueban ejecutando lo que el capítulo dice del software y las cifras de simulación (las `propia` y el matiz de varias `con-matiz`) |
| `r4_sin_literales.py` | busca los 349 literales en los archivos de la ronda que van a git |
| `r4_resumen.py` | saca del registro las tablas de este documento |
| `r4_recorrido.js` | los once módulos por HTTP con Chrome sin ventana, a 1200 y 375 px |
| `r4_comprueba_propuesta.py` | el comprobador que usaron los lectores sobre su JSON antes de entregarlo |

Las citas literales viven en `bibliografia/_local/citas/cap3.yml` y en `bibliografia/_local/herramientas/cap3/`
(propuestas y `r4_entradas.json`): **no están en git y no se regeneran desde nada que esté en git**. Al fusionar a
`main` hay que copiar `_local/citas/cap3.yml` y `_local/herramientas/cap3/` a esa copia, y las instantáneas nuevas
(`_local/web/…`: se pueden volver a extraer con `extrae_fuente.py`, pero la huella de FPP3 puede cambiar si la página cambió).

## Una fila por afirmación

| id | tipo | veredicto | afirmación | fuentes (la visible, en negrita) |
|---|---|---|---|---|
| c3-m1-21 | regla | respaldada | La notación con el operador de rezago es una herramienta muy útil para escribir los modelos de series de tiempo. | **FPP3, §9.2**; Hamilton (1994), p. 26 |
| c3-m1-01 | definicion | respaldada | El operador de rezago B desplaza la serie un periodo hacia atrás, B y_t = y_{t-1}; algunas obras escriben L en lugar de B. | **FPP3, §9.2**; Hamilton (1994), p. 26 |
| c3-m1-02 | regla | respaldada | El operador B se trata con las reglas algebraicas ordinarias: se puede sumar, multiplicar, elevar a potencias y factorizar. | **FPP3, §9.2**; Hamilton (1994), p. 27 |
| c3-m1-03 | resultado | respaldada | Una diferencia estacional seguida de una diferencia regular se escribe (1-B^m)(1-B) y_t y desarrolla en y_t - y_{t-1} - y_{t-m} + y_{t-m-1}. | **FPP3, §9.2** |
| c3-m1-04 | atribucion | respaldada | El preprocesamiento (1-B^12)(1-B) es el del modelo conocido como «airline», ARIMA(0,1,1)(0,1,1)_12, que se desarrolla en el Capítulo 5. | **Cryer y Chan (2008), pp. 240–241** |
| c3-m1-05 | definicion | respaldada | Los polinomios autorregresivo, phi(B) = 1 - phi_1 B - ... - phi_p B^p, y de medias móviles, theta(B) = 1 + theta_1 B + ... + theta_q B^q. | **FPP3, §9.7** |
| c3-m1-14 | resultado | respaldada | Un proceso autorregresivo es estacionario si todas las raíces de phi(B) = 0 están fuera del círculo unitario. | **FPP3, §9.7**; **Cryer y Chan (2008), p. 76** |
| c3-m1-34 | definicion | con-matiz | En el capítulo «estacionario» significa además causal: y_t depende solo de los choques hasta t; las fuentes imponen esa restricción a la solución estacionaria. | **Cryer y Chan (2008), p. 71**; Cryer y Chan (2008), p. 76; Shumway y Stoffer 3.ª, p. 94 |
| c3-m1-15 | resultado | con-matiz | Con \|phi\| >= 1 no hay solución estacionaria que dependa solo de los choques pasados; con \|phi\| > 1 hay una que depende de los choques futuros, inútil para pronosticar, y con \|phi\| = 1 no hay ninguna. | **Cryer y Chan (2008), p. 71**; **Cryer y Chan (2008), ejercicio 4.16**; Shumway y Stoffer 3.ª, p. 88; **Cryer y Chan (2008), ejercicio 4.15** |
| c3-m1-35 | resultado | respaldada | Cuando una raíz del polinomio AR está sobre el círculo unitario no hay solución estacionaria; en el AR(1) ocurre con phi = 1 y phi = -1, y phi = 1 es la caminata aleatoria. | **Cryer y Chan (2008), p. 76**; Cryer y Chan (2008), ejercicio 4.15; **FPP3, §9.3** |
| c3-m1-16 | definicion | respaldada | Se dice que el polinomio AR tiene una raíz unitaria cuando una raíz vale 1 (caso de la caminata aleatoria). | **Cryer y Chan (2008), p. 128** |
| c3-m1-17 | regla | respaldada | Diferenciar la serie es multiplicarla por el factor (1-B). | **FPP3, §9.2** |
| c3-m1-18 | dato | respaldada | polyroot() de R recibe los coeficientes del polinomio en orden ascendente de potencia. | **ayuda de R, §Arguments** |
| c3-m1-36 | dato | propia | np.roots() de NumPy recibe los coeficientes del polinomio en orden descendente de potencia. | — |
| c3-m1-07 | dato | con-matiz | El convenio del capítulo (los phi restando, los theta sumando en los polinomios; MA con signo más) es el que usan R y la librería statsmodels de Python. | **ayuda de R, §Details** |
| c3-m1-08 | atribucion | respaldada | Algunos textos y algún paquete (S-PLUS) escriben el MA con el signo contrario al del capítulo. | **Cryer y Chan (2008), p. 57**; **ayuda de R, §Details** |
| c3-m1-09 | atribucion | respaldada | El convenio de resta, que escribe el MA(1) como y_t = e_t - theta e_{t-1}, es el de textos como Cryer y Chan y el de la documentación de S-PLUS. | **Cryer y Chan (2008), p. 57**; **ayuda de R, §Details** |
| c3-m1-10 | resultado | propia | Los convenios de suma y de resta describen el mismo modelo: ajustado a los mismos datos da la misma verosimilitud, residuales y pronósticos, y solo cambia el signo impreso de theta. | — |
| c3-m1-12 | dato | respaldada | En R, tanto arima() al estimar como arima.sim() al simular usan los coeficientes del modelo, con el mismo convenio. | **ayuda de R, §Details**; ayuda de R, §Arguments; ayuda de R, §Value |
| c3-m1-11 | dato | propia | En Python, al estimar con ARIMA de statsmodels los coeficientes son los del modelo, pero al simular con ArmaProcess se pasan los del polinomio, de modo que el AR va con el signo cambiado. | — |
| c3-m1-13 | resultado | respaldada | En un MA(1) con el convenio de suma, la autocorrelación de orden 1 es rho_1 = theta/(1+theta^2). | **Hamilton (1994), p. 49** |
| c3-m2-01 | definicion | respaldada | Un proceso AR(p) explica el valor actual como una combinación lineal de sus p valores anteriores más un choque de ruido blanco. | **FPP3, §9.3**; Hamilton (1994), p. 58 |
| c3-m2-30 | definicion | respaldada | Una autorregresión es una regresión de la serie contra sí misma, como una regresión múltiple con los rezagos de la serie como predictores. | **FPP3, §9.3** |
| c3-m2-02 | resultado | respaldada | Como los regresores de una autorregresión no son fijos, no valen los resultados de muestra finita de la regresión clásica: el estimador de mínimos cuadrados es sesgado y los estadísticos t y F solo se justifican asintóticamente. | **Hamilton (1994), p. 215** |
| c3-m2-03 | resultado | respaldada | La constante c del AR(p) no es la media: tomando esperanzas, mu = c/(1 - phi_1 - ... - phi_p). | **Hamilton (1994), p. 59** |
| c3-m2-04 | dato | con-matiz | La columna «intercept» que imprime arima() de R es la media mu estimada (no la constante c del modelo). | **ayuda de R, §Details**; ayuda de R, §Arguments |
| c3-m2-05 | resultado | respaldada | Para un AR(p) la PACF teórica es exactamente cero para k > p, y la última barra distinta de cero, la del rezago p, vale phi_p. | **Cryer y Chan (2008), p. 114** |
| c3-m2-06 | resultado | respaldada | La ACF de un AR(p) decae hacia cero (de forma exponencial o sinusoidal) y no se corta en ningún rezago. | **Cryer y Chan (2008), p. 73**; **FPP3, §9.5** |
| c3-m2-08 | definicion | con-matiz | La ACF oscilante de un AR(2) con raíces complejas es un pseudo-ciclo cuya longitud se llama pseudo-periodo. | **Cryer y Chan (2008), p. 74**; Shumway y Stoffer 3.ª, p. 100 |
| c3-m2-10 | resultado | respaldada | Un AR(2) es estacionario (y causal) si y solo si -1 < phi_2 < 1, phi_1 + phi_2 < 1 y phi_2 - phi_1 < 1. | **Cryer y Chan (2008), p. 72**; **FPP3, §9.3** |
| c3-m2-12 | resultado | con-matiz | Si phi_1^2 + 4 phi_2 < 0 las raíces del AR(2) son complejas y la ACF oscila con pseudo-periodo P = 2π/arccos(phi_1/(2 sqrt(-phi_2))). | **Cryer y Chan (2008), pp. 73–74** |
| c3-m2-14 | regla | con-matiz | Un ciclo económico se puede modelar con un AR cuyos coeficientes dan ciclos (p >= 2, raíces complejas); FPP3 lo ilustra con las exportaciones de Egipto. | **FPP3, §9.5** |
| c3-m2-15 | resultado | respaldada | Media, varianza y autocorrelaciones de un AR(p) estacionario: mu = c/(1 - sum phi), varianza gamma_0 = sigma^2/(1 - sum phi_j rho_j) y la recursión rho_k = sum phi_j rho_{k-j}. | **Cryer y Chan (2008), pp. 76–77**; **Hamilton (1994), p. 59** |
| c3-m2-16 | resultado | respaldada | Formas cerradas: AR(1), rho_k = phi^k y gamma_0 = sigma^2/(1-phi^2); AR(2), rho_1, rho_2 y gamma_0 en función de phi_1 y phi_2. | **Hamilton (1994), pp. 53–54**; **Cryer y Chan (2008), p. 73**; **Cryer y Chan (2008), p. 75** |
| c3-m2-17 | resultado | propia | Los tres factores del denominador de la varianza del AR(2) son las tres desigualdades del triángulo; el triángulo es el conjunto de parámetros con solución causal de varianza finita. | — |
| c3-m2-18 | atribucion | respaldada | El sistema de ecuaciones que relaciona los phi con las autocovarianzas (y autocorrelaciones) de un AR se llama ecuaciones de Yule–Walker. | **Cryer y Chan (2008), p. 76**; Cryer y Chan (2008), p. 72; Hamilton (1994), p. 59 |
| c3-m2-19 | resultado | respaldada | En la derivación de Yule-Walker, el término del ruido se anula al multiplicar por y_{t-k} con k >= 1 porque e_t no depende de los valores anteriores de la serie. | **Cryer y Chan (2008), p. 72**; Hamilton (1994), p. 56 |
| c3-m3-32 | dato | propia | El software (R con arima(), statsmodels con ARIMA) impone la invertibilidad por defecto en el MA: devuelve la raíz invertible. | — |
| c3-m3-01 | definicion | respaldada | Un proceso MA(q) expresa el valor actual como combinación lineal del choque presente y de los q choques anteriores; se llama proceso de medias móviles de orden q. | **FPP3, §9.4**; Hamilton (1994), p. 50 |
| c3-m3-02 | definicion | respaldada | El modelo de medias móviles sirve para pronosticar valores futuros; el suavizamiento por medias móviles, para estimar la tendencia-ciclo de valores pasados: no deben confundirse. | **FPP3, §9.4** |
| c3-m3-03 | resultado | respaldada | Un MA(q) es estacionario en covarianza para cualquier valor de los θ: su media y su varianza no dependen de t y su autocovarianza solo depende del rezago. | **Hamilton (1994), p. 51**; Hamilton (1994), p. 48 |
| c3-m3-04 | resultado | respaldada | Varianza y autocorrelaciones de un MA(q): γ0 = σ²(1+Σθj²), ρk dada por el cociente de la suma de productos θjθ(j+k) entre 1+Σθj² para k ≤ q, y ρk = 0 para k > q (con θ0 = 1). | **Hamilton (1994), p. 51** |
| c3-m3-05 | resultado | respaldada | La autocorrelación de un MA(q) es exactamente cero para k > q: dos observaciones separadas por más de q periodos no comparten ningún choque, y por eso la ACF se corta tras el rezago q. | **Cryer y Chan (2008), p. 65**; **Hamilton (1994), p. 51**; Cryer y Chan (2008), p. 57 |
| c3-m3-07 | resultado | con-matiz | (θ, σ²) y (1/θ, θ²σ²) producen las mismas autocovarianzas, por lo que ningún dato puede separar el MA(1) de su recíproco: θ no es identificable sin una regla que elija uno. | **Hamilton (1994), p. 65**; Cryer y Chan (2008), p. 58 |
| c3-m3-08 | regla | respaldada | De la pareja θ, 1/θ se elige la invertible (\|θ\| < 1), porque es la única con la que se puede reconstruir cada choque a partir de lo observado. | **Cryer y Chan (2008), p. 80**; **Hamilton (1994), p. 67** |
| c3-m3-31 | resultado | respaldada | Un MA(1) no puede tener \|ρ1\| mayor que 0.5; los dos extremos se alcanzan en \|θ\| = 1, frontera de la invertibilidad, de modo que un MA(1) invertible queda estrictamente por debajo. | **Hamilton (1994), p. 49**; **Hamilton (1994), p. 65**; Cryer y Chan (2008), p. 58 |
| c3-m3-09 | resultado | respaldada | Un MA(q) es invertible si y solo si todas las raíces de θ(B) = 0 están fuera del círculo unitario; es la condición análoga a la estacionariedad del AR, aplicada al polinomio MA. | **Cryer y Chan (2008), p. 80**; FPP3, §9.4 |
| c3-m3-30 | resultado | respaldada | Diferenciar un ruido blanco (sobrediferenciar) da un MA(1) con θ = −1 en el convenio del capítulo: su raíz 1 − B está sobre el círculo unitario, no es invertible y su ρ1 vale −0.5, el mínimo de un MA(1). | **Cryer y Chan (2008), p. 126**; **Cryer y Chan (2008), p. 127**; **Hamilton (1994), p. 49** |
| c3-m3-10 | resultado | respaldada | Un MA(2) es invertible si y solo si θ1 + θ2 > −1, θ2 − θ1 > −1 y −1 < θ2 < 1. | **FPP3, §9.4** |
| c3-m3-11 | resultado | respaldada | Si la r1 muestral pasa de 0.5 ningún θ iguala su ρ1 a ella (el método de momentos no tiene solución) y el MA(1) queda en duda, aunque una r1 muestral puede superar 0.5 sin que lo haga la ρ1 verdadera. | **Cryer y Chan (2008), p. 150** |
| c3-m3-12 | resultado | propia | En un MA(q) el máximo de ρ1 es cos(π/(q+2)): 0.5 con q = 1, 0.707 con q = 2 y 0.809 con q = 3. | — |
| c3-m3-06 | resultado | respaldada | La PACF de un proceso de medias móviles no se corta nunca: decae, de manera parecida a como lo hace la ACF de un autorregresivo. | **Cryer y Chan (2008), p. 114** |
| c3-m3-15 | definicion | respaldada | La PACF en el rezago k es la correlación entre y_t e y_{t−k} sin el efecto de los rezagos intermedios, o el último coeficiente de la proyección lineal de y_t sobre sus k valores anteriores; en un AR(p) vale cero más allá de p. | **Cryer y Chan (2008), p. 112**; **Hamilton (1994), p. 111**; **Cryer y Chan (2008), p. 114** |
| c3-m3-14 | resultado | respaldada | La PACF de un MA(1) invertible decae exponencialmente al ritmo de \|θ\|^k, alternando de signo si θ > 0 y siendo siempre negativa si θ < 0. | **Cryer y Chan (2008), p. 114** |
| c3-m4-01 | resultado | respaldada | Un ARMA estacionario (raíces de φ(B) fuera del círculo unitario) se escribe como MA(∞) con pesos ψ, ψ(B) = θ(B)/φ(B); uno invertible (raíces de θ(B) fuera) se escribe como AR(∞) con pesos π, π(B) = φ(B)/θ(B). | **Cryer y Chan (2008), p. 78**; **Cryer y Chan (2008), p. 80**; Hamilton (1994), p. 108 |
| c3-m4-02 | definicion | con-matiz | Los pesos ψ dan la respuesta de la serie a un choque ocurrido j periodos atrás (la función de respuesta al impulso). | **Hamilton (1994), p. 54** |
| c3-m4-03 | resultado | respaldada | Con parámetros conocidos y un modelo invertible, el choque εt es el error del mejor pronóstico lineal a un paso: nada del pasado lo anticipa. | **Cryer y Chan (2008), p. 197**; Hamilton (1994), p. 108 |
| c3-m4-04 | resultado | respaldada | En un MA(1) con \|θ\| > 1 los pesos π de la representación AR(∞) crecen con el rezago; con \|θ\| = 1 conservan su magnitud; en ambos casos el proceso no es invertible. | **FPP3, §9.4** |
| c3-m4-05 | resultado | respaldada | Con \|θ\| > 1, reconstruir el choque de hoy exigiría dar peso creciente a observaciones cada vez más antiguas, lo que no tiene sentido: esa es la traducción operativa de la no invertibilidad. | **FPP3, §9.4** |
| c3-m4-31 | dato | con-matiz | La razón de fondo por la que el software devuelve por defecto la raíz invertible: de cada pareja solo una es invertible y los algoritmos de estimación y pronóstico están pensados para esa representación. | **Hamilton (1994), p. 67**; Cryer y Chan (2008), p. 80 |
| c3-m4-06 | resultado | respaldada | Con los pesos ψ la autocovarianza es γk = σ² Σ ψj ψ(j+k), porque los choques son incorrelados. | **Cryer y Chan (2008), p. 56**; Hamilton (1994), p. 52 |
| c3-m4-30 | resultado | con-matiz | En el ARMA(1,1) los pesos tienen forma cerrada para j ≥ 1: ψj = (φ+θ)φ^(j−1) y πj = −(φ+θ)(−θ)^(j−1). | **Cryer y Chan (2008), p. 78** |
| c3-m4-09 | dato | propia | ARMAtoMA() de R devuelve los pesos desde ψ1 y arma2ma() de statsmodels desde ψ0 = 1; con los pesos π ocurre lo mismo (arma2ar empieza en π0 = 1). | — |
| c3-m4-12 | resultado | respaldada | La varianza del error de pronóstico a h pasos de un ARMA invertible es σ² Σ_{j=0}^{h−1} ψj². | **Cryer y Chan (2008), p. 202** |
| c3-m4-13 | resultado | respaldada | En un ARMA estacionario la varianza del error de pronóstico tiende a la varianza del proceso, γ0 = σ² Σ ψj²; los intervalos de pronóstico convergen. | **Cryer y Chan (2008), p. 197**; FPP3, §9.8 |
| c3-m4-14 | resultado | respaldada | En la caminata aleatoria, φ(B) = 1 − B, todos los pesos ψj valen 1: ningún choque se desvanece. | **Cryer y Chan (2008), p. 199**; Cryer y Chan (2008), p. 202 |
| c3-m4-32 | resultado | respaldada | En la caminata aleatoria la varianza del error de pronóstico a h pasos es σ²h y crece sin límite con el horizonte. | **Cryer y Chan (2008), p. 199**; Cryer y Chan (2008), p. 202 |
| c3-m4-10 | regla | con-matiz | Principio de parsimonia: conviene el modelo con el menor número de parámetros que represente bien la serie; el ARMA(1,1) imita con dos parámetros un AR(∞) cuyos pesos decaen como \|θ\|^j. | **Cryer y Chan (2008), p. 8**; Hamilton (1994), p. 109 |
| c3-m4-11 | resultado | respaldada | Si φ(B) y θ(B) comparten un factor, el cociente ψ(B) = θ(B)/φ(B) lo cancela y el modelo es en realidad más pequeño de lo que aparenta. | **Cryer y Chan (2008), p. 77**; Hamilton (1994), p. 60 |
| c3-m5-01 | definicion | respaldada | Un ARMA(p,q) combina un AR(p) y un MA(q): φ(B)yt = c + θ(B)εt; es estacionario si las raíces de φ(B) están fuera del círculo unitario e invertible si lo están las de θ(B), cada polinomio por lo suyo. | **Hamilton (1994), p. 59**; **Hamilton (1994), p. 60**; **Cryer y Chan (2008), p. 80** |
| c3-m5-03 | regla | con-matiz | Principio de parsimonia: mezclar AR y MA permite describir con pocos parámetros lo que un AR puro necesitaría muchos; menos parámetros deja menos margen de error al estimar y, con frecuencia, mejores pronósticos fuera de la muestra. | **Cryer y Chan (2008), p. 8**; **Hamilton (1994), p. 109** |
| c3-m5-11 | regla | con-matiz | Tabla de identificación: AR(p), ACF decae y PACF se corta tras p; MA(q), ACF se corta tras q y PACF decae; ARMA mixto, ambas decaen (la ACF a partir del rezago q con el ritmo de un AR(p)). | **Cryer y Chan (2008), p. 116**; FPP3, §9.5; Hamilton (1994), p. 60 |
| c3-m5-12 | resultado | respaldada | Cuando la ACF y la PACF decaen, la tabla no dice cuáles son p y q: ni el correlograma ni el parcial identifican los órdenes de un ARMA mixto. | **FPP3, §9.5**; Cryer y Chan (2008), p. 116 |
| c3-m5-18 | regla | respaldada | Una ACF muestral no reproduce en detalle la teórica: con una muestra corta, un proceso que sí corresponde a una fila de la tabla puede dar un correlograma que no encaja. | **Cryer y Chan (2008), p. 112** |
| c3-m5-04 | regla | con-matiz | Identificar un modelo es un ciclo (especificar, ajustar, diagnosticar) que se repite hasta que el diagnóstico queda limpio; el capítulo lo recorre en cuatro pasos. | **Cryer y Chan (2008), p. 8**; FPP3, §9.7 |
| c3-m5-31 | dato | con-matiz | Los criterios de información (AICc, BIC) comparan modelos ajustados a los mismos datos y penalizan los parámetros; la prueba de Ljung–Box resume en un p-valor si los residuales parecen ruido blanco, y fitdf descuenta los parámetros estimados. | **FPP3, §9.6**; **ayuda de R, §Arguments** |
| c3-m5-05 | regla | respaldada | Si la ACF se corta tras el rezago q hay una parte MA(q); si decae (geométrica u ondulada) no es un MA puro y hay que mirar la PACF. | **FPP3, §9.5** |
| c3-m5-06 | regla | respaldada | Para una serie de ruido blanco se espera que el 95 % de las barras de la ACF caigan dentro de ±1.96/√T; esa banda marca qué es ruido. | **FPP3, §2.9** |
| c3-m5-30 | dato | con-matiz | Sin bartlett_confint=False, plot_acf de statsmodels dibuja la banda de Bartlett: no supone ruido blanco y se ensancha con el rezago porque la varianza de cada r_k suma las autocorrelaciones de los rezagos anteriores. | **Cryer y Chan (2008), p. 112** |
| c3-m5-07 | regla | respaldada | Una ACF que decae despacio y de forma casi lineal suele ser síntoma de que la serie no es estacionaria: eso se trata en el Capítulo 2. | **Cryer y Chan (2008), p. 128**; FPP3, §9.1 |
| c3-m5-08 | dato | propia | pacf(y)$acf de R devuelve un array de tres dimensiones (por eso conviene envolverlo en as.numeric()). | — |
| c3-m5-09 | regla | con-matiz | Conviene proponer varios candidatos vecinos y no uno solo: la tabla de ACF/PACF acota la búsqueda pero no la resuelve. | **FPP3, §9.7**; Cryer y Chan (2008), p. 8 |
| c3-m5-10 | regla | respaldada | ARMAacf() da la ACF teórica y Box.test(..., type = "Ljung-Box", fitdf = p + q) prueba los residuales de un ARMA(p,q) descontando p + q grados de libertad. | **ayuda de R, §Details**; FPP3, §9.7; ayuda de R, §Description |
| c3-m5-13 | resultado | respaldada | Un ARMA(p,q) estacionario tiene media μ = c/(1−φ1−…−φp) y autocovarianzas γk = σ² Σ ψjψ(j+k), con γ0 = σ² Σ ψj², con los pesos ψ de la representación MA(∞). | **Cryer y Chan (2008), p. 56**; Hamilton (1994), p. 52; **Hamilton (1994), p. 60** |
| c3-m5-14 | resultado | respaldada | En un ARMA con p ≥ 1 no hay una forma corta general de la varianza en función de los parámetros: se pasa por los pesos ψ, sumando su serie o planteando un sistema lineal en el que entran. | **Cryer y Chan (2008), p. 85**; Cryer y Chan (2008), p. 77 |
| c3-m5-15 | resultado | respaldada | Autocovarianzas del ARMA(1,1): γ0 = σ²(1+2φθ+θ²)/(1−φ²) y γ1 = σ²(1+φθ)(φ+θ)/(1−φ²). | **Cryer y Chan (2008), p. 78** |
| c3-m5-16 | resultado | respaldada | En un ARMA(p,q), para k > q la ACF cumple la recursión ρk = φ1ρ(k−1)+…+φpρ(k−p) del AR(p); no vale para k ≤ q. | **Hamilton (1994), p. 60**; Cryer y Chan (2008), p. 79 |
| c3-m5-17 | resultado | respaldada | En el ARMA(1,1) el ritmo de decaimiento de la ACF es φ y la parte MA solo decide con qué valor arranca; un AR(1) con el mismo φ decae al mismo ritmo desde ρ0 = 1. | **Cryer y Chan (2008), p. 78** |
| c3-m5-19 | resultado | respaldada | Si φ(B) y θ(B) comparten un factor, ese factor se cancela y el modelo es en realidad más pequeño de lo que aparenta (redundancia de parámetros). | **Cryer y Chan (2008), p. 77**; Hamilton (1994), p. 60; Cryer y Chan (2008), p. 187 |
| c3-m5-32 | dato | propia | Cuando dos factores casi se cancelan, el ajuste de un ARMA(1,1) da coeficientes muy distintos de los verdaderos con errores estándar grandes y, a veces, un aviso del optimizador, mientras que la suma φ̂ + θ̂ sí reproduce la cancelación. | — |
| c3-m5-20 | regla | con-matiz | Si un ARMA ajustado tiene φ̂1 ≈ −θ̂1 y errores estándar grandes, conviene probar el modelo más pequeño antes de interpretar nada. | **Cryer y Chan (2008), p. 187**; **Hamilton (1994), p. 60** |
| c3-m6-01 | dato | respaldada | arima.sim() descarta por su cuenta un tramo de calentamiento (burn-in): si no se indica su longitud, la función la calcula. | **ayuda de R, §Arguments** |
| c3-m6-04 | dato | propia | generate_sample() de statsmodels no descarta un tramo de calentamiento salvo que se le pase burnin=. | — |
| c3-m6-05 | resultado | propia | Sin calentamiento, una serie que arranca en cero tiene al principio menos varianza que en régimen estacionario; con φ = 0.95 la diferencia es grande en t = 5 y el arranque comprimido dura decenas de observaciones. | — |
| c3-m6-06 | resultado | respaldada | La banda ±1.96/√T es un intervalo al 95 % para cada rezago por separado; en 20 rezagos de ruido blanco se espera que uno se salga por azar. | **FPP3, §2.9**; **FPP3, §5.4** |
| c3-m6-07 | regla | respaldada | Uno o dos picos que apenas asoman fuera de la banda no bastan como evidencia contra el ruido blanco; uno muy grande, o bastantes más del 5 % de los rezagos fuera, sí. | **FPP3, §2.9** |
| c3-m6-08 | regla | respaldada | Para no leer cada rezago por separado existe una prueba de grupo, la de Ljung–Box, que evalúa las primeras autocorrelaciones a la vez. | **FPP3, §5.4**; Cryer y Chan (2008), p. 183 |
| c3-m7-01 | dato | respaldada | sunspot.year, la serie de R, recoge el número anual de manchas solares de 1700 a 1988; el capítulo usa el tramo 1770–1869. | **ayuda de R, §Description** |
| c3-m7-02 | historica | con-matiz | Con los números de manchas de Wolfer de 1749 a 1924, Yule propuso en 1927 lo que hoy se llama un modelo autorregresivo: ajustó la regresión de cada valor sobre los dos anteriores y comparó las manchas con un péndulo que recibe pequeños impulsos al azar. | **Yule (1927), p. 281**; Yule (1927), p. 280; Yule (1927), p. 275; **Yule (1927), p. 294** |
| c3-m7-03 | dato | respaldada | Hacia 1927 el periodo de las manchas solares se estimaba en algo más de once años. | **Yule (1927), p. 276**; FPP3, §12.4 |
| c3-m7-04 | regla | con-matiz | Una ACF que ondula anticipa raíces complejas en el AR(2). | **Cryer y Chan (2008), p. 73** |
| c3-m7-05 | definicion | respaldada | El estimador de Yule–Walker es el de momentos: sustituye las autocorrelaciones teóricas por las muestrales en las ecuaciones de Yule–Walker y resuelve el sistema. | **Cryer y Chan (2008), p. 150**; Shumway y Stoffer 3.ª, p. 121 |
| c3-m7-06 | regla | respaldada | El método de momentos da estimaciones bastante buenas en modelos AR puros y es muy ineficiente cuando el modelo tiene términos de media móvil. | **Cryer y Chan (2008), p. 152**; Shumway y Stoffer 3.ª, p. 123 |
| c3-m7-07 | definicion | respaldada | CSS minimiza la suma de cuadrados de los residuales condicionando en los primeros valores; es regresión ordinaria en un AR puro y mínimos cuadrados no lineales si hay parte MA. | **Cryer y Chan (2008), p. 154**; **Cryer y Chan (2008), p. 157**; Hamilton (1994), p. 122 |
| c3-m7-08 | regla | con-matiz | CSS deja de lado la información de las primeras observaciones. | **ayuda de R, §Arguments**; Hamilton (1994), p. 122 |
| c3-m7-09 | resultado | respaldada | La máxima verosimilitud gaussiana exacta incluye la densidad de la primera observación y aprovecha toda la información de los datos; sus errores estándar salen de la hessiana y pueden ser solo una guía aproximada. | **Cryer y Chan (2008), p. 159**; Cryer y Chan (2008), p. 158; **ayuda de R, §Details** |
| c3-m7-30 | resultado | con-matiz | Entre CSS y máxima verosimilitud la diferencia está en la primera observación: ML incluye su densidad y CSS la ignora, y ese término pesa más cerca de la frontera estacionaria. | **Cryer y Chan (2008), p. 160**; Hamilton (1994), p. 122 |
| c3-m7-31 | resultado | respaldada | Con T grande la primera observación pesa poco y CSS y ML coinciden; con T pequeño o φ cerca de 1, no. | **Cryer y Chan (2008), p. 160**; Hamilton (1994), p. 123 |
| c3-m7-32 | dato | con-matiz | CSS puede salirse de la región estacionaria, cosa que ML no hace en el ejemplo, porque arima() solo reparametriza los coeficientes para mantenerlos dentro cuando no usa CSS. | **ayuda de R, §Arguments** |
| c3-m7-10 | resultado | respaldada | Con T grande un único término frente a los T − 1 de la parte condicional es despreciable y CSS y ML convergen; con T pequeño o φ cerca de la frontera, no. | **Cryer y Chan (2008), p. 160**; Hamilton (1994), p. 123 |
| c3-m7-11 | dato | propia | En el ejemplo con T = 40 y φ = 0.95, CSS estima una raíz fuera de la región estacionaria y ML no; en mil simulaciones iguales CSS pasa de 1 entre un 2.5 y un 4.6 % de las veces, según la semilla. | — |
| c3-m7-33 | dato | con-matiz | ML no sale de la región estacionaria en ninguna de las simulaciones que estima, porque arima() reparametriza los φ (transform.pars = TRUE, su valor por defecto). | **ayuda de R, §Arguments**; ayuda de R, §Usage |
| c3-m7-34 | dato | propia | En 13 a 17 % de las simulaciones la estimación ML es ≥ 0.999, y en 4 a 13 de cada mil el optimizador no llega a dar estimación. | — |
| c3-m7-35 | regla | con-matiz | CSS es más barato de calcular y sirve para arrancar; la máxima verosimilitud exacta cuenta además con las primeras observaciones, cuyo efecto pesa más en series de longitud moderada. | **Hamilton (1994), p. 123**; **Cryer y Chan (2008), p. 158** |
| c3-m7-12 | dato | con-matiz | arima() usa por defecto method = "CSS-ML": estima por CSS para obtener valores iniciales y termina maximizando la verosimilitud. | **ayuda de R, §Arguments** |
| c3-m7-13 | resultado | propia | Con muestras cortas el estimador de Yule–Walker queda sesgado hacia el interior de la región estacionaria. | — |
| c3-m7-14 | dato | respaldada | Yule–Walker obtiene σ² de la ecuación de la varianza del proceso, mientras que ML lo estima junto al resto de los parámetros. | **Cryer y Chan (2008), p. 151**; **ayuda de R, §Value** |
| c3-m7-15 | regla | con-matiz | Los criterios de información se construyen sobre la verosimilitud, así que no deben mezclarse salidas de ar() y de arima(). | FPP3, §9.6; **ayuda de R, §Details**; ayuda de R, §Value |
| c3-m7-17 | dato | propia | yule_walker() de statsmodels usa por defecto method="adjusted" (divisor T − k) y ar() de R usa el divisor T, así que con las opciones por defecto no coinciden. | — |
| c3-m7-16 | dato | propia | Pasando method="mle" a yule_walker() de statsmodels se reproduce la salida de ar() de R; el nombre indica solo el divisor, no que sea máxima verosimilitud. | — |
| c3-m8-24 | resultado | propia | Añadir parámetros a un modelo anidado no empeora la verosimilitud máxima. | — |
| c3-m8-30 | regla | respaldada | Los criterios de información penalizan la complejidad y se elige el modelo con el menor valor. | **FPP3, §9.6**; Cryer y Chan (2008), p. 130 |
| c3-m8-01 | definicion | respaldada | AIC = −2 log L + 2k; AICc = AIC + 2k(k+1)/(T−k−1); BIC = −2 log L + k log T, con k el número de parámetros incluido σ². | **FPP3, §9.6**; Cryer y Chan (2008), p. 130; Cryer y Chan (2008), p. 131 |
| c3-m8-03 | resultado | respaldada | El AICc corrige el sesgo del AIC en muestras pequeñas. | **Cryer y Chan (2008), p. 130**; FPP3, §7.5 |
| c3-m8-04 | regla | con-matiz | Dado que el AICc converge al AIC, no hay razón para preferir el AIC. | **FPP3, §9.6**; FPP3, §7.5 |
| c3-m8-05 | resultado | respaldada | El BIC penaliza más que el AIC y por eso tiende a elegir modelos más pequeños. | **FPP3, §7.5** |
| c3-m8-06 | regla | con-matiz | Para pronosticar conviene el AICc; para identificar el modelo verdadero, el BIC. | **FPP3, §7.5**; **Cryer y Chan (2008), p. 131** |
| c3-m8-07 | regla | respaldada | Los criterios solo son comparables entre modelos ajustados a los mismos datos; diferenciar cambia los datos, así que no se pueden comparar los AIC de modelos con distinto orden de diferenciación. | **FPP3, §9.6**; ayuda de R, §Value |
| c3-m8-34 | regla | respaldada | Si el modelo ha capturado toda la estructura, los residuales no deben tener autocorrelación. | **FPP3, §5.4** |
| c3-m8-08 | definicion | con-matiz | La prueba de Ljung–Box contrasta si las primeras h autocorrelaciones de los residuales son conjuntamente nulas con el estadístico T(T+2)Σ r̂k²/(T−k), que sigue una χ² con h − p − q grados de libertad; un p-valor pequeño indica que el modelo no basta. | **FPP3, §5.4**; Cryer y Chan (2008), p. 183; **Cryer y Chan (2008), p. 184** |
| c3-m8-31 | resultado | con-matiz | Los grados de libertad de la prueba son h − p − q porque los residuales provienen de un modelo estimado; si no se descuentan, la prueba rechaza menos de lo debido. | **FPP3, §9.7**; Cryer y Chan (2008), p. 183 |
| c3-m8-13 | dato | respaldada | En R el descuento de los grados de libertad es el argumento fitdf = p + q de Box.test(), que no se aplica solo, y solo tiene sentido evaluar con lag > p + q. | **ayuda de R, §Details**; ayuda de R, §Arguments |
| c3-m8-15 | dato | propia | Con 3000 series AR(2), T = 100 y h = 12, la prueba al 5 % rechaza el 4.9 % de las veces con fitdf = 2 y el 2.6 % sin él. | — |
| c3-m8-09 | atribucion | con-matiz | Bajo ruido blanco cada autocorrelación muestral es aproximadamente N(0, 1/T) y sumar h cuadrados escalados da el estadístico de Box–Pierce, aproximadamente χ² con h grados de libertad. | **Cryer y Chan (2008), p. 110**; **Cryer y Chan (2008), p. 183**; FPP3, §5.4 |
| c3-m8-10 | resultado | respaldada | La aproximación χ² del estadístico de Box–Pierce no es satisfactoria con T moderado. | **Cryer y Chan (2008), p. 184** |
| c3-m8-11 | resultado | propia | Bajo ruido blanco la varianza de la autocorrelación muestral r̂k es aproximadamente (T − k)/(T(T + 2)), menor que 1/T y decreciente en k. | — |
| c3-m8-36 | atribucion | con-matiz | Ljung y Box (1978) modificaron el estadístico de Box–Pierce con un factor que crece con el rezago; con el factor original la prueba tendía a pasar por alto modelos inadecuados. | **Cryer y Chan (2008), p. 184**; Cryer y Chan (2008), p. 183 |
| c3-m8-12 | resultado | con-matiz | Ignorar los parámetros estimados infla el p-valor de Ljung–Box; la corrección es descontarlos de los grados de libertad. | **FPP3, §9.7**; Cryer y Chan (2008), p. 183 |
| c3-m8-32 | dato | respaldada | En R el descuento es el argumento fitdf = p + q de Box.test(), que no se aplica solo, y solo tiene sentido evaluar con h > p + q. | **ayuda de R, §Details** |
| c3-m8-35 | resultado | propia | Sin el descuento de grados de libertad la prueba rechaza cerca de la mitad de lo que debería. | — |
| c3-m8-16 | regla | con-matiz | Sobre los residuales de un ARMA(p, q) se llama a Box.test() con type = "Ljung-Box" y fitdf = p + q; sin fitdf la prueba es demasiado indulgente. | **ayuda de R, §Details**; FPP3, §9.7 |
| c3-m8-18 | dato | propia | R devuelve en residuals() las innovaciones de arima() divididas entre la raíz de γ0/σ² en el primer residual (y análogamente el segundo), y statsmodels las devuelve sin estandarizar; del tercero en adelante coinciden. | — |
| c3-m8-33 | resultado | respaldada | Ljung–Box evalúa las autocorrelaciones como grupo: varias moderadas, cada una insignificante por separado, pueden acumular un Q que sí lo es. | **Cryer y Chan (2008), p. 183** |
| c3-m9-01 | dato | con-matiz | Los números de manchas solares son índices construidos a partir de conteos de manchas y de grupos de manchas, no conteos puros. | **Cryer y Chan (2008), p. 392**; ayuda de R, §Description |
| c3-m9-02 | resultado | respaldada | Si la desviación estándar de la serie es proporcional a su nivel, el logaritmo produce una serie de varianza aproximadamente constante. | **Cryer y Chan (2008), p. 98** |
| c3-m9-41 | resultado | propia | Si la desviación estándar de cada bloque crece como el nivel elevado a b, la potencia que estabiliza la varianza es λ = 1 − b (con b = 0.5, la raíz cuadrada). | — |
| c3-m9-42 | atribucion | respaldada | El criterio de Guerrero es el que Hyndman y Athanasopoulos ofrecen para elegir λ en la transformación de Box–Cox. | **FPP3, §3.1** |
| c3-m9-43 | definicion | pendiente | El criterio de Guerrero busca que el cociente entre la desviación y el nivel elevado a 1 − λ sea homogéneo entre bloques. | — |
| c3-m9-03 | regla | respaldada | La raíz cuadrada está definida en cero y se señala como transformación útil con datos de tipo Poisson (conteos). | **Cryer y Chan (2008), p. 101**; Cryer y Chan (2008), p. 392 |
| c3-m9-05 | dato | con-matiz | El λ de Guerrero de esta serie, desplazada una unidad para que sea positiva, es 0.3062 y queda entre el logaritmo y la raíz cuadrada. | **Cryer y Chan (2008), p. 101** |
| c3-m9-51 | regla | con-matiz | Los criterios de información solo comparan modelos ajustados a los mismos datos (la serie cruda y su raíz son datos distintos). | **FPP3, §9.6** |
| c3-m9-06 | dato | respaldada | Ya en 1927 se daba como estimación habitual del periodo de las manchas solares algo más de 11 años. | **Yule (1927), p. 276**; FPP3, §12.4 |
| c3-m9-08 | regla | propia | La lectura del caso no depende de haber elegido exactamente λ = 0.5: con λ = 0.5 y con λ = 0.3062 de Guerrero el AR(2) da un pseudo-periodo y un Ljung–Box parecidos. | — |
| c3-m9-53 | regla | respaldada | Un módulo de las raíces del polinomio autorregresivo mayor que uno es la condición de estacionariedad. | **Cryer y Chan (2008), p. 71** |
| c3-m9-10 | resultado | con-matiz | En un AR(2) con raíces complejas, el módulo de la raíz gobierna cuánto se amortigua la oscilación y el ángulo, cada cuánto oscila. | **Cryer y Chan (2008), p. 73**; Cryer y Chan (2008), p. 75 |
| c3-m9-40 | definicion | respaldada | Para un AR(2) con raíces complejas, Hyndman y Athanasopoulos dan el periodo medio de los ciclos como 2π/arccos(−φ1(1−φ2)/(4φ2)). | **FPP3, §9.5** |
| c3-m9-44 | resultado | respaldada | El pseudo-periodo de 11.22 años, el ángulo de la raíz, es el periodo con que oscilan la ACF y los pesos ψ del modelo. | **Cryer y Chan (2008), p. 75**; Cryer y Chan (2008), p. 73 |
| c3-m9-45 | resultado | propia | El periodo de la fórmula de FPP3 coincide con el periodo del máximo de la densidad espectral del AR(2), y se acerca al del ángulo de la raíz cuando el módulo de la raíz tiende a 1. | — |
| c3-m9-09 | resultado | propia | Un AR puro es invertible, porque su polinomio MA es la constante 1 y no tiene raíces que comprobar. | — |
| c3-m9-11 | resultado | respaldada | Los pesos ψ de un AR(2) con raíces complejas tienen forma cerrada: R^j sen((j+1)ω)/sen ω. | **Cryer y Chan (2008), p. 75** |
| c3-m9-46 | resultado | respaldada | La varianza del error de pronóstico a h pasos de un ARIMA invertible es σ² por la suma de los cuadrados de los h primeros pesos ψ. | **Cryer y Chan (2008), p. 201** |
| c3-m9-47 | resultado | respaldada | En un modelo ARMA estacionario la varianza del error de pronóstico converge, a horizontes largos, a γ0 (σ² por la suma de todos los ψ²). | **Cryer y Chan (2008), p. 201**; FPP3, §9.5 |
| c3-m9-48 | resultado | respaldada | Los intervalos de pronóstico de un modelo estacionario convergen a un ancho fijo, mientras que con una raíz unitaria (d ≥ 1, no estacionario) siguen creciendo sin cota. | **FPP3, §9.8**; **Cryer y Chan (2008), p. 202** |
| c3-m9-13 | resultado | respaldada | Al deshacer una transformación se retrotransforman los extremos del intervalo, y eso conserva su cobertura. | **FPP3, §5.6** |
| c3-m9-12 | resultado | respaldada | El pronóstico retrotransformado es la mediana, y no la media, de la distribución de pronóstico, si la distribución en la escala transformada es simétrica. | **FPP3, §5.6** |
| c3-m9-14 | atribucion | respaldada | Shapiro–Wilk es una prueba de normalidad que R implementa con shapiro.test(); su p-valor es aproximado. | **ayuda de R, §Description** |
| c3-m9-15 | resultado | con-matiz | Una serie de manchas solares que sube más rápido de lo que baja es temporalmente irreversible, lo que sugiere un proceso no lineal que un ARMA gaussiano no puede reproducir. | **Cryer y Chan (2008), p. 392**; **Cryer y Chan (2008), p. 396** |
| c3-m9-16 | regla | con-matiz | Los intervalos de pronóstico de un ARIMA suponen residuales incorrelacionados y normales; si no se cumplen, pueden ser incorrectos. | **FPP3, §9.8** |
| c3-m9-17 | resultado | propia | El Capítulo 2 concluyó que la TRM tiene una raíz unitaria y que su primera diferencia es estacionaria. | — |
| c3-m9-18 | definicion | respaldada | El log-retorno multiplicado por 100 es el rendimiento continuo de las finanzas expresado como variación porcentual, lectura que es una buena aproximación mientras la variación sea pequeña. | **Cryer y Chan (2008), p. 278**; **Cryer y Chan (2008), p. 99** |
| c3-m9-20 | dato | con-matiz | auto.arima() (forecast) ajusta varios modelos ARIMA y se queda con el de menor AICc; con los argumentos por defecto devuelve sobre los log-retornos de la TRM un ARIMA(0,0,0) con media cero. | **Hyndman y Khandakar (2008), p. 16**; Hyndman y Khandakar (2008), p. 11; Hyndman y Khandakar (2008), p. 10 |
| c3-m9-52 | regla | con-matiz | Con stepwise = FALSE se explora un conjunto de modelos mucho mayor que con la búsqueda por pasos, y con approximation = FALSE se evitan las aproximaciones; aquí la búsqueda exhaustiva devuelve un MA(1) sin media. | **FPP3, §9.7** |
| c3-m9-23 | regla | propia | Si los log-retornos son ruido blanco, el mejor pronóstico de la variación del mes siguiente es una constante: la media histórica, o cero si la media no se distingue de cero. | — |
| c3-m9-49 | dato | propia | La TRM mensual del curso es el promedio de los valores diarios de cada mes. | — |
| c3-m9-50 | resultado | propia | Las variaciones de un promedio mensual de 21 valores diarios de una caminata aleatoria pura tienen autocorrelación de primer orden de unos 0.25 (0.249). | — |
| c3-m9-24 | regla | con-matiz | El AICc puede comparar modelos con y sin constante sobre los mismos datos, porque cuenta la constante como un parámetro, y auto.arima() decide así si la incluye; no puede comparar modelos con otro orden de diferenciación (ni otra transformación). | **FPP3, §9.6**; FPP3, §9.7; **Hyndman y Khandakar (2008), p. 11** |
| c3-m9-27 | resultado | con-matiz | Aplicar Ljung–Box a los cuadrados de los rendimientos contrasta el agrupamiento de volatilidad (efectos ARCH); sobre los cuadrados de los log-retornos de la TRM no se detecta. | **Cryer y Chan (2008), p. 282**; Cryer y Chan (2008), p. 281 |
| c3-m9-26 | resultado | respaldada | En rendimientos diarios de series financieras es frecuente que el nivel sea incorrelacionado pero sus cuadrados no, y los modelos ARCH y GARCH se plantean para eso. | **Cryer y Chan (2008), p. 285** |
| c3-m10-01 | resultado | con-matiz | Un AR(p) sin ruido equivale a una neurona lineal con una ventana de p entradas: los coeficientes son los pesos y la constante es el sesgo. | **FPP3, §12.4** |
| c3-m10-02 | historica | propia | Los métodos secuenciales modernos pueden leerse como relajaciones, una a una, de los supuestos del AR (linealidad, ventana fija, decaimiento con la distancia); la tabla siguiente las recorre. | — |
| c3-m10-03 | resultado | respaldada | Una red densa con ventana relaja la linealidad del AR: al añadir una capa oculta con activaciones no lineales la red deja de ser lineal. | **FPP3, §12.4** |
| c3-m10-04 | atribucion | pendiente | Las redes RNN, LSTM y GRU relajan la ventana fija del AR: un estado oculto acumula el pasado y la red aprende cuánto recordar y olvidar; su coste es un entrenamiento secuencial costoso y muchos datos. | — |
| c3-m10-05 | atribucion | pendiente | Los transformers temporales relajan el decaimiento con la distancia (la atención puede pesar igual el rezago 1 que el 500), a cambio de un coste cuadrático en la longitud y de aún más datos. | — |
| c3-m10-07 | resultado | propia | El estado oculto de una RNN lineal de una sola unidad sigue la recursión de un AR(1), con la entrada en el lugar de la innovación. | — |
| c3-m10-08 | resultado | propia | En esa recursión lineal el gradiente respecto al estado de k pasos atrás es w^k: con \|w\| < 1 se desvanece y con \|w\| > 1 explota; es la misma cuenta del desvanecimiento de φ^k del AR(1). | — |
| c3-m10-09 | regla | propia | Con T = 100, una LSTM con miles de parámetros puede memorizar la muestra, mientras que el AR(2) tiene cuatro parámetros contando la media y σ². | — |
| c3-m10-10 | regla | con-matiz | Un ARMA da intervalos de pronóstico con una teoría detrás (pesos ψ), aunque tienden a quedar estrechos; el título «calibrados» se reescribe. | **FPP3, §9.8** |
| c3-m10-11 | regla | respaldada | Una red neuronal no parte de un modelo estocástico bien definido, y sus intervalos de pronóstico se obtienen simulando trayectorias futuras. | **FPP3, §12.4** |
| c3-m10-12 | regla | con-matiz | Aunque se use una red, el ARMA es la referencia que hay que batir: un método nuevo se compara con alternativas simples y, si no las supera, no merece consideración. | **FPP3, §5.2** |
| c3-m10-14 | regla | propia | Un asistente de IA entrega código e interpretaciones convincentes de arima(); este capítulo tiene al menos cuatro puntos en los que esa interpretación puede estar mal y hay que verificarlos. | — |
| c3-m10-15 | regla | con-matiz | El AICc no compara modelos con distinto orden de diferenciación d ni en otra escala, pero sí con y sin media. | **FPP3, §9.6**; **FPP3, §9.7** |
| c3-m10-19 | resultado | respaldada | La ACF de un AR decae sin cortarse: exponencialmente si las raíces son reales y como una sinusoide amortiguada (en ondas) si son complejas. | **Cryer y Chan (2008), p. 73**; Cryer y Chan (2008), p. 116 |
| c3-m10-20 | resultado | respaldada | En un AR(p), la PACF teórica en el rezago p es φ_p, y la PACF muestral se obtiene sustituyendo las ρ por las r; en el AR(2) del Módulo 9 la PACF teórica en 2 es el coeficiente φ2. | **Cryer y Chan (2008), pp. 114–115** |
| c3-m10-23 | resultado | respaldada | Para un ARMA(p,q), la ACF decae y, pasado el rezago q, sigue la ecuación en diferencias de orden p que fijan los parámetros autorregresivos (al ritmo de un AR(p)). | **Hamilton (1994), p. 60**; Cryer y Chan (2008), p. 116 |
| c3-m10-24 | regla | respaldada | La PACF de un ARMA(p,q) con p y q positivos decae (no se corta). | **Cryer y Chan (2008), p. 116** |
| c3-m10-25 | regla | con-matiz | Si el coeficiente de mayor orden (φ̂_p o θ̂_q) no es significativo, sobra el parámetro; en las manchas, t = 19.31 y −9.46 en el AR(2) final y t = 2.78 en el θ̂1 del ARMA(2,1) crudo. | **Cryer y Chan (2008), p. 186** |
| c3-m10-28 | resultado | respaldada | Un ARMA(2,2) con φ = (1.1, −0.28) y θ = (0.1, −0.20) tiene la misma ACF que el ARMA(1,1) con φ = 0.7 y θ = 0.5: el factor (1 − 0.4B) está en los dos polinomios y se cancela. | **Hamilton (1994), p. 61** |
| c3-m10-91 | resultado | respaldada | Con un factor común entre los polinomios AR y MA, los coeficientes del modelo grande no son identificables; el daño recae en la estimación, no en el criterio de información. | **Cryer y Chan (2008), p. 187** |
| c3-m10-31 | dato | respaldada | La serie lh de R son 48 mediciones de hormona luteinizante en sangre, tomadas cada 10 minutos. | **ayuda de R, §Description** |
| c3-m10-33 | regla | con-matiz | Si el objetivo fuera pronosticar, convendría comparar el AR(1) y el MA(2) por validación de origen móvil, que es lo que hace el Capítulo 6. | **FPP3, §5.10** |
| c3-m10-90 | regla | respaldada | Que se rechace la normalidad de los residuales es un aviso para los intervalos de pronóstico, que suponen residuales incorrelados y normales. | **FPP3, §9.8** |
| c3-m10-34 | resultado | respaldada | La cota \|ρ1\| ≤ 0.5 se dedujo solo para el MA(1), maximizando θ/(1+θ²). | **Cryer y Chan (2008), p. 58** |
| c3-m10-46 | dato | respaldada | Sobre la serie completa 1700–1988 el AR(2) da un pseudo-periodo de 11.007 años, dentro del rango de duración que FPP3 da para el ciclo de las manchas solares. | **FPP3, §12.4** |
| c3-m10-35 | resultado | propia | El diagnóstico de Ljung–Box del AR(2) a √manchas falla en todas las ventanas de cien años que llegan al siglo XX; no lo explica el tamaño de la muestra, sino el tramo (52 de 190 ventanas pasan). | — |
| c3-m10-38 | atribucion | respaldada | Lectura: FPP3, secciones 9.3 (modelos autorregresivos), 9.4 (modelos de medias móviles) y 5.4 (diagnóstico de residuales). | **FPP3, §9.3**; FPP3, §9.4; FPP3, §5.4 |
| c3-m10-39 | atribucion | pendiente | Lectura: Shumway y Stoffer (4.ª ed.), el tratamiento formal de ARMA, causalidad, invertibilidad y estimación; en la 3.ª edición, secc. 3.2 y 3.6. | Shumway y Stoffer 3.ª, §3.2; Shumway y Stoffer 3.ª, §3.6 |
| c3-m10-41 | atribucion | respaldada | Lectura: Box, Jenkins, Reinsel y Ljung (5.ª ed.), edición del texto clásico de Box y Jenkins que popularizó el modelado ARIMA y a quienes se asocia la estrategia de identificación, ajuste y diagnóstico. | **FPP3, §9.12**; **Cryer y Chan (2008), p. 8** |
| c3-m10-43 | atribucion | respaldada | Lectura opcional: FPP3 §12.4, redes neuronales autorregresivas (NNETAR): una red con una capa oculta que toma los rezagos de la serie como entradas y que, sin neuronas ocultas, equivale a un AR sin las restricciones de estacionariedad. | **FPP3, §12.4** |
| c3-m10-92 | dato | propia | El Capítulo 4 añade el orden de integración d y llega a los modelos ARIMA. | — |
| c3-m10-44 | atribucion | con-matiz | El Capítulo 4 llega a la metodología de Box–Jenkins (la estrategia de identificar, estimar y diagnosticar que se atribuye a Box y Jenkins). | **Cryer y Chan (2008), p. 8**; FPP3, §9.12 |
| c3-m10-45 | atribucion | respaldada | El Capítulo 4 trata el algoritmo de Hyndman–Khandakar, que automatiza la selección de un modelo ARIMA. | **FPP3, §9.7**; FPP3, §9.12; Hyndman y Khandakar (2008), p. 10 |
| c3-m10-93 | regla | respaldada | Los criterios de información no son comparables entre modelos con distinto orden de diferenciación d; la advertencia vuelve en el Capítulo 4. | **FPP3, §9.6** |
| c3-m10-94 | dato | propia | AirPassengers cierra el Capítulo 2, no aparece en el 3, y el Capítulo 5 le ajusta el modelo airline (módulos 5.5 y 5.7) para describir la dependencia que queda en la doble diferencia del logaritmo. | — |

## Cambios de prosa (80: 64 de la primera pasada y 16 de la segunda)

Todos en `ensamblado/cap3/cap3_modulos.html`, aplicados por `r4_marca.py`. La columna «afirmación» es la entrada
a la que va unido el cambio; el texto va sin etiquetas.

| # | afirmación | antes | después | motivo |
|---:|---|---|---|---|
| 1 | c3-m1-21 | Ese atajo de notación es en realidad la herramienta central del análisis clásico de series de tiempo, y conviene presentarla en serio | Ese atajo de notación es en realidad una herramienta muy útil para escribir los modelos de series de tiempo, y conviene presentarla en serio | «La herramienta central del análisis clásico» es una valoración que ninguna fuente hace: FPP3 §9.2 y Hamilton (cap. 2) lo presentan como un recurso muy útil. Se ajusta la frase a eso. |
| 2 | c3-m1-04 | que verás en el Capítulo 5, | que se verá en el Capítulo 5, | segunda pasada: voz impersonal |
| 3 | c3-m1-09 | —el del Box–Jenkins clásico y el de S-PLUS— | —el de algunos textos y el de S-PLUS— | La atribución a «Box–Jenkins clásico» no tiene texto en la caché (la biblioteca tiene las ediciones de Box y Jenkins sin PDF) y ninguna obra leída la hace. Lo que sí dicen las fuentes leídas: Cryer y Chan escriben el MA con signo menos (p. 57) y la ayuda de R atribuye ese signo a la documentación de S-PLUS. |
| 4 | c3-m1-12 | En R los coeficientes son coeficientes en todas partes. | En R los coeficientes son coeficientes del modelo tanto al estimar como al simular (arima() y arima.sim()). | «En todas partes» va más allá de lo que respalda la ayuda de R: polyroot(), por ejemplo, recibe los coeficientes del polinomio (el propio capítulo lo usa así). Se acota a lo que la ayuda de arima() y arima.sim() dice. |
| 5 | c3-m1-16 | De ahí el nombre raíz unitaria. | Se dice entonces que el polinomio tiene una raíz unitaria. | «De ahí el nombre» afirma un origen del término que ninguna fuente leída da. Cryer y Chan (p. 128) usan el término en este sentido; se reescribe para afirmar solo el uso. |
| 6 | c3-m2-30 | Si sustituyes $y_{t-1}$ por $x_1$, $y_{t-2}$ por $x_2$ y así, tienes una regresión múltiple corriente. | Si se sustituye $y_{t-1}$ por $x_1$, $y_{t-2}$ por $x_2$ y así, queda una regresión múltiple corriente. | segunda pasada: voz impersonal |
| 7 | c3-m2-02 | y por eso los errores estándar y la teoría asintótica no son las de la regresión clásica. | y por eso no valen los resultados de muestra finita de la regresión clásica: el estimador de mínimos cuadrados es sesgado y los estadísticos $t$ y $F$ habituales solo se justifican de forma asintótica. | La frase decía que la teoría asintótica no es la de la regresión clásica; Hamilton (§8.2, caso 4, pp. 215-216) dice lo contrario: con una autorregresión estacionaria y errores independientes los resultados asintóticos son los mismos que para regresores estocásticos independientes, y los estadísticos t y F usuales dan pruebas asintóticamente válidas. Lo que falla son los resultados de muestra finita. |
| 8 | c3-m2-18 | De un mismo sistema de ecuaciones que relaciona los $\phi$ con las autocovarianzas del proceso | De un mismo sistema de ecuaciones, el de Yule–Walker, que relaciona los $\phi$ con las autocovarianzas del proceso | El nombre estaba solo en el encabezado; se nombra en la frase que lleva la cita, para que la cita vaya pegada al nombre. Ninguna fuente leída atribuye las ecuaciones a Yule y a Walker con año ni obra: el capítulo no lo hace. |
| 9 | c3-m3-02 | Coinciden solo en el nombre, que es un accidente histórico. | Coinciden en el nombre, no en el uso: un modelo de medias móviles sirve para pronosticar valores futuros, y el suavizamiento, para estimar la tendencia-ciclo de valores pasados. | «Un accidente histórico» no tiene pasaje en ninguna fuente leída (afirma algo sobre el origen del nombre); Cryer y Chan (p. 57) dan incluso una razón para el nombre (los pesos 'se mueven'). FPP3 §9.4 sí dice en qué se distinguen. |
| 10 | c3-m3-11 | no hay ningún $\theta$ que lo produzca. Pero la cota | no hay ningún $\theta$ cuya $\rho_1$ valga eso, y el MA(1) queda en duda: una $r_1$ muestral puede pasar de $0.5$ aunque la $\rho_1$ verdadera no lo haga. Pero la cota | Cryer y Chan (p. 150) advierten que \|r1\| > 0.5 es posible aunque \|ρ1\| < 0.5: entonces el método de momentos falla y el MA(1) queda 'en considerable duda'. 'No hay ningún θ que lo produzca' sin más trataba la r1 muestral como si fuera la ρ1 teórica. |
| 11 | c3-m3-11 | Así que $r_1 = 0.8$ descarta también el MA(2) | Así que $r_1 = 0.8$ pone en duda también el MA(2) | Coherencia con la frase anterior: la fuente habla de duda, no de descarte. |
| 12 | c3-m3-11 | Sirve para descartar modelos sin ajustar nada. | Sirve para poner en duda modelos sin ajustar nada. | Coherencia con las dos frases anteriores. |
| 13 | c3-m3-11 | ver $r_1 = 0.55$ descarta un MA(1), no descarta un MA(2). | ver $r_1 = 0.55$ pone en duda un MA(1), no un MA(2). | ejercicio 2 del M10: repite c3-m3-11; la fuente (Cryer y Chan, p. 150) habla de duda, no de descarte |
| 14 | c3-m3-11 | Si en un correlograma muestral ves $r_1 = 0.8$ y quisieras ajustar un MA(1), | Si un correlograma muestral da $r_1 = 0.8$ y se quisiera ajustar un MA(1), | segunda pasada: voz impersonal |
| 15 | c3-m3-14 | Por eso la PACF decae como $\|\theta\|^k$, | Por eso la PACF decae exponencialmente, a un ritmo que acaba siendo el de $\|\theta\|^k$, | La forma exacta (Cryer y Chan, ec. 6.2.6) es −θ^k(1−θ²)/(1−θ^(2(k+1))) con su convenio de resta: es \|θ\|^k multiplicado por un factor que tiende a 1−θ²; 'decae como \|θ\|^k' a secas era una aproximación asintótica. |
| 16 | c3-m3-15 | el último coeficiente de la regresión de $y_t$ sobre sus $k$ valores anteriores. En un AR($p$) esa regresión ya contiene | el último coeficiente de la proyección lineal (la regresión poblacional) de $y_t$ sobre sus $k$ valores anteriores. En un AR($p$) esa proyección ya contiene | segunda pasada, c3-m3-15 (verificador A): Hamilton (p. 111) habla de la proyección lineal poblacional; con datos, el último coeficiente de una regresión por MCO no coincide con pacf() (lo mismo que c2-m4-05) |
| 17 | c3-m3-32 | por qué el software la impone. | por qué el software la impone por defecto. | «La impone» sin matiz es falso en R y en statsmodels: es el comportamiento por defecto y se puede evitar (ver c3-m4-31). |
| 18 | c3-m3-32 | # arima() devuelve siempre la version invertible | # arima() devuelve por defecto la version invertible | comentario del bloque de R del M3: el «siempre» que c3-m3-32 y c3-m4-31 quitan de la prosa (con transform.pars = FALSE no la devuelve; r4_software.R) |
| 19 | c3-m4-05 | lo cual es absurdo. | lo cual no tiene mucho sentido. | FPP3 §9.4 dice que ninguna de las dos situaciones ('make much sense') tiene sentido y por eso exige \|θ1\| < 1; 'absurdo' era más fuerte que la fuente. |
| 20 | c3-m4-31 | y la razón de fondo por la que el software siempre te devuelve la raíz invertible. | y la razón de fondo por la que el software, por defecto, devuelve la raíz invertible. | 'Siempre' es falso: arima() de R con transform.pars = FALSE y un valor inicial no invertible, y ARIMA de statsmodels con enforce_invertibility = False, devuelven una raíz no invertible (ejecutado, ver `software`). (segunda pasada: además, voz impersonal.) |
| 21 | c3-m5-03 | Menos parámetros significa estimaciones más precisas y pronósticos más estables, que es de lo que se trata. | Tener menos parámetros deja menos margen de error al estimarlos y, con frecuencia, mejores pronósticos fuera de la muestra, que es de lo que se trata. | Ninguna fuente leída dice 'estimaciones más precisas y pronósticos más estables' como regla general: Hamilton (p. 109) dice que cuantos más parámetros hay que estimar, más margen hay para equivocarse, y que los ARMA univariantes con p o q pequeños a menudo pronosticaron mejor que los modelos grandes. |
| 22 | c3-m5-04 | es un ciclo de cuatro pasos que se repite hasta que el diagnóstico queda limpio, y la tabla solo interviene en el tercero. | es un ciclo que se repite hasta que el diagnóstico queda limpio, y que aquí se recorre en cuatro pasos, de los cuales la tabla solo interviene en el tercero. | Cryer y Chan (p. 8) describen el ciclo en tres pasos y FPP3 §9.7 en siete: 'cuatro pasos' es la división del capítulo, no de la fuente. |
| 23 | c3-m5-05 | la parte MA no manda y hay que mirar la PACF | no es un MA puro y hay que mirar la PACF | 'La parte MA no manda' no tiene pasaje, y en un ARMA mixto la ACF también decae (c3-m5-12). Lo que sí dice FPP3 §9.5 es que la huella de un MA(q) es el pico en el rezago q de la ACF y nada más allá; si decae, no es un MA puro. |
| 24 | c3-m5-07 | la serie no es estacionaria: esto no es un problema de identificación | suele ser síntoma de que la serie no es estacionaria: esto no es un problema de identificación | Cryer y Chan (p. 128) dicen que el decaimiento lineal de la ACF muestral 'suele tomarse como síntoma' de no estacionariedad; la frase decía 'la serie no es estacionaria' sin matiz. |
| 25 | c3-m5-08 | envuélvelo en as.numeric(). | conviene envolverlo en as.numeric(). | segunda pasada: voz impersonal |
| 26 | c3-m5-11 | Decae tras el rezago $p$ | Decae, sin cortarse | La celda 'decae tras el rezago p' de la PACF del ARMA no tiene pasaje: Cryer y Chan (cuadro 6.3, p. 116) escriben 'tails off' para la ACF y la PACF del ARMA y dicen que sus valores no nulos son infinitos (p. 116). Con las ACF y PACF teóricas de dos ARMA ejecutadas (ARMA(1,1) con φ = 0.7 y θ = 0.5; ARMA(2,1)) la PACF sí decae geométricamente desde el rezago p, pero eso es comprobación de dos casos, no un resultado de la fuente. |
| 27 | c3-m5-14 | aquí, para $p \ge 1$, no hay forma corta en función de los parámetros y hay que sumar la serie de los $\psi$. | aquí, para $p \ge 1$, no hay una forma corta general en función de los parámetros y hay que pasar por los $\psi$: sumando su serie, como en la derivación de más abajo, o resolviendo un sistema lineal en el que entran. | Cryer y Chan (apéndice C, p. 85) calculan la ACF de un ARMA resolviendo un sistema lineal en el que entran los ψ, y la ayuda de ARMAacf cita otro sistema lineal (Brockwell y Davis); sumar la serie de ψ es una vía, no la única. 'Sin forma corta' vale en general (el ARMA(1,1) sí la tiene y el capítulo la da a continuación). |
| 28 | c3-m5-18 | recuerda este simulador: casi nunca es que el modelo no exista, es que la muestra es corta. | conviene recordar este simulador: con una muestra corta, hasta un proceso que sí corresponde a una fila de la tabla puede dar un correlograma que no encaja. | 'Casi nunca' es una generalización empírica sin fuente: las fuentes (Cryer y Chan, p. 112) piden no esperar que la ACF muestral imite a la teórica en detalle, y piden varios candidatos y diagnóstico (FPP3 §9.5–9.7). La frase nueva dice lo que el simulador muestra. |
| 29 | c3-m5-18 | Cuando en el Módulo 9 veas un correlograma | Cuando en el Módulo 9 aparezca un correlograma | segunda pasada: voz impersonal |
| 30 | c3-m5-20 | Si ves un ARMA con $\hat\phi_1 \approx -\hat\theta_1$ y errores estándar grandes, prueba el modelo más pequeño antes de interpretar nada. | Ante un ARMA con $\hat\phi_1 \approx -\hat\theta_1$ y errores estándar grandes, conviene probar el modelo más pequeño antes de interpretar nada. | segunda pasada: voz impersonal |
| 31 | c3-m6-06 | Si miras 20 rezagos de una serie que es ruido blanco puro, esperas que $20 \times 0.05 = 1$ de ellos se salga por puro azar. | Al mirar 20 rezagos de una serie que es ruido blanco puro, lo esperable es que $20 \times 0.05 = 1$ de ellos se salga por puro azar. | segunda pasada: voz impersonal |
| 32 | c3-m6-07 | Ver uno o dos picos fuera de la banda no es evidencia de nada; por eso existe la prueba de Ljung–Box del Módulo 8, que evalúa todos los rezagos a la vez. | Uno o dos picos que apenas asoman fuera de la banda no bastan como evidencia; uno muy grande, o bastantes más del 5 % de los rezagos fuera, sí. Por eso existe la prueba de Ljung–Box del Módulo 8, que evalúa esos 20 rezagos a la vez. | segunda pasada, c3-m6-07 y c3-m6-08 (verificador A): FPP3 §2.9 dice que una barra grande, o bastante más del 5 % fuera, sí indican que no es ruido blanco (como quedó c2-m2-08); y §5.4, que la prueba mira las primeras ℓ autocorrelaciones, no «todos los rezagos» |
| 33 | c3-m7-01 | Número anual de manchas solares (Wolf number) entre 1770 y 1869, $T = 100$ observaciones. Es la ventana centenaria sobre la que Udny Yule inventó en 1927 el modelo autorregresivo, precisamente para explicar por qué el Sol tiene un ciclo que se repite "más o menos" cada once años sin ser nunca exactamente periódico. Está en R como sunspot.year. | Número anual de manchas solares entre 1770 y 1869, $T = 100$ observaciones, un tramo de sunspot.year, la serie de R que va de 1700 a 1988. Con los números de manchas de Wolfer de 1749 a 1924, Udny Yule propuso en 1927 lo que hoy se llama un modelo autorregresivo: ajustó la regresión de cada valor sobre los dos anteriores y comparó las manchas con un péndulo que recibe pequeños impulsos al azar, de trazo suave pero con amplitud y fase que cambian sin cesar. El periodo de las manchas se estimaba entonces en algo más de once años. | c3-m7-01 a -03: leído Yule (1927). No usó la ventana 1770–1869 sino la serie de Wolfer entera (1749–1924, p. 275); no dice «inventar» ni «autorregresivo»: ajusta una ecuación de regresión sobre los dos valores anteriores y la compara con un péndulo perturbado (p. 294); da como estimación habitual del periodo algo más de 11 años (p. 276). «Wolf number» no está en ninguna fuente leída: Yule escribe «Wolfer». |
| 34 | c3-m7-01 | El AR(2) es el modelo que la identificación proponía y el que hizo famoso a Yule, pero: | El AR(2) es el modelo que la identificación proponía, pero: | M8: retira «el que hizo famoso a Yule», valoración sin pasaje; lo que Yule hizo queda dicho, con su cita, en el recuadro del M7 (c3-m7-02) |
| 35 | c3-m7-06 | Solo sirve para modelos AR puros. Es explícito, rápido y no necesita optimización. | Es explícito, rápido y no necesita optimización. Da estimaciones bastante buenas en modelos AR puros y es muy ineficiente si hay parte MA. | «Solo sirve para modelos AR puros» es más fuerte que las fuentes: Cryer y Chan (p. 152) dicen que con parte MA los estimadores de momentos son muy ineficientes (y p. 150, que con MA(1) pueden no existir), no que no sirvan; Shumway y Stoffer 3.ª (p. 123) dicen que no son óptimos. |
| 36 | c3-m7-09 | Es el más eficiente y el que da errores estándar fiables. | Aprovecha toda la información de los datos; sus errores estándar salen de la hessiana de la log-verosimilitud y pueden ser solo una guía aproximada. | Cryer y Chan (p. 160) dicen que las propiedades de muestra grande de máxima verosimilitud y de mínimos cuadrados (condicionales o no) son idénticas, así que «el más eficiente» no se sostiene; la ayuda de R advierte que la matriz de varianzas sale de la hessiana y puede ser solo una guía aproximada, así que «fiables» tampoco. |
| 37 | c3-m7-35 | CSS es más barato y sirve para arrancar; ML es más preciso. | CSS es más barato y sirve para arrancar; ML cuenta además con las primeras observaciones, cuyo efecto pesa más en series de longitud moderada. | segunda pasada, c3-m7-35 (verificador B): Hamilton (p. 123) no dice que ML sea «más preciso» (con muestra grande coinciden); lo que dicen Cryer y Chan (p. 158) es que en series de longitud moderada los valores iniciales pesan más |
| 38 | c3-m7-14 | parece un abismo, pero no miden lo mismo: | parece un abismo, pero no salen del mismo cálculo: | Los dos estiman la varianza de la innovación: Cryer y Chan dan σ² de Yule–Walker como (1 − φ̂1 r1 − … − φ̂p rp)·s² (p. 151) y la ayuda de R llama a sigma2 de arima() «la MLE de la varianza de las innovaciones». Lo que difiere es el cálculo, no lo que miden. |
| 39 | c3-m8-24 | Añadir parámetros siempre mejora la verosimilitud. | Añadir parámetros nunca empeora la verosimilitud. | segunda pasada (verificador B): el M8 decía «siempre mejora» y el M10 «casi siempre mejora»; lo que se cumple siempre es que no empeora |
| 40 | c3-m8-24 | Añadir un parámetro casi siempre mejora la verosimilitud; | Añadir un parámetro nunca empeora la verosimilitud; | segunda pasada: resumen del M10, la misma frase |
| 41 | c3-m8-36 | $$Q^{*}(h) = T\sum_{k=1}^{h}\hat r_k^2 \;\sim\; \chi^2_h$$ | $$Q_{BP}(h) = T\sum_{k=1}^{h}\hat r_k^2 \;\sim\; \chi^2_h$$ | segunda pasada, notación (verificador B): el capítulo llamaba Q* al de Box–Pierce y Q al de Ljung–Box, al revés que FPP3 §5.4 y Cryer y Chan (pp. 183–184); Q(h) se conserva para Ljung–Box (como en el capítulo 4) y el de Box–Pierce pasa a Q_BP(h) |
| 42 | c3-m8-36 | Con el factor $T$, $Q^{*}$ sale pequeño y la prueba rechaza menos de lo que debería. | Con el factor $T$, $Q_{BP}$ sale pequeño y la prueba rechaza menos de lo que debería (en Cryer y Chan el estadístico de Box–Pierce se escribe $Q$ y el de Ljung–Box, $Q^{*}$). | segunda pasada, notación: la frase citaba la p. 184 con los símbolos cambiados |
| 43 | c3-m9-01 | Los números de manchas solares son conteos. | Los números de manchas solares son índices construidos a partir de conteos. | c3-m9-01: el número de manchas es una suma ponderada de conteos de manchas y de grupos (Cryer y Chan, p. 392), y la ayuda de R lo da redondeado a un decimal: no son conteos enteros |
| 44 | c3-m9-42 | , la escala de Box–Cox del Capítulo 2, cuyo criterio de Guerrero busca justamente que $s_i/\bar y_i^{\,1-\lambda}$ sea homogéneo entre bloques. | , la escala de Box–Cox del Capítulo 2. El criterio de Guerrero, el que ofrecen para elegir $\lambda$, busca justamente que $s_i/\bar y_i^{\,1-\lambda}$ sea homogéneo entre bloques. | c3-m9-42: la atribución a Guerrero se respalda con FPP3 §3.1 (como en c2-m8-13) y la cita se genera en modo narrativo; la descripción de cómo funciona el criterio queda aparte (c3-m9-43) |
| 45 | c3-m9-03 | La raíz cuadrada, en cambio, está definida en cero y es la transformación estabilizadora clásica para conteos. | La raíz cuadrada, en cambio, está definida en cero y se señala como útil con datos de tipo Poisson. | c3-m9-03: «la transformación clásica para conteos» no tiene obra detrás; Cryer y Chan (p. 101) dicen que la raíz cuadrada es útil con datos de tipo Poisson |
| 46 | c3-m9-06 | El ciclo solar documentado por los astrónomos es de aproximadamente 11 años. Corregir la escala no solo arregló el diagnóstico: acercó la estimación al valor físico. | Ya en 1927 se daba como estimación habitual del periodo de las manchas solares algo más de 11 años. Corregir la escala no solo arregló el diagnóstico: acercó la estimación a ese valor. | c3-m9-06: «documentado por los astrónomos» y «valor físico» no tenían obra; Yule (1927, p. 276) sí da la estimación habitual de algo más de 11 años |
| 47 | c3-m9-06 | y el pseudo-periodo se acercó al ciclo solar real. | y el pseudo-periodo se acercó a la estimación habitual del ciclo de las manchas. | resumen del M10: repite c3-m9-06, con las mismas palabras que ahora usa el M9 |
| 48 | c3-m9-06 | anios; el ciclo solar documentado es ~11 | anios; la estimacion habitual del periodo es algo mas de 11 (Modulo 9) | segunda pasada (verificador B): el comentario de código repetía «documentado», que la prosa ya no dice |
| 49 | c3-m9-08 | cualquier transformación de potencia moderada hace el mismo trabajo | las dos transformaciones de potencia probadas hacen el mismo trabajo | c3-m9-08: «cualquier potencia moderada» generaliza a partir de dos valores de λ (0.5 y 0.3062) |
| 50 | c3-m9-40 | El texto de Hyndman y Athanasopoulos (FPP3, sección 9.5) da para el AR(2) | dan para el AR(2) | c3-m9-40: la cita se genera en modo narrativo en lugar del nombre y la sección tecleados |
| 51 | c3-m9-12 | mediana de las manchas, no su media. | mediana de las manchas, y no su media, si la distribución en la escala de la raíz es simétrica. | c3-m9-12: FPP3 §5.6 lo dice con su condición: por lo común, y suponiendo simetría en la escala transformada |
| 52 | c3-m9-15 | y esa asimetría es una no linealidad que ningún modelo lineal ARMA puede capturar. | y esa asimetría sugiere una no linealidad que un modelo ARMA con errores normales no puede capturar. | c3-m9-15: Cryer y Chan (pp. 384 y 396) lo dicen de los procesos ARMA gaussianos (reversibles en el tiempo) y como sugerencia de no linealidad, no de «ningún modelo lineal» |
| 53 | c3-m9-16 | quedarán algo mal calibrados. | pueden quedar algo mal calibrados. | c3-m9-16: FPP3 §9.8 dice «pueden ser incorrectos», no que lo serán |
| 54 | c3-m9-17 | Allí quedó establecido que tiene una raíz unitaria | Allí se concluyó que tiene una raíz unitaria | c3-m9-17: «establecido» es más fuerte que lo que el Módulo 6 del capítulo 2 hace (dos pruebas sobre una muestra finita); Hamilton (p. 445) advierte que con muestra finita no se distingue una raíz unitaria de una cercana a 1 |
| 55 | c3-m9-18 | , que es la variación porcentual mensual y la magnitud habitual en finanzas ($T = 137$). | , el rendimiento continuo de las finanzas, multiplicado por $100$ para leerlo como variación porcentual, lectura que es una buena aproximación mientras la variación sea pequeña ($T = 137$). | c3-m9-18: log(1 + X) ≈ X solo para X pequeño (Cryer y Chan, p. 99); «la magnitud habitual en finanzas» se respalda con la definición de p. 278 |
| 56 | c3-m9-20 | y se queda con el de menor AICc (el Capítulo 4 detalla cómo busca). | y se queda con el de menor AICc (el artículo que la presentó usaba el AIC; el AICc es hoy el criterio por defecto del paquete; el Capítulo 4 detalla cómo busca). | segunda pasada, c3-m9-20 (verificador B): la cita de Hyndman y Khandakar (2008) cerraba una frase que decía AICc, y el artículo elige por AIC; el AICc por defecto se comprobó con formals(auto.arima)$ic |
| 57 | c3-m9-24 | Lo que el AICc no puede comparar son modelos ajustados a datos distintos: otro orden de diferenciación u otra transformación. | Lo que el AICc no puede comparar son modelos ajustados a datos distintos, como los de otro orden de diferenciación o los de otra transformación. | c3-m9-24: la cita de FPP3 §9.6 cubre la diferenciación; se separa la parte de la transformación, que es extensión del capítulo |
| 58 | c3-m9-23 | pronóstico de la variación del mes que viene es la media histórica. | pronóstico de la variación del mes que viene es una constante: la media histórica, o cero si, como aquí, la media no se distingue de cero. | segunda pasada, c3-m9-23 (verificador B): dos párrafos antes el capítulo elige el ruido blanco sin media, cuyo pronóstico es cero |
| 59 | c3-m9-26 | En datos diarios de la misma tasa el resultado suele ser el opuesto —el nivel es ruido blanco y el cuadrado no— y esa es la puerta de entrada a los modelos ARCH y GARCH. La frecuencia de muestreo cambia el fenómeno que se ve. | En los rendimientos diarios de series financieras es frecuente el resultado opuesto —el nivel es ruido blanco y el cuadrado no— y esa es la puerta de entrada a los modelos ARCH y GARCH. Saber si ocurre con la TRM exigiría repetir la prueba con los datos diarios. | c3-m9-26 y c3-m9-28: ninguna fuente leída habla de «datos diarios de la misma tasa» (el ejemplo de Cryer y Chan es un fondo bursátil) ni de que la frecuencia de muestreo cambie el fenómeno; sí dicen que esa estructura es común en series financieras y que los modelos GARCH se introducen para ella |
| 60 | c3-m10-01 | Es exactamente una neurona lineal | Equivale a una neurona lineal | FPP3 §12.4 dice «equivalente», y con una salvedad: la red sin neuronas ocultas coincide con el AR(p) salvo que no impone las restricciones de estacionariedad; «exactamente» iba más allá. |
| 61 | c3-m10-02 | Todo lo que hicieron los métodos secuenciales modernos fue relajar, uno por uno, los supuestos que hay detrás de esa expresión. | Los métodos secuenciales modernos pueden leerse como una forma de relajar, uno por uno, los supuestos que hay detrás de esa expresión. | «Todo lo que hicieron… fue» es una afirmación histórica sobre el desarrollo de esos métodos y ninguna obra de la biblioteca la respalda; se reescribe como una lectura del capítulo. |
| 62 | c3-m10-02 | Situar el AR como el antepasado directo de los métodos secuenciales del aprendizaje profundo | Situar el AR como el punto de partida de los métodos secuenciales del aprendizaje profundo | «Antepasado directo» es una genealogía de ideas sin fuente. FPP3 §12.4 solo respalda que una red autorregresiva usa los rezagos como entradas igual que un AR. |
| 63 | c3-m10-02 | El AR es la idea original | El AR como punto de partida | «La idea original» afirma una prioridad histórica que ninguna obra de la biblioteca respalda (c3-m10-47). |
| 64 | c3-m10-07 | es un AR(1): $h_t = w\,h_{t-1} + u\,x_t$. | sigue la misma recursión que un AR(1): $h_t = w\,h_{t-1} + u\,x_t$, con la entrada $u\,x_t$ en el lugar de la innovación $\varepsilon_t$. | La recursión h_t = w h_{t-1} + u x_t es un AR(1) solo si u x_t es ruido blanco; con una serie observada como entrada es un filtro autorregresivo de esa entrada. «Es un AR(1)» necesitaba esa condición. |
| 65 | c3-m10-08 | El problema del gradiente que se desvanece en las RNN y el desvanecimiento de $\phi^k$ que vimos al desarrollar el AR(1) hacia atrás son el mismo fenómeno matemático. | En este caso lineal, el gradiente que se desvanece en una RNN y el desvanecimiento de $\phi^k$ que se vio al desarrollar el AR(1) hacia atrás son el mismo fenómeno matemático. | Se acota a lo que se deriva en el recuadro (el caso lineal de una unidad): la afirmación general sobre el problema del gradiente en las RNN necesitaría una obra de aprendizaje profundo que la biblioteca no tiene. Se quita el «vimos» (voz impersonal). |
| 66 | c3-m10-09 | sobre cien observaciones memoriza la muestra | sobre cien observaciones puede memorizar la muestra | Sin fuente, «memoriza» es una afirmación categórica sobre el comportamiento de una red; se vuelve condicional. |
| 67 | c3-m10-10 | Intervalos de pronóstico calibrados. Un ARMA da intervalos con una teoría detrás (los pesos $\psi$ del Módulo 4). Cuantificar bien la incertidumbre en una red exige trabajo adicional que a menudo no se hace. | Intervalos de pronóstico con una teoría detrás. Un ARMA da intervalos que parten de los pesos $\psi$ del Módulo 4, aunque tienden a quedar estrechos. Una red no parte de un modelo estocástico bien definido, y sus intervalos exigen simular trayectorias futuras. | FPP3 §9.8 dice que los intervalos de un ARIMA tienden a ser demasiado estrechos, así que «calibrados» contradice la fuente (y el propio Módulo 9 admite que quedan algo mal calibrados). Lo de la red se acota a lo que dice FPP3 §12.4 (no hay modelo estocástico bien definido y se simula); «a menudo no se hace» es una generalización empírica sin respaldo. |
| 68 | c3-m10-12 | Aunque vayas a usar una red, el ARMA es el benchmark que hay que batir. Un modelo complejo que no supera a un AR(2) no es un modelo complejo: es un modelo complejo mal ajustado. | Aunque vayas a usar una red, el ARMA es, en este curso, el benchmark que hay que batir: un método nuevo se compara con alternativas simples, y si no las supera no merece consideración. Un modelo complejo que no supera a un AR(2) no justifica su complejidad. | FPP3 §5.2 fija como referencia cuatro métodos simples (no el ARMA) y concluye que un método que no los supera «no merece consideración»; no dice que un modelo complejo que no gana esté «mal ajustado» (puede no haber estructura no lineal que aprender). |
| 69 | c3-m10-14 | en los que esa interpretación suele estar mal y | en los que esa interpretación puede estar mal y | «Suele estar mal» es una afirmación empírica sobre el comportamiento de los asistentes, sin medición ni fuente; se vuelve condicional. |
| 70 | c3-m10-24 | Decae; desde el rezago $p+1$ | Decae | Ninguna fuente fija desde qué rezago decae la PACF de un ARMA. Cryer y Chan (Exhibit 6.3) y la tabla de Shumway dicen solo que «decae». Además, «desde p+1» no vale en general: con ARMAacf(pacf = TRUE) en un ARMA(1,2) (φ = 0.3; θ = 0.6 y 0.4) la PACF no es monótona a partir del rezago 2 (\|φ44\| > \|φ33\|). |
| 71 | c3-m10-91 | que penaliza al grande y suele acertar, sino la estimación: los cuatro coeficientes del modelo grande no son identificables, sus errores estándar se disparan y ninguno parece significativo. | que penaliza al grande, sino la estimación: los cuatro coeficientes del modelo grande no son identificables, sus errores estándar pueden dispararse y es posible que ninguno parezca significativo. | «Suele acertar», «se disparan» y «ninguno parece significativo» son generalizaciones sin fuente que además fallan en una simulación propia (cinco semillas, ARMA(1,1) verdadero con φ = 0.7 y θ = 0.5, n = 300, ML: en una los cuatro coeficientes del ARMA(2,2) salen significativos y su AIC es menor que el del ARMA(1,1); en otras dos salen con errores estándar grandes y casi todos insignificantes; en las dos restantes los errores estándar no se pueden calcular). Cryer y Chan p. 187 respaldan que los parámetros no son únicos; no dicen nada de los errores estándar. |
| 72 | c3-m10-35 | tengan más datos que la de Yule o menos. | tengan más datos que la de 1770–1869 o menos. | Yule (1927, p. 275) usó la serie entera, 1749–1924: 1770–1869 no es «su» ventana |
| 73 | c3-m10-35 | no un artefacto de la ventana de Yule. | no un artefacto de la ventana 1770–1869. | Yule (1927, p. 275) usó la serie entera, 1749–1924: 1770–1869 no es «su» ventana |
| 74 | c3-m10-35 | menos datos que la ventana de Yule ($n = 89$) | menos datos que la ventana 1770–1869 ($n = 89$) | Yule (1927, p. 275) usó la serie entera, 1749–1924: 1770–1869 no es «su» ventana |
| 75 | c3-m10-35 | La de Yule es una de las favorables; | La de 1770–1869 es una de las favorables; | Yule (1927, p. 275) usó la serie entera, 1749–1924: 1770–1869 no es «su» ventana |
| 76 | c3-m10-46 | Sobre la serie completa da $11.007$, notablemente cerca del ciclo documentado. | Sobre la serie completa da $11.007$, dentro del rango de duración que se da al ciclo de las manchas. | «Notablemente cerca del ciclo documentado» no tenía fuente (el ciclo físico no está en ninguna obra en caché). FPP3 §12.4 sí da un rango de duración del ciclo de las manchas, y 11.007 cae dentro de él. La redacción no repite las cifras del rango. |
| 77 | c3-m10-38 | Hyndman &amp; Athanasopoulos, FPP3 — secciones 9.3 (modelos autorregresivos), 9.4 (modelos de medias móviles) y 5.4 (diagnóstico de residuales). Acceso abierto en | , Forecasting: Principles and Practice (3.ª ed.): esa sección (modelos autorregresivos), la 9.4 (modelos de medias móviles) y la 5.4 (diagnóstico de residuales). Acceso abierto en | La obra y la primera sección las escribe el generador de citas (modo narrativo), como en el capítulo 2 (c2-m9-23); el título y la edición coinciden con referencias.json. |
| 78 | c3-m10-39 | Shumway &amp; Stoffer, Time Series Analysis and Its Applications — capítulo 3, secciones 3.1 a 3.5: es el tratamiento formal de ARMA, causalidad, invertibilidad y estimación, con las manchas solares entre sus ejemplos. | Shumway &amp; Stoffer, Time Series Analysis and Its Applications (4.ª ed.): el tratamiento formal de ARMA, causalidad, invertibilidad y estimación. En la 3.ª edición (2011) son las secc. 3.2 (modelos ARMA, con la causalidad y la invertibilidad) y 3.6 (estimación); la numeración de la 4.ª puede ser otra. | En la 3.ª edición el cap. 3 numera 3.2 ARMA (causalidad e invertibilidad dentro de ella) y 3.6 estimación, de modo que «3.1 a 3.5» no cubría la estimación. «Con las manchas solares entre sus ejemplos» no aparece en el cap. 3 de la 3.ª edición (solo en el cap. 1 y en la lista de datos); la 4.ª no se leyó, así que se retira. Mismo tratamiento que c2-m9-24. |
| 79 | c3-m10-41 | Box, Jenkins, Reinsel &amp; Ljung — capítulos 3 y 6, la fuente original de la metodología de identificación y de la prueba de Ljung–Box. | Box, Jenkins, Reinsel &amp; Ljung, Time Series Analysis: Forecasting and Control (5.ª ed.): una edición del texto clásico de Box y Jenkins que popularizó el modelado ARIMA, a quienes se asocia la estrategia de identificación, ajuste y diagnóstico. | Sin el texto del libro no se sostienen ni «capítulos 3 y 6» ni «la fuente original de la prueba de Ljung–Box» (Cryer y Chan §8.1 atribuyen esa prueba a un artículo de Ljung y Box de 1978, no a este libro). La frase queda reducida a lo que FPP3 §9.12 y Cryer y Chan p. 8 dicen de la obra y de sus autores. |
| 80 | c3-m10-43 | Hyndman &amp; Athanasopoulos, sección 12.4 (redes neuronales autorregresivas, NNETAR), que es literalmente un AR con una capa oculta. | , la sección sobre redes neuronales: la red autorregresiva que ajusta NNETAR es una red con una capa oculta que toma como entradas los rezagos de la serie y que, sin neuronas ocultas, equivale a un AR sin las restricciones de estacionariedad. | FPP3 §12.4 no dice que NNETAR sea «literalmente un AR con una capa oculta»: la red autorregresiva NNAR(p, k) tiene p rezagos como entradas y k neuronas en una capa oculta, y con k = 0 equivale a un ARIMA(p,0,0) sin las restricciones de estacionariedad. La obra y la sección las escribe el generador de citas (modo narrativo). |

Los que más pesan:

- **El recuadro de Yule (M7).** Decía que Yule «inventó en 1927 el modelo autorregresivo» sobre «la ventana
  centenaria» 1770–1869. Leído Yule (1927): usó la serie de Wolfer **entera, de 1749 a 1924** (p. 275), ajustó la
  regresión de cada valor sobre los dos anteriores y la comparó con un péndulo perturbado (p. 294), y da «algo más de
  11 años» como estimación habitual del periodo (p. 276). El recuadro dice ahora eso, con sus citas. «Wolf number»
  sale: Yule escribe «Wolfer». En el M10, «la ventana de Yule» pasa a «la ventana 1770–1869» (cuatro veces), y en
  el M8 sale «el que hizo famoso a Yule».
- **El ciclo de 11 años (M9).** «Documentado por los astrónomos» y «valor físico» no tenían obra; queda «ya en 1927
  se daba como estimación habitual… algo más de 11 años», con Yule (p. 276). FPP3 §12.4 (rango de 9 a 14 años)
  queda como segunda fuente y es la cita del ejercicio 3 del M10.
- **c3-m2-02 seguía discrepando de la fuente** tras la R1: «la teoría asintótica no es la de la regresión clásica».
  Hamilton (pp. 215–216) dice que los t y F usuales son asintóticamente válidos; lo que falla es la muestra finita.
- **«arima() devuelve siempre la invertible»** (M3, M4 y un comentario de código): es el comportamiento por
  defecto; con `transform.pars = FALSE` y un valor inicial no invertible devuelve la otra raíz (`r4_software.out`).
- **«descarta el MA(1)»** → «pone en duda» (M3 y ejercicio 2 del M10): Cryer y Chan (p. 150) avisan de que una r₁
  muestral puede pasar de 0.5 aunque la ρ₁ verdadera no lo haga.
- **Yule–Walker «solo sirve para AR puros»** y **ML «el más eficiente»** (M7): Cryer y Chan dicen «muy ineficiente
  con parte MA» (p. 152) y que ML y mínimos cuadrados tienen las mismas propiedades de muestra grande (p. 160).
- **La PACF del ARMA** en las dos tablas de identificación (M5 y M10): «decae tras el rezago p» / «desde el rezago
  p+1» no tiene fuente y no vale en general; queda «Decae, sin cortarse» / «Decae» (Cryer y Chan, cuadro 6.3).
- **El puente con las redes (M10):** «exactamente una neurona lineal», «antepasado directo», «la idea original»,
  «intervalos calibrados» (FPP3 §9.8 dice que tienden a quedar estrechos), «literalmente un AR con una capa oculta»
  (FPP3 §12.4: sin neuronas ocultas equivale a un AR sin las restricciones de estacionariedad).
- **Las lecturas (M10):** FPP3 con cita generada y los títulos de sección leídos; Shumway y Stoffer por temas, con
  la numeración de la 3.ª dicha como tal (`pendiente`); Box et al. sin «capítulos 3 y 6» ni «la fuente original de
  la prueba de Ljung–Box»; NNETAR como lo describe FPP3 §12.4.

## Lo que queda `pendiente`, agrupado por la obra que falta

- **c3-m9-43** · El criterio de Guerrero busca que el cociente entre la desviación y el nivel elevado a 1 − λ sea homogéneo entre bloques.
  - motivo: Depende de Guerrero (1993), que está en la biblioteca sin texto (Journal of Forecasting 12(1), 37–48): habría que leer en el artículo qué cociente se minimiza y cómo se forman los bloques. Es la misma situación de c2-m8-04 del capítulo 2, que sigue pendiente. FPP3 §3.1 solo dice que el método elige λ.
- **c3-m10-04** · Las redes RNN, LSTM y GRU relajan la ventana fija del AR: un estado oculto acumula el pasado y la red aprende cuánto recordar y olvidar; su coste es un entrenamiento secuencial costoso y muchos datos.
  - motivo: Falta en la biblioteca una obra de aprendizaje profundo que describa las redes recurrentes y las de compuertas (LSTM, GRU) y su coste de entrenamiento. Habría que darla de alta por DOI o ISBN (sin recordar el autor ni el año de memoria), leerla y registrar el pasaje. FPP3 §12.4 solo trata redes de alimentación hacia adelante con una capa oculta, sin recurrencia: no respalda esta fila.
- **c3-m10-05** · Los transformers temporales relajan el decaimiento con la distancia (la atención puede pesar igual el rezago 1 que el 500), a cambio de un coste cuadrático en la longitud y de aún más datos.
  - motivo: Falta en la biblioteca una obra de aprendizaje profundo que describa la atención y los transformers y su coste en la longitud de la secuencia. Habría que darla de alta por DOI o ISBN (sin recordar el autor ni el año de memoria), leerla y registrar el pasaje. Ninguna obra en caché trata esta arquitectura. «Aún más datos» es valoración del capítulo.
- **c3-m10-39** · Lectura: Shumway y Stoffer (4.ª ed.), el tratamiento formal de ARMA, causalidad, invertibilidad y estimación; en la 3.ª edición, secc. 3.2 y 3.6.
  - motivo: La edición que cita el curso (la 4.ª, 2017) no está en la caché; solo se han leído el índice y las secciones 3.2 y 3.6 de la 3.ª (2011), que no es la que cita el curso. Falta leer el índice de la 4.ª para confirmar la numeración y si trata las manchas solares. Hasta entonces la frase dice los temas y la numeración de la 3.ª, y que la de la 4.ª puede ser otra.

| obra que falta | qué desbloquearía | entradas |
|---|---|---|
| **Guerrero (1993)**, *J. of Forecasting* 12(1), 37–48 (en la biblioteca, sin texto) | qué cociente minimiza el criterio y cómo forma los bloques | c3-m9-43 (y c2-m8-04 del cap. 2) |
| **Shumway y Stoffer, 4.ª ed. (2017)**: índice y cap. 3 | la numeración de las secciones de ARMA, causalidad, invertibilidad y estimación, y si las manchas solares están entre sus ejemplos; además pasaría a cita visible lo que hoy respalda la 3.ª solo en el registro (c3-m1-15, c3-m1-34, c3-m2-08 y otras seis citas) | c3-m10-39 |
| **Una obra de aprendizaje profundo** (no hay ninguna en la biblioteca; darla de alta por DOI o ISBN, no de memoria) | las filas RNN/LSTM/GRU y transformers de la tabla del puente del M10: qué relajan y a qué coste | c3-m10-04, c3-m10-05 |

No son `pendiente`, pero **se reescribieron para no depender de una obra sin texto**, y volverían a poder decirse
con ella:

| obra sin texto | qué decía el capítulo y cómo quedó | qué habría que leer |
|---|---|---|
| **Box y Jenkins** (cualquier edición) | «el convenio del Box–Jenkins clásico» (M1) → «el de algunos textos», respaldado con Cryer y Chan p. 57 y `?arima`; «capítulos 3 y 6» y «fuente original» en las lecturas → fuera. La parsimonia y el ciclo identificar–estimar–diagnosticar no se atribuyen a nadie en la prosa (Cryer y Chan p. 8 y Hamilton p. 109 los atribuyen a Box y Jenkins: disponible si se quiere) | el capítulo donde definen el MA (signo) y los de identificación y diagnóstico |
| **Ljung y Box (1978)** | «Ljung y Box (1978) reemplazaron…» se respalda con Cryer y Chan (p. 184) y FPP3 §5.4; la varianza de r̂ₖ que justifica el factor no está en ninguna fuente leída y es `propia` por simulación (c3-m8-11) | la derivación de Var(r̂ₖ) ≈ (T−k)/(T(T+2)) |
| **datos.gov.co** (la TRM) | la procedencia en la prosa es `propia` (c3-m9-49: sale de la copia fija); la ficha del JSON sigue sin obra, como c2-m4-14 | dar de alta el conjunto en «4 Datos y software» |
| **statsmodels, numpy, forecast** (documentación) | todo lo que el capítulo dice de ellos es `propia`, comprobado ejecutando; `auto.arima()` tiene ahora además a Hyndman y Khandakar (2008) | — |

## Lo que no cierra (para la sesión maestra y para Javier)

1. **F07 en las seis citas de Yule (1927)** (c3-m7-02 ×4, c3-m7-03, c3-m9-06): el auditor exige que el año de la
   obra (1927) aparezca en `edicion_comprobada` de `ejemplares.yml`, y la ficha que dejó la sesión maestra no lo
   lleva (la primera página dice «Received December 11, 1926.—Revised February 17, 1927»). No toqué ese archivo:
   basta añadir el año a la ficha (p. ej. «…revisado el 17 de febrero de 1927; Phil. Trans. A 226, 1927»). Las
   citas en sí están en su página (F05 limpio).
2. **Cosas que la lectura de Yule deja falsas o dudosas y que esta ronda no podía tocar** (datos, simuladores, JS):
   - `precalculo/genera_cap3.R:200` y `:566` → el JSON de datos dice «ventana centenaria de Yule (1927)»
     (`MANCHAS.fuente`; no se ve en pantalla). Yule usó 1749–1924.
   - `cap3_js.js:1433`, pie de la tabla de ranking, visible: «El AR(2) de Yule —la fila marcada—». Yule ajustó
     una regresión de orden 2, pero no a esta ventana.
   - `cap3_js.js:1060` y `:1252`, rótulos de dos simuladores: «número de Wolf». Ninguna fuente leída lo dice (Yule: «Wolfer»).
   - `cap3_js.js:1250`: «(ciclo solar ≈ 11)»: ahora tiene fuente (c3-m9-06), se puede dejar.
   - La celda «11 años (un ciclo)» de la tabla de elasticidad y «pasado medio ciclo solar» (M9) usan el
     pseudo-periodo del modelo como si fuera el ciclo; no las exige ninguna fuente y no se tocaron.
3. **La notación de Ljung–Box está al revés que en las fuentes**: FPP3 §5.4 y Cryer y Chan llaman Q al estadístico
   de Box–Pierce y Q* al de Ljung–Box; el capítulo, al contrario (M8, definición y desarrollo). Cambiarla toca
   fórmulas y varias menciones: decisión de Javier. Queda dicho en las notas de c3-m8-08, -09 y -36.
4. **La sección «Fitting methods» de `?arima` no es citable** con el vocabulario de localizadores del auditor
   (`SECCIONES_R`). Ahí está lo de CSS, la verosimilitud exacta y que los MA «se convierten a la forma invertible si
   `transform.pars` es verdadero». Esas afirmaciones quedaron `propia` (ejecutando) o respaldadas con §Arguments o
   §Details. Si se quiere citarlas, hay que añadir «Fitting methods» y «Note» a `SECCIONES_R` (y a
   `prueba_audita_citas.py`): cambio del auditor, fuera de esta ronda.
5. **Tensión interna, no de fuentes (c3-m9-23):** el M9 elige el ruido blanco **sin** media y a la vez dice que «el
   mejor pronóstico… es la media histórica»; el modelo sin media pronostica 0. No se cambió.
6. **El techo cos(π/(q+2)) del MA(q)** (c3-m3-12) es `propia`: ninguna caché lo trae y el capítulo no lo deduce;
   se comprobó numéricamente para q = 1…6 (`r4_software_py.out`). Si se quiere que conste en el capítulo, hace
   falta una línea de derivación o un bloque.
7. **Voz y cuantificadores que quedan fuera de las marcas** (no los exigía una fuente): «será nuestro primer método
   de estimación» (M2), «una de las confusiones más frecuentes» (M2), el comentario de código «retirado en
   statsmodels 0.13» (M7; lo comprobable es que la 0.14.6 lanza `NotImplementedError`).
8. **Citas dentro de celdas de tabla** (seis, en el M10): a 375 px la tabla se desplaza dentro de su contenedor y
   una cita queda fuera de la vista hasta desplazarla (la página no desborda: 375/375 px).
9. **Fuera del capítulo:** `taller-2-modulo-2.html` pregunta por el AR como «antepasado directo» de una red
   recurrente, expresión que el M10 ya no usa.
10. **`propia` discutibles** que el verificador debería mirar con lupa: c3-m10-09 y c3-m10-14 (valoraciones del
    capítulo, ahora condicionales), c3-m10-92 y c3-m10-94 (remisiones internas, leídas en los capítulos 4 y 5).
11. No revisé una a una, contra la caché, las 213 propuestas de los lectores: comprobé mecánicamente cada cita
    (está en su localizador) y leí los 64 cambios de prosa y todo lo de Yule y de Hyndman–Khandakar; el juicio de
    cada veredicto es el del lector y queda para el verificador independiente.

## Lo que va a la R5 (quiz `AUTOEVALUACIONES['cap3']`, no tocado)

- `cap3_js.js:1532–1535` (3.3, invertibilidad): la opción «`arima()` devuelve **siempre** la solución invertible»
  está marcada como correcta, y las dos retros repiten el «siempre». La prosa dice ahora «por defecto».
- `cap3_js.js:1646` (3.7): «Yule–Walker **solo sirve** para modelos AR puros» marcada como correcta; la prosa dice
  ahora «bastante buenas en AR puros, muy ineficiente si hay parte MA».
- `cap3_js.js:1573` (retro del pseudo-periodo): «El ciclo solar documentado por los astrónomos es de unos 11 años»;
  la prosa dice ahora «estimación habitual… algo más de 11 años» (Yule, 1927).
- Los quizzes de 3.1 y 3.2 no repiten ningún error corregido.
- De la R3 siguen: el ejercicio 1 usa `n`, el 3 «periodo», y una retro dice «el modelo no queda identificado».

## Comprobaciones

Tras la última edición. Salidas en `diagnostico/cap3/comprobaciones/`.

| Comprobación | Resultado | Salida |
|---|---|---|
| `python3 precalculo/verifica_todo.py` | **10 de 11 en verde**; falla solo «ninguna cita de memoria», por los F08 y F07 de abajo (Tailwind al día, capítulo 3 reproducible, citas y listas regeneradas, contrato curso → vault al día, cifras del sitio, posición de la correcta) | `r4_verifica_todo.out` |
| `python3 precalculo/audita_citas.py` | **178 hallazgos = 172 F08** (las 172 entradas citables del capítulo 3, sin firma: lo esperado) **+ 6 F07** (ficha del ejemplar de Yule, punto 1 de arriba). F01, F02, F03, F04, F05, F06, F09, F11, F12 y F13 limpios; 586 citas literales comprobadas; A02 sigue en 10 (todas del capítulo 1) | `r4_audita.out` |
| `r4_registro.py`, `migra_citas_fuera.py --comprobar`, `r4_sin_literales.py` | 349 citas comprobadas antes de escribir; «nada por migrar»; 0 literales en archivos que van a git | `r4_registro.out` |
| Verificador de bloques, capítulo 3 | **732 de 732, 0 bloques con discrepancias** (igual que tras la R3); `precalculo/serie.csv` no aparece | `r4_bloques_cap3.out` |
| Cadena | `ensambla_cap3.py`: «reproducible byte a byte»; `ensambla_cap4/5/6.py` corridos en orden: `git diff --stat -- Htmls_Series` muestra solo el capítulo 3; `cap3_js.js` sin diff; `genera_referencias.py --comprobar`: seis capítulos sin cambios | `r4_cadena.out` |
| `r4_marca.py --comprobar` | la fuente de ensamblado es exactamente BASE + cambios + marcas | `r4_marca.out` |
| `r2b_sintaxis.py` | cinco «OK», ninguna declaración repetida | `r4_sintaxis.out` |
| `audita_posicion_correcta.py` | «Ningún instrumento concentra las correctas» | `r4_posicion.out` |
| Software | R 4.6.0 + forecast 9.0.2 y Python con statsmodels 0.14.6: los dos guiones corren con código 0 | `r4_software.out`, `r4_software_py.out` |
| Once módulos por HTTP (servidor propio en el puerto 8747, Chrome sin ventana, 1200 y 375 px) | **22 módulos × ancho: 0 errores de KaTeX, 0 «$» sin componer, 0 fórmulas desbordadas, 0 lienzos sin pintar, 0 citas vacías, 0 enlaces de cita sin destino, 0 citas fuera de una afirmación, 0 signos de puntuación huérfanos, página sin desborde (1200/1200 y 375/375 px)**; lista de fuentes en los módulos 1–10, lista del capítulo (6 obras) en el 10, pie con las 4 básicas; una cita en una celda de tabla del M10 queda fuera de la vista a 375 px (punto 8); un solo evento de consola, el `favicon.ico` 404 de siempre. Servidor detenido al terminar | `r4_recorrido.out`, `.json` |

## Segunda pasada (2026-11-21, tras la verificación independiente)

Dos verificadores leyeron las 213 entradas (`R4_verificacion_A.md`, M1–M6; `R4_verificacion_B.md`, M7–M10) y la
sesión maestra firmó 203. Esta pasada aplica sus hallazgos y el encargo de la maestra, por los mismos guiones
(`r4_reune.py` → `r4_marca.py` → `ensambla_cap3.py --escribir` → `r4_registro.py`). `r4_registro.py` retira ahora
la firma de una entrada si cambian su prosa, su veredicto, sus fuentes o su nota, y lo lista.

| # | punto | lo hecho |
|---:|---|---|
| 1 | c3-m6-07 (error) | «Uno o dos picos que apenas asoman fuera de la banda no bastan como evidencia; uno muy grande, o bastantes más del 5 % de los rezagos fuera, sí» (FPP3 §2.9), como c2-m2-08. Pasa a `respaldada` |
| 2 | c3-m6-08 | «Por eso existe la prueba de Ljung–Box del Módulo 8, que evalúa esos 20 rezagos a la vez» (antes «todos los rezagos»), ahora en oración propia |
| 3 | c3-m1-15 | `con-matiz`; nueva fuente y cita visible, Cryer y Chan, ejercicio 4.15, tras «no hay ninguna»; la nota dice que el ejercicio 4.16 solo pregunta y que la razón («depende del futuro») es de Shumway y Stoffer 3.ª p. 88, solo en el registro |
| 4 | c3-m5-13, c3-m5-20, c3-m3-15, c3-m1-16 | c3-m5-13: Hamilton p. 60 en `fuentes` y a la vista, junto a Cryer y Chan p. 56 (el literal es la frase que sigue a la fórmula, que sale partida en el escaneo). c3-m5-20: segunda cita visible, Hamilton p. 60, tras «errores estándar grandes». c3-m3-15: «el último coeficiente de la proyección lineal (la regresión poblacional)… esa proyección ya contiene». c3-m1-16: `tipo: definicion` |
| 5 | c3-m7-02 | Fuera Cryer y Chan p. 66 (habla de otro artículo de Yule, de 1926) y su nota. Fuentes: Yule p. 281 (resultados de la regresión sobre los números de 1749–1924, ec. 31), p. 280 (la ecuación de regresión sobre los dos anteriores), p. 275 y p. 294. La cita visible de los años pasa de p. 275 a **p. 281**. La nota dice que leer la ec. (31) como un AR(2) es lectura del capítulo. La frase visible no cambia |
| 6 | c3-m7-35 | «CSS es más barato y sirve para arrancar (Hamilton, p. 123); ML cuenta además con las primeras observaciones, cuyo efecto pesa más en series de longitud moderada (Cryer y Chan, p. 158)». Sale «ML es más preciso» |
| 7 | Q / Q* (c3-m8-09, c3-m8-36) | Q(h) sigue siendo Ljung–Box. En el desarrollo plegado el de Box–Pierce es ahora $Q_{BP}(h)$ (la fórmula y la frase de c3-m8-36), y c3-m8-36 añade «(en Cryer y Chan el estadístico de Box–Pierce se escribe Q y el de Ljung–Box, Q*)»; se le añade la fuente p. 183. En c3-m8-09 solo cambia la nota (la fórmula está fuera de su marca) |
| 8 | c3-m9-20 | La cita de Hyndman y Khandakar va tras «ajusta por sí sola varios modelos ARIMA», y la frase dice «…el de menor AICc (el artículo que la presentó usaba el AIC; el AICc es hoy el criterio por defecto del paquete; el Capítulo 4 detalla cómo busca)» |
| 9 | c3-m9-23 | «…es una constante: la media histórica, o cero si, como aquí, la media no se distingue de cero» |
| 10 | c3-m8-24 y resumen del M10 | «Añadir parámetros nunca empeora la verosimilitud» / «Añadir un parámetro nunca empeora la verosimilitud» |
| 11 | Voz | c3-m1-04 «que se verá»; c3-m2-30 «Si se sustituye… queda»; c3-m3-11 «Si un correlograma muestral da… y se quisiera»; c3-m4-31 «por defecto, devuelve»; c3-m5-08 «conviene envolverlo»; c3-m5-18 «Cuando… aparezca… conviene recordar»; c3-m5-20 «Ante un ARMA… conviene probar»; c3-m6-06 «Al mirar… lo esperable es». Ninguna estaba en la introducción de un simulador ni en un enunciado |
| 12 | Comentario del bloque de R del caso 1 (M9) | «anios; la estimacion habitual del periodo es algo mas de 11 (Modulo 9)» (sin tildes, como el resto del bloque). El verificador de bloques cuenta una cifra más: 733 de 733 |
| 13 | `cap3_js.js`, tres cadenas (`r4_marca.py`, tabla `CADENAS_JS`, desde BASE) | Pie de la tabla ordenable: «El AR($2$) —la fila marcada, el que proponía la identificación— no es el mínimo…» (el M8 dice «el AR(2), el modelo que la identificación proponía»); rótulos «Manchas solares (número anual)» y «original (número anual)». El diff del JS son esas tres líneas: quiz, práctica de repaso y simulacro, intactos |
| 14 | Fichas de las lecturas (c3-m10-39, c3-m10-41) | **No se puede con el generador tal como es, y no lo hice.** `genera_referencias.py` solo escribe una ficha en una lista de obras **citadas**, y una `<cite>` exige (F03) una afirmación `respaldada` o `con-matiz` con esa obra en `fuentes`, es decir, leída: `box2016time` y `shumway2017time` no tienen texto, c3-m10-39 es `pendiente` y en c3-m10-41 las fuentes son FPP3 y Cryer y Chan. Haría falta un modo nuevo del generador («ficha de lectura» sin cita) y su regla en el auditor; siguen tecleadas, con «&amp;» |
| 15 | Título de Yule | No lo toqué; las listas llevan ya el título corregido por la maestra |

**Entradas que hay que volver a verificar (20 sin `verificado_por`; 17 citables → 17 F08):**

- *Con la prosa cambiada* (16): c3-m1-04, c3-m2-30, c3-m3-11, c3-m3-15, c3-m4-31, c3-m5-08, c3-m5-18, c3-m5-20
  (además, una cita visible más), c3-m6-06, c3-m6-07 (además, veredicto y nota), c3-m6-08, c3-m7-35 (además, cita
  y nota), c3-m8-24, c3-m8-36 (además, una fuente más y nota), c3-m9-20, c3-m9-23.
- *Sin cambio de prosa, con fuentes, veredicto o nota cambiados* (4, ninguna estaba firmada): c3-m1-15 (veredicto,
  fuente y cita nuevas, nota), c3-m5-13 (fuente y cita nuevas, nota), c3-m7-02 (fuentes, localizador visible y
  nota), c3-m8-09 (solo la nota; la fórmula renombrada queda justo después de su marca).
- **Firmas retiradas por el guion (10):** c3-m1-04, c3-m2-30, c3-m3-11, c3-m3-15, c3-m4-31, c3-m5-08, c3-m5-18,
  c3-m5-20, c3-m6-06, c3-m8-24 (todas por cambio de prosa). No hubo que retirar ninguna firma por un cambio que no
  fuera de prosa.
- *Cambian sin perder la firma* (la huella de la prosa marcada no se mueve): c3-m1-16 (solo `tipo`), c3-m9-06 (el
  comentario de código del punto 12 va unido a ella, fuera de su marca) y el resumen del M10 (punto 10, sin marca).

**Comprobaciones de la segunda pasada** (mismas salidas, reescritas):

| Comprobación | Resultado | Salida |
|---|---|---|
| `r4_registro.py` | 213 entradas, 353 citas literales comprobadas; 193 firmas conservadas, 10 retiradas | `r4_registro.out` |
| `audita_citas.py` | **17 hallazgos, todos F08**, las 17 citables sin firma de la lista de arriba; ningún F07 (la ficha de Yule ya lleva el año); 590 citas literales comprobadas en el curso | `r4_audita.out` |
| Cadena | capítulo 3 reproducible byte a byte; 4–6 sin diff; `cap3_js.js`: tres líneas; `genera_referencias.py --comprobar` y `r4_marca.py --comprobar` en verde | `r4_cadena.out` |
| Bloques del capítulo 3 | **733 de 733**, 0 discrepancias (una cifra más: el comentario del punto 12) | `r4_bloques_cap3.out` |
| `r2b_sintaxis.py`, `audita_posicion_correcta.py`, `r4_sin_literales.py` | en verde; 0 literales en git | `r4_sintaxis.out`, `r4_posicion.out`, `r4_registro.out` |
| Once módulos por HTTP, 1200 y 375 px | 213 citas, 0 vacías, 0 sin destino, 0 errores de KaTeX, 0 lienzos sin pintar, página sin desborde; la misma cita en celda de tabla del M10 fuera de la vista a 375 px; solo el 404 del `favicon.ico`. Servidor detenido | `r4_recorrido.out` |

`verifica_todo.py` no se volvió a correr entero (sus piezas, sí, una por una; falta solo la de Tailwind, y esta
pasada no añade ninguna clase).

De «Lo que no cierra» de la primera pasada quedan resueltos los puntos 1 (F07), 3 (Q/Q*), 5 (c3-m9-23) y, del 2,
el pie de la tabla y los rótulos «Wolf»; del 7, nada (siguen «nuestro primer método» y «una de las confusiones más
frecuentes», fuera de las marcas). Siguen abiertos el 4 («Fitting methods» de `?arima`), el 6 (cos(π/(q+2)) sin
derivación), el 8, el 9 y los pendientes. Para la R5 no cambia nada: las tres cadenas del quiz siguen como estaban.
