# ============================================================================
# genera_cap3.R — Precálculos del Capítulo 3 (modelos AR, MA y ARMA)
#
# Genera salidas/cap3_arma.json y salidas/cap3_datos.js con:
#   - ACF y PACF TEÓRICAS (stats::ARMAacf) de 8 procesos canónicos, más sus
#     pesos psi (representación MA(inf)) y pi (representación AR(inf))
#   - Manchas solares anuales 1770-1869: correlogramas, AR(2) estimado por
#     Yule-Walker, CSS y máxima verosimilitud, raíces del polinomio
#     característico y pseudo-periodo, rejilla de modelos con AIC/AICc/BIC,
#     y residuales + Ljung-Box acumulado de cada candidato
#   - Log-retornos mensuales de la TRM: correlogramas, MA(1) y Ljung-Box
#     (el caso "casi ruido blanco" que sirve de contraste honesto)
#   - Verificación cruzada de la fórmula de los pesos psi que implementa el
#     JavaScript del capítulo contra ARMAacf
#
# Script aparte de genera_datos.R y genera_cap2.R por la misma razón que aquél:
# no volver a descargar la TRM ni a reajustar los modelos de otros capítulos.
# La TRM se lee de salidas/datos_series.json.
#
# Dependencias: jsonlite, tseries, forecast.
# Uso:  Rscript genera_cap3.R      (desde la carpeta precalculo/)
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

MAX_REZAGO   <- 20   # rezagos de los correlogramas del capítulo
MAX_REZAGO_T <- 16   # rezagos de las ACF/PACF teóricas de los procesos canónicos
N_PSI        <- 12   # pesos psi/pi que se muestran en el módulo de dualidad

# ----------------------------------------------------------------------------
# 1. Ayudantes
# ----------------------------------------------------------------------------

# ACF y PACF muestrales, con las mismas definiciones que usa el capítulo en JS:
# stats::acf divide por n y stats::pacf resuelve Durbin-Levinson sobre la ACF.
correlogramas <- function(x, max_rezago = MAX_REZAGO) {
  n <- length(x)
  list(
    n     = n,
    banda = round(1.96 / sqrt(n), 4),
    acf   = round(as.numeric(acf(x,  lag.max = max_rezago, plot = FALSE)$acf)[-1], 4),
    pacf  = round(as.numeric(pacf(x, lag.max = max_rezago, plot = FALSE)$acf), 4)
  )
}

# AICc = AIC + 2k(k+1)/(n-k-1), con k = nº de parámetros estimados + 1 (sigma^2).
aicc_de <- function(ajuste, n) {
  k <- length(ajuste$coef) + 1
  as.numeric(ajuste$aic + 2 * k * (k + 1) / (n - k - 1))
}

# Pesos psi de la representación MA(infinito): y_t = sum psi_j eps_{t-j}.
# Recursión psi_j = theta_j + sum_{i=1..p} phi_i psi_{j-i}, con psi_0 = 1.
# ESTA es la fórmula que implementa el JavaScript del capítulo; el bloque de
# verificación de más abajo la contrasta contra ARMAacf.
pesos_psi <- function(ar = numeric(0), ma = numeric(0), n = N_PSI) {
  psi <- numeric(n + 1)
  psi[1] <- 1
  for (j in 1:n) {
    v <- if (j <= length(ma)) ma[j] else 0
    for (i in seq_along(ar)) if (j - i >= 0) v <- v + ar[i] * psi[j - i + 1]
    psi[j + 1] <- v
  }
  psi
}

# Pesos pi de la representación AR(infinito): eps_t = sum pi_j y_{t-j}.
# Es la misma recursión intercambiando los papeles de phi y theta y cambiando
# el signo: por eso un MA no invertible (|theta| > 1) hace que los pi exploten.
pesos_pi <- function(ar = numeric(0), ma = numeric(0), n = N_PSI) {
  pp <- numeric(n + 1)
  pp[1] <- 1
  for (j in 1:n) {
    v <- if (j <= length(ar)) -ar[j] else 0
    for (i in seq_along(ma)) if (j - i >= 0) v <- v - ma[i] * pp[j - i + 1]
    pp[j + 1] <- v
  }
  pp
}

# Raíces del polinomio característico phi(B) = 1 - phi_1 B - ... - phi_p B^p.
# Estacionariedad <=> todas las raíces caen FUERA del círculo unitario (|B| > 1).
raices_de <- function(phi) {
  r <- polyroot(c(1, -phi))
  complejas <- any(abs(Im(r)) > 1e-8)
  out <- list(
    raices    = lapply(seq_along(r), function(i)
                  list(re = round(Re(r[i]), 4), im = round(Im(r[i]), 4),
                       modulo = round(Mod(r[i]), 4))),
    modulo_min = round(min(Mod(r)), 4),
    complejas  = complejas,
    estacionario = all(Mod(r) > 1)
  )
  if (complejas) {
    out$periodo <- round(2 * pi / Arg(r[which.max(Im(r))]), 4)
    # Comprobación por la fórmula cerrada del AR(2): 2*pi / acos(phi1/(2*sqrt(-phi2)))
    if (length(phi) == 2 && phi[2] < 0)
      out$periodo_formula_ar2 <- round(2 * pi / acos(phi[1] / (2 * sqrt(-phi[2]))), 4)
  }
  out
}

# Ljung-Box acumulado rezago a rezago sobre los residuales de un ajuste.
ljung_box_acumulado <- function(residuales, gl_modelo, hasta = MAX_REZAGO) {
  filas <- list()
  for (h in 1:hasta) {
    if (h <= gl_modelo) next          # sin grados de libertad, la prueba no existe
    b <- Box.test(residuales, lag = h, type = "Ljung-Box", fitdf = gl_modelo)
    filas[[length(filas) + 1]] <- list(
      rezago = h,
      Q      = round(as.numeric(b$statistic), 4),
      gl     = as.integer(b$parameter),
      p      = round(as.numeric(b$p.value), 4)
    )
  }
  filas
}

# ----------------------------------------------------------------------------
# 2. Procesos canónicos: ACF y PACF TEÓRICAS
#
# Son las figuras de identificación del capítulo. ARMAacf las calcula de forma
# exacta (Yule-Walker para el AR, convolución de thetas para el MA), no por
# simulación: por eso el capítulo puede afirmar que la PACF de un AR(p) es
# EXACTAMENTE cero a partir del rezago p+1, y no "aproximadamente cero".
# ----------------------------------------------------------------------------

catalogo <- list(
  list(clave = "ar1_pos",  nombre = "AR(1), phi = 0.8",             ar = 0.8,          ma = numeric(0)),
  list(clave = "ar1_neg",  nombre = "AR(1), phi = -0.7",            ar = -0.7,         ma = numeric(0)),
  list(clave = "ar2_real", nombre = "AR(2), phi = (0.5, 0.3)",      ar = c(0.5, 0.3),  ma = numeric(0)),
  list(clave = "ar2_comp", nombre = "AR(2), phi = (1.4, -0.75)",    ar = c(1.4, -0.75), ma = numeric(0)),
  list(clave = "ma1_pos",  nombre = "MA(1), theta = 0.8",           ar = numeric(0),   ma = 0.8),
  list(clave = "ma1_neg",  nombre = "MA(1), theta = -0.8",          ar = numeric(0),   ma = -0.8),
  list(clave = "ma2",      nombre = "MA(2), theta = (0.6, 0.4)",    ar = numeric(0),   ma = c(0.6, 0.4)),
  list(clave = "arma11",   nombre = "ARMA(1,1), phi = 0.7, theta = 0.5", ar = 0.7,     ma = 0.5)
)

procesos <- lapply(catalogo, function(p) {
  a <- ARMAacf(ar = p$ar, ma = p$ma, lag.max = MAX_REZAGO_T)[-1]
  pa <- ARMAacf(ar = p$ar, ma = p$ma, lag.max = MAX_REZAGO_T, pacf = TRUE)
  psi <- pesos_psi(p$ar, p$ma, N_PSI)
  pii <- pesos_pi(p$ar, p$ma, N_PSI)
  list(
    clave        = p$clave,
    nombre       = p$nombre,
    ar           = if (length(p$ar)) p$ar else NULL,
    ma           = if (length(p$ma)) p$ma else NULL,
    p            = length(p$ar),
    q            = length(p$ma),
    acf_teorica  = round(as.numeric(a), 4),
    pacf_teorica = round(as.numeric(pa), 4),
    psi          = round(psi, 4),
    pi           = round(pii, 4),
    # varianza del proceso con sigma^2 = 1: gamma_0 = sum psi_j^2 (serie infinita;
    # se usan 2000 términos para que el truncamiento no se note al redondear)
    var_proceso  = round(sum(pesos_psi(p$ar, p$ma, 2000)^2), 4),
    raices       = if (length(p$ar)) raices_de(p$ar) else NULL
  )
})
names(procesos) <- sapply(catalogo, `[[`, "clave")

# Realizaciones simuladas (semilla fija) de tres de ellos, para el panel que
# enfrenta la ACF teórica con la ACF muestral de UNA realización finita.
set.seed(3)
realizaciones <- list()
for (cl in c("ar1_pos", "ma1_pos", "arma11")) {
  p <- catalogo[[which(sapply(catalogo, `[[`, "clave") == cl)]]
  x <- arima.sim(n = 200, model = list(ar = p$ar, ma = p$ma), sd = 1)
  realizaciones[[cl]] <- c(
    list(valores = round(as.numeric(x), 4)),
    correlogramas(x, MAX_REZAGO_T)
  )
}

# ----------------------------------------------------------------------------
# 3. Manchas solares anuales, 1770-1869
#
# La ventana centenaria que estudió Yule (1927) al inventar el modelo
# autorregresivo. Es el caso real del capítulo: un AR(2) con raíces complejas
# cuyo pseudo-periodo tiene que salir cerca de los 11 años del ciclo solar.
# ----------------------------------------------------------------------------

manchas <- window(sunspot.year, start = 1770, end = 1869)
anios   <- as.integer(time(manchas))
n_m     <- length(manchas)

cg_manchas <- correlogramas(manchas, MAX_REZAGO)

# --- 3a. El mismo AR(2) por tres métodos de estimación -----------------------
# Yule-Walker resuelve el sistema de momentos con la ACF muestral; CSS minimiza
# la suma de cuadrados condicional; ML maximiza la verosimilitud gaussiana
# exacta. arima() usa por defecto "CSS-ML": CSS para arrancar, ML para terminar.
yw  <- ar(manchas, order.max = 2, aic = FALSE, method = "yule-walker")
bur <- ar(manchas, order.max = 2, aic = FALSE, method = "burg")
css <- arima(manchas, order = c(2, 0, 0), method = "CSS")
ml  <- arima(manchas, order = c(2, 0, 0), method = "ML")

metodos <- list(
  yule_walker = list(
    metodo = "Yule-Walker (ar, method = \"yule-walker\")",
    phi1 = round(yw$ar[1], 4), phi2 = round(yw$ar[2], 4),
    media = round(yw$x.mean, 4), sigma2 = round(yw$var.pred, 4),
    se1 = round(sqrt(yw$asy.var.coef[1, 1]), 4),
    se2 = round(sqrt(yw$asy.var.coef[2, 2]), 4)
  ),
  burg = list(
    metodo = "Burg (ar, method = \"burg\")",
    phi1 = round(bur$ar[1], 4), phi2 = round(bur$ar[2], 4),
    media = round(bur$x.mean, 4), sigma2 = round(bur$var.pred, 4)
  ),
  css = list(
    metodo = "Suma de cuadrados condicional (arima, method = \"CSS\")",
    phi1 = round(coef(css)[["ar1"]], 4), phi2 = round(coef(css)[["ar2"]], 4),
    media = round(coef(css)[["intercept"]], 4), sigma2 = round(css$sigma2, 4),
    se1 = round(sqrt(css$var.coef[1, 1]), 4), se2 = round(sqrt(css$var.coef[2, 2]), 4)
  ),
  ml = list(
    metodo = "Máxima verosimilitud (arima, method = \"ML\")",
    phi1 = round(coef(ml)[["ar1"]], 4), phi2 = round(coef(ml)[["ar2"]], 4),
    media = round(coef(ml)[["intercept"]], 4), sigma2 = round(ml$sigma2, 4),
    se1 = round(sqrt(ml$var.coef[1, 1]), 4), se2 = round(sqrt(ml$var.coef[2, 2]), 4),
    loglik = round(as.numeric(ml$loglik), 4),
    aic = round(as.numeric(ml$aic), 4), aicc = round(aicc_de(ml, n_m), 4),
    bic = round(as.numeric(BIC(ml)), 4)
  )
)

# Distancia entre métodos, en unidades de error estándar: la cifra que decide si
# la discrepancia es una anécdota numérica o algo que cambia las conclusiones.
dist_yw_ml <- list(
  dif_phi1 = round(yw$ar[1] - coef(ml)[["ar1"]], 4),
  dif_phi2 = round(yw$ar[2] - coef(ml)[["ar2"]], 4),
  dif_phi1_en_se = round((yw$ar[1] - coef(ml)[["ar1"]]) / sqrt(ml$var.coef[1, 1]), 3),
  dif_phi2_en_se = round((yw$ar[2] - coef(ml)[["ar2"]]) / sqrt(ml$var.coef[2, 2]), 3),
  periodo_yw = round(raices_de(as.numeric(yw$ar))$periodo, 3),
  periodo_ml = round(raices_de(as.numeric(coef(ml)[1:2]))$periodo, 3)
)

raices_ml <- raices_de(as.numeric(coef(ml)[1:2]))

# --- 3b. Rejilla de modelos candidatos ---------------------------------------
# Todos con d = 0, así que aquí SÍ es lícito comparar AIC entre ellos (la
# advertencia del cap. 4 es sobre comparar entre distintos d).
rejilla_def <- list(
  c(1, 0), c(2, 0), c(3, 0), c(4, 0),
  c(0, 1), c(0, 2), c(0, 3),
  c(1, 1), c(2, 1), c(1, 2), c(2, 2)
)

rejilla <- lapply(rejilla_def, function(pq) {
  aj <- tryCatch(arima(manchas, order = c(pq[1], 0, pq[2]), method = "ML"),
                 error = function(e) NULL)
  if (is.null(aj)) return(NULL)
  gl <- pq[1] + pq[2]
  lb <- Box.test(residuals(aj), lag = 12, type = "Ljung-Box", fitdf = gl)
  list(
    p = pq[1], q = pq[2],
    etiqueta = sprintf("ARMA(%d,%d)", pq[1], pq[2]),
    n_coef = length(aj$coef),
    loglik = round(as.numeric(aj$loglik), 3),
    aic    = round(as.numeric(aj$aic), 6),
    aicc   = round(aicc_de(aj, n_m), 6),
    bic    = round(as.numeric(BIC(aj)), 6),
    sigma2 = round(aj$sigma2, 3),
    lb12_Q = round(as.numeric(lb$statistic), 3),
    lb12_p = round(as.numeric(lb$p.value), 4)
  )
})
rejilla <- Filter(Negate(is.null), rejilla)

# --- 3c. Diagnóstico de residuales de cuatro candidatos ----------------------
# Alimentan el simulador de diagnóstico: uno claramente insuficiente (AR(1)),
# el bueno (AR(2)), uno con un parámetro de más (AR(3)) y uno mixto (ARMA(2,1)).
diagnosticos <- list()
for (esp in list(list(p = 1, q = 0), list(p = 2, q = 0), list(p = 3, q = 0), list(p = 2, q = 1))) {
  aj <- arima(manchas, order = c(esp$p, 0, esp$q), method = "ML")
  r  <- as.numeric(residuals(aj))
  gl <- esp$p + esp$q
  cgr <- correlogramas(r, MAX_REZAGO)
  clave <- sprintf("arma%d%d", esp$p, esp$q)
  diagnosticos[[clave]] <- list(
    etiqueta   = sprintf("ARMA(%d,%d)", esp$p, esp$q),
    p = esp$p, q = esp$q,
    coef       = round(coef(aj), 4),
    se         = round(sqrt(diag(aj$var.coef)), 4),
    aicc       = round(aicc_de(aj, n_m), 6),
    bic        = round(as.numeric(BIC(aj)), 6),
    sigma2     = round(aj$sigma2, 3),
    residuales = round(r, 4),
    ajustados  = round(as.numeric(manchas - r), 4),
    acf_resid  = cgr$acf,
    banda      = cgr$banda,
    ljung_box  = ljung_box_acumulado(r, gl),
    lb12_p     = round(as.numeric(Box.test(r, lag = 12, type = "Ljung-Box", fitdf = gl)$p.value), 4),
    shapiro_p  = round(as.numeric(shapiro.test(r)$p.value), 4),
    raices     = if (esp$p >= 1) raices_de(as.numeric(coef(aj)[seq_len(esp$p)])) else NULL
  )
}

# --- 3d. La resolución: raíz cuadrada antes de modelar -----------------------
# Los números de manchas solares son conteos y su varianza crece con el nivel.
# Sobre la serie CRUDA, la identificación dice AR(2) pero el diagnóstico lo
# rechaza y el AICc prefiere un ARMA(2,1); sobre la RAÍZ CUADRADA, el AR(2) es a
# la vez el mejor por AICc y por BIC, pasa Ljung-Box y su pseudo-periodo se
# acerca más al ciclo solar de 11 años. La conclusión del capítulo es que el
# término MA extra estaba parcheando un problema de varianza, no de dinámica.

# Elasticidad amplitud-nivel: log(sd) contra log(media) por bloques. b = 0 no
# necesita transformación, b = 0.5 pide raíz cuadrada, b = 1 pide logaritmo.
# Se calcula con tres tamaños de bloque porque la conclusión NO debe depender
# de una partición arbitraria.
elasticidad <- function(x, g) {
  niv <- tapply(as.numeric(x), g, mean)
  amp <- tapply(as.numeric(x), g, sd)
  ok  <- niv > 0 & amp > 0
  aj  <- lm(log(amp[ok]) ~ log(niv[ok]))
  list(b = round(as.numeric(coef(aj)[2]), 4),
       ic = round(as.numeric(confint(aj)[2, ]), 4),
       r2 = round(summary(aj)$r.squared, 4),
       bloques = as.integer(sum(ok)))
}
elasticidades <- list(
  bloques_10 = c(list(tamano = 10L), elasticidad(manchas, rep(1:10, each = 10))),
  bloques_5  = c(list(tamano = 5L),  elasticidad(manchas, rep(1:20, each = 5))),
  bloques_11 = c(list(tamano = 11L), elasticidad(manchas,
                    cut(1:n_m, breaks = seq(0, n_m, by = 11.1), labels = FALSE)))
)

# Guerrero exige datos estrictamente positivos y la serie tiene un cero (1810),
# así que se desplaza una unidad. Sin el desplazamiento R avisa y el resultado
# cambia (0.3333 en vez de 0.3062).
lambda_manchas <- round(as.numeric(BoxCox.lambda(manchas + 1, method = "guerrero")), 4)
manchas_sqrt   <- sqrt(manchas)
ml_sqrt        <- arima(manchas_sqrt, order = c(2, 0, 0), method = "ML")
raices_sqrt    <- raices_de(as.numeric(coef(ml_sqrt)[1:2]))
cg_sqrt        <- correlogramas(manchas_sqrt, MAX_REZAGO)

# Misma rejilla sobre la serie transformada: aquí el AR(2) sí gana.
rejilla_sqrt <- lapply(rejilla_def, function(pq) {
  aj <- tryCatch(arima(manchas_sqrt, order = c(pq[1], 0, pq[2]), method = "ML"),
                 error = function(e) NULL)
  if (is.null(aj)) return(NULL)
  gl <- pq[1] + pq[2]
  list(p = pq[1], q = pq[2],
       etiqueta = sprintf("ARMA(%d,%d)", pq[1], pq[2]),
       aicc = round(aicc_de(aj, n_m), 6),
       bic  = round(as.numeric(BIC(aj)), 6),
       lb12_p = round(as.numeric(Box.test(residuals(aj), lag = 12,
                                          type = "Ljung-Box", fitdf = gl)$p.value), 4))
})
rejilla_sqrt <- Filter(Negate(is.null), rejilla_sqrt)

# Box-Cox con el lambda de Guerrero, para comprobar que la conclusión no depende
# de haber elegido exactamente 0.5.
ml_bc <- arima(BoxCox(manchas, lambda_manchas), order = c(2, 0, 0), method = "ML")

transformacion <- list(
  # El logaritmo NO es una opción: hay un año con cero manchas en la ventana.
  minimo = as.numeric(min(manchas)),
  n_ceros = as.integer(sum(manchas == 0)),
  n_ceros_serie_completa = as.integer(sum(sunspot.year == 0)),
  elasticidades = elasticidades,
  lambda_guerrero = lambda_manchas,
  sqrt = list(
    phi1 = round(coef(ml_sqrt)[["ar1"]], 4),
    phi2 = round(coef(ml_sqrt)[["ar2"]], 4),
    se1  = round(sqrt(ml_sqrt$var.coef[1, 1]), 4),
    se2  = round(sqrt(ml_sqrt$var.coef[2, 2]), 4),
    media = round(coef(ml_sqrt)[["intercept"]], 4),
    sigma2 = round(ml_sqrt$sigma2, 4),
    periodo = round(raices_sqrt$periodo, 4),
    modulo  = raices_sqrt$modulo_min,
    aicc = round(aicc_de(ml_sqrt, n_m), 6),
    bic  = round(as.numeric(BIC(ml_sqrt)), 6),
    lb12_p = round(as.numeric(Box.test(residuals(ml_sqrt), lag = 12,
                                       type = "Ljung-Box", fitdf = 2)$p.value), 4),
    shapiro_p = round(as.numeric(shapiro.test(residuals(ml_sqrt))$p.value), 4),
    valores = round(as.numeric(manchas_sqrt), 4),
    acf = cg_sqrt$acf, pacf = cg_sqrt$pacf, banda = cg_sqrt$banda,
    residuales = round(as.numeric(residuals(ml_sqrt)), 4),
    acf_resid  = correlogramas(residuals(ml_sqrt), MAX_REZAGO)$acf,
    ljung_box  = ljung_box_acumulado(residuals(ml_sqrt), 2),
    rejilla    = rejilla_sqrt
  ),
  box_cox_guerrero = list(
    lambda = lambda_manchas,
    phi1 = round(coef(ml_bc)[["ar1"]], 4),
    phi2 = round(coef(ml_bc)[["ar2"]], 4),
    periodo = round(raices_de(as.numeric(coef(ml_bc)[1:2]))$periodo, 4),
    lb12_p = round(as.numeric(Box.test(residuals(ml_bc), lag = 12,
                                       type = "Ljung-Box", fitdf = 2)$p.value), 4)
  ),
  crudo = list(
    shapiro_p = round(as.numeric(shapiro.test(residuals(ml))$p.value), 4),
    asimetria = round(mean((residuals(ml) - mean(residuals(ml)))^3) /
                        sd(residuals(ml))^3, 4)
  ),
  asimetria_sqrt = round(mean((residuals(ml_sqrt) - mean(residuals(ml_sqrt)))^3) /
                           sd(residuals(ml_sqrt))^3, 4),
  ciclo_solar_documentado = 11.0
)

# ----------------------------------------------------------------------------
# 4. Log-retornos mensuales de la TRM: el contraste "casi ruido blanco"
# ----------------------------------------------------------------------------

sd_json <- fromJSON(file.path(dir_salidas, "datos_series.json"), simplifyVector = TRUE)
stopifnot(!is.null(sd_json$trm))
trm <- ts(as.numeric(sd_json$trm$valores),
          start = as.integer(sd_json$trm$inicio), frequency = 12)
ret <- diff(log(trm)) * 100          # variación porcentual mensual aproximada

cg_ret <- correlogramas(ret, MAX_REZAGO)

lb_ret <- lapply(c(6, 12, 20), function(h) {
  b <- Box.test(ret, lag = h, type = "Ljung-Box")
  list(rezago = h, Q = round(as.numeric(b$statistic), 4),
       p = round(as.numeric(b$p.value), 4))
})

ma1_ret  <- arima(ret, order = c(0, 0, 1), method = "ML")
auto_ret <- auto.arima(ret, d = 0, seasonal = FALSE, stepwise = FALSE,
                       approximation = FALSE, max.p = 4, max.q = 4)

retornos <- c(
  list(
    nombre  = "Log-retornos mensuales de la TRM",
    unidad  = "% mensual",
    fuente  = sd_json$trm$fuente,
    fechas  = format(seq(as.Date("2015-02-01"), by = "month",
                         length.out = length(ret)), "%Y-%m"),
    valores = round(as.numeric(ret), 4)
  ),
  cg_ret,
  list(
    ljung_box = lb_ret,
    ma1 = list(
      theta  = round(coef(ma1_ret)[["ma1"]], 4),
      se     = round(sqrt(ma1_ret$var.coef[1, 1]), 4),
      t      = round(coef(ma1_ret)[["ma1"]] / sqrt(ma1_ret$var.coef[1, 1]), 3),
      media  = round(coef(ma1_ret)[["intercept"]], 4),
      aicc   = round(aicc_de(ma1_ret, length(ret)), 3),
      lb12_p = round(as.numeric(Box.test(residuals(ma1_ret), lag = 12,
                                         type = "Ljung-Box", fitdf = 1)$p.value), 4)
    ),
    ruido_blanco_aicc = round(aicc_de(arima(ret, order = c(0, 0, 0), method = "ML"),
                                      length(ret)), 3),
    # auto.arima devuelve un MA(1) SIN media. No es un capricho: la media mensual
    # estimada tiene t = 0.84, y al quitarla el AICc mejora. Comparados en igualdad
    # de condiciones (los dos sin media), el MA(1) y el ruido blanco puro se
    # distinguen en una centésima de AICc: son indistinguibles.
    sin_media = list(
      ma1_aicc = round(aicc_de(arima(ret, order = c(0, 0, 1), include.mean = FALSE,
                                     method = "ML"), length(ret)), 3),
      ruido_blanco_aicc = round(aicc_de(arima(ret, order = c(0, 0, 0), include.mean = FALSE,
                                              method = "ML"), length(ret)), 3),
      media_t = round(coef(ma1_ret)[["intercept"]] / sqrt(ma1_ret$var.coef[2, 2]), 3),
      media_se = round(sqrt(ma1_ret$var.coef[2, 2]), 4)
    ),
    auto_arima = list(
      orden = as.integer(arimaorder(auto_ret)),
      aicc  = round(as.numeric(auto_ret$aicc), 3),
      incluye_media = "intercept" %in% names(coef(auto_ret))
    ),
    volatilidad = list(
      # La estructura que SÍ tienen los retornos financieros no está en el nivel
      # sino en el cuadrado: es la puerta a los modelos ARCH/GARCH del cap. 6.
      acf_cuadrados = round(as.numeric(acf(ret^2, lag.max = MAX_REZAGO,
                                           plot = FALSE)$acf)[-1], 4),
      lb12_cuadrados_p = round(as.numeric(Box.test(ret^2, lag = 12,
                                                   type = "Ljung-Box")$p.value), 4),
      lb12_nivel_p = round(as.numeric(Box.test(ret, lag = 12,
                                               type = "Ljung-Box")$p.value), 4)
    )
  )
)

# ----------------------------------------------------------------------------
# 5. Verificación: los pesos psi reproducen la ACF teórica de ARMAacf
#
# El capítulo calcula la ACF teórica en el navegador como
#   gamma_k = sum_j psi_j psi_{j+k},   rho_k = gamma_k / gamma_0
# con la serie truncada. Aquí se mide el error de esa aproximación contra el
# cálculo exacto de ARMAacf, para poder afirmarlo en el material con una cifra.
# ----------------------------------------------------------------------------

acf_por_psi <- function(ar, ma, lag.max, n_terminos = 2000) {
  psi <- pesos_psi(ar, ma, n_terminos)
  g <- sapply(0:lag.max, function(k) sum(psi[1:(n_terminos + 1 - k)] * psi[(1 + k):(n_terminos + 1)]))
  g[-1] / g[1]
}

verificacion <- lapply(catalogo, function(p) {
  exacta <- as.numeric(ARMAacf(ar = p$ar, ma = p$ma, lag.max = MAX_REZAGO_T))[-1]
  aprox  <- acf_por_psi(p$ar, p$ma, MAX_REZAGO_T)
  list(clave = p$clave,
       error_max = signif(max(abs(exacta - aprox)), 3))
})
error_psi_global <- signif(max(sapply(verificacion, `[[`, "error_max")), 3)

# ----------------------------------------------------------------------------
# 6. Ensamblado y escritura
# ----------------------------------------------------------------------------

cap3 <- list(
  descripcion = paste(
    "Precalculos del Capitulo 3 (modelos AR, MA y ARMA).",
    "ACF y PACF teoricas con stats::ARMAacf (calculo exacto, no simulado).",
    "Correlogramas muestrales con stats::acf (divisor n) y stats::pacf",
    "(Durbin-Levinson). Estimacion con stats::arima (metodos CSS y ML) y",
    "stats::ar (Yule-Walker y Burg). AICc = AIC + 2k(k+1)/(n-k-1) con k =",
    "n coeficientes + 1. Ljung-Box con stats::Box.test y fitdf = p + q."
  ),
  max_rezago          = MAX_REZAGO,
  max_rezago_teorico  = MAX_REZAGO_T,
  procesos            = procesos,
  realizaciones       = realizaciones,
  manchas = c(
    list(
      nombre      = "Manchas solares anuales",
      descripcion = "Numero anual de manchas solares (Wolf), 1770-1869",
      fuente      = "sunspot.year (datasets de R); ventana centenaria de Yule (1927)",
      unidad      = "numero de Wolf",
      anios       = anios,
      valores     = round(as.numeric(manchas), 4),
      media       = round(mean(manchas), 4),
      desv        = round(sd(manchas), 4)
    ),
    cg_manchas,
    list(
      metodos        = metodos,
      distancia_metodos = dist_yw_ml,
      raices         = raices_ml,
      rejilla        = rejilla,
      diagnosticos   = diagnosticos,
      transformacion = transformacion
    )
  ),
  retornos_trm = retornos,
  verificacion = list(
    metodo    = "ACF teorica por pesos psi truncados en 2000 terminos vs. ARMAacf exacta",
    por_proceso = verificacion,
    error_max = error_psi_global
  ),
  metadatos = list(
    generado    = format(Sys.Date(), "%Y-%m-%d"),
    generador   = "precalculo/genera_cap3.R",
    version_r   = paste(R.version$major, R.version$minor, sep = "."),
    forecast    = as.character(packageVersion("forecast"))
  )
)

write(toJSON(cap3, auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null"),
      file.path(dir_salidas, "cap3_arma.json"))

writeLines(paste0(
  "// Generado por precalculo/genera_cap3.R el ", format(Sys.Date(), "%Y-%m-%d"), "\n",
  "// Procesos ARMA teoricos, manchas solares y log-retornos de la TRM (Capitulo 3).\n",
  "const DATOS_CAP3 = ", toJSON(cap3, auto_unbox = TRUE, digits = NA, na = "null"), ";\n"
), file.path(dir_salidas, "cap3_datos.js"))

cat("Escrito: cap3_arma.json / cap3_datos.js\n\n")

# ----------------------------------------------------------------------------
# 7. Resumen por consola (lo que el capítulo debe citar)
# ----------------------------------------------------------------------------

cat("=== ACF/PACF teoricas: corte y decaimiento ========================\n")
for (nm in names(procesos)) {
  pr <- procesos[[nm]]
  cat(sprintf("%-10s p=%d q=%d | ACF(1..4)=%s | PACF(1..4)=%s\n",
              nm, pr$p, pr$q,
              paste(sprintf("%6.3f", pr$acf_teorica[1:4]), collapse = " "),
              paste(sprintf("%6.3f", pr$pacf_teorica[1:4]), collapse = " ")))
}
cat("\nCorte exacto (deben ser 0 hasta el redondeo):\n")
cat("  PACF del AR(1) en el rezago 2:", procesos$ar1_pos$pacf_teorica[2], "\n")
cat("  PACF del AR(2) en el rezago 3:", procesos$ar2_real$pacf_teorica[3], "\n")
cat("  ACF  del MA(1) en el rezago 2:", procesos$ma1_pos$acf_teorica[2], "\n")
cat("  ACF  del MA(2) en el rezago 3:", procesos$ma2$acf_teorica[3], "\n")

cat("\n=== Manchas solares 1770-1869 (n =", n_m, ") =====================\n")
cat("ACF (1..6) :", sprintf("%6.3f", cg_manchas$acf[1:6]), "\n")
cat("PACF(1..6) :", sprintf("%6.3f", cg_manchas$pacf[1:6]), "\n")
cat("banda      : +/-", cg_manchas$banda, "\n\n")
cat("AR(2) por tres metodos:\n")
for (m in c("yule_walker", "css", "ml")) {
  mm <- metodos[[m]]
  cat(sprintf("  %-14s phi1=%7.4f  phi2=%8.4f  sigma2=%8.2f\n",
              m, mm$phi1, mm$phi2, mm$sigma2))
}
cat(sprintf("  YW - ML: dif phi1 = %+.4f (%.2f errores estandar), dif phi2 = %+.4f (%.2f e.e.)\n",
            dist_yw_ml$dif_phi1, dist_yw_ml$dif_phi1_en_se,
            dist_yw_ml$dif_phi2, dist_yw_ml$dif_phi2_en_se))
cat(sprintf("  pseudo-periodo: YW = %.2f anios | ML = %.2f anios\n",
            dist_yw_ml$periodo_yw, dist_yw_ml$periodo_ml))
cat(sprintf("Raices (ML): %.4f +/- %.4fi, modulo %.4f -> periodo %.4f anios\n",
            raices_ml$raices[[1]]$re, abs(raices_ml$raices[[1]]$im),
            raices_ml$modulo_min, raices_ml$periodo))
cat(sprintf("  (formula cerrada del AR(2): %.4f anios)\n", raices_ml$periodo_formula_ar2))

cat("\n=== Rejilla de modelos (todos con d = 0) =========================\n")
cat(sprintf("%-12s %6s %9s %9s %9s %8s\n", "modelo", "k", "loglik", "AICc", "BIC", "LB(12) p"))
for (r in rejilla) {
  cat(sprintf("%-12s %6d %9.2f %9.2f %9.2f %8.4f%s\n",
              r$etiqueta, r$n_coef, r$loglik, r$aicc, r$bic, r$lb12_p,
              if (r$aicc == min(sapply(rejilla, `[[`, "aicc"))) "  <- min AICc" else ""))
}
cat("Minimo BIC:", rejilla[[which.min(sapply(rejilla, `[[`, "bic"))]]$etiqueta, "\n")

cat("\n=== Diagnostico de residuales ====================================\n")
for (nm in names(diagnosticos)) {
  d <- diagnosticos[[nm]]
  cat(sprintf("%-12s ACF resid(1..3)=%s  LB(12) p=%.4f  Shapiro p=%.4f\n",
              d$etiqueta, paste(sprintf("%6.3f", d$acf_resid[1:3]), collapse = " "),
              d$lb12_p, d$shapiro_p))
}

cat("\n=== La resolucion: raiz cuadrada antes de modelar =================\n")
cat("El logaritmo NO es opcion: min =", transformacion$minimo, "manchas, con",
    transformacion$n_ceros, "anio(s) en cero dentro de la ventana (",
    transformacion$n_ceros_serie_completa, "en la serie 1700-1988).\n")
cat("Elasticidad amplitud-nivel (b=0.5 -> sqrt, b=1 -> log):\n")
for (nm in names(elasticidades)) {
  e <- elasticidades[[nm]]
  cat(sprintf("   bloques de %2d anios: b = %.4f  IC95 [%.3f, %.3f]  R2 = %.3f  (%d bloques)\n",
              e$tamano, e$b, e$ic[1], e$ic[2], e$r2, e$bloques))
}
cat("   -> los tres IC excluyen 0 (hay que transformar) pero no separan sqrt de log;\n")
cat("      el cero de la serie decide, y sqrt es el estabilizador de conteos.\n")
cat("lambda de Guerrero:", transformacion$lambda_guerrero, "\n\n")
cat(sprintf("AR(2) sobre sqrt: phi=(%.4f, %.4f)  |raiz| = %.4f -> periodo %.4f anios\n",
            transformacion$sqrt$phi1, transformacion$sqrt$phi2,
            transformacion$sqrt$modulo, transformacion$sqrt$periodo))
cat(sprintf("   AICc %.2f | BIC %.2f | Ljung-Box(12) p = %.4f | Shapiro p = %.4f\n",
            transformacion$sqrt$aicc, transformacion$sqrt$bic,
            transformacion$sqrt$lb12_p, transformacion$sqrt$shapiro_p))
cat(sprintf("Con el lambda de Guerrero (%.4f) en vez de 0.5: periodo %.4f, LB p = %.4f\n",
            transformacion$box_cox_guerrero$lambda, transformacion$box_cox_guerrero$periodo,
            transformacion$box_cox_guerrero$lb12_p))
cat("   -> la conclusion no depende de haber elegido exactamente 0.5.\n\n")
cat("Rejilla sobre sqrt(manchas):\n")
cat(sprintf("%-12s %9s %9s %8s\n", "modelo", "AICc", "BIC", "LB(12) p"))
min_aicc_s <- min(sapply(rejilla_sqrt, `[[`, "aicc"))
min_bic_s  <- min(sapply(rejilla_sqrt, `[[`, "bic"))
for (r in rejilla_sqrt) {
  cat(sprintf("%-12s %9.2f %9.2f %8.4f%s%s\n", r$etiqueta, r$aicc, r$bic, r$lb12_p,
              if (r$aicc == min_aicc_s) "  <- min AICc" else "",
              if (r$bic  == min_bic_s)  "  <- min BIC"  else ""))
}
cat(sprintf("\nCOMPARACION CRUDA vs. SQRT (el hallazgo del capitulo):\n"))
cat(sprintf("   cruda: mejor AICc = ARMA(2,1); el AR(2) falla Ljung-Box (p = %.4f)\n",
            diagnosticos$arma20$lb12_p))
cat(sprintf("   sqrt : mejor AICc y mejor BIC = AR(2); pasa Ljung-Box (p = %.4f)\n",
            transformacion$sqrt$lb12_p))
cat(sprintf("   pseudo-periodo: %.2f anios (cruda) -> %.2f anios (sqrt); ciclo solar ~%.0f\n",
            raices_ml$periodo, transformacion$sqrt$periodo,
            transformacion$ciclo_solar_documentado))
cat(sprintf("   asimetria de los residuales: %.3f -> %.3f | Shapiro %.4f -> %.4f\n",
            transformacion$crudo$asimetria, transformacion$asimetria_sqrt,
            transformacion$crudo$shapiro_p, transformacion$sqrt$shapiro_p))

cat("\n=== Log-retornos de la TRM (n =", length(ret), ") ==================\n")
cat("ACF (1..6):", sprintf("%6.3f", cg_ret$acf[1:6]), " banda +/-", cg_ret$banda, "\n")
for (b in lb_ret) cat(sprintf("  Ljung-Box(%2d): Q=%7.3f  p=%.4f\n", b$rezago, b$Q, b$p))
cat(sprintf("MA(1): theta = %.4f (e.e. %.4f, t = %.2f) | AICc %.2f vs. ruido blanco %.2f\n",
            retornos$ma1$theta, retornos$ma1$se, retornos$ma1$t,
            retornos$ma1$aicc, retornos$ruido_blanco_aicc))
cat(sprintf("auto.arima(d=0) propone ARMA(%d,%d) y SIN media (incluye media: %s)\n",
            retornos$auto_arima$orden[1], retornos$auto_arima$orden[3],
            retornos$auto_arima$incluye_media))
cat(sprintf("   la media mensual %.4f%% tiene e.e. %.4f -> t = %.2f: no significativa\n",
            retornos$ma1$media, retornos$sin_media$media_se, retornos$sin_media$media_t))
cat(sprintf("   sin media: MA(1) AICc = %.3f vs. ruido blanco AICc = %.3f (dif. %.3f)\n",
            retornos$sin_media$ma1_aicc, retornos$sin_media$ruido_blanco_aicc,
            retornos$sin_media$ruido_blanco_aicc - retornos$sin_media$ma1_aicc))
cat("   -> comparados en igualdad de condiciones son INDISTINGUIBLES.\n")
cat(sprintf("Ljung-Box(12) sobre el NIVEL p = %.4f | sobre los CUADRADOS p = %.4f\n",
            retornos$volatilidad$lb12_nivel_p, retornos$volatilidad$lb12_cuadrados_p))

cat("\n=== Verificacion de los pesos psi ================================\n")
cat("Error maximo de la ACF teorica por pesos psi vs. ARMAacf:", error_psi_global, "\n")
