# Capítulo 2 · Afirmaciones que exigen fuente (diagnóstico, 2026-11-16)

Archivo leído: `Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html` (commit `4b71366`): los nueve
módulos, las introducciones de simuladores, la autoevaluación `AUTOEVALUACIONES['cap2']` (8 preguntas), los
cinco ejercicios, las lecturas y el pie. Inventario completo, una fila por afirmación:
`bibliografia/contraste/cap2_inventario.tsv` (136 filas, mismas columnas que el del capítulo 1). No se
inventariaron las cifras que calcula R ni las derivaciones que el capítulo muestra paso a paso (propias).
No se editó nada del capítulo ni del repo salvo esos dos archivos.

## Recuentos

| tipo | alta | media | baja | total |
|---|---:|---:|---:|---:|
| definicion | 4 | 18 | 1 | 23 |
| resultado | 20 | 25 | 0 | 45 |
| regla | 17 | 16 | 6 | 39 |
| dato | 7 | 4 | 2 | 13 |
| atribucion | 11 | 4 | 0 | 15 |
| historica | 1 | 0 | 0 | 1 |
| **total** | **60** | **67** | **9** | **136** |

Pasaje hallado (columna `hallado`):

| prioridad | completo en caché | completo solo en ayuda de R / docstring / metadatos | parcial | no |
|---|---:|---:|---:|---:|
| alta | 24 | 4 | 23 | 9 |
| media | 43 | 5 | 14 | 5 |
| baja | 4 | 0 | 3 | 2 |
| **total** | **71** | **9** | **40** | **16** |

«Completo» = el pasaje respalda la afirmación (28 de 60 en prioridad alta); «parcial:» = respalda la idea
pero no un detalle que se nombra en `donde_buscar`; `no` = nada en lo leído. Las rutas son `ruta:línea`
bajo `bibliografia/_local/` (`texto/<clave>/pNNNN.txt` es página de PDF, no impresa; `web/…`). Los prefijos
`R:`, `py:` y `meta:` señalan ayuda de R, docstring de Python o `referencias.json` leídos en esta sesión: no
están en la caché y habría que registrarlos como instantánea antes de usarlos en un `contraste`. 29 filas
llevan una etiqueta `[CON-MATIZ]`, `[DISCREPA]`, `[ERROR]`, `[LOCALIZADOR…]` o `[TENSIÓN…]` en `donde_buscar`.

## Lo que más pesa (prioridad alta, ordenado por daño al estudiante)

1. **Atribuciones a FPP3 sin pasaje** — `c2-m8-07` («FPP3 hace la misma recomendación», el logaritmo) y
   `c2-m8-10` (misma frase en el quiz). Las secciones extraídas (§3.1, §5.6, §9.x) destacan que el logaritmo es
   interpretable y que un rango de λ cercano al de Guerrero «funciona bien», pero no recomiendan el logaritmo
   frente al óptimo. Retirar o localizar.
2. **Localizadores de lecturas erróneos** — `c2-m9-23`: FPP3 «secc. 3.1–3.2 (transformaciones y Box–Cox)»; la
   3.2 es «Time series components». `c2-m9-24`: Shumway y Stoffer «2.1 (diferenciación)»; en la 3.ª ed. la 2.1
   es «Introduction» y la diferenciación está en la 2.3; la numeración de la 4.ª no se pudo comprobar.
3. **Errores o imprecisiones sobre software** — `c2-m4-09`: `statsmodels` `ywm` no implementa Durbin–Levinson
   (su docstring: Yule–Walker no recursivo, resuelve un sistema Toeplitz por rezago; las «ld/ldb» sí son
   Levinson–Durbin) ni `?pacf` de R nombra esa recursión; `c2-m9-10`: el comentario de Python atribuye a
   `urca::ur.kpss` el truncamiento ⌊3√n/13⌋, que es el que `forecast::ndiffs` impone (el de `ur.kpss` es
   ⌊4(n/100)^¼⌋; la prosa del Módulo 7, `c2-m7-15`, sí es correcta y se comprobó); `c2-m8-09`: que
   `pmdarima.BoxCoxEndogTransformer` sea «el equivalente» del método Guerrero no se pudo comprobar
   (pmdarima no está instalado); `c2-m8-08`: «`statsmodels` no» corrige el sesgo, sin pasaje.
4. **Una afirmación falsa, propia** — `c2-m5-08`: «con la primera diferencia, cualquier φ produce algo que ya se
   parece a ruido blanco». La autocorrelación teórica de ∇y_t en un AR(1) es −(1−φ)/2 (comprobado en R en
   esta sesión): con φ=0.5 vale −0.25, fuera de la banda ±0.139 de T=200; solo se parece a ruido blanco con φ ≳ 0.72.
5. **Reglas de decisión sin fuente** — `c2-m6-07` (ADF y KPSS «ambos no rechazan» = datos poco informativos;
   «ambos rechazan» = contradicción), `c2-m7-08` (el mínimo de varianza señala el d correcto; la repiten
   `c2-m9-07` y `c2-m9-16`), `c2-m6-11` (mecanismo por el que el ADF toma la estacionalidad por
   estacionariedad; solo hay experimentos propios; lo repiten `c2-m9-06` y `c2-m9-17`), `c2-m9-09` (umbral
   |λ|<0.25 para preferir el logaritmo; además choca con «casi siempre se usa el logaritmo» del Módulo 8).
6. **Dato sobre una serie sin ficha** — `c2-m6-08`: la TRM (datos.gov.co, conjunto 32sa-8pi3) no está en la
   biblioteca ni en `instantaneas.yml`.
7. **Las fuentes matizan o contradicen lo escrito** — `c2-m2-02` (Cryer define el ruido blanco como i.i.d.;
   el capítulo sigue a Hamilton y Shumway); `c2-m4-12` (la banda de la PACF es válida bajo un AR(p) en rezagos >p,
   no «bajo ruido blanco» a secas); `c2-m4-11` (FPP3: con p y q positivos, ACF/PACF no identifican los órdenes);
   `c2-m5-12` (Shumway admite que diferenciar también quita una tendencia lineal fija; «quitar la recta a una
   caminata deja residuos no estacionarios» no tiene pasaje) y su tensión con `c2-m3-10` («tendencia o raíz
   unitaria: hay que diferenciar»); `c2-m9-21` («propiedad estructural de la serie»: Hamilton §15.4 sostiene que
   la pregunta es irresoluble con muestra finita); `c2-m8-03` y `c2-m8-11` («exige y>0»: FPP3 y `forecast::BoxCox`
   usan la forma Bickel–Doksum, que admite negativos con λ>0); `c2-m5-11` y `c2-m9-20` («tipos de cambio» como
   caminata «por defecto»/«ejemplo clásico»: FPP3 solo habla de series financieras y de precios e índices bursátiles).
8. **Afirmaciones empíricas generales** — `c2-m9-13` (redes recurrentes y árboles «mucho mejor» con series
   diferenciadas, sin fuente), `c2-m9-12` («la validación cruzada estándar no sirve»; FPP3 §5.10 solo describe
   el origen móvil), `c2-m9-11` (fuga de información).

## Atribuciones que el capítulo hace hoy sin cita

El capítulo no tiene ningún `data-afirma` ni `cite.cita`; todo lo que sigue va sin cita visible.
- A obras: «la recomendación de FPP3» de diferenciar primero por estación (`c2-m7-05`, respaldada en
  `arima.txt:119`); «FPP3 hace la misma recomendación» y el quiz (no respaldadas); las cuatro lecturas y el pie
  (`c2-m9-23` a `c2-m9-26`, `c2-m0-01`; KPSS 1992 y Guerrero 1993 coinciden con los metadatos de la biblioteca).
- A personas o métodos nombrados: Dickey–Fuller y «aumentada» (`c2-m6-04`), Kwiatkowski, Phillips, Schmidt y
  Shin (`c2-m6-05`), Yule–Walker y Durbin–Levinson (`c2-m4-04`, `c2-m4-05`), Guerrero (`c2-m8-04`), Banerjee et al.
  y MacKinnon (`c2-m6-14`), Ljung–Box (`c2-m9-19`), «modelo airline» (`c2-m7-14`), ARCH/GARCH (`c2-m2-04`),
  «regresión espuria» (`c2-m3-14`; Hamilton y Cryer la atribuyen a autores distintos).
- A un estatus: «ejemplo clásico» de los tipos de cambio (`c2-m9-20`); «modelo por defecto» (`c2-m5-11`).

## Obras que faltan

- **En la biblioteca pero sin texto en caché** (hoy no se pueden contrastar): Kwiatkowski et al. 1992
  (`c2-m6-05`, `-06`, `-07`), Guerrero 1993 (`c2-m8-04`, `-12`), Hyndman y Khandakar 2008 (`c2-m6-12`), Box y
  Jenkins 1976 / Box et al. 2015 (`c2-m7-08`, `c2-m7-14`), Brockwell y Davis 2016 (`c2-m3-05`), Banerjee et al. 1993,
  Ljung y Box 1978, Wang, Smith y Hyndman 2006 (el corte 0.64 de `nsdiffs`).
- **Ejemplar equivocado**: Shumway y Stoffer, 4.ª ed. (la que se cita; la caché es la 3.ª y parcial).
- **No están en la biblioteca**: Dickey y Fuller 1979 y Said y Dickey 1984 (ADF); MacKinnon 1994/2010
  (p-valores de `statsmodels`); Box y Cox 1964 (Box–Cox); Granger y Newbold 1974, Phillips 1986, Yule 1926
  (regresión espuria); Engle 1982 y Bollerslev 1986 (solo si se nombran); Venables y Ripley 2002
  (definiciones exactas de `acf`/`pacf`); un texto sobre el contraste conjunto ADF+KPSS; uno sobre raíces
  unitarias con estacionalidad; literatura de aprendizaje automático (redes, árboles, fuga de información);
  literatura sobre tipos de cambio y caminata aleatoria.
- **Datos y software** (colección «4 Datos y software»: hoy solo figura R): TRM de datos.gov.co; manuales de `tseries`,
  `forecast`, `urca`, `fable`, `feasts`; `statsmodels`, `scipy`, `pmdarima` (este último, además, sin instalar).
- **En caché y sin leer**: Hamilton §21.1 (ARCH). **Sin extraer**: los capítulos de FPP3 distintos de 1–5 y 9.

## Hallazgo colateral (no es de fuentes)

La autoevaluación se presenta como «Seis preguntas» (línea 4002) y `AUTOEVALUACIONES['cap2']` tiene ocho.

## Método y límites

Todo pasaje citado se leyó en esta sesión en la caché local; los rangos de línea se comprobaron contra los
archivos. R 4.6.0 (`tseries` 0.10.62, `forecast` 9.0.2 —incluido el código de `ndiffs` y `guer.cv`—,
`urca` 1.3.4); Python con `statsmodels` 0.14.6 y `scipy` 1.15.3. «Hallado» es la lectura de quien inventarió:
según la norma, cada pasaje lo verifica alguien que no lo redactó. Antes de que yo empezara, `bibliografia/instantaneas.yml`
ya estaba modificado; no lo toqué.
