library(forecast)
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

# --- (a) Tres evidencias ----------------------------------------------------
# 1. prueba automatica (con las dos versiones disponibles)
c(seas = nsdiffs(trm), ocsb = nsdiffs(trm, test = "ocsb"))
#> seas ocsb
#>    0    0

# 2. correlograma de la serie SIN tendencia
a <- Acf(diff(trm), lag.max = 36, plot = FALSE)$acf
round(c(r12 = a[13], r24 = a[25], r36 = a[37], banda = 1.96/sqrt(length(trm)-1)), 4)
#>     r12     r24     r36   banda
#> -0.0024 -0.0672  0.0714  0.1675      ninguno fuera de banda

# 3. AJUSTE forzado: el estadistico t del parametro estacional
g <- Arima(trm, order = c(0,1,0), seasonal = list(order = c(1,0,0), period = 12))
round(c(Phi = coef(g)[1], ee = sqrt(diag(g$var.coef))[1],
        t = coef(g)[1]/sqrt(diag(g$var.coef))[1]), 4)
#> Phi.sar1  ee.sar1   t.sar1
#>   0.0013   0.0899   0.0147
round(c(forzado = g$aicc, simple = Arima(trm, order=c(0,1,0))$aicc), 3)
#>  forzado   simple
#> 1708.001 1705.941      aqui SI se comparan: los dos tienen d=1, D=0

# --- (b) Armonicos sobre co2 ------------------------------------------------
for (K in 1:6) {
  xr <- fourier(co2, K = K)
  f <- auto.arima(co2, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  cat(sprintf("K=%d  terminos=%2d  n_ef=%d  AICc=%8.3f  LB=%.4f\n", K, ncol(xr), f$nobs,
      f$aicc, Box.test(residuals(f), lag=24, type="Ljung-Box", fitdf=sum(f$arma[1:4]))$p.value))
}
#> K=1  terminos= 2  n_ef=467  AICc= 435.509  LB=0.0000
#> K=2  terminos= 4  n_ef=467  AICc= 268.475  LB=0.0000
#> K=3  terminos= 6  n_ef=467  AICc= 223.402  LB=0.0000
#> K=4  terminos= 8  n_ef=467  AICc= 180.200  LB=0.0439
#> K=5  terminos=10  n_ef=467  AICc= 181.494  LB=0.0516
#> K=6  terminos=11  n_ef=467  AICc= 183.624  LB=0.0515

airline <- Arima(co2, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
round(c(armonico_K4 = 180.200, n_armonico = 467,
        airline = airline$aicc, n_airline = airline$nobs), 3)
#> armonico_K4  n_armonico     airline   n_airline
#>     180.200     467.000     178.209     455.000