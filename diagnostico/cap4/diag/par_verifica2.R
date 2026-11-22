# Par académico cap. 4 · recálculo independiente (M4-M10, ejercicios, quiz y simulacro)
suppressMessages({library(forecast); library(tseries); library(urca)})
y <- Nile; n <- length(y)
sec <- function(s) cat("\n==== ", s, " ====\n")
aicc_k <- function(f, nef) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(nef-k-1) }
bic_k  <- function(f, nef) { k <- length(f$coef) + 1; f$aic - 2*k + log(nef)*k }
raices <- function(f) {
  ar <- f$coef[grepl("^ar", names(f$coef))]; ma <- f$coef[grepl("^ma", names(f$coef))]
  c(ar = if (length(ar)) min(Mod(polyroot(c(1, -ar)))) else NA,
    ma = if (length(ma)) min(Mod(polyroot(c(1, ma)))) else NA)
}

sec("M4 · ARIMA(0,1,1)")
ma1 <- arima(y, order = c(0,1,1), method = "ML")
cat("theta", round(coef(ma1),4), " ee", round(sqrt(ma1$var.coef[1,1]),4), " t", round(coef(ma1)/sqrt(ma1$var.coef[1,1]),2),
    " sigma2", round(ma1$sigma2,2), "\n")
a <- acf(diff(y), lag.max = 20, plot = FALSE)$acf[-1]
cat("ACF d1 rezago 8:", round(a[8],4), " fuera de ±0.197:", which(abs(a) > 1.96/sqrt(99)), "\n")
a0 <- acf(y, lag.max = 20, plot = FALSE)$acf[-1]
cat("ACF d0 dentro de la banda ±", round(1.96/sqrt(100),3), ":", which(abs(a0) <= 1.96/sqrt(100)), " mínimo:", round(min(a0),4), "\n")
cat("AR(1) phi=0.5: rho_k =", round(0.5^(1:4),4), "\n")

sec("M6 · rejilla 27 modelos")
rej <- do.call(rbind, lapply(0:2, function(d) do.call(rbind, lapply(0:2, function(p) do.call(rbind, lapply(0:2, function(q) {
  f <- tryCatch(arima(y, order = c(p,d,q), method = "ML", include.mean = (d == 0)), error = function(e) NULL)
  if (is.null(f)) return(data.frame(d=d,p=p,q=q,aicc=NA,bic=NA,lb=NA,raiz_ar=NA,raiz_ma=NA,code=NA))
  lb <- Box.test(residuals(f), lag = 20, type = "Ljung-Box", fitdf = p + q)$p.value
  r <- raices(f)
  data.frame(d=d,p=p,q=q,aicc=round(aicc_k(f, n-d),2), bic=round(bic_k(f, n-d),2), lb=round(lb,4),
             raiz_ar=round(r[["ar"]],4), raiz_ma=round(r[["ma"]],4), code=f$code)
}))))))
print(rej)
cat("LB(20) rechaza (p<0.05) en", sum(rej$lb < 0.05, na.rm=TRUE), "modelos:\n"); print(rej[which(rej$lb < 0.05), 1:3])
for (dd in 0:2) { g <- rej[rej$d == dd, ]; b <- min(g$aicc, na.rm=TRUE)
  cat("d =", dd, " mejor AICc", b, " modelos a < 2 del mejor (sin contar el mejor):", sum(g$aicc - b < 2 & g$aicc > b, na.rm=TRUE),
      " LB de esos:", paste(g$lb[g$aicc - b < 2], collapse=" "), "\n") }
cat("d=2 con |raiz MA| <= 1.001:", nrow(subset(rej, d==2 & raiz_ma <= 1.001)), "\n")
cat("AICc (0,1,1)-(1,1,1):", with(rej, aicc[d==1&p==0&q==1] - aicc[d==1&p==1&q==1]),
    " BIC (1,1,1)-(0,1,1):", with(rej, bic[d==1&p==1&q==1] - bic[d==1&p==0&q==1]), "\n")

sec("M7 · ARIMA(2,1,2) y búsqueda exhaustiva")
f212 <- arima(y, order = c(2,1,2), method = "ML"); print(round(coef(f212),4)); print(round(raices(f212),4))
f212b <- Arima(y, order = c(2,1,2)); cat("Arima CSS-ML (2,1,2) raíces:", round(raices(f212b),4), "\n")
f212d <- Arima(y, order = c(2,1,2), include.drift = TRUE); cat("Arima (2,1,2)+deriva raíces:", round(raices(f212d),4), "\n")
tr <- capture.output(ex <- auto.arima(y, trace = TRUE, stepwise = FALSE, approximation = FALSE, seasonal = FALSE))
tr <- grep("^ ARIMA", tr, value = TRUE)
val <- suppressWarnings(as.numeric(sub(".*: *", "", tr)))
o <- order(val); tab <- data.frame(modelo = trimws(sub(":.*", "", tr[o])), aicc = val[o]); tab$dif <- round(tab$aicc - tab$aicc[1], 3)
print(head(tab, 10)); cat("modelos con dif < 2 (incluido el primero):", sum(tab$dif < 2, na.rm = TRUE), " total evaluados:", length(tr), "\n")
cat("approximation por defecto con n=100:", (length(y) > 150 | frequency(y) > 12), "\n")

sec("M8 · modelo final, sobrediferenciación, escalón")
f111 <- arima(y, order = c(1,1,1), method = "ML")
print(round(cbind(coef = coef(f111), ee = sqrt(diag(f111$var.coef))), 4))
cat("sigma2 ML", round(f111$sigma2,2), " raices", round(raices(f111),4), "\n")
cat("LB(20) p", round(Box.test(residuals(f111), 20, "Ljung-Box", fitdf=2)$p.value,4),
    " Shapiro p", round(shapiro.test(residuals(f111))$p.value,4), " sd residuales", round(sd(residuals(f111)),2), "\n")
for (d in 0:3) { x <- if (d==0) y else diff(y, differences=d)
  m <- arima(x, order=c(0,0,1), include.mean=(d==0), method="ML")
  cat(sprintf("d=%d var=%.2f rho1=%.4f theta=%.4f sigma2=%.2f\n", d, var(x), acf(x,1,plot=FALSE)$acf[2], coef(m)[["ma1"]], m$sigma2)) }
esc <- as.numeric(time(y) >= 1899)
fe <- arima(y, order = c(0,0,0), xreg = esc, method = "ML")
cat("medias:", round(mean(y[time(y) < 1899]),2), round(mean(y[time(y) >= 1899]),2),
    " beta", round(coef(fe)[["esc"]],2), " ee", round(sqrt(fe$var.coef[2,2]),2), " t", round(coef(fe)[["esc"]]/sqrt(fe$var.coef[2,2]),2),
    " AICc", round(aicc_k(fe, 100),2), " LB20", round(Box.test(residuals(fe), 20, "Ljung-Box")$p.value,4), "\n")
ent <- window(y, end = 1950); pru <- window(y, start = 1951); ee <- as.numeric(time(ent) >= 1899)
fcs <- list(naive = rep(tail(ent,1),20), arima = forecast(Arima(ent, order=c(1,1,1)), h=20)$mean,
  escalon = forecast(Arima(ent, order=c(0,0,0), xreg=ee), xreg=rep(1,20))$mean,
  escalon_ar1 = forecast(Arima(ent, order=c(1,0,0), xreg=ee), xreg=rep(1,20))$mean, media = rep(mean(ent),20))
print(round(sapply(fcs, function(p) c(rmse = sqrt(mean((pru - as.numeric(p))^2)), mae = mean(abs(pru - as.numeric(p))))), 2))

sec("M8/ejercicio 2 · log(lynx)")
ly <- log(lynx)
cat("var d0,d1:", round(var(ly),3), round(var(diff(ly)),3), " reducción %", round(100*(1-var(diff(ly))/var(ly)),1), "\n")
cat("adf.test p", round(adf.test(ly)$p.value,4), " kpss.test p", round(kpss.test(ly)$p.value,4),
    " PP.test p", round(PP.test(ly)$p.value,4), " pp.test p", round(suppressWarnings(pp.test(ly))$p.value,4), "\n")
cat("ndiffs kpss/adf/pp:", sapply(c("kpss","adf","pp"), function(t) ndiffs(ly, test=t)), "\n")
cat("ARIMA(2,1,1) raices:", round(raices(arima(ly, order=c(2,1,1), method="ML")),4), "\n")

sec("M5 · deriva y constante")
f1b <- Arima(y, order = c(1,1,1), include.drift = TRUE); print(round(coef(f1b), 4))
cat("c = delta(1-phi) =", round(coef(f1b)[["drift"]]*(1-coef(f1b)[["ar1"]]),3), "\n")
f0 <- arima(y, order=c(1,0,1), method="ML"); cat("intercept", round(coef(f0)[["intercept"]],4), " ee", round(sqrt(f0$var.coef[3,3]),2), " media muestral", mean(y), "\n")
cat("(y_100 - y_1)/99 =", round((y[100]-y[1])/99,3), " y1 y100:", y[1], y[100], " 247.78/99 =", round(247.78/99,3), "\n")

sec("M9 · formas del pronóstico")
formas <- list(d0 = Arima(y, order=c(1,0,1)), d1 = Arima(y, order=c(1,1,1)),
               d1d = Arima(y, order=c(1,1,1), include.drift=TRUE), d2 = Arima(y, order=c(1,2,1)))
for (nm in names(formas)) { fc <- forecast(formas[[nm]], h = 30, level = 95); m <- as.numeric(fc$mean)
  cat(sprintf("%-4s ancho95 h1=%.1f h30=%.1f  dif1(h30)=%.3f  ultimo=%.2f  coefs: %s\n", nm, fc$upper[1]-fc$lower[1], fc$upper[30]-fc$lower[30],
      m[30]-m[29], m[30], paste(names(coef(formas[[nm]])), round(coef(formas[[nm]]),4), collapse=" "))) }
m2 <- as.numeric(forecast(formas$d2, h = 30)$mean); d2s <- diff(m2, differences = 2)
cat("2a dif del pronóstico d=2, h=3..8:", signif(d2s[1:6],4), " cociente sucesivo:", round(d2s[2:6]/d2s[1:5],4), "\n")
f <- formas$d1; ph <- coef(f)[["ar1"]]; th <- coef(f)[["ma1"]]
psi_cerrada <- ((1+th) - (ph+th)*ph^(0:30))/(1-ph); psi_r <- c(1, ARMAtoMA(ar=c(1+ph,-ph), ma=th, lag.max=30))
cat("forma cerrada vs ARMAtoMA, error máx:", signif(max(abs(psi_cerrada - psi_r)),3), " psi_inf", round((1+th)/(1-ph),4),
    " psi1", round(psi_r[2],4), " sigma", round(sqrt(f$sigma2),3), "\n")
s <- sqrt(f$sigma2); sh <- s*sqrt(cumsum(psi_r^2)); cat("sigma_2", round(sh[2],3), " sigma_30", round(sh[30],3), " sigma*sqrt(30)", round(s*sqrt(30),2),
  " sigma30/sigma1", round(sh[30]/sh[1],4), " cociente sigma30/(sigma*sqrt30)", round(sh[30]/(s*sqrt(30)),4), "\n")
cat("pronóstico d1: h1", round(forecast(f,h=1)$mean[1],2), " límite h=30", round(forecast(f,h=30)$mean[30],2), " h5", round(forecast(f,h=5)$mean[5],2), "\n")
cat("semiancho95 h1, h30:", round(qnorm(0.975)*sh[c(1,30)],2), "\n")
cat("1/(1-phi_d2) =", round(1/(1-coef(formas$d2)[["ar1"]]),4), "\n")

sec("Ejercicio 3 · BJsales")
fb <- Arima(BJsales, order=c(1,1,1)); phb <- coef(fb)[["ar1"]]; thb <- coef(fb)[["ma1"]]
psib <- c(1, ARMAtoMA(ar=c(1+phb,-phb), ma=thb, lag.max=12)); shb <- sqrt(fb$sigma2)*sqrt(cumsum(psib^2))
cat("psi_inf", round((1+thb)/(1-phb),4), " sigma12/(sigma*sqrt12)", round(shb[12]/(sqrt(fb$sigma2)*sqrt(12)),4), "\n")

sec("M10 · TRM (CSV del repo)")
trm <- ts(read.csv("../../../Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm, start=c(2015,1), frequency=12)
rw <- arima(trm, order=c(0,1,0), method="ML"); e <- residuals(rw); d1 <- diff(trm); s <- sqrt(rw$sigma2)
cat("n", length(trm), " sigma2", round(rw$sigma2,2), " primer residual", round(e[1],3), " último dato", tail(trm,1), "\n")
asim <- function(x) mean((x-mean(x))^3)/mean((x-mean(x))^2)^1.5
cat("asimetría d1", round(asim(d1),3), " residuales", round(asim(e),3), " curtosis d1", round(mean((d1-mean(d1))^4)/mean((d1-mean(d1))^2)^2,2), "\n")
cat("cobertura 80% a 1 mes:", round(100*mean(abs(d1) <= qnorm(0.9)*s),1), "%  95%:", round(100*mean(abs(d1) <= qnorm(0.975)*s),1), "%\n")
cat("mayores cambios:", paste(names(sort(setNames(as.numeric(d1), format(as.Date(paste0(time(d1) %/% 1, "-", round((time(d1) %% 1)*12)+1, "-01")), "%Y-%m")), decreasing=TRUE))[1:3], collapse=", "), "\n")
cat("LB sin el primer residual: 20 ->", round(Box.test(e[-1],20,"Ljung-Box")$p.value,4), " 12 ->", round(Box.test(e[-1],12,"Ljung-Box")$p.value,4),
    " shapiro", round(shapiro.test(e[-1])$p.value,4), " LB12 cuadrados", round(Box.test(e[-1]^2,12,"Ljung-Box")$p.value,4), "\n")
r <- acf(d1, lag.max = 12, plot = FALSE)$acf[-1]
for (h in c(3, 6, 12)) {
  solo_r1 <- 1 + 2*(h-1)/h*r[1]
  todas <- 1 + 2*sum((1 - (1:(h-1))/h) * r[1:(h-1)])
  dh <- diff(trm, lag = h); emp <- mean(dh^2) / (h * mean(d1^2))
  emp2 <- var(dh) / (h * var(d1))
  cat(sprintf("h=%2d  razón con solo rho1: %.3f | con la ACF hasta h-1: %.3f | empírica (sin centrar) %.3f | empírica (var) %.3f\n", h, solo_r1, todas, emp, emp2))
}
cat("cobertura 95% a 12 meses dentro de muestra:", round(100*mean(abs(diff(trm, lag=12)) <= qnorm(0.975)*s*sqrt(12)),1), "%\n")
tr2 <- capture.output(a2 <- auto.arima(trm, trace=TRUE, stepwise=FALSE, approximation=FALSE, seasonal=TRUE))
cat("auto.arima exhaustiva estacional: modelos", length(grep("^ ARIMA", tr2)), " ->", as.character(a2), "\n")
tr3 <- capture.output(a3 <- auto.arima(trm, trace=TRUE, stepwise=FALSE, approximation=FALSE, seasonal=FALSE))
cat("auto.arima exhaustiva no estacional: modelos", length(grep("^ ARIMA", tr3)), " ->", as.character(a3), "\n")

sec("M10 · puente AirPassengers")
lap <- log(AirPassengers)
ap <- auto.arima(lap, seasonal=FALSE, stepwise=FALSE, approximation=FALSE)
ra <- residuals(ap); aa <- acf(ra, lag.max=26, plot=FALSE)$acf[-1]
cat(as.character(ap), " rho12", round(aa[12],4), " rho24", round(aa[24],4), " banda", round(1.96/sqrt(length(ra)),4),
    " Q24", round(Box.test(ra, 24, "Ljung-Box", fitdf=sum(arimaorder(ap)[c(1,3)]))$statistic,1),
    " p", signif(Box.test(ra, 24, "Ljung-Box", fitdf=sum(arimaorder(ap)[c(1,3)]))$p.value,3), "\n")
air <- Arima(lap, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12)); rs <- residuals(air)
cat("airline rho12", round(acf(rs, lag.max=12, plot=FALSE)$acf[13],4), " LB24 p (fitdf 2)", round(Box.test(rs,24,"Ljung-Box",fitdf=2)$p.value,4),
    " nobs", ap$nobs, air$nobs, "\n")
ap8 <- auto.arima(lap, seasonal=FALSE, stepwise=FALSE, approximation=FALSE, max.p=8, max.q=8, max.order=16)
cat("p,q<=8:", as.character(ap8), " rho12", round(acf(residuals(ap8), lag.max=12, plot=FALSE)$acf[13],4), "\n")

sec("Quiz y simulacro")
cat("Q2 sigma_2 =", round(142.045*sqrt(1+0.3802^2),3), "\n")
p1 <- 0.57; t1 <- 0.25; r1 <- (1+p1*t1)*(p1+t1)/(1+2*p1*t1+t1^2); cat("S1 rho2 =", round(p1*r1,4), " (", round(ARMAacf(ar=p1, ma=t1, lag.max=2)[3],4), ")\n")
cat("S2 c =", round(67.1246*(1-1.2254+0.3688),4), " raíces correctas:", round(Mod(polyroot(c(1,-1.2254,0.3688))),4), "\n")
g <- c(16.0539, 11.8658, 4.9091); rr <- g[2:3]/g[1]; ph <- solve(matrix(c(1,rr[1],rr[1],1),2), rr); cat("S4 YW:", round(ph,4), "\n")
ll <- c(MA1=-54.460, AR1=-59.190, MA2=-52.821, ARMA11=-53.428); k <- c(3,3,4,4); nn <- 40
ac <- -2*ll + 2*k + 2*k*(k+1)/(nn-k-1); print(round(sort(ac),3))
x2 <- 5.83 + 1.96*sqrt(2.14*(1+1.22^2)); cat("S6 límite superior y =", round(x2^2,2), "\n")
cat("S7 Holt: alpha =", 1-0.45, " beta =", round((-1.25+2-(1-0.45))/(1-0.45),4), " raiz MA fila 2 =", round(1/0.96,4), "\n")
cat("S8 chi2 0.95 gl 13 =", round(qchisq(0.95,13),2), " p con gl 13 =", round(pchisq(23.329,13,lower.tail=FALSE),4), " p gl16 =", round(pchisq(23.329,16,lower.tail=FALSE),4), "\n")
