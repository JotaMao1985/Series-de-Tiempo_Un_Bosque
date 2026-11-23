library(forecast)
ap <- log(AirPassengers)

# SARIMA(0,1,1)(0,1,1)[12]: el periodo va en `seasonal`, no se deduce solo
# de la serie salvo que sea un objeto ts con frequency correcta.
fit <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
fit
#> Series: ap
#> ARIMA(0,1,1)(0,1,1)[12]
#> Coefficients:
#>           ma1     sma1
#>       -0.4018  -0.5569
#> s.e.   0.0896   0.0731

# Que la parte estacional MULTIPLICA se comprueba expandiendo el polinomio:
# (1 + theta B)(1 + Theta B^12) = 1 + theta B + Theta B^12 + theta*Theta B^13
th <- coef(fit)["ma1"]; Th <- coef(fit)["sma1"]
round(c(B1 = th, B12 = Th, B13 = th * Th), 4)
#>      B1     B12     B13
#> -0.4018 -0.5569  0.2238
# El coeficiente del rezago 13 NO se estima: sale del producto.

# La forma no multiplicativa se pediria con fixed=, y necesita 13 parametros
# para tocar los mismos rezagos. Casi nunca compensa.