theta <- c(0.9, 0.2)

# (a) Invertibilidad: raices de theta(B) = 1 + 0.9 B + 0.2 B^2 = (1 + 0.5 B)(1 + 0.4 B)
round(Re(polyroot(c(1, theta))), 4)
all(Mod(polyroot(c(1, theta))) > 1)

# (b) ACF a mano, con theta_0 = 1
denominador <- 1 + sum(theta^2)                              # 1 + 0.81 + 0.04
rho1 <- (1 * theta[1] + theta[1] * theta[2]) / denominador   # (0.9 + 0.18) / 1.85
rho2 <- (1 * theta[2]) / denominador                         # 0.2 / 1.85
round(c(rho1 = rho1, rho2 = rho2), 4)
round(ARMAacf(ma = theta, lag.max = 4)[-1], 4)     # coinciden, y se corta en q = 2

# (c) El otro MA(2): (1 + 2 B)(1 + 0.4 B) = 1 + 2.4 B + 0.8 B^2
round(ARMAacf(ma = c(2.4, 0.8), lag.max = 4)[-1], 4)      # la MISMA ACF
round(Re(polyroot(c(1, 2.4, 0.8))), 4)             # una raiz dentro del circulo

# Simulado el no invertible, arima() devuelve por defecto el invertible
set.seed(2)
y <- arima.sim(n = 2000, model = list(ma = c(2.4, 0.8)))
m <- arima(y, order = c(0, 0, 2), include.mean = FALSE)
round(c(coef(m), sigma2 = m$sigma2), 4)
