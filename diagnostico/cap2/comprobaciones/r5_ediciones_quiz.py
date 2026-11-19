#!/usr/bin/env python3
"""R5 del capítulo 2 · T5.2: `AUTOEVALUACIONES['cap2']`, las ocho preguntas.

Lo importa `r5_edita.py`. Sustituye el arreglo entero; el motor no se toca. Qué cambia en
cada pregunta, y de dónde sale cada cifra, está en `R5_cambios.md` (§2); las cifras, en
`r5_cifras.out` (etiquetas Q…).
"""

QUIZ = r"""    AUTOEVALUACIONES['cap2'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'Una serie mensual de ventas repite todos los años el mismo patrón: sube en diciembre y baja en febrero. Su nivel promedio anual no cambia. ¿Es estacionaria?',
        pista: 'Relee la primera condición de la estacionariedad débil y fíjate en para qué instantes se pide. Después compara dos meses concretos de esta serie.',
        opciones: [
          {
            texto: 'Sí: el nivel promedio de cada año es siempre el mismo, y eso es lo que se pide.',
            correcta: false,
            retro: 'La condición no es sobre el promedio anual, sino sobre la media en cada instante $t$. Promediar el año entero esconde justamente la variación que rompe la estacionariedad.'
          },
          {
            texto: 'Sí, siempre que además su varianza se mantenga constante de un año a otro.',
            correcta: false,
            retro: 'La varianza constante es la condición (2), pero hacen falta las tres a la vez. Aquí falla la (1).'
          },
          {
            texto: 'No: su media depende del mes y, por tanto, del instante $t$ en que se mire.',
            correcta: true,
            retro: 'La primera condición pide $E[y_t] = \\mu$ para <em>todo</em> $t$. Con estacionalidad, la esperanza de diciembre es distinta de la de febrero. «Estacional» y «estacionario» suenan parecido y significan cosas opuestas.'
          },
          {
            texto: 'No se puede saber sin aplicarle antes una prueba de raíz unitaria.',
            correcta: false,
            retro: 'No hace falta prueba alguna: la estacionalidad incumple la definición por sí sola. Y aplicar el ADF a una serie estacional cruda es precisamente lo que el Módulo 6 desaconseja.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 2,
        pregunta: 'En un correlograma, la barra del rezago 5 vale $r_5 = 0.15$. Que quede dentro o fuera de la banda $\\pm 1.96/\\sqrt{T}$ depende de cuántas observaciones tenga la serie. ¿Cuántas hacen falta, como mínimo, para que quede fuera?',
        pista: 'La banda se estrecha al crecer $T$. Escribe la condición para que $0.15$ quede por fuera y despeja $T$; como $T$ cuenta observaciones, decide hacia dónde se redondea.',
        respuesta: 171,
        tolerancia: 0.5,
        retroAcierto: '$1.96/\\sqrt{T} &lt; 0.15$ equivale a $T &gt; (1.96/0.15)^2 = 170.7$: hacen falta 171 observaciones. La misma barra no dice nada en una serie de 100 datos (banda $\\pm 0.196$) y queda fuera en una de 400 (banda $\\pm 0.098$): la banda depende solo de $T$, no de la serie ni del rezago. Y quedar fuera por poco tampoco basta: de 24 barras, algo más de una se sale por azar.',
        retroFallo: 'Se despeja $T$ de $1.96/\\sqrt{T} &lt; 0.15$: $T &gt; (1.96/0.15)^2 = 170.7$, es decir, 171 observaciones. Si respondiste 13 o 14, te faltó elevar al cuadrado ($1.96/0.15 = 13.07$). Si respondiste 170, redondeaste hacia abajo: con 170 datos la banda vale $0.1503$, todavía por encima de $0.15$.'
      },
      {
        tipo: 'grafico',
        modulo: 7,
        alto: 210,
        descripcionGrafico: descripcionCorrelogramaQuiz('d_log_airpassengers',
          'la primera diferencia del logaritmo de AirPassengers'),
        pregunta: 'Este es el correlograma de $\\nabla \\log(y_t)$ para <code>AirPassengers</code>, es decir, la serie <strong>ya diferenciada una vez</strong>. ¿Qué te dice?',
        pista: 'No todas las barras que salen de la banda pesan lo mismo. Cuenta cuántas salen y mira en qué rezagos están las más altas antes de elegir.',
        dibujar: canvas => correlogramaDe(canvas, 'd_log_airpassengers', 'acf'),
        opciones: [
          {
            texto: 'Queda estacionalidad sin tratar: el pico del rezago 12 pide una diferencia estacional $\\nabla_{12}$.',
            correcta: true,
            retro: '$r_{12} = 0.841$, con una banda de $\\pm 0.164$. La diferencia regular se llevó la tendencia ($r_1 = 0.200$), pero el ciclo anual sigue intacto: cada mes se parece todavía al mismo mes del año anterior.'
          },
          {
            texto: 'Ya es ruido blanco: que alguna barra asome fuera de la banda es lo esperable por azar.',
            correcta: false,
            retro: 'Por azar se esperaría que una o dos de las 24 barras asomaran fuera de la banda. Aquí se salen 10 de 24, y la del rezago 12 muchísimo: $r_{12} = 0.841$ frente a una banda de $\\pm 0.164$.'
          },
          {
            texto: 'Falta otra diferencia regular: la ACF no decae y eso delata una raíz unitaria todavía sin tratar.',
            correcta: false,
            retro: 'La ACF sí decae en los primeros rezagos ($r_1 = 0.200$, ya cerca de la banda). Lo que sobresale es un pico aislado en el 12, que es la firma de la estacionalidad, no de una raíz unitaria. Diferenciar otra vez de forma regular solo sobrediferenciaría.'
          },
          {
            texto: 'Queda una tendencia determinista: hay que restar una recta en lugar de diferenciar más.',
            correcta: false,
            retro: 'Una tendencia sin quitar produce una ACF que decae lenta y casi linealmente desde $r_1 \\approx 1$. Aquí $r_1 = 0.200$: la tendencia ya se fue con la diferencia regular.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 7,
        pregunta: 'Aplicaste una diferencia regular a una serie y sospechas que sobraba. Marca <strong>todos</strong> los indicios que apoyan esa sospecha.',
        pista: 'Separa lo que se sabía de la serie <em>antes</em> de diferenciarla de lo que se ve <em>después</em>, y pregúntate de cada opción si ocurriría igual con una diferencia que sí hacía falta.',
        opciones: [
          {
            texto: 'La varianza de la serie subió al diferenciarla.',
            correcta: false,
            retro: 'La varianza sube o baja al diferenciar según $r_1$ sea menor o mayor que $0.5$, haga falta la diferencia o no: en el Módulo 7 sube de 1.096 a 1.513 con una que hacía falta y baja de 2.497 a 1.033 con una que sobraba.'
          },
          {
            texto: 'Antes de diferenciar, la ACF ya caía rápido y <code>ndiffs()</code> devolvía 0.',
            correcta: true,
            retro: 'Es el indicio que decide: si el correlograma y las pruebas de la serie de partida no pedían la diferencia, sobraba.'
          },
          {
            texto: 'En la ACF aparecen picos en los rezagos múltiplos del periodo estacional.',
            correcta: false,
            retro: 'Es la firma de una estacionalidad sin tratar: ahí falta una diferencia estacional, no sobra una regular.'
          },
          {
            texto: 'En la serie diferenciada aparece un $r_1$ negativo, cercano a $-0.5$.',
            correcta: true,
            retro: 'Es la huella de diferenciar algo que ya era casi ruido blanco: $\\nabla y_t = \\varepsilon_t - \\varepsilon_{t-1}$ tiene $\\rho_1 = -0.5$. Es un indicio y no una regla: el Módulo 7 muestra una serie en la que la diferencia hacía falta y $r_1$ queda en $-0.483$.'
          },
          {
            texto: 'El KPSS de la serie diferenciada ya no rechaza la estacionariedad.',
            correcta: false,
            retro: 'Eso pasa también cuando la diferencia hacía falta: es lo que ocurre con la TRM en el Módulo 6. Que la serie diferenciada sea estacionaria no dice si la de partida ya lo era.'
          }
        ],
        retroAcierto: 'El indicio que decide es que el correlograma y las pruebas no pidieran la diferencia. El $r_1$ cercano a $-0.5$ es su huella cuando lo diferenciado ya era casi ruido blanco: en log(<code>AirPassengers</code>), $r_1$ va $0.200 \\to -0.293 \\to -0.534$ al pasar de una a dos y a tres diferencias.',
        retroFallo: 'Los indicios son dos: que el correlograma y las pruebas de la serie de partida no pidieran la diferencia, y un $r_1$ cercano a $-0.5$ después de aplicarla. Lo que describen las otras opciones ocurre igual, o más, cuando la diferencia hacía falta.'
      },
      {
        tipo: 'opcion',
        modulo: 6,
        pregunta: 'Una serie mensual de 120 observaciones tiene tendencia y una estacionalidad marcada. Sin transformarla ni diferenciarla, <code>adf.test()</code> da $p &lt; 0.01$ y el KPSS de nivel da $p &lt; 0.01$. ¿Qué lectura es correcta?',
        pista: 'Escribe la hipótesis nula de cada prueba y, debajo, qué se concluye al rechazarla. Solo entonces compara las dos conclusiones.',
        opciones: [
          {
            texto: 'Las dos coinciden: la serie no es estacionaria y basta con diferenciarla una vez.',
            correcta: false,
            retro: 'Un p-valor pequeño no significa lo mismo en las dos. En el KPSS rechaza la estacionariedad; en el ADF rechaza la raíz unitaria, que es lo contrario de pedir una diferencia.'
          },
          {
            texto: 'Las dos coinciden: la serie es estacionaria alrededor de una tendencia lineal.',
            correcta: false,
            retro: 'Eso es lo que dice el ADF al rechazar la raíz unitaria, pero el KPSS de nivel rechaza la estacionariedad. No coinciden.'
          },
          {
            texto: 'Ninguna concluye: los datos son poco informativos y hay que conseguir más.',
            correcta: false,
            retro: 'Ese es el caso en que <em>ninguna</em> de las dos rechaza. Aquí rechazan las dos, cada una su hipótesis nula.'
          },
          {
            texto: 'Se contradicen: hay que revisar la especificación de las dos antes de concluir.',
            correcta: true,
            retro: 'El ADF rechaza la raíz unitaria y el KPSS rechaza la estacionariedad: es la cuarta fila de la tabla del Módulo 6. Aquí hay dos cosas que revisar. El KPSS de nivel no admite tendencia, y la serie la tiene. Y <code>adf.test()</code>, con 120 datos, usa por defecto $k = 4$ términos, menos que el periodo, 12: es la situación del caso tramposo.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 5,
        alto: 210,
        descripcionGrafico: descripcionCorrelogramaQuiz('caminata', 'la serie de la pregunta'),
        pregunta: 'Y este otro correlograma, ¿qué recomienda hacer con la serie?',
        pista: 'Compara la altura de la primera barra con la del rezago 12 y describe con tus palabras cómo se pasa de una a otra. Después busca esa descripción en la tabla del Módulo 3.',
        dibujar: canvas => correlogramaDe(canvas, 'caminata', 'acf'),
        opciones: [
          {
            texto: 'Nada: es una serie estacionaria, solo que con una memoria que tarda mucho en apagarse.',
            correcta: false,
            retro: 'Una serie estacionaria de memoria corta no llega al rezago 12 con $r_{12} = 0.488$: con $\\phi = 0.5$ quedaría en $0.5^{12} \\approx 0.0002$. Solo una muy persistente se le parecería —es el caso difícil del Módulo 5—, y ni entonces el correlograma permite quedarse sin hacer nada: manda diferenciar o, al menos, contrastar la raíz unitaria.'
          },
          {
            texto: 'Diferenciarla: un decaimiento tan lento y casi lineal delata una raíz unitaria.',
            correcta: true,
            retro: 'Es la ACF de una caminata aleatoria ($r_1 = 0.961$, $r_{12} = 0.488$). Como la dependencia se propaga en cadena, la ACF tarda muchísimo en bajar. Una sola diferencia la convierte en ruido blanco: pruébalo en el simulador del Módulo 5 poniendo $\\phi = 1$ y activando $\\nabla$.'
          },
          {
            texto: 'Tomar su logaritmo: la ACF muestra una dispersión que crece con el nivel.',
            correcta: false,
            retro: 'Una dispersión que crece con el nivel se ve en el gráfico de la serie, no en su ACF, y es un problema distinto: el logaritmo no quita una raíz unitaria.'
          },
          {
            texto: 'Modelarla como un MA(1): la ACF se corta después de los primeros rezagos.',
            correcta: false,
            retro: 'La ACF de un MA(1) se corta <em>de golpe</em> tras el rezago 1: una barra grande y el resto dentro de la banda. Esta no se corta, decae poquito a poco.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 7,
        pregunta: 'Una serie trimestral tiene 10 años de datos, $T = 40$. Se le aplican una diferencia estacional y una regular, $\\nabla\\nabla_4$. ¿Qué porcentaje de las observaciones se pierde?',
        pista: 'Cuenta primero cuántas observaciones se quedan sin con quién restarse en cada diferencia, y fíjate en cada cuánto se mide esta serie.',
        respuesta: 12.5,
        unidad: '%',
        tolerancia: 0.5,
        retroAcierto: '$\\nabla_4$ cuesta 4 observaciones y $\\nabla$ cuesta 1: quedan $40 - 5 = 35$ y se pierde $5/40 = 12.5\\,\\%$. El costo es absoluto y no proporcional: esas mismas 5 observaciones son el 4.6&nbsp;% de las 108 de <code>UKgas</code>.',
        retroFallo: 'Cada diferencia cuesta su rezago: $\\nabla_4$ quita 4 observaciones y $\\nabla$ quita 1. Se pierden 5 de 40, el $12.5\\,\\%$. Si respondiste 32.5, restaste 12 y 1 como si la serie fuera mensual; si respondiste 10 o 2.5, contaste solo una de las dos diferencias; si respondiste 35, diste las observaciones que quedan.'
      },
      {
        tipo: 'opcion',
        modulo: 8,
        pregunta: 'Para <code>UKgas</code>, la serie trimestral del Módulo 7, el criterio de Guerrero vale 0.792 sin transformar, 0.287 con el logaritmo y 0.084 en su óptimo, $\\lambda = -0.446$. ¿Qué lectura de esas tres cifras es correcta?',
        pista: 'Las tres cifras miden lo mismo, y menor es mejor. Ordénalas y pregúntate con cuál de las otras dos hay que comparar la del logaritmo para decir si ayuda, y con cuál para decir cuánto le falta.',
        opciones: [
          {
            texto: 'El logaritmo empeora la serie: su criterio es más del triple que el del óptimo.',
            correcta: false,
            retro: 'Para saber si el logaritmo ayuda hay que compararlo con no transformar, y ahí gana con claridad: el criterio baja de 0.792 a 0.287. Que quede lejos del óptimo dice cuánto le falta, no que empeore.'
          },
          {
            texto: 'El logaritmo capta el 36&nbsp;% de la mejora posible: apenas cambia la dispersión.',
            correcta: false,
            retro: '$0.287/0.792 = 0.36$ es lo que <em>queda</em> del criterio tras el logaritmo, no la parte de la mejora que capta. La mejora posible es el camino de 0.792 a 0.084, y el logaritmo recorre de 0.792 a 0.287.'
          },
          {
            texto: 'Un $\\lambda$ negativo dice que la dispersión baja con el nivel: no hay que transformar.',
            correcta: false,
            retro: 'Al contrario: cuanto menor es $\\lambda$, más se comprimen los valores grandes. Un óptimo por debajo de 0 pide comprimir <em>más</em> que el logaritmo, porque la dispersión crece con el nivel más deprisa de lo que el logaritmo corrige.'
          },
          {
            texto: 'El logaritmo capta el 71&nbsp;% de la mejora posible y deja amplitud sin estabilizar.',
            correcta: true,
            retro: '$(0.792 - 0.287)/(0.792 - 0.084) = 0.71$. En <code>AirPassengers</code> el logaritmo captaba el 84&nbsp;%; aquí se queda más lejos, y se nota: en $\\log$(<code>UKgas</code>) la desviación de cada año pasa de 0.26 en los tres primeros a más de 0.5 en los tres últimos. El logaritmo sigue siendo la elección del curso, porque se puede interpretar, pero el paso 2 del pipeline pide comprobar lo que deja.'
          }
        ]
      }
    ];
"""


def aplica(src):
    ini = src.index("    AUTOEVALUACIONES['cap2'] = [")
    fin = src.index("    ];\n", ini) + len("    ];\n")
    return src[:ini] + QUIZ + src[fin:]
