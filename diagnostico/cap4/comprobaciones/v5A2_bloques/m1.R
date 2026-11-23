library(tseries); data(tcm)       # tcm1y: rendimiento a un anio, mensual
y <- tcm1y
length(y)

# (a) AR(2) con media, sin diferenciar: la raiz se ESTIMA
ar2 <- arima(y, order = c(2, 0, 0), method = "ML")
round(coef(ar2), 4)
round(c(suma = sum(coef(ar2)[1:2]), modulo = sort(Mod(polyroot(c(1, -coef(ar2)[1:2]))))), 4)

# (b) ARIMA(1,1,0): la raiz se IMPONE. Escrito sobre y_t es un AR(2)
ari <- arima(y, order = c(1, 1, 0), method = "ML")
phi <- coef(ari)[["ar1"]]
round(c(phi = phi, phi1_estrella = 1 + phi, phi2_estrella = -phi), 4)
round(c(suma = (1 + phi) - phi, modulo = sort(Mod(polyroot(c(1, -(1 + phi), phi))))), 4)

# (c) lo que pronostica cada uno a 1, 5 y 10 anios
h <- c(12, 60, 120)
p2 <- predict(ar2, n.ahead = 120); p1 <- predict(ari, n.ahead = 120)
round(rbind(AR2 = p2$pred[h], ARIMA110 = p1$pred[h], ee_AR2 = p2$se[h], ee_ARIMA110 = p1$se[h]), 2)
round(c(ultimo_dato = as.numeric(tail(y, 1)), desv_tipica_de_la_serie = sd(y)), 2)