# Sesión maestra, R1 del cap. 5: vuelve a medir lo que los verificadores A y B levantaron.
suppressPackageStartupMessages(library(forecast))
cat("== R", R.version$minor, " forecast", as.character(packageVersion("forecast")), "\n")

# A1: falsas alarmas del criterio "-1 dentro de Theta_hat +- 1.96 e.e." cuando no sobra nada (n = 144)
set.seed(1)
for (Th0 in c(-0.6, -0.85)) {
  r <- replicate(200, {
    w <- arima.sim(list(ma = c(-0.4, rep(0, 10), Th0, -0.4 * Th0)), n = 131)
    y <- ts(diffinv(diffinv(as.numeric(w), lag = 12), lag = 1), frequency = 12)
    f <- tryCatch(Arima(y, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12)), error = function(e) NULL)
    if (is.null(f)) NA else { Th <- coef(f)[["sma1"]]; (Th + 1) / sqrt(diag(f$var.coef))[["sma1"]] }
  })
  cat(sprintf("A1  Theta verdadero %.2f: alarma en %d de %d\n", Th0, sum(r < 1.96, na.rm = TRUE), sum(!is.na(r))))
}
