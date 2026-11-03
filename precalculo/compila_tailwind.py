#!/usr/bin/env python3
"""
compila_tailwind.py — el CSS de Tailwind compilado, en vez del Play CDN

Material de Series de Tiempo 2026-II (20948).

Hasta el 2026-11-03 las doce páginas del sitio cargaban `cdn.tailwindcss.com`,
el Play CDN, que genera la hoja en el navegador a partir de las clases del DOM.
En una red cuyo DNS no resuelve ese dominio —la de casa del autor, ese día— la
página se queda sin maquetar: la barra lateral se apila encima del contenido,
el título de la cabecera sale oscuro sobre fondo oscuro y `tailwind.config = …`
lanza un ReferenceError. Tailwind presenta el Play CDN para desarrollo, no para
producción.

Este guion compila con Tailwind 3.4.19 —la v3 que sirve el CDN— la misma
configuración que cada página llevaba inline, y la pone en un
`<style id="tailwind-compilado">` al FINAL de <head>. Ahí anexaba el CDN su
hoja, detrás del <style> de la página, así que la cascada no cambia: el bloque
que reafirma la tipografía sobre el Preflight (9e20658) sigue haciendo falta y
sigue funcionando igual.

Dos hojas, porque hay dos configuraciones:
  · PAGINAS: los seis capítulos, los dos preparciales, los dos talleres, el
    proyecto y la plantilla, que comparten configuración byte a byte.
  · INDEX: la portada, cuya configuración no define la fuente `mono`.

El compilador lee las clases del TEXTO de los archivos, incluido el JavaScript
inline y las fuentes de `ensamblado/` y `proyecto/modulos/`. El CDN las leía
del DOM. El 2026-11-03 se comprobó que toda clase presente en el DOM de las doce
páginas, recorriendo todos sus módulos, está escrita literalmente en su código;
las que no, las pone KaTeX o Prism y no son utilidades de Tailwind. Si algún día
una clase se arma concatenando cadenas, el compilador no la verá: hay que
escribirla entera.

Los capítulos 3 a 6 los arma `ensamblado/ensambla_capN.py` sobre el anterior,
empezando por el 2, así que heredan la cabecera. Este guion los toca igual que
a los demás, con la misma hoja; reensamblarlos después debe dejarlos idénticos.

Uso (desde la raíz del repositorio; necesita node y npx):

    python3 precalculo/compila_tailwind.py --instalar    # una vez: quita el CDN y su configuración
    python3 precalculo/compila_tailwind.py               # recompila y sustituye la hoja de cada página
    python3 precalculo/compila_tailwind.py --comprobar   # sale con 1 si alguna página quedó desfasada

`TAILWIND_CLI` puede apuntar a un `tailwindcss` ya instalado; si no, se usa
`npx --yes tailwindcss@3.4.19`.
"""

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITIO = RAIZ / "Htmls_Series"
VERSION = "3.4.19"

PAGINAS = [
    "capitulo-1-componentes-descomposicion.html", "capitulo-2-estacionariedad-acf-pacf.html",
    "capitulo-3-modelos-ar-ma-arma.html", "capitulo-4-modelos-arima.html",
    "capitulo-5-sarima.html", "capitulo-6-pronostico-evaluacion.html",
    "preparcial-corte-1.html", "preparcial-corte-2.html",
    "proyecto-pronostico-corte-iii.html", "taller-1-modulo-1.html", "taller-2-modulo-2.html",
]
PLANTILLA = RAIZ / "plantilla" / "plantilla-capitulo.html"
INDEX = SITIO / "index.html"

COLORES = """colors: { primary: '#012820', secondary: '#FF6600', navy: '#012820', gold: '#FFC24B',
              bg: '#F8FAFC', surface: '#FFFFFF' },"""

# Lo que el compilador lee para encontrar clases. Leer de más solo añade reglas
# que no casan con ningún elemento; leer de menos deja elementos sin estilo.
# Las páginas van como texto ya limpio de su propia hoja compilada: si no, sus
# selectores contarían como clases usadas y cada pasada daría una hoja distinta.
FUENTES_PAGINAS = [SITIO / p for p in PAGINAS] + [PLANTILLA]
GLOBS_PAGINAS = [str(RAIZ / "proyecto/modulos/*.html"), str(RAIZ / "precalculo/ensambla_proyecto.py"),
                 str(RAIZ / "ensamblado/**/*.{html,js,py}")]
FUENTES_INDEX = [INDEX]

TEMA_PAGINAS = """fontFamily: { sans: ['Montserrat', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
                  mono: ['Fira Code', 'monospace'] },
    """ + COLORES
TEMA_INDEX = """fontFamily: { sans: ['Montserrat', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'] },
    """ + COLORES


def config(fuentes, globs, tema):
    contenido = [{"raw": ESTILO_RE.sub("", f.read_text(encoding="utf-8")), "extension": "html"} for f in fuentes]
    return "module.exports = {\n  content: %s,\n  theme: { extend: {\n    %s\n  } },\n};\n" % (
        json.dumps(contenido + globs, ensure_ascii=False), tema)

AVISO = ("  <!-- Tailwind CSS v%s compilado (precalculo/compila_tailwind.py), en lugar del Play CDN\n"
         "       cdn.tailwindcss.com, que en algunas redes no resuelve y dejaba la página sin maquetar.\n"
         "       Va al final de <head>, donde el CDN anexaba su hoja: detrás del <style> de la página. -->\n" % VERSION)
ESTILO_RE = re.compile(r'<style id="tailwind-compilado">.*?</style>', re.S)
CDN_RE = re.compile(r'[ \t]*<script src="https://cdn\.tailwindcss\.com"></script>\n')
# La configuración inline: el <script> que asigna `tailwind.config`, con su
# comentario de cabecera si lo tiene (los capítulos sí, la portada no).
CONFIG_RE = re.compile(r'(?:[ \t]*<!-- Tailwind Configuration -->\n)?[ \t]*<script>\s*tailwind\.config\s*=.*?</script>\n', re.S)


def compila(config_js):
    cli = os.environ.get("TAILWIND_CLI")
    orden = shlex.split(cli) if cli else ["npx", "--yes", "tailwindcss@" + VERSION]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "tailwind.config.cjs").write_text(config_js, encoding="utf-8")
        (tmp / "entrada.css").write_text("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
        r = subprocess.run(orden + ["-c", str(tmp / "tailwind.config.cjs"), "-i", str(tmp / "entrada.css"),
                                    "-o", str(tmp / "salida.css"), "--minify"], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("ERROR: el compilador de Tailwind falló:\n" + r.stderr)
        css = (tmp / "salida.css").read_text(encoding="utf-8").strip()
    # Una sola línea y sin `\n  </style>`: varios ensambladores se orientan por
    # la cadena «  </style>» de la cabecera y exigen que aparezca una sola vez.
    return css.replace("\n", "")


def bloque(css):
    return AVISO + '  <style id="tailwind-compilado">' + css + "</style>\n"


def instala(t, css, nombre):
    n_cdn, n_cfg = len(CDN_RE.findall(t)), len(CONFIG_RE.findall(t))
    if ESTILO_RE.search(t):
        sys.exit(f"ERROR [{nombre}]: ya tiene la hoja compilada; usa el guion sin --instalar")
    if n_cdn != 1 or n_cfg != 1:
        sys.exit(f"ERROR [{nombre}]: esperaba 1 script del CDN y 1 configuración, hay {n_cdn} y {n_cfg}")
    t = CONFIG_RE.sub("", CDN_RE.sub("", t))
    if t.count("</head>") != 1:
        sys.exit(f"ERROR [{nombre}]: </head> no aparece exactamente una vez")
    return t.replace("</head>", bloque(css) + "</head>", 1)


def sustituye(t, css, nombre):
    if len(ESTILO_RE.findall(t)) != 1:
        sys.exit(f"ERROR [{nombre}]: no tiene exactamente un <style id=\"tailwind-compilado\">; ¿falta --instalar?")
    return ESTILO_RE.sub(lambda m: '<style id="tailwind-compilado">' + css + "</style>", t)


def main():
    instalar, comprobar = "--instalar" in sys.argv, "--comprobar" in sys.argv
    hojas = {"paginas": compila(config(FUENTES_PAGINAS, GLOBS_PAGINAS, TEMA_PAGINAS)),
             "index": compila(config(FUENTES_INDEX, [], TEMA_INDEX))}
    destinos = [(SITIO / p, "paginas") for p in PAGINAS] + [(PLANTILLA, "paginas"), (INDEX, "index")]
    desfasadas = []
    for ruta, hoja in destinos:
        t = ruta.read_text(encoding="utf-8")
        nuevo = instala(t, hojas[hoja], ruta.name) if instalar else sustituye(t, hojas[hoja], ruta.name)
        if nuevo == t:
            continue
        if comprobar:
            desfasadas.append(ruta.relative_to(RAIZ))
        else:
            ruta.write_text(nuevo, encoding="utf-8")
            print(f"escrito  {ruta.relative_to(RAIZ)}")
    print(f"hojas: páginas {len(hojas['paginas']) / 1024:.1f} KB · portada {len(hojas['index']) / 1024:.1f} KB")
    if comprobar:
        for d in desfasadas:
            print(f"DESFASADA  {d}")
        sys.exit(1 if desfasadas else 0)


if __name__ == "__main__":
    main()
