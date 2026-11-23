# Verificador A, R5 cap. 4: comprobacion independiente de los «Para practicar» M1-M9
suppressPackageStartupMessages({library(forecast); library(tseries); library(tsibbledata)})
cat("R", as.character(getRversion()), " forecast", as.character(packageVersion("forecast")), "\n")
LB <- function(f, k, lag = 20) Box.test(residuals(f), lag = lag, type = "Ljung-Box", fitdf = k)$p.value

cat("\n==== M1 tcm1y ====\n")
data(tcm); y <- tcm1y
print(tsp(y)); cat("n =", length(y), " NA:", sum(is.na(y)), "\n")
a2 <- Arima(y, order = c(2,0,0), method = "ML"); a1 <- Arima(y, order = c(1,1,0), method = "ML")
print(round(c(loglik_AR2 = a2$loglik, loglik_110 = a1$loglik, s2_AR2 = a2$sigma2, s2_110 = a1$sigma2), 3))
# desviacion tipica incondicional del AR(2) ajustado (limite del ee de prediccion)
ph <- coef(a2)[1:2]; psi <- ARMAtoMA(ar = ph, lag.max = 5000)
cat("sd incondicional del AR(2) =", round(sqrt(a2$sigma2 * (1 + sum(psi^2))), 3), "  sd(y) =", round(sd(y), 3), "\n")
pp <- predict(arima(y, order = c(2,0,0), method = "ML"), n.ahead = 600)
print(round(pp$se[c(12, 60, 120, 240, 600)], 3))
cat("1/phi del 110:", round(1 / coef(a1)[["ar1"]], 4), "\n")

cat("\n==== M2 simulacion ARIMA(2,1,0) ====\n")
uno <- function(s) {
  set.seed(s); y <- arima.sim(n = 200, model = list(order = c(2,1,0), ar = c(0.4, 0.3)))
  f1 <- try(arima(y, order = c(0,1,1), method = "ML"), silent = TRUE)
  f2 <- try(arima(y, order = c(2,2,1), method = "ML"), silent = TRUE)
  f3 <- try(arima(y, order = c(2,1,2), method = "ML"), silent = TRUE)
  f0 <- try(arima(y, order = c(2,1,0), method = "ML"), silent = TRUE)
  if (any(sapply(list(f1, f2, f3, f0), inherits, "try-error"))) return(rep(NA, 4))
  ee3 <- sqrt(diag(f3$var.coef)); ee0 <- sqrt(diag(f0$var.coef))
  c(lb011_rechaza = LB(f1, 1) < 0.05,
    raiz221_menor_1.01 = min(Mod(polyroot(c(1, coef(f2)[["ma1"]])))) < 1.01,
    ee212_max_mayor_2x = max(ee3, na.rm = TRUE) > 2 * max(ee0),
    pacf_corta_en_2 = { p <- pacf(diff(y), lag.max = 6, plot = FALSE)$acf[,1,1]; b <- 1.96/sqrt(199)
                        all(abs(p[1:2]) > b) && all(abs(p[3:6]) < b) })
}
m <- t(sapply(1:200, function(s) suppressWarnings(uno(s))))
print(round(colMeans(m, na.rm = TRUE), 3)); cat("semilla 2026:\n"); print(suppressWarnings(uno(2026)))
set.seed(2026); y <- arima.sim(n = 200, model = list(order = c(2,1,0), ar = c(0.4, 0.3)))
f3 <- arima(y, order = c(2,1,2), method = "ML")
cat("ARIMA(2,1,2): |raices AR| =", round(Mod(polyroot(c(1, -coef(f3)[1:2]))), 4),
    "  |raices MA| =", round(Mod(polyroot(c(1, coef(f3)[3:4]))), 4), "\n")

cat("\n==== M3 escalon + AR(1) ====\n")
pr <- function(x) c(kpss = ndiffs(x, test = "kpss"), adf = ndiffs(x, test = "adf"), pp = ndiffs(x, test = "pp"))
r3 <- t(sapply(1:500, function(s) {
  set.seed(s); e <- as.numeric(1:120 >= 71)
  y <- ts(10 + 3 * e + arima.sim(n = 120, model = list(ar = 0.5)))
  f <- try(suppressWarnings(arima(y, order = c(1,1,1), method = "ML")), silent = TRUE)
  raiz <- if (inherits(f, "try-error")) NA else Mod(polyroot(c(1, coef(f)[["ma1"]])))
  c(kpss_total = ndiffs(y, test = "kpss"),
    tramos_0 = ndiffs(window(y, end = 70), test = "kpss") == 0 && ndiffs(window(y, start = 71), test = "kpss") == 0,
    tramos_0_3pruebas = all(pr(window(y, end = 70)) == 0) && all(pr(window(y, start = 71)) == 0),
    raiz = raiz)
}))
print(round(c(kpss_pide_1_total = mean(r3[,1] >= 1), kpss_0_en_tramos = mean(r3[,2]),
              tres_pruebas_0_en_tramos = mean(r3[,3]), mediana_raiz = median(r3[,4], na.rm = TRUE), fallos_111 = sum(is.na(r3[,4]))), 3))

cat("\n==== M4 global_economy Colombia ====\n")
col <- subset(as.data.frame(global_economy), Country == "Colombia")
y <- ts(col$Imports, start = 1960); cat("n =", length(y), " NA:", sum(is.na(y)), " rango anios:", range(col$Year), "\n")
print(pr(y))
for (o in list(c(0,1,1), c(1,1,0), c(1,1,1), c(0,1,0))) {
  f <- Arima(y, order = o, method = "ML")
  cat(sprintf("Arima(%d,1,%d) AICc=%.3f BIC=%.3f\n", o[1], o[3], f$aicc, f$bic))
}
th <- -0.291; r1 <- th / (1 + th^2); cat("MA(1) theta=-0.291: rho1 =", round(r1, 3), " pacf2 =", round(-r1^2 / (1 - r1^2), 3), "\n")
cat("AR(1) phi=-0.285: rho2 =", round(0.285^2, 3), "\n")
cat("MA(1) con theta=-0.29 exacto: pacf2 =", round(ARMAacf(ma = -0.29, lag.max = 2, pacf = TRUE)[2], 3),
    "  AR(1) phi=-0.29: acf2 =", round(ARMAacf(ar = -0.29, lag.max = 2)[3], 3), "\n")

cat("\n==== M5 airmiles ====\n")
y <- log(airmiles); print(tsp(airmiles))
sin <- Arima(y, order = c(0,1,1)); con <- Arima(y, order = c(0,1,1), include.drift = TRUE)
print(round(c(coef(con), aicc_sin = sin$aicc, aicc_con = con$aicc, mean_diff = mean(diff(y))), 4))
sinML <- Arima(y, order = c(0,1,1), method = "ML"); conML <- Arima(y, order = c(0,1,1), include.drift = TRUE, method = "ML")
print(round(c(aicc_sin_ML = sinML$aicc, aicc_con_ML = conML$aicc, drift_ML = coef(conML)[["drift"]]), 3))
print(round(c(LB_sin = LB(sin, 1), LB_con = LB(con, 1)), 3))

cat("\n==== M6 GOOG 2018 ====\n")
g <- subset(as.data.frame(gafa_stock), Symbol == "GOOG" & format(Date, "%Y") == "2018")
y <- ts(g$Close); cat("n =", length(y), " fechas:", format(range(g$Date)), "\n"); print(pr(y))
f010 <- arima(y, order = c(0,1,0), method = "ML")
f010d <- Arima(y, order = c(0,1,0), include.drift = TRUE, method = "ML")
f021 <- arima(y, order = c(0,2,1), method = "ML")
print(round(c(s2_010 = f010$sigma2, s2_010_drift = f010d$sigma2, s2_021 = f021$sigma2,
              var_diff = var(diff(y)), media_diff = mean(diff(y)), mean_sq_diff = mean(diff(y)^2)), 3))
cat("t de la deriva:", round(coef(f010d)[["drift"]] / sqrt(f010d$var.coef[1,1]), 3), "\n")
# AICc con forecast::Arima para comparar con la funcion casera
print(round(c(Arima_010 = Arima(y, order = c(0,1,0), method = "ML")$aicc, Arima_021 = Arima(y, order = c(0,2,1), method = "ML")$aicc), 3))

cat("\n==== M7 NelPlo ip ====\n")
data(NelPlo); ip <- na.omit(NelPlo[, "ip"]); print(tsp(ip)); print(round(range(ip), 3)); print(head(round(ip, 3)))
tr <- capture.output(ex <- auto.arima(ip, trace = TRUE, stepwise = FALSE, approximation = FALSE))
tr <- grep("^ ARIMA", tr, value = TRUE); print(grep("ARIMA\\(0,1,[0-5]\\) with drift", tr, value = TRUE))
for (q in 0:5) { f <- Arima(ip, order = c(0,1,q), include.drift = TRUE, method = "ML")
  cat(sprintf("(0,1,%d)+drift AICc = %.3f  LB(20,fitdf=q) p = %.4f\n", q, f$aicc, LB(f, q))) }
f010d <- Arima(ip, order = c(0,1,0), include.drift = TRUE)
cat("LB del (0,1,0)+deriva con fitdf=1 (contando la deriva):", round(LB(f010d, 1), 4), " lag 10:", round(LB(f010d, 0, 10), 4), "\n")
print(round(acf(residuals(f010d), lag.max = 8, plot = FALSE)$acf[-1], 3)); cat("banda", round(1.96/sqrt(length(ip)-1), 3), "\n")

cat("\n==== M8 AR(1) sobrediferenciado ====\n")
r8 <- t(sapply(1:200, function(s) {
  set.seed(s); y <- arima.sim(n = 200, model = list(ar = 0.8))
  f1 <- try(arima(y, order = c(0,1,1), method = "ML"), silent = TRUE); f2 <- try(arima(y, order = c(1,1,1), method = "ML"), silent = TRUE)
  if (inherits(f1, "try-error") || inherits(f2, "try-error")) return(rep(NA, 4))
  c(raiz111 = Mod(polyroot(c(1, coef(f2)[["ma1"]]))), raiz011 = Mod(polyroot(c(1, coef(f1)[["ma1"]]))),
    lb011 = LB(f1, 1), r1 = acf(diff(y), plot = FALSE)$acf[2])
}))
print(round(c(raiz111_menor_1.05 = mean(r8[,1] < 1.05, na.rm=TRUE), raiz011_menor_1.05 = mean(r8[,2] < 1.05, na.rm=TRUE),
              lb011_pasa = mean(r8[,3] > 0.05, na.rm=TRUE), r1_menor_menos0.4 = mean(r8[,4] < -0.4, na.rm=TRUE), mediana_r1 = median(r8[,4], na.rm=TRUE), fallos = sum(is.na(r8[,1]))), 3))

cat("\n==== M9 BJsales.lead ====\n")
f <- Arima(BJsales.lead, order = c(0,1,1)); th <- coef(f)[["ma1"]]; phi <- 0
j <- 0:11; psi_cerrada <- ((1 + th) - (phi + th) * phi^j) / (1 - phi); psi_cerrada[1] <- 1  # 0^0 = 1 en R
print(round(c(psi_cerrada[1:3], ARMAtoMA(ma = th, lag.max = 2)), 4))  # ojo: ARMAtoMA da los del ARMA, no del ARIMA
psi_arima <- c(1, ARMAtoMA(ar = c(1), ma = th, lag.max = 11))
print(round(psi_arima[1:4], 4))
fc <- forecast(f, h = 12, level = 95); s <- sqrt(f$sigma2)
print(round(c(s * sqrt(cumsum(psi_arima^2))[c(1, 2, 12)], ((fc$upper - fc$lower) / 2 / qnorm(0.975))[c(1, 2, 12)]), 4))
fd <- Arima(BJsales.lead, order = c(0,1,1), include.drift = TRUE)
print(round(c(drift = coef(fd)[["drift"]], aicc_sin = f$aicc, aicc_con = fd$aicc, dif = f$aicc - fd$aicc,
              sep12 = forecast(fd, h = 100)$mean[12] - forecast(f, h = 100)$mean[12],
              sep100 = forecast(fd, h = 100)$mean[100] - forecast(f, h = 100)$mean[100]), 3))
print(round(c(LB_sin = LB(f, 1), LB_con = LB(fd, 1)), 3)); print(pr(BJsales.lead))
