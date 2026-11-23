# Verificador B · complementos: traza de auto.arima (P7), Ljung-Box de la P8, theta del E1 a 3 decimales
suppressPackageStartupMessages({ library(forecast); library(tsibbledata); library(dplyr) })
ch <- global_economy %>% filter(Country == "Chile") %>% arrange(Year); ex <- ts(ch$Exports, start = 1960)
cat("--- traza exhaustiva (Chile, exportaciones)\n")
tr <- capture.output(a <- auto.arima(ex, stepwise = FALSE, approximation = FALSE, trace = TRUE)); cat(tr, sep = "\n")
lin <- grep("^ ARIMA", tr, value = TRUE); cat("lineas de modelo:", length(lin), "\n")
cat("--- traza escalonada\n"); tr2 <- capture.output(auto.arima(ex, trace = TRUE)); cat(tr2, sep = "\n")
cat("lineas de modelo:", length(grep("^ ARIMA", tr2)), "\n")
pe <- global_economy %>% filter(Country == "Peru") %>% arrange(Year); im <- ts(pe$Imports, start = 1960)
for (d in 1:2) { g <- arima(im, order = c(0, d, 1), method = "ML")
  cat(sprintf("Peru ARIMA(0,%d,1): theta=%.5f sigma2=%.4f LB10 fitdf1 p=%.4f (resid n=%d) | LB10 sobre resid[-(1:d)] p=%.4f\n", d,
      coef(g)[[1]], g$sigma2, Box.test(residuals(g), 10, "Ljung-Box", fitdf = 1)$p.value, length(residuals(g)),
      Box.test(residuals(g)[-(1:d)], 10, "Ljung-Box", fitdf = 1)$p.value)) }
for (d in 1:2) { g <- Arima(im, order = c(0, d, 1)); cat(sprintf("Peru Arima(0,%d,1) CSS-ML: theta=%.5f LB10 p=%.4f\n", d, coef(g)[[1]],
      Box.test(residuals(g), 10, "Ljung-Box", fitdf = 1)$p.value)) }
cat("--- E1 (1,1,1) coeficientes a 3 decimales (ML):\n")
f <- arima(BJsales, order = c(1, 1, 1), method = "ML"); print(round(c(coef(f), sqrt(diag(f$var.coef))), 3))
f <- Arima(BJsales, order = c(1, 1, 1)); print(round(c(coef(f), sqrt(diag(f$var.coef))), 3))
