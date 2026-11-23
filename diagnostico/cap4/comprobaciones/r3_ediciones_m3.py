"""R3 · Módulo 3 (4.3 Elegir d).

D5: Phillips–Perron se nombra completo donde se usa por primera vez y su estadístico sale de un
bloque (`PP.test`); el «modelo de dos medias» se escribe y se ajusta a la vista (de ahí sale σ̂ = 127.03
del experimento); `auto.arima` se presenta en una cláusula; la introducción del simulador deja de dar el
resultado; el encabezado del recuadro de `ndiffs()` ya no repite el «tres» de las tres evidencias."""


def registra(c, mover, entre, esc, T13, **_):
    c("M3 · la tabla de evidencias nombra la prueba PP completa en su primer uso", T13,
      r'''<td>ADF y PP ($H_0$: hay raíz unitaria) y KPSS ($H_0$:
              es estacionaria)</td>''',
      r'''<td>ADF y PP (Phillips–Perron; $H_0$: hay raíz unitaria) y
              KPSS ($H_0$: es estacionaria)</td>''')

    c("M3 · el recuadro de ndiffs(): auto.arima se presenta donde se usa por primera vez", T13,
      r'''Y el valor por
          defecto de <code>ndiffs()</code> —y por tanto el que usa <code>auto.arima()</code>— es KPSS, la única que
          dice que sí.''',
      r'''Y el valor por
          defecto de <code>ndiffs()</code> —y por tanto el que usa <code>auto.arima()</code>, la función de
          <code>forecast</code> que ajusta sola varios ARIMA y se queda con el de menor AICc, y que el Módulo 7
          abre— es KPSS, la única que dice que sí.''')
    c("M3 · el encabezado del recuadro ya no repite «tres» (las tres evidencias son otra cosa)", T13,
      r'''Tres pruebas, tres respuestas, la
          misma serie</h4>''',
      r'''Una misma serie, tres respuestas de
          <code>ndiffs()</code></h4>''')

    c("M3 · el modelo de dos medias se escribe donde se usa por primera vez", T13,
      r'''      <p>Se puede comprobar. Se generan series de ruido blanco puro de la misma longitud y desviación que los
        residuales del modelo de dos medias del Nilo —una antes y otra después de 1899— ($n = 100$,
        $\hat\sigma = 127.0$), se les añade un escalón en la posición 29 —el año 1899— de tamaño $\beta$ regulable,
        y se cuenta cuántas veces rechaza KPSS:</p>''',
      r'''      <p>Se puede comprobar. El <strong>modelo de dos medias</strong> del Nilo,
        $y_t = \mu + \beta\,\mathbf{1}\{t \ge 1899\} + \varepsilon_t$, da a la serie una media hasta 1898 y otra
        desde 1899; el bloque de código de este módulo lo ajusta y el Módulo 8 lo estudia. Se generan series de
        ruido blanco puro de la misma longitud y desviación que sus residuales ($n = 100$,
        $\hat\sigma = 127.0$), se les añade un escalón en la posición 29 —el año 1899— de tamaño $\beta$
        regulable, y se cuenta cuántas veces rechaza KPSS:</p>''')

    c("M3 · la introducción del simulador pide hacer, no cuenta el resultado", T13,
      r'''        <p class="simulador-intro">El deslizador fija el tamaño del descenso en 1899, $|\beta|$. Arriba, una
          realización concreta; abajo, la tasa de rechazo de KPSS al $5\,\%$ medida en R sobre 400 réplicas en nueve
          valores de $|\beta|$, interpolada entre ellos. Recuerda que <strong>ninguna</strong> de estas series tiene
          raíz unitaria: todas son ruido blanco más una constante a trozos. Empieza en $|\beta| = 0$: KPSS rechaza
          cerca del $5\,\%$ nominal, así que la prueba funciona. Luego sube el descenso y busca dónde cruza la curva
          el $50\,\%$; la línea vertical marca el que de verdad tiene el Nilo, $|\beta| = 247.8$. La segunda curva
          es la misma prueba con otro truncamiento de la varianza de largo plazo, $\ell = 12$ en vez de $4$, el de
          <code>nlags="legacy"</code> en Python: rechaza menos, pero no deja de engañarse, solo necesita descensos
          mayores. El recuadro «R y Python no calculan el mismo KPSS», más abajo, explica ese parámetro.</p>''',
      r'''        <p class="simulador-intro">El deslizador fija el tamaño del descenso en 1899, $|\beta|$. Arriba, una
          realización concreta; abajo, la tasa de rechazo de KPSS al $5\,\%$ medida en R sobre 400 réplicas en nueve
          valores de $|\beta|$, interpolada entre ellos. Recuerda que <strong>ninguna</strong> de estas series tiene
          raíz unitaria: todas son ruido blanco más una constante a trozos. Recorre $|\beta|$ desde $0$ y busca
          dónde cruza la curva el $50\,\%$; la línea vertical marca el descenso que tiene el Nilo. La segunda curva
          es la misma prueba con otro truncamiento de la varianza de largo plazo, $\ell = 12$ en vez de $4$, el de
          <code>nlags="legacy"</code> en Python; el recuadro «R y Python no calculan el mismo KPSS», más abajo,
          explica ese parámetro.</p>''')

    # ------------------------------------------------------------------ código R
    c("M3 · R: PP.test en la evidencia 2", T13,
      esc('''# rechaza (p < 0.01): diferenciar. kpss.test avisa "p-value smaller than
# printed p-value": la tabla se acaba en 0.01, no es un error
'''),
      esc('''# rechaza (p < 0.01): diferenciar. kpss.test avisa "p-value smaller than
# printed p-value": la tabla se acaba en 0.01, no es un error
PP.test(Nile)$statistic         # Phillips-Perron: H0, hay raiz unitaria
#> Dickey-Fuller
#>     -6.690051
# rechaza: su p-valor es 0.01, el minimo de su tabla (p < 0.01), y apunta a NO
# diferenciar
'''))
    c("M3 · R: el modelo de dos medias a la vista, y de ahí sale σ", T13,
      esc('''# --- El experimento del escalon -----------------------------------------
set.seed(2026)
escalon <- as.numeric(1:100 >= 29)      # 1899 es la observacion 29
simula <- function(beta, reps = 400) {       # beta = tamano del escalon
  mean(replicate(reps, {
    x <- 1000 + beta * escalon + rnorm(100, 0, 127.03)'''),
      esc('''# --- El modelo de dos medias: y = mu + beta * 1{t >= 1899} + e ----------
escalon <- as.numeric(1:100 >= 29)      # 1899 es la observacion 29
dos_medias <- arima(Nile, order = c(0, 0, 0), xreg = escalon, method = "ML")
round(c(antes = mean(Nile[1:28]), despues = mean(Nile[29:100]),
        beta = coef(dos_medias)[["escalon"]], sigma = sd(residuals(dos_medias))), 2)
#>   antes despues    beta   sigma
#> 1097.75  849.97 -247.78  127.03

# --- El experimento del escalon -----------------------------------------
set.seed(2026)
simula <- function(beta, reps = 400) {       # beta = tamano del escalon
  mean(replicate(reps, {
    x <- 1000 + beta * escalon + rnorm(100, 0, 127.03)    # sigma de arriba'''))

    # ------------------------------------------------------------------ código Python
    c("M3 · Python: PP no está en statsmodels (comentario)", T13,
      esc('''#> -3.3657 0.0561    mismo estadistico que R (-3.3657); el p-valor difiere
#>                   porque R interpola en tablas y statsmodels usa MacKinnon
'''),
      esc('''#> -3.3657 0.0561    mismo estadistico que R (-3.3657); el p-valor difiere
#>                   porque R interpola en tablas y statsmodels usa MacKinnon
# La prueba PP no esta en statsmodels: aqui solo se reproducen ADF y KPSS
'''))
    c("M3 · Python: el modelo de dos medias a la vista", T13,
      esc('''# El experimento del escalon, ya con el truncamiento de R
rng = np.random.default_rng(2026)
escalon = (np.arange(100) >= 28).astype(float)
def simula'''),
      esc('''# El modelo de dos medias: una media hasta 1898 y otra desde 1899
escalon = (np.arange(100) >= 28).astype(float)
res = np.r_[nilo[:28] - nilo[:28].mean(), nilo[28:] - nilo[28:].mean()]
print(round(nilo[:28].mean(), 2), round(nilo[28:].mean(), 2), round(res.std(ddof=1), 2))
#> 1097.75 849.97 127.03
#   beta es la diferencia de las dos medias: 849.97 - 1097.75 = -247.78

# El experimento del escalon, ya con el truncamiento de R
rng = np.random.default_rng(2026)
def simula'''))
