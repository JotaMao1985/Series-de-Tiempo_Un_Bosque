# R3b · cada cifra nueva de la prosa de los Modulos 6, 7, 8 y 9, recalculada (R base).
# Uso: Rscript diagnostico/cap1/comprobaciones/r3b_cifras.R > diagnostico/cap1/comprobaciones/r3b_cifras.out
options(width = 150, digits = 7)
y <- AirPassengers; lx <- log(y); anio <- floor(time(y) + 1e-6); mes <- cycle(y); jul <- which(mes == 7)
sd_anual <- function(r) as.numeric(tapply(as.numeric(r), anio, sd, na.rm = TRUE))
tramo <- function(r) { s <- sd_anual(r); c(`1949-1953` = mean(s[1:5]), `1954-1957` = mean(s[6:9]), `1958-1960` = mean(s[10:12])) }

cat("===== M7 · los pasos de stl(), comprobados =====\n")
s2 <- stl(lx, s.window = "periodic"); s1 <- stl(lx, s.window = "periodic", inner = 1)
cat("stl(lx, 'periodic'): ventanas", s2$win, "| grados", s2$deg, "| saltos", s2$jump, "| pasadas interiores", s2$inner, "| vueltas exteriores", s2$outer, "\n")
sr <- stl(lx, s.window = "periodic", robust = TRUE)
cat("con robust = TRUE:   pasadas interiores", sr$inner, "| vueltas exteriores", sr$outer, "\n")
mm <- tapply(as.numeric(lx), mes, mean)
cat("Paso 1 con 'periodic' = media de cada subserie (una pasada): max |S - (media del mes - media general)| =",
    format(max(abs(as.numeric(s1$time.series[1:12, 1]) - as.numeric(mm - mean(mm)))), digits = 3), "\n")
md <- tapply(as.numeric(lx - s1$time.series[, "trend"]), mes, mean)
cat("Paso 4: en la segunda pasada el paso 1 parte de la serie SIN la tendencia de la primera: max |S - medias centradas| =",
    format(max(abs(as.numeric(s2$time.series[1:12, 1]) - as.numeric(md - mean(md)))), digits = 3),
    " (frente a las medias de la serie tal cual:", format(max(abs(as.numeric(s2$time.series[1:12, 1]) - as.numeric(mm - mean(mm)))), digits = 3), ")\n")
cat("Paso 3: suma de los doce valores estacionales ('periodic') =", format(sum(s2$time.series[1:12, 1]), digits = 3), "\n")
s11 <- stl(lx, s.window = 11)
cat("        s.window = 11: media anual del componente estacional, de", format(min(tapply(s11$time.series[, 1], anio, mean)), digits = 2), "a", format(max(tapply(s11$time.series[, 1], anio, mean)), digits = 2), "\n")
cat("Paso 5: max |log y - S - T - R| =", max(abs(lx - rowSums(s2$time.series))), "\n")
cat("Tendencia sin huecos: NA en la tendencia de stl() =", sum(is.na(s2$time.series[, 2])), "; en la de decompose() =", sum(is.na(decompose(y)$trend)), "\n")

cat("\n===== M7 · la ventana estacional =====\n")
cat("julio, 'periodic': +", round(100 * (exp(s2$time.series[7, 1]) - 1), 1), "% los doce anios (recorrido", round(diff(range(s2$time.series[jul, 1])), 4), ")\n")
cat("julio, s.window = 11, 1949..1960 (%):", round(100 * (exp(as.numeric(s11$time.series[jul, 1])) - 1), 1), "\n")
cat("  exp(S) de julio en 1949 y 1960:", round(exp(s11$time.series[c(7, 139), 1]), 3), "\n")
R2 <- s2$time.series[, 3]; R11 <- s11$time.series[, 3]
cat("residuo de julio, 'periodic', 1949..1960:", round(as.numeric(R2[jul]), 4), "\n")
cat("  negativos:", anio[jul][R2[jul] < 0], "| positivos:", anio[jul][R2[jul] > 0], "\n")
cat("sd del residuo por tramo, 'periodic'  :", round(tramo(R2), 4), "\n")
cat("sd del residuo por tramo, s.window 11 :", round(tramo(R11), 4), "\n")
cat("  bajada relativa por tramo:", round(100 * (1 - tramo(R11) / tramo(R2)), 0), "%\n")
for (w in c(7, 9, 13, 21)) cat("sd del residuo por tramo, s.window", w, ":", round(tramo(stl(lx, s.window = w)$time.series[, 3]), 4),
    " razon extremos/centro:", round(mean(sd_anual(stl(lx, s.window = w)$time.series[, 3])[c(1:5, 10:12)]) / mean(sd_anual(stl(lx, s.window = w)$time.series[, 3])[6:9]), 2), "\n")
cat("  razon extremos/centro: 'periodic'", round(mean(sd_anual(R2)[c(1:5, 10:12)]) / mean(sd_anual(R2)[6:9]), 2), " 11:", round(mean(sd_anual(R11)[c(1:5, 10:12)]) / mean(sd_anual(R11)[6:9]), 2), "\n")
ini <- anio <= 1953; fin <- anio >= 1958
p_ini <- tapply(as.numeric(R2)[ini], mes[ini], mean); p_fin <- tapply(as.numeric(R2)[fin], mes[fin], mean)
cat("residuo 'periodic': correlacion entre el patron mensual medio de 1949-1953 y el de 1958-1960 =", round(cor(p_ini, p_fin), 2), "\n")
cat("pico de mitad de anio (max de julio y agosto), s.window = 11: 1949", round(max(s11$time.series[7:8, 1]), 4), " 1960", round(max(s11$time.series[139:140, 1]), 4), "\n")

cat("\n===== M7 · el atipico =====\n")
yc <- y; yc[79] <- yc[79] * 1.5; lc <- log(yc)
cat("julio de 1955:", y[79], "->", yc[79], "; log(1.5) =", round(log(1.5), 4), "\n")
f <- function(s) c(jul_pct = round(100 * (exp(s$time.series[79, 1]) - 1), 1), T55 = round(exp(s$time.series[79, 2]), 1), R55 = round(s$time.series[79, 3], 4),
                   peso0 = sum(s$weights < 1e-8), w55 = round(s$weights[79], 4))
print(rbind(`limpia, sin robust` = f(s2), `inflada, sin robust` = f(stl(lc, "periodic")), `limpia, robust` = f(sr), `inflada, robust` = f(stl(lc, "periodic", robust = TRUE)),
            `inflada, s.window 11, sin robust` = f(stl(lc, s.window = 11)), `inflada, s.window 11, robust` = f(stl(lc, s.window = 11, robust = TRUE))))
a <- stl(lc, "periodic")$time.series[79, ] - s2$time.series[79, ]
cat("sin robust, lo que cambia en julio de 1955 respecto de la serie limpia: S", round(a[1], 4), " T", round(a[2], 4), " R", round(a[3], 4), " suma", round(sum(a), 4), "\n")
cat("pico de mitad de anio en las variantes s.window = 11 (1949 -> 1960):\n")
for (nm in c("inflada sin robust", "inflada robust", "limpia robust")) { s <- switch(nm, `inflada sin robust` = stl(lc, s.window = 11), `inflada robust` = stl(lc, s.window = 11, robust = TRUE), `limpia robust` = stl(lx, s.window = 11, robust = TRUE))
  cat("  ", nm, ":", round(max(s$time.series[7:8, 1]), 4), "->", round(max(s$time.series[139:140, 1]), 4), "\n") }
cat("residuo mas disperso en los extremos que en el centro, en las cuatro variantes sin atipico:\n")
for (sw in list("periodic", 11)) for (rb in c(FALSE, TRUE)) cat("  s.window", sw, " robust", rb, ":", round(tramo(stl(lx, s.window = sw, robust = rb)$time.series[, 3]), 4), "\n")

cat("\n===== M6 · la aditiva junto a la multiplicativa, en miles =====\n")
da <- decompose(y, "additive"); dm <- decompose(y, "multiplicative")
Sm <- dm$trend * (dm$seasonal - 1); Rm <- y - dm$trend * dm$seasonal
cat("identidad y = T + T(S - 1) + (y - TS): max |dif| =", format(max(abs(y - dm$trend - Sm - Rm), na.rm = TRUE), digits = 3), "\n")
cat("sd anual del residuo, aditiva       :", round(sd_anual(da$random), 1), "\n")
cat("sd anual del residuo, multiplicativa:", round(sd_anual(Rm), 1), "\n")
cat("  la aditiva es mayor en", sum(sd_anual(da$random) > sd_anual(Rm)), "de 12 anios\n")
cat("anchura de la banda estacional (max - min del anio), aditiva:", round(diff(range(da$figure)), 1), "todos los anios; multiplicativa, 1950 y 1959:",
    round(diff(range(Sm[anio == 1950])), 1), round(diff(range(Sm[anio == 1959])), 1), "\n")
cat("rangos: S aditiva", round(range(da$seasonal), 1), "| S mult", round(range(Sm, na.rm = TRUE), 1), "| R aditiva", round(range(da$random, na.rm = TRUE), 1), "| R mult", round(range(Rm, na.rm = TRUE), 1), "\n")
cat("residuo aditivo de julio, 1949..1959:", round(as.numeric(da$random[jul]), 1), "\n")

cat("\n===== M8 · de logaritmos a miles; desestacionalizada; fuerzas =====\n")
ts2 <- s2$time.series
cat("julio de 1955 en log: log y", round(lx[79], 4), "= T", round(ts2[79, 2], 4), "+ S", round(ts2[79, 1], 4), "+ R", round(ts2[79, 3], 4), "\n")
cat("  exp: T", round(exp(ts2[79, 2]), 2), " S", round(exp(ts2[79, 1]), 4), " R", round(exp(ts2[79, 3]), 4), "; septiembre: S", round(ts2[9, 1], 4), "->", round(100 * (exp(ts2[9, 1]) - 1), 1), "%\n")
aj <- y / exp(ts2[, 1]); ajc <- y / dm$seasonal
cat("desestacionalizada, julio de 1955: 364 / exp(S) =", round(aj[79], 1), "; con el indice clasico:", round(ajc[79], 1), "\n")
i <- which.max(abs(aj - ajc))
cat("  mayor diferencia entre las dos:", round(abs(aj - ajc)[i], 1), "mil (", round(100 * abs(aj / ajc - 1)[i], 1), "% ) en", anio[i], "mes", mes[i], "\n")
cat("  log y - S = T + R: max |dif| =", format(max(abs((lx - ts2[, 1]) - (ts2[, 2] + ts2[, 3]))), digits = 3), "\n")
fz <- function(x, ...) { st <- stl(x, ...)$time.series; R <- st[, 3]; c(FT = max(0, 1 - var(R) / var(st[, 2] + R)), FS = max(0, 1 - var(R) / var(st[, 1] + R))) }
cat("fuerzas, s.window = 'periodic' (3 decimales):\n")
for (nm in c("log(AirPassengers)", "nottem", "sunspots", "co2", "USAccDeaths")) cat(sprintf("  %-20s FT = %.3f  FS = %.3f\n", nm, fz(eval(parse(text = nm)), s.window = "periodic")[1], fz(eval(parse(text = nm)), s.window = "periodic")[2]))
cat(sprintf("  log(AirPassengers), s.window = 11: FT = %.3f  FS = %.3f\n", fz(lx, s.window = 11)[1], fz(lx, s.window = 11)[2]))
set.seed(20948); sim <- t(replicate(200, fz(ts(rnorm(144), frequency = 12), s.window = "periodic")))
cat("  ruido puro, 200 series de 144 normales (semilla 20948): mediana FT =", round(median(sim[, 1]), 2), " FS =", round(median(sim[, 2]), 2),
    "; 5 % y 95 %: FT", round(quantile(sim[, 1], c(.05, .95)), 2), " FS", round(quantile(sim[, 2], c(.05, .95)), 2), "; minimo FT", round(min(sim[, 1]), 3), " FS", round(min(sim[, 2]), 3), "\n")
tit <- function(tema) { rd <- utils:::.getHelpFile(help(tema)); paste(capture.output(tools::Rd2txt(rd, options = list(underline_titles = FALSE)))[1:2], collapse = " ") }
cat("?nottem  :", tit("nottem"), "| inicio", start(nottem), "fin", end(nottem), "frecuencia", frequency(nottem), "\n")
cat("?sunspots:", tit("sunspots"), "| inicio", start(sunspots), "fin", end(sunspots), "frecuencia", frequency(sunspots), "\n")
