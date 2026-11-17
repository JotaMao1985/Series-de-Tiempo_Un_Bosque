# Recomprobación de la sesión maestra (2026-11-16) de los errores de más peso
# que reportó el par académico del capítulo 2. Se ejecuta desde la raíz del repo.
suppressMessages({library(jsonlite); library(tseries); library(forecast)})
sd <- fromJSON("precalculo/salidas/datos_series.json")
trm <- ts(as.numeric(sd$trm$valores), start = as.integer(sd$trm$inicio), frequency = 12)
cat("TRM:", length(trm), "meses\n")

cat("\n[E1] ACF de diff(TRM), 24 rezagos, banda ±1.96/sqrt(T)\n")
d <- diff(trm); r <- acf(d, 24, plot = FALSE)$acf[-1]; b <- 1.96/sqrt(length(d))
cat(sprintf("banda = ±%.4f · r1 = %.3f\n", b, r[1]))
fuera <- which(abs(r) > b); cat("rezagos fuera:", fuera, " valores:", round(r[fuera], 3), "\n")

cat("\n[E4] ¿la primera diferencia de más siempre aumenta la varianza?\n")
set.seed(1); y <- arima.sim(list(ar = 0.8), n = 200)
cat(sprintf("AR(1) phi=0.8: ndiffs = %d · var(y) = %.3f · var(diff y) = %.3f\n",
            ndiffs(y), var(y), var(diff(y))))
cat("teórico Var(diff)/Var(y) = 2(1-phi) =", 2*(1-0.8), "\n")

cat("\n[E5] recuadro del M7: la serie diff12 log AirPassengers\n")
s <- diff(log(AirPassengers), lag = 12)
cat(sprintf("n = %d · kpss.test = %.3f (p = %.3f) · ndiffs = %d\n", length(s),
            kpss.test(s)$statistic, kpss.test(s)$p.value, ndiffs(s)))
a <- acf(s, 24, plot = FALSE)$acf[-1]
cat("r1..r3 =", round(a[1:3], 3), " r12 =", round(a[12], 3), "\n")
cat(sprintf("var(s) = %.4f · var(diff s) = %.4f\n", var(s), var(diff(s))))
s2 <- diff(log(AirPassengers)); cat("r12 de diff(log AP) (la otra serie) =", round(acf(s2, 24, plot = FALSE)$acf[13], 3), "\n")

cat("\n[software] truncamiento del KPSS dentro de forecast::ndiffs y en urca::ur.kpss\n")
cuerpo <- paste(deparse(forecast::ndiffs), collapse = "\n")
cat("ndiffs menciona:", regmatches(cuerpo, gregexpr("ur\\.kpss\\([^)]*\\)|3 \\* sqrt\\([^)]*\\)[^\n]*", cuerpo))[[1]], sep = "\n  ")
u <- paste(deparse(urca::ur.kpss), collapse = "\n")
cat("ur.kpss, lags = 'short':", regmatches(u, regexpr("trunc\\(4 \\* \\(n/100\\)\\^0\\.25\\)", u)), "\n")
