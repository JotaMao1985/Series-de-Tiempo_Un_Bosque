# diag/v2.py — Par académico, capítulo 2: los bloques de Python, ejecutados.
# Uso (desde la raíz del repo):  MPLBACKEND=Agg python3 diagnostico/cap2/diag/v2.py
# AirPassengers se descarga como en el capítulo (get_rdataset); la TRM se toma de
# precalculo/salidas/datos_series.json (la serie con la que se escribieron las cifras),
# y aparte se prueba que el código de descarga del capítulo la reproduce.
import json, warnings
import numpy as np, pandas as pd
import statsmodels, scipy
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf, adfuller, kpss
from scipy.stats import boxcox
print("statsmodels", statsmodels.__version__, "pandas", pd.__version__, "scipy", scipy.__version__)

datos = sm.datasets.get_rdataset("AirPassengers").data
pasajeros = pd.Series(datos["value"].values,
                      index=pd.date_range("1949-01-01", periods=len(datos), freq="MS"))

print("== M3 ==")
r = acf(pasajeros, nlags=24, adjusted=False)[1:]
print("r[[0,1,11]]:", np.round(r[[0, 1, 11]], 4))

print("== M4 ==")
p = pacf(pasajeros, nlags=24, method="ywm")[1:]
print("pacf ywm 1..3:", np.round(p[:3], 4))
J = json.load(open("precalculo/salidas/cap2_estacionariedad.json"))
print("max|ywm - pacf R guardada| AP:", np.max(np.abs(p - np.array(J["series"]["airpassengers"]["pacf"]))))
import inspect
from statsmodels.tsa import stattools
src = inspect.getsource(stattools.pacf_yw)
print("pacf_yw usa yule_walker por orden (no Durbin-Levinson):", "yule_walker(" in src, "| levinson_durbin en pacf_yw:", "levinson_durbin" in src)
srcp = inspect.getsource(stattools.pacf)
print("en pacf(): rama ywm ->", [l.strip() for l in srcp.splitlines() if "ywm" in l or "ldb" in l][:8])

print("== M6 (TRM fijada al corte) ==")
d = json.load(open("precalculo/salidas/datos_series.json"))["trm"]
trm = pd.Series(d["valores"], index=pd.date_range("2015-01-01", periods=len(d["valores"]), freq="MS"))
def adf_como_en_r(x):
    k = int(((len(x) - 1) ** (1 / 3)))
    est, p, *_ = adfuller(x, maxlag=k, regression="ct", autolag=None)
    return round(est, 4), round(p, 4), k
print("adf_como_en_r(trm):", adf_como_en_r(trm))
print("adf_como_en_r(diff):", adf_como_en_r(trm.diff().dropna()))
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    est, pk, *_ = kpss(trm, regression="c", nlags=int(4 * (len(trm) / 100) ** 0.25))
    print("kpss(trm):", round(est, 4), pk, "nlags", int(4 * (len(trm) / 100) ** 0.25), "| avisos:", [str(x.message)[:60] for x in w])
print("adfuller por defecto (autolag='AIC', regression='c'):", [round(v, 4) if isinstance(v, float) else v for v in adfuller(trm)[:3]])

print("== M6 código de descarga del capítulo (Python) ==")
try:
    url = ("https://www.datos.gov.co/resource/32sa-8pi3.json"
           "?$select=vigenciadesde,valor"
           "&$where=vigenciadesde%20%3E=%20%272015-01-01T00:00:00.000%27"
           "&$order=vigenciadesde&$limit=20000")
    dd_ = pd.read_json(url)
    dd_["mes"] = dd_["vigenciadesde"].astype(str).str.slice(0, 7)
    dd_ = dd_[dd_["mes"] < pd.Timestamp.today().strftime("%Y-%m")]
    t2 = dd_.groupby("mes")["valor"].mean().round(2)
    t2.index = pd.PeriodIndex(t2.index, freq="M").to_timestamp()
    print("descargada: n =", len(t2), t2.index[0].date(), "->", t2.index[-1].date(), "| dtype valor:", dd_["valor"].dtype)
    comun = t2.loc[:"2026-06-01"]
    print("hasta 2026-06: n =", len(comun), " max|dif| con la serie fijada:", float(np.max(np.abs(comun.values - trm.values))))
except Exception as ex:
    print("descarga fallida:", ex)

print("== M7 ==")
lap = np.log(pasajeros)
for dd in range(4):
    y = lap.copy()
    for _ in range(dd):
        y = y.diff().dropna()
    print(dd, round(y.var(), 5), round(acf(y, nlags=1, adjusted=False)[1], 4))

print("== M8 ==")
w, lam = boxcox(pasajeros.values)
print("scipy boxcox (MV) lambda:", round(lam, 4))
w = np.log(pasajeros); y2 = np.exp(w); print("max|exp(log y) - y|:", float(np.max(np.abs(y2 - pasajeros))))

print("== M9 pipeline Python ==")
def kpss_como_ndiffs(w):
    nlags = int(3 * np.sqrt(len(w)) / 13)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        est, p, *_ = kpss(w, regression="c", nlags=nlags)
    return est, p
def preparar(y, m=12):
    w = np.log(y)
    D = 1 if m > 1 else 0
    if D:
        w = w.diff(m).dropna()
    est, p = kpss_como_ndiffs(w)
    print("   kpss tras nabla12: est", round(est, 4), "p", round(p, 4))
    d = 1 if p < 0.05 else 0
    if d:
        w = w.diff().dropna()
    est, p = kpss_como_ndiffs(w)
    return {"serie": w, "d": d, "D": D, "var_final": float(w.var()), "kpss_p": p}
res = preparar(pasajeros)
print(res["d"], res["D"], round(res["var_final"], 5), round(res["kpss_p"], 3), "n =", len(res["serie"]))
# ¿qué daría con la serie no estacional? D se impone, no se decide:
print("D con m=12 para ruido blanco (no estacional) tambien seria:", 1 if 12 > 1 else 0)
