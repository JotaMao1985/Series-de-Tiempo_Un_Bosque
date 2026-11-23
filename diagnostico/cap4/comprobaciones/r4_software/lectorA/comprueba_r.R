# Lector A (M1, M2) · comprobaciones en R 4.6.0 (forecast 9.0.2)
suppressMessages(library(forecast))
cat(R.version.string, "| forecast", as.character(packageVersion("forecast")), "\n\n")

# c4-m1-28 y c4-m1-27: con el convenio de R (MA con signo mas), rho1 de un MA(1) tiene el signo de theta
cat("ARMAacf(ma = +0.5)[lag 1] =", round(ARMAacf(ma = 0.5, lag.max = 1)[2], 4), " (theta/(1+theta^2) = 0.4)\n")
cat("ARMAacf(ma = -0.5)[lag 1] =", round(ARMAacf(ma = -0.5, lag.max = 1)[2], 4), " (-0.4)\n")
set.seed(11)
y <- arima.sim(list(ma = 0.6), n = 2000)
cat("arima.sim(ma = +0.6): r1 =", round(acf(y, plot = FALSE, lag.max = 1)$acf[2], 3),
    "| arima(order=c(0,0,1)) ma1 =", round(coef(arima(y, order = c(0, 0, 1)))[["ma1"]], 3), "\n")

# c4-m1-20: arima.sim con order c(p,d,q) devuelve n + d valores y el primero es 0
set.seed(2026)
y2 <- arima.sim(list(order = c(1, 1, 1), ar = 0.2544, ma = -0.8741), n = 200)
cat("length(y2) =", length(y2), " primer valor =", y2[1], "\n")

# c4-m1-12: ARIMA(0,1,1) <-> suavizamiento exponencial simple, alpha = 1 + theta (convenio de suma de R)
f <- arima(Nile, order = c(0, 1, 1), method = "ML")
th <- coef(f)[["ma1"]]
s <- ses(Nile, h = 1)
cat("Nile: ARIMA(0,1,1) theta =", round(th, 4), "=> 1 + theta =", round(1 + th, 4),
    "| ses() alpha =", round(s$model$par[["alpha"]], 4), "\n")
# la ecuacion de ses: el pronostico a un paso es alpha*y_T + (1-alpha)*pronostico_anterior
al <- s$model$par[["alpha"]]
fit1 <- fitted(s)
cat("ses: max |fitted[t+1] - (alpha*y[t] + (1-alpha)*fitted[t])| =",
    signif(max(abs(fit1[-1] - (al * Nile[-100] + (1 - al) * fit1[-100]))), 3), "\n")

# c4-m1-23: la causa de que integrar el ARMA(1,1) del Nilo no dispare la varianza es theta ~ -1:
# varianza de largo plazo de w = sigma^2 (1+theta)^2 / (1-phi)^2 frente a gamma0
phi <- 0.2544; theta <- -0.8741
g0 <- (1 + 2 * phi * theta + theta^2) / (1 - phi^2)          # gamma0 / sigma^2 del ARMA(1,1)
lr <- (1 + theta)^2 / (1 - phi)^2                            # varianza de largo plazo / sigma^2
cat("gamma0/sigma^2 =", round(g0, 4), " largo plazo/sigma^2 =", round(lr, 4), " cociente lr/gamma0 =", round(lr / g0, 4), "\n")
phi0 <- 0.2544; lr0 <- 1 / (1 - phi0)^2; g00 <- 1 / (1 - phi0^2)
cat("sin MA: gamma0/sigma^2 =", round(g00, 4), " largo plazo/sigma^2 =", round(lr0, 4), " cociente =", round(lr0 / g00, 4), "\n")
# El bloque del capitulo (set.seed(2026)): razon de varianzas con y sin MA
set.seed(2026)
w <- arima.sim(list(ar = phi, ma = theta), n = 200); yy <- cumsum(w)
cat("razon con MA =", round(var(yy) / var(w), 3), "\n")
set.seed(2026)
w0 <- arima.sim(list(ar = phi), n = 200)
cat("razon sin MA =", round(var(cumsum(w0)) / var(w0), 1), "\n")

# c4-m2-22: nombres de funciones del panel "Con que" en R
suppressMessages(library(tseries))
cat("\nexisten: ndiffs", is.function(forecast::ndiffs), "| checkresiduals", is.function(forecast::checkresiduals),
    "| adf.test", is.function(tseries::adf.test), "| kpss.test", is.function(tseries::kpss.test),
    "| acf", is.function(stats::acf), "| pacf", is.function(stats::pacf), "| Box.test", is.function(stats::Box.test),
    "| shapiro.test", is.function(stats::shapiro.test), "\n")
