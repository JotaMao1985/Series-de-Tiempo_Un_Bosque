library(forecast)

# ACF teorica de un proceso estacional: se EXPANDE el polinomio y se usa
# ARMAacf, que no sabe nada de estacionalidad. m = 12.
acf_sarima <- function(phi = numeric(0), Phi = 0, theta = numeric(0), Theta = 0,
                       m = 12, lag.max = 36) {
  poli_est <- function(c0) { v <- numeric(m + 1); v[1] <- 1; v[m + 1] <- c0; v }
  mult <- function(a, b) {
    r <- numeric(length(a) + length(b) - 1)
    for (i in seq_along(a)) for (j in seq_along(b)) r[i+j-1] <- r[i+j-1] + a[i]*b[j]
    r
  }
  recorta <- function(v) { nz <- which(abs(v) > 1e-12); if (!length(nz)) numeric(0) else v[seq_len(max(nz))] }
  ar <- recorta(-mult(c(1, -phi),   poli_est(-Phi))[-1])
  ma <- recorta( mult(c(1,  theta), poli_est( Theta))[-1])
  ARMAacf(ar = ar, ma = ma, lag.max = lag.max)[-1]
}

# SAR(1): picos limpios, nada entre medias
round(acf_sarima(Phi = 0.7)[c(1, 11, 12, 13, 24)], 4)
#> [1] 0.0000 0.0000 0.7000 0.0000 0.4900

# AR(1) x SAR(1): aparecen los satelites en 11 y 13
round(acf_sarima(phi = 0.6, Phi = 0.7)[c(1, 11, 12, 13, 24)], 4)
#> [1] 0.6016 0.4230 0.7011 0.4218 0.4908
# y en efecto 0.6016 * 0.7011 = 0.4218

# El airline estimado sobre log(AirPassengers)
round(acf_sarima(theta = -0.4018, Theta = -0.5569)[c(1, 11, 12, 13, 24)], 4)
#> [1] -0.3459  0.1471 -0.4251  0.1471  0.0000