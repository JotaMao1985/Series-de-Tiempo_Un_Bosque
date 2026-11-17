# R3b · lo que respalda las frases corregidas tras la verificacion (ninguna cifra de estas se publica).
# Uso: Rscript diagnostico/cap2/comprobaciones/r3b_cifras.R > diagnostico/cap2/comprobaciones/r3b_cifras.out 2>&1
suppressMessages({library(forecast); library(tseries)}); options(warn = -1)

cat("== 1 · que hace ndiffs() (M7, caja de la regla) ==\n")
cat(grep("use.lag|max.d|ur.kpss", deparse(body(ndiffs)), value = TRUE), sep = "\n")
cat("argumentos:", deparse(args(ndiffs))[1:2], "\n")
d12 <- diff(log(AirPassengers), 12); n <- length(d12)
cat(sprintf("sobre nabla_12 log y (n = %d): tseries::kpss.test %.4f con %d rezagos (p = %.4f) | urca::ur.kpss con %d rezagos %.4f (critico 5 %%: 0.463) | ndiffs = %d\n",
    n, kpss.test(d12)$statistic, trunc(4 * (n / 100)^0.25), kpss.test(d12)$p.value,
    trunc(3 * sqrt(n) / 13), urca::ur.kpss(d12, use.lag = trunc(3 * sqrt(n) / 13))@teststat, ndiffs(d12)))
cat(sprintf("nsdiffs: seas.heuristic(log AP) = %.3f (mstl); umbral 0.64\n", forecast:::seas.heuristic(log(AirPassengers))))

cat("\n== 2 · M5: con phi = 0.95 y 200 datos, lo habitual es que las pruebas no lo separen de la raiz unitaria ==\n")
set.seed(2026)
p <- replicate(1000, { y <- arima.sim(list(ar = 0.95), n = 200); c(adf.test(y)$p.value < 0.05, kpss.test(y)$p.value < 0.05) })
cat(sprintf("1000 series AR(1), phi = 0.95, n = 200: el ADF rechaza la raiz unitaria en el %.1f %%; el KPSS de nivel rechaza la estacionariedad en el %.1f %%\n",
    100 * mean(p[1, ]), 100 * mean(p[2, ])))

cat("\n== 5 (menor) · M3: el residuo de decompose() de una serie con error i.i.d. ya trae autocorrelacion ==\n")
set.seed(2026)
f <- replicate(1000, { y <- ts((100 + 2 * (1:144)) * (1 + 0.2 * sin(2 * pi * (1:144) / 12)) * exp(rnorm(144, sd = 0.03)), frequency = 12)
  r <- na.omit(decompose(y, "multiplicative")$random); a <- acf(r, lag.max = 24, plot = FALSE)$acf[-1]
  c(sum(abs(a) > 1.96 / sqrt(length(r))), a[1]) })
cat(sprintf("1000 series multiplicativas con error i.i.d.: barras fuera de 24, media %.2f, percentil 95 %g, maximo %g; r1 medio %.3f. En AirPassengers: 14\n",
    mean(f[1, ]), quantile(f[1, ], 0.95), max(f[1, ]), mean(f[2, ])))

cat("\n== 11 (menor) · M6: el KPSS de tendencia con la estacionalidad dentro y sin ella ==\n")
l <- log(AirPassengers); sa <- seasadj(stl(l, s.window = "periodic"))
k1 <- kpss.test(l, null = "Trend"); k2 <- kpss.test(sa, null = "Trend"); k0 <- kpss.test(AirPassengers, null = "Trend")
cat(sprintf("AirPassengers: %.4f (p %.2f) | log: %.4f (p %.2f) | log desestacionalizada: %.4f (p %.2f)\n",
    k0$statistic, k0$p.value, k1$statistic, k1$p.value, k2$statistic, k2$p.value))

cat("\n== 4 · M9, resumen: el Monte Carlo del M6 (de DATOS_CAP2) ==\n")
cat("amplitud 0, 0.5, 1, 2, 4 -> 3.2, 3.6, 5.0, 11.2, 17.6 % de rechazos (precalculo/salidas/cap2_estacionariedad.json)\n")

cat("\n== 12 (menor) · M9, cierre: la serie final no pide mas ni menos diferencias ==\n")
w <- diff(diff(l, 12)); cat("ndiffs, nsdiffs de la serie final:", ndiffs(w), nsdiffs(w), "| ndiffs(nabla_12 log y):", ndiffs(d12), "| nsdiffs(log y):", nsdiffs(l), "\n")
