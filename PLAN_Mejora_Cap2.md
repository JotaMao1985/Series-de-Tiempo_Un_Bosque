---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-02 Estacionariedad, ACF y PACF]]"
fecha: 2026-11-16
estado: aprobado
---

# Plan — Mejora del capítulo 2 · Estacionariedad, ACF y PACF (Fase 2)

**Objetivo:** dejar el capítulo 2 correcto, con un orden en que nada se use antes de definirse,
con una sola regla para decidir cuántas veces diferenciar, con gráficas que se lean en el
teléfono, con sus fuentes contrastadas y con práctica en cada módulo. Es la segunda aplicación
del molde del capítulo 1 ([[PLAN_Mejora_Cap1]] §9).

**Estado: aprobado por Javier el 2026-11-16 (D1–D9, con D4: los arreglos de gráficas se propagan a los capítulos 3–6). R1 publicada el mismo día; R2 y R3, el 17; sigue la R4.** Lo que sigue es el
diagnóstico y el plan; las rondas se registrarán en §4.

## 1. El hueco — diagnóstico del 2026-11-16

Cinco lecturas independientes, cada una con su lente y sin conocer las conclusiones de las otras.
El detalle, con línea y evidencia, está en `diagnostico/cap2/`.

| # | Lente | Qué se encontró | Detalle |
|---|---|---|---|
| C1 | Corrección | **37 hallazgos: 7 errores**, 20 imprecisiones, 3 lagunas, 4 divergencias con FPP3, 3 sin comprobar. **Ninguna cifra publicada está mal calculada**: todas se reproducen en R y en statsmodels. Los errores están en afirmaciones generales y en lo que se concluye de cifras correctas | `par_academico.md` |
| C2 | Fuentes | **136 afirmaciones exigen fuente**: 60 de prioridad alta, 67 media, 9 baja. Para 80 hay pasaje completo en la caché o en la ayuda de R, 40 parcial, 16 ninguno. El capítulo no tiene ninguna cita marcada. Nombra sin cita a Dickey–Fuller, KPSS, Yule–Walker, Durbin–Levinson, Guerrero, MacKinnon, Ljung–Box. Atribuye a FPP3 una recomendación que FPP3 no hace | `fuentes.md`, `bibliografia/contraste/cap2_inventario.tsv` |
| C3 | Hilo | **Se usa antes de definirse**: ∇ en los M3, M5 y M6 (se define en el M7), la TRM en el M3 (en el M6), raíz unitaria y caminata en los M1–M3 (en el M5), la banda de la ACF en el M2 (en el M3). El orden de las diferencias se cuenta de tres maneras que no coinciden. Carga al revés que el cap. 1: declara 98 min y mide unos 72 sin abrir las soluciones; los M1–M8 sobran y el M9 falta (10 declarados, 19 medidos) | `lector_estudiante.md` |
| C4 | Gráficas | **49 problemas: 4 graves**, 27 medios, 18 leves; 11 comparten causa. Los correlogramas no numeran los rezagos 12 y 24 en pantallas estrechas, que son justo los que se piden leer. A 800 px siete tablas se cortan sin barra (en el M6 desaparece la columna «Veredicto»). El simulador del M5 contradice la nota que tiene al lado. Ningún error de consola; todas las bandas están bien calculadas | `graficas.md`, `capturas/` |
| C5 | Práctica | **Ninguna clave del quiz está mal** y todas las cifras de las soluciones salen. Pero toda la práctica escrita está en el M9: **los M1, M2, M3, M4, M5 y M8 no tienen nada**, y la PACF ninguna. Eligiendo la opción más larga se aciertan **5 de 5** preguntas de una sola respuesta. Las 8 pistas dan el criterio. P2, P7 y P8 hay que rehacerlas: sus respuestas están a la vista en el propio capítulo | `ejercicios.md` |

### Los errores, uno por uno (C1)

Los que comprobé yo mismo en R llevan ✔ (`diagnostico/cap2/comprobaciones/maestra_errores.R`);
los demás constan con su evidencia en el informe del par.

| Línea | Módulo | Qué dice | Qué es |
|---|---|---|---|
| 2515–2517 | M3 | ∇TRM: «r₁ = 0.088, todo lo demás dentro de la banda», como ejemplo de decaimiento exponencial | r₈ = −0.190 se sale de ±0.1675, y r₁ está dentro de la banda: no ilustra un decaimiento ✔ |
| 2835–2837 | M5 | Con ∇, «cualquier φ» da algo parecido a ruido blanco | ρ₁(∇y) = −(1−φ)/2: con φ = 0.5 vale −0.25, fuera de la banda; en el simulador, φ = 0 da r₁ = −0.506 |
| 3217–3221 | M6 | Entre R y statsmodels «solo cambia el tercer decimal» | 0.6132 frente a 0.5855: cambia el primero |
| 3398–3399, 3455, quiz P8 | M7 | «La primera diferencia de más **aumenta** [la varianza]; el mínimo señala el d correcto» | Falso en general: Var(∇y)/Var(y) = 2(1−ρ₁). Un AR(1) con φ = 0.8 y `ndiffs` = 0 pasa de 2.497 a 1.033 al diferenciar ✔ |
| 3476–3490 | M7 | Recuadro: «esa misma serie» ∇₁₂ log y; «el pico de r₁₂ = 0.841 pide la diferencia estacional, y tras aplicarla la serie ya está lista» | El 0.841 es de ∇log y. Sobre ∇₁₂log y, r₁₂ = −0.243, la ACF baja despacio desde 0.714, la varianza cae al diferenciar y `ndiffs` da 1: le falta una diferencia, como hace el pipeline del M9 ✔ |
| 3675–3677 | M8 | `pmdarima.BoxCoxEndogTransformer` es el equivalente de Guerrero | Estima λ con `scipy.stats.boxcox`, por máxima verosimilitud (leído en su código; `pmdarima` no está instalado) |
| 4002–4003 | M9 | «Seis preguntas… cada opción tiene su explicación» | Son ocho, y P2, P4 y P7 no tienen explicación por opción ✔ |

Además, comprobado por mí: el comentario Python de la l. 3893 atribuye a `urca::ur.kpss` el
truncamiento ⌊3√n/13⌋, que es el que `forecast::ndiffs` le pasa (el de `ur.kpss` por defecto es
⌊4(n/100)^¼⌋; la prosa del M7 en la l. 3484 lo dice bien) ✔; y `ywm` de statsmodels es Yule–Walker
sin ajuste, no Durbin–Levinson, que es `ldb` (l. 2654, 2742; los números coinciden) ✔.

Imprecisiones de más peso: el ADF con tendencia se cruza con el KPSS de nivel en la tabla de
veredictos; la banda N(0, 1/T) exige ruido i.i.d., justo después de advertir que incorrelación
no es independencia; el pipeline de R del M9 aplica Box–Cox con λ = −0.295 a `AirPassengers`
mientras el M8 recomienda el logaritmo, que es lo que usan los capítulos 4, 5 y 6; «FPP3 hace la
misma recomendación» no lo respalda FPP3; la lectura «FPP3 §3.2» no trata de Box–Cox.

## 2. Restricciones verificadas antes de planear

- **El capítulo 2 es la base del 3, y el 3 de los 4, 5 y 6.** `ensambla_cap3.py` parte del HTML
  del 2 y sustituye los módulos; lo que no es contenido de módulo (CSS, motor JS, cabecera) baja
  por la cadena 2 → 3 → 4 → 5 → 6. Editar solo dentro de los `<template>` no toca a los demás;
  editar el armazón obliga a reensamblar los cinco y a verificarlos.
- **El ayudante `crearGraficoBarras` es idéntico byte a byte en los capítulos 2 a 6**, que lo
  usan 54 veces. Arreglarlo en el 2 arregla la cadena entera al reensamblar.
- **Los bloques de código no muestran su salida**: el verificador de bloques encuentra 19 y
  comprueba 0 cifras. Ninguna cifra del capítulo está vigilada hoy por una máquina.
- **El código de la TRM descarga datos vivos y la prosa lleva cifras de junio de 2026** (138
  meses). Hoy hay 142, y la ADF de la página (−1.978) ya no es la que saldría. El veredicto no
  cambia, pero quien ejecute el código no ve los números del capítulo.
- **El Corte I ya se evaluó** (Taller 1, preparcial y Parcial 1): corregir no cambia nada que
  esté en evaluación. El semestre termina esta semana; lo que se arregle llega a 2027-I.
- Los datos salen de `precalculo/genera_cap2.R` → `precalculo/salidas/cap2_estacionariedad.json`
  y `cap2_datos.js`.
- Cambiar el número de ejercicios mueve las cifras de la portada y del README, que vigila
  `cuenta_sitio.py`.
- La 4.ª edición de Shumway y Stoffer, la que se cita, está en las colecciones electrónicas de la
  universidad; hace falta que Javier descargue los capítulos con su acceso.

## 3. Decisiones propuestas

Cada una lleva mi recomendación; las decide Javier.

- **D1 · Las mismas cinco rondas, en el mismo orden:** R1 errores → R2 gráficas → R3 estructura →
  R4 fuentes → R5 práctica. Cada ronda termina con `verifica_todo.py`, revisión visual, un
  verificador independiente sobre el diff, commit y tu visto bueno. *Recomendado: el molde
  funcionó, y el verificador encontró problemas en lo «terminado» en todas las rondas del cap. 1.*
- **D2 · Las salidas bajo `#>` entran en la R1**, no al final como en el cap. 1: así el
  verificador de bloques vigila el capítulo desde la primera ronda y cualquier cambio posterior
  que mueva una cifra falla. *Recomendado.*
- **D3 · La TRM, congelada:** el código lee la copia de 138 meses que ya usa `genera_cap2.R`,
  publicada junto al capítulo, y el ejercicio 4 queda como el lugar donde se descarga la serie
  actualizada y se compara. *Recomendado: «ninguna cifra a mano» incluye que el código publicado
  reproduzca la cifra publicada.*
- **D4 · Gráficas del armazón, a toda la cadena:** los arreglos en ayudantes compartidos
  (`crearGraficoBarras`, marcas de fecha, contraste de la banda) se hacen en el capítulo 2 y se
  reensamblan el 3, el 4, el 5 y el 6 en la misma ronda, con captura de sus correlogramas a tres
  anchos. La alternativa es arreglar solo el 2 y dejar que los demás lo hereden en su propia
  ronda. *Recomiendo propagar: el código es el mismo y un arreglo a medias deja la cadena
  divergente.*
- **D5 · Una sola regla para el orden de las diferencias** (estacional primero, como FPP3, que
  el inventario sí encontró respaldado), escrita una vez en el M7 y citada desde el M6 y el M9.
  La regla de la varianza deja de ser criterio de decisión: queda como señal, con el caso en que
  falla, y la señal de sobrediferenciación pasa a ser la autocorrelación cercana a −0.5 en el
  rezago 1.
- **D6 · El pipeline del M9 usa el logaritmo en `AirPassengers`**, como recomienda el M8 y como
  hacen los capítulos 4, 5 y 6; el umbral |λ| < 0.25 se retira o se explica. *Recomendado.*
- **D7 · Definir antes de usar**, sin renumerar módulos: ∇ se presenta en el M3 (donde aparece
  por primera vez) y el M7 lo formaliza; la TRM se presenta en su primera aparición; raíz unitaria
  y caminata se anuncian como adelanto del M5 donde se mencionan antes. Los minutos declarados se
  ajustan a lo medido.
- **D8 · Fuentes:** contrastar las 60 de prioridad alta y las 67 de media. Dar de alta en Zotero,
  con su DOI, las obras que el capítulo nombra y la biblioteca no tiene (Dickey y Fuller, Box y Cox,
  y las que el contraste exija), y conseguir texto de Kwiatkowski et al. (1992) y Guerrero (1993),
  que ya están en la biblioteca sin texto.
- **D9 · Práctica:** un ejercicio corto en cada módulo que no tiene (M1, M2, M3, M4, M5, M6 sobre
  una serie nueva, M8), sobre series distintas de las que el módulo usa; rehacer P2, P7 y P8;
  igualar longitudes; pistas que digan por dónde entrar. *Recomiendo siete ejercicios; con menos,
  la PACF y la tendencia determinista frente a estocástica se quedan sin práctica.*

## 4. Tareas

| # | Ronda | Tarea | Tam. | Depende |
|---|---|---|---|---|
| T1.1 | R1 | Los siete errores de C1, cada uno con su comprobación en R en `diagnostico/cap2/comprobaciones/` | M | — |
| T1.2 | R1 | Las imprecisiones y lagunas del par, una por una (ADF con tendencia y KPSS, banda i.i.d., `ywm`, truncamiento, signo de las cifras en Python) | M | T1.1 |
| T1.3 | R1 | Salidas reales bajo `#>` en los 19 bloques (D2); el verificador de bloques en verde sobre el capítulo | M | T1.1 |
| T1.4 | R1 | TRM congelada (D3); `pasajeros` creado en cada bloque Python que lo usa | S | — |
| T2.1 | R2 | Ayudantes compartidos: rezagos numerados en los correlogramas, marcas de fecha, contraste de la banda (`#e05a00`), eje que incluye el 0 (D4) | M | R1 |
| T2.2 | R2 | Anchos: tablas que se desplazan a 800 px, controles a una columna, fórmulas anchas con indicio de desplazamiento | M | T2.1 |
| T2.3 | R2 | El simulador del M5 y su nota, de acuerdo; pregunta 3 del quiz con el rezago 12 rotulado | S | T2.1 |
| T2.4 | R2 | Accesibilidad: `aria-live` en las 5 lecturas, `aria-label` que describa y no regale; Unicode en los rótulos del lienzo | S | T2.1 |
| T2.5 | R2 | Reensamblar 3–6 y capturar sus correlogramas a 1200, 800 y 375 px | M | T2.1–T2.4 |
| T3.1 | R3 | Definir antes de usar (D7): ∇, TRM, raíz unitaria, banda, MA(1) como adelanto del cap. 3 | M | R1 |
| T3.2 | R3 | Una regla de orden de diferencias y la varianza como señal (D5); reescribir el recuadro del M7 | M | R1 |
| T3.3 | R3 | Pipeline del M9 con logaritmo (D6); su resumen recoge las dos nulas contrarias y el caso tramposo del ADF; puente al cap. 3 | M | T3.2 |
| T3.4 | R3 | M6: las cifras en logaritmos dichas en la prosa; `γ` y `k` con un solo sentido; minutos declarados | S | R1 |
| T4.1 | R4 | Biblioteca: altas por DOI (D8); texto de Kwiatkowski et al. y Guerrero; capítulos de la 4.ª de Shumway y Stoffer | M | Javier, para el acceso institucional |
| T4.2 | R4 | Contrastar alta y media (127), marcar, citar y registrar; lecturas del M9 con secciones exactas | L | R3, T4.1 |
| T5.1 | R5 | Siete ejercicios cortos (D9), con solución calculada en R y salida bajo `#>` | L | R3 |
| T5.2 | R5 | Quiz: rehacer P2, P7 y P8; longitudes; pistas; retros que no filtren el ejercicio 1 y el 3 | M | R3 |
| T5.3 | R5 | Mejorar los cinco ejercicios del M9 (E1 con el log que aplica su propio pipeline; E2 con su control; E3 sin Ljung–Box o con él presentado) | M | R3 |

### Registro de rondas

- **R1 · errores — hecha y PUBLICADA el 2026-11-16** (`main` `7b03463` · gh-pages `016f211`). Los siete errores y las
  imprecisiones del par, una por una (`diagnostico/cap2/R1_cambios.md`). La varianza deja de decidir
  cuántas veces diferenciar, en ningún sentido: falla con un AR(1) estacionario (la baja sin hacer falta) y
  con un ARIMA(0,1,1) con θ = −0.8 (la sube con la diferencia que hace falta). Los 21 bloques muestran su
  salida bajo `#>` y el verificador de bloques pasa de 0 a 226 cifras comprobadas. La TRM se lee de una
  copia fija en `Htmls_Series/datos/`; cinco cifras publicadas estaban redondeadas dos veces. El
  verificador independiente encontró 15 problemas en lo ya corregido, uno de ellos bloqueante (la mitad
  de la regla de la varianza que se había conservado); todos resueltos. Para las rondas de los capítulos 4
  y 5: alinear su lenguaje sobre el mínimo de varianza con lo que ahora enseña el 2.

- **R2 · gráficas — hecha y PUBLICADA el 2026-11-17** (`main` `ee33ee6` · gh-pages `be45a73`). Los ayudantes compartidos se
  arreglaron en el capítulo 2 y se propagaron a los capítulos 3–6 (D4): rezago 12 rotulado en 168 de 168
  correlogramas por ancho (también en ejes j, k, h), fechas en eneros, banda en `#e05a00` (3.73:1), el 0
  rotulado, tablas anchas desplazables dentro de su caja (recortes de `<main>`: 90 → 0), lecturas que se
  anuncian una vez y `aria-label` que describen sin regalar el quiz. De los 49 problemas del diagnóstico:
  37 arreglados, 7 en parte, 1 ya resuelto en la R1, 4 no tocados con su motivo
  (`diagnostico/cap2/R2_cambios.md`). Ningún dato cambió: el verificador de bloques da lo mismo en los
  cinco capítulos. El verificador independiente encontró dos regresiones (el 12 perdido en el eje j del
  cap. 5 y las tablas estrechas entre 769 y 1199 px), resueltas; el redactor encontró y arregló una
  constante repetida que dejaba sin cargar el `<script>` del cap. 5. **La plantilla quedó distinta del
  capítulo 2** (no estaba aprobado tocarla). Para la R3: la pista de que una tabla sigue a la derecha.

- **R3 · estructura — hecha y PUBLICADA el 2026-11-17** (`main` `cfcd0a5` · gh-pages `29a2278`). Cada término se presenta o se anuncia donde
  aparece por primera vez (∇, la TRM, raíz unitaria, la banda, el logaritmo, MA(1) como adelanto del
  capítulo 3). Una sola regla para el orden de las diferencias, la estacional primero, en una caja del M7
  que citan el M6 y el M9, con un caso en que el orden cambia la cuenta (`log(UKgas)`). El pipeline del M9
  usa el logaritmo en R y en Python y su resumen recoge las dos nulas contrarias y el caso tramposo del
  ADF; el M9 cierra con lo que sigue en el capítulo 3. Se cumplen las promesas que el lector encontró
  rotas (el residuo del capítulo 1, el objetivo del M4, la tendencia determinista frente a la estocástica
  del M5 → M6, la contradicción de ADF y KPSS de la tarjeta). Minutos: 98 declarados → 106, a menos de
  0.4 min de lo medido en cada módulo. El verificador de bloques pasa a 277/277. En el armazón, la
  pista de que una tabla sigue a la derecha (un desvanecido que nunca apaga texto entero), propagada a
  los capítulos 3–6. El verificador independiente encontró 5 puntos que corregir y 13 menores; resueltos
  salvo dos menores anotados (`diagnostico/cap2/R3_cambios.md`). Queda abierto: en 38 de 169 tablas que
  se desplazan, el borde cae entre dos columnas y la pista casi no se ve hasta desplazar.

- **R4 · fuentes — hecha el 2026-11-17, sin publicar** (`main` `5ca421b`). 80 afirmaciones marcadas y
  registradas en `bibliografia/contraste/cap2.yml`: **51 respaldada, 12 con-matiz, 9 propia, 8 pendiente**
  (el mensaje del commit dice 52 y 8 por error), las 80 firmadas por un verificador independiente en dos
  lecturas. 79 citas visibles (FPP3, Cryer y Chan, Hamilton, ayuda de R); el capítulo pasa de 0 citas a 79.
  17 frases se reescribieron porque la fuente decía otra cosa; en la primera lectura el verificador devolvió
  23 entradas (7 errores, entre ellos que la regresión del rezago k «equivale» a Yule–Walker, cierto solo en
  la población). No se dio de alta ninguna obra: lo no leído no se cita. Las 8 `pendiente` esperan la 4.ª de
  Shumway y Stoffer, Kwiatkowski et al. (1992) y Guerrero (1993). `ensambla_cap3.py` conserva el pie propio
  de los capítulos 3–6, que siguen idénticos.

  **Citas literales fuera de git** (decisión de Javier del 2026-11-17, la que recomienda la norma común): el
  registro guarda `cita_sha256` y `cita_palabras`; el literal vive en `bibliografia/_local/citas/`. Deja de
  aplicarse el tope global por obra; F13 falla si un literal vuelve al registro. Detalle y lo que queda con
  texto de fuente en archivos versionados: `diagnostico/cap2/R4_citas_fuera_de_git.md`.

## 5. Criterios de aceptación

- [ ] Cada uno de los 7 errores tiene su comprobación en R y deja de reproducirse.
- [ ] `verifica_bloques_cap6.py --html` sobre el capítulo 2 comprueba sus cifras y da 0 discrepancias.
- [ ] Ningún término se usa antes de definirse o de anunciarse como adelanto.
- [ ] Los 20 lienzos, y los correlogramas de los capítulos 3–6, se leen a 1200, 800 y 375 px, con
      los rezagos 12 y 24 rotulados.
- [ ] `audita_citas.py --cierre` en verde con las afirmaciones de prioridad alta y media registradas.
- [ ] Cada módulo tiene al menos una práctica dentro del capítulo; la opción más larga no acierta
      más de una pregunta.
- [ ] La duración declarada de cada módulo dista menos de 3 min de la medida.
- [ ] `verifica_todo.py` en verde y los capítulos 3–6 reproducibles.

## 6. Riesgos

- **Tocar el armazón mueve cuatro capítulos más**: cada cambio de la R2 se reensambla en cadena y
  se verifica; un descuido aquí se publica cinco veces.
- **Las salidas bajo `#>` pueden revelar cifras que no coinciden** con la prosa en algún bloque
  que hoy nadie ejecuta; se resuelven en la R1, con R como árbitro.
- **El contraste de fuentes depende de obras que no hay en texto** (Kwiatkowski et al., Dickey y
  Fuller, la 4.ª de Shumway y Stoffer): sin ellas, la definición y la tabla de decisión del M6
  quedarían `pendiente`.
- **Sesiones concurrentes**: hay varias sesiones de mejora de contenido en marcha; commits por
  archivo y fusión probada antes de cada publicación.

## 7. Preguntas abiertas

Resueltas el 2026-11-16: Javier aprobó D1–D9 tal como están, D4 incluida.

1. ¿Descargas tú, con el acceso institucional, los capítulos de la 4.ª de Shumway y Stoffer y el
   artículo de Kwiatkowski et al. (1992), o te preparo la lista exacta de qué hace falta?

## 8. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Fase 0: [[PLAN_Gestion_Documental]] · Fase 1: [[PLAN_Mejora_Cap1]]
- Capítulo: [[20948-02 Estacionariedad, ACF y PACF]]
- Criterio: [[Criterio de contenido]] · [[Capa de fuentes]]
- Bitácora: [[2026-11-16]]
