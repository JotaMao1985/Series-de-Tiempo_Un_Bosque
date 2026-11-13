# R3c · comprobaciones de A1 (nube frente a r_k), A2 (ACF del residuo) y A7 (sd anual del residuo)
y <- as.numeric(datasets::AirPassengers); n <- length(y); k <- 12
a <- y[(k + 1):n]; b <- y[1:(n - k)]; yb <- mean(y)
cat("== A1 · rezago 12 ==\n")
cat(sprintf("pares: %d de %d observaciones\n", length(a), n))
cat(sprintf("correlacion de la nube (medias y denominador de la nube): %.4f\n", cor(a, b)))
cat(sprintf("r_12 (media global, denominador de la serie entera):       %.4f\n",
            sum((a - yb) * (b - yb)) / sum((y - yb)^2)))
cat(sprintf("acf(y)[12]:                                                %.4f\n",
            acf(y, lag.max = 12, plot = FALSE)$acf[13]))
cat(sprintf("media global, denominador de la nube:                      %.4f\n",
            sum((a - yb) * (b - yb)) / sqrt(sum((a - yb)^2) * sum((b - yb)^2))))
cat(sprintf("medias de la nube, denominador de la serie entera:         %.4f\n",
            sum((a - mean(a)) * (b - mean(b))) / sum((y - yb)^2)))
cat(sprintf("numerador de r_12 / numerador con medias de la nube:       %.4f\n",
            sum((a - yb) * (b - yb)) / sum((a - mean(a)) * (b - mean(b)))))
cat(sprintf("denominador de la nube / denominador de la serie:          %.4f\n",
            sqrt(sum((a - yb)^2) * sum((b - yb)^2)) / sum((y - yb)^2)))
cat(sprintf("medias: serie %.1f · y_t de la nube %.1f · y_(t-12) de la nube %.1f\n", yb, mean(a), mean(b)))

cat("\n== A2 · autocorrelacion del residuo en el rezago 12 ==\n")
da <- decompose(datasets::AirPassengers, type = "additive")
dm <- decompose(datasets::AirPassengers, type = "multiplicative")
for (nm in c("aditiva", "multiplicativa")) {
  r <- na.omit(as.numeric(if (nm == "aditiva") da$random else dm$random))
  cat(sprintf("%-15s r_12 = %.3f   (n = %d, banda +-%.3f)\n", nm,
              acf(r, lag.max = 12, plot = FALSE)$acf[13], length(r), qnorm(0.975) / sqrt(length(r))))
}

cat("\n== A7 · desviacion tipica anual del residuo de la multiplicativa, en miles ==\n")
res <- as.numeric(datasets::AirPassengers) - as.numeric(dm$trend) * as.numeric(dm$seasonal)
an <- rep(1949:1960, each = 12)
s <- tapply(res, an, sd, na.rm = TRUE)
print(round(s, 1))
cat(sprintf("1949-1957: de %.1f a %.1f · 1958-1960: %s\n", min(s[1:9]), max(s[1:9]),
            paste(sprintf("%.1f", s[10:12]), collapse = ", ")))
cat(sprintf("media 1958-1960 / media 1949-1951: %.1f veces\n", mean(s[10:12]) / mean(s[1:3])))
cat(sprintf("media 1958-1960 / media 1949-1957: %.1f veces\n", mean(s[10:12]) / mean(s[1:9])))
