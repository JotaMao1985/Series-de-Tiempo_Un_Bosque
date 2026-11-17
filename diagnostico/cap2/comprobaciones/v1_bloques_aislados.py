#!/usr/bin/env python3
"""Verificador independiente · R1 cap. 2 · cada bloque de código, SOLO.

A diferencia de verifica_bloques_cap6.py (que encadena todos los bloques de un
lenguaje en una sesión y solo busca que cada número de las líneas `#>` aparezca
en algún lugar de la salida), aquí:
  1. cada bloque corre en un proceso nuevo, como lo copiaría un estudiante;
  2. cada línea `#>` se busca como LÍNEA completa (espacios normalizados) en la
     salida, en orden.
Uso: python3 v1_bloques_aislados.py HTML DIR_DE_TRABAJO
"""
import html as H, re, subprocess, sys, os, tempfile
from pathlib import Path

htmltxt = Path(sys.argv[1]).read_text(encoding="utf-8")
cwd = sys.argv[2]
lineas_html = htmltxt.split("\n")
BLOQ = re.compile(r'<pre><code class="language-(r|python)">(.*?)</code></pre>', re.S)
norm = lambda s: re.sub(r"\s+", " ", s.strip())
env = dict(os.environ, MPLBACKEND="Agg")
for i, m in enumerate(BLOQ.finditer(htmltxt)):
    lang, cuerpo = m.group(1), H.unescape(m.group(2))
    linea = htmltxt[:m.start()].count("\n") + 1
    esperadas = [l.strip()[2:].strip() for l in cuerpo.splitlines() if l.strip().startswith("#>")]
    codigo = "\n".join(l for l in cuerpo.splitlines() if not l.strip().startswith("#>"))
    suf = ".R" if lang == "r" else ".py"
    with tempfile.NamedTemporaryFile("w", suffix=suf, delete=False) as f:
        f.write(codigo); ruta = f.name
    cmd = ["Rscript", "--vanilla", ruta] if lang == "r" else ["python3", ruta]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=900, env=env)
        out, rc = r.stdout + "\n" + r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        out, rc = "TIMEOUT", -1
    salida = [norm(l) for l in out.splitlines() if l.strip()]
    pos, faltan = 0, []
    for e in esperadas:
        ne = norm(e)
        k = next((j for j in range(pos, len(salida)) if ne == salida[j] or (ne and ne in salida[j])), None)
        if k is None:
            faltan.append(e)
        else:
            pos = k + 1
    estado = "OK" if rc == 0 and not faltan else "REVISAR"
    print(f"[{estado}] bloque {i:2d} {lang:6s} l. {linea}  rc={rc}  #>={len(esperadas)}  no casan={len(faltan)}")
    for e in faltan:
        print(f"      esperado y no visto (en orden): {e!r}")
    if rc != 0:
        print("      cola de la salida:")
        for l in out.strip().splitlines()[-8:]:
            print("        " + l)
