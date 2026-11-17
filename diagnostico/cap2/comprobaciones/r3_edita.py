#!/usr/bin/env python3
"""R3 · ayudante de edicion: aplica sustituciones exactas y unicas al capitulo 2.

Cada sustitucion es (texto_antes, texto_despues). El guion se niega a escribir
si un `antes` no aparece exactamente una vez: asi ninguna edicion cae en otro
sitio ni se pierde en silencio. Las listas de sustituciones estan en
r3_ediciones_*.py (una por modulo), que definen `EDICIONES`.

Uso:  python3 diagnostico/cap2/comprobaciones/r3_edita.py r3_ediciones_m1.py [...]
"""
import importlib.util
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
HTML = RAIZ / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html"

src = HTML.read_text(encoding="utf-8")
total = 0
for nombre in sys.argv[1:]:
    spec = importlib.util.spec_from_file_location("ed", AQUI / nombre)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for i, (antes, despues) in enumerate(mod.EDICIONES, 1):
        n = src.count(antes)
        if n != 1:
            sys.exit(f"{nombre} #{i}: el texto de partida aparece {n} veces (debe ser 1):\n{antes[:200]}")
        src = src.replace(antes, despues)
        total += 1
    print(f"{nombre}: {len(mod.EDICIONES)} sustituciones")
HTML.write_text(src, encoding="utf-8")
print(f"escrito {HTML.name}: {total} sustituciones")
