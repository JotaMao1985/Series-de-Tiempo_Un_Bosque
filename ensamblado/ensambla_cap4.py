#!/usr/bin/env python3
"""Construye el Capítulo 4 a partir del Capítulo 3, por sustitución de regiones.

Sigue el método descrito en el README de esta carpeta: se parte de un capítulo
que ya funciona y se cambian regiones delimitadas, de modo que todo lo que no
se toca —CSS, ayudantes de JavaScript, componentes, andamiaje— se conserva por
construcción. Cada sustitución exige que su marcador aparezca exactamente una
vez, y al final se comprueba que el resultado contiene todo lo que debe y nada
de lo que no debe.

El componente `.tabla-ranking` no lo instala este script: llegó al capítulo 4
con `retropropaga_ranking.py` y su CSS y sus ayudantes se heredan del capítulo 3.
Lo que sí vive aquí es su **instancia** —marcador `<!--RANKING:...-->` en
`cap4/templates_4_6.html` y el registro en `cap4/chapter.js`—, porque está en las
dos regiones que el ensamblado sustituye y sin ella el reensamblado la borraba
en silencio (ver la Advertencia del README).

Uso:  python3 ensambla_cap4.py       (desde ensamblado/)
"""

import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
CAP3 = RAIZ / "Htmls_Series" / "capitulo-3-modelos-ar-ma-arma.html"
CAP4 = RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
FUENTES = AQUI / "cap4"
COMPONENTES = AQUI / "componentes"
SALIDAS = RAIZ / "precalculo" / "salidas"

sys.path.insert(0, str(COMPONENTES))
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
    """Devuelve el bloque que va de `inicio` a la PRIMERA aparición de `fin`.

    El marcador de inicio sí tiene que ser único —es el que identifica la
    región—; el de fin solo tiene que existir después de él, porque cierres
    como `    };` se repiten por todo el archivo.
    """
    if texto.count(inicio) != 1:
        raise SystemExit(f"ABORTA [{etiqueta}/inicio]: aparece "
                         f"{texto.count(inicio)} veces, se esperaba 1.")
    i = texto.index(inicio)
    j = texto.find(fin, i)
    if j == -1:
        raise SystemExit(f"ABORTA [{etiqueta}/fin]: no hay '{fin[:40]}' tras el inicio.")
    return texto[i:j + len(fin)]


html = lee(CAP3)

# ---------------------------------------------------------------------------
# 1. Metadatos de la cabecera
# ---------------------------------------------------------------------------
html = una_vez(
    html,
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 3: '
    'modelos AR, MA y ARMA; operador de rezago, estacionariedad e invertibilidad, '
    'identificación con ACF/PACF, estimación y diagnóstico de residuales.">',
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 4: '
    'modelos ARIMA y metodología de Box–Jenkins; el orden de integración d, '
    'identificación, criterios de información, el algoritmo de Hyndman–Khandakar, '
    'diagnóstico, sobrediferenciación y pronóstico con intervalos.">',
    "meta description")

html = una_vez(
    html,
    'content="series de tiempo, AR, MA, ARMA, operador de rezago, polinomio '
    'característico, invertibilidad, Yule-Walker, máxima verosimilitud, AIC, AICc, '
    'BIC, Ljung-Box, manchas solares, R, Python"',
    'content="series de tiempo, ARIMA, Box-Jenkins, orden de integración, '
    'diferenciación, raíz unitaria, KPSS, ADF, auto.arima, Hyndman-Khandakar, AICc, '
    'BIC, sobrediferenciación, intervalos de pronóstico, pesos psi, Nilo, TRM, R, Python"',
    "meta keywords")

html = una_vez(
    html,
    "<title>Series de Tiempo · Capítulo 3 — Modelos AR, MA y ARMA</title>",
    "<title>Series de Tiempo · Capítulo 4 — Modelos ARIMA y Box–Jenkins</title>",
    "title")

html = una_vez(
    html,
    'style="margin:0; text-align:left;">CAPÍTULO 3 •',
    'style="margin:0; text-align:left;">CAPÍTULO 4 •',
    "cintillo de la cabecera")

html = una_vez(
    html, "MODELOS AR, MA Y ARMA", "MODELOS ARIMA Y BOX–JENKINS",
    "subtítulo de la cabecera")

# ---------------------------------------------------------------------------
# 1b. El CSS del .simulacro: el del capítulo 3, más las respuestas nuevas
# ---------------------------------------------------------------------------
# Este capítulo también tiene su simulacro del quiz (Módulo 11, desde el
# 2026-09-27). El CSS del componente llega del capítulo 3 tal cual; lo que se
# añade aquí es el de las formas que aquel quiz no tenía —los desplegables de
# emparejar y ordenar y la casilla numérica—, en
# `componentes/simulacro_respuestas.css`, justo detrás del rótulo de cierre del
# heredado. Hasta esa fecha este paso RECORTABA el CSS heredado, porque el
# simulacro era solo del capítulo 3; ahora el recorte, de los dos, lo hace
# `ensambla_cap5.py`. El motor de JavaScript no se hereda: el del capítulo 3
# vive en la región que se rehace entera, y el de este, ampliado, en
# `cap4/chapter.js`.
FIN_CSS_SIMULACRO = "    /* ------------------- fin del componente .simulacro ------------------- */\n"
if ".simulacro-filas {" in html:
    raise SystemExit("ABORTA: el capítulo 3 ya trae el CSS de las respuestas del simulacro. "
                     "Si se retro-portó allí, aquí hay que heredarlo, no instalarlo.")
html = una_vez(html, FIN_CSS_SIMULACRO,
               FIN_CSS_SIMULACRO + "\n" + lee(COMPONENTES / "simulacro_respuestas.css"),
               "CSS de las respuestas del .simulacro")

# ---------------------------------------------------------------------------
# 2. Las doce plantillas de módulo (la 11 es el simulacro del quiz y la 12
#    presenta el preparcial del Corte II, que vive en su propia página)
# ---------------------------------------------------------------------------
plantillas_viejas = entre(html, '  <template id="module-1">',
                          "  </template>\n\n  <script>", "plantillas")
plantillas_nuevas = (
    lee(FUENTES / "templates_1_3.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_4_6.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_7_9.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_10.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_11.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_12.html").rstrip("\n") + "\n\n  <script>"
)

# Los componentes se generan con su constructor, no a mano: así el marcado es
# idéntico al de las otras instancias del proyecto y la comparación de
# selectores CSS no encuentra diferencias. La tabla de ranking llegó a este
# capítulo por `retropropaga_ranking.py`, no por el ensamblado original; vive
# aquí para que el reensamblado no la borre.
RANKINGS = {
    "rejilla-nilo": ("Los 27 modelos del Nilo, con su n efectivo a la vista", ""),
}
for clave, (titulo, pie) in RANKINGS.items():
    marca = f"<!--RANKING:{clave}|{titulo}|{pie}-->"
    if plantillas_nuevas.count(marca) != 1:
        raise SystemExit(f"ABORTA [ranking {clave}]: el marcador aparece "
                         f"{plantillas_nuevas.count(marca)} veces")
    plantillas_nuevas = plantillas_nuevas.replace(
        "      " + marca,
        tabla_ranking_html(clave, titulo, pie, sangria="      ").rstrip("\n"), 1)

html = una_vez(html, plantillas_viejas, plantillas_nuevas, "plantillas de módulo")

# ---------------------------------------------------------------------------
# 3. courseData
# ---------------------------------------------------------------------------
course_viejo = entre(html, "    const courseData = {", "    };", "courseData")
course_nuevo = """    const courseData = {
      title: "Series de Tiempo",
      modules: [
        { id: 1, title: "De ARMA a ARIMA", shortTitle: "ARIMA", duration: "12 min" },
        { id: 2, title: "La metodología Box–Jenkins", shortTitle: "Box–Jenkins", duration: "10 min" },
        { id: 3, title: "Elegir el orden d", shortTitle: "Elegir d", duration: "16 min" },
        { id: 4, title: "Identificar p y q", shortTitle: "Identificar p,q", duration: "14 min" },
        { id: 5, title: "La constante: media y deriva", shortTitle: "Media y deriva", duration: "12 min" },
        { id: 6, title: "Estimar y comparar modelos", shortTitle: "Explorador", duration: "16 min" },
        { id: 7, title: "Dentro de auto.arima", shortTitle: "auto.arima", duration: "14 min" },
        { id: 8, title: "Diagnóstico y errores comunes", shortTitle: "Diagnóstico", duration: "16 min" },
        { id: 9, title: "Pronóstico: forma e intervalos", shortTitle: "Pronóstico", duration: "16 min" },
        { id: 10, title: "Caso TRM, puente y cierre", shortTitle: "Cierre", duration: "24 min" },
        { id: 11, title: "Simulacro del quiz", shortTitle: "Simulacro", duration: "40 min" },
        { id: 12, title: "Preparcial del Corte II", shortTitle: "Preparcial", duration: "5 min" }
      ]
    };"""
html = una_vez(html, course_viejo, course_nuevo, "courseData")

# ---------------------------------------------------------------------------
# 4. Los datos precalculados
# ---------------------------------------------------------------------------
# El capítulo 3 incrusta un solo `const DATOS_CAP3 = {...};` en una línea; el
# 4 incrusta además `SERIES_CAP4`, así que la región se delimita por el
# comentario de cabecera y el final de la línea de la última constante del 3.
inicio_datos = "    // Generado por precalculo/genera_cap3.R"
if html.count(inicio_datos) != 1:
    raise SystemExit("ABORTA [datos]: no encuentro el comentario del precálculo del cap. 3")
i = html.index(inicio_datos)
if html.count("    const DATOS_CAP3 = ") != 1:
    raise SystemExit("ABORTA [datos]: DATOS_CAP3 no aparece exactamente una vez")
j = html.index("\n", html.index("    const DATOS_CAP3 = ", i)) + 1
datos_nuevos = "".join(
    "    " + linea if linea.strip() else linea
    for linea in lee(SALIDAS / "cap4_datos.js").splitlines(keepends=True))
html = html[:i] + datos_nuevos + html[j:]

# ---------------------------------------------------------------------------
# 5. El JavaScript propio del capítulo
# ---------------------------------------------------------------------------
inicio_js = ("    // ================================================================\n"
             "    // Datos y ayudantes del capítulo, tomados del precálculo en R")
if html.count(inicio_js) != 1:
    raise SystemExit("ABORTA [js]: no encuentro el inicio del JavaScript del capítulo")
i = html.index(inicio_js)
# El cierre `</script>` aparece también en la cabecera (config de Tailwind);
# el que interesa es el primero DESPUÉS del inicio del JS del capítulo.
fin_js = "\n  </script>"
j = html.find(fin_js, i)
if j == -1:
    raise SystemExit("ABORTA [js]: no hay '</script>' tras el JavaScript del capítulo")
html = html[:i] + lee(FUENTES / "chapter.js").rstrip("\n") + html[j:]

# ---------------------------------------------------------------------------
# 6. Comprobaciones finales
# ---------------------------------------------------------------------------
fallos = []

SIMULADORES = [
    "nilo-y-diferencia", "escalon-vs-raiz", "identificacion-nilo",
    "explorador-modelos", "traza-auto-arima", "sobrediferenciacion",
    "forma-pronostico", "pesos-psi-sigma", "trm-identificacion",
    "trm-abanico", "puente-estacional", "cap4-simulacro",
]

for n in range(1, 13):
    if html.count(f'<template id="module-{n}">') != 1:
        fallos.append(f"la plantilla module-{n} no aparece exactamente una vez")

for sim in SIMULADORES:
    if html.count(f"SIMULADORES['{sim}']") != 1:
        fallos.append(f"el simulador '{sim}' no está registrado exactamente una vez")
    if html.count(f'data-simulador="{sim}"') != 1:
        fallos.append(f"el contenedor de '{sim}' no aparece exactamente una vez")

# Andamiaje del quiz: renderAutoevaluacion() lanza excepción si falta alguno.
# La comprobación está aquí porque ese fallo ya ocurrió una vez (auditoría T5).
for pieza in ['<div class="quiz" data-quiz="cap4">', 'class="quiz-preguntas"',
              'class="quiz-progreso-barra"', 'class="quiz-resumen"',
              'class="quiz-conteo"', 'class="quiz-reiniciar"']:
    if html.count(pieza) != 1:
        fallos.append(f"andamiaje del quiz: '{pieza}' aparece {html.count(pieza)} veces")
if html.count("AUTOEVALUACIONES['cap4']") != 1:
    fallos.append("AUTOEVALUACIONES['cap4'] no aparece exactamente una vez")

# El componente .ciclo se hereda del capítulo 3; aquí debe tener su instancia
if html.count('data-ciclo="box-jenkins"') != 1:
    fallos.append("falta la instancia .ciclo del ciclo de Box–Jenkins")
if html.count('aria-controls="ciclo-box-jenkins-') != 4:
    fallos.append("el ciclo de Box–Jenkins no tiene exactamente 4 etapas")
if html.count("function iniciarCiclos()") != 1 or html.count("        iniciarCiclos();") != 1:
    fallos.append("el componente .ciclo no se heredó bien del capítulo 3")

# El componente .tabla-ranking llegó aquí con `retropropaga_ranking.py`, después
# de que se escribieran las fuentes de `cap4/`. Reejecutar este script sin estas
# comprobaciones borraba la tabla en silencio (ocurrió el 2026-07-30): el CSS y
# los ayudantes compartidos se heredan del capítulo 3 y sobreviven, pero la
# instancia vive en una plantilla de módulo y su registro en `chapter.js`, que
# son justo las dos regiones que el ensamblado sustituye.
fallos += comprueba_tabla_ranking(html, "rejilla-nilo")
# Se cuenta el TÍTULO de la instancia y la CLAVE del registro, no el contenedor
# ni la cadena `TABLAS_RANKING` a secas: el JavaScript heredado documenta el
# componente con un ejemplo (`TABLAS_RANKING['id'] = {`) dentro de un comentario,
# y contar la cadena suelta daría un falso positivo. Mismo fallo que ya se
# aprendió con las cajas de derivación.
for pieza, esperadas in [
        ('<p class="tabla-ranking-titulo">Los 27 modelos del Nilo, '
         'con su n efectivo a la vista</p>', 1),
        ("TABLAS_RANKING['rejilla-nilo']", 1),
        # Maquinaria compartida, heredada del capítulo 3
        (".tabla-ranking {", 1), (".tabla-ranking-marco {", 1),
        ("function pintarTablaRanking", 1), ("function iniciarTablasRanking", 1),
        ("const TABLAS_RANKING", 1), ("        iniciarTablasRanking();", 1)]:
    if html.count(pieza) != esperadas:
        fallos.append(f"tabla de ranking: '{pieza[:60]}' aparece {html.count(pieza)} "
                      f"veces, se esperaban {esperadas}")

# Componentes heredados que deben seguir intactos
for regla in [".derivacion {", ".ciclo-boton {", ".quiz {", ".simulador-lectura",
              ".ejercicio-guiado {", ".grafico-etiqueta", ".simulador-intro",
              ".control-selector", ".control-interruptor"]:
    if regla not in html:
        fallos.append(f"se perdió la regla CSS {regla}")
for fn in ["function crearGraficoBarras", "function calcularPACF", "function crearSelector",
           "function crearInterruptores", "function iniciarDerivaciones",
           "function renderAutoevaluacion", "function iniciarEjerciciosGuiados"]:
    if html.count(fn) != 1:
        fallos.append(f"el ayudante '{fn}' no aparece exactamente una vez")

# Nada del capítulo anterior debe sobrevivir. El simulacro del Módulo 11 queda
# fuera de esta búsqueda: sus preguntas son del capítulo 3 a propósito (P06 cita
# las manchas solares del 3.9) y su prosa enlaza ese capítulo.
sin_simulacro = html
if sin_simulacro.count('<template id="module-11">') == 1:
    i = sin_simulacro.index('<template id="module-11">')
    sin_simulacro = sin_simulacro[:i] + sin_simulacro[sin_simulacro.index("</template>", i):]
if sin_simulacro.count("    // [inicio · simulacro del quiz]") == 1:
    i = sin_simulacro.index("    // [inicio · simulacro del quiz]")
    sin_simulacro = sin_simulacro[:i] + sin_simulacro[sin_simulacro.index("    // [fin · simulacro del quiz]", i):]
for resto in ["DATOS_CAP3", "SERIES_CAP3", "AUTOEVALUACIONES['cap3']", "PROCESOS",
              "MANCHAS", "RETORNOS", "manchas solares", "Capítulo 3 —",
              "genera_cap3.R", "capitulo-3",
              "AUTOEVALUACIONES['parcial2']", 'data-quiz="parcial2"',
              # El simulacro del capítulo 3: su registro y su contenedor. El
              # componente sí sigue (este capítulo tiene el suyo).
              "cap3-simulacro", "capítulo 2 y módulos 3.1–3.4"]:
    if resto in sin_simulacro:
        fallos.append(f"queda material del capítulo 3: '{resto}'")

# El simulacro del Módulo 11: una variante entera del quiz, SIN CLAVE. El
# contenedor y la prosa están en `cap4/templates_11.html`; el motor y el
# registro, en `cap4/chapter.js` —el registro entre marcadores, escrito por
# `exporta_simulacro.py` fuera del repositorio—, y el CSS, heredado del 3 más
# `componentes/simulacro_respuestas.css`. Se cuenta cada pieza: perderla dejaría
# el módulo vacío y duplicarla pintaría dos relojes sobre el mismo estado.
for pieza in ['<div class="simulacro" data-simulador="cap4-simulacro">',
              "SIMULACROS['cap4-simulacro']", "const SIMULACROS = {};",
              "const ESTADO_SIMULACRO = {};", "const FORMAS_SIMULACRO = {",
              "function pintarSimulacro(", ".simulacro {", ".simulacro-opcion {",
              ".simulacro-filas {", ".simulacro-fila-orden {",
              "    /* ------------------- fin del componente .simulacro ------------------- */",
              "    /* -------------- fin de las respuestas del .simulacro -------------- */",
              "    // [inicio · simulacro del quiz]",
              "    // [fin · simulacro del quiz]",
              '<div class="simulacro-preguntas"></div>',
              'class="simulacro-empezar"', 'class="simulacro-reloj"',
              'class="simulacro-conteo"', 'class="simulacro-borrar"',
              'class="simulacro-resumen"']:
    if html.count(pieza) != 1:
        fallos.append(f"simulacro del quiz: '{pieza}' aparece {html.count(pieza)} "
                      f"veces, se esperaba 1")

# Y lo que NO puede llevar: la clave. El registro publica enunciados, opciones,
# filas y respuestas posibles; si alguna vez alguien pega ahí la salida del
# banco con retroalimentación, esto lo para antes de que el capítulo se publique.
if html.count("SIMULACROS['cap4-simulacro']") == 1 and html.count("    // [fin · simulacro del quiz]") == 1:
    registro = html[html.index("SIMULACROS['cap4-simulacro']"):
                    html.index("    // [fin · simulacro del quiz]")]
    for pista in ("correcta:", "retro:", "clave:", "Correcto.", "Correcta:", "Falsa:",
                  "Cierta.", "retroFallo", "retroAcierto", "✔"):
        if pista in registro:
            fallos.append(f"el simulacro publica «{pista}»: eso es la clave")

# El Módulo 12 presenta el preparcial del Corte II, que es una página aparte
# (`preparcial-corte-2.html`). El enlace es plano, como todos los del sitio: en
# gh-pages los archivos viven en la raíz. Si alguna vez se borra o se duplica,
# el capítulo deja de llevar al preparcial sin ningún error a la vista.
if html.count('<a class="usta-button" href="preparcial-corte-2.html">') != 1:
    fallos.append("el Módulo 12 no enlaza exactamente una vez el preparcial del Corte II")
if html.count('<template id="module-13">'):
    fallos.append("sobra una plantilla module-13")

# Datos del capítulo 4 presentes
for dato in ["const DATOS_CAP4", "const SERIES_CAP4", "genera_cap4.R"]:
    if html.count(dato) != 1:
        fallos.append(f"'{dato}' no aparece exactamente una vez")

# Derivaciones: las tres del capítulo, con su andamiaje. Se cuenta el marcado
# real (contenedor + botón) y no la cadena suelta, porque el JavaScript
# heredado documenta el componente con un ejemplo dentro de un comentario.
n_der = len(re.findall(r'<div class="derivacion">\s*\n\s*<button', html))
if n_der != 3:
    fallos.append(f"hay {n_der} cajas de derivación, se esperaban 3")
n_paneles_der = len(re.findall(r'<div class="derivacion-panel" id="[^"]+" hidden>', html))
if n_paneles_der != 3:
    fallos.append(f"hay {n_paneles_der} paneles de derivación, se esperaban 3")

# Ejercicios guiados con sus dos desplegables cada uno
n_ej = html.count('<div class="ejercicio-guiado">')
if n_ej != 3:
    fallos.append(f"hay {n_ej} ejercicios guiados, se esperaban 3")
for k in (1, 2, 3):
    for suf in ("pista", "sol"):
        if html.count(f'id="c4e{k}-{suf}"') != 1:
            fallos.append(f"falta el panel c4e{k}-{suf}")

if fallos:
    raise SystemExit("ABORTA:\n  - " + "\n  - ".join(fallos))

CAP4.write_text(html, encoding="utf-8")
print(f"OK  {CAP4.name} escrito ({len(html.encode('utf-8')) / 1024:.1f} KB)")
print(f"    12 plantillas · {len(SIMULADORES)} simuladores · 3 derivaciones · "
      f"3 ejercicios · 8 preguntas de autoevaluación · 1 tabla de ranking · "
      f"simulacro del quiz")
