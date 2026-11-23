# Heladeria inventada: desvios de su promedio en tres meses conocidos
feb24 <- 15; mar24 <- 20; feb25 <- 10
phi <- 0.6; Phi <- 0.7                 # SARIMA(1,0,0)(1,0,0)[12]

# Ruta 1: el polinomio ya multiplicado, con el satelite en el rezago 13
phi * feb25 + Phi * mar24 - phi * Phi * feb24
#> [1] 13.7

# Ruta 2: primero la sorpresa regular, despues la pregunta estacional
sorpresa_mar24 <- mar24 - phi * feb24  # lo que febrero no explica de marzo
sorpresa_mar24
#> [1] 11
phi * feb25 + Phi * sorpresa_mar24
#> [1] 13.7

# Si los dos modelos se sumaran, sin satelite
phi * feb25 + Phi * mar24
#> [1] 20

# El polinomio AR multiplicado, rezago a rezago: 2 parametros, 3 rezagos
ar <- c(phi, rep(0, 10), Phi, -phi * Phi)
round(ar[c(1, 12, 13)], 2)
#> [1]  0.60  0.70 -0.42

# En la ACF, el satelite es el producto de los dos caminos
r <- ARMAacf(ar = ar, lag.max = 13)
round(c(r[c("1", "11", "12", "13")], rho1_x_rho12 = r[["1"]] * r[["12"]]), 4)
#>            1           11           12           13 rho1_x_rho12
#>       0.6016       0.4230       0.7011       0.4218       0.4218