# ¿cuán exactamente sobre el círculo unitario están las raíces MA de los modelos con d = 2? (c4-m6-60)
suppressMessages(library(forecast))
for (p in 0:2) for (q in 1:2) {
  f <- tryCatch(suppressWarnings(arima(Nile, order = c(p, 2, q), method = "ML")), error = function(e) NULL)
  if (is.null(f)) next
  r <- Mod(polyroot(c(1, f$coef[grep("^ma", names(f$coef))])))
  cat(sprintf("ARIMA(%d,2,%d)  min|raíz MA| = %.8f  (|raíz|-1 = %.2e)\n", p, q, min(r), min(r) - 1))
}
