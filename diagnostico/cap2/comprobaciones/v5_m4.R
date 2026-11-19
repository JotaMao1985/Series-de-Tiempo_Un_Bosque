set.seed(7); A <- arima.sim(list(ar = c(0.5, 0.3)), n = 200)
set.seed(3); B <- arima.sim(list(ma = 0.8), n = 200)
fuera <- function(x, rezagos) {
  banda <- 1.96 / sqrt(length(x))
  c(acf  = toString(which(abs(acf(x,  lag.max = rezagos, plot = FALSE)$acf[-1]) > banda)),
    pacf = toString(which(abs(pacf(x, lag.max = rezagos, plot = FALSE)$acf) > banda)))
}
print(fuera(A, 24)); print(round(pacf(A, lag.max = 24, plot = FALSE)$acf[1:4], 3))
print(round(acf(A, lag.max = 8, plot = FALSE)$acf[2:9], 3))
print(fuera(B, 24)); print(round(acf(B, lag.max = 24, plot = FALSE)$acf[2:5], 3))
print(round(pacf(B, lag.max = 24, plot = FALSE)$acf[1:5], 3))
print(round(1.96 / sqrt(length(LakeHuron)), 3)); print(length(LakeHuron)); print(tsp(LakeHuron))
print(fuera(LakeHuron, 20))
print(round(acf(LakeHuron, lag.max = 20, plot = FALSE)$acf[2:11], 3))
print(round(pacf(LakeHuron, lag.max = 20, plot = FALSE)$acf[1:10], 3))
suppressMessages(library(tseries))
print(suppressWarnings(adf.test(LakeHuron))); print(suppressWarnings(kpss.test(LakeHuron, null="Trend")))
cat("---M5\n")
set.seed(37); e <- rnorm(200); t <- 1:200
A <- 0.2 * t + e; B <- cumsum(0.2 + e)
huella <- function(x) { r <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  c(r1 = round(r[1], 3), fuera = sum(abs(r) > 1.96 / sqrt(length(x)))) }
print(rbind("A sin su recta" = huella(residuals(lm(A ~ t))), "A diferenciada" = huella(diff(A)),
      "B sin su recta" = huella(residuals(lm(B ~ t))), "B diferenciada" = huella(diff(B))))
print(round(c(pendiente = unname(coef(lm(B ~ t))[2]), media_de_los_cambios = mean(diff(B))), 3))
print(round(c(A = max(abs(A - 0.2 * t)), B = max(abs(B - 0.2 * t))), 1))
cat("---M6\n")
linea <- function(prueba) round(c(estadistico = unname(prueba$statistic), p = prueba$p.value), 3)
print(linea(adf.test(nhtemp))); print(linea(suppressWarnings(kpss.test(nhtemp))))
print(linea(suppressWarnings(kpss.test(nhtemp, null = "Trend"))))
print(trunc((length(nhtemp) - 1)^(1/3)))
print(round(sapply(1:5, function(k) suppressWarnings(adf.test(nhtemp, k = k))$p.value), 3))
print(round(sapply(0:6, function(k) suppressWarnings(adf.test(nhtemp, k = k))$statistic), 3))
tt <- time(nhtemp); sin_recta <- residuals(lm(nhtemp ~ tt))
print(round(c(sin_recta = acf(sin_recta, plot = FALSE)$acf[2], diferenciada = acf(diff(nhtemp), plot = FALSE)$acf[2]), 3))
print(round(1.96 / sqrt(length(nhtemp)), 3)); print(tsp(nhtemp))
print(acf(sin_recta, plot=FALSE, lag.max=10)$acf[2:6])
print(which(abs(acf(sin_recta, plot=FALSE, lag.max=20)$acf[-1])>0.253))
print(which(abs(acf(diff(nhtemp), plot=FALSE, lag.max=20)$acf[-1])>1.96/sqrt(59)))
