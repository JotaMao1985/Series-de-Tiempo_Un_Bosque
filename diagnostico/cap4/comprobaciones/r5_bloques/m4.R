library(forecast); library(tsibbledata)    # global_economy: indicadores anuales por pais
col <- subset(as.data.frame(global_economy), Country == "Colombia")
y <- ts(col$Imports, start = 1960)         # importaciones, en % del PIB
c(kpss = ndiffs(y, test = "kpss"), adf = ndiffs(y, test = "adf"), pp = ndiffs(y, test = "pp"))

# (a) ACF y PACF de la serie diferenciada, con su banda
w <- diff(y)
round(1.96 / sqrt(length(w)), 3)
round(acf(w, lag.max = 10, plot = FALSE)$acf[-1], 3)
round(pacf(w, lag.max = 10, plot = FALSE)$acf[, 1, 1], 3)

# (b) y (c) los candidatos, con el mismo d
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
for (o in list(c(0, 1, 1), c(1, 1, 0), c(1, 1, 1), c(0, 1, 0))) {
  f <- arima(y, order = o, method = "ML")
  cat(sprintf("ARIMA(%d,1,%d)  AICc=%7.3f  BIC=%7.3f  LB(20) p=%.3f  coef: %s  ee: %s\n",
      o[1], o[3], aicc(f, length(y) - 1), BIC(f),
      Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = o[1] + o[3])$p.value,
      paste(sprintf("%.3f", coef(f)), collapse = " "),
      paste(sprintf("%.3f", sqrt(diag(f$var.coef))), collapse = " ")))
}
