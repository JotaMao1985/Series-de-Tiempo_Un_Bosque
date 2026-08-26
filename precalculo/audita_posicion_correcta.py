#!/usr/bin/env python3
"""
audita_posicion_correcta.py — que la correcta no viva siempre en el mismo sitio

Material de Series de Tiempo 2026-II (20948).

Extiende a los seis capítulos la comprobación que `verifica_preparcial.R` hace
sobre el preparcial en su §4 («Dónde cae la opción correcta»): mismas dos reglas
y mismos dos umbrales, sobre el mismo defecto.

El motor pinta las opciones EN EL ORDEN EN QUE ESTÁN ESCRITAS: no baraja
(`renderAutoevaluacion()`, `p.opciones.map((op, j) => ...)`). Como al redactar se
escribe primero la respuesta y luego los distractores, el 2026-08-26 los seis
capítulos tenían la correcta en la posición 1 en **28 de 28** ítems de una sola
correcta. Quien se diera cuenta aprobaba los quizzes sin leer ni una pregunta.

Se comprueba el **reparto**, no un orden concreto, para que una reordenación
futura siga pasando. Y se comprueba por **archivo**, no por `data-quiz`: la
unidad que el estudiante recorre de una sentada es el capítulo entero, igual que
en el preparcial son sus cuatro bloques juntos. Por bloques sueltos la regla del
40 % sale mordiendo repartos que están bien —con seis ítems y cuatro sitios,
alguno se lleva tres— y una comprobación que salta sin motivo se acaba ignorando.

Va en Python y no en R —al revés que el §4 del preparcial— porque aquí no se
recalcula ninguna cifra: es una lectura de texto, como `inventario_items.py` y
`cuenta_sitio.py`.

Audita lo **publicado**, que es lo que el estudiante abre. Ojo al arreglar: los
capítulos 4, 5 y 6 se ensamblan, y su banco de preguntas vive en
`ensamblado/capN/chapter.js`; tocar el HTML sin reflejarlo allí se pierde en el
siguiente `python3 ensamblado/ensambla_capN.py`.

Uso:  python3 precalculo/audita_posicion_correcta.py [archivo.html ...]
      (sin argumentos audita todo `Htmls_Series/`)

Devuelve 1 si algún quiz concentra las correctas.
"""
from __future__ import annotations

import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = RAIZ / "Htmls_Series"

UMBRAL_POSICION = 0.40   # ninguna posición se lleva más del 40 %
RACHA_MAXIMA = 2         # ni tres ítems seguidos con la correcta en el mismo sitio

# Con menos ítems que posiciones el umbral es inaplicable: una sola correcta en
# una posición ya pasa del 40 %. Esos quizzes se informan y no se juzgan.
MINIMO = 4

ABRE = {"[": "]", "{": "}", "(": ")"}

fallos: list[str] = []


def comprueba(cond: bool, msg: str, extra: str = "") -> None:
    print(("  OK   " if cond else "  FALLA") + f"  {msg}" + (f"   [{extra}]" if extra else ""))
    if not cond:
        fallos.append(msg)


# --- lectura del JavaScript incrustado ---------------------------------------
#
# No se evalúa: se recorre el texto contando delimitadores y saltando cadenas.
# Basta para saber cuántas opciones tiene cada ítem y cuál lleva `correcta: true`,
# y evita depender de un intérprete de JavaScript para una lectura de texto.
# (El §4 del preparcial parte por el sangrado exacto, que allí es uniforme; aquí
# no lo es: los capítulos mezclan opciones de una línea y de cinco.)

def cierra(texto: str, i: int) -> int:
    """Índice del delimitador que cierra el abierto en `texto[i]`."""
    prof, cad, esc = 0, None, False
    for j in range(i, len(texto)):
        c = texto[j]
        if esc:
            esc = False
        elif cad:
            if c == "\\":
                esc = True
            elif c == cad:
                cad = None
        elif c in "'\"`":
            cad = c
        elif c in ABRE:
            prof += 1
        elif c in ")]}":
            prof -= 1
            if prof == 0:
                return j
    raise ValueError(f"delimitador sin cerrar en la posición {i}")


def elementos(texto: str, i: int, j: int) -> list[tuple[int, int]]:
    """Spans de los elementos de primer nivel del array que va de `i` a `j`."""
    spans, k = [], i + 1
    while k < j:
        if texto[k] in " \t\r\n,":
            k += 1
            continue
        if texto[k] not in ABRE:
            raise ValueError(f"elemento no literal en {k}: {texto[k:k+40]!r}")
        fin = cierra(texto, k)
        spans.append((k, fin))
        k = fin + 1
    return spans


def quizzes(texto: str) -> list[tuple[str, int, int]]:
    """(id, inicio, fin) de cada `AUTOEVALUACIONES['id'] = [...]`.

    El comentario que documenta el componente escribe
    `AUTOEVALUACIONES['id'] = [pregunta, ...]` como ejemplo, y eso también es un
    array bien formado: se descarta exigiendo que el primer elemento sea un
    objeto, que es lo que distingue un registro de verdad de su ejemplo.
    """
    salida = []
    for m in re.finditer(r"AUTOEVALUACIONES\[(['\"])([^'\"]+)\1\]\s*=\s*\[", texto):
        i = m.end() - 1
        try:
            fin = cierra(texto, i)
        except ValueError:
            continue
        if texto[i + 1:fin].lstrip()[:1] == "{":
            salida.append((m.group(2), i, fin))
    return salida


def items(texto: str, ini: int, fin: int) -> list[tuple[int, int, list[int]]]:
    """Por ítem con opciones: (número del ítem, cuántas opciones, correctas).

    Los de tipo 'numerica' no tienen `opciones:` y no aparecen, pero sí gastan
    número: el que se devuelve es el que el motor pinta en pantalla, para poder
    señalar el ítem por el mismo nombre con el que el estudiante lo ve.
    """
    salida = []
    for n, (a, b) in enumerate(elementos(texto, ini, fin), 1):
        m = re.search(r"\bopciones\s*:\s*\[", texto[a:b])
        if not m:
            continue
        oi = a + m.end() - 1
        spans = elementos(texto, oi, cierra(texto, oi))
        correctas = [k + 1 for k, (x, y) in enumerate(spans)
                     if re.search(r"\bcorrecta\s*:\s*true\b", texto[x:y + 1])]
        salida.append((n, len(spans), correctas))
    return salida


def racha_maxima(pos: list[int]) -> tuple[int, int]:
    """(longitud de la racha más larga, posición que la forma)."""
    mejor, mejor_val, largo = 0, 0, 0
    for k, p in enumerate(pos):
        largo = largo + 1 if k and p == pos[k - 1] else 1
        if largo > mejor:
            mejor, mejor_val = largo, p
    return mejor, mejor_val


# --- las dos reglas ----------------------------------------------------------

def juzga(etiqueta: str, pos: list[int], avisos: list[str]) -> None:
    n = len(pos)
    if n == 0:
        print(f"  --     {etiqueta}: sin ítems de una sola correcta")
        return

    reparto = {p: pos.count(p) for p in sorted(set(pos))}
    detalle = (f"{n} ítems · orden {''.join(str(p) for p in pos)} · reparto " +
               "  ".join(f"{p}->{c}" for p, c in reparto.items()))

    peor = max(reparto, key=lambda p: reparto[p])
    if n < MINIMO:
        avisos.append(f"{etiqueta}: solo {n} ítems, el umbral del "
                      f"{UMBRAL_POSICION:.0%} no es aplicable")
        print(f"  --     {etiqueta}: {detalle}")
    else:
        comprueba(reparto[peor] / n <= UMBRAL_POSICION,
                  f"{etiqueta}: ninguna posición concentra más del "
                  f"{UMBRAL_POSICION:.0%} de las correctas",
                  f"{detalle} · la peor es la {peor} con {reparto[peor]} de {n} "
                  f"({reparto[peor] / n:.0%})")

    largo, cual = racha_maxima(pos)
    comprueba(largo <= RACHA_MAXIMA,
              f"{etiqueta}: ni {RACHA_MAXIMA + 1} ítems seguidos con la correcta "
              f"en la misma posición",
              f"racha más larga: {largo} (posición {cual})")


def main() -> int:
    rutas = [pathlib.Path(a) for a in sys.argv[1:]] or sorted(SITIO.glob("*.html"))
    avisos: list[str] = []
    prefijos: list[str] = []
    auditados = 0

    # Los dos umbrales, probados contra el estado del que se viene: si no
    # mordieran, pasarían igual de verdes y no se notaría.
    print("Las reglas muerden:")
    comprueba(max({1: 28}.values()) / 28 > UMBRAL_POSICION,
              "la regla del 40 % RECHAZA el reparto del que se viene "
              "(las 28 en la primera)")
    comprueba(racha_maxima([4, 2, 2, 2, 1])[0] > RACHA_MAXIMA,
              "y la regla de la racha RECHAZA tres seguidas en el mismo sitio")

    for ruta in rutas:
        texto = ruta.read_text(encoding="utf-8")
        pos, etiquetas = [], []
        for quiz, ini, fin in quizzes(texto):
            auditados += 1
            for n, nopc, correctas in items(texto, ini, fin):
                if len(correctas) == 1:
                    pos.append(correctas[0])
                    etiquetas.append(f"{quiz}#{n}")
                # Una 'multiple' cuyas correctas son las primeras del array se
                # aprueba marcando el prefijo, sin leer nada. Cae fuera de las
                # dos reglas —que solo miran los ítems de una sola correcta— y
                # se informa, porque es el mismo defecto por otra puerta.
                elif correctas == list(range(1, len(correctas) + 1)) and len(correctas) > 1:
                    prefijos.append(f"{ruta.name} · {quiz} #{n}: las {len(correctas)} "
                                    f"correctas son las {len(correctas)} primeras de {nopc}")
        if pos:
            print(f"\n{ruta.name} — posición de la correcta, en el orden en que "
                  f"se encuentran:")
            print("    " + "  ".join(f"{e}:{p}" for e, p in zip(etiquetas, pos)))
        juzga(ruta.name, pos, avisos)

    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print(f"  ·  {a}")

    if prefijos:
        print("\nAviso — preguntas de varias respuestas cuyas correctas ocupan las\n"
              "primeras posiciones, y que por tanto se aprueban marcando el prefijo:")
        for p in prefijos:
            print(f"  ·  {p}")

    print(f"\n{auditados} quizzes auditados en {len(rutas)} archivos.")
    if fallos:
        print(f"{len(fallos)} FALLOS")
        return 1
    print("Ningún instrumento concentra las correctas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
