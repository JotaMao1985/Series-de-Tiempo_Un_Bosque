---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-04 Modelos ARIMA y Box-Jenkins]]"
fecha: 2026-09-22
estado: ejecutado
---

# Plan — El ejemplo aplicado de los capítulos 4, 5 y 6

**Objetivo:** hacerle a los tres capítulos restantes la pregunta con la que se abrió
[[PLAN_Cierre_Algebraico_M9]] —¿su ejemplo aplicado usa **todo** el capítulo, o solo una
parte?— y cerrar los huecos que aparezcan.

**Alcance:** el caso aplicado de cada capítulo y nada más. No se tocan los otros módulos.

## 1. El hueco

La auditoría previa, hecha módulo a módulo sobre los tres capítulos, dio un resultado mejor
que el del capítulo 3: los tres tienen serie de trabajo declarada y recorren su ciclo. Los
huecos son puntuales, y los tres son de la misma familia —una pieza que el capítulo enseña
y su propio caso no ejercita—.

| # | Cap. | Dónde | Qué falta | Por qué importa |
|---|---|---|---|---|
| C1 | 4 | M10, caso TRM | El caso se anuncia como «el ciclo de principio a fin» y la tabla de etapas para en el diagnóstico. El pronóstico recibía **una frase**; ni intervalo, ni abanico | La TRM sale ARIMA($0,1,0$): el único modelo del capítulo con $\psi_j = 1$ y $\sigma_h = \sigma\sqrt h$ **exacto**, que es la referencia contra la que el M9 mide a todos los demás |
| C2 | 5 | M7, Paso 2 | El caso completo despacha la ACF con «prácticamente nada más» y no mira los rezagos $11$ y $13$ | El M2 llama a los satélites «lo único genuinamente nuevo» del capítulo y el M4, «el error de conteo más frecuente». El caso que los enseñaría no los cuenta |
| C3 | 6 | M10, casos 2 y 3 | Diebold–Mariano no aparece en el módulo, y el puntaje de Winkler está **calculado** para los tres casos y solo se enseña en uno | Los titulares de los dos casos son afirmaciones de significancia, y el M9 argumenta que la cobertura sola no sirve. El módulo la lee sola |
| C4 | 5 | M7, Paso 2 | «y prácticamente nada más» no es exacto: hay tres barras más fuera de la banda | Frase heredada, en la misma línea que hay que reescribir para C2 |

Lo que **no** es hueco, y conviene dejar escrito: el Nilo aparece en los **diez** módulos del
capítulo 4, incluido el M9 con sus $\psi$; el M8 cierra su caso recogiendo lo que quedó
pendiente en el M1 y el M3; y el capítulo 6 cierra con tres casos de tres desenlaces
distintos y una tabla del recorrido de los seis capítulos.

## 2. Restricciones verificadas antes de planear

- **Los tres capítulos se ensamblan en cadena** (3 → 4 → 5 → 6) y, a diferencia del 3, sus
  guiones **escriben por defecto**: hay que respaldar antes y comparar después.
- **`ensambla_cap4.py` prohíbe la cadena `manchas solares`** en el capítulo 4, para atrapar
  restos del 3. Una referencia deliberada al caso anterior hay que escribirla sin nombrar la
  serie, o el ensamblado aborta. Ocurrió, y el aborto fue correcto.
- **`ensambla_cap4.py` lleva lista blanca de simuladores**: el nuevo hay que registrarlo.
- **`DATOS_CAP4` y `SERIES_CAP4` ya traen todo lo que necesita C1** —`TRM.caminata.sigma2`
  y la serie—, así que el abanico se calcula en el navegador y el precálculo no se toca.
- **`DATOS_CAP6` ya trae `winkler95` de los tres casos**; la mitad de C3 es enseñar lo que
  ya está calculado.
- **`genera_cap6.R` es determinista**: comprobado antes de tocarlo que una reejecución
  reproduce sus dos salidas byte a byte salvo la fecha. Esa comprobación es la que autoriza
  a ampliarlo.

## 3. Decisiones de esta ronda

- **D1.** El abanico de la TRM se dibuja **sobre la serie**, no como tabla suelta: es la
  Etapa 4 que le faltaba al caso, con el mismo `<h4>` que las otras etapas.
- **D2.** La caja que cierra C1 compara **las tres series del curso** con la misma fórmula
  —TRM, Nilo y el caso del capítulo anterior—, porque el contraste es la lección: la raíz
  unitaria es la frontera entre el abanico con techo y el abanico sin él.
- **D3.** Los satélites se parten en dos: **se observan en el Paso 2** (antes de estimar) y
  **se verifican en el Paso 3** (con $\hat\theta$ y $\hat\Theta$ en la mano). Comprobarlos
  con los parámetros ya estimados en el paso de identificación habría invertido el método
  que el capítulo enseña.
- **D4.** C4 se corrige diciendo **cuáles** son las tres barras y qué pasa con ellas, no
  suavizando la frase. Dos desaparecen en los residuales y **una sobrevive**; se dice.
- **D5.** El Diebold–Mariano de los casos 2 y 3 se calcula **en el generador**, con el mismo
  `dm_de()` del backtest, y no a mano en un guion aparte. Una cifra que el precálculo puede
  producir no se escribe desde fuera.
- **D6.** La comparación que no se puede calcular —varianza negativa y luego cero— **se
  reporta como hueco de la tabla y se explica**, en vez de rellenarse o de reducir la
  rejilla hasta que salga entera.

## 4. Cifras verificadas en R antes de escribir

Contra R 4.6.0 (`forecast`, `stats`) y statsmodels 0.14.6.

```
--- C1, capitulo 4 ---------------------------------------------------------
sigma2 = 14756.38   sigma = 121.4758   semiancho95 = 238.09 * sqrt(h)
ultimo observado (jun 2026) = 3497.09
h= 1  [3259.00, 3735.18]   6.8 %      h=12  [2672.33, 4321.85]  23.6 %
h= 6  [2913.90, 4080.28]  16.7 %      h=24  [2330.70, 4663.48]  33.4 %
max |semi - qnorm(.975)*sigma*sqrt(h)| = 4.5e-13   (identico a forecast())
Nilo ARIMA(1,1,1): psi_inf = (1+theta)/(1-phi) = 0.1688; sigma_30/sigma_1 = 1.404
                   frente a sqrt(30) = 5.477 de una caminata

--- C2 y C4, capitulo 5 ----------------------------------------------------
n tras diferenciar = 131   banda = +/-0.1712
r_1 = -0.3411   r_11 = 0.0644   r_12 = -0.3866   r_13 = 0.1516
fuera de banda en 1..24: 1, 3, 9, 12, 23   (r_3=-0.2021 r_9=0.1764 r_23=0.2233)
airline ajustado: theta = -0.4018  Theta = -0.5569
rho_1 = -0.3460   rho_12 = -0.4251   rho_11 = rho_13 = 0.1471 = rho_1 * rho_12  (EXACTO)
residuales: solo el rezago 23 queda fuera (0.2196); el 3 en -0.1254 y el 9 en 0.1166

--- C3, capitulo 6 ---------------------------------------------------------
TRM, DM del naive contra cada rival (37 origenes):
  media   p = 0.0000 / 0.0500 / 0.2112        snaive  p = 0.0000 / 0.0899 / no calculable
  deriva  p = 0.7210 / 0.3158 / 0.1083        ets     p = 0.3243 / 0.3091 / 0.2026
  auto    p = 0.2223 / 0.3468 / 0.2381
  (h = 12 contra snaive: varianza negativa con "acf" y CERO con "bartlett")
Nilo, DM del ARIMA(1,1,1) (36 origenes, h = 1/3/5):
  deriva  0.0176 / 0.0278 / 0.0013      naive  0.0214 / 0.0395 / 0.0043
  media   0.2222 / 0.4338 / 0.5744      auto   0.2083 / 0.3245 / 0.3815
Winkler 95 %  TRM:  ets 1693.42 < naive 1708.57 < deriva 2351.24 < auto 2587.86
                    < snaive 2601.44 < media 4777.54
              Nilo: auto 629.64 < arima111 631.16 < media 717.92 < naive 1138.35
                    < deriva 1171.24   (los cinco con cobertura 100 %)
```

## 5. Tareas

| # | Tarea | Cap. | Tamaño | Depende de |
|---|---|:--:|:--:|:--:|
| T1 | Etapa 4 del caso TRM: fórmula leída, tabla de intervalos y caja comparativa | 4 | M | — |
| T2 | Simulador `trm-abanico` y su registro en la lista blanca | 4 | M | T1 |
| T3 | Satélites en el Paso 2 + nota de los rezagos que sobran (C2, C4) | 5 | M | — |
| T4 | Caja «Los satélites, comprobados» en el Paso 3 | 5 | S | T3 |
| T5 | Ampliar `genera_cap6.R` con el DM de los dos casos y regenerar | 6 | M | — |
| T6 | Caja del DM y caja del Winkler en el caso 2; columna de Winkler en la tabla | 6 | M | T5 |
| T7 | Caja del DM en el caso 3 y columna de Winkler en `TABLAS_RANKING['nilo']` | 6 | S | T5 |
| T8 | Bloques de R y Python de los tres capítulos | 4,5,6 | M | T1–T7 |
| T9 | Duraciones (4.10 18→21, 5.7 18→21, 6.10 16→20) y recuento del sitio | — | XS | todas |

## 6. Criterios de aceptación

- La cadena 3 → 4 → 5 → 6 se reejecuta entera y **solo** cambia el capítulo de cada ronda.
- `ensambla_cap3.py` sigue diciendo **reproducible byte a byte**.
- `genera_cap6.R` reproduce sus salidas salvo la fecha **antes** de ampliarlo.
- `cuenta_sitio.py` en verde tras cada ronda.
- Comprobado **por HTTP** ([[verificar-html-por-http-no-file]]): sin errores de consola, sin
  fórmulas desbordadas, y la lectura del simulador nuevo reproduce la tabla de la prosa en
  $h = 6$, $12$ y $24$.
- El Python del DM reproduce el `dm.test()` de R.

## 7. Riesgos

- **El que se materializó:** `ensambla_cap4.py` abortó por la cadena prohibida. El aborto
  hizo exactamente su trabajo; la referencia se reescribió sin nombrar la serie.
- **El grande, evitado:** regenerar `cap6_datos.js` podía mover cifras publicadas. Se
  comprobó la determinación del generador antes de tocarlo.
- **Vigente:** los casos 2 y 3 del capítulo 6 tienen ahora `dm` en el JSON y **ningún
  simulador lo lee**. Si alguien añade una tabla de ranking con esa clave, no hay aserción
  que la exija.
- **Vigente:** el desborde en móvil de la ecuación del modelo *airline* en el M7 del 5 es
  anterior y se deja como estaba; está medido y la caja lleva barra horizontal.

## 8. Enlaces

- Ronda previa, misma pregunta sobre el capítulo 3: [[PLAN_Cierre_Algebraico_M9]]
- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- [[series-tiempo-riesgo-reensamblado]] · [[verificar-html-por-http-no-file]] ·
  [[series-tiempo-convenciones-prosa]]
- Sesión: [[2026-09-22]]
