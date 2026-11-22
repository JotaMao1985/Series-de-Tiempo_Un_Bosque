# R1 del cap. 4 · cifras de las correcciones de la sesión maestra (2026-11-22)
acf_nilo <- acf(Nile, lag.max = 20, plot = FALSE)$acf[-1]
banda <- 1.96 / sqrt(length(Nile))
cat("banda", round(banda, 3), "\n")
cat("rezagos fuera de la banda (1-20):", which(abs(acf_nilo) > banda), "\n")
cat("de ellos, pasado el 3:", sum(abs(acf_nilo[4:20]) > banda), "de", length(4:20), "\n")
cat("r13 =", round(acf_nilo[13], 3), "\n")
cat("r1 de diff(log(lynx)):", round(acf(diff(log(lynx)), plot = FALSE)$acf[2], 4), "\n")
cat("r1 de diff(BJsales):", round(acf(diff(BJsales), plot = FALSE)$acf[2], 4), "\n")
