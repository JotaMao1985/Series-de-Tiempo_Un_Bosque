"""Verificador B, R4 del cap. 4: vuelca cada entrada c4-m7..m10 con su prosa de hoy,
su huella, sus citas visibles, el literal de cada fuente y ±500 caracteres de la fuente
alrededor del literal (en el sitio que dice el localizador).

Uso: python3 diagnostico/cap4/comprobaciones/v4B_vuelca.py > diagnostico/cap4/comprobaciones/v4B_vuelca.out
     (con un id o prefijo como argumento, solo esas entradas)
"""
from __future__ import annotations

import html as H
import pathlib
import re
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A  # noqa: E402

HTML = RAIZ / "Htmls_Series" / "capitulo-4-modelos-arima.html"
REG = RAIZ / "bibliografia" / "contraste" / "cap4.yml"
LOTE = re.compile(r"^c4-m(7|8|9|10)-")


def parrafo(crudo: str, ident: str) -> str:
    """Texto del bloque que contiene la marca: del <p|li|td|div|figcaption anterior al cierre."""
    i = crudo.find(f'data-afirma="{ident}"')
    if i < 0:
        return "(no está en el HTML)"
    ini = max(crudo.rfind("<p", 0, i), crudo.rfind("<li", 0, i), crudo.rfind("<td", 0, i),
              crudo.rfind("<figcaption", 0, i), crudo.rfind("<h", 0, i))
    ini = max(ini, i - 2500)
    fin_c = [crudo.find(t, i) for t in ("</p>", "</li>", "</td>", "</figcaption>", "</div>")]
    fin = min([f for f in fin_c if f > 0] + [i + 3000])
    trozo = crudo[ini:fin]
    trozo = re.sub(r"<cite[^>]*>(.*?)</cite>", r" ⟦CITA \1⟧ ", trozo, flags=re.S)
    trozo = re.sub(r"<[^>]+>", " ", trozo)
    return A.normaliza(H.unescape(trozo))


def main() -> None:
    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    crudo = HTML.read_text("utf-8")
    lector = A.lee_html(crudo)
    bib = A.Biblioteca.carga(RAIZ / "bibliografia")
    reg = yaml.safe_load(REG.read_text("utf-8"))
    n = 0
    for e in reg["afirmaciones"]:
        ident = e["id"]
        if not LOTE.match(ident) or (filtro and not ident.startswith(filtro)):
            continue
        n += 1
        print("=" * 100)
        print(f"{ident} · {e.get('tipo')} · {e.get('veredicto')}")
        a = lector.afirmaciones.get(ident)
        if a is None:
            print("  !! NO HAY data-afirma EN EL HTML")
        else:
            h = A.huella(a.texto)
            print(f"  huella {h} · registro {e.get('hash_texto')} · {'COINCIDE' if h == e.get('hash_texto') else '!! DISTINTA'}"
                  f" · línea {a.linea}")
            print(f"  TEXTO HOY: {A.normaliza(a.texto)}")
        print(f"  PÁRRAFO: {parrafo(crudo, ident)}")
        citas = [c for c in lector.citas if c.afirma == ident]
        print("  CITAS VISIBLES: " + ("; ".join(f"{c.clave} {c.loc} (l. {c.linea})" for c in citas) or "ninguna"))
        for campo in ("nota", "motivo"):
            if e.get(campo):
                print(f"  {campo.upper()}: {A.normaliza(str(e[campo]))}")
        for k, f in enumerate(e.get("fuentes") or [], start=1):
            lit = bib.literal(4, ident, k)
            print(f"  -- fuente {k}: {f.get('clave')} · {f.get('loc')} · {f.get('clase')}"
                  f" · pdf {f.get('pagina_pdf')} · inst {f.get('instantanea')}")
            if lit is None:
                print("     !! sin literal")
                continue
            ok_h = A.huella_cita(lit) == f.get("cita_sha256")
            print(f"     LITERAL ({'huella ok' if ok_h else '!! HUELLA DISTINTA'}): {lit}")
            if f.get("clase") == "PDF":
                texto = bib.texto_pdf(f["clave"], f["pagina_pdf"])
            elif f.get("clase") in ("WEB", "DOC"):
                texto, coincide = bib.texto_instantanea(f["clave"], str(f.get("instantanea")))
                if texto is not None:
                    if not coincide:
                        print("     !! instantánea con sha distinto")
                    texto, falta = A.seccion_de(texto, str(f.get("loc") or ""))
                    if falta:
                        print(f"     !! sección {falta} no hallada")
            else:
                texto = None
            if texto is None:
                print("     (sin texto en la caché)")
                continue
            t = A.normaliza(texto)
            j = t.find(A.normaliza(lit))
            if j < 0:
                print("     !! LITERAL NO HALLADO EN EL SITIO")
                continue
            ini, fin = max(0, j - 500), min(len(t), j + len(A.normaliza(lit)) + 500)
            print(f"     CONTEXTO: …{t[ini:j]}【{t[j:j + len(A.normaliza(lit))]}】{t[j + len(A.normaliza(lit)):fin]}…")
    print(f"\n{n} entradas volcadas")


if __name__ == "__main__":
    main()
