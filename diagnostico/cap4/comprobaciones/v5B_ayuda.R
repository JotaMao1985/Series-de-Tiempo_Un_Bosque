# Verificador B · ayuda de las series del quiz que no son de datasets: aus_airpassengers (fpp3) y global_economy (tsibbledata)
db <- tools::Rd_db("fpp3"); n <- grep("airpass", names(db), value = TRUE); cat("fpp3:", n, "\n")
for (k in n) tools::Rd2txt(db[[k]], options = list(underline_titles = FALSE))
db2 <- tools::Rd_db("tsibbledata"); tools::Rd2txt(db2[["global_economy.Rd"]], options = list(underline_titles = FALSE))
