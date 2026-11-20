set.seed(3)

# arima.sim descarta automaticamente un periodo de calentamiento (burn-in),
# asi que la serie que devuelve ya esta en regimen estacionario.
ar1   <- arima.sim(n = 200, model = list(ar = 0.8))
ma1   <- arima.sim(n = 200, model = list(ma = 0.8))
arma  <- arima.sim(n = 200, model = list(ar = 0.7, ma = 0.5))

par(mfrow = c(3, 3), mar = c(3, 4, 2, 1))
for (nm in c("ar1", "ma1", "arma")) {
  x <- get(nm)
  plot(x, main = nm, ylab = "")
  acf(x,  lag.max = 16, main = "ACF")
  pacf(x, lag.max = 16, main = "PACF")
}

# arima.sim EXIGE un modelo estacionario: si le pides una raiz unitaria falla
try(arima.sim(n = 100, model = list(ar = 1)))
#> Error in arima.sim(...) : 'ar' part of model is not stationary
# Para simular una caminata aleatoria hay que usar cumsum(rnorm(n)),
# como se hizo en el Capitulo 2.