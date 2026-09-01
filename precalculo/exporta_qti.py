#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exporta_qti.py — el mismo banco, en IMS QTI 1.2 estándar (sin extensiones)

Material de Series de Tiempo 2026-II (20948).

`exporta_brightspace.py` escribe QTI 1.2 **con las extensiones `d2l_2p0`**, que
es lo que la Biblioteca de Preguntas de Brightspace pide. Este guion escribe el
mismo banco **sin una sola extensión propietaria**: IMS Question & Test
Interoperability 1.2 dentro de un paquete de IMS Content Packaging 1.1.

Para qué sirve cada uno:

    banco_brightspace.zip  → la Biblioteca de Preguntas de Brightspace
    banco_qti12.zip        → cualquier otro sistema que lea QTI 1.2, y el
                             importador genérico de QTI si el de la Biblioteca
                             no traga

Qué cambia respecto del paquete de D2L, y qué no:

  · FUERA: `d2l_2p0:id`, `d2l_2p0:page`, `itemproc_extension`,
    `response_extension` y el `material_type="d2lquestionlibrary"` del
    manifiesto. Son de Desire2Learn y ningún otro sistema los entiende.
  · DENTRO: los ítems van en `assessment > section`, que es la forma que más
    importadores aceptan (el `objectbank` también es QTI 1.2 válido, pero
    varios sistemas solo leen la primera).
  · SE MANTIENE: la retroalimentación por opción. No es una extensión —
    `itemfeedback` enlazado desde `displayfeedback` es QTI 1.2 del manual—, así
    que las 112 explicaciones viajan igual.
  · SE AÑADE: `<outcomes><decvar>`, que D2L no necesita y el estándar sí.

No se ha validado contra la DTD oficial de IMS: no está en esta máquina y no
se descarga nada para construir un examen. Lo que sí se comprueba es que el XML
esté bien formado, que la estructura siga el modelo de elementos de QTI 1.2 y
que **cada opción y cada clave de respuesta coincidan con el paquete de D2L ya
auditado**, que es el contraste que de verdad protege.

    python3 precalculo/exporta_qti.py [--sonda]
"""
from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "precalculo"))

# Se importa el lector del documento en vez de repetirlo: si algún día cambia
# la forma de los ítems, los dos paquetes cambian juntos o ninguno.
from exporta_brightspace import (CAPITULOS, LETRA, NOMBRE_BLOQUE,  # noqa: E402
                                 carga_d2l, construye, lee_capitulo, lee_documento)

QTI_NS = "http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
CP_NS = "http://www.imsglobal.org/xsd/imscp_v1p1"


def esc(t):
    """Contenido: se deja la comilla, que dentro de un `<mattext>` es texto."""
    return html.escape(t or "", quote=False)


def esc_attr(t):
    return html.escape(str(t if t is not None else ""), quote=True)


def item_qti(qid, titulo, enunciado_html, opciones):
    """Un `<item>` de QTI 1.2, sin una sola extensión."""
    lid = f"{qid}_RESP"
    etiquetas, condiciones, retros = [], [], []

    for i, op in enumerate(opciones):
        aid = f"{qid}_A{i + 1}"
        fid = f"{qid}_F{i + 1}"
        etiquetas.append(
            f'<response_label ident="{aid}">'
            f'<material><mattext texttype="text/html">{esc(op["texto"])}</mattext></material>'
            f"</response_label>"
        )
        condiciones.append(
            f'<respcondition title="{esc_attr("Opción %d" % (i + 1))}" continue="No">'
            f'<conditionvar><varequal respident="{lid}">{aid}</varequal></conditionvar>'
            f'<setvar varname="SCORE" action="Set">'
            f'{"100" if op.get("correcta") else "0"}</setvar>'
            f'<displayfeedback feedbacktype="Response" linkrefid="{fid}"/>'
            f"</respcondition>"
        )
        retros.append(
            f'<itemfeedback ident="{fid}" view="Candidate">'
            f'<flow_mat><material>'
            f'<mattext texttype="text/html">{esc(op.get("retro", ""))}</mattext>'
            f"</material></flow_mat></itemfeedback>"
        )

    return (
        f'<item ident="{esc_attr(qid)}" title="{esc_attr(titulo)}">'
        f"<itemmetadata><qtimetadata>"
        f"<qtimetadatafield><fieldlabel>qmd_questiontype</fieldlabel>"
        f"<fieldentry>Multiple Choice</fieldentry></qtimetadatafield>"
        f"<qtimetadatafield><fieldlabel>qmd_computerscored</fieldlabel>"
        f"<fieldentry>Yes</fieldentry></qtimetadatafield>"
        f"</qtimetadata></itemmetadata>"
        f"<presentation>"
        f'<material><mattext texttype="text/html">{esc(enunciado_html)}</mattext></material>'
        f'<response_lid ident="{lid}" rcardinality="Single" rtiming="No">'
        f'<render_choice shuffle="Yes">{"".join(etiquetas)}</render_choice>'
        f"</response_lid></presentation>"
        f"<resprocessing><outcomes>"
        f'<decvar varname="SCORE" vartype="Decimal" defaultval="0" '
        f'minvalue="0" maxvalue="100"/>'
        f'</outcomes>{"".join(condiciones)}</resprocessing>'
        f'{"".join(retros)}'
        f"</item>"
    )


def documento_qti(items_xml, titulo, ident):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<questestinterop xmlns="{QTI_NS}">\n'
        f'  <assessment ident="{ident}" title="{esc_attr(titulo)}">\n'
        f'    <section ident="{ident}_S1">\n'
        f'      {"".join(items_xml)}\n'
        f"    </section>\n  </assessment>\n</questestinterop>\n"
    )


def manifiesto_cp(titulo, ident, rutas_imagenes):
    archivos = '<file href="questestinterop.xml"/>' + "".join(
        f'<file href="{esc_attr(r)}"/>' for r in rutas_imagenes)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<manifest identifier="{ident}_MANIFEST" xmlns="{CP_NS}"\n'
        '          xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_rootv1p2p1">\n'
        "  <metadata>\n"
        "    <schema>IMS Content</schema>\n    <schemaversion>1.1.3</schemaversion>\n"
        "    <imsmd:lom><imsmd:general><imsmd:title>\n"
        f'      <imsmd:langstring xml:lang="es-CO">{esc(titulo)}</imsmd:langstring>\n'
        "    </imsmd:title></imsmd:general></imsmd:lom>\n"
        "  </metadata>\n"
        "  <organizations/>\n"
        "  <resources>\n"
        f'    <resource identifier="{ident}_RES" type="imsqti_xmlv1p2" '
        f'href="questestinterop.xml">\n'
        f"      {archivos}\n    </resource>\n"
        "  </resources>\n</manifest>\n"
    )


def escribe(ruta, items_xml, imagenes, titulo, ident):
    ruta = pathlib.Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    def entrada(nombre):
        info = zipfile.ZipInfo(nombre, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        return info

    a_ascii = lambda s: s.encode("ascii", "xmlcharrefreplace")   # noqa: E731
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(entrada("imsmanifest.xml"),
                   a_ascii(manifiesto_cp(titulo, ident, sorted(imagenes))))
        z.writestr(entrada("questestinterop.xml"),
                   a_ascii(documento_qti(items_xml, titulo, ident)))
        for nombre in sorted(imagenes):
            z.writestr(entrada(nombre), imagenes[nombre])
    return ruta.stat().st_size


def main():
    ap = argparse.ArgumentParser(description="Preparcial del Corte I → IMS QTI 1.2 estándar.")
    ap.add_argument("--html", default="Htmls_Series/preparcial-corte-1.html")
    ap.add_argument("--imagenes", default="precalculo/salidas/graficos")
    ap.add_argument("--salida", default="parcial/qti")
    ap.add_argument("--prefijo", default="ST_C1")
    ap.add_argument("--titulo", default="Series de Tiempo · Corte I")
    ap.add_argument("--skill")
    ap.add_argument("--sonda", action="store_true")
    ap.add_argument("--con-pista", action="store_true")
    ap.add_argument("--capitulos", action="store_true")
    a = ap.parse_args()

    d2l = carga_d2l(a.skill)
    items = lee_documento(RAIZ / a.html)
    if a.capitulos:
        for arch, n_cap in CAPITULOS:
            items += lee_capitulo(RAIZ / "Htmls_Series" / arch, n_cap)
    crudos, imagenes, fuera, _ = construye(
        items, RAIZ / a.imagenes, a.prefijo, a.con_pista, d2l)

    if not crudos:
        sys.exit("PARADO: cero ítems.")

    ident = re.sub(r"[^A-Za-z0-9_]", "_", a.prefijo)
    salida = RAIZ / a.salida
    xml_items = [item_qti(c["qid"], c["titulo"], c["enunciado_html"], c["opciones"])
                 for c in crudos]
    zip_banco = salida / "banco_qti12.zip"
    tam = escribe(zip_banco, xml_items, imagenes, a.titulo, ident)

    zip_sonda = None
    if a.sonda:
        pick = [next(c for c in crudos if c["_tipo"] == "opcion"),
                next(c for c in crudos if c["_tipo"] == "grafico")]
        img = {r: b for r, b in imagenes.items()
               if any(r in c["enunciado_html"] for c in pick)}
        zip_sonda = salida / "sonda_qti12.zip"
        escribe(zip_sonda, [item_qti(c["qid"], c["titulo"], c["enunciado_html"], c["opciones"])
                            for c in pick], img, a.titulo + " · sonda", ident + "_SONDA")

    print(f"\n  IMS QTI 1.2 estándar (sin extensiones propietarias)")
    print(f"  Banco: {zip_banco.relative_to(RAIZ)}  ({tam // 1024} KB)")
    if zip_sonda:
        print(f"  Sonda: {zip_sonda.relative_to(RAIZ)}")
    print(f"\n  {len(crudos)} ítems · "
          f"{sum(len(c['opciones']) for c in crudos)} opciones · "
          f"{len(imagenes)} imagen(es) · {len(fuera)} numéricas fuera")
    print(f"\n  Contrasta contra el paquete de D2L antes de subirlo:\n"
          f"      python3 precalculo/verifica_qti.py\n")


if __name__ == "__main__":
    main()
