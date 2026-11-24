"""Verificador A, R1 cap. 5: busca 7-gramas de las líneas añadidas del diff (contra 7686d33)
en el texto extraído de los libros y de la web (bibliografia/_local/texto y web).
Solo informa del número de coincidencias y del archivo; no imprime el texto del libro.
python3 diagnostico/cap5/comprobaciones/v1a_literales.py
"""
import html, os, re, subprocess, unicodedata

RUTAS = ["ensamblado/cap5", "ensamblado/ensambla_cap5.py", "precalculo/genera_cap5.R",
         "Htmls_Series/diapositivas/fuentes/capitulo_5.md"]
diff = subprocess.run(["git", "diff", "7686d33", "--"] + RUTAS, capture_output=True, text=True).stdout
añadidas = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]


def palabras(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", t)


N = 7
grams = {}
for l in añadidas:
    p = palabras(l)
    for i in range(len(p) - N + 1):
        grams.setdefault(" ".join(p[i:i + N]), l.strip()[:80])
print("líneas añadidas:", len(añadidas), " 7-gramas distintos:", len(grams))

total = 0
for base in ("bibliografia/_local/texto", "bibliografia/_local/web"):
    for raiz, _, archivos in os.walk(base):
        for a in archivos:
            ruta = os.path.join(raiz, a)
            try:
                p = palabras(open(ruta, encoding="utf-8", errors="ignore").read())
            except Exception:
                continue
            vent = set(" ".join(p[i:i + N]) for i in range(len(p) - N + 1))
            hits = [g for g in grams if g in vent]
            if hits:
                total += len(hits)
                print(f"{ruta}: {len(hits)} coincidencias")
                for g in hits[:10]:
                    print("   línea del diff:", grams[g])
print("coincidencias totales:", total)
