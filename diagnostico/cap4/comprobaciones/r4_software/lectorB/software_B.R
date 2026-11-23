# Lector B · M3 y M4: lo que el capítulo dice del software, comprobado ejecutando
suppressMessages({library(forecast); library(tseries); library(urca)})
cat("R", R.version.string, "| forecast", as.character(packageVersion("forecast")),
    "| tseries", as.character(packageVersion("tseries")), "| urca", as.character(packageVersion("urca")), "\n\n")

cat("== ndiffs: valor por defecto de test y cuerpo\n")
print(formals(ndiffs)$test); print(formals(ndiffs)$max.d)
cuerpo <- paste(deparse(body(ndiffs)), collapse = "\n")
cat("ur.df(x, type = 'drift') en el cuerpo:", grepl("ur.df\\(x, type = \"drift\"", cuerpo, fixed = FALSE) || grepl("type = \"drift\"", cuerpo), "\n")
cat("ur.df en el cuerpo:", grepl("ur.df", cuerpo), " ur.pp:", grepl("ur.pp", cuerpo), " kpss:", grepl("kpss", cuerpo), "\n")
cat(grep("ur.df|ur.pp|kpss|urca", deparse(body(ndiffs)), value = TRUE), sep = "\n")
cat("\nndiffs(Nile) por prueba:", sapply(c("kpss","adf","pp"), function(t) ndiffs(Nile, test = t)), "\n")
cat("formals(ur.df)$lags:", formals(urca::ur.df)$lags, "\n")

cat("\n== auto.arima: test por defecto\n")
print(formals(auto.arima)$test)

cat("\n== ADF por urca: tau2 del Nilo (drift, lags = 1) y valor crítico al 5 %\n")
u <- ur.df(as.numeric(Nile), type = "drift", lags = 1)
print(round(u@teststat, 4)); print(u@cval)
cat("cval tau2 5pct con n=100:", u@cval["tau2", "5pct"], "\n")

cat("\n== tseries: adf.test(Nile), kpss.test(Nile) corto y largo, PP.test(Nile)\n")
a <- adf.test(Nile); cat("adf: stat", round(a$statistic, 4), " p", round(a$p.value, 4), " k", a$parameter, "\n")
cat("k por defecto (n=100):", trunc((100 - 1)^(1/3)), "\n")
k1 <- suppressWarnings(kpss.test(Nile)); cat("kpss corto: stat", round(k1$statistic, 4), " p", k1$p.value, " lag", k1$parameter, "\n")
k2 <- suppressWarnings(kpss.test(Nile, lshort = FALSE)); cat("kpss largo: stat", round(k2$statistic, 4), " p", k2$p.value, " lag", k2$parameter, "\n")
w <- NULL; withCallingHandlers(kpss.test(Nile), warning = function(m) { w <<- conditionMessage(m); invokeRestart("muffleWarning") })
cat("aviso de kpss.test(Nile):", w, "\n")
p <- PP.test(Nile); cat("PP.test(Nile): stat", round(p$statistic, 4), " p", p$p.value, " lag", p$parameter, "\n")
cat("método:", p$method, "\n")
cat("kpss.test: 0.463 en el código:", any(grepl("0.463", deparse(body(tseries::kpss.test)), fixed = TRUE)), "\n")
cat(grep("0.463|crit|table", deparse(body(tseries::kpss.test)), value = TRUE)[1:6], sep = "\n")

cat("\n== diff(differences = 0)\n")
r <- try(diff(Nile, differences = 0), silent = TRUE); cat(class(r), "|", as.character(r)[1], "\n")

cat("\n== varianza por d y cociente (cap. 2, M2.7)\n")
for (d in 0:3) { x <- if (d == 0) Nile else diff(Nile, differences = d); cat(sprintf("d=%d n=%d var=%.2f\n", d, length(x), var(x))) }
r1 <- acf(Nile, plot = FALSE)$acf[2]
cat("r1 =", round(r1, 4), " 2(1-r1) =", round(2*(1-r1), 3), " cociente =", round(var(diff(Nile))/var(Nile), 3), "\n")
cat("(var d=1 - var d=0)/var d=0 =", round((var(diff(Nile))-var(Nile))/var(Nile), 4), "  var d=2/var d=1 =", round(var(diff(Nile,differences=2))/var(diff(Nile)), 3), " var d=2/var d=0 =", round(var(diff(Nile,differences=2))/var(Nile), 3), "\n")

cat("\n== ACF/PACF de diff(Nile) (M4)\n")
w1 <- diff(Nile); n <- length(w1)
cat("banda 1.96/sqrt(99) =", round(1.96/sqrt(n), 4), "\n")
a <- acf(w1, lag.max = 20, plot = FALSE)$acf[-1]; pa <- pacf(w1, lag.max = 20, plot = FALSE)$acf
cat("acf 1..8:", round(a[1:8], 4), "\n")
cat("fuera de banda:", which(abs(a) > 1.96/sqrt(n)), " (ACF)\n")
cat("pacf 1..6:", round(pa[1:6], 4), "\n")
cat("pacf fuera de banda:", which(abs(pa) > 1.96/sqrt(n)), "\n")
cat("dim(pacf()$acf):", dim(pacf(w1, plot = FALSE)$acf), "\n")
cat("acf Nile 1..6:", round(acf(Nile, plot = FALSE, lag.max = 6)$acf[-1], 4), "\n")
cat("d = 2: r1 =", round(acf(diff(Nile, differences = 2), plot = FALSE)$acf[2], 3), "\n")
cat("AR(1) phi=.5: 0.5^3 =", 0.5^3, " con n = 100 banda =", round(1.96/sqrt(100), 3), "\n")
ma1 <- arima(Nile, order = c(0,1,1), method = "ML")
cat("theta =", round(coef(ma1), 4), " ee =", round(sqrt(ma1$var.coef[1,1]), 4), " t =", round(coef(ma1)/sqrt(ma1$var.coef[1,1]), 2), " sigma2 =", round(ma1$sigma2, 2), "\n")
cat("LB(20) fitdf=1 p =", Box.test(residuals(ma1), lag = 20, type = "Ljung-Box", fitdf = 1)$p.value, " alpha implícito =", round(1+coef(ma1), 3), "\n")
ses_fit <- ses(Nile); cat("ses alpha =", round(ses_fit$model$par[["alpha"]], 4), "\n")
cat("AICc/BIC de (0,1,1),(1,1,1),(0,1,2),(1,1,0):\n")
for (o in list(c(0,1,1), c(1,1,1), c(0,1,2), c(1,1,0))) { f <- Arima(Nile, order = o, method = "ML"); cat(sprintf("(%d,%d,%d): AICc %.3f BIC %.3f\n", o[1], o[2], o[3], f$aicc, f$bic)) }
