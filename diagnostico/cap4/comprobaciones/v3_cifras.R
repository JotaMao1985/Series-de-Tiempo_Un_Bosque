# V3 · verificador independiente de la R3 del capítulo 4.
# Recalcula en R, sin mirar r3_cifras.R, las cifras que la ronda escribe, mueve o deja en la prosa.
# Uso (desde la raíz del repo):  Rscript diagnostico/cap4/comprobaciones/v3_cifras.R > diagnostico/cap4/comprobaciones/v3_cifras.out
suppressMessages({ library(forecast); library(tseries) })
cat("R", R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")), "\n\n")

sec <- function(x) cat("\n==== ", x, " ====\n", sep = "")
r <- function(x, k = 4) round(x, k)

# --------------------------------------------------------------------------- M1
sec("M1 · ARIMA(1,1,1) del Nilo por ML (bloque nuevo)")
f <- arima(Nile, order = c(1, 1, 1), method = "ML")
print(r(rbind(coef = coef(f), ee = sqrt(diag(f$var.coef)))))
phi <- r(coef(f)[["ar1"]]); theta <- r(coef(f)[["ma1"]])
cat("phi =", phi, " theta =", theta, "\n")
cat("raiz MA     :", r(Mod(polyroot(c(1, theta))), 3), "  (1/|theta| =", r(1 / abs(theta), 3), ")\n")
cat("raices AR* :", r(Mod(polyroot(c(1, -c(1 + phi, -phi)))), 4), "\n")
cat("1/phi       :", r(1 / phi, 4), "\n")
set.seed(2026); w <- arima.sim(list(ar = phi, ma = theta), n = 200); y <- cumsum(w)
print(r(c(var_w = var(w), var_y = var(y), razon = var(y) / var(w)), 3))
set.seed(2026); w0 <- arima.sim(list(ar = phi), n = 200); cat("razon sin MA:", r(var(cumsum(w0)) / var(w0), 1), "\n")
set.seed(2026); y2 <- arima.sim(list(order = c(1, 1, 1), ar = phi, ma = theta), n = 200); cat("length(y2) =", length(y2), "\n")
# la tabla de los casos particulares: alfa = 1 + theta del IMA(1,1)
ma1 <- arima(Nile, order = c(0, 1, 1), method = "ML")
cat("IMA(1,1): theta =", r(coef(ma1)[["ma1"]]), " ee =", r(sqrt(ma1$var.coef[1, 1])), " alfa = 1 + theta =", r(1 + coef(ma1)[["ma1"]], 3),
    "  alfa (4 dec) =", r(1 + coef(ma1)[["ma1"]], 4), "\n")
cat("LB(20) fitdf=1 p =", Box.test(residuals(ma1), lag = 20, type = "Ljung-Box", fitdf = 1)$p.value, "\n")
# SES equivalente: ses() con alpha optimo, para ver que la equivalencia no es solo formal
ets_ses <- ets(Nile, model = "ANN")
cat("ETS(A,N,N) alpha optimo =", r(ets_ses$par[["alpha"]], 4), " (no es lo mismo que 1+theta del ML: otra estimacion)\n")

# --------------------------------------------------------------------------- M2
sec("M2 · esqueleto: d impreso")
d <- ndiffs(Nile); print(d)
aj <- arima(Nile, order = c(1, d, 1), method = "ML")
cat("LB(20) fitdf=2 p =", Box.test(residuals(aj), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value, "\n")
print(r(as.numeric(forecast(aj, h = 10)$mean[1:3]), 2))

# --------------------------------------------------------------------------- M3
sec("M3 · PP, dos medias, ndiffs, experimento del escalón")
pp <- PP.test(Nile); print(pp); cat("PP stat =", r(unname(pp$statistic), 6), " p =", pp$p.value, "\n")
cat("adf.test p =", adf.test(Nile)$p.value, " stat =", r(unname(adf.test(Nile)$statistic), 4), "\n")
suppressWarnings(k <- kpss.test(Nile)); cat("kpss stat =", r(unname(k$statistic), 4), " p =", k$p.value, "\n")
cat("ndiffs kpss/adf/pp:", sapply(c("kpss", "adf", "pp"), function(t) ndiffs(Nile, test = t)), "\n")
r1 <- acf(Nile, plot = FALSE)$acf[2]
cat("r1 =", r(r1, 3), " 2(1-r1) =", r(2 * (1 - r1), 3), " cociente var(diff)/var =", r(var(diff(Nile)) / var(Nile), 3), "\n")
cat("var d=0..3:", sapply(0:3, function(d) r(var(if (d == 0) Nile else diff(Nile, differences = d)), 2)), "\n")
cat("r1 de diff d=1,2:", r(sapply(1:2, function(d) acf(diff(Nile, differences = d), plot = FALSE)$acf[2]), 3), "\n")
escalon <- as.numeric(1:100 >= 29)
dm <- arima(Nile, order = c(0, 0, 0), xreg = escalon, method = "ML")
print(coef(dm)); cat("ee:", r(sqrt(diag(dm$var.coef)), 2), "\n")
cat("medias:", r(mean(Nile[1:28]), 2), r(mean(Nile[29:100]), 2), " dif:", r(mean(Nile[29:100]) - mean(Nile[1:28]), 2), "\n")
cat("sd(residuals) =", r(sd(residuals(dm)), 2), "  sqrt(sigma2 ML) =", r(sqrt(dm$sigma2), 2), "  sigma OLS (n-2) =",
    r(summary(lm(Nile ~ escalon))$sigma, 2), "\n")
cat("beta/ee (t) =", r(coef(dm)[["escalon"]] / sqrt(diag(dm$var.coef))[["escalon"]], 2), "\n")
cat("t=1899 es la obs.", 1899 - 1871 + 1, "; Nile[29] =", Nile[29], "\n")
simula <- function(beta, reps = 400) mean(replicate(reps, {
  x <- 1000 + beta * escalon + rnorm(100, 0, 127.03)
  suppressWarnings(kpss.test(x)$p.value) <= 0.05 }))
set.seed(2026); cat("simula(0), simula(-247.78):", c(simula(0), simula(-247.78)), "\n")
cat("beta/sigma =", r(247.78 / 127.03, 3), "; 100/127.03 =", r(100 / 127.03, 3), "\n")

# --------------------------------------------------------------------------- M5 (T) y M10 (deriva)
sec("M5/M10 · deriva del Nilo y de la TRM")
fd <- Arima(Nile, order = c(1, 1, 1), include.drift = TRUE)
cat("Nilo ARIMA(1,1,1)+deriva: delta =", r(coef(fd)[["drift"]], 3), " ee =", r(sqrt(fd$var.coef["drift", "drift"]), 3),
    " t =", r(coef(fd)[["drift"]] / sqrt(fd$var.coef["drift", "drift"]), 2), " phi =", r(coef(fd)[["ar1"]], 3), "\n")
cat("AICc con/sin deriva:", r(fd$aicc, 2), r(Arima(Nile, order = c(1, 1, 1))$aicc, 2), "\n")
cat("media de las diferencias Nilo =", r(mean(diff(Nile)), 3), " = (740-1120)/99 =", r((Nile[100] - Nile[1]) / 99, 3), "\n")
cat("aporte del escalon de 1899 a esa media: ", r(-247.78 / 99, 3), "\n")
cat(">>> delta-hat del ARIMA(1,1,1)+deriva NO es la media de las diferencias:", r(coef(fd)[["drift"]], 3), "vs", r(mean(diff(Nile)), 3), "\n")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
cat("n TRM =", length(trm), "\n")
fdt <- Arima(trm, order = c(0, 1, 0), include.drift = TRUE)
cat("TRM RW+deriva: delta =", r(coef(fdt)[["drift"]], 3), " ee =", r(sqrt(fdt$var.coef[1, 1]), 3),
    " t =", r(coef(fdt)[["drift"]] / sqrt(fdt$var.coef[1, 1]), 2), "\n")
cat("media de diff(TRM) =", r(mean(diff(trm)), 3), " = (y_n - y_1)/(n-1) =", r((as.numeric(trm)[138] - as.numeric(trm)[1]) / 137, 3), "\n")

# --------------------------------------------------------------------------- M6 / M7
sec("M6 · explorador: 27 modelos, ML, AICc con n efectivo, LB(20) fitdf = p + q")
filas <- list()
for (d in 0:2) for (p in 0:2) for (q in 0:2) {
  fit <- tryCatch(arima(Nile, order = c(p, d, q), method = "ML"), error = function(e) NULL)
  if (is.null(fit)) { filas[[length(filas) + 1]] <- data.frame(p, d, q, aicc = NA); next }
  k <- length(fit$coef) + 1
  aicc <- fit$aic + 2 * k * (k + 1) / (fit$nobs - k - 1)
  lb <- Box.test(residuals(fit), lag = 20, type = "Ljung-Box", fitdf = p + q)$p.value
  ma <- fit$coef[grepl("^ma", names(fit$coef))]; ar <- fit$coef[grepl("^ar", names(fit$coef))]
  filas[[length(filas) + 1]] <- data.frame(p, d, q, aicc = aicc, bic = BIC(fit), nobs = fit$nobs, lb = lb,
    raiz_ar = if (length(ar)) min(Mod(polyroot(c(1, -ar)))) else NA, raiz_ma = if (length(ma)) min(Mod(polyroot(c(1, ma)))) else NA)
}
G <- do.call(rbind, filas)
write.csv(G, file.path(Sys.getenv("V3_TMP", tempdir()), "v3_rejilla.csv"), row.names = FALSE)
G$mejor_d <- ave(G$aicc, G$d, FUN = function(x) min(x, na.rm = TRUE))
G$delta <- G$aicc - G$mejor_d
G$cerca <- G$delta < 2
G$rechaza <- G$lb < 0.05
print(r(G[order(G$d, G$aicc), c("p", "d", "q", "aicc", "delta", "lb", "raiz_ar", "raiz_ma")], 3), row.names = FALSE)
cat("\nmodelos con LB(20) < 0.05 en los 27:", sum(G$rechaza, na.rm = TRUE), "  (por d:", tapply(G$rechaza, G$d, sum, na.rm = TRUE), ")\n")
cat("modelos con LB<0.05 con d=1:", paste(G$p[G$d == 1 & G$rechaza], G$d[G$d == 1 & G$rechaza], G$q[G$d == 1 & G$rechaza]), "\n")
for (dd in 0:2) cat("d =", dd, ": cerca del mejor (delta < 2):", sum(G$cerca[G$d == dd], na.rm = TRUE), " de ellos que rechazan LB:",
                    sum(G$cerca[G$d == dd] & G$rechaza[G$d == dd], na.rm = TRUE), " (distintos del mejor:", sum(G$cerca[G$d == dd]) - 1, ")\n")
cat("con d = 1, modelos a menos de 2 puntos 'sin constante': ", paste0("(", G$p[G$d == 1 & G$cerca], ",1,", G$q[G$d == 1 & G$cerca], ")", collapse = " "), "\n")
for (dd in 0:2) {
  m <- G[G$d == dd & G$delta == 0, ]
  cat("mejor de d =", dd, ": (", m$p, ",", dd, ",", m$q, ") AICc =", r(m$aicc, 2), " raiz AR =", r(m$raiz_ar, 3), " raiz MA =", r(m$raiz_ma, 3), "\n")
}
cat("raices MA de los modelos cerca del mejor con d = 2:", r(G$raiz_ma[G$d == 2 & G$cerca], 3), "\n")
cat("mejor AICc global:", r(min(G$aicc, na.rm = TRUE), 2), " en", with(G[which.min(G$aicc), ], paste0("(", p, ",", d, ",", q, ")")), " n efectivo", G$nobs[which.min(G$aicc)], "\n")

sec("M7 · podio exhaustivo de auto.arima (trace)")
tr <- capture.output(aa <- auto.arima(Nile, stepwise = FALSE, approximation = FALSE, trace = TRUE))
cat(as.character(aa), "\n")
mods <- grep("^ ARIMA", tr, value = TRUE)
cat("modelos evaluados (lineas ARIMA de la traza):", length(mods), "\n")
v <- do.call(rbind, lapply(mods, function(l) {
  m <- regmatches(l, regexec("^ (ARIMA\\([0-9,]+\\)[^:]*) *: *([0-9.]+|Inf)", l))[[1]]
  data.frame(modelo = trimws(m[2]), aicc = suppressWarnings(as.numeric(m[3])))
}))
v <- v[order(v$aicc), ]; v$delta <- v$aicc - v$aicc[1]
print(head(v, 9), row.names = FALSE)
cat("a menos de 2 puntos del mejor:", sum(v$delta < 2, na.rm = TRUE), "\n")
st <- capture.output(auto.arima(Nile, trace = TRUE)); cat("modelos (escalonada):", length(grep("^ ARIMA", st)), "\n")

# --------------------------------------------------------------------------- M8
sec("M8 · escalon (e.e., t, AICc) y fuera de muestra 1951-1970")
cat("ee beta =", r(sqrt(diag(dm$var.coef))[["escalon"]], 2), "\n")
ent <- window(Nile, end = 1950); pru <- window(Nile, start = 1951)
cat("entrenamiento:", length(ent), " prueba:", length(pru), "\n")
mt <- function(p) c(RMSE = sqrt(mean((pru - p)^2)), MAE = mean(abs(pru - p)))
f111 <- Arima(ent, order = c(1, 1, 1))
esc_tr <- as.numeric(time(ent) >= 1899); esc_te <- rep(1, 20)
fe <- Arima(ent, order = c(0, 0, 0), xreg = esc_tr)
fe_ar <- Arima(ent, order = c(1, 0, 0), xreg = esc_tr)
print(r(rbind(naive = mt(rep(tail(ent, 1), 20)), arima111 = mt(forecast(f111, h = 20)$mean),
              escalon = mt(forecast(fe, h = 20, xreg = esc_te)$mean),
              escalon_AR1 = mt(forecast(fe_ar, h = 20, xreg = esc_te)$mean),
              media = mt(rep(mean(ent), 20))), 2))
cat("AICc escalon (d=0, ML, n=100):", { fe_all <- arima(Nile, order = c(0, 0, 0), xreg = escalon, method = "ML"); k <- 3; r(fe_all$aic + 2 * k * (k + 1) / (100 - k - 1), 2) }, "\n")
cat("desv. tipica de los residuales del ARIMA(1,1,1):", r(sd(residuals(Arima(Nile, order = c(1, 1, 1)))), 2), "\n")
# ARMA d=0 mejor sin escalon
a0 <- G[G$d == 0, ]; cat("mejor ARMA d=0 sin escalon: AICc", r(min(a0$aicc, na.rm = TRUE), 2), "\n")

# --------------------------------------------------------------------------- M9
sec("M9 · forma del pronóstico (842.17, 816.18, psi_inf, sigma30/sigma1)")
f2 <- Arima(Nile, order = c(1, 1, 1))
fc <- forecast(f2, h = 30)
cat("pronostico h=1:", r(fc$mean[1], 2), " h=30:", r(fc$mean[30], 2), " h=8..:", r(fc$mean[c(5, 8, 10)], 2), " ultimo dato:", Nile[100], "\n")
ph <- coef(f2)[["ar1"]]; th <- coef(f2)[["ma1"]]; s <- sqrt(f2$sigma2)
psi <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = 40))
sig <- s * sqrt(cumsum(psi^2))
cat("psi_inf = (1+th)/(1-ph) =", r((1 + th) / (1 - ph), 4), " sigma30/sigma1 =", r(sig[30] / sig[1], 3), " sqrt(30) =", r(sqrt(30), 2), "\n")

# --------------------------------------------------------------------------- M10 · Nilo, tabla
sec("M10 · tabla del Nilo")
cat("ACF(1) del Nilo =", r(r1, 3), "\n")
cat("BIC (0,1,1) =", r(G$bic[G$p == 0 & G$d == 1 & G$q == 1], 2), "  AICc (1,1,1) =", r(G$aicc[G$p == 1 & G$d == 1 & G$q == 1], 2),
    "  AICc (1,2,2) =", r(G$aicc[G$p == 1 & G$d == 2 & G$q == 2], 2), " n efectivo (1,2,2) =", G$nobs[G$p == 1 & G$d == 2 & G$q == 2], "\n")
cat("LB(20) (1,1,1) =", r(G$lb[G$p == 1 & G$d == 1 & G$q == 1], 3), "\n")
cat("Shapiro (1,1,1) =", r(shapiro.test(residuals(arima(Nile, order = c(1, 1, 1), method = "ML")))$p.value, 3), "\n")

# --------------------------------------------------------------------------- M10 · TRM
sec("M10 · TRM")
prueba <- function(t) round(c(estad = unname(t$statistic), p = t$p.value), 3)
suppressWarnings(print(rbind(adf_nivel = prueba(adf.test(trm)), kpss_nivel = prueba(kpss.test(trm)),
                             adf_d1 = prueba(adf.test(diff(trm))), kpss_d1 = prueba(kpss.test(diff(trm))))))
cat("ndiffs/nsdiffs:", ndiffs(trm), nsdiffs(trm), "\n")
rr <- Acf(diff(trm), lag.max = 20, plot = FALSE)$acf[-1]; banda <- 1.96 / sqrt(length(diff(trm)))
cat("rho1 =", r(rr[1], 3), " rho8 =", r(rr[8], 3), " banda =", r(banda, 3), " barras fuera:", which(abs(rr) > banda), "\n")
rw <- arima(trm, order = c(0, 1, 0), method = "ML"); e <- residuals(rw)
cat("LB20 =", r(Box.test(e, lag = 20, type = "Ljung-Box")$p.value, 4), " LB12 =", r(Box.test(e, lag = 12, type = "Ljung-Box")$p.value, 4),
    " Shapiro =", r(shapiro.test(e)$p.value, 4), " LB12(e^2) =", r(Box.test(e^2, lag = 12, type = "Ljung-Box")$p.value, 4), "\n")
s <- sqrt(rw$sigma2); z <- qnorm(0.975); yT <- as.numeric(trm)[138]
cat("sigma =", r(s, 2), " semiancho h=1 =", r(z * s, 2), " yT =", yT, " sigma^2 =", r(rw$sigma2, 2), "\n")
h <- c(1, 3, 6, 12, 24); print(r(cbind(h, sigma_h = s * sqrt(h), semi = z * s * sqrt(h), inf = yT - z * s * sqrt(h), sup = yT + z * s * sqrt(h)), 2))
d1 <- diff(trm); d12 <- diff(trm, lag = 12)
cat("fuera 95% a 1 mes:", sum(abs(d1) > z * s), " por arriba:", sum(d1 > z * s), " de:", length(d1),
    "  -> % =", r(100 * sum(abs(d1) > z * s) / length(d1), 1), "\n")
cat("fuera 95% a 12 meses:", sum(abs(d12) > z * s * sqrt(12)), " de:", length(d12), " -> % =", r(100 * sum(abs(d12) > z * s * sqrt(12)) / length(d12), 1), "\n")
cat("cobertura del 80% a 1 mes:", r(mean(abs(d1) <= qnorm(0.90) * s), 4), "  (n dentro:", sum(abs(d1) <= qnorm(0.90) * s), ")\n")
cat("cuadrado medio / (h sigma^2), h = 3, 6, 12:", r(sapply(c(3, 6, 12), function(h) mean(diff(trm, lag = h)^2) / (h * s^2)), 3), "\n")
curt <- function(x) mean((x - mean(x))^4) / mean((x - mean(x))^2)^2; asim <- function(x) mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5
cat("curtosis d1, d12 =", r(c(curt(d1), curt(d12)), 2), " asimetria d1 =", r(asim(d1), 3), "\n")
cat("rho1 de diff(TRM) =", r(rr[1], 3), "\n")
ix <- order(d1, decreasing = TRUE)[1:3]
cat("mayores subidas mensuales (indice, valor, mes):\n"); print(data.frame(i = ix, delta = r(d1[ix], 1), mes = format(seq(as.Date("2015-02-01"), by = "month", length.out = 137)[ix], "%Y-%m")))
cat("ACF(1) TRM en niveles =", r(Acf(trm, plot = FALSE)$acf[2], 3), "\n")
rw_ar <- auto.arima(trm, stepwise = FALSE, approximation = FALSE); cat("auto.arima exhaustivo TRM:", as.character(rw_ar), "\n")

# --------------------------------------------------------------------------- M10 · puente
sec("M10 · puente al Capítulo 5 (log AirPassengers)")
lap <- log(AirPassengers); cat("n =", length(lap), "\n")
mej <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE); cat(as.character(mej), " nobs =", mej$nobs, "\n")
res <- residuals(mej); ra <- Acf(res, lag.max = 24, plot = FALSE)$acf[-1]
print(r(c(rho12 = ra[12], rho24 = ra[24], banda = 1.96 / sqrt(length(res))), 4))
lb <- Box.test(res, lag = 24, type = "Ljung-Box", fitdf = 5)
cat("Q =", r(unname(lb$statistic), 1), " p =", format(lb$p.value, digits = 3), "  p<1e-6:", lb$p.value < 1e-6, "\n")
cat("0.7245/0.1633 =", r(0.7245 / 0.1633, 2), " (\"mas de cuatro veces la banda\")\n")
am <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE, max.p = 8, max.q = 8, max.order = 16)
cat(as.character(am), " rho12 =", r(Acf(residuals(am), lag.max = 24, plot = FALSE)$acf[13], 3), "\n")
air <- Arima(lap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)); r2 <- residuals(air)
print(r(c(rho12 = Acf(r2, lag.max = 24, plot = FALSE)$acf[13], lb24_p = Box.test(r2, lag = 24, type = "Ljung-Box", fitdf = 2)$p.value), 4))
cat("nobs no estacional / airline:", mej$nobs, air$nobs, "\n")
cat("theta, Theta del airline:", r(coef(air), 4), "\n")
