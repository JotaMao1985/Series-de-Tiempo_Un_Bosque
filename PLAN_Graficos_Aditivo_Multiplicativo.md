---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-01 Componentes y descomposición]]"
fecha: 2026-08-11
estado: aprobado
---

# Plan — Gráficos de series aditivas y multiplicativas · Capítulo 1

**Objetivo:** dar forma visual a la distinción aditivo/multiplicativo del Módulo 4, que
hoy se sostiene en una fórmula, un párrafo y una tabla de tres filas, sin un solo
gráfico propio.

## 1. El hueco

El Módulo 4 (`1.4 Los cuatro componentes`) enuncia

$$y_t = T_t + S_t + R_t \qquad\qquad y_t = T_t \times S_t \times R_t$$

y decide entre las dos con el criterio «la amplitud crece con el nivel». Tres carencias:

| # | Carencia | Dónde |
|---|---|---|
| C1 | El criterio se enuncia pero no se **muestra**: no hay ninguna imagen de una banda constante frente a una banda que se abre | tras la fórmula |
| C2 | El argumento cuantitativo —amplitud contra nivel— se da en **tres años sueltos**, sin las dos hipótesis contrastadas y sin los otros nueve | tabla de 1949/1954/1960 |
| C3 | «Un modelo multiplicativo se vuelve aditivo tomando logaritmos» es **solo álgebra**, y de ese hecho dependen el Módulo 7 (STL sobre log) y el 8 | párrafo del logaritmo |

El único apoyo visual existente es indirecto: el «abanico» del gráfico estacional del
Módulo 3, que el texto invoca de memoria dos módulos más tarde.

## 2. Restricciones verificadas antes de planear

| Restricción | Estado |
|---|---|
| ¿Existe `ensamblado/cap1/`? | **No.** El capítulo 1 se edita directo, sin riesgo de reensamblado (ver [[series-tiempo-riesgo-reensamblado]] para los capítulos 4–6) |
| ¿Algún ensamblador lee este archivo? | **No.** `ensambla_cap3.py` parte de `capitulo-2-...html`; la cadena es 2 → 3 → 4 → 5 → 6 |
| ¿Hace falta tocar `precalculo/genera_datos.R`? | **No.** Los tres gráficos se calculan en el navegador desde `DATOS_CAP1.observado`, ya incrustado |
| ¿Cifras a mano nuevas? | **Ninguna.** Todo número que aparezca en pantalla se calcula en JS |
| Tabla existente | Comprobada exacta: 1949 → 126.67 y 44; 1960 → 476.17 y 232. G2 la reproduce, no la contradice |

## 3. Decisiones de esta ronda

| # | Decisión | Elección |
|---|---|---|
| D1 | Alcance | Los **tres** gráficos |
| D2 | Forma de G1 | **Comparador nuevo lado a lado**, no un interruptor en «construye tu serie»: ver las dos series a la vez es el punto |
| D3 | Tabla de amplitud/nivel | **Se conserva** y G2 se añade: la tabla da las cifras que cita la prosa, el gráfico da el patrón |
| D4 | Peso interactivo del módulo | Solo G1 lleva deslizadores. G2 y G3 son estáticos y de panel bajo, para no convertir el Módulo 4 en cuatro simuladores seguidos |
| D5 | Ejes de G1 | **Compartidos** entre los dos paneles. Con autoescalado independiente el abanico se vería igual en ambos y el gráfico mentiría |

## 4. Los tres gráficos

### G1 · Comparador aditivo vs multiplicativo — `comparador-escala`

Sintético, 96 meses. Misma tendencia $T_t = 100 + \beta t$ y misma forma
$s_t = \sin(2\pi t/12)$ en los dos paneles:

- Aditivo: $y_t = T_t + A\,s_t$
- Multiplicativo: $y_t = T_t\,(1 + a\,s_t)$, con $a = A/T_0$

La elección de $a$ hace que **ambas series arranquen idénticas** y se separen solo
al subir el nivel: mismo punto de partida, distinto destino. Cada panel lleva la
tendencia y la **envolvente** $T_t \pm A$ / $T_t(1 \pm a)$ en discontinuo, que es lo
que convierte «banda constante» y «banda que se abre» en algo literal.

Deslizadores: pendiente $\beta$ y amplitud inicial $A$. Lectura numérica: amplitud del
primer año frente a la del último, en los dos modelos.

**Ubicación:** tras la fórmula y el párrafo del criterio, antes de «Dicho así…».

### G2 · Amplitud contra nivel, los doce años — `amplitud-nivel`

Dispersión sobre `AirPassengers` calculada desde `DATOS_CAP1.observado`: eje x, nivel
medio del año; eje y, amplitud (máx − mín). Dos rectas de referencia:

- **Si fuera aditivo:** horizontal a la altura de la amplitud de 1949.
- **Si fuera multiplicativo:** rayo por el origen con la proporción de 1949.

Los puntos siguen el rayo, pero por encima — que es exactamente lo que el capítulo ya
admite en prosa («la proporción sube del 35 % al 49 %»). El gráfico apoya el mensaje de
que ningún modelo describe la serie exactamente, en vez de fingir un ajuste perfecto.

**Ubicación:** tras la tabla, antes del párrafo que la interpreta.

### G3 · Serie frente a log(serie) — `serie-vs-log`

Dos paneles: `AirPassengers` y `log(AirPassengers)`. El abanico y el abanico cerrado.
Lectura numérica calculada en JS: amplitud 1949 vs 1960 en escala original (×5,3) y en
escala log (×1,3) — no ×1,0, y decirlo es coherente con C2.

**Ubicación:** tras el párrafo del logaritmo.

## 5. Tareas

| # | Tarea | Archivos | Tamaño | Depende de |
|---|---|---|---|---|
| 1 | CSS `.grafico-par` (rejilla 1→2 columnas) | HTML cap. 1, bloque `<style>` | XS | — |
| 2 | G1: HTML del bloque + `SIMULADORES['comparador-escala']` | HTML cap. 1 | S | 1 |
| 3 | G2: HTML + `SIMULADORES['amplitud-nivel']` + ayudante de dispersión | HTML cap. 1 | S | — |
| 4 | G3: HTML + `SIMULADORES['serie-vs-log']` | HTML cap. 1 | S | 1 |
| 5 | Prosa de enlace y ajuste del párrafo interpretativo | HTML cap. 1 | XS | 2, 3, 4 |
| 6 | Verificación en navegador | — | XS | 5 |
| 7 | Documentación en el vault | `Vault/Bitacora/`, `Vault/Capitulos/` | S | 6 |

### Criterios de aceptación

- [ ] Los tres gráficos se dibujan al entrar al Módulo 4 y se destruyen al salir
      (`graficosActivos`, sin fugas de `Chart`)
- [ ] Los deslizadores de G1 redibujan los dos paneles con **el mismo eje y**
- [ ] G2 reproduce las tres filas de la tabla (126.7/44, 238.9/114, 476.2/232)
- [ ] Ninguna cifra nueva escrita a mano en la prosa
- [ ] Consola del navegador sin errores ni `Simulador no registrado`
- [ ] La prosa nueva va en voz impersonal y usa «el componente» en masculino
      ([[series-tiempo-convenciones-prosa]])

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| `Object.assign` de `crearGraficoLinea` es superficial: pasar `scales` u `plugins` los reemplaza enteros y se pierden las fuentes | Medio | Reespecificar las fuentes en cada `scales` que se pase. Ya ocurre en el gráfico del Módulo 3 |
| Cuatro bloques interactivos seguidos recargan el Módulo 4 | Medio | D4: solo G1 lleva deslizadores; G2 y G3 con paneles de 240–260 px |
| Ejes independientes en G1 anularían la comparación | Alto | D5: mínimo y máximo fijados al rango global de las dos series, recalculados en cada movimiento |
| Crecimiento del archivo (hoy 201 KB) | Bajo | Sin datos nuevos incrustados; solo HTML y JS. El peso no es criterio de contenido |

## 7. Enlaces

- Plan del curso: [[PLAN_Material_Series_de_Tiempo]]
- Capítulo: [[20948-01 Componentes y descomposición]]
