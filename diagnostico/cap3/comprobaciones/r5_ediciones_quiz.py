#!/usr/bin/env python3
r"""R5 del capítulo 3 · T5.2: `AUTOEVALUACIONES['cap3']` entero, y dos cadenas del simulador de los psi.

No se ejecuta solo: lo importa `r5_edita.py`, que lo aplica sobre `ensamblado/cap3/cap3_js.js`.
`AUTOEVALUACIONES['parcial2']` y `SIMULACROS` no se tocan (vienen de un banco fuera del repo).

Qué cambia en cada pregunta (el detalle, en `R5_cambios.md` §2):
  P1  opciones del mismo cuerpo; pista sin la regla.
  P2  REHECHA: gamma_1 de un MA(2) nuevo (antes, rho_1 del MA(1) con theta = 0.8, en pantalla).
  P3  la retro ya no da las cifras del MA(2) theta = (0.6, 0.4); opciones y pista.
  P4  REHECHA con otro ARMA(1,1): phi = 0.6, theta = -0.3, sigma2 = 5.
  P5  REHECHA sobre un MA(1) concreto (theta = -2.5); retro por opción; «por defecto».
  P6  la salida de arima() es ahora real (set.seed(329), [Q6-01]); opciones y pista.
  P7  REHECHA con otro AR(2), phi = (0.9, -0.5); pasa a etiquetarse como Módulo 2.
  P8  opciones del mismo cuerpo; pista.
  P9  opciones del mismo cuerpo; pista.
  P10 retro por opción; Yule-Walker como lo dice la prosa; pista.
Las cifras que no están bajo un `#>` del capítulo llevan su etiqueta de `r5_cifras.out` en el
comentario que precede a cada pregunta.
"""

QUIZ = r"""    // R5 (2026-11-21). De dónde sale cada cifra que no está bajo un `#>` del capítulo
    // (etiquetas de diagnostico/cap3/comprobaciones/r5_cifras.out):
    //   P1 [Q1-01] · P2 [Q2-01] a [Q2-03] · P4 [Q4-01], [Q4-02] · P5 [Q5-01] a [Q5-03]
    //   P6 [Q6-01] a [Q6-04]: la salida es real, set.seed(329) y
    //      arima(rnorm(100), order = c(1, 0, 1), method = "ML")
    //   P7 [Q7-01], [Q7-02] · P9 [Q9-01]
    // El motor no baraja las opciones: la posición de la correcta la vigila
    // precalculo/audita_posicion_correcta.py.
    AUTOEVALUACIONES['cap3'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'Un AR(2) tiene $\\phi(B) = 1 - 1.2B + 0.9B^2$ y sus raíces tienen módulo $1.054$. ¿Es estacionario?',
        pista: 'Sitúa un número de módulo $1.054$ respecto del círculo unitario. Después relee, en la definición del Módulo 1, a qué lado del círculo tienen que quedar las raíces de $\\phi(B)$, y por qué ese lado sorprende la primera vez.',
        opciones: [
          {
            texto: 'No: para ser estacionario, sus raíces tendrían que caer dentro del círculo unitario.',
            correcta: false,
            retro: 'Es al revés, y es la confusión más común del capítulo. El polinomio está escrito en $B$, no en $1/B$: para el AR(1) la raíz es $1/\\phi$, así que $|\\phi| < 1$ equivale a $|1/\\phi| > 1$, es decir, raíz <strong>fuera</strong> del círculo.'
          },
          {
            texto: 'No: $\\phi_1 + \\phi_2 = -0.3$ es negativo, y con esa suma el proceso no puede ser estable.',
            correcta: false,
            retro: 'Cuidado con los signos del convenio: en $\\phi(B) = 1 - \\phi_1 B - \\phi_2 B^2$ los coeficientes van restando, así que aquí $\\phi_1 = 1.2$ y $\\phi_2 = -0.9$, y su suma es $0.3$. Además, el signo de esa suma no decide nada por sí solo.'
          },
          {
            texto: 'No se puede saber: falta conocer $\\sigma^2$, la varianza del ruido blanco que lo alimenta.',
            correcta: false,
            retro: 'La varianza del ruido no interviene: escala la serie, pero no cambia si el proceso olvida o no su pasado. Eso lo deciden únicamente las raíces de $\\phi(B)$.'
          },
          {
            texto: 'Sí: el módulo es mayor que 1, así que las raíces caen fuera del círculo unitario.',
            correcta: true,
            retro: 'La condición es $|B_i| > 1$ para todas las raíces. $1.054 > 1$, aunque por poco: es un proceso muy persistente, cerca de la frontera de la no estacionariedad.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 3,
        pregunta: 'Un MA(2) es $y_t = \\varepsilon_t + 0.6\\,\\varepsilon_{t-1} - 0.3\\,\\varepsilon_{t-2}$, con $\\sigma^2 = 4$. ¿Cuánto vale su autocovarianza de orden 1, $\\gamma_1 = \\operatorname{Cov}(y_t,\\,y_{t-1})$? Da dos decimales.',
        pista: 'Escribe $y_t$ e $y_{t-1}$ una debajo de la otra, cada una con sus tres choques, y marca los que aparecen en las dos: solo esos aportan a la covarianza. Vigila el signo de cada peso y no olvides $\\sigma^2$.',
        respuesta: 1.68,
        tolerancia: 0.006,
        retroAcierto: '$y_t$ e $y_{t-1}$ comparten dos choques: $\\varepsilon_{t-1}$, con pesos $0.6$ y $1$, y $\\varepsilon_{t-2}$, con pesos $-0.3$ y $0.6$. Entonces $\\gamma_1 = 4\\,(0.6 - 0.18) = 1.68$. Dos observaciones separadas por más de dos periodos ya no comparten ninguno: es la memoria finita del MA.',
        retroFallo: 'Es $\\gamma_1 = \\sigma^2(\\theta_1 + \\theta_1\\theta_2) = 4\\,(0.6 - 0.18) = 1.68$: $y_t$ e $y_{t-1}$ comparten los choques $\\varepsilon_{t-1}$ y $\\varepsilon_{t-2}$, y cada uno aporta el producto de sus dos pesos por $\\sigma^2$. Cada tropiezo habitual deja una cifra distinta: $2.40$ es contar solo el choque $\\varepsilon_{t-1}$; $0.42$, olvidar $\\sigma^2$; $3.12$, perder el signo de $\\theta_2$; $0.29$ es $\\rho_1$, la autocorrelación y no la autocovarianza; y $-1.20$ es $\\gamma_2$.'
      },
      {
        tipo: 'grafico',
        modulo: 5,
        alto: 200,
        descripcionGrafico: describirBarrasQuiz('Función de autocorrelación teórica de un proceso',
          PROCESOS.ma2.acf_teorica),
        pregunta: 'Esta es la ACF <strong>teórica</strong> de un proceso, y su PACF (no mostrada) decae sin cortarse. ¿De qué proceso se trata?',
        pista: 'Describe cada función con una frase: ¿termina de golpe o se va apagando? Con esas dos frases delante, busca la fila que les corresponde en la tabla del Módulo 5.',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS_T, PROCESOS.ma2.acf_teorica, {
          etiqueta: 'ACF teórica', color: COLORES_GRAFICO.primario, tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Un AR(2): hay dos barras distintas de cero, así que $p = 2$.',
            correcta: false,
            retro: 'Contar barras no basta: hay que mirar cuál de las dos funciones se corta. En un AR(2) es la <strong>PACF</strong> la que cae a cero tras el rezago 2, mientras la ACF decae sin cortarse nunca. Aquí ocurre justo lo contrario.'
          },
          {
            texto: 'Un MA(2): la ACF se corta tras el rezago 2 y la PACF decae.',
            correcta: true,
            retro: 'En un MA($q$), dos observaciones separadas por más de $q$ periodos no comparten ningún choque: por eso la ACF vale <strong>exactamente</strong> cero desde el rezago 3, y el corte en el rezago 2 da $q = 2$. La PACF, en cambio, decae sin cortarse.'
          },
          {
            texto: 'Un ARMA(2,2): hay dos rezagos activos en cada una de las dos.',
            correcta: false,
            retro: 'En un ARMA mixto <strong>ninguna</strong> de las dos funciones se corta: las dos decaen. Un corte limpio y exacto como este descarta precisamente el modelo mixto.'
          },
          {
            texto: 'Ruido blanco con dos autocorrelaciones altas por puro azar.',
            correcta: false,
            retro: 'Es una ACF <strong>teórica</strong>, calculada con <code>ARMAacf()</code>: no hay azar en ella. Y el ruido blanco tendría todas las autocorrelaciones nulas, incluidas las dos primeras.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 4,
        pregunta: 'Un ARMA(1,1) tiene $\\phi = 0.6$, $\\theta = -0.3$ y $\\sigma^2 = 5$. ¿Cuánto vale la varianza del error de pronóstico a dos pasos, $\\operatorname{Var}(e_{T+2})$? Da dos decimales.',
        pista: 'Calcula primero los pesos $\\psi$ que hacen falta con la recursión del Módulo 4, vigilando el signo de $\\theta$. Después decide cuántos pesos entran en la suma cuando $h = 2$ y qué factor la multiplica.',
        respuesta: 5.45,
        tolerancia: 0.006,
        retroAcierto: '$\\psi_1 = \\theta + \\phi = 0.3$, así que $\\operatorname{Var}(e_{T+2}) = 5\\,(1 + 0.3^2) = 5 \\times 1.09 = 5.45$. A un paso sería solo $\\sigma^2 = 5$: el pronóstico a dos pasos arrastra además el choque de $T+1$, que aquí pesa poco porque $\\phi$ y $\\theta$ tienen signos opuestos.',
        retroFallo: 'Es $\\sigma^2(\\psi_0^2 + \\psi_1^2) = 5\\,(1 + 0.3^2) = 5.45$, con $\\psi_1 = \\theta + \\phi = 0.3$. Cada tropiezo habitual deja una cifra distinta: $1.09$ es olvidar $\\sigma^2$; $0.45$, olvidar $\\psi_0 = 1$; $6.80$, tomar $\\psi_1 = \\phi$ como si fuera un AR(1); $9.05$, perder el signo de $\\theta$ y tomar $\\psi_1 = 0.9$; $6.50$, sumar los $\\psi$ sin elevarlos al cuadrado; y $5.61$, sumar hasta $j = h$ en vez de hasta $h - 1$.'
      },
      {
        tipo: 'multiple',
        modulo: 3,
        pregunta: 'Se simula una serie larga de un MA(1) con $\\theta = -2.5$ y $\\sigma^2 = 1$, y se le ajusta un MA(1) con <code>arima()</code>. Marca <strong>todas</strong> las afirmaciones correctas.',
        pista: 'Separa las dos propiedades del capítulo y qué polinomio responde por cada una. Después escribe $\\gamma_0$ y $\\gamma_1$ del proceso simulado y busca qué otro par $(\\theta,\\ \\sigma^2)$ da exactamente las mismas.',
        opciones: [
          {
            texto: 'La serie simulada no es estacionaria, porque $|\\theta|$ es mayor que 1.',
            correcta: false,
            retro: 'Un MA($q$) es estacionario para cualquier valor de sus $\\theta$: es una suma finita de ruido blanco. Lo que $|\\theta| > 1$ estropea es la invertibilidad, que se lee en $\\theta(B)$ —su raíz, $0.4$, cae dentro del círculo unitario—, no la estacionariedad.'
          },
          {
            texto: 'Su $\\rho_1$ coincide con la de otro MA(1), el que tiene $\\theta = -0.4$.',
            correcta: true,
            retro: '$-2.5/(1 + 2.5^2) = -0.4/(1 + 0.4^2) = -0.3448$: $\\theta$ y $1/\\theta$ comparten ACF, así que ningún correlograma los distingue.'
          },
          {
            texto: 'Sus pesos $\\pi$ se apagan con el rezago, porque $|\\rho_1|$ no llega a $0.5$.',
            correcta: false,
            retro: 'Con $\\theta = -2.5$ los pesos son $\\pi_j = (-\\theta)^j$: $2.5$, $6.25$, $15.625$… Crecen sin límite, que es lo que significa no ser invertible. Que $|\\rho_1|$ quede por debajo de $0.5$ no dice nada: le pasa a todo MA(1) con $|\\theta| \\ne 1$.'
          },
          {
            texto: 'Con sus opciones por defecto, <code>arima()</code> devolverá un $\\hat\\theta$ cercano a $-0.4$.',
            correcta: true,
            retro: 'Por defecto el software devuelve el MA(1) invertible, el de $|\\theta| < 1$, que aquí es $1/(-2.5) = -0.4$. Simulando 2000 valores sale $\\hat\\theta = -0.405$.'
          },
          {
            texto: 'El $\\hat\\sigma^2$ de ese ajuste quedará cerca de $1$, la varianza con que se simuló.',
            correcta: false,
            retro: 'Para describir el mismo proceso con $\\theta = -0.4$ hace falta $\\sigma^2 = 2.5^2 = 6.25$: así salen la misma $\\gamma_0 = 7.25$ y la misma $\\gamma_1 = -2.5$. En la simulación de 2000 valores, $\\hat\\sigma^2 = 6.58$.'
          }
        ],
        retroAcierto: 'Las dos son caras del mismo hecho: $(\\theta,\\ \\sigma^2) = (-2.5,\\ 1)$ y $(-0.4,\\ 6.25)$ dan las mismas autocovarianzas, de modo que $\\theta$ no es identificable, y el software resuelve el empate devolviendo por defecto el invertible.',
        retroFallo: 'Las correctas son la que compara la $\\rho_1$ de los dos MA(1) y la que dice qué $\\hat\\theta$ devuelve <code>arima()</code>: $(\\theta,\\ \\sigma^2) = (-2.5,\\ 1)$ y $(-0.4,\\ 6.25)$ dan las mismas autocovarianzas, $\\theta$ no es identificable y el software devuelve por defecto el invertible. Las otras tres confunden la estacionariedad con la invertibilidad, leen en la cota $0.5$ algo que no dice, u olvidan que al cambiar $\\theta$ cambia también $\\sigma^2$.'
      },
      {
        tipo: 'opcion',
        modulo: 5,
        pregunta: 'Ajustas un ARMA(1,1) a una serie de 100 datos y <code>arima()</code> devuelve $\\hat\\phi_1 = -0.60$ (error estándar $0.38$) y $\\hat\\theta_1 = 0.67$ (error estándar $0.35$). ¿Qué haces?',
        pista: 'Divide cada coeficiente entre su error estándar y, aparte, suma los dos coeficientes. Con esas tres cifras delante, pregúntate qué ha quedado bien determinado por los datos y qué no.',
        opciones: [
          {
            texto: 'Me quedo con el ARMA(1,1): los dos coeficientes son grandes en valor absoluto y los dos importan.',
            correcta: false,
            retro: 'El tamaño no basta. Ninguno de los dos coeficientes llega a $1.96$ veces su error estándar, y lo que el ajuste fija de verdad es su suma, $0.07$, no cada uno por separado. Dos parámetros que casi se cancelan no describen estructura: la esconden.'
          },
          {
            texto: 'Paso a un ARMA(2,2): con errores estándar tan grandes, al modelo le hacen falta más parámetros.',
            correcta: false,
            retro: 'Es justo al revés. Los errores estándar son grandes porque sobra un factor, no porque falte: la verosimilitud es casi plana en la dirección $\\phi_1 \\approx -\\theta_1$. Añadir parámetros abre la puerta a más factores casi comunes y la aplana todavía más.'
          },
          {
            texto: 'Diferencio la serie: unos coeficientes tan mal determinados indican que no es estacionaria.',
            correcta: false,
            retro: 'Nada apunta a una raíz unitaria: $|\\hat\\phi_1| = 0.60$ está lejos de 1. La imprecisión no es de la serie sino de la parametrización, porque muchas parejas $(\\phi_1, \\theta_1)$ con $\\phi_1 \\approx -\\theta_1$ dan casi la misma verosimilitud.'
          },
          {
            texto: 'Pruebo AR(1), MA(1) y ruido blanco, y los comparo por AICc antes de interpretar coeficientes.',
            correcta: true,
            retro: '$\\phi(B) = 1 + 0.60B$ y $\\theta(B) = 1 + 0.67B$ casi coinciden, así que el factor casi se cancela y el modelo es más pequeño de lo que aparenta. La serie era ruido blanco simulado, y el AICc lo recoge: $270.43$ para el ruido blanco, $272.43$ y $272.46$ para el MA(1) y el AR(1), y $273.88$ para el ARMA(1,1). Es la situación del ejemplo de R del Módulo 5.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 2,
        unidad: 'periodos',
        pregunta: 'Un AR(2) tiene $\\phi_1 = 0.9$ y $\\phi_2 = -0.5$. Sus raíces son complejas, así que su ACF oscila. ¿Cuánto vale su pseudo-periodo? Da dos decimales.',
        pista: 'La fórmula está en la nota «Raíces complejas y ciclos» del Módulo 2. Ve por partes —primero la raíz cuadrada, después el cociente, después el arcocoseno— y comprueba que la calculadora trabaja en <strong>radianes</strong>.',
        respuesta: 7.13,
        tolerancia: 0.006,
        retroAcierto: '$\\sqrt{0.5} = 0.7071$, el argumento del arcocoseno es $0.9/(2 \\times 0.7071) = 0.6364$, su arcocoseno vale $0.8810$ radianes y $2\\pi/0.8810 = 7.13$ periodos. Es el ángulo de la raíz de $\\phi(B)$: la misma cuenta que el Módulo 9 hace con el AR(2) de las manchas solares.',
        retroFallo: 'El cálculo es $2\\pi/\\arccos\\big(0.9/(2\\sqrt{0.5})\\big) = 2\\pi/\\arccos(0.6364) = 2\\pi/0.8810 = 7.13$ periodos. Los tropiezos habituales: dejar la calculadora en grados (sale $0.12$), olvidar la raíz cuadrada del denominador (sale $13.93$) o usar la otra fórmula, la del periodo medio de los ciclos, que el Módulo 9 distingue de esta (sale $7.57$). Y hace falta la precisión pedida: $7.1$ no basta.'
      },
      {
        tipo: 'opcion',
        modulo: 8,
        pregunta: 'Ajustas un ARMA(2,1) y evalúas Ljung–Box con <code>Box.test(residuals(m), lag = 12, type = "Ljung-Box")</code>, sin más argumentos. ¿Qué problema tiene esa llamada?',
        pista: 'Escribe los grados de libertad que usa la prueba tal como está llamada y los que corresponden a los residuales de un modelo con tres coeficientes estimados. Después piensa qué le pasa al $p$-valor al pasar de unos a otros.',
        opciones: [
          {
            texto: 'Ninguno: <code>Box.test()</code> descuenta por sí sola los parámetros del modelo ajustado.',
            correcta: false,
            retro: 'No lo hace. <code>fitdf</code> vale $0$ por defecto, porque la función no sabe de dónde vienen los residuales que recibe: podrían ser datos crudos. Hay que indicárselo siempre.'
          },
          {
            texto: 'Falta <code>fitdf = 3</code>: sin él la prueba es demasiado severa y rechaza de más.',
            correcta: false,
            retro: 'El argumento que falta es ese, pero la dirección del error es la contraria. Con más grados de libertad de los debidos el valor crítico es más alto y el $p$-valor, mayor: la prueba rechaza <em>menos</em>, y aprueba modelos que debería suspender.'
          },
          {
            texto: 'Falta <code>fitdf = 3</code>: sin él la prueba es demasiado indulgente y rechaza de menos.',
            correcta: true,
            retro: 'Con $p+q = 3$ parámetros estimados, el estadístico se distribuye $\\chi^2_{12-3}$, no $\\chi^2_{12}$. El caso más elocuente es el AR(2) de las manchas, donde $p+q = 2$: omitir <code>fitdf</code> cambia su $p$-valor de $0.0461$ (se rechaza) a $0.0996$ (no se rechaza). La conclusión se invierte por omitir un argumento.'
          },
          {
            texto: 'El problema es <code>lag = 12</code>: con un $h$ tan alto la prueba ya no puede detectar nada.',
            correcta: false,
            retro: 'La elección de $h$ admite discusión, pero no es el error de esta llamada: el capítulo evalúa en el rezago 12 las manchas solares. El problema está en otro argumento, y es uno que puede invertir la conclusión.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 8,
        alto: 200,
        descripcionGrafico: describirBarrasQuiz(
          'Función de autocorrelación de los residuales de un AR(1) ajustado a las manchas solares',
          MANCHAS.diagnosticos.arma10.acf_resid, banda(MANCHAS.n)),
        pregunta: 'Esta es la ACF de los residuales de un AR(1) ajustado a las manchas solares. ¿Qué haces?',
        pista: 'Mide antes de decidir: cuántas barras salen de la banda, en qué rezagos, y cuántas veces la supera la más alta. Compáralo con lo que el Módulo 6 dice que produce el azar.',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS, MANCHAS.diagnosticos.arma10.acf_resid, {
          etiqueta: 'ACF de los residuales', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Rechazo el modelo: quedan autocorrelaciones grandes y hay que aumentar el orden.',
            correcta: true,
            retro: '$r_1 = 0.556$ frente a una banda de $\\pm 0.196$, y no está sola: salen ocho de las veinte barras. Eso no es azar, es estructura sin modelar, y Ljung–Box da $p < 0.0001$. Subiendo a AR(2), las dos primeras autocorrelaciones residuales bajan a $0.1297$ y $-0.1477$.'
          },
          {
            texto: 'Lo acepto: con 20 rezagos, una o dos barras fuera de la banda son lo esperable.',
            correcta: false,
            retro: 'Esa regla vale para picos <em>pequeños y aislados</em>, apenas asomados. Aquí $r_1 = 0.556$ casi triplica la banda y salen ocho barras de veinte. La regla del 5 % explica ruido, no una señal así.'
          },
          {
            texto: 'Diferencio la serie: la ACF de los residuales decae despacio, como en una caminata.',
            correcta: false,
            retro: 'Diferenciar es la respuesta a una raíz unitaria en la <em>serie</em>, no a un mal ajuste. Estos residuales vienen de un modelo insuficiente sobre una serie que ya es estacionaria; diferenciar aquí sobrediferenciaría e introduciría un MA(1) espurio.'
          },
          {
            texto: 'Aplico el logaritmo: barras tan altas indican una varianza que crece con el nivel.',
            correcta: false,
            retro: 'La transformación resuelve problemas de <em>escala</em>, que se ven en la serie (amplitud que crece con el nivel), no en la ACF de los residuales. Y en esta serie el logaritmo es además imposible: hay un año con cero manchas.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 7,
        pregunta: 'Marca <strong>todas</strong> las afirmaciones correctas sobre los métodos de estimación.',
        pista: 'Para cada afirmación, localiza en el Módulo 7 la frase de la definición de los tres métodos, o la cifra de la tabla de las manchas, que la respalda o la desmiente.',
        opciones: [
          {
            texto: 'Yule–Walker estima bastante bien un AR puro y es muy ineficiente si hay parte MA.',
            correcta: true,
            retro: 'Es lo que el módulo dice de este método, que sale de las ecuaciones de momentos del AR: funciona bien en un AR puro y pierde mucha eficiencia en cuanto el modelo tiene parte MA.'
          },
          {
            texto: 'Con la misma serie y el mismo modelo, los tres métodos dan lo mismo, salvo diferencias de redondeo.',
            correcta: false,
            retro: 'No coinciden: sobre las manchas solares, Yule–Walker quedó a $1.26$ y $1.10$ errores estándar de máxima verosimilitud. CSS y máxima verosimilitud sí quedaron muy cerca, pero eso depende de $T$ y de lo cerca que esté $\\phi$ de la frontera.'
          },
          {
            texto: 'CSS condiciona en las primeras observaciones e ignora su aporte a la verosimilitud.',
            correcta: true,
            retro: 'Minimiza la suma de cuadrados condicionando en los primeros valores. La verosimilitud exacta añade la densidad de esas primeras observaciones, que es el término que penaliza los $\\phi$ cercanos a la frontera.'
          },
          {
            texto: 'El $\\hat\\sigma^2$ que devuelve <code>ar()</code> y el de <code>arima()</code> son intercambiables para calcular un AIC.',
            correcta: false,
            retro: 'No salen del mismo cálculo: en las manchas fueron $298.96$ y $229.43$. Los criterios de información se construyen sobre la verosimilitud, así que solo tienen sentido con ajustes de <code>arima()</code>.'
          },
          {
            texto: 'Sin indicar método, <code>arima()</code> usa <code>"CSS-ML"</code>: empieza con CSS y acaba con la verosimilitud exacta.',
            correcta: true,
            retro: 'Es su valor por defecto: CSS da los valores iniciales y la estimación final maximiza la verosimilitud exacta.'
          }
        ],
        retroAcierto: 'Son las tres que describen lo que hace cada método. Las dos falsas las desmiente el propio módulo con las manchas solares: Yule–Walker y máxima verosimilitud se separaron $1.26$ y $1.10$ errores estándar, y sus $\\hat\\sigma^2$ fueron $298.96$ y $229.43$.',
        retroFallo: 'Las correctas son las que dicen para qué modelos funciona bien Yule–Walker, qué deja fuera CSS y qué hace <code>arima()</code> por defecto. Las dos falsas son lo que el módulo desmiente con números: los métodos <strong>no</strong> coinciden —Yule–Walker quedó a más de un error estándar de máxima verosimilitud— y sus $\\hat\\sigma^2$ no miden lo mismo, así que mezclar salidas de <code>ar()</code> y <code>arima()</code> para comparar criterios de información no tiene sentido.'
      }
    ];
"""

# «el envolvente» -> «la envolvente» en el simulador de los pesos psi (comentarios y lectura)
ENVOLVENTE = [
    ("      // amortiguación. El envolvente de psi_j = R^j sin((j+1)w)/sin(w) no es",
     "      // amortiguación. La envolvente de psi_j = R^j sin((j+1)w)/sin(w) no es"),
    ("      // El envolvente no es una recta, así que no cabe en la opción `lineas`",
     "      // La envolvente no es una recta, así que no cabe en la opción `lineas`"),
    ("          `, dentro del envolvente ±${factor.toFixed(2)} × ${R.toFixed(4)}ʲ; en color oscuro, ` +",
     "          `, dentro de la envolvente ±${factor.toFixed(2)} × ${R.toFixed(4)}ʲ; en color oscuro, ` +"),
]


def aplica(js):
    ini = js.index("    AUTOEVALUACIONES['cap3'] = [\n")
    fin = js.index("\n    ];\n", ini) + len("\n    ];\n")
    assert js.count("    AUTOEVALUACIONES['cap3'] = [\n") == 1
    assert "AUTOEVALUACIONES['parcial2']" not in js[ini:fin], "el recorte se comió la práctica de repaso"
    js = js[:ini] + QUIZ + js[fin:]
    for antes, despues in ENVOLVENTE:
        assert js.count(antes) == 1, antes
        js = js.replace(antes, despues)
    return js
