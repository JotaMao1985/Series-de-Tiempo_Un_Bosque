# V3 (verificador independiente de la R3 del cap. 5): recalcula, sin copiar los
# bloques del capitulo, las cifras que la R3 escribe, mueve o deja en la prosa.
# Uso: Rscript diagnostico/cap5/comprobaciones/v3_cifras.R > .../v3_cifras.out
suppressMessages(library(forecast))
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")), "\n")
ok <- function(etq, x, esperado, dec) {
  v <- round(x, dec); cat(sprintf("%-58s %14s  texto %-10s %s\n", etq, format(v, nsmall = dec),
                                  format(esperado, nsmall = dec), if (isTRUE(all.equal(v, esperado))) "OK" else "<<< DISTINTO"))
}
y  <- AirPassengers; ly <- log(y); n <- length(ly)

cat("\n== M1: el ARIMA(0,1,5) del cap. 4 ==\n")
m5 <- Arima(ly, order = c(0, 1, 5))
e5 <- as.numeric(residuals(m5))
racf <- function(e, k) { e <- e - mean(e); sum(e[(k + 1):length(e)] * e[1:(length(e) - k)]) / sum(e^2) }
ok("rho12 residual ARIMA(0,1,5) (144 residuales)", racf(e5, 12), 0.7245, 4)
ok("rho24 residual ARIMA(0,1,5)", racf(e5, 24), 0.6727, 4)
Q <- n * (n + 2) * sum(sapply(1:24, function(k) racf(e5, k)^2) / (n - 1:24))
ok("Ljung-Box Q(24), a mano", Q, 222.4, 1)
cat("p con 24 - 5 gl:", format(pchisq(Q, 19, lower.tail = FALSE)), " (< 1e-6?)", pchisq(Q, 19, lower.tail = FALSE) < 1e-6, "\n")
cat("rho12/24 sin el primer residual (como el bloque de Python):", round(racf(e5[-1], 12), 4), round(racf(e5[-1], 24), 4), "\n")
ok("banda 1.96/sqrt(144)", 1.96 / sqrt(144), 0.163, 3)
ok("banda 1.96/sqrt(131)", 1.96 / sqrt(131), 0.171, 3)
ok("banda USAccDeaths 1.96/sqrt(72)", 1.96 / sqrt(72), 0.231, 3)
ok("banda co2 1.96/sqrt(468)", 1.96 / sqrt(length(co2)), 0.091, 3)
ok("banda TRM 1.96/sqrt(137 o 138)", 1.96 / sqrt(137), 0.167, 3)

cat("\n== M2: sigma2 del airline ==\n")
air <- Arima(ly, order = c(0, 1, 1), seasonal = c(0, 1, 1))
ok("theta", coef(air)[[1]], -0.4018, 4); ok("Theta", coef(air)[[2]], -0.5569, 4)
ok("sigma2 (R, SSR/(n-k))", air$sigma2, 0.001371, 6)
ok("B13 = theta*Theta", prod(coef(air)), 0.2238, 4)
cat("ACF teorica heladeria (phi .6, Phi .7) rezagos 1, 11, 12, 13:\n")
print(round(ARMAacf(ar = c(0.6, rep(0, 10), 0.7, -0.42), lag.max = 13)[c(2, 12, 13, 14)], 4))

cat("\n== M3: intro del simulador y la trampa de version ==\n")
ok("rho12 de log(AP) sin diferenciar", racf(as.numeric(ly), 12), 0.762, 3)
cat("rho12 de diff(log AP) (la respuesta a la pregunta de la intro):", round(racf(diff(as.numeric(ly)), 12), 3), "\n")
cat("nsdiffs seas/ocsb  log(AP):", nsdiffs(ly), nsdiffs(ly, test = "ocsb"),
    "  USAccDeaths:", nsdiffs(USAccDeaths), nsdiffs(USAccDeaths, test = "ocsb"), "  (texto: 1 0 / 1 0)\n")

cat("\n== M4 (cierre): ACF de diff(diff(log AP, 12)) ==\n")
w <- diff(diff(as.numeric(ly), 12))
r <- sapply(1:24, function(k) racf(w, k))
cat("n =", length(w), " banda", round(1.96 / sqrt(length(w)), 3), "\n")
print(round(setNames(r, 1:24), 3))
cat("fuera de banda:", which(abs(r) > 1.96 / sqrt(length(w))), "\n")

cat("\n== M5 (cierre): la rejilla tiene 36 modelos -> 35 candidatos ademas del airline ==\n")
cat("p,q,P,Q en 0:2 x 0:2 x 0:1 x 0:1 =", 3 * 3 * 2 * 2, "\n")

cat("\n== M7 ==\n")
ok("rango relativo (max - min)/media de AirPassengers", diff(range(y)) / mean(y), 1.848, 3)
fc <- forecast(air, h = 24, level = 95)
mu <- fc$mean[24]; sh <- (fc$upper[24] - mu) / qnorm(0.975)
ok("mediana a 24 meses", exp(mu), 525.46, 2)
ok("limite inferior 95 %", exp(fc$lower[24]), 399.66, 2)
ok("limite superior 95 %", exp(fc$upper[24]), 690.85, 2)
fl <- Arima(y, order = c(0, 1, 1), seasonal = c(0, 1, 1), lambda = 0)
ok("forecast(lambda = 0)$mean[24] (mediana)", forecast(fl, h = 24)$mean[24], 525.46, 2)
ok("forecast(lambda = 0, biasadj = TRUE)$mean[24]", forecast(fl, h = 24, biasadj = TRUE)$mean[24], 530.58, 2)
cat(sprintf("sigma_h(24) en log = %.5f; exp(mu)*(1 + sigma_h^2/2) = %.2f; exp(mu + sigma_h^2/2) (media lognormal exacta) = %.2f\n",
            sh, exp(mu) * (1 + sh^2 / 2), exp(mu + sh^2 / 2)))
cat("=> biasadj de forecast es la aproximacion de primer orden (1 + s^2/2), no exp(s^2/2)\n")
re <- as.numeric(residuals(air))
cat("residuales del airline: n =", length(re), "; ACF 3, 9, 23 con los 144:", round(sapply(c(3, 9, 23), function(k) racf(re, k)), 3),
    "; sin los 13 de arranque:", round(sapply(c(3, 9, 23), function(k) racf(re[-(1:13)], k)), 3), "\n")

cat("\n== M9: fuera de muestra con el calendario ==\n")
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = 145)
dias <- as.numeric(diff(fechas))
pascua_mes <- function(a) {                     # Pascua por el algoritmo anonimo gregoriano, escrito aparte
  a1 <- a %% 19; b <- a %/% 100; c <- a %% 100; d <- b %/% 4; e <- b %% 4
  f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3; h <- (19 * a1 + b - d - g + 15) %% 30
  i <- c %/% 4; k <- c %% 4; l <- (32 + 2 * e + 2 * i - h - k) %% 7; m <- (a1 + 11 * h + 22 * l) %/% 451
  (h + l - 7 * m + 114) %/% 31 }
anio <- as.numeric(format(fechas[1:144], "%Y")); mes <- as.numeric(format(fechas[1:144], "%m"))
X <- cbind(ld = log(dias), pa = as.numeric(mes == sapply(anio, pascua_mes)))
cat("Pascua en marzo / abril, 1949-1960:", table(sapply(1949:1960, pascua_mes)), "\n")
tr <- 1:120; te <- 121:144; ob <- as.numeric(y)[te]
a0 <- Arima(ts(as.numeric(ly)[tr], frequency = 12), order = c(0, 1, 1), seasonal = c(0, 1, 1))
a2 <- Arima(ts(as.numeric(ly)[tr], frequency = 12), order = c(0, 1, 1), seasonal = c(0, 1, 1), xreg = X[tr, ])
ok("RMSE airline 1959-1960", sqrt(mean((ob - exp(forecast(a0, h = 24)$mean))^2)), 43.18, 2)
ok("RMSE airline + calendario", sqrt(mean((ob - exp(forecast(a2, xreg = X[te, ])$mean))^2)), 45.48, 2)

cat("\n== M10: que suma 'parametros totales' ==\n")
for (K in c(1, 6)) {
  aj <- auto.arima(ly, xreg = fourier(ly, K = K), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  cat("K =", K, as.character(aj), "| length(coef) =", length(aj$coef), "| nombres:", paste(names(aj$coef), collapse = " "), "\n")
}
cat("=> el +1 es la deriva (drift), no sigma^2: length(coef) no cuenta sigma^2\n")

cat("\n== M11: la particion, escrito aparte ==\n")
ent <- ts(as.numeric(ly)[tr], start = c(1949, 1), frequency = 12)
ento <- ts(as.numeric(y)[tr], start = c(1949, 1), frequency = 12)
e_ets <- ets(ento); e_etl <- ets(ent)
cat("ets cruda:", e_ets$method, " | ets log:", e_etl$method, " | length(par):", length(e_ets$par), length(e_etl$par), "\n")
p <- list(
  ets_log  = exp(as.numeric(forecast(e_etl, h = 24)$mean)),
  armonica = exp(as.numeric(forecast(auto.arima(ent, xreg = fourier(ent, 6), seasonal = FALSE, stepwise = FALSE,
                                     approximation = FALSE), xreg = fourier(ent, 6, h = 24))$mean)),
  stl      = exp(as.numeric(forecast(stlm(ent, s.window = "periodic", method = "arima"), h = 24)$mean)),
  sarima   = exp(as.numeric(forecast(a0, h = 24)$mean)),
  ets      = as.numeric(forecast(e_ets, h = 24)$mean),
  snaive   = rep(as.numeric(y)[109:120], 2))
cat("auto.arima(ent):", as.character(auto.arima(ent, stepwise = FALSE, approximation = FALSE)), "\n")
M <- t(sapply(p, function(f) { e <- ob - f; c(rmse = sqrt(mean(e^2)), mae = mean(abs(e)), mape = 100 * mean(abs(e) / ob), sesgo = mean(e)) }))
print(round(M, 4))
cat("texto: ets_log 19.43 16.12 3.55 | armonica 19.51 14.69 3.15 | stl 35.48 30.29 6.33 | sarima 43.18 39.45 8.52 | ets 72.55 63.21 13.30 | snaive 76.99 71.25 15.52\n")
cat("doble redondeo: round(round(x,3),2) frente a round(x,2):\n")
print(cbind(exacto2 = round(M[, 1:3], 2)[c("ets_log", "snaive"), ], doble = round(round(M[, 1:3], 3), 2)[c("ets_log", "snaive"), ]))
cat("RMSE SARIMA / RMSE ETS log =", round(M["sarima", "rmse"] / M["ets_log", "rmse"], 3), "(texto: 'mas del doble')\n")
cat("SARIMA cuarto en las tres?", sapply(c("rmse", "mae", "mape"), function(j) rank(M[, j])[["sarima"]]), "\n")
cat("sesgo SARIMA == MAE?", isTRUE(all.equal(M["sarima", "sesgo"], M["sarima", "mae"])), " todos los meses por debajo?", all(ob > p$sarima), "\n")
tot <- tapply(as.numeric(y), rep(1949:1960, each = 12), sum)
cat("crecimiento anual %:\n"); print(round(100 * diff(tot) / head(tot, -1), 1))
g <- function(f) round(100 * c(sum(f[1:12]) / tot[["1958"]] - 1, sum(f[13:24]) / sum(f[1:12]) - 1), 1)
cat("crecimiento pronosticado 1959, 1960  sarima:", g(p$sarima), " ets_log:", g(p$ets_log), " armonica:", g(p$armonica), "\n")
cat("observado 1959, 1960:", round(100 * c(tot[["1959"]] / tot[["1958"]] - 1, tot[["1960"]] / tot[["1959"]] - 1), 1), "\n")

cat("\n== M11: 61 origenes, escrito aparte (cada origen ajusta y pronostica por separado para h = 12 y h = 24) ==\n")
t0 <- Sys.time()
pron <- function(k, h, stepwise_arm) {
  l <- ts(as.numeric(ly)[1:k], start = c(1949, 1), frequency = 12)
  o <- ts(as.numeric(y)[1:k],  start = c(1949, 1), frequency = 12)
  cbind(sarima   = exp(as.numeric(forecast(Arima(l, order = c(0, 1, 1), seasonal = c(0, 1, 1)), h = h)$mean)),
        ets_log  = exp(as.numeric(forecast(ets(l), h = h)$mean)),
        stl      = exp(as.numeric(forecast(stlm(l, s.window = "periodic", method = "arima"), h = h)$mean)),
        armonica = exp(as.numeric(forecast(auto.arima(l, xreg = fourier(l, 6), seasonal = FALSE, stepwise = stepwise_arm,
                                                      approximation = FALSE), xreg = fourier(l, 6, h = h))$mean)),
        ets      = as.numeric(forecast(ets(o), h = h)$mean),
        snaive   = as.numeric(o)[k - 12 + ((0:(h - 1)) %% 12) + 1])
}
orig <- 72:132
res <- lapply(orig, function(k) { h <- min(24, 144 - k); P <- pron(k, h, TRUE); as.numeric(y)[k + 1:h] - P })
cat("tiempo:", round(as.numeric(difftime(Sys.time(), t0, units = "secs"))), "s\n")
mes_txt <- format(seq(as.Date("1949-01-01"), by = "month", length.out = 144), "%Y-%m")
cat("primer y ultimo origen:", mes_txt[72], mes_txt[132], "\n")
R12 <- t(sapply(res, function(e) sqrt(colMeans(e[1:12, , drop = FALSE]^2))))
cat("origenes h = 12:", nrow(R12), "\n"); print(round(colMeans(R12), 2))
cat("texto: 16.81 21.42 21.85 22.38 26.38 41.24\n")
print(round(100 * colMeans(R12 < R12[, "sarima"]), 1)); cat("texto: - 8.2 8.2 9.8 14.8 11.5\n")
nomejor <- mes_txt[orig[apply(R12, 1, which.min) != 1]]
cat("origenes donde el SARIMA no es el mejor (", length(nomejor), "):", nomejor, "\n")
cat("de ellos entre 1957-05 y 1959-01:", sum(nomejor >= "1957-05" & nomejor <= "1959-01"), "\n")
c24 <- orig <= 120
R24 <- t(sapply(res[c24], function(e) sqrt(colMeans(e^2))))
cat("origenes h = 24:", nrow(R24), "\n"); print(round(colMeans(R24), 2)); cat("texto: 26.00 26.61 27.80 28.30\n")
print(round(100 * colMeans(R24 < R24[, "sarima"]), 1)); cat("texto: ets_log 49.0\n")
E12 <- t(sapply(res, function(e) abs(e[12, ])))
print(round(colMeans(E12), 2)); cat("texto: sarima 18.22, ets_log 15.96; puesto del SARIMA:", rank(colMeans(E12))[["sarima"]], "\n")
cat("\n-- la armonica con stepwise = FALSE, approximation = FALSE en cada origen (la busqueda de la particion y del M10) --\n")
t0 <- Sys.time()
resB <- lapply(orig, function(k) { h <- min(24, 144 - k); P <- pron(k, h, FALSE)[, "armonica"]; as.numeric(y)[k + 1:h] - P })
cat("tiempo", round(as.numeric(difftime(Sys.time(), t0, units = "secs"))), "s\n")
a12 <- sapply(resB, function(e) sqrt(mean(e[1:12]^2)))
cat("h = 12: RMSE medio armonica", round(mean(a12), 2), "(bloque: 22.38) | % que le gana al SARIMA", round(100 * mean(a12 < R12[, "sarima"]), 1), "\n")
cat("orden h = 12 con esta armonica:\n"); m12 <- colMeans(R12); m12["armonica"] <- mean(a12); print(round(sort(m12), 2))
a24 <- sapply(resB[c24], function(e) sqrt(mean(e^2)))
cat("h = 24: RMSE medio armonica", round(mean(a24), 2), "(bloque: 28.30) | %", round(100 * mean(a24 < R24[, "sarima"]), 1), "\n")
cat("mes 12: armonica", round(mean(sapply(resB, function(e) abs(e[12]))), 2), "(bloque: 16.17)\n")
