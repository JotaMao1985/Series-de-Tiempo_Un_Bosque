# Verificador B · R4 del capítulo 4 · repetición de las cifras de M7-M10
# Rscript diagnostico/cap4/comprobaciones/v4B_software.R > diagnostico/cap4/comprobaciones/v4B_software.out 2>&1
suppressPackageStartupMessages({library(forecast); library(tseries)})
cat(R.version.string, "· forecast", as.character(packageVersion("forecast")),
    "· tseries", as.character(packageVersion("tseries")), "\n")
sec <- function(t) cat("\n==== ", t, " ====\n", sep = "")
aicc <- function(f) { k <- length(f$coef) + 1; f$aic + 2 * k * (k + 1) / (f$nobs - k - 1) }
minraiz <- function(v) if (length(v)) min(Mod(polyroot(c(1, v)))) else NA

sec("A. código de forecast 9.0.2: umbral de raíces y valores por defecto")
f <- deparse(forecast:::myarima)
cat(grep("minroot <", f, value = TRUE), sep = "\n")
cat("aparece 1.001 o 1 + 0.001 en myarima:", any(grepl("1\\.001|0\\.001", f)), "\n")
fa <- formals(auto.arima)
cat("ic:", eval(fa$ic)[1], "· test:", eval(fa$test)[1], "· max.order:", fa$max.order,
    "· approximation:", deparse(fa$approximation), "\n")
cat("Nile: length > 150 || frequency > 12 =", length(Nile) > 150 || frequency(Nile) > 12, "\n")
fA <- deparse(forecast::auto.arima)
cat("método en auto.arima (líneas con CSS-ML/CSS):\n"); cat(grep('"CSS', fA, value = TRUE), sep = "\n")

sec("B. M7: trazas de auto.arima sobre el Nilo")
tr1 <- capture.output(a1 <- auto.arima(Nile, trace = TRUE, seasonal = FALSE))
tr2 <- capture.output(a2 <- auto.arima(Nile, trace = TRUE, seasonal = FALSE,
                                        stepwise = FALSE, approximation = FALSE))
l1 <- grep("^ ARIMA.*:", tr1, value = TRUE); l2 <- grep("^ ARIMA.*:", tr2, value = TRUE)
cat("escalonada:", length(l1), "modelos · exhaustiva:", length(l2), "\n")
cat("primeras cinco de la escalonada:\n"); cat(head(l1, 5), sep = "\n")
cat("escalonada con Inf:\n"); cat(grep("Inf", l1, value = TRUE), sep = "\n")
cat("ganadores:", as.character(a1), round(a1$aicc, 3), "|", as.character(a2), round(a2$aicc, 3), "\n")
v <- as.numeric(sub(".*:\\s*", "", l2)); nm <- trimws(sub(":.*", "", l2))
o <- order(v); podio <- data.frame(modelo = nm[o], aicc = v[o], dif = round(v[o] - min(v), 2))
print(head(podio, 9), row.names = FALSE)
cat("a menos de 2 puntos (incluido el ganador):", sum(podio$dif < 2), "\n")
ords <- regmatches(nm, regexpr("\\([0-9],[0-9],[0-9]\\)", nm))
pdq <- do.call(rbind, lapply(strsplit(gsub("[()]", "", ords), ","), as.integer))
cat("d en la exhaustiva:", unique(pdq[, 2]), "· máx p+q:", max(pdq[, 1] + pdq[, 3]), "\n")

sec("C. M7: el ARIMA(2,1,2) del Nilo según el estimador")
for (m in c("CSS-ML", "ML")) for (dr in c(FALSE, TRUE)) {
  a <- Arima(Nile, order = c(2, 1, 2), method = m, include.drift = dr)
  cat(sprintf("%-6s deriva=%-5s logL = %.3f  min|raíz AR| = %.6f  min|raíz MA| = %.6f\n", m, dr,
      a$loglik, minraiz(-coef(a)[c("ar1", "ar2")]), minraiz(coef(a)[c("ma1", "ma2")])))
}
g <- arima(Nile, order = c(2, 1, 2), method = "ML")  # el ajuste de la rejilla (genera_cap4.R)
cat(sprintf("stats::arima ML: logL %.3f, min|raíz AR| %.4f\n", g$loglik, minraiz(-coef(g)[1:2])))

sec("D. M8")
f111 <- arima(Nile, order = c(1, 1, 1), method = "ML")
cat(sprintf("ARIMA(1,1,1) ML: phi %.4f theta %.4f · LB(20,fitdf=2) p %.3f · Shapiro p %.3f\n",
    coef(f111)[1], coef(f111)[2], Box.test(residuals(f111), 20, "Ljung-Box", fitdf = 2)$p.value,
    shapiro.test(residuals(f111))$p.value))
cat(sprintf("raíz MA %.3f · raíz AR %.2f\n", minraiz(coef(f111)[2]), minraiz(-coef(f111)[1])))
for (d in 2:3) {
  ff <- arima(diff(Nile, differences = d), order = c(0, 0, 1), include.mean = FALSE, method = "ML")
  cat(sprintf("d=%d: theta %.6f sigma2 %.2f · var(diff(Nile,%d)) = %.2f\n", d, coef(ff), ff$sigma2,
      d - 1, var(diff(Nile, differences = d - 1))))
}
cat("rejilla d = 2 (ML): min|raíz MA| y BIC\n")
for (q in 0:2) for (p in 0:2) {
  ff <- arima(Nile, order = c(p, 2, q), method = "ML")
  cat(sprintf("  (%d,2,%d) MA %s BIC %.2f\n", p, q,
      if (q) sprintf("%.6f", minraiz(coef(ff)[grepl("^ma", names(coef(ff)))])) else "   -    ", BIC(ff)))
}
r1n <- acf(Nile, plot = FALSE)$acf[2]
cat(sprintf("Nilo: r1 %.3f · var(diff)/var %.3f · 2(1-r1) %.3f\n", r1n, var(diff(Nile)) / var(Nile), 2 * (1 - r1n)))
ly <- log(lynx)
cat(sprintf("log(lynx): var %.3f -> %.3f (reducción %.1f %%) · r1(diff) %.3f\n", var(ly), var(diff(ly)),
    100 * (1 - var(diff(ly)) / var(ly)), acf(diff(ly), plot = FALSE)$acf[2]))
cat("ndiffs kpss/adf/pp:", ndiffs(ly, test = "kpss"), ndiffs(ly, test = "adf"), ndiffs(ly, test = "pp"), "\n")
suppressWarnings(cat(sprintf("adf.test p %.3f · kpss.test p %.3f · PP.test p %.4f · pp.test p %.3f\n",
    adf.test(ly)$p.value, kpss.test(ly)$p.value, PP.test(ly)$p.value, pp.test(ly)$p.value)))
f211 <- arima(ly, order = c(2, 1, 1), method = "ML")
cat(sprintf("ARIMA(2,1,1) log(lynx): |raíz MA| %.5f\n", minraiz(coef(f211)[3])))
esc <- as.numeric(time(Nile) >= 1899)
cat(sprintf("medias: antes de 1899 %.2f · desde 1899 %.2f\n", mean(Nile[esc == 0]), mean(Nile[esc == 1])))
fe <- arima(Nile, order = c(0, 0, 0), xreg = esc, method = "ML")
cat(sprintf("escalón: beta %.2f e.e. %.2f t %.2f AICc %.2f · LB(20) p %.3f · sd resid %.2f\n",
    coef(fe)[2], sqrt(fe$var.coef[2, 2]), coef(fe)[2] / sqrt(fe$var.coef[2, 2]), aicc(fe),
    Box.test(residuals(fe), 20, "Ljung-Box")$p.value, sd(residuals(fe))))
best0 <- NULL
for (p in 0:2) for (q in 0:2) {
  ff <- tryCatch(arima(Nile, order = c(p, 0, q), method = "ML"), error = function(e) NULL)
  if (!is.null(ff)) best0 <- rbind(best0, data.frame(p, q, aicc = aicc(ff)))
}
cat("mejor ARMA d = 0 (rejilla 0..2):\n"); print(head(best0[order(best0$aicc), ], 3), row.names = FALSE)
ent <- window(Nile, end = 1950); pru <- window(Nile, start = 1951); esc_e <- as.numeric(time(ent) >= 1899)
er <- function(p) c(rmse = sqrt(mean((pru - p)^2)), mae = mean(abs(pru - p)))
oos <- rbind(arima = er(forecast(Arima(ent, order = c(1, 1, 1)), h = 20)$mean),
             escalon = er(forecast(Arima(ent, order = c(0, 0, 0), xreg = esc_e), xreg = rep(1, 20))$mean),
             escalon_ar1 = er(forecast(Arima(ent, order = c(1, 0, 0), xreg = esc_e), xreg = rep(1, 20))$mean),
             naive = er(rep(tail(ent, 1), 20)), media = er(rep(mean(ent), 20)))
print(round(oos, 2))
cat(sprintf("sd de los residuales: ARIMA(1,1,1) Arima %.2f · arima ML %.2f\n",
    sd(residuals(Arima(Nile, order = c(1, 1, 1)))), sd(residuals(f111))))

sec("E. M9")
formas <- list(d0 = Arima(Nile, order = c(1, 0, 1)), d1 = Arima(Nile, order = c(1, 1, 1)),
               d1drift = Arima(Nile, order = c(1, 1, 1), include.drift = TRUE),
               d2 = suppressWarnings(Arima(Nile, order = c(1, 2, 1))))
cat(sprintf("ARMA(1,1) media CSS-ML %.2f · ML %.2f · media muestral %.2f\n", coef(formas$d0)[["intercept"]],
    coef(arima(Nile, order = c(1, 0, 1), method = "ML"))[["intercept"]], mean(Nile)))
for (nm in names(formas)) {
  fc <- forecast(formas[[nm]], h = 30, level = 95); m <- as.numeric(fc$mean)
  cat(sprintf("%-8s h1 %.2f h30 %.2f dif1 %.3f dif2 %.6f ancho95 h1 %.0f h30 %.0f\n", nm, m[1], m[30],
      m[30] - m[29], m[30] - 2 * m[29] + m[28], fc$upper[1] - fc$lower[1], fc$upper[30] - fc$lower[30]))
}
w <- tryCatch(Arima(Nile, order = c(1, 2, 1), include.drift = TRUE), warning = function(w) conditionMessage(w))
cat("aviso con d = 2 y deriva:", if (is.character(w)) w else "ninguno", "\n")
f2 <- formas$d2; ph2 <- coef(f2)[["ar1"]]
cat(sprintf("ARIMA(1,2,1): phi %.4f theta %.6f · 1/(1-phi) %.4f\n", ph2, coef(f2)[["ma1"]], 1 / (1 - ph2)))
m2 <- as.numeric(forecast(f2, h = 30)$mean); d2s <- diff(m2, differences = 2)
cat("cociente de segundas diferencias consecutivas h=3..8:", round(d2s[2:7] / d2s[1:6], 4), "\n")
psi2 <- c(1, ARMAtoMA(ar = c(2 + ph2, -(1 + 2 * ph2), ph2), ma = coef(f2)[["ma1"]], lag.max = 29))
fc2 <- forecast(f2, h = 30, level = 95)
cat(sprintf("psi_29 %.4f · ancho con psi %.2f · ancho forecast %.2f\n", psi2[30],
    2 * qnorm(0.975) * sqrt(f2$sigma2 * sum(psi2^2)), fc2$upper[30] - fc2$lower[30]))
f1 <- formas$d1; ph <- coef(f1)[["ar1"]]; th <- coef(f1)[["ma1"]]; s <- sqrt(f1$sigma2)
psi <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = 400))
cerr <- ((1 + th) - (ph + th) * ph^(1:30)) / (1 - ph)
sh <- s * sqrt(cumsum(psi[1:30]^2)); fc1 <- forecast(f1, h = 30, level = 95)
cat(sprintf("phi %.4f theta %.4f · psi_inf %.4f · psi_400 %.4f · max|psi - cerrada| %.1e\n", ph, th,
    (1 + th) / (1 - ph), psi[401], max(abs(psi[2:31] - cerr))))
cat(sprintf("sigma %.3f · sigma_30 %.2f · sigma*sqrt(30) %.2f · cociente %.2f · sigma30/sigma1 %.3f\n",
    s, sh[30], s * sqrt(30), s * sqrt(30) / sh[30], sh[30] / sh[1]))
cat(sprintf("max|semiancho - 1.96 sigma_h| %.2e\n", max(abs((fc1$upper - fc1$lower) / 2 - qnorm(.975) * sh))))
dyT <- as.numeric(Nile[100] - Nile[99]); eT <- as.numeric(tail(residuals(f1), 1))
pr <- as.numeric(forecast(f1, h = 30)$mean); dpr <- diff(c(Nile[100], pr))
cat(sprintf("recursión: max|∇ŷ - phi^(h-1)(phi∇y_T + theta e_T)| %.1e · límite %.2f\n",
    max(abs(dpr - ph^(0:29) * (ph * dyT + th * eT))), Nile[100] + (ph * dyT + th * eT) / (1 - ph)))
cat("qnorm(.975), qnorm(.90):", round(qnorm(.975), 4), round(qnorm(.90), 4), "\n")

sec("F. M10 · Nilo")
suppressWarnings(cat(sprintf("adf p %.3f · kpss p %.3f · pp.test p %.3f · PP.test p %.4f · r1 %.3f\n",
    adf.test(Nile)$p.value, kpss.test(Nile)$p.value, pp.test(Nile)$p.value, PP.test(Nile)$p.value, r1n)))
cat("ACF y PACF de diff(Nile), rezagos 1..6:\n")
print(round(rbind(acf = acf(diff(Nile), 6, plot = FALSE)$acf[-1], pacf = pacf(diff(Nile), 6, plot = FALSE)$acf), 3))
fd <- Arima(Nile, order = c(1, 1, 1), include.drift = TRUE); fs <- Arima(Nile, order = c(1, 1, 1))
cat(sprintf("deriva %.3f t %.2f AICc %.2f frente a %.2f · media dif %.2f · beta/99 %.2f\n", coef(fd)[["drift"]],
    coef(fd)[["drift"]] / sqrt(diag(fd$var.coef))[["drift"]], fd$aicc, fs$aicc, mean(diff(Nile)), coef(fe)[2] / 99))
for (o in list(c(1, 1, 1), c(0, 1, 1), c(1, 2, 2))) {
  ff <- arima(Nile, order = o, method = "ML")
  cat(sprintf("(%s) AICc %.2f BIC %.2f nobs %d\n", paste(o, collapse = ","), aicc(ff), BIC(ff), ff$nobs))
}
gr <- NULL
for (p in 0:2) for (q in 0:2) { ff <- arima(Nile, order = c(p, 1, q), method = "ML")
  gr <- rbind(gr, data.frame(p, q, aicc = aicc(ff), bic = BIC(ff))) }
cat("rejilla d=1: min AICc", with(gr[which.min(gr$aicc), ], paste(p, q)), "· min BIC", with(gr[which.min(gr$bic), ], paste(p, q)), "\n")

sec("F. M10 · TRM")
trm <- ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
cat("n =", length(trm), "· acf1 niveles", round(acf(trm, plot = FALSE)$acf[2], 3), "\n")
suppressWarnings(print(round(rbind(adf = c(adf.test(trm)$statistic, adf.test(trm)$p.value),
  kpss = c(kpss.test(trm)$statistic, kpss.test(trm)$p.value),
  adf_d = c(adf.test(diff(trm))$statistic, adf.test(diff(trm))$p.value),
  kpss_d = c(kpss.test(diff(trm))$statistic, kpss.test(diff(trm))$p.value)), 3)))
cat("ndiffs", ndiffs(trm), "· nsdiffs", nsdiffs(trm), "· nsdiffs ocsb", nsdiffs(trm, test = "ocsb"), "\n")
cat("umbral de nsdiffs en el código:", grep("0.64", deparse(forecast::nsdiffs), value = TRUE), "\n")
r <- acf(diff(trm), 20, plot = FALSE)$acf[-1]; banda <- 1.96 / sqrt(137)
cat(sprintf("rho1 %.3f rho8 %.3f banda %.3f fuera: %s\n", r[1], r[8], banda, paste(which(abs(r) > banda), collapse = " ")))
gt <- NULL; fits <- list()
for (p in 0:2) for (q in 0:2) { ff <- arima(trm, order = c(p, 1, q), method = "ML"); fits[[paste(p, q)]] <- ff
  gt <- rbind(gt, data.frame(p, q, aicc = aicc(ff), bic = BIC(ff))) }
gt <- gt[order(gt$aicc), ]; print(head(gt, 3), row.names = FALSE)
cat(sprintf("ventaja del (2,1,2): %.2f\n", gt$aicc[2] - gt$aicc[1]))
f212 <- fits[["2 2"]]
cat(sprintf("(2,1,2): ar %s ma %s · |AR| %.6f |MA| %.9f\n", paste(round(coef(f212)[1:2], 4), collapse = " "),
    paste(round(coef(f212)[3:4], 6), collapse = " "), minraiz(-coef(f212)[1:2]), minraiz(coef(f212)[3:4])))
ra <- polyroot(c(1, -coef(f212)[1:2])); rm <- polyroot(c(1, coef(f212)[3:4]))
cat("raíces AR", format(ra, digits = 4), "· MA", format(rm, digits = 4), "\n")
cat("dist. mín. entre raíces AR y MA:", round(min(outer(ra, rm, function(a, b) Mod(a - b))), 4), "\n")
tr3 <- capture.output(at <- auto.arima(trm, stepwise = FALSE, approximation = FALSE, trace = TRUE))
cat("auto.arima exhaustivo:", as.character(at), "· líneas (2,1,2):\n"); cat(grep("ARIMA\\(2,1,2\\)", tr3, value = TRUE), sep = "\n")
rw <- arima(trm, order = c(0, 1, 0), method = "ML"); e <- residuals(rw); s <- sqrt(rw$sigma2)
cat(sprintf("LB20 %.4f LB12 %.4f Shapiro %.5f LB12 cuadrados %.4f sigma %.2f\n",
    Box.test(e, 20, "Ljung-Box")$p.value, Box.test(e, 12, "Ljung-Box")$p.value, shapiro.test(e)$p.value,
    Box.test(e^2, 12, "Ljung-Box")$p.value, s))
fdt <- Arima(trm, order = c(0, 1, 0), include.drift = TRUE)
cat(sprintf("deriva %.4f ee %.2f t %.2f · media dif %.4f · (yn-y1)/(n-1) %.4f\n", coef(fdt), sqrt(fdt$var.coef[1, 1]),
    coef(fdt) / sqrt(fdt$var.coef[1, 1]), mean(diff(trm)), (trm[138] - trm[1]) / 137))
yT <- trm[138]; z <- qnorm(.975)
cat(sprintf("yT %.2f · semiancho24 %.2f · [%.2f, %.2f] · cociente %.4f\n", yT, z * s * sqrt(24), yT - z * s * sqrt(24),
    yT + z * s * sqrt(24), z * s * sqrt(24) / yT))
d1 <- diff(trm); d12 <- diff(trm, lag = 12)
kurt <- function(x) mean((x - mean(x))^4) / mean((x - mean(x))^2)^2
asim <- function(x) mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5
cat(sprintf("fuera 95 %% a 1 mes %d (arriba %d) de %d · a 12: %d de %d (%.1f %%) · kurt %.2f / %.2f · asim %.3f\n",
    sum(abs(d1) > z * s), sum(d1 > z * s), length(d1), sum(abs(d12) > z * s * sqrt(12)), length(d12),
    100 * mean(abs(d12) > z * s * sqrt(12)), kurt(d1), kurt(d12), asim(d1)))
cat(sprintf("cubre 80 %% a un mes %.4f · razones h=3,6,12: %s\n", mean(abs(d1) <= qnorm(.9) * s),
    paste(round(sapply(c(3, 6, 12), function(h) mean(diff(trm, lag = h)^2) / (h * s^2)), 3), collapse = " ")))
o <- order(d1, decreasing = TRUE)[1:3]; cat("mayores alzas:", paste(format(time(d1)[o], nsmall = 3), round(d1[o], 1)), "\n")
cat("binomial 5 de 6:", round(binom.test(5, 6, alternative = "greater")$p.value, 3), "\n")

sec("F. M10 · puente AirPassengers")
lap <- log(AirPassengers)
mej <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
rr <- Acf(residuals(mej), 24, plot = FALSE)$acf[-1]
cat(as.character(mej), sprintf("rho12 %.4f rho24 %.4f banda %.4f nobs %d\n", rr[12], rr[24], 1.96 / sqrt(144), mej$nobs))
amp <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE, max.p = 8, max.q = 8, max.order = 16)
cat(as.character(amp), round(Acf(residuals(amp), 24, plot = FALSE)$acf[13], 3), "\n")
air <- Arima(lap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
cat(sprintf("airline rho12 %.4f LB24 p %.4f nobs %d\n", Acf(residuals(air), 24, plot = FALSE)$acf[13],
    Box.test(residuals(air), 24, "Ljung-Box", fitdf = 2)$p.value, air$nobs))

sec("F. M10 · ejercicios")
n <- 150; ak <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2 * k * (k + 1) / (n - k - 1) }
f011 <- arima(BJsales, order = c(0, 1, 1), method = "ML"); f111b <- arima(BJsales, order = c(1, 1, 1), method = "ML")
cat("acf resid (0,1,1) 1..4:", round(acf(residuals(f011), 4, plot = FALSE)$acf[-1], 4), "banda", round(1.96 / sqrt(150), 4), "\n")
cat(sprintf("phi (1,1,1) %.4f · LB20 %.4f -> %.4f\n", coef(f111b)[1],
    Box.test(residuals(f011), 20, "Ljung-Box", fitdf = 1)$p.value, Box.test(residuals(f111b), 20, "Ljung-Box", fitdf = 2)$p.value))
b2 <- NULL; for (p in 0:2) for (q in 0:2) { ff <- arima(BJsales, order = c(p, 2, q), method = "ML")
  b2 <- rbind(b2, data.frame(p, q, aicc = ak(ff, n - 2), ma = minraiz(coef(ff)[grepl("^ma", names(coef(ff)))]))) }
cat("mejor d=2:\n"); print(head(b2[order(b2$aicc), ], 2), row.names = FALSE)
cat(sprintf("AICc (1,1,1) %.3f · nobs %d y %d\n", ak(f111b, n - 1), f111b$nobs, arima(BJsales, order = c(1, 2, 2), method = "ML")$nobs))
fb <- Arima(BJsales, order = c(1, 1, 1)); phb <- coef(fb)[1]; thb <- coef(fb)[2]
psb <- c(1, ARMAtoMA(ar = c(1 + phb, -phb), ma = thb, lag.max = 12)); shb <- sqrt(fb$sigma2) * sqrt(cumsum(psb^2))[1:12]
cat(sprintf("BJ psi_12 %.4f límite %.4f · sigma12/(sigma sqrt12) %.4f\n", psb[13], (1 + thb) / (1 - phb), shb[12] / (sqrt(fb$sigma2) * sqrt(12))))
fbd <- Arima(BJsales, order = c(1, 1, 1), include.drift = TRUE)
cat(sprintf("deriva %.4f t %.4f AICc %.3f vs %.3f · h12 %.2f vs %.2f\n", coef(fbd)[["drift"]],
    coef(fbd)[["drift"]] / sqrt(diag(fbd$var.coef))[["drift"]], fbd$aicc, fb$aicc,
    forecast(fbd, h = 12)$mean[12], forecast(fb, h = 12)$mean[12]))
fl <- arima(ly, order = c(2, 0, 0), method = "ML"); rl <- polyroot(c(1, -coef(fl)[1:2]))
p1 <- coef(fl)[1]; p2 <- coef(fl)[2]
cat(sprintf("lynx AR(2) phi %.4f %.4f periodo raíz %.4f · fórmula FPP3 %.4f · LB20 %.4f\n", p1, p2,
    2 * pi / Arg(rl[which.max(Im(rl))]), 2 * pi / acos(-p1 * (1 - p2) / (4 * p2)),
    Box.test(residuals(fl), 20, "Ljung-Box", fitdf = 2)$p.value))
cat("var de log(lynx) por d=0..3:", round(sapply(0:3, function(d) var(if (d == 0) ly else diff(ly, differences = d))), 4), "\n")
cat(sprintf("r1 %.3f cociente %.3f 2(1-r1) %.3f · auto.arima %s\n", acf(ly, plot = FALSE)$acf[2], var(diff(ly)) / var(ly),
    2 * (1 - acf(ly, plot = FALSE)$acf[2]), as.character(auto.arima(ly, stepwise = FALSE, approximation = FALSE, seasonal = FALSE))))
a_ml <- arima(Nile, order = c(1, 1, 1), method = "ML"); A_c <- Arima(Nile, order = c(1, 1, 1))
cat(sprintf("sigma2 arima ML %.2f · Arima %.2f · razón %.5f · 99/97 %.5f · SSR(Arima)/97 %.2f\n", a_ml$sigma2,
    A_c$sigma2, A_c$sigma2 / a_ml$sigma2, 99 / 97, sum(residuals(A_c)^2) / 97))

sec("G. M9 c4-m9-10/-19: con theta fijo, ¿coinciden fórmula y forecast()?")
for (th0 in c(-0.90, -0.99, -1.00)) {
  ff <- suppressWarnings(Arima(Nile, order = c(1, 2, 1), fixed = c(NA, th0), transform.pars = FALSE))
  p0 <- coef(ff)[["ar1"]]
  ps <- c(1, ARMAtoMA(ar = c(2 + p0, -(1 + 2 * p0), p0), ma = th0, lag.max = 29))
  fcx <- suppressWarnings(forecast(ff, h = 30, level = 95))
  cat(sprintf("theta %.2f: razón ancho forecast()/fórmula en h=30 = %.4f\n", th0,
      (fcx$upper[30] - fcx$lower[30]) / (2 * qnorm(.975) * sqrt(ff$sigma2 * sum(ps^2)))))
}
sec("G. M10 c4-m10-71: divisores de sigma2")
cat(sprintf("arima ML: sigma2 %.2f · SSR(residuos)/99 %.2f · SSR/100 %.2f\n", a_ml$sigma2,
    sum(residuals(a_ml)^2) / 99, sum(residuals(a_ml)^2) / 100))

sec("G. M10 c4-m10-10: log-retornos de la TRM (remisión al cap. 3)")
ret <- diff(log(trm)) * 100
cat(sprintf("n %d · r1 %.3f · banda %.3f · LB p (6, 10, 12, 20): %s · auto.arima %s\n", length(ret),
    acf(ret, plot = FALSE)$acf[2], 1.96 / sqrt(length(ret)),
    paste(sapply(c(6, 10, 12, 20), function(k) sprintf("%.4f", Box.test(ret, k, "Ljung-Box")$p.value)), collapse = " "),
    as.character(auto.arima(ret))))
