library(forecast)

# trace = TRUE imprime CADA modelo evaluado y su AICc: la caja se abre sola
ajuste <- auto.arima(Nile, trace = TRUE, seasonal = FALSE)
#>  ARIMA(2,1,2) with drift         : Inf
#>  ARIMA(0,1,0) with drift         : 1298.77
#>  ARIMA(1,1,0) with drift         : 1283.598
#>  ARIMA(0,1,1) with drift         : 1270.562
#>  ARIMA(0,1,0)                    : 1296.738
#>  ARIMA(1,1,1) with drift         : 1268.063
#>  ...
#>  Best model: ARIMA(1,1,1)

as.character(ajuste)
#> [1] "ARIMA(1,1,1)"
round(ajuste$aicc, 3)
#> [1] 1267.507

# La busqueda COMPLETA: mas lenta, pero sin vecindarios
completo <- auto.arima(Nile, stepwise = FALSE, approximation = FALSE,
                       seasonal = FALSE)
c(escalonada = as.character(ajuste), exhaustiva = as.character(completo))
#>     escalonada     exhaustiva
#> "ARIMA(1,1,1)" "ARIMA(1,1,1)"      coinciden

# Cuantos modelos evalua cada una (las lineas "ARIMA(...) : AICc" de la traza)
n_modelos <- function(...)
  sum(grepl("^ ARIMA.*:", capture.output(invisible(auto.arima(...)))))
c(escalonada = n_modelos(Nile, trace = TRUE, seasonal = FALSE),
  exhaustiva = n_modelos(Nile, trace = TRUE, seasonal = FALSE,
                         stepwise = FALSE, approximation = FALSE))
#> escalonada exhaustiva
#>         18         42