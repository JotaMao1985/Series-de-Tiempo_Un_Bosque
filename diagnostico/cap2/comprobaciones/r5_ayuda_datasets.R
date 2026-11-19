# R5 del capitulo 2 · lo que dice la ayuda de R de cada serie que nombran los ejercicios
# (Description y Format), para describirlas en los enunciados sin escribir de memoria.
# Rscript diagnostico/cap2/comprobaciones/r5_ayuda_datasets.R > diagnostico/cap2/comprobaciones/r5_ayuda_datasets.out 2>&1
for (nm in c("discoveries", "nhtemp", "LakeHuron", "JohnsonJohnson", "EuStockMarkets", "UKDriverDeaths", "UKgas", "co2", "USAccDeaths")) {
  rd <- utils:::.getHelpFile(help(nm, package = "datasets"))
  txt <- capture.output(tools::Rd2txt(rd, options = list(underline_titles = FALSE)))
  i <- grep("^Description:", txt); j <- grep("^(Source|Details|References|Examples|Note):", txt)
  cat("=====", nm, "=====\n"); cat(txt[1:(min(j[j > i]) - 1)], sep = "\n"); cat("\n")
  x <- get(nm); cat("tsp:", tsp(x), "| n:", NROW(x), "\n\n")
}
