# Verificador R5 cap. 3: la P7 (pseudo-periodo de phi = (0.9, -0.5)) con redondeos intermedios
# del estudiante que sigue la pista "por partes"; tolerancia actual 0.006 sobre 7.13.
P <- function(d) { s <- round(sqrt(0.5), d); q <- round(0.9 / (2 * s), d); w <- round(acos(q), d); 2 * pi / w }
res <- sapply(2:5, P); names(res) <- paste0(2:5, "_decimales_intermedios")
print(round(res, 4))
cat("exacto:", 2 * pi / acos(0.9 / (2 * sqrt(0.5))), "\n")
cat("dentro de 7.13 +- 0.006:", abs(round(res, 2) - 7.13) <= 0.006, "\n")
# solo la raiz a 2 decimales (0.71) y el resto exacto
cat("sqrt a 0.71:", 2 * pi / acos(0.9 / 1.42), "  cociente a 0.64:", 2 * pi / acos(0.64), "  cociente a 0.636:", 2*pi/acos(0.636), "\n")
cat("otros tropiezos: grados", 2*pi/(acos(0.6364)*180/pi), " sin raiz", 2*pi/acos(0.9), " pico espectral", 2*pi/acos(0.675), "\n")
