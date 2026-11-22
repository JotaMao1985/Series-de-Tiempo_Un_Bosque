# Réplica EXACTA del Monte Carlo del escalón de precalculo/genera_cap4.R (misma
# semilla, mismo orden de consumo de números aleatorios) para confirmar las cifras
# de la prosa del M3: 4.8 %, 100 %, 0.5 %, 86.4 %, 5.4 %, malla 4.5 %, 70.8 %, 44.5 %,
# KPSS medio 1.07 y 1.23.
suppressMessages({library(forecast); library(tseries)})
nilo <- Nile
escalon <- as.numeric(time(nilo) >= 1899)
fe <- arima(nilo, order = c(0,0,0), xreg = escalon, method = "ML")
res_esc <- as.numeric(residuals(fe))
mc_escalon <- function(n_rep = 1000, n = 100, delta, sigma, pos = 29) {
  e <- as.numeric(seq_len(n) >= pos)
  cuenta <- function(dl) {
    kr <- 0; nk <- integer(0); na <- integer(0); anr <- 0
    for (i in seq_len(n_rep)) {
      x <- 1000 + dl * e + rnorm(n, 0, sigma)
      if (suppressWarnings(kpss.test(x)$p.value) <= 0.05) kr <- kr + 1
      if (suppressWarnings(adf.test(x)$p.value) > 0.05) anr <- anr + 1
      nk <- c(nk, suppressWarnings(ndiffs(x, test = "kpss")))
      na <- c(na, suppressWarnings(ndiffs(x, test = "adf")))
    }
    round(c(kpss_rechaza = kr/n_rep, adf_test_no_rechaza = anr/n_rep,
            ndiffs_kpss = mean(nk >= 1), ndiffs_adf = mean(na >= 1)), 4)
  }
  rbind(sin_escalon = cuenta(0), con_escalon = cuenta(delta))
}
set.seed(2026)
print(mc_escalon(1000, 100, as.numeric(coef(fe)["escalon"]), sd(res_esc), 29))
set.seed(2026)
deltas <- c(0, 25, 50, 75, 100, 150, 200, 250, 300)
e <- as.numeric(1:100 >= 29); s <- sd(res_esc)
malla <- t(sapply(deltas, function(dl) {
  est <- numeric(400); r4 <- 0; r12 <- 0; nd <- integer(400)
  for (i in 1:400) {
    x <- 1000 + dl * e + rnorm(100, 0, s)
    k <- suppressWarnings(kpss.test(x)); est[i] <- k$statistic
    r4 <- r4 + (k$p.value <= 0.05)
    r12 <- r12 + (suppressWarnings(kpss.test(x, lshort = FALSE)$p.value) <= 0.05)
    nd[i] <- suppressWarnings(ndiffs(x, test = "kpss"))
  }
  round(c(delta = dl, sd = dl/s, kpss_medio = mean(est), rechazo_l4 = r4/400, rechazo_l12 = r12/400,
          ndiffs_medio = mean(nd)), 4)
}))
print(malla)
cat("kpss.test(lshort=FALSE) usa l =", trunc(12*(100/100)^0.25), "con n = 100\n")
