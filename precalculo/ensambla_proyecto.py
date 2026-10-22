#!/usr/bin/env python3
"""
ensambla_proyecto.py — Construye la guía del proyecto de pronóstico del Corte III.

Parte de `plantilla/plantilla-capitulo.html` y SUSTITUYE regiones concretas,
como `ensambla_taller2.py`. Calcado de `Diseno de experimentos/ensamblado/
ensambla_proyecto.py`, que es el modelo (ver `PLAN_Proyecto_Pronostico.md`).

    python3 precalculo/ensambla_proyecto.py             → escribe
        Htmls_Series/proyecto-pronostico-corte-iii.html y copia la plantilla .Rmd
    python3 precalculo/ensambla_proyecto.py --revisar   → hace todas las
        comprobaciones y no escribe nada

DE DÓNDE SALE CADA COSA
  · La prosa: `proyecto/modulos/m*.html`, con marcadores `@@CLAVE@@`.
  · Las cifras —fechas, pesos, rúbrica, tope, longitudes mínimas, la
    conjunta—: `proyecto/datos.py`, y SOLO de ahí. El ensamblador las imprime;
    `proyecto/audita_proyecto.py` las vuelve a calcular sobre el artefacto.
  · Las tablas (hitos, pesos, tope, retraso, niveles, frecuencias, exigencias
    y rúbrica) se generan aquí desde `datos.py`: una tabla tecleada en la prosa
    sería la segunda copia de una cifra.
  · El código R de la prosa se escribe crudo en los módulos y se escapa aquí,
    al copiarlo dentro de `<pre><code>`: así el auditor lo puede ejecutar tal
    como está en la fuente.

LAS DOS REGLAS DE LA CASA
  1. Toda sustitución exige que su marcador aparezca EXACTAMENTE UNA VEZ.
  2. Al final se comprueba el ARTEFACTO, no la intención.

La guía no lleva quiz ni simuladores: los entregables son documentos de R.
Reejecutable: dos ejecuciones producen el mismo archivo.
"""
from __future__ import annotations

import html as _html
import pathlib
import re
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"
FUENTES = RAIZ / "proyecto"
SITIO = RAIZ / "Htmls_Series"
DESTINO = SITIO / "proyecto-pronostico-corte-iii.html"
RMD_FUENTE = FUENTES / "plantilla-informe.Rmd"
RMD_DESTINO = SITIO / "proyecto-pronostico-plantilla.Rmd"

sys.path.insert(0, str(FUENTES))
import datos as D  # noqa: E402

TITULO = "Proyecto de pronóstico · Corte III"
PRESUPUESTO_KB = 500

# Los diez módulos: (n, título, título corto, duración, fuente, objetivo).
MODULOS = [
    (1, "Cómo funciona el proyecto", "Cómo funciona", "10 min", "m1-como-funciona.html",
     "Saber qué se te pide, cuándo y cuánto pesa cada cosa, antes de elegir la serie."),
    (2, "Qué serie vale", "Qué serie vale", "8 min", "m2-que-serie-vale.html",
     "Reconocer si una serie da para un proyecto antes de escribir la ficha."),
    (3, "El repositorio en GitHub", "Repositorio", "8 min", "m3-repositorio.html",
     "Montar el repositorio donde vive todo el proyecto y saber qué cuenta como entrega."),
    (4, "Hito 1 · Ficha de la serie", "Ficha", "5 min", "m4-ficha.html",
     "Proponer la serie en una ficha corta, a tiempo para cambiarla."),
    (5, "Hito 2 · Preregistro", "Preregistro", "15 min", "m5-preregistro.html",
     "Fijar cómo se va a juzgar el pronóstico antes de poder ver cómo le va."),
    (6, "Hito 3 · Avance", "Avance", "6 min", "m6-avance.html",
     "Entregar lo que dice el tramo de entrenamiento, cuando todavía se puede corregir."),
    (7, "Hito 4 · Informe y código", "Informe", "10 min", "m7-informe.html",
     "Contar el proyecto entero en un informe que se reproduce de principio a fin."),
    (8, "El proyecto conjunto con Estadística Espacial", "Conjunto", "8 min", "m8-conjunta.html",
     "Saber si te conviene un solo proyecto para las dos materias, y con qué reglas."),
    (9, "La exposición", "Exposición", "6 min", "m9-exposicion.html",
     "Contar el proyecto en el tiempo justo y defender cada decisión."),
    (10, "La rúbrica", "Rúbrica", "10 min", "m10-rubrica.html",
     "Saber con qué se califica cada entrega, y qué separa un nivel de otro."),
]


# ---------------------------------------------------------------------------
# 1. Utilidades
# ---------------------------------------------------------------------------
def lee(ruta: pathlib.Path) -> str:
    if not ruta.exists():
        sys.exit(f"PARADO: falta {ruta}")
    return ruta.read_text(encoding="utf-8")


def sustituye(texto: str, marcador: str, nuevo: str, que: str) -> str:
    n = texto.count(marcador)
    if n != 1:
        sys.exit(f"PARADO: el marcador de «{que}» aparece {n} veces "
                 f"(se esperaba 1):\n    {marcador[:110]!r}")
    print(f"  · {que}")
    return texto.replace(marcador, nuevo)


def sustituye_region(texto: str, inicio: str, fin: str, nuevo: str, que: str) -> str:
    for d in (inicio, fin):
        if texto.count(d) != 1:
            sys.exit(f"PARADO: el delimitador de «{que}» aparece "
                     f"{texto.count(d)} veces:\n    {d[:110]!r}")
    i, j = texto.index(inicio), texto.index(fin)
    if j < i:
        sys.exit(f"PARADO: los delimitadores de «{que}» están en orden inverso")
    print(f"  · {que}")
    return texto[:i] + nuevo + texto[j + len(fin):]


def e(t: str) -> str:
    return _html.escape(t, quote=False)


def cierra(h: dict) -> str:
    return f"{D.frase_fecha(h['fecha'])} a las {D.HORA_ENTREGA}"


def escapa_codigo(texto: str) -> str:
    """El R de los módulos va crudo en la fuente; aquí se escapa dentro de <code>."""
    return re.sub(r'(<pre><code class="language-r">)(.*?)(</code></pre>)',
                  lambda m: m.group(1) + e(m.group(2)) + m.group(3), texto, flags=re.S)


def tabla(caption: str, cabeza: list[str], filas: list[list[str]]) -> str:
    th = "".join(f'<th scope="col">{c}</th>' for c in cabeza)
    tr = "\n".join("          <tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f"""      <table>
        <caption>{caption}</caption>
        <thead>
          <tr>{th}</tr>
        </thead>
        <tbody>
{tr}
        </tbody>
      </table>"""


# ---------------------------------------------------------------------------
# 2. Las tablas, desde datos.py
# ---------------------------------------------------------------------------
def tabla_hitos() -> str:
    filas = []
    for h in D.HITOS:
        peso = "sin nota" if h["id"] == "ficha" else f"{D.puntos_de(h['id'])} %"
        filas.append([str(h["n"]), f"<strong>{e(h['nombre'])}</strong>", e(h["entrega"]),
                      D.frase_fecha(h["fecha"]), str(h["semana"]), peso])
    filas.append(["5", "<strong>Exposición</strong>",
                  f"{D.MINUTOS_EXPOSICION} minutos por equipo y {D.MINUTOS_PREGUNTAS} de preguntas, en clase",
                  "se acuerda en clase", str(D.SEMANA_EXPOSICION), f"{D.puntos_de('exposicion')} %"])
    return tabla(f"Los hitos del proyecto. Las entregas cierran a las {D.HORA_ENTREGA} del día "
                 "indicado; el peso es sobre la nota del proyecto.",
                 ["#", "Hito", "Qué entregas", "Cierra", "Semana", "Peso"], filas)


def tabla_pesos() -> str:
    filas = [[e(b["titulo"]), ", ".join(c["id"] for c in b["criterios"]),
              f"{D.puntos_de(b['hito'])} %",
              f"<strong>{D.pct(D.puntos_de(b['hito']) * D.PROYECTO_DEL_CORTE / 100)} %</strong>"]
             for b in D.RUBRICA]
    return tabla("Reparto de la nota del proyecto. La última columna es sobre la nota del Corte III.",
                 ["Hito", "Criterios", "Del proyecto", "Del corte"], filas)


def tabla_tope() -> str:
    filas = [[e(f["situacion"]), D.nota(f["escrito"]), D.nota(f["exposicion"]),
              D.nota(f["preguntas"]), D.nota(f["sin_tope"]), f"<strong>{D.nota(f['con_tope'])}</strong>"]
             for f in D.filas_tope()]
    p_esc = sum(D.puntos_de(h) for h in D.HITOS_ESCRITOS)
    p_e = {c["id"]: c["puntos"] for b in D.RUBRICA for c in b["criterios"] if c["id"] in ("E1", "E2")}
    return tabla(f"Qué cambia el tope. Lo escrito vale {p_esc} puntos del proyecto, la exposición "
                 f"(E1) {p_e['E1']} y las preguntas (E2) {p_e['E2']}; todo en la escala de 5.",
                 ["Situación", "Escrito", "Exposición (E1)", "Preguntas (E2)", "Sin tope", "Con tope"],
                 filas)


def tabla_retraso() -> str:
    filas = [[str(f["sesiones"]), f"{f['descuento']} %", D.nota(f["nota"])] for f in D.filas_retraso()]
    return tabla(f"El descuento por entrega tardía, sobre una entrega que a tiempo habría sacado "
                 f"{D.nota(D.EJEMPLO_RETRASO)}.",
                 ["Sesiones de retraso", "Descuento", "La nota queda en"], filas)


def tabla_niveles() -> str:
    return tabla("Lo que vale cada nivel, en la escala de 5.", ["Nivel", "Vale"],
                 [[n.capitalize(), D.nota(v)] for n, v in D.NIVELES])


def tabla_frecuencias() -> str:
    filas = [[f, f"${m}$", f"${h}$", f"${D.t0_minimo(m)}$", f"<strong>${D.n_minimo(m, h)}$</strong>"]
             for f, m, h in D.FRECUENCIAS]
    return tabla(f"La longitud mínima para {D.ORIGENES_MIN} orígenes, con un horizonte de ejemplo. "
                 "Con otro horizonte, la cuenta es la misma.",
                 ["Frecuencia", "$m$", "$h$", "$T_0$ mínimo", "$n$ mínimo"], filas)


def tabla_exigencias() -> str:
    filas = []
    for clave, texto in D.EXIGENCIAS_M12.items():
        ids = [c["id"] for b in D.RUBRICA for c in b["criterios"] if c.get("exigencia") == clave]
        filas.append([e(texto), ", ".join(ids)])
    return tabla("Las exigencias del módulo 6.12 y los criterios que las califican.",
                 ["Exigencia", "Criterios"], filas)


def rubrica() -> str:
    partes = []
    for b in D.RUBRICA:
        partes.append(f"      <h3>{e(b['titulo'])} · {D.puntos_de(b['hito'])} puntos</h3>")
        for c in b["criterios"]:
            quien = " Se califica persona por persona." if c.get("individual") else ""
            partes.append(tabla(
                f"<strong>{c['id']} · {e(c['nombre'])}</strong> — {c['puntos']} puntos.{quien}",
                ["Nivel", "Qué se ve"],
                [[n.capitalize(), e(c[clave])] for n, clave in
                 (("insuficiente", "insuficiente"), ("aceptable", "aceptable"), ("sólido", "solido"))]))
    return "\n\n".join(partes)


def lista_y(items: list[str]) -> str:
    return ", ".join(items[:-1]) + " y " + items[-1]


# ---------------------------------------------------------------------------
# 3. Los marcadores de la prosa
# ---------------------------------------------------------------------------
def marcadores() -> dict[str, str]:
    H = D.HITO
    ej0 = D.filas_tope()[0]
    d1, d2 = D.DIAS_EXPOSICION
    m = {
        "TABLA_HITOS": tabla_hitos(),
        "TABLA_PESOS": tabla_pesos(),
        "TABLA_TOPE": tabla_tope(),
        "TABLA_NIVELES": tabla_niveles(),
        "TABLA_RETRASO": tabla_retraso(),
        "TABLA_FRECUENCIAS": tabla_frecuencias(),
        "TABLA_EXIGENCIAS": tabla_exigencias(),
        "SERIES_DEL_MATERIAL": lista_y([f"<code>{s}</code>" if s != "TRM" else "la TRM"
                                        for s in D.SERIES_DEL_MATERIAL]),
        "DESCUENTO": str(D.DESCUENTO_POR_SESION),
        "USUARIO_DOCENTE": D.USUARIO_DOCENTE,
        "NOMBRE_REPO": D.NOMBRE_REPO,
        "NOMBRE_REPO_CONJUNTO": D.NOMBRE_REPO_CONJUNTO,
        "ETIQUETAS": ", ".join(f"<code>{D.ETIQUETA[h['id']]}</code>" for h in D.HITOS[:-1])
                     + f" e <code>{D.ETIQUETA[D.HITOS[-1]['id']]}</code>",
        "DIA_EXPOSICION": D.DIA_EXPOSICION,
        # «martes 17 o miércoles 18 de noviembre»: los dos son del mismo mes.
        "DIAS_EXPOSICION": f"{D.DIAS[d1.weekday()]} {d1.day} o {D.frase_fecha(d2)}",
        "RUBRICA": rubrica(),
        "HORA_ENTREGA": D.HORA_ENTREGA,
        "CANAL_ENTREGA": D.CANAL_ENTREGA,
        "DUDAS_EN": D.DUDAS_EN,
        "TUTORIAS": D.tutorias_en(),
        "SEMANA_EXPOSICION": str(D.SEMANA_EXPOSICION),
        "SEMANA_EXPOSICION_FRASE": D.frase_semana(D.SEMANA_EXPOSICION),
        "MINUTOS_EXPOSICION": str(D.MINUTOS_EXPOSICION),
        "MINUTOS_PREGUNTAS": str(D.MINUTOS_PREGUNTAS),
        "MINUTOS_EXPOSICION_CONJUNTA": str(D.MINUTOS_EXPOSICION_CONJUNTA),
        "MINUTOS_PREGUNTAS_CONJUNTA": str(D.MINUTOS_PREGUNTAS_CONJUNTA),
        "PREGUNTAS_POR_MATERIA": str(D.PREGUNTAS_POR_MATERIA),
        "AREAS_MINIMAS": str(D.AREAS_MINIMAS),
        "PROYECTO_DEL_CORTE": str(D.PROYECTO_DEL_CORTE),
        "QUICES_DEL_CORTE": str(D.QUICES_DEL_CORTE),
        "CORTE_III_DEL_CURSO": str(D.CORTE_III_DEL_CURSO),
        "PROYECTO_DEL_CURSO": D.pct(D.PROYECTO_DEL_CURSO),
        "NIVELES": " · ".join(f"<strong>{n}</strong>" for n, _ in D.NIVELES),
        "UMBRAL": D.nota(D.UMBRAL_TOPE),
        "UMBRAL_DIV": D.divisor(D.UMBRAL_TOPE),
        "EJ0_SIN": D.nota(ej0["sin_tope"]),
        "EJ0_CON": D.nota(ej0["con_tope"]),
        "PALABRAS_FICHA": str(D.PALABRAS_FICHA),
        "PAGINAS_PREREGISTRO": str(D.PAGINAS_PREREGISTRO),
        "PAGINAS_INFORME": str(D.PAGINAS_INFORME),
        "PAGINAS_INFORME_CONJUNTO": str(D.PAGINAS_INFORME_CONJUNTO),
        "PLANTILLA_RMD": RMD_DESTINO.name,
        "CICLOS": str(D.CICLOS_ENTRENAMIENTO),
        "T0_MINIMO": str(D.T0_MINIMO),
        "ORIGENES_MIN": str(D.ORIGENES_MIN),
        "N_MIN_MENSUAL": str(D.n_minimo(12, 12)),
    }
    for clave, h in (("FICHA", H["ficha"]), ("PREREGISTRO", H["preregistro"]),
                     ("AVANCE", H["avance"]), ("INFORME", H["informe"])):
        m[f"{clave}_CIERRA"] = cierra(h)
        m[f"{clave}_SEMANA"] = str(h["semana"])
        m[f"ETIQUETA_{clave}"] = D.ETIQUETA[h["id"]]
        if h["id"] != "ficha":
            m[f"PESO_{clave}"] = str(D.puntos_de(h["id"]))
    m["PESO_EXPOSICION"] = str(D.puntos_de("exposicion"))
    return m


def resuelve(texto: str, m: dict[str, str], usados: set, fuente: str) -> str:
    def rep(mo):
        clave = mo.group(1)
        if clave not in m:
            sys.exit(f"PARADO: {fuente} usa el marcador desconocido @@{clave}@@")
        usados.add(clave)
        return m[clave]
    return re.sub(r"@@([A-Z0-9_]+)@@", rep, texto)


def cabecera_modulo(n: int, titulo: str, objetivo: str) -> str:
    return f"""  <!-- ============================================================ -->
  <!-- MÓDULO {n} · {titulo}
  <!-- ============================================================ -->
  <template id="module-{n}">
    <div class="animate-fade-in">
      <div class="border-b border-gray-100 pb-6 mb-6">
        <div class="flex items-center space-x-2 text-sm text-secondary font-semibold mb-2 uppercase tracking-wide">
          <span>Módulo {n}</span>
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-4" style="border:none; padding:0;">{titulo}</h2>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 flex items-start gap-3">
          <span class="text-xl">🎯</span>
          <div>
            <h3 class="font-bold text-gray-800 text-sm" style="margin:0;">Objetivo</h3>
            <p class="text-gray-600 text-sm" style="margin:0;">{objetivo}</p>
          </div>
        </div>
      </div>
"""


CIERRE_MODULO = "    </div>\n  </template>"


def selectores(t: str) -> set:
    return set(re.findall(r"^\s*(\.[a-zA-Z][\w-]*)", t[:t.index("</style>")], re.M))


# ---------------------------------------------------------------------------
# 4. El ensamblado
# ---------------------------------------------------------------------------
def main() -> int:
    revisar = "--revisar" in sys.argv
    print(f"\n=== ensambla_proyecto.py{' --revisar' if revisar else ''} ===\nbase: {PLANTILLA.name}")
    html = lee(PLANTILLA)
    sel_plantilla = selectores(html)
    print("\nsustituciones:")

    # --- 1. Metadatos y cabecera --------------------------------------------
    html = sustituye(html, "<title>Plantilla de capítulo — Material de estudio interactivo</title>",
                     f"<title>{TITULO} — Series de Tiempo</title>", "título del documento")
    html = sustituye(
        html,
        'content="Plantilla base para capítulos de material de estudio interactivo (Universidad El '
        'Bosque): cajas, código R/Python en pestañas, simuladores con Chart.js, autoevaluación y '
        'ejercicios guiados."',
        'content="Guía del proyecto de pronóstico del Corte III de Series de Tiempo (Universidad El '
        'Bosque): elegir una serie real, preregistrar el protocolo de evaluación, modelarla, '
        'evaluarla por origen móvil y defenderla, con sus hitos, su rúbrica, una plantilla de '
        'informe y la opción conjunta con Estadística Espacial."',
        "meta description")
    html = sustituye(
        html,
        'content="plantilla, material de estudio, capítulo HTML, simulador, autoevaluación, '
        'ejercicios guiados, R, Python, UnBosque"',
        'content="series de tiempo, proyecto de pronóstico, preregistro, origen móvil, MASE, '
        'Diebold-Mariano, cobertura, SARIMA, rúbrica, exposición, uso de IA, R, forecast, UnBosque"',
        "meta keywords")
    html = sustituye(
        html,
        '<h1 class="text-xl font-bold text-white leading-tight tracking-tight" '
        'style="margin:0;">Nombre del curso\n            </h1>',
        '<h1 class="text-xl font-bold text-white leading-tight tracking-tight" '
        f'style="margin:0;">{TITULO}\n            </h1>',
        "título de la cabecera")
    html = sustituye(
        html, "PLANTILLA BASE •\n              4 MÓDULOS DE DEMOSTRACIÓN • UNBOSQUE",
        "SERIES DE TIEMPO (20948) • CORTE III •\n              "
        f"{D.PROYECTO_DEL_CORTE}&nbsp;% DE LA NOTA DEL CORTE • UNBOSQUE 2026-II",
        "subtítulo de la cabecera")
    html = sustituye(html, "Plantilla de capítulo • UnBosque 2026",
                     "Proyecto de pronóstico • Corte III • UnBosque 2026-II", "pie de página")

    # --- 2. Los diez módulos ------------------------------------------------
    m = marcadores()
    usados: set = set()
    piezas = []
    for n, titulo, _corto, _dur, fuente, objetivo in MODULOS:
        cuerpo = escapa_codigo(resuelve(lee(FUENTES / "modulos" / fuente), m, usados, fuente))
        piezas.append(cabecera_modulo(n, titulo, objetivo) + cuerpo.rstrip() + "\n" + CIERRE_MODULO)
    sobran = sorted(set(m) - usados)
    if sobran:
        sys.exit(f"PARADO: marcadores que ninguna prosa usa: {sobran}")
    html = sustituye_region(
        html,
        "  <!-- ============================================================ -->\n"
        "  <!-- MÓDULO 1 · Cajas y tipografía",
        "  </template>\n\n  <script>",
        "\n\n".join(piezas) + "\n\n  <script>",
        f"los {len(MODULOS)} módulos")

    # --- 3. courseData --------------------------------------------------------
    html = sustituye(
        html,
        "    // PLANTILLA BASE. Punto de partida para un capítulo de un curso\n"
        "    // NUEVO. Para un capítulo más de un curso ya empezado, copia su\n"
        "    // último capítulo, que lleva los datos y el contexto ya montados.",
        "    // PROYECTO DE PRONÓSTICO DEL CORTE III. Ensamblado por\n"
        "    // precalculo/ensambla_proyecto.py desde plantilla/plantilla-capitulo.html.\n"
        "    // NO SE EDITA A MANO: la prosa vive en proyecto/modulos/ y las cifras\n"
        "    // en proyecto/datos.py.",
        "comentario de cabecera del script")
    filas = ",\n".join(
        f'        {{ id: {i}, title: "{t}", shortTitle: "{s}", duration: "{d}" }}'
        for i, t, s, d, *_ in MODULOS)
    html = sustituye_region(
        html, "    const courseData = {",
        '        { id: 4, title: "Autoevaluación y ejercicios", shortTitle: "Autoevaluación", duration: "8 min" }\n'
        "      ]\n    };",
        f'    const courseData = {{\n      title: "{TITULO}",\n      modules: [\n{filas}\n      ]\n    }};',
        "courseData")
    html = sustituye(
        html,
        "    // Los datos del capítulo se incrustan aquí, generados por\n"
        "    // precalculo/genera_*.R:  const DATOS_CAPn = { ... };\n"
        "    // Los simuladores de demostración de abajo no usan datos externos.\n",
        "    // La guía no incrusta datos: sus cifras se imprimen en el marcado\n"
        "    // desde proyecto/datos.py.\n",
        "comentario de los datos")

    # --- 4. Las demostraciones ----------------------------------------------
    html = sustituye_region(
        html,
        "    // Demostración del componente .mapa-estacional. Como el resto de la\n",
        "          '\\'divergente\\'</code> y la paleta se centra en cero.'\n      });\n    };\n",
        "", "se retira la demostración del mapa estacional")
    html = sustituye_region(
        html,
        "    // ================================================================\n"
        "    // Simuladores de demostración",
        "    ];\n\n  </script>",
        "  </script>",
        "se retiran los simuladores, la rúbrica, el ranking y el quiz de demostración")

    return comprueba_y_escribe(html, sel_plantilla, revisar)


# ---------------------------------------------------------------------------
# 5. Las comprobaciones, sobre el artefacto
# ---------------------------------------------------------------------------
def modulos_de(archivo: pathlib.Path) -> set:
    return set(int(x) for x in re.findall(r'<template id="module-(\d+)"', lee(archivo)))


def comprueba_y_escribe(html: str, sel_plantilla: set, revisar: bool) -> int:
    print("\ncomprobaciones sobre el resultado:")
    fallos: list[str] = []
    marcado = html[html.index('<template id="module-1">'):html.rindex("\n  <script>")]

    def exige(cond: bool, que: str) -> None:
        print(f"  {'OK ' if cond else 'MAL'}  {que}")
        if not cond:
            fallos.append(que)

    exige(len(re.findall(r'<template id="module-\d+">', marcado)) == len(MODULOS),
          f"las {len(MODULOS)} plantillas de módulo")
    exige(all(f'<template id="module-{i}">' in marcado for i, *_ in MODULOS),
          f"los identificadores de módulo van del 1 al {len(MODULOS)} sin huecos")
    exige("@@" not in html, "ningún marcador @@ sin resolver")

    tablas = marcado.count("<table>")
    exige(tablas == marcado.count("<caption"), f"las {tablas} tablas llevan su caption")

    ids = re.findall(r' id="([^"]+)"', marcado)
    repes = sorted({i for i in ids if ids.count(i) > 1})
    exige(not repes, f"identificadores únicos{'' if not repes else ': ' + ', '.join(repes)}")
    vacias = [c for c in ("note", "warning", "definition", "tip-box", "diagram", "formula")
              if re.search(rf'<div class="{c}">\s*</div>', marcado)]
    exige(not vacias, f"ninguna caja vacía{'' if not vacias else ': ' + ', '.join(vacias)}")
    exige("undefined" not in marcado, "ningún «undefined» impreso en el marcado")

    # El R se escapó: dentro de <code> no queda un «<-» crudo.
    codigos = re.findall(r'<code class="language-r">(.*?)</code>', marcado, re.S)
    exige(codigos and all("<" not in c for c in codigos),
          f"los {len(codigos)} bloques de R van escapados")

    quizzes = set(re.findall(r"AUTOEVALUACIONES\['([\w-]+)'\]\s*=", html)) - {"id"}
    sims = set(re.findall(r"SIMULADORES\['([\w-]+)'\]\s*=", html)) - {"id", "mi-id"}
    exige(not quizzes, f"no hay ningún quiz{'' if not quizzes else ': ' + ', '.join(sorted(quizzes))}")
    exige(not sims, f"no hay ningún simulador{'' if not sims else ': ' + ', '.join(sorted(sims))}")
    exige(selectores(html) == sel_plantilla, f"el CSS es el de la plantilla ({len(sel_plantilla)} selectores)")

    for prohibido, que in [
        ("demo-deslizadores", "simulador de demostración «demo-deslizadores»"),
        ("demo-correlograma", "simulador de demostración «demo-correlograma»"),
        ("demo-interruptores", "simulador de demostración «demo-interruptores»"),
        ("demo-mapa", "mapa estacional de demostración"),
        ("demo-rubrica", "rúbrica de demostración"),
        ("AUTOEVALUACIONES['demo']", "autoevaluación de demostración"),
        ("TABLAS_RANKING['demo']", "tabla de ranking de demostración"),
        ("Cajas y tipografía", "módulo de demostración de cajas"),
        ("PLANTILLA BASE", "el rótulo de plantilla base"),
        ("Nombre del curso", "el título genérico de la plantilla"),
    ]:
        exige(prohibido not in html, f"no queda: {que}")

    for imprescindible in ("renderMathInElement", "wrapCodeBlocks", "iniciarSimuladores",
                           "iniciarAutoevaluaciones", "iniciarEjerciciosGuiados", "moduloDelHash",
                           "destruirSimuladores"):
        exige(imprescindible in html, f"el motor conserva {imprescindible}()")

    # Los enlaces locales resuelven, y un ancla #modulo-N apunta a un módulo que existe.
    enlaces = re.findall(r'href="([^":]+)"', marcado)
    rotos = []
    for h in enlaces:
        archivo, _, ancla = h.partition("#")
        if archivo == RMD_DESTINO.name:
            continue
        ruta = SITIO / archivo
        if not ruta.exists():
            rotos.append(h)
        elif ancla:
            mo = re.fullmatch(r"modulo-(\d+)", ancla)
            if not mo or int(mo.group(1)) not in modulos_de(ruta):
                rotos.append(h)
    exige(not rotos, f"los {len(enlaces)} enlaces locales resuelven, anclas incluidas"
                     + ("" if not rotos else ": " + ", ".join(sorted(set(rotos)))))
    exige(RMD_FUENTE.exists(), "la plantilla .Rmd existe en la fuente")

    kb = len(html.encode("utf-8")) / 1024
    exige(kb < PRESUPUESTO_KB, f"pesa {kb:.0f} KB (presupuesto {PRESUPUESTO_KB} KB)")

    if fallos:
        print(f"\nPARADO: {len(fallos)} comprobaciones fallidas. No se escribió nada.")
        for f in fallos:
            print(f"  · {f}")
        return 1

    if revisar:
        actual = DESTINO.read_text(encoding="utf-8") if DESTINO.exists() else None
        rmd = RMD_DESTINO.read_bytes() if RMD_DESTINO.exists() else None
        print(f"\n--revisar: no se escribe nada.\n"
              f"  {'NUEVO ' if actual is None else ('igual ' if actual == html else 'CAMBIA')} "
              f"{DESTINO.relative_to(RAIZ)}\n"
              f"  {'NUEVO ' if rmd is None else ('igual ' if rmd == RMD_FUENTE.read_bytes() else 'CAMBIA')} "
              f"{RMD_DESTINO.relative_to(RAIZ)}")
        return 0

    DESTINO.write_text(html, encoding="utf-8")
    shutil.copyfile(RMD_FUENTE, RMD_DESTINO)
    print(f"\nEscrito {DESTINO.relative_to(RAIZ)}  ({DESTINO.stat().st_size / 1024:.0f} KB)")
    print(f"Copiado {RMD_DESTINO.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
