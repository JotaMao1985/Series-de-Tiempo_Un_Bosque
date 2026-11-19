set.seed(7)
A <- arima.sim(list(ar = c(0.5, 0.3)), n = 200)
set.seed(3)
B <- arima.sim(list(ma = 0.8), n = 200)

# Rezagos cuya barra sale de la banda, en la ACF y en la PACF
fuera <- function(x, rezagos) {
  banda <- 1.96 / sqrt(length(x))
  c(acf  = toString(which(abs(acf(x,  lag.max = rezagos, plot = FALSE)$acf[-1]) > banda)),
    pacf = toString(which(abs(pacf(x, lag.max = rezagos, plot = FALSE)$acf) > banda)))
}

# (a) La serie A
fuera(A, 24)
round(pacf(A, lag.max = 24, plot = FALSE)$acf[1:4], 3)

# (b) La serie B
fuera(B, 24)
round(acf(B,  lag.max = 24, plot = FALSE)$acf[2:5], 3)
round(pacf(B, lag.max = 24, plot = FALSE)$acf[1:5], 3)

# (c) LakeHuron: 98 datos, 20 rezagos
round(1.96 / sqrt(length(LakeHuron)), 3)
fuera(LakeHuron, 20)
round(acf(LakeHuron,  lag.max = 20, plot = FALSE)$acf[2:6], 3)
round(pacf(LakeHuron, lag.max = 20, plot = FALSE)$acf[1:4], 3)
