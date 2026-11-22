aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
n <- length(lh)   # 48

# La banda es ancha: solo el rezago 1 sale de ella en las dos funciones
round(1.96 / sqrt(n), 4)
round(acf(lh,  lag.max = 6, plot = FALSE)$acf[-1], 4)
# pacf()$acf devuelve un array de tres dimensiones y se imprime como tal:
# as.numeric() lo aplana para poder leerlo de un vistazo
round(as.numeric(pacf(lh, lag.max = 6, plot = FALSE)$acf), 4)

# Las dos se cortan aparentemente en el rezago 1: candidatos AR(1) y MA(1),
# y conviene probar algo mas por si acaso.
for (pq in list(c(1,0), c(2,0), c(3,0), c(0,1), c(0,2), c(1,1))) {
  f <- arima(lh, order = c(pq[1], 0, pq[2]), method = "ML")
  cat(sprintf("ARMA(%d,%d)  AICc=%7.3f  BIC=%7.3f  LB(10) p=%.4f\n",
      pq[1], pq[2], aicc(f, n), BIC(f),
      Box.test(residuals(f), lag = 10, type = "Ljung-Box",
               fitdf = sum(pq))$p.value))
}

# Los dos finalistas: el AR(1), minimo del BIC, y el MA(2), minimo del AICc
ar1 <- arima(lh, order = c(1, 0, 0), method = "ML")
ma2 <- arima(lh, order = c(0, 0, 2), method = "ML")
round(c(phi = coef(ar1)[["ar1"]], ee = sqrt(ar1$var.coef[1,1]),
        media = coef(ar1)[["intercept"]]), 4)
# El coeficiente de mayor orden del MA(2) y su estadistico t
round(c(theta2 = coef(ma2)[["ma2"]],
        t = coef(ma2)[["ma2"]] / sqrt(ma2$var.coef[2,2])), 4)

# La ACF teorica de cada uno frente a la muestral, rezagos 1 a 3
round(rbind(muestral = acf(lh, lag.max = 3, plot = FALSE)$acf[-1],
            AR1 = ARMAacf(ar = coef(ar1)[["ar1"]], lag.max = 3)[-1],
            MA2 = ARMAacf(ma = coef(ma2)[1:2], lag.max = 3)[-1]), 3)

# La normalidad de los residuales se rechaza en los dos
round(c(AR1 = shapiro.test(residuals(ar1))$p.value,
        MA2 = shapiro.test(residuals(ma2))$p.value), 4)

# La busqueda automatica del Modulo 9 tampoco se decide
library(forecast)
c(por_pasos  = as.character(auto.arima(lh)),
  exhaustiva = as.character(auto.arima(lh, stepwise = FALSE, approximation = FALSE)))
