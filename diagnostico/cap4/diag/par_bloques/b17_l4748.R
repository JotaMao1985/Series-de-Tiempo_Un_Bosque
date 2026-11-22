library(forecast)

# La forma del pronostico segun d, MEDIDA en vez de recordada
formas <- list(
  "d=0 con media"    = Arima(Nile, order = c(1,0,1)),
  "d=1 sin constante"= Arima(Nile, order = c(1,1,1)),
  "d=1 con deriva"   = Arima(Nile, order = c(1,1,1), include.drift = TRUE),
  "d=2"              = Arima(Nile, order = c(1,2,1)))
for (nm in names(formas)) {
  m <- as.numeric(forecast(formas[[nm]], h = 30)$mean)
  cat(sprintf("%-18s  1a dif en h=30: %7.3f   2a dif: %9.6f\n",
              nm, m[30] - m[29], m[30] - 2*m[29] + m[28]))
}
#> d=0 con media       1a dif en h=30:   0.254   2a dif: -0.040903
#> d=1 sin constante   1a dif en h=30:   0.000   2a dif:  0.000000
#> d=1 con deriva      1a dif en h=30:  -2.883   2a dif: -0.000000
#> d=2                 1a dif en h=30:  -4.049   2a dif:  0.000000
# d=2 da una RECTA (2a diferencia nula), no una parabola

# --- El intervalo, reconstruido desde los pesos psi ----------------------
f   <- Arima(Nile, order = c(1, 1, 1))
phi <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2)

# ARIMA(1,1,1) = ARMA(2,1) con ar* = (1 + phi, -phi) sobre la serie sin diferenciar
psi     <- c(1, ARMAtoMA(ar = c(1 + phi, -phi), ma = th, lag.max = 30))
sigma_h <- s * sqrt(cumsum(psi^2))[1:30]

fc <- forecast(f, h = 30, level = 95)
semiancho <- (fc$upper - fc$lower) / 2
max(abs(semiancho - qnorm(0.975) * sigma_h))     # deben coincidir
#> [1] 9.077894e-11

round(c(sigma = s, sigma_h1 = sigma_h[1], sigma_h30 = sigma_h[30],
        psi_30 = psi[31]), 3)
#>     sigma  sigma_h1 sigma_h30    psi_30
#>   142.045   142.045   199.363     0.169
# psi tiende a una CONSTANTE, no a cero: es la raiz unitaria

# Con d = 2 el MA estimado es theta = -1: el modelo no es invertible
f2   <- Arima(Nile, order = c(1, 2, 1))
ph2  <- coef(f2)[["ar1"]]
psi2 <- c(1, ARMAtoMA(ar = c(2 + ph2, -(1 + 2 * ph2), ph2),
                      ma = coef(f2)[["ma1"]], lag.max = 29))
fc2  <- forecast(f2, h = 30, level = 95)
round(c(theta     = coef(f2)[["ma1"]],
        psi_29    = psi2[30],
        ancho_psi = 2 * qnorm(0.975) * sqrt(f2$sigma2 * sum(psi2^2)),
        ancho_fc  = fc2$upper[30] - fc2$lower[30]), 3)
#>     theta    psi_29 ancho_psi  ancho_fc
#>    -1.000     0.718  2427.955  2771.452
# La formula se queda corta: con theta = -1 los choques pasados no se
# recuperan de los datos, y forecast() suma esa incertidumbre