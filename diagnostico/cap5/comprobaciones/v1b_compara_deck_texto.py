"""Verificador B: diferencia de texto visible (sin etiquetas) diapositiva a diapositiva del deck del cap. 5."""
import difflib, re, subprocess
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
RUTA = "Htmls_Series/diapositivas/capitulo-5-sarima.html"
v = subprocess.run(["git", "show", f"7686d33:{RUTA}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
n = (RAIZ / RUTA).read_text(encoding="utf-8")
sec = lambda h: re.findall(r"(<section\b.*?</section>)", h, flags=re.S)
def txt(s):
    s = re.sub(r"<aside class=\"notas\".*?</aside>", " [NOTAS] ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()
def clases(s):
    return re.findall(r'class="([^"]+)"', s)
for i, (a, b) in enumerate(zip(sec(v), sec(n)), 1):
    if a == b: continue
    ta, tb = txt(a), txt(b)
    sm = difflib.SequenceMatcher(None, ta.split(), tb.split())
    cambios = [(op, " ".join(ta.split()[i1:i2])[:160], " ".join(tb.split()[j1:j2])[:160]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    ca, cb = clases(a), clases(b)
    dc = [l for l in difflib.ndiff(ca, cb) if l[:1] in "+-"]
    print(f"--- {i}: {len(cambios)} cambios de texto; clases: {' '.join(dc)[:200]}")
    for op, x, y in cambios[:4]:
        print(f"     {op}: «{x}» -> «{y}»")
