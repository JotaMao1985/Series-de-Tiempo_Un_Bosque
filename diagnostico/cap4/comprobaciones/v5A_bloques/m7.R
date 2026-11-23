library(forecast); library(tseries); data(NelPlo)
ip <- na.omit(NelPlo[, "ip"])        # produccion industrial: 129 datos anuales
c(kpss = ndiffs(ip, test = "kpss"), adf = ndiffs(ip, test = "adf"), pp = ndiffs(ip, test = "pp"))

# la traza de auto.arima, guardada como tabla
busca <- function(...) {
  traza <- capture.output(f <- auto.arima(ip, trace = TRUE, ...))
  traza <- grep("^ ARIMA", traza, value = TRUE)
  list(modelo = f, tabla = data.frame(modelo = trimws(sub(":.*", "", traza)),
                                      AICc = as.numeric(sub(".*:", "", traza))))
}
esc <- busca()                                            # (a) escalonada
exh <- busca(stepwise = FALSE, approximation = FALSE)     # (b) exhaustiva
c(escalonada = nrow(esc$tabla), exhaustiva = nrow(exh$tabla))
esc$tabla
head(exh$tabla[order(exh$tabla$AICc), ], 5)

# (c) el diagnostico de los dos ganadores
lb <- function(f, k) Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = k)$p.value
round(c(escalonada = lb(esc$modelo, 0), exhaustiva = lb(exh$modelo, 5)), 4)
round(rbind(coef = coef(exh$modelo), ee = sqrt(diag(exh$modelo$var.coef))), 3)