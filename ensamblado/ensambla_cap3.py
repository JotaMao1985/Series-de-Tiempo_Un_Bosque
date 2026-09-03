#!/usr/bin/env python3
"""
Ensambla Htmls_Series/capitulo-3-modelos-ar-ma-arma.html.

Método: se PARTE del capítulo 2 y se sustituyen regiones bien delimitadas.
No se concatena a partir de fragmentos sueltos, precisamente porque así se
perdió un bloque de CSS entero al montar el capítulo 2.

Toda sustitución pasa por reemplazar(), que aborta si el marcador no aparece
exactamente una vez, y al final se comprueba que el resultado contiene todo
lo que debe contener.

MODO POR DEFECTO: VERIFICAR, NO ESCRIBIR
----------------------------------------
Sin argumentos, el script ensambla en memoria y compara con el archivo que ya
existe en disco. Si coinciden, dice que el capítulo es reproducible; si no,
muestra en qué difieren y NO toca nada. Para sobrescribir hay que pedirlo:

    python3 ensambla_cap3.py --escribir

La razón es histórica y concreta: el capítulo 3 acumuló correcciones hechas
sobre el HTML (auditorías de contenido) que este script no conocía, y una
reejecución distraída las habría borrado en silencio.

ESTADO CONOCIDO (2026-09-02), medido, no supuesto
-------------------------------------------------
El capítulo 2 ha seguido evolucionando y ya trae por su cuenta tres cosas que
este script insertaba —el CSS y el JS del componente .derivacion, y el
`barrasExtra` de crearGraficoBarras—, de modo que esas secciones ya no
insertan: COMPRUEBAN que estén. El CSS de .tabla-ranking sí se inserta (2b).

Con eso, la verificación deja una sola diferencia, y conocida:

  ~179 líneas que están en el capítulo 3 y no en lo ensamblado
      El motor JS de .tabla-ranking (iniciarTablasRanking y su bloque). Está
      guardado en cap3/tabla_ranking.js, pero NO se inserta: en el capítulo 3
      va después de iniciarCiclos(), y en el capítulo 2 el orden de esos
      componentes es otro, así que no hay un marcador único donde anclarlo
      sin reordenar el capítulo 2.

La segunda diferencia que aquí se documentaba —las ~31 líneas de
moduloDelHash(), presentes en el capítulo 2 y ausentes del 3— quedó CERRADA el
2026-09-02. El capítulo 3 ignoraba los enlaces con ancla y abría siempre por el
módulo 1. El bloque se copió del capítulo 2 sin tocar una coma (el comentario,
moduloDelHash(), fijarHashDelModulo() y el oyente de hashchange), junto con las
dos líneas que lo activan: loadModule(moduloDelHash()) al arrancar y
fijarHashDelModulo(id) dentro de loadModule(). Se copió verbatim, y no
adaptado, a propósito: el bloque cae en la región que este script hereda del
capítulo 2 tal cual —cap3_js.js empieza más abajo, en las series de trabajo del
capítulo—, de modo que cualquier retoque de redacción habría reabierto la
diferencia. Comprobado por HTTP, no por file://: #modulo-6 abre el módulo 6;
#modulo-99 y la URL sin ancla abren el 1.

La diferencia que queda tiene la raíz de siempre: el modelo "derivar el
capítulo 3 parcheando el 2" se agotó, porque los dos capítulos evolucionaron
por separado y sus motores JS ya no están en el mismo orden. Reconstruir byte a
byte exigiría reordenar el capítulo 2, que es una tarea distinta y con su
propio riesgo. Por eso este script verifica y avisa en vez de escribir.

FUENTES: ensamblado/cap3/ (dentro del repositorio). Antes vivían en un
scratchpad de sesión que se borró; se recuperaron del HTML ya corregido, así
que incorporan las correcciones de las auditorías.
"""
import json
import pathlib
import re
import sys

BASE = pathlib.Path("/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo")
FUENTES = BASE / "ensamblado" / "cap3"

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
# 2. CSS del componente .derivacion
# ---------------------------------------------------------------------------
# Ya no se inserta: el capítulo 2 lo trae desde que el componente se
# retro-portó allí. Aquí solo se comprueba que efectivamente esté, porque el
# capítulo 3 lo usa en catorce cajas de derivación.
for marca in (".derivacion-boton {", ".derivacion-pasos > li::before {"):
    if marca not in html:
        sys.exit(f"ABORTA: el capítulo 2 ya no trae el CSS de .derivacion ({marca!r}). "
                 "Hay que volver a insertarlo aquí.")

# ---------------------------------------------------------------------------
# 2b. CSS del componente .tabla-ranking (propio del capítulo 3)
# ---------------------------------------------------------------------------
# Este sí hay que insertarlo: el capítulo 2 no lo tiene. Va al final del
# <style>, que es donde lo dejó la ronda que creó el componente.
css_ranking = (FUENTES / "tabla_ranking.css").read_text(encoding="utf-8")
html = reemplazar(
    html,
    "      }\n    }\n  </style>",
    "      }\n    }\n\n" + css_ranking.rstrip("\n") + "\n  </style>",
    "CSS de .tabla-ranking")

# ---------------------------------------------------------------------------
# 3. crearGraficoBarras: barras adicionales (teórica frente a muestral)
# ---------------------------------------------------------------------------
# Igual que el CSS de .derivacion: el capítulo 2 ya lo trae. Se comprueba.
if "barrasExtra" not in html:
    sys.exit("ABORTA: el capítulo 2 ya no trae `barrasExtra` en crearGraficoBarras. "
             "Los simuladores del capítulo 3 que superponen ACF teórica y muestral "
             "lo necesitan; hay que volver a insertarlo aquí.")

# ---------------------------------------------------------------------------
# 4. Los diez módulos
# ---------------------------------------------------------------------------
# Un solo archivo, extraído del HTML ya auditado: trae las correcciones de
# contenido (rejilla de once candidatos, cifras de Guerrero, ACF residual,
# derivación de Ljung-Box, etc.).
plantillas = (FUENTES / "cap3_modulos.html").read_text(encoding="utf-8")

html = recortar(
    html,
    "  <!-- ============================================================ -->\n"
    "  <!-- MÓDULO 1 ·",
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
# Tercera pieza que el capítulo 2 ya trae: la función y su llamada. Se comprueba.
for marca in ("function iniciarDerivaciones()", "iniciarDerivaciones();"):
    if marca not in html:
        sys.exit(f"ABORTA: el capítulo 2 ya no trae {marca!r}. "
                 "Las derivaciones plegables del capítulo 3 no funcionarían.")

# ---------------------------------------------------------------------------
# 8. JavaScript propio del capítulo (simuladores y autoevaluación)
# ---------------------------------------------------------------------------
js_cap3 = (FUENTES / "cap3_js.js").read_text(encoding="utf-8")
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

# ---------------------------------------------------------------------------
# 10. Verificar por defecto; escribir solo si se pide
# ---------------------------------------------------------------------------
escribir = "--escribir" in sys.argv
previo = DESTINO.read_text(encoding="utf-8") if DESTINO.exists() else None

if previo is not None and previo != html:
    import difflib
    d = list(difflib.unified_diff(previo.splitlines(), html.splitlines(),
                                  "en disco", "ensamblado", lineterm="", n=0))
    mas = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
    menos = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
    print(f"DIFIERE del archivo en disco: +{mas} / -{menos} líneas.")
    print("Primeras diferencias:")
    for l in [x for x in d if x.startswith(("+", "-"))
              and not x.startswith(("+++", "---"))][:12]:
        print("   ", l[:118])
    if not escribir:
        print("\nNo se ha escrito nada. El archivo en disco manda: puede llevar")
        print("correcciones de contenido posteriores a este script.")
        print("Para sobrescribirlo de todas formas: python3 ensambla_cap3.py --escribir")
        sys.exit(2)

if not escribir:
    print(f"OK: {DESTINO.name} es reproducible byte a byte desde este script.")
    sys.exit(0)

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
