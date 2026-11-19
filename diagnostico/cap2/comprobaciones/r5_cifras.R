# R5 del capitulo 2 · las cifras de la prosa de los ejercicios y del quiz que NO salen
# bajo un "#>" en el propio capitulo. Cada linea lleva su etiqueta; R5_cambios.md las cita.
# Desde la raiz del repo:
#   Rscript diagnostico/cap2/comprobaciones/r5_cifras.R > diagnostico/cap2/comprobaciones/r5_cifras.out 2>&1
suppressPackageStartupMessages({library(forecast); library(tseries)})
options(warn = 1, width = 110)
et <- function(id, ...) cat(sprintf("[%s] ", id), ..., "\n")
banda <- function(x) 1.96 / sqrt(length(x))

# ---- Quiz ---------------------------------------------------------------
et("Q2-01", "(1.96/0.15)^2 =", (1.96 / 0.15)^2, "| 1.96/0.15 =", 1.96 / 0.15)
et("Q2-02", "banda con T = 170:", 1.96 / sqrt(170), "| 171:", 1.96 / sqrt(171), "| 100:", 1.96 / sqrt(100), "| 400:", 1.96 / sqrt(400))
et("Q2-03", "con 1.959964:", (qnorm(0.975) / 0.15)^2)
dl <- diff(log(AirPassengers)); r <- acf(dl, lag.max = 24, plot = FALSE)$acf[-1]
et("Q3-01", "n", length(dl), "banda", round(banda(dl), 4), "r1", round(r[1], 4), "r12", round(r[12], 4), "fuera", sum(abs(r) > banda(dl)), "en", which(abs(r) > banda(dl)))
la <- log(AirPassengers)
et("Q4-01", "r1 de log(AP) con d = 1, 2, 3:", round(sapply(1:3, function(d) acf(diff(la, differences = d), plot = FALSE)$acf[2]), 3))
set.seed(1); y <- arima.sim(list(ar = 0.8), n = 200); set.seed(4); z <- arima.sim(list(order = c(0, 1, 1), ma = -0.8), n = 143)
et("Q4-02", "AR(0.8): var", round(c(var(y), var(diff(y))), 3), "| ARIMA(0,1,1): var", round(c(var(z), var(diff(z))), 3), "r1 dif", round(acf(diff(z), plot = FALSE)$acf[2], 3))
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
et("Q4-03", "KPSS de diff(TRM): p =", suppressWarnings(kpss.test(diff(trm)))$p.value, "(tope: > 0.10) | ndiffs(TRM) =", ndiffs(trm))
et("Q4-04", "una diferencia de mas: ruido blanco diferenciado, KPSS p (5 semillas):",
   sapply(1:5, function(s) { set.seed(s); suppressWarnings(kpss.test(diff(rnorm(200))))$p.value }))
et("Q5-01", "k por defecto con T = 120:", trunc((120 - 1)^(1/3)))
set.seed(2026); cam <- cumsum(rnorm(200)); rc <- acf(cam, lag.max = 24, plot = FALSE)$acf[-1]
et("Q6-01", "caminata: r1", round(rc[1], 3), "r12", round(rc[12], 3), "| 0.5^12 =", 0.5^12, "| 0.95^12 =", round(0.95^12, 3))
et("Q7-01", "5/40 =", 100 * 5 / 40, "| 13/40 =", 100 * 13 / 40, "| 4/40 =", 100 * 4 / 40, "| 1/40 =", 100 * 1 / 40, "| 5/108 =", round(100 * 5 / 108, 1), "| quedan", 40 - 5)
gcv <- function(y, l) forecast:::guer.cv(l, y)
lg <- BoxCox.lambda(UKgas, method = "guerrero"); v <- sapply(c(1, 0, lg), function(l) gcv(UKgas, l))
et("Q8-01", "UKgas: lambda", round(lg, 4), "| criterio sin transformar, log, optimo:", round(v, 4))
et("Q8-02", "el log capta", round(100 * (v[1] - v[2]) / (v[1] - v[3]), 1), "% | log/sin =", round(v[2] / v[1], 3), "| log/optimo =", round(v[2] / v[3], 2))
b <- matrix(log(as.numeric(UKgas)), nrow = 4)
et("Q8-03", "sd de log(UKgas) por anio: tres primeros", round(apply(b, 2, sd)[1:3], 3), "| tres ultimos", round(apply(b, 2, sd)[25:27], 3), "| anios:", ncol(b))
va <- sapply(c(1, 0, BoxCox.lambda(AirPassengers, method = "guerrero")), function(l) gcv(AirPassengers, l))
et("Q8-04", "AirPassengers: el log capta", round(100 * (va[1] - va[2]) / (va[1] - va[3]), 1), "%")

# ---- Ejercicios cortos ----------------------------------------------------
et("M1-01", "varianza de la uniforme entre -sqrt(3) y sqrt(3):", (2 * sqrt(3))^2 / 12)
et("M2-01", "barras esperadas fuera por azar, de 24:", 0.05 * 24)
dax <- EuStockMarkets[, "DAX"]
et("M2-02", "DAX: dias", length(dax), "| de", paste(round(tsp(dax)[1:2], 2), collapse = " a "), "| rendimientos", length(diff(log(dax))))
et("M3-01", "anios de la ventana:", paste(time(window(discoveries, start = 1927, end = 1936)), collapse = " "))
et("M6-01", "nhtemp: pendiente de la recta (grados F por anio):", round(coef(lm(nhtemp ~ time(nhtemp)))[2], 4), "| en 60 anios:", round(59 * coef(lm(nhtemp ~ time(nhtemp)))[2], 2))
rs <- residuals(lm(nhtemp ~ time(nhtemp))); rr <- acf(rs, lag.max = 15, plot = FALSE)$acf[-1]
et("M6-02", "residuo de la recta: de 15 rezagos, fuera", sum(abs(rr) > banda(rs)), "en", which(abs(rr) > banda(rs)))
et("M8-01", "15.64 - 10.49 =", 15.64 - 10.49, "| 23.34 - 15.64 =", 23.34 - 15.64, "| media/exp(2.75) =", round(15.97 / 15.64, 4), "| exp(0.2^2/2) =", round(exp(0.02), 4))
et("M8-02", "JohnsonJohnson: max/min", round(max(JohnsonJohnson) / min(JohnsonJohnson), 1), "| primer y ultimo dato", JohnsonJohnson[1], JohnsonJohnson[84])

# ---- Ejercicios del Modulo 9 ------------------------------------------------
t0 <- Sys.time()
set.seed(2026); p5000 <- replicate(5000, suppressWarnings(adf.test(cumsum(rnorm(144)))$p.value) < 0.05)
et("E2-01", "5000 caminatas de 144: rechaza", 100 * mean(p5000), "% | error tipico", round(100 * sqrt(mean(p5000) * (1 - mean(p5000)) / 5000), 2), "| segundos", round(as.numeric(Sys.time() - t0, units = "secs"), 1))
set.seed(7); cam7 <- replicate(500, cumsum(rnorm(144))); rech <- function(x) suppressWarnings(adf.test(x)$p.value) < 0.05
et("E2-02", "con set.seed(7), el del Modulo 6: amplitud 0 ->", 100 * mean(apply(cam7, 2, rech)), "% | amplitud 4 ->", 100 * mean(apply(cam7 + 4 * sin(2 * pi * (1:144) / 12), 2, rech)), "%")
et("E2-03", "error tipico de la diferencia de dos porcentajes cerca del 20 % con 500:", round(100 * sqrt(2 * 0.2 * 0.8 / 500), 1))
et("E3-01", "USAccDeaths, nabla12: KPSS p", suppressWarnings(kpss.test(diff(USAccDeaths, lag = 12)))$p.value)
et("E4-01", "TRM fija: KPSS de tendencia p", suppressWarnings(kpss.test(trm, null = "Trend"))$p.value, "| de la diferencia", suppressWarnings(kpss.test(diff(trm), null = "Trend"))$p.value)
u <- UKDriverDeaths
et("E5-01", "UKDriverDeaths: n", length(u), "| KPSS nivel p", suppressWarnings(kpss.test(u))$p.value, "| de", paste(start(u), collapse = "-"), "a", paste(end(u), collapse = "-"))
et("E4-02", "TRM fija: nsdiffs", nsdiffs(trm), "| k por defecto", trunc((length(trm) - 1)^(1/3)))
yy <- as.numeric(window(discoveries, start = 1927, end = 1936)); dd <- yy - mean(yy)
et("M3-02", "desviaciones:", dd, "| cuadrados suman", sum(dd^2))
et("M3-03", "productos del rezago 1:", dd[1:9] * dd[2:10], "| suman", sum(dd[1:9] * dd[2:10]))
et("M3-04", "productos del rezago 2:", dd[1:8] * dd[3:10], "| suman", sum(dd[1:8] * dd[3:10]))
et("M3-05", "cocientes T/(T-k):", round(0.5229 / 0.4706, 3), round(0.0735 / 0.0588, 3))
et("M8-03", "media - exp(2.75) =", 15.97 - 15.64, "| criterio log / sin transformar en JJ:", round(0.402 / 1.081, 2))
et("E1-01", "co2: n", length(co2), "| banda de la serie de partida", round(1.96 / sqrt(length(co2)), 3), "| max/min - 1 =", round(100 * (max(co2) / min(co2) - 1), 1), "%")
et("M5-01", "1.96/sqrt(200) =", round(1.96 / sqrt(200), 3))
