library(forecast)
y <- austres                         # residentes en Australia, en miles; 89 trimestres
A <- Arima(y, order = c(0, 1, 1))                           # d = 1, sin deriva
B <- Arima(y, order = c(0, 1, 1), include.drift = TRUE)     # d = 1, con deriva
C <- Arima(y, order = c(0, 2, 1))                           # d = 2
h <- c(1, 20, 40)
pa <- forecast(A, h = 40, level = 95); pb <- forecast(B, h = 40, level = 95)
pc <- forecast(C, h = 40, level = 95)

# (a) el pronostico puntual a 1, 20 y 40 trimestres
round(rbind(A = pa$mean[h], B = pb$mean[h], C = pc$mean[h]), 1)

# (b) la pendiente del pronostico al final (h = 40) y de donde sale
round(c(A = diff(pa$mean)[39], B = diff(pb$mean)[39], C = diff(pc$mean)[39]), 2)
round(c(deriva_de_B = coef(B)[["drift"]], media_de_las_diferencias = mean(diff(y)),
        ultimas_8_diferencias = mean(tail(diff(y), 8))), 2)
round(c(ultimo_dato = as.numeric(tail(y, 1)), nivel_de_A = pa$mean[40]), 1)

# (c) el ancho del intervalo del 95 %, a 1 y a 40 trimestres
ancho <- function(p) as.numeric(p$upper - p$lower)[c(1, 40)]
round(rbind(A = ancho(pa), B = ancho(pb), C = ancho(pc)), 1)

# y el diagnostico de los tres: Ljung-Box(10)
round(sapply(list(A = A, B = B, C = C), function(f)
  Box.test(residuals(f), lag = 10, type = "Ljung-Box", fitdf = 1)$p.value), 4)