---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-11-19
estado: CERRADO (2026-11-21) — R1–R5 publicadas · main c8683b5 · gh-pages 31136b3
---

# Plan — Mejora del capítulo 3 · Modelos AR, MA y ARMA (Fase 3)

**Objetivo:** dejar el capítulo 3 correcto, con un orden en que el ARMA, Ljung–Box y los criterios
de información no se usen antes de presentarse, con simuladores que muestren lo que la prosa dice,
con sus fuentes contrastadas y con práctica en cada módulo. Es la tercera aplicación del molde de
[[PLAN_Mejora_Cap1]] y [[PLAN_Mejora_Cap2]]: cinco rondas, un redactor por ronda, un verificador
independiente sobre el diff y la sesión maestra volviendo a medir en R.

**Estado: CERRADO por Javier el 2026-11-21.** Aprobado el 2026-11-19 (D1–D9, y las recomendaciones de §7.1 y §7.2);
R1 hecha el 20 y las cinco rondas publicadas el 21. Lo que sigue es el diagnóstico y el plan; las rondas se registran
en §4, y lo que la Fase 3 deja fuera está en §9.

## 1. El hueco — diagnóstico del 2026-11-19

Cinco lecturas independientes sobre `58bdfc5`, cada una con su lente y sin conocer las conclusiones de
las otras. El detalle, con línea y evidencia, está en `diagnostico/cap3/`.

| # | Lente | Qué se encontró | Detalle |
|---|---|---|---|
| C1 | Corrección | **28 hallazgos confirmados: 5 errores que enseñan algo falso**, 2 cifras incorrectas, 10 imprecisiones y 11 menores (más 2 dudosos). El convenio de signo del MA (el de R, con suma) es coherente en todo el capítulo. Las claves del quiz, de la actividad del Parcial 2 y del simulacro están bien. El verificador de bloques comprueba **534 cifras y 533 coinciden**: el capítulo ya muestra salidas bajo `#>` | `par_academico.md` |
| C2 | Fuentes | **254 afirmaciones exigen fuente**: 119 de prioridad alta, 112 media, 23 baja; 30 son atribuciones. El capítulo **no tiene ninguna cita marcada**. En la lectura del inventario, 10 discrepan de la fuente y 25 no se hallan en lo leído. Todo lo atribuido a Yule (el AR de 1927, «la ventana de Yule») descansa en una obra sin texto en disco. Nombra sin cita a Yule–Walker, Box–Jenkins, Ljung–Box, Box–Pierce, Hyndman–Khandakar, Durbin–Levinson, Shapiro–Wilk, ARCH/GARCH; usa los resultados de Akaike, Schwarz y Wold sin nombrarlos. El pie está escrito a mano | `fuentes.md`, `bibliografia/contraste/cap3_inventario.tsv` |
| C3 | Hilo | **El M1 empieza por los convenios de signo y R frente a Python** (406 palabras y 43 líneas de código antes de las raíces) y estima un ARMA(1,1) antes de que exista el modelo. **El M4 se apoya en el ARMA, que se define en el M5.** Ljung–Box, `fitdf`, AICc y BIC aparecen en el M5, unas 850 líneas antes del M8; `auto.arima` no se presenta nunca. La «elasticidad amplitud–nivel» que el M9 atribuye al capítulo 1 no está en el 1 ni en el 2. El M10 hace tres cosas (puente a las redes, cierre y evaluación) y su resumen no es lo último. **Los minutos no están medidos**: M1–M8 declaran 102 y miden 78; M9–M10 declaran 33 y miden 43. 44 fórmulas en bloque (el cap. 2 tiene 4) | `lector_estudiante.md` |
| C4 | Gráficas | **42 problemas: 5 graves**, 19 medios, 18 leves; 9 comparten causa. Los procesos explosivos salen planos en ±10⁶ y dejan los correlogramas vacíos (el calentamiento se come la explosión). El panel de Ljung–Box del M8 pone 0.0461 y la línea del 0.05 a 0.3 px. Dos frases del M9 que el dibujo contradice. El rezago 1 no se rotula a 800 ni a 375 px, y es donde vive la identificación. Ningún error de consola; el rezago 12 rotulado en los 16 correlogramas; las bandas, bien | `graficas.md`, `capturas/` |
| C5 | Práctica | **Ninguna clave mal.** Pero no hay ninguna práctica antes del M10 (unos 120 minutos sin pedir nada), y **el M6 y el M10 no tienen ninguna**. Eligiendo la opción más larga se aciertan **4 de 5** preguntas de una sola respuesta, y en la P5 las tres más largas son las tres correctas. Las 10 pistas dan el criterio; las dos múltiples dicen «Son tres» y las enumeran en orden. La retro de la P3 da la respuesta del ejercicio 2, que ya estaba resuelto tres veces antes. Cuatro de diez preguntas son sobre las manchas solares | `ejercicios.md` |

### Los errores, uno por uno (C1)

Los que comprobé yo mismo en R llevan ✔ (`diagnostico/cap3/comprobaciones/maestra_errores.R`); los
demás constan con su evidencia en el informe del par.

| Línea | Módulo | Qué dice | Qué es |
|---|---|---|---|
| 6163–6194 | E3 | Ljung–Box falla fuera de 1770–1869 porque con más datos la prueba gana potencia | Falla también con menos datos: 1900–1988 (n = 89) da p = 0.001 y 1889–1988 (n = 100, la misma n que la ventana de Yule) da p = 0.0006. Y «p < 0.001 en las tres» no vale para 1900–1988 (0.00102) ✔ |
| 4173–4176, 4221–4225, 4267–4269 | M5 | Aplicada a ρ₁, la recursión del AR daría 0.8 en el ARMA(2,1) | El 0.8 sale de tomar ρ₋₁ = 1; bien aplicada (ρ₋₁ = ρ₁) da 0.7584. La idea se sostiene —sigue sin dar 0.8614—, pero el código enseña el error que el ítem 10 de la actividad del Parcial 2 marca como incorrecto ✔ |
| 5371–5377, 5430; JS 8996, 9013 | M9 | El envolvente ±0.8278ʲ amortigua los ψ | El envolvente es ±Rʲ/sin ω, 1.882 veces mayor: 16 de las 25 barras se salen del dibujado ✔ |
| 5552–5554, 5873 | M9, M10 | El AICc no compara modelos con y sin media | Los dos se ajustan a los mismos datos; FPP3 §9.7 decide la constante con el AICc (el algoritmo de Hyndman–Khandakar, leído) y `auto.arima` hace esa comparación ✔ |
| 5842 | M10 | Con \|w\| < 1 el gradiente no explota ni se desvanece | Con \|w\| < 1 se desvanece |
| 5532–5536, 5550 | M9 | `auto.arima` elige un MA(1) para los rendimientos de la TRM, con θ̂ = 0.1262 | 0.1262 es el MA(1) con media; sin media da 0.1326. Y `auto.arima(ret)` con sus argumentos por defecto devuelve ruido blanco: el MA(1) sale de argumentos de `genera_cap3.R` que la página no muestra (se vuelve a medir en la R1) |
| 5212 | M9 | En la escala de la raíz «la PACF se corta más limpiamente en el rezago 2» | Al revés: en la cruda salen de la banda solo los rezagos 1 y 2; en la raíz, además el 6, el 9 y el 16 (0.200, 0.198, −0.199 frente a ±0.196) ✔ |

Además, comprobado por mí:
- **El periodo del AR(2).** El capítulo usa el argumento de la raíz, 2π/arccos(φ₁/(2√−φ₂)), y da
  11.22 años. FPP3 §9.5 da otra fórmula para el periodo medio de los ciclos, que para el mismo modelo
  da 11.84. Son nociones distintas y el capítulo no lo dice ✔.
- **La discrepancia de residuales entre R y statsmodels** (l. 4998–5009) no es de inicialización:
  R devuelve el primer residual dividido entre √(γ₀/σ²) (52.54/√6.226 = 21.06) y statsmodels lo
  devuelve crudo ✔.
- **`arima.sim(list(order = c(0, 1, 0)))` sí simula una caminata aleatoria**, contra el comentario
  de la l. 4466 que exige `cumsum` ✔.

Imprecisiones de más peso: la causalidad (para |φ| > 1 sí hay solución estacionaria, no causal: el
«si y solo si» del triángulo vale para la causal); «la transformación es monótona» al volver de la
raíz, con límites inferiores negativos en h = 7 y 8; ML «no lo hace en ninguna» lo impone
`transform.pars`, y el 4 % del CSS no lo calcula ningún guion; `AutoReg` sí reproduce el CSS en
Python; el título «Donde sí hay estructura: en el cuadrado» contradice su texto (p = 0.9166); los
intervalos de las elasticidades no contienen los dos valores; «|B| = 1, es decir φ = 1» olvida
φ = −1; la TRM mensual es un promedio de diarios, y promediar una caminata induce ρ₁ ≈ 0.25, cosa
que el capítulo no dice al concluir «ruido blanco».

## 2. Restricciones verificadas antes de planear

- **El capítulo 3 se ensambla.** `ensambla_cap3.py` parte del HTML del 2 y pone los módulos de
  `ensamblado/cap3/cap3_modulos.html` y el JS de `cap3_js.js`. **Se edita la fuente, nunca el HTML
  final**, o el siguiente reensamblado lo borra. El capítulo 4 se construye a partir del 3
  sustituyendo sus regiones: lo que vive solo en `cap3_js.js` (`simularARMA`, `correlogramaDoble`,
  los gráficos de dispersión) **no baja** al 4; lo que vive en el armazón del 2 (`marcasLegibles`,
  `actualizarLectura`) baja a 3, 4, 5 y 6. Cada ronda comprueba que los caps. 4–6 siguen idénticos o
  cambian solo donde se quería.
- **La sección «1b» de `ensambla_cap3.py`** conserva hoy el pie propio del cap. 3 y retira las
  citas del 2; se borra cuando este capítulo haga su R4.
- **Las salidas `#>` ya están**: el verificador de bloques comprueba 534 cifras (falla una, por
  redondeo de R 4.6). No hace falta la D2 del cap. 2. El verificador no lee Python: los 11 bloques
  de Python se comprueban a mano (`diag/ejercicios_*`).
- **La TRM es la misma serie que la del cap. 2** (138 meses, enero de 2015 a junio de 2026, en
  `precalculo/salidas/datos_series.json` y en `Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv`),
  pero los bloques de la página la descargan en vivo.
- **El M10 y el M11 llevan dos instrumentos de un banco que vive fuera del repo**: la «actividad
  preparatoria del Parcial 2» (variante 1 del quiz adicional, `AUTOEVALUACIONES['parcial2']`) y el
  simulacro del M11 (variante 9). Se generan desde el banco; cambiarlos es decisión de Javier y se
  hace allí. El Parcial 2 se aplicó el 14 de octubre.
- **El Corte II ya se evaluó**: corregir no cambia nada que esté en evaluación. Lo que se arregle
  llega a 2027-I.
- **Series ya usadas en la práctica del cap. 2** (no repetirlas): `EuStockMarkets` (DAX),
  `discoveries`, `LakeHuron`, `nhtemp`, `JohnsonJohnson`, `UKDriverDeaths`, `co2`, `USAccDeaths`,
  `UKgas`. El cap. 3 ya usa `sunspot.year`, `lh` y la TRM.
- Cambiar el número de ejercicios mueve las cifras de la portada y del README (`cuenta_sitio.py`).
- **Fuentes sin texto en disco:** Yule (1927), Box, Jenkins, Reinsel y Ljung (5.ª ed.), Ljung y
  Box (1978), la 4.ª de Shumway y Stoffer (la caché es la 3.ª), Brockwell y Davis, Hyndman y
  Khandakar (2008). Lo que dependa de ellas queda `pendiente` hasta que Javier las consiga.

## 3. Decisiones propuestas

Cada una lleva mi recomendación; las decide Javier.

- **D1 · Las mismas cinco rondas, en el mismo orden:** R1 errores → R2 gráficas → R3 estructura →
  R4 fuentes → R5 práctica. Cada ronda termina con `verifica_todo.py`, el verificador de bloques,
  revisión visual por HTTP, un verificador independiente sobre el diff, commit y tu visto bueno.
  *Recomendado: en los caps. 1 y 2 el verificador encontró problemas en lo «terminado» en todas las
  rondas.*
- **D2 · La TRM, congelada como en el cap. 2:** los bloques leen la copia publicada
  `datos/trm_mensual_2015-01_2026-06.csv`, la misma que usan `genera_cap2.R` y `genera_cap3.R`; la
  descarga en vivo queda solo donde el ejercicio lo pide. *Recomendado.*
- **D3 · Lo que tiene arreglo en el armazón, a toda la cadena:** rotular siempre el rezago 1 en
  `marcasLegibles`, el signo menos en `actualizarLectura` y las `aria-label` que cambian con el
  estado se arreglan en el cap. 2 y se reensamblan el 3, el 4, el 5 y el 6 en la misma ronda, como
  en la R2 del cap. 2. Lo que vive solo en `cap3_js.js` se arregla allí. *Recomendado.*
- **D4 · Orden sin renumerar módulos** (el cap. 4, el banco y el simulacro citan «3.N»):
  - el M1 empieza por las raíces, y los convenios de signo y las diferencias entre R y Python pasan
    a una nota al final del módulo;
  - el M4 presenta el ARMA como adelanto del M5 en una frase, o su ejemplo pasa a no necesitarlo;
  - Ljung–Box, AICc y BIC se anuncian como adelanto del M8 donde aparecen en el M5;
  - `auto.arima` se presenta en su primera aparición;
  - lo que los plegados guardan y el texto cita después sale del plegado o deja de citarse.
- **D5 · Una sola noción de periodo:** el capítulo conserva el argumento de la raíz y avisa, en una
  frase con su cifra de R, de que FPP3 da otra fórmula (el periodo medio) y por qué no coinciden.
- **D6 · El M10, en tres partes ordenadas:** el puente a las redes y el material nuevo (PACF(p) =
  φ_p, el aviso del ARMA(2,2)) antes del resumen; el resumen, último antes de la evaluación; un solo
  nombre para el módulo. *La actividad del Parcial 2 y el simulacro: ver §7.*
- **D7 · Minutos medidos**, con los paneles abiertos, como en el cap. 2; el capítulo declara lo que
  mide.
- **D8 · Fuentes:** contrastar las 119 afirmaciones de prioridad alta y las de media que tengan
  texto en caché; marcar, citar y registrar; generar el pie con `genera_referencias.py` y retirar la
  sección «1b» de `ensambla_cap3.py`. Lo que depende de Yule (1927), Box–Jenkins, Ljung y Box (1978)
  o la 4.ª de Shumway y Stoffer queda `pendiente` o se reescribe para no necesitarlas. *Recomiendo
  no dar por cerrada la R4 con la media entera: en el cap. 2 se registraron 80 de 127.*
- **D9 · Práctica:** un «Para practicar» corto en cada módulo del M1 al M9 que no tenga práctica
  propia (M1, M2, M3, M4, M5, M6, M7 y M9; el M8 la tiene en los ejercicios 1 y 3), sobre series
  distintas de las del módulo y de las del cap. 2; rehacer el ejercicio 2 (otro MA(2)) y la
  discusión del 3; la pista del 1 sin el resultado; quiz: rehacer P2, P4, P5 y P7, la retro de la P3
  sin el ejercicio 2, longitudes igualadas, pistas que digan por dónde entrar y retro por opción en
  las dos múltiples. *Son ocho ejercicios: uno más que en el cap. 2, porque aquí la falta empieza en
  el M1.*

## 4. Tareas

| # | Ronda | Tarea | Tam. | Depende |
|---|---|---|---|---|
| T1.1 | R1 | Los errores de C1, cada uno con su comprobación en R en `diagnostico/cap3/comprobaciones/`, editando `ensamblado/cap3/` | M | — |
| T1.2 | R1 | Las imprecisiones y menores del par, una por una (causalidad, residuales R/statsmodels, ML y `transform.pars`, el 4 % del CSS con su guion, `AutoReg`, elasticidades, «|B| = 1», TRM promediada, `arima.sim`) | M | T1.1 |
| T1.3 | R1 | TRM congelada (D2); el bloque que falla en el verificador y los comentarios de Python con la salida real | S | — |
| T1.4 | R1 | El periodo de FPP3 (D5) | S | T1.1 |
| T2.1 | R2 | Armazón (D3): rezago 1 siempre rotulado, signo menos en las lecturas, `aria-label` que cambian con el estado y no regalan el quiz; reensamblar 3–6 | M | R1 |
| T2.2 | R2 | `cap3_js.js`: `simularARMA` sin aplanar lo explosivo; ACF teórica oculta cuando no existe; ejes de los dos gráficos de dispersión; color de la muestral; panel de Ljung–Box en una escala donde se vea el 0.05; envolvente de los ψ | M | R1 |
| T2.3 | R2 | Alturas de los lienzos bajo 640 px y leyendas compactas; capturas a 1200, 800 y 375 px | S | T2.2 |
| T3.1 | R3 | Orden (D4) sin renumerar | M | R1 |
| T3.2 | R3 | El M9: la «elasticidad del cap. 1» presentada o retirada, cifras sin código con su código, `auto.arima` presentado | M | R1 |
| T3.3 | R3 | El M10 en tres partes (D6); notación (`T`/`n`, «identificado», «abanico», «caminata»); minutos medidos (D7) | M | T3.1 |
| T4.1 | R4 | Biblioteca: altas por DOI de lo que exija el contraste; texto de Yule (1927), Ljung y Box (1978), Box–Jenkins 5.ª y Shumway 4.ª | M | Javier, para el acceso institucional |
| T4.2 | R4 | Contrastar alta y la media con texto (D8), marcar, citar y registrar; pie generado; quitar la «1b» de `ensambla_cap3.py`; lecturas del M10 con localizadores leídos | L | R3, T4.1 |
| T5.1 | R5 | Ocho ejercicios cortos (D9), con solución calculada en R bajo `#>` | L | R3 |
| T5.2 | R5 | Ejercicios 1, 2 y 3; quiz: P2, P4, P5, P7, la retro de la P3, longitudes, pistas y retro por opción | M | R3 |

### Registro de rondas

- **R1 · errores — hecha el 2026-11-20 y PUBLICADA el 21** (`main` `5d67632` · gh-pages `8bfaebe`). Los 7 errores de C1 y las imprecisiones y menores
  del par, cada uno con su comprobación en R (`diagnostico/cap3/R1_cambios.md`). El ejercicio 3 ya no
  culpa a la potencia: de 190 ventanas de cien años, el AR(2) falla en 138, también en 49 anteriores a 1900
  y en todas las que llegan al siglo XX. La envolvente de los ψ pasa a ±Rʲ/sin ω (ninguna barra fuera, antes
  16). El AICc compara con y sin media; la TRM, congelada en la copia de 138 meses (D2), con
  `auto.arima` que por defecto da ruido blanco y el MA(1) solo con `stepwise = FALSE`; aviso de la TRM
  promediada (ρ₁ ≈ 0.25 inducido). Nota del periodo con las dos fórmulas (D5). Bloques: 533/534 →
  557/557. Caps. 4–6 idénticos. El verificador independiente halló 8 puntos; corregidos 6, dos menores
  anotados (`diagnostico/cap3/R1_verificacion.md`).

- **R2 · gráficas — hecha y PUBLICADA el 2026-11-21** (`main` `495254f` · gh-pages `56e1007`). En el armazón (cap. 2 → 3–6, D3): el rezago 1 rotulado
  en todos los correlogramas a 800 y 375 px sin que ningún eje pierda rótulos ni el 12, el 24 o el 36 (prueba
  sintética de 3850 ejes), y el signo menos en las lecturas; los caps. 4–6 reciben el mismo diff, solo del
  armazón. En el cap. 3: los procesos explosivos se ven despegar, la ACF teórica se oculta cuando no existe,
  ejes de los gráficos de dispersión con ±2, ±1 y ±0.5, la muestral en gris (3.04:1), el panel de Ljung–Box del
  M8 en un eje de 0 a 0.10 donde 0.0461 queda bajo la línea, el M6 con un rombo en lo que se asoma, los π del M4
  en eje logarítmico con signo, alturas de 98–149 px en estrecho, y `aria-label` que cambian con el estado. De
  los 42 problemas del diagnóstico: 30 arreglados, 5 en parte, 2 en la R1, 5 leves sin tocar
  (`diagnostico/cap3/R2_cambios.md`). El verificador independiente halló 9 puntos, entre ellos un error nuevo
  (la PACF del ARMA(1,1) «nula» por redondeo) y una regresión del eje en el cap. 5; corregidos 6, tres leves
  anotados (`diagnostico/cap3/R2_verificacion.md`).

- **R3 · estructura — hecha y PUBLICADA el 2026-11-21** (`main` `3cf564c` · gh-pages `739a297`). Sin renumerar: el M1 empieza por las raíces y los
  convenios de signo y R/Python pasan a su final; el M4 presenta el ARMA y saca la recursión de ψ y π del plegado;
  el M5 en el orden tabla → laboratorio → ciclo, con AICc, BIC, Ljung–Box y `fitdf` anunciados; `auto.arima`
  presentado en el M9; lo que citaban los «paso 6» y «paso 4» de los plegados, a la vista. El M9 presenta la
  elasticidad amplitud–nivel (no se retira: es su pivote) y cada cifra sin código recibe su bloque con `#>`. El M10
  en tres partes con un solo nombre, «Cierre: redes, resumen y evaluación» (también en la lista de
  `preparcial-corte-2.html`); la actividad, «Práctica de repaso · capítulo 2 y módulos 3.1–3.4», sin tocar sus
  preguntas. Notación: `T`, «identificable»/«identificación», «abanico», «caminata», «pseudo-periodo». Minutos
  medidos con la herramienta corregida (contaba de menos en cuatro módulos): 10, 14, 15, 13, 18, 7, 9, 11, 31, 22 y
  30; todos a < 0.5 min. Bloques: 557/557 → 732/732. Caps. 2 y 4–6 sin cambios (`diagnostico/cap3/R3_cambios.md`).
  El verificador independiente no halló nada falso ni regresiones; 7 puntos menores, 5 corregidos por la maestra,
  uno resuelto con el commit y uno a la R5 (`diagnostico/cap3/R3_verificacion.md`).

- **R4 · fuentes — hecha y PUBLICADA el 2026-11-21 (`main` `6447212` · gh-pages `9c060fe`).** El capítulo pasa de 0 a **213 afirmaciones marcadas y
  registradas** (`bibliografia/contraste/cap3.yml`): 119 `respaldada`, 53 `con-matiz`, 37 `propia` (lo que se dice del
  software, comprobado ejecutando) y 4 `pendiente` (Guerrero 1993, Shumway 4.ª y una obra de aprendizaje profundo para
  RNN/LSTM y transformers). **213 citas visibles**: Cryer y Chan 98, FPP3 62, Hamilton 25, ayuda de R 22, Yule 4 y
  Hyndman y Khandakar 2; 353 citas literales comprobadas contra la caché, ninguna en git. Con permiso de Javier entraron
  los PDF de acceso abierto de **Yule (1927)** (Royal Society, OCR) y **Hyndman y Khandakar (2008)** (JSS): la lectura de
  Yule deshizo «la ventana centenaria de Yule» (usó 1749–1924, p. 275; el AR(2) es su ec. 31, p. 281), también en
  `genera_cap3.R` y en tres cadenas de `cap3_js.js` (pie de la tabla ordenable y rótulos «número de Wolf»); y el título
  de Yule, sin «in» en Crossref, va corregido por `enmiendas.yml`. Prosa: 64 cambios en la primera pasada, todos por lo
  que la fuente decía, y 16 en la segunda, entre ellos el error de c3-m6-07 (un pico grande fuera de la banda SÍ es
  evidencia, FPP3 §2.9), la notación de Ljung–Box (Q(h) = Ljung–Box, como el cap. 4; Q_BP(h) = Box–Pierce),
  `auto.arima` (el artículo usa AIC; el paquete, AICc por defecto) y la voz impersonal en ocho afirmaciones. La sección
  «1b» de `ensambla_cap3.py` sale: el pie y las listas los escribe `genera_referencias.py` al ensamblar; la protección
  pasa a `ensambla_cap4.py` y los caps. 4–6 quedan byte a byte iguales. Inventario: 179 de las 254 filas registradas
  (93 de alta), 68 sin marcar con su motivo (13 viven en cadenas del quiz, la práctica de repaso o el simulacro), 7
  salen; **la media no queda cerrada entera** (32 sin marcar). Dos verificadores independientes en paralelo (M1–M6,
  M7–M10) firmaron 203 en la primera lectura y las 20 restantes tras la corrección (`diagnostico/cap3/R4_cambios.md`,
  `R4_verificacion_A.md`, `R4_verificacion_B.md`). Bloques: 732/732 → 733/733.

- **R5 · práctica — hecha y PUBLICADA el 2026-11-21 (`main` `c8683b5` · gh-pages `31136b3`).** Ocho «Para practicar» al final de M1–M7 y M9 (D9), sobre
  procesos teóricos o simulados con semilla y tres series nuevas en el sitio para la práctica (`diff(WWWusage)`, `treering`
  1880–1979 y `lynx`), cada uno con solución en R bajo `#>`. Ejercicio 1 con pista sin resultado; el 2 con otro MA(2),
  θ = (0.9, 0.2), y un apartado de raíz invertida; el 3 al día con la R1. Quiz: P2, P4, P5 y P7 rehechas, retro por opción
  en las dos múltiples, diez pistas nuevas, las tres cadenas de la R4 y las de la R3 corregidas; la opción más larga
  acierta 0 de 5 (antes 4). Minutos declarados a ≤ 0.5 de lo medido; el sitio pasa de 32 a 40 ejercicios. Una afirmación
  nueva, **c3-m6-09** (la banda del MA(1), Cryer y Chan, p. 111), redactada por la maestra y firmada por el verificador:
  214 afirmaciones, 214 firmadas. Bloques: 733/733 → 1084/1084. El verificador independiente halló 13 puntos —uno que
  chocaba con el módulo (la práctica del M7 comparaba las σ̂² de Yule–Walker y ML) y la P4, que repetía una cifra resuelta
  en la práctica del M4—; corregidos 10, uno queda para Javier (el quiz sin ítem del M6 ni del M9) y dos sin cambio
  (`diagnostico/cap3/R5_cambios.md`, `R5_verificacion.md`). Ninguna frase marcada cambia de texto; `parcial2` y el
  simulacro, intactos; caps. 4–6 idénticos.

## 5. Criterios de aceptación

- [x] Cada uno de los errores de C1 tiene su comprobación en R y deja de reproducirse
      (`diagnostico/cap3/comprobaciones/maestra_errores.R` y `r1_*`; R1).
- [x] `verifica_bloques_cap6.py --html` sobre el capítulo 3 da 0 discrepancias: de 533/534 antes de la R1 a
      1084/1084 al cerrar la R5. Los 11 bloques de Python se comprobaron a mano en la R1 (`r1_bloques_python.out`);
      el verificador no los lee.
- [x] El ARMA, Ljung–Box, el AICc, el BIC y `auto.arima` se presentan o se anuncian donde se usan por primera
      vez: R3, revisado por su verificador. Nadie ha releído el capítulo entero después de la R4 y la R5.
- [x] Los lienzos se leen a 1200, 800 y 375 px; el rezago 1 rotulado en todos los correlogramas; ningún proceso
      explosivo sale plano; las frases que el dibujo contradecía, corregidas (R2). De los 42 problemas de C4 quedan
      5 leves sin tocar y 5 arreglados en parte.
- [ ] `audita_citas.py --cierre` en verde para lo registrado, con las afirmaciones de prioridad alta registradas.
      **Falla**: quedan 4 `pendiente` (Guerrero 1993, la 4.ª de Shumway y Stoffer y dos de una obra de aprendizaje
      profundo que la biblioteca no tiene). De las 119 filas de alta del inventario, 93 quedan registradas y 23 sin
      marcar con su motivo (13 viven en cadenas de JavaScript del quiz, la práctica de repaso o el simulacro); de
      la media, 32 siguen sin marcar.
- [x] Cada módulo del M1 al M9 tiene al menos una práctica dentro del capítulo (ocho «Para practicar» y los
      ejercicios 1 y 3 para el M8); la opción más larga acierta 0 de 5 preguntas (antes, 4); ninguna retro adelanta
      un ejercicio, tras la corrección del verificador de la R5.
- [x] La duración declarada de cada módulo dista menos de 3 min de la medida: como mucho 0.5 min, con los paneles
      abiertos (`r5_minutos_despues.out`).
- [x] `verifica_todo.py` en verde (11 verificadores), el capítulo 3 reproducible byte a byte y los 4–6 idénticos
      en todas las rondas salvo el diff del armazón que la R2 quería.

## 6. Riesgos

- **Editar el HTML final en vez de la fuente**: el siguiente reensamblado lo borra en silencio. El
  encargo de cada ronda lo dice, y la comprobación de reproducibilidad lo atrapa.
- **El tamaño**: 9950 líneas, 254 afirmaciones y 44 fórmulas en bloque. La R4 es la más larga del
  proyecto hasta ahora y puede necesitar dos verificadores en paralelo, uno por obra.
- **Los instrumentos del banco** (actividad del Parcial 2 y simulacro) comparten página con lo que
  se corrige; una ronda que los tocara por error cambiaría algo ya aplicado.
- **Sesiones concurrentes**: commits por archivo y fusión probada antes de cada publicación.

## 7. Preguntas abiertas

Resueltas el 2026-11-19: Javier aprobó D1–D9 y las recomendaciones de las preguntas 1 y 2 (la
actividad se queda con otro título, sin tocar el banco; el simulacro se anota para revisarlo en el
banco, fuera de esta fase). La 3 sigue abierta.

1. **La actividad preparatoria del Parcial 2** (final del M10). El Parcial 2 ya se aplicó. ¿Se
   queda con otro título, como práctica de repaso de los caps. 2 y 3.1–3.4, o se retira del
   capítulo? *Recomiendo quedarla con otro título: sus diez preguntas están bien, tienen retro por
   opción y la más larga no acierta ninguna. Solo cambiaría el encabezado, sin tocar el banco.*
2. **El simulacro del M11.** La correcta recorre las posiciones en ciclo (1 2 3 4 1 2 3 4 1), el
   auditor no lo ve porque el simulacro no lleva clave, y su P10 usa φ = (0.5, 0.3), el ejemplo
   resuelto del M2. Si el banco asigna la posición así en todas las variantes, el patrón llega a
   Brightspace. ¿Lo revisas en el banco, o lo dejo anotado fuera de esta fase?
3. **Los textos que solo consigues tú**, con el acceso institucional: Yule (1927), Ljung y Box
   (1978), los capítulos 3 y 6 de Box, Jenkins, Reinsel y Ljung (5.ª ed.) y el capítulo 3 de la 4.ª
   de Shumway y Stoffer (que también cierra 8 pendientes del cap. 2).

## 9. Cierre (2026-11-21)

Javier cerró la Fase 3 con las cinco rondas publicadas, y aceptó que el quiz quede sin ítem del M6 ni del M9
(los dos se practican en sus «Para practicar»). De los ocho criterios de §5 se cumplen siete; el de las fuentes no,
y queda con lo demás **fuera de esta fase**, sin plan:

- **Las 4 afirmaciones `pendiente`** y la pregunta 3 de §7: hacen falta Guerrero (1993), la 4.ª de Shumway y
  Stoffer (que también cierra pendientes del cap. 2) y una obra de aprendizaje profundo dada de alta por DOI o
  ISBN. Ljung y Box (1978) y Box–Jenkins siguen sin texto; las frases que dependían de ellos se reescribieron para
  no necesitarlos.
- **El inventario sin cerrar:** 23 filas de alta y 32 de media sin marcar, cada una con su motivo en
  `bibliografia/contraste/cap3_inventario.tsv`.
- **Una relectura completa del capítulo ya corregido** por un par que no haya visto ninguna ronda.
- **Lo que anotaron las rondas sin resolver:**
  - las fichas de las lecturas del M10 (`box2016time`, `shumway2017time`) siguen tecleadas: generarlas pide un modo
    «ficha de lectura» en `genera_referencias.py` y su regla en el auditor;
  - los localizadores de la ayuda de R («§Details») no dicen de qué función son, y la sección «Fitting methods» de
    `?arima` no se puede citar con `SECCIONES_R`;
  - «Apliquemos», en primera persona, en el M7; `n` en el enunciado del ejercicio 3, dentro de la frase marcada
    c3-m10-35;
  - la P5 del quiz repite el experimento de la práctica del M3 con otro número: discrimina poco;
  - de la R2, 5 problemas leves sin tocar y 5 arreglados en parte (`diagnostico/cap3/R2_cambios.md`).
- **Lo que no es del capítulo, sino del sistema o de otra página:**
  - El motor del quiz, que tras el primer fallo de la múltiple dice cuántas correctas faltan y que llama
    «impecable» a un 10 de 10 logrado al segundo intento.
  - El simulacro del M11 (pregunta 2 de §7): revisar en el banco la posición de la correcta.
  - Las `aria-label` de los caps. 4–6 y el `descripcionGrafico` del quiz del cap. 4, que la R2 dejó para ellos.
  - `taller-2-modulo-2.html` dice «antepasado directo».
  - Una copia de `bibliografia/_local/` fuera de este equipo.

En la fase, el capítulo pasó de 135 a 196 minutos declarados (medidos con todo abierto), de 3 a 11 ejercicios y de 0
a 214 afirmaciones registradas y firmadas, con 214 citas visibles; y el verificador de bloques, de 533/534 a
1084/1084. Entraron dos obras de acceso abierto: Yule (1927), cuya lectura deshizo «la ventana centenaria de
Yule», y Hyndman y Khandakar (2008). El molde se mantuvo: un solo redactor por ronda, un verificador independiente
de contexto limpio sobre el diff (dos en paralelo en la R4) y la sesión maestra volviendo a medir en R. El
verificador encontró problemas en lo «terminado» en todas las rondas: 8 en la R1, 9 en la R2, 7 en la R3, 20
entradas devueltas en la R4 y 13 en la R5, nunca una clave del quiz mal puesta. Y la maestra también corrigió al
verificador: en la R5, una de sus propuestas ponía el aviso de convergencia de `lynx` en la escala equivocada.

## 8. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Fase 0: [[PLAN_Gestion_Documental]] · Fase 1: [[PLAN_Mejora_Cap1]] · Fase 2: [[PLAN_Mejora_Cap2]]
- Capítulo: [[20948-03 Modelos AR, MA y ARMA]]
- Criterio: [[Criterio de contenido]] · [[Capa de fuentes]]
- Bitácora: [[2026-11-19]]
