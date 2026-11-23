# fuentes_comprobaciones.R · comprobaciones en R detrás del inventario de fuentes del capítulo 5 (SARIMA).
# No escribe nada fuera de la salida estándar. Uso (desde cualquier carpeta):
#   Rscript diagnostico/cap5/diag/fuentes_comprobaciones.R > diagnostico/cap5/diag/fuentes_comprobaciones_r.out
# De las ayudas de R solo se imprimen booleanos: el texto de la ayuda no se copia. Los números sí se imprimen.
suppressMessages(library(forecast))
cat("R:", R.version.string, " · forecast", as.character(packageVersion("forecast")), "\n")

ayuda <- function(tema, paquete) {
  h <- do.call(help, list(tema, package = paquete))
  tf <- tempfile(); tools::Rd2txt(utils:::.getHelpFile(h[1]), out = tf, options = list(underline_titles = FALSE))
  gsub("\\s+", " ", paste(readLines(tf), collapse = " "))
}
ap <- log(AirPassengers)

cat("\n== nsdiffs: prueba por defecto y lo que dice la ayuda (l. 4203-4209 del capítulo)\n")
fn <- formals(nsdiffs)
cat("test por defecto (primer valor):", as.character(eval(fn$test))[1], " · max.D =", eval(fn$max.D), "\n")
a <- ayuda("nsdiffs", "forecast")
cat("?nsdiffs dice que 'seas' es el valor por defecto:", grepl("test = \"seas\"\\) \\(default\\)|\"seas\"\\) \\(default\\)", a) || grepl("seas.{0,10}\\(default\\)", a), "\n")
cat("?nsdiffs: fuerza estacional con umbral 0.64:", grepl("0\\.64", a), " · cita a Wang, Smith y Hyndman (2006):", grepl("Wang", a) && grepl("2006", a), "\n")
cat("?nsdiffs: ofrece ocsb, hegy y ch:", grepl("ocsb", a) && grepl("hegy", a) && grepl("\"ch\"", a), " · cita a Osborn et al. (1988):", grepl("Osborn|Birchenhall", a), " · cita a Canova y Hansen (1995):", grepl("Canova", a), "\n")
cat("?nsdiffs menciona la versión 8.x o un cambio de valor por defecto:", grepl("8\\.[0-9]|changed|previous|formerly|used to", a), "\n")
cat("nsdiffs('seas') y nsdiffs('ocsb') sobre log(AirPassengers):", nsdiffs(ap), nsdiffs(ap, test = "ocsb"), "\n")
cat("nsdiffs('seas') y nsdiffs('ocsb') sobre USAccDeaths:", nsdiffs(USAccDeaths), nsdiffs(USAccDeaths, test = "ocsb"), "\n")
cat("ndiffs(USAccDeaths) crudo y tras la diferencia estacional:", ndiffs(USAccDeaths), ndiffs(diff(USAccDeaths, lag = 12)), "\n")
cat("?ndiffs tiene como ejemplo ndiffs(diff(log(AirPassengers), 12)):", grepl("ndiffs\\(diff\\(log\\(AirPassengers\\), 12\\)\\)", ayuda("ndiffs", "forecast")), "\n")

cat("\n== rezagos por defecto de la ACF (l. 3133 del capítulo: «los 20 o 24 por defecto»)\n")
cat("acf() sobre log(AirPassengers):", length(acf(ap, plot = FALSE)$acf) - 1, " · Acf():", length(Acf(ap, plot = FALSE)$acf) - 1, " · pacf():", length(pacf(ap, plot = FALSE)$acf), "\n")
cat("?acf: el valor por defecto de lag.max es 10*log10(N/m):", grepl("log10\\(N/m\\)", ayuda("acf", "stats")), "\n")

cat("\n== sigma2 de Arima y de arima (l. 3677-3681 y 5055 del capítulo)\n")
f <- Arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
g <- arima(ap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
cat("sigma2 Arima:", round(f$sigma2, 6), " · sigma2 arima:", round(g$sigma2, 6), " · nobs:", f$nobs, "\n")
cat("SSR/(n-2):", round(sum(residuals(f)^2) / (f$nobs - 2), 6), " · SSR/n:", round(sum(residuals(f)^2) / f$nobs, 6), "\n")
cat("?Arima dice que sigma2 es el MLE ajustado por sesgo:", grepl("bias adjusted", ayuda("Arima", "forecast")), " · ?arima dice «the MLE»:", grepl("sigma2: the MLE", ayuda("arima", "stats")), "\n")
cat("?arima trae como ejemplo el airline sobre USAccDeaths:", grepl("arima\\(USAccDeaths, order = c\\(0, ?1, ?1\\), seasonal", ayuda("arima", "stats")), "\n")

cat("\n== Ljung-Box con 2m rezagos en checkresiduals (M6, M7)\n")
cat("lag por defecto de checkresiduals en una serie mensual (ver 'Total lags used'):\n")
print(capture.output(checkresiduals(f, plot = FALSE))[7])
cat("qchisq(0.95, 22) =", round(qchisq(0.95, 22), 2), "\n")

cat("\n== Fourier (M10)\n")
cat("columnas de fourier(ap, K) para K = 1..6:", sapply(1:6, function(K) ncol(fourier(ap, K = K))), "\n")
cat("?fourier: devuelve 2*K columnas:", grepl("2\\*K", ayuda("fourier", "forecast")), "\n")
cat("?stlm: reestacionaliza con el último año del componente estacional:", grepl("last year of the seasonal component", ayuda("stlm", "forecast")), "\n")
cat("?BoxCox.lambda: método de Guerrero = mínimo coeficiente de variación de subseries:", {b <- ayuda("BoxCox.lambda", "forecast"); grepl("Guerrero", b) && grepl("coefficient of variation", b)}, "\n")
cat("auto.arima: opciones seasonal y D disponibles:", all(c("seasonal", "D", "max.P", "max.Q", "seasonal.test") %in% names(formals(auto.arima))), "\n")
set.seed(1); z <- ts(3 * sin(2 * pi * (1:800) / 365) + rnorm(800), frequency = 365)
cat("auto.arima sobre la serie simulada con m = 365:", as.character(auto.arima(z)), "\n")

cat("\n== Pascua: fechas de 1949 a 1960 por el algoritmo del bloque (cuántas veces cae en marzo)\n")
pascua <- function(anio) {
  a <- anio %% 19; b <- anio %/% 100; cc <- anio %% 100
  d <- b %/% 4; e <- b %% 4; f <- (b + 8) %/% 25; g <- (b - f + 1) %/% 3
  h <- (19*a + b - d - g + 15) %% 30; i <- cc %/% 4; k <- cc %% 4
  l <- (32 + 2*e + 2*i - h - k) %% 7; m <- (a + 11*h + 22*l) %/% 451
  (h + l - 7*m + 114) %/% 31
}
cat("meses de Pascua 1949-1960:", sapply(1949:1960, pascua), " · en marzo:", sum(sapply(1949:1960, pascua) == 3), "\n")

cat("\n== diff(x, differences = 0) (l. 4140 del capítulo)\n")
cat("diff(x, differences = 0):", tryCatch({diff(c(1, 3, 6, 10), differences = 0); "sin error"}, error = function(e) paste("ERROR:", conditionMessage(e))), "\n")
