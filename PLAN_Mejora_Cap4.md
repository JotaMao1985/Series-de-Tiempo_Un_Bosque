---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-04 Modelos ARIMA y Box-Jenkins]]"
fecha: 2026-11-22
estado: APROBADO (2026-11-22) — D1–D10 y las recomendaciones de §7.1 y §7.2
---

# Plan — Mejora del capítulo 4 · Modelos ARIMA y Box–Jenkins (Fase 4)

**Objetivo:** dejar el capítulo 4 correcto y coherente con el 2 y el 3, con lo que usa presentado antes
de usarlo, con un M10 que no cargue con todo, con simuladores que se lean y digan lo que dice la prosa,
con sus fuentes contrastadas y con práctica antes del final. Es la cuarta aplicación del molde de
[[PLAN_Mejora_Cap1]], [[PLAN_Mejora_Cap2]] y [[PLAN_Mejora_Cap3]]: cinco rondas, un redactor por ronda,
un verificador independiente sobre el diff y la sesión maestra volviendo a medir en R.

**Estado: APROBADO por Javier el 2026-11-22; R1 y R2 publicadas el mismo día (R2: `29106f5` · gh-pages `af3a60a`); R3 publicada el mismo día (`21ab628` · gh-pages `60a7bf9`); R4 hecha el 2026-11-23 (`d35dc3b`), sin publicar**, con D1–D10 y las recomendaciones de las preguntas 1 y 2 de §7.
El diagnóstico es del mismo día; las rondas se registrarán en §4.

## 1. El hueco — diagnóstico del 2026-11-22

Cinco lecturas independientes sobre `71c42d8`, cada una con su lente y sin conocer las conclusiones de
las otras. El detalle, con línea y evidencia, está en `diagnostico/cap4/`; mis comprobaciones, en
`diagnostico/cap4/comprobaciones/maestra_diagnostico.R` (`.out`).

| # | Lente | Qué se encontró | Detalle |
|---|---|---|---|
| C1 | Corrección | **El par no halla ningún error ni cifra incorrecta**: 7 imprecisiones, 7 menores y 2 dudosos. Los 23 bloques (13 de R, 10 de Python) corren y reproducen sus cifras; las 22 que el verificador de bloques no encuentra (713/735) son cifras de R citadas en comentarios de Python, umbrales, un redondeo y un formato de numpy. Las claves están bien: las 8 del quiz, las 38 del preparcial y las 10 del simulacro, recalculadas en R. **Pero dos lecturas más encontraron dos errores que el par no vio** (abajo) | `par_academico.md` |
| C2 | Fuentes | **357 afirmaciones exigen fuente**: 188 de prioridad alta, 131 media, 38 baja; 31 atribuciones. **Ninguna cita marcada** y el pie tecleado a mano. En la búsqueda, 152 respaldadas en lo leído, 38 con matiz o tensión, 2 discrepan, 18 no halladas, 23 no comprobables (obra sin texto), 4 cifras sin generador y 44 propias; 77 repiten una afirmación ya registrada en los caps. 2 o 3. El umbral de las raíces de `auto.arima` (1.01) se atribuye a Hyndman y Khandakar (2008), que dicen 1.001: 1.01 es el del código de `forecast`. La regla de 2 puntos de AICc, que sostiene el M7, no tiene fuente. La presa de Asuán no está en `?Nile`, que da «cerca de 1898»; Cobb (1978) no tiene texto. Lo que se atribuye a Box y Jenkins descansa en cuatro ediciones sin texto en disco | `fuentes.md`, `bibliografia/contraste/cap4_inventario.tsv` |
| C3 | Hilo | **El M10 tiene 3308 palabras** (los demás, de 704 a 1400) y hace cuatro cosas: el Nilo resumido tres veces, la TRM entera, el puente al cap. 5 y el cierre con la evaluación. **36 de 50 cifras de la prosa no salen de ningún bloque**, entre ellas el ARIMA(1,1,1) del Nilo (0.2544 y −0.8741 entran como constantes en el M1 y se justifican en el M10) y todo el puente al cap. 5. PP se usa en la l. 3251 y se nombra en la 4387; el «modelo de dos medias» va de la 3314 a la 4404; la TRM y `auto.arima` aparecen en el M5; Holt y el suavizamiento exponencial, en el M1, sin que el curso los haya presentado. Las introducciones del M3, M4 y M6 dan el resultado antes de la actividad. La promesa del M9 («El Módulo 10 lo mide», 83.9 %) no se cumple. **Minutos sin medir**: M1–M9 declaran 126 y miden 86.7; el M10 declara 24 y mide 29.4 (39.5 con soluciones, más 17.5 de autoevaluación). El M12 anuncia en futuro el Parcial 2 del 14 de octubre | `lector_estudiante.md` |
| C4 | Gráficas | **44 problemas: 2 graves**, 10 medios, 32 leves; 7 causas comunes. Ningún error de consola ni dato fuera del eje. Graves: a 1200 px el ΔAICc del explorador (M6) rotula 5 de sus 9 barras y deja sin nombre al mejor de d = 2; en el M9, el dibujo contradice la tabla (abajo). Comunes: `escalasLinea()` (solo del cap. 4) deja años sin redondear, fechas `AAAA-MM` crudas, guion por signo menos y el 0 sin su línea; ningún `aria-label` cambia con el estado aunque el armazón tiene `descripcionCorrelograma()`; la leyenda dibuja las líneas como cajas (armazón: toda la cadena 2 → 6); marcos de alto fijo con áreas de 52–94 px; dos iconos que Font Awesome 6.0.0 no trae | `graficas.md`, `capturas/` (fuera de git) |
| C5 | Práctica | **Ninguna clave mal.** Pero la primera tarea comprobable es el quiz, al final del M10 (l. 5473), tras 11 324 palabras. Hay 3 ejercicios, todos en el M10: el E2 se responde leyendo el M8 (l. 4384–4389) y repite `lynx` (práctica del cap. 3), el E3 está resuelto en el M9 y el E1 no demuestra lo que concluye. En el quiz (8 preguntas) la más larga acierta 4 de 5, las 8 pistas dan el criterio, las 8 respuestas están en pantalla en el capítulo y 7 son sobre el Nilo; la retro de la P1 resuelve el E1; la P4 dice «Son tres» y no tiene retro en ninguna opción. El M5 no tiene ningún elemento interactivo | `ejercicios.md` |

### Los dos errores que el par no vio

| Línea | Módulo | Qué dice | Qué es |
|---|---|---|---|
| 4581 (fuente `templates_7_9.html` l. 495), y la diapositiva de la forma del pronóstico | M9 | El ARIMA(1,1,1) sin constante pronostica «**constante en el último nivel**» | No queda en el último dato. Parte de 740 (1970), pasa a 816.18 en h = 1 y se aplana en 842.17, que es exactamente el límite $y_T + (\hat\phi\,\nabla y_T + \hat\theta\,\hat\varepsilon_T)/(1-\hat\phi)$. Lo constante es el nivel al que converge, no el último observado. Lo vio la lectura de gráficas (el dibujo contradice la tabla) ✔ |
| 3226, 3236, 4384, 5446; ejercicios 1 y 2; simulacro P10; diapositivas | M3, M8, M10 | La varianza es una de las «**tres evidencias** complementarias» para elegir $d$, y «si al diferenciar la varianza sube, te has pasado» es «la regla habitual» | **Contradice al capítulo 2**, que ya está contrastado: en una serie estacionaria $\operatorname{Var}(\nabla y)/\operatorname{Var}(y) \approx 2(1-r_1)$, así que la varianza repite lo que dice $r_1$ y **no decide** (`c2-m7-08`, cap. 2 l. 4320). Ninguna fuente de la caché propone el mínimo de la varianza como criterio. Lo vio el inventario de fuentes |

Además, comprobado por mí:
- **El umbral de 1.01** es el del código de `forecast` 9.0.2 (`minroot < 1 + 0.01` en `myarima`); el
  artículo dice 1.001. El ARIMA(2,1,2) del Nilo tiene la raíz AR en 1.0009 con CSS-ML, por debajo de
  los dos umbrales, así que lo descartaría cualquiera de ellos (corregido el 2026-11-22: antes decía que
  dependía del umbral del código; lo vio el verificador de la R1); con ML la menor raíz AR es 2.2407 ✔.
- **La pregunta 4 del quiz** da por cierta «con $d = 1$ la constante es la media de las diferencias».
  En el ARIMA(1,1,1) con deriva, la deriva de `forecast` es −2.88, la constante $c = \mu_w(1-\hat\phi)$
  es −2.10 y la media muestral de las diferencias es −3.84 ✔.
- **De las tres observaciones que la auditoría de las diapositivas dejó sobre el capítulo** («cinco
  modelos», «equivale» a Holt, el título de Cobb en plural), no queda ninguna: el capítulo ya dice
  «siete», «incluye» y el título en singular ✔.

Imprecisiones de más peso (el detalle, en el informe del par): el Ljung–Box del bloque de Python del M2
cuenta $y_1$ como residual; la regla «raíz MA unitaria ⇒ bajar $d$» sin la salvedad de la cancelación
AR/MA (justo la del ARIMA(2,1,2) de la TRM); el ARIMA(2,1,2) del Nilo cambia de raíces según el
estimador (M6 frente a M7); la diferencia de σ̂² entre `arima()` y `Arima()` se atribuye a CSS-ML
frente a ML y es el factor 99/97; el 89.6 % del cap. 6 se presenta como cobertura a 12 meses y es la de
los horizontes 1 a 12 juntos; la pregunta 6 dice «sin acercarse a cero» con $r_{10} = 0.09$.

## 2. Restricciones verificadas antes de planear

- **El capítulo 4 se ensambla** desde `ensamblado/cap4/` (`templates_1_3.html`, `templates_4_6.html`,
  `templates_7_9.html`, `templates_10.html`, `templates_11.html`, `templates_12.html`, `chapter.js`)
  con `ensambla_cap4.py`, **a partir del HTML del 3**; el 5 se ensambla a partir del 4 y el 6 a partir
  del 5. **Se edita la fuente, nunca el HTML final.** Lo que vive en `cap4/chapter.js`
  (`escalasLinea`, los simuladores) no lo tienen el 5 ni el 6; lo que vive en el armazón del 2 (la
  leyenda, `marcasLegibles`, `descripcionCorrelograma`) baja a toda la cadena. Cada ronda comprueba que
  los caps. 5 y 6 siguen idénticos o cambian solo donde se quería.
- **La sección 0 de `ensambla_cap4.py`** retira el CSS de las citas y devuelve el pie tecleado; se borra
  cuando este capítulo haga su R4, y la protección baja a `ensambla_cap5.py`.
- **Los bloques de la TRM descargan en vivo** de datos.gov.co (8 apariciones); la copia congelada
  `Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv` es la que usan los caps. 2 y 3.
- **No se renumeran módulos ni se cambian sus títulos sin necesidad**: el banco, el simulacro y el
  preparcial citan «4.N», y el guion de las diapositivas ancla cada cifra por un trozo del título
  (de la diapositiva, no del módulo). Las **diapositivas del cap. 4** (publicadas) repiten el error
  del M9 (`fuentes/capitulo_4.md` l. 615 y 624), las «tres evidencias» (l. 232–237 y 796) y el umbral
  de 1.01 (l. 479). Su verificador `verifica_directo_cap4.R` **no se reejecuta con otro R que el 4.3.3**.
- **El simulacro del M11** lo escribe `exporta_simulacro.py` desde el banco del quiz, fuera del repo
  (variante 9 de un quiz ya aplicado); **el preparcial** es una página del sitio cuyos ítems viven en
  `fuente/`, fuera del repo. Lo que se halle en ellos se anota para el banco. El texto del M11 y del
  M12 sí está en `templates_11.html` y `templates_12.html`.
- **El Corte II ya se evaluó**: corregir no cambia nada que esté en evaluación. Lo que se arregle llega
  a 2027-I.
- **Series ya usadas en la práctica** (no repetirlas): `EuStockMarkets`, `discoveries`, `LakeHuron`,
  `nhtemp`, `JohnsonJohnson`, `UKDriverDeaths`, `co2`, `USAccDeaths`, `UKgas` (cap. 2); `sunspot.year`,
  `lh`, la TRM, `WWWusage`, `treering`, `lynx` (cap. 3). El cap. 4 usa en la exposición `Nile`,
  `BJsales`, `AirPassengers`, `lynx` y `internet`. La lectura de práctica midió candidatas para cada
  hueco (`beaver2`, `austres`, GOOG 2018, `NelPlo`, Niño 3.4); su disponibilidad se confirma en la R5.
- Cambiar el número de ejercicios mueve las cifras de la portada y del README (`cuenta_sitio.py`).
- **Fuentes sin texto en disco:** Box y Jenkins (1970, 1976), Box, Jenkins y Reinsel (1994), Box,
  Jenkins, Reinsel y Ljung (2015), Cobb (1978), Kwiatkowski et al. (1992), Ljung y Box (1978),
  Brockwell y Davis (2016), FPP2 (2018), Guerrero (1993); la 4.ª de Shumway y Stoffer (la caché es la
  3.ª). Sin alta en la biblioteca, aunque se citan en lo leído: Phillips y Perron, Fuller (1976), Box y
  Pierce, Hurvich y Tsai; y las obras de software (`forecast`, `tseries`, `urca`, `statsmodels`).
  Ya hay texto de Hyndman y Khandakar (2008), que respalda casi todo el M7.

## 3. Decisiones propuestas

Cada una lleva mi recomendación; las decide Javier.

- **D1 · Las mismas cinco rondas, en el mismo orden:** R1 errores → R2 gráficas → R3 estructura →
  R4 fuentes → R5 práctica, cada una con `verifica_todo.py`, el verificador de bloques, revisión visual
  por HTTP, un verificador independiente sobre el diff, commit y tu visto bueno. *Recomendado: aquí el
  par no vio dos errores que vieron otras lentes; el verificador por ronda es lo que los atrapa.*
- **D2 · La TRM, congelada como en los caps. 2 y 3:** los bloques leen la copia publicada
  `datos/trm_mensual_2015-01_2026-06.csv`. *Recomendado.*
- **D3 · La varianza deja de ser una evidencia que decide $d$**, alineada con el cap. 2: el M3 dice que
  la caída de la varianza repite lo que dice $r_1$; las evidencias pasan a ser el gráfico y la ACF, las
  pruebas, y los síntomas de sobrediferenciar (raíz MA cerca de 1, $r_1$ cerca de −0.5), que el
  capítulo ya enseña. Toca el M3, el M8, el resumen y los ejercicios 1 y 2. *Recomendado: hoy el curso
  enseña una regla en el 4 que el 2 desmiente. Ver §7, pregunta 1.*
- **D4 · Lo que tiene arreglo en el armazón, a toda la cadena:** la muestra de línea en la leyenda, las
  `aria-label` con `descripcionCorrelograma()` y los dos iconos (se cambian por iconos que Font Awesome
  6.0.0 trae, sin subir de versión) se arreglan en el cap. 2 y se reensamblan el 3, el 4, el 5 y el 6 en
  la misma ronda. Lo de `escalasLinea()` y los marcos de alto fijo se arregla en `cap4/chapter.js`.
  *Recomendado, como en la R2 del cap. 3.*
- **D5 · Orden sin renumerar:** PP, el «modelo de dos medias», la TRM y `auto.arima` se presentan o se
  anuncian donde se usan por primera vez; la tabla de casos conocidos del M1 presenta en una frase el
  suavizamiento exponencial y Holt o los quita; el ARIMA(1,1,1) del Nilo se ajusta en un bloque visible
  la primera vez que se usa; las introducciones de simulador dejan de dar el resultado.
- **D6 · El M10, ordenado:** el Nilo se resume una vez; la TRM, el puente al cap. 5 (con su código) y
  el resumen, en ese orden, y el resumen es lo último antes de la evaluación. La promesa del M9 se
  cumple o se retira. *Sin partir el módulo: partirlo renumera.*
- **D7 · Minutos medidos**, con los paneles abiertos, como en los caps. 2 y 3: el capítulo declara lo que mide.
- **D8 · Fuentes:** contrastar las 188 afirmaciones de prioridad alta y las de media con texto en
  caché, reutilizando las 77 ya registradas en los caps. 2 y 3; marcar, citar y registrar; pie
  generado y la sección 0 de `ensambla_cap4.py` bajada al 5. El umbral de 1.01 se cita al código y se
  dice que el artículo da 1.001; la regla de 2 puntos se declara convención del capítulo o se cita si
  aparece fuente; la presa de Asuán se retira o se cita; lo de Box y Jenkins queda `pendiente` o se
  reescribe para no necesitarlo. *Recomiendo no cerrar la R4 con la media entera: en el cap. 3 se
  registraron 93 de las 119 altas.*
- **D9 · Práctica:** un «Para practicar» corto en cada módulo del M1 al M9 que no tenga práctica propia,
  sobre series distintas de las del módulo y de las de los caps. 2 y 3; el M5 gana una actividad. El E2,
  con otra serie, y la frase del M8 que lo resuelve, retirada o movida después; el E1 rehecho para que
  demuestre lo que concluye; el E3 sin el resultado impreso en el M9. Quiz: rehacer la P5 y la P8, la
  P4 con retro por opción y sin «Son tres», la retro de la P1 sin el E1, longitudes igualadas, pistas que
  digan por dónde entrar y preguntas sobre otras series que el Nilo.
- **D10 · El M11 y el M12 en pasado**, como el cap. 3: el texto deja de anunciar el Parcial 2 del 14 de
  octubre como futuro. Lo que se halló en el simulacro y el preparcial (el S5 del preparcial acepta el
  error de $n$ frente a $n^*$, 395.66) se anota para el banco, fuera de esta fase.

## 4. Tareas

| # | Ronda | Tarea | Tam. | Depende |
|---|---|---|---|---|
| T1.1 | R1 | Los dos errores (M9 y la varianza, D3), cada uno con su comprobación en R en `diagnostico/cap4/comprobaciones/`, editando `ensamblado/cap4/` | M | D3 |
| T1.2 | R1 | Las 7 imprecisiones y los 7 menores del par; las cifras sin generador (51.3 % y 100 % del Monte Carlo de ADF/PP, 83.9 %, 0.76, 1.07–1.14) a `genera_cap4.R` o a un bloque | M | T1.1 |
| T1.3 | R1 | TRM congelada (D2) y el M11/M12 en pasado (D10) | S | — |
| T2.1 | R2 | Armazón (D4): leyenda, `aria-label`, iconos; reensamblar 3–6 | M | R1 |
| T2.2 | R2 | `cap4/chapter.js`: `escalasLinea`, ΔAICc rotulado entero a 1200 px, cruces de AICc = ∞ sin recortar, colores de leyenda, marcos de alto fijo; capturas a 1200, 800 y 375 px | M | R1 |
| T3.1 | R3 | Orden (D5) sin renumerar | M | R1 |
| T3.2 | R3 | El M10 ordenado (D6); notación (`T`/`n`, `n*`, «abanico», «tres evidencias»); minutos medidos (D7) | M | T3.1 |
| T4.1 | R4 | Biblioteca: altas de Phillips–Perron, Fuller, Box–Pierce, Hurvich–Tsai y del software; texto de lo que consigas por acceso institucional (§7) | M | Javier |
| T4.2 | R4 | Contrastar, marcar, citar y registrar (D8); pie generado; sección 0 a `ensambla_cap5.py`; lecturas del M10 con localizadores leídos | L | R3, T4.1 |
| T5.1 | R5 | Los «Para practicar» de M1–M9 (D9), con solución calculada en R bajo `#>` | L | R3 |
| T5.2 | R5 | Ejercicios 1, 2 y 3; quiz | M | R3 |

### Registro de rondas

- **R1 (errores) — hecha y PUBLICADA el 2026-11-22 (`main` `1f82dec` · gh-pages `adea57a`).** El capítulo 4,
  su deck y los caps. 3, 5 y 6 en vivo, idénticos al commit. Redactor: `diagnostico/cap4/R1_cambios.md`;
  verificador independiente: `R1_verificacion.md`, con lo que hizo la sesión maestra al final.
  - Los dos errores corregidos: la tabla del M9 dice que el ARIMA(1,1,1) sin constante se aplana en
    842.17, no en el último dato, con un bloque que lo comprueba. La varianza deja de decidir $d$: las
    evidencias son el gráfico con la ACF, las pruebas y los síntomas de diferenciar de más, con la raíz MA
    primero y el $\hat\rho_1$ como indicio que falla en los dos sentidos (Módulo 2.7).
  - Las 7 imprecisiones y los 7 menores del par, más σ̂² (factor 99/97), el AICc de statsmodels y el
    φ = 0.271 del M5. Las cifras sin generador salen de `genera_cap4.R` (`nilo.sim_raiz_unitaria`) o de
    un bloque. La TRM se lee de la copia congelada. El M12 queda en pasado.
  - Tres diapositivas (y las que repetían lo mismo), con su guion: 469 claims, 0 que no coinciden;
    50 diapositivas a escala ≥ 88 %.
  - El verificador halló 2 errores, 2 imprecisiones y 7 menores en lo hecho. Entre ellos: el M11 afirmaba
    que el quiz ya se aplicó, y no consta (vuelve a su texto); la solución del ejercicio 1 leía un $r_1$
    positivo como prueba de que no sobra la diferencia; y la nueva tercera evidencia no traía la salvedad
    del cap. 2. También corrigió una frase de §1 de este plan (el 1.0009 queda bajo los dos umbrales).
  - Verificador de bloques: 762/762 (antes 713/735). `verifica_todo.py`, 11 en verde. Revisión por HTTP
    sin errores. Caps. 5 y 6 idénticos.
- **R2 (gráficas) — hecha y PUBLICADA el 2026-11-22 (`main` `29106f5`, registro `ae9511d` · gh-pages `af3a60a`).** Redactor:
  `diagnostico/cap4/R2_cambios.md`; verificador independiente: `R2_verificacion.md`, con lo que hizo la
  sesión maestra al final. De los 44 problemas de `graficas.md`: 41 arreglados, 2 en parte (la barra de 3 px
  del mejor en el ΔAICc; la leyenda de dos renglones del gráfico de residuales del quiz) y 1 que cerró la R1.
  - Armazón (cap. 2 → 3, 5, 6): la leyenda de `crearGraficoLinea` dibuja raya con su trazo, caja para las
    bandas y punto o cruz. Es lo único que cambia en los caps. 2, 3, 5 y 6 (el mismo diff, +68/−6).
  - Cap. 4: `escalasLinea` con los ayudantes del armazón; el ΔAICc rotula los nueve modelos a cualquier
    ancho (se tumba bajo 460 px de lienzo); cruces de AICc = ∞ enteras y sin cifra en el tooltip;
    `aria-label` que cambian con el estado y salen de los datos; marcos más altos (área mínima de 52 a
    125 px); en el M4 y el M10 las barras fuera de la banda van en el color de la serie y las de dentro en
    gris; dos iconos de Font Awesome 6.0.0; las dos `descripcionGrafico` del quiz dicen lo dibujado.
  - El verificador no halló Altos ni regresiones; sus 7 hallazgos (V1–V7) los corrigió la sesión maestra.
  - Quedan fuera, para el registro de pendientes: las copias del armazón en el cap. 1, la plantilla, los
    preparciales, los talleres y la guía del proyecto siguen dibujando líneas como cajas; dos entradas de
    leyenda discontinuas en los gráficos de dispersión del cap. 3; el eje ±1 de los correlogramas es
    convención del curso.
  - `verifica_todo.py`, 11 en verde; bloques del cap. 4, 762/762; recorrido por HTTP a 1200, 800 y 375 px
    sin errores de consola.
  - Publicación: `main` empujado hasta `ae9511d`, `audita_citas` OK (591 literales), `_local/` ya al día en
    la copia principal; los caps. 2–6 en vivo, idénticos byte a byte a `ae9511d`.
- **R3 (estructura) — hecha y PUBLICADA el 2026-11-22 (`main` `21ab628`, registro `0cacb6d` · gh-pages `60a7bf9`).** Redactor:
  `diagnostico/cap4/R3_cambios.md`; verificador independiente: `R3_verificacion.md`, con lo que hizo la
  sesión maestra al final. Solo cambia el cap. 4; los caps. 5 y 6, idénticos.
  - D5: el ARIMA(1,1,1) del Nilo se ajusta en un bloque visible del M1 (antes entraba como constante); PP,
    el «modelo de dos medias» (ajustado en un bloque del M3, de donde sale el 127.03) y `auto.arima` se
    presentan en su primer uso; el M1 presenta en una frase el suavizamiento exponencial y Holt; la nota de
    la TRM sale del M5 al M10. Las introducciones de simulador del M1, M3, M4, M6, M8 y M10 piden hacer y
    el resultado va después.
  - D6: el Nilo se resume una sola vez; luego la TRM, el puente al cap. 5 (con un bloque de R y Python del que
    salen todas sus cifras) y el resumen. La promesa del 83.9 % del M9 se cumple en el M10. Notación: `n` y
    `n*` se quedan, con un aviso en el M6 de que son la `T` de los caps. 2 y 3; «abanico» es solo la banda
    del pronóstico.
  - D7: minutos declarados = medidos con paneles abiertos, distancia máxima 0.5 (M1–M10: 135 min; el M10, 43).
  - El verificador halló 0 Altos, 2 Medios y 8 Bajos; los corrigió la sesión maestra. El más serio: al mover
    la nota de la TRM, la frase decía que la deriva del Nilo es la media de las diferencias (−2.883 frente a −3.84).
  - Abierto: el M10 no baja de tamaño (3 560 palabras) sin partirlo, y partirlo renumera; los rótulos del
    selector del M9, la caja de `lynx` del M8 y la nota de `BJsales` del M9 (dan respuestas de los
    ejercicios) quedan para la R5.
  - `verifica_todo.py`, 11 en verde; bloques 822/822 (antes 762); recorrido por HTTP a 1200 y 375 px sin errores.
  - Publicación: `main` empujado hasta `0cacb6d`, `audita_citas` OK; los caps. 2–6 en vivo, idénticos byte a byte
    a `0cacb6d`.

- **R4 (fuentes) — hecha el 2026-11-23 (`d35dc3b`), SIN PUBLICAR.** Javier decidió arrancarla con los textos que
  hay en disco (§7.3 sigue abierta). T4.1: alta por DOI de CRAN de `forecast` 9.0.2, `tseries` 0.10-62 y `urca` 1.3-4,
  como software con la versión leída (`enmiendas.yml`); 17 ayudas y los caps. 8 y 10 de FPP3 a la caché;
  `extrae_fuente.py --doc paquete::tema`. Phillips–Perron, Fuller, Box–Pierce y Hurvich–Tsai no se dieron de alta: sin
  texto solo serían `pendiente`, y esas pruebas se citan a Hamilton y a Cryer y Chan, leídos. T4.2 (redactor Fable 5.2
  con seis lectores): **286 afirmaciones registradas** (138 `respaldada`, 68 `con-matiz`, 76 `propia`, 4 `pendiente`:
  KPSS ×2, datos.gov.co y Shumway 4.ª), **252 citas visibles** (FPP3, Cryer y Chan, ayuda de forecast y de R, Hyndman y
  Khandakar, Hamilton, tseries). De las 188 altas del inventario, 145 registradas, 8 fuera y 35 sin marcar con motivo
  (16 en cadenas del quiz y el simulacro); la media no se cierra (42 sin marcar). 71 cambios de prosa, todos por lo que
  la fuente decía: el umbral de `auto.arima` con las dos cifras (1.001 del artículo, 1.01 del código); la regla de 2
  puntos de AICc como convención del capítulo; la presa de Asuán fuera (también de `genera_cap4.R`); nada depende ya de
  Box y Jenkins. Sección 0 de `ensambla_cap4.py` bajada a `ensambla_cap5.py`; pie y listas generados.
  - Dos verificadores independientes (Opus 5.5; M1–M6 y M7–M10): 0 Altos, 4 Medios (c4-m1-29 «solo», c4-m7-05 AIC
    frente a AICc, c4-m7-10 la raíz 1.0009, c4-m8-10 la cita de §9.1 pegada a las pruebas) y una decena de Bajos;
    los corrigió la sesión maestra (`r4_ediciones_maestra.py`) y los verificadores volvieron a firmar: **284 de 286
    firmadas** (sin firma, las dos KPSS `pendiente`).
  - La sesión maestra también: unificó «Rob J.» Hyndman (APA ponía iniciales en 139 citas); `genera_referencias.py`
    ordena sin la «y» ante el último autor (los caps. 1–3 no cambian); minutos de M1, M2, M8, M9, M10 = 12, 8, 12, 15,
    46 (declarado = medido, ≤ 0.4).
  - `verifica_todo.py` 11 en verde; bloques 822/822; `audita_citas.py` OK (`--cierre` falla por las 16 `pendiente`
    del sitio, 4 de este capítulo); caps. 5 y 6 byte a byte iguales; HTTP a 1200 y 375 px sin errores.
  - Fuera de la ronda: la presa y «Serie M»/«de libro» siguen en las diapositivas del cap. 4 y en
    `genera_soluciones.R`; el campo `fuente` del Nilo en `datos_series.json` dice «Cobb (1978)» y `?Nile` da Durbin y
    Koopman (no se ve); el quiz del M7 dice «umbral habitual de 2» (R5). Al publicar hay que copiar
    `bibliografia/_local/citas/cap4.yml` y `_local/herramientas/cap4/` a la copia principal.

## 5. Criterios de aceptación

- [ ] Los dos errores de §1 tienen su comprobación en R y dejan de reproducirse; el cap. 4 no contradice al 2.
- [ ] `verifica_bloques_cap6.py --html` sobre el capítulo 4 da 0 discrepancias (hoy 713/735); los bloques de
      Python, comprobados aparte.
- [ ] PP, el «modelo de dos medias», la TRM, `auto.arima`, Holt y el suavizamiento exponencial se presentan
      o se anuncian donde se usan por primera vez; ninguna cifra de la prosa sin un bloque o un generador.
- [ ] Los lienzos se leen a 1200, 800 y 375 px; el ΔAICc rotula todas sus barras; ninguna frase que el
      dibujo contradiga.
- [ ] `audita_citas.py --cierre` en verde para lo registrado, con las afirmaciones de prioridad alta registradas.
- [ ] Cada módulo del M1 al M9 tiene al menos una práctica; la opción más larga no acierta más de 1 de 5;
      ninguna retro adelanta un ejercicio.
- [ ] La duración declarada de cada módulo dista menos de 3 min de la medida.
- [ ] `verifica_todo.py` en verde, el capítulo 4 reproducible byte a byte y los 5–6 idénticos salvo lo que
      la ronda quería.

## 6. Riesgos

- **Editar el HTML final en vez de la fuente**: el siguiente reensamblado lo borra. Cada encargo lo dice
  y la comprobación de reproducibilidad lo atrapa.
- **El tamaño de la R4**: 357 afirmaciones, la mayor del proyecto (el cap. 3 tenía 254). Puede necesitar
  dos verificadores en paralelo, uno por obra.
- **Las diapositivas**: si el capítulo se corrige y el deck no, el curso enseña dos cosas distintas.
- **Los instrumentos del banco** comparten página con lo que se corrige; una ronda que los tocara por
  error cambiaría algo ya aplicado.
- **Sesiones concurrentes**: commits por archivo y fusión probada antes de cada publicación.

## 7. Preguntas abiertas

Resueltas el 2026-11-22: Javier aprobó D1–D10 y las recomendaciones de las preguntas 1 y 2 (la
varianza deja de ser una evidencia de $d$ en el cap. 4; las tres diapositivas que repiten hallazgos
entran en la R1). La 3 sigue abierta.

1. **La varianza como evidencia de $d$ (D3).** El cap. 2 dice que no decide; el 4 la usa como una de
   tres evidencias, en el resumen, en dos ejercicios, en el simulacro (P10) y en las diapositivas.
   ¿La retiro como evidencia en el cap. 4? *Recomiendo que sí: el cap. 2 tiene la razón y la
   cifra que la sostiene. El simulacro se anotaría para el banco.*
2. **Las diapositivas del cap. 4.** Repiten el error del M9, las «tres evidencias» y el umbral de 1.01.
   ¿Entran en esta fase (una tarea más en la R1 y otra en la R3, con su guion re-anclado) o se anotan
   para después? *Recomiendo que entren las tres diapositivas en la R1: son tres cambios puntuales y el
   deck está publicado.*
3. **Los textos que solo consigues tú**, con el acceso institucional: Box y Jenkins (1970 o la 5.ª ed.),
   Cobb (1978), Kwiatkowski et al. (1992), Ljung y Box (1978) y la 4.ª de Shumway y Stoffer. Sin ellos,
   lo que dependa de ellos queda `pendiente` o se reescribe.

## 8. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Fase 0: [[PLAN_Gestion_Documental]] · Fases 1–3: [[PLAN_Mejora_Cap1]] · [[PLAN_Mejora_Cap2]] · [[PLAN_Mejora_Cap3]]
- Auditorías previas del capítulo: [[PLAN_Auditoria_Cap4]] · [[PLAN_Movil_Decimal_Cap4]] · [[PLAN_Auditoria_Diapositivas_Cap4]]
- Capítulo: [[20948-04 Modelos ARIMA y Box-Jenkins]]
- Criterio: [[Criterio de contenido]] · [[Capa de fuentes]]
- Bitácora: [[2026-11-22]]
