#!/usr/bin/env python3
"""R5 del capítulo 4 · T5.1: los nueve ejercicios cortos «Para practicar» (D9), uno por módulo del 1 al 9.

No se ejecuta solo: lo importa `r5_edita.py`. El código de cada solución NO está escrito aquí:
se lee de `r5_bloques/<id>.out`, que es la salida de `r5_reprex.R` sobre `r5_bloques/<id>.R`,
con cada resultado real bajo su línea tras `#> `. Las cifras de la prosa que no salen bajo un
`#>` están en `r5_cifras.out`, con la etiqueta que se anota junto a cada ejercicio.

Cada ejercicio se inserta justo antes de la lista de fuentes de su módulo
(`<aside class="fuentes-modulo"`), como en los capítulos 2 y 3.
"""
import html
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ASIDE = '      <aside class="fuentes-modulo" aria-label="Fuentes citadas en este módulo">'


def codigo(nombre):
    """El bloque ejecutado, escapado como el resto del capítulo (`<`, `>` y `&`)."""
    t = (AQUI / "r5_bloques" / f"{nombre}.out").read_text(encoding="utf-8")
    t = "\n".join(l.rstrip() for l in t.rstrip("\n").splitlines())
    return html.escape(t, quote=False)


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
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c4m{mid}-pista">
              <i class="fas fa-lightbulb" aria-hidden="true"></i> Pista <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
            <button type="button" class="ejercicio-boton" aria-expanded="false" aria-controls="c4m{mid}-sol">
              <i class="fas fa-key" aria-hidden="true"></i> Solución <i class="fas fa-chevron-down" aria-hidden="true"></i>
            </button>
          </div>
          <div class="ejercicio-panel pista" id="c4m{mid}-pista" hidden>
            <p style="margin:0;">{pista}</p>
          </div>
          <div class="ejercicio-panel solucion" id="c4m{mid}-sol" hidden>
{solucion}
          </div>
        </div>
      </div>

'''


def sol(respuesta, bloque, parrafos):
    """Respuesta en negrita, el bloque de R ejecutado y la lectura por apartados."""
    p = [f"            <p><strong>Respuesta: {respuesta}</strong></p>",
         f'            <pre><code class="language-r">{codigo(bloque)}</code></pre>']
    for i, t in enumerate(parrafos):
        estilo = ' style="margin-bottom:0;"' if i == len(parrafos) - 1 else ""
        p.append(f"            <p{estilo}>{t}</p>")
    return "\n".join(p)


# --------------------------------------------------------------------------- M1 · tcm1y
M1 = ejercicio(
    1,
    r'''<code>tcm1y</code>, del paquete <code>tseries</code> (se carga con <code>data(tcm)</code>), es el rendimiento mensual a un año de los títulos del Tesoro de Estados Unidos: 558 datos, de abril de 1953 a septiembre de 1999. Ajústale dos modelos, sin diferenciarla antes, y entrega:''',
    [r'''Un AR(2) con media: la suma $\hat\phi_1 + \hat\phi_2$ y el módulo de sus dos raíces.''',
     r'''Un ARIMA($1,1,0$), escrito como AR(2) sobre $y_t$ con el desarrollo del módulo: $\phi_1^{*}$ y $\phi_2^{*}$, su suma y el módulo de sus raíces.''',
     r'''El pronóstico de cada modelo a 1, 5 y 10 años, con su error estándar. ¿En qué se nota que uno estima la raíz y el otro la impone?'''],
    r'''Para (b), una vez ajustado el ARIMA($1,1,0$), no hace falta nada más: el desarrollo paso a paso del módulo dice cómo pasar de $\phi$ a $(\phi_1^{*},\ \phi_2^{*})$. Para (c), <code>predict()</code> devuelve el pronóstico y su error estándar; mira hacia dónde va cada uno al alejarse.''',
    sol(r'''los dos modelos son un AR(2) sobre $y_t$ con coeficientes casi iguales. La diferencia está en una raíz: el AR(2) la estima en $1.028$ y el ARIMA($1,1,0$) la fija en $1$, y de eso depende todo el pronóstico a largo plazo.''',
        "m1",
        [r'''<strong>(a)</strong> El AR(2) da $(1.3429,\ -0.3599)$: suman $0.9830$, y las raíces tienen módulo $1.0278$ y $2.7033$. Es estacionario por poco: una raíz queda a menos de tres centésimas del círculo unitario.''',
         r'''<strong>(b)</strong> El ARIMA($1,1,0$) da $\hat\phi = 0.3518$, así que sobre $y_t$ es el AR(2) con $\phi_1^{*} = 1.3518$ y $\phi_2^{*} = -0.3518$: suman $1$ exactamente, y sus raíces tienen módulo $1$ y $2.8423$ (que es $1/\hat\phi$). Los coeficientes se parecen a los de (a); lo que cambia es que aquí la suma no se estima: la fija el factor $(1-B)$.''',
         r'''<strong>(c)</strong> El AR(2) vuelve a su media, $5.81$: pronostica $5.42$, $5.70$ y $5.79$, y su error estándar se estabiliza cerca de la desviación típica de la serie ($2.95$ a diez años, frente a $2.98$). El ARIMA($1,1,0$) se queda en $5.28$, junto al último dato ($5.25$), y su error estándar no deja de crecer: $2.24$, $5.18$ y $7.36$. Una raíz en $1.028$ o en $1$ apenas cambia el ajuste y cambia por completo lo que el modelo dice del futuro lejano. Por eso el módulo llama a $d$ una decisión: el Módulo 3 enseña a tomarla, y el Módulo 9, de dónde salen esos errores estándar.''']))

# --------------------------------------------------------------------------- M2 · simulada
M2 = ejercicio(
    2,
    r'''Una serie simulada, para practicar las vueltas atrás sabiendo cuál es el modelo: <code>set.seed(2026); y &lt;- arima.sim(n = 200, model = list(order = c(2, 1, 0), ar = c(0.4, 0.3)))</code>. Ajústale, por máxima verosimilitud, tres modelos mal elegidos a propósito —un ARIMA($0,1,1$), un ARIMA($2,2,1$) y un ARIMA($2,1,2$)— y, con el ciclo del módulo delante, entrega:''',
    [r'''Para cada ajuste, el hallazgo que lo invalida y la etapa en la que aparece.''',
     r'''A qué etapa devuelve cada hallazgo y qué se cambia al volver.''',
     r'''El modelo al que llevan los tres hallazgos, con su diagnóstico.'''],
    r'''Los tres hallazgos están en los paneles «Qué te devuelve atrás» de las etapas 2 y 3. De cada ajuste mira tres cosas: los errores estándar de los coeficientes, el módulo de las raíces del MA y Ljung–Box.''',
    sol(r'''el primero falla en el diagnóstico (le falta orden); el segundo, en la estimación (le sobra una diferencia); el tercero, también en la estimación (le sobran parámetros). Los tres devuelven a la etapa 1, y los tres cambios llevan al ARIMA($2,1,0$).''',
        "m2",
        [r'''<strong>(a)</strong> ARIMA($0,1,1$): Ljung–Box(20) da $p &lt; 0.0001$; los residuales tienen estructura, y eso se ve en la etapa 3. ARIMA($2,2,1$): pasa Ljung–Box ($p = 0.70$), pero $\hat\theta = -1.000$ y la raíz MA tiene módulo $1.0000$; es un hallazgo de la etapa 2, al comprobar las raíces. ARIMA($2,1,2$): también pasa Ljung–Box ($p = 0.44$) y sus raíces están lejos del círculo, pero los errores estándar de sus coeficientes van de $0.20$ a $0.32$, entre tres y cinco veces los del ARIMA($2,1,0$) ($0.065$): sobreparametrización, etapa 2.''',
         r'''<strong>(b)</strong> Los tres devuelven a la identificación. El primero, a proponer más orden: la PACF de $\nabla y_t$ sale de la banda ($\pm 0.139$) en los rezagos 1 y 2 ($0.542$ y $0.372$) y no después, la firma de un AR(2). El segundo, a bajar $d$: una raíz MA sobre el círculo es el modelo deshaciendo una diferencia que sobra. El tercero, a quitar parámetros.''',
         r'''<strong>(c)</strong> El ARIMA($2,1,0$): $\hat\phi = (0.343,\ 0.382)$, con errores estándar de $0.065$ (los verdaderos son $0.4$ y $0.3$), y Ljung–Box(20) $p = 0.71$. Nótese que el ARIMA($2,2,1$) y el ARIMA($2,1,2$) pasaban Ljung–Box: un modelo puede dejar los residuales en orden y estar mal especificado, y por eso la etapa 2 no se limita a estimar. La semilla está elegida para que se vean los cinco rasgos a la vez. En 200 series generadas igual (semillas 1 a 200), Ljung–Box rechaza el ARIMA($0,1,1$) en el $99.5\,\%$; pero el ARIMA($2,2,1$) solo deja la raíz MA sobre el círculo en el $65.5\,\%$, y los cinco rasgos coinciden en el $53\,\%$.''']))

# --------------------------------------------------------------------------- M3 · simulada con escalón
M3 = ejercicio(
    3,
    r'''Una serie con un cambio de nivel y sin raíz unitaria, para practicar la decisión conociendo la respuesta: <code>set.seed(43); y &lt;- ts(10 + 3 * (1:120 &gt;= 71) + arima.sim(n = 120, model = list(ar = 0.5)))</code>. Son 120 datos de un AR(1) con $\phi = 0.5$ alrededor de un nivel que pasa de $10$ a $13$ en $t = 71$. Trátala como una serie cualquiera y entrega:''',
    [r'''El $d$ que pide <code>ndiffs()</code> con cada una de las tres pruebas, sobre la serie completa.''',
     r'''Lo mismo en cada tramo, antes y después de $t = 71$.''',
     r'''El ARIMA($1,1,1$) al que lleva seguir a KPSS, con su $\hat\theta$ y el módulo de su raíz MA; y el modelo de dos medias con un AR(1), con su escalón y su diagnóstico. ¿Qué $d$ eliges, y con cuáles de las tres evidencias del módulo?'''],
    r'''Empieza por el gráfico, <code>plot(y)</code>. Lo que se vea ahí dice qué comprobar después con las pruebas y dónde partir la serie.''',
    sol(r'''$d = 0$, con el escalón dentro del modelo. KPSS pide $d = 1$ sobre la serie completa y $d = 0$ en cada tramo: lo que rechazaba era el cambio de nivel.''',
        "m3",
        [r'''<strong>(a)</strong> KPSS pide $d = 1$; ADF y PP, $d = 0$. Es el mismo reparto que en el Nilo.''',
         r'''<strong>(b)</strong> En cada tramo, las tres pruebas piden $d = 0$. Las medias son $10.14$ y $13.31$: a cada lado del salto la serie vuelve a su nivel, y KPSS rechazaba porque no hay un nivel único.''',
         r'''<strong>(c)</strong> El ARIMA($1,1,1$) da $\hat\phi = 0.488$ y $\hat\theta = -0.858$, con la raíz MA en $1.165$: cerca del círculo, el síntoma de haber diferenciado de más (en el Nilo, $1.144$). El modelo de dos medias con AR(1) estima el escalón en $3.12$ (e.e. $0.33$) y $\hat\phi = 0.473$ (e.e. $0.080$) —los verdaderos son $3$ y $0.5$— y pasa Ljung–Box(20) con $p = 0.68$. Las tres evidencias coinciden una vez que se mira el gráfico: el salto se ve, las pruebas dejan de pedir la diferencia cuando se aplican a cada lado, y el modelo diferenciado tiene la raíz MA cerca de $1$.''',
         r'''La semilla está elegida para que salga el caso completo. En 500 series generadas igual (semillas 1 a 500), KPSS pide diferenciar la serie completa en todas, y en el $65\,\%$ pide $d = 0$ en los dos tramos; el reparto del Nilo (ADF y PP en $d = 0$) sale en el $52\,\%$, y con las tres pruebas en $d = 0$ en cada tramo, en el $33\,\%$. La raíz MA del ARIMA($1,1,1$) tiene mediana $1.15$.''']))

# --------------------------------------------------------------------------- M4 · importaciones de Colombia
M4 = ejercicio(
    4,
    r'''<code>global_economy</code>, del paquete <code>tsibbledata</code>, reúne indicadores anuales del Banco Mundial por país, de 1960 a 2017. Toma las importaciones de bienes y servicios de Colombia, en porcentaje del PIB (58 datos). Las tres pruebas piden $d = 1$, así que la identificación se hace sobre $\nabla y_t$. Entrega:''',
    [r'''La ACF y la PACF de $\nabla y_t$ hasta el rezago 10, con su banda: ¿corta alguna?, ¿decae alguna?''',
     r'''Los candidatos que llevarías a la estimación, y por qué más de uno.''',
     r'''El AICc, el BIC y Ljung–Box(20) de cada candidato. ¿Los separan?'''],
    r'''Con 57 diferencias la banda es ancha. Antes de decidir si una función «decae», cuenta cuántas de sus barras salen de verdad de la banda, y piensa qué enseñarían un AR(1) y un MA(1) cuando su único coeficiente es pequeño.''',
    sol(r'''la tabla no elige. La ACF y la PACF de $\nabla y_t$ tienen una sola barra clara, la del rezago 1, y eso lo producen igual un MA(1) y un AR(1). Se llevan los dos, y el AICc los deja a $0.03$ puntos.''',
        "m4",
        [r'''<strong>(a)</strong> La banda es $\pm 0.260$. En la ACF solo sale el rezago 1 ($-0.288$), y por poco; en la PACF, el rezago 1 ($-0.288$) y, aislado, el 7 ($-0.297$). Ninguna de las dos decae a la vista: las dos «cortan en 1».''',
         r'''<strong>(b)</strong> Con una sola barra de $-0.29$, la tabla no distingue. Un MA(1) con $\theta = -0.29$ tiene una PACF que decae, pero su segundo valor es $-0.08$, dentro de la banda; un AR(1) con $\phi = -0.29$ tiene una ACF que decae, y su segundo valor es $0.08$, también dentro. Los dos son compatibles con lo que se ve. Se proponen el ARIMA($0,1,1$) y el ARIMA($1,1,0$), su vecino ARIMA($1,1,1$) y, como la barra apenas asoma, la caminata aleatoria, ARIMA($0,1,0$).''',
         r'''<strong>(c)</strong> El ARIMA($0,1,1$) ($\hat\theta = -0.291$) y el ARIMA($1,1,0$) ($\hat\phi = -0.285$) tienen AICc $222.505$ y $222.530$: $0.03$ puntos. El ARIMA($1,1,1$) queda a $2.14$, y sus dos coeficientes tienen errores estándar de $0.45$, mayores que ellos: sobra un parámetro. La caminata aleatoria queda a $2.69$ por AICc y, por BIC, es la tercera, a $0.79$ puntos. Los cuatro pasan Ljung–Box(20). Con 58 datos, lo que se puede afirmar es que hay dos modelos de un parámetro que los datos no separan.''']))

# --------------------------------------------------------------------------- M5 · airmiles
M5 = ejercicio(
    5,
    r'''<code>airmiles</code> trae las millas-pasajero de pago voladas cada año por las aerolíneas comerciales de Estados Unidos, de 1937 a 1960 (24 datos). Crece tan deprisa que conviene trabajar con su logaritmo, <code>y &lt;- log(airmiles)</code> (Capítulo 2). Con un ARIMA($0,1,1$), entrega:''',
    [r'''La media de las diferencias, calculada de dos maneras: con <code>mean(diff(y))</code> y solo con el primer dato y el último.''',
     r'''La deriva estimada, su error estándar y su estadístico $t$, y el AICc del modelo con deriva y sin ella. ¿Lleva deriva?''',
     r'''El pronóstico a 1, 5 y 10 años de los dos modelos. ¿Qué afirma la deriva sobre el futuro, en la escala original?'''],
    r'''En <code>forecast::Arima</code> la deriva se pide con <code>include.drift = TRUE</code>. Para (c), recuerda que la serie está en logaritmos: una pendiente constante en el logaritmo es un factor constante en la serie original.''',
    sol(r'''sí lleva deriva: $\hat\delta = 0.182$ con $t = 4.47$, y el AICc baja de $-11.13$ a $-20.89$. Es el caso contrario al del Nilo.''',
        "m5",
        [r'''<strong>(a)</strong> Las dos cuentas dan $0.1872$: la suma de las diferencias es telescópica y queda $(y_{1960} - y_{1937})/23$.''',
         r'''<strong>(b)</strong> $\hat\delta = 0.1818$ (e.e. $0.0407$), $t = 4.47$: claramente distinta de cero. El AICc pasa de $-11.13$ sin deriva a $-20.89$ con ella, casi diez puntos menos, y los dos modelos tienen el mismo $d$, así que la comparación vale. La deriva estimada ($0.182$) no es exactamente la media de las diferencias ($0.187$), porque se estima a la vez que $\theta$ y no como un promedio simple; se parecen, como cabe esperar.''',
         r'''<strong>(c)</strong> Sin deriva el pronóstico es plano, $10.227$ a cualquier horizonte (no en el último dato, $10.326$). Con deriva es una recta: $10.422$, $11.149$ y $12.059$. En la escala original, una pendiente de $0.182$ por año en el logaritmo equivale a multiplicar por $e^{0.182} = 1.20$ cada año, y por $6.2$ en diez. Dentro de la muestra esa tendencia está bien medida; lo que el modelo añade es que seguirá igual sin límite, y esa es la afirmación sobre el futuro contra la que previene el módulo.''']))

# --------------------------------------------------------------------------- M6 · GOOG 2018
M6 = ejercicio(
    6,
    r'''<code>gafa_stock</code>, del paquete <code>tsibbledata</code>, trae los precios diarios de cuatro acciones entre 2014 y 2018. Toma el precio de cierre de Google (<code>Symbol == "GOOG"</code>) en 2018: 251 días de mercado, en dólares. Las tres pruebas piden $d = 1$. Ajusta la rejilla con $p, q \in \{0,1,2\}$ para $d = 1$ y para $d = 2$, por máxima verosimilitud, y entrega:''',
    [r'''El mejor modelo por AICc de cada $d$.''',
     r'''El mínimo de los 18: ¿en qué $d$ cae? ¿Es razón para elegir ese $d$?''',
     r'''El coeficiente y la raíz MA del mejor modelo con $d = 2$, y su $\hat\sigma^2$ frente a $\operatorname{Var}(\nabla y)$. ¿Qué modelo es en realidad?'''],
    r'''Dos preguntas antes de elegir: ¿sobre qué datos se calcula cada AICc?, y ¿qué raíces tiene el modelo que gana?''',
    sol(r'''el mínimo de la rejilla está en $d = 2$, y no vale: se calcula sobre otros datos, y el modelo que lo alcanza es una caminata aleatoria con deriva escrita con una diferencia de más.''',
        "m6",
        [r'''<strong>(a)</strong> Con $d = 1$ gana el ARIMA($0,1,0$), con AICc $2190.69$; con $d = 2$, el ARIMA($0,2,1$), con $2190.48$.''',
         r'''<strong>(b)</strong> El mínimo de los 18 es el ARIMA($0,2,1$), por $0.21$ puntos. No es razón para elegir $d = 2$: el primero se calcula sobre $250$ diferencias y el segundo sobre $249$ segundas diferencias, y un AICc solo se compara con otro calculado sobre los mismos datos. Las pruebas, que sí hablan de $d$, piden una diferencia.''',
         r'''<strong>(c)</strong> $\hat\theta = -1.000$, y la raíz MA tiene módulo $1.000$: el factor $(1 - B)$ del MA cancela una de las dos diferencias. Su $\hat\sigma^2 = 372.71$ coincide con la varianza de $\nabla y$ alrededor de su media: el ARIMA($0,2,1$) es una caminata aleatoria con deriva —la constante la pone la diferencia que el MA deshace— y no la caminata sin ella, cuya $\hat\sigma^2$ es $371.23$. La rejilla ha premiado, por dos décimas, un modelo degenerado. Y dentro de $d = 1$ el resultado también dice algo: gana la caminata aleatoria, y los otros ocho modelos quedan entre $1.0$ y $3.1$ puntos por encima de ella. Es el resultado «no hay señal» que el Módulo 10 encontrará en la TRM.''']))

# --------------------------------------------------------------------------- M7 · NelPlo ip
M7 = ejercicio(
    7,
    r'''<code>NelPlo</code>, del paquete <code>tseries</code> (se carga con <code>data(NelPlo)</code>), reúne catorce series macroeconómicas que terminan en 1988. Toma la de producción industrial, <code>na.omit(NelPlo[, "ip"])</code>: 129 datos anuales, desde 1860, en la escala que trae el paquete (la ayuda no da unidades; sus valores van de $-0.105$ a $5.229$). Entrega:''',
    [r'''El modelo que devuelve <code>auto.arima()</code> con sus opciones por defecto, y cuántos modelos evaluó.''',
     r'''Lo mismo con <code>stepwise = FALSE, approximation = FALSE</code>. ¿Coinciden?''',
     r'''Ljung–Box(20) de los dos ganadores, y una explicación de por qué la búsqueda escalonada se detuvo donde se detuvo.'''],
    r'''Pide <code>trace = TRUE</code> en las dos llamadas y sigue la escalonada modelo a modelo: ¿de dónde partió, qué probó después y cuál de esos modelos mejoraba al de partida?''',
    sol(r'''no coinciden. La escalonada se queda en la caminata aleatoria con deriva tras evaluar 6 modelos; la exhaustiva evalúa 42 y encuentra un ARIMA($0,1,5$) con deriva, $6.1$ puntos mejor por AICc, que además es el único de los dos que pasa Ljung–Box.''',
        "m7",
        [r'''<strong>(a)</strong> <code>auto.arima(ip)</code> devuelve un ARIMA($0,1,0$) con deriva, AICc $-233.72$, después de evaluar 6 modelos (uno de ellos, el ARIMA($2,1,2$) con deriva, descartado con AICc $= \infty$).''',
         r'''<strong>(b)</strong> La exhaustiva evalúa 42 y devuelve un ARIMA($0,1,5$) con deriva, AICc $-239.82$: $6.10$ puntos menos. El segundo de su lista, un ARIMA($5,1,0$) con deriva, también mejora al de la escalonada.''',
         r'''<strong>(c)</strong> El ganador de la escalonada no pasa Ljung–Box(20) ($p = 0.047$); el de la exhaustiva, sí ($p = 0.73$). La escalonada no falló por descuido. De sus cinco modelos iniciales, el mejor fue el ARIMA($0,1,0$) con deriva; después solo evaluó uno más, el ARIMA($1,1,1$) con deriva, que no lo mejoraba, y paró, como manda su regla. Lo que le falta a ese modelo está en el rezago 5 ($\hat\theta_5 = -0.360$, con error estándar $0.094$), y por el camino no hay nada que ganar: los ARIMA($0,1,q$) con deriva de $q = 1$ a $4$ tienen todos peor AICc que el de partida. Es el límite que avisa el módulo: la búsqueda escalonada explora un vecindario, y aquí la mejora estaba fuera de él. Lo delataba el diagnóstico.''']))

# --------------------------------------------------------------------------- M8 · simulada, AR(1) diferenciado
M8 = ejercicio(
    8,
    r'''Una serie estacionaria, diferenciada sin necesidad: <code>set.seed(2026); y &lt;- arima.sim(n = 200, model = list(ar = 0.8))</code>. No le falta ninguna diferencia. Trabaja con $d = 1$ como si no se supiera y entrega:''',
    [r'''El $\hat\rho_1$ de $\nabla y_t$. ¿Avisa de que la diferencia sobra?''',
     r'''El ARIMA($0,1,1$) y el ARIMA($1,1,1$), por máxima verosimilitud: coeficientes, módulo de la raíz MA y Ljung–Box(20). ¿Cuál de los dos muestra la firma de la sobrediferenciación?''',
     r'''La explicación algebraica: escribe el modelo que sigue $\nabla y_t$ a partir del AR(1).'''],
    r'''Para (c), aplica $(1 - B)$ a los dos lados de $(1 - \phi B)\,y_t = \varepsilon_t$ y mira qué polinomio queda del lado de los choques. Después vuelve a (b) y pregúntate cuál de los dos modelos tiene sitio para lo que queda del otro lado.''',
    sol(r'''la firma aparece solo en el ARIMA($1,1,1$): $\hat\theta = -1.000$ y raíz MA de módulo $1.000$. El ARIMA($0,1,1$) pasa el diagnóstico sin ninguna señal, y el $\hat\rho_1$ tampoco avisa.''',
        "m8",
        [r'''<strong>(a)</strong> $\hat\rho_1 = -0.185$, lejos de $-0.5$. No avisa, y no es mala suerte: para un AR(1) diferenciado el valor teórico es $-(1-\phi)/2 = -0.10$. Es el indicio fallando en uno de sus dos sentidos (Módulo 2.7).''',
         r'''<strong>(b)</strong> ARIMA($0,1,1$): $\hat\theta = -0.201$, raíz MA en $4.98$, Ljung–Box(20) $p = 0.56$. Es un modelo con una diferencia de más que pasa el diagnóstico. ARIMA($1,1,1$): $\hat\phi = 0.809$ y $\hat\theta = -1.000$, con la raíz MA de módulo $1.000$ ($p = 0.68$). Ahí está la firma.''',
         r'''<strong>(c)</strong> $(1 - \phi B)\,\nabla y_t = (1 - B)\,\varepsilon_t$: la serie diferenciada es un ARMA($1,1$) con el mismo $\phi$ y $\theta = -1$. El ARIMA($1,1,1$) tiene sitio para las dos partes, y por eso las encuentra: su $\hat\phi = 0.809$ es casi el del AR(1) ajustado sin diferenciar ($0.800$). Al ARIMA($0,1,1$) le falta la parte AR, y su único coeficiente se reparte entre imitarla y deshacer la diferencia: no llega a $-1$. Aquí, la raíz MA solo delató la diferencia sobrante en el modelo que tenía sitio para la parte AR. No siempre sale tan limpio: en 200 series generadas igual (semillas 1 a 200), la raíz MA del ARIMA($1,1,1$) queda por debajo de $1.05$ en el $78\,\%$.''']))

# --------------------------------------------------------------------------- M9 · austres (tras la verificación)
M9 = ejercicio(
    9,
    r'''<code>austres</code> es el número de residentes en Australia, en miles, medido cada trimestre desde 1971: 89 datos. Ajústale con <code>Arima()</code> tres modelos con la misma parte MA(1) y distinto $d$ o distinta constante —A, un ARIMA($0,1,1$) sin deriva; B, un ARIMA($0,1,1$) con deriva; C, un ARIMA($0,2,1$)— y entrega:''',
    [r'''El pronóstico puntual de cada uno a 1, 20 y 40 trimestres. ¿Qué forma tiene cada pronóstico?''',
     r'''La pendiente a la que llega cada pronóstico. ¿De dónde saca la suya el modelo B, y de dónde el C?''',
     r'''El ancho del intervalo del $95\,\%$ a 1 y a 40 trimestres, en los tres. ¿Cuál crece más deprisa, y qué lo decide?'''],
    r'''La tabla del módulo dice qué forma corresponde a cada combinación de $d$ y constante. Para (b), compara cada pendiente con la media de todas las diferencias de la serie y con la de las últimas.''',
    sol(r'''A se aplana; B y C son rectas, y no la misma. B avanza con la pendiente media de toda la muestra ($52.1$ por trimestre) y C, con la del final de la serie ($43.2$). El intervalo de C es el que más se abre: a 40 trimestres es $6.4$ veces el de B.''',
        "m9",
        [r'''<strong>(a)</strong> A se queda en $17\,664.8$ a cualquier horizonte, junto al último dato ($17\,661.5$): con $d = 1$ y sin deriva, el pronóstico se aplana. B y C suben en línea recta: a 40 trimestres B llega a $19\,735.7$ y C, a $19\,390.7$, $345$ menos.''',
         r'''<strong>(b)</strong> La pendiente de A es $0$. La de B es su deriva, $52.11$ por trimestre, casi la media de las 88 diferencias ($52.21$): con $d = 1$ la pendiente la pone la constante, que la mide sobre toda la muestra. C no tiene constante y aun así pronostica una recta, de pendiente $43.23$: con $d = 2$ la pendiente no es un parámetro, sino un promedio de las diferencias con pesos que decaen como $(1-\alpha)^j$ hacia atrás, con $\alpha = 1 + \hat\theta = 0.408$ —el suavizamiento exponencial del Módulo 1 aplicado a $\nabla y$—. Las ocho últimas diferencias se llevan el $98.5\,\%$ del peso: la pendiente sale del tramo final de la serie.''',
         r'''<strong>(c)</strong> A un trimestre, B y C tienen anchos parecidos ($43.6$ y $40.4$). A cuarenta, el de B es $402.0$ y el de C, $2587.0$: $6.4$ veces más. El de B se ha multiplicado por $9.2$ y el de C, por $64$: el ritmo lo decide $d$, como dice el módulo. A, con el mismo $d$ que B, llega a $1438.7$, y ya a un paso es el más ancho ($124.3$), porque sin deriva su $\hat\sigma$ es mucho mayor. El ejercicio no elige modelo —las pruebas tampoco se ponen de acuerdo (KPSS pide $d = 2$; ADF y PP, $d = 1$), y de los tres solo C pasa Ljung–Box(20), con $p = 0.07$—: muestra que elegir $d$ y la constante es elegir la forma del pronóstico y el ritmo al que crece su incertidumbre.''']))

PRACTICAS = [M1, M2, M3, M4, M5, M6, M7, M8, M9]


def aplica(plantillas):
    """`plantillas`: {nombre: texto}. Devuelve el mismo diccionario con los nueve ejercicios insertados."""
    reparto = {"templates_1_3.html": [M1, M2, M3], "templates_4_6.html": [M4, M5, M6],
               "templates_7_9.html": [M7, M8, M9]}
    for nombre, tres in reparto.items():
        t = plantillas[nombre]
        trozos = t.split(ASIDE)
        assert len(trozos) == 4, (nombre, len(trozos))
        # el párrafo de cierre del módulo va pegado a la lista de fuentes: se deja un renglón en blanco antes
        plantillas[nombre] = "".join(tr.rstrip("\n") + "\n\n" + ej + ASIDE if i < 3 else tr
                                     for i, (tr, ej) in enumerate(zip(trozos, tres + [""])))
    return plantillas
