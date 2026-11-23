library(forecast)
f  <- Arima(BJsales.lead, order = c(0, 1, 1))
th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2)
round(c(theta = th, sigma = s, psi_j = 1 + th), 4)

# (a) sigma_h con psi_0 = 1 y psi_j = 1 + theta para j >= 1
h <- c(1, 2, 12)
sigma_h <- s * sqrt(1 + (h - 1) * (1 + th)^2)
fc <- forecast(f, h = 12, level = 95)
round(rbind(h = h, sigma_h = sigma_h, semiancho_95 = qnorm(0.975) * sigma_h,
            el_de_forecast = as.numeric((fc$upper - fc$lower) / 2)[h]), 4)

# (b) frente a una caminata aleatoria con la misma sigma
round(sigma_h[3] / (s * sqrt(12)), 4)

# (c) la forma: el mismo modelo sin deriva y con ella
fd <- Arima(BJsales.lead, order = c(0, 1, 1), include.drift = TRUE)
round(rbind(sin_deriva = forecast(f,  h = 100)$mean[c(1, 12, 100)],
            con_deriva = forecast(fd, h = 100)$mean[c(1, 12, 100)]), 2)
round(c(ultimo_dato = as.numeric(tail(BJsales.lead, 1)), deriva = coef(fd)[["drift"]],
        t = coef(fd)[["drift"]] / sqrt(diag(fd$var.coef))[["drift"]],
        aicc_sin = f$aicc, aicc_con = fd$aicc), 3)