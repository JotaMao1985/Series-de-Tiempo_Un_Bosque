# Verificador A: frecuencia de lo que muestran las semillas de M3 (43) y M8 (2026), y M8 con phi = 0.6
suppressPackageStartupMessages(library(forecast))
pr <- function(x) c(kpss = ndiffs(x, test = "kpss"), adf = ndiffs(x, test = "adf"), pp = ndiffs(x, test = "pp"))
r <- t(sapply(1:500, function(s) { set.seed(s); e <- as.numeric(1:120 >= 71)
  y <- ts(10 + 3 * e + arima.sim(n = 120, model = list(ar = 0.5)))
  c(reparto_nilo = all(pr(y) == c(1, 0, 0)),
    tramos_kpss0 = ndiffs(window(y, end = 70)) == 0 && ndiffs(window(y, start = 71)) == 0,
    tramos_tres0 = all(pr(window(y, end = 70)) == 0) && all(pr(window(y, start = 71)) == 0)) }))
cat("M3, 500 semillas: reparto 1/0/0 del Nilo en la serie completa:", mean(r[,1]),
    "| y KPSS 0 en los dos tramos:", mean(r[,1] & r[,2]), "| reparto y las tres 0 en los dos tramos:", mean(r[,1] & r[,3]), "\n")
cat("semilla 43:", r[43, ], "\n")
q <- sapply(1:200, function(s) { set.seed(s); y <- arima.sim(n = 200, model = list(ar = 0.6))
  f <- try(arima(y, order = c(1,1,1), method = "ML"), silent = TRUE)
  c(if (inherits(f, "try-error")) NA else Mod(polyroot(c(1, coef(f)[["ma1"]]))), acf(diff(y), plot = FALSE)$acf[2]) })
cat("M8 con phi = 0.6: raiz MA del (1,1,1) < 1.05:", round(mean(q[1,] < 1.05, na.rm = TRUE), 3), " mediana r1 de la diferencia:", round(median(q[2,]), 3), "\n")
# M2: frecuencia conjunta de los cuatro hallazgos que muestra la semilla 2026
LB <- function(f, k) Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = k)$p.value
m2 <- t(sapply(1:200, function(s) suppressWarnings({ set.seed(s)
  y <- arima.sim(n = 200, model = list(order = c(2,1,0), ar = c(0.4, 0.3)))
  f <- lapply(list(c(0,1,1), c(2,2,1), c(2,1,2), c(2,1,0)), function(o) try(arima(y, order = o, method = "ML"), silent = TRUE))
  if (any(sapply(f, inherits, "try-error"))) return(rep(NA, 5))
  p <- pacf(diff(y), lag.max = 6, plot = FALSE)$acf[,1,1]; b <- 1.96/sqrt(199)
  c(LB(f[[1]], 1) < 0.05, Mod(polyroot(c(1, coef(f[[2]])[["ma1"]]))) < 1.01,
    max(sqrt(diag(f[[3]]$var.coef))) > 2 * max(sqrt(diag(f[[4]]$var.coef))),
    all(abs(p[1:2]) > b) && all(abs(p[3:6]) < b), LB(f[[2]], 3) > 0.05 && LB(f[[3]], 4) > 0.05) })))
cat("M2, 200 semillas: LB rechaza el (0,1,1):", mean(m2[,1], na.rm=TRUE), "| raiz MA del (2,2,1) < 1.01:", mean(m2[,2], na.rm=TRUE),
    "| ee del (2,1,2) > 2x:", mean(m2[,3], na.rm=TRUE), "| PACF corta en 2:", mean(m2[,4], na.rm=TRUE),
    "| (2,2,1) y (2,1,2) pasan LB:", mean(m2[,5], na.rm=TRUE), "| los cinco a la vez:", mean(rowSums(m2) == 5, na.rm=TRUE), "| sin ajuste:", sum(is.na(m2[,1])), "\n")
