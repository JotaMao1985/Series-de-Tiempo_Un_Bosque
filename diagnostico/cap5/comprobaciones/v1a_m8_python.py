"""Verificador A: el bloque de Python del M8 conserva warnings.filterwarnings("ignore").
¿Convergen sus dos ajustes? Se repiten sin silenciar avisos.
MPLBACKEND=Agg /opt/homebrew/Caskroom/mambaforge/base/bin/python3 v1a_m8_python.py"""
import warnings, numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
uad = sm.datasets.get_rdataset("USAccDeaths").data["value"].values
su = pd.Series(uad, index=pd.date_range("1973-01", periods=len(uad), freq="MS"))
st = pd.read_csv("../../../Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")["trm"]
st.index = pd.date_range("2015-01", periods=len(st), freq="MS")
casos = [("USAccDeaths sd=True", lambda: SARIMAX(su, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n", simple_differencing=True)),
         ("USAccDeaths sd=False", lambda: SARIMAX(su, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n")),
         ("TRM SAR(1)", lambda: SARIMAX(st, order=(0,1,0), seasonal_order=(1,0,0,12), trend="n", simple_differencing=True))]
for nombre, mk in casos:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        f = mk().fit(disp=False)
    g = mk().fit(disp=False, method="bfgs", maxiter=1000)
    print(nombre, "defecto conv", f.mle_retvals["converged"], [x.category.__name__ for x in w],
          np.round(f.params.values, 4), "| bfgs conv", g.mle_retvals["converged"], np.round(g.params.values, 4),
          "t", np.round(g.tvalues.values, 3))
