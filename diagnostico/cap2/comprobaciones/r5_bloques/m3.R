y <- as.numeric(window(discoveries, start = 1927, end = 1936))
y
n <- length(y)
d <- y - mean(y)                          # desviaciones respecto de la media
mean(y)

# (a) y (b) Con el divisor T, aunque la suma del rezago k tenga T - k terminos
g0 <- sum(d^2) / n
g1 <- sum(d[1:(n - 1)] * d[2:n]) / n
g2 <- sum(d[1:(n - 2)] * d[3:n]) / n
c(g0 = g0, g1 = g1, g2 = g2)
round(c(r1 = g1 / g0, r2 = g2 / g0), 4)

# (c) acf() da lo mismo; dividiendo cada suma entre T - k, no
round(acf(y, lag.max = 2, plot = FALSE)$acf[2:3], 4)
round(c(sum(d[1:(n - 1)] * d[2:n]) / (n - 1),
        sum(d[1:(n - 2)] * d[3:n]) / (n - 2)) / g0, 4)

# (d) La banda con T = 10
round(1.96 / sqrt(n), 3)
