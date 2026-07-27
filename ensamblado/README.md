# Scripts de ensamblado

Registro de **cómo** se construyó cada capítulo, no herramientas de uso diario.
Los capítulos publicados en `Htmls_Series/` son la fuente de verdad: a partir de
aquí se editan directamente.

| Script | Qué hizo |
|---|---|
| `ensambla_cap3.py` | Construyó el capítulo 3 **partiendo del capítulo 2** y sustituyendo regiones delimitadas (metadatos, CSS, plantillas de módulo, `courseData`, datos precalculados, JavaScript propio). |
| `retropropaga.py` | Injertó el componente `.derivacion` y la opción `barrasExtra` en los capítulos 1 y 2, y añadió una caja de derivación en cada uno. |
| `instala_ciclo.py` | Instaló el componente `.ciclo` en la plantilla y en los capítulos 1, 2 y 3, con una instancia en cada uno. El capítulo 4 **no** aparece: se ensambla desde el 3 y lo hereda por construcción. |
| `ensambla_cap4.py` | Construyó el capítulo 4 **partiendo del capítulo 3**. Fuentes en `cap4/` (las plantillas de los 10 módulos y el JavaScript propio) y comprobaciones ampliadas: los 10 simuladores registrados **y** sus contenedores, el andamiaje del `.quiz`, las 4 etapas del ciclo, los 3 ejercicios con sus 6 desplegables, y que no quede nada del capítulo 3. |

## Carpetas auxiliares

- `componentes/` — fuentes compartidas de `.ciclo` (`ciclo.css`, `ciclo.js` y el
  constructor `ciclo_html.py`). Los cinco archivos del proyecto se generan desde
  aquí, de modo que su marcado es idéntico y la comparación de selectores CSS no
  encuentra diferencias.
- `cap4/` — plantillas de módulo y JavaScript del capítulo 4. **Son la fuente**
  para `ensambla_cap4.py`: si se edita el capítulo publicado a mano, hay que
  reflejarlo aquí o el siguiente ensamblado lo perderá.

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

Para el capítulo 5, copia el patrón de `ensambla_cap4.py` y actualiza los
marcadores contra el capítulo 4.

## Dos aserciones que se aprendieron por las malas

1. **Delimitar una región por dos marcadores únicos no siempre funciona.** Cierres
   como `    };` o `  </script>` se repiten por todo el archivo. La regla que
   funciona es: el marcador de **inicio** tiene que ser único —es el que
   identifica la región—, y el de fin se busca a partir de él.
2. **Contar una cadena no es contar marcado.** La aserción de las cajas de
   derivación contaba `<div class="derivacion">` y encontraba una de más: el
   JavaScript heredado documenta el componente con un ejemplo dentro de un
   comentario. Ahora la expresión exige el contenedor **y** su botón.
