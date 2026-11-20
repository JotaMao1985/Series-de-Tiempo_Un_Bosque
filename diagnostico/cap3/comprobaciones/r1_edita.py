#!/usr/bin/env python3
"""R1 del capítulo 3 · reaplica sobre HEAD las ediciones de `ensamblado/cap3/`.

Parte del contenido de `ensamblado/cap3/cap3_modulos.html` y `cap3_js.js` en el commit
base (por defecto HEAD), aplica cada sustitución —que debe aparecer exactamente una
vez— y escribe el resultado. Es reejecutable: siempre parte del commit, no del archivo
de trabajo.

Uso (desde la raíz del repo):
    python3 diagnostico/cap3/comprobaciones/r1_edita.py            # escribe
    python3 diagnostico/cap3/comprobaciones/r1_edita.py --comprobar  # solo compara
    python3 diagnostico/cap3/comprobaciones/r1_edita.py --base ce69262

Después: `python3 ensamblado/ensambla_cap3.py --escribir` y los ensambladores 4, 5 y 6.
Las ediciones de `precalculo/genera_cap3.R` y `genera_soluciones.R` están en
`r1_edita_generador.py`.
"""
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
MOD = "ensamblado/cap3/cap3_modulos.html"
JS = "ensamblado/cap3/cap3_js.js"

C = []  # (clave, archivo, antes, después)


def c(clave, archivo, antes, despues):
    C.append((clave, archivo, antes, despues))


# =====================================================================================
# MÓDULO 1
# =====================================================================================
c("M1 · polynomial_ar impreso", MOD,
  r'''print(fit.polynomial_ar)     # [ 1.  -0.5999]  ->  phi(B)   = 1 - 0.5999 B
print(fit.polynomial_ma)     # [ 1.   0.6925]  ->  theta(B) = 1 + 0.6925 B''',
  r'''print(np.round(fit.polynomial_ar, 4))   # [ 1.     -0.5999]  ->  phi(B)   = 1 - 0.5999 B
print(np.round(fit.polynomial_ma, 4))   # [1.     0.6925]    ->  theta(B) = 1 + 0.6925 B''')

c("M1 · causalidad, en la definición", MOD,
  r'''          $B_i$ (incluyendo el módulo si la raíz es compleja).</p>
      </div>''',
  r'''          $B_i$ (incluyendo el módulo si la raíz es compleja).</p>
        <p style="margin-bottom:0; margin-top:0.6rem;">En este capítulo «estacionario» quiere decir además
          <strong>causal</strong>: que $y_t$ depende solo de los choques hasta $t$, que es lo que hace falta para
          pronosticar. La condición de las raíces es la de esa solución; el desarrollo de más abajo enseña qué
          queda cuando no se cumple.</p>
      </div>''')

c("M1 · causalidad, en el desarrollo del AR(1)", MOD,
  r'''              <p>Si $|\phi| \ge 1$, el resto no desaparece: el proceso no olvida y no existe una solución estacionaria.</p>''',
  r'''              <p>Si $|\phi| \ge 1$, el resto no desaparece: el proceso no olvida y no existe una solución
                estacionaria que dependa solo de los choques pasados. Con $|\phi| > 1$ existe otra, estacionaria
                pero escrita con los choques <em>futuros</em>, $y_t = -\sum_{j \ge 1}\phi^{-j}\varepsilon_{t+j}$:
                no sirve para pronosticar y por eso queda fuera. Con $|\phi| = 1$ no hay ninguna.</p>''')

c("M1 · |B| = 1 no es solo phi = 1", MOD,
  r'''        <p><strong>Enlace con el Capítulo 2.</strong> Cuando una raíz cae <em>exactamente</em> sobre el círculo
          ($|B| = 1$, es decir $\phi = 1$), el proceso es la <strong>caminata aleatoria</strong>: la ACF que no decaía
          y el KPSS que rechazaba. De ahí el nombre <em>raíz unitaria</em>. Diferenciar es justamente dividir por el
          factor $(1-B)$ que produce esa raíz.</p>''',
  r'''        <p><strong>Enlace con el Capítulo 2.</strong> Cuando una raíz cae <em>exactamente</em> sobre el círculo
          ($|B| = 1$) el proceso no es estacionario. En el AR(1) eso ocurre con $\phi = 1$ y con $\phi = -1$; el
          primer caso, la raíz $B = 1$, es la <strong>caminata aleatoria</strong>: la ACF que no decaía
          y el KPSS que rechazaba. De ahí el nombre <em>raíz unitaria</em>. Diferenciar es justamente dividir por el
          factor $(1-B)$ que produce esa raíz.</p>''')

# =====================================================================================
# MÓDULO 2
# =====================================================================================
c("M2 · «si y solo si» del triángulo", MOD,
  r'''        <p>Un AR(2) es estacionario si y solo si el par $(\phi_1,\phi_2)$ cumple las tres condiciones:</p>''',
  r'''        <p>Un AR(2) es estacionario —y causal, en el sentido del Módulo 1— si y solo si el par
          $(\phi_1,\phi_2)$ cumple las tres condiciones:</p>''')

c("M2 · «varianza finita»", MOD,
  r'''          es entonces una convención algebraica sobre unas raíces: es exactamente el conjunto de parámetros con los
          que el proceso tiene varianza finita.</p>''',
  r'''          es entonces una convención algebraica sobre unas raíces: es exactamente el conjunto de parámetros con los
          que existe un proceso de varianza finita que depende solo de los choques pasados.</p>''')

# =====================================================================================
# MÓDULO 5 · la recursión del AR en k = 1
# =====================================================================================
c("M5 · recursión en rho_1, prosa", MOD,
  r'''        acierta desde $\rho_2$ —$0.7307$, $0.6238$, $0.5311$—, pero aplicada a $\rho_1$ daría $0.8$ cuando el valor
        verdadero es $0.8614$. Los primeros $q$ rezagos son justamente los que la parte MA todavía toca, y para esos
        hay que volver a la suma de $\psi$ de la sección anterior.</p>''',
  r'''        acierta desde $\rho_2$ —$0.7307$, $0.6238$, $0.5311$—, pero en $k = 1$ no se cumple. Allí diría
        $\rho_1 = \phi_1\rho_0 + \phi_2\rho_{-1} = 0.5 + 0.3\,\rho_1$, porque $\rho_{-1} = \rho_1$; con el valor
        verdadero, $\rho_1 = 0.8614$, el lado derecho da $0.7584$. Los primeros $q$ rezagos son justamente los que
        la parte MA todavía toca, y para esos hay que volver a la suma de $\psi$ de la sección anterior.</p>''')

c("M5 · recursión en rho_1, R", MOD,
  r'''# ...pero NO para k = q: aqui q = 1 y la recursion se equivoca
round(unname(0.5 * r[1] + 0.3 * r[1]), 4)        # lo que daria la recursion
#&gt; [1] 0.8
round(unname(r[2]), 4)                            # rho_1 verdadero
#&gt; [1] 0.8614''',
  r'''# ...pero NO para k = q: aqui q = 1 y la recursion no se cumple.
# En k = 1 dice rho_1 = phi1 rho_0 + phi2 rho_{-1}, y rho_{-1} = rho_1:
round(unname(0.5 * r[1] + 0.3 * r[2]), 4)        # lado derecho, con el rho_1 verdadero
#&gt; [1] 0.7584
round(unname(r[2]), 4)                            # rho_1 verdadero
#&gt; [1] 0.8614''')

c("M5 · recursión en rho_1, Python", MOD,
  r'''# ...pero NO para k = q: aqui q = 1 y la recursion se equivoca
print(round(0.5 * r[0] + 0.3 * r[0], 4), "frente a", round(r[1], 4))
# 0.8 frente a 0.8614''',
  r'''# ...pero NO para k = q: aqui q = 1 y la recursion no se cumple.
# En k = 1 dice rho_1 = phi1 rho_0 + phi2 rho_{-1}, y rho_{-1} = rho_1:
print(round(0.5 * r[0] + 0.3 * r[1], 4), "frente a", round(r[1], 4))
# 0.7584 frente a 0.8614''')

# =====================================================================================
# MÓDULO 6
# =====================================================================================
c("M6 · arima.sim sí simula una caminata", MOD,
  r'''# Para simular una caminata aleatoria hay que usar cumsum(rnorm(n)),
# como se hizo en el Capitulo 2.</code></pre>''',
  r'''# La raiz unitaria no se declara en ar. Una caminata aleatoria se simula con
# cumsum(rnorm(n)), como en el Capitulo 2, o declarando la diferencia en
# order: arima.sim hace esa misma suma y devuelve n + 1 valores (el primero, 0).
length(arima.sim(n = 100, model = list(order = c(0, 1, 0))))
#&gt; [1] 101</code></pre>''')

c("M6 · sin burnin: varianza reducida, no tendencia", MOD,
  r'''          <code>burnin=</code>. Con procesos muy persistentes ($\phi$ cerca de 1), olvidarlo mete una tendencia
          espuria al principio de la serie que después se lee como si fuera estructura.</p>''',
  r'''          <code>burnin=</code>. Sin él la serie arranca en cero y su primer tramo tiene menos varianza que el
          resto: con $\phi = 0.95$, la varianza en $t = 5$ es $4.1$ cuando la del régimen estacionario es $10.3$.
          Con procesos muy persistentes ese arranque comprimido dura decenas de observaciones.</p>''')

# =====================================================================================
# MÓDULO 7
# =====================================================================================
c("M7 · el 4 % del CSS y ML en la frontera", MOD,
  r'''                No es lo habitual —en mil simulaciones iguales CSS pasa de $1$ en un 4&nbsp;% de los casos— pero ML
                no lo hace en ninguna: la verosimilitud exacta cae a $-\infty$ antes de llegar a la frontera.</p>''',
  r'''                No es lo habitual —en mil simulaciones iguales CSS pasa de $1$ entre un 3 y un 5&nbsp;% de las
                veces, según la semilla— y ML no lo hace en ninguna, por dos razones: el sumando
                $\tfrac{1}{2}\log(1-\phi^2)$ cae a $-\infty$ en la frontera, y <code>arima()</code>, al maximizar la
                verosimilitud, reparametriza los $\phi$ para no salir de la región estacionaria
                (<code>transform.pars = TRUE</code>, su valor por defecto). Quedarse dentro no es quedarse lejos:
                en un 13&nbsp;% de esas simulaciones la estimación ML es $\ge 0.999$.</p>''')

c("M7 · AutoReg reproduce el CSS, import", MOD,
  r'''from statsmodels.regression.linear_model import yule_walker

datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR &gt;= 1770) &amp; (datos.YEAR &lt;= 1869), "SUNACTIVITY"].values
print(len(manchas))   # 100''',
  r'''from statsmodels.tsa.ar_model import AutoReg
from statsmodels.regression.linear_model import yule_walker

datos = sm.datasets.sunspots.load_pandas().data
manchas = datos.loc[(datos.YEAR &gt;= 1770) &amp; (datos.YEAR &lt;= 1869), "SUNACTIVITY"].values
print(len(manchas))   # 100''')

c("M7 · AutoReg reproduce el CSS, bloque", MOD,
  r'''# 2. CSS: la API nueva de ARIMA NO lo ofrece. Sus method= son statespace,
#    innovations_mle, hannan_rissanen, burg, innovations y yule_walker;
#    fit(method="css") lanza ValueError: "css" is not a valid estimator.
#    El antiguo tsa.arima_model.ARMA, que si tenia method="css", fue
#    retirado en statsmodels 0.13. El CSS de R (1.4032, -0.7099) no tiene
#    equivalente directo aqui.
''',
  r'''# 2. CSS: la API nueva de ARIMA NO lo ofrece. Sus method= son statespace,
#    innovations_mle, hannan_rissanen, burg, innovations y yule_walker;
#    fit(method="css") lanza ValueError: "css" is not a valid estimator.
#    El antiguo tsa.arima_model.ARMA, que si tenia method="css", fue
#    retirado en statsmodels 0.13. Pero en un AR puro el CSS es la regresion
#    de y_t sobre sus rezagos, y esa la hace AutoReg:
css = AutoReg(manchas, lags=2, trend="c").fit()
print(np.round(css.params[1:], 4))   # [ 1.4032 -0.7099]  el CSS de R
''')

# =====================================================================================
# MÓDULO 8 · residuales de R y de statsmodels
# =====================================================================================
c("M8 · por qué difieren los dos primeros residuales", MOD,
  r'''          $-15.397$…); los que difieren son los <strong>dos primeros</strong>, porque cada programa inicializa de otra
          forma el filtro para las $p$ primeras observaciones (R da $21.06$ y statsmodels $52.54$ para el primero). Y
          $Q$ pondera mucho $\hat r_1$.</p>''',
  r'''          $-15.397$…); los que difieren son los <strong>dos primeros</strong> (R da $21.06$ y statsmodels $52.54$
          para el primero). El modelo y el filtro son los mismos; cambia lo que cada programa <em>devuelve</em>. El
          error de predicción de la primera observación, que no tiene pasado, tiene varianza $\gamma_0$ y no
          $\sigma^2$: statsmodels lo entrega tal cual y R lo entrega dividido entre $\sqrt{\gamma_0/\sigma^2}$,
          para que todos los residuales queden en la misma escala ($52.54/\sqrt{6.226} = 21.06$). Con el segundo
          pasa lo mismo. Dos valores inflados al principio bastan para mover las autocorrelaciones residuales y,
          con ellas, $Q$.</p>''')

c("M8 · qué residuales sirven para el diagnóstico", MOD,
  r'''          <strong>el rechazo del AR(2) es real y se refuerza</strong> ($0.0232 < 0.0461$); lo que hay es una
          inicialización que infla el primer residual y relaja la prueba. Moraleja general: cuando dos programas''',
  r'''          <strong>el rechazo del AR(2) es real y se refuerza</strong> ($0.0232 < 0.0461$); lo que relaja la prueba
          en statsmodels son esos primeros residuales sin estandarizar. Moraleja general: cuando dos programas''')

# =====================================================================================
# MÓDULO 9 · manchas solares
# =====================================================================================
c("M9 · elasticidades: qué contiene cada intervalo", MOD,
  r'''          <strong>hay que transformar</strong>, eso es firme y no depende de cómo se hagan los bloques. Pero ninguno
          separa limpiamente $b=0.5$ (raíz cuadrada) de $b=1$ (logaritmo): los intervalos contienen los dos valores o
          casi. Los datos piden una transformación y no dicen exactamente cuál.</p>''',
  r'''          <strong>hay que transformar</strong>, eso es firme y no depende de cómo se hagan los bloques. Pero entre
          $b=0.5$ (raíz cuadrada) y $b=1$ (logaritmo) las tres particiones se contradicen: con bloques de 10 años
          el intervalo contiene el $1$ y deja fuera el $0.5$; con bloques de 5, al revés; con bloques de 11, deja
          fuera los dos por muy poco. Los datos piden una transformación y no dicen exactamente cuál.</p>''')

c("M9 · la PACF en la raíz no queda más limpia", MOD,
  r'''          picos altos y estrechos y los mínimos son planos: la serie es asimétrica. En la raíz, los ciclos se parecen
          mucho más entre sí y la PACF se corta más limpiamente en el rezago 2.</p>''',
  r'''          picos altos y estrechos y los mínimos son planos: la serie es asimétrica. En la raíz, los ciclos se parecen
          mucho más entre sí. La PACF conserva su forma —dos barras grandes y el resto pequeñas— pero no queda más
          limpia: en la escala original solo salen de la banda los rezagos 1 y 2, y en la raíz la rozan además el
          6, el 9 y el 16 ($0.200$, $0.198$ y $-0.199$ frente a $\pm 0.196$).</p>''')

c("M9 · p = 0.2216", MOD,
  r'''Sobre la desplazada saldría $11.28$ y $p = 0.2217$: la misma lectura.''',
  r'''Sobre la desplazada saldría $11.28$ y $p = 0.2216$: la misma lectura.''')

c("M9 · D5: las dos nociones de periodo", MOD,
  r'''        módulo dice <em>cuánto se amortigua</em> la oscilación; el ángulo, <em>cada cuánto</em> oscila.</p>
''',
  r'''        módulo dice <em>cuánto se amortigua</em> la oscilación; el ángulo, <em>cada cuánto</em> oscila.</p>

      <div class="note">
        <p style="margin-bottom:0;"><strong>Otra fórmula para «el periodo».</strong> FPP3 (sección 9.5) da para el
          AR(2) con raíces complejas el <em>periodo medio de los ciclos</em>,
          $2\pi/\arccos\!\big(-\phi_1(1-\phi_2)/(4\phi_2)\big)$, que con estos coeficientes vale $11.84$ años y no
          $11.22$. Ninguna de las dos cifras está mal: miden cosas distintas. El $11.22$ es el periodo con que
          oscilan la ACF y los pesos $\psi$ del modelo, el ángulo de la raíz; el $11.84$ coincide con el periodo
          en que es máxima la densidad espectral del proceso —el reparto de su varianza por frecuencias, que este
          curso no desarrolla—. Las dos se juntan cuando el módulo de la raíz se acerca a $1$. Este capítulo usa
          siempre la primera.</p>
      </div>
''')

c("M9 · envolvente, unidades y cruces por cero", MOD,
  r'''      <p>Las dos piezas de la raíz reaparecen, ahora haciendo cosas distintas: el módulo manda en la amplitud —el
        envolvente $0.8278^{\,j}$ se reduce a la mitad cada $3.67$ años— y el ángulo, en la oscilación. Traducido a
        manchas: un año con más manchas de las que el modelo esperaba deja $1.40$ de exceso al año siguiente,
        todavía $0.84$ tres años después, y hacia el quinto o el sexto <strong>ha cambiado de signo</strong>. Los
        cruces por cero caen en $j = 4.61$ y $j = 10.22$: medio ciclo y un ciclo de los $11.22$ años. La respuesta''',
  r'''      <p>Las dos piezas de la raíz reaparecen, ahora haciendo cosas distintas: el módulo manda en la amplitud —el
        envolvente $\pm R^{\,j}/\sin\omega = \pm 1.882 \times 0.8278^{\,j}$ se reduce a la mitad cada $3.67$ años—
        y el ángulo, en la oscilación. Los $\psi$ están en la escala en que se ajustó el modelo: un choque de una
        unidad en $\sqrt{\text{manchas}}$ deja $1.40$ unidades de exceso al año siguiente, todavía $0.84$ tres años
        después, y al quinto <strong>ha cambiado de signo</strong>. Los $\psi$ se anulan cuando $(j+1)\,\omega$ es
        múltiplo de $\pi$, es decir en $j + 1 = 5.61$ y $j + 1 = 11.22$: medio ciclo y un ciclo de los $11.22$
        años. La respuesta''')

c("M9 · forecast(h = 6) frente a doce filas", MOD,
  r'''        <p>Las dos últimas columnas no son un ejercicio paralelo: son, hasta el cuarto decimal, lo que imprime
          <code>forecast(ar2s, h = 6)</code>. Y enseñan algo que el Capítulo 4 va a contrastar. La suma''',
  r'''        <p>Las dos últimas columnas no son un ejercicio paralelo: son lo que imprime <code>forecast()</code>. El
          código de abajo lo comprueba en las seis primeras filas, con cuatro decimales. Y enseñan algo que el
          Capítulo 4 va a contrastar. La suma''')

c("M9 · envolvente, intro del simulador", MOD,
  r'''        <p class="simulador-intro">Los pesos $\psi_j$ de la tabla, con el envolvente $\pm 0.8278^{\,j}$ que los
          amortigua: el choque de un año no se agota, se propaga oscilando. Mueve $h$ para colorear los pesos que''',
  r'''        <p class="simulador-intro">Los pesos $\psi_j$ de la tabla, con el envolvente
          $\pm 0.8278^{\,j}/\sin\omega$ que los amortigua: el choque de un año no se agota, se propaga oscilando.
          Mueve $h$ para colorear los pesos que''')

c("M9 · «la transformación es monótona»", MOD,
  r'''        <p><strong>Estas bandas están en la escala de la raíz.</strong> Volver a las manchas es elevar al cuadrado
          los extremos: la transformación es monótona, así que respeta los cuantiles y el $95\,\%$ sigue siendo el
          $95\,\%$. El <em>centro</em>, en cambio, no se transforma igual: el cuadrado del pronóstico es la''',
  r'''        <p><strong>Estas bandas están en la escala de la raíz.</strong> Volver a las manchas es elevar al cuadrado
          los extremos: sobre valores no negativos el cuadrado es creciente, así que respeta los cuantiles y el
          $95\,\%$ sigue siendo el $95\,\%$. Con una salvedad: un límite inferior negativo —pronosticando desde
          1869 ocurre en $h = 7$ y $h = 8$, con $-0.209$ y $-0.114$— se trunca en cero <em>antes</em> de elevarlo,
          porque su cuadrado ($0.044$ y $0.013$) sería una cota positiva falsa. El <em>centro</em>, en cambio, no
          se transforma igual: el cuadrado del pronóstico es la''')

c("M9 · el Módulo 6 usó 200 datos", MOD,
  r'''            <td>El único que no entra en ninguna cuenta, y hace falta igual: enseñó cuánto se aleja de la teoría una
              muestra de $100$ datos, que es la prudencia con la que hay que leer esa PACF.</td></tr>''',
  r'''            <td>El único que no entra en ninguna cuenta, y hace falta igual: enseñó cuánto se aleja de la teoría una
              muestra finita (allí, de $200$ datos), que es la prudencia con la que hay que leer esa PACF.</td></tr>''')

# =====================================================================================
# MÓDULO 9 · TRM
# =====================================================================================
c("M9 · TRM: qué devuelve auto.arima y el theta del MA(1)", MOD,
  r'''        rechaza en ninguno, aunque el $0.06$ es lo bastante bajo como para no cantar victoria. Y si se ajusta el MA(1)
        que sugiere <code>auto.arima</code>:</p>

      <div class="formula">
        $$\hat\theta_1 = 0.1262 \;\; (\text{e.e. } 0.0912,\; t = 1.38)$$
        <p style="margin-bottom:0;">Comparado en igualdad de condiciones con el ruido blanco puro, el MA(1) da un AICc
          de $722.653$ frente a $722.663$: una diferencia de <strong>una centésima</strong>. Son indistinguibles.</p>
      </div>''',
  r'''        rechaza en ninguno, aunque el $0.06$ es lo bastante bajo como para no cantar victoria. La búsqueda
        automática de <code>auto.arima()</code> tampoco encuentra nada firme. Con sus argumentos por defecto devuelve
        un ARIMA(0,0,0) con media cero, es decir, ruido blanco. Solo con la búsqueda exhaustiva
        (<code>stepwise = FALSE, approximation = FALSE</code>), que prueba modelos a los que la búsqueda por pasos
        no llega, devuelve un MA(1), también sin media:</p>

      <div class="formula">
        $$\hat\theta_1 = 0.1326 \;\; (\text{e.e. } 0.0905,\; t = 1.47)$$
        <p style="margin-bottom:0;">Ese MA(1) y el ruido blanco puro, los dos sin media, dan un AICc
          de $722.653$ frente a $722.663$: una diferencia de <strong>una centésima</strong>. Son indistinguibles.</p>
      </div>''')

c("M9 · TRM: la conclusión y el promedio de datos diarios", MOD,
  r'''          pronóstico de la variación del mes que viene es la media histórica. No es un fracaso del análisis: es su
          resultado, y coincide con lo que predice la teoría de mercados eficientes para una tasa de cambio.</p>
      </div>
''',
  r'''          pronóstico de la variación del mes que viene es la media histórica. No es un fracaso del análisis: es su
          resultado.</p>
      </div>

      <div class="warning">
        <p style="margin-bottom:0;"><strong>De qué serie se dice.</strong> Esta TRM mensual es el
          <em>promedio</em> de los valores diarios de cada mes, y promediar deja huella. Si la tasa diaria fuera una
          caminata aleatoria pura, las variaciones del promedio mensual no serían ruido blanco: tendrían
          $\rho_1 \approx 0.25$ ($0.249$ con 21 días por mes). El $r_1$ observado es $0.105$, a $1.7$ errores
          estándar por debajo de esa cifra. El «ruido blanco» de arriba describe, entonces, las variaciones del
          promedio mensual, que es la serie que aquí se modela; no dice que la tasa diaria sea una caminata
          aleatoria, ni lo contrario. Para eso habría que trabajar con la tasa de un día fijo de cada mes o con
          los datos diarios.</p>
      </div>
''')

c("M9 · TRM: el AICc sí compara con y sin media", MOD,
  r'''        <p><strong>Ojo con la media.</strong> <code>auto.arima()</code> devuelve el MA(1) <strong>sin</strong> término
          constante. No es un capricho: la media mensual estimada es $0.2681\ \%$ con un error estándar de $0.3195$,
          o sea $t = 0.84$. Con 137 meses no hay evidencia de que la TRM tenga una deriva distinta de cero. Si al
          comparar AICc de dos modelos uno incluye media y el otro no, no los estás comparando en igualdad de
          condiciones.</p>''',
  r'''        <p><strong>Ojo con la media.</strong> Los dos modelos que devuelve <code>auto.arima()</code> van
          <strong>sin</strong> término constante. No es un capricho: en el MA(1) con media, la media mensual estimada
          es $0.2681\ \%$ con un error estándar de $0.3195$, o sea $t = 0.84$. Con 137 meses no hay evidencia de que
          la TRM tenga una deriva distinta de cero, y el AICc lo recoge: el ruido blanco con media da $723.804$ y
          sin ella $722.663$. Esa comparación es legítima —con media o sin ella, los dos modelos se ajustan a los
          mismos datos y el criterio solo cobra el parámetro de más—, y es la que hace <code>auto.arima()</code>
          para decidir si la incluye. Lo que el AICc no puede comparar son modelos ajustados a datos distintos:
          otro orden de diferenciación u otra transformación.</p>''')

c("M9 · TRM: título de la nota del cuadrado", MOD,
  r'''        <p><strong>Donde sí hay estructura: en el cuadrado.</strong> Ljung–Box sobre $r_t$ da $p = 0.0601$, pero sobre
          $r_t^2$ da $p = 0.9166$: en esta serie mensual tampoco hay agrupamiento de volatilidad detectable. En datos''',
  r'''        <p><strong>¿Y en el cuadrado? Aquí tampoco.</strong> Ljung–Box sobre $r_t$ da $p = 0.0601$, y sobre
          $r_t^2$ da $p = 0.9166$: en esta serie mensual tampoco hay agrupamiento de volatilidad detectable. En datos''')

# ---- bloque de R ---------------------------------------------------------------------
c("M9 · R: Ljung-Box con la salida real", MOD,
  r'''#&gt; [1] 0.1643575          <- ahora SI pasa''',
  r'''#&gt; [1] 0.1643997          <- ahora SI pasa''')

c("M9 · R: la TRM, copia fija (D2)", MOD,
  r'''# trm: serie mensual del Capitulo 2 (promedio mensual, SFC via datos.gov.co).
# Se reconstruye aqui para que el bloque sea autonomo.
url &lt;- paste0("https://www.datos.gov.co/resource/32sa-8pi3.json",
              "?$select=vigenciadesde,valor&amp;$limit=50000")
crudo &lt;- jsonlite::fromJSON(url)
diario &lt;- data.frame(fecha = as.Date(substr(crudo$vigenciadesde, 1, 10)),
                     valor = as.numeric(crudo$valor))
# Dos pasos: order() devuelve INDICES, no un vector logico, y combinarlo con
# & mediante  order(...) & fecha >= ...  no ordena nada (todo indice != 0 se
# coacciona a TRUE). Filtrar y ordenar son operaciones distintas.
diario &lt;- diario[diario$fecha &gt;= as.Date("2015-01-01"), ]
diario &lt;- diario[order(diario$fecha), ]
mes &lt;- format(diario$fecha, "%Y-%m")
prom &lt;- tapply(diario$valor, mes, mean)
prom &lt;- prom[names(prom) &lt;= "2026-06"]
trm &lt;- ts(as.numeric(prom), start = c(2015, 1), frequency = 12)
''',
  r'''# trm: la serie mensual del Capitulo 2, el promedio de los valores diarios
# de cada mes entre enero de 2015 y junio de 2026. Copia fija de los 138
# meses con que se calcularon estas cifras: se lee de la carpeta de trabajo
# si el archivo ya esta ahi; si no, de la pagina del curso.
archivo &lt;- "trm_mensual_2015-01_2026-06.csv"
if (!file.exists(archivo))
  archivo &lt;- paste0("https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/", archivo)
trm &lt;- ts(read.csv(archivo)$trm, start = c(2015, 1), frequency = 12)
''')

c("M9 · R: auto.arima y los cuatro AICc", MOD,
  r'''ma1 &lt;- arima(ret, order = c(0, 0, 1), method = "ML")
round(c(theta = coef(ma1)[["ma1"]], ee = sqrt(ma1$var.coef[1, 1])), 4)
#&gt;  theta     ee
#&gt; 0.1262 0.0912

# Comparacion JUSTA: los dos sin media
c(ma1_sin_media   = aicc(arima(ret, order = c(0,0,1), include.mean = FALSE,
                               method = "ML"), 137),
  ruido_sin_media = aicc(arima(ret, order = c(0,0,0), include.mean = FALSE,
                               method = "ML"), 137))
#&gt;   ma1_sin_media ruido_sin_media
#&gt;        722.6530        722.6632
''',
  r'''# auto.arima(): por defecto devuelve ruido blanco; con la busqueda
# exhaustiva, un MA(1). Ninguno de los dos lleva media.
arimaorder(auto.arima(ret))
#&gt; p d q
#&gt; 0 0 0
exh &lt;- auto.arima(ret, stepwise = FALSE, approximation = FALSE)
arimaorder(exh)
#&gt; p d q
#&gt; 0 0 1
round(c(theta = coef(exh)[["ma1"]], ee = sqrt(exh$var.coef[1, 1])), 4)
#&gt;  theta     ee
#&gt; 0.1326 0.0905

# La media no es significativa: el MA(1) CON media (el defecto de arima())
ma1 &lt;- arima(ret, order = c(0, 0, 1), method = "ML")
round(c(theta = coef(ma1)[["ma1"]], media = coef(ma1)[["intercept"]],
        ee_media = sqrt(ma1$var.coef[2, 2])), 4)
#&gt;    theta    media ee_media
#&gt;   0.1262   0.2681   0.3195

# El AICc SI compara con y sin media: son los mismos datos y solo cambia
# un parametro. Los cuatro modelos, de una vez:
con &lt;- function(q) arima(ret, order = c(0, 0, q), method = "ML")
sin &lt;- function(q) arima(ret, order = c(0, 0, q), include.mean = FALSE, method = "ML")
round(c(ruido_con_media = aicc(con(0), 137), ruido_sin_media = aicc(sin(0), 137),
        ma1_con_media   = aicc(con(1), 137), ma1_sin_media   = aicc(sin(1), 137)), 3)
#&gt; ruido_con_media ruido_sin_media   ma1_con_media   ma1_sin_media
#&gt;         723.804         722.663         724.046         722.653
''')

# ---- bloque de Python ----------------------------------------------------------------
c("M9 · Python: import os", MOD,
  r'''          <pre><code class="language-python">import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima_process import arma2ma
from scipy import stats
''',
  r'''          <pre><code class="language-python">import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima_process import arma2ma
from scipy import stats
''')

c("M9 · Python: Ljung-Box, salida real y mecanismo", MOD,
  r'''print(round(float(lb["lb_pvalue"].iloc[0]), 4))   # 0.1780
# R daba 0.1644, por la inicializacion de residuales del Modulo 8.
# Descartando los 2 primeros, los dos programas dan 0.1682.''',
  r'''print(round(float(lb["lb_pvalue"].iloc[0]), 4))   # 0.178
# R daba 0.1644: devuelve estandarizados los dos primeros residuales, y
# statsmodels no (Modulo 8). Descartando esos dos, los dos programas dan 0.1682.''')

c("M9 · Python: periodo, salida real", MOD,
  r'''print(round(2 * np.pi / np.angle(raices[0]), 4))  # 11.2178
''',
  r'''print(round(2 * np.pi / np.angle(raices[0]), 4))  # 11.218 (en R, 11.2178)
''')

c("M9 · Python: la TRM, copia fija (D2)", MOD,
  r'''url = ("https://www.datos.gov.co/resource/32sa-8pi3.json"
       "?$select=vigenciadesde,valor&amp;$limit=50000")
crudo = pd.read_json(url)
crudo["fecha"] = pd.to_datetime(crudo["vigenciadesde"]).dt.tz_localize(None)
crudo = crudo[crudo["fecha"] &gt;= "2015-01-01"].sort_values("fecha")
trm = (crudo.set_index("fecha")["valor"].resample("MS").mean()
            .loc[:"2026-06-01"])

ret = 100 * np.diff(np.log(trm.values))''',
  r'''# La misma copia fija de 138 meses que lee R (enero de 2015 a junio de
# 2026): de la carpeta de trabajo si el archivo ya esta ahi; si no, de la
# pagina del curso.
archivo = "trm_mensual_2015-01_2026-06.csv"
if not os.path.exists(archivo):
    archivo = "https://jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/datos/" + archivo
trm = pd.read_csv(archivo)["trm"]

ret = 100 * np.diff(np.log(trm.values))''')

c("M9 · Python: MA(1) sin media, con su salida", MOD,
  r'''print(round(ma1.aicc, 4), round(rb.aicc, 4))   # practicamente iguales
''',
  r'''print(np.round(ma1.params[:1], 4))             # [0.1326]  theta, sin media
print(round(ma1.aicc, 3), round(rb.aicc, 3))   # 722.653 722.663  indistinguibles
''')

# =====================================================================================
# MÓDULO 10
# =====================================================================================
c("M10 · RNN: |w| < 1 no evita el desvanecimiento", MOD,
  r'''          unidad <em>es</em> un AR(1): $h_t = w\,h_{t-1} + u\,x_t$. La condición de estabilidad del entrenamiento
          ($|w| < 1$, para que el gradiente no explote ni se desvanezca) es la <strong>misma condición de
            estacionariedad</strong> del Módulo 1. El problema del gradiente que se desvanece en las RNN y el
          desvanecimiento de $\phi^k$ que vimos al desarrollar el AR(1) hacia atrás son el mismo fenómeno
          matemático.</p>''',
  r'''          unidad <em>es</em> un AR(1): $h_t = w\,h_{t-1} + u\,x_t$. La condición para que ese estado no explote
          ($|w| < 1$) es la <strong>misma condición de
            estacionariedad</strong> del Módulo 1, y tiene el mismo precio. La derivada de $h_t$ respecto al estado
          de $k$ pasos atrás es $w^k$: con $|w| < 1$ <strong>se desvanece</strong>, y con $|w| > 1$ explota. El
          problema del gradiente que se desvanece en las RNN y el
          desvanecimiento de $\phi^k$ que vimos al desarrollar el AR(1) hacia atrás son el mismo fenómeno
          matemático.</p>''')

c("M10 · parámetros del AR(2)", MOD,
  r'''            sobre cien observaciones memoriza la muestra; el AR(2) tiene tres.</li>''',
  r'''            sobre cien observaciones memoriza la muestra; el AR(2) tiene cuatro, contando la media y
            $\sigma^2$.</li>''')

c("M10 · lista de verificaciones: el AICc y la media", MOD,
  r'''(3) el AICc no compara modelos con distinto $d$ ni con y sin media; (4) un ARMA que gana por AICc''',
  r'''(3) el AICc no compara modelos con distinto $d$ ni en otra escala —con media o sin ella, sí—; (4) un ARMA que gana por AICc''')

c("M10 · t sin redondeo intermedio", MOD,
  r'''En el AR(2) final de las manchas, $t = 19.29$ y $t = -9.47$;''',
  r'''En el AR(2) final de las manchas, $t = 19.31$ y $t = -9.46$;''')

c("E1 · qué conserva el 57 %", MOD,
  r'''($\hat\phi = 0.574$: cada medición conserva el 57 % de la anterior) y''',
  r'''($\hat\phi = 0.574$: cada medición conserva el 57 % de la desviación de la anterior respecto a la media) y''')

# =====================================================================================
# EJERCICIO 3
# =====================================================================================
c("E3 · pista", MOD,
  r'''coeficientes apenas se muevan, que el periodo sí lo haga y que el diagnóstico se derrumbe. Piensa por qué
            el Ljung–Box empeora tanto al alargar la muestra: ¿el modelo es peor, o la prueba tiene más con qué
            detectarlo?</p>''',
  r'''coeficientes apenas se muevan, que el periodo sí lo haga y que el diagnóstico se derrumbe. Antes de
            atribuir un cambio del Ljung–Box al tamaño de la muestra, compara ventanas del mismo tamaño: 1889–1988
            tiene cien años, igual que 1770–1869.</p>''')

c("E3 · respuesta corta", MOD,
  r'''          <p><strong>Respuesta: los coeficientes son notablemente estables, el periodo se acorta un año y el
              diagnóstico falla en todas las ventanas salvo la de Yule.</strong></p>
          <pre><code class="language-r">for (v in list(c(1770,1869), c(1700,1988), c(1870,1988), c(1900,1988))) {''',
  r'''          <p><strong>Respuesta: los coeficientes son notablemente estables, el periodo se acorta un año y el
              diagnóstico falla en todas las ventanas que llegan al siglo XX, tengan más datos que la de Yule o
              menos.</strong></p>
          <pre><code class="language-r">for (v in list(c(1770,1869), c(1700,1988), c(1870,1988), c(1900,1988), c(1889,1988))) {''')

c("E3 · la ventana de control en la salida", MOD,
  r'''#&gt; 1900-1988 (n= 89): phi=(1.4146, -0.7556)  |raiz|=1.1504  periodo=10.129  LB12 p=0.0010</code></pre>''',
  r'''#&gt; 1900-1988 (n= 89): phi=(1.4146, -0.7556)  |raiz|=1.1504  periodo=10.129  LB12 p=0.0010
#&gt; 1889-1988 (n=100): phi=(1.4101, -0.7431)  |raiz|=1.1600  periodo=10.249  LB12 p=0.0006</code></pre>''')

c("E3 · discusión del diagnóstico y moraleja", MOD,
  r'''            <li><strong>El diagnóstico se derrumba</strong> en cuanto se sale de la ventana de Yule ($p &lt; 0.001$ en
              las tres). Y la causa no es que el modelo empeore —los coeficientes casi no cambian— sino que
              <strong>la prueba gana potencia</strong>: con $n = 289$ en vez de $100$, Ljung–Box detecta
              autocorrelaciones residuales pequeñas que con cien observaciones quedaban dentro del ruido. La asimetría
              no lineal que el Módulo 9 señalaba sigue ahí; simplemente, ahora hay datos suficientes para probarlo.</li>
          </ul>
          <p style="margin-bottom:0;">Moraleja: que un modelo "pase" el diagnóstico depende de cuántos datos tengas
            para desmentirlo. No rechazar $H_0$ nunca es lo mismo que aceptarla.</p>''',
  r'''            <li><strong>El diagnóstico se derrumba</strong> en cuanto la ventana llega al siglo XX: $p = 0.0007$
              en 1870–1988, $p = 0.0010$ en 1900–1988 y por debajo de $0.0001$ en la serie completa. La explicación
              cómoda —con más datos la prueba gana potencia— <strong>aquí no se sostiene</strong>: 1900–1988 tiene
              <em>menos</em> datos que la ventana de Yule ($n = 89$) y rechaza igual, y 1889–1988, con los mismos
              cien años, da $p = 0.0006$. Lo que cambia no es $n$ sino el tramo. De las 190 ventanas de cien años
              que caben entre 1700 y 1988, el AR(2) pasa la prueba en 52, y todas menos una empiezan entre 1734 y
              1785. La de Yule es una de las favorables; en las que alcanzan el siglo XX el mismo modelo, con
              coeficientes casi iguales, deja autocorrelación sin explicar y no pasa en ninguna.</li>
          </ul>
          <p style="margin-bottom:0;">Moraleja: que un modelo «pase» el diagnóstico en una ventana no dice que lo
            pase en otra, y antes de atribuir un cambio de veredicto al tamaño de la muestra hay que comparar con
            $n$ fijo. No rechazar $H_0$ nunca es lo mismo que aceptarla.</p>''')

# =====================================================================================
# JS · envolvente de los psi
# =====================================================================================
c("JS · envolvente ±R^j/sin(omega)", JS,
  r'''      // R = sqrt(-phi2) es el inverso del módulo de la raíz: el envolvente que
      // amortigua la oscilación. Módulo 1.
      const R = Math.sqrt(-TRANSF.sqrt.phi2);
      const etiquetas = Array.from({ length: N + 1 }, (_, j) => String(j));
      const envolvente = etiquetas.map((_, j) => Math.pow(R, j));''',
  r'''      // R = sqrt(-phi2) es el inverso del módulo de la raíz y manda en la
      // amortiguación. El envolvente de psi_j = R^j sin((j+1)w)/sin(w) no es
      // ±R^j sino ±R^j/sin(w): con el w de este ajuste, 1.88 veces mayor.
      const R = Math.sqrt(-TRANSF.sqrt.phi2);
      const omega = Math.acos(TRANSF.sqrt.phi1 / (2 * R));   // ángulo de la raíz
      const factor = 1 / Math.sin(omega);
      const etiquetas = Array.from({ length: N + 1 }, (_, j) => String(j));
      const envolvente = etiquetas.map((_, j) => factor * Math.pow(R, j));''')

c("JS · envolvente, leyenda", JS,
  r'''      [['±(0.83)ʲ — envolvente', envolvente], ['', envolvente.map(v => -v)]].forEach(''',
  r'''      [[`±${factor.toFixed(2)} × ${R.toFixed(2)}ʲ — envolvente`, envolvente],
        ['', envolvente.map(v => -v)]].forEach(''')

c("JS · envolvente, lectura", JS,
  r'''            etiqueta: 'Envolvente √(−φ₂) =',
            valor: `${R.toFixed(4)} — se reduce a la mitad cada ${(Math.log(0.5) / Math.log(R)).toFixed(2)} años`''',
  r'''            etiqueta: 'Envolvente ±Rʲ/sen ω:',
            valor: `R = √(−φ₂) = ${R.toFixed(4)} y 1/sen ω = ${factor.toFixed(3)} — se reduce a la mitad cada ${(Math.log(0.5) / Math.log(R)).toFixed(2)} años`''')


# =====================================================================================
def base(archivo, rev):
    return subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def main():
    rev = "HEAD"
    if "--base" in sys.argv:
        rev = sys.argv[sys.argv.index("--base") + 1]
    comprobar = "--comprobar" in sys.argv
    textos = {a: base(a, rev) for a in (MOD, JS)}
    fallos = 0
    for clave, archivo, antes, despues in C:
        n = textos[archivo].count(antes)
        if n != 1:
            print(f"FALLA · {clave}: el texto original aparece {n} veces en {archivo} (se esperaba 1)")
            fallos += 1
            continue
        textos[archivo] = textos[archivo].replace(antes, despues)
    if fallos:
        sys.exit(f"{fallos} sustituciones no aplicadas; no se escribe nada")
    for archivo, texto in textos.items():
        ruta = RAIZ / archivo
        if comprobar:
            igual = ruta.read_text(encoding="utf-8") == texto
            print(f"{archivo}: {'idéntico a HEAD + ediciones' if igual else 'DIFIERE de HEAD + ediciones'}")
            fallos += 0 if igual else 1
        else:
            ruta.write_text(texto, encoding="utf-8")
    print(f"{len(C)} sustituciones ({sum(1 for x in C if x[1] == MOD)} en los módulos, "
          f"{sum(1 for x in C if x[1] == JS)} en el JS) sobre {rev}")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
