library(forecast)
n <- length(co2)   # 468

# --- Etapa 1: D y d ---------------------------------------------------------
round(c(cruda = var(co2), d1 = var(diff(co2)),
        D1 = var(diff(co2, lag = 12)), ambas = var(diff(diff(co2, lag = 12)))), 4)
#>    cruda       d1       D1    ambas
#> 223.9877   1.4555   0.3882   0.1543      minimo en (d=1, D=1)
c(nsdiffs = nsdiffs(co2), ndiffs_tras_D = ndiffs(diff(co2, lag = 12)))
#>       nsdiffs ndiffs_tras_D
#>             1             1

# --- Etapa 2: la rejilla, con d = 1 y D = 1 FIJOS ---------------------------
res <- data.frame()
for (p in 0:2) for (q in 0:3) for (P in 0:1) for (Q in 0:1) {
  f <- tryCatch(Arima(co2, order = c(p,1,q),
                      seasonal = list(order = c(P,1,Q), period = 12), method = "ML"),
                error = function(e) NULL, warning = function(w) NULL)
  if (is.null(f)) next
  res <- rbind(res, data.frame(m = sprintf("(%d,1,%d)(%d,1,%d)[12]", p,q,P,Q),
    aicc = f$aicc, bic = f$bic, nobs = f$nobs,
    lb = Box.test(residuals(f), lag=24, type="Ljung-Box", fitdf=p+q+P+Q)$p.value))
}
nrow(res)                                  # 47 de los 48 convergen
#> [1] 47
c(mejor_aicc = as.character(res$m[which.min(res$aicc)]),
  mejor_bic  = as.character(res$m[which.min(res$bic)]))
#>         mejor_aicc          mejor_bic
#> "(0,1,3)(0,1,1)[12]" "(0,1,1)(0,1,1)[12]"
# AICc y BIC discrepan: el BIC penaliza mas y se queda con el airline.
round(res[which.min(res$aicc), c("aicc","nobs","lb")], 4)
#>        aicc nobs    lb
#> 14 176.9982  455 0.631
round(178.2089 - 176.9982, 3)              # el airline pierde por poco
#> [1] 1.211

# --- Etapa 3: la comparacion INVALIDA que pide el enunciado -----------------
sinD <- Arima(co2, order = c(0,1,1), seasonal = list(order = c(0,0,1), period = 12))
conD <- Arima(co2, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
round(c(aicc_sinD = sinD$aicc, nobs_sinD = sinD$nobs,
        aicc_conD = conD$aicc, nobs_conD = conD$nobs), 3)
#> aicc_sinD nobs_sinD aicc_conD nobs_conD
#>   988.100   467.000   178.209   455.000
round(Box.test(residuals(sinD), lag=24, type="Ljung-Box", fitdf=2)$p.value, 4)
#> [1] 0        no pasa el diagnostico