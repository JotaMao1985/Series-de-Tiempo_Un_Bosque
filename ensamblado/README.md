# Scripts de ensamblado

Registro de **cómo** se construyó cada capítulo, no herramientas de uso diario.
Los capítulos publicados en `Htmls_Series/` son la fuente de verdad: a partir de
aquí se editan directamente.

| Script | Qué hizo |
|---|---|
| `ensambla_cap3.py` | Construyó el capítulo 3 **partiendo del capítulo 2** y sustituyendo regiones delimitadas (metadatos, CSS, plantillas de módulo, `courseData`, datos precalculados, JavaScript propio). |
| `retropropaga.py` | Injertó el componente `.derivacion` y la opción `barrasExtra` en los capítulos 1 y 2, y añadió una caja de derivación en cada uno. |
| `instala_ciclo.py` | Instaló el componente `.ciclo` en la plantilla y en los capítulos 1, 2 y 3, con una instancia en cada uno. El capítulo 4 **no** aparece: se ensambla desde el 3 y lo hereda por construcción. |
| `ensambla_cap5.py` | Construyó el capítulo 5 **partiendo del capítulo 4**, y además **instaló el componente nuevo `.mapa-estacional`** en la región compartida (CSS, JavaScript y la llamada de `loadModule`). Expande dos marcadores de plantilla —`<!--MAPA:...-->` y `<!--CICLO:...-->`— con sus constructores de `componentes/`, para que el marcado sea idéntico al de las otras instancias. Es **reejecutable** y reproduce el archivo byte a byte. |
| `retropropaga_mapa.py` | Injertó `.mapa-estacional` en el capítulo 1 (módulo de visualización estacional) y en la plantilla, con una instancia en cada uno. Aborta si el archivo ya lo tiene. Los capítulos 2, 3 y 4 **no** aparecen: ninguno trata la estacionalidad. |
| `ensambla_cap6.py` | Construyó el capítulo 6 **partiendo del capítulo 5**, e **instaló el componente nuevo `.tabla-ranking`**. Expande los marcadores `<!--RANKING:...-->` y `<!--CICLO:...-->` con sus constructores de `componentes/`. Es **reejecutable** y reproduce el archivo byte a byte: tras `retropropaga_ranking.py` detecta que el capítulo 5 ya trae el componente y se salta la instalación. Comprueba además el andamiaje de los **dos** `.quiz` (el del cierre y el del taller de auditoría). |
| `retropropaga_ranking.py` | Injertó `.tabla-ranking` en los capítulos 3, 4 y 5 y en la plantilla, con una instancia en cada uno, y **corrigió en los seis capítulos y en la plantilla** el bug por el que una pregunta de selección múltiple acertada mostraba la palabra «undefined». Los capítulos 1 y 2 solo reciben la corrección del quiz: no tienen ninguna tabla comparativa de modelos que ordenar. |
| `ensambla_cap4.py` | Construyó el capítulo 4 **partiendo del capítulo 3**. Fuentes en `cap4/` (las plantillas de los 10 módulos y el JavaScript propio) y comprobaciones ampliadas: los 10 simuladores registrados **y** sus contenedores, el andamiaje del `.quiz`, las 4 etapas del ciclo, los 3 ejercicios con sus 6 desplegables, y que no quede nada del capítulo 3. |

## Carpetas auxiliares

- `componentes/` — fuentes compartidas de los componentes que viven en más de un
  archivo: `.ciclo` (`ciclo.css`, `ciclo.js`, `ciclo_html.py`), `.mapa-estacional`
  (`mapa_estacional.css`, `.js`, `_html.py`) y `.tabla-ranking`
  (`tabla_ranking.css`, `.js`, `_html.py`). Los archivos del proyecto se generan
  desde aquí, de modo que su marcado es idéntico y la comparación de selectores CSS
  no encuentra diferencias. **Si se corrige un componente, se corrige aquí**: las
  correcciones de espaciado del capítulo 5 se hicieron en estas fuentes y el
  reensamblado las reprodujo sin tocar el HTML publicado.
- `cap4/`, `cap5/` — plantillas de módulo y JavaScript de cada capítulo. **Son la
  fuente** para su `ensambla_capN.py`: si se edita el capítulo publicado a mano, hay
  que reflejarlo aquí o el siguiente ensamblado lo perderá.

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
explícita: si el archivo ya tiene `.ciclo`, para). `ensambla_cap4.py` **sí** es
reejecutable, porque su fuente es el capítulo 3 y sus propias plantillas en
`cap4/`; se ha vuelto a correr varias veces durante la auditoría.

`ensambla_cap6.py` **sí** es reejecutable, y su sección 2 está escrita para
tolerar que el capítulo del que parte ya traiga el componente: es lo que permite
que siga reproduciendo el archivo byte a byte después de la retropropagación.
Ese es el patrón a copiar si algún día hay un capítulo 7.

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
