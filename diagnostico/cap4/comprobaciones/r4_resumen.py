#!/usr/bin/env python3
"""
r4_resumen.py — las tablas de `diagnostico/cap4/R4_cambios.md`, sacadas del registro

Lee `bibliografia/contraste/cap4.yml`, el HTML ensamblado y `r4_marcas.json` y
escribe en la salida estándar, en Markdown: el recuento por módulo y veredicto,
las citas visibles por obra, una fila por afirmación, los cambios de prosa con
su motivo y las pendientes con su motivo.

Uso:  python3 diagnostico/cap4/comprobaciones/r4_resumen.py > diagnostico/cap4/comprobaciones/r4_resumen.out
"""
import collections
import json
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import r4_lib as L  # noqa: E402

A = L.A
NOMBRE = {"hyndman2021forecasting": "FPP3", "cryer2008time": "Cryer y Chan (2008)", "hamilton1994time": "Hamilton (1994)",
          "rcoreteam2026r": "ayuda de R", "shumway2011time": "Shumway y Stoffer 3.ª", "hyndman2008automatic": "Hyndman y Khandakar (2008)",
          "hyndman2026forecast": "ayuda de forecast", "trapletti2026tseries": "ayuda de tseries",
          "pfaff2024urca": "ayuda de urca"}
V = ("respaldada", "con-matiz", "propia", "pendiente")


def celda(t):
    return " ".join(str(t).split()).replace("|", "\\|")


def main():
    reg = yaml.safe_load((L.RAIZ / "bibliografia/contraste/cap4.yml").read_text("utf-8"))["afirmaciones"]
    lector = A.lee_html((L.RAIZ / "Htmls_Series/capitulo-4-modelos-arima.html").read_text("utf-8"))
    marcas = json.loads((pathlib.Path(__file__).resolve().parent / "r4_marcas.json").read_text("utf-8"))
    por_mod = collections.defaultdict(collections.Counter)
    for e in reg:
        por_mod[int(A.RE_ID.match(e["id"]).group(2))][e["veredicto"]] += 1
    print("### Por módulo\n\n| módulo | afirmaciones | respaldada | con-matiz | propia | pendiente | citas visibles |\n|---|---:|---:|---:|---:|---:|---:|")
    vis = collections.Counter(int(A.RE_ID.match(c.afirma).group(2)) for c in lector.citas)
    for m in sorted(por_mod):
        c = por_mod[m]
        print(f"| M{m} | {sum(c.values())} | " + " | ".join(str(c[v]) for v in V) + f" | {vis[m]} |")
    tot = collections.Counter(e["veredicto"] for e in reg)
    print(f"| **total** | **{len(reg)}** | " + " | ".join(f"**{tot[v]}**" for v in V) + f" | **{len(lector.citas)}** |")
    obra = collections.Counter(c.clave for c in lector.citas)
    print("\n### Citas visibles por obra\n\n| obra | citas visibles | citas literales en el registro |\n|---|---:|---:|")
    lit = collections.Counter(f["clave"] for e in reg for f in e.get("fuentes") or [])
    for k in sorted(lit, key=lambda k: -lit[k]):
        print(f"| {NOMBRE[k]} | {obra[k]} | {lit[k]} |")
    print(f"| **total** | **{sum(obra.values())}** | **{sum(lit.values())}** |")
    print("\n### Una fila por afirmación\n\n| id | tipo | veredicto | afirmación | fuentes (la visible, en negrita) |\n|---|---|---|---|---|")
    visibles = collections.defaultdict(set)
    for c in lector.citas:
        visibles[c.afirma].add((c.clave, c.loc))
    for e in reg:
        fs = []
        for f in e.get("fuentes") or []:
            t = f"{NOMBRE[f['clave']]}, {f['loc']}"
            t = f"**{t}**" if (f["clave"], f["loc"]) in visibles[e["id"]] else t
            if t not in fs:
                fs.append(t)
        print(f"| {e['id']} | {e['tipo']} | {e['veredicto']} | {celda(e['afirmacion'])} | {'; '.join(fs) or '—'} |")
    print("\n### Cambios de prosa\n\n| # | afirmación | antes | después | motivo |\n|---:|---|---|---|---|")
    n = 0
    for e in marcas:
        for viejo, nuevo, motivo in e["prosa"]:
            n += 1
            limpia = lambda t: celda(re.sub(r"<[^>]+>", "", L.RE_MARCA.sub("", t)))
            print(f"| {n} | {e['id']} | {limpia(viejo)} | {limpia(nuevo)} | {celda(motivo)} |")
    print("\n### Pendientes\n")
    for e in reg:
        if e["veredicto"] == "pendiente":
            print(f"- **{e['id']}** · {celda(e['afirmacion'])}\n  - motivo: {celda(e['motivo'])}")


if __name__ == "__main__":
    main()
