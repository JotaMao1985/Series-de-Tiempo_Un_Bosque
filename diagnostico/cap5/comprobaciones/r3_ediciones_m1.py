"""R3 · Módulo 1 (5.1 La firma de la estacionalidad).

D6: el ARIMA(0,1,5) del Capítulo 4, cuyas cifras abren el capítulo, se vuelve a ajustar en el bloque
del módulo (ρ̂12, ρ̂24, Q y p); el airline se nombra con sus órdenes y con los módulos que lo escriben
(M2), lo estudian (M5) y lo diagnostican (M6). T3.2: la notación de la ACF (ρ̂k frente a r_k) y de la
banda (±1.96/√n, con n las observaciones de la serie que se mira) se dice una vez, aquí."""


def registra(c, mover, entre, despues, esc, T13, **_):
    c("M1 · apertura: el ARIMA(0,1,5) a la vista y el airline con sus órdenes", T13,
      r'''      <p>El Capítulo 4 terminó con un fracaso deliberado. El mejor modelo ARIMA no estacional sobre
        $\log(\text{AirPassengers})$, un ARIMA($0,1,5$) elegido por búsqueda exhaustiva, dejaba en sus residuales
        $\hat\rho_{12} = 0.7245$ y $\hat\rho_{24} = 0.6727$: cinco términos MA, y toda la estructura sobrante
        concentrada en un solo sitio, los múltiplos de 12. Este capítulo se ocupa de ese sitio. En el
        Módulo 6 el modelo <em>airline</em>, con <strong>solo dos parámetros</strong>, deja
        $\hat\rho_{12} = -0.0515$ y pasa Ljung–Box(24) con $p = 0.233$.</p>''',
      r'''      <p>El Capítulo 4 terminó con un fracaso deliberado. El mejor modelo ARIMA no estacional sobre
        $\log(\text{AirPassengers})$, un ARIMA($0,1,5$) elegido por búsqueda exhaustiva, dejaba en sus residuales
        $\hat\rho_{12} = 0.7245$ y $\hat\rho_{24} = 0.6727$ —el bloque de código de este módulo lo vuelve a
        ajustar—: cinco términos MA, y toda la estructura sobrante concentrada en un solo sitio, los múltiplos de
        12. Este capítulo se ocupa de ese sitio. Lo resuelve el modelo que el Capítulo 4 dejó como avance, el
        <em>airline</em>, un SARIMA($0,1,1$)($0,1,1$)$_{12}$: el Módulo 2 lo escribe y lo ajusta, el Módulo 5 lo
        estudia y en el Módulo 6, con <strong>solo dos parámetros</strong>, deja $\hat\rho_{12} = -0.0515$ y pasa
        Ljung–Box(24) con $p = 0.233$.</p>''')

    c("M1 · la notación de la ACF y de la banda, una vez", T13,
      r'''        $3m$ rezagos</strong>: con los $20$ o $24$ por defecto se ve un pico y no se sabe si decae.</p>''',
      r'''        $3m$ rezagos</strong>: con los $20$ o $24$ por defecto se ve un pico y no se sabe si decae.</p>

      <p>En la tabla, $\hat\rho_k$ es la autocorrelación muestral en el rezago $k$ (el código del capítulo, el simulacro y el
        Capítulo 3 la escriben $r_k$), y la banda es la de siempre, $\pm 1.96/\sqrt{n}$, con $n$ el número de observaciones de la
        serie a la que se le mide la ACF: si se diferenció, las que quedan. El capítulo usa esas dos convenciones de
        aquí en adelante.</p>''')

    c("M1 · R: el ARIMA(0,1,5) del Capítulo 4, ajustado otra vez", T13,
      esc('''ap <- log(AirPassengers)          # m = 12, n = 144

# 1. La estacionalidad, VISTA'''),
      esc('''ap <- log(AirPassengers)          # m = 12, n = 144

# 0. El punto de partida: el ARIMA(0,1,5) con que termino el Capitulo 4
f5 <- Arima(ap, order = c(0, 1, 5))
round(coef(f5), 4)
#>    ma1     ma2     ma3     ma4     ma5
#> 0.1302 -0.0032 -0.3010 -0.6104  0.2508
round(as.numeric(residuals(f5))[1:3], 4)                  # los primeros residuales
#> [1] 0.0047 0.0420 0.0863
r5 <- Acf(residuals(f5), lag.max = 24, plot = FALSE)$acf   # r5[1] es el rezago 0
round(c(rho12 = r5[13], rho24 = r5[25]), 4)
#>  rho12  rho24
#> 0.7245 0.6727
lb5 <- Box.test(residuals(f5), lag = 24, type = "Ljung-Box", fitdf = 5)
round(unname(lb5$statistic), 1)
#> [1] 222.4
lb5$p.value < 1e-6
#> [1] TRUE

# 1. La estacionalidad, VISTA'''))

    c("M1 · Python: el ARIMA(0,1,5) con statsmodels", T13,
      esc('''s = pd.Series(ap, index=idx)

# 1. Vista: la tabla mes x anio ES el mapa de calor del simulador'''),
      esc('''s = pd.Series(ap, index=idx)

# 0. El punto de partida: el ARIMA(0,1,5) con que termino el Capitulo 4
import warnings
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
warnings.simplefilter("ignore", RuntimeWarning)   # solo avisos de coma flotante de numpy
f5 = ARIMA(s, order=(0, 1, 5), trend="n").fit()
print(f5.mle_retvals["converged"], np.round(f5.params.iloc[:5].values, 4))
#> True [ 0.1302 -0.0033 -0.301  -0.6104  0.2508]
print(np.round(f5.resid.iloc[:3].values, 4))   # los primeros residuales
#> [4.7185 0.0522 0.1067]
res5 = f5.resid[1:]                       # el primero es casi el nivel de la serie
r5 = sm.tsa.acf(res5, nlags=24, fft=False)
print(np.round(r5[[12, 24]], 4),
      round(float(acorr_ljungbox(res5, lags=[24], model_df=5)["lb_stat"].iloc[0]), 1))
#> [0.7218 0.6676] 219.3
# Los coeficientes coinciden con los de R (el bloque de R los imprime). Lo que
# cambia son los primeros residuales: statsmodels los calcula con el filtro aun
# inicializandose (Modulo 6), y R da 0.0047, 0.0420, 0.0863. Por eso la ACF y Q
# difieren de las de R (0.7245, 0.6727 y 222.4); la lectura es la misma: lo que
# sobra esta en 12 y 24.

# 1. Vista: la tabla mes x anio ES el mapa de calor del simulador'''))
