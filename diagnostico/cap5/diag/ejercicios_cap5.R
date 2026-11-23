# Diagnóstico cap. 5 · recalcula las soluciones de los tres ejercicios guiados,
# las ocho claves del quiz AUTOEVALUACIONES['cap5'] y las seis claves numéricas
# del simulacro SIMULACROS['cap5-simulacro'], con sondas de tolerancia.
#
#   Rscript diagnostico/cap5/diag/ejercicios_cap5.R > diagnostico/cap5/diag/ejercicios_cap5.out 2>&1
#
# La TRM se lee de precalculo/salidas/datos_series.json (la misma que usa
# genera_cap5.R); co2, USAccDeaths y AirPassengers, de datasets, y se compara
# con el JSON. No se toca nada fuera de diagnostico/cap5/.
suppressPackageStartupMessages({ library(forecast); library(tseries); library(jsonlite) })
options(width = 120, warn = 1)
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")), "\n")
raiz <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])), "../../.."))
sb <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"))
trm <- ts(sb$trm$valores, start = sb$trm$inicio, frequency = 12)
cat("co2 == JSON:", isTRUE(all.equal(as.numeric(co2), sb$co2$valores)),
    "| USAccDeaths == JSON:", isTRUE(all.equal(as.numeric(USAccDeaths), sb$usaccdeaths$valores)),
    "| AirPassengers == JSON:", isTRUE(all.equal(as.numeric(AirPassengers), sb$airpassengers$valores)),
    "| TRM n =", length(trm), "\n")
lb <- function(f, lag = 24) Box.test(residuals(f), lag = lag, type = "Ljung-Box", fitdf = sum(f$arma[1:4]))$p.value
sec <- function(t) cat("\n\n==================== ", t, " ====================\n", sep = "")

# =============================================================================
sec("E1 · co2")
print(round(c(cruda = var(co2), d1 = var(diff(co2)), D1 = var(diff(co2, lag = 12)),
              ambas = var(diff(diff(co2, lag = 12)))), 4))
print(c(nsdiffs = nsdiffs(co2), nsdiffs_ocsb = nsdiffs(co2, test = "ocsb"),
        ndiffs_crudo = ndiffs(co2), ndiffs_tras_D = ndiffs(diff(co2, lag = 12))))
res <- data.frame()
for (p in 0:2) for (q in 0:3) for (P in 0:1) for (Q in 0:1) {
  f <- tryCatch(Arima(co2, order = c(p, 1, q), seasonal = list(order = c(P, 1, Q), period = 12), method = "ML"),
                error = function(e) NULL, warning = function(w) NULL)
  if (is.null(f)) { cat("no converge:", sprintf("(%d,1,%d)(%d,1,%d)", p, q, P, Q), "\n"); next }
  res <- rbind(res, data.frame(m = sprintf("(%d,1,%d)(%d,1,%d)[12]", p, q, P, Q), k = p + q + P + Q,
                               aicc = f$aicc, bic = f$bic, nobs = f$nobs,
                               lb = Box.test(residuals(f), lag = 24, type = "Ljung-Box", fitdf = p + q + P + Q)$p.value))
}
cat("modelos que convergen:", nrow(res), "\n")
res <- res[order(res$aicc), ]; res$daicc <- res$aicc - min(res$aicc)
print(head(res, 10), digits = 6, row.names = FALSE)
cat("mejor AICc:", res$m[1], " mejor BIC:", res$m[which.min(res$bic)], "\n")
cat("puesto del airline por AICc:", which(res$m == "(0,1,1)(0,1,1)[12]"), "de", nrow(res),
    "| AICc airline (ML):", round(res$aicc[res$m == "(0,1,1)(0,1,1)[12]"], 4),
    "| diferencia:", round(res$aicc[res$m == "(0,1,1)(0,1,1)[12]"] - res$aicc[1], 3), "\n")
cat("modelos a menos de 2 del mejor:", sum(res$daicc < 2), "| que no pasan LB(24) al 5 %:", sum(res$lb < 0.05), "\n")
sinD <- Arima(co2, order = c(0, 1, 1), seasonal = list(order = c(0, 0, 1), period = 12))
conD <- Arima(co2, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
print(round(c(aicc_sinD = sinD$aicc, nobs_sinD = sinD$nobs, aicc_conD = conD$aicc, nobs_conD = conD$nobs), 3))
print(c(lb_sinD = Box.test(residuals(sinD), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value,
        lb_conD = Box.test(residuals(conD), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value))
cat("auto.arima(co2) exhaustivo:", as.character(auto.arima(co2, stepwise = FALSE, approximation = FALSE)), "\n")

# =============================================================================
sec("E2 · USAccDeaths")
ua <- USAccDeaths
print(c(d_a = ndiffs(ua), D_a = nsdiffs(ua), D_b = nsdiffs(ua), d_b = ndiffs(diff(ua, lag = 12))))
cat("max |∇∇12 - ∇12∇| =", max(abs(diff(diff(ua, lag = 12)) - diff(diff(ua), lag = 12))), "\n")
fa <- Arima(ua, order = c(0, 0, 1), seasonal = list(order = c(0, 1, 1), period = 12))
fb <- Arima(ua, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
print(round(c(lb_a = Box.test(residuals(fa), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value,
              lb_b = Box.test(residuals(fb), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value), 6))
print(round(c(aicc_a = fa$aicc, nobs_a = fa$nobs, aicc_b = fb$aicc, nobs_b = fb$nobs), 3))
cat("auto.arima:", as.character(auto.arima(ua, stepwise = FALSE, approximation = FALSE)), "\n")
print(round(coef(fb), 4)); print(round(sqrt(diag(fb$var.coef)), 4))
print(c(seas = nsdiffs(ua), ocsb = nsdiffs(ua, test = "ocsb")))
cat("raíces MA de fa (módulo):", round(Mod(polyroot(c(1, fa$model$theta)))[1:3], 4), "...\n")
cat("coef fa:", round(coef(fa), 4), "\n")

# =============================================================================
sec("E3 · TRM (a) y armónicos de co2 (b)")
print(c(seas = nsdiffs(trm), ocsb = nsdiffs(trm, test = "ocsb")))
a <- Acf(diff(trm), lag.max = 36, plot = FALSE)$acf
print(round(c(r12 = a[13], r24 = a[25], r36 = a[37], banda_n1 = 1.96 / sqrt(length(trm) - 1)), 6))
g <- Arima(trm, order = c(0, 1, 0), seasonal = list(order = c(1, 0, 0), period = 12))
print(round(c(Phi = coef(g)[1], ee = sqrt(diag(g$var.coef))[1], t = coef(g)[1] / sqrt(diag(g$var.coef))[1]), 4))
print(round(c(forzado = g$aicc, simple = Arima(trm, order = c(0, 1, 0))$aicc), 3))
cat("auto.arima(trm):", as.character(auto.arima(trm, stepwise = FALSE, approximation = FALSE)), "\n")
arm <- data.frame()
for (K in 1:6) {
  xr <- fourier(co2, K = K)
  f <- auto.arima(co2, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  arm <- rbind(arm, data.frame(K = K, terminos = ncol(xr), n_ef = f$nobs, modelo = as.character(f),
                               aicc = round(f$aicc, 3), lb = round(Box.test(residuals(f), lag = 24, type = "Ljung-Box",
                                                                          fitdf = sum(f$arma[1:4]))$p.value, 4)))
}
print(arm, row.names = FALSE)
airline_co2 <- conD
cat("airline co2: AICc", round(airline_co2$aicc, 3), "n", airline_co2$nobs,
    "LB(24) p", round(Box.test(residuals(airline_co2), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value, 4), "\n")
kbest <- arm$K[which.min(arm$aicc)]
cat("mejor K por AICc:", kbest, "| AICc armónico - AICc airline =", round(min(arm$aicc) - airline_co2$aicc, 3),
    "| ¿airline < armónico? ", airline_co2$aicc < min(arm$aicc), "\n")
cat("lectura ingenua (menor AICc) elige:", ifelse(airline_co2$aicc < min(arm$aicc), "el airline", "el armónico"), "\n")

# =============================================================================
sec("Quiz cap5 · claves")
cat("-- Q1 (TRM en niveles)\n")
an <- Acf(trm, lag.max = 36, plot = FALSE)$acf
print(round(c(n = length(trm), r1 = an[2], r12 = an[13], r36 = an[37], banda = 1.96 / sqrt(length(trm))), 4))
print(round(c(d_r12 = a[13], d_r24 = a[25], d_r36 = a[37]), 5))
cat("-- Q2 SARIMA(1,0,0)(1,0,0)12, phi 0.6, Phi 0.7: polinomio y ACF teórica\n")
arpol <- c(0.6, rep(0, 10), 0.7, -0.42)
print(round(ARMAacf(ar = arpol, lag.max = 14)[c(2, 3, 4, 12, 13, 14) ], 4))
cat("coeficientes no nulos del AR(13):", which(arpol != 0), "\n")
cat("-- Q3 n efectivo: 96 - 1 - 12 =", 96 - 1 - 12, "\n")
cat("-- Q4 USAccDeaths: ndiffs crudo", ndiffs(ua), "tras D", ndiffs(diff(ua, lag = 12)), "| theta fb", round(coef(fb)[1], 4), "\n")
cat("   KPSS (tseries, nivel, lshort) sobre ∇12y:", round(kpss.test(diff(ua, lag = 12), lshort = TRUE)$statistic, 4),
    "; sobre ∇∇12y:", round(kpss.test(diff(diff(ua, lag = 12)), lshort = TRUE)$statistic, 4), "\n")
cat("-- Q5 SAR(1)12 Phi = 0.7: ACF en 11, 12, 13, 24, 36\n")
r5 <- ARMAacf(ar = c(rep(0, 11), 0.7), lag.max = 36)
print(round(r5[c(12, 13, 14, 25, 37)], 4))
cat("-- Q6 armónica vs airline sobre log(AirPassengers)\n")
ap <- log(AirPassengers)
fr <- lapply(1:6, function(K) { xr <- fourier(ap, K = K)
  f <- auto.arima(ap, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  list(K = K, f = f) })
ka <- which.min(sapply(fr, function(z) z$f$aicc)); fa6 <- fr[[ka]]$f
air <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
print(round(c(K = ka, aicc_arm = fa6$aicc, n_arm = fa6$nobs, k_arm = length(fa6$coef), lb_arm = lb(fa6),
              aicc_air = air$aicc, n_air = air$nobs, k_air = length(air$coef), lb_air = lb(air)), 4))
cat("   modelo de errores de la armónica:", as.character(fa6), "\n")
cat("-- Q7 calendario: beta log(días) sobre el airline\n")
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = 145)
dias <- as.numeric(diff(fechas))
cal <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), xreg = cbind(log_dias = log(dias)))
b <- coef(cal)["log_dias"]; se <- sqrt(diag(cal$var.coef))["log_dias"]
print(round(c(beta = b, ee = se, t_0 = b / se, t_1 = (b - 1) / se), 4))
cat("   con las cifras del enunciado: (1.0840 - 1)/0.4462 =", round((1.0840 - 1) / 0.4462, 6), "\n")
cat("-- Q8 partición única (últimos 24) y origen móvil (61 orígenes, h = 12)\n")
apb <- AirPassengers; n <- length(ap)
ent <- window(ap, end = time(ap)[n - 24]); ento <- window(apb, end = time(ap)[n - 24])
obs <- as.numeric(window(apb, start = time(ap)[n - 23]))
rm <- function(p) sqrt(mean((obs - as.numeric(p))^2)); ma <- function(p) mean(abs(obs - as.numeric(p)))
mp <- function(p) 100 * mean(abs((obs - as.numeric(p)) / obs))
fsar <- exp(forecast(Arima(ent, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)), h = 24)$mean)
Kb <- ka
farm <- exp(forecast(auto.arima(ent, xreg = fourier(ent, K = Kb), seasonal = FALSE, stepwise = FALSE, approximation = FALSE),
                     xreg = fourier(ent, K = Kb, h = 24), h = 24)$mean)
fets <- forecast(ets(ento), h = 24)$mean
fetsl <- exp(forecast(ets(ent), h = 24)$mean)
fstl <- exp(forecast(stlm(ent, s.window = "periodic", method = "arima"), h = 24)$mean)
fsn <- snaive(ento, h = 24)$mean
fauto <- exp(forecast(auto.arima(ent, stepwise = FALSE, approximation = FALSE), h = 24)$mean)
tab <- rbind(sarima = c(rm(fsar), ma(fsar), mp(fsar)), armonica = c(rm(farm), ma(farm), mp(farm)),
             ets_crudo = c(rm(fets), ma(fets), mp(fets)), ets_log = c(rm(fetsl), ma(fetsl), mp(fetsl)),
             stl = c(rm(fstl), ma(fstl), mp(fstl)), snaive = c(rm(fsn), ma(fsn), mp(fsn)), auto = c(rm(fauto), ma(fauto), mp(fauto)))
colnames(tab) <- c("RMSE", "MAE", "MAPE"); print(round(tab[order(tab[, 1]), ], 3))
cat("   puesto del SARIMA por RMSE/MAE/MAPE entre estos 7 (sin el SARIMA + calendario):",
    rank(tab[, 1])["sarima"], rank(tab[, 2])["sarima"], rank(tab[, 3])["sarima"], "\n")
org <- 72:(n - 12); err <- list()
pr <- list(
  snaive = function(el, eo) as.numeric(snaive(eo, h = 12)$mean),
  sarima = function(el, eo) exp(as.numeric(forecast(Arima(el, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)), h = 12)$mean)),
  armonica = function(el, eo) exp(as.numeric(forecast(auto.arima(el, xreg = fourier(el, K = 6), seasonal = FALSE), xreg = fourier(el, K = 6, h = 12), h = 12)$mean)),
  ets_log = function(el, eo) exp(as.numeric(forecast(ets(el), h = 12)$mean)),
  ets_orig = function(el, eo) as.numeric(forecast(ets(eo), h = 12)$mean),
  stl = function(el, eo) exp(as.numeric(forecast(stlm(el, s.window = "periodic", method = "arima"), h = 12)$mean)))
for (nm in names(pr)) err[[nm]] <- numeric(0)
for (o in org) {
  el <- window(ap, end = time(ap)[o]); eo <- window(apb, end = time(ap)[o])
  ob <- as.numeric(window(apb, start = time(ap)[o + 1], end = time(ap)[o + 12]))
  for (nm in names(pr)) err[[nm]] <- c(err[[nm]], sqrt(mean((ob - pr[[nm]](el, eo))^2)))
}
cat("   orígenes:", length(org), "\n")
print(round(sort(sapply(err, mean)), 3))
cat("   % de orígenes en que el SARIMA gana a cada rival:\n")
print(round(100 * sapply(setdiff(names(err), "sarima"), function(nm) mean(err$sarima < err[[nm]])), 1))

# =============================================================================
sec("Simulacro · claves numéricas desde el enunciado")
cat("-- N2 ∇∇12 log y (sep 2025)\n")
y <- c(ago24 = 496.19, sep24 = 445.82, ago25 = 506.77, sep25 = 434.25)
L <- log(y); v2 <- L[["sep25"]] - L[["ago25"]] - L[["sep24"]] + L[["ago24"]]
print(round(c(exacto = v2, logs4 = sum(round(L, 4) * c(1, -1, -1, 1)), solo_D = L[["sep25"]] - L[["sep24"]],
              solo_d = L[["sep25"]] - L[["ago25"]], log10 = sum(log10(y) * c(1, -1, -1, 1)),
              sin_log = sum(y * c(1, -1, -1, 1))), 6))
cat("-- N4 rho13 del airline\n")
th <- -0.4012; Th <- -0.6514
r13 <- th * Th / ((1 + th^2) * (1 + Th^2))
acf_air <- ARMAacf(ma = c(th, rep(0, 10), Th, th * Th), lag.max = 13)
print(round(c(formula = r13, ARMAacf = acf_air[["13"]], rho1 = acf_air[["1"]], rho12 = acf_air[["12"]]), 6))
cat("-- N5 Q(24)\n")
nn <- 167; s22 <- 0.0006073
Q <- nn * (nn + 2) * (s22 + (-0.0801)^2 / (nn - 12) + 0.0180^2 / (nn - 24))
print(round(c(Q = Q, dividiendo_entre_n = nn * (nn + 2) * (s22 + (-0.0801)^2 / nn + 0.0180^2 / nn),
              sin_n_mas_2 = nn * nn * (s22 + (-0.0801)^2 / (nn - 12) + 0.0180^2 / (nn - 24)),
              critico_22 = qchisq(0.95, 22), critico_24 = qchisq(0.95, 24), p22 = 1 - pchisq(Q, 22)), 4))
cat("-- N6 sigma_13\n")
s2 <- 0.003152
psi <- c(1, rep(1 + th, 11), (1 + th) + (1 + Th))
# pesos psi exactos: el airline como ARMA con AR no estacionario (1-B)(1-B^12)
psi_ex <- c(1, ARMAtoMA(ar = c(1, rep(0, 10), 1, -1), ma = c(th, rep(0, 10), Th, th * Th), lag.max = 12))
print(round(rbind(enunciado = psi, expansion = psi_ex), 6))
print(round(c(sigma13 = sqrt(s2 * sum(psi^2)), sin_escalon = sqrt(s2 * (1 + 12 * (1 + th)^2)),
              sin_psi12 = sqrt(s2 * (1 + 11 * (1 + th)^2)), sumando_psi = sqrt(s2 * sum(psi))), 6))
cat("-- N7 pronóstico de enero de 2026\n")
f7 <- 6.4671 + 6.3034 - 6.3973 + th * 0.0764 + Th * 0.0313 + th * Th * 0.0294
v7 <- c(exacto = exp(f7), sin_satelite = exp(f7 - th * Th * 0.0294), satelite_restado = exp(f7 - 2 * th * Th * 0.0294),
        sin_theta = exp(f7 - th * 0.0764), sin_Theta = exp(f7 - Th * 0.0313),
        log_redondeado_2 = exp(round(f7, 2)), log_redondeado_3 = exp(round(f7, 3)), media_lognormal = exp(f7 + 0.003152 / 2))
print(round(c(log = f7, v7), 4))
cat("   tolerancia 0.008·561.07 =", round(0.008 * 561.07, 5), "; |variante − clave|:\n")
print(round(abs(v7 - 561.07), 3))
cat("-- N10 t de β = 1\n")
print(round(c(t1 = (2.0094 - 1) / 0.3601, t0 = 2.0094 / 0.3601), 6))
cat("-- S11 (comparación dentro de la familia, D = 0, n = 260): menor AICc K =", c(1768.74, 1744.44, 1710.07, 1674.23, 1493.47, 1496.20, 1499.73) |> which.min(), "\n")
cat("-- S12 ETS sobre el log: menor RMSE medio de 4:", c(SARIMA = 37.89, ETS = 25.55, STL = 37.42, naive = 45.02) |> which.min() |> names(), "\n")
