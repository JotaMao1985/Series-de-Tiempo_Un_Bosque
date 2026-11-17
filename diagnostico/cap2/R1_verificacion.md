# R1 · Verificación independiente · Capítulo 2 «Estacionariedad, ACF y PACF»

Verificador que no redactó la ronda. Objeto: el diff sin commitear respecto a `HEAD` (`e1ebf32`) de
`Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html`, `precalculo/genera_cap2.R`,
`Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv` y el enlace `precalculo/trm_mensual_2015-01_2026-06.csv`.
Las líneas son las del archivo de trabajo. `R1_cambios.md` se leyó **al final**, después de cerrar la tabla.

Entorno: R 4.6.0 (tseries 0.10.62, forecast 9.0.2, urca 1.3.4); Python 3 con statsmodels 0.14.6, scipy 1.15.3,
numpy 2.2.6 y pandas 2.3.3; node 26; Chrome sin ventana. `pmdarima` no está instalado y no se instaló.

Guiones y salidas, en `diagnostico/cap2/comprobaciones/`:

| guion | salida | qué comprueba |
|---|---|---|
| `v1_cifras.R` | `v1_cifras.out` | toda cifra nueva o cambiada de la prosa, sin redondear; el CSV frente a `datos_series.json`; la ACF de ∇₁₂ log y; el AR(1) del M3 y el del M7; las variantes de Box–Cox; la P3 |
| `v1_contraejemplo.R` | `v1_contraejemplo.out` | el contraejemplo de la regla de la varianza (problema 1) |
| `v1_simulador_ar1.js` | `v1_simulador_ar1.out` | el simulador del M5 con las funciones extraídas del HTML |
| `v1_bloques_aislados.py` | `v1_bloques_aislados.out` | cada uno de los 21 bloques **solo**, en proceso nuevo; cada línea `#>` buscada como línea, en orden |
| `v1_trm_por_url.sh` | `v1_trm_por_url.out` | los bloques del M6 en una carpeta vacía, leyendo el CSV por HTTP como lo serviría GitHub Pages |
| `v1_csv_regenera.R` | `v1_csv_regenera.out` | el trozo nuevo de `genera_cap2.R`, aislado: ¿escribe el mismo archivo? |
| `v1_paridad_dolar.py` | `v1_paridad_dolar.out` | `$` impares en párrafos, celdas y cadenas del quiz |
| `v1_render_katex.js` | `v1_render_katex.out` | los nueve módulos por HTTP en Chrome: errores de KaTeX, excepciones, `console.error` |

---

## 1. Problemas

**Recuento: 1 bloquea publicar · 2 corregir · 12 menores.** «Ejecutado» = comprobado corriendo código;
«juicio» = lectura razonada.

| # | línea | qué dice | qué está mal | evidencia | tipo | gravedad |
|---|---|---|---|---|---|---|
| 1 | 3460–3462 (M7, señal 3); 6221 (quiz P4, `retroAcierto`). La misma regla, sin tocar, en 3964 y 3978 (M9, ciclo) | «Una diferencia que hacía falta la reduce mucho, y si al diferenciar la varianza **sube**, esa diferencia sobraba»; P4: «una varianza que sube **delata** la diferencia de más» | Es la mitad que quedó del error 4 del par, y también es falsa en general, **en las dos direcciones**. En un ARIMA(0,1,1) con θ = −0.8 la diferencia hace falta (hay raíz unitaria y `ndiffs` lo confirma), y aun así la varianza **sube** al diferenciar en más de la mitad de las muestras de 144. Es el modelo detrás del suavizado exponencial simple, nada exótico. La frase del recuadro de 3526 («salvo en series muy persistentes, infla la varianza») y la del ejercicio 3 («lo habitual es que la varianza suba») van con cautela; estas dos no | `Rscript v1_contraejemplo.R`: `set.seed(4); arima.sim(list(order=c(0,1,1), ma=-0.8), n=143)` → var(y) = 1.096, var(∇y) = **1.513**, `ndiffs` = **1**, ADF p = 0.226. Con 500 series: sube en el **58.8 %**, y de esas `ndiffs` = 1 en el 79.3 % | ejecutado | **bloquea publicar** |
| 2 | 3570–3574 (M7, moraleja del recuadro KPSS) | «Al aplicar la diferencia regular la varianza cae de 0.0038 a 0.0021 y r₁ queda en −0.341, lejos de −0.5: **la diferencia hacía falta**» | Es la inferencia que el propio módulo declara inválida 110 líneas antes (3461–3462: «que la varianza baje no demuestra que la diferencia hiciera falta») y en 3515–3520 y 3537–3540, donde un AR(1) sobrediferenciado tiene la varianza a la baja y r₁ = −0.148, todavía más lejos de −0.5. La caída es exactamente la que predice 2(1 − r₁) para una serie **estacionaria** con r₁ = 0.714: 2 · 0.286 · 0.00380 = 0.00218, frente a 0.00210 observado. No aporta información. La conclusión d = 1 es correcta y la sostienen la ACF lenta y `ndiffs`, que el texto da antes; sobra el «:» final | `v1_cifras.out` §M7 recuadro: var d12 = 0.0038001, var ∇d12 = 0.0021021, r₁ de d12 = 0.7137, r₁ de ∇d12 = −0.3411; `v1_cifras.out` §M7 AR(1): r₁(∇y) = −0.1477 con la varianza bajando | ejecutado + juicio | **corregir** |
| 3 | 2526–2527 (M3, fila «Decaimiento rápido») | «AR(1) con φ = 0.5 simulado sobre ese mismo ruido (Módulo 5): r₁ = 0.504, r₂ = 0.376, r₃ = 0.268, r₄ = 0.176, y r₅ = 0.078 ya está dentro de la banda ±0.139» | Las cinco cifras son correctas, pero el ejemplo repite el defecto del que sustituye. (i) En esa muestra se salen **9 de 24** rezagos: 1–4 y también **20–24** (de −0.151 a −0.188). Quien dibuje `acf(ar1(0.5, e), 24)` ve una cola fuera de la banda en el ejemplo de «memoria corta». (ii) La muestra no se parece a la teoría que el M5 enseña al lado (0.5, 0.25, 0.125: aquí 0.504, 0.376, 0.268). (iii) «(Módulo 5)» manda al lector al simulador, que usa **otro** ruido (semilla JS 20260726): con φ = 0.5 da 0.436, 0.155 y 0.008. (iv) «AR(1)» y φ aparecen aquí antes de definirse; el M5 ni siquiera escribe «AR(1)» | `v1_cifras.out` §M3: fuera = 1 2 3 4 20 21 22 23 24; `v1_simulador_ar1.out`: φ = 0.5 sin ∇ → 0.436 0.155 0.008 −0.008 0.040 | ejecutado + juicio | **corregir** |
| 4 | 2859 (M5, nota del simulador) | «Con φ < 1 la serie ya era estacionaria y la diferencia sobra; **lo delata** una autocorrelación negativa en el rezago 1» | Para φ cerca de 1 no delata nada: con φ = 0.95, r₁(∇y) = −0.044, dentro de la banda, y prácticamente igual al −0.032 de φ = 1. La nota anterior (2855–2856) ya dice que ese caso es indistinguible. Basta con «con φ lejos de 1» | `v1_simulador_ar1.out`: φ = 0.95 con ∇ → r₁ = −0.044, 1/24 fuera; φ = 1 → −0.032, 1/24 fuera | ejecutado | menor |
| 5 | 2364 (M2) | «Si el ruido es incorrelado pero no independiente […], la varianza de r_k **deja de ser** 1/T» | Demasiado categórico: lo que gobierna la varianza asintótica es E[x_t² x_{t−k}²]/σ⁴. Si los cuadrados no están correlacionados, sigue siendo 1/T aunque haya dependencia. En el caso ARCH de la advertencia sí cambia. Sería «puede dejar de ser». Además, la condición que el par leyó incluye cuarto momento finito, y la frase no la menciona | razonamiento | juicio | menor |
| 6 | 3214, 3221, 3227, 3232, 3249 (M6); 4239 (ej. 1) | `#> Warning: p-value smaller than printed p-value` | No es la salida real. R imprime `Warning message:` / `In kpss.test(trm) : p-value smaller than printed p-value` (y `Warning in …` con `warn = 1`). El bloque del M6 avisa de que la copia es abreviada; el del ejercicio 1, no. D2 pide «salidas reales» | `v1_bloques_aislados.out`, bloques 8 y 16: las cinco y la una líneas `Warning:` no casan; todo lo demás casa línea a línea | ejecutado | menor |
| 7 | 4412–4445 (ej. 4, R); 4448–4463 (ej. 4, Python) | bloques nuevos del ejercicio 4 | No corren solos: el de R usa `trm` del M6 y el de Python, `adf_como_en_r()`. El comentario lo dice, pero T1.4 pedía bloques autónomos, y el resto de bloques ahora lo son. Además, el verificador encadenado depende de la red en este bloque (descarga de datos.gov.co) | `v1_bloques_aislados.out`, bloque 19: `Error: object 'trm' not found`; bloque 20: `NameError: name 'adf_como_en_r' is not defined` | ejecutado | menor |
| 8 | 6307 (quiz P8, retro de «λ negativo no está permitido») | «La única restricción de Box–Cox es que los datos sean estrictamente positivos» | Contradice la nota nueva del M8 (3709–3711): `BoxCox()` y `box_cox()` admiten negativos cuando λ > 0. La ronda corrigió el M8 y dejó esta retro como estaba | `v1_cifras.out` §M8: `BoxCox(c(-2,4), 0.5)` → −4.83, 2.00; `fabletools::box_cox(c(-2,4), 0.5)` → −4.83, 2.00; con λ = −0.5 → NA, 1 | ejecutado | menor |
| 9 | 4067 (M9, Python) | «D no se decide con una prueba: se fija en 1 **porque la serie es estacional**» | El código no mira si la serie es estacional: impone D = 1 a toda serie con m > 1. Es justo lo que señalaba el par («cualquier serie mensual, estacional o no»). Debería decir «porque m > 1» | lectura del bloque: `D = 1 if m > 1 else 0` | juicio | menor |
| 10 | 4109–4111 (M9, «en la práctica») | «un modelo basado en árboles no puede predecir valores fuera del rango […] una serie con tendencia **lo deja sin respuesta**» | «Sin respuesta» no es exacto: el árbol responde con una meseta, el valor de su última hoja. Tampoco vale para todas las variantes (los árboles con hojas lineales extrapolan). Es una afirmación general sin fuente; el redactor la deja para la R4 | razonamiento | juicio | menor |
| 11 | 3112 (M6) | «`log(AirPassengers)`, que es la serie con la que se trabaja **de aquí en adelante**» | El pipeline de R del M9 (≈ 4003) usa Box–Cox con λ = −0.2947 sobre `AirPassengers`, no el logaritmo. Se resuelve con D6 (R3), pero la frase nueva lo promete ya | `v1_bloques_aislados.out`, bloque 14: `round(res$lambda, 4)` → −0.2947 y var_final 9.17e-05, en escala Box–Cox | ejecutado | menor |
| 12 | 3005; 3023 (M6, sin tocar) | «Con el ADF, "p < 0.05" significa *estacionaria*»; tabla: «Rechaza / No rechaza → **Estacionaria**» | El par marcó la tabla (2984–2986 orig.). La ronda corrigió la definición (2988–2990) y la frase de AirPassengers, pero 15 líneas más abajo el recuadro y la tabla siguen diciendo «estacionaria» a secas, junto a la definición que ahora dice «alrededor de la tendencia». El redactor lo declara pendiente para la R3 | lectura | juicio | menor |
| 13 | 4466; 4468 (ej. 4, solución) | «con 138 meses la evidencia **de la raíz unitaria** es abundante»; «p = 0.071, **a un paso de rechazar**» | (i) No rechazar el ADF no es evidencia de la raíz unitaria, y el capítulo lo enseña en la P5. Lo que sí es evidencia es el rechazo del KPSS. Sería «la evidencia contra la estacionariedad». (ii) Con p = 0.071 el ADF ya rechaza al 10 %: «a un paso de rechazar al 5 %» | `v1_cifras.out` §Ej. 4: 54 meses, p = 0.07084 | ejecutado + juicio | menor |
| 14 | 6042 (armazón JS del simulador del M7) | lectura «d de varianza mínima =», junto a «ndiffs (R) =» | Sigue presentando el d de varianza mínima como un criterio paralelo a `ndiffs`, y el comentario del código lo llama «la señal práctica de cuántas veces diferenciar». Está fuera de los `<template>` (es armazón, se ensambla en cadena): toca a la R2. Se anota para que el arreglo del problema 1 no quede desmentido por el simulador | lectura | juicio | menor |
| 15 | 2361, 3526, 3529 | «si **miramos** 24 rezagos, **esperamos**»; «**Mira** la columna»; «lo **diferenciamos**, **obtenemos**» | Las frases se reescribieron (o se volvieron a partir) y mantienen la primera del plural y el imperativo en la prosa expositiva. No lo introdujo la ronda, pero la ronda pasó por encima de ellas. «El componente», en masculino, está bien en lo nuevo (4302) | `git diff HEAD` | juicio | menor |

---

## 2. Lo comprobado ejecutando que está bien

- **Verificador de bloques**: `MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html …` →
  **210 de 210**, 12 bloques de R y 9 de Python. *Lo que no comprueba:* que un número aparezca en su sitio. Busca
  cada número como subcadena en cualquier parte de la salida del bloque, así que un `0` o un `1` casan siempre.
  Tampoco comprueba el texto (`TRUE`, `Warning`), el orden, que el bloque corra solo (encadena la sesión) ni la
  prosa frente a las salidas. Mi `v1_bloques_aislados.py` lo cubre en parte: los **21 bloques corren solos**,
  salvo los dos del ejercicio 4 (problema 7), y las 86 líneas `#>` casan **como línea y en orden**, salvo las seis
  de los avisos (problema 6).
- **Cifras nuevas o cambiadas** (`v1_cifras.out`), todas reproducidas. Las cifras de la prosa coinciden con las
  salidas bajo `#>`:
  - M6: TRM ADF −1.9783 (p 0.58549 → **0.585**); ∇TRM KPSS 0.24147 → **0.241**; KPSS de tendencia 0.27297 (p 0.01)
    y en la diferencia **0.0699** (p 0.10); AP k = 12 → −1.5094 (p **0.7807**); log AP k = 5 → **−6.42146** y
    k = 12 → **−1.53249**. Los nuevos redondeos (0.585, 0.241, −6.421, −1.532) son los correctos.
  - M3: AR(1) φ = 0.5 → 0.5042 0.3759 0.2681 0.1760 0.0779.
  - M5: simulador, con ∇, φ = 0.5 → **−0.252** y φ = 0 → **−0.506**. ρ₁(∇y) = −(1−φ)/2 se comprueba por álgebra.
    Con φ = 1.05 y ∇ quedan 24 de 24 rezagos fuera.
  - M7: AR(1) `set.seed(1)` → `ndiffs` 0, varianza 2.497 → 1.033, r₁ −0.148; ACF de ∇₁₂ log y: 0.714 0.623
    0.480, **fuera los rezagos 1–8** (y el 12), banda 0.1706; `nsdiffs(log AP)` 1, `ndiffs(d12)` 1,
    `ndiffs/nsdiffs(∇∇₁₂)` 0 y 0; `kpss.test(d12)` 0.36816 (p 0.09088); `ur.kpss` con 2 rezagos 0.5367; r₁₂ de
    ∇ log y 0.8414.
  - Var(∇y) = 2(1−ρ₁)Var(y): por álgebra, y la razón muestral del AR(1) es 0.413 frente a 0.4 teórico.
  - Ej. 2: el Monte Carlo del M6 es de **144** pasos y con amplitud 0 da **3.2 %**. Ej. 3: r₁ = 0.70747 → **0.707**.
    Ej. 4: 54 meses desde 2022, p **0.071**; 0.585 y 0.017.
  - M8: λ de scipy 0.148; `BoxCox().transform_boxcox(…, method="guerrero", window_length=12)` de statsmodels →
    **−0.29472**, igual que `BoxCox.lambda` de R. Su `_guerrero_cv` usa la misma razón sd/media^(1−λ). `BoxCox`
    con signo, comprobado en el código de forecast y de fabletools. Guerrero anual sin argumentos (Nile) → 0.9989:
    bloques de 2 por defecto, como dice la P8.
  - M4: `pacf(method="ldb")` llama a `levinson_durbin` (leído en el código de statsmodels 0.14.6) y
    `np.allclose(ywm, ldb)` → True.
  - Quiz P3: ∇ log AP con n = 143 y banda 0.1639 tiene **10 de 24** fuera (1 4 8 11 12 13 16 20 23 24).
- **TRM congelada**: el CSV es **idéntico** a `datos_series.json` (138 valores, de 2015-01 a 2026-06,
  consecutivos, diferencia máxima 0). El trozo nuevo de `genera_cap2.R` lo **regenera byte a byte**. Los bloques
  del M6, en una carpeta vacía y leyendo por HTTP desde `Htmls_Series/` servido en local, dan las mismas cifras en
  R y en Python. La base de la URL es la del sitio: el capítulo responde 200 en
  `jotamao1985.github.io/Series-de-Tiempo_Un_Bosque/`. El CSV ahí responde **404 hasta que se despliegue**.
  `.gitignore` no lo excluye.
- **Armazón intacto**: todos los trozos del diff caen en las líneas 2358–4473 (dentro de los templates 2–9,
  2305–4533) y 6195–6315 (dentro de `AUTOEVALUACIONES['cap2']`, 6139–6321). `DATOS_CAP2` (4556) no cambió.
  `python3 ensamblado/ensambla_cap3.py` → «reproducible byte a byte». `verifica_todo.py` → 11 en verde.
- **Quiz**: claves correctas (P1 3, P3 1, P4 {1, 3, 4}, P5 4, P6 2, P8 4; P2 0.1633, P7 131).
  `audita_posicion_correcta.py`: cap2 en verde (orden 31424; la peor posición, la 4, con 2 de 5, que es el 40 %
  justo en el límite). Las tres correctas de la P4 no van seguidas. La P8 sigue teniendo como correcta la opción
  más larga, pero ya la tenía antes; es materia de la R5.
- **Render**: 0 `$` impares; en Chrome por HTTP, a 1280 px, los nueve módulos con 360 fórmulas, 0 `.katex-error`,
  0 excepciones y 0 `console.error`.
- **Errores del par, buscados también fuera del sitio corregido**: no queda «∇TRM … decaimiento», «cualquier φ»,
  «tercer decimal», `BoxCoxEndogTransformer`, «Seis preguntas», «FPP3 hace la misma recomendación» ni «trivial».
  El 0.088 de la l. 3493 es el r₁ de ∇TRM en la tabla del M7, y ahí está bien. Lo que sí queda desplazado es la
  regla de la varianza (problema 1: M9, l. 3964 y 3978, y el simulador, problema 14) y la restricción de Box–Cox
  en la P8 (problema 8).
- **Atribuciones nuevas**: ninguna. Los «Dickey» y «MacKinnon» del diff son salida de R y un comentario que ya
  estaba.

## 3. Lo que no pude comprobar

- **Los resultados de `pmdarima`** (l. 3655–3658: `ndiffs → 1`, `nsdiffs ocsb → 1`, «Con pmdarima 2.1.1»). No
  está instalado y no instalé nada. La 2.1.1 existe en PyPI (publicada el 2025-11-17), según los metadatos.
- **La URL pública del CSV tras desplegar.** Hoy da 404, como es de esperar. El camino por HTTP solo lo probé
  contra un servidor local.
- **Lo visual a 800 y 375 px** (es la R2). Solo comprobé el render de KaTeX a 1280.
- **`statsmodels.base.transform.BoxCox` en otras versiones de statsmodels.** Solo probé la 0.14.6, y es una
  clase poco documentada.
- **Que `pacf()` de R implemente Durbin–Levinson** (afirmación que ya estaba). Llama a `C_pacf1` y no leí el
  código en C. Las dos vías dan los mismos números, así que la coincidencia numérica no decide entre ellas.

---

## 4. Diferencias con `R1_cambios.md` (leído después de la tabla)

1. **La regla de la varianza (problema 1).** El redactor la da por corregida: «si la varianza sube, sobraba» como
   señal de apoyo, con el sentido inverso descartado. En su punto 7 de «lo que el diagnóstico no vio» detecta que
   «r₁ ≈ −0.5» no es universal, pero no prueba el contraejemplo de la mitad que conserva, ni el de «una diferencia
   que hacía falta la reduce mucho». El ARIMA(0,1,1) con θ = −0.8 rompe las dos. El par ya había escrito «lo
   fiable es el sentido inverso», y la ronda heredó esa premisa sin ponerla a prueba.
2. **La moraleja del recuadro (problema 2).** El redactor la presenta como corrección del error 5 y cita las
   varianzas 0.00380 y 0.00210 como evidencia. No advierte que esa caída es la que da 2(1 − r₁) para una serie
   estacionaria, ni que contradice su propia señal 3 del mismo módulo.
3. **El ejemplo del M3 (problema 3).** Coincidimos en el hecho: el redactor también vio que los rezagos 20–24 se
   salen y por eso evitó «todo lo demás dentro». Diferimos en el juicio: para mí, un ejemplo de «memoria corta»
   con 9 de 24 rezagos fuera y una cola negativa sigue sin ilustrarla. Además, remite a un simulador que da otros
   números, y estrena «AR(1)» y φ antes del M5. El redactor no menciona estos dos últimos puntos.
4. **Las salidas «literales».** El redactor dice 86 de 86 literales y explica que los avisos van abreviados. Las
   seis líneas `Warning:` no son la salida de R; el bloque del M6 lo declara y el del ejercicio 1 no (problema 6).
5. **Dependencias del ejercicio 4.** El redactor declara solo la del bloque de Python («el único bloque de Python
   que depende de otro»). El bloque de R también depende del M6 (`trm`) y falla solo (problema 7).
6. **La retro de la P8** sobre la restricción de Box–Cox (problema 8) y **el comentario «porque la serie es
   estacional»** del M9 (problema 9) no aparecen en su registro. El segundo lo da por corregido; para mí repite la
   imprecisión del par con otras palabras.
7. **`pmdarima`.** El redactor lo ejecutó (2.1.1, en un entorno desechable) y anota que su `ndiffs` sobre
   ∇₁₂ log y da 0 donde R da 1. Yo no pude reproducirlo; lo dejo como no comprobado.
8. En lo demás coincidimos: los cinco redondeos dobles (0.585, 0.241, −6.421, −1.532, 0.707) son correctos, el CSV
   es fiel y regenerable, el armazón no se tocó, el cap. 3 se reproduce, y la tabla de cuatro combinaciones del
   M6 y el pipeline con Box–Cox se dejan, declarados, para la R3 (problemas 11 y 12).
