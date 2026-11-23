library(forecast)
ap <- log(AirPassengers)

# --- Etapas 2 a 4: D primero, d despues, y la ACF de la serie ya estacionaria
c(nsdiffs = nsdiffs(ap), ndiffs_tras_D = ndiffs(diff(ap, lag = 12)))
#> nsdiffs ndiffs_tras_D
#>       1             1
w <- diff(diff(ap, lag = 12))
a <- Acf(w, lag.max = 36, plot = FALSE)$acf
# La banda se calcula con la longitud de la serie a la que se le mide la ACF,
# que tras las dos diferencias son 131 observaciones y no las 144 de partida.
round(c(n = length(w), r1 = a[2], r12 = a[13], banda = 1.96/sqrt(length(w))), 4)
#>        n      r1     r12   banda
#> 131.0000 -0.3411 -0.3866  0.1712

# Los SATELITES del Modulo 2: tienen que asomar en 12 +/- 1 sin pedirlos.
# a[1] es el rezago 0, asi que a[12] y a[14] son los rezagos 11 y 13.
round(c(r11 = a[12], r13 = a[14]), 4)
#>    r11    r13
#> 0.0644 0.1516      positivos, y dentro de la banda: NO piden parametros

# --- Etapa 5: estimacion y diagnostico -------------------------------------
fit <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
round(c(coef(fit), sigma2 = fit$sigma2, aicc = fit$aicc), 6)
#>       ma1      sma1    sigma2      aicc
#> -0.401800 -0.556900  0.001371 -483.2101
checkresiduals(fit, lag = 24)     # grafico + Ljung-Box en una sola llamada
#> Ljung-Box test
#> Q* = 26.446, df = 22, p-value = 0.233

# Lo que el modelo AJUSTADO predice para los satelites. En un airline
# (MA x SMA) el termino cruzado del rezago 13 vale theta*Theta, y la ACF
# teorica de los satelites sale EXACTAMENTE rho_1 * rho_12.
th <- coef(fit)[["ma1"]]; TH <- coef(fit)[["sma1"]]
ma <- rep(0, 13); ma[1] <- th; ma[12] <- TH; ma[13] <- th * TH
rt <- unname(ARMAacf(ma = ma, lag.max = 13)[-1])
round(c(rho1 = rt[1], rho11 = rt[11], rho12 = rt[12], rho13 = rt[13]), 4)
#>    rho1   rho11   rho12   rho13
#> -0.3460  0.1471 -0.4251  0.1471
round(rt[1] * rt[12], 4)          # el producto, sin aproximar
#> [1] 0.1471

# --- Pronostico -------------------------------------------------------------
p <- forecast(fit, h = 24, level = c(80, 95))
round(exp(c(media = p$mean[24], lo95 = p$lower[24,2], hi95 = p$upper[24,2])), 2)
#>  media   lo95   hi95
#> 525.46 399.66 690.85
# El intervalo NO es simetrico alrededor de 525.46 en la escala original.
round(c(abajo = 525.46 - 399.66, arriba = 690.85 - 525.46), 2)
#>  abajo arriba
#> 125.80 165.39

# La anchura sale de los pesos psi (Capitulo 4, Modulo 9): aqui solo se usa.
# (1-B)(1-B^12) = 1 - B - B^12 + B^13  ->  ar = c(1, 0...0, 1, -1)
psi <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1),
                     ma = c(-0.4018, rep(0, 10), -0.5569, 0.2238), lag.max = 23))
round(psi[c(1, 2, 12, 13, 14)], 4)
#> [1] 1.0000 0.5982 0.5982 1.0413 0.8633     escalon justo en el rezago 12
round(sqrt(cumsum(psi^2) * fit$sigma2)[c(1, 12, 24)], 6)
#> [1] 0.037031 0.082273 0.139634