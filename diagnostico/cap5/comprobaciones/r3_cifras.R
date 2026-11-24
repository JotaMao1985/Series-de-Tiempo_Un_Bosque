# R3 del capítulo 5 · las cifras que la ronda escribe, mueve o deja en la prosa, recalculadas en R
# aparte de la página (desde datasets::AirPassengers, USAccDeaths y el JSON del generador).
# Cada línea dice la cifra citada, la calculada y si coinciden al redondeo con que se cita.
# Uso (desde la raíz del repo):
#   Rscript diagnostico/cap5/comprobaciones/r3_cifras.R > diagnostico/cap5/comprobaciones/r3_cifras.out 2>&1
suppressMessages({library(forecast); library(jsonlite)})
J <- fromJSON("precalculo/salidas/cap5_sarima.json", simplifyVector = FALSE)$airpassengers
n_si <- 0; n_no <- 0
mira <- function(donde, citada, calculada, dec) {
  ok <- isTRUE(all.equal(round(calculada, dec), citada, tolerance = 1e-9))
  if (ok) n_si <<- n_si + 1 else n_no <<- n_no + 1
  cat(sprintf("%-4s %-62s citada %-10s calculada %-12s %s\n", if (ok) "SI" else "NO", donde,
              format(citada), format(round(calculada, dec + 2)), ""))
}
apb <- AirPassengers; ap <- log(apb)

cat("== M1 · el ARIMA(0,1,5) del Capítulo 4, otra vez\n")
f5 <- Arima(ap, order = c(0, 1, 5)); r5 <- Acf(residuals(f5), lag.max = 24, plot = FALSE)$acf
mira("rho12 de los residuales", 0.7245, r5[13], 4)
mira("rho24 de los residuales", 0.6727, r5[25], 4)
lb <- Box.test(residuals(f5), lag = 24, type = "Ljung-Box", fitdf = 5)
mira("Q(24) de Ljung-Box", 222.4, unname(lb$statistic), 1)
cat(sprintf("     p < 1e-6: %s\n", lb$p.value < 1e-6))
cat("== M1 · la banda es 1.96/sqrt(n) con n las observaciones de la serie que se mira\n")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
mira("log(AirPassengers), n = 144", 0.163, 1.96 / sqrt(length(ap)), 3)
mira("USAccDeaths, n = 72", 0.231, 1.96 / sqrt(length(USAccDeaths)), 3)
mira("co2, n = 468", 0.091, 1.96 / sqrt(length(co2)), 3)
mira("TRM en niveles, n = 138", 0.167, 1.96 / sqrt(length(trm)), 3)
mira("nabla TRM, n = 137", 0.167, 1.96 / sqrt(length(diff(trm))), 3)
mira("M7 · nabla nabla12 log AP, n = 131", 0.171, 1.96 / sqrt(131), 3)
mira("M7 · residuales del airline, n = 144", 0.163, 1.96 / sqrt(144), 3)

cat("== M2 · el airline ajustado, ahora al principio del módulo\n")
fit <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
mira("theta", -0.4018, coef(fit)[["ma1"]], 4)
mira("Theta", -0.5569, coef(fit)[["sma1"]], 4)
mira("sigma2", 0.001371, fit$sigma2, 6)
mira("B13 = theta * Theta", 0.2238, prod(coef(fit)), 4)

cat("== M3 · nsdiffs con las dos pruebas; la ACF en 12 sin diferenciar\n")
mira("nsdiffs seas, log AP", 1, nsdiffs(ap), 0)
mira("nsdiffs ocsb, log AP", 0, nsdiffs(ap, test = "ocsb"), 0)
mira("nsdiffs seas, USAccDeaths", 1, nsdiffs(USAccDeaths), 0)
mira("nsdiffs ocsb, USAccDeaths", 0, nsdiffs(USAccDeaths, test = "ocsb"), 0)
mira("rho12 de log AP", 0.762, Acf(ap, lag.max = 12, plot = FALSE)$acf[13], 3)

cat("== M5 · los candidatos de la rejilla del M6, sin contar el airline\n")
mira("36 - 1", 35, length(J$rejilla) - 1, 0)

cat("== M7 · rango relativo, biasadj\n")
mira("(max - min) / media de AirPassengers", 1.848, diff(range(apb)) / mean(apb), 3)
fl <- Arima(apb, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), lambda = 0)
mira("mediana a 24 meses (lambda = 0)", 525.46, forecast(fl, h = 24)$mean[24], 2)
mira("biasadj = TRUE a 24 meses", 530.58, forecast(fl, h = 24, biasadj = TRUE)$mean[24], 2)
p <- forecast(fit, h = 24)
mira("exp() del pronóstico en log (el mismo 525.46)", 525.46, exp(p$mean[24]), 2)

cat("== M9 · RMSE fuera de muestra, con y sin calendario\n")
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = 144)
dias <- as.numeric(diff(c(fechas, as.Date("1961-01-01"))))
pas <- J$calendario$pascuas
es_pascua <- as.numeric(format(fechas, "%Y-%m") %in% substr(unlist(pas), 1, 7))
xreg <- cbind(log_dias = log(dias), pascua = es_pascua)
ent <- window(ap, end = c(1958, 12)); obs <- as.numeric(window(apb, start = c(1959, 1)))
g0 <- Arima(ent, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
g2 <- Arima(ent, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), xreg = xreg[1:120, ])
rmse <- function(q) sqrt(mean((obs - exp(q))^2))
mira("airline", 43.18, rmse(forecast(g0, h = 24)$mean), 2)
mira("airline + calendario", 45.48, rmse(forecast(g2, xreg = xreg[121:144, ])$mean), 2)

cat("== M10 · «Parámetros totales» = términos + coeficientes ARIMA + deriva (no sigma2; corregido tras V2)\n")
for (K in 1:6) {
  aj <- auto.arima(ap, xreg = fourier(ap, K = K), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  cat(sprintf("     K = %d: length(coef) = %d, con deriva: %s\n", K, length(aj$coef), "drift" %in% names(aj$coef)))
  mira(sprintf("K = %d: la columna es length(coef), que incluye la deriva", K), c(8, 9, 11, 14, 15, 16)[K], length(aj$coef), 0)
}
for (r in J$fourier$resultados) {
  ord <- as.integer(strsplit(gsub("[^0-9,]", "", sub(".*ARIMA\\(", "", r$modelo_errores)), ",")[[1]][c(1, 3)])
  mira(sprintf("K = %d (%s)", r$K, r$modelo_errores), c(8, 9, 11, 14, 15, 16)[r$K], r$n_terminos + sum(ord) + 1, 0)
}

cat("== M11 · lo que la prosa nueva dice de la tabla de la partición\n")
cm <- J$comparativa$modelos
mira("MAE de la armónica", 14.69, cm$armonica$mae, 2)
mira("MAE del ETS sobre el log", 16.12, cm$ets_log$mae, 2)
mira("RMSE del SARIMA / RMSE del ganador (> 2)", 2.22, cm$sarima$rmse / cm$ets_log$rmse, 2)
for (m in c("rmse", "mae", "mape")) {
  v <- sapply(cm, function(x) x[[m]]); v <- v[names(v) != "auto_arima"]
  mira(sprintf("puesto del SARIMA por %s (sin auto.arima, que empata)", toupper(m)), 4, rank(v)[["sarima"]], 0)
}
om <- J$comparativa$origen_movil
mira("primer origen 1954-12: el mes 72", 72, which(format(fechas, "%Y-%m") == om$primer_origen), 0)
mira("último origen 1959-12: el mes 132 = 144 - 12", 132, 144 - 12, 0)
mira("orígenes con h = 12", 61, om$n_origenes, 0)
mira("orígenes con h = 24: 72..120", 49, length(72:120), 0)
mira("ETS(M,A,M) es el ETS sobre el log (16 parámetros)", 16, cm$ets_log$n_par, 0)
mira("ETS(M,Ad,M) es el de la serie cruda (17 parámetros)", 17, cm$ets$n_par, 0)
mira("STL + ARIMA: 2 parámetros + 11 de la estación", 2, cm$stl_arima$n_par, 0)
cat(sprintf("     nombres: «%s» · «%s»\n", cm$ets_log$nombre, cm$ets$nombre))
cat("== M11 · sesgo medio que da la lectura del simulador (desde el JSON, como el navegador)\n")
o <- unlist(J$comparativa$observado)
for (k in names(cm)) cat(sprintf("     %-20s %7.2f\n", k, mean(o - unlist(cm[[k]]$pronostico))))
mira("sesgo del SARIMA = su MAE (39.45)", 39.45, mean(o - unlist(cm$sarima$pronostico)), 2)
fk <- J$armonica_K_sin_fuga
mira("salvedad: K con solo el entrenamiento", 5, fk$K_solo_entrenamiento, 0)
mira("salvedad: RMSE con ese K", 19.58, fk$rmse, 2)

cat("== Correcciones tras el verificador\n")
f5c <- coef(f5)
mira("V4 · ma2 de R", -0.0032, f5c[["ma2"]], 4)
mira("V4 · primer residual de R", 0.0047, as.numeric(residuals(f5))[1], 4)
mira("V4 · segundo residual de R", 0.0420, as.numeric(residuals(f5))[2], 4)
mira("V4 · tercer residual de R", 0.0863, as.numeric(residuals(f5))[3], 4)
sh <- as.numeric(p$upper[24, 2] - p$mean[24]) / qnorm(0.975)
mira("V6 · media exacta exp(mu + sigma_h^2/2)", 530.61, exp(p$mean[24] + sh^2 / 2), 2)
mira("V6 · aproximación exp(mu)(1 + sigma_h^2/2) = biasadj", 530.58, exp(p$mean[24]) * (1 + sh^2 / 2), 2)
a131 <- Acf(residuals(fit)[-(1:13)], lag.max = 23, plot = FALSE)$acf
cat(sprintf("     V9 · sin los 13 de arranque: rezagos 3, 9, 23 = %.3f %.3f %.3f; banda %.3f\n",
            a131[4], a131[10], a131[24], 1.96 / sqrt(131)))
mira("V9 · con 131: el 3 dentro de la banda (1 = sí)", 1, as.numeric(abs(a131[4]) < 1.96 / sqrt(131)), 0)
mira("V9 · con 131: el 9 dentro de la banda (1 = sí)", 1, as.numeric(abs(a131[10]) < 1.96 / sqrt(131)), 0)
mira("V9 · con 131: el 23 sigue fuera (1 = sí)", 1, as.numeric(abs(a131[24]) > 1.96 / sqrt(131)), 0)
ex <- J$comparativa$origen_movil$armonica_exhaustiva
mira("V5 · armónica exhaustiva en los orígenes, h = 12 (JSON)", 21.06, ex$rmse_medio_h12, 2)
mira("V5 · ETS sobre el log en los orígenes (JSON)", 21.42, om$rmse_medio$ets_log, 2)
cat("     V5 · recálculo aparte de la armónica exhaustiva en los 61 orígenes (minuto y medio)\n")
r12ex <- sapply(72:132, function(k) {
  l <- window(ap, end = time(ap)[k])
  q <- exp(as.numeric(forecast(auto.arima(l, xreg = fourier(l, K = 6), seasonal = FALSE, stepwise = FALSE,
                                          approximation = FALSE), xreg = fourier(l, K = 6, h = 12))$mean))
  sqrt(mean((as.numeric(apb)[k + 1:12] - q)^2)) })
mira("V5 · armónica exhaustiva, h = 12, recalculada", 21.06, mean(r12ex), 2)

cat(sprintf("\n%d cifras coinciden, %d no.\n", n_si, n_no))
