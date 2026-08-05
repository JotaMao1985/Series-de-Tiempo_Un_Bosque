# Scripts de ensamblado

Registro de **cómo** se construyó cada capítulo, no herramientas de uso diario.
Los capítulos publicados en `Htmls_Series/` son la fuente de verdad: a partir de
aquí se editan directamente.

| Script | Qué hizo |
|---|---|
| `ensambla_cap3.py` | Construyó el capítulo 3 **partiendo del capítulo 2** y sustituyendo regiones delimitadas (metadatos, CSS, plantillas de módulo, `courseData`, datos precalculados, JavaScript propio). |
| `retropropaga.py` | Injertó el componente `.derivacion` y la opción `barrasExtra` en los capítulos 1 y 2, y añadió una caja de derivación en cada uno. |
| `instala_ciclo.py` | Instaló el componente `.ciclo` en la plantilla y en los capítulos 1, 2 y 3, con una instancia en cada uno. El capítulo 4 **no** aparece: se ensambla desde el 3 y lo hereda por construcción. |
| `ensambla_cap5.py` | Construyó el capítulo 5 **partiendo del capítulo 4**, y además **instaló el componente nuevo `.mapa-estacional`** en la región compartida (CSS, JavaScript y la llamada de `loadModule`). Expande tres marcadores de plantilla —`<!--MAPA:...-->`, `<!--RANKING:...-->` y `<!--CICLO:...-->`— con sus constructores de `componentes/`, para que el marcado sea idéntico al de las otras instancias. Es **reejecutable** y reproduce el archivo byte a byte (ver Advertencia: dejó de serlo con `retropropaga_ranking.py` y se reparó el 2026-08-05). |
| `retropropaga_mapa.py` | Injertó `.mapa-estacional` en el capítulo 1 (módulo de visualización estacional) y en la plantilla, con una instancia en cada uno. Aborta si el archivo ya lo tiene. Los capítulos 2, 3 y 4 **no** aparecen: ninguno trata la estacionalidad. |
| `ensambla_cap6.py` | Construyó el capítulo 6 **partiendo del capítulo 5**, e **instaló el componente nuevo `.tabla-ranking`**. Expande los marcadores `<!--RANKING:...-->` y `<!--CICLO:...-->` con sus constructores de `componentes/`. Es **reejecutable** y reproduce el archivo byte a byte: tras `retropropaga_ranking.py` detecta que el capítulo 5 ya trae el componente y se salta la instalación. Comprueba además el andamiaje de los **dos** `.quiz` (el del cierre y el del taller de auditoría). |
| `retropropaga_ranking.py` | Injertó `.tabla-ranking` en los capítulos 3, 4 y 5 y en la plantilla, con una instancia en cada uno, y **corrigió en los seis capítulos y en la plantilla** el bug por el que una pregunta de selección múltiple acertada mostraba la palabra «undefined». Los capítulos 1 y 2 solo reciben la corrección del quiz: no tienen ninguna tabla comparativa de modelos que ordenar. |
| `ensambla_cap4.py` | Construyó el capítulo 4 **partiendo del capítulo 3**. Fuentes en `cap4/` (las plantillas de los 10 módulos y el JavaScript propio) y comprobaciones ampliadas: los 10 simuladores registrados **y** sus contenedores, el andamiaje del `.quiz`, las 4 etapas del ciclo, los 3 ejercicios con sus 6 desplegables, la tabla de ranking `rejilla-nilo`, y que no quede nada del capítulo 3. Expande el marcador `<!--RANKING:...-->` con su constructor de `componentes/`. Es **reejecutable** y reproduce el archivo byte a byte (ver Advertencia: dejó de serlo con `retropropaga_ranking.py` y se reparó el 2026-08-05). |
| `retropropaga_retro_multiple.py` | Corrigió en los **6 capítulos y en la plantilla** la retroalimentación de las preguntas de selección múltiple: `renderAutoevaluacion()` solo usaba el `retro` de las opciones **correctas**, así que quien fallaba una `multiple` nunca sabía en qué opción concreta se equivocó. Añade el ayudante `desgloseMultiple()`, su llamada en la rama de segundo fallo y las reglas CSS `.quiz-retro ul` (con `color: inherit`, o la regla global `ul li` deja el desglose gris sobre fondo rojo). Desbloqueó **15 explicaciones ya escritas** en los capítulos 5 y 6 que el estudiante nunca había visto. Origen: auditoría de la Fase 0 del material de Diseño de Experimentos. |

## Carpetas auxiliares

- `componentes/` — fuentes compartidas de los componentes que viven en más de un
  archivo: `.ciclo` (`ciclo.css`, `ciclo.js`, `ciclo_html.py`), `.mapa-estacional`
  (`mapa_estacional.css`, `.js`, `_html.py`) y `.tabla-ranking`
  (`tabla_ranking.css`, `.js`, `_html.py`). Los archivos del proyecto se generan
  desde aquí, de modo que su marcado es idéntico y la comparación de selectores CSS
  no encuentra diferencias. **Si se corrige un componente, se corrige aquí**: las
  correcciones de espaciado del capítulo 5 se hicieron en estas fuentes y el
  reensamblado las reprodujo sin tocar el HTML publicado.
- `cap4/`, `cap5/`, `cap6/` — plantillas de módulo y JavaScript de cada capítulo.
  **Son la fuente** para su `ensambla_capN.py`: si se edita el capítulo publicado a
  mano —o si una retropropagación le injerta algo—, hay que reflejarlo aquí o el
  siguiente ensamblado lo perderá. Es exactamente lo que pasó con `.tabla-ranking`
  (ver Advertencia).

## Por qué por sustitución y no por concatenación

Al montar el capítulo 2 se leyó un bloque de CSS en una variable y **nunca se
concatenó**: el capítulo se publicó sin las 22 reglas base del componente
`.quiz` y sin `.simulador-lectura`, y las pruebas de comportamiento seguían
pasando igual. Partir de un capítulo que ya funciona y sustituir regiones
concretas hace que ese fallo sea imposible por construcción: lo que no se toca,
se conserva.

Las dos reglas que hacen que esto funcione:

1. **Toda sustitución exige que su marcador aparezca exactamente una vez.** Si
   aparece 0 o 2 veces, el script aborta en vez de producir un archivo a medias.
2. **Al final se comprueba que el resultado contiene todo lo que debe contener**
   (las 10 plantillas, los simuladores registrados *y* sus contenedores, el
   andamiaje interno del `.quiz`, las reglas CSS heredadas) y **nada de lo que
   no debe** (`DATOS_CAP2`, `SERIES_CAP2`, referencias al capítulo anterior).

La comprobación del andamiaje del `.quiz` está ahí porque la auditoría de esta
sesión encontró justo ese fallo: `renderAutoevaluacion()` lanza excepción si al
contenedor `.quiz` le falta `.quiz-preguntas`.

## Advertencia

`ensambla_cap3.py` e `instala_ciclo.py` están escritos contra el estado de los
archivos **anterior** a su propia ejecución. Volver a ejecutarlos hoy abortaría,
que es exactamente lo que deben hacer (`instala_ciclo.py` lo comprueba de forma
explícita: si el archivo ya tiene `.ciclo`, para). `ensambla_cap3.py` además
apunta a una ruta temporal de la sesión en que se escribió, que ya no existe:
hoy falla al abrir `derivacion.css` antes de tocar nada.

> ⚠️ **`retropropaga_ranking.py` rompió los ensamblados del 4 y del 5.**
> Corregido el 2026-08-05; se deja escrito porque son dos formas distintas de
> quedarse por detrás de una retropropagación, y la segunda no da la cara.
>
> Al injertar `.tabla-ranking` en los capítulos 3, 4 y 5, sus dos ensamblados
> quedaron desfasados respecto al HTML publicado:
>
> - **`ensambla_cap4.py` era destructivo.** El capítulo 4 recibió una instancia
>   (`TABLAS_RANKING['rejilla-nilo']` y su marcado) que no estaba en `cap4/` ni
>   en el script. Al reejecutarlo, el ensamblado reconstruía el capítulo desde el
>   3 y **borraba la tabla en silencio**: escribía sin avisar, porque sus
>   comprobaciones finales no la buscaban. Ocurrió de verdad el 2026-07-30 y de
>   nuevo el 2026-08-05, restaurando desde un respaldo las dos veces.
> - **`ensambla_cap5.py` abortaba sin escribir nada**, que es el fallo benigno:
>   su ancla del CSS del mapa encadenaba desde la última regla del ciclo hasta
>   `  </style>`, y el CSS de `.tabla-ranking` se insertó justo entre esos dos
>   extremos, así que la cadena completa dejó de existir. **Debajo escondía el
>   mismo fallo destructivo que el 4**: al arreglar el ancla, el script perdía la
>   instancia `comparativa`. Un `ABORTA` puede estar tapando algo peor.
>
> La reparación, en las dos, fue la misma y es la que toca repetir la próxima vez:
> **reflejar el componente en las fuentes de `capN/`** —marcador
> `<!--RANKING:...-->` en la plantilla y el registro en `chapter.js`— y **añadir
> una aserción final que lo exija**, siguiendo el patrón de `ensambla_cap6.py`.
> El CSS y los ayudantes compartidos no hacían falta: se heredan del capítulo
> anterior y sobreviven por construcción. Lo que se pierde es siempre lo que vive
> en una región que el script sustituye.
>
> Un tercer detalle del capítulo 5, del mismo origen: la llamada
> `iniciarMapasEstacionales()` se anclaba a `iniciarCiclos();`, y como el 4 ya
> traía `iniciarTablasRanking()` justo detrás, el mapa se colaba por delante y
> cambiaba el orden. Ahora se ancla al **final** del bloque de inicializadores.
>
> Regla general que esto confirma: **haz una copia del capítulo antes de
> reejecutar su ensamblado y compara byte a byte**. Si difiere, el script está
> por detrás de alguna retropropagación.

`ensambla_cap6.py` nunca dejó de ser reejecutable, y su sección 2 está escrita
para tolerar que el capítulo del que parte ya traiga el componente: es lo que
permite que siga reproduciendo el archivo byte a byte después de la
retropropagación. Ese es el patrón a copiar si algún día hay un capítulo 7.

Hoy los **tres** (`ensambla_cap4.py`, `ensambla_cap5.py`, `ensambla_cap6.py`) son
reejecutables y reproducen su capítulo byte a byte, encadenados 4 → 5 → 6.

## Dos aserciones que se aprendieron por las malas

1. **Delimitar una región por dos marcadores únicos no siempre funciona.** Cierres
   como `    };` o `  </script>` se repiten por todo el archivo. La regla que
   funciona es: el marcador de **inicio** tiene que ser único —es el que
   identifica la región—, y el de fin se busca a partir de él.
2. **Una clase inventada no da error: da un componente sin estilo.** El capítulo 6
   se escribió con un `<div class="quiz-pie">` que no existe en ninguna hoja de
   estilos. El JavaScript encontraba sus elementos y todo funcionaba, pero el pie
   de las dos autoevaluaciones se veía crudo, con 0 px de separación. Es el mismo
   fallo que el bloque de CSS ausente del capítulo 2, y se detecta igual: midiendo
   la geometría real y comparando el conjunto de selectores. Al copiar marcado de
   otro capítulo, cópialo **entero**, no de memoria.
3. **Contar una cadena no es contar marcado.** La aserción de las cajas de
   derivación contaba `<div class="derivacion">` y encontraba una de más: el
   JavaScript heredado documenta el componente con un ejemplo dentro de un
   comentario. Ahora la expresión exige el contenedor **y** su botón.

## Cómo se comprueba que el ensamblado no pierde nada

Tras corregir el capítulo 5 a mano durante la auditoría, la comprobación que cierra
el círculo es **volver a ejecutar el script y comparar el resultado con el archivo
anterior byte a byte**. Si sale idéntico, todas las correcciones viven en sus fuentes
(`cap5/`, `componentes/`, el capítulo anterior) y no solo en el HTML publicado:

```bash
cp Htmls_Series/capitulo-5-sarima.html /tmp/antes.html
python3 ensamblado/ensambla_cap5.py
diff /tmp/antes.html Htmls_Series/capitulo-5-sarima.html && echo "sin pérdidas"
```

Los tres ensamblados se encadenan (el 5 parte del 4 y el 6 del 5), así que la
comprobación completa es correrlos en orden y comparar los tres. Con el respaldo
hecho **antes** de tocar nada, porque el fallo que busca esta prueba es
precisamente que un script escriba de menos:

```bash
mkdir -p /tmp/antes && cp Htmls_Series/capitulo-[456]-*.html /tmp/antes/
for n in 4 5 6; do python3 ensamblado/ensambla_cap$n.py || break; done
for f in Htmls_Series/capitulo-[456]-*.html; do diff -q "/tmp/antes/$(basename $f)" "$f"; done && echo "sin pérdidas"
```

Y la prueba que cierra el círculo de verdad: **rompe la fuente a propósito y
comprueba que el script aborta**. Una aserción que nunca ha fallado no está
demostrada. Renombrar la clave de `TABLAS_RANKING` en `capN/chapter.js`, o el
marcador `<!--RANKING:...-->` en su plantilla, tiene que dar `ABORTA` y dejar el
capítulo intacto; si lo escribe igual, la aserción no sirve.
