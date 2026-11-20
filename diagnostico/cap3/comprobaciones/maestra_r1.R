# Capítulo 3 · R1 · cifras de las correcciones de la sesión maestra tras la verificación (2026-11-20)
# 1. Ejercicio 3: cuántas ventanas de cien años rechazan Ljung-Box (lag 12, fitdf 2), y cuántas de ellas acaban antes de 1900
ini <- 1700:1889
p <- sapply(ini, function(a) {
  x <- sqrt(window(sunspot.year, a, a + 99))
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value })
cat("ventanas:", length(ini), "| rechazan:", sum(p < 0.05), "| no rechazan:", sum(p >= 0.05), "\n")
cat("acaban antes de 1900:", sum(ini + 99 < 1900), "| de ellas rechazan:", sum(p < 0.05 & ini + 99 < 1900), "\n")
cat("llegan a 1900 o despues:", sum(ini + 99 >= 1900), "| rechazan:", sum(p < 0.05 & ini + 99 >= 1900), "\n")
# 2. CSS frente a ML con T = 40 y phi = 0.95, mil réplicas por semilla, doce semillas
r <- t(sapply(1:12, function(s) {
  set.seed(s)
  rr <- replicate(1000, {
    z <- arima.sim(list(ar = 0.95), n = 40)
    c(css = tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "CSS"))[[1]], error = function(e) NA),
      ml  = tryCatch(coef(arima(z, order = c(1, 0, 0), include.mean = FALSE, method = "ML"))[[1]],  error = function(e) NA))
  })
  c(css_mayor_1 = 100 * mean(rr["css", ] > 1, na.rm = TRUE), ml_999 = 100 * mean(rr["ml", ] >= 0.999, na.rm = TRUE),
    ml_falla = sum(is.na(rr["ml", ])))
}))
print(round(r, 1))
cat("CSS > 1: de", min(r[, 1]), "a", max(r[, 1]), "% | ML >= 0.999: de", min(r[, 2]), "a", max(r[, 2]),
    "% | ML sin estimacion: de", min(r[, 3]), "a", max(r[, 3]), "por mil\n")
