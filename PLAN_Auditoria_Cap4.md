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
- Cap. 5, tabla de la TRM: banda $\pm0.168$ → $\pm0.167$ ($1.96/\sqrt{137}$).

## 9. Enlaces

- Precedente: [[PLAN_Auditoria_Cap3]]
- Caso TRM hasta el pronóstico: [[PLAN_Casos_Aplicados_456]]
