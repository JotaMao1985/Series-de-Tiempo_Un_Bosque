library(forecast)
ap <- log(AirPassengers)

# --- Regresor 1: dias del mes ----------------------------------------------
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = length(ap))
dias <- as.numeric(diff(c(fechas, seq(tail(fechas,1), by = "month", length.out = 2)[2])))
range(dias)
#> [1] 28 31

# --- Regresor 2: Semana Santa (algoritmo de Meeus/Butcher, calendario gregoriano)
pascua <- function(anio) {
  a <- anio %% 19; b <- anio %/% 100; cc <- anio %% 100
  d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3
  h <- (19*a + b - d - g + 15) %% 30; i <- cc %/% 4; k <- cc %% 4
  l <- (32 + 2*e + 2*i - h - k) %% 7; m <- (a + 11*h + 22*l) %/% 451
  mes <- (h + l - 7*m + 114) %/% 31; dia <- ((h + l - 7*m + 114) %% 31) + 1
  as.Date(sprintf("%04d-%02d-%02d", anio, mes, dia))
}
sapply(1949:1952, function(a) format(pascua(a), "%Y-%m-%d"))
#> [1] "1949-04-17" "1950-04-09" "1951-03-25" "1952-04-13"
es_pascua <- as.numeric(format(fechas, "%m") ==
                        sapply(as.numeric(format(fechas, "%Y")),
                               function(a) format(pascua(a), "%m")))
sum(es_pascua)     # un mes marcado por anio
#> [1] 12

# --- Los tres ajustes -------------------------------------------------------
xreg <- cbind(log_dias = log(dias), pascua = es_pascua)
f0 <- Arima(ap, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
f1 <- Arima(ap, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12), xreg = xreg[, 1, drop = FALSE])
f2 <- Arima(ap, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12), xreg = xreg)
round(c(sin = f0$aicc, dias = f1$aicc, dias_pascua = f2$aicc), 4)
#>         sin        dias dias_pascua
#>   -483.2101   -486.5380   -490.7221

round(cbind(coef = coef(f2), ee = sqrt(diag(f2$var.coef)),
            t = coef(f2)/sqrt(diag(f2$var.coef)))[3:4, ], 4)
#>           coef     ee      t
#> log_dias 1.084 0.4462 2.4291
#> pascua   0.029 0.0111 2.6026

# Contraste de que el efecto es EXACTAMENTE proporcional (beta = 1)
round((coef(f2)["log_dias"] - 1) / sqrt(diag(f2$var.coef))["log_dias"], 4)
#> log_dias
#>   0.1882      no se rechaza beta = 1