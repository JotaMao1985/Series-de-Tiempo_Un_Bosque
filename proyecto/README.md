# Guía del proyecto de pronóstico (Corte III)

Fuente de `Htmls_Series/proyecto-pronostico-corte-iii.html` y de la plantilla descargable
`Htmls_Series/proyecto-pronostico-plantilla.Rmd`. Las decisiones (D1–D14, P1–P3) están en
`PLAN_Proyecto_Pronostico.md`. Está calcada del proyecto aplicado de Diseño de Experimentos
(`../Diseno de experimentos/proyecto/`), que es el modelo.

| Archivo | Qué es |
|---|---|
| `datos.py` | **La única fuente de cifras**: calendario (semana 10 = del 5 al 10 de octubre), festivos, hitos, hora y canal de entrega, descuento, longitudes mínimas de la serie, pesos, rúbrica con sus descriptores y la exigencia del 6.12 de cada criterio, tope y las reglas de la conjunta |
| `modulos/m1…m10-*.html` | La prosa de los diez módulos, con marcadores `@@CLAVE@@` que el ensamblador resuelve desde `datos.py`. El código R va crudo: el ensamblador lo escapa |
| `plantilla-informe.Rmd` | La plantilla del informe que se descarga desde la guía (se copia tal cual al sitio) |
| `audita_proyecto.py` | El auditor, sobre el artefacto: ocho frentes (A calendario, B pesos, C decisiones, D estructura, E código R y plantilla, F contenido, G el módulo 6.12, H la conjunta) |
| `prueba_audita_proyecto.py` | El arnés: inyecta 52 defectos y exige que cada uno lo cace su frente; cinco van en la plantilla, que se le pasa al auditor por `PROYECTO_RMD` |
| `RESISTENCIA_IA.md` | La medición del 2026-10-21: una entrega fabricada con IA, calificada en frío |
| `../precalculo/ensambla_proyecto.py` | El ensamblador, calcado del de Diseño; acepta `--revisar` |

## Construir y comprobar

```bash
python3 precalculo/ensambla_proyecto.py --revisar && python3 precalculo/ensambla_proyecto.py
python3 proyecto/audita_proyecto.py && python3 proyecto/prueba_audita_proyecto.py
```

Desde la carpeta `Series de tiempo/`. El auditor y su arnés leen la guía de `Htmls_Series/`: sin
construirla antes, fallan. El frente E necesita R con `forecast` y `rmarkdown`, y renderiza la plantilla
dos veces (sin serie y con una), una de ellas con R en el idioma C.

## Publicar un cambio

**Publicada el 2026-10-21**, con el visto bueno de Javier y con la cláusula de volver a descargar la serie
que él pidió tras la prueba de resistencia. Fuera de la guía, la publicación tocó el enlace del 6.12
(`ensamblado/cap6/templates_10_12.html`, y el cap. 6 reensamblado), la tarjeta de la portada, la sección del
README del sitio y la fila de `precalculo/cuenta_sitio.py`. Para publicar un cambio:

1. Construir y comprobar, como arriba, y `python3 precalculo/cuenta_sitio.py`.
2. `git status --short`: commitear **por ruta**. Otras sesiones trabajan en el mismo árbol, y un `git add -A`
   se llevaría lo suyo (memoria `sesiones-concurrentes-mismo-arbol`).
3. Push a `main` y `git subtree push --prefix Htmls_Series origin gh-pages` (memoria
   `series-tiempo-despliegue-gh-pages`); comprobar la página en el sitio publicado.

## Cambiar una fecha, el peso o una regla

Se toca **una línea** de `datos.py`, se reensambla y se vuelve a auditar. El auditor recalcula el día de la
semana, la semana del curso, los festivos, las sumas de la rúbrica, la tabla del tope y la de longitudes
mínimas, así que una fecha en otro día o un peso que no cuadra lo para.

## Lo que no se deduce del código

- **La numeración de las semanas es la de Series, no la de Diseño.** Diseño llama semana 9 al receso del 5
  al 10 de octubre; Series y Espacial la llaman 10. Con la de Series, la 16 va del 16 al 21 de noviembre
  (P1, Javier, 2026-10-21).
- **El informe cierra un domingo** porque el lunes 16 de noviembre es festivo. El auditor lleva su propia
  lista de festivos y no la importa de `datos.py`.
- **Los bloques de R de la guía se corren encadenados**: el segundo usa `y`, `h` y `T0` del primero, como en
  el informe. El frente E escribe una serie mensual de prueba en `datos/serie.csv` de un directorio temporal.
- **La plantilla no escribe nada en `datos/`.** Sin serie, usa una simulada en memoria y lo avisa en el
  resumen. El aviso lleva `&iacute;` y no `í` porque con R en el idioma C el carácter sale como `<U+00ED>`;
  la fecha arma el mes a mano por la misma razón.
- **Las anclas `#modulo-N` sí valen aquí**: los capítulos de Series leen el hash (`moduloDelHash`). El
  auditor exige que el módulo exista y que el texto del enlace nombre ese módulo.
- **Las reglas de la conjunta viven solo en el módulo 8.** La guía de Espacial, en su repositorio, las
  enlaza (D12). Si Espacial cambia una regla, el cambio se hace aquí.
