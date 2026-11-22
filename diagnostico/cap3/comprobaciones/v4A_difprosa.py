"""Verificador A · R4 cap. 3: diferencias de PROSA (sin marcas ni <cite>) en los
módulos 1-6 de ensamblado/cap3/cap3_modulos.html entre HEAD y el árbol."""
import re, subprocess, difflib, html, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[3]
F = "ensamblado/cap3/cap3_modulos.html"
antes = subprocess.run(["git", "show", f"HEAD:{F}"], cwd=RAIZ, capture_output=True, text=True).stdout
hoy = (RAIZ / F).read_text("utf-8")
def mods(t):
    partes = re.split(r'<template id="module-(\d+)">', t)
    return {int(partes[i]): partes[i+1] for i in range(1, len(partes), 2)}
def prosa(t):
    t = re.sub(r"<cite\b[^>]*>.*?</cite>", "", t, flags=re.S)
    t = re.sub(r"<script\b.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<(p|li|h\d|div|tr|td|th|summary|figcaption|br)\b[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    lineas = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
    return [l for l in lineas if l]
A, H = mods(antes), mods(hoy)
for m in range(1, 7):
    a, h = prosa(A[m]), prosa(H[m])
    d = [l for l in difflib.unified_diff(a, h, lineterm="", n=0) if not l.startswith(("---", "+++"))]
    print(f"######## MÓDULO {m}: {sum(1 for l in d if l.startswith('-'))} líneas quitadas, {sum(1 for l in d if l.startswith('+'))} añadidas")
    for l in d:
        print(l[:1200])
