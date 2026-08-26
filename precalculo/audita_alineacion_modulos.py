#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audita_alineacion_modulos.py — ¿el módulo al que manda el diagnóstico
enseña lo que el ítem exige?

El preparcial del Corte I no produce un puntaje: produce un plan de
repaso. Cada ítem enlaza a un módulo de los capítulos 1 o 2, y el
termómetro manda ahí a quien falla. Nada comprobaba que ese módulo
contenga lo que hace falta para no volver a fallar.

Y no es una comprobación cosmética: si el módulo no lo trata, el
diagnóstico manda al estudiante a releer algo que no le va a resolver el
fallo — con toda la autoridad de venir impreso, y a días del parcial.

Qué hace: por cada ítem declara los términos que su módulo TIENE que
contener, y busca. Si el módulo no contiene ninguno, es un hueco. Los
huecos que son del CAPÍTULO y no del preparcial se declaran abajo con su
razón, igual que las excepciones de la §4 del verificador: la lista es
corta a propósito, y si crece, lo que hay es un capítulo por escribir.

Salida 0 si no hay huecos sin declarar.
"""
import html
import pathlib
import re
import sys
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
HTMLS = AQUI.parent / "Htmls_Series"
CAPS = {"1": HTMLS / "capitulo-1-componentes-descomposicion.html",
        "2": HTMLS / "capitulo-2-estacionariedad-acf-pacf.html"}

# Lo que cada ítem EXIGE de su módulo. Basta con que aparezca uno de los
# términos: son formas distintas de nombrar la misma cosa, no una lista
# de requisitos que haya que cumplir entera.
EXIGE = {
    "A1": ("1.1", ["orden", "secuencia"]),
    "A2": ("1.4", ["residuo", "irregular"]),
    "A3": ("2.1", ["media constante", "varianza"]),
    "A4": ("2.1", ["autocovarianza", "depende solo del rezago", "solo de h"]),
    "A5": ("2.6", ["kpss"]),
    "A6": ("2.8", ["box-cox", "logaritmo"]),
    "B1": ("1.2", ["ts(", "frequency"]),
    "B2": ("1.5", ["2x4", "2×4", "centrada"]),
    "B3": ("1.6", ["índice estacional", "clásica"]),
    "B4": ("2.2", ["fuera de la banda", "5 %", "5%", "esperan"]),
    "B5": ("2.3", ["autocorrelación muestral", "r_1", "fórmula"]),
    "B6": ("2.4", ["phi_{22}", "pacf", "parcial"]),
    "B7": ("2.6", ["truncamiento", "rezagos"]),
    "B8": ("2.7", ["varianza", "sobrediferenc"]),
    "B9": ("2.8", ["lambda", "guerrero"]),
    "C1": ("1.5", ["centrada", "desfas"]),
    "C2": ("1.7", ["s.window", "stl"]),
    "C3": ("1.8", ["f_t", "fuerza"]),
    "C4": ("2.5", ["caminata", "random walk"]),
    "C5": ("2.3", ["decae", "lenta", "despacio"]),
    "C6": ("2.4", ["phi_{11}", "primer rezago", "pacf"]),
    # «muestra corta» aparece en 2.6, pero solo como paréntesis en una fila de
    # la tabla ADF/KPSS. Lo que el ítem exige es el MECANISMO, así que los
    # términos son los del mecanismo, no los del síntoma.
    "C7": ("2.6", ["potencia", "falso negativo", "ausencia de evidencia",
                   "cambia de veredicto", "más observaciones"]),
    "C8": ("2.6", ["tendencia", "regression", "type ="]),
    "C9": ("2.7", ["estacional", "nabla", "diferencia"]),
    "C10": ("2.9", ["orden", "pipeline"]),
    "D1": ("1.1", ["barajar", "orden"]),
    "D2": ("1.3", ["subseries", "gg_subseries"]),
    "D3": ("1.7", ["robust", "atípico"]),
    "D4": ("2.2", ["ruido blanco", "banda"]),
    "D5": ("2.3", ["periodo", "estacional"]),
    "D6": ("1.3", ["gg_lag", "lag", "rezago"]),   # su claveExtra: el gráfico de rezagos vive en 1.3
    "D7": ("2.7", ["estacional", "rezago 12", "diferencia estacional"]),
}

# Huecos que son del CAPÍTULO, no del preparcial. Cada uno con su razón y
# con lo que se decidió, que es lo que evita rehacer el juicio la próxima vez.
HUECOS_DECLARADOS = {
    "C7": (
        "El módulo 2.6 nombra el caso una sola vez, y de pasada: «Datos poco "
        "informativos (muestra corta)», un paréntesis en una fila de la tabla "
        "ADF/KPSS. Nunca dice «potencia», y en ningún sitio explica el mecanismo "
        "que el ítem pide reconocer — que la MISMA serie cambia de veredicto al "
        "pasar de n=40 a n=200 sin haber cambiado, y que la conclusión fiable es "
        "la de la muestra grande. Quien falle C7 y siga el enlace encuentra ese "
        "paréntesis y poco más. El instrumento sí lo cubre por su cuenta, en el "
        "módulo 8 («falta de potencia: la muestra es corta... con más observaciones "
        "la misma serie puede cambiar de veredicto»), así que el estudiante no se "
        "queda sin la idea; lo que falla es el enlace del diagnóstico. Es un hueco "
        "DEL CAPÍTULO 2 y va a la ronda siguiente: el arreglo es escribirlo allí, "
        "no reenlazar el ítem — no hay otro módulo que lo trate."
    ),
}


def modulos(ruta):
    s = ruta.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<template id="module-(\d+)">(.*?)</template>', s, re.S):
        t = re.sub(r"<script.*?</script>", " ", m.group(2), flags=re.S)
        out[int(m.group(1))] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    return out


def norm(x):
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(c for c in x if unicodedata.category(c) != "Mn")


def main():
    M = {c: modulos(p) for c, p in CAPS.items()}
    print("\n=== audita_alineacion_modulos.py ===\n")
    print("  ¿el módulo al que manda el diagnóstico enseña lo que el ítem exige?\n")
    huecos, parciales = [], []
    for item, (mod, terms) in EXIGE.items():
        cap, n = mod.split(".")
        texto = norm(M[cap].get(int(n), ""))
        falta = [t for t in terms if norm(t) not in texto]
        if len(falta) == len(terms):
            huecos.append((item, mod, terms))
        elif falta:
            parciales.append((item, mod, falta, len(terms) - len(falta)))

    for item, mod, falta, hay in sorted(parciales):
        print(f"  --     {item:4} -> mód. {mod}: encuentra {hay} de {hay + len(falta)}"
              f"  (no está {falta})")

    print()
    sin_declarar = []
    for item, mod, terms in sorted(huecos):
        if item in HUECOS_DECLARADOS:
            print(f"  AVISO  {item:4} -> mód. {mod}: HUECO DECLARADO, del capítulo")
            for linea in re.findall(r".{1,86}(?:\s|$)", HUECOS_DECLARADOS[item]):
                print(f"           {linea.strip()}")
        else:
            sin_declarar.append((item, mod, terms))
            print(f"  FALLA  {item:4} -> mód. {mod}: el módulo no contiene NINGUNO de {terms}")

    print(f"\n  {len(EXIGE)} ítems contrastados contra sus módulos.")
    print(f"  {len(huecos)} huecos, {len(huecos) - len(sin_declarar)} declarados,"
          f" {len(sin_declarar)} sin declarar.")
    if sin_declarar:
        print("\n  El diagnóstico manda a un módulo que no resuelve el fallo. "
              "O se reenlaza el ítem, o se escribe el capítulo, o se declara arriba.")
        return 1
    print("\n  Cada ítem manda a un módulo que trata lo que exige, "
          "salvo los huecos declarados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
