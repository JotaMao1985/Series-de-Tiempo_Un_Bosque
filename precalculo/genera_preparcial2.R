# ============================================================================
# genera_preparcial2.R — Precalculos del Preparcial del Corte II (caps. 3 y 4)
#
# Genera salidas/preparcial2_datos.json y salidas/preparcial2_datos.js con las
# series propias del preparcial y TODAS las cifras de sus 32 items de
# diagnostico y de los 6 del simulacro.
#
# Series propias, ninguna de los casos del material (Nilo, manchas solares,
# BJsales, lynx, lh, AirPassengers, TRM): sobre la serie que ya se vio en
# clase, reconocer sustituye a razonar. Los parametros teoricos tambien
# esquivan los de los ejemplos resueltos y los de los quizzes (ver la lista de
# parametros gastados en el plan).
#
# Algunas realizaciones no se calculan: se BUSCAN. Un item que ensena que la
# PACF tienta a un AR(3), o que CSS se sale de la region estacionaria, necesita
# una muestra que lo haga de verdad. Cada busqueda recorre desplazamientos de la
# semilla en orden, se queda con el primero que cumple su condicion y deja el
# desplazamiento escrito en el JSON: el guion se reproduce solo.
#
# El preparcial NO tiene nota: no hay clave oculta ni reparto por documento.
# Lo que si se mantiene es que ninguna cifra de la pantalla se escriba a mano.
#
# Dependencias: jsonlite, tseries, forecast.
# Uso:  LC_ALL=en_US.UTF-8 Rscript genera_preparcial2.R   (desde precalculo/)
# ============================================================================

suppressMessages({
  library(jsonlite)
  library(tseries)
  library(forecast)
})

invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "en_US.UTF-8")))
if (!isTRUE(l10n_info()$"UTF-8")) {
  warning("Sin configuracion regional UTF-8: las tildes del JSON saldran mal. ",
          "Ejecuta con LC_ALL=en_US.UTF-8 Rscript ...")
}

args_dir <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1]))
if (is.na(args_dir) || args_dir == "") args_dir <- "."
dir_salidas <- file.path(args_dir, "salidas")
stopifnot(dir.exists(dir_salidas))

# La semilla es la fecha del Parcial 2. Cambiarla cambia todas las cifras.
SEMILLA <- 20261013

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

r4 <- function(x, k = 4) round(as.numeric(x), k)
banda <- function(n) 1.96 / sqrt(n)
acf_v  <- function(x, k = 20) as.numeric(acf(x, lag.max = k, plot = FALSE)$acf)[-1]
pacf_v <- function(x, k = 20) as.numeric(pacf(x, lag.max = k, plot = FALSE)$acf)

# AICc y BIC como los escribe el material: k incluye sigma^2, n* = n - d.
aicc <- function(f, n_ef) { k <- length(f$coef) + 1; f$aic + 2 * k * (k + 1) / (n_ef - k - 1) }
bic  <- function(f, n_ef) { k <- length(f$coef) + 1; f$aic - 2 * k + log(n_ef) * k }

min_raiz <- function(f, p, q) {
  cf <- coef(f)
  ar <- if (p > 0) cf[paste0("ar", 1:p)] else NULL
  ma <- if (q > 0) cf[paste0("ma", 1:q)] else NULL
  c(ar = if (p > 0) min(Mod(polyroot(c(1, -ar)))) else NA,
    ma = if (q > 0) min(Mod(polyroot(c(1, ma)))) else NA)
}

salida <- function(obj) paste(capture.output(print(obj)), collapse = "\n")

serie_json <- function(x, nombre, descripcion, unidad, dec = 2) {
  list(nombre = nombre, descripcion = descripcion, unidad = unidad,
       frecuencia = frequency(x), inicio = as.numeric(start(x)),
       n = length(x), valores = round(as.numeric(x), dec))
}

# Busca el primer desplazamiento de la semilla que cumple `cumple`. `genera`
# recibe la semilla ya fijada y devuelve lo que `cumple` examina.
busca <- function(base, genera, cumple, tope = 20000) {
  for (o in seq_len(tope)) {
    set.seed(SEMILLA + base + o)
    x <- suppressWarnings(genera())
    ok <- tryCatch(isTRUE(suppressWarnings(cumple(x))), error = function(e) FALSE)
    if (ok) return(list(desplazamiento = base + o, x = x))
  }
  stop("La busqueda con base ", base, " no encontro ninguna realizacion")
}

items  <- list()
series <- list()

# ===========================================================================
# O1 · Operador B, estacionariedad e invertibilidad (3.1, 3.2, 3.3)
# ===========================================================================

# --- i01 · 3.1 · P · (1 - 0.8B)(1 + 0.5B) y_t = e_t, coeficiente de y_{t-2}
f1 <- c(0.8, -0.5)                         # los dos factores (1 - aB)
pol <- c(1, -(f1[1] + f1[2]), f1[1] * f1[2])  # 1 - (a+b)B + ab B^2
items$i01 <- list(
  factores = c(0.8, 0.5),                  # se escriben (1 - 0.8B)(1 + 0.5B)
  polinomio = pol,                         # 1 - 0.3B - 0.4B^2
  phi = -pol[-1],                          # phi1 = 0.3, phi2 = 0.4
  raices = r4(sort(Re(polyroot(pol)))),    # -2 y 1.25
  triangulo = c(suma = sum(-pol[-1]), resta = -pol[3] - (-pol[2]))
)

# --- i02 · 3.2 · G · ACF teorica de un AR(2) con raices complejas
phi02 <- c(1.0, -0.6)
items$i02 <- list(
  phi = phi02,
  acf = r4(ARMAacf(ar = phi02, lag.max = 20)[-1]),
  discriminante = phi02[1]^2 + 4 * phi02[2],
  modulo = r4(min(Mod(polyroot(c(1, -phi02))))),
  periodo = r4(2 * pi / acos(phi02[1] / (2 * sqrt(-phi02[2]))), 2),
  # Las otras tres opciones: raices reales con phi2 < 0, el mismo par con phi1
  # negativo (oscila rapido y arranca en negativo) y uno fuera del triangulo.
  alternativas = list(
    reales   = list(phi = c(1.0, -0.2), discriminante = 1.0^2 + 4 * -0.2,
                    acf = r4(ARMAacf(ar = c(1.0, -0.2), lag.max = 6)[-1])),
    negativo = list(phi = c(-1.0, -0.6),
                    acf = r4(ARMAacf(ar = c(-1.0, -0.6), lag.max = 6)[-1]),
                    periodo = r4(2 * pi / acos(-1.0 / (2 * sqrt(0.6))), 2)),
    fuera    = list(phi = c(1.0, -1.1))
  )
)

# --- i03 · 3.3 · P · rho_1 de un MA(2) con theta = (-0.5, 0.3)
th03 <- c(-0.5, 0.3)
den03 <- 1 + sum(th03^2)
items$i03 <- list(
  theta = th03, denominador = den03,
  rho1 = r4((th03[1] + th03[1] * th03[2]) / den03),
  rho2 = r4(th03[2] / den03),
  rho1_sin_producto = r4(th03[1] / den03),             # olvidar theta1*theta2
  rho1_sin_theta2 = r4((th03[1] + th03[1] * th03[2]) / (1 + th03[1]^2)),
  acf_R = r4(ARMAacf(ma = th03, lag.max = 3)[-1]),
  invertible = all(Mod(polyroot(c(1, th03))) > 1),
  modulos = r4(Mod(polyroot(c(1, th03))))
)

# --- i04 · 3.3 · I · theta y 1/theta con sigma^2 reescalado
set.seed(SEMILLA + 4)
y04 <- arima.sim(list(ma = 0.57), n = 200, sd = 1)
f04 <- arima(y04, order = c(0, 0, 1), include.mean = FALSE, method = "ML")
th04 <- unname(coef(f04)["ma1"]); s04 <- f04$sigma2
items$i04 <- list(
  theta_R = r4(th04), sigma2_R = r4(s04),
  theta_otro = r4(1 / th04), sigma2_otro = r4(s04 * th04^2),
  rho1_R = r4(th04 / (1 + th04^2)),
  rho1_otro = r4((1 / th04) / (1 + (1 / th04)^2)),
  gamma0_R = r4(s04 * (1 + th04^2)),
  gamma0_otro = r4(s04 * th04^2 * (1 + 1 / th04^2)),
  raiz_R = r4(1 / th04), raiz_otro = r4(th04)
)

# --- i05 · 3.1 · C · convenio de resta: theta = 0.45 en el libro
items$i05 <- list(
  theta_libro = 0.45, theta_R = -0.45,
  rho1 = r4(-0.45 / (1 + 0.45^2))
)

# ===========================================================================
# O2 · Momentos, psi/pi e identificacion (3.4, 3.5, 3.6)
# ===========================================================================

# --- i06 · 3.4 · P · techo del intervalo de un ARMA(1,1): 1.96 sqrt(gamma0)
ph06 <- 0.6; th06 <- -0.3; s2_06 <- 4
g0_06 <- s2_06 * (1 + 2 * ph06 * th06 + th06^2) / (1 - ph06^2)
psi06 <- ARMAtoMA(ar = ph06, ma = th06, lag.max = 2000)
items$i06 <- list(
  phi = ph06, theta = th06, sigma2 = s2_06,
  numerador = 1 + 2 * ph06 * th06 + th06^2,
  gamma0 = r4(g0_06),
  gamma0_psi = r4(s2_06 * (1 + sum(psi06^2))),
  semiancho = r4(1.96 * sqrt(g0_06)),
  semiancho_h1 = r4(1.96 * sqrt(s2_06)),
  semiancho_signo = r4(1.96 * sqrt(s2_06 * (1 + 2 * ph06 * -th06 + th06^2) / (1 - ph06^2))),
  semiancho_sin_raiz = r4(1.96 * g0_06),
  psi = r4(psi06[1:5])
)

# --- i07 · 3.5 · G · ARMA(1,1) muestral cuya PACF tienta a un AR(3)
b07 <- busca(400000,
  function() round(60 + arima.sim(list(ar = 0.85, ma = -0.5), n = 200, sd = 2), 2),
  function(y) {
    a <- acf_v(y); p <- pacf_v(y); b <- banda(200)
    all(abs(p[1:3]) > b) && all(abs(p[4:20]) < b * 0.95) &&
      p[1] > p[2] && p[2] > p[3] && p[3] > 0 && all(a[1:6] > b)
  })
y07 <- ts(b07$x)
fits07 <- list(ar3 = arima(y07, order = c(3, 0, 0), method = "ML"),
               arma11 = arima(y07, order = c(1, 0, 1), method = "ML"),
               ar1 = arima(y07, order = c(1, 0, 0), method = "ML"))
series$humedad <- serie_json(y07, "Humedad del suelo",
  "Doscientas lecturas diarias de humedad del suelo en una parcela", "%")
items$i07 <- list(
  desplazamiento = b07$desplazamiento, n = 200, banda = r4(banda(200), 3),
  acf = r4(acf_v(y07), 3), pacf = r4(pacf_v(y07), 3),
  aicc = lapply(fits07, function(f) r4(aicc(f, 200), 2)),
  bic = lapply(fits07, function(f) r4(bic(f, 200), 2)),
  coef_arma11 = r4(coef(fits07$arma11)), coef_ar3 = r4(coef(fits07$ar3))
)

# --- i08 · 3.6 · G · MA(1) muestral con una barra suelta lejos
b08 <- busca(500000,
  function() round(12 + arima.sim(list(ma = 0.55), n = 100, sd = 1), 3),
  function(y) {
    a <- acf_v(y); b <- banda(100); f <- which(abs(a) > b); p <- pacf_v(y)
    otros <- setdiff(1:20, f)
    length(f) == 2 && f[1] == 1 && f[2] >= 9 && a[1] > 0.33 &&
      all(abs(a[otros]) < 0.85 * b) && abs(a[f[2]]) > 1.08 * b && p[2] < -b
  })
y08 <- ts(b08$x)
a08 <- acf_v(y08)
series$errores_sensor <- serie_json(y08, "Error de un sensor",
  "Cien lecturas del error de calibración de un sensor de temperatura", "décimas de grado", 3)
items$i08 <- list(
  desplazamiento = b08$desplazamiento, n = 100, banda = r4(banda(100), 3),
  acf = r4(a08, 3), pacf = r4(pacf_v(y08), 3),
  fuera = which(abs(a08) > banda(100)),
  esperadas = 20 * 0.05,
  rho1_teorico = r4(0.55 / (1 + 0.55^2))
)

# --- i09 · 3.5 · C · factor comun: (1-0.5B)(1-0.3B) y = (1-0.5B) e
items$i09 <- list(
  phi = c(0.8, -0.15), theta = -0.5,
  factores_ar = r4(sort(1 / Re(polyroot(c(1, -0.8, 0.15))))),   # 0.3 y 0.5
  raiz_ma = r4(-1 / -0.5),                                      # B = 2
  resultado_phi = 0.3
)

# --- i10 · 3.4 · P · de los psi de un ARMA(1,1) a theta
ph10 <- 0.9; th10 <- -0.7
psi10 <- ARMAtoMA(ar = ph10, ma = th10, lag.max = 4)
items$i10 <- list(
  psi = r4(psi10), phi = ph10, theta = th10,
  cociente = r4(psi10[2] / psi10[1])
)

# ===========================================================================
# O3 · Estimar, comparar y diagnosticar un ARMA (3.7, 3.8, 3.9, 3.10)
# ===========================================================================

# --- i11 · 3.7 · P · sigma^2 de Yule-Walker del AR(1)
set.seed(SEMILLA + 11)
y11 <- ts(round(45 + arima.sim(list(ar = 0.65), n = 90, sd = 3), 2))
g11 <- acf(y11, lag.max = 1, type = "covariance", plot = FALSE)$acf
g0_11 <- round(g11[1], 2); r1_11 <- round(g11[2] / g11[1], 3)
yw11 <- ar(y11, order.max = 1, aic = FALSE, method = "yule-walker")
series$vibracion <- serie_json(y11, "Vibración de un motor",
  "Noventa mediciones de la vibración de un motor eléctrico", "mm/s")
items$i11 <- list(
  n = 90, gamma0 = g0_11, r1 = r1_11,
  sigma2 = r4(g0_11 * (1 - r1_11^2)),
  sigma2_sin_cuadrado = r4(g0_11 * (1 - r1_11)),
  sigma2_al_reves = r4(g0_11 * r1_11^2),
  phi_yw = r4(yw11$ar), sigma2_ar_R = r4(yw11$var.pred),
  correccion = r4(90 / (90 - 2))
)

# --- i12 · 3.8 · P · Q(4) de Ljung-Box a mano
b12 <- busca(700000,
  function() 20 + arima.sim(list(ar = c(0.6, 0, 0.2), ma = 0.3), n = 100, sd = 1),
  function(y) {
    f <- arima(y, order = c(1, 0, 1), method = "ML")
    r <- round(acf_v(residuals(f), 4), 3)
    Q <- 100 * 102 * sum(r^2 / (100 - 1:4))
    Q > 6.6 && Q < 8.9 && all(abs(r) < banda(100))
  })
f12 <- arima(b12$x, order = c(1, 0, 1), method = "ML")
r12 <- round(acf_v(residuals(f12), 4), 3)
Q12 <- 100 * 102 * sum(r12^2 / (100 - 1:4))
items$i12 <- list(
  desplazamiento = b12$desplazamiento, n = 100, r = r12,
  Q = r4(Q12), Q_box_pierce = r4(100 * sum(r12^2)),
  Q_R = r4(Box.test(residuals(f12), lag = 4, type = "Ljung-Box", fitdf = 2)$statistic),
  p_R = r4(Box.test(residuals(f12), lag = 4, type = "Ljung-Box", fitdf = 2)$p.value),
  critico_gl2 = r4(qchisq(0.95, 2), 3), critico_gl4 = r4(qchisq(0.95, 4), 3),
  terminos = r4(r12^2 / (100 - 1:4), 6)
)

# --- i13 · 3.7 · I · CSS fuera de la region estacionaria
b13 <- busca(0,
  function() round(50 + arima.sim(list(ar = 0.96), n = 35, sd = 2), 2),
  function(y) {
    css <- arima(y, order = c(1, 0, 0), method = "CSS")
    ml  <- arima(y, order = c(1, 0, 0), method = "ML")
    coef(css)[1] >= 1.005 && coef(ml)[1] < 0.99 && coef(ml)[1] > 0.9
  })
y13 <- ts(b13$x)
css13 <- arima(y13, order = c(1, 0, 0), method = "CSS")
ml13  <- arima(y13, order = c(1, 0, 0), method = "ML")
yw13  <- ar(y13, order.max = 1, aic = FALSE, method = "yule-walker")
series$nivel_tanque <- serie_json(y13, "Nivel de un tanque",
  "Treinta y cinco lecturas del nivel de un tanque de almacenamiento", "cm")
items$i13 <- list(
  desplazamiento = b13$desplazamiento, n = 35,
  css = list(phi = r4(coef(css13)[1]), se = r4(sqrt(css13$var.coef[1, 1])),
             media = r4(coef(css13)[2], 2), se_media = r4(sqrt(css13$var.coef[2, 2]), 2)),
  ml = list(phi = r4(coef(ml13)[1]), se = r4(sqrt(ml13$var.coef[1, 1])),
            media = r4(coef(ml13)[2], 2), se_media = r4(sqrt(ml13$var.coef[2, 2]), 2)),
  yw = list(phi = r4(yw13$ar)),
  distancia_ml_yw_ee = r4((coef(ml13)[1] - yw13$ar) / sqrt(ml13$var.coef[1, 1]), 2),
  media_muestral = r4(mean(y13), 2),
  por_defecto = tryCatch({ arima(y13, order = c(1, 0, 0)); "sin error" },
                         error = function(e) conditionMessage(e))
)

# --- i14 · 3.9 · I · rendimientos: no hay nada que modelar
b14 <- busca(100000,
  function() round(0.6 + arima.sim(list(ma = 0.12), n = 120, sd = 2.5), 2),
  function(r) {
    f0 <- arima(r, order = c(0, 0, 0), method = "ML")
    f1 <- arima(r, order = c(0, 0, 1), method = "ML")
    a0 <- aicc(f0, 120); a1 <- aicc(f1, 120)
    t1 <- coef(f1)[1] / sqrt(f1$var.coef[1, 1])
    lb <- Box.test(r, lag = 12, type = "Ljung-Box")$p.value
    a1 < a0 && a0 - a1 > 0.05 && a0 - a1 < 0.4 && abs(t1) > 1.1 && abs(t1) < 1.6 &&
      lb > 0.3 && sum(abs(acf_v(r)) > banda(120)) == 1
  })
y14 <- ts(b14$x)
f14_0 <- arima(y14, order = c(0, 0, 0), method = "ML")
f14_1 <- arima(y14, order = c(0, 0, 1), method = "ML")
a14 <- acf_v(y14)
series$rendimientos <- serie_json(y14, "Rendimiento mensual de un fondo",
  "Ciento veinte rendimientos mensuales de un fondo de inversión", "%")
items$i14 <- list(
  desplazamiento = b14$desplazamiento, n = 120, banda = r4(banda(120), 3),
  acf = r4(a14, 3), fuera = which(abs(a14) > banda(120)),
  ma1 = r4(coef(f14_1)["ma1"]), se_ma1 = r4(sqrt(f14_1$var.coef[1, 1])),
  t_ma1 = r4(coef(f14_1)["ma1"] / sqrt(f14_1$var.coef[1, 1]), 2),
  aicc_rb = r4(aicc(f14_0, 120), 2), aicc_ma1 = r4(aicc(f14_1, 120), 2),
  dif_aicc = r4(aicc(f14_0, 120) - aicc(f14_1, 120), 2),
  bic_rb = r4(bic(f14_0, 120), 2), bic_ma1 = r4(bic(f14_1, 120), 2),
  lb12 = r4(Box.test(y14, lag = 12, type = "Ljung-Box")$p.value),
  media = r4(coef(f14_0)["intercept"]), se_media = r4(sqrt(f14_0$var.coef[1, 1]))
)

# --- i15 · 3.10 · C · AR(2) frente a una red: solo cuenta parametros
items$i15 <- list(n = 90, parametros_ar2 = 4)

# --- i16 · 3.8 · G · Ljung-Box conjunto rechaza con todas las barras dentro
b16 <- busca(200000,
  function() round(30 + arima.sim(list(ar = c(0.55, 0, 0.17, 0.12)), n = 150, sd = 1.5), 2),
  function(y) {
    e <- residuals(arima(y, order = c(1, 0, 0), method = "ML"))
    if (any(abs(acf_v(e)) >= banda(150) * 0.97)) return(FALSE)
    p <- sapply(2:20, function(h) Box.test(e, lag = h, type = "Ljung-Box", fitdf = 1)$p.value)
    sum(p < 0.05) >= 8 && min(p) < 0.02
  })
y16 <- ts(b16$x)
f16 <- arima(y16, order = c(1, 0, 0), method = "ML")
e16 <- residuals(f16)
p16 <- sapply(2:20, function(h) Box.test(e16, lag = h, type = "Ljung-Box", fitdf = 1)$p.value)
f16b <- arima(y16, order = c(3, 0, 0), method = "ML")
p16b <- sapply(4:20, function(h) Box.test(residuals(f16b), lag = h, type = "Ljung-Box", fitdf = 3)$p.value)
series$trafico <- serie_json(y16, "Tráfico de una red",
  "Ciento cincuenta mediciones del tráfico de una red de datos", "Mb/s")
items$i16 <- list(
  desplazamiento = b16$desplazamiento, n = 150, banda = r4(banda(150), 3),
  phi = r4(coef(f16)["ar1"]),
  acf_res = r4(acf_v(e16), 3), max_acf = r4(max(abs(acf_v(e16))), 3),
  rezago_max = which.max(abs(acf_v(e16))),
  rezagos_lb = 2:20, p_lb = r4(p16),
  rechaza_hasta = max(which(p16 < 0.05)) + 1,
  p_lb20 = r4(p16[length(p16)]),
  ar3 = list(coef = r4(coef(f16b)[1:3]), p_min = r4(min(p16b)),
             aicc = r4(aicc(f16b, 150), 2)),
  aicc_ar1 = r4(aicc(f16, 150), 2)
)

# ===========================================================================
# O4 · De ARMA a ARIMA: d y la constante (4.1, 4.3, 4.5)
# ===========================================================================

# --- i17 · 4.1 · P · IMA(1,1) = SES: alfa = 1 + theta y el siguiente pronostico
set.seed(SEMILLA + 17)
y17 <- ts(round(300 + cumsum(arima.sim(list(ma = -0.6), n = 104, sd = 5)), 2), frequency = 52, start = c(2024, 1))
f17 <- Arima(y17, order = c(0, 1, 1))
th17 <- r4(coef(f17)["ma1"]); yT17 <- round(as.numeric(tail(y17, 1)), 2)
yhat17 <- round(as.numeric(tail(fitted(f17), 1)), 2)
al17 <- 1 + th17
items$i17 <- list(
  theta = th17, alfa = al17, yT = yT17, yhat_T = yhat17,
  pronostico = r4(al17 * yT17 + (1 - al17) * yhat17, 2),
  pronostico_R = r4(forecast(f17, h = 1)$mean[1], 2),
  pronostico_alfa_theta = r4(-th17 * yT17 + (1 + th17) * yhat17, 2),   # alfa = -theta
  pronostico_al_reves = r4((1 - al17) * yT17 + al17 * yhat17, 2)
)
series$ventas_semanales <- serie_json(y17, "Ventas semanales",
  "Dos años de ventas semanales de una tienda", "unidades")

# --- i18 · 4.3 (+4.8) · I · la varianza cae al diferenciar una serie estacionaria
b18 <- busca(1000000,
  function() round(400 + arima.sim(list(ar = c(1.1, -0.5)), n = 150, sd = 10), 2),
  function(y) {
    v <- c(var(y), var(diff(y)), var(diff(y, differences = 2)))
    v[2] < v[1] && v[3] > v[2] && adf.test(y)$p.value < 0.05 && kpss.test(y)$p.value >= 0.1
  })
y18 <- ts(b18$x)
v18 <- c(var(y18), var(diff(y18)), var(diff(y18, differences = 2)))
r1_18 <- acf_v(y18, 1)
adf18 <- suppressWarnings(adf.test(y18)); kpss18 <- suppressWarnings(kpss.test(y18))
f18 <- arima(y18, order = c(2, 0, 0), method = "ML")
series$pedidos <- serie_json(y18, "Pedidos semanales",
  "Ciento cincuenta semanas de pedidos de un distribuidor, con un ciclo de unas nueve semanas", "pedidos")
items$i18 <- list(
  desplazamiento = b18$desplazamiento, n = 150,
  varianzas = r4(v18, 2), razon = r4(v18[2] / v18[1]),
  r1 = r4(r1_18, 3), razon_teorica = r4(2 * (1 - round(r1_18, 3))),
  adf = list(estadistico = r4(adf18$statistic, 3), p = r4(adf18$p.value),
             fuera_tabla = adf18$p.value <= 0.01),
  kpss = list(estadistico = r4(kpss18$statistic, 3), p = r4(kpss18$p.value),
              fuera_tabla = kpss18$p.value >= 0.1),
  ndiffs = ndiffs(y18), ndiffs_adf = ndiffs(y18, test = "adf"),
  ar2 = list(coef = r4(coef(f18)[1:2]), modulo = r4(min(Mod(polyroot(c(1, -coef(f18)[1:2])))))),
  periodo = r4(2 * pi / acos(coef(f18)[1] / (2 * sqrt(-coef(f18)[2]))), 2)
)

# --- i19 · 4.5 · P · deriva de una caminata desde los extremos
set.seed(SEMILLA + 19)
y19 <- ts(round(350 + cumsum(c(0, 2.4 + rnorm(59, 0, 6))), 1), frequency = 12, start = c(2021, 7))
f19 <- Arima(y19, order = c(0, 1, 0), include.drift = TRUE)
y1_19 <- round(y19[1], 1); yn_19 <- round(y19[60], 1)
items$i19 <- list(
  n = 60, y1 = y1_19, yn = yn_19,
  deriva = r4((yn_19 - y1_19) / 59),
  deriva_n = r4((yn_19 - y1_19) / 60),
  deriva_R = r4(coef(f19)["drift"]), se_R = r4(sqrt(f19$var.coef[1, 1])),
  pronostico_12 = r4(yn_19 + 12 * (yn_19 - y1_19) / 59, 1)
)
series$suscriptores <- serie_json(y19, "Suscriptores de un servicio",
  "Cinco años de suscriptores mensuales de un servicio digital", "miles", 1)

# --- i20 · 4.5 · I · Arima(1,1,0) con deriva: la pendiente es la deriva, no c
set.seed(SEMILLA + 20)
w20 <- 1.8 + arima.sim(list(ar = 0.35), n = 99, sd = 1.5)
y20 <- ts(round(1200 + cumsum(c(0, w20)), 1), frequency = 1, start = 1926)
f20 <- Arima(y20, order = c(1, 1, 0), include.drift = TRUE)
f20$series <- "matriculas"
ph20 <- unname(coef(f20)["ar1"]); de20 <- unname(coef(f20)["drift"])
fc20 <- forecast(f20, h = 60)
items$i20 <- list(
  salida = salida(f20),
  phi = r4(ph20), deriva = r4(de20),
  se_deriva = r4(sqrt(f20$var.coef["drift", "drift"])),
  t_deriva = r4(de20 / sqrt(f20$var.coef["drift", "drift"]), 2),
  c = r4(de20 * (1 - ph20)),
  deriva_sobre = r4(de20 / (1 - ph20)),
  phi_por_deriva = r4(ph20 * de20),
  pendiente_final = r4(diff(fc20$mean)[59]),
  pendientes_iniciales = r4(diff(c(tail(y20, 1), fc20$mean))[1:4])
)
series$matriculas <- serie_json(y20, "Matrículas en una universidad",
  "Cien años de matrículas anuales de una universidad pública", "estudiantes", 1)

# --- i21 · 4.1 (+4.2) · I · AR(2) en niveles con una raiz casi unitaria
b21 <- busca(800000,
  function() { w <- arima.sim(list(ar = 0.35), n = 119, sd = 4); round(800 + cumsum(c(0, w)), 2) },
  function(y) {
    f2 <- arima(y, order = c(2, 0, 0), method = "ML")
    s <- sum(coef(f2)[1:2]); r <- min(Mod(polyroot(c(1, -coef(f2)[1:2]))))
    s > 0.975 && s < 0.992 && r < 1.02
  })
y21 <- ts(b21$x)
f21 <- arima(y21, order = c(2, 0, 0), method = "ML")
f21b <- arima(y21, order = c(1, 1, 0), method = "ML")
series$cotizacion <- serie_json(y21, "Cotización de una acción",
  "Ciento veinte cierres diarios de una acción", "pesos")
items$i21 <- list(
  desplazamiento = b21$desplazamiento, n = 120,
  ar2 = list(coef = r4(coef(f21)[1:2]), se = r4(sqrt(diag(f21$var.coef))[1:2]),
             media = r4(coef(f21)[3], 2), se_media = r4(sqrt(f21$var.coef[3, 3]), 2),
             suma = r4(sum(coef(f21)[1:2])),
             raices = r4(sort(Mod(polyroot(c(1, -coef(f21)[1:2])))))),
  arima110 = list(phi = r4(coef(f21b)["ar1"]), se = r4(sqrt(f21b$var.coef[1, 1]))),
  adf_p = r4(suppressWarnings(adf.test(y21))$p.value),
  kpss_p = r4(suppressWarnings(kpss.test(y21))$p.value)
)

# ===========================================================================
# O5 · Box-Jenkins: identificar, comparar, auto.arima (4.2, 4.4, 4.6, 4.7)
# ===========================================================================

# --- i22 · 4.4 · G · ACF y PACF de la serie diferenciada de un ARIMA(2,1,0)
b22 <- busca(600000,
  function() { w <- arima.sim(list(ar = c(0.45, -0.4)), n = 159, sd = 1.2); round(500 + cumsum(c(0, w)), 2) },
  function(y) {
    dy <- diff(y); a <- acf_v(dy); p <- pacf_v(dy); b <- banda(159)
    all(abs(p[1:2]) > b) && all(abs(p[3:20]) < b * 0.95) &&
      sum(abs(a) > b) >= 2 && sum(abs(a) > b) <= 4
  })
y22 <- ts(b22$x)
dy22 <- diff(y22)
series$consumo <- serie_json(y22, "Consumo de agua",
  "Ciento sesenta días de consumo de agua de un barrio", "m3")
items$i22 <- list(
  desplazamiento = b22$desplazamiento, n = 160, n_dif = 159,
  banda = r4(banda(159), 3),
  acf_nivel = r4(acf_v(y22, 6), 3),
  acf = r4(acf_v(dy22), 3), pacf = r4(pacf_v(dy22), 3),
  coef_210 = r4(coef(arima(y22, order = c(2, 1, 0), method = "ML")))
)

# --- i23 · 4.7 · C · que hace y que no hace auto.arima (sin cifras)
items$i23 <- list(umbral_raiz = 1.01)

# --- i24 · 4.6 (+4.10) · I · rejilla: el minimo de AICc es degenerado
rejilla <- function(y, d) {
  out <- list()
  for (p in 0:2) for (q in 0:2) {
    f <- tryCatch(suppressWarnings(arima(y, order = c(p, d, q), method = "ML")),
                  error = function(e) NULL)
    if (is.null(f)) next
    r <- min_raiz(f, p, q)
    out[[length(out) + 1]] <- data.frame(p = p, d = d, q = q, n_ef = length(y) - d,
      AICc = aicc(f, length(y) - d), raiz_ar = r[["ar"]], raiz_ma = r[["ma"]])
  }
  do.call(rbind, out)
}
b24 <- busca(300000,
  function() round(200 + cumsum(rnorm(140, 0, 3)), 2),
  function(y) {
    g1 <- rejilla(y, 1); g1 <- g1[order(g1$AICc), ]
    if (!(g1$p[1] == 2 && g1$q[1] == 2 && g1$raiz_ar[1] < 1.02 && g1$raiz_ma[1] < 1.02)) return(FALSE)
    sano <- pmin(g1$raiz_ar, g1$raiz_ma, na.rm = TRUE)
    sano[is.na(sano)] <- Inf
    # Un solo degenerado, el minimo: un par AR/MA que se cancela sobre el
    # circulo, como el ARIMA(2,1,2) de la TRM. Si hubiera mas modelos con raiz
    # MA en 1, la regla del 4.2 (raiz MA en el circulo: bajar d) mandaria a
    # otro sitio y el item ensenaria otra cosa.
    if (sum(sano < 1.01) != 1) return(FALSE)
    valido <- g1[sano >= 1.01, ][1, ]
    # El mejor de los sanos es la caminata, como en la TRM del 4.10.
    if (!(valido$p == 0 && valido$q == 0)) return(FALSE)
    # Que gane por algo mas que un empate (1.5) y por menos de lo que haria
    # pensar en una estructura real que la rejilla no recoge (5).
    gana <- valido$AICc - g1$AICc[1]
    if (gana < 1.5 || gana > 5) return(FALSE)
    # Sin deriva que valga la pena: con ella, la caminata dejaria de ser la
    # respuesta y la rejilla sin constante no contaria toda la historia.
    fd <- Arima(y, order = c(0, 1, 0), include.drift = TRUE)
    if (abs(coef(fd)["drift"] / sqrt(fd$var.coef[1, 1])) >= 1) return(FALSE)
    # Y que la caminata que el ítem da por buena PASE su propio diagnóstico: si
    # la realización trae por azar un ciclo que Ljung–Box detecta, «no hay
    # señal» sería falso y el (2,1,2) estaría persiguiendo algo real (lo cazó la
    # revisión adversarial del 2026-10-05 en la primera realización).
    dy <- diff(y)
    Box.test(dy, lag = 10, type = "Ljung-Box")$p.value > 0.15 &&
      Box.test(dy, lag = 20, type = "Ljung-Box")$p.value > 0.15 &&
      sum(abs(acf_v(dy, 24)) > banda(length(dy))) <= 1
  }, tope = 6000)
y24 <- ts(b24$x)
g24_1 <- rejilla(y24, 1); g24_1 <- g24_1[order(g24_1$AICc), ]
f24 <- suppressWarnings(arima(y24, order = c(2, 1, 2), method = "ML"))
series$exportaciones <- serie_json(y24, "Exportaciones mensuales",
  "Ciento cuarenta meses de exportaciones de un producto agrícola", "miles de toneladas")
# Si la raíz más cercana al círculo es de un par complejo: la tabla lo marca,
# porque la regla del 4.2 (raíz AR real en B = 1: subir d) no vale para un ciclo.
compleja <- function(y, p, d, q, que) {
  if ((que == "ar" && p == 0) || (que == "ma" && q == 0)) return(NA)
  f <- suppressWarnings(arima(y, order = c(p, d, q), method = "ML"))
  cf <- coef(f)
  z <- if (que == "ar") polyroot(c(1, -cf[paste0("ar", 1:p)])) else polyroot(c(1, cf[paste0("ma", 1:q)]))
  abs(Im(z[which.min(Mod(z))])) > 1e-6
}
fila <- function(g, i) list(p = g$p[i], d = g$d[i], q = g$q[i], n_ef = g$n_ef[i],
                            ar_compleja = compleja(y24, g$p[i], 1, g$q[i], "ar"),
                            ma_compleja = compleja(y24, g$p[i], 1, g$q[i], "ma"),
                            AICc = r4(g$AICc[i], 2),
                            raiz_ar = if (is.na(g$raiz_ar[i])) NULL else r4(g$raiz_ar[i]),
                            raiz_ma = if (is.na(g$raiz_ma[i])) NULL else r4(g$raiz_ma[i]))
items$i24 <- list(
  desplazamiento = b24$desplazamiento, n = 140,
  d1 = lapply(seq_len(nrow(g24_1)), function(i) fila(g24_1, i)),
  coef_212 = r4(coef(f24), 3),
  raices_ar_212 = local({ z <- polyroot(c(1, -coef(f24)[1:2]))
    list(compleja = abs(Im(z[1])) > 1e-6, modulo = r4(Mod(z[1])),
         periodo = r4(2 * pi / abs(Arg(z[1])), 1)) }),
  lb_caminata = local({ dy <- diff(y24)
    list(p10 = r4(Box.test(dy, lag = 10, type = "Ljung-Box")$p.value, 3),
         p20 = r4(Box.test(dy, lag = 20, type = "Ljung-Box")$p.value, 3),
         fuera24 = sum(abs(acf_v(dy, 24)) > banda(length(dy)))) }),
  auto = paste(arimaorder(auto.arima(y24)), collapse = ","),
  deriva = local({ fd <- Arima(y24, order = c(0, 1, 0), include.drift = TRUE)
    list(valor = r4(coef(fd)["drift"]), t = r4(coef(fd)["drift"] / sqrt(fd$var.coef[1, 1]), 2)) })
)

# --- i25 · 4.6 · P · AICc a mano de un ARIMA(1,1,1) con deriva
set.seed(SEMILLA + 25)
y25 <- ts(round(5000 + cumsum(c(0, 12 + arima.sim(list(ar = 0.5, ma = -0.2), n = 119, sd = 40))), 1))
f25 <- Arima(y25, order = c(1, 1, 1), include.drift = TRUE)
ll25 <- round(as.numeric(logLik(f25)), 2)
k25 <- length(coef(f25)) + 1; n25 <- 119
items$i25 <- list(
  n = 120, n_ef = n25, logL = ll25, k = k25,
  aicc = r4(-2 * ll25 + 2 * k25 + 2 * k25 * (k25 + 1) / (n25 - k25 - 1), 2),
  aicc_R = r4(f25$aicc, 2),
  aicc_k_menos_1 = r4(-2 * ll25 + 2 * (k25 - 1) + 2 * (k25 - 1) * k25 / (n25 - k25), 2),
  aicc_con_n = r4(-2 * ll25 + 2 * k25 + 2 * k25 * (k25 + 1) / (120 - k25 - 1), 2),
  aic = r4(-2 * ll25 + 2 * k25, 2)
)
series$turistas <- serie_json(y25, "Llegadas de turistas",
  "Ciento veinte meses de llegadas de turistas a una ciudad", "personas", 1)

# --- i26 · 4.2 · C · tres sintomas, tres vueltas atras (sin cifras propias)
items$i26 <- list(raiz_ma = 1.002, raiz_ar = 1.006)

# ===========================================================================
# O6 · Diagnosticar y pronosticar un ARIMA (4.8, 4.9, 4.10)
# ===========================================================================

# --- i27 · 4.9 · P · pronostico a dos pasos de un ARIMA(1,1,0) a mano
set.seed(SEMILLA + 27)
y27 <- ts(round(120 + cumsum(c(0, arima.sim(list(ar = 0.45), n = 89, sd = 1.5))), 2))
f27 <- arima(y27, order = c(1, 1, 0), method = "ML")
ph27 <- r4(coef(f27)["ar1"])
yT27 <- round(y27[90], 2); yT1_27 <- round(y27[89], 2)
p1_27 <- yT27 + ph27 * (yT27 - yT1_27)
p2_27 <- p1_27 + ph27 * (p1_27 - yT27)
items$i27 <- list(
  phi = ph27, yT = yT27, yT_1 = yT1_27,
  paso1 = r4(p1_27), paso2 = r4(p2_27),
  paso2_R = r4(predict(f27, n.ahead = 2)$pred[2]),
  paso2_ar_en_niveles = r4(ph27^2 * yT27),
  paso2_sin_acumular = r4(yT27 + ph27^2 * (yT27 - yT1_27)),
  paso2_constante = r4(p1_27)
)
series$nivel_embalse <- serie_json(y27, "Nivel de un embalse",
  "Noventa días del nivel de un embalse", "metros sobre el nivel de referencia")

# --- i28 · 4.9 · P · semiancho al 95 % a h = 3 de un ARIMA(0,1,1)
set.seed(SEMILLA + 28)
y28 <- ts(round(80 + cumsum(arima.sim(list(ma = -0.45), n = 130, sd = 2.5)), 2))
f28 <- Arima(y28, order = c(0, 1, 1))
th28 <- r4(coef(f28)["ma1"]); s28 <- r4(sqrt(f28$sigma2), 3)
fc28 <- forecast(f28, h = 3, level = 95)
psi28 <- 1 + th28
items$i28 <- list(
  theta = th28, sigma = s28, psi = r4(psi28),
  suma_psi2 = r4(1 + 2 * psi28^2),
  semiancho = r4(1.96 * s28 * sqrt(1 + 2 * psi28^2)),
  semiancho_R = r4(fc28$upper[3] - fc28$mean[3]),
  semiancho_caminata = r4(1.96 * s28 * sqrt(3)),
  semiancho_psi_theta = r4(1.96 * s28 * sqrt(1 + th28^2 + th28^4)),
  semiancho_sin_psi0 = r4(1.96 * s28 * sqrt(2 * psi28^2)),
  semiancho_varianza = r4(1.96 * s28^2 * (1 + 2 * psi28^2))
)
series$visitas <- serie_json(y28, "Visitas a un sitio web",
  "Ciento treinta días de visitas a un sitio web", "miles")

# --- i29 · 4.9 (+4.5) · G · abanico de un ARIMA(0,2,1): recta y banda que crece rapido
set.seed(SEMILLA + 29)
y29 <- ts(round(1000 + 12 * (1:60) +
              cumsum(cumsum(c(0, 0, arima.sim(list(ma = -0.7), n = 58, sd = 2)))), 1))
f29 <- arima(y29, order = c(0, 2, 1), method = "ML")
fc29 <- predict(f29, n.ahead = 24)
th29 <- unname(coef(f29)["ma1"])
psi29 <- c(1, ARMAtoMA(ar = c(2, -1), ma = th29, lag.max = 23))
semi29 <- 1.96 * fc29$se
items$i29 <- list(
  theta = r4(th29), n = length(y29),
  pronostico = r4(fc29$pred, 1), semiancho = r4(semi29, 1),
  razon_24 = r4(semi29[24] / semi29[1], 2), raiz24 = r4(sqrt(24), 2),
  psi = r4(psi29[1:6]),
  pendiente = r4(diff(fc29$pred)[23], 2),
  razon_011_deriva = local({ f <- Arima(y29, order = c(0, 1, 1), include.drift = TRUE)
    s <- forecast(f, h = 24, level = 95); r4((s$upper[24] - s$mean[24]) / (s$upper[1] - s$mean[1]), 2) })
)
series$usuarios <- serie_json(y29, "Usuarios de una aplicación",
  "Sesenta meses de usuarios activos de una aplicación", "miles", 1)

# --- i30 · 4.8 · I · residuales que pasan Ljung-Box pero no la normalidad
b30 <- busca(900000,
  function() { e <- rt(220, df = 3) * 4; round(150 + stats::filter(e, 0.5, method = "recursive")[21:220], 1) },
  function(y) {
    f <- arima(y, order = c(1, 0, 0), method = "ML"); r <- residuals(f)
    lb <- Box.test(r, lag = 10, type = "Ljung-Box", fitdf = 1)$p.value
    sw <- shapiro.test(r)$p.value
    k <- mean((r - mean(r))^4) / mean((r - mean(r))^2)^2
    lb > 0.3 && sw < 0.001 && k > 5.5 && k < 9
  }, tope = 3000)
y30 <- ts(b30$x)
f30 <- arima(y30, order = c(1, 0, 0), method = "ML")
e30 <- residuals(f30); s30 <- sqrt(f30$sigma2)
series$llamadas <- serie_json(y30, "Llamadas a un centro de atención",
  "Doscientos días de llamadas atendidas por un centro de atención", "llamadas", 1)
items$i30 <- list(
  desplazamiento = b30$desplazamiento, n = 200,
  phi = r4(coef(f30)["ar1"]), media = r4(coef(f30)["intercept"], 2),
  lb10 = r4(Box.test(e30, lag = 10, type = "Ljung-Box", fitdf = 1)$p.value, 3),
  shapiro = signif(shapiro.test(e30)$p.value, 2),
  curtosis = r4(mean((e30 - mean(e30))^4) / mean((e30 - mean(e30))^2)^2, 1),
  asimetria = r4(mean((e30 - mean(e30))^3) / mean((e30 - mean(e30))^2)^1.5, 2),
  fuera = list(n80 = r4(mean(abs(e30) > qnorm(0.90) * s30), 3),
               n95 = r4(mean(abs(e30) > qnorm(0.975) * s30), 3),
               n99 = r4(mean(abs(e30) > qnorm(0.995) * s30), 3))
)

# --- i31 · 4.10 · P · intervalo del 80 % de una caminata a h = 4
set.seed(SEMILLA + 31)
y31 <- ts(round(2400 + cumsum(c(0, rnorm(149, 0, 35))), 2))
f31 <- Arima(y31, order = c(0, 1, 0))
s31 <- r4(sqrt(f31$sigma2), 2)
fc31 <- forecast(f31, h = 4, level = 80)
items$i31 <- list(
  sigma = s31, yT = r4(tail(y31, 1), 2), z80 = 1.282,
  semiancho = r4(1.282 * s31 * sqrt(4), 2),
  semiancho_R = r4(fc31$upper[4] - fc31$mean[4], 2),
  semiancho_95 = r4(1.96 * s31 * 2, 2),
  semiancho_sin_raiz = r4(1.282 * s31 * 4, 2),
  semiancho_h1 = r4(1.282 * s31, 2)
)
series$indice_bursatil <- serie_json(y31, "Índice bursátil",
  "Ciento cincuenta cierres diarios de un índice bursátil", "puntos")

# --- i32 · 4.10 · C · caminata frente a ARMA estacionario a cinco anios
s32 <- 50; ph32 <- 0.8
items$i32 <- list(
  sigma = s32, phi = ph32,
  caminata_60 = r4(1.96 * s32 * sqrt(60), 1),
  ar1_60 = r4(1.96 * s32 * sqrt((1 - ph32^120) / (1 - ph32^2)), 1),
  ar1_techo = r4(1.96 * s32 / sqrt(1 - ph32^2), 1)
)

# ===========================================================================
# Simulacro: seis items, uno por objetivo, sin cifras de los 32
# ===========================================================================
sim <- list()

# s1 · O1 · 3.2 · gamma0 de un AR(2)
ph_s1 <- c(0.6, -0.35); s2_s1 <- 2
sim$s1 <- list(phi = ph_s1, sigma2 = s2_s1,
  gamma0 = r4((1 - ph_s1[2]) * s2_s1 / ((1 + ph_s1[2]) * ((1 - ph_s1[2])^2 - ph_s1[1]^2))),
  gamma0_psi = r4(s2_s1 * (1 + sum(ARMAtoMA(ar = ph_s1, lag.max = 3000)^2))),
  gamma0_ar1 = r4(s2_s1 / (1 - ph_s1[1]^2)))

# s2 · O2 · 3.4 · pi_2 de un ARMA(1,1)
ph_s2 <- 0.5; th_s2 <- 0.4
sim$s2 <- list(phi = ph_s2, theta = th_s2,
  pi = r4(c(-(ph_s2 + th_s2), -(ph_s2 + th_s2) * (-th_s2))),
  pi_R = r4(-ARMAtoMA(ar = -th_s2, ma = -ph_s2, lag.max = 2)))

# s3 · O3 · 3.10 · el coeficiente de mayor orden no significativo
b_s3 <- busca(1100000,
  function() 25 + arima.sim(list(ar = c(0.7, -0.25)), n = 120, sd = 1.2),
  function(y) {
    f <- arima(y, order = c(3, 0, 0), method = "ML")
    t3 <- coef(f)["ar3"] / sqrt(f$var.coef[3, 3])
    abs(t3) < 1 && abs(t3) > 0.5
  })
f_s3 <- arima(b_s3$x, order = c(3, 0, 0), method = "ML")
f_s3$call <- quote(arima(x = y, order = c(3, 0, 0), method = "ML"))
f_s3b <- arima(b_s3$x, order = c(2, 0, 0), method = "ML")
sim$s3 <- list(desplazamiento = b_s3$desplazamiento, salida = salida(f_s3),
  t_ar3 = r4(coef(f_s3)["ar3"] / sqrt(f_s3$var.coef[3, 3]), 2),
  t_ar2 = r4(coef(f_s3)["ar2"] / sqrt(f_s3$var.coef[2, 2]), 2),
  aicc_ar3 = r4(aicc(f_s3, 120), 2), aicc_ar2 = r4(aicc(f_s3b, 120), 2))

# s4 · O4 · 4.5 · el pronostico de un ARIMA(1,0,1) vuelve al intercept
set.seed(SEMILLA + 104)
y_s4 <- ts(73 + arima.sim(list(ar = 0.75, ma = 0.3), n = 150, sd = 2))
f_s4 <- arima(y_s4, order = c(1, 0, 1), method = "ML")
f_s4$call <- quote(arima(x = y, order = c(1, 0, 1), method = "ML"))
sim$s4 <- list(salida = salida(f_s4),
  media = r4(coef(f_s4)["intercept"], 2),
  c = r4(coef(f_s4)["intercept"] * (1 - coef(f_s4)["ar1"]), 2),
  pronostico_200 = r4(predict(f_s4, n.ahead = 200)$pred[200], 2))

# s5 · O5 · 4.6 · BIC a mano de un ARIMA(0,1,1)
set.seed(SEMILLA + 105)
y_s5 <- ts(60 + cumsum(arima.sim(list(ma = -0.35), n = 100, sd = 1.8)))
f_s5 <- arima(y_s5, order = c(0, 1, 1), method = "ML")
ll_s5 <- round(as.numeric(logLik(f_s5)), 2)
sim$s5 <- list(n = 101, n_ef = 100, logL = ll_s5, k = 2,
  bic = r4(-2 * ll_s5 + 2 * log(100), 2),
  bic_R = r4(bic(f_s5, 100), 2),
  bic_n = r4(-2 * ll_s5 + 2 * log(101), 2),
  bic_k1 = r4(-2 * ll_s5 + 1 * log(100), 2))

# s6 · O6 · 4.9 · semiancho a h = 3 de un ARIMA(1,1,0)
ph_s6 <- 0.4; sg_s6 <- 2
psi_s6 <- c(1, (1 - ph_s6^(2:3)) / (1 - ph_s6))
sim$s6 <- list(phi = ph_s6, sigma = sg_s6, psi = r4(psi_s6),
  psi_R = r4(c(1, ARMAtoMA(ar = c(1 + ph_s6, -ph_s6), lag.max = 2))),
  semiancho = r4(1.96 * sg_s6 * sqrt(sum(psi_s6^2))),
  semiancho_ar1 = r4(1.96 * sg_s6 * sqrt(1 + ph_s6^2 + ph_s6^4)),
  semiancho_caminata = r4(1.96 * sg_s6 * sqrt(3)))

# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------
datos <- list(
  meta = list(
    semilla = SEMILLA, generado = "2026-10-05",
    r_version = R.version.string,
    paquetes = list(jsonlite = as.character(packageVersion("jsonlite")),
                    tseries = as.character(packageVersion("tseries")),
                    forecast = as.character(packageVersion("forecast"))),
    n_items = length(items), n_simulacro = length(sim),
    nota = "Preparcial del Corte II. Formativo, sin nota: no hay clave oculta."
  ),
  series = series, items = items, simulacro = sim
)

json <- toJSON(datos, auto_unbox = TRUE, digits = NA, null = "null", na = "null")
writeLines(json, file.path(dir_salidas, "preparcial2_datos.json"), useBytes = TRUE)
writeLines(paste0("const PREPARCIAL_DATOS = ", json, ";"),
           file.path(dir_salidas, "preparcial2_datos.js"), useBytes = TRUE)
cat("OK  preparcial2_datos.json:", length(items), "items,", length(sim), "del simulacro,",
    length(series), "series\n")
