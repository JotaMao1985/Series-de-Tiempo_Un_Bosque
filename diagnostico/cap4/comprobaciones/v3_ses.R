# V3 · ¿el α = 1 + θ̂ = 0.267 del IMA(1,1) es el α que devuelve ses()/ets()?
suppressMessages(library(forecast))
ma1 <- arima(Nile, order = c(0, 1, 1), method = "ML")
cat("IMA(1,1) ML: theta =", round(coef(ma1)[["ma1"]], 4), " alfa implícito 1+theta =", round(1 + coef(ma1)[["ma1"]], 4), "\n")
s <- ses(Nile, h = 3); cat("ses(Nile): alpha =", round(s$model$par[["alpha"]], 4), " l0 =", round(s$model$par[["l"]], 1), " pronóstico h=1:", round(s$mean[1], 2), "\n")
e <- ets(Nile, model = "ANN"); cat("ets(ANN): alpha =", round(e$par[["alpha"]], 4), "\n")
cat("pronóstico h=1 del IMA(1,1):", round(forecast(ma1, h = 1)$mean[1], 2), "\n")
# la equivalencia es de modelo: con alfa fijo = 1+theta el pronóstico SES a 1 paso coincide con el del IMA(1,1) (salvo inicialización)
s2 <- ses(Nile, alpha = 1 + coef(ma1)[["ma1"]], h = 1, initial = "simple"); cat("ses con alpha = 1+theta (inicial simple): h=1:", round(s2$mean[1], 2), "\n")
