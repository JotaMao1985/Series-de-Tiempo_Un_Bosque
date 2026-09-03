---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-09-02
estado: ejecutado
---

# Plan — Auditoría módulo por módulo del Capítulo 3

**Objetivo:** corregir los seis errores factuales y los cuatro bloques de código que no
hacen lo que dicen, detectados al revisar los diez módulos y contrastar **todas** las
cifras contra R 4.6.0 y statsmodels 0.14.6.

**Alcance:** ortografía, redacción, narrativa, gráficos, pertinencia y funcionamiento de
los simuladores. Nada de contenido nuevo.

## 1. El hueco

El capítulo está en muy buen estado: la ortografía es impecable (cero faltas en 2.937
palabras de prosa), los diez simuladores funcionan, y **la mayoría de las cifras
reproducen exactamente**. Lo que falla son puntos concretos, casi todos en el tramo
7–9, donde el material entró en terreno de datos reales.

| # | Dónde | Qué falla | Cómo se detectó |
|---|---|---|---|
| C1 | M9, bloque R | Salida `intercept 6.9903`; R da **6.3317** | `arima(sqrt(manchas), c(2,0,0))` |
| C2 | M9, intro TRM | «la única barra que asoma es el rezago 5» — hay **dos** | El propio simulador dice «2 de 20» |
| C3 | M8, nota | «las mayores son 0.1297 y −0.1477» — son **0.1839 y 0.1718** | `acf(residuals(ar2), lag.max=20)` |
| C4 | M8, derivación LB | «la varianza de $\hat r_k$ … **crece** con $k$» — **decrece** | $\operatorname{Var}(\hat r_k)\approx (T-k)/(T(T+2))$ |
| C5 | M7, tabla | Pseudo-periodo CSS $10.74$; es **10.71** | $2\pi/\arccos(\cdot)$ con $(1.4032,-0.7099)$ |
| C6 | M8, tabla-ranking | «Los **ocho** candidatos» — muestra **once** filas | Lectura del componente en el navegador |
| C7 | M7, bloque Python | `method="statespace"` es ML, no CSS | Da $(1.4059,-0.7111)$, idéntico a `ml` |
| C8 | M8, bloque R | `expand.grid(p=0:2, q=0:2)` no genera el AR(3) de la tabla | Genera MA(1) y ARMA(1,2), que la tabla omite |
| C9 | M5, bloque Python | Última línea es un residuo del M4 | `arma_acf` de $\phi=0.7,\theta=0.5$ |
| C10 | M9, bloque R | `order(fecha) & fecha >= …` **no ordena** | `order()` da índices; `&` los coacciona |

Y seis puntos de precisión menor: C11 «CSS y ML coinciden hasta la tercera cifra» (falso
para $\phi_2$), C12 la $\lambda$ de Guerrero se **estima** sobre la serie desplazada pero
se **aplica** sobre la original sin decirlo, C13 el BIC del AR(3) sale como `848.90` en dos
sitios y `848,91` en un tercero, C14 «autocorrelaciones del mismo signo» sugiere que el
signo interviene en $Q$, C15 «el óptimo está en $\theta=1$ y vale $|\rho_1|\le 1/2$» mezcla
valor y cota, C16 «el AR(2) tiene tres parámetros» frente al $k=4$ del AICc del M8.

## 2. Restricciones verificadas antes de planear

- **`ensamblado/ensambla_cap3.py` regenera el capítulo 3 partiendo del capítulo 2** y
  sobrescribe `Htmls_Series/capitulo-3-modelos-ar-ma-arma.html`. No hay carpeta
  `ensamblado/cap3/`, pero el script generador existe: cualquier corrección hecha a mano
  se pierde si se reejecuta. Además `ensambla_cap4.py` **lee el capítulo 3 como base**.
  → Reflejar en el script toda corrección que caiga dentro de una región que él sustituya.
- Las cifras del capítulo salen de `precalculo/genera_cap3.R` y viajan embebidas en
  `DATOS_CAP3`. C13 y las cifras del §4 exigen **regenerar**, no editar a mano.
- Verificado por HTTP (`preview_start {name:"htmls-series"}`), no por `file://`.

## 3. Decisiones de esta ronda

- **D1.** La prosa manda sobre el bloque de código cuando discrepan y la prosa es la
  correcta (C1: la fórmula con $6.33$ se queda; se arregla la salida comentada).
- **D2.** C7 y C8 se arreglan haciendo que el código **produzca la tabla**, no recortando
  la tabla. En Python no hay CSS en la API nueva de `ARIMA`: se declara explícitamente y
  se muestra la alternativa (`ARMA` está retirado), en vez de fingir que lo hay.
- **D3.** C11 se reescribe en la unidad que el propio párrafo ya estableció —errores
  estándar— en vez de en «cifras»: CSS y ML distan $0.04$ y $0.02$ e.e.
- **D4.** C2 y C3 se aprovechan: dos barras fuera de veinte **refuerzan** el argumento de
  la regla del 5 % en vez de debilitarlo, y $0.1839$ frente a una banda de $0.196$ es un
  ejemplo mejor de por qué hace falta Ljung–Box que $0.1477$.
- **D5.** La voz (2.ª persona en prosa expositiva) queda **fuera** de esta ronda: es una
  decisión de registro para los seis capítulos, no un error del 3.

## 4. Cifras verificadas en R antes de escribir

```
AR(2) manchas 1770-1869, tres métodos
  YW   phi=(1.3173, -0.6338)  var.pred=298.9642  periodo=10.5334
  CSS  phi=(1.4032, -0.7099)  sigma2 =229.0314   periodo=10.7085   <- tabla dice 10.74
  ML   phi=(1.4059, -0.7111)  sigma2 =229.4284   periodo=10.7369
       intercept=48.2616  e.e.=(0.0706, 0.0702, 4.9751)            <- HTML: 48.2642 / 4.9747

AR(2) sobre sqrt(manchas)
  coef = (1.4027, -0.6853, 6.3317)   e.e. = (0.0727, 0.0724, 0.4101)
  Python: const = 6.3316                                           <- HTML dice 6.9903

ACF residual del AR(2), 20 rezagos, banda 0.196
  mayores: 0.1839 (k=11), 0.1718 (k=9), 0.1590 (k=4)   0 fuera de banda
                                                                   <- HTML: «0.1297 y -0.1477»
BIC AR(3) = 848.905212                                             <- HTML: 848.90 / 848,91

ACF log-retornos TRM, banda 0.1675
  k=5:  0.193  FUERA
  k=8: -0.198  FUERA                                               <- HTML: «la única barra»

Guerrero  lambda = 0.3062
  manchas^lambda        -> periodo 11.3883  LB12 0.4892   (las del HTML)
  (manchas+1)^lambda    -> periodo 11.2759  LB12 0.2216
```

Reproducen **exactamente**: todo el módulo 1 al 6, la rejilla del 8, la rejilla sobre
$\sqrt{\text{manchas}}$ del 9, la elasticidad amplitud–nivel (los tres bloques con su IC y
su $R^2$), los tres ejercicios del 10 y —pieza a pieza— la reconciliación R/Python del
módulo 8: $21.056$ vs $52.536$, $8.728$ vs $8.727$, $-15.396$ vs $-15.397$, y los
recortados $0.0232$ / $0.1420$ / $0.1051$.

## 5. Tareas

| # | Tarea | Módulo | Tamaño | Depende de |
|---|---|---|---|---|
| T1 | Corregir `intercept` a `6.3317` en el bloque R (C1) | 9 | XS | — |
| T2 | Reescribir la intro del simulador TRM: dos barras, la mayor en $k=8$ (C2) | 9 | XS | — |
| T3 | Reescribir la nota de la prueba conjunta con $0.1839$ y $0.1718$ (C3, C14) | 8 | S | — |
| T4 | Invertir la dirección en el paso 2 de la derivación de Ljung–Box (C4) | 8 | XS | — |
| T5 | Corregir el pseudo-periodo de CSS a $10.71$ y la frase «tercera cifra» (C5, C11) | 7 | S | — |
| T6 | Ampliar la rejilla del código R a `p=0:3` y alinearla con la tabla (C8) | 8 | S | — |
| T7 | Rehacer el bloque Python de estimación: decir que no hay CSS en la API nueva (C7) | 7 | S | T5 |
| T8 | Borrar la línea residual del bloque Python de redundancia (C9) | 5 | XS | — |
| T9 | Separar el `order()` del filtro de fecha (C10) | 9 | XS | — |
| T10 | Añadir la frase que aclara dónde se aplica $\lambda$ de Guerrero (C12) | 9 | XS | — |
| T11 | Corregir «los ocho candidatos» → «los once» en la tabla-ranking (C6) | 8 | XS | — |
| T12 | Regenerar `DATOS_CAP3` para que el BIC del AR(3) sea `848.91` en los tres sitios (C13) | 8 | S | T11 |
| T13 | Refrescar `intercept`/e.e. del M7 y los tres AICc del M5 con R 4.6.0 (§4) | 5, 7 | S | — |
| T14 | Redacción menor: C15 (M3) y C16 (M10) | 3, 10 | XS | — |
| T15 | Reflejar T1–T14 en `ensamblado/ensambla_cap3.py` y comprobar que reejecuta idéntico | — | M | T1–T14 |

**Pendiente de decisión (no es tarea todavía):** la atribución de la ventana 1770–1869 a
Yule aparece dos veces («la ventana centenaria sobre la que Udny Yule inventó en 1927 el
modelo autorregresivo», M7; «la ventana de Yule», M10-Ej3). Yule (1927) trabajó con los
números de Wolfer de **1749–1924**; 1770–1869 es la ventana que popularizó Box–Jenkins.
No pude confirmarlo en las fuentes del repositorio. Si se confirma, basta cambiar la
atribución sin tocar nada más: la serie y el modelo siguen siendo los mismos.

## 6. Criterios de aceptación

- [x] Toda cifra visible en pantalla reproduce en R 4.6.0 hasta el decimal impreso.
- [x] Los bloques R y Python de cada módulo producen la tabla que acompañan, ejecutados
      tal cual.
- [x] Ninguna afirmación de una intro de simulador contradice la lectura de ese simulador.
- [x] El mismo número no aparece con dos redondeos en dos componentes del mismo módulo.
- [ ] ~~Reejecutar `ensambla_cap3.py` reproduce el archivo byte a byte.~~ **No se cumple, y
      ahora se sabe por qué** (§10). El script ya no puede regenerar el capítulo; se le puso
      una guarda para que tampoco pueda borrarlo.
- [x] Cero errores de consola, cero `.katex-error`, los diez simuladores pintan sus **26**
      canvas y el quiz genera sus ocho preguntas.

## 10. Lo que apareció al ejecutar

Tres cosas que la auditoría de lectura no podía ver y solo salieron al tocar el código:

| # | Hallazgo | Estado |
|---|---|---|
| E1 | `DATOS_CAP3` embebido llevaba **λ de Guerrero = 0.3333** mientras la prosa decía $0.3062$: el simulador de transformación del M9 pintaba $11.35$ y $0.4251$ contra el $11.39$ y $0.4892$ del texto. El precálculo se había actualizado sin reembeber el JSON. | Corregido regenerando |
| E2 | El JSON embebido traía **mojibake** (`M<c3><a1>xima verosimilitud`) por el `LC_CTYPE` de R. | Corregido regenerando |
| E3 | `capitulo-3...html#modulo-6` **no abre el módulo 6**: el capítulo 3 no tiene `moduloDelHash()`, que sí tienen el 1 y el 2. Hoy no lo enlaza nadie (el preparcial del Corte I solo remite a los capítulos 1 y 2), pero fallará en cuanto un instrumento del Corte II lo haga. | **Pendiente**: es función nueva, fuera del alcance de esta ronda |

Y la causa de C13 resultó ser un **doble redondeo**: el generador guardaba los criterios con
`round(..., 3)` y el navegador los reimprimía con dos decimales, así que `848.905212` se
convertía en `848.905` y de ahí en `848.90`. Se subió el precálculo a seis decimales.

## 11. Estado de `ensamblado/ensambla_cap3.py`

Se fue a reflejar T1–T14 en el script y se encontró que **no podía ejecutarse**, por tres
razones acumuladas:

1. `SCRATCH` apuntaba a un directorio de sesión efímero, **borrado hacía tiempo**.
2. La sección del CSS de `.derivacion` abortaba: su marcador ya no existe en el capítulo 2,
   porque el componente se retro-portó allí.
3. Las secciones de `barrasExtra` e `iniciarDerivaciones` habrían **duplicado** código que
   el capítulo 2 ya trae.

Lo hecho:

- Las fuentes se rescataron del HTML **ya corregido** a `ensamblado/cap3/` (dentro del
  repositorio, como en los capítulos 4–6). Por construcción incorporan T1–T14.
- Las tres secciones obsoletas ahora **comprueban** en vez de insertar.
- El CSS de `.tabla-ranking` quedó parametrizado (`cap3/tabla_ranking.css`).
- **El script verifica por defecto y solo escribe con `--escribir`**, mostrando el diff. Ya
  no puede borrar correcciones en silencio, que era el riesgo que abría el plan.

Quedan dos diferencias medidas y documentadas en la cabecera del script: el motor JS de
`.tabla-ranking` (~180 líneas, guardado en `cap3/tabla_ranking.js` pero sin punto de anclaje
único) y `moduloDelHash()` (~31 líneas, E3). La raíz es que **los capítulos 2 y 3
evolucionaron por separado y sus motores JS ya no están en el mismo orden**: el modelo de
"derivar el 3 parcheando el 2" se agotó.

Comprobado además que **`ensambla_cap4.py` sigue reproduciendo el capítulo 4 byte a byte**
partiendo del capítulo 3 corregido: el riesgo de arrastre está descartado.

## 7. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| `ensambla_cap3.py` borra las correcciones al reejecutarse | Alto | T15 antes de dar la ronda por cerrada |
| `ensambla_cap4.py` arrastra el capítulo 3 corregido al 4 | Medio | Comprobar el 4 tras cualquier reensamblado |
| Regenerar `DATOS_CAP3` mueve cifras que hoy sí cuadran | Medio | Diff del JSON antes de aceptar (T12) |
| El bloque de la TRM descarga datos en vivo | Bajo | El corte a `2026-06` fija $n=137$; ya verificado |

## 8. Lo que la auditoría encontró bien

Conviene dejarlo escrito, porque es la mayor parte del capítulo:

- **Ortografía impecable.** Cero faltas en 2.937 palabras de prosa. «Autorregresivo»
  siempre con doble r; «componente» en masculino, conforme a [[series-tiempo-convenciones-prosa]].
- **La reconciliación R/Python del módulo 8** es la mejor pieza del capítulo: diagnostica
  la discrepancia comparando residuales en vez de $p$-valores, y **cada una de sus cifras
  reproduce**. Enseña un método, no un resultado.
- **El arco 7→8→9** funciona: identificación → el modelo correcto suspende el diagnóstico →
  el problema no era el modelo sino la escala. Es narrativa de verdad, no encadenamiento.
- **Los diez simuladores** cargan, pintan, responden a sus controles y sus lecturas
  coinciden con R. El triángulo del M2 arranca ya en el modelo del M9; los $\pi$ del M4
  explotan a $5734.4$ cuando $\theta=2$, exactamente lo que promete su intro; la banda del
  laboratorio del M5 da $\pm 0.2530$ con $T=60$ y $\pm 0.0620$ con $T=1000$.
- **Los gráficos** mantienen un código de color estable en los diez módulos: ACF en verde
  institucional, PACF en cian, muestral en naranja translúcido, banda en naranja. Leyendas
  filtradas, `aria-label` en los 25 canvas, eje de rezagos rotulado.
- **El quiz** reparte la opción correcta en las posiciones 4, 2, 3 y 1 — sin el sesgo que
  vigila [[sesgo-posicion-opcion-correcta]].
- Sin IDs duplicados, sin `aria-controls` huérfanos, sin errores de consola ni de KaTeX.

## 9. Enlaces

- [[series-tiempo-riesgo-reensamblado]] — ampliado: el capítulo 3 **sí** tiene generador.
- [[series-tiempo-convenciones-prosa]] · [[verificar-html-por-http-no-file]]
- [[PLAN_Bloque_E_Graficos_FPP3]] — ronda anterior.
