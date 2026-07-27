#!/usr/bin/env python3
"""
Ensambla Htmls_Series/capitulo-3-modelos-ar-ma-arma.html.

Método: se PARTE del capítulo 2 y se sustituyen regiones bien delimitadas.
No se concatena a partir de fragmentos sueltos, precisamente porque así se
perdió un bloque de CSS entero al montar el capítulo 2.

Toda sustitución pasa por reemplazar(), que aborta si el marcador no aparece
exactamente una vez, y al final se comprueba que el resultado contiene todo
lo que debe contener.
"""
import json
import pathlib
import re
import sys

BASE = pathlib.Path("/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo")
SCRATCH = pathlib.Path("/private/tmp/claude-501/-Users-javiermauriciosierra-Documents-Trabajo-2026-Bosque-2026/831bcb00-26c3-43d4-8bd7-3dd033784b31/scratchpad")

ORIGEN = BASE / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html"
DESTINO = BASE / "Htmls_Series" / "capitulo-3-modelos-ar-ma-arma.html"

sustituciones = 0


def reemplazar(texto, viejo, nuevo, etiqueta):
    """Sustituye exigiendo que el marcador aparezca exactamente una vez."""
    global sustituciones
    n = texto.count(viejo)
    if n != 1:
        sys.exit(f"ABORTA [{etiqueta}]: el marcador aparece {n} veces, se esperaba 1")
    sustituciones += 1
    return texto.replace(viejo, nuevo, 1)


def recortar(texto, inicio, fin, nuevo, etiqueta):
    """Sustituye toda la región entre dos marcadores (ambos únicos)."""
    global sustituciones
    for m in (inicio, fin):
        if texto.count(m) != 1:
            sys.exit(f"ABORTA [{etiqueta}]: marcador no único -> {m[:70]!r}")
    i = texto.index(inicio)
    j = texto.index(fin)
    if j <= i:
        sys.exit(f"ABORTA [{etiqueta}]: los marcadores están en orden inverso")
    sustituciones += 1
    return texto[:i] + nuevo + texto[j:]


html = ORIGEN.read_text(encoding="utf-8")
original_len = len(html)

# ---------------------------------------------------------------------------
# 1. Metadatos de la cabecera
# ---------------------------------------------------------------------------
html = reemplazar(
    html,
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 2: '
    'Estacionariedad, ACF/PACF, pruebas de raíz unitaria (ADF y KPSS), '
    'diferenciación y transformaciones de Box–Cox.">',
    'content="Material de estudio autónomo de Series de Tiempo — Capítulo 3: '
    'modelos AR, MA y ARMA; operador de rezago, estacionariedad e invertibilidad, '
    'identificación con ACF/PACF, estimación y diagnóstico de residuales.">',
    "meta description")

html = reemplazar(
    html,
    '<meta name="keywords" content="series de tiempo, estacionariedad, ACF, PACF, '
    'correlograma, ruido blanco, caminata aleatoria, raíz unitaria, ADF, KPSS, '
    'diferenciación, Box-Cox, R, Python">',
    '<meta name="keywords" content="series de tiempo, AR, MA, ARMA, operador de rezago, '
    'polinomio característico, invertibilidad, Yule-Walker, máxima verosimilitud, AIC, AICc, '
    'BIC, Ljung-Box, manchas solares, R, Python">',
    "meta keywords")

html = reemplazar(
    html,
    "<title>Series de Tiempo · Capítulo 2 — Estacionariedad, ACF y PACF</title>",
    "<title>Series de Tiempo · Capítulo 3 — Modelos AR, MA y ARMA</title>",
    "title")

html = reemplazar(
    html,
    'style="margin:0; text-align:left;">CAPÍTULO 2 •\n              ESTACIONARIEDAD, ACF Y PACF • UNBOSQUE</p>',
    'style="margin:0; text-align:left;">CAPÍTULO 3 •\n              MODELOS AR, MA Y ARMA • UNBOSQUE</p>',
    "subtítulo de la cabecera")

html = reemplazar(
    html,
    'Series de Tiempo • Capítulo 2 • UnBosque 2026',
    'Series de Tiempo • Capítulo 3 • UnBosque 2026',
    "pie de página")

# ---------------------------------------------------------------------------
# 2. CSS del componente .derivacion (idéntico al de la plantilla)
# ---------------------------------------------------------------------------
css_derivacion = (SCRATCH / "derivacion.css").read_text(encoding="utf-8")
html = reemplazar(
    html,
    "    /* Enunciado de una pregunta con gráfico: mismo criterio de separación */\n"
    "    .quiz-pregunta .quiz-enunciado + .quiz-grafico {\n"
    "      margin-top: 0.9rem;\n"
    "    }\n"
    "  </style>",
    "    /* Enunciado de una pregunta con gráfico: mismo criterio de separación */\n"
    "    .quiz-pregunta .quiz-enunciado + .quiz-grafico {\n"
    "      margin-top: 0.9rem;\n"
    "    }\n\n"
    + css_derivacion.rstrip("\n") + "\n  </style>",
    "CSS de .derivacion")

# ---------------------------------------------------------------------------
# 3. crearGraficoBarras: barras adicionales (teórica frente a muestral)
# ---------------------------------------------------------------------------
html = reemplazar(
    html,
    """      (opciones.lineas || []).forEach(linea => {
        datasets.push({
          type: 'line',""",
    """      // Barras adicionales sobre el mismo eje (p. ej. la ACF muestral junto a
      // la teórica). Van antes que las rectas de referencia para que el orden
      // de los datasets sea estable: 0 = principal, 1..k = extra, luego líneas.
      (opciones.barrasExtra || []).forEach(extra => {
        datasets.push({
          type: 'bar',
          label: extra.etiqueta || '',
          data: extra.valores,
          backgroundColor: extra.color || COLORES_GRAFICO.secundario,
          borderWidth: 0,
          barPercentage: 0.4,
          categoryPercentage: 0.9,
          order: 2
        });
      });
      (opciones.lineas || []).forEach(linea => {
        datasets.push({
          type: 'line',""",
    "crearGraficoBarras con barrasExtra")

# ---------------------------------------------------------------------------
# 4. Los diez módulos
# ---------------------------------------------------------------------------
plantillas = "\n".join(
    (SCRATCH / n).read_text(encoding="utf-8").rstrip("\n")
    for n in ("cap3_mod1_5.html", "cap3_mod6_10.html", "cap3_mod10.html")
) + "\n\n"

html = recortar(
    html,
    "  <!-- ============================================================ -->\n"
    "  <!-- MÓDULO 1 · Estacionariedad",
    "  <script>\n"
    "    // ================================================================\n"
    "    // Configuración del capítulo",
    plantillas,
    "bloque de plantillas")

# ---------------------------------------------------------------------------
# 5. courseData
# ---------------------------------------------------------------------------
html = recortar(
    html,
    "      modules: [\n",
    "      ]\n    };",
    """      modules: [
        { id: 1, title: "Operador de rezago", shortTitle: "Operador B", duration: "12 min" },
        { id: 2, title: "Procesos AR(p)", shortTitle: "AR(p)", duration: "14 min" },
        { id: 3, title: "Procesos MA(q)", shortTitle: "MA(q)", duration: "12 min" },
        { id: 4, title: "Dualidad AR ↔ MA", shortTitle: "Dualidad", duration: "12 min" },
        { id: 5, title: "ARMA e identificación", shortTitle: "ARMA", duration: "14 min" },
        { id: 6, title: "Simular y reconocer procesos", shortTitle: "Simulación", duration: "10 min" },
        { id: 7, title: "Estimación de parámetros", shortTitle: "Estimación", duration: "14 min" },
        { id: 8, title: "Criterios de información y diagnóstico", shortTitle: "Diagnóstico", duration: "14 min" },
        { id: 9, title: "Dos casos reales", shortTitle: "Casos reales", duration: "16 min" },
        { id: 10, title: "Cierre, resumen y autoevaluación", shortTitle: "Cierre", duration: "12 min" }
""",
    "courseData.modules")

# ---------------------------------------------------------------------------
# 6. Datos precalculados
# ---------------------------------------------------------------------------
datos_js = (BASE / "precalculo" / "salidas" / "cap3_datos.js").read_text(encoding="utf-8")
# El .js trae el JSON con la cabecera de comentarios ya puesta; se indenta para
# que quede alineado dentro del <script>.
datos_indentado = "\n".join(
    ("    " + linea if linea.strip() else linea) for linea in datos_js.rstrip("\n").split("\n")
)

i = html.index("    // Generado por precalculo/genera_cap2.R")
j = html.index("    // ================================================================\n"
               "    // Estado y elementos del DOM")
html = html[:i] + datos_indentado + "\n" + html[j:]
sustituciones += 1

# ---------------------------------------------------------------------------
# 7. Enganche y función de las derivaciones plegables
# ---------------------------------------------------------------------------
html = reemplazar(
    html,
    "        iniciarEjerciciosGuiados();\n",
    "        iniciarEjerciciosGuiados();\n        iniciarDerivaciones();\n",
    "llamada a iniciarDerivaciones")

js_derivacion = (SCRATCH / "derivacion.js").read_text(encoding="utf-8")
html = reemplazar(
    html,
    """          if (!abierto) {
            if (typeof Prism !== 'undefined') Prism.highlightAllUnder(panel);
            katexEn(panel);
          }
        });
      });
    }
""",
    """          if (!abierto) {
            if (typeof Prism !== 'undefined') Prism.highlightAllUnder(panel);
            katexEn(panel);
          }
        });
      });
    }

""" + js_derivacion.rstrip("\n") + "\n",
    "función iniciarDerivaciones")

# ---------------------------------------------------------------------------
# 8. JavaScript propio del capítulo (simuladores y autoevaluación)
# ---------------------------------------------------------------------------
js_cap3 = (SCRATCH / "cap3_js.js").read_text(encoding="utf-8")
html = recortar(
    html,
    "    // ================================================================\n"
    "    // Series de trabajo del capítulo, tomadas del precálculo en R",
    "  </script>\n\n</body>",
    js_cap3.rstrip("\n") + "\n",
    "JavaScript del capítulo")

# ---------------------------------------------------------------------------
# 9. Comprobaciones finales: nada de lo que debe estar puede faltar
# ---------------------------------------------------------------------------
obligatorios = {
    "10 plantillas de módulo": [f'<template id="module-{k}">' for k in range(1, 11)],
    "9 simuladores registrados": [
        f"SIMULADORES['{s}']" for s in (
            "panel-ar-teorico", "triangulo-ar2", "panel-ma-teorico", "dualidad-psi-pi",
            "laboratorio-arma", "teorica-vs-muestral", "manchas-identificacion",
            "diagnostico-residuales", "manchas-transformada", "trm-retornos")
    ],
    "contenedores de simulador": [
        f'data-simulador="{s}"' for s in (
            "panel-ar-teorico", "triangulo-ar2", "panel-ma-teorico", "dualidad-psi-pi",
            "laboratorio-arma", "teorica-vs-muestral", "manchas-identificacion",
            "diagnostico-residuales", "manchas-transformada", "trm-retornos")
    ],
    # El andamiaje interno del .quiz no es decorativo: renderAutoevaluacion()
    # escribe sobre estos nodos y revienta si falta cualquiera de ellos.
    "autoevaluación": [
        "AUTOEVALUACIONES['cap3']", 'data-quiz="cap3"',
        'class="quiz-preguntas"', 'class="quiz-progreso-barra"',
        'class="quiz-resumen"', 'class="quiz-conteo"', 'class="quiz-reiniciar"',
    ],
    "componente .derivacion": [
        ".derivacion-boton {", ".derivacion-pasos > li::before {",
        "function iniciarDerivaciones()", "iniciarDerivaciones();",
        'class="derivacion-boton"',
    ],
    "datos precalculados": ["const DATOS_CAP3 =", "genera_cap3.R"],
    "helpers nuevos": ["barrasExtra", "function pesosPsi(", "function pesosPi(",
                       "function acfTeorica(", "function analizarAR(", "function esInvertible("],
    "ejercicios guiados": ["c3e1-sol", "c3e2-sol", "c3e3-sol"],
    "CSS heredado del capítulo 2": [
        ".quiz {", ".quiz-opcion {", ".simulador-lectura {", ".control-selector {",
        ".control-interruptor {", ".ejercicio-guiado {", ".grafico-etiqueta {",
    ],
}

fallos = []
for grupo, marcadores in obligatorios.items():
    for m in marcadores:
        if m not in html:
            fallos.append(f"{grupo}: falta {m!r}")

prohibidos = ["DATOS_CAP2", "SERIES_CAP2", "AUTOEVALUACIONES['cap2']",
              "Capítulo 2 • UnBosque", "genera_cap2.R"]
for p in prohibidos:
    if p in html:
        fallos.append(f"resto del capítulo 2 sin sustituir: {p!r}")

# Cada canvas de cada simulador tiene que existir: se cuentan por contenedor
for sim in re.finditer(r'<div class="simulador" data-simulador="([^"]+)">(.*?)\n      </div>',
                       html, re.S):
    if "<canvas" not in sim.group(2):
        fallos.append(f"simulador sin canvas: {sim.group(1)}")

if fallos:
    print("FALLOS DE ENSAMBLADO:")
    for f in fallos:
        print("  ✗", f)
    sys.exit(1)

DESTINO.write_text(html, encoding="utf-8")

n_plantillas = html.count('<template id="module-')
n_sim = html.count("SIMULADORES['")
n_deriv = html.count('class="derivacion-boton"')
n_r = html.count('class="language-r"')
n_py = html.count('class="language-python"')

print(f"Escrito: {DESTINO.name}")
print(f"  sustituciones aplicadas : {sustituciones}")
print(f"  tamaño capítulo 2       : {original_len:,} bytes")
print(f"  tamaño capítulo 3       : {len(html):,} bytes")
print(f"  plantillas de módulo    : {n_plantillas}")
print(f"  simuladores registrados : {n_sim}")
print(f"  cajas de derivación     : {n_deriv}")
print(f"  bloques R               : {n_r}")
print(f"  bloques Python          : {n_py}")
print("  todas las comprobaciones de integridad: OK")
