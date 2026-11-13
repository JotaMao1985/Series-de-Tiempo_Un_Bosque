# R3 (primera mitad) · T3.1 · Módulo 3: cifras del gráfico de subseries y del
# gráfico de rezagos de AirPassengers.
#
# Las cifras que muestran los dos simuladores nuevos se calculan en JavaScript
# sobre DATOS_CAP1.observado; aquí se recalculan en R sobre datasets::AirPassengers
# y, además, se comprueba que la serie incrustada en el HTML es esa.
#
# Uso (desde la raíz del repo):
#   Rscript diagnostico/cap1/comprobaciones/r3a_m3.R > diagnostico/cap1/comprobaciones/r3a_m3.out
suppressPackageStartupMessages(library(jsonlite))
html <- "Htmls_Series/capitulo-1-componentes-descomposicion.html"
lin <- grep("const DATOS_CAP1 = ", readLines(html, warn = FALSE), value = TRUE)[1]
D <- fromJSON(sub(";\\s*$", "", sub("^\\s*const DATOS_CAP1 = ", "", lin)))
y <- as.numeric(AirPassengers); n <- length(y)
cat("serie incrustada == datasets::AirPassengers:", identical(as.numeric(D$observado), y), "; n =", n, "\n")
meses <- c("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
M <- matrix(y, ncol = 12, byrow = TRUE, dimnames = list(1949:1960, meses))   # fila = año, columna = mes

cat("\n== 1. Gráfico de subseries: una serie de 12 años por mes ==\n")
med <- colMeans(M)
sub <- data.frame(mes = meses, media = sprintf("%.1f", med), y1949 = M[1, ], y1960 = M[12, ],
                  subida = M[12, ] - M[1, ], razon = sprintf("%.2f", M[12, ] / M[1, ]),
                  min = apply(M, 2, min), max = apply(M, 2, max),
                  bajadas = apply(M, 2, function(v) sum(diff(v) < 0)))
print(sub, row.names = FALSE)
cat("mes de media más alta:", meses[which.max(med)], sprintf("%.1f", max(med)),
    "; de media más baja:", meses[which.min(med)], sprintf("%.1f", min(med)), "\n")
cat("orden de las medias (de mayor a menor):", paste(meses[order(-med)], collapse = " > "), "\n")
cat("media de toda la serie:", sprintf("%.1f", mean(y)), "; meses con media por encima:", paste(meses[med > mean(y)], collapse = ", "), "\n")
cat("mes que más sube de 1949 a 1960:", meses[which.max(M[12, ] - M[1, ])], max(M[12, ] - M[1, ]),
    "; el que menos:", meses[which.min(M[12, ] - M[1, ])], min(M[12, ] - M[1, ]), "\n")
cat("razón 1960/1949: de", sprintf("%.2f", min(M[12, ] / M[1, ])), "(", meses[which.min(M[12, ] / M[1, ])], ") a",
    sprintf("%.2f", max(M[12, ] / M[1, ])), "(", meses[which.max(M[12, ] / M[1, ])], ")\n")
cat("subseries que suben todos los años (ninguna bajada):", paste(meses[sub$bajadas == 0], collapse = ", "), "\n")
cat("bajadas de un año al siguiente, por mes y año de llegada:\n")
for (j in 1:12) { d <- which(diff(M[, j]) < 0); if (length(d)) cat("  ", meses[j], ":", paste(1949 + d, collapse = ", "), "\n") }
cat("total de pares (mes, año) en que el mes baja respecto del mismo mes del año anterior:", sum(apply(M, 2, diff) < 0),
    "de", 11 * 12, "; iguales:", sum(apply(M, 2, diff) == 0), "\n")
cat("máximo del año: julio en", sum(apply(M, 1, which.max) == 7), "años, agosto en", sum(apply(M, 1, which.max) == 8), "\n")
cat("mínimo del año: noviembre en", sum(apply(M, 1, which.min) == 11), "años; otros:",
    paste(meses[setdiff(unique(apply(M, 1, which.min)), 11)], collapse = ", "), "\n")

cat("\n== 2. Gráfico de rezagos: y_t frente a y_{t-k}, k = 1..12 ==\n")
acf_k <- acf(y, lag.max = 12, plot = FALSE)$acf[-1]
mes_de <- function(t) (t - 1) %% 12 + 1        # mes (1..12) de la observación t (1..144)
lag <- t(sapply(1:12, function(k) {
  a <- y[(k + 1):n]; b <- y[1:(n - k)]          # a = y_t ; b = y_{t-k}
  verano <- mes_de((k + 1):n) %in% c(7, 8)             # y_t es julio o agosto
  c(k = k, pares = n - k, cor = cor(a, b), encima = sum(a > b), igual = sum(a == b), debajo = sum(a < b),
    dist_media = mean(abs(a - b)), verano_n = sum(verano), verano_encima = sum(a[verano] > b[verano]),
    r_k = acf_k[k])
}))
lag <- as.data.frame(lag)
print(transform(lag, cor = sprintf("%.4f", cor), dist_media = sprintf("%.1f", dist_media), r_k = sprintf("%.4f", r_k)), row.names = FALSE)
cat("correlación a 3 decimales, k = 1..12:", sprintf("%.3f", lag$cor), "\n")
cat("correlación más alta: k =", lag$k[which.max(lag$cor)], sprintf("%.3f", max(lag$cor)),
    "; más baja: k =", lag$k[which.min(lag$cor)], sprintf("%.3f", min(lag$cor)), "\n")
cat("orden de k por correlación (de mayor a menor):", paste(lag$k[order(-lag$cor)], collapse = " "), "\n")
cat("la correlación baja de k = 1 a k = 6 sin excepción:", all(diff(lag$cor[1:6]) < 0),
    "; y sube de k = 6 a k = 12 sin excepción:", all(diff(lag$cor[6:12]) > 0), "\n")
cat("k = 12: pares", n - 12, "; por encima de la diagonal", lag$encima[12], "; por debajo", lag$debajo[12], "; iguales", lag$igual[12], "\n")
a <- y[13:n]; b <- y[1:(n - 12)]; f <- D$fechas[13:n]
cat("   meses por debajo o iguales al mismo mes del año anterior:", paste(f[a <= b], collapse = ", "), "\n")
cat("   cociente y_t / y_{t-12}: mínimo", sprintf("%.3f", min(a / b)), "máximo", sprintf("%.3f", max(a / b)), "mediana", sprintf("%.3f", median(a / b)), "\n")
cat("k = 6: julio y agosto (y_t) frente a enero y febrero (y_{t-6}): por encima de la diagonal",
    lag$verano_encima[6], "de", lag$verano_n[6], "\n")
e6 <- mes_de(7:n) %in% c(1, 2)           # y_t es enero o febrero; y_{t-6} es julio o agosto
cat("k = 6: enero y febrero (y_t) frente a julio y agosto (y_{t-6}): por debajo de la diagonal",
    sum(y[7:n][e6] < y[1:(n - 6)][e6]), "de", sum(e6), "\n")
cat("puntos con y_t en julio o agosto, por k: n =", lag$verano_n, "\n")
cat("   de ellos por encima de la diagonal:      ", lag$verano_encima, "\n")
cat("rango de los ejes: mínimo de la serie", min(y), "; máximo", max(y), "\n")

cat("\n== 3. Los bloques de código del Módulo 3 corren (feasts; fpp3 no está instalado) ==\n")
ok <- tryCatch({
  suppressPackageStartupMessages({ library(tsibble); library(feasts); library(ggplot2) })
  pasajeros <- as_tsibble(AirPassengers)
  pdf(NULL)
  print(autoplot(pasajeros, value))
  print(gg_season(pasajeros, value))
  print(gg_subseries(pasajeros, value))
  print(gg_lag(pasajeros, value, geom = "point", lags = 1:12))
  invisible(dev.off())
  "autoplot, gg_season, gg_subseries y gg_lag(geom = 'point', lags = 1:12): sin error"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat(ok, "\n")
