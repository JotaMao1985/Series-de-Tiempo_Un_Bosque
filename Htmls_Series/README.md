# Análisis de Series de Tiempo · Universidad El Bosque

Material de estudio autónomo e interactivo para el curso **Series de Tiempo 2026-II** del programa
de Matemáticas y Ciencia de Datos. Seis capítulos que van de la descomposición de una serie al
*backtesting* de un pronóstico, con teoría, fórmulas KaTeX, código en **R** y **Python**, **65
simuladores** interactivos, autoevaluación con retroalimentación por opción y ejercicios resueltos.

🌐 **Sitio web:** https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/

## Contenido

| # | Capítulo | Temas | Módulos | Simuladores |
|---|----------|-------|:---:|:---:|
| 1 | [Componentes y descomposición](capitulo-1-componentes-descomposicion.html) | Objetos temporales, gráficos estacionales, los cuatro componentes, medias móviles, descomposición clásica y STL | 9 | 11 |
| 2 | [Estacionariedad, ACF y PACF](capitulo-2-estacionariedad-acf-pacf.html) | Ruido blanco, correlograma, PACF, caminata aleatoria, ADF y KPSS, diferenciación, Box–Cox | 9 | 8 |
| 3 | [Modelos AR, MA y ARMA](capitulo-3-modelos-ar-ma-arma.html) | Polinomios característicos, invertibilidad, dualidad AR↔MA, identificación, máxima verosimilitud, diagnóstico | 10 | 10 |
| 4 | [Modelos ARIMA y Box–Jenkins](capitulo-4-modelos-arima.html) | Orden de integración, ciclo de Box–Jenkins, AICc, Hyndman–Khandakar, sobrediferenciación, intervalos | 10 | 10 |
| 5 | [Modelos SARIMA](capitulo-5-sarima.html) | Firma estacional, notación multiplicativa, modelo *airline*, SARIMAX, Fourier y STL | 11 | 12 |
| 6 | [Pronóstico y evaluación](capitulo-6-pronostico-evaluacion.html) | Métricas de error, fuga de información, origen móvil, backtesting, Diebold–Mariano, cobertura, auditoría de IA | 12 | 14 |

La portada [`index.html`](index.html) enlaza los seis capítulos. En total: **61 módulos, 65
simuladores, 49 preguntas de autoevaluación y 20 ejercicios guiados con solución comentada.**

## Taller y preparcial

| # | Taller | Cubre | Módulos | Tareas |
|---|--------|-------|:---:|:---:|
| 1 | [Módulo I · Componentes y estacionariedad](taller-1-modulo-1.html) | Capítulos 1 y 2 · Corte I, semana 4 | 8 | 5 |

El taller es **individual y por variante**: cada estudiante recibe su propia serie no estacionaria
y su propia serie estacional, asignadas por los tres últimos dígitos de su documento a partir de
1000 variantes precalculadas en R. El navegador no calcula nada — busca la fila. El enunciado
incluye la rúbrica y el banco de preguntas de la defensa, y la plantilla de entrega en LaTeX está
en [`entrega/`](entrega/).

Lo que **no** viaja en este repositorio mientras el taller esté abierto: el generador de las
series, los auditores y el ensamblador. Se versionan después de calificar.

| # | Preparcial | Cubre | Módulos | Ítems |
|---|------------|-------|:---:|:---:|
| I | [Corte I · Componentes, estacionariedad, ACF y PACF](preparcial-corte-1.html) | Capítulos 1 y 2 · antes del Parcial 1 | 8 | 32 |

El preparcial **no se entrega y no tiene nota**, y por eso es el mismo para los nueve: aquí copiar
no tiene sentido, porque el que copia se queda sin lo único que produce. Sus 32 ítems se reparten
en cuatro bloques —concepto, procedimiento, interpretación y análisis gráfico— en la misma
proporción con la que está construido el parcial, y esa tabla de especificaciones se publica dentro
del propio instrumento: estudiar sin saber qué pesa es estudiar a ciegas.

Corre sobre **series generadas aparte, ninguna de ellas `AirPassengers`**. Sobre la serie canónica
del material reconocer sustituye a razonar, y entonces el diagnóstico miente. Al terminar cada
bloque, un termómetro por objetivo dice en cuál se está flojo y enlaza al módulo exacto del capítulo
que hay que releer. Las soluciones viajan dentro de la página: no hay clave oculta que proteger.

Ninguna cifra del instrumento está escrita a mano — todas salen de R — y
`precalculo/verifica_preparcial.R` las vuelve a calcular desde los valores publicados y las
contrasta, además de comprobar que ningún enunciado repita uno de los que el estudiante ya vio.

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

Además de los simuladores, el material usa siete componentes propios, presentes en todos los
capítulos y talleres que los necesitan:

| Componente | Qué hace |
|---|---|
| `.quiz` | Autoevaluación con cuatro tipos de pregunta (opción única, selección múltiple con corrección parcial, respuesta numérica y diagnóstico de un gráfico), retroalimentación por opción —también en las incorrectas— y segundo intento con pista |
| `.ejercicio-guiado` | Ejercicio propuesto con desplegables de pista y solución comentada |
| `.derivacion` | Caja plegable con el desarrollo algebraico paso a paso |
| `.ciclo` | Diagrama de etapas recorrible con teclado, que muestra a qué etapa te devuelve cada fallo |
| `.mapa-estacional` | Mapa de calor mes × año, donde un mes sistemáticamente alto dibuja una banda vertical |
| `.tabla-ranking` | Tabla comparativa ordenable: al pulsar una columna cambia el orden, y con él el ganador |
| `.rubrica` | Criterios de calificación recorribles: se pulsa uno y aparece qué mide y qué distingue cada nivel. Va dentro del material, no en un anexo del profesor — una rúbrica que se lee después de entregar no sirve |

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
