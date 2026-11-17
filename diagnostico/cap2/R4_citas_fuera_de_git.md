# Las citas literales, fuera de git (2026-11-17)

Decisión de Javier del 2026-11-17, conforme a la norma común de los cuatro cursos
(`Vault/Estandar/Capa de fuentes.md`, «Se recomienda guardar solo puntero y hash, y dejar el
literal fuera de git»). Sin commit ni push: queda en el árbol de trabajo de la rama
`claude/course-content-improvement-227f2c`.

## Diseño

- **En git**, cada fuente de `bibliografia/contraste/capN.yml` conserva clave, localizador, clase,
  página o instantánea, y cambia `cita` por `cita_sha256` (sha256 completo del literal pasado por
  la `normaliza()` del auditor: espacios, comillas y rayas no la mueven) y `cita_palabras` (el
  mismo recuento `len(literal.split())` que F11 hacía antes).
- **Fuera de git**, en `bibliografia/_local/citas/capN.yml` (ignorado por la regla
  `bibliografia/_local/` de `.gitignore`), los literales, con clave id de la afirmación →
  posición de la fuente en su lista (1, 2…), la misma «fuente n» que nombran los hallazgos.
- **El auditor** lee el literal local; F05 comprueba que su huella es la del registro y que está
  en la caché en ese localizador; sin literal local, «no comprobable aquí» y no aprueba. F11 usa
  `cita_palabras`. El nuevo F13 falla si el literal vuelve al registro versionado.

## Qué cambió en cada archivo

| Archivo | Cambio |
|---|---|
| `precalculo/migra_citas_fuera.py` (nuevo) | Pasa cada `cita:` del registro a `_local/citas/`, escribe huella y palabras, compara campo a campo antes y después (fuera de `cita` no cambia nada: ni `hash_texto`, ni veredictos, ni `verificado_por`, ni notas), relee el archivo local, y tras escribir hace una segunda pasada que no debe encontrar nada. Reejecutable: sobre un registro migrado comprueba que cada fuente tiene su literal con la huella y el recuento del registro. `--comprobar` no escribe. Una entrada nueva puede escribirse con `cita:` y este guion la saca. Se niega (sin escribir nada) si un literal local ya existe y es otro, si una fuente tiene `cita` y además huella, o si una línea `cita:` no es de una sola línea. |
| `bibliografia/contraste/cap1.yml`, `cap2.yml` | 89 + 152 líneas `cita:` → `cita_sha256` + `cita_palabras`. Además, la frase de la cabecera que decía «La `cita` es literal…» dice ahora dónde vive el literal. Ninguna otra línea cambió (comprobado con `diff` contra la copia previa). |
| `bibliografia/_local/citas/cap1.yml`, `cap2.yml` (nuevos, fuera de git) | Los 241 literales. |
| `precalculo/audita_citas.py` | `huella_cita()`, `palabras_cita()`; `Biblioteca` carga `_local/citas/` y da `literal(cap, id, n)`. F04 exige `cita_sha256` (64 hex) y `cita_palabras` (entero positivo) en vez de `cita`. F05: nuevo hallazgo si el literal local no corresponde a su huella (para toda fuente, sea cual sea el veredicto); sin literal local, «no comprobable aquí» (con `--sin-cache`, se cuenta en «sin literal local» sin fallar). F11: máximo de 25 con `cita_palabras` y, si está el literal, que coincida con su recuento; **el tope global de 400 palabras por obra se retiró** (dicho en el código y en el docstring). F13 (nuevo): una fuente con `cita`, o con su literal en otro campo, falla. A02 (aviso nuevo): una `nota`, `motivo` o `afirmacion` que repite un literal. |
| `precalculo/prueba_audita_citas.py` | El capítulo de prueba se construye con huella en el registro y literal en `_local/citas/`. Adaptadas: «cita alterada» (literal y registro coherentes, pero el literal no está en la página → F05) y «cita larga» (→ F11). Nuevas: literal local movido una palabra sin tocar el registro (mismo recuento, también está en la página: solo la huella lo delata → F05); literal local ausente (→ F05, «no comprobable aquí»); `cita_palabras` falseado (→ F11); fuente sin `cita_sha256` (→ F04); el literal vuelve al registro (→ F13). Y un bloque aparte: sin `_local/citas/` todo F05 dice «no comprobable aquí», y con `--sin-cache` informa de 2 sin aprobar ninguna. |
| `diagnostico/cap2/comprobaciones/r4_registro.py` | Adaptado al formato nuevo: escribe huella y palabras en el registro y los literales en `_local/citas/cap2.yml` (con el formato del guion de migración), y se niega a escribir si el registro fuera a llevar un `cita`. Regenerado en una carpeta temporal, produce **byte a byte** el `cap2.yml` migrado y el `_local/citas/cap2.yml`. |
| `diagnostico/cap2/comprobaciones/v4_extrae.py` | Lee el literal de `_local/citas/` (antes leía `f["cita"]` y fallaría). |
| `bibliografia/README.md` | Tabla «Dónde vive cada dato», paso 3 de «Contrastar una afirmación», qué hace el auditor sin `_local/`, F01–F13, 29 inyecciones, el guion nuevo, y que `_local/citas/` no se regenera: se copia. |
| `CLAUDE.md` | «con la cita literal del pasaje leído» → «con la huella de la cita literal del pasaje leído (el literal, fuera de git, en `bibliografia/_local/citas/`)». |

## Resultados

- `python3 precalculo/migra_citas_fuera.py`: 89 + 152 literales fuera; segunda pasada sin nada;
  `--comprobar`: «nada por migrar».
- `python3 precalculo/prueba_audita_citas.py`: **29 inyecciones, todas detectadas con su código
  exacto** (las 24 de antes y 5 nuevas), más los bloques `--sin-cache` y «sin `_local/citas/`».
- `python3 precalculo/audita_citas.py`: **OK**, 241 citas comprobadas contra la fuente, sin
  ningún F11 global (antes de la migración fallaba: FPP3 sumaba 902 palabras). Avisos: A01 (75,
  como antes) y A02 (10, todos del capítulo 1).
- `--cierre`: falla solo por las 8 pendientes del capítulo 2 (c2-m1-04, c2-m2-10, c2-m3-15,
  c2-m4-07, c2-m4-14, c2-m6-05, c2-m8-04, c2-m9-24); nada del 1.
- Con `_local/citas/` renombrado: 241 hallazgos F05 «no comprobable aquí», 0 comprobadas, sale
  con 1; con `--sin-cache`, «sin literal local: 241», 0 comprobadas. Se devolvió a su sitio.
- `genera_referencias.py --comprobar` y `audita_citas.py --uso-comprobar`: OK.
- `verifica_todo.py`: 11 verificadores en verde.

## Lo que la migración no resuelve

1. **El historial de git** conserva los literales del capítulo 1 (publicados) y no se ha
   reescrito. Los del capítulo 2 nunca se han comprometido.
2. **Otros archivos versionados del capítulo 1 tienen literales**, de las rondas ya publicadas:
   `diagnostico/cap1/comprobaciones/r4_entradas.py` (68), `r4_comprueba_citas.out` (62),
   `diagnostico/cap1/R4_cambios.md` (16), `r3b_ayuda_stl.txt` (14, ayuda de R), `R3_cambios.md`,
   `par_academico.md` y algunas salidas `.out`. No se tocaron: son el registro de lo hecho.
   Decide Javier.
3. **El propio registro del capítulo 1** repite literales en 9 notas y en el campo `afirmacion`
   de dos entradas (A02, `audita_citas.py --avisos`). Algunos son títulos (el artículo de STL, el
   nombre de Loess). Reescribir notas firmadas no entraba en esta tarea.
4. **Archivos sin seguimiento del capítulo 2 que no deben ir a git tal cual**:
   `diagnostico/cap2/comprobaciones/r4_registro.py` (144 literales en su tabla `ENTRADAS`),
   `v4_extrae.out` y `v4_extrae_2.out` (citas y contexto de la caché), `R4_verificacion.md` (14),
   `R4_cambios.md` (2), `v4_sin_marca.out` (1) y `diagnostico/cap2/par_academico.md` (6, este sí
   versionado).
5. **`_local/citas/` es dato primario sin copia**: no lo regenera ningún guion. Si se pierde, los
   literales del capítulo 1 se recuperan del historial y los del 2 de `r4_registro.py`, mientras
   exista.

## Para la copia principal (`main`), al fusionar

Sin ejecutar:

```sh
mkdir -p "/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo/bibliografia/_local/citas" && cp -p "/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo/.claude/worktrees/course-content-improvement-227f2c/bibliografia/_local/citas/cap1.yml" "/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo/.claude/worktrees/course-content-improvement-227f2c/bibliografia/_local/citas/cap2.yml" "/Users/javiermauriciosierra/Documents/Trabajo 2026/Bosque 2026/Series de tiempo/bibliografia/_local/citas/"
```

Huellas de los dos archivos al cerrar esta tarea (`shasum -a 256`):
`669eee23…f013b` (cap1.yml) y `cecb9e62…566ba` (cap2.yml). Después, en `main`:
`python3 precalculo/migra_citas_fuera.py --comprobar` y `python3 precalculo/audita_citas.py`.

## Sesión maestra, al cerrar (2026-11-17)

- **Tres archivos de trabajo salen de git**, porque reproducen casi todos los literales del capítulo 2: el guion
  que escribe el registro (`r4_registro.py`, 132 literales) y las dos salidas del verificador
  (`v4_extrae.out` y `v4_extrae_2.out`, 128 y 71). Viven ahora en `bibliografia/_local/herramientas/cap2/`,
  ignorada por git. El guion sigue funcionando desde allí; quien lo reejecute debe hacerlo en esa carpeta.
- **Los dos informes de la ronda** (`R4_verificacion.md`, 13 literales, y `R4_cambios.md`, 2) llevan ahora, en
  lugar de cada literal, un puntero `[literal fuera de git: _local/citas/cap2.yml, <id> · fuente <n>]`.
- **Lo que queda con texto de una fuente en archivos versionados, a criterio de Javier:** el título del artículo
  de la KPSS, que aparece en la lista de lecturas del capítulo, en el inventario y en una salida del verificador
  (un título bibliográfico, no una cita); siete fragmentos cortos (3–12 palabras) en notas firmadas de `cap1.yml`
  (aviso A02); y los archivos del capítulo 1 ya versionados que enumera el punto 2 de arriba. El historial de git
  conserva además los literales del capítulo 1 tal como se publicaron.
- **`_local/citas/` es dato primario sin copia**: no está en git y ningún guion lo regenera. Necesita la copia de
  seguridad del equipo.
