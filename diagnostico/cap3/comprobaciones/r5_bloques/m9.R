library(forecast)

# (a) Hay que transformar? La elasticidad amplitud-nivel del modulo,
#     en bloques de 10 anios
elasticidad <- function(x, k) {
  g <- rep(seq_len(length(x) %/% k), each = k)
  x <- as.numeric(x)[seq_along(g)]
  niv <- tapply(x, g, mean); amp <- tapply(x, g, sd)
  aj <- lm(log(amp) ~ log(niv))
  c(b = coef(aj)[[2]], confint(aj)[2, ], R2 = summary(aj)$r.squared)
}
round(elasticidad(lynx, 10), 3)
min(lynx)                      # sin ceros: el logaritmo SI es una opcion
round(BoxCox.lambda(lynx, method = "guerrero"), 4)

# (b) La rejilla del Modulo 8 (los once candidatos) en las dos escalas
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
rejilla <- list(c(1,0), c(2,0), c(3,0), c(4,0), c(0,1), c(0,2), c(0,3),
                c(1,1), c(2,1), c(1,2), c(2,2))
# en log(lynx), el ARMA(2,1) avisa de un posible problema de convergencia (optim code = 1);
# no lo elige ningun criterio, y suppressWarnings() solo calla ese aviso
compara <- function(x) do.call(rbind, lapply(rejilla, function(pq) {
  aj <- suppressWarnings(arima(x, order = c(pq[1], 0, pq[2]), method = "ML"))
  data.frame(modelo = sprintf("ARMA(%d,%d)", pq[1], pq[2]),
             AICc = round(aicc(aj, length(x)), 2), BIC = round(BIC(aj), 2),
             LB12 = round(Box.test(residuals(aj), lag = 12, type = "Ljung-Box",
                                   fitdf = sum(pq))$p.value, 4))
}))
cruda <- compara(lynx); logar <- compara(log(lynx))
cruda[order(cruda$AICc), ][1:4, ]
logar[order(logar$AICc), ][1:4, ]
mejor <- function(t) c(AICc = t$modelo[which.min(t$AICc)], BIC = t$modelo[which.min(t$BIC)])
rbind(cruda = mejor(cruda), logaritmo = mejor(logar))

# (c) El AR(2) en cada escala: pseudo-periodo, Ljung-Box y normalidad de los residuales
mira <- function(x) {
  f <- arima(x, order = c(2, 0, 0), method = "ML")
  c(phi1 = coef(f)[["ar1"]], phi2 = coef(f)[["ar2"]],
    pseudoperiodo = 2 * pi / Arg(polyroot(c(1, -coef(f)[1:2]))[1]),
    LB12 = Box.test(residuals(f), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value,
    Shapiro = shapiro.test(residuals(f))$p.value)
}
round(rbind(cruda = mira(lynx), logaritmo = mira(log(lynx))), 4)
