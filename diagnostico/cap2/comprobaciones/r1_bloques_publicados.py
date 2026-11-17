#!/usr/bin/env python3
"""R1 del capítulo 2 · los bloques de código, tal como quedaron publicados.

Usa las funciones de `precalculo/verifica_bloques_cap6.py` (misma extracción, misma
ejecución encadenada, mismo directorio de trabajo) y añade una comprobación más
estricta que la suya: cada línea `#>` del HTML tiene que aparecer LITERAL en la salida
real de su bloque, no solo sus números. Imprime además la salida íntegra de cada bloque.

Única abreviatura admitida, declarada en el propio capítulo: de un aviso de R se copia
`#> Warning: <mensaje>`. Los avisos salen por stderr, que el verificador pega al final de
la sesión y por eso atribuye al último bloque; aquí se exige que la sesión de R haya dado
el aviso `Warning in <la llamada de la línea anterior> : <mensaje>`.

Desde la raíz del repo:
  MPLBACKEND=Agg python3 diagnostico/cap2/comprobaciones/r1_bloques_publicados.py \
      > diagnostico/cap2/comprobaciones/r1_bloques_publicados.out 2>&1
"""
import re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import verifica_bloques_cap6 as v

HTML = RAIZ / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html"
bloques = v.extrae([(HTML.name, HTML.read_text(encoding="utf-8"))])
res = {
    "r": v.corre(bloques, "r",
                 'suppressMessages({library(forecast); library(tseries); library(jsonlite)})\noptions(warn = 1)',
                 ["Rscript", "--vanilla"], ".R", 'cat("\\n' + v.SEP + '\\n")'),
    "python": v.corre(bloques, "python", "import warnings; warnings.filterwarnings('ignore')",
                      ["python3"], ".py", 'print("\\n' + v.SEP + '\\n")'),
}
norm = lambda t: re.sub(r"\s+", " ", t).strip()
total = mal = 0
for i, b in enumerate(bloques):
    salida = res[b["lang"]]["trozos"].get(i, "")
    primera = next(l for l in b["codigo"].splitlines() if l.strip())
    print(f"\n=========== bloque #{i} ({b['lang']}) · {primera.strip()[:70]}")
    print(salida.strip("\n"))
    plano = norm(salida)
    todo = norm(res[b["lang"]]["todo"])
    llamada = ""
    for l in b["codigo"].splitlines():
        if not l.strip().startswith("#>"):
            if l.strip() and not l.strip().startswith("#"):
                llamada = norm(l.split("#")[0])
            continue
        total += 1
        esperado = norm(l.strip()[2:])
        if esperado.startswith("Warning: "):
            # p. ej. «Warning in kpss.test(trm) : p-value smaller than printed p-value»
            interior = re.sub(r"\$p\.value$", "", llamada)
            bien = f"Warning in {interior} : {esperado[len('Warning: '):]}" in todo
        else:
            bien = esperado in plano
        if not bien:
            mal += 1
            print(f"   !! NO LITERAL: #> {esperado}")
for lang in res:
    print(f"\nsesión de {lang}: código de salida {res[lang]['codigo_salida']}")
print(f"\n=== {total - mal} de {total} líneas #> aparecen literales en la salida de su bloque ===")
sys.exit(1 if mal else 0)
