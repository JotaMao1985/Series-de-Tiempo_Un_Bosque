# par_verifica2.R — comprobaciones complementarias (M4, M5, M10) y referencias
# para el contraste del JS de los simuladores (par_simuladores.js).
suppressMessages(library(forecast)); options(width = 120)
sec <- function(t) cat("\n==================== ", t, " ====================\n", sep = "")
ap <- log(AirPassengers)
sec("M4 l. 4289-4290 · AR(1)xSAR(1): r11, r13 y el producto con 7 decimales")
r <- ARMAacf(ar = c(0.6, rep(0,10), 0.7, -0.42), lag.max = 13)
cat(sprintf("r11=%.7f r13=%.7f r1*r12=%.7f  r13-r1*r12=%.2e\n", r[["11"]], r[["13"]], r[["1"]]*r[["12"]], r[["13"]]-r[["1"]]*r[["12"]]))
sec("M5 · los pesos psi del airline crecen sin límite (dos raíces unitarias en B = 1)")
fit <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
th <- coef(fit)[[1]]; Th <- coef(fit)[[2]]
psi <- c(1, ARMAtoMA(ar = c(1, rep(0,10), 1, -1), ma = c(th, rep(0,10), Th, th*Th), lag.max = 240))
cat("psi_j en j = 1, 12, 13, 24, 25, 36, 60, 120, 240:", round(psi[c(1,12,13,24,25,36,60,120,240) + 1], 4), "\n")
cat("formula: psi_{12k+i} (i>=1) = (1+th)(1 + k(1+Th)); k=10, i=1:", round((1+th)*(1+10*(1+Th)), 4), "\n")
sec("M5 · referencias para el simulador airline-pesos (theta=-0.40, Theta=-0.56 por defecto)")
for (pp in list(c(-0.40,-0.56), c(th, Th))) {
  ps <- c(1, ARMAtoMA(ar = c(1, rep(0,10), 1, -1), ma = c(pp[1], rep(0,10), pp[2], pp[1]*pp[2]), lag.max = 40))
  sh <- sqrt(cumsum(ps^2) * fit$sigma2)
  cat(sprintf("theta=%.4f Theta=%.4f psi1=%.4f psi12=%.4f psi13=%.4f s1=%.6f s12=%.6f s24=%.6f s12/s1=%.3f\n",
              pp[1], pp[2], ps[2], ps[13], ps[14], sh[1], sh[12], sh[24], sh[12]/sh[1]))
}
sec("Referencias para firma-teorica (ACF y PACF teóricas)")
casos <- list(sar = list(ar = c(rep(0,11), 0.7), ma = numeric(0)),
              ar1sar1 = list(ar = c(0.6, rep(0,10), 0.7, -0.42), ma = numeric(0)),
              extremo = list(ar = c(0.85, rep(0,10), 0.85, -0.7225), ma = numeric(0)),
              mixto = list(ar = c(0.5, rep(0,10), -0.3, 0.15), ma = c(0.4, rep(0,10), -0.6, -0.24)))
for (nm in names(casos)) {
  a <- ARMAacf(ar = casos[[nm]]$ar, ma = casos[[nm]]$ma, lag.max = 36)[-1]
  p <- ARMAacf(ar = casos[[nm]]$ar, ma = casos[[nm]]$ma, lag.max = 36, pacf = TRUE)
  cat(sprintf("%-8s ACF[1,11,12,13,24,36] = %s | PACF[1,2,12,13,24] = %s\n", nm,
      paste(sprintf("%.4f", a[c(1,11,12,13,24,36)]), collapse = " "), paste(sprintf("%.4f", p[c(1,2,12,13,24)]), collapse = " ")))
}
sec("M10 l. 5517-5519 · por qué auto.arima no estima Phi ni Theta con m = 365")
cat("regla de auto.arima: max.P = min(2, floor(n/3/m)); con n = 800, m = 365 ->", min(2, floor(800/3/365)),
    "; con n = 156, m = 52 ->", min(2, floor(156/3/52)), "; n mínimo para P = 1 con m = 365:", 3*365, "\n")
sec("M5 · auto.arima exhaustivo sobre log(AirPassengers)")
cat(as.character(auto.arima(ap, stepwise = FALSE, approximation = FALSE)), "\n")
