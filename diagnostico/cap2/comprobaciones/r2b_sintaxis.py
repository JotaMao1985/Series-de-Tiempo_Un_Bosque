#!/usr/bin/env python3
"""R2b · el <script> de cada capítulo (2–6) pasa `node --check` y no declara dos veces
una función ni una constante de primer nivel (una función repetida no da error: la
segunda pisa a la primera en silencio, que es como un ayudante heredado puede romper
el de un capítulo)."""
import re, subprocess, sys, tempfile, collections
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
mal = 0
for f in sorted((RAIZ / "Htmls_Series").glob("capitulo-[2-6]-*.html")):
    js = max(re.findall(r"<script>(.*?)</script>", f.read_text(encoding="utf-8"), re.S), key=len)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tmp:
        tmp.write(js)
    r = subprocess.run(["node", "--check", tmp.name], capture_output=True, text=True)
    nombres = re.findall(r"^    (?:function|const|let) ([A-Za-z_$][\w$]*)", js, re.M)
    rep = [n for n, k in collections.Counter(nombres).items() if k > 1]
    ok = r.returncode == 0 and not rep
    mal += not ok
    print(f"{'OK ' if ok else 'MAL'} {f.name}: node --check {'limpio' if r.returncode == 0 else r.stderr.strip().splitlines()[4] if len(r.stderr.splitlines()) > 4 else r.stderr[:200]}"
          f" · {len(nombres)} declaraciones de primer nivel, repetidas: {rep or 'ninguna'}")
sys.exit(1 if mal else 0)
