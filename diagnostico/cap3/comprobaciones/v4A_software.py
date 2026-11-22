"""Verificador A · R4 cap. 3 · repetición de las entradas `propia` de software
(numpy, statsmodels). python3 -I v4A_software.py"""
import inspect, warnings
import numpy as np, statsmodels, scipy.optimize as so
from statsmodels.tsa.arima_process import ArmaProcess, arma2ma, arma2ar, arma_acf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
warnings.simplefilter("ignore")
print("statsmodels", statsmodels.__version__, "numpy", np.__version__)
print("\n== c3-m1-36 · np.roots en orden descendente")
coef = [1, -1.4, 0.75]   # 1 - 1.4B + 0.75B^2, ascendente
print("np.roots(coef[::-1]) =", np.roots(coef[::-1]), "|z| =", np.abs(np.roots(coef[::-1])))
print("np.roots(coef)       =", np.roots(coef), "(otro polinomio)")
print("\n== c3-m1-11 · ArmaProcess recibe el polinomio; ARIMA devuelve el coeficiente")
bien = ArmaProcess(ar=np.array([1, -0.6]), ma=np.array([1])); mal = ArmaProcess(ar=np.array([1, 0.6]), ma=np.array([1]))
print("bien.arcoefs", bien.arcoefs, "acf", np.round(bien.acf(4)[1:], 4)); print("mal.arcoefs", mal.arcoefs, "acf", np.round(mal.acf(4)[1:], 4))
x = bien.generate_sample(3000, distrvs=np.random.default_rng(7).standard_normal)
print("ARIMA(1,0,0) ar.L1 =", round(ARIMA(x, order=(1, 0, 0), trend="n").fit().params[0], 4))
print("\n== c3-m1-07 · statsmodels: ma.L1 positivo para theta=+0.7")
x = ArmaProcess(np.r_[1], np.r_[1, 0.7]).generate_sample(nsample=3000, distrvs=np.random.default_rng(4).standard_normal)
print("ma.L1 =", round(ARIMA(x, order=(0, 0, 1), trend="n").fit().params[0], 4), " arma_acf:", np.round(arma_acf(np.r_[1], np.r_[1, 0.7], lags=3), 4))
print("\n== c3-m3-32 / c3-m4-31 · enforce_invertibility por defecto")
print("firma ARIMA:", {k: v.default for k, v in inspect.signature(ARIMA.__init__).parameters.items() if "enforce" in k})
y = ArmaProcess(np.r_[1], np.r_[1, 2.0]).generate_sample(nsample=500, distrvs=np.random.default_rng(1).standard_normal)
r = ARIMA(y, order=(0, 0, 1), trend="n").fit(); print("por defecto: ma.L1 =", round(r.params[0], 4), "sigma2 =", round(r.params[1], 4))
r2 = ARIMA(y, order=(0, 0, 1), trend="n", enforce_invertibility=False).fit(start_params=[2, 1]); print("enforce_invertibility=False, arranque 2: ma.L1 =", round(r2.params[0], 4), "sigma2 =", round(r2.params[1], 4))
print("\n== c3-m4-09 · arma2ma / arma2ar empiezan en el índice 0")
print("arma2ma:", np.round(arma2ma(np.r_[1, -0.7], np.r_[1, 0.5], lags=5), 4)); print("arma2ar:", np.round(arma2ar(np.r_[1, -0.7], np.r_[1, 0.5], lags=5), 4))
print("\n== c3-m3-12 · máximo numérico de rho1 en un MA(q)")
def menos_rho1(th):
    t = np.r_[1, th]; return -np.sum(t[:-1] * t[1:]) / np.sum(t ** 2)
rng = np.random.default_rng(0)
for q in (1, 2, 3, 4):
    best = max(-so.minimize(menos_rho1, rng.normal(size=q) * 2).fun for _ in range(40))
    print(f"q={q}: max numérico {best:.6f}  cos(pi/(q+2)) {np.cos(np.pi / (q + 2)):.6f}")
print("\n== c3-m5-30 · banda de Bartlett en plot_acf")
print("firma plot_acf bartlett_confint =", inspect.signature(plot_acf).parameters["bartlett_confint"].default)
z = ArmaProcess(np.r_[1], np.r_[1, 0.7]).generate_sample(400, distrvs=np.random.default_rng(3).standard_normal)
r, ci = acf(z, nlags=6, alpha=0.05, bartlett_confint=True)
r0, ci0 = acf(z, nlags=6, alpha=0.05, bartlett_confint=False)
semi = (ci[:, 1] - ci[:, 0]) / 2; semi0 = (ci0[:, 1] - ci0[:, 0]) / 2
amano = [1.96 * np.sqrt((1 + 2 * np.sum(r[1:k] ** 2)) / len(z)) for k in range(1, 7)]
print("r_k:", np.round(r[1:], 3)); print("semiancho Bartlett:", np.round(semi[1:], 4)); print("a mano 1.96*sqrt((1+2 sum_{j<k} r_j^2)/n):", np.round(amano, 4)); print("sin Bartlett:", np.round(semi0[1:], 4))
print("\n== c3-m6-04 · generate_sample: burnin=0 por defecto")
print(inspect.signature(ArmaProcess.generate_sample))
