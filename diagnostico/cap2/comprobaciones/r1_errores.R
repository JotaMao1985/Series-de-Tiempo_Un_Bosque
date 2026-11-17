# R1 del capítulo 2 · comprobaciones de los siete errores (T1.1) y de las
# imprecisiones (T1.2). Se ejecuta desde la raíz del repo:
#   Rscript diagnostico/cap2/comprobaciones/r1_errores.R > diagnostico/cap2/comprobaciones/r1_errores.out 2>&1
suppressMessages({library(jsonlite); library(tseries); library(forecast)})
options(warn = 1)
sd <- fromJSON("precalculo/salidas/datos_series.json")
trm <- ts(as.numeric(sd$trm$valores), start = as.integer(sd$trm$inicio), frequency = 12)
AP <- AirPassengers; lx <- log(AP); d1 <- diff(lx); d12 <- diff(lx, lag = 12); dd <- diff(d1, lag = 12)
banda <- function(x) 1.96 / sqrt(length(x))
fuera <- function(x, K = 24) { r <- acf(x, K, plot = FALSE)$acf[-1]; which(abs(r) > banda(x)) }
ar1 <- function(phi, e) { y <- numeric(length(e)); y[1] <- e[1]
  for (t in 2:length(e)) y[t] <- phi * y[t - 1] + e[t]; y }
set.seed(2026); e <- rnorm(200)

cat("== E1 · M3, fila «decaimiento rápido»: lo publicado y el ejemplo que lo sustituye ==\n")
r <- acf(diff(trm), 24, plot = FALSE)$acf[-1]
cat(sprintf("dTRM: banda ±%.4f · r1 = %.4f · rezagos fuera: %s (r8 = %.4f)\n",
            banda(diff(trm)), r[1], paste(fuera(diff(trm)), collapse = " "), r[8]))
for (phi in c(0.5, 0.7, 0.8)) {
  y <- ar1(phi, e); r <- acf(y, 24, plot = FALSE)$acf[-1]
  cat(sprintf("AR(1) phi = %.1f sobre el ruido del M2 (set.seed(2026), n = 200): banda ±%.4f\n", phi, banda(y)))
  cat("   r1..r6 muestral:", sprintf("%.4f", r[1:6]), "\n")
  cat("   phi^k teórico  :", sprintf("%.4f", phi^(1:6)), "\n")
  cat("   rezagos fuera de la banda:", fuera(y), "\n")
}

cat("\n== E2 · M5: la primera diferencia de un AR(1); rho1(dy) = -(1 - phi)/2 ==\n")
for (phi in c(0, 0.3, 0.5, 0.7, 0.95, 1, 1.05)) {
  y <- ar1(phi, e); d <- diff(y); r <- acf(d, 24, plot = FALSE)$acf[-1]
  cat(sprintf("phi = %.2f · r1(dy) = %7.4f · teórico %s · fuera de banda: %2d de 24 · var(dy)/var(y) = %.3f · 2(1-r1(y)) = %.3f\n",
              phi, r[1], if (phi <= 1) sprintf("%6.3f", -(1 - phi) / 2) else "   —  ",
              length(fuera(d)), var(d) / var(y), 2 * (1 - acf(y, 1, plot = FALSE)$acf[2])))
}
cat("phi = 1: all.equal(diff(ar1(1, e)), e[-1]) ->", isTRUE(all.equal(diff(ar1(1, e)), e[-1])), "\n")
cat("teórico con ARMAacf: rho1 de (1-B) aplicado a AR(1) phi=0.5 ->",
    round(ARMAacf(ar = 0.5, ma = -1, lag.max = 1)[2], 4), "\n")

cat("\n== E4 · M7: ¿la diferencia de más siempre aumenta la varianza? ==\n")
tabla <- function(x, nombre) for (d in 0:3) {
  y <- if (d == 0) as.numeric(x) else as.numeric(diff(x, differences = d))
  cat(sprintf("%-14s d = %d · n = %3d · var = %14.5f · r1 = %7.4f\n", nombre, d, length(y), var(y),
              acf(y, 1, plot = FALSE)$acf[2]))
}
tabla(lx, "log(AP)"); tabla(trm, "TRM")
cat("ndiffs(log AP) =", ndiffs(lx), "· ndiffs(TRM) =", ndiffs(trm), "\n")
for (phi in c(0.8, 0.9)) {
  y <- ar1(phi, e)
  cat(sprintf("AR(1) phi = %.1f sobre el ruido del M2: ndiffs = %d · kpss p = %.3f · adf p = %.3f\n", phi, ndiffs(y),
              suppressWarnings(kpss.test(y))$p.value, suppressWarnings(adf.test(y))$p.value))
  tabla(y, sprintf("AR(1) %.1f", phi))
  cat(sprintf("   teórico: Var(dy)/Var(y) = 2(1 - phi) = %.2f · rho1(dy) = -(1 - phi)/2 = %.2f\n", 2 * (1 - phi), -(1 - phi) / 2))
}
set.seed(1); ym <- arima.sim(list(ar = 0.8), n = 200)
cat(sprintf("(maestra) arima.sim phi=0.8, set.seed(1): ndiffs = %d · var %.3f -> %.3f · r1(dy) = %.4f\n",
            ndiffs(ym), var(ym), var(diff(ym)), acf(diff(ym), 1, plot = FALSE)$acf[2]))
cat("ruido blanco del M2: var(e) =", round(var(e), 4), "· var(diff e) =", round(var(diff(e)), 4),
    "· r1(diff e) =", round(acf(diff(e), 1, plot = FALSE)$acf[2], 4), "\n")

cat("\n== E5 · M7, recuadro: la serie d12 = diff(log AP, 12) ==\n")
k1 <- suppressWarnings(kpss.test(d12))
cat(sprintf("n = %d · kpss.test: %.4f, l = %d, p = %.4f · ndiffs(d12) = %d · nsdiffs(lx) = %d\n",
            length(d12), k1$statistic, k1$parameter, k1$p.value, ndiffs(d12), nsdiffs(lx)))
cat("trunc(4*(n/100)^0.25) =", trunc(4 * (132 / 100)^0.25), "· trunc(3*sqrt(n)/13) =", trunc(3 * sqrt(132) / 13), "\n")
u <- urca::ur.kpss(d12, type = "mu", use.lag = trunc(3 * sqrt(length(d12)) / 13))
cat(sprintf("ur.kpss con %d rezagos: %.4f · valores críticos:", u@lag, u@teststat)); print(u@cval)
a <- acf(d12, 24, plot = FALSE)$acf[-1]
cat("ACF de d12, r1..r6:", sprintf("%.4f", a[1:6]), "· r12 =", sprintf("%.4f", a[12]), "· banda ±", round(banda(d12), 4),
    "· fuera:", fuera(d12), "\n")
cat(sprintf("var(d12) = %.5f · var(diff(d12)) = %.5f\n", var(d12), var(diff(d12))))
b <- acf(dd, 24, plot = FALSE)$acf[-1]
cat(sprintf("dd = diff(d12): n = %d · r1 = %.4f · r12 = %.4f · banda ±%.4f · fuera: %s · ndiffs = %d · nsdiffs = %d\n",
            length(dd), b[1], b[12], banda(dd), paste(fuera(dd), collapse = " "), ndiffs(dd), nsdiffs(dd)))
cat("all.equal(diff(d12), dd):", isTRUE(all.equal(as.numeric(diff(d12)), as.numeric(dd))), "\n")
kd1 <- suppressWarnings(kpss.test(d1)); c1 <- acf(d1, 24, plot = FALSE)$acf[-1]
cat(sprintf("d1 = diff(lx): kpss p = %.3f · ndiffs = %d · nsdiffs = %d · r1 = %.4f · r12 = %.4f · banda ±%.4f · fuera (%d): %s\n",
            kd1$p.value, ndiffs(d1), nsdiffs(d1), c1[1], c1[12], banda(d1), length(fuera(d1)), paste(fuera(d1), collapse = " ")))
kdd <- suppressWarnings(kpss.test(dd)); cat(sprintf("dd: kpss.test = %.4f, p = %.3f\n", kdd$statistic, kdd$p.value))

cat("\n== Truncamiento: qué pasa ndiffs a ur.kpss y qué usa ur.kpss por defecto ==\n")
cu <- paste(deparse(forecast::ndiffs), collapse = "\n")
cat(regmatches(cu, gregexpr("[^\n]*3 \\* sqrt[^\n]*|[^\n]*ur\\.kpss[^\n]*", cu))[[1]], sep = "\n")
uu <- paste(deparse(urca::ur.kpss), collapse = "\n")
cat(regmatches(uu, gregexpr("[^\n]*n/100[^\n]*", uu))[[1]], sep = "\n")
cat("formals(ur.kpss)$lags:", deparse(formals(urca::ur.kpss)$lags), "\n")

cat("\n== M6 · ADF con tendencia frente a KPSS de nivel y de tendencia ==\n")
for (nm in c("trm", "dtrm")) { x <- if (nm == "trm") trm else diff(trm)
  a <- suppressWarnings(adf.test(x)); kl <- suppressWarnings(kpss.test(x)); kt <- suppressWarnings(kpss.test(x, null = "Trend"))
  cat(sprintf("%-5s n = %d · ADF %.4f (k = %d, p = %.4f) · KPSS nivel %.4f (p = %.4f) · KPSS tendencia %.4f (p = %.4f)\n",
              nm, length(x), a$statistic, a$parameter, a$p.value, kl$statistic, kl$p.value, kt$statistic, kt$p.value)) }
cat("alternativa que declara adf.test:", suppressWarnings(adf.test(trm))$alternative, "\n")
for (k in c(5, 12)) { a <- suppressWarnings(adf.test(AP, k = k)); b2 <- suppressWarnings(adf.test(lx, k = k))
  cat(sprintf("k = %2d · adf.test(AP): %.4f (p = %.4f) · adf.test(log AP): %.4f (p = %.4f)\n", k, a$statistic, a$p.value, b2$statistic, b2$p.value)) }

cat("\n== M8 · Box-Cox ==\n")
cat("BoxCox(c(-2, 4), 0.5) =", round(BoxCox(c(-2, 4), 0.5), 4), "\n")
cat("fabletools::box_cox(c(-2, 4), 0.5) =", round(fabletools::box_cox(c(-2, 4), 0.5), 4), "\n")
lam <- BoxCox.lambda(AP, method = "guerrero"); cat("lambda Guerrero AP =", round(lam, 4), "· TRM =", round(BoxCox.lambda(trm, method = "guerrero"), 4), "\n")
cat("max|InvBoxCox(BoxCox(AP)) - AP| =", signif(max(abs(InvBoxCox(BoxCox(AP, lam), lam) - AP)), 2), "\n")
cat("guer.cv, línea del periodo:", grep("period", deparse(forecast:::guer.cv), value = TRUE), "\n")
cat("formals(guer.cv)$nonseasonal.length =", formals(forecast:::guer.cv)$nonseasonal.length, "\n")
cat("BoxCox.lambda(Nile, method = 'guerrero') =", round(BoxCox.lambda(Nile, method = "guerrero"), 4), "(frequency(Nile) =", frequency(Nile), ")\n")

cat("\n== M9 · ejercicios y quiz ==\n")
cat(sprintf("co2: (max - min)/mean = %.4f · medias anuales: %.2f -> %.2f (%+.1f %%)\n", (max(co2) - min(co2)) / mean(co2),
            mean(window(co2, 1959, c(1959, 12))), mean(window(co2, 1997, c(1997, 12))),
            100 * (mean(window(co2, 1997, c(1997, 12))) / mean(window(co2, 1959, c(1959, 12))) - 1)))
y <- USAccDeaths; cat("USAccDeaths: ndiffs =", ndiffs(y), "· nsdiffs =", nsdiffs(y), "· ndiffs(diff(y, 12)) =", ndiffs(diff(y, lag = 12)), "\n")
cat("TRM congelada, ADF por ventana (p):", sapply(c(2015, 2018, 2020, 2022), function(a)
  sprintf("desde %d: %.3f", a, suppressWarnings(adf.test(window(trm, start = a)))$p.value)), "\n")
cat("quiz P3: d1 fuera de banda:", length(fuera(d1)), "de 24\n")
cat("quiz P2: 1.96/sqrt(144) =", round(1.96 / 12, 4), "· banda con n = 143:", round(banda(d1), 4), "\n")
