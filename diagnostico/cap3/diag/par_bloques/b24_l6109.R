theta <- c(0.6, 0.4)

# Invertibilidad: raices de theta(B) = 1 + 0.6B + 0.4B^2
raices <- polyroot(c(1, theta))
round(raices, 4)
#> [1] -0.75+1.3919i -0.75-1.3919i
round(Mod(raices), 4)
#> [1] 1.5811 1.5811        > 1  ->  INVERTIBLE

# ACF a mano, con theta_0 = 1
denominador <- 1 + sum(theta^2)                       # 1 + 0.36 + 0.16 = 1.52
rho1 <- (1 * theta[1] + theta[1] * theta[2]) / denominador   # (0.6 + 0.24)/1.52
rho2 <- (1 * theta[2]) / denominador                          # 0.4/1.52
round(c(rho1 = rho1, rho2 = rho2), 4)
#>   rho1   rho2
#> 0.5526 0.2632

# Contra ARMAacf
round(ARMAacf(ma = theta, lag.max = 4)[-1], 4)
#> [1] 0.5526 0.2632 0.0000 0.0000    <- coinciden, y se corta en q = 2

# Pesos pi: el MA(2) invertible se escribe como AR(infinito) convergente
round(ARMAtoMA(ar = -theta, lag.max = 8), 4)
#> [1] -0.6000 -0.0400  0.2640 -0.1424 -0.0202  0.0691 -0.0334 -0.0076
# oscilan y se desvanecen: es la firma de la invertibilidad