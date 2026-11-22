set.seed(33)
n <- 500
e <- rnorm(n + 1)                         # los choques e_0, e_1, ..., e_n
ahora <- e[-1]; antes <- e[-(n + 1)]      # e_t y e_{t-1}, para t = 1, ..., n
y_a <- ahora + 0.5 * antes                # MA(1) con theta = 0.5
y_b <- ahora + 2.0 * antes                # MA(1) con theta = 2 y los MISMOS choques

# Reconstruye los choques: e_t = y_t - theta * e_{t-1}, con 0 donde iria e_0
reconstruye <- function(y, theta) {
  rec <- numeric(length(y)); anterior <- 0
  for (t in seq_along(y)) { rec[t] <- y[t] - theta * anterior; anterior <- rec[t] }
  rec
}

# (a) y (b) El error de reconstruccion, |reconstruido - verdadero|,
#     en t = 1, 2, 5, 10 y 20
abs(e[1])                                 # |e_0|: lo unico que no se conoce
signif(abs(reconstruye(y_a, 0.5) - ahora)[c(1, 2, 5, 10, 20)], 3)
signif(abs(reconstruye(y_b, 2.0) - ahora)[c(1, 2, 5, 10, 20)], 3)

# (c) Lo que devuelve arima() con la serie de theta = 2
m <- arima(y_b, order = c(0, 0, 1), include.mean = FALSE)
round(c(theta = coef(m)[["ma1"]], sigma2 = m$sigma2), 4)
# Sus residuales NO son los choques con que se simulo la serie
round(c(con_e_t = cor(residuals(m), ahora), con_e_t_1 = cor(residuals(m), antes)), 3)
# ... pero si son ruido blanco
round(acf(residuals(m), lag.max = 3, plot = FALSE)$acf[-1], 3)
