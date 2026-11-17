#!/usr/bin/env python3
"""r4_resumen.py — la tabla «una fila por afirmación» de R4_cambios.md, sacada del registro y del HTML."""
import pathlib
import re
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import audita_citas as A  # noqa: E402

NOMBRE = {"hyndman2021forecasting": "FPP3", "cryer2008time": "Cryer y Chan", "hamilton1994time": "Hamilton",
          "rcoreteam2026r": "ayuda de R"}
html = (RAIZ / "Htmls_Series" / "capitulo-2-estacionariedad-acf-pacf.html").read_text("utf-8")
lector = A.lee_html(html)
registro = yaml.safe_load((RAIZ / "bibliografia" / "contraste" / "cap2.yml").read_text("utf-8"))["afirmaciones"]
visibles = {}
for c in lector.citas:
    visibles.setdefault(c.afirma, []).append((c.clave, c.loc))
print("| id | tipo | veredicto | obra y localizador (en **negrita**, la cita visible) |")
print("|---|---|---|---|")
for x in registro:
    vistos, partes = set(), []
    for f in x.get("fuentes") or []:
        par = (f["clave"], f["loc"])
        if par in vistos:
            continue
        vistos.add(par)
        t = f"{NOMBRE[f['clave']]} {f['loc']}"
        partes.append(f"**{t}**" if par in visibles.get(x["id"], []) else t)
    print(f"| {x['id']} | {x['tipo']} | {x['veredicto']} | {'; '.join(partes) or '—'} |")
por_obra = {}
for c in lector.citas:
    por_obra[NOMBRE[c.clave]] = por_obra.get(NOMBRE[c.clave], 0) + 1
print("\ncitas visibles:", len(lector.citas), "·", ", ".join(f"{k} {v}" for k, v in sorted(por_obra.items())))
por_modulo = {}
for x in registro:
    m = re.match(r"c2-m(\d+)", x["id"]).group(1)
    por_modulo.setdefault(m, {}).setdefault(x["veredicto"], 0)
    por_modulo[m][x["veredicto"]] += 1
for m, v in sorted(por_modulo.items()):
    print(f"M{m}: {sum(v.values())} · " + ", ".join(f"{k} {n}" for k, n in sorted(v.items())))
