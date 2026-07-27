# ============================================================================
# genera_soluciones.R — Soluciones verificadas de los ejercicios propuestos
#
# Los capítulos muestran al estudiante una "solución comentada" desplegable.
# Ese texto NO puede escribirse de memoria: los numeros salen de aqui. Este
# script resuelve de verdad cada ejercicio y deja el resultado en
# salidas/soluciones_ejercicios.json, ademas de imprimir un informe legible
# que es el que se contrasta contra la prosa del HTML.
#
# Dependencias: jsonlite, tseries, forecast.
# Uso:  Rscript genera_soluciones.R      (desde la carpeta precalculo/)
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

difn <- function(x, d) if (d == 0) x else diff(x, differences = d)
banda <- function(n) 1.96 / sqrt(n)
fuera_banda <- function(x, k = 24) {
  r <- acf(x, lag.max = k, plot = FALSE)$acf[-1]
  sum(abs(r) > banda(length(x)))
}
p_kpss <- function(x) suppressWarnings(kpss.test(x)$p.value)
p_adf  <- function(x) suppressWarnings(adf.test(x)$p.value)

sol <- list()

# ============================================================================
# CAPITULO 2
# ============================================================================

# ---- Ej. 1: co2 — pipeline completo, cuantas diferencias ------------------
cat("\n=== CAP2 · Ej.1 · co2: cuantas diferencias ===\n")
# Rango relativo: si la serie apenas varia en terminos relativos, cualquier
# transformacion de potencia es casi lineal sobre ese rango y lambda queda mal
# identificado. Por eso aqui el lambda de Guerrero NO es el argumento de peso.
rango_rel_co2 <- (max(co2) - min(co2)) / mean(co2)
lam_co2 <- BoxCox.lambda(co2, method = "guerrero")
nsd_co2 <- nsdiffs(co2)
# ORDEN CORRECTO: estacional primero, y solo despues decidir la regular.
# ndiffs() sobre la serie cruda esta dominado por la estacionalidad y no es
# la cifra que hay que reportar.
co2_s  <- diff(co2, lag = 12)
nd_tras_estacional <- ndiffs(co2_s)
co2_sd <- diff(co2_s)
# La varianza tambien se compara DESPUES de la diferencia estacional
var_por_d <- sapply(0:3, function(d) var(as.numeric(difn(co2_s, d))))
acf_co2   <- acf(co2, lag.max = 24, plot = FALSE)$acf[-1]

sol$cap2_ej1 <- list(
  serie = "co2 (Mauna Loa, mensual 1959-1997)", n = length(co2),
  rango_relativo_pct = round(100 * unname(rango_rel_co2), 1),
  lambda_guerrero = round(unname(lam_co2), 4),
  ndiffs_serie_cruda = unname(ndiffs(co2)),
  nsdiffs = unname(nsd_co2),
  ndiffs_tras_diferencia_estacional = unname(nd_tras_estacional),
  acf_r1 = round(acf_co2[1], 4), acf_r12 = round(acf_co2[12], 4),
  banda = round(banda(length(co2)), 4),
  varianza_por_d_tras_estacional = round(var_por_d, 4),
  d_de_varianza_minima = which.min(var_por_d) - 1,
  final = list(
    n = length(co2_sd),
    varianza = round(var(as.numeric(co2_sd)), 5),
    acf_r1 = round(acf(co2_sd, lag.max = 1, plot = FALSE)$acf[2], 4),
    kpss_p = round(p_kpss(co2_sd), 4),
    rezagos_fuera_de_banda = fuera_banda(co2_sd),
    ndiffs = unname(ndiffs(co2_sd)), nsdiffs = unname(nsdiffs(co2_sd))
  )
)
cat(sprintf("  rango relativo = %.1f%% -> lambda mal identificado (Guerrero da %.4f, pero da igual)\n",
            100 * rango_rel_co2, lam_co2))
cat(sprintf("  nsdiffs = %d ; tras nabla12 -> ndiffs = %d   (d = %d, D = %d)\n",
            nsd_co2, nd_tras_estacional, nd_tras_estacional, nsd_co2))
cat(sprintf("  ACF de la serie cruda: r1 = %.4f, r12 = %.4f (banda +/- %.4f)\n",
            acf_co2[1], acf_co2[12], banda(length(co2))))
cat(sprintf("  varianza tras nabla12, por d = %s  -> minimo en d = %d\n",
            paste(round(var_por_d, 4), collapse = "  "), which.min(var_por_d) - 1))
cat(sprintf("  serie final nabla nabla12: n = %d, var = %.5f, r1 = %.4f, KPSS p = %.4f, fuera de banda = %d de 24\n",
            length(co2_sd), var(as.numeric(co2_sd)),
            acf(co2_sd, lag.max = 1, plot = FALSE)$acf[2], p_kpss(co2_sd), fuera_banda(co2_sd)))

# ---- Ej. 2: 500 caminatas aleatorias, % de rechazo del ADF ----------------
cat("\n=== CAP2 · Ej.2 · 500 caminatas aleatorias: falso rechazo del ADF ===\n")
set.seed(2026)
N_SIM <- 500; LARGO <- 100
p_vals <- replicate(N_SIM, suppressWarnings(adf.test(cumsum(rnorm(LARGO)))$p.value))
tasa5  <- 100 * mean(p_vals < 0.05)
tasa10 <- 100 * mean(p_vals < 0.10)
# Contraste: la misma prueba sobre series que SI son estacionarias
set.seed(2026)
p_est <- replicate(N_SIM, suppressWarnings(adf.test(rnorm(LARGO))$p.value))
potencia <- 100 * mean(p_est < 0.05)

sol$cap2_ej2 <- list(
  n_simulaciones = N_SIM, largo = LARGO, semilla = 2026,
  tasa_rechazo_5pct = round(tasa5, 1),
  tasa_rechazo_10pct = round(tasa10, 1),
  nivel_nominal = 5,
  rechazo_sobre_ruido_blanco_pct = round(potencia, 1),
  k_rezagos = trunc((LARGO - 1)^(1/3))
)
cat(sprintf("  rechaza H0 al 5%%  en %.1f%% de %d caminatas (nominal: 5%%)\n", tasa5, N_SIM))
cat(sprintf("  rechaza H0 al 10%% en %.1f%% (nominal: 10%%)\n", tasa10))
cat(sprintf("  sobre ruido blanco (H0 FALSA) rechaza en %.1f%% -> la prueba si tiene potencia\n", potencia))

# ---- Ej. 3: USAccDeaths — comparar tres diferenciaciones ------------------
cat("\n=== CAP2 · Ej.3 · USAccDeaths: tres diferenciaciones ===\n")
y <- USAccDeaths
candidatas <- list(
  "original"        = y,
  "nabla"           = diff(y),
  "nabla12"         = diff(y, lag = 12),
  "nabla12_nabla"   = diff(diff(y), lag = 12)
)
tabla_ej3 <- lapply(names(candidatas), function(nm) {
  x <- candidatas[[nm]]
  lb <- Box.test(x, lag = 24, type = "Ljung-Box")
  list(transformacion = nm, n = length(x),
       varianza = round(var(as.numeric(x)), 1),
       acf_r1 = round(acf(x, lag.max = 24, plot = FALSE)$acf[2], 4),
       acf_r12 = round(acf(x, lag.max = 24, plot = FALSE)$acf[13], 4),
       rezagos_fuera_de_banda = fuera_banda(x),
       ljung_box_p = round(unname(lb$p.value), 4),
       kpss_p = round(p_kpss(x), 4))
})
names(tabla_ej3) <- names(candidatas)
sol$cap2_ej3 <- list(serie = "USAccDeaths (mensual 1973-1978)", n = length(y),
                     ndiffs_serie_cruda = unname(ndiffs(y)),
                     nsdiffs = unname(nsdiffs(y)),
                     ndiffs_tras_diferencia_estacional = unname(ndiffs(diff(y, lag = 12))),
                     comparacion = unname(tabla_ej3))
cat(sprintf("  nsdiffs = %d ; ndiffs sobre la serie cruda = %d ; ndiffs TRAS nabla12 = %d\n",
            nsdiffs(y), ndiffs(y), ndiffs(diff(y, lag = 12))))
cat(sprintf("  %-16s %4s %10s %8s %8s %6s %9s\n", "transformacion", "n", "varianza", "r1", "r12", "fuera", "LjungBox p"))
for (t in tabla_ej3) {
  cat(sprintf("  %-16s %4d %10.1f %8.4f %8.4f %6d %9.4f\n",
              t$transformacion, t$n, t$varianza, t$acf_r1, t$acf_r12,
              t$rezagos_fuera_de_banda, t$ljung_box_p))
}

# ---- Ej. 4: TRM al corte actual (referencia) ------------------------------
cat("\n=== CAP2 · Ej.4 · TRM al corte de hoy (referencia) ===\n")
sd_json <- fromJSON(file.path(dir_salidas, "datos_series.json"), simplifyVector = TRUE)
trm <- ts(as.numeric(sd_json$trm$valores), start = as.integer(sd_json$trm$inicio), frequency = 12)
sol$cap2_ej4 <- list(
  descripcion = sd_json$trm$descripcion, n = length(trm),
  adf_p = round(p_adf(trm), 4), kpss_p = round(p_kpss(trm), 4),
  adf_p_diferenciada = round(p_adf(diff(trm)), 4),
  kpss_p_diferenciada = round(p_kpss(diff(trm)), 4),
  ndiffs = unname(ndiffs(trm))
)
cat(sprintf("  n = %d · ADF p = %.4f · KPSS p = %.4f · ndiffs = %d\n",
            length(trm), p_adf(trm), p_kpss(trm), ndiffs(trm)))

# ============================================================================
# CAPITULO 1
# ============================================================================

# ---- Ej. 1: co2 aditiva o multiplicativa ---------------------------------
cat("\n=== CAP1 · Ej.1 · co2: aditiva o multiplicativa ===\n")
# Criterio cuantitativo y no ambiguo: se mide la amplitud estacional (max-min)
# y el nivel medio DENTRO DE CADA ANIO y se ajusta
#     log(amplitud_i) = a + b * log(nivel_i)
# La pendiente b es la elasticidad amplitud-nivel:
#   b ~ 0  => la amplitud no depende del nivel  => ADITIVA
#   b ~ 1  => la amplitud es proporcional al nivel => MULTIPLICATIVA
# Comparar "cuanto crecio el nivel" con "cuanto crecio la amplitud" usando solo
# el primer y el ultimo anio es muy ruidoso; la pendiente usa todos los anios.
elasticidad <- function(x) {
  anios <- floor(time(x))
  completos <- names(which(table(anios) == frequency(x)))
  v <- as.numeric(x)
  nivel    <- tapply(v, anios, mean)[completos]
  amplitud <- tapply(v, anios, function(z) max(z) - min(z))[completos]
  fit <- lm(log(amplitud) ~ log(nivel))
  ic <- confint(fit)[2, ]
  list(anios = length(completos),
       nivel_inicial = round(unname(nivel[1]), 1),
       nivel_final = round(unname(nivel[length(nivel)]), 1),
       amplitud_inicial = round(unname(amplitud[1]), 2),
       amplitud_final = round(unname(amplitud[length(amplitud)]), 2),
       pendiente_b = round(unname(coef(fit)[2]), 3),
       ic95 = round(unname(ic), 3),
       r2 = round(summary(fit)$r.squared, 3))
}
e_co2 <- elasticidad(co2)
e_ap  <- elasticidad(AirPassengers)

# ¿La amplitud del co2 crece de verdad, o el aumento observado es ruido?
# Se contrasta la pendiente de amplitud ~ anio.
tendencia_amplitud <- function(x) {
  anios <- floor(time(x))
  completos <- names(which(table(anios) == frequency(x)))
  amplitud <- tapply(as.numeric(x), anios, function(z) max(z) - min(z))[completos]
  t_ <- as.numeric(completos)
  fit <- lm(amplitud ~ t_)
  list(pendiente_por_anio = round(unname(coef(fit)[2]), 4),
       p_valor = round(summary(fit)$coefficients[2, 4], 5),
       r2 = round(summary(fit)$r.squared, 3))
}
ta_co2 <- tendencia_amplitud(co2)

sol$cap1_ej1 <- list(
  criterio = paste0("Pendiente b de log(amplitud anual) ~ log(nivel anual). ",
                    "b ~ 0 => aditiva; b ~ 1 => multiplicativa. El IC95 y el R2 ",
                    "dicen si los datos permiten distinguir una cosa de la otra."),
  co2 = c(e_co2, list(
    lambda_guerrero = round(unname(BoxCox.lambda(co2, method = "guerrero")), 4),
    rango_relativo_del_nivel_pct = round(100 * unname((max(co2) - min(co2)) / mean(co2)), 1),
    tendencia_de_la_amplitud = ta_co2,
    veredicto = paste0("INDISTINGUIBLE: b = ", e_co2$pendiente_b, " con IC95 [",
                       e_co2$ic95[1], ", ", e_co2$ic95[2], "] y R2 = ", e_co2$r2,
                       ". El nivel solo varia un ", round(100*unname((max(co2)-min(co2))/mean(co2)), 1),
                       "% en toda la muestra, asi que las dos descomposiciones se ",
                       "parecen mucho y los datos no permiten elegir. La amplitud SI ",
                       "crece (pendiente ", ta_co2$pendiente_por_anio, " ppm/anio, p = ",
                       ta_co2$p_valor, "), lo que pide un componente estacional que ",
                       "evolucione, es decir, STL, y no una descomposicion con indices fijos."))),
  airpassengers = c(e_ap, list(
    veredicto = paste0("MULTIPLICATIVA sin ambiguedad: b = ", e_ap$pendiente_b, " con IC95 [",
                       e_ap$ic95[1], ", ", e_ap$ic95[2], "], que excluye el 0 con holgura, y R2 = ",
                       e_ap$r2, ". El nivel se multiplica por casi 4 a lo largo de la muestra.")))
)
cat(sprintf("  co2          : b = %.3f  IC95 [%.3f, %.3f]  R2 = %.3f  (nivel %.1f->%.1f, amplitud %.2f->%.2f)\n",
            e_co2$pendiente_b, e_co2$ic95[1], e_co2$ic95[2], e_co2$r2,
            e_co2$nivel_inicial, e_co2$nivel_final, e_co2$amplitud_inicial, e_co2$amplitud_final))
cat(sprintf("  AirPassengers: b = %.3f  IC95 [%.3f, %.3f]  R2 = %.3f  (nivel %.1f->%.1f, amplitud %.2f->%.2f)\n",
            e_ap$pendiente_b, e_ap$ic95[1], e_ap$ic95[2], e_ap$r2,
            e_ap$nivel_inicial, e_ap$nivel_final, e_ap$amplitud_inicial, e_ap$amplitud_final))
cat("  (b = 0 => aditiva ; b = 1 => multiplicativa)\n")
cat(sprintf("  co2: el IC95 de b abarca de %.3f a %.3f y el R2 es %.3f -> los datos NO distinguen\n",
            e_co2$ic95[1], e_co2$ic95[2], e_co2$r2))
cat(sprintf("  co2: la amplitud SI crece: %+.4f ppm/anio (p = %.5f, R2 = %.3f)\n",
            ta_co2$pendiente_por_anio, ta_co2$p_valor, ta_co2$r2))

# ---- Ej. 2: F_T y F_S de varias series -----------------------------------
cat("\n=== CAP1 · Ej.2 · Fuerza de tendencia y estacionalidad ===\n")
fuerzas <- function(x, usar_log = FALSE) {
  z <- if (usar_log) log(x) else x
  st <- stl(z, s.window = "periodic")$time.series
  R <- as.numeric(st[, "remainder"]); T_ <- as.numeric(st[, "trend"]); S <- as.numeric(st[, "seasonal"])
  c(FT = max(0, 1 - var(R) / var(T_ + R)), FS = max(0, 1 - var(R) / var(S + R)))
}
series_f <- list(co2 = co2, USAccDeaths = USAccDeaths,
                 "log(AirPassengers)" = AirPassengers)
tabla_f <- lapply(names(series_f), function(nm) {
  f <- fuerzas(series_f[[nm]], usar_log = grepl("^log", nm))
  list(serie = nm, FT = round(unname(f["FT"]), 4), FS = round(unname(f["FS"]), 4))
})
sol$cap1_ej2 <- list(
  descripcion = "F_T y F_S segun FPP3 3.6, calculadas sobre STL",
  resultados = tabla_f
)
for (t in tabla_f) cat(sprintf("  %-20s F_T = %.4f   F_S = %.4f\n", t$serie, t$FT, t$FS))

# ---- Ej. 3: un atipico rompe la descomposicion clasica, STL aguanta -------
cat("\n=== CAP1 · Ej.3 · Atipico: clasica vs STL ===\n")
# Se inyecta un atipico del +50% en julio de 1955 (obs. 79) de AirPassengers
pos <- 79
ap_out <- AirPassengers
ap_out[pos] <- ap_out[pos] * 1.5

idx_clasica <- function(x) as.numeric(decompose(x, type = "multiplicative")$figure)
# IMPORTANTE: la resistencia de STL a los atipicos viene de robust = TRUE
# (pesos de Loess reponderados). Sin esa opcion, comparar STL con la clasica
# no mide lo que el ejercicio quiere medir.
idx_stl <- function(x, robusto = TRUE) {
  s <- stl(log(x), s.window = "periodic", robust = robusto)$time.series[, "seasonal"]
  as.numeric(exp(s[1:12]))
}
cl_lim <- idx_clasica(AirPassengers); cl_out <- idx_clasica(ap_out)
st_lim <- idx_stl(AirPassengers);     st_out <- idx_stl(ap_out)
# Y para que se vea que la opcion es la que hace el trabajo, tambien sin ella
sr_lim <- idx_stl(AirPassengers, FALSE); sr_out <- idx_stl(ap_out, FALSE)

# Cuanto se mueve el indice estacional de JULIO (el mes contaminado)
sol$cap1_ej3 <- list(
  atipico = list(posicion = pos, fecha = "1955-07", factor = 1.5,
                 valor_original = as.numeric(AirPassengers[pos]),
                 valor_contaminado = as.numeric(ap_out[pos])),
  indice_julio = list(
    clasica_limpia = round(cl_lim[7], 4), clasica_contaminada = round(cl_out[7], 4),
    clasica_cambio_pct = round(100 * (cl_out[7] / cl_lim[7] - 1), 2),
    stl_limpia = round(st_lim[7], 4), stl_contaminada = round(st_out[7], 4),
    stl_cambio_pct = round(100 * (st_out[7] / st_lim[7] - 1), 2)
  ),
  distorsion_maxima_todos_los_meses_pct = list(
    clasica = round(max(abs(100 * (cl_out / cl_lim - 1))), 2),
    stl_robusto = round(max(abs(100 * (st_out / st_lim - 1))), 2),
    stl_sin_robust = round(max(abs(100 * (sr_out / sr_lim - 1))), 2)
  ),
  nota = paste0("La ventaja de STL depende de robust = TRUE. Sin esa opcion su ",
                "distorsion es comparable a la de la descomposicion clasica.")
)
cat(sprintf("  atipico: julio de 1955, %g -> %g (+50%%)\n", AirPassengers[pos], ap_out[pos]))
cat(sprintf("  indice de julio · clasica          : %.4f -> %.4f (%+.2f%%)\n",
            cl_lim[7], cl_out[7], 100*(cl_out[7]/cl_lim[7]-1)))
cat(sprintf("  indice de julio · STL robust=TRUE  : %.4f -> %.4f (%+.2f%%)\n",
            st_lim[7], st_out[7], 100*(st_out[7]/st_lim[7]-1)))
cat(sprintf("  indice de julio · STL robust=FALSE : %.4f -> %.4f (%+.2f%%)\n",
            sr_lim[7], sr_out[7], 100*(sr_out[7]/sr_lim[7]-1)))
cat(sprintf("  distorsion maxima entre los 12 meses · clasica %.2f%% | STL robusto %.2f%% | STL sin robust %.2f%%\n",
            max(abs(100*(cl_out/cl_lim-1))), max(abs(100*(st_out/st_lim-1))),
            max(abs(100*(sr_out/sr_lim-1)))))

# ============================================================================
# CAPITULO 3
# ============================================================================

aicc_de <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2 * k * (k + 1) / (n - k - 1) }

# ---- Ej. 1: identificar y elegir un modelo para lh -------------------------
# El punto del ejercicio es que AICc y BIC NO coinciden, y que los dos
# candidatos pasan el diagnostico: la eleccion se decide por parsimonia.
cat("\n=== CAP3 · Ej.1 · lh: identificacion y seleccion ===\n")
n_lh <- length(lh)
cand_lh <- list(c(1,0), c(2,0), c(3,0), c(0,1), c(0,2), c(1,1))
tabla_lh <- do.call(rbind, lapply(cand_lh, function(pq) {
  f <- arima(lh, order = c(pq[1], 0, pq[2]), method = "ML")
  data.frame(modelo = sprintf("ARMA(%d,%d)", pq[1], pq[2]),
             AICc = round(aicc_de(f, n_lh), 3),
             BIC  = round(as.numeric(BIC(f)), 3),
             LB10 = round(Box.test(residuals(f), lag = 10, type = "Ljung-Box",
                                   fitdf = sum(pq))$p.value, 4))
}))
ar1_lh <- arima(lh, order = c(1, 0, 0), method = "ML")
sol$cap3_ej1 <- list(
  n = n_lh, banda = round(banda(n_lh), 4),
  acf  = round(as.numeric(acf(lh,  lag.max = 6, plot = FALSE)$acf)[-1], 4),
  pacf = round(as.numeric(pacf(lh, lag.max = 6, plot = FALSE)$acf), 4),
  tabla = tabla_lh,
  mejor_aicc = tabla_lh$modelo[which.min(tabla_lh$AICc)],
  mejor_bic  = tabla_lh$modelo[which.min(tabla_lh$BIC)],
  ar1 = list(phi = round(coef(ar1_lh)[["ar1"]], 4),
             ee = round(sqrt(ar1_lh$var.coef[1, 1]), 4),
             media = round(coef(ar1_lh)[["intercept"]], 4),
             shapiro_p = round(shapiro.test(residuals(ar1_lh))$p.value, 6)),
  nota = paste("El AICc elige MA(2) y el BIC elige AR(1) por 0.17 puntos.",
               "Los dos pasan Ljung-Box; se recomienda el AR(1) por parsimonia.")
)
print(tabla_lh, row.names = FALSE)
cat(sprintf("  banda = %.4f | min AICc = %s | min BIC = %s (diferencia BIC = %.3f)\n",
            banda(n_lh), sol$cap3_ej1$mejor_aicc, sol$cap3_ej1$mejor_bic,
            diff(sort(tabla_lh$BIC))[1]))
cat(sprintf("  AR(1): phi = %.4f (e.e. %.4f) · Shapiro p = %.6f\n",
            sol$cap3_ej1$ar1$phi, sol$cap3_ej1$ar1$ee, sol$cap3_ej1$ar1$shapiro_p))

# ---- Ej. 2: MA(2) con theta = (0.6, 0.4) ----------------------------------
# Ademas de la invertibilidad, el ejercicio comprueba que la cota |rho_1|<=0.5
# es propia del MA(1) y NO se extiende al MA(2).
cat("\n=== CAP3 · Ej.2 · MA(2) theta = (0.6, 0.4) ===\n")
th <- c(0.6, 0.4)
raices_ma <- polyroot(c(1, th))
den <- 1 + sum(th^2)
sol$cap3_ej2 <- list(
  theta = th,
  raices_re = round(Re(raices_ma), 4), raices_im = round(Im(raices_ma), 4),
  modulo = round(Mod(raices_ma), 4),
  invertible = all(Mod(raices_ma) > 1),
  rho1_a_mano = round((th[1] + th[1] * th[2]) / den, 4),
  rho2_a_mano = round(th[2] / den, 4),
  acf_armaacf = round(as.numeric(ARMAacf(ma = th, lag.max = 4))[-1], 4),
  pesos_pi = round(as.numeric(ARMAtoMA(ar = -th, lag.max = 8)), 4),
  supera_cota_ma1 = abs((th[1] + th[1] * th[2]) / den) > 0.5,
  nota = paste("rho_1 = 0.5526 > 0.5: la cota del Modulo 3 se dedujo solo para",
               "el MA(1) y no se aplica al MA(2).")
)
cat(sprintf("  raices %.4f +/- %.4fi · modulo %.4f -> invertible: %s\n",
            Re(raices_ma)[1], abs(Im(raices_ma))[1], Mod(raices_ma)[1],
            sol$cap3_ej2$invertible))
cat(sprintf("  rho1 = %.4f (a mano) = %.4f (ARMAacf) · rho2 = %.4f\n",
            sol$cap3_ej2$rho1_a_mano, sol$cap3_ej2$acf_armaacf[1], sol$cap3_ej2$rho2_a_mano))
cat(sprintf("  |rho_1| > 0.5: %s  <- la cota del MA(1) NO vale para el MA(2)\n",
            sol$cap3_ej2$supera_cota_ma1))

# ---- Ej. 3: estabilidad del AR(2) sobre sqrt(manchas) ---------------------
# Tres lecturas distintas: coeficientes estables, periodo sensible y
# diagnostico que se derrumba al crecer n (la prueba gana potencia).
cat("\n=== CAP3 · Ej.3 · estabilidad del AR(2) por ventanas ===\n")
ventanas <- list(c(1770, 1869), c(1700, 1988), c(1870, 1988), c(1900, 1988))
tabla_vent <- do.call(rbind, lapply(ventanas, function(v) {
  x <- sqrt(window(sunspot.year, v[1], v[2]))
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  r <- polyroot(c(1, -coef(f)[1:2]))
  data.frame(ventana = sprintf("%d-%d", v[1], v[2]), n = length(x),
             phi1 = round(coef(f)[["ar1"]], 4), phi2 = round(coef(f)[["ar2"]], 4),
             ee1 = round(sqrt(f$var.coef[1, 1]), 4),
             modulo = round(Mod(r)[1], 4),
             periodo = round(2 * pi / Arg(r[1]), 3),
             LB12 = round(Box.test(residuals(f), lag = 12, type = "Ljung-Box",
                                   fitdf = 2)$p.value, 4))
}))
sol$cap3_ej3 <- list(
  tabla = tabla_vent,
  rango_phi1 = round(range(tabla_vent$phi1), 4),
  rango_phi2 = round(range(tabla_vent$phi2), 4),
  rango_periodo = round(range(tabla_vent$periodo), 3),
  nota = paste("Los coeficientes apenas se mueven, el periodo cae de 11.22 a",
               "10.13 anios y el diagnostico falla fuera de la ventana de Yule",
               "porque la prueba gana potencia con n, no porque el modelo empeore.")
)
print(tabla_vent, row.names = FALSE)
cat(sprintf("  phi1 en [%.4f, %.4f] · phi2 en [%.4f, %.4f] · periodo en [%.3f, %.3f]\n",
            sol$cap3_ej3$rango_phi1[1], sol$cap3_ej3$rango_phi1[2],
            sol$cap3_ej3$rango_phi2[1], sol$cap3_ej3$rango_phi2[2],
            sol$cap3_ej3$rango_periodo[1], sol$cap3_ej3$rango_periodo[2]))

# ============================================================================
# CAPITULO 4
# ============================================================================

aicc_de <- function(f, n_ef) { k <- length(f$coef) + 1; as.numeric(f$aic + 2*k*(k+1)/(n_ef-k-1)) }
bic_de  <- function(f, n_ef) { k <- length(f$coef) + 1; as.numeric(f$aic - 2*k + log(n_ef)*k) }
modulos_ma <- function(f) {
  mc <- f$coef[grepl("^ma", names(f$coef))]
  if (!length(mc)) return(NA_real_)
  round(min(Mod(polyroot(c(1, mc)))), 4)
}

# ---- Ej. 1: BJsales, el Box-Jenkins original ------------------------------
# La Serie M de Box & Jenkins. El punto: elegir d ANTES que (p,q), y ver que
# el AICc de d=1 y el de d=2 no se pueden comparar porque n cambia.
cat("\n=== CAP4 · Ej.1 · BJsales de principio a fin ===\n")
bj <- BJsales
n_bj <- length(bj)
sol$cap4_ej1 <- list(
  serie = "BJsales (Box & Jenkins, Serie M)", n = n_bj,
  pruebas = list(
    adf_nivel = round(suppressWarnings(adf.test(bj)$p.value), 4),
    kpss_nivel = round(p_kpss(bj), 4),
    adf_d1 = round(suppressWarnings(adf.test(diff(bj))$p.value), 4),
    kpss_d1 = round(p_kpss(diff(bj)), 4),
    ndiffs = ndiffs(bj)),
  varianzas = sapply(0:3, function(d) round(var(difn(bj, d)), 4),
                     USE.NAMES = FALSE),
  acf_d1 = round(as.numeric(acf(diff(bj), lag.max = 6, plot = FALSE)$acf)[-1], 4),
  pacf_d1 = round(as.numeric(pacf(diff(bj), lag.max = 6, plot = FALSE)$acf)[1:6], 4),
  banda_d1 = round(banda(n_bj - 1), 4)
)
rej_bj <- do.call(rbind, lapply(0:2, function(q) do.call(rbind, lapply(0:2, function(p) {
  f <- tryCatch(arima(bj, order = c(p, 1, q), method = "ML"), error = function(e) NULL)
  if (is.null(f)) return(NULL)
  data.frame(modelo = sprintf("ARIMA(%d,1,%d)", p, q),
             aicc = round(aicc_de(f, n_bj - 1), 3), bic = round(bic_de(f, n_bj - 1), 3),
             lb20 = round(Box.test(residuals(f), lag = 20, type = "Ljung-Box",
                                   fitdf = p + q)$p.value, 4),
             min_raiz_ma = modulos_ma(f))
}))))
rej_bj <- rej_bj[order(rej_bj$aicc), ]
sol$cap4_ej1$rejilla_d1 <- rej_bj
sol$cap4_ej1$mejor_aicc <- rej_bj$modelo[1]
sol$cap4_ej1$mejor_bic <- rej_bj$modelo[which.min(rej_bj$bic)]
# El ganador es el ARIMA(1,1,1) por AICc, por BIC y por auto.arima.
f_bj <- arima(bj, order = c(1, 1, 1), method = "ML")
ee_bj <- sqrt(diag(f_bj$var.coef))
sol$cap4_ej1$ganador <- list(
  modelo = "ARIMA(1,1,1)",
  phi = round(coef(f_bj)[["ar1"]], 4), phi_ee = round(ee_bj[["ar1"]], 4),
  theta = round(coef(f_bj)[["ma1"]], 4), theta_ee = round(ee_bj[["ma1"]], 4),
  sigma2 = round(f_bj$sigma2, 4),
  aicc = round(aicc_de(f_bj, n_bj - 1), 3),
  lb20_p = round(Box.test(residuals(f_bj), lag = 20, type = "Ljung-Box", fitdf = 2)$p.value, 4),
  shapiro_p = round(shapiro.test(residuals(f_bj))$p.value, 4))

# El "IMA(1,1) de libro" para esta serie NO pasa el diagnostico: ese es el
# punto del ejercicio, y no se ve mirando solo los criterios de informacion.
f_bj011 <- arima(bj, order = c(0, 1, 1), method = "ML")
sol$cap4_ej1$candidato_de_libro <- list(
  modelo = "ARIMA(0,1,1)",
  theta = round(coef(f_bj011)[["ma1"]], 4),
  aicc = round(aicc_de(f_bj011, n_bj - 1), 3),
  lb20_p = round(Box.test(residuals(f_bj011), lag = 20, type = "Ljung-Box",
                          fitdf = 1)$p.value, 4),
  acf_residual_1a4 = round(as.numeric(acf(residuals(f_bj011), lag.max = 4,
                                          plot = FALSE)$acf)[-1], 4),
  # residuals() de un ajuste con d = 1 devuelve n valores, no n - d: la banda
  # que corresponde a ese correlograma se calcula sobre esa longitud.
  banda = round(banda(length(residuals(f_bj011))), 4),
  nota = "Estructura residual en los rezagos 2 y 4: el termino AR hace falta.")

# La comparacion INVALIDA que el ejercicio pide detectar, y ademas degenerada.
rej_bj2 <- do.call(rbind, lapply(0:2, function(q) do.call(rbind, lapply(0:2, function(p) {
  f <- tryCatch(arima(bj, order = c(p, 2, q), method = "ML"), error = function(e) NULL)
  if (is.null(f)) return(NULL)
  data.frame(modelo = sprintf("ARIMA(%d,2,%d)", p, q),
             aicc = round(aicc_de(f, n_bj - 2), 3), min_raiz_ma = modulos_ma(f))
}))))
mejor_d2 <- rej_bj2[which.min(rej_bj2$aicc), ]
sol$cap4_ej1$trampa_d2 <- list(
  mejor_modelo = as.character(mejor_d2$modelo), aicc = mejor_d2$aicc,
  min_raiz_ma = mejor_d2$min_raiz_ma,
  n_efectivo = n_bj - 2, n_efectivo_d1 = n_bj - 1,
  aicc_ganador_d1 = round(aicc_de(f_bj, n_bj - 1), 3),
  nota = paste("Dos motivos independientes para descartarlo: su AICc se calcula",
               "sobre 148 observaciones y el del d = 1 sobre 149 (no son",
               "comparables), y su raiz MA cae SOBRE el circulo unitario, que es",
               "la firma algebraica de haber diferenciado de mas."))
sol$cap4_ej1$auto <- as.character(auto.arima(bj, stepwise = FALSE,
                                             approximation = FALSE, seasonal = FALSE))
cat(sprintf("  n = %d | ndiffs = %d | ADF nivel p = %.4f -> d = 1\n",
            n_bj, sol$cap4_ej1$pruebas$ndiffs, sol$cap4_ej1$pruebas$adf_nivel))
cat("  varianza por d:", sol$cap4_ej1$varianzas, "\n")
print(rej_bj, row.names = FALSE)
cat(sprintf("  min AICc = %s | min BIC = %s | auto.arima -> %s\n",
            sol$cap4_ej1$mejor_aicc, sol$cap4_ej1$mejor_bic, sol$cap4_ej1$auto))
cat(sprintf("  GANADOR (1,1,1): phi = %.4f (e.e. %.4f), theta = %.4f (e.e. %.4f)\n",
            sol$cap4_ej1$ganador$phi, sol$cap4_ej1$ganador$phi_ee,
            sol$cap4_ej1$ganador$theta, sol$cap4_ej1$ganador$theta_ee))
cat(sprintf("           LB(20) p = %.4f | Shapiro p = %.4f\n",
            sol$cap4_ej1$ganador$lb20_p, sol$cap4_ej1$ganador$shapiro_p))
cat(sprintf("  EL DE LIBRO (0,1,1) NO PASA: LB(20) p = %.4f | ACF residual r1..r4 = %s (banda %.4f)\n",
            sol$cap4_ej1$candidato_de_libro$lb20_p,
            paste(sol$cap4_ej1$candidato_de_libro$acf_residual_1a4, collapse = ", "),
            sol$cap4_ej1$candidato_de_libro$banda))
cat(sprintf("  TRAMPA d=2: mejor es %s con AICc %.3f sobre n = %d y |raiz MA| = %.4f\n",
            sol$cap4_ej1$trampa_d2$mejor_modelo, sol$cap4_ej1$trampa_d2$aicc,
            sol$cap4_ej1$trampa_d2$n_efectivo, sol$cap4_ej1$trampa_d2$min_raiz_ma))

# ---- Ej. 2: lynx, un ciclo NO es una raiz unitaria ------------------------
cat("\n=== CAP4 · Ej.2 · log(lynx): ciclo, no raiz unitaria ===\n")
ly <- log(lynx)
n_ly <- length(ly)
f_ly <- arima(ly, order = c(2, 0, 0), method = "ML")
r_ly <- polyroot(c(1, -coef(f_ly)[1:2]))
sol$cap4_ej2 <- list(
  serie = "log(lynx)", n = n_ly,
  ndiffs_kpss = ndiffs(ly, test = "kpss"),
  ndiffs_adf = ndiffs(ly, test = "adf"),
  kpss_p = round(p_kpss(ly), 4), adf_p = round(p_adf(ly), 4),
  acf = round(as.numeric(acf(ly, lag.max = 12, plot = FALSE)$acf)[-1], 4),
  banda = round(banda(n_ly), 4),
  varianzas = sapply(0:2, function(d) round(var(difn(ly, d)), 4), USE.NAMES = FALSE),
  ar2 = list(phi1 = round(coef(f_ly)[["ar1"]], 4), phi2 = round(coef(f_ly)[["ar2"]], 4),
             modulo = round(Mod(r_ly)[1], 4),
             periodo = round(2 * pi / Arg(r_ly[which.max(Im(r_ly))]), 3),
             aicc = round(aicc_de(f_ly, n_ly), 3),
             lb20_p = round(Box.test(residuals(f_ly), lag = 20, type = "Ljung-Box",
                                     fitdf = 2)$p.value, 4)),
  auto = as.character(auto.arima(ly, stepwise = FALSE, approximation = FALSE, seasonal = FALSE))
)
# HALLAZGO: aqui la regla "si te pasas diferenciando, la varianza SUBE" FALLA.
# Sobre log(lynx) la varianza BAJA al diferenciar, y aun asi d = 1 esta de mas.
# Lo que si lo detecta es la raiz unitaria que aparece en la parte MA.
sol$cap4_ej2$regla_varianza <- list(
  var_d0 = round(var(ly), 4), var_d1 = round(var(diff(ly)), 4),
  cambio_pct = round(100 * (var(diff(ly)) / var(ly) - 1), 1),
  la_regla_funciona = var(diff(ly)) > var(ly),
  nota = paste("La varianza cae un 58 %: la regla heuristica no dispara. En una",
               "serie con ciclo fuerte, diferenciar reduce la varianza aunque",
               "sobre. El detector fiable es la raiz del polinomio MA."))
sol$cap4_ej2$diferenciada <- do.call(rbind, lapply(
  list(c(2, 1, 0), c(2, 1, 1), c(0, 1, 1)), function(o) {
    f <- arima(ly, order = o, method = "ML")
    data.frame(modelo = sprintf("ARIMA(%d,%d,%d)", o[1], o[2], o[3]),
               aicc = round(aicc_de(f, n_ly - o[2]), 3),
               min_raiz_ma = modulos_ma(f),
               lb20_p = round(Box.test(residuals(f), lag = 20, type = "Ljung-Box",
                                       fitdf = o[1] + o[3])$p.value, 4))
  }))
cat(sprintf("  n = %d | ndiffs(kpss) = %d, ndiffs(adf) = %d | KPSS p = %.4f, ADF p = %.4f\n",
            n_ly, sol$cap4_ej2$ndiffs_kpss, sol$cap4_ej2$ndiffs_adf,
            sol$cap4_ej2$kpss_p, sol$cap4_ej2$adf_p))
cat(sprintf("  varianza d=0 -> d=1: %.4f -> %.4f (%.1f %%). La regla de la varianza %s\n",
            sol$cap4_ej2$regla_varianza$var_d0, sol$cap4_ej2$regla_varianza$var_d1,
            sol$cap4_ej2$regla_varianza$cambio_pct,
            ifelse(sol$cap4_ej2$regla_varianza$la_regla_funciona, "dispara", "NO DISPARA")))
print(sol$cap4_ej2$diferenciada, row.names = FALSE)
cat("  -> el ARIMA(2,1,1) pone |raiz MA| = 1 exacto: el MA cancela la diferencia.\n")
cat(sprintf("  AR(2) sin diferenciar: phi = (%.4f, %.4f) | |raiz| = %.4f -> periodo %.2f anios\n",
            sol$cap4_ej2$ar2$phi1, sol$cap4_ej2$ar2$phi2, sol$cap4_ej2$ar2$modulo,
            sol$cap4_ej2$ar2$periodo))
cat(sprintf("  pero LB(20) p = %.4f: tampoco basta | auto.arima -> %s\n",
            sol$cap4_ej2$ar2$lb20_p, sol$cap4_ej2$auto))

# ---- Ej. 3: intervalos de pronostico a mano, con los pesos psi ------------
cat("\n=== CAP4 · Ej.3 · el intervalo, a mano, desde los pesos psi ===\n")
# Sobre el ARIMA(1,1,1), que es el modelo que selecciona el ejercicio 1. Usar
# el (0,1,1) aqui seria construir un intervalo con un modelo ya rechazado.
f3 <- Arima(BJsales, order = c(1, 1, 1))
ph3 <- as.numeric(coef(f3)["ar1"]); th3 <- as.numeric(coef(f3)["ma1"])
s3 <- sqrt(f3$sigma2)
H3 <- 12
# ARIMA(1,1,1) sobre y equivale a un ARMA(2,1) con phi* = (1 + phi, -phi)
# sobre la serie SIN diferenciar. De ahi salen los psi.
psi3 <- c(1, ARMAtoMA(ar = c(1 + ph3, -ph3), ma = th3, lag.max = H3))
sh3 <- s3 * sqrt(cumsum(psi3^2))[1:H3]
fc3 <- forecast(f3, h = H3, level = c(80, 95))
semi95 <- as.numeric((fc3$upper[, 2] - fc3$lower[, 2]) / 2)
f3d <- Arima(BJsales, order = c(1, 1, 1), include.drift = TRUE)
fc3d <- forecast(f3d, h = H3, level = 95)
sol$cap4_ej3 <- list(
  modelo = "ARIMA(1,1,1) sobre BJsales",
  phi = round(ph3, 4), theta = round(th3, 4), sigma = round(s3, 4),
  psi_0a4 = round(psi3[1:5], 4),
  psi_limite = round(psi3[H3 + 1], 4),
  psi_limite_teorico = round((1 + th3) / (1 - ph3), 4),
  sigma_h_1a5 = round(sh3[1:5], 4),
  semiancho95_1a5 = round(semi95[1:5], 4),
  error_maximo = signif(max(abs(semi95 - qnorm(0.975) * sh3)), 4),
  razon_h12_h1 = round(sh3[H3] / sh3[1], 4),
  razon_raiz_h = round(sqrt(H3), 4),
  con_deriva = list(
    deriva = round(as.numeric(coef(f3d)["drift"]), 4),
    ee = round(as.numeric(sqrt(diag(f3d$var.coef))["drift"]), 4),
    t = round(as.numeric(coef(f3d)["drift"] / sqrt(diag(f3d$var.coef))["drift"]), 3),
    aicc = round(as.numeric(f3d$aicc), 3), aicc_sin = round(as.numeric(f3$aicc), 3),
    pronostico_h12 = round(as.numeric(fc3d$mean[H3]), 3),
    pronostico_h12_sin = round(as.numeric(fc3$mean[H3]), 3),
    ancho95_h12 = round(as.numeric(fc3d$upper[H3, 1] - fc3d$lower[H3, 1]), 3),
    ancho95_h12_sin = round(as.numeric(fc3$upper[H3, 2] - fc3$lower[H3, 2]), 3))
)
cat(sprintf("  phi = %.4f, theta = %.4f -> psi con ar* = (%.4f, %.4f)\n",
            ph3, th3, 1 + ph3, -ph3))
cat("  psi_0..psi_4:", sol$cap4_ej3$psi_0a4, "\n")
cat(sprintf("  psi_j tiende a (1+theta)/(1-phi) = %.4f (calculado: %.4f)\n",
            sol$cap4_ej3$psi_limite_teorico, sol$cap4_ej3$psi_limite))
cat("  sigma_h (h=1..5):", sol$cap4_ej3$sigma_h_1a5, "\n")
cat("  semiancho 95 % de forecast():", sol$cap4_ej3$semiancho95_1a5, "\n")
cat(sprintf("  error maximo entre las dos vias: %.3e\n", sol$cap4_ej3$error_maximo))
cat(sprintf("  sigma_12/sigma_1 = %.4f, frente a sqrt(12) = %.4f\n",
            sol$cap4_ej3$razon_h12_h1, sol$cap4_ej3$razon_raiz_h))
cat(sprintf("  deriva = %.4f (e.e. %.4f, t = %.2f) | AICc %.3f con deriva vs. %.3f sin\n",
            sol$cap4_ej3$con_deriva$deriva, sol$cap4_ej3$con_deriva$ee,
            sol$cap4_ej3$con_deriva$t, sol$cap4_ej3$con_deriva$aicc,
            sol$cap4_ej3$con_deriva$aicc_sin))
cat(sprintf("  pronostico a h=12: %.2f con deriva vs. %.2f sin\n",
            sol$cap4_ej3$con_deriva$pronostico_h12, sol$cap4_ej3$con_deriva$pronostico_h12_sin))

# ============================================================================
# CAPITULO 5
# ============================================================================

difrs <- function(x, d = 0, D = 0, m = 12) {
  if (D > 0) x <- diff(x, lag = m, differences = D)
  if (d > 0) x <- diff(x, differences = d)
  x
}
gl_arma <- function(f) sum(f$arma[1:4])
lb_p <- function(f, k = 24) Box.test(residuals(f), lag = k, type = "Ljung-Box",
                                     fitdf = gl_arma(f))$p.value
raiz_ma_max <- function(f) {
  th <- f$model$theta
  if (!length(th) || all(th == 0)) return(NA_real_)
  round(max(Mod(1 / polyroot(c(1, th)))), 4)
}

# ---- Ej. 1: co2 de Mauna Loa, recorrido SARIMA completo --------------------
# El punto NO es acertar el modelo, sino que la tabla de la rejilla solo se
# puede leer dentro de un mismo (d, D). El estudiante que ordene los 4 valores
# de varianza y elija el minimo llega a (1,1); el que ademas compare AICc entre
# distintos D se equivoca, y aqui se le muestra por que.
cat("\n=== CAP5 · Ej.1 · co2 de Mauna Loa, recorrido SARIMA ===\n")
co2v <- co2
varianzas_co2 <- c(
  d0D0 = var(co2v), d1D0 = var(diff(co2v)),
  d0D1 = var(diff(co2v, lag = 12)), d1D1 = var(difrs(co2v, 1, 1))
)
rej_co2 <- list()
for (p in 0:2) for (q in 0:3) for (P in 0:1) for (Q in 0:1) {
  f <- tryCatch(Arima(co2v, order = c(p, 1, q),
                      seasonal = list(order = c(P, 1, Q), period = 12), method = "ML"),
                error = function(e) NULL, warning = function(w) NULL)
  if (is.null(f)) next
  rej_co2[[sprintf("(%d,1,%d)(%d,1,%d)[12]", p, q, P, Q)]] <-
    list(aicc = round(f$aicc, 3), bic = round(f$bic, 3), lb = round(lb_p(f), 4),
         k = p + q + P + Q, nobs = f$nobs)
}
mejor_co2 <- names(rej_co2)[which.min(vapply(rej_co2, function(r) r$aicc, numeric(1)))]
mejor_co2_bic <- names(rej_co2)[which.min(vapply(rej_co2, function(r) r$bic, numeric(1)))]
airline_co2 <- Arima(co2v, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
auto_co2 <- auto.arima(co2v, stepwise = FALSE, approximation = FALSE)
# La comparacion INVALIDA que el ejercicio quiere que el estudiante detecte:
# el mismo (p,q) con D = 0 tiene mas observaciones y su AICc parece mejor.
sinD_co2 <- Arima(co2v, order = c(0, 1, 1), seasonal = list(order = c(0, 0, 1), period = 12))

sol$cap5_ej1 <- list(
  n = length(co2v),
  varianzas = round(varianzas_co2, 4),
  varianza_minima = names(which.min(varianzas_co2)),
  ndiffs = ndiffs(co2v), ndiffs_tras_D = ndiffs(diff(co2v, lag = 12)),
  nsdiffs = nsdiffs(co2v),
  n_modelos = length(rej_co2),
  mejor_aicc = mejor_co2, mejor_bic = mejor_co2_bic,
  aicc_mejor = rej_co2[[mejor_co2]]$aicc, bic_mejor = rej_co2[[mejor_co2]]$bic,
  lb_mejor = rej_co2[[mejor_co2]]$lb,
  auto_arima = as.character(auto_co2), auto_aicc = round(auto_co2$aicc, 3),
  airline_aicc = round(airline_co2$aicc, 3), airline_lb = round(lb_p(airline_co2), 4),
  diferencia_aicc = round(airline_co2$aicc - auto_co2$aicc, 3),
  trampa = list(
    modelo_sinD = "(0,1,1)(0,0,1)[12]",
    aicc_sinD = round(sinD_co2$aicc, 3), nobs_sinD = sinD_co2$nobs,
    aicc_conD = round(airline_co2$aicc, 3), nobs_conD = airline_co2$nobs,
    lb_sinD = round(lb_p(sinD_co2), 4),
    leccion = paste("Aqui el AICc sin diferencia estacional sale MUCHO peor y ademas el",
                    "modelo no pasa Ljung-Box, asi que la lectura ingenua acierta por",
                    "casualidad. Sigue siendo invalida: se calcula sobre 12 observaciones",
                    "mas. En el ejercicio 3 los dos numeros quedan a dos puntos de",
                    "distancia y ahi la lectura ingenua si enganya.")
  )
)
s1 <- sol$cap5_ej1
cat(sprintf("  n = %d | ndiffs = %d (tras la estacional: %d) | nsdiffs = %d\n",
            s1$n, s1$ndiffs, s1$ndiffs_tras_D, s1$nsdiffs))
cat(sprintf("  Varianzas: cruda %.4f | d=1 %.4f | D=1 %.4f | ambas %.4f -> minimo en %s\n",
            s1$varianzas[["d0D0"]], s1$varianzas[["d1D0"]], s1$varianzas[["d0D1"]],
            s1$varianzas[["d1D1"]], s1$varianza_minima))
cat(sprintf("  Rejilla de %d modelos (todos d=1, D=1): mejor por AICc %s (%.3f), por BIC %s\n",
            s1$n_modelos, s1$mejor_aicc, s1$aicc_mejor, s1$mejor_bic))
cat(sprintf("  auto.arima: %s (AICc %.3f) | airline: AICc %.3f (%.3f peor) | LB p = %.4f\n",
            s1$auto_arima, s1$auto_aicc, s1$airline_aicc, s1$diferencia_aicc, s1$airline_lb))
cat(sprintf("  TRAMPA: %s da AICc %.3f con %d obs. frente a %.3f con %d obs. del airline\n",
            s1$trampa$modelo_sinD, s1$trampa$aicc_sinD, s1$trampa$nobs_sinD,
            s1$trampa$aicc_conD, s1$trampa$nobs_conD))
cat(sprintf("          y su Ljung-Box(24) da p = %.4f: el modelo 'ganador' no pasa el diagnostico.\n",
            s1$trampa$lb_sinD))

# ---- Ej. 2: USAccDeaths, decidir d y D en el orden correcto ----------------
# ndiffs sobre la serie cruda dice 0. Tras la diferencia estacional dice 1.
# La estacionalidad enmascara la tendencia: hay que quitarla primero.
cat("\n=== CAP5 · Ej.2 · USAccDeaths: el orden en que se decide d y D ===\n")
ua <- USAccDeaths
orden_mal <- list(ndiffs_primero = ndiffs(ua), nsdiffs_despues = NA)
ua_d <- if (ndiffs(ua) > 0) diff(ua, differences = ndiffs(ua)) else ua
orden_mal$nsdiffs_despues <- nsdiffs(ua_d)
orden_bien <- list(nsdiffs_primero = nsdiffs(ua),
                   ndiffs_despues = ndiffs(diff(ua, lag = 12)))
mod_orden_mal <- Arima(ua, order = c(0, orden_mal$ndiffs_primero, 1),
                       seasonal = list(order = c(0, orden_mal$nsdiffs_despues, 1), period = 12))
mod_orden_bien <- Arima(ua, order = c(0, orden_bien$ndiffs_despues, 1),
                        seasonal = list(order = c(0, orden_bien$nsdiffs_primero, 1), period = 12))
auto_ua <- auto.arima(ua, stepwise = FALSE, approximation = FALSE)

sol$cap5_ej2 <- list(
  n = length(ua),
  orden_mal = orden_mal, orden_bien = orden_bien,
  conmutan = max(abs(as.numeric(diff(diff(ua, lag = 12))) - as.numeric(diff(diff(ua), lag = 12)))),
  modelo_orden_mal = list(
    d = orden_mal$ndiffs_primero, D = orden_mal$nsdiffs_despues,
    etiqueta = sprintf("(0,%d,1)(0,%d,1)[12]", orden_mal$ndiffs_primero, orden_mal$nsdiffs_despues),
    aicc = round(mod_orden_mal$aicc, 3), nobs = mod_orden_mal$nobs,
    lb = round(lb_p(mod_orden_mal), 4)),
  modelo_orden_bien = list(
    d = orden_bien$ndiffs_despues, D = orden_bien$nsdiffs_primero,
    etiqueta = sprintf("(0,%d,1)(0,%d,1)[12]", orden_bien$ndiffs_despues, orden_bien$nsdiffs_primero),
    aicc = round(mod_orden_bien$aicc, 3), nobs = mod_orden_bien$nobs,
    lb = round(lb_p(mod_orden_bien), 4),
    theta = round(as.numeric(mod_orden_bien$coef["ma1"]), 4),
    Theta = round(as.numeric(mod_orden_bien$coef["sma1"]), 4)),
  auto_arima = as.character(auto_ua), auto_aicc = round(auto_ua$aicc, 3),
  nsdiffs_ocsb = nsdiffs(ua, test = "ocsb"),
  aicc_no_comparables = paste("Los dos modelos tienen d distinto (0 y 1), asi que sus",
                              "AICc TAMPOCO se comparan: 60 observaciones frente a 59.",
                              "Lo que decide es el diagnostico, que si es valido en ambos."),
  leccion = paste("Los operadores conmutan (la serie resultante es identica), pero las",
                  "PRUEBAS no: ndiffs sobre la serie cruda ve 0 diferencias regulares",
                  "porque la estacionalidad domina la varianza. Se decide D primero.")
)
s2 <- sol$cap5_ej2
cat(sprintf("  Orden equivocado: ndiffs(crudo) = %d -> nsdiffs despues = %d -> %s\n",
            s2$orden_mal$ndiffs_primero, s2$orden_mal$nsdiffs_despues, s2$modelo_orden_mal$etiqueta))
cat(sprintf("  Orden correcto : nsdiffs(crudo) = %d -> ndiffs despues = %d -> %s\n",
            s2$orden_bien$nsdiffs_primero, s2$orden_bien$ndiffs_despues, s2$modelo_orden_bien$etiqueta))
cat(sprintf("  Los operadores conmutan: diferencia maxima %.3g\n", s2$conmutan))
cat(sprintf("  Lo que decide es el DIAGNOSTICO: Ljung-Box(24) p = %.4f (orden equivocado) y %.4f (correcto)\n",
            s2$modelo_orden_mal$lb, s2$modelo_orden_bien$lb))
cat(sprintf("  (sus AICc, %.3f con n=%d y %.3f con n=%d, NO son comparables: distinto d)\n",
            s2$modelo_orden_mal$aicc, s2$modelo_orden_mal$nobs,
            s2$modelo_orden_bien$aicc, s2$modelo_orden_bien$nobs))
cat(sprintf("  auto.arima confirma: %s (AICc %.3f) | theta = %.4f, Theta = %.4f\n",
            s2$auto_arima, s2$auto_aicc, s2$modelo_orden_bien$theta, s2$modelo_orden_bien$Theta))
cat(sprintf("  Aviso: nsdiffs(test='ocsb') devuelve %d, no %d. La prueba por defecto cambio de version.\n",
            s2$nsdiffs_ocsb, s2$orden_bien$nsdiffs_primero))

# ---- Ej. 3: la TRM no es estacional; y armonicos frente a SARIMA -----------
# Dos preguntas de una: (a) tres evidencias independientes de que la TRM no
# tiene estacionalidad; (b) sobre co2, comparar regresion armonica y SARIMA
# -- y descubrir que el AICc NO sirve para esa comparacion.
cat("\n=== CAP5 · Ej.3 · La TRM sin estacionalidad, y armonicos vs. SARIMA ===\n")
series_json <- fromJSON(file.path(dir_salidas, "datos_series.json"), simplifyVector = TRUE)
trm5 <- ts(series_json$trm$valores, start = series_json$trm$inicio, frequency = 12)
trm5_d <- diff(trm5)
acf_trm <- as.numeric(acf(trm5_d, lag.max = 36, plot = FALSE)$acf)[-1]
b_trm <- banda(length(trm5_d))
forzado <- Arima(trm5, order = c(0, 1, 0), seasonal = list(order = c(1, 0, 0), period = 12))
simple <- Arima(trm5, order = c(0, 1, 0))

# (b) armonicos sobre co2, dentro de su familia y contra el SARIMA
arm_co2 <- lapply(1:6, function(K) {
  xr <- fourier(co2v, K = K)
  f <- auto.arima(co2v, xreg = xr, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
  list(K = K, terminos = ncol(xr), aicc = round(f$aicc, 3), nobs = f$nobs,
       modelo = as.character(f), lb = round(lb_p(f), 4))
})
mejorK_co2 <- arm_co2[[which.min(vapply(arm_co2, function(a) a$aicc, numeric(1)))]]

sol$cap5_ej3 <- list(
  trm = list(
    n = length(trm5),
    evidencia1_nsdiffs = nsdiffs(trm5),
    evidencia2_acf = list(r12 = round(acf_trm[12], 4), r24 = round(acf_trm[24], 4),
                          r36 = round(acf_trm[36], 4), banda = round(b_trm, 4),
                          fuera = sum(abs(acf_trm[c(12, 24, 36)]) > b_trm)),
    evidencia3_ajuste = list(
      Phi = round(as.numeric(forzado$coef["sar1"]), 4),
      ee = round(as.numeric(sqrt(diag(forzado$var.coef))["sar1"]), 4),
      t = round(as.numeric(forzado$coef["sar1"] / sqrt(diag(forzado$var.coef))["sar1"]), 3),
      aicc_forzado = round(forzado$aicc, 3), aicc_simple = round(simple$aicc, 3)),
    auto = as.character(auto.arima(trm5, stepwise = FALSE, approximation = FALSE))
  ),
  co2_armonicos = list(
    resultados = arm_co2,
    mejor_K = mejorK_co2$K, aicc_mejor_K = mejorK_co2$aicc, nobs_armonico = mejorK_co2$nobs,
    aicc_airline = round(airline_co2$aicc, 3), nobs_airline = airline_co2$nobs,
    comparable = FALSE,
    leccion = paste("El AICc del armonico parece mucho mejor que el del SARIMA, pero el",
                    "armonico usa D = 0 y el SARIMA D = 1: se evaluan sobre series de",
                    "distinta longitud. La comparacion entre familias solo vale fuera de",
                    "muestra. Es la misma trampa del capitulo 4 con d, ahora con D.")
  )
)
s3 <- sol$cap5_ej3
cat(sprintf("  (a) TRM, n = %d\n", s3$trm$n))
cat(sprintf("      1. nsdiffs = %d\n", s3$trm$evidencia1_nsdiffs))
cat(sprintf("      2. ACF de la diferencia en 12/24/36 = %.4f / %.4f / %.4f (banda %.4f): %d fuera\n",
            s3$trm$evidencia2_acf$r12, s3$trm$evidencia2_acf$r24, s3$trm$evidencia2_acf$r36,
            s3$trm$evidencia2_acf$banda, s3$trm$evidencia2_acf$fuera))
cat(sprintf("      3. Al forzar un SAR(1): Phi = %.4f (e.e. %.4f, t = %.2f), AICc %.3f vs %.3f del simple\n",
            s3$trm$evidencia3_ajuste$Phi, s3$trm$evidencia3_ajuste$ee, s3$trm$evidencia3_ajuste$t,
            s3$trm$evidencia3_ajuste$aicc_forzado, s3$trm$evidencia3_ajuste$aicc_simple))
cat(sprintf("      auto.arima: %s\n", s3$trm$auto))
cat("  (b) co2, armonicos frente al SARIMA:\n")
for (a in s3$co2_armonicos$resultados)
  cat(sprintf("      K=%d (%2d terminos) AICc %9.3f  n=%d  %s  LB p=%.4f\n",
              a$K, a$terminos, a$aicc, a$nobs, a$modelo, a$lb))
cat(sprintf("      Mejor armonico K=%d con AICc %.3f (n=%d) frente al airline %.3f (n=%d)\n",
            s3$co2_armonicos$mejor_K, s3$co2_armonicos$aicc_mejor_K, s3$co2_armonicos$nobs_armonico,
            s3$co2_armonicos$aicc_airline, s3$co2_armonicos$nobs_airline))
cat("      -> NO son comparables: distinto D, distinto n efectivo.\n")

# ============================================================================

# ============================================================================
# CAPÍTULO 6 — Pronóstico, métricas y backtesting
#
# Los tres ejercicios evalúan, que es lo que le toca a este capítulo: ninguno
# vuelve a construir un intervalo (Capítulo 4) ni a comparar métodos sobre una
# sola partición (Capítulo 5).
# ============================================================================

escala_mase_ <- function(entrena, m = 1) {
  x <- as.numeric(entrena)
  if (m > 1 && length(x) > m) mean(abs(diff(x, lag = m))) else mean(abs(diff(x)))
}
winkler_ <- function(y, li, ls, nivel) {
  a <- 1 - nivel / 100
  (ls - li) + (2 / a) * ((li - y) * (y < li) + (y - ls) * (y > ls))
}
om_ <- function(y, ajusta, T0, h, niveles = c(80, 95)) {
  origenes <- T0:(length(y) - h)
  P <- LI <- LS <- R <- matrix(NA_real_, length(origenes), h)
  for (i in seq_along(origenes)) {
    Tt <- origenes[i]
    fc <- try(ajusta(subset(y, start = 1, end = Tt), h), silent = TRUE)
    if (inherits(fc, "try-error")) next
    P[i, ] <- as.numeric(fc$mean)
    LI[i, ] <- as.numeric(fc$lower[, 2]); LS[i, ] <- as.numeric(fc$upper[, 2])
    R[i, ] <- as.numeric(y)[(Tt + 1):(Tt + h)]
  }
  list(origenes = origenes, pron = P, reales = R, li = LI, ls = LS, error = R - P)
}
resumen_ <- function(om, entrena, m) {
  e <- as.numeric(om$error); r <- as.numeric(om$reales); ok <- !is.na(e)
  list(n_origenes = length(om$origenes), n_errores = sum(ok),
       rmse = round(sqrt(mean(e[ok]^2)), 4), mae = round(mean(abs(e[ok])), 4),
       mape = round(100 * mean(abs(e[ok] / r[ok])), 4),
       mase = round(mean(abs(e[ok])) / escala_mase_(entrena, m), 4),
       cob95 = round(100 * mean(r[ok] >= om$li[ok] & r[ok] <= om$ls[ok]), 4),
       winkler95 = round(mean(winkler_(r[ok], om$li[ok], om$ls[ok], 95)), 4))
}

# --- Ejercicio 1: ¿le gana el modelo al naive estacional en USAccDeaths? ----
uad <- ts(sd_json$usaccdeaths$valores, start = sd_json$usaccdeaths$inicio, frequency = 12)
T0_U <- 36; H_U <- 12
metodos_u <- list(
  snaive  = function(tr, h) snaive(tr, h = h, level = c(80, 95)),
  airline = function(tr, h) forecast(Arima(tr, order = c(0, 1, 1),
                                           seasonal = c(0, 1, 1)), h = h, level = c(80, 95)),
  auto    = function(tr, h) forecast(auto.arima(tr), h = h, level = c(80, 95)),
  media   = function(tr, h) meanf(tr, h = h, level = c(80, 95))
)
oms_u <- lapply(metodos_u, function(f) om_(uad, f, T0_U, H_U))
tabla_u <- lapply(names(oms_u), function(nm)
  c(list(metodo = nm), resumen_(oms_u[[nm]], subset(uad, start = 1, end = T0_U), 12)))
dm_u <- lapply(c(1, 6, 12), function(h) {
  a <- oms_u$airline$error[, h]; b <- oms_u$snaive$error[, h]
  ok <- !is.na(a) & !is.na(b)
  p <- try(dm.test(a[ok], b[ok], alternative = "two.sided", h = h, power = 2), silent = TRUE)
  if (inherits(p, "try-error")) return(NULL)
  list(h = h, estadistico = round(as.numeric(p$statistic), 4), p = round(p$p.value, 4))
})
# Y la partición única, para contrastar con el origen móvil
tr_u <- subset(uad, start = 1, end = length(uad) - 12)
te_u <- as.numeric(uad)[(length(uad) - 11):length(uad)]
part_u <- lapply(names(metodos_u), function(nm) {
  fc <- metodos_u[[nm]](tr_u, 12)
  e <- te_u - as.numeric(fc$mean)
  list(metodo = nm, rmse = round(sqrt(mean(e^2)), 4), mae = round(mean(abs(e)), 4),
       mase = round(mean(abs(e)) / escala_mase_(tr_u, 12), 4))
})
sol$cap6_ej1 <- list(
  serie = "USAccDeaths", n = length(uad), T0 = T0_U, h = H_U,
  n_origenes = length(oms_u$snaive$origenes),
  origen_movil = tabla_u, dm_airline_vs_snaive = Filter(Negate(is.null), dm_u),
  particion_unica = part_u,
  orden_om = sapply(tabla_u, function(z) z$metodo)[order(sapply(tabla_u, function(z) z$rmse))],
  orden_particion = sapply(part_u, function(z) z$metodo)[order(sapply(part_u, function(z) z$rmse))]
)

# --- Ejercicio 2: el MAPE engañosamente bueno de co2 -----------------------
co2s <- ts(sd_json$co2$valores, start = sd_json$co2$inicio, frequency = 12)
n_c <- length(co2s); h_c <- 24
tr_c <- subset(co2s, start = 1, end = n_c - h_c)
te_c <- as.numeric(co2s)[(n_c - h_c + 1):n_c]
met_c <- function(real, pron, entrena, m) {
  e <- real - pron
  list(rmse = round(sqrt(mean(e^2)), 4), mae = round(mean(abs(e)), 4),
       mape = round(100 * mean(abs(e / real)), 4),
       mase = round(mean(abs(e)) / escala_mase_(entrena, m), 4))
}
cands_c <- list(
  media   = as.numeric(meanf(tr_c, h = h_c)$mean),
  naive   = as.numeric(naive(tr_c, h = h_c)$mean),
  snaive  = as.numeric(snaive(tr_c, h = h_c)$mean),
  deriva  = as.numeric(rwf(tr_c, h = h_c, drift = TRUE)$mean),
  airline = as.numeric(forecast(Arima(tr_c, order = c(0, 1, 1),
                                      seasonal = c(0, 1, 1)), h = h_c)$mean)
)
tabla_c <- lapply(names(cands_c), function(nm)
  c(list(metodo = nm), met_c(te_c, cands_c[[nm]], tr_c, 12)))
sol$cap6_ej2 <- list(
  serie = "co2 (Mauna Loa)", n = n_c, h = h_c,
  rango = round(range(as.numeric(co2s)), 2),
  variacion_relativa_pct = round(100 * (max(as.numeric(co2s)) / min(as.numeric(co2s)) - 1), 2),
  q_mase = round(escala_mase_(tr_c, 12), 4),
  tabla = tabla_c,
  mape_maximo = round(max(sapply(tabla_c, function(z) z$mape)), 4),
  mase_maximo = round(max(sapply(tabla_c, function(z) z$mase)), 4),
  razon_mape = round(max(sapply(tabla_c, function(z) z$mape)) /
                     min(sapply(tabla_c, function(z) z$mape)), 2),
  razon_mase = round(max(sapply(tabla_c, function(z) z$mase)) /
                     min(sapply(tabla_c, function(z) z$mase)), 2)
)

# --- Ejercicio 3: ¿cubre el intervalo del Nilo lo que promete? -------------
nilo <- ts(sd_json$nilo$valores, start = sd_json$nilo$inicio, frequency = 1)
T0_N <- 60; H_N <- 5
cob_niveles <- function(y, ajusta, T0, h, niveles) {
  origenes <- T0:(length(y) - h)
  sapply(niveles, function(nv) {
    dentro <- c()
    for (Tt in origenes) {
      fc <- ajusta(subset(y, start = 1, end = Tt), h, nv)
      real <- as.numeric(y)[(Tt + 1):(Tt + h)]
      dentro <- c(dentro, real >= fc$lower[, 1] & real <= fc$upper[, 1])
    }
    round(100 * mean(dentro), 4)
  })
}
NIV <- c(50, 80, 90, 95, 99)
cob_arima <- cob_niveles(nilo, function(tr, h, nv)
  forecast(Arima(tr, order = c(1, 1, 1)), h = h, level = nv), T0_N, H_N, NIV)
cob_naive <- cob_niveles(nilo, function(tr, h, nv)
  naive(tr, h = h, level = nv), T0_N, H_N, NIV)
om_a <- om_(nilo, function(tr, h) forecast(Arima(tr, order = c(1, 1, 1)), h = h,
                                           level = c(80, 95)), T0_N, H_N)
om_n <- om_(nilo, function(tr, h) naive(tr, h = h, level = c(80, 95)), T0_N, H_N)
sol$cap6_ej3 <- list(
  serie = "Nile", n = length(nilo), T0 = T0_N, h = H_N,
  n_origenes = length(om_a$origenes),
  niveles = NIV, cobertura_arima = cob_arima, cobertura_naive = cob_naive,
  exceso_arima = round(cob_arima - NIV, 4), exceso_naive = round(cob_naive - NIV, 4),
  arima = resumen_(om_a, subset(nilo, start = 1, end = T0_N), 1),
  naive = resumen_(om_n, subset(nilo, start = 1, end = T0_N), 1),
  ancho95_arima = round(mean(om_a$ls - om_a$li, na.rm = TRUE), 4),
  ancho95_naive = round(mean(om_n$ls - om_n$li, na.rm = TRUE), 4),
  shapiro_p = round(shapiro.test(residuals(Arima(nilo, order = c(1, 1, 1))))$p.value, 4)
)

cat("\n=== CAPÍTULO 6 ===\n")
cat("  Ej. 1 USAccDeaths, origen móvil (", sol$cap6_ej1$n_origenes, "orígenes, h = 12):\n")
for (z in tabla_u) cat(sprintf("      %-8s RMSE %8.2f  MASE %6.3f  cob95 %6.2f  W95 %9.2f\n",
                               z$metodo, z$rmse, z$mase, z$cob95, z$winkler95))
cat("      partición única:", paste(sol$cap6_ej1$orden_particion, collapse = " > "), "\n")
cat("      origen móvil   :", paste(sol$cap6_ej1$orden_om, collapse = " > "), "\n")
for (z in sol$cap6_ej1$dm_airline_vs_snaive)
  cat(sprintf("      DM airline vs snaive h=%2d: %8.4f  p = %.4f\n", z$h, z$estadistico, z$p))
cat("  Ej. 2 co2 (variación relativa", sol$cap6_ej2$variacion_relativa_pct, "%):\n")
for (z in tabla_c) cat(sprintf("      %-8s RMSE %7.4f  MAE %7.4f  MAPE %7.4f  MASE %7.4f\n",
                               z$metodo, z$rmse, z$mae, z$mape, z$mase))
cat(sprintf("      razón peor/mejor: MAPE %.2f  frente a MASE %.2f\n",
            sol$cap6_ej2$razon_mape, sol$cap6_ej2$razon_mase))
cat("  Ej. 3 Nilo, cobertura empírica por nivel nominal:\n")
cat("      nivel   :", paste(sprintf("%6d", NIV), collapse = ""), "\n")
cat("      ARIMA   :", paste(sprintf("%6.1f", cob_arima), collapse = ""), "\n")
cat("      naive   :", paste(sprintf("%6.1f", cob_naive), collapse = ""), "\n")
cat(sprintf("      ancho medio 95%%: ARIMA %.1f  naive %.1f | Shapiro p = %.4f\n",
            sol$cap6_ej3$ancho95_arima, sol$cap6_ej3$ancho95_naive, sol$cap6_ej3$shapiro_p))

sol$metadatos <- list(generado = fecha_corte, generador = "precalculo/genera_soluciones.R",
                      versiones = list(R = paste(R.version$major, R.version$minor, sep = "."),
                                       tseries = as.character(packageVersion("tseries")),
                                       forecast = as.character(packageVersion("forecast"))))
write_json(sol, file.path(dir_salidas, "soluciones_ejercicios.json"),
           auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null")
cat("\nEscrito: salidas/soluciones_ejercicios.json\nListo.\n")
