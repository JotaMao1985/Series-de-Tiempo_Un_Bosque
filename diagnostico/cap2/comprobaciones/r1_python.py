"""R1 del capítulo 2 · comprobaciones en Python (statsmodels, scipy y, si está, pmdarima).

Desde la raíz del repo:
  MPLBACKEND=Agg python3 diagnostico/cap2/comprobaciones/r1_python.py > diagnostico/cap2/comprobaciones/r1_python.out 2>&1
pmdarima no está en el entorno del curso. Para la parte [4] se instaló en un entorno
virtual desechable (python3 -m venv --system-site-packages …; pip install pmdarima) y el
guion se ejecutó con ese intérprete; sin pmdarima, la parte [4] se salta y lo dice.
"""
import inspect, json, warnings
import numpy as np, pandas as pd, scipy, statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import pacf, pacf_yw, kpss
warnings.filterwarnings("ignore")
print("statsmodels", statsmodels.__version__, "· scipy", scipy.__version__, "· numpy", np.__version__, "· pandas", pd.__version__)

datos = sm.datasets.get_rdataset("AirPassengers").data
pasajeros = pd.Series(datos["value"].values, index=pd.date_range("1949-01-01", periods=len(datos), freq="MS"))
J = json.load(open("precalculo/salidas/cap2_estacionariedad.json"))
pacf_r = np.array(J["series"]["airpassengers"]["pacf"])

print("\n[1] PACF: ywm, ldb y pacf() de R sobre AirPassengers")
ywm = pacf(pasajeros, nlags=24, method="ywm")[1:]
ldb = pacf(pasajeros, nlags=24, method="ldb")[1:]
print("ywm[:3] =", np.round(ywm[:3], 4), "· ldb[:3] =", np.round(ldb[:3], 4), "· R[:3] =", pacf_r[:3])
print("max|ywm - ldb| =", float(np.max(np.abs(ywm - ldb))), "· max|ywm - R| =", float(np.max(np.abs(ywm - pacf_r))),
      "· max|ldb - R| =", float(np.max(np.abs(ldb - pacf_r))))
src = inspect.getsource(pacf_yw)
print("pacf_yw llama a yule_walker:", "yule_walker(" in src, "· a levinson_durbin:", "levinson_durbin" in src)
doc = inspect.getdoc(pacf)
for linea in doc.splitlines():
    if "ywm" in linea or "ldb" in linea or "Levinson" in linea or "Yule" in linea:
        print("   doc:", linea.strip())
src_pacf = inspect.getsource(pacf)
print("pacf(method='ldb') usa levinson_durbin:", "levinson_durbin" in src_pacf)

print("\n[2] Box-Cox: scipy (máxima verosimilitud) y statsmodels (Guerrero)")
from scipy.stats import boxcox
w, lam = boxcox(pasajeros.values)
print("scipy.stats.boxcox: lambda =", round(lam, 4))
from statsmodels.base.transform import BoxCox
bc = BoxCox()
for kw in ({"method": "guerrero", "window_length": 12},
           {"method": "guerrero", "window_length": 12, "scale": "sd", "options": {"bounds": (-1, 2)}},
           {"method": "loglik"}):
    try:
        _, l = bc.transform_boxcox(pasajeros.values, **kw)
        print("statsmodels BoxCox().transform_boxcox", kw, "-> lambda =", round(float(l), 4))
    except Exception as ex:
        print("statsmodels BoxCox", kw, "ERROR", type(ex).__name__, ex)
print("firma:", inspect.signature(bc.transform_boxcox))
for linea in inspect.getsource(bc._guerrero_cv).splitlines():
    print("   |", linea)
print("lambda de Guerrero en R (forecast::BoxCox.lambda):", J["box_cox"]["lambda_airpassengers"])
y2 = np.exp(np.log(pasajeros)); print("max|exp(log y) - y| =", float(np.max(np.abs(y2 - pasajeros))))

print("\n[3] KPSS sobre diff12 de log(AirPassengers) con los dos truncamientos")
d12 = np.log(pasajeros).diff(12).dropna()
for nombre, nl in (("floor(3*sqrt(n)/13)", int(3 * np.sqrt(len(d12)) / 13)), ("floor(4*(n/100)^0.25)", int(4 * (len(d12) / 100) ** 0.25))):
    est, p, *_ = kpss(d12, regression="c", nlags=nl)
    print(f"n = {len(d12)} · {nombre} = {nl} · KPSS = {est:.4f} · p = {p:.4f}")

print("\n[4] pmdarima")
try:
    import pmdarima
    from pmdarima.arima import ndiffs, nsdiffs
    from pmdarima.preprocessing import BoxCoxEndogTransformer
    print("pmdarima", pmdarima.__version__)
    lap = np.log(pasajeros)
    print('ndiffs(lap, test="kpss") ->', ndiffs(lap, test="kpss"))
    print('nsdiffs(lap, m=12, test="ocsb") ->', nsdiffs(lap, m=12, test="ocsb"))
    print('nsdiffs(lap, m=12, test="ch") ->', nsdiffs(lap, m=12, test="ch"))
    print('ndiffs(lap.diff(12).dropna(), test="kpss") ->', ndiffs(lap.diff(12).dropna(), test="kpss"))
    t = BoxCoxEndogTransformer().fit(pasajeros.values)
    print("BoxCoxEndogTransformer().fit(pasajeros).lam1_ =", round(float(t.lam1_), 4), "(scipy:", round(lam, 4), ")")
    print("su fit llama a stats.boxcox:", "stats.boxcox(" in inspect.getsource(BoxCoxEndogTransformer.fit))
except ImportError as ex:
    print("pmdarima no está instalado en este intérprete:", ex)
