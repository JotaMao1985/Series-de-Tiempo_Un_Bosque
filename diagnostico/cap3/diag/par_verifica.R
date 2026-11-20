## Par academico, cap. 3 (commit 58bdfc5): recalculo independiente de las cifras de la prosa
## que no salen directamente de un bloque de codigo del capitulo.
suppressPackageStartupMessages(library(forecast))
options(width = 110)
cat("R", as.character(getRversion()), "| forecast", as.character(packageVersion("forecast")), "\n\n")
manchas <- window(sunspot.year, start = 1770, end = 1869)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }

cat("== M2: periodo del triangulo con (1.40, -0.69) y con (1.4, -0.75)\n")
per <- function(p1, p2) 2*pi/acos(p1/(2*sqrt(-p2)))
print(round(c(p140_069 = per(1.40, -0.69), p14_075 = per(1.4, -0.75)), 4))

cat("\n== M2: AR(1) phi=+-1 en el circulo: phi=-1 NO es caminata aleatoria\n")
print(Mod(polyroot(c(1, 1))))

cat("\n== M3: techo de rho_1 en un MA(q) frente a cos(pi/(q+2))\n")
for (q in 1:3) {
  f <- function(th) { th0 <- c(1, th); -sum(th0[-1]*th0[-(q+1)]) / sum(th0^2) }
  best <- min(replicate(20, optim(runif(q, -1, 1), f)$value))
  cat(sprintf("q=%d  max numerico=%.4f  cos(pi/(q+2))=%.4f\n", q, -best, cos(pi/(q+2))))
}

cat("\n== M4: ACF por psi truncados en 600 terminos (la del JS) frente a ARMAacf, 8 procesos\n")
procs <- list(list(ar=0.8,ma=numeric(0)), list(ar=-0.7,ma=numeric(0)), list(ar=c(0.5,0.3),ma=numeric(0)),
              list(ar=c(1.4,-0.75),ma=numeric(0)), list(ar=numeric(0),ma=0.8), list(ar=numeric(0),ma=-0.8),
              list(ar=numeric(0),ma=c(0.6,0.4)), list(ar=0.7,ma=0.5))
err <- sapply(procs, function(p) {
  psi <- c(1, ARMAtoMA(p$ar, p$ma, 600))
  g <- sapply(0:16, function(k) sum(psi[1:(601-k)] * psi[(1+k):601]))
  max(abs(g[-1]/g[1] - ARMAacf(p$ar, p$ma, 16)[-1]))
})
print(signif(err, 3)); cat("max:", signif(max(err), 3), "\n")
cat("peor caso del laboratorio (phi1+phi2=0.95, |root| cerca de 1): ")
p <- list(ar=c(0.65,0.3), ma=c(0.5,0)); psi <- c(1, ARMAtoMA(p$ar, p$ma, 600))
g <- sapply(0:16, function(k) sum(psi[1:(601-k)] * psi[(1+k):601]))
cat(signif(max(abs(g[-1]/g[1] - ARMAacf(p$ar, p$ma, 16)[-1])), 3), "\n")

cat("\n== M4: parsimonia: |pi_j| del ARMA(1,1) 0.7/0.5\n")
print(round(abs(ARMAtoMA(-0.5, -0.7, 10)), 5))

cat("\n== M5: ARMA(2,1) phi=(0.5,0.3) theta=0.4: la recursion AR aplicada a k=1\n")
r <- ARMAacf(ar = c(0.5, 0.3), ma = 0.4, lag.max = 3)
cat("rho1 verdadero =", round(r[2], 4), "\n")
cat("recursion correcta en k=1: phi1*rho0 + phi2*rho_{-1} = 0.5 + 0.3*rho1 =", round(0.5 + 0.3*r[2], 4), "\n")
cat("la del capitulo: 0.5*rho0 + 0.3*rho0 =", 0.5 + 0.3, "(usa rho_{-1} = rho0 = 1, en contra de rho_{-k}=rho_k)\n")
cat("rho1 si fuera AR(2) puro (resolver la ecuacion): 0.5/(1-0.3) =", round(0.5/0.7, 4), "\n")

cat("\n== M7: CSS > 1 con T=40, phi=0.95: frecuencia en 1000 simulaciones (varias semillas)\n")
for (s in c(1, 2, 3, 2026)) {
  set.seed(s)
  est <- t(replicate(1000, {
    z <- arima.sim(list(ar = 0.95), n = 40)
    est1 <- function(m) tryCatch(suppressWarnings(coef(arima(z, order = c(1,0,0), include.mean = FALSE,
                                  method = m))[[1]]), error = function(e) NA_real_)
    c(css = est1("CSS"), ml = est1("ML"))
  }))
  cat(sprintf("seed %4d: CSS>1 = %.1f %%   ML>=1 = %.1f %%  (max ML %.4f)\n", s,
              100*mean(est[, "css"] > 1, na.rm = TRUE), 100*mean(est[, "ml"] >= 1, na.rm = TRUE), max(est[, "ml"], na.rm = TRUE)))
  cat("   fallos de optim (NA): CSS", sum(is.na(est[, "css"])), " ML", sum(is.na(est[, "ml"])), "\n")
}

cat("\n== M7: sigma2 de YW (ar) y su factor n/(n-(p+1))\n")
yw <- ar(manchas, order.max = 2, aic = FALSE, method = "yule-walker")
print(round(c(var.pred = yw$var.pred), 3))

cat("\n== M8: residuales de R: estandarizados en el arranque?\n")
ar2 <- arima(manchas, order = c(2, 0, 0), method = "ML")
e <- residuals(ar2); mu <- coef(ar2)[["intercept"]]; ph <- coef(ar2)[1:2]
g0 <- sum(c(1, ARMAtoMA(ph, numeric(0), 2000))^2)        # gamma0 / sigma2
cat("y1 - mu =", round(manchas[1] - mu, 4), "| (y1-mu)/sqrt(gamma0/s2) =", round((manchas[1]-mu)/sqrt(g0), 4),
    "| residuo R[1] =", round(e[1], 4), "\n")
cat("residuos R[1:4]:", round(e[1:4], 4), "\n")
acfr <- acf(e, lag.max = 20, plot = FALSE)$acf[-1]
o <- order(-abs(acfr))[1:3]
cat("mayores |acf resid| AR(2): rezagos", o, "valores", round(acfr[o], 4), "| banda", round(1.96/10, 4),
    "| fuera:", sum(abs(acfr) > 0.196), "\n")
cat("LB recortado (max(p,q) primeros fuera), R:\n")
for (pq in list(c(2,0), c(2,1), c(2,2))) {
  f <- arima(manchas, order = c(pq[1], 0, pq[2]), method = "ML")
  rr <- residuals(f)[-(1:max(pq))]
  cat(sprintf("  ARMA(%d,%d): %.4f\n", pq[1], pq[2], Box.test(rr, 12, "Ljung-Box", fitdf = sum(pq))$p.value))
}
a21 <- arima(manchas, order = c(2, 0, 1), method = "ML")
cat("ARMA(2,1) cruda: coef", round(coef(a21), 4), " t(theta) =", round(coef(a21)[3]/sqrt(a21$var.coef[3,3]), 3), "\n")
cat("  raiz MA:", round(polyroot(c(1, coef(a21)[3])), 4), "  raices AR:", round(polyroot(c(1, -coef(a21)[1:2])), 4),
    " mod", round(Mod(polyroot(c(1, -coef(a21)[1:2])))[1], 4), "\n")

cat("\n== M9: ceros de sunspot.year completa\n")
print(time(sunspot.year)[sunspot.year == 0])

cat("\n== M9: elasticidades (misma receta que genera_cap3.R)\n")
elas <- function(x, g) { niv <- tapply(as.numeric(x), g, mean); amp <- tapply(as.numeric(x), g, sd)
  ok <- niv > 0 & amp > 0; aj <- lm(log(amp[ok]) ~ log(niv[ok]))
  c(b = coef(aj)[[2]], confint(aj)[2, ], r2 = summary(aj)$r.squared, k = sum(ok)) }
print(round(rbind(b10 = elas(manchas, rep(1:10, each = 10)),
                  b11 = elas(manchas, cut(1:100, breaks = seq(0, 100, by = 11.1), labels = FALSE)),
                  b5  = elas(manchas, rep(1:20, each = 5))), 4))

cat("\n== M9: rejilla de 11 modelos sobre sqrt(manchas)\n")
rej <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3), c(1,1), c(2,1), c(1,2), c(2,2))
res <- do.call(rbind, lapply(rej, function(pq) { f <- arima(sqrt(manchas), order = c(pq[1],0,pq[2]), method = "ML")
  data.frame(m = sprintf("ARMA(%d,%d)", pq[1], pq[2]), AICc = round(aicc(f, 100), 2), BIC = round(BIC(f), 2),
             LB12 = round(Box.test(residuals(f), 12, "Ljung-Box", fitdf = sum(pq))$p.value, 4)) }))
print(res[order(res$AICc), ], row.names = FALSE)

ar2s <- arima(sqrt(manchas), order = c(2, 0, 0), method = "ML")
cat("\nAR(2) sqrt: coef", round(coef(ar2s), 4), " se", round(sqrt(diag(ar2s$var.coef)), 4),
    " t", round(coef(ar2s)[1:2]/sqrt(diag(ar2s$var.coef))[1:2], 2), " sigma2", round(ar2s$sigma2, 4), "\n")
cat("LB recortado (2 primeros fuera), R:", round(Box.test(residuals(ar2s)[-(1:2)], 12, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")

cat("\n== M9: Guerrero\n")
lam <- BoxCox.lambda(manchas + 1, method = "guerrero"); cat("lambda =", round(lam, 4), "\n")
for (nm in c("original", "desplazada")) {
  x <- if (nm == "original") manchas^lam else (manchas + 1)^lam    # sin el (.-1)/lambda: no cambia phi
  x2 <- if (nm == "original") BoxCox(manchas, lam) else BoxCox(manchas + 1, lam)
  f <- arima(x2, order = c(2, 0, 0), method = "ML"); rt <- polyroot(c(1, -coef(f)[1:2]))
  cat(sprintf("  %s: phi=(%.4f, %.4f) periodo=%.4f LB12 p=%.4f\n", nm, coef(f)[1], coef(f)[2], 2*pi/Arg(rt[1]),
              Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value))
}

cat("\n== M9: polinomio con el signo cambiado 1 - 1.4027B - 0.6853B^2\n")
print(round(polyroot(c(1, -1.4027, -0.6853)), 4))

cat("\n== M9: psi frente al envolvente R^j y R^j/sin(w)\n")
ph <- coef(ar2s)[1:2]; R <- sqrt(-ph[[2]]); w <- Arg(polyroot(c(1, -ph))[1])
psi <- c(1, ARMAtoMA(ph, numeric(0), 24)); j <- 0:24
cat("sin(w) =", round(sin(w), 4), " 1/sin(w) =", round(1/sin(w), 4), "\n")
cat("j con |psi_j| > R^j:", j[abs(psi) > R^j + 1e-12], "\n")
cat("j con |psi_j| > R^j/sin(w):", j[abs(psi) > R^j/sin(w) + 1e-12], "\n")
cat("vida media del envolvente:", round(log(0.5)/log(R), 3), " cruces por cero j=k*pi/w-1:", round(c(pi, 2*pi)/w - 1, 3), "\n")

cat("\n== M9: bandas en escala de la raiz y su vuelta al cuadrado (pronostico desde 1869)\n")
fc <- forecast(ar2s, h = 12, level = 95)
tab <- cbind(h = 1:12, media = round(as.numeric(fc$mean), 3), inf = round(as.numeric(fc$lower), 3),
             sup = round(as.numeric(fc$upper), 3))
print(tab)
cat("limites inferiores negativos en la escala de la raiz:", sum(fc$lower < 0), "de 12\n")
cat("semiancho h=1..12:", round(qnorm(.975)*sqrt(ar2s$sigma2*cumsum(psi[1:12]^2)), 2), "\n")
cat("techo:", round(qnorm(.975)*sqrt(ar2s$sigma2*sum(c(1,ARMAtoMA(ph, numeric(0), 2000))^2)), 3),
    " fraccion a h=6:", round(qnorm(.975)*sqrt(ar2s$sigma2*sum(psi[1:6]^2)) /
                                 (qnorm(.975)*sqrt(ar2s$sigma2*sum(c(1,ARMAtoMA(ph, numeric(0), 2000))^2))), 4), "\n")

cat("\n== M9: asimetria y Shapiro de residuales\n")
sk <- function(r) mean((r-mean(r))^3)/mean((r-mean(r))^2)^1.5
cat("cruda:", round(sk(residuals(ar2)), 4), round(shapiro.test(residuals(ar2))$p.value, 4),
    " | sqrt:", round(sk(residuals(ar2s)), 4), round(shapiro.test(residuals(ar2s))$p.value, 4), "\n")

cat("\n== Ejercicio 3: p-valor exacto 1900-1988 y 1870-1988\n")
for (v in list(c(1870,1988), c(1900,1988))) {
  x <- sqrt(window(sunspot.year, v[1], v[2])); f <- arima(x, order = c(2,0,0), method = "ML")
  cat(v, ": p =", format(Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value, digits = 6), " n =", length(x), "\n")
}
cat("misma n que la ventana de Yule pero otro siglo: 1889-1988\n")
x <- sqrt(window(sunspot.year, 1889, 1988)); f <- arima(x, order = c(2,0,0), method = "ML")
cat("  n =", length(x), " p =", round(Box.test(residuals(f), 12, "Ljung-Box", fitdf = 2)$p.value, 4), "\n")

cat("\n== M10: ARMA(2,2) (1.1,-0.28 | 0.1,-0.2) frente a ARMA(1,1) (0.7 | 0.5)\n")
cat("max diff ACF:", max(abs(ARMAacf(c(1.1,-0.28), c(0.1,-0.2), 30) - ARMAacf(0.7, 0.5, 30))), "\n")

cat("\n== M9 caso 2: TRM desde el CSV del repo\n")
trm <- read.csv("../../../precalculo/trm_mensual_2015-01_2026-06.csv")
print(head(trm, 2))
