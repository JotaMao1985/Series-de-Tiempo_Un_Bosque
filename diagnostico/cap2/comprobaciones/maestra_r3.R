# Recomprobación de la sesión maestra (2026-11-17): el caso de log(UKgas) con el
# que la R3 ilustra el orden de las diferencias, y el KPSS de tendencia de AirPassengers.
suppressMessages({library(forecast); library(tseries)})
y <- log(UKgas)
cat("nsdiffs(log UKgas) =", nsdiffs(y), "· ndiffs(log UKgas) =", ndiffs(y), "\n")
s <- diff(y, lag = 4)
cat(sprintf("estacional primero: ndiffs(diff4) = %d · r1(diff4) = %.3f\n", ndiffs(s), acf(s, plot = FALSE)$acf[2]))
r <- diff(y)
cat(sprintf("regular primero: nsdiffs(diff1) = %d\n", nsdiffs(r)))
rr <- diff(r, lag = 4)
cat(sprintf("regular y luego estacional: r1 = %.3f · ndiffs = %d\n", acf(rr, plot = FALSE)$acf[2], ndiffs(rr)))
k <- suppressWarnings(kpss.test(AirPassengers, null = "Trend"))
cat(sprintf("KPSS de tendencia, AirPassengers: %.4f · p = %.4f\n", k$statistic, k$p.value))
