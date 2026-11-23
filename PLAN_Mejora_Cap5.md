---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-05 Modelos SARIMA]]"
fecha: 2026-11-23
estado: PROPUESTO — diagnóstico hecho, plan sin aprobar
---

# Plan — Mejora del capítulo 5 · Modelos SARIMA (Fase 5)

**Objetivo:** dejar el capítulo 5 correcto y coherente con el 2, el 3 y el 4 recién revisados, con lo que
usa presentado antes de usarlo, con un M11 que no cargue con todo, con simuladores que digan lo que dice
la prosa, con sus fuentes contrastadas y con práctica en cada módulo. Es la quinta aplicación del molde de
[[PLAN_Mejora_Cap1]] a [[PLAN_Mejora_Cap4]]: cinco rondas, un redactor por ronda, verificadores
independientes sobre el diff y la sesión maestra volviendo a medir en R.

**Estado: PROPUESTO.** El diagnóstico es del 2026-11-23; las decisiones de §3 y las preguntas de §7 las
decide Javier.

## 1. El hueco — diagnóstico del 2026-11-23

Cinco lecturas independientes sobre `f807b40`, cada una con su lente y sin conocer las conclusiones de
las otras. El detalle, con línea y evidencia, está en `diagnostico/cap5/`; mis comprobaciones, en
`diagnostico/cap5/comprobaciones/maestra_diagnostico.R` (`.out`).

| # | Lente | Qué se encontró | Detalle |
|---|---|---|---|
| C1 | Corrección | **1 error, 1 cifra incorrecta, 7 imprecisiones, 9 menores y 2 dudosos.** Los 27 bloques corren; las 13 cifras que el verificador no halla (1199/1212) son 4 de un ajuste de statsmodels que **no converge** (el bloque silencia el aviso), 3 de una salida de R escrita a mano, 2 de formato, 1 de redondeo y 3 falsos positivos. El M11 se reproduce exacto (61 y 49 orígenes); las 8 claves del quiz y las 12 del simulacro, recalculadas, están bien. Error: el *airline* «acumula incertidumbre más despacio que una caminata» (M5). Imprecisiones de peso: la regla de la varianza atribuida al cap. 4, la ACF de un MA×SMA factorizada con $q < m$ (hace falta $2q < m$), el Ljung–Box de R presentado como «limpio» frente al de Python cuando R también cuenta 13 residuales de arranque, los errores estándar de Python atribuidos a la diferenciación de los regresores (es OPG frente a la hessiana) y el ARIMA$(0,0,0)(0,1,0)_{365}$ atribuido a $m$ y no a $n < 3m$ | `par_academico.md` |
| C2 | Fuentes | **281 afirmaciones exigen fuente**: 119 de prioridad alta, 121 media, 41 baja; 26 atribuciones. **Ninguna cita marcada** (la sección 0 lo impide). En la búsqueda, 85 respaldadas en lo leído, 37 parciales, 53 con matiz o tensión, 2 discrepan, 35 no halladas, 26 no comprobables (obra sin texto), 5 cifras sin generador y 38 propias; **70 repiten una afirmación ya registrada** en los caps. 1–4 (39 del 4). Lo que más pesa: la regla de la varianza (ninguna fuente la propone); la sobrediferenciación estacional, que las fuentes solo dan para la diferencia regular; «primero $D$, después $d$» está respaldado, pero su porqué y la historia de `nsdiffs` («antes OCSB»; el artículo de Hyndman y Khandakar usa Canova–Hansen) no; el *airline* («Box y Jenkins lo llamaron así», «el más usado del mundo», un año que Cryer y FPP3 dan distinto); la tabla «dónde brilla / dónde falla» del M11, atribuida a las competencias M4 y M5, que ninguna obra de la biblioteca nombra; la regla de 2 puntos de AICc sin declararla convención (el 4 sí lo hizo); Ljung–Box «al menos $2m$» (FPP3 pone tope en $T/5$). Las lecturas atribuyen TBATS a FPP3 §12.1, que no lo menciona ✔ | `fuentes.md`, `bibliografia/contraste/cap5_inventario.tsv` |
| C3 | Hilo | **El M11 hace cuatro cosas** (1 899 palabras, 2 469 con los plegados): usa ETS, «naïve estacional» y RMSE sin presentarlos, muestra tres veces la misma comparación de ocho métodos con un pie que ya revela «el SARIMA pasa a primero», y su clímax (unas 25 cifras) no tiene código aunque una nota dice que se reproduce con el del capítulo. **Minutos sin calibrar**: M1–M10 declaran 155 y miden 109.3 (M2 1.68 veces lo declarado; M5 0.37); el cap. 4 sale en 1.0. Solo el M1 y el M11 cierran apuntando al siguiente. **Cuatro remisiones rotas** (M1 → «Módulo 5» por el 6; M6 → manchas solares del cap. 3; M11 → «el código del capítulo»; cap. 6 → un `biasadj` que el 5 no nombra). El criterio «raíz MA sobre el círculo» del M3 lo desmiente el M7. 32 de 64 grupos de cifras de la prosa no salen de ningún bloque. El M2 explica cuatro veces el satélite; el M5, que define el *airline*, no tiene código | `lector_estudiante.md` |
| C4 | Gráficas | **42 problemas: 4 Altas**, 13 Medias, 25 Bajas. Ninguna excepción, NaN ni dato recortado; ningún dibujo depende de la red (la TRM va incrustada). Altas: M1 «dos barras» (son seis); M5 la intro del `airline-pesos` dice lo contrario de lo que dibuja; M9 con solo Semana Santa muestra las cifras de otro modelo; M11 con los 8 métodos la leyenda se corta a 800 y 375 px. Lo que el cap. 4 arregló en el armazón (muestra de línea, rótulos 12/24/36, signo menos) **llega bien**; `descripcionCorrelograma()` **no** llega, porque cada capítulo la llama desde su JS: los 15 `aria-label` son fijos. El componente `.mapa-estacional` (compartido con el cap. 1 y la plantilla) tiene cuatro defectos: contraste 2.24:1, solo enero–junio visibles a 800/375 px, guion por signo menos y una tabla sin filas para el lector de pantalla | `graficas.md`, `capturas/` (fuera de git) |
| C5 | Práctica | **Ninguna clave mal.** Pero **0 «Para practicar»** (el cap. 4 tiene 9): la primera tarea es el quiz, tras 9 912 palabras. E1 (`co2`, serie del cap. 2) se puede mejorar; **E2 hay que rehacerlo** (está resuelto en el M8 y las retros del quiz lo responden); **E3 hay que rehacerlo** (la parte (a) es la tabla del M8 y la solución de la (b) describe mal el error). Quiz: la más larga acierta 5 de 5, las 8 pistas dan el criterio, las 8 respuestas están en pantalla, 4 retros resuelven ejercicios, y no hay ítems del M5, M7, M8 ni M10. Las tres series de los ejercicios repiten capítulos anteriores. El Excel (77 fórmulas, 116 comprobaciones) se puede mejorar: no pide decisiones y se anuncia solo al final del M11 | `ejercicios.md` |

### Lo que una lente vio y otra no

| Línea | Módulo | Qué dice | Qué es | Lo vio |
|---|---|---|---|---|
| 4590–4593 [`templates_4_6.html` 263–266] y diapositiva l. 678 | M5 | El *airline* «acumula incertidumbre más despacio que una sola caminata», por «el mismo mecanismo que el $\psi_\infty = 0.169$ del Nilo» | Solo hasta $h = 41$. La raíz unitaria en $B = 1$ es **doble**: los $\psi_j$ crecen sin límite ($\psi_{240} = 6.08$) y desde $h = 42$ el *airline* acumula **más** incertidumbre que una caminata con la misma $\sigma$ (en $h = 240$, 53.98 frente a 15.49) ✔ | par |
| Intro del `airline-pesos` y diapositiva l. 682 | M5 | Con $\Theta \to 0$ «el escalón del rezago 12 desaparece» | Al revés: con $\Theta = 0$ el salto $\psi_{12} - \psi_{11}$ es 1.000, el mayor; con $\Theta = -0.99$ es 0.010 ✔ | gráficas |
| 4067, 4404, 4408, 4829, 5926; diapositivas l. 435 y 508 | M3, M4, M7, E1 | «La regla de la varianza mínima —del Capítulo 4— señala $d=1, D=1$»; «Si la varianza sube al diferenciar, también [sobra la diferencia]» | El cap. 4 revisado dice que la varianza **no decide** $d$ (repite $r_1$), como el cap. 2 (`c2-m7-08`). Atribuirle la regla al 4 es falso ✔ | maestra, par |
| 6084 y siguientes [`templates_10_11.html`] | E3(b) | El error es responder «el armónico, por dos puntos» | El armónico $K = 4$ tiene el AICc **mayor** (180.200 frente a 178.209) y no pasa Ljung–Box(24) ($p = 0.0439$): la lectura ingenua elige el *airline*, que es lo correcto. La trampa del $n$ efectivo no muerde aquí ✔ | ejercicios (el par dio las soluciones por buenas) |
| 4693 y diapositiva l. 790 | M6 | «en el Capítulo 3 los dos criterios discrepaban sobre las manchas solares» | En el cap. 3 coinciden: el ARMA(2,1) gana por los dos (l. 5731) y, sobre la raíz cuadrada, el AR(2) también (l. 6011) ✔ | lector (el par no lo localizó) |
| 4085–4107, 4394, 5885 frente a 4900–4904 | M3, M4, M7 | El M3 enseña $\lvert\text{raíz MA}\rvert^{-1}$ cerca de 1 como firma de sobrediferenciar; el M7 lo matiza | Con un SMA(1), $\lvert\text{raíz}\rvert^{-1} = \lvert\Theta\rvert^{1/12}$: ya con $\Theta = -0.5569$ vale 0.9524 y con $\Theta = -0.9$, 0.9913, por encima del umbral de 0.99 que usa el simulador y que la prosa no da ✔ | lector |

✔ = comprobado por mí (`maestra_diagnostico.out`, o por lectura de la caché y del HTML).

Además, comprobado por mí:
- **Acentos rotos en los datos incrustados:** `SERIES_CAP5` (l. 6302) trae 4 secuencias literales `<c3><ad>` y
  `<c3><b3>` («aerol…neas», «Concentraci…n», «v…a datos.gov.co» dos veces); vienen de
  `precalculo/salidas/cap5_sarima.json`, así que el arreglo va al generador.
- **TBATS:** la tabla de lecturas lo atribuye a FPP3 §12.1; en las diez secciones de la caché no aparece y
  §12.1 trata la estacionalidad compleja con términos de Fourier.
- **El M12 habla en presente** del quiz del 11 de noviembre, ya aplicado.

## 2. Restricciones verificadas antes de planear

- **El capítulo 5 se ensambla** desde `ensamblado/cap5/` (`templates_1_3.html`, `templates_4_6.html`,
  `templates_7_9.html`, `templates_10_11.html`, `templates_12.html`, `chapter.js`, `simulacro.js`) con
  `ensambla_cap5.py`, **a partir del HTML del 4**; el 6 se ensambla a partir del 5. **Se edita la fuente,
  nunca el HTML final.** Cada ronda comprueba que el 6 sigue idéntico o cambia solo donde se quería.
- **La sección 0 de `ensambla_cap5.py`** retira el CSS de las citas y el pie generado que hereda del 4; se
  borra cuando este capítulo haga su R4, y la protección baja a `ensambla_cap6.py`.
- **El componente `.mapa-estacional`** vive en `ensamblado/componentes/mapa_estacional.{js,css}` y lo
  comparten el cap. 1 (editado a mano, publicado), la plantilla y el 5 (`retropropaga_mapa.py`). Arreglarlo
  toca el cap. 1 y la plantilla, y la plantilla obliga a `ensambla_proyecto.py`.
- **`descripcionCorrelograma()` está en el armazón**, pero cada capítulo la llama desde su `chapter.js`:
  el 5 tiene que adoptarla como hizo el 4.
- **Los bloques de la TRM descargan en vivo** de datos.gov.co (l. 3180, 5202, 5258, 6088); la copia
  congelada `Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv` es la que usan los caps. 2 a 4. Los
  simuladores ya llevan la TRM incrustada.
- **El simulacro del M12** lo escribe `exporta_simulacro.py` en `ensamblado/cap5/simulacro.js` desde el
  banco del quiz del capítulo, fuera del repo; es la variante de un quiz de Brightspace ya aplicado (11 nov).
  Lo que se halle en él (N7 acepta olvidar el satélite, N5 acepta dividir entre $n$, S11 con dos
  lecturas, «las noches» en la ruta de N2) se anota para el banco.
- **Las diapositivas del cap. 5** (84, publicadas) repiten cuatro de los hallazgos: la regla de la varianza
  (`fuentes/capitulo_5.md` l. 435 y 508), el *airline* frente a la caminata (título de la l. 678), $\Theta
  \to 0$ (l. 682) y las manchas solares (l. 790). Su verificador es `verificacion/verifica_directo_cap5.R`
  y el guion ancla por el título de la diapositiva.
- **Los libros de Excel** (`ejercicios/capitulo-5-sarima-{ejercicio,solucion}.xlsx`) los generan
  `genera_excel_cap5.py` y los verifica `verifica_excel_cap5.py` con Excel real: cambiar las series o las
  cifras del M11 obliga a regenerarlos y a recalcularlos en Excel.
- **La subsección de momentos del M2** entró por [[PLAN_Varianza_SARIMA]] (22 sep), con tu autorización;
  el lector dice que nada posterior la usa. No se retira sin preguntarte.
- **No se renumeran módulos ni se cambian sus títulos sin necesidad**: el banco, el simulacro, la portada
  («Clase 1» y «Clase 2») y el guion de las diapositivas los citan.
- **El quiz del capítulo ya se aplicó** (11 nov) y el Corte III se cierra con el proyecto: corregir no cambia
  nada en evaluación. Lo que se arregle llega a 2027-I.
- **Series ya usadas en la práctica** (no repetirlas): `EuStockMarkets`, `discoveries`, `LakeHuron`,
  `nhtemp`, `JohnsonJohnson`, `UKDriverDeaths`, `co2`, `USAccDeaths`, `UKgas` (cap. 2); `sunspot.year`,
  `lh`, la TRM, `WWWusage`, `treering`, `lynx` (cap. 3); `tcm`, las importaciones de Colombia de
  `global_economy`, `airmiles`, `gafa_stock`, `NelPlo`, `austres`, `pelt`, `BJsales` (cap. 4); `nottem`,
  `mdeaths`, `fdeaths` y el gas de `aus_production` (cap. 1). La lectura de práctica midió candidatas
  estacionales para cada módulo (`wineind`, `Seatbelts[, "kms"]` y `[, "PetrolPrice"]`, `souvenirs`,
  `aus_retail`, `us_gasoline`, `canadian_gas`, `aus_births`…); **la trampa del orden de las diferencias no
  aparece en ninguna de 420 series reales**: para ella hace falta una serie simulada.
- Cambiar el número de ejercicios mueve las cifras de la portada y del README (`cuenta_sitio.py`).
- **Fuentes sin texto en disco:** Box y Jenkins (1970, 1976) y la 5.ª ed. (el nombre del *airline* y su
  «Cap. 9»), la 4.ª de Shumway y Stoffer (la que se cita; la caché es la 3.ª), Brockwell y Davis (2016),
  Kwiatkowski et al. (1992), Ljung y Box (1978), Guerrero (1993), Wang et al. (2006) (la «fuerza estacional»
  de `nsdiffs`) y FPP2. **Sin alta en la biblioteca**, aunque las fuentes leídas las citan: Osborn, Chui,
  Smith y Birchenhall (OCSB), Canova y Hansen, Hylleberg et al. (HEGY), Taylor y Letham (Prophet), Holt y
  Winters, Brockwell y Davis (1991) (fuente de `?USAccDeaths`), la TRM de datos.gov.co y el software
  (`forecast`, `statsmodels`). **Sin obra identificable:** las competencias M4 y M5, el algoritmo de la
  fecha de Pascua y Box–Muller.

## 3. Decisiones propuestas

Cada una lleva mi recomendación; las decide Javier.

- **D1 · Las mismas cinco rondas, en el mismo orden:** R1 errores → R2 gráficas → R3 estructura →
  R4 fuentes → R5 práctica, cada una con `verifica_todo.py`, el verificador de bloques, revisión visual
  por HTTP, verificadores independientes sobre el diff, commit y tu visto bueno. *Recomendado: aquí, como
  en el 4, dos errores los vio una lente que no era la del par.*
- **D2 · La TRM, congelada como en los caps. 2 a 4:** los bloques leen la copia publicada. *Recomendado.*
- **D3 · La varianza deja de ser una regla para elegir $d$ y $D$**, alineada con los caps. 2 y 4: el M3
  muestra la tabla de las cuatro combinaciones por lo que hace cada operador (que es lo que ya explica bien)
  y no la atribuye al 4; el ciclo del M4 deja como herramientas `nsdiffs`, `ndiffs` sobre la serie ya
  diferenciada estacionalmente y la ACF, y como señal de vuelta $\hat\theta$ o $\hat\Theta$ pegados a $-1$;
  el M7 y la pista del E1, igual. *Recomendado. Ver §7, pregunta 1.*
- **D4 · El criterio de la raíz MA, con la escala correcta:** la firma de sobrediferenciar es $\hat\Theta$
  pegado a $-1$ (con su error estándar), no $\lvert\text{raíz}\rvert^{-1}$ cerca de 1, que en un SMA es
  $\lvert\Theta\rvert^{1/12}$; el umbral del simulador se dice o se cambia. *Recomendado.*
- **D5 · Lo que tiene arreglo en un componente, en el componente:** `.mapa-estacional` (contraste, señal de
  que hay más meses a la derecha, signo menos, filas para el lector de pantalla) se arregla en
  `ensamblado/componentes/` y se propaga al cap. 1 y a la plantilla en la misma ronda;
  `descripcionCorrelograma()`, el icono `fa-ranking-star`, los ejes del M9, `fmt()` sin signo menos y los
  marcos de alto fijo, en `cap5/chapter.js`. *Recomendado. Ver §7, pregunta 3.*
- **D6 · Orden sin renumerar:** ETS, el «naïve estacional» y el RMSE se presentan en una frase donde
  aparecen por primera vez; el *airline* ajustado se muestra antes de usarse en el M2; las cuatro remisiones
  rotas se arreglan (la del `biasadj`, nombrándolo en el 5 junto a la media lognormal del M7, que es donde
  el 6 lo busca); cada módulo cierra apuntando al siguiente; las intros de simulador dejan de describir un
  estado que no es el inicial.
- **D7 · El M11, ordenado:** la comparación de ocho métodos se muestra una vez, con un pie que no adelanta
  el resultado; su clímax (la partición frente a los 61 orígenes) gana un bloque de R y Python que lo
  reproduce, o la nota que lo promete se retira; el resumen es lo último antes de la evaluación. *Sin
  partir el módulo: partirlo renumera.*
- **D8 · Minutos medidos**, con los paneles abiertos, como en los caps. 2 a 4: el capítulo declara lo que
  mide.
- **D9 · Fuentes:** contrastar las 119 afirmaciones de prioridad alta y las de media con texto en caché,
  reutilizando las 70 ya registradas en los caps. 1 a 4; marcar, citar y registrar; pie generado y la
  sección 0 bajada a `ensambla_cap6.py`. La regla de 2 puntos, declarada convención como en el 4; el nombre
  y el año del *airline*, reescritos para decir solo lo que Cryer y FPP3 sostienen o `pendiente`; la tabla
  del M11 se reduce a lo que FPP3 respalda o se declara opinión del curso, sin atribuirla a M4 y M5; la
  historia de `nsdiffs`, comprobada en el NEWS de `forecast` o retirada; las lecturas, con localizadores
  leídos (TBATS fuera de §12.1). *Recomiendo, como en el 4, no cerrar la R4 con toda la media.*
- **D10 · Práctica:** un «Para practicar» corto en cada módulo del M1 al M10, sobre series nuevas (§2) y
  una simulada para la trampa del orden; el E2 y el E3 rehechos con otras series, y la solución del E3(b)
  con una serie en que la trampa del AICc entre distintos $D$ sí muerda (la lectura de práctica dio cuatro
  de `aus_retail`); el E1 con otra serie que no sea `co2`. Quiz: ítems del M5, M7, M8 y M10, longitudes
  igualadas, pistas que digan por dónde entrar, retros que no resuelvan ejercicios y otras series que
  AirPassengers. El Excel se anuncia donde se usa (M3 y M7), no solo al final del M11.
- **D11 · Python que se pueda reproducir:** los bloques de statsmodels comprueban la convergencia en vez de
  silenciar el aviso, y las explicaciones de las diferencias con R se corrigen (residuales de arranque en
  los dos; OPG frente a la hessiana en el M9).

## 4. Tareas

| # | Ronda | Tarea | Tam. | Depende |
|---|---|---|---|---|
| T1.1 | R1 | Los errores de §1 (M5 *airline* frente a la caminata, intro de $\Theta$, regla de la varianza D3, criterio de la raíz D4, E3(b), remisión de las manchas solares, «dos barras» del M1, salida de R escrita a mano del M7, lectura del M9 con Semana Santa sola), cada uno con su comprobación en R en `diagnostico/cap5/comprobaciones/`, editando `ensamblado/cap5/` | M | D3, D4 |
| T1.2 | R1 | Las imprecisiones y los menores del par; Python reproducible (D11); las cifras de la prosa sin generador, a `genera_cap5.R` o a un bloque | M | T1.1 |
| T1.3 | R1 | TRM congelada (D2); acentos de `cap5_sarima.json` desde el generador; el M12 en pasado; las diapositivas afectadas, si entran (§7, pregunta 2) | S | — |
| T2.1 | R2 | `.mapa-estacional` en el componente, propagado al cap. 1 y a la plantilla (D5) | M | R1 |
| T2.2 | R2 | `cap5/chapter.js`: `aria-label` con `descripcionCorrelograma()`, leyenda del M11, ejes del M9, icono, `fmt()`, marcos; capturas a 1200, 800 y 375 px | M | R1 |
| T3.1 | R3 | Orden (D6) sin renumerar y el M11 ordenado (D7) | M | R1 |
| T3.2 | R3 | El M2 sin repetir el satélite; notación (`n_t`/`n`, $\hat\rho_k$/$r_k$, bandas, «tres»/«cuatro» evidencias); minutos medidos (D8) | M | T3.1 |
| T4.1 | R4 | Biblioteca: altas de OCSB, Canova–Hansen, HEGY, Holt, Winters, Taylor–Letham, Brockwell–Davis (1991) y del software y los datos; texto de lo que consigas por acceso institucional (§7) | M | Javier |
| T4.2 | R4 | Contrastar, marcar, citar y registrar (D9); pie generado; sección 0 a `ensambla_cap6.py` | L | R3, T4.1 |
| T5.1 | R5 | Los «Para practicar» de M1–M10 (D10), con solución calculada en R bajo `#>` | L | R3 |
| T5.2 | R5 | Ejercicios 1, 2 y 3; quiz; aviso del Excel | M | R3 |

## 5. Criterios de aceptación

- [ ] Los errores de §1 tienen su comprobación en R y dejan de reproducirse; el cap. 5 no contradice al 2 ni
      al 4.
- [ ] `verifica_bloques_cap6.py --html` sobre el capítulo 5 da 0 discrepancias (hoy 1199/1212); los bloques
      de Python convergen y se comprueban aparte.
- [ ] ETS, el «naïve estacional», el RMSE y el *airline* ajustado se presentan donde se usan por primera vez;
      ninguna remisión rota; ninguna cifra de la prosa sin un bloque o un generador.
- [ ] Los lienzos y el mapa estacional se leen a 1200, 800 y 375 px; ninguna intro ni lectura que el dibujo
      contradiga; los `aria-label` de los correlogramas cambian con el estado.
- [ ] `audita_citas.py --cierre` en verde para lo registrado, con las afirmaciones de prioridad alta registradas.
- [ ] Cada módulo del M1 al M10 tiene al menos una práctica; la opción más larga no acierta más de 1 de 5;
      ninguna retro adelanta un ejercicio; ningún ejercicio se responde leyendo un módulo.
- [ ] La duración declarada de cada módulo dista menos de 3 min de la medida.
- [ ] `verifica_todo.py` en verde, el capítulo 5 reproducible byte a byte y el 6 idéntico salvo lo que la
      ronda quería; el cap. 1 y la plantilla, solo con el cambio del componente.

## 6. Riesgos

- **Editar el HTML final en vez de la fuente**: el siguiente reensamblado lo borra. Cada encargo lo dice
  y la comprobación de reproducibilidad lo atrapa.
- **El componente compartido**: un arreglo del mapa estacional que no se propague deja el cap. 1 y la
  plantilla con otro aspecto; `audita_proyecto.py` falla si la plantilla cambia sin reensamblar la guía.
- **Las diapositivas y el Excel**: si el capítulo se corrige y ellos no, el curso enseña dos cosas
  distintas. El Excel solo se verifica con Excel real.
- **Los instrumentos del banco** comparten página con lo que se corrige; una ronda que tocara
  `simulacro.js` cambiaría algo ya aplicado.
- **Sesiones concurrentes**: commits por archivo y fusión probada antes de cada publicación.

## 7. Preguntas abiertas

1. **La regla de la varianza (D3).** Los caps. 2 y 4 dicen que la varianza no decide $d$; el 5 la usa
   como regla «del Capítulo 4» en el M3, en el ciclo, en el M7, en el E1 y en dos diapositivas. ¿La retiro?
   *Recomiendo que sí, igual que en el 4.*
2. **Las diapositivas del cap. 5.** Repiten cuatro hallazgos (varianza, *airline* frente a la caminata,
   $\Theta \to 0$, manchas solares). ¿Entran en la R1 con su verificador o se anotan para después?
   *Recomiendo que entren: son cuatro cambios puntuales en un deck publicado, como hicimos con el del 4.*
3. **El mapa estacional (D5).** Arreglarlo en el componente cambia también el cap. 1 y la plantilla, ya
   cerrados. ¿Lo hago así, o lo arreglo solo en el 5? *Recomiendo el componente: un arreglo en una copia
   no llega a las otras.*
4. **El Excel.** ¿Lo dejo como está y lo anuncio donde se usa, o lo rehago para que pida decisiones (lo que
   obliga a regenerarlo y recalcularlo en Excel)? *Recomiendo anunciarlo y dejar el rediseño para después.*
5. **Los textos que solo consigues tú**, con el acceso institucional: Box y Jenkins (1970 o la 5.ª ed.),
   la 4.ª de Shumway y Stoffer, Wang et al. (2006) y Ljung y Box (1978). Sin ellos, el nombre del *airline*,
   el «caso birth» y la fuerza estacional de `nsdiffs` quedan `pendiente` o se reescriben.
6. **La subsección de momentos del M2**, que entró por [[PLAN_Varianza_SARIMA]] con tu visto bueno. ¿La
   conecto con el M5 (los $\sigma_h$ del *airline* la usan de hecho) o la pliego? *Recomiendo conectarla.*

## 8. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Fase 0: [[PLAN_Gestion_Documental]] · Fases 1–4: [[PLAN_Mejora_Cap1]] · [[PLAN_Mejora_Cap2]] · [[PLAN_Mejora_Cap3]] · [[PLAN_Mejora_Cap4]]
- Antes, sobre este capítulo: [[PLAN_Varianza_SARIMA]]
- Capítulo: [[20948-05 Modelos SARIMA]]
- Criterio: [[Criterio de contenido]] · [[Capa de fuentes]]
- Bitácora: [[2026-11-23]]
