# R1 del capítulo 2 · cifras publicadas a 3 decimales cuyo valor a 4 decimales acaba en 5:
# ¿se redondeó el valor exacto o el ya redondeado del JSON (doble redondeo)?
#   Rscript diagnostico/cap2/comprobaciones/r1_redondeo.R > diagnostico/cap2/comprobaciones/r1_redondeo.out 2>&1
suppressMessages({library(tseries); library(forecast)})
d <- read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")
trm <- ts(d$trm, start = c(2015, 1), frequency = 12)
sj <- jsonlite::fromJSON("precalculo/salidas/datos_series.json")
cat("CSV publicado == datos_series.json:", identical(as.numeric(trm), as.numeric(sj$trm$valores)),
    "· n =", length(trm), "· inicio", start(trm), "· fin", end(trm), "\n")
cat("el enlace de precalculo/ apunta al mismo archivo:",
    identical(readLines("precalculo/trm_mensual_2015-01_2026-06.csv"),
              readLines("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")), "\n\n")
lx <- log(AirPassengers); sw <- suppressWarnings
f <- function(nombre, v, publicado) cat(sprintf("%-46s exacto %.6f · a 4 dec. %.4f · a 3 dec. %.3f · publicado %s%s\n",
  nombre, v, round(v, 4), round(v, 3), publicado, if (sprintf("%.3f", round(v, 3)) != sub("−", "-", publicado)) "   <-- NO COINCIDE" else ""))
f("M6 tabla · ADF p, TRM", sw(adf.test(trm))$p.value, "0.586")
f("M6 tabla · KPSS nivel, dTRM", sw(kpss.test(diff(trm)))$statistic, "0.242")
f("M6 tabla · ADF, TRM", sw(adf.test(trm))$statistic, "-1.978")
f("M6 tabla · KPSS nivel, TRM", sw(kpss.test(trm))$statistic, "2.243")
f("M6 tabla · ADF, dTRM", sw(adf.test(diff(trm)))$statistic, "-3.880")
f("M6 tabla · ADF p, dTRM", sw(adf.test(diff(trm)))$p.value, "0.017")
for (k in c(5, 11, 12, 13)) { a <- sw(adf.test(lx, k = k))
  f(sprintf("M6 tabla de k · ADF log AP, k = %d", k), a$statistic, c("5" = "-6.422", "11" = "-0.440", "12" = "-1.533", "13" = "-2.147")[as.character(k)])
  if (k > 5) f(sprintf("M6 tabla de k · p, k = %d", k), a$p.value, c("11" = "0.983", "12" = "0.771", "13" = "0.515")[as.character(k)]) }
sa <- seasadj(stl(lx, s.window = "periodic"))
f("M6 · ADF desestacionalizada", sw(adf.test(sa))$statistic, "-2.152")
f("M6 · p ADF desestacionalizada", sw(adf.test(sa))$p.value, "0.513")
f("M6 · KPSS tendencia desestacionalizada", sw(kpss.test(sa, null = "Trend"))$statistic, "0.386")
f("M6 · KPSS tendencia TRM (nuevo)", sw(kpss.test(trm, null = "Trend"))$statistic, "0.273")
f("M6 · KPSS tendencia dTRM (nuevo)", sw(kpss.test(diff(trm), null = "Trend"))$statistic, "0.070")
f("M6 · ADF AP, k = 12 (nuevo)", sw(adf.test(AirPassengers, k = 12))$statistic, "-1.51")
r1 <- function(x) acf(x, 1, plot = FALSE)$acf[2]
pub <- list(lx = c("0.954", "0.200", "-0.293", "-0.534"), trm = c("0.964", "0.088", "-0.415", "-0.602"))
for (nm in c("lx", "trm")) for (dd in 0:3) { x <- if (nm == "lx") lx else trm
  y <- if (dd == 0) x else diff(x, differences = dd)
  f(sprintf("M7 tabla · r1 de %s, d = %d", nm, dd), r1(y), pub[[nm]][dd + 1]) }
cat(sprintf("M7 tabla · var log AP d = 1: %.7f (quiz: 0.0114) · d = 2: %.7f (0.0182) · d = 3: %.7f (0.0469)\n",
            var(diff(lx)), var(diff(lx, differences = 2)), var(diff(lx, differences = 3))))
d12 <- diff(lx, lag = 12); a <- acf(d12, 24, plot = FALSE)$acf[-1]
f("M7 recuadro · KPSS d12", sw(kpss.test(d12))$statistic, "0.368"); f("M7 recuadro · p", sw(kpss.test(d12))$p.value, "0.091")
f("M7 recuadro · r1 d12", a[1], "0.714"); f("M7 recuadro · r2 d12", a[2], "0.623"); f("M7 recuadro · r3 d12", a[3], "0.480")
f("M7 recuadro · r1 de diff(d12)", r1(diff(d12)), "-0.341")
cat(sprintf("M7 recuadro · var(d12) = %.6f · var(diff(d12)) = %.6f\n", var(d12), var(diff(d12))))
y <- USAccDeaths; r <- function(x, k) acf(x, 24, plot = FALSE)$acf[k + 1]
f("ej. 3 · r1 original", r(y, 1), "0.708"); f("ej. 3 · r12 original", r(y, 12), "0.629")
f("ej. 3 · r1 nabla", r(diff(y), 1), "0.023"); f("ej. 3 · r12 nabla", r(diff(y), 12), "0.709")
f("ej. 3 · r1 nabla12", r(diff(y, 12), 1), "0.690"); f("ej. 3 · r12 nabla12", r(diff(y, 12), 12), "-0.077")
f("ej. 3 · r1 nabla12 nabla", r(diff(diff(y), 12), 1), "-0.353"); f("ej. 3 · r12 nabla12 nabla", r(diff(diff(y), 12), 12), "-0.336")
f("ej. 3 · Ljung-Box p", Box.test(diff(diff(y), 12), lag = 24, type = "Ljung-Box")$p.value, "0.033")
s <- diff(diff(co2, 12)); f("ej. 1 · r1 serie final", r1(s), "-0.302"); f("ej. 1 · var serie final", var(s), "0.154")
f("ej. 1 · r1 co2", r(co2, 1), "0.991"); f("ej. 1 · r12 co2", r(co2, 12), "0.928"); f("ej. 1 · banda", 1.96 / sqrt(length(co2)), "0.091")
set.seed(2026); e <- rnorm(200); w <- cumsum(e); aw <- acf(w, 24, plot = FALSE)$acf[-1]
f("M3 · r1 ruido", r1(e), "-0.078"); f("M3 · r1 caminata", aw[1], "0.961"); f("M3 · r12 caminata", aw[12], "0.488")
f("M3 · r12 AP", acf(AirPassengers, 24, plot = FALSE)$acf[13], "0.760"); f("quiz · r12 de d1", acf(diff(lx), 24, plot = FALSE)$acf[13], "0.841")
f("M8 · lambda AP", BoxCox.lambda(AirPassengers, method = "guerrero"), "-0.295"); f("M8 · lambda TRM", BoxCox.lambda(trm, method = "guerrero"), "0.129")
