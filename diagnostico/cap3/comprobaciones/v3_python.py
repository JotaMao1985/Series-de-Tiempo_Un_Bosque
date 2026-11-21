"""v3 · ejecuta los bloques de Python de los modulos que toco la R3 (1, 3, 9) tal como estan en el HTML
final y guarda cada salida junto a su codigo, para compararla con los comentarios.
Uso: python3 v3_python.py <capitulo.html> <carpeta de trabajo con trm_mensual_*.csv>"""
import html, re, subprocess, sys, os
src = open(sys.argv[1], encoding="utf-8").read()
wd = sys.argv[2]
for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', src, re.S):
    k = int(m.group(1))
    if k not in (1, 3, 9):
        continue
    for j, code in enumerate(re.findall(r'<code class="language-python">(.*?)</code>', m.group(2), re.S)):
        code = html.unescape(code)
        print(f"\n######## M{k} bloque Python {j + 1} ########")
        r = subprocess.run([sys.executable, "-c", "import warnings; warnings.filterwarnings('ignore')\n" + code],
                           capture_output=True, text=True, cwd=wd, timeout=600)
        print(r.stdout)
        if r.returncode:
            print("!! STDERR:", r.stderr[-1500:])
