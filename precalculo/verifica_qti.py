#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifica_qti.py — que el paquete QTI estándar diga lo mismo que el de D2L

Material de Series de Tiempo 2026-II (20948).

El paquete de Brightspace ya pasó dos auditorías: la de la skill (que mira el
ZIP por dentro) y `audita_brightspace.py` (que lo contrasta contra el documento
publicado). El paquete QTI estándar sale del mismo lector, pero por un
serializador distinto, y ese serializador puede equivocarse solo: cambiar de
sitio una clave de respuesta, perder una explicación, dejar un enlace de
retroalimentación colgando.

Así que no se vuelve a auditar contra el documento —eso ya está hecho— sino
contra **el paquete que ya está auditado**. Si los dos coinciden ítem a ítem,
opción a opción y clave a clave, lo que se demostró del primero vale para el
segundo.

Y aparte, lo que es propio del estándar: que no quede ni rastro de las
extensiones de Desire2Learn, que la estructura siga el modelo de elementos de
QTI 1.2 y que cada `displayfeedback` apunte a un `itemfeedback` que existe.

    python3 precalculo/verifica_qti.py

Devuelve 1 si algo no cuadra.
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
QTI_NS = "{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}"

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
    t = re.sub(r"<[^>]+>", " ", _html.unescape(t or ""))
    return re.sub(r"\s+", " ", t).strip()


def lee_d2l(ruta):
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("questiondb.xml").decode("utf-8")
        imgs = {n: z.read(n) for n in z.namelist() if n.startswith("images/")}
    items = {}
    for it in ET.fromstring(xml).iter("item"):
        puntos = {}
        for rc in it.iter("respcondition"):
            ve, sv = rc.find(".//varequal"), rc.find(".//setvar")
            if ve is not None and sv is not None:
                puntos[ve.text] = float(sv.text)
        ops = [(l.get("ident"), plano(l.find(".//mattext").text)) for l in it.iter("response_label")]
        items[it.get("label")] = {
            "enunciado": plano(it.find("./presentation/flow/material/mattext").text),
            "textos": [t for _, t in ops],
            "correctas": {t for i, t in ops if puntos.get(i, 0) > 0},
        }
    return items, imgs


def lee_qti(ruta):
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        manifiesto = z.read("imsmanifest.xml").decode("utf-8")
        xml = z.read("questestinterop.xml").decode("utf-8")
        imgs = {n: z.read(n) for n in nombres if n.startswith("images/")}
    raiz = ET.fromstring(xml)
    items = {}
    for it in raiz.iter(f"{QTI_NS}item"):
        puntos, enlaces = {}, {}
        for rc in it.iter(f"{QTI_NS}respcondition"):
            ve = rc.find(f".//{QTI_NS}varequal")
            sv = rc.find(f".//{QTI_NS}setvar")
            df = rc.find(f".//{QTI_NS}displayfeedback")
            if ve is not None and sv is not None:
                puntos[ve.text] = float(sv.text)
                if df is not None:
                    enlaces[ve.text] = df.get("linkrefid")
        ops = [(l.get("ident"), plano(l.find(f".//{QTI_NS}mattext").text))
               for l in it.iter(f"{QTI_NS}response_label")]
        retros = {fb.get("ident"): plano(fb.find(f".//{QTI_NS}mattext").text)
                  for fb in it.iter(f"{QTI_NS}itemfeedback")}
        pres = it.find(f"{QTI_NS}presentation")
        items[it.get("ident")] = {
            "enunciado": plano(pres.find(f"{QTI_NS}material/{QTI_NS}mattext").text),
            "textos": [t for _, t in ops],
            "correctas": {t for i, t in ops if puntos.get(i, 0) > 0},
            "enlaces": enlaces, "retros": retros,
            "rcard": pres.find(f".//{QTI_NS}response_lid").get("rcardinality"),
            "shuffle": pres.find(f".//{QTI_NS}render_choice").get("shuffle"),
            "decvar": it.find(f".//{QTI_NS}outcomes/{QTI_NS}decvar") is not None,
        }
    return items, imgs, xml, manifiesto, raiz, nombres


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qti", default="parcial/qti/banco_qti12.zip")
    ap.add_argument("--d2l", default="parcial/brightspace/banco_brightspace.zip")
    a = ap.parse_args()

    rq, rd = RAIZ / a.qti, RAIZ / a.d2l
    print(f"\n  Contrastando {rq.name} contra {rd.name}\n")

    d2l, imgs_d2l = lee_d2l(rd)
    qti, imgs_qti, xml, manifiesto, raiz, nombres = lee_qti(rq)

    # ---------------------------------------------- 1 · el paquete
    paso("1.1 trae imsmanifest.xml", "imsmanifest.xml" in nombres)
    paso("1.2 trae questestinterop.xml", "questestinterop.xml" in nombres)
    paso("1.3 el manifiesto declara el recurso como imsqti_xmlv1p2",
         'type="imsqti_xmlv1p2"' in manifiesto)
    declaradas = set(re.findall(r'<file href="([^"]+)"', manifiesto)) - {"questestinterop.xml"}
    paso("1.4 lo declarado coincide con lo empaquetado", declaradas == set(imgs_qti),
         f"declaradas {sorted(declaradas)} vs en el ZIP {sorted(imgs_qti)}")

    # ---------------------------------------------- 2 · nada propietario
    paso("2.1 no queda ni una extensión d2l_2p0 en el XML", "d2l_2p0" not in xml)
    paso("2.2 ni en el manifiesto", "d2l_2p0" not in manifiesto)
    paso("2.3 no queda ningún itemproc_extension ni response_extension",
         "itemproc_extension" not in xml and "response_extension" not in xml)

    # ---------------------------------------------- 3 · el modelo de QTI 1.2
    paso("3.1 la raíz es questestinterop", raiz.tag == f"{QTI_NS}questestinterop")
    assessment = raiz.find(f"{QTI_NS}assessment")
    paso("3.2 lleva un assessment", assessment is not None)
    paso("3.3 con una section dentro",
         assessment is not None and assessment.find(f"{QTI_NS}section") is not None)
    paso("3.4 todo item cuelga de la section",
         len(raiz.findall(f"{QTI_NS}assessment/{QTI_NS}section/{QTI_NS}item")) == len(qti))

    # ---------------------------------------------- 4 · ítem a ítem
    paso("4.1 los dos paquetes tienen los mismos ítems", set(qti) == set(d2l),
         f"solo en QTI {sorted(set(qti) - set(d2l))}, solo en D2L {sorted(set(d2l) - set(qti))}")

    for et in sorted(set(qti) & set(d2l)):
        q, d = qti[et], d2l[et]
        paso(f"4.2 [{et}] el enunciado es el mismo", q["enunciado"] == d["enunciado"])
        paso(f"4.3 [{et}] las opciones son las mismas", q["textos"] == d["textos"],
             "difieren en texto o en orden")
        paso(f"4.4 [{et}] la clave de respuesta es la misma", q["correctas"] == d["correctas"],
             f"QTI {sorted(q['correctas'])} vs D2L {sorted(d['correctas'])}")
        paso(f"4.5 [{et}] una sola correcta", len(q["correctas"]) == 1)
        paso(f"4.6 [{et}] declara su variable de salida (decvar)", q["decvar"])
        paso(f"4.7 [{et}] es de respuesta única y baraja",
             q["rcard"] == "Single" and q["shuffle"] == "Yes",
             f"{q['rcard']} / shuffle={q['shuffle']}")
        idents, enlazados = set(q["retros"]), set(q["enlaces"].values())
        paso(f"4.8 [{et}] todo enlace de retro resuelve", enlazados <= idents,
             f"rotos {sorted(enlazados - idents)}")
        paso(f"4.9 [{et}] toda opción lleva explicación",
             all(q["retros"].get(f, "") for f in q["enlaces"].values()))

    # ---------------------------------------------- 5 · las imágenes
    paso("5.1 las imágenes son las mismas que las del paquete auditado",
         imgs_qti == imgs_d2l,
         f"{len(imgs_qti)} vs {len(imgs_d2l)}, o el contenido difiere")

    n_ret = sum(1 for q in qti.values() for f in q["enlaces"].values() if q["retros"].get(f))
    print(f"  {len(qti)} ítems · {sum(len(q['textos']) for q in qti.values())} opciones "
          f"· {n_ret} explicaciones · {len(imgs_qti)} imágenes\n")
    if fallos:
        print(f"  ✗ {len(fallos)} de {comprobaciones} comprobaciones FALLARON:\n")
        for f in fallos[:20]:
            print(f"      {f}")
        print()
        sys.exit(1)
    print(f"  ✓ {comprobaciones} comprobaciones, todas limpias\n")


if __name__ == "__main__":
    main()
