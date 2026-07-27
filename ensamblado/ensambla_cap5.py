#!/usr/bin/env python3
"""Construye el Capítulo 5 a partir del Capítulo 4, por sustitución de regiones.

Mismo método que `ensambla_cap4.py` (ver el README de esta carpeta): se parte
de un capítulo que ya funciona y se cambian regiones delimitadas, de modo que
todo lo que no se toca —CSS, ayudantes de JavaScript, componentes, andamiaje—
se conserva por construcción.

Novedad respecto al capítulo 4: este script además **instala el componente
`.mapa-estacional`** en la región compartida (CSS, JavaScript y la llamada de
`loadModule`), porque es nuevo en este capítulo. `retropropaga_mapa.py` hace lo
mismo sobre el capítulo 1 y la plantilla.

Uso:  python3 ensambla_cap5.py       (desde ensamblado/)
"""

import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
CAP4 = RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
CAP5 = RAIZ / "Htmls_Series" / "capitulo-5-sarima.html"
FUENTES = AQUI / "cap5"
COMPONENTES = AQUI / "componentes"
SALIDAS = RAIZ / "precalculo" / "salidas"

sys.path.insert(0, str(COMPONENTES))
from ciclo_html import ciclo_html, comprueba_ciclo                    # noqa: E402
from mapa_estacional_html import (mapa_estacional_html,               # noqa: E402
                                  comprueba_mapa_estacional)


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


html = lee(CAP4)

# ---------------------------------------------------------------------------
# 1. Metadatos de la cabecera
# ---------------------------------------------------------------------------
html = una_vez(
    html,
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 4: '
    'modelos ARIMA y metodología de Box–Jenkins; el orden de integración d, '
    'identificación, criterios de información, el algoritmo de Hyndman–Khandakar, '
    'diagnóstico, sobrediferenciación y pronóstico con intervalos.">',
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 5: '
    'modelos SARIMA; firma estacional en ACF y PACF, notación multiplicativa, '
    'diferenciación estacional, el modelo airline, regresores de calendario, '
    'regresión armónica con términos de Fourier y comparación con ETS.">',
    "meta description")

html = una_vez(
    html,
    'content="series de tiempo, ARIMA, Box-Jenkins, orden de integración, '
    'diferenciación, raíz unitaria, KPSS, ADF, auto.arima, Hyndman-Khandakar, AICc, '
    'BIC, sobrediferenciación, intervalos de pronóstico, pesos psi, Nilo, TRM, R, Python"',
    'content="series de tiempo, SARIMA, estacionalidad, diferencia estacional, '
    'modelo airline, ACF estacional, rezagos satélite, nsdiffs, SARIMAX, regresores '
    'de calendario, Semana Santa, términos de Fourier, regresión armónica, STL, ETS, '
    'AirPassengers, USAccDeaths, TRM, R, Python"',
    "meta keywords")

html = una_vez(
    html,
    "<title>Series de Tiempo · Capítulo 4 — Modelos ARIMA y Box–Jenkins</title>",
    "<title>Series de Tiempo · Capítulo 5 — Modelos SARIMA</title>",
    "title")

html = una_vez(
    html,
    'style="margin:0; text-align:left;">CAPÍTULO 4 •',
    'style="margin:0; text-align:left;">CAPÍTULO 5 •',
    "cintillo de la cabecera")

html = una_vez(
    html, "MODELOS ARIMA Y BOX–JENKINS", "MODELOS SARIMA",
    "subtítulo de la cabecera")

# ---------------------------------------------------------------------------
# 2. Instalación del componente .mapa-estacional (CSS, JS y llamada de arranque)
# ---------------------------------------------------------------------------
if ".mapa-estacional {" in html:
    raise SystemExit("ABORTA: el capítulo 4 ya trae el componente .mapa-estacional; "
                     "este script está escrito contra el estado anterior.")

ancla_css = """      .ciclo-etapa:not(:last-child)::after {
        content: "\\2193";
        align-self: center;
        margin: 0.15rem 0;
      }
    }
  </style>"""
html = una_vez(html, ancla_css,
               ancla_css.replace("  </style>",
                                 lee(COMPONENTES / "mapa_estacional.css").rstrip("\n")
                                 + "\n  </style>"),
               "CSS del mapa estacional")

ancla_js = """        const inicial = botones.findIndex(b => b.getAttribute('aria-selected') === 'true');
        seleccionar(inicial >= 0 ? inicial : 0, false);
      });
    }
"""
html = una_vez(html, ancla_js,
               ancla_js + "\n" + lee(COMPONENTES / "mapa_estacional.js").rstrip("\n") + "\n",
               "JavaScript del mapa estacional")

html = una_vez(html, "        iniciarCiclos();\n",
               "        iniciarCiclos();\n        iniciarMapasEstacionales();\n",
               "llamada de arranque del mapa estacional")

# ---------------------------------------------------------------------------
# 3. Las once plantillas de módulo
# ---------------------------------------------------------------------------
ETAPAS_CICLO = [
    {
        "clave": "transformar",
        "numero": "Etapa 1",
        "titulo": "Transformar",
        "resumen": "¿Log o Box–Cox?",
        "campos": [
            ("Qué haces", "<p>Miras si la amplitud del patrón estacional crece con el nivel. "
                          "Si crece, la estacionalidad es multiplicativa y hay que pasarla a "
                          "aditiva antes de modelar.</p>"),
            ("Con qué", "<p>El mapa mes × año del Módulo 1, <code>ggseasonplot()</code> y, si "
                        "hace falta un número, <code>BoxCox.lambda()</code>.</p>"),
        ],
        "vuelta": "<p>Si al final los residuales tienen varianza creciente, la transformación "
                  "estaba mal elegida y hay que volver aquí, no añadir parámetros.</p>",
    },
    {
        "clave": "elegir-D",
        "numero": "Etapa 2",
        "titulo": "Elegir $D$",
        "resumen": "Primero la estacional",
        "campos": [
            ("Qué haces", "<p>Decides cuántas diferencias <strong>estacionales</strong> hacen "
                          "falta. Casi siempre $D \\in \\{0, 1\\}$; $D = 2$ es rarísimo.</p>"),
            ("Con qué", "<p><code>nsdiffs()</code> —comprobando qué prueba usa— y la ACF en "
                        "$m, 2m, 3m$: si decae despacio, falta $\\nabla_m$.</p>"),
        ],
        "vuelta": "<p>Si al estimar sale $\\hat\\Theta$ pegado a $-1$ y la raíz MA sobre el "
                  "círculo unitario, sobraba una diferencia estacional.</p>",
    },
    {
        "clave": "elegir-d",
        "numero": "Etapa 3",
        "titulo": "Elegir $d$",
        "resumen": "Sobre la serie ya sin estación",
        "campos": [
            ("Qué haces", "<p>Decides las diferencias regulares <strong>sobre la serie a la que "
                          "ya has aplicado $\\nabla_m^D$</strong>. Este es el paso que más se "
                          "hace en el orden equivocado.</p>"),
            ("Con qué", "<p><code>ndiffs(diff(y, lag = m))</code>, la varianza de las cuatro "
                        "combinaciones, y KPSS o ADF sobre la serie desestacionalizada.</p>"),
        ],
        "vuelta": "<p>Si $\\hat\\theta \\to -1$, sobra la diferencia regular. Si la varianza "
                  "sube al diferenciar, también.</p>",
    },
    {
        "clave": "identificar",
        "numero": "Etapa 4",
        "titulo": "Identificar los cuatro órdenes",
        "resumen": "$(p,q)$ abajo, $(P,Q)$ en $m$",
        "campos": [
            ("Qué haces", "<p>Lees $(p, q)$ en los rezagos bajos y $(P, Q)$ en $m, 2m, 3m$, con "
                          "la misma tabla de identificación del Capítulo 3 aplicada dos veces.</p>"),
            ("Con qué", "<p>ACF y PACF de la serie ya estacionaria, con al menos $3m$ rezagos. "
                        "<strong>No cuentes los satélites</strong> de $m\\pm 1$: los genera la "
                        "multiplicación de polinomios, no hacen falta parámetros para ellos.</p>"),
        ],
        "vuelta": "<p>Si el diagnóstico deja una barra grande justo en el rezago $m$, faltaba "
                  "$P$ o $Q$; si la deja en los primeros rezagos, faltaba $p$ o $q$.</p>",
    },
    {
        "clave": "diagnosticar",
        "numero": "Etapa 5",
        "titulo": "Estimar y diagnosticar",
        "resumen": "Ljung–Box con $2m$",
        "campos": [
            ("Qué haces", "<p>Estimas por máxima verosimilitud y compruebas los residuales. La "
                          "rejilla de candidatos solo se ordena por AICc si <strong>todos "
                          "comparten $d$ y $D$</strong>.</p>"),
            ("Con qué", "<p><code>Arima()</code> o <code>auto.arima()</code>; Ljung–Box con al "
                        "menos $2m$ rezagos, el correlograma barra por barra en $m$ y $2m$, y "
                        "los módulos de las raíces.</p>"),
        ],
        "vuelta": "<p>Cualquier fallo aquí te devuelve a la etapa que lo causó: varianza "
                  "creciente a la 1, raíz sobre el círculo a la 2 o la 3, barra en $m$ a la 4.</p>",
    },
]

plantillas_viejas = entre(html, '  <template id="module-1">',
                          "  </template>\n\n  <script>", "plantillas")
plantillas_nuevas = (
    lee(FUENTES / "templates_1_3.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_4_6.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_7_9.html").rstrip("\n") + "\n\n" +
    lee(FUENTES / "templates_10_11.html").rstrip("\n") + "\n\n  <script>"
)

# Los componentes se generan con su constructor, no a mano: así el marcado es
# idéntico al de las otras instancias del proyecto y la comparación de
# selectores CSS no encuentra diferencias.
MAPAS = {
    "firma": ("Mapa mes × año", ""),
}
for clave, (titulo, nota) in MAPAS.items():
    marca = f"<!--MAPA:{clave}|{titulo}|{nota}-->"
    if plantillas_nuevas.count(marca) != 1:
        raise SystemExit(f"ABORTA [mapa {clave}]: el marcador aparece "
                         f"{plantillas_nuevas.count(marca)} veces")
    plantillas_nuevas = plantillas_nuevas.replace(
        "        " + marca,
        mapa_estacional_html(clave, titulo, nota, sangria="        ").rstrip("\n"), 1)

marca_ciclo = "<!--CICLO:identificacion-estacional-->"
if plantillas_nuevas.count(marca_ciclo) != 1:
    raise SystemExit("ABORTA [ciclo]: el marcador no aparece exactamente una vez")
plantillas_nuevas = plantillas_nuevas.replace(
    "      " + marca_ciclo,
    ciclo_html("identificacion-estacional", ETAPAS_CICLO,
               "El ciclo no es una lista: cada fallo del diagnóstico te devuelve a la etapa "
               "que lo causó, y la etapa 3 depende de haber hecho bien la 2.",
               sangria="      ").rstrip("\n"), 1)

html = una_vez(html, plantillas_viejas, plantillas_nuevas, "plantillas de módulo")

# ---------------------------------------------------------------------------
# 4. courseData
# ---------------------------------------------------------------------------
course_viejo = entre(html, "    const courseData = {", "    };", "courseData")
course_nuevo = """    const courseData = {
      title: "Series de Tiempo",
      modules: [
        { id: 1, title: "La firma de la estacionalidad", shortTitle: "Firma estacional", duration: "14 min" },
        { id: 2, title: "Notación SARIMA y polinomio multiplicativo", shortTitle: "Notación", duration: "12 min" },
        { id: 3, title: "Diferenciación estacional", shortTitle: "Diferenciar", duration: "16 min" },
        { id: 4, title: "Identificar los órdenes estacionales", shortTitle: "Identificar P,Q", duration: "16 min" },
        { id: 5, title: "El modelo airline", shortTitle: "Airline", duration: "14 min" },
        { id: 6, title: "Estimar, comparar y diagnosticar", shortTitle: "Explorador", duration: "16 min" },
        { id: 7, title: "Caso completo: AirPassengers", shortTitle: "Caso completo", duration: "18 min" },
        { id: 8, title: "Segundo caso y contraejemplo", shortTitle: "Contraejemplo", duration: "16 min" },
        { id: 9, title: "Regresores de calendario y SARIMAX", shortTitle: "Calendario", duration: "14 min" },
        { id: 10, title: "Cuando m es grande: Fourier y STL", shortTitle: "Fourier y STL", duration: "16 min" },
        { id: 11, title: "Panorama comparativo y cierre", shortTitle: "Cierre", duration: "20 min" }
      ]
    };"""
html = una_vez(html, course_viejo, course_nuevo, "courseData")

# ---------------------------------------------------------------------------
# 5. Los datos precalculados
# ---------------------------------------------------------------------------
inicio_datos = "    // Generado por precalculo/genera_cap4.R"
if html.count(inicio_datos) != 1:
    raise SystemExit("ABORTA [datos]: no encuentro el comentario del precálculo del cap. 4")
i = html.index(inicio_datos)
if html.count("    const SERIES_CAP4 = ") != 1:
    raise SystemExit("ABORTA [datos]: SERIES_CAP4 no aparece exactamente una vez")
j = html.index("\n", html.index("    const SERIES_CAP4 = ", i)) + 1
datos_nuevos = "".join(
    "    " + linea if linea.strip() else linea
    for linea in lee(SALIDAS / "cap5_datos.js").splitlines(keepends=True))
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
    "mapa-firma", "constructor-polinomio", "cuatro-combinaciones",
    "sobrediferenciacion-estacional", "firma-teorica", "airline-pesos",
    "explorador-sarima", "pronostico-estacional", "contraejemplo-trm",
    "calendario-regresores", "armonicos-K", "comparativa-particion",
]

for n in range(1, 12):
    if html.count(f'<template id="module-{n}">') != 1:
        fallos.append(f"la plantilla module-{n} no aparece exactamente una vez")
if html.count('<template id="module-12">') != 0:
    fallos.append("ha quedado una plantilla module-12")

for sim in SIMULADORES:
    if html.count(f"SIMULADORES['{sim}']") != 1:
        fallos.append(f"el simulador '{sim}' no está registrado exactamente una vez")
    if html.count(f'data-simulador="{sim}"') != 1:
        fallos.append(f"el contenedor de '{sim}' no aparece exactamente una vez")

# Andamiaje del quiz: renderAutoevaluacion() lanza excepción si falta alguno.
for pieza in ['<div class="quiz" data-quiz="cap5">', 'class="quiz-preguntas"',
              'class="quiz-progreso-barra"', 'class="quiz-resumen"',
              'class="quiz-conteo"', 'class="quiz-reiniciar"']:
    if html.count(pieza) != 1:
        fallos.append(f"andamiaje del quiz: '{pieza}' aparece {html.count(pieza)} veces")
if html.count("AUTOEVALUACIONES['cap5']") != 1:
    fallos.append("AUTOEVALUACIONES['cap5'] no aparece exactamente una vez")

# Componente .ciclo: se hereda, y aquí tiene su propia instancia de 5 etapas
fallos += comprueba_ciclo(html, "identificacion-estacional", 5)
if html.count("function iniciarCiclos()") != 1 or html.count("        iniciarCiclos();") != 1:
    fallos.append("el componente .ciclo no se heredó bien del capítulo 4")

# Componente .mapa-estacional: nuevo, hay que comprobar las tres piezas
fallos += comprueba_mapa_estacional(html, "firma")
# `.mapa-estacional-rejilla` y `.mapa-estacional-celda` salen dos veces a
# propósito: la segunda es la sobreescritura de la media query de móvil.
for pieza, esperadas in [(".mapa-estacional {", 1), (".mapa-estacional-rejilla {", 2),
                         (".mapa-estacional-celda {", 2), (".mapa-estacional-vacia {", 1),
                         (".mapa-estacional-leyenda {", 1), (".mapa-estacional-nota {", 1),
                         ("function pintarMapaEstacional", 1),
                         ("function iniciarMapasEstacionales", 1),
                         ("const MAPAS_ESTACIONALES", 1),
                         ("        iniciarMapasEstacionales();", 1)]:
    if html.count(pieza) != esperadas:
        fallos.append(f"mapa estacional: '{pieza}' aparece {html.count(pieza)} veces, "
                      f"se esperaban {esperadas}")

# Componentes heredados que deben seguir intactos
for regla in [".derivacion {", ".ciclo-boton {", ".quiz {", ".simulador-lectura",
              ".ejercicio-guiado {", ".grafico-etiqueta", ".simulador-intro",
              ".control-selector", ".control-interruptor"]:
    if regla not in html:
        fallos.append(f"se perdió la regla CSS {regla}")
for fn in ["function crearGraficoBarras", "function calcularPACF", "function crearSelector",
           "function crearInterruptores", "function iniciarDerivaciones",
           "function renderAutoevaluacion", "function iniciarEjerciciosGuiados",
           "function diferenciar(y, veces)"]:
    if html.count(fn) != 1:
        fallos.append(f"el ayudante '{fn}' no aparece exactamente una vez")

# Nada del capítulo anterior debe sobrevivir
for resto in ["DATOS_CAP4", "SERIES_CAP4", "AUTOEVALUACIONES['cap4']", "genera_cap4.R",
              "capitulo-4", "Capítulo 4 —", "data-ciclo=\"box-jenkins\"",
              "SIMULADORES['nilo-y-diferencia']", "SIMULADORES['explorador-modelos']"]:
    if resto in html:
        fallos.append(f"queda material del capítulo 4: '{resto}'")

# Datos del capítulo 5 presentes
for dato in ["const DATOS_CAP5", "const SERIES_CAP5", "genera_cap5.R"]:
    if html.count(dato) != 1:
        fallos.append(f"'{dato}' no aparece exactamente una vez")

# Derivaciones: se cuenta el marcado real (contenedor + botón), no la cadena
# suelta, porque el JavaScript heredado documenta el componente con un ejemplo
# dentro de un comentario.
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
        if html.count(f'id="c5e{k}-{suf}"') != 1:
            fallos.append(f"falta el panel c5e{k}-{suf}")

# No deben quedar marcadores de plantilla sin expandir
for marca in re.findall(r"<!--(?:MAPA|CICLO):[^>]*-->", html):
    fallos.append(f"marcador sin expandir: {marca}")

if fallos:
    raise SystemExit("ABORTA:\n  - " + "\n  - ".join(fallos))

CAP5.write_text(html, encoding="utf-8")
print(f"OK  {CAP5.name} escrito ({len(html.encode('utf-8')) / 1024:.1f} KB)")
print(f"    11 plantillas · {len(SIMULADORES)} simuladores · 3 derivaciones · "
      f"3 ejercicios · 8 preguntas de autoevaluación · componente .mapa-estacional instalado")
