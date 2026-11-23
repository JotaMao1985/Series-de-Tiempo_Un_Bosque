# Verificador independiente B · R5 del capítulo 4 · ejercicios 1-3 del M10 y quiz
# Cálculo propio (no reutiliza los bloques del redactor). Salida: v5B_m10_quiz.out
suppressPackageStartupMessages({ library(forecast); library(tseries); library(tsibbledata); library(dplyr) })
options(width = 120)
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")),
    "| tsibbledata", as.character(packageVersion("tsibbledata")), "\n")
sec <- function(x) cat("\n==================== ", x, " ====================\n")
mi_aicc <- function(f, nst) { k <- length(f$coef) + 1; -2 * f$loglik + 2 * k + 2 * k * (k + 1) / (nst - k - 1) }
min_raiz <- function(cf) if (length(cf)) min(Mod(polyroot(c(1, cf)))) else NA

## ------------------------------------------------------------------ E1
sec("E1 BJsales")
y <- BJsales; n <- length(y)
cat("n =", n, "\n")
print(c(adf_p = adf.test(y)$p.value, kpss_d = ndiffs(y, test = "kpss"),
        adf_d = ndiffs(y, test = "adf"), pp_d = ndiffs(y, test = "pp")))
cat("r1 diff1, diff2:", sapply(1:2, function(d) acf(diff(y, differences = d), plot = FALSE)$acf[2]), "\n")
rej <- do.call(rbind, lapply(1:2, function(d) do.call(rbind, lapply(0:2, function(q) do.call(rbind, lapply(0:2, function(p) {
  f <- Arima(y, order = c(p, d, q), method = "ML")
  g <- arima(y, order = c(p, d, q), method = "ML")
  data.frame(d = d, p = p, q = q, aicc_Arima = f$aicc, aicc_mio = mi_aicc(g, n - d), bic = f$bic,
             lb20 = Box.test(residuals(g), lag = 20, type = "Ljung-Box", fitdf = p + q)$p.value,
             raizMA = min_raiz(coef(g)[grepl("^ma", names(coef(g)))]))
}))))))
print(rej, digits = 6)
r1g <- subset(rej, d == 1); r1g$puesto <- rank(r1g$aicc_mio)
cat("puesto del (0,1,1) en d=1:", r1g$puesto[r1g$p == 0 & r1g$q == 1], "de", nrow(r1g),
    " distancia al mejor:", r1g$aicc_mio[r1g$p == 0 & r1g$q == 1] - min(r1g$aicc_mio), "\n")
cat("min BIC d=1:", with(r1g, paste(p, q)[which.min(bic)]), "\n")
r2g <- subset(rej, d == 2)
cat("mejor d=2 por AICc:", with(r2g, paste(p, d, q)[which.min(aicc_mio)]), min(r2g$aicc_mio),
    " | mejor d=1:", min(r1g$aicc_mio), " | min global en d =", rej$d[which.min(rej$aicc_mio)], "\n")
f011 <- arima(y, order = c(0, 1, 1), method = "ML")
a <- acf(residuals(f011), lag.max = 20, plot = FALSE)$acf[-1]
banda <- 1.96 / sqrt(length(residuals(f011)))
cat("ACF resid IMA 1..20:\n"); print(round(a, 4)); cat("banda", banda, " fuera en:", which(abs(a) > banda), "\n")
cat("banda con n-1 =", 1.96 / sqrt(n - 1), "\n")
f111 <- arima(y, order = c(1, 1, 1), method = "ML")
print(c(coef(f111), se = sqrt(diag(f111$var.coef))), digits = 7)
cat("Shapiro", shapiro.test(residuals(f111))$p.value, " LB20", Box.test(residuals(f111), 20, "Ljung-Box", fitdf = 2)$p.value, "\n")
cat("auto.arima exhaustiva:", as.character(auto.arima(y, stepwise = FALSE, approximation = FALSE)),
    " | por defecto:", as.character(auto.arima(y)), "\n")
f122 <- arima(y, order = c(1, 2, 2), method = "ML")
print(coef(f122), digits = 7)
cat("1 + ma1 + ma2 =", 1 + sum(coef(f122)[c("ma1", "ma2")]), "  raices MA:", Mod(polyroot(c(1, coef(f122)[c("ma1", "ma2")]))), "\n")
# division por (1 - B): (1 + a B + b B^2) = (1 - B)(1 - c B) => c = -b ; a = -(1 + c)
cat("factor restante (1 - cB): c =", -coef(f122)[["ma2"]], " comprobacion -(1+c) =", -(1 - coef(f122)[["ma2"]]), "vs ma1", coef(f122)[["ma1"]], "\n")
cat("AICc IMA (d=1) - AICc (1,2,2) =", mi_aicc(f011, n - 1) - mi_aicc(f122, n - 2), "\n")
cat("AICc (1,1,1) - AICc(1,2,2) =", mi_aicc(f111, n - 1) - mi_aicc(f122, n - 2), "\n")

## ------------------------------------------------------------------ E2
sec("E2 pelt$Hare (ayuda)")
rd <- tools::Rd_db("tsibbledata")[["pelt.Rd"]]
tools::Rd2txt(rd, options = list(underline_titles = FALSE))
sec("E2 calculos")
x <- ts(log(pelt$Hare), start = min(pelt$Year)); n2 <- length(x)
cat("anios", range(pelt$Year), " n =", n2, " min Hare", min(pelt$Hare), "\n")
print(c(kpss = ndiffs(x, test = "kpss"), adf = ndiffs(x, test = "adf"), pp = ndiffs(x, test = "pp")))
print(c(kpss_p = suppressWarnings(kpss.test(x)$p.value), adf_p = suppressWarnings(adf.test(x)$p.value),
        pp_p = suppressWarnings(pp.test(x)$p.value)))
v <- c(var(x), var(diff(x)), var(diff(x, differences = 2))); print(v)
cat("caida 1 - v1/v0 =", 1 - v[2] / v[1], "\n")
r1 <- acf(x, plot = FALSE)$acf[2]
cat("r1", r1, " cociente", v[2] / v[1], " 2(1-r1)", 2 * (1 - r1), " r1 dif", acf(diff(x), plot = FALSE)$acf[2], "\n")
for (o in list(c(0, 1, 1), c(1, 1, 1), c(2, 1, 1), c(3, 1, 1))) {
  g <- arima(x, order = o, method = "ML")
  cat(sprintf("ARIMA(%d,1,%d) theta=%8.5f |raizMA|=%8.4f AICc=%.3f LB20 p=%.4f  ARroots=%s\n", o[1], o[3], coef(g)[["ma1"]],
              min_raiz(coef(g)[["ma1"]]), mi_aicc(g, n2 - 1),
              Box.test(residuals(g), 20, "Ljung-Box", fitdf = o[1] + 1)$p.value,
              if (o[1] > 0) paste(round(Mod(polyroot(c(1, -coef(g)[1:o[1]]))), 4), collapse = ",") else "-"))
}
for (p in c(2, 3, 4)) {
  g <- arima(x, order = c(p, 0, 0), method = "ML")
  r <- polyroot(c(1, -coef(g)[1:p]))
  cat(sprintf("AR(%d) AICc=%.3f LB20 p=%.4f min|raiz|=%.4f  periodo(raiz compleja)=%s\n", p, mi_aicc(g, n2),
              Box.test(residuals(g), 20, "Ljung-Box", fitdf = p)$p.value, min(Mod(r)),
              paste(round(2 * pi / abs(Arg(r[abs(Im(r)) > 1e-8])), 2), collapse = ",")))
}
cat("auto.arima exhaustiva:", as.character(auto.arima(x, stepwise = FALSE, approximation = FALSE)),
    " | por defecto:", as.character(auto.arima(x)), "\n")
# ¿los ciclos de la liebre tienen longitud fija? distancia entre maximos locales
pk <- which(diff(sign(diff(as.numeric(x)))) == -2) + 1
cat("maximos locales (anios):", pelt$Year[pk], "\n  separaciones:", diff(pelt$Year[pk]), "\n")
sec("E2 lynx (parrafo de la solucion)")
ly <- log(lynx)
print(c(kpss = ndiffs(ly, test = "kpss"), adf = ndiffs(ly, test = "adf"), pp = ndiffs(ly, test = "pp")))
cat("var", var(ly), var(diff(ly)), " caida", 1 - var(diff(ly)) / var(ly), " r1", acf(ly, plot = FALSE)$acf[2],
    " cociente", var(diff(ly)) / var(ly), " 2(1-r1)", 2 * (1 - acf(ly, plot = FALSE)$acf[2]),
    " r1dif", acf(diff(ly), plot = FALSE)$acf[2], "\n")
g <- arima(ly, order = c(2, 1, 1), method = "ML"); cat("lynx (2,1,1) theta", coef(g)[["ma1"]], "\n")

## ------------------------------------------------------------------ E3
sec("E3 BJsales ARIMA(1,1,1) con Arima()")
f <- Arima(BJsales, order = c(1, 1, 1)); ph <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]; s <- sqrt(f$sigma2)
print(c(phi = ph, theta = th, sigma = s, limite = (1 + th) / (1 - ph), phi_mas_theta = ph + th), digits = 7)
j <- 0:12
psi_cerrada <- ((1 + th) - (ph + th) * ph^j) / (1 - ph)
psi_exp <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = 12))
cat("max |psi cerrada - expandida| =", max(abs(psi_cerrada - psi_exp)), "\n"); print(round(psi_exp, 4))
sh <- s * sqrt(cumsum(psi_exp^2))[1:12]
fc <- forecast(f, h = 12, level = 95)
cat("max dif semiancho:", max(abs((fc$upper - fc$lower) / 2 - qnorm(0.975) * sh)), "\n")
cat("sigma12/sigma1", sh[12] / sh[1], " sqrt12", sqrt(12), " cociente", sh[12] / (s * sqrt(12)), " psi12", psi_exp[13], "\n")
fd <- Arima(BJsales, order = c(1, 1, 1), include.drift = TRUE)
print(c(drift = coef(fd)[["drift"]], se = sqrt(diag(fd$var.coef))[["drift"]],
        t = coef(fd)[["drift"]] / sqrt(diag(fd$var.coef))[["drift"]], aicc_con = fd$aicc, aicc_sin = f$aicc,
        dif = fd$aicc - f$aicc, h12_con = forecast(fd, h = 12)$mean[12], h12_sin = forecast(f, h = 12)$mean[12]), digits = 7)
cat("Nilo psi_inf:", { g <- Arima(Nile, order = c(1, 1, 1)); (1 + coef(g)[["ma1"]]) / (1 - coef(g)[["ar1"]]) }, "\n")

## ------------------------------------------------------------------ P1
sec("P1 aus_airpassengers")
ap <- ts(fpp3::aus_airpassengers$Passengers, start = min(fpp3::aus_airpassengers$Year))
cat("anios", range(fpp3::aus_airpassengers$Year), " n =", length(ap), "\n")
print(c(kpss = ndiffs(ap, test = "kpss"), adf = ndiffs(ap, test = "adf"), pp = ndiffs(ap, test = "pp")))
for (variante in c("sin constante", "con deriva (d=1)")) {
  for (d in 1:2) {
    res <- sapply(0:2, function(p) sapply(0:2, function(q) {
      if (variante == "con deriva (d=1)" && d == 1) {
        g <- try(Arima(ap, order = c(p, d, q), include.drift = TRUE, method = "ML"), silent = TRUE)
      } else g <- try(Arima(ap, order = c(p, d, q), method = "ML"), silent = TRUE)
      if (inherits(g, "try-error")) NA else g$aicc }))
    cat(variante, " d =", d, " min AICc =", round(min(res, na.rm = TRUE), 3), " en (p,q) =",
        paste(which(res == min(res, na.rm = TRUE), arr.ind = TRUE)[1, 2:1] - 1, collapse = ","), "\n")
  }
}
cat("auto.arima:", as.character(auto.arima(ap, stepwise = FALSE, approximation = FALSE)), "\n")

## ------------------------------------------------------------------ P2
sec("P2 ARIMA(1,1,0) phi = 0.5 sigma = 2")
ps <- c(1, ARMAtoMA(ar = c(1.5, -0.5), lag.max = 3)); print(ps)
exacto <- 2 * sqrt(sum(ps[1:3]^2)); cat("sigma3 exacto", exacto, "\n")
cat("variantes de redondeo:\n")
cat("  3.0625->3.063, suma 6.313, sqrt 2.5126 -> 2*", 2 * sqrt(6.313), "\n")
cat("  sqrt(6.3125) a 3 dec 2.512 -> ", 2 * 2.512, "; a 2 dec 2.51 ->", 2 * 2.51, "\n")
cat("  suma 6.313 y sqrt a 3 dec:", 2 * round(sqrt(6.313), 3), "\n")
cat("  1.75^2 -> 3.06 (2 dec): ", 2 * sqrt(1 + 2.25 + 3.06), "\n")
cat("distractores: phi^j", 2 * sqrt(1 + 0.25 + 0.0625), " caminata", 2 * sqrt(3), " sin psi0", 2 * sqrt(2.25 + 3.0625),
    " sin cuadrado", 2 * sqrt(1 + 1.5 + 1.75), " psi3 de mas", 2 * sqrt(sum(ps^2)), " sin sigma", sqrt(6.3125), "\n")
cat("  sin cuadrado y sin raiz 2*(1+1.5+1.75) =", 2 * 4.25, "\n")

## ------------------------------------------------------------------ P4
sec("P4 constante")
g <- Arima(Nile, order = c(1, 1, 1)); print(round(forecast(g, h = 30)$mean[c(1, 30)], 2))
w <- tryCatch(Arima(BJsales, order = c(0, 2, 1), include.drift = TRUE), warning = function(w) conditionMessage(w)); print(w)
g0 <- arima(Nile, order = c(1, 0, 1)); cat("intercept", coef(g0)[["intercept"]], " mean(Nile)", mean(Nile), "\n")

## ------------------------------------------------------------------ P5
sec("P5 beaver2 (ayuda)")
tools::Rd2txt(tools::Rd_db("datasets")[["beavers.Rd"]], options = list(underline_titles = FALSE))
sec("P5 calculos")
b <- ts(beaver2$temp); act <- beaver2$activ
cat("n =", length(b), " primera lectura con activ = 1:", which(act == 1)[1], " todas desde ahi:", all(act[which(act == 1)[1]:100] == 1), "\n")
cat("dif. de medias:", mean(b[act == 1]) - mean(b[act == 0]), "\n")
cat("intervalo entre lecturas (time):", head(beaver2$time), "\n")
print(c(kpss_p = suppressWarnings(kpss.test(b)$p.value), adf_p = adf.test(b)$p.value, pp_p = suppressWarnings(pp.test(b)$p.value)))
print(c(kpss = ndiffs(b, test = "kpss"), adf = ndiffs(b, test = "adf"), pp = ndiffs(b, test = "pp")))
e <- residuals(lm(as.numeric(b) ~ act))
cat("escalon OLS", coef(lm(as.numeric(b) ~ act))[2], " KPSS resid p", suppressWarnings(kpss.test(e)$p.value),
    " r1 resid", acf(e, plot = FALSE)$acf[2], "\n")
g <- arima(b, order = c(1, 0, 0), xreg = act, method = "ML")
cat("AR(1)+escalon:", coef(g), " LB10", Box.test(residuals(g), 10, "Ljung-Box", fitdf = 1)$p.value, "\n")
print(c(adf_resid = adf.test(e)$p.value, pp_resid = suppressWarnings(pp.test(e)$p.value),
        ndiffs_kpss_resid = ndiffs(e, test = "kpss"), ndiffs_adf_resid = ndiffs(e, test = "adf")))

## ------------------------------------------------------------------ P6, P7
sec("P6/P7 Chile, exportaciones % PIB")
ch <- tsibbledata::global_economy %>% filter(Country == "Chile") %>% arrange(Year)
ex <- ts(ch$Exports, start = min(ch$Year)); cat("anios", range(ch$Year), " n =", length(ex), " NA:", sum(is.na(ex)), "\n")
a6 <- acf(ex, lag.max = 20, plot = FALSE)$acf[-1]; print(round(a6, 3))
cat("banda", 1.96 / sqrt(length(ex)), " ultimo rezago fuera:", max(which(abs(a6) > 1.96 / sqrt(length(ex)))),
    " todos fuera hasta:", min(which(abs(a6) <= 1.96 / sqrt(length(ex)))) - 1, "\n")
ad <- acf(diff(ex), lag.max = 20, plot = FALSE)$acf[-1]
cat("ACF diff:", round(ad, 3), "\n banda", 1.96 / sqrt(length(ex) - 1), " fuera:", which(abs(ad) > 1.96 / sqrt(length(ex) - 1)), "\n")
print(c(kpss = ndiffs(ex, test = "kpss"), adf = ndiffs(ex, test = "adf"), pp = ndiffs(ex, test = "pp")))
esc <- auto.arima(ex); exh <- auto.arima(ex, stepwise = FALSE, approximation = FALSE)
cat("escalonada:", as.character(esc), esc$aicc, " | exhaustiva:", as.character(exh), exh$aicc, "\n")
tr <- capture.output(auto.arima(ex, stepwise = FALSE, approximation = FALSE, trace = TRUE))
lin <- grep(":", tr, value = TRUE); lin <- lin[!grepl("Best", lin)]
val <- suppressWarnings(as.numeric(sub(".*:\\s*", "", lin)))
cat("modelos en la traza exhaustiva:", length(lin), " finitos:", sum(is.finite(val)), "\n")
o <- order(val); print(data.frame(modelo = trimws(sub(":.*", "", lin[o[1:6]])), aicc = val[o[1:6]], delta = val[o[1:6]] - val[o[1]]))
tr2 <- capture.output(auto.arima(ex, trace = TRUE)); cat("modelos en la escalonada:", length(grep(":", tr2)) - 1, "\n")

## ------------------------------------------------------------------ P8
sec("P8 Peru, importaciones % PIB")
pe <- tsibbledata::global_economy %>% filter(Country == "Peru") %>% arrange(Year)
im <- ts(pe$Imports, start = min(pe$Year)); cat("anios", range(pe$Year), " n =", length(im), " NA:", sum(is.na(im)), "\n")
for (d in 1:2) {
  z <- diff(im, differences = d)
  g <- arima(z, order = c(0, 0, 1), method = "ML")
  cat(sprintf("d=%d theta=%.4f sigma2=%.4f var=%.4f LB10(fitdf=1) p=%.4f LB10(fitdf=0) p=%.4f n=%d\n", d, coef(g)[["ma1"]],
              g$sigma2, var(z), Box.test(residuals(g), 10, "Ljung-Box", fitdf = 1)$p.value,
              Box.test(residuals(g), 10, "Ljung-Box", fitdf = 0)$p.value, length(z)))
  g2 <- arima(im, order = c(0, d, 1), method = "ML")
  cat(sprintf("    (como ARIMA(0,%d,1) sin media) theta=%.4f sigma2=%.4f\n", d, coef(g2)[["ma1"]], g2$sigma2))
}
print(c(kpss = ndiffs(im, test = "kpss"), adf = ndiffs(im, test = "adf"), pp = ndiffs(im, test = "pp")))
