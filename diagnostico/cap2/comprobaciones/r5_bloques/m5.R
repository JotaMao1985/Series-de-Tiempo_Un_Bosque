set.seed(37)
e <- rnorm(200)
t <- 1:200
A <- 0.2 * t + e                 # recta con ruido
B <- cumsum(0.2 + e)             # caminata con deriva, con el mismo ruido

# r1 y cuantos de 24 rezagos salen de la banda
huella <- function(x) {
  r <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  c(r1 = round(r[1], 3), fuera = sum(abs(r) > 1.96 / sqrt(length(x))))
}

# (a) Los dos tratamientos, aplicados a las dos series
rbind("A sin su recta"  = huella(residuals(lm(A ~ t))),
      "A diferenciada"  = huella(diff(A)),
      "B sin su recta"  = huella(residuals(lm(B ~ t))),
      "B diferenciada"  = huella(diff(B)))

# (c) Lo que sube B por periodo, de dos maneras
round(c(pendiente = unname(coef(lm(B ~ t))[2]), media_de_los_cambios = mean(diff(B))), 3)
# Y lo mas lejos que llega cada serie de la recta 0.2 t
round(c(A = max(abs(A - 0.2 * t)), B = max(abs(B - 0.2 * t))), 1)
