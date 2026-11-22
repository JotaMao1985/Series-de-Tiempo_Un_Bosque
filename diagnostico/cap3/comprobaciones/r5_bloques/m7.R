x <- window(treering, start = 1880)      # los ultimos cien anios de la serie
length(x)

# (a) Los tres estimadores de un AR(2)
yw  <- ar(x, order.max = 2, aic = FALSE, method = "yule-walker")
css <- arima(x, order = c(2, 0, 0), method = "CSS")
ml  <- arima(x, order = c(2, 0, 0), method = "ML")
round(rbind(YW = yw$ar, CSS = coef(css)[1:2], ML = coef(ml)[1:2]), 4)

# (b) La distancia a ML, en errores estandar de ML
ee <- sqrt(diag(ml$var.coef))[1:2]
round(rbind(ee_ML = ee, YW_menos_ML = (yw$ar - coef(ml)[1:2]) / ee,
            CSS_menos_ML = (coef(css)[1:2] - coef(ml)[1:2]) / ee), 4)
round(Mod(polyroot(c(1, -coef(ml)[1:2]))), 4)                # modulo de las raices

# (c) El experimento: 500 series de T = 100 de cada proceso; distancia media
#     de Yule-Walker a ML, en errores estandar de ML
distancia <- function(phi) {
  d <- replicate(500, {
    s  <- arima.sim(n = 100, model = list(ar = phi))
    f  <- tryCatch(arima(s, order = c(2, 0, 0), method = "ML"), error = function(e) NULL)
    yw <- ar(s, order.max = 2, aic = FALSE, method = "yule-walker")$ar
    if (is.null(f)) c(NA, NA) else abs(yw - coef(f)[1:2]) / sqrt(diag(f$var.coef))[1:2]
  })
  c(rowMeans(d, na.rm = TRUE), sin_ajuste = sum(is.na(d[1, ])),
    modulo = min(Mod(polyroot(c(1, -phi)))))
}
set.seed(37)
round(rbind(raices_lejos = distancia(c(0.14, 0.21)),
            raices_cerca = distancia(c(1.40, -0.70))), 2)
