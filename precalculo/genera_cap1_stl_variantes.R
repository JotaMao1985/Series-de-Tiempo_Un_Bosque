# ============================================================================
# genera_cap1_stl_variantes.R — Datos del capítulo 1 que no están en DATOS_CAP1
#
# Genera, en la carpeta salidas/:
#   cap1_stl_variantes.json / cap1_stl_variantes.js  (const DATOS_CAP1_STL)
#
# Contenido:
#   1. stl      : las ocho variantes de STL sobre log(AirPassengers) que enseña
#                 el simulador del Módulo 7. Tres interruptores:
#                   ventana estacional  "periodic" (per) | s.window = 11 (s11)
#                   julio de 1955       original (orig)  | inflado un 50 % (atip)
#                   robust              FALSE (norob)    | TRUE (rob)
#                 La variante per_orig_norob es la de DATOS_CAP1.stl_log; el
#                 guion se detiene si no coincide con stl() tal como allí se usa.
#                 Cada variante lleva dos resúmenes: `resumen`, a 4 decimales,
#                 para comprobar; y `lectura`, con las cifras que el simulador
#                 escribe en pantalla, cada una redondeada UNA sola vez desde
#                 el valor completo y con los decimales con que se muestra. El
#                 simulador solo lee de `lectura`: una cifra de pantalla nunca
#                 sale de redondear un dato que ya venía redondeado.
#   2. clasica  : la descomposición clásica ADITIVA (Módulo 6) y, para ponerla
#                 al lado en las mismas unidades, la multiplicativa traducida a
#                 miles de pasajeros: T*(S - 1) y y - T*S.
#   3. desestacionalizada : y / exp(S) con el componente estacional de la STL
#                 del capítulo (Módulo 8), y su distancia a la del índice clásico.
#   4. fuerzas  : F_T y F_S de varias series de R, como referencia (Módulo 8).
#
# Dependencias: SOLO R base (ni jsonlite). No descarga nada y no toca
# DATOS_CAP1 ni genera_datos.R.
# Uso:  Rscript precalculo/genera_cap1_stl_variantes.R
# ============================================================================

args_dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
if (is.na(args_dir) || args_dir == "") args_dir <- "."
dir_salidas <- file.path(args_dir, "salidas")
dir.create(dir_salidas, showWarnings = FALSE, recursive = TRUE)

# ---------------------------------------------------------------------------
# JSON con R base. Listas con nombre -> objeto; sin nombre -> arreglo;
# vectores de longitud > 1 -> arreglo; NA -> null. Las cadenas van en ASCII.
# ---------------------------------------------------------------------------
num_json <- function(v) {
  if (is.na(v)) return("null")
  if (v == 0) return("0")                       # evita "-0"
  format(v, digits = 15, scientific = FALSE, trim = TRUE)
}
a_json <- function(x) {
  if (is.null(x)) return("null")
  if (is.list(x)) {
    partes <- vapply(x, a_json, character(1))
    if (!is.null(names(x))) return(paste0("{", paste0('"', names(x), '":', partes, collapse = ","), "}"))
    return(paste0("[", paste(partes, collapse = ","), "]"))
  }
  s <- if (is.character(x)) {
    paste0('"', gsub('"', '\\\\"', gsub("\\\\", "\\\\\\\\", x)), '"')
  } else if (is.logical(x)) {
    ifelse(is.na(x), "null", ifelse(x, "true", "false"))
  } else {
    vapply(as.numeric(x), num_json, character(1))
  }
  if (length(x) == 1) s else paste0("[", paste(s, collapse = ","), "]")
}

# ---------------------------------------------------------------------------
# Series
# ---------------------------------------------------------------------------
y    <- AirPassengers
n    <- length(y)
anio <- floor(time(y) + 1e-6)
mes  <- cycle(y)
POS  <- 79                                      # julio de 1955
stopifnot(anio[POS] == 1955, mes[POS] == 7, y[POS] == 364)

y_atip <- y
y_atip[POS] <- y_atip[POS] * 1.5                # 364 -> 546, el atipico del capitulo
stopifnot(y_atip[POS] == 546)

julios <- which(mes == 7)
tramos <- list(`1949-1953` = 1949:1953, `1954-1957` = 1954:1957, `1958-1960` = 1958:1960)
sd_anual <- function(r) as.numeric(tapply(as.numeric(r), anio, sd, na.rm = TRUE))

# ---------------------------------------------------------------------------
# 1. Las ocho variantes de STL
# ---------------------------------------------------------------------------
variante <- function(ventana, atipico, robusto) {
  x  <- log(if (atipico) y_atip else y)
  sw <- if (ventana == "per") "periodic" else 11
  s  <- stl(x, s.window = sw, robust = robusto)
  ts <- s$time.series
  S <- as.numeric(ts[, "seasonal"]); Tt <- as.numeric(ts[, "trend"]); R <- as.numeric(ts[, "remainder"])
  sdA <- sd_anual(R)
  sd_tramos <- vapply(tramos, function(a) mean(sdA[sort(unique(anio)) %in% a]), numeric(1))   # sin redondear
  list(
    llamada = sprintf("stl(log(%s), s.window = %s%s)",
                      if (atipico) "serie con julio de 1955 x 1.5" else "AirPassengers",
                      if (ventana == "per") "'periodic'" else "11",
                      if (robusto) ", robust = TRUE" else ""),
    ventanas = as.integer(s$win), pasadas_interiores = as.integer(s$inner), vueltas_exteriores = as.integer(s$outer),
    tendencia  = round(Tt, 4),
    estacional = round(S, 4),
    residuo    = round(R, 4),
    resumen = list(
      julio_pct             = round(100 * (exp(S[julios[c(1, 7, 12)]]) - 1), 1),   # 1949, 1955, 1960
      indice_julio_1955     = round(exp(S[POS]), 4),
      recorrido_julio_log   = round(diff(range(S[julios])), 4),
      tendencia_jul55_miles = round(exp(Tt[POS]), 1),
      residuo_jul55         = round(R[POS], 4),
      sd_residuo_tramos     = round(sd_tramos, 4),
      sd_residuo_anual      = round(sdA, 4),
      sd_residuo            = round(sd(R), 4),
      n_peso_cero           = sum(s$weights < 1e-8),
      n_peso_menor_05       = sum(s$weights < 0.5),
      peso_jul55            = round(s$weights[POS], 4)
    ),
    # Lo que el simulador escribe (lectura y aria-label). Los decimales de aqui
    # son los de pantalla: si cambian en un sitio, cambian en el otro.
    lectura = list(
      julio_pct             = round(100 * (exp(S[julios[c(1, 7, 12)]]) - 1), 1),   # 1949, 1955, 1960 · 1 decimal
      tendencia_jul55_miles = round(exp(Tt[POS]), 1),                               # 1 decimal
      residuo_jul55         = round(R[POS], 4),                                     # 4 decimales
      sd_residuo_tramos     = round(sd_tramos, 3),                                  # 3 decimales
      n_peso_cero           = sum(s$weights < 1e-8),
      jul55_peso_cero       = s$weights[POS] < 1e-8
    )
  )
}

stl_var <- list()
for (ventana in c("per", "s11")) for (atipico in c(FALSE, TRUE)) for (robusto in c(FALSE, TRUE)) {
  clave <- paste(ventana, if (atipico) "atip" else "orig", if (robusto) "rob" else "norob", sep = "_")
  stl_var[[clave]] <- variante(ventana, atipico, robusto)
}
# La variante de partida tiene que ser la figura que ya publica el capitulo
base <- stl(log(AirPassengers), s.window = "periodic")$time.series
stopifnot(identical(stl_var$per_orig_norob$estacional, round(as.numeric(base[, "seasonal"]), 4)),
          identical(stl_var$per_orig_norob$tendencia,  round(as.numeric(base[, "trend"]), 4)),
          identical(stl_var$per_orig_norob$residuo,    round(as.numeric(base[, "remainder"]), 4)))

# ---------------------------------------------------------------------------
# 2. Clasica aditiva, y la multiplicativa traducida a miles de pasajeros
# ---------------------------------------------------------------------------
da <- decompose(y, type = "additive")
dm <- decompose(y, type = "multiplicative")
stopifnot(isTRUE(all.equal(as.numeric(da$trend), as.numeric(dm$trend))))   # el paso 2 no depende de la escala

mult_est_miles <- dm$trend * (dm$seasonal - 1)          # lo que la estacionalidad anade o quita
mult_res_miles <- y - dm$trend * dm$seasonal            # lo que queda sin explicar
stopifnot(max(abs(y - dm$trend - mult_est_miles - mult_res_miles), na.rm = TRUE) < 1e-9)

clasica <- list(
  aditiva = list(
    indices          = round(as.numeric(da$figure), 2),
    estacional       = round(as.numeric(da$seasonal), 2),
    residuo          = round(as.numeric(da$random), 2),
    sd_residuo_anual = round(sd_anual(da$random), 1),
    sd_residuo       = round(sd(da$random, na.rm = TRUE), 1)
  ),
  multiplicativa_en_miles = list(
    estacional       = round(as.numeric(mult_est_miles), 2),
    residuo          = round(as.numeric(mult_res_miles), 2),
    sd_residuo_anual = round(sd_anual(mult_res_miles), 1),
    sd_residuo       = round(sd(mult_res_miles, na.rm = TRUE), 1)
  )
)

# ---------------------------------------------------------------------------
# 3. Serie desestacionalizada con la STL del capitulo: y / exp(S)
# ---------------------------------------------------------------------------
aj_stl <- y / exp(base[, "seasonal"])
aj_cla <- y / dm$seasonal
stopifnot(max(abs(aj_stl - exp(base[, "trend"] + base[, "remainder"]))) < 1e-9)
i_max <- which.max(abs(aj_stl - aj_cla))
desest <- list(
  stl     = round(as.numeric(aj_stl), 1),
  clasica = round(as.numeric(aj_cla), 1),
  jul55   = list(stl = round(aj_stl[POS], 1), clasica = round(aj_cla[POS], 1)),
  max_diferencia = list(miles = round(abs(aj_stl - aj_cla)[i_max], 1),
                        pct   = round(100 * abs(aj_stl / aj_cla - 1)[i_max], 1),
                        fecha = sprintf("%d-%02d", anio[i_max], mes[i_max]))
)

# ---------------------------------------------------------------------------
# 4. Fuerzas de referencia (STL con s.window = "periodic", como en el capitulo)
# ---------------------------------------------------------------------------
fuerzas <- function(x, ...) {
  st <- stl(x, ...)$time.series
  R <- st[, "remainder"]
  c(FT = max(0, 1 - var(R) / var(st[, "trend"] + R)),
    FS = max(0, 1 - var(R) / var(st[, "seasonal"] + R)))
}
fila <- function(nombre, x) {
  f <- fuerzas(x, s.window = "periodic")
  list(serie = nombre, n = length(x), frecuencia = frequency(x), FT = round(f[["FT"]], 4), FS = round(f[["FS"]], 4))
}
# Ruido puro: 200 series de 144 normales independientes, mensuales
set.seed(20948)
sim <- t(replicate(200, fuerzas(ts(rnorm(144), frequency = 12), s.window = "periodic")))
f11 <- fuerzas(log(AirPassengers), s.window = 11)
ref_fuerzas <- list(
  series = list(
    fila("log(AirPassengers)", log(AirPassengers)),
    fila("co2", co2),
    fila("nottem", nottem),
    fila("USAccDeaths", USAccDeaths),
    fila("sunspots", sunspots)
  ),
  airpassengers_s11 = list(FT = round(f11[["FT"]], 4), FS = round(f11[["FS"]], 4)),
  ruido = list(simulaciones = 200, n = 144, semilla = 20948,
               FT = round(as.numeric(quantile(sim[, "FT"], c(0.05, 0.5, 0.95))), 3),
               FS = round(as.numeric(quantile(sim[, "FS"], c(0.05, 0.5, 0.95))), 3),
               cuantiles = c(0.05, 0.5, 0.95))
)

# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------
fecha <- format(Sys.Date(), "%Y-%m-%d")
datos <- list(
  serie = "airpassengers",
  descripcion = paste0(
    "Variantes de stats::stl sobre log(AirPassengers) para el simulador del Modulo 7 ",
    "(ventana estacional periodic o 11; julio de 1955 original o multiplicado por 1.5; robust FALSE o TRUE), ",
    "descomposicion clasica aditiva y multiplicativa traducida a miles de pasajeros (Modulo 6), ",
    "serie desestacionalizada y / exp(S) con la STL del capitulo y fuerzas de referencia (Modulo 8). ",
    "Componentes de STL en escala log, a 4 decimales; NA como null. ",
    "En cada variante, 'lectura' trae las cifras de pantalla redondeadas una sola vez desde el valor completo."),
  n = n,
  atipico = list(posicion = POS, fecha = "1955-07", factor = 1.5, original = as.numeric(y[POS]),
                 inflado = as.numeric(y_atip[POS]), log_factor = round(log(1.5), 4)),
  tramos = names(tramos),
  stl = stl_var,
  clasica = clasica,
  desestacionalizada = desest,
  fuerzas = ref_fuerzas,
  metadatos = list(generado = fecha, generador = "precalculo/genera_cap1_stl_variantes.R",
                   R = paste(R.version$major, R.version$minor, sep = "."))
)

json <- a_json(datos)
writeLines(json, file.path(dir_salidas, "cap1_stl_variantes.json"))
writeLines(c(
  paste0("// Generado por precalculo/genera_cap1_stl_variantes.R el ", fecha),
  "// Variantes de STL (Modulo 7), clasica aditiva (Modulo 6), desestacionalizada y fuerzas (Modulo 8).",
  paste0("const DATOS_CAP1_STL = ", json, ";")
), file.path(dir_salidas, "cap1_stl_variantes.js"))

cat("Escrito: salidas/cap1_stl_variantes.json / .js (", nchar(json), "caracteres )\n")
cat("\nResumen de las ocho variantes:\n")
tab <- t(sapply(stl_var, function(v) with(v$resumen, c(
  jul49 = julio_pct[1], jul55 = julio_pct[2], jul60 = julio_pct[3], idx55 = indice_julio_1955,
  T55 = tendencia_jul55_miles, R55 = residuo_jul55,
  sd1 = sd_residuo_tramos[[1]], sd2 = sd_residuo_tramos[[2]], sd3 = sd_residuo_tramos[[3]],
  peso0 = n_peso_cero, `peso<.5` = n_peso_menor_05, w55 = peso_jul55))))
print(tab)
cat("\nCifras de pantalla (campo 'lectura'), junto al valor completo de la sd por tramos:\n")
for (ventana in c("per", "s11")) for (atipico in c(FALSE, TRUE)) for (robusto in c(FALSE, TRUE)) {
  clave <- paste(ventana, if (atipico) "atip" else "orig", if (robusto) "rob" else "norob", sep = "_")
  s  <- stl(log(if (atipico) y_atip else y), s.window = if (ventana == "per") "periodic" else 11, robust = robusto)
  sdA <- sd_anual(s$time.series[, "remainder"])
  completo <- vapply(tramos, function(a) mean(sdA[sort(unique(anio)) %in% a]), numeric(1))
  l <- stl_var[[clave]]$lectura
  cat(sprintf("  %-15s julio %s | T55 %.1f | R55 %.4f | sd %s (completo %s) | peso 0: %d, jul55 %s\n", clave,
              paste(sprintf("%+.1f", l$julio_pct), collapse = " "), l$tendencia_jul55_miles, l$residuo_jul55,
              paste(sprintf("%.3f", l$sd_residuo_tramos), collapse = " "),
              paste(sprintf("%.6f", completo), collapse = " "), l$n_peso_cero, l$jul55_peso_cero))
}
cat("\nVentanas (s, t, l) y pasadas (interiores, exteriores):\n")
print(t(sapply(stl_var, function(v) c(v$ventanas, v$pasadas_interiores, v$vueltas_exteriores))))
cat("\nClasica: sd anual del residuo, en miles\n  aditiva        :", clasica$aditiva$sd_residuo_anual,
    "\n  multiplicativa :", clasica$multiplicativa_en_miles$sd_residuo_anual, "\n")
cat("  sd global: aditiva", clasica$aditiva$sd_residuo, " multiplicativa", clasica$multiplicativa_en_miles$sd_residuo, "\n")
cat("\nDesestacionalizada: julio de 1955, STL", desest$jul55$stl, " clasica", desest$jul55$clasica,
    "; diferencia maxima", desest$max_diferencia$miles, "mil (", desest$max_diferencia$pct, "% ) en", desest$max_diferencia$fecha, "\n")
cat("\nFuerzas (periodic):\n")
for (f in ref_fuerzas$series) cat(sprintf("  %-20s n = %4d  FT = %.4f  FS = %.4f\n", f$serie, f$n, f$FT, f$FS))
cat("  log(AirPassengers), s.window = 11: FT =", ref_fuerzas$airpassengers_s11$FT, " FS =", ref_fuerzas$airpassengers_s11$FS, "\n")
cat("  ruido puro (200 x 144 normales): FT 5 %, mediana, 95 % =", ref_fuerzas$ruido$FT, " | FS =", ref_fuerzas$ruido$FS, "\n")
