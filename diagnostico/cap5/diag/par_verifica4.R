# par_verifica4.R — M6/M7: los 13 primeros residuales del airline en R y su peso en Ljung-Box
suppressMessages(library(forecast))
ap <- log(AirPassengers)
fit <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
r <- residuals(fit)
cat("13 primeros residuales:", round(r[1:13], 5), "\n")
cat("sd de los 13 primeros:", round(sd(r[1:13]), 5), " sd de los 131 restantes:", round(sd(r[-(1:13)]), 5), "\n")
cat("LB24 con los 144:", round(Box.test(r, 24, "Ljung-Box", fitdf = 2)$p.value, 4),
    " | con los 131 sin los 13 primeros:", round(Box.test(r[-(1:13)], 24, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")
cat("LB36 con los 144:", round(Box.test(r, 36, "Ljung-Box", fitdf = 2)$p.value, 4),
    " | con los 131:", round(Box.test(r[-(1:13)], 36, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")
cat("Shapiro con los 144:", round(shapiro.test(r)$p.value, 4), " | con los 131:", round(shapiro.test(r[-(1:13)])$p.value, 4), "\n")
a <- Acf(r[-(1:13)], lag.max = 24, plot = FALSE)$acf
cat("r12, r24 con los 131:", round(a[c(13, 25)], 4), "\n")
u <- Arima(USAccDeaths, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12)); ru <- residuals(u)
cat("USAccDeaths LB24 con 72:", round(Box.test(ru, 24, "Ljung-Box", fitdf = 2)$p.value, 4), " | con 59:",
    round(Box.test(ru[-(1:13)], 24, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")
