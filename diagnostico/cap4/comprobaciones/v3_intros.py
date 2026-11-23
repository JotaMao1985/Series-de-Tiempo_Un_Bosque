#!/usr/bin/env python3
"""V3 · introducciones de simulador (p.simulador-intro) antes y después: palabras y texto."""
import re, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v3_modulos import lee, modulos, texto, RAIZ, HTML
head = subprocess.run(["git", "show", "HEAD:Htmls_Series/capitulo-4-modelos-arima.html"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
def intros(h):
    out = {}
    for k, v in sorted(modulos(h).items()):
        for m in re.finditer(r'<div class="simulador" data-simulador="([^"]+)">.*?<p class="simulador-intro">(.*?)</p>', v, re.S):
            t = re.sub(r"\s+", " ", texto(m.group(2), con_pre=False))
            out[(k, m.group(1))] = t
    return out
a, b = intros(head), intros(lee(HTML))
for key in b:
    ta, tb = a.get(key, ""), b[key]
    nums = re.findall(r"-?\d+(?:\.\d+)?", re.sub(r"\$[^$]*\$", lambda m: m.group(0), tb))
    print(f"M{key[0]} · {key[1]} · palabras {len(ta.split())} -> {len(tb.split())} · {'CAMBIA' if ta != tb else 'igual'}")
    print("   AHORA:", tb[:1200])
    print()
