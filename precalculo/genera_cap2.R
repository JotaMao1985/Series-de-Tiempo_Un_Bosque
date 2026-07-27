# ============================================================================
# genera_cap2.R — Precálculos del Capítulo 2 (estacionariedad, ACF/PACF,
#                 diferenciación y transformaciones)
#
# Genera salidas/cap2_estacionariedad.json y salidas/cap2_datos.js con:
#   - 8 series de trabajo (ruido blanco, caminata aleatoria, AirPassengers y
#     sus transformaciones, TRM y su primera diferencia)
#   - ACF y PACF muestrales hasta el rezago 24 de cada una
#   - Pruebas de raíz unitaria: ADF (tseries) y KPSS de nivel y de tendencia
#   - Número sugerido de diferencias: ndiffs / nsdiffs (forecast)
#   - Lambda de Box-Cox por el método de Guerrero (forecast)
#   - Tabla de varianzas por nivel de diferenciación (sobrediferenciación)
#
# Script APARTE de genera_datos.R a propósito: aquel vuelve a descargar la TRM
# y a reajustar los 37 modelos del origen móvil del capítulo 6. Aquí solo
# leemos su salida ya generada (salidas/datos_series.json) y añadimos lo nuevo.
#
# Dependencias: jsonlite, tseries, forecast.
# Uso:  Rscript genera_cap2.R      (desde la carpeta precalculo/)
# ============================================================================

suppressMessages({
  library(jsonlite)
  library(tseries)
  library(forecast)
})

# R arranca aqui con LC_CTYPE = "C", y entonces jsonlite trata los bytes UTF-8
# de las tildes como caracteres sueltos y los escribe en el JSON como <c3><ad>.
# En el navegador eso se lee como marcado desconocido y la palabra pierde la
# tilde ("dias" en vez de "dias" con tilde). Hay que forzar la configuracion
# regional ANTES de generar nada.
locale_ok <- suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"))
if (!isTRUE(l10n_info()$"UTF-8")) {
  warning("No se pudo activar una configuracion regional UTF-8: las tildes de ",
          "las cadenas del JSON saldran mal. Prueba a ejecutar con ",
          "LC_ALL=en_US.UTF-8 Rscript ...")
}

args_dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
if (is.na(args_dir) || args_dir == "") args_dir <- "."
dir_salidas <- file.path(args_dir, "salidas")
stopifnot(dir.exists(dir_salidas))

fecha_corte <- format(Sys.Date(), "%Y-%m-%d")
MAX_REZAGO <- 24

# ----------------------------------------------------------------------------
# 0. Series de partida
# ----------------------------------------------------------------------------

# TRM: se lee de la salida de genera_datos.R (no se vuelve a descargar)
sd_json <- fromJSON(file.path(dir_salidas, "datos_series.json"), simplifyVector = TRUE)
stopifnot(!is.null(sd_json$trm))
trm <- ts(as.numeric(sd_json$trm$valores),
          start = as.integer(sd_json$trm$inicio), frequency = 12)
cat("TRM leída de datos_series.json:", length(trm), "meses ·",
    sd_json$trm$descripcion, "\n")

# Ruido blanco y caminata aleatoria: misma realización siempre (semilla fija).
# La caminata es el acumulado del MISMO ruido: así el capítulo puede decir
# "esta caminata es la suma acumulada de aquel ruido blanco" y es literal.
set.seed(2026)
ruido_blanco <- rnorm(200)
caminata     <- cumsum(ruido_blanco)

ap      <- AirPassengers
log_ap  <- log(ap)
d_logap <- diff(log_ap)                    # diferencia regular
dd_logap <- diff(d_logap, lag = 12)        # + diferencia estacional
d_trm   <- diff(trm)

# ----------------------------------------------------------------------------
# 1. Ayudantes
# ----------------------------------------------------------------------------

# ACF y PACF muestrales. stats::acf divide por n (no por n-k) y stats::pacf
# resuelve Durbin-Levinson sobre la ACF muestral: son exactamente las mismas
# definiciones que implementa el capítulo en JavaScript.
correlogramas <- function(x, max_rezago = MAX_REZAGO) {
  n <- length(x)
  a <- acf(x, lag.max = max_rezago, plot = FALSE)$acf
  p <- pacf(x, lag.max = max_rezago, plot = FALSE)$acf
  list(
    n     = n,
    banda = round(1.96 / sqrt(n), 4),
    acf   = round(as.numeric(a)[-1], 4),   # se descarta el rezago 0 (= 1)
    pacf  = round(as.numeric(p), 4)
  )
}

# ADF de tseries: H0 = hay raíz unitaria (no estacionaria).
# Especificación: deriva + tendencia, k = trunc((n-1)^(1/3)) rezagos.
# adf.test avisa cuando el p-valor cae fuera de la tabla de Banerjee et al.;
# capturamos ese aviso para reportarlo en vez de esconderlo.
prueba_adf <- function(x) {
  aviso <- NA_character_
  r <- withCallingHandlers(
    adf.test(x),
    warning = function(w) { aviso <<- conditionMessage(w); invokeRestart("muffleWarning") }
  )
  list(
    estadistico = round(unname(r$statistic), 4),
    rezagos     = unname(r$parameter),
    p_valor     = round(unname(r$p.value), 4),
    fuera_tabla = !is.na(aviso),
    aviso       = if (is.na(aviso)) NULL else aviso
  )
}

# KPSS de tseries: H0 = la serie ES estacionaria (hipótesis OPUESTA a la del
# ADF). null="Level" contrasta estacionariedad en nivel; "Trend", alrededor de
# una tendencia determinista. lshort=TRUE => l = trunc(4*(n/100)^0.25).
prueba_kpss <- function(x, nulo) {
  aviso <- NA_character_
  r <- withCallingHandlers(
    kpss.test(x, null = nulo),
    warning = function(w) { aviso <<- conditionMessage(w); invokeRestart("muffleWarning") }
  )
  list(
    estadistico = round(unname(r$statistic), 4),
    truncamiento = unname(r$parameter),
    p_valor     = round(unname(r$p.value), 4),
    fuera_tabla = !is.na(aviso),
    aviso       = if (is.na(aviso)) NULL else aviso
  )
}

# Bloque completo por serie
analiza <- function(x, clave, nombre, descripcion, estacional_esperada) {
  cor <- correlogramas(x)
  n <- length(x)
  bloque <- list(
    clave = clave,
    nombre = nombre,
    descripcion = descripcion,
    n = n,
    banda = cor$banda,
    valores = round(as.numeric(x), 5),
    acf = cor$acf,
    pacf = cor$pacf,
    media = round(mean(x), 4),
    desv = round(sd(x), 4),
    varianza = round(var(as.numeric(x)), 6),
    adf = prueba_adf(x),
    kpss_nivel = prueba_kpss(x, "Level"),
    kpss_tendencia = prueba_kpss(x, "Trend"),
    ndiffs = unname(ndiffs(x))
  )
  # nsdiffs solo tiene sentido con frecuencia > 1 y exige al menos 2 periodos
  if (estacional_esperada && frequency(x) > 1 && n >= 2 * frequency(x)) {
    bloque$nsdiffs <- unname(nsdiffs(x))
  }
  bloque
}

# ----------------------------------------------------------------------------
# 2. Las ocho series de trabajo del capítulo
# ----------------------------------------------------------------------------

series_cap2 <- list(
  analiza(ts(ruido_blanco), "ruido_blanco", "Ruido blanco simulado",
          "200 valores i.i.d. N(0,1), set.seed(2026). Caso de referencia: ACF y PACF sin estructura.",
          FALSE),
  analiza(ts(caminata), "caminata", "Caminata aleatoria simulada",
          "Suma acumulada del MISMO ruido blanco anterior. Caso de referencia de serie no estacionaria: ACF que decae muy lentamente.",
          FALSE),
  analiza(ap, "airpassengers", "AirPassengers (nivel)",
          "Pasajeros mensuales 1949-1960: tendencia creciente y estacionalidad cuya amplitud crece con el nivel.",
          TRUE),
  analiza(log_ap, "log_airpassengers", "log(AirPassengers)",
          "El logaritmo estabiliza la varianza: la amplitud estacional deja de crecer, pero la tendencia sigue ahi.",
          TRUE),
  analiza(d_logap, "d_log_airpassengers", "Diferencia regular de log(AirPassengers)",
          "Una diferencia regular elimina la tendencia; los picos en los rezagos 12 y 24 delatan la estacionalidad que queda.",
          TRUE),
  analiza(dd_logap, "dd_log_airpassengers", "Diferencia regular y estacional de log(AirPassengers)",
          "Diferencia regular seguida de diferencia estacional (lag 12): la serie del modelo 'airline'.",
          TRUE),
  analiza(trm, "trm", "TRM mensual (COP/USD)",
          sd_json$trm$descripcion,
          TRUE),
  analiza(d_trm, "d_trm", "Primera diferencia de la TRM",
          "Cambio mensual de la TRM en pesos. La diferencia convierte una serie con raiz unitaria en una estacionaria.",
          TRUE)
)
names(series_cap2) <- vapply(series_cap2, function(s) s$clave, character(1))

# ----------------------------------------------------------------------------
# 3. Transformaciones: lambda de Box-Cox (Guerrero) y tabla de varianzas
# ----------------------------------------------------------------------------

lambda_ap  <- BoxCox.lambda(ap,  method = "guerrero")
lambda_trm <- BoxCox.lambda(trm, method = "guerrero")

# ¿Cuánto se pierde por usar el logaritmo en vez del lambda óptimo? El capítulo
# recomienda log, así que hay que poner el precio sobre la mesa en lugar de
# afirmar que "da casi igual". Se evalúa el propio criterio de Guerrero
# (forecast:::guer.cv, menor es mejor) en tres puntos y se mide el ancho de la
# zona donde el criterio se queda a menos del 20% de su mínimo.
cv_guerrero <- function(x, lam) forecast:::guer.cv(lam, x)
cv_sin  <- cv_guerrero(ap, 1)          # sin transformar
cv_log  <- cv_guerrero(ap, 0)          # logaritmo
cv_opt  <- cv_guerrero(ap, lambda_ap)  # optimo
rejilla_lam <- seq(-1, 2, by = 0.005)
buenos <- rejilla_lam[sapply(rejilla_lam, function(L) cv_guerrero(ap, L)) <= 1.2 * cv_opt]

costo_del_log <- list(
  descripcion = paste0(
    "Criterio de Guerrero (menor es mejor) evaluado en tres lambdas, para ",
    "cuantificar lo que cuesta preferir el logaritmo al lambda optimo."
  ),
  cv_sin_transformar = round(cv_sin, 5),
  cv_logaritmo = round(cv_log, 5),
  cv_optimo = round(cv_opt, 5),
  exceso_del_log_sobre_el_optimo_pct = round(100 * (cv_log / cv_opt - 1)),
  mejora_captada_por_el_log_pct = round(100 * (cv_sin - cv_log) / (cv_sin - cv_opt), 1),
  zona_dentro_del_20pct = c(round(min(buenos), 2), round(max(buenos), 2))
)

# Sobrediferenciación: diferenciar de más NO estabiliza más. Dos huellas
# delatoras, y el capítulo cita ambas: (1) la varianza deja de bajar y vuelve a
# subir; (2) aparece autocorrelación negativa fuerte en el rezago 1 (la segunda
# diferencia induce un MA con raíz unitaria, cuya ACF teórica en el rezago 1
# tiende a -0.5).
tabla_sobrediferenciacion <- function(x, digitos) {
  lapply(0:3, function(d) {
    y <- if (d == 0) as.numeric(x) else as.numeric(diff(x, differences = d))
    list(d = d,
         n = length(y),
         varianza = round(var(y), digitos),
         acf1 = round(acf(y, lag.max = 1, plot = FALSE)$acf[2], 4))
  })
}
varianzas_dif     <- tabla_sobrediferenciacion(log_ap, 6)
varianzas_dif_trm <- tabla_sobrediferenciacion(trm, 4)

# ----------------------------------------------------------------------------
# 3bis. La trampa de aplicar el ADF a una serie estacional
#
# Hallazgo de la auditoría: adf.test(AirPassengers) devuelve -7.32 con p = 0.01,
# es decir, RECHAZA la raíz unitaria en una serie con tendencia y estacionalidad
# evidentes. No es un error de la prueba: adf.test usa por defecto
# k = trunc((n-1)^(1/3)) = 5 rezagos, MENOS que el periodo estacional m = 12,
# de modo que la oscilación anual —que es fuertemente reversiva a la media— se
# queda en el residuo y el ADF la lee como evidencia de estacionariedad.
# Aquí se documenta con tres evidencias: (a) el resultado cambia de signo al
# alargar k hasta cubrir un ciclo; (b) desaparece al desestacionalizar; (c) una
# simulación Monte Carlo muestra que el falso rechazo crece con la amplitud
# estacional aunque la serie SÍ tenga raíz unitaria por construcción.
# ----------------------------------------------------------------------------

adf_por_k <- lapply(c(5, 11, 12, 13), function(kk) {
  r <- suppressWarnings(adf.test(log_ap, k = kk))
  list(k = kk,
       estadistico = round(unname(r$statistic), 4),
       p_valor = round(unname(r$p.value), 4))
})

log_ap_sa <- seasadj(stl(log_ap, s.window = "periodic"))
adf_sa    <- prueba_adf(log_ap_sa)
kpss_sa   <- prueba_kpss(log_ap_sa, "Trend")
adf_estacional_pura <- suppressWarnings(
  adf.test(stl(log_ap, s.window = "periodic")$time.series[, "seasonal"])
)

# Monte Carlo: caminata aleatoria + seno estacional. H0 (raíz unitaria) es
# CIERTA por construcción, así que un test bien calibrado debería rechazar
# alrededor del 5% de las veces, sea cual sea la amplitud.
N_REP <- 500
montecarlo <- lapply(c(0, 0.5, 1, 2, 4), function(amp) {
  set.seed(7)  # misma semilla por amplitud: solo cambia la estacionalidad
  rechazos <- sum(replicate(N_REP, {
    x <- ts(cumsum(rnorm(144)) + amp * sin(2 * pi * (1:144) / 12), frequency = 12)
    suppressWarnings(adf.test(x))$p.value < 0.05
  }))
  list(amplitud = amp,
       tasa_rechazo = round(100 * rechazos / N_REP, 1))
})

trampa_estacionalidad <- list(
  descripcion = paste0(
    "adf.test rechaza la raiz unitaria en AirPassengers porque su k por defecto ",
    "(trunc((n-1)^(1/3)) = 5) es menor que el periodo estacional m = 12. ",
    "Al cubrir un ciclo completo con k, o al desestacionalizar, el rechazo desaparece."
  ),
  k_por_defecto = trunc((length(ap) - 1)^(1/3)),
  periodo_estacional = 12,
  adf_nivel_crudo = list(
    estadistico = round(unname(suppressWarnings(adf.test(ap))$statistic), 4),
    p_valor = round(unname(suppressWarnings(adf.test(ap))$p.value), 4)
  ),
  adf_log_por_k = adf_por_k,
  desestacionalizada = list(
    metodo = "forecast::seasadj(stl(log(AirPassengers), s.window='periodic'))",
    adf = adf_sa,
    kpss_tendencia = kpss_sa
  ),
  adf_componente_estacional_pura = list(
    estadistico = round(unname(adf_estacional_pura$statistic), 4),
    p_valor = round(unname(adf_estacional_pura$p.value), 4)
  ),
  montecarlo = list(
    descripcion = paste0(
      "Caminata aleatoria de 144 pasos mas amplitud*sin(2*pi*t/12). H0 (raiz ",
      "unitaria) es CIERTA por construccion: un test bien calibrado rechazaria ",
      "cerca del 5% de las veces. ", N_REP, " replicas por amplitud, set.seed(7)."
    ),
    n_replicas = N_REP,
    nivel_nominal = 5,
    resultados = montecarlo
  )
)

# ----------------------------------------------------------------------------
# 4. Etiquetas de tiempo para los ejes
# ----------------------------------------------------------------------------

etiquetas_mensuales <- function(x) {
  ini <- start(x)
  format(seq(as.Date(sprintf("%d-%02d-01", ini[1], ini[2])),
             by = "month", length.out = length(x)), "%Y-%m")
}

fechas <- list(
  airpassengers        = etiquetas_mensuales(ap),
  log_airpassengers    = etiquetas_mensuales(log_ap),
  d_log_airpassengers  = etiquetas_mensuales(d_logap),
  dd_log_airpassengers = etiquetas_mensuales(dd_logap),
  trm                  = etiquetas_mensuales(trm),
  d_trm                = etiquetas_mensuales(d_trm)
)

# ----------------------------------------------------------------------------
# 5. Salida
# ----------------------------------------------------------------------------

cap2 <- list(
  descripcion = paste0(
    "Precalculos del Capitulo 2 (estacionariedad, ACF/PACF, diferenciacion). ",
    "ACF con stats::acf (divisor n) y PACF con stats::pacf (Durbin-Levinson sobre ",
    "la ACF muestral), hasta el rezago ", MAX_REZAGO, ". ADF: tseries::adf.test ",
    "(H0 = raiz unitaria; deriva + tendencia; k = trunc((n-1)^(1/3))). KPSS: ",
    "tseries::kpss.test (H0 = estacionariedad; l = trunc(4*(n/100)^0.25)). ",
    "ndiffs/nsdiffs y lambda de Guerrero: paquete forecast."
  ),
  max_rezago = MAX_REZAGO,
  fechas = fechas,
  series = series_cap2,
  box_cox = list(
    lambda_airpassengers = round(unname(lambda_ap), 4),
    lambda_trm = round(unname(lambda_trm), 4),
    metodo = "forecast::BoxCox.lambda(method = 'guerrero')",
    costo_del_log = costo_del_log
  ),
  varianzas_diferenciacion = list(
    log_airpassengers = varianzas_dif,
    trm = varianzas_dif_trm
  ),
  trampa_estacionalidad = trampa_estacionalidad,
  metadatos = list(
    generado = fecha_corte,
    generador = "precalculo/genera_cap2.R",
    versiones = list(
      R = paste(R.version$major, R.version$minor, sep = "."),
      tseries = as.character(packageVersion("tseries")),
      forecast = as.character(packageVersion("forecast"))
    )
  )
)

write_json(cap2, file.path(dir_salidas, "cap2_estacionariedad.json"),
           auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null")

writeLines(paste0(
  "// Generado por precalculo/genera_cap2.R el ", fecha_corte, "\n",
  "// Series, ACF/PACF y pruebas de raiz unitaria del Capitulo 2.\n",
  "const DATOS_CAP2 = ", toJSON(cap2, auto_unbox = TRUE, digits = NA, na = "null"), ";\n"
), file.path(dir_salidas, "cap2_datos.js"))

cat("Escrito: cap2_estacionariedad.json / cap2_datos.js\n\n")

# ----------------------------------------------------------------------------
# 6. Resumen legible (para contrastar contra el texto del capítulo)
# ----------------------------------------------------------------------------

cat("=== Pruebas de raiz unitaria =====================================\n")
cat(sprintf("%-22s %5s %9s %8s %9s %8s %7s %7s\n",
            "serie", "n", "ADF", "p(ADF)", "KPSS niv", "p(KPSS)", "ndiffs", "nsdiffs"))
for (s in series_cap2) {
  cat(sprintf("%-22s %5d %9.4f %8.4f %9.4f %8.4f %7d %7s\n",
              s$clave, s$n, s$adf$estadistico, s$adf$p_valor,
              s$kpss_nivel$estadistico, s$kpss_nivel$p_valor,
              s$ndiffs, if (is.null(s$nsdiffs)) "-" else as.character(s$nsdiffs)))
}

cat("\n=== ACF en los primeros rezagos ==================================\n")
for (s in series_cap2) {
  cat(sprintf("%-22s r1=%7.4f r2=%7.4f r12=%7.4f  banda=+/-%.4f\n",
              s$clave, s$acf[1], s$acf[2], s$acf[12], s$banda))
}

cat("\n=== Box-Cox (Guerrero) ===========================================\n")
cat("lambda AirPassengers:", cap2$box_cox$lambda_airpassengers, "\n")
cat("lambda TRM          :", cap2$box_cox$lambda_trm, "\n")
cat("Criterio (menor es mejor): sin transformar =", costo_del_log$cv_sin_transformar,
    "| log =", costo_del_log$cv_logaritmo, "| optimo =", costo_del_log$cv_optimo, "\n")
cat("El log queda", costo_del_log$exceso_del_log_sobre_el_optimo_pct,
    "% por encima del minimo, pero capta el", costo_del_log$mejora_captada_por_el_log_pct,
    "% de la mejora posible\n")
cat("Zona con criterio <= 1.2 x minimo: [",
    costo_del_log$zona_dentro_del_20pct[1], ",", costo_del_log$zona_dentro_del_20pct[2],
    "] -> lambda = 0 queda FUERA\n")

cat("\n=== Sobrediferenciacion: varianza y ACF(1) por numero de diferencias ===\n")
for (nm in c("log_airpassengers", "trm")) {
  cat(nm, "\n")
  for (r in cap2$varianzas_diferenciacion[[nm]]) {
    cat(sprintf("   d=%d  n=%3d  var=%14s  acf1=%7.4f\n",
                r$d, r$n, format(r$varianza, scientific = FALSE), r$acf1))
  }
}

cat("\n=== Trampa: ADF sobre una serie estacional ========================\n")
cat("ADF de log(AirPassengers) segun el numero de rezagos k:\n")
for (r in adf_por_k) {
  cat(sprintf("   k=%2d -> ADF=%8.4f  p=%.4f%s\n", r$k, r$estadistico, r$p_valor,
              if (r$k == trampa_estacionalidad$k_por_defecto) "   <- k por defecto" else ""))
}
cat(sprintf("Desestacionalizada (STL): ADF=%.4f (p=%.4f) · KPSS tendencia=%.4f (p=%.4f)\n",
            adf_sa$estadistico, adf_sa$p_valor, kpss_sa$estadistico, kpss_sa$p_valor))
cat(sprintf("Componente estacional pura: ADF=%.4f (p=%.4f)\n",
            trampa_estacionalidad$adf_componente_estacional_pura$estadistico,
            trampa_estacionalidad$adf_componente_estacional_pura$p_valor))
cat("Monte Carlo (caminata + estacionalidad, H0 CIERTA, nivel nominal 5%):\n")
for (r in montecarlo) {
  cat(sprintf("   amplitud=%.1f -> rechaza en %.1f%% de %d replicas\n",
              r$amplitud, r$tasa_rechazo, N_REP))
}

cat("\n=== Avisos de p-valor fuera de tabla =============================\n")
hubo <- FALSE
for (s in series_cap2) {
  for (nm in c("adf", "kpss_nivel", "kpss_tendencia")) {
    if (isTRUE(s[[nm]]$fuera_tabla)) {
      cat(sprintf("%-22s %-15s %s\n", s$clave, nm, s[[nm]]$aviso)); hubo <- TRUE
    }
  }
}
if (!hubo) cat("(ninguno)\n")
cat("\nListo.\n")
