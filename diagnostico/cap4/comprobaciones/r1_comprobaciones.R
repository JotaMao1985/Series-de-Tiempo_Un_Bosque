# R1 del capítulo 4 · comprobaciones de cada cifra nueva o corregida (2026-11-22)
# Uso, desde la raíz del repositorio:
#   Rscript diagnostico/cap4/comprobaciones/r1_comprobaciones.R > diagnostico/cap4/comprobaciones/r1_comprobaciones.out 2>&1
suppressPackageStartupMessages({library(forecast); library(tseries)})
cat("R", R.version$major, R.version$minor, "· forecast", as.character(packageVersion("forecast")),
    "· tseries", as.character(packageVersion("tseries")), "\n\n")

y <- Nile

cat("== [E1 · M9] ARIMA(1,1,1) sin constante: de 740 a 816.18 y se aplana en 842.17\n")
f <- Arima(y, order = c(1, 1, 1))
fc <- forecast(f, h = 30)
cat("ultimo observado:", tail(y, 1), "· h = 1, 2, 3, 10, 30:", round(fc$mean[c(1, 2, 3, 10, 30)], 2), "\n")
phi <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; e <- as.numeric(tail(residuals(f), 1))
lim <- y[100] + (phi * (y[100] - y[99]) + th * e) / (1 - phi)
cat("limite y_T + (phi*dy_T + theta*e_T)/(1-phi):", round(lim, 2), "\n")
cat("primer h con |m_h - limite| < 0.005:", which(abs(as.numeric(fc$mean) - lim) < 0.005)[1], "\n\n")

cat("== [E2 · varianza] el cociente de varianzas repite r1 (cap. 2, c2-m7-08)\n")
cociente <- function(x) var(diff(x)) / var(x)
r1 <- function(x) acf(x, plot = FALSE)$acf[2]
for (nm in c("Nile", "log(lynx)", "BJsales")) {
  x <- switch(nm, Nile = Nile, "log(lynx)" = log(lynx), BJsales = BJsales)
  cat(sprintf("%-10s r1 = %.4f · 2(1 - r1) = %.4f · Var(dy)/Var(y) = %.4f\n",
              nm, r1(x), 2 * (1 - r1(x)), cociente(x)))
}
cat("r1 de la serie diferenciada (sintoma de sobrediferenciar si se acerca a -0.5):\n")
for (nm in c("Nile", "log(lynx)", "BJsales")) {
  x <- switch(nm, Nile = Nile, "log(lynx)" = log(lynx), BJsales = BJsales)
  cat(sprintf("  %-10s d = 1: %.4f · d = 2: %.4f\n", nm,
              r1(diff(x)), r1(diff(x, differences = 2))))
}
cat("\n")

cat("== [I · M2] raiz MA unitaria con pareja AR: el ARIMA(2,1,2) de la TRM\n")
dat <- read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
trm <- ts(dat$trm, start = c(2015, 1), frequency = 12)
f212 <- arima(trm, order = c(2, 1, 2), method = "ML")
cat("AR:", round(Mod(polyroot(c(1, -coef(f212)[1:2]))), 4),
    "· MA:", round(Mod(polyroot(c(1, coef(f212)[3:4]))), 4), "\n\n")

cat("== [I · sigma2] arima(ML) frente a Arima(): el factor 99/97\n")
a_ml <- arima(y, order = c(1, 1, 1), method = "ML")
A_def <- Arima(y, order = c(1, 1, 1))
A_ml <- Arima(y, order = c(1, 1, 1), method = "ML")
ssr <- sum(residuals(A_def)^2)
cat(sprintf("arima ML sigma2 = %.2f · Arima defecto (CSS-ML) = %.2f · Arima method='ML' = %.2f\n",
            a_ml$sigma2, A_def$sigma2, A_ml$sigma2))
cat(sprintf("razon Arima/arima = %.5f · 99/97 = %.5f\n", A_def$sigma2 / a_ml$sigma2, 99 / 97))
cat(sprintf("SCR = %.2f · SCR/97 = %.2f · SCR/99 = %.2f\n", ssr, ssr / 97, ssr / 99))
cat("codigo de forecast::Arima que reescala sigma2:\n")
cat(grep("sigma2", deparse(forecast::Arima), value = TRUE), sep = "\n")
cat(sprintf("BJsales ARIMA(1,1,1): arima ML sigma2 = %.4f · Arima = %.4f · razon = %.5f · 149/147 = %.5f\n\n",
            arima(BJsales, order = c(1, 1, 1), method = "ML")$sigma2,
            Arima(BJsales, order = c(1, 1, 1))$sigma2,
            Arima(BJsales, order = c(1, 1, 1))$sigma2 / arima(BJsales, order = c(1, 1, 1), method = "ML")$sigma2,
            149 / 147))

cat("== [I · M7] ARIMA(2,1,2) del Nilo segun el estimador\n")
for (m in c("CSS-ML", "ML")) {
  a <- Arima(y, order = c(2, 1, 2), method = m)
  cat(sprintf("%-6s logL = %.3f · AICc = %.2f · min|raiz AR| = %.4f · min|raiz MA| = %.4f\n", m,
              a$loglik, a$aicc, min(Mod(polyroot(c(1, -coef(a)[c("ar1", "ar2")])))),
              min(Mod(polyroot(c(1, coef(a)[c("ma1", "ma2")]))))))
}
a2 <- arima(y, order = c(2, 1, 2), method = "ML")
cat(sprintf("stats::arima ML: logL = %.3f · min|raiz AR| = %.4f\n\n", a2$loglik,
            min(Mod(polyroot(c(1, -coef(a2)[c("ar1", "ar2")]))))))

cat("== [I · quiz 4] deriva frente a c y a la media muestral de las diferencias\n")
g <- Arima(y, order = c(1, 1, 1), include.drift = TRUE)
print(round(coef(g), 4))
cat("c = drift*(1-phi):", round(coef(g)[["drift"]] * (1 - coef(g)[["ar1"]]), 2),
    "· media de las diferencias:", round(mean(diff(y)), 2), "\n\n")

cat("== [M · M9] ARIMA(1,0,1): la 'media' segun el estimador\n")
cat("Arima (CSS-ML):", round(coef(Arima(y, order = c(1, 0, 1)))[["intercept"]], 4),
    "· arima ML:", round(coef(arima(y, order = c(1, 0, 1), method = "ML"))[["intercept"]], 4), "\n\n")

cat("== [N1 · M3] Monte Carlo: PP y ADF con raiz unitaria verdadera (replica de verifica_directo_r46_cap4.R)\n")
set.seed(2026)
B <- 1000; rej_pp <- 0; rej_adf <- 0
for (b in seq_len(B)) {
  x <- 900 + cumsum(arima.sim(list(ar = 0.2544, ma = -0.8741), n = 100))
  if (suppressWarnings(PP.test(x)$p.value) < 0.05) rej_pp <- rej_pp + 1
  if (suppressWarnings(adf.test(x, k = 4)$p.value) < 0.05) rej_adf <- rej_adf + 1
}
cat("PP rechaza:", rej_pp / B, "· adf.test(k = 4) rechaza:", rej_adf / B, "\n\n")

cat("== [N2-N4 · M9/M10] TRM: cobertura del 80 % a un mes, asimetria, razon de cuadrados medios\n")
rw <- arima(trm, order = c(0, 1, 0), method = "ML")
s <- sqrt(rw$sigma2); d1 <- diff(trm)
cat("cubre el 80 % a un mes:", round(mean(abs(d1) <= qnorm(0.90) * s), 4),
    "(", sum(abs(d1) <= qnorm(0.90) * s), "de", length(d1), ")\n")
asim <- function(x) mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5
cat("asimetria de los cambios mensuales:", round(asim(d1), 4),
    "· de los residuales:", round(asim(residuals(rw)), 4), "\n")
razon <- sapply(c(3, 6, 12), function(h) mean(diff(trm, lag = h)^2) / (h * s^2))
cat("cuadrado medio de los cambios a h = 3, 6, 12 / (h sigma2):", round(razon, 4), "\n")
r1t <- acf(d1, plot = FALSE)$acf[2]
cat("con solo rho1 =", round(r1t, 4), ": 1 + 2 rho1 (h-1)/h =",
    round(1 + 2 * r1t * (c(3, 6, 12) - 1) / c(3, 6, 12), 4), "\n")
cat("cobertura del 95 % a 12 meses dentro de la muestra:",
    round(mean(abs(diff(trm, lag = 12)) <= qnorm(0.975) * s * sqrt(12)), 4), "\n\n")

cat("== [M · M10] efecto Working: rho1 de los cambios del promedio mensual de una caminata diaria\n")
set.seed(2026)
m <- 21; meses <- 4000
x <- cumsum(rnorm(m * meses))
prom <- colMeans(matrix(x, nrow = m))
cat("rho1 simulado (m = 21):", round(acf(diff(prom), plot = FALSE)$acf[2], 4),
    "· limite teorico (m^2 - 1)/(2(2m^2 + 1)):", round((m^2 - 1) / (2 * (2 * m^2 + 1)), 4), "\n")
cat("rho1 de la TRM:", round(r1t, 4), "· e.e. aprox 1/sqrt(137):", round(1 / sqrt(137), 4), "\n")
