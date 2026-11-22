# Sesion maestra, R5 del cap. 3: cifras de las correcciones tras la verificacion independiente.
# (1) P4 del quiz con phi = 0.6, theta = -0.2, sigma2 = 5
phi <- 0.6; th <- -0.2; s2 <- 5
psi <- ARMAtoMA(ar = phi, ma = th, lag.max = 3); print(psi)
cat("[Q4] respuesta              ", sprintf("%.2f", s2 * (1 + psi[1]^2)), "\n")
cat("[Q4] olvida sigma2          ", sprintf("%.2f", 1 + psi[1]^2), "\n")
cat("[Q4] olvida psi0            ", sprintf("%.2f", s2 * psi[1]^2), "\n")
cat("[Q4] psi1 = phi             ", sprintf("%.2f", s2 * (1 + phi^2)), "\n")
cat("[Q4] psi1 = phi - theta     ", sprintf("%.2f", s2 * (1 + (phi - th)^2)), "\n")
cat("[Q4] sin cuadrado           ", sprintf("%.2f", s2 * (1 + psi[1])), "\n")
cat("[Q4] suma hasta j = h       ", sprintf("%.2f", s2 * (1 + psi[1]^2 + psi[2]^2)), "\n")
# (2) lynx: Ljung-Box (rezago 12) de los once candidatos en las dos escalas, y avisos
rejilla <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3),
                c(1,1), c(2,1), c(1,2), c(2,2))
lb <- function(x) sapply(rejilla, function(pq) {
  aviso <- NULL
  aj <- withCallingHandlers(arima(x, order = c(pq[1], 0, pq[2]), method = "ML"),
          warning = function(w) { aviso <<- conditionMessage(w); invokeRestart("muffleWarning") })
  if (!is.null(aviso)) cat("  aviso en ARMA(", pq[1], ",", pq[2], "): ", aviso, "\n", sep = "")
  Box.test(residuals(aj), lag = 12, type = "Ljung-Box", fitdf = sum(pq))$p.value
})
nom <- sapply(rejilla, function(pq) sprintf("ARMA(%d,%d)", pq[1], pq[2]))
cat("cruda:\n"); p1 <- lb(lynx); cat("log:\n"); p2 <- lb(log(lynx))
print(data.frame(modelo = nom, cruda = round(p1, 4), log = round(p2, 4)))
cat("[M9] candidatos que pasan (p > 0.05) en cruda:", sum(p1 > 0.05), " en log:", sum(p2 > 0.05), "\n")
# (3) P7: lo que sale al redondear pasos intermedios a dos decimales
r2 <- function(x) round(x, 2)
cat("[Q7] exacto                 ", sprintf("%.4f", 2*pi/acos(0.9/(2*sqrt(0.5)))), "\n")
cat("[Q7] todo a 2 decimales     ", sprintf("%.2f", 2*pi/r2(acos(r2(0.9/(2*r2(sqrt(0.5)))))) ), "\n")
cat("[Q7] solo sqrt a 0.71       ", sprintf("%.2f", 2*pi/acos(0.9/(2*0.71))), "\n")
cat("[Q7] solo cociente a 0.64   ", sprintf("%.2f", 2*pi/acos(0.64)), "\n")
cat("[Q7] solo arcocoseno a 0.88 ", sprintf("%.2f", 2*pi/0.88), "\n")
