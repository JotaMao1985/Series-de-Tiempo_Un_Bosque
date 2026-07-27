#!/usr/bin/env python3
"""Ejecuta los bloques de código del capítulo 6 y contrasta cada cifra anunciada.

El material del curso ha acumulado ya cuatro auditorías en las que la mayor
fuente de errores han sido los comentarios `#>` de los bloques: son plausibles,
nadie los ejecuta, y acaban publicados. Esta herramienta los ejecuta.

Qué hace:
  1. Extrae los bloques `language-r` y `language-python` de las plantillas de
     `ensamblado/cap6/` (o del HTML ya ensamblado) en orden de módulo.
  2. Los ejecuta ENCADENADOS —todos los de R en una sesión, todos los de Python
     en otra—, porque así los ejecutaría un estudiante que sigue el capítulo de
     arriba abajo: si un bloque usa un objeto que nunca se definió, se ve aquí.
  3. Para cada bloque, extrae los números de sus líneas `#>` y comprueba que
     aparezcan en la salida real de ESE bloque.

Uso:  python3 verifica_bloques_cap6.py [--html ruta.html]
"""

import argparse
import html as html_mod
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
FUENTES = RAIZ / "ensamblado" / "cap6"
TMP = Path("/tmp/verifica_cap6")

SEP = "###BLOQUE-%d###"
BLOQUE_RE = re.compile(
    r'<pre><code class="language-(r|python)">(.*?)</code></pre>', re.S)
# Números con signo, decimales y notación científica; `1e-13` incluido.
NUM_RE = re.compile(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?')


def extrae(textos):
    bloques = []
    for nombre, texto in textos:
        for lang, cuerpo in BLOQUE_RE.findall(texto):
            bloques.append({
                "archivo": nombre,
                "lang": lang,
                "codigo": html_mod.unescape(cuerpo),
            })
    return bloques


def esperados(codigo):
    """Números anunciados en las líneas `#>` del bloque."""
    fuera = []
    for linea in codigo.splitlines():
        s = linea.strip()
        marca = "#>" if s.startswith("#>") else ("#&gt;" if s.startswith("#&gt;") else None)
        if marca is None:
            continue
        fuera.extend(NUM_RE.findall(s[len(marca):]))
    return fuera


def limpia(codigo):
    """El código sin sus líneas `#>`, que es lo que de verdad se ejecuta."""
    return "\n".join(l for l in codigo.splitlines() if not l.strip().startswith("#>"))


def corre(bloques, lang, cabecera, comando, sufijo, sep_fmt):
    idx = [i for i, b in enumerate(bloques) if b["lang"] == lang]
    if not idx:
        return {}
    TMP.mkdir(parents=True, exist_ok=True)
    partes = [cabecera]
    for k, i in enumerate(idx):
        partes.append(sep_fmt % k)
        partes.append(limpia(bloques[i]["codigo"]))
    ruta = TMP / f"bloques{sufijo}"
    ruta.write_text("\n\n".join(partes), encoding="utf-8")

    res = subprocess.run(comando + [str(ruta)], capture_output=True, text=True,
                         cwd=str(AQUI), timeout=1800)
    salida = res.stdout + "\n" + res.stderr
    trozos = {}
    partes_salida = re.split(r"###BLOQUE-(\d+)###", salida)
    # partes_salida = [preludio, '0', texto0, '1', texto1, ...]
    for j in range(1, len(partes_salida) - 1, 2):
        trozos[idx[int(partes_salida[j])]] = partes_salida[j + 1]
    return {"trozos": trozos, "codigo_salida": res.returncode, "todo": salida}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default=None,
                    help="HTML ensamblado; por defecto, las plantillas de cap6/")
    args = ap.parse_args()

    if args.html:
        textos = [(Path(args.html).name, Path(args.html).read_text(encoding="utf-8"))]
    else:
        rutas = sorted(FUENTES.glob("templates_*.html"),
                       key=lambda p: int(re.search(r"_(\d+)_", p.name).group(1)))
        if not rutas:
            raise SystemExit(f"ABORTA: no hay plantillas en {FUENTES}")
        textos = [(p.name, p.read_text(encoding="utf-8")) for p in rutas]

    bloques = extrae(textos)
    print(f"Bloques encontrados: {sum(b['lang'] == 'r' for b in bloques)} de R, "
          f"{sum(b['lang'] == 'python' for b in bloques)} de Python\n")

    resultados = {}
    resultados["r"] = corre(
        bloques, "r",
        'suppressMessages({library(forecast); library(tseries); library(jsonlite)})\n'
        'options(warn = 1)',
        ["Rscript", "--vanilla"], ".R", 'cat("\\n' + SEP + '\\n")')
    resultados["python"] = corre(
        bloques, "python",
        "import warnings; warnings.filterwarnings('ignore')",
        ["python3"], ".py", 'print("\\n' + SEP + '\\n")')

    total_ok = total = 0
    fallos = []
    for i, b in enumerate(bloques):
        r = resultados[b["lang"]]
        if not r:
            continue
        salida = r["trozos"].get(i, "")
        esp = esperados(b["codigo"])
        vistos = set(NUM_RE.findall(salida))
        faltan = []
        for e in esp:
            total += 1
            if e in vistos or e in salida:
                total_ok += 1
            else:
                faltan.append(e)
        if faltan:
            fallos.append((i, b, faltan, salida))

    for i, b, faltan, salida in fallos:
        primera = next((l for l in b["codigo"].splitlines() if l.strip()), "")
        print(f"--- bloque #{i} ({b['lang']}, {b['archivo']}) ---")
        print(f"    empieza por: {primera.strip()[:78]}")
        print(f"    NO aparecen en la salida: {faltan}")
        print("    salida real:")
        for l in salida.strip().splitlines()[:22]:
            print("      " + l)
        print()

    for lang in ("r", "python"):
        r = resultados[lang]
        if r and r["codigo_salida"] != 0:
            print(f"!! la sesión de {lang} terminó con código {r['codigo_salida']}")
            print("\n".join(r["todo"].strip().splitlines()[-25:]))

    print(f"\n=== {total_ok} de {total} cifras anunciadas aparecen en la salida real "
          f"({len(fallos)} bloques con discrepancias) ===")
    return 0 if total_ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
