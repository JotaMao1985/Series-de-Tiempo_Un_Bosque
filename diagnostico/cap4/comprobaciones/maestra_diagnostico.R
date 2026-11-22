# Comprobaciones de la sesión maestra sobre los hallazgos del diagnóstico del cap. 4 (2026-11-22)
suppressPackageStartupMessages(library(forecast))
cat("R", R.version$major, R.version$minor, "· forecast", as.character(packageVersion("forecast")), "\n\n")
y <- Nile
cat("== [G-M9] ARIMA(1,1,1) sin constante: ¿el pronóstico queda en el último nivel?\n")
f <- Arima(y, order = c(1,1,1))
print(round(coef(f), 4))
fc <- forecast(f, h = 30)
cat("ultimo observado:", tail(y, 1), "\n")
cat("h=1, 2, 30:", round(fc$mean[c(1,2,30)], 2), "\n")
phi <- coef(f)["ar1"]; th <- coef(f)["ma1"]; e <- tail(residuals(f), 1)
paso1 <- phi * (y[100] - y[99]) + th * e
lim <- y[100] + paso1 / (1 - phi)
cat("limite analitico y_T + (phi*dy_T + theta*e_T)/(1-phi):", round(lim, 2), "\n\n")

cat("== [P-quiz4] ARIMA(1,1,1) con deriva: deriva frente a c = mu_w*phi(1)\n")
g <- Arima(y, order = c(1,1,1), include.drift = TRUE)
print(round(coef(g), 4))
cat("c = drift*(1-phi):", round(coef(g)["drift"] * (1 - coef(g)["ar1"]), 2),
    "· media muestral de las diferencias:", round(mean(diff(y)), 2), "\n\n")

cat("== [P-M2] Ljung-Box del ARIMA(0,1,1) con y sin el primer residual\n")
h <- Arima(y, order = c(0,1,1))
r <- residuals(h)
cat("primer residual:", round(r[1], 2), "\n")
for (k in c(10, 20)) {
  cat("lag", k, "con r1: p =", round(Box.test(r, k, "Ljung-Box", fitdf = 1)$p.value, 4),
      "· sin r1: p =", round(Box.test(r[-1], k, "Ljung-Box", fitdf = 1)$p.value, 4), "\n")
}

cat("\n== [F-M7] Umbral de las raíces en forecast (código de la versión instalada)\n")
b <- deparse(forecast:::myarima)
cat(grep("minroot", b, value = TRUE), sep = "\n")
cat("\n== [F-M7] ARIMA(2,1,2) del Nilo: menor módulo de raíz AR según el método\n")
for (m in c("CSS-ML", "ML")) {
  a <- Arima(Nile, order = c(2,1,2), method = m)
  cat(m, ": AR", round(min(Mod(polyroot(c(1, -coef(a)[c("ar1","ar2")])))), 4),
      "· MA", round(min(Mod(polyroot(c(1, coef(a)[c("ma1","ma2")])))), 4), "\n")
}
