# Busca 7-gramas de las líneas añadidas por la R1 (fuentes y diapositivas) en bibliografia/_local/texto y web.
# python3 diagnostico/cap4/comprobaciones/v1_literales.py
import re, subprocess, unicodedata, html
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
rutas = ["ensamblado/cap4", "precalculo/genera_cap4.R", "Htmls_Series/diapositivas/fuentes/capitulo_4.md",
         "Htmls_Series/diapositivas/fuentes/verificacion/verifica_cifras_cap4.py"]
diff = subprocess.run(["git", "diff", "-U0", "7e9bc58", "--"] + rutas, cwd=RAIZ, capture_output=True, text=True).stdout
añadidas = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
def norm(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", t)
pal = []
for l in añadidas:
    pal += norm(l)
g7 = {" ".join(pal[i:i+7]) for i in range(len(pal) - 6)}
print("líneas añadidas:", len(añadidas), "· palabras:", len(pal), "· 7-gramas:", len(g7))
corpus = {}
for base in ("bibliografia/_local/texto", "bibliografia/_local/web"):
    for f in (RAIZ / base).rglob("*"):
        if f.is_file() and f.suffix in (".txt", ".md", ".html", ".htm", ""):
            try:
                corpus[str(f.relative_to(RAIZ))] = " ".join(norm(f.read_text(encoding="utf-8", errors="ignore")))
            except Exception:
                pass
print("archivos del corpus:", len(corpus))
hits = []
for g in g7:
    for nombre, txt in corpus.items():
        if " " + g + " " in " " + txt + " ":
            hits.append((g, nombre))
print("coincidencias de 7-gramas:", len(hits))
for g, n in sorted(hits)[:50]:
    print(f"  «{g}» en {n}")
