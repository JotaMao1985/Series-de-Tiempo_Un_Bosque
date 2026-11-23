# Lector B · c4-m3-18 y c4-m3-34: reproducción del Monte Carlo del escalón y de la malla
# (receta copiada de precalculo/genera_cap4.R §«¿Un cambio de nivel…?»; NO se reejecuta el generador)
suppressMessages({library(forecast); library(tseries)})
nilo <- Nile; n_nilo <- length(nilo)
escalon <- as.numeric(time(nilo) >= 1899)
fit_escalon <- arima(nilo, order = c(0,0,0), xreg = escalon, method = "ML")
res_esc <- as.numeric(residuals(fit_escalon))
delta_nilo <- as.numeric(fit_escalon$coef["escalon"]); sigma <- sd(res_esc)
cat(sprintf("beta = %.2f  sigma = %.2f  beta/sigma = %.3f\n", delta_nilo, sigma, abs(delta_nilo)/sigma))

mc_escalon <- function(n_rep = 1000, n = 100, delta, sigma, pos = 29) {
  escalon_sim <- as.numeric(seq_len(n) >= pos)
  cuenta <- function(delta_usado) {
    kpss_rechaza <- 0; nd_kpss <- integer(0); nd_adf <- integer(0); adf_no <- 0
    for (i in seq_len(n_rep)) {
      x <- 1000 + delta_usado * escalon_sim + rnorm(n, 0, sigma)
      if (suppressWarnings(kpss.test(x)$p.value) <= 0.05) kpss_rechaza <- kpss_rechaza + 1
      if (suppressWarnings(adf.test(x)$p.value) > 0.05) adf_no <- adf_no + 1
      nd_kpss <- c(nd_kpss, suppressWarnings(ndiffs(x, test = "kpss")))
      nd_adf  <- c(nd_adf,  suppressWarnings(ndiffs(x, test = "adf")))
    }
    c(kpss_rechaza = kpss_rechaza / n_rep, adf_test_no_rechaza = adf_no / n_rep,
      ndiffs_kpss_1_o_mas = mean(nd_kpss >= 1), ndiffs_adf_1_o_mas = mean(nd_adf >= 1))
  }
  list(sin_escalon = cuenta(0), con_escalon = cuenta(delta))
}
set.seed(2026)
mc <- mc_escalon(1000, n_nilo, delta_nilo, sigma, which(time(nilo) == 1899))
cat("\nMonte Carlo (1000 réplicas)\nsin escalón:\n"); print(round(mc$sin_escalon, 4))
cat("con escalón:\n"); print(round(mc$con_escalon, 4))

set.seed(2026)
escalon_mc <- as.numeric(seq_len(n_nilo) >= which(time(nilo) == 1899))
deltas <- c(0, 25, 50, 75, 100, 150, 200, 250, 300)
cat("\nMalla (400 réplicas por punto)\n")
for (dl in deltas) {
  est <- numeric(400); rech <- 0; rech12 <- 0
  for (i in 1:400) {
    x <- 1000 + dl * escalon_mc + rnorm(n_nilo, 0, sigma)
    k <- suppressWarnings(kpss.test(x)); est[i] <- as.numeric(k$statistic)
    if (k$p.value <= 0.05) rech <- rech + 1
    if (suppressWarnings(kpss.test(x, lshort = FALSE)$p.value) <= 0.05) rech12 <- rech12 + 1
    suppressWarnings(ndiffs(x, test = "kpss"))     # el generador lo llama: no consume números aleatorios
  }
  cat(sprintf("delta = %3d  KPSS medio %.4f  rechaza (l=4) %.4f  rechaza (l=12) %.4f  salto = %.3f sigmas\n",
              dl, mean(est), rech/400, rech12/400, dl/sigma))
}
