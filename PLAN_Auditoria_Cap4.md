---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-04 Modelos ARIMA y Box-Jenkins]]"
fecha: 2026-09-23
estado: ejecutado
---

# Plan — Auditoría módulo por módulo del Capítulo 4

**Objetivo:** corregir los errores factuales, las etiquetas de figuras y simuladores que
no dicen lo que dibujan, y las ecuaciones que faltan, detectados al revisar los diez
módulos y contrastar las cifras contra R 4.6 (forecast 9.0.2, tseries) y statsmodels 0.14.6.

**Alcance:** ortografía, redacción, narrativa, figuras, simuladores, ecuaciones. Nada de
contenido nuevo salvo ecuaciones y frases de transición.

## 1. El hueco

**Estado general.** El capítulo está sano: los 11 simuladores responden a todos sus
controles (mín., medio, máx., cada opción de cada selector) sin errores de consola, sin
valores no finitos y sin errores de KaTeX; la ortografía está limpia y casi todas las
cifras reproducen en R al decimal. Lo que falla son **lecturas** de las cifras —la prosa
dice algo que el propio simulador desmiente— y un bug visible de fechas.

### Gravedad alta (errores que un estudiante puede ver o aprender mal)

| # | Dónde | Qué falla | Verificado |
|---|---|---|---|
| C1 | M10, `trm-abanico` | Eje x con «2015-91»; la historia acaba en «2019-11» cuando es 2026-06. `mesInicial = 1 + 90` y `mesesDesde()` no normaliza un mes > 12 de entrada | node + captura |
| C2 | M4 intro + tabla; quiz P6 | «En $d=1$ solo el rezago 1 se sale de la banda» — también el 8 ($0.231 > 0.197$). El simulador dice «2 de 20» | R |
| C3 | M10 intro + tabla Etapa 1 | «Tras una diferencia, **todas** caen dentro», «máximo 0.088» — $\hat\rho_8=-0.190$ fuera de $\pm0.167$; 0.088 es $\hat\rho_1$ | R |
| C4 | M10 caja abanico | «el intervalo abarca un tercio del nivel» — es el **semiancho** (±33.4 %) | R |
| C5 | M3 tabla vs recuadro | Dos ADF distintos sin decirlo: `adf.test` (tendencia, $k=4$) no rechaza; el de `ndiffs()` (constante, $k=1$) sí. La nota del 0.5 % los mezcla: con la especificación de la tabla el escalón engaña al ADF el 86 % | R |
| C6 | M3 recuadro R vs Python | statsmodels **no** usa `legacy` por defecto: `nlags="auto"` → 5 rezagos, KPSS = 0.8691; «casi el doble» es falso | statsmodels 0.14.6 |
| C7 | M3 `escalon-vs-raiz` | La marca «δ elegido» no se dibuja nunca (dataset de un punto con `pointRadius: 0`); además el eje x es de categorías con malla no uniforme | código + captura |
| C8 | M7 algoritmo | «cuatro modelos iniciales, cada uno con y sin constante» — son cuatro con constante + ARIMA(0,d,0) sin ella; el vecindario también mueve $p$ y $q$ a la vez | R, traza |
| C9 | M6 bloque Python | «statsmodels no descuenta las diferencias» — sí: `nobs_effective` y `aicc` usan $n-d$ | statsmodels |
| C10 | M1 nota del signo | Atribuye el MA con signo menos a Shumway & Stoffer; usan $+$ (como R). Es Box & Jenkins | texto |
| C11 | M10 nota final | «la TRM… entra en el marco [SARIMA]» — la propia tabla da `nsdiffs = 0` | texto |

### Gravedad media

| # | Dónde | Qué falla |
|---|---|---|
| C12 | M5 | $\hat\delta$ (deriva) sin ecuación ni relación con $c$, $\mu_w$; $\delta$ ya es el escalón en M3/M8 |
| C13 | M5 | «No hay forma de pedir deriva» con `stats::arima` — sí, `xreg = seq_along(y)` (−2.8829 vs −2.8827) |
| C14 | M5 | «`auto.arima` prueba con y sin deriva» solo vale con $d=1$; «sin constante, $d=0$ vuelve a la media» — va a cero |
| C15 | M6 tabla ranking | «Ljung–Box p» es a 12 rezagos (explorador y prosa usan 20: (1,1,1) sale 0.41 vs 0.80); «Coeficientes» incluye $\sigma^2$; `mejor` marcado en `d` y `n` |
| C16 | M6 explorador | Rótulo «AICc de todos los modelos» dibuja ΔAICc; «el marcador de la izquierda» no existe; el modelo elegido no se resalta y el mejor (Δ=0) no tiene barra; orden de barras 1,2,0 |
| C17 | M6 | «Error por partida doble»: el (1,2,2) tiene raíz MA 1.03, no 1 |
| C18 | M3 | $\hat\sigma=127.0$ atribuido a «residuales del Nilo» — es del modelo de dos medias (ARIMA: 140.6); «$S_t$ crece como $t$» → $t^{3/2}$; «las tres prueban hipótesis distintas» (ADF y PP comparten $H_0$); 4.8 % vs 4.5 % |
| C19 | M3→M4 | M4 abre con «Fijado $d=1$» cuando M3 lo dejó abierto; falta el puente |
| C20 | M9 nota $d=2$ | «$\Delta^2=0$ a partir de $h\approx3$» (decae como $0.39^h$); «cuatro veces» → 3.55; calla que ese ARIMA(1,2,1) es el sobrediferenciado ($\hat\theta=-1$) del M8 |
| C21 | M9 | «$\psi_\infty=2.99$ … al doble» se contradice con «el cociente tiende a $\psi_\infty$»; la caminata comparada usa la misma $\sigma$ |
| C22 | M9 Python | La diferencia de $\sigma$ no es CSS-ML vs exacta: forecast divide SCR entre $n^*-k$ ($19\,769\cdot99/97$) |
| C23 | M9 `pesos-psi-sigma` | La intro pide mover $h$ y ver cuánto se separan las curvas, pero el gráfico de $\sigma_h$ no marca $h$; etiquetas crudas «σ_h», «ψ_{h-1}» |
| C24 | M9 derivación | «Todo ARIMA admite MA(∞)» (no converge con $d\ge1$); $z_{\alpha/2}$ convive con $z_{0.975}$ |
| C25 | M2 código | La etapa 4 reajusta con CSS-ML y orden a mano; rompe el hilo del esqueleto ($\sigma^2$ 19 769 vs 20 177) |
| C26 | M4 Python | Ljung–Box 0.7323 incluye el residual 0 (= $y_1$ por inicialización difusa); sin él, 0.6984 |
| C27 | M10 | Tabla de etapas se detiene en 3 (el caso ya tiene Etapa 4); resumen sin «el diagnóstico manda» ni el puente; «KPSS confunde… el 100 %» solo vale con el escalón del Nilo; GARCH mal motivado (no hay agrupamiento; hay asimetría y colas) |
| C28 | M10 ejercicio 2 | La pista no dice qué modelo delata la raíz (el (0,1,1) da 1.51); la regla de la varianza no solo «no avisa»: elige $d=2$ |
| C29 | M10 quiz P5 | «escalón en la mitad» — está en la posición 29 (1899); 4.8 % vs 4.5 % en la misma pregunta |
| C30 | M10 lecturas | Shumway & Stoffer: secciones 3.4, 3.6, 3.7 (no 3.8); Box et al.: caps. 4–8 |
| C31 | Voz (todos) | ~30 focos de «tú» / «nosotros» en prosa expositiva (lista por módulo en §7) |
| C32 | Transiciones | M1→M2, M2→M3, M4→M5, M6→M7, M7→M8, M8→M9, M9→M10 acaban en bloque de código sin puente |

### Gravedad baja (figuras)

| # | Qué falla |
|---|---|
| C33 | Ejes Y sin título ni unidades en casi todos los gráficos (10⁸ m³, COP por USD, AICc, % de rechazo) |
| C34 | «∇2 Nilo» en las leyendas de M4 y M8 → «∇²Nilo» |
| C35 | M8: log₁₀ de la varianza en barras desde 0 esconde la diferencia; mejor eje logarítmico con la varianza real |
| C36 | M7: arranca en el paso 1 con el gráfico vacío (ese modelo es ∞); los ∞ no se ven nunca |
| C37 | M4: tabla ACF/PACF con columnas mal repartidas: «ARIMA(p,d,0» y «)» en renglones distintos; la celda del Nilo ocupa 7 renglones |
| C38 | M9 `forma_medida` se calcula sobre el pronóstico ya redondeado: el simulador muestra 0.260/−0.0300 y la tabla 0.25/−0.0409 |
| C39 | «ρ₁» para valores muestrales en las lecturas (el puente ya usa ρ̂) |
| C40 | **Transversal:** las lecturas de los simuladores formatean en es-CO («0,4020», «28.637,95») y los ejes de Chart.js en en-US («1,400»), mientras la prosa usa punto decimal. Tres convenciones en pantalla |

### Fuera del capítulo 4

| # | Qué falla |
|---|---|
| C41 | **Cap. 5, apertura:** dice que el mejor ARIMA no estacional era un (0,1,1) con AICc −238.64 y $\hat\rho_{12}=0.8106$; el puente del cap. 4 dice (0,1,5), −261.45, 0.7245. Y compara AICc con distinta diferenciación, lo que el cap. 4 prohíbe |

## 2. Restricciones verificadas antes de planear

- `ensambla_cap4.py` **reproduce el capítulo byte a byte** hoy (comprobado 2026-09-23).
  Toda edición va en `ensamblado/cap4/` y se regenera; nunca solo en el HTML.
- `mesesDesde()` de `cap4/chapter.js` **no llega al capítulo 5**: el 5 tiene su propia
  copia y normaliza en la llamada. Arreglarlo en el 4 no cambia el 5.
- El reparto de la correcta del quiz (2 3 1 4 3; múltiple [1,2,4]) está vigilado por
  `audita_posicion_correcta.py`: no se toca.
- Cifras nuevas (86 %, 70 %→43 % con $\ell=12$, `forma_medida` sin redondear) deben salir
  de `precalculo/genera_cap4.R`, no escribirse a mano.

## 3. Decisiones de esta ronda

Tomadas con Javier el 2026-09-23:

- **D1. Alcance: todo el plan** (C1–C39 y E1–E14).
- **D2. C40 (formato decimal) queda fuera:** es transversal a los seis capítulos y pide
  una ronda propia. La prosa conserva el punto decimal.
- **D3. C41 sí entra:** se corrige solo el párrafo de apertura del capítulo 5, en
  `ensamblado/cap5/`, y se comprueba que el 5 no cambia en nada más.
- **D4. Notación:** la **deriva es $\delta$** (M5, M9, M10) y el **escalón de 1899 pasa a
  $\beta$** en todo el capítulo (M3, M8, simulador, quiz). En la ecuación ADF los
  coeficientes de los rezagos son $a_j$. Antes, $\hat\delta$ era a la vez $-2.88$ (deriva)
  y $-247.78$ (escalón).
- **D5. Voz:** impersonal en la prosa; «tú» solo en intros de simuladores y enunciados
  de ejercicios. Los textos del componente `.ciclo` quedan fuera (convención).
- **D6. Cifras nuevas en `genera_cap4.R`,** no a mano: `adf_test_no_rechaza` en el Monte
  Carlo (86.4 % con escalón, 5.4 % sin él), `kpss_rechaza_l12` en la malla (44.5 % en
  $\beta=100$ frente a 70.8 % con $\ell=4$), y `forma_medida` sobre el pronóstico sin
  redondear. Añadir las pruebas no consume números aleatorios: el resto de cifras del
  JSON sale idéntico (comprobado campo a campo).

## 4. Ecuaciones que conviene añadir (criterio: solo donde la prosa describe en palabras un objeto que el estudiante tiene que manipular)

| # | Dónde | LaTeX |
|---|---|---|
| E1 | M1, definición | $\nabla \equiv 1-B,\quad w_t=\nabla^d y_t=(1-B)^d y_t$ |
| E2 | M1, fila IMA(1,1) | $\hat y_{t+1\mid t}=\alpha\,y_t+(1-\alpha)\,\hat y_{t\mid t-1},\quad \alpha=1+\theta$ |
| E3 | M3, junto a la tabla de evidencias | ADF $\nabla y_t=\alpha+\beta t+\gamma y_{t-1}+\sum_{j=1}^{k}\delta_j\nabla y_{t-j}+\varepsilon_t,\ H_0:\gamma=0$; KPSS $y_t=\mu+r_t+u_t,\ r_t=r_{t-1}+v_t,\ H_0:\sigma_v^2=0$ |
| E4 | M3, derivación KPSS paso 4 | $\max_t S_t\approx\tau(1-\tau)\,n\,\delta$ con $\tau=0.28$ |
| E5 | M3, recuadro R vs Python | $\hat\sigma^2_{LP}=\hat\gamma_0+2\sum_{j=1}^{\ell}\bigl(1-\tfrac{j}{\ell+1}\bigr)\hat\gamma_j$ |
| E6 | M4, tras la tabla | $(1-B)\,y_t=(1-0.733\,B)\,\varepsilon_t$ |
| E7 | M5, antes de «¿La lleva el Nilo?» | $\phi(B)(1-B)(y_t-\mu_w t)=\theta(B)\varepsilon_t\ \Rightarrow\ \operatorname{E}[\nabla y_t]=\mu_w=c/\phi(1)$ |
| E8 | M6, criterios | AIC / AICc / BIC en `aligned` (hoy en una línea que desborda en móvil) |
| E9 | M8, firma de la sobrediferenciación | $\nabla^2 y_t=(1-B)\,w_t=\varepsilon_t-\varepsilon_{t-1}$ si $w_t=\nabla y_t$ es ruido ($\theta=-1$) |
| E10 | M8, caso del Nilo | $y_t=\mu+\beta\,\mathbb 1\{t\ge1899\}+\varepsilon_t$ |
| E11 | M9, pesos ψ | $\psi(B)\,\phi(B)(1-B)^d=\theta(B)$ y, para el ARIMA(1,1,1), $\psi_j\to(1+\theta)/(1-\phi)$ |
| E12 | M10, caminata | $\hat y_{T+h\mid T}=y_T,\quad \operatorname{Var}(y_{T+h}-\hat y_{T+h\mid T})=h\sigma^2$ |
| E13 | M10, cancelación del (2,1,2) | $(1-0.661B+0.992B^2)\nabla y_t=(1-0.623B+1.000B^2)\varepsilon_t$ |
| E14 | M10, puente | $(1-B)(1-B^{12})\log y_t=(1+\theta B)(1+\Theta B^{12})\varepsilon_t$ |

## 5. Tareas

| T | Qué | Archivos | Depende de |
|---|---|---|---|
| T1 | Bug de fechas (C1) y marca «δ elegido» + eje lineal (C7) | `cap4/chapter.js` | — |
| T2 | Errores factuales de prosa (C2–C6, C8–C11, C13–C14, C17–C18, C20–C22, C24) | `cap4/templates_*.html`, `chapter.js` (quiz) | D |
| T3 | Etiquetas de simuladores y tabla ranking (C15–C16, C23, C33–C36, C39) | `cap4/chapter.js` | — |
| T4 | Ecuaciones E1–E14 | `cap4/templates_*.html` | — |
| T5 | Voz y transiciones (C31–C32) | `cap4/templates_*.html` | — |
| T6 | Cifras nuevas en R (C5, C38, 43 %) | `precalculo/genera_cap4.R` → `cap4_datos.js` | — |
| T7 | Reensamblar 4 → 5 → 6 y comprobar que 5 y 6 no cambian | scripts | T1–T6 |
| T8 | Verificar en navegador por HTTP, módulo a módulo | — | T7 |

## 6. Criterios de aceptación

- `ensambla_cap4.py` regenera el capítulo y `ensambla_cap5.py`/`cap6` reproducen sus archivos byte a byte.
- Ninguna afirmación de la prosa contradice la lectura de su simulador (rezagos fuera de banda).
- El abanico de la TRM rotula 2022-07 … 2026-06 y el pronóstico hasta 2029-06 como máximo.
- Cero errores de consola y de KaTeX en los 10 módulos; los 11 simuladores responden.
- `audita_posicion_correcta.py` en verde.

## 7. Riesgos

- `ensambla_cap5.py` parte del 4: cualquier cambio en la región compartida (CSS, motor)
  se arrastraría al 5. Esta ronda solo toca regiones propias del 4 (plantillas y `chapter.js`).
- C40 (formato decimal) es transversal a los seis capítulos: no se toca sin decisión explícita.

## 8. Resultado (2026-09-23)

Aplicado C1–C39, C41 y E1–E14 (E7 de M10, la banda del puente, se descartó por sobrar).
Hecho por cinco manos en paralelo: un agente por plantilla (`templates_1_3`, `4_6`, `7_9`,
`10` + apertura del cap. 5) y `chapter.js` y `genera_cap4.R` en la sesión principal.

**Verificado:**

- `genera_cap4.R` regenera el JSON con **todas las cifras previas idénticas**, campo a
  campo; solo cambian `generado`, los campos nuevos de D6 y unas tildes que el JSON
  anterior llevaba mal codificadas (`Escal<c3><b3>n`).
- Reensamblado 3 → 4 → 5 → 6: el 3 reproducible byte a byte, el 5 cambia solo en su
  párrafo de apertura, el 6 idéntico.
- Chrome sin ventana a 1440 px y a 375 px, los 10 módulos con las derivaciones abiertas:
  cero excepciones, cero `.katex-error`, cero LaTeX sin renderizar; los 11 simuladores
  responden en mínimo, medio, máximo y cada opción.
- Abanico de la TRM: la historia termina en 2026-06 y el pronóstico llega a 2028-06.
- `audita_posicion_correcta.py` y `audita_alineacion_modulos.py` en verde.

**No aplicado, a propósito:**

- Paneles del `.ciclo` del M2 (concordancia «la decide» → «la deciden», voz, a11y): fuera
  de alcance por convención; es texto de componente.
- Comentarios de código sin tildes: convención ASCII del capítulo.
- M9: la diferencia del 14 % entre `forecast()` y la fórmula ψ en el ARIMA(1,2,1) no
  invertible (2771 frente a 2428) no se escribió: no está en el JSON.

**Pendiente, fuera de esta ronda:**

- **Teléfono (375 px).** Desbordaban 17 fórmulas en bloque; quedan 9, todas anteriores a
  esta ronda (M1 ×3, M3 ×3, M7, M9 ×2), y la página tiene scroll horizontal en M4–M7, M9 y
  M10 (568, 500, 412, 388, 391 y 503 px). Es la misma ronda que se hizo al capítulo 3 en
  `8ceb706`: la copia MathML de KaTeX y las tablas.
- **C40**, formato decimal de lecturas y ejes (los seis capítulos).
- ~~Cap. 5, tabla de la TRM: banda $\pm0.168$ → $\pm0.167$ ($1.96/\sqrt{137}$)~~: hecho el
  2026-09-23, commit `6696a91`.

### Añadido el 2026-09-24: la introducción del simulador del Nilo (M1)

La auditoría dejó intacta la intro de `nilo-y-diferencia`, y era la lectura que el simulador
necesitaba. Pedía mirar dos cosas del gráfico —«el nivel deja de vagar» y que la diferencia
oscila más rápido— y no las cifras del panel, que son el porqué del simulador:

| $d$ | $n$ | media | varianza | $\hat\rho_1$ |
|---|---|---|---|---|
| 0 | 100 | 919.35 | 28 638 | $+0.50$ |
| 1 | 99 | $-3.84$ | 28 268 | $-0.40$ |
| 2 | 98 | $-0.14$ | 80 055 | $-0.63$ |

La nueva hace leer la media (casi cero: la serie pasa a ser su cambio anual), la varianza
(apenas baja con $d = 1$, casi se triplica con $d = 2$) y el signo de $\hat\rho_1$ (con $d = 2$,
por debajo del $-0.5$ de la diferencia de un ruido blanco), y cierra preguntando si hacía falta
diferenciar: el hilo que retoman la nota de la anomalía, el M3 y el M8. «Vagar» se sustituye
por el descenso hacia 1899, que es lo que se ve y lo que el M3 convierte en escalón.

Editada en `ensamblado/cap4/templates_1_3.html` y en el HTML; `ensambla_cap4.py` la reproduce
byte a byte y los capítulos 5 y 6 reensamblados salen idénticos. Cero `.katex-error`. Commit
`76af7c6`.

### Añadido el 2026-09-24: dos frases del ciclo de Box–Jenkins (M2)

Fuera del alcance de la ronda por ser texto de componente, pero con dos errores de contenido:

- **La línea de retorno** decía «Las tres primeras etapas forman un bucle», y el panel de Uso
  del mismo ciclo manda de vuelta a elegir $d$ (y remite al capítulo 6, que «puede mandarte de
  vuelta al principio»). Ahora: las etapas 2, 3 y 4 pueden devolver a la identificación; solo se
  llega a pronosticar cuando el diagnóstico no objeta nada, y aun entonces la forma del
  pronóstico puede delatar un $d$ mal elegido.
- **«Qué te devuelve atrás» de Estimación** metía una raíz sobre el círculo unitario con la
  sobreparametrización y les daba un solo arreglo, «un orden más pequeño». Ahora se separan: no
  converger o un error estándar enorme → $p$ o $q$ más pequeños; una raíz unitaria **o muy
  cerca** depende de cuál sea: la del MA pide **bajar** $d$ (sobrediferenciación), la del AR,
  **subirlo**. El «muy cerca» cubre el Nilo, cuya raíz MA está en $B = 1.144$.

El resto del `.ciclo` del M2 (voz de «Qué haces», a11y) sigue pendiente. Verificado igual que
la intro del Nilo: 4 reproducible, 5 y 6 idénticos, cero `.katex-error` con la pestaña de
Estimación abierta. Commit `e3b63ed`.

### Añadido el 2026-09-24: el simulador del escalón (M3) y su leyenda en el teléfono

Tres huecos de `escalon-vs-raiz` y uno de disposición:

- **La introducción** no decía qué mirar. Ahora: con $|\beta| = 0$ KPSS rechaza cerca del
  $5\,\%$ (la prueba funciona); buscar dónde cruza la curva el $50\,\%$ (hacia $|\beta| \approx 80$,
  $0.6$ desviaciones típicas); la línea vertical es el Nilo; la segunda curva es $\ell = 12$
  (`nlags="legacy"`), que rechaza menos pero también se engaña, y remite al recuadro de R frente
  a Python, donde se explica $\ell$ y que antes quedaba unas 180 líneas más abajo sin aviso.
- **El Nilo no estaba en el gráfico.** Línea vertical punteada en `malla.delta_del_nilo`
  ($247.78$), con entrada «Nilo (247.8)» en la leyenda y **fuera del tooltip**: con la
  interacción por índice, sus dos puntos salían como «Nilo: 100» al pasar sobre $|\beta| = 25$.
- **El signo de $\beta$.** El deslizador (0 a 300) leía «descenso de $\beta$» y la prosa usaba
  $\beta = -247.8$. Control, eje y lectura dicen ahora «descenso $|\beta|$»; la prosa pasa a
  $|\beta|$ donde $\beta$ es un tamaño (100, 200, 300 en la nota, la derivación y el recuadro de
  R frente a Python) y conserva $\beta = -247.8$, que es el valor del parámetro.
- **La leyenda en el teléfono**, anterior a esta ronda: a $375$ px el lienzo mide $236$ px y
  las cinco entradas ocupaban cuatro filas, con $40$ px útiles para las curvas y la última fila
  rozando el «100 %». Por debajo de $420$ px de lienzo la leyenda se compacta (letra $10$, caja
  $12$, separación $6$) y el marco de la tasa pasa de $200$ a $280$ px, con `onResize`: $151$ px
  útiles a $375$, $125$ a $320$, tres y cuatro filas sin solape; el escritorio queda igual. Va en
  el JavaScript del simulador y no en CSS porque el `<style>` del capítulo se hereda del 3. La
  leyenda de la realización, que se cortaba, se acorta a «Descenso de $|\beta|$ en 1899» («Sin
  escalón» en cero): el rótulo de encima ya dice «ruido blanco + escalón».

Verificado: las dos fuentes (`templates_1_3.html`, `chapter.js`) reensamblan el 4 con solo sus
líneas cambiadas, 5 y 6 idénticos; Chrome sin ventana a 1280, 768, 375 y 320 px sin excepciones;
el barrido de los 10 módulos, cero `.katex-error` y solo los falsos positivos conocidos del
detector de decimales. Commit `a54eb2e`.

### Añadido el 2026-09-24: el simulador de identificación (M4)

`identificacion-nilo` enseñaba bien que $p$ y $q$ se leen sobre la serie ya diferenciada, pero
no el resto. Cifras comprobadas en R:

| $d$ | ACF fuera de banda | PACF fuera de banda | $\hat\rho_1$ | varianza |
|---|---|---|---|---|
| 0 | 11 de 20 | 1 de 20 | $+0.498$ | 28 638 |
| 1 | 2 de 20 (1 y 8) | 4 de 20 | $-0.402$ | 28 268 |
| 2 | 2 de 20 (1 y 8) | 7 de 20 | $-0.626$ | 80 055 |

Al diferenciar ruido blanco con $n = 99$, $\hat\rho_1$ cae entre $-0.60$ y $-0.36$ el $90\,\%$ de
las veces, y el $-0.402$ del Nilo está dentro: el pico negativo de $d = 1$ es también el que deja
diferenciar sin necesidad. Simulando el escalón del M8 (ruido de $\sigma = 127.7$ y $\beta =
-247.8$), el $14\,\%$ de las réplicas da un $\hat\rho_1 \ge -0.402$; el $\hat\theta = -0.733$ del
ARIMA($0,1,1$) queda en su cola ($5\,\%$, mediana $-0.82$), así que no lo zanja.

- **La etiqueta del selector**, «d = 1 — ∇Nilo (la correcta)», contradecía el primer párrafo
  del módulo («decisión de trabajo»). Pasa a «(la de trabajo)».
- **La introducción** no mencionaba la PACF, que es donde está la trampa de $d = 0$ (un solo
  pico, como un AR(1) con $\phi \approx 0.5$, que la ACF desmiente: ese AR(1) daría $0.25$ y
  $0.12$ en los rezagos 2 y 3, no $0.385$ y $0.328$). Atribuía la sobrediferenciación al signo
  de $\rho_1$, sin gorro, cuando el signo ya cambia en $d = 1$; y decía que el rezago 8 «roza» la
  banda, cuando se sale. La nueva, en *tú*: leer las dos funciones; la ACF de $d = 0$ como huella
  de un nivel que se mueve, «por una raíz unitaria o por un cambio de nivel como el de 1899»; la
  trampa de la PACF; el MA(1) de $d = 1$ y el rezago 8 como el uno de cada veinte esperable; en
  $d = 2$, $\hat\rho_1$ por debajo de $-0.5$, como en la intro del M1; y el cierre, «La tabla elige
  $p$ y $q$; no confirma $d$».
- **El panel** contaba solo la ACF fuera de banda, que da 2 de 20 en $d = 1$ y en $d = 2$.
  Añade «PACF fuera de banda»: 1, 4 y 7 de 20.
- **Los gráficos en el teléfono**: a $375$ px la leyenda de la ACF y de la PACF ocupaba dos filas
  y dejaba $56$ px a las barras sobre una escala de $-1$ a $1$; el cruce del rezago 8 no se
  apreciaba. Usan la compactación del M3, que sale del cierre de `escalon-vs-raiz` a los
  ayudantes del capítulo, con el marco de $180$ a $240$ px: $144$ px útiles a $375$ (una fila),
  $128$ a $320$, $141$ a $768$; el escritorio sigue en $75$. `crearGraficoBarras` no admite
  `onResize` y se le añade ya creado.

Verificado: `chapter.js` y `templates_4_6.html` reensamblan el 4 con solo sus líneas cambiadas, 5
y 6 idénticos; el M3 mide lo mismo que tras `a54eb2e` ($151$ y $125$ px); Chrome sin ventana a
cuatro anchos sin excepciones; cero `.katex-error` en los 10 módulos. Commit `6c35e68`.

Queda fuera: la tabla del M7 rotula $d = 1$ «Mínimo de varianza. Correcto.», el mismo exceso que
tenía el selector.

### Añadido el 2026-09-24: tres conexiones del M5 (media y deriva)

El M5 no tiene simulador; lo interactivo son las pestañas R/Python. Lo que tiene es correcto,
comprobado otra vez: en R, $\hat\delta = -2.8827$ (e.e. $2.0167$, $t = -1.429$) con $\hat\phi_1 =
0.2707$, de donde $c = -2.10$; AICc $1268.063$ frente a $1267.507$; la TRM, $8.001$ con e.e.
$10.356$ ($t = 0.773$); `arima()` con $d = 1$ devuelve solo `ar1` y `ma1` pese a
`include.mean = TRUE`, y `Arima()` con $d = 2$ da el aviso citado. En Python (statsmodels
0.14.6), `trend="n"` por defecto con $d > 0$, `ValueError` con `trend="t"` y $d = 2$, y la deriva
$-2.8518$ (e.e. $2.124$) del comentario. Faltaban tres conexiones, añadidas en prosa impersonal:

- **La regla del polinomio** remite al simulador «La forma del pronóstico según $d$» del M9, que
  dibuja cuatro de sus seis casos sobre el Nilo (con media, sin constante, con deriva y $d = 2$).
  Ninguno de los dos módulos citaba al otro.
- **«¿Lleva deriva el Nilo?»**: la media de las diferencias es $(740 - 1120)/99 = -3.84$ —suma
  telescópica, solo quedan los extremos— y el descenso de $247.8$ de 1899 aporta $-2.50$; con
  $d = 1$ un cambio de nivel único solo entra como choque o repartido en pendiente, y el M8 lo
  ajusta como escalón. Se habla de la media de $\nabla y_t$ y no de $\hat\delta$, que se estima con
  errores ARMA y no se descompone exactamente así.
- **La nota de la TRM**: en el ARIMA($0,1,0$), $\hat\delta = (y_n - y_1)/(n-1) = 8.001$, que
  depende solo del primer y del último mes; lo de en medio solo entra en el error estándar (no
  «no aporta nada»: fija la varianza de las diferencias).

Verificado: el 4 reensamblado con solo las líneas de `templates_4_6.html`, 5 y 6 idénticos; en
Chrome sin ventana a 1280, 375 y 320 px, las 24 fórmulas de los tres párrafos renderizan, ningún
`$` crudo, ninguna más ancha que la vista (la larga se parte en el «=» a $375$); cero
`.katex-error` en los 10 módulos. Commit `d2de1cf`.

## 9. Enlaces

- Precedente: [[PLAN_Auditoria_Cap3]]
- Caso TRM hasta el pronóstico: [[PLAN_Casos_Aplicados_456]]
- Sesión de la intro del Nilo: [[2026-09-24]]
