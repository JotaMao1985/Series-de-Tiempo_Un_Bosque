## Comprobaciones complementarias (par academico, cap. 3)
suppressPackageStartupMessages(library(forecast))
manchas <- window(sunspot.year, start = 1770, end = 1869)
cat("== M6: realizaciones con set.seed(3) en el orden del bloque de R\n")
set.seed(3)
ar1 <- arima.sim(n = 200, model = list(ar = 0.8)); ma1 <- arima.sim(n = 200, model = list(ma = 0.8))
arma <- arima.sim(n = 200, model = list(ar = 0.7, ma = 0.5))
for (nm in c("ar1", "ma1", "arma")) { x <- get(nm); a <- acf(x, 16, plot = FALSE)$acf[-1]
  p <- as.numeric(pacf(x, 16, plot = FALSE)$acf)
  cat(nm, " acf[1:3]", round(a[1:3], 4), " pacf[1:3]", round(p[1:3], 4), "\n") }
b <- 1.96/sqrt(200)
cat("MA(1): rezagos 2..16 de la ACF fuera de la banda:", (2:16)[abs(acf(ma1, 16, plot = FALSE)$acf[-1][-1]) > b], "\n")
cat("AR(1): rezagos 2..16 de la PACF fuera de la banda:", (2:16)[abs(as.numeric(pacf(ar1, 16, plot = FALSE)$acf)[-1]) > b], "\n")

cat("\n== M9: Guerrero sobre la serie desplazada, p con mas cifras\n")
lam <- BoxCox.lambda(manchas + 1, method = "guerrero")
f <- arima(BoxCox(manchas + 1, lam), order = c(2,0,0), method = "ML")
cat(format(Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value, digits = 8), "\n")
f2 <- arima((manchas + 1)^lam, order = c(2,0,0), method = "ML")
cat("con (manchas+1)^lambda sin BoxCox():", format(Box.test(residuals(f2), 12, "Ljung-Box", fitdf = 2)$p.value, digits = 8), "\n")

cat("\n== M7: ML en T=40, phi=0.95: cuantas estimaciones quedan en >= 0.999 (seed 1)\n")
set.seed(1)
est <- replicate(1000, { z <- arima.sim(list(ar = 0.95), n = 40)
  tryCatch(suppressWarnings(coef(arima(z, order = c(1,0,0), include.mean = FALSE, method = "ML"))[[1]]),
           error = function(e) NA_real_) })
cat("ML >= 0.999:", sum(est >= 0.999, na.rm = TRUE), " fallos:", sum(is.na(est)), "\n")
cat("R restringe ML a la region estacionaria via transform.pars = TRUE (por defecto):",
    formals(arima)$transform.pars, "\n")

cat("\n== Ej. 3: elasticidad sobre 1900-1988 frente a 1770-1869 no viene al caso; LB con n parecido\n")
for (v in list(c(1770,1869), c(1789,1888), c(1820,1919), c(1850,1949), c(1889,1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2])); f <- arima(x, order = c(2,0,0), method = "ML")
  cat(sprintf("%d-%d n=%d  LB12 p=%.4f\n", v[1], v[2], length(x), Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value))
}
