# Guarda el texto de la ayuda de R de las series que citan las diapositivas del capítulo 5,
# y la entrada del NEWS de forecast sobre la prueba estacional, en docs_cap5.json.
# Uso (desde la raíz del repositorio):
#   Rscript Htmls_Series/diapositivas/fuentes/verificacion/verifica_docs_cap5.R
suppressMessages(library(jsonlite))
aqui <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
ayuda <- function(tema, paquete) {
  rd <- utils:::.getHelpFile(help(tema, package = (paquete)))
  gsub("[[:space:]]+", " ", paste(capture.output(tools::Rd2txt(rd, options = list(underline_titles = FALSE))), collapse = " "))
}
news_md <- readLines(system.file("NEWS.md", package = "forecast"))
cab <- grep("^# forecast ", news_md)
i <- grep("Changed method for choosing D", news_md)
version <- sub("^# forecast ", "", news_md[max(cab[cab < i])])
out <- list(
  entorno = list(R = R.version.string, forecast = as.character(packageVersion("forecast"))),
  airpassengers = ayuda("AirPassengers", "datasets"),
  usaccdeaths = ayuda("USAccDeaths", "datasets"),
  co2 = ayuda("co2", "datasets"),
  nsdiffs_test_por_defecto = eval(formals(forecast::nsdiffs)$test)[1],
  news_cambio_D = list(version = version, texto = trimws(news_md[i]))
)
writeLines(toJSON(out, auto_unbox = TRUE, pretty = TRUE), file.path(aqui, "docs_cap5.json"), useBytes = TRUE)
