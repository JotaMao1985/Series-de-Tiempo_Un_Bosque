# ============================================================================
# genera_preparcial.R — Precalculos del Preparcial del Corte I (Modulo I)
#
# Genera salidas/preparcial_datos.json y salidas/preparcial_datos.js con las
# series propias del preparcial y TODAS las cifras de sus 32 items.
#
# Por que series propias y no AirPassengers (D14 del plan): de los 56 items que
# ya se le han hecho al estudiante sobre el Modulo I, la mitad corren sobre
# AirPassengers, y es ademas la serie que cualquier modelo de lenguaje conoce de
# memoria. Sobre ella, reconocer sustituye a razonar y el diagnostico miente.
#
# El preparcial NO tiene nota, asi que aqui no hay clave oculta ni reparto por
# documento: un unico instrumento para los nueve. Lo que si se mantiene es que
# ninguna cifra de la pantalla se escriba a mano (Criterio de contenido).
#
# Dependencias: jsonlite, tseries, forecast, urca.
# Uso:  LC_ALL=en_US.UTF-8 Rscript genera_preparcial.R   (desde precalculo/)
# ============================================================================

suppressMessages({
  library(jsonlite)
  library(tseries)
  library(forecast)
  library(urca)
})

# Misma trampa de configuracion regional que genera_cap2.R: sin UTF-8, jsonlite
# escribe las tildes como bytes sueltos y el navegador se come la letra.
suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"))
if (!isTRUE(l10n_info()$"UTF-8")) {
  warning("Sin configuracion regional UTF-8: las tildes del JSON saldran mal. ",
          "Ejecuta con LC_ALL=en_US.UTF-8 Rscript ...")
}

args_dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
if (is.na(args_dir) || args_dir == "") args_dir <- "."
dir_salidas <- file.path(args_dir, "salidas")
stopifnot(dir.exists(dir_salidas))

# La semilla es la fecha del parcial. No tiene magia: la fija este guion y no se
# vuelve a tocar, porque cambiarla cambia todas las cifras del instrumento.
SEMILLA <- 20260901
MAX_REZAGO <- 36

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

r3 <- function(x, k = 4) if (is.null(x)) NULL else round(as.numeric(x), k)

acf_de <- function(x, lag.max = MAX_REZAGO) {
  a <- acf(x, lag.max = lag.max, plot = FALSE)
  p <- pacf(x, lag.max = lag.max, plot = FALSE)
  n <- length(x)
  list(rezagos = seq_len(lag.max),
       acf = r3(as.numeric(a$acf)[-1]),
       pacf = r3(as.numeric(p$acf)),
       banda = r3(1.96 / sqrt(n)),
       n = n)
}

adf_de <- function(x) {
  r <- suppressWarnings(adf.test(x))
  list(estadistico = r3(r$statistic), p_valor = r3(r$p.value),
       rezagos = as.integer(r$parameter),
       fuera_tabla = r$p.value %in% c(0.01, 0.99))
}

kpss_de <- function(x, tipo = c("Level", "Trend")) {
  tipo <- match.arg(tipo)
  r <- suppressWarnings(kpss.test(x, null = tipo))
  list(estadistico = r3(r$statistic), p_valor = r3(r$p.value),
       truncamiento = as.integer(r$parameter),
       fuera_tabla = r$p.value %in% c(0.01, 0.1))
}

serie_json <- function(x, nombre, descripcion, unidad) {
  list(nombre = nombre, descripcion = descripcion, unidad = unidad,
       frecuencia = frequency(x), inicio = as.numeric(start(x)),
       n = length(x), valores = r3(as.numeric(x), 3))
}

cat("=== genera_preparcial.R · semilla", SEMILLA, "===\n\n")

# ---------------------------------------------------------------------------
# 1. Las series propias
# ---------------------------------------------------------------------------

set.seed(SEMILLA)

# (A) demanda — mensual, 120 obs, tendencia creciente y estacionalidad cuya
#     amplitud crece con el nivel: el caso multiplicativo, que pide logaritmo.
n_A <- 120
t_A <- seq_len(n_A)
estacional_A <- c(-0.10, -0.14, 0.02, 0.06, 0.09, 0.16, 0.21, 0.18, 0.03, -0.02, -0.06, -0.05)
demanda <- ts(exp(3.4 + 0.0075 * t_A + estacional_A[((t_A - 1) %% 12) + 1] +
                    rnorm(n_A, 0, 0.045)),
              start = c(2016, 1), frequency = 12)

# (B) ocupacion — trimestral, 48 obs. Frecuencia 4 a proposito: la media movil
#     centrada 2x4 y el grafico de rezagos contra y_{t-4} viven aqui.
n_B <- 48
t_B <- seq_len(n_B)
estacional_B <- c(-6.2, 2.8, 9.4, -6.0)
ocupacion <- ts(62 + 0.28 * t_B + estacional_B[((t_B - 1) %% 4) + 1] + rnorm(n_B, 0, 1.8),
                start = c(2014, 1), frequency = 4)

# (C) residuo_blanco — ruido blanco puro, 200 obs. 36 rezagos para que la cuenta
#     de barras esperadas fuera de banda (5 % de 36) no sea la del banco (24).
residuo_blanco <- ts(rnorm(200, 0, 1), start = 1, frequency = 1)

# (D) caudal — AR(1) con dependencia debil. Es el contraste del anterior: su
#     correlograma NO es plano, pero tampoco grita.
caudal <- ts(as.numeric(arima.sim(list(ar = 0.35), n = 200)), start = 1, frequency = 1)

# (E) indice — caminata aleatoria. Varianza que crece con t.
indice <- ts(100 + cumsum(rnorm(200, 0, 1.4)), start = 1, frequency = 1)

# (F) linea — tendencia DETERMINISTA mas ruido. Su ACF decae despacio igual que
#     la de una caminata, y sin embargo no tiene raiz unitaria. Es el
#     contraejemplo del item 18: una ACF lenta no prueba raiz unitaria.
linea <- ts(20 + 0.15 * seq_len(200) + rnorm(200, 0, 2.5), start = 1, frequency = 1)

# (G) saldo — serie con valores negativos, para que el logaritmo falle (item 32).
saldo <- ts(cumsum(rnorm(80, 0.05, 1.1)) - 1.5, start = 1, frequency = 1)

# (H) demanda_atipico — la demanda con un atipico sembrado en un mes concreto.
POS_ATIPICO <- 63
demanda_atipico <- demanda
demanda_atipico[POS_ATIPICO] <- demanda_atipico[POS_ATIPICO] * 1.55

cat("Series generadas:\n")
for (nm in c("demanda", "ocupacion", "residuo_blanco", "caudal", "indice", "linea", "saldo")) {
  x <- get(nm)
  cat(sprintf("  %-16s n=%3d  frec=%2d  media=%9.3f  sd=%8.3f\n",
              nm, length(x), frequency(x), mean(x), sd(x)))
}
cat(sprintf("  %-16s atipico en la posicion %d (x1.55)\n", "demanda_atipico", POS_ATIPICO))

# ---------------------------------------------------------------------------
# 2. La serie del item 24: el ADF que cambia de conclusion con n
# ---------------------------------------------------------------------------
# No se puede fijar de antemano: hay que BUSCAR una realizacion AR(1) con phi
# alto en la que el ADF no rechace con n=40 y si rechace con n=200. Es
# exactamente la falta de potencia, y es el item que mas trabajo da de los 32.

buscar_potencia <- function(phi = 0.82, n_corto = 40, n_largo = 200, intentos = 4000) {
  for (k in seq_len(intentos)) {
    set.seed(SEMILLA + k)
    x <- as.numeric(arima.sim(list(ar = phi), n = n_largo))
    p_corto <- suppressWarnings(adf.test(x[seq_len(n_corto)])$p.value)
    p_largo <- suppressWarnings(adf.test(x)$p.value)
    if (p_corto > 0.10 && p_largo < 0.05) {
      return(list(desplazamiento = k, x = x, p_corto = p_corto, p_largo = p_largo))
    }
  }
  stop("No se encontro una realizacion que ilustre la falta de potencia")
}

pot <- buscar_potencia()
potencia <- ts(pot$x, start = 1, frequency = 1)
cat(sprintf("\nItem 24 · realizacion hallada con SEMILLA+%d: ADF p=%.4f con n=40, p=%.4f con n=200\n",
            pot$desplazamiento, pot$p_corto, pot$p_largo))

# ---------------------------------------------------------------------------
# 2.bis. La serie del item 25: ndiffs() y kpss.test() dicen lo CONTRARIO
# ---------------------------------------------------------------------------
# La nota metodologica de precalculo/README documenta que ndiffs() no llama a
# tseries::kpss.test sino a urca::ur.kpss, con truncamiento floor(3*sqrt(n)/13)
# frente a floor(4*(n/100)^0.25). Sobre `demanda` los truncamientos difieren
# pero la CONCLUSION coincide, y entonces el item no ensena nada: hay que
# buscar una realizacion donde de verdad se contradigan.

buscar_frontera <- function(phi = 0.90, n = 120, intentos = 2000) {
  for (k in seq_len(intentos)) {
    set.seed(SEMILLA + 5000 + k)
    x <- as.numeric(arima.sim(list(ar = phi), n = n))
    nd <- suppressWarnings(ndiffs(x))
    kt <- suppressWarnings(kpss.test(x, null = "Level"))
    if ((nd > 0) != (kt$p.value < 0.05)) {
      return(list(desplazamiento = 5000 + k, x = x, ndiffs = nd, p = kt$p.value))
    }
  }
  stop("No se encontro una realizacion donde ndiffs y kpss.test se contradigan")
}

fro <- buscar_frontera()
frontera <- ts(fro$x, start = 1, frequency = 1)
cat(sprintf("Item 25 · realizacion hallada con SEMILLA+%d: ndiffs()=%d pero kpss.test p=%.3f\n",
            fro$desplazamiento, fro$ndiffs, fro$p))

# ---------------------------------------------------------------------------
# 3. El par del item 11: F_T parecida, F_S muy distinta
# ---------------------------------------------------------------------------
# Tampoco se fija a ojo. Se genera una rejilla de amplitudes estacionales sobre
# la MISMA tendencia y se elige el par cuya fuerza de tendencia difiera menos y
# cuya fuerza estacional difiera mas.

fuerzas <- function(x) {
  d <- stl(x, s.window = "periodic")$time.series
  ft <- max(0, 1 - var(d[, "remainder"]) / var(d[, "trend"] + d[, "remainder"]))
  fs <- max(0, 1 - var(d[, "remainder"]) / var(d[, "seasonal"] + d[, "remainder"]))
  c(FT = ft, FS = fs)
}

set.seed(SEMILLA + 1)
rejilla <- lapply(c(0.02, 0.05, 0.10, 0.18, 0.30), function(amp) {
  y <- ts(exp(3.4 + 0.0075 * t_A + amp * estacional_A[((t_A - 1) %% 12) + 1] / 0.21 +
                rnorm(n_A, 0, 0.045)), start = c(2016, 1), frequency = 12)
  list(amplitud = amp, serie = y, f = fuerzas(y))
})
mejor <- NULL
for (i in seq_along(rejilla)) for (j in seq_along(rejilla)) {
  if (i >= j) next
  a <- rejilla[[i]]; b <- rejilla[[j]]
  d_ft <- abs(a$f["FT"] - b$f["FT"]); d_fs <- abs(a$f["FS"] - b$f["FS"])
  if (d_ft < 0.03 && (is.null(mejor) || d_fs > mejor$d_fs)) {
    mejor <- list(a = a, b = b, d_ft = as.numeric(d_ft), d_fs = as.numeric(d_fs))
  }
}
stopifnot(!is.null(mejor))
cat(sprintf("Item 11 · par elegido: amplitudes %.2f y %.2f · dif F_T=%.4f · dif F_S=%.4f\n",
            mejor$a$amplitud, mejor$b$amplitud, mejor$d_ft, mejor$d_fs))

# ---------------------------------------------------------------------------
# 4. Los 32 items, uno por uno
# ---------------------------------------------------------------------------

items <- list()

# --- Item 1 [1.1 · G] la serie y sus valores barajados -----------------------
set.seed(SEMILLA + 101)
demanda_barajada <- ts(sample(as.numeric(demanda)), start = c(2016, 1), frequency = 12)
items$i01 <- list(
  modulo = "1.1", dimension = "G",
  acf_original = acf_de(demanda, 24), acf_barajada = acf_de(demanda_barajada, 24),
  valores_barajados = r3(as.numeric(demanda_barajada), 3),
  media_igual = r3(mean(demanda) - mean(demanda_barajada), 10),
  sd_igual = r3(sd(demanda) - sd(demanda_barajada), 10))

# --- Item 3 [1.2 · P] aritmetica del objeto ts -------------------------------
# Item de opcion multiple: la Biblioteca de Preguntas de Brightspace no importa
# respuesta numerica, asi que las cuatro opciones son cuatro fechas. Las tres
# equivocadas NO se escriben a mano: se calculan con la misma aritmetica de
# `ts` que la correcta, cada una a partir del error que representa. Si algun
# dia cambian el arranque o el numero de observaciones, los distractores se
# mueven solos y siguen siendo esos errores.
MESES_ES <- c("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
              "agosto", "septiembre", "octubre", "noviembre", "diciembre")
en_prosa <- function(fin) sprintf("%s de %d", MESES_ES[fin[2]], fin[1])

ts_demo <- ts(rep(0, 30), start = c(2019, 7), frequency = 12)
fin_correcto <- end(ts_demo)
# sumar 30 meses en vez de 29: la primera observacion ya ocupa el mes de arranque
fin_suma_n    <- end(ts(rep(0, 31), start = c(2019, 7), frequency = 12))
# contar los 30 meses desde enero, olvidando que la serie arranca en julio
fin_desde_ene <- end(ts(rep(0, 30), start = c(2019, 1), frequency = 12))
# creer que `frequency = 12` obliga a anios completos: 30 observaciones -> 3 anios
fin_anios     <- end(ts(rep(0, 37), start = c(2019, 7), frequency = 12))

items$i03 <- list(
  modulo = "1.2", dimension = "P", n = 30, inicio = c(2019, 7), frecuencia = 12,
  ultimo = as.numeric(fin_correcto),
  ultimo_texto = sprintf("%d-%02d", fin_correcto[1], fin_correcto[2]),
  ultimo_prosa = en_prosa(fin_correcto),
  errores = list(
    suma_n      = en_prosa(fin_suma_n),
    desde_enero = en_prosa(fin_desde_ene),
    anios       = en_prosa(fin_anios)))

# --- Item 4 [1.3 · G] gg_subseries: medias por mes ---------------------------
meses <- cycle(demanda)
items$i04 <- list(
  modulo = "1.3", dimension = "G",
  medias_por_mes = r3(tapply(as.numeric(demanda), meses, mean), 3),
  mes_mas_alto = as.integer(which.max(tapply(as.numeric(demanda), meses, mean))),
  mes_mas_bajo = as.integer(which.min(tapply(as.numeric(demanda), meses, mean))),
  # Lo que el grafico estacional NO deja ver: la TENDENCIA dentro de cada mes.
  pendiente_por_mes = r3(sapply(1:12, function(m) {
    y <- as.numeric(demanda)[meses == m]
    unname(coef(lm(y ~ seq_along(y)))[2])
  }), 4))

# --- Item 5 [1.4 · C] que componente absorbe el atipico ----------------------
d_at <- stl(log(demanda_atipico), s.window = "periodic")$time.series
d_li <- stl(log(demanda), s.window = "periodic")$time.series
items$i05 <- list(
  modulo = "1.4", dimension = "C", posicion_atipico = POS_ATIPICO,
  salto_en_residuo = r3(d_at[POS_ATIPICO, "remainder"] - d_li[POS_ATIPICO, "remainder"]),
  salto_en_tendencia = r3(d_at[POS_ATIPICO, "trend"] - d_li[POS_ATIPICO, "trend"]),
  salto_en_estacional = r3(d_at[POS_ATIPICO, "seasonal"] - d_li[POS_ATIPICO, "seasonal"]),
  sd_residuo_limpia = r3(sd(d_li[, "remainder"])),
  sd_residuo_atipico = r3(sd(d_at[, "remainder"])))

# --- Items 6 y 7 [1.5 · P, I] medias moviles ---------------------------------
cinco <- r3(as.numeric(window(ocupacion, start = c(2014, 1), end = c(2015, 1))), 2)
ma_2x4 <- function(y) {
  m4 <- stats::filter(y, rep(1 / 4, 4), sides = 2)
  stats::filter(m4, c(0.5, 0.5), sides = 1)
}
tendencia_centrada <- ma_2x4(as.numeric(ocupacion))
tendencia_sin_centrar <- as.numeric(stats::filter(as.numeric(ocupacion), rep(1 / 4, 4), sides = 1))
items$i06 <- list(
  modulo = "1.5", dimension = "P", observaciones = cinco,
  # Primer valor de la 2x4: media de las dos MA(4) consecutivas, es decir
  # (1/8, 1/4, 1/4, 1/4, 1/8) sobre las cinco observaciones.
  pesos = c(0.125, 0.25, 0.25, 0.25, 0.125),
  respuesta = r3(sum(c(0.125, 0.25, 0.25, 0.25, 0.125) * cinco), 3),
  comprobacion = r3(tendencia_centrada[3], 3))
items$i07 <- list(
  modulo = "1.5", dimension = "I",
  centrada = r3(tendencia_centrada, 3), sin_centrar = r3(tendencia_sin_centrar, 3),
  # El desfase: la MA(4) de un solo lado va medio periodo por detras.
  desfase_periodos = 0.5,
  no_estimados_inicio = as.integer(sum(is.na(tendencia_centrada[1:6]))),
  no_estimados_final = as.integer(sum(is.na(tail(tendencia_centrada, 6)))))

# --- Item 8 [1.6 · P] indices estacionales clasicos --------------------------
dc <- decompose(ocupacion, type = "additive")
detrended <- as.numeric(ocupacion) - as.numeric(dc$trend)
prom_trim <- tapply(detrended, cycle(ocupacion), mean, na.rm = TRUE)
items$i08 <- list(
  modulo = "1.6", dimension = "P",
  promedios_sin_tendencia = r3(prom_trim, 4),
  media_de_promedios = r3(mean(prom_trim), 4),
  indices = r3(prom_trim - mean(prom_trim), 4),
  suman_cero = r3(sum(prom_trim - mean(prom_trim)), 10),
  indices_de_R = r3(as.numeric(dc$figure), 4))

# --- Items 9 y 10 [1.7 · I, G] la malla de s.window --------------------------
malla_sw <- lapply(list(5, 21, "periodic"), function(sw) {
  d <- stl(log(demanda), s.window = if (is.character(sw)) sw else as.numeric(sw))$time.series
  a <- acf(d[, "remainder"], lag.max = 24, plot = FALSE)
  list(s_window = if (is.character(sw)) sw else as.numeric(sw),
       var_estacional = r3(var(d[, "seasonal"]), 6),
       var_residuo = r3(var(d[, "remainder"]), 6),
       acf_residuo_12 = r3(as.numeric(a$acf)[13]),
       banda = r3(1.96 / sqrt(n_A)),
       queda_estacionalidad = abs(as.numeric(a$acf)[13]) > 1.96 / sqrt(n_A))
})
items$i09 <- list(modulo = "1.7", dimension = "I", malla = malla_sw)

stl_robusto <- stl(log(demanda_atipico), s.window = "periodic", robust = TRUE)$time.series
stl_no_robusto <- stl(log(demanda_atipico), s.window = "periodic", robust = FALSE)$time.series
items$i10 <- list(
  modulo = "1.7", dimension = "G", posicion_atipico = POS_ATIPICO,
  mes_atipico = as.integer(cycle(demanda)[POS_ATIPICO]),
  robusto = list(residuo_en_atipico = r3(stl_robusto[POS_ATIPICO, "remainder"]),
                 var_estacional = r3(var(stl_robusto[, "seasonal"]), 6)),
  no_robusto = list(residuo_en_atipico = r3(stl_no_robusto[POS_ATIPICO, "remainder"]),
                    var_estacional = r3(var(stl_no_robusto[, "seasonal"]), 6)),
  # Lo que se contamina al no ser robusto: el estacional del MES del atipico.
  estacional_del_mes = list(
    robusto = r3(stl_robusto[POS_ATIPICO, "seasonal"]),
    no_robusto = r3(stl_no_robusto[POS_ATIPICO, "seasonal"])),
  # El ciclo estacional de los 12 meses bajo las dos variantes. Hace falta
  # para poder DIBUJAR el item: con los escalares no se ve nada.
  ciclo_robusto = r3(tapply(stl_robusto[, "seasonal"], cycle(demanda), mean)),
  ciclo_no_robusto = r3(tapply(stl_no_robusto[, "seasonal"], cycle(demanda), mean)),
  # Y el residuo alrededor del atipico, que es donde se ve la diferencia.
  ventana = as.integer((POS_ATIPICO - 6):(POS_ATIPICO + 6)),
  residuo_robusto = r3(stl_robusto[(POS_ATIPICO - 6):(POS_ATIPICO + 6), "remainder"]),
  residuo_no_robusto = r3(stl_no_robusto[(POS_ATIPICO - 6):(POS_ATIPICO + 6), "remainder"]))

# --- Item 11 [1.8 · I] F_T parecida, F_S distinta ----------------------------
items$i11 <- list(
  modulo = "1.8", dimension = "I",
  serie_1 = list(amplitud = mejor$a$amplitud, FT = r3(mejor$a$f["FT"]), FS = r3(mejor$a$f["FS"]),
                 valores = r3(as.numeric(mejor$a$serie), 3)),
  serie_2 = list(amplitud = mejor$b$amplitud, FT = r3(mejor$b$f["FT"]), FS = r3(mejor$b$f["FS"]),
                 valores = r3(as.numeric(mejor$b$serie), 3)),
  diferencia_FT = r3(mejor$d_ft), diferencia_FS = r3(mejor$d_fs))

# --- Items 12 y 13 [2.1 · C] las tres condiciones ----------------------------
tramos <- function(x, k = 3) {
  cortes <- split(as.numeric(x), cut(seq_along(x), k, labels = FALSE))
  list(medias = r3(sapply(cortes, mean), 3), varianzas = r3(sapply(cortes, var), 3))
}
items$i12 <- list(
  modulo = "2.1", dimension = "C",
  con_tendencia = tramos(linea), caminata = tramos(indice),
  estacional = tramos(demanda), blanco = tramos(residuo_blanco))
items$i13 <- list(
  modulo = "2.1", dimension = "C",
  # La tercera condicion: Cov(y_t, y_{t+h}) depende solo de h, no de t.
  # Se ilustra con la caminata, cuya autocovarianza a rezago 1 crece con t.
  autocov_rezago1_por_tramo = r3(sapply(
    split(as.numeric(indice), cut(seq_along(indice), 3, labels = FALSE)),
    function(z) cov(z[-length(z)], z[-1])), 3))

# --- Items 14 y 15 [2.2 · P, G] ruido blanco ---------------------------------
a_blanco <- acf_de(residuo_blanco, 36)
fuera <- sum(abs(a_blanco$acf) > a_blanco$banda)
# Tambien de opcion multiple, y por lo mismo. Los tres distractores son tres
# formas concretas de equivocarse con la banda, calculadas y no escritas.
items$i14 <- list(
  modulo = "2.2", dimension = "P", n = length(residuo_blanco), rezagos = 36,
  banda = a_blanco$banda, acf = a_blanco$acf,
  observadas_fuera = as.integer(fuera),
  esperadas_fuera = r3(0.05 * 36, 2),
  errores = list(
    # creer que bajo la nula no se sale ninguna barra
    ninguna    = 0,
    # aplicar el 5 % a las observaciones en vez de a los rezagos
    sobre_n    = r3(0.05 * length(residuo_blanco), 2),
    # contar dos veces las dos colas y usar el 10 %
    doble_cola = r3(0.10 * 36, 2)),
  rezagos_fuera = as.integer(which(abs(a_blanco$acf) > a_blanco$banda)))
items$i15 <- list(
  modulo = "2.2", dimension = "G",
  blanco = a_blanco, ar_debil = acf_de(caudal, 36),
  phi_verdadero = 0.35,
  pacf1_blanco = a_blanco$pacf[1], pacf1_ar = acf_de(caudal, 36)$pacf[1])

# --- Item 16 [2.5 · I] la varianza de la caminata ----------------------------
items$i16 <- list(
  modulo = "2.5", dimension = "I",
  varianza_por_tramo = tramos(indice)$varianzas,
  adf = adf_de(indice), kpss_nivel = kpss_de(indice, "Level"),
  acf = acf_de(indice, 24)$acf[1:6],
  adf_diferenciada = adf_de(diff(indice)))

# --- Item 17 [2.3 · P] r_1 a mano --------------------------------------------
seis <- c(12, 15, 11, 18, 14, 16)
media6 <- mean(seis)
num6 <- sum((seis[-length(seis)] - media6) * (seis[-1] - media6))
den6 <- sum((seis - media6)^2)
items$i17 <- list(
  modulo = "2.3", dimension = "P", observaciones = seis, media = r3(media6),
  numerador = r3(num6), denominador = r3(den6), respuesta = r3(num6 / den6),
  comprobacion_R = r3(as.numeric(acf(seis, lag.max = 1, plot = FALSE)$acf)[2]))

# --- Item 18 [2.3 · I] la ACF lenta que NO prueba raiz unitaria --------------
items$i18 <- list(
  modulo = "2.3", dimension = "I",
  acf_linea = acf_de(linea, 24)$acf[1:10],
  acf_caminata = acf_de(indice, 24)$acf[1:10],
  # La linea tiene tendencia DETERMINISTA: el ADF con tendencia la rechaza.
  linea_adf = adf_de(linea),
  linea_kpss_nivel = kpss_de(linea, "Level"),
  linea_kpss_tendencia = kpss_de(linea, "Trend"),
  caminata_adf = adf_de(indice),
  caminata_kpss_tendencia = kpss_de(indice, "Trend"))

# --- Item 19 [2.3 · G] leer el periodo en el correlograma --------------------
a_dem <- acf_de(diff(log(demanda)), 36)
items$i19 <- list(
  modulo = "2.3", dimension = "G", acf = a_dem$acf, banda = a_dem$banda,
  picos = as.integer(which(abs(a_dem$acf) > a_dem$banda)),
  periodo = 12L)

# --- Item 20 [2.4 · P] phi_22 a mano -----------------------------------------
a_oc <- acf(as.numeric(ocupacion), lag.max = 2, plot = FALSE)
r1 <- as.numeric(a_oc$acf)[2]; r2 <- as.numeric(a_oc$acf)[3]
items$i20 <- list(
  modulo = "2.4", dimension = "P", r1 = r3(r1), r2 = r3(r2),
  respuesta = r3((r2 - r1^2) / (1 - r1^2)),
  comprobacion_R = r3(as.numeric(pacf(as.numeric(ocupacion), lag.max = 2, plot = FALSE)$acf)[2]))

# --- Item 21 [2.4 · I] phi_11 = r_1 siempre ----------------------------------
items$i21 <- list(
  modulo = "2.4", dimension = "I",
  comprobado_en = lapply(list(demanda = demanda, caudal = caudal, indice = indice),
                         function(x) {
                           r <- as.numeric(acf(x, lag.max = 2, plot = FALSE)$acf)[2]
                           p <- as.numeric(pacf(x, lag.max = 2, plot = FALSE)$acf)[1]
                           list(r1 = r3(r), phi11 = r3(p), diferencia = r3(r - p, 12))
                         }))

# --- Item 22 [2.3 · 1.3 · G] grafico de rezagos ------------------------------
y_oc <- as.numeric(ocupacion)
items$i22 <- list(
  modulo = "2.3 · 1.3", dimension = "G",
  pares_rezago4 = list(x = r3(head(y_oc, -4), 3), y = r3(tail(y_oc, -4), 3)),
  pares_rezago1 = list(x = r3(head(y_oc, -1), 3), y = r3(tail(y_oc, -1), 3)),
  r4 = r3(as.numeric(acf(y_oc, lag.max = 4, plot = FALSE)$acf)[5]),
  r1 = r3(as.numeric(acf(y_oc, lag.max = 4, plot = FALSE)$acf)[2]),
  trimestre = as.integer(cycle(ocupacion)[-(1:4)]))

# --- Item 23 [2.6 · C] que caso caza el KPSS y el ADF deja pasar -------------
items$i23 <- list(
  modulo = "2.6", dimension = "C",
  # linea: el ADF (que incluye tendencia) la trata bien, pero el KPSS de NIVEL
  # la rechaza. Es la serie estacionaria en tendencia, no en nivel.
  linea = list(adf = adf_de(linea), kpss_nivel = kpss_de(linea, "Level"),
               kpss_tendencia = kpss_de(linea, "Trend")),
  caudal = list(adf = adf_de(caudal), kpss_nivel = kpss_de(caudal, "Level")))

# --- Item 24 [2.6 · I] la potencia del ADF -----------------------------------
items$i24 <- list(
  modulo = "2.6", dimension = "I", phi = 0.82, desplazamiento_semilla = pot$desplazamiento,
  corto = list(n = 40, adf = adf_de(potencia[1:40]), kpss = kpss_de(potencia[1:40], "Level")),
  largo = list(n = 200, adf = adf_de(potencia), kpss = kpss_de(potencia, "Level")),
  valores = r3(as.numeric(potencia), 4))

# --- Item 25 [2.6 · P] los dos truncamientos ---------------------------------
trunc_ndiffs <- function(n) floor(3 * sqrt(n) / 13)
trunc_kpss <- function(n) floor(4 * (n / 100)^0.25)
items$i25 <- list(
  modulo = "2.6", dimension = "P",
  n = length(frontera),
  desplazamiento_semilla = fro$desplazamiento,
  truncamiento_urca = as.integer(trunc_ndiffs(length(frontera))),
  truncamiento_kpss_test = as.integer(trunc_kpss(length(frontera))),
  # El mismo dato, dos funciones, dos conclusiones opuestas. Esto es el item.
  ndiffs = as.integer(ndiffs(frontera)),
  kpss_test_nivel = kpss_de(frontera, "Level"),
  adf = adf_de(frontera),
  se_contradicen = (as.integer(ndiffs(frontera)) > 0) !=
    (suppressWarnings(kpss.test(frontera, null = "Level"))$p.value < 0.05),
  tabla = lapply(c(60, 100, 120, 200, 468), function(n)
    list(n = as.integer(n), urca = as.integer(trunc_ndiffs(n)),
         kpss_test = as.integer(trunc_kpss(n)))))

# --- Item 26 [2.6 · I] ur.df con deriva y con tendencia ----------------------
df_drift <- ur.df(as.numeric(linea), type = "drift", lags = trunc((length(linea) - 1)^(1 / 3)))
df_trend <- ur.df(as.numeric(linea), type = "trend", lags = trunc((length(linea) - 1)^(1 / 3)))
items$i26 <- list(
  modulo = "2.6", dimension = "I",
  drift = list(estadistico = r3(df_drift@teststat[1]), criticos = r3(df_drift@cval[1, ])),
  trend = list(estadistico = r3(df_trend@teststat[1]), criticos = r3(df_trend@cval[1, ])),
  rechaza_drift_5 = as.logical(df_drift@teststat[1] < df_drift@cval[1, "5pct"]),
  rechaza_trend_5 = as.logical(df_trend@teststat[1] < df_trend@cval[1, "5pct"]))

# --- Item 27 [2.7 · P] la tabla de varianzas ---------------------------------
tabla_var <- lapply(0:3, function(d) {
  y <- if (d == 0) log(demanda) else diff(log(demanda), differences = d)
  list(orden = as.integer(d), n = length(y), varianza = r3(var(y), 6))
})
tabla_var_est <- lapply(0:2, function(d) {
  y <- diff(log(demanda), lag = 12)
  if (d > 0) y <- diff(y, differences = d)
  list(orden_regular_tras_estacional = as.integer(d), n = length(y), varianza = r3(var(y), 6))
})
items$i27 <- list(
  modulo = "2.7", dimension = "P", tabla = tabla_var, tabla_tras_estacional = tabla_var_est,
  minimo_en = as.integer(which.min(sapply(tabla_var, function(z) z$varianza)) - 1),
  ndiffs = as.integer(ndiffs(log(demanda))),
  nsdiffs = as.integer(nsdiffs(log(demanda))))

# --- Item 28 [2.7 · I] las diferencias conmutan ------------------------------
a1 <- diff(diff(log(demanda), lag = 12), lag = 1)
a2 <- diff(diff(log(demanda), lag = 1), lag = 12)
items$i28 <- list(
  modulo = "2.7", dimension = "I",
  n_original = n_A, n_resultado = length(a1),
  diferencia_maxima = r3(max(abs(as.numeric(a1) - as.numeric(a2))), 12),
  conmutan = isTRUE(all.equal(as.numeric(a1), as.numeric(a2))),
  var_estacional_primero = r3(var(a1), 6), var_regular_primero = r3(var(a2), 6))

# --- Item 29 [2.7 · G] ¿basto d = 1? -----------------------------------------
items$i29 <- list(
  modulo = "2.7", dimension = "G",
  antes = list(acf = acf_de(log(demanda), 36)$acf, banda = r3(1.96 / sqrt(n_A)),
               adf = adf_de(log(demanda))),
  despues = list(acf = acf_de(diff(log(demanda)), 36)$acf,
                 banda = r3(1.96 / sqrt(n_A - 1)),
                 adf = adf_de(diff(log(demanda))),
                 kpss = kpss_de(diff(log(demanda)), "Level")),
  # La respuesta: d=1 quita la tendencia pero NO la estacionalidad.
  acf12_despues = r3(as.numeric(acf(diff(log(demanda)), lag.max = 12, plot = FALSE)$acf)[13]))

# --- Items 30 y 31 [2.8 · C, P] Box-Cox --------------------------------------
lambda <- BoxCox.lambda(demanda, method = "guerrero")
valor_demo <- as.numeric(demanda)[1]
items$i30 <- list(
  modulo = "2.8", dimension = "C",
  var_por_tramo_cruda = tramos(demanda)$varianzas,
  var_por_tramo_log = tramos(log(demanda))$varianzas,
  media_por_tramo_cruda = tramos(demanda)$medias,
  media_por_tramo_log = tramos(log(demanda))$medias)
items$i31 <- list(
  modulo = "2.8", dimension = "P", lambda = r3(lambda),
  valor = r3(valor_demo, 3),
  transformado = r3(if (abs(lambda) < 1e-8) log(valor_demo)
                    else (valor_demo^lambda - 1) / lambda),
  comprobacion_R = r3(as.numeric(BoxCox(valor_demo, lambda))),
  log_del_valor = r3(log(valor_demo)))

# --- Item 32 [2.9 · I] el orden del pipeline ---------------------------------
saldo_dif <- diff(saldo)
items$i32 <- list(
  modulo = "2.9", dimension = "I",
  minimo_original = r3(min(saldo), 3), minimo_diferenciado = r3(min(saldo_dif), 3),
  negativos_original = as.integer(sum(saldo <= 0)),
  negativos_diferenciados = as.integer(sum(saldo_dif <= 0)),
  cuantos_NaN = as.integer(sum(is.nan(suppressWarnings(log(as.numeric(saldo_dif)))))),
  valores = r3(as.numeric(saldo), 3))

# Items sin cifras propias (conceptuales puros): 2. Se declara para que la
# cuenta de 32 cuadre y para que verifica_preparcial.R no lo eche en falta.
items$i02 <- list(modulo = "1.1 · 1.9", dimension = "C", sin_cifras = TRUE)

items <- items[order(names(items))]


# ---------------------------------------------------------------------------
# 4b. Los dos pares del bloque E (FPP3 §2.6, diagramas de dispersion)
#
# Son los unicos datos BIVARIADOS del preparcial: todo lo demas es univariado,
# y sin dos series relacionadas no hay diagrama de dispersion que ensenar. Cada
# par existe para que una lectura concreta falle:
#
#   (1) temperatura / demanda_electrica — correlacion ALTA y relacion NO lineal.
#       Es el ejemplo del capitulo 2 de FPP3: la demanda sube con el calor por
#       el aire acondicionado y vuelve a subir con el frio por la calefaccion.
#       En clima templado la rama de calor domina, asi que la recta ajusta
#       "bien" —r alto— y aun asi se equivoca sistematicamente en los extremos.
#       Ese es el ítem: un coeficiente alto no dice que la relacion sea lineal.
#
#   (2) ventas_norte / ventas_sur — correlacion alta y relacion NINGUNA. Dos
#       caminatas aleatorias INDEPENDIENTES, generadas con semillas distintas.
#       El delator es que sus diferencias no se correlacionan: lo que compartian
#       era la tendencia, no el comportamiento.
# ---------------------------------------------------------------------------

set.seed(SEMILLA + 700)
n_disp <- 120
temperatura <- round(runif(n_disp, 8, 32), 1)
# Confort en 18 grados; la rama de calor pesa mas que la de frio, que es lo que
# hace la U asimetrica y deja la correlacion lineal alta.
calor <- pmax(0, temperatura - 18)
frio  <- pmax(0, 15 - temperatura)
demanda_electrica <- round(120 + 2.4 * calor^1.45 + 2.1 * frio^1.35 +
                             rnorm(n_disp, 0, 6), 2)

ajuste_disp <- lm(demanda_electrica ~ temperatura)
resid_disp  <- residuals(ajuste_disp)
tercil <- cut(temperatura, quantile(temperatura, c(0, 1/3, 2/3, 1)),
              include.lowest = TRUE, labels = FALSE)
resid_por_tercil <- tapply(resid_disp, tercil, mean)

# El par espurio tampoco se fija a ojo, por la misma razon que la realizacion
# del item 25: hace falta una donde el fenomeno se VEA. Se recorren pares
# independientes y se elige el primero con correlacion de niveles alta y
# correlacion de diferencias despreciable. Y de paso se cuenta cuantos de los
# `intentos` pasan de 0.7, que es el dato que de verdad ensena el item: no es
# que hayamos tenido suerte, es que pasa constantemente.
buscar_espurias <- function(intentos = 400, r_min = 0.85, r_dif_max = 0.15) {
  hallado <- NULL
  altos <- 0L
  for (k in seq_len(intentos)) {
    set.seed(SEMILLA + 7000 + 2 * k)
    a <- cumsum(rnorm(n_disp, 0.8, 4)) + 200
    set.seed(SEMILLA + 7001 + 2 * k)
    b <- cumsum(rnorm(n_disp, 0.7, 4)) + 180
    if (abs(cor(a, b)) > 0.7) altos <- altos + 1L
    if (is.null(hallado) && cor(a, b) > r_min &&
        abs(cor(diff(a), diff(b))) < r_dif_max) {
      hallado <- list(k = k, a = a, b = b)
    }
  }
  if (is.null(hallado)) {
    stop("No se encontro un par espurio con r > ", r_min, " y diferencias planas")
  }
  c(hallado, list(intentos = intentos, altos = altos))
}

esp <- buscar_espurias()
ventas_norte <- esp$a
ventas_sur   <- esp$b
cat(sprintf("Bloque E · par espurio hallado en el intento %d; %d de %d pares independientes pasan de |r| = 0.7\n",
            esp$k, esp$altos, esp$intentos))

bloque_e <- list(
  dispersion = list(
    n = n_disp,
    correlacion = r3(cor(temperatura, demanda_electrica), 3),
    r2_lineal = r3(summary(ajuste_disp)$r.squared, 3),
    # El patron que delata la curva: la recta se queda CORTA en los dos
    # extremos y se pasa en el centro. Es la U vista desde la recta.
    residuo_por_tercil = r3(as.numeric(resid_por_tercil), 2),
    temperatura_confort = 18),
  espuria = list(
    n = n_disp,
    correlacion_niveles = r3(cor(ventas_norte, ventas_sur), 3),
    correlacion_diferencias = r3(cor(diff(ventas_norte), diff(ventas_sur)), 3),
    pares_probados = esp$intentos,
    pares_con_r_alto = esp$altos,
    de_cada_cien = as.integer(round(100 * esp$altos / esp$intentos))))

cat("\n=== Bloque E · los dos pares =================================\n")
cat(sprintf("dispersion  r = %.3f  R2 = %.3f  residuo por tercil: %s\n",
            bloque_e$dispersion$correlacion, bloque_e$dispersion$r2_lineal,
            paste(sprintf("%+.2f", bloque_e$dispersion$residuo_por_tercil), collapse = " ")))
cat(sprintf("espuria     r(niveles) = %.3f   r(diferencias) = %.3f\n",
            bloque_e$espuria$correlacion_niveles,
            bloque_e$espuria$correlacion_diferencias))

# ---------------------------------------------------------------------------
# 5. Salida
# ---------------------------------------------------------------------------

series <- list(
  temperatura = serie_json(ts(temperatura), "Temperatura media diaria",
                           "Ciento veinte dias de temperatura, entre 8 y 32 grados", "grados C"),
  demanda_electrica = serie_json(ts(demanda_electrica), "Demanda electrica diaria",
                                 "La de esos mismos dias: sube con el calor y vuelve a subir con el frio", "MW"),
  ventas_norte = serie_json(ts(ventas_norte), "Ventas de la tienda del norte",
                            "Caminata aleatoria con deriva", "millones"),
  ventas_sur = serie_json(ts(ventas_sur), "Ventas de la tienda del sur",
                          "Otra caminata aleatoria, generada aparte y sin relacion con la anterior", "millones"),
  demanda = serie_json(demanda, "Demanda mensual", "Serie mensual con tendencia y estacionalidad de amplitud creciente", "miles de unidades"),
  demanda_atipico = serie_json(demanda_atipico, "Demanda con atípico", "La misma, con un mes anómalo sembrado", "miles de unidades"),
  ocupacion = serie_json(ocupacion, "Ocupación trimestral", "Serie trimestral con tendencia y estacionalidad aditiva", "por ciento"),
  residuo_blanco = serie_json(residuo_blanco, "Ruido blanco", "Ruido blanco puro", "unidades tipificadas"),
  caudal = serie_json(caudal, "Dependencia débil", "AR(1) con phi = 0.35", "unidades tipificadas"),
  indice = serie_json(indice, "Índice acumulado", "Caminata aleatoria", "puntos"),
  linea = serie_json(linea, "Tendencia determinista", "Recta más ruido: ACF lenta SIN raíz unitaria", "unidades"),
  saldo = serie_json(saldo, "Saldo neto", "Serie con valores negativos", "millones"),
  potencia = serie_json(potencia, "AR(1) persistente", "phi = 0.82: el ADF cambia de conclusión entre n=40 y n=200", "unidades tipificadas"),
  frontera = serie_json(frontera, "AR(1) en la frontera", "phi = 0.90: ndiffs() y kpss.test() concluyen lo contrario sobre el mismo dato", "unidades tipificadas"))

salida <- list(
  meta = list(
    semilla = SEMILLA,
    generado = format(Sys.Date(), "%Y-%m-%d"),
    r_version = R.version.string,
    paquetes = list(jsonlite = as.character(packageVersion("jsonlite")),
                    tseries = as.character(packageVersion("tseries")),
                    forecast = as.character(packageVersion("forecast")),
                    urca = as.character(packageVersion("urca"))),
    n_items = length(items),
    nota = "Preparcial del Corte I. Formativo, sin nota: no hay clave oculta."),
  series = series,
  items = items,
  bloque_e = bloque_e)

ruta_json <- file.path(dir_salidas, "preparcial_datos.json")
write_json(salida, ruta_json, auto_unbox = TRUE, digits = NA, pretty = TRUE, null = "null")
ruta_js <- file.path(dir_salidas, "preparcial_datos.js")
writeLines(c("// Generado por genera_preparcial.R — no editar a mano",
             paste0("const PREPARCIAL_DATOS = ",
                    toJSON(salida, auto_unbox = TRUE, digits = NA, null = "null"), ";")),
           ruta_js, useBytes = TRUE)

cat("\n=== Resumen ================================================\n")
cat(sprintf("items con cifras ....... %d de 32\n", length(items)))
cat(sprintf("series ................. %d\n", length(series)))
cat(sprintf("JSON ................... %s (%.0f KB)\n", basename(ruta_json),
            file.size(ruta_json) / 1024))
cat(sprintf("JS ..................... %s (%.0f KB)\n", basename(ruta_js),
            file.size(ruta_js) / 1024))
cat("\n=== Cifras que van a la pantalla ===========================\n")
cat(sprintf("i06 MA 2x4, primer valor ........ %.3f (R: %.3f)\n", items$i06$respuesta, items$i06$comprobacion))
cat(sprintf("i08 indices suman ............... %.10f\n", items$i08$suman_cero))
cat(sprintf("i14 fuera de banda .............. %d observadas, %.1f esperadas\n",
            items$i14$observadas_fuera, items$i14$esperadas_fuera))
cat(sprintf("i17 r1 a mano ................... %.4f (R: %.4f)\n", items$i17$respuesta, items$i17$comprobacion_R))
cat(sprintf("i20 phi_22 a mano ............... %.4f (R: %.4f)\n", items$i20$respuesta, items$i20$comprobacion_R))
cat(sprintf("i24 ADF n=40 p=%.4f  ->  n=200 p=%.4f\n", items$i24$corto$adf$p_valor, items$i24$largo$adf$p_valor))
cat(sprintf("i25 truncamientos n=%d .......... urca=%d, kpss.test=%d\n",
            items$i25$n, items$i25$truncamiento_urca, items$i25$truncamiento_kpss_test))
cat(sprintf("i25 ndiffs()=%d vs kpss.test p=%.3f -> se contradicen: %s\n",
            items$i25$ndiffs, items$i25$kpss_test_nivel$p_valor, items$i25$se_contradicen))
cat(sprintf("i27 minimo de varianza en d ..... %d (ndiffs=%d, nsdiffs=%d)\n",
            items$i27$minimo_en, items$i27$ndiffs, items$i27$nsdiffs))
cat(sprintf("i28 conmutan .................... %s (dif max %.2e)\n",
            items$i28$conmutan, items$i28$diferencia_maxima))
cat(sprintf("i31 lambda de Guerrero .......... %.4f\n", items$i31$lambda))
cat(sprintf("i32 NaN al aplicar log tras diff  %d de %d\n", items$i32$cuantos_NaN, length(saldo) - 1))
cat("\nListo.\n")
