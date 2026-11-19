#!/usr/bin/env python3
"""R5 del capítulo 2 · T5.3: los cinco ejercicios del Módulo 9.

Lo importa `r5_edita.py`. Rehace los ejercicios 1, 2, 3 y 5 (enunciado con entregables,
pista y solución) y retoca el 4 (enunciado, pista, tres líneas de código y un párrafo).
El código de las soluciones 1, 2, 3 y 5 se lee de `r5_bloques/e?.out` (salida real de
`r5_reprex.R`). Los dos bloques largos del ejercicio 4 se conservan tal cual de HEAD.
"""
import re
from r5_ediciones_cortos import codigo


def botones(n, etiqueta_sol="Solución", icono="fa-key"):
    return f'''          <div class="ejercicio-acciones">
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c2e{n}-pista">
              <i class="fas fa-lightbulb" aria-hidden="true"></i> Pista <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c2e{n}-sol">
              <i class="fas {icono}" aria-hidden="true"></i> {etiqueta_sol} <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
          </div>'''


def lista(items):
    cuerpo = "\n".join(f"            <li>{i}</li>" for i in items)
    return ('          <ol style="list-style-type: lower-alpha; margin-top: 0.5rem; margin-bottom: 0;">\n'
            f"{cuerpo}\n          </ol>")


def enunciado(n, texto):
    return (f'          <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;">'
            f'<span class="ejercicio-numero">{n}.</span>{texto}</p>')


def pista(n, texto):
    return f'''          <div class="ejercicio-panel pista" id="c2e{n}-pista" hidden>
            <p style="margin:0;">{texto}</p>
          </div>'''


def panel_sol(n, cuerpo):
    return f'''          <div class="ejercicio-panel solucion" id="c2e{n}-sol" hidden>
{cuerpo}
          </div>'''


def guiado(*partes):
    return '        <div class="ejercicio-guiado">\n' + "\n".join(partes) + "\n        </div>\n"


# ------------------------------------------------------------------ Ejercicio 1
E1 = guiado(
    enunciado(1, "Toma la serie <code>co2</code> de R (la concentración de CO₂ en Mauna Loa, en partes por "
                 "millón, mensual de 1959 a 1997) y aplícale el pipeline de este módulo. Entrega:"),
    lista([
        "La decisión del paso 2 —el argumento <code>logaritmo</code> de <code>preparar()</code>— y una "
        "medida que la respalde.",
        "Cuántas diferencias estacionales y regulares hacen falta, $D$ y $d$, decididas en el orden de la "
        "regla.",
        "El correlograma en cada etapa —la serie de partida, tras la primera diferencia y la serie final—: "
        "qué dice en cada una.",
        "La ACF y la PACF de la serie final: cuántas barras salen de la banda y en qué rezagos. ¿Es ruido "
        "blanco?",
    ]),
    botones(1),
    pista(1, "El argumento <code>logaritmo</code> no lo decide ninguna función: lo decide el paso 1, "
             "mirando. Relee qué pide el paso 2 del ciclo para dejar una serie como está y busca una medida "
             "que lo compruebe. Después sigue la regla del orden, y vuelve a mirar el correlograma tras cada "
             "diferencia, no solo el de la serie de partida."),
    panel_sol(1, f'''            <p><strong>Respuesta: sin logaritmo, $D = 1$ y $d = 1$.</strong></p>
            <pre><code class="language-r">{codigo("e1")}</code></pre>
            <table>
              <caption class="sr-only">Lo que dicen el paso 2, las pruebas y el correlograma sobre co2</caption>
              <thead>
                <tr><th scope="col">Dónde se mira</th><th scope="col">Qué dice</th></tr>
              </thead>
              <tbody>
                <tr><td>Paso 2</td><td>El máximo de la serie es 1.17 veces su mínimo (en
                  <code>AirPassengers</code>, 5.98 veces): el nivel apenas cambia de escala y no hay nada que
                  estabilizar. <code>logaritmo = FALSE</code></td></tr>
                <tr><td>Pruebas</td><td><code>nsdiffs()</code> pide 1; sobre $\\nabla_{{12}} y_t$,
                  <code>ndiffs()</code> pide 1 más</td></tr>
                <tr><td>Correlograma de partida</td><td>$r_1 = 0.991$ y $r_{{12}} = 0.928$: tendencia
                  <em>y</em> estacionalidad, las dos muy marcadas</td></tr>
                <tr><td>Correlograma tras $\\nabla_{{12}}$</td><td>$r_1 = 0.800$, $r_2 = 0.720$, $r_3 = 0.628$:
                  baja despacio, queda una raíz unitaria regular</td></tr>
                <tr><td>Serie final, $\\nabla\\nabla_{{12}} y_t$</td><td>$n = 455$ y banda $\\pm 0.092$. La ACF
                  sale en los rezagos 1, 3, 9, 11 y 12; la PACF, en 1, 3, 9, 11, 12, 13 y 24</td></tr>
              </tbody>
            </table>
            <p><strong>La serie final</strong> ya no pide diferencias y el KPSS no rechaza la estacionariedad
              ($p &gt; 0.10$). No es ruido blanco: salen de la banda 5 de las 24 barras de la ACF y 7 de las de la
              PACF, con $r_1 = -0.302$ y $r_{{12}} = -0.420$. Queda dependencia de un mes al siguiente y de un
              año al siguiente, y describirla es el trabajo de los Capítulos 3 y 5. Ese $r_1$ negativo no es
              el rastro de una diferencia de más: las pruebas pedían las dos y ya no piden ninguna.</p>
            <p style="margin-bottom:0;"><strong>Sobre el logaritmo.</strong> La decisión del paso 2 aquí pesa
              poco, y conviene comprobarlo en vez de suponerlo: con <code>logaritmo = TRUE</code> las dos
              funciones piden lo mismo, $D = 1$ y $d = 1$, como muestra la última línea del código. Sobre un
              nivel que solo cambia un 17 %, la serie y su logaritmo cuentan la misma historia.</p>'''),
)

# ------------------------------------------------------------------ Ejercicio 2
E2 = guiado(
    enunciado(2, "Simula 500 caminatas aleatorias de longitud 144, la del Monte Carlo del Módulo 6, y "
                 "aplica <code>adf.test()</code> a cada una. Entrega:"),
    lista([
        "El porcentaje de series en que la prueba rechaza $H_0$ al 5&nbsp;%.",
        "El error de Monte Carlo de ese porcentaje: entre qué valores esperarías verlo, con 500 series, si "
        "la prueba rechazara exactamente el 5&nbsp;%. ¿Dónde caen tu resultado y la barra de amplitud 0 del "
        "Módulo 6, que marca 3.2&nbsp;%?",
        "El mismo porcentaje después de sumarles a esas mismas 500 caminatas la oscilación "
        "$4\\sin(2\\pi t/12)$.",
        "Una frase: qué cambió entre (a) y (c), y qué no.",
    ]),
    botones(2),
    pista(2, "En estas 500 series $H_0$ (hay raíz unitaria) es <strong>cierta por construcción</strong>, "
             "porque tú las fabricaste como caminatas: todo rechazo es un error de tipo I. Antes de correr "
             "nada, predice cuántos esperas si la prueba está bien calibrada. Y para el apartado (b), piensa "
             "que un porcentaje calculado con 500 series es él mismo una estimación, con su desviación "
             "típica."),
    panel_sol(2, f'''            <p><strong>Respuesta: 3.0&nbsp;% sin la oscilación y 21.6&nbsp;% con ella.</strong></p>
            <pre><code class="language-r">{codigo("e2")}</code></pre>
            <p><strong>(a) y (b)</strong> Con 500 series, una prueba que rechazara exactamente el 5&nbsp;%
              daría, por el puro azar del experimento, entre 3.1&nbsp;% y 6.9&nbsp;% (dos errores típicos de 0.97
              puntos a cada lado). El 3.0&nbsp;% de aquí y el 3.2&nbsp;% del Módulo 6 —que es este mismo
              experimento con otra semilla— caen en el borde de abajo. Con 5000 series el error baja a 0.3
              puntos y sale 4.3&nbsp;%: con esta longitud la prueba rechaza algo menos de lo que anuncia. Se
              queda corta, que es el lado prudente: no fabrica rechazos.</p>
            <p><strong>(c) y (d)</strong> Con las mismas caminatas —el mismo azar, la misma longitud, la misma
              raíz unitaria— y la oscilación como único cambio, el falso rechazo sube a 21.6&nbsp;%. El Módulo 6
              obtuvo 17.6&nbsp;% con otras 500: cuatro puntos de diferencia entre dos experimentos de ese tamaño
              también son error de Monte Carlo, que para esa comparación ronda los 2.5 puntos. Lo que no
              cabe en ese error es el salto de 3 a más de 17.</p>
            <p style="margin-bottom:0;">Conclusión: el ADF <strong>no está roto</strong>. Sobre caminatas puras
              rechaza poco, y sobre ruido blanco, donde $H_0$ es falsa, rechaza el 99.8&nbsp;% de las veces. Lo
              que lo rompe es aplicarlo a una serie estacional con menos rezagos que el periodo.</p>'''),
)

# ------------------------------------------------------------------ Ejercicio 3
E3 = guiado(
    enunciado(3, "Sobre <code>USAccDeaths</code> (las muertes accidentales de cada mes en Estados Unidos, "
                 "de 1973 a 1978), compara tres series diferenciadas: $\\nabla y_t$, $\\nabla_{12} y_t$ y "
                 "$\\nabla_{12}\\nabla y_t$. Entrega:"),
    lista([
        "Lo que piden <code>nsdiffs()</code> y <code>ndiffs()</code>, consultadas en el orden de la regla.",
        "Una tabla con $n$, la banda, $r_1$, $r_{12}$ y el número de barras, de 24, que salen de la banda, "
        "para la serie de partida y para las tres diferenciadas.",
        "Cuál de las tres queda más cerca del ruido blanco, y si su $r_1$ es una señal de "
        "sobrediferenciación.",
    ]),
    botones(3),
    pista(3, "Las cuatro series de la tabla no tienen la misma longitud, así que no comparten banda: "
             "calcula la de cada una. Y antes de preguntarle nada a <code>ndiffs()</code>, relee la caja "
             "«Regla del orden» del Módulo 7: importa sobre qué serie se le pregunta."),
    panel_sol(3, f'''            <p><strong>Respuesta: $\\nabla_{{12}}\\nabla y_t$.</strong></p>
            <pre><code class="language-r">{codigo("e3")}</code></pre>
            <table>
              <caption class="sr-only">Comparación de las tres diferenciaciones sobre USAccDeaths</caption>
              <thead>
                <tr>
                  <th scope="col">Serie</th><th scope="col">$n$</th><th scope="col">Banda</th>
                  <th scope="col">$r_1$</th><th scope="col">$r_{{12}}$</th>
                  <th scope="col">Fuera de la banda</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>De partida</td><td>72</td><td>$\\pm 0.231$</td><td>0.707</td><td>0.629</td><td>14 de 24</td></tr>
                <tr><td>$\\nabla$</td><td>71</td><td>$\\pm 0.233$</td><td>0.023</td><td>0.709</td><td>6 de 24</td></tr>
                <tr><td>$\\nabla_{{12}}$</td><td>60</td><td>$\\pm 0.253$</td><td>0.690</td><td>−0.077</td><td>6 de 24</td></tr>
                <tr><td><strong>$\\nabla_{{12}}\\nabla$</strong></td><td>59</td><td>$\\pm 0.255$</td><td>−0.353</td><td>−0.336</td><td><strong>2 de 24</strong></td></tr>
              </tbody>
            </table>
            <p><strong>(a)</strong> <code>nsdiffs()</code> pide 1 y, sobre $\\nabla_{{12}} y_t$,
              <code>ndiffs()</code> pide 1. Preguntada por la serie de partida, <code>ndiffs()</code> devuelve
              0: es la trampa que la regla del orden evita.</p>
            <p><strong>(b) y (c)</strong> Cada diferencia sola arregla la mitad del problema y deja la otra
              intacta: $\\nabla$ limpia el rezago 1 ($r_1 = 0.023$) y deja viva la estacionalidad
              ($r_{{12}} = 0.709$), y $\\nabla_{{12}}$ hace lo contrario. Solo con las dos baja el recuento a 2
              barras de 24, cerca de las 1.2 que un ruido blanco dejaría fuera por azar. El recuento de barras
              es la herramienta de este capítulo; el Capítulo 3 lo cambia por la prueba formal que anunció el
              Módulo 3.</p>
            <p style="margin-bottom:0;"><strong>Sobre el $r_1 = -0.353$:</strong> se parece al $-0.5$ del
              Módulo 7, pero aquí no delata una diferencia de más, porque las pruebas pedían las dos. Un $r_1$
              negativo es un indicio de sobrediferenciación, no una prueba: decide si el correlograma y las
              pruebas de la serie anterior pedían o no la diferencia. Lo que queda en esta serie —también
              $r_{{12}} = -0.336$ sale de la banda— es dependencia por describir, no un defecto del
              preprocesamiento.</p>'''),
)

# ------------------------------------------------------------------ Ejercicio 5
E5 = guiado(
    enunciado(5, "<strong>Con IA como tutor:</strong> pide a un asistente que te explique por qué el ADF "
                 "puede rechazar la raíz unitaria en una serie estacional, y pon a prueba su explicación con "
                 "una serie que este capítulo no resolvió: <code>UKDriverDeaths</code>, los conductores "
                 "muertos o heridos graves cada mes en Gran Bretaña, de 1969 a 1984. Entrega:"),
    lista([
        "Una tabla de dos columnas: cada afirmación del asistente y cómo la comprobaste, o «sin comprobar».",
        "Un párrafo con lo que su explicación predecía para esa serie y lo que salió al ejecutarlo.",
    ]),
    botones(5, "Criterios de una buena respuesta", "fa-list-check"),
    pista(5, "No le preguntes solo «¿por qué?». Pídele además una <strong>predicción que se pueda "
             "comprobar</strong>: algo que, si su explicación es correcta, tendría que cambiar al modificar "
             "la prueba, y en qué dirección. Una explicación que no permite predecir nada no se puede "
             "verificar, y ahí está el ejercicio."),
    panel_sol(5, f'''            <p>Al ser un ejercicio abierto no hay respuesta única, pero sí criterios claros. Una buena entrega:</p>
            <ol>
              <li><strong>Identifica el mecanismo concreto</strong>, no una vaguedad. «La estacionalidad afecta
                a la prueba» no sirve; «los $k = 5$ rezagos por defecto no cubren el periodo $m = 12$, así que
                la oscilación anual queda en el residuo y se lee como reversión a la media» sí.</li>
              <li><strong>Convierte la explicación en una predicción y la ejecuta.</strong> Si el mecanismo es
                el número de rezagos, cubrir un periodo completo debe cambiar el resultado. En
                <code>UKDriverDeaths</code> lo cambia: el estadístico pasa de $-6.54$ ($p &lt; 0.01$) a
                $-2.58$ ($p = 0.33$).</li>
              <li><strong>Separa lo verificado de lo aceptado a ciegas.</strong> Ejemplo de lo primero: los
                estadísticos con distintos $k$, o el resultado sobre la serie desestacionalizada. Ejemplo de lo
                segundo: cualquier afirmación sobre «lo que dice la literatura» o sobre la distribución
                asintótica del estadístico, que no comprobaste.</li>
              <li><strong>Señala los errores del asistente, si los hubo:</strong> por ejemplo, que confunda la
                estacionalidad con la tendencia, que atribuya el problema a la tabla de p-valores y no a la
                especificación, o que dé un valor crítico sin decir de dónde sale. Detectarlo <em>es</em> el
                ejercicio.</li>
            </ol>
            <pre><code class="language-r">{codigo("e5")}</code></pre>
            <p style="margin-bottom:0;">La idea de fondo vale para todo el curso: un asistente es útil para
              generar hipótesis y rapidísimo para producir texto plausible. La parte que no se le puede
              delegar es la verificación, y en series de tiempo verificar casi siempre significa
              <strong>correr el código y mirar el número</strong>.</p>'''),
)


def e4(viejo):
    """El ejercicio 4 de HEAD con cinco cambios puntuales."""
    def cambia(a, b):
        nonlocal viejo
        assert viejo.count(a) == 1, a[:60]
        viejo = viejo.replace(a, b)

    cambia('''          <p class="ejercicio-enunciado"><span class="ejercicio-numero">4.</span>Descarga la TRM actualizada de
            <a href="https://www.datos.gov.co/resource/32sa-8pi3.json" target="_blank" rel="noopener">datos.gov.co</a>
            y repite el análisis del Módulo 6 con los datos más recientes. ¿Cambia la conclusión sobre la raíz
            unitaria?</p>
''', '''          <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;"><span class="ejercicio-numero">4.</span>Descarga la TRM actualizada de
            <a href="https://www.datos.gov.co/resource/32sa-8pi3.json" target="_blank" rel="noopener">datos.gov.co</a>
            y repite el análisis del Módulo 6 con los datos más recientes. Entrega:</p>
''' + lista([
        "Cuántos meses tiene tu serie y hasta cuál llega.",
        "La especificación que eliges, y por qué: el KPSS de nivel o el de tendencia, y si hace falta "
        "cambiar los rezagos del ADF.",
        "Las dos pruebas sobre la TRM y sobre su primera diferencia, con la fila de la tabla del Módulo 6 en "
        "que cae cada pareja. ¿Cambia la conclusión sobre la raíz unitaria?",
        "El ADF sobre la serie recortada a los meses que van desde enero de 2022. ¿Qué cambia, y por qué?",
    ]) + "\n")
    cambia('''            <p style="margin:0;">El Módulo 6 trabaja con una copia fija de la serie, cortada en junio de 2026. El código
              que descarga la serie al día está al abrir «Cómo comprobarlo», listo para copiar. Antes de correrlo,
              escribe tu predicción: el Módulo 6 encontró en la TRM una raíz unitaria, así que ¿esperas que unos meses más de datos cambien el veredicto?</p>''',
           '''            <p style="margin:0;">El Módulo 6 trabaja con una copia fija de la serie, cortada en junio de 2026. El código
              que descarga la serie al día está al abrir «Cómo comprobarlo», listo para copiar. Antes de correrlo,
              escribe tu predicción para los apartados (c) y (d), con su porqué. Para el (b), relee en el
              Módulo 6 el «detalle de especificación» del caso limpio y la advertencia del caso tramposo, y
              di cuál de los dos problemas puede tener una serie como esta.</p>''')
    cambia('''round(c(adf.test(trm)$p.value, adf.test(diff(trm))$p.value), 3)
#> [1] 0.585 0.017
''', '''round(c(adf.test(trm)$p.value, adf.test(diff(trm))$p.value), 3)
#> [1] 0.585 0.017
# El KPSS que corresponde a adf.test() es el de tendencia (0.01 es p &lt; 0.01)
suppressWarnings(kpss.test(trm, null = "Trend"))$p.value
#> [1] 0.01
''')
    cambia('''            <pre><code class="language-r">library(tseries); library(jsonlite)
''', '''            <p><strong>La especificación.</strong> La TRM no es estacional —sobre la copia fija,
              <code>nsdiffs()</code> devuelve 0—, así que los 5 rezagos por defecto del ADF no tienen el
              problema del caso tramposo y no hace falta cambiarlos. Y como la regresión de
              <code>adf.test()</code> lleva tendencia, el KPSS que le corresponde es el de tendencia, que
              sobre la copia fija rechaza igual que el de nivel ($p &lt; 0.01$).</p>
            <pre><code class="language-r">library(tseries); library(jsonlite)
''')
    return viejo


def aplica(src):
    ini = src.index('        <div class="ejercicio-guiado">\n          <p class="ejercicio-enunciado"><span class="ejercicio-numero">1.</span>')
    fin = src.index('      </div>\n\n      <h3>Lo que sigue: de la serie estacionaria al modelo</h3>')
    viejo = src[ini:fin]
    partes = re.split(r'(?=        <div class="ejercicio-guiado">\n)', viejo)
    partes = [p for p in partes if p.strip()]
    assert len(partes) == 5, len(partes)
    e4_nuevo = e4(partes[3])
    nuevo = E1 + "\n" + E2 + "\n" + E3 + "\n" + e4_nuevo.rstrip("\n") + "\n\n" + E5
    return src[:ini] + nuevo + src[fin:]
