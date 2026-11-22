phi <- c(0.8, -0.6); const <- 4; sigma2 <- 3

# (a) El triangulo, las raices y el pseudo-periodo
c(phi[1] + phi[2] < 1, phi[2] - phi[1] < 1, abs(phi[2]) < 1)
phi[1]^2 + 4 * phi[2]                 # negativo: raices complejas
round(Mod(polyroot(c(1, -phi))), 4)
round(2 * pi / acos(phi[1] / (2 * sqrt(-phi[2]))), 2)

# (b) La media y las tres primeras autocorrelaciones
const / (1 - sum(phi))
rho1 <- phi[1] / (1 - phi[2])
rho2 <- phi[2] + phi[1]^2 / (1 - phi[2])
rho3 <- phi[1] * rho2 + phi[2] * rho1
c(rho1 = rho1, rho2 = rho2, rho3 = rho3)
round(ARMAacf(ar = phi, lag.max = 3)[-1], 4)

# (c) La varianza, por los dos caminos
sigma2 / (1 - phi[1] * rho1 - phi[2] * rho2)
sigma2 * (1 - phi[2]) / ((1 + phi[2]) * ((1 - phi[2])^2 - phi[1]^2))

# (d) Una realizacion larga: la media y la varianza muestrales
set.seed(32)
y <- const / (1 - sum(phi)) +
  arima.sim(n = 100000, model = list(ar = phi), sd = sqrt(sigma2))
round(c(media = mean(y), varianza = var(y)), 2)
