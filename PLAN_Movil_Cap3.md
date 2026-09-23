---
tipo: plan
curso: "[[20948 Series de Tiempo]]"
capitulo: "[[20948-03 Modelos AR, MA y ARMA]]"
fecha: 2026-09-23
estado: ejecutado
---

# Plan — El capítulo 3 en un teléfono

**Objetivo:** el encargo fue «arregla las seis fórmulas que desbordan en móvil» del capítulo
3. La cifra venía de un barrido mío, y estaba mal.

**Alcance:** las fórmulas en bloque y las tablas del capítulo 3. Nada de CSS compartido,
ningún otro capítulo.

## 1. El recuento, corregido

El barrido anterior leía solo el **primer renglón** de cada caja `.formula`. Midiendo cada
`.katex-display` por separado, en cualquier contenedor y con las derivaciones plegables
**desplegadas**:

| Ancho | Fórmulas que desbordan su caja | Dónde |
|---|---|---|
| $375$ px | **29 de 73** | 13 en `.formula`, 12 en pasos de derivación, 2 en definiciones, 1 en nota, 1 en párrafo |
| $360$ px | **8 más**, por 1–11 px | Cabían a 375; $360$ es el Android más común |

Contenido útil de cada caja a $375$ px: `.formula` $273$, definición y nota $257$, paso de
derivación $238$. A $360$, quince menos.

## 2. Un segundo defecto, hallado al medir

En los módulos 7, 9 y 10 la **página** medía $435$, $424$ y $426$ px en un teléfono de $375$.
No eran las fórmulas: KaTeX acompaña cada expresión de una copia MathML invisible con
`position: absolute`, y dentro de una tabla que se desplaza en horizontal esa copia escapa
del recorte y ensancha el documento. Comprobado: con `position: relative` en la tabla, la
página vuelve a $375$ en los tres módulos. La del M10 era la tabla de decisión de
[[PLAN_Tabla_Decision_M10]], así que en parte era regresión propia.

**Una trampa de medición.** El emulador, como un móvil real, **aleja el zoom** cuando la
página es más ancha que la pantalla, y `innerWidth` sube con ella. Comparar
`scrollWidth` contra `innerWidth` da siempre «cabe». La comparación válida es contra el
ancho de maquetación, `documentElement.clientWidth`, que se queda en $375$.

## 3. Decisiones

- **D1 · Se arreglan las 37, no las seis.** El encargo era el defecto, no la cifra.
- **D2 · Ningún cambio de contenido.** Cortes de maquetación: `aligned` por el signo igual
  cuando hay varias igualdades; lado izquierdo en su renglón cuando es una sola; la
  condición ($k \ge 1$, $k > q$, $|\phi| < 1$) en renglón propio; y el término $\phi_2$
  elidido en seis sumas que ya llevaban $\cdots$, como el propio capítulo escribe la
  recursión del M5.
- **D3 · El denominador del AR(2) se apila, no se parte.** Dos fracciones cabían igual,
  pero la nota siguiente dice «el denominador es el triángulo»: los tres factores tienen que
  seguir en un solo denominador.
- **D4 · Objetivo de diseño, $360$ px.** Todo se midió con margen para $360$, no solo para
  $375$.
- **D5 · Las tablas se contienen con un atributo en línea, no con CSS.** El CSS de las tablas
  se hereda del capítulo 2 y se propaga por la cadena hasta el 6: arreglarlo ahí es un
  cambio de sitio completo. Además, otra sesión prepara la auditoría del capítulo 4
  ([[PLAN_Auditoria_Cap4]]) y está regenerando sus datos.
- **D6 · Cada corte se midió antes de escribirlo.** Un banco de pruebas en la página
  renderiza el candidato junto a la fórmula original, en su mismo contenedor, y devuelve el
  ancho real con su fuente y su caja.

## 4. Criterios de aceptación

- A $375$, $360$ y $1280$ px: **0 de 73** fórmulas desbordan, con las derivaciones plegadas y
  desplegadas.
- Ningún módulo más ancho que el teléfono.
- Cero `.katex-error` y nada sin renderizar.
- `ensambla_cap3.py` reproducible byte a byte; capítulos 4, 5 y 6 sin cambios.
- `cuenta_sitio.py` en verde.

Cumplidos todos.

## 5. Lo que queda fuera

El mismo barrido, a $375$ px, en el resto del sitio:

| Capítulo | Fórmulas | Desbordan | Módulos con página más ancha |
|---|---|---|---|
| 1 | 20 | 9 | 0 |
| 2 | 16 | 10 | 2 (hasta $391$ px) |
| 4 | 23 | 16 | 6 (hasta $677$) |
| 5 | 20 | 13 | 10 de 11 (hasta $665$) |
| 6 | 17 | 5 | 9 de 12 (hasta $571$) |

En los capítulos 4–6 la causa del ancho de página **no está confirmada**: puede ser la misma
MathML de tablas o las tablas de ranking y los simuladores. Y ningún guion de ensamblado
vigila el ancho: una aserción que midiera cada fórmula contra su caja evitaría que vuelva a
colarse.

## 6. Enlaces

- Bitácora: [[2026-09-23]]
- Nota del capítulo: [[20948-03 Modelos AR, MA y ARMA]]
- La tabla que introdujo la regresión del M10: [[PLAN_Tabla_Decision_M10]]
- El primer arreglo de este tipo, en el capítulo 5: la ecuación del *airline*, en [[2026-09-23]]
