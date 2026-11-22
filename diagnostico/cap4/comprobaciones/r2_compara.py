#!/usr/bin/env python3
"""R2 del cap. 4 · compara el recorrido de humo de los capítulos 2 a 6 antes (HEAD) y después
(árbol de trabajo): r2_recorrido_antes.json frente a r2_recorrido_despues.json.

Por capítulo y ancho: errores de consola, lienzos sin gráfico, desbordes de la página, y en cada eje
horizontal de rezagos (categorías «1, 2, 3…») si el 1, el 12 y el 24 llevan número y si algún rótulo
se monta. Después lista qué rótulos de eje, qué lecturas, qué aria-label y qué muestras de leyenda cambian fuera del cap. 4."""
import json, pathlib, re, sys
AQUI = pathlib.Path(__file__).parent
A = json.loads((AQUI / "r2_recorrido_antes.json").read_text())
D = json.loads((AQUI / "r2_recorrido_despues.json").read_text())
ENTERO = re.compile(r"^\d+$")

def ejes_rezago(canv):
    for e in canv.get("escalas", []):
        et = e.get("etiquetas")
        if e.get("horiz") and et and len(et) >= 4 and all(ENTERO.match(x) for x in et) \
                and et[0] == "1" and all(int(et[i + 1]) - int(et[i]) == 1 for i in range(len(et) - 1)):
            yield e

def resumen(J, nombre):
    print(f"== {nombre}: eventos de consola {len(J.get('eventos') or [])}")
    for ev in (J.get("eventos") or []):
        if "favicon" not in ev["txt"]:
            print("   ", ev)
    for cap, anchos in J["r"].items():
        for ancho, dat in anchos.items():
            n = sin = ejes = sin1 = sin12 = sin24 = solapes = fuera = desb = sin0 = 0
            for m, med in dat["modulos"].items():
                desb += med["docSw"] > med["innerWidth"]
                for cv in med["canv"]:
                    n += 1
                    sin += "tipo" not in cv
                    for e in cv.get("escalas", []):
                        solapes += len(e.get("solapes") or [])
                        fuera += len(e.get("fuera") or [])
                        sin0 += e.get("tieneCero") is False
                    for e in ejes_rezago(cv):
                        ejes += 1
                        rot = e["rotulos"]
                        sin1 += "1" not in rot
                        sin12 += len(e["etiquetas"]) >= 12 and "12" not in rot
                        sin24 += len(e["etiquetas"]) >= 24 and "24" not in rot
            print(f"   cap{cap} {ancho:>4}: {n:3d} lienzos, {sin} sin gráfico, {desb} módulos con desborde; "
                  f"ejes de rezagos {ejes:3d}: sin el 1 {sin1:3d}, sin el 12 {sin12}, sin el 24 {sin24}; "
                  f"solapes {solapes}, rótulos fuera del lienzo {fuera}, eje y sin el 0 {sin0}")

resumen(A, "ANTES (HEAD)")
resumen(D, "DESPUÉS")

print("== Lo que cambia fuera del capítulo 4")
for cap in ("2", "3", "5", "6"):
    rot = lect = aria = otros = ley = 0
    ley_ej = []
    ejemplos = []
    for ancho in A["r"][cap]:
        for m in A["r"][cap][ancho]["modulos"]:
            a, d = A["r"][cap][ancho]["modulos"][m], D["r"][cap][ancho]["modulos"][m]
            for ca, cd in zip(a["canv"], d["canv"]):
                if ca.get("aria") != cd.get("aria"):
                    aria += 1
                for ea, ed in zip(ca.get("escalas", []), cd.get("escalas", [])):
                    if ea.get("rotulos") != ed.get("rotulos"):
                        rot += 1
                        if len(ejemplos) < 6:
                            ejemplos.append(f"cap{cap} {ancho} M{m} {ca.get('sim')}: {' '.join(ea['rotulos'])}  ->  {' '.join(ed['rotulos'])}")
                    if (ea.get("min"), ea.get("max")) != (ed.get("min"), ed.get("max")):
                        otros += 1
                if [x.get("label") for x in ca.get("datasets", [])] != [x.get("label") for x in cd.get("datasets", [])] \
                        or ca.get("area") != cd.get("area"):
                    otros += 1
                    if len(ejemplos) < 12:
                        ejemplos.append(f"OTRO cap{cap} {ancho} M{m} {ca.get('sim')}: área {ca.get('area')} -> {cd.get('area')}; "
                                        f"datasets {[x.get('label') for x in ca.get('datasets', [])]} -> {[x.get('label') for x in cd.get('datasets', [])]}")
                la, ld = ca.get("leyenda") or {}, cd.get("leyenda") or {}
                if la.get("estilos") != ld.get("estilos") or la.get("items") != ld.get("items"):
                    ley += 1
                    if len(ley_ej) < 4 and ancho == "1200":
                        ley_ej.append(f"cap{cap} M{m} {ca.get('sim')}: {la.get('items')} {la.get('estilos')} -> {ld.get('items')} {ld.get('estilos')}")
            for sa, sd in zip(a["sims"], d["sims"]):
                ta, td = (sa.get("lectura") or {}).get("txt"), (sd.get("lectura") or {}).get("txt")
                if ta != td:
                    lect += 1
                    if ta is not None and td is not None and ta.replace("-", "−") != td.replace("-", "−"):
                        print(f"   LECTURA DISTINTA (no solo el signo) cap{cap} {ancho} M{m} {sa['sim']}:\n      {ta}\n      {td}")
                    elif len(ejemplos) < 12 and ancho == "1200":
                        ejemplos.append(f"cap{cap} M{m} {sa['sim']} lectura: {td[:150]}")
    print(f"   cap{cap}: ejes con otros rótulos {rot}, lecturas que cambian {lect}, aria-label que cambian {aria}, "
          f"leyendas con otra muestra {ley}, otros cambios (escala, área, rótulos de leyenda) {otros}")
    for e in ley_ej:
        print("      LEYENDA " + e)
    for e in ejemplos:
        print("      " + e)

# ---------------------------------------------------------------------------------------------
# Eje a eje: todos los ejes horizontales de categorías con enteros seguidos (rezagos k, retardos j,
# horizontes h) de los caps. 2 a 6, antes y después. Ninguno puede tener menos rótulos pintados que
# en HEAD ni perder el 12, el 24 o el 36.
print("== Ejes de rezagos y horizontes, uno por uno (rótulos realmente pintados)")
from collections import Counter
peor = 0
for cap in A["r"]:
    for ancho in A["r"][cap]:
        trans = Counter()
        for m in A["r"][cap][ancho]["modulos"]:
            a, d = A["r"][cap][ancho]["modulos"][m], D["r"][cap][ancho]["modulos"][m]
            for ca, cd in zip(a["canv"], d["canv"]):
                for ea, ed in zip(ca.get("escalas", []), cd.get("escalas", [])):
                    et = ea.get("etiquetas")
                    if not (ea.get("horiz") and et and len(et) >= 4 and all(ENTERO.match(x) for x in et)
                            and all(int(et[i + 1]) - int(et[i]) == 1 for i in range(len(et) - 1))):
                        continue
                    if len(et) > 60:
                        continue        # instantes de una serie, no rezagos
                    if cap == "4" and et != ed.get("etiquetas"):
                        continue        # paneles del cap. 4 que esta ronda rehízo (otro eje)
                    ra, rd = ea["rotulos"], ed["rotulos"]
                    pierde = [x for x in ("12", "24", "36") if x in ra and x not in rd]
                    if len(rd) < len(ra) or pierde:
                        # Dos ejes del cap. 4 se rehicieron en esta ronda (la traza y σ_h): antes se pisaban o se
                        # inclinaban y no llegaban al último valor; ahora llevan menos marcas, legibles y con el extremo.
                        if cap == "4" and ca.get("sim") in ("traza-auto-arima", "pesos-psi-sigma") and not pierde:
                            print(f"   REHECHO cap{cap} {ancho} M{m} {ca.get('sim')}: {' '.join(ra)} -> {' '.join(rd)}")
                        else:
                            peor += 1
                            print(f"   PEOR cap{cap} {ancho} M{m} {ca.get('sim')}: {' '.join(ra)} -> {' '.join(rd)} {pierde}")
                    trans[(f"{et[0]}..{et[-1]}", " ".join(ra), " ".join(rd))] += 1
        for (rango, ra, rd), k in sorted(trans.items()):
            print(f"   cap{cap} {ancho:>4} {rango:>6} ×{k:<2} {ra}" + ("   (igual)" if ra == rd else f"   ->   {rd}"))
print(f"ejes que pierden rótulos o un múltiplo de 12: {peor}")
