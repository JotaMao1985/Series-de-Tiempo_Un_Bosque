# R2 del cap. 5 · las cifras que la ronda hace aparecer, recalculadas en R aparte de la página.
# La página las calcula en JS desde DATOS_CAP5 / SERIES_CAP5 (salen de precalculo/genera_cap5.R);
# aquí se rehacen desde datasets::AirPassengers y la copia fija de la TRM del curso.
# Uso: Rscript diagnostico/cap5/comprobaciones/r2_cifras.R > diagnostico/cap5/comprobaciones/r2_cifras.out
suppressPackageStartupMessages({ library(forecast); library(jsonlite) })
cat("R", R.version$major, ".", R.version$minor, " · forecast ", as.character(packageVersion("forecast")), "\n\n", sep = "")
raiz <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))), "..", "..", ".."))
ap <- log(AirPassengers)
trm_csv <- read.csv(file.path(raiz, "Htmls_Series", "datos", "trm_mensual_2015-01_2026-06.csv"))
trm <- ts(trm_csv$trm, start = c(2015, 1), frequency = 12)
J <- fromJSON(file.path(raiz, "precalculo", "salidas", "cap5_sarima.json"), simplifyVector = TRUE)
fuera <- function(x, lag.max = 36) {
  r <- acf(x, lag.max = lag.max, plot = FALSE)$acf[-1]; b <- 1.96 / sqrt(length(x))
  k <- which(abs(r) > b)
  list(r = r, b = b, est = k[k %% 12 == 0], otros = k[k %% 12 != 0])
}

cat("== 1. M6 · tabla: fila (0,1,0)(0,1,0)[12] sobre log(AirPassengers) ==\n")
m0 <- Arima(ap, order = c(0, 1, 0), seasonal = list(order = c(0, 1, 0), period = 12))
# Misma convención que las otras filas de la tabla y que el explorador: los 144 residuales
# (la fila del airline da -0.0515 así; sin los 13 de arranque daría -0.0434).
r0 <- acf(residuals(m0), lag.max = 24, plot = FALSE)$acf[-1]
r0b <- acf(residuals(m0)[-(1:13)], lag.max = 24, plot = FALSE)$acf[-1]
ra <- acf(residuals(Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))),
          lag.max = 24, plot = FALSE)$acf[-1]
cat(sprintf("AICc %.2f  BIC %.2f (tabla: -431.95)  rho12 residual %.4f (tabla: -0.3907; sin los 13 de arranque, %.4f) · airline, misma convención: %.4f (tabla: -0.0515)\n",
            m0$aicc, m0$bic, r0[12], r0b[12], ra[12]))
cat(sprintf("JSON: aicc %.3f bic %.4f acf12 %.4f\n\n", J$airpassengers$rejilla[["(0,1,0)(0,1,0)[12]"]]$aicc,
            J$airpassengers$rejilla[["(0,1,0)(0,1,0)[12]"]]$bic, J$airpassengers$rejilla[["(0,1,0)(0,1,0)[12]"]]$acf12))

cat("== 2. M7 · intro: el abanico en logaritmos, ancho del IC 95 % por horizonte ==\n")
al <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
f <- forecast(al, h = 24, level = 95)
ancho <- as.numeric(f$upper - f$lower)
inc <- c(NA, diff(ancho))
print(data.frame(h = 1:24, ancho = round(ancho, 4), incremento = round(inc, 4)), row.names = FALSE)
cat(sprintf("incremento en h = 13: %.4f; mayor incremento de h = 2..24 en h = %d; incremento medio de h = 2..12: %.4f, de h = 14..24: %.4f\n",
            inc[13], which.max(inc), mean(inc[2:12]), mean(inc[14:24])))
cat(sprintf("JSON (log): ancho en h = 12, 13: %.4f, %.4f\n\n",
            J$airpassengers$pronostico$log$hi95[12] - J$airpassengers$pronostico$log$lo95[12],
            J$airpassengers$pronostico$log$hi95[13] - J$airpassengers$pronostico$log$lo95[13]))

cat("== 3. M9 · Domingo de Pascua 1949–1960 (algoritmo gregoriano anónimo) ==\n")
pascua <- function(y) {
  a <- y %% 19; b <- y %/% 100; c <- y %% 100; d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25
  g <- (b - f + 1) %/% 3; h <- (19 * a + b - d - g + 15) %% 30; i <- c %/% 4; k <- c %% 4
  l <- (32 + 2 * e + 2 * i - h - k) %% 7; m <- (a + 11 * h + 22 * l) %/% 451
  mes <- (h + l - 7 * m + 114) %/% 31; dia <- ((h + l - 7 * m + 114) %% 31) + 1
  sprintf("%d-%02d-%02d", y, mes, dia)
}
p <- sapply(1949:1960, pascua)
print(p)
cat(sprintf("años con Pascua en marzo: %d de %d (JSON meses_pascua_marzo: %d); coincide con el JSON: %s\n\n",
            sum(substr(p, 6, 7) == "03"), length(p), J$airpassengers$calendario$meses_pascua_marzo,
            identical(unname(unlist(J$airpassengers$calendario$pascuas)), unname(p))))

cat("== 4. Quiz, pregunta 5 · ACF teórica de un SAR(1)_12 con Phi = 0.7 ==\n")
r <- ARMAacf(ar = c(rep(0, 11), 0.7), lag.max = 36)[-1]
nz <- which(abs(r) >= 0.005)
cat("rezagos no nulos:", nz, " valores:", sprintf("%.2f", r[nz]), " · los demás:", 36 - length(nz),
    "con máximo |valor|", max(abs(r[-nz])), "\n\n")

cat("== 5. M1 y M8 · barras fuera de banda (las lecturas nuevas) ==\n")
casos <- list(
  "log AP, ∇∇₁₂" = diff(diff(ap, lag = 12)),
  "log AP, ∇ (M8)" = diff(ap),
  "TRM sin log, ∇ (M1, última fila de la tabla; M8)" = diff(trm),
  "TRM sin log, ∇₁₂" = diff(trm, lag = 12),
  "TRM log, ∇₁₂" = diff(log(trm), lag = 12),
  "TRM sin log, ∇∇₁₂" = diff(diff(trm, lag = 12)))
for (nm in names(casos)) {
  z <- fuera(casos[[nm]])
  cat(sprintf("%-48s n = %3d banda %.4f · rho1 %.4f rho12 %.4f rho24 %.4f rho36 %.4f · múltiplos de 12 fuera: %s · otros: %s\n",
              nm, length(casos[[nm]]), z$b, z$r[1], z$r[12], z$r[24], z$r[36],
              if (length(z$est)) paste(z$est, collapse = ", ") else "ninguno",
              if (length(z$otros)) paste(z$otros, collapse = ", ") else "ninguno"))
}
cat("\n")

cat("== 6. M2 · constructor con todos los órdenes en 2 (coeficientes de ejemplo de la página) ==\n")
mult <- function(a, b) { r <- rep(0, length(a) + length(b) - 1)
  for (i in seq_along(a)) for (j in seq_along(b)) r[i + j - 1] <- r[i + j - 1] + a[i] * b[j]; r }
est <- function(c) { v <- rep(0, 13); v[1] <- 1; v[13] <- c; v }
pol <- 1
for (i in 1:2) pol <- mult(pol, c(1, -0.5 / i))
for (i in 1:2) pol <- mult(pol, est(-0.6 / i))
for (i in 1:2) pol <- mult(pol, c(1, -1))
for (i in 1:2) pol <- mult(pol, est(-1))
co <- -pol[-1]
cat(sprintf("rezago más lejano %d · no nulos %d · mayor |coef| %.2f en el rezago %d · menor |coef| no nulo %.4f\n\n",
            length(co), sum(abs(co) > 1e-12), co[which.max(abs(co))], which.max(abs(co)), min(abs(co[abs(co) > 1e-12]))))

cat("== 7. M5 · pesos psi y sigma_h del airline en el estado inicial (theta = -0.40, Theta = -0.56) ==\n")
th <- -0.40; TH <- -0.56
ar <- -mult(c(1, -1), est(-1))[-1]
ma <- mult(c(1, th), est(TH))[-1]
psi <- c(1, ARMAtoMA(ar = ar, ma = ma, lag.max = 35))
s2 <- J$airpassengers$airline$sigma2
sh <- sqrt(cumsum(psi^2) * s2)
cat(sprintf("psi1 %.3f psi11 %.3f psi12 %.3f salto %.3f psi24 %.3f psi35 %.3f · sigma2 (JSON) %.6f · sigma1 %.4f sigma12 %.4f sigma24 %.4f sigma36 %.4f\n\n",
            psi[2], psi[12], psi[13], psi[13] - psi[12], psi[25], psi[36], s2, sh[1], sh[12], sh[24], sh[36]))

cat("== 8. M11 · el SARIMA y auto.arima dan el mismo pronóstico ==\n")
mo <- J$airpassengers$comparativa$modelos
cat("idénticos:", identical(mo$sarima$pronostico, mo$auto_arima$pronostico), "· otros pares idénticos:",
    sum(combn(names(mo), 2, function(x) identical(mo[[x[1]]]$pronostico, mo[[x[2]]]$pronostico))) - 1, "\n\n")

cat("== 9. Contraste del texto del mapa estacional (WCAG 2) ==\n")
lum <- function(rgb) { v <- rgb / 255; v <- ifelse(v <= 0.03928, v / 12.92, ((v + 0.055) / 1.055)^2.4)
  sum(c(0.2126, 0.7152, 0.0722) * v) }
cr <- function(a, b) (max(a, b) + 0.05) / (min(a, b) + 0.05)
L <- seq(0, 1, by = 1e-4)
peor <- min(sapply(L, function(l) max(cr(l, 1), cr(l, 0))))
cat(sprintf("blanco o negro, el mejor de los dos: peor caso %.2f:1 (en luminancia %.4f)\n", peor,
            L[which.min(sapply(L, function(l) max(cr(l, 1), cr(l, 0))))]))
pizarra <- lum(c(30, 41, 59))
hueco <- L[sapply(L, function(l) max(cr(l, 1), cr(l, pizarra)) < 4.5)]
cat(sprintf("pizarra #1e293b o blanco: ninguno llega a 4.5:1 con luminancia de fondo entre %.4f y %.4f\n",
            min(hueco), max(hueco)))
# Las dos paletas del componente, en 1001 pasos
mezcla <- function(a, b, t) round(a + (b - a) * t)
pal <- list(sec = lapply(seq(0, 1, by = 0.001), function(t) mezcla(c(238, 245, 242), c(1, 40, 32), t)),
            neg = lapply(seq(0, 1, by = 0.001), function(t) mezcla(c(248, 250, 252), c(255, 102, 0), t)),
            pos = lapply(seq(0, 1, by = 0.001), function(t) mezcla(c(248, 250, 252), c(1, 40, 32), t)))
regla <- function(rgb) { l <- lum(rgb); o <- cr(l, pizarra); w <- cr(l, 1)
  if (max(o, w) >= 4.5) max(o, w) else max(cr(l, 0), w) }
for (nm in names(pal)) {
  k <- sapply(pal[[nm]], regla)
  cat(sprintf("paleta %-3s: contraste mínimo con la regla del componente %.2f:1; con el umbral viejo (0.42) %.2f:1\n",
              nm, min(k), min(sapply(pal[[nm]], function(rgb) { l <- lum(rgb); if (l > 0.42) cr(l, pizarra) else cr(l, 1) }))))
}
