# Lector B · M4: ACF y PACF del Nilo sin diferenciar y diferenciado; ARIMA candidatos
suppressMessages(library(forecast))
y <- as.numeric(Nile); w <- diff(y); n0 <- length(y); n1 <- length(w)
cat("banda d=0:", round(1.96/sqrt(n0), 4), " banda d=1:", round(1.96/sqrt(n1), 4), "\n")
pa0 <- pacf(y, lag.max = 8, plot = FALSE)$acf[, 1, 1]; a0 <- acf(y, lag.max = 8, plot = FALSE)$acf[-1]
cat("Nile sin diferenciar: ACF 1..8:", round(a0, 3), "\n                     PACF 1..8:", round(pa0, 3), "\n")
cat("PACF fuera de banda (d=0):", which(abs(pa0) > 1.96/sqrt(n0)), "\n")
pa1 <- pacf(w, lag.max = 20, plot = FALSE)$acf[, 1, 1]; a1 <- acf(w, lag.max = 20, plot = FALSE)$acf[-1]
cat("diff(Nile): PACF 1..12:", round(pa1[1:12], 3), "\n")
cat("ACF fuera de banda (d=1):", which(abs(a1) > 1.96/sqrt(n1)), " valores:", round(a1[abs(a1) > 1.96/sqrt(n1)], 3), "\n")
cat("PACF fuera de banda (d=1):", which(abs(pa1) > 1.96/sqrt(n1)), " valores:", round(pa1[abs(pa1) > 1.96/sqrt(n1)], 3), "\n")
cat("AR(1) phi=.5, ACF teórica 1..4:", 0.5^(1:4), " banda n=100:", round(1.96/10, 3), "\n")
cat("limites inferior del MA(1): rho1 = theta/(1+theta^2) en theta=-1:", -1/(1+1), "\n")
cat("2da diferencia de ruido blanco: rho1 teórico -0.5; Nile d=2 r1:", round(acf(diff(y, differences = 2), plot = FALSE)$acf[2], 3), "\n")
ma1 <- Arima(Nile, order = c(0,1,1), method = "ML"); cat("IMA(1,1): theta", round(coef(ma1), 4), " alpha=1+theta", round(1+coef(ma1), 3), "\n")
cat("ses(Nile) alpha:", round(ses(Nile)$model$par[["alpha"]], 4), "\n")
cat("auto.arima(Nile) elige:", as.character(forecast::auto.arima(Nile)), "\n")
cat("diferencia AICc (0,1,1)-(1,1,1):", round(Arima(Nile, order=c(0,1,1), method="ML")$aicc - Arima(Nile, order=c(1,1,1), method="ML")$aicc, 2), "\n")
