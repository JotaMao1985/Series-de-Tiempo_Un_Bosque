library(forecast); library(tseries)

# ---- Etapa 1: identificacion --------------------------------------------
plot(Nile)                              # SIEMPRE lo primero
d <- ndiffs(Nile)                       # cuantas diferencias
w <- if (d == 0) Nile else diff(Nile, differences = d)
par(mfrow = c(1, 2)); acf(w); pacf(w); par(mfrow = c(1, 1))

# ---- Etapa 2: estimacion ------------------------------------------------
ajuste <- arima(Nile, order = c(1, d, 1), method = "ML")

# ---- Etapa 3: diagnostico -----------------------------------------------
res <- residuals(ajuste)
Box.test(res, lag = 20, type = "Ljung-Box", fitdf = 2)$p.value
#> [1] 0.7997371       > 0.05: no hay evidencia de estructura sobrante

# ---- Etapa 4: uso (con el MISMO ajuste de la etapa 2) -------------------
pron <- forecast(ajuste, h = 10)
round(as.numeric(pron$mean[1:3]), 2)
#> [1] 816.18 835.56 840.49