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
sol$metadatos <- list(generado = fecha_corte, generador = "precalculo/genera_soluciones.R",
                      versiones = list(R = paste(R.version$major, R.version$minor, sep = "."),
                                       tseries = as.character(packageVersion("tseries")),
                                       forecast = as.character(packageVersion("forecast"))))
write_json(sol, file.path(dir_salidas, "soluciones_ejercicios.json"),
           auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null")
cat("\nEscrito: salidas/soluciones_ejercicios.json\nListo.\n")
