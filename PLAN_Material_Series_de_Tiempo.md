# Plan de implementación: Material de estudio — Series de Tiempo 2026-II

**Fecha:** 2026-07-23 · **Autor del curso:** Javier Mauricio Sierra · Universidad El Bosque

## Resumen

Sitio estático de 6 capítulos HTML autocontenidos (+ portada `index.html`), con el mismo
formato visual y técnico del material de Muestreo (`Muestreo/Htmls_Muestreo/`), alineado
con el syllabus `Syllabus/6_Series_de_Tiempo_2026-II.docx`: 4 módulos del curso repartidos
en 6 capítulos temáticos, código **R (fpp3/fable/feasts)** como principal y **Python
(statsmodels)** como equivalente, **un simulador interactivo con sliders por capítulo**,
publicado en un repo git propio con GitHub Pages.

## Decisiones de arquitectura

| Decisión | Elección | Justificación |
|---|---|---|
| Formato | 1 archivo HTML autocontenido por capítulo, sin build | Igual que Muestreo; portable, sin dependencias locales |
| Stack CDN | Tailwind, KaTeX, Chart.js, Prism (+ `prism-r`), Font Awesome, Montserrat/Fira Code | Mismo stack de Muestreo; solo se añade el componente Prism para R |
| Paleta y layout | Verde `#012820` / naranja `#FF6600`, sidebar sticky con módulos internos, tarjetas `usta-card`, cajas `definition`/`note`/`warning`, botones copiar/ocultar código | Continuidad visual exacta con Muestreo |
| Código | Bloque R primero (lenguaje del syllabus) + pestaña/bloque "Equivalente en Python" por tema | Elección del usuario: R + Python |
| Simuladores | JavaScript puro + Chart.js con `<input type="range">`; cálculos en el navegador cuando sean livianos (simulación AR/MA, ACF empírica) y **precalculados en R e incrustados como JSON** cuando no (ajustes ARIMA, AIC de rejillas de modelos) | Un ajuste ARIMA real no es viable en el navegador; precalcular mantiene el archivo autocontenido |
| Datos | Series incrustadas como arrays JS: `AirPassengers`, 1–2 series de FPP3 (p. ej. producción de electricidad australiana) y una serie mensual colombiana (p. ej. IPC del DANE) descargada una vez y congelada en el archivo | Sin `fetch` externo → funciona offline y en Pages |
| Referencias | Cada capítulo cierra con lecturas exactas de FPP3 (cap./sección según cronograma) y Shumway & Stoffer | Amarra el material a la bibliografía del syllabus |
| Idioma | Español, con términos técnicos en inglés entre paréntesis la primera vez (*lag*, *white noise*, *backtesting*) | Igual que el syllabus |

## Estructura de archivos

```
Series de tiempo/
└── Htmls_Series/
    ├── index.html
    ├── capitulo-1-componentes-descomposicion.html
    ├── capitulo-2-estacionariedad-acf-pacf.html
    ├── capitulo-3-modelos-ar-ma-arma.html
    ├── capitulo-4-modelos-arima.html
    ├── capitulo-5-sarima.html
    ├── capitulo-6-pronostico-evaluacion.html
    ├── README.md
    ├── .nojekyll
    └── .gitignore
```

Carpeta auxiliar (no publicada, en `.gitignore`): `Series de tiempo/precalculo/` con los
scripts R que generan los datos/ajustes incrustados, para reproducibilidad.

---

## Contenido capítulo por capítulo

### Capítulo 1 — Introducción y componentes de una serie de tiempo
*Módulo I del syllabus · Semanas 1–2 · Lecturas: FPP3 caps. 1–3*

Módulos internos (~9):
1. ¿Qué es una serie de tiempo? Motivación: demanda, anomalías, señales, economía
2. Objetos temporales en software: `tsibble`/`ts` en R, `pandas` con índice temporal
3. Visualización: gráfico de tiempo, gráfico estacional, subseries, gráfico de rezagos
4. Los cuatro componentes: tendencia, estacionalidad, ciclo y ruido (ciclo ≠ estacionalidad)
5. Medias móviles y suavizamiento
6. Descomposición clásica aditiva y multiplicativa
7. Descomposición STL
8. Ajuste estacional; fuerza de tendencia y de estacionalidad
9. Conexión con ciencia de datos · Resumen · Lecturas

**Simulador:** "Construye tu serie" — sliders de pendiente de tendencia, amplitud
estacional y desviación del ruido; se ve la serie compuesta y sus componentes separados.
**Fórmulas clave:** \(y_t = T_t + S_t + R_t\), \(y_t = T_t \times S_t \times R_t\), media móvil de orden m.
**Código:** R `autoplot`, `gg_season`, `gg_lag`, `model(STL(...))` · Python `seasonal_decompose`, `STL`.

### Capítulo 2 — Estacionariedad, ACF/PACF y diferenciación
*Módulo I · Semanas 3–4 · Lecturas: FPP3 secc. 9.1, 3.1–3.2 (Box–Cox)*

Módulos internos (~9):
1. Estacionariedad estricta y débil; por qué importa
2. Ruido blanco
3. Autocovarianza, autocorrelación (ACF) y correlograma
4. Autocorrelación parcial (PACF): definición e interpretación
5. Caminata aleatoria y caminata con deriva
6. Pruebas de raíz unitaria: ADF y KPSS (hipótesis opuestas — advertencia)
7. Diferenciación regular y estacional; cuántas diferencias (`unitroot_ndiffs`)
8. Transformaciones: logaritmo y Box–Cox
9. Pipeline de preprocesamiento temporal (conexión ciencia de datos) · Resumen

**Simulador:** slider de \(\phi\) en \(y_t = \phi y_{t-1} + \varepsilon_t\) (de 0 a 1.05):
la serie simulada y su ACF empírica se actualizan en vivo; en \(\phi = 1\) se ve la
caminata aleatoria y la ACF que no decae. Botón "aplicar diferencia".
**Fórmulas clave:** \(\gamma_k, \rho_k\), operador \(B\), \(\nabla y_t = (1-B)y_t\), \(\nabla_m\), Box–Cox.
**Código:** R `ACF/PACF` (feasts), `unitroot_kpss`, `difference()` · Python `plot_acf/plot_pacf`, `adfuller`, `kpss`, `.diff()`.

### Capítulo 3 — Modelos AR, MA y ARMA
*Módulo II · Semanas 5–7 · Lecturas: FPP3 secc. 9.3–9.5, 5.4; Shumway & Stoffer cap. 3*

Módulos internos (~10):
1. Operador de rezago y polinomios característicos
2. AR(p): definición, condición de estacionariedad, ACF/PACF teóricas
3. MA(q): definición, invertibilidad, ACF/PACF teóricas
4. Dualidad AR ↔ MA (representaciones infinitas)
5. ARMA(p,q); tabla de identificación con ACF/PACF
6. Simulación de procesos (R y Python)
7. Estimación por máxima verosimilitud; AIC, AICc y BIC
8. Diagnóstico de residuales: Ljung–Box, normalidad, gráficos
9. Conexión: autorregresión como base de los métodos secuenciales (RNN/LSTM)
10. Resumen · Lecturas

**Simulador:** sliders \(\phi_1, \phi_2\) (AR) y \(\theta_1\) (MA): serie simulada + ACF y
PACF **teóricas** dibujadas en vivo; para AR(2), el triángulo de estacionariedad con el
punto \((\phi_1,\phi_2)\) marcado dentro/fuera.
**Fórmulas clave:** \(\phi(B)y_t = \varepsilon_t\), \(y_t = \theta(B)\varepsilon_t\), ecuaciones de Yule–Walker, estadístico de Ljung–Box.
**Código:** R `arima.sim` / fable `ARIMA(y ~ pdq(p,0,q))`, `gg_tsresiduals`, `ljung_box` · Python `ArmaProcess`, `ARIMA`, `acorr_ljungbox`.

### Capítulo 4 — Modelos ARIMA y selección de modelos
*Módulo III · Semanas 8–9 · Lecturas: FPP3 secc. 9.5–9.7*

Módulos internos (~8):
1. De ARMA a ARIMA: integración y el orden d
2. Metodología Box–Jenkins: identificación → estimación → diagnóstico → (re)especificación
3. Identificación práctica de (p, d, q) sobre una serie real
4. El algoritmo de Hyndman–Khandakar (`auto.arima` / `ARIMA()` de fable)
5. Selección manual vs. automática; comparación por AICc/BIC
6. Caso de estudio completo de principio a fin (serie colombiana)
7. Errores comunes: sobrediferenciación, sobreajuste, comparar AIC entre distintos d
8. Resumen · Lecturas

**Simulador:** "Explorador de modelos" — el usuario elige \(p, d, q \in \{0,1,2\}\) con
steppers sobre la serie del caso de estudio; se muestran AICc, BIC y la ACF de los
residuales de ese modelo, **precalculados en R** para la rejilla de 27 combinaciones e
incrustados como JSON.
**Código:** R fable `ARIMA`, `report`, `glance` · Python `pmdarima.auto_arima` / `statsmodels`.

### Capítulo 5 — Modelos ARIMA estacionales (SARIMA)
*Módulo III · Semanas 10–11 · Lecturas: FPP3 secc. 9.9*

Módulos internos (~8):
1. Estacionalidad en la ACF/PACF: picos en rezagos múltiplos de m
2. Notación SARIMA(p,d,q)(P,D,Q)\(_m\) y su polinomio completo
3. Diferenciación estacional: cuándo y cuántas veces
4. Identificación de los órdenes estacionales
5. Estimación y diagnóstico de SARIMA
6. Casos: `AirPassengers` (log + diferencias) y la serie mensual colombiana
7. Panorama comparativo: SARIMA vs. Prophet, RNN/LSTM y Transformers temporales (cuándo elegir qué)
8. Resumen · Lecturas

**Simulador:** sobre `log(AirPassengers)`, dos interruptores — "diferencia regular" y
"diferencia estacional (m=12)" — muestran la serie transformada y su ACF en las 4
combinaciones (calculables en el navegador).
**Fórmulas clave:** \(\Phi(B^m)\phi(B)(1-B)^d(1-B^m)^D y_t = \Theta(B^m)\theta(B)\varepsilon_t\).
**Código:** R fable `ARIMA(y ~ pdq() + PDQ())` · Python `SARIMAX`.

### Capítulo 6 — Pronóstico, métricas de error y backtesting
*Módulo IV · Semanas 12–14 (+ nociones de la semana 15) · Lecturas: FPP3 secc. 5.8–5.10, 9.8*

Módulos internos (~9):
1. Pronóstico puntual h pasos adelante con ARIMA/SARIMA
2. Intervalos de pronóstico: construcción e interpretación; el abanico de incertidumbre
3. Métodos de referencia (*benchmarks*): media, naïve, naïve estacional, deriva
4. Métricas de error: RMSE, MAE, MAPE — definiciones, unidades y límites (MAPE con valores cercanos a 0); mención de MASE
5. Partición temporal entrenamiento/prueba; por qué la validación cruzada estándar mezcla pasado y futuro
6. Validación de origen móvil (*rolling-origin* / *time series cross-validation*)
7. Backtesting: comparación honesta de varios modelos sobre la misma serie
8. Guía para el proyecto de pronóstico del curso + uso ético y verificación crítica de asistentes de IA
9. Resumen · Lecturas

**Simulador:** dos vistas — (a) slider de horizonte h que extiende un pronóstico
precalculado con bandas 80/95%; (b) animación de origen móvil: la ventana de
entrenamiento avanza paso a paso y se acumula el error de prueba.
**Fórmulas clave:** \(\hat{y}_{T+h|T}\), intervalos \(\hat{y} \pm c\,\hat\sigma_h\), RMSE, MAE, MAPE, MASE.
**Código:** R `forecast(h=...)`, `accuracy()`, `stretch_tsibble` · Python `get_forecast`, advertencia sobre `TimeSeriesSplit`.

### Portada (`index.html`) + README + repo

Portada con tarjetas de los 6 capítulos (igual estilo que la de Muestreo), README con
tabla de contenido y stack, `.nojekyll`, `git init` + primer commit, instrucciones de
publicación en GitHub Pages.

---

## Lista de tareas

### Fase 0 — Plantilla y datos (fundación) — ✅ COMPLETADA (2026-07-23)

- [x] **T1 · Plantilla base** — `plantilla/plantilla-capitulo.html`. Paleta y layout de
  Muestreo, `prism-r` añadido, pestañas R/Python con estado ARIA, fábrica de simuladores
  (`SIMULADORES` + `crearControles` + `crearGraficoLinea` + `generarRuidoNormal` +
  `calcularACF`), ruido con semilla fija (mulberry32 + Box–Muller), gráficos destruidos al
  cambiar de módulo. 3 módulos de demostración (estilo, código, simulador).
  - *Verificado:* consola limpia; KaTeX en línea y display (con `\underbrace`); Prism
    resalta R (35 tokens) y Python; pestañas conmutan y actualizan `aria-selected`;
    deslizadores actualizan el gráfico en vivo (β: 0.5→2 movió y₁₂₀ de 48.1 a 226.6);
    los 2 bloques R parsean con `parse()`; el bloque Python corre verbatim.
- [x] **T2 · Datos y precálculos** — `precalculo/genera_datos.R` (R base + jsonlite, sin
  forecast/fpp3). Salidas en `precalculo/salidas/`: `datos_series.js/.json` (AirPassengers,
  co2, Nile, USAccDeaths, TRM mensual 2015-01→2026-06 de datos.gov.co),
  `cap4_rejilla_arima.json` (27 modelos sobre el Nilo), `cap6_pronostico.json` (modelo
  airline: pronóstico con bandas 80/95, métricas vs. 4 referencias, origen móvil 37
  orígenes × h12).
  - *Verificado:* `Rscript` corre de principio a fin; JSON validados; `node --check` del
    .js; verificación cruzada R↔Python (statsmodels): coeficientes casi idénticos
    (ma1 −0.3424 vs −0.3422) y pronósticos con diferencia máxima 0.015%.
  - *Ajustes sobre el plan original:* (1) caso de estudio del cap. 4 = **Nilo** (anual, sin
    estacionalidad, resultado de libro ARIMA(1,1,1)) en lugar de la serie colombiana; la
    TRM queda para ejemplos de los caps. 2 y 5. (2) La rejilla reporta **mejor AICc por
    cada d** — nunca un mínimo global, porque el AIC no es comparable entre distintos d
    (hallazgo de la auditoría, y contenido del módulo "errores comunes"). (3) Series de
    R base en lugar de series fpp3 (sin dependencias). (4) Prueba de raíz unitaria:
    Phillips–Perron de R base (`PP.test`) en lugar de ADF/KPSS de paquetes.

**Refinamientos de plantilla (2026-07-24, tras revisión de Javier del pie de página):**
- Legibilidad de las referencias bibliográficas. (1) Token de paleta `gold`
  `#90FF00` → `#FFC24B` (ámbar cálido): los títulos de libros dejan de ser verde-lima
  sobre verde oscuro (contraste ~9.9:1, sin vibración de la misma familia de color).
  (2) Bug de CSS: la regla global `ul li { color:#374151 }` (para listas en tarjetas
  claras) se filtraba al `<footer>` y pintaba el texto de autores/editoriales en gris
  oscuro casi ilegible; se añadió `footer ul li { color: rgba(255,255,255,0.92) }`
  (mayor especificidad, sin `!important`). Ambos cambios se heredan a los 6 capítulos.

### Checkpoint 0
- [x] Plantilla aprobada (2026-07-24, con los refinamientos del pie de página anotados arriba)
      y **regenerada desde el capítulo 2 el 2026-07-26**, porque se había quedado sin ninguno
      de los componentes añadidos después. Ahora lleva los 10 al día y 4 módulos de
      demostración: cajas y tipografía, código en pestañas, los tres tipos de control con las
      dos fábricas de gráficos, y autoevaluación con los cuatro tipos de pregunta más un
      ejercicio guiado. No incrusta ningún dato: los simuladores de demostración generan sus
      series en JS con semilla fija.
      - *Verificado:* consola limpia, 0 errores de KaTeX, los 4 módulos navegan con sus
        gráficos creados y destruidos, los tres simuladores responden en valores extremos, el
        quiz cubre los cuatro tipos y el desplegable del ejercicio abre. Hueco mínimo entre
        elementos: 8 px.
      - **Regla que hay que respetar:** cuando se añada un componente a un capítulo, se añade
        a la plantilla **en la misma sesión**. Se quedó atrás una vez precisamente por no
        hacerlo, y el skill decía "copia la plantilla" cuando ya no servía.
      - *Cuándo usar cuál:* la plantilla es para arrancar un **curso nuevo**; para un capítulo
        más de un curso ya empezado, copia su **último capítulo**, que trae datos y contexto.

### Fase 1 — Capítulos 1 y 2

- [x] **T3 · Capítulo 1** (componentes y descomposición) — `Htmls_Series/capitulo-1-componentes-descomposicion.html`.
  9 módulos: (1) qué es una serie, (2) ts/tsibble/pandas, (3) visualización + gráfico
  estacional, (4) cuatro componentes + simulador "construye tu serie", (5) medias móviles
  (simulador interactivo con slider de orden m), (6) descomposición clásica multiplicativa
  (4 paneles), (7) STL sobre log (4 paneles), (8) desestacionalización + fuerza F_T/F_S,
  (9) ciencia de datos + resumen + lecturas. Títulos bilingües ES/EN. Datos y descomposición
  (clásica + STL) precalculados en R (`cap1_descomposicion.json` / `cap1_datos.js`).
  - *Verificado:* consola limpia; 9 módulos navegan; los 8 gráficos se crean y destruyen al
    cambiar de módulo; 0 errores KaTeX; simulador de media móvil responde (m=3→142 pts,
    m=24→120, recorta más con m mayor); los **5 bloques R** pasan `parse()`; los **5 bloques
    Python** ejecutan encadenados sin error; verificación cruzada: índices estacionales
    Python `seasonal_decompose` = R `decompose` (dif. máx. 0.0).
  - *Ajustes:* (1) se añadió un simulador de media móvil (además del "construye tu serie").
    (2) Descomposición clásica y STL **precalculadas en R** e incrustadas (STL no es viable en
    el navegador). (3) El bloque Python usa índice de fechas `freq="MS"` en vez de
    `period_range`: `seasonal_decompose().plot()` y `STL().plot()` fallan con `PeriodIndex`
    (un estudiante toparía el error) — [[leccion-...]] candidata si reaparece.
  - *Dependencias:* T1, T2. *Tamaño:* L (una sesión completa).
- [x] **T4 · Capítulo 2** (estacionariedad, ACF/PACF, diferenciación) — `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html`.
  9 módulos: (1) estacionariedad estricta y débil, (2) ruido blanco, (3) ACF y correlograma,
  (4) PACF con Durbin–Levinson, (5) caminata aleatoria y raíz unitaria, (6) ADF y KPSS,
  (7) diferenciación, (8) logaritmo y Box–Cox, (9) pipeline + resumen + autoevaluación.
  **4 simuladores interactivos** (explorador ACF/PACF de 8 series; deslizador de φ con ACF en
  vivo y botón de diferenciar; contador de diferencias con lectura de varianza; deslizador de
  λ con la curva del criterio de Guerrero) **+ 4 paneles estáticos**. Precálculo en
  `precalculo/genera_cap2.R` → `cap2_estacionariedad.json` / `cap2_datos.js`.
  - *Verificado:* consola sin errores; 9 módulos navegan; canvas creados = gráficos activos en
    todos (se destruyen al cambiar de módulo); **0 errores KaTeX** en 211 fórmulas; los 8
    bloques R parsean y **corren** (salvo las líneas `library(fpp3)`, que no está instalado
    aquí); los 8 bloques Python corren encadenados. Verificación cruzada **R = Python = JS**:
    ACF, PACF, ADF y KPSS sobre las 8 series coinciden con dif. máx. 1e-4 (el redondeo del
    JSON); el λ de Guerrero en JS reproduce `BoxCox.lambda` con dif. 1e-14. El simulador de
    diferenciación reproduce la tabla de varianzas de R (dif. relativa 3.5e-4) y su ACF(1) es
    idéntica a 4 decimales. La TRM descargada en vivo el 2026-07-26 devuelve exactamente las
    cifras del texto (ADF −1.9783, KPSS 2.2427, n = 138).
  - *Hallazgos de la auditoría (todos incorporados al capítulo):*
    1. **`adf.test(AirPassengers)` da p < 0.01**, es decir "estacionaria", en una serie con
       tendencia y estacionalidad obvias. Causa: su `k` por defecto (5) es menor que m = 12.
       Verificado con tres evidencias: con k = 12 el estadístico pasa a −1.53 (p = 0.771);
       sobre la serie desestacionalizada, a −2.15 (p = 0.513); y un Monte Carlo de 500
       réplicas muestra que el falso rechazo sube del 3.2 % al 17.6 % con la amplitud
       estacional. **Es ahora el núcleo del módulo 6.**
    2. **`ndiffs()` y `tseries::kpss.test()` discrepan** sobre ∇₁₂log(AP): d = 1 vs. d = 0.
       No es un bug: `ndiffs` llama a `urca::ur.kpss` con truncamiento ⌊3√n/13⌋ = 2 y
       `kpss.test` usa ⌊4(n/100)^¼⌋ = 4. Documentado como caja de advertencia en el módulo 7.
    3. **El ADF de R y el de statsmodels dan el mismo estadístico y distinto p-valor**
       (tablas de Banerjee et al. vs. superficie de MacKinnon). Documentado en el bloque
       Python del módulo 6.
    4. Corregido antes de publicar: `diff(x, differences = 0)` **lanza un error** en R (no es
       la identidad), así que el bucle de sobrediferenciación no habría corrido; y los bloques
       de R y Python del módulo 6 usaban `trm` sin definirlo nunca. Los dos arreglados.
    5. Corregido antes de publicar: había justificado el uso del logaritmo diciendo que la
       curva de Guerrero "es muy plana cerca del mínimo". **Es falso**: en λ = 0 el criterio
       está 88 % por encima del mínimo y la franja dentro del 20 % es [−0.41, −0.17]. El texto
       ahora da las cifras reales (0.530 sin transformar → 0.153 con log → 0.081 en el óptimo,
       o sea el 84 % de la mejora posible) y justifica el logaritmo por interpretabilidad.
  - *Desviaciones sobre el plan:* (a) se instalaron **`tseries` y `forecast`** (decisión de
    Javier) para que las cifras salgan de las mismas funciones que usarán los estudiantes;
    Fase 0 había evitado dependencias a propósito. (b) El precálculo va en un **script aparte**
    (`genera_cap2.R`) para no re-descargar la TRM ni re-ajustar los 37 modelos del cap. 6 en
    cada corrida. (c) El archivo pesa **191 KB** (50 KB comprimido), por encima del límite
    práctico de ~160 KB de la tabla de riesgos: es contenido real (9 módulos densos), no
    duplicación, y GitHub Pages sirve comprimido. (d) La diferenciación **estacional** se trata
    en texto, código y correlogramas precalculados, pero el simulador interactivo cubre solo la
    regular, para no duplicar el del capítulo 5.
  - *Dependencias:* T1, T2. *Tamaño:* L.

- [x] **T4b · Componente de autoevaluación** (nuevo en la plantilla, decisión de Javier).
  Cajas `.quiz` con preguntas de opción múltiple y **retroalimentación por opción** (también en
  las incorrectas, explicando dónde falla el razonamiento). Registro `AUTOEVALUACIONES['id']`
  sobre un contenedor `data-quiz="id"`, análogo a `SIMULADORES`; marcador, botón de reiniciar,
  `role="group"` y `role="status"`, y KaTeX dentro de la retroalimentación.
  6 preguntas en el capítulo 2 y **6 retropropagadas al capítulo 1**.
  - *Verificado en ambos capítulos:* 6×4 opciones, exactamente una correcta por pregunta,
    marcador correcto al acertar y al fallar, botones bloqueados tras responder, reinicio
    limpio, 0 errores de KaTeX en la retroalimentación, consola sin errores y los simuladores
    previos del capítulo 1 intactos.

- [x] **T4c · Autoevaluación v2 y ejercicios guiados** (2026-07-26, a petición de Javier:
  *"la autoevaluación podría ser más interactiva y los ejercicios podrían tener
  retroalimentación"*).
  - **Cuatro tipos de pregunta** en vez de uno: `opcion` (una correcta), `multiple` (varias,
    con corrección parcial que dice cuántas acertaste y cuántas faltan), `numerica` (campo de
    entrada con tolerancia, acepta coma o punto decimal) y `grafico` (la pregunta **dibuja** un
    Chart.js y pide diagnosticarlo). Cada capítulo tiene 8 preguntas usando los cuatro tipos.
  - **Segundo intento con pista.** Al primer fallo ya no se revela la respuesta: se muestra una
    pista y se deja reintentar. Al segundo se revela y se explica. El marcador distingue
    aciertos al primer intento de aciertos al segundo, hay barra de progreso, y al terminar
    aparece un **resumen que nombra los módulos a repasar** (los de las preguntas que costaron).
  - **Ejercicios guiados** (`.ejercicio-guiado`): cada ejercicio propuesto lleva dos
    desplegables accesibles (`aria-expanded`/`aria-controls`) con una **pista** y una
    **solución comentada**. El código dentro de una solución se muestra ya desplegado (no
    obliga a un segundo clic) y se resalta con Prism al abrir.
  - **Las soluciones se calculan, no se escriben de memoria:** `precalculo/genera_soluciones.R`
    resuelve de verdad los ejercicios de los dos capítulos y deja el resultado en
    `salidas/soluciones_ejercicios.json`. Las cifras del HTML se contrastan contra esa salida.
  - *Verificado:* consola limpia y 0 errores KaTeX en los dos capítulos; los cuatro tipos
    corrigen bien incluidos los casos límite (numérica justo dentro y justo fuera de la
    tolerancia, coma decimal, entrada no numérica, múltiple parcial y múltiple sin marcar
    nada); el reintento con pista no revela la respuesta; **los gráficos de las preguntas se
    registran en `graficosActivos`** y no se acumulan tras reiniciar (2 antes, 2 después de
    tres reinicios); resumen final correcto con 8/8 y con 7/8. **Los 6 bloques R nuevos de las
    soluciones se ejecutan y devuelven exactamente las cifras citadas**; en total 18 de 19
    bloques R corren (el 19.º es solo código `fpp3`, que parsea) y los 13 de Python corren.
  - *Hallazgos de la auditoría:*
    1. Iba a dar por buena la respuesta "co2 es aditiva". **Los datos la desmienten**: la
       elasticidad amplitud–nivel da $b = 1.083$ con IC95 [0.575, 1.591] y $R^2 = 0.335$, es
       decir, **indistinguible**, porque el nivel del CO₂ solo varía un 16 % en toda la
       muestra. La solución ahora enseña eso, que es más útil, y añade el dato de que la
       amplitud sí crece (+0.024 ppm/año, p = 0.0002), lo que argumenta a favor de STL.
    2. La comparación "clásica vs. STL ante un atípico" era **injusta con STL**: la hacía sin
       `robust = TRUE`, que es justo la opción que le da resistencia. Con ella la distorsión
       cae de +3.14 % a −0.82 % frente al +4.02 % de la clásica. Que la ventaja **dependa del
       argumento** es ahora el punto del ejercicio.
    3. Tres cifras mal en el borrador, corregidas contra la salida real de R: el λ de Guerrero
       del co2 lo describí como "cerca de 1" cuando es −0.034; la varianza por $d$ del co2 la
       calculaba **sin** diferenciar estacionalmente (inservible para decidir $d$); y el rango
       relativo de `AirPassengers` lo cité como 1.7 cuando es 1.848.
    4. `ndiffs(USAccDeaths)` sobre la serie cruda devuelve **0**, y tras $\nabla_{12}$ devuelve
       **1**: la misma trampa del orden que ya documentaba el módulo 7. Está incorporada al
       enunciado y a la pista del ejercicio 3.

- [x] **T4d · Espaciado alrededor de los gráficos** (2026-07-26, Javier reportó que el texto
  bajo "El deslizador de φ" se veía amontonado). El síntoma destapó **dos bugs de fondo**:
  1. **Al capítulo 2 le faltaba un bloque entero de CSS.** En el script de ensamblado leí
     `cap2_css.txt` en una variable y **nunca la concatené**, así que el capítulo se publicó sin
     `.simulador-lectura`, `.control-selector`, `.control-interruptor` y **las 22 reglas base
     del componente `.quiz`**: la lectura numérica salía como texto corrido sin separación
     (justo lo que Javier vio), el desplegable y los interruptores sin estilo, y toda la
     autoevaluación en blanco y negro. Se insertó el bloque antes del CSS v2 y ahora los dos
     capítulos tienen exactamente el mismo conjunto de reglas.
  2. **Conflicto de cascada en la selección múltiple:** una opción marcada conservaba la clase
     `marcada`, que empata en especificidad con `correcta`/`incorrecta` y ganaba por orden de
     fuente, de modo que al corregir se veía naranja en vez de verde o roja. Se resuelve en el
     JS quitando `marcada` al pintar el estado final, en vez de depender del orden del CSS.
  - **Espaciado:** auditoría geométrica de los 84 pares de elementos consecutivos dentro de
    simuladores y preguntas de los dos capítulos. Había 0 px entre el título del simulador y su
    párrafo (7 casos) y 4 px entre una etiqueta y el lienzo que encabeza (6 casos). Los
    márgenes vivían en atributos `style` repartidos por el HTML; se sustituyeron por dos clases
    (`.simulador-intro`, `.grafico-etiqueta`) más reglas de hermano adyacente, y la lectura
    numérica se separa ahora con una línea fina. Resultado: hueco mínimo de 0 → **7 px**
    (cap. 2) y **8 px** (cap. 1), mediana 11 → 13 px, sin desbordes de canvas.
  - *Lección de método:* la verificación anterior comprobó a fondo el **DOM y el comportamiento**
    pero solo hizo comprobaciones puntuales de **estilo calculado**, y justo en el capítulo 2
    revisé únicamente las reglas nuevas. De ahí que un bloque de CSS ausente pasara. A partir de
    ahora: comparar el conjunto de selectores entre capítulos y medir la geometría real.
    Además, `getComputedStyle` justo después de un `click()` devuelve el valor **inicial** de
    una transición CSS: hay que desactivar las transiciones antes de medir colores de estado.

### Checkpoint 1
- [x] Revisión de Javier del capítulo 1 (2026-07-26): **sin cambios**; se mantienen tono,
      profundidad y densidad de fórmulas y código para los capítulos siguientes.

### Fase 2 — Capítulos 3 y 4 — ✅ COMPLETADA (2026-07-26)

**Siguiente tarea: T6.** Al retomar, arranca por aquí. Ya disponible para reutilizar, además
de lo del capítulo 2: el álgebra ARMA en JS (`pesosPsi`, `pesosPi`, `acfTeorica`,
`analizarAR`, `esInvertible`, `simularARMA`), la opción `barrasExtra` de
`crearGraficoBarras` (dos juegos de barras: teórica y muestral) y el componente
`.derivacion`. Copiar el capítulo 3 como base.

- [x] **T5 · Capítulo 3** (AR/MA/ARMA) — `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html`.
  10 módulos: (1) operador de rezago y polinomios característicos, (2) AR(p) y triángulo de
  estacionariedad, (3) MA(q) e invertibilidad, (4) dualidad AR↔MA con pesos ψ/π, (5) ARMA e
  identificación, (6) simular y reconocer procesos, (7) estimación por Yule–Walker/CSS/ML,
  (8) criterios de información y diagnóstico, (9) dos casos reales, (10) autorregresión y
  redes neuronales + cierre. **4 simuladores interactivos** (triángulo AR(2) con pseudo-periodo
  en vivo; pesos ψ/π con la divergencia al perder la invertibilidad; laboratorio ARMA con ACF/PACF
  teóricas frente a muestrales y deslizador de T; diagnóstico de residuales de 4 candidatos)
  **+ 6 paneles** con selector. 8 preguntas de autoevaluación con los 4 tipos, 3 ejercicios
  guiados, 6 cajas de derivación. Precálculo en `precalculo/genera_cap3.R` →
  `cap3_arma.json` / `cap3_datos.js`. Ensamblado por sustitución de regiones sobre el capítulo 2
  (script con aserciones, `scratchpad/ensambla_cap3.py`), **no** por concatenación de fragmentos:
  es la lección del bug de T4d.
  - *Verificado:* consola sin errores en los 10 módulos; **0 errores KaTeX** en 553 fórmulas;
    canvas creados = gráficos activos en todos los módulos (se destruyen al cambiar); los
    **12 bloques R y los 9 de Python corren de principio a fin** (el bloque 9 descarga la TRM en
    vivo y reproduce exactamente las cifras del texto: n = 137, banda 0.1675, ACF 0.105/−0.077/…,
    Ljung–Box 0.0931/0.0601/0.0599); los 4 simuladores responden en valores extremos y reproducen
    las cifras de R; autoevaluación con los 4 tipos y casos límite (numérica justo dentro y justo
    fuera de la tolerancia, coma decimal, texto, vacío), reintento con pista que **no** revela, y
    los gráficos de las preguntas no se acumulan (2 antes, 2 tras 4 reinicios); **conjunto de
    selectores CSS idéntico al de la plantilla** (218) y superconjunto del capítulo 2 sin pérdidas;
    geometría medida en 85 pares consecutivos, hueco mínimo **8 px**, sin desbordes de canvas ni
    scroll horizontal.
  - *Hallazgos de la auditoría (todos incorporados al capítulo):*
    1. **El AR(2) "de libro" de Yule sobre las manchas solares crudas no pasa el diagnóstico:**
       Ljung–Box(12) da $p = 0.0461$ y el mínimo de AICc **y** de BIC es un ARMA(2,1)
       (834.73 / 847.12 frente a 838.30 / 848.30). La causa no era falta de dinámica sino de
       **escala**: sobre $\sqrt{\text{manchas}}$ el AR(2) pasa a ser el mínimo de los dos criterios
       (324.00 / 334.00), pasa Ljung–Box ($p = 0.1644$) y su pseudo-periodo sube de 10.74 a
       **11.22 años**, que es el ciclo solar documentado. El término MA parcheaba la varianza.
       Es ahora el núcleo de los módulos 8 y 9.
    2. **R y statsmodels dan distinto $p$-valor de Ljung–Box y aquí la conclusión se invierte**
       (0.0461 frente a 0.1085 sobre el mismo ajuste: AICc y BIC coinciden hasta el último
       decimal). Comparando los residuales uno a uno, **del tercero en adelante son idénticos**;
       difieren los dos primeros por la inicialización del filtro (21.06 frente a 52.54). Descartando
       los $\max(p,q)$ primeros, los dos programas coinciden: 0.0232 y 0.0232. O sea, el rechazo
       del AR(2) es real y se **refuerza**. Documentado en el módulo 8.
    3. **El logaritmo es imposible en esta serie**: hay un año con cero manchas (1810; tres en la
       serie completa). La elasticidad amplitud–nivel da $b$ entre 0.70 y 0.82 según el tamaño de
       bloque, con IC95 que excluyen 0 —hay que transformar— pero **no separan** $\sqrt{\ }$ de
       log. Lo que decide es el cero. Y `BoxCox.lambda` avisa con datos no estrictamente positivos:
       desplazando una unidad da $\lambda = 0.3062$, con el que la conclusión no cambia
       (periodo 11.39, Ljung–Box 0.4892).
    4. **El AR(2) tiene 0 de 20 autocorrelaciones residuales fuera de la banda y aun así
       Ljung–Box lo rechaza.** Mirando el correlograma barra por barra se habría dado por bueno.
       Es el mejor argumento para la prueba conjunta y está incorporado como caja de nota.
    5. **`auto.arima` devuelve el MA(1) de la TRM sin media**, no por capricho: la media mensual
       0.2681 % tiene $t = 0.84$. Comparados en igualdad de condiciones (los dos sin media), el
       MA(1) y el ruido blanco puro se separan **una centésima** de AICc (722.653 vs 722.663):
       son indistinguibles. La conclusión honesta del caso 2 es que no hay nada que modelar.
    6. **Cifras corregidas contra la salida real de R antes de publicar** (todas estaban mal en
       el borrador): la ACF teórica del AR(2) en los rezagos 3–5; el $\hat\theta$ que devuelve
       `arima` sobre un MA(1) simulado no invertible (0.4794, no 0.5311); los **pesos $\pi$
       llevaban un signo de más** (`ARMAtoMA(ar=-θ, ma=-φ)` ya los da con su signo); la ACF del
       ARMA(1,1) (0.8308, no 0.8306); la media del modelo final sobre $\sqrt{\ }$ (6.33, no 6.99);
       el Ljung–Box sin `fitdf` (0.0996, no 0.1053); y `pacf()$acf` **se imprime como un array de
       tres dimensiones**, no como el vector que anunciaba el comentario.
    7. **Bug encontrado por la auditoría en el navegador:** el contenedor `.quiz` necesita su
       andamiaje interno (`.quiz-preguntas`, `.quiz-progreso-barra`, `.quiz-resumen`,
       `.quiz-conteo`, `.quiz-reiniciar`) o `renderAutoevaluacion()` lanza excepción. Se añadió
       como comprobación al script de ensamblado para que no vuelva a pasar.
  - *Desviaciones sobre el plan:* (a) el plan pedía **un** simulador; se hicieron 4 interactivos
    + 6 paneles (decisión de Javier). (b) Caso real = **manchas solares 1770–1869** (AR(2) de
    Yule con raíces complejas) + **log-retornos de la TRM** como contraste "casi ruido blanco",
    en vez de dejarlo sin especificar. (c) Los módulos 7 y 8 del plan original ("estimación +
    criterios" y "diagnóstico") se reorganizaron en "estimación" / "criterios + diagnóstico",
    que reparte mejor la carga y deja el módulo 9 para los casos completos. (d) El archivo pesa
    **298 KB**, por encima del límite práctico de la tabla de riesgos: mismo criterio que en el
    capítulo 2 (contenido real, y Pages sirve comprimido). (e) **No se instaló ningún paquete
    nuevo**: todo sale de R base + `tseries` + `forecast`, ya presentes.
  - *Dependencias:* T1, T2. *Tamaño:* L.

- [x] **T5b · Componente `.derivacion`** (nuevo en la plantilla, decisión de Javier).
  Caja plegable "Ver el desarrollo paso a paso" con `aria-expanded`/`aria-controls`, pasos
  numerados con marcador circular y banda de resultado. Guarda el álgebra completa sin cargar el
  texto principal. 15 reglas CSS + `iniciarDerivaciones()`.
  **6 cajas en el capítulo 3** (estacionariedad del AR(1), Yule–Walker, invertibilidad del MA(1),
  pesos ψ/π, verosimilitud exacta frente a condicional, grados de libertad de Ljung–Box) y
  **retropropagado**: la recursión de Durbin–Levinson al capítulo 2 y la construcción de
  $F_T$/$F_S$ al capítulo 1. Añadido también a la plantilla en la misma sesión, junto con la
  opción `barrasExtra` de `crearGraficoBarras`.
  - *Verificado en los cuatro archivos:* las 15 reglas CSS presentes en todos; KaTeX renderizado
    **antes** del primer clic (`loadModule` pasa por el módulo entero, incluidos los paneles
    ocultos); apertura y cierre correctos con cambio de texto del botón; 0 errores KaTeX dentro
    de los paneles; capítulos 1 y 2 sin errores de consola y con sus simuladores previos intactos
    tras el injerto; `barrasExtra` probado en la plantilla (3 datasets en el orden bar/bar/line).
    El capítulo 1 no recibe `barrasExtra` porque nunca tuvo `crearGraficoBarras`: no dibuja
    correlogramas.

- [x] **T6 · Capítulo 4** (ARIMA y Box–Jenkins) — `Htmls_Series/capitulo-4-modelos-arima.html`.
  10 módulos: (1) de ARMA a ARIMA, (2) la metodología Box–Jenkins, (3) elegir $d$, (4) identificar
  $p$ y $q$, (5) la constante: media y deriva, (6) estimar y comparar (el explorador), (7) dentro de
  `auto.arima`, (8) diagnóstico y errores comunes, (9) pronóstico: forma e intervalos, (10) caso TRM,
  puente al cap. 5 y cierre. **10 simuladores interactivos**, 8 preguntas de autoevaluación con los
  4 tipos, 3 ejercicios guiados, 3 cajas de derivación y el nuevo componente `.ciclo`. Precálculo en
  `precalculo/genera_cap4.R` → `cap4_arima.json` / `cap4_datos.js`. Ensamblado por sustitución de
  regiones sobre el capítulo 3 (`ensamblado/ensambla_cap4.py`, con aserciones).
  - *Verificado:* consola sin errores ni avisos en los 10 módulos; **0 errores KaTeX** en 656 fórmulas;
    canvas = `graficosActivos` en todos (19 gráficos, creados y destruidos al cambiar de módulo);
    los **12 bloques R parsean y corren**, y **177 de 179 cifras anunciadas en sus comentarios `#>`
    aparecen en la salida real** (las 2 restantes son umbrales en prosa, 0.05 y 0.01); los **9 bloques
    de Python corren** y **52 de 53 cifras propias verificadas** (la restante es un coeficiente citado
    en prosa); los simuladores reproducen las cifras de R en valores extremos (varianzas
    28 637.95 / 28 268.34 / 80 055.01, ACF(1) 0.4984 / −0.4020 / −0.6264, $\sigma_1 = \sigma = 142.045$,
    $\sigma_2 = 151.967$); autoevaluación con los 4 tipos y casos límite (numérica justo dentro y justo
    fuera de la tolerancia, coma decimal, texto, vacío; múltiple parcial; el reintento **no** revela la
    respuesta) y **sin acumulación de gráficos** tras 4 reinicios; **conjunto de selectores CSS idéntico**
    al de la plantilla y a los capítulos 2 y 3 (241); geometría medida en 71 pares consecutivos con
    hueco mínimo **8 px** y mediana 16 px, sin desbordes de canvas ni scroll horizontal.
  - *Hallazgos de la auditoría (todos incorporados al capítulo):*
    1. **KPSS confunde un cambio de nivel con una raíz unitaria, y eso explica el caso del Nilo entero.**
       Monte Carlo de 1000 réplicas de ruido blanco *estacionario por construcción*: sin escalón, KPSS
       rechaza el **4.8 %** (su tamaño nominal); con el escalón real de 1899 ($\delta = -247.8$, que son
       1.95 desviaciones típicas), el **100 %**, y `ndiffs` pide diferenciar en el 100 % de las réplicas.
       El ADF solo se deja engañar en el 0.5 %. Eso explica que sobre el Nilo `ndiffs` dé **1 con KPSS
       pero 0 con ADF y con PP** — y como `auto.arima` elige $d$ con KPSS, diferencia. Se añadió al
       precálculo una malla de 400 réplicas × 9 valores de $\delta$ para el simulador del módulo 3.
    2. **La sobrediferenciación tiene firma algebraica, no solo estadística:** $\hat\theta \to -1$ y una
       raíz MA **exactamente sobre el círculo unitario**. En la rejilla del Nilo, **4 de los 9 modelos con
       $d = 2$** la tienen, incluido el mejor por BIC de ese grupo. Y el mínimo de AICc de la rejilla de la
       **TRM** es un ARIMA(2,1,2) con las dos raíces MA en 1.000 y las AR en 1.0042: gana por 2.56 puntos
       y hay que descartarlo — que es justo lo que hace `auto.arima`.
    3. **Descubierto al ejecutar el código del módulo 1:** con los coeficientes reales del Nilo, integrar
       la serie **no** dispara la varianza (razón 1.006), mientras que sin el término MA la multiplica por
       32.8. La causa es que $\theta = -0.874$ hace que $(1+\theta B) \approx (1-B)$ y cancele la
       integración. Es el mismo hilo que el hallazgo 1: el modelo está deshaciendo una diferencia que
       probablemente no hacía falta. Se convirtió en el hilo conductor del capítulo (se plantea en el
       módulo 1, se explica en el 3 y se cierra en el 8).
    4. **Error conceptual mío, corregido:** etiqueté $\sigma\sqrt{h}$ como "lo que valdría si los errores
       fueran independientes". Es falso: $\sigma\sqrt{h}$ es exactamente lo que da una **caminata
       aleatoria** (en un ARIMA(0,1,0) todos los $\psi_j$ valen 1, comprobado con error 4.5e-13). Con la
       lectura correcta el dato se vuelve útil: el Nilo tiene $\psi_\infty = 0.169$ y su incertidumbre
       crece **4 veces menos** que la de una caminata, mientras que `BJsales` tiene $\psi_\infty = 2.99$ y
       crece **al doble**. Está ahora como caja de nota en el módulo 9 y en la discusión del ejercicio 3.
    5. **El pronóstico con $d = 2$ es una recta, no una parábola** (segundas diferencias nulas, medidas).
       `forecast::Arima` **se niega** a ajustar la deriva con $d \ge 2$ (avisa y la descarta) y
       `statsmodels` lanza un `ValueError` porque un término de orden menor que $d$ lo elimina la propia
       diferenciación. Lo habría escrito como "parábola" de memoria.
    6. **Trampa nueva R↔Python: el truncamiento de KPSS no es el mismo.** `tseries::kpss.test` usa
       $\lfloor 4(n/100)^{1/4}\rfloor = 4$ y `statsmodels.kpss` con `nlags="legacy"` usa 12, así que sobre
       el Nilo dan 0.9654 y 0.5497. Con `nlags=4` coinciden hasta el último decimal. Documentado como caja
       de advertencia en el módulo 3.
    7. **`statsmodels` reporta `nobs = 100` para todo $d$**: no descuenta las diferencias, así que sus
       AIC/BIC *parecen* comparables entre distintos $d$ cuando no lo son. En R el $n$ efectivo baja
       (100, 99, 98) y el problema salta a la vista. Documentado en el bloque Python del módulo 6.
    8. **Los dos ejercicios salieron mejores de lo diseñado, pero por razones distintas a las previstas.**
       En `BJsales`, el "IMA(1,1) de libro" **no pasa el diagnóstico** (Ljung–Box $p = 0.0340$, ACF residual
       $r_2 = 0.248$): gana el ARIMA(1,1,1). Y en `log(lynx)` **la regla de la varianza falla**: diferenciar
       la reduce un 58 %, así que no dispara ninguna alarma; lo que sí detecta el exceso es la raíz MA en
       1.000 del ARIMA(2,1,1). Los enunciados y las soluciones se reescribieron contra estos hechos.
    9. **Cifras corregidas contra la salida real antes de publicar** (todas estaban mal en el borrador):
       en R, el Ljung–Box del módulo 2 (0.7997371), el pronóstico a 3 pasos (816.18 / 835.56 / 840.49, no
       833.67 / 838.12), el $p$ del ADF (0.06419542), el estadístico KPSS (0.9654349), el número de líneas
       de la traza (20 y 44), el Shapiro de `BJsales` (0.6294597), el pseudo-periodo del lince (9.7839) y la
       banda de los residuales de `BJsales` (**0.1600**, no 0.1606: `residuals()` devuelve $n$ valores y no
       $n-d$). En Python, **cuatro bloques enteros** en los que había escrito la salida de R como si fuera la
       de Python: la razón de varianzas (1.363 / 56.7), los $\theta$ y raíces de la sobrediferenciación
       (−0.9988 / 1.0012, no −1.0000 / 1.0000), el error estándar del escalón (27.77, no 28.15) y todo el
       bloque de intervalos ($\sigma = 140.599$, no 142.045).
    10. **Bug propio en el JS, encontrado en el navegador:** mis simuladores destruyen y recrean sus
       gráficos al repintar, y devolvían funciones donde `destruirSimuladores()` espera objetos con
       `.destroy()`. Los 10 módulos lanzaban excepción. Se añadió el ayudante `manejador()`, que devuelve
       un objeto estable que destruye el gráfico **vigente**.
    11. **`jsonlite` escribe los `Inf` como `null`**, y `Number(null)` es 0: el primer paso de la traza de
       `auto.arima` mostraba "mejor AICc = 0.000". `fmt()` es ahora defensiva y devuelve un guion.
    12. **Hueco de 0 px entre el título del quiz y su párrafo**, heredado de los capítulos 2 y 3 y de la
       plantilla (el `h4` no tiene margen inferior y Tailwind pone los `<p>` a cero). Es la misma clase de
       fallo que encontró la auditoría de T4d en los simuladores. Se añadió `.quiz > h4 + p` a los
       **cinco archivos** y el hueco pasó de 0 a 10 px en todos.
  - *Trampa de método (nueva, anotar):* el contexto de JavaScript del navegador de esta herramienta puede
    reportar `innerWidth = 0`, con lo que se activa la media query móvil y **toda medición de geometría
    sale falsa** (llegué a "detectar" un bug de alturas desiguales que no existía). Antes de medir hay que
    llamar a `resize_window` y **comprobar que `innerWidth > 1024`**. Además, los `await` con `setTimeout`
    se congelan cuando el panel está oculto: las comprobaciones de simuladores hay que hacerlas síncronas.
  - *Desviaciones sobre el plan:* (a) el plan pedía 8 módulos y un simulador; se hicieron **10 módulos y
    10 simuladores** (decisión de Javier sobre densidad, ya vigente desde el cap. 3). (b) Javier pidió
    incluir **también los intervalos de pronóstico**, por encima de la recomendación: el capítulo 4 los
    **construye** desde los pesos $\psi$ (comprobación contra `forecast()` con error 9.1e-11) y el
    **capítulo 6 los evaluará** (cobertura real frente a nominal, backtesting) — **T8 no debe duplicar la
    construcción**. (c) Caso de estudio = **Nilo** (recorrido completo) + **TRM en niveles** (resultado
    honesto: caminata aleatoria) + **panel puente** con `log(AirPassengers)`, en vez de solo el Nilo.
    (d) La rejilla de la Fase 0 se **recalculó** y coincide con la anterior con diferencia máxima de AICc
    de 0.0000 en los 27 modelos, con los mismos mejores por $d$ (101, 111, 122). (e) El archivo pesa
    **325 KB**, por encima del límite de la tabla de riesgos: mismo criterio que en los caps. 2 y 3.
    (f) **No se instaló ningún paquete nuevo.** El bloque de `pmdarima` del módulo 7 se reescribió para que
    lo ejecutable (rejilla con statsmodels) vaya primero y la alternativa con dependencia extra quede
    marcada como no ejecutada, en vez de anunciar una salida sin verificar.
  - *Dependencias:* T2, T5. *Tamaño:* L.

- [x] **T6b · Componente `.ciclo`** (nuevo en la plantilla, decisión de Javier).
  Diagrama de etapas recorrible con semántica de pestañas (`role="tablist"`/`tab`/`tabpanel`), navegable
  con las flechas del teclado y con vuelta al principio al llegar al final. Cada etapa despliega **qué
  haces**, **con qué función** y **qué te devuelve atrás**, que es la dimensión que una lista numerada no
  sabe dibujar. 22 reglas CSS + `iniciarCiclos()`, en la familia de color naranja para distinguirlo de las
  cajas verdes de derivación. Fuentes compartidas en `ensamblado/componentes/` (`ciclo.css`, `ciclo.js`,
  `ciclo_html.py`) para que las cinco instancias tengan exactamente la misma estructura.
  - **Instancias:** ciclo de Box–Jenkins de 4 etapas en el capítulo 4; y **retropropagado**: pipeline de
    preprocesamiento de 6 pasos en el cap. 2 (**sustituye** a la caja `.diagram` con la lista, que decía lo
    mismo sin las vueltas atrás), flujo de descomposición de 4 pasos en el cap. 1, protocolo de
    identificación ARMA de 4 pasos en el cap. 3, y una demostración de 3 etapas en la plantilla —añadida en
    la misma sesión, como exige la regla del Checkpoint 0.
  - *Verificado en los cinco archivos:* las 22 reglas CSS presentes en todos; clic y flechas del teclado
    (incluida la vuelta circular) conmutan `aria-selected`, `tabIndex` y la visibilidad de los paneles;
    KaTeX renderizado **antes** del primer clic, también en los paneles ocultos; 0 errores de consola y de
    KaTeX en los cuatro capítulos tras el injerto, con sus simuladores y autoevaluaciones previos intactos;
    los cuatro botones del ciclo del cap. 4 miden 75 px de alto en una sola fila (medido con viewport real).
  - *Nota de homogeneidad pendiente:* el capítulo 1 sigue sin `crearSelector` ni `crearInterruptores` (10
    selectores CSS menos que los demás) porque ninguno de sus simuladores usa esos controles. Es anterior a
    esta sesión y no afecta a lo que se ve; si un futuro simulador del cap. 1 los necesita, hay que
    injertarlos entonces.

### Fase 3 — Capítulos 5 y 6

### Fase 3 — ✅ COMPLETADA (2026-07-27)

**Siguiente tarea: Checkpoint 2 y luego T9.** Los seis capítulos están terminados y verificados. Al
retomar, lo que queda es la revisión de contenido de Javier (Checkpoint 2), la portada `index.html`
(T9) y la publicación (T10). Disponible para reutilizar, además de todo lo anterior: el componente
**`.tabla-ranking`**, el verificador de bloques de código `precalculo/verifica_bloques_cap6.py`
—que sirve para cualquier capítulo pasándole `--html`— y, en el precálculo, el motor de origen móvil
(`origen_movil` / `resume_om`), las métricas implementadas a mano y el puntaje de Winkler.

- [x] **T7 · Capítulo 5** (SARIMA) — `Htmls_Series/capitulo-5-sarima.html`.
  11 módulos: (1) la firma de la estacionalidad, (2) notación SARIMA y polinomio multiplicativo,
  (3) diferenciación estacional y el orden en que se decide, (4) identificar $(P,Q)$ y los rezagos
  satélite, (5) el modelo *airline*, (6) estimar, comparar y diagnosticar, (7) caso completo
  `log(AirPassengers)`, (8) segundo caso `USAccDeaths` y contraejemplo TRM, (9) regresores de calendario
  y SARIMAX, (10) cuando $m$ es grande: Fourier y STL, (11) panorama comparativo y cierre.
  **12 simuladores interactivos**, 8 preguntas de autoevaluación con los 4 tipos, 3 ejercicios guiados,
  3 cajas de derivación, una instancia del `.ciclo` de 5 etapas y el componente nuevo
  `.mapa-estacional`. Precálculo en `precalculo/genera_cap5.R` → `cap5_sarima.json` / `cap5_datos.js`;
  verificación cruzada en `precalculo/verifica_cap5_python.py`. Ensamblado por sustitución de regiones
  sobre el capítulo 4 (`ensamblado/ensambla_cap5.py`), que además **instala el componente nuevo** en la
  región compartida (CSS, JS y la llamada de `loadModule`).
  - *Verificado:* consola sin errores ni avisos en los 11 módulos; **0 errores KaTeX en 960 fórmulas**;
    canvas = `graficosActivos` en todos (16 gráficos, creados y destruidos al cambiar de módulo); los
    **12 bloques de R y los 9 de Python se ejecutan de principio a fin** y **454 de 456 cifras anunciadas
    en los comentarios `#>` de R y 155 de 160 de Python aparecen en la salida real** (las 7 restantes son
    prosa: porcentajes, un valor crítico comprobado aparte y una cifra de R citada dentro de un comentario
    de Python); los 12 simuladores responden en valores extremos y reproducen las cifras de R (ACF teórica
    del AR(1)×SAR(1) 0.6016/0.4230/0.7011/0.4218 idéntica a `ARMAacf`; varianzas de la sobrediferenciación
    0.011354 / 0.002102 / 0.005960; $\hat\rho_{12}$ de ∇TRM = −0.0025); autoevaluación con los 4 tipos y
    casos límite (numérica justo dentro y justo fuera de la tolerancia, coma decimal, texto, vacío;
    múltiple parcial —"te falta 1"— y sin marcar nada; el reintento muestra la pista y **no** revela la
    respuesta) y **sin acumulación de gráficos** tras 4 reinicios; el `.ciclo` navega con las flechas y da
    la vuelta; **conjunto de selectores CSS idéntico al de la plantilla (259 = 259, cero diferencias)** y
    superconjunto exacto de los capítulos 2–4 (+12, los del componente nuevo); geometría medida en 71
    pares consecutivos con hueco mínimo **8 px**, mediana 16 px, sin desbordes de canvas ni scroll
    horizontal. `ensambla_cap5.py` es reejecutable y reproduce el archivo **byte a byte**.
  - *Hallazgos de la auditoría (todos incorporados al capítulo):*
    1. **La comparativa sobre una sola partición corona al método equivocado, y medirlo se volvió el cierre
       del capítulo.** Sobre los últimos 24 meses el SARIMA *airline* queda **cuarto** (RMSE 43.18) detrás
       del ETS sobre logaritmos (19.43) y de la regresión armónica $K=6$ (19.51). Repitiendo la misma
       comparación sobre **61 orígenes** con $h = 12$, el orden **se invierte**: el SARIMA es primero
       (RMSE medio 16.81) frente a 21.42 (ETS), 21.85 (STL), 22.39 (armónica) y 41.24 (naïve), y le gana a
       cada rival en más del 85 % de los orígenes. Es el mejor puente posible hacia el capítulo 6, y está
       en el módulo 11 como advertencia, sin desarrollar el método (que es contenido del 6).
    2. **El AICc tampoco compara entre distintos $D$, y con la estacional el error es mayor**: cada $D$
       cuesta $m$ observaciones, no una. Los modelos armónicos ($D=0$) se evalúan sobre 143 observaciones
       y el *airline* ($D=1$) sobre 131, así que poner sus AICc en la misma tabla (−521.22 frente a
       −483.21) es exactamente el error del capítulo 4 con otra letra. La rejilla del módulo 6 fija
       $d=1$ y $D=1$ en los 36 modelos, y el aviso viaja en el propio JSON para que el texto no lo olvide.
    3. **Escribí una comparativa con el ETS ajustado sobre logaritmos y ganaba por goleada (RMSE 19.43
       frente a 72.55 sobre la serie cruda).** Ajustado sobre los logaritmos, `ets()` elige ETS(M,A,M);
       sobre la serie cruda elige ETS(M,A<sub>d</sub>,M), con tendencia **amortiguada**, y a 24 meses eso
       cuesta un factor de 3.7 en RMSE. La comparativa final ajusta cada método como se usaría de verdad y
       reporta **las dos variantes del ETS**, porque la elección de escala es el hallazgo.
    4. **`nsdiffs()` cambió de prueba por defecto.** Desde `forecast` 8.x usa `test = "seas"` (fuerza
       estacional de STL); antes usaba OCSB, que todavía se puede pedir. Sobre `log(AirPassengers)` y
       `USAccDeaths` dan **1 y 0** respectivamente. Documentado como caja de advertencia en el módulo 3 y
       en la solución del ejercicio 2.
    5. **`statsmodels` no diferencia la serie: mete $d$ y $D$ en el espacio de estados con un prior
       difuso.** Consecuencias medidas: informa `nobs = 144` para todos los modelos (el mismo problema que
       el capítulo 4 documentó con $d$, ahora sin arreglo aparente) y, en series cortas, mueve los
       coeficientes — sobre `USAccDeaths` ($n = 72$) $\hat\theta$ pasa de −0.4303 a −0.3924, y **no es
       falta de convergencia**: Python alcanza ese óptimo desde varios inicios y con varios optimizadores.
       **`simple_differencing=True` lo arregla** y las dos salidas coinciden al cuarto decimal. Pero
       entonces `get_forecast()` devuelve el pronóstico de la serie **diferenciada** (0.0 en vez de 6.2643):
       la opción sirve para estimar como R, no para pronosticar. Las dos mitades están documentadas.
    6. **Los operadores conmutan; las pruebas no.** $\nabla\nabla_{12}y$ es idéntica en cualquier orden
       (diferencia máxima medida: 0), pero `ndiffs(USAccDeaths)` da **0** en la serie cruda y **1** tras
       $\nabla_{12}$. En Python lo mismo: KPSS sobre $\nabla_{12}y$ da 0.8672 (rechaza) y sobre
       $\nabla\nabla_{12}y$ baja a 0.0713. Es el núcleo del módulo 3 y del ejercicio 2.
    7. **Los regresores de calendario funcionan y el coeficiente dice algo bonito.** Añadir
       $\log(\text{días del mes})$ y la Semana Santa (algoritmo de Meeus) al *airline* baja el AICc de
       −483.21 a −490.72, con $\hat\beta_{\log(\text{días})} = 1.084$ (e.e. 0.446): el contraste de
       $\beta = 1$ da $t = 0.188$, **no se rechaza**, que es justo lo que predice la aritmética del
       calendario. Y aun así el modelo con calendario **empeora** fuera de muestra (RMSE 45.48 frente a
       43.18): mejorar el AICc no es mejorar el pronóstico, y está como caja de advertencia.
    8. **Bug de codificación en toda la cadena de precálculos, encontrado en el navegador.** R arranca con
       `LC_CTYPE = "C"`, así que `jsonlite` escribe las tildes como `<c3><ad>`; el navegador las lee como
       marcado desconocido y **se come la letra** ("log(das del mes)"). Los capítulos 3 y 4 arrastran el
       mismo defecto en 2 y 9 campos, pero **ninguno de ellos se renderiza** (son `descripcion`, `fuente`,
       `nota`); en el 5 sí, porque muestra nombres de modelo. Se añadió `Sys.setlocale("LC_CTYPE",
       "en_US.UTF-8")` con aviso a los **seis** scripts generadores y se regeneraron `cap5_sarima.json` y
       `soluciones_ejercicios.json`. Quedan 4 apariciones en el capítulo 5, todas heredadas de
       `datos_series.json` y en campos que no se muestran: se limpiarán cuando T8 regenere ese archivo.
    9. **Hueco de 0 px entre la lectura numérica y el gráfico** en los simuladores de los módulos 9 y 11,
       porque `.simulador-lectura` se diseñó para ir al final y no lleva margen inferior. Misma clase de
       fallo que encontró la auditoría de T4d. Se añadió la regla `.simulador-lectura + .grafico-wrapper`
       (y su variante con `.grafico-etiqueta`) a los **seis archivos**, y el hueco mínimo pasó de 0 a 8 px.
    10. **Cifras corregidas contra la salida real antes de publicar:** el polinomio AR de los pesos $\psi$
       lo escribí con el signo cambiado (daba $\sigma_{24} = 2.34$ en vez de 0.1396); la banda del módulo 7
       la calculaba sobre $n = 144$ cuando la ACF es de la serie diferenciada ($n = 131$, banda 0.1712 y no
       0.1633); el Ljung–Box del mejor modelo de co2 es 0.631 y yo había puesto el 0.4081 del *airline*;
       los índices de fila del `data.frame` ordenado; la tabla mes × año del bloque de Python del módulo 1;
       los seis AIC de la regresión armónica en Python y el del STL, que estaban **inventados** (los reales
       son −306.95 … −501.62 y −643.05); y el $t$ de los regresores de calendario en Python.
    11. **`fourier()` de R y `Fourier` de `statsmodels` no dan lo mismo con $K = m/2$:** R emite 11
       columnas y Python 12, y la de más es el seno de frecuencia $m/2$, **idénticamente cero**. La matriz
       de diseño de Python queda con rango 11 y una columna sobra; hay que quitarla a mano. Documentado en
       el bloque de Python del módulo 10.
    12. **El simulador del módulo 1 aplicaba el logaritmo siempre**, así que la TRM diferenciada daba
       $\hat\rho_{12} = 0.0100$ y no el −0.0025 de la tabla del texto. Se separó el logaritmo en su propio
       interruptor; ahora la lectura del simulador reproduce **exactamente** la última fila de la tabla.
  - *Desviaciones sobre el plan:* (a) el plan pedía 8 módulos y un simulador; se hicieron **11 módulos y
    12 simuladores**, con el alcance ampliado que eligió Javier: regresión armónica y STL para $m$ grande,
    SARIMAX con regresores de calendario, y comparación con ETS/Holt–Winters. (b) **La TRM pasó de caso de
    estudio a contraejemplo**, porque los datos lo exigen: `nsdiffs(trm) = 0` con las dos pruebas y la ACF
    de $\nabla$TRM en 12/24/36 vale −0.0025 / −0.0672 / 0.0714 frente a una banda de 0.1675. El plan la
    proponía como caso SARIMA; enseñar a **descartar** la estacionalidad resultó más útil. (c) Casos de
    estudio: `log(AirPassengers)` (recorrido completo) + `USAccDeaths` (segundo caso con la trampa del
    orden) + `co2` (ejercicios) + TRM (contraejemplo); ninguna descarga nueva. (d) El módulo comparativo
    trae cifras reales **solo de lo instalado** (snaive, ETS, armónica, STL, SARIMA); Prophet, RNN/LSTM y
    Transformers van con criterios de elección y sin números inventados, y el capítulo lo dice
    explícitamente. (e) El archivo pesa **378 KB**, por encima del límite de la tabla de riesgos: mismo
    criterio que en los capítulos 2, 3 y 4. (f) **No se instaló ningún paquete nuevo** (`uroot` no está, así
    que `nsdiffs(test="ch")` no se usa; `pmdarima` tampoco).
  - **Frontera con el capítulo 6 (acordada al empezar T7):** el capítulo 5 **pronostica** con SARIMA y
    enseña la forma escalonada del abanico, y compara métodos sobre **una sola partición fija** para
    mostrar que eso no basta. El capítulo 6 **no debe repetir** la construcción del intervalo (capítulo 4)
    ni la comparación de métodos de una partición: le toca el **método** —origen móvil, cobertura empírica
    frente a la nominal, métricas y su interpretación—. Las cifras de los 61 orígenes ya calculadas están
    en `cap5_sarima.json` (`airpassengers.comparativa.origen_movil`) y se citan en el módulo 11 como
    advertencia, no como contenido.
  - *Dependencias:* T2, T6. *Tamaño:* L.

- [x] **T7b · Componente `.mapa-estacional`** (nuevo en la plantilla, decisión de Javier).
  Mapa de calor mes × año en rejilla CSS, **sin dependencias nuevas**: los años en las filas y los meses en
  las columnas, de modo que un mes sistemáticamente alto dibuja una banda vertical y la diferencia
  estacional la borra ante los ojos. Escala secuencial (verde) para niveles y divergente (naranja ↔ verde)
  centrada en cero para series ya diferenciadas; los huecos que dejan las diferencias van con trama, no en
  blanco. El valor va **escrito dentro de la celda** y repetido en su nombre accesible, así que el color
  nunca es el único canal; con más de 20 filas se omite el número y queda solo en el `aria-label`.
  Semántica de tabla (`role="table"/"rowheader"/"columnheader"/"cell"`). 13 reglas CSS +
  `pintarMapaEstacional()` + `matrizMesAnio()` + `iniciarMapasEstacionales()`, con fuentes compartidas en
  `ensamblado/componentes/` (`mapa_estacional.css`, `.js`, `_html.py`) para que las tres instancias tengan
  marcado idéntico. El registro `MAPAS_ESTACIONALES['id']` admite **una función**, de modo que un simulador
  puede repintarlo y una instancia estática puede leer datos definidos más abajo en el archivo.
  - **Instancias:** simulador "mapa y correlograma en paralelo" del capítulo 5 (4 series × 4
    diferenciaciones × logaritmo sí/no); y **retropropagado** (`ensamblado/retropropaga_mapa.py`):
    `AirPassengers` mes × año en el módulo 3 del capítulo 1 —el de visualización estacional— y una
    demostración con serie sintética de semilla fija en la plantilla, en la misma sesión, como exige la
    regla del Checkpoint 0. Los capítulos 2, 3 y 4 **no** lo reciben: ninguno trata la estacionalidad.
  - *Verificado en los tres archivos:* las 13 reglas CSS presentes; consola y KaTeX sin errores; los
    simuladores y autoevaluaciones previos intactos; 144 celdas en el capítulo 1, 96 en la plantilla y
    132 con 1 hueco en la vista diferenciada del capítulo 5; hueco mínimo 8 px (7 px en el capítulo 1 y en
    la plantilla, que usan `font-size` raíz de 14 px en vez de 16: es el mismo `0.5rem`); y el conjunto de
    selectores del capítulo 5 **idéntico** al de la plantilla.

- [x] **T8 · Capítulo 6** (pronóstico y evaluación) — `Htmls_Series/capitulo-6-pronostico-evaluacion.html`.
  12 módulos: (1) residual frente a error de pronóstico, (2) los métodos de referencia, (3) RMSE y MAE,
  (4) MAPE y sMAPE, (5) MASE y RMSSE, (6) partición temporal y fuga de información, (7) validación de
  origen móvil, (8) backtesting y Diebold–Mariano, (9) cobertura y puntaje de Winkler, (10) tres casos
  con tres desenlaces, (11) taller de auditoría de un análisis asistido por IA, (12) el proyecto y cierre
  del curso. **14 simuladores interactivos**, 8 preguntas de autoevaluación con los 4 tipos, un segundo
  `.quiz` para el taller, 3 ejercicios guiados, 1 caja de derivación, una instancia del `.ciclo` de 5
  etapas y el componente nuevo `.tabla-ranking` (dos instancias). Precálculo en `precalculo/genera_cap6.R`
  → `cap6_evaluacion.json` / `cap6_datos.js`; soluciones en `genera_soluciones.R`; verificación de bloques
  en `precalculo/verifica_bloques_cap6.py`. Ensamblado por sustitución de regiones sobre el capítulo 5
  (`ensamblado/ensambla_cap6.py`), que además **instala el componente nuevo** en la región compartida.
  - **Fronteras respetadas:** el capítulo 4 construye el intervalo desde los pesos $\psi$ y el capítulo 5
    compara métodos sobre una sola partición. El 6 no repite ninguna de las dos cosas: la partición única
    solo define los métodos de referencia (contenido nuevo), y el intervalo se **evalúa**, no se construye.
  - *Verificado:* consola sin errores ni avisos en los 12 módulos; **0 errores KaTeX en 629 fórmulas**;
    canvas = `graficosActivos` en todos (17 gráficos, creados y destruidos al cambiar de módulo); los
    **14 bloques de R y los 11 de Python se ejecutan ENCADENADOS y las 390 cifras anunciadas en sus
    comentarios `#>` aparecen en la salida real** (390 de 390, comprobado por script); las métricas
    implementadas a mano coinciden con `forecast::accuracy` con **diferencia 0**; el RMSE medio de los
    orígenes reconcilia **exactamente** con las cuatro cifras que publicó el capítulo 5 (snaive 41.238,
    sarima 16.812, ets 21.416, stl 21.848; diferencia máxima 0.0003, que es su redondeo); los 14
    simuladores responden en valores extremos y reproducen las cifras de R; las dos tablas de ranking
    reordenan con `aria-sort`, anuncian en `role="status"` y marcan el mejor valor; autoevaluación con los
    4 tipos y casos límite (numérica justo dentro y justo fuera de la tolerancia, coma decimal, texto,
    vacío; múltiple parcial —"de las 3 que marcaste, 3 están en la respuesta y te faltan 3"—; el reintento
    **no** revela) y **sin acumulación de gráficos** tras 8 reinicios; el `.ciclo` navega con las flechas y
    da la vuelta en los dos sentidos; **conjunto de selectores CSS idéntico al de la plantilla (224 = 224,
    cero diferencias)**; geometría medida en 74 pares consecutivos con hueco mínimo **8 px**, mediana 16 px,
    sin desbordes ni scroll horizontal. `ensambla_cap6.py` es reejecutable y reproduce el archivo
    **byte a byte**.
  - *Hallazgos de la auditoría (todos incorporados al capítulo):*
    1. **`accuracy()` cambia la definición del MASE según la CLASE del conjunto de prueba.** Decide la
       escala con `frequency(x)`: con un `ts` mensual usa el naïve estacional ($Q = 28.5741$) y devuelve
       $2.4935$; con el **mismo vector** pasado por `as.numeric()`, `frequency` vale 1, usa el naïve simple
       ($Q = 22.1597$) y devuelve $3.2153$. Un **28.9 %** de diferencia sin ningún aviso. Es ahora caja de
       advertencia del módulo 5 y uno de los seis fallos del taller del módulo 11.
    2. **La afirmación de manual sobre la validación cruzada aleatoria es falsa tal cual se enuncia.** Medida
       sobre cinco montajes, el $k$-fold aleatorio **no** sobrestima el desempeño con una regresión sobre
       rezagos (optimismo **−21.8 %**); sí lo hace, y mucho, cuando el modelo **interpola en el tiempo**:
       $+40.0$ % con 1 vecino, $+58.0$ % con 3, $+37.0$ % con tendencia e indicadoras de mes y $+99.0$ %
       con un polinomio de grado 8 ($0.1351$ prometido frente a $12.8984$ real, un factor de 95). El módulo 6
       enseña la versión medida, que es más útil que el eslogan.
    3. **`tsCV` tiene dos trampas y ninguna avisa.** (a) Su matriz de errores es **desbalanceada**: la columna
       $h=1$ tiene 72 errores y la $h=12$ solo 61, así que `sqrt(colMeans(e^2, na.rm=TRUE))` compara
       horizontes sobre muestras distintas. (b) `initial` y `window` **no empiezan en el mismo sitio**:
       `initial = 72` hace que el primer origen sea el 73 y `window = 72` que sea el 72. Con `initial = 71` y
       filtrando las filas completas, `tsCV` reproduce exactamente el 18.9154 del capítulo; sin filtrar da
       18.7452 y con `initial = 72`, 18.9422.
    4. **El sesgo destruye el intervalo estrecho antes que el ancho, y se puede medir.** El naïve estacional
       cubre solo el **46.0 %** al nivel nominal del 80 % y un correcto **93.4 %** al 95 %: su sesgo relativo
       $\bar e/\text{RMSE}$ es $0.909$, así que la banda de $\pm1.28\sigma$ se queda del lado equivocado y la
       de $\pm1.96\sigma$ todavía alcanza. **Comprobar solo el 95 % habría dado por bueno ese intervalo.**
    5. **El mejor pronosticando es el peor calibrado, y aun así gana en Winkler.** El SARIMA es primero en
       las cinco métricas puntuales y sus intervalos cubren el 98.4 % cuando prometen el 95 % (quinto puesto
       por cobertura); por Winkler vuelve a ser primero (104.1), porque el puntaje paga el ancho una vez y el
       fallo cuarenta veces. Cobertura y Winkler dan ganadores distintos y las dos preguntas son legítimas.
    6. **`auto.arima` es el mismo modelo con otro nombre, y cuesta 270 veces más.** No hay diferencia
       significativa con el *airline* a ningún horizonte ($p = 0.9662$, $0.4245$, $0.2744$), el SARIMA solo le
       gana en el **45.9 %** de los orígenes —menos de la mitad—, y tarda 118.61 s frente a 0.44 s.
    7. **A $h = 12$ el SARIMA deja de ganar.** No se distingue del naïve estacional ($p = 0.0600$), ni del STL
       ($p = 0.1039$), ni de la deriva ($p = 0.7241$, cuyo RMSE a ese horizonte es incluso menor), y
       **pierde** contra el ETS ($\text{DM} = 3.5558$, $p = 0.0007$). El agregado dice otra cosa.
    8. **El Nilo invierte el veredicto y eso corrige la lectura del capítulo 4.** Con la partición de aquel
       capítulo la **deriva** es primera (122.28), por delante del naïve (123.06) y del ARIMA(1,1,1) (125.05);
       sobre 36 orígenes la deriva pasa a ser **última** (161.27) y gana el ARIMA (121.37). El capítulo 4 no
       tiene ningún error de cálculo: el error habría sido decidir con 20 observaciones de un solo tramo.
    9. **`USAccDeaths` da la misma lección en el ejercicio 1, y más fuerte.** La partición única corona al
       *airline* (288.83) y el origen móvil corona al naïve estacional (331.33 frente a 434.92); Diebold–Mariano
       dice además que la diferencia no es significativa a ningún horizonte ($p$ entre 0.22 y 0.95). Con seis
       años de datos, dos parámetros no pagan su costo.
    10. **El MAPE no se puede leer en términos absolutos entre series (ejercicio 2).** Sobre `co2`, el método
       de la media saca un MAPE de $7.60\,\%$ —mejor que el $15.52\,\%$ del naïve estacional sobre
       AirPassengers— y su MASE es $21.99$: veintidós veces peor que la referencia. La causa es que el co2
       solo varía un $17.13\,\%$ en toda la serie.
    11. **Los intervalos del Nilo se pasan en los cinco niveles y no es culpa de la normalidad (ejercicio 3).**
       Shapiro da $p = 0.7312$ y aun así el 50 % nominal cubre el 63.9 % (ARIMA) y el 79.4 % (naïve). El
       problema es el ancho, y **solo se ve mirando el nivel del 50 %**: al 95 % los dos cubren el 100 % y son
       indistinguibles.
    12. **Bug propio, del tipo que ya costó una sesión: inventé la clase `.quiz-pie`**, que no existe en
       ninguna hoja de estilos. El andamiaje funcionaba —el JavaScript encontraba sus elementos— pero el pie
       de las dos autoevaluaciones se veía **sin estilo**, con 0 px entre las preguntas y el marcador. Se
       sustituyó por el marcado de la casa (`.quiz-resumen` + `.quiz-marcador`) y se añadió la aserción
       correspondiente al script de ensamblado. Es exactamente el fallo de T4d con otro nombre.
    13. **11 de las 22 cifras que escribí a mano en los comentarios `#>` estaban mal**, algunas por un factor
       de dos. Se escribió `precalculo/verifica_bloques_cap6.py`, que extrae los bloques, los ejecuta
       encadenados y contrasta cada número; el capítulo se publica con **390 de 390** verificadas. El dato es
       ahora contenido del módulo 11.
    14. **Trampa de método propia: trabajé un rato con un volcado de datos obsoleto.** Al alinear el ETS y el
       STL con las definiciones del capítulo 5, sus cifras cambiaron (ETS de 23.82 a 23.17, STL de 19.78 a
       23.63) y con ellas el orden de la tabla y dos párrafos del módulo 8. Lo detectó el verificador de
       bloques, no la relectura. **Tras regenerar un JSON hay que volver a leerlo, no fiarse del volcado.**
  - *Desviaciones sobre el plan:* (a) el plan pedía 9 módulos y un simulador; se hicieron **12 módulos y 14
    simuladores**, con el alcance ampliado que eligió Javier: MASE y RMSSE completos, evaluación del intervalo
    (cobertura y Winkler), Diebold–Mariano, y el taller de auditoría de IA de la semana 15. (b) El taller
    **no estrena componente**: es una pregunta de selección múltiple del `.quiz` en su propio contenedor
    `data-quiz="auditoria"`, porque ese componente ya corrige parcialmente y da retroalimentación por opción.
    (c) Casos de estudio: AirPassengers (recorrido completo), TRM (nadie vence al naïve) y **Nilo** (la
    partición única y el origen móvil dan ganadores opuestos), más `USAccDeaths` y `co2` en los ejercicios.
    (d) El archivo pesa **445 KB**, por encima del límite de la tabla de riesgos: mismo criterio que en los
    capítulos 2 a 5. (e) **No se instaló ningún paquete nuevo.**
  - *Dependencias:* T2, T7. *Tamaño:* L.

- [x] **T8b · Componente `.tabla-ranking`** (nuevo en la plantilla, decisión de Javier).
  Tabla comparativa **ordenable**: al pulsar la cabecera de una métrica la tabla se reordena, se renumeran los
  puestos, se ilumina la fila ganadora y se marca el mejor valor de la columna activa. Es el argumento del
  capítulo —«el orden depende de la pregunta»— convertido en componente. Sin dependencias nuevas: una `<table>`
  de verdad con cabeceras que son botones, `aria-sort` en el `<th>`, `scope` en filas y columnas, `<caption>`, y
  cada reordenación anunciada en una región `role="status"`. Admite tres criterios por columna —`menor`, `mayor`
  y **`cerca` de un objetivo**, que es el único que sabe expresar lo que se le pide a una cobertura nominal—.
  Fuentes compartidas en `ensamblado/componentes/` (`tabla_ranking.css`, `.js`, `_html.py`).
  - **Instancias:** backtesting de 8 métodos y comparación del Nilo en el capítulo 6; y **retropropagado**
    (`ensamblado/retropropaga_ranking.py`): los 11 candidatos ARMA de las manchas solares en el capítulo 3, la
    **rejilla de 27 modelos del Nilo con su $n$ efectivo a la vista** en el capítulo 4 —ordenar por AICc corona
    a un modelo con $d=2$ evaluado sobre 98 observaciones, que es justo el error que ese capítulo enseña a no
    cometer—, la comparativa de 6 métodos del capítulo 5, y una demostración en la plantilla, en la misma
    sesión, como exige la regla del Checkpoint 0. Los capítulos 1 y 2 **no** lo reciben: ninguno tiene una tabla
    comparativa de modelos que ordenar (mismo criterio que con `.mapa-estacional`).
  - *Verificado en los cinco archivos:* consola sin errores; las tablas reordenan y renumeran; `aria-sort` queda
    en exactamente una columna; los anuncios de `role="status"` nombran la columna y el nuevo primero; el
    conjunto de selectores del capítulo 6 y del 5 es **idéntico al de la plantilla** (224) y ningún archivo tiene
    selectores que la plantilla no tenga; hueco mínimo 8 px tras subir el margen de `.tabla-ranking-estado` de
    0.4rem a 0.6rem, que medía 6.4 px.

- [x] **T8c · Bug del `.quiz` corregido en los seis capítulos y en la plantilla** (encontrado auditando T8).
  Al **acertar** una pregunta de selección múltiple, `renderAutoevaluacion()` escribía `p.retroAcierto`, que en
  ese tipo de pregunta **nunca se define**, y el estudiante veía literalmente la palabra «undefined» detrás de
  «Correcto». Son **9 preguntas en 7 archivos** y estaba ahí desde T4c. Corregido por partida doble: `cerrar()`
  ya no imprime un valor indefinido, y la rama de selección múltiple pasa como respaldo la retroalimentación de
  **las opciones correctas, que ya estaba escrita y no se mostraba nunca**. Los dos cambios van en
  `retropropaga_ranking.py` y se aplicaron a los seis capítulos y a la plantilla; los capítulos 1 y 2 no
  recibieron nada más, y su diff frente al respaldo son exactamente esas dos sustituciones.
  - *Verificado:* el `undefined` desaparece en las dos preguntas múltiples del capítulo 6 y en la del 3; la
    corrección parcial sigue funcionando («de las 5 que marcaste, 3 están en la respuesta»); el JavaScript de
    los siete archivos pasa `node --check`.

### Checkpoint 2
- [ ] Los 6 capítulos abren sin errores; navegación cruzada entre capítulos consistente; revisión de contenido de Javier.

### Fase 4 — Portada, repo y publicación

- [ ] **T9 · index.html + README + .nojekyll + .gitignore** — portada con las 6 tarjetas. *Dependencias:* T3–T8. *Tamaño:* S.
- [ ] **T10 · Despliegue** — push al repo remoto y activación de Pages.
  - *Ya hecho (2026-07-24, adelantado desde T10):* `git init -b main` en `Series de tiempo/`
    (todo el proyecto, no solo los HTML, para rastrear plan + plantilla + precálculos) y
    commit inicial `54e45ef` con 12 archivos. `.gitignore` excluye `*.pdf` — hay dos libros
    de texto (35 MB, uno de z-lib) en la carpeta que **no deben** publicarse ni entrar al
    historial de un repo público.
  - *Decisión pendiente — cómo sirve Pages:* el repositorio remoto ya existe
    (`JotaMao1985/Series-de-Tiempo_Un_Bosque`), pero Pages solo publica desde la raíz o
    desde `/docs`, y los capítulos viven en `Htmls_Series/`. Tres opciones: (a) renombrar
    `Htmls_Series/` → `docs/` y usar "deploy from /docs" (una sola rama, todo versionado);
    (b) `git subtree push --prefix Htmls_Series origin gh-pages` (mantiene el nombre, sitio
    limpio sin plan ni precálculos); (c) repo separado solo para los HTML, como en Muestreo.
    Recomendación: **(b)**, conserva la convención `Htmls_*` y publica únicamente el sitio.
  - *Criterios:* sitio accesible en la URL de Pages; KaTeX, simuladores y navegación
    funcionan en producción; el sitio publicado NO contiene los PDF ni los precálculos.
  - *Dependencias:* T9. *Tamaño:* XS (+ acción manual de Javier: `git remote add` y activar Pages).

## Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Ajustar ARIMA en el navegador es inviable | Alto | Precalcular en R e incrustar JSON (decidido; tareas T2, T6, T8) |
| Tailwind CDN u otros CDN caen o cambian | Medio | Mismo riesgo ya asumido en Muestreo; versiones fijadas donde el CDN lo permite (KaTeX 0.16.9, Prism 1.29.0) |
| Divergencia de resultados R vs. Python (p. ej. estimadores distintos) | Medio | Ejecutar ambos antes de publicar; cuando difieran, señalarlo como nota didáctica en el texto |
| Capítulos muy largos degradan el rendimiento móvil | Bajo | Límite práctico ~160 KB por archivo (máximo actual de Muestreo); simuladores con `requestAnimationFrame` |
| Serie colombiana con licencia/fuente ambigua | Bajo | Usar datos abiertos DANE con cita de fuente y fecha de corte |

## Preguntas abiertas — RESUELTAS (2026-07-23)

1. Serie colombiana: **TRM mensual** (SFC vía datos.gov.co), resuelto en Fase 0.
2. Repo remoto (ya creado por Javier): `https://github.com/JotaMao1985/Series-de-Tiempo_Un_Bosque.git`
   → Pages quedará en `https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/`.
   En T10 basta `git remote add origin` + push y activar Pages.
3. Títulos bilingües: **SÍ** — los títulos en inglés del cronograma (p. ej. "Stationarity
   & ACF/PACF") acompañan al español en los encabezados de los capítulos correspondientes.
