# Recomprobación de la sesión maestra (2026-11-16) de las cifras que la R1 cambió
# por doble redondeo, desde el CSV congelado que lee el capítulo.
suppressMessages({library(tseries)})
d <- read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
trm <- ts(d$trm, start = c(2015, 1), frequency = 12)
cat("n =", length(trm), "· de", d$mes[1], "a", d$mes[nrow(d)], "\n")
a <- suppressWarnings(adf.test(trm)); cat(sprintf("ADF TRM: stat %.4f · p %.6f -> %.3f\n", a$statistic, a$p.value, a$p.value))
k <- suppressWarnings(kpss.test(diff(trm))); cat(sprintf("KPSS diff TRM: stat %.6f -> %.3f\n", k$statistic, k$statistic))
for (kk in c(5, 12)) { x <- suppressWarnings(adf.test(log(trm), k = kk)); cat(sprintf("ADF log TRM k=%d: %.6f -> %.3f\n", kk, x$statistic, x$statistic)) }
s <- read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
j <- jsonlite::fromJSON("precalculo/salidas/datos_series.json")
cat("CSV = datos_series.json:", isTRUE(all.equal(as.numeric(j$trm$valores), s$trm)), "\n")
cat(sprintf("E3 r1 de USAccDeaths: %.6f -> %.3f\n", acf(USAccDeaths, plot = FALSE)$acf[2], acf(USAccDeaths, plot = FALSE)$acf[2]))
for (kk in c(5, 12)) { x <- suppressWarnings(adf.test(log(AirPassengers), k = kk)); cat(sprintf("ADF log AirPassengers k=%d: %.6f -> %.3f\n", kk, x$statistic, x$statistic)) }

cat("\n[verificador, bloquea] ¿una diferencia que hace falta siempre reduce la varianza?\n")
suppressMessages(library(forecast))
set.seed(4); y <- arima.sim(list(order = c(0,1,1), ma = -0.8), n = 143)
cat(sprintf("ARIMA(0,1,1) theta=-0.8: ndiffs = %d · var(y) = %.3f · var(diff y) = %.3f\n", ndiffs(y), var(y), var(diff(y))))
set.seed(2026); r <- replicate(500, { z <- arima.sim(list(order = c(0,1,1), ma = -0.8), n = 143); c(var(diff(z)) > var(z), ndiffs(z)) })
cat(sprintf("500 series: sube la varianza en %.1f %% · de esas, ndiffs = 1 en %.1f %%\n", 100*mean(r[1,]), 100*mean(r[2, r[1,] == 1] == 1)))
