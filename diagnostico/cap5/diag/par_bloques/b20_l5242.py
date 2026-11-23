import numpy as np, pandas as pd, statsmodels.api as sm, warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
warnings.filterwarnings("ignore")

# --- USAccDeaths -----------------------------------------------------------
uad = sm.datasets.get_rdataset("USAccDeaths").data["value"].values
su = pd.Series(uad, index=pd.date_range("1973-01", periods=len(uad), freq="MS"))
f = SARIMAX(su, order=(0,1,1), seasonal_order=(0,1,1,12), trend="n",
            simple_differencing=True).fit(disp=False)
print(f.params[["ma.L1", "ma.S.L12"]].round(4))
#> ma.L1      -0.4303
#> ma.S.L12   -0.5527
# Con simple_differencing=True coincide con R. SIN esa opcion da -0.3924 y
# -0.5475: con n = 72 el prior difuso mueve theta casi cuatro centesimas.

# --- TRM: el contraejemplo -------------------------------------------------
# TRM mensual (promedio del mes, SFC via datos.gov.co); necesita internet.
url = ("https://www.datos.gov.co/resource/32sa-8pi3.json"
       "?$select=vigenciadesde,valor&$limit=50000")
crudo = pd.read_json(url)
crudo["fecha"] = pd.to_datetime(crudo["vigenciadesde"]).dt.tz_localize(None)
crudo = crudo[crudo["fecha"] >= "2015-01-01"].sort_values("fecha")
st = crudo.set_index("fecha")["valor"].resample("MS").mean().loc[:"2026-06-01"]
trm = st.values

acf = sm.tsa.acf(np.diff(trm), nlags=36, fft=False)
print(np.round(acf[[12, 24, 36]], 4), round(1.96/np.sqrt(len(trm)-1), 4))
#> [-0.0024 -0.0672  0.0714] 0.1675

g = SARIMAX(st, order=(0,1,0), seasonal_order=(1,0,0,12), trend="n",
            simple_differencing=True).fit(disp=False)
print(round(g.params["ar.S.L12"], 4), round(g.tvalues["ar.S.L12"], 3))
#> 0.0013 0.015
# t practicamente cero: el parametro estacional no aporta nada.