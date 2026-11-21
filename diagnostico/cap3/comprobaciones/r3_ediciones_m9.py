"""R3 · Módulo 9 · la elasticidad amplitud–nivel se presenta (qué es y cómo se calcula) y su tabla
sale de un bloque; cada cifra de la prosa que no tenía código lo recibe (rejilla sobre la raíz,
variantes de λ, ARMA(2,1) de la serie cruda, polinomio mal escrito, envolvente, bandas, límites
inferiores, asimetría y Shapiro–Wilk, rezagos de la TRM, ρ₁ inducido por el promedio mensual);
`auto.arima()` se presenta; el código se parte en uno por caso, cada uno tras su prosa."""
import html


def esc(codigo):
    """El código va escapado en el HTML, como en el resto de los bloques."""
    return html.escape(codigo, quote=False)


def grupo(etiqueta, r, py):
    return (
        '      <div class="code-tabs">\n'
        '        <div class="code-tabs-nav" role="tablist" aria-label="' + etiqueta + '">\n'
        '          <button class="code-tab-btn active" data-lang="r" role="tab" aria-selected="true">R</button>\n'
        '          <button class="code-tab-btn" data-lang="python" role="tab" aria-selected="false">Python</button>\n'
        '        </div>\n'
        '        <div class="code-tab-panel" data-lang="r">\n'
        '          <pre><code class="language-r">' + esc(r.rstrip("\n")) + '</code></pre>\n'
        '        </div>\n'
        '        <div class="code-tab-panel" data-lang="python" hidden>\n'
        '          <pre><code class="language-python">' + esc(py.rstrip("\n")) + '</code></pre>\n'
        '        </div>\n'
        '      </div>\n')


R_CASO1 = r'''## ---- Caso 1: manchas solares en raiz cuadrada -------------------------
manchas <- window(sunspot.year, start = 1770, end = 1869)

# Elasticidad amplitud-nivel: pendiente de log(desviacion) contra log(media) en
# bloques consecutivos de k anios (los que sobran al final se descartan)
elasticidad <- function(x, k) {
  g <- rep(seq_len(length(x) %/% k), each = k)
  x <- as.numeric(x)[seq_along(g)]
  niv <- tapply(x, g, mean); amp <- tapply(x, g, sd)
  aj <- lm(log(amp) ~ log(niv))
  c(b = coef(aj)[[2]], confint(aj)[2, ], R2 = summary(aj)$r.squared)
}
res <- t(sapply(c(10, 11, 5), function(k) elasticidad(manchas, k)))
rownames(res) <- paste(c(10, 11, 5), "anios")
round(res, 3)
#>              b 2.5 % 97.5 %    R2
#> 10 anios 0.816 0.593  1.040 0.899
#> 11 anios 0.766 0.533  0.998 0.897
#> 5 anios  0.703 0.475  0.931 0.700

min(manchas)          # el logaritmo NO es una opcion
#> [1] 0
sum(manchas == 0)
#> [1] 1
sum(sunspot.year == 0)   # en la serie completa, 1700-1988
#> [1] 3

library(forecast)
# Guerrero exige datos ESTRICTAMENTE positivos y aqui hay un cero, asi que
# se desplaza la serie una unidad (con el cero crudo, R lanza un aviso).
round(BoxCox.lambda(manchas + 1, method = "guerrero"), 4)
#> [1] 0.3062      entre el logaritmo (0) y la raiz cuadrada (0.5)

# La PACF en las dos escalas: que rezagos salen de la banda +-0.196
banda <- 1.96 / sqrt(length(manchas))
fuera <- function(x) {
  p <- pacf(x, lag.max = 20, plot = FALSE)$acf[, 1, 1]
  round(setNames(p[abs(p) > banda], which(abs(p) > banda)), 3)
}
fuera(manchas)
#>      1      2
#>  0.806 -0.634
fuera(sqrt(manchas))
#>      1      2      6      9     16
#>  0.818 -0.617  0.200  0.198 -0.199

# La misma rejilla del Modulo 8 (los once candidatos), ahora sobre la raiz cuadrada
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
rejilla <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3),
                c(1,1), c(2,1), c(1,2), c(2,2))
compara <- function(x) do.call(rbind, lapply(rejilla, function(pq) {
  aj <- arima(x, order = c(pq[1], 0, pq[2]), method = "ML")
  data.frame(modelo = sprintf("ARMA(%d,%d)", pq[1], pq[2]),
             AICc = round(aicc(aj, length(x)), 2), BIC = round(BIC(aj), 2),
             LB12 = round(Box.test(residuals(aj), lag = 12, type = "Ljung-Box",
                                   fitdf = sum(pq))$p.value, 4))
}))
sq <- compara(sqrt(manchas))
sq[order(sq$AICc), ][1:4, ]          # las cuatro filas de la tabla, ordenadas por AICc
#>       modelo   AICc    BIC   LB12
#> 2  ARMA(2,0) 324.00 334.00 0.1644
#> 3  ARMA(3,0) 325.35 337.74 0.2005
#> 9  ARMA(2,1) 325.41 337.80 0.1856
#> 11 ARMA(2,2) 327.42 342.14 0.1833
c(AICc = sq$modelo[which.min(sq$AICc)], BIC = sq$modelo[which.min(sq$BIC)])
#>        AICc         BIC
#> "ARMA(2,0)" "ARMA(2,0)"       <- el AR(2) gana por los dos criterios

ar2s <- arima(sqrt(manchas), order = c(2, 0, 0), method = "ML")
round(coef(ar2s), 4)
#>     ar1     ar2  intercept
#>  1.4027 -0.6853     6.3317
round(sqrt(diag(ar2s$var.coef))[1:2], 4)    # errores estandar de phi_1 y phi_2
#>    ar1    ar2
#> 0.0727 0.0724
round(coef(ar2s)[1:2] / sqrt(diag(ar2s$var.coef))[1:2], 2)   # estadisticos t
#>    ar1    ar2
#>  19.31  -9.46
round(ar2s$sigma2, 4)
#> [1] 1.341

Box.test(residuals(ar2s), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value
#> [1] 0.1643997          <- ahora SI pasa

phi <- coef(ar2s)[1:2]
round(2 * pi / Arg(polyroot(c(1, -phi))[1]), 4)
#> [1] 11.2178            anios; el ciclo solar documentado es ~11

# Cambiar la raiz por la potencia de Guerrero (lambda = 0.3062): la lectura no cambia
ajusta <- function(x) {
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  c(periodo = 2 * pi / Arg(polyroot(c(1, -coef(f)[1:2]))[1]),
    LB12 = Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value)
}
lam <- BoxCox.lambda(manchas + 1, method = "guerrero")
round(rbind(raiz = ajusta(sqrt(manchas)),
            guerrero = ajusta(manchas^lam),                 # se aplica sobre la serie original
            guerrero_desplazada = ajusta((manchas + 1)^lam)), 4)
#>                     periodo   LB12
#> raiz                11.2178 0.1644
#> guerrero            11.3883 0.4892
#> guerrero_desplazada 11.2759 0.2216

# --- El modelo como polinomio: modulo Y angulo de la raiz --------------
raices <- polyroot(c(1, -phi))     # phi(B) = 1 - 1.4027 B + 0.6853 B^2
round(raices, 4)
#> [1] 1.0234+0.6418i 1.0234-0.6418i
round(c(modulo = Mod(raices)[1], angulo = Arg(raices)[1]), 4)
#> modulo angulo
#> 1.2080 0.5601            modulo > 1: estacionario; 2*pi/angulo = 11.2178

# Con el signo de phi_2 sin cambiar, el polinomio es OTRO proceso: 1 - 1.4027 B - 0.6853 B^2
round(Re(polyroot(c(1, -phi[[1]], phi[[2]]))), 4)
#> [1]  0.5598 -2.6066      una raiz DENTRO del circulo: ni siquiera es estacionario

# La otra formula del periodo: el periodo medio de los ciclos (no coincide)
round(2 * pi / acos(-phi[[1]] * (1 - phi[[2]]) / (4 * phi[[2]])), 4)
#> [1] 11.8356

# theta(B) = 1 no tiene raices: un AR puro es invertible y sus pi se acaban
round(c(pi1 = -phi[[1]], pi2 = -phi[[2]]), 4)
#>     pi1     pi2
#> -1.4027  0.6853
# ...y la PACF teorica de este AR(2) se corta en 2, con el propio phi_2
round(ARMAacf(ar = phi, lag.max = 3, pacf = TRUE), 4)
#> [1]  0.8323 -0.6853  0.0000

# El ARMA(2,1) de la serie cruda: invertible y sin factor comun con la parte AR
a21 <- arima(manchas, order = c(2, 0, 1), method = "ML")
round(coef(a21), 4)
#>       ar1       ar2       ma1 intercept
#>    1.2274   -0.5620    0.3732   48.5307
round(coef(a21)[["ma1"]] / sqrt(a21$var.coef["ma1", "ma1"]), 2)   # t de theta_1
#> [1] 2.78
round(polyroot(c(1, coef(a21)[["ma1"]])), 4)                      # raiz de theta(B)
#> [1] -2.6795+0i
raices21 <- polyroot(c(1, -coef(a21)[c("ar1", "ar2")]))           # raices AR
round(raices21, 4)
#> [1] 1.092+0.7661i 1.092-0.7661i
round(Mod(raices21), 4)
#> [1] 1.3339 1.3339

# Los pesos psi del Modulo 4, sobre los coeficientes ESTIMADOS.
# ARMAtoMA() devuelve psi_1 en adelante; psi_0 = 1 va por convenio.
psi <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 11))
round(psi, 4)
#>  [1]  1.0000  1.4027  1.2822  0.8372  0.2957 -0.1590 -0.4257 -0.4881 -0.3929
#> [10] -0.2167 -0.0346  0.0999      cambian de signo entre el 4 y el 5
# Forma cerrada del AR(2) con raices complejas: envolvente x oscilacion
Rmod <- unname(sqrt(-phi[2])); w <- Arg(raices)[1]
round(Rmod^(0:11) * sin((0:11 + 1) * w) / sin(w), 4)
#>  [1]  1.0000  1.4027  1.2822  0.8372  0.2957 -0.1590 -0.4257 -0.4881 -0.3929
#> [10] -0.2167 -0.0346  0.0999      identica a la recursion
# La envolvente es +-factor * R^j; se reduce a la mitad cada "mitad" anios; los
# psi se anulan cuando (j + 1) * w es multiplo de pi, es decir, en j + 1 = "ceros" (medio ciclo)
round(c(R = Rmod, factor = 1 / sin(w), mitad = log(0.5) / log(Rmod), ceros = pi / w), 4)
#>      R factor  mitad  ceros
#> 0.8278 1.8823 3.6684 5.6089

# De los psi salen las bandas del pronostico, que es lo que hace forecast()
ee <- sqrt(ar2s$sigma2 * cumsum(psi^2))
round(cumsum(psi^2), 4)                 # columna de la suma de cuadrados
#>  [1] 1.0000 2.9675 4.6115 5.3124 5.3998 5.4251 5.6063 5.8446 5.9990 6.0459
#> [11] 6.0471 6.0571
round(ee, 2)                            # error estandar
#>  [1] 1.16 1.99 2.49 2.67 2.69 2.70 2.74 2.80 2.84 2.85 2.85 2.85
round(qnorm(0.975) * ee, 2)             # semiancho al 95 %
#>  [1] 2.27 3.91 4.87 5.23 5.27 5.29 5.37 5.49 5.56 5.58 5.58 5.59
round(qnorm(0.975) * ee[1:6], 4)
#> [1] 2.2697 3.9098 4.8739 5.2312 5.2741 5.2864
f <- forecast(ar2s, h = 6, level = 95)
round(as.numeric((f$upper - f$lower) / 2), 4)
#> [1] 2.2697 3.9098 4.8739 5.2312 5.2741 5.2864   <- lo mismo

# El techo: en un proceso ESTACIONARIO la suma de psi^2 converge
psi_largo <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 600))
round(c(suma = sum(psi_largo^2), gamma0 = ar2s$sigma2 * sum(psi_largo^2),
        var_muestral = var(sqrt(manchas))), 4)
#>         suma       gamma0 var_muestral
#>       6.1360       8.2283       8.1490   el abanico no pasa de gamma0
techo <- qnorm(0.975) * sqrt(ar2s$sigma2 * sum(psi_largo^2))
round(c(techo = techo, fraccion_h6 = qnorm(0.975) * ee[6] / techo), 4)
#>       techo fraccion_h6
#>      5.6222      0.9403

# Volver a las manchas: un limite inferior negativo se trunca en cero ANTES de
# elevarlo al cuadrado, porque su cuadrado seria una cota positiva falsa
inf <- as.numeric(forecast(ar2s, h = 8, level = 95)$lower)[7:8]   # h = 7 y h = 8
round(inf, 3)
#> [1] -0.209 -0.114
round(inf^2, 3)
#> [1] 0.044 0.013

# Lo que sigue sin estar bien: la normalidad de los residuales
asimetria <- function(e) mean((e - mean(e))^3) / sd(e)^3
ml <- arima(manchas, order = c(2, 0, 0), method = "ML")          # sobre la serie cruda
round(c(cruda = asimetria(residuals(ml)), raiz = asimetria(residuals(ar2s))), 3)
#>  cruda   raiz
#>  0.791  0.573
round(c(cruda = shapiro.test(residuals(ml))$p.value,
        raiz  = shapiro.test(residuals(ar2s))$p.value), 4)
#>  cruda   raiz
#> 0.0007 0.0470
'''

PY_CASO1 = r'''import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.arima_process import arma2ma

## ---- Caso 1: manchas solares en raiz cuadrada -------------------------
datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR >= 1770) & (datos.YEAR <= 1869), "SUNACTIVITY"].values

# Elasticidad amplitud-nivel: pendiente de log(desviacion) contra log(media) en
# bloques consecutivos de k anios (los que sobran al final se descartan)
def elasticidad(x, k):
    n = len(x) // k
    bloques = x[:n * k].reshape(n, k)
    niv, amp = bloques.mean(axis=1), bloques.std(axis=1, ddof=1)
    aj = sm.OLS(np.log(amp), sm.add_constant(np.log(niv))).fit()
    lo, hi = aj.conf_int()[1]
    return [aj.params[1], lo, hi, aj.rsquared]

print(np.round([elasticidad(manchas, k) for k in (10, 11, 5)], 3))
# [[0.816 0.593 1.04  0.899]
#  [0.766 0.533 0.998 0.897]
#  [0.703 0.475 0.931 0.7  ]]     filas: bloques de 10, 11 y 5 anios; columnas: b, IC 95 %, R2

print(manchas.min(), (manchas == 0).sum())   # 0.0  1   -> log imposible
print((datos.loc[datos.YEAR <= 1988, "SUNACTIVITY"] == 0).sum())   # 3 en 1700-1988

# La PACF en las dos escalas: que rezagos salen de la banda +-0.196
banda = 1.96 / np.sqrt(len(manchas))
def fuera(x):
    p = pacf(x, nlags=20, method="ywm")[1:]
    return {int(k + 1): round(float(p[k]), 3) for k in np.where(np.abs(p) > banda)[0]}
print(fuera(manchas))             # {1: 0.806, 2: -0.634}
print(fuera(np.sqrt(manchas)))    # {1: 0.818, 2: -0.617, 6: 0.2, 9: 0.198, 16: -0.199}

ar2s = ARIMA(np.sqrt(manchas), order=(2, 0, 0), trend="c").fit()
print(np.round(ar2s.arparams, 4))            # [ 1.4027 -0.6853]

lb = acorr_ljungbox(ar2s.resid, lags=[12], model_df=2)
print(round(float(lb["lb_pvalue"].iloc[0]), 4))   # 0.178
# R daba 0.1644: devuelve estandarizados los dos primeros residuales, y
# statsmodels no (Modulo 8). Descartando esos dos, los dos programas dan 0.1682.

phi = ar2s.arparams
raices = np.roots(np.r_[1, -phi][::-1])
print(round(2 * np.pi / np.angle(raices[0]), 4))  # 11.218 (en R, 11.2178)

print(np.round(ar2s.polynomial_ar, 4))       # [ 1.     -1.4027  0.6853]
print(round(abs(raices[0]), 4), round(float(np.angle(raices[0])), 4))
# 1.208 0.5601        modulo y angulo: estacionariedad y pseudo-periodo

# arma2ma es la misma recursion del Modulo 4, pero pide los coeficientes
# del POLINOMIO: el AR va negado, igual que en ArmaProcess (Modulo 1).
psi = arma2ma(np.r_[1, -phi], np.r_[1], lags=12)
print(np.round(psi, 4))
# [ 1.      1.4027  1.2822  0.8372  0.2957 -0.159  -0.4256 -0.4881 -0.3929
#  -0.2167 -0.0346  0.0999]
# El septimo peso sale -0.4256 y en R -0.4257: los dos optimizadores no dan
# exactamente el mismo phi. Es diferencia de estimacion, no de formula.

s2 = ar2s.params[-1]                  # ['const', 'ar.L1', 'ar.L2', 'sigma2']
ee = np.sqrt(s2 * np.cumsum(psi**2))
print(np.round(1.959964 * ee[:6], 4))
# [2.2697 3.9098 4.8739 5.2312 5.2741 5.2864]
ci = np.asarray(ar2s.get_forecast(6).conf_int(alpha=0.05))
print(np.round((ci[:, 1] - ci[:, 0]) / 2, 4))
# [2.2697 3.9098 4.8739 5.2312 5.2741 5.2864]   <- lo mismo

# La rejilla sobre la raiz, las variantes de lambda y la normalidad de los residuales
# se calculan en la pestana R: statsmodels devuelve sin estandarizar los dos primeros
# residuales (Modulo 8) y la asimetria y el Shapiro-Wilk saldrian distintos.
'''

R_CASO2 = r'''## ---- Caso 2: log-retornos de la TRM -----------------------------------
library(forecast)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }   # la de arriba

# trm: la serie mensual del Capitulo 2, el promedio de los valores diarios
# de cada mes entre enero de 2015 y junio de 2026. Copia fija de los 138
# meses con que se calcularon estas cifras: se lee de la carpeta de trabajo
# si el archivo ya esta ahi; si no, de la pagina del curso.
archivo <- "trm_mensual_2015-01_2026-06.csv"
if (!file.exists(archivo))
  archivo <- paste0("https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/", archivo)
trm <- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)

ret <- diff(log(trm)) * 100
length(ret)
#> [1] 137

round(1.96 / sqrt(length(ret)), 4)      # banda
#> [1] 0.1675
round(acf(ret, lag.max = 6, plot = FALSE)$acf[-1], 3)
#> [1]  0.105 -0.077 -0.078  0.006  0.193  0.123

# Los rezagos que se salen de la banda, entre los 20 primeros
a <- acf(ret, lag.max = 20, plot = FALSE)$acf[-1]
round(setNames(a, 1:20)[abs(a) > 1.96 / sqrt(length(ret))], 3)
#>      5      8
#>  0.193 -0.198

sapply(c(6, 12, 20), function(h)
  round(Box.test(ret, lag = h, type = "Ljung-Box")$p.value, 4))
#> [1] 0.0931 0.0601 0.0599

# auto.arima(): por defecto devuelve ruido blanco; con la busqueda
# exhaustiva, un MA(1). Ninguno de los dos lleva media.
arimaorder(auto.arima(ret))
#> p d q
#> 0 0 0
exh <- auto.arima(ret, stepwise = FALSE, approximation = FALSE)
arimaorder(exh)
#> p d q
#> 0 0 1
round(c(theta = coef(exh)[["ma1"]], ee = sqrt(exh$var.coef[1, 1])), 4)
#>  theta     ee
#> 0.1326 0.0905

# Promediar deja huella: si la tasa DIARIA fuera una caminata aleatoria, las
# variaciones del promedio mensual de m = 21 dias tendrian esta rho_1
m <- 21
pesos <- c(1:m, (m - 1):1) / m     # peso de cada choque diario en la variacion mensual
rho1 <- sum(pesos[1:(m - 1)] * pesos[(m + 1):(2 * m - 1)]) / sum(pesos^2)
round(c(rho1_inducido = rho1, r1_observado = a[1],
        distancia_ee = (rho1 - a[1]) * sqrt(length(ret))), 3)
#>  rho1_inducido   r1_observado   distancia_ee
#>          0.249          0.105          1.683

# La media no es significativa: el MA(1) CON media (el defecto de arima())
ma1 <- arima(ret, order = c(0, 0, 1), method = "ML")
round(c(theta = coef(ma1)[["ma1"]], media = coef(ma1)[["intercept"]],
        ee_media = sqrt(ma1$var.coef[2, 2])), 4)
#>    theta    media ee_media
#>   0.1262   0.2681   0.3195

# El AICc SI compara con y sin media: son los mismos datos y solo cambia
# un parametro. Los cuatro modelos, de una vez:
con <- function(q) arima(ret, order = c(0, 0, q), method = "ML")
sin <- function(q) arima(ret, order = c(0, 0, q), include.mean = FALSE, method = "ML")
round(c(ruido_con_media = aicc(con(0), 137), ruido_sin_media = aicc(sin(0), 137),
        ma1_con_media   = aicc(con(1), 137), ma1_sin_media   = aicc(sin(1), 137)), 3)
#> ruido_con_media ruido_sin_media   ma1_con_media   ma1_sin_media
#>         723.804         722.663         724.046         722.653

# Volatilidad: estructura en los cuadrados?
round(Box.test(ret^2, lag = 12, type = "Ljung-Box")$p.value, 4)
#> [1] 0.9166             <- tampoco
'''

PY_CASO2 = r'''import os
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

## ---- Caso 2: log-retornos de la TRM -----------------------------------
# La misma copia fija de 138 meses que lee R (enero de 2015 a junio de
# 2026): de la carpeta de trabajo si el archivo ya esta ahi; si no, de la
# pagina del curso.
archivo = "trm_mensual_2015-01_2026-06.csv"
if not os.path.exists(archivo):
    archivo = "https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/" + archivo
trm = pd.read_csv(archivo)["trm"]

ret = 100 * np.diff(np.log(trm.values))
print(len(ret), round(1.96 / np.sqrt(len(ret)), 4))    # 137 0.1675
a = acf(ret, nlags=20, fft=False)[1:]
print(np.round(a[:6], 3))
# [ 0.105 -0.077 -0.078  0.006  0.193  0.123]
fuera = np.where(np.abs(a) > 1.96 / np.sqrt(len(ret)))[0]
print({int(k + 1): round(float(a[k]), 3) for k in fuera})   # {5: 0.193, 8: -0.198}

print(np.round(acorr_ljungbox(ret, lags=[6, 12, 20])["lb_pvalue"].values, 4))
# [0.0931 0.0601 0.0599]

# Promediar deja huella: rho_1 de las variaciones de un promedio de m = 21 dias
# de una caminata aleatoria, frente a la r_1 observada
m = 21
pesos = np.r_[np.arange(1, m + 1), np.arange(m - 1, 0, -1)] / m
rho1 = (pesos[:m - 1] * pesos[m:]).sum() / (pesos**2).sum()
print(round(rho1, 3), round(a[0], 3), round((rho1 - a[0]) * np.sqrt(len(ret)), 2))
# 0.249 0.105 1.68

ma1 = ARIMA(ret, order=(0, 0, 1), trend="n").fit()
rb  = ARIMA(ret, order=(0, 0, 0), trend="n").fit()
print(np.round(ma1.params[:1], 4))             # [0.1326]  theta, sin media
print(round(ma1.aicc, 3), round(rb.aicc, 3))   # 722.653 722.663  indistinguibles

print(round(float(acorr_ljungbox(ret**2, lags=[12])["lb_pvalue"].iloc[0]), 4))
# 0.9166
'''


def registra(c, mover, entre, MOD, **_):
    c("M9 · la elasticidad amplitud–nivel se presenta: qué es, cómo se calcula y qué relación tiene con Box–Cox", MOD,
      r'''nivel: en un máximo solar hay más manchas y también fluctúan más. Eso se comprueba, no se supone. Midiendo la
        elasticidad amplitud–nivel (la pendiente de $\log(\text{desviación})$ contra $\log(\text{media})$ por bloques,
        el mismo diagnóstico del Capítulo 1):</p>''',
      r'''nivel: en un máximo solar hay más manchas y también fluctúan más. Eso se comprueba, no se supone. Una forma de
        medirlo es la <strong>elasticidad amplitud–nivel</strong>: se parte la serie en bloques consecutivos, se
        calcula la media (el nivel) y la desviación estándar (la amplitud) de cada uno, y se ajusta una recta a
        $\log(\text{desviación})$ contra $\log(\text{media})$. Su pendiente $\hat b$ dice cuánto crece la amplitud cuando
        crece el nivel: con $b = 0$ no depende de él y no hay nada que corregir; con $b = 1$ crece en proporción, y el
        remedio es el logaritmo; con $b = 0.5$, la raíz cuadrada. En general la potencia que estabiliza es
        $\lambda = 1 - b$, la escala de Box–Cox del Capítulo 2, cuyo criterio de Guerrero busca justamente que
        $s_i/\bar y_i^{\,1-\lambda}$ sea homogéneo entre bloques. Es la pregunta del gráfico de amplitud frente a nivel
        del Capítulo 1, con un número en lugar de una nube de puntos. Con tres tamaños de bloque (la función que los
        calcula está en el código del caso, al final de su sección):</p>''')

    c("M9 · la tabla de elasticidades, con tres decimales como lo que imprime el bloque", MOD,
      r'''          <tr><td>10 años</td><td>$0.8165$</td><td>$[0.593,\ 1.040]$</td><td>$0.899$</td></tr>
          <tr><td>11 años (un ciclo)</td><td>$0.7658$</td><td>$[0.533,\ 0.998]$</td><td>$0.897$</td></tr>
          <tr><td>5 años</td><td>$0.7034$</td><td>$[0.475,\ 0.931]$</td><td>$0.700$</td></tr>''',
      r'''          <tr><td>10 años</td><td>$0.816$</td><td>$[0.593,\ 1.040]$</td><td>$0.899$</td></tr>
          <tr><td>11 años (un ciclo)</td><td>$0.766$</td><td>$[0.533,\ 0.998]$</td><td>$0.897$</td></tr>
          <tr><td>5 años</td><td>$0.703$</td><td>$[0.475,\ 0.931]$</td><td>$0.700$</td></tr>''')

    c("M9 · cada columna de AICc se lee por separado: son datos distintos", MOD,
      r'''      <p>Y ahora el resultado. Repitiendo exactamente la misma rejilla del Módulo 8 sobre $\sqrt{\text{manchas}}$:</p>''',
      r'''      <p>Y ahora el resultado. Repitiendo exactamente la misma rejilla del Módulo 8 sobre $\sqrt{\text{manchas}}$
        —y leyendo cada columna de AICc por separado: la serie cruda y su raíz son datos distintos, y los criterios solo
        comparan modelos ajustados a los mismos—:</p>''')

    c("M9 · la otra fórmula del periodo se llama pseudo-periodo (la del código: 11.84)", MOD,
      r'''<strong>Otra fórmula para «el periodo».</strong>''',
      r'''<strong>Otra fórmula para «el pseudo-periodo».</strong>''')

    c("M9 · el 11.22 es el pseudo-periodo con que oscilan la ACF y los ψ", MOD,
      r'''El $11.22$ es el periodo con que
          oscilan la ACF y los pesos $\psi$ del modelo, el ángulo de la raíz;''',
      r'''El $11.22$ es el pseudo-periodo con que
          oscilan la ACF y los pesos $\psi$ del modelo, el ángulo de la raíz;''')

    c("M9 · j y h = j + 1: qué fila es qué horizonte, antes de la tabla de los pesos", MOD,
      r'''        $$\operatorname{Var}(e_{T+h}) = \hat\sigma^2\sum_{j=0}^{h-1}\psi_j^2$$
      </div>

      <table style="position:relative;">''',
      r'''        $$\operatorname{Var}(e_{T+h}) = \hat\sigma^2\sum_{j=0}^{h-1}\psi_j^2$$
      </div>

      <p>Cada fila lleva el peso $\psi_j$ y, a su derecha, lo que se acumula hasta él: la fila de $j = 5$ es el
        horizonte $h = 6$, porque el horizonte $h$ suma los $h$ pesos $\psi_0, \ldots, \psi_{h-1}$.</p>

      <table style="position:relative;">''')

    c("M9 · auto.arima() se presenta en su primera aparición", MOD,
      r'''rechaza en ninguno, aunque el $0.06$ es lo bastante bajo como para no cantar victoria. La búsqueda
        automática de <code>auto.arima()</code> tampoco encuentra nada firme. Con sus argumentos por defecto devuelve
        un ARIMA(0,0,0) con media cero, es decir, ruido blanco.''',
      r'''rechaza en ninguno, aunque el $0.06$ es lo bastante bajo como para no cantar victoria. La búsqueda
        automática tampoco encuentra nada firme: <code>auto.arima()</code>, del paquete <code>forecast</code>, ajusta
        por sí sola varios modelos ARIMA y se queda con el de menor AICc (el Capítulo 4 detalla cómo busca). Con sus
        argumentos por defecto devuelve un ARIMA(0,0,0) con media cero, es decir, ruido blanco.''')

    c("M9 · T, no n, para la longitud de la serie de log-retornos", MOD,
      r'''finanzas ($n = 137$).</p>''',
      r'''finanzas ($T = 137$).</p>''')

    # El código, partido por caso: el del caso 1 tras su prosa, el del caso 2 al final.
    c("M9 · el código del caso 1, tras «Lo que sigue sin estar bien»", MOD,
      r'''      <h3>El capítulo entero, sobre una sola serie</h3>
''',
      "      <h3>El código del caso 1</h3>\n\n"
      "      <p>Las cifras del caso sobre la raíz cuadrada salen de este bloque, en el orden en que aparecen; las de la serie cruda, de los bloques de los Módulos 7 y 8.</p>\n\n"
      + grupo("Caso 1: manchas solares", R_CASO1, PY_CASO1) + "\n"
      + r'''      <h3>El capítulo entero, sobre una sola serie</h3>
''')

    # El grupo viejo («Los dos casos reales») se sustituye por el del caso 2.
    entre("M9 · el código del caso 2, al final del módulo (sustituye al bloque único de los dos casos)", MOD,
           '      <div class="code-tabs">\n        <div class="code-tabs-nav" role="tablist" aria-label="Los dos casos reales">',
           '    </div>\n  </template>\n  <!-- ============================================================ -->\n'
           '  <!-- MÓDULO 10 · Cierre: ciencia de datos, resumen y evaluación    -->',
           grupo("Caso 2: log-retornos de la TRM", R_CASO2, PY_CASO2))
