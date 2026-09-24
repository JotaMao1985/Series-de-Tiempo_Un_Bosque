---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-04 Modelos ARIMA y Box-Jenkins]]"
fecha: 2026-09-23
estado: ejecutado
---

# Plan — El capítulo 4 en un teléfono, con punto decimal

**Objetivo:** cerrar los tres pendientes que dejó [[PLAN_Auditoria_Cap4]]: el capítulo en un
teléfono, el formato decimal (C40) y la concordancia «la decide» del ciclo del M2.

**Alcance:** el capítulo 4. El formato decimal de los capítulos 1–3, 5 y 6 **no** se toca:
la decisión de usar punto decimal es de Javier y vale para todo el material, pero el
encargo fue «los pendientes de este capítulo».

## 1. El capítulo en un teléfono

Medido como en [[PLAN_Movil_Cap3]]: cada `.katex-display` contra el ancho útil de su primer
contenedor de bloque, con las derivaciones desplegadas, a $375$ y $360$ px.

| Defecto | Antes | Después |
|---|---|---|
| Fórmulas que desbordan su caja | **9 de 44** (M1 ×3, M3 ×3, M7, M9 ×2) | 0 de 44 |
| Módulos con la página más ancha que el teléfono | M4 $568$, M5 $500$, M6 $412$, M7 $388$, M9 $391$, M10 $503$ px | ninguno |

La causa del ancho de página era la misma del capítulo 3: la copia MathML de KaTeX, en
`position: absolute`, escapa del desplazamiento de las tablas. Las **once** tablas de las
plantillas llevan `style="position:relative;"`. Queda confirmada, para el 4, la causa que
[[PLAN_Movil_Cap3]] §5 dejaba abierta.

Los nueve cortes, sin cambiar el contenido:

- definición del ARIMA: $\varepsilon_t \sim \mathrm{RB}(0,\sigma^2)$ en su renglón (`gathered`);
- $(1-\phi B)(1-B)$: el lado izquierdo en su renglón y las dos igualdades debajo;
- el ARMA(2,1) sin diferenciar, $S_t$ y el KPSS, $\sum_t S_t^2 \Longrightarrow \mathrm{KPSS}$,
  y $e_{T+h}$: `aligned` o `gathered` por el `=` o por la implicación;
- las tres llamadas a `ndiffs()`, una por renglón y en `\footnotesize`: a tamaño completo
  pedían $273$ px en una caja de $242$ a $360$ px;
- escalonada y exhaustiva del M7 en cuatro renglones; $\sigma_h^2$ y el intervalo del M9
  en dos.

## 2. Punto decimal (C40)

**Antes:** tres convenciones en pantalla. La prosa, $0.402$; las lecturas de los simuladores,
`0,4020` y `28.637,95` (es-CO); los ejes y tooltips de Chart.js, **el idioma del
navegador**: `1,400` en uno en inglés y `1.400` en uno en español. El intervalo de la TRM se
leía `[3.797,12, 4.213,40]`.

**Decisiones:**

- **D1 · Punto decimal** (Javier, 2026-09-23).
- **D2 · Miles con espacio fino solo desde cinco cifras enteras** (`80 055.01`); con cuatro
  van juntos (`1267.51`). Es como los escribe la prosa: `1267.507` en el texto,
  `28\,268` en las fórmulas. La coma de miles se descartó: junto a una prosa en español se
  lee como decimal.
- **D3 · Ejes y tooltips fijos en en-US y pasados por la misma agrupación**, sustituyendo el
  callback por defecto de la escala lineal y los de `label`/`title` del tooltip. La
  expresión regular solo toca comas entre dígitos seguidas de grupos de tres, así que
  `ARIMA(1,1,1)` pasa intacto. Los años del eje ya no salen `1,871`.
- **D4 · La tabla ordenable gana un `formato` opcional** en su spec. Sin él sigue en es-CO,
  así que en los capítulos 3, 5 y 6 cambian tres líneas de código y nada en pantalla. La
  plantilla de capítulo lleva el mismo cambio. Los talleres y el preparcial llevan copias
  propias del componente y no se tocaron.

## 3. La concordancia

«La forma del pronóstico a largo plazo la **deciden** $d$ y la constante». La auditoría la
había dejado fuera por ser texto de componente; Javier pidió corregirla. El resto del
`.ciclo` (voz «Qué haces», a11y) sigue sin tocar.

## 4. Criterios de aceptación

- A $375$, $360$ y $1280$ px: **0 de 44** fórmulas desbordan y ningún módulo es más ancho que
  la pantalla, con las derivaciones plegadas y desplegadas.
- Ninguna cifra con coma decimal en el texto, los ejes ni los tooltips de los diez módulos.
- Cero `.katex-error` y cero errores de JS.
- Cadena $3 \rightarrow 6$ reensamblada; `audita_posicion_correcta.py` y
  `audita_alineacion_modulos.py` en verde.

Cumplidos todos. Commits `5e3dbf7` (teléfono) y `bdd4c39` (decimales y concordancia).

## 5. Lo que queda fuera

- ~~Punto decimal en los capítulos 3, 5 y 6~~: hecho el mismo día, §6. Siguen con coma los
  capítulos 1 y 2 (sin revisar) y los talleres y el preparcial (copias propias del
  componente).
- El capítulo 5, tabla de la TRM: banda $\pm0.168 \rightarrow \pm0.167$.
- Ningún guion de ensamblado vigila el ancho de las fórmulas.

## 6. Extensión a los capítulos 3, 5 y 6 (2026-09-23)

Javier pidió después «pasa a punto decimal los capítulos 3, 5 y 6». Se copió el bloque del 4:

- `fmt()` del 5 y del 6 con punto decimal y la misma agrupación de miles;
- el 3 no tenía `fmt()` —sus lecturas usan `toFixed()`, que ya escribe punto— y gana uno para
  su tabla ordenable;
- `Chart.defaults.locale = 'en-US'` con ticks y tooltips por `agrupaMiles()` en los tres;
- `formato: fmt` en las cuatro tablas ordenables (`criterios`, `comparativa`, `backtest` y
  `nilo`).

Verificado por HTTP en los 34 módulos: lecturas, tablas, ejes y tooltips con punto decimal,
cero `.katex-error`, cero errores de JS; el 4 se reensambla idéntico y el 3 sigue siendo
reproducible. Commit `df035d0`.

## 7. Enlaces

- Bitácora: [[2026-09-23]]
- Nota del capítulo: [[20948-04 Modelos ARIMA y Box-Jenkins]]
- La auditoría que dejó estos pendientes: [[PLAN_Auditoria_Cap4]]
- La misma ronda en el capítulo 3: [[PLAN_Movil_Cap3]]
