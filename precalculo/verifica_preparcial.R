# =====================================================================
# verifica_preparcial.R — rehacer en R cada cifra del preparcial · P9
#
#   Series de Tiempo 2026-II (20948) · Corte I · Módulo I
#   Ver PLAN_Preparcial_Corte_I.md, §7 Fase 4 (P9) y §8 criterios 3 y 5.
#
# PARA QUÉ EXISTE
#
# El preparcial no tiene nota, así que toda la cadena de auditoría de
# calificación del Taller 1 sobra. Lo que NO sobra es esto: una cifra mal
# calculada en un instrumento de diagnóstico enseña el error justo antes
# del examen, y lo enseña con la autoridad de venir impresa. Este guion
# rehace las cifras y las contrasta contra lo que la página dice.
#
# LO QUE COMPRUEBA, en siete secciones y una prueba de sí mismo:
#
#   §1  El JSON incrustado en el HTML es el mismo que `salidas/`. Este
#       desfase ya ocurrió una vez y es INVISIBLE: el archivo se lee
#       perfectamente bien y el gráfico del ítem 10 salía vacío.
#   §2  Las diez series: forma, coherencia y las copias que viajan dos
#       veces (i24 y i32 repiten valores que también están en `series`).
#   §3  Las cifras de los 32 ítems, recalculadas desde los valores
#       publicados: ACF, PACF, bandas, ADF, KPSS, STL, medias móviles,
#       índices estacionales, fuerzas, varianzas por orden, Box–Cox.
#   §4  La procedencia de cada cifra IMPRESA EN LA PROSA de los 32
#       ítems. Es la sección que ninguna otra herramienta cubre: el JSON
#       puede estar perfecto y el enunciado citar un 0.898 que no existe.
#   §5  Las siete claves numéricas del bloque B y sus tolerancias: que
#       acepten la respuesta correcta y RECHACEN el error que la propia
#       retroalimentación nombra.
#   §6  La tabla de especificaciones publicada (D13) contra el reparto
#       real de los ítems, y los 18 módulos del Módulo I cubiertos.
#   §7  Casi-duplicados contra los 56 ítems que el estudiante ya vio
#       (R7 y R8), leídos de `salidas/inventario_items.json`.
#   §8  `--inyecta`: siembra cifras falsas y exige que las secciones
#       correspondientes las cacen. Un verificador que nunca ha fallado
#       no es un verificador, es un adorno.
#
# DE DÓNDE SALEN LAS CIFRAS QUE SE RECALCULAN, que es la decisión de
# diseño que manda sobre todo lo demás:
#
#   NO se vuelve a ejecutar `genera_preparcial.R` ni se resimulan las
#   series. Resimular copiaría el generador —y con él sus errores— y
#   además ataría la comprobación a que la semilla siga dando lo mismo.
#   Lo que se hace es lo que hace `verifica_taller1.R`: leer los VALORES
#   PUBLICADOS de cada serie y rehacer desde ahí todo lo derivado. Así
#   una cifra solo pasa si se deduce de los datos que el estudiante tiene
#   delante, que es la única propiedad que importa.
#
#   El precio son las tolerancias. Las series se publican redondeadas a
#   3 o 4 decimales, así que lo recalculado no coincide al bit. La
#   distancia medida es de 1e-5 en las ACF y de 3e-4 en el peor
#   estadístico ADF; las tolerancias están puestas por encima de eso y
#   el guion IMPRIME el margen de cada comprobación en vez de suponerlo.
#   Consecuencia honesta: el último decimal de un estadístico de prueba
#   no es verificable desde los datos publicados. Se dice, no se tapa.
#
# ESTE GUION NO ESCRIBE NADA. Ni en `salidas/`, ni en `Htmls_Series/`.
# Es de solo lectura sobre el material, salvo la copia en `tempdir()`
# que fabrica `--inyecta` para probarse a sí mismo.
#
# CÓMO SE USA, desde la carpeta `Series de tiempo/`:
#
#   LC_ALL=en_US.UTF-8 Rscript precalculo/verifica_preparcial.R
#   LC_ALL=en_US.UTF-8 Rscript precalculo/verifica_preparcial.R --inyecta
#   LC_ALL=en_US.UTF-8 Rscript precalculo/verifica_preparcial.R --margenes
#
# Devuelve 0 si todo cuadra y 1 si algo no. El `LC_ALL` no es adorno:
# sin él R arranca en LC_CTYPE=C, las tildes de la prosa se rompen y la
# §4 empieza a ver cifras donde no las hay.
# =====================================================================

suppressPackageStartupMessages({
  library(jsonlite)
  library(tseries)
  library(forecast)
  library(urca)
})

suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"))
if (!isTRUE(l10n_info()$"UTF-8")) {
  stop("Sin configuración regional UTF-8 la §4 no puede leer la prosa. ",
       "Ejecuta con LC_ALL=en_US.UTF-8 Rscript ...")
}

ARGS      <- commandArgs(TRUE)
INYECTA   <- "--inyecta"  %in% ARGS
MARGENES  <- "--margenes" %in% ARGS
# `--interno` lo pone la propia §8 al reinvocarse sobre una copia
# saboteada. Evita que la prueba del verificador se llame a sí misma.
INTERNO   <- "--interno"  %in% ARGS

SALIDAS <- file.path("precalculo", "salidas")
HTML    <- file.path("Htmls_Series", "preparcial-corte-1.html")
JS      <- file.path(SALIDAS, "preparcial_datos.js")
JSON    <- file.path(SALIDAS, "preparcial_datos.json")
INVENT  <- file.path(SALIDAS, "inventario_items.json")

for (f in c(HTML, JS, JSON, INVENT)) {
  if (!file.exists(f)) stop("No encuentro ", f, ". Ejecuta desde la carpeta `Series de tiempo/`.")
}

# ---------------------------------------------------------------------
# El arnés: cada comprobación deja constancia de su margen
# ---------------------------------------------------------------------

.fallos  <- new.env(parent = emptyenv())
.fallos$lista <- character(0)
.fallos$secciones <- character(0)
.fallos$total <- 0L
.margen  <- new.env(parent = emptyenv())
.margen$filas <- list()
.seccion <- new.env(parent = emptyenv())
.seccion$actual <- "?"

seccion <- function(titulo) {
  .seccion$actual <- sub("^§([0-9]+).*", "\\1", titulo)
  cat("\n", titulo, "\n", rep("", 0), sep = "")
  cat(strrep("-", 70), "\n", sep = "")
}

comprueba <- function(ok, que, detalle = "") {
  ok <- isTRUE(ok)
  .fallos$total <- .fallos$total + 1L
  cat(if (ok) "  OK    " else "  FALLA ", que,
      if (nzchar(detalle)) paste0("   [", detalle, "]") else "", "\n", sep = "")
  if (!ok) {
    .fallos$lista <- c(.fallos$lista, que)
    .fallos$secciones <- c(.fallos$secciones, .seccion$actual)
  }
  invisible(ok)
}

# Igualdad numérica con el margen a la vista. `brecha` es lo que de
# verdad separa a lo recalculado de lo publicado; `tol` es lo que se
# tolera. Si la brecha se acerca a la tolerancia, la comprobación está
# pasando de milagro y hay que saberlo antes de que falle sola.
# `dec` es a cuántos decimales PUBLICA el generador esa cifra. Redondear
# a 3 decimales ya introduce medio ulp —5e-4— antes de que nadie calcule
# nada, así que una tolerancia fija por debajo de eso hace fallar
# comprobaciones correctas. La tolerancia efectiva es `tol` (el ruido de
# recalcular desde datos redondeados) más ese medio ulp, y se imprimen
# las dos: lo que se tolera por aritmética y lo que se tolera por el
# formato de salida son cosas distintas y conviene no confundirlas.
cerca <- function(recalculado, publicado, tol, que, detalle = "", dec = 4) {
  a <- as.numeric(recalculado); b <- as.numeric(publicado)
  if (length(a) != length(b)) {
    return(comprueba(FALSE, que, sprintf("longitudes %d vs %d", length(a), length(b))))
  }
  finito <- is.finite(a) & is.finite(b)
  if (!all(finito) && !any(finito)) return(comprueba(FALSE, que, "todo no finito"))
  brecha <- if (any(finito)) max(abs(a[finito] - b[finito])) else Inf
  # Los NA tienen que estar en las mismas posiciones en los dos lados.
  mismo_hueco <- identical(is.finite(a), is.finite(b))
  # Y un término RELATIVO. Recalcular una varianza de 103 desde valores
  # redondeados a la milésima arrastra un error proporcional a la
  # magnitud, no absoluto: sin esto, las varianzas por tramo pasaban con
  # un margen de 1.2x y habrían empezado a fallar solas.
  tol_ef <- tol + 0.5 * 10^(-dec) + 1e-5 * max(abs(b[finito]), 0)
  .margen$filas[[length(.margen$filas) + 1]] <-
    data.frame(seccion = .seccion$actual, que = que, brecha = brecha, tol = tol_ef,
               stringsAsFactors = FALSE)
  comprueba(brecha <= tol_ef && mismo_hueco, que,
            sprintf("%sbrecha %.3g / tol %.3g (%.3g + medio ulp de %d dec. + 1e-5 relativo)",
                    if (nzchar(detalle)) paste0(detalle, " · ") else "", brecha, tol_ef, tol, dec))
}

# ---------------------------------------------------------------------
# Tolerancias, puestas donde están por lo que se midió, no a ojo
# ---------------------------------------------------------------------
# Medido sobre los valores publicados (redondeados a 3-4 decimales):
#   ACF y PACF ........ 9.4e-05    varianzas y STL ... 3.6e-07
#   estadístico ADF ... 3.3e-04    estadístico KPSS .. 4.7e-05
#   lambda Guerrero ... 5.8e-07    fuerzas F_T / F_S . 2.0e-05
# Cada tolerancia deja al menos un orden de magnitud sobre lo medido y
# sigue por debajo de un error de transcripción, que es >= 1e-3.
TOL_ACF     <- 1e-3    # ACF, PACF, bandas
TOL_PRUEBA  <- 5e-3    # estadísticos de ADF, KPSS y ur.df
TOL_P       <- 2e-3    # p-valores interpolados de `tseries`
TOL_VAR     <- 1e-5    # varianzas, que se publican a 6 decimales
TOL_SERIE   <- 1e-3    # valores de serie contra otra copia de sí mismos
TOL_GENERAL <- 5e-4    # todo lo demás: medias, saltos, índices, fuerzas

# ---------------------------------------------------------------------
# Lectura: el HTML manda, porque es lo que el estudiante tiene delante
# ---------------------------------------------------------------------

texto_html <- function(ruta) paste(readLines(ruta, warn = FALSE, encoding = "UTF-8"), collapse = "\n")

# El bloque incrustado viaja en una sola línea, tal como lo escupe
# `genera_preparcial.R`. Se recorta por los extremos de la asignación en
# vez de por un `regexpr` glotón sobre todo el archivo.
carga_incrustado <- function(txt) {
  lineas <- strsplit(txt, "\n", fixed = TRUE)[[1]]
  i <- grep("^\\s*const PREPARCIAL_DATOS = \\{", lineas)
  if (length(i) != 1L) stop("Esperaba una sola línea `const PREPARCIAL_DATOS = {`, encontré ", length(i))
  cruda <- lineas[i]
  ini <- regexpr("\\{", cruda)
  fin <- max(gregexpr("\\}", cruda)[[1]])
  list(texto = substr(cruda, ini, fin), linea = i)
}

md5_de_texto <- function(s) digest_md5(s)
# `digest` no está entre las dependencias declaradas del proyecto (R15),
# así que el hash se hace con `tools::md5sum` sobre un archivo temporal.
# Es el mismo MD5 que imprime la cadena del §0 del plan.
digest_md5 <- function(s) {
  tmp <- tempfile()
  on.exit(unlink(tmp), add = TRUE)
  con <- file(tmp, open = "wb")
  writeBin(charToRaw(s), con)
  close(con)
  unname(tools::md5sum(tmp))
}

# La §8 apunta aquí cuando reinvoca al guion sobre una copia saboteada.
ruta_html <- Sys.getenv("PREPARCIAL_HTML_INYECTADO", "")
if (!nzchar(ruta_html)) ruta_html <- HTML

TXT <- texto_html(ruta_html)
INC <- carga_incrustado(TXT)
D   <- fromJSON(INC$texto, simplifyVector = TRUE)

cat("=== verifica_preparcial.R ===\n")
cat("HTML     : ", ruta_html, "\n", sep = "")
cat("semilla  : ", D$meta$semilla, "   generado: ", D$meta$generado, "\n", sep = "")
cat("R        : ", R.version.string, "\n", sep = "")

# =====================================================================
seccion("§1 · Anclas del archivo — el JSON incrustado contra `salidas/`")
# =====================================================================
# Este desfase ya ocurrió (P3-P6, «dos defectos que solo aparecieron al
# ejecutar»): P2 incrustó el JSON, después se amplió el precálculo del
# ítem 10, y el gráfico salió vacío sin que nada diera señal. La única
# forma de verlo es comparar los dos, y por eso es la sección 1.

js_txt   <- texto_html(JS)
i_js     <- regexpr("\\{", js_txt)
f_js     <- max(gregexpr("\\}", js_txt)[[1]])
js_carga <- substr(js_txt, i_js, f_js)

md5_inc <- digest_md5(INC$texto)
md5_js  <- digest_md5(js_carga)

comprueba(identical(INC$texto, js_carga),
          "el bloque incrustado en el HTML es byte a byte el de salidas/preparcial_datos.js",
          sprintf("MD5 %s vs %s", substr(md5_inc, 1, 12), substr(md5_js, 1, 12)))

D_json <- fromJSON(JSON, simplifyVector = TRUE)
comprueba(isTRUE(all.equal(D, D_json)),
          "el bloque incrustado parsea igual que salidas/preparcial_datos.json")

comprueba(identical(as.integer(D$meta$semilla), 20260901L),
          "la semilla es 20260901 (la fecha del parcial)", as.character(D$meta$semilla))
comprueba(identical(as.integer(D$meta$n_items), 32L),
          "meta declara 32 ítems", as.character(D$meta$n_items))
comprueba(length(D$items) == 32L,
          "y hay 32 entradas de ítem", as.character(length(D$items)))
comprueba(identical(sort(names(D$items)), sprintf("i%02d", 1:32)),
          "los identificadores van de i01 a i32 sin huecos")
# Diez del blueprint y cuatro del bloque E. Se cuentan por separado a
# propósito: las del bloque E son los únicos datos BIVARIADOS del preparcial
# —los dos pares de §2.6 de FPP3— y no alimentan ningún ítem de los 32, así
# que mezclarlas en la cuenta escondería si alguna de las diez desapareciera.
SERIES_E <- c("temperatura", "demanda_electrica", "ventas_norte", "ventas_sur")
comprueba(length(setdiff(names(D$series), SERIES_E)) == 10L,
          "hay 10 series propias del blueprint",
          paste(setdiff(names(D$series), SERIES_E), collapse = ", "))
comprueba(all(SERIES_E %in% names(D$series)),
          "y las cuatro del bloque E, que son los dos pares de la dispersión",
          paste(SERIES_E, collapse = ", "))
comprueba(!any(grepl("AirPassengers", names(D$series))) &&
            !grepl("AirPassengers", INC$texto, fixed = TRUE),
          "ninguna serie es AirPassengers (D14)")

# =====================================================================
seccion("§2 · Las diez series — forma, coherencia y las copias dobles")
# =====================================================================

serie_ts <- function(nombre) {
  s <- D$series[[nombre]]
  ts(as.numeric(s$valores), start = as.numeric(s$inicio), frequency = as.numeric(s$frecuencia))
}

ESPERADO <- list(
  demanda         = list(n = 120, f = 12), demanda_atipico = list(n = 120, f = 12),
  ocupacion       = list(n =  48, f =  4), residuo_blanco  = list(n = 200, f =  1),
  caudal          = list(n = 200, f =  1), indice          = list(n = 200, f =  1),
  linea           = list(n = 200, f =  1), saldo           = list(n =  80, f =  1),
  potencia        = list(n = 200, f =  1), frontera        = list(n = 120, f =  1))

for (nm in names(ESPERADO)) {
  s <- D$series[[nm]]
  ok <- !is.null(s) &&
    length(s$valores) == ESPERADO[[nm]]$n &&
    as.integer(s$n) == ESPERADO[[nm]]$n &&
    as.integer(s$frecuencia) == ESPERADO[[nm]]$f &&
    all(is.finite(as.numeric(s$valores)))
  comprueba(ok, sprintf("serie `%s`: n = %d, frecuencia = %d, sin valores no finitos",
                        nm, ESPERADO[[nm]]$n, ESPERADO[[nm]]$f),
            if (is.null(s)) "no existe" else sprintf("n = %d", length(s$valores)))
}

demanda   <- serie_ts("demanda")
dem_atip  <- serie_ts("demanda_atipico")
ocupacion <- serie_ts("ocupacion")
blanco    <- serie_ts("residuo_blanco")
caudal    <- serie_ts("caudal")
indice    <- serie_ts("indice")
linea     <- serie_ts("linea")
saldo     <- serie_ts("saldo")
potencia  <- serie_ts("potencia")
frontera  <- serie_ts("frontera")

I <- D$items

# `demanda_atipico` tiene que ser `demanda` con UN valor tocado, y ese
# valor un 55 % por encima: es lo que afirma el enunciado del ítem 5.
distintos <- which(abs(as.numeric(dem_atip) - as.numeric(demanda)) > 1e-9)
comprueba(length(distintos) == 1L && distintos == I$i05$posicion_atipico,
          "`demanda_atipico` difiere de `demanda` en una sola posición, la 63",
          paste(distintos, collapse = ", "))
razon <- as.numeric(dem_atip)[I$i05$posicion_atipico] / as.numeric(demanda)[I$i05$posicion_atipico]
cerca(razon, 1.55, 1e-3, "y ese valor está un 55 % por encima del original",
      sprintf("razón %.4f", razon))

# Las copias dobles: i24 y i32 repiten valores que ya viajan en `series`,
# con distinto redondeo. Que se separen es un desfase como el de §1.
cerca(as.numeric(I$i24$valores), as.numeric(D$series$potencia$valores), TOL_SERIE,
      "i24$valores es la serie `potencia` (dos redondeos del mismo dato)", dec = 3)
cerca(as.numeric(I$i32$valores), as.numeric(D$series$saldo$valores), TOL_SERIE,
      "i32$valores es la serie `saldo`", dec = 3)
cerca(as.numeric(I$i01$valores_barajados)[order(as.numeric(I$i01$valores_barajados))],
      as.numeric(D$series$demanda$valores)[order(as.numeric(D$series$demanda$valores))],
      TOL_SERIE, "i01$valores_barajados es `demanda` reordenada: mismo multiconjunto", dec = 3)

# =====================================================================
seccion("§3 · Las cifras de los 32 ítems, rehechas desde los valores publicados")
# =====================================================================

# La ACF muestral, escrita desde su definición y no llamando a `acf()`.
# Es la cantidad que más veces aparece en el instrumento —siete gráficos
# y una docena de enunciados viven de ella— así que se calcula aquí a
# mano y se contrasta con `acf()` antes de usarla. Si las dos coinciden,
# lo publicado se está comparando contra la definición, no contra la
# misma función que lo produjo.
acf_manual <- function(x, h_max) {
  y <- as.numeric(x); n <- length(y); m <- mean(y)
  den <- sum((y - m)^2)
  vapply(seq_len(h_max), function(h) sum((y[1:(n - h)] - m) * (y[(1 + h):n] - m)) / den, 0)
}
acf_r  <- function(x, h) as.numeric(acf(as.numeric(x), lag.max = h, plot = FALSE)$acf)[-1]
pacf_r <- function(x, h) as.numeric(pacf(as.numeric(x), lag.max = h, plot = FALSE)$acf)
banda  <- function(n) 1.96 / sqrt(n)

cerca(acf_manual(demanda, 24), acf_r(demanda, 24), 1e-12,
      "la ACF escrita a mano coincide con acf() de R (anclaje de la definición)")

adf_de  <- function(x) suppressWarnings(adf.test(as.numeric(x)))
kpss_de <- function(x, tipo) suppressWarnings(kpss.test(as.numeric(x), null = tipo))

# Una prueba publicada = estadístico + p-valor + parámetro + bandera de
# borde de tabla. Las cuatro cosas se comprueban juntas: el `fuera_tabla`
# es lo que hace que la página escriba `p < 0.01` en vez de `p = 0.01`.
prueba_adf <- function(x, pub, que) {
  r <- adf_de(x)
  cerca(r$statistic, pub$estadistico, TOL_PRUEBA, paste(que, "· estadístico ADF"))
  cerca(r$p.value,   pub$p_valor,     TOL_P,      paste(que, "· p-valor ADF"))
  comprueba(as.integer(r$parameter) == as.integer(pub$rezagos),
            paste(que, "· rezagos del ADF"), sprintf("%d vs %d", as.integer(r$parameter), pub$rezagos))
  comprueba(isTRUE(pub$fuera_tabla) == (r$p.value %in% c(0.01, 0.99)),
            paste(que, "· bandera fuera_tabla del ADF"))
}
prueba_kpss <- function(x, tipo, pub, que) {
  r <- kpss_de(x, tipo)
  cerca(r$statistic, pub$estadistico, TOL_PRUEBA, paste(que, "· estadístico KPSS"))
  cerca(r$p.value,   pub$p_valor,     TOL_P,      paste(que, "· p-valor KPSS"))
  comprueba(as.integer(r$parameter) == as.integer(pub$truncamiento),
            paste(que, "· truncamiento del KPSS"))
  comprueba(isTRUE(pub$fuera_tabla) == (r$p.value %in% c(0.01, 0.1)),
            paste(que, "· bandera fuera_tabla del KPSS"))
}

stl_de <- function(x, sw = "periodic", robusto = FALSE)
  stl(x, s.window = sw, robust = robusto)$time.series

tramos <- function(x, k = 3) split(as.numeric(x), cut(seq_along(as.numeric(x)), k, labels = FALSE))

cat("\n-- i01 [1.1 · G] la serie y sus valores barajados\n")
barajada <- ts(as.numeric(I$i01$valores_barajados), start = c(2016, 1), frequency = 12)
cerca(acf_manual(demanda, 24), I$i01$acf_original$acf,  TOL_ACF, "i01 · ACF de demanda a 24 rezagos")
cerca(pacf_r(demanda, 24),     I$i01$acf_original$pacf, TOL_ACF, "i01 · PACF de demanda")
cerca(banda(120),              I$i01$acf_original$banda, TOL_ACF, "i01 · banda de demanda")
cerca(acf_manual(barajada, 24), I$i01$acf_barajada$acf,  TOL_ACF, "i01 · ACF de la barajada")
cerca(pacf_r(barajada, 24),     I$i01$acf_barajada$pacf, TOL_ACF, "i01 · PACF de la barajada")
cerca(mean(demanda) - mean(barajada), 0, TOL_SERIE, "i01 · barajar no mueve la media")
cerca(sd(demanda)   - sd(barajada),   0, TOL_SERIE, "i01 · barajar no mueve la desviación típica")
comprueba(I$i01$media_igual == 0 && I$i01$sd_igual == 0,
          "i01 · y así está publicado: media_igual y sd_igual valen 0")

cat("\n-- i02 [1.1 · 1.9 · C] sin cifras propias\n")
comprueba(isTRUE(I$i02$sin_cifras), "i02 · declarado `sin_cifras`: es conceptual puro")

cat("\n-- i03 [1.2 · P] aritmética del objeto ts\n")
demo <- ts(rep(0, I$i03$n), start = as.numeric(I$i03$inicio), frequency = I$i03$frecuencia)
comprueba(identical(as.numeric(end(demo)), as.numeric(I$i03$ultimo)),
          "i03 · la última observación cae en 2021-12",
          sprintf("%d-%02d", end(demo)[1], end(demo)[2]))
comprueba(identical(I$i03$ultimo_texto, sprintf("%d-%02d", end(demo)[1], end(demo)[2])),
          "i03 · y el texto de la fecha coincide")

cat("\n-- i04 [1.3 · G] gg_subseries: medias y pendientes por mes\n")
mes <- cycle(demanda)
medias_mes <- as.numeric(tapply(as.numeric(demanda), mes, mean))
cerca(medias_mes, I$i04$medias_por_mes, TOL_GENERAL, "i04 · medias por mes", dec = 3)
comprueba(which.max(medias_mes) == I$i04$mes_mas_alto, "i04 · el mes más alto es julio")
comprueba(which.min(medias_mes) == I$i04$mes_mas_bajo, "i04 · el mes más bajo es febrero")
pend <- vapply(1:12, function(m) {
  y <- as.numeric(demanda)[mes == m]; unname(coef(lm(y ~ seq_along(y)))[2]) }, 0)
cerca(pend, I$i04$pendiente_por_mes, TOL_GENERAL, "i04 · pendiente dentro de cada mes")
comprueba(all(pend > 0), "i04 · los doce meses suben, que es lo que el ítem afirma")

cat("\n-- i05 [1.4 · C] qué componente absorbe el atípico\n")
st_lim <- stl_de(log(demanda)); st_at <- stl_de(log(dem_atip))
pos <- I$i05$posicion_atipico
cerca(st_at[pos, "remainder"] - st_lim[pos, "remainder"], I$i05$salto_en_residuo,   TOL_GENERAL, "i05 · salto en el residuo")
cerca(st_at[pos, "trend"]     - st_lim[pos, "trend"],     I$i05$salto_en_tendencia, TOL_GENERAL, "i05 · salto en la tendencia")
cerca(st_at[pos, "seasonal"]  - st_lim[pos, "seasonal"],  I$i05$salto_en_estacional, TOL_GENERAL, "i05 · salto en el estacional")
cerca(sd(st_lim[, "remainder"]), I$i05$sd_residuo_limpia,  TOL_GENERAL, "i05 · sd del residuo sin atípico")
cerca(sd(st_at[,  "remainder"]), I$i05$sd_residuo_atipico, TOL_GENERAL, "i05 · sd del residuo con atípico")

cat("\n-- i06 y i07 [1.5 · P, I] medias móviles\n")
ma_2x4 <- function(y) as.numeric(stats::filter(stats::filter(y, rep(1/4, 4), sides = 2), c(.5, .5), sides = 1))
cinco <- round(as.numeric(ocupacion)[1:5], 2)
cerca(cinco, I$i06$observaciones, 1e-9, "i06 · las cinco observaciones son las de `ocupacion`")
cerca(sum(c(0.125, 0.25, 0.25, 0.25, 0.125) * cinco), I$i06$respuesta, TOL_GENERAL,
      "i06 · el primer valor de la 2x4, con los pesos (1/8,1/4,1/4,1/4,1/8)", dec = 3)
centrada    <- ma_2x4(as.numeric(ocupacion))
sin_centrar <- as.numeric(stats::filter(as.numeric(ocupacion), rep(1/4, 4), sides = 1))
cerca(centrada[3], I$i06$comprobacion, TOL_GENERAL, "i06 · y coincide con la MA que calcula R", dec = 3)
cerca(centrada,    suppressWarnings(as.numeric(I$i07$centrada)),    TOL_GENERAL, "i07 · la 2x4 centrada entera", dec = 3)
cerca(sin_centrar, suppressWarnings(as.numeric(I$i07$sin_centrar)), TOL_GENERAL, "i07 · la MA(4) sin centrar entera", dec = 3)
comprueba(sum(is.na(centrada[1:6])) == I$i07$no_estimados_inicio &&
            sum(is.na(tail(centrada, 6))) == I$i07$no_estimados_final,
          "i07 · dos valores no estimados a cada lado")
comprueba(I$i07$desfase_periodos == 0.5,
          "i07 · el desfase declarado es medio periodo (definición de la MA de un solo lado)")

cat("\n-- i08 [1.6 · P] índices estacionales clásicos\n")
dc <- decompose(ocupacion, type = "additive")
detrend <- as.numeric(ocupacion) - as.numeric(dc$trend)
prom <- as.numeric(tapply(detrend, cycle(ocupacion), mean, na.rm = TRUE))
cerca(prom, I$i08$promedios_sin_tendencia, TOL_GENERAL, "i08 · promedios por trimestre sin tendencia")
cerca(mean(prom), I$i08$media_de_promedios, TOL_GENERAL, "i08 · la media de los cuatro promedios")
cerca(prom - mean(prom), I$i08$indices, TOL_GENERAL, "i08 · los índices centrados")
cerca(sum(prom - mean(prom)), 0, 1e-9, "i08 · y suman cero, que es lo que el centrado busca")
cerca(as.numeric(dc$figure), I$i08$indices_de_R, TOL_GENERAL, "i08 · coinciden con decompose()$figure")

cat("\n-- i09 [1.7 · I] la malla de s.window\n")
malla <- I$i09$malla
for (k in seq_len(nrow(malla))) {
  sw  <- malla$s_window[k]
  swv <- if (sw == "periodic") "periodic" else as.numeric(sw)
  dd  <- stl_de(log(demanda), sw = swv)
  a12 <- acf_manual(dd[, "remainder"], 12)[12]
  cerca(var(dd[, "seasonal"]),  malla$var_estacional[k], TOL_VAR, sprintf("i09 · s.window=%s · varianza del estacional", sw), dec = 6)
  cerca(var(dd[, "remainder"]), malla$var_residuo[k],    TOL_VAR, sprintf("i09 · s.window=%s · varianza del residuo", sw), dec = 6)
  cerca(a12, malla$acf_residuo_12[k], TOL_ACF, sprintf("i09 · s.window=%s · ACF del residuo en el rezago 12", sw))
  comprueba(isTRUE(malla$queda_estacionalidad[k]) == (abs(a12) > banda(120)),
            sprintf("i09 · s.window=%s · el veredicto «queda estacionalidad» sale de la banda", sw))
}
comprueba(isTRUE(malla$queda_estacionalidad[1]) && !any(unlist(malla$queda_estacionalidad[-1])),
          "i09 · solo la ventana PEQUEÑA deja el residuo fuera de banda (es sobreajuste, no infraajuste)")

cat("\n-- i10 [1.7 · G] STL robusto frente a no robusto\n")
rob <- stl_de(log(dem_atip), robusto = TRUE)
nor <- stl_de(log(dem_atip), robusto = FALSE)
cerca(rob[pos, "remainder"], I$i10$robusto$residuo_en_atipico,    TOL_GENERAL, "i10 · residuo en el atípico (robusto)")
cerca(nor[pos, "remainder"], I$i10$no_robusto$residuo_en_atipico, TOL_GENERAL, "i10 · residuo en el atípico (no robusto)")
cerca(var(rob[, "seasonal"]), I$i10$robusto$var_estacional,    TOL_VAR, "i10 · varianza del estacional (robusto)", dec = 6)
cerca(var(nor[, "seasonal"]), I$i10$no_robusto$var_estacional, TOL_VAR, "i10 · varianza del estacional (no robusto)", dec = 6)
cerca(rob[pos, "seasonal"], I$i10$estacional_del_mes$robusto,    TOL_GENERAL, "i10 · estacional de marzo (robusto)")
cerca(nor[pos, "seasonal"], I$i10$estacional_del_mes$no_robusto, TOL_GENERAL, "i10 · estacional de marzo (no robusto)")
cerca(as.numeric(tapply(rob[, "seasonal"], mes, mean)), I$i10$ciclo_robusto,    TOL_GENERAL, "i10 · ciclo estacional robusto (12 meses)")
cerca(as.numeric(tapply(nor[, "seasonal"], mes, mean)), I$i10$ciclo_no_robusto, TOL_GENERAL, "i10 · ciclo estacional no robusto")
cerca(rob[(pos - 6):(pos + 6), "remainder"], I$i10$residuo_robusto,    TOL_GENERAL, "i10 · residuo alrededor del atípico (robusto)")
cerca(nor[(pos - 6):(pos + 6), "remainder"], I$i10$residuo_no_robusto, TOL_GENERAL, "i10 · residuo alrededor del atípico (no robusto)")
comprueba(as.integer(cycle(demanda)[pos]) == I$i10$mes_atipico, "i10 · el atípico cae en marzo")

cat("\n-- i11 [1.8 · I] F_T parecida, F_S muy distinta\n")
fuerzas <- function(x) {
  dd <- stl_de(x)
  c(FT = max(0, 1 - var(dd[, "remainder"]) / var(dd[, "trend"] + dd[, "remainder"])),
    FS = max(0, 1 - var(dd[, "remainder"]) / var(dd[, "seasonal"] + dd[, "remainder"])))
}
s1 <- ts(as.numeric(I$i11$serie_1$valores), start = c(2016, 1), frequency = 12)
s2 <- ts(as.numeric(I$i11$serie_2$valores), start = c(2016, 1), frequency = 12)
f1 <- fuerzas(s1); f2 <- fuerzas(s2)
cerca(f1, c(I$i11$serie_1$FT, I$i11$serie_1$FS), TOL_GENERAL, "i11 · F_T y F_S de la serie 1")
cerca(f2, c(I$i11$serie_2$FT, I$i11$serie_2$FS), TOL_GENERAL, "i11 · F_T y F_S de la serie 2")
cerca(abs(f1[1] - f2[1]), I$i11$diferencia_FT, TOL_GENERAL, "i11 · diferencia en F_T")
cerca(abs(f1[2] - f2[2]), I$i11$diferencia_FS, TOL_GENERAL, "i11 · diferencia en F_S")
comprueba(abs(f1[1] - f2[1]) < 0.03 && abs(f1[2] - f2[2]) > 0.5,
          "i11 · el par cumple lo que el ítem promete: F_T casi igual, F_S muy distinta",
          sprintf("dF_T = %.4f · dF_S = %.4f", abs(f1[1] - f2[1]), abs(f1[2] - f2[2])))

cat("\n-- i12 y i13 [2.1 · C] las tres condiciones de la estacionariedad débil\n")
por_tramo <- function(x, f) as.numeric(vapply(tramos(x), f, 0))
for (par in list(list("con_tendencia", linea), list("caminata", indice),
                 list("estacional", demanda), list("blanco", blanco))) {
  nm <- par[[1]]; x <- par[[2]]
  cerca(por_tramo(x, mean), I$i12[[nm]]$medias,    TOL_GENERAL, sprintf("i12 · %s · medias por tramo", nm),    dec = 3)
  cerca(por_tramo(x, var),  I$i12[[nm]]$varianzas, TOL_GENERAL, sprintf("i12 · %s · varianzas por tramo", nm), dec = 3)
}
comprueba(diff(range(I$i12$con_tendencia$medias))    > 15 &&
            diff(range(I$i12$con_tendencia$varianzas)) < 10,
          "i12 · `linea` mueve la media y deja quieta la varianza: viola SOLO la condición (1)")
comprueba(all(diff(I$i12$caminata$varianzas) > 0),
          "i12 · la varianza de la caminata crece tramo a tramo")
cerca(por_tramo(indice, function(z) cov(z[-length(z)], z[-1])),
      I$i13$autocov_rezago1_por_tramo, TOL_GENERAL, "i13 · autocovarianza al rezago 1 por tramo", dec = 3)
comprueba(all(diff(I$i13$autocov_rezago1_por_tramo) > 0),
          "i13 · y crece con t: es la tercera condición, la que no se ve en media ni varianza")

cat("\n-- i14 y i15 [2.2 · P, G] ruido blanco frente a dependencia débil\n")
a_bl <- acf_manual(blanco, 36)
cerca(a_bl, I$i14$acf, TOL_ACF, "i14 · ACF de residuo_blanco a 36 rezagos")
cerca(banda(200), I$i14$banda, TOL_ACF, "i14 · banda con n = 200")
comprueba(sum(abs(a_bl) > banda(200)) == I$i14$observadas_fuera,
          "i14 · barras observadas fuera de banda", sprintf("%d", sum(abs(a_bl) > banda(200))))
comprueba(identical(as.integer(which(abs(a_bl) > banda(200))), as.integer(I$i14$rezagos_fuera)),
          "i14 · y están en los rezagos publicados", paste(which(abs(a_bl) > banda(200)), collapse = ", "))
cerca(0.05 * 36, I$i14$esperadas_fuera, 1e-9, "i14 · esperadas fuera = 5 % de 36 rezagos", dec = 2)
comprueba(I$i14$observadas_fuera <= I$i14$esperadas_fuera + 1,
          "i14 · lo observado es compatible con lo esperado: la serie se comporta como ruido blanco")
cerca(acf_manual(blanco, 36), I$i15$blanco$acf,   TOL_ACF, "i15 · ACF del ruido blanco")
cerca(pacf_r(blanco, 36),     I$i15$blanco$pacf,  TOL_ACF, "i15 · PACF del ruido blanco")
cerca(acf_manual(caudal, 36), I$i15$ar_debil$acf, TOL_ACF, "i15 · ACF del AR(1) débil")
cerca(pacf_r(caudal, 36),     I$i15$ar_debil$pacf, TOL_ACF, "i15 · PACF del AR(1) débil")
cerca(pacf_r(blanco, 36)[1], I$i15$pacf1_blanco, TOL_ACF, "i15 · primer rezago de la PACF del blanco")
cerca(pacf_r(caudal, 36)[1], I$i15$pacf1_ar,     TOL_ACF, "i15 · primer rezago de la PACF del AR(1)")
comprueba(abs(I$i15$pacf1_blanco) < banda(200) && abs(I$i15$pacf1_ar) > banda(200),
          "i15 · el contraste que el ítem pide existe: uno dentro de banda y el otro fuera")

cat("\n-- i16 [2.5 · I] la varianza de la caminata\n")
cerca(por_tramo(indice, var), I$i16$varianza_por_tramo, TOL_GENERAL, "i16 · varianza por tramo de la caminata", dec = 3)
prueba_adf(indice, I$i16$adf, "i16 · caminata")
prueba_kpss(indice, "Level", I$i16$kpss_nivel, "i16 · caminata en nivel")
cerca(acf_manual(indice, 6), I$i16$acf, TOL_ACF, "i16 · los seis primeros rezagos de la ACF")
prueba_adf(diff(indice), I$i16$adf_diferenciada, "i16 · caminata diferenciada")
comprueba(I$i16$adf$p_valor > 0.05 && I$i16$adf_diferenciada$p_valor < 0.05,
          "i16 · el ADF no rechaza en nivel y sí tras diferenciar, que es lo que el ítem predice")

cat("\n-- i17 [2.3 · P] r_1 a mano sobre seis observaciones\n")
seis <- as.numeric(I$i17$observaciones)
m6 <- mean(seis)
num6 <- sum((seis[-6] - m6) * (seis[-1] - m6)); den6 <- sum((seis - m6)^2)
cerca(m6,          I$i17$media,         TOL_GENERAL, "i17 · la media de las seis")
cerca(num6,        I$i17$numerador,     TOL_GENERAL, "i17 · el numerador: cinco productos cruzados")
cerca(den6,        I$i17$denominador,   TOL_GENERAL, "i17 · el denominador: los SEIS cuadrados")
cerca(num6 / den6, I$i17$respuesta,     TOL_GENERAL, "i17 · r_1")
cerca(acf_r(seis, 1)[1], I$i17$comprobacion_R, TOL_GENERAL, "i17 · y coincide con acf() de R")

cat("\n-- i18 [2.3 · I] la ACF lenta que NO prueba raíz unitaria\n")
cerca(acf_manual(linea, 10),  I$i18$acf_linea,    TOL_ACF, "i18 · ACF de `linea` (tendencia determinista)")
cerca(acf_manual(indice, 10), I$i18$acf_caminata, TOL_ACF, "i18 · ACF de `indice` (caminata)")
prueba_adf(linea, I$i18$linea_adf, "i18 · linea")
prueba_kpss(linea, "Level", I$i18$linea_kpss_nivel,     "i18 · linea en nivel")
prueba_kpss(linea, "Trend", I$i18$linea_kpss_tendencia, "i18 · linea en tendencia")
prueba_adf(indice, I$i18$caminata_adf, "i18 · caminata")
prueba_kpss(indice, "Trend", I$i18$caminata_kpss_tendencia, "i18 · caminata en tendencia")
comprueba(all(I$i18$acf_linea[1:5] > 0.8) && I$i18$linea_adf$p_valor < 0.05,
          "i18 · el contraejemplo se sostiene: ACF que decae despacio y ADF que SÍ rechaza")

cat("\n-- i19 [2.3 · G] leer el periodo en el correlograma\n")
d_log <- diff(log(demanda))
a19 <- acf_manual(d_log, 36)
cerca(a19, I$i19$acf, TOL_ACF, "i19 · ACF de la demanda log-diferenciada")
cerca(banda(119), I$i19$banda, TOL_ACF, "i19 · banda con n = 119")
comprueba(identical(as.integer(which(abs(a19) > banda(119))), as.integer(I$i19$picos)),
          "i19 · los picos fuera de banda", paste(which(abs(a19) > banda(119)), collapse = ", "))
comprueba(all(diff(I$i19$picos) == I$i19$periodo / 2) || all(I$i19$picos %% 6 == 0),
          "i19 · los picos caen en múltiplos de 6, y el periodo declarado es 12",
          paste(I$i19$picos, collapse = ", "))

cat("\n-- i20 y i21 [2.4 · P, I] la autocorrelación parcial\n")
a_oc <- acf_manual(ocupacion, 2)
cerca(a_oc[1], I$i20$r1, TOL_ACF, "i20 · r_1 de `ocupacion`")
cerca(a_oc[2], I$i20$r2, TOL_ACF, "i20 · r_2 de `ocupacion`")
phi22 <- (I$i20$r2 - I$i20$r1^2) / (1 - I$i20$r1^2)
cerca(phi22, I$i20$respuesta, TOL_GENERAL, "i20 · phi_22 por la fórmula de Durbin-Levinson")
cerca(pacf_r(ocupacion, 2)[2], I$i20$comprobacion_R, TOL_ACF, "i20 · y coincide con pacf() de R")
for (nm in names(I$i21$comprobado_en)) {
  x <- get(if (nm == "indice") "indice" else nm)
  pub <- I$i21$comprobado_en[[nm]]
  cerca(acf_manual(x, 2)[1], pub$r1,    TOL_ACF, sprintf("i21 · %s · r_1", nm))
  cerca(pacf_r(x, 2)[1],     pub$phi11, TOL_ACF, sprintf("i21 · %s · phi_11", nm))
  comprueba(pub$diferencia == 0 && abs(acf_manual(x, 2)[1] - pacf_r(x, 2)[1]) < 1e-9,
            sprintf("i21 · %s · phi_11 = r_1 exactamente, que es lo que el ítem afirma", nm))
}

cat("\n-- i22 [2.3 · 1.3 · G] el gráfico de rezagos\n")
y_oc <- as.numeric(ocupacion)
cerca(head(y_oc, -4), I$i22$pares_rezago4$x, TOL_SERIE, "i22 · eje x del gráfico contra y_{t-4}", dec = 3)
cerca(tail(y_oc, -4), I$i22$pares_rezago4$y, TOL_SERIE, "i22 · eje y del gráfico contra y_{t-4}", dec = 3)
cerca(head(y_oc, -1), I$i22$pares_rezago1$x, TOL_SERIE, "i22 · eje x del gráfico contra y_{t-1}", dec = 3)
cerca(tail(y_oc, -1), I$i22$pares_rezago1$y, TOL_SERIE, "i22 · eje y del gráfico contra y_{t-1}", dec = 3)
cerca(acf_manual(ocupacion, 4)[4], I$i22$r4, TOL_ACF, "i22 · r_4, la autocorrelación que la nube enseña")
cerca(acf_manual(ocupacion, 4)[1], I$i22$r1, TOL_ACF, "i22 · r_1, para el contraste")
comprueba(identical(as.integer(cycle(ocupacion))[-(1:4)], as.integer(I$i22$trimestre)),
          "i22 · el trimestre que colorea cada punto")
comprueba(I$i22$r4 > 0.8 && abs(I$i22$r1) < 0.3,
          "i22 · la nube a rezago 4 está alineada y la de rezago 1 no: el contraste existe")

cat("\n-- i23 [2.6 · C] qué caza el KPSS que el ADF deja pasar\n")
prueba_adf(linea, I$i23$linea$adf, "i23 · linea")
prueba_kpss(linea, "Level", I$i23$linea$kpss_nivel,     "i23 · linea en nivel")
prueba_kpss(linea, "Trend", I$i23$linea$kpss_tendencia, "i23 · linea en tendencia")
prueba_adf(caudal, I$i23$caudal$adf, "i23 · caudal")
prueba_kpss(caudal, "Level", I$i23$caudal$kpss_nivel, "i23 · caudal en nivel")
comprueba(I$i23$linea$adf$p_valor < 0.05 && I$i23$linea$kpss_nivel$p_valor <= 0.05 &&
            I$i23$linea$kpss_tendencia$p_valor > 0.05,
          "i23 · el caso que justifica usar las dos: ADF rechaza, KPSS de NIVEL rechaza, KPSS de tendencia no")

cat("\n-- i24 [2.6 · I] la potencia del ADF\n")
prueba_adf(potencia[1:40], I$i24$corto$adf,  "i24 · n = 40")
prueba_kpss(potencia[1:40], "Level", I$i24$corto$kpss, "i24 · n = 40")
prueba_adf(potencia, I$i24$largo$adf, "i24 · n = 200")
prueba_kpss(potencia, "Level", I$i24$largo$kpss, "i24 · n = 200")
comprueba(I$i24$corto$adf$p_valor > 0.10 && I$i24$largo$adf$p_valor < 0.05,
          "i24 · la conclusión del ADF CAMBIA con n, que es el ítem entero",
          sprintf("p = %.4f con 40 · p = %.4f con 200", I$i24$corto$adf$p_valor, I$i24$largo$adf$p_valor))
comprueba(I$i24$corto$n == 40 && I$i24$largo$n == 200, "i24 · los dos tamaños declarados")

cat("\n-- i25 [2.6 · P] los dos truncamientos que se contradicen\n")
trunc_urca <- function(n) floor(3 * sqrt(n) / 13)
trunc_kpss <- function(n) floor(4 * (n / 100)^0.25)
comprueba(trunc_urca(120) == I$i25$truncamiento_urca,       "i25 · truncamiento de urca::ur.kpss con n = 120 es 2")
comprueba(trunc_kpss(120) == I$i25$truncamiento_kpss_test,  "i25 · truncamiento de tseries::kpss.test con n = 120 es 4")
comprueba(as.integer(suppressWarnings(ndiffs(frontera))) == as.integer(I$i25$ndiffs),
          "i25 · ndiffs(frontera) = 1")
prueba_kpss(frontera, "Level", I$i25$kpss_test_nivel, "i25 · frontera en nivel")
prueba_adf(frontera, I$i25$adf, "i25 · frontera")
kt <- kpss_de(frontera, "Level")
comprueba(((as.integer(ndiffs(frontera)) > 0) != (kt$p.value < 0.05)) == isTRUE(I$i25$se_contradicen),
          "i25 · y de verdad se contradicen: ndiffs dice «diferencia», kpss.test dice «no»")
tabla25 <- I$i25$tabla
for (k in seq_len(nrow(tabla25))) {
  n <- tabla25$n[k]
  comprueba(trunc_urca(n) == tabla25$urca[k] && trunc_kpss(n) == tabla25$kpss_test[k],
            sprintf("i25 · tabla de truncamientos con n = %d", n),
            sprintf("urca %d · kpss.test %d", trunc_urca(n), trunc_kpss(n)))
}

cat("\n-- i26 [2.6 · I] ur.df con deriva y con tendencia\n")
rez26 <- trunc((length(linea) - 1)^(1/3))
df_d <- ur.df(as.numeric(linea), type = "drift", lags = rez26)
df_t <- ur.df(as.numeric(linea), type = "trend", lags = rez26)
cerca(df_d@teststat[1], I$i26$drift$estadistico, TOL_PRUEBA, "i26 · estadístico con `drift`")
cerca(df_t@teststat[1], I$i26$trend$estadistico, TOL_PRUEBA, "i26 · estadístico con `trend`")
cerca(as.numeric(df_d@cval[1, ]), I$i26$drift$criticos, 1e-9, "i26 · valores críticos de `drift`", dec = 2)
cerca(as.numeric(df_t@cval[1, ]), I$i26$trend$criticos, 1e-9, "i26 · valores críticos de `trend`", dec = 2)
comprueba(as.logical(df_d@teststat[1] < df_d@cval[1, "5pct"]) == isTRUE(I$i26$rechaza_drift_5),
          "i26 · con `drift` NO rechaza al 5 %")
comprueba(as.logical(df_t@teststat[1] < df_t@cval[1, "5pct"]) == isTRUE(I$i26$rechaza_trend_5),
          "i26 · con `trend` SÍ rechaza al 5 %: elegir mal la especificación cambia la conclusión")

cat("\n-- i27 [2.7 · P] la tabla de varianzas por orden\n")
tab27 <- I$i27$tabla
for (k in seq_len(nrow(tab27))) {
  d_ <- tab27$orden[k]
  y <- if (d_ == 0) log(demanda) else diff(log(demanda), differences = d_)
  cerca(var(y), tab27$varianza[k], TOL_VAR, sprintf("i27 · varianza con d = %d", d_), dec = 6)
  comprueba(length(y) == tab27$n[k], sprintf("i27 · n con d = %d", d_), sprintf("%d", length(y)))
}
tab27e <- I$i27$tabla_tras_estacional
for (k in seq_len(nrow(tab27e))) {
  d_ <- tab27e$orden_regular_tras_estacional[k]
  y <- diff(log(demanda), lag = 12)
  if (d_ > 0) y <- diff(y, differences = d_)
  cerca(var(y), tab27e$varianza[k], TOL_VAR,
        sprintf("i27 · varianza tras la estacional, d regular = %d", d_), dec = 6)
}
comprueba(which.min(tab27$varianza) - 1 == I$i27$minimo_en,
          "i27 · la varianza mínima está en d = 1")
comprueba(all(diff(tab27$varianza[-1]) > 0),
          "i27 · y VUELVE a subir después: es la firma de la sobrediferenciación")
comprueba(as.integer(suppressWarnings(ndiffs(log(demanda))))  == as.integer(I$i27$ndiffs) &&
            as.integer(suppressWarnings(nsdiffs(log(demanda)))) == as.integer(I$i27$nsdiffs),
          "i27 · ndiffs = 1 y nsdiffs = 1 sobre log(demanda)")

cat("\n-- i28 [2.7 · I] las dos diferencias conmutan\n")
c1 <- diff(diff(log(demanda), lag = 12), lag = 1)
c2 <- diff(diff(log(demanda), lag = 1),  lag = 12)
comprueba(length(c1) == I$i28$n_resultado && length(as.numeric(demanda)) == I$i28$n_original,
          "i28 · 120 observaciones quedan en 107", sprintf("%d -> %d", length(as.numeric(demanda)), length(c1)))
cerca(max(abs(as.numeric(c1) - as.numeric(c2))), I$i28$diferencia_maxima, 1e-12,
      "i28 · la diferencia máxima entre los dos órdenes es CERO", dec = 12)
comprueba(isTRUE(all.equal(as.numeric(c1), as.numeric(c2))) == isTRUE(I$i28$conmutan),
          "i28 · conmutan, y así está publicado")
cerca(var(c1), I$i28$var_estacional_primero, TOL_VAR, "i28 · varianza con la estacional primero", dec = 6)
cerca(var(c2), I$i28$var_regular_primero,    TOL_VAR, "i28 · varianza con la regular primero",    dec = 6)

cat("\n-- i29 [2.7 · G] ¿bastó d = 1?\n")
cerca(acf_manual(log(demanda), 36),  I$i29$antes$acf,   TOL_ACF, "i29 · ACF antes de diferenciar")
cerca(acf_manual(d_log, 36),         I$i29$despues$acf, TOL_ACF, "i29 · ACF después de diferenciar")
cerca(banda(120), I$i29$antes$banda,   TOL_ACF, "i29 · banda antes (n = 120)")
cerca(banda(119), I$i29$despues$banda, TOL_ACF, "i29 · banda después (n = 119)")
prueba_adf(log(demanda), I$i29$antes$adf,   "i29 · antes")
prueba_adf(d_log,        I$i29$despues$adf, "i29 · después")
prueba_kpss(d_log, "Level", I$i29$despues$kpss, "i29 · después, en nivel")
cerca(acf_manual(d_log, 12)[12], I$i29$acf12_despues, TOL_ACF, "i29 · la barra del rezago 12 que queda")
comprueba(I$i29$despues$adf$p_valor < 0.05 && I$i29$despues$kpss$p_valor > 0.05 &&
            abs(I$i29$acf12_despues) > I$i29$despues$banda,
          "i29 · el hueco del ítem: las dos pruebas dicen «estacionaria» y el rezago 12 sigue fuera de banda")

cat("\n-- i30 y i31 [2.8 · C, P] estabilizar la varianza\n")
cerca(por_tramo(demanda, var),       I$i30$var_por_tramo_cruda,   TOL_GENERAL, "i30 · varianza por tramo, serie cruda", dec = 3)
cerca(por_tramo(log(demanda), var),  I$i30$var_por_tramo_log,     TOL_GENERAL, "i30 · varianza por tramo, en logaritmo", dec = 3)
cerca(por_tramo(demanda, mean),      I$i30$media_por_tramo_cruda, TOL_GENERAL, "i30 · media por tramo, serie cruda", dec = 3)
cerca(por_tramo(log(demanda), mean), I$i30$media_por_tramo_log,   TOL_GENERAL, "i30 · media por tramo, en logaritmo", dec = 3)
comprueba(max(I$i30$var_por_tramo_cruda) / min(I$i30$var_por_tramo_cruda) > 3 &&
            max(I$i30$var_por_tramo_log) / min(I$i30$var_por_tramo_log) < 1.5,
          "i30 · el logaritmo aplana la varianza y NO aplana la media: ataca (2), no (1)")
comprueba(all(diff(I$i30$media_por_tramo_log) > 0),
          "i30 · la media en logaritmo sigue subiendo: sigue haciendo falta diferenciar")
lam <- BoxCox.lambda(demanda, method = "guerrero")
cerca(lam, I$i31$lambda, TOL_GENERAL, "i31 · lambda de Guerrero")
cerca(as.numeric(demanda)[1], I$i31$valor, TOL_SERIE, "i31 · el valor transformado es el primero de `demanda`", dec = 3)
v31 <- I$i31$valor; l31 <- I$i31$lambda
cerca((v31^l31 - 1) / l31, I$i31$transformado, TOL_GENERAL, "i31 · la transformación de Box-Cox aplicada a mano")
cerca(as.numeric(BoxCox(v31, l31)), I$i31$comprobacion_R, TOL_GENERAL, "i31 · y coincide con BoxCox() de forecast")
cerca(log(v31), I$i31$log_del_valor, TOL_GENERAL, "i31 · el logaritmo del mismo valor, para el contraste")
comprueba(abs(I$i31$transformado - I$i31$log_del_valor) < 0.05,
          "i31 · con lambda tan cerca de cero, Box-Cox es el logaritmo a efectos prácticos")

cat("\n-- i32 [2.9 · I] el orden del pipeline\n")
saldo_d <- diff(saldo)
cerca(min(saldo),   I$i32$minimo_original,     TOL_SERIE, "i32 · el mínimo de `saldo`", dec = 3)
cerca(min(saldo_d), I$i32$minimo_diferenciado, TOL_SERIE, "i32 · el mínimo de la serie diferenciada", dec = 3)
comprueba(sum(as.numeric(saldo)   <= 0) == I$i32$negativos_original,
          "i32 · valores no positivos en el original", sprintf("%d", sum(as.numeric(saldo) <= 0)))
comprueba(sum(as.numeric(saldo_d) <= 0) == I$i32$negativos_diferenciados,
          "i32 · y en la diferenciada", sprintf("%d", sum(as.numeric(saldo_d) <= 0)))
comprueba(sum(is.nan(suppressWarnings(log(as.numeric(saldo_d))))) == I$i32$cuantos_NaN,
          "i32 · el logaritmo de la diferenciada produce 37 NaN")
comprueba(I$i32$cuantos_NaN == I$i32$negativos_diferenciados,
          "i32 · un NaN por cada valor no positivo, que es exactamente lo que el ítem enseña")

# =====================================================================
seccion("§4 · La procedencia de cada cifra impresa en la prosa")
# =====================================================================
# §3 comprueba que el JSON es correcto. Esto es otra cosa: que lo que el
# enunciado ESCRIBE salga de ese JSON. Los dos defectos son
# independientes —el precálculo puede estar impecable y la retro citar un
# 0.898 que no existe— y este es el que ninguna otra herramienta ve,
# porque no vive en ningún dato, vive en una frase.
#
# El criterio, que es el de aceptación 3 del plan: toda cifra impresa
# tiene que ser (a) una hoja del JSON de su ítem, (b) una hoja de un ítem
# que ese enunciado cita expresamente, (c) una cantidad DERIVADA que se
# recalcula aquí en R, o (d) notación declarada —un subíndice, un orden,
# un rezago—. Lo que no encaje en ninguna de las cuatro, falla.

# El mapa de ítem a bloque. No está en el HTML: el motor de
# autoevaluación no numera los ítems, así que el enlace entre la página y
# el precálculo se declara aquí y se COMPRUEBA contra la página —contra
# el `clave` de cada ítem y contra las seis referencias `D.iNN` que los
# gráficos ya llevan escritas—. Declararlo sin comprobarlo sería suponer
# justo lo que hace falta demostrar.
DIMENSION <- c("G","C","P","G","C","P","I","P","I","G","I","C","C","P","G","I",
               "P","I","G","P","I","G","C","I","P","I","P","I","G","C","P","I")
MODULO <- c("1.1","1.1 · 1.9","1.2","1.3","1.4","1.5","1.5","1.6","1.7","1.7",
            "1.8","2.1","2.1","2.2","2.2","2.5","2.3","2.3","2.3","2.4","2.4",
            "2.3 · 1.3","2.6","2.6","2.6","2.6","2.7","2.7","2.7","2.8","2.8","2.9")
BLOQUE_DE <- c(C = "bloque-a", P = "bloque-b", I = "bloque-c", G = "bloque-d")

trozos_de_bloque <- function(txt, b) {
  i <- regexpr(sprintf("AUTOEVALUACIONES\\['%s'\\] = \\[", b), txt)
  if (i < 0) stop("No encuentro el bloque ", b)
  resto <- substring(txt, i)
  j <- regexpr("\n    \\];", resto)
  bl <- substring(resto, 1, j)
  pos <- as.integer(gregexpr("\n        tipo: '", bl)[[1]])
  fin <- c(pos[-1] - 1L, nchar(bl))
  vapply(seq_along(pos), function(k) substring(bl, pos[k], fin[k]), "")
}

TROZOS <- lapply(unname(BLOQUE_DE), function(b) trozos_de_bloque(TXT, b))
names(TROZOS) <- unname(BLOQUE_DE)

comprueba(sum(lengths(TROZOS)) == 32L, "los cuatro bloques suman 32 ítems en la página",
          paste(sprintf("%s=%d", names(TROZOS), lengths(TROZOS)), collapse = " "))
comprueba(lengths(TROZOS)[["bloque-a"]] == 6 && lengths(TROZOS)[["bloque-b"]] == 9 &&
            lengths(TROZOS)[["bloque-c"]] == 10 && lengths(TROZOS)[["bloque-d"]] == 7,
          "y el reparto por dimensión es 6 C · 9 P · 10 I · 7 G, el del blueprint")

trozo_de_item <- function(n) {
  b <- BLOQUE_DE[[DIMENSION[n]]]
  k <- sum(DIMENSION[1:n] == DIMENSION[n])
  TROZOS[[b]][k]
}

# El mapa, comprobado ítem a ítem contra lo que la página declara.
malos_mapa <- character(0)
for (n in 1:32) {
  s <- trozo_de_item(n)
  cl <- sub(".*clave: '([0-9.]+)'.*", "\\1", regmatches(s, regexpr("clave: '[0-9.]+'", s)))
  ce <- regmatches(s, regexpr("claveExtra: '[0-9.]+'", s))
  claves <- c(cl, if (length(ce)) sub(".*'([0-9.]+)'.*", "\\1", ce))
  esperadas <- trimws(strsplit(MODULO[n], "·", fixed = TRUE)[[1]])
  if (!setequal(claves, esperadas)) malos_mapa <- c(malos_mapa, sprintf("i%02d (%s vs %s)", n,
                paste(claves, collapse = "+"), MODULO[n]))
}
comprueba(length(malos_mapa) == 0,
          "cada ítem del blueprint cae sobre el ítem de la página con el mismo módulo",
          paste(malos_mapa, collapse = " "))

refs_mal <- character(0)
for (n in 1:32) {
  r <- unique(regmatches(trozo_de_item(n), gregexpr("D\\.i[0-9]{2}", trozo_de_item(n)))[[1]])
  if (length(r) && !all(r == sprintf("D.i%02d", n))) refs_mal <- c(refs_mal, sprintf("i%02d->%s", n, paste(r, collapse = ",")))
}
comprueba(length(refs_mal) == 0,
          "y las referencias `D.iNN` que los gráficos ya llevan escritas confirman el mapa",
          if (length(refs_mal)) paste(refs_mal, collapse = " ") else "6 gráficos comprobados")

# ---------------------------------------------------------------------
# Los argumentos de `dibujar` — la tercera superficie
# ---------------------------------------------------------------------
# §3 recorre el JSON y el resto de §4 recorre la prosa. Lo que se le pasa
# a las funciones de dibujo no es ni lo uno ni lo otro, y nadie lo
# miraba: ahí vivía el gráfico del ítem 19, que pintaba la banda de 120
# observaciones sobre la ACF de 119. Ninguna barra caía entre las dos, así
# que no enseñaba nada falso — pero era una cifra escrita a mano en una
# página cuya premisa es que ninguna lo está.
#
# Tres comprobaciones, y la tercera es la que cierra el agujero:
#   (i)   ningún argumento de datos es un literal: todos son rutas del JSON
#   (ii)  toda ruta `D.…` / `S.…` del dibujo resuelve en el JSON incrustado
#         —que es lo que habría delatado el día uno el gráfico vacío del
#         ítem 10, cuando el bloque incrustado se quedó atrás—
#   (iii) la banda que se dibuja es la HERMANA de la ACF que se dibuja, y la
#         frecuencia del subseries la de SU serie: así una cifra correcta no
#         puede acabar emparejada con la serie equivocada, que es
#         exactamente lo que le pasó al ítem 19

# El cuerpo del `dibujar` de un ítem: desde `dibujar:` hasta el campo
# siguiente, que en este archivo va siempre a ocho espacios de sangría.
cuerpo_dibujar <- function(s) {
  i <- regexpr("dibujar: ", s, fixed = TRUE)
  if (i < 0) return("")
  resto <- substring(s, i)
  j <- regexpr("\n        [A-Za-z]+:", resto)
  if (j > 0) substring(resto, 1, j - 1) else resto
}

# Las funciones de dibujo que reciben DATOS. Las otras llamadas del
# cuerpo —`new Chart`, `crearGraficoLinea`— llevan literales de estilo
# (grosores, radios, tensiones) que no son cifras del instrumento.
AYUDANTES <- c("correlograma", "subseries")
FUENTE    <- c(correlograma = "acf", subseries = "valores")
HERMANA   <- c(correlograma = "banda", subseries = "frecuencia")
# Sufijos que son métodos de JavaScript, no niveles del JSON.
METODOS_JS <- c("map", "forEach", "slice", "filter", "reduce", "join", "concat", "length")

# `D.` en la página son los ítems y `S.` las series (`const D =
# PREPARCIAL_DATOS.items`), así que la ruta se resuelve contra el JSON
# incrustado, que es de donde el navegador las va a leer.
resuelve_ruta <- function(ruta) {
  partes <- strsplit(ruta, ".", fixed = TRUE)[[1]]
  nodo <- if (partes[1] == "D") I else if (partes[1] == "S") D$series else NULL
  if (is.null(nodo)) return(NULL)
  for (k in partes[-1]) {
    if (!is.list(nodo)) return(NULL)
    if (!(k %in% names(nodo))) return(NULL)
    nodo <- nodo[[k]]
    if (is.null(nodo)) return(NULL)
  }
  nodo
}
# Se cae por los métodos de JS antes de darla por rota: `D.i22.pares.x.map`
# es la ruta `D.i22.pares.x` con un `.map()` detrás.
resuelve_con_metodos <- function(ruta) {
  partes <- strsplit(ruta, ".", fixed = TRUE)[[1]]
  while (length(partes) > 1) {
    v <- resuelve_ruta(paste(partes, collapse = "."))
    if (!is.null(v)) return(list(ok = TRUE, ruta = paste(partes, collapse = "."), valor = v))
    if (!(partes[length(partes)] %in% METODOS_JS)) break
    partes <- partes[-length(partes)]
  }
  list(ok = FALSE, ruta = ruta, valor = NULL)
}

CUERPOS <- vapply(1:32, function(n) cuerpo_dibujar(trozo_de_item(n)), "")
con_dibujo <- which(nzchar(CUERPOS))
comprueba(identical(as.integer(con_dibujo), as.integer(which(DIMENSION == "G"))),
          "los siete ítems con `dibujar` son exactamente los siete de dimensión G",
          paste(sprintf("i%02d", con_dibujo), collapse = " "))

# (i) y (iii): las llamadas a los ayudantes que reciben datos
literales <- character(0); descuadres <- character(0); pares <- character(0)
CORRELOGRAMAS <- list()
for (n in con_dibujo) {
  id <- sprintf("i%02d", n)
  llamadas <- regmatches(CUERPOS[n],
    gregexpr(sprintf("(%s)\\([^()]*\\)", paste(AYUDANTES, collapse = "|")), CUERPOS[n]))[[1]]
  for (ll in llamadas) {
    fn   <- sub("\\(.*", "", ll)
    args <- trimws(strsplit(sub("^[a-z]+\\(", "", sub("\\)$", "", ll)), ",", fixed = TRUE)[[1]])
    datos <- args[-1]                      # el primero es el canvas
    malos <- datos[!grepl("^[DS]\\.[A-Za-z_]", datos)]
    if (length(malos)) literales <- c(literales, sprintf("%s·%s(%s)", id, fn, paste(malos, collapse = "|")))
    if (length(datos) == 2L && !length(malos)) {
      p <- strsplit(datos[1], ".", fixed = TRUE)[[1]]
      esperada <- paste(c(p[-length(p)], HERMANA[[fn]]), collapse = ".")
      ok <- p[length(p)] == FUENTE[[fn]] && identical(datos[2], esperada)
      if (!ok) descuadres <- c(descuadres, sprintf("%s· %s no es la hermana de %s", id, datos[2], datos[1]))
      pares <- c(pares, sprintf("%s:%s", id, datos[2]))
      # Se apunta el par para el recuento de barras fuera de banda, que
      # necesita la prosa y por tanto se comprueba más abajo.
      if (fn == "correlograma" && ok)
        CORRELOGRAMAS[[id]] <- list(item = n,
                                     acf = as.numeric(unlist(resuelve_ruta(datos[1]))),
                                     banda = as.numeric(resuelve_ruta(datos[2])))
    }
  }
}
comprueba(length(literales) == 0,
          "ningún argumento de datos de `dibujar` es un literal escrito a mano",
          if (length(literales)) paste(literales, collapse = " ") else
            sprintf("%d llamadas a %s, todas con rutas del JSON", length(pares),
                    paste(AYUDANTES, collapse = "/")))
comprueba(length(descuadres) == 0,
          "y cada banda/frecuencia dibujada es la HERMANA en el JSON de la serie que dibuja",
          if (length(descuadres)) paste(descuadres, collapse = " · ") else paste(pares, collapse = " "))

# (ii) Toda ruta del dibujo resuelve, y las que van al ayudante son numéricas
rotas <- character(0); no_numericas <- character(0); n_rutas <- 0L
for (n in con_dibujo) {
  id <- sprintf("i%02d", n)
  rutas <- unique(regmatches(CUERPOS[n],
    gregexpr("[DS]\\.[A-Za-z_][A-Za-z0-9_]*(\\.[A-Za-z_][A-Za-z0-9_]*)*", CUERPOS[n]))[[1]])
  for (r in rutas) {
    n_rutas <- n_rutas + 1L
    res <- resuelve_con_metodos(r)
    if (!res$ok) { rotas <- c(rotas, sprintf("%s·%s", id, r)); next }
    v <- unlist(res$valor, use.names = FALSE)
    if (!length(v) || !all(is.finite(suppressWarnings(as.numeric(v)))))
      no_numericas <- c(no_numericas, sprintf("%s·%s", id, res$ruta))
  }
}
comprueba(length(rotas) == 0,
          "las rutas `D.…`/`S.…` de los siete dibujos resuelven en el JSON incrustado",
          if (length(rotas)) paste(rotas, collapse = " ") else sprintf("%d rutas seguidas", n_rutas))
comprueba(length(no_numericas) == 0,
          "y todas traen datos numéricos, no un hueco que dibujaría un gráfico vacío",
          if (length(no_numericas)) paste(no_numericas, collapse = " ") else "")


# --- La prosa, limpia de marcado ---
CAMPOS <- c("pregunta", "pista", "retro", "retroAcierto", "retroFallo", "texto", "descripcionGrafico")
prosa_de <- function(s) {
  out <- character(0)
  for (cp in CAMPOS) {
    pt <- sprintf("(?<![A-Za-z])%s: '((\\\\'|[^'])*)'", cp)
    out <- c(out, regmatches(s, gregexpr(pt, s, perl = TRUE))[[1]])
  }
  p <- paste(out, collapse = " ")
  p <- gsub("&nbsp;", " ", p, fixed = TRUE)
  p <- gsub("−", "-", p, fixed = TRUE)   # el menos tipográfico
  p <- gsub("–", "-", p, fixed = TRUE)
  p
}
cifras_de <- function(p)
  unique(regmatches(p, gregexpr("(?<![0-9A-Za-z_.])-?[0-9]+(\\.[0-9]+)?", p, perl = TRUE))[[1]])

hojas_de <- function(x) {
  v <- unlist(x, use.names = FALSE)
  n <- suppressWarnings(as.numeric(v))
  n[is.finite(n)]
}

# (d) Notación: cifras que no son magnitudes sino índices. Órdenes de
# diferenciación y de media móvil, números de condición y de opción,
# subíndices de la PACF (`\phi_{11}`, `\phi_{22}`), el periodo estacional,
# los horizontes de rezago que se pintan y el 95/5 de la banda.
NOTACION <- c(0, 1, 2, 3, 4, 5, 6, 11, 12, 22, 24, 36, 95, 100,
              0.05)   # el 5 % de la banda, escrito como proporción

# Excepciones por ítem, cada una con su razón. La lista es corta a
# propósito: si crece, lo que hay es prosa citando cifras que nadie
# calcula, y eso es el hallazgo, no el estorbo.
EXCEPCION <- list(
  i02 = list(valores = c(200, 10, 50, 2020, 2024),
             razon = "los tres conjuntos de datos del enunciado son ficticios: el ítem es `sin_cifras`"),
  i19 = list(valores = c(48),
             razon = "un rezago hipotético: «con 48 habría un pico ahí también»"),
  i25 = list(valores = c(13),
             razon = "la constante del truncamiento de urca::ur.kpss, floor(3*sqrt(n)/13)"),
  i03 = list(valores = c(2019, 2021, 30),
             razon = "el inicio, el final y el n del objeto ts, ya comprobados en §3")
)

# (c) Las cantidades DERIVADAS que la prosa calcula por su cuenta. Cada
# una se rehace aquí en R. Son las que más lo necesitan: no vienen de
# `genera_preparcial.R`, las escribió una frase.
DERIVADAS <- list(
  # Las esperadas por azar en los 24 rezagos del correlograma barajado:
  # el mismo 5 % con el que el item 14 cuenta 1.8 sobre 36.
  i01 = c(esperadas_fuera_por_azar     = 0.05 * length(I$i01$acf_barajada$acf)),
  i03 = c(meses_desde_el_inicio         = I$i03$n - 1,
          anio_si_sumas_30              = as.numeric(I$i03$inicio[1]) + floor((as.numeric(I$i03$inicio[2]) - 1 + I$i03$n) / 12),
          observacion_siguiente         = I$i03$n + 1),
  i05 = c(porcentaje_del_atipico        = 100 * (as.numeric(dem_atip)[pos] / as.numeric(demanda)[pos] - 1)),
  i06 = c(media_simple_de_las_cinco     = mean(cinco)),
  i10 = c(diferencia_en_marzo           = nor[pos, "seasonal"] - rob[pos, "seasonal"]),
  i12 = c(observaciones_por_tramo       = length(as.numeric(blanco)) / 3),
  # El error que la propia retro nombra: dividir entre las cinco
  # desviaciones que participan en el numerador en vez de entre las seis.
  i17 = c(r1_con_denominador_de_cinco   = num6 / sum((seis[-1] - m6)^2)),
  i20 = c(r1_al_cuadrado                = I$i20$r1^2,
          numerador_de_phi22            = I$i20$r2 - I$i20$r1^2,
          denominador_de_phi22          = 1 - I$i20$r1^2),
  i25 = c(n_sobre_100                   = I$i25$n / 100,
          raiz_cuarta_de_n_sobre_100    = (I$i25$n / 100)^0.25,
          # La retro multiplica por el 1.0466 YA REDONDEADO que la pista
          # le acaba de dar al estudiante, no por el valor exacto: 4.186 y
          # no 4.187. Es la aritmética del estudiante, y está bien así.
          cuatro_por_la_raiz_redondeada = 4 * round((I$i25$n / 100)^0.25, 4)),
  i28 = c(observaciones_perdidas        = I$i28$n_original - I$i28$n_resultado),
  i30 = c(razon_de_varianzas_cruda      = max(I$i30$var_por_tramo_cruda) / min(I$i30$var_por_tramo_cruda),
          razon_de_varianzas_log        = max(I$i30$var_por_tramo_log) / min(I$i30$var_por_tramo_log)),
  i31 = c(diferencia_con_el_logaritmo   = I$i31$transformado - I$i31$log_del_valor,
          porcentaje_de_esa_diferencia  = 100 * (I$i31$transformado - I$i31$log_del_valor) / I$i31$log_del_valor),
  i32 = c(n_de_saldo                    = length(as.numeric(saldo)),
          n_de_saldo_diferenciada       = length(as.numeric(saldo)) - 1)
)

# (b) Los ítems que citan expresamente cifras de OTRO ítem. Declararlo
# deja escrito el grafo de citas de la página, que hasta ahora no estaba
# en ninguna parte.
CITAS <- list(i15 = "i14", i16 = "i12", i19 = "i14", i21 = "i20",
              i28 = "i32", i29 = "i27", i32 = "i28")

sin_origen <- list()
for (n in 1:32) {
  id <- sprintf("i%02d", n)
  candidatas <- c(hojas_de(I[[id]]), NOTACION,
                  unname(DERIVADAS[[id]]),
                  if (!is.null(CITAS[[id]])) c(hojas_de(I[[CITAS[[id]]]]),
                                               unname(DERIVADAS[[CITAS[[id]]]])),
                  if (!is.null(EXCEPCION[[id]])) EXCEPCION[[id]]$valores,
                  as.numeric(unlist(lapply(D$series, function(s) c(s$n, s$frecuencia, s$inicio)))))
  huerfanas <- character(0)
  for (z in cifras_de(prosa_de(trozo_de_item(n)))) {
    dec <- if (grepl("\\.", z)) nchar(sub(".*\\.", "", z)) else 0
    v <- as.numeric(z)
    media_ulp <- 0.5 * 10^(-dec) + 1e-9
    if (!any(abs(candidatas - v) <= media_ulp) && !any(abs(abs(candidatas) - abs(v)) <= media_ulp))
      huerfanas <- c(huerfanas, z)
  }
  if (length(huerfanas)) sin_origen[[id]] <- huerfanas
}

for (n in 1:32) {
  id <- sprintf("i%02d", n)
  nums <- cifras_de(prosa_de(trozo_de_item(n)))
  h <- sin_origen[[id]]
  comprueba(is.null(h), sprintf("%s · las %d cifras de su prosa tienen origen", id, length(nums)),
            if (is.null(h)) "" else paste("sin origen:", paste(h, collapse = " ")))
}

# ---------------------------------------------------------------------
# Lo que la prosa AFIRMA de su propio correlograma
# ---------------------------------------------------------------------
# Todo lo anterior comprueba cifras, y una afirmación falsa no siempre
# lleva una cifra dentro. El ítem 1 decía «correlograma plano: las 24
# barras caen dentro de la banda» y «aquí ninguna barra llega a la
# banda» — con tres barras fuera, en los rezagos 13, 14 y 18. Las dos
# frases pasaban las 370 comprobaciones porque no contenían ninguna
# cifra sin origen: 0.1789 existe, la ACF está bien calculada, y «plano»
# no es un número.
#
# Aquí se recuenta desde los datos que el gráfico dibuja y se exige que
# la prosa del ítem no lo desmienta. El recuento se IMPRIME siempre, que
# es lo que convierte «nadie lo miró» en «está en la salida».
FRASES_DE_VACIO <- c("ninguna barra", "correlograma plano", "caen dentro de la banda",
                     "llega a la banda", "todas dentro de la banda", "ninguna se sale")
cat("\n  Barras fuera de banda en cada correlograma dibujado:\n")
desmentidos <- character(0)
for (id in names(CORRELOGRAMAS)) {
  cg <- CORRELOGRAMAS[[id]]
  fuera <- which(abs(cg$acf) > cg$banda)
  cat(sprintf("    %s  %2d de %2d fuera (banda %.4f)%s\n", id, length(fuera), length(cg$acf),
              cg$banda, if (length(fuera)) paste("  rezagos", paste(fuera, collapse = ", ")) else ""))
  if (length(fuera)) {
    pr <- tolower(prosa_de(trozo_de_item(cg$item)))
    dichas <- FRASES_DE_VACIO[vapply(FRASES_DE_VACIO, function(f) grepl(f, pr, fixed = TRUE), TRUE)]
    if (length(dichas))
      desmentidos <- c(desmentidos, sprintf("%s dice «%s» con %d barras fuera",
                                            id, paste(dichas, collapse = "»/«"), length(fuera)))
  }
}
comprueba(length(desmentidos) == 0,
          "ninguna prosa afirma que su correlograma está limpio cuando tiene barras fuera de banda",
          if (length(desmentidos)) paste(desmentidos, collapse = " · ") else
            sprintf("%d correlogramas recontados desde sus propios datos", length(CORRELOGRAMAS)))

cat("\n  Excepciones declaradas (cifras impresas que NO salen de R):\n")
for (id in names(EXCEPCION))
  cat(sprintf("    %s  %-28s  %s\n", id,
              paste(EXCEPCION[[id]]$valores, collapse = " "), EXCEPCION[[id]]$razon))

# ---------------------------------------------------------------------
# Dónde cae la opción correcta
# ---------------------------------------------------------------------
# El motor pinta las opciones EN EL ORDEN EN QUE ESTÁN ESCRITAS: no
# baraja. Los 23 ítems de opción y de gráfico se escribieron con la
# correcta la primera, los 23, y así el instrumento se aprueba sin
# leerlo: marcando siempre la primera salen 23 de 32 y ningún objetivo
# del termómetro llega a «flojo». Es el peor defecto posible aquí,
# porque el diagnóstico es el único producto (D9) y el patrón se ve a
# los tres ítems.
#
# Se comprueba lo que importa —el reparto—, no un orden concreto, para
# que una reordenación futura siga pasando.
UMBRAL_POSICION <- 0.40   # ninguna posición se lleva más del 40 %
RACHA_MAXIMA    <- 2L     # ni tres ítems seguidos con la correcta en el mismo sitio

# Se cuentan las banderas `correcta:`, no los bloques de texto: los ítems
# del diagnóstico y los del simulacro tienen sangrías distintas, y cortar
# por sangría hacía que el simulacro contara CERO opciones sin que nada
# lo dijera. Contar banderas no depende del formato.
posicion_correcta <- function(s) {
  m <- regmatches(s, gregexpr("correcta: (true|false)", s))[[1]]
  if (!length(m)) return(structure(integer(0), n = 0L))
  structure(which(m == "correcta: true"), n = length(m))
}

# En el orden en que el estudiante los encuentra: bloque A, bloque C,
# bloque D. El bloque B es numérico y no tiene opciones.
n_A <- sum(DIMENSION == "C"); n_C <- sum(DIMENSION == "I"); n_D <- sum(DIMENSION == "G")
ORDEN_ENCUENTRO <- c(which(DIMENSION == "C"), which(DIMENSION == "I"), which(DIMENSION == "G"))
ETIQUETAS <- paste0(rep(c("A", "C", "D"), c(n_A, n_C, n_D)),
                    c(seq_len(n_A), seq_len(n_C), seq_len(n_D)))
POSICIONES <- lapply(ORDEN_ENCUENTRO, function(n) posicion_correcta(trozo_de_item(n)))
n_opciones <- vapply(POSICIONES, function(z) as.integer(attr(z, "n")), 0L)
# Una sola correcta por ítem, o NA. Sin este colador, un ítem con dos
# correctas alargaba el vector y REVENTABA el informe en vez de hacerlo
# fallar — que es la forma más tonta de que una comprobación no sirva.
pos <- vapply(POSICIONES, function(z) if (length(z) == 1L) as.integer(z) else NA_integer_, 0L)
sanos <- !is.na(pos)

comprueba(length(ORDEN_ENCUENTRO) == 23L && all(n_opciones == 4L) && all(sanos),
          "los 23 ítems de opción y gráfico traen cuatro opciones y exactamente una correcta",
          sprintf("%d ítems · opciones %s · con una sola correcta %d de %d",
                  length(ORDEN_ENCUENTRO), paste(unique(n_opciones), collapse = "/"),
                  sum(sanos), length(pos)))

reparto <- table(factor(pos[sanos], levels = 1:4))
cat("\n  Posición de la opción correcta, en el orden en que se encuentran:\n")
cat("   ", paste(sprintf("%s:%s", ETIQUETAS, ifelse(sanos, pos, "?")), collapse = "  "), "\n")
cat("    reparto: ", paste(sprintf("%d->%d", 1:4, as.integer(reparto)), collapse = "  "), "\n", sep = "")

# Los dos umbrales, probados contra el estado del que se viene: si no
# mordieran, pasarían igual de verdes y no se notaría. La extracción
# desde el HTML la prueba la siembra de §8; esto prueba las reglas.
comprueba(max(table(rep(1L, 23L))) / 23 > UMBRAL_POSICION,
          "la regla del 40 % RECHAZA el reparto del que se viene (las 23 en la primera)")
comprueba(max(rle(c(4L, 2L, 2L, 2L, 1L))$lengths) > RACHA_MAXIMA,
          "y la regla de la racha RECHAZA tres seguidas en el mismo sitio")

comprueba(sum(sanos) > 0 && max(reparto) / sum(sanos) <= UMBRAL_POSICION,
          sprintf("ninguna posición concentra más del %.0f %% de las respuestas correctas",
                  100 * UMBRAL_POSICION),
          sprintf("la peor es la %d con %d de %d (%.0f %%)", which.max(reparto), max(reparto),
                  sum(sanos), 100 * max(reparto) / max(sum(sanos), 1)))
racha <- rle(pos[sanos])
comprueba(max(racha$lengths) <= RACHA_MAXIMA,
          sprintf("ni %d ítems seguidos con la correcta en la misma posición", RACHA_MAXIMA + 1L),
          sprintf("racha más larga: %d (posición %d)", max(racha$lengths),
                  racha$values[which.max(racha$lengths)]))

# ---------------------------------------------------------------------
# Tipografía y terminología (A5)
# ---------------------------------------------------------------------
# No hay corrector de ortografía en esta máquina —ni `hunspell`, ni
# `aspell`, ni `ispell`, ni `pyobjc` para el de macOS— así que la
# ortografía se lee. Lo que sí se mecaniza es lo que una lectura hace
# peor que un `grep`: que no se cuele un carácter roto, que las
# matemáticas cierren, y que el vocabulario no se bifurque a mitad del
# instrumento. En un archivo cuyas tildes ya viajaron rotas una vez, lo
# primero no es paranoia.
CARACTERES_ESPERADOS <- c("á","é","í","ó","ú","ü","ñ","Á","É","Í","Ó","Ú","Ñ",
                          "¿","¡","«","»","—","–","·","×","≠","≤","≥","±",
                          "∇","−","↔","→","∑","…","°","º","ª","🎯")
prosa_items <- paste(vapply(1:32, function(n) prosa_de(trozo_de_item(n)), ""), collapse = " ")
raros <- setdiff(unique(strsplit(gsub("[ -~\n\t]", "", prosa_items), "")[[1]]),
                 CARACTERES_ESPERADOS)
comprueba(length(raros) == 0,
          "ningún carácter fuera del repertorio esperado: las tildes siguen enteras",
          if (length(raros)) paste(raros, collapse = " ") else
            sprintf("%d caracteres no ASCII, todos declarados",
                    length(unique(strsplit(gsub("[ -~\n\t]", "", prosa_items), "")[[1]]))))

# Los `$` de KaTeX, campo a campo: uno impar deja media fórmula en crudo.
campos_sueltos <- unlist(lapply(1:32, function(n) {
  s <- trozo_de_item(n)
  unlist(lapply(CAMPOS, function(cp)
    regmatches(s, gregexpr(sprintf("(?<![A-Za-z])%s: '((\\\\'|[^'])*)'", cp), s, perl = TRUE))[[1]]))
}))
impares <- sum(vapply(campos_sueltos, function(z) nchar(gsub("[^$]", "", z)) %% 2 == 1, TRUE))
comprueba(impares == 0, "los `$` de KaTeX cierran en los 32 ítems, campo a campo",
          sprintf("%d campos con número impar de $ (de %d)", impares, length(campos_sueltos)))

# El vocabulario no se bifurca. El de la izquierda es el término del
# material; el de la derecha, el sinónimo que lo rompería.
TERMINOS <- list(c("rezago", "retardo"), c("banda", "intervalo de confianza"),
                 c("correlograma", "gráfico de autocorrelación"), c("atípico", "outlier"))
bifurcado <- character(0)
for (par in TERMINOS) {
  n_malo <- length(gregexpr(par[2], prosa_items, fixed = TRUE)[[1]])
  if (!(n_malo == 1 && gregexpr(par[2], prosa_items, fixed = TRUE)[[1]][1] == -1))
    bifurcado <- c(bifurcado, sprintf("«%s» aparece %d veces junto a «%s»", par[2], n_malo, par[1]))
}
comprueba(length(bifurcado) == 0,
          "la terminología no se bifurca: un solo término para cada cosa",
          if (length(bifurcado)) paste(bifurcado, collapse = " · ") else
            paste(vapply(TERMINOS, function(p) p[1], ""), collapse = " · "))

comprueba(!grepl("--", prosa_items, fixed = TRUE),
          "ni un guion doble donde va una raya (—)")


# ---------------------------------------------------------------------
# El simulacro (P8): seis ítems que NO estaban en las comprobaciones
# ---------------------------------------------------------------------
# El simulacro vive fuera de `AUTOEVALUACIONES` a propósito —no entra en
# el diagnóstico— y por eso todo lo de arriba lo ignoraba: sus cifras no
# se trazaban, sus enunciados no se contrastaban contra los 56 previos y
# la posición de su opción correcta no la miraba nadie. Seis ítems
# publicados sin una sola comprobación es exactamente el estado del que
# esta auditoría viene.
sim_bloque <- local({
  i <- regexpr("const SIMULACRO = {", TXT, fixed = TRUE)
  if (i < 0) stop("No encuentro `const SIMULACRO`")
  resto <- substring(TXT, i)
  j <- regexpr("\n    };", resto, fixed = TRUE)
  substring(resto, 1, j)
})
SIM_TROZOS <- local({
  pos <- as.integer(gregexpr("\n          objetivo: '", sim_bloque, fixed = TRUE)[[1]])
  fin <- c(pos[-1] - 1L, nchar(sim_bloque))
  vapply(seq_along(pos), function(k) substring(sim_bloque, pos[k], fin[k]), "")
})

comprueba(length(SIM_TROZOS) == 6L, "el simulacro declara seis ítems",
          sprintf("%d", length(SIM_TROZOS)))

sim_obj <- vapply(SIM_TROZOS, function(s)
  sub(".*objetivo: '(O[0-9])'.*", "\\1", regmatches(s, regexpr("objetivo: 'O[0-9]'", s))), "")
comprueba(identical(unname(sim_obj), sprintf("O%d", 1:6)),
          "uno por objetivo, O1 a O6: es el formato del parcial en pequeño",
          paste(sim_obj, collapse = " "))

sim_min <- as.integer(sub(".*: *", "", regmatches(sim_bloque, regexpr("minutos: [0-9]+", sim_bloque))))
comprueba(is.finite(sim_min) && sim_min > 0,
          "declara cuántos minutos dura, y la barra lateral dice lo mismo",
          sprintf("%d min · barra lateral: %s", sim_min,
                  regmatches(TXT, regexpr('shortTitle: "Simulacro",\\s*duration: "[^"]+"', TXT))))
comprueba(grepl(sprintf('shortTitle: "Simulacro", *duration: "%d min"', sim_min), TXT),
          "y la duración de la barra lateral no se ha quedado atrás")

# La posición de la correcta, igual que en los 23 del diagnóstico.
sim_pos <- lapply(SIM_TROZOS, posicion_correcta)
# El ítem numérico no tiene `opciones`, así que no trae el atributo: sin
# este colador el `vapply` reventaba en vez de contar cinco.
sim_con_opciones <- which(vapply(sim_pos, function(z) {
  n <- attr(z, "n"); if (is.null(n)) 0L else as.integer(n)
}, 0L) > 0L)
sim_p <- vapply(sim_pos[sim_con_opciones],
                function(z) if (length(z) == 1L) as.integer(z) else NA_integer_, 0L)
comprueba(all(!is.na(sim_p)) && length(sim_con_opciones) == 5L,
          "los cinco ítems de opción del simulacro traen exactamente una correcta",
          sprintf("%d ítems de opción · posiciones %s", length(sim_con_opciones),
                  paste(sim_p, collapse = " ")))
comprueba(length(sim_p) > 0 && max(table(sim_p)) <= 2L,
          "y su correcta no se concentra en una posición",
          sprintf("posiciones %s", paste(sim_p, collapse = " ")))

# De qué ítems del precálculo toma prestadas sus cifras cada uno. El
# simulacro no tiene entrada propia en el JSON —no se generó nada nuevo
# para él, que es lo que evita regenerar el precálculo (R3)— así que su
# procedencia se declara aquí y se comprueba igual que la de la prosa.
CITAS_SIMULACRO <- list(S1 = "i05", S2 = "i10", S3 = "i12", S4 = "i22",
                        S5 = "i27", S6 = c("i12", "i30"))
sim_sin_origen <- list()
for (k in 1:6) {
  id <- sprintf("S%d", k)
  candidatas <- c(NOTACION,
                  unlist(lapply(CITAS_SIMULACRO[[id]], function(z) hojas_de(I[[z]]))),
                  as.numeric(unlist(lapply(D$series, function(s) c(s$n, s$frecuencia, s$inicio)))))
  huerfanas <- character(0)
  for (z in cifras_de(prosa_de(SIM_TROZOS[k]))) {
    dec <- if (grepl("\\.", z)) nchar(sub(".*\\.", "", z)) else 0
    v <- as.numeric(z); ulp <- 0.5 * 10^(-dec) + 1e-9
    if (!any(abs(candidatas - v) <= ulp) && !any(abs(abs(candidatas) - abs(v)) <= ulp))
      huerfanas <- c(huerfanas, z)
  }
  if (length(huerfanas)) sim_sin_origen[[id]] <- huerfanas
}
for (k in 1:6) {
  id <- sprintf("S%d", k)
  nums <- cifras_de(prosa_de(SIM_TROZOS[k]))
  h <- sim_sin_origen[[id]]
  comprueba(is.null(h),
            sprintf("%s · las %d cifras de su prosa salen de %s", id, length(nums),
                    paste(CITAS_SIMULACRO[[id]], collapse = "+")),
            if (is.null(h)) "" else paste("sin origen:", paste(h, collapse = " ")))
}

# El borde de la tabla de `tseries`: 16 p-valores llegan como 0.01 o 0.1
# porque son los extremos interpolables, y escribirlos con un igual es
# afirmar de más. El plan lo exige y la página lo cumple; esto lo mantiene.
prosa_toda <- paste(vapply(1:32, function(n) prosa_de(trozo_de_item(n)), ""), collapse = " ")
comprueba(!grepl("p = 0\\.01(?![0-9])", prosa_toda, perl = TRUE) &&
            !grepl("p = 0\\.10?(?![0-9])", prosa_toda, perl = TRUE),
          "ni un `p = 0.01` ni un `p = 0.10` en la prosa: los bordes van con < o >")

# =====================================================================
seccion("§5 · Las siete claves numéricas y los dos ítems convertidos")
# =====================================================================
# Una clave numérica no basta con que sea correcta: su TOLERANCIA tiene
# que dejar fuera el error que la propia retroalimentación nombra. Si lo
# admite, el ítem da por bueno justo el razonamiento que quería corregir,
# y el diagnóstico —que es el único producto de esto— miente.

claves_b <- regmatches(TROZOS[["bloque-b"]],
                       regexpr("respuesta: (-?[0-9.]+), tolerancia: ([0-9.]+)", TROZOS[["bloque-b"]]))
# Siete y no nueve: i03 e i14 son ahora de opción múltiple. La Biblioteca de
# Preguntas de Brightspace no importa respuesta numérica, y esos dos eran los
# ítems de FPP3 §2.1 y §2.9 — los únicos de sus temas en todo el instrumento.
# Convertirlos los mete en el banco; lo que se comprueba de ellos está abajo.
comprueba(length(claves_b) == 7L, "los siete ítems numéricos del bloque B declaran respuesta y tolerancia",
          sprintf("%d de 7", length(claves_b)))
respuesta_de  <- as.numeric(sub(".*respuesta: (-?[0-9.]+), .*", "\\1", claves_b))
tolerancia_de <- as.numeric(sub(".*tolerancia: ([0-9.]+).*", "\\1", claves_b))

# Ítem del blueprint, lo que R vuelve a calcular, y el error típico que
# la retroalimentación de ese mismo ítem nombra con todas sus letras.
CLAVES <- list(
  list(item = 6,  recalculado = sum(c(0.125, 0.25, 0.25, 0.25, 0.125) * cinco),
       error = mean(cinco), porque = "promediar las cinco a partes iguales (61.29)"),
  list(item = 8,  recalculado = (prom - mean(prom))[3],
       error = prom[3], porque = "no centrar: quedarse en el promedio sin restar la media (9.5724)"),
  list(item = 17, recalculado = num6 / den6,
       error = num6 / sum((seis[-1] - m6)^2), porque = "dividir entre cinco desviaciones y no entre seis (-0.64)"),
  list(item = 20, recalculado = phi22,
       error = I$i20$r2, porque = "no descontar nada y devolver r_2 (-0.3766)"),
  list(item = 25, recalculado = trunc_kpss(120),
       error = trunc_urca(120), porque = "dar el truncamiento de urca (2) en vez del de tseries (4)"),
  list(item = 27, recalculado = which.min(tab27$varianza) - 1,
       error = 2, porque = "sobrediferenciar y elegir d = 2"),
  list(item = 31, recalculado = (v31^l31 - 1) / l31,
       error = log(v31), porque = "devolver el logaritmo (3.3418) en vez de la Box-Cox")
)

for (k in seq_along(CLAVES)) {
  cv <- CLAVES[[k]]
  id <- sprintf("i%02d", cv$item)
  r  <- respuesta_de[k]; tol <- tolerancia_de[k]
  cerca(cv$recalculado, r, max(tol, 1e-9), sprintf("%s · la clave publicada es la que R calcula", id),
        sprintf("clave %s", format(r)), dec = 4)
  admite_error <- abs(cv$error - r) <= tol
  comprueba(!admite_error,
            sprintf("%s · la tolerancia (%s) RECHAZA el error típico: %s", id, format(tol), cv$porque),
            sprintf("|%s - %s| = %.4f", format(cv$error), format(r), abs(cv$error - r)))
}

# --- Los dos que dejaron de ser numéricos ----------------------------------
# i03 e i14 ya no tienen tolerancia que pueda admitir el error típico: ahora el
# error ES una de las cuatro opciones. La garantía cambia de forma y no de
# fondo — se comprueba que la opción marcada como correcta sea la que lleva la
# cifra que R calcula, y que cada distractor lleve exactamente la del error que
# dice representar. Si el generador cambia una, el ítem deja de cuadrar y esto
# lo dice, que es lo mismo que hacía la tolerancia.

opciones_de <- function(trozo) {
  crudo <- regmatches(trozo, gregexpr("texto: '[^']*', correcta: (true|false)", trozo))[[1]]
  data.frame(texto = sub("^texto: '(.*)', correcta: (true|false)$", "\\1", crudo),
             correcta = grepl("correcta: true$", crudo),
             stringsAsFactors = FALSE)
}

CONVERTIDOS <- list(
  list(id = "i03", k = 1L, correcta = I$i03$ultimo_prosa,
       errores = unlist(I$i03$errores, use.names = FALSE)),
  list(id = "i14", k = 4L, correcta = format(I$i14$esperadas_fuera),
       errores = vapply(I$i14$errores, format, ""))
)

for (cv in CONVERTIDOS) {
  s5 <- TROZOS[["bloque-b"]][cv$k]
  comprueba(grepl("tipo: 'opcion'", s5, fixed = TRUE),
            sprintf("%s · es de opción múltiple y no numérica (la Biblioteca no importa numéricas)", cv$id))
  ops <- opciones_de(s5)
  comprueba(nrow(ops) == 4L, sprintf("%s · ofrece cuatro opciones", cv$id),
            sprintf("%d", nrow(ops)))

  lleva <- function(valor) grepl(valor, ops$texto, fixed = FALSE, ignore.case = TRUE)
  comprueba(sum(lleva(cv$correcta) & ops$correcta) == 1L &&
              sum(lleva(cv$correcta)) == 1L,
            sprintf("%s · la ÚNICA opción que lleva la cifra de R (%s) es la marcada correcta",
                    cv$id, cv$correcta),
            paste(sprintf("[%s]%s", ops$texto, ifelse(ops$correcta, "*", "")), collapse = " · "))

  for (e in cv$errores) {
    comprueba(sum(lleva(e) & !ops$correcta) == 1L,
              sprintf("%s · el error «%s» está ofrecido como distractor, y solo como distractor",
                      cv$id, e))
  }
}

# =====================================================================
seccion("§6 · La tabla de especificaciones publicada y los 18 módulos")
# =====================================================================
# D13 publica la tabla dentro del módulo 1. Publicarla obliga a que sea
# verdad: si el reparto real de los 32 ítems no se parece a los pesos que
# la tabla anuncia, el estudiante estudia con una brújula torcida.

pesos_js <- regmatches(TXT, gregexpr("O[1-6]: \\{ titulo: '[^']*', peso: ([0-9]+) \\}", TXT))[[1]]
pesos <- as.numeric(sub(".*peso: ([0-9]+).*", "\\1", pesos_js))
names(pesos) <- sub("^(O[1-6]).*", "\\1", pesos_js)
comprueba(length(pesos) == 6L && sum(pesos) == 100,
          "los seis objetivos de OBJETIVOS pesan 100 % en total",
          paste(sprintf("%s=%d", names(pesos), pesos), collapse = " "))

# La tabla del módulo 1, leída del HTML y no del código: es la que se ve.
m1 <- substring(TXT, regexpr('<template id="module-1">', TXT))
m1 <- substring(m1, 1, regexpr("</template>", m1))
pesos_tabla <- as.numeric(sub(".*<strong>([0-9]+) %</strong>.*", "\\1",
                              regmatches(m1, gregexpr("<strong>[0-9]+ %</strong>", m1))[[1]]))
comprueba(identical(as.numeric(pesos_tabla), as.numeric(pesos)),
          "la tabla que el estudiante ve publica exactamente esos pesos",
          paste(pesos_tabla, collapse = " · "))

objetivo_de <- vapply(1:32, function(n)
  sub(".*objetivo: '(O[1-6])'.*", "\\1", regmatches(trozo_de_item(n), regexpr("objetivo: 'O[1-6]'", trozo_de_item(n)))), "")
reparto <- table(factor(objetivo_de, levels = sprintf("O%d", 1:6)))
comprueba(identical(as.integer(reparto), c(5L, 6L, 5L, 6L, 7L, 3L)),
          "el reparto real de los 32 ítems por objetivo es 5/6/5/6/7/3",
          paste(sprintf("%s=%d", names(reparto), reparto), collapse = " "))
desv <- max(abs(100 * as.numeric(reparto) / 32 - pesos))
comprueba(desv <= 2.0,
          "y la desviación entre peso e ítems no pasa de 2 puntos porcentuales",
          sprintf("máxima %.1f puntos", desv))

claves_item <- lapply(1:32, function(n) {
  s <- trozo_de_item(n)
  c(sub(".*clave: '([0-9.]+)'.*", "\\1", regmatches(s, regexpr("clave: '[0-9.]+'", s))),
    if (grepl("claveExtra", s)) sub(".*claveExtra: '([0-9.]+)'.*", "\\1", regmatches(s, regexpr("claveExtra: '[0-9.]+'", s))))
})
cobertura <- table(unlist(claves_item))
LOS_18 <- c(sprintf("1.%d", 1:9), sprintf("2.%d", 1:9))
comprueba(all(LOS_18 %in% names(cobertura)),
          "los 18 módulos del Módulo I quedan tocados por algún ítem",
          sprintf("%d de 18", sum(LOS_18 %in% names(cobertura))))
HUERFANOS <- c("1.1", "1.5", "1.7", "2.2", "2.4")
comprueba(all(cobertura[HUERFANOS] >= 2),
          "los cinco módulos que el Taller 1 dejó fuera del escrito llevan DOS ítems (D5)",
          paste(sprintf("%s×%d", HUERFANOS, cobertura[HUERFANOS]), collapse = " "))
comprueba(cobertura[["1.9"]] >= 1 && cobertura[["2.9"]] >= 1,
          "y los dos módulos de cierre, 1.9 y 2.9, llevan al menos uno")
comprueba(grepl("subseries", TXT, fixed = TRUE) && grepl("gg_subseries|subseries", prosa_toda),
          "`gg_subseries` aparece en el instrumento (C3, que el Taller 1 mandó al parcial)")

modulos_js <- regmatches(TXT, gregexpr("\\{ clave: '[0-9.]+', n: [0-9]+, archivo: CAP[12],[^}]*\\}", TXT))[[1]]
comprueba(length(modulos_js) == 18L, "MODULOS_MODULO_I declara los 18 módulos con su archivo y su n",
          sprintf("%d", length(modulos_js)))
obj_modulo <- setNames(sub(".*objetivo: '(O[1-6])'.*", "\\1", modulos_js),
                       sub(".*clave: '([0-9.]+)'.*", "\\1", modulos_js))
choques <- character(0)
for (n in 1:32) {
  esperados <- unique(obj_modulo[claves_item[[n]]])
  if (!objetivo_de[n] %in% esperados)
    choques <- c(choques, sprintf("i%02d (%s pero su módulo es %s)", n, objetivo_de[n], paste(esperados, collapse = "/")))
}
comprueba(length(choques) == 0,
          "el objetivo de cada ítem coincide con el que su módulo tiene asignado en el mapa de repaso",
          paste(choques, collapse = " "))

# =====================================================================
seccion("§7 · Casi-duplicados contra los 56 ítems que el estudiante ya vio")
# =====================================================================
# D7, corregido por C7: con 56 preguntas previas y un banco que toca los
# 18 módulos, «no repetir» NO puede significar «no tocar el mismo tema»,
# porque entonces no queda tema. Lo que no se puede repetir es el
# PLANTEAMIENTO. Se mide de dos formas, porque fallan distinto: el
# solapamiento de vocabulario en trigramas ve el parecido global, y la
# tirada común de palabras ve la frase copiada dentro de un enunciado por
# lo demás distinto.

INV <- fromJSON(INVENT, simplifyVector = FALSE)
previos <- c(lapply(INV$quiz,       function(z) list(fuente = paste("quiz", z$fuente), texto = z$normalizado)),
             lapply(INV$banco,      function(z) list(fuente = paste("banco", z$etiqueta), texto = z$normalizado)),
             lapply(INV$ejercicios, function(z) list(fuente = paste("ejercicio", z$fuente), texto = z$normalizado)))
comprueba(length(previos) == 56L, "el inventario trae los 56 ítems previos (16 quiz + 32 banco + 8 ejercicios)",
          sprintf("%d", length(previos)))

# La misma normalización que `inventario_items.py`, para comparar peras
# con peras: sin marcado, sin tildes, sin signos, todo en minúsculas.
normaliza <- function(s) {
  s <- gsub("<[^>]+>", " ", s)
  s <- gsub("&nbsp;", " ", s, fixed = TRUE); s <- gsub("&amp;", "&", s, fixed = TRUE)
  s <- gsub("&lt;", "<", s, fixed = TRUE);   s <- gsub("&gt;", ">", s, fixed = TRUE)
  s <- gsub("\\\\'", "'", s); s <- gsub('\\\\"', '"', s)
  s <- tolower(s)
  for (k in seq_along(c("á","é","í","ó","ú","ü","ñ")))
    s <- gsub(c("á","é","í","ó","ú","ü","ñ")[k], c("a","e","i","o","u","u","n")[k], s, fixed = TRUE)
  s <- gsub("[^a-z0-9 ]+", " ", s)
  trimws(gsub("\\s+", " ", s))
}
palabras   <- function(s) strsplit(normaliza(s), " ", fixed = TRUE)[[1]]
trigramas  <- function(w) if (length(w) < 3) character(0) else
  vapply(seq_len(length(w) - 2), function(i) paste(w[i:(i + 2)], collapse = " "), "")
jaccard <- function(a, b) {
  if (!length(a) || !length(b)) return(0)
  length(intersect(a, b)) / length(union(a, b))
}
# La tirada común más larga, por programación dinámica sobre las dos
# listas de palabras. Es lo que caza una frase pegada tal cual.
tirada_comun <- function(a, b) {
  if (!length(a) || !length(b)) return(0L)
  prev <- integer(length(b) + 1L); mejor <- 0L
  for (i in seq_along(a)) {
    act <- integer(length(b) + 1L)
    coincide <- which(b == a[i])
    for (j in coincide) { act[j + 1L] <- prev[j] + 1L; if (act[j + 1L] > mejor) mejor <- act[j + 1L] }
    prev <- act
  }
  mejor
}

UMBRAL_JACCARD <- 0.25   # ver la tabla de márgenes que imprime esta sección
UMBRAL_TIRADA  <- 8L     # ocho palabras seguidas ya es una frase, no una coincidencia

enunciado_de <- function(n) {
  s <- trozo_de_item(n)
  m <- regmatches(s, regexpr("(?<![A-Za-z])pregunta: '((\\\\'|[^'])*)'", s, perl = TRUE))
  if (!length(m)) "" else sub("^pregunta: '", "", sub("'$", "", m))
}

# Los 38 enunciados publicados: los 32 del diagnóstico y los 6 del
# simulacro. El simulacro se escribió después de todo esto, así que si no
# entrara aquí sería la única parte del instrumento sin contrastar contra
# los 56 — y el estudiante no distingue de qué bloque viene una pregunta
# que ya ha visto.
ENUNCIADOS <- c(vapply(1:32, enunciado_de, ""),
                vapply(SIM_TROZOS, function(s) {
                  m <- regmatches(s, regexpr("(?<![A-Za-z])pregunta: '((\\\\'|[^'])*)'", s, perl = TRUE))
                  if (!length(m)) "" else sub("^pregunta: '", "", sub("'$", "", m))
                }, ""))
ETIQ <- c(sprintf("i%02d", 1:32), sprintf("S%d", 1:6))
comprueba(length(ENUNCIADOS) == 38L && all(nzchar(ENUNCIADOS)),
          "los 38 enunciados publicados entran a la comparación: 32 del diagnóstico y 6 del simulacro",
          sprintf("%d enunciados, %d no vacíos", length(ENUNCIADOS), sum(nzchar(ENUNCIADOS))))

peor <- data.frame(item = integer(0), jac = numeric(0), tir = integer(0),
                   fuente = character(0), stringsAsFactors = FALSE)
prev_pal <- lapply(previos, function(z) strsplit(z$texto, " ", fixed = TRUE)[[1]])
prev_tri <- lapply(prev_pal, trigramas)
for (n in seq_along(ENUNCIADOS)) {
  w <- palabras(ENUNCIADOS[n]); t3 <- trigramas(w)
  j <- vapply(prev_tri, function(x) jaccard(t3, x), 0)
  s <- vapply(prev_pal, function(x) as.numeric(tirada_comun(w, x)), 0)
  k <- which.max(j); kt <- which.max(s)
  peor <- rbind(peor, data.frame(item = n, jac = j[k], tir = as.integer(s[kt]),
                                 fuente = sprintf("%s / %s", previos[[k]]$fuente, previos[[kt]]$fuente),
                                 stringsAsFactors = FALSE))
}
orden <- order(-peor$jac)
cat("\n  Los seis enunciados que más se acercan a algo que el estudiante ya vio:\n")
for (r in head(orden, 6))
  cat(sprintf("    %-4s  jaccard %.3f   tirada %2d palabras   %s\n",
              ETIQ[peor$item[r]], peor$jac[r], peor$tir[r], peor$fuente[r]))

comprueba(max(peor$jac) < UMBRAL_JACCARD,
          sprintf("ningún enunciado comparte más del %.0f %% de sus trigramas con uno de los 56",
                  100 * UMBRAL_JACCARD),
          sprintf("máximo %.3f en %s", max(peor$jac), ETIQ[peor$item[which.max(peor$jac)]]))
comprueba(max(peor$tir) < UMBRAL_TIRADA,
          sprintf("ningún enunciado repite %d palabras seguidas de uno de los 56", UMBRAL_TIRADA),
          sprintf("máxima %d en %s", max(peor$tir), ETIQ[peor$item[which.max(peor$tir)]]))

# =====================================================================
if (INYECTA && !INTERNO) {
seccion("§8 · La prueba del propio verificador")
# =====================================================================
# Un verificador que nunca ha fallado no es un verificador, es un
# adorno: pasa igual de verde si comprueba algo que si no comprueba
# nada. Esto siembra cifras falsas en una copia del HTML —en
# `tempdir()`, nunca sobre el material— y exige que la sección que le
# toca las cace. Si una siembra pasa desapercibida, esa sección está
# rota aunque el resto salga en verde.

sabotea <- function(etiqueta, viejo, nuevo, seccion_esperada, fijo = TRUE) {
  copia <- file.path(tempdir(), sprintf("preparcial-saboteado-%s.html", etiqueta))
  t <- TXT
  if (!grepl(viejo, t, fixed = fijo)) {
    return(comprueba(FALSE, sprintf("siembra «%s»: el patrón existe en el HTML", etiqueta), viejo))
  }
  t <- sub(viejo, nuevo, t, fixed = fijo)
  writeLines(t, copia, useBytes = TRUE)
  salida <- suppressWarnings(system2(
    file.path(R.home("bin"), "Rscript"),
    args = c(shQuote(file.path("precalculo", "verifica_preparcial.R")), "--interno"),
    env = c(sprintf("PREPARCIAL_HTML_INYECTADO=%s", copia), "LC_ALL=en_US.UTF-8"),
    stdout = TRUE, stderr = TRUE))
  codigo <- attr(salida, "status")
  linea <- grep("^SECCIONES_CON_FALLO:", salida, value = TRUE)
  cazadas <- if (length(linea)) strsplit(trimws(sub("^SECCIONES_CON_FALLO:", "", linea[1])), " +")[[1]] else character(0)
  unlink(copia)
  comprueba(!is.null(codigo) && codigo != 0 && seccion_esperada %in% cazadas,
            sprintf("siembra «%s» -> la §%s la caza", etiqueta, seccion_esperada),
            sprintf("salida %s · secciones que fallaron: %s",
                    if (is.null(codigo)) "0" else as.character(codigo),
                    if (length(cazadas)) paste(cazadas, collapse = ",") else "ninguna"))
}

# (1) Una cifra del precálculo, cambiada dentro del bloque incrustado.
#     Es el desfase que ya ocurrió una vez: el archivo se sigue leyendo
#     perfectamente y el gráfico sale mal. Tiene que caerse el ancla §1
#     y tiene que caerse la §3, que es la que de verdad la recalcula.
sabotea("acf-del-item-14", '"observadas_fuera":1', '"observadas_fuera":3', "3")
sabotea("estadistico-adf", '"estadistico":-1.8708', '"estadistico":-1.9708', "3")

# (2) Una cifra de la PROSA, cambiada sin tocar el precálculo. El JSON
#     queda impecable, el hash cuadra y §3 pasa: solo la §4 puede verlo.
sabotea("cifra-inventada-en-la-retro", "Numerador $-17.78$", "Numerador $-17.99$", "4")
sabotea("indice-estacional-en-el-enunciado", "<strong>9.5724</strong> (T3)", "<strong>9.5824</strong> (T3)", "4")

# (3) Una tolerancia ensanchada hasta admitir el error que la retro
#     nombra. Nada más cambia: la clave sigue siendo correcta.
sabotea("tolerancia-que-lo-admite-todo", "respuesta: -0.5333, tolerancia: 0.006",
        "respuesta: -0.5333, tolerancia: 0.2", "5")

# (4) El reparto de la tabla de especificaciones, descuadrado.
sabotea("peso-de-un-objetivo", "ordenar el pipeline', peso: 10 }",
        "ordenar el pipeline', peso: 15 }", "6")

# (5) Los argumentos de `dibujar`, que son la tercera superficie: ni JSON
#     ni prosa. Las tres siembras son los tres defectos que de verdad
#     aparecieron o pudieron aparecer en este archivo.
#     a) el hallazgo 0 tal cual: la `n` del correlograma, escrita a mano.
sabotea("banda-escrita-a-mano", "correlograma(c, D.i19.acf, D.i19.banda)",
        "correlograma(c, D.i19.acf, 120)", "4")
#     b) la banda de OTRA serie del mismo ítem: 0.1789 sobre la ACF de
#        0.1797. Es correcta, existe en el JSON y está mal emparejada —
#        que es exactamente lo que le pasaba al ítem 19.
sabotea("banda-de-la-serie-equivocada", "correlograma(c, D.i29.despues.acf, D.i29.despues.banda)",
        "correlograma(c, D.i29.despues.acf, D.i29.antes.banda)", "4")
#     c) una ruta que no resuelve: el gráfico sale VACÍO y el archivo no
#        da ninguna señal. Le pasó al ítem 10 al quedarse atrás el bloque
#        incrustado, y hasta ahora solo se veía abriendo la página.
sabotea("ruta-de-dibujo-rota", "D.i10.ciclo_no_robusto", "D.i10.ciclo_sin_robustez", "4")

# (6) Una afirmación falsa SIN cifras dentro: el hallazgo del ítem 1, que
#     pasó 370 comprobaciones porque «plano» no es un número. Se recupera
#     la frase original y se exige que ahora sí se caiga.
sabotea("prosa-que-desmiente-al-grafico", "Correlograma sin estructura: la primera barra",
        "Correlograma plano: la primera barra", "4")

# (8) Una tilde rota, que es como se rompen de verdad: no desaparece, se
#     convierte en dos caracteres. Ya le pasó a este proyecto una vez.
sabotea("tilde-mangiada-por-el-utf8", "el último decimal en las tres",
        "el \u00c3\u00baltimo decimal en las tres", "4")
# (9) El vocabulario bifurcado a mitad del instrumento.
sabotea("rezago-que-se-vuelve-retardo", "la del rezago 17", "la del retardo 17", "4")

# (10) El simulacro, que se escribió después de todo lo demás y por eso
#      es el que más fácil se quedaría sin comprobar.
sabotea("simulacro-con-un-objetivo-repetido", "objetivo: 'O3', clave: '2.5'",
        "objetivo: 'O2', clave: '2.5'", "4")
sabotea("cifra-inventada-en-el-simulacro", "vale <strong>0.381</strong>",
        "vale <strong>0.391</strong>", "4")

# (7) Una segunda opción marcada como correcta. Prueba de extremo a
#     extremo la lectura de las opciones desde el HTML, que es de donde
#     salen el reparto de posiciones y la racha.
sabotea("dos-opciones-correctas", "así que siempre concuerdan.', correcta: false,",
        "así que siempre concuerdan.', correcta: true,", "4")
}

# =====================================================================
# Cierre
# =====================================================================
cat("\n", strrep("=", 70), "\n", sep = "")
secciones_fallo <- sort(unique(.fallos$secciones))
cat("SECCIONES_CON_FALLO:", paste(secciones_fallo, collapse = " "), "\n")

if (MARGENES && length(.margen$filas)) {
  m <- do.call(rbind, .margen$filas)
  m$holgura <- m$tol / pmax(m$brecha, 1e-300)
  m <- m[order(m$holgura), ]
  cat("\nLas diez comprobaciones numéricas con menos holgura (tol / brecha):\n")
  for (k in seq_len(min(10, nrow(m))))
    cat(sprintf("  %6.1fx   brecha %-10.3g tol %-10.3g §%s %s\n",
                m$holgura[k], m$brecha[k], m$tol[k], m$seccion[k], substr(m$que[k], 1, 60)))
}

if (length(.fallos$lista)) {
  cat("\n", length(.fallos$lista), " comprobaciones NO se sostienen:\n", sep = "")
  for (f in .fallos$lista) cat("  · ", f, "\n", sep = "")
  cat("\nVERIFICACIÓN: hay cifras que no cuadran. NO publicar hasta resolverlo.\n")
  quit(status = 1)
}
cat(sprintf("\nVERIFICACIÓN: todo en verde. %d comprobaciones, %d de ellas numéricas.\n",
            .fallos$total, length(.margen$filas)))
quit(status = 0)
