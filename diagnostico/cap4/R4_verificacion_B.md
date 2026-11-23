# Capítulo 4 · ronda R4 «fuentes» · verificación independiente, lote B (M7–M12)

Fecha: 2026-11-23. Verificador independiente (subagente, contexto limpio): no redactó nada de esta ronda.
Leyó `CLAUDE.md`, `bibliografia/README.md` y `diagnostico/cap3/R4_verificacion_B.md`. No leyó
`diagnostico/cap4/R4_cambios.md` ni `bibliografia/_local/herramientas/cap4/` hasta terminar las secciones 1 a 8; la 9 es
la comparación (de `_local/herramientas/` no se leyó nada).

No toqué nada fuera de `diagnostico/cap4/`: ni la prosa, ni `cap4.yml` (sin `verificado_por`: la firma está en
`comprobaciones/v4_firmas_B.txt`), ni el JS. Sin commits, sin reensamblar: la huella md5 del HTML del capítulo fue
`b196030b…` al empezar y al terminar. Ningún literal de fuente en este archivo salvo fragmentos de menos de 25 palabras.

Guiones y salidas (`diagnostico/cap4/comprobaciones/`): `v4B_vuelca.py` → `v4B_vuelca.out` (cada entrada con su texto de
hoy, su huella, sus citas visibles, el literal y ±500 caracteres de la fuente en su localizador); `v4B_software.R` →
`.out` (R 4.6.0, forecast 9.0.2, tseries 0.10-62); `v4B_software.py` → `v4B_software_py.out` (statsmodels 0.14.6);
`v4B_listas.py` → `.out` (listas por módulo, lista del capítulo y pie).

## 1. Resultado

| | entradas |
|---|---|
| Lote B (`c4-m7-*` a `c4-m10-*`) | 145 (M7 20, M8 21, M9 34, M10 70) |
| **Firmadas** | **142**: 71 `respaldada`, 32 `con-matiz`, 37 `propia`, 2 `pendiente` |
| **Sin firmar** | **3**: c4-m7-05 (`con-matiz`), c4-m7-10 (`propia`), c4-m8-10 (`con-matiz`) |

Las 145 huellas de prosa coinciden con `hash_texto`; los 222 literales de mis entradas tienen la huella del
registro y están en su página (PDF, con la siguiente) o en la sección que dice el localizador (FPP3 y ayudas de R).
Ningún literal cae fuera de su sitio. Qué significa la firma: leí el pasaje en su contexto, el veredicto, el localizador
y la nota son correctos, la cita visible no cubre nada que la fuente no diga; en las `propia` repetí la cuenta o la
derivación (§4); en las dos `pendiente` el motivo es cierto (la 4.ª de Shumway y Stoffer no tiene texto en la caché; la
3.ª numera 3.5, 3.7 y 3.8, comprobado; datos.gov.co no es obra de `referencias.json`).

`git diff 21b311b -- ensamblado/cap4/chapter.js` está vacío: la ronda no tocó quiz, simulacro ni simuladores.

## 2. Errores (algo que el estudiante lee mal o una cita pegada a lo que la fuente no dice)

| id o lugar | qué dice | qué dice la fuente | qué falla | propuesta de texto |
|---|---|---|---|---|
| **c4-m7-05** (M7, paso 2 del algoritmo) | «El de menor AICc es el *modelo actual* (Hyndman y Khandakar, 2008, p. 11).» | El artículo (p. 11) elige entre los cuatro iniciales el de menor **AIC** y usa el AIC en todo el algoritmo (pp. 10–11). El AICc lo dicen FPP3 §9.7 (de fable) y la ayuda de `auto.arima` (§Usage, `ic` por defecto `"aicc"`; comprobado con `formals`). | La cita visible cae justo sobre el dato que el artículo no dice. Es el mismo caso que c3-m9-20 en el capítulo 3, que se corrigió moviendo la cita. La nota lo reconoce, pero el estudiante no ve la nota. | «El de menor AICc es el *modelo actual* (Hyndman y Athanasopoulos, 2021, §9.7); el artículo original elegía por AIC (Hyndman y Khandakar, 2008, p. 11).» Cambia la huella; volvería a pedir firma, que daría. |
| **c4-m7-10** (M7, mismo párrafo que c4-m7-09) | «…el artículo rechaza el modelo con alguna raíz de módulo menor que $1.001$ … su menor raíz AR tiene módulo $1.001$.» | La raíz es 1.000937 con CSS-ML (1.000875 con deriva): `v4B_software.out` §C. El bloque de código del propio módulo imprime 1.0009. | Redondeada a tres decimales, la cifra coincide con el umbral: quien lea «menor que 1.001» y luego «módulo 1.001» concluye que el artículo **no** lo rechazaría, que es lo contrario de lo que el párrafo quiere decir. | «…su menor raíz AR tiene módulo $1.0009$, por debajo de los dos umbrales.» La cifra ya está en la salida impresa del bloque (no es cifra nueva). |
| **c4-m8-10** (M8, recuadro de la varianza) | «…y aun así $d = 1$ sobra, como coinciden en señalar ADF, KPSS y Phillips–Perron (Hyndman y Athanasopoulos, 2021, §9.1).» | FPP3 §9.1 dice que una serie con ciclos de longitud no fija (la de los linces) es estacionaria. No ejecuta ninguna prueba sobre ella. Las tres pruebas son cifras de R (comprobadas: `ndiffs` 0/0/0; `adf.test` 0.01, `kpss.test` 0.10, `PP.test` y `pp.test` 0.01). | La cita, pegada a «como coinciden en señalar ADF, KPSS y Phillips–Perron», atribuye a FPP3 el resultado de las pruebas. Además la nota dice que FPP3 habla de la serie «(sin logaritmo)», cosa que la caché no permite saber (los pies de figura no están extraídos), y la 2.ª fuente (Hamilton p. 506, quién propuso la prueba de PP) no respalda nada de la frase. | «…y aun así $d = 1$ sobra: una serie con ciclos de longitud no fija es estacionaria (Hyndman y Athanasopoulos, 2021, §9.1), y ADF, KPSS y Phillips–Perron coinciden en no diferenciar.» En el registro, quitar Hamilton p. 506 y «(sin logaritmo)» de la nota. |

## 3. Juicios (firmadas; el veredicto se sostiene, pero algo debería cambiar)

| id o lugar | qué falla | propuesta |
|---|---|---|
| **Quiz del M7** (`ensamblado/cap4/chapter.js:1575`, retroalimentación de la opción correcta, y la pista de la pregunta) | «por debajo del umbral **habitual** de $2$». La ronda declaró el umbral convención del capítulo en el M6 y el M7 porque ninguna fuente leída lo da; el quiz lo sigue presentando como norma general. La pista («¿Cuánta diferencia de AICc hace falta para distinguir dos modelos?») sugiere lo mismo. Sin marca: lo ve el estudiante | «…por debajo del umbral de $2$ que el capítulo toma por convención». Es de la R5 (el redactor lo anota), pero es la misma afirmación que esta ronda retiró de la prosa |
| **c4-m8-17** | `tipo: historica`. La frase de hoy («un ARIMA sin término de intervención no tiene dónde poner el cambio de nivel, así que lo absorbe subiendo $d$») no es histórica: era la vieja («Box–Jenkins no tiene una etapa…») la que lo era | `tipo: resultado` (o `regla`). No cambia el veredicto |
| **c4-m10-123** | La cita va **después del punto**: «…no es opcional.**</strong>** (Hyndman y Athanasopoulos, 2021, §9.7)». Es la única así en M7–M12 (búsqueda de `[.:;]` seguido de `<cite`) | Cita antes del punto, dentro del `strong` o justo tras él: «…no es opcional (…, §9.7).» |
| **c4-m10-15** | «Es ruido blanco.» sobre una ACF con una barra fuera. La nota lo reconoce (FPP3 dice «se parece a la de un ruido blanco»); la prosa lo afirma | «Es compatible con ruido blanco.» Cambia huella |
| **c4-m7-11** | «la búsqueda usa **además** una verosimilitud aproximada (CSS)»: según la ayuda, con `approximation = TRUE` la estimación de la búsqueda *es* por CSS (en lugar de CSS-ML) y el modelo final se reajusta por máxima verosimilitud; «además» sugiere que se calculan las dos | «la búsqueda usa una verosimilitud aproximada (CSS) en lugar de la exacta y al final reajusta el ganador con la exacta» |
| **Notas caducas** | c4-m8-65 remite a «c4-m10-56», que no existe ni en el registro ni en el HTML. c4-m10-21 dice que la frase del M7 (c4-m7-09) «debería decir lo mismo»: ya lo dice | Limpieza del registro; no cambia nada visible |

### Observaciones sobre entradas firmadas (no impiden la firma)

- **c4-m7-09.** Correcta tal como está: el artículo da 1.001 (p. 11) y el código instalado `minroot < 1 + 0.01` con
  `fit$ic <- Inf` (`v4B_software.out` §A: no aparece ningún 1.001 en `myarima`). También comprobé que `auto.arima`
  pasa `method = "CSS-ML"` a `Arima()` cuando `approximation = FALSE`, como dice la frase siguiente, y que la búsqueda
  escalonada cambia de modelo actual en cuanto encuentra uno mejor (`next` en el bucle), como dice c4-m7-06 citando
  FPP3, que habla de fable. El M10 (c4-m10-21, -113) repite las dos cifras con su origen; el (2,1,2) de la TRM tiene la
  raíz MA en 1.000018 y la AR en 1.0042: «por debajo de los dos» es cierto del modelo (de su raíz mínima).
- **Regla de 2 puntos.** En la prosa (M6 l. 4197, M7 c4-m7-14 y -15) ya es convención declarada; c4-m10-119 («siete
  caben en $2$ puntos») no la reformula, y no hace falta. El recuento se reproduce: siete modelos a menos de 2 puntos,
  el octavo, ARIMA(0,1,3), a +2.13.
- **Nilo y cambio de nivel.** Coherente en todo el capítulo: media 1097.75 hasta 1898 y 849.97 desde 1899, «cambio
  aparente cerca de 1898» atribuido a `?Nile` (c4-m8-12, c4-m10-83), 1899 como año del capítulo. No queda ninguna presa
  en el capítulo ni en `genera_cap4.R` salvo el comentario que explica la retirada. «Asuán» sigue solo como lugar de
  medida (M1 y `SERIES_CAP4.descripcion`), que es lo que dice `?Nile`. El campo `fuente` del JSON de la serie dice
  «Cobb (1978) (datasets de R)», cuando `?Nile` da como Source a Durbin y Koopman (2001) y cita a Cobb en Description;
  no se muestra en pantalla (ninguna referencia a `.fuente` en el JS).
- **Lecturas del M10.** c4-m10-74: las cuatro secciones de FPP3 existen con esos temas (9.7 es «ARIMA modelling in
  fable»). c4-m10-81: §3.1 empieza en la p. 9 y §3.2 en la p. 10; el 3.3 en la p. 11: «pp. 9 a 11» correcto; volumen 27,
  número 3, julio de 2008 (p. 1). c4-m10-78: FPP3 §9.12 (clásico que popularizó el ARIMA; la 5.ª es de 2015) y Cryer y
  Chan p. 8 (estrategia en tres pasos «de Box y Jenkins (1976)»). c4-m10-83: Cobb (1978), *Biometrika* 65(2), coincide
  con `?Nile` (§References) y con `referencias.json`. Las fichas de Box et al., Shumway y Stoffer y Cobb siguen
  tecleadas con «&» y no generadas (como en el cap. 3).
- **c4-m10-61.** «cuyos datos figuran en Box y Jenkins (1976, p. 537)» es una cita de segunda mano visible: la apoya la
  cita a `?BJsales` (§Source), que lo dice tal cual. Está bien así mientras `data-via` no exista.
- **Ayuda de R sin nombre de página.** Como en el cap. 3: «(R Core Team, 2026, §Details)» no dice si es `?Box.test` o
  `?predict.Arima`. Es del generador.
- **c4-m9-25 / c4-m10-35.** La cobertura del 83.9 % es dentro de muestra (cambios observados frente a $\hat\sigma$
  estimado con ellos). La prosa del M10 lo dice («dentro de la muestra»); la del M9 no, pero remite al M10.

## 4. Propias repetidas (`v4B_software.R` → `.out`; `v4B_software.py` → `_py.out`)

Todas las cifras de las 38 `propia` del lote se reproducen (y las de las `con-matiz`/`respaldada` que llevan cifras):

| entradas | resultado |
|---|---|
| c4-m7-60, -12, -61, -14, -15 | `length(Nile) > 150 ‖ frequency > 12` = FALSE; escalonada 18 modelos, exhaustiva 42; ganador ARIMA(1,1,1) 1267.507 en las dos; podio +0.56, +0.70, +1.46, +1.71, +1.81, +1.84 (siete), octavo +2.13; d = 1 en todos; máx p+q = 5 |
| c4-m7-09, -10 | `minroot < 1 + 0.01`, sin 1.001; (2,1,2) CSS-ML: logL −630.169, raíz AR 1.000937 (deriva 1.000875); ML: −630.445, raíz AR 2.2407; las dos líneas (con y sin deriva) con AICc Inf en la traza |
| c4-m8-02, -05, -06 | LB(20, fitdf 2) 0.800, Shapiro 0.731; MA(1) sobre ∇²y: θ̂ −1.000000, σ̂² 28268.34 = var(∇y); sobre ∇³y: θ̂ −0.999999, σ̂² 80055.05 frente a 80055.01; rejilla d = 2: raíces MA 1.000000, 1.000001, 1.000001, 1.000014, 1.031564, 1.048272; mejor BIC (0,2,2) 1273.50 |
| c4-m8-60, -10, -11, -61 | Nilo: 0.987 frente a 2(1−r1) 1.003; log(lynx): 1.653 → 0.687 (−58.4 %), r1 de la diferencia 0.565, pruebas como en §2, ARIMA(2,1,1) raíz MA 1.00000 |
| c4-m8-12, -14, -15, -16, -20 | medias 1097.75/849.97; β̂ −247.78, e.e. 28.15, t −8.80, AICc 1257.91; mejor ARMA d = 0: ARMA(1,1) 1282.50; LB(20) 0.812; fuera de muestra RMSE 125.05 / 127.99 / 128.31 / 123.06 / 133.31 (rango 123–133), sd residual 139.67. statsmodels: β̂ −247.78 |
| c4-m9-03, -62, -04, -60, -05, -67, -68, -06, -07, -66 | media CSS-ML 920.56, ML 920.70, muestral 919.35; h = 1 y 30: 816.18 y 842.17; pendiente −2.883; d = 2: segunda diferencia 0.000000, cociente −0.3924 en h = 3..8; aviso «No drift term fitted as the order of difference is 2 or more.»; anchos 95 %: 613 (h = 1, d = 2) y 2771 (h = 30), d = 1: 781; recursión: error 1.9·10⁻¹¹, límite 842.17 |
| c4-m9-09, -10, -19, -13, -14, -15, -16 | θ̂ −0.999999, ψ₂₉ 0.7182 = 1/(1−φ̂); ancho con ψ 2427.96 frente a 2771.45; con θ fijo −0.90 / −0.99 / −1.00 la razón forecast()/fórmula es 1.0000 / 1.0355 / 1.1415; forma cerrada: error 5.0·10⁻¹⁶; ψ∞ 0.1688 (ψ₄₀₀ igual); semianchos: error 9.08·10⁻¹¹; σ 142.045, σ₃₀ 199.36, σ√30 778.02 (3.90 veces), σ₃₀/σ₁ 1.404 |
| c4-m9-23, -65, -26 | qnorm 1.96 y 1.2816; Shapiro 0.00063 (R, 138 residuales; statsmodels 0.0007 con 137, lo que el bloque de Python explica); cubre el 80 % el 0.8394 |
| c4-m10-01, -117, -02, -119, -04, -110 | adf 0.064, kpss 0.010, pp.test 0.010; ACF/PACF de ∇Nilo: −0.402 y PACF negativa en los rezagos 1–6 (−0.402, −0.246, −0.119, −0.173, −0.155, −0.074); deriva −2.883, t −1.43, AICc 1268.06 frente a 1267.51; media de las diferencias −3.84, β̂/99 = −2.50; min AICc (1,1,1) 1267.51, min BIC (0,1,1) 1274.28; (1,2,2) 1264.60 con nobs 98 frente a 99; raíces 1.144 y 3.93 |
| c4-m10-111, -10 | promedio mensual de la diaria: `precalculo/genera_datos.R:101` (`aggregate(valor ~ mes, …, FUN = mean)`); log-retornos: r1 0.105 (banda 0.167), LB 0.0931 / 0.0601 / 0.0599 en 6, 12, 20 (0.0322 en 10), `auto.arima` ARIMA(0,0,0) sin media |
| c4-m10-11, -14, -15, -105 | acf1 0.964; ADF −1.978 (0.585), KPSS 2.243, ∇: −3.880 (0.017), 0.241; ndiffs 1, nsdiffs 0 (también ocsb), umbral `> 0.64` en el código de `nsdiffs`; ρ̂1 0.088, ρ̂8 −0.190, banda 0.167, una sola barra fuera |
| c4-m10-18, -19, -112, -20, -21, -113, -115, -114 | (2,1,2) gana por 2.56; AR 0.6612, −0.9917, MA −0.622614, 0.999963; \|AR\| 1.004185, \|MA\| 1.000018406; distancia mínima AR–MA 0.0223; `auto.arima` exhaustivo: ARIMA(0,1,0), los seis (2,1,2) de la traza con Inf; LB 0.189 / 0.206 |
| c4-m10-120, -121, -27, -30 | deriva 8.0009 = media de las diferencias = (y₁₃₈ − y₁)/137, e.e. 10.36, t 0.77; σ 121.48; semiancho a 24 meses 1166.39, [2330.70, 4663.48], 33.35 % del nivel |
| c4-m10-32, -33, -34, -35, -37 | LB(12) de cuadrados 0.857; curtosis simple 5.09 (exceso 2.09), asimetría 0.761; mayores alzas 2020-03 (+470.2), 2022-07 (+466.8); fuera del 95 %: 6 (5 arriba) de 137, a 12 meses 11 de 126 (8.7 %), curtosis 2.83; binomial 5 de 6: 0.109; razones 1.097, 1.144, 1.069 |
| c4-m10-45, -46, -49, -50 | ARIMA(0,1,5); ρ̂12 0.7245 (4.4 bandas), ρ̂24 0.6727; amplio ARIMA(8,1,3) con deriva, ρ̂12 0.437; airline ρ̂12 −0.0515, LB(24) 0.2330; nobs 143 y 131 |
| c4-m10-65, -72 | BJsales: ACF residual del (0,1,1) 0.2483 (r2) y 0.2087 (r4), banda 0.16; φ̂ 0.8799; LB 0.0340 → 0.6216; mejor d = 2 (1,2,2) 515.86 con raíz MA 1.000001 frente a 514.902; nobs 149/148; ψ₁₂ 2.5593, límite 2.9883, σ₁₂ = 1.9619 veces la caminata; deriva 0.4001, t 1.5644, AICc 515.062, h = 12: 266.99 frente a 263.76 |
| c4-m10-150, -67, -69, -70 | AR(2) de log(lynx): 1.3776, −0.7399, periodo 9.7839 por la raíz y 10.0236 por la fórmula de FPP3 §9.5; varianzas 1.6532, 0.6871, 0.6026, 1.1532; r1 0.785, cociente 0.416, 2(1−r1) 0.430; LB del AR(2) 0.0094; `auto.arima` ARIMA(2,0,3) |
| c4-m10-71 | arima ML 19769.29 = SSR/99 (19769.30); Arima 20176.91 = SSR/97; razón 1.02062 = 99/97 |
| c4-m10-116, -124, c4-m7-16, c4-m8-16, c4-m9-16 | derivaciones o lecturas del material: correctas tal como se enuncian (θ = −1 anula los ψ_j con d = 1; un MA necesita q ≥ 24 para llegar al rezago 24) |

## 5. Cambios de prosa revisados (M7–M12, `git diff 21b311b`)

Revisé con `--word-diff` los de `templates_7_9.html` y `templates_10.html`; `templates_11.html`, `templates_12.html` y
`chapter.js` no cambian. Los cambios de M7–M10 (filas 24 a 61 de la tabla de `R4_cambios.md`) son correctos o mejoran el texto: ninguno introduce un error, cambia
el sentido de algo correcto ni rompe la voz impersonal; ninguna cifra nueva sin R (1.001 es del artículo, «versión
9.0.2» el dato de la obra, «1976, p. 537» y «cerca de 1898» de las ayudas, 1.088 de la salida del bloque, «a tres» y
«a cuatro decimales» describen cifras ya impresas). En particular:

- Correctos y comprobados: «Aquí coinciden» (antes «lo habitual»); 2 puntos como convención; «a tres decimales»;
  «sobre el círculo (a cuatro decimales)» y «casi se cancelan»; los dos umbrales; la presa fuera; «suelen seguir siendo
  razonables» (Hamilton p. 117); «tienden a quedar demasiado estrechos»; «alzas/bajas» en lugar de devaluación;
  «el intervalo normal… no la recoge» con el bootstrap; BJsales sin «Serie M» ni «de libro»; el lince con «ciclos de
  longitud no fija».
- **Comentarios de código cambiados** (bloque de Python de la TRM, M10), los dos ciertos: con el arranque por defecto
  statsmodels da un (2,1,2) con raíces MA 1.088 y 4.208 y AICc 1712.91, 6.97 peor que el (0,1,0); con los coeficientes
  de R como arranque llega a raíces MA 1.00002 (AICc 1703.27); la deriva tiene e.e. 11.17 con OPG y 10.35 con la
  información observada (`v4B_software_py.out`). El comentario «Etapa 3: por que falla el IMA(1,1)» es correcto.
- **`genera_cap4.R`**: el comentario y `cambio_nivel$fuente` dicen lo que dice `?Nile`; el JSON solo cambia esa línea y
  la fecha. Correcto.
- Lo único que no cierra está en §2 (c4-m7-10: el 1.001 que la ronda dejó junto al umbral 1.001) y §3.

## 6. Pie y listas (`v4B_listas.out`)

- M7–M10: cada lista de fuentes del módulo tiene exactamente las obras citadas en él; 0 enlaces rotos, 0 citas vacías,
  y el `title` de cada cita es la ficha de la lista. M11 y M12 no citan y no tienen lista (correcto).
- Lista del capítulo (tras las lecturas del M10): las 7 obras citadas en todo el capítulo, ni una más.
- Pie: la bibliografía básica (Box et al. 5.ª, 2015; Brockwell y Davis 3.ª; FPP3; Shumway y Stoffer 4.ª), generada.
  Coherente con las lecturas del M10.
- **Orden (bajo, del generador):** en las listas del M7, M9, M10 y del capítulo, «Hyndman, R. J., Athanasopoulos, G.,
  Bergmeir, C., … (2026)» va **antes** que «Hyndman, R. J., y Athanasopoulos, G. (2021)». `genera_referencias.py:173`
  ordena por el texto de la ficha, y compara la «y» de la ficha de dos autores con «Bergmeir»: la ficha de dos autores
  debería ir primero (se ordena por los apellidos, no por la conjunción). Afecta a cualquier capítulo que cite las dos.

## 7. Fuera del capítulo, pero sobre lo mismo

- **Diapositivas del cap. 4**: una viñeta visible (`diapositivas/fuentes/capitulo_4.md:545`, y su HTML) dice que el
  descenso coincide en fecha con la construcción de la presa baja de Asuán; la nota (l. 552) lo apoya en Wikipedia y
  resúmenes de buscador, ninguno en la biblioteca. El capítulo ya no lo dice. Decide Javier.
- El quiz del M7 («umbral habitual»): §3.

## 8. Lo que no pude comprobar

- El bloque de Python del puente (descarga AirPassengers) no lo ejecuté; las cifras del puente las comprobé en R.
- No hice recorrido visual por HTTP (citas a 375 px, KaTeX): no estaba en el encargo y no quise arrancar servidores que
  el otro verificador pudiera estar usando.
- Que la cobertura del 89.6 % del Capítulo 6 sea la del naïve sobre la TRM con 37 orígenes y h = 12: lo leí en el HTML
  del cap. 6, no lo recalculé.

## 9. Comparación con `R4_cambios.md` (leído al terminar)

**Coincidimos** en: los dos umbrales de raíces y su origen; la retirada de la presa (y en que el deck la conserva, su
punto 4); la regla de 2 puntos como convención; que el quiz dice «regla habitual» (su punto 5, para la R5); los
cambios de prosa de M7–M10 (sus filas 24 a 61); las dos `pendiente` de mi lote y sus motivos; todas las cifras de las `propia`. Su punto 2
(«R. J. Hyndman» en las citas) ya no se ve en mi lote: las citas dicen «Hyndman y Athanasopoulos» y «Hyndman et al.».

**Difiero o añado:**

1. **c4-m7-05.** La cita a Hyndman y Khandakar sobre «menor AICc» (el artículo usa AIC). No lo menciona; es el
   error que el cap. 3 corrigió en c3-m9-20.
2. **c4-m7-10.** El «módulo 1.001» frente a «menor que 1.001»: la ronda dio las dos cifras de umbral pero dejó la de la
   raíz redondeada a tres decimales, y la lectura se invierte. No lo menciona (el bloque ya imprime 1.0009).
3. **c4-m8-10.** Su punto 7 dice solo que las pruebas se ejecutaron sobre log(lynx); no que la cita visible de FPP3
   quede pegada al acuerdo de las tres pruebas, ni la 2.ª fuente irrelevante (Hamilton p. 506), ni el «(sin
   logaritmo)» de la nota.
4. **Bajos que no menciona:** el `tipo` de c4-m8-17; la cita tras el punto en c4-m10-123; «además» en c4-m7-11; «Es
   ruido blanco» (c4-m10-15, la nota sí lo dice); las notas caducas de c4-m8-65 y c4-m10-21; el orden de las fichas de
   Hyndman en las listas; el campo `fuente` del JSON del Nilo (Cobb, cuando `?Nile` da a Durbin y Koopman).
5. **Su lista de cambios** atribuye a «Hamilton (1994, pp. 144–145)» la cercanía OPG–información observada del
   comentario de código: la p. 145 (PDF 160) lo dice. No es prosa visible ni lleva cita; está bien.

## 10. Segunda lectura (2026-11-23)

Releí las 8 entradas que corrigió la sesión maestra (`r4_ediciones_maestra.py`), con el HTML reensamblado de hoy:
`v4B_vuelca.py <id>` y `audita_citas.py --huella <id>`. Las 8 huellas coinciden con `hash_texto`, y los literales están
en su sitio. **Firmo las 8**: las añadí al final de `comprobaciones/v4_firmas_B.txt`.

- **c4-m7-05** · `respaldada`, firmo. «El de menor AICc es el modelo actual (FPP3 §9.7); el artículo original elegía por
  AIC (Hyndman y Khandakar, 2008, p. 11)». Cada cita respalda la parte que tiene pegada: FPP3 §9.7, el AICc; el
  artículo, el AIC. La ayuda (`ic = "aicc"`) queda como fuente adicional. Ya no hay cita sobre lo que la fuente no dice.
- **c4-m7-10** · `propia`, firmo. «…módulo 1.0009, por debajo de los dos umbrales». Repetido en R:
  `Arima(Nile, c(2,1,2))` da 1.0009 (1.000937 en `v4B_software.out` §C), menor que 1.001 y que 1.01.
- **c4-m7-11** · `respaldada`, firmo. «…usa una verosimilitud aproximada (CSS) en lugar de la exacta y al final reajusta
  el ganador con la exacta»: es lo que dice la ayuda (§Arguments, `approximation`).
- **c4-m8-10** · `con-matiz`, firmo. La cita de FPP3 §9.1 va ahora sobre «una serie con ciclos de longitud no fija, como
  la del lince, es estacionaria», que es lo que dice la fuente. Las pruebas ya no llevan cita: son de R y se reproducen
  (§4). Salieron la fuente de Hamilton y el «(sin logaritmo)». El matiz (log(lynx) frente a la serie de FPP3) está bien
  dicho.
- **c4-m10-15** · `respaldada`, firmo. «Es compatible con ruido blanco» es la lectura de FPP3 §9.1, que hace lo mismo con
  una sola barra fuera de los límites. Matiz menor de la nota: FPP3 dice que la ACF «se parece» a la de un ruido blanco
  («looks just like»), y la nota escribe «idéntica». No cambia nada visible.
- **c4-m10-123** · `con-matiz`, firmo. En el HTML, la cita va ahora antes del punto (`…opcional</strong> <cite>…</cite></span>.`).
- **c4-m8-65, c4-m10-21** · firmo. Las notas ya no remiten a c4-m10-56 y ya no piden un cambio en el M7.
- **c4-m8-17** pasa a `tipo: resultado` y conserva su firma: el texto no cambió.
- **Orden de las listas** (`v4B_listas_2.out`, `clave_de_orden`): las 12 listas de módulo, la del capítulo y el pie
  coinciden con lo citado (0 enlaces rotos, `title` = ficha). Ahora el orden es FPP3 (2021) → forecast (2026) →
  Hyndman y Khandakar (2008), por apellidos sucesivos, y la «y» ya no interviene en la comparación.
  Comprobé que la clave compara «…Athanasopoulos, G. (» con «…Athanasopoulos, G., Bergmeir»: el espacio va antes que la
  coma, así que la ficha de dos autores queda primero.
- **c4-m10-15, tercera lectura (2026-11-23)** · firmo otra vez. La nota dice ahora «parecida a la de un ruido blanco»,
  que es lo que dice FPP3 §9.1 («looks just like»). La prosa no cambió y la huella coincide.
