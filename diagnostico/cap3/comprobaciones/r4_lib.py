#!/usr/bin/env python3
"""
r4_lib.py — piezas comunes de la ronda R4 (fuentes) del capítulo 3

La notación de las marcas es la de `diagnostico/cap2/comprobaciones/r4_marca.py`
(el texto original es el mismo sin las marcas):

  [[c3-m1-01]] … [[/]]   <span data-afirma="c3-m1-01"> … </span>
  [[@c3-m1-06]]          atributo data-afirma dentro de la etiqueta que lo lleva
  {{F|§9.3}}             cita vacía, con un espacio delante
  {{^F|§9.3|narrativa}}  sin espacio delante, y con data-modo
  [[+.]]                 texto que se añade (un punto tras la cita)

Claves: F = FPP3, C = Cryer y Chan, H = Hamilton, R = ayuda de R,
Y = Yule (1927), K = Hyndman y Khandakar (2008),
S = Shumway y Stoffer 3.ª (solo en el registro: no se cita a la vista).
Los blancos del original se respetan: al buscar, cualquier tramo de blancos
casa con cualquier otro. Cada texto tiene que aparecer EXACTAMENTE una vez.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A  # noqa: E402

BASE = "6fe8b18"          # el capítulo 3 tras la R3, sin ninguna cita marcada
FUENTE = "ensamblado/cap3/cap3_modulos.html"
CLAVES = {"F": "hyndman2021forecasting", "C": "cryer2008time", "H": "hamilton1994time",
          "R": "rcoreteam2026r", "S": "shumway2011time",
          "Y": "yule1927method", "K": "hyndman2008automatic"}

RE_MARCA = re.compile(r"\[\[(/|@[a-z0-9-]+|\+[^\]]*|c\d-m\d+-\d+)\]\]"
                      r"|\{\{(\^?)([FCHRSYK])\|([^|}]+)(?:\|(\w+))?\}\}")


class Aborta(Exception):
    pass


def base() -> str:
    """Los módulos del capítulo 3 tal como estaban en BASE."""
    return subprocess.run(["git", "show", f"{BASE}:{FUENTE}"], cwd=RAIZ, capture_output=True,
                          check=True).stdout.decode("utf-8")


def flexible(texto: str) -> str:
    partes = re.split(r"(\s+)", texto)
    return "".join(r"\s+" if p.isspace() else re.escape(p) for p in partes if p != "")


def expande(m: re.Match) -> str:
    if m.group(1) is not None:
        t = m.group(1)
        if t == "/":
            return "</span>"
        if t.startswith("@"):
            return f' data-afirma="{t[1:]}"'
        if t.startswith("+"):
            return t[1:]
        return f'<span data-afirma="{t}">'
    pegada, clave, loc, modo = m.group(2), CLAVES[m.group(3)], m.group(4), m.group(5)
    extra = f' data-modo="{modo}"' if modo else ""
    return (("" if pegada else " ")
            + f'<cite class="cita" data-ref="{clave}" data-loc="{loc}"{extra}></cite>')


def aplica(html: str, viejo: str | None, nuevo: str, etiqueta: str) -> str:
    """Sustituye `viejo` (o `nuevo` sin marcas) por `nuevo` con las marcas expandidas."""
    if viejo is None:
        trozos, ultimo = [], 0
        for m in RE_MARCA.finditer(nuevo):
            trozos.append(("lit", nuevo[ultimo:m.start()]))
            trozos.append(("marca", m))
            ultimo = m.end()
        trozos.append(("lit", nuevo[ultimo:]))
        if not any(t == "marca" for t, _ in trozos):
            raise Aborta(f"[{etiqueta}]: la marca no lleva ninguna marca\n   {nuevo[:110]}")
        patron = "".join(f"({flexible(t)})" for tipo, t in trozos if tipo == "lit")
        halla = list(re.finditer(patron, html))
        if len(halla) != 1:
            raise Aborta(f"[{etiqueta}]: aparece {len(halla)} veces, se esperaba 1\n   {nuevo[:140]}")
        h, n, salida = halla[0], 0, []
        for tipo, t in trozos:
            if tipo == "lit":
                n += 1
                salida.append(h.group(n))
            else:
                salida.append(expande(t))
        return html[:h.start()] + "".join(salida) + html[h.end():]
    halla = list(re.finditer(flexible(viejo), html))
    if len(halla) != 1:
        raise Aborta(f"[{etiqueta}]: aparece {len(halla)} veces, se esperaba 1\n   {viejo[:140]}")
    h = halla[0]
    return html[:h.start()] + RE_MARCA.sub(expande, nuevo) + html[h.end():]


_BIB = None


def biblioteca() -> A.Biblioteca:
    global _BIB
    if _BIB is None:
        _BIB = A.Biblioteca.carga(RAIZ / "bibliografia")
    return _BIB


def comprueba_fuente(f: dict, donde: str) -> list[str]:
    """Lo que el auditor comprobará de esta fuente (F04, F05, F06, F07, F11), ya."""
    bib, fallos = biblioteca(), []
    literal = f.get("cita")
    for campo in ("clave", "loc", "clase", "cita"):
        if not f.get(campo):
            fallos.append(f"{donde}: falta `{campo}`")
    if fallos:
        return fallos
    if f["clave"] not in bib.referencias:
        return [f"{donde}: la clave «{f['clave']}» no está en referencias.json"]
    if not A.localizador_valido(f["loc"]):
        fallos.append(f"{donde}: el localizador «{f['loc']}» no usa el vocabulario cerrado")
    if f["clase"] == "PDF" and not isinstance(f.get("pagina_pdf"), int):
        fallos.append(f"{donde}: clase PDF sin `pagina_pdf` (entero)")
    if f["clase"] in ("WEB", "DOC") and not f.get("instantanea"):
        fallos.append(f"{donde}: clase {f['clase']} sin `instantanea`")
    if A.palabras_cita(literal) > A.MAX_PALABRAS_CITA:
        fallos.append(f"{donde}: la cita tiene {A.palabras_cita(literal)} palabras (máximo 25)")
    cuenta = {"sin_guion": 0, "sin_literal": 0, "sin_cache": 0, "comprobadas": 0}
    fallos += [str(h) for h in A.f05_cita_literal(bib, f, donde, False, cuenta, literal)]
    fallos += [str(h) for h in A.f06_f07_ejemplar(bib, f, donde)]
    if f["clase"] == "PDF" and isinstance(f.get("pagina_pdf"), int):
        # el auditor acepta la cita en la página o en la siguiente: aquí se exige
        # la página dicha (o que el localizador sea un rango pp. N–N+1)
        hoja = bib.dir / "_local" / "texto" / f["clave"] / f"p{f['pagina_pdf']:04d}.txt"
        if hoja.is_file() and A.normaliza(literal) not in A.normaliza(hoja.read_text("utf-8")) \
                and not f["loc"].startswith("pp. "):
            fallos.append(f"{donde}: la cita no está entera en la página {f['pagina_pdf']} del PDF "
                          "(¿cruza a la siguiente? entonces el localizador es pp. N–N+1)")
    return fallos
