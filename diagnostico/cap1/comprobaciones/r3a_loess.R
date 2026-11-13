# R3 (primera mitad) · Loess alineado con stl(): radio = distancia al vecino
# más lejano, sin el «+ 1».
#
# Réplica en R de las funciones del simulador `loess-local` (pesoTricubo,
# ventanaLocal, ajusteLocal, mediaMovilCentrada), sobre LOS MISMOS datos que
# usa el simulador: los vectores redondeados a 4 decimales de DATOS_CAP1 en el
# HTML (des = stl_log.tendencia + stl_log.residuo). Después se compara con
# stl() calculado de nuevo.
#
# Uso (desde la raíz del repo):
#   Rscript diagnostico/cap1/comprobaciones/r3a_loess.R > diagnostico/cap1/comprobaciones/r3a_loess.out
suppressPackageStartupMessages(library(jsonlite))
html <- "Htmls_Series/capitulo-1-componentes-descomposicion.html"
lin <- grep("const DATOS_CAP1 = ", readLines(html, warn = FALSE), value = TRUE)[1]
D <- fromJSON(sub(";\\s*$", "", sub("^\\s*const DATOS_CAP1 = ", "", lin)))
fechas <- D$fechas
stlT <- D$stl_log$tendencia
des <- D$stl_log$tendencia + D$stl_log$residuo   # lo que hace el simulador
n <- length(des)
stopifnot(n == 144)

tric <- function(u) { a <- abs(u); ifelse(a >= 1, 0, (1 - a^3)^3) }

ventana <- function(n, foco, span) {            # foco en base 1
  k <- (span - 1) %/% 2
  ini <- foco - k; fin <- foco + k
  if (ini < 1) { fin <- min(n, fin + (1 - ini)); ini <- 1 }
  if (fin > n) { ini <- max(1, ini - (fin - n)); fin <- n }
  ini:fin
}

# mas = 0: convención de stl() (la nueva del simulador); mas = 1: la anterior
ajuste <- function(y, foco, span, grado, tricubo, mas = 0) {
  idx <- ventana(length(y), foco, span)
  x <- idx - foco
  radio <- max(abs(x)) + mas
  w <- if (tricubo) tric(x / radio) else rep(1, length(x))
  sw <- sum(w); sx <- sum(w * x); sy <- sum(w * y[idx])
  sxx <- sum(w * x * x); sxy <- sum(w * x * y[idx])
  b <- 0
  if (grado == 1) { den <- sw * sxx - sx^2; if (den != 0) b <- (sw * sxy - sx * sy) / den }
  list(nivel = (sy - b * sx) / sw, pendiente = b, pesos = w, idx = idx, radio = radio)
}
curva <- function(y, span, grado, tricubo, mas = 0)
  sapply(seq_along(y), function(t) ajuste(y, t, span, grado, tricubo, mas)$nivel)
mm_impar <- function(y, m) {
  k <- m %/% 2; out <- rep(NA_real_, length(y))
  for (t in (k + 1):(length(y) - k)) out[t] <- mean(y[(t - k):(t + k)])
  out
}
f4 <- function(x) formatC(x, format = "f", digits = 4)

cat("== 1. Pesos tricúbicos en una ventana de 19 meses ==\n")
cat("radio = 9 (stl(), y ahora el simulador): u = 3/9, 6/9, 9/9 ->", f4(tric(c(3, 6, 9) / 9)), "\n")
cat("   con más decimales:", format(tric(c(3, 6, 9) / 9), digits = 10), "\n")
cat("radio = 10 (convención anterior): u = 0.3, 0.6, 0.9 ->", f4(tric(c(3, 6, 9) / 10)),
    " ; 1/w(0.9) =", round(1 / tric(0.9), 1), "\n")
a72 <- ajuste(des, 72, 19, 1, TRUE)
cat("ventana del foco 72 (", fechas[72], "): de", fechas[min(a72$idx)], "a", fechas[max(a72$idx)],
    "; radio =", a72$radio, "\n")
cat("pesos de esa ventana (distancias 0..9):", f4(a72$pesos[10:19]), "\n")
cat("vecinos con peso > 0:", sum(a72$pesos > 0), "de", length(a72$pesos),
    "; 1/w a 6 meses =", round(1 / tric(6 / 9), 2), "; w(3 meses)/w(6 meses) =", round(tric(3 / 9) / tric(6 / 9), 2), "\n")
a1 <- ajuste(des, 1, 19, 1, TRUE)
cat("ventana del foco 1 (", fechas[1], "): de", fechas[min(a1$idx)], "a", fechas[max(a1$idx)],
    "; radio =", a1$radio, "; peso del vecino más lejano =", f4(a1$pesos[19]), "\n")
a144 <- ajuste(des, 144, 19, 1, TRUE)
cat("ventana del foco 144 (", fechas[144], "): de", fechas[min(a144$idx)], "a", fechas[max(a144$idx)],
    "; radio =", a144$radio, "\n")

cat("\n== 2. Las cifras que la prosa toma del simulador (span 19) ==\n")
linea <- function(foco, mas) {
  g1 <- ajuste(des, foco, 19, 1, TRUE, mas)$nivel
  g0 <- ajuste(des, foco, 19, 0, TRUE, mas)$nivel
  p0 <- ajuste(des, foco, 19, 0, FALSE, mas)$nivel
  p1 <- ajuste(des, foco, 19, 1, FALSE, mas)$nivel
  mm <- mm_impar(des, 19)[foco]
  cat(sprintf("%s (foco %3d) radio%s | grado 1 tricubo %s | grado 0 tricubo %s | dif %s | grado 0 planos %s | grado 1 planos %s | media movil 19 %s | stl() %s\n",
      fechas[foco], foco, if (mas) "+1" else "  ", f4(g1), f4(g0), f4(abs(g1 - g0)), f4(p0), f4(p1),
      if (is.na(mm)) "  NA  " else f4(mm), f4(stlT[foco])))
  invisible(c(g1 = g1, g0 = g0))
}
cat("-- convención anterior (radio + 1) --\n")
for (f in c(72, 144, 1)) linea(f, 1)
cat("-- convención de stl() (radio = distancia al vecino más lejano): la del simulador desde R3 --\n")
for (f in c(72, 144, 1)) linea(f, 0)
v72 <- linea(72, 0)
cat("dic-1954: |grado 1 - grado 0| =", format(abs(v72["g1"] - v72["g0"]), digits = 3),
    " (misma cifra con todos los decimales:", isTRUE(all.equal(unname(v72["g1"]), unname(v72["g0"]), tolerance = 1e-12)), ")\n")
v144 <- linea(144, 0)
cat("dic-1960: grado 0 - grado 1 =", f4(v144["g0"] - v144["g1"]), "(el nivel queda por",
    if (v144["g0"] < v144["g1"]) "DEBAJO" else "ENCIMA", "de la recta) ; recta - stl() =",
    f4(v144["g1"] - stlT[144]), "; nivel - stl() =", f4(v144["g0"] - stlT[144]), "\n")
v1 <- linea(1, 0)
cat("ene-1949: grado 0 - grado 1 =", f4(v1["g0"] - v1["g1"]), "; recta - stl() =", f4(v1["g1"] - stlT[1]), "\n")
cat("media móvil de 19: primeros y últimos NA =", sum(is.na(mm_impar(des, 19)[1:20])), "y",
    sum(is.na(mm_impar(des, 19)[125:144])), "\n")

cat("\n== 3. La curva del simulador frente a la tendencia de stl() ==\n")
cur0 <- curva(des, 19, 1, TRUE, 0)   # nueva
cur1 <- curva(des, 19, 1, TRUE, 1)   # anterior
d0 <- abs(cur0 - stlT); d1 <- abs(cur1 - stlT)
cat("frente a la tendencia incrustada (stl por defecto, 4 decimales):\n")
cat("  antes (radio + 1): máx |dif| =", f4(max(d1)), "en", fechas[which.max(d1)], "; media =", f4(mean(d1)),
    "; meses que coinciden a 4 decimales:", sum(round(cur1, 4) == stlT), "de 144\n")
cat("  ahora (radio)    : máx |dif| =", f4(max(d0)), "en", fechas[which.max(d0)], "; media =", f4(mean(d0)),
    "; meses que coinciden a 4 decimales:", sum(round(cur0, 4) == stlT), "de 144\n")
impar <- seq(1, 143, 2)   # instantes en que stl() ajusta de verdad con t.jump = 2: 1, 3, ..., 143 y el 144
eval2 <- c(impar, 144); interp <- setdiff(1:144, eval2)
cat("  ahora, en los", length(eval2), "meses en que stl() ajusta (1, 3, …, 143 y 144): máx |dif| =", format(max(d0[eval2]), digits = 3),
    "; coinciden a 4 decimales:", sum(round(cur0[eval2], 4) == stlT[eval2]), "\n")
cat("  ahora, en los", length(interp), "meses que stl() interpola (2, 4, …, 142): máx |dif| =", f4(max(d0[interp])),
    "en", fechas[interp][which.max(d0[interp])], "; media =", f4(mean(d0[interp])),
    "; coinciden a 4 decimales:", sum(round(cur0[interp], 4) == stlT[interp]), "\n")
cat("  ahora, |dif| > 0.0005 en", sum(d0 > 0.0005), "meses; > 0.001 en", sum(d0 > 0.001), "; > 0.002 en", sum(d0 > 0.002), "\n")
cat("  los cinco mayores:", paste(fechas[order(-d0)[1:5]], f4(sort(d0, decreasing = TRUE)[1:5])), "\n")

cat("\n== 4. Contra stl() calculado de nuevo ==\n")
lx <- log(AirPassengers)
s2 <- stl(lx, s.window = "periodic")                 # por defecto
s1 <- stl(lx, s.window = "periodic", t.jump = 1)     # ajuste en todos los instantes
cat("stl por defecto: ventanas (s, t, l) =", s2$win, "; saltos (s, t, l) =", s2$jump, "; inner =", s2$inner, "outer =", s2$outer, "\n")
cat("incrustado == round(stl por defecto, 4):", all(round(as.numeric(s2$time.series[, "trend"]), 4) == stlT),
    all(round(as.numeric(s2$time.series[, "remainder"]), 4) == D$stl_log$residuo), "\n")
t2 <- as.numeric(s2$time.series[, "trend"]); t1 <- as.numeric(s1$time.series[, "trend"])
# (a) Loess del simulador (datos redondeados) frente a stl() por defecto sin redondear
cat("(a) simulador - stl(t.jump = 2, por defecto):          máx |dif| =", format(max(abs(cur0 - t2)), digits = 3),
    "en", fechas[which.max(abs(cur0 - t2))], "\n")
# (b) El mismo ajuste sobre la desestacionalizada SIN redondear de stl por defecto
des2 <- as.numeric(lx - s2$time.series[, "seasonal"])
c2 <- curva(des2, 19, 1, TRUE, 0)
cat("(b) ajuste local sobre lx - S de stl por defecto, sin redondear, frente a su tendencia:\n")
cat("      en los meses en que stl() ajusta: máx |dif| =", format(max(abs(c2 - t2)[eval2]), digits = 3), "\n")
cat("      en los que interpola            : máx |dif| =", format(max(abs(c2 - t2)[interp]), digits = 3), "\n")
# (c) Con t.jump = 1 stl() ajusta en todos: la tendencia ES el ajuste local de su desestacionalizada
des1 <- as.numeric(lx - s1$time.series[, "seasonal"])
c1 <- curva(des1, 19, 1, TRUE, 0)
cat("(c) stl(t.jump = 1): ajuste local sobre su lx - S frente a su tendencia: máx |dif| =", format(max(abs(c1 - t1)), digits = 3), "\n")
cat("    y con la convención anterior (radio + 1):                              máx |dif| =",
    format(max(abs(curva(des1, 19, 1, TRUE, 1) - t1)), digits = 3), "\n")
# (d) El simulador (datos incrustados) frente a stl(t.jump = 1)
cat("(d) simulador - stl(t.jump = 1): máx |dif| =", format(max(abs(cur0 - t1)), digits = 3), "en", fechas[which.max(abs(cur0 - t1))],
    "; coinciden a 4 decimales:", sum(round(cur0, 4) == round(t1, 4)), "de 144\n")
cat("    máx |tendencia(t.jump = 2) - tendencia(t.jump = 1)| =", format(max(abs(t2 - t1)), digits = 3), "en", fechas[which.max(abs(t2 - t1))], "\n")
cat("    máx |estacional(t.jump = 2) - estacional(t.jump = 1)| =", format(max(abs(s2$time.series[, 1] - s1$time.series[, 1])), digits = 3), "\n")
cat("    dic-1960: stl por defecto", f4(t2[144]), "; stl(t.jump = 1)", f4(t1[144]), "; simulador", f4(cur0[144]), "\n")
cat("    dic-1954: stl por defecto", f4(t2[72]), "; stl(t.jump = 1)", f4(t1[72]), "; simulador", f4(cur0[72]), "\n")
cat("    ene-1949: stl por defecto", f4(t2[1]), "; stl(t.jump = 1)", f4(t1[1]), "; simulador", f4(cur0[1]), "\n")
# (e) La interpolación de stl() entre dos ajustes: ¿lineal?
lin <- (cur0[impar[-length(impar)]] + cur0[impar[-1]]) / 2   # media de los dos vecinos impares
cat("(e) en los meses pares, |stl - media de los dos ajustes vecinos del simulador|: máx =",
    format(max(abs(stlT[interp] - lin)), digits = 3), "(si es ~1e-4, stl() interpola en línea recta)\n")

cat("\n== 5. Tabla completa: foco, simulador (grado 1, tricubo, span 19) y stl() ==\n")
tab <- data.frame(fecha = fechas, simulador = f4(cur0), stl = f4(stlT), dif = f4(cur0 - stlT),
                  stl_ajusta = ifelse(seq_len(n) %in% eval2, "sí", "interpola"))
print(tab, row.names = FALSE)
