"""Verificador independiente R2 cap. 5: regresiones estáticas entre HEAD y el árbol.
- bloques <pre> (código R/Python y salidas) del cap. 5, idénticos y en el mismo orden;
- orden y títulos de los módulos (<template id="module-N"> y su <h2>);
- el registro del quiz AUTOEVALUACIONES['cap5'] en la fuente: qué líneas cambian;
- ensamblado/cap5/simulacro.js sin cambios."""
import re, subprocess, difflib
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
def head(p): return subprocess.run(["git", "show", "HEAD:" + p], cwd=RAIZ, capture_output=True, text=True).stdout
def ahora(p): return (RAIZ / p).read_text(encoding="utf-8")
H = "Htmls_Series/capitulo-5-sarima.html"
for nombre, f in [("HEAD", head), ("árbol", ahora)]:
    pass
pre = lambda t: re.findall(r"<pre[^>]*>.*?</pre>", t, re.S)
a, b = pre(head(H)), pre(ahora(H))
print(f"<pre> en HEAD: {len(a)} · en el árbol: {len(b)} · idénticos y en orden: {a == b}")
mods = lambda t: re.findall(r'<template id="module-(\d+)">\s*.*?<h2[^>]*>(.*?)</h2>', t, re.S)
ma, mb = mods(head(H)), mods(ahora(H))
print(f"módulos HEAD: {len(ma)} · árbol: {len(mb)} · mismo orden y títulos: {ma == mb}")
for (n, t) in mb: print("   ", n, re.sub(r"<[^>]+>|\s+", " ", t).strip()[:80])
# Quiz en la fuente
J = "ensamblado/cap5/chapter.js"
def quiz(t):
    i = t.index("AUTOEVALUACIONES['cap5'] = [")
    j = t.index("\n    ];", i)
    return t[i:j].splitlines()
qa, qb = quiz(head(J)), quiz(ahora(J))
d = [l for l in difflib.unified_diff(qa, qb, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
print(f"\nquiz cap5 en la fuente: {len(qa)} → {len(qb)} líneas; líneas cambiadas:")
for l in d: print("   ", l[:150])
# Funciones auxiliares del quiz fuera del bloque
print("\nsimulacro.js idéntico a HEAD:", head("ensamblado/cap5/simulacro.js") == ahora("ensamblado/cap5/simulacro.js"))
# Bloques de código en las plantillas fuente
for p in sorted((RAIZ / "ensamblado/cap5").glob("templates_*.html")):
    r = str(p.relative_to(RAIZ))
    print(f"{r}: <pre> idénticos: {pre(head(r)) == pre(ahora(r))}")
