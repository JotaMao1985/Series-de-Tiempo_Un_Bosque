# Comprobaciones de la sesión maestra sobre el diagnóstico del capítulo 5 (2026-11-23)
suppressMessages(library(forecast))
y <- log(AirPassengers)
f <- Arima(y, order = c(0,1,1), seasonal = c(0,1,1))
print(round(coef(f), 4))
# (1) ¿el airline acumula incertidumbre más despacio que una caminata?
# pesos psi del modelo expandido: (1-B)(1-B^12) y = (1+theta B)(1+Theta B^12) e
H <- 240
ma <- c(coef(f)[["ma1"]], rep(0, 10), coef(f)[["sma1"]], coef(f)[["ma1"]] * coef(f)[["sma1"]])
ar_ext <- c(1, rep(0, 10), 1, -1)   # (1-B)(1-B^12) = 1 - B - B^12 + B^13
psi <- ARMAtoMA(ar = ar_ext, ma = ma, lag.max = H)
sh_air <- sqrt(cumsum(c(1, psi^2)))       # sigma_h / sigma, h = 1..H+1
sh_rw  <- sqrt(seq_len(H + 1))            # caminata con la misma sigma
cat("psi_240 =", round(psi[240], 2), "\n")
cruce <- which(sh_air > sh_rw)
cat("primer h en que el airline supera a la caminata (misma sigma):", if (length(cruce)) min(cruce) else NA, "\n")
print(round(rbind(h = c(1, 12, 24, 36, 42, 60, 120, 240), airline = sh_air[c(1,12,24,36,42,60,120,240)],
                  caminata = sh_rw[c(1,12,24,36,42,60,120,240)]), 3))

# (2) Simulador airline-pesos del M5: ¿con Theta -> 0 desaparece el escalón del rezago 12?
pesos <- function(th, Th, H = 25) {
  ma <- c(th, rep(0, 10), Th, th * Th)
  ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = ma, lag.max = H)
}
th <- coef(f)[["ma1"]]
for (Th in c(0, coef(f)[["sma1"]], -0.99)) {
  p <- pesos(th, Th)
  cat(sprintf("Theta = %6.3f   psi_11 = %.3f  psi_12 = %.3f  salto psi_12 - psi_11 = %.3f\n", Th, p[11], p[12], p[12] - p[11]))
}

# (3) Ejercicio 3(b): ¿«el armónico, por dos puntos» es la lectura ingenua?
xr <- fourier(co2, K = 4)
h4 <- auto.arima(co2, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
al <- Arima(co2, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
cat(sprintf("armónico K = 4: AICc %.3f (n %d, LB(24) p %.4f) · airline: AICc %.3f (n %d, LB(24) p %.4f)\n",
            h4$aicc, h4$nobs, Box.test(residuals(h4), lag = 24, type = "Ljung-Box", fitdf = sum(h4$arma[1:4]))$p.value,
            al$aicc, al$nobs, Box.test(residuals(al), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value))

# (4) Remisión del M6 a las manchas solares del cap. 3: ¿«los dos criterios discrepaban»?
#     Lectura del cap. 3 (no se recalcula): l. 5731 «no es el mejor por AICc ni por BIC. Gana el ARMA(2,1)»;
#     l. 6011 «Sobre la raíz cuadrada, el AR(2) es a la vez el mejor por AICc y el mejor por BIC».
#     La única discrepancia AICc/BIC del cap. 3 (AR(4) frente a AR(2), l. 6799 y 6864) es la de un ejercicio sobre otra serie.

# (5) Criterio |raíz MA|^-1 del M3: con un SMA(1), |raíz|^-1 = |Theta|^(1/12): se pega a 1 aunque Theta esté lejos de -1
for (Th in c(-0.3, -0.5569, -0.9, -0.9973)) cat(sprintf("Theta = %7.4f  ->  |raíz|^-1 = %.4f\n", Th, abs(Th)^(1/12)))
