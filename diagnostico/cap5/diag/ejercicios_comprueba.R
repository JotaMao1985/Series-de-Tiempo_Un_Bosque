# Diagnóstico cap. 5 · comprobaciones finas que ejercicios_cap5.R dejó abiertas:
#   1. Q7: el beta de log(días) con Semana Santa (el modelo del que salen 1.0840 y 0.4462).
#   2. Q8: el SARIMA + calendario en la partición única (la octava fila de la tabla del M11).
#   3. Cifras con más decimales: TRM (r12 de ∇TRM, rho12 en niveles, t del SAR forzado).
#   4. Variantes del simulacro (redondeos y errores sin ruta) → ejercicios_variantes.json,
#      que lee ejercicios_longitud_opciones.js.
#   LC_ALL=en_US.UTF-8 Rscript diagnostico/cap5/diag/ejercicios_comprueba.R > diagnostico/cap5/diag/ejercicios_comprueba.out 2>&1
suppressPackageStartupMessages({ library(forecast); library(jsonlite) })
aqui <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
raiz <- normalizePath(file.path(aqui, "../../.."))
sb <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"))
trm <- ts(sb$trm$valores, start = sb$trm$inicio, frequency = 12)
ap <- log(AirPassengers)

pascua <- function(a) {   # Meeus/Jones/Butcher, el mismo algoritmo de genera_cap5.R
  b <- a %/% 100; c <- a %% 100; d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3
  h <- (19 * (a %% 19) + b - d - g + 15) %% 30; i <- c %/% 4; k <- c %% 4
  l <- (32 + 2 * e + 2 * i - h - k) %% 7; m <- ((a %% 19) + 11 * h + 22 * l) %/% 451
  as.Date(sprintf("%d-%02d-%02d", a, (h + l - 7 * m + 114) %/% 31, ((h + l - 7 * m + 114) %% 31) + 1))
}
fechas <- seq(as.Date("1949-01-01"), by = "month", length.out = 145)
dias <- as.numeric(diff(fechas)); fechas <- fechas[1:144]
pm <- as.numeric(format(fechas, "%m")) == as.numeric(format(pascua(as.numeric(format(fechas, "%Y"))), "%m"))
X <- cbind(log_dias = log(dias), pascua = as.numeric(pm))
cat("== 1. Q7: airline + log(días) + Semana Santa\n")
full <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), xreg = X)
b <- coef(full)["log_dias"]; se <- sqrt(diag(full$var.coef))["log_dias"]
print(round(c(beta = b, ee = se, t0 = b / se, t1 = (b - 1) / se, aicc = full$aicc), 4))
cat("Pascua en marzo:", sum(format(pascua(1949:1960), "%m") == "03"), "de 12 años\n")

cat("\n== 2. Q8: SARIMA + calendario en la partición única (últimos 24 meses)\n")
n <- length(ap); ent <- window(ap, end = time(ap)[n - 24]); obs <- as.numeric(window(AirPassengers, start = time(ap)[n - 23]))
mc <- Arima(ent, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12), xreg = X[1:(n - 24), ])
fc <- exp(forecast(mc, xreg = X[(n - 23):n, ], h = 24)$mean)
cat("RMSE SARIMA + calendario:", round(sqrt(mean((obs - fc)^2)), 3), "\n")

cat("\n== 3. Más decimales\n")
a <- Acf(diff(trm), lag.max = 36, plot = FALSE)$acf
an <- Acf(trm, lag.max = 36, plot = FALSE)$acf
g <- Arima(trm, order = c(0, 1, 0), seasonal = list(order = c(1, 0, 0), period = 12))
print(c(r12_dif = a[13], r12_niv = an[13], Phi = unname(coef(g)[1]), ee = sqrt(g$var.coef[1, 1]),
        t = unname(coef(g)[1]) / sqrt(g$var.coef[1, 1])), digits = 8)
cat("round(r12_dif, 4) =", round(a[13], 4), "| sprintf %.4f =", sprintf("%.4f", a[13]), "\n")

cat("\n== 4. Variantes del simulacro\n")
th <- -0.4012; Th <- -0.6514; s2 <- 0.003152
f7 <- 6.4671 + 6.3034 - 6.3973 + th * 0.0764 + Th * 0.0313 + th * Th * 0.0294
nn <- 167; s22 <- 0.0006073
v <- list(
  `2` = list(`logs a 4 decimales` = sum(round(log(c(496.19, 445.82, 506.77, 434.25)), 4) * c(1, -1, -1, 1)),
             `cifra a 3 decimales` = round(sum(log(c(496.19, 445.82, 506.77, 434.25)) * c(1, -1, -1, 1)), 3),
             `cifra a 2 decimales` = round(sum(log(c(496.19, 445.82, 506.77, 434.25)) * c(1, -1, -1, 1)), 2)),
  `4` = list(`a 3 decimales` = round(th * Th / ((1 + th^2) * (1 + Th^2)), 3),
             `a 2 decimales` = round(th * Th / ((1 + th^2) * (1 + Th^2)), 2)),
  `5` = list(`exacto` = nn * (nn + 2) * (s22 + 0.0801^2 / (nn - 12) + 0.018^2 / (nn - 24)),
             `dividiendo entre n y no n − k en 12 y 24` = nn * (nn + 2) * (s22 + 0.0801^2 / nn + 0.018^2 / nn),
             `sin el +2 (n·n)` = nn * nn * (s22 + 0.0801^2 / (nn - 12) + 0.018^2 / (nn - 24)),
             `a un decimal` = round(nn * (nn + 2) * (s22 + 0.0801^2 / (nn - 12) + 0.018^2 / (nn - 24)), 1)),
  `6` = list(`a 3 decimales` = round(sqrt(s2 * (1 + 11 * (1 + th)^2 + (2 + th + Th)^2)), 3),
             `sin el escalón (12 pesos 1+θ)` = sqrt(s2 * (1 + 12 * (1 + th)^2)),
             `sin ψ12 (h = 12)` = sqrt(s2 * (1 + 11 * (1 + th)^2))),
  `7` = list(`exacto` = exp(f7), `sin el término θΘε(t−13)` = exp(f7 - th * Th * 0.0294),
             `satélite restado` = exp(f7 - 2 * th * Th * 0.0294), `sin θε(t−1)` = exp(f7 - th * 0.0764),
             `sin Θε(t−12)` = exp(f7 - Th * 0.0313), `log redondeado a 2 dec.` = exp(round(f7, 2)),
             `media lognormal` = exp(f7 + s2 / 2)),
  `10` = list(`a 1 decimal` = round((2.0094 - 1) / 0.3601, 1), `β y ee a 2 dec.` = (2.01 - 1) / 0.36))
str(lapply(v, function(z) round(unlist(z), 6)))
writeLines(toJSON(v, auto_unbox = TRUE, digits = 10, pretty = TRUE), file.path(aqui, "ejercicios_variantes.json"))
cat("escrito ejercicios_variantes.json\n")
