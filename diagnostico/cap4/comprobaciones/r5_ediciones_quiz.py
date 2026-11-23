#!/usr/bin/env python3
"""R5 del capítulo 4 · T5.2: `AUTOEVALUACIONES['cap4']` (ensamblado/cap4/chapter.js).

No se ejecuta solo: lo importa `r5_edita.py`. No toca `SIMULACROS['cap4-simulacro']` ni el motor.

El texto se escribe aquí con LaTeX normal (una barra) y `js()` lo convierte en un literal de
JavaScript entre comillas simples (dobla las barras y escapa las comillas). Las cifras salen de
`r5_cifras.out`; la etiqueta de cada una va en el comentario de su pregunta.
"""


def js(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def opcion(texto, correcta, retro):
    return ("          {\n"
            f"            texto: {js(texto)},\n"
            f"            correcta: {'true' if correcta else 'false'},\n"
            f"            retro: {js(retro)}\n"
            "          }")


def opciones(lista):
    return "        opciones: [\n" + ",\n".join(opcion(*o) for o in lista) + "\n        ]\n"


# ------------------------------------------------------------------------------------------- P1 · M6
P1 = ("      {\n"
      "        tipo: 'opcion',\n"
      "        modulo: 6,\n"
      "        pregunta: " + js(r'Sobre los pasajeros aéreos anuales de Australia entre 1970 y 2016 ($n = 47$), el mejor ARIMA sin constante de la rejilla con $d = 1$ tiene AICc $= 204.28$, y el mejor con $d = 2$, AICc $= 198.32$. ¿Qué dice esa comparación sobre $d$?') + ",\n"
      "        pista: " + js(r'Mira de dónde sale un AICc: vuelve a su fórmula en el Módulo 6 y sigue qué cambia en ella al pasar de $d = 1$ a $d = 2$.') + ",\n"
      + opciones([
          (r'Que conviene $d = 2$: seis puntos de AICc son una diferencia clara entre dos modelos.', False,
           r'Seis puntos serían una diferencia clara dentro de un mismo $d$. Aquí no: el segundo AICc es la verosimilitud de <strong>otros datos</strong>, con una observación menos, y un valor menor no significa un modelo mejor.'),
          (r'Nada: cada AICc se calcula sobre datos distintos, y solo se comparan con un mismo $d$.', True,
           r'El primero se calcula sobre $n^{*} = 46$ diferencias y el segundo sobre $45$ segundas diferencias: <strong>datos distintos</strong>. En esta serie la duda sobre $d$ es real —KPSS pide dos diferencias, y ADF y PP, una—, pero no se resuelve restando dos AICc.'),
          (r'Que conviene $d = 1$: a igualdad de ajuste, se prefiere el modelo con menos diferencias.', False,
           r'No diferenciar más de lo necesario es una cautela razonable, y el Módulo 8 explica por qué. Pero no sale de esta comparación: aquí no hay «igualdad de ajuste» que valorar, porque los dos AICc no miden lo mismo.'),
          (r'Que hay que decidir con el BIC, que penaliza más y sí se compara entre distintos $d$.', False,
           r'El BIC tiene el mismo problema: también parte de $-2\log L$, y esa verosimilitud se calcula sobre $n^{*} = n - d$ observaciones. Cambiar de criterio no arregla que los datos sean distintos.'),
      ]) +
      "      }")

# ------------------------------------------------------------------------------------------- P2 · M9
P2 = ("      {\n"
      "        tipo: 'numerica',\n"
      "        modulo: 9,\n"
      "        pregunta: " + js(r'Un ARIMA($1,1,0$) tiene $\phi = 0.5$ y $\sigma = 2$. ¿Cuánto vale $\sigma_3$, la desviación típica del error de pronóstico a tres pasos? Da dos decimales.') + ",\n"
      "        pista: " + js(r'Para los pesos $\psi$, escribe primero el modelo sobre $y_t$, como en el desarrollo del Módulo 1, y cuenta cuántos pesos entran en $\sigma_3$. Conserva al menos tres decimales en los pasos intermedios.') + ",\n"
      "        respuesta: 5.02,\n"
      "        tolerancia: 0.011,\n"
      "        retroAcierto: " + js(r'Sobre $y_t$ el modelo es un AR(2) con $\phi^{*} = (1.5,\ -0.5)$, así que $\psi_0 = 1$, $\psi_1 = 1.5$ y $\psi_2 = 1.5 \times 1.5 - 0.5 = 1.75$. Entonces $\sigma_3 = 2\sqrt{1 + 1.5^2 + 1.75^2} = 2\sqrt{6.3125} = 5.02$.') + ",\n"
      "        retroFallo: " + js(r'Sobre $y_t$ el modelo es un AR(2) con $\phi^{*} = (1.5,\ -0.5)$: $\psi_0 = 1$, $\psi_1 = 1.5$ y $\psi_2 = 1.75$, y $\sigma_3 = 2\sqrt{1 + 2.25 + 3.0625} = 5.02$. Si te salió $2.29$, usaste $\psi_j = \phi^{\,j}$, los pesos del AR(1) sin la diferencia; $3.46$ es tomar todos los pesos iguales a $1$; $4.61$, olvidar $\psi_0$; $4.12$, sumar los pesos sin elevarlos al cuadrado; $6.27$, sumar un peso de más, $\psi_3$; $2.51$, olvidar $\sigma$; y $5.00$, redondear la raíz a $2.5$ antes de multiplicar.') + "\n"
      "      }")

# ------------------------------------------------------------------------------------------- P3 · M10
P3 = ("      {\n"
      "        tipo: 'grafico',\n"
      "        modulo: 10,\n"
      "        alto: 250,\n"
      "        descripcionGrafico: describirBarrasQuiz(\n"
      "          'Función de autocorrelación de los residuales de un ARIMA ajustado a una serie mensual',\n"
      "          PUENTE.no_estacional.acf_residuales, PUENTE.no_estacional.banda),\n"
      "        pregunta: " + js(r'Esta es la ACF de los residuales de un ARIMA ajustado a una serie mensual. ¿Qué hay que hacer?') + ",\n"
      "        pista: " + js(r'No te quedes en cuántas barras salen de la banda: fíjate en cuáles son.') + ",\n"
      "        dibujar: canvas => crearGraficoBarras(canvas,\n"
      "          etiquetasRezago(PUENTE.no_estacional.acf_residuales.length),\n"
      "          PUENTE.no_estacional.acf_residuales, {\n"
      "            etiqueta: 'ACF de los residuales', color: '#b91c1c',\n"
      "            lineas: lineasBanda(PUENTE.n), tituloX: 'Rezago k'\n"
      "          }),\n"
      + opciones([
          (r'Aumentar $q$ hasta que todas las barras queden dentro de la banda de confianza.', False,
           r'Funcionaría en el sentido técnico, pero haría falta $q = 24$ para alcanzar el rezago 24: veinticuatro parámetros para describir un patrón que se repite cada doce meses. Un modelo estacional recoge lo mismo con dos.'),
          (r'Diferenciar una vez más: una autocorrelación tan alta indica no estacionariedad.', False,
           r'Diferenciar de nuevo en el rezago 1 no toca el patrón de los rezagos 12 y 24, y además puede dejar en el MA la raíz unitaria que estudió el Módulo 8. Lo que hace falta aquí es una diferencia <strong>estacional</strong>, $\nabla_{12}$, que es otra cosa.'),
          (r'Pasar a un modelo estacional: lo que sobra está en los rezagos múltiplos de 12.', True,
           r'$\hat\rho_{12} = 0.72$ y $\hat\rho_{24} = 0.67$, frente a una banda de $0.163$: la estructura que sobra es estacional. Subir $q$ hasta 24 la cubriría con dos docenas de parámetros; un SARIMA lo hace con dos. Es el Capítulo 5.'),
          (r'Nada: casi todas las barras están dentro de la banda, y el modelo es adecuado.', False,
           r'Contar cuántas barras se salen no basta, y aquí las que se salen lo hacen por un factor de cuatro. Ljung–Box(24) da $Q = 222.4$ con $p < 10^{-6}$: el rechazo es rotundo. Un patrón sistemático en pocos rezagos es peor señal que ruido repartido en muchos.'),
      ]) +
      "      }")

# ------------------------------------------------------------------------------------------- P4 · M5
P4 = ("      {\n"
      "        tipo: 'multiple',\n"
      "        modulo: 5,\n"
      "        pregunta: " + js(r'Marca <strong>todas</strong> las afirmaciones correctas sobre la constante de un modelo ARIMA.') + ",\n"
      "        pista: " + js(r'Para cada afirmación, piensa qué grado tiene la tendencia que genera la constante con ese $d$, y qué le pasa al pronóstico cuando la constante no está.') + ",\n"
      + opciones([
          (r'Con $d = 1$, la deriva $\mu_w = c/\phi(1)$ es el incremento medio por período: una tendencia lineal.', True,
           r'Tomando esperanzas en la ecuación, $\mu_w = c/\phi(1)$ es la media de $\nabla y_t$: lo que la serie sube o baja en promedio cada período, es decir, una pendiente. Es lo que <code>forecast</code> llama deriva.'),
          (r'Sin constante, un modelo con $d = 2$ pronostica a largo plazo una parábola, no una línea recta.', False,
           r'Sin constante, con $d = 2$ el pronóstico acaba en una recta: la segunda diferencia del pronóstico tiende a cero. La parábola necesitaría una constante con $d = 2$.'),
          (r'Con $d = 1$ y sin deriva, el pronóstico se aplana en un nivel, que puede no ser el último dato.', True,
           r'Sin deriva no hay pendiente a largo plazo y el pronóstico se aplana; pero la parte ARMA lo mueve durante unos pasos, y el nivel al que llega no es, en general, el último dato. En el Nilo parte de $740$ y se aplana en $842.17$.'),
          (r'Con $d \ge 2$, <code>forecast::Arima</code> avisa y no ajusta la deriva, aunque se le pida.', True,
           r'Es lo que hace: avisa de que no ajusta la deriva con dos o más diferencias. Una constante con $d = 2$ generaría una tendencia cuadrática, y el Módulo 5 explica por qué no conviene extrapolarla.'),
          (r'En un ARIMA($p,0,q$), el <code>intercept</code> que da R es la constante $c$ de la ecuación, no la media.', False,
           r'Es al revés: lo que R llama <code>intercept</code> en un modelo con $d = 0$ es la media $\mu$ del proceso. La constante de la ecuación es $c = \mu\,\phi(1)$, y solo coinciden si $p = 0$.'),
      ])[:-1] + ",\n"
      "        retroAcierto: " + js(r'Las que hablan de la deriva con $d = 1$, del pronóstico que se aplana y de lo que hace <code>forecast::Arima</code> con $d \ge 2$. Las dos falsas son las que el capítulo desmiente midiendo: con $d = 2$ y sin constante el pronóstico termina en una <strong>recta</strong>, y el <code>intercept</code> de R <strong>es</strong> la media del proceso, pese al nombre.') + ",\n"
      "        retroFallo: " + js(r'Las correctas son las que hablan de la deriva con $d = 1$, del pronóstico que se aplana cuando no hay deriva y de lo que hace <code>forecast::Arima</code> con $d \ge 2$. Abajo va la explicación de cada opción que quedó mal juzgada.') + "\n"
      "      }")

# ------------------------------------------------------------------------------------------- P5 · M3
P5 = ("      {\n"
      "        tipo: 'opcion',\n"
      "        modulo: 3,\n"
      "        pregunta: " + js(r'<code>beaver2</code> trae la temperatura corporal de un castor medida cada 10 minutos (100 lecturas). Desde la lectura 39, cuando el animal sale de su refugio, la media sube unos $0.8$ °C. Sobre la serie completa, KPSS rechaza la estacionariedad ($p < 0.01$) y ADF no rechaza la raíz unitaria ($p = 0.57$). ¿Qué conviene hacer antes de fijar $d$?') + ",\n"
      "        pista: " + js(r'Repasa en el Módulo 3 qué contrasta cada prueba y qué le pasó a cada una en el experimento del cambio de nivel.') + ",\n"
      + opciones([
          (r'Diferenciar una vez: las dos pruebas coinciden, y eso cierra la discusión sobre $d$.', False,
           r'Que coincidan no las hace fiables aquí. El experimento del Módulo 3 mostró que un escalón hace rechazar a KPSS y también impide rechazar al ADF de <code>adf.test</code>: con el salto dentro, las dos pueden estar respondiendo al escalón y no a una raíz unitaria.'),
          (r'Ajustar el salto como un escalón y volver a examinar lo que queda de la serie.', True,
           r'Con el salto dentro, las pruebas no separan una raíz unitaria de un cambio de nivel (Módulo 3). Quitado el escalón ($0.81$ °C), lo que queda sigue muy autocorrelacionado ($r_1 = 0.78$), y probadas en cada tramo, a un lado y otro de la lectura 39, las tres pruebas siguen pidiendo una diferencia: la discusión sobre $d$ no termina ahí, pero ya es sobre la serie, y no sobre el salto.'),
          (r'Diferenciar dos veces: una diferencia para la raíz unitaria y otra para el salto.', False,
           r'Una sola diferencia ya convierte un escalón en un único valor atípico: no hace falta otra para «quitarlo». Y diferenciar de más deja una raíz unitaria en la parte MA (Módulo 8). Antes de subir $d$ conviene volver al gráfico.'),
          (r'No diferenciar: un salto con causa conocida prueba que no hay raíz unitaria.', False,
           r'El salto puede bastar para que KPSS rechace, pero no dice nada de lo que hay a cada lado: quitado el escalón, lo que queda tiene $r_1 = 0.78$ y hay que examinarlo. Fijar $d = 0$ sin mirarlo es el mismo error que diferenciar sin mirar el gráfico, en sentido contrario.'),
      ]) +
      "      }")

# ------------------------------------------------------------------------------------------- P6 · M4
P6 = ("      {\n"
      "        tipo: 'grafico',\n"
      "        modulo: 4,\n"
      "        alto: 250,\n"
      "        descripcionGrafico: describirBarrasQuiz('Función de autocorrelación muestral de una serie anual sin diferenciar',\n"
      "          ACF_P6, banda(N_P6)),\n"
      "        pregunta: " + js(r'Esta es la ACF de las exportaciones de bienes y servicios de Chile, en porcentaje del PIB (58 datos anuales, de 1960 a 2017), <strong>sin diferenciar</strong>. ¿Qué se puede concluir sobre $p$ y $q$?') + ",\n"
      "        pista: " + js(r'Antes de contar barras, mira la forma en que bajan.') + ",\n"
      "        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS, ACF_P6, {\n"
      "          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,\n"
      "          lineas: lineasBanda(N_P6), tituloX: 'Rezago k'\n"
      "        }),\n"
      + opciones([
          (r'Que es un AR de orden alto, porque hay muchas barras fuera de la banda.', False,
           r'Un AR estacionario tiene una ACF que decae, de forma exponencial u oscilante (Capítulo 3), y esa lectura presupone que la serie es estacionaria. Con una caída tan lenta, lo primero es preguntarse si el nivel de la serie se mueve: leer órdenes aquí es confundir la no estacionariedad con dinámica.'),
          (r'Que es un MA($q$), con $q$ igual al número de barras fuera de la banda.', False,
           r'Un MA($q$) tiene la ACF teórica nula después del rezago $q$: un corte, no un descenso gradual. Aquí no hay corte por ninguna parte.'),
          (r'Que hace falta $d = 2$, porque las barras tardan más de diez rezagos en entrar.', False,
           r'Que la serie no parezca estacionaria es razonable, pero la ACF no dice cuántas diferencias hacen falta: la lentitud de la caída no mide $d$. Eso lo deciden el gráfico, las pruebas y los síntomas de haber diferenciado de más (Módulo 3).'),
          (r'Nada todavía: una caída tan lenta obliga a decidir $d$ antes de leer $p$ y $q$.', True,
           r'Una ACF que baja despacio y sin cortar —aquí $0.946,\ 0.868,\ 0.802,\dots$, fuera de la banda hasta el rezago 12— es compatible con una serie no estacionaria. La tabla de identificación se lee sobre la serie ya estacionaria: primero se decide $d$, y después se leen $p$ y $q$ en la ACF y la PACF de la serie diferenciada. Con $d = 1$, en esta serie solo sale de la banda el rezago 1 ($0.270$).'),
      ]) +
      "      }")

# ------------------------------------------------------------------------------------------- P7 · M7
P7 = ("      {\n"
      "        tipo: 'opcion',\n"
      "        modulo: 7,\n"
      "        pregunta: " + js(r'Sobre esa misma serie de exportaciones de Chile, <code>auto.arima</code> devuelve un ARIMA($0,1,2$) con deriva, AICc $265.85$. La búsqueda exhaustiva encuentra un ARIMA($0,1,1$) sin deriva con AICc $264.32$, y su tercer clasificado tiene $266.26$. ¿Qué se concluye?') + ",\n"
      "        pista: " + js(r'Mide primero cuánto separa el AICc a esos tres modelos, y busca en el Módulo 7 qué hace el capítulo con distancias de ese tamaño.') + ",\n"
      + opciones([
          (r'Que la búsqueda escalonada falló, y su modelo debe sustituirse por el de la exhaustiva.', False,
           r'La escalonada explora un vecindario y no garantiza el mínimo: aquí se quedó a $1.53$ puntos de él, y por eso conviene contrastarla con la exhaustiva. Pero una distancia así no descarta a nadie: este capítulo toma por convención que diferencias menores que $2$ puntos no distinguen modelos.'),
          (r'Que el ARIMA($0,1,1$) es el modelo verdadero, porque es el mínimo de la búsqueda completa.', False,
           r'Ser el mínimo de la búsqueda completa dice que es el mejor según el AICc de los que la búsqueda pudo ajustar, no que sea el verdadero. Y hay otro modelo a $1.53$ puntos y otro a $1.94$: el criterio apenas los separa.'),
          (r'Que hay tres modelos que el AICc apenas separa, y conviene decirlo al dar el resultado.', True,
           r'Del primero al tercero hay $1.94$ puntos, menos de los $2$ que este capítulo toma por convención como indistinguibles. La salida de una línea de <code>auto.arima</code> no comunica esa incertidumbre; <code>trace = TRUE</code> sí.'),
          (r'Que, con menos de $2$ puntos entre ellos, se elige sin más el de menos parámetros de los tres.', False,
           r'La parsimonia es un criterio razonable para desempatar, y llevaría al ARIMA($0,1,1$), que es defendible. Pero lo primero es <strong>reconocer que hay un empate</strong>: elegir por parsimonia sin decir que había tres candidatos oculta la misma incertidumbre.'),
      ]) +
      "      }")

# ------------------------------------------------------------------------------------------- P8 · M8
P8 = ("      {\n"
      "        tipo: 'opcion',\n"
      "        modulo: 8,\n"
      "        pregunta: " + js(r'Importaciones de bienes y servicios de Perú, en porcentaje del PIB (58 datos anuales). Un MA(1) sin media ajustado a $\nabla y_t$ da $\hat\theta = -0.288$ y pasa Ljung–Box(10) ($p = 0.43$). Ajustado a $\nabla^2 y_t$ da $\hat\theta = -1.000$ y también lo pasa ($p = 0.17$). La varianza de $\nabla y_t$ es $5.12$, y la de $\nabla^2 y_t$, $13.18$. ¿Qué se concluye sobre $d$?') + ",\n"
      "        pista: " + js(r'Los dos modelos pasan Ljung–Box. Repasa todo lo que el Módulo 8 enseña a mirar en un modelo ajustado.') + ",\n"
      + opciones([
          (r'Que $d = 2$ sobra: con $\hat\theta = -1$, la raíz MA cae sobre el círculo y deshace la diferencia.', True,
           r'La raíz de $1 + \hat\theta B$ es $-1/\hat\theta$, de módulo $1.000$ con tres decimales: el polinomio MA es, en la práctica, $(1 - B)$, el mismo operador de diferencia, y cancela la segunda. Hay una comprobación: el $\hat\sigma^2$ de ese MA(1) es $5.12$, la varianza de $\nabla y_t$. El modelo ha vuelto a la serie diferenciada una sola vez.'),
          (r'Que $d = 2$ también es válido: sus residuales pasan Ljung–Box, igual que los de $d = 1$.', False,
           r'Pasar Ljung–Box no basta: un modelo con una diferencia de más puede dejar residuales sin estructura, porque su parte MA deshace la diferencia que sobra. El diagnóstico incluye las raíces, y la de este MA(1) tiene módulo $1.000$.'),
          (r'Que $d = 1$ es mejor, porque con la segunda diferencia la varianza sube de $5.12$ a $13.18$.', False,
           r'La conclusión es la buena y el argumento no sirve. Que la varianza suba o baje al diferenciar repite lo que dice $r_1$ (Módulo 2.7) y no decide $d$: hay series estacionarias en las que diferenciar reduce la varianza. Lo que delata la diferencia sobrante es la raíz MA sobre el círculo.'),
          (r'Que hay que comparar el AICc de los dos modelos y quedarse con el $d$ del menor.', False,
           r'Los AICc de modelos con distinto $d$ no se comparan: uno se calcula sobre $57$ observaciones y el otro sobre $56$ (Módulo 6). Y aquí no hace falta ningún criterio: $\hat\theta = -1$ ya dice que la segunda diferencia sobra.'),
      ]) +
      "      }")

DATOS = '''    // ACF de la pregunta 6 de la autoevaluación: exportaciones de bienes y servicios de Chile
    // (% del PIB, 1960-2017; tsibbledata::global_economy), sin diferenciar, rezagos 1 a 20.
    // Salen de diagnostico/cap4/comprobaciones/r5_cifras.R, etiqueta [P6-01].
    const ACF_P6 = [0.946, 0.868, 0.802, 0.734, 0.662, 0.593, 0.526, 0.469, 0.429, 0.392,
      0.344, 0.291, 0.238, 0.198, 0.178, 0.164, 0.137, 0.100, 0.070, 0.039];
    const N_P6 = 58;

    // Autoevaluación del capítulo (ronda R5, 2026-11-23). Procedencia de las cifras, en
    // diagnostico/cap4/comprobaciones/r5_cifras.out: P1, etiquetas P1-01 a P1-03 (pasajeros aéreos
    // de Australia, fpp3::aus_airpassengers); P2, P2-01 a P2-03; P5, P5-01 a P5-04 (datasets::beaver2);
    // P6 y P7, P6-01 a P7-03 (exportaciones de Chile); P8, P8-01 a P8-04 (importaciones de Perú).
    // Las de la P3 son las del puente al Capítulo 5 y las del Nilo de la P4, las del Módulo 9.
'''


def aplica(fuente):
    ini = fuente.index("    AUTOEVALUACIONES['cap4'] = [")
    fin = fuente.index("\n    ];\n", ini) + len("\n    ];\n")
    nuevo = (DATOS + "    AUTOEVALUACIONES['cap4'] = [\n" +
             ",\n".join([P1, P2, P3, P4, P5, P6, P7, P8]) + "\n    ];\n")
    return fuente[:ini] + nuevo + fuente[fin:]
