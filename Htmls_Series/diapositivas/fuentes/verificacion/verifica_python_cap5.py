#!/usr/bin/env python3
"""Cifras de statsmodels que citan las diapositivas del capítulo 5, recalculadas.

Usa las series congeladas de `precalculo/salidas/datos_series.json` (no descarga nada) y
escribe `directo_python_cap5.json` junto a este archivo, con la versión de statsmodels.

Uso (desde la raíz del repositorio):
    python3 Htmls_Series/diapositivas/fuentes/verificacion/verifica_python_cap5.py
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import kpss

warnings.filterwarnings("ignore")
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
DAT = json.loads((RAIZ / "precalculo/salidas/datos_series.json").read_text(encoding="utf-8"))

ap = np.log(np.array(DAT["airpassengers"]["valores"], float))
uad = np.array(DAT["usaccdeaths"]["valores"], float)
s_ap = pd.Series(ap, index=pd.date_range("1949-01", periods=len(ap), freq="MS"))
s_ua = pd.Series(uad, index=pd.date_range("1973-01", periods=len(uad), freq="MS"))


def ajusta(s, sd):
    f = SARIMAX(s, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n", simple_differencing=sd).fit(disp=False)
    return {"nobs": int(f.nobs), "ma1": float(f.params["ma.L1"]), "sma1": float(f.params["ma.S.L12"]),
            "sigma2": float(f.params["sigma2"])}


def diferencia(x, d=0, D=0, m=12):
    for _ in range(D):
        x = x[m:] - x[:-m]
    return np.diff(x, n=d) if d else x


out = {
    "entorno": {"statsmodels": statsmodels.__version__, "numpy": np.__version__},
    "ap_difuso": ajusta(s_ap, False),
    "ap_simple": ajusta(s_ap, True),
    "uad_difuso": ajusta(s_ua, False),
    "uad_simple": ajusta(s_ua, True),
    "kpss_uad_D1": float(kpss(diferencia(uad, 0, 1), regression="c", nlags=4)[0]),
    "kpss_uad_d1D1": float(kpss(diferencia(uad, 1, 1), regression="c", nlags=4)[0]),
    "kpss_critico_5": float(kpss(diferencia(uad, 0, 1), regression="c", nlags=4)[3]["5%"]),
}
out["ap_dif_max_coef"] = max(abs(out["ap_difuso"]["ma1"] - out["ap_simple"]["ma1"]),
                             abs(out["ap_difuso"]["sma1"] - out["ap_simple"]["sma1"]))
(AQUI / "directo_python_cap5.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
