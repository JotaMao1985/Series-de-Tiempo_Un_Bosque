# R3 · Modulos 8 y 9: el logaritmo remitido hacia atras; pipeline con logaritmo (D6), sin el umbral
# |lambda| < 0.25 y numerado como el componente; la regla del orden citada; resumen con las dos nulas,
# el caso tramposo, la regla y la sobrediferenciacion; cierre hacia el Capitulo 3.
EDICIONES = [
# retoque de la regla del M7: la atribucion a FPP3 se queda en lo que ya se le atribuia
(
r"""por dos razones. La primera es que la diferencia estacional ya lleva dentro una regular:
          $1 - B^m = (1-B)(1 + B + \cdots + B^{m-1})$. Por eso, como recomienda FPP3, conviene aplicar primero la
          estacional: a veces con ella basta y la serie ya queda estacionaria, y se ahorra una diferencia regular
          que solo añadiría ruido. La segunda es la del Módulo 6:""",
r"""por dos razones. La primera es que a veces con la diferencia estacional basta y la serie ya queda
          estacionaria, con lo que se ahorra una diferencia regular que solo añadiría ruido: por eso la
          recomendación de FPP3 es aplicar primero la estacional. Tiene su explicación: la diferencia estacional ya
          lleva dentro una regular, porque $1 - B^m = (1-B)(1 + B + \cdots + B^{m-1})$. La segunda es la del
          Módulo 6:"""),
# ---------------------------------------------------------------- M8
(
r"""de 1960 son mucho más amplias que las de 1949: la dispersión <strong>crece con el nivel</strong>. Eso viola la
        segunda condición de estacionariedad y ninguna cantidad de diferencias lo corrige.</p>""",
r"""de 1960 son mucho más amplias que las de 1949: la dispersión <strong>crece con el nivel</strong>, el abanico del
        Capítulo 1. Eso viola la segunda condición de estacionariedad y ninguna cantidad de diferencias lo corrige.
        Es la razón por la que los Módulos 6 y 7 trabajaron con <code>log(AirPassengers)</code>.</p>"""),
(
r"""        <p><strong>Al deshacer la transformación aparece un sesgo.</strong> Si pronosticamos $w_t$ y volvemos con
          $\exp(\cdot)$, lo que obtenemos es la <strong>mediana</strong> del pronóstico, no la media""",
r"""        <p><strong>Al deshacer la transformación aparece un sesgo.</strong> Si se pronostica $w_t$ y se vuelve con
          $\exp(\cdot)$, lo que se obtiene es la <strong>mediana</strong> del pronóstico, no la media"""),
(
r"""falta una corrección de sesgo (que <code>fable</code> aplica sola y <code>statsmodels</code> no). Volveremos a
          esto en el Capítulo 6; por ahora basta saber que la vuelta atrás no es simétrica.</p>""",
r"""falta una corrección de sesgo (que <code>fable</code> aplica sola y <code>statsmodels</code> no). El Capítulo 6
          vuelve sobre esto; por ahora basta saber que la vuelta atrás no es simétrica.</p>"""),
(
r"""print(float(np.max(np.abs(y2 - pasajeros))) &lt; 1e-9)
#> True</code></pre>
        </div>
      </div>
""",
r"""print(float(np.max(np.abs(y2 - pasajeros))) &lt; 1e-9)
#> True</code></pre>
        </div>
      </div>

      <p>Con esto están todas las piezas: una transformación para la varianza, dos diferencias para la media y dos
        pruebas para decidir. El Módulo 9 las pone en orden.</p>
"""),
# ---------------------------------------------------------------- M9
(
r"""      <p>Todo el capítulo se resume en una secuencia de decisiones que conviene ejecutar <strong>siempre en este
          orden</strong>, porque cada paso condiciona el diagnóstico del siguiente:</p>""",
r"""      <p>Todo el capítulo se resume en una secuencia de decisiones que conviene ejecutar <strong>siempre en este
          orden</strong>, porque cada paso condiciona el diagnóstico del siguiente. Los pasos 2 a 4 son la regla del
        orden del Módulo 7; los otros tres la rodean de lo que ninguna función hace sola: mirar antes, comprobar
        después y dejar constancia.</p>"""),
(
r"""            <p>Si la dispersión crece con el nivel, transformar <strong>antes</strong> de diferenciar: logaritmo o Box–Cox. El orden importa, porque diferenciar no arregla una varianza que cambia.</p>""",
r"""            <p>Si la dispersión crece con el nivel, transformar <strong>antes</strong> de diferenciar, y en la práctica con el logaritmo (Módulo 8). Si el nivel apenas cambia de escala a lo largo de la muestra no hay nada que estabilizar, y la serie se deja como está. El orden importa, porque diferenciar no arregla una varianza que cambia.</p>"""),
(
r"""            <p><code>BoxCox.lambda(y, method = "guerrero")</code> y <code>BoxCox()</code> (Módulo 8); en Python,""",
r"""            <p><code>log(y)</code>; para compararlo con el $\lambda$ de Guerrero, <code>BoxCox.lambda(y, method = "guerrero")</code> y <code>BoxCox()</code> (Módulo 8); en Python,"""),
(
r"""            <p>Si el $\lambda$ elegido deja el gráfico igual de abombado, o si la serie tiene ceros o negativos, hay que replantear la transformación.</p>""",
r"""            <p>Si tras transformar la amplitud de las oscilaciones sigue creciendo con el nivel, o si la serie tiene ceros o negativos, hay que replantear la transformación.</p>"""),
(
r"""            <p>Si hay estacionalidad, aplicar $\nabla_m$ <strong>antes</strong> que la diferencia regular. Hacerlo al revés cambia el número de diferencias que hace falta: es la trampa del orden del Módulo 7.</p>""",
r"""            <p>Si hay estacionalidad, aplicar $\nabla_m$ <strong>antes</strong> que la diferencia regular: es la regla del orden del Módulo 7. La diferencia estacional ya lleva dentro una regular, y preguntar primero por la regular puede acabar en una diferencia de más, como en <code>log(UKgas)</code>.</p>"""),
(
r"""el ADF puede rechazar la raíz unitaria solo porque usa menos rezagos que el período (Módulo 6).</p>""",
r"""el ADF puede rechazar la raíz unitaria solo porque usa menos rezagos que el periodo estacional (Módulo 6).</p>"""),
(
r"""Una diferencia que las pruebas no pedían → paso 4 con una diferencia menos. Abombamiento → paso 2.""",
r"""Una diferencia que las pruebas no pedían → paso 4 con una diferencia menos. Una amplitud que sigue creciendo con el nivel → paso 2."""),
(
r"""            <p>Guardar $\lambda$, $d$ y $D$ junto al objeto del modelo;""",
r"""            <p>Guardar la transformación (el logaritmo o su $\lambda$) y el número de diferencias regulares y estacionales, $d$ y $D$, junto al objeto del modelo;"""),
# --- el pipeline en R
(
r"""preparar &lt;- function(y, m = frequency(y)) {
  # 1. Estabilizar la varianza
  lambda &lt;- BoxCox.lambda(y, method = "guerrero")
  w &lt;- if (abs(lambda) &lt; 0.25) log(y) else BoxCox(y, lambda)

  # 2. Diferencia estacional PRIMERO
  D &lt;- if (m > 1) nsdiffs(w) else 0
  if (D > 0) w &lt;- diff(w, lag = m, differences = D)

  # 3. Diferencia regular despues
  d &lt;- ndiffs(w)
  if (d > 0) w &lt;- diff(w, differences = d)

  # 4. Verificar: el KPSS de la serie final no debe rechazar
  list(serie = w, lambda = lambda, d = d, D = D,
       var_final = var(w),
       kpss_p = suppressWarnings(kpss.test(w)$p.value))
}

res &lt;- preparar(AirPassengers)
res$d; res$D                 # el modelo airline
#> [1] 1
#> [1] 1
round(res$lambda, 4)
#> [1] -0.2947
# La varianza final esta en la escala Box-Cox: NO es comparable con la de la
# serie original
signif(res$var_final, 3)
#> [1] 9.17e-05
# El p-valor del KPSS es el tope de la tabla (sin suppressWarnings() saldria
# el aviso "greater than printed p-value"): ya no se rechaza la estacionariedad
res$kpss_p
#> [1] 0.1
length(res$serie)            # 144 - 12 - 1: cada diferencia cuesta datos
#> [1] 131

par(mfrow = c(1, 2))
acf(res$serie,  lag.max = 24, main = "ACF final")
pacf(res$serie, lag.max = 24, main = "PACF final")</code></pre>""",
r"""# Los pasos 2 a 5 del procedimiento. El paso 1 (graficar) decide el argumento
# `logaritmo`: TRUE si la dispersion crece con el nivel, FALSE si no hay nada
# que estabilizar. El paso 6 es guardar lo que devuelve la funcion.
preparar &lt;- function(y, logaritmo = TRUE, m = frequency(y)) {
  # Paso 2. Estabilizar la varianza: el logaritmo (Modulo 8)
  w &lt;- if (logaritmo) log(y) else y

  # Paso 3. Diferencia estacional PRIMERO (la regla del orden, Modulo 7)
  D &lt;- if (m > 1) nsdiffs(w) else 0
  if (D > 0) w &lt;- diff(w, lag = m, differences = D)

  # Paso 4. Diferencia regular, sobre lo que dejo el paso 3
  d &lt;- ndiffs(w)
  if (d > 0) w &lt;- diff(w, differences = d)

  # Paso 5. Verificar: el KPSS de la serie final no debe rechazar
  list(serie = w, logaritmo = logaritmo, d = d, D = D,
       kpss_p = suppressWarnings(kpss.test(w)$p.value))
}

res &lt;- preparar(AirPassengers)
res$d; res$D                 # el modelo airline
# El p-valor del KPSS es el tope de la tabla (sin suppressWarnings() saldria
# el aviso "greater than printed p-value"): ya no se rechaza la estacionariedad
res$kpss_p
length(res$serie)            # 144 - 12 - 1: cada diferencia cuesta datos

# El lambda de Guerrero se anota para comparar, pero no decide: el Modulo 8
# explica por que se prefiere el logaritmo
round(BoxCox.lambda(AirPassengers, method = "guerrero"), 4)

# Lo que queda en la serie final: estacionaria, pero no ruido blanco
par(mfrow = c(1, 2))
r &lt;- acf(res$serie,  lag.max = 24, main = "ACF final")$acf[-1]
pacf(res$serie, lag.max = 24, main = "PACF final")
round(r[c(1, 12)], 3)                                # r1 y r12
sum(abs(r) > 1.96 / sqrt(length(res$serie)))         # de 24 rezagos</code></pre>"""),
# --- el pipeline en Python
(
r"""def preparar(y, m=12):
    # 1. Estabilizar la varianza (en la practica, el logaritmo)
    w = np.log(y)

    # 2. Diferencia estacional PRIMERO. Aqui D no se decide con una prueba:
    #    se fija en 1 siempre que m &gt; 1, sea o no estacional la serie
    #    (statsmodels no trae un equivalente de nsdiffs)
    D = 1 if m > 1 else 0
    if D:
        w = w.diff(m).dropna()

    # 3. Diferencia regular despues
    est, p = kpss_como_ndiffs(w)
    d = 1 if p &lt; 0.05 else 0
    if d:
        w = w.diff().dropna()

    est, p = kpss_como_ndiffs(w)
    return {"serie": w, "d": d, "D": D,
            "var_final": float(w.var()), "kpss_p": float(p)}

res = preparar(pasajeros)
print(res["d"], res["D"], round(res["var_final"], 5), round(res["kpss_p"], 3))
#> 1 1 0.0021 0.1

# d coincide con la version en R; D tambien, pero aqui estaba puesto a mano.
# La varianza final NO coincide con la del bloque de R (9.17e-05) y no tiene
# por que: esta version usa el logaritmo y aquella el lambda optimo de
# Box-Cox. Son escalas distintas, asi que solo son comparables las decisiones
# (d y D), no los numeros.</code></pre>""",
r"""# Los pasos 2 a 5 del procedimiento. El paso 1 (graficar) decide el argumento
# `logaritmo`; el paso 6 es guardar lo que devuelve la funcion.
def preparar(y, logaritmo=True, m=12):
    # Paso 2. Estabilizar la varianza: el logaritmo (Modulo 8)
    w = np.log(y) if logaritmo else y

    # Paso 3. Diferencia estacional PRIMERO. Aqui D no se decide con una
    #    prueba: se fija en 1 siempre que m &gt; 1, sea o no estacional la
    #    serie (statsmodels no trae un equivalente de nsdiffs)
    D = 1 if m > 1 else 0
    if D:
        w = w.diff(m).dropna()

    # Paso 4. Diferencia regular, sobre lo que dejo el paso 3
    est, p = kpss_como_ndiffs(w)
    d = 1 if p &lt; 0.05 else 0
    if d:
        w = w.diff().dropna()

    # Paso 5. Verificar: el KPSS de la serie final no debe rechazar
    est, p = kpss_como_ndiffs(w)
    return {"serie": w, "logaritmo": logaritmo, "d": d, "D": D, "kpss_p": float(p)}

res = preparar(pasajeros)
print(res["d"], res["D"], round(res["kpss_p"], 3), len(res["serie"]))

# d y D coinciden con la version en R (aqui D estaba puesto a mano), y como
# las dos versiones usan el logaritmo, la serie final es la misma: r1 y r12
r = acf(res["serie"], nlags=24, adjusted=False)[1:]
print(np.round(r[[0, 11]], 3))
print(int(np.sum(np.abs(r) > 1.96 / np.sqrt(len(res["serie"])))))   # de 24 rezagos</code></pre>"""),
(
r"""from statsmodels.tsa.stattools import kpss

datos = sm.datasets.get_rdataset("AirPassengers").data
pasajeros = pd.Series(
    datos["value"].values,
    index=pd.date_range("1949-01-01", periods=len(datos), freq="MS"),
)

# Para que esta funcion decida IGUAL""",
r"""from statsmodels.tsa.stattools import acf, kpss

datos = sm.datasets.get_rdataset("AirPassengers").data
pasajeros = pd.Series(
    datos["value"].values,
    index=pd.date_range("1949-01-01", periods=len(datos), freq="MS"),
)

# Para que esta funcion decida IGUAL"""),
(
r"""entrena con datos posteriores a los de prueba. Hay que usar validación de origen móvil, y a eso dedicamos el
            Capítulo 6.</li>""",
r"""entrena con datos posteriores a los de prueba. Hay que usar validación de origen móvil, y a eso se dedica el
            Capítulo 6.</li>"""),
# --- el resumen
(
r"""          <tr>
            <td>ACF ($\rho_k$)</td>
            <td>Correlación total con el rezago $k$</td>
            <td><code>acf()</code></td>
          </tr>""",
r"""          <tr>
            <td>ACF ($\rho_k$)</td>
            <td>Correlación total con el rezago $k$</td>
            <td><code>acf()</code></td>
          </tr>
          <tr>
            <td>Banda $\pm 1.96/\sqrt{T}$</td>
            <td>Donde cae el 95 % de las barras de un ruido blanco: una que asoma no es evidencia; un patrón, sí</td>
            <td>la dibuja <code>acf()</code></td>
          </tr>"""),
(
r"""          <tr>
            <td>Raíz unitaria</td>
            <td>$\phi = 1$: los choques no se olvidan nunca</td>
            <td><code>adf.test()</code>, <code>kpss.test()</code></td>
          </tr>
          <tr>
            <td>Diferenciación</td>
            <td>$\nabla y_t = (1-B)y_t$ elimina la raíz unitaria</td>
            <td><code>diff()</code>, <code>ndiffs()</code></td>
          </tr>""",
r"""          <tr>
            <td>Raíz unitaria</td>
            <td>$\phi = 1$: los choques no se olvidan nunca</td>
            <td>—</td>
          </tr>
          <tr>
            <td>ADF y KPSS</td>
            <td>Hipótesis nulas <strong>contrarias</strong>: un p-valor pequeño rechaza la raíz unitaria en el ADF
              y la estacionariedad en el KPSS</td>
            <td><code>adf.test()</code>, <code>kpss.test()</code></td>
          </tr>
          <tr>
            <td>El ADF con estacionalidad</td>
            <td>Con menos rezagos que el periodo estacional rechaza la raíz unitaria sin motivo: no se aplica a
              una serie estacional cruda</td>
            <td><code>adf.test(y, k = 12)</code> para comprobarlo</td>
          </tr>
          <tr>
            <td>Diferenciación</td>
            <td>$\nabla y_t = (1-B)y_t$ elimina la raíz unitaria; $\nabla_m y_t = (1-B^m)y_t$, la estacionalidad.
              Cada una cuesta tantos datos como su rezago</td>
            <td><code>diff()</code></td>
          </tr>
          <tr>
            <td>Regla del orden</td>
            <td>Transformar, decidir la diferencia estacional y, sobre lo que quede, la regular</td>
            <td><code>nsdiffs()</code> y después <code>ndiffs()</code></td>
          </tr>
          <tr>
            <td>Sobrediferenciación</td>
            <td>Una diferencia de más fabrica autocorrelación (su indicio, $r_1$ cerca de $-0.5$) y quita datos</td>
            <td>—</td>
          </tr>"""),
(
r"""          <tr>
            <td>Box–Cox</td>
            <td>Estabiliza la varianza; $\lambda = 0$ es el logaritmo</td>
            <td><code>BoxCox.lambda()</code></td>
          </tr>""",
r"""          <tr>
            <td>Box–Cox</td>
            <td>Estabiliza la varianza; $\lambda = 0$ es el logaritmo, que es lo que se usa en la práctica</td>
            <td><code>log()</code>, <code>BoxCox.lambda()</code></td>
          </tr>
          <tr>
            <td>Pipeline</td>
            <td>Graficar, transformar, $\nabla_m$, $\nabla$, verificar y documentar, siempre en ese orden</td>
            <td><code>preparar()</code>, en este módulo</td>
          </tr>"""),
# --- la pista del ejercicio 3
(
r"""<code>ndiffs(USAccDeaths)</code> directamente, desconfía del número que salga y relee la «Regla de
              trabajo» del Módulo 6.</p>""",
r"""<code>ndiffs(USAccDeaths)</code> directamente, desconfía del número que salga y relee la regla del orden
              del Módulo 7.</p>"""),
(
r"""              <em>airline</em> que ajustaremos en el Capítulo 5. Un $r_1$ negativo""",
r"""              <em>airline</em> que se ajusta en el Capítulo 5. Un $r_1$ negativo"""),
# --- el cierre
(
r"""      <div class="references">
        <h3><i class="fas fa-book-open mr-2" aria-hidden="true"></i>Lecturas de este capítulo</h3>""",
r"""      <h3>Lo que sigue: de la serie estacionaria al modelo</h3>

      <p>El capítulo termina con una serie estacionaria, no con un modelo. La que devuelve el pipeline,
        $\nabla\nabla_{12}\log y_t$, ya no pide diferencias, pero tampoco es ruido blanco: $r_1 = -0.341$,
        $r_{12} = -0.387$ y 5 de sus 24 autocorrelaciones fuera de la banda. Queda dependencia, y describirla es el
        trabajo del Capítulo 3.</p>

      <p>Allí vuelven, convertidas en herramienta, cuatro piezas de este capítulo. El ruido blanco (Módulo 2) pasa a
        ser el material con que se construyen los procesos AR y MA, y la vara con que se juzgan sus residuales, ya
        con una prueba formal. La pareja de ACF y PACF (Módulos 3 y 4) deja de describir y empieza a identificar:
        cuál de las dos se corta, y en qué rezago, dice qué modelo proponer. El operador $B$ y la raíz fuera del
        círculo unitario (Módulos 5 y 7) se extienden a procesos con más de un rezago. Y la TRM (Módulo 6), ya
        diferenciada, es una de las series que allí se modelan. <code>AirPassengers</code> espera al Capítulo 5, que
        ajusta sobre $\nabla\nabla_{12}\log y_t$ el modelo <em>airline</em>.</p>

      <div class="references">
        <h3><i class="fas fa-book-open mr-2" aria-hidden="true"></i>Lecturas de este capítulo</h3>"""),
]
