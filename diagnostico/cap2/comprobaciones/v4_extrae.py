#!/usr/bin/env python3
"""v4_extrae.py — verificador independiente de la R4 del capítulo 2.

Para cada entrada de bibliografia/contraste/cap2.yml escribe:
  - el texto marcado en el HTML, con las citas visibles en su sitio («⟦clave loc⟧»);
  - por cada fuente, dónde está la cita literal en la caché: archivo, línea,
    página del PDF (la indicada o la siguiente, que el auditor también acepta),
    la sección de FPP3 o de la ayuda de R que la contiene, y un contexto.

No escribe nada en el repo salvo su salida (v4_extrae.out).
Uso: python3 diagnostico/cap2/comprobaciones/v4_extrae.py [ids…] > …/v4_extrae.out (sin ids, todas)
"""
from __future__ import annotations

import html.parser
import pathlib
import re
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
from audita_citas import normaliza  # noqa: E402

HTML = RAIZ / "Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html"
REG = RAIZ / "bibliografia/contraste/cap2.yml"
LOCAL = RAIZ / "bibliografia/_local"
VACIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
          "source", "track", "wbr"}


class L(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila = []
        self.txt = {}
        self.linea = {}

    def actual(self):
        return next((a for _, a in reversed(self.pila) if a), None)

    def handle_starttag(self, t, at):
        a = dict(at)
        idf = a.get("data-afirma")
        if idf:
            self.txt[idf] = ""
            self.linea[idf] = self.getpos()[0]
        cur = idf or self.actual()
        if t == "cite" and cur:
            self.txt[cur] += f"⟦{a.get('data-ref')} {a.get('data-loc')}⟧"
        if t not in VACIOS:
            self.pila.append((t, idf if idf else (None if t != "cite" else "§CITE")))

    def handle_endtag(self, t):
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == t:
                del self.pila[i:]
                return

    def handle_data(self, d):
        if self.pila and self.pila[-1][0] in ("script", "style"):
            return
        if any(a == "§CITE" for _, a in self.pila):
            return
        cur = next((a for _, a in reversed(self.pila) if a and a != "§CITE"), None)
        if cur:
            self.txt[cur] += d


def seccion(lineas, i, web):
    if web == "R":
        for j in range(i, -1, -1):
            if re.fullmatch(r"[A-Z][A-Za-z() ]*:", lineas[j].rstrip()):
                return lineas[j].strip()
        return "?"
    for j in range(i, -1, -1):
        if re.match(r"^\d+(?:\.\d+)*\s{1,4}[A-ZÁÉÍÓÚ¿]", lineas[j]):
            return lineas[j].strip()[:60]
    return "?"


def busca(texto_lineas, cita):
    """Índice de línea donde empieza la cita (tolerando saltos de línea)."""
    n = normaliza(cita)
    for i in range(len(texto_lineas)):
        bloque = normaliza("\n".join(texto_lineas[i:i + 4]))
        if n in bloque:
            # afinar: la línea más tardía que aún lo contiene empezando ahí
            return i
    return None


def main():
    lector = L()
    lector.feed(HTML.read_text("utf-8"))
    reg = yaml.safe_load(REG.read_text("utf-8"))
    # Desde el 2026-11-17 el literal vive fuera de git (precalculo/migra_citas_fuera.py).
    literales = (yaml.safe_load((LOCAL / "citas" / "cap2.yml").read_text("utf-8")) or {}).get("citas") or {}
    filtro = set(sys.argv[1:])
    for e in reg["afirmaciones"]:
        i = e["id"]
        if filtro and i not in filtro:
            continue
        print("=" * 100)
        print(f"{i} · {e['veredicto']} · HTML línea {lector.linea.get(i)}")
        print("AFIRMACION (registro):", e["afirmacion"])
        t = re.sub(r"\s+", " ", lector.txt.get(i, "¿SIN MARCA?")).strip()
        print("HTML:", t)
        for n, f in enumerate(e.get("fuentes") or [], start=1):
            cl, cita = f["clave"], f.get("cita") or (literales.get(i) or {}).get(n, "¿SIN LITERAL LOCAL?")
            print(f"  -- {cl} · {f['loc']} · «{cita}»")
            if f["clase"] == "PDF":
                p = f["pagina_pdf"]
                hallado = False
                for q in (p, p + 1):
                    ruta = LOCAL / "texto" / cl / f"p{q:04d}.txt"
                    if not ruta.is_file():
                        continue
                    L_ = ruta.read_text("utf-8").splitlines()
                    k = busca(L_, cita)
                    if k is not None:
                        borde = (L_[0][:50] if L_ else "") + " … " + (L_[-1][:50] if L_ else "")
                        print(f"     en {ruta.relative_to(RAIZ)}:{k+1}  {'(PÁGINA SIGUIENTE)' if q != p else ''}  bordes: {borde}")
                        for x in L_[max(0, k - 3):k + 5]:
                            print("       |", x)
                        hallado = True
                        break
                if not hallado:
                    print("     !! NO HALLADA")
            else:
                ruta = LOCAL / "web" / cl / f"{f['instantanea']}.txt"
                L_ = ruta.read_text("utf-8").splitlines()
                k = busca(L_, cita)
                if k is None:
                    print("     !! NO HALLADA en", ruta.name)
                else:
                    sec = seccion(L_, k, "R" if cl == "rcoreteam2026r" else "F")
                    print(f"     en {ruta.relative_to(RAIZ)}:{k+1}  sección: {sec}")
                    for x in L_[max(0, k - 3):k + 5]:
                        print("       |", x[:220])
        if e.get("nota"):
            print("NOTA:", e["nota"])
        if e.get("motivo"):
            print("MOTIVO:", e["motivo"])


if __name__ == "__main__":
    main()
