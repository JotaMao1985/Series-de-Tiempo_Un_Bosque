# Verificador independiente R2 cap. 5: recalcula en R 4.6 (forecast) las cifras nuevas o tocadas.
# Uso: Rscript diagnostico/cap5/comprobaciones/v2_cifras.R <SERIES_CAP5.json>
suppressPackageStartupMessages({ library(forecast); library(jsonlite) })
args <- commandArgs(TRUE)
S <- fromJSON(args[1])
cat("R", R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n\n")

# ---- 1. M6: fila (0,1,0)(0,1,0)[12] sobre log(AirPassengers)
ly <- log(AirPassengers)
f0 <- Arima(ly, order = c(0, 1, 0), seasonal = c(0, 1, 0))
cat("== M6 (0,1,0)(0,1,0)[12]\n")
cat(sprintf("AICc %.4f  BIC %.4f  AIC %.4f  nobs %d\n", f0$aicc, f0$bic, f0$aic, f0$nobs))
r <- residuals(f0)
cat(sprintf("rho12 resid (144 residuales, como el airline del JSON): %.4f\n", acf(r, 36, plot = FALSE)$acf[13]))
cat(sprintf("rho12 resid (sin los 13 primeros): %.4f\n", acf(r[-(1:13)], 36, plot = FALSE)$acf[13]))
lb <- Box.test(r, lag = 24, type = "Ljung-Box", fitdf = 0)
cat(sprintf("Ljung-Box(24) p = %.3g (Q = %.2f)\n", lb$p.value, lb$statistic))
fa <- Arima(ly, order = c(0, 1, 1), seasonal = c(0, 1, 1))
cat(sprintf("airline: theta %.4f  Theta %.4f (e.e. %.4f)  IC95 Theta [%.4f, %.4f]  BIC %.4f\n",
  coef(fa)[1], coef(fa)[2], sqrt(diag(fa$var.coef))[2],
  coef(fa)[2] - 1.96 * sqrt(diag(fa$var.coef))[2], coef(fa)[2] + 1.96 * sqrt(diag(fa$var.coef))[2], fa$bic))
cat(sprintf("rho12 teórico del SMA(1) con Theta^: Theta/(1+Theta^2) = %.4f\n\n", coef(fa)[2] / (1 + coef(fa)[2]^2)))

# ---- 2. M1: las 32 combinaciones; dónde salta la nota «negativo tras ∇12»
cat("== M1 mapa-firma: ACF hasta min(36, n-2), banda 1.96/sqrt(n)\n")
serie <- function(k) ts(S[[k]]$valores, start = S[[k]]$inicio, frequency = 12)
for (k in c("airpassengers", "usaccdeaths", "co2", "trm")) for (lg in c(TRUE, FALSE))
  for (df in c("ninguna", "d1", "D1", "d1D1")) {
    y <- serie(k); if (lg) y <- log(y)
    if (df %in% c("D1", "d1D1")) y <- diff(y, lag = 12)
    if (df %in% c("d1", "d1D1")) y <- diff(y)
    n <- length(y); L <- min(36, n - 2)
    a <- acf(as.numeric(y), lag.max = L, plot = FALSE, demean = TRUE)$acf[-1]
    b <- 1.96 / sqrt(n)
    fuera <- which(abs(a) > b)
    est <- fuera[fuera %% 12 == 0]; otros <- fuera[fuera %% 12 != 0]
    nota <- df %in% c("D1", "d1D1") && any(a[est] < 0)
    cat(sprintf("%-13s %-5s %-7s n=%3d r1=%7.4f r12=%7.4f r24=%7.4f r36=%7.4f b=%.4f  x12: %-9s otros: %-22s nota=%s\n",
      k, ifelse(lg, "log", "nolog"), df, n, a[1], a[12], if (L >= 24) a[24] else NA, if (L >= 36) a[36] else NA, b,
      if (length(est)) paste(est, collapse = ",") else "ninguno", if (length(otros)) paste(otros, collapse = ",") else "ninguno",
      ifelse(nota, "SÍ", "no")))
  }
cat("\nTeoría: si y_t es una caminata aleatoria (TRM), ∇12 y_t = e_t + … + e_{t-11} tiene rho_12 = 0,",
    "y ∇∇12 y_t = e_t − e_{t-12} tiene rho_12 = −0.5 exactamente.\n")
cat(sprintf("ARMAacf(ma = c(rep(1, 11)))[13] = %.4f ; ARMAacf(ma = c(rep(0, 11), -1))[13] = %.4f\n\n",
  ARMAacf(ma = rep(1, 11), lag.max = 12)[13], ARMAacf(ma = c(rep(0, 11), -1), lag.max = 12)[13]))

# ---- 3. M7: ancho del IC 95 % en logaritmos, h = 1…24
fc <- forecast(fa, h = 24, level = c(80, 95))
w <- as.numeric(fc$upper[, 2] - fc$lower[, 2])
cat("== M7 ancho del IC 95 % (log) y su incremento\n")
for (h in 1:24) cat(sprintf("h=%2d ancho=%.4f  incremento=%s\n", h, w[h], if (h > 1) sprintf("%+.4f", w[h] - w[h - 1]) else "—"))
cat("\n")

# ---- 4. M5: pesos psi y sigma_h del airline en el estado inicial del simulador (theta = -0.40, Theta = -0.56)
psi_airline <- function(th, Th, H = 36) {
  ar <- c(1, rep(0, 10), 1, -1)                 # (1-B)(1-B^12) = 1 - B - B^12 + B^13
  ma <- c(th, rep(0, 10), Th, th * Th)
  c(1, ARMAtoMA(ar = ar, ma = ma, lag.max = H))
}
s2 <- 0.001371
for (par in list(c(-0.40, -0.56), c(-0.95, -0.95), c(-0.40, 0))) {
  p <- psi_airline(par[1], par[2])
  sh <- sqrt(s2 * cumsum(p^2))[1:36]
  cat(sprintf("== M5 theta=%.2f Theta=%.2f: psi1 %.3f psi11 %.3f psi12 %.3f salto %.3f psi24 %.3f psi35 %.3f | s1 %.4f s12 %.4f s24 %.4f s36 %.4f\n",
    par[1], par[2], p[2], p[12], p[13], p[13] - p[12], p[25], p[36], sh[1], sh[12], sh[24], sh[36]))
}
cat("\n")

# ---- 5. Quiz, pregunta 5: ACF teórica de un SAR(1)_12 con Phi = 0.7
q <- ARMAacf(ar = c(rep(0, 11), 0.7), lag.max = 36)[-1]
cat("== Quiz: rezagos con |rho| >= 0.005:", paste(sprintf("%d:%.2f", which(abs(q) >= 0.005), q[abs(q) >= 0.005]), collapse = " "),
    "| los demás:", sum(abs(q) < 0.005), "\n\n")

# ---- 6. M9: años 1949-1960 con el Domingo de Pascua en marzo (algoritmo de Meeus/Jones/Butcher)
pascua <- function(Y) { a <- Y %% 19; b <- Y %/% 100; c <- Y %% 100; d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25
  g <- (b - f + 1) %/% 3; h <- (19 * a + b - d - g + 15) %% 30; i <- c %/% 4; k <- c %% 4
  l <- (32 + 2 * e + 2 * i - h - k) %% 7; m <- (a + 11 * h + 22 * l) %/% 451
  mes <- (h + l - 7 * m + 114) %/% 31; dia <- ((h + l - 7 * m + 114) %% 31) + 1; sprintf("%d-%02d-%02d", Y, mes, dia) }
pa <- sapply(1949:1960, pascua)
cat("== M9 Pascuas:", paste(pa, collapse = " "), "\n   en marzo:", sum(substr(pa, 6, 7) == "03"), "de", length(pa), "\n\n")

# ---- 7. M2 constructor: coeficientes no nulos con todo en 2 (p=d=P=D=2)
pol <- function(v, w) { r <- rep(0, length(v) + length(w) - 1); for (i in seq_along(v)) for (j in seq_along(w)) r[i + j - 1] <- r[i + j - 1] + v[i] * w[j]; r }

# ---- 8. aria-label del M6 con (0,1,0)(0,1,0): barras fuera de ±1.96/sqrt(144) en los rezagos 1–24 y rho_1
a0 <- acf(residuals(f0), 24, plot = FALSE)$acf[-1]
cat(sprintf("== M6 aria (0,1,0)(0,1,0): %d de 24 fuera de ±%.3f; rho_1 = %.3f\n", sum(abs(a0) > 1.96 / sqrt(144)), 1.96 / sqrt(144), a0[1]))
