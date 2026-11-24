# Verificador independiente A · R1 del capítulo 5
# Recalcula las cifras nuevas o cambiadas del diff contra 7686d33.
# Ejecutar desde la raíz del repo:
#   LC_ALL=en_US.UTF-8 Rscript diagnostico/cap5/comprobaciones/v1a_comprobaciones.R
suppressPackageStartupMessages({ library(forecast); library(tseries) })
cat(R.version.string, " forecast", as.character(packageVersion("forecast")), "\n")
ap <- log(AirPassengers)
fit <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
th <- coef(fit)[["ma1"]]; TH <- coef(fit)[["sma1"]]
ee <- sqrt(diag(fit$var.coef))

cat("\n== M1: ACF de nabla nabla_12 log AP, rezagos fuera de banda ==\n")
w <- diff(diff(ap, lag = 12))
a <- Acf(w, lag.max = 36, plot = FALSE)$acf[-1]
banda1 <- 1.96 / sqrt(length(ap)); banda2 <- 1.96 / sqrt(length(w))
cat("banda con n=144:", round(banda1, 4), " con n=131:", round(banda2, 4), "\n")
print(round(a[abs(a) > banda1], 4)); print(which(abs(a) > banda1))
print(which(abs(a) > banda2))

cat("\n== M1/M8: TRM desde la copia congelada ==\n")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015,1), frequency = 12)
cat("n =", length(trm), "\n")
b <- Acf(diff(trm), lag.max = 36, plot = FALSE)$acf
print(round(b[c(13, 25, 37)], 4)); print(b[13], digits = 10)
g <- Arima(trm, order = c(0,1,0), seasonal = list(order = c(1,0,0), period = 12))
print(round(c(Phi = coef(g)[1], ee = sqrt(diag(g$var.coef))[1], t = coef(g)[1]/sqrt(diag(g$var.coef))[1]), 4))
print(round(c(forzado = g$aicc, simple = Arima(trm, order = c(0,1,0))$aicc), 3))
print(c(seas = nsdiffs(trm), ocsb = nsdiffs(trm, test = "ocsb")))

cat("\n== M2: gamma0/sigma2, q alcanza a m, AR no factoriza ==\n")
print(round(unname((1 + th^2) * (1 + TH^2)), 4))
print(round(unname(fit$sigma2 * (1 + th^2) * (1 + TH^2)), 6))
ma12 <- c(rep(0, 11), 0.5 + 0.6, rep(0, 11), 0.5 * 0.6)
cat(sprintf("exacta %.3f  factorizada %.3f\n", 1 + sum(ma12^2), (1 + 0.5^2) * (1 + 0.6^2)))
Phi <- 0.7
for (phi in c(0.6, 0.8, 0.9, 0.95)) {
  psi <- c(1, ARMAtoMA(ar = c(phi, rep(0, 10), Phi, -phi * Phi), lag.max = 20000))
  ex <- sum(psi^2); fa <- 1 / ((1 - phi^2) * (1 - Phi^2))
  cat(sprintf("phi=%.2f  phi^12=%.3f  exacta=%7.3f  factorizada=%7.3f  error=%6.1f %%\n",
              phi, phi^12, ex, fa, 100 * (fa / ex - 1)))
}
# Comprobacion de la condicion 2q < m para la ACF: MA(q) x SMA(1) con q = 7, m = 12
acf_ma <- function(ma) unname(ARMAacf(ma = ma, lag.max = 36))   # rho_0 en la posicion 1
mult <- function(a, b) { r <- rep(0, length(a) + length(b) - 1); for (i in seq_along(a)) for (j in seq_along(b)) r[i+j-1] <- r[i+j-1] + a[i]*b[j]; r }
reg7 <- c(1, rep(0.3, 7)); est <- c(1, rep(0, 11), 0.6)
r_full <- acf_ma(mult(reg7, est)[-1])
r_reg  <- acf_ma(reg7[-1]); r_est <- acf_ma(est[-1])
# producto teorico en el rezago 5 = rho_reg(5) * rho_est(0) + ... ; con 2q < m sería rho_reg(5)
cat("q=7, m=12: rho_5 exacto", round(r_full[6], 5), " producto rho_reg(5)*rho_est(0)", round(r_reg[6], 5), "\n")
reg5 <- c(1, rep(0.3, 5)); r_full5 <- acf_ma(mult(reg5, est)[-1]); r_reg5 <- acf_ma(reg5[-1])
cat("q=5, m=12: rho_5 exacto", round(r_full5[6], 5), " producto", round(r_reg5[6], 5),
    "  rho_13 exacto", round(r_full5[14], 5), " producto", round(r_reg5[2]*r_est[13], 5), "\n")

cat("\n== M3: nabla sola, rho_12; sobrediferenciacion ==\n")
print(round(Acf(diff(ap), lag.max = 12, plot = FALSE)$acf[13], 4))
for (D in 0:2) {
  f <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,D,1), period = 12))
  Th <- coef(f)[["sma1"]]; e <- sqrt(diag(f$var.coef))[["sma1"]]
  cat(sprintf("D=%d  Theta=%+.6f (e.e. %.6f)  a -1: %6.3f e.e.  |raiz MA|^-1=%.4f  |Th|^(1/12)=%.4f\n",
      D, Th, e, (Th + 1) / e, max(Mod(1/polyroot(c(1, f$model$theta)))), abs(Th)^(1/12)))
}
cat("Variancias: \n")
print(round(c(d0D0 = var(ap), d1D0 = var(diff(ap)), d0D1 = var(diff(ap, 12)), d1D1 = var(w)), 6))
r1 <- Acf(ap, plot = FALSE, lag.max = 12)$acf
cat("2(1-r1) =", round(2*(1-r1[2]), 4), " cociente real =", round(var(diff(ap))/var(ap), 4), "\n")
cat("2(1-r12) =", round(2*(1-r1[13]), 4), " cociente real =", round(var(diff(ap,12))/var(ap), 4), "\n")

cat("\n== Criterio e.e. en los casos del cap. 4 (Nilo d = 2, lynx ARIMA(2,1,1)) ==\n")
for (d in 1:3) {
  f <- tryCatch(Arima(Nile, order = c(0, d, 1)), error = function(e) NULL)
  if (!is.null(f)) cat(sprintf("Nilo d=%d  theta=%+.6f  e.e.=%s  a -1 = %s e.e.\n", d, coef(f)[["ma1"]],
      format(sqrt(diag(f$var.coef))[["ma1"]], digits = 4),
      format((coef(f)[["ma1"]] + 1)/sqrt(diag(f$var.coef))[["ma1"]], digits = 4)))
}
fl <- Arima(log(lynx), order = c(2,1,1))
print(round(cbind(coef = coef(fl), ee = sqrt(diag(fl$var.coef))), 6))
cat("lynx ma1 a -1:", (coef(fl)[["ma1"]] + 1)/sqrt(diag(fl$var.coef))[["ma1"]], "e.e.\n")
# Simulacion: ruido blanco con D sobrante, frecuencia del pegado y del criterio
set.seed(20261123)
res <- t(replicate(200, {
  e <- ts(rnorm(144), frequency = 12)
  y <- ts(cumsum(e), frequency = 12)          # caminata: d = 1 basta, D = 1 sobra
  f <- tryCatch(Arima(y, order = c(0,1,0), seasonal = list(order = c(0,1,1), period = 12)), error = function(e) NULL)
  if (is.null(f)) return(c(NA, NA))
  Th <- coef(f)[["sma1"]]; e2 <- sqrt(diag(f$var.coef))[["sma1"]]
  c(Th, (Th + 1)/e2)
}))
cat("Simulacion D sobrante (200): Theta mediana", round(median(res[,1], na.rm=TRUE), 4),
    "; e.e. NaN o NA:", sum(is.na(res[,2])),
    "; criterio avisa (dist < 1.96):", sum(res[,2] < 1.96, na.rm = TRUE),
    "; no avisa:", sum(res[,2] >= 1.96, na.rm = TRUE), "\n")
print(summary(res[,2]))

cat("\n== M4: AR(1) x SAR(1) ==\n")
ar <- c(0.6, rep(0, 10), 0.7, -0.42)
r <- unname(ARMAacf(ar = ar, lag.max = 36)[-1])
print(round(c(rho11 = r[11], rho13 = r[13], prod = r[1] * r[12]), 7))
print(round(r[c(1, 11, 12, 13, 24)], 4))

cat("\n== M5: pesos psi y sigma_h ==\n")
psi <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = c(th, rep(0, 10), TH, th * TH), lag.max = 600))
print(round(psi[c(1, 11, 12, 13) + 1], 4))
print(round(c(salto = psi[13] - psi[12], uno_mas_Theta = 1 + TH), 6))
print(round(psi[c(24, 60, 120, 240) + 1], 4))
inc <- psi[(13:600) + 1] - psi[(1:588) + 1]
cat("subida anual (j>=13): min", round(min(inc), 10), " max", round(max(inc), 10), " producto", round((1+th)*(1+TH), 6), "\n")
cat("subida j=12:", round(psi[13]-psi[1], 6), "\n")
sh <- sqrt(cumsum(psi^2))
h <- c(1, 12, 24, 36, 41, 42, 120, 240)
print(round(rbind(airline = sh[h], caminata = sqrt(h)), 4))
dif <- sh - sqrt(seq_along(sh))
cat("primer h en que supera:", min(which(dif > 0)), "; ultimo h <= 0 tras 42:",
    if (any(dif[42:length(dif)] <= 0)) max(which(dif[42:length(dif)] <= 0)) + 41 else "ninguno", "\n")
cat("sigma_1, 12, 24:", round(sqrt(fit$sigma2) * sh[c(1, 12, 24)], 6), "\n")
cat("cociente sh^2 / h^3 en h = 60, 120, 240, 600:", signif(sh[c(60,120,240,600)]^2 / c(60,120,240,600)^3, 4), "\n")
cat("constante asintotica c^2/3 con c = (1+th)(1+TH)/12:", signif(((1+th)*(1+TH)/12)^2/3, 4), "\n")
cat("crecimiento de sh^2 entre 120 y 240 (h^3 daria 8):", round(sh[240]^2/sh[120]^2, 3), "\n")
cat("sigma_12/sigma_1 =", round(sh[12], 4), " sqrt(12) =", round(sqrt(12), 4), "\n")

cat("\n== M6: Ljung-Box sin arranque y el modelo sin ARMA ==\n")
print(round(Box.test(residuals(fit), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4))
print(round(Box.test(residuals(fit)[-(1:13)], lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4))
print(round(residuals(fit)[1:14], 6))
f0 <- Arima(ap, order = c(0,1,0), seasonal = list(order = c(0,1,0), period = 12))
print(round(f0$aicc, 2)); print(signif(Box.test(residuals(f0), lag = 24, type = "Ljung-Box")$p.value, 3))

cat("\n== M7: salida de R y psi con th, TH ==\n")
print(round(c(coef(fit), sigma2 = fit$sigma2, aicc = fit$aicc), 6))
print(round(ee, 4))
psi23 <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = c(th, rep(0, 10), TH, th * TH), lag.max = 23))
print(round(psi23[c(1, 2, 12, 13, 14)], 4))
print(round(sqrt(cumsum(psi23^2) * fit$sigma2)[c(1, 12, 24)], 6))

cat("\n== M9: calendario ==\n")
dias <- as.numeric(monthdays(ap))
# Semana Santa con timeDate::Easter (independiente del algoritmo del generador)
pas <- as.Date(timeDate::Easter(1949:1960))
mes_pas <- as.numeric(format(pas, "%m"))
anio <- floor(time(ap) + 1e-6); mes <- cycle(ap)
pascua <- as.numeric(mes == mes_pas[anio - 1948])
cat("meses con Pascua:", sum(pascua), "\n")
fp <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12), xreg = cbind(pascua = pascua))
print(round(c(aicc = fp$aicc, bic = fp$bic), 4))
print(round(cbind(coef = coef(fp), ee = sqrt(diag(fp$var.coef)), t = coef(fp)/sqrt(diag(fp$var.coef))), 4))
fd <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12), xreg = cbind(log_dias = log(dias), pascua = pascua))
print(round(cbind(coef = coef(fd), ee = sqrt(diag(fd$var.coef))), 4))
cat("t(beta = 1) =", round((coef(fd)[["log_dias"]] - 1)/sqrt(diag(fd$var.coef))[["log_dias"]], 4), "\n")
cat("AICc airline:", round(fit$aicc, 4), " mejora Semana Santa sola:", round(fit$aicc - fp$aicc, 4), "\n")

cat("\n== M10: tope de auto.arima, stlm ==\n")
set.seed(1)
cat(grep("max.P <-|max.Q <-|serieslength <-", deparse(forecast::auto.arima), value = TRUE), sep = "\n")
s <- stlm(ap, s.window = "periodic", method = "arima")
print(as.character(s$model)); print(round(c(aic = s$model$aic, aicc = s$model$aicc), 2))

cat("\n== Quiz 6: parametros de la armonica K = 5 ==\n")
m5 <- auto.arima(ap, xreg = fourier(ap, K = 5), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
print(m5); cat("coeficientes estimados:", length(coef(m5)), " + sigma2 =", length(coef(m5)) + 1, "\n")
print(round(m5$aicc, 4))

cat("\n== E1: co2 ==\n")
a <- Acf(diff(co2), lag.max = 36, plot = FALSE)$acf
print(round(c(r12 = a[13], r24 = a[25], r36 = a[37], banda = 1.96 / sqrt(length(co2) - 1)), 4))
conD <- Arima(co2, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
print(round(cbind(coef = coef(conD), ee = sqrt(diag(conD$var.coef)),
            a_menos_1 = (coef(conD) + 1) / sqrt(diag(conD$var.coef))), 4))

cat("\n== E3(b): armonicos sobre co2 ==\n")
mods <- list()
for (K in 1:6) {
  xr <- fourier(co2, K = K)
  f <- mods[[K]] <- auto.arima(co2, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  cat(sprintf("K=%d  %s  n_ef=%d  AICc=%8.3f  LB=%.4f\n", K, as.character(f), f$nobs,
      f$aicc, Box.test(residuals(f), lag = 24, type = "Ljung-Box", fitdf = sum(f$arma[1:4]))$p.value))
}
print(round(c(armonico_K4 = mods[[4]]$aicc, n_armonico = mods[[4]]$nobs,
        airline = conD$aicc, n_airline = conD$nobs), 3))
print(round(c(armonico_K4 = Box.test(residuals(mods[[4]]), lag = 24, type = "Ljung-Box",
                               fitdf = sum(mods[[4]]$arma[1:4]))$p.value,
        airline = Box.test(residuals(conD), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value), 4))
print(round(Box.test(residuals(conD)[-(1:13)], lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4))
