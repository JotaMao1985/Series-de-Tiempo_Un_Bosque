#!/usr/bin/env python3
"""R5 del capítulo 4 · que ningún texto marcado ni ningún <cite> cambie (HTML ensamblado, b53fdcb frente a ahora).

Para cada `<span data-afirma="id">…</span>` compara el elemento entero, byte a byte; de los `<cite …>…</cite>`,
el multiconjunto. Informa además de los ids que cambian de orden (los que la ronda movió de sitio).
Uso: python3 diagnostico/cap4/comprobaciones/r5_afirma.py > diagnostico/cap4/comprobaciones/r5_afirma.out
"""
import collections, pathlib, re, subprocess, sys
RAIZ = pathlib.Path(__file__).resolve().parents[3]
RUTA = "Htmls_Series/capitulo-4-modelos-arima.html"


def elemento(t, i):
    nivel = 0
    for m in re.finditer(r"<span\b|</span>", t[i:]):
        nivel += 1 if m.group() != "</span>" else -1
        if nivel == 0:
            return t[i:i + m.end()]
    raise ValueError(i)


def marcas(t):
    return [(m.group(1), elemento(t, m.start())) for m in re.finditer(r'<span data-afirma="([^"]+)">', t)]


antes = subprocess.run(["git", "show", f"b53fdcb:{RUTA}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
ahora = (RAIZ / RUTA).read_text(encoding="utf-8")
a, b = marcas(antes), marcas(ahora)
da, db = dict(a), dict(b)
cambian = sorted(k for k in da if k in db and da[k] != db[k])
ca = collections.Counter(re.findall(r"<cite\b.*?</cite>", antes, flags=re.S))
cb = collections.Counter(re.findall(r"<cite\b.*?</cite>", ahora, flags=re.S))
def otras(t):
    """Marcas en elementos que no son <span> (celdas, ítems…): id -> texto hasta el cierre de esa etiqueta."""
    return {m.group(2): t[m.start():t.index(f"</{m.group(1)}>", m.start())]
            for m in re.finditer(r'<(?!span\b)(\w+)[^>]*\bdata-afirma="([^"]+)"[^>]*>', t)}


xa, xb = otras(antes), otras(ahora)
print(f"marcas fuera de <span>: {len(xa)} antes, {len(xb)} ahora; idénticas: {xa == xb}; total de data-afirma: "
      f"{antes.count('data-afirma=')} antes, {ahora.count('data-afirma=')} ahora")
print(f"data-afirma: {len(a)} antes, {len(b)} ahora; ids que faltan: {sorted(set(da) - set(db))}; nuevos: {sorted(set(db) - set(da))}")
print(f"elementos marcados cuyo contenido cambia: {cambian}")
print(f"<cite>: {sum(ca.values())} antes, {sum(cb.values())} ahora; multiconjunto idéntico: {ca == cb}")
oa, ob = [k for k, _ in a], [k for k, _ in b]
movidos = [k for k in oa if k in db and oa.index(k) != ob.index(k)] if oa != ob else []
if oa != ob:
    import difflib
    movidos = sorted({l[2:] for l in difflib.unified_diff(oa, ob, lineterm="", n=0) if l[:1] in "+-" and l[:2] not in ("++", "--")} )
    movidos = sorted({l[1:] for l in difflib.unified_diff(oa, ob, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))})
print(f"ids que cambian de sitio en el orden de la página: {movidos}")
sys.exit(0 if not cambian and set(da) == set(db) and ca == cb and xa == xb else 1)
