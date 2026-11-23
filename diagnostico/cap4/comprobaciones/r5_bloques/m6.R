library(tsibbledata)                 # gafa_stock: precios diarios de cuatro acciones
g <- subset(as.data.frame(gafa_stock), Symbol == "GOOG" & format(Date, "%Y") == "2018")
y <- ts(g$Close)                     # cierre diario de Google en 2018, en dolares
n <- length(y); n

# (a) la rejilla de AICc, con d = 1 y con d = 2
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
rejilla <- function(d) {
  m <- outer(0:2, 0:2, Vectorize(function(p, q) aicc(arima(y, order = c(p, d, q), method = "ML"), n - d)))
  dimnames(m) <- list(paste0("p=", 0:2), paste0("q=", 0:2)); m
}
r1 <- rejilla(1); r2 <- rejilla(2)
round(r1, 2)
round(r2, 2)

# (b) el mejor de cada d
round(c(mejor_d1 = min(r1), mejor_d2 = min(r2), diferencia = min(r1) - min(r2)), 3)

# (c) el mejor de d = 2, por dentro
f021 <- arima(y, order = c(0, 2, 1), method = "ML")
round(c(theta = coef(f021)[["ma1"]], raiz_MA = Mod(polyroot(c(1, coef(f021)[["ma1"]])))), 4)
round(c(sigma2_del_021 = f021$sigma2, varianza_de_la_diferencia = var(diff(y))), 2)
round(c(sigma2_del_010 = arima(y, order = c(0, 1, 0), method = "ML")$sigma2), 2)   # sin constante
