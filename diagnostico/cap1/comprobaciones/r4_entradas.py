# Entradas de la ronda R4 para bibliografia/contraste/cap1.yml
F, CL, R, SH, CR = "hyndman2021forecasting", "cleveland1990stl", "rcoreteam2026r", "shumway2011time", "cryer2008time"
def web(loc, inst, cita): return dict(clave=F, loc=loc, clase="WEB", instantanea=inst, cita=cita)
def rdoc(loc, tema, cita): return dict(clave=R, loc=loc, clase="WEB", instantanea=tema, cita=cita)
def pdf(clave, loc, pag, cita): return dict(clave=clave, loc=loc, clase="PDF", pagina_pdf=pag, cita=cita)
VA = "subagente verificador de la ronda R4 (Opus 5.5), contexto limpio · lote R4a"
VB = "subagente verificador de la ronda R4 (Opus 5.5), contexto limpio · lote R4b"
E = []
def e(id, tipo, afirmacion, veredicto, fuentes, nota, verif): E.append(dict(id=id, tipo=tipo, afirmacion=afirmacion, veredicto=veredicto, fuentes=fuentes, nota=nota, verificado_por=verif))

e("c1-m1-01", "definicion", "Una serie de tiempo es una sucesión de observaciones de una misma variable, registradas en instantes ordenados y, por lo general, equiespaciados.", "respaldada", [
  web("§1.4", "intro", "observed at regular intervals of time"),
  pdf(SH, "p. 11; §1.3", 24, "according to the order they are obtained in time"),
  pdf(SH, "p. 11; §1.3", 24, "sampled at equally spaced points"),
], "FPP3 §1.4 respalda el registro a intervalos regulares, y Shumway y Stoffer §1.3 la indexación por el orden temporal y el muestreo equiespaciado. Dos detalles de alcance que no cambian el veredicto: FPP3 se limita a intervalos regulares, mientras el capítulo dice «por lo general, equiespaciados»; y Shumway y Stoffer presentan la serie como una colección de variables aleatorias, no como la sucesión de valores observados del capítulo. La cita visible es la de FPP3. Único cambio de prosa: el paréntesis final «(cada mes, cada día, cada hora)» pasó a dos puntos, para que la cita no quedara pegada a otro paréntesis.", VA)

e("c1-m1-04", "dato", "AirPassengers: pasajeros mensuales de aerolíneas internacionales, en miles, de 1949 a 1960; es la serie clásica del curso.", "con-matiz", [
  rdoc("§Description", "AirPassengers", "international airline passengers, 1949 to 1960."),
  rdoc("§Description", "AirPassengers", "The classic Box & Jenkins airline data."),
  rdoc("§Format", "AirPassengers", "A monthly time series, in thousands."),
  pdf(CR, "p. 247; ejercicio 10.9", 257, "is considered a classic time series. The data are in the file named airpass."),
], "El verificador leyó Cryer y Chan y dio «con-matiz»: respaldan los pasajeros mensuales de aerolíneas internacionales, en miles, y el carácter de serie clásica, pero fechan su archivo airpass en 01/1960–12/1971 (p. 104, ejercicio 5.13, y la lista de datos de la p. 471), no en 1949–1960; y señaló que el rango solo podía salir de la ayuda de R. Esa ayuda ya está en la biblioteca (R 4.6.0, datasets 4.6.0) y lo dice literalmente: totales mensuales, 1949 a 1960, en miles, «the classic Box & Jenkins airline data». Las tres citas de la ayuda de R las localizó el redactor de la R4 por indicación de la sesión maestra y las comprobó con grep contra la instantánea: NO pasaron por el verificador R4a, y por eso el veredicto no se sube a «respaldada»; queda para el verificador posterior. Matiz que permanece: las fechas de Cryer y Chan no coinciden con las de R; el capítulo usa el conjunto de datos de R. «De este curso» es afirmación propia. Cambio de prosa: «en miles (1949–1960)» pasó a «en miles, de 1949 a 1960», para no encadenar dos paréntesis con la cita.", VA)

e("c1-m3-08", "regla", "En el gráfico estacional, líneas casi paralelas indican estacionalidad estable y un abanico que se abre indica estacionalidad que crece con el nivel: es la señal de un modelo multiplicativo.", "con-matiz", [
  web("§3.2", "decomposition", "then a multiplicative decomposition is more appropriate"),
], "FPP3 §3.2 respalda la conclusión —si la variación estacional es proporcional al nivel, el modelo es multiplicativo—, pero no la regla de lectura del gráfico estacional: §2.4 describe gg_season sin hablar de líneas paralelas ni de un abanico. Traducir el criterio a esa imagen es aportación del capítulo, que no la atribuye a nadie: basta esta nota y no se tocó la prosa. Por eso la cita visible va justo detrás de «modelo multiplicativo», que es lo que la fuente sostiene, y la marca se extendió hasta esa frase.", VA)

e("c1-m4-02", "definicion", "Tendencia: movimiento de largo plazo, creciente o decreciente.", "respaldada", [
  web("§2.3", "graphics", "long-term increase or decrease in the data"),
  pdf(CR, "p. 28; §3.1", 41, "Many authors use the word trend only for a slowly changing mean"),
], "FPP3 §2.3 define la tendencia como el capítulo: aumento o descenso de largo plazo. El capítulo no recoge que FPP3 añade que no tiene por qué ser lineal y que puede «cambiar de dirección», ni que Cryer y Chan advierten de que el uso del término varía entre autores.", VA)

e("c1-m4-03", "definicion", "Estacionalidad: patrón que se repite con período fijo y conocido.", "respaldada", [
  web("§2.3", "graphics", "Seasonality is always of a fixed and known period."),
], "FPP3 §2.3 sostiene literalmente el período fijo y conocido. El mismo pasaje añade, entre paréntesis, que una serie puede tener más de un patrón estacional. Cambio de prosa sin contenido: el paréntesis «(12 meses, 7 días…)» pasó a rayas, para que la cita no quedara pegada a otro paréntesis.", VA)

e("c1-m4-04", "definicion", "Ciclo: oscilaciones de duración variable y no fija, como los ciclos económicos de varios años.", "respaldada", [
  web("§2.3", "graphics", "that are not of a fixed frequency"),
  web("§2.3", "graphics", "usually due to economic conditions"),
], "FPP3 §2.3 respalda la duración no fija y el vínculo con el ciclo económico. El «varios años» del capítulo es compatible pero menos preciso que la fuente, que dice que la duración suele ser de al menos dos años. Cambio de prosa sin contenido: el paréntesis del ejemplo pasó a rayas, por la misma razón que en c1-m4-03.", VA)

e("c1-m4-06", "atribucion", "Al descomponer una serie, Hyndman y Athanasopoulos agrupan tendencia y ciclo en un solo componente tendencia-ciclo.", "con-matiz", [
  web("cap. 3", "decomposition", "combine the trend and cycle into a single trend-cycle component"),
], "El verificador leyó la frase anterior —«Muchos textos agrupan tendencia y ciclo en un solo término tendencia-ciclo»— y dio «con-matiz»: la práctica está en la introducción del cap. 3 de FPP3, que la presenta como lo que sus autores hacen al descomponer y añade que al componente se le suele llamar simplemente tendencia; pero ninguna fuente leída sostiene que lo hagan «muchos textos». SE AJUSTÓ LA PROSA para decir lo que la fuente dice: la práctica se atribuye a FPP3 con cita narrativa. La frase nueva no la ha leído el verificador: el veredicto se deja en «con-matiz» hasta que el verificador posterior la confirme.", VA)

e("c1-m4-07", "resultado", "Las fluctuaciones cíclicas no tienen duración fija y suelen durar al menos dos años; un ciclo largo del que solo se ve un tramo es indistinguible de una tendencia.", "respaldada", [
  web("§2.3", "graphics", "is usually at least 2 years"),
  web("§2.3", "graphics", "is actually part of a long cycle"),
], "El texto del inventario («un ciclo económico de siete u ocho años cabría ahí una vez y media») ya no está en el capítulo: lo retiró una ronda anterior. Se marcó la frase vigente del mismo párrafo, que es la que el verificador leyó y respaldó con FPP3 §2.3, incluido el ejemplo de los bonos del Tesoro, donde un ciclo largo visto en una ventana corta parece tendencia. La cifra retirada no la sostenía ninguna fuente leída. Que AirPassengers cubra doce años, y que en ella quepan pocos ciclos, lo pone el capítulo y queda fuera de la marca.", VA)

e("c1-m4-10", "definicion", "Los componentes se combinan de forma aditiva o multiplicativa.", "respaldada", [
  web("§3.2", "decomposition", "additive decomposition, then we can write y_{t} = S_{t} + T_{t} + R_t"),
  web("§3.2", "decomposition", "y_{t} = S_{t} \\times T_{t} \\times R_t"),
], "FPP3 §3.2 escribe las dos ecuaciones que el capítulo pone a continuación de la frase marcada; el orden de los sumandos y de los factores difiere, sin consecuencia. El puntero del inventario a Shumway y Stoffer, p. 2, no sirve: esa página trata del dominio del tiempo frente al de la frecuencia.", VA)

e("c1-m4-11", "regla", "El modelo aditivo conviene cuando la amplitud estacional, o la variación alrededor de la tendencia, no depende del nivel; el multiplicativo, cuando es proporcional al nivel.", "respaldada", [
  web("§3.2", "decomposition", "does not vary with the level of the time series"),
  web("§3.2", "decomposition", "proportional to the level of the time series"),
], "El criterio del capítulo coincide con FPP3 §3.2, incluida la mención de la variación alrededor de la tendencia además de la amplitud estacional. El texto del inventario era una versión anterior de la frase («amplitud constante» / «crece con el nivel»); se marcó la vigente, que es la que leyó el verificador.", VA)

e("c1-m5-01", "definicion", "Media móvil de orden m; para m impar, el promedio de los m = 2k + 1 valores centrados en t.", "respaldada", [
  web("§3.3", "decomposition", "moving average of order m can be written as \\hat{T}_{t} = \\frac{1}{m} \\sum_{j=-k}^k y_{t+j}"),
  pdf(SH, "p. 71; §2.4; ec. 2.50", 84, "the weights, a−k , . . . , a0 , . . . , ak , we used were all the same"),
], "La fórmula y la condición m = 2k + 1 son las de FPP3 §3.3 (su ecuación 3.2), y Shumway y Stoffer describen la misma media móvil simétrica de pesos iguales. El verificador escribió el localizador como «§3.3; ec. 3.2»; aquí se deja «§3.3», que es donde está la ecuación 3.2 en la instantánea, para que la cita visible sea más corta.", VA)

e("c1-m5-02", "definicion", "Con m par se promedian dos ventanas consecutivas de orden m, lo que equivale a usar m + 1 valores con los dos extremos a medio peso.", "respaldada", [
  web("§3.3", "decomposition", "equivalent to a weighted moving average of order m + 1"),
], "Por el tope de palabras citadas de FPP3 (F11) se registra una sola de las dos citas del verificador; la otra («The first value in the 2x4-MA column is the average of these two») respaldaba la primera mitad. FPP3 §3.3 sostiene las dos mitades: que la 2×m-MA es el promedio de dos ventanas consecutivas de orden m, y que equivale a una media ponderada de orden m + 1 con pesos 1/m salvo los extremos, que llevan 1/(2m): los «extremos a media ración» del capítulo.", VA)

e("c1-m6-09", "definicion", "Quitar la tendencia —restando o dividiendo— deja la serie sin tendencia, y el índice de cada mes sale de promediar esa serie por posición.", "respaldada", [
  web("§3.4", "decomposition", "Calculate the detrended series: y_t - \\hat{T}_t."),
  web("§3.4", "decomposition", "average the detrended values for that season"),
], "FPP3 §3.4 da el paso 2 en las dos escalas —restar en la aditiva, dividir en la multiplicativa— y el paso 3 como el promedio por posición. Que en la serie sin tendencia «ya solo quedan estacionalidad y ruido» no lo dice con esas palabras: se sigue del modelo que §3.2 escribe. La marca termina en «y así con los doce meses»; la frase siguiente, sobre la rigidez de los índices, queda fuera (está cubierta por c1-m6-01).", VA)

e("c1-m6-13", "definicion", "La tabla «El método en símbolos»: los pasos de la descomposición clásica en notación, en paralelo para el modelo aditivo y el multiplicativo, que solo difieren en la operación.", "con-matiz", [
  web("§3.4", "decomposition", "trend-cycle component \\hat{T}_t using a 2 \\times m-MA."),
  web("§3.4", "decomposition", "adjusted to ensure that they add to m."),
  web("§3.4", "decomposition", "dividing out the estimated seasonal and trend-cycle components"),
], "FPP3 §3.4 respalda el contenido de cada fila —tendencia por media móvil, serie sin tendencia, promedio por posición, ajuste de los índices y residuo— en las dos columnas. El matiz, que el capítulo no oculta porque no atribuye la tabla a nadie: la numeración no coincide (el paso 1 de FPP3 es la tendencia; el del capítulo es elegir la escala, que FPP3 trata en §3.2), y FPP3 enuncia la condición de los índices pero no escribe las fórmulas de normalización ni el recuento n_k, que son construcciones del capítulo. No se tocó la prosa. La afirmación del inventario era el rótulo de la tabla, que solo ven los lectores de pantalla: la marca envuelve la tabla entera y el párrafo que la lee («Leída en horizontal…»), de modo que la huella vigila también las fórmulas, y la cita visible va en ese párrafo.", VA)

e("c1-m6-14", "resultado", "Los índices multiplicativos promedian 1: es la condición que impone la normalización.", "respaldada", [
  web("§3.4", "decomposition", "adjusted to ensure that they add to m."),
], "FPP3 §3.4 impone que los índices multiplicativos sumen m —con m = 12, media 1— y que los aditivos sumen cero. Enuncia la condición sin decir cómo se impone: el reescalado concreto del paso 3c es del capítulo. La marca cubre solo la primera frase de la nota: la cifra 12.0001, que sale de R, y la condición aditiva quedan fuera. El verificador dio también la cita de la condición aditiva («…adjusted to ensure that they add to zero»), que se retiró porque la frase marcada solo habla del caso multiplicativo y por el tope de palabras citadas de FPP3 (F11).", VA)

e("c1-m6-20", "definicion", "El encadenamiento se llama descomposición clásica y arranca con una media móvil del orden del período.", "respaldada", [
  web("§3.4", "decomposition", "\\hat{T}_t using a 2 \\times m-MA."),
  web("§3.3", "decomposition", "first step in a classical decomposition is to use a moving average"),
], "CAMBIO DE IDENTIFICADOR: en el inventario esta afirmación es c1-m6-02, pero ese id ya estaba registrado desde la R3 para la cuarta limitación del método clásico; aquí lleva c1-m6-20, el primero libre del módulo. El verificador la contrastó con el id del inventario y avisó del choque. FPP3 §3.3 y §3.4 respaldan que el primer paso del método clásico es la media móvil del orden del período. La frase siguiente del capítulo, que describe el procedimiento como un bucle gobernado por el residuo, es organización propia y queda fuera de la marca.", VA)

e("c1-m7-01", "atribucion", "STL se desarrolla como «Seasonal and Trend decomposition using Loess».", "con-matiz", [
  web("§3.6", "decomposition", "acronym for “Seasonal and Trend decomposition using Loess”"),
  pdf(CL, "p. 3", 1, "STL: A Seasonal-Trend Decomposition"),
  pdf(CL, "p. 3", 1, "Procedure Based on Loess"),
  rdoc("§Description", "stl", "components using ‘loess’, acronym STL."),
], "Estaba «pendiente» desde el piloto. El capítulo escribía «Seasonal-Trend decomposition using Loess», y el verificador, ya con el artículo original leído, confirmó que ninguna fuente escribe esa cadena: mezclaba el guion del título original con el «using Loess» de FPP3. Qué dice cada una: el artículo de Cleveland et al. (1990) nunca desarrolla el acrónimo en prosa, solo en su título, «STL: A Seasonal-Trend Decomposition Procedure Based on Loess»; FPP3 §3.6 dice que STL es el acrónimo de «Seasonal and Trend decomposition using Loess»; y la ayuda de stl() habla de descomponer «using 'loess', acronym STL». SE CORRIGIÓ LA PROSA: el capítulo copia ahora la forma de FPP3, que es la única fuente que desarrolla el acrónimo en una frase, y la cita. El matiz que queda es que esa forma no es la del título del artículo original. La frase corregida no la ha leído el verificador (dio «con-matiz» a la anterior): la confirma el verificador posterior. Sobre el rango de páginas que el piloto dejó abierto: la portada del PDF dice pp. 3–73, que incluye los comentarios publicados; FPP3 cita 3–33, solo el artículo.", VB)

e("c1-m7-02", "resultado", "En STL la robustez es una opción aparte, cuesta un segundo bucle y en stl() viene desactivada.", "respaldada", [
  pdf(CL, "§3.3", 12, "The STL robust estimation is needed when"),
  pdf(CL, "§3.3", 12, "consists of the inner loop."),
  pdf(CL, "§2.2", 4, "an inner loop nested inside an outer loop. In"),
  rdoc("§Usage", "stl", "robust = FALSE,"),
  rdoc("§Usage", "stl", "outer = if(robust) 15 else 0,"),
], "Estaba «pendiente» desde el piloto, a falta del artículo original y de la ayuda de R. Las tres partes quedan respaldadas, cada una por su fuente. Opcional: §3.3 del artículo dice que la estimación robusta hace falta cuando hay comportamiento no gaussiano y que, si no, se pueden omitir las iteraciones de robustez. Segundo bucle: §2.2 define el bucle exterior, y §3.3 dice que sin robustez STL consiste en el bucle interior. Por defecto: lo dice la ayuda de stl(), robust = FALSE y outer = 0. Las 15 vueltas con robust = TRUE son de R; el artículo recomienda 5 o 10. El verificador dio además la cita «the robustness iterations and set ,,,= 0;in», que está en el texto de la caché pero con el subíndice n_o destrozado por el OCR: se dejó fuera por ilegible, y lo que decía lo cubren las otras dos de §3.3. La prosa no cambió; la huella sí, porque la cita del artículo va en mitad de la frase y deja un espacio antes de la coma.", VB)

e("c1-m7-05", "definicion", "Loess, regresión local ponderada: para dar el valor en t toma los puntos más próximos, les ajusta una recta por mínimos cuadrados y se queda con su altura en t.", "respaldada", [
  pdf(CL, "§2.1", 4, "x; that are closest to x are selected and each"),
  pdf(CL, "§2.1", 4, "fitting is locally-linear or locally-quadratic."),
  pdf(CL, "§2.1", 4, "locally-fitted polynomial at x is g(x). In this"),
  pdf(CL, "§2.1", 4, "increase in distance from x and become zero"),
  pdf(CL, "p. 5", 3, "weighted regression, or loess (Cleveland and"),
  pdf(SH, "p. 75; fig. 2.14", 88, "Nearest neighbor (supsmu) and locally weighted regression (lowess)"),
], "§2.1 del artículo dice las cuatro cosas de la frase: se eligen los q valores más próximos a x, se ajusta un polinomio local de grado 1 o 2, el valor devuelto es el del polinomio en x, y los pesos se anulan en el q-ésimo punto más lejano. El ajuste es ponderado, cosa que el capítulo añade dos frases después. SE CORRIGIÓ LA PROSA: el capítulo desarrollaba Loess como «locally estimated scatterplot smoothing», y el verificador advirtió de que esa expresión no está en ninguna fuente leída. El artículo lo presenta en su p. 5 como «locally-weighted regression, or loess» (en el texto de la caché, «locally-» queda a final de renglón), y Shumway y Stoffer rotulan su figura 2.14 «locally weighted regression (lowess)» y en la p. 64 desarrollan lowess como «locally weighted scatterplot smoothing». El capítulo dice ahora «regresión local ponderada, locally weighted regression». La última cita, la de Shumway y Stoffer, la añadió el redactor para sostener esa forma sin guion y no pasó por el verificador.", VB)

e("c1-m7-06", "dato", "En stl(), t.window es la anchura de la ventana de Loess con que se suaviza la tendencia.", "respaldada", [
  rdoc("§Arguments", "stl", "t.window: the span (in lags) of the loess window for trend extraction,"),
], "La frase del inventario («es lo que en R se pasa como t.window para la tendencia y s.window para lo estacional») ya no está: la R3-bis repartió su contenido entre los pasos 1 y 2 de «El método, paso a paso». Aquí se marca el paso 2, que dice lo de t.window; lo de s.window está en el paso 1, dentro de c1-m7-15, adonde se llevó la cita correspondiente del verificador. La ayuda de stl() respalda literalmente que t.window es la anchura de la ventana de Loess para la tendencia. Dice «in lags»: el «en meses» del capítulo es su lectura para una serie mensual. El artículo no usa ese nombre —allí el parámetro es n_t—.", VB)

e("c1-m7-07", "dato", "Grados por defecto de stl(): t.degree = 1 para la tendencia y s.degree = 0 para lo estacional.", "respaldada", [
  rdoc("§Usage", "stl", "stl(x, s.window, s.degree = 0,"),
  rdoc("§Usage", "stl", "t.window = NULL, t.degree = 1,"),
  pdf(CL, "§2.3", 5, "smoothed by loess with q = m, andd = 1."),
], "Los dos valores por defecto están en la línea de uso de la ayuda de stl(). La frase del inventario («una recta para la tendencia (t.degree = 1) y una constante para lo estacional (s.degree = 0)») ya no está; se marcó el párrafo de cierre del desarrollo, que es donde hoy se dan los dos grados. ATENCIÓN, para el docente: la fuente respalda los VALORES, no las razones. El párrafo marcado explica s.degree = 0 diciendo que las subseries son cortas y que «pedirles una pendiente sería pedirle demasiado a doce puntos»; esa razón es del capítulo, y el artículo original describe el suavizado de las subseries de ciclo con d = 1 (§2.3, paso 2), de modo que el 0 es una decisión de la implementación de R que se aparta del artículo. La cita visible va pegada a «los dos grados por defecto» para no dar a entender que la ayuda de R da las razones. No se tocó la prosa.", VB)

e("c1-m7-08", "definicion", "Los pesos de la ventana los da la función tricúbica, que vale 1 sobre el punto estimado y se anula en el borde.", "respaldada", [
  pdf(CL, "§2.1", 4, "tricube weight function:"),
  pdf(CL, "§2.1", 4, "Thus the x, close to x have the largest"),
  pdf(CL, "§2.1", 4, "increase in distance from x and become zero"),
  pdf(CL, "§2.1", 4, "at the qth farthest point."),
], "El nombre y la forma son del artículo: «tricube weight function», peso máximo sobre x, que decrece con la distancia y se anula en el q-ésimo punto más lejano, es decir, en el borde de la ventana. La fórmula del capítulo coincide con la ecuación de la página impresa 6, que el OCR destroza y el verificador leyó sobre la imagen de la página: W(u) = (1 − u³)³ para 0 ≤ u < 1 y 0 para u ≥ 1. No hay cita literal posible de la fórmula.", VB)

e("c1-m7-10", "regla", "stl() deduce la ventana de tendencia del período y de la ventana estacional: el impar inmediato al techo de 1.5·m / (1 − 1.5/s.window).", "respaldada", [
  rdoc("§Arguments", "stl", "‘nextodd(ceiling((1.5*period) / (1-(1.5/s.window))))’, is"),
  pdf(CL, "p. 20", 18, "to be the smallest odd integer satisfying the"),
  pdf(CL, "p. 20", 18, "chosen to be 35; the right side of the"),
], "La ayuda de stl() da la regla carácter por carácter, incluidos el techo y el impar inmediato. El artículo respalda la misma regla en prosa —n_t es el menor entero impar que satisface la desigualdad con 1.5 n_p— y la ilustra con el CO2 mensual: con n_s = 35 el lado derecho da 18.8 y n_t = 19, el mismo 19 del capítulo, aunque allí sale de otra ventana estacional. La desigualdad impresa es ilegible en el OCR.", VB)

e("c1-m7-15", "resultado", "El componente estacional se obtiene suavizando con Loess cada subserie de un mismo mes; s.window es la anchura de ese suavizado y con \"periodic\" se sustituye por la media.", "respaldada", [
  pdf(CL, "§2.2", 5, "subseries as cycle-subseries."),
  pdf(CL, "§2.2", 5, "January values, the second is the February"),
  pdf(CL, "§2.3", 5, "cycle-subseries of the detrended series is"),
  rdoc("§Details", "stl", "sub-series (the series of all January values, ...); if ‘s.window ="),
  rdoc("§Details", "stl", "\"periodic\"’ smoothing is effectively replaced by taking the mean."),
  rdoc("§Arguments", "stl", "lags) of the loess window for seasonal extraction, which"),
], "El artículo nombra y define las subseries de enero, de febrero, etc. («cycle-subseries»), y el paso 2 de su bucle interior las suaviza por separado con Loess. La ayuda de stl() lo repite y añade que con s.window = \"periodic\" el suavizado se sustituye por la media de cada subserie; el artículo no describe ese caso, que es una comodidad de R. La frase del inventario («no se ajusta sobre la serie entera, sino sobre cada subserie de ciclo») sigue en el cierre del desarrollo, dentro de c1-m7-07; aquí se marca el paso 1 de «El método, paso a paso», que es donde el lector lo encuentra primero y dice lo mismo. La última cita viene del veredicto de c1-m7-06, porque lo de s.window quedó en este paso. La ayuda dice «in lags»: el «en años» del capítulo es su lectura (un rezago de la subserie de un mes es un año).", VB)

e("c1-m7-16", "resultado", "Los pasos de estacionalidad y tendencia se repiten unas pocas veces: dos pasadas por defecto.", "con-matiz", [
  rdoc("§Arguments", "stl", "inner: integer; the number of ‘inner’ (backfitting) iterations;"),
  rdoc("§Arguments", "stl", "usually very few (2) iterations suffice."),
  pdf(CL, "§2.2", 4, "STL consists of two recursive procedures:"),
  pdf(CL, "§2.2", 4, "an inner loop nested inside an outer loop. In"),
  pdf(CL, "§2.3", 5, "Each pass of the inner loop consists of"),
  pdf(CL, "§2.2", 4, "loop followed by a computation of"),
], "La frase del inventario («Son dos bucles, uno dentro de otro: el interior alterna estacionalidad y tendencia hasta que se estabilizan…») ya no está: la R3 y la R3-bis la repartieron entre el paso 4 de «El método, paso a paso» y el párrafo del bucle exterior. Se marca el paso 4. El «con-matiz» del verificador era para la frase vieja: «hasta que se estabilizan» sugería un criterio de parada, y el número de pasadas interiores es fijo (n_i en el artículo; 2 en stl()). La frase vigente —«unas pocas veces, dos pasadas por defecto»— ya no incurre en eso, como anotó el propio verificador; no se tocó la prosa y el veredicto se deja como él lo dio. El artículo respalda la estructura de dos bucles anidados (§2.2) y la ayuda de stl() el número de pasadas. La segunda cita es la continuación, en la misma entrada «inner» de la ayuda, de la que dio el verificador; el valor por defecto está además en la línea de uso (inner = if(robust) 1 else 2). El bucle exterior lo cubre c1-m7-02.", VB)

e("c1-m7-18", "definicion", "El recorte de pesos lo fija la función bicuadrada, medida en unidades de seis veces la mediana de los residuos absolutos.", "respaldada", [
  pdf(CL, "§2.4", 6, "where B is the bisquare weight function:"),
  pdf(CL, "§2.4", 6, "h = 6 median(|R,|)."),
  pdf(CL, "§2.4", 6, "will have a small or zero weight. Let"),
  pdf(CL, "§2.4", 6, "in the data that results in a very large |R,|"),
], "El artículo da las tres piezas de la frase: el nombre («bisquare weight function»), la unidad de medida —h es seis veces la mediana de los residuos absolutos— y el corte, porque un atípico con residuo grande recibe un peso pequeño o nulo. La fórmula del capítulo coincide con la ecuación impresa, que el OCR destroza y el verificador leyó sobre la imagen: B(u) = (1 − u²)² para 0 ≤ u < 1 y 0 para u > 1. En las citas, «|R,|» es como el OCR dejó |R_v|.", VB)

e("c1-m8-02", "definicion", "La serie desestacionalizada retira el componente estacional y deja tendencia y residuo: y − S en el modelo aditivo, y / S en el multiplicativo.", "respaldada", [
  web("§3.2", "decomposition", "removed from the original data, the resulting values are the “seasonally adjusted” data."),
  web("§3.2", "decomposition", "contain the remainder component as well as the trend-cycle"),
], "FPP3 §3.2 respalda la definición, las dos fórmulas y el punto fino de que la serie ajustada conserva el residuo además de la tendencia-ciclo. FPP3 añade una advertencia que el párrafo marcado no recoge: por eso la serie ajustada no es suave y sus giros pueden engañar (el capítulo lo dice en la entradilla del gráfico siguiente).", VA)

e("c1-m8-03", "historica", "La serie desestacionalizada es lo que reportan muchas estadísticas oficiales, como las de desempleo.", "con-matiz", [
  web("§3.2", "decomposition", "monthly unemployment data are usually seasonally adjusted"),
  web("§3.5", "decomposition", "decomposition procedures which are used for seasonal adjustment"),
], "El verificador leyó «muchas estadísticas oficiales —desempleo, producción—» y dio «con-matiz»: FPP3 respalda el desempleo como caso típico de ajuste estacional (§3.2) y que las oficinas de estadística lo practican con procedimientos propios (§3.5), pero no dice nada de la «producción»; el pasaje más cercano habla de los datos de empleo «and many other economic series». SE AJUSTÓ LA PROSA: se retiró «producción», que habría exigido la metodología de una oficina de estadística concreta, y queda «las de desempleo, por ejemplo». La frase nueva no la ha leído el verificador. Queda sin tocar, porque no era de esta ronda, la retroalimentación de la autoevaluación que dice «las cifras oficiales de empleo o PIB» (c1-m8-13 del inventario): el PIB tampoco está en FPP3.", VA)

# ============================================================================
# Corrección de la R4 (2026-11-13): los 21 puntos del verificador independiente
# ============================================================================
D = {x["id"]: x for x in E}
VM = "sesión maestra de la ronda R4, que comprobó la frase contra la instantánea el 2026-11-13"
POST = " Corrección posterior a la verificación independiente de la R4 (2026-11-13): "
def cambia(id, vieja, nueva):
    f = [x for x in D[id]["fuentes"] if x["cita"] == vieja]; assert len(f) == 1, (id, vieja); f[0]["cita"] = nueva

# 15 · c1-m1-01
D["c1-m1-01"]["nota"] = "Lo que las citas sostienen y lo que no. La de FPP3 §1.4 —«observed at regular intervals of time»— no es una definición: es una declaración de alcance del libro («In this book, we will only consider time series that are…»), que respalda el registro a intervalos regulares. Las dos de Shumway y Stoffer §1.3 respaldan la indexación por el orden temporal y el muestreo equiespaciado, pero presentan la serie como una colección de variables aleatorias, no como la sucesión de valores observados del capítulo. Ninguna de las tres cubre lo univariante («de una misma variable»): eso lo pone el capítulo. FPP3 se limita a intervalos regulares, y el capítulo dice «por lo general, equiespaciados». La cita visible es la de FPP3. Único cambio de prosa: el paréntesis final «(cada mes, cada día, cada hora)» pasó a dos puntos, para que la cita no quedara pegada a otro paréntesis."

# 6 · c1-m1-04
x = D["c1-m1-04"]; x["veredicto"] = "respaldada"; x["verificado_por"] = VM
x["fuentes"] = [rdoc("§Description; §Format", "AirPassengers", "international airline passengers, 1949 to 1960."),
                rdoc("§Description", "AirPassengers", "The classic Box & Jenkins airline data."),
                rdoc("§Format", "AirPassengers", "A monthly time series, in thousands.")]
x["nota"] = "La ayuda de R (R 4.6.0, datasets 4.6.0) sostiene la frase entera: totales mensuales de pasajeros de aerolíneas internacionales, de 1949 a 1960 y «the classic Box & Jenkins airline data» en la sección Description, y «in thousands» en la sección Format; por eso la cita visible lleva las dos secciones. Las citas las localizó el redactor de la R4 y las comprobó la sesión maestra contra la instantánea, que es quien subió el veredicto a «respaldada». El verificador del lote R4a había leído solo Cryer y Chan y dio «con-matiz»: ese libro llama clásica a la serie (p. 247, ejercicio 10.9), pero fecha su archivo airpass en 01/1960–12/1971 (p. 104, ejercicio 5.13, y la lista de datos de la p. 471), que no es el rango del capítulo. Por eso Cryer y Chan no figura entre las fuentes: no sostiene la frase marcada y en las fechas la contradice; el capítulo usa el conjunto de datos de R. «De este curso» es afirmación propia. Cambio de prosa: «en miles (1949–1960)» pasó a «en miles, de 1949 a 1960», para no encadenar dos paréntesis con la cita."

# 9 · c1-m3-08
x = D["c1-m3-08"]
x["afirmacion"] = "El abanico que se abre en el gráfico estacional es la señal de un modelo multiplicativo."
x["nota"] = "FPP3 §3.2 respalda la conclusión —si la variación estacional es proporcional al nivel, el modelo es multiplicativo—, pero no la regla de lectura del gráfico estacional: §2.4 describe gg_season sin hablar de líneas paralelas ni de un abanico. Traducir el criterio a esa imagen es aportación del capítulo, que no la atribuye a nadie. Por eso la marca empieza en «Esa forma es la señal de un modelo multiplicativo»: la oración anterior, la que enseña a leer el abanico, queda fuera de la huella y la cita visible ya no la respalda a la vista. El matiz que queda es que «esa forma» remite a una imagen que la fuente no describe. No se tocó la prosa."

# 18 y 14 · c1-m4-02 absorbe a c1-m4-03 y c1-m4-04
x = D["c1-m4-02"]
x["afirmacion"] = "La lista de los cuatro componentes: tendencia, estacionalidad y ciclo, definidos como en FPP3 §2.3, y el ruido, que define el capítulo."
x["fuentes"] = [D["c1-m4-02"]["fuentes"][0], D["c1-m4-03"]["fuentes"][0], D["c1-m4-04"]["fuentes"][0], D["c1-m4-04"]["fuentes"][1], D["c1-m4-02"]["fuentes"][1]]
x["nota"] = "FUSIÓN DE IDENTIFICADORES: esta entrada absorbe a c1-m4-03 (estacionalidad) y c1-m4-04 (ciclo), que se registraron por separado y se retiraron en la corrección de la R4 por decisión de la sesión maestra: las tres viñetas llevaban la misma cita, idéntica, tres veces seguidas. La marca va ahora en la lista entera y la cita visible, una sola, al final de la viñeta de la tendencia. Las tres las contrastó el verificador del lote R4a, una por una, y las tres salieron «respaldada». FPP3 §2.3 define los TRES PRIMEROS componentes: la tendencia como aumento o descenso de largo plazo, la estacionalidad con período fijo y conocido, y el ciclo como subidas y bajadas sin frecuencia fija, ligadas por lo general a las condiciones económicas. El CUARTO, el ruido, lo define el capítulo y la cita no lo cubre, aunque la huella sí lo vigila por estar en la misma lista. Lo que el capítulo no recoge: que la tendencia no tiene por qué ser lineal y puede «cambiar de dirección», que una serie puede tener más de un patrón estacional, y que Cryer y Chan advierten de que el uso de la palabra tendencia varía entre autores. Cambio de prosa: la viñeta del ciclo decía «ciclos económicos de varios años» y tres párrafos después el capítulo dice «al menos dos años» citando la misma sección; la fuente solo dice «usually at least 2 years», así que a la viñeta se le quitó la cifra («p. ej. los ciclos económicos»). Los paréntesis de las viñetas, que la primera pasada había cambiado por rayas, vuelven a su forma original."
E[:] = [y for y in E if y["id"] not in ("c1-m4-03", "c1-m4-04")]

# 1 · c1-m4-06
x = D["c1-m4-06"]; x["tipo"] = "resultado"
x["afirmacion"] = "Al descomponer una serie suele agruparse tendencia y ciclo en un solo componente tendencia-ciclo, al que a menudo se llama simplemente tendencia."
x["fuentes"] = [web("cap. 3", "decomposition", "we usually combine the trend and cycle into a single trend-cycle component (often just called the trend for simplicity)")]
x["nota"] = "Historia de la frase. El verificador del lote R4a leyó «Muchos textos agrupan tendencia y ciclo en un solo término tendencia-ciclo» y dio «con-matiz»: la práctica está en la entrada del cap. 3 de FPP3, pero ninguna fuente leída sostiene que lo hagan «muchos textos». La primera pasada de la R4 la reescribió atribuyéndola a los dos autores con cita narrativa, y el verificador independiente lo objetó: la fuente no dice que lo hagan ellos, dice que es lo habitual («we usually»), y la cita registrada recortaba justo esas dos palabras. La frase vigente vuelve a la voz impersonal y dice lo que dice la fuente, incluido que al componente se le suele llamar simplemente tendencia. LA FRASE NUEVA LA ESCRIBIÓ EL REDACTOR DE LA R4 y no la ha leído ningún verificador: el veredicto se queda en «con-matiz» hasta que la compruebe la sesión maestra."

# 7 · c1-m8-03
x = D["c1-m8-03"]; x["veredicto"] = "respaldada"; x["verificado_por"] = VM
x["nota"] = "El verificador del lote R4a leyó «muchas estadísticas oficiales —desempleo, producción—» y dio «con-matiz», porque FPP3 no dice nada de la «producción». La primera pasada de la R4 la retiró y dejó «las de desempleo, por ejemplo». La sesión maestra comprobó la frase vigente y subió el veredicto: FPP3 §3.2 dice que los datos mensuales de desempleo se suelen desestacionalizar y que lo mismo ocurre con los de empleo «and many other economic series», y §3.5 que las oficinas de estadística tienen procedimientos propios de ajuste estacional; eso sostiene «muchas» y «las de desempleo». La única reserva: la fuente da como finalidad «highlight variation due to the underlying state of the economy», y el capítulo dice «comparar meses sin el vaivén estacional», que es su manera de decirlo. La retroalimentación de la autoevaluación del Módulo 9 decía «las cifras oficiales de empleo o PIB» (c1-m8-13 del inventario): el PIB tampoco está en FPP3 y se retiró en la corrección; esa frase vive en una cadena de JavaScript que el auditor no lee, de modo que no puede llevar marca ni entrada propia."

# 12 · c1-m6-09
x = D["c1-m6-09"]
cambia("c1-m6-09", "Calculate the detrended series: y_t - \\hat{T}_t.", "detrended series: y_t - \\hat{T}_t.")
x["fuentes"].insert(1, web("§3.4", "decomposition", "detrended series: y_t / \\hat{T}_t."))
x["nota"] = "FPP3 §3.4 da el paso 2 en las dos escalas —restar en la aditiva, dividir en la multiplicativa: de ahí las dos primeras citas— y el paso 3 como el promedio por posición. Dos cosas son del capítulo y no de la fuente. Que en la serie sin tendencia «ya solo quedan estacionalidad y ruido» no lo dice con esas palabras: se sigue del modelo que §3.2 escribe. Y el mecanismo —«el ruido se cancela y sobrevive el índice de enero»— tampoco: la fuente solo dice «simply average the detrended values for that season». La marca termina en «y así con los doce meses»; la frase siguiente, sobre la rigidez de los índices, queda fuera (está cubierta por c1-m6-01)."

# 13 · c1-m6-14
x = D["c1-m6-14"]
x["nota"] = "FPP3 §3.4 impone que los índices multiplicativos sumen m —con m = 12, media 1—. La marca termina en «…la condición de la última fila de la tabla»: que el reescalado del paso 3c esté puesto para imponerla es construcción del capítulo (FPP3 enuncia la condición sin decir cómo se impone) y quedó fuera de la huella en la corrección de la R4. Fuera quedan también la cifra 12.0001, que sale de R, y la condición aditiva. El verificador dio además la cita de la condición aditiva («…adjusted to ensure that they add to zero»), que se retiró porque la frase marcada solo habla del caso multiplicativo y por el tope de palabras citadas de FPP3 (F11)."

# 11 · c1-m6-20
x = D["c1-m6-20"]
x["fuentes"] = [web("§3.3; §3.4", "decomposition", "first step in a classical decomposition is to use a moving average"),
                web("§3.4", "decomposition", "\\hat{T}_t using a 2 \\times m-MA.")]
x["nota"] += " La cita visible lleva las dos secciones: que el método arranca con una media móvil lo dice §3.3 («The first step in a classical decomposition is to use a moving average method…»), y §3.4 es la sección del método, donde el paso 1 usa la 2×m-MA."

# 19 · c1-m7-01
x = D["c1-m7-01"]
x["afirmacion"] = "STL se desarrolla como «Seasonal and Trend decomposition using Loess»; el título del artículo original lo escribe con guion y «based on»."
x["nota"] += POST + "la lista de fuentes del módulo imprime el título del artículo, con «Seasonal-Trend» y «Based on», a dos pantallas de la forma de FPP3. Se añadió un inciso que lo dice y cita el título (Cleveland et al., 1990, p. 3), para que las dos formas no parezcan una errata. El inciso lo escribió el redactor y tampoco lo ha leído el verificador."

# 2 y 3 · c1-m7-05 y la entrada nueva c1-m7-23
x = D["c1-m7-05"]; x["veredicto"] = "con-matiz"
x["afirmacion"] = "Loess es una regresión local: para dar el valor en t toma los puntos más próximos, les ajusta una recta por mínimos cuadrados y se queda con su altura en t."
x["fuentes"] = x["fuentes"][:4]
x["nota"] = "§2.1 del artículo dice las cuatro cosas de la frase: se eligen los q valores más próximos a x, se ajusta un polinomio local, el valor devuelto es el del polinomio en x, y los pesos se anulan en el q-ésimo punto más lejano. EL MATIZ: la frase dice «les ajusta una recta por mínimos cuadrados», y el artículo dice polinomio de grado 1 o 2 («locally-linear or locally-quadratic») por mínimos cuadrados PONDERADOS. La recta es el caso que usa el capítulo, y lo de ponderados lo dice el propio capítulo tres párrafos después, como remate de la explicación; aquí todavía no. Por eso el verificador independiente bajó el veredicto de «respaldada» a «con-matiz». Historia del nombre: el capítulo desarrollaba Loess como «locally estimated scatterplot smoothing», que no está en ninguna fuente leída; la primera pasada de la R4 lo cambió aquí por «regresión local ponderada, locally weighted regression», y eso adelantaba la palabra que el capítulo revela después. En la corrección, esta primera mención glosa solo «una regresión local» y el nombre completo pasó al párrafo de «ponderada», con su propia entrada, c1-m7-23. Se retiró la cita de Shumway y Stoffer (pie de la figura 2.14) que el redactor había añadido: glosa lowess, que es otro suavizador, y en el texto en caché de ese libro la palabra «loess» no aparece."
e("c1-m7-23", "definicion", "El nombre completo de Loess: regresión local ponderada (locally weighted regression).", "respaldada", [
  pdf(CL, "p. 5", 3, "weighted regression, or loess (Cleveland and"),
], "ENTRADA NUEVA de la corrección de la R4; no está en el inventario (c1-m7-23 es el primer id libre del módulo). Sale de c1-m7-05: el verificador del lote R4b anotó allí que el artículo presenta el suavizador como «locally-weighted regression, or loess», y el verificador independiente precisó dónde: al final del §1, en la página impresa 5, y no en §2.1. El desarrollo del nombre se llevó al párrafo que revela la palabra «ponderada», y con él la cita, de ahí esta entrada. En el texto de la caché «locally-» queda a final de renglón, así que la cita literal empieza en «weighted»; el capítulo lo escribe sin guion. La frase la escribió el redactor de la R4: la comprueba la sesión maestra.", VB)

# 4 y 17 · c1-m7-07
x = D["c1-m7-07"]
x["nota"] = "Los dos valores por defecto están en la línea de uso de la ayuda de stl(): s.degree = 0 y t.degree = 1. La marca cubre solo la primera oración del párrafo de cierre del desarrollo («Los dos grados por defecto… responden a dos problemas distintos»); las dos razones que vienen después quedaron FUERA de la huella en la corrección de la R4, porque la fuente respalda los valores y no las razones. Para el docente: el párrafo explica s.degree = 0 diciendo que las subseries son cortas y que «pedirles una pendiente sería pedirle demasiado a doce puntos». Esa razón es del capítulo. El artículo original, en §2.3, paso 2, suaviza las subseries de ciclo con d = 1 (tercera cita; «andd» es como el OCR dejó «and d»): el 0 es una decisión de la implementación de R, no del artículo. La derivación no se reescribió: es una decisión que queda planteada. Los valores 1 y 0 aparecen en las oraciones de fuera de la marca; dentro queda la afirmación de que son los de la línea de uso. Cambio de prosa: la cita partía sujeto y verbo, y pasó a un inciso («—los que trae la línea de uso de stl()…—»)."

# 16 · c1-m7-10
D["c1-m7-10"]["nota"] += POST + "la cita partía «la regla» de su complemento; la frase dice ahora «con la regla que da su ayuda (…): tomar el impar inmediato de». No cambia lo que afirma."

# 10 · c1-m7-15
x = D["c1-m7-15"]
x["fuentes"] = [pdf(CL, "§2.2; §2.3", 5, "cycle-subseries of the detrended series is"),
                pdf(CL, "§2.2", 5, "subseries as cycle-subseries."),
                pdf(CL, "§2.2", 5, "January values, the second is the February"),
                rdoc("§Details", "stl", "sub-series (the series of all January values, ...); if ‘s.window ="),
                rdoc("§Details", "stl", "\"periodic\"’ smoothing is effectively replaced by taking the mean."),
                rdoc("§Arguments", "stl", "lags) of the loess window for seasonal extraction, which"),
                web("§3.6", "decomposition", "periodic season(window='periodic') (i.e., identical across years)")]
x["nota"] += POST + "la cita visible del artículo lleva ahora las dos secciones, porque §2.2 define las subseries de ciclo y es §2.3, paso 2, la que las suaviza con Loess. Y «el patrón queda fijo» no está en la ayuda de R, que solo dice que el suavizado se sustituye por la media: que con \"periodic\" el componente estacional es idéntico de un año a otro lo dice FPP3 §3.6, y se añadió esa cita, visible y literal. FPP3 habla de season(window = 'periodic') en STL() de fable, no de stl(); el argumento es el mismo."

# 5 · c1-m7-16
x = D["c1-m7-16"]
x["afirmacion"] = "Los pasos de estacionalidad y tendencia se repiten unas pocas veces: dos pasadas por defecto, con la opción robusta apagada."
x["fuentes"] = [rdoc("§Usage", "stl", "inner = if(robust)  1 else 2,")] + x["fuentes"]
x["nota"] = "La frase del inventario («Son dos bucles, uno dentro de otro: el interior alterna estacionalidad y tendencia hasta que se estabilizan…») ya no está: la R3 y la R3-bis la repartieron entre el paso 4 de «El método, paso a paso» y el párrafo del bucle exterior. Se marca el paso 4. El verificador del lote R4b dio «con-matiz» a la frase vieja, por el «hasta que se estabilizan» (el número de pasadas interiores es fijo, no un criterio de parada). EL MATIZ VIVO lo señaló el verificador independiente: la línea de uso de stl() dice inner = if(robust) 1 else 2, de modo que las dos pasadas son el valor por defecto SOLO con robust = FALSE; con la opción robusta es una pasada por cada vuelta del bucle exterior, y el capítulo enseña a encender esa opción dos pantallas más abajo. La frase decía «dos pasadas, por defecto», sin esa condición. SE CORRIGIÓ LA PROSA: «dos pasadas por defecto, con la opción robusta apagada», y la cita visible pasó a §Usage, que es donde está el valor. La frase nueva la escribió el redactor y no la ha leído ningún verificador: el veredicto se queda en «con-matiz». El artículo respalda la estructura de dos bucles anidados (§2.2); la entrada «inner» de los argumentos dice que bastan muy pocas pasadas, y su segunda cita es la continuación de la que dio el verificador. El bucle exterior lo cubre c1-m7-02. Cita sustituida: «loop followed by a computation of robust-» acababa en un guion de corte de renglón; se dejó sin «robust-»."

# tope F11: recortes para hacer sitio a las citas nuevas de FPP3
cambia("c1-m8-02", "removed from the original data, the resulting values are the “seasonally adjusted” data.", "the resulting values are the “seasonally adjusted” data.")
cambia("c1-m4-11", "does not vary with the level of the time series", "does not vary with the level")
cambia("c1-m4-11", "proportional to the level of the time series", "proportional to the level")
cambia("c1-m5-02", "equivalent to a weighted moving average of order m + 1", "weighted moving average of order m + 1")
cambia("c1-m7-01", "acronym for “Seasonal and Trend decomposition using Loess”", "“Seasonal and Trend decomposition using Loess”")
cambia("c1-m4-07", "is actually part of a long cycle", "part of a long cycle")
cambia("c1-m6-13", "trend-cycle component \\hat{T}_t using a 2 \\times m-MA.", "using a 2 \\times m-MA.")
