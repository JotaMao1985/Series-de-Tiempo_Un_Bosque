# lectorD_comprobaciones.R · comprobaciones de la R4 (capítulo 4, lector D: Módulos 8 y 9).
# Solo lee datos de R y la copia fija de la TRM; no escribe nada salvo la salida estándar.
# Uso: Rscript lectorD_comprobaciones.R  (R 4.6.0, forecast 9.0.2, tseries 0.10.62, urca 1.3.4)
suppressMessages({library(forecast); library(tseries); library(urca)})
raiz <- "."   # se ejecuta desde la raíz del repo
cat("== versiones\n"); cat(R.version.string, "| forecast", as.character(packageVersion("forecast")),
                         "| tseries", as.character(packageVersion("tseries")),
                         "| urca", as.character(packageVersion("urca")), "\n")

cat("\n== M8 · la firma de la sobrediferenciación (c4-m8-03, -04, -05, -06)\n")
for (d in 1:3) {
  x <- diff(Nile, differences = d)
  f <- arima(x, order = c(0, 0, 1), include.mean = FALSE, method = "ML")
  th <- coef(f)[["ma1"]]
  rho1 <- acf(x, plot = FALSE)$acf[2]
  cat(sprintf("d=%d var=%.2f rho1=%.3f theta=%.6f |raiz MA|=%.6f sigma2_MA1=%.2f\n",
              d, var(x), rho1, th, Mod(polyroot(c(1, th))), f$sigma2))
}
cat("var(diff(Nile))     =", round(var(diff(Nile)), 2), "\n")
cat("var(diff(Nile,2))   =", round(var(diff(Nile, differences = 2)), 2), "\n")
# El MA(1) con theta = -1 sobre una serie w_t - w_{t-1}: sigma2 ~ media de w^2 (no la varianza centrada)
w <- diff(Nile); cat("mean(w^2) con w = diff(Nile) =", round(mean(w^2), 2), " var(w) =", round(var(w), 2), "\n")
cat("rejilla d=2 (q en 1:2, p en 0:2), min|raiz MA| con 6 decimales:\n")
for (q in 1:2) for (p in 0:2) {
  f <- suppressWarnings(arima(Nile, order = c(p, 2, q), method = "ML"))
  ma <- f$coef[grepl("^ma", names(f$coef))]
  cat(sprintf("  ARIMA(%d,2,%d) min|raiz MA| = %.6f\n", p, q, min(Mod(polyroot(c(1, ma))))))
}

cat("\n== M8 · la ayuda de Nile dice 'near 1898'; medias y escalón (c4-m8-12, -14, -15)\n")
cat("media antes de 1899 =", round(mean(Nile[time(Nile) < 1899]), 2), " desde 1899 =", round(mean(Nile[time(Nile) >= 1899]), 2), "\n")
esc <- as.numeric(time(Nile) >= 1899)
fe <- arima(Nile, order = c(0, 0, 0), xreg = esc, method = "ML")
cat("beta =", round(coef(fe)[["esc"]], 2), " e.e. =", round(sqrt(diag(fe$var.coef))[["esc"]], 2),
    " t =", round(coef(fe)[["esc"]] / sqrt(diag(fe$var.coef))[["esc"]], 2), "\n")
fe2 <- Arima(Nile, order = c(0, 0, 0), xreg = esc)
cat("AICc escalon (forecast::Arima, n =", length(Nile), ") =", round(fe2$aicc, 2),
    " Ljung-Box(20) p =", round(Box.test(residuals(fe2), lag = 20, type = "Ljung-Box")$p.value, 3), "\n")
mejor <- NULL
for (p in 0:2) for (q in 0:2) {
  a <- tryCatch(Arima(Nile, order = c(p, 0, q), method = "ML"), error = function(e) NULL)
  if (!is.null(a)) cat(sprintf("  d=0 ARMA(%d,%d) AICc = %.2f\n", p, q, a$aicc))
}
cat("ARIMA(1,1,1) AICc (d = 1, NO comparable con los d = 0):", round(Arima(Nile, order = c(1, 1, 1))$aicc, 2), "\n")

cat("\n== M8 · log(lynx): varianza, r1 y pruebas (c4-m8-09, -10, -11, -22)\n")
ll <- log(lynx)
cat("var(log lynx) =", round(var(ll), 3), " var(diff) =", round(var(diff(ll)), 3),
    " reduccion =", round(100 * (1 - var(diff(ll)) / var(ll)), 1), "%\n")
cat("r1 de diff(log lynx) =", round(acf(diff(ll), plot = FALSE)$acf[2], 3), "\n")
cat("ndiffs por prueba:", sapply(c("kpss", "adf", "pp"), function(t) ndiffs(ll, test = t)), "(kpss, adf, pp)\n")
cat("adf.test p =", round(adf.test(ll)$p.value, 4), " kpss.test p =", round(kpss.test(ll)$p.value, 4),
    " PP.test (stats) p =", round(PP.test(ll)$p.value, 4), " pp.test (tseries) p =", round(pp.test(ll)$p.value, 4), "\n")
f211 <- arima(ll, order = c(2, 1, 1), method = "ML")
cat("ARIMA(2,1,1) en log(lynx): |raiz MA| =", round(Mod(polyroot(c(1, coef(f211)[["ma1"]]))), 4), "\n")
cat("cociente var(diff)/var =", round(var(diff(ll)) / var(ll), 3), " 2(1 - r1) =", round(2 * (1 - acf(ll, plot = FALSE)$acf[2]), 3), "\n")
cat("Nile: cociente var(diff)/var =", round(var(diff(Nile)) / var(Nile), 3),
    " 2(1 - r1) =", round(2 * (1 - acf(Nile, plot = FALSE)$acf[2]), 3), " r1 =", round(acf(Nile, plot = FALSE)$acf[2], 3), "\n")

cat("\n== M8 · diagnóstico del ARIMA(1,1,1) del Nilo (c4-m8-01, -02)\n")
f111 <- arima(Nile, order = c(1, 1, 1), method = "ML")
e <- residuals(f111)
cat("Ljung-Box(20, fitdf=2) p =", round(Box.test(e, lag = 20, type = "Ljung-Box", fitdf = 2)$p.value, 3),
    " | sin fitdf p =", round(Box.test(e, lag = 20, type = "Ljung-Box")$p.value, 3),
    " | Shapiro p =", round(shapiro.test(e)$p.value, 3), " | gl =", Box.test(e, lag = 20, type = "Ljung-Box", fitdf = 2)$parameter, "\n")

cat("\n== M9 · forma del pronóstico (c4-m9-01 a -08)\n")
formas <- list("d=0 con media" = Arima(Nile, order = c(1, 0, 1)),
               "d=1 sin constante" = Arima(Nile, order = c(1, 1, 1)),
               "d=1 con deriva" = Arima(Nile, order = c(1, 1, 1), include.drift = TRUE),
               "d=2" = Arima(Nile, order = c(1, 2, 1)))
for (nm in names(formas)) {
  m <- as.numeric(forecast(formas[[nm]], h = 30)$mean)
  fc <- forecast(formas[[nm]], h = 30, level = 95)
  cat(sprintf("%-18s 1a dif h=30: %7.3f  2a dif: %9.6f  ancho95 h=1: %.0f h=30: %.0f  media h=30: %.2f\n", nm,
              m[30] - m[29], m[30] - 2 * m[29] + m[28],
              fc$upper[1] - fc$lower[1], fc$upper[30] - fc$lower[30], m[30]))
}
cat("media muestral de Nile =", round(mean(Nile), 2), " | intercept CSS-ML (Arima) =", round(coef(formas[[1]])[["intercept"]], 2),
    " | intercept ML (arima) =", round(coef(arima(Nile, order = c(1, 0, 1), method = "ML"))[["intercept"]], 2), "\n")
w <- NULL
r <- withCallingHandlers(Arima(Nile, order = c(1, 2, 1), include.drift = TRUE),
                         warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") })
cat("Arima(d=2, include.drift=TRUE) avisa:", w, "| ajusta drift:", "drift" %in% names(coef(r)), "\n")
f1 <- formas[["d=1 sin constante"]]
ph <- coef(f1)[["ar1"]]; th1 <- coef(f1)[["ma1"]]
yT <- as.numeric(tail(Nile, 1)); dyT <- yT - as.numeric(Nile)[99]; eT <- as.numeric(tail(residuals(f1), 1))
cat("ultimo", yT, " h1", round(forecast(f1, h = 1)$mean[1], 2), " h30", round(forecast(f1, h = 30)$mean[30], 2),
    " limite", round(yT + (ph * dyT + th1 * eT) / (1 - ph), 2), "\n")
d2 <- Arima(Nile, order = c(1, 2, 1))
cat("d=2: phi =", round(coef(d2)[["ar1"]], 3), " theta =", round(coef(d2)[["ma1"]], 4), " (segunda dif. pronostico: potencias de phi)\n")
m2 <- as.numeric(forecast(d2, h = 30)$mean)
dd <- diff(c(as.numeric(tail(Nile, 2)), m2), differences = 2)
cat("2a dif del pronostico d=2, h=1..6:", round(dd[1:6], 4), "; cociente consecutivo:", round(dd[3:6] / dd[2:5], 3), "\n")

cat("\n== M9 · pesos psi, sigma_h, invertible frente a no invertible (c4-m9-09 a -22)\n")
f <- Arima(Nile, order = c(1, 1, 1)); phi <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2)
psi <- c(1, ARMAtoMA(ar = c(1 + phi, -phi), ma = th, lag.max = 30)); sigma_h <- s * sqrt(cumsum(psi^2))[1:30]
fc <- forecast(f, h = 30, level = 95)
cat("max|semiancho - 1.96*sigma_h| =", format(max(abs((fc$upper - fc$lower) / 2 - qnorm(0.975) * sigma_h)), digits = 4), "\n")
cat("psi_inf =", round((1 + th) / (1 - phi), 3), " psi_30 =", round(psi[31], 3), " sigma =", round(s, 3),
    " sigma_30 =", round(sigma_h[30], 1), " camino aleatorio sigma*sqrt(30) =", round(s * sqrt(30), 1), "\n")
f2 <- Arima(Nile, order = c(1, 2, 1)); ph2 <- coef(f2)[["ar1"]]
psi2 <- c(1, ARMAtoMA(ar = c(2 + ph2, -(1 + 2 * ph2), ph2), ma = coef(f2)[["ma1"]], lag.max = 29))
fc2 <- forecast(f2, h = 30, level = 95)
cat("d=2: theta =", round(coef(f2)[["ma1"]], 4), " psi_29 =", round(psi2[30], 3), " 1/(1-phi) =", round(1 / (1 - ph2), 3),
    " ancho_psi =", round(2 * qnorm(0.975) * sqrt(f2$sigma2 * sum(psi2^2)), 1), " ancho_forecast =", round(fc2$upper[30] - fc2$lower[30], 1), "\n")
# mismo ARIMA(1,2,1) con theta FIJO en un valor invertible: la fórmula de psi y forecast() ¿coinciden?
for (thf in c(-0.9, -0.99, -1)) {
  g <- suppressWarnings(Arima(Nile, order = c(1, 2, 1), fixed = c(NA, thf), transform.pars = FALSE))
  phg <- coef(g)[["ar1"]]
  psig <- c(1, ARMAtoMA(ar = c(2 + phg, -(1 + 2 * phg), phg), ma = thf, lag.max = 29))
  fcg <- forecast(g, h = 30, level = 95)
  cat(sprintf("  theta fijo %.2f: ancho_psi %.1f vs ancho_forecast %.1f (razon %.4f)\n", thf,
              2 * qnorm(0.975) * sqrt(g$sigma2 * sum(psig^2)), fcg$upper[30] - fcg$lower[30],
              (fcg$upper[30] - fcg$lower[30]) / (2 * qnorm(0.975) * sqrt(g$sigma2 * sum(psig^2)))))
}
pw <- tryCatch({ w <- NULL; withCallingHandlers(predict(f2, n.ahead = 3), warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") }); w },
               error = function(e) conditionMessage(e))
cat("predict(ARIMA(1,2,1) del Nilo) avisa de no invertibilidad:", if (is.null(pw)) "no avisa" else pw, "\n")
cat("forecast(f2, h=3) avisa:", tryCatch({ w <- NULL; withCallingHandlers(forecast(f2, h = 3), warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") }); if (is.null(w)) "no avisa" else w }, error = function(e) conditionMessage(e)), "\n")
cat("forecast.Arima usa predict.Arima (cuerpo):", grepl("predict", paste(deparse(forecast:::forecast.Arima), collapse = " ")), "\n")

cat("\n== M9 · sigma2 de arima() frente a Arima() (c4-m9-31)\n")
fm <- arima(Nile, order = c(1, 1, 1), method = "ML"); fa <- Arima(Nile, order = c(1, 1, 1)); faM <- Arima(Nile, order = c(1, 1, 1), method = "ML")
scr <- sum(residuals(fm)^2)
cat("sigma2 arima ML =", round(fm$sigma2, 2), "| Arima defecto =", round(fa$sigma2, 2), "| Arima ML =", round(faM$sigma2, 2),
    "| razon =", round(fa$sigma2 / fm$sigma2, 5), " 99/97 =", round(99 / 97, 5), "| SCR/99 =", round(scr / 99, 2), " SCR/97 =", round(scr / 97, 2), "\n")

cat("\n== M9 · BJsales, psi_inf (c4-m9-15, -22)\n")
bj <- BJsales
fb <- Arima(bj, order = c(1, 1, 1)); pb <- coef(fb)[["ar1"]]; tb <- coef(fb)[["ma1"]]
cat("BJsales ARIMA(1,1,1): phi =", round(pb, 3), " theta =", round(tb, 3), " psi_inf =", round((1 + tb) / (1 - pb), 2), "\n")
psib <- c(1, ARMAtoMA(ar = c(1 + pb, -pb), ma = tb, lag.max = 11)); cat("sigma_12 / (sigma*sqrt(12)) =", round(sqrt(sum(psib^2)) / sqrt(12), 2), "\n")

cat("\n== M9 · TRM: Shapiro y cobertura del 80 % a un mes (c4-m9-25, -26)\n")
trm <- read.csv(file.path(raiz, "precalculo/trm_mensual_2015-01_2026-06.csv"))
trm <- ts(trm$trm, start = c(2015, 1), frequency = 12)
rw <- arima(trm, order = c(0, 1, 0), method = "ML"); e <- residuals(rw); s <- sqrt(rw$sigma2); d1 <- diff(trm)
cat("n =", length(trm), " Shapiro p =", round(shapiro.test(e)$p.value, 4), " cubre 80 % =", round(mean(abs(d1) <= qnorm(0.90) * s), 4),
    " (", sum(abs(d1) <= qnorm(0.90) * s), "de", length(d1), ")", " cubre 95 % =", round(mean(abs(d1) <= qnorm(0.975) * s), 4), "\n")
cat("curtosis =", round(mean((d1 - mean(d1))^4) / mean((d1 - mean(d1))^2)^2, 1),
    " asimetria =", round(mean((d1 - mean(d1))^3) / mean((d1 - mean(d1))^2)^1.5, 2), "\n")
cat("z_0.975 =", round(qnorm(0.975), 3), " z_0.90 =", round(qnorm(0.90), 4), "\n")

cat("\n== M9 · forma cerrada de psi_j y trayectoria del ARIMA(1,1,1) sin constante (c4-m9-13, -67)\n")
f <- Arima(Nile, order = c(1, 1, 1)); phi <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]
psi <- c(1, ARMAtoMA(ar = c(1 + phi, -phi), ma = th, lag.max = 30))
j <- 1:30; cerrada <- ((1 + th) - (phi + th) * phi^j) / (1 - phi)
cat("max|psi_j (ARMAtoMA) - forma cerrada| j=1..30:", format(max(abs(psi[2:31] - cerrada)), digits = 4), " | psi_0 =", psi[1], "\n")
yT <- as.numeric(tail(Nile, 1)); dyT <- yT - as.numeric(Nile)[99]; eT <- as.numeric(tail(residuals(f), 1))
m <- as.numeric(forecast(f, h = 30)$mean); dm <- diff(c(yT, m))
formula_dif <- phi^(0:29) * (phi * dyT + th * eT)
cat("max|dif. pronosticada - phi^(h-1)(phi*dy_T + theta*e_T)| h=1..30:", format(max(abs(dm - formula_dif)), digits = 4), "\n")
cat("h=1:", round(m[1], 2), " h=30:", round(m[30], 2), " limite:", round(yT + (phi * dyT + th * eT) / (1 - phi), 2), "\n")
