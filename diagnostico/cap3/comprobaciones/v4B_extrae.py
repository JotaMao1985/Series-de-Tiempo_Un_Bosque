#!/usr/bin/env python3
"""Verificador B, R4 cap. 3: por cada entrada c3-m7..m10, la afirmación tal como está
hoy en ensamblado/cap3/cap3_modulos.html (con sus <cite> en su sitio) y cada literal
localizado en la caché local (página, sección, contexto). Solo lee.

Uso: python3 v4B_extrae.py [id ...]  (sin ids: todo el lote B)
Imprime literales (salida local; no la commitea nadie: el .out queda en diagnostico/,
que está en git → se escribe SIN literales; con --literal los muestra en pantalla).
"""
import html, html.parser, pathlib, re, sys
import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
from audita_citas import normaliza, seccion_de  # noqa: E402

LOTE = re.compile(r"^c3-m(7|8|9|10)-")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
MUESTRA_LITERAL = "--literal" in sys.argv

registro = yaml.safe_load((RAIZ / "bibliografia/contraste/cap3.yml").read_text("utf-8"))
citas = yaml.safe_load((RAIZ / "bibliografia/_local/citas/cap3.yml").read_text("utf-8"))["citas"]
ejemplares = yaml.safe_load((RAIZ / "bibliografia/ejemplares.yml").read_text("utf-8"))
fuente_html = (RAIZ / "ensamblado/cap3/cap3_modulos.html").read_text("utf-8")

VACIOS = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "col", "area", "base"}


class Spans(html.parser.HTMLParser):
    def __init__(self, txt):
        super().__init__(convert_charrefs=False)
        self.txt = txt
        self.off = [0]
        for l in txt.splitlines(keepends=True):
            self.off.append(self.off[-1] + len(l))
        self.pila = []
        self.spans = {}

    def pos(self):
        l, c = self.getpos()
        return self.off[l - 1] + c

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VACIOS:
            return
        self.pila.append((tag, a.get("data-afirma"), self.pos()))

    def handle_endtag(self, tag):
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == tag:
                for t, ida, ini in self.pila[i:]:
                    if ida:
                        fin = self.txt.index(">", self.pos()) + 1
                        self.spans[ida] = (ini, fin)
                del self.pila[i:]
                return


def texto_visible(frag):
    frag = re.sub(r'<cite class="cita"([^>]*)>.*?</cite>',
                  lambda m: " ⟦CITA " + " ".join(re.findall(r'data-(?:ref|loc)="([^"]*)"', m.group(1))) + "⟧",
                  frag, flags=re.S)
    frag = re.sub(r"<script.*?</script>", "", frag, flags=re.S)
    frag = re.sub(r"<[^>]+>", "", frag)
    return re.sub(r"\s+", " ", html.unescape(frag)).strip()


p = Spans(fuente_html)
p.feed(fuente_html)
linea_de = lambda off: fuente_html.count("\n", 0, off) + 1


def busca_pdf(clave, literal):
    base = RAIZ / "bibliografia/_local/texto" / clave
    n = normaliza(literal)
    hits = []
    for f in sorted(base.glob("p*.txt")):
        t = normaliza(f.read_text("utf-8"))
        if n in t:
            hits.append(int(f.stem[1:]))
    # cruce de página
    if not hits:
        fs = sorted(base.glob("p*.txt"))
        for a, b in zip(fs, fs[1:]):
            if n in normaliza(a.read_text("utf-8") + "\n" + b.read_text("utf-8")):
                hits.append(int(a.stem[1:]) + 0.5)
    return hits


def contexto(texto, literal, ancho=350):
    t = normaliza(texto)
    n = normaliza(literal)
    i = t.find(n)
    if i < 0:
        return None
    return t[max(0, i - ancho): i + len(n) + ancho]


def impreso(clave, pag):
    """Número impreso en el encabezado de la página del PDF (si se ve)."""
    f = RAIZ / "bibliografia/_local/texto" / clave / f"p{pag:04d}.txt"
    if not f.is_file():
        return None
    cab = " ".join(f.read_text("utf-8").splitlines()[:4] + f.read_text("utf-8").splitlines()[-3:])
    return re.findall(r"\b\d{1,3}\b", cab)[:6]


for e in registro["afirmaciones"]:
    ident = e["id"]
    if not LOTE.match(ident) or (args and ident not in args):
        continue
    print("=" * 100)
    print(f"{ident} · {e['tipo']} · {e['veredicto']}")
    if ident in p.spans:
        a, b = p.spans[ident]
        print(f"  HTML (cap3_modulos.html:{linea_de(a)}): {texto_visible(fuente_html[a:b])}")
    else:
        print("  HTML: NO ENCONTRADA")
    if e.get("nota"):
        print(f"  NOTA: {e['nota']}")
    if e.get("motivo"):
        print(f"  MOTIVO: {e['motivo']}")
    for k, f in enumerate(e.get("fuentes") or [], 1):
        lit = (citas.get(ident) or {}).get(k)
        cl = f.get("clave")
        print(f"  [{k}] {cl} · {f.get('loc')} · {f.get('clase')} · pdf={f.get('pagina_pdf')} inst={f.get('instantanea')}")
        if lit is None:
            print("      (sin literal)")
            continue
        if MUESTRA_LITERAL:
            print(f"      LIT: {lit}")
        if f.get("clase") == "PDF":
            hits = busca_pdf(cl, str(lit))
            des = (ejemplares.get(cl) or {}).get("desfase")
            pag = f.get("pagina_pdf")
            m = re.search(r"pp?\.\s*(\d+)(?:[–-](\d+))?", f.get("loc") or "")
            esperado = None
            if m and des is not None:
                lo = int(m.group(1)) + des
                hi = int(m.group(2) or m.group(1)) + des
                esperado = (lo, hi)
            marca = ""
            if esperado and hits and not any(esperado[0] <= h <= esperado[1] for h in hits):
                marca = "  <<< FUERA DEL LOCALIZADOR"
            if pag and hits and pag not in hits:
                marca += f"  <<< pagina_pdf {pag} no contiene el literal"
            print(f"      en páginas PDF {hits} (esperado {esperado}; encabezado de {pag}: {impreso(cl, pag) if pag else None}){marca}")
            if MUESTRA_LITERAL and hits:
                h = int(hits[0])
                t = (RAIZ / f"bibliografia/_local/texto/{cl}/p{h:04d}.txt").read_text("utf-8")
                nx = RAIZ / f"bibliografia/_local/texto/{cl}/p{h+1:04d}.txt"
                if nx.is_file():
                    t += "\n" + nx.read_text("utf-8")
                print(f"      CTX: {contexto(t, str(lit))}")
        else:
            ruta = RAIZ / "bibliografia/_local/web" / cl / f"{f.get('instantanea')}.txt"
            t = ruta.read_text("utf-8")
            sec, falta = seccion_de(t, f.get("loc") or "")
            dentro = normaliza(str(lit)) in normaliza(sec)
            entero = normaliza(str(lit)) in normaliza(t)
            print(f"      en sección: {dentro} · en la instantánea: {entero}{'  <<< FUERA DE SECCIÓN' if entero and not dentro else ''}")
            if MUESTRA_LITERAL:
                print(f"      CTX: {contexto(sec if dentro else t, str(lit))}")
