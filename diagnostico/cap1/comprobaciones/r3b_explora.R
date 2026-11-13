# R3b · exploracion previa a redactar (M6, M7, M8). Solo R base.
# Uso: Rscript diagnostico/cap1/comprobaciones/r3b_explora.R > diagnostico/cap1/comprobaciones/r3b_explora.out
options(width = 150, digits = 6)
y  <- AirPassengers
lx <- log(y)
anio <- floor(time(y) + 1e-6); mes <- cycle(y)
sd_anual <- function(r) round(tapply(as.numeric(r), anio, sd, na.rm = TRUE), 4)

cat("===== A. Los pasos de stl(), comprobados ejecutando =====\n")
s2 <- stl(lx, s.window = "periodic")
cat("win:", s2$win, " deg:", s2$deg, " jump:", s2$jump, " inner:", s2$ni, " outer:", s2$no, "\n")
s1 <- stl(lx, s.window = "periodic", inner = 1)
# A1. Primera pasada: la estacionalidad se saca de la serie tal cual (tendencia inicial 0)?
#     Con periodic, el suavizado de cada subserie es su media; luego se le quita el nivel (filtro de paso bajo).
medias_mes <- tapply(as.numeric(lx), mes, mean)
cat("A1. inner = 1: estacional de stl() frente a (media de cada mes - media general):\n")
print(round(rbind(stl = as.numeric(s1$time.series[1:12, "seasonal"]), medias = as.numeric(medias_mes - mean(medias_mes))), 4))
cat("    max |dif| =", max(abs(as.numeric(s1$time.series[1:12, "seasonal"]) - as.numeric(medias_mes - mean(medias_mes)))), "\n")
# A2. Segunda pasada: la estacionalidad se vuelve a sacar de la serie SIN la tendencia de la primera?
T1 <- s1$time.series[, "trend"]
medias_det <- tapply(as.numeric(lx - T1), mes, mean)
cat("A2. inner = 2: estacional de stl() frente a (media de cada mes de la serie sin la tendencia de la pasada 1, centrada):\n")
print(round(rbind(stl = as.numeric(s2$time.series[1:12, "seasonal"]), medias = as.numeric(medias_det - mean(medias_det))), 4))
cat("    max |dif| =", max(abs(as.numeric(s2$time.series[1:12, "seasonal"]) - as.numeric(medias_det - mean(medias_det)))), "\n")
cat("    (y frente a las medias de la serie SIN quitar tendencia: max |dif| =",
    max(abs(as.numeric(s2$time.series[1:12, "seasonal"]) - as.numeric(medias_mes - mean(medias_mes)))), ")\n")
# A3. El componente estacional queda sin nivel: suma de los 12
cat("A3. suma de los 12 valores estacionales (periodic):", sum(s2$time.series[1:12, "seasonal"]), "\n")
s11 <- stl(lx, s.window = 11)
cat("    s.window = 11: media del componente estacional por anio (debe rondar 0):\n"); print(round(tapply(as.numeric(s11$time.series[, "seasonal"]), anio, mean), 5))
# A4. El residuo es lo que queda
cat("A4. max |x - S - T - R| =", max(abs(lx - rowSums(s2$time.series))), "\n")
# A5. La tendencia es el suavizado de la desestacionalizada (lo comprobo r3a_loess.R: 2.9e-08 con t.jump = 1)
cat("A6. pasadas: sin robust inner/outer =", s2$ni, s2$no, "; con robust =", stl(lx, "periodic", robust = TRUE)$ni, stl(lx, "periodic", robust = TRUE)$no, "\n")
cat("    s.window = 11 -> win:", s11$win, " jump:", s11$jump, "\n")
s11_19 <- stl(lx, s.window = 11, t.window = 19)
cat("    s.window = 11 con t.window = 19 frente a 21: max |dif| estacional =", max(abs(s11$time.series[, 1] - s11_19$time.series[, 1])),
    " tendencia =", max(abs(s11$time.series[, 2] - s11_19$time.series[, 2])), "\n")

cat("\n===== B. Flexibilidad: periodic frente a s.window = 11 (serie original) =====\n")
jul <- which(mes == 7)
cat("Julio estacional, periodic (log):", round(unique(as.numeric(s2$time.series[jul, 1])), 4), " exp:", round(exp(unique(round(as.numeric(s2$time.series[jul, 1]), 10))), 4), "\n")
cat("Julio estacional, s.window = 11 (log), 1949..1960:\n"); print(round(as.numeric(s11$time.series[jul, 1]), 4))
cat("  en % sobre la tendencia (exp - 1):\n"); print(round(100 * (exp(as.numeric(s11$time.series[jul, 1])) - 1), 1))
cat("  recorrido (log):", round(diff(range(s11$time.series[jul, 1])), 4), "\n")
cat("  con t.window = 19: % 1949 y 1960:", round(100 * (exp(as.numeric(s11_19$time.series[jul, 1])) - 1), 1)[c(1, 12)], "\n")
cat("Recorrido de cada mes con s.window = 11 (log):\n"); print(round(tapply(as.numeric(s11$time.series[, 1]), mes, function(v) diff(range(v))), 4))
cat("Cocientes clasicos de julio (y / media movil), 1949-1959, para comparar el sentido:\n")
dc <- decompose(y, type = "multiplicative")
print(round(as.numeric((y / dc$trend)[jul]), 3))

cat("\n===== C. Por que el residuo de la STL periodica es mas disperso en los extremos =====\n")
R2 <- s2$time.series[, "remainder"]; R11 <- s11$time.series[, "remainder"]
cat("sd del residuo por anio, periodic:\n"); print(sd_anual(R2))
cat("sd del residuo por anio, s.window = 11:\n"); print(sd_anual(R11))
tramo <- function(r) round(c(primeros_49_53 = mean(sd_anual(r)[1:5]), centro_54_57 = mean(sd_anual(r)[6:9]), ultimos_58_60 = mean(sd_anual(r)[10:12])), 4)
cat("media de las sd anuales por tramo, periodic:\n"); print(tramo(R2))
cat("media de las sd anuales por tramo, s.window = 11:\n"); print(tramo(R11))
cat("razon extremos/centro: periodic", round(mean(sd_anual(R2)[c(1:5, 10:12)]) / mean(sd_anual(R2)[6:9]), 2),
    " s.window = 11", round(mean(sd_anual(R11)[c(1:5, 10:12)]) / mean(sd_anual(R11)[6:9]), 2), "\n")
cat("sd global: periodic", round(sd(R2), 4), " s.window = 11", round(sd(R11), 4), "\n")
cat("Residuo de julio por anio, periodic:\n"); print(round(as.numeric(R2[jul]), 4))
cat("Residuo de julio por anio, s.window = 11:\n"); print(round(as.numeric(R11[jul]), 4))
# El patron estacional 'verdadero' cambia: residuo periodic, media por mes en los primeros 5 y los ultimos 5 anios
m_ini <- tapply(as.numeric(R2)[anio <= 1953], mes[anio <= 1953], mean)
m_cen <- tapply(as.numeric(R2)[anio >= 1954 & anio <= 1957], mes[anio >= 1954 & anio <= 1957], mean)
m_fin <- tapply(as.numeric(R2)[anio >= 1958], mes[anio >= 1958], mean)
cat("Residuo periodic: media por mes, 1949-1953 / 1954-1957 / 1958-1960:\n"); print(round(rbind(ini = m_ini, cen = m_cen, fin = m_fin), 4))
cat("  correlacion entre el patron medio de los primeros anios y el de los ultimos:", round(cor(m_ini, m_fin), 3), "\n")
# Cuanto de la varianza del residuo periodic por tramo es 'patron mensual medio del tramo'
frac <- function(sel) { r <- as.numeric(R2)[sel]; mm <- tapply(r, mes[sel], mean)[as.character(mes[sel])]; round(1 - var(r - mm) / var(r), 3) }
cat("  parte de la varianza del residuo que es patron mensual repetido dentro del tramo: ini", frac(anio <= 1953), " cen", frac(anio >= 1954 & anio <= 1957), " fin", frac(anio >= 1958), "\n")
# La diferencia entre los dos residuos es exactamente lo que el estacional flexible recoge de mas (mas diferencia de tendencia)
dS <- s11$time.series[, 1] - s2$time.series[, 1]; dT <- s11$time.series[, 2] - s2$time.series[, 2]
cat("  S(11) - S(periodic): sd por anio:\n"); print(sd_anual(dS))
cat("  T(11) - T(periodic): max |dif| =", round(max(abs(dT)), 4), "\n")
cat("  sd por anio de [R(periodic) - (S(11) - S(periodic))] :\n"); print(sd_anual(R2 - dS))
cat("ACF del residuo, rezagos 1 y 12: periodic", round(acf(R2, plot = FALSE)$acf[c(2, 13)], 3), " s.window = 11", round(acf(R11, plot = FALSE)$acf[c(2, 13)], 3), " banda", round(1.96 / sqrt(144), 3), "\n")

cat("\n===== D. Robustez: julio de 1955 x 1.5 =====\n")
yc <- y; yc[79] <- yc[79] * 1.5; lc <- log(yc)
v <- list(
  limpia_per_norob = s2, limpia_per_rob = stl(lx, "periodic", robust = TRUE),
  limpia_11_norob = s11, limpia_11_rob = stl(lx, s.window = 11, robust = TRUE),
  cont_per_norob = stl(lc, "periodic"), cont_per_rob = stl(lc, "periodic", robust = TRUE),
  cont_11_norob = stl(lc, s.window = 11), cont_11_rob = stl(lc, s.window = 11, robust = TRUE))
res <- t(sapply(v, function(s) {
  ts <- s$time.series
  c(S_jul49 = ts[7, 1], S_jul55 = ts[79, 1], S_jul60 = ts[139, 1], idx55 = exp(ts[79, 1]), T_jul55 = ts[79, 2], expT55 = exp(ts[79, 2]), R_jul55 = ts[79, 3],
    maxR = max(abs(ts[, 3])), minRes = min(ts[, 3]), maxRes = max(ts[, 3]), peso0 = sum(s$weights < 1e-8), peso_menor_05 = sum(s$weights < 0.5), w79 = s$weights[79])
}))
print(round(res, 4))
cat("Rangos por componente en las 8 variantes (para fijar ejes):\n")
print(round(t(sapply(v, function(s) c(S = range(s$time.series[, 1]), T = range(s$time.series[, 2]), R = range(s$time.series[, 3])))), 4))
cat("Tendencia alrededor de julio de 1955 (obs 73..85), limpia / contaminada sin robust / contaminada con robust (periodic):\n")
print(round(rbind(limpia = s2$time.series[73:85, 2], cont_norob = v$cont_per_norob$time.series[73:85, 2], cont_rob = v$cont_per_rob$time.series[73:85, 2]), 4))
cat("  max |T cont_norob - T limpia| =", round(max(abs(v$cont_per_norob$time.series[, 2] - s2$time.series[, 2])), 4), "en obs", which.max(abs(v$cont_per_norob$time.series[, 2] - s2$time.series[, 2])),
    "; max |T cont_rob - T limpia_rob| =", round(max(abs(v$cont_per_rob$time.series[, 2] - v$limpia_per_rob$time.series[, 2])), 4),
    "; max |T cont_rob - T limpia_norob| =", round(max(abs(v$cont_per_rob$time.series[, 2] - s2$time.series[, 2])), 4), "\n")
cat("  indice de julio (exp): limpia sin robust", round(exp(s2$time.series[7, 1]), 4), "-> cont sin robust", round(exp(v$cont_per_norob$time.series[7, 1]), 4),
    "; limpia con robust", round(exp(v$limpia_per_rob$time.series[7, 1]), 4), "-> cont con robust", round(exp(v$cont_per_rob$time.series[7, 1]), 4), "\n")
cat("  log(1.5) =", round(log(1.5), 4), "\n")
cat("  observaciones con peso 0, cont_per_rob:", which(v$cont_per_rob$weights < 1e-8), " limpia_per_rob:", which(v$limpia_per_rob$weights < 1e-8), "\n")

cat("\n===== E. Clasica aditiva junto a la multiplicativa =====\n")
da <- decompose(y, type = "additive")
cat("aditiva: indices (figure):\n"); print(round(da$figure, 2))
cat("  julio 1955: y", y[79], " T", da$trend[79], " S", round(da$seasonal[79], 2), " R", round(da$random[79], 2), "\n")
cat("  sd del residuo aditivo por anio:\n"); print(round(tapply(as.numeric(da$random), anio, sd, na.rm = TRUE), 1))
Sm_miles <- dc$trend * (dc$seasonal - 1); Rm_miles <- y - dc$trend * dc$seasonal
cat("  identidad y = T + T(S-1) + (y - TS): max |dif| =", max(abs(y - dc$trend - Sm_miles - Rm_miles), na.rm = TRUE), "\n")
cat("  sd del residuo multiplicativo EN MILES (y - T*S) por anio:\n"); print(round(tapply(as.numeric(Rm_miles), anio, sd, na.rm = TRUE), 1))
cat("  sd del residuo multiplicativo (factor) por anio:\n"); print(round(tapply(as.numeric(dc$random), anio, sd, na.rm = TRUE), 4))
cat("  rangos: S aditiva", round(range(da$seasonal), 1), " S mult en miles", round(range(Sm_miles, na.rm = TRUE), 1), " R aditiva", round(range(da$random, na.rm = TRUE), 1), " R mult miles", round(range(Rm_miles, na.rm = TRUE), 1), "\n")
cat("  sd global: R aditiva", round(sd(da$random, na.rm = TRUE), 2), " R mult miles", round(sd(Rm_miles, na.rm = TRUE), 2), "\n")
cat("  julio: efecto estacional mult en miles T*(S-1), 1949..1960:\n"); print(round(as.numeric(Sm_miles[jul]), 1))
cat("  julio: residuo aditivo, 1949..1960:\n"); print(round(as.numeric(da$random[jul]), 1))
cat("  residuo aditivo, media por mes 1949-1953 y 1956-1960:\n")
print(round(rbind(ini = tapply(as.numeric(da$random)[anio <= 1953], mes[anio <= 1953], mean, na.rm = TRUE), fin = tapply(as.numeric(da$random)[anio >= 1956], mes[anio >= 1956], mean, na.rm = TRUE)), 1))
cat("  ACF del residuo, rezago 12: aditiva", round(acf(na.omit(as.numeric(da$random)), plot = FALSE)$acf[13], 3), " multiplicativa", round(acf(na.omit(as.numeric(dc$random)), plot = FALSE)$acf[13], 3), "\n")

cat("\n===== F. M8: desestacionalizada con STL frente a la clasica; fuerzas =====\n")
aj_stl <- y / exp(s2$time.series[, 1]); aj_cla <- y / dc$seasonal
cat("aj STL = exp(log y - S) = exp(T + R): max |dif| =", max(abs(aj_stl - exp(s2$time.series[, 2] + s2$time.series[, 3]))), "\n")
cat("max |aj STL - aj clasica| =", round(max(abs(aj_stl - aj_cla)), 2), "en obs", which.max(abs(aj_stl - aj_cla)), "(", format(time(y)[which.max(abs(aj_stl - aj_cla))]), ") ; media |dif| =", round(mean(abs(aj_stl - aj_cla)), 2), "\n")
cat("  en %: max", round(100 * max(abs(aj_stl / aj_cla - 1)), 2), "\n")
cat("  julio 1955: aj STL", round(aj_stl[79], 1), " aj clasica", round(aj_cla[79], 1), "\n")
cat("  indices exp(S) STL:", round(exp(s2$time.series[1:12, 1]), 4), "\n  indices clasicos:", round(dc$figure, 4), "\n")
fuerzas <- function(x, ...) { st <- stl(x, ...)$time.series; R <- st[, 3]
  round(c(FT = max(0, 1 - var(R) / var(st[, 2] + R)), FS = max(0, 1 - var(R) / var(st[, 1] + R))), 4) }
set.seed(20948); ruido <- ts(rnorm(144), start = c(1949, 1), frequency = 12)
cand <- list(`log(AirPassengers)` = log(AirPassengers), co2 = co2, nottem = nottem, USAccDeaths = USAccDeaths, mdeaths = mdeaths, ldeaths = ldeaths,
             UKDriverDeaths = UKDriverDeaths, `log(UKgas)` = log(UKgas), sunspots = sunspots, `log(JohnsonJohnson)` = log(JohnsonJohnson), lynxNO = NULL, ruido = ruido)
cand <- cand[!sapply(cand, is.null)]
cat("Fuerzas con s.window = 'periodic':\n"); print(t(sapply(cand, fuerzas, s.window = "periodic")))
cat("Fuerzas con s.window = 11:\n"); print(t(sapply(cand, fuerzas, s.window = 11)))
cat("Ruido blanco: 200 simulaciones de 144 normales, periodic: cuantiles de FT y FS\n")
set.seed(1); sim <- t(replicate(200, fuerzas(ts(rnorm(144), frequency = 12), s.window = "periodic")))
print(round(apply(sim, 2, quantile, c(0.05, 0.5, 0.95)), 3))
