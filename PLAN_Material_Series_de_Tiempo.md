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

### Fase 2 — Capítulos 3 y 4

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

- [ ] **T6 · Capítulo 4** (ARIMA) — explorador de modelos con rejilla precalculada. *Dependencias:* T2 (rejilla), T5 (continuidad narrativa). *Tamaño:* L.

### Fase 3 — Capítulos 5 y 6

- [ ] **T7 · Capítulo 5** (SARIMA) — simulador de diferencias sobre AirPassengers. *Dependencias:* T6. *Tamaño:* L.
- [ ] **T8 · Capítulo 6** (pronóstico y evaluación) — simuladores de horizonte y rolling-origin. *Dependencias:* T2, T6. *Tamaño:* L.

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
