"""R3 · Módulo 10 (4.10 La TRM, el puente y el cierre) · D6, sin partir el módulo.

Orden final: el Nilo (resumido UNA sola vez) → la TRM → el puente al Capítulo 5 (con su código) → el
resumen del capítulo (lo último antes de la evaluación) → autoevaluación, ejercicios, lecturas y la nota
«Y en el Capítulo 5…». Qué cambia:

  * una frase al comienzo dice las cuatro partes y que el resumen cierra antes de la evaluación;
  * el Nilo: la tabla, el modelo, las dos lecciones y el empalme eran cuatro resúmenes seguidos; queda
    la tabla (sin el Shapiro ni los semianchos, que ningún bloque imprime), una frase sobre el modelo
    (que se ajustó en el Módulo 1) y la nota de las dos lecciones;
  * la TRM: «192 modelos (con la parte estacional…)» sale (el 192 no salía de ningún bloque); los
    coeficientes «no son identificables» (el otro sentido de «identificar» es el de la etapa 1); la nota
    «El resultado, aceptado tal cual» recoge lo que decía la nota de la TRM del Módulo 5 (que se va); el
    80 % que el Módulo 9 prometía medir se mide aquí; el *naïve* remite al Módulo 8;
  * el puente: gana su bloque de código (R y Python), de donde salen todas sus cifras;
  * el resumen: la viñeta de las evidencias no repite el 100 % del Monte Carlo del Módulo 3.
"""


def registra(c, mover, entre, esc, T10, **_):
    # =============================================================== intro y el Nilo, una sola vez
    entre("M10 · introducción y «El Nilo, de principio a fin»: un solo resumen", T10,
          '''      <p>Nueve módulos han desmontado el ciclo de Box–Jenkins pieza a pieza, casi siempre sobre el Nilo. Este''',
          '''      <h3>Caso: la tasa representativa del mercado</h3>''',
          r'''      <p>Nueve módulos han desmontado el ciclo de Box–Jenkins pieza a pieza, casi siempre sobre el Nilo. Este
        último lo vuelve a montar en cuatro tiempos. Primero, el Nilo, resumido una sola vez con las piezas en el
        orden del ciclo. Después, de un tirón, una serie que no se eligió por dócil, la TRM, hasta la etapa que el
        Módulo 9 dejó preparada: usar el modelo para pronosticar y leer el ancho de su intervalo. Luego, el puente al
        Capítulo 5, y al final el resumen del capítulo, que cierra el módulo antes de la autoevaluación, los
        ejercicios y las lecturas.</p>

      <h3>El Nilo, de principio a fin</h3>

      <p>Cada módulo tomó del Nilo lo que necesitaba para su pieza. En el orden del ciclo, esas piezas cuentan una
        sola historia, con una vuelta atrás incluida:</p>

      <!-- Por debajo de lg (1024 px) la tabla se apila: con el menú lateral al lado, a 768 px el contenido
           mide unos 330 px y dos columnas de texto largo no caben. -->
      <div class="diagram px-3 py-4 lg:p-8">
        <table class="block lg:table mb-0 lg:mb-8" style="position:relative; text-align:left;">
          <thead class="hidden lg:table-header-group"><tr><th>Etapa</th><th>Qué salió en el Nilo</th></tr></thead>
          <tbody class="block lg:table-row-group">
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>1. Identificación de $d$</strong><br><span class="text-gray-500 text-sm">Módulos 1 y 3</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                Un descenso brusco hacia 1899 en el gráfico y una ACF que decae despacio desde $0.498$. Las
                pruebas discrepan: <code>adf.test</code> ($p = 0.064$) y KPSS ($p &lt; 0.01$) apuntan a diferenciar,
                y PP ($p &lt; 0.01$) rechaza la raíz unitaria. Se sigue a KPSS, la de <code>auto.arima</code>:
                <strong>$d = 1$</strong>, a título provisional.</td></tr>
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>1. Identificación de $p,q$</strong><br><span class="text-gray-500 text-sm">Módulo 4</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                La ACF de $\nabla$Nilo corta en el rezago 1 ($\hat\rho_1 = -0.402$) y la PACF decae con signo
                negativo: ARIMA($0,1,1$), y a la estimación van también sus vecinos.</td></tr>
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>2. Estimación: la constante</strong><br><span class="text-gray-500 text-sm">Módulo 5</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                Con deriva, $\hat\delta = -2.883$ ($t = -1.43$) y el AICc empeora ($1268.06$ frente a
                $1267.51$): el modelo va <strong>sin constante</strong>. De la media de las diferencias, $-3.84$,
                el descenso de 1899 aporta $-2.50$: no es una pendiente.</td></tr>
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>2. Estimación: la rejilla</strong><br><span class="text-gray-500 text-sm">Módulos 6 y 7</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                Dentro de $d = 1$, el AICc elige el <strong>ARIMA($1,1,1$)</strong> ($1267.51$) y el BIC el
                $(0,1,1)$ ($1274.28$); <code>auto.arima</code> llega al $(1,1,1)$ evaluando $18$ modelos o $42$,
                aunque siete caben en $2$ puntos. El ARIMA($1,2,2$), con $1264.60$, no cuenta: ese AICc se calcula
                sobre $98$ observaciones y no sobre $99$.</td></tr>
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>3. Diagnóstico</strong><br><span class="text-gray-500 text-sm">Módulo 8</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                Ljung–Box(20) $p = 0.800$: los residuales pasan. Pero la raíz MA ($1.144$; la AR, $3.93$) está
                cerca del círculo: con $\hat\theta = -0.874$ el MA casi deshace la diferencia, la anomalía del
                Módulo 1.</td></tr>
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>Vuelta a la etapa 1</strong><br><span class="text-gray-500 text-sm">Módulo 8</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                Un escalón en 1899 sin diferenciar ($\hat\beta = -247.78$, $t = -8.80$) le saca casi $25$ puntos de
                AICc al mejor ARMA con $d = 0$ y sus residuales pasan Ljung–Box ($p = 0.812$), pero contra el
                ARIMA($1,1,1$) el AICc no compara: el $d$ es otro. Fuera de muestra, en 1951–1970, el RMSE es
                $125.05$ el del ARIMA, $127.99$ el del escalón y $123.06$ el del naïve: ninguno se impone.</td></tr>
            <tr class="block lg:table-row">
              <td class="block lg:table-cell pb-1 lg:pb-4 border-b-0 lg:border-b">
                <strong>4. Uso (pronóstico)</strong><br><span class="text-gray-500 text-sm">Módulo 9</span></td>
              <td class="block lg:table-cell pt-0 lg:pt-4">
                Sin constante y con $d = 1$, el pronóstico se aplana: $816.18$ para 1971 y $842.17$ a los pocos
                años, no el último dato ($740$). Con $\psi_\infty = 0.169$, el intervalo se abre mucho más despacio
                que el de una caminata aleatoria (se compara más abajo).</td></tr>
          </tbody>
        </table>
      </div>

      <p>El modelo que sale del ciclo es el del Módulo 1, con $\hat\phi = 0.2544$ y $\hat\theta = -0.8741$. En
        nivel, su pronóstico casi coincide con el de su rival: el escalón pronostica $849.97$, la media desde 1899, y
        el ARIMA se queda en $842.17$. Lo que los separa es la banda, que en el escalón no se ensancha y en el
        ARIMA sí.</p>

      <div class="note">
        <p style="margin-bottom:0;"><strong>Leído de corrido, el caso deja dos lecciones.</strong> La primera: el
          ciclo funciona y aun así no basta. El ARIMA($1,1,1$) supera cada etapa con las herramientas previstas, y la
          pista de que $d = 1$ podía sobrar asomó en casi todas —las pruebas que discrepan, el
          $\hat\rho_1 = -0.402$ de la serie diferenciada, el $\hat\theta$ cerca de $-1$—, pero solo el gráfico la
          explica. La segunda: la duda final, diferenciar o modelar el escalón, no la resuelve ningún criterio dentro
          de muestra, porque los dos modelos tienen distinto $d$. Hay que medirla fuera de muestra, y eso es el
          Capítulo 6.</p>
      </div>

      <p>En el Nilo el ciclo encontró estructura y dejó abierta la duda sobre $d$. La serie siguiente invierte la
        situación: sobre $d$ no hay discusión, y lo que está en duda es si queda algo que modelar.</p>

''')

    # =============================================================== la TRM
    c("M10 · TRM, tabla: auto.arima sin el «192 modelos» (no salía de ningún bloque)", T10,
      r'''<code>auto.arima</code> con búsqueda exhaustiva sobre $192$ modelos
                (con la parte estacional permitida; sin ella son $42$) devuelve <strong>ARIMA($0,1,0$)</strong>.</td></tr>''',
      r'''<code>auto.arima</code> con búsqueda exhaustiva devuelve
                <strong>ARIMA($0,1,0$)</strong>.</td></tr>''')
    c("M10 · TRM, el ARIMA(2,1,2): «no son identificables» (el parámetro), no «no están identificados»", T10,
      r'''los coeficientes no están identificados y el AICc
          premia un espejismo.''',
      r'''los coeficientes no son identificables y el AICc
          premia un espejismo.''')
    c("M10 · TRM, nota del resultado aceptado: recoge la nota de la deriva que estaba en el Módulo 5", T10,
      r'''$\hat\delta = 8.00$ pesos/mes con error estándar $10.36$ ($t = 0.77$): no significativa, así que ni
          siquiera hay una tendencia que extrapolar.</p>''',
      r'''$\hat\delta = 8.00$ pesos/mes con error estándar $10.36$ ($t = 0.77$): no significativa, así que ni
          siquiera hay una tendencia que extrapolar, aunque a ojo la serie «claramente sube». Como en el Nilo
          (Módulo 5), esa deriva es la media de las diferencias, $(y_n - y_1)/(n-1)$: depende solo del primer mes y
          del último. Que una tendencia visible no sea distinguible de cero con $n = 138$ dice más sobre la
          variabilidad de la serie que sobre la tendencia.</p>''')
    c("M10 · TRM, el naïve remite al Módulo 8", T10,
      r'''En el Capítulo 6 la caminata aleatoria
          reaparece con otro nombre —el método <em>naïve</em>— y como <strong>referencia que hay que batir</strong>.</p>''',
      r'''En el Capítulo 6 la caminata aleatoria
          reaparece como el método <em>naïve</em>, el mismo que el Módulo 8 usó de referencia, y como
          <strong>referencia que hay que batir</strong>.</p>''')
    c("M10 · TRM, cobertura: el 80 % del Módulo 9 se mide aquí", T10,
      r'''A un mes, el $95\,\%$ se cumple dentro de la
        muestra —solo $6$ de los $137$ cambios mensuales caen fuera, un $4.4\,\%$—, pero $5$ de esos $6$ caen
        <strong>por arriba</strong>''',
      r'''A un mes, los dos intervalos se cumplen dentro
        de la muestra: el $95\,\%$ deja fuera solo $6$ de los $137$ cambios mensuales, un $4.4\,\%$, y el $80\,\%$ del
        Módulo 9 cubre el $83.9\,\%$. Pero $5$ de esos $6$ caen <strong>por arriba</strong>''')

    # =============================================================== el puente, con su código
    c("M10 · puente: el bloque de código (R y Python) de donde salen todas sus cifras", T10,
      r'''decide aquí no es un criterio de información sino el <strong>diagnóstico</strong>, que es categórico.</p>
      </div>
''',
      r'''decide aquí no es un criterio de información sino el <strong>diagnóstico</strong>, que es categórico.</p>
      </div>

      <p>El experimento entero, de la búsqueda no estacional al modelo <em>airline</em>, en un solo bloque:</p>

      <div class="code-tabs">
        <div class="code-tabs-nav" role="tablist" aria-label="El puente al Capítulo 5">
          <button class="code-tab-btn active" data-lang="r" role="tab" aria-selected="true">R</button>
          <button class="code-tab-btn" data-lang="python" role="tab" aria-selected="false">Python</button>
        </div>
        <div class="code-tab-panel" data-lang="r">
          <pre><code class="language-r">''' + esc('''library(forecast)

lap <- log(AirPassengers)                  # 144 meses, 1949-1960
length(lap)
#> [1] 144

# El mejor ARIMA NO estacional, con busqueda exhaustiva (p + q <= 5 por defecto)
mejor <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE)
as.character(mejor)
#> [1] "ARIMA(0,1,5)"

# Su diagnostico: lo que sobra en los residuales esta en los rezagos 12 y 24
res <- residuals(mejor)
r <- Acf(res, lag.max = 24, plot = FALSE)$acf[-1]
round(c(rho12 = r[12], rho24 = r[24], banda = 1.96 / sqrt(length(res))), 4)
#>  rho12  rho24  banda
#> 0.7245 0.6727 0.1633
lb <- Box.test(res, lag = 24, type = "Ljung-Box", fitdf = 5)   # fitdf = p + q
round(unname(lb$statistic), 1)
#> [1] 222.4
lb$p.value < 1e-6
#> [1] TRUE

# Subir el tope de p y q no lo arregla
amplio <- auto.arima(lap, seasonal = FALSE, stepwise = FALSE, approximation = FALSE,
                     max.p = 8, max.q = 8, max.order = 16)
as.character(amplio)
#> [1] "ARIMA(8,1,3) with drift"
round(Acf(residuals(amplio), lag.max = 24, plot = FALSE)$acf[13], 3)
#> [1] 0.437

# El modelo estacional "airline" del Capitulo 5, solo como avance
airline <- Arima(lap, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1), period = 12))
res2 <- residuals(airline)
round(c(rho12 = Acf(res2, lag.max = 24, plot = FALSE)$acf[13],
        lb24_p = Box.test(res2, lag = 24, type = "Ljung-Box", fitdf = 2)$p.value), 4)
#>   rho12  lb24_p
#> -0.0515  0.2330

# Los AICc no se comparan: sus verosimilitudes usan distinto numero de datos
c(no_estacional = mejor$nobs, airline = airline$nobs)
#> no_estacional       airline
#>           143           131''') + r'''</code></pre>
        </div>
        <div class="code-tab-panel" data-lang="python" hidden>
          <pre><code class="language-python">''' + esc('''import numpy as np, statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings; warnings.filterwarnings("ignore")

ap = np.log(sm.datasets.get_rdataset("AirPassengers").data["value"].values)
print(len(ap))
#> 144

# El ARIMA(0,1,5) que elige auto.arima en R. statsmodels no trae auto.arima, ni
# por tanto la busqueda amplia (p, q <= 8): aqui se ajusta el orden que R eligio
f = ARIMA(ap, order=(0, 1, 5), trend="n").fit()
e = f.resid[1:]                       # el primer residual es el dato: se descarta
r = acf(e, nlags=24, fft=False)
print(np.round([r[12], r[24], 1.96 / np.sqrt(len(e))], 4).tolist())
#> [0.7218, 0.6676, 0.1639]
#   R da 0.7245, 0.6727 y 0.1633: coeficientes casi iguales, residuales algo distintos
lb = acorr_ljungbox(e, lags=[24], model_df=5)
print(round(float(lb["lb_stat"].iloc[0]), 1), float(lb["lb_pvalue"].iloc[0]) < 1e-6)
#> 219.3 True
#   R da Q = 222.4: la misma lectura, rechaza

# El modelo estacional "airline", solo como avance
air = ARIMA(ap, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n").fit()
e2 = air.resid[13:]                   # los 13 primeros residuales son del arranque (1 + 12)
r2 = acf(e2, nlags=24, fft=False)
lb2 = acorr_ljungbox(e2, lags=[24], model_df=2)
print(round(r2[12], 4), round(float(lb2["lb_pvalue"].iloc[0]), 4))
#> -0.0525 0.3676
#   R da -0.0515 y 0.2330: el mismo veredicto, no rechaza

# Los AICc no se comparan: sus verosimilitudes usan distinto numero de datos
print(f.nobs_effective, air.nobs_effective)
#> 143 131''') + r'''</code></pre>
        </div>
      </div>
''')

    # =============================================================== el resumen
    c("M10 · resumen: la viñeta de las evidencias no repite el 100 % del Monte Carlo (del Módulo 3)", T10,
      r'''las pruebas pueden engañar: con un escalón como el del Nilo, KPSS
            confunde el cambio de nivel con una raíz unitaria el $100\,\%$ de las veces.''',
      r'''las pruebas pueden engañar: un cambio de nivel como el del Nilo
            hace que KPSS lo lea como una raíz unitaria.''')

    c("M10 · TRM, etapa 4: la presentación de la caminata es más corta (la fórmula se deduce en el Módulo 9)", T10,
      r'''      <p>Queda una etapa, y en esta serie es la más instructiva de todas. El Módulo 9 dedujo que el ancho del
        intervalo sale de los pesos $\psi$, $\sigma_h^2 = \sigma^2\sum_{j=0}^{h-1}\psi_j^2$, y que la caminata
        aleatoria es el caso de referencia porque <strong>todos sus $\psi$ valen $1$</strong>: la integración no
        amortigua nada, así que ningún choque se olvida nunca. Aquí no hay que aplicar la fórmula, hay que leerla.
        A $h$ pasos, el cambio desde el último dato es la suma de los $h$ choques que aún no han ocurrido. Como su
        esperanza es cero, el pronóstico es el último valor, y el error de pronóstico es esa misma suma:</p>''',
      r'''      <p>Queda la etapa 4, y en esta serie es la más instructiva. El Módulo 9 dedujo que el ancho del intervalo
        sale de los pesos $\psi$, $\sigma_h^2 = \sigma^2\sum_{j=0}^{h-1}\psi_j^2$, y que la caminata aleatoria es el
        caso de referencia: <strong>todos sus $\psi$ valen $1$</strong>, la integración no amortigua nada y ningún
        choque se olvida. Aquí la fórmula no se aplica, se lee: a $h$ pasos, el cambio desde el último dato es la
        suma de los $h$ choques que aún no han ocurrido, de esperanza cero, así que el pronóstico es el último valor
        y el error es esa misma suma:</p>''')
