library(forecast)

# --- USAccDeaths: la trampa del orden --------------------------------------
uad <- USAccDeaths
c(crudo = ndiffs(uad), tras_D = ndiffs(diff(uad, lag = 12)), nsdiffs = nsdiffs(uad))
#>  crudo tras_D nsdiffs
#>      0      1       1
f <- auto.arima(uad, stepwise = FALSE, approximation = FALSE)
f
#> Series: uad
#> ARIMA(0,1,1)(0,1,1)[12]
#> Coefficients:
#>           ma1     sma1
#>       -0.4303  -0.5528
#> s.e.   0.1228   0.1784
round(Box.test(residuals(f), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4)
#> [1] 0.2477

# --- TRM: cuatro evidencias de que NO hay estacionalidad --------------------
# TRM mensual (promedio del mes, SFC via datos.gov.co). Se reconstruye en cada
# bloque que la use para que sea autonomo; necesita internet.
url <- paste0("https://www.datos.gov.co/resource/32sa-8pi3.json",
              "?$select=vigenciadesde,valor&$limit=50000")
crudo <- jsonlite::fromJSON(url)
diario <- data.frame(fecha = as.Date(substr(crudo$vigenciadesde, 1, 10)),
                     valor = as.numeric(crudo$valor))
diario <- diario[diario$fecha >= as.Date("2015-01-01"), ]
diario <- diario[order(diario$fecha), ]
prom <- tapply(diario$valor, format(diario$fecha, "%Y-%m"), mean)
prom <- prom[names(prom) <= "2026-06"]     # se descarta el mes en curso
trm <- ts(as.numeric(prom), start = c(2015, 1), frequency = 12)

# 1. las dos pruebas automaticas
c(seas = nsdiffs(trm), ocsb = nsdiffs(trm, test = "ocsb"))
#> seas ocsb
#>    0    0

# 2. el correlograma de la serie SIN tendencia
a <- Acf(diff(trm), lag.max = 36, plot = FALSE)$acf
round(c(r12 = a[13], r24 = a[25], r36 = a[37], banda = 1.96/sqrt(length(diff(trm)))), 4)
#>     r12     r24     r36   banda
#> -0.0024 -0.0672  0.0714  0.1675

# 3. forzar la parte estacional y mirar el estadistico t
g <- Arima(trm, order = c(0,1,0), seasonal = list(order = c(1,0,0), period = 12))
round(c(Phi = coef(g)[1], ee = sqrt(diag(g$var.coef))[1],
        t = coef(g)[1]/sqrt(diag(g$var.coef))[1]), 4)
#> Phi.sar1  ee.sar1   t.sar1
#>   0.0013   0.0899   0.0147

# 4. AICc: aqui SI se comparan, porque los dos tienen d = 1 y D = 0
h <- Arima(trm, order = c(0,1,0))
round(c(forzado = g$aicc, simple = h$aicc), 3)
#>  forzado   simple
#> 1708.001 1705.941
as.character(auto.arima(trm, stepwise = FALSE, approximation = FALSE))
#> [1] "ARIMA(0,1,0)"