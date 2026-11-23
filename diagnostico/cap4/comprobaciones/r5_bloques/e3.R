library(forecast)
f  <- Arima(BJsales, order = c(1, 1, 1))
ph <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2)
H  <- 12

# --- (a) el limite de los psi, antes de expandir nada ---------------------
round(c(phi = ph, theta = th, limite = (1 + th) / (1 - ph)), 4)

# --- (b) el intervalo, a mano ---------------------------------------------
# ARIMA(1,1,1) = ARMA(2,1) con ar* = (1 + phi, -phi)
psi     <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = H))
sigma_h <- s * sqrt(cumsum(psi^2))[1:H]
round(psi[1:5], 4)
round(sigma_h[1:5], 4)

fc <- forecast(f, h = H, level = 95)
semi <- as.numeric((fc$upper - fc$lower) / 2)
round(semi[1:5], 4)
max(abs(semi - qnorm(0.975) * sigma_h))    # identicos salvo error de maquina

# --- (c) ¿crece como una caminata aleatoria? ------------------------------
# En un ARIMA(0,1,0) todos los psi valen 1 y sigma_h = sigma*sqrt(h): esa es la referencia
round(c(sigma_12_sobre_sigma_1 = sigma_h[H] / sigma_h[1], raiz_de_12 = sqrt(H),
        frente_a_la_caminata   = sigma_h[H] / (s * sqrt(H))), 4)
round(c(psi_12 = psi[H + 1], limite = (1 + th) / (1 - ph)), 4)
