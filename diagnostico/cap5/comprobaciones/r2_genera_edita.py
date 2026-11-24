#!/usr/bin/env python3
"""R2 del cap. 5 · escribe r2_edita.py a partir de la diferencia entre HEAD y el árbol de trabajo.

Cada bloque distinto de cada fuente se convierte en una sustitución (antes → después) con el contexto
justo para que el «antes» sea único en el archivo de HEAD (y siga siéndolo al aplicar las anteriores) y
el «después», en el archivo nuevo.
Se ejecuta una vez, cuando las fuentes están terminadas; r2_edita.py es el guion que queda.

Uso: python3 diagnostico/cap5/comprobaciones/r2_genera_edita.py
"""
import difflib
import pathlib
import subprocess

RAIZ = pathlib.Path(__file__).resolve().parents[3]
FUENTES = [
    "ensamblado/componentes/mapa_estacional.css",
    "ensamblado/componentes/mapa_estacional.js",
    "ensamblado/retropropaga_mapa.py",
    "ensamblado/cap5/chapter.js",
    "ensamblado/cap5/templates_1_3.html",
    "ensamblado/cap5/templates_4_6.html",
    "ensamblado/cap5/templates_7_9.html",
    "ensamblado/cap5/templates_10_11.html",
]


def head(archivo):
    return subprocess.run(["git", "show", f"HEAD:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def sustituciones(viejo, nuevo):
    a, b = viejo.splitlines(keepends=True), nuevo.splitlines(keepends=True)
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != "equal"]
    # Contexto mínimo para que el «antes» sea único; los bloques que se tocan se funden.
    bloques = []
    for _, i1, i2, j1, j2 in ops:
        c = 0
        while True:
            x1, x2 = max(0, i1 - c), min(len(a), i2 + c)
            y1, y2 = j1 - (i1 - x1), j2 + (x2 - i2)
            antes, despues = "".join(a[x1:x2]), "".join(b[y1:y2])
            # Único el «antes» en el viejo y el «después» en el nuevo: lo segundo deja
            # reconocer una sustitución ya aplicada.
            if antes and despues and viejo.count(antes) == 1 and nuevo.count(despues) == 1:
                break
            c += 1
        bloques.append([x1, x2, y1, y2])
    fundidos = []
    for blq in bloques:
        if fundidos and blq[0] <= fundidos[-1][1]:
            f = fundidos[-1]
            f[1], f[3] = max(f[1], blq[1]), max(f[3], blq[3])
        else:
            fundidos.append(blq)
    return [("".join(a[x1:x2]), "".join(b[y1:y2])) for x1, x2, y1, y2 in fundidos]


def aplica(texto, pares):
    for antes, despues in pares:
        assert texto.count(antes) == 1, antes[:80]
        texto = texto.replace(antes, despues, 1)
    return texto


lineas = []
total = 0
for archivo in FUENTES:
    viejo, nuevo = head(archivo), (RAIZ / archivo).read_text(encoding="utf-8")
    pares = sustituciones(viejo, nuevo)
    assert aplica(viejo, pares) == nuevo, archivo
    for k, (antes, despues) in enumerate(pares, 1):
        lineas.append(f"c({archivo.split('/')[-1] + ' · ' + str(k)!r}, {archivo!r},\n  {antes!r},\n  {despues!r})\n")
    total += len(pares)
    print(f"{archivo}: {len(pares)} sustituciones")

CABECERA = '''#!/usr/bin/env python3
"""R2 del capítulo 5 · reaplica sobre HEAD las ediciones de la ronda de gráficas y simuladores.

Ocho fuentes: el componente `.mapa-estacional` (`ensamblado/componentes/mapa_estacional.{css,js}`), el
modo `--actualiza` de `ensamblado/retropropaga_mapa.py`, y el capítulo 5 (`ensamblado/cap5/chapter.js` y
las cuatro plantillas de módulo con lienzos). Parte de cada archivo en el commit base (por defecto HEAD) y
aplica cada sustitución, cuyo «antes» debe aparecer exactamente una vez. Si una sustitución ya está
aplicada (su «después» ya está y su «antes» no, o el «antes» va dentro del «después» y este ya está), se
salta: así el guion vale también sobre un árbol que ya la lleva. Reejecutarlo no cambia nada.

Generado por r2_genera_edita.py desde la diferencia con HEAD (e084436).

Uso (desde la raíz del repo):
    python3 diagnostico/cap5/comprobaciones/r2_edita.py              # escribe las fuentes
    python3 diagnostico/cap5/comprobaciones/r2_edita.py --comprobar  # solo compara
    python3 diagnostico/cap5/comprobaciones/r2_edita.py --ensambla   # escribe y regenera lo derivado
    python3 diagnostico/cap5/comprobaciones/r2_edita.py --base e084436

Lo derivado, en este orden (lo hace --ensambla):
    python3 ensamblado/retropropaga_mapa.py --actualiza   # caps. 1 y plantilla
    python3 ensamblado/ensambla_cap5.py
    python3 ensamblado/ensambla_cap6.py
    python3 precalculo/ensambla_proyecto.py               # la guía, que sale de la plantilla
"""
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
C = []  # (clave, archivo, antes, después)


def c(clave, archivo, antes, despues):
    C.append((clave, archivo, antes, despues))


'''

PIE = '''

def base(archivo, rev):
    return subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def main():
    rev = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "HEAD"
    comprobar = "--comprobar" in sys.argv
    archivos = list(dict.fromkeys(x[1] for x in C))
    textos = {a: base(a, rev) for a in archivos}
    fallos = saltadas = 0
    for clave, archivo, antes, despues in C:
        t = textos[archivo]
        if antes in despues:
            ya = t.count(despues) == 1
        else:
            ya = t.count(antes) == 0 and t.count(despues) == 1
        if ya:
            saltadas += 1
            continue
        n = t.count(antes)
        if n != 1:
            print(f"FALLA · {clave}: el texto original aparece {n} veces en {archivo} (se esperaba 1)")
            fallos += 1
            continue
        textos[archivo] = t.replace(antes, despues, 1)
    if fallos:
        sys.exit(f"{fallos} sustituciones no aplicadas; no se escribe nada")
    for archivo, texto in textos.items():
        ruta = RAIZ / archivo
        if comprobar:
            igual = ruta.read_text(encoding="utf-8") == texto
            print(f"{archivo}: {'idéntico a ' + rev + ' + ediciones' if igual else 'DIFIERE de ' + rev + ' + ediciones'}")
            fallos += 0 if igual else 1
        elif ruta.read_text(encoding="utf-8") != texto:
            ruta.write_text(texto, encoding="utf-8")
    print(f"{len(C)} sustituciones sobre {rev} ({saltadas} ya aplicadas): "
          + ", ".join(f"{sum(1 for x in C if x[1] == a)} en {a.split('/')[-1]}" for a in archivos))
    if "--ensambla" in sys.argv and not comprobar:
        for orden in (["ensamblado/retropropaga_mapa.py", "--actualiza"], ["ensamblado/ensambla_cap5.py"],
                      ["ensamblado/ensambla_cap6.py"], ["precalculo/ensambla_proyecto.py"]):
            subprocess.run([sys.executable] + orden, cwd=RAIZ, check=True)
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
'''

salida = pathlib.Path(__file__).with_name("r2_edita.py")
salida.write_text(CABECERA + "".join(lineas) + PIE, encoding="utf-8")
print(f"{total} sustituciones escritas en {salida.name}")
