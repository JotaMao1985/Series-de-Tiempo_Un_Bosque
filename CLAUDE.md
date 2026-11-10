# Series de Tiempo (20948) · reglas para quien trabaje en este repo

Material HTML interactivo de un curso universitario, publicado en GitHub Pages desde
`Htmls_Series/`. Lo leen estudiantes: un error publicado es un error enseñado.

## Las dos normas duras

1. **Ninguna cifra a mano.** Toda cifra en pantalla sale de R (`precalculo/genera_*.R`) y se
   verifica antes de escribirla.
2. **Ninguna cita de memoria.** No escribas un autor, un año, una página, una sección ni un DOI
   que no hayas leído en esta sesión en la fuente o en `bibliografia/`. Una obra entra por
   Zotero con su DOI o ISBN; una afirmación atribuida lleva `data-afirma`, una entrada en
   `bibliografia/contraste/capN.yml` con la cita literal del pasaje leído, y la verifica alguien
   que no la redactó. Lo que no se pueda contrastar se declara `propia` o `pendiente`: nunca se
   rellena. El procedimiento completo está en `bibliografia/README.md`.

## Antes de dar algo por hecho

- `python3 precalculo/verifica_todo.py` (segundos; `--lento`, `--red` y `--zotero` amplían).
- Lo visual se comprueba por HTTP con los servidores de `.claude/launch.json`, no por `file://`.

## Lo que rompe cosas

- Los capítulos 3 a 6 **se ensamblan** desde `ensamblado/capN/`. Editar el HTML final sin
  reflejarlo en la fuente lo borra al reensamblar. Los capítulos 1 y 2 se editan a mano, y el 2
  es la base del 3: tras tocarlo, correr `ensamblado/ensambla_cap3.py`.
- `plantilla/plantilla-capitulo.html` es la base de la guía del proyecto: si cambia su CSS, hay
  que correr `precalculo/ensambla_proyecto.py` o `proyecto/audita_proyecto.py` falla.
- Una clase nueva de Tailwind exige `python3 precalculo/compila_tailwind.py`.
- Los PDF de los libros y su texto extraído nunca van a git (`bibliografia/_local/`): el repo es
  público.

## Publicar

`git push` y el despliegue a `gh-pages` publican para los estudiantes: se consultan siempre con
Javier. Voz impersonal en la prosa expositiva; «el componente», en masculino.
