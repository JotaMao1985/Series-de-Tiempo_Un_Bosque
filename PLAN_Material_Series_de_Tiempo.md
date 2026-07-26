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
- [ ] Plantilla aprobada visualmente por Javier antes de producir capítulos en serie.
      Abrir `plantilla/plantilla-capitulo.html` y revisar los 3 módulos de demostración.

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
- [ ] **T4 · Capítulo 2** (estacionariedad, ACF/PACF, diferenciación) — mismos criterios; simulador de φ con ACF en vivo.
  - *Dependencias:* T1, T2. *Tamaño:* L.

### Checkpoint 1
- [ ] Revisión de Javier del capítulo 1 completo (tono, profundidad, densidad de fórmulas y código) antes de continuar. Ajustes se propagan a la plantilla.

### Fase 2 — Capítulos 3 y 4

- [ ] **T5 · Capítulo 3** (AR/MA/ARMA) — simulador con ACF/PACF teóricas y triángulo AR(2). *Dependencias:* T1, T2. *Tamaño:* L.
- [ ] **T6 · Capítulo 4** (ARIMA) — explorador de modelos con rejilla precalculada. *Dependencias:* T2 (rejilla), T5 (continuidad narrativa). *Tamaño:* L.

### Fase 3 — Capítulos 5 y 6

- [ ] **T7 · Capítulo 5** (SARIMA) — simulador de diferencias sobre AirPassengers. *Dependencias:* T6. *Tamaño:* L.
- [ ] **T8 · Capítulo 6** (pronóstico y evaluación) — simuladores de horizonte y rolling-origin. *Dependencias:* T2, T6. *Tamaño:* L.

### Checkpoint 2
- [ ] Los 6 capítulos abren sin errores; navegación cruzada entre capítulos consistente; revisión de contenido de Javier.

### Fase 4 — Portada, repo y publicación

- [ ] **T9 · index.html + README + .nojekyll + .gitignore** — portada con las 6 tarjetas. *Dependencias:* T3–T8. *Tamaño:* S.
- [ ] **T10 · Repo y despliegue** — `git init`, primer commit; Javier crea el repo remoto en GitHub y activa Pages (rama main, carpeta raíz); verificación del sitio publicado.
  - *Criterios:* sitio accesible en la URL de Pages; KaTeX, simuladores y navegación funcionan en producción.
  - *Dependencias:* T9. *Tamaño:* XS (+ acción manual de Javier).

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
