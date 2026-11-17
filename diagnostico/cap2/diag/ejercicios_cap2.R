# Diagnóstico cap. 2 · reproducción independiente de los 5 ejercicios y de las
# claves del quiz. Rscript diagnostico/cap2/diag/ejercicios_cap2.R
# No toca el repo: solo imprime. Los datos de la TRM se leen del precálculo
# incrustado en el capítulo (datos_cap2.json, extraído de la línea 4310).
suppressPackageStartupMessages({
  library(forecast); library(tseries); library(urca); library(jsonlite)
  library(fpp3)
})
options(width = 120)
banda <- function(x) 1.96 / sqrt(length(x))
fuera <- function(x, L = 24) { r <- acf(x, lag.max = L, plot = FALSE)$acf[-1]; sum(abs(r) > banda(x)) }
difn  <- function(x, d) if (d == 0) x else diff(x, differences = d)
cat("R:", R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")),
    "| feasts", as.character(packageVersion("feasts")), "\n")

# =========================== E1 · co2 =======================================
cat("\n=== E1 · co2 ===\n")
cat("n =", length(co2), " rango rel =", round((max(co2) - min(co2)) / mean(co2), 4), "\n")
lam <- BoxCox.lambda(co2, method = "guerrero"); cat("lambda Guerrero =", round(lam, 4), "\n")
# Planitud del criterio de Guerrero sobre co2 (¿lambda 'mal identificado'?)
gcv <- function(lam, x) forecast:::guer.cv(lam, x, nonseasonal.length = 2)
for (L in c(-1, -0.5, -0.0343, 0, 0.5, 1, 2)) cat(sprintf("  CV(%.4f) = %.6f\n", L, gcv(L, co2)))
cat("nsdiffs(co2) =", nsdiffs(co2), "  ndiffs(co2) =", ndiffs(co2), "\n")
co2_s <- diff(co2, lag = 12); co2_sd <- diff(co2_s)
cat("ndiffs(co2_s) =", ndiffs(co2_s), "\n")
r <- acf(co2, lag.max = 24, plot = FALSE)$acf[c(2, 13)]; cat("r1, r12 co2 =", round(r, 4), " banda =", round(banda(co2), 4), "\n")
cat("var tras nabla12 por d:", signif(sapply(0:3, function(d) var(difn(co2_s, d))), 4), "\n")
cat("var serie cruda por d (lo que la pista dice NO hacer):", signif(sapply(0:3, function(d) var(difn(co2, d))), 4), "\n")
cat("kpss.test(co2_sd) p =", suppressWarnings(kpss.test(co2_sd)$p.value), "\n")
cat("final: n =", length(co2_sd), " var =", round(var(co2_sd), 4),
    " r1 =", round(acf(co2_sd, plot = FALSE)$acf[2], 4), " fuera =", fuera(co2_sd), "de 24",
    " banda =", round(banda(co2_sd), 4), "\n")
cat("  ¿Y nabla12 sola? fuera =", fuera(co2_s), " r1 =", round(acf(co2_s, plot = FALSE)$acf[2], 4),
    " kpss p =", suppressWarnings(kpss.test(co2_s)$p.value),
    " adf p =", suppressWarnings(adf.test(co2_s)$p.value), "\n")
cat("  urca ur.kpss(co2_s, lags='short') stat =", round(ur.kpss(co2_s, lags = "short")@teststat, 4), "\n")
# PACF: el enunciado la pide; la solución no la usa
pc <- pacf(co2_sd, lag.max = 24, plot = FALSE)$acf
cat("  PACF final, rezagos fuera de banda:", which(abs(pc) > banda(co2_sd)), "\n")
ac <- acf(co2_sd, lag.max = 24, plot = FALSE)$acf[-1]
cat("  ACF final, rezagos fuera de banda:", which(abs(ac) > banda(co2_sd)), " r12 =", round(ac[12], 4), "\n")

# El pipeline del M9 tal cual (el enunciado pide aplicarlo)
preparar <- function(y, m = frequency(y)) {
  lambda <- BoxCox.lambda(y, method = "guerrero")
  w <- if (abs(lambda) < 0.25) log(y) else BoxCox(y, lambda)
  D <- if (m > 1) nsdiffs(w) else 0
  if (D > 0) w <- diff(w, lag = m, differences = D)
  d <- ndiffs(w)
  if (d > 0) w <- diff(w, differences = d)
  list(serie = w, lambda = lambda, d = d, D = D, var_final = var(w),
       kpss_p = suppressWarnings(kpss.test(w)$p.value))
}
res <- preparar(co2)
cat("preparar(co2): transforma con log? ", abs(res$lambda) < 0.25, " d =", res$d, " D =", res$D,
    " var_final =", signif(res$var_final, 4), " kpss_p =", res$kpss_p, "\n")
res_ap <- preparar(AirPassengers)
cat("preparar(AirPassengers): lambda =", round(res_ap$lambda, 4), " -> usa log? ", abs(res_ap$lambda) < 0.25,
    " d =", res_ap$d, " D =", res_ap$D, " var_final =", signif(res_ap$var_final, 3), "\n")
# Herramientas fpp3 (feasts)
tco2 <- as_tsibble(co2)
cat("feasts: unitroot_nsdiffs =", features(tco2, value, unitroot_nsdiffs)$nsdiffs,
    "; ndiffs tras dif. estacional =",
    features(tco2 |> mutate(v = difference(value, 12)), v, unitroot_ndiffs)$ndiffs, "\n")

# =========================== E2 · Monte Carlo ADF ===========================
cat("\n=== E2 · 500 caminatas, adf.test ===\n")
set.seed(2026)
p <- replicate(500, suppressWarnings(adf.test(cumsum(rnorm(100)))$p.value))
cat("rechazo 5% =", 100 * mean(p < 0.05), " 10% =", 100 * mean(p < 0.10), "\n")
set.seed(2026)
p2 <- replicate(500, suppressWarnings(adf.test(rnorm(100))$p.value))
cat("potencia sobre ruido blanco 5% =", 100 * mean(p2 < 0.05), "\n")
cat("error estándar MC con p=0.05, R=500:", round(100 * sqrt(0.05 * 0.95 / 500), 2), "pp\n")
cat("IC95 binomial del 4.6%:", round(100 * binom.test(23, 500)$conf.int, 2), "\n")
# El Monte Carlo del M6 con amplitud 0 (T=144, set.seed(7)) es el mismo experimento
set.seed(7)
p0 <- replicate(500, suppressWarnings(adf.test(ts(cumsum(rnorm(144)), frequency = 12))$p.value))
cat("M6 amplitud 0 reproducido:", 100 * mean(p0 < 0.05), "%\n")
# Sensibilidad a la semilla del 4.6 %
tas <- sapply(1:20, function(s) { set.seed(s); 100 * mean(replicate(500,
  suppressWarnings(adf.test(cumsum(rnorm(100)))$p.value)) < 0.05) })
cat("20 semillas, % rechazo:", range(tas), " media", round(mean(tas), 2), "\n")

# =========================== E3 · USAccDeaths ===============================
cat("\n=== E3 · USAccDeaths ===\n")
y <- USAccDeaths
cat("ndiffs(y) =", ndiffs(y), " nsdiffs(y) =", nsdiffs(y), " ndiffs(diff(y,12)) =", ndiffs(diff(y, lag = 12)), "\n")
resumen <- function(x, nombre) {
  r <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  data.frame(serie = nombre, n = length(x), varianza = round(var(x)),
             r1 = round(r[1], 4), r12 = round(r[12], 4),
             fuera = sum(abs(r) > banda(x)),
             ljung_box_p = signif(Box.test(x, lag = 24, type = "Ljung-Box")$p.value, 4))
}
print(rbind(resumen(y, "original"), resumen(diff(y), "nabla"),
            resumen(diff(y, lag = 12), "nabla12"), resumen(diff(diff(y), lag = 12), "nabla12 nabla")))
# Con 24 rezagos y n = 59, ¿cuántos esperamos fuera por azar?
cat("esperados fuera por azar en 24 rezagos:", 24 * 0.05, "\n")
# ¿Qué dicen las pruebas sobre nabla12 sola?
x12 <- diff(y, lag = 12)
cat("nabla12: kpss p =", suppressWarnings(kpss.test(x12)$p.value), " adf p =", suppressWarnings(adf.test(x12)$p.value),
    " ur.kpss short =", round(ur.kpss(x12, lags = "short")@teststat, 4), "(crit 5% 0.463)\n")
# ¿Qué dice la PACF / el pipeline del M9?
ru <- preparar(USAccDeaths); cat("preparar(USAccDeaths): lambda =", round(ru$lambda, 4), " log?", abs(ru$lambda) < 0.25,
  " d =", ru$d, " D =", ru$D, "\n")

# =========================== E4 · TRM (datos del capítulo) ===================
cat("\n=== E4 · TRM (precálculo incrustado, n = 138) ===\n")
d <- fromJSON("diagnostico/cap2/diag/datos_cap2.json")
trm <- ts(d$series$trm$valores, start = c(2015, 1), frequency = 12)
cat("n =", length(trm), " fin =", tail(d$fechas$trm, 1), "\n")
a <- adf.test(trm); k <- kpss.test(trm)
cat("TRM: ADF", round(a$statistic, 4), "p", round(a$p.value, 4), "| KPSS", round(k$statistic, 4), "p", k$p.value, "\n")
a <- suppressWarnings(adf.test(diff(trm))); k <- suppressWarnings(kpss.test(diff(trm)))
cat("dTRM: ADF", round(a$statistic, 4), "p", round(a$p.value, 4), "| KPSS", round(k$statistic, 4), "p", k$p.value, "\n")
cat("ndiffs(trm) =", ndiffs(trm), "\n")
# ¿Es 'estructural' el veredicto? Sensibilidad del ADF sobre dTRM a la ventana
cat("ADF sobre dTRM según el último mes incluido (ventana desde 2015-01):\n")
for (n in seq(96, 138, by = 6)) {
  x <- diff(window(trm, end = time(trm)[n]))
  cat(sprintf("  n=%3d (hasta %s): ADF p = %.3f  KPSS p = %s\n", n, d$fechas$trm[n],
              suppressWarnings(adf.test(x)$p.value), format(suppressWarnings(kpss.test(x)$p.value))))
}
cat("ADF sobre dTRM según el primer mes (ventana hasta 2026-06):\n")
for (s in c(1, 13, 25, 37, 49)) {
  x <- diff(window(trm, start = time(trm)[s]))
  cat(sprintf("  desde %s (n=%d): ADF p = %.3f\n", d$fechas$trm[s], length(x) + 1, suppressWarnings(adf.test(x)$p.value)))
}

# =========================== E5 · cifras citadas =============================
cat("\n=== E5 · ADF log(AP) k = 5 y k = 12 ===\n")
for (kk in c(5, 12)) { a <- suppressWarnings(adf.test(log(AirPassengers), k = kk)); cat("k =", kk, round(a$statistic, 4), "p", round(a$p.value, 4), "\n") }
cat("adf.test(AirPassengers):", round(suppressWarnings(adf.test(AirPassengers))$statistic, 4), "\n")

# =========================== Quiz ===========================================
cat("\n=== Quiz ===\n")
cat("Q2: 1.96/sqrt(144) =", 1.96 / sqrt(144), " ; 1.96/144 =", 1.96 / 144, "\n")
dl <- diff(log(AirPassengers)); r <- acf(dl, lag.max = 24, plot = FALSE)$acf[-1]
cat("Q3: n =", length(dl), " banda =", round(banda(dl), 4), " r1 =", round(r[1], 4), " r12 =", round(r[12], 4),
    " fuera =", sum(abs(r) > banda(dl)), "de 24: rezagos", which(abs(r) > banda(dl)), "\n")
cat("Q4: var log AP por d:", round(sapply(0:3, function(d) var(difn(log(AirPassengers), d))), 5),
    " r1:", round(sapply(0:3, function(d) acf(difn(log(AirPassengers), d), lag.max = 1, plot = FALSE)$acf[2]), 4), "\n")
set.seed(2026); e <- rnorm(200); cam <- cumsum(e); rc <- acf(cam, lag.max = 24, plot = FALSE)$acf[-1]
cat("Q6: caminata r1 =", round(rc[1], 4), " r12 =", round(rc[12], 4), " min =", round(min(cam), 2), " 0.5^12 =", 0.5^12, "\n")
cat("Q7: 144 - 1 - 12 =", length(diff(diff(AirPassengers), lag = 12)), "\n")
cv1 <- gcv(1, AirPassengers); cv0 <- gcv(0, AirPassengers); lo <- BoxCox.lambda(AirPassengers, method = "guerrero"); cvo <- gcv(lo, AirPassengers)
cat("Q8: lambda =", round(lo, 4), " CV(1) =", round(cv1, 5), " CV(0) =", round(cv0, 5), " CV(opt) =", round(cvo, 5),
    " exceso log =", round(100 * (cv0 / cvo - 1), 1), "% mejora captada =", round(100 * (cv1 - cv0) / (cv1 - cvo), 1), "%\n")
