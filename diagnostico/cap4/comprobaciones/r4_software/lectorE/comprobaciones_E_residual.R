# Comentario del bloque Python de la TRM (c4-m10-43): primer residual de arima() y «quitándoselo»
suppressMessages(library(forecast))
trm <- ts(read.csv("trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
rw <- arima(trm, order = c(0, 1, 0), method = "ML"); e <- residuals(rw)
cat("primer residual de R:", round(e[1], 3), " segundo:", round(e[2], 3), " y_1/sqrt(1e6+1) =", round(trm[1] / sqrt(1e6 + 1), 3), "\n")
cat("p con el primero :", round(c(Box.test(e, 20, "Ljung-Box")$p.value, Box.test(e, 12, "Ljung-Box")$p.value,
    shapiro.test(e)$p.value, Box.test(e^2, 12, "Ljung-Box")$p.value), 4), "\n")
e2 <- e[-1]
cat("p sin el primero :", round(c(Box.test(e2, 20, "Ljung-Box")$p.value, Box.test(e2, 12, "Ljung-Box")$p.value,
    shapiro.test(e2)$p.value, Box.test(e2^2, 12, "Ljung-Box")$p.value), 4), "\n")
