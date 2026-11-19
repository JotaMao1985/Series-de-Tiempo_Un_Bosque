dax <- EuStockMarkets[, "DAX"]
r <- diff(log(dax))                       # rendimiento de cada dia
banda <- 1.96 / sqrt(length(r))
c(n = length(r), banda = round(banda, 4))

# Rezagos, de 24, cuya autocorrelacion sale de la banda
fuera <- function(x) {
  rk <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  which(abs(rk) > banda)
}

# (a) Los rendimientos
fuera(r)
# (b) Sus cuadrados
fuera(r^2)
round(acf(r^2, lag.max = 24, plot = FALSE)$acf[2:4], 3)     # r1, r2 y r3

# (c) Los mismos rendimientos en un orden al azar: cuantos rezagos salen
set.seed(2026)
b <- sample(r)
c(barajados = length(fuera(b)), sus_cuadrados = length(fuera(b^2)))
