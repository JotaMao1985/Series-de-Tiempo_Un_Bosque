# Verifica las cifras del Modulo 6 del capitulo 1 (descomposicion clasica).
# Contrasta contra stats::decompose() todo numero escrito a mano en la prosa:
# el contraejemplo aditivo, los indices brutos y el reescalado del paso 3c.
# Uso: Rscript precalculo/verifica_cap1_descomposicion.R

y <- AirPassengers; da <- decompose(y,"additive"); dm <- decompose(y,"multiplicative")
M <- matrix(as.numeric(y), nrow=12); t79 <- 79
ok <- TRUE
chk <- function(etiqueta, obtenido, escrito, tol=0.051) {
  bien <- abs(obtenido-escrito) <= tol
  ok <<- ok && bien
  cat(sprintf("%-46s escrito %-10s R %-10s %s\n", etiqueta, format(escrito),
              format(round(obtenido,4)), if (bien) "OK" else "<<< DISCREPA"))
}
chk("aditivo jul-1955 · tendencia",  da$trend[t79],  285.75)
chk("aditivo jul-1955 · S_julio",    da$figure[7],   63.83)
chk("aditivo jul-1955 · residuo",    da$random[t79], 14.42)
chk("aditivo jul-1955 · suma = y_t", da$trend[t79]+da$figure[7]+da$random[t79], 364)

ex <- M[7,] - colMeans(M)
esc_ex <- c(21.3,30.3,28.8,33.0,39.0,63.1,80.0,84.8,96.6,110.0,119.7,145.8)
for (i in 1:12) chk(paste0("exceso de julio ", 1948+i), ex[i], esc_ex[i])
chk("exceso: cuantas veces se multiplica", ex[12]/ex[1], 6.85, 0.05)
chk("63.83 frente a 1949 (el triple)",     da$figure[7]/ex[1], 3.00, 0.05)
chk("63.83 frente a 1960 (menos de 1/2)",  da$figure[7]/ex[12], 0.44, 0.01)

mult_pas <- colMeans(M)*(dm$figure[7]-1)
chk("multiplicativo en pasajeros · 1949", mult_pas[1], 28.7)
chk("multiplicativo en pasajeros · 1960", mult_pas[12], 107.9)

sdev <- apply(matrix(as.numeric(da$random), nrow=12), 2, sd, na.rm=TRUE)
esc_sd <- c(30.5,20.7,22.4,17.0,14.5,5.6,6.1,10.0,17.2,29.4,29.4,25.4)
for (i in 1:12) chk(paste0("sd del residuo aditivo ", 1948+i), sdev[i], esc_sd[i])

det <- y/dm$trend
brutos <- sapply(1:12, function(i) mean(det[seq(i,144,by=12)], na.rm=TRUE))
chk("s barra (media de los 12 brutos)", mean(brutos), 0.998236, 1e-5)
chk("indice bruto de julio",            brutos[7],    1.224391, 1e-5)
chk("1 / s barra",                      1/mean(brutos), 1.0018, 1e-4)
chk("S_julio reescalado",               brutos[7]/mean(brutos), 1.2266, 1e-4)
chk("desvio en %",                      (1/mean(brutos)-1)*100, 0.18, 0.005)
chk("n_k",  sum(!is.na((y-dm$trend)[seq(7,144,by=12)])), 11, 0)
chk("suma de los 12 indices redondeados", sum(round(as.numeric(dm$figure),4)), 12.0001, 1e-9)

cat("\n", if (ok) ">>> TODAS LAS CIFRAS COINCIDEN" else ">>> HAY DISCREPANCIAS", "\n")
