w <- diff(WWWusage)                    # cambios de un minuto al siguiente
n <- length(w); banda <- 1.96 / sqrt(n)
round(c(n = n, banda = banda), 4)

# (a) Pasos 1 a 3: que rezagos salen de la banda
a <- acf(w, lag.max = 20, plot = FALSE)$acf[-1]
p <- as.numeric(pacf(w, lag.max = 20, plot = FALSE)$acf)
which(abs(a) > banda)
which(abs(p) > banda)
round(a[1:6], 3)
round(p[1:6], 3)

# Los dos candidatos
ar3    <- arima(w, order = c(3, 0, 0), method = "ML")
arma11 <- arima(w, order = c(1, 0, 1), method = "ML")
round(coef(arma11), 4)

# (b) El ARMA(1,1) redondeado, con las formulas del modulo
phi <- 0.63; theta <- 0.53
rho1 <- (1 + phi * theta) * (phi + theta) / (1 + 2 * phi * theta + theta^2)
round(rho1 * phi^(0:2), 3)             # rho_1, rho_2, rho_3

# (c) Paso 4: la ACF teorica de cada modelo ajustado frente a la muestral
round(rbind(muestral = a[1:6],
            AR3      = ARMAacf(ar = coef(ar3)[1:3], lag.max = 6)[-1],
            ARMA11   = ARMAacf(ar = coef(arma11)[["ar1"]], ma = coef(arma11)[["ma1"]],
                               lag.max = 6)[-1]), 3)

# Adelanto del Modulo 8: los dos criterios (menor es mejor) y Ljung-Box
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
lb <- function(f, k) Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = k)$p.value
round(rbind(AICc = c(AR3 = aicc(ar3, n), ARMA11 = aicc(arma11, n)),
            BIC  = c(BIC(ar3), BIC(arma11)),
            LB12 = c(lb(ar3, 3), lb(arma11, 2))), 3)
