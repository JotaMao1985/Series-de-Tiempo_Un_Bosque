#!/usr/bin/env python3
"""R3 del capítulo 4 · reaplica sobre HEAD las ediciones de la ronda de estructura.

Una lista de sustituciones por módulo (`r3_ediciones_m1.py` … `r3_ediciones_m10.py`, más
`r3_ediciones_minutos.py`), cada una con el texto que sale y el que entra, literales. Cada
sustitución debe aparecer exactamente una vez en el archivo de partida; los traslados (`mover`)
llevan un bloque [inicio, fin) delante de un marcador, y los tres marcadores también deben ser
únicos. `entre()` sustituye de un marcador a otro (se usa solo para bloques enteros; lo que sale
queda en el commit base). El código va sin escapar en las listas y pasa por `esc()` (html.escape
sin comillas), que es como vive dentro de los `<pre>` de las plantillas.

Archivos que toca:
  ensamblado/cap4/templates_1_3.html   módulos 1 a 3
  ensamblado/cap4/templates_4_6.html   módulos 4 a 6
  ensamblado/cap4/templates_7_9.html   módulos 7 a 9
  ensamblado/cap4/templates_10.html    módulo 10
  ensamblado/ensambla_cap4.py          solo `courseData`: los minutos medidos

No toca el armazón, la plantilla, `chapter.js` ni los módulos 11 y 12. Es reejecutable: siempre
parte del commit base (por defecto HEAD), no del archivo de trabajo.

Uso (desde la raíz del repo):
    python3 diagnostico/cap4/comprobaciones/r3_edita.py              # escribe
    python3 diagnostico/cap4/comprobaciones/r3_edita.py --comprobar  # solo compara
    python3 diagnostico/cap4/comprobaciones/r3_edita.py --base 531b907

Después, en este orden:
    python3 ensamblado/ensambla_cap4.py
    python3 ensamblado/ensambla_cap5.py
    python3 ensamblado/ensambla_cap6.py
y `git diff --stat` debe mostrar los capítulos 5 y 6 sin cambios.
"""
import html
import importlib
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI))

T13 = "ensamblado/cap4/templates_1_3.html"
T46 = "ensamblado/cap4/templates_4_6.html"
T79 = "ensamblado/cap4/templates_7_9.html"
T10 = "ensamblado/cap4/templates_10.html"
ENS = "ensamblado/ensambla_cap4.py"

C = []      # (clave, archivo, antes, después)
MOVER = []  # (clave, archivo, inicio, fin, destino): el bloque [inicio, fin) pasa a ir antes de `destino`


def c(clave, archivo, antes, despues):
    C.append((clave, archivo, antes, despues))


def mover(clave, archivo, inicio, fin, destino):
    MOVER.append((clave, archivo, inicio, fin, destino))


def entre(clave, archivo, inicio, fin, despues):
    """Sustituye todo lo que hay desde `inicio` (incluido) hasta `fin` (excluido) por `despues`.
    Se usa solo para bloques de código enteros; lo que sale queda en el commit base."""
    C.append((clave, archivo, ("__ENTRE__", inicio, fin), despues))


def esc(codigo):
    """El código de un <pre> de las plantillas vive con `<`, `>` y `&` escapados (las comillas, no)."""
    return html.escape(codigo, quote=False)


LISTAS = ["r3_ediciones_m1", "r3_ediciones_m2", "r3_ediciones_m3", "r3_ediciones_m4",
          "r3_ediciones_m5", "r3_ediciones_m6", "r3_ediciones_m7", "r3_ediciones_m8",
          "r3_ediciones_m9", "r3_ediciones_m10", "r3_ediciones_minutos"]
for nombre in LISTAS:
    if (AQUI / (nombre + ".py")).exists():
        importlib.import_module(nombre).registra(c, mover, entre=entre, esc=esc, T13=T13, T46=T46,
                                                 T79=T79, T10=T10, ENS=ENS)


def base(archivo, rev):
    return subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def main():
    rev = "HEAD"
    if "--base" in sys.argv:
        rev = sys.argv[sys.argv.index("--base") + 1]
    comprobar = "--comprobar" in sys.argv
    archivos = sorted({x[1] for x in C} | {x[1] for x in MOVER})
    textos = {a: base(a, rev) for a in archivos}
    fallos = 0
    for clave, archivo, antes, despues in C:
        if isinstance(antes, tuple):
            _, inicio, fin = antes
            t = textos[archivo]
            cuenta = [t.count(inicio), t.count(fin)]
            if cuenta != [1, 1] or not t.index(inicio) < t.index(fin):
                print(f"FALLA · {clave}: los marcadores aparecen {cuenta} veces en {archivo} (se esperaba 1, 1, en orden)")
                fallos += 1
                continue
            i, j = t.index(inicio), t.index(fin)
            print(f"  · {clave}: salen {t[i:j].count(chr(10))} líneas")
            textos[archivo] = t[:i] + despues + t[j:]
            continue
        n = textos[archivo].count(antes)
        if n != 1:
            print(f"FALLA · {clave}: el texto original aparece {n} veces en {archivo} (se esperaba 1)")
            fallos += 1
            continue
        textos[archivo] = textos[archivo].replace(antes, despues)
    for clave, archivo, inicio, fin, destino in MOVER:
        t = textos[archivo]
        cuenta = [t.count(m) for m in (inicio, fin, destino)]
        if cuenta != [1, 1, 1]:
            print(f"FALLA · {clave}: los marcadores aparecen {cuenta} veces en {archivo} (se esperaba 1, 1, 1)")
            fallos += 1
            continue
        i, j = t.index(inicio), t.index(fin)
        if not i < j:
            print(f"FALLA · {clave}: los marcadores están en orden inverso")
            fallos += 1
            continue
        bloque = t[i:j]
        t = t[:i] + t[j:]
        k = t.index(destino)
        textos[archivo] = t[:k] + bloque + t[k:]
    if fallos:
        sys.exit(f"{fallos} sustituciones no aplicadas; no se escribe nada")
    for archivo, texto in textos.items():
        ruta = RAIZ / archivo
        if comprobar:
            igual = ruta.read_text(encoding="utf-8") == texto
            print(f"{archivo}: {'idéntico a ' + rev + ' + ediciones' if igual else 'DIFIERE de ' + rev + ' + ediciones'}")
            fallos += 0 if igual else 1
        else:
            ruta.write_text(texto, encoding="utf-8")
    print(f"{len(C)} sustituciones y {len(MOVER)} traslados sobre {rev}: "
          + ", ".join(f"{sum(1 for x in C if x[1] == a) + sum(1 for x in MOVER if x[1] == a)} en {a.split('/')[-1]}"
                      for a in archivos))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
