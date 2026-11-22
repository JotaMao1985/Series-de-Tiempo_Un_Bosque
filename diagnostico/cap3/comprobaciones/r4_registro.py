#!/usr/bin/env python3
"""
r4_registro.py — ronda R4 (fuentes) del capítulo 3: el registro de contraste

Escribe `bibliografia/contraste/cap3.yml` (en git: huella y número de palabras
de cada cita) y `bibliografia/_local/citas/cap3.yml` (fuera de git: los
literales) a partir de `bibliografia/_local/herramientas/cap3/r4_entradas.json`,
que es donde están las entradas con su cita literal (fuera de git; lo escribe
`r4_reune.py`, en esa misma carpeta).

Antes de escribir comprueba cada cita contra la caché con las funciones del
auditor (F04, F05, F06, F07, F11): está en la página o en la sección de su
localizador, tiene 25 palabras como mucho y el número impreso es el de esa
página. Si algo no está, no escribe. La huella de la prosa (`hash_texto`) sale
del HTML ensamblado, que tiene que estar al día (`r4_marca.py` y
`ensambla_cap3.py --escribir` antes).

Conserva el `verificado_por` que el verificador haya puesto solo si no cambian
la prosa (huella), el veredicto, las fuentes ni la nota de la entrada; si cambia
algo, la firma se retira y se lista, para que la vuelva a mirar quien no redactó. `redactado_por` es el redactor; `verificado_por`
no lo pone este guion nunca.

Uso:  python3 diagnostico/cap3/comprobaciones/r4_registro.py [--tolera-f07 CLAVE]
      (--tolera-f07: escribe aunque la ficha del ejemplar de esa obra no pase
      F07; el auditor lo seguirá diciendo)
"""
import json
import pathlib
import re
import sys
import textwrap

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

A = L.A
ENTRADAS = L.RAIZ / "bibliografia" / "_local" / "herramientas" / "cap3" / "r4_entradas.json"
REGISTRO = L.RAIZ / "bibliografia" / "contraste" / "cap3.yml"
LOCAL = L.RAIZ / "bibliografia" / "_local" / "citas" / "cap3.yml"
HTML = L.RAIZ / "Htmls_Series" / "capitulo-3-modelos-ar-ma-arma.html"
REDACTOR = "subagente redactor de la ronda R4 del capítulo 3 (Fable 5.2)"
FECHA = "2026-11-21"

CABECERA = """\
# Registro de contraste · Capítulo 3 · Modelos AR, MA y ARMA
#
# Cada entrada une una afirmación del capítulo (el elemento con ese
# `data-afirma`) con el pasaje LEÍDO que la respalda. La cita literal vive
# fuera de git, en `bibliografia/_local/citas/cap3.yml`; aquí quedan su huella
# (`cita_sha256`, del literal normalizado) y su número de palabras, y
# `precalculo/audita_citas.py` busca el literal en el texto de la fuente, en la
# sección o página que dice `loc`. Quien verifica no es quien redactó.
#
# Ronda R4 «fuentes» (2026-11-21). Este archivo lo escribe
# `diagnostico/cap3/comprobaciones/r4_registro.py` a partir de las entradas de
# `bibliografia/_local/herramientas/cap3/r4_entradas.json`: cinco lectores
# leyeron cada pasaje en la caché local (FPP3, Cryer y Chan, Hamilton, Yule,
# Hyndman y Khandakar, la ayuda de R y, solo como fuente adicional, la 3.ª
# edición de Shumway y Stoffer), copiaron de ahí la cita y el guion la comprobó
# antes de escribir. Los veredictos son la PROPUESTA del redactor: ninguna
# entrada lleva `verificado_por` hasta que la firme un verificador que no
# redactó. Las citas de Hamilton y de Yule reproducen las erratas de su escaneo.
#
# Lo que NO se pudo contrastar queda `pendiente` con su motivo. Lo que el
# capítulo dice del software (forecast, statsmodels, numpy) o calcula por
# simulación, y ninguna obra leída respalda, es `propia`: se comprobó
# ejecutando, en `diagnostico/cap3/comprobaciones/r4_software.*`.
"""
CABECERA_LOCAL = """\
# Literales de las citas del registro de contraste del capítulo 3
# (bibliografia/contraste/cap3.yml). FUERA DE GIT: el repo es público y solo
# guarda la huella de cada literal (`cita_sha256`) y su número de palabras.
# Clave: id de la afirmación → posición de la fuente en su lista (1, 2…).
# Lo escribe diagnostico/cap3/comprobaciones/r4_registro.py (con el formato de
# precalculo/migra_citas_fuera.py); lo lee precalculo/audita_citas.py (F05, F11).
# No se regenera desde ninguna parte que esté en git: es dato primario, y hay
# que copiarlo a cada copia de trabajo que audite el registro.
"""


def q(texto: str) -> str:
    return json.dumps(str(texto), ensure_ascii=False)


def plegado(campo: str, texto: str) -> str:
    lineas = textwrap.wrap(" ".join(texto.split()), width=108, break_long_words=False, break_on_hyphens=False)
    return f"  {campo}: >-\n" + "".join(f"    {l}\n" for l in lineas)


def limpia_software(t: str) -> str:
    t = re.sub(r"/private/tmp/\S*?/scratchpad/lector[A-E]/(\w+)\.(R|py)",
               r"diagnostico/cap3/comprobaciones/r4_software.\2 (bloque «\1»)", t)
    return t


def main() -> int:
    tolera = set()
    if "--tolera-f07" in sys.argv:
        tolera.add(sys.argv[sys.argv.index("--tolera-f07") + 1])
    dato = json.loads(ENTRADAS.read_text("utf-8"))
    por_id = {e["id"]: e for e in dato["entradas"]}
    lector = A.lee_html(HTML.read_text("utf-8"))
    fallos = [f"{i}: sin `data-afirma` en el HTML" for i in por_id if i not in lector.afirmaciones]
    fallos += [f"{i}: marcada en el HTML y sin entrada" for i in lector.afirmaciones if i not in por_id]
    previo = {}
    if REGISTRO.exists():
        previo = {e["id"]: e for e in (yaml.safe_load(REGISTRO.read_text("utf-8")) or {}).get("afirmaciones") or []}

    for ident, e in por_id.items():
        for n, f in enumerate(e.get("fuentes") or [], start=1):
            for x in L.comprueba_fuente(f, f"{ident} · fuente {n}"):
                if "[F07]" in x and f["clave"] in tolera and "la portada dice" in x:
                    continue
                fallos.append(x)
        for campo in ("afirmacion", "nota", "motivo"):
            for f in e.get("fuentes") or []:
                if len(f["cita"].split()) >= 4 and A.normaliza(f["cita"]) in A.normaliza(e.get(campo) or ""):
                    fallos.append(f"{ident}: `{campo}` repite el literal de una cita")
    if fallos:
        print("\n".join("FALLA  " + x for x in fallos))
        print(f"No se ha escrito nada: {len(fallos)} fallos")
        return 1

    orden = [i for i in lector.afirmaciones if i in por_id]        # el del documento
    salida, local, firmas = [CABECERA, "capitulo: 3\n", f"archivo: Htmls_Series/{HTML.name}\n", "afirmaciones:\n"], [], 0
    n_citas = 0
    caidas, sin_firma_cambian = [], []
    for ident in orden:
        e = por_id[ident]
        hash_texto = A.huella(lector.afirmaciones[ident].texto)
        s = [f"\n- id: {ident}\n", f"  tipo: {e['tipo']}\n", f"  afirmacion: {q(e['afirmacion'])}\n",
             f"  hash_texto: {q(hash_texto)}\n", f"  veredicto: {e['veredicto']}\n"]
        if e.get("fuentes"):
            s.append("  fuentes:\n")
            local.append(f"  {ident}:\n")
            for n, f in enumerate(e["fuentes"], start=1):
                s.append(f"  - clave: {f['clave']}\n    loc: {q(f['loc'])}\n    clase: {f['clase']}\n")
                s.append(f"    pagina_pdf: {f['pagina_pdf']}\n" if f["clase"] == "PDF"
                         else f"    instantanea: {f['instantanea']}\n")
                s.append(f"    cita_sha256: {q(A.huella_cita(f['cita']))}\n"
                         f"    cita_palabras: {A.palabras_cita(f['cita'])}\n")
                local.append(f"    {n}: {q(f['cita'])}\n")
                n_citas += 1
        nota = e.get("nota") or ""
        if e.get("software"):
            nota = (nota + " Comprobación: " + limpia_software(e["software"])).strip()
        if nota:
            s.append(plegado("nota", nota))
        if e.get("motivo"):
            s.append(plegado("motivo", e["motivo"]))
        s.append(f"  redactado_por: {REDACTOR}\n")
        ant = previo.get(ident) or {}
        firma = ant.get("verificado_por")
        if firma:
            # La firma vale para lo que el verificador leyó: se conserva solo si no cambian la
            # prosa, el veredicto, las fuentes (obra, localizador y cita) ni la nota.
            fuentes_ant = [(f["clave"], str(f["loc"]), f["cita_sha256"]) for f in ant.get("fuentes") or []]
            fuentes_hoy = [(f["clave"], f["loc"], A.huella_cita(f["cita"])) for f in e.get("fuentes") or []]
            cambia = [que for que, distinto in (
                ("prosa", ant.get("hash_texto") != hash_texto), ("veredicto", ant.get("veredicto") != e["veredicto"]),
                ("fuentes", fuentes_ant != fuentes_hoy),
                ("nota", " ".join(str(ant.get("nota") or "").split()) != " ".join(nota.split())),
                ("motivo", " ".join(str(ant.get("motivo") or "").split()) != " ".join((e.get("motivo") or "").split())),
            ) if distinto]
            if cambia:
                caidas.append(f"{ident}: {', '.join(cambia)}")
            else:
                s.append(f"  verificado_por: {q(firma)}\n")
                firmas += 1
        elif ant and ant.get("hash_texto") != hash_texto:
            sin_firma_cambian.append(ident)
        s.append(f"  fecha: {FECHA}\n")
        salida += s
    texto = "".join(salida)
    relee = yaml.safe_load(texto)
    assert [x["id"] for x in relee["afirmaciones"]] == orden
    for x in relee["afirmaciones"]:                      # el YAML dice lo que las entradas
        e = por_id[x["id"]]
        assert x["afirmacion"] == e["afirmacion"], x["id"]
        assert not any("cita" in f for f in x.get("fuentes") or []), x["id"]
    texto_local = CABECERA_LOCAL + "capitulo: 3\ncitas:\n" + "".join(local)
    relee_local = yaml.safe_load(texto_local)["citas"]
    for ident, e in por_id.items():
        for n, f in enumerate(e.get("fuentes") or [], start=1):
            assert relee_local[ident][n] == f["cita"], (ident, n)
    REGISTRO.write_text(texto, "utf-8")
    LOCAL.parent.mkdir(parents=True, exist_ok=True)
    LOCAL.write_text(texto_local, "utf-8")
    cuenta = {}
    for e in por_id.values():
        cuenta[e["veredicto"]] = cuenta.get(e["veredicto"], 0) + 1
    print(f"OK  {REGISTRO.relative_to(L.RAIZ)}: {len(orden)} entradas ({cuenta}), {n_citas} citas literales "
          f"comprobadas contra la caché; {firmas} firmas conservadas")
    if caidas:
        print(f"Firmas retiradas ({len(caidas)}), porque cambió lo que se firmó:")
        for x in caidas:
            print(f"  {x}")
    if sin_firma_cambian:
        print(f"Sin firma y con la prosa cambiada: {', '.join(sin_firma_cambian)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
