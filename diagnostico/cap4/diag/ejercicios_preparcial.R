# Diagnóstico cap. 4 · claves del preparcial del Corte II (preparcial-corte-2.html)
#   python3 diagnostico/cap4/diag/ejercicios_extrae_preparcial.py
#   Rscript diagnostico/cap4/diag/ejercicios_preparcial.R > diagnostico/cap4/diag/ejercicios_preparcial.out 2>&1
# Recalcula cada clave desde lo que el enunciado da (ítems de cuenta) o desde la
# serie publicada en la propia página (ítems de datos). Los ítems llevan el
# nombre del bloque y su número (A1 ... D6, S1 ... S6) y, entre corchetes, la
# entrada de PREPARCIAL_DATOS.items de la que salen sus cifras.
suppressPackageStartupMessages({ library(forecast); library(tseries); library(jsonlite) })
options(width = 110)
dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
D <- fromJSON(file.path(dir, "ejercicios_preparcial_datos.json"))
S <- function(nombre) { s <- D$series[[nombre]]; ts(s$valores, frequency = s$frecuencia) }
aicc <- function(f, n) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n-k-1) }
r4 <- function(x) round(x, 4)
it <- function(s) cat("\n---", s, "---\n")

it("A1 [i05] MA(1) theta_R = -0.45: rho1");  print(r4(-0.45/(1 + 0.45^2)))
it("A2 [i09] factores de 1 - 0.8B + 0.15B^2"); print(r4(1/Mod(polyroot(c(1, -0.8, 0.15)))))
it("A6 [i32] semianchos a h = 60"); print(round(c(caminata = 1.96*50*sqrt(60), ar1_60 = 1.96*50*sqrt(sum(0.8^(2*(0:59)))),
  techo = 1.96*50/sqrt(1 - 0.64), ar1_12 = 1.96*50*sqrt(sum(0.8^(2*(0:11))))), 1))

it("B1 [i01] (1-0.8B)(1+0.5B)"); print(r4(convolve(c(1, -0.8), rev(c(1, 0.5)), type = "o")))
it("B2 [i03] rho1 MA(2) theta = (-0.5, 0.3)"); print(r4(ARMAacf(ma = c(-0.5, 0.3), lag.max = 2)))
it("B3 [i06] techo 1.96 sqrt(gamma0), ARMA(1,1) 0.6 / -0.3, s2 = 4")
g0 <- 4 * (1 + 2*0.6*(-0.3) + 0.09) / (1 - 0.36); print(round(c(gamma0 = g0, techo = 1.96*sqrt(g0)), 4))
it("B4 [i10] psi = 0.2, 0.18, 0.162 -> theta"); print(r4(c(phi = 0.18/0.2, theta = 0.2 - 0.18/0.2)))
it("B5 [i11] vibracion: gamma0, r1, sigma2 YW")
v <- S("vibracion"); a <- acf(v, plot = FALSE, lag.max = 1)
g0 <- a$acf[1] * 0; g0 <- acf(v, type = "covariance", plot = FALSE, lag.max = 0)$acf[1]
print(round(c(gamma0 = g0, r1 = a$acf[2], sigma2 = g0*(1 - a$acf[2]^2), del_enunciado = 15.04*(1 - 0.632^2),
              ar_yw = ar(v, order.max = 1, aic = FALSE, method = "yule-walker")$var.pred), 4))
it("B6 [i12] Q(4) de Ljung-Box a mano"); r <- c(-0.020, -0.191, 0.176, 0.061)
Q <- 100*102*sum(r^2/(100 - 1:4)); print(round(c(Q = Q, BoxPierce = 100*sum(r^2), p_gl2 = 1 - pchisq(Q, 2)), 4))
it("B7 [i17] SES equivalente: alfa y + (1-alfa) yhat; y forecast() sobre ventas_semanales")
print(round(c(a_mano = 0.4101*276.63 + 0.5899*285.10, cruzado = 0.5899*276.63 + 0.4101*285.10), 2))
vs <- S("ventas_semanales"); fv <- Arima(vs, order = c(0, 1, 1))
print(round(c(theta = coef(fv)[[1]], yT = tail(as.numeric(vs), 1), fitted_T = tail(as.numeric(fitted(fv)), 1),
              pron = as.numeric(forecast(fv, h = 1)$mean)), 4))
it("B8 [i19] suscriptores: deriva"); su <- S("suscriptores")
fs <- Arima(su, order = c(0, 1, 0), include.drift = TRUE)
print(round(c(y1 = su[1], yn = tail(su, 1), media_dif = mean(diff(su)), drift = coef(fs)[["drift"]], div60 = (tail(su,1) - su[1])/60), 4))
it("B9 [i25] turistas: AICc del ARIMA(1,1,1) con deriva"); tu <- S("turistas")
ft <- Arima(tu, order = c(1, 1, 1), include.drift = TRUE)
print(round(c(logL = ft$loglik, aicc_R = ft$aicc, a_mano = -2*(-622.58) + 8 + 40/114, k3 = -2*(-622.58) + 6 + 24/115), 2))
it("B10 [i27] nivel_embalse: pronóstico a 2 pasos del ARIMA(1,1,0)"); ne <- S("nivel_embalse")
fe <- Arima(ne, order = c(1, 1, 0))
p1 <- 98.20 + 0.4863*1.56; p2 <- p1 + 0.4863*(p1 - 98.20)
print(round(c(phi = coef(fe)[[1]], yT_1 = ne[length(ne) - 1], yT = tail(ne, 1), a_mano = p2,
              forecast = as.numeric(forecast(fe, h = 2)$mean[2])), 4))
it("B11 [i28] visitas: semiancho a 3 pasos del ARIMA(0,1,1)"); vi <- S("visitas")
fvi <- Arima(vi, order = c(0, 1, 1)); fc <- forecast(fvi, h = 3, level = 95)
print(round(c(theta = coef(fvi)[[1]], sigma = sqrt(fvi$sigma2), a_mano = 1.96*2.584*sqrt(1 + 2*(1 - 0.4866)^2),
              forecast = (fc$upper[3] - fc$lower[3])/2), 4))
it("B12 [i31] indice_bursatil: semiancho 80 % a 4 pasos"); ib <- S("indice_bursatil")
fi <- Arima(ib, order = c(0, 1, 0)); fc <- forecast(fi, h = 4, level = 80)
print(round(c(sigma = sqrt(fi$sigma2), a_mano = 1.282*32.41*2, forecast = (fc$upper[4] - fc$lower[4])/2), 2)); print(arimaorder(auto.arima(ib)))

it("C1 [i04] MA(1) theta y 1/theta: rho1 y gamma0")
print(round(c(rho1_R = 0.6045/(1 + 0.6045^2), rho1_otro = 1.6542/(1 + 1.6542^2),
              g0_R = 0.9166*(1 + 0.6045^2), g0_otro = 0.3350*(1 + 1.6542^2), inv = 1/0.6045), 4))
it("C2 [i13] nivel_tanque: YW, CSS, ML"); nt <- S("nivel_tanque")
print(r4(c(yw = ar(nt, order.max = 1, aic = FALSE, method = "yule-walker")$ar)))
print(r4(coef(arima(nt, order = c(1, 0, 0), method = "CSS"))))
print(r4(coef(arima(nt, order = c(1, 0, 0), method = "ML"))))
print(tryCatch(coef(arima(nt, order = c(1, 0, 0))), error = function(e) conditionMessage(e)))
it("C3 [i14] rendimientos: RB frente a MA(1)"); re <- S("rendimientos")
f0 <- Arima(re, order = c(0, 0, 0)); f1 <- Arima(re, order = c(0, 0, 1))
ar <- acf(re, lag.max = 20, plot = FALSE)$acf[-1]
print(round(c(aicc_rb = f0$aicc, aicc_ma1 = f1$aicc, bic_rb = f0$bic, bic_ma1 = f1$bic,
              t_ma1 = coef(f1)[[1]]/sqrt(f1$var.coef[1,1]), r14 = ar[14], fuera = sum(abs(ar) > 1.96/sqrt(120)),
              lb12 = Box.test(re, lag = 12, type = "Ljung-Box")$p.value), 4))
it("C4 [i21] cotizacion: AR(2) en niveles y ARIMA(1,1,0)"); co <- S("cotizacion")
f2 <- arima(co, order = c(2, 0, 0), method = "ML"); f110 <- arima(co, order = c(1, 1, 0), method = "ML")
print(r4(c(coef(f2), suma = sum(coef(f2)[1:2]), raices = Mod(polyroot(c(1, -coef(f2)[1:2]))), phi110 = coef(f110)[[1]])))
it("C5 [i18] pedidos: varianzas, ADF, KPSS, r1"); pe <- S("pedidos")
print(round(c(sapply(0:2, function(d) var(if (d == 0) pe else diff(pe, differences = d))),
              r1 = acf(pe, plot = FALSE)$acf[2], adf = suppressWarnings(adf.test(pe)$p.value),
              kpss = suppressWarnings(kpss.test(pe)$p.value), ndiffs = ndiffs(pe)), 4))
it("C6 [i20] matriculas: ARIMA(1,1,0) con deriva"); ma <- S("matriculas")
fm <- Arima(ma, order = c(1, 1, 0), include.drift = TRUE); pm <- as.numeric(forecast(fm, h = 40)$mean)
print(round(c(coef(fm), c = coef(fm)[[2]]*(1 - coef(fm)[[1]]), pend_h40 = pm[40] - pm[39]), 4))
it("C7 [i24] exportaciones: rejilla d = 1"); ex <- S("exportaciones")
rej <- do.call(rbind, lapply(0:2, function(p) do.call(rbind, lapply(0:2, function(q) {
  f <- arima(ex, order = c(p, 1, q), method = "ML")
  ar <- coef(f)[grepl("^ar", names(coef(f)))]; mq <- coef(f)[grepl("^ma", names(coef(f)))]
  data.frame(p, q, aicc = round(aicc(f, 139), 2),
             rAR = if (length(ar)) round(min(Mod(polyroot(c(1, -ar)))), 4) else NA,
             rMA = if (length(mq)) round(min(Mod(polyroot(c(1, mq)))), 4) else NA)
})))); print(rej[order(rej$aicc), ])
print(as.character(auto.arima(ex)))
it("C8 [i30] llamadas: AR(1), LB10, Shapiro, curtosis"); ll <- S("llamadas")
fl <- arima(ll, order = c(1, 0, 0), method = "ML"); e <- residuals(fl); z <- (e - mean(e))/sd(e)
print(round(c(phi = coef(fl)[[1]], lb10 = Box.test(e, lag = 10, type = "Ljung-Box", fitdf = 1)$p.value,
              shapiro = shapiro.test(e)$p.value, curt = mean(z^4), fuera80 = mean(abs(z) > 1.282),
              fuera95 = mean(abs(z) > 1.96), fuera99 = mean(abs(z) > 2.576)), 4))

it("D1 [i02] AR(2) phi = (1, -0.6): ACF, discriminante, periodo")
print(r4(ARMAacf(ar = c(1, -0.6), lag.max = 4)[-1])); rr <- polyroot(c(1, -1, 0.6))
print(r4(c(disc = 1 - 2.4, modulo = Mod(rr[1]), periodo = 2*pi/abs(Arg(rr[1])))))
it("D2 [i07] humedad: ACF, PACF, AICc AR(3) y ARMA(1,1)"); hu <- S("humedad")
print(round(pacf(hu, lag.max = 4, plot = FALSE)$acf[, 1, 1], 3))
print(round(c(ar3 = Arima(hu, order = c(3, 0, 0))$aicc, arma11 = Arima(hu, order = c(1, 0, 1))$aicc,
              ar1 = Arima(hu, order = c(1, 0, 0))$aicc, ar2 = Arima(hu, order = c(2, 0, 0))$aicc), 2))
it("D3 [i08] errores_sensor: barras fuera de la banda"); es <- S("errores_sensor")
ae <- acf(es, lag.max = 20, plot = FALSE)$acf[-1]; print(which(abs(ae) > 1.96/sqrt(100))); print(round(ae[c(1, 2, 19)], 3))
it("D4 [i16] trafico: LB de los residuales del AR(1) por rezago"); tr <- S("trafico")
ftr <- arima(tr, order = c(1, 0, 0), method = "ML")
print(round(sapply(2:20, function(h) Box.test(residuals(ftr), lag = h, type = "Ljung-Box", fitdf = 1)$p.value), 4))
it("D5 [i22] consumo: ACF y PACF de las diferencias"); cs <- S("consumo")
print(round(acf(diff(cs), lag.max = 4, plot = FALSE)$acf[-1], 3)); print(round(pacf(diff(cs), lag.max = 4, plot = FALSE)$acf[, 1, 1], 3))
print(as.character(auto.arima(cs)))
it("D6 [i29] usuarios: ARIMA(0,2,1), semiancho h = 1 y 24"); us <- S("usuarios")
fu <- Arima(us, order = c(0, 2, 1)); fc <- forecast(fu, h = 24, level = 95); sa <- (fc$upper - fc$lower)/2
fdr <- Arima(us, order = c(0, 1, 1), include.drift = TRUE); fc1 <- forecast(fdr, h = 24, level = 95); sa1 <- (fc1$upper - fc1$lower)/2
print(round(c(theta = coef(fu)[[1]], theta_rep = 4*coef(fu)[[1]]/4, sigma = sqrt(fu$sigma2), h1 = sa[1], h24 = sa[24], razon = sa[24]/sa[1], razon_011_deriva = sa1[24]/sa1[1]), 2))

it("S1 gamma0 del AR(2) 0.6 / -0.35, s2 = 2"); print(r4(c(formula = 1.35*2/(0.65*(1.35^2 - 0.36)),
  psi = 2*sum(ARMAtoMA(ar = c(0.6, -0.35), lag.max = 500)^2) + 2)))
it("S2 pi_2 del ARMA(1,1) 0.5 / 0.4 en el pronóstico"); print(r4(c(pi1 = -(0.9), pi2 = -0.9*(-0.4), peso_y_t2 = 0.9*(-0.4))))
it("S5 BIC del ARIMA(0,1,1), n = 101"); print(round(c(bic = 386.46 + 2*log(100), con_n = 386.46 + 2*log(101), k1 = 386.46 + log(100)), 2))
it("S6 semiancho 95 % a 3 pasos, ARIMA(1,1,0) 0.4, sigma 2")
ps <- c(1, ARMAtoMA(ar = c(1.4, -0.4), lag.max = 2)); print(round(c(ps, semi = 1.96*2*sqrt(sum(ps^2))), 4))

it("D6 bis · usuarios con arima(method = 'ML') y con predict()")
fu2 <- arima(us, order = c(0, 2, 1), method = "ML"); pr <- predict(fu2, n.ahead = 24)
print(round(c(theta = coef(fu2)[[1]], sigma = sqrt(fu2$sigma2), h1 = 1.96*pr$se[1], h24 = 1.96*pr$se[24],
              razon = pr$se[24]/pr$se[1], pend = pr$pred[24] - pr$pred[23]), 3))

it("Redondeos intermedios honestos en las numéricas del bloque B y del simulacro")
print(round(c(b3_raiz_2.14 = 1.96*2.14, b10_phi_0.49 = {p1 <- 98.2 + 0.49*1.56; p1 + 0.49*(p1 - 98.2)},
  b10_paso1_98.96 = 98.96 + 0.4863*0.76, b11_psi_0.51 = 1.96*2.584*sqrt(1 + 2*0.51^2),
  s5_log101_4.6 = 386.46 + 2*4.6, s5_log100_4.61 = 386.46 + 2*4.61), 4))
