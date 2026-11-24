# R1 del capítulo 5 · comprobaciones del redactor (2026-11-23)
# Uso: Rscript r1_comprobaciones.R > r1_comprobaciones.out   (desde esta carpeta)
suppressMessages({ library(forecast) })
options(width = 110)
ap <- log(AirPassengers)
fit <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
th <- coef(fit)[["ma1"]]; TH <- coef(fit)[["sma1"]]
cat("== airline:", round(c(th, TH), 6), " sigma2", round(fit$sigma2, 6), "\n")

# --- E1 (M5) · el airline frente a una caminata: psi y sigma_h/sigma --------------
H <- 240
psi <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = c(th, rep(0, 10), TH, th * TH), lag.max = H))
sh  <- sqrt(cumsum(psi^2))            # sigma_h / sigma, h = 1..H+1
cat("\n== E1 · psi_j en j = 12, 24, 60, 120, 240\n")
print(round(psi[c(12, 24, 60, 120, 240) + 1], 4))
cat("subida anual de psi (psi_{j+12} - psi_j) en j = 24, 120, 228:",
    round(psi[c(36, 132, 240) + 1] - psi[c(24, 120, 228) + 1], 4),
    " (1+theta)(1+Theta) =", round((1 + th) * (1 + TH), 4), "\n")
hh <- c(1, 12, 24, 36, 41, 42, 48, 120, 240)
print(round(rbind(h = hh, airline = sh[hh], caminata = sqrt(hh), razon = sh[hh] / sqrt(hh)), 3))
cat("primer h con sigma_h(airline) > sigma_h(caminata):", min(which(sh > sqrt(seq_along(sh)))), "\n")
cat("sigma_12/sigma_1 =", round(sh[12] / sh[1], 3), " sqrt(12) =", round(sqrt(12), 3), "\n")

# --- E2 (M5) · salto psi_12 - psi_11 = 1 + Theta -----------------------------------
cat("\n== E2 · salto psi_12 - psi_11 segun Theta (theta del ajuste)\n")
for (T2 in c(0, TH, -0.95, -0.99)) {
  p <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = c(th, rep(0, 10), T2, th * T2), lag.max = 25))
  cat(sprintf("Theta = %6.3f  psi_11 = %.4f  psi_12 = %.4f  salto = %.4f  (1 + Theta = %.4f)\n",
              T2, p[12], p[13], p[13] - p[12], 1 + T2))
}

# --- M2 · factorizacion de la ACF de un MA x SMA: q < m frente a 2q < m -----------
cat("\n== M2 · MA(7) x SMA(1), m = 12: la varianza factoriza, la ACF no\n")
thq <- rep(0.5, 7); Thq <- 0.6
ma_full <- c(thq, rep(0, 4), Thq, Thq * thq)
g0 <- 1 + sum(ma_full^2)
cat("gamma0 exacta", round(g0, 4), " factorizada", round((1 + sum(thq^2)) * (1 + Thq^2), 4), "\n")
r_full <- ARMAacf(ma = ma_full, lag.max = 20)
r_reg  <- ARMAacf(ma = thq, lag.max = 7)
cat("rho_5 exacta", round(r_full[["5"]], 4), " rho_5 regular", round(r_reg[["5"]], 4), "\n")

# --- M3 · sobrediferenciacion estacional: Theta y su distancia a -1 -----------------
cat("\n== M3 · D = 0, 1, 2 con d = 1\n")
for (D in 0:2) {
  f <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, D, 1), period = 12))
  Tt <- coef(f)[["sma1"]]; ee <- sqrt(diag(f$var.coef))[["sma1"]]
  cat(sprintf("D=%d Theta=%+.4f ee=%.4f (Theta+1)/ee=%.2f IC95=[%.3f, %.3f] |raiz|^-1=%.4f |Theta|^(1/12)=%.4f\n",
              D, Tt, ee, (Tt + 1) / ee, Tt - 1.96 * ee, Tt + 1.96 * ee,
              max(Mod(1 / polyroot(c(1, f$model$theta)))), abs(Tt)^(1 / 12)))
}

# --- M4 · rho_11, rho_13 y el producto con parte AR -------------------------------
cat("\n== M4 · AR(1) x SAR(1), phi = 0.6, Phi = 0.7\n")
r <- ARMAacf(ar = c(0.6, rep(0, 10), 0.7, -0.42), lag.max = 13)
cat(sprintf("rho1 %.7f rho11 %.7f rho12 %.7f rho13 %.7f rho1*rho12 %.7f\n",
            r[["1"]], r[["11"]], r[["12"]], r[["13"]], r[["1"]] * r[["12"]]))

# --- M6 · Ljung-Box de R con y sin los 13 residuales de arranque -----------------
cat("\n== M6 · residuales de arranque del airline en R\n")
e <- residuals(fit)
cat("desv. tipica de los 13 primeros", round(sd(e[1:13]), 4), " del resto", round(sd(e[-(1:13)]), 4), "\n")
lb <- function(x, h) Box.test(x, lag = h, type = "Ljung-Box", fitdf = 2)$p.value
cat("LB(24) con los 144:", round(lb(e, 24), 4), " sin los 13:", round(lb(e[-(1:13)], 24), 4), "\n")
cat("LB(36) con los 144:", round(lb(e, 36), 4), " sin los 13:", round(lb(e[-(1:13)], 36), 4), "\n")
cat("Shapiro con los 144:", round(shapiro.test(e)$p.value, 4), " sin los 13:",
    round(shapiro.test(e[-(1:13)])$p.value, 4), "\n")
f0 <- Arima(ap, order = c(0, 1, 0), seasonal = list(order = c(0, 1, 0), period = 12))
cat("(0,1,0)(0,1,0): AICc", round(f0$aicc, 2), " LB(24) p", signif(Box.test(residuals(f0), lag = 24, type = "Ljung-Box")$p.value, 3), "\n")

# --- M7 · salida real del bloque --------------------------------------------------
cat("\n== M7 · round(c(coef, sigma2, aicc), 6)\n")
print(round(c(coef(fit), sigma2 = fit$sigma2, aicc = fit$aicc), 6))

# --- M9 · el modelo con solo Semana Santa (para el simulador) ---------------------
cat("\n== M9 · Semana Santa sola\n")
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = 144)
pascua <- function(anio) {
  a <- anio %% 19; b <- anio %/% 100; cc <- anio %% 100
  d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3
  h <- (19*a + b - d - g + 15) %% 30; i <- cc %/% 4; k <- cc %% 4
  l <- (32 + 2*e + 2*i - h - k) %% 7; m <- (a + 11*h + 22*l) %/% 451
  as.Date(sprintf("%04d-%02d-%02d", anio, (h + l - 7*m + 114) %/% 31, ((h + l - 7*m + 114) %% 31) + 1))
}
es_p <- as.numeric(format(fechas, "%m") == sapply(as.numeric(format(fechas, "%Y")), function(a) format(pascua(a), "%m")))
fp <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), xreg = cbind(pascua = es_p))
cat("AICc", round(fp$aicc, 4), " BIC", round(fp$bic, 4), " beta", round(coef(fp)[["pascua"]], 4),
    " ee", round(sqrt(diag(fp$var.coef))[["pascua"]], 4), "\n")

# --- M10 · por que ARIMA(0,0,0)(0,1,0)[365]; AIC frente a AICc de stlm ------------
cat("\n== M10\n")
cat("floor(800 / (3 * 365)) =", floor(800 / (3 * 365)), "\n")
cat("en el codigo de auto.arima:\n")
print(grep("max.P <-|max.Q <-", deparse(body(auto.arima)), value = TRUE))
s <- stlm(AirPassengers |> log(), s.window = "periodic", method = "arima")
cat("stlm: AIC", round(s$model$aic, 2), " AICc", round(s$model$aicc, 2), "\n")

# --- M11 · el K de la armonica, con y sin los 24 meses de prueba -----------------
cat("\n== M11 · K elegido por AICc\n")
ent <- window(ap, end = c(1958, 12))
for (serie in list(list("completa", ap), list("entrenamiento", ent))) {
  a <- sapply(1:6, function(K) auto.arima(serie[[2]], xreg = fourier(serie[[2]], K = K), seasonal = FALSE,
                                          stepwise = FALSE, approximation = FALSE)$aicc)
  cat(sprintf("%-14s AICc K=1..6: %s  -> K = %d\n", serie[[1]], paste(round(a, 2), collapse = " "), which.min(a)))
}

# --- E1 (co2) · evidencias para D y d, sin varianzas -------------------------------
cat("\n== Ejercicio 1 · co2\n")
a <- Acf(diff(co2), lag.max = 36, plot = FALSE)$acf
cat("ACF de diff(co2) en 12, 24, 36:", round(a[c(13, 25, 37)], 4), " banda", round(1.96 / sqrt(length(co2) - 1), 4), "\n")
w <- diff(diff(co2, lag = 12)); b <- Acf(w, lag.max = 36, plot = FALSE)$acf
cat("ACF de la doble diferencia en 1 y 12:", round(b[c(2, 13)], 4), "\n")
al <- Arima(co2, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
cat("airline co2: Theta", round(coef(al)[["sma1"]], 4), " ee", round(sqrt(diag(al$var.coef))[["sma1"]], 4),
    " theta", round(coef(al)[["ma1"]], 4), " ee", round(sqrt(diag(al$var.coef))[["ma1"]], 4),
    " LB(24) p", round(Box.test(residuals(al), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4), "\n")

# --- Quiz, item 6 · parametros de la armonica con K = 5 y K = 6 -------------------
cat("\n== Quiz 6\n")
for (K in 5:6) {
  f <- auto.arima(ap, xreg = fourier(ap, K = K), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  cat(sprintf("K=%d  AICc %.2f  coeficientes %d  (%s)\n", K, f$aicc, length(coef(f)), as.character(f)))
}
cat("\n", R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n")
