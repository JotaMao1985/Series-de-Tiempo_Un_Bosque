# ============================================================================
# genera_datos.R — Precálculos para el material de Series de Tiempo (UnBosque)
#
# Genera, en la carpeta salidas/:
#   1. datos_series.js / datos_series.json : series incrustables en los
#      capítulos (AirPassengers, co2, Nile, USAccDeaths, TRM mensual).
#   2. cap4_rejilla_arima.json : rejilla ARIMA(p,d,q), p,d,q en {0,1,2},
#      ajustada sobre el caudal anual del Nilo (caso del Capítulo 4).
#   3. cap6_pronostico.json : pronóstico SARIMA con bandas 80/95, métricas
#      frente a métodos de referencia y validación de origen móvil sobre
#      AirPassengers (caso del Capítulo 6).
#
# Dependencias: R base + jsonlite. NO usa forecast/fpp3 a propósito, para que
# el precálculo corra en cualquier instalación de R.
# Uso:  Rscript genera_datos.R      (desde la carpeta precalculo/)
# ============================================================================

suppressMessages(library(jsonlite))

args_dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
if (is.na(args_dir) || args_dir == "") args_dir <- "."
dir_salidas <- file.path(args_dir, "salidas")
dir.create(dir_salidas, showWarnings = FALSE, recursive = TRUE)

fecha_corte <- format(Sys.Date(), "%Y-%m-%d")

# ----------------------------------------------------------------------------
# 1. Series incrustables
# ----------------------------------------------------------------------------

serial_ts <- function(x, nombre, descripcion, unidad, fuente) {
  list(
    nombre      = nombre,
    descripcion = descripcion,
    unidad      = unidad,
    fuente      = fuente,
    inicio      = as.integer(start(x)),
    frecuencia  = as.integer(frequency(x)),
    valores     = round(as.numeric(x), 3)
  )
}

series <- list(
  airpassengers = serial_ts(
    AirPassengers, "AirPassengers",
    "Pasajeros mensuales de aerolíneas internacionales, 1949-1960",
    "miles de pasajeros",
    "Box, Jenkins & Reinsel (datasets de R)"
  ),
  co2 = serial_ts(
    co2, "co2",
    "Concentración mensual de CO2 en Mauna Loa, 1959-1997",
    "ppm",
    "Scripps / Keeling (datasets de R)"
  ),
  nilo = serial_ts(
    Nile, "Nile",
    "Caudal anual del río Nilo en Asuán, 1871-1970",
    "10^8 m^3",
    "Cobb (1978) (datasets de R)"
  ),
  usaccdeaths = serial_ts(
    USAccDeaths, "USAccDeaths",
    "Muertes accidentales mensuales en EE.UU., 1973-1978",
    "personas",
    "datasets de R"
  )
)

# --- TRM mensual (promedio del mes) desde datos.gov.co (Socrata) ------------
trm_ok <- FALSE
tryCatch({
  base_url <- "https://www.datos.gov.co/resource/32sa-8pi3.json"
  consulta <- paste0(
    "?$select=vigenciadesde,valor",
    "&$where=vigenciadesde%20%3E=%20%272015-01-01T00:00:00.000%27",
    "&$order=vigenciadesde&$limit=20000"
  )
  con <- url(paste0(base_url, consulta))
  crudo <- suppressWarnings(readLines(con, warn = FALSE))
  close(con)
  trm_diaria <- fromJSON(paste(crudo, collapse = ""))
  stopifnot(nrow(trm_diaria) > 1000)

  trm_diaria$valor <- as.numeric(trm_diaria$valor)
  trm_diaria$mes <- substr(trm_diaria$vigenciadesde, 1, 7)

  # Promedio mensual; se descarta el mes en curso (incompleto)
  mes_actual <- format(Sys.Date(), "%Y-%m")
  agregada <- aggregate(valor ~ mes, data = trm_diaria[trm_diaria$mes < mes_actual, ], FUN = mean)
  agregada <- agregada[order(agregada$mes), ]

  # Verificar que la secuencia de meses sea continua
  meses_esperados <- format(seq(as.Date(paste0(agregada$mes[1], "-01")),
                                as.Date(paste0(agregada$mes[nrow(agregada)], "-01")),
                                by = "month"), "%Y-%m")
  stopifnot(identical(agregada$mes, meses_esperados))

  inicio_anio <- as.integer(substr(agregada$mes[1], 1, 4))
  inicio_mes  <- as.integer(substr(agregada$mes[1], 6, 7))
  trm_ts <- ts(round(agregada$valor, 2), start = c(inicio_anio, inicio_mes), frequency = 12)

  series$trm <- serial_ts(
    trm_ts, "TRM mensual",
    paste0("Tasa Representativa del Mercado (COP/USD), promedio mensual, ",
           agregada$mes[1], " a ", agregada$mes[nrow(agregada)]),
    "COP por USD",
    paste0("Superintendencia Financiera de Colombia vía datos.gov.co (consulta: ", fecha_corte, ")")
  )
  trm_ok <- TRUE
  cat("TRM descargada:", nrow(agregada), "meses (", agregada$mes[1], "a",
      agregada$mes[nrow(agregada)], ")\n")
}, error = function(e) {
  cat("AVISO: no se pudo descargar la TRM (", conditionMessage(e),
      "). El archivo se genera sin esa serie.\n")
})

series$metadatos <- list(
  generado    = fecha_corte,
  generador   = "precalculo/genera_datos.R",
  descripcion = "Series incrustables para los capitulos de Series de Tiempo (UnBosque)"
)

json_series <- toJSON(series, auto_unbox = TRUE, digits = NA, pretty = FALSE)
writeLines(paste0("const SERIES_DATOS = ", json_series, ";"),
           file.path(dir_salidas, "datos_series.js"))
writeLines(json_series, file.path(dir_salidas, "datos_series.json"))
cat("Escrito: datos_series.js / datos_series.json\n")

# ----------------------------------------------------------------------------
# 2. Capítulo 4: rejilla ARIMA(p,d,q) sobre el Nilo
# ----------------------------------------------------------------------------

metricas_arima <- function(fit, n_efectivo, p, q) {
  k    <- length(coef(fit)) + 1  # parametros estimados + sigma^2
  aic  <- AIC(fit)
  aicc <- aic + (2 * k * (k + 1)) / (n_efectivo - k - 1)
  bic  <- aic + (log(n_efectivo) - 2) * k
  res  <- as.numeric(residuals(fit))
  lb   <- Box.test(res, lag = 10, type = "Ljung-Box", fitdf = p + q)
  list(
    aic = round(aic, 2), aicc = round(aicc, 2), bic = round(bic, 2),
    ljung_box_p = round(unname(lb$p.value), 4),
    acf_residuales = round(as.numeric(acf(res, lag.max = 20, plot = FALSE)$acf[-1]), 4)
  )
}

serie_nilo <- Nile
n_nilo <- length(serie_nilo)
rejilla <- list()
for (p in 0:2) for (d in 0:2) for (q in 0:2) {
  clave <- sprintf("%d%d%d", p, d, q)
  resultado <- tryCatch({
    fit <- arima(serie_nilo, order = c(p, d, q), method = "ML")
    m <- metricas_arima(fit, n_nilo - d, p, q)
    c(list(p = p, d = d, q = q, convergio = TRUE), m)
  }, error = function(e) {
    list(p = p, d = d, q = q, convergio = FALSE, error = conditionMessage(e))
  })
  rejilla[[clave]] <- resultado
}

# IMPORTANTE (y contenido del capitulo): el AIC/AICc solo es comparable entre
# modelos con el MISMO orden de diferenciacion d, porque al diferenciar cambia
# la serie sobre la que se calcula la verosimilitud. Se reporta el mejor por d.
mejor_por_d <- sapply(0:2, function(dd) {
  sub <- Filter(function(r) isTRUE(r$convergio) && r$d == dd, rejilla)
  names(sub)[which.min(vapply(sub, function(r) r$aicc, numeric(1)))]
})
names(mejor_por_d) <- paste0("d", 0:2)

# Eleccion de d: prueba de Phillips-Perron (H0: raiz unitaria) de R base
pp_nivel <- PP.test(serie_nilo)
pp_dif1  <- PP.test(diff(serie_nilo))

# Banda de confianza para la ACF de residuales: +/- 1.96/sqrt(n)
cap4 <- list(
  serie = "nilo",
  descripcion = paste0(
    "Rejilla ARIMA(p,d,q) con p,d,q en {0,1,2} ajustada por maxima verosimilitud ",
    "(stats::arima) sobre el caudal anual del Nilo. AICc y BIC calculados a partir ",
    "del AIC con n efectivo = n - d. El AICc SOLO es comparable entre modelos con ",
    "el mismo d; usar mejor_aicc_por_d, nunca un minimo global."
  ),
  n = n_nilo,
  banda_acf = round(1.96 / sqrt(n_nilo), 4),
  max_rezago_acf = 20,
  mejor_aicc_por_d = as.list(mejor_por_d),
  prueba_raiz_unitaria = list(
    prueba = "Phillips-Perron (stats::PP.test), H0: raiz unitaria",
    p_nivel = round(unname(pp_nivel$p.value), 4),
    p_primera_diferencia = round(unname(pp_dif1$p.value), 4)
  ),
  modelos = rejilla,
  metadatos = list(generado = fecha_corte, generador = "precalculo/genera_datos.R")
)
write_json(cap4, file.path(dir_salidas, "cap4_rejilla_arima.json"),
           auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat("Escrito: cap4_rejilla_arima.json (mejor AICc por d:",
    paste(names(mejor_por_d), mejor_por_d, sep = "=", collapse = ", "), ")\n")

# ----------------------------------------------------------------------------
# 3. Capítulo 6: pronóstico, métricas y origen móvil sobre AirPassengers
# ----------------------------------------------------------------------------

# Modelo "airline": SARIMA(0,1,1)(0,1,1)[12] sobre log(AirPassengers)
serie_ap  <- AirPassengers
log_ap    <- log(serie_ap)
n_ap      <- length(serie_ap)        # 144
n_train   <- 120                     # 1949-1958
h_test    <- n_ap - n_train         # 24 (1959-1960)

entren <- ts(log_ap[1:n_train], start = start(log_ap), frequency = 12)
reales_test <- as.numeric(serie_ap[(n_train + 1):n_ap])

ajusta_airline <- function(y) {
  arima(y, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12),
        method = "ML")
}

fit_air <- ajusta_airline(entren)
pron    <- predict(fit_air, n.ahead = h_test)
z80 <- qnorm(0.90); z95 <- qnorm(0.975)

puntual <- exp(as.numeric(pron$pred))
li80 <- exp(as.numeric(pron$pred) - z80 * as.numeric(pron$se))
ls80 <- exp(as.numeric(pron$pred) + z80 * as.numeric(pron$se))
li95 <- exp(as.numeric(pron$pred) - z95 * as.numeric(pron$se))
ls95 <- exp(as.numeric(pron$pred) + z95 * as.numeric(pron$se))

rmse <- function(e) sqrt(mean(e^2))
mae  <- function(e) mean(abs(e))
mape <- function(e, real) mean(abs(e / real)) * 100

met <- function(pred, real) {
  e <- real - pred
  list(rmse = round(rmse(e), 2), mae = round(mae(e), 2),
       mape = round(mape(e, real), 2))
}

# Métodos de referencia sobre la escala original
ultimo <- as.numeric(serie_ap[n_train])
pron_naive <- rep(ultimo, h_test)
ult_anio <- as.numeric(serie_ap[(n_train - 11):n_train])
pron_snaive <- rep(ult_anio, length.out = h_test)
media_train <- mean(as.numeric(serie_ap[1:n_train]))
pron_media <- rep(media_train, h_test)
pendiente_deriva <- (ultimo - as.numeric(serie_ap[1])) / (n_train - 1)
pron_deriva <- ultimo + pendiente_deriva * seq_len(h_test)

# Validación de origen móvil: ventana expansiva, refit en cada origen, h = 1..12
origenes <- 96:(n_ap - 12)   # 96..132: 37 orígenes, siempre con 12 reales adelante
lista_origenes <- list()
errores_horizonte <- matrix(NA_real_, nrow = length(origenes), ncol = 12)
for (i in seq_along(origenes)) {
  To <- origenes[i]
  y_o <- ts(log_ap[1:To], start = start(log_ap), frequency = 12)
  fit_o <- ajusta_airline(y_o)
  pron_o <- exp(as.numeric(predict(fit_o, n.ahead = 12)$pred))
  reales_o <- as.numeric(serie_ap[(To + 1):(To + 12)])
  errores_horizonte[i, ] <- reales_o - pron_o
  lista_origenes[[i]] <- list(
    T = To,
    pronostico = round(pron_o, 1),
    reales = round(reales_o, 1)
  )
}
rmse_horizonte <- round(apply(errores_horizonte, 2, function(e) sqrt(mean(e^2))), 2)

cap6 <- list(
  serie = "airpassengers",
  descripcion = paste0(
    "Modelo airline SARIMA(0,1,1)(0,1,1)[12] sobre log(AirPassengers), ajustado con ",
    "stats::arima (ML). Entrenamiento 1949-1958 (120 obs.), prueba 1959-1960 (24 obs.). ",
    "Intervalos construidos en escala log y transformados con exp (el puntual es la mediana). ",
    "Origen movil: ventana expansiva, reajuste en cada origen T=96..132, horizonte 12."
  ),
  n = n_ap,
  n_entrenamiento = n_train,
  h = h_test,
  coeficientes = as.list(round(coef(fit_air), 4)),
  pronostico = list(
    puntual = round(puntual, 1),
    li80 = round(li80, 1), ls80 = round(ls80, 1),
    li95 = round(li95, 1), ls95 = round(ls95, 1)
  ),
  reales_prueba = round(reales_test, 1),
  metricas = list(
    sarima  = met(puntual, reales_test),
    naive   = met(pron_naive, reales_test),
    snaive  = met(pron_snaive, reales_test),
    media   = met(pron_media, reales_test),
    deriva  = met(pron_deriva, reales_test)
  ),
  origen_movil = list(
    origenes = lista_origenes,
    rmse_por_horizonte = rmse_horizonte
  ),
  metadatos = list(generado = fecha_corte, generador = "precalculo/genera_datos.R")
)
write_json(cap6, file.path(dir_salidas, "cap6_pronostico.json"),
           auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat("Escrito: cap6_pronostico.json\n")

# ----------------------------------------------------------------------------
# 4. Capítulo 1: descomposición clásica y STL de AirPassengers
#    (el navegador solo dibuja; STL y decompose se calculan aquí en R)
# ----------------------------------------------------------------------------

# Etiquetas de mes YYYY-MM para el eje
fechas_ap <- format(seq(as.Date("1949-01-01"), by = "month", length.out = n_ap), "%Y-%m")

# Descomposición clásica multiplicativa (medias móviles centradas)
dc <- decompose(serie_ap, type = "multiplicative")

# STL sobre log(AirPassengers) -> componentes aditivos en escala log
st <- stl(log_ap, s.window = "periodic")
stl_comp <- st$time.series
stl_tend <- as.numeric(stl_comp[, "trend"])
stl_seas <- as.numeric(stl_comp[, "seasonal"])
stl_rem  <- as.numeric(stl_comp[, "remainder"])

# Fuerza de tendencia y estacionalidad (Hyndman & Athanasopoulos, FPP3 3.6)
FT <- max(0, 1 - var(stl_rem) / var(stl_tend + stl_rem))
FS <- max(0, 1 - var(stl_rem) / var(stl_seas + stl_rem))

# Índices estacionales multiplicativos (clásicos), promedio por mes
indices_mes <- round(as.numeric(dc$figure), 4)  # 12 valores, Ene..Dic

cap1 <- list(
  serie = "airpassengers",
  descripcion = paste0(
    "Descomposicion de AirPassengers. Clasica multiplicativa con stats::decompose ",
    "(tendencia por media movil centrada de orden 12; NA en los extremos como null). ",
    "STL con stats::stl sobre log(AirPassengers): componentes aditivos en escala log. ",
    "Fuerza de tendencia/estacionalidad segun FPP3 seccion 3.6, calculada sobre STL."
  ),
  n = n_ap,
  fechas = fechas_ap,
  observado = round(as.numeric(serie_ap), 1),
  clasica_multiplicativa = list(
    tendencia = round(as.numeric(dc$trend), 4),
    estacional = round(as.numeric(dc$seasonal), 4),
    residuo = round(as.numeric(dc$random), 4)
  ),
  indices_estacionales = indices_mes,
  stl_log = list(
    escala = "log",
    tendencia = round(stl_tend, 4),
    estacional = round(stl_seas, 4),
    residuo = round(stl_rem, 4)
  ),
  fuerza_tendencia = round(FT, 3),
  fuerza_estacional = round(FS, 3),
  metadatos = list(generado = fecha_corte, generador = "precalculo/genera_datos.R")
)
write_json(cap1, file.path(dir_salidas, "cap1_descomposicion.json"),
           auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null")

# Bloque JS listo para incrustar en el capítulo 1 (serie + descomposición)
js_cap1 <- paste0(
  "// Generado por precalculo/genera_datos.R el ", fecha_corte, "\n",
  "// AirPassengers y su descomposicion (clasica multiplicativa + STL sobre log).\n",
  "const DATOS_CAP1 = ",
  toJSON(cap1, auto_unbox = TRUE, digits = NA, na = "null"), ";\n"
)
writeLines(js_cap1, file.path(dir_salidas, "cap1_datos.js"))
cat("Escrito: cap1_descomposicion.json / cap1_datos.js (FT =", round(FT, 3),
    ", FS =", round(FS, 3), ")\n")

cat("\nResumen:\n")
cat(" - Series incrustadas:", paste(setdiff(names(series), "metadatos"), collapse = ", "), "\n")
cat(" - Mejor ARIMA por AICc y por d (Nilo):",
    paste(names(mejor_por_d), mejor_por_d, sep = "=", collapse = ", "), "\n")
cat(" - RMSE prueba SARIMA:", cap6$metricas$sarima$rmse,
    "| naive:", cap6$metricas$naive$rmse,
    "| snaive:", cap6$metricas$snaive$rmse, "\n")
if (!trm_ok) cat(" - PENDIENTE: reintentar la descarga de la TRM.\n")
cat("Listo.\n")
