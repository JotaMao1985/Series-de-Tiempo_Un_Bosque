# Verificador B · R4 del capítulo 3 · repetición independiente de las `propia`
# (y de las cifras de software) de los módulos 7-10. Solo calcula; no escribe
# nada fuera de su salida. Uso:
#   Rscript diagnostico/cap3/comprobaciones/v4B_software.R > .../v4B_software.out 2>&1
suppressPackageStartupMessages(library(forecast))
cat(R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n\n")
manchas <- window(sunspot.year, start = 1770, end = 1869)

cat("== c3-m7-11 · CSS y ML con T = 40, phi = 0.95, set.seed(1)\n")
set.seed(1); z <- arima.sim(list(ar = 0.95), n = 40)
print(round(c(css = coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS"))[[1]],
              ml  = coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML"))[[1]]), 4))

cat("\n== c3-m7-11 / c3-m7-33 / c3-m7-34 · 12 semillas x 1000 réplicas\n")
una <- function() {
  z <- arima.sim(list(ar = 0.95), n = 40)
  css <- tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS"))[[1]], error = function(e) NA)
  ml  <- tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML"))[[1]], error = function(e) NA)
  c(css = css, ml = ml)
}
tab <- t(sapply(1:12, function(s) {
  set.seed(s); r <- replicate(1000, suppressWarnings(una()))
  c(semilla = s, css_mayor_1 = 100 * mean(r["css", ] > 1, na.rm = TRUE),
    ml_mayor_1 = 100 * mean(r["ml", ] > 1, na.rm = TRUE),
    ml_999 = 100 * mean(r["ml", ] >= 0.999, na.rm = TRUE),
    ml_na_por_mil = sum(is.na(r["ml", ])))
}))
print(round(tab, 2))
cat("rangos: CSS>1", range(tab[, 2]), "| ML>1", range(tab[, 3]), "| ML>=0.999", round(range(tab[, 4]), 2),
    "| ML sin estimación (por mil)", range(tab[, 5]), "\n")

cat("\n== c3-m7-13 · sesgo de Yule-Walker hacia el interior (AR(2) de las manchas, T = 100, 1000 réplicas)\n")
set.seed(2027); phi <- c(1.4059, -0.7111)
res <- replicate(1000, {
  y <- arima.sim(list(ar = phi), n = 100)
  yw <- ar(y, order.max = 2, aic = FALSE, method = "yule-walker")$ar
  ml <- tryCatch(coef(arima(y, order = c(2, 0, 0), method = "ML"))[1:2], error = function(e) c(NA, NA))
  c(yw, ml, min(Mod(polyroot(c(1, -yw)))), min(Mod(polyroot(c(1, -ml)))))
})
cat("media YW:", round(rowMeans(res[1:2, ]), 4), "| media ML:", round(rowMeans(res[3:4, ], na.rm = TRUE), 4),
    "| módulo medio YW:", round(mean(res[5, ]), 4), "ML:", round(mean(res[6, ], na.rm = TRUE), 4),
    "verdadero:", round(min(Mod(polyroot(c(1, -phi)))), 4), "\n")
set.seed(2028)
cat("AR(1) phi = 0.95, T = 100: media YW =",
    round(mean(replicate(1000, ar(arima.sim(list(ar = .95), n = 100), order.max = 1, aic = FALSE, method = "yule-walker")$ar)), 3), "\n")

cat("\n== c3-m7-17 (lado R) · ar() usa divisor n\n")
print(round(ar(manchas, order.max = 2, aic = FALSE, method = "yule-walker")$ar, 4))

cat("\n== c3-m8-24 · logLik de modelos anidados (ML)\n")
ll <- sapply(list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2)),
             function(pq) c(p = pq[1], q = pq[2], ll = as.numeric(logLik(arima(manchas, order = c(pq[1], 0, pq[2]), method = "ML")))))
print(round(t(ll), 3))

cat("\n== c3-m8-15 / c3-m8-35 · Ljung-Box con y sin fitdf (set.seed(8), 3000 AR(2), T = 100, h = 12)\n")
set.seed(8)
p <- replicate(3000, {
  y <- arima.sim(list(ar = c(1.4, -0.7)), n = 100)
  e <- residuals(suppressWarnings(arima(y, order = c(2, 0, 0), method = "ML")))
  c(sin = Box.test(e, lag = 12, type = "Ljung-Box")$p.value,
    con = Box.test(e, lag = 12, type = "Ljung-Box", fitdf = 2)$p.value)
})
rr <- rowMeans(p < 0.05); print(round(rr, 4)); cat("cociente sin/con:", round(rr[1] / rr[2], 3), "\n")

cat("\n== c3-m8-11 · Var(r_k) de ruido blanco, T = 50, 20000 series\n")
set.seed(5); Tn <- 50; ks <- c(1, 2, 5, 10, 20)
R <- replicate(20000, acf(rnorm(Tn), lag.max = 20, plot = FALSE)$acf[-1][ks])
print(rbind(simulada = round(apply(R, 1, var), 5), formula = round((Tn - ks) / (Tn * (Tn + 2)), 5), uno_T = 1 / Tn))

cat("\n== c3-m8-18 · residuales de R (estandarizados) frente a la innovación cruda\n")
ml2 <- arima(manchas, order = c(2, 0, 0), method = "ML")
ph <- coef(ml2)[1:2]
g0s2 <- 1 / (1 - sum(ph * ARMAacf(ar = ph, lag.max = 2)[2:3]))
rho1 <- ARMAacf(ar = ph, lag.max = 1)[2]
cat("residuals[1:4]:", round(residuals(ml2)[1:4], 3), "| gamma0/sigma2 =", round(g0s2, 3),
    "raíz", round(sqrt(g0s2), 3), "| factor 2.º:", round(sqrt(g0s2 * (1 - rho1^2)), 3), "\n")
cat("21.056 * raíz =", round(residuals(ml2)[1] * sqrt(g0s2), 3), "\n")
cat("Ljung-Box AR(2) crudo, lag 12: con fitdf=2", round(Box.test(residuals(ml2), 12, "Ljung-Box", fitdf = 2)$p.value, 4),
    "| sin fitdf", round(Box.test(residuals(ml2), 12, "Ljung-Box")$p.value, 4), "  (c3-m10-14)\n")
cat("sin los 2 primeros residuales, fitdf=2:", round(Box.test(residuals(ml2)[-(1:2)], 12, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")

cat("\n== c3-m9-05 / c3-m9-43 · Guerrero\n")
cat("min(manchas) =", min(manchas), "| ceros 1770-1869:", sum(manchas == 0), "| ceros 1700-1988:", sum(sunspot.year == 0), "\n")
w <- NULL
l0 <- withCallingHandlers(BoxCox.lambda(manchas, method = "guerrero"), warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") })
cat("sin desplazar:", round(l0, 4), "| aviso:", w, "\n")
cat("manchas + 1:", round(BoxCox.lambda(manchas + 1, method = "guerrero"), 4), "\n")
cat("guer.cv usa nonseasonal.length:\n"); print(formals(forecast:::guer.cv)); print(body(forecast:::guer.cv)[2:4])
cat("BoxCox.lambda: lower por defecto", deparse(formals(BoxCox.lambda)$lower), "\n")

cat("\n== c3-m9-08 / c3-m9-47 · AR(2) sobre raíz y sobre la potencia de Guerrero\n")
ajusta <- function(x) { f <- arima(x, order = c(2, 0, 0), method = "ML")
  c(periodo = 2 * pi / Arg(polyroot(c(1, -coef(f)[1:2]))[1]), LB12 = Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value) }
lam <- BoxCox.lambda(manchas + 1, method = "guerrero")
print(round(rbind(raiz = ajusta(sqrt(manchas)), guerrero = ajusta(manchas^lam), desplazada = ajusta((manchas + 1)^lam)), 4))
ar2s <- arima(sqrt(manchas), order = c(2, 0, 0), method = "ML")
ps <- c(1, ARMAtoMA(ar = coef(ar2s)[1:2], lag.max = 500))
cat("phi =", round(coef(ar2s)[1:2], 4), "sigma2 =", round(ar2s$sigma2, 4), "| suma psi^2 =", round(sum(ps^2), 3),
    "| sigma2*suma =", round(ar2s$sigma2 * sum(ps^2), 3), "| var muestral sqrt =", round(var(sqrt(manchas)), 3),
    "| semiancho límite =", round(1.96 * sqrt(ar2s$sigma2 * sum(ps^2)), 2), "\n")

cat("\n== c3-m9-45 · pico espectral del AR(2) frente al ángulo de la raíz\n")
ph <- c(1.4027, -0.6853)
den <- function(w, ph) Mod(1 - ph[1] * exp(-1i * w) - ph[2] * exp(-2i * w))^2
pico <- function(ph) 2 * pi / optimize(function(w) den(w, ph), c(1e-4, pi))$minimum
ang <- function(ph) 2 * pi / abs(Arg(polyroot(c(1, -ph))[1]))
cat("pico:", round(pico(ph), 4), "| fórmula FPP3:", round(2 * pi / acos(-ph[1] * (1 - ph[2]) / (4 * ph[2])), 4),
    "| ángulo:", round(ang(ph), 4), "\n")
om <- abs(Arg(polyroot(c(1, -ph))[1]))
for (R in c(0.828, 0.95, 0.99, 0.999)) { p2 <- c(2 * R * cos(om), -R^2); cat("R =", R, "pico", round(pico(p2), 4), "ángulo", round(ang(p2), 4), "\n") }

cat("\n== c3-m9-50 · rho_1 inducido por promediar una caminata (m días por mes)\n")
rho1m <- function(m) { c <- c(1:m, (m - 1):1) / m; sum(c[1:(m - 1)] * c[(m + 1):(2 * m - 1)]) / sum(c^2) }
for (m in c(2, 5, 20, 21, 30)) cat("m =", m, "suma de pesos", round(rho1m(m), 4), "forma cerrada", round((m^2 - 1) / (2 * (2 * m^2 + 1)), 4), "\n")
set.seed(31); r1 <- replicate(2000, { d <- cumsum(rnorm(138 * 21)); y <- colMeans(matrix(d, 21)); acf(diff(y), plot = FALSE)$acf[2] })
cat("simulación (2000 caminatas, 138 meses de 21 días): media r1 =", round(mean(r1), 3), "\n")

cat("\n== c3-m9-20 / c3-m9-52 / c3-m9-24 · auto.arima sobre los log-retornos de la TRM\n")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
ret <- diff(log(trm)) * 100
cat("n =", length(ret), "frecuencia =", frequency(ret), "\n")
cat("formals ic:", deparse(formals(auto.arima)$ic), "| stepwise:", deparse(formals(auto.arima)$stepwise),
    "| approximation:", deparse(formals(auto.arima)$approximation), "\n")
a1 <- auto.arima(ret); a2 <- auto.arima(ret, stepwise = FALSE); a3 <- auto.arima(ret, stepwise = FALSE, approximation = FALSE)
for (a in list(a1, a2, a3)) cat(as.character(a), " AICc =", round(a$aicc, 3), " coef:", round(coef(a), 4), "\n")
a4 <- Arima(ret, order = c(0, 0, 0), include.mean = TRUE); a5 <- Arima(ret, order = c(0, 0, 1), include.mean = TRUE)
cat("WN con media AICc", round(a4$aicc, 3), "| MA(1) con media AICc", round(a5$aicc, 3), "media", round(coef(a5)["intercept"], 4),
    "ee", round(sqrt(diag(a5$var.coef))["intercept"], 4), "\n")
cat("LB r_t lag 6/12/20:", round(sapply(c(6, 12, 20), function(h) Box.test(ret, h, "Ljung-Box")$p.value), 4),
    "| LB r_t^2 lag 12:", round(Box.test(ret^2, 12, "Ljung-Box")$p.value, 4), "| r1 =", round(acf(ret, plot = FALSE)$acf[2], 3), "\n")

cat("\n== c3-m10-28 · ARMA(2,2) con factor común frente a ARMA(1,1)\n")
cat("max |dif ACF| =", max(abs(ARMAacf(ar = c(1.1, -0.28), ma = c(0.1, -0.20), lag.max = 15) - ARMAacf(ar = 0.7, ma = 0.5, lag.max = 15))), "\n")
cat("raíces AR:", round(Mod(polyroot(c(1, -1.1, 0.28))), 4), "| raíces MA:", round(Re(polyroot(c(1, 0.1, -0.2))), 4), "\n")
cat("c3-m10-24 · PACF ARMA(1,2):", round(ARMAacf(ar = 0.3, ma = c(0.6, 0.4), lag.max = 6, pacf = TRUE), 3), "\n")

cat("\n== c3-m10-35 · 190 ventanas de cien años, AR(2) sobre la raíz, LB(12) con fitdf = 2\n")
ini <- 1700:1889
pv <- sapply(ini, function(a) { x <- sqrt(window(sunspot.year, a, a + 99)); f <- arima(x, order = c(2, 0, 0), method = "ML")
  Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value })
cat("ventanas:", length(ini), "| pasan:", sum(pv >= 0.05), "| fallan:", sum(pv < 0.05),
    "| fallan y acaban antes de 1900:", sum(pv < 0.05 & ini + 99 < 1900),
    "| inicios que pasan:", paste(range(ini[pv >= 0.05]), collapse = "-"), "fuera de 1734-1785:",
    paste(setdiff(ini[pv >= 0.05], 1734:1785), collapse = ","), "| llegan a 1900 y pasan:", sum(pv >= 0.05 & ini + 99 >= 1900), "\n")
for (v in list(c(1770, 1869), c(1870, 1988), c(1900, 1988), c(1889, 1988), c(1700, 1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2])); f <- arima(x, order = c(2, 0, 0), method = "ML")
  cat(v[1], "-", v[2], "p =", signif(Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value, 3),
      "periodo", round(2 * pi / Arg(polyroot(c(1, -coef(f)[1:2]))[1]), 3), "\n") }

cat("\n== c3-m10-25 · t de los coeficientes\n")
cat("AR(2) raíz:", round(coef(ar2s)[1:2] / sqrt(diag(ar2s$var.coef))[1:2], 2))
a21 <- arima(manchas, order = c(2, 0, 1), method = "ML")
cat(" | ARMA(2,1) crudo theta:", round(coef(a21)[3], 4), "t =", round(coef(a21)[3] / sqrt(diag(a21$var.coef))[3], 2), "\n")
