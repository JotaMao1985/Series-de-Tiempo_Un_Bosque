library(forecast)

# (a) El criterio de Guerrero con la receta del modulo: bloques de m datos,
#     cociente s / media^(1 - lambda) en cada uno y su coeficiente de variacion
guerrero <- function(y, lambda, m = frequency(y)) {
  bloques  <- matrix(y[1:(m * (length(y) %/% m))], nrow = m)   # un bloque por columna
  cociente <- apply(bloques, 2, sd) / colMeans(bloques)^(1 - lambda)
  sd(cociente) / mean(cociente)
}
# Comprobacion con las cifras del modulo: sin transformar, logaritmo y optimo
round(sapply(c(1, 0, -0.2947), function(l) guerrero(AirPassengers, l)), 3)

# (b) JohnsonJohnson: sin transformar, raiz cuadrada, logaritmo y optimo
y <- JohnsonJohnson
lambda <- BoxCox.lambda(y, method = "guerrero")
round(lambda, 4)
cv <- sapply(c(1, 0.5, 0, lambda), function(l) guerrero(y, l))
round(cv, 3)
round(100 * (cv[1] - cv[3]) / (cv[1] - cv[4]), 1)    # % de la mejora que capta el log

# (c) Deshacer un pronostico hecho en logaritmos: w = 2.75, error normal de sd 0.20
round(exp(2.75), 2)
round(exp(2.75 + c(-2, 2) * 0.20), 2)                # los extremos, en dolares
set.seed(8)
w <- rnorm(100000, mean = 2.75, sd = 0.20)
round(c(mediana = median(exp(w)), media = mean(exp(w))), 2)
