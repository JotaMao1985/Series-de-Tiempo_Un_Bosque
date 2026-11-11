---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo:
fecha: 2026-11-10
estado: publicado
---

# Plan — Gestión documental y control de fuentes (Fase 0)

**Objetivo:** que ninguna cita del material pueda escribirse de memoria —igual que ninguna
cifra—, y que eso lo haga cumplir un auditor determinista y no la buena voluntad de un modelo.
Es la Fase 0 de la mejora de contenido del curso; la del capítulo 1 tiene plan propio y se
aprueba aparte, después del Checkpoint 0.

## 1. El hueco

| # | Carencia | Evidencia (medida el 2026-11-10) |
|---|---|---|
| C1 | No había registro bibliográfico | ni `.bib` ni CSL-JSON ni un solo DOI en el sitio; ~19 obras citadas en texto libre |
| C2 | No existía componente de cita | 0 `<cite>` en la plantilla y los capítulos; 1–3 citas sueltas por capítulo |
| C3 | Nada auditaba citas ni enlaces externos | ningún frente de fuentes en `precalculo/` |
| C4 | ~20 afirmaciones del cap. 1 sin atribuir | STL sin Cleveland et al. (1990), entre otras |
| C5 | Pie y «Lecturas» inconsistentes | el pie decía «Capítulo 3» en los caps. 4–6 y «Plantilla» en el 1; «3rd ed.» frente a «3.ª ed.» |
| C6 | Se contrastó contra una edición y se citó otra | Shumway y Stoffer: PDF de la 3.ª, cita de la 4.ª |
| C7 | El vault no tenía capa de fuentes | sin fila de Series en «Fuentes de contraste por curso» |
| C8 | Zotero no tenía nada del curso | 62 ítems de otro proyecto |

## 2. Restricciones verificadas antes de planear

- **Zotero 10.0.6**: la API local (`localhost:23119/api`) funciona y exporta CSL-JSON; hay campo
  nativo de clave de cita, vacío en todos los ítems. No se usa Better BibTeX.
- **pandoc 3.9** con `--citeproc` y `lang: es` escribe «3.ª ed.» y «et al.»; el `apa.csl` de
  Zotero pone «&», así que se deriva `apa-es.csl` con «y».
- **El repo es público**: ni PDF ni texto extraído pueden entrar a git.
- **FPP3 sirve hoy un capítulo por página**: `stl.html` redirige a `decomposition.html`. El
  auditor acota la búsqueda a la sección del localizador.
- **Crossref no registra el número de edición** de los libros de Springer ni las páginas del
  artículo de JSS: van en `bibliografia/enmiendas.yml`, con evidencia.
- **La guía del proyecto se ensambla desde la plantilla**: tocar el CSS de la plantilla obliga a
  reensamblarla (88 líneas de CSS añadidas, ninguna quitada; su auditor sale limpio).

## 3. Decisiones de esta ronda

- **D1** Se extiende el vault existente; no se crea otro. Cero plugins de comunidad. La capa de
  fuentes del vault la escribe la sesión de Muestreo para los cuatro cursos (2026-11-10).
- **D2** Citas autor-año con localizador en la prosa, y listas de referencias en APA 7 en español.
- **D3** Zotero lo opera Claude por el escritorio; incluye activar la API local.
- **D4** Se empieza con lo que hay: FPP3 en línea, PDF en disco, artículos abiertos.
- **D5** Una sola fuente de verdad por dato: Zotero es la entrada, el repo guarda la instantánea,
  el vault es navegación.
- **D6** Sin Better BibTeX. Las claves se fijan en `bibliografia/claves.json`.
- **D7** Se cita la edición que se leyó.
- **D8** Ejemplares admitidos: Cryer y Chan 2.ª, Hamilton, Shumway y Stoffer 3.ª (como 3.ª). El
  PDF de Tsay con marca «z-lib» no entra.
- **D9** Quinta pregunta del *Criterio de contenido*: «¿Tiene fuente?».
- **D10** `CLAUDE.md` en la raíz, con las dos normas duras.
- **D11** Se trabaja en la rama del worktree; fusionar a `main` y publicar se consultan.
- **D12** *(surgió al ejecutar)* Cada cita enlaza a una lista «Fuentes citadas en este módulo»,
  porque solo el módulo abierto está en el DOM; la lista del capítulo va en el módulo 9.
- **D13** *(surgió al ejecutar)* La página impresa se comprueba en el encabezado de la página
  del PDF, no con un desfase fijo: en Cryer y Chan el desfase va de 13 a 10.

## 4. Hechos verificados leyendo (no recordados)

| Hecho | Dónde se leyó |
|---|---|
| $F_T$ y $F_S$ están en FPP3 **§4.3** «STL Features», no en §3.6 como dice el capítulo publicado | `otexts.com/fpp3/features.html`, 2026-11-10 |
| FPP3 desarrolla STL como «Seasonal **and** Trend decomposition using Loess»; el capítulo dice «Seasonal-Trend» | FPP3 §3.6 |
| FPP3 lista cuatro problemas del método clásico; el capítulo, tres. «$m/2$» solo es exacto con $m$ par | FPP3 §3.4 y §3.3 |
| FPP3 no dice que la robustez cueste un segundo bucle ni que `stl()` la traiga desactivada | FPP3 §3.6 (sin ninguna mención a bucles ni a `stl(`) |
| FPP3 da Cleveland et al. (1990) como JOS 6(1), 3–33; OpenAlex, 3–73 | FPP3 §3.8; `bibliografia/obras.tsv` |
| Existe una 5.ª edición de Shumway y Stoffer (Springer, 2025); el syllabus cita la 4.ª | Crossref, DOI 10.1007/978-3-031-70584-7 |
| Box et al., 5.ª ed.: 2016 según la Library of Congress, 2015 según el syllabus | registro de Zotero |
| El PDF de Shumway y Stoffer en disco es de la 3.ª ed. y tiene 202 de unas 600 páginas | portada y encabezados del propio PDF |

## 5. Tareas

| # | Tarea | Estado |
|---|---|---|
| T0.1 | Respaldos; API local de Zotero; pandoc en español | ✅ |
| T0.2 | Lista maestra de obras con identificador verificado en red (`bibliografia/obras.tsv`, 26 filas) | ✅ |
| T0.3 | Colección `Docencia › 20948 Series de Tiempo` en Zotero: 23 obras por identificador | ✅ — faltan 3 sin identificador (ver §7) |
| T0.4 | `exporta_zotero.py`, `extrae_fuente.py`, `ejemplares.yml`, `instantaneas.yml`, `.gitignore` | ✅ |
| T0.5 | `audita_citas.py` (F01–F12, A01) y `prueba_audita_citas.py` (24 inyecciones) | ✅ |
| T0.6 | `genera_referencias.py` y componente `.cita` en la plantilla y el cap. 1 | ✅ |
| T0.7 | Piloto: 5 afirmaciones de los módulos 6–8 del cap. 1, de punta a punta | ✅ — 2 respaldadas, 1 con matiz, 2 pendientes |
| T0.8 | Capa de fuentes en el vault | ➡️ pasa a la sesión de Muestreo (decisión de Javier, 2026-11-10). Series entrega `bibliografia/uso_fuentes.json` (T0.11) |
| T0.9 | `verifica_todo.py` | ✅ |
| T0.11 | *(pedido por la sesión de Muestreo)* vocabulario cerrado de localizadores en el auditor y `bibliografia/uso_fuentes.json` | ✅ — `data-via` sin implementar |
| T0.10 | Este plan, `bibliografia/README.md`, `CLAUDE.md`, bitácora y nota del curso | ✅ |
| **CP0** | Revisión de Javier | ⬜ — pero la Fase 0 se publicó el 2026-11-11 junto con la R1 del capítulo 1 (`main` `b26787e` · gh-pages `4052a27`), por decisión de Javier. Las preguntas de §7 siguen abiertas |

## 6. Criterios de aceptación

- [x] `python3 precalculo/prueba_audita_citas.py`: 24 inyecciones, todas con su código exacto.
- [x] `python3 precalculo/audita_citas.py`: en verde, con 7 citas literales comprobadas contra FPP3.
- [x] `python3 precalculo/exporta_zotero.py --comprobar`: el repo coincide con Zotero.
- [x] `git check-ignore bibliografia/_local/x.pdf`: nada con derechos entra al repo.
- [x] El piloto se ve en el navegador (cita, lista del módulo, pie); a 375 px no desborda.
- [x] «Trayectorias PostTX» conserva sus 62 ítems en Zotero.
- [ ] `python3 precalculo/verifica_todo.py` en verde: **falla `cuenta_sitio.py`, y fallaba antes de
      esta ronda** (la portada dice 68 simuladores y son 70; el cap. 5 dice 12 y son 14).
- [ ] Javier firma las cinco entradas del piloto.

## 7. Lo que queda abierto para el Checkpoint 0

1. **Permiso para descargar** el PDF de Cleveland et al. (1990) del archivo del JOS (Statistics
   Sweden, 2,8 MB): sin él, dos afirmaciones del piloto siguen `pendiente`.
2. **¿El pie se regenera ya en los seis capítulos** o capítulo a capítulo? Hoy solo el cap. 1 lo
   toma de Zotero; los otros cinco conservan el pie tecleado, con «Capítulo 3» en los caps. 4–6.
3. **«y» o «&»** en las citas: se eligió «y» (la prosa es en español).
4. **Año de Box et al., 5.ª ed.**: 2015 o 2016.
5. **Edición de Shumway y Stoffer**: seguir con la 4.ª o pasar a la 5.ª (2025).
6. **Guerrero (2003)** y **Box y Jenkins (1970)**: no tienen identificador que Zotero resuelva;
   hay que transcribir la portada.
7. **Procedencia de los tres PDF** admitidos (queda «por confirmar» en `ejemplares.yml`).
8. Zotero adjuntó solo, al buscar el ISBN de FPP3, un PDF de 28 KB con la tabla de contenido
   (catálogo GBV). No es el libro y el exportador lo ignora; se puede borrar.
9. **¿`git init` en `Vault/`?** Hoy el vault no tiene control de versiones.
10. ~~Quién escribe la capa de fuentes del vault.~~ **Resuelto el 2026-11-10: la escribe la
    sesión de Muestreo**, como dice `Vault/Estandar/Capa de fuentes.md`. Series no toca
    `Vault/Estandar`, `Vault/Bases`, `Vault/scripts` ni `Vault/Fuentes`; entrega
    `bibliografia/uso_fuentes.json` y, si necesita una propiedad o una fila, la pide. Las notas de
    fuente de Series aparecerán en el vault cuando esta rama se fusione a `main`, que es de donde
    lee su generador. De esa norma falta aquí `data-via` (citas de segunda mano).

## 8. Riesgos

- **La caché `_local/` es de cada copia de trabajo.** Tras fusionar a `main` hay que correr
  `extrae_fuente.py` allí, o el auditor dirá «no comprobable aquí».
- **FPP3 cambia en línea.** La instantánea lleva fecha y huella; si la página cambia, F05 falla
  y obliga a releer.
- **Operar Zotero por el escritorio es frágil**: el panel de «Añadir por identificador» se
  cierra si la ventana pierde el foco. Una vez las teclas fueron al árbol de colecciones (se
  plegó; nada se perdió). El respaldo es pegar los identificadores a mano.
- **El texto de un PDF escaneado tiene erratas** (Hamilton): una cita literal correcta puede no
  coincidir.

## 9. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Criterio que motiva la ronda: [[Criterio de contenido]]
- Cómo funciona: `bibliografia/README.md`
- Bitácora: [[2026-11-10]]
