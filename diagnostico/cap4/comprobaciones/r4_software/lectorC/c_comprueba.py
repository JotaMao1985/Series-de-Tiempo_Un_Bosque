# lector C · comprobaciones en Python (statsmodels) para M5, M6 y M7 del capítulo 4
# Uso: python3 -I c_comprueba.py > c_comprueba_py.out
import warnings; warnings.filterwarnings("ignore")
import numpy as np, statsmodels, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import pkgutil, statsmodels.tsa as tsa
print("statsmodels", statsmodels.__version__, "· numpy", np.__version__)
nilo = sm.datasets.nile.load_pandas().data["volume"].values

print("\n== [m7-20] ¿hay un módulo auto_arima en statsmodels.tsa?")
print([m.name for m in pkgutil.walk_packages(tsa.__path__, "statsmodels.tsa.") if "auto" in m.name.lower()])
try:
    import pmdarima; print("pmdarima importable")
except Exception as e:
    print("pmdarima importable: False")

print("\n== [m6-16] nobs, nobs_effective y loglikelihood_burn por d (rejilla completa)")
filas = []
for d in range(3):
    for p in range(3):
        for q in range(3):
            try:
                f = ARIMA(nilo, order=(p, d, q), trend="c" if d == 0 else "n").fit()
            except Exception as e:
                continue
            filas.append((d, p, q, f.nobs, f.nobs_effective, f.loglikelihood_burn, f.aic, f.aicc, f.bic, f))
print("burn == d en todos:", all(r[5] == r[0] for r in filas), " · nobs == 100 en todos:", all(r[3] == 100 for r in filas), " · nobs_effective == 100 - d:", all(r[4] == 100 - r[0] for r in filas))
for d in range(3):
    g = [r for r in filas if r[0] == d]; b = min(g, key=lambda r: r[7])
    print(f"d={d} mejor AICc ({b[1]},{d},{b[2]}) aicc={b[7]:.3f} nobs={b[3]} nobs_eff={b[4]} burn={b[5]}")
# aicc a mano con n efectivo y con n
f = [r for r in filas if r[:3] == (1, 1, 1)][0][-1]
k = len(f.params)
aicc_eff = f.aic + 2 * k * (k + 1) / (f.nobs_effective - k - 1)
aicc_n   = f.aic + 2 * k * (k + 1) / (f.nobs - k - 1)
print(f"ARIMA(1,1,1): k={k}  f.aicc={f.aicc:.4f}  a mano n_ef=99: {aicc_eff:.4f}  a mano n=100: {aicc_n:.4f}  · dif = {aicc_eff-aicc_n:.4f}")
print(f"aic = {f.aic:.3f} (R: 1267.255)  · aicc - aic = {f.aicc-f.aic:.4f}")
print(f"aicc statsmodels - aicc R(1267.507) = {f.aicc-1267.507:.3f}")

print("\n== [m7-22] la búsqueda a mano del bloque del módulo 7: p, q en 0..3 con d=1, sin constante")
mejor, mejor_aicc, evaluados = None, float("inf"), 0
for p in range(4):
    for q in range(4):
        try:
            f = ARIMA(nilo, order=(p, 1, q), trend="n").fit()
        except Exception:
            continue
        evaluados += 1
        if f.aicc < mejor_aicc:
            mejor, mejor_aicc = (p, 1, q), f.aicc
print(mejor, round(mejor_aicc, 3), f"({evaluados} modelos)")

print("\n== [m5-14] trend por defecto y deriva con d >= 1")
for orden, tr in [((1,0,1), None), ((1,1,1), None), ((1,1,1), "t"), ((1,2,1), "t"), ((1,2,1), [0,0,1])]:
    try:
        r = ARIMA(nilo, order=orden, trend=tr).fit()
        print(orden, "trend =", tr, "->", r.param_names)
    except Exception as e:
        print(orden, "trend =", tr, "->", type(e).__name__, str(e)[:160].replace("\n", " "))
f0 = ARIMA(nilo, order=(1,0,1), trend="c").fit(); print("d=0 const =", round(f0.params[0], 4), " media muestral =", round(nilo.mean(), 4))
f1 = ARIMA(nilo, order=(1,1,1), trend="t").fit(); i = f1.param_names.index("x1")
print("d=1 trend='t': x1 =", round(f1.params[i], 4), "e.e. =", round(f1.bse[i], 4), "t =", round(f1.params[i]/f1.bse[i], 3))
