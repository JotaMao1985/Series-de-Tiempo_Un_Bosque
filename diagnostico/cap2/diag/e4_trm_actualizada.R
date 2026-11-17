# E4 con la TRM descargada hoy (curl a la URL del capítulo, guardada en
# diagnostico/cap2/diag/trm_descarga/trm.json). Mismo tratamiento que
# descarga_trm() del bloque R del M6, línea 3151, pero leyendo el archivo.
suppressPackageStartupMessages({ library(tseries); library(forecast); library(jsonlite) })
d <- fromJSON("diagnostico/cap2/diag/trm_descarga/trm.json")
d$valor <- as.numeric(d$valor)
d$mes   <- substr(d$vigenciadesde, 1, 7)
cat("Fecha de ejecución:", format(Sys.Date()), " último registro:", max(d$vigenciadesde), "\n")
d <- d[d$mes < format(Sys.Date(), "%Y-%m"), ]
m <- aggregate(valor ~ mes, data = d, FUN = mean); m <- m[order(m$mes), ]
trm <- ts(round(m$valor, 2), start = c(as.integer(substr(m$mes[1], 1, 4)), as.integer(substr(m$mes[1], 6, 7))), frequency = 12)
cat("n =", length(trm), " de", m$mes[1], "a", tail(m$mes, 1), "\n")
# ¿Coinciden los 138 meses del capítulo?
cap <- fromJSON("diagnostico/cap2/diag/datos_cap2.json")$series$trm$valores
cat("máx |diferencia| con los 138 meses del capítulo:", max(abs(as.numeric(trm)[1:138] - cap)), "\n")
for (x in list(list("TRM", trm), list("dTRM", diff(trm)))) {
  a <- suppressWarnings(adf.test(x[[2]])); k <- suppressWarnings(kpss.test(x[[2]]))
  cat(sprintf("%-5s ADF %.4f p %.4f | KPSS %.4f p %s\n", x[[1]], a$statistic, a$p.value, k$statistic, format(k$p.value)))
}
cat("ndiffs(trm) =", ndiffs(trm), "\n")
cat("Últimos meses:\n"); print(tail(m, 6))
