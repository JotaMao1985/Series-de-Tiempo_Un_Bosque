# Ronda R2 (gráficas) del capítulo 1 · comprobaciones de lo que la prosa dice que se ve.
# Uso: Rscript r2_graficas.R > r2_graficas.out
y <- AirPassengers

cat("== 1. Comparador (M4): ¿«valen lo mismo al nivel de partida» frente a 20.0 y 23.6? ==\n")
# Misma construcción que SIMULADORES['comparador-escala']: T0 = 100, beta = 2, A = 20, a = A/T0.
t <- 0:95; T0 <- 100; beta <- 2; A <- 20; a <- A / T0
Tt <- T0 + beta * t; forma <- sin(2 * pi * t / 12)
adi <- Tt + A * forma; mul <- Tt * (1 + a * forma)
osc <- function(s, k) max(abs(s[(k * 12 + 1):(k * 12 + 12)] - Tt[(k * 12 + 1):(k * 12 + 12)]))
cat(sprintf("oscilacion maxima, anio 1: aditiva %.1f, multiplicativa %.1f\n", osc(adi, 0), osc(mul, 0)))
cat(sprintf("oscilacion maxima, anio 8: aditiva %.1f, multiplicativa %.1f\n", osc(adi, 7), osc(mul, 7)))
i <- which.max(abs(mul[1:12] - Tt[1:12]))
cat(sprintf("el maximo multiplicativo del anio 1 cae en t = %d (mes %d), con nivel T = %.0f: a*T = %.1f\n", t[i], i, Tt[i], a * Tt[i]))
cat(sprintf("nivel al empezar y al acabar el anio 1: %.0f y %.0f\n", Tt[1], Tt[12]))
cat(sprintf("al nivel de partida T0 = %.0f: aditiva A = %.1f, multiplicativa a*T0 = %.1f\n", T0, A, a * T0))

cat("\n== 2. STL (M7): ¿«el residuo no tiene estructura visible»? ==\n")
s <- stl(log(y), s.window = "periodic")
R <- s$time.series[, "remainder"]
cat("desviacion tipica del residuo por anio:\n"); print(round(tapply(as.numeric(R), floor(time(R)), sd), 4))
cat(sprintf("media de esas desviaciones: 1949-1953 %.4f | 1955-1957 %.4f | 1958-1960 %.4f\n",
  mean(tapply(as.numeric(R), floor(time(R)), sd)[1:5]), mean(tapply(as.numeric(R), floor(time(R)), sd)[7:9]),
  mean(tapply(as.numeric(R), floor(time(R)), sd)[10:12])))
cat("residuo de julio, anio por anio:", round(as.numeric(R)[cycle(R) == 7], 4), "\n")
cat("autocorrelacion del residuo en los rezagos 1, 12 y 24:", round(acf(R, lag.max = 24, plot = FALSE)$acf[c(2, 13, 25)], 3), "\n")
cat(sprintf("banda de ruido blanco al 95 %%: +/- %.3f\n", 1.96 / sqrt(length(R))))

cat("\n== 3. Lo que afirman los aria-label nuevos ==\n")
cat("mes del maximo de cada anio (M3):", tapply(as.numeric(y), floor(time(y)), which.max), "\n")
m <- matrix(as.numeric(y), ncol = 12, byrow = TRUE)
cat("anios con algun mes por debajo del mismo mes del anio anterior (M3):", which(apply(diff(m) < 0, 1, any)) + 1949, "\n")
d <- decompose(y, "multiplicative")
cat("indices clasicos (M6):", round(d$figure, 4), "-> maximo en el mes", which.max(d$figure), ", minimo en el mes", which.min(d$figure), "\n")
cat("desviacion tipica del residuo clasico por anio (M6):\n"); print(round(tapply(as.numeric(d$random), floor(time(y)), sd, na.rm = TRUE), 4))
est <- s$time.series[1:12, "seasonal"]
cat("estacional de STL (M7): maximo en el mes", which.max(est), ", minimo en el mes", which.min(est), "\n")
mm <- stats::filter(y, c(0.5, rep(1, 11), 0.5) / 12)
cat("media movil 2x12 (M5): valores no NA =", sum(!is.na(mm)), "; NA al principio =", which(!is.na(mm))[1] - 1, "\n")
mm5 <- stats::filter(y, rep(1 / 5, 5)); mm24 <- stats::filter(y, c(0.5, rep(1, 23), 0.5) / 24)
cat("m = 5: no NA =", sum(!is.na(mm5)), "| m = 24 (2x24): no NA =", sum(!is.na(mm24)), "\n")
