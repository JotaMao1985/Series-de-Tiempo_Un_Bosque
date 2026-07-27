# ============================================================================
# genera_cap4.R — Precálculos del Capítulo 4 (modelos ARIMA y Box-Jenkins)
#
# Genera salidas/cap4_arima.json y salidas/cap4_datos.js con:
#   - Caudal del Nilo 1871-1970: identificación completa (correlogramas de la
#     serie y de sus diferencias, ADF/KPSS/PP, ndiffs), rejilla ARIMA(p,d,q)
#     con p,d,q en {0,1,2} agrupada POR d, diagnóstico del modelo final,
#     sobrediferenciación (theta -> -1) y el cambio de nivel de 1899
#   - Traza real de auto.arima(trace = TRUE) paso a paso y comparación contra
#     la búsqueda exhaustiva (stepwise = FALSE, approximation = FALSE)
#   - Formas del pronóstico a largo plazo según d y la constante, con bandas
#     80/95 %, y los pesos psi que generan la anchura del intervalo
#   - TRM mensual en NIVELES: caso completo de Box-Jenkins
#   - Puente al capítulo 5: ARIMA no estacional sobre log(AirPassengers)
#
# Script aparte de genera_datos.R / genera_cap2.R / genera_cap3.R por la misma
# razón: no volver a descargar la TRM ni a reajustar modelos de otros capítulos.
# Las series se leen de salidas/datos_series.json.
#
# Dependencias: jsonlite, tseries, forecast.
# Uso:  Rscript genera_cap4.R      (desde la carpeta precalculo/)
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

MAX_REZAGO <- 20   # rezagos de los correlogramas del capítulo
H_PRON     <- 30   # horizonte de los pronósticos del módulo de la forma
set.seed(2026)

series_base <- fromJSON(file.path(dir_salidas, "datos_series.json"),
                        simplifyVector = TRUE)

# ----------------------------------------------------------------------------
# 1. Ayudantes
# ----------------------------------------------------------------------------

# Correlogramas muestrales con las mismas definiciones que el JS del capítulo:
# stats::acf divide por n; stats::pacf resuelve Durbin-Levinson sobre la ACF.
correlogramas <- function(x, max_rezago = MAX_REZAGO) {
  n <- length(x)
  list(
    n     = n,
    banda = round(1.96 / sqrt(n), 4),
    acf   = round(as.numeric(acf(x,  lag.max = max_rezago, plot = FALSE)$acf)[-1], 4),
    pacf  = round(as.numeric(pacf(x, lag.max = max_rezago, plot = FALSE)$acf), 4)
  )
}

# AICc = AIC + 2k(k+1)/(n-k-1), con k = nº de coeficientes + 1 (sigma^2) y
# n = longitud EFECTIVA (n - d): es la que usa arima() para la verosimilitud.
aicc_de <- function(ajuste, n_efectivo) {
  k <- length(ajuste$coef) + 1
  as.numeric(ajuste$aic + 2 * k * (k + 1) / (n_efectivo - k - 1))
}

bic_de <- function(ajuste, n_efectivo) {
  k <- length(ajuste$coef) + 1
  as.numeric(ajuste$aic - 2 * k + log(n_efectivo) * k)
}

# Diferenciación que trata d = 0 aparte. `diff(x, differences = 0)` NO es la
# identidad en R: lanza un error. Es una trampa documentada del proyecto.
dif <- function(x, d) if (d == 0) x else diff(x, differences = d)

# Errores estándar de un ajuste de arima().
ee_de <- function(ajuste) sqrt(diag(ajuste$var.coef))

# Resumen de coeficientes en formato lista de listas (para el JSON).
coeficientes_de <- function(ajuste) {
  if (length(ajuste$coef) == 0) return(list())
  ee <- ee_de(ajuste)
  lapply(seq_along(ajuste$coef), function(i) list(
    nombre = names(ajuste$coef)[i],
    valor  = round(as.numeric(ajuste$coef[i]), 4),
    ee     = round(as.numeric(ee[i]), 4),
    t      = round(as.numeric(ajuste$coef[i] / ee[i]), 4)
  ))
}

# ----------------------------------------------------------------------------
# 2. Series de trabajo
# ----------------------------------------------------------------------------

nilo <- ts(series_base$nilo$valores, start = series_base$nilo$inicio[1], frequency = 1)
n_nilo <- length(nilo)

trm_inicio <- series_base$trm$inicio
trm <- ts(series_base$trm$valores, start = c(trm_inicio[1], trm_inicio[2]), frequency = 12)
n_trm <- length(trm)

ap <- ts(series_base$airpassengers$valores,
         start = c(series_base$airpassengers$inicio[1], series_base$airpassengers$inicio[2]),
         frequency = 12)
lap <- log(ap)

cat("Series cargadas: Nilo n =", n_nilo, "| TRM n =", n_trm, "| AirPassengers n =", length(ap), "\n")

# ============================================================================
# 3. NILO — Identificación
# ============================================================================

identificacion <- list(
  cruda = correlogramas(as.numeric(nilo)),
  d1    = correlogramas(as.numeric(dif(nilo, 1))),
  d2    = correlogramas(as.numeric(dif(nilo, 2)))
)

# Pruebas de raíz unitaria. El Nilo es ANUAL: no hay estacionalidad que pueda
# desbaratar el ADF (la trampa del capítulo 2), así que aquí sí es aplicable.
pruebas <- list(
  adf_nivel  = list(estadistico = round(as.numeric(adf.test(nilo)$statistic), 4),
                    p = round(adf.test(nilo)$p.value, 4),
                    rezagos = as.numeric(adf.test(nilo)$parameter)),
  adf_d1     = list(estadistico = round(as.numeric(adf.test(dif(nilo, 1))$statistic), 4),
                    p = round(adf.test(dif(nilo, 1))$p.value, 4),
                    rezagos = as.numeric(adf.test(dif(nilo, 1))$parameter)),
  kpss_nivel = list(estadistico = round(as.numeric(kpss.test(nilo)$statistic), 4),
                    p = round(kpss.test(nilo)$p.value, 4)),
  kpss_d1    = list(estadistico = round(as.numeric(kpss.test(dif(nilo, 1))$statistic), 4),
                    p = round(kpss.test(dif(nilo, 1))$p.value, 4)),
  pp_nivel   = list(estadistico = round(as.numeric(PP.test(nilo)$statistic), 4),
                    p = round(PP.test(nilo)$p.value, 4)),
  ndiffs_kpss = ndiffs(nilo, test = "kpss"),
  ndiffs_adf  = ndiffs(nilo, test = "adf"),
  ndiffs_pp   = ndiffs(nilo, test = "pp")
)

# Varianza por orden de diferenciación: el criterio de "no pasarse".
varianzas <- lapply(0:3, function(d) list(
  d = d,
  varianza = round(var(dif(nilo, d)), 2),
  n_efectivo = length(dif(nilo, d))
))

cat("\n=== NILO: identificación ===\n")
cat(sprintf("ADF nivel: %.4f (p = %.4f, k = %d) | KPSS nivel: %.4f (p = %.4f)\n",
            pruebas$adf_nivel$estadistico, pruebas$adf_nivel$p, pruebas$adf_nivel$rezagos,
            pruebas$kpss_nivel$estadistico, pruebas$kpss_nivel$p))
cat(sprintf("ADF d=1  : %.4f (p = %.4f)          | KPSS d=1  : %.4f (p = %.4f)\n",
            pruebas$adf_d1$estadistico, pruebas$adf_d1$p,
            pruebas$kpss_d1$estadistico, pruebas$kpss_d1$p))
cat(sprintf("ndiffs: kpss = %d, adf = %d, pp = %d\n",
            pruebas$ndiffs_kpss, pruebas$ndiffs_adf, pruebas$ndiffs_pp))
for (v in varianzas) cat(sprintf("   var(d = %d) = %10.2f  (n = %d)\n", v$d, v$varianza, v$n_efectivo))

# ============================================================================
# 4. NILO — Rejilla ARIMA(p,d,q), p,d,q en {0,1,2}
# ============================================================================
# El AICc NO es comparable entre modelos con distinto d: la verosimilitud se
# calcula sobre series de longitudes distintas (n - d observaciones). Por eso
# la salida reporta el mejor POR CADA d y nunca un mínimo global.

ajusta_modelo <- function(x, p, d, q, incluir_media = NULL) {
  if (is.null(incluir_media)) incluir_media <- (d == 0)
  tryCatch({
    fit <- arima(x, order = c(p, d, q), method = "ML", include.mean = incluir_media)
    n_ef <- length(x) - d
    gl   <- p + q
    lb   <- if (MAX_REZAGO > gl)
      Box.test(residuals(fit), lag = MAX_REZAGO, type = "Ljung-Box", fitdf = gl) else NULL
    lb12 <- if (12 > gl)
      Box.test(residuals(fit), lag = 12, type = "Ljung-Box", fitdf = gl) else NULL
    list(
      p = p, d = d, q = q,
      etiqueta = sprintf("ARIMA(%d,%d,%d)", p, d, q),
      convergio = fit$code == 0,
      k = length(fit$coef) + 1,
      n_efectivo = n_ef,
      loglik = round(as.numeric(fit$loglik), 4),
      sigma2 = round(as.numeric(fit$sigma2), 2),
      aic  = round(as.numeric(fit$aic), 2),
      aicc = round(aicc_de(fit, n_ef), 2),
      bic  = round(bic_de(fit, n_ef), 2),
      ljung_box_p    = if (!is.null(lb)) round(as.numeric(lb$p.value), 4) else NA,
      ljung_box_12_p = if (!is.null(lb12)) round(as.numeric(lb12$p.value), 4) else NA,
      acf_residuales = round(as.numeric(acf(residuals(fit), lag.max = MAX_REZAGO,
                                            plot = FALSE)$acf)[-1], 4),
      coeficientes = coeficientes_de(fit),
      # Módulo de las raíces de phi(B) y theta(B). Un módulo <= 1.001 significa
      # raíz sobre el círculo unitario: el ajuste es degenerado (no invertible
      # o no estacionario) por mucho que gane en AICc. auto.arima los descarta.
      raices = {
        ar_c <- fit$coef[grepl("^ar", names(fit$coef))]
        ma_c <- fit$coef[grepl("^ma", names(fit$coef))]
        mod_ar <- if (length(ar_c)) round(Mod(polyroot(c(1, -ar_c))), 4) else numeric(0)
        mod_ma <- if (length(ma_c)) round(Mod(polyroot(c(1,  ma_c))), 4) else numeric(0)
        list(
          ar = as.numeric(mod_ar), ma = as.numeric(mod_ma),
          min_ar = if (length(mod_ar)) min(mod_ar) else NA,
          min_ma = if (length(mod_ma)) min(mod_ma) else NA,
          degenerado = (length(mod_ar) > 0 && min(mod_ar) <= 1.001) ||
                       (length(mod_ma) > 0 && min(mod_ma) <= 1.001)
        )
      }
    )
  }, error = function(e) list(
    p = p, d = d, q = q, etiqueta = sprintf("ARIMA(%d,%d,%d)", p, d, q),
    convergio = FALSE, error = conditionMessage(e)
  ))
}

rejilla <- list()
for (d in 0:2) for (p in 0:2) for (q in 0:2) {
  clave <- paste0(p, d, q)
  rejilla[[clave]] <- ajusta_modelo(nilo, p, d, q)
}

mejor_por_d <- list()
for (d in 0:2) {
  cand <- Filter(function(m) m$d == d && isTRUE(m$convergio), rejilla)
  aiccs <- sapply(cand, `[[`, "aicc")
  bics  <- sapply(cand, `[[`, "bic")
  mejor_por_d[[paste0("d", d)]] <- list(
    d = d,
    n_efectivo = length(nilo) - d,
    mejor_aicc = names(cand)[which.min(aiccs)],
    valor_aicc = round(min(aiccs), 2),
    mejor_bic  = names(cand)[which.min(bics)],
    valor_bic  = round(min(bics), 2)
  )
}

cat("\n=== NILO: rejilla ARIMA(p,d,q) ===\n")
cat(sprintf("%-16s %6s %9s %9s %9s %9s\n", "modelo", "n_ef", "loglik", "AICc", "BIC", "LB(20) p"))
for (m in rejilla) {
  if (!isTRUE(m$convergio)) { cat(sprintf("%-16s  NO CONVERGE\n", m$etiqueta)); next }
  marca <- ""
  md <- mejor_por_d[[paste0("d", m$d)]]
  if (paste0(m$p, m$d, m$q) == md$mejor_aicc) marca <- paste0(marca, "  <- min AICc (d=", m$d, ")")
  if (paste0(m$p, m$d, m$q) == md$mejor_bic)  marca <- paste0(marca, "  <- min BIC (d=", m$d, ")")
  cat(sprintf("%-16s %6d %9.2f %9.2f %9.2f %9.4f%s\n",
              m$etiqueta, m$n_efectivo, m$loglik, m$aicc, m$bic, m$ljung_box_p, marca))
}
cat("\nAVISO METODOLOGICO: las columnas AICc/BIC solo se comparan DENTRO de un mismo d.\n")
cat("   n efectivo: d=0 -> 100, d=1 -> 99, d=2 -> 98 observaciones.\n")

# ============================================================================
# 5. NILO — Modelo final y diagnóstico
# ============================================================================

final <- arima(nilo, order = c(1, 1, 1), method = "ML")
res_final <- as.numeric(residuals(final))

lb_acumulado <- lapply(3:MAX_REZAGO, function(h) {
  b <- Box.test(res_final, lag = h, type = "Ljung-Box", fitdf = 2)
  list(rezago = h, Q = round(as.numeric(b$statistic), 4), p = round(as.numeric(b$p.value), 4))
})

diagnostico <- list(
  orden = c(1, 1, 1),
  coeficientes = coeficientes_de(final),
  sigma2 = round(as.numeric(final$sigma2), 2),
  loglik = round(as.numeric(final$loglik), 4),
  aicc = round(aicc_de(final, n_nilo - 1), 2),
  bic  = round(bic_de(final, n_nilo - 1), 2),
  residuales = round(res_final, 3),
  acf_residuales = round(as.numeric(acf(res_final, lag.max = MAX_REZAGO, plot = FALSE)$acf)[-1], 4),
  banda_residuales = round(1.96 / sqrt(length(res_final)), 4),
  ljung_box_acumulado = lb_acumulado,
  ljung_box_20 = list(
    Q = round(as.numeric(Box.test(res_final, lag = 20, type = "Ljung-Box", fitdf = 2)$statistic), 4),
    p = round(as.numeric(Box.test(res_final, lag = 20, type = "Ljung-Box", fitdf = 2)$p.value), 4)),
  ljung_box_10 = list(
    Q = round(as.numeric(Box.test(res_final, lag = 10, type = "Ljung-Box", fitdf = 2)$statistic), 4),
    p = round(as.numeric(Box.test(res_final, lag = 10, type = "Ljung-Box", fitdf = 2)$p.value), 4)),
  shapiro_p = round(as.numeric(shapiro.test(res_final)$p.value), 4),
  media_residual = round(mean(res_final), 4),
  ee_media_residual = round(sd(res_final) / sqrt(length(res_final)), 4),
  # Raíces del polinomio característico, NO sus inversas: phi(B) = 1 - phi B se
  # anula en B = 1/phi. Estacionariedad/invertibilidad piden |B| > 1.
  raices = list(
    ar_modulo = round(Mod(polyroot(c(1, -final$coef["ar1"]))[1]), 4),
    ma_modulo = round(Mod(polyroot(c(1,  final$coef["ma1"]))[1]), 4)
  )
)

cat("\n=== NILO: modelo final ARIMA(1,1,1) ===\n")
for (cf in diagnostico$coeficientes)
  cat(sprintf("   %-6s %8.4f  (e.e. %.4f, t = %6.2f)\n", cf$nombre, cf$valor, cf$ee, cf$t))
cat(sprintf("   sigma^2 = %.2f | AICc = %.2f | BIC = %.2f\n",
            diagnostico$sigma2, diagnostico$aicc, diagnostico$bic))
cat(sprintf("   Ljung-Box(10) p = %.4f | Ljung-Box(20) p = %.4f | Shapiro p = %.4f\n",
            diagnostico$ljung_box_10$p, diagnostico$ljung_box_20$p, diagnostico$shapiro_p))
cat(sprintf("   |raiz AR| = %.4f (>1: estacionario tras diferenciar) | |raiz MA| = %.4f (>1: invertible)\n",
            diagnostico$raices$ar_modulo, diagnostico$raices$ma_modulo))

# ---- arima(ML) frente a Arima(CSS-ML): mismos coeficientes, distinta sigma^2 --
final_cssml <- Arima(nilo, order = c(1, 1, 1))     # método por defecto de forecast
metodos_estimacion <- list(
  ml = list(ar1 = round(as.numeric(final$coef["ar1"]), 6),
            ma1 = round(as.numeric(final$coef["ma1"]), 6),
            sigma2 = round(as.numeric(final$sigma2), 2)),
  css_ml = list(ar1 = round(as.numeric(coef(final_cssml)["ar1"]), 6),
                ma1 = round(as.numeric(coef(final_cssml)["ma1"]), 6),
                sigma2 = round(as.numeric(final_cssml$sigma2), 2)),
  dif_relativa_sigma2 = round(abs(final_cssml$sigma2 - final$sigma2) / final$sigma2, 5),
  nota = paste("stats::arima(method='ML') y forecast::Arima() (CSS-ML por defecto)",
               "dan coeficientes iguales a 5 decimales pero sigma^2 distinta:",
               "el ancho de los intervalos hereda esa diferencia.")
)
diagnostico$metodos_estimacion <- metodos_estimacion
cat(sprintf("   ML vs CSS-ML: coeficientes iguales a 5 decimales, sigma^2 %.2f vs %.2f (%.2f%%)\n",
            metodos_estimacion$ml$sigma2, metodos_estimacion$css_ml$sigma2,
            100 * metodos_estimacion$dif_relativa_sigma2))

# ---- El cambio de nivel de 1899 (presa de Asuán) ---------------------------
# Alternativa honesta a diferenciar: modelar el escalón explícitamente.
escalon <- as.numeric(time(nilo) >= 1899)
fit_escalon <- arima(nilo, order = c(0, 0, 0), xreg = escalon, method = "ML")
fit_escalon_ar <- arima(nilo, order = c(1, 0, 0), xreg = escalon, method = "ML")
res_esc <- as.numeric(residuals(fit_escalon))

cambio_nivel <- list(
  anio = 1899,
  fuente = "Cobb (1978); el descenso coincide con la construcción de la presa baja de Asuán",
  media_antes = round(mean(nilo[time(nilo) < 1899]), 2),
  media_despues = round(mean(nilo[time(nilo) >= 1899]), 2),
  escalon = list(
    coef = round(as.numeric(fit_escalon$coef["escalon"]), 2),
    ee   = round(as.numeric(sqrt(diag(fit_escalon$var.coef))["escalon"]), 2),
    t    = round(as.numeric(fit_escalon$coef["escalon"] /
                            sqrt(diag(fit_escalon$var.coef))["escalon"]), 2),
    aicc = round(aicc_de(fit_escalon, n_nilo), 2),
    bic  = round(bic_de(fit_escalon, n_nilo), 2),
    ljung_box_20_p = round(as.numeric(Box.test(res_esc, lag = 20, type = "Ljung-Box",
                                               fitdf = 0)$p.value), 4)
  ),
  escalon_ar1 = list(
    aicc = round(aicc_de(fit_escalon_ar, n_nilo), 2),
    bic  = round(bic_de(fit_escalon_ar, n_nilo), 2),
    ar1  = round(as.numeric(fit_escalon_ar$coef["ar1"]), 4),
    ar1_t = round(as.numeric(fit_escalon_ar$coef["ar1"] /
                             sqrt(diag(fit_escalon_ar$var.coef))["ar1"]), 2)
  ),
  # Comparación LEGÍTIMA: los dos modelos con escalón son d = 0, así que se
  # comparan entre sí y contra los d = 0 de la rejilla. NO contra el (1,1,1).
  mejor_d0_rejilla = mejor_por_d$d0$valor_aicc,
  advertencia = paste("El ARIMA(1,1,1) tiene d = 1: su AICc se calcula sobre 99",
                      "observaciones y NO es comparable con estos.")
)

# ---- Comparación LEGÍTIMA entre d distintos: fuera de muestra ---------------
# El AICc no cruza la frontera de d. Lo que sí la cruza es el error de
# pronóstico sobre datos que ningún modelo vio.
corte <- 1950                       # entrena 1871-1950 (80 años), prueba 20
ent <- window(nilo, end = corte)
pru <- window(nilo, start = corte + 1)
h_pru <- length(pru)
esc_ent <- as.numeric(time(ent) >= 1899)

compara_fuera <- function(etiqueta, pronostico) {
  e <- as.numeric(pru) - as.numeric(pronostico)
  list(etiqueta = etiqueta,
       rmse = round(sqrt(mean(e^2)), 2),
       mae  = round(mean(abs(e)), 2))
}

fc_arima <- forecast(Arima(ent, order = c(1, 1, 1)), h = h_pru)$mean
fc_esc   <- forecast(Arima(ent, order = c(0, 0, 0), xreg = esc_ent),
                     h = h_pru, xreg = rep(1, h_pru))$mean
fc_escar <- forecast(Arima(ent, order = c(1, 0, 0), xreg = esc_ent),
                     h = h_pru, xreg = rep(1, h_pru))$mean
fc_naive <- rep(as.numeric(ent[length(ent)]), h_pru)
fc_media <- rep(mean(ent), h_pru)

fuera_muestra <- list(
  corte = corte, n_entrenamiento = length(ent), h = h_pru,
  modelos = list(
    compara_fuera("ARIMA(1,1,1)", fc_arima),
    compara_fuera("Escalón 1899 (d = 0)", fc_esc),
    compara_fuera("Escalón 1899 + AR(1)", fc_escar),
    compara_fuera("Naïve (último valor)", fc_naive),
    compara_fuera("Media de la muestra", fc_media)
  ),
  nota = paste("Única comparación válida entre modelos con distinto d. La media",
               "de toda la muestra es un mal referente aquí porque mezcla los dos",
               "regímenes; el naïve y el escalón coinciden casi en todo porque",
               "ambos pronostican una constante cercana al nivel posterior a 1899.")
)
cambio_nivel$fuera_muestra <- fuera_muestra

cat("\n--- Comparación fuera de muestra (entrena hasta 1950, prueba 20 años) ---\n")
for (m in fuera_muestra$modelos)
  cat(sprintf("   %-24s RMSE = %7.2f | MAE = %7.2f\n", m$etiqueta, m$rmse, m$mae))
cat(sprintf("   sd de los residuales del ARIMA(1,1,1) = %.2f: el abanico de RMSE (%.0f-%.0f)\n",
            sd(res_final), min(sapply(fuera_muestra$modelos, `[[`, "rmse")),
            max(sapply(fuera_muestra$modelos, `[[`, "rmse"))))
cat("   es pequeño frente a él -> los modelos son prácticamente indistinguibles aquí.\n")

# ---- ¿Un cambio de nivel hace que KPSS vea una raíz unitaria? ---------------
# Hipótesis: la serie NO tiene raíz unitaria; tiene un escalón. KPSS no
# distingue una cosa de la otra, y como auto.arima elige d con KPSS, acaba
# diferenciando. Se comprueba simulando series estacionarias CON escalón.
mc_escalon <- function(n_rep = 1000, n = 100, delta, sigma, pos = 29) {
  escalon_sim <- as.numeric(seq_len(n) >= pos)
  cuenta <- function(delta_usado) {
    kpss_rechaza <- 0; nd_kpss <- integer(0); nd_adf <- integer(0)
    for (i in seq_len(n_rep)) {
      x <- 1000 + delta_usado * escalon_sim + rnorm(n, 0, sigma)
      p <- suppressWarnings(kpss.test(x)$p.value)
      if (p <= 0.05) kpss_rechaza <- kpss_rechaza + 1
      nd_kpss <- c(nd_kpss, suppressWarnings(ndiffs(x, test = "kpss")))
      nd_adf  <- c(nd_adf,  suppressWarnings(ndiffs(x, test = "adf")))
    }
    list(kpss_rechaza = round(kpss_rechaza / n_rep, 4),
         ndiffs_kpss_1_o_mas = round(mean(nd_kpss >= 1), 4),
         ndiffs_adf_1_o_mas  = round(mean(nd_adf  >= 1), 4))
  }
  list(n_replicas = n_rep, n = n, delta = round(delta, 2), sigma = round(sigma, 2),
       posicion_escalon = pos,
       sin_escalon = cuenta(0),
       con_escalon = cuenta(delta))
}

set.seed(2026)
monte_carlo <- mc_escalon(n_rep = 1000, n = n_nilo,
                          delta = as.numeric(fit_escalon$coef["escalon"]),
                          sigma = sd(res_esc),
                          pos = which(time(nilo) == 1899))
cambio_nivel$monte_carlo <- monte_carlo

cat("\n--- Monte Carlo: ¿confunde KPSS un escalón con una raíz unitaria? ---\n")
cat(sprintf("   %d réplicas de ruido blanco (n = %d, sigma = %.1f), escalón de %.1f en t = %d\n",
            monte_carlo$n_replicas, monte_carlo$n, monte_carlo$sigma,
            monte_carlo$delta, monte_carlo$posicion_escalon))
cat(sprintf("   SIN escalón: KPSS rechaza %.1f%% | ndiffs(kpss) >= 1 en %.1f%% | ndiffs(adf) >= 1 en %.1f%%\n",
            100 * monte_carlo$sin_escalon$kpss_rechaza,
            100 * monte_carlo$sin_escalon$ndiffs_kpss_1_o_mas,
            100 * monte_carlo$sin_escalon$ndiffs_adf_1_o_mas))
cat(sprintf("   CON escalón: KPSS rechaza %.1f%% | ndiffs(kpss) >= 1 en %.1f%% | ndiffs(adf) >= 1 en %.1f%%\n",
            100 * monte_carlo$con_escalon$kpss_rechaza,
            100 * monte_carlo$con_escalon$ndiffs_kpss_1_o_mas,
            100 * monte_carlo$con_escalon$ndiffs_adf_1_o_mas))
cat("   (por construcción NINGUNA de estas series tiene raíz unitaria)\n")

# Rejilla sobre el TAMAÑO del escalón, para el simulador del capítulo: el
# usuario mueve delta y ve cómo la tasa de rechazo de KPSS pasa de 5 % a 100 %
# sin que ninguna serie deje de ser estacionaria.
set.seed(2026)
sigma_mc <- sd(res_esc)
pos_mc <- which(time(nilo) == 1899)
escalon_mc <- as.numeric(seq_len(n_nilo) >= pos_mc)
deltas <- c(0, 25, 50, 75, 100, 150, 200, 250, 300)
N_REP_MALLA <- 400

malla_delta <- lapply(deltas, function(dl) {
  est <- numeric(N_REP_MALLA); rech <- 0; nd <- integer(N_REP_MALLA)
  for (i in seq_len(N_REP_MALLA)) {
    x <- 1000 + dl * escalon_mc + rnorm(n_nilo, 0, sigma_mc)
    k <- suppressWarnings(kpss.test(x))
    est[i] <- as.numeric(k$statistic)
    if (k$p.value <= 0.05) rech <- rech + 1
    nd[i] <- suppressWarnings(ndiffs(x, test = "kpss"))
  }
  list(delta = dl,
       kpss_medio = round(mean(est), 4),
       kpss_rechaza = round(rech / N_REP_MALLA, 4),
       ndiffs_medio = round(mean(nd), 4),
       salto_en_sigmas = round(dl / sigma_mc, 3))
})
cambio_nivel$malla_delta <- list(
  n_replicas = N_REP_MALLA, n = n_nilo, sigma = round(sigma_mc, 2),
  posicion = pos_mc, valor_critico_kpss_5 = 0.463,
  delta_del_nilo = round(abs(as.numeric(fit_escalon$coef["escalon"])), 2),
  puntos = malla_delta)

cat("\n--- Malla sobre el tamaño del escalón (para el simulador) ---\n")
cat(sprintf("%8s %10s %12s %12s %10s\n", "delta", "delta/sd", "KPSS medio", "% rechazo", "ndiffs"))
for (p in malla_delta)
  cat(sprintf("%8.0f %10.2f %12.4f %11.1f%% %10.2f\n",
              p$delta, p$salto_en_sigmas, p$kpss_medio,
              100 * p$kpss_rechaza, p$ndiffs_medio))

cat("\n=== NILO: el cambio de nivel de 1899 ===\n")
cat(sprintf("   media antes = %.2f | media después = %.2f | escalón = %.2f (e.e. %.2f, t = %.2f)\n",
            cambio_nivel$media_antes, cambio_nivel$media_despues,
            cambio_nivel$escalon$coef, cambio_nivel$escalon$ee, cambio_nivel$escalon$t))
cat(sprintf("   AICc del escalón solo = %.2f | con AR(1) = %.2f | mejor d=0 de la rejilla = %.2f\n",
            cambio_nivel$escalon$aicc, cambio_nivel$escalon_ar1$aicc,
            cambio_nivel$mejor_d0_rejilla))
cat(sprintf("   Ljung-Box(20) de los residuales del escalón: p = %.4f\n",
            cambio_nivel$escalon$ljung_box_20_p))

# ============================================================================
# 6. NILO — Sobrediferenciación
# ============================================================================
# Al diferenciar de más aparece una raíz unitaria en la parte MA: el theta
# estimado de un MA(1) se va hacia -1 y la varianza crece.

sobredif <- lapply(0:3, function(d) {
  x <- dif(nilo, d)
  ma1 <- tryCatch(arima(x, order = c(0, 0, 1), include.mean = (d == 0), method = "ML"),
                  error = function(e) NULL)
  list(
    d = d,
    n = length(x),
    varianza = round(var(x), 2),
    acf1 = round(as.numeric(acf(x, lag.max = 1, plot = FALSE)$acf)[2], 4),
    theta_ma1 = if (!is.null(ma1)) round(as.numeric(ma1$coef["ma1"]), 4) else NA,
    theta_ee  = if (!is.null(ma1)) round(as.numeric(sqrt(diag(ma1$var.coef))["ma1"]), 4) else NA,
    sigma2_ma1 = if (!is.null(ma1)) round(as.numeric(ma1$sigma2), 2) else NA
  )
})

cat("\n=== NILO: sobrediferenciación ===\n")
cat(sprintf("%3s %5s %12s %8s %10s %8s\n", "d", "n", "varianza", "ACF(1)", "theta MA(1)", "e.e."))
for (s in sobredif)
  cat(sprintf("%3d %5d %12.2f %8.4f %10.4f %8.4f\n",
              s$d, s$n, s$varianza, s$acf1, s$theta_ma1, s$theta_ee))
cat("   -> theta se acerca a -1: es la firma de haber diferenciado de más.\n")

# ============================================================================
# 7. NILO — Hyndman-Khandakar: traza real y búsqueda exhaustiva
# ============================================================================

# Parsea las líneas de traza de auto.arima:  " ARIMA(1,1,1)  with drift : 1263.1"
parsea_traza <- function(lineas) {
  pat <- "ARIMA\\(([0-9]+),([0-9]+),([0-9]+)\\)(\\([0-9]+,[0-9]+,[0-9]+\\)\\[[0-9]+\\])?[[:space:]]*(with drift|with non-zero mean|with zero mean|with[^:]*)?[[:space:]]*:[[:space:]]*([-0-9.]+|Inf)"
  pasos <- list()
  mejor <- Inf
  for (ln in lineas) {
    m <- regmatches(ln, regexec(pat, ln))[[1]]
    if (length(m) == 0) next
    valor <- suppressWarnings(as.numeric(m[7]))
    if (is.na(valor)) valor <- Inf
    extra <- trimws(ifelse(is.na(m[6]), "", m[6]))
    mejora <- is.finite(valor) && valor < mejor
    if (mejora) mejor <- valor
    pasos[[length(pasos) + 1]] <- list(
      orden = as.integer(c(m[2], m[3], m[4])),
      etiqueta = sprintf("ARIMA(%s,%s,%s)%s", m[2], m[3], m[4],
                         if (nzchar(extra)) paste0(" ", extra) else ""),
      constante = extra,
      aicc = if (is.finite(valor)) round(valor, 3) else NA,
      infinito = !is.finite(valor),
      mejora = mejora,
      mejor_hasta_aqui = round(mejor, 3)
    )
  }
  pasos
}

salida_paso <- capture.output(
  auto_paso <- auto.arima(nilo, trace = TRUE, stepwise = TRUE,
                          approximation = FALSE, seasonal = FALSE))
traza_paso <- parsea_traza(salida_paso)

salida_exh <- capture.output(
  auto_exh <- auto.arima(nilo, trace = TRUE, stepwise = FALSE,
                         approximation = FALSE, seasonal = FALSE))
traza_exh <- parsea_traza(salida_exh)

hk <- list(
  serie = "nilo",
  criterio = "AICc",
  escalonada = list(
    pasos = traza_paso,
    n_modelos = length(traza_paso),
    resultado = as.character(auto_paso),
    orden = as.integer(arimaorder(auto_paso)[1:3]),
    aicc = round(as.numeric(auto_paso$aicc), 3),
    incluye_deriva = "drift" %in% names(coef(auto_paso)),
    incluye_media  = "intercept" %in% names(coef(auto_paso))
  ),
  exhaustiva = list(
    pasos = traza_exh,          # el simulador del capítulo recorre las dos
    n_modelos = length(traza_exh),
    resultado = as.character(auto_exh),
    orden = as.integer(arimaorder(auto_exh)[1:3]),
    aicc = round(as.numeric(auto_exh$aicc), 3),
    # Los 5 mejores de la búsqueda completa, para ver cuán apretado está el ranking
    ranking = {
      finitos <- Filter(function(p) !p$infinito, traza_exh)
      ord <- order(sapply(finitos, `[[`, "aicc"))
      lapply(ord[1:min(5, length(ord))], function(i)
        list(etiqueta = finitos[[i]]$etiqueta, aicc = finitos[[i]]$aicc))
    }
  ),
  coinciden = identical(as.integer(arimaorder(auto_paso)[1:3]),
                        as.integer(arimaorder(auto_exh)[1:3])) &&
              (("drift" %in% names(coef(auto_paso))) == ("drift" %in% names(coef(auto_exh))))
)
hk$diferencia_aicc <- round(hk$escalonada$aicc - hk$exhaustiva$aicc, 3)

cat("\n=== NILO: Hyndman-Khandakar ===\n")
cat(sprintf("Búsqueda escalonada: %d modelos evaluados -> %s (AICc %.3f)\n",
            hk$escalonada$n_modelos, hk$escalonada$resultado, hk$escalonada$aicc))
for (p in traza_paso)
  cat(sprintf("   %-34s AICc %10s %s\n", p$etiqueta,
              if (p$infinito) "Inf" else sprintf("%.3f", p$aicc),
              if (p$mejora) "  <- mejora" else ""))
cat(sprintf("Búsqueda exhaustiva: %d modelos -> %s (AICc %.3f)\n",
            hk$exhaustiva$n_modelos, hk$exhaustiva$resultado, hk$exhaustiva$aicc))
cat("   Cinco mejores de la búsqueda completa:\n")
for (r in hk$exhaustiva$ranking) cat(sprintf("      %-34s %.3f\n", r$etiqueta, r$aicc))
cat(sprintf("   Coinciden: %s | diferencia de AICc = %.3f\n", hk$coinciden, hk$diferencia_aicc))

# ============================================================================
# 8. NILO — Forma del pronóstico según d y la constante
# ============================================================================
# d = 0 con media   -> vuelve a la media
# d = 1 sin deriva  -> se queda en el último nivel
# d = 1 con deriva  -> recta
# d = 2             -> curva (parábola)

forma_pronostico <- function(x, orden, deriva = FALSE, h = H_PRON, etiqueta) {
  fit <- if (deriva) Arima(x, order = orden, include.drift = TRUE)
         else if (orden[2] == 0) Arima(x, order = orden, include.mean = TRUE)
         else Arima(x, order = orden)
  fc <- forecast(fit, h = h, level = c(80, 95))
  list(
    etiqueta = etiqueta,
    orden = as.integer(orden),
    deriva = deriva,
    media = round(as.numeric(fc$mean), 2),
    lo80 = round(as.numeric(fc$lower[, 1]), 2),
    hi80 = round(as.numeric(fc$upper[, 1]), 2),
    lo95 = round(as.numeric(fc$lower[, 2]), 2),
    hi95 = round(as.numeric(fc$upper[, 2]), 2),
    aicc = round(as.numeric(fit$aicc), 2),
    sigma = round(sqrt(fit$sigma2), 3),
    coeficientes = {
      cf <- coef(fit); ee <- sqrt(diag(fit$var.coef))
      lapply(seq_along(cf), function(i) list(nombre = names(cf)[i],
                                             valor = round(as.numeric(cf[i]), 4),
                                             ee = round(as.numeric(ee[i]), 4)))
    }
  )
}

formas <- list(
  d0        = forma_pronostico(nilo, c(1, 0, 1), FALSE, H_PRON, "ARIMA(1,0,1) con media"),
  d1        = forma_pronostico(nilo, c(1, 1, 1), FALSE, H_PRON, "ARIMA(1,1,1) sin constante"),
  d1_deriva = forma_pronostico(nilo, c(1, 1, 1), TRUE,  H_PRON, "ARIMA(1,1,1) con deriva"),
  d2        = forma_pronostico(nilo, c(1, 2, 1), FALSE, H_PRON, "ARIMA(1,2,1)")
)

# ---- De dónde sale la anchura del intervalo --------------------------------
# ARIMA(1,1,1) sobre y_t equivale a un ARMA(2,1) sobre la serie SIN diferenciar
# con phi* = (1 + phi, -phi). Los pesos psi de esa representación dan
# sigma_h = sigma * sqrt(1 + psi_1^2 + ... + psi_{h-1}^2).
#
# OJO: los psi y sigma tienen que salir del MISMO ajuste que produjo el
# intervalo. formas$d1 se ajustó con forecast::Arima (CSS-ML por defecto) y
# `final` con stats::arima(method = "ML"): sus sigma^2 difieren un 2 % y la
# verificación falla por esa causa, no por la fórmula.
fit_int <- Arima(nilo, order = c(1, 1, 1))
phi_f <- as.numeric(coef(fit_int)["ar1"])
th_f  <- as.numeric(coef(fit_int)["ma1"])
sigma_f <- sqrt(as.numeric(fit_int$sigma2))
psi_f <- c(1, ARMAtoMA(ar = c(1 + phi_f, -phi_f), ma = th_f, lag.max = H_PRON))
sigma_h <- sigma_f * sqrt(cumsum(psi_f^2))[1:H_PRON]

# Verificación: la mitad del intervalo 95 % que devuelve forecast() debe ser
# qnorm(0.975) * sigma_h. Se comprueba SIN redondear (el JSON guarda 2
# decimales, y ese redondeo por sí solo mete un error de hasta 0.005).
fc_int <- forecast(fit_int, h = H_PRON, level = c(80, 95))
error_intervalo <- max(abs((fc_int$upper[, 2] - fc_int$lower[, 2]) / 2 -
                           qnorm(0.975) * sigma_h))
semiancho_fc <- (formas$d1$hi95 - formas$d1$lo95) / 2
error_intervalo_redondeado <- max(abs(semiancho_fc - qnorm(0.975) * sigma_h))

intervalos <- list(
  modelo = "ARIMA(1,1,1)",
  sigma = round(sigma_f, 3),
  psi = round(psi_f[1:(H_PRON)], 4),
  sigma_h = round(sigma_h, 3),
  z80 = round(qnorm(0.90), 4),
  z95 = round(qnorm(0.975), 4),
  semiancho_95 = round(semiancho_fc, 3),
  error_maximo_verificacion = signif(error_intervalo, 4),
  error_maximo_tras_redondear = signif(error_intervalo_redondeado, 4),
  # El intervalo NO crece como sqrt(h) cuando hay una raíz unitaria: crece
  # aproximadamente lineal, porque los pesos psi tienden a una constante.
  psi_limite = round(psi_f[H_PRON], 4),
  razon_h1_h30 = round(sigma_h[H_PRON] / sigma_h[1], 3)
)

# ---- ¿Qué FORMA tiene cada pronóstico? Medido, no recordado -----------------
# d = 0 con media -> converge a la media; d = 1 sin constante -> constante;
# d = 1 con deriva -> recta; d = 2 sin constante -> TAMBIÉN una recta (la
# segunda diferencia del pronóstico se anula), no una parábola.
forma_medida <- function(f, media_serie) {
  m <- f$media
  list(
    etiqueta = f$etiqueta,
    primera_dif_h2  = round(m[2] - m[1], 4),
    primera_dif_h30 = round(m[H_PRON] - m[H_PRON - 1], 4),
    segunda_dif_h30 = round(m[H_PRON] - 2 * m[H_PRON - 1] + m[H_PRON - 2], 6),
    distancia_a_la_media_h30 = round(abs(m[H_PRON] - media_serie), 2),
    ancho95_h1  = round(f$hi95[1] - f$lo95[1], 2),
    ancho95_h30 = round(f$hi95[H_PRON] - f$lo95[H_PRON], 2)
  )
}
formas_medidas <- lapply(formas, forma_medida, media_serie = mean(nilo))

# forecast se NIEGA a fitear el caso cuadrático: con d >= 2 ignora la deriva.
aviso_deriva_d2 <- tryCatch(
  withCallingHandlers({ Arima(nilo, order = c(1, 2, 1), include.drift = TRUE); "sin aviso" },
                      warning = function(w) invokeRestart("muffleWarning")),
  error = function(e) conditionMessage(e))
aviso_deriva_d2_texto <- {
  msg <- NULL
  withCallingHandlers(Arima(nilo, order = c(1, 2, 1), include.drift = TRUE),
                      warning = function(w) { msg <<- conditionMessage(w)
                                              invokeRestart("muffleWarning") })
  if (is.null(msg)) "(no avisó)" else msg
}
intervalos$forma_medida <- formas_medidas
intervalos$deriva_con_d2 <- list(
  se_ajusta = FALSE,
  aviso = aviso_deriva_d2_texto,
  nota = paste("forecast::Arima descarta la deriva cuando d >= 2. Por eso el",
               "pronóstico con d = 2 es una RECTA y no una parábola: el caso",
               "cuadrático existe en el álgebra, pero el software se niega a",
               "ajustarlo porque extrapola sin control.")
)

cat("\n=== NILO: forma del pronóstico e intervalos ===\n")
for (nm in names(formas)) {
  f <- formas[[nm]]
  cat(sprintf("   %-30s y_T+1 = %8.2f | y_T+30 = %8.2f | ancho95(h=30) = %8.2f\n",
              f$etiqueta, f$media[1], f$media[H_PRON], f$hi95[H_PRON] - f$lo95[H_PRON]))
}
cat(sprintf("   psi_j -> %.4f (constante, no 0: hay raíz unitaria)\n", intervalos$psi_limite))
cat(sprintf("   sigma_h: h=1 -> %.2f, h=30 -> %.2f (razón %.2f)\n",
            sigma_h[1], sigma_h[H_PRON], intervalos$razon_h1_h30))
cat(sprintf("   VERIFICACIÓN psi vs. forecast(): error máximo = %.2e (sin redondear) / %.2e (con el redondeo del JSON)\n",
            error_intervalo, error_intervalo_redondeado))
cat("   Forma MEDIDA de cada pronóstico (1ª y 2ª diferencia al final del horizonte):\n")
for (nm in names(formas_medidas)) {
  f <- formas_medidas[[nm]]
  cat(sprintf("      %-30s Δ(h=30) = %8.4f | Δ²(h=30) = %9.6f | ancho95 %.0f -> %.0f\n",
              f$etiqueta, f$primera_dif_h30, f$segunda_dif_h30, f$ancho95_h1, f$ancho95_h30))
}
cat(sprintf("   Deriva con d = 2: %s\n", intervalos$deriva_con_d2$aviso))

# ============================================================================
# 9. TRM en niveles — caso completo
# ============================================================================

trm_ident <- list(
  cruda = correlogramas(as.numeric(trm)),
  d1    = correlogramas(as.numeric(dif(trm, 1)))
)

trm_pruebas <- list(
  adf_nivel = list(estadistico = round(as.numeric(adf.test(trm)$statistic), 4),
                   p = round(adf.test(trm)$p.value, 4),
                   rezagos = as.numeric(adf.test(trm)$parameter)),
  kpss_nivel = list(estadistico = round(as.numeric(kpss.test(trm)$statistic), 4),
                    p = round(kpss.test(trm)$p.value, 4)),
  adf_d1 = list(estadistico = round(as.numeric(adf.test(dif(trm, 1))$statistic), 4),
                p = round(adf.test(dif(trm, 1))$p.value, 4)),
  kpss_d1 = list(estadistico = round(as.numeric(kpss.test(dif(trm, 1))$statistic), 4),
                 p = round(kpss.test(dif(trm, 1))$p.value, 4)),
  ndiffs = ndiffs(trm),
  nsdiffs = nsdiffs(trm)
)

# Rejilla pequeña sobre d = 1 (que es lo que dicen las pruebas)
trm_rejilla <- list()
for (p in 0:2) for (q in 0:2) {
  clave <- paste0(p, "1", q)
  trm_rejilla[[clave]] <- ajusta_modelo(trm, p, 1, q)
}
trm_aiccs <- sapply(Filter(function(m) isTRUE(m$convergio), trm_rejilla), `[[`, "aicc")
trm_bics  <- sapply(Filter(function(m) isTRUE(m$convergio), trm_rejilla), `[[`, "bic")

salida_trm <- capture.output(
  trm_auto <- auto.arima(trm, trace = TRUE, stepwise = FALSE,
                         approximation = FALSE, seasonal = TRUE))
trm_traza <- parsea_traza(salida_trm)

trm_rw <- arima(trm, order = c(0, 1, 0), method = "ML")
trm_rw_drift <- Arima(trm, order = c(0, 1, 0), include.drift = TRUE)
res_trm <- as.numeric(residuals(trm_rw))

trm_caso <- list(
  nombre = series_base$trm$nombre,
  fuente = series_base$trm$fuente,
  unidad = series_base$trm$unidad,
  n = n_trm,
  identificacion = trm_ident,
  pruebas = trm_pruebas,
  varianzas = lapply(0:2, function(d) list(d = d, varianza = round(var(dif(trm, d)), 2))),
  rejilla = trm_rejilla,
  mejor_aicc = names(trm_aiccs)[which.min(trm_aiccs)],
  mejor_bic  = names(trm_bics)[which.min(trm_bics)],
  auto_arima = list(
    resultado = as.character(trm_auto),
    orden = as.integer(arimaorder(trm_auto)[1:3]),
    estacional = length(arimaorder(trm_auto)) > 3,
    aicc = round(as.numeric(trm_auto$aicc), 3),
    n_modelos = length(trm_traza)
  ),
  caminata = list(
    sigma2 = round(as.numeric(trm_rw$sigma2), 2),
    aicc = round(aicc_de(trm_rw, n_trm - 1), 2),
    bic  = round(bic_de(trm_rw, n_trm - 1), 2),
    ljung_box_20_p = round(as.numeric(Box.test(res_trm, lag = 20, type = "Ljung-Box",
                                               fitdf = 0)$p.value), 4),
    ljung_box_12_p = round(as.numeric(Box.test(res_trm, lag = 12, type = "Ljung-Box",
                                               fitdf = 0)$p.value), 4),
    acf_residuales = round(as.numeric(acf(res_trm, lag.max = MAX_REZAGO, plot = FALSE)$acf)[-1], 4),
    shapiro_p = round(as.numeric(shapiro.test(res_trm)$p.value), 4)
  ),
  deriva = list(
    valor = round(as.numeric(coef(trm_rw_drift)["drift"]), 4),
    ee = round(as.numeric(sqrt(diag(trm_rw_drift$var.coef))["drift"]), 4),
    t = round(as.numeric(coef(trm_rw_drift)["drift"] /
                         sqrt(diag(trm_rw_drift$var.coef))["drift"]), 4),
    aicc = round(as.numeric(trm_rw_drift$aicc), 2)
  ),
  volatilidad = list(
    lb12_cuadrados_p = round(as.numeric(Box.test(res_trm^2, lag = 12,
                                                 type = "Ljung-Box")$p.value), 4)
  ),
  # El mínimo de AICc de la rejilla es un ajuste DEGENERADO: sus raíces caen
  # sobre el círculo unitario. Gana en AICc y hay que descartarlo igualmente;
  # es exactamente lo que hace auto.arima. Este es el punto del caso.
  minimo_degenerado = {
    m <- trm_rejilla[[names(trm_aiccs)[which.min(trm_aiccs)]]]
    list(
      etiqueta = m$etiqueta,
      aicc = m$aicc,
      ventaja_aicc = round(min(trm_aiccs) - trm_rejilla[["010"]]$aicc, 2),
      raices_ar = m$raices$ar,
      raices_ma = m$raices$ma,
      degenerado = m$raices$degenerado,
      motivo = paste("Las raíces del polinomio MA tienen módulo 1.000: el modelo",
                     "no es invertible. Las del AR quedan en 1.004, prácticamente",
                     "encima del círculo. auto.arima lo descarta por eso, aunque",
                     "sea el mínimo de AICc de la rejilla.")
    )
  }
)

cat("\n=== TRM en niveles ===\n")
cat(sprintf("ADF nivel %.4f (p = %.4f) | KPSS nivel %.4f (p = %.4f) | ndiffs = %d, nsdiffs = %d\n",
            trm_pruebas$adf_nivel$estadistico, trm_pruebas$adf_nivel$p,
            trm_pruebas$kpss_nivel$estadistico, trm_pruebas$kpss_nivel$p,
            trm_pruebas$ndiffs, trm_pruebas$nsdiffs))
cat(sprintf("ADF d=1   %.4f (p = %.4f) | KPSS d=1   %.4f (p = %.4f)\n",
            trm_pruebas$adf_d1$estadistico, trm_pruebas$adf_d1$p,
            trm_pruebas$kpss_d1$estadistico, trm_pruebas$kpss_d1$p))
cat(sprintf("%-16s %9s %9s %9s\n", "modelo", "AICc", "BIC", "LB(20) p"))
for (m in trm_rejilla) if (isTRUE(m$convergio))
  cat(sprintf("%-16s %9.2f %9.2f %9.4f%s%s\n", m$etiqueta, m$aicc, m$bic, m$ljung_box_p,
              if (paste0(m$p, m$d, m$q) == trm_caso$mejor_aicc) "  <- min AICc" else "",
              if (paste0(m$p, m$d, m$q) == trm_caso$mejor_bic)  "  <- min BIC"  else ""))
cat(sprintf("auto.arima (exhaustiva, %d modelos) -> %s\n",
            trm_caso$auto_arima$n_modelos, trm_caso$auto_arima$resultado))
cat(sprintf("Caminata aleatoria ARIMA(0,1,0): Ljung-Box(20) p = %.4f | Shapiro p = %.4f\n",
            trm_caso$caminata$ljung_box_20_p, trm_caso$caminata$shapiro_p))
cat(sprintf("Deriva: %.4f (e.e. %.4f, t = %.2f) -> %s\n",
            trm_caso$deriva$valor, trm_caso$deriva$ee, trm_caso$deriva$t,
            if (abs(trm_caso$deriva$t) < 2) "NO significativa" else "significativa"))
cat(sprintf("Ljung-Box(12) sobre los residuales AL CUADRADO: p = %.4f\n",
            trm_caso$volatilidad$lb12_cuadrados_p))
cat(sprintf("MÍNIMO DE AICc DEGENERADO: %s gana %.2f de AICc al ARIMA(0,1,0)\n",
            trm_caso$minimo_degenerado$etiqueta,
            -trm_caso$minimo_degenerado$ventaja_aicc))
cat(sprintf("   |raíces AR| = %s | |raíces MA| = %s -> descartado\n",
            paste(trm_caso$minimo_degenerado$raices_ar, collapse = ", "),
            paste(trm_caso$minimo_degenerado$raices_ma, collapse = ", ")))
cat("\nModelos degenerados en la rejilla del Nilo (raíz sobre el círculo unitario):\n")
deg_nilo <- Filter(function(m) isTRUE(m$convergio) && isTRUE(m$raices$degenerado), rejilla)
if (length(deg_nilo) == 0) cat("   ninguno\n") else
  for (m in deg_nilo) cat(sprintf("   %-16s AICc %9.2f | min|raiz AR| = %s | min|raiz MA| = %s\n",
                                  m$etiqueta, m$aicc, m$raices$min_ar, m$raices$min_ma))

# ============================================================================
# 10. Puente al capítulo 5 — ARIMA no estacional sobre log(AirPassengers)
# ============================================================================

salida_ap <- capture.output(
  ap_auto <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE,
                        approximation = FALSE, trace = TRUE))
res_ap <- as.numeric(residuals(ap_auto))
ap_acf <- round(as.numeric(acf(res_ap, lag.max = 26, plot = FALSE)$acf)[-1], 4)

ap_sarima <- Arima(lap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
res_sar <- as.numeric(residuals(ap_sarima))

puente <- list(
  serie = "log(AirPassengers)",
  n = length(lap),
  no_estacional = list(
    resultado = as.character(ap_auto),
    orden = as.integer(arimaorder(ap_auto)[1:3]),
    aicc = round(as.numeric(ap_auto$aicc), 3),
    acf_residuales = ap_acf,
    banda = round(1.96 / sqrt(length(res_ap)), 4),
    acf_12 = ap_acf[12], acf_24 = ap_acf[24],
    ljung_box_24 = list(
      Q = round(as.numeric(Box.test(res_ap, lag = 24, type = "Ljung-Box",
                                    fitdf = sum(arimaorder(ap_auto)[c(1, 3)]))$statistic), 3),
      p = round(as.numeric(Box.test(res_ap, lag = 24, type = "Ljung-Box",
                                    fitdf = sum(arimaorder(ap_auto)[c(1, 3)]))$p.value), 6))
  ),
  # El modelo "airline" del capítulo 5, solo como avance de lo que viene
  estacional = list(
    etiqueta = "ARIMA(0,1,1)(0,1,1)[12]",
    aicc = round(as.numeric(ap_sarima$aicc), 3),
    acf_residuales = round(as.numeric(acf(res_sar, lag.max = 26, plot = FALSE)$acf)[-1], 4),
    ljung_box_24_p = round(as.numeric(Box.test(res_sar, lag = 24, type = "Ljung-Box",
                                               fitdf = 2)$p.value), 4)
  ),
  advertencia_aicc = paste("Los dos modelos tienen la MISMA diferenciación total",
                           "(d + D*m distinta): el no estacional usa d = 1 y el airline",
                           "d = 1, D = 1. Sus AICc se calculan sobre n distinto (143 vs. 131)",
                           "y NO son comparables. La comparación válida es el diagnóstico.")
)

cat("\n=== Puente al capítulo 5: log(AirPassengers) sin estacionalidad ===\n")
cat(sprintf("auto.arima(seasonal = FALSE) -> %s\n", puente$no_estacional$resultado))
cat(sprintf("   ACF residual en el rezago 12 = %.4f | en el 24 = %.4f | banda = %.4f\n",
            puente$no_estacional$acf_12, puente$no_estacional$acf_24,
            puente$no_estacional$banda))
cat(sprintf("   Ljung-Box(24): Q = %.3f, p = %.6f -> el diagnóstico RECHAZA\n",
            puente$no_estacional$ljung_box_24$Q, puente$no_estacional$ljung_box_24$p))
cat(sprintf("   Modelo airline (cap. 5): Ljung-Box(24) p = %.4f, ACF(12) = %.4f\n",
            puente$estacional$ljung_box_24_p, puente$estacional$acf_residuales[12]))

# ============================================================================
# 11. Verificación cruzada contra la rejilla de la Fase 0
# ============================================================================

ruta_fase0 <- file.path(dir_salidas, "cap4_rejilla_arima.json")
comparacion_fase0 <- NULL
if (file.exists(ruta_fase0)) {
  f0 <- fromJSON(ruta_fase0, simplifyVector = FALSE)
  difs <- c()
  for (clave in names(f0$modelos)) {
    if (is.null(rejilla[[clave]]) || !isTRUE(rejilla[[clave]]$convergio)) next
    if (is.null(f0$modelos[[clave]]$aicc)) next
    difs <- c(difs, abs(f0$modelos[[clave]]$aicc - rejilla[[clave]]$aicc))
  }
  comparacion_fase0 <- list(
    modelos_comparados = length(difs),
    diferencia_maxima_aicc = round(max(difs), 4),
    mejor_por_d_fase0 = f0$mejor_aicc_por_d,
    mejor_por_d_ahora = sapply(mejor_por_d, `[[`, "mejor_aicc")
  )
  cat("\n=== Verificación contra la rejilla de la Fase 0 ===\n")
  cat(sprintf("   %d modelos comparados | diferencia máxima de AICc = %.4f\n",
              comparacion_fase0$modelos_comparados, comparacion_fase0$diferencia_maxima_aicc))
  cat(sprintf("   mejor por d — Fase 0: %s | ahora: %s\n",
              paste(unlist(f0$mejor_aicc_por_d), collapse = ", "),
              paste(comparacion_fase0$mejor_por_d_ahora, collapse = ", ")))
}

# ============================================================================
# 12. Escritura de las salidas
# ============================================================================

datos <- list(
  descripcion = paste(
    "Precálculos del Capítulo 4 (modelos ARIMA y metodología Box-Jenkins).",
    "Ajustes con stats::arima y forecast::Arima por máxima verosimilitud.",
    "AICc = AIC + 2k(k+1)/(n-k-1) con k = nº de coeficientes + 1 y n EFECTIVO = n - d.",
    "El AICc solo se compara dentro de un mismo d. Ljung-Box con fitdf = p + q.",
    "Trazas de auto.arima capturadas con trace = TRUE (criterio AICc)."),
  generado = format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z"),
  max_rezago = MAX_REZAGO,
  horizonte = H_PRON,
  nilo = list(
    nombre = series_base$nilo$nombre,
    fuente = series_base$nilo$fuente,
    unidad = series_base$nilo$unidad,
    n = n_nilo,
    inicio = series_base$nilo$inicio,
    identificacion = identificacion,
    pruebas = pruebas,
    varianzas = varianzas,
    rejilla = rejilla,
    mejor_por_d = mejor_por_d,
    diagnostico = diagnostico,
    cambio_nivel = cambio_nivel,
    sobrediferenciacion = sobredif,
    hyndman_khandakar = hk,
    formas_pronostico = formas,
    intervalos = intervalos
  ),
  trm = trm_caso,
  puente_estacional = puente,
  verificacion_fase0 = comparacion_fase0
)

ruta_json <- file.path(dir_salidas, "cap4_arima.json")
write(toJSON(datos, auto_unbox = TRUE, digits = 8, na = "null", pretty = TRUE), ruta_json)

series_cap4 <- list(
  nilo = series_base$nilo,
  trm = series_base$trm,
  airpassengers = series_base$airpassengers
)

ruta_js <- file.path(dir_salidas, "cap4_datos.js")
write(paste0(
  "// Generado por precalculo/genera_cap4.R el ", format(Sys.Date(), "%Y-%m-%d"), "\n",
  "// Precalculos ARIMA y Box-Jenkins (Capitulo 4). No editar a mano.\n",
  "const DATOS_CAP4 = ", toJSON(datos, auto_unbox = TRUE, digits = 8, na = "null"), ";\n",
  "const SERIES_CAP4 = ", toJSON(series_cap4, auto_unbox = TRUE, digits = 8, na = "null"), ";\n"
), ruta_js)

cat("\n=== Salidas ===\n")
cat(sprintf("   %s (%.1f KB)\n", basename(ruta_json), file.size(ruta_json) / 1024))
cat(sprintf("   %s (%.1f KB)\n", basename(ruta_js), file.size(ruta_js) / 1024))
cat("Listo.\n")
