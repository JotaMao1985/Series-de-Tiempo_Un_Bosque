"""Verificador R5 cap. 3: cada bloque de R de los «Para practicar» y de los ejercicios 1-3,
ejecutado SOLO en una sesion limpia; compara cada linea #> con la salida real."""
import re, html, subprocess, tempfile, os
src = open("ensamblado/cap3/cap3_modulos.html", encoding="utf-8").read()
paneles = re.findall(r'id="(c3m\d-sol|c3e\d-sol)".*?<pre><code class="language-r">(.*?)</code></pre>', src, re.S)
for ident, code in paneles:
    code = html.unescape(code)
    esperado = [l[3:].rstrip() for l in code.splitlines() if l.startswith("#>")]
    limpio = "\n".join(l for l in code.splitlines() if not l.startswith("#>"))
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as f: f.write(limpio); ruta = f.name
    r = subprocess.run(["Rscript", ruta], capture_output=True, text=True, timeout=900); os.unlink(ruta)
    salida = [l.rstrip() for l in r.stdout.splitlines()]
    norm = lambda s: " ".join(s.split())
    faltan = [e for e in esperado if norm(e.split("<-")[0]) and not any(norm(e.split("<-")[0]).strip() in norm(s) for s in salida)]
    print(f"{ident}: exit={r.returncode} lineas #>={len(esperado)} no encontradas={len(faltan)}")
    for e in faltan: print("   FALTA:", e)
    if r.returncode: print("   STDERR:", r.stderr[-400:])
