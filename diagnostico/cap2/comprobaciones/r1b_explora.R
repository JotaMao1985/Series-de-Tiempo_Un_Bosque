# R1 del capítulo 2, tras la verificación · cifras nuevas.
#   Rscript diagnostico/cap2/comprobaciones/r1b_explora.R > diagnostico/cap2/comprobaciones/r1b_explora.out 2>&1
suppressMessages({library(tseries); library(forecast)})
banda <- function(x) 1.96 / sqrt(length(x))
fuera <- function(x, K = 24) { r <- acf(x, K, plot = FALSE)$acf[-1]; which(abs(r) > banda(x)) }

cat("== M3 · ejemplo de «decaimiento rápido»: y_t = 0.5 y_{t-1} + e_t, 200 valores ==\n")
cat("Criterio, fijado antes de mirar: la primera semilla (1, 2, 3…) con la que, de 24 rezagos, solo quedan fuera\n")
cat("de la banda los primeros y seguidos (1, o 1-2, o 1-2-3), con r1 > r2 > r3 > 0.\n")
for (s in 1:200) { set.seed(s); x <- arima.sim(list(ar = 0.5), n = 200); f <- fuera(x)
  r <- acf(x, 24, plot = FALSE)$acf[-1]
  ok <- length(f) >= 1 && length(f) <= 3 && identical(f, seq_along(f)) && r[1] > r[2] && r[2] > r[3] && r[3] > 0
  cat(sprintf("semilla %2d · fuera: %-22s · r1..r4 = %s%s\n", s, paste(f, collapse = " "), paste(sprintf("%.3f", r[1:4]), collapse = " "),
              if (ok) "   <-- la primera que cumple" else ""))
  if (ok) break }
cat("máx |r_k| para k >= 4:", round(max(abs(r[4:24])), 3), "· banda ±", round(banda(x), 4), "· teórico 0.5^k: 0.5 0.25 0.125\n")

cat("\n== M7 · la varianza no decide, en ningún sentido ==\n")
set.seed(1); y <- arima.sim(list(ar = 0.8), n = 200)
cat(sprintf("AR(1) phi = 0.8 (set.seed(1), n = 200): ndiffs = %d · var %.3f -> %.3f · r1(y) = %.4f · 2(1 - r1) = %.3f · razón = %.3f · r1(dy) = %.3f\n",
            ndiffs(y), var(y), var(diff(y)), acf(y, 1, plot = FALSE)$acf[2], 2 * (1 - acf(y, 1, plot = FALSE)$acf[2]), var(diff(y)) / var(y), acf(diff(y), 1, plot = FALSE)$acf[2]))
set.seed(4); z <- arima.sim(list(order = c(0, 1, 1), ma = -0.8), n = 143)
a <- acf(z, 24, plot = FALSE)$acf[-1]
cat(sprintf("ARIMA(0,1,1) theta = -0.8 (set.seed(4), n = 143 -> length %d): ndiffs = %d · var %.3f -> %.3f · r1(z) = %.4f · 2(1 - r1) = %.3f · razón = %.3f · r1(dz) = %.3f\n",
            length(z), ndiffs(z), var(z), var(diff(z)), a[1], 2 * (1 - a[1]), var(diff(z)) / var(z), acf(diff(z), 1, plot = FALSE)$acf[2]))
cat("   ACF de z, r1..r8:", sprintf("%.3f", a[1:8]), "· fuera de banda:", fuera(z), "\n")
cat(sprintf("   adf p = %.3f · kpss p = %.3f\n", suppressWarnings(adf.test(z))$p.value, suppressWarnings(kpss.test(z))$p.value))
lx <- log(AirPassengers); d12 <- diff(lx, lag = 12)
cat(sprintf("d12: var %.5f -> %.5f · 2(1 - r1) var = %.5f\n", var(d12), var(diff(d12)), 2 * (1 - acf(d12, 1, plot = FALSE)$acf[2]) * var(d12)))
for (nm in c("lx", "trm")) { x <- if (nm == "lx") lx else ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
  for (d in 0:2) { u <- if (d == 0) x else diff(x, differences = d)
    cat(sprintf("%s d = %d -> %d: razón de varianzas %.3f · 2(1 - r1) = %.3f\n", nm, d, d + 1, var(diff(u)) / var(u), 2 * (1 - acf(u, 1, plot = FALSE)$acf[2]))) } }

cat("\n== Ejercicio 1 · co2: el correlograma tras la diferencia estacional ==\n")
s <- diff(co2, lag = 12); a <- acf(s, 24, plot = FALSE)$acf[-1]
cat(sprintf("co2_s: n = %d · banda ±%.4f · r1..r6 = %s · fuera: %d de 24 (%s)\n", length(s), banda(s),
            paste(sprintf("%.4f", a[1:6]), collapse = " "), length(fuera(s)), paste(fuera(s), collapse = " ")))
sd2 <- diff(s); b <- acf(sd2, 24, plot = FALSE)$acf[-1]
cat(sprintf("co2_sd: n = %d · r1 = %.4f · fuera: %d de 24 · ndiffs = %d · nsdiffs = %d · kpss p = %.3f\n", length(sd2), b[1], length(fuera(sd2)),
            ndiffs(sd2), nsdiffs(sd2), suppressWarnings(kpss.test(sd2))$p.value))
cat("\n== Ejercicio 3 · USAccDeaths ==\n"); y <- USAccDeaths
cat("ndiffs(diff(y, 12)) =", ndiffs(diff(y, lag = 12)), "· ndiffs y nsdiffs de la doble diferencia:", ndiffs(diff(diff(y), lag = 12)), nsdiffs(diff(diff(y), lag = 12)), "\n")
