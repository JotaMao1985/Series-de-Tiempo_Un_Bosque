# R5 del capitulo 4 (copia de diagnostico/cap3/comprobaciones/r5_reprex.R) · ejecuta un bloque y escribe cada salida debajo de su linea, tras "#> ".
# Asi el codigo que se pega en el capitulo lleva la salida REAL, no una copiada a mano.
# Uso: Rscript r5_reprex.R r5_bloques/m1.R > r5_bloques/m1.out
# Lee y escribe en UTF-8 sea cual sea el locale de la sesion (sin esto, un «¿» de un comentario
# salia como <U+00BF>; lo vio el verificador B de la R5).
invisible(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"))
args <- commandArgs(TRUE)
f <- args[1]
src <- readLines(f, encoding = "UTF-8")
exprs <- parse(f, keep.source = TRUE, encoding = "UTF-8")
refs <- attr(exprs, "srcref")
options(width = 90, warn = 1)
pdf(NULL)
pos <- 1
for (i in seq_along(exprs)) {
  l1 <- refs[[i]][1]; l2 <- refs[[i]][3]
  if (pos <= l2) writeLines(enc2utf8(src[pos:l2]), useBytes = TRUE)
  out <- capture.output({
    res <- withVisible(eval(exprs[[i]], globalenv()))
    if (res$visible) print(res$value)
  })
  if (length(out)) writeLines(enc2utf8(paste0("#> ", out)), useBytes = TRUE)
  pos <- max(pos, l2 + 1)
}
if (pos <= length(src)) writeLines(enc2utf8(src[pos:length(src)]), useBytes = TRUE)
