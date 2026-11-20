# ARMA(1,1) con phi = 0.6 y theta = 0.7, ambos POSITIVOS
set.seed(2026)
x <- arima.sim(model = list(ar = 0.6, ma = 0.7), n = 600)
write.csv(data.frame(x = as.numeric(x)), "serie.csv", row.names = FALSE)

arima(x, order = c(1, 0, 1), include.mean = FALSE)
#> Coefficients:
#>          ar1     ma1
#>       0.5999  0.6925
#> s.e.  0.0364  0.0355
#>
#> sigma^2 estimated as 0.9992:  log likelihood = -852.03,  aic = 1710.05

# ma1 sale POSITIVO: convenio de suma, el mismo del capitulo.
# La ayuda de ?arima imprime la ecuacion con signos + en la parte MA y
# advierte que por eso sus coeficientes tienen el signo contrario a los
# de la documentacion de S-PLUS.

# En R no hay asimetria: arima.sim() y arima() hablan el mismo idioma,
# el de los COEFICIENTES del modelo. Lo que se pone es lo que sale.