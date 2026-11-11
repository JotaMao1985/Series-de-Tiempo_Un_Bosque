fz <- function(x) { st <- stl(x, s.window = "periodic")$time.series; R <- st[,3]
  c(FT = max(0, 1 - var(R)/var(st[,2]+R)), FS = max(0, 1 - var(R)/var(st[,1]+R))) }
el <- function(x) { an <- floor(time(x)); comp <- names(which(table(an) == frequency(x)))
  v <- as.numeric(x); niv <- tapply(v, an, mean)[comp]; amp <- tapply(v, an, function(z) max(z)-min(z))[comp]
  f <- lm(log(amp) ~ log(niv)); c(b = unname(coef(f)[2]), confint(f)[2,], R2 = summary(f)$r.squared,
  rango_nivel = (max(niv)-min(niv))/mean(niv)) }
for (nm in c("nottem","UKgas","JohnsonJohnson","ldeaths","UKDriverDeaths","USAccDeaths","co2","AirPassengers")) {
  x <- get(nm); cat(sprintf("%-15s f=%2d n=%3d  FT=%.3f FS=%.3f | b=%.2f IC[%.2f,%.2f] R2=%.2f rangoNivel=%.2f\n",
    nm, frequency(x), length(x), fz(x)[1], fz(x)[2], el(x)[1], el(x)[2], el(x)[3], el(x)[4], el(x)[5])) }
cat("lynx: frecuencia", frequency(lynx), "n", length(lynx), "; sunspot.year frecuencia", frequency(sunspot.year), "\n")
# distancia entre picos de lynx (ciclo de duración variable)
pk <- which(diff(sign(diff(as.numeric(lynx)))) == -2) + 1
pk <- pk[as.numeric(lynx)[pk] > median(lynx)]
cat("lynx: separación entre picos altos (años):", diff(time(lynx)[pk]), "\n")
suppressMessages({library(tsibble); library(dplyr)})
d <- cbind(hombres = mdeaths, mujeres = fdeaths)
tb <- as_tsibble(d)
print(tb, n = 3)
cat("key_vars:", key_vars(tb), " n_keys:", n_keys(tb), "\n")
