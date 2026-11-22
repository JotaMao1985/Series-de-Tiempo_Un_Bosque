# Compara SIMULACROS['cap4-simulacro'] y la estructura de AUTOEVALUACIONES['cap4'] entre 7e9bc58 y el árbol
# python3 diagnostico/cap4/comprobaciones/v1_quiz_simulacro.py
import re, subprocess, hashlib
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
ruta = "Htmls_Series/capitulo-4-modelos-arima.html"
viejo = subprocess.run(["git", "show", f"7e9bc58:{ruta}"], cwd=RAIZ, capture_output=True, text=True).stdout
nuevo = (RAIZ / ruta).read_text(encoding="utf-8")
def bloque(t, ini, fin_pat):
    i = t.index(ini); j = t.index(fin_pat, i); return t[i:j]
for nombre, t in (("7e9bc58", viejo), ("árbol", nuevo)):
    sim = bloque(t, "SIMULACROS['cap4-simulacro']", "// [fin")  if "SIMULACROS['cap4-simulacro']" in t else ""
    print(nombre, "simulacro md5", hashlib.md5(sim.encode()).hexdigest(), len(sim))
def items(t):
    i = t.index("AUTOEVALUACIONES['cap4']"); j = t.index("];", i)
    q = t[i:j]
    return [(m.start(), m.group(0)) for m in re.finditer(r"correcta:\s*(true|false)", q)], q
(cv, qv), (cn, qn) = items(viejo), items(nuevo)
print("flags 7e9bc58:", [c.split(":")[1].strip() for _, c in cv])
print("flags árbol  :", [c.split(":")[1].strip() for _, c in cn])
print("iguales:", [c for _, c in cv] == [c for _, c in cn])
# clave de numéricas
print("respuesta/tolerancia 7e9bc58:", re.findall(r"(?:respuesta|tolerancia|clave):\s*[^,\n]+", qv))
print("respuesta/tolerancia árbol  :", re.findall(r"(?:respuesta|tolerancia|clave):\s*[^,\n]+", qn))
# longitudes de las opciones del ítem 4 (más larga = correcta?)
def opciones_item(q, n):
    partes = re.split(r"\n\s*\{\s*\n\s*tipo:", q)
    return partes[n] if n < len(partes) else ""
for idx in range(1, 9):
    p = opciones_item(qn, idx)
    ops = re.findall(r"\{ texto: '((?:[^'\\]|\\.)*)', correcta: (true|false)", p)
    if not ops:
        ops = re.findall(r"texto: '((?:[^'\\]|\\.)*)',\s*correcta: (true|false)", p)
    if ops:
        L = [(len(o), c) for o, c in ops]
        mx = max(L)[0]
        print(f"ítem {idx}: longitudes {L} · la más larga es correcta: {[c for l, c in L if l == mx]}")
