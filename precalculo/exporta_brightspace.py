#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exporta_brightspace.py — banco de la Biblioteca de Preguntas desde el preparcial

Material de Series de Tiempo 2026-II (20948).

Lee los ítems del **HTML publicado** del preparcial del Corte I y escribe un
paquete QTI 1.2 con las extensiones `d2l_2p0` que exige Brightspace.

Se lee el documento y no `salidas/preparcial_datos.json` por la misma razón por
la que lo hace el exportador de Estadística Espacial: lo que se exporta tiene
que ser **lo que el estudiante vio**, no lo que un JSON dice que vio. El JSON
lleva las cifras; el enunciado, las opciones y la retroalimentación por opción
solo existen en el documento.

Tres tipos de pregunta y tres destinos:

    opcion    ->  Multiple Choice
    grafico   ->  Multiple Choice, con el <canvas> ya rasterizado a PNG
    numerica  ->  FUERA, y el informe las nombra una a una

La numérica es la que obliga a este guion a decir que no. La Biblioteca de
Preguntas **no importa respuesta numérica**, así que solo puede viajar
convertida en opción múltiple, y para eso hacen falta tres distractores que
sean errores concretos. El material nombra **uno** por ítem —«si sumas 30 meses
te vas a enero de 2022»—, nunca tres. Inventar los otros dos aquí sería
escribir a mano cifras del material, que es justo lo que este repositorio no
hace: cada cifra del preparcial se rehace en R. El informe nombra las nueve y
dice qué distractor sí tiene cada una, para que quien quiera incluirlas sepa
exactamente qué le falta y dónde calcularlo.

Entra:  Htmls_Series/preparcial-corte-1.html
        precalculo/salidas/graficos_preparcial/   (node precalculo/rasteriza_graficos.js)
Sale:   parcial/brightspace/banco_brightspace.zip
        parcial/brightspace/sonda_brightspace.zip   con --sonda

Uso:

    python3 precalculo/exporta_brightspace.py [--sonda] [--con-pista]

La salida NO se versiona: es un artefacto de construcción y lleva la clave de
respuesta junta en un archivo, que es una forma de dejarla suelta que el
documento publicado no tiene.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "precalculo"))

# El analizador de literales de JavaScript vive en `audita_posicion_correcta.py`
# y de ahí se importa. Copiarlo aquí sería tener dos convenios que se
# desincronizan sin que nada falle, y el de este guion fallaría en silencio
# exportando de menos.
from audita_posicion_correcta import cierra, elementos, quizzes  # noqa: E402

CANDIDATOS_SKILL = [
    pathlib.Path.home() / ".claude/skills/brightspace-elbosque/scripts",
    pathlib.Path.home() / ".claude/plugins/cache/brightspace-elbosque/scripts",
]


def carga_d2l(ruta_skill):
    rutas = [pathlib.Path(ruta_skill)] if ruta_skill else CANDIDATOS_SKILL
    for r in rutas:
        if (r / "d2l_items.py").exists():
            sys.path.insert(0, str(r))
            import d2l_items  # noqa: PLC0415
            return d2l_items
    sys.exit(
        "PARADO: no encuentro `d2l_items.py`, que es de la skill "
        "`brightspace-elbosque` y no de este repositorio.\n        Busqué en:\n          "
        + "\n          ".join(str(r) for r in rutas)
        + "\n        Pásame su carpeta con --skill <ruta>/scripts."
    )


# =====================================================================
# LEER EL DOCUMENTO
# =====================================================================

def cadena(texto, i):
    """Valor y fin del literal de cadena que empieza en `texto[i]`.

    `cierra()` casa paréntesis y corchetes, no comillas: hace falta este otro
    lector para los campos de texto, que además llevan comillas escapadas
    dentro (`d\\'Agostino`).
    """
    q, j, partes = texto[i], i + 1, []
    while j < len(texto):
        c = texto[j]
        if c == "\\":
            partes.append(texto[j:j + 2])
            j += 2
            continue
        if c == q:
            return "".join(partes), j
        partes.append(c)
        j += 1
    raise ValueError(f"cadena sin cerrar en {i}")


def campo(cuerpo, nombre):
    m = re.search(rf"\b{nombre}\s*:\s*(['\"])", cuerpo)
    return cadena(cuerpo, m.end() - 1)[0] if m else None


def bandera(cuerpo, nombre):
    m = re.search(rf"\b{nombre}\s*:\s*(true|false)\b", cuerpo)
    return m.group(1) == "true" if m else False


def opciones_de(cuerpo):
    m = re.search(r"\bopciones\s*:\s*\[", cuerpo)
    if not m:
        return []
    oi = m.end() - 1
    salida = []
    for a, b in elementos(cuerpo, oi, cierra(cuerpo, oi)):
        trozo = cuerpo[a:b + 1]
        salida.append({
            "texto": campo(trozo, "texto") or "",
            "correcta": bandera(trozo, "correcta"),
            "retro": campo(trozo, "retro") or "",
        })
    return salida


def lee_documento(ruta):
    """Los ítems del preparcial, en el orden en que el estudiante los ve.

    Cinco fuentes: los cuatro bloques de `AUTOEVALUACIONES` y el simulacro
    cronometrado, que vive aparte en `SIMULACRO.items` y que también son
    preguntas del Corte I.
    """
    t = ruta.read_text(encoding="utf-8")
    grupos = []
    for qid, i, f in quizzes(t):
        if qid == "id":          # el ejemplo del comentario que documenta el componente
            continue
        grupos.append((qid, elementos(t, i, f)))

    m = re.search(r"const SIMULACRO\s*=\s*\{", t)
    if m:
        mi = re.search(r"\bitems\s*:\s*\[", t[m.start():])
        oi = m.start() + mi.end() - 1
        grupos.append(("simulacro", elementos(t, oi, cierra(t, oi))))

    items = []
    for bloque, spans in grupos:
        for n, (a, b) in enumerate(spans, 1):
            c = t[a:b + 1]
            items.append({
                "bloque": bloque,
                "n": n,
                "tipo": campo(c, "tipo"),
                "clave": campo(c, "clave"),
                "claveExtra": campo(c, "claveExtra"),
                "objetivo": campo(c, "objetivo"),
                "pregunta": campo(c, "pregunta") or "",
                "pista": campo(c, "pista") or "",
                "descripcion": campo(c, "descripcionGrafico") or "",
                "respuesta": (re.search(r"\brespuesta\s*:\s*(-?[0-9.]+)", c) or [None, None])[1]
                             if re.search(r"\brespuesta\s*:\s*(-?[0-9.]+)", c) else None,
                "retroFallo": campo(c, "retroFallo") or "",
                "opciones": opciones_de(c),
            })
    return items


# =====================================================================
# PASARLO A LO QUE BRIGHTSPACE RENDERIZA
# =====================================================================

# El material escribe las matemáticas con los delimitadores de KaTeX. El
# MathJax de Brightspace **no** trata el `$` como delimitador por defecto: sin
# esta conversión las fórmulas salen en crudo, con los dólares a la vista.
def a_mathjax(html):
    html = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", html, flags=re.S)
    html = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", r"\\(\1\\)", html, flags=re.S)
    return html


# `&nbsp;` y demás entidades con nombre viajan bien en HTML, pero el XML solo
# conoce cinco. Se convierten a la referencia numérica equivalente.
ENTIDADES = {"&nbsp;": "&#160;", "&mdash;": "&#8212;", "&ndash;": "&#8211;",
             "&hellip;": "&#8230;", "&times;": "&#215;", "&minus;": "&#8722;",
             "&aacute;": "á", "&eacute;": "é", "&iacute;": "í",
             "&oacute;": "ó", "&uacute;": "ú", "&ntilde;": "ñ"}


def limpia(html):
    html = html.replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
    for k, v in ENTIDADES.items():
        html = html.replace(k, v)
    return a_mathjax(html)


LETRA = {"bloque-a": "A", "bloque-b": "B", "bloque-c": "C", "bloque-d": "D",
         "bloque-e": "E", "simulacro": "S"}

NOMBRE_BLOQUE = {"bloque-a": "Bloque A · Conceptos", "bloque-b": "Bloque B · Cálculo",
                 "bloque-c": "Bloque C · Interpretación", "bloque-d": "Bloque D · Gráficos",
                 "bloque-e": "Bloque E · Gráficos de series (FPP3 cap. 2)",
                 "simulacro": "Simulacro cronometrado"}


def construye(items, imagenes_dir, prefijo, con_pista, d2l):
    """(ítems D2L crudos, imágenes, fuera) — sin escribir nada todavía."""
    crudos, imagenes, fuera = [], {}, []
    graficos_por_bloque = {}

    for it in items:
        etiqueta = f"{LETRA[it['bloque']]}{it['n']:02d}"
        qid = f"{prefijo}_{etiqueta}"
        modulo = it["clave"] + (f" y {it['claveExtra']}" if it["claveExtra"] else "")

        if it["tipo"] == "numerica":
            fuera.append(it)
            continue

        partes = [f"<p>{limpia(it['pregunta'])}</p>"]

        if it["tipo"] == "grafico":
            k = graficos_por_bloque.get(it["bloque"], 0) + 1
            graficos_por_bloque[it["bloque"]] = k
            png = imagenes_dir / f"{it['bloque']}_{k}.png"
            if not png.exists():
                sys.exit(f"PARADO: falta {png.name}. Los gráficos se rasterizan antes:\n"
                         f"        node precalculo/rasteriza_graficos.js")
            ruta_zip = f"images/{it['bloque']}_{k}.png"
            imagenes[ruta_zip] = png.read_bytes()
            # `max-width` y no `width`: la columna de Brightspace es más
            # estrecha que el lienzo de 1424 px con el que se rasterizó.
            partes.append(
                f'<p><img src="{ruta_zip}" alt="{limpia(it["descripcion"])}" '
                f'style="max-width:100%; height:auto;" /></p>')

        if con_pista and it["pista"]:
            partes.append(f"<p><em>Pista.</em> {limpia(it['pista'])}</p>")

        opciones = [{"texto": limpia(o["texto"]), "correcta": o["correcta"],
                     "retro": limpia(o["retro"])} for o in it["opciones"]]

        crudos.append({
            "qid": qid,
            "enunciado_html": "".join(partes),
            "titulo": f"{NOMBRE_BLOQUE[it['bloque']]} · módulo {modulo} · {it['objetivo']}",
            "opciones": opciones,
            "_tipo": it["tipo"],
            "_objetivo": it["objetivo"],
            "_correctas": sum(1 for o in opciones if o["correcta"]),
        })

    return crudos, imagenes, fuera


def arma(crudos, d2l):
    """Los ítems D2L. `pagina` es el ordinal: 1…N, sin huecos ni repeticiones."""
    return [d2l.construye_item(
        qid=c["qid"], enunciado_html=c["enunciado_html"],
        opciones=c["opciones"], titulo=c["titulo"], pagina=n)
        for n, c in enumerate(crudos, 1)]


# =====================================================================

def main():
    ap = argparse.ArgumentParser(description="Preparcial del Corte I → banco de Brightspace.")
    ap.add_argument("--html", default="Htmls_Series/preparcial-corte-1.html")
    ap.add_argument("--imagenes", default="precalculo/salidas/graficos_preparcial")
    ap.add_argument("--salida", default="parcial/brightspace")
    ap.add_argument("--prefijo", default="ST_C1")
    ap.add_argument("--titulo", default="Series de Tiempo · Corte I")
    ap.add_argument("--skill", help="carpeta scripts/ de la skill brightspace-elbosque")
    ap.add_argument("--sonda", action="store_true",
                    help="además, un paquete de 3 ítems para probar la importación")
    ap.add_argument("--con-pista", action="store_true",
                    help="incluye la pista del documento (banco de práctica, no de examen)")
    a = ap.parse_args()

    d2l = carga_d2l(a.skill)
    items = lee_documento(RAIZ / a.html)
    crudos, imagenes, fuera = construye(
        items, RAIZ / a.imagenes, a.prefijo, a.con_pista, d2l)

    if not crudos:
        sys.exit("PARADO: cero ítems. Un banco vacío se importa sin protestar "
                 "y deja el cuestionario sin preguntas.")

    salida = RAIZ / a.salida
    salida.mkdir(parents=True, exist_ok=True)
    zip_banco = salida / "banco_brightspace.zip"
    tam = d2l.escribe_paquete(str(zip_banco), arma(crudos, d2l), a.titulo, imagenes=imagenes)

    zip_sonda = None
    if a.sonda:
        # Uno de cada forma que el banco usa. El gráfico es el que hay que mirar
        # con los ojos: es donde se ve si la figura viajó y si se lee.
        pick = [next(c for c in crudos if c["_tipo"] == "opcion"),
                next(c for c in crudos if c["_tipo"] == "grafico")]
        img_sonda = {r: b for r, b in imagenes.items()
                     if any(r in c["enunciado_html"] for c in pick)}
        zip_sonda = salida / "sonda_brightspace.zip"
        d2l.escribe_paquete(str(zip_sonda), arma(pick, d2l),
                            a.titulo + " · sonda", imagenes=img_sonda)

    # ------------------------------------------------------------ informe
    from collections import Counter
    por_tipo = Counter(c["_tipo"] for c in crudos)
    por_obj = Counter(c["_objetivo"] for c in crudos)
    ms = [c["qid"] for c in crudos if c["_correctas"] > 1]

    print(f"\n  Banco: {zip_banco.relative_to(RAIZ)}  ({tam // 1024} KB)")
    if zip_sonda:
        print(f"  Sonda: {zip_sonda.relative_to(RAIZ)}  — se sube PRIMERO")
    print(f"\n  {len(crudos)} ítems · {por_tipo['opcion']} de opción · "
          f"{por_tipo['grafico']} con gráfico · {len(imagenes)} imagen(es)")
    print(f"  Retroalimentación: {sum(1 for c in crudos for o in c['opciones'] if o['retro'])}"
          f"/{sum(len(c['opciones']) for c in crudos)} opciones con explicación")
    print("  Por objetivo: " + " · ".join(f"{k} {por_obj[k]}" for k in sorted(por_obj)))
    if ms:
        print(f"\n  ⚠ {len(ms)} ítem(s) de varias respuestas ({', '.join(ms)}): salen como "
              f"Multi-Select, que NUNCA se ha importado a un Brightspace real. Pruébalos "
              f"con la sonda antes de subir el banco.")

    if fuera:
        print(f"\n  {len(fuera)} numérica(s) FUERA — la Biblioteca de Preguntas no importa")
        print("  respuesta numérica, y convertirlas pide tres distractores. El material")
        print("  nombra uno por ítem; los otros dos habría que calcularlos en R:\n")
        for it in fuera:
            # Los decimales valen vengan de donde vengan —el fallo que nombra
            # el ítem 2.3 es $-0.64$, dentro de una fórmula—, pero los enteros
            # solo se recogen de la prosa: dentro de un $\tfrac18$ hay dígitos
            # que no son valores de respuesta, y listarlos como distractores
            # candidatos sería ruido con pinta de dato.
            sin_etiquetas = re.sub(r"<[^>]+>", " ", it["retroFallo"])
            sin_ordenes = re.sub(r"\\[a-zA-Z]+", " ", sin_etiquetas)
            prosa = re.sub(r"\$[^$]*\$", " ", sin_etiquetas)
            citadas = (re.findall(r"-?\d+\.\d+", sin_ordenes)
                       + re.findall(r"(?<![\d.])-?\d+(?![\d.])", prosa))
            resp = str(it["respuesta"])
            otras = [c for c in dict.fromkeys(citadas) if c != resp][:3]
            print(f"      {LETRA[it['bloque']]}{it['n']:02d} · módulo {it['clave']:4s} "
                  f"· {it['objetivo']} · respuesta {resp:>8s} · "
                  f"el fallo que nombra: {', '.join(otras) if otras else '—'}")

    print(f"\n  Audita antes de subir:\n"
          f"      python3 ~/.claude/skills/brightspace-elbosque/scripts/audita_paquete.py "
          f"--zip {zip_banco.relative_to(RAIZ)}\n")


if __name__ == "__main__":
    main()
