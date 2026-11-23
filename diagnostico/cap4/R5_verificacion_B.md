# Capítulo 4 · R5 (práctica) · verificación independiente B

2026-11-23. Verificador B, de contexto limpio, que no redactó nada de la ronda. Alcance: los ejercicios 1–3
del M10 (`c4e1`–`c4e3`), el quiz `AUTOEVALUACIONES['cap4']`, los minutos declarados, la portada y las
reglas del ensamblado (los nueve «Para practicar» son del verificador A). Base: `HEAD` = `b53fdcb` más el
árbol de trabajo sin commit. Comprobación propia completa **antes** de leer `R5_cambios.md`; después, el
contraste con las dudas del redactor (§4). No se editó el capítulo ni sus fuentes.

**Veredicto: las ocho claves y las cifras salen de R salvo dos (θ̂ y su e.e. en el E1, doble redondeo); hay un error que enseña algo falso (la P5 da por hecho que KPSS deja de rechazar al quitar el escalón de `beaver2`, y no es así), una pista que vuelve a contar la varianza entre las «tres evidencias» y una frase firmada que ahora habla de otra serie: publicable tras corregir 1–6.**

## 1 · Qué se comprobó y cómo

| Comprobación | Resultado | Evidencia |
|---|---|---|
| E1, E2 (liebre y lince), E3 y las ocho preguntas, resueltos con código propio (AICc a mano frente a `Arima()$aicc`, ψ por la forma cerrada frente a `ARMAtoMA`, traza completa de `auto.arima`, MA(1) con y sin media) | Claves correctas; todas las cifras coinciden **salvo** θ̂ = −0.642 (e.e. 0.104) del E1 (c) (hallazgo 4) | `comprobaciones/v5B_m10_quiz.R` · `.out`, `v5B_extra.R` · `.out` |
| P5: KPSS dentro de cada tramo de `beaver2` y distribución nula del KPSS sobre los residuales del escalón (4000 réplicas, semilla 2026) | La afirmación de la retro no se sostiene (hallazgo 1) | `v5B_p5_tramos.R` · `.out` |
| Ayuda de `pelt`, `beaver2` (`beavers`), `aus_airpassengers` y `global_economy` | Lo que dicen los enunciados (qué mide, años, unidades, 10 min, «fuera del refugio») está en la ayuda | `v5B_m10_quiz.out`, `v5B_ayuda.out` |
| Frases marcadas y `<cite>` (BeautifulSoup sobre el HTML ensamblado, `HEAD` frente a ahora) | 286 = 286 ids, **ningún texto cambia**; 252 = 252 `<cite>`, idénticos; cambian de orden c4-m10-151, -66, -150, -67, -68 y -69 | `v5B_afirma.py` · `.out` |
| Simulacro, motor del quiz y del simulacro, preparcial | `SIMULACROS['cap4-simulacro']` y el motor del simulacro idénticos (mismo md5); entre `const AUTOEVALUACIONES` y el quiz solo se añaden `ACF_P6`, `N_P6` y un comentario; todo lo que sigue al quiz, idéntico; `preparcial-corte-2.html` igual a `HEAD` | `v5B_intactos.out` |
| `ensambla_cap4.py` dos veces; luego `_cap5` y `_cap6` | Mismo md5 (`51454d9b…`) las dos veces; caps. 1, 2, 3, 5 y 6 y la portada con el mismo md5 antes y después; `git diff --stat -- Htmls_Series` solo muestra el cap. 4, `index.html` y `README.md`. Nada que restaurar | `v5B_ensamblado.out` |
| Comprobación nueva de `ensambla_cap4.py` (12 `.ejercicio-guiado`, paneles `c4e1-3` y `c4m1-9`) | Correcta y necesaria; ver §4, duda 13 | lectura del diff |
| `verifica_todo.py` | 11 en verde | `v5B_verifica_todo.out` |
| `verifica_bloques_cap6.py --html` sobre el cap. 4 | **1326 de 1326**, 0 discrepancias; sin `URLError` (el «write failed» de la sesión de R ya estaba en las rondas anteriores) | `v5B_bloques.out` |
| `cuenta_sitio.py` | Al día (49 ejercicios; cap. 4: 12 módulos, 11 simuladores, 8 preguntas, 12 ejercicios) | `v5B_cuenta_sitio.out` |
| `audita_posicion_correcta.py` | En verde: orden 2 3 2 4 3 1, reparto 1→1, 2→2, 3→2, 4→1; la múltiple, {1, 3, 4} | `v5B_posicion.out` |
| Longitud de las opciones (texto visible, una fórmula contada por sus símbolos) | La más larga acierta 1 de 6 (P1, empatada con la opción c: 84 y 84); en la múltiple, de las tres más largas solo una es correcta; cociente máx./mín. ≤ 1.26 | `v5B_longitudes.py` · `.out` |
| Minutos (`r3_minutos.py`, paneles abiertos) | Declarado frente a medido: diferencia ≤ 0.5 min en M1–M10; el quiz, 22.8 min (el comentario dice «unos 23») | `v5B_minutos.out` |
| Texto literal de libro en lo que iría a git (7-gramas contra `_local/texto`, `_local/web` y `_local/citas`) | Ninguno; solo coincide la ayuda de R copiada en `r5_ayuda_datasets.out`, que no es un libro | `v5B_literales.py` · `.out` |
| «regla habitual», «consistente», negar la parsimonia | Ninguna retro lo hace: la P1 (c) dice que no diferenciar de más es «una cautela razonable», la P7 habla de convención del capítulo | lectura; `grep` |
| Por HTTP (`python3 -m http.server 8772`, Chrome sin ventana en el CDP 9282), 1200 y 375 px | E1–E3 abiertos con sus botones: 140 fórmulas, 0 errores de KaTeX, 0 «$» sueltos, nada se sale (página 1200/1200 y 375/375). Quiz en cuatro pasadas: todo bien (8 de 8), un fallo y bien (P2 con «5,02»), dos fallos (desglose de la múltiple), y doce valores en la P2. Consola limpia salvo el favicon. Servidor y Chrome cerrados | `v5B_recorrido.js` · `.out`; capturas en `capturas/r5/v5B/` |

## 2 · Hallazgos

Gravedad: **E** error que enseña algo falso o choca con su módulo · **C** cifra · **P** pedagogía · **m** menor.
Líneas de `ensamblado/cap4/templates_10.html` (T) y `ensamblado/cap4/chapter.js` (J).

| # | Dónde | Qué dice | Qué es | Evidencia | Grav. |
|---|---|---|---|---|---|
| 1 | J 1539 (retro de la correcta de la P5) | «Quitado el escalón ($0.81$ °C), KPSS deja de rechazar ($p > 0.10$).» | Falso. Ese $p$ sale de aplicar la tabla ordinaria de KPSS a los residuales de una regresión sobre el escalón, y con el escalón estimado la nula es otra: el estadístico, 0.293, supera el cuantil 95 % de esa nula (0.203 con ruido blanco; 0.255 con un AR(1) de 0.5) y queda cerca del 99 % (0.294 · 0.345). Y dentro de cada tramo KPSS **rechaza** ($p = 0.016$ y $0.022$) y las tres pruebas piden $d = 1$. El redactor lo dejó como duda 1 | `v5B_p5_tramos.out` | **E** |
| 2 | T 903 (pista del E2) | «Las tres evidencias del Módulo 3, por orden. Para la tercera, recuerda…» | Los apartados son (a) pruebas, (b) varianza, (c) raíz MA: leída «por orden», la pista hace de la varianza la segunda evidencia. El M3 (tabla c4-m3-65/-05/-61) y el resumen del M10 (T 710–713) dicen que las tres son el gráfico con la ACF, las pruebas y los síntomas de sobrediferenciar, y que la varianza «no es una evidencia más». Es lo que D3 retiró | lectura de T 690–713 y del M3 | **E** |
| 3 | T 950–951 (E2, a) · `contraste/cap4.yml`, c4-m10-69 | «…la serie es estacionaria, y tiene sentido, porque un ciclo de longitud no fija *sí* vuelve a su media (Hyndman y Athanasopoulos, 2021, §9.1)» | La frase firmada ahora habla de la **liebre**. Su nota dice que se contrastó del lince («que la serie lynx de R sea estacionaria lo dicen las pruebas del bloque»), y FPP3 §9.1 habla de una serie de linces; además, que los ciclos de la liebre no tengan longitud fija no lo dice el enunciado ni la solución. El texto no cambió y `audita_citas` pasa porque la huella es la misma: el cambio de referente no lo ve nadie. El redactor lo señala en su §7 | `v5B_afirma.out`; yml | **m** (fuente; hay que resolverlo antes de publicar) |
| 4 | T 866–867 (E1, c) | «$\hat\phi = 0.880$ (e.e. $0.064$) y $\hat\theta = -0.642$ (e.e. $0.104$)» | Doble redondeo desde lo impreso a cuatro decimales ($-0.6415$, $0.1035$). Con `arima(method = "ML")`, que es lo que usa el bloque, $\hat\theta = -0.64148$ y e.e. $0.10348$: a tres decimales, $-0.641$ y $0.103$ | `v5B_m10_quiz.out` («ar1 ma1 se.ar1 se.ma1»), `v5B_extra.out` | **C** |
| 5 | J 1446–1448 (P2) | Pista: «Conserva al menos tres decimales en los pasos intermedios»; `respuesta: 5.02`, `tolerancia: 0.006` | Quien sigue la pista puede salir de la tolerancia: $\psi_2^2 = 3.0625 \to 3.063$ da $2\sqrt{6.313} = 5.0251 \to 5.03$; $\sqrt{6.313} \to 2.513$ da $5.026$. Por HTTP se rechazan $5.026$ y $5.03$, y se aceptan $5.0251$, $5.025$ y $5.014$. El valor exacto, $5.02494$, cae a cinco milésimas del borde del redondeo: es «la tolerancia que castiga el redondeo» | `v5B_m10_quiz.out` §P2; `v5B_recorrido.out`, pasada D | **P** |
| 6 | T 1050 (bloque del E3) | `# --- (c) <U+00BF>crece como una caminata aleatoria? ---` | El «¿» del guion (`r5_bloques/e3.R`, l. 21) salió escapado al pasar por la sesión de R, y la página muestra «<U+00BF>» | `grep 'U+00BF'` (única aparición en el capítulo) | **m** |
| 7 | T 903–904, 950–970 (E2) frente al aviso del M8 (`templates_7_9.html` 396–402) | — | El E2 cambió de serie, pero el aviso del M8 sigue resolviendo el patrón completo sobre el lince, el depredador de la liebre, con los mismos años y la misma compañía: las tres pruebas piden $d = 0$, la varianza cae y no decide, $\hat\rho_1$ de la diferencia no avisa, y el ARIMA($2,1,1$) da la raíz MA en 1.000. Solo (c, «por qué no todos») y (d) son nuevos, y la pista de (c) remite a la práctica del M8 que los resuelve. D9 pedía retirar o mover esa frase; el redactor la dejó (duda 3) | lectura | **P** |
| 8 | T 1012–1013 (pista del E3) y J 1446 (pista de la P2) | «Los $\psi$ no salen del ARIMA directamente: hay que expandirlo primero como el ARMA($2,1$)» | Choca con el apartado (a) del propio E3 («con la forma cerrada del Módulo 9 y antes de expandir nada») y con el M9 (c4-m9-13), que da $\psi_j = [(1+\theta) - (\phi+\theta)\phi^{\,j}]/(1-\phi)$ para el ARIMA($1,1,1$) sin expandir nada (y con $\theta = 0$, la de la P2). Comprobado: la forma cerrada y `ARMAtoMA` difieren en $2\times10^{-15}$ | `v5B_m10_quiz.out` §E3 | **P** |
| 9 | T 1085–1086 (E3, d) | «$t = 1.56$ no es significativa y **empeora el AICc** ($515.06$ frente a $514.90$)» | 0.16 puntos. La práctica del M9 (`templates_7_9.html` 1002) trata 1.45 puntos como «menos de los 2 que este capítulo toma por convención como indistinguibles»; aquí la misma clase de diferencia se lee como empeorar | `v5B_m10_quiz.out` («dif 0.1599648») | **P** |
| 10 | J 1560 (P6), J 1620 (P8), T 779–780 (pista del E1, d) | P6: «…repasa el primer párrafo del Módulo 4»; P8: «…así que la respuesta no está ahí. Repasa qué más enseña a comprobar el Módulo 8»; E1: «antes de mirar ningún AICc pregúntate sobre qué datos se calcula cada uno» | Dan el criterio: el primer párrafo del M4 dice que la ACF sin diferenciar «no informa sobre $p$ ni sobre $q$»; la de la P8 descarta la opción b y señala las raíces; la del E1 es la respuesta de su segunda lección (y la de la P1). Con el motor, que cuenta el segundo intento como acierto, inflan el resultado | lectura del M4; `v5B_recorrido.out`, pasada B | **P** (m) |
| 11 | T 1073–1088 (E3) frente a la práctica del M9 (`templates_7_9.html` 945–1002) | — | El E3 repite, apartado por apartado, la práctica del M9 sobre `BJsales.lead`: forma cerrada y $\psi_\infty$, intervalo frente a `forecast()`, cociente frente a la caminata, deriva. Lo único nuevo es que $\phi \ne 0$. La frase del M9 con las cifras sí se fue | lectura | **m** |
| 12 | T 869–874 (E1, d) · c4-m10-65 | «La primera: un criterio de información no sustituye al diagnóstico (§9.7). El mejor modelo con $d = 2$… residuales sin estructura… y, sin embargo, una raíz MA de módulo $1.000$» | La frase firmada se contrastó como «no sustituye a la **comprobación de los residuales**» (campo `afirmacion` de c4-m10-65, que no lleva nota), y el ejemplo nuevo es uno en que los residuales **pasan** y lo que falla son las raíces. El texto lo dice («Ni el AICc ni Ljung–Box lo delatan; las raíces, sí»), pero la cita queda ilustrando una lección más amplia que la contrastada | yml; lectura | **m** |
| 13 | yml: c4-m10-67 y c4-m10-150 | Notas «Con r1 = 0.785 … el medido en log(lynx)» (-67) y «El AR(2) que el ejercicio ajusta a log(lynx)…» (-150) | La -67 está ahora en el apartado de la liebre (es general y sigue siendo cierta: $r_1 = 0.666$, cociente $0.673$ frente a $2(1-r_1) = 0.669$). La -150 se apoya en un AR(2) del lince que ya no está en la página (sigue en `r4_software/lectorF/sigma2_y_lince.R`) | `v5B_m10_quiz.out` §E2 | **m** |
| 14 | J 1417 (P1) | «el mejor ARIMA de la rejilla con $d = 1$ tiene AICc $= 204.28$» | Es el mejor **sin constante** (la convención del M6). En una serie que crece así, el M5 manda decidir la deriva; con deriva, el mejor de $d = 1$ es el ARIMA($0,1,0$) con 200.59, a 2.27 del de $d = 2$. La clave no cambia | `v5B_m10_quiz.out` §P1 | **m** |
| 15 | J 1602 (retro de la P7, b) | «…es el mejor de los $42$ modelos probados según el AICc» | De los 42 de la traza, 27 dan AICc infinito (descartados); el mínimo lo es entre 15 | `v5B_extra.out` (traza) | **m** |
| 16 | J 1619, 1625 (P8) | «Un MA(1) ajustado a $\nabla y_t$ da $\hat\theta = -0.288$… ($p = 0.43$)… $p = 0.17$»; «el $\hat\sigma^2$ de ese MA(1) es $5.12$, la varianza de $\nabla y_t$» | Las cifras son de un MA(1) **sin media** y Ljung–Box sobre sus 57 y 56 residuales. Con `arima()` por defecto sobre la serie diferenciada: $-0.289$, $\hat\sigma^2 = 5.108$, $p = 0.16$; con ARIMA($0,d,1$) y los residuales que devuelve `residuals()` (como hace el E1): $p = 0.42$ y $0.15$. La clave no cambia | `v5B_m10_quiz.out` §P8, `v5B_extra.out` | **m** |
| 17 | T 961–962 (E2, d) | «El AR(4), que es el que elige `auto.arima`» | Lo elige la búsqueda exhaustiva (la del bloque); `auto.arima` por defecto da ARIMA($2,0,2$) | `v5B_m10_quiz.out` («por defecto: ARIMA(2,0,2)») | **m** |
| 18 | J 1449 (retroAcierto de la P2) | «Una caminata aleatoria con la misma $\sigma$ daría $2\sqrt{3} = 3.46$: aquí los pesos pasan de $1$ y la incertidumbre crece más deprisa.» | Adelanta la conclusión de E3 (a) y (c). El M9 ya lo dice en general (T 758 de `templates_7_9.html`), así que no regala cifras | lectura | **m** |

Fuera del alcance (motor, sin cambio en la ronda): tras acertar todo al segundo intento, «Resultado: 8 de 8 ·
impecable» junto a «Te costaron preguntas de estos módulos» (`v5B_recorrido.out`, pasada B); ya anotado en el cap. 3.

Lo que está bien y conviene no tocar: E1 ya demuestra sus dos lecciones (el IMA es 8.º de 9 por AICc, a
18.4 del mejor, y el texto lo dice; la trampa entre $d$ muerde con 17.489 puntos; el ARIMA($1,2,2$) es
$(1-B)(1-0.625B)$, verificado: $1 + \text{ma}_1 + \text{ma}_2 = 3\times10^{-7}$ y lo que queda es un
ARIMA($1,1,1$) con $\phi = 0.860$, $\theta = -0.625$). El E3 ya no se responde con la nota del M9. Las
claves de las ocho preguntas, las tolerancias de la P2 frente a sus siete tropiezos, la ACF de la P6
(`ACF_P6` = R a tres decimales) y la traza de la P7 (1.53, 1.94; el cuarto a 2.86) son correctas.

## 3 · Correcciones propuestas (exactas)

**1 (P5).** J 1539, `retro` de la correcta:
«Con el salto dentro, las pruebas no separan una raíz unitaria de un cambio de nivel (Módulo 3). Quitado el escalón ($0.81$ °C), KPSS deja de rechazar ($p > 0.10$). Lo que queda sigue muy autocorrelacionado ($r_1 = 0.78$), así que la discusión sobre $d$ no termina ahí; pero ya es sobre la serie, y no sobre el salto.»
→ «Con el salto dentro, las pruebas no separan una raíz unitaria de un cambio de nivel (Módulo 3). Quitado el escalón ($0.81$ °C), lo que queda sigue muy autocorrelacionado ($r_1 = 0.78$), y probadas en cada tramo, a un lado y otro de la lectura 39, las tres pruebas siguen pidiendo una diferencia: la discusión sobre $d$ no termina ahí, pero ya es sobre la serie, y no sobre el salto.»
(Cifras en `v5B_p5_tramos.out`: `ndiffs` 1/1/1 en los dos tramos; llevarlas a `r5_cifras.R` como `[P5-04]`.)

**2 (pista del E2).** T 903–904:
«Las tres evidencias del Módulo 3, por orden. Para la tercera, recuerda qué necesitaba el modelo de la práctica del Módulo 8 para que la firma apareciera.»
→ «Para (a) y (c), la segunda y la tercera evidencia del Módulo 3; para (b), lo que advierte el Módulo 2.7 sobre la varianza. Para (c), piensa qué parte del modelo tiene que recoger el ciclo antes de que el término MA pueda delatar algo.»

**3 (c4-m10-69).** Dos salidas; recomiendo la (a):
- (a) Mantener el texto y rehacer la entrada del yml: `nota` → «FPP3 §9.1 respalda el principio (la serie cíclica sin tendencia ni estacionalidad es estacionaria) sobre una serie de linces; aquí se dice de `log(pelt$Hare)`, cuya estacionariedad dan las tres pruebas del bloque del ejercicio (R 4.6.0: `ndiffs` 0/0/0) y cuyos ciclos no tienen longitud fija (separación entre máximos locales de 2 a 11 años; periodo del AR(2) 10.65, `v5B_m10_quiz.out`). "Vuelve a su media" es la lectura del capítulo.» Veredicto `con-matiz`, y la firma de alguien que no la redactó.
- (b) Si no se quiere abrir el registro: T 950–951 → «<strong>(a)</strong> Las tres pruebas coinciden en $d = 0$: según las tres, la serie es estacionaria.», y llevar el `<span data-afirma="c4-m10-69">…</span>` (texto intacto) al párrafo del lince, tras «las tres pruebas piden $d = 0$».

**4 (E1).** T 866–867: «$\hat\theta = -0.642$ (e.e. $0.104$)» → «$\hat\theta = -0.641$ (e.e. $0.103$)». Añadir a `r5_cifras.R` la etiqueta `[E1-03]` con `round(c(coef(f111), sqrt(diag(f111$var.coef))), 3)`.

**5 (P2).** J 1448: `tolerancia: 0.006` → `tolerancia: 0.011` (acepta de 5.009 a 5.031: 5.02, 5.026, 5.03; sigue rechazando 5.00 y los otros seis tropiezos, el más cercano a 0.02). Alternativa sin tocar la tolerancia: J 1446, «Conserva al menos tres decimales en los pasos intermedios.» → «Conserva al menos cuatro decimales en los pasos intermedios.» (con cuatro, $3.0625$ y $6.3125$ son exactos y sale $5.0249 \to 5.02$).

**6 (E3, bloque).** `r5_bloques/e3.R` y `e3.out`, y T 1050: `# --- (c) &lt;U+00BF&gt;crece como una caminata aleatoria? ------------------------------` → `# --- (c) crece como una caminata aleatoria? -----------------------------------` (o asegurar que `r5_reprex.R` escribe en UTF-8 y volver a pasar el bloque). Volver a correr el verificador de bloques.

**7 (E2 y el M8).** Decisión de Javier. O se acepta como transferencia (las cifras no están en el M8, y (c) y (d) añaden), y entonces basta la corrección 2; o se cumple D9 a la letra moviendo el tramo del lince del aviso del M8 (`templates_7_9.html` 397–402, con c4-m8-10, -11 y -61 intactas) detrás del E2 y dejando en el M8 solo c4-m8-60 y «El ejercicio 2 lo pone a prueba en una serie con ciclos.»; eso exige rehacer las anclas `#ref-m8-…` y volver a firmar las tres. Recomiendo lo primero.

**8 (pistas del E3 y la P2).** T 1012–1013: «Los $\psi$ no salen del ARIMA directamente: hay que expandirlo primero como el ARMA($2,1$) del Módulo 1, con $\phi^{*} = (1+\phi,\ -\phi)$.» → «Los $\psi$ salen de la forma cerrada del Módulo 9, o de expandir el modelo como el ARMA($2,1$) del Módulo 1, con $\phi^{*} = (1+\phi,\ -\phi)$: las dos vías dan lo mismo.» J 1446: «Los pesos $\\psi$ no salen del ARIMA directamente: escríbelo primero sobre $y_t$…» → «Para los pesos $\\psi$, escribe primero el modelo sobre $y_t$…».

**9 (E3, d).** T 1085–1086: «no es significativa y empeora el AICc ($515.06$ frente a $514.90$), aunque…» → «no es significativa, y el AICc no la distingue ($515.06$ con ella, $514.90$ sin ella: $0.16$ puntos, muy por debajo de los $2$ que este capítulo toma por convención), aunque…».

**10 (pistas).** J 1560: «…mira la forma en que bajan, y repasa el primer párrafo del Módulo 4.» → «Antes de contar barras, mira la forma en que bajan.» J 1620: «Los dos modelos pasan el diagnóstico de residuales, así que la respuesta no está ahí. Repasa qué más enseña a comprobar el Módulo 8.» → «Los dos modelos pasan Ljung–Box. Repasa todo lo que el Módulo 8 enseña a mirar en un modelo ajustado.» T 779–780: «Y para (d), antes de mirar ningún AICc pregúntate sobre qué datos se calcula cada uno, y recuerda que diagnosticar no es solo mirar los residuales.» → «Y para (d), mira la fórmula del AICc antes de comparar, y recuerda que diagnosticar no es solo mirar los residuales.»

**11 (E3 frente a M9).** Opcional: quitar del E3 el apartado (d) (la deriva ya la practica el M9) o cambiarlo por la comparación con un ARIMA($0,1,1$) de `BJsales`, cuyos ψ son constantes.

**12 (c4-m10-65).** Sin tocar la marca ni el texto de la página: añadir a la entrada del yml una `nota` que diga «En el E1 (desde la R5) la lección se ilustra con un modelo cuyos residuales pasan y cuyas raíces no: el diagnóstico del capítulo incluye las raíces (resumen del M10)», y que la firme alguien que no la redactó.

**13 (notas del yml).** c4-m10-67: añadir «Desde la R5 la frase está en el apartado de la liebre: $r_1 = 0.666$, cociente $0.673$, $2(1-r_1) = 0.669$ (`r5_bloques/e2.out`).» c4-m10-150: «El AR(2) que el ejercicio ajusta» → «El AR(2) de log(lynx) (ya no se imprime en la página; comprobación en…)».

**14 (P1).** J 1417: «el mejor ARIMA de la rejilla con $d = 1$» → «el mejor ARIMA sin constante de la rejilla con $d = 1$», y lo mismo para $d = 2$.

**15 (P7).** J 1602: «el mejor de los $42$ modelos probados según el AICc» → «el mejor según el AICc de los que la búsqueda pudo ajustar».

**16 (P8).** J 1619: «Un MA(1) ajustado a $\\nabla y_t$» → «Un MA(1) sin media ajustado a $\\nabla y_t$».

**17 (E2, d).** T 961–962: «El AR(4), que es el que elige <code>auto.arima</code>,» → «El AR(4), que es el que elige la búsqueda exhaustiva de <code>auto.arima</code>,».

**18 (P2).** Opcional: quitar de J 1449 «Una caminata aleatoria con la misma $\\sigma$ daría $2\\sqrt{3} = 3.46$: aquí los pesos pasan de $1$ y la incertidumbre crece más deprisa.»

Tras corregir: reensamblar, `verifica_bloques_cap6.py`, `verifica_todo.py`, `audita_posicion_correcta.py` (si
cambia la P5 no cambia la posición) y la P2 por HTTP con 5.026 y 5.03.

## 4 · Respuestas a las dudas del redactor que caen en esta parte (§7 y §8 de `R5_cambios.md`)

- **1 (`beaver2`).** La duda era fundada y es peor de lo que dice: no es solo que los valores críticos «no
  son exactamente los de la prueba»; con los correctos, KPSS **rechaza** sobre los residuales del escalón
  (0.293 frente a un 95 % de 0.20–0.26), y rechaza en cada tramo. Hallazgo 1. La pregunta sirve; la retro
  tiene que dejar de afirmar que KPSS deja de rechazar.
- **3 (la caja del lince en el M8).** Es exposición, pero resuelve el E2 por analogía: la liebre es la presa
  del lince, de la misma compañía y los mismos años, y el patrón es idéntico. Hallazgo 7; decisión de Javier.
- **4 (el párrafo final del lince en el E2).** Aceptable: es la exposición del M8 con su bloque, y conserva
  cinco marcas sin cambiar de serie (c4-m10-151, -66, -150, -68, -70 siguen hablando del lince). Lo que no
  conserva su serie es la c4-m10-69 (hallazgo 3), y la nota de la -150 quedó sin bloque (hallazgo 13).
- **5 (paquetes).** Sin problema: `tsibbledata` en el E2, y `fpp3::aus_airpassengers` solo detrás de las cifras de la P1.
- **9 (P1 y la parsimonia).** Bien resuelto: la retro de (c) reconoce la cautela y dice por qué no sale de
  esa comparación. Lo que falta es «sin constante» (hallazgo 14).
- **10 (P6 y P7 con la misma serie).** Aceptable: la retro de la P6 no adelanta la clave de la P7, y la P7
  dice que es la misma serie.
- **11 (P8 deja de ser numérica).** Aceptable; la única numérica (P2) es la que necesita la corrección 5.
- **12 (pistas que remiten a un módulo).** P1 y P7 orientan sin decir el criterio; P6 y P8 lo dan (hallazgo 10).
- **13 (`ensambla_cap4.py`).** La comprobación es correcta (cuenta 12 `.ejercicio-guiado` exactos y un
  `id` por panel en los doce) y sin ella el ensamblado aborta: no veo motivo para revertirla. Solo no
  comprueba que cada `c4mN` esté en la plantilla del módulo N; opcional.
- **14 (P4, «se aplana»).** Aceptable: «se aplana en un nivel, que puede no ser el último dato» es cierto
  a largo plazo también con raíces complejas; el vaivén es transitorio.
- **§7 (c4-m10-67 y -69).** La -67 es general y sigue siendo cierta de la liebre (actualizar la nota,
  hallazgo 13); la -69 no, porque su cita y su nota hablan del lince (hallazgo 3).

Las dudas 2, 6, 7 y 8 son de los «Para practicar» (verificador A).

## 5 · Guiones de esta verificación (`diagnostico/cap4/comprobaciones/`)

`v5B_m10_quiz.R` · `.out` (E1–E3, el lince, las ocho preguntas, ayuda de `pelt` y `beavers`) · `v5B_extra.R` · `.out`
(traza de la P7, Ljung–Box de la P8, θ̂ del E1 a tres decimales) · `v5B_p5_tramos.R` · `.out` (KPSS por tramos y
nula con escalón) · `v5B_ayuda.R` · `.out` · `v5B_afirma.py` · `.out` · `v5B_longitudes.py` · `.out` ·
`v5B_literales.py` · `.out` · `v5B_recorrido.js` · `.out` · `v5B_intactos.out` · `v5B_ensamblado.out` ·
`v5B_verifica_todo.out` · `v5B_bloques.out` · `v5B_posicion.out` · `v5B_cuenta_sitio.out` · `v5B_minutos.out`.
Capturas (ignoradas por git): `diagnostico/cap4/capturas/r5/v5B/`.

## 6 · Segunda lectura (2026-11-23, tras la §10 de `R5_cambios.md`)

Mismas reglas; sin editar el capítulo ni sus fuentes. Única escritura fuera de `v5B_*`: `comprobaciones/v5_firmas_B.txt`.

**Veredicto: las correcciones de mi parte están aplicadas y son correctas, sin daños colaterales; firmo las tres entradas rehechas. Queda un detalle menor (hallazgo 19) y, en `verifica_todo`, dos fallos que se resuelven al aplicar las firmas y regenerar `uso_fuentes.json`.**

### Qué se comprobó

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Frases marcadas y `<cite>` (`HEAD` frente a ahora) | 285 ids (falta solo c4-m10-69, retirada) y 251 `<cite>` (falta solo el suyo, FPP3 §9.1); ningún texto cambia | `v5B_afirma_2.out` |
| `audita_citas.py` antes de firmar | Falla **solo** por `[F08] c4-m10-65: falta verificado_por` | `v5B_audita_citas_2.out` |
| `ensambla_cap4.py` dos veces, luego `_cap5` y `_cap6` | Mismo md5 (`35af4f15…`) las dos veces; caps. 1–3, 5, 6 y portada con el md5 de antes | `v5B_ensamblado_2.out` |
| Verificador de bloques | **1347 de 1347**, 0 discrepancias | `v5B_bloques_2.out` |
| `verifica_todo.py` | 9 de 11; fallan `audita_citas` (la firma de c4-m10-65, aún sin aplicar) y `--uso-comprobar` (`uso_fuentes.json` desfasado tras retirar c4-m10-69: hay que correr `audita_citas.py --uso` después de aplicar las firmas) | `v5B_verifica_todo_2.out` |
| Minutos | Abierto/declarado entre 0.97 y 1.03 en M1–M10; quiz, 22.8 min | `v5B_minutos_2.out` |
| Longitudes del quiz | Las mismas que en la primera lectura (ningún texto de opción cambió) | `v5B_longitudes_2.out` |
| Por HTTP (8774, CDP 9284), 1200 y 375 px | M8 (con el bloque del lince nuevo, coloreado, sin desborde) y M10: 0 errores de KaTeX, 0 «$» sueltos, nada se sale; «U+00» ya no aparece; el E3 tiene (a)–(c); quiz en las cuatro pasadas; P2: aceptados 5.02, 5,02, 5.01, 5.009, 5.026 y 5.03; rechazados 5.0089, 5.031, 5.032, 5.04, 5.00, 4.99 y 5. Consola limpia salvo el favicon. Servidor y Chrome cerrados | `v5B_recorrido_2.js` · `.out`; capturas en `capturas/r5/v5B_2/` |

**La P2 y el 5.01 (pregunta 2 de la maestra).** No es el resultado de ningún tropiezo: los de la lista son 2.29 ($\psi_j = \phi^j$), 3.46 (caminata), 4.61 (sin $\psi_0$), 4.12 (sin cuadrados), 6.27 (un peso de más), 2.51 (sin $\sigma$) y 5.00 (raíz redondeada a 2.5), más 12.62 (sin la raíz). El más cercano al intervalo aceptado [5.009, 5.031] es 5.00, que sigue fuera. Aceptar 5.01 no deja pasar ningún error identificado.

### Hallazgos nuevos

| # | Dónde | Qué dice | Qué es | Grav. |
|---|---|---|---|---|
| 19 | `templates_10.html`, último párrafo de la solución del E2 | «Todas estas cifras son las del bloque que sigue al aviso "La columna de la varianza no decide $d$" del Módulo 8.» | El párrafo también da «1821–1934» (de la ayuda) y «unos 10 años» (c4-m10-150, que **no** sale de ese bloque: su AR(2) no se imprime en ninguna parte) | **m** |

Corrección exacta: «Todas estas cifras son las del bloque…» → «Las cifras de las pruebas, de la varianza, de $r_1$ y del ARIMA($2,1,1$) son las del bloque…».

### Estado de los hallazgos de la primera lectura

| # | Estado |
|---|---|
| 1 · P5, KPSS sin escalón | **Resuelto.** La retro dice que en cada tramo las tres pruebas siguen pidiendo una diferencia (`[P5-04]`: 1 1 1 y 1 1 1, como en `v5B_p5_tramos.out`); la cuarta opción ya no da por hecho que el salto explica el rechazo |
| 2 · pista del E2 | **Resuelto.** Remite al M3 para la varianza, y el M3 dice que «no decide $d$» (c4-m3-60) |
| 3 · c4-m10-69 | **Resuelto** con la retirada: la liebre dice «según las tres, la serie es estacionaria», y el lince conserva la c4-m10-68 con la misma cita. Las demás marcas del lince (151, 66, 150, 68, 70) siguen hablando del lince |
| 4 · θ̂ del E1 | **Resuelto**: −0.641 (e.e. 0.103), `[E1-03]` |
| 5 · tolerancia de la P2 | **Resuelto**: 0.011 (ver arriba) |
| 6 · `<U+00BF>` | **Resuelto**: 0 apariciones; el bloque del E3 dice «¿crece…» |
| 7 · E2 frente a la caja del M8 | Sin cambio, aceptado como transferencia (decisión de Javier) |
| 8 · pistas del E3 y la P2 | **Resuelto** |
| 9 · «empeora el AICc» | **Desaparece** con el apartado (d) del E3; la respuesta y el bloque del E3 ya no hablan de deriva |
| 10 · pistas P6, P8, E1 (d) | **Resuelto**; las tres ya no dicen el criterio |
| 11 · E3 frente a la práctica del M9 | **Resuelto**: la práctica del M9 es ahora otra (`austres`; la revisa el verificador A) |
| 12 · c4-m10-65 | **Resuelto** con la nota nueva; firmada |
| 13 · notas de -67 y -150 | **Resuelto**; firmadas |
| 14–18 · P1, P7, P8, E2 (d), retro de la P2 | **Resueltos** con la redacción propuesta |

### Firmas

Leí, para cada entrada, el pasaje en la caché y comprobé las cifras de su nota:

- **c4-m10-65** (respaldada): `_local/web/hyndman2021forecasting/arima.txt` l. 450–461, el procedimiento de modelado de FPP3 §9.7: el paso 5 usa el AICc y el paso 6, aparte, comprueba los residuales; «The Hyndman-Khandakar algorithm only takes care of steps 3–5». Los dos literales de `_local/citas/cap4.yml` están en el pasaje (el primero, con la huella `6c28c917…` del registro). La nota dice bien que el E1 ilustra con las raíces algo más amplio que el pasaje y que la frase solo afirma la parte respaldada; sus cifras (Ljung–Box del ARIMA(1,2,2) $p = 0.565$, raíz MA 1.000) coinciden con `v5B_m10_quiz.out`.
- **c4-m10-67** (propia): la identidad $\operatorname{Var}(\nabla y) = 2(1-\rho_1)\operatorname{Var}(y)$ en una serie estacionaria es correcta; las cifras de la nota (0.666, 0.669, 0.673) son las de `r5_bloques/e2.out` y de mi `v5B_m10_quiz.out`.
- **c4-m10-150** (propia): las cifras de la nota (φ 1.3776 y −0.7399; periodo 9.7839 por la raíz y 10.0236 con la fórmula; $\phi_1^2 + 4\phi_2 = -1.0617$) son las de `r4_software/lectorF/sigma2_y_lince.out`, sección 2, y la fórmula del periodo medio es la de FPP3 §9.5 (`arima.txt` l. 328). La nota dice ya que ese AR(2) no se imprime en la página.

Las tres van en `diagnostico/cap4/comprobaciones/v5_firmas_B.txt`, una por línea. Falta que la sesión maestra las aplique (`r4_firmas.py`, que no corrí) y regenere `uso_fuentes.json`.
