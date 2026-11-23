# Lector B · c4-m3-19, -20, -31, -34 y la frase «más rezagos inflan σ²_LP»
suppressMessages({library(tseries); library(urca)})
y <- as.numeric(Nile); n <- length(y)

kpss_manual <- function(y, l) {
  e <- y - mean(y); S <- cumsum(e); n <- length(y)
  g <- function(j) sum(e[(j+1):n] * e[1:(n-j)]) / n     # autocovarianza muestral, divisor n
  s2 <- g(0) + 2 * sum(sapply(seq_len(l), function(j) (1 - j/(l+1)) * g(j)))
  list(stat = sum(S^2) / (n^2 * s2), s2lp = s2)
}
cat("== El estadístico KPSS escrito en el capítulo, calculado a mano\n")
for (l in c(4, 12)) {
  m <- kpss_manual(y, l)
  t <- suppressWarnings(kpss.test(y, lshort = (l == 4)))
  cat(sprintf("l = %2d: a mano %.10f | tseries::kpss.test %.10f | diferencia %.2e | sigma2_LP = %.2f\n",
              l, m$stat, as.numeric(t$statistic), abs(m$stat - as.numeric(t$statistic)), m$s2lp))
}
cat("sigma2_LP(l=12) > sigma2_LP(l=4):", kpss_manual(y, 12)$s2lp > kpss_manual(y, 4)$s2lp, "\n")
cat("autocovarianzas muestrales 1..12 de Nile - media (divisor n):\n")
e <- y - mean(y); print(round(sapply(1:12, function(j) sum(e[(j+1):n]*e[1:(n-j)])/n) / (sum(e^2)/n), 3))

cat("\n== Truncamientos: kpss.test (tseries) frente a ndiffs (urca::ur.kpss, use.lag = trunc(3*sqrt(n)/13))\n")
cat("trunc(4*(n/100)^0.25) =", trunc(4*(n/100)^0.25), " trunc(12*(n/100)^0.25) =", trunc(12*(n/100)^0.25),
    " ceiling(12*(n/100)^0.25) =", ceiling(12*(n/100)^0.25), " trunc(3*sqrt(n)/13) =", trunc(3*sqrt(n)/13), "\n")
u <- ur.kpss(y, type = "mu", use.lag = trunc(3*sqrt(n)/13)); cat("ur.kpss(Nile, 'mu', use.lag = 2):", round(u@teststat, 4), " lag", u@lag, "\n")
cat("kpss manual con l = 2:", round(kpss_manual(y, 2)$stat, 4), "\n")

cat("\n== Bajo raíz unitaria el estadístico KPSS crece con n (caminata aleatoria, regla l = trunc(4*(n/100)^0.25))\n")
set.seed(2026)
for (nn in c(100, 400, 1600)) {
  st <- replicate(200, { x <- cumsum(rnorm(nn)); kpss_manual(x, trunc(4*(nn/100)^0.25))$stat })
  cat(sprintf("n = %4d: KPSS medio %.2f  (mínimo %.2f)  rechaza al 5%% (0.463): %.0f%%\n", nn, mean(st), min(st), 100*mean(st > 0.463)))
}
cat("\n== Crecimiento de S_t = sumas parciales de los residuales para una caminata (media del max|S_t| / n^1.5)\n")
for (nn in c(100, 400, 1600)) {
  r <- replicate(200, { x <- cumsum(rnorm(nn)); e <- x - mean(x); max(abs(cumsum(e))) / nn^1.5 })
  cat(sprintf("n = %4d: max|S_t| / n^(3/2) = %.3f\n", nn, mean(r)))
}
