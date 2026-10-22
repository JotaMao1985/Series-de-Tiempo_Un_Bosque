# Prueba de resistencia a la IA — proyecto de pronóstico del Corte III

**Medida:** 2026-10-21, antes de publicar la guía (T8 de `PLAN_Proyecto_Pronostico.md`). Es la misma
medición que se hizo con el proyecto de Diseño (`../Diseno de experimentos/proyecto/RESISTENCIA_IA.md`).

> **El principio no cambia:** la IA está permitida, y la contramedida es la defensa oral con su tope, no la
> dificultad del escrito. Esta medición dice cuánto protege esa defensa en un proyecto donde el estudiante
> elige la serie y la descarga él mismo.

## Cómo se hizo

Un agente recibió solo la guía y la plantilla y fabricó en unos **7 minutos** de reloj (más la lectura) un
proyecto simple completo. La entrega incluía:

- la ficha, el preregistro con sus diez campos, el avance y el informe renderizado;
- una serie **simulada en R**, presentada como el acopio mensual de leche de una entidad real, con un enlace
  y una nota metodológica inventados y una descarga cruda que imita un export de Excel;
- diez commits con fechas puestas a mano entre el 26 de octubre y el 15 de noviembre;
- una declaración de IA falsa que cita un commit que no existe.

El preregistro se escribió sabiendo ya que el modelo le ganaba a la referencia. **Otro agente calificó la
entrega en frío** con la rúbrica del módulo 10, sin saber que era fabricada: clonó el repositorio, lo
reprodujo y comprobó sus cifras en R. Lo que el agente que fabricó dice de su propia entrega solo sirve de
contraste. Lo producido quedó en el directorio temporal de la sesión y no se versiona, porque es un ejemplo
de fraude completo listo para copiar.

## El resultado, sin adornos

**Lo escrito saca 4,10 de 5** (preregistro 5,0 · avance 4,25 · informe 3,77), con sólido en 7 de los 13
criterios. El preregistro, que es lo más fácil de fabricar después de los hechos, saca la nota máxima.

| Si en la defensa las preguntas sacan | Exposición | Nota sin tope | **Nota con tope** |
|---|---|---|---|
| 1,0 (no sabe explicar nada) | 5,0 | 3,65 | **1,74** |
| 2,25 (una aceptable y una insuficiente) | 3,5 | 3,69 | **2,98** |
| 3,5 (las explica) | 3,5 | 3,92 | **3,92** |

Calculado con la fórmula de la guía: lo escrito vale 70 puntos, E1 12 y E2 18, y el tope es
min(1, preguntas / 3,0). **El tope hace su trabajo**: una entrega fabricada que no se sabe defender cae por
debajo de 2.

## Lo que la calificación en frío vio y lo que no vio

**Lo vio** porque comprobó en vez de leer:

- el commit que cita la declaración de IA no existe;
- el `informe.html` dice 21 de octubre mientras su commit dice 15 de noviembre;
- los grados de libertad del Ljung–Box, el MA estacional sobre el círculo unidad (−0,999), una PACF mal
  leída y un rechazo de normalidad que es un artefacto de los doce primeros residuos con D = 1.

**No lo vio:** que la serie es inventada. Desde el texto no se nota. Solo se nota intentando descargarla
de la fuente citada, que es justo lo que la serie pública hace posible y lo que el proyecto de Diseño no
tenía.

## Lo que cambió en la guía por esta medición

1. **Un error real de la plantilla.** `fitdf = length(coef(modelo))` cuenta la deriva y los regresores, que
   no son parámetros ARMA: con deriva, el Ljung–Box daba 21 grados de libertad en vez de 22. La plantilla
   cuenta ahora p + q + P + Q con `arimaorder()` (también en modelos sin estación, donde no trae P y Q). El
   módulo 7 avisa del error, y el auditor y su arnés lo vigilan.
2. **La pérdida del Diebold–Mariano sigue a la métrica.** La guía y la plantilla usaban `power = 2` con el
   MASE; ahora usan `power = 1` y dicen cuándo va `power = 2`. El módulo 7 lo añade a los errores que más
   cuestan.

## Lo que se propone y no se aplicó (decide Javier)

- **Volver a descargar la serie.** La guía podría decir que el docente vuelve a descargar la serie de la
  fuente citada en la fecha de corte declarada, y que si no coincide, P1 e I7 quedan en insuficiente. Es la
  única comprobación que caza una serie inventada, y anunciarla basta para disuadir.
- **La cobertura por horizonte.** La fabricada promediaba la cobertura en los doce horizontes y escondía que
  caía del 78 % al 69 %. Se podría pedir la tabla por horizonte en I5.
- **Imputar solo con el pasado.** `na.interp` sobre la serie entera imputa un hueco con datos posteriores,
  una fuga menor si el hueco cae en el tramo de evaluación. Cabe una línea en el módulo 6.

## Preguntas de la defensa que funcionaron

Las cinco que propuso la calificación en frío son preguntas sobre los *porqués* de la propia entrega, y
ninguna se contesta sin haber hecho el trabajo: qué parámetros cuenta el `fitdf`, qué significa un MA
estacional de −0,999 para D = 1, por qué un AR(1) con la PACF fuera de la banda en el rezago 2, por qué la
referencia cubre de menos lo mismo que el modelo, y que muestre el commit que cita su declaración.
