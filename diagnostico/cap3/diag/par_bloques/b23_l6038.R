aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
n <- length(lh)   # 48

round(1.96 / sqrt(n), 4)
#> [1] 0.2829                       banda ancha: solo el rezago 1 se sale

round(acf(lh,  lag.max = 6, plot = FALSE)$acf[-1], 4)
#> [1]  0.5755  0.1818 -0.1448 -0.1748 -0.1497 -0.0210
# pacf()$acf devuelve un array de tres dimensiones y se imprime como tal:
# as.numeric() lo aplana para poder leerlo de un vistazo
round(as.numeric(pacf(lh, lag.max = 6, plot = FALSE)$acf), 4)
#> [1]  0.5755 -0.2234 -0.2269  0.1028 -0.0759  0.0676

# Las dos se cortan aparentemente en el rezago 1: candidatos AR(1) y MA(1),
# y conviene probar algo mas por si acaso.
for (pq in list(c(1,0), c(2,0), c(3,0), c(0,1), c(0,2), c(1,1))) {
  f <- arima(lh, order = c(pq[1], 0, pq[2]), method = "ML")
  cat(sprintf("ARMA(%d,%d)  AICc=%7.3f  BIC=%7.3f  LB(10) p=%.4f\n",
      pq[1], pq[2], aicc(f, n), BIC(f),
      Box.test(residuals(f), lag = 10, type = "Ljung-Box",
               fitdf = sum(pq))$p.value))
}
#> ARMA(1,0)  AICc= 65.304  BIC= 70.372  LB(10) p=0.4050
#> ARMA(2,0)  AICc= 65.434  BIC= 71.989  LB(10) p=0.4185
#> ARMA(3,0)  AICc= 65.613  BIC= 73.541  LB(10) p=0.7958
#> ARMA(0,1)  AICc= 68.649  BIC= 73.717  LB(10) p=0.1962
#> ARMA(0,2)  AICc= 63.991  BIC= 70.545  LB(10) p=0.8492   <- min AICc
#> ARMA(1,1)  AICc= 66.454  BIC= 73.009  LB(10) p=0.3927

# El BIC prefiere el AR(1): 70.372 frente a 70.545. Diferencia de 0.17,
# practicamente un empate.
ar1 <- arima(lh, order = c(1, 0, 0), method = "ML")
round(c(phi = coef(ar1)[["ar1"]], ee = sqrt(ar1$var.coef[1,1]),
        media = coef(ar1)[["intercept"]]), 4)
#>    phi     ee  media
#> 0.5739 0.1161 2.4133

shapiro.test(residuals(ar1))$p.value
#> [1] 0.008348901   <- la normalidad SI se rechaza