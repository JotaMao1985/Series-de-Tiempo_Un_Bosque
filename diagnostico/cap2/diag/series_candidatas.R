# Diagnóstico cap. 2 · series de R base medidas como candidatas para los huecos.
# Rscript diagnostico/cap2/diag/series_candidatas.R
suppressPackageStartupMessages({ library(forecast); library(tseries) })
banda <- function(x) 1.96 / sqrt(length(x))
fueraR <- function(r, x) which(abs(r) > banda(x))
pr <- function(nombre, x) {
  a <- suppressWarnings(adf.test(x)); k <- suppressWarnings(kpss.test(x)); kt <- suppressWarnings(kpss.test(x, null = "Trend"))
  ac <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]; pc <- pacf(x, lag.max = 24, plot = FALSE)$acf
  cat(sprintf("%-16s n=%4d f=%2d | ADF p=%.3f KPSS-nivel p=%.3f KPSS-tend p=%.3f | ndiffs=%d nsdiffs=%s | r1=%.3f | PACF fuera: %s\n",
      nombre, length(x), as.integer(frequency(x)), a$p.value, k$p.value, kt$p.value, ndiffs(x),
      if (frequency(x) > 1) nsdiffs(x) else "-", ac[1], paste(head(fueraR(pc, x), 6), collapse = ",")))
}
cat("--- Raíz unitaria / tendencia / PACF ---\n")
pr("LakeHuron", LakeHuron); pr("Nile", Nile); pr("WWWusage", WWWusage); pr("lh", lh)
pr("log(lynx)", log(lynx)); pr("uspop", uspop); pr("nottem", nottem)
pr("log(UKgas)", log(UKgas)); pr("JohnsonJohnson", JohnsonJohnson)
# LakeHuron sin tendencia lineal: ¿estacionaria alrededor de una recta?
res <- residuals(lm(LakeHuron ~ time(LakeHuron)))
pr("LakeHuron-recta", ts(res))
cat("\n--- Box-Cox (Guerrero) ---\n")
for (nm in c("UKgas", "JohnsonJohnson", "nottem", "USAccDeaths", "co2", "AirPassengers", "sunspot.month"))
{ x <- get(nm); cat(sprintf("%-14s min=%8.2f  lambda=%s\n", nm, min(x),
   tryCatch(format(round(BoxCox.lambda(x, method = "guerrero"), 4)), error = function(e) paste("ERROR:", conditionMessage(e))))) }
cat("\n--- Incorrelación no es independencia: rendimientos del DAX ---\n")
r <- diff(log(EuStockMarkets[, "DAX"]))
a1 <- acf(r, lag.max = 24, plot = FALSE)$acf[-1]; a2 <- acf(r^2, lag.max = 24, plot = FALSE)$acf[-1]
cat("n =", length(r), " banda =", round(banda(r), 4), "\n")
cat("rendimientos: fuera de banda", sum(abs(a1) > banda(r)), "de 24; r1 =", round(a1[1], 4), "\n")
cat("cuadrados   : fuera de banda", sum(abs(a2) > banda(r)), "de 24; r1 =", round(a2[1], 4), "\n")
cat("Ljung-Box(24) p: rend =", signif(Box.test(r, 24, "Ljung-Box")$p.value, 3), " cuad =", signif(Box.test(r^2, 24, "Ljung-Box")$p.value, 3), "\n")
