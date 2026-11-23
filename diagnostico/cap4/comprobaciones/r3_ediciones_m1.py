"""R3 · Módulo 1 (4.1 De ARMA a ARIMA).

D5 (orden sin renumerar): el ARIMA(1,1,1) del Nilo se ajusta a la vista la primera vez que se usa
(0.2544 y −0.8741 dejan de entrar como constantes), la constante `c` se anuncia donde aparece, la
tabla de casos conocidos presenta el suavizamiento exponencial simple y el método de Holt, y «el
software» de la nota de la anomalía tiene antecedente."""


def registra(c, mover, entre, esc, T13, **_):
    # ------------------------------------------------------------------ la constante c
    c("M1 · la constante c se anuncia donde aparece (la decide el Módulo 5)", T13,
      r'''          $\theta(B) = 1 + \theta_1 B + \cdots + \theta_q B^q$, exactamente los del capítulo anterior. La letra
          <strong>I</strong> es de <em>integrated</em>: para volver de $w_t$ a $y_t$ hay que sumar
          (<em>integrar</em>) $d$ veces.</p>''',
      r'''          $\theta(B) = 1 + \theta_1 B + \cdots + \theta_q B^q$, exactamente los del capítulo anterior. La letra
          <strong>I</strong> es de <em>integrated</em>: para volver de $w_t$ a $y_t$ hay que sumar
          (<em>integrar</em>) $d$ veces. La constante $c$ cambia de significado según $d$: la trata el Módulo 5, y
          hasta entonces el modelo va sin ella.</p>''')

    # ------------------------------------------------------------------ la tabla de casos conocidos
    c("M1 · «Casos particulares»: el suavizamiento exponencial simple y Holt, presentados en una frase", T13,
      r'''      <h3>Casos particulares ya conocidos</h3>

      <div class="diagram">''',
      r'''      <h3>Casos particulares</h3>

      <p>Dos de las filas nombran métodos de pronóstico que los capítulos anteriores no presentaron. El
        <strong>suavizamiento exponencial simple</strong> pronostica con un promedio ponderado de todo el pasado, con
        pesos que decaen geométricamente: cada pronóstico corrige el anterior con una fracción $\alpha$ de su error.
        El método de <strong>Holt</strong> hace lo mismo con el nivel y con la pendiente de la serie. Aquí solo
        importa que los dos resultan ser ARIMA con los coeficientes restringidos: el capítulo no los usa más allá de
        esa equivalencia.</p>

      <div class="diagram">''')
    c("M1 · la fila del IMA(2,2) dice qué suaviza Holt", T13,
      r'''<td>Incluye al método de <strong>Holt</strong> con
              tendencia, con restricciones sobre los coeficientes.</td></tr>''',
      r'''<td>Incluye al método de <strong>Holt</strong>
              (nivel y tendencia suavizados), con restricciones sobre los coeficientes.</td></tr>''')

    # ------------------------------------------------------------------ el modelo se ajusta a la vista
    c("M1 · R: el ARIMA(1,1,1) del Nilo se ajusta y se imprime; phi y theta salen de ahí", T13,
      esc('''data(Nile)          # datasets de R base: caudal anual 1871-1970
length(Nile)
#> [1] 100

# Un ARIMA(1,1,1) es un ARMA(2,1) con una raiz unitaria impuesta.
# Se comprueba expandiendo el polinomio:
phi <- 0.2544
ar_expandido'''),
      esc('''data(Nile)          # datasets de R base: caudal anual 1871-1970
length(Nile)
#> [1] 100

# El modelo que acompana todo el capitulo: un ARIMA(1,1,1) para el Nilo,
# por maxima verosimilitud (el estimador del Capitulo 3)
f <- arima(Nile, order = c(1, 1, 1), method = "ML")
round(rbind(coef = coef(f), ee = sqrt(diag(f$var.coef))), 4)
#>         ar1     ma1
#> coef 0.2544 -0.8741
#> ee   0.1194  0.0605
phi   <- round(coef(f)[["ar1"]], 4)       #  0.2544
theta <- round(coef(f)[["ma1"]], 4)       # -0.8741
round(Mod(polyroot(c(1, theta))), 3)      # la raiz del polinomio MA
#> [1] 1.144

# Un ARIMA(1,1,1) es un ARMA(2,1) con una raiz unitaria impuesta.
# Se comprueba expandiendo el polinomio:
ar_expandido'''))
    c("M1 · R: arima.sim con phi y theta", T13,
      esc('''w <- arima.sim(list(ar = 0.2544, ma = -0.8741), n = 200)  # la diferencia'''),
      esc('''w <- arima.sim(list(ar = phi, ma = theta), n = 200)       # la diferencia'''))
    c("M1 · R: arima.sim sin MA, con phi", T13,
      esc('''w0 <- arima.sim(list(ar = 0.2544), n = 200)'''),
      esc('''w0 <- arima.sim(list(ar = phi), n = 200)'''))
    c("M1 · R: arima.sim con order, phi y theta", T13,
      esc('''y2 <- arima.sim(list(order = c(1, 1, 1), ar = 0.2544, ma = -0.8741), n = 200)'''),
      esc('''y2 <- arima.sim(list(order = c(1, 1, 1), ar = phi, ma = theta), n = 200)'''))

    c("M1 · Python: se importa ARIMA y se ajusta el modelo del Nilo; phi y theta, los de R", T13,
      esc('''from statsmodels.tsa.arima_process import ArmaProcess

nilo = sm.datasets.nile.load_pandas().data["volume"].values
print(len(nilo))
#> 100

# El mismo polinomio expandido
phi = 0.2544
ar_expandido'''),
      esc('''from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA

nilo = sm.datasets.nile.load_pandas().data["volume"].values
print(len(nilo))
#> 100

# El modelo que acompana todo el capitulo: un ARIMA(1,1,1) para el Nilo
ajuste = ARIMA(nilo, order=(1, 1, 1), trend="n").fit()
print(np.round(ajuste.params[:2], 4), np.round(ajuste.bse[:2], 4))
#> [ 0.2549 -0.8749] [0.1287 0.0546]
#   R da 0.2544 y -0.8741, con e.e. 0.1194 y 0.0605: otro arranque y otra
#   covarianza, la misma lectura. Abajo se usan los de R, para que las
#   cifras de los dos lenguajes se puedan comparar
phi, theta = 0.2544, -0.8741

# El mismo polinomio expandido
ar_expandido'''))
    c("M1 · Python: ArmaProcess con phi y theta", T13,
      esc('''proceso  = ArmaProcess(ar=np.r_[1, -0.2544], ma=np.r_[1, -0.8741])
proceso0 = ArmaProcess(ar=np.r_[1, -0.2544], ma=np.r_[1])      # sin termino MA'''),
      esc('''proceso  = ArmaProcess(ar=np.r_[1, -phi], ma=np.r_[1, theta])
proceso0 = ArmaProcess(ar=np.r_[1, -phi], ma=np.r_[1])         # sin termino MA'''))

    # ------------------------------------------------------------------ la nota de la anomalía
    c("M1 · la anomalía: «los coeficientes estimados» (se acaban de ajustar), no «reales»", T13,
      r'''y con los coeficientes reales
          del Nilo, en esta realización, la deja prácticamente igual''',
      r'''y con los coeficientes
          estimados del Nilo, en esta realización, la deja prácticamente igual''')
    c("M1 · «el software decidió que sí» tiene antecedente: la regla automática que elige d", T13,
      r'''El Módulo 3 explica por qué el software decidió que sí, y el Módulo 8 cierra el
          caso.''',
      r'''El Módulo 3 explica por qué la regla automática que elige $d$ decidió que sí, y el Módulo 8 cierra el
          caso.''')
