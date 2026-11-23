#!/usr/bin/env python3
"""
r4_comprueba_propuesta.py — comprueba una propuesta de marcas y citas (JSON)

Uso:  python3 diagnostico/cap4/comprobaciones/r4_comprueba_propuesta.py [--texto] propuesta.json [otra.json …]
      (--texto imprime además el texto que queda dentro de cada marca)

Aplica en memoria, sobre las plantillas del capítulo 4 en BASE, los cambios de
prosa y las marcas de la propuesta, y comprueba lo mismo que comprobará el
auditor: cada texto aparece una sola vez, ninguna marca anidada ni repetida,
cada cita visible dentro de una afirmación citable y con una fuente de esa
entrada que coincide en clave y localizador, y cada cita literal está en la
caché en su localizador, con 25 palabras como mucho. No escribe nada.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

A = L.A
CAMPOS = {"id", "tipo", "afirmacion", "veredicto", "marcas", "prosa", "fuentes", "nota", "motivo",
          "inventario", "software"}


def main() -> int:
    entradas, fallos = [], []
    for ruta in [a for a in sys.argv[1:] if not a.startswith("--")]:
        dato = json.loads(pathlib.Path(ruta).read_text("utf-8"))
        entradas += dato["entradas"]
    html = L.base()
    ids = [e.get("id") for e in entradas]
    for i in set(ids):
        if ids.count(i) > 1:
            fallos.append(f"{i}: id repetido")
    for e in entradas:
        ident = e.get("id", "¿sin id?")
        if set(e) - CAMPOS:
            fallos.append(f"{ident}: campos desconocidos {sorted(set(e) - CAMPOS)}")
        if not A.RE_ID.match(ident) or not ident.startswith("c4-"):
            fallos.append(f"{ident}: id mal formado")
        if e.get("tipo") not in A.TIPOS:
            fallos.append(f"{ident}: tipo {e.get('tipo')!r}")
        if e.get("veredicto") not in ("respaldada", "con-matiz", "propia", "pendiente"):
            fallos.append(f"{ident}: veredicto {e.get('veredicto')!r}")
        if not e.get("afirmacion"):
            fallos.append(f"{ident}: falta `afirmacion`")
        if e.get("veredicto") == "pendiente" and not e.get("motivo"):
            fallos.append(f"{ident}: pendiente sin `motivo`")
        if e.get("veredicto") in A.CITABLES and not e.get("fuentes"):
            fallos.append(f"{ident}: {e.get('veredicto')} sin fuentes")
        if e.get("veredicto") in ("con-matiz", "propia") and not e.get("nota"):
            fallos.append(f"{ident}: {e.get('veredicto')} sin `nota`")
        for viejo, nuevo, motivo in e.get("prosa") or []:
            try:
                html = L.aplica(html, viejo, nuevo, f"{ident} · prosa")
            except L.Aborta as x:
                fallos.append(str(x))
    for e in entradas:
        ident = e.get("id", "¿sin id?")
        if not e.get("marcas"):
            fallos.append(f"{ident}: sin `marcas`")
        for n, marca in enumerate(e.get("marcas") or [], start=1):
            try:
                html = L.aplica(html, None, marca, f"{ident} · marca {n}")
            except L.Aborta as x:
                fallos.append(str(x))
        for n, f in enumerate(e.get("fuentes") or [], start=1):
            fallos += L.comprueba_fuente(f, f"{ident} · fuente {n}")
    lector = A.lee_html(html)
    por_id = {e.get("id"): e for e in entradas}
    for linea, que in lector.problemas:
        fallos.append(f"línea {linea}: {que}")
    for ident in por_id:
        if ident not in lector.afirmaciones:
            fallos.append(f"{ident}: ninguna marca pone su `data-afirma`")
    for c in lector.citas:
        e = por_id.get(c.afirma)
        if not e:
            fallos.append(f"línea {c.linea}: la cita de {c.clave} ({c.loc}) no está dentro de una afirmación de la propuesta")
            continue
        if e.get("veredicto") not in A.CITABLES:
            fallos.append(f"{c.afirma}: cita visible con veredicto {e.get('veredicto')}")
        if not any(f.get("clave") == c.clave and f.get("loc") == c.loc for f in e.get("fuentes") or []):
            fallos.append(f"{c.afirma}: la cita visible ({c.clave}, «{c.loc}») no coincide con ninguna fuente de la entrada")
        if c.clave == "shumway2011time":
            fallos.append(f"{c.afirma}: Shumway y Stoffer 3.ª no se cita a la vista (no es la edición del curso)")
    avisos = [f"{i}: {e['veredicto']} sin cita visible" for i, e in por_id.items()
              if e.get("veredicto") in A.CITABLES and not any(c.afirma == i for c in lector.citas)]
    for a in avisos:
        print("AVISO ", a)
    for f in fallos:
        print("FALLA ", f)
    n_citas = sum(len(e.get("fuentes") or []) for e in entradas)
    print(f"{'FALLA' if fallos else 'OK'}: {len(entradas)} entradas, {len(lector.citas)} citas visibles, "
          f"{n_citas} citas literales; {len(fallos)} fallos, {len(avisos)} avisos")
    for ident in por_id:
        a = lector.afirmaciones.get(ident)
        if a and "--texto" in sys.argv:
            print(f"   {ident}: {A.normaliza(a.texto)[:300]}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
