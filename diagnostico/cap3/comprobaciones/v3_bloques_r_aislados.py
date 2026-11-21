"""v3 · ejecuta cada bloque de R del cap. 3 en una sesion NUEVA (el verificador de bloques los encadena
en una sola sesion, lo que oculta dependencias entre bloques) y avisa de los que fallan.
Uso: python3 v3_bloques_r_aislados.py <capitulo.html> <carpeta de trabajo con la copia de la TRM>"""
import html, re, subprocess, sys, tempfile, os
src = open(sys.argv[1], encoding="utf-8").read()
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    for j, code in enumerate(re.findall(r'<code class="language-r">(.*?)</code>', m.group(2), re.S)):
        code = html.unescape(code)
        ruta = os.path.join(sys.argv[2], f"v3_M{m.group(1)}_{j + 1}.R")
        open(ruta, "w").write(code)   # por archivo: Rscript -e con un bloque largo se colgaba
        r = subprocess.run(["Rscript", "--vanilla", ruta], capture_output=True, text=True, cwd=sys.argv[2], timeout=900)
        errs = [l for l in r.stderr.splitlines() if l.startswith("Error")]
        print(f"M{m.group(1)} bloque R {j + 1}: {'OK' if r.returncode == 0 else 'FALLA'} {errs[:2]}")
