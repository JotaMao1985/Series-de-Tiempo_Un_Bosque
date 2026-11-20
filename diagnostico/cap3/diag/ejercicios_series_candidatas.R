# Diagnóstico cap. 3 · series de R base medidas para los huecos de práctica (§8–§9).
# Rscript --vanilla diagnostico/cap3/diag/ejercicios_series_candidatas.R > diagnostico/cap3/diag/ejercicios_series_candidatas.out 2>&1
suppressMessages({library(forecast); library(tseries)})
options(width = 120)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
fuera <- function(x, n) paste(which(abs(x) > 1.96/sqrt(n)), collapse = ",")
rejilla <- list(c(1,0), c(2,0), c(3,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))

mide <- function(nombre, y, lb_h = 10) {
  n <- length(y)
  a <- acf(y, lag.max = 20, plot = FALSE)$acf[-1]
  p <- as.numeric(pacf(y, lag.max = 20, plot = FALSE)$acf)
  cat(sprintf("\n--- %s  n = %d  banda = %.3f\n", nombre, n, 1.96/sqrt(n)))
  cat("  ACF 1:5 ", sprintf("%.3f", a[1:5]), "| fuera:", fuera(a, n), "\n")
  cat("  PACF 1:5", sprintf("%.3f", p[1:5]), "| fuera:", fuera(p, n), "\n")
  res <- do.call(rbind, lapply(rejilla, function(pq) {
    f <- tryCatch(arima(y, order = c(pq[1], 0, pq[2]), method = "ML"), error = function(e) NULL)
    if (is.null(f)) return(NULL)
    data.frame(m = sprintf("ARMA(%d,%d)", pq[1], pq[2]), AICc = round(aicc(f, n), 2), BIC = round(BIC(f), 2),
               LB = round(Box.test(residuals(f), lag = lb_h, type = "Ljung-Box", fitdf = sum(pq))$p.value, 4))
  }))
  res <- res[order(res$AICc), ]
  cat("  mejores por AICc:", paste(sprintf("%s %.2f (BIC %.2f, LB%d p %.3f)", res$m, res$AICc, res$BIC, lb_h, res$LB)[1:3], collapse = " · "), "\n")
  cat("  mínimo BIC:", res$m[which.min(res$BIC)], "\n")
  rb <- arima(y, order = c(0,0,0), method = "ML")
  cat(sprintf("  ruido blanco: AICc %.2f; LB%d sobre la serie p = %.4f\n", aicc(rb, n), lb_h,
              Box.test(y, lag = lb_h, type = "Ljung-Box")$p.value))
  invisible(res)
}

mide("lynx (crudo)", lynx)
mide("log(lynx)", log(lynx))
f <- arima(log(lynx), order = c(2,0,0), method = "ML"); r <- polyroot(c(1, -coef(f)[1:2]))
cat("  AR(2) log(lynx): phi", round(coef(f)[1:2], 4), " |raíz|", round(Mod(r[1]), 4), " periodo", round(2*pi/Arg(r[1]), 2), "\n")
cat("  Guerrero lynx:", round(BoxCox.lambda(lynx, method = "guerrero"), 4), " min", min(lynx), "\n")
mide("LakeHuron", LakeHuron)
mide("Nile", Nile)
mide("diff(Nile)", diff(Nile))
m <- arima(diff(Nile), order = c(0,0,1), method = "ML"); cat("  MA(1) sobre diff(Nile): theta", round(coef(m)[1], 4), "\n")
mide("diff(WWWusage)", diff(WWWusage))
mide("diff(BJsales)", diff(BJsales))
mide("nhtemp", nhtemp)
mide("discoveries", discoveries)
mide("sqrt(discoveries)", sqrt(discoveries))
dax <- diff(log(EuStockMarkets[, "DAX"])) * 100
mide("rendimientos DAX (%)", dax)
cat("  LB12 de los cuadrados:", signif(Box.test(dax^2, lag = 12, type = "Ljung-Box")$p.value, 3), "\n")
mide("treering (n grande)", treering)

## Estimadores (M7) sobre otra serie: YW, CSS y ML en log(lynx)
cat("\n--- M7 · tres estimadores sobre log(lynx), AR(2)\n")
y <- log(lynx)
yw <- ar(y, order.max = 2, aic = FALSE, method = "yule-walker")
cs <- arima(y, order = c(2,0,0), method = "CSS"); ml <- arima(y, order = c(2,0,0), method = "ML")
ee <- sqrt(diag(ml$var.coef))[1:2]
cat("  YW ", round(yw$ar, 4), " CSS", round(coef(cs)[1:2], 4), " ML", round(coef(ml)[1:2], 4),
    "\n  (YW-ML)/ee", round((yw$ar - coef(ml)[1:2])/ee, 2), " (CSS-ML)/ee", round((coef(cs)[1:2] - coef(ml)[1:2])/ee, 2), "\n")
cat("  LakeHuron AR(2): YW", round(ar(LakeHuron, order.max=2, aic=FALSE)$ar, 4),
    " ML", round(coef(arima(LakeHuron, order=c(2,0,0), method="ML"))[1:2], 4), "\n")

## M2/M3/M5 · procesos teóricos para ejercicios a mano (que no coincidan con los ejemplos)
cat("\n--- Procesos teóricos candidatos\n")
for (th in list(c(1.2, 0.5), c(-0.9, 0.4), c(0.5, -0.6), c(0.9, 0.2))) {
  cat(sprintf("  MA(2) theta=(%.1f, %.1f): |raíces| %s  rho %s  gamma0 %.2f\n", th[1], th[2],
      paste(round(Mod(polyroot(c(1, th))), 4), collapse = " "),
      paste(round(ARMAacf(ma = th, lag.max = 3)[-1], 4), collapse = " "), 1 + sum(th^2)))
}
for (ph in list(c(0.4, 0.4), c(-0.5, 0.3), c(1.2, -0.5), c(0.9, -0.2))) {
  r <- polyroot(c(1, -ph)); rho <- ARMAacf(ar = ph, lag.max = 3)[-1]
  g0 <- 1 / (1 - sum(ph * rho[1:2]))
  cat(sprintf("  AR(2) phi=(%.1f, %.1f): |raíces| %s  rho %s  gamma0/s2 %.4f  pacf %s\n", ph[1], ph[2],
      paste(round(Mod(r), 4), collapse = " "), paste(round(rho, 4), collapse = " "), g0,
      paste(round(ARMAacf(ar = ph, lag.max = 3, pacf = TRUE), 4), collapse = " ")))
}
for (pt in list(c(0.6, -0.3), c(-0.5, 0.8), c(0.8, -0.8))) {
  cat(sprintf("  ARMA(1,1) phi=%.1f theta=%.1f: rho %s  gamma0/s2 %.4f  psi %s\n", pt[1], pt[2],
      paste(round(ARMAacf(ar = pt[1], ma = pt[2], lag.max = 3)[-1], 4), collapse = " "),
      (1 + 2*pt[1]*pt[2] + pt[2]^2)/(1 - pt[1]^2),
      paste(round(ARMAtoMA(ar = pt[1], ma = pt[2], lag.max = 4), 4), collapse = " ")))
}

## M6 · FPP3 9.11 ej. 6 f: AR(2) phi = (-0.8, 0.3) no estacionario
cat("\n--- FPP3 9.11 ej. 6f: AR(2) phi = (-0.8, 0.3)\n")
cat("  |raíces|", round(Mod(polyroot(c(1, 0.8, -0.3))), 4), " phi2 - phi1 =", 0.3 + 0.8, "\n")

## M6 · cuántas barras fuera en ruido blanco con 20 rezagos: n = 50, 200, 1000
set.seed(20948)
for (nn in c(50, 200, 1000)) {
  k <- replicate(2000, sum(abs(acf(rnorm(nn), lag.max = 20, plot = FALSE)$acf[-1]) > 1.96/sqrt(nn)))
  cat(sprintf("  RB n = %4d: barras fuera de 20 — media %.2f, P(>=2) = %.3f, P(>=3) = %.3f\n", nn, mean(k), mean(k >= 2), mean(k >= 3)))
}

## E1 · auto.arima sin búsqueda escalonada
cat("\n--- lh: auto.arima(stepwise = FALSE)\n"); print(auto.arima(lh, stepwise = FALSE, approximation = FALSE))
