# Capítulo 3 · revisión del par académico

- **Archivo:** `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html` en el commit `58bdfc5` (once `<template id="module-N">`, l. 2677–6320; motor y simuladores l. 6345–9800; `AUTOEVALUACIONES['cap3']` l. 9125, `['parcial2']` l. 9354, `SIMULACROS['cap3-simulacro']` l. 9818). Las líneas citadas abajo son de ese archivo; la fuente editable está en `ensamblado/cap3/`.
- **Lente:** corrección y rigor (definiciones, fórmulas, lógica del JS, código R y Python, cifras, ejercicios y claves, interpretaciones). No reviso estilo, fuentes ni diseño de gráficas.
- **Entorno:** R 4.6.0 · forecast 9.0.2 · tseries 0.10.62 · jsonlite 2.0.0 | Python 3.10.14 · statsmodels 0.14.6 · numpy 2.2.6 · scipy 1.15.3 · pandas 2.3.3 · matplotlib 3.10.8 (`MPLBACKEND=Agg`). Los bloques de la TRM se ejecutaron contra la API de datos.gov.co (respondió) y se contrastaron con `precalculo/trm_mensual_2015-01_2026-06.csv`.
- **Guiones** (en `diagnostico/cap3/diag/`):
  - `par_extrae_bloques.py` extrae los 25 bloques de código (14 de R, 11 de Python) del HTML en `58bdfc5` a `par_bloques/bNN_lLLLL.{R,py}`. Cada bloque se ejecutó tal cual y su salida está en `par_bloques/bNN_lLLLL.out`.
  - `par_compara_bloques.py` → `par_compara_bloques.out` cruza cada cifra de los comentarios `#>` (R) y `# …` (Python) con la salida real.
  - `par_verifica.R` → `par_verifica.out`: recálculo independiente de las cifras de la prosa que no salen de un bloque.
  - `par_verifica2.R` → `par_verifica2.out`: comprobaciones complementarias (M6, M7, M9 y ejercicio 3).
  - `par_verifica_trm.R` → `par_verifica_trm.out`: el caso de la TRM con el `auto.arima` por defecto y con el del precálculo.
  - `par_verifica.py` → `par_verifica_py.out`: AutoReg frente al CSS, residuales de statsmodels y Ljung–Box recortado.
- **Convención de signos:** el capítulo usa en todas partes el convenio de suma de R ($\theta(B)=1+\theta_1B+\dots$). Lo cumplen la prosa, las recursiones $\psi$/$\pi$, el JS (`pesosPsi`, `pesosPi`, `esInvertible`), el quiz, la actividad del Parcial 2 y el simulacro: en el ítem 9, $(1-0.12B)$ se lee bien como $\theta=-0.12$. No encontré ninguna mezcla. La afirmación sobre S-PLUS (l. 2747, 2778–2780) coincide con `?arima` de R 4.6.0.

**Resultado global.** Los 25 bloques corren y reproducen sus cifras, con tres excepciones menores de redondeo o formato (§ Menores). La gran mayoría de las cifras de la prosa salen del recálculo. Los problemas están en **interpretaciones y en dos cálculos mal planteados**, no en la aritmética de las tablas.

---

## Módulo 3.1 · Operador de rezago (l. 2677–2944)

- **Correcto:** la definición de $B$, el desarrollo $(1-B^m)(1-B)$, los polinomios y la equivalencia $|\phi|<1 \Leftrightarrow |1/\phi|>1$. Los dos bloques reproducen todo: `arima` da 0.5999/0.6925, s.e. 0.0364/0.0355, σ² 0.9992, logL −852.03 y AIC 1710.05, y la ACF de `bien`/`mal` vale 0.7923… y 0.0892…. Las raíces $0.9333\pm0.6799i$ tienen módulo 1.1547. Está bien el aviso sobre `polyroot` frente a `np.roots`.
- **l. 2868 · imprecisión (causalidad).** Dice: «Si $|\phi|\ge1$ … no existe una solución estacionaria». Con $|\phi|>1$ sí existe una solución estacionaria, la **no causal** $y_t=-\sum_{j\ge1}\phi^{-j}\varepsilon_{t+j}$. Lo que no existe es una estacionaria que dependa solo del pasado. Lo mismo afecta al «si y solo si» del triángulo (l. 3031) y a «la región de estacionariedad … es exactamente el conjunto de parámetros con los que el proceso tiene varianza finita» (l. 3118–3123). Fuera del triángulo, sin raíces sobre el círculo, también hay una solución de varianza finita, aunque no causal. Es la simplificación habitual en cursos introductorios, pero el propio capítulo la resuelve bien en otro sitio: el ítem 1 de la actividad del Parcial 2 (l. 9358) añade «$y_t$ depende solo de los choques hasta $t$». Basta con decir «estacionario (causal)» una vez, en el recuadro de l. 2833–2836.
- **l. 2885–2887 · imprecisión.** Dice «$|B|=1$, es decir $\phi=1$, … es la caminata aleatoria». En el AR(1), $|B|=1$ equivale a $|\phi|=1$, y con $\phi=-1$ el proceso no es una caminata aleatoria (`par_verifica.out`: `Mod(polyroot(c(1,1)))` = 1).
- **l. 2797–2798 · menor.** El comentario muestra `print(fit.polynomial_ar)  # [ 1. -0.5999]`, pero lo que se imprime es `[ 1. -0.59985818]`.

## Módulo 3.2 · Procesos AR (l. 2945–3267)

- **Correcto:** la definición, $\mu=c/(1-\sum\phi)$ y que el `intercept` de `arima()` es $\hat\mu$; $\phi_{kk}=0$ para $k>p$; las cuatro firmas (en el AR(2) complejo, la ACF 0.800, 0.370, −0.082, −0.392); el triángulo; la parábola $\phi_1^2+4\phi_2<0$ y el pseudo-periodo $2\pi/\arccos(\phi_1/2\sqrt{-\phi_2})$, que es el periodo de la ACF amortiguada. Con (1.40, −0.69), el valor inicial del simulador, sale 11.05 («unos 11»). También son correctas la recursión de momentos, $\gamma_0$ del AR(2) y su factorización en los tres lados del triángulo, la derivación de Yule–Walker y el ejemplo (0.5, 0.3) con 0.714, 0.657 y 2.2436 σ². Los bloques R y Python reproducen todas las cifras.
- **JS `triangulo-ar2` (l. 8329–8438):** `analizarAR` calcula bien el módulo mínimo (raíces reales: $(-\phi_1\mp r)/2\phi_2$; complejas: $1/\sqrt{-\phi_2}$, estacionario si $\phi_2>-1$). El periodo coincide con la fórmula de la prosa y el triángulo dibujado tiene los vértices correctos.
- La imprecisión del «si y solo si» y de la «varianza finita» está en 3.1.

## Módulo 3.3 · Procesos MA (l. 3268–3571)

- **Correcto:** $\gamma_0$ y $\rho_k$ del MA($q$) con $\theta_0=1$, y el corte exacto. La identificación $(\theta,\sigma^2)\sim(1/\theta,\theta^2\sigma^2)$ está bien demostrada (ρ₁(0.5)=ρ₁(2)=0.4). También la cota $|\rho_1|\le\frac12$ y su derivada, y el triángulo de invertibilidad del MA(2), bien deducido del AR(2) cambiando signos. Con θ=(1.5, 0.6) el módulo es 1.291, y con (0.5, −0.6) los módulos son 0.940 y 1.773. El techo $\cos(\pi/(q+2))$ da 0.5, 0.707 y 0.809, y lo comprobé optimizando numéricamente (`par_verifica.out`). La PACF del MA(1) con θ=0.8 vale 0.4878, −0.3123, 0.2215, −0.1652 y su signo se describe bien. En R, `arima` devuelve θ=0.4794 con σ²=4.08; en Python, 0.5051 con 3.8888.
- **JS `rho1-theta-ma1` (l. 8482–8607):** el «mismo proceso: θ con σ², o 1/θ con θ²σ²» es correcto, y también el tratamiento de la frontera |θ|=1.
- Sin errores.

## Módulo 3.4 · Dualidad AR↔MA (l. 3572–3875)

- **Correcto:** $\psi(B)=\theta/\phi$ y $\pi(B)=\phi/\theta$; las recursiones $\psi_j=\theta_j+\sum\phi_i\psi_{j-i}$ y $\pi_j=-\phi_j-\sum\theta_i\pi_{j-i}$ (comprobadas contra el producto de polinomios); $\hat y_{t|t-1}=-\sum\pi_jy_{t-j}$; la tabla de pesos (1.2, 0.84, 0.588; −1.2, 0.6, −0.3) y las formas cerradas $(\phi+\theta)\phi^{j-1}$ y $-(\phi+\theta)(-\theta)^{j-1}$; $\operatorname{Var}(e_{T+h})=\sigma^2\sum_{j<h}\psi_j^2$; el límite $\gamma_0/\sigma^2$ y el paseo aleatorio $\sigma^2h$. En la parsimonia, $|\pi_7|=0.0188$ y $|\pi_8|=0.0094$, así que hacen falta siete coeficientes. El truco `ARMAtoMA(ar=-0.5, ma=-0.7)` para los $\pi$ es correcto. Los dos bloques reproducen sus cifras.
- **JS (`pesosPsi`, `pesosPi`, `acfTeorica`, l. 8141–8182):** implementan exactamente las recursiones de la prosa. Con 600 términos, la ACF de los ocho procesos difiere de `ARMAacf` en 7.2e−16 como máximo. En el peor caso que permiten los deslizadores del laboratorio ($\phi_1+\phi_2=0.95$), la diferencia es 2.3e−15.
- **l. 3701–3704 (y el comentario JS l. 8133–8138) · menor.** La prosa atribuye el «error máximo $6.7\times10^{-16}$» a la truncación en 600 términos del navegador. La cifra del JSON viene de otra cuenta, hecha en R con **2000** términos (`verificacion.metodo`). Con 600 sale 7.2e−16: la conclusión no cambia, pero la cifra no corresponde a lo que se describe.

## Módulo 3.5 · ARMA e identificación (l. 3876–4419)

- **Correcto:** la definición, la tabla de identificación y el ciclo de cuatro pasos (`bartlett_confint=False` → ±1.96/√n; `pacf()$acf` es 3-D; `fitdf=p+q`). $\gamma_0$ y $\gamma_1$ del ARMA(1,1) valen 3.8235 y 3.1765, con $\rho_1=0.8308$, y $\rho_k=\phi^{k-1}\rho_1$. Las bandas de T=60 y T=1000 son 0.253 y 0.062. La redundancia φ=−θ da ruido blanco, y con −0.45 la ACF vale 0.0515…. Con `set.seed(11)`, el ajuste da 0.8300/−0.7953 (s.e. 0.2307/0.2477) y AICc 554.35 / 552.99 / 550.94. En Python, −0.0798/0.1254 con s.e. ≈1.53. Todo se reproduce.
- **JS `laboratorio-arma` (l. 8677–8767):** simula con 200 periodos de calentamiento, calcula la ACF muestral con divisor n y la PACF con Durbin–Levinson, y pone la ACF teórica a cero si el proceso no es estacionario. Coincide con la prosa.
- **l. 4173–4176, R l. 4221–4225, Python l. 4267–4269 · ERROR (cifra y procedimiento).** Dice: «aplicada a $\rho_1$ [la recursión] daría $0.8$ cuando el valor verdadero es $0.8614$». El código calcula `0.5*r[1] + 0.3*r[1]`, es decir $\phi_1\rho_0+\phi_2\rho_0$. Pero en $k=1$ la recursión es $\rho_1=\phi_1\rho_0+\phi_2\rho_{-1}$, y $\rho_{-1}=\rho_1$, como el propio capítulo establece en l. 3083. Bien aplicada da $0.5+0.3(0.8614)=0.7584$, o $0.5/0.7=0.7143$ si se resuelve como un AR puro (`par_verifica.out`). La conclusión se sostiene (la recursión falla en $k\le q$), pero el número y la línea de código enseñan exactamente el error que el ítem 10 de la actividad del Parcial 2 (l. 9628–9640) marca como incorrecto: «se tomó $\rho_{-1}=1$; pero $\rho_{-1}=\rho_1$». Hay que corregir tres sitios: la prosa, el bloque R y el bloque Python.

## Módulo 3.6 · Simular y reconocer (l. 4420–4539)

- **Correcto:** las realizaciones del panel (`DATOS_CAP3.realizaciones`) salen de `set.seed(3)` en el mismo orden que el bloque R (ACF 0.8139, 0.4706 y 0.8161; `par_verifica2.out`). «Alguno se asoma» es cierto: en el MA(1), los rezagos 6 y 15 caen fuera de ±0.1386. También son correctos la regla del 5 %, el `burnin` por defecto (0) de `generate_sample` y el mensaje de error de `arima.sim(ar=1)`.
- **l. 4501–4502 · imprecisión (dudosa).** Dice: «olvidarlo [el `burnin`] mete una tendencia espuria al principio». `generate_sample` arranca desde valores iniciales nulos, que coinciden con la media de un `ArmaProcess`, que no tiene constante. Lo que produce es un tramo inicial con **varianza reducida** ($\sigma^2(1-\phi^{2t})/(1-\phi^2)$), no una tendencia. Una deriva visible solo aparecería si se arrancara lejos de la media.

## Módulo 3.7 · Estimación (l. 4540–4819)

- **Correcto:** con YW, 1.3173/−0.6338 y σ² 298.96; con CSS, 1.4032/−0.7099 y 229.03; con ML, 1.4059/−0.7111 (s.e. 0.0706/0.0702), 229.43, logL −414.94 y AIC 837.88. La distancia en errores estándar es −1.26/1.10; las raíces tienen módulo 1.1859 y los periodos son 10.53, 10.71 y 10.74. En Python, `yule_walker(method="mle")` reproduce `ar()`, `statespace` coincide con `innovations_mle` y el periodo sale 10.7365. La derivación de CSS como verosimilitud condicional, el término $\tfrac12\log(1-\phi^2)$ y `CSS-ML` por defecto son correctos. El ejemplo T=40 con `set.seed(1)` da CSS 1.0086 y ML 0.9808. El error de `fit(method="css")` es el que se cita.
- **l. 4652–4655 · imprecisión.** Dice: «en mil simulaciones iguales CSS pasa de 1 en un 4 % de los casos — pero ML no lo hace en ninguna: la verosimilitud exacta cae a −∞ antes de llegar a la frontera».
  1. Ningún guion del repo calcula ese 4 %. En mis réplicas sale 4.6 %, 4.4 %, 2.8 % y 3.3 % con las semillas 1, 2, 3 y 2026 (`par_verifica.out`): «entre un 3 y un 5 %» sería más fiel.
  2. Que ML nunca pase de 1 lo garantiza también `transform.pars = TRUE`, el valor por defecto, que reparametriza para quedarse en la región estacionaria. No es solo cosa de la verosimilitud.
  3. ML se **pega** a la frontera: con la semilla 1, 132 de 1000 estimaciones son ≥ 0.999 y `optim` falla en 10 (`par_verifica2.out`). «No lo hace en ninguna» es cierto en sentido estricto, pero sugiere que ML se queda holgadamente dentro, y no es así.
- **Python l. 4783–4788 · imprecisión.** Dice: «El CSS de R (1.4032, −0.7099) no tiene equivalente directo aquí». En un AR puro, CSS es MCO condicional, y `statsmodels.tsa.ar_model.AutoReg(manchas, lags=2, trend="c")` da exactamente 1.4032 y −0.7099, con σ² 229.03 (`par_verifica_py.out`). Es cierto que la API `ARIMA` no lo ofrece; el equivalente existe en otra clase.
- **l. 4565–4567 (Yule y la «ventana centenaria» 1770–1869) · dudoso, fuera de mi lente.** El texto de Yule (1927) no está en `bibliografia/_local/`, así que no puedo contrastar qué años usó. Lo dejo a la revisión de fuentes.

## Módulo 3.8 · Criterios y diagnóstico (l. 4820–5150)

- **Correcto:** AIC, AICc y BIC con $k$ que incluye $\sigma^2$, en el mismo convenio que `arima()$aic`; $\log n>2$ desde $n=8$; la advertencia sobre $d$; $Q(h)$ y $\chi^2_{h-p-q}$; $\operatorname{Var}(\hat r_k)\approx(T-k)/(T(T+2))$; la dirección del sesgo sin `fitdf`. La simulación con `set.seed(8)` da 0.0257 y 0.0490. La rejilla completa de 11 modelos coincide (AICc, BIC y LB12), y también la de Python (0.3211, …, 0.1085). Las ACF residuales del AR(2) valen 0.1297, −0.1477 y 0.0285, con p = 0.0461 y 0.0996 sin `fitdf`. La mayor ACF residual es 0.1839 (rezago 11), seguida de 0.1718 (rezago 9), y ninguna sale de ±0.196. Los recortados de R dan 0.0232, 0.1424 y 0.1057, y los de Python 0.0232, 0.1420 y 0.1051. En el ARMA(2,1), θ̂ = 0.3732 con t = 2.78.
- **JS `diagnostico-residuales`:** lee los precálculos y el color y el veredicto son coherentes.
- **l. 4998–5009 · imprecisión (mecanismo).** Dice: «cada programa inicializa de otra forma el filtro para las $p$ primeras observaciones (R da 21.06 y statsmodels 52.54)». Los dos usan el mismo filtro de Kalman exacto; la diferencia está en lo que **devuelven**. `residuals()` de R entrega las innovaciones estandarizadas por $\sqrt{F_t/\sigma^2}$: $52.54/\sqrt{\gamma_0/\sigma^2}=52.54/\sqrt{6.226}=21.056$, idéntico al residuo de R. `res.resid` de statsmodels entrega la innovación cruda, cuya varianza en $t=1$ es $\gamma_0$ y no $\sigma^2$. Al estandarizar las de statsmodels con su `forecasts_error_cov` sale exactamente 21.056 y −6.911 (`par_verifica.out`, `par_verifica_py.out`). La moraleja se sostiene; el residuo «inflado» es el de statsmodels, y el de R es el adecuado para el diagnóstico.

## Módulo 3.9 · Dos casos reales (l. 5151–5772)

**Manchas solares**

- **Correcto:** la tabla de elasticidades (b, IC y R² con la receta de `genera_cap3.R`); los ceros (1810 en la ventana; 1711, 1712 y 1810 en la serie completa); λ de Guerrero 0.3062. La rejilla sobre √ coincide en los 11 modelos: el AR(2) es el mínimo por AICc (324.00) y por BIC (334.00), y LB vale 0.1644, 0.2005, 0.1856 y 0.1833. Coinciden también el modelo final (1.4027, −0.6853, μ 6.3317, s.e. 0.0727/0.0724, módulo 1.208, ω 0.5601, 11.22 años), las raíces del polinomio con el signo mal puesto (0.5598 y −2.6066) y la raíz MA del ARMA(2,1) (−2.6795), cuyas raíces AR son $1.092\pm0.766i$ con módulo 1.3339. Lo mismo vale para la forma cerrada de $\psi_j$, la tabla de pesos y bandas de 12 filas, $\sum\psi^2=6.136$, $\gamma_0=8.228$ frente a 8.149, el techo ±5.62 y el 94 % a h=6. Con Guerrero sobre la serie original salen 11.39 y p 0.4892. La asimetría (0.791 → 0.573) y Shapiro (0.0007 → 0.0470) coinciden con la definición de `genera_cap3.R` (momento 3 / sd³ con n−1).
- **l. 5196–5199 · imprecisión.** Dice: «ninguno separa limpiamente b=0.5 de b=1: los intervalos contienen los dos valores o casi». Ninguno contiene los dos:

  | Bloques | IC | Contiene 0.5 | Contiene 1 |
  |---|---|---|---|
  | 10 años | [0.593, 1.040] | no | sí |
  | 5 años | [0.475, 0.931] | sí | no |
  | 11 años | [0.533, 0.998] | no | no |

  La conclusión («los datos no dicen cuál») se sostiene porque las particiones **se contradicen**, no porque cada intervalo contenga ambos valores.
- **l. 5276 · menor.** «Sobre la desplazada … $p=0.2217$»: sale 0.22164, es decir 0.2216, tanto con `BoxCox()` como con la potencia directa (`par_verifica2.out`).
- **l. 5371–5377, 5430–5431 y JS l. 8996 y 9013 · ERROR (gráfico y prosa).** Se presenta $\pm R^j=\pm0.8278^j$ como «el envolvente que los amortigua», y el simulador lo dibuja así. Pero $\psi_j=R^j\sin((j+1)\omega)/\sin\omega$, y su envolvente es $\pm R^j/\sin\omega$, con $1/\sin\omega=1.882$. En el gráfico, $|\psi_j|>R^j$ en 16 de los 25 rezagos dibujados (j = 1, 2, 3, 6–9, 12–14, 17–20, 23, 24), y ninguno supera $R^j/\sin\omega$ (`par_verifica.out`). El estudiante ve barras que se salen del «envolvente». La vida media de 3.67 años sigue siendo correcta, porque no depende de la constante.
- **l. 5378 · imprecisión.** Dice: «deja $1.40$ de exceso al año siguiente, todavía $0.84$ tres años después». Los $\psi$ son multiplicadores del choque en la escala $\sqrt{\cdot}$: un choque unitario en $\sqrt{\text{manchas}}$ deja 1.40 unidades de $\sqrt{\text{manchas}}$. No son «manchas».
- **l. 5380 · imprecisión menor.** Dice: «cruces por cero en $j=4.61$ y $j=10.22$: medio ciclo y un ciclo de los 11.22 años». Los cruces son $(j+1)\omega=k\pi$. Medio ciclo y un ciclo son $j+1=5.61$ y $11.22$, así que los $j$ citados están desplazados una unidad respecto a esa lectura.
- **l. 5418–5419 · menor.** «Las dos últimas columnas … son, hasta el cuarto decimal, lo que imprime `forecast(ar2s, h = 6)`»: la tabla tiene 12 filas con dos decimales, y solo las 6 primeras se contrastan con `forecast`.
- **l. 5448–5450 · imprecisión con consecuencia.** Dice: «Volver a las manchas es elevar al cuadrado los extremos: la transformación es monótona». Elevar al cuadrado solo es monótono en $[0,\infty)$. Pronosticando desde 1869, el límite inferior en la escala de la raíz es negativo en h=7 y h=8 (−0.209 y −0.114; `par_verifica.out`). Al elevarlo al cuadrado da 0.044 y 0.013 en lugar de 0. Hay que truncar en 0 antes de elevar, o decir «monótona sobre los valores no negativos».
- **l. 5489–5490 · menor.** «[3.6] enseñó cuánto se aleja de la teoría una muestra de 100 datos»: el Módulo 6 usa T=200, y el laboratorio del 3.5 varía T entre 60 y 1000.
- **R l. 5590 · menor.** `#> [1] 0.1643575`: R 4.6.0 da 0.1643997. Los dos redondean a 0.1644. Puede ser una diferencia de versión u optimizador, pero la cifra impresa no se reproduce.
- **Python l. 5714 y 5720 · menor.** Los comentarios dicen `# 0.1780` y `# 11.2178`, pero Python imprime `0.178` y `11.218`: su periodo es 11.21797, no el 11.2178 de R. Sí se reproduce «descartando los 2 primeros, los dos programas dan 0.1682».

**TRM**

- **Correcto:** n = 137, banda 0.1675, ACF (0.105, −0.077, −0.078, 0.006, 0.193, 0.123); fuera de la banda quedan la ACF en los rezagos 5 y 8 (0.193 y −0.198). LB da 0.0931, 0.0601 y 0.0599. Con media, el MA(1) da θ 0.1262 (s.e. 0.0912), media 0.2681 (s.e. 0.3195, t 0.84). Sin media, el AICc es 722.653 frente a 722.663, y LB(r²) da 0.9166. El bloque R corrió contra la API y coincide.
- **l. 5532–5536 y 5550 · CIFRA INCORRECTA / atribución.** Dice: «si se ajusta el MA(1) que sugiere auto.arima: $\hat\theta_1=0.1262$ (e.e. 0.0912, t = 1.38)» y «auto.arima() devuelve el MA(1) sin término constante». Hay dos problemas:
  1. 0.1262 es el θ del MA(1) **con** media. El MA(1) sin media que devuelve `auto.arima` tiene θ = 0.1326 (s.e. 0.0905, t ≈ 1.47).
  2. `auto.arima(ret)` con sus argumentos por defecto, que es lo que correrá un estudiante, devuelve **ARIMA(0,0,0) con media cero** (AICc 722.66), no un MA(1). El MA(1) solo aparece con `d = 0, seasonal = FALSE, stepwise = FALSE, approximation = FALSE` (`genera_cap3.R` l. 444), y el capítulo no muestra esa llamada (`par_verifica_trm.out`).

  La conclusión del caso («es ruido blanco») sale reforzada; lo incorrecto es lo que se atribuye a auto.arima y la cifra.
- **l. 5552–5554 · ERROR que enseña algo falso.** Dice: «Si al comparar AICc de dos modelos uno incluye media y el otro no, no los estás comparando en igualdad de condiciones». Se repite en el punto (3) de l. 5873: «el AICc no compara modelos … ni con y sin media». Es falso. Con o sin media, los dos modelos se ajustan a los mismos datos y sus verosimilitudes son comparables. El AICc está para eso: penaliza el parámetro de más. `auto.arima` hace exactamente esa comparación en su búsqueda; la traza muestra «with non-zero mean 723.80» frente a «with zero mean 722.66» y elige la segunda. Lo único no comparable es lo que cambia los datos ($d$, la transformación). Si lo que se quería era aislar el efecto del término MA, la elección de comparar los dos modelos sin media es razonable; la regla general que se enuncia, no.
- **l. 5558 · imprecisión (contradicción).** El título de la nota, «Donde sí hay estructura: en el cuadrado», afirma lo contrario de su contenido: p = 0.9166, «tampoco hay agrupamiento de volatilidad».

## Módulo 3.10 · Autorregresión, redes y cierre (l. 5773–6257)

- **Correcto:** la tabla de criterios ($\phi_{pp}=\phi_p$, que en el AR(2) final vale −0.6853), la tabla de modelos, el resumen y la advertencia del ARMA(2,2) con factor común. La ACF de (1.1, −0.28 | 0.1, −0.2) coincide con la del ARMA(1,1) (0.7 | 0.5) hasta 1.1e−16. Quiz `cap3`: las diez claves son correctas, y también los distractores numéricos (2.44, 2.88, 2.98, 4.40, 6.29), las tolerancias (0.0006 en 0.4878 y 0.006 en 4.88) y las cifras de las retroalimentaciones.
- **l. 5842 · ERROR que enseña algo falso.** Dice: «La condición de estabilidad del entrenamiento ($|w|<1$, para que el gradiente no explote **ni se desvanezca**)». Con $|w|<1$ el gradiente $\propto w^k$ **se desvanece**; con $|w|>1$ explota. $|w|<1$ evita la explosión, no el desvanecimiento, y la frase siguiente del propio párrafo lo confirma («el gradiente que se desvanece … y el desvanecimiento de $\phi^k$ … son el mismo fenómeno»).
- **l. 5854 · menor.** «el AR(2) tiene tres [parámetros]». Con el convenio del Módulo 8 ($k$ incluye $\sigma^2$) son cuatro.
- **l. 5969 · menor.** «$t=19.29$ y $t=-9.47$» salen de dividir coeficientes y errores estándar ya redondeados. Sin redondear dan 19.31 y −9.46.
- **Ejercicio 1 (`lh`, l. 6018–6086):** todas las cifras se reproducen (AICc, BIC, LB, φ 0.5739, s.e. 0.1161, Shapiro 0.0083). **Menor:** «cada medición conserva el 57 % de la anterior» (l. 6081). Lo que conserva el 57 % es la **desviación respecto a la media**.
- **Ejercicio 2 (MA(2) 0.6, 0.4):** correcto. Las raíces tienen módulo 1.5811, ρ = 0.5526 y 0.2632, los π están bien y la explicación de la cota es correcta.
- **Ejercicio 3 (l. 6143–6195) · ERROR que enseña algo falso + cifra incorrecta.** Las cifras de la tabla se reproducen. La discusión, no:
  - **Cifra incorrecta:** «$p<0.001$ en las tres» (l. 6187). Para 1900–1988 sale p = 0.00102 (0.0010 en la propia tabla).
  - **Interpretación falsa:** «la causa no es que el modelo empeore … sino que la prueba gana potencia: con n = 289 en vez de 100» (l. 6188–6191), y la moraleja «que un modelo pase el diagnóstico depende de cuántos datos tengas». Dos de las tres ventanas que fallan tienen tamaño parecido o **menor** que la de Yule: 1870–1988 (n = 119, p = 0.0007) y 1900–1988 (n = 89, p = 0.0010). Además, cualquier otra ventana de exactamente 100 años rechaza (`par_verifica2.out`):

    | Ventana | p |
    |---|---|
    | 1789–1888 | 0.0245 |
    | 1820–1919 | 0.0197 |
    | 1850–1949 | 0.0092 |
    | 1889–1988 | 0.0006 |

    La que no rechaza es 1770–1869, y es la excepción. El tamaño muestral no explica el derrumbe. Lo que muestran los datos es que el AR(2) en raíz ajusta peor fuera de esa ventana, o que la ventana de Yule es la afortunada. «Hay más potencia con más datos» es cierto en general, pero aquí la evidencia lo desmiente. Hay que reescribir la discusión y la respuesta corta de l. 6163–6164.
- **Actividad preparatoria del Parcial 2 (l. 9354–9632):** diez ítems con las claves correctas. Los recalculé todos: c = 10.51 (distractores 18.94, 243.46 y 40.08), θ = 0.4606/2.1710, Var = 2.5683 (distractores 1.7651, 1.0889 y 1.6010), ρ = 0.75/0.65, $\phi_{22}=0.2$, $\phi_{33}=0$ (distractores 0.54 y 0.568), el AR(2) (1, −0.5) con módulo 1.4142 y periodo 8, $(1-0.3B)(1-B)$, la deriva 118/144, la sobrediferenciación 0.5/−0.5 y $k=\lfloor95^{1/3}\rfloor=4$. El ítem 1 ya precisa la causalidad.

## Módulo 11 · Simulacro (l. 6258–6320, datos l. 9818–9950)

- Sin clave, como se pretende. Comprobé que cada ítem tiene su opción correcta y que las cifras de las opciones salen bien:
  - ítem 1: dos procesos estacionarios, $(-1)^t\varepsilon_t$ y el AR 0.92;
  - ítem 2: $k=\lfloor115^{1/3}\rfloor=4$;
  - ítem 3: 1.62;
  - ítem 4: 164 y 193.6;
  - ítem 5: $(1+0.6B)(1-B)$ da (0.4, 0.6), que no es estacionario;
  - ítem 6: (1.4, −0.45) es estacionario con raíces reales, porque $\phi_1^2+4\phi_2=0.16$;
  - ítem 7: c = 28.45 (14.51 y 126.19 son distractores coherentes);
  - ítem 8: 0.5966/1.6761;
  - ítem 9: θ = −0.12 da 4.8918;
  - ítem 10: 0.7143/0.6571 con 0.3/0.
- «35 % del capítulo 2 y 65 % de este» (l. 6280) solo cuadra contando como medias las tres preguntas mixtas (2 + 1.5 = 3.5 de 10). Es correcto, aunque el texto no lo explica.

---

## Recuento por gravedad

| Gravedad | Confirmados | Dudosos |
|---|---|---|
| Error que enseña algo falso | 5 | 0 |
| Cifra incorrecta | 2 | 0 |
| Imprecisión | 10 | 1 (burn-in, 3.6) |
| Menor | 11 | 1 (ventana de Yule: a fuentes) |

## Los errores, uno por uno (ordenados por daño)

1. **Ejercicio 3, discusión (l. 6163–6164, 6187–6194).** Atribuye el fallo de Ljung–Box fuera de 1770–1869 a la potencia que da una n mayor, y saca de ahí la moraleja. Es falso: falla con n = 89 y n = 119, y con cualquier otra ventana de 100 años (p entre 0.0006 y 0.0245). Además, «p < 0.001 en las tres» es falso para 1900–1988 (0.00102). *Error que enseña algo falso + cifra incorrecta. Confirmado.*
2. **3.5, la recursión AR aplicada a ρ₁ (l. 4173–4176; R l. 4221–4225; Py l. 4267–4269).** El 0.8 sale de usar $\rho_{-1}=\rho_0=1$. Con $\rho_{-1}=\rho_1$ da 0.7584. El código enseña exactamente el error que el ítem 10 del Parcial 2 marca como incorrecto. *Error. Confirmado.*
3. **«El AICc no compara modelos con y sin media» (l. 5552–5554 y l. 5873, punto 3).** Es falso: misma serie y misma verosimilitud. `auto.arima` hace esa comparación y el capítulo usa su resultado. Además está en la lista de «verificaciones» frente a los asistentes de IA. *Error. Confirmado.*
4. **3.10, RNN (l. 5842).** «$|w|<1$ para que el gradiente no explote ni se desvanezca»: con $|w|<1$ el gradiente se desvanece. *Error. Confirmado.*
5. **3.9, envolvente de los ψ (l. 5371–5377, 5430–5431; JS l. 8996 y 9013).** Dibuja $\pm R^j$ cuando el envolvente es $\pm R^j/\sin\omega$ (×1.88). 16 de 25 barras se salen. *Error de prosa y gráfico. Confirmado.*
6. **3.9 TRM, auto.arima y θ̂ (l. 5532–5536, 5550).** 0.1262 es el MA(1) con media; el de auto.arima, sin media, da 0.1326 (s.e. 0.0905). Además, `auto.arima(ret)` por defecto devuelve ruido blanco con media cero, no un MA(1). *Cifra incorrecta / atribución. Confirmado.*
7. **3.9, «la transformación es monótona» al volver de la raíz (l. 5448–5450).** Los límites inferiores en la escala de la raíz son negativos en h = 7 y 8, y al elevarlos al cuadrado dan cotas positivas falsas. *Imprecisión con consecuencia. Confirmado.*
8. **Causalidad (l. 2868, 3031, 3118–3123).** «No existe solución estacionaria si $|\phi|\ge1$», el «si y solo si» del triángulo y la «varianza finita»: valen para la solución causal, no en general. *Imprecisión. Confirmado.*
9. **3.8, mecanismo de la discrepancia R/statsmodels (l. 4998–5009).** No es otra inicialización: R devuelve innovaciones estandarizadas y statsmodels las crudas. *Imprecisión. Confirmado.*
10. **3.7, ML «no lo hace en ninguna» y el 4 % (l. 4652–4655).** Que ML no pase de 1 lo impone `transform.pars`; ML queda en ≥ 0.999 en el 13 % de las réplicas y falla en el 1 %. El 4 % oscila entre 2.8 y 4.6 % según la semilla, y ningún guion lo calcula. *Imprecisión. Confirmado.*
11. **3.7 Python, «el CSS no tiene equivalente directo» (l. 4783–4788).** `AutoReg(trend="c")` lo reproduce exactamente. *Imprecisión. Confirmado.*
12. **3.9, elasticidades: «los intervalos contienen los dos valores o casi» (l. 5196–5199).** Ninguno los contiene; lo que pasa es que se contradicen entre particiones. *Imprecisión. Confirmado.*
13. **3.9, título de la nota «Donde sí hay estructura: en el cuadrado» (l. 5558).** Contradice su texto (p = 0.9166). *Imprecisión. Confirmado.*
14. **3.9, «1.40 de exceso» (l. 5378).** Son unidades de $\sqrt{\text{manchas}}$ por choque unitario, no manchas. *Imprecisión. Confirmado.*
15. **3.1, «|B| = 1, es decir φ = 1» (l. 2885–2886).** También φ = −1, que no es una caminata aleatoria. *Imprecisión. Confirmado.*
16. **3.6, «tendencia espuria» sin `burnin` (l. 4501–4502).** El efecto es un tramo inicial con varianza reducida. *Imprecisión. Dudoso.*
17. **3.9, cruces por cero «medio ciclo y un ciclo» (l. 5380).** Corresponden a j + 1, no a j. *Menor/imprecisión.*
18. **Menores:**
    - p = 0.2217 → 0.2216 (l. 5276);
    - `#> 0.1643575` → 0.1643997 (l. 5590);
    - comentarios de Python `0.1780` y `11.2178` → `0.178` y `11.218` (l. 5714, 5720);
    - `polynomial_ar` impreso (l. 2797);
    - 6.7e−16 atribuido a 600 términos cuando se midió con 2000 (l. 3701–3704, JS l. 8133–8138);
    - t = 19.29/−9.47 → 19.31/−9.46 (l. 5969);
    - «el AR(2) tiene tres» parámetros (l. 5854);
    - «una muestra de 100 datos» en el 3.6 (l. 5489–5490);
    - «forecast(h = 6)» frente a una tabla de 12 filas (l. 5418–5419);
    - «conserva el 57 % de la anterior» (l. 6081);
    - la ventana 1770–1869 «de Yule» no se puede contrastar con lo que hay en `bibliografia/` (se pasa a fuentes).

Recordatorio de ensamblado: las correcciones de los módulos 3.1–3.10 y del JS van en `ensamblado/cap3/cap3_modulos.html` y `cap3_js.js`, no en el HTML final. El texto de la actividad del Parcial 2 y del simulacro se genera fuera del repositorio, pero no requieren cambios.
