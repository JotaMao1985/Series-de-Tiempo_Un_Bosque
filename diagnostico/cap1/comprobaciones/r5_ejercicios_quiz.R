# R5 · practica · capitulo 1
# ---------------------------------------------------------------------------
# Un solo guion para TODAS las cifras de la ronda R5 (primer encargo):
# el bloque del Modulo 2, los ejercicios 1 a 3 y las preguntas del quiz.
#
# Uso (desde la raiz del repo):
#   Rscript --vanilla diagnostico/cap1/comprobaciones/r5_ejercicios_quiz.R \
#     > diagnostico/cap1/comprobaciones/r5_ejercicios_quiz.out 2>&1
#
# Cada linea de la salida lleva una etiqueta entre corchetes ([E1-07], [Q2-03]...)
# y `diagnostico/cap1/R5_cambios.md` dice de que etiqueta sale cada cifra del
# capitulo. Las secciones «BLOQUE» ejecutan, tal cual, el codigo que el capitulo
# publica en las soluciones: su salida es la que el capitulo copia tras `#>`.
# ---------------------------------------------------------------------------
options(width = 80, warn = 1)
suppressMessages(library(fpp3))

L <- function(etq, ...) cat(sprintf("[%s] ", etq), ..., "\n", sep = "")
titulo <- function(x) cat("\n", strrep("=", 76), "\n", x, "\n", strrep("=", 76), "\n", sep = "")
anio_de <- function(x) floor(time(x) + 1e-6)   # anio de cada observacion, a salvo del redondeo

titulo("0 · Entorno")
L("ENT-01", R.version.string)
L("ENT-02", "fpp3 ", as.character(packageVersion("fpp3")),
  " · tsibble ", as.character(packageVersion("tsibble")),
  " · tsibbledata ", as.character(packageVersion("tsibbledata")),
  " · feasts ", as.character(packageVersion("feasts")),
  " · ggtime ", as.character(packageVersion("ggtime")))
L("ENT-03", "locale: ", Sys.getlocale())

cat("\n--- que es cada serie, segun la ayuda de R (titulo y descripcion) ---\n")
for (nm in c("co2", "nottem", "USAccDeaths", "AirPassengers", "UKgas")) {
  h <- gsub("_\b", "", capture.output(tools::Rd2txt(utils:::.getHelpFile(help(nm, package = "datasets")))))
  h <- h[nzchar(trimws(h))]
  fin <- which(grepl("^(Usage|Format):", h))[1]
  cat(paste0("[ENT-04 ?", nm, "] ", h[seq_len(fin - 1)]), sep = "\n")
}

# ===========================================================================
titulo("M2 · BLOQUE del Modulo 2: lo que R imprime de verdad")
# ===========================================================================
data(AirPassengers)
print(frequency(AirPassengers))
print(start(AirPassengers))
pasajeros <- as_tsibble(AirPassengers)
cat("--- print(pasajeros, n = 2) ---\n")
print(pasajeros, n = 2)
cat("--- pasajeros (impresion por defecto, lo que el bloque NO muestra) ---\n")
print(pasajeros)
L("M2-01", "filas totales = ", nrow(pasajeros), " ; mostradas con n = 2 -> quedan ", nrow(pasajeros) - 2)
cat("--- la misma orden en una sesion UTF-8, que es la de RStudio: cambia el simbolo de la ultima linea ---\n")
orden <- "suppressMessages(library(fpp3)); print(as_tsibble(AirPassengers), n = 2)"
for (loc in c("en_US.UTF-8", "es_ES.UTF-8")) {
  sal <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript"), c("--vanilla", "-e", shQuote(orden)),
                                  env = paste0("LC_ALL=", loc), stdout = TRUE, stderr = TRUE))
  cat(paste0("[M2-02 ", loc, "] ", sal), sep = "\n")
}
L("M2-03", "el bloque del capitulo copia la salida de en_US.UTF-8; los nombres de los meses siguen el idioma del sistema")

# ===========================================================================
titulo("E1 · Ejercicio 1: co2, aditiva o multiplicativa")
# ===========================================================================
L("E1-01", "co2: n = ", length(co2), ", frecuencia ", frequency(co2), ", de ",
  paste(start(co2), collapse = "-"), " a ", paste(end(co2), collapse = "-"),
  " (", length(unique(anio_de(co2))), " anios completos)")
stopifnot(identical(as.numeric(floor(time(co2))), as.numeric(anio_de(co2))))
L("E1-02", "floor(time(co2)) coincide con el anio a salvo del redondeo en las 468 observaciones: TRUE")

cat("\n--- (a) lo que ensena el grafico estacional ---\n")
mes_max <- tapply(co2, anio_de(co2), which.max); mes_min <- tapply(co2, anio_de(co2), which.min)
L("E1-03", "mes del maximo de cada anio (tabla mes:n.anios): ",
  paste(names(table(mes_max)), table(mes_max), sep = ":", collapse = "  "))
L("E1-04", "mes del minimo de cada anio (tabla mes:n.anios): ",
  paste(names(table(mes_min)), table(mes_min), sep = ":", collapse = "  "))

L("E1-04b", "minimo de la serie = ", min(co2), " ppm ; maximo = ", max(co2), " ppm ; recorrido = ", round(max(co2) - min(co2), 2), " ppm")
pdf(NULL)
co2_ts <- as_tsibble(co2)
g1 <- autoplot(co2_ts, value); g2 <- gg_season(co2_ts, value); print(g1); print(g2)
invisible(dev.off())
L("E1-04c", "autoplot(co2_ts, value) y gg_season(co2_ts, value) se dibujan sin error ni aviso (los avisos, si los hubiera, saldrian encima de esta linea)")

cat("\n--- BLOQUE (b) y (c) de la solucion, tal como va en el capitulo (alli sin print(): R imprime solo) ---\n")
# (b) Medir: nivel y amplitud de cada anio, como en el Modulo 4
anio     <- floor(time(co2))
nivel    <- tapply(co2, anio, mean)
amplitud <- tapply(co2, anio, function(z) max(z) - min(z))
tabla    <- cbind(nivel, amplitud, pct = 100 * amplitud / nivel)
print(round(tabla[c("1959", "1978", "1997"), ], 2))

ajuste <- lm(log(amplitud) ~ log(nivel))
print(round(c(b = coef(ajuste)[[2]], confint(ajuste)[2, ]), 3))

# (c) Descomponer de las dos maneras y comparar las series ajustadas, en ppm
adi <- decompose(co2, type = "additive")
mul <- decompose(co2, type = "multiplicative")
ajustada_adi <- co2 - adi$seasonal
ajustada_mul <- co2 / mul$seasonal
print(round(max(abs(ajustada_adi - ajustada_mul)), 2))
print(round(c(aditiva        = sd(adi$random, na.rm = TRUE),
              multiplicativa = sd(co2 - mul$trend * mul$seasonal, na.rm = TRUE)), 3))
cat("--- fin del BLOQUE ---\n\n")

L("E1-05", "nivel medio 1959 = ", round(nivel["1959"], 2), " ; 1997 = ", round(nivel["1997"], 2),
  " ; variacion = +", round(100 * (nivel["1997"] / nivel["1959"] - 1), 1), " % en ", length(nivel), " anios")
L("E1-06", "amplitud 1959 = ", round(amplitud["1959"], 2), " ; 1997 = ", round(amplitud["1997"], 2),
  " ; variacion = +", round(100 * (amplitud["1997"] / amplitud["1959"] - 1), 1), " % ; diferencia = ",
  round(amplitud["1997"] - amplitud["1959"], 2), " ppm")
L("E1-07", "amplitud/nivel: minimo ", round(min(100 * amplitud / nivel), 2), " % (", names(which.min(amplitud / nivel)),
  ") ; maximo ", round(max(100 * amplitud / nivel), 2), " % (", names(which.max(amplitud / nivel)), ")")
L("E1-08", "recorrido total de la serie frente a su media: (max - min)/media = ",
  round((max(co2) - min(co2)) / mean(co2), 3))
ic <- confint(ajuste)[2, ]
L("E1-09", "b = ", round(coef(ajuste)[[2]], 3), " ; IC95 [", round(ic[1], 3), ", ", round(ic[2], 3), "] ; R2 = ",
  round(summary(ajuste)$r.squared, 3), " ; excluye el 0: ", ic[1] > 0, " ; contiene el 1: ", ic[1] < 1 && ic[2] > 1)

cat("\n--- la amplitud del CO2 crece, y al ritmo que predice la proporcionalidad ---\n")
yrs <- as.numeric(names(nivel))
f1 <- summary(lm(amplitud ~ yrs))$coefficients
L("E1-10", "amplitud ~ anio: pendiente ", sprintf("%+.4f", f1[2, 1]), " ppm/anio ; p = ", signif(f1[2, 4], 2))
c0 <- mean(amplitud) / mean(nivel)
L("E1-11", "si amplitud = c x nivel con c = media(amplitud)/media(nivel) = ", round(c0, 5),
  ": pendiente ", sprintf("%+.4f", coef(lm(I(c0 * nivel) ~ yrs))[2]), " ppm/anio")
f2 <- summary(lm(I(amplitud / nivel) ~ yrs))$coefficients
L("E1-12", "(amplitud/nivel) ~ anio: pendiente ", signif(f2[2, 1], 2), " ; p = ", round(f2[2, 4], 2))

cat("\n--- (c) las dos descomposiciones clasicas, en detalle ---\n")
L("E1-13", "componente estacional ADITIVO (ppm), ene..dic: ", paste(sprintf("%+.2f", adi$figure), collapse = " "))
L("E1-14", "  maximo ", sprintf("%+.2f", max(adi$figure)), " (mes ", which.max(adi$figure), ") ; minimo ",
  sprintf("%+.2f", min(adi$figure)), " (mes ", which.min(adi$figure), ") ; vaiven (max - min) = ",
  round(diff(range(adi$figure)), 2), " ppm")
L("E1-15", "indices MULTIPLICATIVOS, ene..dic: ", paste(sprintf("%.4f", mul$figure), collapse = " "))
L("E1-16", "  vaiven que implican (rango de indices x nivel): 1959 ", round(diff(range(mul$figure)) * nivel["1959"], 2),
  " ppm ; 1997 ", round(diff(range(mul$figure)) * nivel["1997"], 2), " ppm")
dif <- abs(ajustada_adi - ajustada_mul)
L("E1-17", "max |ajustada aditiva - ajustada multiplicativa| = ", round(max(dif), 2), " ppm, en ",
  paste(floor(time(co2)[which.max(dif)]), cycle(co2)[which.max(dif)], sep = "-"),
  " ; media de esa diferencia = ", round(mean(dif), 2), " ppm")
L("E1-18", "esa diferencia maxima, como fraccion del vaiven aditivo: ", round(100 * max(dif) / diff(range(adi$figure)), 1), " %")
L("E1-19", "sd del residuo: aditiva ", round(sd(adi$random, na.rm = TRUE), 3), " ppm ; multiplicativa (y - T x S) ",
  round(sd(co2 - mul$trend * mul$seasonal, na.rm = TRUE), 3), " ppm")
sd_a <- tapply(adi$random, anio_de(co2), sd, na.rm = TRUE)
sd_m <- tapply(co2 - mul$trend * mul$seasonal, anio_de(co2), sd, na.rm = TRUE)
L("E1-20", "sd anual del residuo aditivo: 1959-1964 media ", round(mean(sd_a[1:6]), 3), " ; 1975-1981 media ",
  round(mean(sd_a[as.character(1975:1981)]), 3), " ; 1992-1997 media ", round(mean(sd_a[34:39]), 3))
L("E1-21", "sd anual del residuo multiplicativo: 1959-1964 media ", round(mean(sd_m[1:6]), 3), " ; 1975-1981 media ",
  round(mean(sd_m[as.character(1975:1981)]), 3), " ; 1992-1997 media ", round(mean(sd_m[34:39]), 3))

cat("\n--- la misma cuenta en AirPassengers, como referencia de escala ---\n")
elasticidad <- function(x) {
  a <- anio_de(x); niv <- tapply(x, a, mean); amp <- tapply(x, a, function(z) max(z) - min(z))
  fit <- lm(log(amp) ~ log(niv))
  c(b = coef(fit)[[2]], confint(fit)[2, ], R2 = summary(fit)$r.squared)
}
eap <- elasticidad(AirPassengers)
L("E1-22", "AirPassengers: b = ", round(eap[1], 3), " ; IC95 [", round(eap[2], 3), ", ", round(eap[3], 3), "] ; R2 = ", round(eap[4], 3))
nap <- tapply(AirPassengers, anio_de(AirPassengers), mean)
L("E1-23", "AirPassengers: nivel medio ", round(nap[1], 1), " -> ", round(nap[12], 1), " = x", round(nap[12] / nap[1], 2))
apa <- decompose(AirPassengers, "additive"); apm <- decompose(AirPassengers, "multiplicative")
dap <- abs((AirPassengers - apa$seasonal) - AirPassengers / apm$seasonal)
L("E1-24", "AirPassengers: max |ajustada aditiva - multiplicativa| = ", round(max(dap), 1), " mil ; vaiven aditivo = ",
  round(diff(range(apa$figure)), 1), " mil ; fraccion = ", round(100 * max(dap) / diff(range(apa$figure)), 1), " %")

cat("\n--- STL con ventana estacional finita tambien recoge el crecimiento de la amplitud ---\n")
s11 <- stl(co2, s.window = 11)$time.series[, "seasonal"]
a11 <- tapply(s11, anio_de(co2), function(z) max(z) - min(z))
L("E1-25", "stl(co2, s.window = 11): vaiven del componente estacional 1959 = ", round(a11["1959"], 2),
  " ppm ; 1997 = ", round(a11["1997"], 2), " ppm")

# ===========================================================================
titulo("E2 · Ejercicio 2: F_T y F_S, cuatro casos y el efecto de la escala")
# ===========================================================================
cat("--- BLOQUE de la solucion, tal como va en el capitulo ---\n")
fuerzas <- function(x) {
  st <- stl(x, s.window = "periodic")$time.series
  Tt <- st[, "trend"]; St <- st[, "seasonal"]; Rt <- st[, "remainder"]
  c(FT = max(0, 1 - var(Rt) / var(Tt + Rt)),
    FS = max(0, 1 - var(Rt) / var(St + Rt)))
}
print(round(rbind(nottem               = fuerzas(nottem),
                  USAccDeaths          = fuerzas(USAccDeaths),
                  "log(AirPassengers)" = fuerzas(log(AirPassengers)),
                  AirPassengers        = fuerzas(AirPassengers)), 3))

# El residuo de la STL sin logaritmo: su dispersion, anio por anio
st <- stl(AirPassengers, s.window = "periodic")$time.series
print(round(tapply(st[, "remainder"], floor(time(AirPassengers)), sd), 1))
cat("--- fin del BLOQUE ---\n\n")

partes <- function(x) {
  st <- stl(x, s.window = "periodic")$time.series
  Tt <- st[, "trend"]; St <- st[, "seasonal"]; Rt <- st[, "remainder"]
  c(VarR = var(Rt), VarTR = var(Tt + Rt), VarSR = var(St + Rt),
    FT = max(0, 1 - var(Rt) / var(Tt + Rt)), FS = max(0, 1 - var(Rt) / var(St + Rt)))
}
casos <- list(nottem = nottem, USAccDeaths = USAccDeaths, "log(AirPassengers)" = log(AirPassengers),
              AirPassengers = AirPassengers, co2 = co2)
for (nm in names(casos)) {
  p <- partes(casos[[nm]])
  L(paste0("E2-", sprintf("%02d", match(nm, names(casos)))), sprintf("%-19s Var(R) = %-10s Var(T+R) = %-10s Var(S+R) = %-10s F_T = %.4f  F_S = %.4f  Var(R)/Var(S+R) = %.3f",
    nm, signif(p["VarR"], 4), signif(p["VarTR"], 4), signif(p["VarSR"], 4), p["FT"], p["FS"], p["VarR"] / p["VarSR"]))
}
L("E2-06", "nottem: n = ", length(nottem), ", de ", paste(start(nottem), collapse = "-"), " a ", paste(end(nottem), collapse = "-"),
  " ; medias anuales entre ", round(min(tapply(nottem, anio_de(nottem), mean)), 1), " y ",
  round(max(tapply(nottem, anio_de(nottem), mean)), 1), " grados F")
L("E2-07", "USAccDeaths: n = ", length(USAccDeaths), ", de ", paste(start(USAccDeaths), collapse = "-"), " a ",
  paste(end(USAccDeaths), collapse = "-"), " ; medias anuales: ",
  paste(names(tapply(USAccDeaths, anio_de(USAccDeaths), mean)), round(tapply(USAccDeaths, anio_de(USAccDeaths), mean)), sep = ":", collapse = "  "))
sdl <- tapply(stl(log(AirPassengers), s.window = "periodic")$time.series[, "remainder"], anio_de(AirPassengers), sd)
sdr <- tapply(st[, "remainder"], anio_de(AirPassengers), sd)
L("E2-08", "sd anual del residuo, STL SIN logaritmo: ", paste(names(sdr), sprintf("%.1f", sdr), sep = ":", collapse = "  "))
L("E2-09", "  maximo/minimo de esas doce = ", round(max(sdr) / min(sdr), 1), " (minimo en ", names(which.min(sdr)), ")")
L("E2-10", "sd anual del residuo, STL CON logaritmo: ", paste(names(sdl), sprintf("%.4f", sdl), sep = ":", collapse = "  "))
L("E2-11", "  maximo/minimo de esas doce = ", round(max(sdl) / min(sdl), 1), " (minimo en ", names(which.min(sdl)), ")")
set.seed(20261114)
L("E2-12", "(referencia ya publicada en el Modulo 8, no recalculada aqui: ruido puro 0.12 / 0.08, de r3b_cifras.out, l. 70; sunspots 0.907 / 0.005)")

# ===========================================================================
titulo("E3 · Ejercicio 3: un atipico en mitad de la serie y otro al final")
# ===========================================================================
cat("--- BLOQUE de la solucion, tal como va en el capitulo ---\n")
contamina <- function(pos) { x <- AirPassengers; x[pos] <- 1.5 * x[pos]; x }

julio_clasica <- function(x) decompose(x, type = "multiplicative")$figure[7]
julio_stl <- function(x, robusta) {
  s <- stl(log(x), s.window = "periodic", robust = robusta)$time.series[, "seasonal"]
  exp(s[7])
}
indices <- function(x) c(clasica     = julio_clasica(x),
                         stl         = julio_stl(x, robusta = FALSE),
                         stl_robusta = julio_stl(x, robusta = TRUE))

tabla <- rbind(limpia   = indices(AirPassengers),
               jul_1955 = indices(contamina(79)),     # 364 -> 546
               jul_1960 = indices(contamina(139)))    # 622 -> 933
print(round(tabla, 4))

# Distorsion de cada metodo frente a SU propia linea base, en %
print(round(100 * (sweep(tabla[-1, ], 2, tabla["limpia", ], "/") - 1), 2))

# Que ve la clasica en el ultimo julio: ni tendencia ni residuo
final <- decompose(contamina(139), type = "multiplicative")
print(c(tendencia = final$trend[139], residuo = final$random[139]))
cat("--- fin del BLOQUE ---\n\n")

L("E3-01", "obs. 79 = ", paste(floor(time(AirPassengers)[79]), cycle(AirPassengers)[79], sep = "-"), ", valor ", AirPassengers[79],
  " -> ", contamina(79)[79], " ; obs. 139 = ", paste(floor(time(AirPassengers)[139]), cycle(AirPassengers)[139], sep = "-"),
  ", valor ", AirPassengers[139], " -> ", contamina(139)[139])
L("E3-02", "la opcion robusta sobre la serie LIMPIA: julio ", round(tabla["limpia", "stl"], 4), " -> ",
  round(tabla["limpia", "stl_robusta"], 4), " = ", sprintf("%+.2f", 100 * (tabla["limpia", "stl_robusta"] / tabla["limpia", "stl"] - 1)), " %")
L("E3-03", "clasica: |distorsion| en el centro / al final = ", round(4.02 / 0.21, 0), " veces (con las cifras redondeadas de la tabla) ; exacto ",
  round((tabla["jul_1955", "clasica"] / tabla["limpia", "clasica"] - 1) / (tabla["jul_1960", "clasica"] / tabla["limpia", "clasica"] - 1), 1))
L("E3-04", "en el centro, |clasica| / |STL robusta| = ",
  round(abs(tabla["jul_1955", "clasica"] / tabla["limpia", "clasica"] - 1) / abs(tabla["jul_1955", "stl_robusta"] / tabla["limpia", "stl_robusta"] - 1), 1))

cat("\n--- por que la clasica casi no se mueve con el atipico al final ---\n")
lim <- decompose(AirPassengers, type = "multiplicative")
L("E3-05", "tendencia clasica: primera obs. con valor = ", min(which(!is.na(lim$trend))), " ; ultima = ", max(which(!is.na(lim$trend))),
  " ; NA = ", sum(is.na(lim$trend)), " (", paste(which(is.na(lim$trend)), collapse = " "), ")")
L("E3-06", "julios con tendencia (los que entran en el indice de julio): ",
  paste(floor(time(AirPassengers))[cycle(AirPassengers) == 7 & !is.na(lim$trend)], collapse = " "),
  " -> ", sum(cycle(AirPassengers) == 7 & !is.na(lim$trend)), " de 12")
dt <- final$trend - lim$trend
L("E3-07", "cambio de la tendencia clasica al contaminar julio de 1960 (obs. con cambio): ",
  paste(which(abs(dt) > 1e-9), sprintf("%+.2f", dt[which(abs(dt) > 1e-9)]), sep = ":", collapse = "  "))
L("E3-08", "cambio de los doce indices clasicos, en %, ene..dic: ",
  paste(sprintf("%+.2f", 100 * (final$figure / lim$figure - 1)), collapse = " "))
cen <- decompose(contamina(79), type = "multiplicative")
L("E3-09", "y con el atipico en el centro (obs. 79), ene..dic: ",
  paste(sprintf("%+.2f", 100 * (cen$figure / lim$figure - 1)), collapse = " "),
  " ; residuo clasico de esa obs. = ", round(cen$random[79], 4), " (limpio ", round(lim$random[79], 4), ")")

cat("\n--- que hace STL con cada atipico ---\n")
for (pos in c(79, 139)) for (rb in c(FALSE, TRUE)) {
  s1 <- stl(log(contamina(pos)), s.window = "periodic", robust = rb)
  s0 <- stl(log(AirPassengers), s.window = "periodic", robust = rb)
  L(sprintf("E3-1%d", match(paste(pos, rb), c("79 FALSE", "79 TRUE", "139 FALSE", "139 TRUE")) - 1),
    sprintf("obs. %d, robust = %-5s: residuo %.4f (limpio %.4f) ; tendencia %.1f mil (limpia %.1f) ; peso de la obs. = %s ; obs. con peso 0 = %d",
      pos, rb, s1$time.series[pos, "remainder"], s0$time.series[pos, "remainder"],
      exp(s1$time.series[pos, "trend"]), exp(s0$time.series[pos, "trend"]),
      format(round(s1$weights[pos], 4)), sum(s1$weights == 0)))
}
w0 <- stl(log(AirPassengers), s.window = "periodic", robust = TRUE)$weights
L("E3-13b", "ajuste robusto sobre la serie LIMPIA: obs. con peso 0 = ", sum(w0 == 0), " ; con peso menor que 0.5 = ", sum(w0 < 0.5))
r0 <- stl(log(AirPassengers), s.window = "periodic", robust = TRUE)$time.series
r1 <- stl(log(contamina(79)), s.window = "periodic", robust = TRUE)$time.series
n0 <- stl(log(AirPassengers), s.window = "periodic")$time.series
L("E3-13c", "julio de 1955 (obs. 79), para el parrafo del Modulo 7. SIN robustez, serie limpia: julio ", sprintf("%+.1f", 100 * (exp(n0[7, "seasonal"]) - 1)),
  " % y tendencia ", sprintf("%.1f", exp(n0[79, "trend"])), " mil. CON robustez, serie limpia (su linea base): julio ",
  sprintf("%+.1f", 100 * (exp(r0[7, "seasonal"]) - 1)), " % y tendencia ", sprintf("%.1f", exp(r0[79, "trend"])),
  " mil. CON robustez, julio inflado: julio ", sprintf("%+.1f", 100 * (exp(r1[7, "seasonal"]) - 1)), " % y tendencia ",
  sprintf("%.1f", exp(r1[79, "trend"])), " mil ; residuo ", sprintf("%.4f", r1[79, "remainder"]))
L("E3-13d", "  el indice robusto contaminado frente a su propia linea base: ", sprintf("%+.2f", 100 * (exp(r1[7, "seasonal"]) / exp(r0[7, "seasonal"]) - 1)),
  " % ; frente a la linea base NO robusta (la comparacion que no vale): ", sprintf("%+.2f", 100 * (exp(r1[7, "seasonal"]) / exp(n0[7, "seasonal"]) - 1)), " %")
L("E3-14", "valor por defecto de `robust` en stl(): ", deparse(formals(stl)$robust))

# ===========================================================================
titulo("Q2 · Quiz, pregunta 2: Gas de aus_production (tsibbledata)")
# ===========================================================================
ayuda <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("aus_production", package = "tsibbledata"))))
ayuda <- gsub("_\b", "", ayuda)
cat(paste0("[Q2-00] ?aus_production | ", ayuda[nzchar(trimws(ayuda))]), sep = "\n")
gas <- ts(aus_production$Gas, start = c(1956, 1), frequency = 4)
L("Q2-01", "Gas: n = ", length(gas), ", trimestral, de ", paste(start(gas), collapse = "-T"), " a ", paste(end(gas), collapse = "-T"),
  " ; NA = ", sum(is.na(gas)), " ; primera fila del tsibble: ", format(aus_production$Quarter[1]),
  " ; ultima: ", format(aus_production$Quarter[nrow(aus_production)]))
ag <- anio_de(gas); comp <- names(which(table(ag) == 4))
niv_g <- tapply(gas, ag, mean)[comp]; amp_g <- tapply(gas, ag, function(z) max(z) - min(z))[comp]
for (a in c("1960", "1975", "1990", "2005"))
  L(paste0("Q2-", sprintf("%02d", 1 + match(a, c("1960", "1975", "1990", "2005")))),
    a, ": trimestres ", paste(gas[ag == as.numeric(a)], collapse = " "), " ; nivel medio = ", niv_g[a], " ; amplitud = ", amp_g[a],
    " ; amplitud/nivel = ", sprintf("%.1f", 100 * amp_g[a] / niv_g[a]), " %")
L("Q2-06", "de 1960 a 2005: el nivel se multiplica por ", round(niv_g["2005"] / niv_g["1960"], 1),
  " y la amplitud por ", round(amp_g["2005"] / amp_g["1960"], 1))
L("Q2-07", "incrementos de la amplitud entre filas: ", paste(diff(amp_g[c("1960", "1975", "1990", "2005")]), collapse = ", "))
fg <- lm(log(amp_g) ~ log(niv_g))
L("Q2-08", "con los ", length(comp), " anios completos: b = ", round(coef(fg)[[2]], 3), " ; IC95 [",
  round(confint(fg)[2, 1], 3), ", ", round(confint(fg)[2, 2], 3), "] ; R2 = ", round(summary(fg)$r.squared, 3))
ga <- decompose(gas, "additive")
L("Q2-09", "clasica ADITIVA de Gas: componente estacional T1..T4 = ", paste(sprintf("%+.2f", ga$figure), collapse = " "),
  " ; vaiven fijo = ", round(diff(range(ga$figure)), 1), " PJ")
sdg <- tapply(ga$random, ag, sd, na.rm = TRUE)
L("Q2-10", "sd anual del residuo aditivo de Gas: 1960 = ", round(sdg["1960"], 1), " ; 1975 = ", round(sdg["1975"], 1),
  " ; 1985 = ", round(sdg["1985"], 1), " ; 1990 = ", round(sdg["1990"], 1), " ; 2005 = ", round(sdg["2005"], 1),
  " ; minimo = ", round(min(sdg, na.rm = TRUE), 1), " (", names(which.min(sdg)), ")")
L("Q2-10b", "  en los cuatro anios de la tabla del enunciado: ", paste(c("1960", "1975", "1990", "2005"), sprintf("%.1f", sdg[c("1960", "1975", "1990", "2005")]), sep = " = ", collapse = " ; "))
cat("[Q2-11] sd anual del residuo aditivo de Gas, serie completa:\n"); print(round(sdg, 1))
ap_adi <- decompose(AirPassengers, "additive")
sdu <- tapply(ap_adi$random, anio_de(AirPassengers), sd, na.rm = TRUE)
L("Q2-12", "la U del Modulo 6 (sd anual del residuo ADITIVO de AirPassengers): ",
  paste(names(sdu), sprintf("%.1f", sdu), sep = ":", collapse = "  "))
L("Q2-13", "  1949 = ", sprintf("%.1f", sdu["1949"]), " ; minimo = ", sprintf("%.1f", min(sdu)), " (", names(which.min(sdu)),
  ") ; 1960 = ", sprintf("%.1f", sdu["1960"]))

# ===========================================================================
titulo("Q3 · Quiz, pregunta 3: los pesos de la media movil 2x4")
# ===========================================================================
ma4a <- c(1, 1, 1, 1, 0) / 4; ma4b <- c(0, 1, 1, 1, 1) / 4
L("Q3-01", "promedio de dos ventanas de 4 seguidas: pesos = ", paste((ma4a + ma4b) / 2, collapse = " "),
  " ; suman ", sum((ma4a + ma4b) / 2))
L("Q3-02", "filtro que usa decompose() con frecuencia 4, c(0.5, rep(1, 3), 0.5)/4 = ", paste(c(0.5, rep(1, 3), 0.5) / 4, collapse = " "))
du <- decompose(UKgas)
fm <- stats::filter(UKgas, c(0.5, 1, 1, 1, 0.5) / 4)
L("Q3-03", "decompose(UKgas)$trend coincide con ese filtro: ", isTRUE(all.equal(as.numeric(du$trend), as.numeric(fm))),
  " ; UKgas: n = ", length(UKgas), " trimestres ; NA en la tendencia = ", sum(is.na(du$trend)))
L("Q3-04", "peso total de cada trimestre del anio dentro de la ventana: el de los dos extremos (el mismo trimestre, a un anio de distancia) ",
  2 * 0.125, " ; cada uno de los otros tres ", 0.25)
L("Q3-04b", "tolerancia: |0.13 - 0.125| = ", format(abs(0.13 - 0.125), digits = 17), " -> mayor que 0.005: ", abs(0.13 - 0.125) > 0.005,
  " ; menor o igual que 0.0051: ", abs(0.13 - 0.125) <= 0.0051, " ; con 0.0051 siguen fuera 0.25, 0.2, 0.042 y 12.5: ",
  all(abs(c(0.25, 0.2, 0.042, 12.5) - 0.125) > 0.0051), " ; 1/8 = ", 1 / 8)
L("Q3-05", "respuestas equivocadas que la retroalimentacion diagnostica: 1/4 = ", 1 / 4, " ; 1/5 = ", 1 / 5,
  " ; 1/24 = ", round(1 / 24, 4), " ; correcta 1/8 = ", 1 / 8)
L("Q3-06", "comprobacion de que la 2x4 borra un patron trimestral que suma cero sobre una recta: ",
  isTRUE(all.equal(as.numeric(na.omit(stats::filter(ts(10 + 2 * (1:24) + rep(c(5, -3, -4, 2), 6), frequency = 4), c(0.5, 1, 1, 1, 0.5) / 4))),
                   10 + 2 * (3:22))))

# ===========================================================================
titulo("Q4 · Quiz, pregunta 4: los huecos de la tendencia clasica")
# ===========================================================================
L("Q4-01", "sum(is.na(decompose(AirPassengers)$trend)) = ", sum(is.na(decompose(AirPassengers)$trend)),
  " ; posiciones: ", paste(which(is.na(decompose(AirPassengers)$trend)), collapse = " "),
  " ; valores de tendencia = ", sum(!is.na(decompose(AirPassengers)$trend)), " de ", length(AirPassengers))
un_lado <- stats::filter(AirPassengers, rep(1 / 12, 12), sides = 1)
L("Q4-02", "media de los doce meses ANTERIORES (un solo lado): NA = ", sum(is.na(un_lado)), " ; posiciones: ",
  paste(which(is.na(un_lado)), collapse = " "), " ; ultimo valor disponible en la obs. ", max(which(!is.na(un_lado))))

# ===========================================================================
titulo("Q5 · Quiz, pregunta 5: lo que STL necesita y lo que no")
# ===========================================================================
err <- tryCatch(stl(ts(as.numeric(AirPassengers)), s.window = "periodic"), error = function(e) conditionMessage(e))
L("Q5-01", "stl() sobre la misma serie sin frecuencia declarada (ts de frecuencia 1) -> error: «", err, "»")
sp <- stl(log(AirPassengers), s.window = "periodic")$time.series
L("Q5-02", "tendencia de STL: NA = ", sum(is.na(sp[, "trend"])), " de ", nrow(sp), " ; tendencia clasica: valores = ",
  sum(!is.na(decompose(AirPassengers)$trend)))
s11ap <- exp(stl(log(AirPassengers), s.window = 11)$time.series[, "seasonal"])
L("Q5-02b", "stl(log(AirPassengers), s.window = 11): julio de 1949 = ", sprintf("%+.1f", 100 * (s11ap[7] - 1)),
  " % ; julio de 1960 = ", sprintf("%+.1f", 100 * (s11ap[139] - 1)), " % (las cifras del Modulo 7 que cita la retro)")
r79 <- stl(log(contamina(79)), s.window = "periodic", robust = TRUE)
L("Q5-02c", "julio de 1955 inflado, robust = TRUE: peso = ", r79$weights[79], " ; julio estacional = ",
  sprintf("%+.1f", 100 * (exp(r79$time.series[7, "seasonal"]) - 1)), " % (sin atipico y sin robustez: ",
  sprintf("%+.1f", 100 * (exp(sp[7, "seasonal"]) - 1)), " %)")
L("Q5-03", "(las fuerzas con y sin logaritmo de la retro de la opcion «evita transformar» salen de E2-03 y E2-04)")

# ===========================================================================
titulo("Q6 · Quiz, pregunta 6: tres descomposiciones y sus varianzas")
# ===========================================================================
cuatro <- c("USAccDeaths", "log(AirPassengers)", "co2", "nottem")
for (nm in cuatro) {
  p <- partes(casos[[nm]])
  L(paste0("Q6-", sprintf("%02d", match(nm, cuatro))),
    sprintf("%-19s Var(R) = %-12s Var(T+R) = %-12s Var(R)/Var(T+R) = %.5f   F_T = %.4f",
      nm, format(signif(p["VarR"], if (nm == "nottem") 5 else 4), scientific = FALSE),
      format(signif(p["VarTR"], if (nm == "nottem") 5 else 4), scientific = FALSE),
      p["VarR"] / p["VarTR"], p["FT"]))
}
vr <- sapply(cuatro, function(nm) partes(casos[[nm]]))
L("Q6-07", "mayor Var(T+R): ", colnames(vr)[which.max(vr["VarTR", ])], " ; menor Var(R): ", colnames(vr)[which.min(vr["VarR", ])],
  " ; mayor F_T: ", colnames(vr)[which.max(vr["FT", ])], " ; menor F_T: ", colnames(vr)[which.min(vr["FT", ])])
L("Q6-04b", "con las cifras TAL COMO las ve el estudiante: 44960/223800 = ", round(44960 / 223800, 3), " -> ", round(1 - 44960 / 223800, 3),
  " ; 0.001074/0.1793 = ", round(0.001074 / 0.1793, 4), " -> ", round(1 - 0.001074 / 0.1793, 3),
  " ; 0.06768/220.7 = ", round(0.06768 / 220.7, 4), " -> ", round(1 - 0.06768 / 220.7, 4),
  " ; 4.0613/5.1117 = ", round(4.0613 / 5.1117, 3), " -> ", round(1 - 4.0613 / 5.1117, 3))
L("Q6-05", "insumos del item antiguo (0.0012 y 0.20) frente a los reales de log(AirPassengers): Var(R) = ",
  signif(vr["VarR", "log(AirPassengers)"], 4), " ; Var(T+R) = ", signif(vr["VarTR", "log(AirPassengers)"], 4))
L("Q6-06", "unidades: USAccDeaths en muertes, co2 en ppm, log(AirPassengers) sin unidad; las varianzas, en esas unidades al cuadrado")

# ===========================================================================
titulo("Q7 · Quiz, pregunta 7: fuerzas altas no validan la descomposicion")
# ===========================================================================
pr <- partes(AirPassengers); pl <- partes(log(AirPassengers))
L("Q7-01", "log(AirPassengers): F_T = ", round(pl["FT"], 3), " ; F_S = ", round(pl["FS"], 3))
L("Q7-02", "AirPassengers sin logaritmo: F_T = ", round(pr["FT"], 3), " ; F_S = ", round(pr["FS"], 3))
L("Q7-03", "sd anual del residuo de esa STL sin logaritmo: 1949 = ", sprintf("%.1f", sdr["1949"]), " ; minimo = ",
  sprintf("%.1f", min(sdr)), " (", names(which.min(sdr)), ") ; 1960 = ", sprintf("%.1f", sdr["1960"]))

titulo("Fin")
