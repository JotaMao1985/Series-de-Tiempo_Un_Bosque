#!/usr/bin/env Rscript
# R2 del cap. 4 · las cifras que la ronda hace aparecer en pantalla, calculadas en R aparte de la página.
# Todas salen en JS de los datos incrustados (DATOS_CAP4, SERIES_CAP4: la salida de genera_cap4.R); aquí se
# recalculan de otra fuente (los datos de R y salidas/cap4_arima.json) para contrastarlas con lo que
# escribe la página (r2_resumen.out, `aria-label` y lecturas).
# Uso: Rscript diagnostico/cap4/comprobaciones/r2_cifras.R > diagnostico/cap4/comprobaciones/r2_cifras.out
suppressMessages(library(jsonlite))
j <- fromJSON("precalculo/salidas/cap4_arima.json", simplifyVector = FALSE)
n <- j$nilo
f2 <- function(x) formatC(x, format = "f", digits = 2)
f3 <- function(x) formatC(x, format = "f", digits = 3)
f4 <- function(x) formatC(x, format = "f", digits = 4)
nilo <- as.numeric(datasets::Nile)

cat("== 1. M7 · cotas del eje de la traza (a partir de los AICc finitos de las dos búsquedas)\n")
fin <- unlist(lapply(c("escalonada", "exhaustiva"), function(m)
  vapply(n$hyndman_khandakar[[m]]$pasos, function(p) if (isTRUE(p$infinito) || is.null(p$aicc)) NA_real_ else p$aicc, 0)))
fin <- fin[!is.na(fin)]
cat("   AICc finitos:", length(fin), " mín", f3(min(fin)), " máx", f3(max(fin)), "\n")
suelo <- floor(min(fin) / 5) * 5; cima <- ceiling(max(fin) / 5) * 5
cat("   SUELO", suelo, " CIMA", cima, " TECHO (fila del ∞) =", cima + 5, "\n")
for (m in c("escalonada", "exhaustiva")) {
  inf <- which(vapply(n$hyndman_khandakar[[m]]$pasos, function(p) isTRUE(p$infinito), TRUE))
  mej <- which(vapply(n$hyndman_khandakar[[m]]$pasos, function(p) isTRUE(p$mejora), TRUE))
  cat("  ", m, ": pasos con AICc = ∞:", paste(inf, collapse = ", "), "· mejoras:", paste(mej, collapse = ", "), "\n")
}

cat("\n== 2. M9 · límite inferior del 95 % de cada forma (lectura nueva con d = 2)\n")
for (k in names(n$formas_pronostico)) {
  f <- n$formas_pronostico[[k]]
  lo <- unlist(f$lo95)
  cat(sprintf("   %-10s %-34s mín lo95 = %9s en h = %d; lo95[h=30] = %s; hi95[h=30] = %s; ŷ[1] = %s; ŷ[30] = %s\n",
              k, f$etiqueta, f2(min(lo)), which.min(lo), f2(lo[30]), f2(tail(unlist(f$hi95), 1)),
              f2(f$media[[1]]), f2(tail(unlist(f$media), 1))))
}
cat("   último caudal observado (1970):", nilo[100], "\n")

cat("\n== 3. M6 · ΔAICc sobre el mejor de cada d (aria-label del segundo lienzo)\n")
for (d in 0:2) {
  mejor <- n$mejor_por_d[[paste0("d", d)]]$valor_aicc
  ms <- Filter(function(m) m$d == d && isTRUE(m$convergio), n$rejilla)
  dl <- vapply(ms, function(m) m$aicc - mejor, 0)
  cat(sprintf("   d = %d: %d modelos, ΔAICc de %s a %s; barras cortadas en 20: %d (%s)\n", d, length(ms),
              f2(min(dl)), f2(max(dl)), sum(dl > 20),
              paste(vapply(ms[dl > 20], function(m) sprintf("%s ↑%.0f", sub("ARIMA", "", m$etiqueta), m$aicc - mejor), ""), collapse = ", ")))
}
cat("   (0,2,0): AICc", f2(n$rejilla[["020"]]$aicc), " ΔAICc", f2(n$rejilla[["020"]]$aicc - n$mejor_por_d$d2$valor_aicc), "\n")

cat("\n== 4. Quiz · lo que dibujan los dos gráficos (descripcionGrafico)\n")
for (k in c("cruda")) {
  v <- unlist(n$identificacion[[k]]$acf); b <- n$identificacion[[k]]$banda
  cat("   ACF muestral del Nilo sin diferenciar, banda", f3(b), "= 1.96/sqrt(100) =", f3(1.96 / sqrt(100)), "\n")
  cat("   valores (2 decimales):", paste(f2(v), collapse = ", "), "\n")
  cat("   dentro de la banda:", sum(abs(v) <= b), "de", length(v), "· rezagos:", paste(which(abs(v) <= b), collapse = ", "), "\n")
}
p <- j$puente_estacional
v <- unlist(p$no_estacional$acf_residuales)
cat("   ACF residual del puente, banda", f3(p$no_estacional$banda), "= 1.96/sqrt(144) =", f3(1.96 / sqrt(144)), "\n")
cat("   valores (2 decimales):", paste(f2(v), collapse = ", "), "\n")
cat("   fuera de la banda:", sum(abs(v) > p$no_estacional$banda), "de", length(v), "· rezagos:",
    paste(which(abs(v) > p$no_estacional$banda), collapse = ", "), "\n")

cat("\n== 5. M1, M4, M8 · media, varianza y ρ̂₁ de la serie del Nilo por número de diferencias (aria-label)\n")
for (d in 0:3) {
  y <- if (d == 0) nilo else diff(nilo, differences = d)
  cat(sprintf("   d = %d: n = %d, media %s, varianza %s, ρ̂₁ %s, mín %.0f, máx %.0f\n", d, length(y), f2(mean(y)),
              f2(var(y)), f4(acf(y, plot = FALSE, lag.max = 1)$acf[2]), min(y), max(y)))
}

cat("\n== 6. M9 · pesos ψ (aria-label del primer gráfico) y σ_h\n")
i <- n$intervalos
psi <- unlist(i$psi)
cat("   ψ: n =", length(psi), " ψ0 =", f3(psi[1]), " ψ1 =", f3(psi[2]), " ψ29 =", f3(psi[length(psi)]), " máx =", max(psi), "\n")
sh <- unlist(i$sigma_h)
cat("   h = 15: σ_h =", f3(sh[15]), " σ√h =", f3(i$sigma * sqrt(15)), "; h = 30: σ_h =", f3(sh[30]), " σ√h =", f3(i$sigma * sqrt(30)), "\n")

cat("\n== 7. M10 · abanico de la TRM a 36 meses (aria-label)\n")
tr <- j$trm$caminata
cat("   σ² =", tr$sigma2, " σ =", f2(sqrt(tr$sigma2)), "\n")
