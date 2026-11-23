# lector C · comprobaciones en R 4.6.0 + forecast 9.0.2 para las filas de M5, M6 y M7 del capítulo 4
# Uso: Rscript c_comprueba.R > c_comprueba.out
suppressMessages(library(forecast))
cat("R", R.version.string, "· forecast", as.character(packageVersion("forecast")), "\n")
f4 <- function(x) formatC(x, digits = 4, format = "f")

cat("\n== [m7-09] umbral de raíces en el código\n")
am <- deparse(forecast:::myarima)
cat("líneas con 'minroot <' :", paste(trimws(grep("minroot <", am, value = TRUE)), collapse = " || "), "\n")
cat("aparece 1.001 en myarima:", any(grepl("1\\.001", am)), "\n")
cat("líneas que asignan Inf al ic:", sum(grepl("fit\\$ic <- Inf", am)), "\n")
print(trimws(am[(grep("minroot < 1 \\+ 0.01", am)-3):(grep("minroot < 1 \\+ 0.01", am)+6)]))

cat("\n== [m7-09, m7-10] ARIMA(2,1,2) del Nilo: raíces AR y logL según estimador (con y sin deriva)\n")
raiz_ar <- function(a) min(Mod(polyroot(c(1, -coef(a)[grep("^ar", names(coef(a)))]))))
raiz_ma <- function(a) min(Mod(polyroot(c(1,  coef(a)[grep("^ma", names(coef(a)))]))))
for (dr in c(FALSE, TRUE)) for (m in c("CSS-ML", "ML")) {
  a <- suppressWarnings(Arima(Nile, order = c(2, 1, 2), include.drift = dr, method = m))
  cat(sprintf("drift=%-5s %-6s logL = %.3f  min|raíz AR| = %.6f  min|raíz MA| = %.6f  aicc = %s\n", dr, m, a$loglik, raiz_ar(a), raiz_ma(a), a$aicc))
}
cat("¿1.0009 (4 dec.) o 1.00094…<1.001?  Con CSS-ML sin deriva: ", raiz_ar(Arima(Nile, order = c(2,1,2), method = "CSS-ML")) < 1.001, "\n")

cat("\n== [m7-12] traza de auto.arima(Nile): conteo y podio\n")
tr <- capture.output(aj <- auto.arima(Nile, trace = TRUE, seasonal = FALSE))
lin <- grep("^ ARIMA.*:", tr, value = TRUE)
cat("modelos evaluados (escalonada):", length(lin), " · ganador:", as.character(aj), " · aicc =", round(aj$aicc, 3), "\n")
print(lin)
tr2 <- capture.output(cm <- auto.arima(Nile, trace = TRUE, seasonal = FALSE, stepwise = FALSE, approximation = FALSE))
lin2 <- grep("^ ARIMA.*:", tr2, value = TRUE)
cat("\nmodelos evaluados (exhaustiva):", length(lin2), " · ganador:", as.character(cm), " · aicc =", round(cm$aicc, 3), "\n")
val <- as.numeric(sub(".*: *", "", lin2)); nom <- trimws(sub(" *:.*", "", lin2))
o <- order(val); fin <- is.finite(val)
cat("podio (exhaustiva):\n"); print(data.frame(modelo = nom[o][1:10], aicc = round(val[o][1:10], 3), dif = round(val[o][1:10] - min(val), 2)))
cat("modelos de la exhaustiva a menos de 2 puntos:", sum(val - min(val) < 2, na.rm = TRUE), " · con AICc = Inf:", sum(!fin), "\n")
cat("d de todos los modelos de la exhaustiva:", paste(unique(sub("ARIMA\\(\\d,(\\d),\\d\\).*", "\\1", nom)), collapse = ","), "\n")
pq <- as.numeric(sub("ARIMA\\((\\d),\\d,(\\d)\\).*", "\\1", nom)) + as.numeric(sub("ARIMA\\(\\d,\\d,(\\d)\\).*", "\\1", nom))
cat("max p+q en la exhaustiva:", max(pq), " · nº de órdenes (p,q) distintos:", length(unique(sub(" with.*| *$", "", nom))), "\n")

cat("\n== [m7-11] approximation por defecto con el Nilo\n")
cat("length(Nile) > 150 || frequency(Nile) > 12:", (length(Nile) > 150 || frequency(Nile) > 12), " · ndiffs(Nile) =", ndiffs(Nile), "\n")

cat("\n== [m7-04, m5-13] auto.arima: modelos iniciales y constante, con d = 1\n")
cat("primeras líneas de la traza:\n"); print(head(lin, 6))
cat("Nile d=2 forzado, ¿aparece 'with drift' o 'with non-zero mean'?:", any(grepl("drift|non-zero", capture.output(invisible(auto.arima(Nile, d = 2, trace = TRUE, seasonal = FALSE))))), "\n")
x0 <- diff(Nile)  # serie sin tendencia clara con d = 0 forzado: ¿se prueba la media?
t0 <- capture.output(invisible(auto.arima(Nile, d = 0, trace = TRUE, seasonal = FALSE)))
cat("Nile d=0: ¿aparece 'with non-zero mean'?:", any(grepl("non-zero mean", t0)), " · ¿'drift'?:", any(grepl("drift", t0)), "\n"); print(head(t0, 5))
t1 <- capture.output(invisible(auto.arima(Nile, d = 1, trace = TRUE, seasonal = FALSE)))
cat("Nile d=1: ¿'with drift'?:", any(grepl("with drift", t1)), " · ¿hay el mismo orden con y sin deriva?:", any(grepl("ARIMA\\(0,1,0\\) *:", t1)) && any(grepl("ARIMA\\(0,1,0\\) with drift", t1)), "\n")

cat("\n== [m6-02..04] n* = n - d en forecast::Arima\n")
ar <- deparse(Arima)
print(trimws(grep("nstar|npar", ar, value = TRUE)))
fa <- Arima(Nile, order = c(1, 1, 1), method = "ML")
n <- length(Nile); k <- length(coef(fa)) + 1
manual <- fa$aic + 2 * k * (k + 1) / ((n - 1) - k - 1)
manual_n <- fa$aic + 2 * k * (k + 1) / (n - k - 1)
cat(sprintf("Arima(1,1,1) ML: aicc = %.4f · a mano con n* = n-d = 99: %.4f · con n = 100: %.4f · aic = %.4f · bic = %.4f · bic a mano (log 99): %.4f\n", fa$aicc, manual, manual_n, fa$aic, fa$bic, fa$aic - 2*k + log(99)*k))
cat("stats::arima: nobs =", arima(Nile, c(1,1,1), method = "ML")$nobs, " (n - d = 99) · n.cond =", arima(Nile, c(1,1,1), method = "ML")$n.cond, "\n")
cat("stats::arima d=2: nobs =", arima(Nile, c(1,2,1), method = "ML")$nobs, "\n")

cat("\n== [m6-01, m6-05] la verosimilitud es la de los datos diferenciados: logL de arima(Nile,(0,1,1)) = logL de arima(diff(Nile),(0,0,1), include.mean=FALSE)?\n")
a1 <- arima(Nile, c(0,1,1), method = "ML"); a2 <- arima(diff(Nile), c(0,0,1), include.mean = FALSE, method = "ML")
cat(sprintf("logL ARIMA(0,1,1) sobre Nile = %.4f · logL MA(1) sobre diff(Nile) = %.4f · theta: %.4f / %.4f\n", a1$loglik, a2$loglik, coef(a1), coef(a2)))
cat("Nota: aic de ?arima solo válido con method='ML'; el bloque del capítulo usa ML.\n")

cat("\n== [m5-10] arima ignora include.mean con d >= 1, sin aviso\n")
w <- NULL; ff <- withCallingHandlers(arima(Nile, order = c(1,1,1), include.mean = TRUE, method = "ML"), warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
cat("coef:", names(coef(ff)), " · avisos:", length(w), "\n")
f0 <- arima(Nile, order = c(1,0,1), method = "ML"); cat("d=0:", names(coef(f0)), " intercept =", f4(coef(f0)[["intercept"]]), " · media muestral =", f4(mean(Nile)), "\n")

cat("\n== [m5-11, m5-12, m5-16] Arima con deriva = regresión con xreg = seq_along\n")
fb <- Arima(Nile, order = c(1,1,1), include.drift = TRUE)
fc <- arima(Nile, order = c(1,1,1), xreg = seq_along(Nile), method = "CSS-ML")
cat("Arima include.drift: ", paste(names(coef(fb)), f4(coef(fb)), collapse = " | "), "\n")
cat("arima xreg=seq_along:", paste(names(coef(fc)), f4(coef(fc)), collapse = " | "), "\n")
cat("coincide (tol 1e-3):", isTRUE(all.equal(unname(coef(fb)), unname(coef(fc)), tolerance = 1e-3)), "\n")
cat("cuerpo de Arima: cbind(drift = seq_along(x), xreg):", any(grepl("cbind\\(drift = seq_along\\(x\\)", ar)), "\n")
ee <- sqrt(diag(fb$var.coef)); cat(sprintf("drift = %.4f e.e. = %.4f t = %.3f · phi1 = %.4f · c = delta(1-phi1) = %.4f · aicc con deriva = %.3f · sin deriva = %.3f\n",
  coef(fb)[["drift"]], ee[["drift"]], coef(fb)[["drift"]]/ee[["drift"]], coef(fb)[["ar1"]], coef(fb)[["drift"]]*(1-coef(fb)[["ar1"]]), fb$aicc, Arima(Nile, order = c(1,1,1))$aicc))
fs <- Arima(Nile, order = c(1,1,1)); cat(sprintf("phi1 sin deriva = %.4f\n", coef(fs)[["ar1"]]))
w2 <- NULL; f2 <- withCallingHandlers(Arima(Nile, order = c(1,2,1), include.drift = TRUE), warning = function(x) { w2 <<- c(w2, conditionMessage(x)); invokeRestart("muffleWarning") })
cat("d=2 con drift: coef =", names(coef(f2)), " · aviso:", w2, "\n")
cat("include.drift por defecto:", eval(formals(Arima)$include.drift), "\n")

cat("\n== [m5-19] media de las diferencias y aporte de 1899\n")
cat(sprintf("Nile[1]=%g Nile[100]=%g · (740-1120)/99 = %.4f · mean(diff(Nile)) = %.4f\n", Nile[1], Nile[100], (740-1120)/99, mean(diff(Nile))))
d <- diff(Nile); i99 <- which(time(d) == 1899); cat(sprintf("diff 1899 = %g · /99 = %.4f\n", d[i99], d[i99]/99))
cat("Nile 1898, 1899:", Nile[time(Nile) == 1898], Nile[time(Nile) == 1899], "\n")

cat("\n== [m6, rejilla] los mejores de cada d, raíces y modelos a menos de 2 puntos (replica del bloque del capítulo)\n")
aicc <- function(f, n_ef) { k <- length(f$coef) + 1; f$aic + 2*k*(k+1)/(n_ef-k-1) }
bic2 <- function(f, n_ef) { k <- length(f$coef) + 1; f$aic - 2*k + log(n_ef)*k }
n <- length(Nile); filas <- list()
for (d in 0:2) for (p in 0:2) for (q in 0:2) {
  f <- tryCatch(suppressWarnings(arima(Nile, order = c(p, d, q), method = "ML")), error = function(e) NULL)
  if (is.null(f)) next
  rar <- if (p > 0) min(Mod(polyroot(c(1, -f$coef[grep("^ar", names(f$coef))])))) else NA
  rma <- if (q > 0) min(Mod(polyroot(c(1,  f$coef[grep("^ma", names(f$coef))])))) else NA
  filas[[length(filas)+1]] <- data.frame(d = d, p = p, q = q, aicc = aicc(f, n - d), bic = bic2(f, n - d), rar = rar, rma = rma)
}
G <- do.call(rbind, filas); cat("modelos ajustados:", nrow(G), "\n")
for (d in 0:2) { g <- G[G$d == d, ]; b <- g[which.min(g$aicc), ]; bb <- g[which.min(g$bic), ]
  cat(sprintf("d=%d  n*=%d  mejor AICc: (%d,%d,%d) %.2f [raíz AR %s, raíz MA %s] · mejor BIC: (%d,%d,%d) %.2f [raíz MA %s] · a menos de 2 del mejor (sin él): %d\n",
    d, n - d, b$p, d, b$q, b$aicc, round(b$rar, 3), round(b$rma, 3), bb$p, d, bb$q, bb$bic, round(bb$rma, 3), sum(g$aicc - b$aicc < 2) - 1)) }
g2 <- G[G$d == 2, ]; cat("d=2: raíces MA de los 9 (3 decimales):", paste(round(g2$rma, 3), collapse = " "), " · con raíz MA < 1.0005:", sum(g2$rma < 1.0005, na.rm = TRUE), "\n")
cat("AICc mínimo global:", min(G$aicc), " en d =", G$d[which.min(G$aicc)], " (", G$p[which.min(G$aicc)], G$q[which.min(G$aicc)], ")\n")
cat("raíz MA del ARIMA(1,2,2):", round(G$rma[G$d == 2 & G$p == 1 & G$q == 2], 4), "\n")
cat("log(99) =", round(log(99), 3), " · log(99)/2 =", round(log(99)/2, 3), "\n")
