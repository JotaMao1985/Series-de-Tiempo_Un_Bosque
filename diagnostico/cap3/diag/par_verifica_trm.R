## TRM: cifras del caso 2 del Modulo 9 a partir de precalculo/trm_mensual_2015-01_2026-06.csv
suppressPackageStartupMessages(library(forecast))
d <- read.csv("../../../precalculo/trm_mensual_2015-01_2026-06.csv")
trm <- ts(d$trm, start = c(2015, 1), frequency = 12)
ret <- diff(log(trm)) * 100
cat("n =", length(ret), " banda =", round(1.96/sqrt(length(ret)), 4), "\n")
a <- acf(ret, 20, plot = FALSE)$acf[-1]; p <- as.numeric(pacf(ret, 20, plot = FALSE)$acf)
b <- 1.96/sqrt(length(ret))
cat("ACF fuera:", which(abs(a) > b), round(a[abs(a) > b], 3), "\n")
cat("PACF fuera:", which(abs(p) > b), round(p[abs(p) > b], 3), "\n")
cat("ACF 1:8", round(a[1:8], 3), "\n")
m1 <- arima(ret, order = c(0,0,1), method = "ML")
m0 <- arima(ret, order = c(0,0,1), include.mean = FALSE, method = "ML")
cat("MA(1) con media: theta", round(coef(m1)[1], 4), "se", round(sqrt(m1$var.coef[1,1]), 4),
    "media", round(coef(m1)[2], 4), "se media", round(sqrt(m1$var.coef[2,2]), 4), "\n")
cat("MA(1) sin media: theta", round(coef(m0)[1], 4), "se", round(sqrt(m0$var.coef[1,1]), 4), "\n")
cat("media muestral", round(mean(ret), 4), " sd/sqrt(n)", round(sd(ret)/sqrt(length(ret)), 4),
    " t", round(mean(ret)/(sd(ret)/sqrt(length(ret))), 3), "\n")
aa <- auto.arima(ret); print(aa)
cat("auto.arima trace (que compara con y sin media):\n")
invisible(auto.arima(ret, trace = TRUE))
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
cat("AICc: ruido con media", round(aicc(arima(ret, c(0,0,0)), 137), 3),
    " ruido sin media", round(aicc(arima(ret, c(0,0,0), include.mean = FALSE), 137), 3), "\n")

cat("\n== auto.arima con los argumentos del precalculo (d=0, seasonal=FALSE, stepwise=FALSE, approximation=FALSE)\n")
print(auto.arima(ret, d = 0, seasonal = FALSE, stepwise = FALSE, approximation = FALSE))
cat("\n== auto.arima por defecto sobre la misma serie (lo que haria un estudiante)\n")
print(auto.arima(ret))
cat("\n== auto.arima por defecto, sin estacionalidad\n")
print(auto.arima(ret, seasonal = FALSE))
