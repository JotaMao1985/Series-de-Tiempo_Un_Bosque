"""R3 · Módulos 7, 8 y 9 (5.7 Caso completo, 5.8 Segundo caso y contraejemplo, 5.9 Calendario).

D6:
- M7 dice que sus etapas son las del ciclo del M4; el «rango relativo» se define y lo calcula el
  bloque; la banda de los residuales (±0.163) se explica; el ARIMA(0,1,5) remite al bloque del M1; el
  `biasadj` que el Capítulo 6 busca en el 5 se nombra junto a la media lognormal, y el bloque lo
  calcula (y deja de llamar «media» a la mediana).
- M8 dice su estado inicial; «cuatro evidencias independientes» pasa a cuatro comprobaciones que
  son tres evidencias (la tercera y la cuarta miran el mismo Φ̂).
- M9: «dos clases» con cuatro filas; RMSE y «fuera de muestra» se presentan donde aparecen por
  primera vez, y el bloque calcula el 43.18 y el 45.48; $\\eta_t$ para el error de la regresión.
- Cada módulo cierra apuntando al siguiente."""


def registra(c, mover, entre, despues, esc, T79, **_):
    # ------------------------------------------------------------ M7
    c("M7 · las etapas son las del ciclo del Módulo 4", T79,
      '''      <h3>Etapa 1 · La transformación</h3>''',
      r'''      <p>Las cinco etapas que siguen son las del ciclo del Módulo 4, en su orden, aplicadas a
        $\log(\text{AirPassengers})$; el pronóstico, el uso del modelo, va después del ciclo.</p>

      <h3>Etapa 1 · La transformación</h3>''')
    c("M7 · el rango relativo, definido y calculado", T79,
      r'''nivel, y el rango relativo de la serie es $1.848$.''',
      r'''nivel, y el rango relativo de la serie —su recorrido, del mínimo al máximo, dividido por la media— es
        $1.848$.''')
    c("M7 · la banda de los residuales, explicada", T79,
      r'''en $0.117$, dentro de $\pm 0.163$. <strong>El $23$ sobrevive</strong>''',
      r'''en $0.117$, dentro de $\pm 0.163$, la banda de los $144$ residuales que devuelve R, $1.96/\sqrt{144}$.
          Trece de ellos son de arranque (Módulo 6); sin ellos la banda es la de $131$ observaciones, $\pm 0.171$, y
          la lectura no cambia. <strong>El $23$ sobrevive</strong>''')
    c("M7 · el ARIMA(0,1,5) remite al bloque del Módulo 1", T79,
      r'''          $\hat\rho_{12} = 0.7245$ en los residuales. Con <strong>solo dos parámetros</strong>''',
      r'''          $\hat\rho_{12} = 0.7245$ en los residuales, como vuelve a imprimir el bloque del Módulo 1. Con
          <strong>solo dos parámetros</strong>''')
    c("M7 · el biasadj del Capítulo 6, nombrado junto a la media lognormal", T79,
      r'''          de $525.46$: $126$ por debajo y $165$ por arriba. Esa asimetría es correcta y es del logaritmo, no un error
          del modelo.</p>''',
      r'''          de $525.46$: $126$ por debajo y $165$ por arriba. Esa asimetría es correcta y es del logaritmo, no un error
          del modelo. En R, si el logaritmo va dentro del modelo —<code>Arima(AirPassengers, …, lambda = 0)</code>—,
          <code>forecast()</code> deshace la transformación y devuelve esa mediana; con <code>biasadj = TRUE</code>
          la multiplica por $1 + \sigma_h^2/2$, una aproximación de la media: a $24$ meses, $530.58$ en lugar de
          $525.46$; la media exacta, $e^{\mu + \sigma_h^2/2}$, es $530.61$ (el bloque de abajo hace las tres cuentas).
          Cuál de las dos conviene depende de con qué se mida el error, y eso es del
          Capítulo 6.</p>''')
    c("M7 · R: el rango relativo en la etapa 1", T79,
      esc('''ap <- log(AirPassengers)

# --- Etapas 2 a 4: D primero, d despues, y la ACF de la serie ya estacionaria'''),
      esc('''ap <- log(AirPassengers)

# --- Etapa 1: el rango relativo de la serie cruda, (maximo - minimo) / media
round(diff(range(AirPassengers)) / mean(AirPassengers), 3)
#> [1] 1.848

# --- Etapas 2 a 4: D primero, d despues, y la ACF de la serie ya estacionaria'''))
    c("M7 · R: el pronóstico puntual es la mediana, y biasadj da la media", T79,
      esc('''round(exp(c(media = p$mean[24], lo95 = p$lower[24,2], hi95 = p$upper[24,2])), 2)
#>  media   lo95   hi95
#> 525.46 399.66 690.85'''),
      esc('''round(exp(c(mediana = p$mean[24], lo95 = p$lower[24,2], hi95 = p$upper[24,2])), 2)
#> mediana    lo95    hi95
#>  525.46  399.66  690.85'''))
    c("M7 · R: el mismo pronóstico con lambda = 0 y biasadj", T79,
      esc('''round(c(abajo = 525.46 - 399.66, arriba = 690.85 - 525.46), 2)
#>  abajo arriba
#> 125.80 165.39
'''),
      esc('''round(c(abajo = 525.46 - 399.66, arriba = 690.85 - 525.46), 2)
#>  abajo arriba
#> 125.80 165.39
# Con el logaritmo DENTRO del modelo (lambda = 0), forecast() lo deshace solo y
# devuelve la mediana; biasadj = TRUE devuelve una aproximacion de la media.
fl <- Arima(AirPassengers, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12),
            lambda = 0)
round(c(mediana = forecast(fl, h = 24)$mean[24],
        media   = forecast(fl, h = 24, biasadj = TRUE)$mean[24]), 2)
#> mediana   media
#>  525.46  530.58
sh <- (p$upper[24, 2] - p$mean[24]) / qnorm(0.975)    # sigma_24, en logaritmos
round(c(aproximada = exp(p$mean[24]) * (1 + sh^2 / 2), exacta = exp(p$mean[24] + sh^2 / 2)), 2)
#> aproximada    exacta
#>     530.58    530.61
'''))
    c("M7 · Python: por qué su media no es la de R; y cierre que apunta al Módulo 8", T79,
      '''#&gt; 530.52     un 1 % por encima de la mediana</code></pre>
        </div>
      </div>
    </div>''',
      '''#&gt; 530.52     un 1 % por encima de la mediana
# R da 530.61 con la misma formula y 530.58 con biasadj = TRUE, que usa la
# aproximacion 1 + sigma_h^2/2. La diferencia con 530.52 es sigma^2: statsmodels
# lo estima por maxima verosimilitud (0.001348) y R lo corrige por los parametros
# (0.001371).</code></pre>
        </div>
      </div>

      <p>Una serie y un modelo no prueban que el recorrido funcione siempre. El Módulo 8 lo repite en una serie
        donde las pruebas engañan y en otra que no tiene estación.</p>
    </div>''')

    # ------------------------------------------------------------ M8
    c("M8 · intro del contraejemplo: estado inicial", T79,
      r'''diferenciadas de forma regular. Es la comparación honesta''',
      r'''diferenciadas de forma regular; se abre con la primera. Es la comparación honesta''')
    c("M8 · cuatro comprobaciones, tres evidencias", T79,
      r'''      <p>Cuatro evidencias independientes y todas en la misma dirección. <code>auto.arima</code> lo confirma''',
      r'''      <p>Cuatro comprobaciones de tres tipos —una prueba, el correlograma y un ajuste forzado, que se lee por su
        $t$ y por su AICc— y todas en la misma dirección. No son independientes: salen de los mismos $138$ meses, y el
        $\hat\Phi$ del ajuste forzado mide casi lo mismo que $\hat\rho_{12}$; lo que pesa es que ninguna deja
        resquicio. <code>auto.arima</code> lo confirma''')
    c("M8 · la tabla: «Comprobación», no «Evidencia»", T79,
      '''            <tr><th>Evidencia</th><th>Qué se mide</th><th>Resultado</th></tr>''',
      '''            <tr><th>Comprobación</th><th>Qué se mide</th><th>Resultado</th></tr>''')
    c("M8 · el comentario del bloque, como la prosa", T79,
      '''# --- TRM: cuatro evidencias de que NO hay estacionalidad --------------------''',
      '''# --- TRM: cuatro comprobaciones de que NO hay estacionalidad ---------------''')
    c("M8 · cierre que apunta al Módulo 9", T79,
      '''#&gt; True True</code></pre>
        </div>
      </div>
    </div>''',
      '''#&gt; True True</code></pre>
        </div>
      </div>

      <p>Descartar la estacionalidad cuando no está es la mitad del oficio; la otra mitad es reconocer lo que la
        estacionalidad no puede absorber aunque esté. El Módulo 9 se ocupa de los efectos del calendario que cambian
        de posición de un año a otro.</p>
    </div>''')

    # ------------------------------------------------------------ M9
    c("M9 · «dos clases» con cuatro filas", T79,
      r'''      <p>El SARIMA supone que el patrón se repite <strong>en la misma posición</strong> cada $m$ observaciones. Hay dos
        clases de efectos de calendario que rompen ese supuesto y que, por tanto, ningún $\Phi$ ni ningún $\Theta$
        pueden absorber:</p>''',
      r'''      <p>El SARIMA supone que el patrón se repite <strong>en la misma posición</strong> cada $m$ observaciones. Lo
        que en el calendario no se repite así —la Semana Santa, que salta de marzo a abril; el febrero de los años
        bisiestos; los días hábiles de cada mes— ningún $\Phi$ ni ningún $\Theta$ puede absorberlo. La tabla repasa
        cuatro clases de efectos: el módulo construye las dos primeras, la tercera se trataría igual y la cuarta es la
        que no hace falta, porque se repite cada año en el mismo mes.</p>''')
    c("M9 · η_t para el error de la regresión, no n_t", T79,
      r'''        $$y_t = \beta' x_t + n_t$$
        <p style="margin-bottom:0;">donde $n_t$ sigue un SARIMA($p,d,q$)($P,D,Q$)$_m$.''',
      r'''        $$y_t = \beta' x_t + \eta_t$$
        <p style="margin-bottom:0;">donde $\eta_t$ —una letra distinta de la $n$ del tamaño de la muestra— sigue un
          SARIMA($p,d,q$)($P,D,Q$)$_m$.''')
    c("M9 · intro del simulador: estado inicial", T79,
      r'''Los interruptores activan cada regresor sobre el modelo <em>airline</em>; cada''',
      r'''Los interruptores activan cada regresor sobre el modelo <em>airline</em> (se abre con los
          días encendidos y la Semana Santa apagada); cada''')
    c("M9 · registro: «algo bonito»", T79,
      r'''y el primero dice algo bonito.</strong>''',
      r'''y el primero dice algo más.</strong>''')
    c("M9 · RMSE y «fuera de muestra», presentados donde aparecen por primera vez", T79,
      r'''          AICc, y sin embargo en la comparación fuera de muestra del Módulo 11 sale <em>peor</em> que el
          <em>airline</em> desnudo (RMSE $45.48$ frente a $43.18$). No es contradictorio:''',
      r'''          AICc, y sin embargo <strong>fuera de muestra</strong> —entrenando hasta 1958-12 y midiendo el error de
          pronóstico en los $24$ meses siguientes, la comparación del Módulo 11— sale <em>peor</em> que el
          <em>airline</em> desnudo: su <strong>RMSE</strong>, la raíz del error cuadrático medio en pasajeros, es
          $45.48$ frente a $43.18$ (el bloque de abajo lo calcula). No es contradictorio:''')
    c("M9 · R: el RMSE fuera de muestra, con y sin calendario", T79,
      esc('''#>   0.1882      no se rechaza beta = 1''') + '</code></pre>',
      esc('''#>   0.1882      no se rechaza beta = 1

# --- Fuera de muestra (Modulo 11): entrenar hasta 1958-12, pronosticar 24 meses
ent <- window(ap, end = c(1958, 12))
obs <- as.numeric(window(AirPassengers, start = c(1959, 1)))
g0 <- Arima(ent, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
g2 <- Arima(ent, order=c(0,1,1), seasonal=list(order=c(0,1,1), period=12), xreg = xreg[1:120, ])
rmse <- function(p) sqrt(mean((obs - exp(p))^2))     # en pasajeros: exp() deshace el log
round(c(airline = rmse(forecast(g0, h = 24)$mean),
        calendario = rmse(forecast(g2, xreg = xreg[121:144, ])$mean)), 2)
#>    airline calendario
#>      43.18      45.48''') + '</code></pre>')
    c("M9 · Python: el RMSE fuera de muestra, y cierre que apunta al Módulo 10", T79,
      esc('''# R da 0.1882 (con su 1.0840): tampoco aqui se rechaza beta = 1.''') + '''</code></pre>
        </div>
      </div>
''',
      esc('''# R da 0.1882 (con su 1.0840): tampoco aqui se rechaza beta = 1.

# --- Fuera de muestra (Modulo 11): entrenar hasta 1958-12, pronosticar 24 meses
def rmse_fuera(exog):
    m = dict(order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n")
    ex = None if exog is None else exog[:120]
    # se estima diferenciando, como R, y se pronostica con el modelo en niveles
    est = SARIMAX(s[:120], exog=ex, simple_differencing=True, **m).fit(
        disp=False, method="bfgs", maxiter=1000)
    p = SARIMAX(s[:120], exog=ex, **m).filter(est.params).get_forecast(
        24, exog=None if exog is None else exog[120:]).predicted_mean.to_numpy()
    e = np.exp(ap[120:]) - np.exp(p)                  # en pasajeros
    return est.mle_retvals["converged"], round(float(np.sqrt(np.mean(e**2))), 2)
print(rmse_fuera(None), rmse_fuera(X))
#> (True, 43.18) (True, 45.48)''') + '''</code></pre>
        </div>
      </div>

      <p>Calendario aparte, todo lo anterior ha funcionado porque $m = 12$ es pequeño. El Módulo 10 mira qué se
        rompe cuando no lo es, y qué se usa entonces.</p>
''')
