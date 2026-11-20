manchas <- window(sunspot.year, start = 1770, end = 1869)   # n = 100

# 1. Yule-Walker (metodo de momentos)
yw <- ar(manchas, order.max = 2, aic = FALSE, method = "yule-walker")
round(yw$ar, 4)
#> [1]  1.3173 -0.6338

# 2. Suma de cuadrados condicional
css <- arima(manchas, order = c(2, 0, 0), method = "CSS")
round(coef(css)[1:2], 4)
#>     ar1     ar2
#>  1.4032 -0.7099

# 3. Maxima verosimilitud exacta
ml <- arima(manchas, order = c(2, 0, 0), method = "ML")
ml
#> Coefficients:
#>          ar1      ar2  intercept
#>       1.4059  -0.7111    48.2616
#> s.e.  0.0706   0.0702     4.9751
#> sigma^2 estimated as 229.4:  log likelihood = -414.94,  aic = 837.88

# La distancia entre YW y ML, medida en errores estandar
ee <- sqrt(diag(ml$var.coef))[1:2]
round((yw$ar - coef(ml)[1:2]) / ee, 2)
#>   ar1   ar2
#> -1.26  1.10

# Raices, modulo y pseudo-periodo del ajuste por ML
raices <- polyroot(c(1, -coef(ml)[1:2]))
round(Mod(raices), 4)
#> [1] 1.1859 1.1859        (> 1: estacionario)
round(2 * pi / Arg(raices[1]), 4)
#> [1] 10.7369              anios por ciclo

# La formula cerrada del AR(2) da lo mismo
phi <- coef(ml)[1:2]
round(2 * pi / acos(phi[1] / (2 * sqrt(-phi[2]))), 4)
#> [1] 10.7369

# El paso 6 del desarrollo: CSS puede salirse de la region estacionaria
set.seed(1)
z <- arima.sim(list(ar = 0.95), n = 40)
round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS")), 4)
#>    ar1
#> 1.0086     (> 1: fuera de la region estacionaria)
round(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML")), 4)
#>    ar1
#> 0.9808