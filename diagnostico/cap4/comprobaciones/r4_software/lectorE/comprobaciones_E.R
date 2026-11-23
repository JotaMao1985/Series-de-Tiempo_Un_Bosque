# Lector E · R4 «fuentes» del capítulo 4 · comprobaciones ejecutadas (R 4.6.0, forecast 9.0.2, tseries)
# Uso (desde Htmls_Series/datos, para que lea la copia fija y no descargue nada):
#   Rscript comprobaciones_E.R
suppressMessages({library(forecast); library(tseries)})
cat("forecast", as.character(packageVersion("forecast")), "|", R.version.string, "\n\n")
trm <- ts(read.csv("trm_mensual_2015-01_2026-06.csv")$trm, start = c(2015, 1), frequency = 12)
meses <- format(seq(as.Date("2015-01-01"), by = "month", length.out = 138), "%Y-%m")

cat("== 1. Umbral de raíces en el código de forecast (myarima) ==\n")
am <- paste(deparse(forecast:::myarima), collapse = "\n")
cat("minroot < 1 + 0.01 :", grepl("minroot < 1 \\+ 0.01", am), "\n")
cat("aparece 1.001 / 1 + 0.001 :", grepl("1\\.001|1 \\+ 0\\.001", am), "\n")
l <- grep("minroot", strsplit(am, "\n")[[1]], value = TRUE); cat(l, sep = "\n")

cat("\n== 1b. auto.arima exhaustivo sobre la TRM con trace: ¿evalúa el (2,1,2) y lo descarta? ==\n")
tr <- capture.output(a <- auto.arima(trm, stepwise = FALSE, approximation = FALSE, trace = TRUE))
cat(grep("ARIMA\\(2,1,2\\)", tr, value = TRUE), sep = "\n")
cat("elegido:", as.character(a), "\n")
cat("n de modelos listados:", sum(grepl("^ ARIMA", tr)), "\n")

cat("\n== 2. Pruebas por defecto de auto.arima / ndiffs ==\n")
cat("auto.arima test por defecto:", eval(formals(auto.arima)$test)[1], "\n")
cat("ndiffs  test por defecto  :", eval(formals(ndiffs)$test)[1], "\n")
cat("auto.arima max.order      :", formals(auto.arima)$max.order, "\n")

cat("\n== 3. ARIMA(2,1,2) de la TRM: ¿cancelación? errores estándar, raíces ==\n")
f212 <- arima(trm, order = c(2, 1, 2), method = "ML")
print(round(coef(f212), 4)); print(round(sqrt(diag(f212$var.coef)), 4))
rar <- Mod(polyroot(c(1, -coef(f212)[1:2]))); rma <- Mod(polyroot(c(1, coef(f212)[3:4])))
cat("|raíces AR| =", format(rar, digits = 10), "\n|raíces MA| =", format(rma, digits = 10), "\n")
cat("coef ma2 =", format(coef(f212)[["ma2"]], digits = 10), "\n")
cat("cond. número Hessiano-aprox (var.coef):", format(kappa(f212$var.coef, exact = TRUE), digits = 4), "\n")
ar_p <- c(1, -coef(f212)[1:2]); ma_p <- c(1, coef(f212)[3:4])
cat("polinomio AR:", round(ar_p, 3), " MA:", round(ma_p, 3), "\n")
cat("raíces AR complejas:", format(polyroot(ar_p), digits = 4), "\n")
cat("raíces MA complejas:", format(polyroot(ma_p), digits = 4), "\n")
cat("distancia entre raíces AR y MA (par más cercano):",
    format(min(abs(outer(polyroot(ar_p), polyroot(ma_p), "-"))), digits = 3), "\n")
cat("AICc (2,1,2):", round(f212$aic + 2 * 5 * 6 / (f212$nobs - 5 - 1), 2), "\n")

cat("\n== 4. Deriva del ARIMA(0,1,0) frente a la media de las diferencias ==\n")
fd <- Arima(trm, order = c(0, 1, 0), include.drift = TRUE)
cat("deriva ML =", format(coef(fd)[["drift"]], digits = 8), "\n")
cat("media de las diferencias =", format(mean(diff(trm)), digits = 8),
    " (y_n - y_1)/(n-1) =", format((trm[138] - trm[1]) / 137, digits = 8), "\n")

cat("\n== 5. Log-retornos de la TRM (el 'ruido blanco' del Capítulo 3) ==\n")
ret <- diff(log(trm))
cat("n =", length(ret), " r1 =", round(acf(ret, plot = FALSE)$acf[2], 3),
    " banda =", round(1.96 / sqrt(length(ret)), 3), "\n")
cat("Ljung-Box(10,20) p =", round(Box.test(ret, 10, "Ljung-Box")$p.value, 3),
    round(Box.test(ret, 20, "Ljung-Box")$p.value, 3), "\n")
cat("auto.arima(ret):", as.character(auto.arima(ret)), "\n")

cat("\n== 6. Cambios mensuales de la TRM: los mayores y los que salen del 95 % ==\n")
d1 <- diff(trm); s <- sqrt(arima(trm, order = c(0, 1, 0), method = "ML")$sigma2)
nm <- meses[-1]
o <- order(d1, decreasing = TRUE)[1:5]; cat("mayores subidas:", paste(nm[o], round(d1[o], 1)), sep = "\n  ")
o <- order(d1)[1:3]; cat("\nmayores bajadas:", paste(nm[o], round(d1[o], 1)), sep = "\n  ")
fuera <- which(abs(d1) > qnorm(.975) * s)
cat("\nfuera del 95 %:", paste(nm[fuera], round(d1[fuera], 1)), sep = "\n  ")
cat("\nsigma =", round(s, 2), " sigma^2 =", round(s^2, 2), "\n")
cat("por debajo:", sum(d1 < -qnorm(.975) * s), " por arriba:", sum(d1 > qnorm(.975) * s), "\n")
cat("binomial (5 de 6, p = .5): una cola", round(binom.test(5, 6, .5, "greater")$p.value, 3),
    "  dos colas", round(binom.test(5, 6, .5)$p.value, 3), "\n")
cat("asimetría de d1:", round(mean((d1 - mean(d1))^3) / mean((d1 - mean(d1))^2)^1.5, 3),
    " curtosis (no exceso):", round(mean((d1 - mean(d1))^4) / mean((d1 - mean(d1))^2)^2, 2), "\n")

cat("\n== 7. «Un tercio del nivel»: semiancho a h = 24 / último dato ==\n")
z <- qnorm(.975); yT <- as.numeric(tail(trm, 1))
cat("semiancho24 =", round(z * s * sqrt(24), 2), " yT =", yT, " cociente =", round(z * s * sqrt(24) / yT, 4), "\n")

cat("\n== 8. hσ² frente a la varianza real de los cambios a h meses, con ρ1 ==\n")
r1 <- acf(d1, plot = FALSE)$acf[2]
rat <- sapply(c(3, 6, 12), function(h) mean(diff(trm, lag = h)^2) / (h * s^2))
teo <- sapply(c(3, 6, 12), function(h) (h + 2 * (h - 1) * r1) / h)   # solo con rho_1 (MA(1) en los cambios)
cat("rho1 =", round(r1, 3), "\n razón medida:", round(rat, 3), "\n razón con solo rho1:", round(teo, 3), "\n")
for (rr in c(1.07, 1.14)) cat(" cobertura nominal 95 % con varianza", rr, "veces mayor (normal):",
  round(2 * pnorm(1.96 / sqrt(rr)) - 1, 4), "\n")

cat("\n== 9. Estacionalidad de la TRM: nsdiffs y fuerza estacional ==\n")
cat("código de nsdiffs (líneas con 0.64):", grep("0\\.64", deparse(nsdiffs), value = TRUE), sep = "\n  ")
cat("nsdiffs(trm) por defecto (seas):", nsdiffs(trm), " | ocsb:", nsdiffs(trm, test = "ocsb"), "\n")
dd <- mstl(trm, iterate = 1)
FS <- max(0, 1 - var(dd[, "Remainder"]) / var(dd[, "Seasonal12"] + dd[, "Remainder"]))
cat("F_S (1 - Var(R)/Var(S+R)) =", round(FS, 3), "\n")

cat("\n== 10. Nilo: ARIMA(1,1,1), ψ∞ y cocientes de σ_h ==\n")
n111 <- arima(Nile, order = c(1, 1, 1), method = "ML")
ph <- coef(n111)[["ar1"]]; th <- coef(n111)[["ma1"]]
cat("phi =", round(ph, 4), " theta =", round(th, 4), " sigma2 =", round(n111$sigma2, 1), "\n")
cat("psi_inf = (1+theta)/(1-phi) =", round((1 + th) / (1 - ph), 4), "\n")
psi <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = 400))   # (1-B)(1-phi B) y = (1+theta B) e
cat("psi_j para j = 200..400 (último):", round(tail(psi, 1), 4), "\n")
vh <- function(h) sum(psi[1:h]^2)
cat("sigma_30/sigma_1 =", round(sqrt(vh(30) / vh(1)), 3), "  sqrt(30) =", round(sqrt(30), 3), "\n")
cat("sigma_h aprox sigma*psi_inf*sqrt(h) para h = 30, 200:",
    round(sqrt(vh(30)), 3), "vs", round(((1 + th) / (1 - ph)) * sqrt(30), 3), ";",
    round(sqrt(vh(200)), 3), "vs", round(((1 + th) / (1 - ph)) * sqrt(200), 3), "\n")
psi0 <- c(1, ARMAtoMA(ar = c(1), ma = -1, lag.max = 20))                # ARIMA(0,1,1) con theta = -1
cat("ARIMA(0,1,1) con theta = -1: psi_1..psi_5 =", psi0[2:6], " Var h=1..4:",
    sapply(1:4, function(h) sum(psi0[1:h]^2)), "\n")
cat("pronóstico ARIMA(1,1,1) del Nilo a 1 y 30 pasos:",
    round(forecast(n111, h = 30)$mean[c(1, 30)], 2), " ultimo dato:", tail(Nile, 1), "\n")
cat("ACF Nilo nivel rho1 =", round(acf(Nile, plot = FALSE)$acf[2], 3),
    " rho1 de diff =", round(acf(diff(Nile), plot = FALSE)$acf[2], 3), "\n")
cat("adf.test p =", round(adf.test(Nile)$p.value, 3), " kpss p =", suppressWarnings(kpss.test(Nile)$p.value),
    " pp.test p =", suppressWarnings(pp.test(Nile)$p.value), "\n")
cat("|raíz MA| y |raíz AR| del (1,1,1):", round(1 / abs(th), 3), round(1 / abs(ph), 2), "\n")
cat("ndiffs(Nile) =", ndiffs(Nile), "\n")
