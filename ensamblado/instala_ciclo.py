#!/usr/bin/env python3
"""Instala el componente `.ciclo` en la plantilla y en los capítulos 1, 2 y 3.

Sigue las dos reglas del README de esta carpeta:
  1. toda sustitución exige que su marcador aparezca EXACTAMENTE una vez;
  2. al final se comprueba que el resultado contiene todo lo que debe.

El capítulo 4 no aparece aquí a propósito: se ensambla a partir del 3, así que
hereda el componente por construcción — que es justo el objetivo del método de
sustitución de regiones.

Uso:  python3 instala_ciclo.py            (desde ensamblado/)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "componentes"))
from ciclo_html import ciclo_html, comprueba_ciclo   # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
COMPONENTES = Path(__file__).resolve().parent / "componentes"

CSS = (COMPONENTES / "ciclo.css").read_text(encoding="utf-8")
JS = (COMPONENTES / "ciclo.js").read_text(encoding="utf-8")

MARCA_CSS = "  </style>"
MARCA_JS = "    function iniciarDerivaciones() {"
MARCA_LLAMADA = "        iniciarDerivaciones();"


def sustituye_una_vez(texto, marcador, nuevo, etiqueta):
    n = texto.count(marcador)
    if n != 1:
        raise SystemExit(f"ABORTA [{etiqueta}]: el marcador aparece {n} veces, "
                         f"se esperaba 1.\n  marcador: {marcador!r}")
    return texto.replace(marcador, nuevo, 1)


# ---------------------------------------------------------------------------
# Instancias del componente, una por archivo
# ---------------------------------------------------------------------------

CICLO_PLANTILLA = ciclo_html(
    "demo",
    [
        {
            "clave": "planear", "numero": "Etapa 1", "titulo": "Planear",
            "resumen": "¿Qué se quiere responder?",
            "campos": [
                ("Qué haces", "<p>Se describe la etapa en una o dos frases. Este componente "
                              "es para procedimientos que se <strong>recorren</strong> y en los "
                              "que se vuelve atrás; si los pasos nunca se repiten, usa la caja "
                              "<code>.diagram</code> con una lista y ya está.</p>"),
                ("Con qué", "<p>Aquí van las funciones concretas: <code>funcion()</code> en R, "
                            "<code>metodo()</code> en Python.</p>"),
            ],
            "vuelta": "<p>La etapa 1 es el principio: no se vuelve a ella desde ningún sitio "
                      "salvo desde el diagnóstico final.</p>",
        },
        {
            "clave": "hacer", "numero": "Etapa 2", "titulo": "Hacer",
            "resumen": "Ejecutar y medir",
            "campos": [
                ("Qué haces", "<p>Las fórmulas de KaTeX funcionan dentro del panel, "
                              "incluidas las de bloque: $\\hat{y}_{t} = \\phi y_{t-1}$.</p>"),
                ("Con qué", "<p><code>otra_funcion(x, opcion = TRUE)</code></p>"),
            ],
            "vuelta": "<p>Si el resultado no converge, se vuelve a la etapa 1 con otra "
                      "especificación.</p>",
        },
        {
            "clave": "comprobar", "numero": "Etapa 3", "titulo": "Comprobar",
            "resumen": "¿Se sostiene?",
            "campos": [
                ("Qué haces", "<p>La última etapa es la que cierra el ciclo: su resultado "
                              "decide si se termina o si se vuelve al principio.</p>"),
                ("Con qué", "<p><code>diagnostico(ajuste)</code></p>"),
            ],
            "vuelta": "<p>Si la comprobación falla, el ciclo entero empieza otra vez. Esa "
                      "flecha de vuelta es lo que una lista numerada no sabe dibujar.</p>",
        },
    ],
    "El ciclo se recorre con clic o con las flechas del teclado, y vuelve al principio "
    "cuantas veces haga falta.",
)

CICLO_CAP1 = ciclo_html(
    "descomposicion",
    [
        {
            "clave": "escala", "numero": "Paso 1", "titulo": "Elegir la escala",
            "resumen": "¿Aditiva o multiplicativa?",
            "campos": [
                ("Qué haces", "<p>Mirar si la amplitud estacional <strong>crece con el nivel</strong> "
                              "de la serie. Si crece, el modelo es multiplicativo "
                              "$y_t = T_t \\times S_t \\times R_t$; si se mantiene, aditivo "
                              "$y_t = T_t + S_t + R_t$. Trabajar en logaritmos convierte el "
                              "segundo caso en el primero.</p>"),
                ("Con qué", "<p><code>autoplot(y)</code> y el gráfico estacional "
                            "<code>gg_season(y)</code>; en Python, <code>y.plot()</code>. "
                            "La decisión es visual, no hay prueba automática.</p>"),
            ],
            "vuelta": "<p>Si al final el residuo $\\hat{R}_t$ conserva la forma estacional "
                      "abombada, la escala estaba mal elegida.</p>",
        },
        {
            "clave": "tendencia", "numero": "Paso 2", "titulo": "Estimar la tendencia",
            "resumen": "Media móvil de orden $m$",
            "campos": [
                ("Qué haces", "<p>Suavizar con una media móvil centrada del orden del período. "
                              "Con $m$ par hace falta la media móvil $2\\times m$ para que quede "
                              "centrada, y eso cuesta $m/2$ observaciones en cada extremo.</p>"),
                ("Con qué", "<p><code>stats::filter(y, rep(1/m, m))</code> o directamente "
                            "<code>decompose()</code>; en Python, "
                            "<code>seasonal_decompose()</code>.</p>"),
            ],
            "vuelta": "<p>Si la tendencia estimada ondula al ritmo de la estacionalidad, el "
                      "orden $m$ no coincide con el período real.</p>",
        },
        {
            "clave": "estacionalidad", "numero": "Paso 3", "titulo": "Estimar la estacionalidad",
            "resumen": "Promedio por posición",
            "campos": [
                ("Qué haces", "<p>Quitar la tendencia (restando o dividiendo, según la escala) "
                              "y promediar por posición estacional. Los índices resultantes son "
                              "<strong>fijos</strong> para toda la serie: esa es la limitación "
                              "central del método clásico.</p>"),
                ("Con qué", "<p>El componente <code>$seasonal</code> de <code>decompose()</code>; "
                            "STL lo hace variar en el tiempo.</p>"),
            ],
            "vuelta": "<p>Si los índices no sirven igual al principio y al final de la muestra, "
                      "la estacionalidad cambia: hay que pasar a STL.</p>",
        },
        {
            "clave": "residuo", "numero": "Paso 4", "titulo": "Analizar el residuo",
            "resumen": "¿Queda estructura?",
            "campos": [
                ("Qué haces", "<p>Mirar $\\hat{R}_t$: debe parecer ruido, sin ciclos ni "
                              "abombamientos ni atípicos concentrados. Es la comprobación de "
                              "que la descomposición hizo su trabajo.</p>"),
                ("Con qué", "<p>El panel de residuo de <code>decompose()</code> o de "
                            "<code>STL()</code>, y las fuerzas $F_T$ y $F_S$ del Módulo 8.</p>"),
            ],
            "vuelta": "<p>Estructura en el residuo manda de vuelta al paso 1 (escala) o al 2 "
                      "(orden de la media móvil). Este es el bucle del método.</p>",
        },
    ],
    "Descomponer no es una fórmula sino un ciclo: el residuo es quien dice si hay que volver.",
)

CICLO_CAP2 = ciclo_html(
    "preprocesamiento",
    [
        {
            "clave": "graficar", "numero": "Paso 1", "titulo": "Graficar la serie",
            "resumen": "Antes que nada",
            "campos": [
                ("Qué haces", "<p>Buscar <strong>saltos de nivel, cambios de régimen, datos "
                              "faltantes y atípicos</strong>. Ninguna prueba automática los "
                              "detecta por ti, y todos ellos desbaratan las que vienen después.</p>"),
                ("Con qué", "<p><code>autoplot(y)</code>, <code>gg_season(y)</code>, "
                            "<code>gg_lag(y)</code>; en Python, <code>y.plot()</code>.</p>"),
            ],
            "vuelta": "<p>Es el principio del pipeline. Se vuelve aquí cada vez que un paso "
                      "posterior da un resultado que no encaja con lo que se ve en el gráfico.</p>",
        },
        {
            "clave": "varianza", "numero": "Paso 2", "titulo": "Estabilizar la varianza",
            "resumen": "¿Crece la dispersión?",
            "campos": [
                ("Qué haces", "<p>Si la dispersión crece con el nivel, transformar "
                              "<strong>antes</strong> de diferenciar: logaritmo o Box–Cox. El "
                              "orden importa, porque diferenciar no arregla una varianza que "
                              "cambia.</p>"),
                ("Con qué", "<p><code>BoxCox.lambda(y, method = \"guerrero\")</code> y "
                            "<code>BoxCox()</code> (Módulo 8); en Python, "
                            "<code>scipy.stats.boxcox</code>.</p>"),
            ],
            "vuelta": "<p>Si el $\\lambda$ elegido deja el gráfico igual de abombado, o si la "
                      "serie tiene ceros o negativos, hay que replantear la transformación.</p>",
        },
        {
            "clave": "estacional", "numero": "Paso 3", "titulo": "Diferencia estacional",
            "resumen": "$\\nabla_m$ primero",
            "campos": [
                ("Qué haces", "<p>Si hay estacionalidad, aplicar $\\nabla_m$ <strong>antes</strong> "
                              "que la diferencia regular. Hacerlo al revés cambia el número de "
                              "diferencias que hace falta: es la trampa del orden del Módulo 7.</p>"),
                ("Con qué", "<p><code>nsdiffs(y)</code> y <code>difference(y, lag = m)</code>; "
                            "en Python, <code>y.diff(m)</code>.</p>"),
            ],
            "vuelta": "<p>Si tras diferenciar siguen apareciendo picos en los rezagos múltiplos "
                      "de $m$, falta una diferencia estacional más.</p>",
        },
        {
            "clave": "regular", "numero": "Paso 4", "titulo": "Diferencia regular",
            "resumen": "$\\nabla$ si queda tendencia",
            "campos": [
                ("Qué haces", "<p>Comprobar si queda tendencia o raíz unitaria y aplicar "
                              "$\\nabla$. Nunca sobre una serie estacional cruda: el ADF puede "
                              "rechazar la raíz unitaria solo porque usa menos rezagos que el "
                              "período (Módulo 6).</p>"),
                ("Con qué", "<p><code>ndiffs(y)</code>, <code>adf.test()</code>, "
                            "<code>kpss.test()</code>, ACF; en Python, <code>adfuller</code> "
                            "y <code>kpss</code>.</p>"),
            ],
            "vuelta": "<p>Si la varianza <em>sube</em> al diferenciar, te pasaste: vuelve con "
                      "una diferencia menos.</p>",
        },
        {
            "clave": "verificar", "numero": "Paso 5", "titulo": "Verificar",
            "resumen": "¿Ya es estacionaria?",
            "campos": [
                ("Qué haces", "<p>ACF y PACF de la serie transformada, repetir las pruebas y "
                              "comprobar que la varianza <strong>no subió</strong>. Este paso es "
                              "el que cierra el ciclo y manda de vuelta a los anteriores.</p>"),
                ("Con qué", "<p><code>ACF()</code>/<code>PACF()</code> de feasts, "
                            "<code>adf.test()</code>, <code>kpss.test()</code> y "
                            "<code>var()</code> por cada $d$.</p>"),
            ],
            "vuelta": "<p>ACF que no decae → paso 4. Varianza que crece → paso 4 con una "
                      "diferencia menos. Abombamiento → paso 2. Un salto de nivel que no viste "
                      "→ paso 1.</p>",
        },
        {
            "clave": "documentar", "numero": "Paso 6", "titulo": "Documentar",
            "resumen": "Para poder deshacerlo",
            "campos": [
                ("Qué haces", "<p>Anotar qué transformaciones se aplicaron y en qué orden. Sin "
                              "eso, los pronósticos del Capítulo 6 <strong>no se pueden devolver "
                              "a la escala original</strong>, y un pronóstico en escala "
                              "logarítmica y diferenciada no se lo puedes enseñar a nadie.</p>"),
                ("Con qué", "<p>Guardar $\\lambda$, $d$ y $D$ junto al objeto del modelo; "
                            "<code>fable</code> lo hace por ti si transformas dentro de la "
                            "fórmula.</p>"),
            ],
        },
    ],
    "Cada paso condiciona el diagnóstico del siguiente: por eso el orden no es negociable "
    "y por eso se vuelve atrás.",
)

CICLO_CAP3 = ciclo_html(
    "identificacion-arma",
    [
        {
            "clave": "acf", "numero": "Paso 1", "titulo": "Leer la ACF",
            "resumen": "¿Decae o corta?",
            "campos": [
                ("Qué haces", "<p>Si la ACF <strong>corta</strong> tras el rezago $q$, hay una "
                              "parte MA($q$). Si <strong>decae</strong> —geométrica o con ondas—, "
                              "la parte MA no manda y hay que mirar la PACF.</p>"),
                ("Con qué", "<p><code>acf(y, lag.max = 20)</code>; en Python, "
                            "<code>plot_acf(y)</code>. La banda $\\pm 1.96/\\sqrt{n}$ marca "
                              "qué es ruido.</p>"),
            ],
            "vuelta": "<p>Si la ACF no decae en absoluto, la serie no es estacionaria: esto no "
                      "es un problema de identificación sino del Capítulo 2.</p>",
        },
        {
            "clave": "pacf", "numero": "Paso 2", "titulo": "Leer la PACF",
            "resumen": "¿Decae o corta?",
            "campos": [
                ("Qué haces", "<p>Si la PACF corta tras el rezago $p$, hay una parte AR($p$). "
                              "Si <strong>las dos</strong> decaen sin cortar, es un ARMA mixto y "
                              "la tabla ya no basta: hay que probar.</p>"),
                ("Con qué", "<p><code>pacf(y)</code> — ojo, <code>pacf(y)$acf</code> devuelve un "
                            "array de tres dimensiones; envuélvelo en <code>as.numeric()</code>.</p>"),
            ],
            "vuelta": "<p>Un corte limpio en la teoría se vuelve borroso con datos reales: con "
                      "$n$ pequeño, vuelve al paso 1 sabiendo que la banda es ancha.</p>",
        },
        {
            "clave": "proponer", "numero": "Paso 3", "titulo": "Proponer $(p, q)$",
            "resumen": "Con la tabla",
            "campos": [
                ("Qué haces", "<p>Cruzar las dos lecturas en la tabla de identificación. Proponer "
                              "<strong>varios</strong> candidatos vecinos, no uno: la tabla acota "
                              "la búsqueda, no la resuelve.</p>"),
                ("Con qué", "<p><code>arima(y, order = c(p, 0, q))</code> para cada candidato, y "
                            "los criterios AICc/BIC del Módulo 8 para compararlos.</p>"),
            ],
            "vuelta": "<p>Si ningún candidato pasa el diagnóstico, vuelve aquí y amplía el "
                      "conjunto antes de dar por buena la lectura de los correlogramas.</p>",
        },
        {
            "clave": "comprobar", "numero": "Paso 4", "titulo": "Comprobar",
            "resumen": "Teórica vs. muestral",
            "campos": [
                ("Qué haces", "<p>Enfrentar la ACF/PACF <strong>teórica</strong> del modelo "
                              "propuesto contra la muestral, y revisar los residuales. Es el paso "
                              "que convierte una corazonada en un modelo.</p>"),
                ("Con qué", "<p><code>ARMAacf()</code> para la teórica y "
                            "<code>Box.test(..., type = \"Ljung-Box\", fitdf = p + q)</code> para "
                            "los residuales.</p>"),
            ],
            "vuelta": "<p>Residuales con estructura → paso 3 con otro candidato. Curvas teórica "
                      "y muestral que no se parecen ni de lejos → paso 1.</p>",
        },
    ],
    "Identificar es un ciclo de conjeturas, no una lectura única: el diagnóstico devuelve al "
    "correlograma tantas veces como haga falta.",
)


# ---------------------------------------------------------------------------
# Dónde va cada instancia
# ---------------------------------------------------------------------------

ANCLA_PLANTILLA = """      <p>Este es un párrafo normal. El cuerpo del texto va justificado y con interlineado 1.625. Los términos técnicos
        se marcan en <strong>negrita</strong> la primera vez, y su equivalente en inglés va en <em>cursiva entre
        paréntesis</em> (<em>technical term</em>).</p>
"""

ANCLA_CAP1 = """      <div class="simulador" data-simulador="descomp-clasica">
"""

ANCLA_CAP3 = """      <div class="definition">
        <h4><i class="fas fa-book mr-2" aria-hidden="true"></i>Definición: proceso ARMA($p,q$)</h4>
"""

# En el capítulo 2 el ciclo SUSTITUYE a la caja `.diagram` con la lista del
# pipeline: dice lo mismo y además dice qué te hace volver atrás. Dejar las dos
# sería repetir el contenido del módulo entero.
DIAGRAM_CAP2 = """      <div class="diagram">
        <ol>
          <li><strong>Graficar la serie.</strong> Antes que nada. Buscar saltos de nivel, cambios de régimen, datos
            faltantes y atípicos, que ninguna prueba automática detecta por ti.</li>
          <li><strong>¿La dispersión crece con el nivel?</strong> → logaritmo o Box–Cox (Módulo 8).</li>
          <li><strong>¿Hay estacionalidad?</strong> → diferencia estacional $\\nabla_m$ primero
            (<code>nsdiffs()</code>).</li>
          <li><strong>¿Queda tendencia o raíz unitaria?</strong> → diferencia regular $\\nabla$
            (<code>ndiffs()</code>, ACF, pruebas ADF/KPSS).</li>
          <li><strong>Verificar.</strong> ACF/PACF de la serie transformada, pruebas de nuevo, y comprobar que la
            varianza no subió (señal de sobrediferenciación).</li>
          <li><strong>Documentar</strong> qué transformaciones se aplicaron: sin eso, los pronósticos del Capítulo 6 no
            se pueden devolver a la escala original.</li>
        </ol>
      </div>
"""

TRABAJOS = [
    dict(ruta=RAIZ / "plantilla" / "plantilla-capitulo.html",
         id_base="demo", etapas=3, ciclo=CICLO_PLANTILLA,
         ancla=ANCLA_PLANTILLA, modo="antes"),
    dict(ruta=RAIZ / "Htmls_Series" / "capitulo-1-componentes-descomposicion.html",
         id_base="descomposicion", etapas=4, ciclo=CICLO_CAP1,
         ancla=ANCLA_CAP1, modo="antes"),
    dict(ruta=RAIZ / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html",
         id_base="preprocesamiento", etapas=6, ciclo=CICLO_CAP2,
         ancla=DIAGRAM_CAP2, modo="sustituye"),
    dict(ruta=RAIZ / "Htmls_Series" / "capitulo-3-modelos-ar-ma-arma.html",
         id_base="identificacion-arma", etapas=4, ciclo=CICLO_CAP3,
         ancla=ANCLA_CAP3, modo="antes"),
]


def main():
    for t in TRABAJOS:
        ruta = t["ruta"]
        if not ruta.exists():
            raise SystemExit(f"ABORTA: no existe {ruta}")
        html = ruta.read_text(encoding="utf-8")
        nombre = ruta.name

        if "data-ciclo=" in html or ".ciclo-boton" in html:
            raise SystemExit(f"ABORTA [{nombre}]: ya tiene el componente .ciclo. "
                             "Este script solo se ejecuta una vez por archivo.")

        html = sustituye_una_vez(html, MARCA_CSS, CSS + MARCA_CSS, f"{nombre}/css")
        html = sustituye_una_vez(html, MARCA_JS, JS + MARCA_JS, f"{nombre}/js")
        html = sustituye_una_vez(html, MARCA_LLAMADA,
                                 MARCA_LLAMADA + "\n        iniciarCiclos();",
                                 f"{nombre}/llamada")

        if t["modo"] == "sustituye":
            html = sustituye_una_vez(html, t["ancla"], t["ciclo"], f"{nombre}/instancia")
        else:
            html = sustituye_una_vez(html, t["ancla"], t["ciclo"] + "\n" + t["ancla"],
                                     f"{nombre}/instancia")

        # --- Comprobaciones finales -------------------------------------
        fallos = comprueba_ciclo(html, t["id_base"], t["etapas"])
        for regla in [".ciclo {", ".ciclo-etapas {", ".ciclo-boton {", ".ciclo-numero {",
                      ".ciclo-titulo {", ".ciclo-resumen {", ".ciclo-retorno {",
                      ".ciclo-panel {", ".ciclo-campo {", ".ciclo-etiqueta {",
                      ".ciclo-vuelta {"]:
            if regla not in html:
                fallos.append(f"falta la regla CSS {regla}")
        if html.count("function iniciarCiclos()") != 1:
            fallos.append("iniciarCiclos() no aparece exactamente una vez")
        if html.count("        iniciarCiclos();") != 1:
            fallos.append("la llamada a iniciarCiclos() no aparece exactamente una vez")
        if html.count('role="tablist" aria-label="Etapas del ciclo"') != 1:
            fallos.append("el tablist del ciclo no aparece exactamente una vez")
        # El componente que ya existía tiene que seguir intacto
        if "function iniciarDerivaciones()" not in html:
            fallos.append("se perdió iniciarDerivaciones()")
        if fallos:
            raise SystemExit(f"ABORTA [{nombre}]:\n  - " + "\n  - ".join(fallos))

        ruta.write_text(html, encoding="utf-8")
        print(f"OK  {nombre}: componente .ciclo instalado "
              f"(instancia '{t['id_base']}', {t['etapas']} etapas)")

    print("\nHecho. El capítulo 4 heredará el componente al ensamblarse desde el 3.")


if __name__ == "__main__":
    main()
