# Recomprobación de la sesión maestra (2026-11-17): ¿el último coeficiente de la
# regresión del rezago k coincide con la PACF muestral de pacf()? (hallazgo c2-m4-05)
y <- log(AirPassengers); p <- as.numeric(pacf(y, lag.max = 12, plot = FALSE)$acf)
ols <- sapply(1:12, function(k) { X <- embed(y, k + 1); unname(coef(lm(X[, 1] ~ X[, -1]))[k + 1]) })
d <- round(ols - p, 3)
cat("k:      ", sprintf("%6d", 1:12), "\n")
cat("pacf:   ", sprintf("%6.3f", p), "\n")
cat("MCO:    ", sprintf("%6.3f", ols), "\n")
cat("máx |diferencia| =", max(abs(d)), "en k =", which.max(abs(d)), "\n")
