#!/usr/bin/env python3
"""R3 del capítulo 5 · reaplica sobre HEAD las ediciones de la ronda de estructura.

Copia del `r3_edita.py` del capítulo 4, con los archivos del 5. Una lista de sustituciones por
módulo (`r3_ediciones_m1.py`, `_m2`, `_m3`, `_m4_6`, `_m7_9`, `_m10_11`, más `r3_ediciones_minutos.py`), cada una con
el texto que sale y el que entra, literales. Cada sustitución debe aparecer exactamente una vez en
el archivo de partida; los traslados (`mover`) llevan un bloque [inicio, fin) delante de un
marcador, y los tres marcadores también deben ser únicos. `entre()` sustituye de un marcador a
otro. `despues()` registra una sustitución que se aplica DESPUÉS de los traslados (para coser el
bloque trasladado con lo que queda a su alrededor). El código va sin escapar en las listas y pasa
por `esc()` (html.escape sin comillas), que es como vive dentro de los `<pre>` de las plantillas.

Archivos que toca:
  ensamblado/cap5/templates_1_3.html     módulos 1 a 3
  ensamblado/cap5/templates_4_6.html     módulos 4 a 6
  ensamblado/cap5/templates_7_9.html     módulos 7 a 9
  ensamblado/cap5/templates_10_11.html   módulos 10 y 11
  ensamblado/cap5/chapter.js             el simulador y la tabla ordenable del M11 (nada del quiz)
  ensamblado/ensambla_cap5.py            el ciclo (una glosa) y `courseData` (los minutos medidos)
  precalculo/genera_cap5.R               las métricas del M11, también sin redondear (campo `exactas`)

No toca el armazón, la plantilla, `simulacro.js`, el M12, el quiz ni los enunciados y soluciones
de los ejercicios. Es reejecutable: siempre parte del commit base (por defecto HEAD), no del
archivo de trabajo.

Uso (desde la raíz del repo):
    python3 diagnostico/cap5/comprobaciones/r3_edita.py              # escribe
    python3 diagnostico/cap5/comprobaciones/r3_edita.py --comprobar  # solo compara
    python3 diagnostico/cap5/comprobaciones/r3_edita.py --base ad84aa7

Después, en este orden:
    python3 ensamblado/ensambla_cap5.py
    python3 ensamblado/ensambla_cap6.py
y `git status` debe mostrar el capítulo 6 sin cambios.
"""
import html
import importlib
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI))

T13 = "ensamblado/cap5/templates_1_3.html"
T46 = "ensamblado/cap5/templates_4_6.html"
T79 = "ensamblado/cap5/templates_7_9.html"
T1011 = "ensamblado/cap5/templates_10_11.html"
CJS = "ensamblado/cap5/chapter.js"
ENS = "ensamblado/ensambla_cap5.py"

C = []      # (clave, archivo, antes, después)
MOVER = []  # (clave, archivo, inicio, fin, destino): el bloque [inicio, fin) pasa a ir antes de `destino`
POST = []   # (clave, archivo, antes, después): como C, pero después de los traslados


def c(clave, archivo, antes, despues):
    C.append((clave, archivo, antes, despues))


def mover(clave, archivo, inicio, fin, destino):
    MOVER.append((clave, archivo, inicio, fin, destino))


def despues(clave, archivo, antes, nuevo):
    POST.append((clave, archivo, antes, nuevo))


def entre(clave, archivo, inicio, fin, nuevo):
    """Sustituye todo lo que hay desde `inicio` (incluido) hasta `fin` (excluido) por `nuevo`."""
    C.append((clave, archivo, ("__ENTRE__", inicio, fin), nuevo))


def esc(codigo):
    """El código de un <pre> de las plantillas vive con `<`, `>` y `&` escapados (las comillas, no)."""
    return html.escape(codigo, quote=False)


LISTAS = ["r3_ediciones_m1", "r3_ediciones_m2", "r3_ediciones_m3", "r3_ediciones_m4_6",
          "r3_ediciones_m7_9", "r3_ediciones_m10_11", "r3_ediciones_voz", "r3_ediciones_minutos",
          "r3_ediciones_genera", "r3_ediciones_deck"]
for nombre in LISTAS:
    if (AQUI / (nombre + ".py")).exists():
        importlib.import_module(nombre).registra(c, mover, entre=entre, despues=despues, esc=esc,
                                                 T13=T13, T46=T46, T79=T79, T1011=T1011,
                                                 CJS=CJS, ENS=ENS)


def base(archivo, rev):
    return subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def sustituye(lista, textos):
    fallos = 0
    for clave, archivo, antes, nuevo in lista:
        t = textos[archivo]
        if isinstance(antes, tuple):
            _, inicio, fin = antes
            cuenta = [t.count(inicio), t.count(fin)]
            if cuenta != [1, 1] or not t.index(inicio) < t.index(fin):
                print(f"FALLA · {clave}: los marcadores aparecen {cuenta} veces en {archivo} (se esperaba 1, 1, en orden)")
                fallos += 1
                continue
            i, j = t.index(inicio), t.index(fin)
            textos[archivo] = t[:i] + nuevo + t[j:]
            continue
        n = t.count(antes)
        if n != 1:
            print(f"FALLA · {clave}: el texto original aparece {n} veces en {archivo} (se esperaba 1)")
            fallos += 1
            continue
        textos[archivo] = t.replace(antes, nuevo)
    return fallos


def main():
    rev = "HEAD"
    if "--base" in sys.argv:
        rev = sys.argv[sys.argv.index("--base") + 1]
    comprobar = "--comprobar" in sys.argv
    archivos = sorted({x[1] for x in C} | {x[1] for x in MOVER} | {x[1] for x in POST})
    textos = {a: base(a, rev) for a in archivos}
    fallos = sustituye(C, textos)
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
    fallos += sustituye(POST, textos)
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
    n_por = {a: sum(1 for x in C + POST if x[1] == a) + sum(1 for x in MOVER if x[1] == a) for a in archivos}
    print(f"{len(C) + len(POST)} sustituciones y {len(MOVER)} traslados sobre {rev}: "
          + ", ".join(f"{n_por[a]} en {a.split('/')[-1]}" for a in archivos))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
