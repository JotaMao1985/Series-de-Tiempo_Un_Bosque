# Análisis de Series de Tiempo · Universidad El Bosque

Material de estudio autónomo e interactivo para el curso **Series de Tiempo 2026-II** del programa
de Matemáticas y Ciencia de Datos. Seis capítulos que van de la descomposición de una serie al
*backtesting* de un pronóstico, con teoría, fórmulas KaTeX, código en **R** y **Python**, **61
simuladores** interactivos, autoevaluación con retroalimentación por opción y ejercicios resueltos.

🌐 **Sitio web:** https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/

## Contenido

| # | Capítulo | Temas | Módulos | Simuladores |
|---|----------|-------|:---:|:---:|
| 1 | [Componentes y descomposición](capitulo-1-componentes-descomposicion.html) | Objetos temporales, gráficos estacionales, los cuatro componentes, medias móviles, descomposición clásica y STL | 9 | 7 |
| 2 | [Estacionariedad, ACF y PACF](capitulo-2-estacionariedad-acf-pacf.html) | Ruido blanco, correlograma, PACF, caminata aleatoria, ADF y KPSS, diferenciación, Box–Cox | 9 | 8 |
| 3 | [Modelos AR, MA y ARMA](capitulo-3-modelos-ar-ma-arma.html) | Polinomios característicos, invertibilidad, dualidad AR↔MA, identificación, máxima verosimilitud, diagnóstico | 10 | 10 |
| 4 | [Modelos ARIMA y Box–Jenkins](capitulo-4-modelos-arima.html) | Orden de integración, ciclo de Box–Jenkins, AICc, Hyndman–Khandakar, sobrediferenciación, intervalos | 10 | 10 |
| 5 | [Modelos SARIMA](capitulo-5-sarima.html) | Firma estacional, notación multiplicativa, modelo *airline*, SARIMAX, Fourier y STL | 11 | 12 |
| 6 | [Pronóstico y evaluación](capitulo-6-pronostico-evaluacion.html) | Métricas de error, fuga de información, origen móvil, backtesting, Diebold–Mariano, cobertura, auditoría de IA | 12 | 14 |

La portada [`index.html`](index.html) enlaza los seis capítulos. En total: **61 módulos, 61
simuladores, 49 preguntas de autoevaluación y 20 ejercicios guiados con solución comentada.**

## Cómo está construido

- **Un archivo HTML autocontenido por capítulo.** Sin build, sin `fetch`, sin dependencias locales:
  se puede abrir con doble clic y funciona sin conexión salvo por los CDN.
- **Los cómputos pesados no ocurren en el navegador.** Ajustar 61 orígenes de un SARIMA o una
  rejilla de 36 modelos se precalcula en R y se incrusta como JSON. Los simuladores hacen en vivo
  solo lo que es liviano (simular un ARMA, calcular una ACF, reordenar una tabla).
- **Los números salen de ejecutar el código, no de escribirlo.** Cada cifra que aparece en un
  comentario `#>` de un bloque de R o de Python se contrasta contra la salida real mediante un
  script; las soluciones de los ejercicios se resuelven en R antes de redactarlas.
- **Cuando R y Python difieren, el material lo dice.** Hay varias diferencias reales documentadas
  —el $p$-valor del ADF, el truncamiento del KPSS, la inicialización difusa de `statsmodels`— y se
  presentan como nota didáctica en vez de esconderse.

## Tecnología

- HTML estático, un solo archivo por capítulo.
- [Tailwind CSS](https://tailwindcss.com/) (CDN), [Font Awesome](https://fontawesome.com/),
  [KaTeX](https://katex.org/) 0.16.9, [Chart.js](https://www.chartjs.org/) 4 y
  [Prism](https://prismjs.com/) 1.29 con el componente de R.
- Cálculos en **R** (base + `tseries` + `forecast` + `jsonlite`) y equivalentes en **Python**
  (`numpy`, `pandas`, `statsmodels`, `scipy`).
- Diseño responsive y accesible: navegación por teclado, `aria-*` en todos los componentes
  interactivos, contraste cuidado y respeto a `prefers-reduced-motion`.

## Componentes interactivos

Además de los simuladores, el material usa cinco componentes propios, presentes en todos los
capítulos que los necesitan:

| Componente | Qué hace |
|---|---|
| `.quiz` | Autoevaluación con cuatro tipos de pregunta (opción única, selección múltiple con corrección parcial, respuesta numérica y diagnóstico de un gráfico), retroalimentación por opción —también en las incorrectas— y segundo intento con pista |
| `.ejercicio-guiado` | Ejercicio propuesto con desplegables de pista y solución comentada |
| `.derivacion` | Caja plegable con el desarrollo algebraico paso a paso |
| `.ciclo` | Diagrama de etapas recorrible con teclado, que muestra a qué etapa te devuelve cada fallo |
| `.mapa-estacional` | Mapa de calor mes × año, donde un mes sistemáticamente alto dibuja una banda vertical |
| `.tabla-ranking` | Tabla comparativa ordenable: al pulsar una columna cambia el orden, y con él el ganador |

## Despliegue

El sitio se publica con **GitHub Pages** desde la rama `gh-pages`, que contiene únicamente esta
carpeta. El repositorio principal (`main`) conserva además el plan de trabajo, los scripts de
precálculo en R y los de ensamblado, que no forman parte del sitio publicado. El archivo
`.nojekyll` desactiva el procesamiento Jekyll para servir el HTML tal cual.

## Créditos

Diseñado por **Javier Mauricio Sierra** · Universidad El Bosque · 2026.
Contenido alineado con el syllabus de Series de Tiempo 2026-II y basado en Hyndman &
Athanasopoulos, *Forecasting: Principles and Practice* (3.ª ed.) y Shumway & Stoffer, *Time Series
Analysis and Its Applications* (4.ª ed.).
