# ============================================================================
# genera_cap5.R — Precálculos del Capítulo 5 (modelos SARIMA)
#
# Genera salidas/cap5_sarima.json y salidas/cap5_datos.js con:
#   - log(AirPassengers) como hilo central: firma estacional en ACF/PACF hasta
#     36 rezagos, mapa mes x año, las cuatro combinaciones (d, D), rejilla
#     SARIMA de 36 modelos, el modelo airline con diagnóstico y pronóstico
#   - USAccDeaths como segundo caso: mismo recorrido, y la trampa del orden
#     (ndiffs = 0 en crudo, 1 tras la diferencia estacional)
#   - TRM mensual como CONTRAEJEMPLO: serie mensual sin estacionalidad
#     (nsdiffs = 0); qué pasa si se le impone un modelo estacional
#   - co2 de Mauna Loa para los ejercicios guiados
#   - Regresores de calendario sobre AirPassengers: longitud del mes y la
#     Semana Santa móvil (algoritmo de Meeus), ajustados con xreg
#   - Regresión armónica (términos de Fourier, K = 1..6) y STL + ARIMA, que es
#     lo que se usa cuando m es grande o hay varias estacionalidades
#   - Comparación con ETS/Holt-Winters y con snaive sobre UNA partición fija
#     (los últimos 24 meses). La evaluación seria —origen móvil, cobertura— es
#     del capítulo 6: aquí solo se necesita un punto de referencia honesto.
#
# Script aparte de genera_datos.R / genera_cap2.R / genera_cap3.R / genera_cap4.R
# por la misma razón de siempre: no volver a descargar la TRM ni a reajustar
# modelos de otros capítulos. Las series se leen de salidas/datos_series.json.
#
# Dependencias: jsonlite, tseries, forecast. NINGUNA nueva (uroot y pmdarima
# NO están instalados y el material no debe suponerlos).
# Uso:  Rscript genera_cap5.R      (desde la carpeta precalculo/)
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

MAX_REZAGO <- 36   # tres ciclos estacionales completos: sin esto no se ve la firma
H_PRON     <- 24   # horizonte de los pronósticos del capítulo
H_PRUEBA   <- 24   # tamaño de la partición de prueba de la comparativa
M          <- 12
set.seed(2026)

series_base <- fromJSON(file.path(dir_salidas, "datos_series.json"),
                        simplifyVector = TRUE)

ap_bruta <- ts(series_base$airpassengers$valores,
               start = series_base$airpassengers$inicio, frequency = 12)
ap       <- log(ap_bruta)
uad      <- ts(series_base$usaccdeaths$valores,
               start = series_base$usaccdeaths$inicio, frequency = 12)
co2s     <- ts(series_base$co2$valores,
               start = series_base$co2$inicio, frequency = 12)
trm      <- ts(series_base$trm$valores,
               start = series_base$trm$inicio, frequency = 12)

cat("Series cargadas: AirPassengers n =", length(ap_bruta),
    "| USAccDeaths n =", length(uad),
    "| co2 n =", length(co2s), "| TRM n =", length(trm), "\n")

# ----------------------------------------------------------------------------
# 1. Ayudantes
# ----------------------------------------------------------------------------

# Correlogramas muestrales, con las mismas definiciones que el JS del capítulo.
correlogramas <- function(x, max_rezago = MAX_REZAGO) {
  n <- length(x)
  mr <- min(max_rezago, n - 2)
  list(
    n     = n,
    banda = round(1.96 / sqrt(n), 4),
    acf   = round(as.numeric(acf(x,  lag.max = mr, plot = FALSE)$acf)[-1], 4),
    pacf  = round(as.numeric(pacf(x, lag.max = mr, plot = FALSE)$acf), 4)
  )
}

# Diferenciación regular y estacional. `diff(x, differences = 0)` LANZA UN ERROR
# en R (no es la identidad): los casos d = 0 / D = 0 van tratados aparte.
dif_rs <- function(x, d = 0, D = 0, m = M) {
  if (D > 0) x <- diff(x, lag = m, differences = D)
  if (d > 0) x <- diff(x, differences = d)
  x
}

ee_de <- function(ajuste) {
  if (length(ajuste$coef) == 0) return(numeric(0))
  sqrt(diag(ajuste$var.coef))
}

coeficientes_de <- function(ajuste) {
  if (length(ajuste$coef) == 0) return(list())
  ee <- ee_de(ajuste)
  lapply(seq_along(ajuste$coef), function(i) list(
    nombre = names(ajuste$coef)[i],
    valor  = round(as.numeric(ajuste$coef[i]), 4),
    ee     = round(as.numeric(ee[i]), 4),
    t      = round(as.numeric(ajuste$coef[i] / ee[i]), 3)
  ))
}

# Nº de coeficientes ARMA estimados (para el fitdf de Ljung-Box). No cuenta la
# constante ni los regresores: solo p + q + P + Q, que es lo que exige la teoría.
n_arma <- function(ajuste) sum(ajuste$arma[1:4])

diagnostico_de <- function(ajuste, rezago = MAX_REZAGO) {
  r <- residuals(ajuste)
  gl <- n_arma(ajuste)
  lb24 <- Box.test(r, lag = 24, type = "Ljung-Box", fitdf = gl)
  lb36 <- Box.test(r, lag = 36, type = "Ljung-Box", fitdf = gl)
  co <- correlogramas(r, rezago)
  list(
    n_residuales = length(r),
    fitdf        = gl,
    lb24_Q       = round(as.numeric(lb24$statistic), 4),
    lb24_p       = round(lb24$p.value, 4),
    lb36_Q       = round(as.numeric(lb36$statistic), 4),
    lb36_p       = round(lb36$p.value, 4),
    shapiro_p    = round(shapiro.test(r)$p.value, 4),
    acf          = co$acf,
    pacf         = co$pacf,
    banda        = co$banda,
    acf12        = round(co$acf[12], 4),
    acf24        = round(co$acf[24], 4),
    sd_resid     = round(sd(r), 6)
  )
}

# Módulo de las raíces del polinomio COMPLETO (regular x estacional). Una raíz
# sobre el círculo unitario es la firma de la sobrediferenciación, y con la
# parte estacional aparece igual de a menudo que sin ella.
modulos_raices <- function(ajuste) {
  maximo <- function(coefs) {
    if (!length(coefs) || all(coefs == 0)) return(NA_real_)
    r <- tryCatch(Mod(1 / polyroot(c(1, coefs))), error = function(e) numeric(0))
    if (!length(r)) NA_real_ else round(max(r), 4)
  }
  list(
    ar_max = maximo(-ajuste$model$phi),
    ma_max = maximo(ajuste$model$theta)
  )
}

# Etiqueta legible del modelo, del tipo "(0,1,1)(0,1,1)[12]".
etiqueta_sarima <- function(p, d, q, P, D, Q, m = M) {
  sprintf("(%d,%d,%d)(%d,%d,%d)[%d]", p, d, q, P, D, Q, m)
}

# Domingo de Pascua (algoritmo de Meeus/Jones/Butcher para el calendario
# gregoriano). Devuelve la fecha; se usa para el regresor de Semana Santa.
domingo_pascua <- function(anio) {
  a <- anio %% 19
  b <- anio %/% 100
  c <- anio %% 100
  d <- b %/% 4
  e <- b %% 4
  f <- (b + 8) %/% 25
  g <- (b - f + 1) %/% 3
  h <- (19 * a + b - d - g + 15) %% 30
  i <- c %/% 4
  k <- c %% 4
  l <- (32 + 2 * e + 2 * i - h - k) %% 7
  m2 <- (a + 11 * h + 22 * l) %/% 451
  mes <- (h + l - 7 * m2 + 114) %/% 31
  dia <- ((h + l - 7 * m2 + 114) %% 31) + 1
  as.Date(sprintf("%04d-%02d-%02d", anio, mes, dia))
}

# Matriz mes x año para el mapa de calor. Devuelve una lista de filas (años).
mapa_mes_anio <- function(x, digitos = 4) {
  ini <- start(x); fin <- end(x)
  anios <- ini[1]:fin[1]
  m <- matrix(NA_real_, nrow = length(anios), ncol = 12)
  tt <- time(x)
  for (i in seq_along(x)) {
    anio <- floor(round(tt[i], 6))
    mes  <- round((tt[i] - anio) * 12) + 1
    m[anio - anios[1] + 1, mes] <- as.numeric(x[i])
  }
  list(
    anios  = anios,
    filas  = lapply(seq_len(nrow(m)), function(i) round(m[i, ], digitos)),
    minimo = round(min(m, na.rm = TRUE), digitos),
    maximo = round(max(m, na.rm = TRUE), digitos)
  )
}

# Fechas "AAAA-MM" a partir de un objeto ts, para las etiquetas de los gráficos.
etiquetas_ts <- function(x) {
  tt <- time(x)
  vapply(seq_along(tt), function(i) {
    anio <- floor(round(tt[i], 6))
    mes  <- round((tt[i] - anio) * 12) + 1
    sprintf("%04d-%02d", anio, mes)
  }, character(1))
}

etiquetas_futuras <- function(x, h) {
  tt <- tail(time(x), 1)
  anio <- floor(round(tt, 6)); mes <- round((tt - anio) * 12) + 1
  vapply(seq_len(h), function(k) {
    mm <- mes + k; aa <- anio + (mm - 1) %/% 12; mm <- ((mm - 1) %% 12) + 1
    sprintf("%04d-%02d", aa, mm)
  }, character(1))
}

# Multiplicación de polinomios, para expandir phi(B)*Phi(B^m) y theta(B)*Theta(B^m).
# Convención: el vector guarda los coeficientes de 1, B, B^2, ... incluido el 1.
mult_poli <- function(a, b) {
  r <- numeric(length(a) + length(b) - 1)
  for (i in seq_along(a)) for (j in seq_along(b)) r[i + j - 1] <- r[i + j - 1] + a[i] * b[j]
  r
}

# Polinomio estacional (1 + c B^m) a partir de su coeficiente.
poli_estacional <- function(coef, m = M) {
  v <- numeric(m + 1); v[1] <- 1; v[m + 1] <- coef; v
}

# Recorta los ceros del final de un vector de coeficientes. Sin esto, ARMAacf
# recibe órdenes inflados (un SMA(1) con m = 12 llegaría como MA(12) con once
# ceros) y protesta o devuelve basura.
recorta_ceros <- function(v) {
  nz <- which(abs(v) > 1e-12)
  if (!length(nz)) numeric(0) else v[seq_len(max(nz))]
}

# ----------------------------------------------------------------------------
# 2. Módulo 1 — La firma de la estacionalidad en la ACF y la PACF
# ----------------------------------------------------------------------------

firma <- list(
  airpassengers_cruda = correlogramas(ap_bruta),
  airpassengers_log   = correlogramas(ap),
  usaccdeaths         = correlogramas(uad),
  co2                 = correlogramas(co2s),
  trm                 = correlogramas(trm),
  trm_diff            = correlogramas(diff(trm))
)

cat("\n=== FIRMA ESTACIONAL: ACF en los rezagos múltiplos de 12 ===\n")
cat(sprintf("%-22s %8s %8s %8s %8s\n", "serie", "r12", "r24", "r36", "banda"))
for (nm in names(firma)) {
  f <- firma[[nm]]
  cat(sprintf("%-22s %8.4f %8.4f %8.4f %8.4f\n", nm, f$acf[12], f$acf[24],
              if (length(f$acf) >= 36) f$acf[36] else NA, f$banda))
}

# ----------------------------------------------------------------------------
# 3. Módulo 3 — Diferenciación estacional: las cuatro combinaciones (d, D)
# ----------------------------------------------------------------------------

combinaciones <- list()
for (d in 0:1) for (D in 0:1) {
  w <- dif_rs(ap, d = d, D = D)
  co <- correlogramas(w)
  clave <- sprintf("d%d_D%d", d, D)
  combinaciones[[clave]] <- list(
    d = d, D = D,
    etiqueta = c("d0_D0" = "log(y_t) sin diferenciar",
                 "d1_D0" = "Diferencia regular",
                 "d0_D1" = "Diferencia estacional",
                 "d1_D1" = "Ambas diferencias")[[clave]],
    n        = length(w),
    varianza = round(var(w), 6),
    media    = round(mean(w), 6),
    valores  = round(as.numeric(w), 5),
    fechas   = etiquetas_ts(w),
    acf      = co$acf, pacf = co$pacf, banda = co$banda,
    acf1     = round(co$acf[1], 4), acf12 = round(co$acf[12], 4)
  )
}

cat("\n=== log(AirPassengers): las cuatro combinaciones (d, D) ===\n")
cat(sprintf("%-26s %5s %12s %9s %9s\n", "combinación", "n", "varianza", "ACF(1)", "ACF(12)"))
for (k in names(combinaciones)) {
  c5 <- combinaciones[[k]]
  cat(sprintf("%-26s %5d %12.6f %9.4f %9.4f\n", c5$etiqueta, c5$n, c5$varianza, c5$acf1, c5$acf12))
}

# ---- Los operadores conmutan; las PRUEBAS no --------------------------------
conmutan <- list(
  max_diferencia_ap  = max(abs(as.numeric(diff(diff(ap, lag = M))) -
                               as.numeric(diff(diff(ap), lag = M)))),
  max_diferencia_uad = max(abs(as.numeric(diff(diff(uad, lag = M))) -
                               as.numeric(diff(diff(uad), lag = M))))
)

orden_pruebas <- list(
  airpassengers = list(
    ndiffs_crudo     = ndiffs(ap),
    ndiffs_tras_D    = ndiffs(diff(ap, lag = M)),
    nsdiffs_seas     = nsdiffs(ap),
    nsdiffs_ocsb     = nsdiffs(ap, test = "ocsb")
  ),
  usaccdeaths = list(
    ndiffs_crudo     = ndiffs(uad),
    ndiffs_tras_D    = ndiffs(diff(uad, lag = M)),
    nsdiffs_seas     = nsdiffs(uad),
    nsdiffs_ocsb     = nsdiffs(uad, test = "ocsb")
  ),
  co2 = list(
    ndiffs_crudo     = ndiffs(co2s),
    ndiffs_tras_D    = ndiffs(diff(co2s, lag = M)),
    nsdiffs_seas     = nsdiffs(co2s),
    nsdiffs_ocsb     = nsdiffs(co2s, test = "ocsb")
  ),
  trm = list(
    ndiffs_crudo     = ndiffs(trm),
    ndiffs_tras_D    = ndiffs(diff(trm, lag = M)),
    nsdiffs_seas     = nsdiffs(trm),
    nsdiffs_ocsb     = nsdiffs(trm, test = "ocsb")
  ),
  conmutan = conmutan
)

cat("\n=== El orden de las diferencias ===\n")
cat(sprintf("Los operadores conmutan: diferencia máxima %.3g (AP) y %.3g (USAccDeaths)\n",
            conmutan$max_diferencia_ap, conmutan$max_diferencia_uad))
cat(sprintf("%-16s %13s %14s %13s %13s\n", "serie", "ndiffs crudo", "ndiffs tras D", "nsdiffs seas", "nsdiffs ocsb"))
for (nm in c("airpassengers", "usaccdeaths", "co2", "trm")) {
  o <- orden_pruebas[[nm]]
  cat(sprintf("%-16s %13d %14d %13d %13d\n", nm, o$ndiffs_crudo, o$ndiffs_tras_D,
              o$nsdiffs_seas, o$nsdiffs_ocsb))
}
cat("   AVISO: nsdiffs() usa test = 'seas' (fuerza estacional) desde forecast 8.x;\n")
cat("   con test = 'ocsb' —el de versiones antiguas— la respuesta puede cambiar.\n")

# ---- Sobrediferenciación estacional: D = 2 ---------------------------------
sobredif_estacional <- lapply(0:2, function(D) {
  w <- dif_rs(ap, d = 1, D = D)
  aj <- tryCatch(Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, D, 1), period = M)),
                 error = function(e) NULL)
  list(
    D        = D,
    n        = length(w),
    varianza = round(var(w), 6),
    theta_est = if (!is.null(aj) && "sma1" %in% names(aj$coef))
      round(as.numeric(aj$coef["sma1"]), 4) else NA,
    ee       = if (!is.null(aj) && "sma1" %in% names(aj$coef))
      round(as.numeric(ee_de(aj)["sma1"]), 4) else NA,
    raiz_ma  = if (!is.null(aj)) modulos_raices(aj)$ma_max else NA,
    aicc     = if (!is.null(aj)) round(aj$aicc, 3) else NA
  )
})

cat("\n=== Sobrediferenciación ESTACIONAL sobre log(AirPassengers) (d = 1 fijo) ===\n")
cat(sprintf("%3s %5s %12s %11s %8s %11s\n", "D", "n", "varianza", "Theta est.", "e.e.", "|raiz MA|"))
for (s in sobredif_estacional)
  cat(sprintf("%3d %5d %12.6f %11.4f %8.4f %11.4f\n", s$D, s$n, s$varianza, s$theta_est, s$ee, s$raiz_ma))
cat("   -> con D = 2, Theta se pega a -1 y la raíz MA cae sobre el círculo unitario:\n")
cat("      la misma firma algebraica de la sobrediferenciación del capítulo 4.\n")

# ----------------------------------------------------------------------------
# 4. Módulo 4 — ACF/PACF teóricas de procesos estacionales (verificación del JS)
# ----------------------------------------------------------------------------

# Procesos canónicos: el JS del capítulo recalcula estas curvas en vivo con los
# deslizadores; esta tabla es la referencia contra la que se verifican.
procesos_teoricos <- list(
  list(id = "sar1_pos",  nombre = "SAR(1) con Phi = 0.7",              phi = numeric(0), Phi = 0.7,  theta = numeric(0), Theta = 0),
  list(id = "sar1_neg",  nombre = "SAR(1) con Phi = -0.7",             phi = numeric(0), Phi = -0.7, theta = numeric(0), Theta = 0),
  list(id = "sma1",      nombre = "SMA(1) con Theta = -0.6",           phi = numeric(0), Phi = 0,    theta = numeric(0), Theta = -0.6),
  list(id = "ar1_sar1",  nombre = "AR(1)xSAR(1): phi=0.6, Phi=0.7",    phi = 0.6,        Phi = 0.7,  theta = numeric(0), Theta = 0),
  list(id = "ma1_sma1",  nombre = "Airline: theta=-0.4018, Theta=-0.5569", phi = numeric(0), Phi = 0, theta = -0.4018,  Theta = -0.5569),
  list(id = "ar1_sma1",  nombre = "AR(1)xSMA(1): phi=0.5, Theta=-0.7", phi = 0.5,        Phi = 0,    theta = numeric(0), Theta = -0.7)
)

teoricas <- lapply(procesos_teoricos, function(p) {
  # Polinomio AR completo: phi(B) * Phi(B^m). ARMAacf espera los coeficientes
  # del lado derecho, o sea el polinomio con el signo cambiado y sin el 1.
  pol_ar <- mult_poli(c(1, -p$phi), poli_estacional(-p$Phi))
  pol_ma <- mult_poli(c(1,  p$theta), poli_estacional(p$Theta))
  ar <- recorta_ceros(-pol_ar[-1]); ma <- recorta_ceros(pol_ma[-1])
  acf_t  <- as.numeric(ARMAacf(ar = ar, ma = ma, lag.max = MAX_REZAGO))[-1]
  pacf_t <- as.numeric(ARMAacf(ar = ar, ma = ma, lag.max = MAX_REZAGO, pacf = TRUE))
  list(id = p$id, nombre = p$nombre,
       phi = p$phi, Phi = p$Phi, theta = p$theta, Theta = p$Theta,
       ar_expandido = round(ar, 6), ma_expandido = round(ma, 6),
       acf = round(acf_t, 4), pacf = round(pacf_t, 4))
})
names(teoricas) <- vapply(procesos_teoricos, function(p) p$id, character(1))

cat("\n=== ACF teóricas de procesos estacionales (referencia para el simulador) ===\n")
cat(sprintf("%-38s %8s %8s %8s %8s\n", "proceso", "r1", "r11", "r12", "r13"))
for (t in teoricas)
  cat(sprintf("%-38s %8.4f %8.4f %8.4f %8.4f\n", t$nombre, t$acf[1], t$acf[11], t$acf[12], t$acf[13]))
cat("   Los rezagos 11 y 13 son los 'satélites' que genera la multiplicación de polinomios.\n")

# ----------------------------------------------------------------------------
# 5. Módulo 6 — Rejilla SARIMA sobre log(AirPassengers), con d = 1 y D = 1
# ----------------------------------------------------------------------------

# TODOS los modelos comparten d = 1 y D = 1: solo así el AICc es comparable
# entre ellos (la lección del capítulo 4, ahora también para D).
rejilla <- list()
for (p in 0:2) for (q in 0:2) for (P in 0:1) for (Q in 0:1) {
  aj <- tryCatch(
    Arima(ap, order = c(p, 1, q), seasonal = list(order = c(P, 1, Q), period = M),
          method = "ML"),
    error = function(e) NULL, warning = function(w) NULL)
  if (is.null(aj)) next
  di <- diagnostico_de(aj, 24)
  ra <- modulos_raices(aj)
  rejilla[[etiqueta_sarima(p, 1, q, P, 1, Q)]] <- list(
    p = p, q = q, P = P, Q = Q,
    n_par   = p + q + P + Q,
    nobs    = aj$nobs,
    loglik  = round(aj$loglik, 4),
    aicc    = round(aj$aicc, 4),
    bic     = round(aj$bic, 4),
    lb_p    = di$lb24_p,
    acf12   = di$acf12,
    sigma2  = round(aj$sigma2, 6),
    raiz_ar = ra$ar_max,
    raiz_ma = ra$ma_max,
    # La ACF de los residuales, para que el explorador del capítulo la dibuje
    # sin volver a ajustar nada en el navegador.
    acf     = di$acf[1:24],
    banda   = di$banda
  )
}

orden_aicc <- order(vapply(rejilla, function(r) r$aicc, numeric(1)))
mejores <- names(rejilla)[orden_aicc][1:5]
mejor_bic <- names(rejilla)[which.min(vapply(rejilla, function(r) r$bic, numeric(1)))]

cat("\n=== log(AirPassengers): rejilla SARIMA(p,1,q)(P,1,Q)[12], ", length(rejilla), " modelos ===\n", sep = "")
cat(sprintf("%-20s %5s %10s %10s %9s %9s %9s\n", "modelo", "k", "AICc", "BIC", "LB(24) p", "r12 res", "|raiz MA|"))
for (nm in mejores) {
  r <- rejilla[[nm]]
  cat(sprintf("%-20s %5d %10.4f %10.4f %9.4f %9.4f %9.4f\n",
              nm, r$n_par, r$aicc, r$bic, r$lb_p, r$acf12, r$raiz_ma))
}
cat(sprintf("Mejor por AICc: %s | mejor por BIC: %s\n", mejores[1], mejor_bic))
cat(sprintf("Todos los modelos comparten d = 1 y D = 1 -> n efectivo = %d en todos.\n",
            rejilla[[1]]$nobs))

# ---- ¿Qué elige auto.arima? -------------------------------------------------
auto_ap <- auto.arima(ap, stepwise = FALSE, approximation = FALSE)
auto_ap_paso <- auto.arima(ap)
cat(sprintf("auto.arima exhaustivo: %s (AICc %.4f)\n", as.character(auto_ap), auto_ap$aicc))
cat(sprintf("auto.arima escalonado: %s (AICc %.4f)\n", as.character(auto_ap_paso), auto_ap_paso$aicc))

# ----------------------------------------------------------------------------
# 6. Módulos 5 y 7 — El modelo airline sobre log(AirPassengers)
# ----------------------------------------------------------------------------

airline <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M))
diag_airline <- diagnostico_de(airline)
raices_airline <- modulos_raices(airline)

# Pesos psi del modelo completo, expandido a un ARIMA no estacional.
# (1-B)(1-B^12) en el AR; (1+theta B)(1+Theta B^12) en el MA.
pol_ar_airline <- mult_poli(c(1, -1), poli_estacional(-1))          # (1-B)(1-B^12)
pol_ma_airline <- mult_poli(c(1, as.numeric(airline$coef["ma1"])),
                            poli_estacional(as.numeric(airline$coef["sma1"])))
psi_airline <- c(1, ARMAtoMA(ar = -pol_ar_airline[-1], ma = pol_ma_airline[-1], lag.max = H_PRON - 1))

pron_log <- forecast(airline, h = H_PRON, level = c(80, 95))
pron <- list(
  fechas  = etiquetas_futuras(ap, H_PRON),
  log     = list(
    media = round(as.numeric(pron_log$mean), 5),
    lo80  = round(as.numeric(pron_log$lower[, 1]), 5),
    hi80  = round(as.numeric(pron_log$upper[, 1]), 5),
    lo95  = round(as.numeric(pron_log$lower[, 2]), 5),
    hi95  = round(as.numeric(pron_log$upper[, 2]), 5)
  ),
  original = list(
    media = round(exp(as.numeric(pron_log$mean)), 2),
    lo80  = round(exp(as.numeric(pron_log$lower[, 1])), 2),
    hi80  = round(exp(as.numeric(pron_log$upper[, 1])), 2),
    lo95  = round(exp(as.numeric(pron_log$lower[, 2])), 2),
    hi95  = round(exp(as.numeric(pron_log$upper[, 2])), 2)
  ),
  psi = round(psi_airline, 6),
  sigma_h = round(sqrt(cumsum(psi_airline^2) * airline$sigma2), 6),
  nota_mediana = paste("exp() del pronóstico en logaritmos devuelve la MEDIANA de la",
                       "distribución en la escala original, no la media.")
)

# Verificación: sigma_h reconstruido desde los psi frente al que usa forecast().
sigma_h_forecast <- (as.numeric(pron_log$upper[, 2]) - as.numeric(pron_log$mean)) / qnorm(0.975)
verif_psi <- max(abs(pron$sigma_h - sigma_h_forecast))

cat("\n=== log(AirPassengers): modelo airline (0,1,1)(0,1,1)[12] ===\n")
cat(sprintf("   theta = %.4f (e.e. %.4f) | Theta = %.4f (e.e. %.4f)\n",
            airline$coef["ma1"], ee_de(airline)["ma1"],
            airline$coef["sma1"], ee_de(airline)["sma1"]))
cat(sprintf("   sigma^2 = %.6f | AICc = %.4f | BIC = %.4f | n efectivo = %d\n",
            airline$sigma2, airline$aicc, airline$bic, airline$nobs))
cat(sprintf("   Ljung-Box(24) p = %.4f | Ljung-Box(36) p = %.4f | Shapiro p = %.4f\n",
            diag_airline$lb24_p, diag_airline$lb36_p, diag_airline$shapiro_p))
cat(sprintf("   ACF residual en 12 = %.4f | en 24 = %.4f | banda = %.4f\n",
            diag_airline$acf12, diag_airline$acf24, diag_airline$banda))
cat(sprintf("   |raiz MA| máximo = %.4f (invertible si < 1)\n", raices_airline$ma_max))
cat(sprintf("   Verificación de los pesos psi contra forecast(): error máximo %.3g\n", verif_psi))

# ---- Comparación con el ARIMA no estacional del capítulo 4 ------------------
no_estacional <- Arima(ap, order = c(0, 1, 1))
comparacion_puente <- list(
  no_estacional = list(
    modelo = "ARIMA(0,1,1)", aicc = round(no_estacional$aicc, 4),
    lb24_p = diagnostico_de(no_estacional, 24)$lb24_p,
    acf12  = diagnostico_de(no_estacional, 24)$acf12
  ),
  airline = list(
    modelo = "SARIMA(0,1,1)(0,1,1)[12]", aicc = round(airline$aicc, 4),
    lb24_p = diag_airline$lb24_p, acf12 = diag_airline$acf12
  ),
  parametros_extra = 1
)

cat("\n=== Puente con el capítulo 4 ===\n")
cat(sprintf("   ARIMA(0,1,1) no estacional: AICc %.2f | LB(24) p = %.2g | r12 = %.4f\n",
            comparacion_puente$no_estacional$aicc, comparacion_puente$no_estacional$lb24_p,
            comparacion_puente$no_estacional$acf12))
cat(sprintf("   SARIMA airline           : AICc %.2f | LB(24) p = %.4f | r12 = %.4f\n",
            comparacion_puente$airline$aicc, comparacion_puente$airline$lb24_p,
            comparacion_puente$airline$acf12))
cat("   Un solo parámetro más y el problema desaparece.\n")

# ----------------------------------------------------------------------------
# 7. Módulo 8 — Segundo caso (USAccDeaths) y contraejemplo (TRM)
# ----------------------------------------------------------------------------

uad_airline <- Arima(uad, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M))
uad_auto <- auto.arima(uad, stepwise = FALSE, approximation = FALSE)
caso_uad <- list(
  nombre = series_base$usaccdeaths$nombre,
  fuente = series_base$usaccdeaths$fuente,
  unidad = series_base$usaccdeaths$unidad,
  n = length(uad), inicio = series_base$usaccdeaths$inicio,
  valores = round(as.numeric(uad), 2), fechas = etiquetas_ts(uad),
  correlogramas = correlogramas(uad),
  diferenciada = correlogramas(dif_rs(uad, d = 1, D = 1)),
  serie_dif = list(valores = round(as.numeric(dif_rs(uad, 1, 1)), 3),
                   fechas = etiquetas_ts(dif_rs(uad, 1, 1))),
  mapa = mapa_mes_anio(uad, 0),
  ndiffs_crudo = ndiffs(uad), ndiffs_tras_D = ndiffs(diff(uad, lag = M)),
  nsdiffs = nsdiffs(uad),
  coeficientes = coeficientes_de(uad_airline),
  aicc = round(uad_airline$aicc, 4), bic = round(uad_airline$bic, 4),
  sigma2 = round(uad_airline$sigma2, 3), nobs = uad_airline$nobs,
  diagnostico = diagnostico_de(uad_airline, 24),
  auto_arima = as.character(uad_auto),
  auto_aicc = round(uad_auto$aicc, 4)
)

cat("\n=== USAccDeaths: segundo caso ===\n")
cat(sprintf("   ndiffs crudo = %d, tras la diferencia estacional = %d, nsdiffs = %d\n",
            caso_uad$ndiffs_crudo, caso_uad$ndiffs_tras_D, caso_uad$nsdiffs))
cat(sprintf("   airline: theta = %.4f | Theta = %.4f | AICc = %.2f | LB(24) p = %.4f\n",
            uad_airline$coef["ma1"], uad_airline$coef["sma1"], uad_airline$aicc,
            caso_uad$diagnostico$lb24_p))
cat(sprintf("   auto.arima exhaustivo: %s (AICc %.2f)\n", caso_uad$auto_arima, caso_uad$auto_aicc))

# ---- TRM: el contraejemplo --------------------------------------------------
trm_dif <- diff(trm)
trm_forzado <- Arima(trm, order = c(0, 1, 0), seasonal = list(order = c(1, 0, 0), period = M))
trm_simple  <- Arima(trm, order = c(0, 1, 0))
trm_lb <- Box.test(trm_dif, lag = 24, type = "Ljung-Box")
# Cuántas ACF estacionales caen fuera de la banda
acf_trm_dif <- correlogramas(trm_dif)
estacionales_fuera <- sum(abs(acf_trm_dif$acf[c(12, 24, 36)]) > acf_trm_dif$banda)

contraejemplo <- list(
  nombre = series_base$trm$nombre, fuente = series_base$trm$fuente,
  unidad = series_base$trm$unidad, n = length(trm),
  valores = round(as.numeric(trm), 2), fechas = etiquetas_ts(trm),
  mapa = mapa_mes_anio(trm, 1),
  correlogramas = acf_trm_dif,
  acf12 = acf_trm_dif$acf[12], acf24 = acf_trm_dif$acf[24], acf36 = acf_trm_dif$acf[36],
  banda = acf_trm_dif$banda,
  estacionales_fuera_de_banda = estacionales_fuera,
  nsdiffs_seas = nsdiffs(trm), nsdiffs_ocsb = nsdiffs(trm, test = "ocsb"),
  lb24_p = round(trm_lb$p.value, 4),
  forzado = list(
    modelo = "SARIMA(0,1,0)(1,0,0)[12]",
    Phi = round(as.numeric(trm_forzado$coef["sar1"]), 4),
    ee  = round(as.numeric(ee_de(trm_forzado)["sar1"]), 4),
    t   = round(as.numeric(trm_forzado$coef["sar1"] / ee_de(trm_forzado)["sar1"]), 3),
    aicc = round(trm_forzado$aicc, 3)
  ),
  simple = list(modelo = "ARIMA(0,1,0)", aicc = round(trm_simple$aicc, 3)),
  auto = as.character(auto.arima(trm, stepwise = FALSE, approximation = FALSE))
)

cat("\n=== TRM: el contraejemplo (serie mensual SIN estacionalidad) ===\n")
cat(sprintf("   nsdiffs = %d (seas) y %d (ocsb) | ACF de la diferencia en 12/24/36: %.4f / %.4f / %.4f (banda %.4f)\n",
            contraejemplo$nsdiffs_seas, contraejemplo$nsdiffs_ocsb,
            contraejemplo$acf12, contraejemplo$acf24, contraejemplo$acf36, contraejemplo$banda))
cat(sprintf("   Si se le impone un SAR(1) estacional: Phi = %.4f (e.e. %.4f, t = %.2f), AICc %.2f frente a %.2f del modelo simple\n",
            contraejemplo$forzado$Phi, contraejemplo$forzado$ee, contraejemplo$forzado$t,
            contraejemplo$forzado$aicc, contraejemplo$simple$aicc))
cat(sprintf("   auto.arima: %s\n", contraejemplo$auto))

# ----------------------------------------------------------------------------
# 8. Módulo 9 — Regresores de calendario sobre AirPassengers
# ----------------------------------------------------------------------------

fechas_ap <- seq(as.Date(sprintf("%d-%02d-01", start(ap_bruta)[1], start(ap_bruta)[2])),
                 by = "month", length.out = length(ap_bruta))
dias_mes <- as.numeric(diff(c(fechas_ap, seq(tail(fechas_ap, 1), by = "month", length.out = 2)[2])))
anios_ap <- unique(as.numeric(format(fechas_ap, "%Y")))
pascuas <- setNames(vapply(anios_ap, function(a) format(domingo_pascua(a), "%Y-%m-%d"),
                           character(1)), anios_ap)

# Regresor de Semana Santa: 1 si el Domingo de Pascua cae en ese mes.
pascua_mes <- as.numeric(vapply(seq_along(fechas_ap), function(i) {
  a <- as.numeric(format(fechas_ap[i], "%Y")); m <- as.numeric(format(fechas_ap[i], "%m"))
  p <- domingo_pascua(a)
  as.numeric(format(p, "%m")) == m
}, logical(1)))

xreg_cal <- cbind(log_dias = log(dias_mes), pascua = pascua_mes)

cal_sin  <- airline
cal_dias <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M),
                  xreg = xreg_cal[, "log_dias", drop = FALSE])
cal_full <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M),
                  xreg = xreg_cal)

calendario <- list(
  dias_mes = dias_mes,
  fechas   = etiquetas_ts(ap),
  pascuas  = as.list(pascuas),
  meses_pascua_marzo = sum(vapply(anios_ap, function(a) as.numeric(format(domingo_pascua(a), "%m")) == 3, logical(1))),
  rango_dias = c(min(dias_mes), max(dias_mes)),
  variacion_pct = round(100 * (max(dias_mes) / min(dias_mes) - 1), 1),
  modelos = list(
    sin_regresores = list(nombre = "airline sin regresores",
                          aicc = round(cal_sin$aicc, 4), bic = round(cal_sin$bic, 4),
                          coeficientes = coeficientes_de(cal_sin)),
    con_dias = list(nombre = "airline + log(días del mes)",
                    aicc = round(cal_dias$aicc, 4), bic = round(cal_dias$bic, 4),
                    coeficientes = coeficientes_de(cal_dias)),
    con_dias_pascua = list(nombre = "airline + log(días) + Semana Santa",
                           aicc = round(cal_full$aicc, 4), bic = round(cal_full$bic, 4),
                           coeficientes = coeficientes_de(cal_full))
  )
)

cat("\n=== Regresores de calendario sobre log(AirPassengers) ===\n")
cat(sprintf("   Longitud del mes: entre %d y %d días (%.1f%% de diferencia)\n",
            calendario$rango_dias[1], calendario$rango_dias[2], calendario$variacion_pct))
cat(sprintf("   Domingo de Pascua en marzo en %d de los %d años de la serie\n",
            calendario$meses_pascua_marzo, length(anios_ap)))
for (mm in calendario$modelos) {
  cat(sprintf("   %-36s AICc = %9.4f | BIC = %9.4f\n", mm$nombre, mm$aicc, mm$bic))
  for (cf in mm$coeficientes)
    if (cf$nombre %in% c("log_dias", "pascua"))
      cat(sprintf("       %-10s = %8.4f (e.e. %.4f, t = %6.2f)\n", cf$nombre, cf$valor, cf$ee, cf$t))
}

# ----------------------------------------------------------------------------
# 9. Módulo 10 — Regresión armónica (Fourier) y STL + ARIMA
# ----------------------------------------------------------------------------

fourier_res <- lapply(1:6, function(K) {
  xr <- fourier(ap, K = K)
  aj <- auto.arima(ap, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  list(
    K = K,
    n_terminos = ncol(xr),
    n_par_total = length(aj$coef),
    nobs = aj$nobs,
    modelo_errores = as.character(aj),
    aicc = round(aj$aicc, 4),
    bic  = round(aj$bic, 4),
    lb24_p = diagnostico_de(aj, 24)$lb24_p,
    acf12  = diagnostico_de(aj, 24)$acf12
  )
})

# La componente estacional que dibuja cada K (para el simulador): la parte
# explicada por los términos de Fourier de un ajuste por mínimos cuadrados.
fourier_curvas <- lapply(1:6, function(K) {
  xr <- fourier(ap, K = K)
  mod <- lm(as.numeric(ap) ~ xr)
  round(as.numeric(xr %*% coef(mod)[-1]), 5)
})

# El argumento de fondo: con m grande, la parte estacional del SARIMA se dispara.
costo_m <- lapply(c(12, 52, 168, 365), function(m) {
  list(m = m,
       observaciones_perdidas = m,           # las que consume la diferencia estacional
       rezago_maximo_sma1 = m,               # hasta dónde llega un solo Theta
       parametros_fourier_K3 = 6)            # 2K, independiente de m
})

stl_ap <- stlm(ap, s.window = "periodic", method = "arima")
# stlm() devuelve una matriz `mstl`, cuya columna estacional se llama
# "Seasonal12" (con el periodo pegado), no "seasonal".
col_estacional <- grep("^Seasonal", colnames(stl_ap$stl), value = TRUE)[1]
stl_res <- list(
  modelo_errores = as.character(stl_ap$model),
  aicc = round(stl_ap$model$aicc, 4),
  columna = col_estacional,
  componente_estacional = round(as.numeric(stl_ap$stl[, col_estacional])[1:12], 5)
)

# AVISO DE COMPARABILIDAD, y es el mismo error del capítulo 4 con otra letra:
# los modelos armónicos usan D = 0 (n efectivo 143) y el airline usa D = 1
# (n efectivo 131). Sus AICc NO se pueden poner en la misma tabla. Entre
# familias solo se compara fuera de muestra. Este campo viaja al JSON para que
# el texto del capítulo no pueda "olvidarlo".
comparabilidad <- list(
  nobs_armonicos = fourier_res[[1]]$nobs,
  nobs_airline   = airline$nobs,
  aicc_airline   = round(airline$aicc, 4),
  advertencia = paste(
    "Los AICc de la regresión armónica y del SARIMA airline NO son comparables:",
    "los armónicos modelan la serie con D = 0 y el airline con D = 1, así que la",
    "verosimilitud se evalúa sobre series distintas (143 frente a 131 observaciones).",
    "Es la misma trampa del AIC entre distintos d del capítulo 4, ahora con D.",
    "Entre familias solo vale la comparación fuera de muestra.")
)

cat("\n=== Regresión armónica sobre log(AirPassengers) ===\n")
cat(sprintf("%3s %10s %12s %6s %-36s %10s %9s\n",
            "K", "términos", "parám. tot.", "n_ef", "errores ARIMA", "AICc", "LB(24) p"))
for (f in fourier_res)
  cat(sprintf("%3d %10d %12d %6d %-36s %10.4f %9.4f\n", f$K, f$n_terminos, f$n_par_total,
              f$nobs, f$modelo_errores, f$aicc, f$lb24_p))
cat(sprintf("   Con K = %d los %d términos equivalen a 11 indicadoras mensuales: estacionalidad\n",
            M %/% 2, fourier_res[[M %/% 2]]$n_terminos))
cat("   determinista saturada. Más allá de K = m/2 no hay nada que añadir.\n")
cat(sprintf("   STL + ARIMA: errores %s, AICc = %.4f\n", stl_res$modelo_errores, stl_res$aicc))
cat(sprintf("!! COMPARABILIDAD: el airline tiene AICc = %.4f con n efectivo %d; los armónicos,\n",
            comparabilidad$aicc_airline, comparabilidad$nobs_airline))
cat(sprintf("   n efectivo %d. NO se comparan por AICc. Solo fuera de muestra (sección siguiente).\n",
            comparabilidad$nobs_armonicos))

# ----------------------------------------------------------------------------
# 10. Módulo 11 — Comparativa sobre UNA partición fija (últimos 24 meses)
# ----------------------------------------------------------------------------

# Cada método se ajusta en la forma en que se usaría de verdad —ETS sobre la
# serie CRUDA, donde su estacionalidad multiplicativa es la natural; los de la
# familia ARIMA sobre el logaritmo— y todas las métricas se calculan en la
# ESCALA ORIGINAL, que es la única en la que son comparables. Ajustar un
# ETS(M,A,M) sobre datos ya logaritmados sería contarle dos veces la
# multiplicatividad.
n_ap <- length(ap)
entrena      <- window(ap,       end = time(ap)[n_ap - H_PRUEBA])
entrena_orig <- window(ap_bruta, end = time(ap)[n_ap - H_PRUEBA])
prueba       <- window(ap,       start = time(ap)[n_ap - H_PRUEBA + 1])
prueba_orig  <- as.numeric(window(ap_bruta, start = time(ap)[n_ap - H_PRUEBA + 1]))

metricas <- function(pred) {
  pred <- as.numeric(pred)
  e <- prueba_orig - pred
  list(rmse = round(sqrt(mean(e^2)), 3),
       mae  = round(mean(abs(e)), 3),
       mape = round(100 * mean(abs(e / prueba_orig)), 3))
}
# exp() del pronóstico en logaritmos devuelve la MEDIANA, no la media. Es lo
# que se compara aquí, y hay que decirlo.
desde_log <- function(pred_log) exp(as.numeric(pred_log))

comp <- list()

m_snaive <- snaive(entrena_orig, h = H_PRUEBA)
comp[["snaive"]] <- c(list(nombre = "Naive estacional", escala = "original", n_par = 0,
                           pronostico = round(as.numeric(m_snaive$mean), 2)),
                      metricas(m_snaive$mean))

m_sarima <- Arima(entrena, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M))
f_sarima <- desde_log(forecast(m_sarima, h = H_PRUEBA)$mean)
comp[["sarima"]] <- c(list(nombre = "SARIMA airline (0,1,1)(0,1,1)[12]", escala = "log",
                           n_par = 2, pronostico = round(f_sarima, 2)),
                      metricas(f_sarima))

m_auto <- auto.arima(entrena, stepwise = FALSE, approximation = FALSE)
f_auto <- desde_log(forecast(m_auto, h = H_PRUEBA)$mean)
comp[["auto_arima"]] <- c(list(nombre = paste("auto.arima sobre el log:", as.character(m_auto)),
                               escala = "log", n_par = length(m_auto$coef),
                               pronostico = round(f_auto, 2)),
                          metricas(f_auto))

m_ets <- ets(entrena_orig)
f_ets <- as.numeric(forecast(m_ets, h = H_PRUEBA)$mean)
comp[["ets"]] <- c(list(nombre = paste("ETS sobre la serie cruda:", m_ets$method),
                        escala = "original", n_par = length(m_ets$par),
                        pronostico = round(f_ets, 2)),
                   metricas(f_ets))

# El MISMO ets(), sobre el logaritmo. Selecciona otro modelo (sin amortiguar la
# tendencia) y el pronóstico a 24 meses cambia por completo: la elección de la
# escala no es cosmética.
m_ets_log <- ets(entrena)
f_ets_log <- desde_log(forecast(m_ets_log, h = H_PRUEBA)$mean)
comp[["ets_log"]] <- c(list(nombre = paste("ETS sobre el logaritmo:", m_ets_log$method),
                            escala = "log", n_par = length(m_ets_log$par),
                            pronostico = round(f_ets_log, 2)),
                       metricas(f_ets_log))

# K elegido DENTRO de su familia (todos los armónicos comparten D = 0, así que
# ahí el AICc sí compara), no contra el SARIMA.
mejor_K <- fourier_res[[which.min(vapply(fourier_res, function(f) f$aicc, numeric(1)))]]$K
xr_ent <- fourier(entrena, K = mejor_K)
xr_fut <- fourier(entrena, K = mejor_K, h = H_PRUEBA)
m_arm <- auto.arima(entrena, xreg = xr_ent, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
f_arm <- desde_log(forecast(m_arm, xreg = xr_fut, h = H_PRUEBA)$mean)
comp[["armonica"]] <- c(list(nombre = sprintf("Regresión armónica K = %d + errores ARIMA", mejor_K),
                             escala = "log", n_par = length(m_arm$coef),
                             pronostico = round(f_arm, 2)),
                        metricas(f_arm))

m_stl <- stlm(entrena, s.window = "periodic", method = "arima")
f_stl <- desde_log(forecast(m_stl, h = H_PRUEBA)$mean)
comp[["stl_arima"]] <- c(list(nombre = "STL + ARIMA sobre el log", escala = "log",
                              n_par = length(m_stl$model$coef),
                              pronostico = round(f_stl, 2)),
                         metricas(f_stl))

# ¿Y si al SARIMA se le dan los regresores de calendario del módulo 9?
xcal_ent <- xreg_cal[seq_len(length(entrena)), , drop = FALSE]
xcal_fut <- xreg_cal[length(entrena) + seq_len(H_PRUEBA), , drop = FALSE]
m_cal <- Arima(entrena, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M),
               xreg = xcal_ent)
f_cal <- desde_log(forecast(m_cal, xreg = xcal_fut, h = H_PRUEBA)$mean)
comp[["sarima_calendario"]] <- c(list(nombre = "SARIMA airline + calendario", escala = "log",
                                      n_par = length(m_cal$coef),
                                      pronostico = round(f_cal, 2)),
                                 metricas(f_cal))

orden_rmse <- names(comp)[order(vapply(comp, function(m) m$rmse, numeric(1)))]

comparativa <- list(
  n_entrenamiento = length(entrena),
  n_prueba = H_PRUEBA,
  corte = tail(etiquetas_ts(entrena), 1),
  fechas_prueba = etiquetas_ts(prueba),
  observado = round(prueba_orig, 2),
  modelos = comp,
  orden_rmse = orden_rmse,
  nota_escala = paste("Cada método se ajusta como se usaría de verdad (ETS sobre la serie",
                      "cruda; la familia ARIMA sobre el logaritmo) y todas las métricas se",
                      "calculan en la escala original. exp() del pronóstico en logaritmos",
                      "devuelve la mediana, no la media."),
  advertencia = paste("Una sola partición y 24 puntos de prueba. Diferencias de RMSE de este",
                      "tamaño no separan modelos con seguridad: el capítulo 6 repite la",
                      "comparación sobre muchos orígenes, y solo ahí se puede concluir.")
)

cat("\n=== Comparativa sobre los últimos 24 meses (UNA partición) ===\n")
cat(sprintf("   Entrena hasta %s (n = %d), prueba %d meses. Métricas en la escala original.\n",
            comparativa$corte, comparativa$n_entrenamiento, H_PRUEBA))
cat(sprintf("%-46s %9s %6s %10s %10s %8s\n", "modelo", "escala", "k", "RMSE", "MAE", "MAPE %"))
for (nm in orden_rmse) {
  m <- comp[[nm]]
  cat(sprintf("%-46s %9s %6d %10.3f %10.3f %8.3f\n", m$nombre, m$escala, m$n_par,
              m$rmse, m$mae, m$mape))
}

# ---- POR QUÉ NO SE PUEDE CONCLUIR DE AHÍ, medido ----------------------------
# La tabla de arriba corona a la regresión armónica. Repitiendo la comparación
# sobre 61 orígenes en vez de uno, el orden SE INVIERTE y gana el SARIMA. El
# capítulo 5 solo cita este resultado como advertencia; el MÉTODO (validación de
# origen móvil) es contenido del capítulo 6 y allí se desarrolla.
H_OM <- 12
origenes <- seq(from = 72, to = n_ap - H_OM)
pronosticadores <- list(
  snaive  = function(e_log, e_orig, h) as.numeric(snaive(e_orig, h = h)$mean),
  sarima  = function(e_log, e_orig, h) desde_log(forecast(
              Arima(e_log, order = c(0, 1, 1),
                    seasonal = list(order = c(0, 1, 1), period = M)), h = h)$mean),
  armonica = function(e_log, e_orig, h) desde_log(forecast(
              auto.arima(e_log, xreg = fourier(e_log, K = 6), seasonal = FALSE),
              xreg = fourier(e_log, K = 6, h = h), h = h)$mean),
  ets_log  = function(e_log, e_orig, h) desde_log(forecast(ets(e_log), h = h)$mean),
  ets_orig = function(e_log, e_orig, h) as.numeric(forecast(ets(e_orig), h = h)$mean),
  stl      = function(e_log, e_orig, h) desde_log(forecast(
              stlm(e_log, s.window = "periodic", method = "arima"), h = h)$mean)
)

errores_om <- lapply(names(pronosticadores), function(nm) numeric(0))
names(errores_om) <- names(pronosticadores)
for (o in origenes) {
  e_log  <- window(ap,       end = time(ap)[o])
  e_orig <- window(ap_bruta, end = time(ap)[o])
  obs    <- as.numeric(window(ap_bruta, start = time(ap)[o + 1], end = time(ap)[o + H_OM]))
  for (nm in names(pronosticadores)) {
    p <- pronosticadores[[nm]](e_log, e_orig, H_OM)
    errores_om[[nm]] <- c(errores_om[[nm]], sqrt(mean((obs - p)^2)))
  }
}

rmse_medio <- vapply(errores_om, mean, numeric(1))
gana_al_sarima <- vapply(names(errores_om), function(nm)
  mean(errores_om[[nm]] < errores_om[["sarima"]]), numeric(1))

origen_movil <- list(
  n_origenes = length(origenes),
  horizonte = H_OM,
  primer_origen = etiquetas_ts(window(ap, end = time(ap)[origenes[1]]))[origenes[1]],
  rmse_medio = as.list(round(rmse_medio, 3)),
  porcentaje_gana_al_sarima = as.list(round(100 * gana_al_sarima, 1)),
  orden = names(sort(rmse_medio)),
  nota = paste("Verificación, no contenido: la sola partición de la tabla anterior",
               "corona a la regresión armónica y este resultado la desmiente. El",
               "método de origen móvil se desarrolla en el capítulo 6.")
)
comparativa$origen_movil <- origen_movil

cat("\n--- Verificación: la misma comparación sobre", length(origenes), "orígenes (h = 12) ---\n")
cat(sprintf("%-12s %12s %26s\n", "modelo", "RMSE medio", "% orígenes que gana al SARIMA"))
for (nm in origen_movil$orden)
  cat(sprintf("%-12s %12.3f %25.1f%%\n", nm, rmse_medio[[nm]], 100 * gana_al_sarima[[nm]]))
cat("   -> el orden de la tabla anterior SE INVIERTE. Una sola partición no decide nada.\n")

# ----------------------------------------------------------------------------
# 11. co2 de Mauna Loa — ejercicios guiados
# ----------------------------------------------------------------------------

co2_auto <- auto.arima(co2s, stepwise = FALSE, approximation = FALSE)
co2_airline <- Arima(co2s, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = M))
co2_datos <- list(
  nombre = series_base$co2$nombre, fuente = series_base$co2$fuente,
  unidad = series_base$co2$unidad, n = length(co2s), inicio = series_base$co2$inicio,
  correlogramas = correlogramas(co2s),
  diferenciada = correlogramas(dif_rs(co2s, 1, 1)),
  mapa = mapa_mes_anio(co2s, 2),
  ndiffs = ndiffs(co2s), ndiffs_tras_D = ndiffs(diff(co2s, lag = M)),
  nsdiffs = nsdiffs(co2s),
  varianzas = list(
    d0_D0 = round(var(co2s), 4), d1_D0 = round(var(diff(co2s)), 4),
    d0_D1 = round(var(diff(co2s, lag = M)), 4), d1_D1 = round(var(dif_rs(co2s, 1, 1)), 4)
  ),
  auto = as.character(co2_auto), auto_aicc = round(co2_auto$aicc, 4),
  auto_coeficientes = coeficientes_de(co2_auto),
  auto_diagnostico = diagnostico_de(co2_auto, 24),
  airline = list(modelo = "SARIMA(0,1,1)(0,1,1)[12]", aicc = round(co2_airline$aicc, 4),
                 bic = round(co2_airline$bic, 4),
                 coeficientes = coeficientes_de(co2_airline),
                 diagnostico = diagnostico_de(co2_airline, 24))
)

cat("\n=== co2 de Mauna Loa (ejercicios) ===\n")
cat(sprintf("   ndiffs = %d (tras D: %d) | nsdiffs = %d\n",
            co2_datos$ndiffs, co2_datos$ndiffs_tras_D, co2_datos$nsdiffs))
cat(sprintf("   auto.arima: %s (AICc %.2f) | airline: AICc %.2f\n",
            co2_datos$auto, co2_datos$auto_aicc, co2_datos$airline$aicc))
cat(sprintf("   Varianzas: cruda %.4f | d=1 %.4f | D=1 %.4f | ambas %.4f\n",
            co2_datos$varianzas$d0_D0, co2_datos$varianzas$d1_D0,
            co2_datos$varianzas$d0_D1, co2_datos$varianzas$d1_D1))

# ----------------------------------------------------------------------------
# 12. Ensamblado del JSON
# ----------------------------------------------------------------------------

datos <- list(
  descripcion = paste("Precálculos del Capítulo 5 (SARIMA):",
                      "log(AirPassengers) como caso central, USAccDeaths como segundo caso,",
                      "TRM como contraejemplo sin estacionalidad, co2 para los ejercicios,",
                      "regresores de calendario, regresión armónica y comparativa sobre",
                      "una partición fija."),
  generado = format(Sys.time(), "%Y-%m-%d %H:%M"),
  max_rezago = MAX_REZAGO,
  horizonte = H_PRON,
  m = M,
  airpassengers = list(
    nombre = series_base$airpassengers$nombre,
    fuente = series_base$airpassengers$fuente,
    unidad = series_base$airpassengers$unidad,
    n = length(ap_bruta),
    inicio = series_base$airpassengers$inicio,
    fechas = etiquetas_ts(ap),
    log = round(as.numeric(ap), 5),
    firma = firma,
    mapa = list(
      cruda  = mapa_mes_anio(ap_bruta, 0),
      log    = mapa_mes_anio(ap, 4),
      d1     = mapa_mes_anio(diff(ap), 4),
      D1     = mapa_mes_anio(diff(ap, lag = M), 4),
      d1D1   = mapa_mes_anio(dif_rs(ap, 1, 1), 4)
    ),
    combinaciones = combinaciones,
    orden_pruebas = orden_pruebas,
    sobrediferenciacion_estacional = sobredif_estacional,
    rejilla = rejilla,
    mejores_aicc = mejores,
    mejor_bic = mejor_bic,
    auto_arima = list(exhaustivo = as.character(auto_ap), aicc = round(auto_ap$aicc, 4),
                      escalonado = as.character(auto_ap_paso)),
    airline = list(
      modelo = "SARIMA(0,1,1)(0,1,1)[12]",
      coeficientes = coeficientes_de(airline),
      sigma2 = round(airline$sigma2, 6), loglik = round(airline$loglik, 4),
      aicc = round(airline$aicc, 4), bic = round(airline$bic, 4), nobs = airline$nobs,
      raices = raices_airline,
      diagnostico = diag_airline,
      residuales = round(as.numeric(residuals(airline)), 5)
    ),
    pronostico = pron,
    verificacion_psi = signif(verif_psi, 3),
    puente_cap4 = comparacion_puente,
    calendario = calendario,
    fourier = list(resultados = fourier_res, curvas = fourier_curvas,
                   mejor_K = mejor_K, costo_m = costo_m, stl = stl_res,
                   comparabilidad = comparabilidad),
    comparativa = comparativa
  ),
  teoricas = teoricas,
  usaccdeaths = caso_uad,
  trm_contraejemplo = contraejemplo,
  co2 = co2_datos
)

ruta_json <- file.path(dir_salidas, "cap5_sarima.json")
write(toJSON(datos, auto_unbox = TRUE, digits = 8, na = "null", pretty = TRUE), ruta_json)

series_cap5 <- list(
  airpassengers = series_base$airpassengers,
  usaccdeaths   = series_base$usaccdeaths,
  co2           = series_base$co2,
  trm           = series_base$trm
)

ruta_js <- file.path(dir_salidas, "cap5_datos.js")
write(paste0(
  "// Generado por precalculo/genera_cap5.R el ", format(Sys.Date(), "%Y-%m-%d"), "\n",
  "// Precalculos SARIMA (Capitulo 5). No editar a mano.\n",
  "const DATOS_CAP5 = ", toJSON(datos, auto_unbox = TRUE, digits = 8, na = "null"), ";\n",
  "const SERIES_CAP5 = ", toJSON(series_cap5, auto_unbox = TRUE, digits = 8, na = "null"), ";\n"
), ruta_js)

cat("\n=== Salidas ===\n")
cat(sprintf("   %s (%.1f KB)\n", basename(ruta_json), file.size(ruta_json) / 1024))
cat(sprintf("   %s (%.1f KB)\n", basename(ruta_js), file.size(ruta_js) / 1024))
cat("Listo.\n")
