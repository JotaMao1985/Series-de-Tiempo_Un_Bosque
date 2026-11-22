# Extrae los bloques <pre><code class="language-r|python"> de los modulos del cap. 4 (commit 71c42d8)
import re, html, subprocess, pathlib
raiz = pathlib.Path(__file__).resolve().parents[3]
src = subprocess.run(["git","show","71c42d8:Htmls_Series/capitulo-4-modelos-arima.html"],
                     cwd=raiz, capture_output=True, text=True).stdout
dest = pathlib.Path(__file__).parent / "par_bloques"
dest.mkdir(exist_ok=True)
pat = re.compile(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', re.S)
n = 0
for m in pat.finditer(src):
    linea = src[:m.start()].count("\n") + 1
    if linea > 6000: continue
    n += 1
    lang, cuerpo = m.group(1), html.unescape(re.sub(r'</?[a-zA-Z][^>]*>', '', m.group(2)))
    ext = "R" if lang == "r" else "py"
    (dest / f"b{n:02d}_l{linea}.{ext}").write_text(cuerpo)
    print(n, lang, linea)
