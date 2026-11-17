# Verificador independiente · R1 cap. 2 · el trozo nuevo de genera_cap2.R que
# escribe el CSV, aislado y apuntado a una carpeta temporal: ¿da el mismo archivo?
suppressMessages(library(jsonlite))
a <- commandArgs(TRUE); raiz <- a[1]; tmp <- a[2]
sd_json <- fromJSON(file.path(raiz, "precalculo/salidas/datos_series.json"))
trm <- ts(as.numeric(sd_json$trm$valores), start = sd_json$trm$inicio, frequency = sd_json$trm$frecuencia)
meses_trm <- format(seq(as.Date(sprintf("%d-%02d-01", start(trm)[1], start(trm)[2])),
                        by = "month", length.out = length(trm)), "%Y-%m")
archivo_trm <- sprintf("trm_mensual_%s_%s.csv", meses_trm[1], meses_trm[length(meses_trm)])
write.csv(data.frame(mes = meses_trm, trm = as.numeric(trm)), file.path(tmp, archivo_trm), row.names = FALSE, quote = FALSE)
cat("nombre:", archivo_trm, "\n")
cat("identico byte a byte al publicado:",
    identical(readBin(file.path(tmp, archivo_trm), "raw", 1e5),
              readBin(file.path(raiz, "Htmls_Series/datos", archivo_trm), "raw", 1e5)), "\n")
