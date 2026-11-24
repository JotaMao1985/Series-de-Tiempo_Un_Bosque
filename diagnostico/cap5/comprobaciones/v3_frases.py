"""V3: frases de la prosa (fuera de <pre>) que desaparecen, aparecen o se duplican entre HEAD y el arbol, por plantilla."""
import re, html, subprocess, collections
ARCH = ["ensamblado/cap5/templates_1_3.html", "ensamblado/cap5/templates_4_6.html",
        "ensamblado/cap5/templates_7_9.html", "ensamblado/cap5/templates_10_11.html"]
def frases(s):
    s = re.sub(r"<pre>.*?</pre>", " ", s, flags=re.S); s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
    return [f.strip() for f in re.split(r"(?<=[.:;!?])\s+(?=[A-ZÁÉÍÓÚÑ¿«$(])", t) if len(f.strip()) > 25]
def codigo(s): return [l.strip() for b in re.findall(r"<pre>(.*?)</pre>", s, re.S) for l in html.unescape(b).splitlines() if l.strip()]
for a in ARCH:
    viejo = subprocess.run(["git", "show", "HEAD:" + a], capture_output=True, text=True).stdout
    nuevo = open(a, encoding="utf-8").read()
    fv, fn = frases(viejo), frases(nuevo)
    sv, sn = set(fv), set(fn)
    print(f"\n######## {a}\n--- frases que desaparecen ({len(sv - sn)})")
    for f in fv:
        if f not in sn: print("  -", f[:400])
    print(f"--- frases nuevas ({len(sn - sv)})")
    for f in fn:
        if f not in sv: print("  +", f[:400])
    cn = collections.Counter(fn); cv = collections.Counter(fv)
    dup = [f for f in cn if cn[f] > 1 and cn[f] > cv.get(f, 0)]
    print("--- frases duplicadas nuevas:", dup or "ninguna")
    lv, ln = codigo(viejo), codigo(nuevo)
    cv2, cn2 = collections.Counter(lv), collections.Counter(ln)
    quit_ = [l for l in cv2 if cv2[l] > cn2.get(l, 0)]
    print(f"--- lineas de codigo que desaparecen ({len(quit_)}):"); [print("  -", l[:200]) for l in quit_]
