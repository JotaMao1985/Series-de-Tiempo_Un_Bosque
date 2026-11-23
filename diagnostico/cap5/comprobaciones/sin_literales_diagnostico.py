#!/usr/bin/env python3
"""Ningún pasaje de la caché de fuentes (fuera de git) copiado en lo que el diagnóstico del cap. 5 versiona.

Busca secuencias de 10 palabras normalizadas de `bibliografia/_local/texto/` y `bibliografia/_local/web/`
en los archivos de texto de `diagnostico/cap5/` (salvo capturas), en el inventario y en el plan.
Uso:  python3 diagnostico/cap5/comprobaciones/sin_literales_diagnostico.py
"""
import pathlib, re, sys, unicodedata
RAIZ = pathlib.Path(__file__).resolve().parents[3]
N = 10
def palabras(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", t)
cache = set()
for base in ("bibliografia/_local/texto", "bibliografia/_local/web"):
    for f in (RAIZ / base).rglob("*.txt"):
        w = palabras(f.read_text("utf-8", errors="ignore"))
        for i in range(len(w) - N + 1):
            cache.add(hash(tuple(w[i:i + N])))
objetivos = [p for p in (RAIZ / "diagnostico/cap5").rglob("*") if p.is_file() and "capturas" not in p.parts
             and p.suffix in {".md", ".tsv", ".R", ".py", ".js", ".out", ".json", ".txt"}]
objetivos += [RAIZ / "bibliografia/contraste/cap5_inventario.tsv", RAIZ / "PLAN_Mejora_Cap5.md"]
fallos = 0
for p in objetivos:
    w = palabras(p.read_text("utf-8", errors="ignore"))
    # solo ventanas de prosa: al menos 7 palabras de 4 letras o más (el código y las cifras no cuentan)
    hits = [i for i in range(len(w) - N + 1) if hash(tuple(w[i:i + N])) in cache
            and sum(1 for x in w[i:i + N] if x.isalpha() and len(x) >= 4) >= 7]
    if hits:
        fallos += 1
        i = hits[0]
        print(f"COINCIDE  {p.relative_to(RAIZ)}  ({len(hits)} ventanas)  «{' '.join(w[i:i + N + 4])}»")
print(f"{len(objetivos)} archivos, {len(cache)} ventanas de la caché; {fallos} con coincidencias")
sys.exit(1 if fallos else 0)
