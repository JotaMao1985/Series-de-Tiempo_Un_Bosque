#!/usr/bin/env python3
"""
verifica_excel_cap5.py — comprueba los dos libros del ejercicio del capítulo 5

Material de Series de Tiempo 2026-II (20948), Universidad El Bosque.

Tres capas, cada una independiente de las demás:

  1. EL ORÁCULO. numpy (y statsmodels y dateutil donde ayudan a no repetir la
     aritmética del generador) recalcula cada resultado del libro a partir de
     las series y lo compara con J (`cap5_sarima.json`) y con el texto del
     capítulo (`ensamblado/cap5/templates_*.html`). Las diferencias entre la
     recursión CSS del libro y la verosimilitud exacta de R se miden aquí y se
     imprimen con su tolerancia.
  2. LO ESTÁTICO. Los libros del disco son los que genera hoy
     `genera_excel_cap5.py` (byte a byte, dos veces seguidas); solo usan
     funciones clásicas; en el del estudiante las celdas clave están vacías y
     en la solución tienen fórmula; los datos de los ejemplos inventados son
     los del capítulo.
  3. EXCEL DE VERDAD. Abre cada libro en Microsoft Excel por AppleScript,
     fuerza `calculate full`, lo guarda y lo lee con openpyxl `data_only`:
       · en la solución, todas las comprobaciones en ✔ (o «—» si están en
         pausa), ningún error salvo los #N/A deliberados de los gráficos, y
         los valores calculados frente al oráculo;
       · en el del estudiante, ✘ exactamente en las comprobaciones que
         dependen de una celda por completar, y el resto como en la solución.

Excel abre una COPIA en un directorio temporal, con `open POSIX file` (así el
sandbox de Excel recibe permiso sobre ese archivo y no pregunta), y cierra solo
esa copia. Si hay otros libros abiertos, no fuerza `calculate full` sobre la
aplicación —que los recalcularía también—: recalcula hoja a hoja la copia.

Uso (desde la raíz del repositorio):
    python3 precalculo/verifica_excel_cap5.py              # las tres capas
    python3 precalculo/verifica_excel_cap5.py --sin-excel  # solo 1 y 2
Sale con 1 si algo falla.
"""

import argparse
import glob
import html
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

import numpy as np
import openpyxl
from dateutil.easter import easter
from scipy import stats
from statsmodels.tsa.arima_process import arma_acf

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "precalculo"))
import genera_excel_cap5 as G  # noqa: E402

D = json.loads((RAIZ / "precalculo/salidas/datos_series.json").read_text(encoding="utf-8"))
J = json.loads((RAIZ / "precalculo/salidas/cap5_sarima.json").read_text(encoding="utf-8"))
CAPITULO = "".join(Path(f).read_text(encoding="utf-8")
                   for f in sorted(glob.glob(str(RAIZ / "ensamblado/cap5/templates_*.html"))))
TEXTO = html.unescape(re.sub(r"<[^>]+>", " ", CAPITULO)).replace("−", "-")

FALLOS = []


def ok(cond, que, detalle=""):
    print(f"  {'ok   ' if cond else 'FALLA'} {que}{('  · ' + detalle) if detalle else ''}")
    if not cond:
        FALLOS.append(que)
    return cond


def en_capitulo(valor, decimales):
    """¿Aparece el número, con esos decimales, en el texto del capítulo?"""
    s = f"{valor:.{decimales}f}"
    return re.search(rf"(?<![\d.]){re.escape(s)}(?!\d)", TEXTO) is not None


# =============================================================== 1. oráculo
def acf(x, kmax):
    x = np.asarray(x, float)
    d = x - x.mean()
    den = float(np.sum(d * d))
    return np.array([float(np.sum(d[:-k] * d[k:])) / den for k in range(1, kmax + 1)])


def oraculo():
    print("\n1 · El oráculo (numpy) frente a J y al capítulo")
    O = {}
    A = J["airpassengers"]
    air = A["airline"]
    th, Th = [c["valor"] for c in air["coeficientes"]]
    ap = np.array(D["airpassengers"]["valores"], float)
    ly = np.log(ap)
    trm = np.array(D["trm"]["valores"], float)
    uad = np.array(D["usaccdeaths"]["valores"], float)
    r4 = lambda a, b: float(np.max(np.abs(np.round(a, 4) - np.asarray(b))))

    # M1
    O["acf_log"] = acf(ly, 36)
    O["acf_dlog"] = acf(np.diff(ly), 36)
    O["acf_trm"] = acf(trm, 36)
    O["acf_dtrm"] = acf(np.diff(trm), 36)
    ok(r4(O["acf_log"], A["firma"]["airpassengers_log"]["acf"]) == 0, "M1: ACF de log y = J (4 decimales)")
    ok(r4(O["acf_dlog"], A["combinaciones"]["d1_D0"]["acf"]) == 0, "M1: ACF de ∇log y = J")
    ok(r4(O["acf_trm"], A["firma"]["trm"]["acf"]) == 0, "M1: ACF de la TRM = J")
    ok(r4(O["acf_dtrm"], A["firma"]["trm_diff"]["acf"]) == 0, "M1: ACF de ∇TRM = J",
       f"ρ̂₁₂ = {O['acf_dtrm'][11]:.5f}: el −0.0025 del capítulo; R con la copia viva da −0.0024")

    # M2
    he = G.EJEMPLOS["heladeria"]
    T = J["teoricas"]["ar1_sar1"]
    phi, Phi = T["phi"], T["Phi"]
    ruta1 = phi * he["feb25"] + Phi * he["mar24"] - phi * Phi * he["feb24"]
    u = he["mar24"] - phi * he["feb24"]
    ruta2 = phi * he["feb25"] + Phi * u
    suma = phi * he["feb25"] + Phi * he["mar24"]
    O["heladeria"] = [u, Phi * u, ruta2, ruta1, suma]
    ok("feb24 <- 15; mar24 <- 20; feb25 <- 10" in html.unescape(CAPITULO), "M2: los datos de la heladería son los del capítulo")
    ok(abs(ruta1 - ruta2) < 1e-12 and en_capitulo(ruta1, 1) and en_capitulo(u, 0) and en_capitulo(suma - ruta1, 1),
       "M2: heladería 11 → 7.7 → 13.7 por las dos rutas; 20 sumando; 6.3 de diferencia")
    poli = np.convolve([1, -phi], np.r_[1, np.zeros(11), -Phi])
    acf_teo = arma_acf(poli, [1], lags=37)[1:]
    O["acf_ar1sar1"] = acf_teo
    ok(r4(acf_teo, T["acf"]) == 0, "M2: ACF teórica del AR(1)×SAR(1) (statsmodels) = J")
    psi = np.zeros(G.N_PSI)
    for j in range(G.N_PSI):
        psi[j] = (j == 0) + (phi * psi[j - 1] if j >= 1 else 0) + (Phi * psi[j - 12] if j >= 12 else 0) \
            - (phi * Phi * psi[j - 13] if j >= 13 else 0)
    O["acf_psi720"] = np.array([psi[:-k] @ psi[k:] / (psi @ psi) for k in range(1, 37)])
    ok(np.max(np.abs(O["acf_psi720"] - acf_teo)) < 1e-9,
       "M2: 720 pesos ψ bastan: ρ_k por Σψψ coincide con la ACF exacta (< 10⁻⁹)")
    for ph in G.PHIS_TABLA:
        p_ = np.zeros(20000)
        for j in range(20000):
            p_[j] = (j == 0) + (ph * p_[j - 1] if j >= 1 else 0) + (Phi * p_[j - 12] if j >= 12 else 0) \
                - (ph * Phi * p_[j - 13] if j >= 13 else 0)
        ex = float(np.sum(p_ * p_))
        fa = 1 / ((1 - ph ** 2) * (1 - Phi ** 2))
        ok(en_capitulo(ex, 3) and en_capitulo(fa, 3), f"M2: γ₀/σ² con φ = {ph}: exacta {ex:.3f} y factorizada {fa:.3f}, las del capítulo")
        if ph == phi:
            O["gamma_exacta"], O["gamma_fact"] = (psi @ psi), fa
    O["b13"] = th * Th
    ok(en_capitulo(th * Th, 4), f"M2: satélite MA del airline θ̂Θ̂ = {th * Th:.4f}, el del capítulo")
    ruido = G.ruido_fijo(G.SIMULACION["n"], G.SIMULACION["semilla"])
    y = np.zeros(G.SIMULACION["n"] + 13)
    for t in range(13, len(y)):
        y[t] = phi * y[t - 1] + Phi * y[t - 12] - phi * Phi * y[t - 13] + ruido[t - 13]
    usados = y[13 + G.SIMULACION["quemado"]:]
    O["sim_suma"] = usados.sum()
    O["acf_sim"] = acf(usados, 36)
    banda = 1.96 / math.sqrt(len(usados))
    ok(O["acf_sim"][10] > banda and O["acf_sim"][12] > banda,
       "M2: en la serie simulada asoman los satélites", f"ρ̂₁₁ = {O['acf_sim'][10]:.3f}, ρ̂₁₃ = {O['acf_sim'][12]:.3f}, banda {banda:.3f}")

    # M3
    t_ = G.EJEMPLOS["tienda"]
    ok("patron <- c(-6, -8, -4, -2, 0, 4, 6, 4, 0, -2, 2, 6)" in html.unescape(CAPITULO)
       and "abre en enero de 2022 con $100$" in CAPITULO,
       "M3: los datos de la tienda son los del capítulo")
    t = np.arange(1, 49)
    pat = np.array(t_["patron"])[(t - 1) % 12]
    y0 = 100 + (t - 1) + pat
    y1 = 100 + np.where(t <= 24, t - 1, 23 + 3 * (t - 24)) + pat
    O["tienda"] = (y0, y1)
    ok("$122 - 110 = 12$" in CAPITULO and y0[26] - y0[14] == 12, "M3: marzo de 2024, 122 − 110 = 12")
    ok("$128 - 121 - 110 + 105 = 2$" in CAPITULO and y1[26] - y1[25] - y1[14] + y1[13] == 2,
       "M3: con aceleración, 128 − 121 − 110 + 105 = 2")
    d12 = lambda x: x[12:] - x[:-12]
    dd = lambda x: np.diff(x)
    w = dd(d12(ly))
    O["w"] = w
    comb = {"d0_D0": ly, "d1_D0": dd(ly), "d0_D1": d12(ly), "d1_D1": w}
    O["comb"] = {}
    for k, s in comb.items():
        cj = A["combinaciones"][k]
        v = s.var(ddof=1)
        a = acf(s, 12)
        O["comb"][k] = (len(s), v, a[0], a[11])
        ok(len(s) == cj["n"] and abs(v - cj["varianza"]) <= 5.1e-7 and abs(a[0] - cj["acf1"]) <= 5.1e-5
           and abs(a[11] - cj["acf12"]) <= 5.1e-5, f"M3: {cj['etiqueta']}: n, varianza, ρ̂₁ y ρ̂₁₂ = J")
    O["var_D2"] = dd(d12(d12(ly))).var(ddof=1)
    ok(abs(O["var_D2"] - A["sobrediferenciacion_estacional"][2]["varianza"]) <= 5e-6 and en_capitulo(O["var_D2"], 6),
       f"M3: con D = 2 la varianza sube a {O['var_D2']:.6f}")
    ok(np.max(np.abs(w - d12(dd(ly)))) < 1e-12, "M3: ∇∇₁₂ = ∇₁₂∇ (diferencia máxima 0)")

    # M4
    O["acf_w"] = acf(w, 36)
    ok(r4(O["acf_w"], A["combinaciones"]["d1_D1"]["acf"]) == 0, "M4: ACF de ∇∇₁₂ log y = J")
    rho1, rho12 = th / (1 + th ** 2), Th / (1 + Th ** 2)
    O["airline_teo"] = (rho1, rho12, rho1 * rho12)
    ma = np.zeros(14)
    ma[0], ma[1], ma[12], ma[13] = 1, th, Th, th * Th
    teo = arma_acf([1], ma, lags=14)
    ok(abs(teo[1] - rho1) < 1e-12 and abs(teo[13] - rho1 * rho12) < 1e-12 and abs(teo[11] - teo[13]) < 1e-12,
       "M4: en el airline ρ₁₁ = ρ₁₃ = ρ₁ρ₁₂ exactamente (statsmodels)")
    ok(en_capitulo(rho1 * rho12, 4) and en_capitulo(rho12, 4),
       f"M4: ρ₁₂ = {rho12:.4f} y ρ₁₁ = ρ₁₃ = {rho1 * rho12:.4f}, los del capítulo",
       f"ρ₁ = {rho1:.5f}: con θ̂ de 4 decimales cae en el empate; el capítulo da −0.3460 con θ̂ completo")
    # PACF por Durbin–Levinson
    r = O["acf_w"]
    phis = [r[0]]
    pacf = [r[0]]
    for k in range(2, 37):
        prev = np.array(phis)
        fkk = (r[k - 1] - prev @ r[k - 2::-1][:k - 1]) / (1 - prev @ r[:k - 1])
        phis = list(prev - fkk * prev[::-1]) + [fkk]
        pacf.append(fkk)
    O["pacf_w"] = np.array(pacf)
    ok(r4(O["pacf_w"], A["combinaciones"]["d1_D1"]["pacf"]) == 0, "M4: PACF por Durbin–Levinson = pacf() de R (J)")

    # M5
    psi_a = np.zeros(36)
    mac = {0: 1, 1: th, 12: Th, 13: th * Th}
    for j in range(36):
        psi_a[j] = mac.get(j, 0) + (psi_a[j - 1] if j >= 1 else 0) + (psi_a[j - 12] if j >= 12 else 0) \
            - (psi_a[j - 13] if j >= 13 else 0)
    sh = np.sqrt(air["sigma2"] * np.cumsum(psi_a ** 2))
    O["psi_air"], O["sigma_h"] = psi_a, sh
    dpsi = float(np.max(np.abs(psi_a[:24] - np.array(A["pronostico"]["psi"]))))
    dsh = float(np.max(np.abs(sh[:24] - np.array(A["pronostico"]["sigma_h"]))))
    ok(dpsi < 1e-4, "M5: ψ_j con θ̂, Θ̂ de 4 decimales frente a J (coeficientes completos)", f"diferencia máxima {dpsi:.2e} ≤ 10⁻⁴")
    ok(dsh < 2e-5, "M5: σ_h con σ̂² = 0.001371 frente a J", f"diferencia máxima {dsh:.2e} ≤ 2·10⁻⁵")
    ok(en_capitulo(sh[0], 4) and en_capitulo(sh[11], 4) and en_capitulo(sh[23], 4) and en_capitulo(sh[11] / sh[0], 2),
       "M5: σ₁ = 0.0370, σ₁₂ = 0.0823, σ₂₄ = 0.1396 y σ₁₂/σ₁ = 2.22, los del capítulo")

    # M6
    e = np.zeros(len(w))
    for k in range(len(w)):
        e[k] = w[k] - (th * e[k - 1] if k >= 1 else 0) - (Th * e[k - 12] if k >= 12 else 0) \
            - (th * Th * e[k - 13] if k >= 13 else 0)
    O["e_css"] = e
    res_r = np.array(air["residuales"])
    dif = np.abs(e - res_r[13:])
    O["dif_css_fin"], O["dif_css_ini"] = dif[-24:].max(), dif[:12].max()

    def lb(x, h, gl):
        n = len(x)
        a = acf(x, h)
        q = n * (n + 2) * np.sum(a ** 2 / (n - np.arange(1, h + 1)))
        return q, stats.chi2.sf(q, gl)
    O["lb_r24"], O["lb_r36"], O["lb_css24"] = lb(res_r, 24, 22), lb(res_r, 36, 34), lb(e, 24, 22)
    dg = air["diagnostico"]
    ok(abs(O["lb_r24"][0] - dg["lb24_Q"]) < 1e-3 and abs(O["lb_r24"][1] - dg["lb24_p"]) < 1e-4,
       "M6: Ljung–Box(24) con los residuales de R = J", f"Q = {O['lb_r24'][0]:.4f}, p = {O['lb_r24'][1]:.4f}")
    ok(abs(O["lb_r36"][0] - dg["lb36_Q"]) < 1e-3 and abs(O["lb_r36"][1] - dg["lb36_p"]) < 1e-4,
       "M6: Ljung–Box(36) con los residuales de R = J")
    ok(O["lb_css24"][1] > 0.05, "M6: con los residuales CSS, la misma conclusión (no rechaza)",
       f"Q = {O['lb_css24'][0]:.2f}, p = {O['lb_css24'][1]:.3f} frente a {dg['lb24_Q']} y {dg['lb24_p']}: "
       "es el arranque en cero del primer año")
    ok(O["dif_css_fin"] < 5e-4, "M6: los residuales CSS alcanzan a los de R al final de la muestra",
       f"|CSS − R| ≤ {O['dif_css_fin']:.1e} en los últimos 24; {O['dif_css_ini']:.3f} en el primer año")
    d_acf = float(np.max(np.abs(acf(res_r, 36) - np.array(dg["acf"]))))
    ok(d_acf < 1e-4, "M6: ACF de los residuales de R = J",
       f"diferencia máxima {d_acf:.1e} ≤ 10⁻⁴: J guarda los residuales con 5 decimales")
    mx = 0
    O["rejilla"] = {}
    for nombre, v in A["rejilla"].items():
        k = v["n_par"] + 1
        aic = -2 * v["loglik"] + 2 * k
        aicc = aic + 2 * k * (k + 1) / (v["nobs"] - k - 1)
        bic = -2 * v["loglik"] + k * math.log(v["nobs"])
        O["rejilla"][nombre] = (aicc, bic)
        mx = max(mx, abs(aicc - v["aicc"]), abs(bic - v["bic"]))
    ok(mx < 1e-3, "M6: AICc y BIC de los 36 modelos desde el log-verosimilitud = J", f"diferencia máxima {mx:.1e}")
    orden = sorted(O["rejilla"], key=lambda n_: O["rejilla"][n_][0])
    ok(orden[:4] == A["mejores_aicc"][:4], "M6: los cuatro mejores por AICc son los del capítulo")

    # M7
    def pron(res):
        yy, ee = list(ly), list(res)
        for _ in range(24):
            T_ = len(yy)
            yy.append(yy[T_ - 1] + yy[T_ - 12] - yy[T_ - 13] + th * ee[T_ - 1] + Th * ee[T_ - 12]
                      + th * Th * ee[T_ - 13])
            ee.append(0.0)
        return np.array(yy[144:])
    O["pron_css"] = pron(np.r_[np.zeros(13), e])
    O["pron_r"] = pron(res_r)
    P = A["pronostico"]
    d_css = float(np.max(np.abs(O["pron_css"] - P["log"]["media"])))
    d_r = float(np.max(np.abs(O["pron_r"] - P["log"]["media"])))
    ok(d_css < 3e-4, "M7: pronóstico en logaritmos con los residuales CSS frente a R", f"diferencia máxima {d_css:.1e} ≤ 3·10⁻⁴")
    ok(d_r < 2e-5, "M7: con los residuales de R", f"diferencia máxima {d_r:.1e}")
    z95 = stats.norm.ppf(0.975)
    O["z"] = (stats.norm.ppf(0.9), z95)
    med, lo, hi = math.exp(O["pron_css"][23]), math.exp(O["pron_css"][23] - z95 * sh[23]), math.exp(O["pron_css"][23] + z95 * sh[23])
    O["m7_24"] = (med, lo, hi, math.exp(O["pron_css"][23] + sh[23] ** 2 / 2))
    ok(abs(med - P["original"]["media"][23]) < 0.2 and abs(lo - P["original"]["lo95"][23]) < 0.2
       and abs(hi - P["original"]["hi95"][23]) < 0.2,
       "M7: a 24 meses, mediana e intervalo del 95 % en pasajeros frente a R (± 0.2)",
       f"{med:.2f} [{lo:.2f}, {hi:.2f}] frente a 525.46 [399.66, 690.85]")
    ok(all(en_capitulo(v, 2) for v in (P["original"]["media"][23], P["original"]["lo95"][23], P["original"]["hi95"][23])),
       "M7: 525.46, 399.66 y 690.85 están en el capítulo")

    # M8
    O["acf_duad"] = acf(np.diff(uad), 36)
    TR = J["trm_contraejemplo"]
    bt = 1.96 / math.sqrt(len(trm) - 1)
    ok(sum(abs(O["acf_dtrm"][k - 1]) > bt for k in (12, 24, 36)) == TR["estacionales_fuera_de_banda"],
       "M8: ningún rezago estacional de ∇TRM fuera de la banda")
    bu = 1.96 / math.sqrt(len(uad) - 1)
    O["uad_fuera"] = sum(abs(O["acf_duad"][k - 1]) > bu for k in (12, 24, 36))
    ok(O["uad_fuera"] >= 1, "M8: ∇USAccDeaths conserva picos estacionales fuera de la banda",
       f"{O['uad_fuera']} de 3 (ρ̂₁₂ = {O['acf_duad'][11]:.3f}, banda {bu:.3f})")
    O["t_trm"] = TR["forzado"]["Phi"] / TR["forzado"]["ee"]
    ok(abs(O["t_trm"] - TR["forzado"]["t"]) < 1e-3, "M8: t del SAR(1) forzado sobre la TRM ≈ J (redondeo)",
       f"{O['t_trm']:.4f} frente a {TR['forzado']['t']}; el capítulo da 0.0147 con Φ̂ completo")

    # M9
    C = A["calendario"]
    meses = [(1949 + i // 12, i % 12 + 1) for i in range(144)]
    dias = [((date(a + (m == 12), m % 12 + 1, 1) - date(a, m, 1)).days) for a, m in meses]
    O["dias"] = dias
    ok(dias == C["dias_mes"], "M9: días de cada mes = J")
    pas = {a: easter(a) for a in range(1949, 1961)}
    O["pascuas"] = pas
    ok(all(pas[a].isoformat() == C["pascuas"][str(a)] for a in pas), "M9: Pascuas (dateutil) = J")
    ok(sum(p.month == 3 for p in pas.values()) == C["meses_pascua_marzo"], "M9: dos Pascuas en marzo")
    O["pascua_ind"] = [1 if pas[a].month == m else 0 for a, m in meses]
    co = {c["nombre"]: c for c in C["modelos"]["con_dias_pascua"]["coeficientes"]}
    O["t_beta1"] = (co["log_dias"]["valor"] - 1) / co["log_dias"]["ee"]
    ok(abs(O["t_beta1"] - 0.1882) < 1e-3 and "= 0.19$" in CAPITULO, "M9: t de β = 1 vale 0.19")

    # M10
    tt = np.arange(1, 145, dtype=float)

    def ssr(cols):
        X = np.column_stack([np.ones(144), tt] + cols)
        q, rr = np.linalg.qr(X)
        b = np.linalg.solve(rr, (q * ly[:, None]).sum(axis=0))
        res = ly - (X * b).sum(axis=1)
        return float(res @ res)
    four = []
    for k in range(1, 7):
        if k < 6:
            four.append(np.sin(2 * np.pi * k * tt / 12))
        four.append(np.cos(2 * np.pi * k * tt / 12))
    O["ssr_K"] = {K: ssr(four[:min(2 * K, 11)]) for K in range(1, 7)}
    ind = [((tt - 1) % 12 + 1 == m).astype(float) for m in range(2, 13)]
    O["ssr_ind"] = ssr(ind)
    ok(abs(O["ssr_K"][6] - O["ssr_ind"]) < 1e-10, "M10: con K = 6, Fourier y 11 indicadoras dan el mismo ajuste",
       f"SSR {O['ssr_K'][6]:.10f}")
    ok([min(2 * K, 11) for K in range(1, 7)] == [r_["n_terminos"] for r_ in A["fourier"]["resultados"]],
       "M10: 2K términos, 11 con K = 6, como en J")

    # M11
    CO = A["comparativa"]
    obs = np.array(CO["observado"], float)
    O["metricas"] = {}
    mx = 0
    for k, m in CO["modelos"].items():
        pr = np.array(m["pronostico"], float)
        rm, ma_, mp = np.sqrt(np.mean((obs - pr) ** 2)), np.mean(np.abs(obs - pr)), 100 * np.mean(np.abs((obs - pr) / obs))
        O["metricas"][k] = (rm, ma_, mp)
        mx = max(mx, abs(rm - m["rmse"]), abs(ma_ - m["mae"]), abs(mp - m["mape"]))
    ok(mx < 2e-3, "M11: RMSE, MAE y MAPE de los ocho métodos frente a J",
       f"diferencia máxima {mx:.4f}: J las calcula con los pronósticos sin redondear")
    rk = sorted(O["metricas"], key=lambda k: O["metricas"][k][0])
    ok(rk[0] == "ets_log" and rk.index("sarima") in (3, 4), "M11: gana el ETS sobre el log y el SARIMA queda cuarto")
    return O


# ============================================================ 2. lo estático
PERMITIDAS = {"SUMPRODUCT", "INDEX", "AVERAGE", "DEVSQ", "COUNT", "SQRT", "LN", "EXP", "VAR", "SUMSQ",
              "SUMXMY2", "ABS", "IF", "IFERROR", "AND", "_XLFN.CHISQ.DIST.RT", "_XLFN.NORM.S.INV", "LINEST",
              "OFFSET", "DAY", "EOMONTH", "DATE", "YEAR", "MONTH", "MOD", "INT", "SIN", "COS", "PI",
              "MATCH", "RANK", "SUMIF", "COUNTIF", "NA", "MIN", "MAX", "SMALL", "SUM", "CHOOSE"}
PROHIBIDAS = {"LET", "LAMBDA", "SEQUENCE", "FILTER", "UNIQUE", "SORT", "SORTBY", "XLOOKUP", "XMATCH",
              "RANDARRAY", "MAKEARRAY", "BYROW", "BYCOL", "MAP", "REDUCE", "SCAN", "VSTACK", "HSTACK",
              "TAKE", "DROP", "CHOOSECOLS", "CHOOSEROWS", "TOCOL", "TOROW", "WRAPROWS", "WRAPCOLS",
              "TEXTSPLIT", "IFS", "SWITCH", "MAXIFS", "MINIFS", "CONCAT", "TEXTJOIN"}
RE_FUN = re.compile(r"(?<![A-Za-z0-9_.])(_?[A-Za-z][A-Za-z0-9_.]*)\(")
RE_REF = re.compile(r"(?:'([^']+)'!|(?<![A-Za-z0-9_.'])([A-Za-z][A-Za-z0-9_]*)!)?(?<![A-Za-z0-9_.])"
                    r"\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?(?![A-Za-z0-9_(])")


def col_num(s):
    n = 0
    for ch in s:
        n = n * 26 + ord(ch) - 64
    return n


def formulas(wb):
    for ws in wb.worksheets:
        for fila in ws.iter_rows():
            for c in fila:
                if isinstance(c.value, str) and c.value.startswith("="):
                    yield ws.title, c.coordinate, c.value


def precedentes(hoja, f):
    sin_textos = re.sub(r'"[^"]*"', '""', f)
    for m in RE_REF.finditer(sin_textos):
        h = m.group(1) or m.group(2) or hoja
        c1, f1 = col_num(m.group(3)), int(m.group(4))
        c2, f2 = (col_num(m.group(5)), int(m.group(6))) if m.group(5) else (c1, f1)
        for cc in range(min(c1, c2), max(c1, c2) + 1):
            for ff in range(min(f1, f2), max(f1, f2) + 1):
                yield (h, cc, ff)


def estatico():
    print("\n2 · Lo estático")
    destino = G.DESTINO
    ruta = {m: destino / n for m, n in G.ARCHIVOS.items()}
    for modo in G.ARCHIVOS:
        b1 = G.a_bytes(G.construir(modo))
        b2 = G.a_bytes(G.construir(modo))
        ok(b1 == b2, f"{modo}: el generador es determinista (dos construcciones, mismos bytes)")
        ok(ruta[modo].exists() and ruta[modo].read_bytes() == b1,
           f"{modo}: el libro del disco es el que genera hoy genera_excel_cap5.py")
    sol = openpyxl.load_workbook(ruta["solucion"])
    est = openpyxl.load_workbook(ruta["ejercicio"])
    usadas, malas = set(), set()
    for wb in (sol, est):
        for _, _, f in formulas(wb):
            for fn in RE_FUN.findall(f):
                usadas.add(fn.upper())
    malas = usadas - PERMITIDAS
    ok(not malas, "solo funciones clásicas (Excel 2016+, LibreOffice, Google Sheets)",
       f"{len(usadas)} distintas" + (f"; fuera de la lista: {sorted(malas)}" if malas else ""))
    ok(not (usadas & PROHIBIDAS), "ninguna de LET, LAMBDA, SEQUENCE ni las de matriz dinámica")
    claves = []
    for ws in sol.worksheets:
        we = est[ws.title]
        for fila in ws.iter_rows():
            for c in fila:
                if isinstance(c.value, str) and c.value.startswith("=") and we[c.coordinate].value is None:
                    claves.append((ws.title, c.coordinate))
    reg = G.construir("ejercicio").claves
    ok(sorted(claves) == sorted(reg), "las celdas vacías del estudiante son exactamente las claves registradas",
       f"{len(claves)} celdas clave")
    distintas = [(ws.title, c.coordinate) for ws in sol.worksheets for fila in ws.iter_rows() for c in fila
                 if est[ws.title][c.coordinate].value != c.value and (ws.title, c.coordinate) not in set(reg)]
    ok(distintas == [("Portada", "A2")], "fuera de las claves y del subtítulo, los dos libros son idénticos celda a celda",
       "" if distintas == [("Portada", "A2")] else str(distintas[:6]))
    por_hoja = {}
    for h, c in reg:
        por_hoja.setdefault(h, []).append(c)
    # «arrástrala»: cada celda del bloque es la primera fórmula arrastrada (openpyxl Translator)
    from openpyxl.formula.translate import Translator
    from openpyxl.utils.cell import coordinate_from_string, get_column_letter
    regset = set(reg)
    rotos, revisadas = [], 0
    for h, c in reg:
        com = est[h][c].comment
        if not com or "rrástrala" not in com.text:
            continue
        letra, fila = coordinate_from_string(c)
        col = col_num(letra)
        f0 = sol[h][c].value
        if "derecha" in com.text:
            pasos = [(0, 1)]                  # a la derecha, por la fila
        elif ":AL" in com.text:
            pasos = [(1, 0), (0, 1)]          # el cuadro de Durbin–Levinson, en las dos direcciones
        else:
            pasos = [(1, 0)]                  # hacia abajo, por la columna
        for df, dc in pasos:
            ff, cc = fila + df, col + dc
            while (h, f"{get_column_letter(cc)}{ff}") in regset:
                destino = f"{get_column_letter(cc)}{ff}"
                revisadas += 1
                if Translator(f0, origin=c).translate_formula(destino) != sol[h][destino].value:
                    rotos.append((h, destino))
                ff, cc = ff + df, cc + dc
    ok(not rotos, "donde la instrucción dice «arrástrala», cada celda es la primera fórmula arrastrada",
       f"{revisadas} celdas" + (f"; no casan {rotos[:6]}" if rotos else ""))
    sin_instr = [h for h, cs in por_hoja.items() if not any(est[h][c].comment for c in cs)]
    ok(not sin_instr, "cada hoja con celdas clave lleva sus instrucciones en comentarios",
       f"{sum(1 for h, c in reg if est[h][c].comment)} comentarios")
    return sol, set(claves)


# ====================================================== 3. Excel de verdad
APPLESCRIPT = r'''
on run argv
  set ruta to item 1 of argv
  set nombre to item 2 of argv
  with timeout of 900 seconds
    tell application "Microsoft Excel"
      set display alerts to false
      set otros to count of workbooks
      open (POSIX file ruta)
      if otros is 0 then
        calculate full
        set modo to "calculate full"
      else
        repeat with h in worksheets of workbook nombre
          calculate h
        end repeat
        set modo to "hoja a hoja"
      end if
      save workbook nombre
      close workbook nombre saving no
    end tell
  end timeout
  return modo
end run
'''


def recalcula_en_excel(origen, carpeta):
    copia = Path(carpeta) / origen.name.replace(".xlsx", "-recalculado.xlsx")
    shutil.copyfile(origen, copia)
    guion = Path(carpeta) / "recalcula.applescript"
    guion.write_text(APPLESCRIPT, encoding="utf-8")
    r = subprocess.run(["osascript", str(guion), str(copia), copia.name],
                       capture_output=True, text=True, timeout=1000)
    if r.returncode != 0:
        raise SystemExit(f"Excel no pudo recalcular {origen.name}: {r.stderr.strip()}")
    return copia, r.stdout.strip()


def valores(ruta):
    return openpyxl.load_workbook(ruta, data_only=True)


def excel(O, sol_f, claves):
    print("\n3 · Excel de verdad")
    with tempfile.TemporaryDirectory(prefix="recalculo-cap5-") as tmp:
        rs, modo_s = recalcula_en_excel(G.DESTINO / G.ARCHIVOS["solucion"], tmp)
        re_, modo_e = recalcula_en_excel(G.DESTINO / G.ARCHIVOS["ejercicio"], tmp)
        print(f"  (Excel recalculó: {modo_s})")
        vs, ve = valores(rs), valores(re_)
    # comprobaciones de la solución
    checks = [(h, c) for h, c, f in formulas(sol_f) if f.startswith("=IFERROR(IF(") and '"✔"' in f]
    estado_s = {k: vs[k[0]][k[1]].value for k in checks}
    malos = {k: v for k, v in estado_s.items() if v not in ("✔", "—")}
    ok(not malos, f"solución: las {len(checks)} comprobaciones en ✔",
       f"{sum(v == '✔' for v in estado_s.values())} ✔, {sum(v == '—' for v in estado_s.values())} —"
       + (f"; fallan {sorted(malos.items())[:8]}" if malos else ""))
    errores = []
    for h, c, f in formulas(sol_f):
        v = vs[h][c].value
        if isinstance(v, str) and v.startswith("#") and not (v == "#N/A" and "NA()" in f):
            errores.append((h, c, v))
    ok(not errores, "solución: ninguna celda con error (salvo los #N/A de los gráficos)",
       str(errores[:6]) if errores else "")
    # el estudiante: ✘ justo donde la comprobación depende de una clave
    grafo = {}
    for h, c, f in formulas(sol_f):
        hc = openpyxl.utils.cell.coordinate_from_string(c)
        grafo[(h, col_num(hc[0]), hc[1])] = list(precedentes(h, f))
    cl = {(h, col_num(openpyxl.utils.cell.coordinate_from_string(c)[0]),
           openpyxl.utils.cell.coordinate_from_string(c)[1]) for h, c in claves}
    memo = {}

    def depende(n):
        if n in memo:
            return memo[n]
        memo[n] = False
        res = n in cl or any(depende(p) for p in grafo.get(n, ()))
        memo[n] = res
        return res
    sys.setrecursionlimit(100000)
    mal_est = []
    n_rojo = 0
    for h, c in checks:
        hc = openpyxl.utils.cell.coordinate_from_string(c)
        nodo = (h, col_num(hc[0]), hc[1])
        dep = any(depende(p) for p in grafo[nodo])
        esperado = "✘" if dep else estado_s[(h, c)]
        n_rojo += dep
        if ve[h][c].value != esperado:
            mal_est.append((h, c, ve[h][c].value, esperado))
    ok(not mal_est, f"estudiante: ✘ en las {n_rojo} comprobaciones que dependen de una celda por completar, "
                    f"y las otras {len(checks) - n_rojo} como en la solución",
       str(mal_est[:6]) if mal_est else "")
    # valores frente al oráculo
    def col(h, letra, f1, f2):
        return np.array([vs[h][f"{letra}{f}"].value for f in range(f1, f2 + 1)], float)

    def cerca(nombre, a, b, tol):
        no_num = [v for v in a if not isinstance(v, (int, float))]
        if no_num:
            ok(False, f"Excel frente al oráculo: {nombre}", f"valores no numéricos: {no_num[:4]}")
            return
        d = float(np.max(np.abs(np.asarray(a, float) - np.asarray(b, float))))
        ok(d <= tol, f"Excel frente al oráculo: {nombre}", f"diferencia máxima {d:.1e}")
    cerca("M1, ACF de log y, ∇log y, TRM y ∇TRM",
          np.r_[col("M1 Firma", "I", 47, 82), col("M1 Firma", "J", 47, 82), col("M1 Firma", "K", 47, 82),
                col("M1 Firma", "L", 47, 82)],
          np.r_[O["acf_log"], O["acf_dlog"], O["acf_trm"], O["acf_dtrm"]], 1e-10)
    cerca("M2, heladería", [vs["M2 Multiplicativo"][f"C{f}"].value for f in range(16, 21)], O["heladeria"], 1e-12)
    cerca("M2, ρ_k teórica (36 rezagos)", col("M2 Multiplicativo", "J", 70, 105), O["acf_ar1sar1"], 1e-9)
    cerca("M2, γ₀/σ² exacta y factorizada", [vs["M2 Multiplicativo"]["C67"].value, vs["M2 Multiplicativo"]["C68"].value],
          [O["gamma_exacta"], O["gamma_fact"]], 1e-9)
    cerca("M2, ACF de la serie simulada", col("M2 Multiplicativo", "J", 113, 148), O["acf_sim"], 1e-9)
    y0, y1 = O["tienda"]
    cerca("M3, la tienda (y y ∇₁₂ de la rejilla)",
          [vs["M3 Diferenciar"].cell(23 + i, 3 + m).value for i in range(4) for m in range(12)]
          + [vs["M3 Diferenciar"].cell(30 + i, 3 + m).value for i in range(3) for m in range(12)],
          list(y0) + list(y0[12:] - y0[:-12]), 0)
    cerca("M3, varianzas de las cinco combinaciones",
          col("M3 Diferenciar", "E", 66, 70),
          [O["comb"][k][1] for k in ("d0_D0", "d1_D0", "d0_D1", "d1_D1")] + [O["var_D2"]], 1e-12)
    cerca("M4, ACF de ∇∇₁₂ log y", col("M4 Identificar", "C", 13, 48), O["acf_w"], 1e-10)
    cerca("M4, ACF teórica del airline", [vs["M4 Identificar"][f"D{f}"].value for f in (58, 59, 60)], O["airline_teo"], 1e-12)
    cerca("M4, PACF por Durbin–Levinson", col("M4 Identificar", "AN", 81, 116), O["pacf_w"], 1e-9)
    cerca("M5, pesos ψ", col("M5 Airline", "I", 21, 56), O["psi_air"], 1e-12)
    cerca("M5, σ_h", col("M5 Airline", "L", 21, 56), O["sigma_h"], 1e-12)
    cerca("M6, residuales CSS", col("M6 Diagnóstico", "D", 113, 243), O["e_css"], 1e-10)
    m6 = vs["M6 Diagnóstico"]
    cerca("M6, Ljung–Box (Q y p, R y CSS)", [m6[f"B{f}"].value for f in range(25, 31)],
          [O["lb_r24"][0], O["lb_r24"][1], O["lb_r36"][0], O["lb_r36"][1], O["lb_css24"][0], O["lb_css24"][1]], 1e-8)
    cerca("M6, AICc y BIC de la rejilla", [m6[f"H{40 + i}"].value for i in range(36)] + [m6[f"I{40 + i}"].value for i in range(36)],
          [O["rejilla"][n][0] for n in J["airpassengers"]["rejilla"]] + [O["rejilla"][n][1] for n in J["airpassengers"]["rejilla"]], 1e-9)
    cerca("M7, los 24 pronósticos en logaritmos (CSS)", col("M7 Pronóstico", "C", 204, 227), O["pron_css"], 1e-10)
    m7 = vs["M7 Pronóstico"]
    cerca("M7, z y el horizonte 24 en pasajeros", [m7["B8"].value, m7["B9"].value, m7["K227"].value, m7["O227"].value,
                                                  m7["P227"].value, m7["L227"].value], list(O["z"]) + list(O["m7_24"][:3]) + [O["m7_24"][3]], 1e-7)
    cerca("M8, ACF de ∇USAccDeaths", col("M8 Contraejemplo", "D", 10, 45), O["acf_duad"], 1e-10)
    cerca("M8, t del SAR(1) forzado", [vs["M8 Contraejemplo"]["C61"].value], [O["t_trm"]], 1e-12)
    cerca("M9, días del mes", col("M9 Calendario", "C", 60, 203), O["dias"], 0)
    cerca("M9, indicadora de Pascua", col("M9 Calendario", "G", 60, 203), O["pascua_ind"], 0)
    pas = [vs["M9 Calendario"][f"P{21 + i}"].value for i in range(12)]
    ok([p.date() if isinstance(p, datetime) else p for p in pas] == [O["pascuas"][1949 + i] for i in range(12)],
       "Excel frente al oráculo: M9, fechas de Pascua por Meeus = dateutil")
    cerca("M9, t de β = 1", [vs["M9 Calendario"]["B41"].value], [O["t_beta1"]], 1e-12)
    cerca("M10, SSR con K = 6, con indicadoras y para K = 1…6",
          [vs["M10 Fourier"]["B11"].value, vs["M10 Fourier"]["B13"].value] + list(col("M10 Fourier", "C", 17, 22)),
          [O["ssr_K"][6], O["ssr_ind"]] + [O["ssr_K"][K] for K in range(1, 7)], 1e-10)
    m11 = vs["M11 Métricas"]
    claves_m = list(J["airpassengers"]["comparativa"]["modelos"])
    cerca("M11, RMSE, MAE y MAPE", [m11.cell(35 + i, 3 + j).value for i in range(3) for j in range(8)],
          [O["metricas"][k][i] for i in range(3) for k in claves_m], 1e-9)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--sin-excel", action="store_true", help="no abre Excel: solo el oráculo y lo estático")
    args = ap.parse_args()
    O = oraculo()
    sol_f, claves = estatico()
    if not args.sin_excel:
        excel(O, sol_f, claves)
    print()
    if FALLOS:
        print(f"{len(FALLOS)} comprobaciones fallan.")
        sys.exit(1)
    print("Todo en orden.")


if __name__ == "__main__":
    main()
