# R2 · verificación independiente · Capítulo 4 · gráficas y simuladores

Verificador: sesión distinta de la que redactó. Fecha: 2026-11-22. Base: `b3e9042` + el diff sin commit (10 archivos). Sin edición de ningún archivo del
repo; guiones y salidas propios en `diagnostico/cap4/comprobaciones/v2_*` (capturas en `capturas/v2/`, 51 MB, git las ignora). El informe del redactor
(`R2_cambios.md`) se leyó **después** de la revisión propia y se contrasta en §2 y §5.

**Veredicto.** La ronda hace lo que dice: no encontré ningún problema Alto ni ninguna regresión en los caps. 2, 3, 5 y 6. De las 44 fichas, **40 confirmadas,
3 en parte (M4-1, M10-1, quiz-3) y 1 no (M6-3, la barra de 3 px)**. Lo nuevo que encontré es todo Medio o Bajo (§1): la separación barra–banda de los
correlogramas sigue en 1–3 px, nueve rótulos del ΔAICc que se tocan en una franja estrecha de ancho, y el tooltip de las cruces ∞.

Método: Chrome sin ventana por CDP (9280–9289), servidor propio en 8766 (árbol) y 8767 (HEAD desde `git archive`), ambos cerrados al terminar junto con todos los
Chrome; anchos 1200, 800 y 375 px (este con emulación móvil, dsf 2), más 12 anchos intermedios.

---

## 1. Problemas encontrados

Rutas de la **fuente** (`ensamblado/cap4/chapter.js`, en adelante `chapter.js`); el HTML final es la fuente + 7750 líneas en la zona de simuladores.

| # | Gravedad | Dónde | Qué pasa y cómo reproducirlo |
|---|---|---|---|
| V1 | **Media** | `chapter.js` l. 448 (`ALTOS_BARRAS`) y l. 1119 (`ALTOS_ACF`); el eje ±1 es de `crearGraficoBarras` (armazón) | **Las fichas M4-1 y M10-1 quedan en parte.** El área de dibujo pasó de 75 a 145 px, pero el eje sigue en −1…1 (72.4 px por unidad), así que lo que se compara, que está en 0.2, sigue a 1–3 px de la banda: M4 d = 0, rezagos 4–7 (0.2392, 0.2284, 0.2273, 0.2220) frente a ±0.196 = 3.1, 2.3, 2.2 y 1.9 px; 11–13 (0.2155, 0.2129, 0.2370) = 1.4, 1.2 y 3.0 px; M4 d = 1, rezago 8 (0.2312 frente a 0.197) = 2.5 px; M10 d = 1, ρ̂₈ = −0.190 frente a 0.1675 = **1.6 px**. «11 de 20 fuera de banda» se sigue sin poder contar a ojo (`capturas/v2/m4-identificacion-nilo-d0-1200.png`). El propio `R2_cambios.md` §6 lo admite («a 1–3 px») pero marca las dos fichas **A**. Arreglo posible: acotar el eje de estos correlogramas a ±0.6 (o a ±(máx + holgura)) con la banda dentro; no es del armazón si se pasa `min`/`max` y se fuerzan (hoy son *suggested*). |
| V2 | Baja | `chapter.js` l. 565 (`tumbado = gAicc.width < ESTRECHO`, ESTRECHO = 420 l. 168) y l. 599–604 (`autoSkip: false`) | **Los nueve rótulos del ΔAICc se tocan en una franja de ancho.** Con el lienzo entre 421 y ≈ 455 px (ventana de **560 a 595 px**; solo se descubre fuera de 1200/800/375) los nueve rótulos de 7 caracteres caben a la fuerza: hueco entre rótulos **−1 px a 421**, 3.7 px a 461, 6.7 a 487, 7.1 a 490 (ventana de 1024). En HEAD el salto automático dejaba 3 o 5 de 9 (sin choque). Reproducir: ventana de 560 px, M6, d = 1 o 2 (`v2_anchos.js`; `v2_anchos.out`). Arreglo: tumbar el gráfico por debajo de ≈ 460 px solo para este lienzo, o fuente de 9 px. Ningún otro de los gráficos medidos (M6 ACF, M7, M9, M10, M3) baja de 5.4 px de hueco en ningún ancho de 420 a 1440. |
| V3 | Baja | `chapter.js` l. 737 (`p.infinito ? TECHO : null`) | **El tooltip de una cruz ∞ da un AICc inventado:** «AICc = ∞ (descartado): **1305**» (en HEAD, 1302; la misma clase de defecto, otra cifra). Reproducir: M7, «Búsqueda exhaustiva», paso 21 o más, pasar el ratón sobre una cruz (`v2_tooltip.js`). Arreglo: `tooltip.callbacks.label` que devuelva «∞» para ese conjunto. El redactor declaró los tooltips «no mirados»; esta es la lectura. |
| V4 | Baja | `chapter.js` l. 1034 y l. 1263 | **Concordancia en dos `aria-label`:** «los **1** primeros, en naranja, entran en σₕ» (M9 ψ con h = 1) y «pronóstico de caminata aleatoria a **1 meses**» (M10 abanico con h = 1; la lectura de ese mismo gráfico ya decía «σ a 1 meses»). |
| V5 | Baja | `chapter.js` l. 1139 (`info.banda`) | **Doble redondeo en el `aria-label` de la ACF de la TRM con ∇:** dice «banda ±**0.168**»; 1.96/√137 = 0.16745, que a tres decimales es 0.167 (la lectura da ±0.1675, el dato incrustado está redondeado a 4). El M6 lo hace bien (`banda(nEf)`). El conteo de barras fuera de banda no cambia. Arreglo: pasar `1.96 / Math.sqrt(info.n)`. |
| V6 | Baja | `chapter.js` l. 345 y l. 412 | **Dos literales a mano en `aria-label`** del M3: «desde 1899» y «de 0 a 300». Hoy coinciden con los datos (`malla.posicion` = 29 → 1871 + 28 = 1899; el último punto de la malla es 300), pero no salen de ellos. |
| V7 | Baja | cifra heredada que el `aria-label` repite | σ√h a tres decimales: la página da **778.013** (h = 30), R da **778.015**, porque multiplica la σ ya redondeada (142.045). Ya estaba en la lectura y en la prosa; el `aria-label` del M9 σ_h lo copia. |
| V8 | Nota | M6, `leyendaDeColores` (`chapter.js` l. 585–590) | La leyenda fija lista «Mejor de su d» (verde) también en los estados en que el elegido *es* el mejor (p. ej. (1,1,1) con d = 1): no hay barra verde, solo la naranja. No confunde, pero la entrada no tiene barra. |
| V9 | Nota (no es regresión) | cap. 3 M2 y M3 (gráficos de dispersión) | Dos entradas de leyenda dibujan rayas continuas siendo discontinuas en el gráfico («Debajo: raíces complejas», «Cota \|ρ₁\| = 0.5»). Igual que en HEAD; la leyenda nueva solo cubre `crearGraficoLinea`. Fuera del alcance de la ronda. |
| V10 | Nota | cap. 1, `plantilla-capitulo.html`, preparciales, talleres, guía del proyecto | Traen su copia del armazón y siguen dibujando las líneas como cajas; el redactor lo declara (§6 de su informe). Queda una diferencia visible entre el cap. 1 y los caps. 2–6. |

Lo demás que se buscó y **no** apareció: ninguna excepción ni `console.error/warn` de la página (solo el 404 de `/favicon.ico` y mis propios avisos de
`getImageData`) en 12 módulos × 3 anchos × todos los estados; ningún lienzo en blanco (138 estados × 3 anchos, tinta leída del propio canvas a los 300 y a los
1500 ms, `v2_tinta.js`: 0 en blanco; tres de mis capturas de pantalla salieron en blanco —`m10-trm-abanico-h24-1200`, `m10-trm-identificacion-d0-1200`,
`m10-puente-estacional-si-1200`— y son artefactos de la captura, no de la página); área de dibujo mínima **128.8 px** (el gráfico 1 del quiz a 800 px; antes 52).

---

## 2. Las 44 fichas de `graficas.md`

Numeración por orden de aparición (M1: 1–3; M3: 4–8; M4: 9–12; M6: 13–16; M7: 17–20; M8: 21–23; M9 forma: 24–27; M9 ψ/σ: 28–32; M10 TRM: 33–36;
abanico: 37–39; puente: 40–41; quiz: 42–44). «Medido» = lo que leí en `v2_medidas.json` (por estado y ancho) y en las capturas.

| # | Ficha (grav. original) | Veredicto | Medido |
|---|---|---|---|
| 1 | M1 · años sin redondear, solapes (B) | **confirmado** | 1200: 1880…1970 de 10 en 10 (hueco 34 px); 800: 1880…1960 (19 px); 375: 1875…1950 (19.7); d = 0, 1, 2 |
| 2 | M1 · guion y sin línea del 0 (B) | **confirmado** | ticks `−400…`, `−800…` con U+2212; el 0 oscuro (captura `m1-…-d1-1200`) |
| 3 | M1 · `aria-label` fijo (B) | **confirmado** | cambia con d; n, media, varianza y ρ̂₁ recalculados aparte: 919.35/−3.84/−0.14; 28 637.95/28 268.34/80 055.01; 0.4984/−0.4020/−0.6264 |
| 4 | M3 · área de la tasa 94 px a 1200 (M) | **confirmado** | 153.6 px a 1200 (antes 93.6), 163.6 a 800, 166.6 a 375; la recta del 5 % queda a 7.7 px del 0 (antes 4.7) |
| 5 | M3 · marcador β recortado (B) | **confirmado** | `clip: false`; β = 0, 5, 100, 150, 200, 245, 250, 300: círculo entero (capturas β = 0 a 1200 y β = 300 a 375) |
| 6 | M3 · leyenda con cajas (B) | **confirmado** | raya continua, raya discontinua [5,4], punteada [2,3], círculo; a 375 px, 2 líneas (antes 3) |
| 7 | M3 · eje x a 375 sin aire (B) | **confirmado** | 1875, 1900, 1925, 1950; hueco 19.5 px |
| 8 | M3 · `aria-label` fijos (B) | **confirmado** | cambian con β; 70.8 % / 44.5 % (β = 100) y 4.5 % / 3.5 % (β = 0) iguales a la lectura; la media baja 0.72·β (994.65 → 922.65) como debe |
| 9 | M4 · ACF/PACF de 75 px a 1200 (M) | **en parte** | área 144.8 px (antes 74.8) y a 800/375 sin cambio (140.8/143.8); pero el eje sigue en ±1 y la separación barra–banda es 1.2–3.1 px: **V1** |
| 10 | M4 · icono vacío (B) | **confirmado** | `fa-chart-column` (`\e0e3`) y `fa-arrows-left-right` (`\f07e`) existen en `all.min.css` 6.0.0 (descargué la hoja); ancho 18 px y se dibujan (capturas M4 y M9 ψ/σ) |
| 11 | M4 · serie con años sin redondear (B) | **confirmado** | huecos 19.1–20.1 px a 800 y 375; guion → U+2212 |
| 12 | M4 · `aria-label` fijos (B) | **confirmado** | `descripcionCorrelograma`: 11/1 (d = 0), 2/4 (d = 1), 2/7 (d = 2) barras fuera de banda de ACF/PACF; recalculado con numpy: idéntico |
| 13 | M6 · ΔAICc rotula 5 de 9 a 1200 (**A**) | **confirmado** | los **27 estados** a 1200: 9 de 9 rótulos (hueco 26.6 px, `↑121`, `↑27`, `↑74`, `↑51` en dos renglones); 800 y 375 tumbado con 9 de 9. Reserva: **V2** (421–455 px de lienzo) |
| 14 | M6 · muestra de la leyenda toma el color de la primera (B) | **confirmado** | los 27 estados × 3 anchos: «Elegido» #FB6400, «Mejor de su d» #012820, «Los demás» #8795A9, siempre iguales (**V8**, nota) |
| 15 | M6 · la barra del mejor es una raya de 3 px (B) | **no** | sigue de 3 px (`minBarLength = 3`); la leyenda ya nombra su color y el `aria-label` dice «+0.00». El redactor lo marca P; coincide |
| 16 | M6 · `aria-label` del ΔAICc (B) | **confirmado** | dice «ΔAICc», cambia con d y con el elegido; **27/27 estados** reproducidos aparte (mín., máx., «+Y», barras cortadas); el de la ACF, 27/27 (recuento y rezago 1) |
| 17 | M7 · cruces cortadas por la mitad (M) | **confirmado** | fila propia (eje 1265…1305 con «∞» arriba), `clip: false`; cruces enteras en pasos 1 y 18 de la escalonada y 21, 27–30 de la exhaustiva, a los tres anchos; la leyenda dibuja la cruz. Reserva: **V3** (tooltip) |
| 18 | M7 · muestra cambia de color con el modo (M) | **confirmado** | «Modelo evaluado» #012820 y «Mejora del mejor AICc» #FB6400 en las dos búsquedas y en todos los pasos |
| 19 | M7 · leyenda de 3 líneas y área 78–81 (M) | **confirmado** | 2 líneas a 800 y 375; área 174.8 y 177.8 px |
| 20 | M7 · rótulos inclinados, paso irregular, puntos cortados (B) | **confirmado** | rot = 0; y: 1265, 1270 … 1300, ∞ (de 5 en 5); primer y último punto enteros (`offset` + `clip: false`) |
| 21 | M8 · eje logarítmico con 3 rótulos (B) | **confirmado** | 10 000 · 30 000 · 100 000 · 300 000 (con espacio fino); barras en 28 638, 28 268, 80 055, 262 507; leyenda «Orden elegido / Los demás» |
| 22 | M8 · serie: años y guion (B) | **confirmado** | como M1, d = 0…3 |
| 23 | M8 · `aria-label` fijos (B) | **confirmado** | d, n, rango y varianza (28 637.95 / 28 268.34 / 80 055.01 / 262 507.29 recalculadas); la de la varianza lista las cuatro |
| 24 | M9 forma · el pronóstico sin constante no se queda en el último nivel (**A**) | **confirmado (R1)** | no lo toca esta ronda: la tabla y el párrafo de debajo (`templates_7_9.html`, R1) ya dicen «no en el último dato (740), sino en 842.17»; R da 724.16/610.05 y 816.18/842.17 con `forecast::Arima`, iguales a la página |
| 25 | M9 forma · leyenda de 4 líneas a 375; «Pronóstico» como caja (M) | **confirmado** | 2 líneas (antes 4), área 207.8 px (antes 131.8); «Pronóstico» es raya naranja, los intervalos son cajas |
| 26 | M9 forma · banda negativa con d = 2 (B) | **confirmado** | lectura: «límite inferior 95 % (h=30) −775.67 — por debajo de 0, y un caudal no puede ser negativo»; R: −775.67 y 1995.78. La serie sigue comprimida (el eje llega a −1000): es lo que dibuja el intervalo |
| 27 | M9 forma · eje x a 375, seis solapes (B) | **confirmado** | 1900, 1950, 2000 a 800 y 375 (hueco 34.8 px); 1880…2000 de 20 en 20 a 1200 |
| 28 | M9 σ_h · área 74/52/55 (M) | **confirmado** | σ_h 134.8 / 144.8 / 147.8 px; ψ 134.8 / 140.8 / 143.8 px |
| 29 | M9 σ_h · marcadores h = 1 y h = 30 cortados (B) | **confirmado** | `clip: false`; enteros a los tres anchos (captura h = 30 a 800) |
| 30 | M9 ψ · eje hasta 1.5 (B) | **confirmado** | eje 0.0…1.0 (`max` = máx. de los datos) |
| 31 | M9 σ_h · eje x sin el 30 (B) | **confirmado** | 1200: 1, 3, 6 … 30; 800: 1, 4, 8, 12, 16, 20, 24, 30; 375: 1, 6, 12, 18, 24, 30 |
| 32 | M9 ψ · icono vacío (B) | **confirmado** | ver ficha 10 |
| 33 | M10 TRM · ACF de 75 px (M) | **en parte** | área 144.8 px a 1200 (antes 74.8) y 140.8–143.8 a 800/375; ρ̂₈ = −0.190 frente a ±0.167 sigue a **1.6 px**: **V1** |
| 34 | M10 TRM · fechas `AAAA-MM` crudas (B) | **confirmado** | eneros con su año: 2015…2026 (1200, hueco 26.5), 2016/2019/2022/2025 (800 y 375) |
| 35 | M10 TRM · ∇TRM con guion, sin línea del 0 (B) | **confirmado** | ticks `−400…`; el 0 oscuro |
| 36 | M10 TRM · `aria-label` fijos (B) | **confirmado** | rango (2400.97–4931.33 y −323.30–470.19, recalculado) y ACF (20/20 y 1/20). Reserva: **V5** (±0.168) |
| 37 | M10 abanico · leyenda de 4 líneas a 375 (M) | **confirmado** | 2 líneas; área 207.8 px (antes 111.8) |
| 38 | M10 abanico · fechas irregulares (B) | **confirmado** | 2023…2028 según h; ningún solape |
| 39 | M10 abanico · `aria-label` sin horizonte (B) | **confirmado** | h = 1, 12, 24, 36: pronóstico 3497.09 e intervalo igual al de la lectura (2330.70–4663.48 en h = 24). Reserva: **V4** |
| 40 | M10 puente · `aria-label` (B) | **confirmado** | modelo, 8/26 y 1/26 barras fuera de banda (rezagos 2, 5, 7, 12, 14, 19, 24, 26 y el 23) y ρ̂₁ −0.019 / 0.014: recalculado aparte |
| 41 | M10 puente · leyenda de 2 líneas, área 95–98 (B) | **confirmado** | rótulo «ACF residual» a 800 y 375; 1 línea; área 140.8 y 143.8 px |
| 42 | quiz · `descripcionGrafico` de la ACF «sin diferenciar» (M) | **confirmado** | ahora lista los 20 valores a 2 decimales y la banda ±0.196 (todos coinciden con los datos, 9 de 20 dentro de la banda); ya no afirma «sin llegar a cortarse». La retro de la opción a la había corregido la R1 («8 de los 17 rezagos…»: comprobado, 8 de los rezagos 4–20 salen de la banda) |
| 43 | quiz · `descripcionGrafico` del correlograma mensual (B) | **confirmado** | 26 valores a 2 decimales y ±0.163, todos iguales a los datos |
| 44 | quiz · área de 82 px a 375 (B) | **en parte** | área 131.8 px (antes 81.8) a 375 y 149.8 a 1200; pero la leyenda sigue a 2 líneas (el de los residuales a 800 y 375; el de la ACF cruda a 375) |

**Recuento:** 40 confirmadas · 3 en parte (9, 33, 44) · 1 no (15) · 0 no comprobadas. De las 2 Altas, ambas confirmadas (13 por esta ronda, con la reserva
V2; 24 por la R1). De las 10 Medias: 8 confirmadas y 2 en parte (9, 33).

---

## 3. Los ocho puntos del encargo

1. **Reproducibilidad: sí.** Copia en el scratchpad (`rsync` sin `.git`, `diagnostico` ni `bibliografia/_local`); `ensambla_cap3.py --escribir`, luego 4, 5 y 6: los
   cinco capítulos (2–6) salen con el **mismo md5** que los del árbol (`07600bcb…`, `58313bfa…`, `1af8ede2…`, `ff6b52cb…`, `75571fab…`). El diff de los caps. 2, 3, 5 y 6 es
   idéntico en los cuatro (68 líneas añadidas, 6 quitadas; md5 del diff `b38db31a…`) y está todo dentro de `crearGraficoLinea` / `etiquetasDeLeyendaLinea` /
   el plugin `anchoDeLaMuestra`. El diff del cap. 4 = ese armazón + `ensamblado/cap4/` (leí los 713 renglones de `chapter.js` y los de las cuatro plantillas).
2. **Las 44 fichas:** §2. Medido por HTTP, a 1200/800/375 y los estados de `graficas.md` ampliados (27 del explorador, escalón de 8 valores, traza con 10 pasos,
   d = 0…3, los 4 modelos con y sin bandas, h = 1, 2, 15, 30; h = 1, 12, 24, 36), más 12 anchos intermedios (420–1440 px) para M6, M7, M9, M10 y M3.
3. **Regresiones: no hay** (`v2_regresion*.js/.py`). Caps. 2, 3, 5 y 6 a 1200 y 375 px, HEAD frente al árbol, **cada control movido un paso a la vez** (38, 138, 101 y 93
   pares lienzo-estado por ancho): mismos textos y mismo número de entradas de leyenda, mismo número de conjuntos de datos, ninguna pérdida de tinta, ningún lienzo
   sin gráfico, consola limpia; la única diferencia de área es cap. 5 M9 `calendario-regresores` a 375 px (leyenda de 3 a 2 líneas: 113.8 → 135.8 px, a favor).
   Formas de la muestra: de 543 apariciones de entradas (a 1200 px, todos los estados) de gráficos de línea con trazo conocido, 525 son raya (con su discontinuidad), 10 son punto y 8 son caja (las bandas
   «IC 80 %» e «IC 95 %» del cap. 5); ninguna serie dibujada como caja ni banda como raya. Capturas HEAD/árbol de seis simuladores de los caps. 2, 3, 5 y 6
   (`capturas/v2/leyenda-*`): cap. 5 «Pronóstico» discontinuo y bandas en caja; cap. 6 «error por horizonte» con rayas. Pulsar una entrada de la leyenda oculta
   su conjunto (M7 probado) y las leyendas de colores del cap. 4 no reaccionan. Cambiar el ancho con el módulo abierto: el ΔAICc se repinta al cruzar 420 px
   (1200 → 375 → 560 → 800 → 1200) y vuelve a sus nueve rótulos; los rótulos cortos del M3, fijados al crear el gráfico, no cambian al ensanchar (lo declara el redactor).
4. **Cifras: todas salen de los datos y coinciden.** Recalculé aparte (numpy sobre `SERIES_CAP4`; R sobre `Nile` con `forecast`) lo que los `aria-label`, lecturas y
   `descripcionGrafico` escriben: M1 (media, varianza y ρ̂₁ para d = 0…3), M4 (ACF/PACF fuera de banda y rangos), M6 (**los 27** `aria-label` del ΔAICc y de la ACF),
   M7 (mejoras e infinitos por paso, con un recuento independiente; mejor AICc 1267.507 y 1296.738), M8 (cuatro varianzas), M9 (ŷ₁, ŷ₃₀, límites del 95 % de los 4
   modelos; **−775.67 y 1995.78** con R; ψ₀, ψ₁, ψ₂₉ y σ_h), TRM (mín. y máx., banda), puente (8/26, 1/26, −0.019, 0.014) y las dos `descripcionGrafico` del quiz (valores
   redondeados a 2 decimales, bandas ±0.196 y ±0.163). `DATOS_CAP4` es idéntico a `precalculo/salidas/cap4_arima.json`. Reservas: V5, V6, V7 (nada de esto
   cambia un resultado).
5. **Quiz y simulacro: intactos.** Volcado de `AUTOEVALUACIONES['cap4']` y `SIMULACROS['cap4-simulacro']` en HEAD y en el árbol (`v2_quiz.js`, `v2_quiz_*.json`): 8 preguntas
   en el mismo orden; solo cambian `alto` (200 → 250) y `descripcionGrafico` de las preguntas 3 (M10) y 6 (M4); enunciados, opciones, claves, retros y pistas, idénticos; el
   simulacro, idéntico (24 096 caracteres); los 12 módulos, en el mismo orden. Bloques de código: **27 de 27** `<pre>` de R/Python iguales a HEAD (el único `<pre>` que
   difiere es un tramo del JavaScript del capítulo).
6. **Iconos: sí.** `fa-chart-column` y `fa-arrows-left-right` están en la hoja 6.0.0 que carga el capítulo y se dibujan (capturas); los 12 `<h4>` de simulador con ancho > 0 y
   `::before` no vacío a 1200 y 375 px.
7. **Prosa nueva: impersonal y sin citas.** Todo lo nuevo visible son `aria-label`, rótulos de leyenda, la fila de la lectura del M9 y las dos descripciones del
   quiz; sin segunda persona, sin autores, años ni DOI nuevos (`grep` sobre las líneas añadidas). «Un caudal no puede ser negativo» es una afirmación propia, no atribuida.
8. **Verificadores:** `python3 precalculo/verifica_todo.py` → **11 en verde** (`v2_verifica_todo.out`; Tailwind compilado, ensamblado del cap. 3 y guía del proyecto incluidos);
   `MPLBACKEND=Agg python3 precalculo/verifica_bloques_cap6.py --html Htmls_Series/capitulo-4-modelos-arima.html` → **762 de 762** (`v2_bloques_cap4.out`).
   Tras todo, los md5 de los cinco capítulos del árbol son los del principio y `git status` no cambió salvo mis archivos `v2_*`.

---

## 4. Lo que no pude comprobar

- Un lector de pantalla real: solo leí el texto de los `aria-label`.
- Modo oscuro, zoom del navegador, impresión y navegadores distintos de Chrome.
- Tooltips: solo los de la traza (V3); el resto de los gráficos, no.
- Giro del teléfono: lo emulé cambiando el ancho de la ventana en caliente (M6, M3), no con el sensor ni con el evento de orientación.
- La exhaustiva de la traza en cada paso (medí 1, 18, 21, 27, 30 y 42) y el escalón en todos los pasos de 5 (medí 0, 5, 100, 150, 200, 245, 250 y 300).
- `verifica_todo.py --lento`, `--red` y `--zotero` (no pedidos).
- Si la hoja de Font Awesome 6.0.0 del CDN es la que ven los estudiantes sin red: la comprobé contra la copia de cdnjs.

## 5. Contraste con `R2_cambios.md` (fila a fila, después de mi revisión)

Coinciden mis medidas con sus cifras en las 44 filas salvo en tres juicios: **M4-1 y M10-1** (ellos **A**, yo en parte: V1), y **quiz-3** (ellos A, yo en parte por la
leyenda de 2 líneas). Su única fila **P** (M6-3) coincide con mi «no». Su afirmación «0 solapes» vale en los tres anchos revisados y no entre 421 y 455 px de lienzo (V2); su
«tooltips no mirados» es la fuente de V3. Su registro dice «9 de 20 dentro de la banda» en el quiz y «8 de 26 fuera» en el mensual: ambos reproducidos.

## 6. Guiones y salidas (`diagnostico/cap4/comprobaciones/`)

`v2_revisa.js` → `v2_medidas.json`, `v2_revisa.log`, `capturas/v2/` (barrido de la ronda a tres anchos, 85 estados por ancho) · `v2_ver.py`, `v2_analiza.py` (lectura de las
medidas) · `v2_regresion.js`, `v2_regresion_lanza.sh`, `v2_regresion_compara.py`, `v2_regresion_*.json/.log` (caps. 2, 3, 5, 6; HEAD frente a árbol) · `v2_captura_leyendas.js`
· `v2_quiz.js`, `v2_quiz_{nuevo,viejo}.json` · `v2_tinta.js` (lienzos en blanco) · `v2_anchos.js`, `v2_anchos.out`, `v2_anchos*.json` (12 anchos intermedios; HEAD a 560 y 600) ·
`v2_gira.js` (cambio de ancho en caliente) · `v2_tooltip.js` · `v2_DATOS_CAP4.json`, `v2_SERIES_CAP4.json` (extraídos del HTML) · `v2_verifica_todo.out`, `v2_bloques_cap4.out`.

---

## Qué hizo la sesión maestra

Correcciones en `ensamblado/cap4/chapter.js` con `comprobaciones/r2_ediciones_maestra.py` (16 sustituciones de marcador único, `--comprobar` en OK; se aplica después de
`r2_edita.py`); cap. 4 reensamblado; caps. 5 y 6 reensamblados y con el mismo md5 que antes de estas correcciones (el armazón no se tocó).

| # | Qué se hizo | Cómo se comprobó |
|---|---|---|
| V1 | `resaltarFueraDeBanda()`: en los correlogramas de identificación (M4 ACF y PACF, M10 ACF) las barras con \|ρ̂\| > banda van en el color de la serie y las de dentro en gris, con el mismo criterio que la cuenta de la lectura; la leyenda dice «ACF/PACF fuera de la banda · Dentro · Banda». El eje sigue en ±1 (convención del curso). M4-1 y M10-1 pasan a **A** | capturas `capturas/r2/m4-identificacion-nilo-d0-1200.png` (11 oscuras de 20) y `m10-trm-identificacion-d1-375.png` (solo ρ̂₈); área mínima del recorrido 127.8 / 124.8 px a 800 / 375 (la leyenda de la PACF pasa a dos renglones), antes 138.8 / 135.8 |
| V2 | El ΔAICc se tumba por debajo de 460 px de lienzo, no de 420 | `r2_maestra_anchos.out`: a 560 px de ventana (lienzo 421) el gráfico sale tumbado con hueco de 69.5–71 px; los demás anchos, iguales a `v2_anchos.out` |
| V3 | Tooltip de la cruz: «AICc = ∞ (descartado)», sin cifra | `r2_maestra_tooltip.out` (copia de `v2_tooltip.js` contra 8764) |
| V4 | «el primero, en naranja, entra en σₕ» con h = 1; «a 1 mes» en el `aria-label` y en la lectura del abanico | código; h = 1 no está entre los estados del recorrido |
| V5 | La banda del `aria-label` de la TRM se calcula con `banda(n)`: ±0.167 | `r2_resumen.out` (recorrido de la maestra) |
| V6 | El año del escalón (`etiquetas[malla.posicion − 1]`), el rango de β (`betas[0]`, `betas[último]`) y el primer año de la realización simulada (`SERIES_CAP4.nilo.inicio[0]`, antes «1871» a mano) salen de los datos | el recorrido da los mismos textos que antes («1899», «de 0 a 300») |
| V7 | σ√h se da a un decimal en la lectura y el `aria-label` del M9: σ llega redondeada a tres, y a tres decimales σ√h discrepaba de R (778.013 frente a 778.015); a uno da 778.0, como la prosa | `r2_resumen.out`: «σ√h = 550.1» en h = 15 |
| V8 | Sin cambio: la entrada «Mejor de su d» sin barra cuando el elegido es el mejor no confunde | — |
| V9, V10 | Fuera del alcance (cap. 3 dispersión; copias del armazón en el cap. 1, la plantilla, preparciales, talleres y guía) | quedan anotados para el registro de pendientes |
| M6-3 | La barra del mejor (Δ = 0) sigue siendo de 3 px: la leyenda nombra su color y el `aria-label` da «+0.00». Queda **P** | — |
| quiz-3 | La leyenda del gráfico de residuales sigue en dos renglones a 800 y 375, con 131.8 px de área (antes 81.8). Queda **P** | — |

Al cierre: `python3 precalculo/verifica_todo.py` → 11 en verde (`r2_maestra_verifica_todo.out`); bloques del cap. 4 → 762 de 762 (`r2_maestra_bloques.out`); recorrido
del cap. 4 por HTTP (8764, CDP 9277; `r2_maestra_revisa.log`, `r2_medidas.json` y `r2_resumen.out` reescritos con el estado final): mismos 55 eventos de consola que el
del redactor, ninguno de error de la página. Las capturas del verificador se movieron de `comprobaciones/v2_capturas/` (no ignorada por git) a `capturas/v2/`.

**Recuento final de las 44 fichas:** 41 A · 2 P (M6-3, quiz-3) · 1 R1 (M9 forma-1). Las dos Altas, cerradas.
