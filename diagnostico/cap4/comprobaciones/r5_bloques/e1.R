library(forecast); library(tseries)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
raiz_ma <- function(f) { ma <- coef(f)[grepl("^ma", names(coef(f)))]
                         if (length(ma)) sprintf("%.4f", min(Mod(polyroot(c(1, ma))))) else "   -  " }
n <- length(BJsales)   # 150

# --- (a) d ---------------------------------------------------------------
round(c(adf = adf.test(BJsales)$p.value, ndiffs = ndiffs(BJsales)), 4)
# sintomas de diferenciar de mas: r1 de la serie diferenciada una y dos veces
round(sapply(1:2, function(d) acf(diff(BJsales, differences = d), plot = FALSE)$acf[2]), 4)
# un indicio, no una regla (Modulo 2.7): con d = 1 no avisa; con d = 2 ronda -0.5

# --- (b) la rejilla, con d = 1 y con d = 2 -------------------------------
for (d in 1:2) for (q in 0:2) for (p in 0:2) {
  f <- arima(BJsales, order = c(p, d, q), method = "ML")
  cat(sprintf("ARIMA(%d,%d,%d)  AICc=%8.3f  BIC=%8.3f  LB(20) p=%.4f  |raiz MA|=%s\n", p, d, q,
      aicc(f, n - d), BIC(f),
      Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = p + q)$p.value, raiz_ma(f)))
}

# --- (b) por que falla el IMA(1,1) ---------------------------------------
f011 <- arima(BJsales, order = c(0, 1, 1), method = "ML")
round(as.numeric(acf(residuals(f011), lag.max = 4, plot = FALSE)$acf)[-1], 4)
round(1.96 / sqrt(length(residuals(f011))), 4)   # residuals() devuelve 150

# --- (c) el modelo que queda ----------------------------------------------
f111 <- arima(BJsales, order = c(1, 1, 1), method = "ML")
round(c(phi = coef(f111)[["ar1"]], ee_phi = sqrt(f111$var.coef[1,1]),
        theta = coef(f111)[["ma1"]], ee_theta = sqrt(f111$var.coef[2,2])), 4)
shapiro.test(residuals(f111))$p.value
as.character(auto.arima(BJsales, stepwise = FALSE, approximation = FALSE))

# --- (d) la comparacion que NO vale --------------------------------------
f122 <- arima(BJsales, order = c(1, 2, 2), method = "ML")
round(c(ima_d1 = aicc(f011, n - 1), mejor_d2 = aicc(f122, n - 2),
        diferencia = aicc(f011, n - 1) - aicc(f122, n - 2)), 3)
c(n_efectivo_d1 = n - 1, n_efectivo_d2 = n - 2)
round(rbind(coef = coef(f122), ee = sqrt(diag(f122$var.coef))), 4)
