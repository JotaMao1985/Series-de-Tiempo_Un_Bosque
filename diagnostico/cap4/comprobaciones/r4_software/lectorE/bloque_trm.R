library(forecast); library(tseries)

# TRM mensual: promedio de cada mes de la TRM diaria (Superintendencia
# Financiera, publicada en datos.gov.co), de enero de 2015 a junio de 2026.
# Copia fija de los 138 meses con que se calcularon estas cifras, la misma de
# los capitulos 2 y 3: se lee de la carpeta de trabajo si el archivo ya esta
# ahi; si no, de la pagina del curso.
archivo <- "trm_mensual_2015-01_2026-06.csv"
if (!file.exists(archivo))
  archivo <- paste0("https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/", archivo)
trm <- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)
length(trm)
#> [1] 138

# --- Etapa 1: d ---------------------------------------------------------
prueba <- function(t) round(c(estad = unname(t$statistic), p = t$p.value), 3)
suppressWarnings(rbind(adf_nivel  = prueba(adf.test(trm)),
                       kpss_nivel = prueba(kpss.test(trm)),
                       adf_d1     = prueba(adf.test(diff(trm))),
                       kpss_d1    = prueba(kpss.test(diff(trm)))))
#>             estad     p
#> adf_nivel  -1.978 0.585
#> kpss_nivel  2.243 0.010      KPSS topa en su tabla: "p < 0.01"
#> adf_d1     -3.880 0.017
#> kpss_d1     0.241 0.100      y aqui "p > 0.10"
c(ndiffs = ndiffs(trm), nsdiffs = nsdiffs(trm))
#>  ndiffs nsdiffs
#>       1       0

# --- Etapa 1: p y q -----------------------------------------------------
r <- Acf(diff(trm), lag.max = 20, plot = FALSE)$acf[-1]
banda <- 1.96 / sqrt(length(diff(trm)))
round(c(rho1 = r[1], rho8 = r[8], banda = banda), 3)
#>   rho1   rho8  banda
#>  0.088 -0.190  0.167
which(abs(r) > banda)                         # la unica barra fuera, de veinte
#> [1] 8

# --- Etapa 2: la rejilla con d = 1, y auto.arima ------------------------
aicc <- function(f) {
  k <- length(f$coef) + 1; f$aic + 2 * k * (k + 1) / (f$nobs - k - 1)
}
rej <- expand.grid(p = 0:2, q = 0:2)
ajustes <- lapply(seq_len(nrow(rej)), function(i)
  arima(trm, order = c(rej$p[i], 1, rej$q[i]), method = "ML"))
rej$AICc <- round(sapply(ajustes, aicc), 2)
rej$BIC  <- round(sapply(ajustes, BIC), 2)
head(rej[order(rej$AICc), ], 3)
#>   p q    AICc     BIC
#> 9 2 2 1703.38 1717.52      <- minimo de AICc
#> 1 0 0 1705.94 1708.83      <- minimo de BIC
#> 4 0 1 1706.70 1712.45
arimaorder(auto.arima(trm, stepwise = FALSE, approximation = FALSE))
#> p d q
#> 0 1 0

# --- El minimo de AICc, descartado por sus raices -----------------------
f212 <- ajustes[[which(rej$p == 2 & rej$q == 2)]]
round(coef(f212), 3)
#>    ar1    ar2    ma1    ma2
#>  0.661 -0.992 -0.623  1.000
round(c(ar = Mod(polyroot(c(1, -coef(f212)[1:2]))),
        ma = Mod(polyroot(c(1,  coef(f212)[3:4])))), 4)
#>    ar1    ar2    ma1    ma2
#> 1.0042 1.0042 1.0000 1.0000      el MA, sobre el circulo: no invertible

# --- Etapa 3: diagnostico de la caminata aleatoria ----------------------
rw <- arima(trm, order = c(0, 1, 0), method = "ML")
e  <- residuals(rw)
round(c(lb20 = Box.test(e, lag = 20, type = "Ljung-Box")$p.value,
        lb12 = Box.test(e, lag = 12, type = "Ljung-Box")$p.value,
        shapiro = shapiro.test(e)$p.value,
        lb12_cuadrados = Box.test(e^2, lag = 12,
                                  type = "Ljung-Box")$p.value), 4)
#>           lb20           lb12        shapiro lb12_cuadrados
#>         0.1890         0.2059         0.0006         0.8570
fd <- Arima(trm, order = c(0, 1, 0), include.drift = TRUE)
round(c(deriva = coef(fd)[["drift"]], ee = sqrt(fd$var.coef[1, 1])), 2)
#> deriva     ee
#>   8.00  10.36

# --- Etapa 4: el abanico, y_T +- z * sigma * sqrt(h) --------------------
s <- sqrt(rw$sigma2); z <- qnorm(0.975); yT <- tail(as.numeric(trm), 1)
h <- c(1, 3, 6, 12, 24)
round(cbind(h, sigma_h = s * sqrt(h), semiancho = z * s * sqrt(h),
            inf = yT - z * s * sqrt(h), sup = yT + z * s * sqrt(h)), 2)
#>       h sigma_h semiancho     inf     sup
#> [1,]  1  121.48    238.09 3259.00 3735.18
#> [2,]  3  210.40    412.38 3084.71 3909.47
#> [3,]  6  297.55    583.19 2913.90 4080.28
#> [4,] 12  420.80    824.76 2672.33 4321.85
#> [5,] 24  595.11   1166.39 2330.70 4663.48
fc <- forecast(rw, h = 24, level = 95)
max(abs(fc$upper[h] - (yT + z * s * sqrt(h))))
#> [1] 0                 forecast() da el mismo abanico

# --- Cuantos cambios reales caen fuera del 95 % -------------------------
d1 <- diff(trm); d12 <- diff(trm, lag = 12)
c(fuera_1 = sum(abs(d1) > z * s), por_arriba = sum(d1 > z * s), de = length(d1))
#>    fuera_1 por_arriba         de
#>          6          5        137
c(fuera_12 = sum(abs(d12) > z * s * sqrt(12)), de = length(d12))
#> fuera_12       de
#>       11      126
curtosis <- function(x) mean((x - mean(x))^4) / mean((x - mean(x))^2)^2
round(c(curtosis_1 = curtosis(d1), curtosis_12 = curtosis(d12)), 1)
#>  curtosis_1 curtosis_12
#>         5.1         2.8
asimetria <- function(x) mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5
round(c(asimetria_1 = asimetria(d1)), 2)
#> asimetria_1
#>        0.76

# --- Lo que el intervalo nominal no recoge ------------------------------
# El 80 % a un mes (Modulo 9): cuantos cambios caen dentro
round(c(cubre_80_a_un_mes = mean(abs(d1) <= qnorm(0.90) * s)), 3)
#> cubre_80_a_un_mes
#>             0.839
# Cuadrado medio de los cambios a 3, 6 y 12 meses frente a h * sigma^2
round(sapply(c(3, 6, 12), function(h) mean(diff(trm, lag = h)^2) / (h * s^2)), 2)
#> [1] 1.10 1.14 1.07