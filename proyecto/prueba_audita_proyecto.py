#!/usr/bin/env python3
"""prueba_audita_proyecto.py — ¿Caza el auditor lo que dice que caza?

Inyecta un defecto por vez en una COPIA de la guía y exige dos cosas: que
`audita_proyecto.py` falle, y que falle EN EL FRENTE al que ese defecto
pertenece. Un auditor que para por la razón equivocada solo acierta por suerte.
Antes y después corre un control limpio: si el original no pasa, el arnés no
mide nada. Calcado del arnés del proyecto de Diseño.

    python3 proyecto/prueba_audita_proyecto.py

El frente E (código R) solo se corre en los defectos que lo necesitan: tarda
unos segundos y los demás no lo tocan.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
PUBLICADO = AQUI.parent / "Htmls_Series" / "proyecto-pronostico-corte-iii.html"
AUDITOR = AQUI / "audita_proyecto.py"
RMD_FUENTE = AQUI / "plantilla-informe.Rmd"


def cambia(viejo: str, nuevo: str, todas: bool = False):
    def f(t: str) -> str:
        if viejo not in t:
            raise SystemExit(f"!! el arnés no encuentra «{viejo[:60]}»: el defecto no se inyectaría")
        return t.replace(viejo, nuevo, -1 if todas else 1)
    return f


def antes_de_style(extra: str):
    def f(t: str) -> str:
        i = t.index("</style>")
        return t[:i] + extra + t[i:]
    return f


def en_modulo(n: int, extra: str):
    def f(t: str) -> str:
        marca = f'<template id="module-{n}">'
        i = t.index(marca) + len(marca)
        return t[:i] + extra + t[i:]
    return f


# (nombre, frente esperado, transformación, ¿corre R?)
DEFECTOS = [
    # A · Calendario
    ("día de la semana equivocado", "A", cambia("martes 27 de octubre", "lunes 27 de octubre", todas=True), False),
    ("una semana mal en la tabla de hitos", "A",
     cambia("<td>martes 10 de noviembre</td><td>15</td>", "<td>martes 10 de noviembre</td><td>14</td>"), False),
    ("el informe cae en el festivo", "A", cambia("domingo 15 de noviembre", "lunes 16 de noviembre", todas=True), False),
    ("una fecha suelta", "A", en_modulo(6, "<p>Hay una sesión de dudas el jueves 12 de noviembre.</p>"), False),
    ("una hora de cierre distinta", "A", cambia("a las 11:00", "a las 12:30"), False),
    ("un día fijo para la exposición, que se acuerda en clase", "A",
     cambia("<td>se acuerda en clase</td>", "<td>martes 17 de noviembre</td>"), False),
    # B · Pesos
    ("un criterio que ya no suma (la rúbrica da 95)", "B",
     cambia("I2 · Corrección técnica en R</strong> — 8 puntos.", "I2 · Corrección técnica en R</strong> — 3 puntos."), False),
    ("vuelve el 20 % del sílabo en el módulo 1", "B",
     cambia("el proyecto vale el <strong>50 %</strong>", "el proyecto vale el <strong>20 %</strong>"), False),
    ("los quices con otro peso: el corte ya no suma 100", "B",
     cambia("el otro <strong>50 %</strong>", "el otro <strong>40 %</strong>"), False),
    ("un descuento tardío compuesto", "B",
     cambia("<tr><td>2</td><td>30 %</td><td>2,8</td></tr>", "<tr><td>2</td><td>30 %</td><td>2,89</td></tr>"), False),
    ("otra tasa de descuento en la prosa", "B",
     cambia("se descuenta el <strong>15 %</strong>", "se descuenta el <strong>20 %</strong>"), False),
    ("una fila del tope mal calculada", "B", lambda t: re.sub(
        r"(Proyecto impecable que no sabe defender</td>.*?<td><strong>)(\d,\d+)(</strong>)",
        lambda m: m.group(1) + "2,56" + m.group(3), t, count=1, flags=re.S), False),
    ("una exposición que la rúbrica no puede dar", "B", lambda t: re.sub(
        r"(Proyecto impecable que no sabe defender</td><td>\d,\d+</td><td>)\d,\d+",
        r"\g<1>4,5", t, count=1), False),
    ("un módulo con otro peso", "B",
     cambia("vale el <strong>10 %</strong> del proyecto", "vale el <strong>15 %</strong> del proyecto"), False),
    # C · Decisiones
    ("vuelve el examen final", "C", cambia("no tiene examen final ni Talleres 4 y 5",
                                           "tiene examen final y Talleres 4 y 5"), False),
    ("tríos en vez de parejas", "C", cambia("individual o en parejas", "individual o en tríos", todas=True), False),
    ("otro usuario para invitar al docente", "C", cambia("<code>JotaMao1985</code>", "<code>JotaMao1958</code>"), False),
    ("un hito sin su release", "C", cambia("<code>avance</code>.</p>", "<code>avance-final</code>.</p>"), False),
    ("el guion de la exposición se pasa del tiempo", "C",
     cambia("<td>El modelo frente a la referencia, con una figura, y los intervalos</td><td>3</td>",
            "<td>El modelo frente a la referencia, con una figura, y los intervalos</td><td>4</td>"), False),
    ("una longitud mínima mal calculada", "C", cambia("<strong>$230$</strong>", "<strong>$220$</strong>"), False),
    ("vuelven a valer las series simuladas", "C", cambia("Las series simuladas", "Las series inventadas"), False),
    ("desaparece la nueva descarga de la serie", "C",
     cambia("Si no coincide, P1 e I7 quedan en insuficiente.", "Si no coincide, se conversa en la defensa."), False),
    ("I7 deja de castigar una descarga que no coincide", "C", lambda t: re.sub(
        r"(I7 · .*?)o la descarga cruda no coincide con la que se vuelve a\s+descargar de la fuente citada",
        r"\1o el README no existe", t, count=1, flags=re.S), False),
    ("el preregistro pierde un campo", "C",
     cambia("<li><strong>Los niveles de los intervalos</strong>", "<li><strong>El nivel de confianza</strong>"), False),
    ("el preregistro deja de decir que se elige solo con el entrenamiento", "C",
     cambia("solo ese tramo", "todo el tramo"), False),
    # D · Estructura
    ("un enlace roto", "D", cambia('href="capitulo-5-sarima.html#modulo-9"', 'href="capitulo-5-sarimax.html#modulo-9"'), False),
    ("un ancla a un módulo que no existe", "D",
     cambia('href="capitulo-5-sarima.html#modulo-9"', 'href="capitulo-5-sarima.html#modulo-19"'), False),
    ("un id repetido", "D", en_modulo(2, '<span id="dup"></span><span id="dup"></span>'), False),
    ("un resto de la plantilla", "D", en_modulo(3, "<p>Cajas y tipografía</p>"), False),
    ("mojibake", "D", en_modulo(4, "<p>pronÃ³stico</p>"), False),
    ("un «<» sin escapar", "D", en_modulo(5, "<p>si p < 0.05</p>"), False),
    ("un selector CSS de más", "D", antes_de_style("\n    .selector-de-mas { color: red; }\n"), False),
    ("una tabla sin caption", "D", en_modulo(6, "<table><tr><td>x</td></tr></table>"), False),
    # E · Código R
    ("un bloque de R que no corre", "E", cambia("initial = T0 - 1))\nstopifnot", "initial = T0 - 1)\nstopifnot"), True),
    ("la plantilla pierde los grados de libertad del Ljung–Box", "E", "rmd",
     cambia(', fitdf = k)', ')')),
    ("la plantilla vuelve a escribir la serie de ejemplo en datos/", "E", "rmd",
     cambia('    valor = round(100 + 0.3 * t_ej + 8 * sin(2 * pi * t_ej / 12) + ruido, 2))\n',
            '    valor = round(100 + 0.3 * t_ej + 8 * sin(2 * pi * t_ej / 12) + ruido, 2))\n'
            '  dir.create("datos", showWarnings = FALSE); write.csv(serie, "datos/serie.csv", row.names = FALSE)\n')),
    ("la plantilla vuelve a contar la deriva en fitdf", "E", "rmd",
     cambia('o <- arimaorder(modelo)\nk <- sum(o[intersect(names(o), c("p", "q", "P", "Q"))])', "k <- length(coef(modelo))")),
    ("el preregistro vuelve a la pérdida cuadrática con el MASE", "F",
     cambia("h = h, power = 1)", "h = h, power = 2)"), False),
    ("la plantilla vuelve a la fecha con %B", "E", "rmd",
     cambia("paste(as.integer(format(hoy, '%d')), 'de', meses[as.integer(format(hoy, '%m'))], 'de', format(hoy, '%Y'))",
            "format(hoy, '%d de %B de %Y')")),
    # F · Contenido
    ("una referencia a un módulo que trata otra cosa", "F", cambia(">módulo 4.8</a>", ">módulo 4.7</a>"), False),
    ("el texto de un enlace nombra otro módulo", "F",
     cambia('href="capitulo-5-sarima.html#modulo-9">módulo 5.9</a>', 'href="capitulo-5-sarima.html#modulo-9">módulo 5.10</a>'), False),
    ("tsCV con otro primer origen", "F", cambia("initial = T0 - 1", "initial = T0", todas=True), False),
    # G · Módulo 6.12
    ("la guía deja de pedir el MASE por defecto", "G", cambia("El MASE por defecto", "El RMSE por defecto"), False),
    ("una exigencia del 6.12 se queda sin criterio", "G", lambda t: re.sub(
        r"(<tr><td>Cobertura del intervalo</td><td>)I5(</td></tr>)", r"\1\2", t, count=1), False),
    # H · Conjunta
    ("vuelven las parejas mixtas", "H", cambia("no hay parejas mixtas", "puede haber parejas mixtas"), False),
    ("se puede cambiar de opción hasta el informe", "H", cambia("hasta el preregistro", "hasta el informe"), False),
    ("vuelve el kriging como tercera pregunta", "H", lambda t: t.replace(
        "</li>\n        </ol>\n      </div>\n\n      <div class=\"warning\">\n        <p style=\"margin:0;\"><strong>En la (b)",
        "</li>\n          <li><strong>Pronosticar el territorio</strong> por kriging.</li>\n        </ol>\n      </div>\n\n"
        "      <div class=\"warning\">\n        <p style=\"margin:0;\"><strong>En la (b)", 1), False),
    ("la conjunta pesa distinto en cada materia", "H", cambia("lo mismo en las dos", "más en Series que en Espacial"), False),
    ("las reglas se copian en la guía de Espacial", "H",
     cambia("La guía de Espacial las enlaza", "La guía de Espacial las copia"), False),
    ("se pierde el aviso del autoplagio", "H", cambia("autoplagio", "un descuido", todas=True), False),
    ("se pierde el acuerdo individual por escrito", "H",
     cambia("solo con un <strong>acuerdo individual por escrito</strong>\n          con el docente, que fija sus propias reglas",
            "solo en ella"), False),
    ("vuelve la «única situación»", "H",
     cambia("Esta opción está autorizada por escrito aquí.",
            "Esta es la única situación en que un mismo trabajo cuenta en dos cursos, y está autorizada por escrito aquí."),
     False),
]


def audita(ruta: pathlib.Path, con_r: bool, rmd: pathlib.Path | None = None) -> tuple[int, set, str]:
    env = dict(os.environ, PROYECTO_HTML=str(ruta), PROYECTO_SIN_R="0" if con_r else "1")
    if rmd:
        env["PROYECTO_RMD"] = str(rmd)
    r = subprocess.run([sys.executable, str(AUDITOR)], env=env, capture_output=True, text=True)
    frentes = set(re.findall(r"^  MAL \[([A-H])\]", r.stdout, re.M))
    return r.returncode, frentes, r.stdout


def main() -> int:
    original = PUBLICADO.read_text(encoding="utf-8")
    fallos = []
    with tempfile.TemporaryDirectory() as tmp:
        copia = pathlib.Path(tmp) / "guia.html"

        # El de antes corre también el frente E: un control sin R no ve un falso
        # positivo del frente E, y los defectos de R pasarían por cazados igual.
        def control(cuando: str, con_r: bool = False) -> None:
            copia.write_text(original, encoding="utf-8")
            rc, fr, _ = audita(copia, con_r=con_r)
            ok = rc == 0 and not fr
            print(f"  {'OK ' if ok else 'MAL'}  control limpio ({cuando})")
            if not ok:
                fallos.append(f"control {cuando}: {sorted(fr)}")

        print("=== prueba_audita_proyecto.py ===\n")
        control("antes, con R", con_r=True)
        rmd = pathlib.Path(tmp) / "plantilla.Rmd"
        for nombre, frente, transforma, con_r in DEFECTOS:
            if transforma == "rmd":      # el defecto va en la plantilla, la guía queda intacta
                copia.write_text(original, encoding="utf-8")
                rmd.write_text(con_r(RMD_FUENTE.read_text(encoding="utf-8")), encoding="utf-8")
                rc, fr, _ = audita(copia, True, rmd)
            else:
                nuevo = transforma(original)
                if nuevo == original:
                    raise SystemExit(f"!! el defecto «{nombre}» no cambió nada")
                copia.write_text(nuevo, encoding="utf-8")
                rc, fr, _ = audita(copia, con_r)
            ok = rc == 1 and frente in fr
            print(f"  {'OK ' if ok else 'MAL'}  [{frente}] {nombre}"
                  + ("" if ok else f"  (salida {rc}, frentes {sorted(fr)})"))
            if not ok:
                fallos.append(nombre)
        control("después")

    cazados = len(DEFECTOS) - len([f for f in fallos if not f.startswith("control")])
    print(f"\n  {len(DEFECTOS)} defectos inyectados · {cazados} cazados por su frente")
    if fallos:
        print("\nNo cazados o controles sucios:")
        for f in fallos:
            print(f"  · {f}")
        return 1
    print("Todo cazado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
