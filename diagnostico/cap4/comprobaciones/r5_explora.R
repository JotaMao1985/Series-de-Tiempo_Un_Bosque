# R5 cap. 4 · exploracion de series candidatas (no es fuente de cifras del capitulo: esas salen
# de r5_bloques/*.R y de r5_cifras.R).  Rscript r5_explora.R > r5_explora.out 2>&1
suppressPackageStartupMessages({ library(forecast); library(tseries); library(tsibbledata) })
options(width = 150, warn = 1)
data(tcm, package = "tseries"); data(NelPlo, package = "tseries"); data(USeconomic, package = "tseries"); data(bev, package = "tseries")
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
bar <- function(x, k = 10) round(acf(x, lag.max = k, plot = FALSE)$acf[-1], 3)
par_ <- function(x, k = 10) round(pacf(x, lag.max = k, plot = FALSE)$acf, 3)

cat("== pelt (Hare) ==\n"); print(head(pelt, 3)); print(range(pelt$Year)); 
h <- ts(pelt$Hare, start = 1845); lh <- log(h)
for (nm in c("h", "lh")) { y <- get(nm)
  cat(nm, "n", length(y), "ndiffs k/a/p", ndiffs(y, test="kpss"), ndiffs(y, test="adf"), ndiffs(y, test="pp"),
      "var d0..2", signif(sapply(0:2, function(d) var(if (d==0) y else diff(y, differences=d))), 4), "r1", bar(y,1), "r1 dif", bar(diff(y),1), "\n")
  cat(" kpss p", kpss.test(y)$p.value, "adf p", adf.test(y)$p.value, "pp p", pp.test(y)$p.value, "\n")
  for (o in list(c(2,1,0), c(2,1,1), c(0,1,1), c(1,1,1), c(3,1,1), c(2,1,2), c(4,1,1))) { f <- tryCatch(arima(y, order=o, method="ML"), error=function(e) NULL); if (is.null(f)) next
    ma <- coef(f)[grepl("^ma", names(coef(f)))]; cat(sprintf("  ARIMA(%d,1,%d) raizMA=%s aicc=%.2f\n", o[1], o[3], if (length(ma)) sprintf("%.4f", min(Mod(polyroot(c(1, ma))))) else "-", aicc(f, length(y)-1))) }
  a <- auto.arima(y, stepwise=FALSE, approximation=FALSE); cat("  auto:", as.character(a), "\n")
  for (p in 1:4) { f <- arima(y, order=c(p,0,0), method="ML"); cat(sprintf("  AR(%d) aicc=%.2f LB20 p=%.4f minroot=%.4f\n", p, aicc(f, length(y)), Box.test(residuals(f), lag=20, type="Ljung-Box", fitdf=p)$p.value, min(Mod(polyroot(c(1, -coef(f)[1:p])))))) }
}

cat("\n== tcm1y ==\n"); y <- tcm1y; print(tsp(y)); cat("n", length(y), "\n")
f2 <- arima(y, order=c(2,0,0), method="ML"); print(f2); print(Mod(polyroot(c(1, -coef(f2)[1:2])))); f110 <- arima(y, order=c(1,1,0), method="ML"); print(f110)
cat("ndiffs", ndiffs(y, test="kpss"), ndiffs(y, test="adf"), ndiffs(y, test="pp"), "\n")

cat("\n== gnp.real y otras NelPlo: ACF/PACF de la diferencia ==\n")
for (nm in c("gnp.real", "real.wages", "ip", "emp", "unemp", "gnp.capita", "cpi", "money.stock")) { y <- na.omit(NelPlo[, nm]); d <- diff(y)
  cat(nm, "n", length(y), "anios", start(y)[1], end(y)[1], "banda", round(1.96/sqrt(length(d)),3), "ndiffs", ndiffs(y, test="kpss"), ndiffs(y, test="adf"), ndiffs(y, test="pp"), "\n  ACF ", bar(d), "\n  PACF", par_(d), "\n  auto esc:", as.character(auto.arima(y)), "| exh:", as.character(auto.arima(y, stepwise=FALSE, approximation=FALSE)), "\n") }

cat("\n== beaver2 ==\n"); y <- ts(beaver2$temp); act <- beaver2$activ; print(table(act)); print(which(diff(act)!=0)); print(head(beaver2,3)); print(tail(beaver2,3))
cat("ndiffs", ndiffs(y, test="kpss"), ndiffs(y, test="adf"), ndiffs(y, test="pp"), "\n"); print(tapply(beaver2$temp, act, mean))
f0 <- lm(temp ~ activ, beaver2); print(summary(f0)$coef); r <- residuals(f0); cat("resid step: r1..5", bar(r,5), "kpss p", kpss.test(r)$p.value, "adf p", adf.test(r)$p.value, "\n")
fe <- Arima(y, order=c(1,0,0), xreg=act); print(fe); cat("LB10", Box.test(residuals(fe), lag=10, type="Ljung-Box", fitdf=1)$p.value, "shapiro", shapiro.test(residuals(fe))$p.value, "\n")
cat("r1 nivel", bar(y,1), "r1 dif", bar(diff(y),5), "\n"); f010 <- Arima(y, order=c(0,1,0)); cat("ARIMA(0,1,0) LB10", Box.test(residuals(f010), lag=10, type="Ljung-Box")$p.value, "sigma2", f010$sigma2, " fe sigma2", fe$sigma2, "\n")
cat("antes/despues por separado: ndiffs", ndiffs(window(y, end=38)), ndiffs(window(y, start=39)), " kpss p", kpss.test(window(y, end=38))$p.value, kpss.test(window(y, start=39))$p.value, "adf", adf.test(window(y, end=38))$p.value, adf.test(window(y, start=39))$p.value, "\n")

cat("\n== airmiles / aus_airpassengers ==\n"); y <- log(airmiles); print(tsp(airmiles)); print(airmiles)
cat("ndiffs", ndiffs(y, test="kpss"), ndiffs(y, test="adf"), ndiffs(y, test="pp"), "\n")
for (o in list(c(0,1,0), c(0,1,1), c(1,1,0))) { f1 <- Arima(y, order=o, include.drift=TRUE); f0 <- Arima(y, order=o)
  cat(sprintf("ARIMA(%d,1,%d) deriva=%.4f ee=%.4f t=%.2f aicc con=%.2f sin=%.2f LB con=%.3f\n", o[1], o[3], coef(f1)[["drift"]], sqrt(diag(f1$var.coef))[["drift"]], coef(f1)[["drift"]]/sqrt(diag(f1$var.coef))[["drift"]], f1$aicc, f0$aicc, Box.test(residuals(f1), lag=8, type="Ljung-Box", fitdf=sum(o[c(1,3)]))$p.value)) }
aus_airpassengers <- fpp3::aus_airpassengers; ap <- ts(aus_airpassengers$Passengers, start = 1970); print(tsp(ap)); print(round(ap,2))
cat("ndiffs", ndiffs(ap, test="kpss"), ndiffs(ap, test="adf"), ndiffs(ap, test="pp"), "\n")
for (d in 1:2) for (q in 0:2) for (p in 0:2) { f <- tryCatch(arima(ap, order=c(p,d,q), method="ML"), error=function(e) NULL); if (is.null(f)) next
  ma <- coef(f)[grepl("^ma", names(coef(f)))]
  cat(sprintf("ARIMA(%d,%d,%d) AICc=%.3f BIC=%.3f LB10=%.3f raizMA=%s\n", p,d,q, aicc(f, length(ap)-d), BIC(f), Box.test(residuals(f), lag=10, type="Ljung-Box", fitdf=p+q)$p.value, if (length(ma)) sprintf("%.4f", min(Mod(polyroot(c(1, ma))))) else "-")) }
for (o in list(c(0,1,0), c(0,1,1), c(1,1,0))) { f1 <- Arima(ap, order=o, include.drift=TRUE); cat(sprintf("con deriva ARIMA(%d,1,%d) aicc=%.3f t=%.2f\n", o[1], o[3], f1$aicc, coef(f1)[["drift"]]/sqrt(diag(f1$var.coef))[["drift"]])) }
cat("auto:", as.character(auto.arima(ap)), "| adf:", as.character(auto.arima(ap, test="adf")), "\n")

cat("\n== austres ==\n"); print(tsp(austres)); cat("ndiffs", ndiffs(austres, test="kpss"), ndiffs(austres, test="adf"), ndiffs(austres, test="pp"), "\n")
a1 <- capture.output(f1 <- auto.arima(austres, trace=TRUE)); cat(a1, sep="\n"); a2 <- capture.output(f2 <- auto.arima(austres, trace=TRUE, stepwise=FALSE, approximation=FALSE)); cat(a2, sep="\n")
a3 <- capture.output(f3 <- auto.arima(austres, trace=TRUE, seasonal=FALSE)); cat(a3, sep="\n"); a4 <- capture.output(f4 <- auto.arima(austres, trace=TRUE, seasonal=FALSE, stepwise=FALSE, approximation=FALSE)); cat(a4, sep="\n")

cat("\n== BJsales.lead ==\n"); y <- BJsales.lead; cat("ACF dif", bar(diff(y)), "\nPACF dif", par_(diff(y)), "\n"); f <- Arima(y, order=c(0,1,1)); print(f); fd <- Arima(y, order=c(0,1,1), include.drift=TRUE); print(fd)
cat("LB20", Box.test(residuals(f), lag=20, type="Ljung-Box", fitdf=1)$p.value, "shapiro", shapiro.test(residuals(f))$p.value, "\n")
