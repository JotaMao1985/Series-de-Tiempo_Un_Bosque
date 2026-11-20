# Redundancia: phi = -theta hace que el modelo colapse a ruido blanco
round(ARMAacf(ar = 0.5, ma = -0.5, lag.max = 5)[-1], 6)
#> [1] 0 0 0 0 0        <- la ACF de un ruido blanco

# Un proceso CASI redundante: phi = 0.5 y theta = -0.45 casi se cancelan,
# asi que en la practica es casi ruido blanco
round(ARMAacf(ar = 0.5, ma = -0.45, lag.max = 5)[-1], 4)
#> [1] 0.0515 0.0257 0.0129 0.0064 0.0032    <- autocorrelaciones minusculas

set.seed(11)
y <- arima.sim(n = 200, list(ar = 0.5, ma = -0.45))
ajuste <- arima(y, order = c(1, 0, 1))
#> Warning: possible convergence problem: optim gave code = 1
round(cbind(coef = coef(ajuste), ee = sqrt(diag(ajuste$var.coef))), 4)
#>              coef     ee
#> ar1        0.8300 0.2307
#> ma1       -0.7953 0.2477
#> intercept  0.0137 0.0806

# Los verdaderos son 0.5 y -0.45; la estimacion se va a 0.83 y -0.80.
# Lo que SI reproduce es la suma (0.0347 frente a 0.05): el ajuste fija
# la cancelacion, no cada coeficiente por separado.

# Y el modelo mas pequeno gana:
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
c(arma11 = aicc(ajuste, 200),
  ar1    = aicc(arima(y, order = c(1, 0, 0)), 200),
  ruido  = aicc(arima(y, order = c(0, 0, 0)), 200))
#>   arma11      ar1    ruido
#> 554.3463 552.9939 550.9449