# Verificador B · P5 (beaver2): KPSS dentro de cada tramo y sobre los residuales del escalón
suppressPackageStartupMessages({ library(tseries); library(forecast) })
b <- beaver2$temp; a <- beaver2$activ; k <- which(a == 1)[1]
for (tr in list(1:(k - 1), k:100)) {
  z <- b[tr]
  cat(sprintf("tramo %d-%d (n=%d): KPSS stat=%.3f p=%s | ADF p=%.3f | ndiffs kpss=%d adf=%d pp=%d | r1=%.3f\n", min(tr), max(tr), length(z),
      suppressWarnings(kpss.test(z)$statistic), format(suppressWarnings(kpss.test(z)$p.value)), suppressWarnings(adf.test(z)$p.value),
      ndiffs(z, test = "kpss"), ndiffs(z, test = "adf"), ndiffs(z, test = "pp"), acf(z, plot = FALSE)$acf[2]))
}
e <- residuals(lm(b ~ a))
cat(sprintf("residuales del escalon: KPSS stat=%.3f p=%s (valor critico 10%% de la tabla = 0.347)\n",
    suppressWarnings(kpss.test(e)$statistic), format(suppressWarnings(kpss.test(e)$p.value))))

# Distribucion nula del KPSS aplicado a los residuales de una regresion sobre el escalon (ruptura conocida en
# la lectura 39 de 100), por simulacion: ruido blanco y AR(1) con phi = 0.5, 4000 replicas, semilla 2026.
set.seed(2026)
nula <- function(gen) replicate(4000, { z <- gen(); suppressWarnings(kpss.test(residuals(lm(z ~ a)))$statistic) })
q_rb <- quantile(nula(function() rnorm(100)), c(0.90, 0.95, 0.99))
q_ar <- quantile(nula(function() as.numeric(arima.sim(list(ar = 0.5), 100))), c(0.90, 0.95, 0.99))
cat("cuantiles 90/95/99 % con escalon, ruido blanco:", round(q_rb, 3), "\n")
cat("cuantiles 90/95/99 % con escalon, AR(1) 0.5:   ", round(q_ar, 3), "\n")
cat("tabla ordinaria de KPSS (nivel): 0.347 0.463 0.739 | estadistico de beaver2:", round(suppressWarnings(kpss.test(e)$statistic), 3), "\n")
