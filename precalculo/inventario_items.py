#!/usr/bin/env python3
"""
inventario_items.py — todo lo que ya se le ha preguntado al estudiante sobre el Módulo I

Material de Series de Tiempo 2026-II (20948).

El preparcial del Corte I no puede repetir un enunciado que el estudiante ya vio:
si lo reconoce, acierta sin pensar y el diagnóstico miente. El problema es que la
cuenta de memoria falla. Contando a ojo salieron «10 preguntas»; contadas de
verdad son **60**, y el banco de la defensa toca **los 18 módulos**.

Este guion recoge las tres fuentes y las deja en un JSON que
`verifica_preparcial.R` usa como oráculo:

  · quiz de los capítulos 1 y 2 — claves `pregunta:` de `AUTOEVALUACIONES`
  · banco de la defensa del Taller 1 — los `<li>` de `.banco`
  · ejercicios guiados de los capítulos 1 y 2 — `<div class="ejercicio-guiado">`

No decide nada: deja la lista. Quien decide si un enunciado nuevo choca es P9.

Uso:  python3 precalculo/inventario_items.py
      (desde la carpeta `Series de tiempo/`)
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = RAIZ / "Htmls_Series"
SALIDA = RAIZ / "precalculo" / "salidas" / "inventario_items.json"

CAPS = {
    "cap1": "capitulo-1-componentes-descomposicion.html",
    "cap2": "capitulo-2-estacionariedad-acf-pacf.html",
}
TALLER = "taller-1-modulo-1.html"


def limpia(s: str) -> str:
    """Texto plano comparable: sin marcado, sin entidades, sin escapes de JS."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\\\\", "\\").replace("\\'", "'").replace('\\"', '"')
    return re.sub(r"\s+", " ", s).strip()


def normaliza(s: str) -> str:
    """Forma canónica para detectar casi-duplicados: minúsculas, solo letras y cifras."""
    s = limpia(s).lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def quiz(texto: str) -> list[dict]:
    """Cada `pregunta:` con el `modulo:` que la precede. El `modulo` va antes que
    la `pregunta` en los cuatro tipos, pero en los de tipo `grafico` hay dos
    claves en medio: por eso se recorre en orden en vez de emparejar con un
    solo patrón."""
    marcas = [(m.start(), "mod", m.group(1)) for m in re.finditer(r"modulo:\s*(\d+)", texto)]
    marcas += [
        (m.start(), "q", m.group(2))
        for m in re.finditer(r"pregunta:\s*(['\"])(.*?)\1,?\s*\n", texto, re.S)
    ]
    marcas.sort()
    modulo, salida = None, []
    for _, clase, valor in marcas:
        if clase == "mod":
            modulo = int(valor)
        else:
            salida.append({"modulo": modulo, "texto": limpia(valor)})
    return salida


def banco(texto: str) -> list[dict]:
    i = texto.find('class="banco')
    if i < 0:
        return []
    trozo = texto[i : i + 60000]
    salida = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", trozo, re.S):
        t = limpia(li)
        etiqueta = re.match(r"(cap\. \d · mód\. \d|T\d|transversal)\s*(.*)", t)
        if etiqueta:
            salida.append({"etiqueta": etiqueta.group(1), "texto": etiqueta.group(2)})
    return salida


def ejercicios(texto: str) -> list[dict]:
    """Los `</div>` de cierre no se pueden emparejar con una expresión regular
    —el ejercicio anida pista y solución— así que se corta desde cada apertura
    hasta la siguiente. Basta: lo que interesa es el enunciado, que va primero."""
    aperturas = [m.start() for m in re.finditer(r'<div class="ejercicio-guiado">', texto)]
    salida = []
    for i, ini in enumerate(aperturas):
        fin = aperturas[i + 1] if i + 1 < len(aperturas) else ini + 6000
        cuerpo = limpia(texto[ini:fin])
        if cuerpo:
            salida.append({"texto": cuerpo[:400]})
    return salida


def main() -> int:
    inventario: dict = {"quiz": [], "banco": [], "ejercicios": []}
    for clave, archivo in CAPS.items():
        t = (SITIO / archivo).read_text(encoding="utf-8")
        for q in quiz(t):
            inventario["quiz"].append({"fuente": clave, **q})
        for e in ejercicios(t):
            inventario["ejercicios"].append({"fuente": clave, **e})
    t = (SITIO / TALLER).read_text(encoding="utf-8")
    inventario["banco"] = banco(t)

    for grupo in inventario.values():
        for it in grupo:
            it["normalizado"] = normaliza(it["texto"])

    total = sum(len(g) for g in inventario.values())
    inventario["total"] = total
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(
        json.dumps(inventario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"quiz caps. 1-2 ......... {len(inventario['quiz']):3d}")
    print(f"banco de la defensa .... {len(inventario['banco']):3d}")
    print(f"ejercicios guiados ..... {len(inventario['ejercicios']):3d}")
    print(f"{'':.<24}{total:3d}  ->  {SALIDA.relative_to(RAIZ)}")

    modulos = sorted({(i["fuente"], i["modulo"]) for i in inventario["quiz"]})
    print(f"\nmódulos tocados por el quiz: {len(modulos)} de 18")
    etiquetas = sorted({b["etiqueta"] for b in inventario["banco"]})
    print(f"etiquetas del banco: {len(etiquetas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
