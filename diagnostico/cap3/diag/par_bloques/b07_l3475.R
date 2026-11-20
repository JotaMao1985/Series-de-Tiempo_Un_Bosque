# Dos MA(1) con la MISMA ACF: theta y 1/theta
round(ARMAacf(ma = 0.5, lag.max = 3)[-1], 4)
#> [1] 0.4 0.0 0.0
round(ARMAacf(ma = 2.0, lag.max = 3)[-1], 4)
#> [1] 0.4 0.0 0.0     <- identicas: el modelo no esta identificado

# Invertibilidad: raices de theta(B) = 1 + theta*B
Mod(polyroot(c(1, 0.5)))   # theta = 0.5  -> raiz en -2
#> [1] 2
Mod(polyroot(c(1, 2.0)))   # theta = 2    -> raiz en -0.5
#> [1] 0.5              <- DENTRO del circulo: NO invertible

# MA(2): el triangulo, contra las raices de 1 + theta1*B + theta2*B^2
Mod(polyroot(c(1, 1.5, 0.6)))    # theta1 = 1.5 > 1...
#> [1] 1.290994 1.290994     <- ...y aun asi invertible
Mod(polyroot(c(1, 0.5, -0.6)))   # coeficientes pequenos...
#> [1] 0.9399017 1.7732350   <- ...y NO invertible

# El maximo de |rho_1| de un MA(1) esta en theta = 1
th <- seq(-3, 3, by = 0.01)
max(abs(th / (1 + th^2)))
#> [1] 0.5

# arima() devuelve siempre la version invertible
set.seed(1)
y <- arima.sim(n = 500, list(ma = 2.0))   # se le pide theta = 2 con sigma2 = 1...
m <- arima(y, order = c(0, 0, 1))
coef(m)["ma1"]                             # ...y devuelve theta ~ 1/2
#>       ma1
#> 0.4794171
m$sigma2                                   # ...con sigma2 ~ 2^2 = 4: el mismo proceso
#> [1] 4.081804