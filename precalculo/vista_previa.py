#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vista_previa.py — el banco entero en una página, para revisarlo sin importarlo

Material de Series de Tiempo 2026-II (20948).

Los auditores comprueban que el paquete esté bien construido y que diga lo que
dice el preparcial. Ninguno de los dos puede comprobar lo único que queda:
**cómo se lee la pregunta**. Si una fórmula sale en crudo, si un gráfico se
desborda o si una opción quedó con la etiqueta a medias, se ve mirando.

Esta página se genera DESDE EL ZIP, no desde el documento: lo que se revisa es
lo que se va a subir. Las fórmulas se renderizan con el MathJax de Brightspace
y con sus mismos delimitadores, `\\(…\\)`, así que si aquí salen bien, allí
también.

    python3 precalculo/vista_previa.py
    → parcial/brightspace/vista_previa.html  (y las imágenes al lado)
"""
from __future__ import annotations

import argparse
import html as _html
import pathlib
import xml.etree.ElementTree as ET
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent

CABECERA = """<!DOCTYPE html>
<meta charset="utf-8">
<title>Vista previa · banco de Brightspace</title>
<script>window.MathJax = { tex: { inlineMath: [['\\\\(', '\\\\)']],
                                 displayMath: [['\\\\[', '\\\\]']] } };</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
<style>
  body { font-family: system-ui, -apple-system, sans-serif; max-width: 54rem;
         margin: 2rem auto; padding: 0 1rem; line-height: 1.55; color: #14281f; }
  h1 { font-size: 1.4rem; border-bottom: 3px solid #012820; padding-bottom: .4rem; }
  .item { border: 1px solid #d7dedb; border-radius: .6rem; padding: 1rem 1.2rem;
          margin: 1.2rem 0; }
  .et { font: 600 .78rem/1.2 ui-monospace, monospace; color: #4b6058;
        text-transform: uppercase; letter-spacing: .04em; }
  .tit { font-size: .84rem; color: #4b6058; margin: .15rem 0 .7rem 0; }
  img { max-width: 100%; height: auto; border: 1px solid #e6ebe9; border-radius: .3rem; }
  ol { padding-left: 1.3rem; }
  li { margin: .5rem 0; }
  li.ok { background: #eaf5ef; border-left: 3px solid #1c7a4f; padding: .4rem .6rem;
          border-radius: .25rem; }
  .retro { display: block; font-size: .85rem; color: #4b6058; margin-top: .2rem; }
</style>
<h1>@TITULO@ — @N@ ítems</h1>
<p style="color:#4b6058;font-size:.9rem">Generada desde <code>@ZIP@</code>.
La opción marcada en verde es la que el paquete puntúa con 100.</p>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default="parcial/brightspace/banco_brightspace.zip")
    ap.add_argument("--salida", default="parcial/brightspace/vista_previa.html")
    a = ap.parse_args()

    ruta = RAIZ / a.zip
    destino = RAIZ / a.salida
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("questiondb.xml").decode("utf-8")
        for n in z.namelist():
            if n.startswith("images/"):
                (destino.parent / n).parent.mkdir(parents=True, exist_ok=True)
                (destino.parent / n).write_bytes(z.read(n))

    raiz = ET.fromstring(xml)
    partes, total = [], 0
    for it in raiz.iter("item"):
        total += 1
        puntos = {}
        for rc in it.iter("respcondition"):
            ve, sv = rc.find(".//varequal"), rc.find(".//setvar")
            if ve is not None and sv is not None:
                puntos[ve.text] = float(sv.text)
        retros = {fb.get("ident"): (fb.findtext(".//mattext") or "") for fb in it.iter("itemfeedback")}
        enlaces = {rc.find(".//varequal").text: rc.find(".//displayfeedback").get("linkrefid")
                   for rc in it.iter("respcondition")
                   if rc.find(".//varequal") is not None and rc.find(".//displayfeedback") is not None}

        enun = it.find("./presentation/flow/material/mattext").text or ""
        filas = []
        for l in it.find("./presentation/flow/response_lid").iter("response_label"):
            oid = l.get("ident")
            texto = l.find(".//mattext").text or ""
            clase = " class=\"ok\"" if puntos.get(oid, 0) > 0 else ""
            retro = retros.get(enlaces.get(oid, ""), "")
            filas.append(f"<li{clase}>{texto}<span class=\"retro\">{retro}</span></li>")

        partes.append(
            f'<div class="item"><div class="et">{_html.escape(it.get("label"))}</div>'
            f'<div class="tit">{_html.escape(it.get("title") or "")}</div>'
            f'{enun}<ol>{"".join(filas)}</ol></div>')

    titulo = raiz.find(".//objectbank").get("ident", "Banco")
    destino.write_text(
        CABECERA.replace("@TITULO@", _html.escape(titulo))
                .replace("@N@", str(total))
                .replace("@ZIP@", ruta.name)
        + "\n".join(partes), encoding="utf-8")
    print(f"\n  {destino.relative_to(RAIZ)}  ({total} ítems)\n")


if __name__ == "__main__":
    main()
