# R2 del capítulo 3 · cifras que la ronda de gráficas hace aparecer en pantalla (lecturas,
# aria-label, frases nuevas), recalculadas en R a partir del precálculo y de las fórmulas.
# Uso (desde la raíz del repo): Rscript diagnostico/cap3/comprobaciones/r2_cifras.R > …/r2_cifras.out
suppressMessages(library(jsonlite))
d <- fromJSON("precalculo/salidas/cap3_arma.json", simplifyVector = FALSE)
num <- function(x) as.numeric(unlist(x))
cat("R", as.character(getRversion()), "\n\n")

cat("== 1. M4 · pesos pi de un ARMA(1,1): pi(B) = phi(B)/theta(B), con theta(B) = 1 + theta B ==\n")
pesos_pi <- function(phi, theta, n = 12) {
  p <- numeric(n + 1); p[1] <- 1
  for (j in 1:n) p[j + 1] <- (if (j == 1) -phi else 0) - theta * p[j]
  p
}
for (caso in list(c(0.8, 0), c(0.8, 1), c(0.8, -1), c(0.8, 1.05), c(0.95, 2), c(-0.95, -2), c(0.5, -0.5))) {
  p <- pesos_pi(caso[1], caso[2])
  cat(sprintf("phi = %5.2f, theta = %5.2f: pi_1 = %9.4f, pi_2 = %9.4f, pi_12 = %10.4f, max|pi_j| (j >= 1) = %10.4f, |pi_j| constante: %s\n",
              caso[1], caso[2], p[2], p[3], p[13], max(abs(p[-1])),
              isTRUE(all.equal(abs(p[-1]), rep(abs(p[2]), 12)))))
}
cat("Con |theta| = 1 la magnitud no cambia (|pi_j| = |phi + theta|): ni crece ni se desvanece.\n")
cat("Umbral del eje logarítmico (max|pi_j| > 20), al mover theta con phi = 0.8 en pasos de 0.05:\n")
for (th in seq(1.05, 2, by = 0.05)) {
  m <- max(abs(pesos_pi(0.8, th)))
  if (m > 20) { cat(sprintf("  primer theta con eje logarítmico: %.2f (max|pi_j| = %.2f); el anterior, %.2f, da %.2f\n",
                            th, m, th - 0.05, max(abs(pesos_pi(0.8, th - 0.05))))); break }
}
s <- function(v) sign(v) * log10(1 + abs(v))
p <- pesos_pi(0.95, 2)
cat("phi = 0.95, theta = 2 · s(pi_j) = signo·log10(1 + |pi_j|), j = 1..12:", sprintf("%.2f", s(p[-1])), "\n")
cat("  incrementos de |s|:", sprintf("%.3f", diff(abs(s(p[-1])))), " (log10(2) =", sprintf("%.3f", log10(2)), ")\n\n")

cat("== 2. M6 · rezagos con la función teórica nula y la muestral fuera de la banda ==\n")
for (k in c("ar1_pos", "ma1_pos", "arma11")) {
  pr <- d$procesos[[k]]; r <- d$realizaciones[[k]]
  b <- 1.96 / sqrt(r$n)
  for (tipo in c("acf", "pacf")) {
    teo <- num(pr[[paste0(tipo, "_teorica")]]); mu <- num(r[[tipo]])[seq_along(teo)]
    # Nulos por el MODELO (ACF de un MA(q) puro tras q; PACF de un AR(p) puro tras p), no por el
    # dato redondeado: la PACF del ARMA(1,1) no se corta nunca, aunque el JSON deje 0.0000 al final.
    corte <- if (tipo == "acf" && pr$p == 0 && pr$q > 0) pr$q else if (tipo == "pacf" && pr$q == 0 && pr$p > 0) pr$p else NA
    ceros <- if (is.na(corte)) rep(FALSE, length(teo)) else seq_along(teo) > corte
    if (sum(abs(teo) < 1e-9) != sum(ceros))
      cat(sprintf("  (ojo: en el JSON hay %d valores de la %s teórica de %s redondeados a 0 que el modelo no anula)\n",
                  sum(abs(teo) < 1e-9) - sum(ceros), toupper(tipo), k))
    fuera <- which(ceros & abs(mu) > b)
    cat(sprintf("%-8s %-4s n = %d, banda = %.4f: %2d rezagos con teórica nula; fuera de la banda: %s%s\n",
                k, toupper(tipo), r$n, b, sum(ceros),
                if (length(fuera)) paste(fuera, collapse = ", ") else "ninguno",
                if (length(fuera)) paste0(" (", paste(sprintf("%.3f", mu[fuera]), collapse = ", "), ")") else ""))
  }
  mayor <- max(abs(c(num(pr$acf_teorica), num(pr$pacf_teorica), num(r$acf)[1:16], num(r$pacf)[1:16])))
  cat(sprintf("         mayor valor absoluto dibujado: %.4f -> eje de ±%s\n", mayor, if (mayor <= 0.5) "0.5" else "1"))
}

pa <- ARMAacf(ar = 0.7, ma = 0.5, lag.max = 16, pacf = TRUE)
cat("PACF teórica exacta del ARMA(1,1), rezagos 13 a 16:", sprintf("%.2e", pa[13:16]), "\n")
cat("\n== 3. M8 · p-valores de Ljung-Box por modelo (eje de 0 a 0.10, nivel 0.05) ==\n")
for (k in c("arma10", "arma20", "arma30", "arma21")) {
  m <- d$manchas$diagnosticos[[k]]
  ps <- sapply(m$ljung_box, function(f) f$p); hs <- sapply(m$ljung_box, function(f) f$rezago)
  cat(sprintf("%-10s rezagos %d a %d: %2d de %2d bajo 0.05 (rezagos %s); %2d entre 0.05 y 0.10; %2d por encima de 0.10; p(12) = %.4f\n",
              m$etiqueta, min(hs), max(hs), sum(ps < 0.05), length(ps),
              if (any(ps < 0.05)) paste(hs[ps < 0.05], collapse = ", ") else "-",
              sum(ps >= 0.05 & ps <= 0.10), sum(ps > 0.10), m$lb12_p))
}
cat("En un eje de 0 a 0.10, la distancia entre 0.0461 y 0.05 es el",
    sprintf("%.1f %%", 100 * (0.05 - 0.0461) / 0.10), "de la altura; en uno de 0 a 1, el",
    sprintf("%.2f %%", 100 * (0.05 - 0.0461)), "\n")
b <- 1.96 / sqrt(d$manchas$n)
for (k in c("arma10", "arma20", "arma30", "arma21")) {
  r <- num(d$manchas$diagnosticos[[k]]$acf_resid)
  cat(sprintf("%-10s ACF de residuales: %d de %d fuera de ±%.3f; r1 = %.3f\n",
              d$manchas$diagnosticos[[k]]$etiqueta, sum(abs(r) > b), length(r), b, r[1]))
}

cat("\n== 4. Quiz · lo que dicen los aria-label de los dos gráficos ==\n")
cat("P3, ACF teórica del MA(2):", sprintf("%.2f", num(d$procesos$ma2$acf_teorica)), "\n")
cat("P9, ACF de los residuales del AR(1):", sprintf("%.2f", num(d$manchas$diagnosticos$arma10$acf_resid)),
    sprintf("· banda ±%.3f\n", b))

cat("\n== 5. Contraste (WCAG) de los colores de correlogramaDoble ==\n")
lum <- function(hex) {
  v <- col2rgb(hex)[, 1] / 255
  v <- ifelse(v <= 0.03928, v / 12.92, ((v + 0.055) / 1.055)^2.4)
  sum(c(0.2126, 0.7152, 0.0722) * v)
}
cr <- function(a, b) { l <- sort(c(lum(a), lum(b)), decreasing = TRUE); (l[1] + 0.05) / (l[2] + 0.05) }
# El naranja de antes era rgba(255,102,0,0.5) sobre blanco: se mezcla con el fondo
antes <- rgb(t((col2rgb("#FF6600") + col2rgb("#FFFFFF")) / 2), maxColorValue = 255)
cat(sprintf("muestral de antes (%s) sobre blanco: %.2f:1 · frente a la banda #e05a00: %.2f:1\n",
            antes, cr(antes, "#FFFFFF"), cr(antes, "#e05a00")))
cat(sprintf("muestral de ahora (#8795A9) sobre blanco: %.2f:1 · frente a la banda #e05a00: %.2f:1 · frente a la teórica #012820: %.2f:1 · frente a #0e7490: %.2f:1\n",
            cr("#8795A9", "#FFFFFF"), cr("#8795A9", "#e05a00"), cr("#8795A9", "#012820"), cr("#8795A9", "#0e7490")))
cat(sprintf("rojo de las barras que se asoman (#dc2626) sobre blanco: %.2f:1 · frente al gris: %.2f:1\n",
            cr("#dc2626", "#FFFFFF"), cr("#dc2626", "#8795A9")))

cat("\n== 6. Pasos que tarda en pasar de 1e6 un AR explosivo sin ruido (orden de magnitud del corte) ==\n")
for (lam in c(1.05, 1.5, 2.65)) cat(sprintf("raíz dominante %.2f: t = %.0f\n", lam, ceiling(log(1e6) / log(lam))))
cat("Raíz dominante de phi = (2.2, 1.2):", sprintf("%.4f", max(Mod(polyroot(c(-1.2, -2.2, 1))))), "\n")
