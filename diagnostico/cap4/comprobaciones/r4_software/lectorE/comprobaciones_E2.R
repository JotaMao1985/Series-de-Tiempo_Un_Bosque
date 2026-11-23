# Lector E · comprobaciones adicionales (R 4.6.0, forecast 9.0.2). Desde Htmls_Series/datos.
suppressMessages(library(forecast))
trm <- ts(read.csv("trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
cat("== ACF de la TRM en niveles, rezago 1:", round(acf(trm, plot = FALSE)$acf[2], 3), "\n")
ret <- diff(log(trm))
cat("== Log-retornos: Ljung-Box en los rezagos 6, 12, 20 (los del Capítulo 3):",
    round(sapply(c(6, 12, 20), function(l) Box.test(ret, l, "Ljung-Box")$p.value), 4), "\n")
cat("== Nilo: nobs de los ARIMA(1,1,1) y (1,2,2):", arima(Nile, c(1, 1, 1), method = "ML")$nobs,
    arima(Nile, c(1, 2, 2), method = "ML")$nobs, " (n =", length(Nile), ")\n")
cat("== Producto (1 + th B)(1 + Th B^12): lugares con coeficiente no nulo (rezagos):\n")
th <- 0.5; Th <- 0.3
p <- convolve(c(1, th), rev(c(1, rep(0, 11), Th)), type = "open")
cat("  rezagos con coeficiente:", which(abs(p) > 1e-12) - 1, " coef:", round(p[abs(p) > 1e-12], 3), "(th*Th =", th * Th, ")\n")
d1 <- diff(trm); n <- length(d1)
g1 <- mean((d1 - mean(d1))^3) / mean((d1 - mean(d1))^2)^1.5
cat("== Asimetría de los cambios:", round(g1, 3), " error estándar aprox sqrt(6/n) =", round(sqrt(6 / n), 3),
    " cociente =", round(g1 / sqrt(6 / n), 2), "\n")
# Cobertura en la muestra del 95 % a 12 meses: 11 de 126 fuera
cat("== 12 meses: cobertura en la muestra =", round(1 - 11 / 126, 3), "\n")
cat("== Nilo (1,1,1) con deriva: AICc frente a sin deriva\n")
f0 <- Arima(Nile, c(1, 1, 1)); f1 <- Arima(Nile, c(1, 1, 1), include.drift = TRUE)
cat("  AICc sin deriva", round(f0$aicc, 2), " con deriva", round(f1$aicc, 2), " drift =", round(coef(f1)[["drift"]], 3),
    " t =", round(coef(f1)[["drift"]] / sqrt(f1$var.coef["drift", "drift"]), 2), "\n")
