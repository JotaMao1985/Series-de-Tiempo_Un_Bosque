#!/usr/bin/env python3
"""Construye el Capítulo 6 a partir del Capítulo 5, por sustitución de regiones.

Mismo método que `ensambla_cap5.py` (ver el README de esta carpeta): se parte de
un capítulo que ya funciona y se cambian regiones delimitadas, de modo que todo
lo que no se toca —CSS, ayudantes de JavaScript, componentes, andamiaje— se
conserva por construcción.

Novedad respecto al capítulo 5: este script además **instala el componente
`.tabla-ranking`** en la región compartida (CSS, JavaScript y la llamada de
`loadModule`), porque es nuevo en este capítulo. `retropropaga_ranking.py` hace
lo mismo sobre los capítulos 3, 4, 5 y la plantilla.

El taller de auditoría del módulo 11 **no estrena componente**: es una pregunta
de selección múltiple del `.quiz` en su propio contenedor `data-quiz="auditoria"`.
Se decidió así para no añadir un segundo componente y porque el `.quiz` ya
corrige parcialmente y da retroalimentación por opción, que es justo lo que el
taller necesita.

Uso:  python3 ensambla_cap6.py       (desde ensamblado/)
"""

import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
CAP5 = RAIZ / "Htmls_Series" / "capitulo-5-sarima.html"
CAP6 = RAIZ / "Htmls_Series" / "capitulo-6-pronostico-evaluacion.html"
FUENTES = AQUI / "cap6"
COMPONENTES = AQUI / "componentes"
SALIDAS = RAIZ / "precalculo" / "salidas"

sys.path.insert(0, str(COMPONENTES))
from ciclo_html import ciclo_html, comprueba_ciclo                      # noqa: E402
from tabla_ranking_html import (tabla_ranking_html,                     # noqa: E402
                                comprueba_tabla_ranking)


def lee(p):
    if not p.exists():
        raise SystemExit(f"ABORTA: falta {p}")
    return p.read_text(encoding="utf-8")


def una_vez(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ABORTA [{etiqueta}]: el marcador aparece {n} veces, "
                         f"se esperaba 1.\n  marcador: {viejo[:110]!r}")
    return texto.replace(viejo, nuevo, 1)


def entre(texto, inicio, fin, etiqueta):
    """Bloque de `inicio` a la PRIMERA aparición de `fin` después de él.

    El marcador de inicio tiene que ser único —es el que identifica la región—;
    el de fin solo tiene que existir después, porque cierres como `    };` se
    repiten por todo el archivo.
    """
    if texto.count(inicio) != 1:
        raise SystemExit(f"ABORTA [{etiqueta}/inicio]: aparece "
                         f"{texto.count(inicio)} veces, se esperaba 1.")
    i = texto.index(inicio)
    j = texto.find(fin, i)
    if j == -1:
        raise SystemExit(f"ABORTA [{etiqueta}/fin]: no hay '{fin[:40]}' tras el inicio.")
    return texto[i:j + len(fin)]


html = lee(CAP5)

# ---------------------------------------------------------------------------
# 1. Metadatos de la cabecera
# ---------------------------------------------------------------------------
html = una_vez(
    html,
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 5: '
    'modelos SARIMA; firma estacional en ACF y PACF, notación multiplicativa, '
    'diferenciación estacional, el modelo airline, regresores de calendario, '
    'regresión armónica con términos de Fourier y comparación con ETS.">',
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 6: '
    'pronóstico y evaluación; residuales frente a errores de pronóstico, métodos '
    'de referencia, RMSE, MAE, MAPE y MASE, fuga de información, validación de '
    'origen móvil, backtesting, Diebold-Mariano, cobertura empírica y puntaje de '
    'Winkler.">',
    "meta description")

html = una_vez(
    html,
    'content="series de tiempo, SARIMA, estacionalidad, diferencia estacional, '
    'modelo airline, ACF estacional, rezagos satélite, nsdiffs, SARIMAX, regresores '
    'de calendario, Semana Santa, términos de Fourier, regresión armónica, STL, ETS, '
    'AirPassengers, USAccDeaths, TRM, R, Python"',
    'content="series de tiempo, pronóstico, backtesting, validación de origen móvil, '
    'rolling origin, time series cross-validation, RMSE, MAE, MAPE, sMAPE, MASE, '
    'RMSSE, Diebold-Mariano, cobertura empírica, puntaje de Winkler, fuga de '
    'información, data leakage, tsCV, accuracy, AirPassengers, Nilo, TRM, R, Python"',
    "meta keywords")

html = una_vez(
    html,
    "<title>Series de Tiempo · Capítulo 5 — Modelos SARIMA</title>",
    "<title>Series de Tiempo · Capítulo 6 — Pronóstico y evaluación</title>",
    "title")

html = una_vez(
    html,
    'style="margin:0; text-align:left;">CAPÍTULO 5 •',
    'style="margin:0; text-align:left;">CAPÍTULO 6 •',
    "cintillo de la cabecera")

html = una_vez(html, "MODELOS SARIMA", "PRONÓSTICO Y EVALUACIÓN",
               "subtítulo de la cabecera")

# ---------------------------------------------------------------------------
# 2. Instalación del componente .tabla-ranking (CSS, JS y llamada de arranque)
# ---------------------------------------------------------------------------
# Tras `retropropaga_ranking.py`, el capítulo 5 ya trae el componente y solo hay
# que dejarlo pasar: así este script sigue siendo REEJECUTABLE, que es la
# propiedad con la que se comprueba que las correcciones a mano viven en las
# fuentes y no solo en el HTML publicado.
ya_instalado = ".tabla-ranking {" in html
if not ya_instalado:
    # Ancla: el final del CSS del mapa estacional, que es lo último que instaló
    # el capítulo 5. Se inserta justo antes del cierre de <style>.
    ancla_css = """    @media (max-width: 640px) {
      .mapa-estacional-rejilla {
        grid-template-columns: 2.6rem repeat(12, minmax(2rem, 1fr));
      }

      .mapa-estacional-celda {
        font-size: 0.55rem;
        min-height: 1.4rem;
      }
    }
  </style>"""
    html = una_vez(html, ancla_css,
                   ancla_css.replace("  </style>",
                                     lee(COMPONENTES / "tabla_ranking.css").rstrip("\n")
                                     + "\n  </style>"),
                   "CSS de la tabla de ranking")

    ancla_js = """    function iniciarDerivaciones("""
    html = una_vez(html, ancla_js,
                   lee(COMPONENTES / "tabla_ranking.js").rstrip("\n") + "\n\n" + ancla_js,
                   "JavaScript de la tabla de ranking")

    html = una_vez(html, "        iniciarCiclos();\n",
                   "        iniciarCiclos();\n        iniciarTablasRanking();\n",
                   "llamada de arranque de la tabla de ranking")

# ---------------------------------------------------------------------------
# 3. Las doce plantillas de módulo
# ---------------------------------------------------------------------------
ETAPAS_CICLO = [
    {
        "clave": "pregunta",
        "numero": "Etapa 1",
        "titulo": "Fijar la pregunta",
        "resumen": "¿Qué horizonte, qué métrica?",
        "campos": [
            ("Qué haces", "<p>Decides <strong>a qué horizonte</strong> hay que pronosticar y "
                          "<strong>con qué métrica</strong> se va a juzgar, antes de ver ningún "
                          "resultado. El MASE por defecto; RMSE o MAE si el costo del error lo "
                          "justifica; MAPE solo si la serie está lejos del cero.</p>"),
            ("Con qué", "<p>El problema, no los datos. Si un error del doble de tamaño hace el "
                        "doble de daño, MAE; si hace más del doble, RMSE.</p>"),
        ],
        "vuelta": "<p>Si acabas eligiendo la métrica con la que gana tu modelo, todo lo demás "
                  "sobra: es la versión pequeña de la fuga del Módulo 6.</p>",
    },
    {
        "clave": "referencia",
        "numero": "Etapa 2",
        "titulo": "Elegir la referencia",
        "resumen": "¿Contra qué se compara?",
        "campos": [
            ("Qué haces", "<p>Fijas el método trivial que hay que batir: naïve estacional si hay "
                          "estación, naïve si la serie se parece a una caminata. Es el mismo que "
                          "irá en el denominador del MASE.</p>"),
            ("Con qué", "<p><code>snaive()</code>, <code>naive()</code>, <code>rwf(drift=TRUE)</code> "
                        "y <code>meanf()</code>. Cuestan una línea y no estiman nada.</p>"),
        ],
        "vuelta": "<p>Si tu modelo no le gana a la referencia, vuelve al modelo —o acepta la "
                  "referencia como respuesta, que en la TRM es lo correcto—.</p>",
    },
    {
        "clave": "origenes",
        "numero": "Etapa 3",
        "titulo": "Recorrer los orígenes",
        "resumen": "Reajustando en cada uno",
        "campos": [
            ("Qué haces", "<p>Fijas $T_0$, el horizonte y la ventana, y recorres todos los orígenes "
                          "<strong>reajustando el modelo en cada uno</strong> con solo su pasado.</p>"),
            ("Con qué", "<p><code>tsCV()</code> —comprobando que <code>initial</code> empieza donde "
                        "crees y quedándote con las filas completas— o un bucle propio.</p>"),
        ],
        "vuelta": "<p>Si los primeros orígenes tienen menos datos de los que el modelo necesita, "
                  "sube $T_0$: un ajuste con veinte observaciones efectivas contamina el promedio.</p>",
    },
    {
        "clave": "medir",
        "numero": "Etapa 4",
        "titulo": "Medir el punto y el intervalo",
        "resumen": "Métricas, cobertura y Winkler",
        "campos": [
            ("Qué haces", "<p>Calculas la métrica elegida <strong>por horizonte</strong>, y además "
                          "la cobertura empírica al $80\\,\\%$ <em>y</em> al $95\\,\\%$ y el puntaje "
                          "de Winkler.</p>"),
            ("Con qué", "<p>Las fórmulas de los Módulos 3 a 5 y 9. Declara siempre si el promedio "
                        "es sobre todos los errores o sobre los RMSE de cada origen: no dan lo mismo.</p>"),
        ],
        "vuelta": "<p>Si la cobertura del $80\\,\\%$ falla y la del $95\\,\\%$ no, hay <strong>sesgo</strong> "
                  "y el problema está en el modelo, no en el intervalo: vuelve a la etapa 2.</p>",
    },
    {
        "clave": "contrastar",
        "numero": "Etapa 5",
        "titulo": "Contrastar la diferencia",
        "resumen": "¿Es real o es ruido?",
        "campos": [
            ("Qué haces", "<p>Compruebas si la diferencia entre los dos mejores es distinguible del "
                          "azar, en el horizonte que te importa.</p>"),
            ("Con qué", "<p><code>dm.test</code> con el argumento <code>h</code>, vigilando que no "
                        "avise de varianza negativa; si avisa, <code>varestimator = \"bartlett\"</code>.</p>"),
        ],
        "vuelta": "<p>Si no hay diferencia significativa, no vuelvas a la tabla: elige por costo, "
                  "simplicidad e interpretabilidad, que es lo que separa al SARIMA de "
                  "<code>auto.arima</code>.</p>",
    },
]

plantillas_viejas = entre(html, '  <template id="module-1">',
                          "  </template>\n\n  <script>", "plantillas")
plantillas_nuevas = (
    lee(FUENTES / "templates_1_3.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_4_6.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_7_9.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_10_12.html").rstrip("\n") + "\n\n  <script>"
)

# Los componentes se generan con su constructor, no a mano: así el marcado es
# idéntico al de las otras instancias del proyecto y la comparación de
# selectores CSS no encuentra diferencias.
RANKINGS = {
    "backtest": ("Backtesting sobre 61 orígenes (h = 12)", ""),
    "nilo": ("El Nilo: una partición frente a treinta y seis orígenes", ""),
}
for clave, (titulo, pie) in RANKINGS.items():
    marca = f"<!--RANKING:{clave}|{titulo}|{pie}-->"
    if plantillas_nuevas.count(marca) != 1:
        raise SystemExit(f"ABORTA [ranking {clave}]: el marcador aparece "
                         f"{plantillas_nuevas.count(marca)} veces")
    plantillas_nuevas = plantillas_nuevas.replace(
        "      " + marca,
        tabla_ranking_html(clave, titulo, pie, sangria="      ").rstrip("\n"), 1)

marca_ciclo = "<!--CICLO:evaluacion-honesta-->"
if plantillas_nuevas.count(marca_ciclo) != 1:
    raise SystemExit("ABORTA [ciclo]: el marcador no aparece exactamente una vez")
plantillas_nuevas = plantillas_nuevas.replace(
    "      " + marca_ciclo,
    ciclo_html("evaluacion-honesta", ETAPAS_CICLO,
               "Las vueltas atrás son lo que distingue este ciclo de una lista: una cobertura "
               "que falla solo en el nivel estrecho no se arregla tocando el intervalo, se "
               "arregla volviendo al modelo.",
               sangria="      ").rstrip("\n"), 1)

html = una_vez(html, plantillas_viejas, plantillas_nuevas, "plantillas de módulo")

# ---------------------------------------------------------------------------
# 4. courseData
# ---------------------------------------------------------------------------
course_viejo = entre(html, "    const courseData = {", "    };", "courseData")
course_nuevo = """    const courseData = {
      title: "Series de Tiempo",
      modules: [
        { id: 1, title: "Residual no es error de pronóstico", shortTitle: "Residual vs. error", duration: "14 min" },
        { id: 2, title: "Los métodos de referencia", shortTitle: "Referencias", duration: "12 min" },
        { id: 3, title: "RMSE y MAE: qué optimiza cada uno", shortTitle: "RMSE y MAE", duration: "14 min" },
        { id: 4, title: "MAPE y sMAPE: los dos fallos del porcentaje", shortTitle: "MAPE", duration: "14 min" },
        { id: 5, title: "MASE: comparar entre series", shortTitle: "MASE", duration: "12 min" },
        { id: 6, title: "Partición temporal y fuga de información", shortTitle: "Fuga", duration: "18 min" },
        { id: 7, title: "Validación de origen móvil", shortTitle: "Origen móvil", duration: "18 min" },
        { id: 8, title: "Backtesting y Diebold–Mariano", shortTitle: "Backtesting", duration: "18 min" },
        { id: 9, title: "Evaluar el intervalo: cobertura y Winkler", shortTitle: "Cobertura", duration: "16 min" },
        { id: 10, title: "Tres casos, tres desenlaces", shortTitle: "Tres casos", duration: "16 min" },
        { id: 11, title: "Taller: auditar un análisis asistido por IA", shortTitle: "Auditar IA", duration: "16 min" },
        { id: 12, title: "El proyecto y cierre del curso", shortTitle: "Cierre", duration: "20 min" }
      ]
    };"""
html = una_vez(html, course_viejo, course_nuevo, "courseData")

# ---------------------------------------------------------------------------
# 5. Los datos precalculados
# ---------------------------------------------------------------------------
inicio_datos = "    // Generado por precalculo/genera_cap5.R"
if html.count(inicio_datos) != 1:
    raise SystemExit("ABORTA [datos]: no encuentro el comentario del precálculo del cap. 5")
i = html.index(inicio_datos)
if html.count("    const SERIES_CAP5 = ") != 1:
    raise SystemExit("ABORTA [datos]: SERIES_CAP5 no aparece exactamente una vez")
j = html.index("\n", html.index("    const SERIES_CAP5 = ", i)) + 1
datos_nuevos = "".join(
    "    " + linea if linea.strip() else linea
    for linea in lee(SALIDAS / "cap6_datos.js").splitlines(keepends=True))
html = html[:i] + datos_nuevos + html[j:]

# ---------------------------------------------------------------------------
# 6. El JavaScript propio del capítulo
# ---------------------------------------------------------------------------
inicio_js = ("    // ================================================================\n"
             "    // Datos y ayudantes del capítulo, tomados del precálculo en R")
if html.count(inicio_js) != 1:
    raise SystemExit("ABORTA [js]: no encuentro el inicio del JavaScript del capítulo")
i = html.index(inicio_js)
fin_js = "\n  </script>"
j = html.find(fin_js, i)
if j == -1:
    raise SystemExit("ABORTA [js]: no hay '</script>' tras el JavaScript del capítulo")
html = html[:i] + lee(FUENTES / "chapter.js").rstrip("\n") + html[j:]

# ---------------------------------------------------------------------------
# 7. Comprobaciones finales
# ---------------------------------------------------------------------------
fallos = []

SIMULADORES = [
    "residual-vs-error", "benchmarks", "rmse-vs-mae", "sesgo-mape", "mape-cero",
    "cambio-escala", "fuga-cv", "seleccion-prueba", "origen-movil",
    "error-por-horizonte", "diebold-mariano", "winkler", "cobertura", "tres-casos",
]

for n in range(1, 13):
    if html.count(f'<template id="module-{n}">') != 1:
        fallos.append(f"la plantilla module-{n} no aparece exactamente una vez")
if html.count('<template id="module-13">') != 0:
    fallos.append("ha quedado una plantilla module-13")

for sim in SIMULADORES:
    if html.count(f"SIMULADORES['{sim}']") != 1:
        fallos.append(f"el simulador '{sim}' no está registrado exactamente una vez")
    if html.count(f'data-simulador="{sim}"') != 1:
        fallos.append(f"el contenedor de '{sim}' no aparece exactamente una vez")

# Andamiaje de los DOS quizzes: renderAutoevaluacion() lanza excepción si falta
# alguna pieza, y este capítulo tiene el del cierre y el del taller de auditoría.
for quiz in ("cap6", "auditoria"):
    if html.count(f'<div class="quiz" data-quiz="{quiz}">') != 1:
        fallos.append(f"el contenedor del quiz '{quiz}' no aparece exactamente una vez")
    if html.count(f"AUTOEVALUACIONES['{quiz}']") != 1:
        fallos.append(f"AUTOEVALUACIONES['{quiz}'] no aparece exactamente una vez")
for pieza, esperadas in [('class="quiz-preguntas"', 2), ('class="quiz-progreso-barra"', 2),
                         ('class="quiz-resumen"', 2), ('class="quiz-conteo"', 2),
                         ('class="quiz-reiniciar"', 2), ('class="quiz-marcador"', 2)]:
    if html.count(pieza) != esperadas:
        fallos.append(f"andamiaje del quiz: '{pieza}' aparece {html.count(pieza)} veces, "
                      f"se esperaban {esperadas}")

# Componente .ciclo: se hereda, y aquí tiene su propia instancia de 5 etapas
fallos += comprueba_ciclo(html, "evaluacion-honesta", 5)
if html.count("function iniciarCiclos()") != 1 or html.count("        iniciarCiclos();") != 1:
    fallos.append("el componente .ciclo no se heredó bien del capítulo 5")

# Componente .tabla-ranking: nuevo, hay que comprobar las tres piezas
for clave in RANKINGS:
    fallos += comprueba_tabla_ranking(html, clave)
# `.tabla-ranking table` y `.tabla-ranking-boton` salen dos veces a propósito:
# la segunda es la sobreescritura de la media query de móvil.
for pieza, esperadas in [(".tabla-ranking {", 1), (".tabla-ranking table {", 2),
                         (".tabla-ranking-marco {", 1), (".tabla-ranking-boton {", 3),
                         (".tabla-ranking-puesto {", 2), (".tabla-ranking-pie {", 1),
                         (".tabla-ranking-estado {", 1),
                         ("function pintarTablaRanking", 1),
                         ("function iniciarTablasRanking", 1),
                         ("const TABLAS_RANKING", 1),
                         ("        iniciarTablasRanking();", 1)]:
    if html.count(pieza) != esperadas:
        fallos.append(f"tabla de ranking: '{pieza}' aparece {html.count(pieza)} veces, "
                      f"se esperaban {esperadas}")

# El .mapa-estacional se hereda del capítulo 5 pero este capítulo NO lo usa:
# tiene que quedar el CSS y el JavaScript, y ninguna instancia.
if html.count(".mapa-estacional {") != 1 or html.count("function pintarMapaEstacional") != 1:
    fallos.append("se perdió el componente .mapa-estacional heredado")
# Se cuenta el TÍTULO de la instancia y no el contenedor, porque el JavaScript
# heredado documenta el componente con un ejemplo dentro de un comentario.
if html.count('<p class="mapa-estacional-titulo">') != 0:
    fallos.append("ha quedado una instancia del mapa estacional del capítulo 5")

# Componentes heredados que deben seguir intactos
for regla in [".derivacion {", ".ciclo-boton {", ".quiz {", ".simulador-lectura",
              ".ejercicio-guiado {", ".grafico-etiqueta", ".simulador-intro",
              ".control-selector", ".control-interruptor"]:
    if regla not in html:
        fallos.append(f"se perdió la regla CSS {regla}")
for fn in ["function crearGraficoBarras", "function calcularPACF", "function crearSelector",
           "function crearInterruptores", "function iniciarDerivaciones",
           "function renderAutoevaluacion", "function iniciarEjerciciosGuiados",
           "function manejador"]:
    if html.count(fn) != 1:
        fallos.append(f"el ayudante '{fn}' no aparece exactamente una vez")

# Nada del capítulo anterior debe sobrevivir
for resto in ["DATOS_CAP5", "SERIES_CAP5", "AUTOEVALUACIONES['cap5']", "genera_cap5.R",
              "capitulo-5", "Capítulo 5 —", 'data-ciclo="identificacion-estacional"',
              "SIMULADORES['mapa-firma']", "SIMULADORES['explorador-sarima']"]:
    if resto in html:
        fallos.append(f"queda material del capítulo 5: '{resto}'")

# Datos del capítulo 6 presentes
for dato in ["const DATOS_CAP6", "const SERIES_CAP6"]:
    if html.count(dato) != 1:
        fallos.append(f"'{dato}' no aparece exactamente una vez")
# `genera_cap6.R` sale dos veces: en el comentario de cabecera del .js y en el
# campo `generador` que el propio JSON incrusta.
if html.count("genera_cap6.R") != 2:
    fallos.append(f"'genera_cap6.R' aparece {html.count('genera_cap6.R')} veces, se esperaban 2")

# Derivaciones: se cuenta el marcado real (contenedor + botón), no la cadena
# suelta, porque el JavaScript heredado documenta el componente con un ejemplo
# dentro de un comentario.
n_der = len(re.findall(r'<div class="derivacion">\s*\n\s*<button', html))
if n_der != 1:
    fallos.append(f"hay {n_der} cajas de derivación, se esperaba 1")
n_paneles_der = len(re.findall(r'<div class="derivacion-panel" id="[^"]+" hidden>', html))
if n_paneles_der != 1:
    fallos.append(f"hay {n_paneles_der} paneles de derivación, se esperaba 1")

# Ejercicios guiados con sus dos desplegables cada uno
n_ej = html.count('<div class="ejercicio-guiado">')
if n_ej != 3:
    fallos.append(f"hay {n_ej} ejercicios guiados, se esperaban 3")
for k in (1, 2, 3):
    for sufijo in ("pista", "sol"):
        if html.count(f'id="c6e{k}-{sufijo}"') != 1:
            fallos.append(f"el panel c6e{k}-{sufijo} no aparece exactamente una vez")
n_botones_ej = html.count('class="ejercicio-boton"')
if n_botones_ej != 6:
    fallos.append(f"hay {n_botones_ej} botones de ejercicio, se esperaban 6")

if fallos:
    print("ABORTA: el resultado no pasa las comprobaciones\n")
    for f in fallos:
        print("  -", f)
    raise SystemExit(1)

CAP6.write_text(html, encoding="utf-8")
print(f"Escrito: {CAP6.relative_to(RAIZ)} ({len(html.encode('utf-8')) / 1024:.1f} KB)")
print(f"  {len(SIMULADORES)} simuladores · 12 módulos · 2 tablas de ranking · "
      f"2 quizzes · 3 ejercicios · 1 ciclo de 5 etapas")
