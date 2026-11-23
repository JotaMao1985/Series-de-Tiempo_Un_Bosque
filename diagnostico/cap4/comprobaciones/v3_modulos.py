#!/usr/bin/env python3
"""V3 · utilidades: parte el capítulo 4 en sus módulos (plantillas) y pasa cada uno a texto plano.
Uso: v3_modulos.py [--html RUTA] [--out CARPETA]  -> escribe CARPETA/mN.txt (prosa, con [PRE:lang]...[/PRE] para el código)
Como módulo: from v3_modulos import modulos, texto, primera_aparicion"""
import re, sys, html as H, pathlib, json

RAIZ = pathlib.Path(__file__).resolve().parents[3]
HTML = RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"


def lee(ruta=HTML):
    return pathlib.Path(ruta).read_text(encoding="utf-8")


def modulos(h):
    return {int(m.group(1)): m.group(2)
            for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', h, re.S)}


def texto(frag, con_pre=True):
    t = frag
    if con_pre:
        t = re.sub(r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
                   lambda m: f"\n[PRE:{m.group(1)}]\n{m.group(2)}\n[/PRE]\n", t, flags=re.S)
    else:
        t = re.sub(r'<pre>.*?</pre>', ' ', t, flags=re.S)
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', t, flags=re.S)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'</(p|div|li|tr|h\d|table|ul|ol)>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = H.unescape(t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n\n', t)
    return t.strip()


def primera_aparicion(h, patron, flags=re.I):
    """(módulo, línea dentro de la plantilla) de la primera aparición en la PROSA (sin <pre>) de cada módulo."""
    out = []
    for k, v in sorted(modulos(h).items()):
        for m in re.finditer(patron, v, flags):
            # ¿dentro de un <pre>?
            ini = v.rfind('<pre>', 0, m.start()); fin = v.rfind('</pre>', 0, m.start())
            en_pre = ini > fin
            out.append((k, v.count('\n', 0, m.start()), 'pre' if en_pre else 'prosa', H.unescape(re.sub(r'<[^>]+>', '', v[max(0, m.start()-50):m.end()+50])).replace('\n', ' ')))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    ruta = HTML
    if "--html" in args:
        ruta = args[args.index("--html") + 1]
    out = pathlib.Path(args[args.index("--out") + 1]) if "--out" in args else None
    h = lee(ruta)
    ms = modulos(h)
    for k, v in ms.items():
        t = texto(v)
        if out:
            out.mkdir(parents=True, exist_ok=True)
            (out / f"m{k}.txt").write_text(t, encoding="utf-8")
        else:
            print(f"M{k}: {len(t.split())} palabras")
