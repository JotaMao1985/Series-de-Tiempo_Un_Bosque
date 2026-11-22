library(forecast)

# Con d = 0 la constante es la MEDIA, y R la llama "intercept"
f0 <- arima(Nile, order = c(1, 0, 1), method = "ML")
round(coef(f0), 4)
#>      ar1      ma1 intercept
#>   0.8610  -0.5177  920.7037     <- es la media, no una ordenada al origen

# Con d = 1, stats::arima IGNORA include.mean sin avisar:
f1a <- arima(Nile, order = c(1, 1, 1), include.mean = TRUE, method = "ML")
names(coef(f1a))
#> [1] "ar1" "ma1"            no hay constante por ningun lado

# Para pedirla hay que usar forecast::Arima con include.drift
f1b <- Arima(Nile, order = c(1, 1, 1), include.drift = TRUE)
round(c(coef(f1b)[["drift"]], sqrt(diag(f1b$var.coef))[["drift"]]), 4)
#> [1] -2.8827  2.0167
round(coef(f1b)[["drift"]] / sqrt(diag(f1b$var.coef))[["drift"]], 3)
#> [1] -1.429                   no significativa

round(c(con_deriva = f1b$aicc, sin_deriva = Arima(Nile, order = c(1,1,1))$aicc), 3)
#> con_deriva sin_deriva
#>   1268.063   1267.507     anadirla empeora el AICc

# Con d = 2 forecast se NIEGA a ajustarla (y lo dice)
f2 <- Arima(Nile, order = c(1, 2, 1), include.drift = TRUE)
#> Warning message:
#> In Arima(Nile, order = c(1, 2, 1), include.drift = TRUE) :
#>   No drift term fitted as the order of difference is 2 or more.
"drift" %in% names(coef(f2))
#> [1] FALSE