# R5 del capitulo 2 · exploracion previa: que series sirven para cada hueco.
# Rscript diagnostico/cap2/comprobaciones/r5_explora.R > diagnostico/cap2/comprobaciones/r5_explora.out 2>&1
suppressPackageStartupMessages({library(forecast); library(tseries)})
options(warn = 1, width = 120)
banda <- function(x) 1.96 / sqrt(length(x))
fuera <- function(x, L = 24, f = acf) { r <- f(x, lag.max = L, plot = FALSE)$acf; if (identical(f, acf)) r <- r[-1]; which(abs(r) > banda(x)) }

cat("== M3: discoveries ==\n")
print(head(discoveries, 12)); print(start(discoveries))

cat("\n== M4: lh ==\n")
print(length(lh)); print(round(banda(lh), 3))
print(round(acf(lh, lag.max = 16, plot = FALSE)$acf[2:9], 3))
print(round(pacf(lh, lag.max = 16, plot = FALSE)$acf[1:8], 3))
cat("ACF fuera:", fuera(lh, 16), " PACF fuera:", fuera(lh, 16, pacf), "\n")
for (s in 1:12) { set.seed(s); x <- arima.sim(list(ma = 0.8), n = 200)
  cat("ma seed", s, "ACF fuera:", fuera(x, 24), "| PACF fuera:", fuera(x, 24, pacf), "| r:", round(acf(x, plot = FALSE)$acf[2:4], 3), "| p:", round(pacf(x, plot = FALSE)$acf[1:6], 3), "\n") }

cat("\n== M6: WWWusage, LakeHuron, Nile, otras ==\n")
pr <- function(x, nombre) {
  a <- suppressWarnings(adf.test(x)); kl <- suppressWarnings(kpss.test(x)); kt <- suppressWarnings(kpss.test(x, null = "Trend"))
  cat(sprintf("%-22s n=%3d ADF %.3f p=%.4f (k=%d) | KPSS L %.3f p=%.4f | KPSS T %.3f p=%.4f | ndiffs %d\n", nombre, length(x),
      a$statistic, a$p.value, a$parameter, kl$statistic, kl$p.value, kt$statistic, kt$p.value, ndiffs(x)))
}
for (nm in c("WWWusage", "LakeHuron", "Nile", "lh", "lynx", "BJsales", "uspop", "airmiles", "austres", "precip", "treering", "sunspot.year", "nhtemp", "discoveries", "JohnsonJohnson")) {
  x <- tryCatch(get(nm), error = function(e) NULL); if (is.null(x) || !is.ts(x) || is.matrix(x)) next
  x <- na.omit(x)
  pr(x, nm); pr(diff(x), paste0("  diff(", nm, ")"))
}

cat("\n== M8: criterio de Guerrero en varias series ==\n")
guerrero <- function(y, lambda, m = frequency(y)) {
  n <- m * (length(y) %/% m)
  b <- matrix(tail(as.numeric(y), n), nrow = m)
  medias <- colMeans(b); desv <- apply(b, 2, sd)
  coc <- desv / medias^(1 - lambda)
  sd(coc) / mean(coc)
}
cat("AP:", round(sapply(c(1, 0, BoxCox.lambda(AirPassengers, "guerrero")), function(l) guerrero(AirPassengers, l)), 4), "\n")
cat("AP interno:", round(sapply(c(1, 0, -0.2947), function(l) forecast:::guer.cv(l, AirPassengers)), 4), "\n")
for (nm in c("UKgas", "JohnsonJohnson", "USAccDeaths", "ldeaths", "mdeaths", "UKDriverDeaths", "co2", "nottem", "sunspot.year", "lynx", "austres", "airmiles", "uspop", "BJsales", "WWWusage", "LakeHuron", "Nile", "wineind", "gas", "woolyrnq")) {
  x <- tryCatch(get(nm), error = function(e) NULL); if (is.null(x) || frequency(x) > 12) next
  x <- na.omit(x)
  if (min(x) <= 0) { cat(nm, "tiene ceros o negativos\n"); next }
  l <- suppressWarnings(BoxCox.lambda(x, method = "guerrero"))
  v <- sapply(c(1, 0.5, 0, l), function(z) forecast:::guer.cv(z, x))
  cat(sprintf("%-15s m=%2.0f n=%4.0f lambda=%7.4f | CV(1)=%.4f CV(.5)=%.4f CV(0)=%.4f CV(opt)=%.4f | log capta %.1f%% | max/min=%.2f\n",
              nm, frequency(x), length(x), l, v[1], v[2], v[3], v[4], 100 * (v[1] - v[3]) / (v[1] - v[4]), max(x) / min(x)))
}

cat("\n== E5: series estacionales donde el ADF por defecto rechaza y con k = 12 no ==\n")
for (nm in c("nottem", "UKDriverDeaths", "ldeaths", "USAccDeaths", "co2", "UKgas")) {
  x <- get(nm); m <- frequency(x)
  a <- suppressWarnings(adf.test(x)); b <- suppressWarnings(adf.test(x, k = m)); kk <- suppressWarnings(kpss.test(x))
  cat(sprintf("%-15s n=%3d k=%d ADF %.3f p=%.3f | k=%d ADF %.3f p=%.3f | KPSS L p=%.3f | nsdiffs %d ndiffs(dm) %d\n", nm, length(x), a$parameter, a$statistic, a$p.value, m, b$statistic, b$p.value, kk$p.value, nsdiffs(x), ndiffs(diff(x, lag = m))))
}

cat("\n== M4: AR(2) simulado, semillas ==\n")
for (s in 1:15) { set.seed(s); x <- arima.sim(list(ar = c(0.5, 0.3)), n = 200)
  cat("ar2 seed", s, "ACF fuera:", fuera(x, 24), "| PACF fuera:", fuera(x, 24, pacf), "| r:", round(acf(x, plot = FALSE)$acf[2:6], 3), "| p:", round(pacf(x, plot = FALSE)$acf[1:4], 3), "\n") }

cat("\n== M6: nhtemp con detalle ==\n")
print(tsp(nhtemp)); print(range(nhtemp))
for (k in 0:6) { a <- suppressWarnings(adf.test(nhtemp, k = k)); cat("k =", k, "ADF", round(a$statistic, 3), "p", round(a$p.value, 4), "\n") }
res <- residuals(lm(nhtemp ~ time(nhtemp))); print(round(coef(lm(nhtemp ~ time(nhtemp))), 4))
cat("residuo de la recta: fuera", fuera(res, 15), "r1", round(acf(res, plot = FALSE)$acf[2], 3), "banda", round(banda(res), 3), "\n")
cat("nhtemp: fuera", fuera(nhtemp, 15), "r1..4", round(acf(nhtemp, plot = FALSE)$acf[2:5], 3), "\n")
cat("diff: fuera", fuera(diff(nhtemp), 15), "r1", round(acf(diff(nhtemp), plot = FALSE)$acf[2], 3), "\n")
print(suppressWarnings(kpss.test(res))); 

cat("\n== M2: DAX ==\n")
dax <- EuStockMarkets[, "DAX"]; r <- diff(log(dax)); print(length(r)); print(round(banda(r), 4))
cat("rend fuera:", fuera(r), "| cuadrados fuera:", fuera(r^2), "| abs fuera:", length(fuera(abs(r))), "\n")
print(round(acf(r, lag.max = 24, plot = FALSE)$acf[2:6], 3)); print(round(acf(r^2, lag.max = 24, plot = FALSE)$acf[2:6], 3))
for (s in c(1, 2, 3, 2026)) { set.seed(s); b <- sample(r); cat("seed", s, "barajada: rend fuera", length(fuera(b)), "cuadrados fuera", length(fuera(b^2)), "\n") }
for (nm in colnames(EuStockMarkets)) { z <- diff(log(EuStockMarkets[, nm])); cat(nm, "rend fuera", length(fuera(z)), "cuad fuera", length(fuera(z^2)), "\n") }

cat("\n== M5: recta con ruido frente a caminata con deriva ==\n")
for (s in c(5, 8, 10, 11, 12, 20, 21, 30)) { set.seed(s); e <- rnorm(200); t <- 1:200
  A <- 0.3 * t + e; B <- cumsum(0.3 + e)
  f <- function(x) c(r1 = round(acf(x, plot = FALSE)$acf[2], 3), fuera = length(fuera(x)))
  cat("seed", s, "| A sin recta", f(residuals(lm(A ~ t))), "| A dif", f(diff(A)), "| B sin recta", f(residuals(lm(B ~ t))), "| B dif", f(diff(B)),
      "| pend A", round(coef(lm(A ~ t))[2], 3), "pend B", round(coef(lm(B ~ t))[2], 3), "media dif B", round(mean(diff(B)), 3), "\n") }

cat("\n== M8/Q8: JohnsonJohnson y UKgas ==\n")
jj <- JohnsonJohnson; print(tsp(jj)); print(window(jj, start = c(1980, 1)))
l <- BoxCox.lambda(jj, "guerrero")
cat("1980: media", mean(window(jj, start = 1980)), "| vuelta log", exp(mean(log(window(jj, start = 1980)))), "| vuelta opt", InvBoxCox(mean(BoxCox(window(jj, start = 1980), l)), l), "\n")
cat("toda: media", mean(jj), "| vuelta log", exp(mean(log(jj))), "| mediana", median(jj), "\n")
for (nm in c("UKgas", "JohnsonJohnson", "AirPassengers")) { x <- get(nm); m <- frequency(x)
  b <- matrix(log(as.numeric(x))[1:(m * (length(x) %/% m))], nrow = m)
  cat(nm, "en log: cor(media, sd) por bloque", round(cor(colMeans(b), apply(b, 2, sd)), 3), "| sd primeros 3 y ultimos 3 bloques:", round(apply(b, 2, sd)[c(1:3, ncol(b) - 2:0)], 3), "\n") }

cat("\n== M3: ventanas de discoveries con media entera o .5 y |r1| > 0.35 ==\n")
d <- as.numeric(discoveries)
for (L in c(8, 10)) for (i in 1:(100 - L + 1)) { x <- d[i:(i + L - 1)]; m <- mean(x)
  if (abs(2 * m - round(2 * m)) < 1e-9) { r <- acf(x, plot = FALSE)$acf[2:3]
    if (abs(r[1]) > 0.35) cat(L, "valores desde", 1859 + i, ":", x, "| media", m, "| r1 r2", round(r, 3), "\n") } }

cat("\n== M5: la misma busqueda de semilla con pendiente 0.2 (la elegida: 37) ==\n")
for (s in 31:45) { set.seed(s); e <- rnorm(200); t <- 1:200; A <- 0.2 * t + e; B <- cumsum(0.2 + e)
  f <- function(x) c(round(acf(x, plot = FALSE)$acf[2], 3), length(fuera(x)))
  cat("seed", s, "| A sin recta", f(residuals(lm(A ~ t))), "| A dif", f(diff(A)), "| B sin recta", f(residuals(lm(B ~ t))), "| B dif", f(diff(B)),
      "| pend B", round(coef(lm(B ~ t))[2], 3), "media dif B", round(mean(diff(B)), 3), "| max dist A", round(max(abs(A - 0.2 * t)), 1), "B", round(max(abs(B - 0.2 * t)), 1), "\n") }

cat("\n== M4: series reales para la lectura de la PACF (lh se descarta: es el ejercicio 1 del cap. 3) ==\n")
f4 <- function(x, L, nm) { b <- banda(x); a <- acf(x, lag.max = L, plot = FALSE)$acf[-1]; p <- pacf(x, lag.max = L, plot = FALSE)$acf
  cat(sprintf("%-22s n=%4d banda %.3f | ACF fuera: %s | PACF fuera: %s\n", nm, length(x), b, toString(which(abs(a) > b)), toString(which(abs(p) > b)))) }
f4(LakeHuron, 20, "LakeHuron"); f4(residuals(lm(LakeHuron ~ time(LakeHuron))), 20, "LakeHuron sin recta"); f4(log(lynx), 20, "log(lynx)"); f4(Nile, 20, "Nile"); f4(diff(WWWusage), 20, "diff(WWWusage)"); f4(diff(BJsales), 20, "diff(BJsales)")
