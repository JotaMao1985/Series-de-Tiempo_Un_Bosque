# R5 · practica · capitulo 1 · segundo encargo
# ---------------------------------------------------------------------------
# Un solo guion para TODAS las cifras de los cinco ejercicios cortos de modulo
# (M2, M3, M6, M7 y M8).
#
# Uso (desde la raiz del repo):
#   Rscript --vanilla diagnostico/cap1/comprobaciones/r5_ejercicios_cortos.R \
#     > diagnostico/cap1/comprobaciones/r5_ejercicios_cortos.out 2>&1
#
# Cada linea de la salida lleva una etiqueta entre corchetes ([M6-03]...) y
# `diagnostico/cap1/R5_cambios.md` dice de que etiqueta sale cada cifra. Las
# secciones «BLOQUE» ejecutan el codigo que el capitulo publica en cada
# solucion (alli sin print(): R imprime solo); su salida es la que el capitulo
# copia tras `#>`.
#
# Las cuatro series (UKgas, nottem, mdeaths, fdeaths) son de `datasets`: el
# guion no pide red en ningun momento.
# ---------------------------------------------------------------------------
options(width = 80, warn = 1)
suppressMessages(library(fpp3))

L <- function(etq, ...) cat(sprintf("[%s] ", etq), ..., "\n", sep = "")
titulo <- function(x) cat("\n", strrep("=", 76), "\n", x, "\n", strrep("=", 76), "\n", sep = "")
anio_de <- function(x) floor(time(x) + 1e-6)

titulo("0 · Entorno y series")
L("ENT-01", R.version.string)
L("ENT-02", "fpp3 ", as.character(packageVersion("fpp3")), " · tsibble ", as.character(packageVersion("tsibble")),
  " · feasts ", as.character(packageVersion("feasts")), " · ggtime ", as.character(packageVersion("ggtime")))
L("ENT-03", "locale: ", Sys.getlocale())
for (nm in c("UKgas", "nottem", "mdeaths", "fdeaths"))
  L("ENT-04", nm, ": paquete ", sub("package:", "", grep("datasets", find(nm), value = TRUE)),
    " ; n = ", length(get(nm)), " ; frecuencia ", frequency(get(nm)), " ; de ",
    paste(start(get(nm)), collapse = "-"), " a ", paste(end(get(nm)), collapse = "-"))
cat("\n--- que es cada serie, segun la ayuda de R ---\n")
for (nm in c("UKgas", "nottem", "UKLungDeaths")) {
  h <- gsub("_\b", "", capture.output(tools::Rd2txt(utils:::.getHelpFile(help(nm, package = "datasets")))))
  h <- h[nzchar(trimws(h))]
  fin <- which(grepl("^(Usage|Format):", h))[1]
  cat(paste0("[ENT-05 ?", nm, "] ", h[seq_len(fin - 1)]), sep = "\n")
}

# ===========================================================================
titulo("M2 · construir el objeto: indice, intervalo y clave (mdeaths + fdeaths)")
# ===========================================================================
cat("--- BLOQUE del enunciado: la tabla cruda ---\n")
meses <- seq(as.Date("1974-01-01"), by = "month",
             length.out = 72)
crudo <- data.frame(
  mes     = rep(meses, times = 2),
  sexo    = rep(c("hombres", "mujeres"), each = 72),
  muertes = c(mdeaths, fdeaths)
)
cat("--- BLOQUE de la solucion ---\n")
# (a) Solo el indice
try(as_tsibble(crudo, index = mes))
print(nrow(duplicates(crudo, index = mes)))
print(nrow(duplicates(crudo, index = mes, key = sexo)))

# (b) Indice y clave, con `mes` todavia como fecha de dia
diario <- as_tsibble(crudo, index = mes, key = sexo)
print(diario, n = 2)
print(has_gaps(diario)$.gaps)

# (c) El mes, declarado como mes
muertes <- crudo |>
  mutate(mes = yearmonth(mes)) |>
  as_tsibble(index = mes, key = sexo)
print(muertes, n = 2)
print(has_gaps(muertes)$.gaps)
cat("--- fin del BLOQUE ---\n\n")

cat("--- la misma salida en una sesion UTF-8 (la de RStudio), que es la que copia el capitulo ---\n")
orden <- paste(
  "suppressMessages(library(fpp3))",
  "crudo <- data.frame(mes = rep(seq(as.Date('1974-01-01'), by = 'month', length.out = 72), times = 2), sexo = rep(c('hombres', 'mujeres'), each = 72), muertes = c(mdeaths, fdeaths))",
  "try(as_tsibble(crudo, index = mes)); print(nrow(duplicates(crudo, index = mes))); print(nrow(duplicates(crudo, index = mes, key = sexo)))",
  "diario <- as_tsibble(crudo, index = mes, key = sexo); print(diario, n = 2); print(has_gaps(diario)$.gaps)",
  "muertes <- crudo |> mutate(mes = yearmonth(mes)) |> as_tsibble(index = mes, key = sexo); print(muertes, n = 2); print(has_gaps(muertes)$.gaps)",
  sep = "; ")
sal <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript"), c("--vanilla", "-e", shQuote(orden)),
                                env = "LC_ALL=en_US.UTF-8", stdout = TRUE, stderr = TRUE))
cat(paste0("[M2-00 en_US.UTF-8] ", sal), sep = "\n")

L("M2-01", "crudo: ", nrow(crudo), " filas x ", ncol(crudo), " columnas ; clase de `mes`: ", class(crudo$mes),
  " ; filas con mes == 1974-01-01: ", sum(crudo$mes == as.Date("1974-01-01")))
L("M2-02", "meses distintos: ", length(unique(crudo$mes)), " ; valores de `sexo`: ", paste(unique(crudo$sexo), collapse = ", "),
  " ; ", length(unique(crudo$mes)), " x ", length(unique(crudo$sexo)), " = ", length(unique(crudo$mes)) * length(unique(crudo$sexo)))
L("M2-03", "dias entre fechas consecutivas de `mes` (una serie): ", paste(sort(unique(as.numeric(diff(crudo$mes[1:72])))), collapse = ", "))
L("M2-04", "con [1D], dias que el objeto espera entre 1974-01-01 y 1979-12-01: ",
  as.numeric(as.Date("1979-12-01") - as.Date("1974-01-01")) + 1, " por serie ; hay ", 72)
L("M2-05", "intervalo de `diario`: ", format(interval(diario)), " ; de `muertes`: ", format(interval(muertes)))
ancho <- cbind(hombres = mdeaths, mujeres = fdeaths)
L("M2-06", "la via de R base: class(cbind(mdeaths, fdeaths)) = ", paste(class(ancho), collapse = " "),
  " ; frequency = ", frequency(ancho), " ; dim = ", paste(dim(ancho), collapse = " x "))
aviso <- tryCatch({ diario |> model(STL(muertes)); "sin aviso" }, warning = function(w) conditionMessage(w), error = function(e) conditionMessage(e))
L("M2-08", "una STL sobre `diario` (el objeto [1D]): ", gsub("\\s+", " ", aviso))
ok <- muertes |> model(STL(muertes))
L("M2-09", "la misma STL sobre `muertes` (el objeto [1M]): ", nrow(ok), " modelos ajustados, clase ", class(ok[[2]][[1]]$fit)[1])
L("M2-10", "duplicates(crudo, index = mes): clase ", class(duplicates(crudo, index = mes))[1], " ; filas ", nrow(duplicates(crudo, index = mes)),
  " de ", nrow(crudo), " ; con la clave: ", nrow(duplicates(crudo, index = mes, key = sexo)))
L("M2-11", "lo que nombra ahora la prosa del M2: clase del indice de as_tsibble(AirPassengers) = ", class(as_tsibble(AirPassengers)$index)[1],
  " ; intervalo = ", format(interval(as_tsibble(AirPassengers))), " ; existen yearmonth(), yearquarter() y yearweek(): ",
  exists("yearmonth"), " ", exists("yearquarter"), " ", exists("yearweek"),
  " ; yearmonth(as.Date('1974-01-01')) = ", format(yearmonth(as.Date("1974-01-01"))))
L("M2-07", "primer dato de cada serie: hombres ", mdeaths[1], " ; mujeres ", fdeaths[1])

# ===========================================================================
titulo("M3 · subseries y rezagos de nottem")
# ===========================================================================
cat("--- BLOQUE de la solucion ---\n")
temp <- as_tsibble(nottem)
pdf(NULL)
print(gg_subseries(temp, value))
print(gg_lag(temp, value, geom = "point", lags = 1:12))
invisible(dev.off())

# (a) Cada dato frente a la media de su mes
desvio <- nottem - ave(nottem, cycle(nottem))
i <- c(which.min(desvio), which.max(desvio))
print(data.frame(anio = floor(time(nottem))[i], mes = cycle(nottem)[i],
                 valor = nottem[i], desvio = round(desvio[i], 1)))

# (b) La correlacion de la nube en tres rezagos
n <- length(nottem)
nube <- function(k) cor(nottem[(k + 1):n], nottem[1:(n - k)])
print(round(sapply(c(3, 6, 12), nube), 3))
cat("--- fin del BLOQUE ---\n\n")

L("M3-01", "gg_subseries() y gg_lag() sobre nottem se dibujan sin error ni aviso (los avisos saldrian encima de esta linea)")
medias <- tapply(nottem, cycle(nottem), mean)
L("M3-02", "media de cada mes, ene..dic: ", paste(sprintf("%.1f", medias), collapse = " "))
L("M3-03", "minimo de toda la serie: ", min(nottem), " (obs. ", which.min(nottem), " = ", floor(time(nottem))[which.min(nottem)], "-",
  cycle(nottem)[which.min(nottem)], ") ; maximo: ", max(nottem), " ; recorrido ", max(nottem) - min(nottem))
L("M3-04", "febrero de 1929: ", nottem[110], " ; media de febrero ", sprintf("%.1f", medias[2]), " ; desvio ", sprintf("%+.1f", desvio[110]),
  " ; segundo febrero mas frio: ", sort(nottem[cycle(nottem) == 2])[2])
L("M3-05", "diciembre de 1934: ", nottem[180], " ; media de diciembre ", sprintf("%.1f", medias[12]), " ; desvio ", sprintf("%+.1f", desvio[180]),
  " ; media de abril ", sprintf("%.1f", medias[4]), " ; meses de la serie con valor entre 44.8 y 46.8: ", sum(nottem >= 44.8 & nottem <= 46.8))
L("M3-06", "los cinco desvios mas grandes en valor absoluto: ",
  paste(sapply(order(abs(desvio), decreasing = TRUE)[1:5], function(j) sprintf("%d-%d %+.1f", floor(time(nottem))[j], cycle(nottem)[j], desvio[j])), collapse = " ; "))
L("M3-07", "correlacion de la nube en los doce rezagos: ",
  paste(1:12, sprintf("%+.3f", sapply(1:12, function(k) cor(nottem[(k + 1):n], nottem[1:(n - k)]))), sep = ":", collapse = "  "))
L("M3-08", "medias anuales de nottem: minima ", sprintf("%.1f", min(tapply(nottem, anio_de(nottem), mean))), " ; maxima ",
  sprintf("%.1f", max(tapply(nottem, anio_de(nottem), mean))))
nap <- length(AirPassengers)
L("M3-09", "en AirPassengers (lo que dice el Modulo 3): rezago 6 = ", sprintf("%.3f", cor(AirPassengers[7:nap], AirPassengers[1:(nap - 6)])),
  " ; rezago 12 = ", sprintf("%.3f", cor(AirPassengers[13:nap], AirPassengers[1:(nap - 12)])))
L("M3-10", "pares de la nube: rezago 3 = ", n - 3, " ; rezago 6 = ", n - 6, " ; rezago 12 = ", n - 12)

# ===========================================================================
titulo("M6 · leer el residuo de UKgas y decidir a que paso volver")
# ===========================================================================
cat("--- BLOQUE de la solucion ---\n")
anio <- floor(time(UKgas))
tres <- c("1961", "1975", "1985")
sd_anual <- function(r, decimales) {
  round(tapply(r, anio, sd, na.rm = TRUE)[tres], decimales)
}

# (a) La clasica aditiva: dispersion del residuo en tres anios
adi <- decompose(UKgas, type = "additive")
print(sd_anual(adi$random, 1))

# (c) Paso 1 otra vez: multiplicativa. El residuo es un cociente
mul <- decompose(UKgas, type = "multiplicative")
print(sd_anual(mul$random, 3))

# El residuo multiplicativo del primer trimestre, cada 5 anios
t1 <- setNames(mul$random[cycle(UKgas) == 1], 1960:1986)
print(round(t1[c("1961", "1966", "1971", "1976", "1981", "1986")], 2))
cat("--- fin del BLOQUE ---\n\n")

L("M6-01", "UKgas: n = ", length(UKgas), " trimestres, de ", paste(start(UKgas), collapse = "-T"), " a ", paste(end(UKgas), collapse = "-T"),
  " ; residuos sin valor (NA): ", sum(is.na(adi$random)), " (obs. ", paste(which(is.na(adi$random)), collapse = " "), ")")
sda <- tapply(adi$random, anio_de(UKgas), sd, na.rm = TRUE)
cat("[M6-02] sd anual del residuo ADITIVO, 1960..1986:\n"); print(round(sda, 1))
L("M6-03", "  1960 = ", sprintf("%.1f", sda["1960"]), " ; 1975 = ", sprintf("%.1f", sda["1975"]), " ; 1986 = ", sprintf("%.1f", sda["1986"]),
  " ; minimo = ", sprintf("%.1f", min(sda)), " (", names(which.min(sda)), ") ; 1985/1975 = ", round(sda["1985"] / sda["1975"], 1),
  " ; 1961/1975 = ", round(sda["1961"] / sda["1975"], 1))
L("M6-04", "componente estacional aditivo, T1..T4: ", paste(sprintf("%+.1f", adi$figure), collapse = " "),
  " ; vaiven fijo = ", round(diff(range(adi$figure)), 1))
niv <- tapply(UKgas, anio_de(UKgas), mean); amp <- tapply(UKgas, anio_de(UKgas), function(z) max(z) - min(z))
L("M6-05", "nivel medio y amplitud: 1961 = ", sprintf("%.1f", niv["1961"]), " / ", sprintf("%.1f", amp["1961"]), " ; 1975 = ",
  sprintf("%.1f", niv["1975"]), " / ", sprintf("%.1f", amp["1975"]), " ; 1985 = ", sprintf("%.1f", niv["1985"]), " / ", sprintf("%.1f", amp["1985"]))
r1 <- setNames(adi$random[cycle(UKgas) == 1], 1960:1986)
L("M6-06", "residuo ADITIVO del primer trimestre: 1961 = ", sprintf("%+.0f", r1["1961"]), " ; 1975 = ", sprintf("%+.0f", r1["1975"]),
  " ; 1985 = ", sprintf("%+.0f", r1["1985"]), " ; negativos hasta ", max(as.numeric(names(r1))[!is.na(r1) & r1 < 0 & as.numeric(names(r1)) < 1976]),
  " ; n.o de negativos 1961-1975: ", sum(r1[as.character(1961:1975)] < 0), " de 15 ; n.o de positivos 1978-1986: ", sum(r1[as.character(1978:1986)] > 0), " de 9")
sdm <- tapply(UKgas - mul$trend * mul$seasonal, anio_de(UKgas), sd, na.rm = TRUE)
cat("[M6-07] sd anual del residuo MULTIPLICATIVO en unidades (y - T x S), 1960..1986:\n"); print(round(sdm, 1))
L("M6-08", "  aditiva / multiplicativa: 1961 = ", round(sda["1961"] / sdm["1961"], 1), " veces ; 1975 = ", round(sda["1975"] / sdm["1975"], 2),
  " ; 1985 = ", round(sda["1985"] / sdm["1985"], 2))
L("M6-08b", "  residuo multiplicativo en unidades, 1985 / 1975 = ", round(sdm["1985"] / sdm["1975"], 1), " veces")
sdc <- tapply(mul$random, anio_de(UKgas), sd, na.rm = TRUE)
cat("[M6-09] sd anual del residuo MULTIPLICATIVO como cociente, 1960..1986:\n"); print(round(sdc, 3))
L("M6-09b", "  como cociente: 1961 = ", sprintf("%.3f", sdc["1961"]), " ; 1975 = ", sprintf("%.3f", sdc["1975"]), " ; 1985 = ", sprintf("%.3f", sdc["1985"]),
  " ; 1985/1975 = ", round(sdc["1985"] / sdc["1975"], 1), " veces (en la aditiva, ", round(sda["1985"] / sda["1975"], 1), ")")
L("M6-10", "  de los 27 anios, entre 0.16 y 0.24: ", sum(sdc >= 0.16 & sdc <= 0.24), " ; 1970 = ", sprintf("%.3f", sdc["1970"]),
  " ; minimo = ", sprintf("%.3f", min(sdc)), " (", names(which.min(sdc)), ")")
L("M6-11", "indices multiplicativos, T1..T4: ", paste(sprintf("%.3f", mul$figure), collapse = " "))
cat("[M6-12] residuo MULTIPLICATIVO del primer trimestre, 1960..1986:\n"); print(round(t1, 2))
L("M6-13", "  por debajo de 1 en ", sum(t1[as.character(1961:1970)] < 1), " de los 10 anios de 1961 a 1970 ; por encima de 1 en ",
  sum(t1[as.character(1978:1986)] > 1), " de los 9 de 1978 a 1986")
t3 <- setNames(mul$random[cycle(UKgas) == 3], 1960:1986)
L("M6-14", "  y el del tercer trimestre va al reves: 1961 = ", sprintf("%.2f", t3["1961"]), " ; 1976 = ", sprintf("%.2f", t3["1976"]),
  " ; 1985 = ", sprintf("%.2f", t3["1985"]))

# ===========================================================================
titulo("M7 · STL sobre log(UKgas): s.window = \"periodic\" frente a un numero")
# ===========================================================================
cat("--- BLOQUE de la solucion ---\n")
fija  <- stl(log(UKgas), s.window = "periodic")$time.series
movil <- stl(log(UKgas), s.window = 7)$time.series
es_t1 <- cycle(UKgas) == 1   # el primer trimestre de cada anio

# (a) Factor estacional del primer trimestre en 1960 y 1986,
#     ya sin logaritmos; y el de 1986, antes y despues de exp()
factor_t1 <- function(st) {
  f <- exp(st[es_t1, "seasonal"])[c(1, 27)]
  setNames(f, c("1960", "1986"))
}
print(round(rbind(periodic  = factor_t1(fija),
                  ventana_7 = factor_t1(movil)), 3))
t1_1986 <- movil[es_t1, "seasonal"][27]
print(round(c(logaritmo = t1_1986, factor = exp(t1_1986)), 3))

# (b) Residuo del primer trimestre: en cuantos anios es negativo,
#     por tramos, y su media en los 13 primeros y los 14 ultimos
res_t1 <- function(st) st[es_t1, "remainder"]
tramo  <- cut(1960:1986, c(1959, 1970, 1977, 1986),
              labels = c("1960-70", "1971-77", "1978-86"))
negativos <- function(st) tapply(res_t1(st) < 0, tramo, sum)
print(rbind(periodic = negativos(fija), ventana_7 = negativos(movil)))
mitad <- rep(c("1960-72", "1973-86"), c(13, 14))
media <- function(st) tapply(res_t1(st), mitad, mean)
print(round(rbind(periodic  = media(fija),
                  ventana_7 = media(movil)), 3))
cat("--- fin del BLOQUE ---\n\n")

L("M7-01", "obs. 105 = ", floor(time(UKgas))[105], "-T", cycle(UKgas)[105], " ; obs. 1 = ", floor(time(UKgas))[1], "-T", cycle(UKgas)[1],
  " ; primeros trimestres: ", sum(es_t1), " (el 1.o es 1960 y el 27.o es 1986)")
L("M7-02", "lectura apresurada del T1 de 1986: +", sprintf("%.1f", 100 * movil[105, "seasonal"]), " % ; lectura correcta: +",
  sprintf("%.1f", 100 * (exp(movil[105, "seasonal"]) - 1)), " %")
L("M7-03", "factor del T3 (ventana 7): 1960 = ", sprintf("%.3f", exp(movil[3, "seasonal"])), " ; 1986 = ", sprintf("%.3f", exp(movil[107, "seasonal"])),
  " ; con periodic, fijo en ", sprintf("%.3f", exp(fija[3, "seasonal"])))
L("M7-04", "dispersion del residuo: periodic / ventana 7 = ", round(sd(fija[, "remainder"]) / sd(movil[, "remainder"]), 1), " veces")
for (sw in c(5, 7, 9, 11, 13)) {
  s <- stl(log(UKgas), s.window = sw)$time.series
  L("M7-05", sprintf("s.window = %-2d: factor T1 1960 = %.3f ; 1986 = %.3f ; sd del residuo = %.3f", sw,
    exp(s[1, "seasonal"]), exp(s[105, "seasonal"]), sd(s[, "remainder"])))
}
rf <- setNames(res_t1(fija), 1960:1986); rm7 <- setNames(res_t1(movil), 1960:1986)
cat("[M7-06] residuo del primer trimestre con periodic, 1960..1986:\n"); print(round(rf, 2))
L("M7-06b", "  negativo en ", sum(rf < 0), " de los 27 anios y positivo en ", sum(rf > 0), " ; anios negativos despues de 1970: ",
  paste(names(rf)[rf < 0 & as.numeric(names(rf)) > 1970], collapse = " "), " ; ultimo anio negativo: ", max(as.numeric(names(rf)[rf < 0])),
  " ; anios por tramo: ", paste(names(table(tramo)), table(tramo), sep = ":", collapse = "  "))
L("M7-06c", "  en los 13 primeros anios (1960-1972): ", sum(rf[1:13] < 0), " negativos ; en los 14 ultimos (1973-1986): ", sum(rf[14:27] > 0),
  " positivos ; anios seguidos negativos desde 1960: ", rle(as.vector(rf < 0))$lengths[1], " ; anios seguidos positivos hasta 1986: ",
  tail(rle(as.vector(rf > 0))$lengths, 1))
cat("[M7-06d] residuo del primer trimestre con ventana 7, 1960..1986:\n"); print(round(rm7, 2))
L("M7-06e", "  negativo en ", sum(rm7 < 0), " de los 27 anios ; cambios de signo a lo largo de la serie: ", length(rle(as.vector(sign(rm7)))$lengths) - 1,
  " (con periodic: ", length(rle(as.vector(sign(rf)))$lengths) - 1, ")")
L("M7-07", "ventana de tendencia por defecto de stl(): con periodic = ", stl(log(UKgas), s.window = "periodic")$win["t"],
  " ; con s.window = 7 = ", stl(log(UKgas), s.window = 7)$win["t"])
L("M7-08", "valor por defecto de s.window en stl(): no tiene (", deparse(formals(stl)$s.window), "); hay que darlo siempre")

# ===========================================================================
titulo("M8 · la serie desestacionalizada de mdeaths, en las dos escalas")
# ===========================================================================
cat("--- BLOQUE de la solucion ---\n")
# Dos STL: sobre la serie (y = T + S + R) y sobre su logaritmo
suma     <- stl(mdeaths, s.window = "periodic")$time.series
producto <- stl(log(mdeaths), s.window = "periodic")$time.series

ajustada_resta  <- mdeaths - suma[, "seasonal"]
ajustada_divide <- mdeaths / exp(producto[, "seasonal"])

# (a) Cuatro meses seguidos
tabla <- cbind(observada = mdeaths,
               resta     = ajustada_resta,
               divide    = ajustada_divide)
print(round(window(tabla, start = c(1975, 11), end = c(1976, 2))))

# (b) Donde se separan mas las dos series ajustadas
dif <- abs(ajustada_resta - ajustada_divide)
j   <- which.max(dif)
print(c(maxima = round(max(dif)),
        anio = floor(time(dif))[j], mes = cycle(dif)[j]))
cat("--- fin del BLOQUE ---\n\n")

L("M8-01", "mdeaths: n = ", length(mdeaths), ", de ", paste(start(mdeaths), collapse = "-"), " a ", paste(end(mdeaths), collapse = "-"),
  " ; maximo = ", max(mdeaths), " (obs. ", which.max(mdeaths), " = ", floor(time(mdeaths))[which.max(mdeaths)], "-", cycle(mdeaths)[which.max(mdeaths)], ")")
L("M8-02", "componente estacional de la suma, ene..dic: ", paste(sprintf("%+.0f", suma[1:12, "seasonal"]), collapse = " "))
L("M8-03", "factor estacional del producto, exp(S), ene..dic: ", paste(sprintf("%.3f", exp(producto[1:12, "seasonal"])), collapse = " "))
L("M8-04", "noviembre -> diciembre de 1975: observada ", mdeaths[23], " -> ", mdeaths[24], " (", sprintf("%+.0f", mdeaths[24] - mdeaths[23]),
  ") ; resta ", round(ajustada_resta[23]), " -> ", round(ajustada_resta[24]), " (", sprintf("%+.0f", round(ajustada_resta[24]) - round(ajustada_resta[23])),
  ") ; divide ", round(ajustada_divide[23]), " -> ", round(ajustada_divide[24]), " (", sprintf("%+.0f", round(ajustada_divide[24]) - round(ajustada_divide[23])), ")")
L("M8-05", "  lo que el patron anual pone en ese paso: suma ", sprintf("%+.0f", suma[24, "seasonal"] - suma[23, "seasonal"]),
  " muertes ; producto x", sprintf("%.3f", exp(producto[24, "seasonal"] - producto[23, "seasonal"])))
L("M8-06", "febrero de 1976: observada ", mdeaths[26], " ; resta ", round(ajustada_resta[26]), " (quita ", round(suma[26, "seasonal"]),
  ") ; divide ", round(ajustada_divide[26]), " (quita ", round(mdeaths[26] - ajustada_divide[26]), ", factor ", sprintf("%.3f", exp(producto[26, "seasonal"])), ")")
L("M8-07", "  enero y marzo de 1976, ajustadas: resta ", round(ajustada_resta[25]), " y ", round(ajustada_resta[27]), " ; divide ",
  round(ajustada_divide[25]), " y ", round(ajustada_divide[27]))
L("M8-08", "media de cada serie ajustada: resta ", round(mean(ajustada_resta)), " ; divide ", round(mean(ajustada_divide)),
  " ; mediana de |resta - divide| = ", round(median(dif)), " ; n.o de meses con diferencia > 100: ", sum(dif > 100))
L("M8-09", "febrero de 1976 en la serie ajustada: es el maximo de `resta` (", round(max(ajustada_resta)), ", obs. ", which.max(ajustada_resta),
  ") y de `divide` (", round(max(ajustada_divide)), ", obs. ", which.max(ajustada_divide), ") ; segundo valor mas alto: resta ",
  round(sort(ajustada_resta, decreasing = TRUE)[2]), " ; divide ", round(sort(ajustada_divide, decreasing = TRUE)[2]))
L("M8-10", "medias anuales de mdeaths: ", paste(names(tapply(mdeaths, anio_de(mdeaths), mean)), round(tapply(mdeaths, anio_de(mdeaths), mean)), sep = ":", collapse = "  "))
L("M8-11", "residuo de febrero de 1976: suma ", sprintf("%+.0f", suma[26, "remainder"]), " muertes ; producto ", sprintf("%+.3f", producto[26, "remainder"]),
  " en logaritmos (x", sprintf("%.3f", exp(producto[26, "remainder"])), ")")

titulo("Fin")
