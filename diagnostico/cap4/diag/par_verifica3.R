# ¿Descarta auto.arima el ARIMA(2,1,2) de la TRM por sus raíces, o porque su ajuste CSS-ML es otro?
suppressMessages(library(forecast))
trm <- ts(read.csv("../../../Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start=c(2015,1), frequency=12)
tr <- capture.output(a <- auto.arima(trm, trace=TRUE, stepwise=FALSE, approximation=FALSE, seasonal=FALSE))
cat(grep("ARIMA\\(2,1,2\\)|ARIMA\\(0,1,0\\)", tr, value=TRUE), sep="\n")
f_cssml <- Arima(trm, order=c(2,1,2))
cat("Arima CSS-ML (2,1,2): coef", round(coef(f_cssml),4), " AICc", round(f_cssml$aicc,2),
    " |raíces AR|", round(Mod(polyroot(c(1,-coef(f_cssml)[1:2]))),4), " |raíces MA|", round(Mod(polyroot(c(1,coef(f_cssml)[3:4]))),4), "\n")
f_ml <- Arima(trm, order=c(2,1,2), method="ML")
cat("Arima ML (2,1,2): coef", round(coef(f_ml),4), " AICc", round(f_ml$aicc,2), "\n")
# Nilo: lo mismo
f_n <- Arima(Nile, order=c(2,1,2)); cat("Nilo Arima CSS-ML (2,1,2): coef", round(coef(f_n),4), " AICc", round(f_n$aicc,3),
  " |raíces AR|", round(Mod(polyroot(c(1,-coef(f_n)[1:2]))),4), "\n")
f_n2 <- arima(Nile, order=c(2,1,2), method="ML"); cat("Nilo arima ML (2,1,2): coef", round(coef(f_n2),4), " loglik", round(f_n2$loglik,3), " vs CSS-ML loglik", round(f_n$loglik,3), "\n")

# Efecto Working: la diferencia de promedios mensuales de una caminata aleatoria diaria
# tiene rho1 = (m^2 - 1) / (2 (2 m^2 + 1)) con m días por mes (simulación de comprobación).
m <- 21; cat("\nWorking, rho1 teórico con m = 21:", round((m^2-1)/(2*(2*m^2+1)),4), "\n")
set.seed(2026); z <- cumsum(rnorm(m*20000)); pm <- colMeans(matrix(z, nrow = m))
cat("simulado (20000 meses):", round(acf(diff(pm), plot=FALSE)$acf[2],4), "\n")
d1 <- diff(trm); cat("TRM: rho1 =", round(acf(d1, plot=FALSE)$acf[2],4), " ee aprox 1/sqrt(n) =", round(1/sqrt(length(d1)),4), "\n")
