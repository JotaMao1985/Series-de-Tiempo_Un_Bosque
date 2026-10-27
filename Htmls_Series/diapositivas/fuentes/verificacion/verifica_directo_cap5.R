# ============================================================================
# verifica_directo_cap5.R — cifras de las diapositivas del capítulo 5 que NO
# están en precalculo/salidas/cap5_sarima.json, recalculadas desde los datos.
#
# Lo que hace
#   - Lee las series de precalculo/salidas/datos_series.json (las mismas que usa
#     genera_cap5.R) y comprueba que AirPassengers, USAccDeaths y co2 coinciden
#     con los de `datasets` de R.
#   - Recalcula: los momentos del M2 (factorización exacta en el MA y la tabla
#     de error con parte AR), las ACF teóricas a 5 decimales del M4, el rango
#     relativo del M7, el contraste de beta = 1 del M9, el auto.arima con m = 365
#     del M10, y todo lo del M11 que el JSON no guarda (crecimientos anuales, el
#     sesgo del airline, los orígenes en que pierde, el horizonte de 24 meses y
#     el error del mes 12).
#   - Guarda el entorno (versiones de R, forecast y tseries) en el JSON.
#
# Uso (desde la raíz del repositorio; tarda unos minutos por el origen móvil):
#   Rscript Htmls_Series/diapositivas/fuentes/verificacion/verifica_directo_cap5.R
# Escribe directo_cap5.json junto a este archivo.
# ============================================================================

suppressMessages({
  library(jsonlite)
  library(forecast)
  library(tseries)
})
invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8")))

aqui <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
raiz <- normalizePath(file.path(aqui, "..", "..", "..", ".."))
base <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"), simplifyVector = TRUE)

out <- list()
out$entorno <- list(R = R.version.string,
                    forecast = as.character(packageVersion("forecast")),
                    tseries = as.character(packageVersion("tseries")),
                    fecha = format(Sys.time(), "%Y-%m-%d %H:%M"))

ap_bruta <- ts(base$airpassengers$valores, start = base$airpassengers$inicio, frequency = 12)
ap  <- log(ap_bruta)
uad <- ts(base$usaccdeaths$valores, start = base$usaccdeaths$inicio, frequency = 12)
co2s <- ts(base$co2$valores, start = base$co2$inicio, frequency = 12)
trm <- ts(base$trm$valores, start = base$trm$inicio, frequency = 12)

# --- Los datos congelados son los de `datasets` -------------------------------
out$datos <- list(
  ap_igual_datasets  = isTRUE(all.equal(as.numeric(ap_bruta), as.numeric(AirPassengers))),
  uad_igual_datasets = isTRUE(all.equal(as.numeric(uad), as.numeric(USAccDeaths))),
  co2_igual_datasets = isTRUE(all.equal(as.numeric(co2s), as.numeric(co2))),
  ap_inicio = start(ap)[1], ap_fin = end(ap)[1], ap_n = length(ap),
  uad_inicio = start(uad)[1], uad_fin = end(uad)[1], uad_n = length(uad),
  co2_inicio = start(co2s)[1], co2_fin = end(co2s)[1], co2_n = length(co2s),
  trm_inicio = paste(start(trm), collapse = "-"), trm_fin = paste(end(trm), collapse = "-"),
  trm_n = length(trm)
)

# --- M1 · bandas y la ACF de las series --------------------------------------
acf_en <- function(x, k) { a <- Acf(x, lag.max = max(k), plot = FALSE)$acf; a[k + 1] }
out$m1 <- list(
  ap_log = acf_en(ap, c(1, 12, 24, 36)),
  banda_ap = 1.96 / sqrt(length(ap)),
  trm_niveles = acf_en(trm, c(1, 12, 24, 36)),
  banda_trm = 1.96 / sqrt(length(trm)),
  trm_diff = acf_en(diff(trm), c(1, 12, 24, 36)),
  banda_trm_diff = 1.96 / sqrt(length(diff(trm)))
)

# --- M2 · momentos -------------------------------------------------------------
fit <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
th <- unname(coef(fit)["ma1"]); Th <- unname(coef(fit)["sma1"]); s2 <- fit$sigma2
w <- diff(diff(ap, lag = 12))
psi_ar <- function(phi, Phi, n = 20000)
  c(1, ARMAtoMA(ar = c(phi, rep(0, 10), Phi, -phi * Phi), lag.max = n))
tabla_phi <- lapply(c(0.6, 0.8, 0.9, 0.95), function(phi) {
  psi <- psi_ar(phi, 0.7)
  ex <- sum(psi^2); fa <- 1 / ((1 - phi^2) * (1 - 0.7^2))
  list(phi = phi, phi12 = phi^12, exacta = ex, factorizada = fa, error_pct = 100 * (fa - ex) / ex,
       psi12 = psi[13])
})
out$m2 <- list(
  theta = th, Theta = Th, sigma2 = s2,
  factor_airline = (1 + th^2) * (1 + Th^2),
  gamma0_airline = s2 * (1 + th^2) * (1 + Th^2),
  var_muestral_w = var(w), n_w = length(w),
  rho1_airline = th / (1 + th^2),
  # q alcanza a m: theta_12 = 0.5 y Theta = 0.6 chocan en el rezago 12
  choque_exacta = sum(c(1, 0.5 + 0.6, 0.5 * 0.6)^2),
  choque_factorizada = (1 + 0.5^2) * (1 + 0.6^2),
  tabla_phi = tabla_phi,
  coef_b13 = th * Th
)

# --- M4 · ACF teóricas exactas ----------------------------------------------
acf_t <- function(ar = numeric(0), ma = numeric(0)) ARMAacf(ar = ar, ma = ma, lag.max = 36)[-1]
r_arsar <- acf_t(ar = c(0.6, rep(0, 10), 0.7, -0.42))
r_air <- acf_t(ma = c(th, rep(0, 10), Th, th * Th))
r_air_red <- acf_t(ma = c(-0.4018, rep(0, 10), -0.5569, -0.4018 * -0.5569))
r_sma <- acf_t(ma = c(rep(0, 11), -0.6))
r_sar <- acf_t(ar = c(rep(0, 11), 0.7))
r_arsma <- acf_t(ar = 0.5, ma = c(rep(0, 11), -0.7))
out$m4 <- list(
  ar1_sar1 = list(r1 = r_arsar[1], r11 = r_arsar[11], r12 = r_arsar[12], r13 = r_arsar[13], r24 = r_arsar[24],
                  producto = r_arsar[1] * r_arsar[12]),
  airline = list(r1 = r_air[1], r11 = r_air[11], r12 = r_air[12], r13 = r_air[13], r24 = r_air[24],
                 producto = r_air[1] * r_air[12]),
  airline_redondeado = list(r1 = r_air_red[1], r11 = r_air_red[11], r12 = r_air_red[12]),
  sar1 = list(r12 = r_sar[12], r24 = r_sar[24], r36 = r_sar[36], r1 = r_sar[1], r11 = r_sar[11]),
  sma1 = list(r12 = r_sma[12], r24 = r_sma[24]),
  ar1_sma1 = list(r1 = r_arsma[1], r11 = r_arsma[11], r12 = r_arsma[12], r13 = r_arsma[13], r24 = r_arsma[24])
)

# --- M3 · nsdiffs según la prueba, y desde cuándo `seas` es la de por defecto --
noticias <- tryCatch(as.data.frame(news(package = "forecast")), error = function(e) NULL)
linea_seas <- if (!is.null(noticias)) {
  i <- grep("nsdiffs", noticias$Text)
  i <- i[grepl("seas", noticias$Text[i])]
  if (length(i)) paste(noticias$Version[i], "·", gsub("\\s+", " ", noticias$Text[i]), collapse = " || ") else ""
} else ""
out$m3 <- list(
  formals_nsdiffs_test = paste(eval(formals(nsdiffs)$test), collapse = ","),
  news_seas = linea_seas,
  ap = c(seas = nsdiffs(ap), ocsb = nsdiffs(ap, test = "ocsb")),
  uad = c(seas = nsdiffs(uad), ocsb = nsdiffs(uad, test = "ocsb"), ndiffs = ndiffs(uad),
          ndiffs_tras_D = ndiffs(diff(uad, lag = 12))),
  ap_var = c(d0D0 = var(ap), d1D0 = var(diff(ap)), d0D1 = var(diff(ap, lag = 12)), d1D1 = var(w))
)

# --- M7 · rango relativo, ACF de la serie diferenciada, e.e. aproximado -------
a_w <- Acf(w, lag.max = 24, plot = FALSE)$acf
r_res <- Acf(residuals(fit), lag.max = 24, plot = FALSE)$acf
out$m7 <- list(
  rango_relativo = (max(ap_bruta) - min(ap_bruta)) / mean(ap_bruta),
  n_w = length(w), banda_w = 1.96 / sqrt(length(w)), ee_aprox = 1 / sqrt(length(w)),
  r1 = a_w[2], r11 = a_w[12], r12 = a_w[13], r13 = a_w[14], r3 = a_w[4], r9 = a_w[10], r23 = a_w[24],
  res_r3 = r_res[4], res_r9 = r_res[10], res_r23 = r_res[24], res_r12 = r_res[13], res_r24 = r_res[25],
  banda_res = 1.96 / sqrt(length(residuals(fit))),
  ee = sqrt(diag(fit$var.coef)), t = coef(fit) / sqrt(diag(fit$var.coef)),
  lb24 = Box.test(residuals(fit), lag = 24, type = "Ljung-Box", fitdf = 2)$p.value,
  lb36 = Box.test(residuals(fit), lag = 36, type = "Ljung-Box", fitdf = 2)$p.value,
  shapiro = shapiro.test(residuals(fit))$p.value,
  raiz_ma = max(Mod(1 / polyroot(c(1, fit$model$theta))))
)
p24 <- forecast(fit, h = 24, level = c(80, 95))
out$m7$pron24 <- c(mediana = exp(p24$mean[24]), lo95 = exp(p24$lower[24, 2]), hi95 = exp(p24$upper[24, 2]))
sig24 <- (p24$upper[24, 2] - p24$mean[24]) / qnorm(0.975)
out$m7$media24 <- exp(p24$mean[24] + sig24^2 / 2)

# --- M9 · el contraste de beta = 1 --------------------------------------------
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = length(ap))
dias <- as.numeric(diff(c(fechas, seq(tail(fechas, 1), by = "month", length.out = 2)[2])))
pascua <- function(anio) {
  a <- anio %% 19; b <- anio %/% 100; cc <- anio %% 100
  d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3
  h <- (19*a + b - d - g + 15) %% 30; i <- cc %/% 4; k <- cc %% 4
  l <- (32 + 2*e + 2*i - h - k) %% 7; m <- (a + 11*h + 22*l) %/% 451
  mes <- (h + l - 7*m + 114) %/% 31; dia <- ((h + l - 7*m + 114) %% 31) + 1
  as.Date(sprintf("%04d-%02d-%02d", anio, mes, dia))
}
mes_pascua <- sapply(1949:1960, function(a) as.numeric(format(pascua(a), "%m")))
es_pascua <- as.numeric(as.numeric(format(fechas, "%m")) == mes_pascua[as.numeric(format(fechas, "%Y")) - 1948])
f2 <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12),
            xreg = cbind(log_dias = log(dias), pascua = es_pascua))
ee2 <- sqrt(diag(f2$var.coef))
out$m9 <- list(
  beta_dias = unname(coef(f2)["log_dias"]), ee_dias = unname(ee2["log_dias"]),
  t_beta1 = unname((coef(f2)["log_dias"] - 1) / ee2["log_dias"]),
  beta_pascua = unname(coef(f2)["pascua"]), t_pascua = unname(coef(f2)["pascua"] / ee2["pascua"]),
  pascua_pct = 100 * (exp(unname(coef(f2)["pascua"])) - 1),
  pascuas_marzo = sum(mes_pascua == 3), pascuas_abril = sum(mes_pascua == 4),
  aicc = f2$aicc, delta_aicc = fit$aicc - f2$aicc,
  variacion_dias_pct = 100 * (31 / 28 - 1)
)

# --- M10 · m grande ---------------------------------------------------------
set.seed(1); z <- ts(rnorm(800), frequency = 365)
out$m10 <- list(
  auto_365 = as.character(auto.arima(z)),
  n_semanal = 156, queda_tras_52 = 156 - 52,
  ncol_fourier_K3_m52 = ncol(fourier(ts(rnorm(156), frequency = 52), K = 3)),
  nobs_airline = fit$nobs
)

# --- M11 · lo que el JSON no guarda ------------------------------------------
anual <- tapply(as.numeric(ap_bruta), floor(time(ap_bruta)), sum)
crec <- 100 * (anual[-1] / anual[-length(anual)] - 1)
n_ap <- length(ap)
entrena <- window(ap, end = time(ap)[n_ap - 24])
entrena_orig <- window(ap_bruta, end = time(ap)[n_ap - 24])
obs24 <- as.numeric(window(ap_bruta, start = time(ap)[n_ap - 23]))
desde_log <- function(p) exp(as.numeric(p))
f_sar <- desde_log(forecast(Arima(entrena, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)), h = 24)$mean)
f_ets_log <- desde_log(forecast(ets(entrena), h = 24)$mean)
xr_ent <- fourier(entrena, K = 6); xr_fut <- fourier(entrena, K = 6, h = 24)
f_arm <- desde_log(forecast(auto.arima(entrena, xreg = xr_ent, seasonal = FALSE, stepwise = FALSE,
                                       approximation = FALSE), xreg = xr_fut, h = 24)$mean)
crec_pron <- function(f) {
  t58 <- anual[["1958"]]; t59 <- sum(f[1:12]); t60 <- sum(f[13:24])
  c(f59_vs_obs58 = 100 * (t59 / t58 - 1), f60_vs_f59 = 100 * (t60 / t59 - 1),
    f60_vs_obs59 = 100 * (t60 / anual[["1959"]] - 1))
}
out$m11 <- list(
  crecimiento_anual = as.list(round(crec, 4)),
  crec_1958 = crec[["1958"]],
  crec_otros_min = min(crec[names(crec) != "1958"]), crec_otros_max = max(crec[names(crec) != "1958"]),
  sarima_pron = as.list(crec_pron(f_sar)),
  ets_log_pron = as.list(crec_pron(f_ets_log)),
  armonica_pron = as.list(crec_pron(f_arm)),
  sesgo_sarima = mean(obs24 - f_sar), mae_sarima = mean(abs(obs24 - f_sar)),
  errores_positivos = sum(obs24 - f_sar > 0)
)

# Las métricas de la partición única SIN redondear (J las guarda a 3 decimales y la
# diapositiva las muestra a 2: hace falta el valor exacto para no redondear dos veces)
metr <- function(p) { e <- obs24 - as.numeric(p)
  list(rmse = sqrt(mean(e^2)), mae = mean(abs(e)), mape = 100 * mean(abs(e / obs24))) }
xcal <- cbind(log_dias = log(dias), pascua = es_pascua)
m_ets <- ets(entrena_orig); m_ets_log <- ets(entrena)
m_arm <- auto.arima(entrena, xreg = xr_ent, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
m_stl <- stlm(entrena, s.window = "periodic", method = "arima")
m_cal <- Arima(entrena, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12),
               xreg = xcal[seq_len(length(entrena)), , drop = FALSE])
out$m11$particion <- list(
  snaive = metr(snaive(entrena_orig, h = 24)$mean),
  sarima = metr(f_sar),
  ets = c(metr(forecast(m_ets, h = 24)$mean), list(metodo = m_ets$method, n_par = length(m_ets$par))),
  ets_log = c(metr(f_ets_log), list(metodo = m_ets_log$method, n_par = length(m_ets_log$par))),
  armonica = c(metr(f_arm), list(n_par = length(m_arm$coef))),
  stl_arima = c(metr(desde_log(forecast(m_stl, h = 24)$mean)), list(n_par = length(m_stl$model$coef),
                modelo = as.character(m_stl$model))),
  sarima_calendario = metr(desde_log(forecast(m_cal, xreg = xcal[length(entrena) + 1:24, , drop = FALSE], h = 24)$mean))
)

# Origen móvil, con los mismos seis pronosticadores que genera_cap5.R
pron <- list(
  snaive  = function(e_log, e_orig, h) as.numeric(snaive(e_orig, h = h)$mean),
  sarima  = function(e_log, e_orig, h) desde_log(forecast(
              Arima(e_log, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12)), h = h)$mean),
  armonica = function(e_log, e_orig, h) desde_log(forecast(
              auto.arima(e_log, xreg = fourier(e_log, K = 6), seasonal = FALSE),
              xreg = fourier(e_log, K = 6, h = h), h = h)$mean),
  ets_log  = function(e_log, e_orig, h) desde_log(forecast(ets(e_log), h = h)$mean),
  ets_orig = function(e_log, e_orig, h) as.numeric(forecast(ets(e_orig), h = h)$mean),
  stl      = function(e_log, e_orig, h) desde_log(forecast(
              stlm(e_log, s.window = "periodic", method = "arima"), h = h)$mean)
)
etiqueta <- function(o) { t <- time(ap)[o]; sprintf("%d-%02d", floor(t + 1e-8), round(12 * (t - floor(t + 1e-8))) + 1) }
origen_movil <- function(H) {
  origenes <- seq(from = 72, to = n_ap - H)
  rmse <- matrix(NA, length(origenes), length(pron), dimnames = list(NULL, names(pron)))
  e_h <- rmse
  for (i in seq_along(origenes)) {
    o <- origenes[i]
    e_log <- window(ap, end = time(ap)[o]); e_orig <- window(ap_bruta, end = time(ap)[o])
    obs <- as.numeric(window(ap_bruta, start = time(ap)[o + 1], end = time(ap)[o + H]))
    for (nm in names(pron)) {
      p <- pron[[nm]](e_log, e_orig, H)
      rmse[i, nm] <- sqrt(mean((obs - p)^2)); e_h[i, nm] <- obs[H] - p[H]
    }
  }
  no_mejor <- which(apply(rmse, 1, which.min) != which(colnames(rmse) == "sarima"))
  list(n = length(origenes), primer = etiqueta(origenes[1]),
       rmse_medio = as.list(colMeans(rmse)),
       gana_al_sarima_pct = as.list(100 * colMeans(rmse < rmse[, "sarima"])),
       error_mes_h_abs = as.list(colMeans(abs(e_h))),
       error_mes_h_rmse = as.list(sqrt(colMeans(e_h^2))),
       sarima_no_es_el_mejor = length(no_mejor),
       origenes_no_mejor = vapply(origenes[no_mejor], etiqueta, ""))
}
cat("Origen móvil h = 12…\n"); out$m11$om12 <- origen_movil(12)
cat("Origen móvil h = 24…\n"); out$m11$om24 <- origen_movil(24)

destino <- file.path(aqui, "directo_cap5.json")
writeLines(toJSON(out, auto_unbox = TRUE, digits = 10, pretty = TRUE), destino, useBytes = TRUE)
cat("escrito:", destino, "\n")
