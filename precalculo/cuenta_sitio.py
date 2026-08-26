#!/usr/bin/env python3
"""
cuenta_sitio.py — las cifras del sitio, contadas y no recordadas

Material de Series de Tiempo 2026-II (20948).

La portada y el README anuncian cuántos capítulos, módulos, simuladores,
preguntas y ejercicios tiene el material. Son las primeras cifras que alguien
lee al entrar, y son justo las que nadie rehace: **cuando el capítulo 1 creció
con la ronda de Loess y STL, su tarjeta siguió diciendo 7 simuladores durante
meses, y había 11.** Nadie mintió; simplemente nadie volvió a contar.

Este guion cuenta sobre los archivos y **contrasta lo contado con lo escrito**.
No arregla nada: dice qué no cuadra y dónde, que es lo que permite arreglarlo
en el sitio correcto.

Qué cuenta cada cosa, dicho por si algún día no cuadra por definición y no por
error:

  · módulo      — un `<template id="module-N">` en el marcado
  · simulador   — un `data-simulador` DISTINTO en el marcado (los repetidos,
                  como la tira de variante del taller, cuentan una vez)
  · pregunta    — una clave `pregunta:` en los arrays de autoevaluación
  · ejercicio   — un `<div class="ejercicio-guiado">`

Uso:  python3 precalculo/cuenta_sitio.py
      (desde la carpeta `Series de tiempo/`)

Devuelve 1 si alguna cifra escrita no coincide con la contada.
"""
from __future__ import annotations

import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = RAIZ / "Htmls_Series"

CAPITULOS = [
    ("capitulo-1-componentes-descomposicion.html", "Componentes y descomposición"),
    ("capitulo-2-estacionariedad-acf-pacf.html", "Estacionariedad, ACF y PACF"),
    ("capitulo-3-modelos-ar-ma-arma.html", "Modelos AR, MA y ARMA"),
    ("capitulo-4-modelos-arima.html", "Modelos ARIMA y Box–Jenkins"),
    ("capitulo-5-sarima.html", "Modelos SARIMA"),
    ("capitulo-6-pronostico-evaluacion.html", "Pronóstico y evaluación"),
]
TALLERES = [
    ("taller-1-modulo-1.html", "Taller 1 · Módulo I"),
    ("preparcial-corte-1.html", "Preparcial · Corte I"),
]

# El preparcial no declara simuladores ni ejercicios: lo que anuncia son sus
# módulos y sus ítems. Se comprueban aparte porque su tarjeta y su fila del
# README no tienen la forma de las de los capítulos — y sin esto quedaría
# registrado pero con las cifras sin contrastar, que es exactamente cómo la
# tarjeta del capítulo 1 estuvo meses diciendo 7 simuladores cuando eran 11.
PREPARCIAL = "preparcial-corte-1.html"


def cuenta(ruta: pathlib.Path) -> dict:
    t = ruta.read_text(encoding="utf-8")
    marcado = t[:t.rindex("\n  <script>")] if "\n  <script>" in t else t
    return {
        "modulos": len(re.findall(r'<template id="module-\d+">', marcado)),
        "simuladores": len(set(re.findall(r'data-simulador="([^"]+)"', marcado))),
        "preguntas": len(re.findall(r"^\s*pregunta:\s*", t, re.M)),
        "ejercicios": marcado.count('<div class="ejercicio-guiado">'),
        "kb": round(len(t.encode("utf-8")) / 1024),
    }


def main() -> int:
    faltan = [n for n, _ in CAPITULOS + TALLERES if not (SITIO / n).exists()]
    if faltan:
        sys.exit(f"PARADO: faltan del sitio: {faltan}")

    print("\n=== cuenta_sitio.py ===\n")
    print(f"  {'archivo':<40} {'mód':>4} {'sim':>4} {'preg':>5} {'ejer':>5} {'KB':>6}")
    print("  " + "-" * 68)

    caps = {}
    for nombre, _ in CAPITULOS:
        c = cuenta(SITIO / nombre)
        caps[nombre] = c
        print(f"  {nombre:<40} {c['modulos']:>4} {c['simuladores']:>4} "
              f"{c['preguntas']:>5} {c['ejercicios']:>5} {c['kb']:>6}")
    tot = {k: sum(c[k] for c in caps.values())
           for k in ("modulos", "simuladores", "preguntas", "ejercicios", "kb")}
    print("  " + "-" * 68)
    print(f"  {f'{len(CAPITULOS)} capítulos':<40} {tot['modulos']:>4} "
          f"{tot['simuladores']:>4} {tot['preguntas']:>5} {tot['ejercicios']:>5} {tot['kb']:>6}")

    print()
    talleres = {}
    for nombre, _ in TALLERES:
        c = cuenta(SITIO / nombre)
        talleres[nombre] = c
        print(f"  {nombre:<40} {c['modulos']:>4} {c['simuladores']:>4} "
              f"{c['preguntas']:>5} {c['ejercicios']:>5} {c['kb']:>6}")

    # --- Lo escrito contra lo contado ------------------------------------
    idx = (SITIO / "index.html").read_text(encoding="utf-8")
    readme = (SITIO / "README.md").read_text(encoding="utf-8")
    problemas = []

    # La banda de la portada.
    for patron, esperado, que in (
            (r">(\d+) capítulos<", len(CAPITULOS), "capítulos en la banda de la portada"),
            (r"(\d+) módulos en total", tot["modulos"], "módulos en la banda"),
            (r">(\d+) simuladores<", tot["simuladores"], "simuladores en la banda"),
            (r">(\d+) preguntas<", tot["preguntas"], "preguntas en la banda"),
            (r"Y (\d+) ejercicios resueltos", tot["ejercicios"], "ejercicios en la banda")):
        m = re.search(patron, idx)
        if not m:
            problemas.append(f"no encuentro en index.html: {que}")
        elif int(m.group(1)) != esperado:
            problemas.append(f"{que}: dice {m.group(1)} y son {esperado}")

    # La cabecera y las metadescripciones. La banda ya decía 65 simuladores y
    # estas TRES decían 61 —el número de módulos, por coincidencia—: la frase
    # que más se lee del sitio y las dos que viajan a Google y a WhatsApp.
    # Se colaron porque la comprobación solo miraba la banda.
    for patron, que in ((r"y (\d+) simuladores para mover", "párrafo de cabecera de la portada"),
                        (r"código en R y Python, (\d+) simuladores y", "metadescripción de la portada"),
                        (r"Python, (\d+) simuladores interactivos", "descripción para redes sociales")):
        m = re.search(patron, idx)
        if not m:
            problemas.append(f"no encuentro en index.html: {que}")
        elif int(m.group(1)) != tot["simuladores"]:
            problemas.append(f"{que}: dice {m.group(1)} simuladores y son {tot['simuladores']}")

    # Las tarjetas, capítulo a capítulo. Es donde se quedó atrás el 1.
    for i, (nombre, _) in enumerate(CAPITULOS, 1):
        m = re.search(rf'href="{re.escape(nombre)}"[\s\S]{{0,2200}}?'
                      r"(\d+) módulos · (\d+) simuladores", idx)
        if not m:
            problemas.append(f"la tarjeta del capítulo {i} no declara sus cifras")
            continue
        for leido, real, que in ((m.group(1), caps[nombre]["modulos"], "módulos"),
                                 (m.group(2), caps[nombre]["simuladores"], "simuladores")):
            if int(leido) != real:
                problemas.append(f"tarjeta del capítulo {i}: dice {leido} {que} y son {real}")

    # El README: la tabla de contenido y la línea del total.
    for i, (nombre, _) in enumerate(CAPITULOS, 1):
        fila = re.search(rf"\|\s*{i}\s*\|\s*\[[^\]]+\]\({re.escape(nombre)}\)[^|]*\|[^|]*\|"
                         r"\s*(\d+)\s*\|\s*(\d+)\s*\|", readme)
        if not fila:
            problemas.append(f"el README no tiene fila para el capítulo {i}")
            continue
        for leido, real, que in ((fila.group(1), caps[nombre]["modulos"], "módulos"),
                                 (fila.group(2), caps[nombre]["simuladores"], "simuladores")):
            if int(leido) != real:
                problemas.append(f"README, capítulo {i}: dice {leido} {que} y son {real}")

    m = re.search(r"\*\*(\d+) módulos,\s*(\d+)\s*\n?simuladores, (\d+) preguntas de "
                  r"autoevaluación y (\d+) ejercicios", readme)
    if not m:
        problemas.append("no encuentro la línea de totales del README")
    else:
        for leido, real, que in zip(m.groups(),
                                    (tot["modulos"], tot["simuladores"],
                                     tot["preguntas"], tot["ejercicios"]),
                                    ("módulos", "simuladores", "preguntas", "ejercicios")):
            if int(leido) != real:
                problemas.append(f"README, totales: dice {leido} {que} y son {real}")

    m = re.search(r"\*\*(\d+)\s*\n?simuladores\*\* interactivos", readme)
    if m and int(m.group(1)) != tot["simuladores"]:
        problemas.append(f"README, párrafo de cabecera: dice {m.group(1)} simuladores "
                         f"y son {tot['simuladores']}")

    # El preparcial: sus dos cifras, en la portada y en el README.
    prep = talleres[PREPARCIAL]
    m = re.search(rf'href="{re.escape(PREPARCIAL)}"[\s\S]{{0,2200}}?'
                  r"(\d+) módulos · (\d+) ítems", idx)
    if not m:
        problemas.append("la tarjeta del preparcial no declara sus cifras")
    else:
        for leido, real, que in ((m.group(1), prep["modulos"], "módulos"),
                                 (m.group(2), prep["preguntas"], "ítems")):
            if int(leido) != real:
                problemas.append(f"tarjeta del preparcial: dice {leido} {que} y son {real}")

    fila = re.search(rf"\|[^|]*\|\s*\[[^\]]+\]\({re.escape(PREPARCIAL)}\)[^|]*\|[^|]*\|"
                     r"\s*(\d+)\s*\|\s*(\d+)\s*\|", readme)
    if not fila:
        problemas.append("el README no tiene fila para el preparcial")
    else:
        for leido, real, que in ((fila.group(1), prep["modulos"], "módulos"),
                                 (fila.group(2), prep["preguntas"], "ítems")):
            if int(leido) != real:
                problemas.append(f"README, preparcial: dice {leido} {que} y son {real}")

    # El taller, alcanzable desde la portada. En Espacial quedó publicado y
    # con cero enlaces entrantes: existía y no se podía llegar a él.
    for nombre, titulo in TALLERES:
        if f'href="{nombre}"' not in idx:
            problemas.append(f"{titulo} no está enlazado desde la portada: quedaría "
                             f"publicado e inalcanzable")
        if f"]({nombre})" not in readme:
            problemas.append(f"{titulo} no está registrado en el README")

    # Los componentes que el README declara tener, contados sobre el marcado.
    declarados = re.findall(r"^\|\s*`\.([a-z-]+)`\s*\|", readme, re.M)
    m = re.search(r"el material usa (\w+) componentes propios", readme)
    NUM = {"tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8}
    if m:
        dicho = NUM.get(m.group(1))
        if dicho != len(declarados):
            problemas.append(f"el README dice «{m.group(1)} componentes propios» y su tabla "
                             f"lista {len(declarados)}")

    print()
    if problemas:
        for p in problemas:
            print(f"  MAL  {p}")
        print(f"\n  {len(problemas)} cifra(s) del sitio que no cuadran.\n")
        return 1
    print("  Las cifras escritas coinciden con las contadas.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
