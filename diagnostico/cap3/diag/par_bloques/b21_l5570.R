## ---- Caso 1: manchas solares en raiz cuadrada -------------------------
manchas <- window(sunspot.year, start = 1770, end = 1869)

min(manchas)          # el logaritmo NO es una opcion
#> [1] 0
sum(manchas == 0)
#> [1] 1

library(forecast)
# Guerrero exige datos ESTRICTAMENTE positivos y aqui hay un cero, asi que
# se desplaza la serie una unidad (con el cero crudo, R lanza un aviso).
round(BoxCox.lambda(manchas + 1, method = "guerrero"), 4)
#> [1] 0.3062      entre el logaritmo (0) y la raiz cuadrada (0.5)

ar2s <- arima(sqrt(manchas), order = c(2, 0, 0), method = "ML")
round(coef(ar2s), 4)
#>     ar1     ar2  intercept
#>  1.4027 -0.6853     6.3317

Box.test(residuals(ar2s), lag = 12, type = "Ljung-Box", fitdf = 2)$p.value
#> [1] 0.1643575          <- ahora SI pasa

phi <- coef(ar2s)[1:2]
round(2 * pi / Arg(polyroot(c(1, -phi))[1]), 4)
#> [1] 11.2178            anios; el ciclo solar documentado es ~11

# --- El modelo como polinomio: modulo Y angulo de la raiz --------------
raices <- polyroot(c(1, -phi))     # phi(B) = 1 - 1.4027 B + 0.6853 B^2
round(raices, 4)
#> [1] 1.0234+0.6418i 1.0234-0.6418i
round(c(modulo = Mod(raices)[1], angulo = Arg(raices)[1]), 4)
#> modulo angulo
#> 1.2080 0.5601            modulo > 1: estacionario; 2*pi/angulo = 11.2178

# Los pesos psi del Modulo 4, sobre los coeficientes ESTIMADOS.
# ARMAtoMA() devuelve psi_1 en adelante; psi_0 = 1 va por convenio.
psi <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 11))
round(psi, 4)
#>  [1]  1.0000  1.4027  1.2822  0.8372  0.2957 -0.1590 -0.4257 -0.4881 -0.3929
#> [10] -0.2167 -0.0346  0.0999      cambian de signo entre el 4 y el 5
# Forma cerrada del AR(2) con raices complejas: envolvente x oscilacion
Rmod <- unname(sqrt(-phi[2])); w <- Arg(raices)[1]
round(Rmod^(0:11) * sin((0:11 + 1) * w) / sin(w), 4)
#>  [1]  1.0000  1.4027  1.2822  0.8372  0.2957 -0.1590 -0.4257 -0.4881 -0.3929
#> [10] -0.2167 -0.0346  0.0999      identica a la recursion
# theta(B) = 1 no tiene raices: un AR puro es invertible y sus pi se acaban
round(c(pi1 = -phi[[1]], pi2 = -phi[[2]]), 4)
#>     pi1     pi2
#> -1.4027  0.6853

# De los psi salen las bandas del pronostico, que es lo que hace forecast()
ee <- sqrt(ar2s$sigma2 * cumsum(psi^2))
round(qnorm(0.975) * ee[1:6], 4)
#> [1] 2.2697 3.9098 4.8739 5.2312 5.2741 5.2864
f <- forecast(ar2s, h = 6, level = 95)
round(as.numeric((f$upper - f$lower) / 2), 4)
#> [1] 2.2697 3.9098 4.8739 5.2312 5.2741 5.2864   <- lo mismo

# El techo: en un proceso ESTACIONARIO la suma de psi^2 converge
psi_largo <- c(1, ARMAtoMA(ar = phi, ma = numeric(0), lag.max = 600))
round(c(suma = sum(psi_largo^2), gamma0 = ar2s$sigma2 * sum(psi_largo^2),
        var_muestral = var(sqrt(manchas))), 4)
#>         suma       gamma0 var_muestral
#>       6.1360       8.2283       8.1490   el abanico no pasa de gamma0

# Comparacion directa con la serie cruda
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
c(cruda_ar2 = aicc(arima(manchas, order = c(2,0,0), method = "ML"), 100),
  cruda_21  = aicc(arima(manchas, order = c(2,0,1), method = "ML"), 100))
#> cruda_ar2  cruda_21
#>  838.3012  834.7292        <- sobre la cruda gana el ARMA(2,1)
c(sqrt_ar2 = aicc(ar2s, 100),
  sqrt_21  = aicc(arima(sqrt(manchas), order = c(2,0,1), method = "ML"), 100))
#>  sqrt_ar2   sqrt_21
#>  323.9970  325.4128        <- sobre la raiz gana el AR(2)

## ---- Caso 2: log-retornos de la TRM -----------------------------------
# trm: serie mensual del Capitulo 2 (promedio mensual, SFC via datos.gov.co).
# Se reconstruye aqui para que el bloque sea autonomo.
url <- paste0("https://www.datos.gov.co/resource/32sa-8pi3.json",
              "?$select=vigenciadesde,valor&$limit=50000")
crudo <- jsonlite::fromJSON(url)
diario <- data.frame(fecha = as.Date(substr(crudo$vigenciadesde, 1, 10)),
                     valor = as.numeric(crudo$valor))
# Dos pasos: order() devuelve INDICES, no un vector logico, y combinarlo con
# & mediante  order(...) & fecha >= ...  no ordena nada (todo indice != 0 se
# coacciona a TRUE). Filtrar y ordenar son operaciones distintas.
diario <- diario[diario$fecha >= as.Date("2015-01-01"), ]
diario <- diario[order(diario$fecha), ]
mes <- format(diario$fecha, "%Y-%m")
prom <- tapply(diario$valor, mes, mean)
prom <- prom[names(prom) <= "2026-06"]
trm <- ts(as.numeric(prom), start = c(2015, 1), frequency = 12)

ret <- diff(log(trm)) * 100
length(ret)
#> [1] 137

round(1.96 / sqrt(length(ret)), 4)      # banda
#> [1] 0.1675
round(acf(ret, lag.max = 6, plot = FALSE)$acf[-1], 3)
#> [1]  0.105 -0.077 -0.078  0.006  0.193  0.123

sapply(c(6, 12, 20), function(h)
  round(Box.test(ret, lag = h, type = "Ljung-Box")$p.value, 4))
#> [1] 0.0931 0.0601 0.0599

ma1 <- arima(ret, order = c(0, 0, 1), method = "ML")
round(c(theta = coef(ma1)[["ma1"]], ee = sqrt(ma1$var.coef[1, 1])), 4)
#>  theta     ee
#> 0.1262 0.0912

# Comparacion JUSTA: los dos sin media
c(ma1_sin_media   = aicc(arima(ret, order = c(0,0,1), include.mean = FALSE,
                               method = "ML"), 137),
  ruido_sin_media = aicc(arima(ret, order = c(0,0,0), include.mean = FALSE,
                               method = "ML"), 137))
#>   ma1_sin_media ruido_sin_media
#>        722.6530        722.6632

# Volatilidad: estructura en los cuadrados?
round(Box.test(ret^2, lag = 12, type = "Ljung-Box")$p.value, 4)
#> [1] 0.9166             <- tampoco