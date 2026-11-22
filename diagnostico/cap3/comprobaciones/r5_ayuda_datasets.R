# R5 del capitulo 3 · lo que dice la ayuda de R de cada serie que nombran los ejercicios nuevos
# (titulo, Description, Format y Details), para describirlas en los enunciados sin escribir de memoria.
# Rscript diagnostico/cap3/comprobaciones/r5_ayuda_datasets.R > diagnostico/cap3/comprobaciones/r5_ayuda_datasets.out 2>&1
cat(R.version.string, "\n\n")
for (nm in c("WWWusage", "treering", "lynx", "lh", "sunspot.year")) {
  rd <- utils:::.getHelpFile(help(nm, package = "datasets"))
  txt <- capture.output(tools::Rd2txt(rd, options = list(underline_titles = FALSE)))
  j <- grep("^(Source|References|Examples|Note|See Also):", txt)
  cat("=====", nm, "=====\n"); cat(txt[1:(min(j) - 1)], sep = "\n"); cat("\n")
  x <- get(nm); cat("tsp:", tsp(x), "| n:", NROW(x), "| min:", min(x), "| max:", max(x), "\n\n")
}
