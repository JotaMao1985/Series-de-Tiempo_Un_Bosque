# diag/v5_trm_descarga.R — ejecuta el código de descarga de la TRM del bloque R del M6 tal cual
# (requiere internet), comprueba que hasta 2026-06 reproduce la serie fijada y repite el
# análisis del ejercicio 4 con los meses que haya hoy. También: KPSS de tendencia sobre la TRM.
# Uso (desde la raíz del repo):  Rscript diagnostico/cap2/diag/v5_trm_descarga.R
suppressMessages({ library(tseries); library(jsonlite); library(forecast) })
descarga_trm <- function() {
  url <- paste0("https://www.datos.gov.co/resource/32sa-8pi3.json",
                "?$select=vigenciadesde,valor",
                "&$where=vigenciadesde%20%3E=%20%272015-01-01T00:00:00.000%27",
                "&$order=vigenciadesde&$limit=20000")
  d <- fromJSON(url)
  d$valor <- as.numeric(d$valor)
  d$mes   <- substr(d$vigenciadesde, 1, 7)
  d <- d[d$mes < format(Sys.Date(), "%Y-%m"), ]
  m <- aggregate(valor ~ mes, data = d, FUN = mean)
  m <- m[order(m$mes), ]
  ts(round(m$valor, 2),
     start = c(as.integer(substr(m$mes[1], 1, 4)), as.integer(substr(m$mes[1], 6, 7))),
     frequency = 12)
}
fij <- fromJSON("precalculo/salidas/datos_series.json")$trm$valores
trm_hoy <- tryCatch(descarga_trm(), error = function(e) { cat("descarga fallida:", conditionMessage(e), "\n"); NULL })
if (!is.null(trm_hoy)) {
  cat("descargada: n =", length(trm_hoy), "fin", end(trm_hoy), "\n")
  cat("max|dif| con la serie fijada (primeros 138):", max(abs(trm_hoy[1:138] - fij)), "\n")
  f <- function(z) c(ADF = round(unname(suppressWarnings(adf.test(z))$statistic),4), pADF = round(suppressWarnings(adf.test(z))$p.value,4),
                     KPSS = round(unname(suppressWarnings(kpss.test(z))$statistic),4), pKPSS = suppressWarnings(kpss.test(z))$p.value)
  print(rbind(TRM_hoy = f(trm_hoy), dTRM_hoy = f(diff(trm_hoy)))); cat("ndiffs hoy:", ndiffs(trm_hoy), "\n")
}
trm <- ts(fij, start = c(2015, 1), frequency = 12)
cat("KPSS de tendencia, TRM fijada:", round(suppressWarnings(kpss.test(trm, null = "Trend"))$statistic, 4),
    suppressWarnings(kpss.test(trm, null = "Trend"))$p.value, "\n")
# ventanas: ¿el veredicto del ADF depende de la ventana? (ejercicio 4, «propiedad estructural»)
for (ini in c(2015, 2018, 2020, 2022)) { z <- window(trm, start = c(ini, 1))
  a <- suppressWarnings(adf.test(z)); cat("ventana desde", ini, ": n", length(z), " ADF", round(a$statistic,3), " p", round(a$p.value,3), "\n") }
