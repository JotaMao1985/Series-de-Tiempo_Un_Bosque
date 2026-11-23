# Lector F · cifras del quiz (autoevaluacion) que dependen del Nilo, solo para anotar en para_r5
suppressMessages(library(forecast))
f111 <- Arima(Nile, order = c(1, 1, 1)); f122 <- Arima(Nile, order = c(1, 2, 2))
cat(sprintf("AICc ARIMA(1,1,1) = %.2f  ARIMA(1,2,2) = %.2f\n", f111$aicc, f122$aicc))
ma <- coef(f122)[grepl("^ma", names(coef(f122)))]
cat(sprintf("|raiz MA| min del ARIMA(1,2,2) = %.3f\n", min(Mod(polyroot(c(1, ma))))))
cat("sigma(1,1,1) arima ML:", round(sqrt(arima(Nile, c(1,1,1), method="ML")$sigma2), 3), " Arima:", round(sqrt(f111$sigma2), 3), "\n")
