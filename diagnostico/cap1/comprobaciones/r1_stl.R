# R1 · T1.2 · M7: pesos tricubicos, pasadas de los bucles, pesos de robustez,
# 19 frente a 21 en la ventana de tendencia, t.jump; y M8: fuerzas.
suppressPackageStartupMessages({
  library(tsibble); library(dplyr); library(fabletools); library(feasts)
})
AP <- AirPassengers; lx <- log(AP)

cat("== 1. Pesos tricubicos: convencion de stl() frente a la de la tabla ==\n")
tric <- function(u) ifelse(abs(u) < 1, (1 - abs(u)^3)^3, 0)
cat("tabla del capitulo (radio = 9 + 1 = 10): u = 0.3, 0.6, 0.9 ->",
    sprintf("%.4f", tric(c(3, 6, 9) / 10)), " ; 1/w(0.9) =", round(1 / tric(0.9), 1), "\n")
cat("stl() (radio = 9, el vecino mas lejano): u = 3/9, 6/9, 9/9 ->",
    sprintf("%.4f", tric(c(3, 6, 9) / 9)), "\n")
# Cual de las dos reproduce la tendencia de stl(): ajuste local reimplementado
s1 <- stl(lx, s.window = "periodic", inner = 1, outer = 0, t.jump = 1)
des <- as.numeric(lx - s1$time.series[, "seasonal"])
loc <- function(y, foco, q, plus) {
  n <- length(y); k <- (q - 1) %/% 2; ini <- foco - k; fin <- foco + k
  if (ini < 1) { fin <- min(n, fin - ini + 1); ini <- 1 }
  if (fin > n) { ini <- max(1, ini - (fin - n)); fin <- n }
  i <- ini:fin; x <- i - foco; h <- max(abs(x)) + plus
  w <- tric(abs(x) / h)
  unname(coef(lm(y[i] ~ x, weights = w))[1])
}
tr1 <- as.numeric(s1$time.series[, "trend"])
cat("max|ajuste local - tendencia de stl()| con radio = dist. max      :",
    signif(max(abs(sapply(1:144, loc, y = des, q = 19, plus = 0) - tr1)), 3), "\n")
cat("max|ajuste local - tendencia de stl()| con radio = dist. max + 1  :",
    signif(max(abs(sapply(1:144, loc, y = des, q = 19, plus = 1) - tr1)), 3), "\n")

cat("\n== 2. Pasadas de los bucles ==\n")
cat("valores por defecto en la firma de stl():\n")
print(formals(stl)[c("robust", "inner", "outer")])
s0 <- stl(lx, s.window = "periodic")
sR <- stl(lx, s.window = "periodic", robust = TRUE)
cat("sin robust: inner =", s0$inner, " outer =", s0$outer, "\n")
cat("con robust: inner =", sR$inner, " outer =", sR$outer, "\n")

cat("\n== 3. Ventana de tendencia: 19 con 'periodic', 21 con s.window = 11 ==\n")
cat("stl(lx, s.window = 'periodic')$win:", s0$win, "\n")
s11 <- stl(lx, s.window = 11)
cat("stl(lx, s.window = 11)$win       :", s11$win, "\n")
nextodd <- function(x) { x <- round(x); if (x %% 2 == 0) x + 1 else x }
cat("regla: periodic -> ", 1.5 * 12 / (1 - 1.5 / (10 * 144 + 1)), "-> techo e impar:",
    nextodd(ceiling(1.5 * 12 / (1 - 1.5 / (10 * 144 + 1)))), "\n")
cat("regla: s.window 11 -> ", 1.5 * 12 / (1 - 1.5 / 11), "-> techo e impar:",
    nextodd(ceiling(1.5 * 12 / (1 - 1.5 / 11))), "\n")
cat("t.jump por defecto (periodic):", s0$jump, "\n")
cat("max|tendencia(t.jump=2) - tendencia(t.jump=1)|:",
    signif(max(abs(stl(lx, s.window = "periodic", t.jump = 1)$time.series[, 2] - s0$time.series[, 2])), 3), "\n")
# tidyverts: el bloque del capitulo y sus variantes
ts_lx <- as_tsibble(log(AirPassengers))
comp <- function(f) ts_lx |> model(stl = STL(!!f)) |> components()
c19  <- ts_lx |> model(stl = STL(value ~ trend(window = 19) + season(window = "periodic"))) |> components()
cper <- ts_lx |> model(stl = STL(value ~ season(window = "periodic"))) |> components()
c21  <- ts_lx |> model(stl = STL(value ~ trend(window = 21) + season(window = "periodic"))) |> components()
cdef <- ts_lx |> model(stl = STL(value)) |> components()
cat("feasts, bloque del capitulo (trend 19 + periodic): S_julio =", round(exp(c19$season_year[7]), 4),
    " ; max|dif| con stats::stl(periodic):", signif(max(abs(c19$trend - s0$time.series[, 2])), 3), "\n")
cat("feasts, solo season('periodic'), sin trend(): max|dif tendencia| con la de 19:",
    signif(max(abs(cper$trend - c19$trend)), 3), "\n")
cat("feasts, trend(window = 21) + periodic: S_julio =", round(exp(c21$season_year[7]), 4), "\n")
cat("feasts, STL(value) por defecto: max|dif tendencia| con stats::stl(s.window = 11) [t.window 21]:",
    signif(max(abs(cdef$trend - s11$time.series[, 2])), 3), "\n")
jul <- s11$time.series[cycle(AP) == 7, "seasonal"]
cat("julio con s.window = 11: 1949", round(100 * (exp(jul[1]) - 1), 1), "%  1960",
    round(100 * (exp(jul[12]) - 1), 1), "%  recorrido en log:", round(diff(range(jul)), 4), "\n")
cat("julio-1955 (periodic): T", round(s0$time.series[79, 2], 4), " S", round(s0$time.series[79, 1], 4),
    " R", round(s0$time.series[79, 3], 4), " exp(S) =", round(exp(s0$time.series[79, 1]), 4), "\n")

cat("\n== 4. Pesos de robustez con julio de 1955 inflado un 50 % ==\n")
ap_out <- AP; ap_out[79] <- ap_out[79] * 1.5
cat("364 ->", ap_out[79], "\n")
sn <- stl(log(ap_out), s.window = "periodic")
R <- sn$time.series[, "remainder"]; thr <- 6 * median(abs(R)); u <- abs(R) / thr
w <- ifelse(u < 1, (1 - u^2)^2, 0)
cat("PRIMERA pasada (residuos del ajuste no robusto): |R79| =", round(abs(R[79]), 4), " umbral =", round(thr, 4),
    " u =", round(u[79], 2), " peso 0 en:", which(w == 0), " peso mediano del resto =", round(median(w[-79]), 4), "\n")
sr <- stl(log(ap_out), s.window = "periodic", robust = TRUE)
z <- which(sr$weights < 1e-12)
cat("AJUSTE COMPLETO robust = TRUE (", sr$outer, "pasadas exteriores): peso 0 en obs.", z, "\n")
fe <- paste(month.abb[cycle(AP)[z]], floor(time(AP))[z])
cat("   son:", paste(fe, collapse = ", "), "\n")
cat("   observaciones con peso < 0.5:", sum(sr$weights < 0.5), " ; peso mediano:", round(median(sr$weights), 4), "\n")
src <- stl(lx, s.window = "periodic", robust = TRUE)
zc <- which(src$weights < 1e-12)
cat("SERIE SIN CONTAMINAR, robust = TRUE: peso 0 en obs.", zc, "->",
    paste(month.abb[cycle(AP)[zc]], floor(time(AP))[zc], collapse = ", "), " ; < 0.5:", sum(src$weights < 0.5), "\n")
cat("indice de julio: limpio robusto", round(exp(src$time.series[7, 1]), 4), " contaminado robusto",
    round(exp(sr$time.series[7, 1]), 4), " limpio no robusto", round(exp(s0$time.series[7, 1]), 4),
    " contaminado no robusto", round(exp(sn$time.series[7, 1]), 4), "\n")
cat("clasica: limpio", round(decompose(AP, "multiplicative")$figure[7], 4), " contaminado",
    round(decompose(ap_out, "multiplicative")$figure[7], 4), "\n")

cat("\n== 5. Fuerzas (M8) ==\n")
fz <- function(x) { st <- stl(x, s.window = "periodic")$time.series
  c(FT = max(0, 1 - var(st[, 3]) / var(st[, 2] + st[, 3])), FS = max(0, 1 - var(st[, 3]) / var(st[, 1] + st[, 3]))) }
cat("stl(log(AP), s.window = 'periodic'):", round(fz(lx), 4), "\n")
ft <- ts_lx |> features(value, feat_stl)
cat("feasts::feat_stl sobre log(AP): trend_strength =", round(ft$trend_strength, 5),
    " seasonal_strength_year =", round(ft$seasonal_strength_year, 5), "\n")
cat("argumentos por defecto de feat_stl:\n"); print(formals(feat_stl))
cat("USAccDeaths:", round(fz(USAccDeaths), 4), "  co2:", round(fz(co2), 4), "\n")

cat("\n== 6. Lo que dice ?stl de los saltos y de los bucles ==\n")
h <- gsub("_\b", "", capture.output(tools::Rd2txt(utils:::.getHelpFile(help("stl")))))
i <- grep("s.jump, t.jump, l.jump|^ *inner:|^ *outer:|^ *robust:", h)
for (k in i) cat(trimws(h[k:(k + 3)]), "\n")
