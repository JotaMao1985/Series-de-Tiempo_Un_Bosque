# Extrae los bloques <pre><code class="language-r|python"> de los modulos del cap. 3 (commit 58bdfc5)
import re, html, subprocess, pathlib, sys
raiz = pathlib.Path(__file__).resolve().parents[3]
src = subprocess.run(["git","show","58bdfc5:Htmls_Series/capitulo-3-modelos-ar-ma-arma.html"],
                     cwd=raiz, capture_output=True, text=True).stdout
lineas = src.split("\n")
dest = pathlib.Path(__file__).parent / "par_bloques"
dest.mkdir(exist_ok=True)
pat = re.compile(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', re.S)
n = 0
for m in pat.finditer(src):
    linea = src[:m.start()].count("\n") + 1
    if linea > 7420: continue
    n += 1
    lang, cuerpo = m.group(1), html.unescape(re.sub(r'</?[a-zA-Z][^>]*>', '', m.group(2)))
    ext = "R" if lang == "r" else "py"
    (dest / f"b{n:02d}_l{linea}.{ext}").write_text(cuerpo)
    print(n, lang, linea)
