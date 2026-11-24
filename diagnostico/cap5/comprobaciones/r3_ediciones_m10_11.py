"""R3 · Módulos 10 y 11 (5.10 Cuando m es grande, 5.11 Panorama comparativo y cierre).

M10 (D6, T3.2): «media horarios» se dice; la introducción del simulador de armónicos dice su estado
inicial y pregunta en vez de dar el resultado; la columna «Parámetros totales» se explica; η_t para
el error de la regresión; el módulo cierra apuntando al 11.

M11 (D6, D7), sin partirlo:
- ETS, el naïve estacional, RMSE, MAE y MAPE se presentan en una frase en su primer uso.
- La comparación de los ocho métodos se muestra una sola vez: la tabla ordenable, con Escala y k, y
  con una descripción y un pie que no adelantan nada (`chapter.js`). Sale la tabla estática; la
  lectura del simulador deja de repetir el ranking y da el sesgo medio de cada método encendido.
- El aviso «Esa conclusión es falsa» dice cómo se construyen los 61 orígenes y qué promedia la tabla.
- El clímax gana un bloque de R y de Python que lo reproduce; la nota que lo prometía remite a él.
- «once módulos» pasa a «diez»; el resumen sigue siendo lo último antes de la evaluación."""

BLOQUE_R = r'''library(forecast)
apb <- AirPassengers; ap <- log(apb)
ent  <- window(ap,  end = c(1958, 12))           # 120 meses para entrenar
ento <- window(apb, end = c(1958, 12))
obs  <- as.numeric(window(apb, start = c(1959, 1)))   # los 24 meses de prueba
mediana <- function(p) exp(as.numeric(p))       # exp() del pronostico en log

# --- 1. Una sola particion ---------------------------------------------------
# La armonica usa el K = 6 de la tabla del Modulo 10. El SARIMA con calendario
# (RMSE 45.48) lo calcula el bloque del Modulo 9.
pron <- list(
  ets_log  = mediana(forecast(ets(ent), h = 24)$mean),
  armonica = mediana(forecast(auto.arima(ent, xreg = fourier(ent, K = 6), seasonal = FALSE,
                                         stepwise = FALSE, approximation = FALSE),
                              xreg = fourier(ent, K = 6, h = 24))$mean),
  stl      = mediana(forecast(stlm(ent, s.window = "periodic", method = "arima"), h = 24)$mean),
  sarima   = mediana(forecast(Arima(ent, order = c(0, 1, 1),
                                    seasonal = list(order = c(0, 1, 1), period = 12)), h = 24)$mean),
  ets      = as.numeric(forecast(ets(ento), h = 24)$mean),
  snaive   = as.numeric(snaive(ento, h = 24)$mean))
as.character(auto.arima(ent, stepwise = FALSE, approximation = FALSE))   # el mismo airline
#> [1] "ARIMA(0,1,1)(0,1,1)[12]"
metricas <- function(p) { e <- obs - p
  c(rmse = sqrt(mean(e^2)), mae = mean(abs(e)), mape = 100 * mean(abs(e / obs)), sesgo = mean(e)) }
round(t(sapply(pron, metricas)), 2)
#>           rmse   mae  mape sesgo
#> ets_log  19.43 16.12  3.55  8.92
#> armonica 19.51 14.69  3.15  3.22
#> stl      35.48 30.29  6.33 28.29
#> sarima   43.18 39.45  8.52 39.45
#> ets      72.55 63.21 13.30 63.21
#> snaive   76.99 71.25 15.52 71.25
all(obs > pron$sarima)        # el SARIMA se queda corto los 24 meses: sesgo = MAE
#> [1] TRUE

# --- 2. El anio en que el trafico casi no crecio ------------------------------
tot <- setNames(colSums(matrix(as.numeric(apb), nrow = 12)), 1949:1960)
round(100 * (tot[-1] / tot[-12] - 1), 1)       # crecimiento del total anual, %
#> 1950 1951 1952 1953 1954 1955 1956 1957 1958 1959 1960
#> 10.3 21.8 15.8 14.2  6.2 18.9 15.6 12.2  3.4 12.4 11.2
crece <- function(p) round(100 * c(en_1959 = sum(p[1:12]) / tot[["1958"]] - 1,
                                   en_1960 = sum(p[13:24]) / sum(p[1:12]) - 1), 1)
rbind(sarima = crece(pron$sarima), ets_log = crece(pron$ets_log), armonica = crece(pron$armonica))
#>          en_1959 en_1960
#> sarima       4.7     6.9
#> ets_log      9.4    12.8
#> armonica    10.6    13.1

# --- 3. La misma comparacion desde 61 origenes --------------------------------
# Cada origen k entrena con los meses 1..k y pronostica los 24 siguientes, o los
# que queden. Los 12 primeros sirven para h = 12 (origenes 72 a 132, de 1954-12 a
# 1959-12) y los 24 para h = 24 (72 a 120). Tarda menos de un minuto: para eso la
# armonica se busca aqui por pasos (el valor por defecto de auto.arima), no de forma
# exhaustiva como en la particion; con la exhaustiva su RMSE medio a h = 12 baja a
# 21.06, por delante del ETS sobre el log (lo calcula el generador de los datos
# del capitulo; tarda minuto y medio).
metodos <- list(
  sarima   = function(l, o, h) mediana(forecast(Arima(l, order = c(0, 1, 1),
                 seasonal = list(order = c(0, 1, 1), period = 12)), h = h)$mean),
  ets_log  = function(l, o, h) mediana(forecast(ets(l), h = h)$mean),
  stl      = function(l, o, h) mediana(forecast(stlm(l, s.window = "periodic",
                                                     method = "arima"), h = h)$mean),
  armonica = function(l, o, h) mediana(forecast(auto.arima(l, xreg = fourier(l, K = 6),
                 seasonal = FALSE), xreg = fourier(l, K = 6, h = h))$mean),
  ets      = function(l, o, h) as.numeric(forecast(ets(o), h = h)$mean),
  snaive   = function(l, o, h) as.numeric(snaive(o, h = h)$mean))
origenes <- 72:132
E <- lapply(origenes, function(k) {            # errores: una matriz h x 6 por origen
  h <- min(24, 144 - k)
  l <- window(ap, end = time(ap)[k]); o <- window(apb, end = time(ap)[k])
  sapply(metodos, function(f) as.numeric(apb)[k + 1:h] - f(l, o, h))
})
rmse <- function(H) t(sapply(E[origenes <= 144 - H], function(e) sqrt(colMeans(e[1:H, ]^2))))
R12 <- rmse(12); R24 <- rmse(24)               # un RMSE por origen y metodo
c(h12 = nrow(R12), h24 = nrow(R24))
#> h12 h24
#>  61  49
round(colMeans(R12), 2)                        # el promedio de los 61 RMSE
#>   sarima  ets_log      stl armonica      ets   snaive
#>    16.81    21.42    21.85    22.38    26.38    41.24
round(100 * colMeans(R12 < R12[, "sarima"]), 1)   # % de origenes en que le gana
#>   sarima  ets_log      stl armonica      ets   snaive
#>      0.0      8.2      8.2      9.8     14.8     11.5
mes <- format(seq(as.Date("1949-01-01"), by = "month", length.out = 144), "%Y-%m")
mes[origenes[apply(R12, 1, which.min) != 1]]   # donde el SARIMA no es el mejor
#>  [1] "1955-05" "1956-06" "1957-05" "1957-06" "1957-07" "1957-08" "1957-09"
#>  [8] "1957-10" "1957-11" "1957-12" "1958-01" "1958-11" "1958-12" "1959-01"

# --- 4. A 24 meses, y midiendo solo el error del mes 12 -----------------------
round(colMeans(R24), 2)
#>   sarima  ets_log      stl armonica      ets   snaive
#>    26.00    26.61    27.80    28.30    34.84    59.53
round(100 * colMeans(R24 < R24[, "sarima"]), 1)
#>   sarima  ets_log      stl armonica      ets   snaive
#>      0.0     49.0     32.7     32.7     40.8      8.2
round(colMeans(abs(t(sapply(E, function(e) e[12, ])))), 2)
#>   sarima  ets_log      stl armonica      ets   snaive
#>    18.22    15.96    16.27    16.17    23.61    38.61'''

BLOQUE_PY = r'''import numpy as np, pandas as pd, statsmodels.api as sm, warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
warnings.simplefilter("ignore", RuntimeWarning)   # solo avisos de coma flotante de numpy

y = sm.datasets.get_rdataset("AirPassengers").data["value"].to_numpy(dtype=float)
meses = pd.date_range("1949-01", periods=len(y), freq="MS")

def airline(k, h):
    """El airline sobre log(y) con los k primeros meses: mediana de h pasos."""
    s = pd.Series(np.log(y[:k]), index=meses[:k])
    modelo = dict(order=(0, 1, 1), seasonal_order=(0, 1, 1, 12), trend="n")
    # Se estima diferenciando, como R, y se pronostica con el modelo en niveles:
    # con simple_differencing=True, get_forecast() daria la serie diferenciada.
    est = SARIMAX(s, simple_differencing=True, **modelo).fit(disp=False, method="bfgs", maxiter=1000)
    f = SARIMAX(s, **modelo).filter(est.params)
    return np.exp(f.get_forecast(h).predicted_mean.to_numpy()), est.mle_retvals["converged"]

def naive_estacional(k, h):
    return y[k - 12 + np.arange(h) % 12]           # repite los ultimos 12 meses

# statsmodels no trae ets() ni la eleccion automatica de auto.arima: aqui van el
# SARIMA y el naive estacional; los otros cuatro metodos, en el bloque de R.

# --- 1. Una sola particion: entrenar con 120 meses, hasta 1958-12 -------------
obs = y[120:]
p_sar, ok = airline(120, 24)
print(ok)
#> True
for nombre, p in (("sarima", p_sar), ("snaive", naive_estacional(120, 24))):
    e = obs - p                                     # rmse, mae, mape y sesgo
    print(nombre, np.round([np.sqrt(np.mean(e**2)), np.mean(np.abs(e)),
                            100 * np.mean(np.abs(e / obs)), np.mean(e)], 2))
#> sarima [43.18 39.45  8.52 39.45]
#> snaive [76.99 71.25 15.52 71.25]

# --- 2. El crecimiento de los totales anuales ---------------------------------
tot = y.reshape(12, 12).sum(axis=1)               # una fila por anio, 1949-1960
print(np.round(100 * (tot[1:] / tot[:-1] - 1), 1))
#> [10.3 21.8 15.8 14.2  6.2 18.9 15.6 12.2  3.4 12.4 11.2]
print(np.round(100 * np.array([p_sar[:12].sum() / tot[9] - 1,      # 1959 frente a 1958
                               p_sar[12:].sum() / p_sar[:12].sum() - 1]), 1))
#> [4.7 6.9]

# --- 3. 61 origenes, h = 12: el SARIMA frente al naive estacional --------------
rmse = {"sarima": [], "snaive": []}
convergieron = 0
for k in range(72, 133):                          # de 1954-12 a 1959-12
    o = y[k:k + 12]
    p, ok = airline(k, 12)
    convergieron += ok
    rmse["sarima"].append(np.sqrt(np.mean((o - p) ** 2)))
    rmse["snaive"].append(np.sqrt(np.mean((o - naive_estacional(k, 12)) ** 2)))
r = {m: np.array(v) for m, v in rmse.items()}
print(len(r["sarima"]), convergieron)             # origenes y ajustes que convergieron
#> 61 61
print(np.round([r["sarima"].mean(), r["snaive"].mean()], 2),
      round(100 * np.mean(r["snaive"] < r["sarima"]), 1))
#> [16.81 41.24] 11.5'''


def registra(c, mover, entre, despues, esc, T1011, CJS, **_):
    # ================================================================ M10
    c("M10 · «media horarios», dicho", T1011,
      r'''o media horarios ($m = 48$ y $m = 336$ a la vez)''',
      r'''o tomados cada media hora con un patrón diario y otro semanal ($m = 48$ y $m = 336$ a la vez)''')
    c("M10 · η_t para el error de la regresión armónica", T1011,
      r'''          &+ \sum_{k=1}^{K}\delta_k \cos\!\left(\frac{2\pi k t}{m}\right) + n_t
        \end{aligned}$$
        <p style="margin-bottom:0;">con $n_t$ un ARIMA''',
      r'''          &+ \sum_{k=1}^{K}\delta_k \cos\!\left(\frac{2\pi k t}{m}\right) + \eta_t
        \end{aligned}$$
        <p style="margin-bottom:0;">con $\eta_t$, como en el Módulo 9, un ARIMA''')
    c("M10 · intro de armonicos-K: estado inicial y una pregunta, sin el resultado", T1011,
      r'''          $p$-valor de Ljung–Box. Fíjate en dónde deja de rechazar el diagnóstico: hasta $K=4$ los residuales
          conservan estructura estacional, y hace falta llegar a $K=5$ para que la sinusoide represente bien el pico de
          verano.</p>''',
      r'''          $p$-valor de Ljung–Box. Se abre en $K = 3$. Fíjate en dónde deja de rechazar el diagnóstico: ¿desde qué
          $K$ dejan los residuales de conservar estructura estacional?</p>''')
    c("M10 · la columna «Parámetros totales», explicada", T1011,
      r'''      <div class="warning">
        <p><strong>La trampa de esta tabla, y es la lección central del módulo.</strong>''',
      r'''      <p>«Parámetros totales» suma los términos de Fourier, los coeficientes del ARIMA de los errores y su deriva
        (<em>drift</em>), que <code>auto.arima</code> añade aquí porque los errores llevan $d = 1$: con $K = 6$,
        $11 + 4 + 1 = 16$. La varianza $\sigma^2$ no se cuenta.</p>

      <div class="warning">
        <p><strong>La trampa de esta tabla, y es la lección central del módulo.</strong>''')
    c("M10 · cierre que apunta al Módulo 11", T1011,
      esc('''# componente estacional de otra forma.''') + '''</code></pre>
        </div>
      </div>
    </div>''',
      esc('''# componente estacional de otra forma.''') + '''</code></pre>
        </div>
      </div>

      <p>La tabla de este módulo compara armónicos entre sí; entre familias distintas, el AICc no sirve. El
        Módulo 11 hace esa comparación de la manera que sí vale, fuera de muestra, y mira qué pasa cuando se repite
        desde muchos cortes.</p>
    </div>''')

    # ================================================================ M11 · plantilla
    entre("M11 · la comparación: presentaciones, una sola tabla, el aviso de los 61 orígenes", T1011,
          '''      <p>Todo el capítulo ha usado criterios <em>dentro</em> de la muestra''',
          '''            <tr><th>Método</th><th>RMSE medio sobre $61$ orígenes</th>''',
          r'''      <p>Todo el capítulo ha usado criterios <em>dentro</em> de la muestra, y el Módulo 10 acaba de mostrar que entre
        familias distintas eso no vale. La alternativa evidente es comparar <strong>fuera de muestra</strong>: partir
        la serie, entrenar con los primeros $120$ meses, hasta 1958-12, y medir el error de pronóstico en los últimos
        $24$. El error se mide de tres maneras, siempre en pasajeros y en la escala original, la única en la que los
        métodos son comparables: el <strong>RMSE</strong>, la raíz del error cuadrático medio, que castiga más los
        errores grandes; el <strong>MAE</strong>, el error absoluto medio; y el <strong>MAPE</strong>, el error
        absoluto medio en porcentaje de lo observado.</p>

      <p>Entran ocho métodos. Cinco son de la familia ARIMA y ya han salido en el capítulo, todos sobre el logaritmo:
        el <em>airline</em>, el modelo que elige <code>auto.arima</code>, el <em>airline</em> con el calendario del
        Módulo 9, y la regresión armónica y el STL + ARIMA del Módulo 10. Los otros tres son nuevos. El
        <strong>ETS</strong> extiende el suavizamiento exponencial simple y el método de Holt del Capítulo 4
        (Módulo 1) con un componente estacional: suaviza por separado el nivel, la tendencia y la estación, y sus
        tres letras dicen cómo entra cada uno —primero el error, después la tendencia y la estación—: $A$ aditivo,
        $A_d$ aditivo amortiguado, $M$ multiplicativo. Se ajusta en las dos escalas: sobre la serie cruda, donde su
        estacionalidad multiplicativa es la natural, y sobre el logaritmo, la misma escala que el ARIMA. El
        <strong>naïve estacional</strong> es la referencia mínima: pronostica cada mes con el valor del mismo mes del
        último año observado, sin estimar nada. La columna $k$ cuenta los parámetros estimados, sin la varianza
        $\sigma^2$: en el STL + ARIMA, los $11$ valores de la estacionalidad además de los $2$ parámetros del ARIMA,
        y en la armónica, también la deriva.</p>

      <!--RANKING:comparativa|Los ocho métodos sobre una sola partición|-->

      <div class="simulador" data-simulador="comparativa-particion">
        <h4><i class="fas fa-trophy" aria-hidden="true"></i> Ocho métodos sobre los últimos 24 meses</h4>
        <p class="simulador-intro">Los interruptores encienden y apagan métodos en el gráfico. Los ocho pronósticos
          están calculados en R sobre el mismo conjunto de entrenamiento (hasta 1958-12). Se abre con lo observado y
          los cuatro primeros métodos por RMSE; con todos apagados queda solo lo observado. La lectura da, de cada
          método encendido, su <strong>sesgo medio</strong>: lo observado menos lo pronosticado, en promedio de los
          $24$ meses, positivo si el método se queda corto. Antes de seguir leyendo, mira de qué lado de lo observado
          cae cada curva.</p>
        <div class="simulador-controles"></div>
        <div class="simulador-lectura"></div>
        <div class="grafico-wrapper" style="height:320px;">
          <canvas aria-label="Pronósticos de los ocho métodos frente a lo observado" role="img"></canvas>
        </div>
      </div>

      <p>Leída sin más, la tabla es un veredicto. Arriba quedan casi empatados el ETS sobre el logaritmo, primero por
        RMSE, y la regresión armónica, primera por MAE ($14.69$ frente a $16.12$) y por MAPE. El modelo que ha
        ocupado diez módulos queda <strong>cuarto</strong> con las tres métricas, con más del doble de RMSE que el
        ganador, y ni siquiera le gana al ETS aplicado sobre la misma escala. Un lector razonable cerraría el
        capítulo concluyendo que el SARIMA no vale para esta serie.</p>

      <p>Una salvedad sobre la armónica: su $K = 6$ se eligió por AICc sobre la serie completa (la tabla del
        Módulo 10), con los $24$ meses de prueba dentro; con solo el entrenamiento el AICc elige $K = 5$, que da un
        RMSE de $19.58$ en vez de $19.51$ (ese cálculo lo hace el generador de los datos del capítulo, no el
        bloque de abajo). Es una ventaja indebida, pequeña, y no cambia el orden de
        la tabla.</p>

      <h3>La misma comparación, desde $61$ orígenes</h3>

      <div class="warning">
        <p><strong>Esa conclusión es falsa.</strong> Repitiendo la comparación desde <strong>$61$ orígenes</strong> en
          vez de uno —el corte avanza mes a mes, de 1954-12 a 1959-12; en cada corte se reajusta todo y se mide el
          RMSE de los $12$ meses siguientes—, el SARIMA <strong>pasa de cuarto a primero</strong>. La tabla de abajo
          da el promedio de esos $61$ RMSE. Entran los seis métodos distintos: <code>auto.arima</code> elige el mismo
          <em>airline</em>, y el calendario queda fuera.</p>
      </div>

      <div class="diagram">
        <table>
          <thead>
''')

    c("M11 · el orden tras el SARIMA, cierto con las dos búsquedas de la armónica (V5)", T1011,
      r'''        orígenes</strong>. El resto del orden apenas se mueve: el ETS sobre el logaritmo sigue por delante del STL y de
        la armónica, y el ETS sobre la serie cruda y el naïve siguen últimos.</p>''',
      r'''        orígenes</strong>. Detrás, el ETS sobre el logaritmo, el STL y la armónica quedan cerca unos de otros, y el ETS
        sobre la serie cruda y el naïve siguen últimos. Una salvedad sobre la armónica: en cada origen se busca por
        pasos —el valor por defecto de <code>auto.arima</code>—, para que el bloque de abajo tarde menos de un minuto.
        Con la búsqueda exhaustiva de la partición, su RMSE medio baja a $21.06$ y queda por delante del ETS sobre el
        logaritmo ($21.42$): entre esos dos, el orden depende de la búsqueda y la diferencia es pequeña. El SARIMA
        sigue primero con las dos (la cifra exhaustiva la calcula el generador de los datos del capítulo).</p>''')
    c("M11 · «la tabla anterior» es la de la partición (V12)", T1011,
      '''      <p>Lo que ocurría en la tabla anterior no tiene que ver''',
      '''      <p>Lo que ocurría en la tabla de la partición no tiene que ver''')
    c("M11 · la tabla de los 61 orígenes dice cómo se buscó la armónica", T1011,
      r'''<tr><td>Regresión armónica $K=6$</td><td>$22.38$</td>''',
      r'''<tr><td>Regresión armónica $K=6$ (búsqueda por pasos)</td><td>$22.38$</td>''')
    c("M11 · el bloque del clímax, antes del puente con el Capítulo 6", T1011,
      '''      <div class="note">
        <p><strong>Puente con el Capítulo 6.</strong> Lo que acaba de pasar —una conclusión que se invierte al cambiar
          la partición— es exactamente el problema que el capítulo siguiente resuelve: validación de <em>origen
          móvil</em>, cobertura empírica de los intervalos frente a la nominal, y métricas que se puedan comparar entre
          series. Aquí se han citado sus resultados como advertencia; allí se construye el método.</p>
      </div>''',
      '''      <p>El bloque siguiente reproduce todo lo anterior salvo la salvedad del $K$ de la armónica y su búsqueda
        exhaustiva en los orígenes: la tabla de la partición (el SARIMA con calendario lo calcula el bloque del
        Módulo 9), el crecimiento de cada año y los dos horizontes desde muchos orígenes. En R
        tarda menos de un minuto. En Python, <code>statsmodels</code> no trae <code>ets()</code> ni la elección
        automática de <code>auto.arima</code>, y el bloque se queda con el SARIMA y el naïve estacional.</p>

      <div class="code-tabs">
        <div class="code-tabs-nav" role="tablist" aria-label="La comparación desde muchos orígenes">
          <button class="code-tab-btn active" data-lang="r" role="tab" aria-selected="true">R</button>
          <button class="code-tab-btn" data-lang="python" role="tab" aria-selected="false">Python</button>
        </div>
        <div class="code-tab-panel active" data-lang="r">
          <pre><code class="language-r">''' + esc(BLOQUE_R) + '''</code></pre>
        </div>
        <div class="code-tab-panel" data-lang="python" hidden>
          <pre><code class="language-python">''' + esc(BLOQUE_PY) + '''</code></pre>
        </div>
      </div>

      <div class="note">
        <p><strong>Puente con el Capítulo 6.</strong> Lo que acaba de pasar —una conclusión que se invierte al cambiar
          la partición— es exactamente el problema que el capítulo siguiente resuelve: validación de <em>origen
          móvil</em>, cobertura empírica de los intervalos frente a la nominal, y métricas que se puedan comparar entre
          series. Aquí solo se ha medido, como advertencia; allí se construye el método.</p>
      </div>''')

    c("M11 · la nota de las cifras remite al bloque, no a «el código del capítulo»", T1011,
      '''          serie y se pueden reproducir con el código del capítulo.</p>''',
      '''          serie y las reproduce el bloque de código de la comparación.</p>''')

    # ================================================================ M11 · chapter.js
    c("M11 · simulador: sin selector de métrica (la tabla ordenable ya ordena)", CJS,
      '''      const params = { metrica: 'rmse' };
      claves.forEach((k, i) => { params['m_' + k] = i < 3 || k === 'sarima'; });''',
      '''      const params = {};
      claves.forEach((k, i) => { params['m_' + k] = i < 3 || k === 'sarima'; });
      // Sesgo medio sobre la prueba: lo observado menos lo pronosticado.
      const sesgo = k => comp.observado.reduce((s, o, j) => s + o - comp.modelos[k].pronostico[j], 0) /
        comp.observado.length;''')
    c("M11 · lectura: el sesgo de cada método encendido, no el ranking otra vez", CJS,
      '''        const met = params.metrica;
        const orden = claves.slice().sort((a, b) => comp.modelos[a][met] - comp.modelos[b][met]);
        const campos = [
          { etiqueta: 'entrena hasta', valor: comp.corte + ` (n = ${comp.n_entrenamiento})` },
          { etiqueta: 'prueba', valor: comp.n_prueba + ' meses' }
        ];
        orden.forEach((k, i) => campos.push({
          etiqueta: `${i + 1}. ${comp.modelos[k].nombre}`,
          valor: fmt(comp.modelos[k][met], 3) + (met === 'mape' ? '\\u00a0%' : '') + (k === 'sarima' ? '  ← el SARIMA' : '')
        }));
        actualizarLectura(lectura, campos);''',
      '''        // La lectura no repite el ranking, que ya da la tabla ordenable de arriba:
        // da el sesgo medio de cada método encendido, que es lo que explica el
        // párrafo del crecimiento de 1958.
        const campos = [
          { etiqueta: 'entrena hasta', valor: comp.corte + ` (n = ${comp.n_entrenamiento})` },
          { etiqueta: 'prueba', valor: comp.n_prueba + ' meses' },
          { etiqueta: 'sesgo medio', valor: 'observado − pronóstico; positivo si se queda corto' }
        ];
        encendidos.forEach(k => campos.push({
          etiqueta: comp.modelos[k].nombre,
          valor: fmt(sesgo(k), 2) + '\\u00a0pasajeros'
        }));
        if (!encendidos.length) campos.push({ etiqueta: 'métodos encendidos', valor: 'ninguno' });
        actualizarLectura(lectura, campos);''')
    c("M11 · sin el selector de métrica", CJS,
      '''      crearSelector(controles, {
        clave: 'metrica', etiqueta: 'Métrica del ranking',
        opciones: [
          { valor: 'rmse', texto: 'RMSE' },
          { valor: 'mae', texto: 'MAE' },
          { valor: 'mape', texto: 'MAPE (%)' }
        ]
      }, params, pintar);
      crearInterruptores(controles,''',
      '''      crearInterruptores(controles,''')
    c("M11 · tabla ordenable: Escala y k, y una descripción y un pie que no adelantan", CJS,
      '''    // Tabla ordenable de la comparativa sobre UNA partición. El pie recuerda que
    // este ranking se desmiente en el capítulo 6 con 61 orígenes.
    TABLAS_RANKING['comparativa'] = function () {
      const claves = AP.comparativa.orden_rmse;
      return {
        descripcion: 'Los ocho métodos sobre los últimos ' + AP.comparativa.n_prueba +
          ' meses, una sola partición. Pulsa las cabeceras: por RMSE gana el ETS sobre el ' +
          'logaritmo y por MAE y MAPE la regresión armónica, pero las tres dejan al SARIMA cuarto.',
        columnas: [
          { clave: 'modelo', titulo: 'Método', tipo: 'texto' },''',
      '''    // Tabla ordenable de la comparativa sobre UNA partición: es la única vez que el
    // capítulo muestra las tres métricas de los ocho métodos. La descripción y el
    // pie no adelantan el resultado; lo cuenta la prosa de después.
    TABLAS_RANKING['comparativa'] = function () {
      const comp = AP.comparativa;
      const claves = comp.orden_rmse;
      return {
        descripcion: 'Los ocho métodos sobre los últimos ' + comp.n_prueba +
          ' meses, una sola partición. Pulsa una cabecera para ordenar por esa métrica.',
        columnas: [
          { clave: 'modelo', titulo: 'Método', tipo: 'texto' },''')
    c("M11 · tabla ordenable: Escala y k, detrás de las métricas (V10)", CJS,
      '''          { clave: 'mape', titulo: 'MAPE', decimales: 2, sufijo: ' %', mejor: 'menor' }
        ],''',
      '''          { clave: 'mape', titulo: 'MAPE', decimales: 2, sufijo: ' %', mejor: 'menor' },
          { clave: 'escala', titulo: 'Escala', tipo: 'texto' },
          { clave: 'k', titulo: 'k', tipo: 'texto' }
        ],''')
    c("M11 · leyenda corta del simulador: «Naïve» (V15)", CJS,
      "ets: 'ETS (cruda)', snaive: 'Naive est.' };",
      "ets: 'ETS (cruda)', snaive: 'Naïve est.' };")
    c("quiz · retro de la pregunta 1, solo la remisión a las evidencias (V3, autorizado por la maestra)", CJS,
      "Cuatro evidencias independientes (Módulo 8) muestran que esta serie no tiene estacionalidad.",
      "Las comprobaciones del Módulo 8 muestran que esta serie no tiene estacionalidad.")
    c("M11 · tabla ordenable: filas con Escala y k, y el pie", CJS,
      '''        filas: claves.map(k => ({
          modelo: AP.comparativa.modelos[k].nombre,
          rmse: AP.comparativa.modelos[k].rmse,
          mae: AP.comparativa.modelos[k].mae,
          mape: AP.comparativa.modelos[k].mape
        })),
        formato: fmt,
        inicial: 'rmse',
        pie: 'Las tres métricas coinciden en el cuarto puesto y aun así es engañoso: sobre ' +
          '61 orígenes, midiendo los 12 meses siguientes a cada corte, el SARIMA pasa a primero. ' +
          'El Capítulo 6 construye esa evaluación.'
      };''',
      '''        filas: claves.map(k => ({
          modelo: comp.modelos[k].nombre,
          escala: comp.modelos[k].escala,
          // El STL + ARIMA estima además los m − 1 = 11 valores libres de la estación.
          k: k === 'stl_arima' ? comp.modelos[k].n_par + ' + ' + (12 - 1) : String(comp.modelos[k].n_par),
          // Sin redondear: las de 3 decimales, redondeadas otra vez a 2, suben
          // 16.1249 a 16.13 y 76.9946 a 77.00 (R da 16.12 y 76.99).
          rmse: comp.modelos[k].exactas.rmse,
          mae: comp.modelos[k].exactas.mae,
          mape: comp.modelos[k].exactas.mape
        })),
        formato: fmt,
        inicial: 'rmse',
        pie: 'Entrenamiento: los ' + comp.n_entrenamiento + ' meses hasta ' + comp.corte +
          '; prueba: de ' + comp.fechas_prueba[0] + ' a ' + comp.fechas_prueba[comp.fechas_prueba.length - 1] +
          '. Los errores, en pasajeros y en la escala original (el MAPE, en porcentaje); <em>k</em>, lo que ' +
          'estima cada método.'
      };''')
