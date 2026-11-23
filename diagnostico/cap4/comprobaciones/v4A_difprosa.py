"""Verificador A · R4 cap. 4: diferencias de PROSA (sin marcas data-afirma ni
<cite>) en los módulos 1-6 de ensamblado/cap4/templates_*.html entre 21b311b
(cierre de la R3) y el árbol de trabajo."""
import re, subprocess, difflib, html, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[3]
BASE = "21b311b"
FS = ["ensamblado/cap4/templates_1_3.html", "ensamblado/cap4/templates_4_6.html"]
def mods(t):
    partes = re.split(r'<template id="module-(\d+)"[^>]*>', t)
    return {int(partes[i]): partes[i+1] for i in range(1, len(partes), 2)}
def prosa(t):
    t = re.sub(r"<cite\b[^>]*>.*?</cite>", "", t, flags=re.S)
    t = re.sub(r"<script\b.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<(p|li|h\d|div|tr|td|th|summary|figcaption|br|pre)\b[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    lineas = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
    return [l for l in lineas if l]
A, H = {}, {}
for F in FS:
    A.update(mods(subprocess.run(["git", "show", f"{BASE}:{F}"], cwd=RAIZ, capture_output=True, text=True).stdout))
    H.update(mods((RAIZ / F).read_text("utf-8")))
for m in range(1, 7):
    a, h = prosa(A[m]), prosa(H[m])
    d = [l for l in difflib.unified_diff(a, h, lineterm="", n=0) if not l.startswith(("---", "+++"))]
    print(f"######## MÓDULO {m}: {sum(1 for l in d if l.startswith('-'))} líneas quitadas, {sum(1 for l in d if l.startswith('+'))} añadidas")
    for l in d:
        print(l[:1500])

# Segunda vista: diferencia por PALABRAS (insensible al cambio de cortes de
# línea que introducen las marcas), con 12 palabras de contexto.
print("\n\n================ DIFERENCIA POR PALABRAS ================")
for m in range(1, 7):
    j = lambda t: re.sub(r"\s+([.,:;)])", r"\1", " ".join(prosa(t))).split()
    a = j(A[m]); h = j(H[m])
    sm = difflib.SequenceMatcher(None, a, h, autojunk=False)
    print(f"######## MÓDULO {m}")
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        ctx_a = " ".join(a[max(0, i1-12):i1])
        print(f"  [{op}] …{ctx_a} ⟦−{' '.join(a[i1:i2])}⟧ ⟦+{' '.join(h[j1:j2])}⟧ {' '.join(a[i2:i2+8])}…")
