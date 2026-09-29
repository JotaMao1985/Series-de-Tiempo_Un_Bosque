# ============================================================================
# verifica_directo_cap4.R — recalcula en R, sobre los datos crudos, las cifras
# de las diapositivas del capítulo 4 que NO están en precalculo/salidas/
# cap4_arima.json (o que conviene contrastar por un camino independiente).
#
# Uso (desde la raíz del repositorio):
#   Rscript Htmls_Series/diapositivas/fuentes/verificacion/verifica_directo_cap4.R
# Escribe verificacion/directo_cap4.json. Dependencias: forecast, tseries,
# jsonlite, urca (la carga forecast::ndiffs).
# ============================================================================
suppressMessages({ library(forecast); library(tseries); library(jsonlite) })

args  <- commandArgs(trailingOnly = TRUE)
raiz  <- if (length(args) >= 1) args[1] else "."
salida <- if (length(args) >= 2) args[2] else file.path(raiz, "Htmls_Series/diapositivas/fuentes/verificacion/directo_cap4.json")

sj <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"), simplifyVector = TRUE)
out <- list(entorno = list(R = R.version.string,
                           forecast = as.character(packageVersion("forecast")),
                           tseries  = as.character(packageVersion("tseries"))))
put <- function(k, v) { out[[k]] <<- v; invisible(NULL) }
r   <- function(x, d) round(as.numeric(x), d)
mods <- function(f, patron) { cf <- coef(f); cf[grepl(patron, names(cf))] }
kurt <- function(x) mean((x - mean(x))^4) / mean((x - mean(x))^2)^2
skew <- function(x) mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5

# ---- Datos: los de las diapositivas son los de R --------------------------
put("datos.nilo_igual_datasets", isTRUE(all(as.numeric(Nile) == sj$nilo$valores)))
put("datos.nilo_n", length(Nile)); put("datos.nilo_inicio", start(Nile)[1]); put("datos.nilo_fin", end(Nile)[1])
put("datos.ap_igual_datasets", isTRUE(all(as.numeric(AirPassengers) == sj$airpassengers$valores)))
put("datos.ap_n", length(AirPassengers)); put("datos.ap_inicio", start(AirPassengers)[1]); put("datos.ap_fin", end(AirPassengers)[1])
trm <- ts(sj$trm$valores, start = c(2015, 1), frequency = 12)
put("datos.trm_n", length(trm)); put("datos.trm_primero", as.numeric(trm)[1])
put("datos.trm_ultimo", tail(as.numeric(trm), 1)); put("datos.trm_inicio", paste(start(trm), collapse = "-")); put("datos.trm_fin", paste(end(trm), collapse = "-"))
put("datos.bjsales_n", length(BJsales)); put("datos.lynx_n", length(lynx)); put("datos.lynx_inicio", start(lynx)[1]); put("datos.lynx_fin", end(lynx)[1])

# ---- M1 -------------------------------------------------------------------
for (d in 0:2) {
  x <- if (d == 0) Nile else diff(Nile, differences = d)
  put(sprintf("m1.d%d.n", d), length(x)); put(sprintf("m1.d%d.media", d), r(mean(x), 2))
  put(sprintf("m1.d%d.var", d), r(var(x), 2)); put(sprintf("m1.d%d.rho1", d), r(acf(x, plot = FALSE)$acf[2], 4))
}
phi <- 0.2544; ar_exp <- c(1 + phi, -phi)
put("m1.ar_expandido", r(ar_exp, 4)); put("m1.suma_ar", sum(ar_exp))
put("m1.raices", r(Mod(polyroot(c(1, -ar_exp))), 4))
set.seed(2026); w <- arima.sim(list(ar = 0.2544, ma = -0.8741), n = 200); y <- cumsum(w)
put("m1.razon", r(var(y) / var(w), 3))
set.seed(2026); w0 <- arima.sim(list(ar = 0.2544), n = 200)
put("m1.razon_sin_ma", r(var(cumsum(w0)) / var(w0), 1))

# ---- M2: el esqueleto del ciclo, tal cual se proyecta ----------------------
d <- ndiffs(Nile); put("m2.ndiffs", d)
ajuste <- arima(Nile, order = c(1, d, 1), method = "ML"); res <- residuals(ajuste)
put("m2.lb20_p", Box.test(res, lag = 20, type = "Ljung-Box", fitdf = 2)$p.value)
pron <- forecast(ajuste, h = 10); put("m2.pron_1a3", r(pron$mean[1:3], 2))

# ---- M3 -------------------------------------------------------------------
put("m3.var_d0a3", r(sapply(0:3, function(k) var(if (k == 0) Nile else diff(Nile, differences = k))), 2))
a <- suppressWarnings(adf.test(Nile)); put("m3.adf_stat", r(a$statistic, 4)); put("m3.adf_p", r(a$p.value, 4)); put("m3.adf_rezagos", as.numeric(a$parameter))
kp <- suppressWarnings(kpss.test(Nile)); put("m3.kpss_stat", r(kp$statistic, 4)); put("m3.kpss_p", kp$p.value)
pp <- PP.test(Nile); put("m3.pp_stat", r(pp$statistic, 4)); put("m3.pp_p", pp$p.value)   # stats::PP.test, como genera_cap4.R
put("m3.ndiffs", as.list(sapply(c("kpss", "adf", "pp"), function(t) ndiffs(Nile, test = t))))
u <- urca::ur.df(Nile, type = "drift", lags = 1)
put("m3.urdf_tau", r(u@teststat[1, "tau2"], 2)); put("m3.urdf_crit5", r(u@cval["tau2", "5pct"], 2))

# ---- M4 -------------------------------------------------------------------
w <- diff(Nile)
put("m4.banda", r(1.96 / sqrt(length(w)), 4))
put("m4.acf_1a6", r(acf(w, lag.max = 6, plot = FALSE)$acf[-1], 4))
put("m4.pacf_1a3", r(as.numeric(pacf(w, lag.max = 6, plot = FALSE)$acf)[1:3], 4))
put("m4.acf_sin_dif_1a4", r(acf(Nile, lag.max = 4, plot = FALSE)$acf[-1], 4))
put("m4.ar1_phi05_rezagos2y3", c(0.5^2, 0.5^3))
ma1 <- arima(Nile, order = c(0, 1, 1), method = "ML")
put("m4.theta", r(coef(ma1)[["ma1"]], 4)); put("m4.theta_ee", r(sqrt(ma1$var.coef[1, 1]), 4))
put("m4.theta_t", r(coef(ma1)[["ma1"]] / sqrt(ma1$var.coef[1, 1]), 2)); put("m4.sigma2", r(ma1$sigma2, 2))
put("m4.lb20_p", Box.test(residuals(ma1), lag = 20, type = "Ljung-Box", fitdf = 1)$p.value)

# ---- M5 -------------------------------------------------------------------
f0 <- arima(Nile, order = c(1, 0, 1), method = "ML"); put("m5.f0_coef", r(coef(f0), 4))
f1a <- arima(Nile, order = c(1, 1, 1), include.mean = TRUE, method = "ML"); put("m5.arima_d1_include_mean_coef", names(coef(f1a)))
f1b <- Arima(Nile, order = c(1, 1, 1), include.drift = TRUE)
ee <- sqrt(diag(f1b$var.coef))[["drift"]]; dr <- coef(f1b)[["drift"]]
put("m5.deriva", r(dr, 4)); put("m5.deriva_ee", r(ee, 4)); put("m5.deriva_t", r(dr / ee, 3))
put("m5.phi1", r(coef(f1b)[["ar1"]], 4)); put("m5.c", r(dr * (1 - coef(f1b)[["ar1"]]), 2))
put("m5.aicc_con", r(f1b$aicc, 3)); put("m5.aicc_sin", r(Arima(Nile, order = c(1, 1, 1))$aicc, 3))
aviso <- NA_character_
f2 <- withCallingHandlers(Arima(Nile, order = c(1, 2, 1), include.drift = TRUE),
        warning = function(w) { aviso <<- conditionMessage(w); invokeRestart("muffleWarning") })
put("m5.d2_aviso", aviso); put("m5.d2_tiene_deriva", "drift" %in% names(coef(f2)))
put("m5.media_dif", r((Nile[100] - Nile[1]) / 99, 2)); put("m5.nilo_1871", as.numeric(Nile[1])); put("m5.nilo_1970", as.numeric(Nile[100]))
escalon <- as.numeric(time(Nile) >= 1899)
fe <- arima(Nile, order = c(0, 0, 0), xreg = escalon, method = "ML")
put("m5.aporte_escalon", r(coef(fe)[["escalon"]] / 99, 2))
ft <- Arima(trm, order = c(0, 1, 0), include.drift = TRUE)
put("m5.trm_deriva", r(coef(ft)[["drift"]], 4)); put("m5.trm_deriva_ee", r(sqrt(diag(ft$var.coef))[["drift"]], 4))
put("m5.trm_deriva_t", r(coef(ft)[["drift"]] / sqrt(diag(ft$var.coef))[["drift"]], 3))
put("m5.trm_media_dif", r((tail(as.numeric(trm), 1) - as.numeric(trm)[1]) / (length(trm) - 1), 4))
put("m5.trm_aicc_con", r(ft$aicc, 2)); put("m5.trm_aicc_sin", r(Arima(trm, order = c(0, 1, 0))$aicc, 2))

# ---- M8 -------------------------------------------------------------------
put("m8.escalon_coef", r(coef(fe)[["escalon"]], 2)); put("m8.escalon_ee", r(sqrt(fe$var.coef[2, 2]), 2))
put("m8.escalon_t", r(coef(fe)[["escalon"]] / sqrt(fe$var.coef[2, 2]), 2))
put("m8.escalon_lb20_p", r(Box.test(residuals(fe), lag = 20, type = "Ljung-Box")$p.value, 4))
put("m8.media_antes_1899", r(mean(Nile[1:28]), 2)); put("m8.media_desde_1899", r(mean(Nile[29:100]), 2))
put("m8.posicion_1899", which(time(Nile) == 1899))
res111 <- residuals(Arima(Nile, order = c(1, 1, 1)))
put("m8.sd_res_111_todos", r(sd(res111), 2)); put("m8.sd_res_111_sin_primero", r(sd(res111[-1]), 2))
ly <- log(lynx)
put("m8.lynx_var_d0a3", r(sapply(0:3, function(k) var(if (k == 0) ly else diff(ly, differences = k))), 4))
put("m8.lynx_reduccion_pct", r(100 * (1 - var(diff(ly)) / var(ly)), 1))
put("m8.lynx_ndiffs", list(kpss = ndiffs(ly, test = "kpss"), adf = ndiffs(ly, test = "adf")))
put("m8.lynx_kpss_p", suppressWarnings(kpss.test(ly)$p.value)); put("m8.lynx_adf_p", suppressWarnings(adf.test(ly)$p.value))
f211 <- arima(ly, order = c(2, 1, 1), method = "ML"); put("m8.lynx_211_raiz_ma", r(min(Mod(polyroot(c(1, mods(f211, "^ma"))))), 4))
f011 <- arima(ly, order = c(0, 1, 1), method = "ML"); put("m8.lynx_011_raiz_ma", r(min(Mod(polyroot(c(1, mods(f011, "^ma"))))), 4))
f200 <- arima(ly, order = c(2, 0, 0), method = "ML"); rr <- polyroot(c(1, -coef(f200)[1:2]))
put("m8.lynx_ar2", r(c(coef(f200)[["ar1"]], coef(f200)[["ar2"]], Mod(rr)[1], 2 * pi / Arg(rr[which.max(Im(rr))])), 4))
put("m8.lynx_ar2_lb20_p", Box.test(residuals(f200), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value)
put("m8.lynx_auto", as.character(auto.arima(ly, stepwise = FALSE, approximation = FALSE, seasonal = FALSE)))

# ---- M9: BJsales (contraste del Nilo) ---------------------------------------
fb <- Arima(BJsales, order = c(1, 1, 1)); ph <- coef(fb)[["ar1"]]; th <- coef(fb)[["ma1"]]; s <- sqrt(fb$sigma2)
psi <- c(1, ARMAtoMA(ar = c(1 + ph, -ph), ma = th, lag.max = 12)); sh <- s * sqrt(cumsum(psi^2))[1:12]
put("m9.bj_psi_limite", r((1 + th) / (1 - ph), 4)); put("m9.bj_psi12", r(psi[13], 4))
put("m9.bj_sigma12_sobre_caminata", r(sh[12] / (s * sqrt(12)), 4))
fn <- Arima(Nile, order = c(1, 1, 1)); pn <- coef(fn)[["ar1"]]; tn <- coef(fn)[["ma1"]]; sn <- sqrt(fn$sigma2)
psin <- c(1, ARMAtoMA(ar = c(1 + pn, -pn), ma = tn, lag.max = 30)); shn <- sn * sqrt(cumsum(psin^2))[1:30]
put("m9.nilo_sigma", r(sn, 3)); put("m9.nilo_sigma30", r(shn[30], 3)); put("m9.nilo_caminata30", r(sn * sqrt(30), 1))
put("m9.nilo_psi_limite", r((1 + tn) / (1 - pn), 4)); put("m9.nilo_razon_30_1", r(shn[30] / shn[1], 3)); put("m9.raiz30", r(sqrt(30), 2))

# ---- M10: la TRM ------------------------------------------------------------
dtrm <- diff(trm); fw <- arima(trm, order = c(0, 1, 0), method = "ML"); s <- sqrt(fw$sigma2)   # como genera_cap4.R
put("m10.sigma", r(s, 2)); put("m10.sigma2", r(fw$sigma2, 2)); put("m10.semiancho_h1", r(qnorm(0.975) * s, 2))
ult <- tail(as.numeric(trm), 1)
hs <- c(1, 3, 6, 12, 24); z <- qnorm(0.975)   # el capítulo usa z = 1.959964, no 1.96
put("m10.tabla", lapply(hs, function(h) list(h = h, sigma_h = r(s * sqrt(h), 2), semiancho = r(z * s * sqrt(h), 2),
      lo = r(ult - z * s * sqrt(h), 2), hi = r(ult + z * s * sqrt(h), 2), pct = r(100 * z * s * sqrt(h) / ult, 1))))
put("m10.n_cambios_1m", length(dtrm))
put("m10.fuera_1m", sum(abs(dtrm) > qnorm(0.975) * s)); put("m10.fuera_1m_arriba", sum(dtrm > qnorm(0.975) * s))
d12 <- diff(trm, lag = 12)
put("m10.n_cambios_12m", length(d12)); put("m10.fuera_12m", sum(abs(d12) > qnorm(0.975) * s * sqrt(12)))
put("m10.curtosis_1m", r(kurt(dtrm), 2)); put("m10.asimetria_1m", r(skew(dtrm), 2)); put("m10.curtosis_12m", r(kurt(d12), 2))
put("m10.razon_var_3a12", r(sapply(3:12, function(h) var(diff(trm, lag = h)) / (h * var(dtrm))), 3))
put("m10.acf_dif_rezago1", r(acf(dtrm, plot = FALSE)$acf[2], 4))


# ---- M3/M5: cómo trabajan ndiffs y auto.arima con la constante -------------
cuerpo_nd <- deparse(body(forecast::ndiffs))
put("m3.ndiffs_defecto_test", eval(formals(forecast::ndiffs)$test)[1])
put("m3.ndiffs_usa_urdf_drift", any(grepl("ur.df", cuerpo_nd, fixed = TRUE)) && any(grepl("drift", cuerpo_nd, fixed = TRUE)))
put("m3.urdf_lags_defecto", eval(formals(urca::ur.df)$lags))
a2 <- auto.arima(Nile, d = 2, seasonal = FALSE)
put("m5.auto_d2_tiene_deriva", "drift" %in% names(coef(a2)))
tr1 <- capture.output(invisible(auto.arima(Nile, d = 1, trace = TRUE, seasonal = FALSE)))
put("m5.auto_d1_traza_con_deriva", any(grepl("with drift", tr1)))
put("m5.auto_d1_traza_sin_deriva", any(grepl("^ *ARIMA\\([0-9,]+\\) +:", tr1)))
tr2 <- capture.output(invisible(auto.arima(Nile, d = 2, trace = TRUE, seasonal = FALSE)))
put("m5.auto_d2_traza_con_deriva", any(grepl("with drift", tr2)))

# ---- M7: reglas de auto.arima ------------------------------------------------
b_my <- deparse(get("myarima", asNamespace("forecast")))
put("m7.regla_raiz_1_01", any(grepl("minroot < 1 + 0.01", b_my, fixed = TRUE)))
put("m7.regla_approximation", paste(deparse(formals(auto.arima)$approximation), collapse = ""))
raiz_ar <- function(f) { cf <- coef(f); ar <- cf[grepl("^ar", names(cf))]; min(Mod(polyroot(c(1, -ar)))) }
put("m7.raiz_ar_212_sin_deriva", r(raiz_ar(Arima(Nile, order = c(2, 1, 2))), 4))
put("m7.raiz_ar_212_con_deriva", r(raiz_ar(Arima(Nile, order = c(2, 1, 2), include.drift = TRUE)), 4))
put("m7.raiz_ar_212_arima_ml",  r(raiz_ar(arima(Nile, order = c(2, 1, 2), method = "ML")), 4))

# ---- Documentación de R (fuente de los datos y de las referencias) ---------
ayuda <- function(tema, paquete) {
  x <- capture.output(tools::Rd2txt(utils:::.getHelpFile(do.call(help, list(tema, package = paquete))), options = list(underline_titles = FALSE)))
  gsub("\\s+", " ", paste(x, collapse = " "))
}
put("doc.nile", ayuda("Nile", "datasets")); put("doc.bjsales", ayuda("BJsales", "datasets"))
put("doc.lynx", ayuda("lynx", "datasets")); put("doc.airpassengers", ayuda("AirPassengers", "datasets"))
put("doc.arima", ayuda("arima", "stats")); put("doc.pptest", ayuda("PP.test", "stats"))
put("doc.citation_forecast", gsub("\\s+", " ", paste(capture.output(print(citation("forecast"), style = "text")), collapse = " ")))

dir.create(dirname(salida), showWarnings = FALSE, recursive = TRUE)
writeLines(toJSON(out, auto_unbox = TRUE, digits = NA, pretty = TRUE, null = "null"), salida, useBytes = TRUE)
cat("Listo:", salida, "\n")
