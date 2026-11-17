#!/usr/bin/env python3
"""R2b · compara r2b_tablas_head.json con r2b_tablas_ahora.json: recortes de <main>, tablas que
no llenan su contenedor, tablas más estrechas que en HEAD y tablas que se desplazan."""
import json
from pathlib import Path
A = Path(__file__).resolve().parent
H = json.loads((A / "r2b_tablas_head.json").read_text()); N = json.loads((A / "r2b_tablas_ahora.json").read_text())
print("eventos de consola  HEAD:", len(H["eventos"]), " ahora:", len(N["eventos"]))
tot = dict(tablas=0, rec_head=0, rec_ahora=0, nollena_head=0, nollena_ahora=0, mas_estrecha=0, desplaza_ahora=0, ancha_clase=0)
for cap in "23456":
    for w in ("1200", "1024", "900", "800", "375"):
        c = dict(tablas=0, rec_head=0, rec_ahora=0, nollena_head=0, nollena_ahora=0, mas_estrecha=0, desplaza_ahora=0, ancha_clase=0)
        notas = []
        for m in N[cap][w]:
            th, tn = H[cap][w][m], N[cap][w][m]
            assert len(th) == len(tn), (cap, w, m)
            for h, n in zip(th, tn):
                if n.get("oculta") or h.get("oculta"):
                    continue
                c["tablas"] += 1
                c["rec_head"] += h["recorte"] > 0; c["rec_ahora"] += n["recorte"] > 0
                c["nollena_head"] += not h["llena"]; c["nollena_ahora"] += not n["llena"]
                c["desplaza_ahora"] += n["desplaza"]; c["ancha_clase"] += "tabla-ancha" in n["cls"]
                # «más estrecha»: las filas visibles ocupan menos que en HEAD dentro del área
                vis_h = min(h["filas"], h["hueco"] + h["recorte"]) if h["recorte"] else min(h["filas"], max(h["caja"], h["filas"]))
                if n["filas"] < min(h["filas"], h["hueco"]) - 2:
                    c["mas_estrecha"] += 1
                    notas.append(f"    M{m} tabla {n['i']} [{n['cab']}]: filas {h['filas']} → {n['filas']} (hueco {n['hueco']})")
                if n["recorte"] > 0:
                    notas.append(f"    M{m} tabla {n['i']} [{n['cab']}]: <main> la corta {n['recorte']} px")
                if not n["llena"] and h["llena"]:
                    notas.append(f"    M{m} tabla {n['i']} [{n['cab']}]: ya no llena su contenedor (filas {n['filas']}, hueco {n['hueco']})")
        print(f"cap{cap} {w:>4} px · tablas {c['tablas']} · cortadas por <main>: {c['rec_head']} → {c['rec_ahora']} · no llenan su contenedor: "
              f"{c['nollena_head']} → {c['nollena_ahora']} · más estrechas que en HEAD: {c['mas_estrecha']} · con desplazamiento ahora: {c['desplaza_ahora']} (clase tabla-ancha: {c['ancha_clase']})")
        for l in notas:
            print(l)
        for k in tot:
            tot[k] += c[k]
print("TOTAL · " + " · ".join(f"{k} {v}" for k, v in tot.items()))
