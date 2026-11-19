library(forecast); library(tseries)

# (a) Paso 2: hay algo que estabilizar? El nivel del CO2 cambia muy poco de
#     escala: el maximo es 1.17 veces el minimo (en AirPassengers, 5.98 veces)
round(c(co2 = max(co2) / min(co2), AirPassengers = max(AirPassengers) / min(AirPassengers)), 2)
# Se deja sin transformar: preparar(co2, logaritmo = FALSE)

# (b) Paso 3: la diferencia estacional PRIMERO
nsdiffs(co2)
co2_s <- diff(co2, lag = 12)
# Paso 4: la regular, sobre lo que dejo el paso 3
ndiffs(co2_s)
co2_sd <- diff(co2_s)

# (c) El correlograma en cada etapa. Serie original: r1 y r12
round(acf(co2, lag.max = 24, plot = FALSE)$acf[c(2, 13)], 4)
# Tras la diferencia estacional la ACF todavia baja despacio: r1, r2 y r3
round(acf(co2_s, lag.max = 24, plot = FALSE)$acf[2:4], 4)

# (d) Paso 5: la serie final no pide mas diferencias y el KPSS ya no rechaza
#     (0.1 es el tope de la tabla: p > 0.10; suppressWarnings() calla ese aviso)
ndiffs(co2_sd); nsdiffs(co2_sd)
suppressWarnings(kpss.test(co2_sd))$p.value
# Lo que queda en ella: r1, r12 y los rezagos, de 24, fuera de la banda
banda <- 1.96 / sqrt(length(co2_sd))
r <- acf(co2_sd,  lag.max = 24, plot = FALSE)$acf[-1]
p <- pacf(co2_sd, lag.max = 24, plot = FALSE)$acf
c(n = length(co2_sd), banda = round(banda, 3), r1 = round(r[1], 3), r12 = round(r[12], 3))
which(abs(r) > banda)          # ACF
which(abs(p) > banda)          # PACF

# Y si se hubiera tomado el logaritmo? Las mismas dos decisiones
nsdiffs(log(co2)); ndiffs(diff(log(co2), lag = 12))
