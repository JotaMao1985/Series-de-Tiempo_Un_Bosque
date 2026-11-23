"""Verificador A · R4 cap. 4: vuelca, por entrada c4-m1..m6, la afirmación tal
como está hoy en el HTML (y si su huella coincide con hash_texto), sus citas
visibles, y el contexto (±500 car.) de cada literal en la fuente, en la página
del PDF indicada (con la cabecera y el pie para leer el número impreso) o en la
sección acotada como la acota el auditor."""
import sys, re, pathlib, yaml
RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A

bib = A.Biblioteca.carga(RAIZ / "bibliografia")
reg = yaml.safe_load((RAIZ / "bibliografia/contraste/cap4.yml").read_text("utf-8"))
htm = (RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html").read_text("utf-8")
lec = A.lee_html(htm)
lot = re.compile(r"^c4-m[1-6]-")
filtro = sys.argv[1] if len(sys.argv) > 1 else None
ancho = int(sys.argv[2]) if len(sys.argv) > 2 else 500

vis = {}
for c in lec.citas:
    vis.setdefault(c.afirma, []).append((c.clave, c.loc, c.linea))

def ctx(texto, lit):
    n = A.normaliza(texto); l = A.normaliza(lit)
    i = n.find(l)
    if i < 0:
        return None
    return n[max(0, i - ancho): i + len(l) + ancho].replace(l, "<<<" + l + ">>>")

cuenta = {"n": 0, "hash_mal": 0, "no_html": 0, "lit_no": 0, "pag_sig": 0}
for e in reg["afirmaciones"]:
    if not lot.match(e["id"]) or (filtro and not re.search(filtro, e["id"])):
        continue
    cuenta["n"] += 1
    a = lec.afirmaciones.get(e["id"])
    print("=" * 100)
    print(e["id"], "·", e["veredicto"], "·", e["tipo"])
    if a is None:
        print("  !!! NO ESTÁ EN EL HTML"); cuenta["no_html"] += 1
    else:
        t = re.sub(r"\s+", " ", a.texto).strip()
        ok = A.huella(a.texto) == e.get("hash_texto")
        if not ok: cuenta["hash_mal"] += 1
        print("  HTML l.%d · hash %s (reg %s)%s" % (a.linea, A.huella(a.texto), e.get("hash_texto"),
              "" if ok else "  !!! HASH DISTINTO"))
        print("  TEXTO:", t)
    print("  CITAS VISIBLES:", vis.get(e["id"], []))
    print("  REG afirmacion:", e.get("afirmacion"))
    if e.get("nota"): print("  NOTA:", re.sub(r"\s+", " ", e["nota"]))
    if e.get("motivo"): print("  MOTIVO:", re.sub(r"\s+", " ", e["motivo"]))
    for k, f in enumerate(e.get("fuentes") or [], 1):
        lit = bib.literal(4, e["id"], k)
        print(f"  -- fuente {k}: {f.get('clave')} {f.get('loc')} {f.get('clase')} pdf={f.get('pagina_pdf')} inst={f.get('instantanea')}")
        print("     LITERAL:", lit)
        if lit is None:
            continue
        if f.get("clase") == "PDF":
            base = RAIZ / "bibliografia/_local/texto" / f["clave"]
            p = f["pagina_pdf"]
            t1 = (base / f"p{p:04d}.txt").read_text("utf-8") if (base / f"p{p:04d}.txt").exists() else ""
            t2 = (base / f"p{p+1:04d}.txt").read_text("utf-8") if (base / f"p{p+1:04d}.txt").exists() else ""
            c = ctx(t1, lit)
            if c is None:
                c2 = ctx(t1 + "\n" + t2, lit)
                print("     !!! NO en la página indicada;", "SÍ cruzando/página siguiente" if c2 else "TAMPOCO en la siguiente")
                cuenta["pag_sig" if c2 else "lit_no"] += 1
                c = c2
            lin = [l for l in t1.strip().splitlines() if l.strip()]
            print("     CABECERA:", " | ".join(lin[:2])[:120])
            print("     PIE:", " | ".join(lin[-2:])[:120])
            print("     CTX:", c)
        else:
            texto, okh = bib.texto_instantanea(f["clave"], str(f.get("instantanea")))
            sec, falta = A.seccion_de(texto or "", str(f.get("loc") or ""))
            c = ctx(sec, lit)
            if c is None:
                cuenta["lit_no"] += 1
                print("     !!! NO en la sección", f.get("loc"), "(falta:", falta, "); en la instantánea entera:",
                      ctx(texto or "", lit) is not None)
            print("     CTX:", c)
print("=" * 100)
print("RESUMEN", cuenta)
