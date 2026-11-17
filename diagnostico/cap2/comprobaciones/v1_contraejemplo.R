# Verificador independiente · R1 cap. 2 · contraejemplo a «si al diferenciar la
# varianza sube, esa diferencia sobraba» (M7, l. 3460-3462; quiz P4, retroAcierto)
suppressMessages({library(forecast); library(tseries)})
# ARIMA(0,1,1): y_t = y_{t-1} + e_t - 0.8 e_{t-1}. Tiene raiz unitaria: la diferencia HACE FALTA.
set.seed(4); y <- arima.sim(list(order = c(0, 1, 1), ma = -0.8), n = 143)   # 144 valores
cat("n =", length(y), "\n")
cat("var(y) =", round(var(y), 3), " var(diff(y)) =", round(var(diff(y)), 3), "-> la varianza SUBE\n")
cat("ndiffs(y) =", ndiffs(y), "· adf.test p =", round(suppressWarnings(adf.test(y)$p.value), 3),
    "· r1 de diff(y) =", round(acf(diff(y), plot = FALSE)$acf[2], 3), "\n")
cat("Teoria: Var(diff y) = (1 + 0.8^2) sigma^2 = 1.64; la de y en 144 pasos crece con t: la comparacion depende de n.\n")
set.seed(2026)
res <- t(replicate(500, { y <- arima.sim(list(order = c(0, 1, 1), ma = -0.8), n = 143)
                          c(sube = var(diff(y)) > var(y), nd = ndiffs(y)) }))
cat(sprintf("500 series, theta = -0.8, n = 144: la varianza sube en el %.1f %%; ndiffs = 1 en el %.1f %% de esas\n",
            100 * mean(res[, 1]), 100 * mean(res[res[, 1] == 1, 2] == 1)))
