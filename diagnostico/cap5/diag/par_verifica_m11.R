# par_verifica_m11.R — M11: la partición única, el crecimiento anual y la
# validación de origen móvil (h = 12 con 61 orígenes, h = 24 con 49), replicando
# los pronosticadores de precalculo/genera_cap5.R §10 sin leer sus salidas.
# Uso: Rscript par_verifica_m11.R > par_verifica_m11.out 2>&1
suppressMessages(library(forecast))
options(width = 120)
sec <- function(t) cat("\n==================== ", t, " ====================\n", sep = "")
apb <- AirPassengers; ap <- log(apb); n <- length(ap); M <- 12
desde_log <- function(p) exp(as.numeric(p))

sec("Partición única: entrena hasta 1958-12, prueba 24 meses")
ent <- window(ap, end = c(1958, 12)); ento <- window(apb, end = c(1958, 12))
obs <- as.numeric(window(apb, start = c(1959, 1)))
met <- function(p) { e <- obs - p; c(rmse = sqrt(mean(e^2)), mae = mean(abs(e)), mape = 100*mean(abs(e/obs)), sesgo = mean(e)) }
# K elegido como en el precálculo: mínimo AICc sobre la serie COMPLETA
aiccK <- sapply(1:6, function(K) auto.arima(ap, xreg = fourier(ap, K = K), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)$aicc)
K <- which.min(aiccK); cat("K elegido (AICc sobre la serie completa, incluida la prueba):", K, "\n")
m <- list()
m$snaive  <- as.numeric(snaive(ento, h = 24)$mean)
f_sar <- Arima(ent, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12)); m$sarima <- desde_log(forecast(f_sar, h = 24)$mean)
f_auto <- auto.arima(ent, stepwise = FALSE, approximation = FALSE); cat("auto.arima en entrenamiento:", as.character(f_auto), "\n")
m$auto <- desde_log(forecast(f_auto, h = 24)$mean)
f_ets <- ets(ento); cat("ETS cruda:", f_ets$method, " npar =", length(f_ets$par), "\n"); m$ets <- as.numeric(forecast(f_ets, h = 24)$mean)
f_etl <- ets(ent); cat("ETS log:", f_etl$method, " npar =", length(f_etl$par), "\n"); m$ets_log <- desde_log(forecast(f_etl, h = 24)$mean)
f_arm <- auto.arima(ent, xreg = fourier(ent, K = K), seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
cat("armónica:", as.character(f_arm), " ncoef =", length(f_arm$coef), " nombres:", paste(names(f_arm$coef), collapse = " "), "\n")
m$armonica <- desde_log(forecast(f_arm, xreg = fourier(ent, K = K, h = 24), h = 24)$mean)
f_stl <- stlm(ent, s.window = "periodic", method = "arima"); cat("stlm entrenamiento:", as.character(f_stl$model), " ncoef =", length(f_stl$model$coef), "\n")
m$stl <- desde_log(forecast(f_stl, h = 24)$mean)
tab <- t(sapply(m, met)); print(round(tab[order(tab[, "rmse"]), ], 2))

sec("Crecimiento anual de los totales")
tot <- tapply(as.numeric(apb), floor(time(apb) + 1e-6), sum)
print(round(100 * (tot[-1] / tot[-length(tot)] - 1), 1))
for (nm in c("sarima", "ets_log", "armonica")) {
  p <- m[[nm]]; t59 <- sum(p[1:12]); t60 <- sum(p[13:24])
  cat(sprintf("%-9s 1959 vs 1958 real: %.1f%%   1960 vs 1959 pronosticado: %.1f%%   1960 vs 1959 real: %.1f%%\n",
              nm, 100*(t59/tot["1958"] - 1), 100*(t60/t59 - 1), 100*(t60/tot["1959"] - 1)))
}
cat("errores del SARIMA (obs - pron) todos positivos:", all(obs - m$sarima > 0), "\n")

sec("Origen móvil")
pron <- list(
  snaive  = function(el, eo, h) as.numeric(snaive(eo, h = h)$mean),
  sarima  = function(el, eo, h) desde_log(forecast(Arima(el, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = M)), h = h)$mean),
  armonica = function(el, eo, h) desde_log(forecast(auto.arima(el, xreg = fourier(el, K = 6), seasonal = FALSE),
                                                    xreg = fourier(el, K = 6, h = h), h = h)$mean),
  ets_log  = function(el, eo, h) desde_log(forecast(ets(el), h = h)$mean),
  ets_orig = function(el, eo, h) as.numeric(forecast(ets(eo), h = h)$mean),
  stl      = function(el, eo, h) desde_log(forecast(stlm(el, s.window = "periodic", method = "arima"), h = h)$mean))
corre <- function(H) {
  orig <- 72:(n - H); E <- list()
  for (o in orig) {
    el <- window(ap, end = time(ap)[o]); eo <- window(apb, end = time(ap)[o])
    ob <- as.numeric(window(apb, start = time(ap)[o + 1], end = time(ap)[o + H]))
    E[[length(E) + 1]] <- sapply(pron, function(f) ob - f(el, eo, H))   # H x 6
  }
  list(orig = orig, E = E)
}
etq <- function(o) format(as.Date(sprintf("%d-%02d-01", floor(time(ap)[o] + 1e-6), cycle(ap)[o])), "%Y-%m")
for (H in c(12, 24)) {
  r <- corre(H); no <- length(r$orig)
  rm <- t(sapply(r$E, function(e) sqrt(colMeans(e^2))))         # no x 6
  cat(sprintf("\nH = %d: %d orígenes (primero %s, último %s)\n", H, no, etq(r$orig[1]), etq(r$orig[no])))
  cat("RMSE medio:\n"); print(round(sort(colMeans(rm)), 3))
  cat("% de orígenes en que cada uno gana al SARIMA:\n"); print(round(100 * colMeans(rm < rm[, "sarima"]), 1))
  mejor <- colnames(rm)[apply(rm, 1, which.min)]
  cat("orígenes en que el SARIMA NO es el mejor de los seis:", sum(mejor != "sarima"), "\n")
  cat("  fechas:", sapply(r$orig[mejor != "sarima"], etq), "\n")
  if (H == 12) {
    e12 <- t(sapply(r$E, function(e) e[12, ]))
    cat("solo el mes 12 · media de |e12|:\n"); print(round(sort(colMeans(abs(e12))), 2))
    cat("solo el mes 12 · RMSE entre orígenes de e12:\n"); print(round(sort(sqrt(colMeans(e12^2))), 2))
  }
}
cat("\nfin\n")
