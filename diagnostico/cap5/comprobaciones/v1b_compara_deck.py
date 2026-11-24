"""Verificador B, R1 del cap. 5: qué cambió en el deck construido entre 7686d33 y el árbol,
separando las diapositivas corregidas de lo que entró por la skill (CSS, JS, armazón)."""
import difflib
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
RUTA = "Htmls_Series/diapositivas/capitulo-5-sarima.html"

viejo = subprocess.run(["git", "show", f"7686d33:{RUTA}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
nuevo = (RAIZ / RUTA).read_text(encoding="utf-8")
print(f"tamaño: {len(viejo)} -> {len(nuevo)} caracteres")


def partes(html):
    estilos = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S)
    scripts = re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>", html, flags=re.S)
    externos = re.findall(r"<(?:script|link)[^>]*(?:src|href)=\"([^\"]+)\"", html)
    secciones = re.findall(r"(<section\b.*?</section>)", html, flags=re.S)
    return estilos, scripts, externos, secciones


ev, sv, xv, secv = partes(viejo)
en, sn, xn, secn = partes(nuevo)
print(f"bloques <style>: {len(ev)} -> {len(en)}; <script> en línea: {len(sv)} -> {len(sn)}; diapositivas <section>: {len(secv)} -> {len(secn)}")
print("recursos externos iguales:", xv == xn)
if xv != xn:
    print("  antes:", xv, "\n  ahora:", xn)


def muestra(a, b, nombre, maximo=200):
    d = list(difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0))
    mas = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
    menos = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
    print(f"\n== {nombre}: +{mas} / -{menos} líneas")
    for l in d[:maximo]:
        print("   " + l[:220])


muestra("\n".join(ev), "\n".join(en), "CSS")
muestra("\n".join(sv), "\n".join(sn), "JS en línea", maximo=120)


def titulo(sec):
    m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", sec, flags=re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()[:90] if m else "(sin título)"


print("\n== diapositivas que cambian (por posición)")
for i, (a, b) in enumerate(zip(secv, secn), 1):
    if a != b:
        ta, tb = titulo(a), titulo(b)
        sa = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a))
        sb = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", b))
        solo_marcado = sa == sb
        print(f"  {i:3d}. {'[solo marcado] ' if solo_marcado else ''}{tb}" + (f"   (antes: {ta})" if ta != tb else ""))
        if solo_marcado:
            d = [l for l in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
                 if l[:1] in "+-" and not l.startswith(("+++", "---"))]
            for l in d[:6]:
                print("        " + l[:200])

# Fuera de <style>, <script> y <section>: el armazón
def armazon(html):
    h = re.sub(r"<style[^>]*>.*?</style>", "<style/>", html, flags=re.S)
    h = re.sub(r"<script[^>]*>.*?</script>", "<script/>", h, flags=re.S)
    h = re.sub(r"<section\b.*?</section>", "<section/>", h, flags=re.S)
    return h


muestra(armazon(viejo), armazon(nuevo), "armazón fuera de style/script/section", maximo=60)
