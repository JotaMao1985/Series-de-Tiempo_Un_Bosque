# diag/v3.R — Par académico, capítulo 2: M9 (pipeline), ejercicios 1–4 y cifras del quiz,
# más algunas comprobaciones de apoyo para los hallazgos del M3 y el M7.
# Uso (desde la raíz del repo):  Rscript diagnostico/cap2/diag/v3.R
suppressMessages({ library(jsonlite); library(tseries); library(forecast) })
options(width = 120)
AP <- AirPassengers; lx <- log(AP)
sd_json <- fromJSON("precalculo/salidas/datos_series.json")
trm <- ts(as.numeric(sd_json$trm$valores), start = as.integer(sd_json$trm$inicio), frequency = 12)
difn <- function(x, d) if (d == 0) x else diff(x, differences = d)

cat("== M3 apoyo: ACF de nabla TRM ==\n")
rt <- acf(diff(trm), 24, plot = FALSE)$acf[-1]; b <- 1.96/sqrt(length(diff(trm)))
cat("banda", round(b,4), " r8 =", round(rt[8],4), "  |r_k| > banda en k =", which(abs(rt) > b), "\n")
cat("ndiffs(trm):", ndiffs(trm), "\n")

cat("== M7 apoyo: la serie del recuadro (nabla12 log y) ==\n")
d12 <- diff(lx, lag = 12); dd <- diff(d12)
cat("var d12, var nabla d12:", signif(var(d12),4), signif(var(dd),4), "\n")
cat("ACF d12 1..6:", round(acf(d12, 24, plot=FALSE)$acf[2:7],3), "\n")

cat("== M9 pipeline R ==\n")
preparar <- function(y, m = frequency(y)) {
  lambda <- BoxCox.lambda(y, method = "guerrero")
  w <- if (abs(lambda) < 0.25) log(y) else BoxCox(y, lambda)
  D <- if (m > 1) nsdiffs(w) else 0
  if (D > 0) w <- diff(w, lag = m, differences = D)
  d <- ndiffs(w)
  if (d > 0) w <- diff(w, differences = d)
  list(serie = w, lambda = lambda, d = d, D = D, var_final = var(w),
       kpss_p = suppressWarnings(kpss.test(w)$p.value))
}
res <- preparar(AP)
cat("d D:", res$d, res$D, " lambda", round(res$lambda,4), " var", signif(res$var_final,3),
    " kpss_p", res$kpss_p, " n", length(res$serie), "\n")
cat("rama elegida: abs(lambda) < 0.25 ?", abs(res$lambda) < 0.25, "\n")

cat("== Ejercicio 1: co2 ==\n")
cat("(max-min)/mean:", round((max(co2)-min(co2))/mean(co2),4), "\n")
ma <- tapply(co2, floor(time(co2)), mean); cat("medias anuales primera/última:", round(ma[1],2), round(ma[length(ma)],2),
  " subida %:", round(100*(ma[length(ma)]/ma[1]-1),1), "\n")
cat("lambda guerrero co2:", round(BoxCox.lambda(co2, method = "guerrero"),4), "\n")
cat("nsdiffs(co2):", nsdiffs(co2)); co2_s <- diff(co2, lag = 12); cat("  ndiffs(co2_s):", ndiffs(co2_s), "\n")
co2_sd <- diff(co2_s)
cat("r1 r12 co2:", round(acf(co2, 24, plot = FALSE)$acf[c(2,13)],4), " banda", round(1.96/sqrt(length(co2)),4), "\n")
cat("var d=0..3 tras nabla12:", round(sapply(0:3, function(d) var(difn(co2_s, d))),4), "\n")
cat("kpss.test(co2_sd) p:", suppressWarnings(kpss.test(co2_sd))$p.value, "\n")
rf <- acf(co2_sd, 24, plot = FALSE)$acf[-1]
cat("final: n", length(co2_sd), " var", round(var(co2_sd),4), " r1", round(rf[1],4),
    " fuera:", sum(abs(rf) > 1.96/sqrt(length(co2_sd))), "de 24\n")
cat("ndiffs(co2) sin diferencia estacional:", ndiffs(co2), "\n")

cat("== Ejercicio 2 ==\n")
set.seed(2026); p <- replicate(500, suppressWarnings(adf.test(cumsum(rnorm(100)))$p.value))
cat("rechazo 5% y 10%:", 100*mean(p < 0.05), 100*mean(p < 0.10), "\n")
set.seed(2026); p2 <- replicate(500, suppressWarnings(adf.test(rnorm(100))$p.value))
cat("potencia sobre ruido blanco:", 100*mean(p2 < 0.05), "\n")
cat("p-valores en el tope 0.01 (sobre ruido blanco):", 100*mean(p2 <= 0.01), "%\n")

cat("== Ejercicio 3: USAccDeaths ==\n")
y <- USAccDeaths
cat("ndiffs(y)", ndiffs(y), " nsdiffs(y)", nsdiffs(y), " ndiffs(diff(y,12))", ndiffs(diff(y, lag = 12)), "\n")
banda <- function(x) 1.96 / sqrt(length(x))
resumen <- function(x, nombre) {
  r <- acf(x, lag.max = 24, plot = FALSE)$acf[-1]
  data.frame(serie = nombre, n = length(x), varianza = round(var(x)),
             r1 = round(r[1], 4), r12 = round(r[12], 4),
             fuera = sum(abs(r) > banda(x)),
             ljung_box_p = signif(Box.test(x, lag = 24, type = "Ljung-Box")$p.value, 4))
}
print(rbind(resumen(y, "original"), resumen(diff(y), "nabla"),
      resumen(diff(y, lag = 12), "nabla12"), resumen(diff(diff(y), lag = 12), "nabla12 nabla")))

cat("== Ejercicio 4 / quiz ==\n")
cat("caminata: min valor", round(min(cumsum({set.seed(2026); rnorm(200)})),3), "\n")
cat("1.96/12 =", 1.96/12, "  1.96/144 =", 1.96/144, " cociente", (1.96/12)/(1.96/144), "\n")
cat("0.5^12 =", 0.5^12, "  banda n=143:", round(1.96/sqrt(143),4), "\n")
d1 <- diff(lx); r <- acf(d1, 24, plot = FALSE)$acf[-1]
cat("nabla log AP: fuera de banda en k =", which(abs(r) > 1.96/sqrt(143)), "\n")

cat("== Referencias en la ayuda de R ==\n")
ayuda <- function(f, pkg) { h <- utils:::.getHelpFile(help(f, package = (pkg)))
  tx <- capture.output(tools::Rd2txt(h, options = list(underline_titles = FALSE)))
  i <- grep("References", tx); if (length(i)) cat(paste(tx[i[1]:min(length(tx), i[1]+14)], collapse = "\n"), "\n") }
ayuda("kpss.test", "tseries"); ayuda("adf.test", "tseries"); ayuda("BoxCox.lambda", "forecast")
h <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("adf.test", package = "tseries"))))
cat(grep("interpolated|alternative|stationary", h, value = TRUE), sep = "\n")

cat("== M8 apoyo: forecast::BoxCox admite negativos con lambda > 0 ==\n")
print(body(forecast::BoxCox)); print(BoxCox(c(-2, 4), 0.5))
