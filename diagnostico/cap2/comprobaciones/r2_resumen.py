#!/usr/bin/env python3
"""Resume las medidas de r2_capturas.js (capturas/r2/medidas-<etiqueta>.json).

Uso:  python3 diagnostico/cap2/comprobaciones/r2_resumen.py <etiqueta> [--detalle]

Cuenta, por capítulo y ancho: desbordes de la página, elementos que <main> corta
sin barra, fórmulas en bloque que desbordan, correlogramas sin el 12 o sin el 24
rotulados, ejes verticales que cruzan el 0 sin rotularlo, rótulos del eje x
pisados o fuera del lienzo, leyendas cortadas y lecturas sin aria-live.
Con --detalle escribe además una línea por lienzo con sus marcas.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R2 = AQUI.parent / "capturas" / "r2"
etiqueta = next((a for a in sys.argv[1:] if not a.startswith("--")), "despues")
detalle = "--detalle" in sys.argv
datos = json.loads((R2 / f"medidas-{etiqueta}.json").read_text(encoding="utf-8"))

print(f"# medidas-{etiqueta}.json · {datos['fecha']}")
total = {}
for cap, d in sorted(datos["caps"].items()):
    for ancho, mods in d["medidas"].items():
        cuenta = dict(lienzos=0, correlogramas=0, sin12o24=0, sin_cero=0, pisados=0, fuera=0,
                      leyenda_cortada=0, leyenda_3_lineas=0, desborde_pagina=0, recortados=0,
                      formulas=0, formulas_sin_pista=0, lecturas=0, lecturas_sin_live=0,
                      tablas_cortadas=0)
        lineas = []
        for n, m in sorted(mods.items(), key=lambda kv: int(kv[0])):
            if m["docSw"] > m["innerWidth"]:
                cuenta["desborde_pagina"] += 1
                lineas.append(f"    M{n}: la página mide {m['docSw']} px en una ventana de {m['innerWidth']}")
            cuenta["recortados"] += len(m["recortados"])
            for r in m["recortados"]:
                lineas.append(f"    M{n}: cortado por <main> · {r['tag']}.{r['cls']} sobra {r['sobra']} px · {r['txt']}")
            cuenta["formulas"] += len(m["katex"])
            for k in m["katex"]:
                if not k.get("pista"):
                    cuenta["formulas_sin_pista"] += 1
                    lineas.append(f"    M{n}: fórmula en bloque que desborda sin pista ({k['sw']} en {k['cw']}, en .{k['dentro']}) · {k['txt']}")
            for t in m["tablas"]:
                if t["fuera"] > 1 and t["ox"] not in ("auto", "scroll"):
                    cuenta["tablas_cortadas"] += 1
            for s in m["sims"]:
                if s["lectura"]:
                    cuenta["lecturas"] += 1
                    if not s["lectura"]["ariaLive"]:
                        cuenta["lecturas_sin_live"] += 1
            for c in m["canv"]:
                if "escalas" not in c:
                    continue
                cuenta["lienzos"] += 1
                ex = next((e for e in c["escalas"] if e["id"] == "x"), None)
                ey = next((e for e in c["escalas"] if e["id"] == "y"), None)
                nombre = f"M{n} {c['sim'] or 'suelto'}#{c['i']}"
                if ex and c.get("tipo") == "bar" and ex.get("title") and "ezago" in (ex["title"] or ""):
                    cuenta["correlogramas"] += 1
                    faltan = [k for k in ("12", "24") if k not in ex["ticks"] and ex["max"] >= int(k) - 1]
                    if faltan:
                        cuenta["sin12o24"] += 1
                        lineas.append(f"    {nombre}: correlograma sin {' ni '.join(faltan)} · marcas: {' '.join(ex['ticks'])}")
                if ex and ex.get("solapes"):
                    cuenta["pisados"] += 1
                    lineas.append(f"    {nombre}: rótulos del eje x a menos de 3 px · {'; '.join(ex['solapes'][:3])}")
                if ex and ex.get("fuera"):
                    cuenta["fuera"] += 1
                    lineas.append(f"    {nombre}: rótulos del eje x fuera del lienzo · {ex['fuera']}")
                if ey and ey.get("cruzaCero") and not ey.get("tieneCero"):
                    cuenta["sin_cero"] += 1
                    lineas.append(f"    {nombre}: el eje y cruza el 0 y no lo rotula · {' '.join(ey['ticks'])}")
                if c["legend"]["cortada"]:
                    cuenta["leyenda_cortada"] += 1
                    lineas.append(f"    {nombre}: leyenda más ancha que el lienzo · {[i['t'] for i in c['legend']['items']]}")
                if c["legend"]["lineas"] >= 3:
                    cuenta["leyenda_3_lineas"] += 1
                if detalle:
                    ley = ", ".join(f"{i['t']}[{i['ps'] or 'caja'}]" for i in c["legend"]["items"])
                    print(f"  cap{cap} {ancho} {nombre} {c.get('tipo')} · x: {' '.join(ex['ticks']) if ex else '—'}"
                          f" · y: {' '.join(ey['ticks']) if ey else '—'} · leyenda: {ley}")
        print(f"\ncap{cap} · {ancho} px · " + " · ".join(f"{k} {v}" for k, v in cuenta.items()))
        for l in lineas:
            print(l)
        for k, v in cuenta.items():
            total[k] = total.get(k, 0) + v
    ev = d.get("eventos") or []
    print(f"\ncap{cap} · consola (sin el 404 del favicon): {len(ev)} eventos")
    for e in ev[:10]:
        print(f"    {e['cuando']}: {e['txt'][:200]}")

print("\n# total · " + " · ".join(f"{k} {v}" for k, v in total.items()))
