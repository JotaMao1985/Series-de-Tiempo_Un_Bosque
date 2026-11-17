# v4_software_2.R — segunda lectura del verificador independiente (R4, cap. 2).
# c2-m4-04: cuánto difiere pacf() del último coeficiente MCO, en una serie no
# estacionaria y en estacionarias. c2-m7-08: cociente de varianzas frente a
# 2(1 - r1) en muestras de series estacionarias. Salida: v4_software_2.out
ols_pacf <- function(x, K) sapply(1:K, function(k) { z <- x - mean(x); X <- embed(z, k + 1)
  coef(lm(X[, 1] ~ X[, -1] - 1))[k] })
dif <- function(x, K = 24) max(abs(as.numeric(pacf(x, K, plot = FALSE)$acf) - ols_pacf(x, K)))
ly <- log(AirPassengers)
cat("== c2-m4-04: max |pacf() - MCO|, k = 1..24\n")
cat("log(AirPassengers):", dif(ly), "\n")
cat("diff(diff(log AP), 12):", dif(diff(diff(ly), 12)), "\n")
set.seed(2026)
for (phi in c(0.5, 0.8)) for (n in c(144, 500)) {
  d <- replicate(200, dif(arima.sim(list(ar = phi), n), 12))
  cat(sprintf("AR(1) phi=%.1f n=%d: mediana %.3f · p90 %.3f\n", phi, n, median(d), quantile(d, .9))) }
cat("\n== c2-m7-08: Var(diff)/Var frente a 2(1 - r1) en series estacionarias simuladas\n")
for (phi in c(0, 0.5, 0.8, 0.95)) {
  e <- replicate(500, { z <- arima.sim(list(ar = phi), 200); if (phi == 0) z <- rnorm(200)
    r1 <- acf(z, 1, plot = FALSE)$acf[2]; c(var(diff(z)) / var(z), 2 * (1 - r1)) })
  cat(sprintf("phi=%.2f: |cociente - 2(1-r1)| mediana %.4f, máx %.4f · signos distintos (cociente<1 vs r1>0.5): %d de 500\n",
      phi, median(abs(e[1, ] - e[2, ])), max(abs(e[1, ] - e[2, ])), sum((e[1, ] < 1) != (e[2, ] < 1)))) }
