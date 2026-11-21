#!/usr/bin/env python3
"""R2 del cap. 3 · resumen de r2_medidas.json (lo que midió r2_revisa.js en cada estado de cada
simulador a 1200, 800 y 375 px): datos no finitos, series constantes, área de dibujo mínima,
marcas de los ejes de dispersión, puntos recortados, aria-label y lecturas con guion."""
import json, pathlib, re, math
J = json.loads((pathlib.Path(__file__).parent / "r2_medidas.json").read_text())
print("eventos de consola (sin el favicon):", [e for e in (J["eventos"] or []) if "favicon" not in e["txt"]])
for ancho, estados in J["estados"].items():
    nan = const = guion = vacios = recorte = 0
    area_min = (1e9, "")
    arias = {}
    for clave, e in estados.items():
        if re.search(r"(^|[\s(=,:;±])-\d", e.get("lectura") or ""):
            guion += 1; print("   guion en la lectura:", ancho, clave, e["lectura"][:120])
        for k, g in enumerate(e["graficos"]):
            if "area" not in g: continue
            if g["area"]["h"] < area_min[0]: area_min = (g["area"]["h"], f"{clave} lienzo {k}")
            arias.setdefault((clave.split(":")[0], k), set()).add(g["aria"])
            visibles = [d for d in g["datasets"] if d.get("label")]
            if not any(d["n"] for d in visibles): vacios += 1; print("   lienzo sin datos:", ancho, clave, k)
            for d in g["datasets"]:
                datos = d.get("datos")
                if datos and any(isinstance(v, float) and not math.isfinite(v) for v in datos) or (datos and any(v is None for v in datos) and d.get("type") == "bar"):
                    nan += 1; print("   dato no finito:", ancho, clave, k, d["label"])
                r = d.get("rango")
                if r and d["n"] > 20 and r[0] == r[1] and d.get("type") != "line" and d.get("label") not in ("",):
                    const += 1; print("   serie constante:", ancho, clave, k, d["label"], r)
            for p in g.get("puntos", []):
                if any(p.get("recorte", [])) and p["label"] in ("θ", "1/θ", "(φ₁, φ₂)"):
                    recorte += 1
    fijos = [k for k, v in arias.items() if len(v) == 1 and len([c for c in estados if c.startswith(k[0] + ":")]) > 1]
    print(f"{ancho}: {len(estados)} estados; datos no finitos {nan}; series constantes {const}; lienzos sin datos {vacios}; "
          f"lecturas con guion {guion}; área mínima {area_min[0]} px ({area_min[1]}); "
          f"puntos a menos de su radio del borde (ahora con clip: false) {recorte}")
    print("   lienzos cuyo aria-label no cambia entre estados:", fijos or "ninguno")
    for sim, est in (("triangulo-ar2", "inicial"), ("rho1-theta-ma1", "inicial")):
        g = estados[f"{sim}:{est}"]["graficos"][0]
        print(f"   {sim}: " + " | ".join(f"{s['id']}: {' '.join(s['ticks'])}" for s in g["escalas"]))
for clave in ("triangulo-ar2:fuera-max-2.2-1.2", "triangulo-ar2:fuera-min-2.2-1.2", "laboratorio-arma:phi1-1.5",
              "laboratorio-arma:max-todo", "laboratorio-arma:phi1-1.0", "dualidad-psi-pi:theta1-frontera",
              "dualidad-psi-pi:theta2-phi0.95", "teorica-vs-muestral:ma1_pos", "diagnostico-residuales:arma10",
              "diagnostico-residuales:arma20"):
    e = J["estados"]["1200"][clave]
    print("\n" + clave + "\n  lectura:", e["lectura"])
    for g in e["graficos"]:
        print("  aria:", g["aria"])
        print("  leyenda:", g["legend"]["items"], "· área", g["area"])
