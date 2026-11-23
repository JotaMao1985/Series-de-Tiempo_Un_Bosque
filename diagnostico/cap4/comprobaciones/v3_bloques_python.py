"""V3 · ejecuta cada bloque de Python del capítulo 4 ensamblado en una carpeta vacía y cruza las líneas `#>`
(salida esperada, escrita en la página) con la salida real, número a número. Independiente de r3_bloques_python.py.
Uso:  MPLBACKEND=Agg python3 diagnostico/cap4/comprobaciones/v3_bloques_python.py > .../v3_bloques_python.out 2>&1"""
import html, os, pathlib, re, shutil, subprocess, sys, tempfile
RAIZ = pathlib.Path(__file__).resolve().parents[3]
CAP = RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
CSV = RAIZ / "Htmls_Series" / "datos" / "trm_mensual_2015-01_2026-06.csv"
src = CAP.read_text(encoding="utf-8")
pat = re.compile(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', re.S)
num = re.compile(r'-?\d+(?:\.\d+)?(?:e-?\d+)?')
bloques = []
for m in pat.finditer(src):
    modulo = max(int(x) for x in re.findall(r'<template id="module-(\d+)">', src[:m.start()]))
    bloques.append((m.group(1), modulo, html.unescape(m.group(2))))
env = dict(os.environ, MPLBACKEND="Agg", PYTHONWARNINGS="ignore")
malos = 0
for i, (lang, modulo, cuerpo) in enumerate(bloques):
    if lang != "python":
        continue
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t); shutil.copy(CSV, t / CSV.name)
        (t / "b.py").write_text(cuerpo, encoding="utf-8")
        p = subprocess.run([sys.executable, "b.py"], cwd=t, capture_output=True, text=True, env=env, timeout=1200)
    esperado = []
    for l in cuerpo.splitlines():
        if l.startswith("#>"):
            esperado.append(l[2:].strip())
    real = p.stdout
    # números esperados que no aparecen en la salida real (comparación por texto de cada token)
    toks_real = set(num.findall(real))
    falta = []
    for l in esperado:
        izq = re.split(r"\s{3,}[a-zA-Z<(]", l)[0]       # corta comentarios al final de la línea (3+ espacios y letra)
        for tk in num.findall(izq):
            if tk not in toks_real:
                falta.append((tk, l))
    print(f"===== M{modulo} · bloque Python #{i} · código {p.returncode} · líneas #> esperadas: {len(esperado)} · números esperados ausentes en la salida: {len(falta)} =====")
    if p.returncode != 0:
        malos += 1; print("STDERR:", p.stderr[-800:])
    print(real.rstrip())
    for tk, l in falta:
        print(f"   FALTA {tk:>12}   en la línea esperada:  {l[:110]}")
    print()
print("bloques con código de salida != 0:", malos)
