"""V3 · equilibrio de etiquetas en cada módulo (plantilla) y escapes dentro de <pre>: antes (HEAD) y después."""
import re, subprocess, sys, pathlib
from html.parser import HTMLParser
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v3_modulos import lee, modulos, RAIZ, HTML
VOID = {"br", "hr", "img", "input", "meta", "link", "col", "source", "wbr"}
class V(HTMLParser):
    def __init__(s): super().__init__(); s.pila = []; s.mal = []
    def handle_starttag(s, t, a):
        if t not in VOID: s.pila.append((t, s.getpos()[0]))
    def handle_endtag(s, t):
        if t in VOID: return
        if s.pila and s.pila[-1][0] == t: s.pila.pop()
        else:
            s.mal.append((t, s.getpos()[0], s.pila[-1] if s.pila else None))
            for i in range(len(s.pila) - 1, -1, -1):
                if s.pila[i][0] == t: del s.pila[i:]; break
def revisa(h):
    out = {}
    for k, v in sorted(modulos(h).items()):
        p = V(); p.feed(v); p.close()
        pre_crudos = len(re.findall(r"<pre><code[^>]*>[^<]*?(?:<(?![/]code)[^>]*>)", v))  # etiquetas dentro de <pre>
        amp = [m.group(0) for m in re.finditer(r"<pre><code[^>]*>(.*?)</code></pre>", v, re.S) for m in re.finditer(r"&(?!gt;|lt;|amp;|quot;|#\d+;)", m.group(1))]
        out[k] = (len(p.pila), len(p.mal), pre_crudos, len(amp))
    return out
head = subprocess.run(["git", "show", "HEAD:Htmls_Series/capitulo-4-modelos-arima.html"], cwd=RAIZ, capture_output=True, text=True).stdout
a, b = revisa(head), revisa(lee(HTML))
print("módulo | sin cerrar (antes→ahora) | cierres sobrantes | etiquetas dentro de <pre> | '&' sin escapar en <pre>")
for k in sorted(b): print(f"M{k:<2} | {a[k][0]}→{b[k][0]} | {a[k][1]}→{b[k][1]} | {a[k][2]}→{b[k][2]} | {a[k][3]}→{b[k][3]}")
