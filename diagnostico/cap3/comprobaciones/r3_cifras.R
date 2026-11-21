# R3 del capítulo 3 · cifras que la ronda escribe o hace visibles.
# Cada sección dice qué frase del capítulo respalda. Se ejecuta desde la raíz del repo:
#   Rscript diagnostico/cap3/comprobaciones/r3_cifras.R > diagnostico/cap3/comprobaciones/r3_cifras.out
suppressMessages(library(forecast))
tit <- function(s) cat("\n====", s, "====\n")

manchas <- window(sunspot.year, start = 1770, end = 1869)

# ---------------------------------------------------------------------------
tit("M1 · el convenio de signo, sin arima(): MA(1) con theta = 0.7, n = 600")
set.seed(2026)
x <- arima.sim(model = list(ma = 0.7), n = 600)
cat("rho_1 teorica theta/(1+theta^2):", round(0.7 / (1 + 0.7^2), 4), "\n")
print(round(ARMAacf(ma = 0.7, lag.max = 3), 4))
cat("r_1 muestral:", round(acf(x, plot = FALSE)$acf[2], 4), "\n")
f <- arima(x, order = c(0, 0, 1), include.mean = FALSE)
cat("ma1 estimado:", round(coef(f), 4), "  s.e.:", round(sqrt(diag(f$var.coef)), 4), "\n")
print(f)
cat("AR(1) con phi = 0.6: ACF teorica ", round(ARMAacf(ar = 0.6, lag.max = 4)[-1], 4), "\n")
cat("AR(1) con phi = -0.6: ACF teorica", round(ARMAacf(ar = -0.6, lag.max = 4)[-1], 4), "\n")

# ---------------------------------------------------------------------------
tit("M3 · sobrediferenciar un ruido blanco: MA(1) con theta = -1")
print(round(ARMAacf(ma = -1, lag.max = 3), 4))
print(Mod(polyroot(c(1, -1))))
set.seed(2026)
e <- rnorm(500); d <- diff(e)
cat("r_1 de diff(ruido blanco):", round(acf(d, plot = FALSE)$acf[2], 4), "\n")

# ---------------------------------------------------------------------------
tit("M5 · gamma_1 y rho_1 del ARMA(1,1) con phi = 0.7 y theta = 0.5")
phi <- 0.7; theta <- 0.5
g0 <- (1 + 2*phi*theta + theta^2) / (1 - phi^2)
g1 <- (1 + phi*theta) * (phi + theta) / (1 - phi^2)
cat("gamma0 =", g0, " gamma1 =", g1, " rho1 =", g1 / g0, "\n")
cat("1+2 phi theta + theta^2 =", 1 + 2*phi*theta + theta^2, " (1+phi theta)(phi+theta) =", (1 + phi*theta)*(phi + theta), "\n")

# ---------------------------------------------------------------------------
tit("M9 · elasticidad amplitud-nivel: la versión corta frente a la de genera_cap3.R")
elasticidad_pre <- function(x, g) {
  niv <- tapply(as.numeric(x), g, mean); amp <- tapply(as.numeric(x), g, sd)
  ok <- niv > 0 & amp > 0
  aj <- lm(log(amp[ok]) ~ log(niv[ok]))
  c(b = coef(aj)[[2]], confint(aj)[2, ], R2 = summary(aj)$r.squared, bloques = sum(ok))
}
n_m <- length(manchas)
pre <- rbind(
  elasticidad_pre(manchas, rep(1:10, each = 10)),
  elasticidad_pre(manchas, cut(1:n_m, breaks = seq(0, n_m, by = 11.1), labels = FALSE)),
  elasticidad_pre(manchas, rep(1:20, each = 5)))
print(round(pre, 4))
# versión que escribirá la página
elasticidad <- function(x, k) {
  g <- rep(seq_len(length(x) %/% k), each = k)
  x <- as.numeric(x)[seq_along(g)]
  niv <- tapply(x, g, mean); amp <- tapply(x, g, sd)
  aj <- lm(log(amp) ~ log(niv))
  c(b = coef(aj)[[2]], confint(aj)[2, ], R2 = summary(aj)$r.squared)
}
res <- t(sapply(c(10, 11, 5), function(k) elasticidad(manchas, k)))
print(round(res, 4))
cat("¿iguales a la de genera_cap3.R? ", all.equal(unname(res), unname(pre[, 1:4])), "\n")

tit("M9 · ceros")
cat("ceros en la ventana:", sum(manchas == 0), " en la serie completa:", sum(sunspot.year == 0),
    " año del cero:", time(manchas)[manchas == 0], "\n")

tit("M9 · PACF fuera de la banda, cruda y raíz (lag.max = 20)")
banda <- 1.96 / sqrt(100)
for (nm in c("cruda", "raiz")) {
  x <- if (nm == "cruda") manchas else sqrt(manchas)
  p <- pacf(x, lag.max = 20, plot = FALSE)$acf[, 1, 1]
  cat(nm, ": fuera de la banda en rezagos", which(abs(p) > banda), "\n")
  print(round(setNames(p[abs(p) > banda], which(abs(p) > banda)), 3))
}
cat("banda:", round(banda, 3), "\n")

tit("M9 · la rejilla del Módulo 8 sobre la raíz cuadrada")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
rejilla <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
rej <- function(x) do.call(rbind, lapply(rejilla, function(pq) {
  aj <- arima(x, order = c(pq[1], 0, pq[2]), method = "ML")
  data.frame(modelo = sprintf("ARMA(%d,%d)", pq[1], pq[2]), AICc = round(aicc(aj, length(x)), 2),
             BIC = round(BIC(aj), 2),
             LB12 = round(Box.test(residuals(aj), lag = 12, type = "Ljung-Box", fitdf = sum(pq))$p.value, 4))
}))
rs <- rej(sqrt(manchas)); print(rs[order(rs$AICc), ])
cat("mínimo AICc:", rs$modelo[which.min(rs$AICc)], " mínimo BIC:", rs$modelo[which.min(rs$BIC)], "\n")
rc <- rej(manchas); print(rc[order(rc$AICc), ])

tit("M9 · AR(2) final sobre sqrt: se, sigma2, polinomio mal escrito, PACF teórica")
ar2s <- arima(sqrt(manchas), order = c(2, 0, 0), method = "ML")
phi <- coef(ar2s)[1:2]
cat("coef:", round(coef(ar2s), 4), " se:", round(sqrt(diag(ar2s$var.coef)), 4), " sigma2:", round(ar2s$sigma2, 4), "\n")
cat("t:", round(coef(ar2s)[1:2] / sqrt(diag(ar2s$var.coef))[1:2], 2), "\n")
cat("polinomio bien escrito, raíces:", round(polyroot(c(1, -phi)), 4), "\n")
cat("polinomio MAL escrito 1 - 1.4027B - 0.6853B^2, raíces:", round(polyroot(c(1, -phi[[1]], phi[[2]])), 4), "\n")
cat("PACF teórica AR(2) final:", round(ARMAacf(ar = phi, lag.max = 3, pacf = TRUE), 4), "\n")
raices <- polyroot(c(1, -phi)); w <- Arg(raices)[1]; Rmod <- unname(sqrt(-phi[2]))
cat("R =", round(Rmod, 4), " 1/sin(w) =", round(1 / sin(w), 4), " mitad (años) =", round(log(0.5) / log(Rmod), 4),
    " pi/w =", round(pi / w, 4), " 2pi/w =", round(2 * pi / w, 4), "\n")

tit("M9 · variantes de lambda")
ajusta <- function(x) {
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  p <- coef(f)[1:2]
  c(periodo = 2 * pi / Arg(polyroot(c(1, -p))[1]),
    LB12 = Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value)
}
lambda <- BoxCox.lambda(manchas + 1, method = "guerrero")
cat("lambda:", round(lambda, 4), "\n")
print(round(rbind(raiz = ajusta(sqrt(manchas)), guerrero = ajusta(manchas^lambda),
                  guerrero_desplazada = ajusta((manchas + 1)^lambda)), 4))
cat("Guerrero sin desplazar (aviso):\n")
print(round(suppressWarnings(BoxCox.lambda(manchas, method = "guerrero")), 4))

tit("M9 · ARMA(2,1) sobre la cruda")
a21 <- arima(manchas, order = c(2, 0, 1), method = "ML")
print(round(coef(a21), 4)); print(round(sqrt(diag(a21$var.coef)), 4))
cat("t de theta1:", round(coef(a21)[["ma1"]] / sqrt(a21$var.coef["ma1", "ma1"]), 2), "\n")
cat("raíz MA:", round(polyroot(c(1, coef(a21)[["ma1"]])), 4), " módulo", round(Mod(polyroot(c(1, coef(a21)[["ma1"]]))), 4), "\n")
ra <- polyroot(c(1, -coef(a21)[c("ar1", "ar2")]))
cat("raíces AR:", round(ra, 4), " módulo", round(Mod(ra), 4), "\n")

tit("M9 · tabla de psi, cumsum, errores estándar y semianchos, 12 filas")
psi <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 11))
ee <- sqrt(ar2s$sigma2 * cumsum(psi^2))
print(round(cbind(j = 0:11, psi = psi, h = 1:12, suma = cumsum(psi^2), ee = ee, semi = qnorm(0.975) * ee), 4))
psi_largo <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 600))
gamma0 <- ar2s$sigma2 * sum(psi_largo^2)
cat("suma psi^2 =", round(sum(psi_largo^2), 4), " gamma0 =", round(gamma0, 4), " var muestral =", round(var(sqrt(manchas)), 4), "\n")
cat("techo del semiancho:", round(qnorm(0.975) * sqrt(gamma0), 4), " fracción a h = 6:",
    round(qnorm(0.975) * ee[6] / (qnorm(0.975) * sqrt(gamma0)), 4), "\n")
f8 <- forecast(ar2s, h = 8, level = 95)
cat("lower h = 7, 8:", round(as.numeric(f8$lower)[7:8], 3), " al cuadrado:", round(as.numeric(f8$lower)[7:8]^2, 3), "\n")

tit("M9 · residuales: asimetría y Shapiro, cruda frente a raíz")
ml <- arima(manchas, order = c(2, 0, 0), method = "ML")
asim <- function(e) mean((e - mean(e))^3) / sd(e)^3
cat("cruda: asimetría", round(asim(residuals(ml)), 3), " Shapiro p", round(shapiro.test(residuals(ml))$p.value, 4), "\n")
cat("raíz : asimetría", round(asim(residuals(ar2s)), 3), " Shapiro p", round(shapiro.test(residuals(ar2s))$p.value, 4), "\n")
cat("(con la definición de momentos: ", round(asim(residuals(ml)) , 4), ")\n")
sk <- function(e) { m <- mean(e); mean((e - m)^3) / mean((e - m)^2)^1.5 }
cat("cruda (m3/m2^1.5):", round(sk(residuals(ml)), 3), " raíz:", round(sk(residuals(ar2s)), 3), "\n")

tit("M9 · TRM")
archivo <- "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv"
trm <- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)
ret <- diff(log(trm)) * 100
a <- acf(ret, lag.max = 20, plot = FALSE)$acf[-1]
cat("n =", length(ret), " banda =", round(1.96 / sqrt(length(ret)), 4), "\n")
print(round(setNames(a[abs(a) > 1.96 / sqrt(137)], which(abs(a) > 1.96 / sqrt(137))), 3))
cat("r1 =", round(a[1], 4), "\n")
rho1_promedio <- function(m) {
  cw <- c(1:m, (m - 1):1) / m
  sum(cw[1:(m - 1)] * cw[(m + 1):(2 * m - 1)]) / sum(cw^2)
}
cat("rho1 inducido, m = 21:", round(rho1_promedio(21), 4), " fórmula cerrada:", round((21^2 - 1) / (2 * (2 * 21^2 + 1)), 4), "\n")
cat("distancia en errores estándar (1/sqrt(137)):", round((rho1_promedio(21) - a[1]) * sqrt(137), 2), "\n")
