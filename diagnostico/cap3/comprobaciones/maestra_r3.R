# R3 del cap. 3 · comprobación de la sesión maestra, con código propio
y <- sunspot.year
# elasticidad amplitud-nivel por bloques de 11 años: pendiente de log(sd) contra log(media)
el <- function(k) {
  g <- rep(seq_len(length(y) %/% k), each = k); x <- y[seq_along(g)]
  m <- tapply(x, g, mean); s <- tapply(x, g, sd)
  coef(lm(log(s) ~ log(m)))[2]
}
print(round(sapply(c(10, 11, 12), el), 4))
cat("ceros en 1700-1988:", sum(y == 0), "\n")
# rho1 inducido al promediar una caminata en bloques de 21 dias
k <- 21; w <- c(1:k, (k-1):1)            # pesos de los choques en la diferencia de promedios
rho1 <- sum(w[1:(length(w)-k)] * w[(k+1):length(w)]) / sum(w^2)
cat("rho1 inducido:", round(rho1, 4), "\n")
library(forecast); cat("ic por defecto de auto.arima:", eval(formals(auto.arima)$ic)[1], "\n")
# la elasticidad del M9 es sobre la ventana 1770-1869 (T = 100), no sobre la serie completa
y <- window(sunspot.year, start = 1770, end = 1869)
print(round(sapply(c(10, 11, 5), el), 4))
