#!/usr/bin/env python3
"""R2 del cap. 4 · resumen de r2_medidas.json (lo que midió r2_revisa.js en el estado inicial y en
cada estado de cada simulador, a 1200, 800 y 375 px).

Por ancho: consola, datos no finitos, lienzos sin datos, área de dibujo mínima (global y la lista de
lo que queda bajo 110 px), marcadores que quedan cortados por el borde del área (sin `clip: false`),
solapes y rótulos fuera del lienzo en los ejes horizontales, guiones en lugar del signo menos (en
ejes y en lecturas), `aria-label` que no cambian entre estados y leyendas de más de dos renglones.
Después, lo propio de cada simulador: los nueve rótulos del ΔAICc, las cruces y la leyenda de la
traza, las marcas del eje logarítmico de la varianza, el 30 en el eje de σ_h y el máximo del eje de
los ψ.

Uso: python3 diagnostico/cap4/comprobaciones/r2_resumen.py > diagnostico/cap4/comprobaciones/r2_resumen.out
"""
import json
import math
import pathlib
import re

AQUI = pathlib.Path(__file__).parent
J = json.loads((AQUI / "r2_medidas.json").read_text())
MINIMO = 110
GUION = re.compile(r"(^|[\s(=,:;±])-\d")

# (el aviso de getImageData es del arnés, que cuenta los píxeles pintados de cada lienzo; el 404 es el del favicon)
print("eventos de consola (sin el favicon ni el aviso de willReadFrequently del arnés):",
      [e for e in (J["eventos"] or []) if "favicon" not in e["txt"] and "willReadFrequently" not in e["txt"]])
print("eventos totales:", len(J["eventos"] or []), "· de la página, aparte del favicon:",
      sum(1 for e in (J["eventos"] or []) if "favicon" not in e["txt"] and "willReadFrequently" not in e["txt"]))
print("base:", J["base"], J["fecha"])


def finito(v):
    return isinstance(v, (int, float)) and math.isfinite(v)


for ancho, estados in J["estados"].items():
    print(f"\n######## {ancho} px · {len(estados)} estados")
    nan = vacios = cortados = sin_clip = guion_eje = guion_lect = 0
    area_min = (1e9, "")
    bajos = {}
    arias = {}
    ley_largas = {}
    solapes = []
    fuera = []
    en_blanco = []
    for clave, e in estados.items():
        sim = clave.split(":")[0]
        if GUION.search(e.get("lectura") or ""):
            guion_lect += 1
            print("   guion en la lectura:", clave, e["lectura"][:110])
        for k, g in enumerate(e["graficos"]):
            if "area" not in g:
                print("   lienzo sin gráfico:", clave, k)
                continue
            h = g["area"]["h"]
            if h < area_min[0]:
                area_min = (h, f"{clave} lienzo {k}")
            if h < MINIMO:
                bajos[(sim, k)] = min(bajos.get((sim, k), 1e9), h)
            arias.setdefault((sim, k), set()).add(g["aria"])
            if not g.get("pintados"):
                en_blanco.append(f"{clave} lienzo {k}")
            if g["legend"]["lineas"] > 2:
                ley_largas[(clave, k)] = g["legend"]["lineas"]
            visibles = [d for d in g["datasets"] if d.get("label")]
            if not any(d["n"] for d in visibles):
                vacios += 1
                print("   lienzo sin datos:", clave, k)
            for d in g["datasets"]:
                r = d.get("rango")
                if r and (r[0] is None or r[1] is None):
                    nan += 1
                    print("   dato no finito:", clave, k, d["label"])
            for p in g.get("puntos", []):
                ds = next((d for d in g["datasets"] if d["label"] == p["label"] and d.get("clip") is not None), None)
                con_clip_off = ds is not None and ds.get("clip") is False
                if any(p["recorte"]):
                    if con_clip_off:
                        sin_clip += sum(p["recorte"])
                    else:
                        cortados += sum(p["recorte"])
                        print("   marcador cortado por el borde:", clave, k, p["label"], sum(p["recorte"]))
            for s in g["escalas"]:
                if s.get("guion"):
                    guion_eje += 1
                    print("   guion en un eje:", clave, k, s["id"], s["guion"][:4])
                for x in s.get("solapes") or []:
                    solapes.append(f"{clave} lienzo {k}: {x}")
                for x in s.get("fuera") or []:
                    fuera.append(f"{clave} lienzo {k}: {x}")
    fijos = [k for k, v in arias.items() if len(v) == 1 and len([c for c in estados if c.startswith(k[0] + ":")]) > 2]
    print(f"datos no finitos {nan}; lienzos sin datos {vacios}; marcadores cortados {cortados} "
          f"(con clip: false, sobre el borde y enteros: {sin_clip}); guiones en ejes {guion_eje}, en lecturas {guion_lect}")
    print(f"área de dibujo mínima: {area_min[0]} px ({area_min[1]})")
    print(f"lienzos con alguna área < {MINIMO} px:", {f"{k[0]}#{k[1]}": v for k, v in bajos.items()} or "ninguno")
    print(f"lienzos en blanco al medir (sin un solo píxel pintado): {len(en_blanco)}", en_blanco[:6])
    print("lienzos cuyo aria-label no cambia entre estados:", [f"{k[0]}#{k[1]}" for k in fijos] or "ninguno")
    print(f"leyendas de más de 2 renglones: {len(ley_largas)}", sorted(set(f"{c.split(':')[0]}#{k}={n}" for (c, k), n in ley_largas.items())))
    print(f"solapes de rótulos en ejes horizontales: {len(solapes)}", solapes[:6])
    print(f"rótulos fuera del lienzo: {len(fuera)}", fuera[:6])

    # ---------------- lo propio de cada simulador
    print("-- explorador-modelos, ΔAICc: rótulos pintados por estado")
    malos = 0
    for clave, e in estados.items():
        if not clave.startswith("explorador-modelos:pdq"):
            continue
        g = e["graficos"][1]
        if "escalas" not in g:
            continue
        # a 1200 los rótulos van en el eje x; tumbado (800/375), en el y
        horiz = next(s for s in g["escalas"] if s["id"] == "x")
        vert = next(s for s in g["escalas"] if s["id"] == "y")
        rot = horiz["ticks"] if any("(" in t for t in horiz["ticks"]) else vert["ticks"]
        n_barras = g["datasets"][0]["n"]
        # los rótulos de dos renglones salen con una coma al aplanar la lista de Chart.js; se cuentan los modelos
        modelos = [t for t in rot if re.match(r"^\(\d,\d,\d\)", t)]
        if len(modelos) != n_barras:
            malos += 1
            print(f"   {clave}: {len(modelos)} rótulos para {n_barras} barras: {rot}")
    print(f"   estados con menos rótulos que barras: {malos} de {sum(1 for c in estados if c.startswith('explorador-modelos:pdq'))}")
    e = estados["explorador-modelos:pdq020"]["graficos"][1]
    print("   (0,2,0): rótulos x:", next(s for s in e["escalas"] if s["id"] == "x")["ticks"], "| y:", next(s for s in e["escalas"] if s["id"] == "y")["ticks"][:12])
    print("   leyenda:", e["legend"]["items"], e["legend"]["colores"], "· aria:", e["aria"])
    for k in ("pdq000", "pdq111", "pdq122"):
        g = estados[f"explorador-modelos:{k}"]["graficos"][1]
        print(f"   {k}: leyenda {g['legend']['items']} {g['legend']['colores']} (renglones {g['legend']['lineas']})")

    print("-- traza-auto-arima")
    for k in ("paso1", "paso18", "exh-paso1", "exh-paso21", "exh-paso42"):
        g = estados[f"traza-auto-arima:{k}"]["graficos"][0]
        yy = next(s for s in g["escalas"] if s["id"] == "y")
        xx = next(s for s in g["escalas"] if s["id"] == "x")
        cruces = [p for p in g.get("puntos", []) if p["label"] and "∞" in p["label"]]
        print(f"   {k}: leyenda {g['legend']['items']} estilos {g['legend']['estilos']} colores {g['legend']['colores']} ({g['legend']['lineas']} renglones)")
        print(f"       y: {' '.join(yy['ticks'])} · x: {' '.join(xx['ticks'])} · inclinación sin solapes: {xx.get('solapes')} · cruces {[ (len(p['px']), sum(p['recorte'])) for p in cruces]}")
        print(f"       aria: {g['aria']}")

    print("-- sobrediferenciacion, varianza")
    for k in ("d0", "d1", "d3"):
        g = estados[f"sobrediferenciacion:{k}"]["graficos"][1]
        yy = next(s for s in g["escalas"] if s["id"] == "y")
        print(f"   {k}: y {' · '.join(yy['ticks'])} ({yy['min']}..{yy['max']}); leyenda {g['legend']['items']} {g['legend']['colores']}")
    print("-- pesos-psi-sigma")
    for k in ("h1", "h30"):
        gp, gs = estados[f"pesos-psi-sigma:{k}"]["graficos"]
        yp = next(s for s in gp["escalas"] if s["id"] == "y")
        xs = next(s for s in gs["escalas"] if s["id"] == "x")
        print(f"   {k}: ψ y {yp['ticks']} ({yp['min']}..{yp['max']}) · σ_h x {xs['ticks']} · áreas {gp['area']['h']} / {gs['area']['h']} px")
        print(f"       marcadores σ_h: {[ (p['recorte'], p['px']) for p in gs.get('puntos', [])]}")
    print("-- forma-pronostico")
    for k in ("d0", "d1", "d1_deriva", "d2", "d2-sin-bandas"):
        e = estados[f"forma-pronostico:{k}"]
        g = e["graficos"][0]
        xx = next(s for s in g["escalas"] if s["id"] == "x")
        yy = next(s for s in g["escalas"] if s["id"] == "y")
        print(f"   {k}: leyenda {g['legend']['items']} {g['legend']['estilos']} ({g['legend']['lineas']} renglones, área {g['area']['h']}) · x {' '.join(xx['ticks'])} solapes {xx.get('solapes')}")
        print(f"       y {' '.join(yy['ticks'])}")
        print(f"       lectura: {e['lectura']}")
    print("-- TRM")
    for k in ("trm-identificacion:d0", "trm-identificacion:d1", "trm-abanico:h1", "trm-abanico:h36"):
        e = estados[k]
        for g in e["graficos"]:
            if g["tipo"] != "line":
                continue
            xx = next(s for s in g["escalas"] if s["id"] == "x")
            print(f"   {k}: x {' '.join(xx['ticks'])} solapes {xx.get('solapes')}; y {' '.join(next(s for s in g['escalas'] if s['id']=='y')['ticks'])}; leyenda {g['legend']['items']} ({g['legend']['lineas']})")
    print("-- aria-label, un ejemplo por lienzo (estado inicial y un extremo)")
    for clave in ("nilo-y-diferencia:d2", "escalon-vs-raiz:beta250", "identificacion-nilo:d0", "explorador-modelos:pdq122",
                  "explorador-modelos:pdq202", "sobrediferenciacion:d2", "forma-pronostico:d2", "pesos-psi-sigma:h15",
                  "trm-identificacion:d1", "trm-abanico:h36", "puente-estacional:si"):
        for k, g in enumerate(estados[clave]["graficos"]):
            print(f"   {clave} #{k}: {g['aria']}")
