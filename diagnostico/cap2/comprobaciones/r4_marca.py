#!/usr/bin/env python3
"""
r4_marca.py — ronda R4 (fuentes) del capítulo 2: las marcas, las citas y el armazón

Parte SIEMPRE del capítulo 2 tal como estaba en el commit BASE (antes de la R4)
y le aplica, en este orden:

  1. los cambios de prosa (PROSA): frases que la fuente leída no sostenía;
  2. las marcas `data-afirma` y los `<cite class="cita">` vacíos (MARCAS);
  3. el armazón: el CSS de las citas (copiado del capítulo 1), los marcadores
     del pie, la lista de cada módulo y la del capítulo;
  4. `genera_referencias.genera()`, que escribe el texto de citas y listas.

Es reejecutable: como parte del commit BASE y no del archivo de trabajo, correrlo
dos veces da el mismo resultado. Cada cambio exige que su texto aparezca
exactamente una vez; si no, aborta sin escribir.

Notación de MARCAS (el texto original es el mismo sin las marcas):
  [[c2-m1-01]] … [[/]]   <span data-afirma="c2-m1-01"> … </span>
  [[@c2-m1-06]]          atributo data-afirma dentro de la etiqueta que lo lleva
  {{F|§9.1}}             cita vacía, con un espacio delante; F, C, H, R son las claves
  {{^F|§9.1|narrativa}}  sin espacio delante, y con data-modo
  [[+.]]                 texto que se añade (un punto tras la cita)
Los espacios y saltos de línea del original se respetan: al buscar, cualquier
tramo de blancos casa con cualquier otro.

Uso:  python3 diagnostico/cap2/comprobaciones/r4_marca.py
"""
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "precalculo"))
import genera_referencias  # noqa: E402

BASE = "31bfbb6"
RUTA = "Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html"
CAP1 = RAIZ / "Htmls_Series" / "capitulo-1-componentes-descomposicion.html"
CLAVES = {"F": "hyndman2021forecasting", "C": "cryer2008time",
          "H": "hamilton1994time", "R": "rcoreteam2026r"}

# --------------------------------------------------------------------------- #
# 1. Prosa: (texto de BASE, texto nuevo, por qué)
# --------------------------------------------------------------------------- #
PROSA = [
    ("en la práctica, imposible de verificar con una sola",
     "en la práctica, difícil de verificar con una sola",
     "c2-m1-04: la fuente leída dice «difficult», no imposible"),
    ("</strong>, que es lo que hace <code>pacf()</code> en R.</p>",
     "</strong>, que da los mismos valores que <code>pacf()</code> en R.</p>",
     "c2-m4-04: la ayuda de pacf() no nombra la recursión; lo comprobable es que los valores coinciden"),
    ("Esta es la recursión que implementan <code>pacf()</code> de R, el método <code>ldb</code> de statsmodels y "
     "la función <code>calcularPACF()</code> que mueve",
     "Con esta recursión coinciden <code>pacf()</code> de R y el método <code>ldb</code> de statsmodels, y es la "
     "que implementa la función <code>calcularPACF()</code> que mueve",
     "c2-m4-09: lo mismo; calcularPACF() sí es del repo"),
    ("de la PACF vale bajo la hipótesis de que la serie es ruido blanco.",
     "de la PACF vale para los rezagos mayores que $p$ cuando la serie sigue un AR($p$); el ruido blanco es el "
     "caso $p = 0$.",
     "c2-m4-12: Cryer y Chan p. 115 y Hamilton p. 112 dan la banda bajo un AR(p), para rezagos mayores que p"),
    ("Es el modelo por defecto para precios de activos, índices y tipos de cambio, y explica por qué el pronóstico "
     "ingenuo (<em>naïve</em>: \"mañana será como hoy\") es tan difícil de batir en esos casos.",
     "Las caminatas aleatorias se usan mucho para datos financieros y económicos, y eso explica por qué en "
     "precios e índices bursátiles el pronóstico ingenuo (<em>naïve</em>: \"mañana será como hoy\") suele ser el "
     "mejor método.",
     "c2-m5-11: FPP3 no habla de «modelo por defecto» ni de tipos de cambio"),
    ("Las dos más usadas son ADF y KPSS, y lo primero", "Aquí se usan dos, ADF y KPSS, y lo primero",
     "c2-m6-02: «las más usadas» no tiene fuente"),
    ("<td>Datos poco informativos (muestra corta). Ninguna prueba concluye.</td>",
     "<td>Datos poco informativos: ninguna prueba concluye.</td>",
     "c2-m6-06: la causa «muestra corta» no tiene fuente"),
    ("pero el P-VALOR no: R interpola en las tablas de\n# Banerjee et al. (1993) y statsmodels usa la superficie "
     "de respuesta de\n# MacKinnon. De ahi 0.6132",
     "pero el P-VALOR no: R lo interpola en una tabla\n# de valores criticos y statsmodels lo aproxima con una "
     "superficie de\n# respuesta. De ahi 0.6132",
     "c2-m6-14: Banerjee et al. y MacKinnon no se han leído; lo dicen las ayudas de adf.test y adfuller"),
    ("<li>La recomendación de FPP3 es aplicar primero la diferencia estacional: a veces con ella basta y la serie "
     "ya queda estacionaria, y se ahorra una diferencia regular que solo añadiría ruido. Que baste",
     "<li[[@c2-m7-05]]>{{^F|§9.1|narrativa}} recomiendan aplicar primero la diferencia estacional cuando el "
     "patrón estacional es marcado: a veces con ella basta y la serie ya queda estacionaria, y se ahorra una "
     "diferencia regular. Que baste",
     "c2-m7-05: la recomendación de FPP3 lleva su condición; «solo añadiría ruido» no es de la fuente"),
    ("Ese es el indicio más frecuente: una autocorrelación", "Ese es el indicio: una autocorrelación",
     "M7: «más frecuente» no tiene fuente"),
    ("y la más frecuente es el logaritmo, que convierte", "y a menudo sirve el logaritmo, que convierte",
     "c2-m8-02: FPP3 dice «often useful», no «la más frecuente»"),
    ("<strong>En la práctica casi siempre se usa el logaritmo</strong>, aunque",
     "<strong>En este curso se usa el logaritmo</strong>, aunque",
     "c2-m8-07: «casi siempre» no tiene fuente; es la decisión D6 del curso"),
    ("(que <code>fable</code> aplica sola y <code>statsmodels</code> no)", "(que <code>fable</code> aplica sola)",
     "c2-m8-08: lo de statsmodels no tiene pasaje"),
    ("es el logaritmo, que es lo que se usa en la práctica</td>",
     "es el logaritmo, que es lo que se usa en este curso</td>",
     "c2-m8-07, en la tabla de resumen"),
    ("los tipos de cambio son el ejemplo clásico de caminata aleatoria con deriva, así que",
     "el Módulo 6 encontró en la TRM una raíz unitaria, así que",
     "c2-m9-20: «el ejemplo clásico» no tiene fuente"),
    ("<strong>secc. 9.1</strong> (estacionariedad y diferenciación) y <strong>secc. 3.1–3.2</strong> "
     "(transformaciones y Box–Cox).",
     "<strong>secc. 9.1–9.2</strong> (estacionariedad, diferenciación y el operador $B$), "
     "<strong>secc. 2.8–2.9</strong> (autocorrelación y ruido blanco) y <strong>secc. 3.1</strong> "
     "(transformaciones y Box–Cox).",
     "c2-m9-23: la 3.2 de FPP3 es «Time series components»; Box–Cox está en la 3.1"),
    ("(4.ª ed.), secc. 1.4–1.6 (autocovarianza y estacionariedad) y 2.1 (diferenciación).</li>",
     "(4.ª ed.): medidas de dependencia, series estacionarias, estimación de la correlación y diferenciación. "
     "En la 3.ª edición (2011) son las secc. 1.4–1.6 y 2.3; la numeración de la 4.ª puede ser otra.</li>",
     "c2-m9-24: en la 3.ª ed. la 2.1 es «Introduction» y la diferenciación está en la 2.3; la 4.ª no se ha leído"),
]

# --------------------------------------------------------------------------- #
# 2. Marcas
# --------------------------------------------------------------------------- #
DEF = '<div class="definition"{}> <h4><i class="fas fa-book mr-2" aria-hidden="true"></i>'
MARCAS = [
    # ---- Módulo 1
    "El paso siguiente es otro: [[c2-m1-01]]para <em>modelar</em> la dependencia temporal hace falta que las "
    "reglas del juego no cambien con el tiempo. Esa es la idea de <strong>estacionariedad</strong> "
    "(<em>stationarity</em>){{F|§9.1}}.[[/]]</p>",
    "<p>[[c2-m1-03]]Un proceso $\\{y_t\\}$ es <strong>estrictamente estacionario</strong> si, para cualquier "
    "conjunto de instantes $t_1, \\ldots, t_k$ y cualquier desplazamiento $h$, la distribución conjunta de "
    "$(y_{t_1}, \\ldots, y_{t_k})$ es idéntica a la de $(y_{t_1+h}, \\ldots, y_{t_k+h})${{C|p. 16}}.[[/]]</p>",
    "traslaciones en el tiempo. [[c2-m1-04]]Es una condición muy fuerte y, en la práctica, difícil de verificar "
    "con una sola realización de la serie.[[/]]</p>",
    DEF.format("[[@c2-m1-06]]") + "Definición: estacionariedad débil",
    "es <strong>débilmente estacionario</strong> si cumple las tres condiciones{{C|p. 17}}:</p>",
    "<strong>Relación entre las dos.</strong> [[c2-m1-07]]La estacionariedad estricta con varianza finita implica "
    "la débil, pero no al revés. Hay una excepción importante: si el proceso es <strong>gaussiano</strong>, la "
    "distribución conjunta queda determinada por medias y covarianzas, y entonces las dos nociones "
    "coinciden{{H|p. 46}}.[[/]] En este curso,",
    "[[c2-m1-13]]Una serie con <strong>estacionalidad</strong> no es estacionaria: su media depende del mes, y "
    "por tanto de $t${{F|§9.1}}.[[/]] Los dos términos",
    "<strong>¿Por qué importa tanto?</strong> [[c2-m1-15]]Porque los modelos ARMA del Capítulo 3 —y la teoría de "
    "estimación e inferencia que los acompaña— <strong>suponen</strong> estacionariedad{{C|p. 16}}.[[/]] Si la "
    "serie no lo es,",
    # ---- Módulo 2
    "aleatoriedad sin memoria. [[c2-m2-01]]Es el ladrillo con el que se construyen todos los modelos del "
    "curso{{H|p. 47}}[[/]]; el primero aparece",
    DEF.format("[[@c2-m2-02]]") + "Definición: ruido blanco</h4>",
    "que se escribe $\\varepsilon_t \\sim \\mathrm{N}(0, \\sigma^2)$ i.i.d.{{H|pp. 47–48}}[[+.]]</p>",
    "<strong>No confundir incorrelación con independencia.</strong> [[c2-m2-03]]El ruido blanco exige covarianzas "
    "nulas, que es una condición sobre relaciones <em>lineales</em>. Dos variables pueden ser incorreladas y aun "
    "así dependientes{{H|p. 48}}: si $x_t$ es ruido blanco, la serie $x_t^2$ puede tener estructura clarísima. Esa "
    "distinción es la puerta de entrada a los modelos ARCH/GARCH de volatilidad, que quedan fuera de este curso "
    "pero explican por qué en finanzas los rendimientos parecen ruido blanco y sus cuadrados no{{C|p. 285}}.[[/]]</p>",
    "<strong>Cómo leer la banda.</strong> [[c2-m2-06]]Si la serie es ruido blanco <strong>independiente</strong> "
    "—i.i.d., no solo incorrelado—, cada autocorrelación muestral se distribuye aproximadamente "
    "$\\mathrm{N}(0, 1/T)${{C|p. 110}}. Por eso la banda de $\\pm 1.96/\\sqrt{T}$ marca la zona donde cae el 95 % "
    "de las barras <strong>por azar</strong>{{F|§2.9}}.[[/]] Con",
    "[[c2-m2-08]]Una barra que apenas asoma fuera de la banda no es evidencia de nada; una barra muy grande, o un "
    "patrón, sí{{F|§2.9}}.[[/]] [[c2-m2-10]]Y si el ruido es incorrelado pero no independiente —el caso de la "
    "advertencia de arriba—, la varianza de $r_k$ puede dejar de ser $1/T$, y entonces la banda ya no cubre el "
    "95 %.[[/]]</p>",
    "<strong>El ruido blanco es también la meta.</strong> [[c2-m2-09]]Un modelo de series de tiempo es bueno "
    "cuando ha exprimido toda la estructura predecible de la serie y lo que sobra —los residuales— es "
    "indistinguible del ruido blanco. Si en los residuales todavía queda autocorrelación, queda información sin "
    "aprovechar{{F|§5.4}}.[[/]] Ese",
    # ---- Módulo 3
    "<p>[[c2-m3-01]]La <strong>autocorrelación</strong> mide cuánto se parece una serie a una copia de sí misma "
    "desplazada $k$ instantes. Es la traducción cuantitativa del gráfico de rezagos del Módulo 3 del "
    "Capítulo 1{{F|§2.8}}[[/]], y es también el",
    "<strong>Un detalle que sorprende:</strong> [[c2-m3-05]]la suma tiene $T-k$ términos pero se divide entre "
    "$T$, no entre $T-k${{C|p. 46}}.[[/]] [[c2-m3-15]]Es deliberado. Ese divisor garantiza que la matriz de "
    "autocovarianzas resultante sea semidefinida positiva —una propiedad que los algoritmos de estimación "
    "necesitan— a cambio de un sesgo pequeño hacia cero en rezagos grandes.[[/]] [[c2-m3-06]]Tanto "
    "<code>acf()</code> de R como <code>acf(..., adjusted=False)</code> de <code>statsmodels</code> usan el "
    "divisor $T$; por eso las dos coinciden.[[/]]</p>",
    "<p>[[c2-m3-07]]El <strong>correlograma</strong> es simplemente el gráfico de $r_k$ contra "
    "$k${{F|§2.8}}.[[/]] Es la herramienta",
    "Módulo 5. [[c2-m3-16]]Y las fórmulas de este módulo suponen una serie estacionaria{{C|p. 46}}[[/]]: en una "
    "caminata o en",
    "que además cambia el recuento de barras por [[c2-m3-17]]una prueba formal, la de Ljung–Box, que las resume "
    "todas en un solo p-valor{{F|§5.4}}[[/]].</p>",
    "<strong>La ACF no distingue causa de coincidencia.</strong> [[c2-m3-13]]Dos series con tendencia creciente "
    "tendrán autocorrelaciones altas y correlación cruzada alta entre sí aunque no tengan ninguna relación "
    "real{{C|pp. 263–264}}. Es el fenómeno de la <em>regresión espuria</em>: con series no estacionarias, los "
    "estadísticos habituales mienten{{H|pp. 557–558}}.[[/]] Otra razón",
    # ---- Módulo 4
    "[[c2-m4-01]]Si hoy depende de ayer, y ayer de anteayer, hoy y anteayer aparecerán correlacionados "
    "<strong>aunque no haya ninguna relación directa</strong> entre ellos: la correlación viaja de forma "
    "indirecta a través de ayer{{F|§9.5}}.[[/]] La ACF no sabe",
    DEF.format("[[@c2-m4-02]]") + "Definición: autocorrelación parcial (PACF)</h4>",
    "el efecto de los rezagos intermedios $y_{t-1}, \\ldots, y_{t-k+1}${{C|p. 112}}.</p>",
    "es el coeficiente $\\phi_{kk}$ de la regresión{{F|§9.5}}</p>",
    "<p>[[c2-m4-04]]En la práctica no se corren $k$ regresiones: se obtiene la PACF a partir de la ACF con la "
    "<strong>recursión de Durbin–Levinson</strong>{{C|p. 115}}, que da los mismos valores que <code>pacf()</code> "
    "en R.[[/]]</p>",
    "<p>[[c2-m4-05]]Ajustar la regresión del rezago $k$ equivale a resolver el sistema de Yule–Walker de orden "
    "$k$, cuya matriz está formada por las propias autocorrelaciones{{C|p. 114}}[[/]]:</p>",
    "<li[[@c2-m4-06]]> <p>La matriz no es una matriz cualquiera: es <strong>simétrica y de Toeplitz</strong> "
    "(constante a lo largo de cada diagonal). Eso permite pasar de la solución de orden $k-1$ a la de orden $k$ "
    "sin volver a empezar{{C|p. 115}}. El coeficiente nuevo es</p>",
    "<li[[@c2-m4-07]]> <p>Léelo como lo que es:",
    "<li[[@c2-m4-08]]> <p>Y los demás coeficientes se actualizan con una sola pasada{{C|p. 115}}:</p>",
    '<p class="derivacion-resultado"[[@c2-m4-09]]>Con esta recursión coinciden',
    "<li[[@c2-m4-14]]>La <strong>TRM</strong> es la Tasa Representativa del Mercado",
    '<div class="note"[[@c2-m4-11]]> <p><strong>Anticipo del Capítulo 3.</strong>',
    "y en ese caso los gráficos ya no dicen cuánto valen $p$ y $q${{F|§9.5}}.</li>",
    "<strong>La misma banda, la misma trampa.</strong> [[c2-m4-12]]La banda $\\pm 1.96/\\sqrt{T}$ de la PACF vale "
    "para los rezagos mayores que $p$ cuando la serie sigue un AR($p$){{C|p. 115}}; el ruido blanco es el caso "
    "$p = 0$.[[/]] Con 24 rezagos",
    # ---- Módulo 5
    "<p>Todo depende del valor de $\\phi$:</p> <ul[[@c2-m5-01]]> <li><strong>$|\\phi| &lt; 1$</strong>: el proceso "
    "es <strong>estacionario</strong>{{F|§9.3}}. Un choque",
    "La ACF teórica es $\\rho_k = \\phi^k$, un decaimiento exponencial{{C|p. 67}}.</li>",
    "Rara vez sirve para modelar datos reales{{C|p. 89}}.</li>",
    "De ahí salen sus dos propiedades incómodas:</p> <ul[[@c2-m5-04]]> <li>$\\operatorname{Var}(y_t) = "
    "t\\,\\sigma^2$: la varianza <strong>crece sin límite</strong>{{C|p. 13}};</li> <li>un choque nunca se olvida: "
    "su efecto sobre todos los valores futuros es permanente{{H|p. 443}}.</li>",
    '<p style="margin-bottom:0;">[[c2-m5-05]]El nombre <strong>raíz unitaria</strong> viene de escribir el modelo '
    "con el operador de rezago $B$ (donde $By_t = y_{t-1}$): la ecuación $(1-\\phi B)y_t = \\varepsilon_t$ tiene el "
    "polinomio característico $1 - \\phi z = 0$, cuya raíz es $z = 1/\\phi$. La condición de estacionariedad "
    "$|\\phi| &lt; 1$ equivale a que esa raíz esté <strong>fuera</strong> del círculo unitario{{C|p. 71}}; con "
    "$\\phi = 1$ la raíz vale exactamente 1.[[/]] El Capítulo 3",
    "[[c2-m5-07]]Este es el caso difícil: cuanto más corta es la muestra y más se acerca $\\phi$ a 1, menos se "
    "diferencian los dos correlogramas, y distinguir $\\phi = 0.95$ de $\\phi = 1$ acaba siendo casi "
    "imposible{{H|p. 445}}.[[/]]</li>",
    "<p>[[c2-m5-09]]Al añadir una constante se obtiene la <strong>caminata aleatoria con deriva</strong> "
    "(<em>random walk with drift</em>){{F|§9.1}}[[/]]:</p>",
    "<p>[[c2-m5-10]]El término $ct$ es una recta, y la suma $\\sum\\varepsilon_i$ que se le añade es la "
    "<strong>tendencia estocástica</strong>: la serie sube en promedio $c$ por periodo, pero no vuelve a esa "
    "recta{{H|p. 442}}, porque la distancia que la separa de ella es una caminata aleatoria cuya varianza, "
    "$t\\sigma^2$, no deja de crecer.[[/]] [[c2-m5-11]]Las caminatas aleatorias se usan mucho para datos "
    "financieros y económicos{{F|§9.1}}, y eso explica por qué en precios e índices bursátiles el pronóstico "
    "ingenuo (<em>naïve</em>: \"mañana será como hoy\") suele ser el mejor método{{F|§5.4}}.[[/]]</p>",
    "<strong>Tendencia determinista vs. tendencia estocástica.</strong> [[c2-m5-12]]Se parecen en el gráfico y "
    "exigen tratamientos opuestos. $y_t = a + bt + \\varepsilon_t$ (determinista) se corrige <em>quitando</em> la "
    "recta ajustada; $y_t = c + y_{t-1} + \\varepsilon_t$ (estocástica) se corrige "
    "<strong>diferenciando</strong>{{H|pp. 435–436}}.[[/]] Aplicar",
    # ---- Módulo 6
    "<p>[[c2-m6-01]]Mirar el correlograma es indispensable, pero es subjetivo. Las <strong>pruebas de raíz "
    "unitaria</strong> (<em>unit root tests</em>) ponen un número a la decisión{{F|§9.1}}. Aquí se usan dos, ADF "
    "y KPSS, y lo primero que hay que grabarse es que <strong>plantean hipótesis nulas "
    "contrarias</strong>.[[/]]</p>",
    DEF.format("[[@c2-m6-04]]") + "ADF — Dickey–Fuller aumentada</h4>",
    "Un <strong>p-valor pequeño rechaza la raíz unitaria</strong>, es decir, favorece la "
    "estacionariedad{{C|pp. 128–129}}. <code>adf.test()</code>",
    "<p>[[c2-m6-05]]Descompone la serie en tendencia determinista + caminata aleatoria + error estacionario, y "
    "contrasta $H_0$: la varianza del componente de caminata es cero, es decir, <strong>la serie ES "
    "estacionaria</strong> (en nivel o alrededor de una tendencia, según la variante).[[/]]</p> "
    '<p style="margin-bottom:0;">[[c2-m6-16]]Aquí un <strong>p-valor pequeño rechaza la '
    "estacionariedad</strong>{{F|§9.1}}. Es exactamente al revés que el ADF.[[/]]</p>",
    '<table[[@c2-m6-06]]> <caption class="sr-only">Combinaciones posibles de resultados de ADF y KPSS</caption>',
    "[[c2-m6-17]]En el ADF la hipótesis nula es la tendencia estocástica y la alternativa, la "
    "determinista{{C|pp. 129–130}}[[/]]; en el KPSS de tendencia, al revés.",
    "<strong>Sobre los p-valores al borde.</strong> [[c2-m6-09]]Tanto <code>adf.test</code> como "
    "<code>kpss.test</code> interpolan en tablas publicadas y avisan cuando el valor cae fuera del rango "
    "tabulado.[[/]] Por eso",
    "<strong>Eso es falso, y conviene entender exactamente por qué.</strong> [[c2-m6-10]]<code>adf.test</code> "
    "elige por defecto $k = \\lfloor (T-1)^{1/3} \\rfloor = 5$ rezagos, <strong>menos que el periodo "
    "estacional</strong> $m = 12$.[[/]] [[c2-m6-11]]La oscilación anual —que sube y baja con enorme regularidad, "
    "es decir, revierte a su media todo el tiempo— no cabe en esos 5 rezagos, se queda en el residuo, y el ADF la "
    "lee como evidencia de estacionariedad.[[/]]</p>",
    # ---- Módulo 7
    "<p>[[c2-m7-01]]La <strong>diferenciación</strong> es la herramienta estándar para eliminar una raíz "
    "unitaria: en vez de modelar el nivel de la serie, se modelan sus <em>cambios</em>{{F|§9.1}}.[[/]] El "
    "Módulo 3",
    DEF.format("[[@c2-m7-02]]") + "Operador de rezago y operador de diferencia</h4>",
    "$B y_t = y_{t-1}$, y en general $B^k y_t = y_{t-k}${{F|§9.2}}.</p>",
    "$\\nabla$ deja $T-1$ datos, $\\nabla_{12}$ deja $T-12${{F|§9.1}}.</p>",
    "<p>[[c2-m7-18]]<code>nsdiffs()</code> y <code>ndiffs()</code> son funciones del paquete "
    "<code>forecast</code> de R. La segunda repite una prueba KPSS —diferenciar, volver a probar— hasta que deja "
    "de rechazar o llega a dos diferencias, y devuelve cuántas hicieron falta. No es el <code>kpss.test()</code> "
    "del Módulo 6: usa la versión del paquete <code>urca</code>, con otro truncamiento de rezagos, y las dos "
    "pueden no coincidir, como muestra el recuadro del final de este módulo. La primera mide la fuerza de la "
    "estacionalidad con la fórmula del $F_S$ del Capítulo 1, calculada sobre su propia descomposición STL, y pide "
    "una diferencia estacional si pasa de 0.64{{F|§9.1}}.[[/]] Cada una decide",
    "<li[[@c2-m7-06]]><strong>El correlograma.</strong> Si la ACF decae despacio y casi en línea recta, falta "
    "diferenciar. Si tras diferenciar cae rápido dentro de la banda, ya está{{F|§9.1}}.</li>",
    "<li[[@c2-m7-07]]><strong>Las pruebas del Módulo 6</strong>, aplicadas de forma secuencial: diferenciar, "
    "volver a probar, repetir{{F|§9.1}}. Es lo que hace",
    "<p[[@c2-m7-08]]>Que aquí coincidan no convierte el mínimo de la varianza en una regla",
    "<p>[[c2-m7-09]]Diferenciar de más no es inofensivo: <strong>introduce autocorrelación que no estaba en los "
    "datos</strong>{{F|§9.1}}.[[/]] La columna",
    "<p[[@c2-m7-11]]><strong>Adelanto del Capítulo 3.</strong> Esa serie fabricada tiene nombre:",
    "y que le da problemas al estimador{{C|pp. 126–127}}. En la duda, conviene diferenciar de "
    "menos{{F|§9.1}}.</p>",
    "Son $D = 1$ y $d = 1$: [[c2-m7-14]]la serie del modelo <em>airline</em> que se ajusta en el "
    "Capítulo 5{{C|pp. 240–241}}[[/]], y una de las",
    "[[c2-m7-19]]<code>UKgas</code>, la serie de un ejercicio del Capítulo 1, es el consumo trimestral de gas del "
    "Reino Unido de 1960 a 1986: 108 trimestres, con $m = 4${{R|§Description; §Format}}.[[/]] Se toma en "
    "logaritmos",
    "<p[[@c2-m7-15]]>El motivo es el <strong>truncamiento de rezagos</strong>",
    # ---- Módulo 8
    "<p>[[c2-m8-01]]La diferenciación arregla la media, pero no la varianza{{F|§9.1}}.[[/]] En "
    "<code>AirPassengers</code> las oscilaciones",
    "<p>[[c2-m8-02]]La solución es una transformación de <strong>estabilización de la varianza</strong>, y a "
    "menudo sirve el logaritmo, que convierte crecimiento multiplicativo en aditivo. La familia de Box–Cox lo "
    "generaliza{{F|§3.1}}[[/]]:</p>",
    DEF.format("[[@c2-m8-03]]") + "Transformación de Box–Cox</h4>",
    "Así escrita exige $y_t &gt; 0${{C|p. 101}}; <code>BoxCox()</code> de <code>forecast</code> y "
    "<code>box_cox()</code> de <code>fpp3</code> usan una variante con el signo de $y_t$ que admite valores "
    "negativos cuando $\\lambda &gt; 0${{F|§3.1}}.",
    DEF.format("[[@c2-m8-04]]") + "Cómo elegir $\\lambda$: el criterio de Guerrero</h4>",
    '<p style="margin-bottom:0;">[[c2-m8-05]]Se prefiere igual, por dos razones que pesan más que ese '
    "sobrecosto: (1) $\\lambda = 0$ es interpretable —los cambios se leen como variaciones porcentuales— mientras "
    "que $\\lambda = -0.295$ no significa nada para nadie{{F|§3.1}}; (2) el $\\hat\\lambda$ óptimo es él mismo una "
    "estimación, hecha aquí con solo 12 bloques anuales, y tiene su propia incertidumbre{{C|p. 101}}.[[/]]</p>",
    "<strong>Al deshacer la transformación aparece un sesgo.</strong> [[c2-m8-08]]Si se pronostica $w_t$ y se "
    "vuelve con $\\exp(\\cdot)$, lo que se obtiene es la <strong>mediana</strong> del pronóstico, no la media "
    "—siempre que la distribución del pronóstico en la escala transformada sea simétrica—. Para la media hace "
    "falta una corrección de sesgo (que <code>fable</code> aplica sola){{F|§5.6}}.[[/]] El Capítulo 6",
    # ---- Módulo 9
    "<p>[[c2-m9-01]]Todo el capítulo se resume en una secuencia de decisiones que conviene ejecutar "
    "<strong>siempre en este orden</strong>, porque cada paso condiciona el diagnóstico del "
    "siguiente{{F|§9.7}}.[[/]] Los pasos 2 a 5",
    "<li[[@c2-m9-11]]><strong>Fuga de información</strong> (<em>data leakage</em>):",
    "se estiman <strong>solo</strong> con el entrenamiento{{F|§5.10}}.</li>",
    "<li[[@c2-m9-12]]><strong>La validación cruzada estándar no sirve</strong>: barajar observaciones destruye "
    "el orden y entrena con datos posteriores a los de prueba. Hay que usar validación de origen "
    "móvil{{F|§5.10}}, y a eso",
    "<li[[@c2-m9-13]]><strong>La estacionariedad sigue importando fuera de ARIMA</strong>",
    "<li[[@c2-m9-24]]>Shumway &amp; Stoffer, <em>Time Series Analysis and Its Applications</em> (4.ª ed.): "
    "medidas",
]


# --------------------------------------------------------------------------- #
# Tras la verificación independiente (R4_verificacion.md): más cambios de prosa
# y las marcas que cambian con ellos. Se aplican después de PROSA y antes de
# MARCAS; MARCAS_V sustituye a la marca de MARCAS que empieza igual.
# --------------------------------------------------------------------------- #
PROSA_V = [
    ("Ajustar la regresión del rezago $k$ equivale a resolver el sistema de Yule–Walker de orden $k$, cuya",
     "Los coeficientes $\\phi_{k1}, \\ldots, \\phi_{kk}$ de la definición satisfacen el sistema de Yule–Walker "
     "de orden $k$, cuya",
     "c2-m4-05: la equivalencia con una regresión ajustada solo vale en la población"),
    ("<p>En la práctica no se corren $k$ regresiones: se obtiene la PACF a partir de la ACF con la "
     "<strong>recursión de Durbin–Levinson</strong>, que da los mismos valores que <code>pacf()</code> en R.</p>",
     "<p>[[c2-m4-04]]En la práctica la PACF muestral se calcula a partir de la ACF: se sustituyen las "
     "autocorrelaciones teóricas $\\rho_k$ por las muestrales $r_k$ y se aplica la <strong>recursión de "
     "Durbin–Levinson</strong>{{C|p. 115}}, que da los mismos valores que <code>pacf()</code> en R. Por eso no "
     "coincide exactamente con el último coeficiente de una regresión por mínimos cuadrados sobre $k$ "
     "rezagos.[[/]]</p>",
     "c2-m4-04: daba a entender que k regresiones darían lo mismo"),
    ("Equivalentemente: sobre la serie centrada —a la que ya se le restó su media—, es el coeficiente "
     "$\\phi_{kk}$ de la regresión</p>",
     "Equivalentemente: con el proceso centrado —ya restada su media—, es el último coeficiente, $\\phi_{kk}$, "
     "de la mejor predicción lineal de $y_t$ a partir de sus $k$ valores anteriores{{H|p. 111}}:</p>",
     "c2-m4-02: la cita separaba «la regresión» de su ecuación, y «regresión» se leía como ajuste muestral"),
    ("Dos series con tendencia creciente tendrán autocorrelaciones altas y correlación cruzada alta entre sí "
     "aunque no tengan ninguna relación real.",
     "Dos series no estacionarias independientes pueden mostrar una correlación cruzada alta sin tener ninguna "
     "relación real.",
     "c2-m3-13: la fuente dice «sometimes» y su ejemplo no tiene tendencia determinista"),
    ("Rara vez sirve para modelar datos reales.</li>",
     "Es una no estacionariedad menos razonable que la de $\\phi = 1${{C|p. 89}}.</li>",
     "c2-m5-01: «rara vez sirve» no lo dice la fuente"),
    ("<code>adf.test()</code> de R estima siempre la regresión completa, con constante y tendencia.</p>",
     "La regresión con constante y tendencia es la que corresponde cuando la alternativa es una tendencia lineal "
     "más un error estacionario{{C|p. 130}}, y es la que <code>adf.test()</code> de R estima siempre.</p>",
     "c2-m6-04: la regresión con constante y tendencia está en la p. 130"),
    ("Un modelo de series de tiempo es bueno cuando ha exprimido toda la estructura predecible de la serie y lo "
     "que sobra",
     "Un buen modelo de series de tiempo ha exprimido toda la estructura predecible de la serie, y lo que sobra",
     "c2-m2-09: la fuente lo da como propiedad de un buen método, no como criterio suficiente"),
    ("hoy y anteayer aparecerán correlacionados", "hoy y anteayer pueden aparecer correlacionados",
     "c2-m4-01: FPP3 dice «might»"),
    ("es la herramienta estándar para eliminar una raíz", "es una manera de eliminar una raíz",
     "c2-m7-01: FPP3 dice «one way»"),
    ("La diferenciación arregla la media, pero no la varianza.",
     "La diferenciación estabiliza la media; para la varianza hace falta una transformación.",
     "c2-m8-01: la fuente reparte los papeles, no niega"),
    ("no es evidencia de nada;", "no basta como evidencia;", "c2-m2-08: más fuerte que la fuente"),
    ("mide cuánto se parece una serie a una copia de sí misma desplazada",
     "mide la relación lineal entre una serie y una copia de sí misma desplazada",
     "c2-m3-01: FPP3 dice «linear relationship»"),
    (", y eso explica por qué en precios e índices bursátiles",
     "; como su pronóstico es el último valor observado, en precios e índices bursátiles",
     "c2-m5-11: la causa, en la fuente, es que el pronóstico de una caminata es el último valor"),
    ("En la duda, conviene diferenciar de menos.", "No conviene diferenciar más de lo necesario.",
     "c2-m7-11: la fuente no habla de la duda"),
    ("en una muestra cualquiera el cociente de varianzas sigue de cerca a",
     "en una muestra de una serie estacionaria el cociente de varianzas se acerca a",
     "c2-m7-08: no se cumple en series no estacionarias"),
    ("<p>Por eso se trabaja casi siempre con una versión más manejable, que solo pide que los <strong>dos "
     "primeros momentos</strong> sean invariantes:</p>",
     "<p>[[c2-m1-05]]Por eso se trabaja con una versión más manejable, que solo pide que los <strong>dos "
     "primeros momentos</strong> sean invariantes{{C|p. 17}}[[/]]:</p>",
     "c2-m1-05: «casi siempre» no tiene fuente"),
    ("Abajo, el criterio de Guerrero para cada $\\lambda$: el punto naranja",
     "Abajo, [[c2-m8-13]]el criterio de Guerrero para cada $\\lambda$ —el que {{^F|§3.1|narrativa}} ofrecen "
     "para elegirla—[[/]]: el punto naranja",
     "c2-m8-13: la atribución a Guerrero no tenía marca"),
    ("<li>Hyndman &amp; Athanasopoulos, <em>Forecasting: Principles and Practice</em> (3.ª ed.), "
     "<strong>secc. 9.1–9.2</strong> (estacionariedad, diferenciación y el operador $B$), "
     "<strong>secc. 2.8–2.9</strong> (autocorrelación y ruido blanco) y <strong>secc. 3.1</strong> "
     "(transformaciones y Box–Cox).",
     "<li[[@c2-m9-23]]>{{^F|§9.1|narrativa}}, <em>Forecasting: Principles and Practice</em> (3.ª ed.): esa "
     "sección (estacionariedad y diferenciación) y las secc. <strong>9.2</strong> (el operador $B$), "
     "<strong>2.8–2.9</strong> (autocorrelación y ruido blanco) y <strong>3.1</strong> (transformaciones y "
     "Box–Cox).",
     "c2-m9-23: la lectura de FPP3, con cita generada"),
    ("<li>Kwiatkowski, Phillips, Schmidt &amp; Shin (1992).", "<li[[@c2-m9-25]]>Kwiatkowski, Phillips, Schmidt "
     "&amp; Shin (1992).", "c2-m9-25: marca"),
    ("— el artículo original de la prueba KPSS.</li>",
     "— el artículo al que se atribuye la prueba KPSS{{F|§9.1}}.</li>",
     "c2-m9-25: «original» no se puede afirmar sin leerlo; FPP3 le atribuye la prueba"),
    ("<li>Guerrero, V.M. (1993).", "<li[[@c2-m9-26]]>Guerrero, V.M. (1993).", "c2-m9-26: marca"),
    ("— el criterio de selección de $\\lambda$ del Módulo 8.</li>",
     "— el criterio de selección de $\\lambda$ del Módulo 8{{F|§3.1}}.</li>", "c2-m9-26: cita"),
    ("</i>KPSS — Kwiatkowski, Phillips, Schmidt y Shin</h4>",
     "</i>[[c2-m6-18]]KPSS — Kwiatkowski, Phillips, Schmidt y Shin{{F|§9.1}}[[/]]</h4>",
     "c2-m6-18: el título atribuía la prueba sin marca"),
]

MARCAS_V = {
    "es <strong>débilmente estacionario</strong> si cumple":
        "es <strong>débilmente estacionario</strong>{{C|p. 17}} si cumple las tres condiciones:</p>",
    "<strong>El ruido blanco es también la meta.</strong>":
        "<strong>El ruido blanco es también la meta.</strong> [[c2-m2-09]]Un buen modelo de series de tiempo ha "
        "exprimido toda la estructura predecible de la serie, y lo que sobra —los residuales— es indistinguible "
        "del ruido blanco. Si en los residuales todavía queda autocorrelación, queda información sin "
        "aprovechar{{F|§5.4}}.[[/]] Ese",
    "[[c2-m2-08]]Una barra":
        "[[c2-m2-08]]Una barra que apenas asoma fuera de la banda no basta como evidencia; una barra muy grande, "
        "o un patrón, sí{{F|§2.9}}.[[/]] [[c2-m2-10]]Y si el ruido es incorrelado pero no independiente —el caso "
        "de la advertencia de arriba—, la varianza de $r_k$ puede dejar de ser $1/T$, y entonces la banda ya no "
        "cubre el 95 %.[[/]]</p>",
    "<p>[[c2-m3-01]]":
        "<p>[[c2-m3-01]]La <strong>autocorrelación</strong> mide la relación lineal entre una serie y una copia "
        "de sí misma desplazada $k$ instantes. Es la traducción cuantitativa del gráfico de rezagos del Módulo 3 "
        "del Capítulo 1{{F|§2.8}}[[/]], y es también el",
    "<strong>La ACF no distingue causa de coincidencia.</strong>":
        "<strong>La ACF no distingue causa de coincidencia.</strong> [[c2-m3-13]]Dos series no estacionarias "
        "independientes pueden mostrar una correlación cruzada alta sin tener ninguna relación "
        "real{{C|pp. 263–264}}. Es el fenómeno de la <em>regresión espuria</em>: con series no estacionarias, los "
        "estadísticos habituales mienten{{H|pp. 557–558}}.[[/]] Otra razón",
    "[[c2-m4-01]]":
        "[[c2-m4-01]]Si hoy depende de ayer, y ayer de anteayer, hoy y anteayer pueden aparecer correlacionados "
        "<strong>aunque no haya ninguna relación directa</strong> entre ellos: la correlación viaja de forma "
        "indirecta a través de ayer{{F|§9.5}}.[[/]] La ACF no sabe",
    "es el coeficiente $\\phi_{kk}$ de la regresión": None,          # la cita va ya en PROSA_V
    "<p>[[c2-m4-04]]": None,                                          # la marca va ya en PROSA_V
    "<p>[[c2-m4-05]]":
        "<p>[[c2-m4-05]]Los coeficientes $\\phi_{k1}, \\ldots, \\phi_{kk}$ de la definición satisfacen el sistema "
        "de Yule–Walker de orden $k$, cuya matriz está formada por las propias autocorrelaciones{{C|p. 114}}[[/]]:</p>",
    "Rara vez sirve para modelar datos reales": None,                 # la cita va ya en PROSA_V
    "<p>[[c2-m5-09]]":
        "<p>[[c2-m5-09]]Al añadir una constante se obtiene la <strong>caminata aleatoria con deriva</strong> "
        "(<em>random walk with drift</em>){{H|p. 436}}[[/]]:</p>",
    "<p>[[c2-m5-10]]":
        "<p>[[c2-m5-10]]El término $ct$ es una recta, y la suma $\\sum\\varepsilon_i$ que se le añade es la "
        "<strong>tendencia estocástica</strong>: la serie sube en promedio $c$ por periodo, pero no vuelve a esa "
        "recta{{H|p. 442}}, porque la distancia que la separa de ella es una caminata aleatoria cuya varianza, "
        "$t\\sigma^2$, no deja de crecer.[[/]] [[c2-m5-11]]Las caminatas aleatorias se usan mucho para datos "
        "financieros y económicos{{F|§9.1}}; como su pronóstico es el último valor observado, en precios e "
        "índices bursátiles el pronóstico ingenuo (<em>naïve</em>: \"mañana será como hoy\") suele ser el mejor "
        "método{{F|§5.4}}.[[/]]</p>",
    "Un <strong>p-valor pequeño rechaza la raíz unitaria</strong>":
        "Un <strong>p-valor pequeño rechaza la raíz unitaria</strong>, es decir, favorece la "
        "estacionariedad{{C|pp. 128–129}}. La regresión",
    "<p>[[c2-m7-01]]":
        "<p>[[c2-m7-01]]La <strong>diferenciación</strong> es una manera de eliminar una raíz unitaria: en vez de "
        "modelar el nivel de la serie, se modelan sus <em>cambios</em>{{F|§9.1}}.[[/]] El Módulo 3",
    "y que le da problemas al estimador":
        "y que le da problemas al estimador{{C|pp. 126–127}}. No conviene diferenciar más de lo "
        "necesario{{F|§9.1}}.</p>",
    "<p>[[c2-m8-01]]":
        "<p>[[c2-m8-01]]La diferenciación estabiliza la media; para la varianza hace falta una "
        "transformación{{F|§9.1}}.[[/]] En <code>AirPassengers</code> las oscilaciones",
    '<p style="margin-bottom:0;">[[c2-m8-05]]':
        '<p style="margin-bottom:0;">[[c2-m8-05]]Se prefiere igual, por dos razones que pesan más que ese '
        "sobrecosto: (1) $\\lambda = 0$ es interpretable —los cambios se leen como variaciones "
        "porcentuales{{F|§3.1}}— mientras que $\\lambda = -0.295$ no significa nada para nadie; (2) el "
        "$\\hat\\lambda$ óptimo es él mismo una estimación, hecha aquí con solo 12 bloques anuales, y tiene su "
        "propia incertidumbre{{C|p. 101}}.[[/]]</p>",
}


def _capa_tras_verificacion() -> None:
    PROSA.extend(PROSA_V)
    usadas = set()
    for n, marca in enumerate(MARCAS):
        for inicio, nueva in MARCAS_V.items():
            if marca.startswith(inicio):
                MARCAS[n] = nueva
                usadas.add(inicio)
    if set(MARCAS_V) - usadas:
        sys.exit(f"ABORTA [MARCAS_V]: sin usar {sorted(set(MARCAS_V) - usadas)}")
    MARCAS[:] = [m for m in MARCAS if m is not None]


_capa_tras_verificacion()

RE_MARCA = re.compile(r"\[\[(/|@[a-z0-9-]+|\+[^\]]*|c\d-m\d+-\d+)\]\]|\{\{(\^?)([FCHR])\|([^|}]+)(?:\|(\w+))?\}\}")


def flexible(texto: str) -> str:
    """El texto como expresión regular en la que los blancos casan con blancos."""
    partes = re.split(r"(\s+)", texto)
    return "".join(r"\s+" if p.isspace() else re.escape(p) for p in partes if p != "")


def expande(m: re.Match) -> str:
    if m.group(1) is not None:
        t = m.group(1)
        if t == "/":
            return "</span>"
        if t.startswith("@"):
            return f' data-afirma="{t[1:]}"'
        if t.startswith("+"):
            return t[1:]
        return f'<span data-afirma="{t}">'
    pegada, clave, loc, modo = m.group(2), CLAVES[m.group(3)], m.group(4), m.group(5)
    extra = f' data-modo="{modo}"' if modo else ""
    return (("" if pegada else " ")
            + f'<cite class="cita" data-ref="{clave}" data-loc="{loc}"{extra}></cite>')


def aplica(html: str, viejo: str | None, nuevo: str, etiqueta: str) -> str:
    """Sustituye `viejo` (o `nuevo` sin marcas) por `nuevo` con las marcas expandidas."""
    if viejo is None:
        # las piezas literales entre marcas se capturan para devolverlas intactas
        trozos, ultimo = [], 0
        for m in RE_MARCA.finditer(nuevo):
            trozos.append(("lit", nuevo[ultimo:m.start()]))
            trozos.append(("marca", m))
            ultimo = m.end()
        trozos.append(("lit", nuevo[ultimo:]))
        patron = "".join(f"({flexible(t)})" for tipo, t in trozos if tipo == "lit")
        halla = list(re.finditer(patron, html))
        if len(halla) != 1:
            sys.exit(f"ABORTA [{etiqueta}]: aparece {len(halla)} veces, se esperaba 1\n   {nuevo[:110]}")
        h, n, salida = halla[0], 0, []
        for tipo, t in trozos:
            if tipo == "lit":
                n += 1
                salida.append(h.group(n))
            else:
                salida.append(expande(t))
        return html[:h.start()] + "".join(salida) + html[h.end():]
    halla = list(re.finditer(flexible(viejo), html))
    if len(halla) != 1:
        sys.exit(f"ABORTA [{etiqueta}]: aparece {len(halla)} veces, se esperaba 1\n   {viejo[:110]}")
    h = halla[0]
    return html[:h.start()] + RE_MARCA.sub(expande, nuevo) + html[h.end():]


def unico(html: str, texto: str, etiqueta: str) -> int:
    if html.count(texto) != 1:
        sys.exit(f"ABORTA [{etiqueta}]: aparece {html.count(texto)} veces, se esperaba 1")
    return html.index(texto)


def main() -> int:
    html = subprocess.run(["git", "show", f"{BASE}:{RUTA}"], cwd=RAIZ, capture_output=True,
                          check=True).stdout.decode("utf-8")

    # 1 y 2 — prosa y marcas
    for viejo, nuevo, motivo in PROSA:
        html = aplica(html, viejo, nuevo, "prosa · " + motivo[:40])
    for n, marca in enumerate(MARCAS, start=1):
        html = aplica(html, None, marca, f"marca {n}")

    # La tabla de patrones del correlograma: la marca envuelve la tabla y la
    # línea de fuentes que se le añade debajo (c2-m3-09).
    i = unico(html, '      <table>\n        <caption class="sr-only">Patrones del correlograma y su '
                    'interpretación</caption>', "tabla de patrones")
    j = html.index("      </table>\n", i) + len("      </table>\n")
    tabla = "".join("  " + linea if linea.strip() else linea for linea in html[i:j].splitlines(keepends=True))
    cita = '<cite class="cita" data-ref="{}" data-loc="{}" data-modo="narrativa"></cite>'
    nota = ('        <p class="text-sm text-gray-600" style="margin:-1.25rem 0 1.75rem;">Lecturas de la segunda columna: '
            f'fila 1, {cita.format(CLAVES["F"], "§2.9")}; fila 2, {cita.format(CLAVES["C"], "p. 128")}; fila 3, '
            f'{cita.format(CLAVES["F"], "§2.8")}; fila 4, {cita.format(CLAVES["F"], "§9.1")}. Las cifras de la '
            'tercera columna se calcularon en R.</p>\n')
    html = html[:i] + '      <div data-afirma="c2-m3-09">\n' + tabla + nota + "      </div>\n" + html[j:]

    # 3 — armazón
    # 3a. El CSS de las citas, tal cual lo lleva el capítulo 1, en el mismo sitio.
    c1 = CAP1.read_text("utf-8")
    a = unico(c1, "    /* ------------------------------------------------------------------\n"
                  "       Cita con fuente", "CSS de citas en el cap. 1")
    b = unico(c1, "    /* SVG Styles */", "fin del CSS de citas en el cap. 1")
    css = c1[a:b]
    k = unico(html, "    /* SVG Styles */", "sitio del CSS de citas")
    html = html[:k] + css + html[k:]

    # 3b. El pie: la bibliografía básica la escribe el generador.
    a = unico(html, '      <ul class="space-y-3 text-white/90 text-sm">\n', "lista tecleada del pie")
    b = html.index("      </ul>\n", a) + len("      </ul>\n")
    html = html[:a] + "      <!--PIE-REFERENCIAS:inicio-->\n      <!--PIE-REFERENCIAS:fin-->\n" + html[b:]

    # 3c. La lista de fuentes de cada módulo, al final de su plantilla.
    aside = ('\n      <aside class="fuentes-modulo" aria-label="Fuentes citadas en este módulo">\n'
             "        <h4>Fuentes citadas en este módulo</h4>\n"
             "        <!--FUENTES-MODULO:inicio-->\n        <!--FUENTES-MODULO:fin-->\n      </aside>\n")
    cierre = "    </div>\n  </template>"

    def con_aside(m: re.Match) -> str:
        cuerpo = m.group("cuerpo")
        if "data-ref=" not in cuerpo:
            return m.group(0)
        if not cuerpo.endswith("\n    </div>\n  "):
            sys.exit(f"ABORTA [aside]: el módulo {m.group('n')} no acaba como se esperaba")
        return m.group("abre") + cuerpo[:-len("    </div>\n  ")] + aside.lstrip("\n") + "    </div>\n  " + m.group("cierra")

    html = genera_referencias.RE_MODULO.sub(con_aside, html)
    assert cierre in html

    # 3d. La lista del capítulo, tras las lecturas del Módulo 9.
    k = unico(html, 'data-afirma="c2-m9-26"', "última lectura")
    k = html.index("        </ul>\n", k) + len("        </ul>\n")
    html = (html[:k]
            + '        <h3 style="margin-top:1.5rem;"><i class="fas fa-quote-right mr-2" aria-hidden="true"></i>'
              "Referencias citadas en este capítulo</h3>\n"
              "        <!--REFERENCIAS-CAPITULO:inicio-->\n        <!--REFERENCIAS-CAPITULO:fin-->\n"
            + html[k:])

    # 4 — el generador escribe citas y listas
    biblioteca, candado = genera_referencias.carga_biblioteca()
    html = genera_referencias.genera(html, biblioteca, candado)
    (RAIZ / RUTA).write_text(html, "utf-8")
    print(f"OK  {RUTA}: {len(PROSA)} cambios de prosa, {len(MARCAS)} marcas, "
          f"{html.count('data-afirma=')} afirmaciones, {html.count('<cite class=')} citas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
