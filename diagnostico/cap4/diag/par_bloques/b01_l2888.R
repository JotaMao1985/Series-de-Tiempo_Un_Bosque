data(Nile)          # datasets de R base: caudal anual 1871-1970
length(Nile)
#> [1] 100

# Un ARIMA(1,1,1) es un ARMA(2,1) con una raiz unitaria impuesta.
# Se comprueba expandiendo el polinomio:
phi <- 0.2544
ar_expandido <- c(1 + phi, -phi)     # phi*_1 = 1 + phi, phi*_2 = -phi
round(ar_expandido, 4)
#> [1]  1.2544 -0.2544
sum(ar_expandido)                    # la firma de la raiz unitaria: suma 1
#> [1] 1

round(Mod(polyroot(c(1, -ar_expandido))), 4)
#> [1] 1.0000 3.9308           una raiz JUSTO sobre el circulo unitario

# Simular un ARIMA(1,1,1) es simular el ARMA(1,1) y acumular (integrar):
set.seed(2026)
w <- arima.sim(list(ar = 0.2544, ma = -0.8741), n = 200)  # la diferencia
y <- cumsum(w)                                            # la serie integrada
round(c(var_w = var(w), var_y = var(y), razon = var(y) / var(w)), 3)
#>  var_w  var_y  razon
#>  1.426  1.434  1.006     <- ?! integrar NO disparo la varianza

# Con el mismo AR pero SIN el termino MA la historia es la esperada:
set.seed(2026)
w0 <- arima.sim(list(ar = 0.2544), n = 200)
round(var(cumsum(w0)) / var(w0), 1)
#> [1] 32.8                  aqui integrar la multiplica por 33

# arima.sim lo hace directamente con order = c(p, d, q)
set.seed(2026)
y2 <- arima.sim(list(order = c(1, 1, 1), ar = 0.2544, ma = -0.8741), n = 200)
length(y2)                # devuelve n + d valores (arranca en y_0)
#> [1] 201