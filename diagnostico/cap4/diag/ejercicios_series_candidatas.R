# Diagnóstico cap. 4 · series candidatas para los huecos de práctica
#   Rscript diagnostico/cap4/diag/ejercicios_series_candidatas.R > diagnostico/cap4/diag/ejercicios_series_candidatas.out 2>&1
# Ninguna está en la práctica de los caps. 2-3 ni aparece en Htmls_Series (grep
# en el informe). Para cada hueco se mide lo que la tarea necesitaría que pasara.
suppressPackageStartupMessages({ library(forecast); library(tseries); library(tsibble); library(tsibbledata); library(fpp3) })
options(width = 120, warn = -1)
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
data(NelPlo, package = "tseries"); data(tcm, package = "tseries")
pr <- function(...) print(round(c(...), 4))

cand <- list(
  beaver2_temp   = ts(beaver2$temp),
  austres        = austres,
  log_airmiles   = log(airmiles),
  uspop          = uspop,
  BJsales.lead   = BJsales.lead,
  gnp_real       = na.omit(NelPlo[, "gnp.real"]),     # NelPlo ya viene en logaritmos (rango 4.76-7.09)
  ip             = na.omit(NelPlo[, "ip"]),
  tcm1y          = tcm1y,
  stock_prices   = na.omit(NelPlo[, "stock.prices"]),
  goog_close     = ts(dplyr::filter(gafa_stock, Symbol == "GOOG")$Close),
  aus_air        = ts(aus_airpassengers$Passengers, start = 1970),
  log_us_gdp     = ts(log(dplyr::filter(global_economy, Country == "United States")$GDP), start = 1960)
)

cat("===== Panorama: n, ndiffs (kpss/adf/pp), var por d, auto.arima escalonado y exhaustivo =====\n")
for (nm in names(cand)) {
  y <- cand[[nm]]
  v <- sapply(0:2, function(d) var(if (d == 0) y else diff(y, differences = d)))
  a1 <- tryCatch(auto.arima(y, seasonal = FALSE), error = function(e) "falla")
  a2 <- tryCatch(auto.arima(y, seasonal = FALSE, stepwise = FALSE, approximation = FALSE), error = function(e) "falla")
  cat(sprintf("%-14s n=%4d nd=%d/%d/%d var=%s  esc=%-28s exh=%-28s\n", nm, length(y),
              ndiffs(y, test = "kpss"), ndiffs(y, test = "adf"), ndiffs(y, test = "pp"),
              paste(signif(v, 4), collapse = "/"), if (is.character(a1)) a1 else as.character(a1), if (is.character(a2)) a2 else as.character(a2)))
}

cat("\n===== M1 · raíz unitaria estimada frente a impuesta: AR(2) en niveles y ARIMA(1,1,0) =====\n")
for (nm in c("austres", "gnp_real", "ip", "tcm1y", "BJsales.lead", "log_us_gdp")) {
  y <- cand[[nm]]
  f2 <- tryCatch(arima(y, order = c(2, 0, 0), method = "ML"), error = function(e) NULL)
  if (is.null(f2)) { cat(nm, ": AR(2) no converge\n"); next }
  f110 <- arima(y, order = c(1, 1, 0), method = "ML")
  cat(sprintf("%-14s phi* = (%.4f, %.4f) suma = %.4f |raíces| = %s ; ARIMA(1,1,0) phi = %.4f (−phi2* = %.4f)\n",
              nm, coef(f2)[1], coef(f2)[2], sum(coef(f2)[1:2]),
              paste(sprintf("%.4f", Mod(polyroot(c(1, -coef(f2)[1:2])))), collapse = ", "),
              coef(f110)[1], -coef(f2)[2]))
}
cat("\nM1 · IMA(1,1) frente a SES: alfa = 1 + theta\n")
for (nm in c("BJsales.lead", "tcm1y", "goog_close")) {
  y <- cand[[nm]]; f <- Arima(y, order = c(0, 1, 1)); s <- ses(y, h = 1)
  cat(sprintf("%-14s theta = %.4f  1 + theta = %.4f  alfa(ses) = %.4f  pron ARIMA = %.3f  pron SES = %.3f\n", nm,
              coef(f)[1], 1 + coef(f)[1], s$model$par[["alpha"]], forecast(f, h = 1)$mean[1], s$mean[1]))
}

cat("\n===== M8 / M3 · escalón frente a raíz unitaria: beaver2 (la actividad empieza en la obs. 39) =====\n")
y <- cand$beaver2_temp; act <- beaver2$activ
cat("primer índice con activ = 1:", which(act == 1)[1], " n =", length(y), "\n")
pr(kpss_p = kpss.test(y)$p.value, adf_p = adf.test(y)$p.value, pp_p = pp.test(y)$p.value,
   ndiffs = ndiffs(y), var_d0 = var(y), var_d1 = var(diff(y)), var_d2 = var(diff(y, differences = 2)))
fa <- auto.arima(y); cat("auto.arima:", as.character(fa), " |raíz MA| mín:",
  { ma <- coef(fa)[grepl("^ma", names(coef(fa)))]; if (length(ma)) round(min(Mod(polyroot(c(1, ma)))), 4) else NA }, "\n")
fe <- Arima(y, order = c(1, 0, 0), xreg = act)
pr(beta = coef(fe)[["xreg"]], ee = sqrt(diag(fe$var.coef))[["xreg"]], phi = coef(fe)[["ar1"]],
   lb10 = Box.test(residuals(fe), lag = 10, type = "Ljung-Box", fitdf = 1)$p.value)
set.seed(2026)
esc <- act; s0 <- sd(residuals(fe))
cat("KPSS sobre AR(1) phi estimado + escalón del tamaño estimado, 400 réplicas: tasa de rechazo =",
    mean(replicate(400, { x <- arima.sim(list(ar = coef(fe)[["ar1"]]), n = 100, sd = s0) + coef(fe)[["xreg"]]*esc
                          kpss.test(x)$p.value <= 0.05 })), "\n")

cat("\n===== M7 · auto.arima: modelos a menos de 2 de AICc en la búsqueda exhaustiva =====\n")
for (nm in c("austres", "BJsales.lead", "log_us_gdp", "aus_air", "tcm1y")) {
  y <- cand[[nm]]
  tr <- capture.output(invisible(auto.arima(y, trace = TRUE, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)))
  tr <- grep("^ ARIMA.*:", tr, value = TRUE); v <- suppressWarnings(as.numeric(sub(".*:\\s*", "", tr)))
  te <- capture.output(invisible(auto.arima(y, trace = TRUE, seasonal = FALSE)))
  te <- grep("^ ARIMA.*:", te, value = TRUE)
  cat(sprintf("%-14s escalonada evalúa %2d, exhaustiva %2d; a < 2 del mejor: %d (%s)\n", nm, length(te), length(tr),
              sum(v - min(v, na.rm = TRUE) < 2, na.rm = TRUE),
              paste(trimws(sub(":.*", "", tr[order(v)][1:min(4, sum(v - min(v, na.rm = TRUE) < 2, na.rm = TRUE))])), collapse = " | ")))
}

cat("\n===== M5 · ¿lleva deriva? t de la deriva y AICc con y sin =====\n")
for (nm in c("austres", "log_airmiles", "log_us_gdp", "aus_air", "BJsales.lead", "goog_close")) {
  y <- cand[[nm]]; o <- arimaorder(auto.arima(y, seasonal = FALSE)); o[2] <- 1
  f1 <- tryCatch(Arima(y, order = o, include.drift = TRUE), error = function(e) NULL)
  f0 <- tryCatch(Arima(y, order = o), error = function(e) NULL)
  if (is.null(f1) || is.null(f0)) { cat(nm, ": no ajusta\n"); next }
  cat(sprintf("%-14s ARIMA(%d,1,%d)  deriva = %.4g  t = %.2f  AICc con = %.2f  sin = %.2f  (y_n - y_1)/(n-1) = %.4g\n",
              nm, o[1], o[3], coef(f1)[["drift"]], coef(f1)[["drift"]]/sqrt(diag(f1$var.coef))[["drift"]],
              f1$aicc, f0$aicc, (tail(y, 1) - y[1])/(length(y) - 1)))
}

cat("\n===== M10 · ¿queda algo que modelar? caminatas candidatas =====\n")
for (nm in c("goog_close", "stock_prices", "tcm1y")) {
  y <- cand[[nm]]; dy <- diff(y); a <- auto.arima(y, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  r <- acf(dy, lag.max = 20, plot = FALSE)$acf[-1]
  cat(sprintf("%-14s n=%4d auto=%-26s r1=%.3f fuera=%d de 20 (banda %.3f) LB20 p=%.4f Shapiro p=%.2g curtosis=%.1f\n",
              nm, length(y), as.character(a), r[1], sum(abs(r) > 1.96/sqrt(length(dy))), 1.96/sqrt(length(dy)),
              Box.test(dy, lag = 20, type = "Ljung-Box")$p.value, shapiro.test(dy[1:min(5000, length(dy))])$p.value,
              mean(((dy - mean(dy))/sd(dy))^4)))
}

cat("\n===== M10 bis · más candidatas a caminata aleatoria =====\n")
extra <- list(
  amzn_close = ts(dplyr::filter(gafa_stock, Symbol == "AMZN")$Close),
  fb_close   = ts(dplyr::filter(gafa_stock, Symbol == "FB")$Close),
  aapl_close = ts(dplyr::filter(gafa_stock, Symbol == "AAPL")$Close),
  goog_2018  = ts(dplyr::filter(gafa_stock, Symbol == "GOOG", lubridate::year(Date) == 2018)$Close),
  tcm10y     = tcm10y,
  int_rate   = na.omit(NelPlo[, "int.rate"]),
  real_wages = na.omit(NelPlo[, "real.wages"]))
for (nm in names(extra)) {
  y <- extra[[nm]]; dy <- diff(y); a <- auto.arima(y, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  r <- acf(dy, lag.max = 20, plot = FALSE)$acf[-1]
  cat(sprintf("%-11s n=%4d nd=%d auto=%-26s r1=%.3f fuera=%d de 20 LB20 p=%.4f Shapiro p=%.2g curtosis=%.1f\n",
              nm, length(y), ndiffs(y), as.character(a), r[1], sum(abs(r) > 1.96/sqrt(length(dy))),
              Box.test(dy, lag = 20, type = "Ljung-Box")$p.value, shapiro.test(dy[1:min(5000, length(dy))])$p.value,
              mean(((dy - mean(dy))/sd(dy))^4)))
}

cat("\n===== M10 ter · fb_close: el ARIMA(1,1,1) que elige auto.arima, ¿cancela raíces? =====\n")
y <- extra$fb_close; f <- Arima(y, order = c(1, 1, 1)); f0 <- Arima(y, order = c(0, 1, 0))
print(round(c(coef(f), raiz_AR = Mod(polyroot(c(1, -coef(f)[1]))), raiz_MA = Mod(polyroot(c(1, coef(f)[2]))),
              aicc_111 = f$aicc, aicc_010 = f0$aicc), 4))
cat("goog_2018: Ljung-Box de las diferencias a 10 y 20, y la barra fuera\n")
dy <- diff(extra$goog_2018); r <- acf(dy, lag.max = 20, plot = FALSE)$acf[-1]
print(round(c(lb10 = Box.test(dy, lag = 10, type = "Ljung-Box")$p.value, lb20 = Box.test(dy, lag = 20, type = "Ljung-Box")$p.value,
              rezago_fuera = which(abs(r) > 1.96/sqrt(length(dy))), valor = r[which(abs(r) > 1.96/sqrt(length(dy)))]), 4))

cat("\n===== Sustituto del E2 (lynx): estacionarias con r1 > 0.5 donde diferenciar BAJA la varianza =====\n")
data(nino, package = "tseries"); data(ice.river, package = "tseries")
e2 <- list(nino3.4 = nino3.4, nino3 = nino3, beaver1_temp = ts(beaver1$temp), flow_vat = ice.river[, "flow.vat"])
for (nm in names(e2)) {
  y <- e2[[nm]]; v <- sapply(0:2, function(d) var(if (d == 0) y else diff(y, differences = d)))
  f <- tryCatch(arima(y, order = c(2, 1, 1), method = "ML"), error = function(e) NULL)
  rm <- if (is.null(f)) NA else min(Mod(polyroot(c(1, coef(f)[["ma1"]]))))
  cat(sprintf("%-12s n=%4d frec=%2d r1=%.3f var d0/d1/d2 = %s (d1/d0 = %.3f; 2(1-r1) = %.3f) nd kpss/adf/pp = %d/%d/%d  ARIMA(2,1,1) |raíz MA| = %.4f\n",
              nm, length(y), frequency(y), acf(y, plot = FALSE)$acf[2], paste(signif(v, 4), collapse = "/"), v[2]/v[1],
              2*(1 - acf(y, plot = FALSE)$acf[2]), ndiffs(y, test = "kpss"), ndiffs(y, test = "adf"), ndiffs(y, test = "pp"), rm))
}
cat("nino3: ¿estacionalidad residual? nsdiffs, ACF en 12 y 24; ¿escalón en beaver1?\n")
print(round(c(nsdiffs = nsdiffs(nino3), r12 = acf(nino3, lag.max = 24, plot = FALSE)$acf[13],
              r24 = acf(nino3, lag.max = 24, plot = FALSE)$acf[25], activ1_beaver1 = sum(beaver1$activ)), 3))
cat("nino3 y nino3.4 desestacionalizados restando la media de cada mes (sin pasar por SARIMA):\n")
for (nm in c("nino3", "nino3.4")) {
  y <- e2[[nm]]; m <- ave(as.numeric(y), cycle(y)); y <- ts(as.numeric(y) - m, start = start(y), frequency = 12)
  v <- sapply(0:2, function(d) var(if (d == 0) y else diff(y, differences = d)))
  f <- arima(y, order = c(2, 1, 1), method = "ML"); r <- acf(y, lag.max = 24, plot = FALSE)$acf
  cat(sprintf("%-8s anomalía: r1=%.3f r12=%.3f var d0/d1/d2 = %s nd kpss/adf/pp = %d/%d/%d nsdiffs = %d ARIMA(2,1,1) |raíz MA| = %.4f\n",
              nm, r[2], r[13], paste(signif(v, 4), collapse = "/"), ndiffs(y, test = "kpss"), ndiffs(y, test = "adf"),
              ndiffs(y, test = "pp"), nsdiffs(y), min(Mod(polyroot(c(1, coef(f)[["ma1"]]))))))
}
cat("nino3.4 anomalía: |raíz MA| mínima de cada ARIMA(p,1,q), y auto.arima con d = 1 forzado\n")
y <- e2[["nino3.4"]]; y <- ts(as.numeric(y) - ave(as.numeric(y), cycle(y)), frequency = 12)
for (p in 1:3) for (q in 1:2) { f <- tryCatch(arima(y, order = c(p, 1, q), method = "ML"), error = function(e) NULL)
  if (!is.null(f)) cat(sprintf("  ARIMA(%d,1,%d) |raíz MA| = %.4f  AICc = %.2f\n", p, q,
    min(Mod(polyroot(c(1, coef(f)[grepl("^ma", names(coef(f)))])))), aicc(f, length(y) - 1))) }
fa <- auto.arima(y, d = 1, seasonal = FALSE); cat("  auto.arima(d = 1):", as.character(fa), "\n")
