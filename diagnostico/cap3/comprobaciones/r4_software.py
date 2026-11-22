# r4_software.py — ronda R4 (fuentes) del capítulo 3
#
# Lo que el capítulo dice de statsmodels y numpy, comprobado ejecutando (las
# entradas `propia` de bibliografia/contraste/cap3.yml). Son las comprobaciones
# de los lectores de la ronda, reunidas.
#
# Uso:  python3 diagnostico/cap3/comprobaciones/r4_software.py > diagnostico/cap3/comprobaciones/r4_software_py.out 2>&1

# ==========================================================================
# M1: convenio del MA en statsmodels, ArmaProcess pide el polinomio, np.roots descendente (c3-m1-07, -11, -36)
# ==========================================================================
print('\n=== M1: convenio del MA en statsmodels, ArmaProcess pide el polinomio, np.roots descendente (c3-m1-07, -11, -36) ===')
import numpy as np, statsmodels
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf
from statsmodels.tsa.arima.model import ARIMA
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
# (1) convenio de suma al estimar y al calcular la ACF
print(np.round(arma_acf(np.r_[1], np.r_[1, 0.7], lags=4), 4))
x = ArmaProcess(np.r_[1], np.r_[1, 0.7]).generate_sample(nsample=600, distrvs=np.random.default_rng(3).standard_normal)
print("r1", round(float(np.corrcoef(x[1:], x[:-1])[0, 1]), 4))
fit = ARIMA(x, order=(0, 0, 1), trend="n").fit()
print(fit.param_names, fit.params.round(4))
# (2) ArmaProcess pide el polinomio: ar=[1,-0.6] es phi=0.6
bien = ArmaProcess(ar=np.array([1, -0.6]), ma=np.array([1]))
mal = ArmaProcess(ar=np.array([1, 0.6]), ma=np.array([1]))
print(bien.arcoefs, np.round(bien.acf(5)[1:], 4))
print(mal.arcoefs, np.round(mal.acf(5)[1:], 4))
# (3) ARIMA de statsmodels estima phi como coeficiente (ar.L1 ~ +0.6 si phi=+0.6)
rng = np.random.default_rng(11)
y = bien.generate_sample(nsample=2000, distrvs=rng.standard_normal)
f2 = ARIMA(y, order=(1, 0, 0), trend="n").fit()
print(f2.param_names, f2.params.round(3))
# (4) numpy.roots: coeficientes de mayor a menor grado
print("np.roots([1,-3,2]) =", np.roots([1, -3, 2]), "(polinomio x^2-3x+2: raices 2 y 1)")
print("np.roots([2,-3,1]) =", np.roots([2, -3, 1]), "(mismos coeficientes invertidos: x'=2x^2-3x+1: 1 y 0.5)")
phi = np.array([1.4, -0.75]); coef = np.r_[1.0, -phi]
print("raices ascendente->invertido", np.roots(coef[::-1]), "sin invertir", np.roots(coef))

# ==========================================================================
# M3-M4: ARIMA de statsmodels y la invertibilidad; arma2ma/arma2ar (c3-m3-32, c3-m4-09)
# ==========================================================================
print('\n=== M3-M4: ARIMA de statsmodels y la invertibilidad; arma2ma/arma2ar (c3-m3-32, c3-m4-09) ===')
import inspect, numpy as np
from statsmodels.tsa.arima.model import ARIMA
print(inspect.signature(ARIMA.__init__))
from statsmodels.tsa.arima_process import ArmaProcess
y = ArmaProcess(np.r_[1], np.r_[1, 2.0]).generate_sample(nsample=1000, distrvs=np.random.default_rng(1).standard_normal)
r = ARIMA(y, order=(0,0,1)).fit()
print("defecto:", np.round(r.maparams,4), np.round(r.params[-1],4))
r2 = ARIMA(y, order=(0,0,1), enforce_invertibility=False).fit()
print("enforce_invertibility=False:", np.round(r2.maparams,4), np.round(r2.params[-1],4))
r3 = ARIMA(y, order=(0,0,1), enforce_invertibility=False).fit(start_params=[0.0, 2.0, 1.0])
print("enforce_invertibility=False, inicio 2:", np.round(r3.maparams,4), np.round(r3.params[-1],4))
import statsmodels.tsa.arima.model as m
doc = ARIMA.__doc__
i = doc.find("enforce_invertibility")
print(doc[i-50:i+400])

# ==========================================================================
# M3: techo de rho_1 en un MA(q), cos(pi/(q+2)) (c3-m3-12)
# ==========================================================================
print('\n=== M3: techo de rho_1 en un MA(q), cos(pi/(q+2)) (c3-m3-12) ===')
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(0)
def rho1(th):
    t = np.r_[1.0, th]
    return float(np.dot(t[:-1], t[1:]) / np.dot(t, t))
print("q  maximo numerico de rho_1   cos(pi/(q+2))   mayor valor propio de A/2")
for q in range(1, 7):
    best = 0
    for _ in range(40):
        r = minimize(lambda th: -rho1(th), rng.normal(size=q), method="BFGS")
        best = max(best, -r.fun)
    A = np.zeros((q+1, q+1))
    for i in range(q):
        A[i, i+1] = A[i+1, i] = 0.5
    print(q, round(best, 6), round(np.cos(np.pi/(q+2)), 6), round(np.linalg.eigvalsh(A).max(), 6))

# ==========================================================================
# M5: banda de Bartlett de statsmodels (c3-m5-30)
# ==========================================================================
print('\n=== M5: banda de Bartlett de statsmodels (c3-m5-30) ===')
import numpy as np
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima_process import ArmaProcess
n = 400
y = ArmaProcess(np.r_[1], np.r_[1, 0.7]).generate_sample(nsample=n, distrvs=np.random.default_rng(3).standard_normal)
a, ci = acf(y, nlags=6, alpha=0.05, bartlett_confint=True)
semiancho = (ci[:,1]-ci[:,0])/2
print("r_k:", np.round(a,3))
print("semiancho Bartlett:", np.round(semiancho,4))
print("a mano 1.96*sqrt((1+2*sum r_j^2, j<k)/n):", np.round([0]+[1.96*np.sqrt((1+2*np.sum(a[1:k]**2))/n) if k>1 else 1.96/np.sqrt(n) for k in range(1,7)],4))
print("ruido blanco 1.96/sqrt(n):", round(1.96/np.sqrt(n),4))
a2, ci2 = acf(y, nlags=6, alpha=0.05, bartlett_confint=False)
print("bartlett_confint=False semiancho:", np.round((ci2[:,1]-ci2[:,0])/2,4))

# ==========================================================================
# M5: redundancia de parametros en Python (c3-m5-32)
# ==========================================================================
print('\n=== M5: redundancia de parametros en Python (c3-m5-32) ===')
import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA
proceso = ArmaProcess(np.r_[1, -0.5], np.r_[1, -0.45])
y = proceso.generate_sample(nsample=200, distrvs=np.random.default_rng(11).standard_normal)
res = ARIMA(y, order=(1, 0, 1)).fit()
print(res.summary().tables[1])
print("suma ar1 + ma1 =", round(res.arparams[0] + res.maparams[0], 4))

# ==========================================================================
# M6-M8: generate_sample, yule_walker, acorr_ljungbox, residuales (c3-m6-04, c3-m7-16, -17, c3-m8-18)
# ==========================================================================
print('\n=== M6-M8: generate_sample, yule_walker, acorr_ljungbox, residuales (c3-m6-04, c3-m7-16, -17, c3-m8-18) ===')
import inspect, warnings
import numpy as np
import statsmodels, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.regression.linear_model import yule_walker
from statsmodels.stats.diagnostic import acorr_ljungbox
warnings.simplefilter("ignore")
print("statsmodels", statsmodels.__version__)
print("generate_sample:", inspect.signature(ArmaProcess.generate_sample))
print("yule_walker:", inspect.signature(yule_walker))
print("acorr_ljungbox:", inspect.signature(acorr_ljungbox))
doc = yule_walker.__doc__
i = doc.find("method")
print(doc[i-20:i+300])
datos = sm.datasets.sunspots.load_pandas().data
m = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values
print(len(m))
for meth in ("adjusted", "mle"):
    rho, sg = yule_walker(m - m.mean(), order=2, method=meth)
    print(meth, np.round(rho, 4), round(sg**2, 2) if sg is not None else None)
try:
    ARIMA(m, order=(2,0,0), trend="c").fit(method="css")
except Exception as e:
    print("css ->", type(e).__name__, e)
print((ARIMA.fit.__doc__ or "")[:100])
d = ARIMA.fit.__doc__
j = d.find("method : str")
print(d[j:j+900])
res = ARIMA(m, order=(2,0,0), trend="c").fit()
print("resid[:4]", np.round(res.resid[:4], 3))
print("aicc", hasattr(res, "aicc"), round(res.aicc, 2), round(res.bic, 2))
for md in (0, 2):
    print("model_df", md, acorr_ljungbox(res.resid, lags=[12], model_df=md).iloc[0].round(4).to_dict())
print(np.sqrt(6.226), 52.536/np.sqrt(6.226))

# ==========================================================================
# M7: tsa.arima_model.ARMA ya no existe; metodo por defecto de ARIMA.fit
# ==========================================================================
print('\n=== M7: tsa.arima_model.ARMA ya no existe; metodo por defecto de ARIMA.fit ===')
import warnings, inspect
warnings.simplefilter("ignore")
import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
try:
    import statsmodels.tsa.arima_model as am
    print("arima_model importa:", am.__file__)
    try:
        am.ARMA([1.0,2.0,3.0], order=(1,0))
    except Exception as e:
        print("ARMA ->", type(e).__name__, str(e)[:200])
except Exception as e:
    print("import arima_model ->", type(e).__name__, str(e)[:200])
src = inspect.getsource(ARIMA.fit)
i = src.find("method")
print([l.strip() for l in src.splitlines() if "method is None" in l or "method = " in l][:6])
print(inspect.signature(ARIMA.fit))
datos = sm.datasets.sunspots.load_pandas().data
m = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values
a = ARIMA(m, order=(2,0,0), trend="c").fit()
b = ARIMA(m, order=(2,0,0), trend="c").fit(method="innovations_mle")
print(np.round(a.arparams,4), np.round(b.arparams,4))
