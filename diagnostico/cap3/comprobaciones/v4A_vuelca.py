"""Verificador A · R4 cap. 3: vuelca, por entrada c3-m1..m6, la afirmación tal
como está hoy en el HTML, sus citas visibles, y el contexto de cada literal en
la fuente (página indicada / sección indicada), marcando si el literal está en
la página SIGUIENTE y no en la indicada."""
import sys, re, pathlib, yaml, html
RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A

bib = A.Biblioteca.carga(RAIZ / "bibliografia")
reg = yaml.safe_load((RAIZ / "bibliografia/contraste/cap3.yml").read_text("utf-8"))
htm = (RAIZ / "Htmls_Series/capitulo-3-modelos-ar-ma-arma.html").read_text("utf-8")
lec = A.lee_html(htm)
lot = re.compile(r"^c3-m[1-6]-")
filtro = sys.argv[1] if len(sys.argv) > 1 else None

# citas visibles por afirmación
vis = {}
for c in lec.citas:
    vis.setdefault(c.afirma, []).append((c.clave, c.loc, c.linea))

def ctx(texto, lit, ancho=500):
    n = A.normaliza(texto); l = A.normaliza(lit)
    i = n.find(l)
    if i < 0:
        return None
    return n[max(0, i - ancho): i + len(l) + ancho].replace(l, "<<<" + l + ">>>")

for e in reg["afirmaciones"]:
    if not lot.match(e["id"]) or (filtro and not re.search(filtro, e["id"])):
        continue
    a = lec.afirmaciones.get(e["id"])
    print("=" * 100)
    print(e["id"], "·", e["veredicto"], "·", e["tipo"])
    if a is None:
        print("  !!! NO ESTÁ EN EL HTML")
    else:
        t = re.sub(r"\s+", " ", a.texto).strip()
        print("  HTML l.%d · hash %s (reg %s)%s" % (a.linea, A.huella(a.texto), e.get("hash_texto"),
              "" if A.huella(a.texto) == e.get("hash_texto") else "  !!! HASH DISTINTO"))
        print("  TEXTO:", t)
    print("  CITAS VISIBLES:", vis.get(e["id"], []))
    print("  REG afirmacion:", e.get("afirmacion"))
    if e.get("nota"): print("  NOTA:", re.sub(r"\s+", " ", e["nota"]))
    if e.get("motivo"): print("  MOTIVO:", re.sub(r"\s+", " ", e["motivo"]))
    for k, f in enumerate(e.get("fuentes") or [], 1):
        lit = bib.literal(3, e["id"], k)
        print(f"  -- fuente {k}: {f.get('clave')} {f.get('loc')} {f.get('clase')} pdf={f.get('pagina_pdf')} inst={f.get('instantanea')}")
        print("     LITERAL:", lit)
        if lit is None: continue
        if f.get("clase") == "PDF":
            base = RAIZ / "bibliografia/_local/texto" / f["clave"]
            p = f["pagina_pdf"]
            t1 = (base / f"p{p:04d}.txt").read_text("utf-8") if (base / f"p{p:04d}.txt").exists() else ""
            t2 = (base / f"p{p+1:04d}.txt").read_text("utf-8") if (base / f"p{p+1:04d}.txt").exists() else ""
            c = ctx(t1, lit)
            if c is None:
                c2 = ctx(t1 + "\n" + t2, lit)
                print("     !!! NO en la página indicada;", "SÍ cruzando/página siguiente" if c2 else "TAMPOCO en la siguiente")
                c = c2
            # encabezado: número impreso
            cab = " | ".join(t1.strip().splitlines()[:2])[:120]
            print("     CABECERA p.pdf:", cab)
            print("     CTX:", c)
        else:
            texto, ok = bib.texto_instantanea(f["clave"], str(f.get("instantanea")))
            sec, falta = A.seccion_de(texto or "", str(f.get("loc") or ""))
            c = ctx(sec, lit)
            if c is None:
                print("     !!! NO en la sección", f.get("loc"), "; en la instantánea entera:", ctx(texto or "", lit, 100) is not None)
            print("     CTX:", c)
