library(forecast); library(tsibbledata)
x <- ts(log(pelt$Hare), start = 1845); n <- length(x)   # 91
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }

# --- (a) las pruebas ------------------------------------------------------
c(kpss = ndiffs(x, test = "kpss"), adf = ndiffs(x, test = "adf"), pp = ndiffs(x, test = "pp"))

# --- (b) la varianza y r1 -------------------------------------------------
round(sapply(0:2, function(d) var(if (d == 0) x else diff(x, differences = d))), 4)
r1 <- acf(x, plot = FALSE)$acf[2]
round(c(r1 = r1, cociente = var(diff(x)) / var(x), dos_por_1_menos_r1 = 2 * (1 - r1),
        r1_de_la_diferencia = acf(diff(x), plot = FALSE)$acf[2]), 3)

# --- (c) las raices MA de cuatro modelos con d = 1 ------------------------
for (o in list(c(0, 1, 1), c(1, 1, 1), c(2, 1, 1), c(3, 1, 1))) {
  f <- arima(x, order = o, method = "ML")
  cat(sprintf("ARIMA(%d,1,%d)  theta = %7.4f  |raiz MA| = %7.4f  AICc = %.2f\n", o[1], o[3],
      coef(f)[["ma1"]], Mod(polyroot(c(1, coef(f)[["ma1"]]))), aicc(f, n - 1)))
}

# --- (d) sin diferenciar --------------------------------------------------
for (p in c(2, 4)) {
  f <- arima(x, order = c(p, 0, 0), method = "ML")
  cat(sprintf("AR(%d)  AICc = %.2f  LB(20) p = %.4f  |raiz AR| menor = %.4f\n", p, aicc(f, n),
      Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = p)$p.value,
      min(Mod(polyroot(c(1, -coef(f)[1:p]))))))
}
as.character(auto.arima(x, stepwise = FALSE, approximation = FALSE))
