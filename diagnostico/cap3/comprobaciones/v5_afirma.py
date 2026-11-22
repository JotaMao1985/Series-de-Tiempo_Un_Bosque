"""Verificador R5 cap. 3: (1) lineas del diff con data-afirma o <cite>; (2) contenido de cada
elemento con data-afirma en HEAD frente al arbol de trabajo (el texto que firma la R4)."""
import re, subprocess
from html.parser import HTMLParser
F = "ensamblado/cap3/cap3_modulos.html"
diff = subprocess.run(["git", "diff", "-U0", "--", F], capture_output=True, text=True).stdout
toc = [l for l in diff.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---")) and ("data-afirma" in l or "<cite" in l)]
print("Lineas del diff con data-afirma o <cite>:", len(toc))
for l in toc: print("  ", l[:1], (re.findall(r'data-afirma="([^"]+)"', l) or ["(solo cite)"]), re.sub(r"<cite.*?</cite>", "<cite/>", l[1:].strip())[:160])

class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.st = []; s.out = {}
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ("br", "img", "input", "hr", "meta", "link", "source"): return
        s.st.append([t, a.get("data-afirma"), []])
    def handle_endtag(s, t):
        while s.st:
            tag, idf, buf = s.st.pop()
            txt = "".join(buf)
            if idf: s.out.setdefault(idf, []).append(" ".join(txt.split()))
            if s.st: s.st[-1][2].append(txt)
            if tag == t: break
    def handle_data(s, d):
        if s.st: s.st[-1][2].append(d)
def afirma(src):
    p = P(); p.feed(src); return p.out
old = afirma(subprocess.run(["git", "show", "HEAD:" + F], capture_output=True, text=True).stdout)
new = afirma(open(F, encoding="utf-8").read())
print("ids HEAD:", len(old), " ids ahora:", len(new), " desaparecen:", sorted(set(old) - set(new)), " nuevos:", sorted(set(new) - set(old)))
cambios = [k for k in old if k in new and old[k] != new[k]]
print("ids con el texto cambiado:", cambios)
for k in cambios: print(" ", k, "\n   antes:", old[k], "\n   ahora:", new[k])
