# Capítulo 4 · R5 · verificación independiente A (los «Para practicar» c4m1–c4m9 y la prosa del M8 y del M9)

Fecha: 2026-11-23. Verificador A, sin haber redactado nada. Base `b53fdcb` + el diff sin commit de la R5.
No se editó el capítulo ni sus fuentes.

**Veredicto: aceptable con correcciones.** Los nueve bloques corren solos y reproducen su `#>` (9/9), todas las
cifras de enunciado y lectura coinciden con R, nada enseña algo falso de fondo; hay **un error leve** (M6: el
ARIMA(0,2,1) no es la caminata aleatoria sino la caminata *con deriva*), **una frase falsa sobre la semilla**
(M3: «La semilla no es especial»), **una simulación sin frecuencia** (M2) y tres problemas de pedagogía en el
encaje M8/M9 ↔ E2/E3 (la prosa nueva del M9 todavía adelanta el E3; la práctica del M9 duplica el E3).

## Cómo se comprobó

| Qué | Resultado | Salida (`diagnostico/cap4/comprobaciones/`) |
|---|---|---|
| Cada bloque c4m1–c4m9 extraído de `ensamblado/`, ejecutado en un `Rscript --vanilla` nuevo, carpeta vacía, proxies a `127.0.0.1:9` (sin red), comparado línea a línea con lo que hay bajo `#>` | **9/9 idénticos**; stderr solo el aviso de `quantmod` al cargar `tseries` (M1, M7) | `v5A_bloques.py`, `v5A_bloques.out`, `v5A_bloques/m*.R/.out` |
| Resolución propia (otro código: `forecast::Arima`, `ARMAacf`, `ARMAtoMA`, trazas completas) de cada cifra de enunciado, pista y lectura; páginas de ayuda leídas con `tools::Rd2txt` | todas coinciden salvo lo de la tabla | `v5A_cifras.R`, `v5A_cifras.out` |
| Frecuencia de lo que muestran las semillas (M2: 200; M3: 500; M8: 200, y con φ = 0.6) | ver hallazgos 2 y 3 | `v5A_semillas.R`, `v5A_semillas.out` |
| Por HTTP (servidor 8771, Chrome sin ventana CDP 9281), 1200 y 375 px, pulsando Pista y Solución | los 9 paneles abren; 0 errores de KaTeX, 0 «$» sueltos, 0 KaTeX en `<pre>`, página = ventana, Prism activo, consola limpia. El «se salen 5» del M9 es un falso positivo de mi medida (nodos `.katex-mathml` ocultos); la captura lo confirma | `v5A_revisa.js`, `v5A_revisa.out`; capturas en `diagnostico/cap4/capturas/r5/v5A/` |
| `data-afirma` de las tres plantillas antes y después | mismo conjunto (md5 idéntico); en el M8 el `<span data-afirma="c4-m8-61">` cierra antes del paréntesis cambiado | — |
| Series: lista de prohibidas, repetición en el sitio | ninguna prohibida tal cual; ninguna repetida fuera de su módulo (ver hallazgo 8 sobre `BJsales.lead` y `global_economy`) | `grep` sobre `Htmls_Series/*.html` y `chapter.js` |

Servidor y Chrome cerrados (`lsof -i :8771 -i :9281` vacío).

## Hallazgos

| # | Dónde | Qué dice | Qué es | Evidencia | Gravedad |
|---|---|---|---|---|---|
| 1 | `templates_4_6.html` 722 (Respuesta del c4m6) y 762 (lectura (c)) | «el modelo que lo alcanza es la caminata aleatoria de $d = 1$ con una diferencia de más»; «el ARIMA($0,2,1$) es el ARIMA($0,1,0$) con una diferencia de más y un MA que la deshace» | Con $\theta = -1$, $\nabla^2 y_t = (1-B)\varepsilon_t$ da $\nabla y_t = c + \varepsilon_t$: una caminata **con deriva**, con la constante absorbida por la diferencia sobrante. La propia evidencia que se cita lo muestra: $\hat\sigma^2 = 372.71$ es la varianza *centrada* de $\nabla y$, que es la del ARIMA(0,1,0) **con deriva** (372.711); la del ARIMA(0,1,0) sin constante es 371.229 | `v5A_cifras.out`, M6: `s2_010 371.229 · s2_010_drift 372.711 · s2_021 372.707 · var_diff 372.706`; deriva $-0.118$, $t = -0.10$ | **error** (leve) |
| 2 | `templates_1_3.html` 1093 (cierre del c4m3), con 1090 | «La semilla no es especial. En 500 series… KPSS pide diferenciar la serie completa en todas; en el 65 %, además, pide $d = 0$ en los dos tramos…» | Las dos cifras son ciertas, pero la semilla 43 **sí** es especial y el informe del redactor lo dice (duda 2: «se eligió porque reproduce el reparto del Nilo»). Lo que la solución enseña en (a) —KPSS 1, ADF y PP 0, «el mismo reparto que en el Nilo»— sale en el 51.8 % de las semillas; eso más las tres pruebas en 0 en los dos tramos (lo que dice (b)), en el 33.4 % | `v5A_semillas.out`: `reparto 1/0/0: 0.518 · …y las tres 0 en los dos tramos: 0.334`; `v5A_cifras.out`: `kpss_0_en_tramos 0.646`, mediana 1.154 | **cifra** (afirmación falsa sobre la semilla) |
| 3 | `templates_1_3.html` 582–641 (c4m2) | Simulación con `set.seed(2026)`; ninguna frase dice con qué frecuencia salen los hallazgos | La semilla muestra los cinco rasgos que la lectura usa (LB rechaza el (0,1,1); raíz MA del (2,2,1) en 1; ee del (2,1,2) inflados; PACF que corta en 2; el (2,2,1) y el (2,1,2) pasan LB). Por separado: 99.5 %, 65.5 %, 93.4 %, 81.5 %, 89.5 %; **los cinco a la vez, 53.0 %** de 200 semillas | `v5A_semillas.out`, línea M2 | **pedagogía** |
| 4 | `templates_7_9.html` 758–759 (prosa nueva del M9) | «Cuando $\phi+\theta>0$, $\psi_\infty$ es mayor que 1 y cada choque acaba pesando más que cuando llegó: **el ejercicio 3 lo mide sobre otra serie**.» | La regla es correcta ($\psi_\infty = (1+\theta)/(1-\phi) > 1 \iff \phi+\theta>0$ con $\phi<1$). Pero al decir que el E3 «lo mide», le dice al estudiante que en el E3 $\psi_\infty>1$, que es la respuesta de E3(a) («¿qué anticipa sobre el intervalo, comparado con el del Nilo?»). Ya no da la cifra 2.99, pero sigue adelantando la conclusión | lectura | **pedagogía** |
| 5 | `templates_7_9.html` 946–1003 (c4m9) | ARIMA(0,1,1) de `BJsales.lead`: (a) $\psi_j$ por la forma cerrada y semianchos frente a `forecast()`; (b) $\sigma_{12}$ frente a la caminata y su límite; (c) con y sin deriva | Las cifras son todas correctas (`v5A_cifras.out`, M9). Pero (a), (b) y (c) son, uno a uno, el E3(a)–(d) (ψ∞ por la forma cerrada, intervalo desde los ψ frente a `forecast()`, σ₁₂ frente a la caminata, «el mismo modelo con deriva: ¿se queda?») sobre la serie hermana de la del E3. El E3 queda como repetición del c4m9, y la práctica del M9 no toca el otro objetivo del módulo (que $d$ y la constante deciden la forma), salvo en (c) | lectura de `templates_10.html` 992–1000 | **pedagogía** |
| 6 | `templates_7_9.html` 598 (lectura (c) del c4m8) | «La consecuencia práctica es que la raíz MA solo delata la diferencia sobrante si el modelo tiene orden suficiente para lo demás.» | Correcto para el caso, pero es literalmente la respuesta de E2(c) («¿cuáles delatan la diferencia, y **por qué no todos**?»); el E2 lo reconoce en su propia lectura («Es lo que mostraba la práctica del Módulo 8»). Junto con la caja de `log(lynx)` del M8 (mismas cuatro preguntas que el E2: pruebas, varianza frente a $2(1-r_1)$, raíz del ARIMA(2,1,1), modelo sin diferenciar), el E2 queda como aplicación directa. La frecuencia (78 %) está dicha y es correcta | `v5A_cifras.out`, M8: `raiz111_menor_1.05 0.780` | **pedagogía** (leve) |
| 7 | `templates_7_9.html` 401–402 (prosa nueva del M8) | «(El bloque que lo calcula está al final de la solución del ejercicio 2.)» | Cierto (el bloque `e2b` da 0.565, 1.653 → 0.687 y la raíz 1.000). Pero manda al estudiante a abrir la solución del E2, donde lo primero que ve es la respuesta de la liebre: el M8 sigue llevando a la solución del E2, ahora por la puerta de atrás | lectura de `templates_10.html` 906–975 | **pedagogía** |
| 8 | `templates_7_9.html` 946 (c4m9); `chapter.js` 1401 (quiz, zona de B) | `BJsales.lead`; `global_economy` (Colombia, importaciones) en el M4 y Chile/Perú en el quiz | No violan la lista a la letra (son otras series), pero `BJsales.lead` comparte página de ayuda y objeto de origen con `BJsales`, serie de la exposición y de los E1 y E3; el riesgo que el redactor mismo anota («que se confunda») es real, y se suma al 5 | `r5_ayuda_datasets.out`; `v5A_cifras.R` lee la misma ayuda | **menor** |
| 9 | `templates_4_6.html` 184 (c4m4, (a)) | «¿cuál corta y cuál decae?» | Pregunta con presuposición falsa: la respuesta es que **ninguna** decae (las dos «cortan en 1»). Solo la pista lo deshace | lectura de 187–219 | **menor** |
| 10 | `templates_1_3.html` 297 (pista del c4m1) | «Para (b) no hace falta ajustar nada más» | (b) exige ajustar el ARIMA(1,1,0); la frase quiere decir «nada más que ese modelo» | lectura | **menor** |
| 11 | `templates_7_9.html` 228 (c4m7) | «Toma la de producción industrial … 129 datos anuales» | Los valores van de $-0.105$ a $5.229$: no es un índice de producción sino, por su rango, su logaritmo; la ayuda de `NelPlo` no da unidades ni dice que esté en logaritmos (el redactor lo anota, duda 7). Un estudiante que la grafique verá valores negativos sin explicación | `v5A_cifras.out`, M7: `range -0.105 5.229`, primeros valores $-0.105, -0.105, -0.105, 0, 0, 0$ | **menor** |
| 12 | `templates_7_9.html` 292 (c4m7, (c)) | «los ARIMA($0,1,q$) con deriva de $q = 1$ a $4$ tienen todos peor AICc que el de partida» | Cierto ($-231.885, -232.224, -231.206, -229.723$ frente a $-233.722$), y está en `r5_cifras.out [M7-01]`, pero el bloque solo imprime $q = 1, 2$ (en el `head(…, 5)`): el estudiante no puede comprobar $q = 3, 4$ con la solución delante | `v5A_cifras.out`, M7 | **menor** |
| 13 | `templates_7_9.html` 948 (c4m9, (a)) | «para $h = 1$, $2$ y $12$» | A 375 px la coma queda sola al comienzo de línea («h = 1 / , 2 y 12»): son tres fórmulas separadas | `capturas/r5/v5A/c4m9-375.png` | **menor** |

Comprobado y **sin problema** (para que no se repita el trabajo): M1 fechas (abr. 1953 – sep. 1999 por `tsp`),
558 datos, la lectura del ee del AR(2) (límite del modelo 2.952 frente a $sd = 2.976$) y «apenas cambia el ajuste»
(log L $-328.34$ frente a $-329.58$); M2 asignación de etapas, idéntica a los paneles «Qué te devuelve atrás», y
sin cancelación AR–MA en el (2,1,2) (raíces AR 1.394 y 5.70, MA 1.7375); M3 65 %, 100 % y mediana 1.15 (con 9 de
500 ajustes del (1,1,1) que no convergen, que no cambian la mediana); M4 los $-0.08$ y $0.08$ teóricos, la banda,
los ΔAICc y ΔBIC, el AICc casero = `Arima()$aicc`; M5 todo, incluida la telescópica, $e^{0.182}$ y la coherencia
con el M5 («una deriva estimada es una tendencia que se extrapola sin límite»); M6 tres pruebas = 1 (no estaba en
el bloque; `v5A_cifras.out`), 250/249, el rango 0.96–3.14 y la TRM «no hay señal» del M10; M7 6 y 42 modelos, que
la escalonada paró según la regla de `forecast` (del (0,1,0)+deriva solo el (1,1,1)+deriva era vecino nuevo) y el
rezago 5 de la ACF residual ($-0.257$, banda $\pm0.173$); M8 $\rho_1$ teórico $-(1-\phi)/2$ (lo derivé: $\gamma_0(2\phi-1-\phi^2)/[2\gamma_0(1-\phi)]$) y la factorización de (c); M9 la forma cerrada con $\phi=0$, los ψ contra `ARMAtoMA`, los semianchos, el cociente que tiende a $|1+\theta|$ y la convención de 2 puntos dicha como convención. Ayuda: `tcm`, `NelPlo`, `airmiles`, `BJsales`,
`global_economy` y `gafa_stock` respaldan lo que se dice de cada serie (salvo lo del 11). La prosa del M8 sigue
diciendo lo correcto y ya no remite al E2 como su enunciado.

## Correcciones propuestas

1. **M6** (`templates_4_6.html` 722) «el modelo que lo alcanza es la caminata aleatoria de $d = 1$ con una
   diferencia de más» → «el modelo que lo alcanza es una caminata aleatoria con deriva escrita con una diferencia
   de más». Y en 762: «Su $\hat\sigma^2 = 372.71$ coincide con la varianza de $\nabla y$: el ARIMA($0,2,1$) es el
   ARIMA($0,1,0$) con una diferencia de más y un MA que la deshace.» → «Su $\hat\sigma^2 = 372.71$ coincide con la
   varianza de $\nabla y$ alrededor de su media: el ARIMA($0,2,1$) es una caminata aleatoria con deriva —la
   constante la pone la diferencia que el MA deshace— y no la caminata sin ella, cuya $\hat\sigma^2$ es
   $371.23$.» Añadir al bloque `round(c(sigma2_del_010 = arima(y, order = c(0, 1, 0), method = "ML")$sigma2), 2)`
   (→ 371.23) para que la cifra tenga su `#>`. La frase final («gana la caminata aleatoria») puede quedarse: ahí
   sí es el (0,1,0) sin constante el que gana con $d=1$.
2. **M3** (1093) «La semilla no es especial. En 500 series generadas igual (semillas 1 a 500), KPSS pide
   diferenciar la serie completa en todas; en el $65\,\%$, además, pide $d = 0$ en los dos tramos, y la raíz MA
   del ARIMA($1,1,1$) tiene mediana $1.15$.» → «La semilla está elegida para que salga el caso completo. En 500
   series generadas igual (semillas 1 a 500), KPSS pide diferenciar la serie completa en todas, y en el $65\,\%$
   pide $d = 0$ en los dos tramos; el reparto del Nilo (ADF y PP en $d = 0$) sale en el $52\,\%$, y con las
   tres pruebas en $d = 0$ en cada tramo, en el $33\,\%$. La raíz MA del ARIMA($1,1,1$) tiene mediana $1.15$.»
   Las cifras nuevas, a `r5_cifras.R` con etiqueta (están en `v5A_semillas.out`).
3. **M2** (al final de la lectura (c), 641) añadir: «La semilla está elegida para que se vean los cinco rasgos a
   la vez: en 200 series generadas igual (semillas 1 a 200) Ljung–Box rechaza el ARIMA($0,1,1$) en el $99.5\,\%$,
   pero el ARIMA($2,2,1$) solo deja la raíz MA en el círculo en el $65.5\,\%$, y los cinco rasgos coinciden en el
   $53\,\%$.» (cifras de `v5A_semillas.out`, a pasar a `r5_cifras.R`).
4. **M9** (758–759) «y cada choque acaba pesando más que cuando llegó: el ejercicio 3 lo mide sobre otra serie.»
   → «y cada choque acaba pesando más que cuando llegó.» (sin decir qué caso es el del E3).
5. **c4m9 frente al E3**: quitar el apartado (b) del c4m9 (enunciado 949; la línea 985 y su `#>`; la lectura
   1001; y en la Respuesta 964 «, pero más despacio que el de una caminata aleatoria»), que es el E3(c), y dejar
   que el c4m9 practique (a) y (c). Mejor aún, si se acepta el coste: cambiar la serie del c4m9 por una sin
   relación con `BJsales` (hallazgo 8).
6. **c4m8** (598) «La consecuencia práctica es que la raíz MA solo delata la diferencia sobrante si el modelo
   tiene orden suficiente para lo demás.» → «Aquí, la raíz MA solo delató la diferencia sobrante en el modelo que
   tenía sitio para la parte AR.» (el caso, no la regla; el E2 la generaliza, y su pista ya remite a este
   ejercicio).
7. **M8** (401–402) «(El bloque que lo calcula está al final de la solución del ejercicio 2.)» → mover el bloque
   `e2b` (sin texto marcado) a un `<pre>` justo después de esa caja del M8 y escribir «(El bloque de abajo lo
   calcula.)». Qué hacer con el párrafo «El mismo patrón en otra serie» del E2 y sus cinco marcas es de la parte
   de B.
8. **c4m4** (184) «¿cuál corta y cuál decae?» → «¿corta alguna?, ¿decae alguna?».
9. **c4m1** (297) «Para (b) no hace falta ajustar nada más:» → «Para (b), una vez ajustado el ARIMA($1,1,0$), no
   hace falta nada más:».
10. **c4m7** (228) tras «129 datos anuales, desde 1860» añadir: «en la escala que trae el paquete (la ayuda no da
    unidades; sus valores van de $-0.105$ a $5.229$)». Y para el 12: cambiar `head(exh$tabla[order(exh$tabla$AICc), ], 5)`
    por esa línea más `exh$tabla[grepl("^ARIMA\\(0,1,[0-5]\\) with drift", exh$tabla$modelo), ]`, con su `#>`.
11. **c4m9** (948) «para $h = 1$, $2$ y $12$» → «para $h = 1, 2$ y $12$».

## Respuestas a las dudas del redactor que caen en esta parte

- **2 (M3, probar por tramos; semilla 43).** Aplicar `ndiffs()` a cada lado no está enseñado en el M3, pero es
  la consecuencia directa del experimento del escalón y el ejercicio lo plantea de forma explícita: se puede
  resolver con lo enseñado. El problema no es ese sino el texto: dice «La semilla no es especial» cuando el
  propio informe dice que se eligió (hallazgo 2).
- **3 (la caja de `lynx` del M8 se queda).** De acuerdo en dejarla: es exposición y sus marcas están
  contrastadas. Pero, sumada a la práctica del M8 (hallazgo 6) y al paréntesis que manda a la solución del E2
  (hallazgo 7), el E2 queda como aplicación casi mecánica. Lo mínimo: las correcciones 6 y 7.
- **5 (tres simuladas, `tsibbledata`).** Tres simuladas de nueve es razonable, porque las tres dicen el modelo
  verdadero y eso es lo que practican; pero entonces las tres deben dar la frecuencia (falta en M2, falsa en M3,
  correcta en M8). `tsibbledata` carga sin red en este equipo (bloques 9/9 con los proxies cortados).
- **6 (semillas elegidas; φ = 0.8 en el M8).** El 78 % es correcto. Con $\phi = 0.6$ la firma saldría en el
  $95\,\%$ y $\hat\rho_1$ quedaría en $-0.20$ de mediana, también lejos de $-0.5$ (`v5A_semillas.out`); la elección
  de 0.8 hace la lección menos limpia pero está declarada, así que no es un defecto.
- **7 (M7, la traza frente al código; `NelPlo`).** La descripción coincide también con el código de
  `forecast`: desde el (0,1,0) con deriva, los vecinos (1,0), (0,1) y el cambio de constante ya estaban
  evaluados entre los cinco iniciales, y el único nuevo era el (1,1,1) con deriva. Lo de las unidades, hallazgo 11.
- **8 (juicios al final de M9 (c) y M5 (c)).** Son juicios razonables y coherentes con el M5 («una deriva
  estimada es una tendencia que se extrapola sin límite»); el del M9 se apoya en la convención de 2 puntos dicha
  como convención. La explicación del M5 («no es exactamente la media… porque se estima a la vez que $\theta$»)
  es correcta en lo que afirma y no pide fuente.
- **`BJsales.lead` (decisión pedida en §1).** Ver hallazgos 5 y 8: la serie es lícita a la letra, pero con el
  mismo esquema que el E3 lo vuelve repetición. Recomiendo, como mínimo, la corrección 5.

## Fuera de mi parte (para B)

`templates_10.html` 1050 (solución del E3) imprime `# --- (c) <U+00BF>crece como una caminata aleatoria?`: el
«¿» quedó como `<U+00BF>` (no estaba en `b53fdcb`). Se ve tal cual en la página.

## Segunda lectura (2026-11-23, tras la §10 de `R5_cambios.md`)

**Veredicto: aceptable.** Las trece correcciones están aplicadas y son correctas. No hay daños colaterales:
las `data-afirma` de las tres plantillas son las mismas, y los nueve bloques c4m1–c4m9 más el `<pre>` del lince
del M8 corren solos y reproducen su `#>` (10/10). El c4m9 nuevo (`austres`) es correcto en todas sus cifras y
practica el primer objetivo del M9. Quedan dos hallazgos **menores**, con corrección propuesta.

Comprobación: `comprobaciones/v5A_bloques.py --segunda` → `v5A2_bloques.out` y `v5A2_bloques/`; resolución
propia del c4m9 por otra vía (ψ con `ARMAtoMA`, anchos a mano, pendiente de C como suavizado exponencial de las
diferencias) en `v5A2_austres.R` → `.out`; por HTTP, solo los módulos cambiados (1, 2, 3, 4, 6, 7, 8, 9), puerto
8773, CDP 9283, a 1200 y 375 px, en `v5A2_revisa.js` → `.out` (todo en orden y consola limpia). Las capturas
están en `capturas/r5/v5A2/`. Servidor y Chrome, cerrados.

### Hallazgos nuevos

| # | Dónde | Qué es | Evidencia | Gravedad | Corrección |
|---|---|---|---|---|---|
| 14 | c4m9, bloque y lectura (c) (`templates_7_9.html`, sección del c4m9) | Ljung–Box con `lag = 10`; el resto del capítulo usa 20 y el texto no explica el cambio. Con 20, la conclusión no cambia: A y B $p < 0.0001$, C $p = 0.071$ | `v5A2_austres.out`: lags 8, 10 y 20 | menor | `lag = 10` → `lag = 20` en el bloque (el `#>` pasa a `0.0000 0.0000 0.0714`), y en (c) «solo C pasa Ljung–Box(10), con $p = 0.16$» → «solo C pasa Ljung–Box(20), con $p = 0.07$» |
| 15 | c4m9, lectura (b) | «con $d = 2$ la pendiente no es un parámetro, sale del tramo final de la serie (las ocho últimas diferencias promedian $46.19$)». Es cierto, pero el 46.19 no lo demuestra: no coincide con 43.23. Lo que sí coincide **exactamente** es el suavizado exponencial de las diferencias con $\alpha = 1 + \hat\theta = 0.408$ (43.229), y ahí las ocho últimas diferencias pesan el 98.5 % (es la duda 2 del redactor) | `v5A2_austres.out`, última línea: `43.229 43.229 0.408 0.985` | menor | Añadir al bloque `al <- 1 + coef(C)[["ma1"]]; round(c(alfa = al, peso_de_las_8_ultimas = 1 - (1 - al)^8), 3)` (→ `0.408 0.985`). En (b), «(las ocho últimas diferencias promedian $46.19$)» → «: es un promedio de las diferencias con pesos que decaen como $(1-\alpha)^j$, con $\alpha = 1 + \hat\theta = 0.408$ —el suavizamiento exponencial del Módulo 1 aplicado a $\nabla y$—, y las ocho últimas se llevan el $98.5\,\%$ del peso». La línea `ultimas_8_diferencias` puede quedarse como contraste o salir |

### El c4m9 nuevo, resuelto por mi cuenta

- **Cifras.** Todo coincide con R:
  - θ: A 0.846, B 0.467, C −0.592; σ̂: 31.7, 11.1 y 10.3.
  - Anchos reconstruidos desde los ψ: 124.3/1438.7, 43.6/402.0 y 40.4/2587.0.
  - Cocientes: 6.44, 9.21 y 64.02; diferencia entre B y C a 40 trimestres, 345.1.
  - Pruebas: KPSS 2, ADF 1, PP 1. `nsdiffs` = 0, así que tratarla sin estacionalidad no esconde nada del cap. 5.
- **Ayuda.** «en miles» y «cada trimestre» están en la ayuda; «desde 1971» vale tanto para la ayuda como para `tsp`. No está en el sitio ni en la lista de prohibidas.
- **Objetivo del módulo.** Practica que $d$ y la constante deciden la forma del pronóstico, que es la primera mitad del objetivo del M9. Los ψ quedan para el E3: ya no lo duplica.

### Las tres dudas

1. **Modelos que no pasan Ljung–Box.** Sí es aceptable. La forma del pronóstico es una propiedad de la especificación, no del ajuste, y el texto lo dice bien: «El ejercicio no elige modelo… solo C pasa». Sugerencia opcional: decirlo ya en el enunciado («ninguno se propone como modelo final»), para que nadie tome el 402.0 de B como un intervalo creíble.
2. **Fechas de `austres`.** La ayuda dice de marzo de 1971 a marzo de 1994; `tsp`, de 1971 T2 a 1993 T2, con 89 datos, que no llenan el rango de la ayuda. «desde 1971» es lo único que ambas sostienen: dejarlo así y no añadir mes ni año final.
3. **El `<pre>` del M8.**
   - **Se ve bien.** El script de la página lo envuelve como a todos (`wrapCodeBlocks`): rótulo «R», Copiar y Mostrar/Ocultar. Por fuera de un panel de solución empieza plegado a 150 px, igual que los bloques de pestañas. Es el único `<pre>` de la exposición fuera de `.code-tabs`, y le falta la pestaña de Python que llevan los demás; es una diferencia de forma, no un fallo. Si se quiere uniformar, basta con envolverlo en `.code-tabs` con solo R.
   - **Lo cuenta el verificador de bloques.** Sí: la expresión de `verifica_bloques_cap6.py` es `<pre><code class="language-(r|python)">` y lo recoge. Además reproduce su `#>` en un proceso aparte (`v5A2_bloques.out`).

### Estado de los hallazgos anteriores

| # | Estado |
|---|---|
| 1 | **Resuelto.** «caminata aleatoria con deriva», y el bloque imprime 371.23 (comprobado). |
| 2 | **Resuelto.** «La semilla está elegida…», con 100 %, 65 %, 52 % y 33 %: coinciden con `v5A_semillas.out`. |
| 3 | **Resuelto.** 99.5 %, 65.5 % y 53 %, iguales a los míos. «sobre el círculo» corresponde a módulo < 1.01, el criterio usado. |
| 4 | **Resuelto.** La frase acaba en «pesando más que cuando llegó». |
| 5 | **Resuelto.** El c4m9 nuevo ya no repite el E3. |
| 6 | **Resuelto**, con la redacción propuesta. |
| 7 | **Resuelto.** El bloque está en el M8 y reproduce su salida; el paréntesis dice «(El bloque de abajo lo calcula.)». |
| 8 | **Resuelto en mi parte** (`BJsales.lead` ya no se usa). `global_economy` sigue en el M4 y en el quiz, con otros países: se acepta. |
| 9–12 | **Resueltos** como se propuso. |
| 13 | **Desaparece** con el c4m9 nuevo (a 375 px no queda ninguna coma suelta). |
