# Bibliografía del curso · ninguna cita de memoria

El material tiene una norma para las cifras —ninguna se escribe a mano, todas salen de R— y
desde el 2026-11-10 tiene la misma para las fuentes: **ninguna cita se escribe de memoria**.
Toda afirmación que el capítulo atribuye a una obra apunta a un pasaje que alguien leyó, y un
guion lo comprueba.

## Dónde vive cada dato

| Dato | Vive en | Lo escribe |
|---|---|---|
| Metadatos de la obra y su PDF | Zotero, colección `Docencia › 20948 Series de Tiempo` | los traductores de Zotero, desde un DOI o un ISBN |
| Instantánea de la biblioteca | `referencias.json` (CSL-JSON), `claves.json`, `zotero.lock.json` | `precalculo/exporta_zotero.py` |
| Lo que Zotero no trajo | `enmiendas.yml`, cada una con su evidencia | a mano, con URL y fecha |
| Cómo se encontró cada identificador | `obras.tsv` | la búsqueda en Crossref y Open Library del 2026-11-10 |
| Ejemplar leído (huella, portada) | `ejemplares.yml` | `precalculo/extrae_fuente.py` + una mirada a la portada |
| Páginas web leídas (URL, fecha, huella) | `instantaneas.yml` | `precalculo/extrae_fuente.py --web` |
| Afirmación ↔ pasaje leído | `contraste/capN.yml` | quien dirige la ronda, con lo que devuelve el verificador |
| Contrato curso → vault | `uso_fuentes.json`: lo único que el vault lee de este curso | `precalculo/audita_citas.py --uso` |
| PDF y texto por página | `_local/` — **fuera de git**: el repo es público | `precalculo/extrae_fuente.py` |
| Estilo de cita | `apa-es.csl` (APA 7; variante con «y» en lugar de «&») | derivado del `apa.csl` de Zotero |

Zotero es la puerta de entrada. El repo guarda lo que el auditor necesita para no depender de
que Zotero esté abierto. El vault de Obsidian (`Vault/Fuentes/`) es navegación y notas de
lectura, nunca dato primario.

## Dar de alta una obra

1. Buscar su DOI o ISBN **en la red** (Crossref, la editorial, Open Library), no de memoria, y
   anotarlo en `obras.tsv` con la URL que lo demuestra.
2. En Zotero, seleccionar la subcolección (`1 Básica`, `2 Complementaria`, `3 Fuentes primarias`,
   `4 Datos y software`) y usar **Añadir por identificador**. Los ISBN se envían aparte de los DOI.
3. `python3 precalculo/exporta_zotero.py` (Zotero abierto, con la API local activada en
   Ajustes → Avanzado).
4. Si falta un campo que la editorial sí publica (Crossref no registra el número de edición de
   los libros de Springer), añadirlo a `enmiendas.yml` con su evidencia. Mejor aún: corregirlo en
   Zotero y borrar la enmienda.
5. Si hay PDF: adjuntarlo en Zotero, o dejarlo (puede ser un enlace simbólico) en
   `_local/pdf/<clave>.pdf`; correr `python3 precalculo/extrae_fuente.py` y llenar en
   `ejemplares.yml` lo que diga la portada (`edicion_comprobada`).

Una obra sin DOI ni ISBN (Cleveland et al., 1990; la edición de 1970 de Box y Jenkins) se da de
alta a mano en Zotero copiando la portada, y se anota `origen: portada`.

## Contrastar una afirmación

1. Quien redacta marca la afirmación en el HTML con `data-afirma="c1-m7-03"` (capítulo, módulo,
   número) y, si va a llevar cita visible, deja dentro
   `<cite class="cita" data-ref="clave" data-loc="§3.6"></cite>`.
2. Un verificador **que no es quien redactó** recibe la afirmación y el texto de la fuente —no el
   veredicto esperado— y devuelve el veredicto y una cita literal de 25 palabras como mucho.
3. La entrada se escribe en `contraste/capN.yml`. La huella de la prosa sale de
   `python3 precalculo/audita_citas.py --huella c1-m7-03`.
4. `python3 precalculo/genera_referencias.py` escribe el texto de las citas y las listas.
5. `python3 precalculo/audita_citas.py` tiene que salir en verde.

Los localizadores usan el vocabulario cerrado de la norma común de los cuatro cursos
(`Vault/Estandar/Capa de fuentes.md`): `§3.4` · `cap. 3` · `p. 15` · `pp. 15–17` · `tabla 3.1` ·
`fig. 3.1` · `ec. 3.3` · `ejemplo 3.2` · `ejercicio 3.12` · `problema 2.28` · `ap. A`; varios se
separan con «; ». Una página de ayuda de R no tiene secciones numeradas: su localizador es el
nombre de la sección (`§Description` · `§Usage` · `§Arguments` · `§Format` · `§Details` · `§Value` ·
`§Source` · `§References`), una extensión local de ese vocabulario que el auditor acota igual que
una sección de FPP3 (ronda R4 del capítulo 1). Las citas de segunda mano (`data-via`) de esa norma aún no están implementadas
aquí: no se ha necesitado ninguna.

Veredictos: `respaldada` · `con-matiz` (la fuente apoya la idea pero difiere en un detalle; la
`nota` dice cuál) · `discrepa` (solo lo cierra Javier) · `propia` (se deduce en el material o sale
de R) · `pendiente` (con `motivo`) · `por-reverificar` (la prosa cambió). Solo las dos primeras
admiten cita visible. Un capítulo con algo pendiente no cierra su auditoría
(`audita_citas.py --cierre`).

Clases de evidencia: `PDF` (página del ejemplar), `WEB` (instantánea de una página, acotada a la
sección del localizador) y `DOC` (documentación de R) las comprueba el auditor contra `_local/`.
`MAN` (un libro en papel, con página) y `REPO` (una derivación o una cifra del propio repo) no
las ejecuta ningún guion y se cuentan aparte.

## Los guiones

| Guion | Qué hace |
|---|---|
| `precalculo/exporta_zotero.py` | Zotero → `referencias.json`. `--comprobar` no escribe |
| `precalculo/extrae_fuente.py` | PDF y páginas web → texto en `_local/`, y su huella |
| `precalculo/genera_referencias.py` | escribe las citas, las listas de fuentes y el pie |
| `precalculo/audita_citas.py` | F01–F12: la cita literal está en la fuente, la edición es la leída, quien verifica no redactó, la prosa no cambió… |
| `precalculo/prueba_audita_citas.py` | inyecta 24 defectos y exige que cada uno salte con su código exacto |
| `precalculo/verifica_todo.py` | todos los verificadores del sitio, de una vez |

## Lo que falta (2026-11-10)

- **Cleveland et al. (1990)**, la fuente original de STL: sin DOI; su PDF está en el archivo del
  *Journal of Official Statistics* y descargarlo espera el permiso de Javier. FPP3 da su rango
  de páginas como 3–33 y OpenAlex como 3–73: se decide leyendo.
- **Guerrero (2003)**: Zotero no encuentra su ISBN. Hay que transcribir la portada.
- **Box y Jenkins (1970)**: la edición original no tiene ISBN. En la biblioteca está la revisada
  de 1976.
- **R y sus paquetes** como obras (`4 Datos y software`), para poder contrastar contra `?stl`.
- **Libros que no están en disco**: Box et al. (5.ª ed.), Brockwell y Davis (3.ª ed.), Shumway y
  Stoffer (4.ª ed.). El PDF de Shumway y Stoffer que hay es de la 3.ª y está incompleto.
- **Box et al., 5.ª ed.**: el catálogo de la Library of Congress la fecha en 2016 y el syllabus
  en 2015 (Wiley la publicó en junio de 2015 con copyright 2016). Decide Javier.
- La caché `_local/` es de cada copia de trabajo: tras fusionar a `main` hay que volver a correr
  `extrae_fuente.py` allí.
