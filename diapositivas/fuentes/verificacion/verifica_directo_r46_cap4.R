#!/usr/bin/env Rscript
# Cifras de las diapositivas del capítulo 4 que NO están en los JSON entregados
# (directo_cap4.json y regenerado_cap4_arima.json salieron de R 4.3.3) o que ahí
# aparecen redondeadas a 4 decimales. Se calculan aquí desde los datos crudos con el
# R de quien ejecute el guion y se guardan CON EL ENTORNO, para que el informe diga
# con qué versión se obtuvieron.
#
# Uso, desde la raíz del repositorio:
#   Rscript Htmls_Series/diapositivas/fuentes/verificacion/verifica_directo_r46_cap4.R
# Escribe `directo_r46_cap4.json`. No toca `directo_cap4.json` (el de R 4.3.3).
suppressMessages({library(forecast); library(tseries); library(jsonlite)})

aqui <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
raiz <- normalizePath(file.path(aqui, "../../../.."))
dat <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"))
trm <- ts(dat$trm$valores, start = c(2015, 1), frequency = 12)

out <- list(entorno = list(R = R.version.string,
                           forecast = as.character(packageVersion("forecast")),
                           tseries = as.character(packageVersion("tseries"))))

# --- TRM: p y estadísticos SIN el doble redondeo (el JSON los guarda a 4 decimales) ---
adf_n <- adf.test(trm)
kpss_d1 <- suppressWarnings(kpss.test(diff(trm)))
out$trm.adf_nivel_p <- unname(adf_n$p.value)
out$trm.adf_nivel_stat <- unname(adf_n$statistic)
out$trm.kpss_d1_stat <- unname(kpss_d1$statistic)

# --- Nilo: búsqueda exhaustiva de auto.arima, TODOS los candidatos (no solo los cinco primeros) ---
traza <- capture.output(auto.arima(Nile, stepwise = FALSE, approximation = FALSE, trace = TRUE))
lin <- grep("^ ARIMA", traza, value = TRUE)
nombre <- trimws(sub(":.*", "", lin))
aicc_traza <- as.numeric(sub(".*: *", "", lin))
o <- order(aicc_traza)
out$nilo.exhaustiva.n_modelos <- length(lin)
out$nilo.exhaustiva.a_menos_de_2 <- sum(aicc_traza - min(aicc_traza) < 2)
out$nilo.exhaustiva.orden <- nombre[o][1:8]
# AICc con todos los decimales de los siete primeros, reajustados con Arima()
ajusta <- function(orden, deriva) Arima(Nile, order = orden, include.drift = deriva)$aicc
mods <- list(list(c(1, 1, 1), FALSE), list(c(1, 1, 1), TRUE), list(c(0, 1, 2), FALSE), list(c(0, 1, 2), TRUE),
             list(c(0, 1, 1), FALSE), list(c(2, 1, 1), FALSE), list(c(1, 1, 2), FALSE))
raw <- vapply(mods, function(m) ajusta(m[[1]], m[[2]]), numeric(1))
out$nilo.exhaustiva.aicc_siete <- raw
out$nilo.exhaustiva.delta_siete <- raw - raw[1]

# --- TRM: cuántos candidatos evalúa la búsqueda exhaustiva con y sin parte estacional ---
cuenta <- function(seas) length(grep("^ ARIMA", capture.output(
  auto.arima(trm, stepwise = FALSE, approximation = FALSE, trace = TRUE, seasonal = seas))))
out$trm.auto.n_modelos_con_estacional <- cuenta(TRUE)
out$trm.auto.n_modelos_sin_estacional <- cuenta(FALSE)

# --- Nilo: raíz AR del ARIMA(2,1,2) con Arima() (depende del estimador y de la versión) ---
raiz_ar <- function(deriva) min(Mod(polyroot(c(1, -Arima(Nile, order = c(2, 1, 2), include.drift = deriva)$model$phi))))
out$nilo.raiz_ar_212_sin_deriva <- raiz_ar(FALSE)
out$nilo.raiz_ar_212_con_deriva <- raiz_ar(TRUE)

# --- Valores por defecto de las funciones (tabla «Cada programa trata la constante») ---
out$Arima.include_mean_por_defecto <- eval(formals(Arima)$include.mean)
out$Arima.include_drift_por_defecto <- eval(formals(Arima)$include.drift)

# --- ¿Cuánto vale el PP.test cuando SÍ hay raíz unitaria y un MA fuerte y negativo? ---
# Mismo ARIMA(1,1,1) que el del Nilo (phi = 0.2544, theta = -0.8741, n = 100). Semilla 2026, 1 000 réplicas.
set.seed(2026)
B <- 1000; rej_pp <- 0; rej_adf <- 0
for (b in seq_len(B)) {
  x <- 900 + cumsum(arima.sim(list(ar = 0.2544, ma = -0.8741), n = 100))
  if (suppressWarnings(PP.test(x)$p.value) < 0.05) rej_pp <- rej_pp + 1
  if (suppressWarnings(adf.test(x, k = 4)$p.value) < 0.05) rej_adf <- rej_adf + 1
}
out$sim_raiz_unitaria.replicas <- B
out$sim_raiz_unitaria.pp_rechaza <- rej_pp / B
out$sim_raiz_unitaria.adf_k4_rechaza <- rej_adf / B

# --- Puente estacional: «el mejor no estacional» depende del tope de p + q ---
lap <- log(AirPassengers)
rho12 <- function(f) unname(acf(residuals(f), plot = FALSE, lag.max = 24)$acf[13, 1, 1])
f_def <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
f_amplio <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE,
                       max.p = 8, max.q = 8, max.order = 16)
out$puente.mejor_por_defecto <- as.character(f_def)
out$puente.mejor_por_defecto_rho12 <- rho12(f_def)
out$puente.mejor_amplio <- as.character(f_amplio)
out$puente.mejor_amplio_rho12 <- rho12(f_amplio)

# --- Documentación de R de esta versión (la cita de AirPassengers cambió entre 4.3.3 y 4.6) ---
ayuda <- function(tema) paste(capture.output(tools::Rd2txt(utils:::.getHelpFile(help(tema, package = "datasets")),
                                                            options = list(underline_titles = FALSE))), collapse = " ")
out$doc.airpassengers <- gsub("\\s+", " ", ayuda("AirPassengers"))

write_json(out, file.path(aqui, "directo_r46_cap4.json"), auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat("escrito directo_r46_cap4.json con", R.version.string, "\n")
