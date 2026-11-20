"""R1 del capítulo 3 · comprobaciones en Python (statsmodels).
Ejecutar desde la raíz del repo:
  MPLBACKEND=Agg python3 diagnostico/cap3/comprobaciones/r1_python.py > diagnostico/cap3/comprobaciones/r1_python.out 2>&1
"""
import warnings
import numpy as np
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.simplefilter("ignore")
print("statsmodels", statsmodels.__version__, "· numpy", np.__version__)

datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values

print("\n== AutoReg reproduce el CSS de R (1.4032, -0.7099; sigma2 229.03)")
css = AutoReg(manchas, lags=2, trend="c").fit()
print("params (const, L1, L2):", np.round(css.params, 4), " sigma2:", round(float(css.sigma2), 2))
print("np.round(css.params[1:], 4) ->", np.round(css.params[1:], 4))

print("\n== Residuales del AR(2) sobre la serie cruda: statsmodels devuelve la innovación cruda")
ml = ARIMA(manchas, order=(2, 0, 0), trend="c").fit()
print("resid[:4]:", np.round(ml.resid[:4], 3))
F = ml.filter_results.forecasts_error_cov[0, 0, :]
s2 = ml.params[-1]
print("varianza de la innovación / sigma2, t = 1, 2, 3:", np.round(F[:3] / s2, 3))
est = ml.resid / np.sqrt(F / s2)
print("resid estandarizados a escala sigma (lo que devuelve R), t = 1..4:", np.round(est[:4], 3))
lb = lambda e: round(float(acorr_ljungbox(e, lags=[12], model_df=2)["lb_pvalue"].iloc[0]), 4)
print("Ljung-Box(12): resid crudos", lb(ml.resid), "| estandarizados", lb(est), "| sin los dos primeros", lb(ml.resid[2:]))

print("\n== ARMA(2,1) con phi = (0.5, 0.3), theta = 0.4: la recursión del AR en k = 1")
r = arma_acf(np.r_[1, -0.5, -0.3], np.r_[1, 0.4], lags=6)
print("rho_1 =", round(r[1], 4), "| 0.5*rho_0 + 0.3*rho_1 =", round(0.5 * r[0] + 0.3 * r[1], 4),
      "| con rho_{-1} = 1:", round(0.5 * r[0] + 0.3 * r[0], 4))

print("\n== generate_sample sin burnin: arranca en cero, con varianza reducida (phi = 0.95, 5000 réplicas)")
rng = np.random.default_rng(11)
proc = ArmaProcess(np.r_[1, -0.95], np.r_[1])
M = np.array([proc.generate_sample(nsample=200, distrvs=rng.standard_normal) for _ in range(5000)])
for t in (1, 5, 20, 50, 200):
    print(f"t = {t:3d}: media = {M[:, t-1].mean():6.3f}  varianza = {M[:, t-1].var(ddof=1):6.3f}"
          f"  teórica = {(1 - 0.95**(2*t)) / (1 - 0.95**2):6.3f}")
print("varianza estacionaria:", round(1 / (1 - 0.95**2), 3))
Mb = np.array([proc.generate_sample(nsample=5, burnin=300, distrvs=rng.standard_normal) for _ in range(5000)])
print("con burnin=300, varianza en t = 1:", round(Mb[:, 0].var(ddof=1), 3))

print("\n== AR(2) sobre la raíz: Ljung-Box(12) con y sin los dos primeros residuales")
ar2s = ARIMA(np.sqrt(manchas), order=(2, 0, 0), trend="c").fit()
print("todos:", lb(ar2s.resid), "| sin los dos primeros:", lb(ar2s.resid[2:]))
phi = ar2s.arparams
print("periodo:", 2 * np.pi / np.angle(np.roots(np.r_[1, -phi][::-1])[0]))
