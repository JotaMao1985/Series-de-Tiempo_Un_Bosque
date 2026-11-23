library(forecast)
ap <- log(AirPassengers)

# Rejilla con d = 1 y D = 1 FIJOS: es la condicion para que el AICc compare.
res <- data.frame()
for (p in 0:2) for (q in 0:2) for (P in 0:1) for (Q in 0:1) {
  f <- tryCatch(Arima(ap, order = c(p,1,q),
                      seasonal = list(order = c(P,1,Q), period = 12), method = "ML"),
                error = function(e) NULL)
  if (is.null(f)) next
  res <- rbind(res, data.frame(
    modelo = sprintf("(%d,1,%d)(%d,1,%d)[12]", p, q, P, Q),
    k = p+q+P+Q, nobs = f$nobs, aicc = f$aicc, bic = f$bic,
    lb = Box.test(residuals(f), lag = 24, type = "Ljung-Box",
                  fitdf = p+q+P+Q)$p.value))
}
salida <- head(res[order(res$aicc), ], 4)
salida[, c("aicc", "bic", "lb")] <- round(salida[, c("aicc", "bic", "lb")], 4)
salida
#>                modelo k nobs      aicc       bic     lb
#> 6  (0,1,1)(0,1,1)[12] 2  131 -483.2101 -474.7735 0.2330
#> 30 (2,1,1)(0,1,1)[12] 4  131 -481.7923 -467.8963 0.1371
#> 8  (0,1,1)(1,1,1)[12] 3  131 -481.5957 -470.4123 0.2271
#> 18 (1,1,1)(0,1,1)[12] 3  131 -481.5820 -470.3987 0.2453
unique(res$nobs)      # todos iguales: la comparacion es legitima
#> [1] 131

# Diagnostico del ganador, con 2m rezagos
fit <- Arima(ap, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
round(Box.test(residuals(fit), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4)
#> [1] 0.233
round(Box.test(residuals(fit), lag = 36, type = "Ljung-Box", fitdf = 2)$p.value, 4)
#> [1] 0.2969
round(shapiro.test(residuals(fit))$p.value, 4)
#> [1] 0.1674

# Barra por barra en los rezagos que importan
r <- Acf(residuals(fit), lag.max = 36, plot = FALSE)$acf
round(c(r12 = r[13], r24 = r[25], banda = 1.96/sqrt(length(ap))), 4)
#>     r12     r24   banda
#> -0.0515  0.0124  0.1633