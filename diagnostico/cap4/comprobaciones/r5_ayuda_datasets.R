# R5 del capitulo 4 · lo que dice la ayuda de R de cada serie que nombran los ejercicios nuevos y el quiz
# (titulo, Description, Usage, Format y Details), para describirlas sin escribir de memoria.
# Rscript diagnostico/cap4/comprobaciones/r5_ayuda_datasets.R > diagnostico/cap4/comprobaciones/r5_ayuda_datasets.out 2>&1
cat(R.version.string, "\n")
for (p in c("tseries", "tsibbledata", "fpp3", "forecast")) cat(p, as.character(packageVersion(p)), "\n")
cat("\n")
temas <- list(c("tcm", "tseries"), c("NelPlo", "tseries"), c("global_economy", "tsibbledata"), c("gafa_stock", "tsibbledata"),
              c("pelt", "tsibbledata"), c("airmiles", "datasets"), c("BJsales", "datasets"), c("lynx", "datasets"),
              c("beaver1", "datasets"), c("austres", "datasets"), c("uspop", "datasets"), c("aus_airpassengers", "fpp3"))
for (t in temas) {
  rd <- utils:::.getHelpFile(help(t[1], package = (t[2])))
  txt <- capture.output(tools::Rd2txt(rd, options = list(underline_titles = FALSE)))
  j <- grep("^(References|Examples|Note|See Also):", txt)
  cat("=====", t[1], "(", t[2], ") =====\n"); cat(txt[1:(if (length(j)) min(j) - 1 else length(txt))], sep = "\n"); cat("\n")
}
suppressPackageStartupMessages({ library(tseries); library(tsibbledata) })
data(tcm); data(NelPlo)
cat("tcm1y tsp:", tsp(tcm1y), "n:", length(tcm1y), "rango:", range(tcm1y), "\n")
ip <- na.omit(NelPlo[, "ip"]); cat("NelPlo ip tsp:", tsp(ip), "n:", length(ip), "rango:", range(ip), "\n")
col <- subset(as.data.frame(global_economy), Country == "Colombia"); cat("Colombia: anios", range(col$Year), "n:", nrow(col), "Imports rango:", range(col$Imports), "NA:", sum(is.na(col$Imports)), "\n")
g <- subset(as.data.frame(gafa_stock), Symbol == "GOOG" & format(Date, "%Y") == "2018"); cat("GOOG 2018: n", nrow(g), "fechas", format(range(g$Date)), "Close rango", range(g$Close), "\n")
cat("pelt: anios", range(pelt$Year), "n:", nrow(pelt), "Hare rango:", range(pelt$Hare), "\n")
cat("airmiles tsp:", tsp(airmiles), "n:", length(airmiles), "rango:", range(airmiles), "\n")
cat("BJsales.lead tsp:", tsp(BJsales.lead), "n:", length(BJsales.lead), "rango:", range(BJsales.lead), "\n")
cat("lynx tsp:", tsp(lynx), "n:", length(lynx), "\n")
cat("beaver2: n", nrow(beaver2), "dias", unique(beaver2$day), "horas", range(beaver2$time), "primera lectura con activ = 1:", which(beaver2$activ == 1)[1], "temp rango", range(beaver2$temp), "\n")
cat("austres tsp:", tsp(austres), "n:", length(austres), "rango:", range(austres), "\n")
cat("uspop tsp:", tsp(uspop), "n:", length(uspop), "\n")
a <- fpp3::aus_airpassengers; cat("aus_airpassengers: anios", range(a$Year), "n:", nrow(a), "rango:", range(a$Passengers), "\n")
