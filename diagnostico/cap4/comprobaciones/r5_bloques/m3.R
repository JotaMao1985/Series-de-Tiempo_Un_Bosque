library(forecast)
set.seed(43)
n <- 120
escalon <- as.numeric(seq_len(n) >= 71)        # 0 hasta t = 70, 1 desde t = 71
y <- ts(10 + 3 * escalon + arima.sim(n = n, model = list(ar = 0.5)))
plot(y)                                        # el salto se ve a simple vista

pruebas <- function(x) c(kpss = ndiffs(x, test = "kpss"), adf = ndiffs(x, test = "adf"),
                         pp = ndiffs(x, test = "pp"))
# (a) el d que pide cada prueba, sobre la serie completa
pruebas(y)

# (b) y en cada tramo por separado
antes <- window(y, end = 70); despues <- window(y, start = 71)
rbind(antes = pruebas(antes), despues = pruebas(despues))
round(c(media_antes = mean(antes), media_despues = mean(despues)), 2)

# (c) el ARIMA(1,1,1) que saldria de seguir a KPSS, y sus raices
f111 <- arima(y, order = c(1, 1, 1), method = "ML")
round(c(coef(f111), raiz_MA = Mod(polyroot(c(1, coef(f111)[["ma1"]])))), 4)

# el modelo de dos medias, con un AR(1) para lo que queda
fesc <- arima(y, order = c(1, 0, 0), xreg = escalon, method = "ML")
round(rbind(coef = coef(fesc), ee = sqrt(diag(fesc$var.coef))), 3)
Box.test(residuals(fesc), lag = 20, type = "Ljung-Box", fitdf = 1)$p.value
