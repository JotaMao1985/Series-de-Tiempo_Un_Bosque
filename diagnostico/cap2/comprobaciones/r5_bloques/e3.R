library(forecast)
y <- USAccDeaths

# (a) Las pruebas, en el orden de la regla. ndiffs() sobre la serie cruda
#     devuelve 0: la estacionalidad confunde a la prueba
ndiffs(y)
nsdiffs(y)
ndiffs(diff(y, lag = 12))     # sobre lo que deja la diferencia estacional

# (b) El correlograma de cada serie, con SU banda: las cuatro tienen distinta n
resumen <- function(x, nombre) {
  r <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  banda <- 1.96 / sqrt(length(x))
  data.frame(serie = nombre, n = length(x), banda = round(banda, 3),
             r1 = round(r[1], 3), r12 = round(r[12], 3),
             fuera = sum(abs(r) > banda))
}
rbind(resumen(y, "original"),
      resumen(diff(y), "nabla"),
      resumen(diff(y, lag = 12), "nabla12"),
      resumen(diff(diff(y), lag = 12), "nabla12 nabla"))

# Cuantas de 24 barras se esperan fuera por azar en un ruido blanco
0.05 * 24
