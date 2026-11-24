#!/usr/bin/env python3
"""R3 · barrido de secuencias de escape involuntarias (hallazgo V1 del verificador).

1. En las listas de ediciones (`r3_ediciones_*.py`): toda cadena literal que NO sea cruda y contenga
   una barra invertida seguida de t, n, b, f, r, v o a pegada a letras (\\text, \\nabla, \\bar, \\frac,
   \\rho, \\theta, \\varepsilon, \\alpha…) es sospechosa: Python la convierte en un carácter de control.
2. En el HTML ensamblado del capítulo 5 y en las plantillas: caracteres de control (tabulador, \\b, \\f,
   \\v, \\a, \\r) y, dentro de las fórmulas ($…$ y $$…$$), restos de comandos sin su barra («ext{»,
   «rac{», «ar{», «abla», «heta», «imes», «arepsilon», «lpha», «ho_»), comparados con HEAD.
Sale con 1 si hay algo nuevo respecto de HEAD.
Uso: python3 diagnostico/cap5/comprobaciones/r3_control.py
"""
import io
import pathlib
import re
import subprocess
import sys
import tokenize

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
fallos = 0

print("== 1. Cadenas no crudas con escapes sospechosos en las listas de ediciones")
SOSP = re.compile(r"\\[tnbfrva][a-zA-Z]")
for p in sorted(AQUI.glob("r3_ediciones_*.py")):
    for tok in tokenize.generate_tokens(io.StringIO(p.read_text(encoding="utf-8")).readline):
        if tok.type != tokenize.STRING:
            continue
        prefijo = re.match(r"[a-zA-Z]*", tok.string).group(0).lower()
        if "r" in prefijo:
            continue
        for m in SOSP.finditer(tok.string):
            if tok.string[max(0, m.start() - 1)] == "\\":
                continue          # «\\t» escrito doble: es una barra literal
            print(f"   SOSPECHOSA {p.name}:{tok.start[0]}  …{tok.string[max(0, m.start() - 20):m.end() + 10]!r}")
            fallos += 1
print("   ninguna" if not fallos else f"   {fallos} sospechosas")

CONTROL = re.compile(r"[\t\x07\x08\x0b\x0c\r]")
RESTOS = re.compile(r"(?<![\\A-Za-z])(ext\{|rac\{|ar\{|abla|heta|imes|arepsilon|lpha|ho_)")
FORM = re.compile(r"\$\$.*?\$\$|\$[^$]+\$", re.S)


def cuenta(texto):
    ctrl = len(CONTROL.findall(texto))
    restos = [m.group(0) for f in FORM.finditer(texto) for m in RESTOS.finditer(f.group(0))]
    return ctrl, restos


def head(ruta):
    return subprocess.run(["git", "show", f"HEAD:{ruta}"], cwd=RAIZ, capture_output=True, text=True).stdout


print("\n== 2. Caracteres de control y comandos sin barra (árbol frente a HEAD)")
archivos = ["Htmls_Series/capitulo-5-sarima.html", "ensamblado/cap5/templates_1_3.html",
            "ensamblado/cap5/templates_4_6.html", "ensamblado/cap5/templates_7_9.html",
            "ensamblado/cap5/templates_10_11.html", "ensamblado/cap5/chapter.js",
            "Htmls_Series/diapositivas/fuentes/capitulo_5.md"]
for a in archivos:
    ahora = (RAIZ / a).read_text(encoding="utf-8")
    c1, r1 = cuenta(ahora)
    c0, r0 = cuenta(head(a))
    nuevo = c1 > c0 or len(r1) > len(r0)
    fallos += nuevo
    print(f"   {'NUEVO ' if nuevo else 'igual '} {a}: control {c0} -> {c1}; restos en fórmulas {len(r0)} -> {len(r1)}"
          + (f"  {sorted(set(r1))}" if r1 else ""))
    if nuevo:
        for i, linea in enumerate(ahora.splitlines(), 1):
            if CONTROL.search(linea) and not CONTROL.search(linea.replace("\t", "")) is None:
                pass
            if CONTROL.search(linea):
                print(f"      l. {i}: {linea.strip()[:120]!r}")
print(f"\n{'HAY ' + str(fallos) + ' COSAS QUE REVISAR' if fallos else 'TODO EN ORDEN'}")
sys.exit(1 if fallos else 0)
