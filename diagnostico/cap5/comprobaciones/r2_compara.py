#!/usr/bin/env python3
"""R2 del cap. 5 · compara el recorrido de humo de los caps. 1 a 6 y la plantilla antes (HEAD, servido
desde `git archive`) y después (árbol de trabajo): r2_recorrido_antes.json frente a
r2_recorrido_despues.json (los escribe r2_recorrido.js; adaptado de diagnostico/cap4/comprobaciones/r2_compara.py).

1. Por capítulo y ancho: eventos de consola, lienzos sin gráfico, módulos con desborde de la página,
   elementos recortados por <main>, solapes y rótulos fuera del lienzo.
2. Fuera del cap. 5: qué cambia en lienzos (aria-label, rótulos de ejes, áreas, leyendas), lecturas,
   tablas y mapas estacionales. En los caps. 2, 3, 4 y 6 no debe cambiar nada; en el 1 y la plantilla,
   solo el mapa.
3. Los mapas estacionales de todas las páginas, antes y después.
"""
import json
import pathlib

import sys
AQUI = pathlib.Path(__file__).parent
# Uso: r2_compara.py [etiqueta_antes etiqueta_después]  (por omisión, antes y despues)
EA, ED = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("antes", "despues")
A = json.loads((AQUI / f"r2_recorrido_{EA}.json").read_text())
D = json.loads((AQUI / f"r2_recorrido_{ED}.json").read_text())


def resumen(J, nombre):
    eventos = [e for e in (J.get("eventos") or []) if "favicon" not in e["txt"]]
    print(f"== {nombre}: eventos de consola {len(J.get('eventos') or [])} ({len(eventos)} sin contar el favicon)")
    for ev in eventos:
        print("   ", ev)
    for cap, anchos in J["r"].items():
        for ancho, dat in anchos.items():
            n = sin = solapes = fuera = desb = rec = 0
            for med in dat["modulos"].values():
                desb += med["docSw"] > med["innerWidth"]
                rec += len(med["recortados"])
                for cv in med["canv"]:
                    n += 1
                    sin += "tipo" not in cv
                    for e in cv.get("escalas", []):
                        solapes += len(e.get("solapes") or [])
                        fuera += len(e.get("fuera") or [])
            print(f"   cap{cap:>9} {ancho:>4}: {len(dat['modulos']):2d} módulos, {n:3d} lienzos, {sin} sin gráfico, "
                  f"{desb} módulos con desborde, {rec} recortados, solapes {solapes}, rótulos fuera {fuera}")


resumen(A, "ANTES (HEAD)")
resumen(D, "DESPUÉS")

print("\n== Lo que cambia fuera del capítulo 5")
for cap in A["r"]:
    if cap == "5":
        continue
    cuenta = {"aria": 0, "rotulos": 0, "areas": 0, "leyendas": 0, "lecturas": 0, "tablas": 0, "mapas": 0}
    ejemplos = []
    for ancho in A["r"][cap]:
        for m in A["r"][cap][ancho]["modulos"]:
            a, d = A["r"][cap][ancho]["modulos"][m], D["r"][cap][ancho]["modulos"][m]
            if len(a["canv"]) != len(d["canv"]):
                ejemplos.append(f"cap{cap} {ancho} M{m}: {len(a['canv'])} lienzos -> {len(d['canv'])}")
            for ca, cd in zip(a["canv"], d["canv"]):
                cuenta["aria"] += ca.get("aria") != cd.get("aria")
                cuenta["areas"] += ca.get("area") != cd.get("area")
                cuenta["leyendas"] += (ca.get("leyenda") or {}) != (cd.get("leyenda") or {})
                for ea, ed in zip(ca.get("escalas", []), cd.get("escalas", [])):
                    if ea.get("rotulos") != ed.get("rotulos"):
                        cuenta["rotulos"] += 1
                        if len(ejemplos) < 8:
                            ejemplos.append(f"cap{cap} {ancho} M{m} {ca.get('sim')}: {ea.get('rotulos')} -> {ed.get('rotulos')}")
            for sa, sd in zip(a["sims"], d["sims"]):
                if (sa.get("lectura") or {}).get("txt") != (sd.get("lectura") or {}).get("txt"):
                    cuenta["lecturas"] += 1
            cuenta["tablas"] += [(t["sw"], t["cw"]) for t in a["tablas"]] != [(t["sw"], t["cw"]) for t in d["tablas"]]
            ma, md = a.get("mapas", []), d.get("mapas", [])
            if ma != md:
                cuenta["mapas"] += 1
    print(f"   cap{cap}: " + ", ".join(f"{k} {v}" for k, v in cuenta.items()))
    for e in ejemplos:
        print("      " + e)

print("\n== Mapas estacionales, antes -> después")
CAMPOS = ("desplaza", "mesesVisibles", "columnas", "filasARIA", "conCifra", "contrasteMin", "bajo45", "desbordan", "guiones")
for cap in A["r"]:
    for ancho in A["r"][cap]:
        for m in A["r"][cap][ancho]["modulos"]:
            ma = A["r"][cap][ancho]["modulos"][m].get("mapas", [])
            md = D["r"][cap][ancho]["modulos"][m].get("mapas", [])
            for x, y in zip(ma, md):
                print(f"   cap{cap} {ancho:>4} M{m} «{x['id']}»")
                print("      antes:   " + " · ".join(f"{k} {x.get(k)}" for k in CAMPOS))
                print("      después: " + " · ".join(f"{k} {y.get(k)}" for k in CAMPOS))
                print(f"      aria antes:   {x.get('aria')!r}")
                print(f"      aria después: {y.get('aria')!r}")
