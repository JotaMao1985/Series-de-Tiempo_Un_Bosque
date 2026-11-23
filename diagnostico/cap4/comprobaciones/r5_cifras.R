# R5 del capitulo 4 · cifras de prosa, enunciados, pistas, retros y claves que NO salen bajo un `#>`
# del capitulo. Cada una lleva su etiqueta ([M3-01], [P2-01]...), que es la que cita R5_cambios.md.
#   Rscript diagnostico/cap4/comprobaciones/r5_cifras.R > diagnostico/cap4/comprobaciones/r5_cifras.out 2>&1
suppressPackageStartupMessages({ library(forecast); library(tseries); library(tsibbledata) })
options(width = 150, warn = -1)
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")), "| tseries", as.character(packageVersion("tseries")),
    "| tsibbledata", as.character(packageVersion("tsibbledata")), "| fpp3", as.character(packageVersion("fpp3")), "\n\n")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
et <- function(e, ...) cat(sprintf("[%s] ", e), ..., "\n")
ge <- as.data.frame(global_economy)

# ---------------------------------------------------------------- M1 (tcm1y)
data(tcm); f2 <- arima(tcm1y, order = c(2, 0, 0), method = "ML"); f1 <- arima(tcm1y, order = c(1, 1, 0), method = "ML")
et("M1-01", "media del AR(2):", round(coef(f2)[["intercept"]], 2), "| 1/phi del ARIMA(1,1,0):", round(1 / coef(f1)[["ar1"]], 4),
   "| distancia de la raiz al circulo:", round(min(Mod(polyroot(c(1, -coef(f2)[1:2])))) - 1, 4))
et("M1-02", "inicio y fin de tcm1y (anio, mes):", start(tcm1y), "-", end(tcm1y), "| n =", length(tcm1y))

# ---------------------------------------------------------------- M2 (simulada, semilla 2026)
set.seed(2026); y <- arima.sim(n = 200, model = list(order = c(2, 1, 0), ar = c(0.4, 0.3)))
e212 <- sqrt(diag(arima(y, order = c(2, 1, 2), method = "ML")$var.coef)); e210 <- sqrt(diag(arima(y, order = c(2, 1, 0), method = "ML")$var.coef))
et("M2-01", "ee del ARIMA(2,1,2):", round(e212, 3), "| ee del ARIMA(2,1,0):", round(e210, 3), "| cocientes frente a", round(mean(e210), 4), ":", round(e212 / mean(e210), 2))
et("M2-02", "p de Ljung-Box(20) del ARIMA(0,1,1):", format(Box.test(residuals(arima(y, order = c(0, 1, 1), method = "ML")), lag = 20, type = "Ljung-Box", fitdf = 1)$p.value, digits = 3))
et("M2-03", "PACF de la diferencia, rezagos 1 a 6, fuera de la banda:", which(abs(pacf(diff(y), lag.max = 6, plot = FALSE)$acf[, 1, 1]) > 1.96 / sqrt(200)))

LB <- function(f, k) Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = k)$p.value
m2 <- t(sapply(1:200, function(s) { set.seed(s); y <- arima.sim(n = 200, model = list(order = c(2, 1, 0), ar = c(0.4, 0.3)))
  f <- lapply(list(c(0, 1, 1), c(2, 2, 1), c(2, 1, 2), c(2, 1, 0)), function(o) tryCatch(arima(y, order = o, method = "ML"), error = function(e) NULL))
  if (any(sapply(f, is.null))) return(rep(NA, 5))
  p <- pacf(diff(y), lag.max = 6, plot = FALSE)$acf[, 1, 1]; b <- 1.96 / sqrt(199)
  c(LB(f[[1]], 1) < 0.05, Mod(polyroot(c(1, coef(f[[2]])[["ma1"]]))) < 1.01, max(sqrt(diag(f[[3]]$var.coef))) > 2 * max(sqrt(diag(f[[4]]$var.coef))),
    all(abs(p[1:2]) > b) && all(abs(p[3:6]) < b), LB(f[[2]], 3) > 0.05 && LB(f[[3]], 4) > 0.05) }))
et("M2-04", "200 semillas (1 a 200): Ljung-Box rechaza el (0,1,1):", round(mean(m2[, 1], na.rm = TRUE), 3), "| |raiz MA| del (2,2,1) < 1.01:", round(mean(m2[, 2], na.rm = TRUE), 3),
   "| ee del (2,1,2) mas del doble que los del (2,1,0):", round(mean(m2[, 3], na.rm = TRUE), 3), "| PACF fuera en 1 y 2 y dentro en 3 a 6:", round(mean(m2[, 4], na.rm = TRUE), 3),
   "| (2,2,1) y (2,1,2) pasan Ljung-Box:", round(mean(m2[, 5], na.rm = TRUE), 3), "| los cinco a la vez:", round(mean(rowSums(m2) == 5, na.rm = TRUE), 3), "| semillas sin algun ajuste:", sum(is.na(m2[, 1])))

# ---------------------------------------------------------------- M3 (simulada, semilla 43) y su robustez
res <- t(sapply(1:500, function(s) { set.seed(s); n <- 120; x <- as.numeric(seq_len(n) >= 71); y <- ts(10 + 3 * x + arima.sim(n = n, model = list(ar = 0.5)))
  a <- window(y, end = 70); b <- window(y, start = 71); f <- tryCatch(arima(y, order = c(1, 1, 1), method = "ML"), error = function(e) NULL)
  c(k = ndiffs(y, test = "kpss"), ka = ndiffs(a, test = "kpss"), kb = ndiffs(b, test = "kpss"), raiz = if (is.null(f)) NA else Mod(polyroot(c(1, coef(f)[["ma1"]])))) }))
et("M3-01", "500 semillas (1 a 500): KPSS pide d >= 1 en la serie completa:", mean(res[, "k"] >= 1), "| y ademas d = 0 en los dos tramos:", mean(res[, "k"] >= 1 & res[, "ka"] == 0 & res[, "kb"] == 0),
   "| mediana de |raiz MA| del ARIMA(1,1,1):", round(median(res[, "raiz"], na.rm = TRUE), 3), "| cuartiles:", round(quantile(res[, "raiz"], c(.25, .75), na.rm = TRUE), 3))
pr <- function(x) c(ndiffs(x, test = "kpss"), ndiffs(x, test = "adf"), ndiffs(x, test = "pp"))
r3 <- t(sapply(1:500, function(s) { set.seed(s); y <- ts(10 + 3 * (1:120 >= 71) + arima.sim(n = 120, model = list(ar = 0.5)))
  c(all(pr(y) == c(1, 0, 0)), all(pr(window(y, end = 70)) == 0) && all(pr(window(y, start = 71)) == 0)) }))
et("M3-03", "500 semillas: reparto del Nilo (KPSS 1, ADF 0, PP 0) en la serie completa:", round(mean(r3[, 1]), 3), "| eso y las tres pruebas en 0 en los dos tramos:", round(mean(r3[, 1] & r3[, 2]), 3), "| la 43 cumple las dos:", all(r3[43, ]))
fn <- arima(Nile, order = c(1, 1, 1), method = "ML")
et("M3-02", "Nilo: ndiffs kpss/adf/pp:", ndiffs(Nile, test = "kpss"), ndiffs(Nile, test = "adf"), ndiffs(Nile, test = "pp"), "| raiz MA del ARIMA(1,1,1):", round(Mod(polyroot(c(1, coef(fn)[["ma1"]]))), 3))

# ---------------------------------------------------------------- M4 (importaciones de Colombia)
col <- ts(ge[ge$Country == "Colombia", "Imports"], start = 1960)
et("M4-01", "teoricos con coeficiente -0.29: PACF(2) de un MA(1):", round(ARMAacf(ma = -0.29, lag.max = 2, pacf = TRUE)[2], 3), "| ACF(2) de un AR(1):", round(ARMAacf(ar = -0.29, lag.max = 2)[3], 3))
m <- lapply(list(c(0, 1, 1), c(1, 1, 0), c(1, 1, 1), c(0, 1, 0)), function(o) arima(col, order = o, method = "ML"))
a <- sapply(m, aicc, n = length(col) - 1); b <- sapply(m, BIC)
et("M4-02", "AICc menos el mejor:", round(a - min(a), 3), "| BIC menos el mejor:", round(b - min(b), 3), "| n =", length(col), "| anios", start(col)[1], end(col)[1])
w <- diff(col); et("M4-03", "rezagos (1 a 10) fuera de la banda: ACF", which(abs(acf(w, lag.max = 10, plot = FALSE)$acf[-1]) > 1.96 / sqrt(length(w))), "| PACF", which(abs(pacf(w, lag.max = 10, plot = FALSE)$acf[, 1, 1]) > 1.96 / sqrt(length(w))))

# ---------------------------------------------------------------- M5 (airmiles)
y <- log(airmiles); s0 <- Arima(y, order = c(0, 1, 1)); s1 <- Arima(y, order = c(0, 1, 1), include.drift = TRUE)
et("M5-01", "AICc sin menos con:", round(s0$aicc - s1$aicc, 2), "| exp(deriva):", round(exp(coef(s1)[["drift"]]), 2), "| exp(10*deriva):", round(exp(10 * coef(s1)[["drift"]]), 1),
   "| auto.arima:", as.character(auto.arima(y)))

# ---------------------------------------------------------------- M6 (GOOG 2018)
g <- subset(as.data.frame(gafa_stock), Symbol == "GOOG" & format(Date, "%Y") == "2018"); y <- ts(g$Close); n <- length(y)
r1 <- outer(0:2, 0:2, Vectorize(function(p, q) aicc(arima(y, order = c(p, 1, q), method = "ML"), n - 1)))
et("M6-01", "ndiffs kpss/adf/pp:", ndiffs(y, test = "kpss"), ndiffs(y, test = "adf"), ndiffs(y, test = "pp"), "| d = 1: exceso de AICc de los otros ocho sobre el (0,1,0): de",
   round(min(r1[-1] - r1[1]), 2), "a", round(max(r1[-1] - r1[1]), 2), "| n efectivo:", n - 1, n - 2, "| fechas:", format(range(g$Date)))

# ---------------------------------------------------------------- M7 (NelPlo ip)
data(NelPlo); ip <- na.omit(NelPlo[, "ip"])
q <- sapply(0:5, function(q) Arima(ip, order = c(0, 1, q), include.drift = TRUE)$aicc)
et("M7-02", "rango de ip:", round(range(ip), 3))
et("M7-01", "AICc del ARIMA(0,1,q) con deriva, q = 0..5:", round(q, 3), "| diferencia entre q = 0 y q = 5:", round(q[1] - q[6], 2), "| anios", start(ip)[1], end(ip)[1], "n", length(ip))

# ---------------------------------------------------------------- M8 (simulada, semilla 2026) y su robustez
r <- sapply(1:200, function(s) { set.seed(s); y <- arima.sim(n = 200, model = list(ar = 0.8)); f <- tryCatch(arima(y, order = c(1, 1, 1), method = "ML"), error = function(e) NULL)
  if (is.null(f)) NA else Mod(polyroot(c(1, coef(f)[["ma1"]]))) })
et("M8-01", "200 semillas (1 a 200): |raiz MA| del ARIMA(1,1,1) < 1.05 en la fraccion", round(mean(r < 1.05, na.rm = TRUE), 3), "| sin ajuste:", sum(is.na(r)))
et("M8-02", "rho_1 teorico de la diferencia de un AR(1) con phi = 0.8: -(1-phi)/2 =", -(1 - 0.8) / 2, "| con ARMAacf(ar = 0.8, ma = -1):", round(ARMAacf(ar = 0.8, ma = -1, lag.max = 1)[2], 4))

# ---------------------------------------------------------------- M9 (austres), tras la verificacion
A <- Arima(austres, order = c(0, 1, 1)); B <- Arima(austres, order = c(0, 1, 1), include.drift = TRUE); C <- Arima(austres, order = c(0, 2, 1))
wb <- as.numeric(forecast(B, h = 40, level = 95)$upper - forecast(B, h = 40, level = 95)$lower); wc <- as.numeric(forecast(C, h = 40, level = 95)$upper - forecast(C, h = 40, level = 95)$lower)
et("M9-01", "austres: n =", length(austres), "| inicio y fin (anio, trimestre):", start(austres), "-", end(austres), "| ndiffs kpss/adf/pp:", ndiffs(austres, test = "kpss"), ndiffs(austres, test = "adf"), ndiffs(austres, test = "pp"))
et("M9-02", "ancho 95 % a h = 40, C entre B:", round(wc[40] / wb[40], 1), "| a h = 1:", round(wc[1] / wb[1], 2), "| B menos C a h = 40:", round(forecast(B, h = 40)$mean[40] - forecast(C, h = 40)$mean[40], 1),
   "| ancho de B, h = 40 entre h = 1:", round(wb[40] / wb[1], 1), "| de C:", round(wc[40] / wc[1], 1), "| raiz de 40:", round(sqrt(40), 1))
et("M9-03", "theta: A", round(coef(A)[["ma1"]], 3), "| B", round(coef(B)[["ma1"]], 3), "| C", round(coef(C)[["ma1"]], 3), "| t de la deriva de B:", round(coef(B)[["drift"]] / sqrt(diag(B$var.coef))[["drift"]], 1))

# ---------------------------------------------------------------- E1 (BJsales)
n <- length(BJsales); g1 <- sapply(list(c(0,1,0), c(1,1,0), c(2,1,0), c(0,1,1), c(1,1,1), c(2,1,1), c(0,1,2), c(1,1,2), c(2,1,2)), function(o) aicc(arima(BJsales, order = o, method = "ML"), n - 1))
f122 <- arima(BJsales, order = c(1, 2, 2), method = "ML"); th <- coef(f122)[c("ma1", "ma2")]
et("E1-01", "puesto del IMA(1,1) por AICc entre los nueve de d = 1:", rank(g1)[4], "| distancia al mejor:", round(g1[4] - min(g1), 1))
f111 <- arima(BJsales, order = c(1, 1, 1), method = "ML")
et("E1-03", "ARIMA(1,1,1) por ML, a tres decimales: phi, theta:", round(coef(f111), 3), "| ee:", round(sqrt(diag(f111$var.coef)), 3))
et("E1-02", "ARIMA(1,2,2): theta(B) = 1", round(th[1], 4), "B +", round(th[2], 4), "B^2; (1 - B)(1 - c B) con c =", round(th[2], 4), "da 1", round(-(1 + th[2]), 4), "B +", round(th[2], 4), "B^2",
   "| LB(20) p:", round(Box.test(residuals(f122), lag = 20, type = "Ljung-Box", fitdf = 3)$p.value, 3))

# ---------------------------------------------------------------- E2 (liebre) y el lince
x <- ts(log(pelt$Hare), start = 1845); fa <- arima(x, order = c(2, 0, 0), method = "ML"); rr <- polyroot(c(1, -coef(fa)[1:2]))
et("E2-01", "caida de la varianza al diferenciar:", round(100 * (1 - var(diff(x)) / var(x))), "% | AR(2): raices complejas:", all(abs(Im(rr)) > 1e-8), "periodo:", round(2 * pi / abs(Arg(rr[1])), 1),
   "| anios", range(pelt$Year), "n", length(x))

# ---------------------------------------------------------------- P1 (pasajeros aereos de Australia)
ap <- ts(fpp3::aus_airpassengers$Passengers, start = 1970); n <- length(ap)
for (d in 1:2) { g <- expand.grid(p = 0:2, q = 0:2); g$a <- mapply(function(p, q) aicc(arima(ap, order = c(p, d, q), method = "ML"), n - d), g$p, g$q); i <- which.min(g$a)
  et(sprintf("P1-0%d", d), sprintf("d = %d: mejor ARIMA(%d,%d,%d), AICc %.2f, n efectivo %d", d, g$p[i], d, g$q[i], g$a[i], n - d)) }
et("P1-03", "n =", n, "| anios", range(fpp3::aus_airpassengers$Year), "| ndiffs kpss/adf/pp:", ndiffs(ap, test = "kpss"), ndiffs(ap, test = "adf"), ndiffs(ap, test = "pp"))

# ---------------------------------------------------------------- P2 (ARIMA(1,1,0) con phi = 0.5 y sigma = 2)
psi <- c(1, ARMAtoMA(ar = c(1.5, -0.5), lag.max = 3)); s <- 2
et("P2-01", "psi_0..psi_3:", psi, "| forma cerrada (1 - phi^(j+1))/(1 - phi):", (1 - 0.5^(1:4)) / 0.5)
et("P2-02", "sigma_3 =", round(s * sqrt(sum(psi[1:3]^2)), 4), "| suma de cuadrados:", sum(psi[1:3]^2))
et("P2-03", "tropiezos: sin psi_0:", round(s * sqrt(sum(psi[2:3]^2)), 2), "| sin elevar al cuadrado:", round(s * sqrt(sum(psi[1:3])), 2), "| psi_j = phi^j (olvidar la diferencia):", round(s * sqrt(sum(0.5^(2 * (0:2)))), 2),
   "| caminata (psi_j = 1):", round(s * sqrt(3), 2), "| cuatro pesos:", round(s * sqrt(sum(psi[1:4]^2)), 2), "| sin sigma:", round(sqrt(sum(psi[1:3]^2)), 2), "| sin la raiz:", round(s * sum(psi[1:3]^2), 2),
   "| raiz redondeada a 2.5:", s * 2.5, "| a 2.51:", s * 2.51)

# ---------------------------------------------------------------- P5 (beaver2)
y <- ts(beaver2$temp); m <- lm(temp ~ activ, data = beaver2); e <- ts(residuals(m))
et("P5-01", "n =", length(y), "| primera lectura con activ = 1:", which(beaver2$activ == 1)[1], "| medias:", round(tapply(beaver2$temp, beaver2$activ, mean), 3), "| escalon:", round(coef(m)[["activ"]], 2))
et("P5-02", "serie completa: KPSS p =", kpss.test(y)$p.value, "(el aviso dice que es menor) | ADF p =", round(adf.test(y)$p.value, 2), "| ndiffs kpss/adf/pp:", ndiffs(y, test = "kpss"), ndiffs(y, test = "adf"), ndiffs(y, test = "pp"))
et("P5-03", "quitado el escalon: KPSS p =", kpss.test(e)$p.value, "(el aviso dice que es mayor) | r1 de lo que queda:", round(acf(e, plot = FALSE)$acf[2], 2))

tr1 <- ts(beaver2$temp[1:38]); tr2 <- ts(beaver2$temp[39:100])
et("P5-04", "ndiffs kpss/adf/pp en cada tramo: lecturas 1 a 38:", pr(tr1), "| lecturas 39 a 100:", pr(tr2))

# ---------------------------------------------------------------- P6 y P7 (exportaciones de Chile)
ch <- ts(ge[ge$Country == "Chile", "Exports"], start = 1960); r <- acf(ch, lag.max = 20, plot = FALSE)$acf[-1]; rd <- acf(diff(ch), lag.max = 20, plot = FALSE)$acf[-1]
et("P6-01", "n =", length(ch), "| anios", start(ch)[1], end(ch)[1], "| banda de la serie:", round(1.96 / sqrt(length(ch)), 3), "| ACF 1..20:"); cat("       ", paste(sprintf("%.3f", r), collapse = ", "), "\n")
et("P6-02", "rezagos fuera de la banda:", which(abs(r) > 1.96 / sqrt(length(ch))), "| con d = 1, banda", round(1.96 / sqrt(length(ch) - 1), 3), "fuera:", which(abs(rd) > 1.96 / sqrt(length(ch) - 1)), "valor", round(rd[abs(rd) > 1.96 / sqrt(length(ch) - 1)], 3),
   "| ndiffs:", ndiffs(ch, test = "kpss"), ndiffs(ch, test = "adf"), ndiffs(ch, test = "pp"))
tr <- function(...) { t <- capture.output(f <- auto.arima(ch, trace = TRUE, ...)); t <- grep("^ ARIMA", t, value = TRUE); d <- data.frame(m = trimws(sub(":.*", "", t)), a = as.numeric(sub(".*:", "", t))); list(f = f, d = d[order(d$a), ]) }
e1 <- tr(); e2 <- tr(stepwise = FALSE, approximation = FALSE)
et("P7-01", "escalonada:", as.character(e1$f), round(e1$f$aicc, 2), "(", nrow(e1$d), "modelos ) | exhaustiva:", as.character(e2$f), round(e2$f$aicc, 2), "(", nrow(e2$d), "modelos )")
et("P7-02", "los cuatro primeros de la exhaustiva:"); print(head(e2$d, 4), row.names = FALSE)
et("P7-03", "distancia al primero del 2.o, 3.o y 4.o:", round(e2$d$a[2:4] - e2$d$a[1], 2), "| a menos de 2 puntos del primero:", sum(e2$d$a - e2$d$a[1] < 2))

# ---------------------------------------------------------------- P8 (importaciones de Peru)
pe <- ts(ge[ge$Country == "Peru", "Imports"], start = 1960)
et("P8-01", "n =", length(pe), "| anios", start(pe)[1], end(pe)[1], "| ndiffs kpss/adf/pp:", ndiffs(pe, test = "kpss"), ndiffs(pe, test = "adf"), ndiffs(pe, test = "pp"))
for (d in 1:2) { w <- diff(pe, differences = d); f <- arima(w, order = c(0, 0, 1), include.mean = FALSE, method = "ML")
  et(sprintf("P8-0%d", d + 1), sprintf("d = %d: Var = %.2f | r1 = %.3f | theta de un MA(1) = %.4f | |raiz MA| = %.4f | sigma2 = %.2f | Ljung-Box(10) p = %.2f", d, var(w), acf(w, plot = FALSE)$acf[2], coef(f)[["ma1"]],
     Mod(polyroot(c(1, coef(f)[["ma1"]]))), f$sigma2, Box.test(residuals(f), lag = 10, type = "Ljung-Box", fitdf = 1)$p.value)) }
a1 <- aicc(arima(pe, order = c(0, 1, 1), method = "ML"), length(pe) - 1); a2 <- aicc(arima(pe, order = c(0, 2, 1), method = "ML"), length(pe) - 2)
et("P8-04", "AICc del ARIMA(0,1,1):", round(a1, 2), "| del ARIMA(0,2,1):", round(a2, 2))
