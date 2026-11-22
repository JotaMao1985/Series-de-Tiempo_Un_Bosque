# Verificación independiente de la R1 del capítulo 4 (cifras nuevas o cambiadas)
# Rscript diagnostico/cap4/comprobaciones/v1_comprobaciones.R > .../v1_comprobaciones.out 2>&1
suppressPackageStartupMessages({ library(forecast); library(tseries) })
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")), "\n")
raiz <- function(p) min(Mod(polyroot(p)))
sec <- function(t) cat("\n=====", t, "=====\n")

sec("M1 · razón sin MA (32.8)")
set.seed(2026); w0 <- arima.sim(list(ar = 0.2544), n = 200)
print(round(var(cumsum(w0)) / var(w0), 1))

sec("M2 · residual 1 de R y coeficientes (para cotejar con statsmodels)")
aj <- arima(Nile, order = c(1, 1, 1), method = "ML")
print(round(coef(aj), 6)); print(round(residuals(aj)[1:3], 4))
print(Box.test(residuals(aj), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value)
print(Box.test(residuals(aj)[-1], lag = 20, type = "Ljung-Box", fitdf = 2)$p.value)

sec("M3 · cociente de varianzas, 2(1-r1), r1 de las diferencias")
r1 <- acf(Nile, plot = FALSE)$acf[2]
print(round(c(r1 = r1, cociente = var(diff(Nile)) / var(Nile), dos = 2 * (1 - r1)), 4))
print(round(sapply(1:3, function(d) acf(diff(Nile, differences = d), plot = FALSE)$acf[2]), 4))
print(round(sapply(0:3, function(d) var(if (d == 0) Nile else diff(Nile, differences = d))), 2))
# raíces MA: ARIMA(1,1,1) y MA(1) sobre la diferencia
cat("raiz MA (1,1,1):", round(raiz(c(1, coef(aj)["ma1"])), 4),
    " raiz MA de MA(1) con d=1:", round(raiz(c(1, coef(arima(Nile, c(0,1,1), method="ML"))["ma1"])), 4), "\n")
cat("ACF Nile lags 1..20:\n"); print(round(acf(Nile, lag.max = 20, plot = FALSE)$acf[-1], 4))
cat("banda:", round(1.96 / sqrt(100), 4), "\n")

sec("M3 · Monte Carlo con raíz unitaria verdadera (réplica del genera_cap4.R y otra semilla)")
mc <- function(seed, phi = 0.2544, th = -0.8741, R = 1000) {
  set.seed(seed); pp <- 0; adf <- 0
  for (i in seq_len(R)) {
    x <- 900 + cumsum(arima.sim(list(ar = phi, ma = th), n = 100))
    if (suppressWarnings(PP.test(x)$p.value) < 0.05) pp <- pp + 1
    if (suppressWarnings(adf.test(x, k = 4)$p.value) < 0.05) adf <- adf + 1
  }
  c(pp = pp / R, adf = adf / R)
}
print(mc(2026)); print(mc(7))
cat("phi, theta redondeados del ajuste:", round(coef(aj), 4), "\n")

sec("M5 · Arima con deriva")
f1b <- Arima(Nile, order = c(1, 1, 1), include.drift = TRUE)
print(round(coef(f1b), 4)); print(round(sqrt(diag(f1b$var.coef)), 4))
cat("c = delta(1-phi):", round(coef(f1b)[["drift"]] * (1 - coef(f1b)[["ar1"]]), 3), "\n")

sec("M5/M9 · media del ARIMA(1,0,1): arima ML, Arima CSS-ML, Arima ML")
print(round(c(arima_ML = coef(arima(Nile, c(1,0,1), method = "ML"))[["intercept"]],
              Arima_CSSML = coef(Arima(Nile, c(1,0,1)))[["intercept"]],
              Arima_ML = coef(Arima(Nile, c(1,0,1), method = "ML"))[["intercept"]]), 2))

sec("M7 · ARIMA(2,1,2) con CSS-ML y ML (Arima y stats::arima)")
for (m in c("CSS-ML", "ML")) {
  a <- Arima(Nile, order = c(2, 1, 2), method = m)
  cat(sprintf("Arima %-6s logL = %.3f  min|raiz AR| = %.4f  min|raiz MA| = %.4f  AICc = %.2f\n", m, a$loglik,
              raiz(c(1, -coef(a)[c("ar1", "ar2")])), raiz(c(1, coef(a)[c("ma1", "ma2")])), a$aicc))
}
b <- arima(Nile, order = c(2, 1, 2), method = "ML")
cat(sprintf("stats::arima ML logL = %.3f  min|raiz AR| = %.4f\n", b$loglik, raiz(c(1, -coef(b)[c("ar1","ar2")]))))
cat("umbral: 1.0009 < 1.001 ?", raiz(c(1, -coef(Arima(Nile, c(2,1,2)))[c("ar1","ar2")])) < 1.001, "\n")

sec("M7/M9/E3 · sigma^2: arima ML, Arima CSS-ML, Arima ML; razón 99/97")
s_ml <- arima(Nile, c(1,1,1), method = "ML")$sigma2
a_css <- Arima(Nile, c(1,1,1)); a_ml <- Arima(Nile, c(1,1,1), method = "ML")
print(round(c(arima_ML = s_ml, Arima_CSSML = a_css$sigma2, Arima_ML = a_ml$sigma2,
              arimaML_x_99_97 = s_ml * 99 / 97, SCR_97 = sum(residuals(a_css)^2) / 97,
              SCR_ml_99 = sum(residuals(aj)^2) / 99), 2))
cat("dif relativa:", round((a_css$sigma2 - s_ml) / s_ml, 5), " 2/97 =", round(2/97, 5), "\n")
cat("diferencia de coeficientes CSS-ML vs ML:", signif(coef(a_css) - coef(aj), 3), "\n")

sec("M9 · forma del ARIMA(1,1,1) sin constante")
f1 <- Arima(Nile, order = c(1, 1, 1))
ph <- coef(f1)[["ar1"]]; th1 <- coef(f1)[["ma1"]]
yT <- 740; dyT <- 740 - as.numeric(Nile)[99]; eT <- tail(as.numeric(residuals(f1)), 1)
fc <- forecast(f1, h = 60)$mean
print(round(c(h1 = fc[1], h2 = fc[2], h3 = fc[3], h30 = fc[30], h60 = fc[60],
              limite = yT + (ph * dyT + th1 * eT) / (1 - ph)), 2))
# fórmula de la diferencia pronosticada
dh <- sapply(1:5, function(h) ph^(h - 1) * (ph * dyT + th1 * eT))
print(round(rbind(formula = dh, forecast = diff(c(yT, fc[1:5]))), 4))

sec("M10 · TRM desde la copia fija")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
rw <- arima(trm, order = c(0, 1, 0), method = "ML"); s <- sqrt(rw$sigma2)
d1 <- diff(trm); d12 <- diff(trm, lag = 12); z <- qnorm(0.975); h <- c(1, 3, 6, 12, 24)
yTt <- tail(as.numeric(trm), 1)
print(round(cbind(h, inf = yTt - z * s * sqrt(h), sup = yTt + z * s * sqrt(h)), 4))
fcw <- forecast(rw, h = 24, level = 95); print(max(abs(fcw$upper[h] - (yTt + z * s * sqrt(h)))))
asim <- function(x) mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5
cat("asimetria d1:", round(asim(d1), 4), " residuales:", round(asim(residuals(rw)[-1]), 4), "\n")
cat("cubre 80% a un mes:", round(mean(abs(d1) <= qnorm(0.90) * s), 4), "\n")
print(round(sapply(c(3, 6, 12), function(h) mean(diff(trm, lag = h)^2) / (h * s^2)), 4))
cat("rho1 d1:", round(acf(d1, plot = FALSE)$acf[2], 4), "\n")
cat("razon teorica 1 + 2 rho1 (h-1)/h:", round(1 + 2 * acf(d1, plot = FALSE)$acf[2] * (c(3,6,12) - 1) / c(3,6,12), 4), "\n")
cat("fuera 12:", sum(abs(d12) > z * s * sqrt(12)), "de", length(d12), "\n")
cat("residual 1 de R (TRM):", round(residuals(rw)[1], 3), "\n")

sec("E1 · BJsales")
print(round(sapply(1:2, function(d) acf(diff(BJsales, differences = d), plot = FALSE)$acf[2]), 4))

sec("E2 · log(lynx)")
ly <- log(lynx); r1l <- acf(ly, plot = FALSE)$acf[2]
print(round(c(r1 = r1l, cociente = var(diff(ly)) / var(ly), dos = 2 * (1 - r1l)), 4))
cat("r1 de diff(log lynx), d = 1 y 2:", round(sapply(1:2, function(d) acf(diff(ly, differences = d), plot = FALSE)$acf[2]), 4), "\n")
f211 <- Arima(ly, order = c(2, 1, 1)); cat("ARIMA(2,1,1) log lynx |raiz MA|:", round(raiz(c(1, coef(f211)["ma1"])), 4), "\n")
cat("ndiffs:", sapply(c("kpss","adf","pp"), function(t) ndiffs(ly, test = t)), "\n")

sec("Quiz 4 · deriva, c y media muestral de diferencias")
print(round(c(deriva = coef(f1b)[["drift"]], c = coef(f1b)[["drift"]] * (1 - coef(f1b)[["ar1"]]),
              media_dif = mean(diff(Nile))), 3))

sec("M7 · AIC de R del ARIMA(1,1,1) (para la nota del bloque de Python)")
cat("AIC R:", round(AIC(arima(Nile, c(1,1,1), method = "ML")), 3), "\n")
