#!/usr/bin/env python3
"""
r4_marca.py — ronda R4 (fuentes) del capítulo 4: las marcas, las citas y las listas

Parte SIEMPRE de las seis plantillas de `ensamblado/cap4/` tal como estaban en
el commit BASE (antes de la R4; ver r4_lib.py), tratadas como un solo texto, y
les aplica, en este orden:

  1. los cambios de prosa de `r4_marcas.json`: frases que la fuente leída no
     sostenía (y cuatro comentarios de bloques de código que afirmaban algo
     falso o atribuían sin fuente);
  2. las marcas `data-afirma` y los `<cite class="cita">` vacíos del mismo
     archivo (notación en r4_lib.py);
  3. la lista de fuentes de cada módulo que cita algo, al final de su
     plantilla, y la lista del capítulo, tras las lecturas del Módulo 10;
  4. `genera_referencias.genera()`, que escribe el texto de citas y listas.

Escribe la FUENTE DE ENSAMBLADO (las seis plantillas), no el HTML final:
después hay que correr `python3 ensamblado/ensambla_cap4.py` (y los del 5 y el
6). El CSS de las citas y el pie no se tocan aquí: llegan del armazón del
capítulo 2 por el 3. `ensamblado/cap4/chapter.js` (quiz, simulacro,
simuladores) no se toca en esta ronda.

Es reejecutable: como parte de BASE y no de los archivos de trabajo, correrlo
dos veces da el mismo resultado. Cada texto exige aparecer exactamente una vez
en el conjunto de las plantillas; si no, aborta sin escribir. `r4_marcas.json`
lo escribe `bibliografia/_local/herramientas/cap4/r4_reune.py` (fuera de git,
porque junto a las marcas guarda las citas literales).

Uso:  python3 diagnostico/cap4/comprobaciones/r4_marca.py [--comprobar]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

import genera_referencias  # noqa: E402  (r4_lib ya puso precalculo/ en la ruta)

AQUI = pathlib.Path(__file__).resolve().parent

ASIDE = ('      <aside class="fuentes-modulo" aria-label="Fuentes citadas en este módulo">\n'
         "        <h4>Fuentes citadas en este módulo</h4>\n"
         "        <!--FUENTES-MODULO:inicio-->\n        <!--FUENTES-MODULO:fin-->\n      </aside>\n")
FIN_MODULO = "    </div>\n  "
LISTA_CAPITULO = ('      <h3><i class="fas fa-quote-right mr-2" aria-hidden="true"></i>'
                  "Referencias citadas en este capítulo</h3>\n"
                  "      <!--REFERENCIAS-CAPITULO:inicio-->\n      <!--REFERENCIAS-CAPITULO:fin-->\n")


def main() -> int:
    tabla = json.loads((AQUI / "r4_marcas.json").read_text("utf-8"))
    html = L.base()
    try:
        for e in tabla:
            for viejo, nuevo, motivo in e["prosa"]:
                html = L.aplica(html, viejo, nuevo, f"{e['id']} · prosa")
        for e in tabla:
            for n, marca in enumerate(e["marcas"], start=1):
                html = L.aplica(html, None, marca, f"{e['id']} · marca {n}")
    except L.Aborta as x:
        sys.exit(f"ABORTA {x}")

    # 3a — la lista de cada módulo que cita algo, al final de su plantilla
    def con_aside(m):
        cuerpo = m.group("cuerpo")
        if "data-ref=" not in cuerpo:
            return m.group(0)
        if not cuerpo.endswith(FIN_MODULO):
            sys.exit(f"ABORTA [aside]: el módulo {m.group('n')} no acaba como se esperaba")
        return m.group("abre") + cuerpo[:-len(FIN_MODULO)] + ASIDE + FIN_MODULO + m.group("cierra")

    html = genera_referencias.RE_MODULO.sub(con_aside, html)

    # 3b — la lista del capítulo, tras el recuadro de lecturas del Módulo 10
    ancla = '      <div class="note">\n        <p><strong>Y en el Capítulo 5…</strong>'
    if html.count(ancla) != 1:
        sys.exit(f"ABORTA [lista del capítulo]: el ancla aparece {html.count(ancla)} veces")
    k = html.index(ancla)
    if not html[:k].endswith("        </ul>\n      </div>\n\n"):
        sys.exit("ABORTA [lista del capítulo]: antes del ancla no está el cierre del recuadro de lecturas")
    html = html[:k] + LISTA_CAPITULO + "\n" + html[k:]

    # 4 — el generador escribe citas y listas
    biblioteca, candado = genera_referencias.carga_biblioteca()
    html = genera_referencias.genera(html, biblioteca, candado)

    partes = L.parte(html)
    n_prosa = sum(len(e["prosa"]) for e in tabla)
    resumen = (f"{L.DIR_FUENTE}/templates_*.html: {n_prosa} cambios de prosa, {len(tabla)} afirmaciones "
               f"({html.count('data-afirma=')} marcas en el HTML), {html.count('<cite class=')} citas, "
               f"{html.count('<aside class=')} listas de módulo")
    if "--comprobar" in sys.argv:
        difieren = [n for n, t in partes.items() if (L.RAIZ / L.DIR_FUENTE / n).read_text("utf-8") != t]
        print(("OK" if not difieren else "DIFIERE (" + ", ".join(difieren) + ")") + f"  {resumen}")
        return 1 if difieren else 0
    for n, t in partes.items():
        (L.RAIZ / L.DIR_FUENTE / n).write_text(t, "utf-8")
    print(f"OK  {resumen}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
