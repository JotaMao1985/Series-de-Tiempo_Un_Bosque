#!/usr/bin/env python3
"""
r4_marca.py — ronda R4 (fuentes) del capítulo 3: las marcas, las citas y las listas

Parte SIEMPRE de `ensamblado/cap3/cap3_modulos.html` tal como estaba en el
commit BASE (antes de la R4; ver r4_lib.py) y le aplica, en este orden:

  1. los cambios de prosa de `r4_marcas.json`: frases que la fuente leída no
     sostenía;
  2. las marcas `data-afirma` y los `<cite class="cita">` vacíos del mismo
     archivo (notación en r4_lib.py);
  3. la lista de fuentes de cada módulo que cita algo, al final de su
     plantilla, y la lista del capítulo, tras las lecturas del Módulo 10;
  4. `genera_referencias.genera()`, que escribe el texto de citas y listas;
  5. (segunda pasada) tres cadenas visibles de `ensamblado/cap3/cap3_js.js`,
     también desde BASE (tabla CADENAS_JS).

Escribe la FUENTE DE ENSAMBLADO, no el HTML final: después hay que correr
`python3 ensamblado/ensambla_cap3.py --escribir`. El CSS de las citas y el pie
no se tocan aquí: llegan del armazón del capítulo 2.

Es reejecutable: como parte de BASE y no del archivo de trabajo, correrlo dos
veces da el mismo resultado. Cada texto exige aparecer exactamente una vez; si
no, aborta sin escribir. `r4_marcas.json` lo escribe
`bibliografia/_local/herramientas/cap3/r4_reune.py` (fuera de git, porque junto
a las marcas guarda las citas literales).

Uso:  python3 diagnostico/cap3/comprobaciones/r4_marca.py [--comprobar]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

import genera_referencias  # noqa: E402  (r4_lib ya puso precalculo/ en la ruta)

AQUI = pathlib.Path(__file__).resolve().parent
DESTINO = L.RAIZ / L.FUENTE

# Segunda pasada: tres cadenas visibles de `cap3_js.js` (el pie de la tabla ordenable del M8 y dos rótulos
# de simulador). Se aplican sobre el archivo de BASE, cada una exactamente una vez. El quiz, la práctica de
# repaso y el simulacro no se tocan.
JS = "ensamblado/cap3/cap3_js.js"
CADENAS_JS = [
    ("pie: 'El AR($2$) de Yule —la fila marcada— no es el mínimo",
     "pie: 'El AR($2$) —la fila marcada, el que proponía la identificación— no es el mínimo",
     "Yule ajustó su regresión a 1749–1924, no a esta ventana (c3-m7-02)"),
    ("'Manchas solares (número de Wolf)'", "'Manchas solares (número anual)'",
     "ninguna obra leída dice «Wolf» (Yule escribe «Wolfer»; la ayuda de R, «Yearly numbers of sunspots»)"),
    ("valor: 'original (número de Wolf)'", "valor: 'original (número anual)'", "lo mismo"),
]

ASIDE = ('      <aside class="fuentes-modulo" aria-label="Fuentes citadas en este módulo">\n'
         "        <h4>Fuentes citadas en este módulo</h4>\n"
         "        <!--FUENTES-MODULO:inicio-->\n        <!--FUENTES-MODULO:fin-->\n      </aside>\n")
FIN_MODULO = "    </div>\n  "
LISTA_CAPITULO = ('\n      <h3><i class="fas fa-quote-right mr-2" aria-hidden="true"></i>'
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
    ancla = "      <h3>Práctica de repaso · capítulo 2 y módulos 3.1–3.4</h3>\n"
    if html.count(ancla) != 1:
        sys.exit(f"ABORTA [lista del capítulo]: el ancla aparece {html.count(ancla)} veces")
    k = html.index(ancla)
    if not html[:k].endswith("      </div>\n\n"):
        sys.exit("ABORTA [lista del capítulo]: antes del ancla no está el cierre del recuadro de lecturas")
    html = html[:k] + LISTA_CAPITULO.lstrip("\n") + "\n" + html[k:]

    # 4 — el generador escribe citas y listas
    biblioteca, candado = genera_referencias.carga_biblioteca()
    html = genera_referencias.genera(html, biblioteca, candado)

    # 5 — las tres cadenas del JavaScript
    import subprocess
    js = subprocess.run(["git", "show", f"{L.BASE}:{JS}"], cwd=L.RAIZ, capture_output=True,
                        check=True).stdout.decode("utf-8")
    for viejo, nuevo, _ in CADENAS_JS:
        if js.count(viejo) != 1:
            sys.exit(f"ABORTA [JS]: aparece {js.count(viejo)} veces, se esperaba 1\n   {viejo}")
        js = js.replace(viejo, nuevo)

    n_prosa = sum(len(e["prosa"]) for e in tabla)
    resumen = (f"{L.FUENTE}: {n_prosa} cambios de prosa, {len(tabla)} afirmaciones "
               f"({html.count('data-afirma=')} marcas en el HTML), {html.count('<cite class=')} citas, "
               f"{html.count('<aside class=')} listas de módulo; {len(CADENAS_JS)} cadenas de {JS}")
    if "--comprobar" in sys.argv:
        igual = DESTINO.read_text("utf-8") == html and (L.RAIZ / JS).read_text("utf-8") == js
        print(("OK" if igual else "DIFIERE") + f"  {resumen}")
        return 0 if igual else 1
    DESTINO.write_text(html, "utf-8")
    (L.RAIZ / JS).write_text(js, "utf-8")
    print(f"OK  {resumen}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
