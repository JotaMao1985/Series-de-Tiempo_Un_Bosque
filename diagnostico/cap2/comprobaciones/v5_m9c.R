suppressMessages({library(tseries); library(forecast)})
archivo <- "Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv"
trm <- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)
print(length(trm)); print(trunc((length(trm)-1)^(1/3)))
print(round(c(adf.test(trm)$p.value, adf.test(diff(trm))$p.value), 3))
print(suppressWarnings(kpss.test(trm, null = "Trend")))
print(nsdiffs(trm)); print(ndiffs(trm))
print(length(window(trm, start = c(2022, 1)))); print(round(adf.test(window(trm, start = c(2022, 1)))$p.value, 3))
