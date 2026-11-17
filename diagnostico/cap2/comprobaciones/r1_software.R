# R1 del capítulo 2 · lo que la prosa afirma del software, leído en el propio código de R.
#   Rscript diagnostico/cap2/comprobaciones/r1_software.R > diagnostico/cap2/comprobaciones/r1_software.out 2>&1
suppressMessages({library(tseries); library(forecast)})
cat("R", as.character(getRversion()), "· tseries", as.character(packageVersion("tseries")), "· forecast",
    as.character(packageVersion("forecast")), "· urca", as.character(packageVersion("urca")), "· fabletools",
    as.character(packageVersion("fabletools")), "\n")
cat("\n[adf.test] la regresión que estima (constante y tendencia `tt`) y su k por defecto:\n")
x <- deparse(tseries::adf.test)
cat(grep("lm\\(|tt <-|k = trunc|alternative = c", x, value = TRUE), sep = "\n")
cat("\n[kpss.test] truncamiento:\n"); x <- deparse(tseries::kpss.test)
cat(grep("trunc\\(", x, value = TRUE), sep = "\n")
cat("\n[forecast::ndiffs] el truncamiento que le pasa a urca::ur.kpss:\n"); x <- deparse(forecast::ndiffs)
cat(grep("3 \\* sqrt|ur\\.kpss", x, value = TRUE), sep = "\n")
cat("\n[urca::ur.kpss] sus propios truncamientos (lags = 'short' es el primero):\n"); x <- deparse(urca::ur.kpss)
cat(grep("n/100", x, value = TRUE), sep = "\n")
cat("\n[forecast::BoxCox] variante con signo:\n"); print(body(forecast::BoxCox))
cat("\n[fabletools::box_cox]:\n"); print(body(fabletools::box_cox))
cat("\n[guer.cv] tamaño de bloque:\n"); cat(grep("period <-", deparse(forecast:::guer.cv), value = TRUE), sep = "\n")
cat("nonseasonal.length por defecto =", formals(forecast:::guer.cv)$nonseasonal.length, "\n")
