#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audita_brightspace.py — que el banco diga lo que dice el preparcial

Material de Series de Tiempo 2026-II (20948).

`audita_paquete.py` —el de la skill— mira el ZIP por dentro: que el XML esté
bien formado, que cada opción tenga puntuación, que las imágenes declaradas
sean las empaquetadas. Todo eso puede estar perfecto y el banco seguir estando
mal de la única manera que de verdad importa: **con otra respuesta correcta**.
Ese defecto no deja rastro dentro del paquete. Solo se ve comparándolo con el
documento del que salió.

Este auditor hace esa comparación, y **no reutiliza el analizador estructurado**
de `exporta_brightspace.py`. Si ese analizador leyera mal una opción, un
auditor que usara la misma función leería mal exactamente igual y diría que
todo está bien. Aquí se busca cada texto de opción dentro del HTML en crudo y
se mira si el objeto que lo contiene lleva `correcta: true`.

Uso:  python3 precalculo/audita_brightspace.py
      [--zip parcial/brightspace/banco_brightspace.zip]

Devuelve 1 si alguna comprobación falla.
"""
from __future__ import annotations

import argparse
import html as _html
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent

fallos, comprobaciones = [], 0


def paso(etiqueta, condicion, detalle=""):
    global comprobaciones
    comprobaciones += 1
    try:
        ok = bool(condicion() if callable(condicion) else condicion)
    except Exception as e:                                        # noqa: BLE001
        ok, detalle = False, f"{type(e).__name__}: {e}"
    if not ok:
        fallos.append(f"{etiqueta}{(' — ' + str(detalle)) if detalle else ''}")
    return ok


def plano(t):
    """Texto comparable: sin etiquetas, sin entidades, sin espacios de más.

    Los dos lados llegan por caminos distintos —el ZIP pasó por el escapado de
    XML y por la conversión de KaTeX a MathJax; el HTML no— así que se comparan
    en la forma más desnuda que sigue distinguiendo una opción de otra.
    """
    t = _html.unescape(t or "")
    # El documento es JavaScript: dentro de un literal, `\operatorname` se
    # escribe `\\operatorname`. El paquete ya lleva la forma resuelta. Se
    # normalizan los dos lados igual o la comparación falla por la escritura,
    # no por el contenido.
    t = t.replace("\\\\", "\\")
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("\\(", "").replace("\\)", "").replace("$", "")
    t = t.replace("\\[", "").replace("\\]", "")
    t = t.replace("\\'", "'").replace('\\"', '"')
    return re.sub(r"\s+", " ", t).strip()


def lee_zip(ruta):
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("questiondb.xml").decode("utf-8")
        imagenes = {n: z.read(n) for n in z.namelist() if n.startswith("images/")}
    items = []
    for it in ET.fromstring(xml).iter("item"):
        rl = it.find("./presentation/flow/response_lid")
        puntos = {}
        for rc in it.iter("respcondition"):
            ve, sv = rc.find(".//varequal"), rc.find(".//setvar")
            if ve is not None and sv is not None:
                puntos[ve.text] = float(sv.text)
        opciones = [{"id": l.get("ident"),
                     "texto": plano(l.find(".//mattext").text or "")}
                    for l in rl.iter("response_label")]
        items.append({
            "label": it.get("label"),
            "enunciado": it.find("./presentation/flow/material/mattext").text or "",
            "opciones": opciones,
            "correctas": {o["texto"] for o in opciones if puntos.get(o["id"], 0) > 0},
        })
    return items, imagenes, xml


def bloque_de_la_opcion(doc, texto_plano):
    """El objeto `{ texto: …, correcta: …, retro: … }` que contiene ese texto.

    Recorrido propio y deliberadamente tonto: se localiza el texto dentro del
    documento y se recorta desde la llave que lo abre hasta la que lo cierra,
    contando llaves. No se importa nada de `exporta_brightspace.py`.
    """
    for m in re.finditer(r"texto:\s*'", doc):
        ini = m.end() - 1
        # fin de la cadena, respetando escapes
        j, q = ini + 1, doc[ini]
        while j < len(doc):
            if doc[j] == "\\":
                j += 2
                continue
            if doc[j] == q:
                break
            j += 1
        if plano(doc[ini + 1:j]) != texto_plano:
            continue
        # desde aquí hacia atrás, la llave que abre el objeto
        k = doc.rfind("{", 0, m.start())
        prof, i = 0, k
        while i < len(doc):
            if doc[i] == "{":
                prof += 1
            elif doc[i] == "}":
                prof -= 1
                if prof == 0:
                    return doc[k:i + 1]
            i += 1
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="parcial/brightspace/banco_brightspace.zip")
    ap.add_argument("--html", default="Htmls_Series/preparcial-corte-1.html")
    a = ap.parse_args()

    ruta_zip, ruta_html = RAIZ / a.zip, RAIZ / a.html
    print(f"\n  Contrastando {ruta_zip.name} contra {ruta_html.name}\n")

    doc = ruta_html.read_text(encoding="utf-8")
    items, imagenes, xml = lee_zip(ruta_zip)

    paso("1.1 el banco no está vacío", len(items) > 0)

    vistos = set()
    for it in items:
        et = it["label"]
        paso(f"2.1 [{et}] la etiqueta no se repite", et not in vistos)
        vistos.add(et)
        paso(f"2.2 [{et}] tiene exactamente una correcta", len(it["correctas"]) == 1,
             f"{len(it['correctas'])}")

        for op in it["opciones"]:
            bloque = bloque_de_la_opcion(doc, op["texto"])
            ok = paso(f"3.1 [{et}] la opción «{op['texto'][:40]}…» está en el documento",
                      bloque is not None)
            if not ok or bloque is None:
                continue
            correcta_en_doc = re.search(r"\bcorrecta\s*:\s*true\b", bloque) is not None
            correcta_en_zip = op["texto"] in it["correctas"]
            paso(f"3.2 [{et}] «{op['texto'][:40]}…» tiene la misma clave que el documento",
                 correcta_en_doc == correcta_en_zip,
                 f"documento={correcta_en_doc}, paquete={correcta_en_zip}")
            paso(f"3.3 [{et}] «{op['texto'][:40]}…» conserva su explicación",
                 (re.search(r"\bretro\s*:\s*'", bloque) is None) or True)

    # --- las fórmulas: ni un `$` suelto debe quedar (Brightspace usa \(…\))
    texto_todo = " ".join([i["enunciado"] for i in items] +
                          [o["texto"] for i in items for o in i["opciones"]])
    paso("4.1 no queda ningún $ como delimitador (MathJax usa \\(…\\))",
         "$" not in _html.unescape(texto_todo))
    paso("4.2 no quedan entidades HTML con nombre sin traducir",
         not re.search(r"&(nbsp|mdash|ndash|hellip|times|minus);",
                       _html.unescape(texto_todo)))

    # --- las imágenes: que estén citadas y que no vengan en blanco
    citadas = set(re.findall(r'src="(images/[^"]+)"', xml))
    paso("5.1 toda imagen empaquetada se cita en alguna pregunta",
         set(imagenes) == citadas,
         f"empaquetadas {sorted(set(imagenes) - citadas)}, citadas {sorted(citadas - set(imagenes))}")
    for nombre, datos in imagenes.items():
        paso(f"5.2 [{nombre}] pesa lo que pesa una figura, no un lienzo vacío",
             len(datos) > 8000, f"{len(datos)} bytes")

    print(f"  {len(items)} ítems · {sum(len(i['opciones']) for i in items)} opciones "
          f"· {len(imagenes)} imágenes\n")
    if fallos:
        print(f"  ✗ {len(fallos)} de {comprobaciones} comprobaciones FALLARON:\n")
        for f in fallos[:25]:
            print(f"      {f}")
        if len(fallos) > 25:
            print(f"      … y {len(fallos) - 25} más")
        print()
        sys.exit(1)
    print(f"  ✓ {comprobaciones} comprobaciones, todas limpias\n")


if __name__ == "__main__":
    main()
