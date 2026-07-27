# ============================================================================
# genera_cap6.R — Precálculos del Capítulo 6 (pronóstico, métricas y backtesting)
#
# Genera salidas/cap6_evaluacion.json y salidas/cap6_datos.js con:
#   - Residual (dentro de muestra) frente a error de pronóstico (fuera): la
#     distinción que ordena todo el capítulo, medida sobre varios cortes
#   - Métodos de referencia: media, naive, naive estacional y deriva, con sus
#     intervalos, sobre los tres casos
#   - Las siete métricas (ME, RMSE, MAE, MPE, MAPE, sMAPE, MASE, RMSSE)
#     implementadas a mano y VERIFICADAS contra forecast::accuracy
#   - Contraejemplos medidos: dónde se invierte el orden RMSE/MAE, el sesgo a
#     la baja que induce el MAPE, el MAPE sobre una serie que cruza el cero, y
#     qué métricas sobreviven a un cambio de unidades
#   - Fuga de información: validación cruzada aleatoria frente a origen móvil,
#     y la selección de modelo hecha sobre el propio conjunto de prueba
#   - Origen móvil con ventana expansiva y ventana deslizante, error por
#     horizonte, y el costo computacional
#   - Backtesting de 7 métodos sobre 61 orígenes + prueba de Diebold-Mariano
#   - Evaluación del INTERVALO: cobertura empírica frente a la nominal y
#     puntaje de Winkler (el capítulo 4 lo construye; este lo evalúa)
#   - Tres casos con tres desenlaces: AirPassengers (gana el modelo), TRM
#     (nadie vence al naive) y Nilo (el naive le gana al ARIMA)
#   - Las cifras reales de los cinco errores del taller de auditoría de IA
#
# FRONTERAS acordadas y respetadas:
#   - El capítulo 4 CONSTRUYE el intervalo desde los pesos psi. Aquí no se
#     vuelve a construir: se evalúa.
#   - El capítulo 5 compara métodos sobre UNA partición para mostrar que no
#     basta. Aquí la partición única solo sirve para definir los métodos de
#     referencia; la comparación seria es por origen móvil.
#
# Dependencias: jsonlite, tseries, forecast. NINGUNA nueva.
# Uso:  Rscript genera_cap6.R      (desde la carpeta precalculo/)
# ============================================================================

suppressMessages({
  library(jsonlite)
  library(tseries)
  library(forecast)
})

# R arranca con LC_CTYPE = "C" y entonces jsonlite escribe las tildes como
# <c3><ad>; el navegador lo lee como marcado y se come la letra. Hay que forzar
# la configuracion regional ANTES de generar nada. (Bug real del capitulo 5.)
suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"))
if (!isTRUE(l10n_info()$"UTF-8")) {
  warning("No se pudo activar una configuracion regional UTF-8: las tildes ",
          "del JSON saldran mal. Ejecuta con LC_ALL=en_US.UTF-8 Rscript ...")
}

args_dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
if (is.na(args_dir) || args_dir == "") args_dir <- "."
dir_salidas <- file.path(args_dir, "salidas")
stopifnot(dir.exists(dir_salidas))

set.seed(2026)
M <- 12
H <- 12          # horizonte de la evaluación por origen móvil
NIVELES <- c(80, 95)

series_base <- fromJSON(file.path(dir_salidas, "datos_series.json"), simplifyVector = TRUE)
serie_ts <- function(nombre) ts(series_base[[nombre]]$valores,
                                start = series_base[[nombre]]$inicio,
                                frequency = series_base[[nombre]]$frecuencia)

ap   <- serie_ts("airpassengers")   # n = 144, m = 12
trm  <- serie_ts("trm")             # n = 138, m = 12
nilo <- serie_ts("nilo")            # n = 100, anual
uad  <- serie_ts("usaccdeaths")     # n =  72, m = 12
co2s <- serie_ts("co2")             # n = 468, m = 12

cat("Series:", "AP", length(ap), "| TRM", length(trm), "| Nilo", length(nilo),
    "| USAccDeaths", length(uad), "| co2", length(co2s), "\n\n")

r4 <- function(x) round(as.numeric(x), 4)
r2 <- function(x) round(as.numeric(x), 2)

# ----------------------------------------------------------------------------
# 1. Las métricas, implementadas a mano
#
# Se escriben aquí y no se toman de accuracy() por dos razones: el capítulo las
# enseña con su fórmula, y así se puede VERIFICAR que la fórmula del texto es
# la que produce el número. La comprobación contra accuracy() va más abajo.
# ----------------------------------------------------------------------------

# Q: escala del MASE. Es el MAE del método naive (estacional si m > 1) sobre el
# conjunto de ENTRENAMIENTO, nunca sobre el de prueba: si se calculara sobre la
# prueba, la métrica dejaría de ser comparable entre particiones.
escala_mase <- function(entrena, m = 1) {
  x <- as.numeric(entrena)
  if (m > 1 && length(x) > m) mean(abs(diff(x, lag = m))) else mean(abs(diff(x)))
}
escala_rmsse <- function(entrena, m = 1) {
  x <- as.numeric(entrena)
  d <- if (m > 1 && length(x) > m) diff(x, lag = m) else diff(x)
  sqrt(mean(d^2))
}

metricas <- function(real, pron, entrena, m = 1) {
  real <- as.numeric(real); pron <- as.numeric(pron)
  e <- real - pron
  q_mae  <- escala_mase(entrena, m)
  q_rmse <- escala_rmsse(entrena, m)
  hay_cero <- any(real == 0)
  list(
    me    = r4(mean(e)),
    rmse  = r4(sqrt(mean(e^2))),
    mae   = r4(mean(abs(e))),
    mpe   = if (hay_cero) NA else r4(100 * mean(e / real)),
    mape  = if (hay_cero) NA else r4(100 * mean(abs(e / real))),
    smape = r4(200 * mean(abs(e) / (abs(real) + abs(pron)))),
    mase  = r4(mean(abs(e)) / q_mae),
    rmsse = r4(sqrt(mean(e^2)) / q_rmse)
  )
}

# Puntaje de Winkler (FPP3 secc. 5.9): ancho del intervalo, más una penalización
# proporcional a lo que se aleja el valor observado cuando queda fuera. Menor es
# mejor. Es la métrica que castiga a la vez el intervalo demasiado ancho y el
# demasiado estrecho; ninguna de las dos cosas la ve la cobertura sola.
winkler <- function(real, li, ls, nivel) {
  alfa <- 1 - nivel / 100
  ancho <- ls - li
  w <- ancho +
    ifelse(real < li, (2 / alfa) * (li - real), 0) +
    ifelse(real > ls, (2 / alfa) * (real - ls), 0)
  as.numeric(w)
}

cobertura <- function(real, li, ls) mean(real >= li & real <= ls)

# ----------------------------------------------------------------------------
# 2. Métodos: cada uno es una función (entrenamiento, h) -> pronóstico + bandas
#
# Devuelven SIEMPRE en la escala original de la serie, de modo que las métricas
# de todos los métodos sean comparables. Los que trabajan en logaritmos
# devuelven la MEDIANA al deshacer la transformación (es lo que hace `lambda=0`
# sin `biasadj`), y eso queda dicho en el capítulo.
# ----------------------------------------------------------------------------

envuelve <- function(fc) {
  list(media = as.numeric(fc$mean),
       li80 = as.numeric(fc$lower[, 1]), ls80 = as.numeric(fc$upper[, 1]),
       li95 = as.numeric(fc$lower[, 2]), ls95 = as.numeric(fc$upper[, 2]))
}

m_media   <- function(tr, h) envuelve(meanf(tr, h = h, level = NIVELES))
m_naive   <- function(tr, h) envuelve(naive(tr, h = h, level = NIVELES))
m_snaive  <- function(tr, h) envuelve(snaive(tr, h = h, level = NIVELES))
m_deriva  <- function(tr, h) envuelve(rwf(tr, h = h, drift = TRUE, level = NIVELES))

# SARIMA airline sobre logaritmos: lambda = 0 lo ajusta en log y deshace la
# transformación al pronosticar. Sin biasadj el puntual es la mediana.
m_sarima  <- function(tr, h) envuelve(forecast(
  Arima(tr, order = c(0, 1, 1), seasonal = c(0, 1, 1), lambda = 0),
  h = h, level = NIVELES))

# ETS y STL se ajustan sobre los logaritmos y se deshace la transformación a
# mano, EXACTAMENTE como en genera_cap5.R (`ets(log x)` y `stlm` con
# `s.window = "periodic"`). No es un capricho: el capítulo 5 publica el RMSE
# medio de estos mismos métodos sobre estos mismos 61 orígenes, y las dos
# cifras tienen que reconciliar. Con `ets(x, lambda = 0)` o con `stlf` y su
# `s.window` por defecto salen números parecidos pero distintos.
desde_log <- function(fc) list(
  media = exp(as.numeric(fc$mean)),
  li80 = exp(as.numeric(fc$lower[, 1])), ls80 = exp(as.numeric(fc$upper[, 1])),
  li95 = exp(as.numeric(fc$lower[, 2])), ls95 = exp(as.numeric(fc$upper[, 2])))

m_ets_log <- function(tr, h) desde_log(forecast(ets(log(tr)), h = h, level = NIVELES))

m_stl     <- function(tr, h) desde_log(forecast(
  stlm(log(tr), s.window = "periodic", method = "arima"), h = h, level = NIVELES))

# auto.arima con la búsqueda escalonada (stepwise), que es la que usa un
# estudiante por defecto y la que cuesta un tiempo razonable en 61 orígenes.
m_auto    <- function(tr, h) envuelve(forecast(
  auto.arima(tr, lambda = 0), h = h, level = NIVELES))

# Versiones sin logaritmo, para las series que no lo admiten o no lo necesitan
m_arima_n <- function(tr, h) envuelve(forecast(
  Arima(tr, order = c(1, 1, 1)), h = h, level = NIVELES))
m_auto_n  <- function(tr, h) envuelve(forecast(auto.arima(tr), h = h, level = NIVELES))
m_ets_n   <- function(tr, h) envuelve(forecast(ets(tr), h = h, level = NIVELES))

# ----------------------------------------------------------------------------
# 3. Motor de origen móvil
#
# Ventana EXPANSIVA: el entrenamiento crece con cada origen (usa todo el pasado).
# Ventana DESLIZANTE: el entrenamiento tiene tamaño fijo (olvida lo más viejo).
# Reajusta el modelo en cada origen — que es la parte cara y honesta: reutilizar
# los coeficientes estimados con toda la serie sería fuga de información.
# ----------------------------------------------------------------------------

origen_movil <- function(y, metodo, T0, h = H, ventana = NULL) {
  n <- length(y)
  origenes <- T0:(n - h)
  pron <- matrix(NA_real_, length(origenes), h)
  li80 <- ls80 <- li95 <- ls95 <- pron
  reales <- pron
  for (i in seq_along(origenes)) {
    Tt <- origenes[i]
    desde <- if (is.null(ventana)) 1 else max(1, Tt - ventana + 1)
    tr <- subset(y, start = desde, end = Tt)
    fc <- try(metodo(tr, h), silent = TRUE)
    if (inherits(fc, "try-error")) next
    pron[i, ] <- fc$media
    li80[i, ] <- fc$li80; ls80[i, ] <- fc$ls80
    li95[i, ] <- fc$li95; ls95[i, ] <- fc$ls95
    reales[i, ] <- as.numeric(y)[(Tt + 1):(Tt + h)]
  }
  list(origenes = origenes, pron = pron, reales = reales,
       li80 = li80, ls80 = ls80, li95 = li95, ls95 = ls95,
       error = reales - pron)
}

# Resumen de un origen móvil: métricas agregadas sobre TODOS los errores, y el
# RMSE por horizonte, que es la lectura que de verdad interesa (el error crece
# con h y un promedio único lo esconde).
resume_om <- function(om, y, T0, m = 1) {
  e <- as.numeric(om$error); r <- as.numeric(om$reales); p <- as.numeric(om$pron)
  ok <- !is.na(e)
  entrena <- subset(y, start = 1, end = T0)   # escala del MASE: el primer entrenamiento
  q_mae <- escala_mase(entrena, m); q_rmse <- escala_rmsse(entrena, m)
  # Dos formas de agregar que NO dan lo mismo y que hay que distinguir:
  #   - rmse: se juntan todos los errores y se calcula un solo RMSE
  #   - rmse_medio_origenes: se calcula el RMSE de cada origen y se promedian
  # La segunda es menor por la desigualdad de Jensen (la raíz es cóncava). El
  # capítulo 5 citó la segunda; el capítulo 6 usa la primera y lo dice.
  rmse_por_origen <- sqrt(rowMeans(om$error^2, na.rm = TRUE))
  list(
    n_origenes = length(om$origenes),
    n_errores  = sum(ok),
    rmse  = r4(sqrt(mean(e[ok]^2))),
    rmse_medio_origenes = r4(mean(rmse_por_origen, na.rm = TRUE)),
    rmse_origenes = r4(rmse_por_origen),
    mae   = r4(mean(abs(e[ok]))),
    me    = r4(mean(e[ok])),
    mape  = r4(100 * mean(abs(e[ok] / r[ok]))),
    smape = r4(200 * mean(abs(e[ok]) / (abs(r[ok]) + abs(p[ok])))),
    mase  = r4(mean(abs(e[ok])) / q_mae),
    rmsse = r4(sqrt(mean(e[ok]^2)) / q_rmse),
    rmse_h = r4(sqrt(colMeans(om$error^2, na.rm = TRUE))),
    mae_h  = r4(colMeans(abs(om$error), na.rm = TRUE)),
    cob80  = r4(100 * cobertura(om$reales[ok], om$li80[ok], om$ls80[ok])),
    cob95  = r4(100 * cobertura(om$reales[ok], om$li95[ok], om$ls95[ok])),
    winkler80 = r4(mean(winkler(om$reales[ok], om$li80[ok], om$ls80[ok], 80))),
    winkler95 = r4(mean(winkler(om$reales[ok], om$li95[ok], om$ls95[ok], 95)))
  )
}

etiqueta_fecha <- function(y, i) {
  tt <- time(y)[i]
  if (frequency(y) == 1) return(as.character(floor(tt)))
  sprintf("%d-%02d", floor(tt + 1e-8), round((tt - floor(tt + 1e-8)) * 12) + 1)
}

# ============================================================================
# SECCIÓN A — Residual frente a error de pronóstico  (módulo 1)
# ============================================================================
cat("A. Residual vs. error de pronóstico...\n")

# Para una rejilla de cortes: RMSE de los residuales del modelo ajustado con los
# datos hasta el corte (dentro de muestra) frente al RMSE de sus pronósticos a
# h = 1..12 (fuera). El primero es sistemáticamente menor y NO mide capacidad
# de pronóstico: es la trampa nº 1 del capítulo.
cortes <- seq(72, 132, by = 6)
rve <- lapply(cortes, function(Tt) {
  tr <- subset(ap, start = 1, end = Tt)
  fit <- Arima(tr, order = c(0, 1, 1), seasonal = c(0, 1, 1), lambda = 0)
  res <- as.numeric(residuals(fit, type = "response"))   # en la escala original
  h <- min(H, length(ap) - Tt)
  fc <- forecast(fit, h = h, level = NIVELES)
  real <- as.numeric(ap)[(Tt + 1):(Tt + h)]
  e <- real - as.numeric(fc$mean)
  list(T = Tt, fecha = etiqueta_fecha(ap, Tt),
       rmse_dentro = r4(sqrt(mean(res^2))),
       rmse_fuera  = r4(sqrt(mean(e^2))),
       rmse_fuera_h1 = r4(abs(e[1])),
       razon = r4(sqrt(mean(e^2)) / sqrt(mean(res^2))))
})
razones <- sapply(rve, function(z) z$razon)
cat("   razón fuera/dentro: mín", r4(min(razones)), " mediana", r4(median(razones)),
    " máx", r4(max(razones)), "\n")

# El mismo mensaje con el modelo completo: accuracy() sobre el entrenamiento.
fit_ap_completo <- Arima(ap, order = c(0, 1, 1), seasonal = c(0, 1, 1), lambda = 0)
acc_entrena <- accuracy(fit_ap_completo)
residual_vs_error <- list(
  cortes = rve,
  entrenamiento_completo = list(
    rmse = r4(acc_entrena[1, "RMSE"]), mae = r4(acc_entrena[1, "MAE"]),
    mape = r4(acc_entrena[1, "MAPE"]), mase = r4(acc_entrena[1, "MASE"])
  ),
  nota = paste0("El RMSE de los residuales del modelo ajustado con toda la serie es ",
                r4(acc_entrena[1, "RMSE"]), ", y el RMSE medio de sus pronósticos ",
                "a 12 meses en origen móvil es varias veces mayor.")
)

# ============================================================================
# SECCIÓN B — Métodos de referencia sobre una partición  (módulo 2)
# ============================================================================
cat("B. Métodos de referencia...\n")

partition_bench <- function(y, m, h_prueba, metodos, nombres) {
  n <- length(y)
  tr <- subset(y, start = 1, end = n - h_prueba)
  te <- as.numeric(y)[(n - h_prueba + 1):n]
  res <- lapply(seq_along(metodos), function(i) {
    fc <- metodos[[i]](tr, h_prueba)
    mm <- metricas(te, fc$media, tr, m)
    c(list(metodo = nombres[i],
           pronostico = r2(fc$media),
           li80 = r2(fc$li80), ls80 = r2(fc$ls80),
           li95 = r2(fc$li95), ls95 = r2(fc$ls95),
           cobertura80 = r4(100 * cobertura(te, fc$li80, fc$ls80)),
           cobertura95 = r4(100 * cobertura(te, fc$li95, fc$ls95)),
           winkler95 = r4(mean(winkler(te, fc$li95, fc$ls95, 95)))), mm)
  })
  list(n = n, n_entrena = n - h_prueba, n_prueba = h_prueba,
       corte = etiqueta_fecha(y, n - h_prueba),
       observado = r2(te),
       fechas = sapply((n - h_prueba + 1):n, function(i) etiqueta_fecha(y, i)),
       q_mase = r4(escala_mase(tr, m)),
       metodos = res)
}

bench_ap <- partition_bench(
  ap, M, 24,
  list(m_media, m_naive, m_snaive, m_deriva),
  c("Media", "Naive", "Naive estacional", "Deriva"))

cat("   AirPassengers (24 meses de prueba) RMSE:",
    paste(sapply(bench_ap$metodos, function(z) sprintf("%s=%.2f", z$metodo, z$rmse)),
          collapse = " | "), "\n")

# ============================================================================
# SECCIÓN C — Verificación de las métricas contra forecast::accuracy
# ============================================================================
cat("C. Verificando las métricas contra accuracy()...\n")

tr_ap  <- subset(ap, start = 1, end = 120)
te_ts  <- subset(ap, start = 121, end = 144)   # sigue siendo ts mensual
te_ap  <- as.numeric(te_ts)                    # el mismo vector, sin frecuencia
fc_ver <- snaive(tr_ap, h = 24)
mias  <- metricas(te_ap, as.numeric(fc_ver$mean), tr_ap, M)
suyas <- accuracy(fc_ver, te_ts)["Test set", ]

# TRAMPA ENCONTRADA AUDITANDO ESTE SCRIPT, y va al capítulo:
# accuracy() decide la escala del MASE con la FRECUENCIA del conjunto de prueba
#   d <- as.numeric(frequency(x) == 1);  D <- as.numeric(frequency(x) > 1)
# Si se le pasa el conjunto de prueba como ts mensual, escala con el naive
# ESTACIONAL (rezago 12), que es la definición de Hyndman-Koehler y de FPP3.
# Si se le pasa el MISMO vector con as.numeric(), frequency vale 1 y escala con
# el naive simple (rezago 1). El MASE cambia sin ningún aviso.
suyas_num <- accuracy(fc_ver, te_ap)["Test set", ]
verificacion <- list(
  metodo = "Naive estacional sobre AirPassengers, entrenamiento 1949-1958",
  mias = mias[c("me", "rmse", "mae", "mpe", "mape", "mase")],
  accuracy = list(me = r4(suyas["ME"]), rmse = r4(suyas["RMSE"]), mae = r4(suyas["MAE"]),
                  mpe = r4(suyas["MPE"]), mape = r4(suyas["MAPE"]), mase = r4(suyas["MASE"])),
  diferencia_maxima = r4(max(abs(c(mias$me - suyas["ME"], mias$rmse - suyas["RMSE"],
                                   mias$mae - suyas["MAE"], mias$mpe - suyas["MPE"],
                                   mias$mape - suyas["MAPE"], mias$mase - suyas["MASE"])))),
  trampa_mase = list(
    mase_test_ts      = r4(suyas["MASE"]),
    mase_test_numeric = r4(suyas_num["MASE"]),
    q_estacional      = r4(escala_mase(tr_ap, M)),
    q_simple          = r4(escala_mase(tr_ap, 1)),
    cambio_pct        = r4(100 * (suyas_num["MASE"] / suyas["MASE"] - 1))
  )
)
cat("   diferencia máxima con accuracy():", verificacion$diferencia_maxima, "\n")
cat("   MASE con prueba ts:", r4(suyas["MASE"]),
    "| con as.numeric():", r4(suyas_num["MASE"]), "\n")

# ============================================================================
# SECCIÓN D — Contraejemplos de las métricas  (módulos 3, 4, 5)
# ============================================================================
cat("D. Contraejemplos de métricas...\n")

# --- D1. RMSE y MAE no ordenan igual --------------------------------------
# El RMSE eleva al cuadrado: un solo error grande pesa más que muchos pequeños.
# Se busca en los orígenes reales de AirPassengers uno donde el orden de dos
# métodos se invierta al pasar de RMSE a MAE. No se fabrica: se busca.
om_snaive_ap <- origen_movil(ap, m_snaive, T0 = 72)
om_deriva_ap <- origen_movil(ap, m_deriva, T0 = 72)
inversiones <- list()
for (i in seq_along(om_snaive_ap$origenes)) {
  e1 <- om_snaive_ap$error[i, ]; e2 <- om_deriva_ap$error[i, ]
  r1 <- sqrt(mean(e1^2)); r2_ <- sqrt(mean(e2^2))
  a1 <- mean(abs(e1)); a2 <- mean(abs(e2))
  if (sign(r1 - r2_) != sign(a1 - a2)) {
    inversiones[[length(inversiones) + 1]] <- list(
      T = om_snaive_ap$origenes[i], fecha = etiqueta_fecha(ap, om_snaive_ap$origenes[i]),
      snaive_rmse = r4(r1), deriva_rmse = r4(r2_),
      snaive_mae = r4(a1), deriva_mae = r4(a2),
      gana_rmse = if (r1 < r2_) "Naive estacional" else "Deriva",
      gana_mae  = if (a1 < a2)  "Naive estacional" else "Deriva")
  }
}
cat("   orígenes donde RMSE y MAE se contradicen:", length(inversiones),
    "de", length(om_snaive_ap$origenes), "\n")

# Los 12 errores de cada origen, para que el simulador los dibuje barra a barra
# en vez de mostrar solo el resumen: lo que hay que ver es la FORMA del reparto.
errores_por_origen <- lapply(seq_along(om_snaive_ap$origenes), function(i) list(
  T = om_snaive_ap$origenes[i],
  fecha = etiqueta_fecha(ap, om_snaive_ap$origenes[i]),
  snaive = r2(om_snaive_ap$error[i, ]), deriva = r2(om_deriva_ap$error[i, ]),
  snaive_rmse = r4(sqrt(mean(om_snaive_ap$error[i, ]^2))),
  deriva_rmse = r4(sqrt(mean(om_deriva_ap$error[i, ]^2))),
  snaive_mae = r4(mean(abs(om_snaive_ap$error[i, ]))),
  deriva_mae = r4(mean(abs(om_deriva_ap$error[i, ]))),
  conflicto = sign(sqrt(mean(om_snaive_ap$error[i, ]^2)) -
                   sqrt(mean(om_deriva_ap$error[i, ]^2))) !=
              sign(mean(abs(om_snaive_ap$error[i, ])) -
                   mean(abs(om_deriva_ap$error[i, ])))
))

# --- D2. El MAPE empuja el pronóstico hacia abajo -------------------------
# Escenario mínimo y exacto: el valor futuro vale 100 o 200 con probabilidad
# 1/2. Para cada pronóstico constante f se calcula el MAPE esperado y el MAE
# esperado. El MAE se minimiza en cualquier punto del intervalo; el MAPE, en el
# valor BAJO. La consecuencia práctica: quien optimiza MAPE subpronostica.
f_rejilla <- seq(80, 220, by = 2)
mape_esperado <- sapply(f_rejilla, function(f) 100 * (0.5 * abs(100 - f) / 100 + 0.5 * abs(200 - f) / 200))
mae_esperado  <- sapply(f_rejilla, function(f) 0.5 * abs(100 - f) + 0.5 * abs(200 - f))
rmse_esperado <- sapply(f_rejilla, function(f) sqrt(0.5 * (100 - f)^2 + 0.5 * (200 - f)^2))
sesgo_mape <- list(
  escenario = "El valor futuro vale 100 o 200 con probabilidad 1/2",
  f = f_rejilla,
  mape = r4(mape_esperado), mae = r4(mae_esperado), rmse = r4(rmse_esperado),
  f_optimo_mape = f_rejilla[which.min(mape_esperado)],
  f_optimo_rmse = f_rejilla[which.min(rmse_esperado)],
  mape_en_100 = r4(mape_esperado[f_rejilla == 100]),
  mape_en_150 = r4(mape_esperado[f_rejilla == 150]),
  mape_en_200 = r4(mape_esperado[f_rejilla == 200]),
  media = 150, mediana_min_mae = "cualquier f entre 100 y 200"
)
cat("   MAPE esperado mínimo en f =", sesgo_mape$f_optimo_mape,
    "| RMSE mínimo en f =", sesgo_mape$f_optimo_rmse, "\n")

# --- D3. El MAPE sobre una serie que cruza el cero ------------------------
# Los log-retornos mensuales de la TRM pasan por cero varias veces. El MAPE de
# CUALQUIER método se dispara, y no porque el pronóstico sea malo.
ret_trm <- diff(log(trm)) * 100      # en porcentaje mensual
n_ret <- length(ret_trm)
tr_ret <- subset(ret_trm, start = 1, end = n_ret - 24)
te_ret <- as.numeric(ret_trm)[(n_ret - 23):n_ret]
fc_ret <- m_media(tr_ret, 24)
ape_ret <- 100 * abs((te_ret - fc_ret$media) / te_ret)
mape_cero <- list(
  serie = "Log-retornos mensuales de la TRM (%), últimos 24 meses de prueba",
  n = n_ret, cercanos_a_cero = sum(abs(as.numeric(ret_trm)) < 0.1),
  minimo_absoluto = r4(min(abs(as.numeric(ret_trm)))),
  observado = r4(te_ret), pronostico = r4(fc_ret$media),
  ape = r4(ape_ret),
  mape = r4(mean(ape_ret)), mape_mediano = r4(median(ape_ret)),
  ape_maximo = r4(max(ape_ret)),
  observado_del_maximo = r4(te_ret[which.max(ape_ret)]),
  mae = r4(mean(abs(te_ret - fc_ret$media))),
  rmse = r4(sqrt(mean((te_ret - fc_ret$media)^2))),
  mase = r4(mean(abs(te_ret - fc_ret$media)) / escala_mase(tr_ret, 1))
)
cat("   MAPE sobre log-retornos:", mape_cero$mape, "% (mediana", mape_cero$mape_mediano,
    "%), APE máximo", mape_cero$ape_maximo, "%\n")

# --- D4. Qué métricas sobreviven a un cambio de unidades ------------------
# La misma serie en miles de pasajeros y en pasajeros (x1000). Las métricas
# dependientes de la escala se multiplican por 1000; las porcentuales y las
# escaladas no se mueven. Es el argumento de existencia del MASE.
esc_a <- metricas(te_ap, as.numeric(fc_ver$mean), tr_ap, M)
ap_k  <- ap * 1000
tr_k  <- subset(ap_k, start = 1, end = 120)
fc_k  <- snaive(tr_k, h = 24)
esc_b <- metricas(as.numeric(ap_k)[121:144], as.numeric(fc_k$mean), tr_k, M)
cambio_escala <- list(
  original = esc_a, por_mil = esc_b,
  razon = list(rmse = r4(esc_b$rmse / esc_a$rmse), mae = r4(esc_b$mae / esc_a$mae),
               mape = r4(esc_b$mape / esc_a$mape), smape = r4(esc_b$smape / esc_a$smape),
               mase = r4(esc_b$mase / esc_a$mase), rmsse = r4(esc_b$rmsse / esc_a$rmsse))
)
cat("   cambio de unidades x1000 -> razón RMSE", cambio_escala$razon$rmse,
    "| MASE", cambio_escala$razon$mase, "\n")

# ============================================================================
# SECCIÓN E — Fuga de información  (módulo 6)
# ============================================================================
cat("E. Fuga de información...\n")

# --- E1. Validación cruzada aleatoria frente a origen móvil ---------------
#
# La afirmación de manual es que el k-fold aleatorio "sobrestima el desempeño".
# Antes de escribirla en el capítulo hay que MEDIRLA, porque no siempre es
# cierta: depende de por dónde entra el futuro. Se comparan tres montajes sobre
# la misma serie, con las tres formas de estimar el error (k-fold aleatorio,
# origen móvil, y un bloque final que nadie tocó, que es la verdad).
#
# El resultado medido es más fino que el eslogan, y por eso vale la pena: el
# k-fold aleatorio miente cuando el modelo INTERPOLA EN EL TIEMPO —vecinos más
# cercanos, un polinomio en t, tendencia con indicadoras de mes—, porque al
# repartir al azar deja los vecinos de cada punto de prueba dentro del
# entrenamiento. Con una regresión sobre rezagos NO miente: los rezagos ya
# llevan esa información y el pliegue aleatorio no regala nada.
P <- 13
y_log <- as.numeric(log(ap))
n_ap  <- length(y_log)
K     <- 5
n_fin <- 24

X_fuga <- as.data.frame(embed(y_log, P + 1))
colnames(X_fuga) <- c("y", paste0("l", 1:P))
X_fuga$t <- (P + 1):n_ap
cols_rez <- paste0("l", 1:P)
dev_f <- X_fuga[1:(nrow(X_fuga) - n_fin), ]
fin_f <- X_fuga[(nrow(X_fuga) - n_fin + 1):nrow(X_fuga), ]

set.seed(2026)                         # el reparto de pliegues, reproducible
pliegue <- sample(rep(1:K, length.out = nrow(dev_f)))

vecinos <- function(tr, te, k) sapply(seq_len(nrow(te)), function(i) {
  d <- sqrt(colSums((t(as.matrix(tr[, cols_rez])) - as.numeric(te[i, cols_rez]))^2))
  mean(tr$y[order(d)[1:k]])
})

evalua_montaje <- function(id, nombre, predice, interpola) {
  # (a) k-fold aleatorio: los pliegues mezclan pasado y futuro
  e_k <- unlist(lapply(1:K, function(k)
    dev_f$y[pliegue == k] - predice(dev_f[pliegue != k, ], dev_f[pliegue == k, ])))
  # (b) origen móvil de un paso: siempre se entrena solo con el pasado
  inicio <- floor(nrow(dev_f) / 2)
  e_o <- unlist(lapply(inicio:(nrow(dev_f) - 1), function(i)
    dev_f$y[i + 1] - predice(dev_f[1:i, ], dev_f[i + 1, , drop = FALSE])))
  # (c) el bloque final, que no participó en nada: la verdad
  e_f <- fin_f$y - predice(dev_f, fin_f)
  rk <- sqrt(mean(e_k^2)); ro <- sqrt(mean(e_o^2)); rf <- sqrt(mean(e_f^2))
  list(id = id, nombre = nombre, interpola_en_el_tiempo = interpola,
       rmse_kfold = r4(rk), rmse_origen_movil = r4(ro), rmse_bloque_final = r4(rf),
       # optimismo > 0 = el método promete MENOS error del que de verdad habrá
       optimismo_kfold = r4(100 * (1 - rk / rf)),
       optimismo_origen_movil = r4(100 * (1 - ro / rf)))
}

montajes <- list(
  evalua_montaje("rezagos", paste0("Regresión lineal sobre los rezagos 1..", P),
                 function(tr, te) predict(lm(y ~ . - t, data = tr), te), FALSE),
  evalua_montaje("vecinos1", "1 vecino más cercano sobre los rezagos",
                 function(tr, te) vecinos(tr, te, 1), TRUE),
  evalua_montaje("vecinos3", "3 vecinos más cercanos sobre los rezagos",
                 function(tr, te) vecinos(tr, te, 3), TRUE),
  evalua_montaje("estacionales", "Tendencia lineal + indicadoras de mes",
                 function(tr, te) predict(
                   lm(y ~ t + factor(((t - 1) %% 12) + 1), data = tr), te), TRUE),
  evalua_montaje("polinomio", "Polinomio de grado 8 en el índice de tiempo",
                 function(tr, te) predict(lm(y ~ poly(t, 8), data = tr), te), TRUE)
)

fuga_cv <- list(
  descripcion = paste0("log(AirPassengers): ", nrow(X_fuga), " filas con los rezagos ",
                       "1..", P, ". Las últimas ", n_fin, " se reservan como bloque final ",
                       "y no participan en nada; sobre las ", nrow(dev_f),
                       " restantes se estima el error de dos maneras."),
  p = P, k = K, n_filas = nrow(X_fuga), n_desarrollo = nrow(dev_f), n_final = n_fin,
  escala = "logaritmos", montajes = montajes,
  nota = paste0("El optimismo del k-fold aleatorio NO es automático. Aparece ",
                "cuando el modelo interpola en el tiempo, porque el reparto al ",
                "azar deja los vecinos de cada punto de prueba dentro del ",
                "entrenamiento. Con una regresión sobre rezagos no aparece.")
)
for (mo in montajes) {
  cat(sprintf("   %-13s k-fold %.4f | origen móvil %.4f | bloque final %.4f | optimismo %+.1f %%\n",
              mo$id, mo$rmse_kfold, mo$rmse_origen_movil, mo$rmse_bloque_final,
              mo$optimismo_kfold))
}

# --- E2. Elegir el modelo mirando el conjunto de prueba -------------------
# El segundo pecado, más sutil y más común: probar muchos modelos, quedarse con
# el que mejor sale en la prueba, y reportar ESE número como desempeño. Se mide
# el optimismo: el ganador se reevalúa sobre un bloque que nunca vio nadie.
rejilla_pdq <- expand.grid(p = 0:2, q = 0:2, P = 0:1, Q = 0:1)
n_val <- 24; n_test <- 24
tr_sel <- subset(ap, start = 1, end = n_ap - n_val - n_test)
val_sel <- as.numeric(ap)[(n_ap - n_val - n_test + 1):(n_ap - n_test)]
test_sel <- as.numeric(ap)[(n_ap - n_test + 1):n_ap]
sel <- lapply(seq_len(nrow(rejilla_pdq)), function(i) {
  g <- rejilla_pdq[i, ]
  aj <- try(Arima(tr_sel, order = c(g$p, 1, g$q), seasonal = c(g$P, 1, g$Q), lambda = 0),
            silent = TRUE)
  if (inherits(aj, "try-error")) return(NULL)
  fv <- forecast(aj, h = n_val)
  # el mismo modelo, reajustado con entrenamiento + validación, sobre el test
  aj2 <- try(Arima(subset(ap, start = 1, end = n_ap - n_test),
                   order = c(g$p, 1, g$q), seasonal = c(g$P, 1, g$Q), lambda = 0),
             silent = TRUE)
  rmse_t <- if (inherits(aj2, "try-error")) NA else
    sqrt(mean((test_sel - as.numeric(forecast(aj2, h = n_test)$mean))^2))
  list(modelo = sprintf("(%d,1,%d)(%d,1,%d)[12]", g$p, g$q, g$P, g$Q),
       aicc = r4(aj$aicc),
       rmse_validacion = r4(sqrt(mean((val_sel - as.numeric(fv$mean))^2))),
       rmse_prueba = r4(rmse_t))
})
sel <- Filter(Negate(is.null), sel)
rv <- sapply(sel, function(z) z$rmse_validacion)
rp <- sapply(sel, function(z) z$rmse_prueba)
ai <- sapply(sel, function(z) z$aicc)
i_mejor_val <- which.min(rv)
i_mejor_aicc <- which.min(ai)
seleccion_sobre_prueba <- list(
  n_modelos = length(sel), modelos = sel,
  mejor_por_validacion = sel[[i_mejor_val]]$modelo,
  rmse_que_se_reporta  = r4(rv[i_mejor_val]),
  rmse_real_del_mismo  = r4(rp[i_mejor_val]),
  optimismo            = r4(100 * (rp[i_mejor_val] / rv[i_mejor_val] - 1)),
  mejor_por_aicc       = sel[[i_mejor_aicc]]$modelo,
  rmse_real_del_aicc   = r4(rp[i_mejor_aicc]),
  rmse_medio_prueba    = r4(mean(rp, na.rm = TRUE)),
  nota = paste0("Los ", length(sel), " modelos comparten d = 1 y D = 1: el AICc solo ",
                "es comparable dentro del mismo orden de diferenciación.")
)
cat("   mejor por validación:", seleccion_sobre_prueba$mejor_por_validacion,
    "-> se reporta", seleccion_sobre_prueba$rmse_que_se_reporta,
    ", de verdad", seleccion_sobre_prueba$rmse_real_del_mismo, "\n")

# ============================================================================
# SECCIÓN F — Origen móvil: expansiva, deslizante y por horizonte  (módulo 7)
# ============================================================================
cat("F. Origen móvil (esto tarda)...\n")

T0_AP <- 72   # primer origen en 1954-12: 61 orígenes con h = 12, igual que el cap. 5
t_ini <- Sys.time()
om_sarima_exp <- origen_movil(ap, m_sarima, T0 = T0_AP)
t_exp <- as.numeric(difftime(Sys.time(), t_ini, units = "secs"))
om_sarima_desl <- origen_movil(ap, m_sarima, T0 = T0_AP, ventana = 72)

res_exp  <- resume_om(om_sarima_exp,  ap, T0_AP, M)
res_desl <- resume_om(om_sarima_desl, ap, T0_AP, M)
cat("   SARIMA expansiva RMSE", res_exp$rmse, "| deslizante(72)", res_desl$rmse,
    sprintf("| %.1f s\n", t_exp))

ventanas <- list(expansiva = res_exp, deslizante_72 = res_desl)

# ============================================================================
# SECCIÓN G — Backtesting de varios métodos + Diebold-Mariano  (módulo 8)
# ============================================================================
cat("G. Backtesting multi-método...\n")

metodos_bt <- list(
  list(id = "media",  nombre = "Media",            f = m_media,   ref = TRUE),
  list(id = "naive",  nombre = "Naive",            f = m_naive,   ref = TRUE),
  list(id = "snaive", nombre = "Naive estacional", f = m_snaive,  ref = TRUE),
  list(id = "deriva", nombre = "Deriva",           f = m_deriva,  ref = TRUE),
  list(id = "ets",    nombre = "ETS sobre log",    f = m_ets_log, ref = FALSE),
  list(id = "stl",    nombre = "STL + ARIMA",      f = m_stl,     ref = FALSE),
  list(id = "sarima", nombre = "SARIMA airline",   f = m_sarima,  ref = FALSE),
  list(id = "auto",   nombre = "auto.arima",       f = m_auto,    ref = FALSE)
)

oms <- list(); oms[["sarima"]] <- om_sarima_exp
tiempos <- list(sarima = r2(t_exp))
for (mt in metodos_bt) {
  if (mt$id == "sarima") next
  t0 <- Sys.time()
  oms[[mt$id]] <- origen_movil(ap, mt$f, T0 = T0_AP)
  tiempos[[mt$id]] <- r2(as.numeric(difftime(Sys.time(), t0, units = "secs")))
  cat("   ", mt$id, "listo\n")
}

tabla_backtest <- lapply(metodos_bt, function(mt) {
  s <- resume_om(oms[[mt$id]], ap, T0_AP, M)
  c(list(id = mt$id, metodo = mt$nombre, referencia = mt$ref,
         segundos = tiempos[[mt$id]]), s)
})

# Reconciliación con el capítulo 5: aquel publicó el RMSE MEDIO DE LOS ORÍGENES
# de snaive, sarima, ets_log y stl sobre estos mismos 61 orígenes. Si las dos
# cifras no coinciden, una de las dos está mal y el estudiante lo va a ver.
cap5 <- list(snaive = 41.238, sarima = 16.812, ets = 21.416, stl = 21.848)
recon <- lapply(names(cap5), function(id) {
  mio <- Filter(function(z) z$id == id, tabla_backtest)[[1]]$rmse_medio_origenes
  list(id = id, cap5 = cap5[[id]], cap6 = mio, diferencia = r4(mio - cap5[[id]]))
})
cat("   reconciliación con el capítulo 5 (RMSE medio de los orígenes):\n")
for (z in recon) cat(sprintf("      %-8s cap5 %8.3f | cap6 %8.3f | dif %+.4f\n",
                             z$id, z$cap5, z$cap6, z$diferencia))

# El punto del componente .tabla-ranking: el orden cambia según la columna.
orden_por <- function(campo, menor_mejor = TRUE) {
  v <- sapply(tabla_backtest, function(z) z[[campo]])
  sapply(tabla_backtest, function(z) z$id)[order(v, decreasing = !menor_mejor)]
}
ordenes <- list(
  rmse = orden_por("rmse"), mae = orden_por("mae"), mape = orden_por("mape"),
  mase = orden_por("mase"), smape = orden_por("smape"),
  cob95 = sapply(tabla_backtest, function(z) z$id)[
    order(abs(sapply(tabla_backtest, function(z) z$cob95) - 95))],
  winkler95 = orden_por("winkler95"), segundos = orden_por("segundos")
)

# --- Diebold-Mariano: ¿la diferencia es real o es ruido? -------------------
# Se compara el SARIMA con cada rival usando los errores del MISMO horizonte
# sobre los MISMOS orígenes. h > 1 exige la corrección de Harvey-Leybourne-Newbold,
# que dm.test aplica con el argumento h.
dm_de <- function(id_a, id_b, h) {
  ea <- oms[[id_a]]$error[, h]; eb <- oms[[id_b]]$error[, h]
  ok <- !is.na(ea) & !is.na(eb)
  # El estimador de varianza por defecto ("acf") puede salir NEGATIVO cuando la
  # autocovarianza muestral de la diferencia de pérdidas lo es; dm.test avisa y
  # sigue con h = 1, que no es lo que se le pidió. El estimador de Bartlett está
  # garantizado no negativo. Se usa el de defecto y se cae al de Bartlett solo
  # si hace falta, dejando anotado cuál se usó.
  est <- "acf"
  p <- withCallingHandlers(
    try(dm.test(ea[ok], eb[ok], alternative = "two.sided", h = h, power = 2), silent = TRUE),
    warning = function(w) { est <<- "bartlett"; invokeRestart("muffleWarning") })
  if (est == "bartlett" || inherits(p, "try-error")) {
    p <- try(dm.test(ea[ok], eb[ok], alternative = "two.sided", h = h, power = 2,
                     varestimator = "bartlett"), silent = TRUE)
    est <- "bartlett"
  }
  if (inherits(p, "try-error")) return(NULL)
  list(a = id_a, b = id_b, h = h, n = sum(ok), varestimator = est,
       rmse_a = r4(sqrt(mean(ea[ok]^2))), rmse_b = r4(sqrt(mean(eb[ok]^2))),
       estadistico = r4(p$statistic), p = r4(p$p.value),
       significativo = p$p.value < 0.05)
}
dm_pruebas <- list()
for (id in c("snaive", "deriva", "ets", "stl", "auto")) {
  for (h in c(1, 6, 12)) {
    z <- dm_de("sarima", id, h)
    if (!is.null(z)) dm_pruebas[[length(dm_pruebas) + 1]] <- z
  }
}
n_sig <- sum(sapply(dm_pruebas, function(z) z$significativo))
cat("   Diebold-Mariano:", n_sig, "de", length(dm_pruebas), "comparaciones significativas\n")

# Fracción de orígenes en los que el SARIMA le gana a cada rival (RMSE del origen)
gana_por_origen <- lapply(metodos_bt, function(mt) {
  if (mt$id == "sarima") return(NULL)
  a <- sqrt(rowMeans(oms[["sarima"]]$error^2, na.rm = TRUE))
  b <- sqrt(rowMeans(oms[[mt$id]]$error^2, na.rm = TRUE))
  ok <- !is.na(a) & !is.na(b)
  list(id = mt$id, metodo = mt$nombre,
       gana_sarima = r4(100 * mean(a[ok] < b[ok])), n = sum(ok))
})
gana_por_origen <- Filter(Negate(is.null), gana_por_origen)

# Datos para la animación del origen móvil: tres métodos, todos los orígenes.
animacion <- list(
  fechas = sapply(seq_along(ap), function(i) etiqueta_fecha(ap, i)),
  serie = as.numeric(ap),
  T0 = T0_AP, h = H,
  origenes = lapply(seq_along(om_sarima_exp$origenes), function(i) list(
    T = om_sarima_exp$origenes[i],
    fecha = etiqueta_fecha(ap, om_sarima_exp$origenes[i]),
    reales = r2(om_sarima_exp$reales[i, ]),
    sarima = r2(om_sarima_exp$pron[i, ]),
    sarima_li95 = r2(om_sarima_exp$li95[i, ]),
    sarima_ls95 = r2(om_sarima_exp$ls95[i, ]),
    snaive = r2(oms[["snaive"]]$pron[i, ]),
    ets    = r2(oms[["ets"]]$pron[i, ]),
    # la misma serie con ventana deslizante, para el interruptor del simulador
    sarima_desl = r2(om_sarima_desl$pron[i, ]),
    ventana_desl = 72
  ))
)

# Diferencias de pérdida d_i = e_sarima^2 - e_rival^2 en cada origen, que es lo
# que de verdad contrasta Diebold-Mariano. Sin ellas el simulador solo podría
# mostrar el p-valor, que es justo lo que no hay que mirar a solas.
dm_diferencias <- lapply(c("snaive", "deriva", "ets", "stl", "auto"), function(id) {
  list(id = id,
       nombre = Filter(function(z) z$id == id, metodos_bt)[[1]]$nombre,
       h = lapply(c(1, 6, 12), function(h) {
         a <- om_sarima_exp$error[, h]; b <- oms[[id]]$error[, h]
         list(h = h, d = r4(a^2 - b^2))
       }))
})

# ============================================================================
# SECCIÓN H — Evaluación del intervalo: cobertura y Winkler  (módulo 9)
# ============================================================================
cat("H. Cobertura y Winkler...\n")

cobertura_por_h <- function(om, nivel) {
  li <- if (nivel == 80) om$li80 else om$li95
  ls <- if (nivel == 80) om$ls80 else om$ls95
  sapply(1:H, function(h) {
    ok <- !is.na(om$reales[, h])
    r4(100 * mean(om$reales[ok, h] >= li[ok, h] & om$reales[ok, h] <= ls[ok, h]))
  })
}

intervalos <- list(
  metodos = lapply(metodos_bt, function(mt) {
    om <- oms[[mt$id]]; ok <- !is.na(om$error)
    list(id = mt$id, metodo = mt$nombre,
         cob80 = r4(100 * cobertura(om$reales[ok], om$li80[ok], om$ls80[ok])),
         cob95 = r4(100 * cobertura(om$reales[ok], om$li95[ok], om$ls95[ok])),
         cob80_h = cobertura_por_h(om, 80),
         cob95_h = cobertura_por_h(om, 95),
         winkler80 = r4(mean(winkler(om$reales[ok], om$li80[ok], om$ls80[ok], 80))),
         winkler95 = r4(mean(winkler(om$reales[ok], om$li95[ok], om$ls95[ok], 95))),
         ancho95 = r4(mean(om$ls95[ok] - om$li95[ok])))
  }),
  nominal80 = 80, nominal95 = 95
)

# Normalidad de los residuales: el supuesto del que cuelga el intervalo.
normalidad <- lapply(list(
  list(id = "airpassengers", nombre = "log(AirPassengers), airline",
       r = residuals(Arima(ap, order = c(0,1,1), seasonal = c(0,1,1), lambda = 0))),
  list(id = "trm", nombre = "TRM, ARIMA(0,1,0)",
       r = residuals(Arima(trm, order = c(0, 1, 0)))),
  list(id = "nilo", nombre = "Nilo, ARIMA(1,1,1)",
       r = residuals(Arima(nilo, order = c(1, 1, 1))))
), function(z) {
  r <- as.numeric(z$r)
  list(id = z$id, nombre = z$nombre, n = length(r),
       shapiro_p = r4(shapiro.test(r)$p.value),
       jarque_bera_p = r4(jarque.bera.test(r)$p.value),
       curtosis = r4(mean(((r - mean(r)) / sd(r))^4)),
       asimetria = r4(mean(((r - mean(r)) / sd(r))^3)),
       # cuántos residuales estandarizados caen fuera de +-1.96, si fueran
       # normales serían el 5 %
       fuera_196 = r4(100 * mean(abs((r - mean(r)) / sd(r)) > 1.96)))
})
cat("   normalidad (Shapiro p):",
    paste(sapply(normalidad, function(z) sprintf("%s=%.4f", z$id, z$shapiro_p)),
          collapse = " | "), "\n")

# Simulador de Winkler: un intervalo que se mueve sobre un valor observado fijo.
winkler_demo <- local({
  real <- 100
  anchos <- seq(4, 120, by = 4)
  centros <- seq(60, 140, by = 5)
  list(real = real, anchos = anchos, centros = centros,
       nivel = 95,
       # matriz centro x ancho del puntaje, para que el simulador la lea directo
       puntaje = lapply(centros, function(c0) r4(sapply(anchos, function(a)
         winkler(real, c0 - a / 2, c0 + a / 2, 95)))))
})

# ============================================================================
# SECCIÓN I — Los tres casos  (módulo 10)
# ============================================================================
cat("I. Los tres casos...\n")

# --- I1. TRM: nadie vence al naive ----------------------------------------
T0_TRM <- 90
metodos_trm <- list(
  list(id = "naive",  nombre = "Naive",            f = m_naive),
  list(id = "media",  nombre = "Media",            f = m_media),
  list(id = "deriva", nombre = "Deriva",           f = m_deriva),
  list(id = "snaive", nombre = "Naive estacional", f = m_snaive),
  list(id = "ets",    nombre = "ETS",              f = m_ets_n),
  list(id = "auto",   nombre = "auto.arima",       f = m_auto_n)
)
tabla_trm <- lapply(metodos_trm, function(mt) {
  om <- origen_movil(trm, mt$f, T0 = T0_TRM)
  c(list(id = mt$id, metodo = mt$nombre), resume_om(om, trm, T0_TRM, M))
})
orden_trm <- sapply(tabla_trm, function(z) z$id)[order(sapply(tabla_trm, function(z) z$rmse))]
cat("   TRM, orden por RMSE:", paste(orden_trm, collapse = " > "), "\n")

# --- I2. Nilo: la partición única corona al naive; el origen móvil no ------
# Se replica EXACTAMENTE la partición del capítulo 4 (corte en 1950, 80 de
# entrenamiento, h = 20), para que las cifras enlacen con las que ya publicó
# ese capítulo, y luego se hace lo que el capítulo 6 exige: origen móvil.
n_nilo <- length(nilo); h_nilo <- 20
tr_nilo <- subset(nilo, start = 1, end = n_nilo - h_nilo)
te_nilo <- as.numeric(nilo)[(n_nilo - h_nilo + 1):n_nilo]
nilo_particion <- lapply(list(
  list(id = "arima111", nombre = "ARIMA(1,1,1)", f = m_arima_n),
  list(id = "naive",    nombre = "Naive",        f = m_naive),
  list(id = "media",    nombre = "Media",        f = m_media),
  list(id = "deriva",   nombre = "Deriva",       f = m_deriva),
  list(id = "auto",     nombre = "auto.arima",   f = m_auto_n)
), function(mt) {
  fc <- mt$f(tr_nilo, h_nilo)
  c(list(id = mt$id, metodo = mt$nombre,
         cobertura95 = r4(100 * cobertura(te_nilo, fc$li95, fc$ls95)),
         winkler95 = r4(mean(winkler(te_nilo, fc$li95, fc$ls95, 95)))),
    metricas(te_nilo, fc$media, tr_nilo, 1))
})

T0_NILO <- 60; H_NILO <- 5
tabla_nilo <- lapply(list(
  list(id = "arima111", nombre = "ARIMA(1,1,1)", f = m_arima_n),
  list(id = "naive",    nombre = "Naive",        f = m_naive),
  list(id = "media",    nombre = "Media",        f = m_media),
  list(id = "deriva",   nombre = "Deriva",       f = m_deriva),
  list(id = "auto",     nombre = "auto.arima",   f = m_auto_n)
), function(mt) {
  om <- origen_movil(nilo, mt$f, T0 = T0_NILO, h = H_NILO)
  e <- as.numeric(om$error); r <- as.numeric(om$reales); ok <- !is.na(e)
  entrena <- subset(nilo, start = 1, end = T0_NILO)
  list(id = mt$id, metodo = mt$nombre,
       n_origenes = length(om$origenes), n_errores = sum(ok),
       rmse = r4(sqrt(mean(e[ok]^2))), mae = r4(mean(abs(e[ok]))),
       mape = r4(100 * mean(abs(e[ok] / r[ok]))),
       mase = r4(mean(abs(e[ok])) / escala_mase(entrena, 1)),
       cob95 = r4(100 * cobertura(om$reales[ok], om$li95[ok], om$ls95[ok])),
       winkler95 = r4(mean(winkler(om$reales[ok], om$li95[ok], om$ls95[ok], 95))),
       rmse_h = r4(sqrt(colMeans(om$error^2, na.rm = TRUE))))
})
orden_nilo <- sapply(tabla_nilo, function(z) z$id)[order(sapply(tabla_nilo, function(z) z$rmse))]
cat("   Nilo (partición) RMSE:",
    paste(sapply(nilo_particion, function(z) sprintf("%s=%.2f", z$id, z$rmse)), collapse = " | "), "\n")
cat("   Nilo (origen móvil) orden:", paste(orden_nilo, collapse = " > "), "\n")

# ============================================================================
# SECCIÓN J — Las cifras del taller de auditoría de IA  (módulo 11)
# ============================================================================
cat("J. Cifras del taller de auditoría...\n")

# Error 1: comparar AICc entre modelos con distinto d. Rejilla sobre el Nilo.
rej_nilo <- expand.grid(p = 0:2, d = 0:2, q = 0:2)
aicc_nilo <- lapply(seq_len(nrow(rej_nilo)), function(i) {
  g <- rej_nilo[i, ]
  aj <- try(Arima(nilo, order = c(g$p, g$d, g$q)), silent = TRUE)
  if (inherits(aj, "try-error")) return(NULL)
  list(modelo = sprintf("(%d,%d,%d)", g$p, g$d, g$q), d = g$d,
       aicc = r4(aj$aicc), nobs = aj$nobs)
})
aicc_nilo <- Filter(Negate(is.null), aicc_nilo)
mejor_global <- aicc_nilo[[which.min(sapply(aicc_nilo, function(z) z$aicc))]]
mejor_d1 <- local({
  sub <- Filter(function(z) z$d == 1, aicc_nilo)
  sub[[which.min(sapply(sub, function(z) z$aicc))]]
})
mejor_d0 <- local({
  sub <- Filter(function(z) z$d == 0, aicc_nilo)
  sub[[which.min(sapply(sub, function(z) z$aicc))]]
})

# Error 2: ADF sobre una serie estacional cruda. Se reportan las cifras sobre
# log(AirPassengers), que son las que ya publicó el módulo 6 del capítulo 2
# (-1.5325, p = 0.7711), y también las de la serie sin transformar, para que no
# haya dos números distintos rondando el material.
adf_defecto     <- suppressWarnings(adf.test(log(ap)))
adf_k12         <- suppressWarnings(adf.test(log(ap), k = 12))
adf_defecto_cru <- suppressWarnings(adf.test(ap))
adf_k12_cru     <- suppressWarnings(adf.test(ap, k = 12))

# Error 3: MAPE sobre serie que cruza cero -> ya está en `mape_cero`.
# Error 4: k-fold aleatorio -> ya está en `fuga_cv`.
# Error 5: reportar el error de entrenamiento como si fuera de pronóstico
#          -> ya está en `residual_vs_error`.

auditoria_ia <- list(
  error_aicc = list(
    n_modelos = length(aicc_nilo),
    mejor_global = mejor_global, mejor_d0 = mejor_d0, mejor_d1 = mejor_d1,
    nobs_por_d = sapply(0:2, function(d) aicc_nilo[[which(sapply(aicc_nilo, function(z) z$d) == d)[1]]]$nobs),
    diferencia = r4(mejor_d1$aicc - mejor_global$aicc)
  ),
  error_adf = list(
    serie = "log(AirPassengers), con tendencia y estacionalidad evidentes",
    k_defecto = adf_defecto$parameter, estadistico_defecto = r4(adf_defecto$statistic),
    p_defecto = r4(adf_defecto$p.value),
    k_12 = 12, estadistico_k12 = r4(adf_k12$statistic), p_k12 = r4(adf_k12$p.value),
    cruda = list(estadistico_defecto = r4(adf_defecto_cru$statistic),
                 p_defecto = r4(adf_defecto_cru$p.value),
                 estadistico_k12 = r4(adf_k12_cru$statistic),
                 p_k12 = r4(adf_k12_cru$p.value))
  ),
  error_mape = list(mape = mape_cero$mape, ape_maximo = mape_cero$ape_maximo,
                    mase = mape_cero$mase),
  error_cv = local({
    peor <- montajes[[which.max(sapply(montajes, function(z) z$optimismo_kfold))]]
    list(montaje = peor$nombre, rmse_kfold = peor$rmse_kfold,
         rmse_real = peor$rmse_bloque_final, optimismo = peor$optimismo_kfold,
         montaje_sin_fuga = montajes[[1]]$nombre,
         sin_fuga_optimismo = montajes[[1]]$optimismo_kfold)
  }),
  error_mase = verificacion$trampa_mase,
  error_entrenamiento = list(rmse_dentro = residual_vs_error$entrenamiento_completo$rmse,
                             rmse_fuera = res_exp$rmse,
                             razon = r4(res_exp$rmse / residual_vs_error$entrenamiento_completo$rmse))
)
cat("   AICc Nilo: mejor global", mejor_global$modelo, mejor_global$aicc,
    "| mejor con d=1", mejor_d1$modelo, mejor_d1$aicc, "\n")
cat("   ADF AirPassengers: k por defecto", adf_defecto$parameter, "p =", r4(adf_defecto$p.value),
    "| k=12 p =", r4(adf_k12$p.value), "\n")

# ============================================================================
# SECCIÓN K — Escritura
# ============================================================================

datos <- list(
  descripcion = paste0("Precálculos del Capítulo 6 (pronóstico, métricas de error y ",
                       "backtesting). Origen móvil con reajuste en cada origen; ",
                       "métricas implementadas a mano y verificadas contra ",
                       "forecast::accuracy. El capítulo 4 construye el intervalo y ",
                       "el 5 lo usa: aquí se evalúa."),
  generado = format(Sys.Date(), "%Y-%m-%d"),
  generador = "precalculo/genera_cap6.R",
  h = H, m = M, niveles = NIVELES,
  residual_vs_error = residual_vs_error,
  benchmarks = list(airpassengers = bench_ap),
  verificacion_metricas = verificacion,
  contraejemplos = list(
    rmse_vs_mae = list(n_origenes = length(om_snaive_ap$origenes),
                       n_inversiones = length(inversiones), casos = inversiones,
                       por_origen = errores_por_origen),
    sesgo_mape = sesgo_mape,
    mape_cero = mape_cero,
    cambio_escala = cambio_escala
  ),
  fuga = list(cv = fuga_cv, seleccion = seleccion_sobre_prueba),
  origen_movil = list(ventanas = ventanas, T0 = T0_AP,
                      primer_origen = etiqueta_fecha(ap, T0_AP),
                      tiempos = tiempos, animacion = animacion),
  backtest = list(tabla = tabla_backtest, ordenes = ordenes,
                  dm = dm_pruebas, dm_diferencias = dm_diferencias,
                  gana_por_origen = gana_por_origen,
                  reconciliacion_cap5 = recon),
  intervalos = intervalos,
  normalidad = normalidad,
  winkler_demo = winkler_demo,
  casos = list(
    trm = list(T0 = T0_TRM, primer_origen = etiqueta_fecha(trm, T0_TRM),
               tabla = tabla_trm, orden = orden_trm),
    nilo = list(particion = nilo_particion, h_particion = h_nilo,
                T0 = T0_NILO, h = H_NILO, tabla = tabla_nilo, orden = orden_nilo)
  ),
  auditoria_ia = auditoria_ia
)

ruta_json <- file.path(dir_salidas, "cap6_evaluacion.json")
write(toJSON(datos, auto_unbox = TRUE, digits = 8, na = "null", pretty = TRUE), ruta_json)

series_cap6 <- list(
  airpassengers = series_base$airpassengers,
  trm           = series_base$trm,
  nilo          = series_base$nilo,
  usaccdeaths   = series_base$usaccdeaths,
  co2           = series_base$co2
)
ruta_js <- file.path(dir_salidas, "cap6_datos.js")
write(paste0(
  "// Generado por precalculo/genera_cap6.R el ", format(Sys.Date(), "%Y-%m-%d"), "\n",
  "// Precalculos de pronostico y evaluacion (Capitulo 6). No editar a mano.\n",
  "const DATOS_CAP6 = ", toJSON(datos, auto_unbox = TRUE, digits = 8, na = "null"), ";\n",
  "const SERIES_CAP6 = ", toJSON(series_cap6, auto_unbox = TRUE, digits = 8, na = "null"), ";\n"
), ruta_js)

cat("\n=== Salidas ===\n")
cat(sprintf("   %s (%.1f KB)\n", basename(ruta_json), file.size(ruta_json) / 1024))
cat(sprintf("   %s (%.1f KB)\n", basename(ruta_js), file.size(ruta_js) / 1024))
cat("Listo.\n")
