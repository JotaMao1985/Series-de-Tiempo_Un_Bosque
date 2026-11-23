library(forecast)

ap <- log(AirPassengers)          # m = 12, n = 144

# 1. La estacionalidad, VISTA: un trazo por año, los meses en el eje x
ggseasonplot(ap, year.labels = TRUE)
monthplot(ap)                     # un panel por mes, con su media

# 2. La estacionalidad, MEDIDA: al menos 3m rezagos o no se ve el decaimiento
a <- Acf(ap, lag.max = 36, plot = FALSE)
round(a$acf[c(2, 13, 25, 37)], 4)          # rezagos 1, 12, 24, 36
#> [1] 0.9537 0.7619 0.5205 0.3193
round(1.96 / sqrt(length(ap)), 4)          # banda
#> [1] 0.1633

# 3. El contraejemplo: la TRM, sobre la serie YA sin tendencia
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
b <- Acf(diff(trm), lag.max = 36, plot = FALSE)
round(b$acf[c(13, 25, 37)], 4)
#> [1] -0.0024 -0.0672  0.0714
# El cuarto decimal baila (-0.0024 aqui, -0.0025 en las tablas del capitulo):
# la copia congelada de la TRM esta redondeada a dos decimales y el valor cae
# justo en el empate del redondeo. Ninguna conclusion depende de eso.
round(1.96 / sqrt(length(diff(trm))), 4)
#> [1] 0.1675
# Ninguno se acerca a la banda: no hay nada estacional que modelar.