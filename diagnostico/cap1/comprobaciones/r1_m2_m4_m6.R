# R1 · T1.3 y T1.5 · Comprobaciones de M2 (mts), M4 (unidades, proporcion,
# amplitud en log) y M6 (clasica: log frente a multiplicativa, normalizacion,
# exceso de julio, desviacion tipica anual del residuo aditivo).
suppressPackageStartupMessages({
  library(tsibble); library(dplyr); library(fabletools); library(feasts)
})
AP <- AirPassengers

cat("== M2 · ts con varias series ==\n")
m <- ts(matrix(1:48, 24, 2), start = c(2020, 1), frequency = 12)
cat("class(ts(matrix(1:48, 24, 2), frequency = 12)):", class(m), "\n")
cat("class(EuStockMarkets):", class(EuStockMarkets), " dim:", dim(EuStockMarkets), "\n")
cat("un solo indice para todas las columnas: length(time(m)) =", length(time(m)), " ncol =", ncol(m), "\n")
# tsibble: varias series con clave, cada una con sus propias fechas
v <- tibble::tibble(mes = yearmonth(c("2020 Jan", "2020 Feb", "2020 Mar", "2021 Jun", "2021 Jul")),
                    tienda = c("A", "A", "A", "B", "B"), ventas = 1:5)
tb <- as_tsibble(v, index = mes, key = tienda)
cat("tsibble con clave y fechas distintas por serie: filas", nrow(tb), " claves", n_keys(tb), "\n")
cat("frequency(AirPassengers) =", frequency(AP), "\n")

cat("\n== M4 · Unidades ==\n")
h <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("AirPassengers"))))
print(trimws(grep("thousands|Format|Description", gsub("_\b", "", h), value = TRUE)))
print(trimws(gsub("_\b", "", h)[grep("Description", gsub("_\b", "", h)) + 0:4]))

cat("\n== M4 · Amplitud y nivel por anio ==\n")
an <- floor(time(AP))
niv <- tapply(AP, an, mean); amp <- tapply(AP, an, function(z) max(z) - min(z))
print(rbind(nivel = round(niv, 1), amplitud = amp, pct = round(100 * amp / niv, 1)))
cat("amplitud 1960/1949:", round(amp[12] / amp[1], 2), " nivel 1960/1949:", round(niv[12] / niv[1], 2), "\n")
p <- 100 * amp / niv
cat("anios por debajo del rayo (pct < pct de 1949):", names(p)[p < p[1]], "\n")
cat("minimo:", names(p)[which.min(p)], round(min(p), 1), " maximo:", names(p)[which.max(p)], round(max(p), 1), "\n")
la <- tapply(log(AP), an, function(z) max(z) - min(z))
cat("amplitud en log: 1949", round(la[1], 4), " 1960", round(la[12], 4), " razon:", round(la[12] / la[1], 3), "\n")

cat("\n== M6 · Clasica ==\n")
dc <- decompose(AP, type = "multiplicative"); da <- decompose(AP, type = "additive")
cat("indice julio multiplicativo:", round(dc$figure[7], 4), " exp(aditivo sobre log):",
    round(exp(decompose(log(AP))$figure[7]), 4), "\n")
cat("max |tendencia mult - exp(tendencia de log)|:",
    round(max(abs(dc$trend - exp(decompose(log(AP))$trend)), na.rm = TRUE), 2), "\n")
cl <- as_tsibble(AirPassengers) |>
  model(clasica = classical_decomposition(value, type = "multiplicative")) |> components()
cat("feasts classical_decomposition multiplicativa: indice julio =", round(cl$seasonal[7], 4),
    " max|dif| con decompose():", signif(max(abs(cl$seasonal - as.numeric(dc$seasonal))), 3), "\n")
# normalizacion: a donde va el factor s-barra
d <- AP / dc$trend
bruto <- tapply(d, cycle(AP), mean, na.rm = TRUE)
sbar <- mean(bruto)
cat("s-barra =", round(sbar, 6), " julio bruto =", round(bruto[7], 6), " normalizado =", round(bruto[7] / sbar, 4), "\n")
cat("la tendencia no cambia al normalizar: es la misma media movil (paso 2)\n")
cat("media del residuo CON normalizar (decompose):", round(mean(dc$random, na.rm = TRUE), 6), "\n")
cat("media del residuo SIN normalizar (y / (T * s-tilde)):",
    round(mean(AP / (dc$trend * bruto[cycle(AP)]), na.rm = TRUE), 6), "\n")
cat("media de los 12 indices normalizados:", mean(dc$figure), " suma redondeada a 4:", sum(round(dc$figure, 4)), "\n")
# exceso de julio y lo que traduce el indice
jul <- AP[cycle(AP) == 7]
cat("exceso de julio sobre el nivel medio de su anio:", round(jul - niv, 1), "\n")
cat("aditivo: S_julio =", round(da$figure[7], 2), " R jul-1955 =", round(da$random[79], 2), "\n")
cat("(S_julio - 1) x nivel medio de 1949 y de 1960:", round((dc$figure[7] - 1) * niv[c(1, 12)], 1), "\n")
cat("tendencia en jul-1949 y jul-1960:", dc$trend[7], dc$trend[139], "\n")
cat("(S_julio - 1) x tendencia de jul-1949 y jul-1959:", round((dc$figure[7] - 1) * dc$trend[c(7, 127)], 1), "\n")
sdy <- tapply(da$random, an, sd, na.rm = TRUE)
cat("sd anual del residuo aditivo:", round(sdy, 1), "\n")
cat("residuos disponibles por anio:", tapply(da$random, an, function(z) sum(!is.na(z))), "\n")
cat("anios de sd minima:", names(sort(sdy))[1:2], "\n")
cat("noviembre:", round(dc$figure[11], 4), " tendencia jul-1955:", dc$trend[79], " residuo:", round(dc$random[79], 4), "\n")
