# Verificador A · R4 cap. 4 · repite las entradas `propia` de M1–M6 y las
# cifras de R que aparecen dentro de entradas citables. Guion propio: no
# llama a precalculo/genera_cap4.R ni a los guiones de los lectores; donde una
# cifra depende de la secuencia aleatoria se sigue la receta que describe la
# prosa (semilla 2026, orden de los sorteos) para poder compararla.
suppressPackageStartupMessages({library(forecast); library(tseries); library(urca)})
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")),
    "| urca", as.character(packageVersion("urca")), "\n")
r4 <- function(x) round(x, 4)
sec <- function(s) cat("\n==================== ", s, " ====================\n", sep = "")
nilo <- Nile; n <- length(nilo)

sec("M1 · ajuste ARIMA(1,1,1) del Nilo y raíces (c4-m1-07, -24, -66)")
f111 <- arima(nilo, order = c(1, 1, 1), method = "ML")
print(r4(rbind(coef = coef(f111), ee = sqrt(diag(f111$var.coef)))))
phi <- round(coef(f111)[["ar1"]], 4); theta <- round(coef(f111)[["ma1"]], 4)
cat("raíz MA:", round(Mod(polyroot(c(1, theta))), 4), "\n")
ae <- c(1 + phi, -phi); cat("AR expandido:", r4(ae), " suma:", sum(ae),
  " |raíces|:", r4(Mod(polyroot(c(1, -ae)))), "\n")

sec("M1 · c4-m1-23: razón de varianzas al integrar (set.seed(2026), n = 200)")
set.seed(2026); w <- arima.sim(list(ar = phi, ma = theta), n = 200); y <- cumsum(w)
cat("var_w", round(var(w), 3), "var_y", round(var(y), 3), "razón", round(var(y)/var(w), 3), "\n")
set.seed(2026); w0 <- arima.sim(list(ar = phi), n = 200)
cat("sin MA: razón", round(var(cumsum(w0))/var(w0), 1), "\n")

sec("M1 · c4-m1-66: varianza de largo plazo / gamma0, con y sin MA")
lrv <- function(ph, th) (1 + th)^2 / (1 - ph)^2
g0  <- function(ph, th) (1 + 2*ph*th + th^2) / (1 - ph^2)
cat("ARMA(1,1) Nilo: LRV/g0 =", r4(lrv(phi, theta)/g0(phi, theta)),
    "| AR(1) sin MA: LRV/g0 =", r4(lrv(phi, 0)/g0(phi, 0)), "\n")
cat("(1+theta)^2 =", r4((1 + theta)^2), "\n")

sec("M1 · c4-m1-12: ses() frente a ARIMA(0,1,1) sobre el Nilo")
f011 <- arima(nilo, order = c(0, 1, 1), method = "ML")
s <- ses(nilo, h = 1)
cat("ses alpha =", r4(s$model$par[["alpha"]]), "| 1 + theta(ARIMA 0,1,1) =", r4(1 + coef(f011)[["ma1"]]), "\n")
fv <- as.numeric(fitted(s)); yy <- as.numeric(nilo); a <- s$model$par[["alpha"]]
cat("max |yhat_{t+1} - (a y_t + (1-a) yhat_t)| =",
    signif(max(abs(fv[-1] - (a*yy[-n] + (1-a)*fv[-n]))), 3), "\n")

sec("M1 · c4-m1-16: el nivel alrededor de 1899")
print(window(nilo, 1895, 1903))
cat("media 1871-1898:", round(mean(window(nilo, end = 1898)), 2),
    "| media 1899-1970:", round(mean(window(nilo, start = 1899)), 2), "\n")

sec("M1 · c4-m1-27 / -28: convenio de signo de R y rho1 del MA(1)")
cat("ARMAacf(ma = +0.5)[2] =", ARMAacf(ma = 0.5)[2], "| ARMAacf(ma = -0.5)[2] =", ARMAacf(ma = -0.5)[2], "\n")
set.seed(1); xs <- arima.sim(list(ma = 0.6), n = 2000)
cat("arima(order = c(0,0,1)) sobre MA(1) con theta = +0.6: ma1 =", r4(coef(arima(xs, c(0,0,1)))[["ma1"]]), "\n")

sec("M2 · c4-m2-62: un escalón sin modelar sube d o infla sigma^2")
esc <- as.numeric(time(nilo) >= 1899)
cat("ndiffs(Nile) =", ndiffs(nilo), "\n")
cat("sigma2 ARMA(1,1) con media, sin escalón:", round(arima(nilo, c(1,0,1), method = "ML")$sigma2, 1),
    "| con escalón como xreg:", round(arima(nilo, c(1,0,1), xreg = esc, method = "ML")$sigma2, 1), "\n")
cat("sigma2 ruido blanco con media:", round(arima(nilo, c(0,0,0), method = "ML")$sigma2, 1),
    "| media + escalón:", round(arima(nilo, c(0,0,0), xreg = esc, method = "ML")$sigma2, 1), "\n")

sec("M3 · pruebas sobre el Nilo (tabla de evidencias, c4-m3-09, -10, -11, -12, -13)")
ad <- adf.test(nilo); cat("adf.test: stat", r4(ad$statistic), "p", r4(ad$p.value), "k", ad$parameter, "\n")
cat("trunc((n-1)^(1/3)) =", trunc((n - 1)^(1/3)), "\n")
kp <- kpss.test(nilo); cat("kpss.test: stat", r4(kp$statistic), "p", kp$p.value, "trunc", kp$parameter, "\n")
pp <- PP.test(nilo); cat("PP.test:", names(pp$statistic), r4(pp$statistic), "p", r4(pp$p.value), "\n")
cat("ndiffs kpss/adf/pp:", sapply(c("kpss", "adf", "pp"), function(t) ndiffs(nilo, test = t)), "\n")
cat("formals(ndiffs)$test:", deparse(formals(ndiffs)$test), "\n")
cat("formals(auto.arima)$test:", deparse(formals(auto.arima)$test), "| ic:", deparse(formals(auto.arima)$ic), "\n")
cuerpo <- deparse(body(ndiffs))
cat("ndiffs, líneas con ur.df / ur.kpss / use.lag:\n"); cat(grep("ur\\.df|ur\\.kpss|use\\.lag|ur\\.pp", cuerpo, value = TRUE), sep = "\n")
cat("formals(ur.df)$lags =", formals(ur.df)$lags, "\n")
u <- ur.df(nilo, type = "drift", lags = 1)
cat("ur.df(drift, lags = 1): tau2 =", r4(u@teststat[1, "tau2"]), "| cval tau2 5pct =", u@cval["tau2", "5pct"], "\n")
cat("ADF de d = 1 y 2, rho1:", round(sapply(1:2, function(d) acf(diff(nilo, differences = d), plot = FALSE)$acf[2]), 3), "\n")
cat("raíz MA del ARIMA(0,1,1):", r4(Mod(polyroot(c(1, coef(f011)[["ma1"]])))), "\n")

sec("M3 · c4-m3-60: varianza por orden de diferencia y 2(1 - r1)")
for (d in 0:3) { x <- if (d == 0) nilo else diff(nilo, differences = d); cat("d =", d, "var =", round(var(x), 2), "\n") }
r1 <- acf(nilo, plot = FALSE)$acf[2]
cat("r1 =", r4(r1), "| 2(1-r1) =", round(2*(1 - r1), 3), "| cociente =", round(var(diff(nilo))/var(nilo), 3),
    "| baja d0->d1 =", round(100*(1 - var(diff(nilo))/var(nilo)), 2), "% | d2/d1 =", round(var(diff(nilo, differences = 2))/var(diff(nilo)), 2), "\n")

sec("M3 · c4-m3-15: ARIMA(1,1,1) con raíz unitaria verdadera, 1000 réplicas")
set.seed(2026); rpp <- 0; radf <- 0
for (i in 1:1000) {
  x <- 900 + cumsum(arima.sim(list(ar = phi, ma = theta), n = n))
  if (suppressWarnings(PP.test(x)$p.value) < 0.05) rpp <- rpp + 1
  if (suppressWarnings(adf.test(x, k = 4)$p.value) < 0.05) radf <- radf + 1
}
cat("PP.test rechaza", 100*rpp/1000, "% | adf.test(k = 4) rechaza", 100*radf/1000, "%\n")

sec("M3 · modelo de dos medias (beta, sigma de los residuales)")
fe <- arima(nilo, order = c(0, 0, 0), xreg = esc, method = "ML")
beta <- coef(fe)[["esc"]]; sig <- sd(residuals(fe)); pos <- which(time(nilo) == 1899)
cat("beta =", round(beta, 2), "| sd resid =", round(sig, 2), "| beta/sd =", round(abs(beta)/sig, 3), "| posición =", pos, "\n")
cat("100/sd =", round(100/sig, 3), "\n")

sec("M3 · c4-m3-18 y -66: Monte Carlo de 1000 réplicas (sin escalón, luego con él)")
set.seed(2026); e01 <- as.numeric(seq_len(n) >= pos)
cuenta <- function(dl) {
  k <- 0; adf_nr <- 0; ndk <- 0; nda <- 0
  for (i in 1:1000) {
    x <- 1000 + dl * e01 + rnorm(n, 0, sig)
    if (suppressWarnings(kpss.test(x)$p.value) <= 0.05) k <- k + 1
    if (suppressWarnings(adf.test(x)$p.value) > 0.05) adf_nr <- adf_nr + 1
    ndk <- ndk + (suppressWarnings(ndiffs(x, test = "kpss")) >= 1)
    nda <- nda + (suppressWarnings(ndiffs(x, test = "adf")) >= 1)
  }
  c(kpss_rechaza = k, adf_test_no_rechaza = adf_nr, ndiffs_kpss = ndk, ndiffs_adf = nda) / 1000
}
cat("sin escalón:\n"); print(cuenta(0)); cat("con escalón beta:\n"); print(cuenta(beta))

sec("M3 · c4-m3-67 y -34: malla de 400 réplicas (deltas 0..300 en orden)")
set.seed(2026)
for (dl in c(0, 25, 50, 75, 100, 150, 200, 250, 300)) {
  r <- 0; r12 <- 0; est <- numeric(400)
  for (i in 1:400) {
    x <- 1000 + dl * e01 + rnorm(n, 0, sig)
    kk <- suppressWarnings(kpss.test(x)); est[i] <- kk$statistic
    if (kk$p.value <= 0.05) r <- r + 1
    if (suppressWarnings(kpss.test(x, lshort = FALSE)$p.value) <= 0.05) r12 <- r12 + 1
  }
  cat(sprintf("delta %3d (%.3f sd): kpss_rechaza %.4f | l12 %.4f | kpss medio %.2f\n", dl, dl/sig, r/400, r12/400, mean(est)))
}

sec("M3 · c4-m3-19, -64, -31: fórmula del KPSS y truncamientos")
kpss_a_mano <- function(x, l) {
  e <- x - mean(x); S <- cumsum(e); m <- length(x)
  g <- sapply(0:l, function(j) sum(e[(j+1):m] * e[1:(m-j)]) / m)
  s2 <- g[1] + 2 * sum((1 - (1:l)/(l + 1)) * g[-1])
  c(stat = sum(S^2) / (m^2 * s2), s2 = s2)
}
cat("a mano l = 4:", kpss_a_mano(nilo, 4), "| tseries:", kpss.test(nilo)$statistic, "\n")
cat("a mano l = 12:", kpss_a_mano(nilo, 12), "| tseries lshort = FALSE:", kpss.test(nilo, lshort = FALSE)$statistic, "\n")
cat("a mano l = 2:", kpss_a_mano(nilo, 2), "| ur.kpss(use.lag = 2):", ur.kpss(nilo, use.lag = 2)@teststat,
    "| trunc(3 sqrt(n)/13) =", trunc(3*sqrt(n)/13), "\n")
cat("ACF del Nilo, rezagos 1-12:", round(acf(nilo, lag.max = 12, plot = FALSE)$acf[-1], 3), "\n")
cat("tabla de kpss.test (cuerpo):", grep("table <-|tablep <-", deparse(body(kpss.test)), value = TRUE), sep = "\n")

sec("M3 · c4-m3-71: puente browniano (ruido blanco, n = 400, 4000 réplicas)")
set.seed(11); m <- 400; rr <- c(.1, .25, .5, .75)
Sm <- replicate(4000, { e <- rnorm(m); e <- e - mean(e); S <- cumsum(e) / sqrt(m); c(S[rr*m], S[m]) })
cat("Var(S_t/sqrt n) en r = 0.10, 0.25, 0.50, 0.75:", round(apply(Sm[1:4, ], 1, var), 4),
    "| r(1-r):", rr*(1 - rr), "| max|S_n| =", signif(max(abs(Sm[5, ])), 2), "\n")

sec("M3 · c4-m3-20 y -22: caminata aleatoria, S_t ~ t^(3/2) y KPSS")
set.seed(12)
for (m in c(100, 400, 1600)) {
  z <- replicate(500, { x <- cumsum(rnorm(m)); e <- x - mean(x); S <- cumsum(e)
    k <- suppressWarnings(kpss.test(x)); c(max(abs(S))/m^1.5, k$statistic, k$p.value <= 0.05) })
  cat(sprintf("n = %4d: mean max|S|/n^1.5 = %.3f | KPSS medio = %.2f | rechazo = %.2f\n", m, mean(z[1, ]), mean(z[2, ]), mean(z[3, ])))
}

sec("M4 · ACF/PACF del Nilo y de su diferencia; ARIMA(0,1,1); vecinos (c4-m4-02..17)")
cat("ACF Nilo 1-4:", round(acf(nilo, plot = FALSE)$acf[2:5], 3), "\n")
pn <- pacf(nilo, lag.max = 20, plot = FALSE)$acf; bn <- 1.96/sqrt(n)
cat("PACF Nilo 1-8:", round(pn[1:8], 3), "| fuera de ±", round(bn, 3), "en:", which(abs(pn) > bn), "\n")
cat("0.5^(1:4) =", 0.5^(1:4), "| banda n = 100:", round(bn, 3), "\n")
wd <- diff(nilo); bw <- 1.96/sqrt(length(wd))
aw <- acf(wd, lag.max = 20, plot = FALSE)$acf[-1]; pw <- pacf(wd, lag.max = 20, plot = FALSE)$acf
cat("banda n = 99:", round(bw, 4), "| ACF fuera en:", which(abs(aw) > bw), "valores", round(aw[abs(aw) > bw], 3), "\n")
cat("PACF de la diferencia 1-4:", round(pw[1:4], 3), "\n")
ee011 <- sqrt(f011$var.coef[1, 1])
cat("ARIMA(0,1,1): theta", r4(coef(f011)), "ee", r4(ee011), "t", round(coef(f011)/ee011, 2),
    "sigma2", round(f011$sigma2, 2), "LB(20, fitdf 1) p", r4(Box.test(residuals(f011), 20, "Ljung-Box", fitdf = 1)$p.value),
    "| 1 + theta =", round(1 + coef(f011), 3), "\n")
for (o in list(c(0,1,1), c(1,1,1), c(0,1,2), c(1,1,0))) {
  A <- Arima(nilo, order = o, method = "ML"); cat(sprintf("Arima(%s): AICc %.3f BIC %.3f\n", paste(o, collapse = ","), A$aicc, A$bic))
}

sec("M5 · constante y deriva (c4-m5-04, -10, -11, -12, -13, -17, -18, -19)")
f101 <- arima(nilo, c(1, 0, 1), method = "ML"); cat("arima(1,0,1) coef:", names(coef(f101)), r4(coef(f101)), "| media muestral", round(mean(nilo), 2), "\n")
av <- 0; fm <- withCallingHandlers(arima(nilo, c(1,1,1), include.mean = TRUE, method = "ML"), warning = function(w) {av <<- av + 1; invokeRestart("muffleWarning")})
cat("arima(1,1,1, include.mean = TRUE): coef", names(coef(fm)), "| avisos:", av, "\n")
Ad <- Arima(nilo, order = c(1, 1, 1), include.drift = TRUE, method = "ML")
Ax <- arima(nilo, order = c(1, 1, 1), xreg = seq_along(nilo), method = "ML")
cat("Arima con deriva:", names(coef(Ad)), r4(coef(Ad)), "| arima xreg seq_along:", r4(coef(Ax)), "\n")
eed <- sqrt(diag(Ad$var.coef))[["drift"]]
cat("deriva", r4(coef(Ad)[["drift"]]), "ee", r4(eed), "t", round(coef(Ad)[["drift"]]/eed, 3),
    "| c = delta(1-phi) =", r4(coef(Ad)[["drift"]] * (1 - coef(Ad)[["ar1"]])),
    "| AICc con", round(Ad$aicc, 3), "sin", round(Arima(nilo, order = c(1,1,1), method = "ML")$aicc, 3), "\n")
cat("cuerpo de Arima con seq_along:", any(grepl("drift = seq_along", deparse(body(Arima)))), "\n")
cat("formals(Arima)$include.drift =", formals(Arima)$include.drift, "\n")
w2 <- NULL; A2 <- withCallingHandlers(Arima(nilo, order = c(1, 2, 1), include.drift = TRUE, method = "ML"),
  warning = function(w) {w2 <<- conditionMessage(w); invokeRestart("muffleWarning")})
cat("Arima(1,2,1, include.drift = TRUE): coef", names(coef(A2)), "| aviso:", w2, "\n")
cat("auto.arima, líneas allowdrift/allowmean:\n"); cat(grep("allowdrift <-|allowmean <-", deparse(body(auto.arima)), value = TRUE), sep = "\n")
for (dd in 0:2) { tr <- capture.output(invisible(auto.arima(nilo, d = dd, stepwise = TRUE, trace = TRUE)))
  cat(sprintf("traza d = %d: 'drift' %d veces, 'non-zero mean' %d veces, %d líneas\n", dd,
    sum(grepl("drift", tr)), sum(grepl("non-zero mean", tr)), length(tr))) }
cat("Nile[1] =", nilo[1], "Nile[100] =", nilo[100], "| (y100 - y1)/99 =", r4((nilo[100] - nilo[1])/99),
    "| mean(diff) =", r4(mean(diff(nilo))), "| beta/99 =", r4(beta/99), "\n")
cat("medias 1871-1898 y 1899-1970:", round(mean(nilo[1:28]), 2), round(mean(nilo[29:100]), 2), "\n")

sec("M6 · criterios y n efectivo (c4-m6-02, -05)")
A111 <- Arima(nilo, order = c(1, 1, 1), method = "ML")
ll <- A111$loglik; k <- length(coef(A111)) + 1
for (ns in c(99, 100)) cat(sprintf("AICc a mano con n* = %d: %.4f | BIC: %.4f\n", ns, -2*ll + 2*k + 2*k*(k+1)/(ns - k - 1), -2*ll + k*log(ns)))
cat("Arima: AICc", sprintf("%.4f", A111$aicc), "BIC", sprintf("%.4f", A111$bic), "\n")
cat("nobs(arima d = 1, 2):", nobs(arima(nilo, c(0,1,1), method = "ML")), nobs(arima(nilo, c(0,2,1), method = "ML")), "\n")
cat("loglik arima(Nile, 0,1,1) =", r4(f011$loglik), "| MA(1) sin media sobre diff:", r4(arima(diff(nilo), c(0,0,1), include.mean = FALSE, method = "ML")$loglik), "\n")
cat("log(99) =", r4(log(99)), "\n")

sec("M6 · rejilla de 27 modelos con forecast::Arima (c4-m6-08, -09, -10, -11, -60, tabla)")
R <- do.call(rbind, lapply(0:2, function(d) do.call(rbind, lapply(0:2, function(p) do.call(rbind, lapply(0:2, function(q) {
  A <- Arima(nilo, order = c(p, d, q), include.mean = (d == 0), method = "ML")
  ar <- coef(A)[grepl("^ar", names(coef(A)))]; ma <- coef(A)[grepl("^ma", names(coef(A)))]
  lb <- if (20 > p + q) Box.test(residuals(A), 20, "Ljung-Box", fitdf = p + q)$p.value else NA
  data.frame(p, d, q, aicc = A$aicc, bic = A$bic, nobs = A$nobs,
    min_ar = if (length(ar)) min(Mod(polyroot(c(1, -ar)))) else NA,
    min_ma = if (length(ma)) min(Mod(polyroot(c(1, ma)))) else NA, lb = lb)
}))))))
R$daicc <- ave(R$aicc, R$d, FUN = function(a) a - min(a))
print(format(transform(R, aicc = round(aicc, 2), bic = round(bic, 2), daicc = round(daicc, 2),
  min_ar = round(min_ar, 4), min_ma = round(min_ma, 4), lb = round(lb, 4)), drop0trailing = FALSE), row.names = FALSE)
for (d in 0:2) { S <- R[R$d == d, ]
  cat(sprintf("d = %d: mejor AICc (%d,%d,%d) %.2f | mejor BIC (%d,%d,%d) %.2f | a menos de 2 (sin el mejor): %d\n", d,
    S$p[which.min(S$aicc)], d, S$q[which.min(S$aicc)], min(S$aicc), S$p[which.min(S$bic)], d, S$q[which.min(S$bic)], min(S$bic),
    sum(S$daicc > 0 & S$daicc < 2))) }
cat("LB(20) rechaza en", sum(R$lb < 0.05, na.rm = TRUE), "de 27; ¿alguno de ellos a menos de 2 del mejor de su d?",
    any(R$lb < 0.05 & R$daicc < 2, na.rm = TRUE), "\n")
D2 <- R[R$d == 2 & !is.na(R$min_ma), ]
cat("d = 2, min|raíz MA|:", paste(sprintf("(%d,2,%d) %.5f", D2$p, D2$q, D2$min_ma), collapse = "; "), "\n")
cat("d = 2 con raíz MA < 1.0005:", sum(D2$min_ma < 1.0005), "de 9 modelos\n")
cat("diferencia AICc (1,1,1) vs (0,1,1):", round(R$aicc[R$p==0&R$d==1&R$q==1] - R$aicc[R$p==1&R$d==1&R$q==1], 2), "\n")

sec("M6 · c4-m6-08: «el Módulo 7 contará siete» (d = 1, con y sin deriva) y traza de auto.arima")
G <- do.call(rbind, lapply(c(FALSE, TRUE), function(dr) do.call(rbind, lapply(0:2, function(p) do.call(rbind, lapply(0:2, function(q) {
  A <- Arima(nilo, order = c(p, 1, q), include.drift = dr, method = "ML")
  data.frame(p, q, deriva = dr, aicc = A$aicc) }))))))
G$dif <- G$aicc - min(G$aicc); G <- G[order(G$aicc), ]
print(transform(G, aicc = round(aicc, 2), dif = round(dif, 2)), row.names = FALSE)
cat("con d = 1 y p, q <= 2, con y sin deriva: modelos a menos de 2 del mejor, contando el mejor:", sum(G$dif < 2), "\n")
tr <- capture.output(invisible(auto.arima(nilo, trace = TRUE)))
cat(tr, sep = "\n")
