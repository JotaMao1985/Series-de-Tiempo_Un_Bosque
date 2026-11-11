# R1 · T1.4 · Ejercicio 1 del M9: cada cifra de la conclusion y de la tabla.
elasticidad <- function(x) {
  anios <- floor(time(x))
  completos <- names(which(table(anios) == frequency(x)))
  v <- as.numeric(x)
  nivel    <- tapply(v, anios, mean)[completos]
  amplitud <- tapply(v, anios, function(z) max(z) - min(z))[completos]
  fit <- lm(log(amplitud) ~ log(nivel))
  c(b = coef(fit)[2], confint(fit)[2, ], R2 = summary(fit)$r.squared)
}
cat("== La funcion del capitulo, tal cual ==\n")
e1 <- elasticidad(co2); e2 <- elasticidad(AirPassengers)
print(round(e1, 3)); print(round(e2, 3))
cat("co2: IC excluye 0?", e1[2] > 0, " contiene 1?", e1[2] < 1 && e1[3] > 1, "\n")
cat("AP : IC excluye 0?", e2[2] > 0, " excluye 1?", e2[2] > 1, "\n")

cat("\n== Las dos ultimas lineas del bloque ==\n")
cat("(max(co2) - min(co2)) / mean(co2) =", round((max(co2) - min(co2)) / mean(co2), 3), "\n")
cat("(max(AP) - min(AP)) / mean(AP)    =", round((max(AirPassengers) - min(AirPassengers)) / mean(AirPassengers), 3), "\n")

cat("\n== Cuanto sube el NIVEL (medias anuales) ==\n")
nc <- tapply(co2, floor(time(co2)), mean); na <- tapply(AirPassengers, floor(time(AirPassengers)), mean)
cat("co2:", names(nc)[1], round(nc[1], 1), "->", names(nc)[length(nc)], round(nc[length(nc)], 1),
    " = +", round(100 * (nc[length(nc)] / nc[1] - 1), 1), "% en", length(nc), "anios\n")
cat("AP :", names(na)[1], round(na[1], 1), "->", names(na)[length(na)], round(na[length(na)], 1),
    " = x", round(na[length(na)] / na[1], 2), "\n")

cat("\n== La amplitud del CO2: crece, y como ==\n")
ac <- tapply(co2, floor(time(co2)), function(z) max(z) - min(z)); yrs <- as.numeric(names(nc))
f1 <- summary(lm(ac ~ yrs))$coefficients
cat("amplitud ~ anio: pendiente", round(f1[2, 1], 4), "ppm/anio, p =", signif(f1[2, 4], 2), "\n")
c0 <- mean(ac) / mean(nc)
cat("si amplitud = c * nivel, con c = media(amp)/media(nivel) =", round(c0, 5),
    ": pendiente", round(coef(lm(I(c0 * nc) ~ yrs))[2], 4), "ppm/anio\n")
f2 <- summary(lm(I(ac / nc) ~ yrs))$coefficients
cat("(amplitud/nivel) ~ anio: pendiente", signif(f2[2, 1], 2), ", p =", round(f2[2, 4], 2), "\n")
cat("amplitud/nivel: primer anio", round(100 * ac[1] / nc[1], 2), "%  ultimo", round(100 * ac[length(ac)] / nc[length(nc)], 2), "%\n")

cat("\n== 'La eleccion importa poco': clasica aditiva frente a multiplicativa en co2 ==\n")
da <- decompose(co2, "additive"); dm <- decompose(co2, "multiplicative")
aj_a <- co2 - da$seasonal; aj_m <- co2 / dm$seasonal
cat("max |desestacionalizada aditiva - multiplicativa| =", round(max(abs(aj_a - aj_m)), 2),
    "ppm ; amplitud estacional aditiva =", round(diff(range(da$figure)), 2), "ppm\n")
cat("sd del residuo: aditiva", round(sd(da$random, na.rm = TRUE), 3), " multiplicativa (en ppm, y - T*S)",
    round(sd(co2 - dm$trend * dm$seasonal, na.rm = TRUE), 3), "\n")
ap_a <- decompose(AirPassengers, "additive"); ap_m <- decompose(AirPassengers, "multiplicative")
cat("misma comparacion en AP: max |dif| =", round(max(abs((AirPassengers - ap_a$seasonal) - AirPassengers / ap_m$seasonal)), 1),
    " ; amplitud estacional aditiva =", round(diff(range(ap_a$figure)), 1), "\n")
cat("amplitud que implica la multiplicativa de indices fijos en co2 (rango de indices x nivel): 1959",
    round(diff(range(dm$figure)) * nc[1], 2), " 1997", round(diff(range(dm$figure)) * nc[length(nc)], 2), "ppm\n")

cat("\n== STL con ventana estacional finita tambien recoge el crecimiento ==\n")
s <- stl(co2, s.window = 11)$time.series[, "seasonal"]
as_ <- tapply(s, floor(time(co2)), function(z) max(z) - min(z))
cat("stl(co2, s.window = 11): amplitud del componente estacional 1959", round(as_[1], 2), " 1997", round(as_[length(as_)], 2), "ppm\n")
sp <- stl(co2, s.window = "periodic")$time.series[, "seasonal"]
cat("stl(co2, s.window = 'periodic'): amplitud 1959", round(diff(range(sp[1:12])), 2), " 1997", round(diff(range(sp[457:468])), 2), "ppm\n")
