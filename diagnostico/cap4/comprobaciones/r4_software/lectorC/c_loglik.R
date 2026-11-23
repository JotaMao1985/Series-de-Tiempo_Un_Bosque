# lector C · [c4-m7-22] ¿se debe la diferencia 1267.471 (statsmodels) frente a 1267.507 (R) a la inicialización del filtro?
suppressMessages(library(forecast))
a <- arima(Nile, order = c(1,1,1), method = "ML")
cat(sprintf("R arima ML: ar1 = %.6f ma1 = %.6f sigma2 = %.4f loglik = %.6f aic = %.6f\n", coef(a)[1], coef(a)[2], a$sigma2, a$loglik, a$aic))
# loglik de R evaluado en los parámetros de statsmodels (pasados por fixed; sigma2 se concentra)
args <- commandArgs(TRUE)
if (length(args) == 2) {
  b <- arima(Nile, order = c(1,1,1), method = "ML", fixed = as.numeric(args), transform.pars = FALSE)
  cat(sprintf("R evaluado en ar1 = %s ma1 = %s: sigma2 = %.4f loglik = %.6f aic = %.6f\n", args[1], args[2], b$sigma2, b$loglik, b$aic))
}
