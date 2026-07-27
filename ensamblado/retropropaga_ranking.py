#!/usr/bin/env python3
"""Retropropaga el componente `.tabla-ranking` y corrige un bug del `.quiz`.

Hace dos cosas independientes:

1. **Instala `.tabla-ranking`** (CSS, JavaScript y la llamada de arranque) en los
   capítulos 3, 4 y 5 y en la plantilla, con una instancia en cada uno. Los
   capítulos 1 y 2 **no** lo reciben: ninguno tiene una tabla comparativa de
   modelos que ordenar, igual que en su día no recibieron `.mapa-estacional`.
   El capítulo 6 ya lo trae por construcción (`ensambla_cap6.py`).

2. **Corrige un bug encontrado auditando el capítulo 6** que afecta a los seis
   capítulos y a la plantilla: al acertar una pregunta de selección múltiple,
   `renderAutoevaluacion()` escribe `p.retroAcierto`, que en las preguntas de ese
   tipo **nunca se define**, y el estudiante ve literalmente la palabra
   «undefined» detrás de «Correcto». Son 9 preguntas en 7 archivos. Se arregla
   por partida doble: `cerrar()` deja de imprimir un valor indefinido, y la rama
   de selección múltiple pasa como respaldo la retroalimentación de las opciones
   correctas, que ya estaba escrita y no se mostraba.

Aborta si un archivo ya tiene el componente, así que es seguro reejecutarlo por
error pero NO es reejecutable: está escrito contra el estado anterior.

Uso:  python3 retropropaga_ranking.py       (desde ensamblado/)
"""

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
COMPONENTES = AQUI / "componentes"
HTMLS = RAIZ / "Htmls_Series"
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"

sys.path.insert(0, str(COMPONENTES))
from tabla_ranking_html import (tabla_ranking_html,          # noqa: E402
                                comprueba_tabla_ranking)

CSS = (COMPONENTES / "tabla_ranking.css").read_text(encoding="utf-8").rstrip("\n")
JS = (COMPONENTES / "tabla_ranking.js").read_text(encoding="utf-8").rstrip("\n")


def una_vez(texto, viejo, nuevo, etiqueta, archivo):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ABORTA [{archivo} / {etiqueta}]: el marcador aparece "
                         f"{n} veces, se esperaba 1.\n  {viejo[:100]!r}")
    return texto.replace(viejo, nuevo, 1)


# ---------------------------------------------------------------------------
# Parte 1 — instalación del componente
# ---------------------------------------------------------------------------

def instala_componente(html, archivo):
    if ".tabla-ranking {" in html:
        raise SystemExit(f"ABORTA: {archivo} ya tiene el componente .tabla-ranking")

    html = una_vez(html, "  </style>", CSS + "\n  </style>",
                   "CSS", archivo)

    # El JavaScript va justo antes del inicializador de derivaciones, que existe
    # en los seis capítulos y en la plantilla desde T5b.
    ancla = "    function iniciarDerivaciones("
    html = una_vez(html, ancla, JS + "\n\n" + ancla, "JavaScript", archivo)

    html = una_vez(html, "        iniciarCiclos();\n",
                   "        iniciarCiclos();\n        iniciarTablasRanking();\n",
                   "llamada de arranque", archivo)
    return html


# Cada instancia: (id, título, pie, ancla del HTML, registro en JS, ancla del registro)
INSTANCIAS = {
    "capitulo-3-modelos-ar-ma-arma.html": dict(
        id="criterios",
        titulo="Los criterios de información sobre las manchas solares",
        pie="",
        ancla_html='      <div class="simulador" data-simulador="diagnostico-residuales">',
        ancla_js="    AUTOEVALUACIONES['cap3'] = [",
        registro="""    // Tabla ordenable de los criterios de información: los ocho modelos
    // comparten $d = 0$, así que aquí el AICc SÍ es comparable entre todos.
    TABLAS_RANKING['criterios'] = function () {
      return {
        descripcion: 'Los ocho candidatos ARMA sobre las manchas solares crudas. ' +
          'Los ocho comparten $d = 0$ y el mismo $n$, así que sus criterios son ' +
          'comparables entre sí. Pulsa una cabecera para reordenar.',
        columnas: [
          { clave: 'modelo', titulo: 'Modelo', tipo: 'texto' },
          { clave: 'k', titulo: 'Coeficientes', decimales: 0, mejor: 'menor' },
          { clave: 'aicc', titulo: 'AICc', decimales: 2, mejor: 'menor' },
          { clave: 'bic', titulo: 'BIC', decimales: 2, mejor: 'menor' },
          { clave: 'sigma2', titulo: 'σ²', decimales: 1, mejor: 'menor' },
          { clave: 'lb', titulo: 'Ljung–Box p', tituloLargo: 'p-valor de Ljung-Box', decimales: 4, mejor: 'mayor' }
        ],
        filas: MANCHAS.rejilla.map(m => ({
          modelo: m.etiqueta, k: m.n_coef, aicc: m.aicc, bic: m.bic,
          sigma2: m.sigma2, lb: m.lb12_p
        })),
        inicial: 'aicc',
        destacada: 'ARMA(2,0)',
        pie: 'El AR($2$) de Yule —la fila marcada— no es el mínimo de ninguno de los ' +
          'dos criterios sobre la serie cruda, y ordenando por Ljung–Box se ve además ' +
          'que no pasa el diagnóstico. Sobre $\\\\sqrt{\\\\text{manchas}}$ la conclusión cambia.'
      };
    };

"""),
    "capitulo-4-modelos-arima.html": dict(
        id="rejilla-nilo",
        titulo="Los 27 modelos del Nilo, con su n efectivo a la vista",
        pie="",
        ancla_html='      <div class="simulador" data-simulador="explorador-modelos">',
        ancla_js="    AUTOEVALUACIONES['cap4'] = [",
        registro="""    // Tabla ordenable de la rejilla del Nilo. Se incluye a propósito la columna
    // del n efectivo: ordenar por AICc con modelos de distinto d es el error que
    // este capítulo enseña a no cometer, y aquí queda a la vista.
    TABLAS_RANKING['rejilla-nilo'] = function () {
      const filas = Object.keys(NILO.rejilla).map(k => {
        const m = NILO.rejilla[k];
        return {
          modelo: m.etiqueta, d: m.d, n: m.n_efectivo, k: m.k,
          aicc: m.aicc, bic: m.bic, lb: m.ljung_box_12_p
        };
      });
      return {
        descripcion: 'Los 27 modelos ARIMA($p,d,q$) sobre el Nilo. Ordena por AICc y ' +
          'mira la columna <strong>n efectivo</strong>: el «mejor» tiene $d = 2$ y se ' +
          'evalúa sobre 98 observaciones, no sobre 100. <strong>Esa ordenación no es ' +
          'válida.</strong>',
        columnas: [
          { clave: 'modelo', titulo: 'Modelo', tipo: 'texto' },
          { clave: 'd', titulo: 'd', decimales: 0, mejor: 'menor' },
          { clave: 'n', titulo: 'n efectivo', tituloLargo: 'número de observaciones efectivas', decimales: 0, mejor: 'mayor' },
          { clave: 'k', titulo: 'Coeficientes', decimales: 0, mejor: 'menor' },
          { clave: 'aicc', titulo: 'AICc', decimales: 2, mejor: 'menor' },
          { clave: 'bic', titulo: 'BIC', decimales: 2, mejor: 'menor' },
          { clave: 'lb', titulo: 'Ljung–Box p', tituloLargo: 'p-valor de Ljung-Box', decimales: 4, mejor: 'mayor' }
        ],
        filas: filas,
        inicial: 'd',
        destacada: 'ARIMA(1,1,1)',
        pie: 'Ordena primero por <em>d</em> y compara dentro de cada grupo; solo así ' +
          'la comparación es legítima. Los mejores por AICc son $(1,0,1)$, $(1,1,1)$ y ' +
          '$(1,2,2)$, uno por cada $d$, y no se pueden poner en la misma lista.'
      };
    };

"""),
    "capitulo-5-sarima.html": dict(
        id="comparativa",
        titulo="Los seis métodos sobre una sola partición",
        pie="",
        ancla_html='      <div class="simulador" data-simulador="comparativa-particion">',
        ancla_js="    AUTOEVALUACIONES['cap5'] = [",
        registro="""    // Tabla ordenable de la comparativa sobre UNA partición. El pie recuerda que
    // este ranking se desmiente en el capítulo 6 con 61 orígenes.
    TABLAS_RANKING['comparativa'] = function () {
      const claves = AP.comparativa.orden_rmse;
      return {
        descripcion: 'Los seis métodos sobre los últimos ' + AP.comparativa.n_prueba +
          ' meses, una sola partición. Pulsa las cabeceras: las tres métricas coinciden ' +
          'en el orden, lo que da una falsa sensación de solidez.',
        columnas: [
          { clave: 'modelo', titulo: 'Método', tipo: 'texto' },
          { clave: 'rmse', titulo: 'RMSE', decimales: 2, mejor: 'menor' },
          { clave: 'mae', titulo: 'MAE', decimales: 2, mejor: 'menor' },
          { clave: 'mape', titulo: 'MAPE', decimales: 2, sufijo: ' %', mejor: 'menor' }
        ],
        filas: claves.map(k => ({
          modelo: AP.comparativa.modelos[k].nombre,
          rmse: AP.comparativa.modelos[k].rmse,
          mae: AP.comparativa.modelos[k].mae,
          mape: AP.comparativa.modelos[k].mape
        })),
        inicial: 'rmse',
        pie: 'Las tres columnas dan el mismo orden y aun así el orden es engañoso: ' +
          'sobre 61 orígenes en vez de uno, el SARIMA pasa de cuarto a primero. ' +
          'El Capítulo 6 construye esa evaluación.'
      };
    };

"""),
}

PLANTILLA_INSTANCIA = dict(
    id="demo",
    titulo="Tabla comparativa ordenable (demostración)",
    pie="",
    ancla_html='      <div class="simulador" data-simulador="demo-interruptores">',
    ancla_js="    AUTOEVALUACIONES['demo'] = [",
    registro="""    // Demostración del componente .tabla-ranking. Datos fijos: la plantilla no
    // incrusta ningún precálculo, igual que sus simuladores generan sus series.
    TABLAS_RANKING['demo'] = function () {
      return {
        descripcion: 'Cuatro métodos ficticios. Pulsa la cabecera de cualquier columna: ' +
          'la tabla se reordena, se renumeran los puestos y se marca el mejor valor. ' +
          'La columna de cobertura no ordena por «menor» sino por <em>cercanía</em> al ' +
          '95 %, que es lo que de verdad se quiere de un intervalo.',
        columnas: [
          { clave: 'metodo', titulo: 'Método', tipo: 'texto' },
          { clave: 'rmse', titulo: 'RMSE', decimales: 2, mejor: 'menor' },
          { clave: 'mase', titulo: 'MASE', decimales: 3, mejor: 'menor' },
          { clave: 'cob', titulo: 'Cob. 95 %', tituloLargo: 'cobertura del 95 %', decimales: 1, sufijo: ' %', mejor: 'cerca', objetivo: 95 },
          { clave: 'seg', titulo: 'Segundos', decimales: 2, mejor: 'menor' }
        ],
        filas: [
          { metodo: 'Referencia simple', rmse: 42.55, mase: 1.681, cob: 93.4, seg: 0.02 },
          { metodo: 'Modelo A', rmse: 18.92, mase: 0.621, cob: 98.4, seg: 0.44 },
          { metodo: 'Modelo B', rmse: 20.63, mase: 0.678, cob: 92.1, seg: 118.61 },
          { metodo: 'Modelo C', rmse: 23.17, mase: 0.759, cob: 94.3, seg: 13.09 }
        ],
        inicial: 'rmse',
        destacada: 'Modelo A',
        pie: 'El Modelo A gana por RMSE y por MASE, y sin embargo es el peor calibrado; ' +
          'el Modelo B es el mejor calibrado y el más lento. El orden depende de la pregunta.'
      };
    };

""")


def instala_instancia(html, archivo, spec):
    marcado = tabla_ranking_html(spec["id"], spec["titulo"], spec["pie"],
                                 sangria="      ").rstrip("\n")
    html = una_vez(html, spec["ancla_html"], marcado + "\n\n" + spec["ancla_html"],
                   "instancia HTML", archivo)
    html = una_vez(html, spec["ancla_js"], spec["registro"] + spec["ancla_js"],
                   "registro en JavaScript", archivo)
    return html


# ---------------------------------------------------------------------------
# Parte 2 — el bug del `undefined` en las preguntas de selección múltiple
# ---------------------------------------------------------------------------

CERRAR_VIEJO = "        retro.innerHTML = encabezado + textoRetro;"
CERRAR_NUEVO = """        // Defensivo: las preguntas de seleccion multiple no declaran
        // `retroAcierto`, y sin esta guarda el estudiante veia la palabra
        // "undefined" detras de "Correcto". (Bug encontrado auditando el cap. 6.)
        retro.innerHTML = encabezado + (textoRetro || '');"""

MULTIPLE_VIEJO = """              boton.disabled = true;
              cerrar(i, bloque, true, p.retroAcierto);"""
MULTIPLE_NUEVO = """              boton.disabled = true;
              // Respaldo para las preguntas de seleccion multiple, que no
              // declaran `retroAcierto`: se junta la retroalimentacion de las
              // opciones correctas, que ya estaba escrita y no se mostraba.
              cerrar(i, bloque, true, p.retroAcierto || p.opciones
                .filter(o => o.correcta).map(o => o.retro).filter(Boolean).join(' '));"""


def corrige_quiz(html, archivo):
    if "(textoRetro || '')" in html:
        raise SystemExit(f"ABORTA: {archivo} ya tiene corregido el bug del quiz")
    html = una_vez(html, CERRAR_VIEJO, CERRAR_NUEVO, "cerrar() defensivo", archivo)
    html = una_vez(html, MULTIPLE_VIEJO, MULTIPLE_NUEVO,
                   "respaldo de retroalimentación en selección múltiple", archivo)
    return html


# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------

TODOS = [HTMLS / n for n in sorted(p.name for p in HTMLS.glob("capitulo-*.html"))]
TODOS.append(PLANTILLA)

resumen = []
for ruta in TODOS:
    html = ruta.read_text(encoding="utf-8")
    acciones = []

    # (1) el componente, solo donde toca
    nombre = ruta.name
    spec = INSTANCIAS.get(nombre)
    if nombre == PLANTILLA.name:
        spec = PLANTILLA_INSTANCIA
    if spec is not None:
        html = instala_componente(html, nombre)
        html = instala_instancia(html, nombre, spec)
        acciones.append(f"componente + instancia '{spec['id']}'")

    # (2) el bug del quiz, en todos
    html = corrige_quiz(html, nombre)
    acciones.append("corregido el 'undefined' del quiz")

    # comprobaciones
    fallos = []
    if spec is not None:
        fallos += comprueba_tabla_ranking(html, spec["id"])
        for pieza, esperadas in [(".tabla-ranking {", 1), ("function pintarTablaRanking", 1),
                                 ("function iniciarTablasRanking", 1),
                                 ("const TABLAS_RANKING", 1),
                                 ("        iniciarTablasRanking();", 1)]:
            if html.count(pieza) != esperadas:
                fallos.append(f"'{pieza}' aparece {html.count(pieza)} veces, "
                              f"se esperaban {esperadas}")
    if html.count("(textoRetro || '')") != 1:
        fallos.append("la guarda de cerrar() no quedó exactamente una vez")
    if html.count("p.retroAcierto || p.opciones") != 1:
        fallos.append("el respaldo de selección múltiple no quedó exactamente una vez")
    if fallos:
        print(f"ABORTA en {nombre}:")
        for f in fallos:
            print("   -", f)
        raise SystemExit(1)

    ruta.write_text(html, encoding="utf-8")
    resumen.append((nombre, acciones, len(html.encode("utf-8")) / 1024))

print("Retropropagación completada:\n")
for nombre, acciones, kb in resumen:
    print(f"  {nombre:48s} {kb:7.1f} KB   {' · '.join(acciones)}")
print("\nLos capítulos 1 y 2 no reciben el componente: no tienen ninguna tabla")
print("comparativa de modelos que ordenar (mismo criterio que con .mapa-estacional).")
