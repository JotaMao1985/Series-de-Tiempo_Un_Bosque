# Diagnóstico: ejecuta tal cual el R de las tres soluciones del cap. 1
# y unas comprobaciones adicionales sobre el quiz y los bloques del M5.
options(digits = 7)
cat("==== EJERCICIO 1 (código de la solución, literal) ====\n")
elasticidad <- function(x) {
  anios <- floor(time(x))
  completos <- names(which(table(anios) == frequency(x)))
  v <- as.numeric(x)
  nivel    <- tapply(v, anios, mean)[completos]
  amplitud <- tapply(v, anios, function(z) max(z) - min(z))[completos]
  fit <- lm(log(amplitud) ~ log(nivel))
  c(b = coef(fit)[2], confint(fit)[2, ], R2 = summary(fit)$r.squared)
}
print(elasticidad(co2))
print(elasticidad(AirPassengers))
print((max(co2) - min(co2)) / mean(co2))
print((max(AirPassengers) - min(AirPassengers)) / mean(AirPassengers))

cat("\n-- extra Ej.1: ¿el IC excluye 0 / 1? --\n")
e1 <- elasticidad(co2); e2 <- elasticidad(AirPassengers)
cat("co2 IC excluye 0:", e1[2] > 0, " incluye 1:", e1[2] < 1 & e1[3] > 1, "\n")
cat("AP  IC excluye 0:", e2[2] > 0, " incluye 1:", e2[2] < 1 & e2[3] > 1, "\n")
cat("co2: variación del nivel anual 1959->1997 (pista):\n")
niv <- tapply(as.numeric(co2), floor(time(co2)), mean)
print(round(100 * (niv[length(niv)] / niv[1] - 1), 1))
# tendencia de la amplitud del co2 (afirmación +0.024 ppm/año, p = 0.0002)
an <- floor(time(co2)); amp <- tapply(as.numeric(co2), an, function(z) max(z) - min(z))
f <- lm(amp ~ as.numeric(names(amp)))
print(round(summary(f)$coefficients[2, c(1, 4)], 5))
# ¿cuánto importa la elección en co2? índices clásicos en ppm
da <- decompose(co2, "additive"); dm <- decompose(co2, "multiplicative")
tr <- range(dm$trend, na.rm = TRUE)
cat("co2 julio(máx) aditivo ppm:", round(max(da$figure), 3),
    " multiplicativo al nivel mín/máx ppm:", round((max(dm$figure) - 1) * tr, 3), "\n")

cat("\n==== EJERCICIO 2 (código de la solución, literal) ====\n")
fuerzas <- function(x, usar_log = FALSE) {
  z  <- if (usar_log) log(x) else x
  st <- stl(z, s.window = "periodic")$time.series
  R <- st[, "remainder"]; T_ <- st[, "trend"]; S <- st[, "seasonal"]
  c(FT = max(0, 1 - var(R) / var(T_ + R)),
    FS = max(0, 1 - var(R) / var(S  + R)))
}
print(round(fuerzas(co2), 4))
print(round(fuerzas(USAccDeaths), 4))
print(round(fuerzas(AirPassengers, usar_log = TRUE), 4))

cat("\n-- extra Ej.2 / Q6: varianzas reales de STL(log AP, periodic) --\n")
st <- stl(log(AirPassengers), s.window = "periodic")$time.series
cat("Var(R) =", signif(var(st[, "remainder"]), 4),
    " Var(T+R) =", signif(var(st[, "trend"] + st[, "remainder"]), 4),
    " Var(S+R) =", signif(var(st[, "seasonal"] + st[, "remainder"]), 4), "\n")
cat("-- extra: fuerzas con s.window = 13 (no periódico) --\n")
fz <- function(x, sw) { st <- stl(x, s.window = sw)$time.series
  R <- st[, 3]; c(FT = 1 - var(R) / var(st[, 2] + R), FS = 1 - var(R) / var(st[, 1] + R)) }
print(round(fz(log(AirPassengers), 13), 4)); print(round(fz(USAccDeaths, 13), 4))
if (requireNamespace("feasts", quietly = TRUE) && requireNamespace("tsibble", quietly = TRUE)) {
  suppressMessages({ library(tsibble); library(feasts); library(dplyr) })
  cat("-- feat_stl de feasts (lo que haría un estudiante con fpp3) --\n")
  print(as_tsibble(log(AirPassengers)) |> features(value, feat_stl) |>
          select(trend_strength, seasonal_strength_year))
  print(as_tsibble(USAccDeaths) |> features(value, feat_stl) |>
          select(trend_strength, seasonal_strength_year))
  print(as_tsibble(co2) |> features(value, feat_stl) |>
          select(trend_strength, seasonal_strength_year))
}

cat("\n==== EJERCICIO 3 (código de la solución, literal) ====\n")
pos <- 79
ap_out <- AirPassengers
ap_out[pos] <- ap_out[pos] * 1.5
idx_clasica <- function(x) as.numeric(decompose(x, type = "multiplicative")$figure)
idx_stl <- function(x, robusto) {
  s <- stl(log(x), s.window = "periodic", robust = robusto)$time.series[, "seasonal"]
  as.numeric(exp(s[1:12]))
}
print(c(idx_clasica(AirPassengers)[7], idx_clasica(ap_out)[7]))
print(c(idx_stl(AirPassengers, TRUE)[7], idx_stl(ap_out, TRUE)[7]))
print(c(idx_stl(AirPassengers, FALSE)[7], idx_stl(ap_out, FALSE)[7]))
pct <- function(a, b) round(100 * (b / a - 1), 2)
cat("distorsión %: clásica", pct(idx_clasica(AirPassengers)[7], idx_clasica(ap_out)[7]),
    " STL robusto", pct(idx_stl(AirPassengers, TRUE)[7], idx_stl(ap_out, TRUE)[7]),
    " STL sin robust", pct(idx_stl(AirPassengers, FALSE)[7], idx_stl(ap_out, FALSE)[7]), "\n")
cat("-- extra Ej.3: el robusto mueve el índice LIMPIO de julio en %:",
    pct(idx_stl(AirPassengers, FALSE)[7], idx_stl(AirPassengers, TRUE)[7]), "\n")
cat("-- extra Ej.3 (FPP3 3.7 ej.7f): atípico al final (obs. 139, jul-1960) --\n")
ap_fin <- AirPassengers; ap_fin[139] <- ap_fin[139] * 1.5
cat("clásica julio:", pct(idx_clasica(AirPassengers)[7], idx_clasica(ap_fin)[7]),
    "% ; STL robusto:", pct(idx_stl(AirPassengers, TRUE)[7], idx_stl(ap_fin, TRUE)[7]), "%\n")

cat("\n==== QUIZ Q3/Q4: valores de tendencia no NA ====\n")
print(sum(!is.na(decompose(AirPassengers)$trend)))
print(sum(is.na(decompose(AirPassengers)$trend)))

cat("\n==== Bloque R del M5: slide_dbl(.before=6,.after=6) vs 2x12 ====\n")
y <- as.numeric(AirPassengers)
ma13 <- slider::slide_dbl(y, mean, .before = 6, .after = 6, .complete = TRUE)
ma2x12 <- as.numeric(stats::filter(y, c(0.5, rep(1, 11), 0.5) / 12, sides = 2))
dec <- as.numeric(decompose(AirPassengers)$trend)
cat("max |2x12 - decompose| =", max(abs(ma2x12 - dec), na.rm = TRUE), "\n")
cat("max |slide_dbl(13 iguales) - 2x12| =", round(max(abs(ma13 - ma2x12), na.rm = TRUE), 3), "\n")
cat("julio 1955 (obs 79): 2x12 =", round(ma2x12[79], 2), " slide_dbl =", round(ma13[79], 2), "\n")
ma12f <- as.numeric(stats::filter(y, rep(1 / 12, 12), sides = 2))
cat("stats::filter(y, rep(1/12,12)) (ciclo M6 'Con qué'), obs 79:", round(ma12f[79], 2), "\n")
