#!/usr/bin/env python3
"""V3 · Orden (D5): primera aparición de cada término en los módulos M1-M12, antes (HEAD) y después."""
import sys, subprocess, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v3_modulos import lee, modulos, primera_aparicion, RAIZ, HTML

head = subprocess.run(["git", "show", "HEAD:Htmls_Series/capitulo-4-modelos-arima.html"], cwd=RAIZ,
                      capture_output=True, text=True, check=True).stdout
ahora = lee(HTML)
TERMINOS = {
    "Phillips–Perron": r"Phillips.Perron",
    "PP (sigla)": r"\bPP\b",
    "PP.test": r"PP\.test",
    "dos medias": r"dos medias",
    "TRM": r"\bTRM\b",
    "auto.arima": r"auto\.arima",
    "Holt": r"\bHolt\b",
    "suavizamiento exponencial": r"suavizamiento exponencial",
    "0.2544": r"0\.2544",
    "-0.8741": r"0\.8741",
    "ARIMA(1,1,1) ajustado en bloque (arima(Nile, order = c(1, 1, 1))": r"order = c\(1, 1, 1\)",
    "naïve": r"na[ïi]ve",
    "RMSE": r"RMSE",
    "MAE": r"\bMAE\b",
    "abanico": r"abanico",
    "lynx": r"\blynx\b",
    "BJsales": r"BJsales",
    "AirPassengers": r"AirPassengers",
    "fuera de muestra": r"fuera de muestra",
    "airline": r"airline",
    "Shapiro": r"Shapiro",
    "kpss.test|ndiffs": r"ndiffs",
    "stepwise/escalonada": r"escalonad",
    "exhaustiv": r"exhaustiv",
    "deriva": r"\bderiva\b",
    "AICc": r"AICc",
    "n efectivo (n*)": r"n\^\{\*\}|n efectivo|número efectivo",
}
def primeras(h):
    res = {}
    for nombre, pat in TERMINOS.items():
        ap = primera_aparicion(h, pat)
        pr = [a for a in ap if a[2] == 'prosa']
        co = [a for a in ap if a[2] == 'pre']
        res[nombre] = (pr[0] if pr else None, co[0] if co else None, len(ap))
    return res
a, b = primeras(head), primeras(ahora)
print(f"{'término':58s} | {'ANTES prosa':>14s} {'ANTES código':>14s} | {'AHORA prosa':>14s} {'AHORA código':>14s}")
for k in TERMINOS:
    def f(x): return f"M{x[0]}:{x[1]}" if x else "—"
    print(f"{k:58s} | {f(a[k][0]):>14s} {f(a[k][1]):>14s} | {f(b[k][0]):>14s} {f(b[k][1]):>14s}")
print()
for k in ["Phillips–Perron", "PP (sigla)", "dos medias", "TRM", "auto.arima", "Holt", "suavizamiento exponencial", "naïve", "RMSE", "MAE", "abanico", "0.2544"]:
    print("== AHORA, primera prosa de", k, "->", b[k][0])
