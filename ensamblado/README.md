# Scripts de ensamblado

Registro de **cómo** se construyó cada capítulo, no herramientas de uso diario.
Los capítulos publicados en `Htmls_Series/` son la fuente de verdad: a partir de
aquí se editan directamente.

| Script | Qué hizo |
|---|---|
| `ensambla_cap3.py` | Construyó el capítulo 3 **partiendo del capítulo 2** y sustituyendo regiones delimitadas (metadatos, CSS, plantillas de módulo, `courseData`, datos precalculados, JavaScript propio). |
| `retropropaga.py` | Injertó el componente `.derivacion` y la opción `barrasExtra` en los capítulos 1 y 2, y añadió una caja de derivación en cada uno. |

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

`ensambla_cap3.py` está escrito contra el capítulo 2 **anterior** a la
retropropagación de `.derivacion`. Volver a ejecutarlo hoy abortaría (los
marcadores del CSS han cambiado), que es exactamente lo que debe hacer. Para el
capítulo 4, copia el patrón y actualiza los marcadores contra el capítulo 3.
