# Verificador A: tasa de falsas alarmas del criterio "-1 dentro de Theta +- 1.96 e.e."
# cuando NO sobra ninguna diferencia y Theta verdadero es -0.85 o -0.6 (n = 144).
suppressPackageStartupMessages(library(forecast))
set.seed(20261123)
for (Th0 in c(-0.6, -0.85, -0.95)) {
  r <- t(replicate(300, {
    w <- arima.sim(list(ma = c(-0.4, rep(0,10), Th0, -0.4*Th0)), n = 131)
    y <- ts(diffinv(diffinv(as.numeric(w), lag = 12), lag = 1), frequency = 12)  # se ajusta con D = 1 y d = 1: no sobra nada
    f <- tryCatch(Arima(y, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12)), error = function(e) NULL)
    if (is.null(f)) return(c(NA, NA))
    Th <- coef(f)[["sma1"]]; e <- sqrt(diag(f$var.coef))[["sma1"]]
    c(Th, (Th + 1) / e)
  }))
  cat(sprintf("Theta verdadero %.2f: alarma (dist < 1.96) en %d de %d; e.e. NaN %d; Theta_hat < -0.99 en %d\n",
      Th0, sum(r[,2] < 1.96, na.rm = TRUE), sum(!is.na(r[,1])), sum(is.nan(r[,2])), sum(r[,1] < -0.99, na.rm = TRUE)))
}
