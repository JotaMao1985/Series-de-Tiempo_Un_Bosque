set.seed(2026)
y <- arima.sim(n = 200, model = list(order = c(2, 1, 0), ar = c(0.4, 0.3)))

ajusta <- function(orden) {
  f  <- arima(y, order = orden, method = "ML")
  ma <- coef(f)[grepl("^ma", names(coef(f)))]
  print(round(rbind(coef = coef(f), ee = sqrt(diag(f$var.coef))), 3))
  cat(sprintf("|raiz MA| menor = %s    Ljung-Box(20) p = %.4f\n",
      if (length(ma)) sprintf("%.4f", min(Mod(polyroot(c(1, ma))))) else "no hay",
      Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = orden[1] + orden[3])$p.value))
}

ajusta(c(0, 1, 1))     # ajuste 1
ajusta(c(2, 2, 1))     # ajuste 2
ajusta(c(2, 1, 2))     # ajuste 3

# de vuelta a la etapa 1: la PACF de la serie diferenciada
round(pacf(diff(y), lag.max = 6, plot = FALSE)$acf[, 1, 1], 3)
round(1.96 / sqrt(length(diff(y))), 3)
ajusta(c(2, 1, 0))     # el modelo al que llevan los tres hallazgos
