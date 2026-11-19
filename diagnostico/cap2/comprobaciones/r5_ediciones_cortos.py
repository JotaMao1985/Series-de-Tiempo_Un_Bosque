#!/usr/bin/env python3
"""R5 del capítulo 2 · T5.1: los siete ejercicios cortos «Para practicar» (D9).

No se ejecuta solo: lo importa `r5_edita.py`, que parte del capítulo de HEAD y aplica las
tres tandas (cortos, Módulo 9, quiz) y los minutos. El código de cada solución NO está
escrito aquí: se lee de `r5_bloques/<id>.out`, que es la salida de `r5_reprex.R` sobre
`r5_bloques/<id>.R`, con cada resultado real bajo su línea tras `#> `.
"""
import html
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def codigo(nombre):
    """El bloque ejecutado, escapado como el resto del capítulo (`<` y `&`; `>` se deja)."""
    t = (AQUI / "r5_bloques" / f"{nombre}.out").read_text(encoding="utf-8").rstrip("\n")
    return html.escape(t, quote=False).replace("&gt;", ">")


def ejercicio(mid, enunciado, entregables, pista, solucion):
    items = "\n".join(f"            <li>{e}</li>" for e in entregables)
    return f'''      <div class="exercise">
        <h4><i class="fas fa-pen-to-square mr-2" aria-hidden="true"></i>Para practicar</h4>
        <div class="ejercicio-guiado">
          <p class="ejercicio-enunciado" style="margin-bottom: 0.75rem;">{enunciado}</p>
          <ol style="list-style-type: lower-alpha; margin-top: 0.5rem; margin-bottom: 0;">
{items}
          </ol>
          <div class="ejercicio-acciones">
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c2m{mid}-pista">
              <i class="fas fa-lightbulb" aria-hidden="true"></i> Pista <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c2m{mid}-sol">
              <i class="fas fa-key" aria-hidden="true"></i> Solución <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
          </div>
          <div class="ejercicio-panel pista" id="c2m{mid}-pista" hidden>
            <p style="margin:0;">{pista}</p>
          </div>
          <div class="ejercicio-panel solucion" id="c2m{mid}-sol" hidden>
{solucion}
          </div>
        </div>
      </div>
'''


def sol(respuesta, bloque, parrafos):
    cuerpo = [f"            <p><strong>Respuesta: {respuesta}</strong></p>",
              f'            <pre><code class="language-r">{codigo(bloque)}</code></pre>']
    for i, p in enumerate(parrafos):
        estilo = ' style="margin-bottom:0;"' if i == len(parrafos) - 1 else ""
        cuerpo.append(f"            <p{estilo}>{p}</p>")
    return "\n".join(cuerpo)


CORTOS = {}

# ---------------------------------------------------------------- Módulo 1
CORTOS[1] = ejercicio(
    1,
    "Un proceso se construye así: en los instantes impares, $y_t$ sigue una normal de media 0 y varianza 1; "
    "en los pares, una uniforme entre $-\\sqrt{3}$ y $\\sqrt{3}$. Todos los valores son independientes entre "
    "sí. Entrega cuatro cosas:",
    [
        "La media y la varianza de $y_t$ en un instante impar y en uno par, y la covarianza entre dos "
        "instantes distintos. ¿Cumple el proceso las tres condiciones de la estacionariedad débil? (La "
        "varianza de una uniforme entre $a$ y $b$ es $(b-a)^2/12$.)",
        "La probabilidad de que $y_t$ pase de 2 en un instante impar y en uno par. ¿Es el proceso "
        "estrictamente estacionario? Di qué instantes y qué desplazamiento $h$ de la definición lo deciden.",
        "Una comprobación: simula 20 000 valores y calcula por separado, en los impares y en los pares, la "
        "media, la varianza y la proporción de valores mayores que 2.",
        "El caso contrario: un millón de valores independientes de <code>rcauchy()</code>, una distribución "
        "de colas tan pesadas que no tiene varianza finita. ¿Es ese proceso estrictamente estacionario? ¿Y "
        "débilmente? Calcula la varianza muestral de los primeros 100, 10 000 y 1 000 000 valores y di qué "
        "le pasa.",
    ],
    "Las dos definiciones no miran lo mismo: la débil pregunta solo por la media, la varianza y las "
    "covarianzas; la estricta, por la distribución entera. Para cada proceso haz dos listas: qué cambia de "
    "un instante a otro y qué no. Y en el apartado (d), relee la segunda condición de la débil palabra por "
    "palabra.",
    sol(
        "el primer proceso es débilmente estacionario y no lo es en sentido estricto; el segundo, al revés.",
        "m1",
        [
            "<strong>(a)</strong> En los dos tipos de instante la media es 0 y la varianza es 1 —la de la "
            "uniforme, $(2\\sqrt{3})^2/12 = 1$—, y la covarianza entre dos instantes distintos es 0, porque "
            "los valores son independientes. Se cumplen las tres condiciones: el proceso es débilmente "
            "estacionario.",
            "<strong>(b)</strong> En un instante impar, la probabilidad de pasar de 2 es 0.0228; en uno par "
            "es 0, porque la uniforme no llega más allá de $\\sqrt{3} = 1.732$. La distribución de $y_1$ no "
            "es la de $y_2$: basta un solo instante, $t_1 = 1$, y el desplazamiento $h = 1$ para que la "
            "definición falle. El proceso no es estrictamente estacionario.",
            "<strong>(c)</strong> La simulación dice lo mismo. Las medias (0.011 y 0.003), las varianzas "
            "(0.987 y 0.994) y la correlación entre valores vecinos (0.003) no distinguen los instantes "
            "pares de los impares; la proporción de valores por encima de 2, sí: 0.0225 en los impares y "
            "ninguno en los pares.",
            "<strong>(d)</strong> Los valores de Cauchy son independientes y tienen todos la misma "
            "distribución, así que cualquier grupo de ellos tiene la misma distribución conjunta que el "
            "mismo grupo desplazado: el proceso es estrictamente estacionario. No es débilmente "
            "estacionario, porque la segunda condición pide una varianza finita y aquí no la hay: la "
            "varianza muestral no se asienta al añadir datos (753, 3125 y 182 823). Es lo que hay detrás de "
            "la nota del módulo: la estacionariedad estricta implica la débil solo cuando la varianza es "
            "finita, y la débil no implica la estricta.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 2
CORTOS[2] = ejercicio(
    2,
    "<code>EuStockMarkets</code> trae el cierre diario de cuatro índices bursátiles europeos entre 1991 y "
    "1998; la columna <code>DAX</code> es el alemán, con 1860 días. El <strong>rendimiento</strong> de un "
    "día es el cambio del logaritmo del índice respecto del día anterior: "
    "<code>r &lt;- diff(log(EuStockMarkets[, \"DAX\"]))</code>, 1859 valores. Entrega tres cosas:",
    [
        "De las 24 primeras autocorrelaciones de <code>r</code>, cuántas salen de la banda y en qué "
        "rezagos. ¿Se parece a un ruido blanco?",
        "Lo mismo para <code>r^2</code>, los rendimientos al cuadrado. ¿Son independientes el rendimiento "
        "de un día y los de los días anteriores?",
        "Baraja los rendimientos con <code>sample(r)</code> y repite los dos recuentos con la serie "
        "barajada. Una frase: qué se conserva al barajar, qué se pierde y qué dice eso sobre dónde estaba "
        "lo que encontraste en (b).",
    ],
    "El cuadrado de un rendimiento mide su tamaño y olvida su signo. Antes de calcular, escribe una "
    "apuesta para cada apartado: cuántas barras esperas fuera de la banda, y por qué. Para contarlas "
    "sirve el código del módulo, cambiando la serie.",
    sol(
        "los rendimientos son, para el correlograma, ruido blanco, y aun así no son independientes.",
        "m2",
        [
            "<strong>(a)</strong> Salen 2 de 24 barras, las de los rezagos 11 y 17, por poco y sin ningún "
            "patrón; en un ruido blanco se espera por azar algo más de una. El rendimiento de un día no "
            "ayuda a predecir, con una relación lineal, el de los siguientes: la serie es incorrelada.",
            "<strong>(b)</strong> En los cuadrados salen 10 de 24, entre ellas las siete primeras "
            "($r_1 = 0.079$, $r_2 = 0.171$, $r_3 = 0.074$, con una banda de $\\pm 0.0455$). A un día de "
            "movimientos grandes tienden a seguirle otros de movimientos grandes, hacia arriba o hacia "
            "abajo: el <em>tamaño</em> del rendimiento sí depende del pasado. Si los rendimientos fueran "
            "independientes, sus cuadrados también lo serían, y no lo son. Es el caso de la advertencia del "
            "módulo, y por eso el recuento de (a) se lee con cautela: sin independencia, la banda ya no "
            "cubre exactamente el 95 %.",
            "<strong>(c)</strong> Barajados, sale 1 barra de 24 en los rendimientos y ninguna en los "
            "cuadrados. Barajar conserva los 1859 valores —su media, su varianza, su histograma— y destruye "
            "solo el orden. La estructura de los cuadrados desaparece con él: no era una rareza de la "
            "distribución de los rendimientos, sino dependencia entre un día y los siguientes.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 3
CORTOS[3] = ejercicio(
    3,
    "<code>discoveries</code> cuenta los grandes inventos y descubrimientos científicos de cada año entre "
    "1860 y 1959. Los diez valores de 1927 a 1936 son 2, 4, 7, 5, 3, 3, 0, 2, 2 y 2. Con papel y lápiz, sin "
    "<code>acf()</code>, entrega:",
    [
        "La media $\\bar y$ y la autocovarianza $\\hat\\gamma_0$.",
        "$\\hat\\gamma_1$ y $\\hat\\gamma_2$ con la fórmula del módulo y, con ellas, $r_1$ y $r_2$. Escribe "
        "los productos que sumas: ¿cuántos son en cada rezago?",
        "Lo que saldría para $r_1$ y $r_2$ si cada suma se dividiera entre el número de productos que "
        "tiene. Comprueba con <code>acf()</code> cuál de las dos versiones calcula R.",
        "La banda para $T = 10$ y una frase: ¿es $r_1$ evidencia de que un año se parece al anterior?",
    ],
    "Empieza por una tabla de tres columnas: el año, $y_t$ y la desviación $y_t - \\bar y$. Todo lo demás "
    "son productos de dos casillas de la tercera columna: para el rezago 1, cada casilla por la de abajo; "
    "para el rezago 2, por la que está dos filas más abajo.",
    sol(
        "$r_1 = 0.471$ y $r_2 = 0.059$, y ninguna de las dos sale de la banda, $\\pm 0.620$.",
        "m3",
        [
            "<strong>(a)</strong> La media es 3 y las desviaciones son $-1, 1, 4, 2, 0, 0, -3, -1, -1, -1$. "
            "Sus cuadrados suman 34, así que $\\hat\\gamma_0 = 34/10 = 3.4$.",
            "<strong>(b)</strong> En el rezago 1 hay nueve productos —$-1, 4, 8, 0, 0, 0, 3, 1, 1$—, que "
            "suman 16: $\\hat\\gamma_1 = 16/10 = 1.6$ y $r_1 = 1.6/3.4 = 0.471$. En el rezago 2 hay ocho "
            "—$-4, 2, 0, 0, 0, 0, 3, 1$—, que suman 2: $\\hat\\gamma_2 = 0.2$ y $r_2 = 0.059$. Cada rezago "
            "pierde un producto, y el divisor sigue siendo $T = 10$.",
            "<strong>(c)</strong> Dividiendo entre el número de productos, $16/9$ y $2/8$, saldrían 0.523 y "
            "0.074. <code>acf()</code> devuelve 0.4706 y 0.0588: usa el divisor $T$. La otra versión es "
            "mayor en un factor $T/(T-k)$ —$10/9$ en el rezago 1, $10/8$ en el 2—, que crece con el rezago: "
            "es el sesgo hacia cero del que habla la nota del módulo, visto desde el otro lado.",
            "<strong>(d)</strong> La banda es $\\pm 1.96/\\sqrt{10} = \\pm 0.620$. Un $r_1$ de 0.471, que en "
            "una serie de 200 datos quedaría muy por fuera de su banda ($\\pm 0.139$), aquí queda dentro: "
            "con diez datos el azar solo puede fabricar una autocorrelación de ese tamaño, y estos diez "
            "años no bastan para decir que un año se parezca al anterior.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 4
CORTOS[4] = ejercicio(
    4,
    "Tres series y la misma tarea. <code>A</code> y <code>B</code> son simuladas, de 200 valores. En "
    "<code>A</code>, cada valor es 0.5 veces el anterior más 0.3 veces el de dos instantes atrás más un "
    "ruido nuevo: <code>set.seed(7); A &lt;- arima.sim(list(ar = c(0.5, 0.3)), n = 200)</code>. En "
    "<code>B</code>, cada valor es un ruido nuevo más 0.8 veces el ruido del instante anterior: "
    "<code>set.seed(3); B &lt;- arima.sim(list(ma = 0.8), n = 200)</code>. La tercera es real: "
    "<code>LakeHuron</code>, el nivel anual del lago Hurón, en pies, de 1875 a 1972. Para cada una, "
    "entrega:",
    [
        "Los rezagos en que la ACF y la PACF salen de la banda (24 rezagos en <code>A</code> y "
        "<code>B</code>, 20 en <code>LakeHuron</code>).",
        "Cuál de las tres líneas de la regla del módulo le corresponde y qué orden, $p$ o $q$, sugiere.",
        "Qué barras de las que salen atribuyes al azar y, en <code>LakeHuron</code>, qué habría que "
        "comprobar antes de dar la lectura por buena.",
    ],
    "Empieza por <code>A</code>, y antes de calcular nada: su receta dice de cuántos valores anteriores "
    "depende cada uno <em>directamente</em>, y la definición del módulo dice qué mide la PACF. Escribe lo "
    "que esperas ver y después compáralo. En las tres, calcula primero la banda: no es la misma con 200 "
    "datos que con 98.",
    sol(
        "<code>A</code>, un AR(2); <code>B</code>, un MA(1); <code>LakeHuron</code>, un AR(2), con una "
        "comprobación pendiente.",
        "m4",
        [
            "<strong><code>A</code>.</strong> La ACF sale de la banda en los seis primeros rezagos y baja "
            "poco a poco. La PACF sale en los rezagos 1 y 2 (0.698 y 0.230) y en el 3 ya está dentro "
            "($-0.032$): se corta tras el rezago 2. Es la primera línea de la regla, un AR(2), que es lo "
            "que anunciaba la receta: cada valor depende directamente de los dos anteriores y de ninguno "
            "más. Las barras 13 y 16 de la PACF son dos de 24, lo que se espera por azar.",
            "<strong><code>B</code>.</strong> Al revés. La ACF tiene una barra grande en el rezago 1 (0.492) "
            "y enseguida nada (0.013, 0.024): se corta. La PACF no se corta: decae alternando el signo "
            "(0.492, $-0.302$, 0.238, $-0.083$, 0.136), con tres barras fuera. Es la segunda línea, un "
            "MA(1). La barra 15 de la ACF, sola y lejos de las demás, es azar.",
            "<strong><code>LakeHuron</code>.</strong> Con 98 datos la banda es $\\pm 0.198$. La PACF sale en "
            "los rezagos 1 y 2 (0.832 y $-0.267$) y en el 3 queda dentro (0.131); la ACF decae (0.832, "
            "0.610, 0.458, 0.371, 0.326). Primera línea otra vez: un AR(2). La barra 10 de la PACF es una de "
            "20. Lo que queda por comprobar es lo que el módulo pide antes de leer un modelo en una PACF: "
            "que la serie sea estacionaria. Su ACF sale de la banda en los nueve primeros rezagos, tres más "
            "que la de <code>A</code>, y decidir si eso es memoria o una serie que no vuelve a su nivel es "
            "la pregunta de los Módulos 5 y 6.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 5
CORTOS[5] = ejercicio(
    5,
    "Dos series de 200 valores que suben, en promedio, 0.2 por periodo, hechas con el mismo ruido: tras "
    "<code>set.seed(37); e &lt;- rnorm(200); t &lt;- 1:200</code>, la serie <code>A &lt;- 0.2 * t + e</code> es "
    "una recta con ruido y <code>B &lt;- cumsum(0.2 + e)</code>, una caminata con deriva. Aplica a cada una "
    "los dos tratamientos del módulo —restarle la recta ajustada, <code>residuals(lm(A ~ t))</code>, y "
    "diferenciarla, <code>diff(A)</code>— y entrega:",
    [
        "Una tabla de cuatro filas, cada serie con cada tratamiento, con $r_1$ y el número de barras, de 24, "
        "que salen de la banda.",
        "Qué tratamiento le corresponde a cada serie y qué huella deja el equivocado en cada caso.",
        "Para <code>B</code>, lo que sube por periodo, estimado de dos maneras: con la pendiente de su "
        "recta ajustada y con la media de sus diferencias. Y, para las dos, lo más lejos que llegan de la "
        "recta $0.2\\,t$. ¿Cuál de las dos vuelve a su recta?",
    ],
    "Antes de calcular, escribe qué queda, en ecuaciones, al diferenciar $a + bt + \\varepsilon_t$ y al "
    "restarle una recta a $y_0 + ct + \\sum \\varepsilon_i$. La tabla del apartado (a) debería parecerse a lo "
    "que escribiste.",
    sol(
        "a <code>A</code> se le resta la recta y <code>B</code> se diferencia; cada tratamiento equivocado "
        "deja su firma.",
        "m5",
        [
            "<strong>(a) y (b)</strong> Con el tratamiento que le corresponde, a cada serie le queda el "
            "ruido: $r_1 = -0.014$ y ninguna barra fuera de la banda, en las dos. El número coincide porque "
            "lo que queda es, en los dos casos, prácticamente el mismo $\\varepsilon_t$. Con el equivocado:",
            "<code>A</code> diferenciada queda estacionaria, pero con $r_1 = -0.517$: es "
            "$\\nabla y_t = b + \\varepsilon_t - \\varepsilon_{t-1}$, y dos valores seguidos comparten un "
            "ruido con el signo cambiado. Esa autocorrelación no estaba en los datos; la fabricó la "
            "diferencia. <code>B</code> sin su recta sigue con $r_1 = 0.959$ y 21 de 24 barras fuera: "
            "restar $ct$ no toca la suma $\\sum\\varepsilon_i$, y el residuo sigue siendo una caminata.",
            "<strong>(c)</strong> La pendiente de la recta ajustada a <code>B</code> da 0.235 y la media de "
            "sus cambios, 0.205: las dos estiman la deriva, 0.2, y ninguna la acierta del todo. "
            "<code>A</code> no se aleja nunca más de 2.7 de la recta $0.2\\,t$; <code>B</code> llega a "
            "estar a 12.0. La que vuelve es <code>A</code>: su distancia a la recta es un ruido de varianza "
            "fija. La de <code>B</code> es una caminata, y su varianza crece con $t$.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 6
CORTOS[6] = ejercicio(
    6,
    "<code>nhtemp</code> es la temperatura media anual de New Haven (Connecticut), en grados Fahrenheit, de "
    "1912 a 1971: 60 años, sin estacionalidad porque el dato es anual. La serie sube; hay que decidir si esa "
    "tendencia es estocástica o determinista. Entrega:",
    [
        "<code>adf.test()</code> y <code>kpss.test()</code> tal como vienen: estadístico, p-valor y la fila "
        "de la tabla del módulo en que cae la pareja.",
        "Esas dos pruebas no contrastan lo mismo. Di cuál de las dos variantes del KPSS corresponde a la "
        "regresión que estima <code>adf.test()</code>, córrela y di en qué fila cae ahora la pareja.",
        "El p-valor del ADF con $k = 1, 2, 3, 4$ y $5$. ¿Depende la decisión al 5 % del número de términos?",
        "El veredicto en dos frases: qué se puede afirmar con estos 60 datos y qué no. Para desempatar, "
        "calcula $r_1$ después de cada uno de los dos tratamientos del Módulo 5.",
    ],
    "Antes de interpretar una salida, escribe la $H_0$ de esa prueba y qué deja oscilar a la serie "
    "alrededor de qué: de una constante o de una recta. Dos pruebas solo se pueden comparar si admiten lo "
    "mismo.",
    sol(
        "con la especificación emparejada ninguna de las dos pruebas rechaza, y el correlograma inclina la "
        "decisión hacia una recta con ruido.",
        "m6",
        [
            "<strong>(a)</strong> El ADF da $-3.277$ con $p = 0.084$: no rechaza la raíz unitaria al 5 %. El "
            "KPSS de nivel da 0.883 con $p &lt; 0.01$: rechaza la estacionariedad. Es la segunda fila de la "
            "tabla, «no estacionaria: hay que diferenciar».",
            "<strong>(b)</strong> La regresión de <code>adf.test()</code> lleva tendencia, así que el KPSS "
            "que le corresponde es el de tendencia, y ese da 0.094 con $p &gt; 0.10$: no rechaza. La pareja "
            "pasa a la tercera fila, la de los datos poco informativos. Lo que el KPSS de nivel rechazaba "
            "era que la serie oscile alrededor de una constante, y no lo hace, porque sube; que oscile "
            "alrededor de una recta, no lo rechaza.",
            "<strong>(c)</strong> Los p-valores son $&lt; 0.01$, 0.045, 0.084, 0.053 y 0.370. Con uno o dos "
            "términos el ADF rechaza la raíz unitaria al 5 %; con tres —el valor por defecto—, cuatro o "
            "cinco, no. La decisión depende de $k$, y esa es otra forma de decir que 60 datos informan "
            "poco.",
            "<strong>(d)</strong> Lo que se puede afirmar: los datos son compatibles con una recta más un "
            "ruido estacionario, y el correlograma apunta hacia ahí. Restada la recta queda $r_1 = 0.107$, "
            "dentro de la banda $\\pm 0.253$; diferenciada, $r_1 = -0.526$, la huella del $-0.5$ que deja "
            "diferenciar una recta con ruido (Módulo 5). Lo que no se puede afirmar es que la raíz unitaria "
            "esté descartada: el ADF, con su $k$ por defecto, no llega a rechazarla. Con esta "
            "evidencia, lo razonable es tratar la tendencia como determinista —restar la recta— y dejar "
            "dicho con qué especificación se decidió y que el ADF no fue concluyente.",
        ],
    ),
)

# ---------------------------------------------------------------- Módulo 8
CORTOS[8] = ejercicio(
    8,
    "<code>JohnsonJohnson</code> son las ganancias trimestrales por acción de Johnson &amp; Johnson, en "
    "dólares, de 1960 a 1980: 84 trimestres, con $m = 4$, en una serie cuyo máximo es casi 37 veces su "
    "mínimo. Entrega:",
    [
        "Una función que calcule el criterio de Guerrero con la receta del módulo, dada la serie y "
        "$\\lambda$. Compruébala con <code>AirPassengers</code>: debe devolver 0.530, 0.153 y 0.081 para "
        "$\\lambda = 1$, $0$ y $-0.2947$.",
        "Para <code>JohnsonJohnson</code>: el $\\lambda$ de <code>BoxCox.lambda()</code>; el criterio sin "
        "transformar, con la raíz cuadrada, con el logaritmo y en el óptimo; y qué parte de la mejora "
        "alcanzable capta el logaritmo. ¿Con qué transformación te quedas?",
        "Deshacer. Un modelo ajustado a $\\log y_t$ pronostica $w = 2.75$ para el trimestre siguiente, con "
        "un error normal de desviación 0.20. Da en dólares el pronóstico y los extremos del intervalo "
        "$w \\pm 2 \\times 0.20$; después simula 100 000 valores de $w$, deshaz cada uno y compara su media "
        "con su mediana. Una frase: ¿qué es $\\exp(2.75)$?",
    ],
    "En el apartado (a), una matriz con una columna por año deja el resto en dos llamadas, una para las "
    "medias de las columnas y otra para sus desviaciones. En el (c), deshaz primero los dos extremos del "
    "intervalo y mide a qué distancia queda cada uno del centro.",
    sol(
        "el logaritmo; y $\\exp(2.75) = 15.64$ dólares es la mediana del pronóstico, no su media.",
        "m8",
        [
            "<strong>(a)</strong> La función reproduce las tres cifras del módulo: 0.530, 0.153 y 0.081.",
            "<strong>(b)</strong> El criterio de Guerrero elige $\\lambda = 0.154$. El criterio vale 1.081 "
            "sin transformar, 0.575 con la raíz cuadrada, 0.402 con el logaritmo y 0.344 en el óptimo. "
            "Aquí transformar importa —el logaritmo deja el criterio en poco más de un tercio— y el "
            "logaritmo capta el 92.1 % de la mejora alcanzable, más que en <code>AirPassengers</code> "
            "(84 %). Con el óptimo tan cerca de 0, la elección es el logaritmo: casi igual de bueno y se "
            "puede interpretar.",
            "<strong>(c)</strong> El pronóstico es $\\exp(2.75) = 15.64$ dólares y el intervalo va de 10.49 "
            "a 23.34: 5.15 por debajo y 7.70 por encima. Lo que en logaritmos era simétrico, en dólares no "
            "lo es. En la simulación, la mediana de los valores deshechos es 15.66 —$\\exp(2.75)$, salvo el "
            "azar de la simulación— y su media, 15.97, unos 33 centavos más. Deshacer con "
            "<code>exp()</code> devuelve la mediana del pronóstico; la media queda por encima, y tanto más "
            "cuanto mayor sea la dispersión del error. Es el sesgo del aviso del módulo.",
        ],
    ),
)


def aplica(src):
    """Inserta cada ejercicio al final de su módulo, justo antes de la lista de fuentes."""
    for mid, bloque in CORTOS.items():
        ini = src.index(f'<template id="module-{mid}">')
        fin = src.index("</template>", ini)
        ancla = '      <aside class="fuentes-modulo"'
        pos = src.rindex(ancla, ini, fin)
        assert src.count(ancla, ini, fin) == 1, mid
        src = src[:pos] + bloque + src[pos:]
    return src
