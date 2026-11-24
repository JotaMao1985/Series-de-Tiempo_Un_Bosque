library(jsonlite)
sin_tildes_rotas <- function(txt, que) {
  if (grepl("<[cdef][0-9a-f]>", txt, perl = TRUE))
    stop("Tildes rotas en ", que, ": ", regmatches(txt, regexpr(".{20}<[cdef][0-9a-f]>.{10}", txt, perl = TRUE)))
  txt
}
Sys.setlocale("LC_CTYPE", "C")
x <- fromJSON('{"a":"Pasajeros mensuales de aerolíneas internacionales"}')
j <- toJSON(x, auto_unbox = TRUE)
cat("en C:", j, "\n")
r <- try(sin_tildes_rotas(j, "prueba"), silent = TRUE); cat("guarda en C aborta:", inherits(r, "try-error"), "\n")
Sys.setlocale("LC_CTYPE", "en_US.UTF-8")
x <- fromJSON('{"a":"Pasajeros mensuales de aerolíneas internacionales"}')
j <- toJSON(x, auto_unbox = TRUE)
cat("en UTF-8:", j, "\n"); r <- try(sin_tildes_rotas(j, "prueba"), silent = TRUE); cat("guarda en UTF-8 aborta:", inherits(r, "try-error"), "\n")
