# Verificador independiente R5 cap. 3: paginas de ayuda de las series de la practica
for (d in c("WWWusage", "treering", "lynx")) {
  cat("\n=====", d, "=====\n")
  rd <- utils:::.getHelpFile(help(d, package = "datasets"))
  tools::Rd2txt(rd, options = list(underline_titles = FALSE))
  x <- get(d)
  cat("-> length:", length(x), " start:", start(x), " end:", end(x), " frequency:", frequency(x), " min:", min(x), "\n")
}
