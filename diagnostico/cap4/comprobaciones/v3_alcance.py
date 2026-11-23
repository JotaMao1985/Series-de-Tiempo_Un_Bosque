#!/usr/bin/env python3
"""V3 · alcance: qué cambia y qué no entre HEAD y el árbol de trabajo en el capítulo 4 ensamblado."""
import re, subprocess, sys, pathlib, difflib, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v3_modulos import lee, modulos, texto, RAIZ, HTML

head = subprocess.run(["git", "show", "HEAD:Htmls_Series/capitulo-4-modelos-arima.html"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
now = lee(HTML)

def md5(s): return hashlib.md5(s.encode()).hexdigest()[:10]

print("== 1. Archivos modificados respecto de HEAD (git status, sin diagnostico/):")
st = subprocess.run(["git", "status", "--short"], cwd=RAIZ, capture_output=True, text=True).stdout
print("\n".join(l for l in st.splitlines() if "diagnostico/" not in l))
print("   Archivos de otros capítulos / preparcial / diapositivas / bibliografía tocados:",
      [l for l in st.splitlines() if re.search(r"capitulo-[1235-6]|preparcial|diapositivas|bibliografia|chapter\.js|plantilla|precalculo", l)] or "ninguno")

print("\n== 2. Ids, títulos y estructura")
ids_a, ids_b = re.findall(r'\bid="([^"]+)"', head), re.findall(r'\bid="([^"]+)"', now)
print("   ids HTML: antes", len(ids_a), "después", len(ids_b), "| añadidos:", sorted(set(ids_b) - set(ids_a)), "| quitados:", sorted(set(ids_a) - set(ids_b)))
sim_a, sim_b = re.findall(r'data-simulador="([^"]+)"', head), re.findall(r'data-simulador="([^"]+)"', now)
print("   data-simulador igual:", sim_a == sim_b, len(sim_a))
h2a = [re.sub(r"\s+", " ", texto(re.search(r"<h2.*?</h2>", v, re.S).group(0))) for k, v in sorted(modulos(head).items())]
h2b = [re.sub(r"\s+", " ", texto(re.search(r"<h2.*?</h2>", v, re.S).group(0))) for k, v in sorted(modulos(now).items())]
print("   títulos <h2> de módulo iguales:", h2a == h2b)
t_a = re.findall(r'\{ id: (\d+), title: "([^"]*)", shortTitle: "([^"]*)"', head)
t_b = re.findall(r'\{ id: (\d+), title: "([^"]*)", shortTitle: "([^"]*)"', now)
print("   courseData ids/títulos/shortTitle iguales:", t_a == t_b, len(t_b))
for k in sorted(modulos(head)):
    a = re.findall(r"<h3>(.*?)</h3>", modulos(head)[k], re.S); b = re.findall(r"<h3>(.*?)</h3>", modulos(now)[k], re.S)
    if a != b: print(f"   <h3> de M{k} cambian:\n      antes : {[re.sub(chr(10),' ',x)[:60] for x in a]}\n      ahora : {[re.sub(chr(10),' ',x)[:60] for x in b]}")

print("\n== 3. Bloques JS que no deben cambiar")
def bloque(h, ini, fin="\n    ];"):
    i = h.find(ini); j = h.find(fin, i); return h[i:j] if i >= 0 else None
for nombre, ini, fin in [("SIMULACROS['cap4-simulacro']", "SIMULACROS['cap4-simulacro']", "\n    };"),
                         ("AUTOEVALUACIONES['cap4']", "AUTOEVALUACIONES['cap4']", "\n    ];"),
                         ("SIMULADORES (JS)", "const SIMULADORES", None), ("DATOS_CAP4", "const DATOS_CAP4", "};\n")]:
    if fin is None:
        a, b = head[head.find(ini):], now[now.find(ini):]
        # hasta el final del documento
    else:
        a, b = bloque(head, ini, fin), bloque(now, ini, fin)
    print(f"   {nombre}: {'idéntico' if a == b else 'CAMBIA'} (md5 {md5(a or '')} / {md5(b or '')}, {len(a or '')} y {len(b or '')} caracteres)")

print("\n== 4. Ejercicios 1-3 (enunciado, pista, solución), M10, y quiz")
ea = re.findall(r'<div class="ejercicio-guiado">.*?(?=<h3>Lecturas</h3>)', modulos(head)[10], re.S)
eb = re.findall(r'<div class="ejercicio-guiado">.*?(?=<h3>Lecturas</h3>)', modulos(now)[10], re.S)
print("   bloque de ejercicios 1-3 idéntico:", ea == eb)
for k in (11, 12):
    print(f"   Módulo {k} idéntico:", modulos(head)[k] == modulos(now)[k])
ma, mb = modulos(head)[10], modulos(now)[10]
qa = re.search(r'<h3>Autoevaluación</h3>.*?(?=<h3>Ejercicios propuestos</h3>)', ma, re.S).group(0)
qb = re.search(r'<h3>Autoevaluación</h3>.*?(?=<h3>Ejercicios propuestos</h3>)', mb, re.S).group(0)
print("   sección Autoevaluación (contenedor) idéntica:", qa == qb)
la = re.search(r'<h3>Lecturas</h3>.*', ma, re.S).group(0); lb = re.search(r'<h3>Lecturas</h3>.*', mb, re.S).group(0)
print("   Lecturas + nota 'Y en el Capítulo 5…' idénticas:", la == lb)

print("\n== 5. Atribuciones nuevas (cite, data-afirma, autor-año) en las líneas añadidas")
d = subprocess.run(["git", "diff", "HEAD", "-U0", "--", "Htmls_Series/capitulo-4-modelos-arima.html"], cwd=RAIZ, capture_output=True, text=True).stdout
add = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
rem = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
txt_add = "\n".join(add); txt_rem = "\n".join(rem)
for pat, nom in [(r"<cite", "<cite"), (r"data-afirma", "data-afirma"), (r"\b[A-Z][a-zé]+(?: y [A-Z][a-zé]+)?,? \(?(?:19|20)\d\d\)?", "Autor (año)"), (r"doi\.org|\bDOI\b", "DOI"), (r"§\s*\d", "§"), (r"\bp\. \d+", "p. N")]:
    print(f"   {nom:12s}: añadidas {len(re.findall(pat, txt_add)):2d} | quitadas {len(re.findall(pat, txt_rem)):2d} | {sorted(set(re.findall(pat, txt_add)))[:5]}")
print("   (líneas añadidas / quitadas en total:", len(add), "/", len(rem), ")")

print("\n== 6. Frases de prosa que desaparecen del todo / se duplican")
def frases(h, solo_prosa=True):
    out = []
    for k, v in sorted(modulos(h).items()):
        t = texto(v, con_pre=False)
        t = re.sub(r"\s+", " ", t)
        for f in re.split(r"(?<=[.!?:;])\s+(?=[A-ZÁÉÍÓÚ¿¡$«\"])", t):
            f = f.strip()
            if len(f.split()) >= 5: out.append((k, f))
    return out
fa, fb = frases(head), frases(now)
sa, sb = {f for _, f in fa}, {f for _, f in fb}
quitadas = [(k, f) for k, f in fa if f not in sb]
nuevas = [(k, f) for k, f in fb if f not in sa]
print(f"   frases antes {len(fa)}, ahora {len(fb)}; quitadas literalmente: {len(quitadas)}; nuevas literalmente: {len(nuevas)}")
pool = [f for _, f in nuevas]
huerfanas = []
for k, f in quitadas:
    best = max((difflib.SequenceMatcher(None, f, g).ratio() for g in pool), default=0)
    huerfanas.append((best, k, f))
huerfanas.sort()
print("   Quitadas cuyo mejor parecido con una frase nueva es < 0.45 (contenido que quizá se perdió):")
for best, k, f in huerfanas:
    if best < 0.45:
        print(f"     [M{k}] ({best:.2f}) {f[:230]}")
from collections import Counter
dup = [(f, n) for f, n in Counter(f for _, f in fb).items() if n > 1 and len(f.split()) >= 8]
print("   Frases (≥8 palabras) repetidas literalmente en el capítulo ahora:", len(dup))
for f, n in dup[:12]: print(f"     x{n}: {f[:160]}")
dup_a = {f for f, n in Counter(f for _, f in fa).items() if n > 1}
print("   de ellas, ya repetidas antes:", sum(1 for f, _ in dup if f in dup_a))
