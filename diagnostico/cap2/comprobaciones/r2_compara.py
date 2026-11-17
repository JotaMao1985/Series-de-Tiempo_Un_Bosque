#!/usr/bin/env python3
"""Compara medidas-antes.json con medidas-despues.json (r2_capturas.js), lienzo a lienzo.

Uso:  python3 diagnostico/cap2/comprobaciones/r2_compara.py [--detalle]

Para cada capítulo dice en cuántos lienzos (× 3 anchos) cambiaron las marcas del eje
x, las del eje y y los textos de la leyenda, y comprueba que NO cambió lo que no debía:
el número de lienzos, sus series (etiqueta y número de puntos) y las rectas de
referencia (valor de la banda). Con --detalle lista cada cambio de marcas.
"""
import json
import sys
from pathlib import Path

R2 = Path(__file__).resolve().parent.parent / "capturas" / "r2"
antes = json.loads((R2 / "medidas-antes.json").read_text(encoding="utf-8"))["caps"]
despues = json.loads((R2 / "medidas-despues.json").read_text(encoding="utf-8"))["caps"]
detalle = "--detalle" in sys.argv


def marcas(c, eje):
    return next((e["ticks"] for e in c["escalas"] if e["id"] == eje), None)


def sin_menos(v):
    return [s.replace("−", "-") for s in (v or [])]


for cap in sorted(antes):
    n = cx = cy = cy_solo_signo = cl = 0
    problemas = []
    lineas = []
    for ancho in antes[cap]["medidas"]:
        for m in antes[cap]["medidas"][ancho]:
            ca = antes[cap]["medidas"][ancho][m]["canv"]
            cd = despues[cap]["medidas"][ancho][m]["canv"]
            if len(ca) != len(cd):
                problemas.append(f"{ancho} M{m}: {len(ca)} lienzos antes, {len(cd)} después")
                continue
            for a, d in zip(ca, cd):
                if "escalas" not in a:
                    continue
                n += 1
                nombre = f"{ancho} M{m} {a['sim']}#{a['i']}"
                # Lo que no debe cambiar: número de series, sus puntos y las rectas
                if [x["n"] for x in a["datasets"]] != [x["n"] for x in d["datasets"]]:
                    problemas.append(f"{nombre}: cambian las series ({[x['n'] for x in a['datasets']]} → {[x['n'] for x in d['datasets']]})")
                ra = [(r["label"], r["valor"]) for r in a.get("rectas", [])]
                rd = [(r["label"], r["valor"]) for r in d.get("rectas", [])]
                if ra != rd and cap != "2":
                    problemas.append(f"{nombre}: cambian las rectas de referencia {ra} → {rd}")
                if [r["valor"] for r in a.get("rectas", [])] != [r["valor"] for r in d.get("rectas", [])]:
                    problemas.append(f"{nombre}: cambia el VALOR de una recta de referencia")
                for eje in "xy":
                    ma, md = marcas(a, eje), marcas(d, eje)
                    if ma != md:
                        if eje == "x":
                            cx += 1
                        else:
                            cy += 1
                            if sin_menos(ma) == sin_menos(md):
                                cy_solo_signo += 1
                        if detalle and sin_menos(ma) != sin_menos(md):
                            lineas.append(f"    {nombre} {a.get('tipo')} {eje}: {' '.join(ma or [])[:70]} → {' '.join(md or [])[:70]}")
                if [i["t"] for i in a["legend"]["items"]] != [i["t"] for i in d["legend"]["items"]]:
                    cl += 1
                    if detalle:
                        lineas.append(f"    {nombre} leyenda: {[i['t'] for i in a['legend']['items']]} → {[i['t'] for i in d['legend']['items']]}")
    print(f"cap{cap}: {n} lienzos × anchos · cambian las marcas del eje x en {cx} · las del eje y en {cy} "
          f"(de ellas, {cy_solo_signo} solo por el signo menos) · textos de leyenda en {cl} · "
          f"lo que no debía cambiar: {'sin cambios' if not problemas else str(len(problemas)) + ' PROBLEMAS'}")
    for p in problemas:
        print("    !! " + p)
    for l in lineas:
        print(l)
