# Diagnóstico cap. 5 · series ESTACIONALES candidatas para la práctica de los módulos
# que no la tienen, medidas en R 4.6. Ninguna está en las listas de práctica de los caps.
# 2-4 ni en Htmls_Series (ver ejercicios_series_grep.out); se excluyen además nottem,
# mdeaths, fdeaths y ldeaths (práctica del cap. 1) y la columna Gas de aus_production
# (quiz del cap. 1), y las cuatro series del propio capítulo 5.
#
#   LC_ALL=en_US.UTF-8 Rscript diagnostico/cap5/diag/ejercicios_series_candidatas.R > diagnostico/cap5/diag/ejercicios_series_candidatas.out 2>&1
#
# Qué se mide, por serie mensual (y para qué módulo sirve):
#   mult   cor(media anual, desviación anual) en la escala cruda: > 0.5 pide log (M1, M7)
#   ndiffs crudo / nsdiffs (seas, ocsb) / ndiffs tras ∇12: la trampa del orden (M3, M8)
#   ACF de ∇y en 12, 24, 36 frente a la banda: la firma (M1, M8)
#   airline: θ, Θ, LB(24), |raíz MA estacional| (M5, M6); con D = 2: Θ y |raíz| (M3)
#   auto.arima: órdenes (M4: ¿SAR o SMA?) y LB(24)
#   trampa del M6: mejor modelo con D = 0 frente al airline: AICc, n, LB
#   calendario (M9): β de log(días) y de Pascua con errores airline: t contra 0 y contra 1
#   no estacional (M8): SAR(1) forzado sobre (0,1,0): Φ, t; AICc frente al simple
suppressPackageStartupMessages({ library(forecast); library(fpp3); library(tseries) })
options(width = 160, warn = -1)
set.seed(2026)
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")), "| fpp3", as.character(packageVersion("fpp3")), "\n")
a_ts <- function(tb, col) { idx <- as.Date(tb[[index_var(tb)]]); o <- order(idx)
  y <- tb[[col]][o]; idx <- idx[o]; ts(y, start = c(as.numeric(format(idx[1], "%Y")), as.numeric(format(idx[1], "%m"))), frequency = 12) }
pascua <- function(a) {
  b <- a %/% 100; c <- a %% 100; d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3
  h <- (19 * (a %% 19) + b - d - g + 15) %% 30; i <- c %/% 4; k <- c %% 4
  l <- (32 + 2 * e + 2 * i - h - k) %% 7; m <- ((a %% 19) + 11 * h + 22 * l) %/% 451
  as.Date(sprintf("%d-%02d-%02d", a, (h + l - 7 * m + 114) %/% 31, ((h + l - 7 * m + 114) %% 31) + 1))
}
cal <- function(y) {
  t0 <- start(y); f <- seq(as.Date(sprintf("%d-%02d-01", t0[1], t0[2])), by = "month", length.out = length(y) + 1)
  dias <- as.numeric(diff(f)); f <- f[-length(f)]
  pm <- as.numeric(as.numeric(format(f, "%m")) == as.numeric(format(pascua(as.numeric(format(f, "%Y"))), "%m")))
  cbind(log_dias = log(dias), pascua = pm)
}
raizMA <- function(fit) { th <- fit$model$theta; if (!length(th) || all(th == 0)) return(NA)
  round(min(Mod(polyroot(c(1, th)))), 4) }
lb <- function(fit, lag = 24) round(Box.test(residuals(fit), lag = lag, type = "Ljung-Box", fitdf = sum(fit$arma[1:4]))$p.value, 4)
seguro <- function(expr) tryCatch(expr, error = function(e) NULL)

S <- list(
  wineind = wineind,
  gas = gas,
  souvenirs = a_ts(souvenirs, "Sales"),
  canadian_gas = a_ts(canadian_gas, "Volume"),
  seatbelts_kms = Seatbelts[, "kms"],
  us_retail_empleo = window(a_ts(filter(us_employment, Title == "Retail Trade"), "Employed"), start = c(2000, 1)),
  vic_cafes = a_ts(filter(aus_retail, State == "Victoria", Industry == "Cafes, restaurants and takeaway food services"), "Turnover"),
  vic_cerdos = a_ts(filter(aus_livestock, State == "Victoria", Animal == "Pigs"), "Count"),
  nsw_nacimientos = a_ts(filter(aus_births, State == "NSW"), "Births"),
  ny_childcare = a_ts(ny_childcare, "Count"),
  petrolprice = Seatbelts[, "PetrolPrice"],
  sunspot_month = window(sunspot.month, start = c(1950, 1), end = c(2013, 12))
)
cat("\n### 1. Diferencias, firma y transformación\n")
fila <- list()
for (nm in names(S)) {
  y0 <- S[[nm]]; n <- length(y0)
  an <- tapply(as.numeric(y0), floor(time(y0) + 1e-6), function(z) c(mean(z), sd(z)))
  an <- do.call(rbind, an[sapply(an, function(z) all(is.finite(z)))])
  mult <- round(cor(an[, 1], an[, 2]), 3)
  usa_log <- mult > 0.5 && all(y0 > 0)
  y <- if (usa_log) log(y0) else y0
  a <- Acf(diff(y), lag.max = 36, plot = FALSE)$acf; banda <- 1.96 / sqrt(n - 1)
  fila[[nm]] <- data.frame(serie = nm, n = n, inicio = paste(start(y0), collapse = "-"), mult = mult, log = usa_log,
    nd = ndiffs(y), nsd = nsdiffs(y), nsd_ocsb = nsdiffs(y, test = "ocsb"), nd_trasD = ndiffs(diff(y, lag = 12)),
    r12 = round(a[13], 3), r24 = round(a[25], 3), r36 = round(a[37], 3), banda = round(banda, 3))
  S[[nm]] <- y
}
T1 <- do.call(rbind, fila); print(T1, row.names = FALSE)
cat("trampa del orden (ndiffs crudo = 0 y tras ∇12 = 1):", T1$serie[T1$nd == 0 & T1$nd_trasD == 1], "\n")
cat("sin firma estacional (nsdiffs 0 con las dos pruebas y |r12|,|r24|,|r36| < banda):",
    T1$serie[T1$nsd == 0 & T1$nsd_ocsb == 0 & abs(T1$r12) < T1$banda & abs(T1$r24) < T1$banda & abs(T1$r36) < T1$banda], "\n")

cat("\n### 2. Airline, D = 2, auto.arima y la trampa del AICc entre D (series estacionales)\n")
est <- setdiff(names(S), c("petrolprice", "sunspot_month"))
fila <- list()
for (nm in est) {
  y <- S[[nm]]
  air <- seguro(Arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)))
  d2 <- seguro(Arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 2, 1), period = 12)))
  aa <- auto.arima(y)
  d0 <- auto.arima(y, D = 0)
  fila[[nm]] <- data.frame(serie = nm,
    th = round(coef(air)["ma1"], 3), Th = round(coef(air)["sma1"], 3), lb_air = lb(air), aicc_air = round(air$aicc, 2), n_air = air$nobs,
    Th_D2 = if (is.null(d2)) NA else round(coef(d2)["sma1"], 3), raiz_D2 = if (is.null(d2)) NA else raizMA(d2),
    auto = sub("ARIMA", "", as.character(aa)), lb_auto = lb(aa),
    D0 = sub("ARIMA", "", as.character(d0)), aicc_D0 = round(d0$aicc, 2), n_D0 = d0$nobs, lb_D0 = lb(d0))
}
T2 <- do.call(rbind, fila); print(T2, row.names = FALSE)
cat("la trampa muerde (el mejor con D = 0 tiene menor AICc que el airline):", T2$serie[T2$aicc_D0 < T2$aicc_air], "\n")
cat("  ...y además ese D = 0 no pasa LB(24) al 5 %:", T2$serie[T2$aicc_D0 < T2$aicc_air & T2$lb_D0 < 0.05], "\n")
cat("auto.arima con parte SAR y sin SMA (para el M4):", T2$serie[grepl("\\([1-9],[0-9],0\\)\\[12\\]", T2$auto)], "\n")
cat("auto.arima con SMA y sin SAR:", T2$serie[grepl("\\(0,[0-9],[1-9]\\)\\[12\\]", T2$auto)], "\n")
cat("airline que pasa LB(24) al 5 %:", T2$serie[T2$lb_air >= 0.05], "\n")

cat("\n### 3. M5: escalón de σ_h del airline (σ13/σ12) y ψ12, en las que pasan LB\n")
for (nm in T2$serie[T2$lb_air >= 0.05]) {
  y <- S[[nm]]; air <- Arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
  th <- coef(air)["ma1"]; Th <- coef(air)["sma1"]
  psi <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = c(th, rep(0, 10), Th, th * Th), lag.max = 24))
  sg <- sqrt(air$sigma2 * cumsum(psi^2))
  cat(sprintf("  %-16s θ=%.3f Θ=%.3f ψ1=%.4f ψ12=%.4f σ1=%.4f σ12=%.4f σ13=%.4f σ13/σ12=%.4f σ12/σ11=%.4f\n",
              nm, th, Th, psi[2], psi[13], sg[1], sg[12], sg[13], sg[13] / sg[12], sg[12] / sg[11]))
}

cat("\n### 4. M9: calendario con errores airline (log(días) y Pascua)\n")
for (nm in est) {
  y <- S[[nm]]; X <- cal(y)
  f <- seguro(Arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), xreg = X))
  if (is.null(f)) { cat("  ", nm, ": no converge\n"); next }
  b <- coef(f)[c("log_dias", "pascua")]; s <- sqrt(diag(f$var.coef))[c("log_dias", "pascua")]
  base <- Arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
  cat(sprintf("  %-16s log %-5s β_días=%7.4f (ee %.4f, t0=%6.2f, t1=%6.2f) β_pascua=%7.4f (t=%6.2f) ΔAICc=%7.2f\n",
              nm, T1$log[T1$serie == nm], b[1], s[1], b[1] / s[1], (b[1] - 1) / s[1], b[2], b[2] / s[2], f$aicc - base$aicc))
}

cat("\n### 5. M8: series mensuales sin estacionalidad, SAR(1) forzado\n")
for (nm in c("petrolprice", "sunspot_month")) {
  y <- S[[nm]]
  g <- Arima(y, order = c(0, 1, 0), seasonal = list(order = c(1, 0, 0), period = 12))
  h <- Arima(y, order = c(0, 1, 0))
  an <- Acf(y, lag.max = 36, plot = FALSE)$acf
  cat(sprintf("  %-14s n=%d  ρ12 en niveles=%.3f  Φ=%.4f (ee %.4f, t=%.2f)  AICc forzado %.2f vs simple %.2f  auto.arima %s\n",
              nm, length(y), an[13], coef(g)[1], sqrt(g$var.coef[1, 1]), coef(g)[1] / sqrt(g$var.coef[1, 1]), g$aicc, h$aicc,
              as.character(auto.arima(y))))
}

cat("\n### 6. M10: m grande (semanal, diario, semihorario)\n")
gs <- ts(us_gasoline$Barrels, frequency = 365.25 / 7)
cat("us_gasoline: n =", length(gs), " frecuencia =", round(frequency(gs), 2), "\n")
t0 <- Sys.time()
fg <- lapply(1:12, function(K) { f <- auto.arima(gs, xreg = fourier(gs, K = K), seasonal = FALSE)
  c(K = K, aicc = round(f$aicc, 2), n = f$nobs, lb104 = lb(f, 104)) })
print(do.call(rbind, fg))
cat("  tiempo Fourier K = 1..12:", round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1), "s\n")
gs52 <- ts(us_gasoline$Barrels, frequency = 52)
t0 <- Sys.time()
s52 <- seguro(Arima(gs52, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 52)))
cat("  SARIMA(0,1,1)(0,1,1)[52]:", if (is.null(s52)) "no se ajusta" else sprintf("AICc %.2f, n %d, LB(104) %.4f", s52$aicc, s52$nobs, lb(s52, 104)),
    "| tiempo", round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1), "s\n")
data(ice.river, package = "tseries"); fl <- ts(ice.river[, "flow.jok"], frequency = 365)
fl <- log(fl)
cat("ice.river flow.jok (log): n =", length(fl), "\n")
fr <- lapply(1:5, function(K) { f <- auto.arima(fl, xreg = fourier(fl, K = K), seasonal = FALSE)
  c(K = K, aicc = round(f$aicc, 2), n = f$nobs, lb = lb(f, 30)) })
print(do.call(rbind, fr))
ty <- taylor
cat("taylor: n =", length(ty), " periodos", paste(attr(ty, "msts"), collapse = ", "), "\n")
t0 <- Sys.time()
for (KK in list(c(5, 5), c(10, 10))) {
  f <- Arima(ty, order = c(2, 0, 1), xreg = fourier(ty, K = KK), include.mean = TRUE, method = "CSS")
  cat(sprintf("  Fourier K = (%d, %d): %d términos; sd residual %.1f\n", KK[1], KK[2], ncol(fourier(ty, K = KK)), sd(residuals(f))))
}
cat("  tiempo:", round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1), "s; parámetros de un SARIMA(1,0,1)(1,1,1)[336] con D = 1 consumen 336 datos de", length(ty), "\n")

cat("\n### 7. M11: una partición frente a origen móvil (h = 12), tres métodos\n")
om <- function(nm, y, desde) {
  n <- length(y); te <- n - 24
  ent <- window(y, end = time(y)[te]); ob <- exp(as.numeric(window(y, start = time(y)[te + 1])))
  m <- list(snaive = function(e, h) exp(as.numeric(snaive(e, h = h)$mean)),
            airline = function(e, h) exp(as.numeric(forecast(Arima(e, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)), h = h)$mean)),
            ets = function(e, h) exp(as.numeric(forecast(ets(e), h = h)$mean)))
  una <- sapply(m, function(f) sqrt(mean((ob - f(ent, 24))^2)))
  org <- desde:(n - 12)
  E <- sapply(m, function(f) sapply(org, function(o) { e <- window(y, end = time(y)[o])
    obs <- exp(as.numeric(window(y, start = time(y)[o + 1], end = time(y)[o + 12]))); sqrt(mean((obs - f(e, 12))^2)) }))
  cat(sprintf("  %s (log): una partición RMSE %s → gana %s | %d orígenes RMSE medio %s → gana %s\n", nm,
      paste(sprintf("%s %.2f", names(una), una), collapse = ", "), names(which.min(una)), length(org),
      paste(sprintf("%s %.2f", colnames(E), colMeans(E)), collapse = ", "), colnames(E)[which.min(colMeans(E))]))
  cat(sprintf("    %% de orígenes en que gana cada uno: %s\n", paste(sprintf("%s %.1f", colnames(E), 100 * tabulate(apply(E, 1, which.min), 3) / nrow(E)), collapse = ", ")))
}
om("wineind", log(wineind), 96)
om("vic_cafes", if (T1$log[T1$serie == "vic_cafes"]) S$vic_cafes else log(S$vic_cafes), length(S$vic_cafes) - 120)
