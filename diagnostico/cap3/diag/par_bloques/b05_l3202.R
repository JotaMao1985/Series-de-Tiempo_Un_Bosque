# ACF y PACF TEORICAS (exactas, no simuladas)
phi <- c(0.5, 0.3)

round(ARMAacf(ar = phi, lag.max = 5)[-1], 4)          # se quita el rezago 0
#> [1] 0.7143 0.6571 0.5429 0.4686 0.3971

round(ARMAacf(ar = phi, lag.max = 5, pacf = TRUE), 4) # PACF
#> [1] 0.7143 0.3000 0.0000 0.0000 0.0000
#   la PACF se corta EXACTAMENTE en el rezago p = 2

# Comprobacion de la formula de Yule-Walker para el AR(2)
rho1 <- phi[1] / (1 - phi[2])
rho2 <- phi[2] + phi[1]^2 / (1 - phi[2])
round(c(rho1, rho2), 4)
#> [1] 0.7143 0.6571

# Varianza del proceso: ecuacion de Yule-Walker con k = 0
sigma2 <- 1
rho    <- ARMAacf(ar = phi, lag.max = 2)[-1]
round(sigma2 / (1 - sum(phi * rho)), 4)
#> [1] 2.2436

# La misma, por la formula cerrada del AR(2)
round(sigma2 * (1 - phi[2]) /
        ((1 + phi[2]) * ((1 - phi[2])^2 - phi[1]^2)), 4)
#> [1] 2.2436

# Estacionariedad
all(Mod(polyroot(c(1, -phi))) > 1)
#> [1] TRUE