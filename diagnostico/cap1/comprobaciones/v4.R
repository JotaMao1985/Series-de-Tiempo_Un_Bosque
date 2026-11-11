elasticidad <- function(x) {
  anios <- floor(time(x)); completos <- names(which(table(anios) == frequency(x)))
  v <- as.numeric(x)
  nivel <- tapply(v, anios, mean)[completos]; amplitud <- tapply(v, anios, function(z) max(z) - min(z))[completos]
  fit <- lm(log(amplitud) ~ log(nivel))
  list(r=c(b = unname(coef(fit)[2]), confint(fit)[2, ], R2 = summary(fit)$r.squared), nivel=nivel, amplitud=amplitud)
}
e1 <- elasticidad(co2); e2 <- elasticidad(AirPassengers)
print(round(e1$r,3)); print(round(e2$r,3))
cat("co2 range/mean:", (max(co2)-min(co2))/mean(co2), " AP:", (max(AirPassengers)-min(AirPassengers))/mean(AirPassengers), "\n")
n <- e1$nivel; a <- e1$amplitud; yrs <- as.numeric(names(n))
cat("co2 level first/last yr:", n[1], n[length(n)], " growth %:", 100*(n[length(n)]/n[1]-1), " years:", length(n), "\n")
fa <- lm(a ~ yrs); print(summary(fa)$coefficients)
cat("mean amplitude:", mean(a), "\n")
# amplitude growth predicted by exact proportionality: a_t = c * nivel_t, c = mean(a)/mean(n)
c0 <- mean(a)/mean(n); pred <- c0*n; fp <- lm(pred ~ yrs); cat("slope if amplitude proportional to level:", coef(fp)[2], "\n")
# test b=1 for AP and b=0 for co2
cat("AP CI excludes 1?", e2$r[2] > 1, "  co2 CI excludes 0?", e1$r[2] > 0, " co2 CI contains 1?", e1$r[2] < 1 & e1$r[3] > 1, "\n")
# ratio amp/level for co2 trend over years
fr <- lm(I(a/n) ~ yrs); print(summary(fr)$coefficients)
