"""R3 · Módulo 1 · el módulo empieza por las raíces; los convenios de signo y las diferencias
entre R y Python pasan a una sección al final, y su primer bloque deja de estimar un ARMA(1,1)."""


def registra(c, mover, MOD, **_):
    c("M1 · la entrada ya no dice «de contrabando» y anuncia el orden del módulo", MOD,
      r'''      <p>En el Capítulo 2 apareció, casi de contrabando, el operador $B$ para escribir la diferencia como
        $\nabla y_t = (1-B)y_t$. Ese atajo de notación es en realidad la herramienta central del análisis clásico de
        series de tiempo, y conviene presentarla en serio antes de construir modelos con ella.</p>''',
      r'''      <p>En el Capítulo 2 se usó el operador $B$ para escribir la diferencia como $\nabla y_t = (1-B)y_t$ y para
        explicar el nombre de la raíz unitaria. Ese atajo de notación es en realidad la herramienta central del
        análisis clásico de series de tiempo, y conviene presentarla en serio antes de construir modelos con ella. El
        módulo va de la notación a la condición de las raíces; los convenios de signo y las diferencias entre R y
        Python, que dan tropiezos, quedan para el final.</p>''')

    c("M1 · los signos, en una frase tras los polinomios; el aviso pasa a su sección", MOD,
      r'''        $$\theta(B) = 1 + \theta_1 B + \cdots + \theta_q B^q$$
      </div>

      <div class="warning">
        <p><strong>Ojo con los signos.</strong> Los coeficientes $\phi$ entran <strong>restando</strong> y los $\theta$
          <strong>sumando</strong>. No es un capricho: así, al pasar todo al mismo lado, un AR queda
          $\phi(B)y_t = \varepsilon_t$ y un MA queda $y_t = \theta(B)\varepsilon_t$, con los signos "naturales" en la
          forma en que se escribe cada modelo. La consecuencia práctica es que <strong>R y Python usan este mismo
            convenio</strong>, pero algunos textos —y algún paquete— invierten el signo de $\theta$. Si un $\theta$
          estimado te sale con el signo contrario al que esperabas, comprueba el convenio antes de dudar de tus datos.</p>''',
      r'''        $$\theta(B) = 1 + \theta_1 B + \cdots + \theta_q B^q$$
      </div>

      <p>Los coeficientes $\phi$ entran <strong>restando</strong> y los $\theta$ <strong>sumando</strong>. No es un
        capricho: así, al pasar todo al mismo lado, un AR queda $\phi(B)y_t = \varepsilon_t$ y un MA queda
        $y_t = \theta(B)\varepsilon_t$, con los signos «naturales» en la forma en que se escribe cada modelo (los dos
        modelos se definen en los Módulos 2 y 3; aquí solo importa la notación). Algunos textos y paquetes escriben el
        MA con el signo contrario: cómo comprobarlo, y qué otras diferencias hay entre R y Python, está al final del
        módulo.</p>

      <h3>Convenios de signo y diferencias entre R y Python</h3>

      <div class="warning">
        <p><strong>Ojo con los signos.</strong> El convenio de este capítulo —los $\phi$ restando, los $\theta$
          sumando— es <strong>el que usan R y Python</strong>, pero algunos textos —y algún paquete— invierten el signo
          de $\theta$. Si un $\theta$ estimado te sale con el signo contrario al que esperabas, comprueba el convenio
          antes de dudar de tus datos.</p>''')

    c("M1 · la comprobación del convenio, con un MA(1) y sin AIC", MOD,
      r'''      <p>Comprobar cuál usa un paquete no requiere leer su documentación: basta ajustar una serie simulada con un
        $\theta$ conocido y mirar el signo que devuelve. Aquí la serie se genera una sola vez en R y se ajusta en los
        dos lenguajes, para que la comparación sea sobre los mismos números.</p>''',
      r'''      <p>Comprobar cuál usa un paquete no requiere leer su documentación: basta ajustar una serie simulada con un
        $\theta$ conocido y mirar el signo que devuelve. El bloque lo hace con un MA(1) de $\theta = +0.7$, el modelo
        que el Capítulo 2 adelantó; el estimador que devuelve $\hat\theta$ es el del Módulo 7, y por ahora solo importa
        su signo. Cada lenguaje simula su propia serie, así que las cifras difieren; el signo, no.</p>''')

    c("M1 · bloque R del convenio: MA(1) en lugar de ARMA(1,1), sin escribir serie.csv", MOD,
      r'''          <pre><code class="language-r"># ARMA(1,1) con phi = 0.6 y theta = 0.7, ambos POSITIVOS
set.seed(2026)
x &lt;- arima.sim(model = list(ar = 0.6, ma = 0.7), n = 600)
write.csv(data.frame(x = as.numeric(x)), "serie.csv", row.names = FALSE)

arima(x, order = c(1, 0, 1), include.mean = FALSE)
#&gt; Coefficients:
#&gt;          ar1     ma1
#&gt;       0.5999  0.6925
#&gt; s.e.  0.0364  0.0355
#&gt;
#&gt; sigma^2 estimated as 0.9992:  log likelihood = -852.03,  aic = 1710.05

# ma1 sale POSITIVO: convenio de suma, el mismo del capitulo.''',
      r'''          <pre><code class="language-r"># Convenio de suma (el de este capitulo y el de R): un MA(1) con theta = +0.7
# tiene rho_1 = theta / (1 + theta^2), POSITIVA
round(ARMAacf(ma = 0.7, lag.max = 3), 4)
#&gt;      0      1      2      3
#&gt; 1.0000 0.4698 0.0000 0.0000

set.seed(2026)
x &lt;- arima.sim(model = list(ma = 0.7), n = 600)   # arima.sim recibe el theta del modelo
round(acf(x, plot = FALSE)$acf[2], 4)             # r_1 muestral: positiva, como rho_1
#&gt; [1] 0.4614

# El estimador (Modulo 7) devuelve el signo que usa el paquete
round(coef(arima(x, order = c(0, 0, 1), include.mean = FALSE)), 4)
#&gt;    ma1
#&gt; 0.6887

# ma1 sale POSITIVO: convenio de suma, el mismo del capitulo.''')

    c("M1 · bloque Python del convenio: autosuficiente (sin serie.csv) y con AR(1) en lugar de ARMA(1,1)", MOD,
      r'''          <pre><code class="language-python">import numpy as np, pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima_process import ArmaProcess

x = pd.read_csv("serie.csv")["x"].to_numpy()          # LA MISMA serie de R
fit = ARIMA(x, order=(1, 0, 1), trend="n").fit()

print(fit.param_names, fit.params.round(4))
# ['ar.L1', 'ma.L1', 'sigma2'] [0.5999 0.6925 0.9992]
# Identico a R hasta el cuarto decimal, y con el mismo signo positivo.

print(np.round(fit.polynomial_ar, 4))   # [ 1.     -0.5999]  ->  phi(B)   = 1 - 0.5999 B
print(np.round(fit.polynomial_ma, 4))   # [1.     0.6925]    ->  theta(B) = 1 + 0.6925 B

# PERO al SIMULAR, statsmodels no pide los coeficientes del modelo sino
# los del POLINOMIO. Como phi(B) = 1 - phi1*B, el AR va NEGADO:
bien = ArmaProcess(ar=np.array([1, -0.6]), ma=np.array([1, 0.7]))
mal  = ArmaProcess(ar=np.array([1,  0.6]), ma=np.array([1, 0.7]))

print(bien.arcoefs, np.round(bien.acf(5)[1:], 4))
# [0.6]  [0.7923 0.4754 0.2852 0.1711]    &lt;- lo que se queria
print(mal.arcoefs,  np.round(mal.acf(5)[1:], 4))
# [-0.6] [ 0.0892 -0.0535  0.0321 -0.0193]  &lt;- otro modelo, sin avisar</code></pre>''',
      r'''          <pre><code class="language-python">import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess, arma_acf
from statsmodels.tsa.arima.model import ARIMA

# Convenio de suma tambien en statsmodels: rho_1 positiva para theta = +0.7
print(np.round(arma_acf(np.r_[1], np.r_[1, 0.7], lags=4), 4))
# [1.     0.4698 0.     0.    ]

# Cada lenguaje simula su propia serie: las cifras difieren de las de R, el signo no
x = ArmaProcess(np.r_[1], np.r_[1, 0.7]).generate_sample(
    nsample=600, distrvs=np.random.default_rng(3).standard_normal)
print(round(float(np.corrcoef(x[1:], x[:-1])[0, 1]), 4))   # r_1 muestral
# 0.4575
fit = ARIMA(x, order=(0, 0, 1), trend="n").fit()
print(fit.param_names, fit.params.round(4))
# ['ma.L1', 'sigma2'] [0.6979 0.9847]    &lt;- ma.L1 POSITIVO, como en R

# PERO al SIMULAR un AR, statsmodels no pide los coeficientes del modelo sino
# los del POLINOMIO. Como phi(B) = 1 - phi1*B, el AR va NEGADO:
bien = ArmaProcess(ar=np.array([1, -0.6]), ma=np.array([1]))
mal  = ArmaProcess(ar=np.array([1,  0.6]), ma=np.array([1]))

print(bien.arcoefs, np.round(bien.acf(5)[1:], 4))
# [0.6]  [0.6    0.36   0.216  0.1296]    &lt;- lo que se queria
print(mal.arcoefs,  np.round(mal.acf(5)[1:], 4))
# [-0.6] [-0.6    0.36  -0.216   0.1296]   &lt;- otro proceso, sin avisar</code></pre>''')

    c("M1 · la regla del AR negado, con el AR(1) del bloque y la remisión hacia atrás", MOD,
      r'''          Escribir <code>ar=[1, 0.6]</code> en vez de <code>ar=[1, -0.6]</code> no produce ningún error: produce
          calladamente un proceso con $\phi = -0.6$, cuya ACF oscila alrededor de cero en lugar de decaer desde 0.79.
          Es el mismo tipo de fallo silencioso que reaparece unas líneas más abajo con el orden de los coeficientes en
          <code>polyroot()</code> y <code>np.roots()</code>.</p>''',
      r'''          Escribir <code>ar=[1, 0.6]</code> en vez de <code>ar=[1, -0.6]</code> no produce ningún error: produce
          calladamente un proceso con $\phi = -0.6$, cuya ACF alterna de signo ($-0.600,\ 0.360,\ -0.216,\ldots$) en
          lugar de decaer sin cambiarlo desde $0.600$. Es el mismo tipo de fallo silencioso que el del orden de los
          coeficientes en <code>polyroot()</code> y <code>np.roots()</code>, que está unas líneas más arriba.</p>''')

    c("M1 · «diferenciar es dividir» pasa a «multiplicar por el factor»", MOD,
      r'''          y el KPSS que rechazaba. De ahí el nombre <em>raíz unitaria</em>. Diferenciar es justamente dividir por el
          factor $(1-B)$ que produce esa raíz.</p>''',
      r'''          y el KPSS que rechazaba. De ahí el nombre <em>raíz unitaria</em>. Diferenciar es multiplicar la serie por
          ese mismo factor $(1-B)$: lo que queda, $\nabla y_t$, ya no tiene esa raíz.</p>''')

    # La sección de convenios se lleva, con su título, hasta el final del módulo.
    mover("M1 · la sección de convenios, al final del módulo", MOD,
          "      <h3>Convenios de signo y diferencias entre R y Python</h3>\n",
          "      <h3>Las raíces son la respuesta</h3>\n",
          "    </div>\n  </template>\n\n  <!-- ============================================================ -->\n"
          "  <!-- MÓDULO 2 · Procesos AR(p)")
