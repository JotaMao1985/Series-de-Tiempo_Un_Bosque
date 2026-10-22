---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: 6
fecha: 2026-10-21
estado: PUBLICADO (2026-10-21), con el visto bueno de Javier
---

# Plan · Guía del proyecto de pronóstico — Corte III, con opción conjunta con Estadística Espacial

Series de Tiempo 2026-II (20948) · Corte III · Universidad El Bosque

El sílabo pone en el Corte III un **proyecto de pronóstico**: la propuesta se presenta en la semana 13
y la sustentación y la entrega en la 16, con un peso del **20 % del Corte III**. Hoy no hay nada publicado
que lo sostenga, salvo el bloque «Guía del proyecto de pronóstico» del **Módulo 12 del capítulo 6**, con
sus «Seis exigencias del informe». Esta ronda publica la guía como documento propio del sitio:
`Htmls_Series/proyecto-pronostico-corte-iii.html`, más una plantilla `.Rmd` descargable. Sigue el modelo
del proyecto aplicado de Diseño de Experimentos (`../Diseno de experimentos/PLAN_Proyecto_Aplicado.md`,
publicado el 9 oct y auditado el 20 oct) y le añade algo que Diseño no tiene: **una opción conjunta con
Estadística Espacial (20929)**. Con ella, quien curse las dos materias presenta un solo proyecto y recibe
dos notas.

## 0. Estado

- 2026-10-21: plan propuesto. **Nada construido.** Las decisiones D1–D14 son propuestas por defecto, casi
  todas heredadas de Diseño, y se aprueban con el plan. **P1–P3 (§4) son de Javier** y bloquean las fechas
  y el peso.
- 2026-10-21: **P1 cerrada por Javier: la última semana de clases va del 16 al 21 de noviembre.** Vale la
  numeración de los planes de Series y Espacial (la semana 10 es la del 5 al 9 de octubre), no la de Diseño.
  El calendario de §5 está rehecho con esa cuenta.
- 2026-10-21: **P2 y P3 cerradas por Javier**, con la opción recomendada en las tres preguntas:
  - **P2:** el proyecto vale el **50 % del Corte III** y el otro 50 % son quices en clase. **No hay examen final
    ni Talleres 4 y 5.** Con el Corte III al 40 % del curso, el proyecto es el **20 % de la nota final**.
  - **P3:** la conjunta va, con **solo las preguntas (a) y (b)**. La (c), de kriging, se retira.
  - **El proyecto pesa en Espacial lo mismo que en Series**: el 50 % de su Corte III.
  - Las decisiones D1–D14 quedan aprobadas con el plan. Lo siguiente es T1.
- 2026-10-21 (noche): **T1–T9 hechas; sin publicar ni commitear.** Comandos y detalle en `proyecto/README.md`.
  - `proyecto/datos.py`, los diez módulos y `plantilla-informe.Rmd`; `precalculo/ensambla_proyecto.py`
    (210 KB, 31 comprobaciones propias).
  - `proyecto/audita_proyecto.py`: 0 fallos en ocho frentes, A–H (G vigila las exigencias del 6.12; H, la
    conjunta). `prueba_audita_proyecto.py`: 47 defectos, 47 cazados por su frente. El control inicial corre
    con R, porque sin R no se vio un falso positivo del frente E.
  - Navegador por HTTP: diez módulos sin errores de consola, KaTeX compuesto, 375 px sin desborde, el enlace
    del 6.12 abre en el módulo 12.
  - T6 y T7 verificados en su sitio (el cap. 6 reensamblado cambia solo en las seis líneas del enlace;
    `cuenta_sitio.py` en verde) y **después retirados** con todo lo construido en `Htmls_Series/`: viven en
    `proyecto/publicacion.patch`. Hay cambios ajenos sin commit en el cap. 4, y un `subtree push` de otra
    sesión se llevaría la guía a medias.
  - T8 en `proyecto/RESISTENCIA_IA.md`: una entrega fabricada en 7 minutos saca **4,10 en lo escrito** en
    frío, y **1,74 con el tope** si no sabe defenderla. La medición destapó un error de la plantilla
    (`fitdf` contaba la deriva) y la pérdida del Diebold–Mariano (power = 2 con el MASE): los dos
    corregidos. Quedan tres propuestas para Javier, entre ellas volver a descargar la serie.
- 2026-10-21: **Javier aprueba la cláusula de volver a descargar la serie** (si no coincide, P1 e I7 en
  insuficiente; las revisiones que la fuente documente después de la fecha de corte no cuentan) **y la
  publicación.** Va en el módulo 2 y en los descriptores de P1 e I7; el auditor la vigila (frente C) y el arnés
  pasa a 49 defectos, 49 cazados. Publicada: commit en `main` por ruta (el cap. 4 de otra sesión queda fuera) y
  `subtree push` a `gh-pages`. Las otras dos propuestas de `RESISTENCIA_IA.md` (cobertura por horizonte,
  imputar con el pasado) siguen sin aplicar.

## 1. El hueco

| | Carencia | Consecuencia si no se cierra |
|---|---|---|
| C1 | No hay guía del proyecto: solo las seis exigencias del cap. 6, M12 | Sin hitos, rúbrica ni canal, el proyecto se entrega en la semana 16 sin control intermedio |
| C2 | No hay fechas: el sílabo dice «semana 13» y «semana 16», sin día | Las dos numeraciones de semanas en uso difieren en una semana; cerrado con P1 (§5) |
| C3 | No hay rúbrica ni regla de defensa | El proyecto no tendría la contramedida de los talleres (el tope de las preguntas) frente a una entrega hecha con IA |
| C4 | La propuesta del protocolo de evaluación no se congela antes de ver resultados | El cap. 6 (M6 y M10) enseña que una métrica o una partición elegidas después son fuga de información; el proyecto no lo exigiría |
| C5 | No existe la opción conjunta ni su autorización por escrito | Presentar el mismo trabajo en dos cursos sin autorización escrita es autoplagio |
| C6 | Espacial no tiene guía de proyecto, y su sílabo ponía la propuesta en la semana 10, que ya pasó | La parte espacial de la conjunta no tiene rúbrica que la califique (T11) |

## 2. Restricciones verificadas antes de planear

- **Quién cruza las dos materias** (exportaciones de notas de Brightspace del Corte 1 y de la prueba
  diagnóstica, cruzadas por `OrgDefinedId` el 2026-10-21): Series tiene **9** estudiantes y Espacial **12**;
  **5 están en las dos**. Con Diseño solo se cruza **1** de Series. Para la conjunta, el tope son dos parejas
  y una persona sola.
- **Los dos sílabos son compatibles con un solo trabajo.** Series pide un «proyecto de pronóstico» y Espacial
  un «proyecto integrador sobre un territorio real con datos abiertos». Los dos valen el 20 % del Corte III y
  los dos se sustentan en la semana 16.
- **El contenido que la guía puede exigir ya está publicado.** El cap. 5 cubre SARIMA y variables exógenas, y
  el cap. 6 los métodos de referencia, el RMSE, el MAE, el MAPE y el MASE, el origen móvil, Diebold–Mariano, la
  cobertura y Winkler, y el taller de auditoría de IA. En Espacial están publicados los caps. 1–7: pesos
  espaciales y autocorrelación espacial (este último, el 2026-10-20). Faltan el 8 (econometría), el 9
  (geoestadística) y el 10 (ML espacial y proyecto integrador).
- **El M12 del cap. 6 ya le promete al estudiante seis exigencias**: fuente y fecha de corte; al menos un método
  de referencia; la métrica elegida antes de ver resultados (MASE por defecto); el origen móvil con orígenes,
  horizonte y ventana declarados; la cobertura al 80 % y al 95 %; y el diagnóstico (Ljung–Box, normalidad y
  raíces), además de la nota sobre la IA. La guía no puede contradecirlas. Cada una se vuelve un criterio de la
  rúbrica (D13).
- **Días de clase:** Series, martes y miércoles (Taller 2 defendido el martes 13 y Parcial 2 el miércoles 14 de
  octubre). Espacial tuvo su Parcial 2 el jueves 15 de octubre. Las tutorías son martes y viernes de 11:00 a
  13:00 y jueves de 14:00 a 16:00 (memoria de Diseño `calendario-curso-2026-ii`).
- **El repositorio es público y va a Pages.** La guía no lleva clave ni secreto, así que este plan se versiona.
  El producto de la prueba de resistencia a la IA (T8) **no** se versiona, como en Diseño.
- **Riesgo de reensamblado** (memoria `series-tiempo-riesgo-reensamblado`): el enlace desde el M12 del cap. 6
  se escribe en `ensamblado/cap6/` y no en el HTML. Si se escribe en el HTML, se borra en el siguiente
  reensamblado.

## 3. Decisiones de esta ronda — propuestas por defecto

Todo lo que lleva cifra vivirá en `proyecto/datos.py` como constante, igual que en Diseño. La columna
«Origen» indica de dónde viene cada decisión.

| | Decisión | Origen | Coste / consecuencia |
|---|---|---|---|
| **D1** | **Individual o en parejas** (máximo 2) | Diseño D1 | Hasta 9 proyectos en Series |
| **D2** | **Qué serie vale.** Una serie real y pública, con fuente citable y fecha de descarga, y de longitud suficiente para el origen móvil: **n ≥ T₀ + h + 9** (10 orígenes como mínimo), con **T₀ ≥ máx(4m, 30)** (cuatro ciclos para entrenar y nunca menos de 30 observaciones; el piso de 30 se añadió al construir, para las series sin estación o trimestrales). Para una serie mensual con h = 12, n ≥ 69. **No valen** las series del material, de los talleres o de los paquetes de R (`AirPassengers`, `USAccDeaths`, `co2`, `nottem`…), ni las series simuladas. La estacionalidad se recomienda, no se exige: sin ella, el SARIMA del cap. 5 queda fuera | Nueva (equivale al «Qué experimento vale» de Diseño) | La longitud mínima sale del ejercicio 1 del M12: con 72 observaciones, el *airline* estima dos parámetros con poco más de 20 datos efectivos en los primeros orígenes |
| **D3** | **Cuatro hitos y una exposición**: ficha (sin nota), preregistro, avance, informe y código. Las fechas están en §5 (P1 cerrada) | Diseño D3 | La ficha cae en la semana 13, la de la «presentación de la propuesta» del sílabo. De la ficha al informe hay menos de tres semanas, contra las cinco de Diseño |
| **D4** | **Exposición en clase**: 10 min y 5 de preguntas por equipo (15 y 10 en la conjunta, D11). El orden se sortea y, en las parejas, un dado decide quién responde cada pregunta. El día exacto se acuerda en clase | Diseño D4 y D12 | Con 9 estudiantes caben en una sesión |
| **D5** | **Documento propio, no anexo**, con prefijo `proyecto-*`. Se construye como el Taller 2 y el proyecto de Diseño: `datos.py`, módulos con marcadores `@@CLAVE@@`, ensamblador con `--revisar`, auditor por frentes y arnés de defectos | Diseño D5 | La guía hay que añadirla a la portada y a la lista explícita de documentos de `cuenta_sitio.py`, que no va por prefijo |
| **D6** | **Reparto interno 15 · 10 · 45 · 30** (preregistro · avance · informe · exposición), con tres niveles: insuficiente 1,0 · aceptable 3,5 · sólido 5,0. La rúbrica está en §6 | Diseño D6 | El peso en el corte lo cerró P2: 50 % del Corte III, el 20 % de la nota final |
| **D7** | **Las preguntas acotan lo escrito**: lo escrito de cada persona se multiplica por **min(1, nota de las preguntas / 3,0)**. En pareja, cada integrante responde al menos una pregunta | Diseño D7 (regla de los talleres) | Es la contramedida frente a una entrega fabricada con IA (T8) |
| **D8** | **El canal es un repositorio privado de GitHub por equipo**, con el docente (`JotaMao1985`) como colaborador. Cada hito es una release con su etiqueta (`ficha`, `preregistro`, `avance`, `informe`). Cuenta la hora en que GitHub publica la release, y la release congela lo entregado. Entregas a las **11:00** | Diseño D8 y D10 | El repositorio se llama `proyecto-st-apellido1-apellido2` (`proyecto-st-ee-…` en la conjunta) |
| **D9** | **Entrega tardía: −15 % de la nota original por cada sesión de retraso**, contando la primera desde el cierre | Diseño D11 | La exposición no se puede atrasar |
| **D10** | **El preregistro congela el protocolo de evaluación** antes de tocar el tramo de prueba: horizonte, métrica y su porqué, T₀, número de orígenes, ventana (creciente o deslizante), método de referencia, candidatos y nivel de los intervalos. Cambiarlo después **se permite si se declara**, con la razón, en la sección de desviaciones del informe. Lo que se sanciona es cambiarlo en silencio (criterio I7) | Nueva: es la fuga de información del cap. 6, M6 y M10, llevada al proyecto | Hay que enseñar a separar en el repositorio lo exploratorio de lo confirmatorio (Diseño D10 ya lo hace) |
| **D11** | **La opción conjunta con Estadística Espacial**, con las reglas de §7: dos notas y dos rúbricas sobre un entregable, una pregunta que necesite las dos dimensiones, solo para quien curse las dos materias, una sola defensa con el tope aplicado por materia y autorización explícita escrita en la guía | Nueva | P3 la aprobó con solo las preguntas (a) y (b), y con el mismo peso en las dos materias. Depende de T11 |
| **D12** | **Las reglas de la conjunta se escriben en un solo sitio**: el módulo 8 de esta guía. La guía de Espacial lo **enlaza**, no lo copia | Memoria `componentes-injertados-entre-cursos` | Si Espacial cambia una regla de la conjunta, el cambio se hace aquí |
| **D13** | **Las seis exigencias del M12 se vuelven criterios** (§6) y la guía se enlaza desde ese bloque del cap. 6, editando `ensamblado/cap6/` | Nueva | Hay que reejecutar `ensambla_cap6.py`, que escribe directamente y reproduce el capítulo byte a byte, y comprobar con `git diff` que solo cambia ese enlace |
| **D14** | **IA permitida y declaración obligatoria** (criterio I8): qué herramienta, para qué, qué produjo y qué se verificó, con un ejemplo. Se mide la resistencia a la IA como en Diseño (T8) | Diseño D7 e I6, y el cap. 6, M11 | En Diseño, I6 dio «sólido» a una declaración falsa. El descriptor de I8 exige el ejemplo verificable, no solo la forma |

## 4. Pendientes de Javier — bloquean

| | Pregunta | Por qué bloquea | Propuesta por defecto |
|---|---|---|---|
| ~~P1~~ | ~~¿Cuál es la última semana de clases?~~ **Cerrada el 2026-10-21 (Javier): del 16 al 21 de noviembre.** Diseño cuenta el receso del 5 al 10 de octubre como semana 9 y pone su semana 16 del 23 al 28; los planes de Series y Espacial llaman semana 10 a la del 5 al 9 de octubre, y es esta cuenta la que vale | Fijaba las cinco fechas de §5 | — |
| ~~P2~~ | ~~¿Cuánto vale el proyecto en el Corte III?~~ **Cerrada el 2026-10-21 (Javier): el 50 %, y el otro 50 % son quices en clase; sin examen final ni Talleres 4 y 5**, como en Diseño (D13–D14). Las otras opciones eran el 40 % con examen (con el proyecto absorbiendo los Talleres 4 y 5) y el 20 % del sílabo. Del Corte III no había nada construido: ni el Quiz 3, ni los talleres, ni el examen. El sílabo, que está fuera del proyecto, sigue diciendo examen 50 · proyecto 20 · talleres 10 + 10 · quiz 10; corregirlo allá le toca a Javier | Fijaba la tabla de pesos del módulo 1 | — |
| ~~P3~~ | ~~¿En qué términos va la conjunta?~~ **Cerrada el 2026-10-21 (Javier): sí, con solo las preguntas (a) y (b)**, las mismas fechas en las dos materias, una sola defensa y la rúbrica espacial en la guía de Espacial antes del preregistro (T11). **El proyecto pesa en Espacial lo mismo que en Series, el 50 % de su Corte III**, para que la conjunta no premie descuidar ninguna de las dos mitades. Cómo se reparte el otro 50 % del Corte III de Espacial se decide en T11 | Sin la guía de Espacial, quien elija la conjunta en la ficha no sabe cómo se le califica la mitad espacial | — |

## 5. Calendario (P1 cerrada: semana 16 = 16–21 de noviembre)

Semanas del curso con la numeración de Series: la 12 va del 19 al 24 de octubre (la de hoy), la 13 del 26 al 31,
la 14 del 2 al 7 de noviembre, la 15 del 9 al 14 y la 16 del 16 al 21. Series tiene clase los martes y miércoles.

| Hito | Semana | Fecha | Hora | Qué se entrega |
|---|---|---|---|---|
| Ficha (sin nota) | 13 | martes 27 de octubre | 11:00 | Unas 150 palabras: la serie, la fuente, la frecuencia, la longitud, la pregunta y si es conjunta |
| Preregistro | 14 | martes 3 de noviembre | 11:00 | El protocolo de D10 congelado, más la descarga cruda y su fecha |
| Avance | 15 | martes 10 de noviembre | 11:00 | Exploración, descomposición, estacionariedad, candidatos ajustados sobre el tramo de entrenamiento y desviaciones |
| Informe y código | 15 | **domingo 15 de noviembre** | 11:00 | El informe reproducible desde el repositorio |
| Exposición | 16 | martes 17 o miércoles 18 de noviembre | en clase | El día exacto se acuerda en clase |

- **Los días de la semana están comprobados con `datetime`.** El lunes 2 y el lunes 16 de noviembre son festivos y
  no se usan. Por eso el informe va el **domingo 15**, la víspera del festivo, como el Taller 2 se entregó un
  domingo. La hora es la misma de los demás hitos (D8), no las 12:30 del Taller 2: una sola hora para todo.
- **Del avance al informe hay cinco días.** Es lo más apretado del calendario. Se sostiene porque el preregistro
  ya fija el protocolo el 3 de noviembre: el código del origen móvil se puede escribir desde ese día, y el avance
  solo pide lo del tramo de entrenamiento. La guía lo dice en el módulo 6 («el avance no es un borrador del
  informe»).
- **El contenido que se evalúa llega a tiempo, pero justo.** El sílabo da el pronóstico y los intervalos en la
  semana 13, las métricas en la 14 y el origen móvil en la 15, y el cap. 6 está publicado entero desde antes.
  El preregistro (semana 14) exige declarar el origen móvil antes de que se vea en clase. La guía remite al
  cap. 6, M7, y la ficha recibe respuesta en la clase del miércoles 28.
- **La semana 16 es solo de exposiciones.** P2 quitó el examen final, así que el martes 17 y el miércoles 18
  quedan libres para exponer. Los quices en clase del otro 50 % del corte van en las semanas 12–15, fuera de este
  plan.
- La guía tiene que estar publicada **antes del viernes 23 de octubre** para que la ficha tenga su semana.

## 6. La rúbrica (propuesta: criterios y puntos; los descriptores se escriben en T1)

| Hito | Criterio | Puntos | Exigencia del M12 que lo origina |
|---|---|---|---|
| Preregistro (15) | P1 · La serie y su fuente: origen, fecha de corte, frecuencia, longitud y huecos | 4 | Fuente y fecha de corte |
| | P2 · El protocolo de evaluación: h, métrica y su porqué, T₀, orígenes, ventana y referencia | 7 | Métrica decidida antes; origen móvil declarado; método de referencia |
| | P3 · Los candidatos y el plan de diagnóstico | 4 | Diagnóstico |
| Avance (10) | A1 · Exploración: descomposición, transformación, estacionariedad y diferencias justificadas | 5 | (caps. 1–2) |
| | A2 · Identificación y candidatos sobre el entrenamiento, con las desviaciones del plan | 5 | (caps. 3–5) |
| Informe (45) | I1 · El modelo final y su justificación | 6 | |
| | I2 · Corrección técnica en R: estimación, órdenes y raíces | 8 | Diagnóstico (raíces) |
| | I3 · Diagnóstico de residuales: Ljung–Box con sus gl, normalidad y lectura de lo que se vio | 6 | Diagnóstico |
| | I4 · Evaluación por origen móvil frente a la referencia, con Diebold–Mariano | 8 | Origen móvil; método de referencia |
| | I5 · Intervalos: cobertura al 80 % y al 95 % y Winkler | 5 | Cobertura a los dos niveles |
| | I6 · Interpretación y conclusión en el lenguaje del problema, con sus límites | 5 | «Si el modelo no le gana, hay que decirlo» |
| | I7 · Fidelidad al preregistro y reproducibilidad desde el repositorio | 4 | Fuente y fecha de corte (reproducible) |
| | I8 · Declaración de uso de IA con un ejemplo verificado | 3 | Nota sobre la IA |
| Exposición (30) | E1 · La exposición | 12 | |
| | E2 · Las preguntas (individual) | 18 | |
| **Total** | | **100** | |

Sumas: 4 + 7 + 4 = 15 · 5 + 5 = 10 · 6 + 8 + 6 + 8 + 5 + 5 + 4 + 3 = 45 · 12 + 18 = 30. El auditor las recalcula
(frente B). Los criterios P1–P3 del preregistro siguen la nomenclatura de Diseño y no tienen que ver con los
pendientes P1–P3 de §4.

## 7. La opción conjunta con Estadística Espacial (módulo 8 de la guía)

1. **Quién.** Quien curse las dos materias. Puede ser individual o en pareja, pero en la pareja **los dos**
   cursan las dos. No hay parejas mixtas: la doble nota no se puede repartir entre alguien que solo está en
   una de las materias.
2. **Datos.** Un **panel abierto**: N unidades espaciales (áreas o estaciones) × T periodos, con fuente citable.
   Mínimos de Series: **la serie de al menos una unidad, o el agregado, cumple D2** y se modela con el protocolo
   completo de D10. Los mínimos espaciales (N de áreas o de estaciones, tipo de dato) los fija la guía de
   Espacial. La propuesta es N ≥ 25 áreas para que el Moran por permutación tenga sentido.
3. **La pregunta tiene que necesitar las dos dimensiones.** Se elige una de estas dos o se propone otra en la
   ficha, con aprobación. La (c) se retiró con P3 y queda aquí tachada, para que no vuelva sin decisión:
   - **(a) ¿Los errores de pronóstico tienen estructura espacial?** El mismo protocolo (la referencia y un
     ARIMA o SARIMA automático) se aplica a cada unidad, se calcula el MASE por origen móvil de cada una y se
     prueba Moran global y LISA sobre esos MASE. Usa el cap. 6 de Series y el cap. 7 de Espacial, los dos
     publicados.
   - **(b) ¿Los vecinos ayudan a pronosticar?** Una regresión con errores ARIMA (cap. 5, variables exógenas)
     con el rezago espacial de la serie, **W y** con rezago **≥ h**, como regresor, frente al mismo modelo sin
     él, por origen móvil y Diebold–Mariano. Si el rezago es menor que h, se usa el futuro de los vecinos: es
     la fuga del cap. 6, M6, y la guía lo dice en un recuadro de advertencia.
   - ~~**(c) Pronosticar el territorio.** Se pronostica en las estaciones y se interpola el pronóstico, o su
     error, por kriging.~~ **Retirada con P3.** Depende del cap. 9 de Espacial, que el sílabo da en la semana 15,
     y el informe se entrega el domingo 15 de noviembre, al cierre de esa misma semana. Una propuesta propia que
     dependa del kriging tiene el mismo problema.
4. **Dos notas y dos rúbricas sobre un entregable.** Series califica la parte temporal con la rúbrica completa
   de §6. El puente entra en I6. Espacial califica la parte espacial con la rúbrica de su guía. Si falta una de
   las dos partes, cae la nota de esa materia y no la de la otra. **El proyecto pesa lo mismo en las dos: el
   50 % del Corte III** (P3).
5. **Tamaño.** Unas 1,5 veces un proyecto simple: informe de hasta **15 páginas** (10 en el simple) y exposición
   de **15 min** más **10 de preguntas**, con al menos tres preguntas de cada materia.
6. **Una defensa, dos topes.** La nota de E2 en Series sale solo de las preguntas de Series, y la de Espacial
   solo de las de Espacial. D7 se aplica a cada materia por separado.
7. **Un repositorio y las mismas releases.** El repositorio es `proyecto-st-ee-apellido1-apellido2`. Las dos
   materias califican la misma release, en las fechas de §5, que Espacial adopta (P3).
8. **Cambiar de opción.** Se puede pasar de la conjunta al proyecto simple **hasta el preregistro**. Después, no.
9. **La autorización, por escrito.** La guía dice que esta es la **única** situación en que un mismo trabajo
   cuenta en dos cursos. Fuera de ella, presentar en Series un trabajo de otra materia es autoplagio.

## 8. Estructura de la guía (10 módulos)

| Módulo | Título | Origen |
|---|---|---|
| m1 | Cómo funciona: hitos, entrega tardía, pesos, el tope | Diseño m1, con las cifras de Series |
| m2 | Qué serie vale | Nuevo (D2) |
| m3 | El repositorio en GitHub | Diseño m3, casi tal cual |
| m4 | La ficha | Diseño m4, adaptado |
| m5 | El preregistro: el protocolo de evaluación | Nuevo (D10), con el código de `tsCV` y de la partición |
| m6 | El avance | Nuevo |
| m7 | El informe: estructura, que corra entero, declaración de IA, los errores que más cuestan | Diseño m7, con los errores de Series: Ljung–Box con gl mal puestos, una sola partición, MAPE cerca de cero, un solo nivel de cobertura |
| m8 | La opción conjunta con Estadística Espacial | Nuevo (§7) |
| m9 | La exposición | Diseño m8, con la variante conjunta |
| m10 | La rúbrica | Desde `datos.py` |

## 9. Tareas

| | Tarea | Tamaño | Depende de |
|---|---|---|---|
| T0 | ~~Cerrar P1–P3 con Javier~~ Hecha el 2026-10-21 | — | — |
| T1 | `proyecto/datos.py`: calendario, canal, pesos, rúbrica con descriptores, tope y retraso, portado del de Diseño | M | T0 |
| T2 | Los diez módulos en `proyecto/modulos/` | L | T1 |
| T3 | `proyecto/plantilla-informe.Rmd`: secciones que siguen la rúbrica, esqueleto de `tsCV`, MASE, cobertura y Winkler, con `forecast` como en el cap. 6 | M | T1 |
| T4 | `precalculo/ensambla_proyecto.py` sobre `plantilla/plantilla-capitulo.html`, con `--revisar` | M | T2 |
| T5 | `proyecto/audita_proyecto.py` y `prueba_audita_proyecto.py`: frentes A (calendario y días de la semana; ningún hito en festivo), B (pesos y sumas; proyecto + quices = 100 % del corte, y el examen final y los Talleres 4 y 5 solo se nombran para decir que no los hay), C (decisiones), D (estructura), E (el R de la guía corre en un R limpio y la plantilla renderiza con `rmarkdown`), F (contenido), **G** (cada exigencia del M12 tiene su criterio y nada la contradice) y **H** (la conjunta: elegibilidad, dos topes, fechas iguales, la autorización escrita) | L | T4 |
| T6 | Enlace a la guía desde el M12 del cap. 6, en `ensamblado/cap6/templates_10_12.html`; reejecutar `ensambla_cap6.py` y comprobar con `git diff` que solo cambia eso | S | T4 |
| T7 | Tarjeta en el Corte III de `Htmls_Series/index.html` y la guía en la lista de documentos de `cuenta_sitio.py` | S | T4 |
| T8 | Prueba de resistencia a la IA, como `RESISTENCIA_IA.md` de Diseño: una entrega fabricada, calificada en frío. El producto **no** se versiona | M | T5 |
| T9 | Navegador por HTTP (no `file://`): los diez módulos sin errores de consola, KaTeX compuesto, 375 px sin scroll horizontal | S | T5 |
| T10 | Publicar a `gh-pages` (subtree push) con el visto bueno de Javier y comprobar en el sitio | S | T9 |
| T11 | **Lado de Espacial** (otro repositorio, otra sesión): su guía de proyecto con la rúbrica de la parte espacial y un enlace al m8 de esta guía, antes del 3 de noviembre | L | P3 |
| T12 | Vault: bitácora de cada sesión y nota del cap. 6 (*Pendiente* y *Enlaces*) | S | — |

## 10. Criterios de aceptación

- `audita_proyecto.py` en verde y el arnés caza todos sus defectos, cada uno con su frente.
- Ninguna cifra de la guía está escrita a mano: todas salen de `datos.py`, y el R de la guía se ejecuta.
- Las seis exigencias del M12 aparecen como criterios y la guía no contradice ninguna (frente G).
- Tras reejecutar `ensambla_cap6.py`, `git diff` del cap. 6 muestra como único cambio el enlace del M12.
- La conjunta dice por escrito quién puede elegirla, cómo se califica en cada materia y que es la única
  excepción al autoplagio (frente H).
- Publicada antes del viernes 23 de octubre, o con la ficha corrida en la misma cantidad de días si no se llega.

## 11. Riesgos

- **El tiempo.** Hay dos días hábiles para construir, auditar y publicar antes de que la ficha tenga su semana.
  Si no se llega, se corre la ficha y no se recorta la auditoría. Para los estudiantes, entre la ficha y el
  informe hay 19 días (del 27 de octubre al 15 de noviembre), contra los 38 de Diseño (del 16 de octubre al
  23 de noviembre). Por eso el proyecto no puede pedir más que el de Diseño, y la conjunta lo agrava.
- **La conjunta sin la guía de Espacial.** Quien la elija en la ficha lo hace sin la rúbrica espacial. Se
  mitiga con los mínimos de §7, con la posibilidad de cambiar de opción hasta el preregistro y con T11 antes
  de esa fecha.
- **El material de Espacial que llega tarde.** Con la (c) retirada, las dos preguntas que quedan usan lo que ya
  está publicado: la (a) usa Moran y LISA (cap. 7) y la (b) la matriz de pesos (cap. 6). Una propuesta propia
  que dependa de la econometría (cap. 8) o del kriging (cap. 9) llega tarde y no se aprueba en la ficha.
- **Datos fabricados.** Es menos probable que en Diseño, porque la serie es pública y el docente la puede
  descargar de nuevo en la fecha de corte declarada. Aun así, T8 lo mide.
- **Sesiones concurrentes en el mismo árbol** (memoria `sesiones-concurrentes-mismo-arbol`): hoy hay cambios
  ajenos sin commit en `capitulo-4-modelos-arima.html` y `ensamblado/cap4/templates_10.html`. Esta ronda no
  los toca, y el reensamblado de T6 se limita al cap. 6.

## 12. Enlaces

- Modelo: `../Diseno de experimentos/PLAN_Proyecto_Aplicado.md` · `../Diseno de experimentos/proyecto/README.md` ·
  `../Diseno de experimentos/proyecto/RESISTENCIA_IA.md`
- Sílabos: `../Syllabus/20948_Syllabus_Series_de_Tiempo_2026-II.pdf` (semanas 13–16) ·
  `../Syllabus/20929_Syllabus_Estadistica_Espacial_2026-II.pdf` (semanas 10 y 16)
- [[20948-06 Pronóstico y evaluación]] (M12) · [[20929-10 ML espacial y proyecto integrador]] ·
  [[PLAN_Material_Series_de_Tiempo]]
