phi <- 0.8; theta <- -0.5

# (a) Pesos pi: los psi del proceso que intercambia los polinomios
#     (ar = -theta, ma = -phi)
round(ARMAtoMA(ar = -theta, ma = -phi, lag.max = 6), 4)
round(-(phi + theta) * (-theta)^(0:5), 4)       # la forma cerrada: los mismos

# (b) Una serie de 200 valores y su pronostico a un paso
set.seed(34)
y <- arima.sim(n = 200, model = list(ar = phi, ma = theta))
ultimas <- round(rev(y)[1:4], 2)                # y_200, y_199, y_198, y_197
ultimas
pesos <- -ARMAtoMA(ar = -theta, ma = -phi, lag.max = 200)    # -pi_1, -pi_2, ...
round(sum(pesos[1:4] * ultimas), 4)             # a mano: con esas cuatro
# Con las k ultimas observaciones, sin redondear
pronostico <- function(k) sum(pesos[1:k] * rev(y)[1:k])
round(c(con_4 = pronostico(4), con_8 = pronostico(8), con_200 = pronostico(200)), 4)
# El pronostico exacto de R, con los coeficientes fijados en los verdaderos
m <- arima(y, order = c(1, 0, 1), include.mean = FALSE,
           fixed = c(phi, theta), transform.pars = FALSE)
round(as.numeric(predict(m, n.ahead = 1)$pred), 4)

# (c) Pesos psi y varianza del error de pronostico, en unidades de sigma^2
psi <- c(1, ARMAtoMA(ar = phi, ma = theta, lag.max = 2))     # psi_0, psi_1, psi_2
round(psi, 4)
round(cumsum(psi^2), 4)                         # h = 1, 2, 3
techo <- sum(c(1, ARMAtoMA(ar = phi, ma = theta, lag.max = 500))^2)
round(c(techo = techo, fraccion_h3 = cumsum(psi^2)[3] / techo), 4)
