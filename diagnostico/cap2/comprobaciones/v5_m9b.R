suppressMessages(library(tseries))
set.seed(2026)
caminatas <- replicate(500, cumsum(rnorm(144)))
rechaza <- function(x) suppressWarnings(adf.test(x)$p.value) < 0.05
print(100 * mean(apply(caminatas, 2, rechaza)))
ee <- 100 * sqrt(0.05 * 0.95 / 500); print(round(ee, 2)); print(round(5 + c(-2, 2) * ee, 1))
set.seed(2026); a5000 <- 100 * mean(replicate(5000, rechaza(cumsum(rnorm(144))))); print(a5000)
print(100*sqrt(.05*.95/5000)); print(5+c(-2,2)*100*sqrt(.05*.95/5000)); print(100*sqrt(a5000/100*(1-a5000/100)/5000))
onda <- 4 * sin(2 * pi * (1:144) / 12)
print(100 * mean(apply(caminatas + onda, 2, rechaza)))
set.seed(2026); print(100 * mean(replicate(500, rechaza(rnorm(144)))))
# error de la diferencia de dos experimentos con p~0.2
print(100*sqrt(2*0.2*0.8/500)); print(100*sqrt(.216*.784/500+.176*.824/500))
# bloque autónomo: ¿el bloque corre solo? (en el HTML, set.seed antes de 5000 reinicia)
