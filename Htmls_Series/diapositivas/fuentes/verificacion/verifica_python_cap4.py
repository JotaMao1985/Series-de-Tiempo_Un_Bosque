"""Contrasta con statsmodels las afirmaciones de Python de las diapositivas del
capítulo 4 (KPSS y valores por defecto de la constante en ARIMA).

Uso (desde la raíz del repositorio), con statsmodels instalado:
    python3 Htmls_Series/diapositivas/fuentes/verificacion/verifica_python_cap4.py
Escribe verificacion/directo_python_cap4.json.
"""
import json, warnings
from pathlib import Path
import numpy as np
import statsmodels
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parents[4]
nilo = np.array(json.loads((RAIZ / "precalculo/salidas/datos_series.json").read_text(encoding="utf-8"))["nilo"]["valores"], float)

out = {"entorno": {"statsmodels": statsmodels.__version__, "numpy": np.__version__}}
out["m3.kpss_auto"] = round(float(kpss(nilo, regression="c")[0]), 4)
out["m3.kpss_auto_rezagos"] = int(kpss(nilo, regression="c")[2])
out["m3.kpss_legacy"] = round(float(kpss(nilo, regression="c", nlags="legacy")[0]), 4)
out["m3.kpss_legacy_rezagos"] = int(kpss(nilo, regression="c", nlags="legacy")[2])
out["m3.kpss_nlags4"] = round(float(kpss(nilo, regression="c", nlags=4)[0]), 4)

# esqueleto del ciclo (módulo 2): Ljung–Box del ARIMA(1,1,1) en statsmodels
_aj = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
out["m2.lb20_statsmodels"] = round(float(acorr_ljungbox(_aj.resid, lags=[20], model_df=2)["lb_pvalue"].iloc[0]), 4)

# valores por defecto de `trend` según d
out["m5.parametros_d0_por_defecto"] = ARIMA(nilo, order=(1, 0, 1)).fit().param_names
out["m5.parametros_d1_por_defecto"] = ARIMA(nilo, order=(1, 1, 1)).fit().param_names
out["m5.parametros_d1_trend_t"] = ARIMA(nilo, order=(1, 1, 1), trend="t").fit().param_names
try:
    ARIMA(nilo, order=(1, 2, 1), trend="t").fit()
    out["m5.d2_trend_t"] = "no lanzó error"
except ValueError as e:
    out["m5.d2_trend_t"] = "ValueError: " + str(e)[:110]
out["m5.deriva_d1_python"] = None
f = ARIMA(nilo, order=(1, 1, 1), trend="t").fit()
i = f.param_names.index("x1")
out["m5.deriva_d1_python"] = [round(float(f.params[i]), 4), round(float(f.bse[i]), 4), round(float(f.params[i] / f.bse[i]), 3)]

(Path(__file__).with_name("directo_python_cap4.json")).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
