"""V3 · ejecuta cada bloque de R del capítulo 4 ensamblado en una carpeta vacía (con la copia de la TRM) y cruza las
líneas `#>` con la salida real, token a token. Independiente de verifica_bloques_cap6.py.
Uso: python3 diagnostico/cap4/comprobaciones/v3_bloques_r.py > .../v3_bloques_r.out 2>&1"""
import html, pathlib, re, shutil, subprocess, tempfile
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
malos = 0
for i, (lang, modulo, cuerpo) in enumerate(bloques):
    if lang != "r":
        continue
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t); shutil.copy(CSV, t / CSV.name)
        (t / "b.R").write_text(cuerpo, encoding="utf-8")
        # echo=FALSE: solo la salida impresa, como en la consola sin los comandos
        p = subprocess.run(["Rscript", "-e", "source('b.R', echo = FALSE, print.eval = TRUE)"], cwd=t, capture_output=True, text=True, timeout=1800)
    esperado = [l[2:].strip() for l in cuerpo.splitlines() if l.startswith("#>")]
    real = p.stdout
    toks_real = set(num.findall(real))
    falta = []
    for l in esperado:
        izq = re.split(r"\s{3,}[a-zA-Z<(\"']", l)[0]
        for tk in num.findall(izq):
            if tk not in toks_real:
                falta.append((tk, l))
    print(f"===== M{modulo} · bloque R #{i} · código {p.returncode} · líneas #> esperadas: {len(esperado)} · números esperados ausentes: {len(falta)} =====")
    if p.returncode != 0:
        malos += 1; print("STDERR:", p.stderr[-800:])
    for tk, l in falta:
        print(f"   FALTA {tk:>12}   en:  {l[:110]}")
    if modulo in (1, 3, 4) or (modulo == 10 and i > 17):
        print(real.rstrip())
    print()
print("bloques con código != 0:", malos)
