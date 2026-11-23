# Lector F · R4 cap. 4 · comprobaciones de software (R 4.6.0, forecast, tseries)
suppressMessages({library(forecast)})
cat("R", as.character(getRversion()), " forecast", as.character(packageVersion("forecast")), "\n\n")

cat("== 1. sigma2 de arima() frente a Arima(): ¿es CSS-ML frente a ML, o el divisor?\n")
chk <- function(y, order, nom) {
  fa  <- arima(y, order = order, method = "ML")              # stats::arima, MLE
  fb  <- Arima(y, order = order)                              # forecast::Arima, método por defecto (CSS-ML)
  fc  <- Arima(y, order = order, method = "ML")               # forecast::Arima, ML explícito
  n   <- length(y); d <- order[2]; nstar <- n - d; pq <- order[1] + order[3]
  ss  <- sum(residuals(fa)^2)
  cat(sprintf("%s: n=%d, n*=%d, p+q=%d\n", nom, n, nstar, pq))
  cat(sprintf("  sigma2 arima(ML)           = %.4f   (SC/n*       = %.4f)\n", fa$sigma2, ss / nstar))
  cat(sprintf("  sigma2 Arima(CSS-ML)       = %.4f\n", fb$sigma2))
  cat(sprintf("  sigma2 Arima(method='ML')  = %.4f\n", fc$sigma2))
  cat(sprintf("  razon Arima/arima          = %.5f   n*/(n*-p-q) = %.5f\n", fb$sigma2 / fa$sigma2, nstar / (nstar - pq)))
  cat(sprintf("  SC residuales de Arima/(n*-p-q) = %.4f\n", sum(residuals(fb)^2) / (nstar - pq)))
}
chk(Nile, c(1, 1, 1), "Nile ARIMA(1,1,1)")
chk(BJsales, c(1, 1, 1), "BJsales ARIMA(1,1,1)")
cat("\nCodigo de Arima(): lineas que mencionan sigma2\n")
print(grep("sigma2", deparse(body(forecast::Arima)), value = TRUE))
cat("\n?Arima Value (sigma2) y ?arima Value (sigma2) se leyeron en la cache: 'bias adjusted MLE' frente a 'the MLE'.\n")

cat("\n== 2. lynx: varianza al diferenciar, r1, 2(1-r1) y periodo del AR(2)\n")
ly <- log(lynx)
v <- sapply(0:3, function(d) var(if (d == 0) ly else diff(ly, differences = d)))
cat("var(d=0..3) =", round(v, 4), "  caida d=0->1 =", round(100 * (1 - v[2] / v[1]), 1), "%  minimo en d =", which.min(v) - 1, "\n")
r1 <- acf(ly, plot = FALSE)$acf[2]
cat(sprintf("r1 = %.3f  cociente = %.3f  2(1-r1) = %.3f\n", r1, var(diff(ly)) / var(ly), 2 * (1 - r1)))
f <- arima(ly, order = c(2, 0, 0), method = "ML")
ph <- coef(f)[1:2]
r <- polyroot(c(1, -ph))
cat(sprintf("AR(2): phi1 = %.4f phi2 = %.4f  periodo por raiz = %.4f\n", ph[1], ph[2], 2 * pi / Arg(r[which.max(Im(r))])))
cat(sprintf("  condicion de ciclo phi1^2 + 4 phi2 = %.4f (<0: ciclico)\n", ph[1]^2 + 4 * ph[2]))
cat(sprintf("  periodo medio segun la formula de FPP3 9.5: 2pi/acos(-phi1(1-phi2)/(4 phi2)) = %.4f\n",
            2 * pi / acos(-ph[1] * (1 - ph[2]) / (4 * ph[2]))))
cat(sprintf("n = %d, tiempo %d-%d\n", length(lynx), start(lynx)[1], end(lynx)[1]))

cat("\n== 3. BJsales: n, rango, aicc d=1 frente a d=2 (n efectivo)\n")
cat("length(BJsales) =", length(BJsales), " class:", class(BJsales), " start/end:", start(BJsales), end(BJsales), "\n")
cat("IMA(1,1) = ARIMA(0,1,1): arima(BJsales, c(0,1,1)) coef ma1 =", round(coef(arima(BJsales, order = c(0, 1, 1), method = "ML")), 4), "\n")
cat("p Ljung-Box(20, fitdf=1) del (0,1,1):",
    round(Box.test(residuals(arima(BJsales, order = c(0, 1, 1), method = "ML")), lag = 20, type = "Ljung-Box", fitdf = 1)$p.value, 4), "\n")
