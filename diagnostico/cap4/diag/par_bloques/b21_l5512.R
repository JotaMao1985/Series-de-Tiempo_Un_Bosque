library(forecast); library(tseries)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
n <- length(BJsales)   # 150

# --- Etapa 1: d ---------------------------------------------------------
round(sapply(0:3, function(d) var(if (d == 0) BJsales else diff(BJsales, differences = d))), 4)
#> [1] 461.3769   2.0851   2.8823   8.5626      minimo en d = 1
round(c(adf = adf.test(BJsales)$p.value, ndiffs = ndiffs(BJsales)), 4)
#>    adf ndiffs
#> 0.5302 1.0000

# --- Etapa 2: la rejilla con d = 1 --------------------------------------
for (q in 0:2) for (p in 0:2) {
  f <- arima(BJsales, order = c(p, 1, q), method = "ML")
  cat(sprintf("ARIMA(%d,1,%d)  AICc=%8.3f  BIC=%8.3f  LB(20) p=%.4f\n", p, q,
      aicc(f, n - 1), BIC(f),
      Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = p + q)$p.value))
}
#> ARIMA(0,1,0)  AICc= 545.544  BIC= 548.521  LB(20) p=0.0000
#> ARIMA(1,1,0)  AICc= 526.209  BIC= 532.134  LB(20) p=0.1830
#> ARIMA(2,1,0)  AICc= 520.088  BIC= 528.935  LB(20) p=0.2627
#> ARIMA(0,1,1)  AICc= 533.348  BIC= 539.274  LB(20) p=0.0340   <- RECHAZA
#> ARIMA(1,1,1)  AICc= 514.902  BIC= 523.748  LB(20) p=0.6216   <- min AICc y BIC
#> ARIMA(2,1,1)  AICc= 516.922  BIC= 528.660  LB(20) p=0.5576
#> ARIMA(0,1,2)  AICc= 527.856  BIC= 536.702  LB(20) p=0.1346
#> ARIMA(1,1,2)  AICc= 516.914  BIC= 528.652  LB(20) p=0.5592
#> ARIMA(2,1,2)  AICc= 518.575  BIC= 533.175  LB(20) p=0.4613

# --- Etapa 3: por que falla el de libro ---------------------------------
f011 <- arima(BJsales, order = c(0, 1, 1), method = "ML")
round(as.numeric(acf(residuals(f011), lag.max = 4, plot = FALSE)$acf)[-1], 4)
#> [1] 0.0142 0.2483 0.1185 0.2087
round(1.96 / sqrt(length(residuals(f011))), 4)   # residuals() devuelve 150
#> [1] 0.16
# los rezagos 2 y 4 se salen holgadamente: queda estructura AR

f111 <- arima(BJsales, order = c(1, 1, 1), method = "ML")
round(c(phi = coef(f111)[["ar1"]], ee_phi = sqrt(f111$var.coef[1,1]),
        theta = coef(f111)[["ma1"]], ee_theta = sqrt(f111$var.coef[2,2])), 4)
#>     phi  ee_phi   theta ee_theta
#>  0.8799  0.0644 -0.6415   0.1035
shapiro.test(residuals(f111))$p.value
#> [1] 0.6294597                    normalidad, sin problema

as.character(auto.arima(BJsales, stepwise = FALSE, approximation = FALSE))
#> [1] "ARIMA(1,1,1)"

# --- La comparacion que NO vale -----------------------------------------
f122 <- arima(BJsales, order = c(1, 2, 2), method = "ML")
round(c(d1 = aicc(f111, n - 1), d2 = aicc(f122, n - 2)), 3)
#>      d1      d2
#> 514.902 515.859
round(min(Mod(polyroot(c(1, coef(f122)[grepl("^ma", names(coef(f122)))])))), 4)
#> [1] 1