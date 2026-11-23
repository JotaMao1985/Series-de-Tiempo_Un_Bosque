# par_verifica.R — recálculo independiente de las cifras de la prosa, las tablas
# y los simuladores del capítulo 5 (commit f807b40), módulos 1 a 10 y ejercicios.
# Uso: Rscript par_verifica.R > par_verifica.out 2>&1   (desde diagnostico/cap5/diag)
suppressMessages({ library(forecast); library(tseries); library(jsonlite) })
options(width = 120)
sec <- function(t) cat("\n==================== ", t, " ====================\n", sep = "")
raiz <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])), "../../.."))
csv <- read.csv(file.path(raiz, "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv"))
trm <- ts(csv$trm, start = c(2015, 1), frequency = 12)
ap <- log(AirPassengers); uad <- USAccDeaths
cat("R", R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| TRM congelada n =", length(trm), "\n")
acfk <- function(x, k) { a <- Acf(x, lag.max = max(k), plot = FALSE)$acf; a[k + 1] }
air <- function(y, ...) Arima(y, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12), ...)

sec("M1 · tabla de la l. 3141-3145")
for (nm in c("logAP", "USAccDeaths", "co2", "TRM", "dTRM")) {
  x <- switch(nm, logAP = ap, USAccDeaths = uad, co2 = co2, TRM = trm, dTRM = diff(trm))
  cat(sprintf("%-12s n=%3d  r1=%.4f r12=%.4f r24=%.4f r36=%.4f banda=%.4f\n", nm, length(x),
              acfk(x,1), acfk(x,12), acfk(x,24), acfk(x,36), 1.96/sqrt(length(x))))
}
sec("M1/M7 · ARIMA no estacional del cap. 4 y airline (l. 3076-3081, 4933-4936)")
m05 <- auto.arima(ap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
r05 <- residuals(m05); a05 <- Acf(r05, lag.max = 24, plot = FALSE)$acf
lb05 <- Box.test(r05, lag = 24, type = "Ljung-Box", fitdf = 5)
cat(as.character(m05), " r12 =", round(a05[13], 4), " r24 =", round(a05[25], 4),
    " Q24 =", round(lb05$statistic, 1), " p =", signif(lb05$p.value, 3), " nobs =", m05$nobs, "\n")
fit <- air(ap); rr <- residuals(fit); ar_res <- Acf(rr, lag.max = 36, plot = FALSE)$acf
cat("airline: coef =", round(coef(fit), 6), " sigma2 =", fit$sigma2, " r12 resid =", round(ar_res[13], 4),
    " LB24 p =", round(Box.test(rr, 24, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")

sec("M1 (l. 3109-3110) y M7 (l. 4865-4869) · barras fuera de banda en la ACF de nabla nabla12 log AP")
w <- diff(diff(ap, lag = 12)); aw <- Acf(w, lag.max = 36, plot = FALSE)$acf[-1]; bw <- 1.96/sqrt(length(w))
cat("n =", length(w), " banda =", round(bw, 4), "\n")
cat("rezagos 1-36 fuera de banda:", which(abs(aw) > bw), "\n")
print(round(aw[which(abs(aw) > bw)], 4))
cat("r11 =", round(aw[11], 4), " r13 =", round(aw[13], 4), " r3 =", round(aw[3], 4), " r9 =", round(aw[9], 4), " r23 =", round(aw[23], 4), "\n")
cat("residuales airline (n=144, banda 0.1633): r3 =", round(ar_res[4], 4), " r9 =", round(ar_res[10], 4),
    " r23 =", round(ar_res[24], 4), " fuera de banda (1-24):", which(abs(ar_res[2:25]) > 1.96/sqrt(144)), "\n")
cat("residuales airline sin los 13 primeros: banda", round(1.96/sqrt(131),4), " fuera (1-24):",
    which(abs(Acf(rr[-(1:13)], lag.max = 24, plot = FALSE)$acf[-1]) > 1.96/sqrt(131)), "\n")
cat("con la ACF de nabla log AP (n=143): r12, r24, r36 =", round(acfk(diff(ap), c(12,24,36)), 4), " banda", round(1.96/sqrt(143),4), "\n")

sec("M2 · varianzas y factorización")
cat("theta12=0.5, Theta=0.6: exacta", 1 + (0.5+0.6)^2 + (0.5*0.6)^2, " factorizada", (1+0.25)*(1+0.36), "\n")
th <- coef(fit)[["ma1"]]; Th <- coef(fit)[["sma1"]]
cat("(1+th^2)(1+Th^2) =", round((1+th^2)*(1+Th^2), 4), "  gamma0 =", round(fit$sigma2*(1+th^2)*(1+Th^2), 6),
    "  var muestral =", round(var(w), 6), "\n")
cat("sigma2 de forecast =", fit$sigma2, "\n")
cat("  SSR(144 resid)/(131-2) =", sum(rr^2)/129, "  SSR(144)/131 =", sum(rr^2)/131, "\n")
f_ml <- arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
cat("  sigma2 de stats::arima (ML) =", f_ml$sigma2, "\n")
for (phi in c(0.6, 0.8, 0.9, 0.95)) {
  Phi <- 0.7
  psi <- c(1, ARMAtoMA(ar = c(phi, rep(0, 10), Phi, -phi*Phi), lag.max = 20000))
  ex <- sum(psi^2); fa <- 1/((1-phi^2)*(1-Phi^2))
  cat(sprintf("phi=%.2f phi^12=%.3f exacta=%.3f factorizada=%.3f error=%.1f%%\n", phi, phi^12, ex, fa, 100*(fa-ex)/ex))
}
r <- ARMAacf(ar = c(0.6, rep(0,10), 0.7, -0.42), lag.max = 13)
cat("AR1xSAR1: r11 =", round(r[["11"]], 5), " r13 =", round(r[["13"]], 5), " r1*r12 =", round(r[["1"]]*r[["12"]], 5), "\n")
rm_ <- ARMAacf(ma = c(th, rep(0,10), Th, th*Th), lag.max = 13)
cat("airline exacto: r1 r11 r12 r13 =", round(rm_[c("1","11","12","13")], 5), " producto", round(rm_[["1"]]*rm_[["12"]], 5),
    " dif r13 - r1*r12 =", signif(rm_[["13"]] - rm_[["1"]]*rm_[["12"]], 3), "\n")

sec("M3 · crecimiento anual medio de log AP (l. 3885) y varianzas")
d12 <- diff(ap, lag = 12)
print(round(tapply(as.numeric(d12), floor(time(d12) + 1e-6), mean), 3))
cat("razones de varianza: var/var(d=1) =", round(var(ap)/var(diff(ap)), 2), " var/var(D=1) =", round(var(ap)/var(d12), 2), "\n")
for (D in 0:2) {
  y <- if (D == 0) ap else diff(ap, lag = 12, differences = D); y <- diff(y)
  f <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,D,1), period = 12))
  cat(sprintf("D=%d n=%d var=%.6f Theta=%+.4f ee=%.4f |raiz MA|^-1=%.4f  |Theta|^(1/12)=%.4f\n", D, length(y), var(y),
              coef(f)[["sma1"]], sqrt(diag(f$var.coef))[["sma1"]], max(Mod(1/polyroot(c(1, f$model$theta)))),
              abs(coef(f)[["sma1"]])^(1/12)))
}
sec("M3/M8 · ndiffs y nsdiffs (tabla l. 5112-5118), con la TRM congelada")
for (nm in c("logAP", "USAccDeaths", "co2", "TRM")) {
  x <- switch(nm, logAP = ap, USAccDeaths = uad, co2 = co2, TRM = trm)
  cat(sprintf("%-12s ndiffs=%d ndiffs_tras_D=%d nsdiffs_seas=%d nsdiffs_ocsb=%d\n", nm, ndiffs(x),
              ndiffs(diff(x, lag = 12)), nsdiffs(x), nsdiffs(x, test = "ocsb")))
}
cat("auto.arima(TRM congelada) =", as.character(auto.arima(trm, stepwise = FALSE, approximation = FALSE)), "\n")
g <- Arima(trm, order = c(0,1,0), seasonal = list(order = c(1,0,0), period = 12))
cat("TRM forzada: Phi =", round(coef(g)[1], 4), " ee =", round(sqrt(g$var.coef[1,1]), 4), " t =", round(coef(g)[1]/sqrt(g$var.coef[1,1]), 4),
    " AICc forzado =", round(g$aicc, 3), " simple =", round(Arima(trm, order = c(0,1,0))$aicc, 3), "\n")
cat("TRM: r12 de diff con 5 decimales =", round(acfk(diff(trm), 12), 5), "\n")

sec("M4 · tabla de la l. 4269-4276 (ACF teóricas)")
pr <- function(lbl, r) cat(sprintf("%-26s r1=%.4f r11=%.4f r12=%.4f r13=%.4f r24=%.4f\n", lbl, r[["1"]], r[["11"]], r[["12"]], r[["13"]], r[["24"]]))
pr("SAR1 0.7", ARMAacf(ar = c(rep(0,11), 0.7), lag.max = 24))
pr("SMA1 -0.6", ARMAacf(ma = c(rep(0,11), -0.6), lag.max = 24))
pr("AR1xSAR1 0.6/0.7", ARMAacf(ar = c(0.6, rep(0,10), 0.7, -0.42), lag.max = 24))
pr("airline -0.4018/-0.5569", ARMAacf(ma = c(-0.4018, rep(0,10), -0.5569, 0.4018*0.5569), lag.max = 24))
r5 <- ARMAacf(ar = 0.5, ma = c(rep(0,11), -0.7), lag.max = 24); pr("AR1xSMA1 0.5/-0.7", r5)
cat("  AR1xSMA1: r1*r12 =", round(r5[["1"]]*r5[["12"]], 4), "\n")

sec("M5 · pesos psi y sigma_h con los coeficientes sin redondear")
psi <- c(1, ARMAtoMA(ar = c(1, rep(0,10), 1, -1), ma = c(th, rep(0,10), Th, th*Th), lag.max = 239))
cat("psi1 =", round(psi[2], 4), " psi12 =", round(psi[13], 4), " psi13 =", round(psi[14], 4), "\n")
sh <- sqrt(cumsum(psi^2) * fit$sigma2)
cat("sigma_1, 12, 24 =", round(sh[c(1,12,24)], 4), " sigma12/sigma1 =", round(sh[12]/sh[1], 3), " sqrt(12) =", round(sqrt(12), 3), "\n")
razon <- sh / (sh[1] * sqrt(seq_along(sh)))   # airline frente a una caminata con el mismo sigma
cat("sigma_h / (sigma_1 sqrt(h)) en h = 12, 24, 36, 48, 60, 120, 240:", round(razon[c(12,24,36,48,60,120,240)], 3), "\n")
cat("primer h en que el airline acumula MAS incertidumbre que la caminata:", which(razon > 1)[1], "\n")

sec("M6 · rejilla de 36 modelos (d = D = 1)")
res <- data.frame()
for (p in 0:2) for (q in 0:2) for (P in 0:1) for (Q in 0:1) {
  f <- tryCatch(Arima(ap, order = c(p,1,q), seasonal = list(order = c(P,1,Q), period = 12), method = "ML"), error = function(e) NULL)
  if (is.null(f)) next
  res <- rbind(res, data.frame(m = sprintf("(%d,1,%d)(%d,1,%d)", p,q,P,Q), k = p+q+P+Q, aicc = f$aicc, bic = f$bic,
                               lb = Box.test(residuals(f), 24, "Ljung-Box", fitdf = p+q+P+Q)$p.value))
}
cat("convergen:", nrow(res), " min AICc:", res$m[which.min(res$aicc)], " min BIC:", res$m[which.min(res$bic)], "\n")
print(head(res[order(res$aicc), ], 5), digits = 6)
print(res[res$m == "(0,1,0)(0,1,0)", ], digits = 6)
cat("distancia AICc entre el 1.o y el 4.o:", round(sort(res$aicc)[4] - sort(res$aicc)[1], 3), "\n")

sec("M7 · rango relativo, Ljung-Box de checkresiduals y t")
cat("rango relativo (max-min)/media =", round(diff(range(AirPassengers))/mean(AirPassengers), 3), "\n")
lb <- Box.test(rr, 24, "Ljung-Box", fitdf = 2); cat("Q* =", round(lb$statistic, 3), " df =", lb$parameter, " p =", round(lb$p.value, 4), "\n")
se <- sqrt(diag(fit$var.coef)); cat("t =", round(coef(fit)/se, 2), " ee =", round(se, 4), " 0.1^(1/12) =", round(0.1^(1/12), 3), "\n")
cat("1/sqrt(131) =", round(1/sqrt(131), 4), "\n")
p24 <- forecast(fit, h = 24, level = 95)
cat("h=24: media", round(exp(p24$mean[24]), 2), " lo95", round(exp(p24$lower[24]), 2), " hi95", round(exp(p24$upper[24]), 2), "\n")

sec("M8 · USAccDeaths")
fu <- auto.arima(uad, stepwise = FALSE, approximation = FALSE); seu <- sqrt(diag(fu$var.coef))
cat(as.character(fu), " coef", round(coef(fu), 4), " ee", round(seu, 4), " AICc", round(fu$aicc, 2),
    " razones ee:", round(seu/se, 2), "\n")

sec("M9 · calendario")
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = 144)
dias <- as.numeric(diff(c(fechas, as.Date("1961-01-01"))))
pascua <- function(anio) { a <- anio %% 19; b <- anio %/% 100; cc <- anio %% 100; d <- b %/% 4; e <- b %% 4
  f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3; h <- (19*a + b - d - g + 15) %% 30; i <- cc %/% 4; k <- cc %% 4
  l <- (32 + 2*e + 2*i - h - k) %% 7; m <- (a + 11*h + 22*l) %/% 451
  as.Date(sprintf("%04d-%02d-%02d", anio, (h + l - 7*m + 114) %/% 31, ((h + l - 7*m + 114) %% 31) + 1)) }
pas <- sapply(1949:1960, function(a) format(pascua(a), "%m")); cat("Pascuas en marzo:", sum(pas == "03"), "de 12\n")
es_p <- as.numeric(format(fechas, "%m") == pas[as.numeric(format(fechas, "%Y")) - 1948])
X <- cbind(log_dias = log(dias), pascua = es_p)
f1 <- air(ap, xreg = X[, 1, drop = FALSE]); f2 <- air(ap, xreg = X)
tt <- function(f) round(coef(f)/sqrt(diag(f$var.coef)), 2)
cat("f0: AICc", round(fit$aicc, 2), " BIC", round(fit$bic, 2), "\n")
cat("f1: AICc", round(f1$aicc, 2), " BIC", round(f1$bic, 2), " coef", round(coef(f1), 4), " t", tt(f1), "\n")
cat("f2: AICc", round(f2$aicc, 2), " BIC", round(f2$bic, 2), " coef", round(coef(f2), 4), " t", tt(f2), "\n")
cat("mejora AICc f2 vs f0 =", round(fit$aicc - f2$aicc, 2), "  31/28 - 1 =", round(31/28 - 1, 4), "\n")

sec("M10 · Fourier, STL y m grande")
for (K in 1:6) {
  xr <- fourier(ap, K = K)
  f <- auto.arima(ap, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  cat(sprintf("K=%d n_ef=%d %s npar_total=%d AICc=%.2f LB=%.4f\n", K, f$nobs, as.character(f), length(coef(f)) + 1, f$aicc,
              Box.test(residuals(f), 24, "Ljung-Box", fitdf = sum(f$arma[1:4]))$p.value))
}
s <- stlm(ap, s.window = "periodic", method = "arima")
cat("stlm:", as.character(s$model), " aic =", round(s$model$aic, 2), " aicc =", round(s$model$aicc, 2), "\n")

sec("Ejercicio 3 · airline sobre co2")
fc <- air(co2); cat("AICc", round(fc$aicc, 3), " nobs", fc$nobs, " LB24 p", round(Box.test(residuals(fc), 24, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")
cat("\nfin\n")
