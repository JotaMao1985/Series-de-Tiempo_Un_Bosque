## v3 · verificador independiente de la R3 del capitulo 3
## Recalcula, con codigo propio, las cifras nuevas o cambiadas de la R3.
## Uso: Rscript --vanilla v3_cifras.R  (la TRM se lee de Htmls_Series/datos/)
suppressMessages(library(forecast))
r4 <- function(x) round(x, 4)
cat("== M1: MA(1) theta = +0.7 ==\n")
print(r4(ARMAacf(ma = 0.7, lag.max = 3)))                     # 0.4698
cat("rho1 a mano:", r4(0.7 / (1 + 0.49)), "\n")
set.seed(2026); x <- arima.sim(model = list(ma = 0.7), n = 600)
cat("r1 =", r4(acf(x, plot = FALSE)$acf[2]), " theta_hat =",
    r4(coef(arima(x, order = c(0, 0, 1), include.mean = FALSE))), "\n")   # 0.4614 0.6887
cat("ACF AR(1) phi=-0.6:", r4(ARMAacf(ar = -0.6, lag.max = 4)[-1]), "\n")
cat("ACF AR(1) phi=+0.6:", r4(ARMAacf(ar = 0.6, lag.max = 4)[-1]), "\n")

cat("\n== M2: pseudo-periodo de phi = (1.40, -0.69) y PACF de (0.5, 0.3) ==\n")
cat("P =", r4(2 * pi / acos(1.40 / (2 * sqrt(0.69)))), "\n")
cat("PACF:", r4(ARMAacf(ar = c(0.5, 0.3), lag.max = 4, pacf = TRUE)), "\n")

cat("\n== M3: theta = -1 ==\n")
cat("rho:", r4(ARMAacf(ma = -1, lag.max = 3)[-1]), " |raiz| =", Mod(polyroot(c(1, -1))), "\n")
th <- seq(-3, 3, by = 0.001); cat("min rho1 MA(1):", min(th / (1 + th^2)), "en", th[which.min(th / (1 + th^2))], "\n")

cat("\n== M5: ARMA(1,1) phi=0.7 theta=0.5 ==\n")
ph <- 0.7; t <- 0.5
g0 <- (1 + 2 * ph * t + t^2) / (1 - ph^2); g1 <- (1 + ph * t) * (ph + t) / (1 - ph^2)
cat("gamma0 =", r4(g0), " gamma1 =", r4(g1), " num g1 =", (1 + ph * t) * (ph + t), " rho1 =", r4(g1 / g0), "\n")
cat("ARMAacf:", r4(ARMAacf(ar = ph, ma = t, lag.max = 4)[-1]), "\n")
cat("bandas T=60, T=1000:", round(1.96 / sqrt(c(60, 1000)), 3), "\n")

cat("\n== M8: Monte Carlo fitdf (otra semilla y la del capitulo) ==\n")
mc <- function(seed, B = 3000) {
  set.seed(seed)
  p <- replicate(B, {
    y <- arima.sim(list(ar = c(1.4, -0.7)), n = 100)
    e <- residuals(suppressWarnings(arima(y, order = c(2, 0, 0), method = "ML")))
    c(Box.test(e, 12, "Ljung-Box")$p.value, Box.test(e, 12, "Ljung-Box", fitdf = 2)$p.value)
  })
  r4(rowMeans(p < 0.05))
}
cat("semilla 8 (capitulo):", mc(8), "\n")
cat("semilla 123 (control):", mc(123), "\n")

cat("\n== M9 caso 1 ==\n")
m <- window(sunspot.year, start = 1770, end = 1869)
elas <- function(x, k) {
  nb <- length(x) %/% k; x <- as.numeric(x)[1:(nb * k)]
  M <- matrix(x, nrow = k)                          # una columna por bloque
  fit <- lm(log(apply(M, 2, sd)) ~ log(colMeans(M)))
  c(coef(fit)[2], confint(fit)[2, ], summary(fit)$r.squared)
}
print(round(rbind(k10 = elas(m, 10), k11 = elas(m, 11), k5 = elas(m, 5)), 4))
cat("ceros 1770-1869:", sum(m == 0), " en 1700-1988:", sum(sunspot.year == 0), "\n")
lam <- BoxCox.lambda(m + 1, method = "guerrero"); cat("lambda Guerrero:", r4(lam), "\n")
b <- 1.96 / sqrt(100)
for (s in list(cruda = m, raiz = sqrt(m))) {
  p <- pacf(s, lag.max = 20, plot = FALSE)$acf[, 1, 1]
  cat("PACF fuera:", paste0(which(abs(p) > b), ":", round(p[abs(p) > b], 3)), "\n")
}
aicc <- function(f, n) f$aic + 2 * (length(f$coef) + 1) * (length(f$coef) + 2) / (n - length(f$coef) - 2)
grid <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
tab <- t(sapply(grid, function(pq) {
  fc <- arima(m, order = c(pq[1], 0, pq[2]), method = "ML")
  fs <- arima(sqrt(m), order = c(pq[1], 0, pq[2]), method = "ML")
  c(p = pq[1], q = pq[2], AICc_cruda = aicc(fc, 100), LB_cruda = Box.test(residuals(fc), 12, "Ljung-Box", fitdf = sum(pq))$p.value,
    AICc_raiz = aicc(fs, 100), BIC_raiz = BIC(fs), LB_raiz = Box.test(residuals(fs), 12, "Ljung-Box", fitdf = sum(pq))$p.value)
}))
print(round(tab[order(tab[, "AICc_raiz"]), ], 4))
cat("min BIC raiz en:", tab[which.min(tab[, "BIC_raiz"]), 1:2], "\n")
f <- arima(sqrt(m), order = c(2, 0, 0), method = "ML"); se <- sqrt(diag(f$var.coef))
cat("AR2 raiz coef:", r4(coef(f)), " ee:", r4(se[1:2]), " t:", round(coef(f)[1:2] / se[1:2], 2), " s2:", r4(f$sigma2), "\n")
rr <- polyroot(c(1, -coef(f)[1:2]))
cat("raiz:", r4(Mod(rr[1])), r4(Arg(rr[1])), " P =", r4(2 * pi / abs(Arg(rr[1]))), "\n")
cat("signo cambiado, raices:", r4(sort(Re(polyroot(c(1, -coef(f)[1], coef(f)[2]))))), "\n")
cat("FPP3 periodo medio:", r4(2 * pi / acos(-coef(f)[1] * (1 - coef(f)[2]) / (4 * coef(f)[2]))), "\n")
for (nm in c("guerrero", "desplazada")) {
  y <- if (nm == "guerrero") m^lam else (m + 1)^lam
  g <- arima(y, order = c(2, 0, 0), method = "ML"); z <- polyroot(c(1, -coef(g)[1:2]))
  cat(nm, ": P =", r4(2 * pi / abs(Arg(z[1]))), " LB =", r4(Box.test(residuals(g), 12, "Ljung-Box", fitdf = 2)$p.value), "\n")
}
cat("PACF teorica:", r4(ARMAacf(ar = coef(f)[1:2], lag.max = 3, pacf = TRUE)), "\n")
a21 <- arima(m, order = c(2, 0, 1), method = "ML")
cat("ARMA(2,1) cruda:", r4(coef(a21)), " t_theta:", round(coef(a21)[3] / sqrt(a21$var.coef[3, 3]), 2),
    " raiz MA:", r4(-1 / coef(a21)[3]), " |raiz AR|:", r4(Mod(polyroot(c(1, -coef(a21)[1:2]))[1])), "\n")
psi <- c(1, ARMAtoMA(ar = coef(f)[1:2], lag.max = 11))
cat("psi:", r4(psi), "\n")
R <- sqrt(-coef(f)[[2]]); w <- abs(Arg(rr[1]))
cat("R, 1/sin w, mitad, pi/w:", r4(c(R, 1 / sin(w), log(0.5) / log(R), pi / w)), "\n")
cs <- cumsum(psi^2); ee <- sqrt(f$sigma2 * cs)
cat("cumsum psi2:", r4(cs), "\nee:", round(ee, 2), "\nsemiancho:", round(qnorm(.975) * ee, 2), "\n")
fc <- forecast(f, h = 8, level = 95)
cat("forecast semiancho h1-6:", r4(((fc$upper - fc$lower) / 2)[1:6]), "\n")
S <- sum(c(1, ARMAtoMA(ar = coef(f)[1:2], lag.max = 3000))^2)
cat("suma psi2 inf:", r4(S), " gamma0:", r4(f$sigma2 * S), " var muestral:", r4(var(sqrt(m))),
    " techo:", r4(qnorm(.975) * sqrt(f$sigma2 * S)), " fraccion h6:", r4(qnorm(.975) * ee[6] / (qnorm(.975) * sqrt(f$sigma2 * S))), "\n")
cat("inferior h7,h8:", round(fc$lower[7:8], 3), " al cuadrado:", round(fc$lower[7:8]^2, 3), "\n")
sk <- function(e) { e <- e - mean(e); mean(e^3) / sd(e)^3 }
ml <- arima(m, order = c(2, 0, 0), method = "ML")
cat("asimetria cruda/raiz:", round(c(sk(residuals(ml)), sk(residuals(f))), 3),
    " Shapiro:", r4(c(shapiro.test(residuals(ml))$p.value, shapiro.test(residuals(f))$p.value)), "\n")

cat("\n== M9 caso 2: TRM ==\n")
trm <- read.csv(file.path("Htmls_Series", "datos", "trm_mensual_2015-01_2026-06.csv"))
print(head(trm, 2)); col <- names(trm)[sapply(trm, is.numeric)][1]
ret <- 100 * diff(log(trm[[col]])); cat("T =", length(ret), "\n")
a <- acf(ret, lag.max = 20, plot = FALSE)$acf[-1]
cat("fuera de la banda:", paste0(which(abs(a) > 1.96 / sqrt(length(ret))), ":", round(a[abs(a) > 1.96 / sqrt(length(ret))], 3)), "\n")
# rho_1 de la primera diferencia de un promedio de m dias de una caminata aleatoria, por simulacion y formula
mm <- 21
w <- c(1:mm, (mm - 1):1) / mm
rho_f <- sum(w[1:(mm - 1)] * w[(mm + 1):(2 * mm - 1)]) / sum(w^2)
set.seed(1); d <- cumsum(rnorm(mm * 20000)); prom <- colMeans(matrix(d, nrow = mm)); dp <- diff(prom)
cat("rho1 inducido formula:", round(rho_f, 4), " simulacion:", round(cor(dp[-1], dp[-length(dp)]), 4),
    " distancia en ee:", round((rho_f - a[1]) * sqrt(length(ret)), 3), "\n")
aa <- auto.arima(ret); cat("auto.arima defecto:", arimaorder(aa), " ic:", "aicc (defecto de auto.arima)\n")
