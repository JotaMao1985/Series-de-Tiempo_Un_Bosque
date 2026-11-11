---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-01 Componentes y descomposición]]"
fecha: 2026-11-10
estado: aprobado
---

# Plan — Mejora del capítulo 1 · Componentes y descomposición (Fase 1)

**Objetivo:** dejar el capítulo 1 correcto, con sus fuentes contrastadas, con un hilo que no
prometa lo que no muestra, con gráficas que se lean y con práctica para cada objetivo que
declara. Es la primera aplicación del sistema de [[PLAN_Gestion_Documental]] a un capítulo entero
y el molde para los otros cinco.

**Estado: aprobado por Javier el 2026-11-10 (D1–D9). R1 y R2 publicadas el 2026-11-11; sigue R3.** Lo que sigue es el diagnóstico y el plan;
las rondas se registran en §4.

## 1. El hueco — diagnóstico del 2026-11-10

Cinco lecturas independientes, cada una con su lente y sin conocer las conclusiones de las otras.
El detalle, con línea y evidencia, está en `diagnostico/cap1/`.

| # | Lente | Qué se encontró | Detalle |
|---|---|---|---|
| C1 | Corrección | **41 hallazgos: 13 errores**, 19 imprecisiones, 3 lagunas, 4 divergencias con FPP3, 2 sin comprobar. M1 y M3 limpios; las cifras del M6 se reproducen exactas | `par_academico.md` |
| C2 | Fuentes | **103 afirmaciones exigen fuente** (más las 5 del piloto): 26 de prioridad alta, 44 media, 33 baja. Para 74 ya hay un pasaje localizado. Faltan dos obras de las que cuelga casi todo lo demás: Cleveland et al. (1990), 16 afirmaciones; y la documentación de R y sus paquetes, 21 | `bibliografia/contraste/cap1_inventario.tsv` |
| C3 | Hilo | El capítulo tarda **~105 min y declara 88**. El M7 dura el doble de lo anunciado (10 → 18–20) y el M8 la mitad. El M3 promete cuatro gráficos y muestra uno; el de rezagos no aparece y el capítulo 2 dice «que vimos al final del Capítulo 1». «Ciclo» significa tres cosas | `lector_estudiante.md` |
| C4 | Gráficas | Los 22 gráficos mirados dibujados. Paneles que se salen de la página a 800 px, áreas de dibujo de 35 px de alto en las descomposiciones, fechas montadas en móvil, la fórmula de $F_S$ fuera de pantalla. Siete defectos se arreglan de una vez porque vienen de una misma regla | `graficas.md`, `capturas/` |
| C5 | Práctica | M1 y M2 no tienen ningún ejercicio. Nada practica subseries, rezagos, la desestacionalizada ni la lectura del residuo. Del quiz, 3 de 8 preguntas hay que rehacerlas; en las 5 de respuesta única la correcta es la opción más larga. De los 3 ejercicios, 1 hay que rehacerlo | `ejercicios.md` |

### Los errores, uno por uno (C1)

Los que comprobé yo mismo en R llevan ✔; los demás constan con su evidencia en el informe del par.

| Línea | Módulo | Qué dice | Qué es |
|---|---|---|---|
| 2920–2925 | M5 | El bloque R «media móvil 2×12» usa `slide_dbl(.before = 6, .after = 6)` | Es una media de 13 términos iguales: julio de 1955 da 284.00 y no 285.75 ✔ |
| 2930 | M5 | pandas `rolling(12, center=True)` como 2×12 | Tampoco lo es: 284.0 y 11 huecos en vez de 12 |
| 3030 | M6 | `stats::filter(y, rep(1/m, m))` | Con $m$ par no está centrado: 287.5 y 11 `NA` ✔. `decompose()` usa `c(0.5, rep(1, m-1), 0.5)/m` |
| 3280 | M6 | «aditiva sobre log = multiplicativa» | Falso en la descomposición clásica: 1.2347 frente a 1.2266 |
| 3411–3428 | M7 | Tabla de pesos tricúbicos | No es la convención de `stl()`: allí el vecino del borde pesa 0 |
| 3551 | M7 | El bucle interior corre «hasta que se estabilizan» | `stl()` hace un número fijo de pasadas: `inner = if (robust) 1 else 2` ✔ |
| 3587 | M7 | La versión robusta «expulsa exactamente una» observación | Solo en la primera pasada; el ajuste completo da peso 0 a varias (4 sobre la serie sin contaminar ✔) |
| 3664–3668 | M7 | Bloque Python de STL | No reproduce la figura: usa otros valores por defecto y `robust=True` |
| 2472 | M2 | `ts` «no puede» guardar varias series | `ts()` sobre una matriz crea un `mts` ✔ |
| 2760, 3208… | varios | «pasajeros» | `?AirPassengers`: «in thousands» ✔; los ejes del propio capítulo dicen «miles» |
| 3916–3945 | M9, ej. 1 | En `co2` «los datos no distinguen» aditiva de multiplicativa; la amplitud «no es proporcional al nivel» | El IC de $b$ es [0.575, 1.591] ✔: excluye el 0 y contiene el 1. Con el criterio de la propia solución rechaza la aditiva. La conclusión está invertida |
| 3864 | M9 | «Seis preguntas» | Son ocho ✔ |
| 6031 | quiz, P2 | Residuo «en embudo» | El M6 mide una U (3331–3333) |

Además: el quiz dice ciclos de «4 o 9 años» y el M4 «siete u ocho»; $F_T$ y $F_S$ se calculan con
`s.window = "periodic"` sin decirlo (con `feat_stl`, como FPP3, salen 0.997 y 0.964 en vez de 0.994
y 0.937); la serie desestacionalizada del M8 usa el índice clásico después de haber enseñado STL.

## 2. Restricciones verificadas antes de planear

- El capítulo 1 **se edita a mano** y no es base de ningún otro (la cadena de ensamblado empieza
  en el 2). Sus datos salen de `precalculo/genera_datos.R` → `DATOS_CAP1`; las soluciones, de
  `precalculo/genera_soluciones.R`.
- **El Corte I ya se evaluó** (Taller 1, preparcial y Parcial 1): corregir ahora no cambia nada
  que esté en evaluación. Los estudiantes sí siguen consultando el capítulo.
- **El verificador de bloques no corre en este equipo**: a R le falta `fpp3` y el Python se cuelga
  en `plt.show()`. Las tres soluciones se ejecutaron aparte y reproducen sus cifras.
- **La prosa tiene que estar quieta antes de contrastar**: F09 del auditor invalida una entrada
  si la frase cambia. Por eso las fuentes van después de las correcciones y de la estructura.
- Varios defectos de gráficas vienen de reglas de la **plantilla** (`.grafico-par`,
  `.simulador h4`): arreglarlas ahí obliga a reensamblar la guía del proyecto.
- Cambiar el número de ejercicios o de simuladores mueve las cifras de la portada y del README,
  que vigila `cuenta_sitio.py` (hoy ya en rojo: 68 simuladores escritos, 70 contados).
- La capa de fuentes del vault es de la sesión de Muestreo: aquí solo se entrega
  `bibliografia/uso_fuentes.json`.

## 3. Decisiones propuestas

Cada una lleva mi recomendación; las decide Javier.

- **D1 · Cinco rondas, en este orden:** R1 errores → R2 gráficas → R3 estructura → R4 fuentes →
  R5 práctica. Cada ronda termina con `verifica_todo.py`, revisión visual, commit y tu visto bueno.
- **D2 · Publicar R1 en cuanto esté**, sin esperar al resto: hoy hay código publicado que no
  calcula lo que dice. *Recomendado.*
- **D3 · Gráficas:** arreglar en el capítulo 1 **y en la plantilla**; llevar los arreglos a los
  capítulos 2–6 en la ronda de cada uno, no ahora. *Recomendado.*
- **D4 · M3:** añadir el gráfico de subseries y el de rezagos, que hoy se anuncian y no existen.
  La alternativa es retirar la promesa; pero el capítulo 2 se apoya en el de rezagos y el de
  subseries es la puerta a `s.window`. *Recomiendo añadirlos.*
- **D5 · No renumerar módulos.** Se mueve contenido entre el M5, el M7 y el M8 y se corrigen las
  duraciones declaradas; siguen siendo nueve.
- **D6 · Unidades:** «miles de pasajeros» en prosa, ejes y lecturas.
- **D7 · Fuentes:** contrastar las 26 de prioridad alta y las 44 de media. Las 33 de baja se
  resuelven al redactar: o se reescriben como propias, o se retiran, o suben a media.
- **D8 · Práctica:** rehacer el ejercicio 1 y las preguntas 2, 3 y 6; igualar la longitud de las
  opciones; y añadir cinco ejercicios cortos donde no hay ninguno (M2, M3, M6, M7, M8), sobre
  series distintas de `AirPassengers` (`UKgas`, `nottem`, `mdeaths`/`fdeaths`).
- **D9 · Quién hace qué:** una sola sesión escribe el capítulo en cada ronda. Verifican subagentes
  de contexto limpio que no redactaron. Las cifras las da R.

## 4. Tareas

| # | Ronda | Tarea | Tam. | Depende |
|---|---|---|---|---|
| T1.1 ✅ | R1 | M5 y M6: los tres bloques de media móvil calculan de verdad la 2×12; cifra de control 285.75 | S | — |
| T1.2 ✅ | R1 | M7: pesos tricúbicos con la convención de `stl()`, pasadas del bucle, «expulsa una», bloque Python que reproduzca la figura; resolver 19 frente a 21 en `trend(window)` ejecutando | M | — |
| T1.3 ✅ | R1 | M2 (`mts`), M6 (l. 3280), unidades (D6), «Seis preguntas», ciclos del quiz y del M4 | S | — |
| T1.4 ✅ | R1 | Ejercicio 1: conclusión coherente con sus intervalos; M8: declarar `periodic` y qué índice desestacionaliza | M | — |
| T1.5 ✅ | R1 | Las 19 imprecisiones y 3 lagunas del par, una por una (incluye «$m/2$» del piloto) | M | T1.1–T1.4 |
| T2.1 ✅ | R2 | Arreglos de una vez: `.grafico-par`, marcas de fecha, `panelComponente`, `.simulador h4`, contraste, títulos de eje | M | R1 |
| T2.2 ✅ | R2 | Específicos: fórmula $F_T$/$F_S$, gráfico estacional del M3, `loess-local`, mapa estacional a 375 px | M | T2.1 |
| T2.3 ✅ | R2 | Accesibilidad: `aria-label` que describa, `aria-live` en las lecturas | S | T2.1 |
| T3.1 | R3 | M3: gráficos de subseries y de rezagos, con sus datos desde R | M | R1 |
| T3.2 | R3 | M7: STL como secuencia de pasos; figura con la robustez y la flexibilidad a la vista; recibe el anticipo del M5 | L | R1 |
| T3.3 | R3 | M8: recibe la lectura en logaritmos y el contraste de fuerzas; gana código y una referencia para «muy fuertes» | M | T3.2 |
| T3.4 | R3 | M6: el resultado antes que los símbolos; la aditiva, dibujada | M | R1 |
| T3.5 | R3 | Vocabulario de «ciclo»; transiciones M1→M2 y M7→M8; resumen del M9; duraciones; tarjeta de la portada | S | T3.1–T3.4 |
| T4.1 | R4 | Biblioteca: Cleveland et al. (1990), R y sus paquetes, y lo que haga falta para ciclos económicos y oficinas de estadística | M | permiso de descarga |
| T4.2 | R4 | Contrastar alta y media (70), marcar, citar y registrar; lecturas del M9 con secciones exactas | L | R3, T4.1 |
| T5.1 | R5 | Rehacer el ejercicio 1; mejorar el 2 y el 3 | M | R3 |
| T5.2 | R5 | Quiz: rehacer P2, P3 y P6; longitudes; pistas que no regalen | M | R3 |
| T5.3 | R5 | Cinco ejercicios cortos de módulo (D8), con solución calculada en R | L | R3 |
| T5.4 | R5 | Que `verifica_bloques_cap6.py` corra sobre el capítulo 1 | S | instalar `fpp3` |

### Registro de rondas

- **R1 · errores — hecha y PUBLICADA el 2026-11-11** (`main` `b26787e` · gh-pages `4052a27`; con ella se publicó la Fase 0). De los 41 hallazgos del par: 34 corregidos, 5
  declarados y 2 que pasan a R4 por falta de fuente legible (el desarrollo de «Loess» y la 4.ª edición de
  Shumway y Stoffer). Un verificador independiente encontró siete problemas en lo corregido, y el redactor
  un error que el diagnóstico no había visto (la normalización del M6); todos resueltos. Detalle y
  evidencia: `diagnostico/cap1/R1_cambios.md`. Lo que R1 deja para otras rondas: alinear el simulador de
  Loess con la convención de pesos de `stl()` (R3), la cuarta limitación del método clásico (R3), y las
  preguntas 2, 3 y 6 del quiz y el ejercicio 1, que se corrigieron en lo falso pero siguen por rehacer (R5).

- **R2 · gráficas — hecha y PUBLICADA el 2026-11-11** (`main` `ad2840f` · gh-pages `9796360`). De los 63 problemas de las 14 fichas: 52 arreglados, 2 en parte,
  4 que ya había resuelto R1 y 5 sin tocar (exigen cambiar un cálculo o son de R3). Los 21 lienzos, el mapa
  y el ciclo se recapturaron a 1200, 800 y 375 px: sin desbordes ni fechas montadas; los paneles de las
  descomposiciones pasan de 35 a 130 px de alto. Seis reglas de CSS fueron también a la plantilla y la guía
  del proyecto se reensambló (solo CSS). Decisiones de diseño que tomó la ronda: la observada en verde
  oscuro en todo el capítulo, un morado para la desestacionalizada, `loess-local` en dos lienzos y una
  lectura nueva en el simulador del M5. Detalle: `diagnostico/cap1/R2_cambios.md`. Para R3: presentar el
  mapa estacional en la prosa, el eje que se reescala en `construye-tu-serie` y por qué el residuo de STL
  es más disperso en los extremos.

## 5. Criterios de aceptación

- [ ] Cada uno de los 13 errores tiene su comprobación en R en `diagnostico/cap1/comprobaciones/`
      y deja de reproducirse.
- [ ] Un segundo par académico, que no vio el primero, no encuentra errores nuevos en lo corregido.
- [ ] `audita_citas.py --cierre` en verde: nada pendiente en prioridad alta ni media.
- [ ] Los 22 gráficos vuelven a capturarse a 1200, 800 y 375 px sin desbordes ni fechas montadas.
- [ ] Cada objetivo de módulo tiene al menos una práctica dentro del capítulo.
- [ ] `verifica_todo.py` en verde, con `cuenta_sitio.py` incluido.
- [ ] La duración declarada de cada módulo dista menos de 3 min de la estimada.

## 6. Riesgos

- **Corregir un bloque de código cambia cifras** que la prosa cita más abajo: cada corrección de
  R1 termina buscando la cifra vieja en todo el capítulo.
- **El M7 puede crecer aún más** al ganar los pasos de STL: T3.2 tiene que quitar tanto como
  añade (lo que sale va al M8).
- **Cleveland et al. (1990) puede contradecir al capítulo** en algo más que el acrónimo: 16
  afirmaciones dependen de un artículo que nadie ha leído todavía.
- **Sesiones concurrentes:** `main` recibió hoy dos commits de otra sesión sobre el capítulo 5.
  No tocan estos archivos, pero la fusión se prueba antes de cada publicación.

## 7. Preguntas abiertas

1. ¿Apruebas D1–D9 tal como están?
2. ¿Permiso para descargar el PDF de Cleveland et al. (1990) desde scb.se (2,8 MB)?
3. ¿Instalo `fpp3` en R para que corra el verificador de bloques, o lo instalas tú?
4. Del Checkpoint 0 siguen abiertas: el pie de referencias en los seis capítulos, el año de
   Box et al. y la edición de Shumway y Stoffer.

## 8. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Fase 0: [[PLAN_Gestion_Documental]]
- Rondas anteriores del capítulo: [[PLAN_Graficos_Aditivo_Multiplicativo]] · [[PLAN_Formalizacion_Descomposicion]] · [[PLAN_Loess_STL]]
- Capítulo: [[20948-01 Componentes y descomposición]]
- Criterio: [[Criterio de contenido]] · [[Capa de fuentes]]
- Bitácora: [[2026-11-10]]
