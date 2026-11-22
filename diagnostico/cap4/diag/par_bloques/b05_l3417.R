library(forecast); library(tseries)

# --- Evidencia 2: la varianza por orden de diferencia --------------------
# OJO: diff(x, differences = 0) LANZA UN ERROR en R, no es la identidad.
for (d in 0:3) {
  x <- if (d == 0) Nile else diff(Nile, differences = d)
  cat(sprintf("d = %d  n = %3d  var = %10.2f\n", d, length(x), var(x)))
}
#> d = 0  n = 100  var =   28637.95
#> d = 1  n =  99  var =   28268.34      <- minimo
#> d = 2  n =  98  var =   80055.01
#> d = 3  n =  97  var =  262507.29

# --- Evidencia 3: las pruebas -------------------------------------------
adf.test(Nile)$p.value          # H0: hay raiz unitaria
#> [1] 0.06419542                no rechaza (al 5 %): diferenciar
kpss.test(Nile)$statistic       # H0: es estacionaria
#> KPSS Level
#>  0.9654349                    rechaza (p < 0.01): diferenciar
# (kpss.test avisa "p-value smaller than printed p-value": la tabla se acaba
#  en 0.01, no es un error)

# --- Y las tres respuestas de ndiffs ------------------------------------
sapply(c("kpss", "adf", "pp"), function(t) ndiffs(Nile, test = t))
#> kpss  adf   pp
#>    1    0    0            <- el defecto es "kpss", y es el unico que dice 1
# (el ADF de ndiffs es urca::ur.df(type = "drift", lags = 1): solo constante y
#  un rezago, no la especificacion con tendencia y k = 4 de adf.test)

# --- El experimento del escalon -----------------------------------------
set.seed(2026)
escalon <- as.numeric(1:100 >= 29)      # 1899 es la observacion 29
simula <- function(beta, reps = 400) {       # beta = tamano del escalon
  mean(replicate(reps, {
    x <- 1000 + beta * escalon + rnorm(100, 0, 127.03)
    suppressWarnings(kpss.test(x)$p.value) <= 0.05
  }))
}
c(sin_escalon = simula(0), con_el_del_Nilo = simula(-247.78))
#>     sin_escalon con_el_del_Nilo
#>           0.045           1.000