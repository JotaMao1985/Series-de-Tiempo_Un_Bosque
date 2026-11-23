library(forecast)

lap <- log(AirPassengers)                  # 144 meses, 1949-1960
length(lap)
#> [1] 144

# El mejor ARIMA NO estacional, con busqueda exhaustiva (p + q <= 5 por defecto)
mejor <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
as.character(mejor)
#> [1] "ARIMA(0,1,5)"

# Su diagnostico: lo que sobra en los residuales esta en los rezagos 12 y 24
res <- residuals(mejor)
r <- Acf(res, lag.max = 24, plot = FALSE)$acf[-1]
round(c(rho12 = r[12], rho24 = r[24], banda = 1.96 / sqrt(length(res))), 4)
#>  rho12  rho24  banda
#> 0.7245 0.6727 0.1633
lb <- Box.test(res, lag = 24, type = "Ljung-Box", fitdf = 5)   # fitdf = p + q
round(unname(lb$statistic), 1)
#> [1] 222.4
lb$p.value < 1e-6
#> [1] TRUE

# Subir el tope de p y q no lo arregla
amplio <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE,
                     max.p = 8, max.q = 8, max.order = 16)
as.character(amplio)
#> [1] "ARIMA(8,1,3) with drift"
round(Acf(residuals(amplio), lag.max = 24, plot = FALSE)$acf[13], 3)
#> [1] 0.437

# El modelo estacional "airline" del Capitulo 5, solo como avance
airline <- Arima(lap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
res2 <- residuals(airline)
round(c(rho12 = Acf(res2, lag.max = 24, plot = FALSE)$acf[13],
        lb24_p = Box.test(res2, lag = 24, type = "Ljung-Box", fitdf = 2)$p.value), 4)
#>   rho12  lb24_p
#> -0.0515  0.2330

# Los AICc no se comparan: sus verosimilitudes usan distinto numero de datos
c(no_estacional = mejor$nobs, airline = airline$nobs)
#> no_estacional       airline
#>           143           131