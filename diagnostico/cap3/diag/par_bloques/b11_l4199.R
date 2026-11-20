# ACF de un ARMA(1,1): rho_1 por la formula y despues rho_k = phi * rho_{k-1}
phi <- 0.7; theta <- 0.5
rho1 <- (1 + phi * theta) * (phi + theta) / (1 + 2 * phi * theta + theta^2)
round(rho1 * phi^(0:4), 4)
#> [1] 0.8308 0.5815 0.4071 0.2850 0.1995
round(ARMAacf(ar = phi, ma = theta, lag.max = 5)[-1], 4)
#>      1      2      3      4      5
#> 0.8308 0.5815 0.4071 0.2850 0.1995    <- coinciden

# Un AR(1) con el mismo phi decae al mismo ritmo, desde otro arranque
round(ARMAacf(ar = phi, lag.max = 5)[-1], 4)
#>      1      2      3      4      5
#> 0.7000 0.4900 0.3430 0.2401 0.1681

# Para k > q la recursion del AR vale en cualquier ARMA: un ARMA(2,1)
r <- ARMAacf(ar = c(0.5, 0.3), ma = 0.4, lag.max = 5)
round(r[3:6], 4)                                  # rho_2 a rho_5
#>      2      3      4      5
#> 0.7307 0.6238 0.5311 0.4527
round(unname(0.5 * r[2:5] + 0.3 * r[1:4]), 4)    # phi1 rho_{k-1} + phi2 rho_{k-2}
#> [1] 0.7307 0.6238 0.5311 0.4527

# ...pero NO para k = q: aqui q = 1 y la recursion se equivoca
round(unname(0.5 * r[1] + 0.3 * r[1]), 4)        # lo que daria la recursion
#> [1] 0.8
round(unname(r[2]), 4)                            # rho_1 verdadero
#> [1] 0.8614

# VARIANZA del proceso: gamma_k = s2 * sum(psi_j * psi_{j+k})
sigma2 <- 1
psi    <- c(1, ARMAtoMA(ar = 0.7, ma = 0.5, lag.max = 4000))
round(sigma2 * sum(psi^2), 4)                     # gamma_0
#> [1] 3.8235

# La misma, por la formula cerrada del ARMA(1,1)
phi <- 0.7; theta <- 0.5
round(sigma2 * (1 + 2*phi*theta + theta^2) / (1 - phi^2), 4)
#> [1] 3.8235

# Y gamma_1 / gamma_0 devuelve la rho_1 de la formula de arriba
g1 <- sigma2 * sum(psi[-length(psi)] * psi[-1])
round(c(gamma1 = g1, rho1 = g1 / (sigma2 * sum(psi^2))), 4)
#>  gamma1    rho1
#>  3.1765  0.8308