library(forecast)
f  <- Arima(BJsales, order = c(1, 1, 1))
ph <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2)
H  <- 12

# ARIMA(1,1,1) = ARMA(2,1) con ar* = (1 + phi, -phi)
psi     <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = H))
sigma_h <- s * sqrt(cumsum(psi^2))[1:H]
round(psi[1:5], 4)
#> [1] 1.0000 1.2385 1.4485 1.6332 1.7958
round(sigma_h[1:5], 4)
#> [1] 1.3416 2.1356 2.8874 3.6246 4.3523

fc <- forecast(f, h = H, level = 95)
semi <- as.numeric((fc$upper - fc$lower) / 2)
round(semi[1:5], 4)
#> [1] 2.6295 4.1857 5.6592 7.1042 8.5303
max(abs(semi - qnorm(0.975) * sigma_h))
#> [1] 2.398082e-14        identicos salvo error de maquina

# ¿Crece como una caminata aleatoria? En un ARIMA(0,1,0) todos los psi
# valen 1 y sigma_h = sigma*sqrt(h) EXACTAMENTE; esa es la referencia.
round(c(sigma_12_sobre_sigma_1 = sigma_h[H] / sigma_h[1], raiz_de_12 = sqrt(H),
        frente_a_la_caminata   = sigma_h[H] / (s * sqrt(H))), 4)
#> sigma_12_sobre_sigma_1             raiz_de_12   frente_a_la_caminata
#>                 6.7963                 3.4641                 1.9619

# psi tiende a (1 + theta)/(1 - phi); con phi = 0.88 converge muy despacio
round(c(psi_12 = psi[H + 1], limite = (1 + th) / (1 - ph)), 4)
#> psi_12 limite
#> 2.5593 2.9883

# --- Con deriva ----------------------------------------------------------
fd <- Arima(BJsales, order = c(1, 1, 1), include.drift = TRUE)
round(c(deriva = coef(fd)[["drift"]], ee = sqrt(diag(fd$var.coef))[["drift"]],
        t = coef(fd)[["drift"]] / sqrt(diag(fd$var.coef))[["drift"]]), 4)
#> deriva     ee      t
#> 0.4001 0.2557 1.5644
round(c(aicc_con = fd$aicc, aicc_sin = f$aicc), 3)
#> aicc_con aicc_sin
#>  515.062  514.902
round(c(h12_con = forecast(fd, h = H)$mean[H],
        h12_sin = forecast(f,  h = H)$mean[H]), 2)
#> h12_con h12_sin
#>  266.99  263.76