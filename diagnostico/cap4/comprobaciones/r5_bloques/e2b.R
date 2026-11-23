ly <- log(lynx)
c(kpss = forecast::ndiffs(ly, test = "kpss"), adf = forecast::ndiffs(ly, test = "adf"),
  pp = forecast::ndiffs(ly, test = "pp"))
round(c(var_d0 = var(ly), var_d1 = var(diff(ly)), caida = 1 - var(diff(ly)) / var(ly)), 4)
r1 <- acf(ly, plot = FALSE)$acf[2]
round(c(r1 = r1, cociente = var(diff(ly)) / var(ly), dos_por_1_menos_r1 = 2 * (1 - r1),
        r1_de_la_diferencia = acf(diff(ly), plot = FALSE)$acf[2]), 3)
f <- arima(ly, order = c(2, 1, 1), method = "ML")
round(c(theta = coef(f)[["ma1"]], raiz_MA = Mod(polyroot(c(1, coef(f)[["ma1"]])))), 4)
