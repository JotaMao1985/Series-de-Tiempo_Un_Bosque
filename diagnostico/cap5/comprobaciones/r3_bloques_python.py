"""R3 del capítulo 5 (copia de r1_bloques_python.py, sin cambios de lógica) · ejecuta los bloques de Python del capítulo ensamblado y cruza
sus comentarios con la salida real.

Cada bloque corre solo, en una carpeta temporal vacía (en este capítulo ninguno necesita
archivos de otro bloque). El bloque de la
TRM (Módulo 8) corre dos veces: sin el CSV de la TRM en la carpeta (lo lee de la página del
curso) y con él. Uso, desde la raíz del repo:
  MPLBACKEND=Agg python3 diagnostico/cap5/comprobaciones/r3_bloques_python.py \
      > diagnostico/cap5/comprobaciones/r3_bloques_python.out 2>&1
"""
import html, os, pathlib, re, shutil, subprocess, sys, tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[3]
CAP = RAIZ / "Htmls_Series" / "capitulo-5-sarima.html"
CSV = RAIZ / "Htmls_Series" / "datos" / "trm_mensual_2015-01_2026-06.csv"
src = CAP.read_text(encoding="utf-8")
pat = re.compile(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', re.S)
num = re.compile(r'-?\d+\.\d+')
bloques = []
for m in pat.finditer(src):
    linea = src[:m.start()].count("\n") + 1
    modulo = max((int(x) for x in re.findall(r'<template id="module-(\d+)">', src[:m.start()])), default=0)
    cuerpo = html.unescape(re.sub(r'</?[a-zA-Z][^>]*>', '', m.group(2)))
    bloques.append((m.group(1), linea, modulo, cuerpo))
print(f"{sum(b[0] == 'r' for b in bloques)} bloques de R y {sum(b[0] == 'python' for b in bloques)} de Python en {CAP.name}\n")

# Sin PYTHONWARNINGS: los avisos de convergencia de statsmodels tienen que verse.
env = dict(os.environ, MPLBACKEND="Agg")
total_faltan = 0


def corre(cuerpo, carpeta):
    (carpeta / "b.py").write_text(cuerpo, encoding="utf-8")
    p = subprocess.run([sys.executable, "b.py"], cwd=carpeta, capture_output=True, text=True, env=env, timeout=900)
    return p.returncode, p.stdout, p.stderr


for i, (lang, linea, modulo, cuerpo) in enumerate(bloques):
    if lang != "python":
        continue
    variantes = [("", False)]
    if "trm_mensual" in cuerpo:
        variantes = [(" · TRM desde la página del curso", False), (" · TRM desde la carpeta de trabajo", True)]
    for rotulo, con_csv in variantes:
        with tempfile.TemporaryDirectory() as t:
            t = pathlib.Path(t)
            if 'read_csv("serie.csv")' in cuerpo:           # lo escribe el bloque de R que lo precede
                r = bloques[i - 1][3]
                subprocess.run(["Rscript", "-e", r], cwd=t, capture_output=True, text=True)
            if con_csv:
                shutil.copy(CSV, t / CSV.name)
            rc, out, err = corre(cuerpo, t)
        print(f"===== Módulo {modulo} · línea {linea}{rotulo} · código de salida {rc} =====")
        print(out.rstrip())
        if rc != 0:
            print("STDERR:", err[-1500:])
            total_faltan += 1
        avisos = sorted(set(re.findall(r"(\w+Warning): ([^\n]{0,90})", err)))
        print(f"--- avisos en stderr: {avisos if avisos else 'ninguno'}")
        # Cada línea #> tiene que aparecer tal cual (salvo espacios finales) en la salida
        salida = [s.rstrip() for s in out.splitlines()]
        no_literal = [l for l in cuerpo.splitlines() if l.startswith("#> ")
                      and not any(s.startswith(l[3:].rstrip().split("   ")[0].rstrip()) for s in salida)]
        print(f"--- líneas #> sin su par literal en la salida: {len(no_literal)}")
        for l in no_literal: print("      ", l)
        reales = set(num.findall(out))
        faltan = []
        for l in cuerpo.splitlines():
            if "#" not in l:
                continue
            com = l.split("#", 1)[1]
            for tok in num.findall(com):
                if tok not in reales and tok.lstrip("-") not in reales and ("-" + tok) not in reales:
                    faltan.append((tok, l.strip()[:100]))
        print(f"--- cifras con decimales de los comentarios que NO están en la salida: {len(faltan)}")
        for tok, l in faltan:
            print(f"      {tok:>10}  <- {l}")
        print()
