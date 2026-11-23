# R3 · cap. 4 · cada cifra que la ronda escribe, mueve o deja en la prosa del Modulo 10 (y de los
# modulos que la ronda toca), recalculada en R aparte de la pagina. Una linea por cifra:
#   [ok|NO] cifra citada · valor calculado · donde se muestra (bloque o generador)
suppressMessages({library(forecast); library(tseries)})
.cmp <- function(nombre, citado, calculado, donde, tol = 0.006) {
  ok <- is.na(citado) || abs(citado - calculado) <= tol
  cat(sprintf("[%s] %-62s citado %-10s calculado %-12.5g %s\n", if (ok) "ok" else "NO", nombre,
              format(citado), calculado, donde))
}
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
n <- length(Nile)

cat("== Nilo (cuadro del M10 y modulos 1-9) ==\n")
f111 <- arima(Nile, order = c(1,1,1), method = "ML")
.cmp("M1/M10 phi", 0.2544, coef(f111)[["ar1"]], "M1 bloque (ajuste)", 5e-5)
.cmp("M1/M10 theta", -0.8741, coef(f111)[["ma1"]], "M1 bloque (ajuste)", 5e-5)
.cmp("M1 e.e. phi", 0.1194, sqrt(f111$var.coef[1,1]), "M1 bloque", 5e-5)
.cmp("M1 e.e. theta", 0.0605, sqrt(f111$var.coef[2,2]), "M1 bloque", 5e-5)
.cmp("M1/M10 raiz MA 1.144", 1.144, Mod(polyroot(c(1, coef(f111)[["ma1"]]))), "M1 bloque", 5e-4)
.cmp("M10 raiz AR 3.93", 3.93, max(Mod(polyroot(c(1, -(c(1 + coef(f111)[["ar1"]], -coef(f111)[["ar1"]])))))), "M1 bloque (3.9308)", 5e-3)
.cmp("M10 ACF Nilo rezago 1 = 0.498", 0.498, acf(Nile, plot = FALSE)$acf[2], "M4 bloque", 5e-4)
.cmp("M10 adf.test p = 0.064", 0.064, adf.test(Nile)$p.value, "M3 bloque", 5e-4)
.cmp("M10 KPSS p < 0.01 (p reportado = 0.01)", 0.01, suppressWarnings(kpss.test(Nile)$p.value), "M3 bloque", 5e-4)
.cmp("M3/M10 PP.test estadistico -6.690", -6.690, unname(PP.test(Nile)$statistic), "M3 bloque (nuevo)", 5e-4)
.cmp("M3/M10 PP.test p <= 0.01 (p reportado = 0.01)", 0.01, PP.test(Nile)$p.value, "M3 bloque (nuevo)", 5e-4)
.cmp("M10 r1 de nabla Nilo -0.402", -0.402, acf(diff(Nile), plot = FALSE)$acf[2], "M4 bloque", 5e-4)
fd <- Arima(Nile, order = c(1,1,1), include.drift = TRUE)
.cmp("M10 delta -2.883", -2.883, coef(fd)[["drift"]], "M5 bloque", 5e-4)
.cmp("M10 t de delta -1.43", -1.43, coef(fd)[["drift"]] / sqrt(diag(fd$var.coef))[["drift"]], "M5 bloque (-1.429)", 5e-3)
.cmp("M10 AICc con deriva 1268.06", 1268.06, fd$aicc, "M5 bloque", 5e-3)
.cmp("M10 AICc sin deriva 1267.51", 1267.51, Arima(Nile, order = c(1,1,1))$aicc, "M5 bloque", 5e-3)
.cmp("M10 media de las diferencias -3.84", -3.84, (740 - 1120) / 99, "M5 prosa (aritmetica)", 5e-3)
.cmp("M10 aporte del escalon -2.50", -2.50, -247.78 / 99, "M5 prosa (aritmetica)", 5e-3)
aicc <- function(f, n_ef) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n_ef-k-1) }
bic2 <- function(f, n_ef) { k <- length(f$coef) + 1; f$aic - 2*k + log(n_ef)*k }
f011 <- arima(Nile, order = c(0,1,1), method = "ML")
.cmp("M10 BIC (0,1,1) 1274.28", 1274.28, bic2(f011, 99), "M6 bloque", 5e-3)
f122 <- arima(Nile, order = c(1,2,2), method = "ML")
.cmp("M10 AICc (1,2,2) 1264.60", 1264.60, aicc(f122, 98), "M6 bloque", 5e-3)
.cmp("M10 LB(20) p = 0.800 del ARIMA(1,1,1)", 0.800, Box.test(residuals(f111), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value, "M2 bloque (0.7997)", 5e-4)
esc <- as.numeric(time(Nile) >= 1899)
fe <- arima(Nile, order = c(0,0,0), xreg = esc, method = "ML")
.cmp("M10 beta -247.78", -247.78, coef(fe)[["esc"]], "M3/M8 bloque", 5e-3)
.cmp("M10 t = -8.80", -8.80, coef(fe)[["esc"]] / sqrt(diag(fe$var.coef))[["esc"]], "M8 prosa (e.e. 28.15 del bloque)", 5e-3)
.cmp("M10 AICc del mejor ARMA d=0 menos el del escalon: casi 25", 25, aicc(arima(Nile, order = c(1,0,1), method = "ML"), 100) - aicc(fe, 100), "M6 + M8 (JSON)", 0.5)
.cmp("M10 LB(20) escalon p = 0.812", 0.812, Box.test(residuals(fe), lag = 20, type = "Ljung-Box")$p.value, "M8 bloque", 5e-4)
.cmp("M3/M10 media 1871-1898 = 1097.75", 1097.75, mean(Nile[1:28]), "M3 bloque (nuevo)", 5e-3)
.cmp("M3/M10 media desde 1899 = 849.97", 849.97, mean(Nile[29:100]), "M3 bloque (nuevo)", 5e-3)
.cmp("M3 sigma del modelo de dos medias = 127.03", 127.03, sd(residuals(fe)), "M3 bloque (nuevo)", 5e-3)
ent <- window(Nile, end = 1950); pru <- window(Nile, start = 1951)
esc_e <- as.numeric(time(ent) >= 1899)
rmse <- function(p) sqrt(mean((as.numeric(pru) - as.numeric(p))^2))
.cmp("M10 RMSE ARIMA 125.05", 125.05, rmse(forecast(Arima(ent, order = c(1,1,1)), h = 20)$mean), "M8 bloque", 5e-3)
.cmp("M10 RMSE escalon 127.99", 127.99, rmse(forecast(Arima(ent, order = c(0,0,0), xreg = esc_e), xreg = rep(1, 20))$mean), "M8 bloque", 5e-3)
.cmp("M10 RMSE naive 123.06", 123.06, rmse(rep(tail(ent, 1), 20)), "M8 bloque", 5e-3)
f1 <- Arima(Nile, order = c(1,1,1))
.cmp("M10 pronostico h=1 816.18", 816.18, forecast(f1, h = 1)$mean[1], "M2/M9 bloque", 5e-3)
.cmp("M10 pronostico h=30 842.17", 842.17, forecast(f1, h = 30)$mean[30], "M9 bloque", 5e-3)
ph <- coef(f1)[["ar1"]]; th <- coef(f1)[["ma1"]]
.cmp("M10 psi_inf = 0.169", 0.169, (1 + th) / (1 - ph), "M9 bloque (psi_30)", 5e-4)
psi <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = 30)); s <- sqrt(f1$sigma2); sh <- s * sqrt(cumsum(psi^2))[1:30]
.cmp("M10 lista psi_inf = 0.1688 (sin redondear)", 0.1688, (1 + th) / (1 - ph), "aritmetica del bloque M9", 5e-5)
.cmp("M10 lista sigma_30/sigma_1 = 1.404", 1.404, sh[30] / sh[1], "M9 bloque (199.363/142.045)", 5e-4)
.cmp("M9 sigma_1 = 142.0 (M10 ya no lo cita)", 142.045, sh[1], "M9 bloque", 5e-4)

cat("\n== Modulo 6: lo que dice el recuadro tras el explorador (precalculado en genera_cap4.R; aqui, recalculado) ==\n")
rej <- expand.grid(p = 0:2, d = 0:2, q = 0:2)
rej$aicc <- NA; rej$lb <- NA; rej$minar <- NA; rej$minma <- NA
for (i in seq_len(nrow(rej))) {
  o <- unlist(rej[i, c("p","d","q")])
  f <- tryCatch(suppressWarnings(arima(Nile, order = o, method = "ML")), error = function(e) NULL)
  if (is.null(f)) next
  rej$aicc[i] <- aicc(f, 100 - o[["d"]])
  rej$lb[i] <- Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = o[["p"]] + o[["q"]])$p.value
  ar <- f$coef[grepl("^ar", names(f$coef))]; ma <- f$coef[grepl("^ma", names(f$coef))]
  rej$minar[i] <- if (length(ar)) min(Mod(polyroot(c(1, -ar)))) else NA
  rej$minma[i] <- if (length(ma)) min(Mod(polyroot(c(1, ma)))) else NA
}
.cmp("M6 modelos con Ljung-Box(20) < 0.05: 8 de 27", 8, sum(rej$lb < 0.05, na.rm = TRUE), "JSON del explorador", 0)
.cmp("M6 modelos ajustados: 27", 27, sum(!is.na(rej$aicc)), "JSON del explorador", 0)
mejor_d <- sapply(0:2, function(d) min(rej$aicc[rej$d == d], na.rm = TRUE))
cerca <- sapply(0:2, function(d) sum(rej$aicc[rej$d == d] - mejor_d[d + 1] < 2, na.rm = TRUE) - 1)
.cmp("M6 d = 1: cuatro modelos mas a menos de 2 puntos", 4, cerca[2], "JSON del explorador", 0)
cercanos_rechazan <- sum(sapply(0:2, function(d) sum(rej$aicc[rej$d == d] - mejor_d[d + 1] < 2 & rej$lb[rej$d == d] < 0.05, na.rm = TRUE)))
.cmp("M6 de los cercanos al mejor de su d, los que rechazan LB: 0", 0, cercanos_rechazan, "JSON del explorador", 0)
.cmp("M6 mejor de d = 0: raiz AR minima 1.161", 1.161, rej$minar[rej$d == 0 & abs(rej$aicc - mejor_d[1]) < 1e-9], "JSON / lectura", 5e-4)
.cmp("M6 mejor de d = 1: raiz MA minima 1.144", 1.144, rej$minma[rej$d == 1 & abs(rej$aicc - mejor_d[2]) < 1e-9], "JSON / lectura", 5e-4)
buenos2 <- rej$minma[rej$d == 2 & rej$aicc - mejor_d[3] < 2 | (rej$d == 2 & !is.na(rej$minma) & rej$p == 0 & rej$q %in% 1:2)]
cat(sprintf("   (M6) raices MA minimas de los modelos de d = 2 con MA: %s\n", paste(sort(round(rej$minma[rej$d == 2], 3)), collapse = " ")))

cat("\n== Modulo 4: alfa del IMA(1,1) ==\n")
.cmp("M4 alfa = 1 + theta = 0.267", 0.267, 1 + coef(f011)[["ma1"]], "M4 bloque (nuevo)", 5e-4)
.cmp("M4 t de theta = -6.41", -6.41, coef(f011)[["ma1"]] / sqrt(f011$var.coef[1,1]), "M4 prosa", 5e-3)

cat("\n== TRM (M10, un solo bloque; aqui, recalculado) ==\n")
d1 <- diff(trm); rw <- arima(trm, order = c(0,1,0), method = "ML"); sg <- sqrt(rw$sigma2); z <- qnorm(.975)
.cmp("TRM n = 138", 138, length(trm), "M10 bloque", 0)
.cmp("TRM sigma = 121.48", 121.48, sg, "M10 bloque", 5e-3)
.cmp("TRM ACF del nivel en el rezago 1 = 0.964 (intro del simulador, JSON)", 0.964, acf(trm, plot = FALSE)$acf[2], "JSON", 5e-4)
.cmp("TRM rho8 de nabla TRM = -0.190 y banda 0.167", -0.190, acf(d1, plot = FALSE)$acf[9], "M10 bloque", 5e-4)
.cmp("TRM sigma^2 = 14756.38 (intro del simulador, JSON)", 14756.38, rw$sigma2, "JSON", 5e-3)
.cmp("TRM cubre el 80 % a un mes: 0.839 (promesa del M9)", 0.839, mean(abs(d1) <= qnorm(.90) * sg), "M10 bloque (nuevo en R1)", 5e-4)
.cmp("TRM cubre el 95 % a un mes: 6 de 137 fuera", 6, sum(abs(d1) > z * sg), "M10 bloque", 0)
.cmp("TRM 4.4 % fuera = 6/137", 4.4, 100 * 6 / 137, "M10 prosa (aritmetica)", 0.05)
.cmp("TRM deriva = media de las diferencias (y_n - y_1)/(n-1) = 8.00", 8.00, (as.numeric(tail(trm, 1)) - as.numeric(trm[1])) / (length(trm) - 1), "M10 bloque (deriva 8.00)", 5e-3)
fdt <- Arima(trm, order = c(0,1,0), include.drift = TRUE)
.cmp("TRM t de la deriva 0.77", 0.77, coef(fdt)[["drift"]] / sqrt(fdt$var.coef[1,1]), "M10 prosa", 5e-3)
mayores <- order(d1, decreasing = TRUE)[1:2]
cat(sprintf("   (M10) los dos mayores aumentos mensuales: %s con %s  [prosa: marzo de 2020 y julio de 2022; NO sale de un bloque]\n",
            paste(sprintf("%d-%02d", floor(time(d1)[mayores]), round((time(d1)[mayores] %% 1) * 12) + 1), collapse = " y "),
            paste(round(d1[mayores], 1), collapse = " y ")))

cat("\n== Puente (M10, bloque nuevo) ==\n")
lap <- log(AirPassengers)
a <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
r <- as.numeric(acf(residuals(a), lag.max = 24, plot = FALSE)$acf)[-1]
.cmp("Puente rho12 = 0.7245", 0.7245, r[12], "M10 bloque (nuevo)", 5e-5)
.cmp("Puente rho24 = 0.6727", 0.6727, r[24], "M10 bloque (nuevo)", 5e-5)
.cmp("Puente banda = 0.1633", 0.1633, 1.96 / sqrt(length(residuals(a))), "M10 bloque (nuevo)", 5e-5)
.cmp("Puente 0.7245 / 0.1633 = mas de cuatro veces la banda", 4.4, r[12] / (1.96 / sqrt(144)), "M10 prosa (aritmetica)", 0.05)
.cmp("Puente Q_LB(24) = 222.4", 222.4, unname(Box.test(residuals(a), lag = 24, type = "Ljung-Box", fitdf = 5)$statistic), "M10 bloque (nuevo)", 0.05)
w <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE, max.p = 8, max.q = 8, max.order = 16)
.cmp("Puente (8,1,3): rho12 = 0.437", 0.437, as.numeric(acf(residuals(w), lag.max = 24, plot = FALSE)$acf)[13], "M10 bloque (nuevo)", 5e-4)
air <- Arima(lap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
.cmp("Puente airline rho12 = -0.0515", -0.0515, as.numeric(acf(residuals(air), lag.max = 24, plot = FALSE)$acf)[13], "M10 bloque (nuevo)", 5e-5)
.cmp("Puente airline LB(24) p = 0.233", 0.233, Box.test(residuals(air), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, "M10 bloque (nuevo)", 5e-4)
.cmp("Puente 143 observaciones (no estacional)", 143, a$nobs, "M10 bloque (nuevo)", 0)
.cmp("Puente 131 observaciones (airline)", 131, air$nobs, "M10 bloque (nuevo)", 0)
.cmp("Puente max.order por defecto = 5 (p + q <= 5)", 5, formals(auto.arima)$max.order, "M10 prosa", 0)
