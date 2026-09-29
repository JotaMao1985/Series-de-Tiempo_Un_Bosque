# Verificación de cifras · Capítulo 4 (diapositivas)

Generado por `verifica_cifras_cap4.py`. Cada fila es una cifra (o afirmación) de las diapositivas o de sus notas, con las fuentes contra las que se contrastó.

## Cómo se verificó

- **J** · JSON publicado `precalculo/salidas/cap4_arima.json` (R 4.6, forecast 9.0.2).
- **RJ** · el mismo JSON regenerado con `genera_cap4.R` en R version 4.3.3 (2024-02-29) (forecast 8.21.1, tseries 0.10.55): `regenerado_cap4_arima.json`.
- **RD** · recálculo directo sobre los datos crudos, `verifica_directo_cap4.R` → `directo_cap4.json`.
- **PY** · statsmodels 0.14.6, `verifica_python_cap4.py` → `directo_python_cap4.json`.
- **DOC** · documentación de R (`?Nile`, `?BJsales`, `?lynx`, `?AirPassengers`, `?arima`, `citation("forecast")`).
- **CALC** · aritmética sobre las fuentes anteriores. **C** · texto del capítulo. **A** · `PLAN_Auditoria_Cap4.md`.
- La fuente se redondea a los decimales que muestra la diapositiva, a la mitad hacia arriba.
- Los datos crudos de la TRM son la copia congelada de `datos_series.json` (consulta 2026-07-26); **no** se cotejaron con datos.gov.co.
- Las definiciones y equivalencias teóricas y las referencias bibliográficas se toman del capítulo; **los libros no estaban disponibles** y no se contrastaron.

## Resumen

- Cifras y afirmaciones registradas: **412**
- Verificadas contra al menos una fuente: **395**
- Definiciones o convenciones (nivel del 5 %, z = 1.96, etc.): **11**; no se miden, se enuncian
- Marcadas `[SIN VERIFICAR]` (no se presentan como dato confirmado): **6**
- No coinciden: **0**

Contrastes por tipo de fuente: A 3, C 3, CALC 80, DOC 31, J 219, PY 5, RD 180, RJ 179, RS 1.

## Código proyectado, ejecutado

Cada bloque `r` de la presentación se ejecutó en R version 4.3.3 (2024-02-29) y sus líneas de salida (`#>`) se compararon con la salida real.

| Bloque (primera línea) | Salidas esperadas | Encontradas | Estado |
|---|---|---|---|
| `library(forecast)` | 2 | 2 | coincide |
| `library(forecast)` | 2 | 2 | coincide |

## Lo que no se pudo verificar (`[SIN VERIFICAR]`)

| Diapositiva | Qué | Por qué |
|---|---|---|
| Tres series conducen el capítulo, y cada una enseña algo dis | origen de la TRM en datos.gov.co | no se pudo contrastar con la fuente primaria; solo con la copia congelada del repositorio |
| Box y Jenkins aportaron el método, no el modelo: un ciclo co | 1970 (edición de Time Series Analysis: Forecasting and Control) | la documentación de R (?BJsales) cita la edición de 1976; ninguna fuente de esta sesión confirma 1970 |
| El caso del Nilo, cerrado: un escalón en 1899 explica más qu | el descenso coincide con la construcción de la presa baja de Asuán | afirmación histórica del capítulo y del JSON (cambio_nivel.fuente); ninguna fuente de esta sesión la confirma |
| Para seguir: tres ejercicios y las lecturas del capítulo {co | FPP3, secciones 9.5 a 9.8 | las secciones salen del capítulo; no se tuvo el libro |
| Para seguir: tres ejercicios y las lecturas del capítulo {co | Shumway y Stoffer (2017), cap. 3 | año y capítulo salen del capítulo; no se tuvo el libro |
| Para seguir: tres ejercicios y las lecturas del capítulo {co | Box, Jenkins, Reinsel y Ljung (2015), caps. 4 a 8 | año y capítulos salen del capítulo; no se tuvo el libro |
| Cada cifra remite a una fuente; lo que no se pudo contrastar | la presa baja de Asuán · la edición de 1970 de Box y Jenkins · el signo de θ en Box y Jenkins · el origen de la TRM en datos.gov.co · las secciones y capítulos de las lecturas | ver la lista completa en verificacion_cifras.md |

## Observaciones sobre el material (no corregidas en silencio)

1. `?Nile` habla de un cambio «cerca de 1898»; el capítulo usa 1899 (observación 29) como primer año del nuevo nivel. No es un error: 1898 es el último año del nivel alto y 1899 el primero del bajo. Conviene decirlo así en clase.
2. `?BJsales` cita Box y Jenkins (1976), no 1970, y no dice «Serie M». El capítulo llama a BJsales «la Serie M del libro original de Box y Jenkins»: esa denominación no se pudo confirmar.
3. `citation("forecast")` imprime Hyndman y Khandakar como *26*(3), pero su DOI es 10.18637/jss.v027.i03 (volumen 27). El capítulo cita 27(3), coherente con el DOI. La discrepancia está en el texto de citación que imprime R.
4. Cobb (1978): `?Nile` da *Biometrika* 65, 243–251; el capítulo escribe 65(2). El volumen y las páginas coinciden; el número (2) no se pudo confirmar.
5. La raíz AR del ARIMA(2,1,2) del Nilo (Módulo 7, «1.001») depende del estimador: 1.0008 sin deriva y 1.0005 con deriva (`Arima`, CSS-ML), pero 2.24 con `arima(method = "ML")`, que es lo que trae la rejilla del JSON. Es coherente con lo que el capítulo dice de `auto.arima` (usa `Arima`), pero conviene no mezclar las dos cifras.
6. Módulo 10: «la varianza real de los cambios a 3–12 meses es entre 1.07 y 1.14 veces esa cifra» no se reproduce. El cálculo directo var(Δ_h)/(h·var(Δ₁)) da entre 1.02 y 1.20 para h = 3…12. No se usa en las diapositivas.
7. Las coberturas 83.9 % (Módulo 9) y 89.6 % (Módulo 10) vienen del Capítulo 6 (`cap6_evaluacion.json`), no del 4. No se proyectan; si se citan, la fuente es el Capítulo 6.
8. La tabla del Módulo 8 rotula d = 1 «Mínimo de varianza. Correcto.» aunque el mismo módulo dice que ese mínimo es por poco margen. Ya figuraba como pendiente en `PLAN_Auditoria_Cap4.md`; en las diapositivas se dejó «Mínimo de varianza».
9. `puente_estacional.advertencia_aicc` (JSON) dice «la MISMA diferenciación total (d + D*m distinta)», que se contradice a sí misma. Es texto interno del JSON; no se muestra en el capítulo.
10. Entre el JSON publicado (R 4.6, forecast 9.0.2) y el regenerado aquí (R 4.3.3, forecast 8.21.1) se compararon **3836** valores: **13** difieren más de 1.5 unidades del último decimal publicado, todos en modelos mal condicionados de la rejilla: ARIMA (2,1,2) de la TRM; ARIMA (2,1,2) del Nilo; ARIMA (2,2,2) del Nilo (σ², errores estándar, estadísticos t, coeficientes y raíces cercanas al círculo unitario). Ninguno se usa en las diapositivas: las cifras que sí se muestran se reproducen.

<details><summary>Los valores que difieren</summary>

| Ruta | Publicado | Regenerado |
|---|---|---|
| `nilo.rejilla.212.raices.ar.1` | 10.5373 | 10.5375 |
| `nilo.rejilla.212.raices.ma.1` | 10.7214 | 10.721 |
| `nilo.rejilla.222.sigma2` | 19932.19 | 19932.15 |
| `nilo.rejilla.222.coeficientes.0.t` | 2.2915 | 2.2917 |
| `nilo.rejilla.222.coeficientes.2.t` | -26.1021 | -26.1059 |
| `nilo.rejilla.222.coeficientes.3.t` | 12.0533 | 12.0552 |
| `nilo.rejilla.222.raices.ar.1` | 5.5426 | 5.5424 |
| `trm.rejilla.212.sigma2` | 13187.43 | 13188.21 |
| `trm.rejilla.212.coeficientes.0.t` | 40.1372 | 40.1507 |
| `trm.rejilla.212.coeficientes.1.t` | -94.7748 | -94.9263 |
| `trm.rejilla.212.coeficientes.2.t` | -25.9219 | -25.913 |
| `trm.rejilla.212.coeficientes.3.valor` | 1 | 0.9998 |
| `trm.rejilla.212.coeficientes.3.t` | 28.1573 | 28.2812 |

</details>


## Tabla de cifras

### Cada afirmación es un dato, una definición, una interpretación o una opinión

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `4.6` | versión | A: PLAN_Auditoria_Cap4.md contiene «R 4.6» | verificado |
| `4.3.3` | versión | RD: directo_cap4.json › entorno.R | verificado |

### Tres series conducen el capítulo, y cada una enseña algo distinto

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1871` | documentación | RD: directo_cap4.json › datos.nilo_inicio = 1871<br>DOC: documentación de R (doc.nile) contiene «1871-1970» | verificado |
| `1970` | documentación | RD: directo_cap4.json › datos.nilo_fin = 1970<br>DOC: documentación de R (doc.nile) contiene «1871-1970» | verificado |
| `100` | dato | RD: directo_cap4.json › datos.nilo_n = 100<br>J: cap4_arima.json › nilo.n = 100 | verificado |
| `10` | documentación | DOC: documentación de R (doc.nile) contiene «10^8 m^3» | verificado |
| `1978` | documentación | DOC: documentación de R (doc.nile) contiene «Cobb(1978)» | verificado |
| `2015` | dato | CALC: directo_cap4.json › datos.trm_inicio = 2015<br>RD: datos_series.json › trm.descripcion | verificado |
| `2026` | dato | CALC: directo_cap4.json › datos.trm_fin = 2026<br>RD: datos_series.json › trm.descripcion | verificado |
| `138` | dato | J: cap4_arima.json › trm.n = 138<br>RD: directo_cap4.json › datos.trm_n = 138 | verificado |
| `26` | dato | RD: datos_series.json › trm.fuente («consulta: 2026-07-26») | verificado |
| `1949` | documentación | RD: directo_cap4.json › datos.ap_inicio = 1949<br>DOC: documentación de R (doc.airpassengers) contiene «1949 to 1960» | verificado |
| `1960` | documentación | RD: directo_cap4.json › datos.ap_fin = 1960<br>DOC: documentación de R (doc.airpassengers) contiene «1949 to 1960» | verificado |
| `144` | dato | J: cap4_arima.json › puente_estacional.n = 144<br>RD: directo_cap4.json › datos.ap_n = 144 | verificado |
| `1976` | documentación | DOC: documentación de R (doc.airpassengers) contiene «(1976)» | verificado |
| `150` | documentación | RD: directo_cap4.json › datos.bjsales_n = 150<br>DOC: documentación de R (doc.bjsales) contiene «150 observations» | verificado |
| `1821` | documentación | RD: directo_cap4.json › datos.lynx_inicio = 1821<br>DOC: documentación de R (doc.lynx) contiene «1821-1934» | verificado |
| `1934` | documentación | RD: directo_cap4.json › datos.lynx_fin = 1934<br>DOC: documentación de R (doc.lynx) contiene «1821-1934» | verificado |

### Un ARIMA(1,1,1) es un ARMA(2,1) con una raíz unitaria impuesta

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.2544` | dato | J: cap4_arima.json › nilo.diagnostico.coeficientes.0.valor = 0.2544<br>RJ: regenerado (R 4.3.3) › nilo.diagnostico.coeficientes.0.valor = 0.2544 | verificado |
| `1.2544` | dato | RD: directo_cap4.json › m1.ar_expandido.0 = 1.2544<br>CALC: 1 + φ = 1.2544 | verificado |
| `-0.2544` | dato | RD: directo_cap4.json › m1.ar_expandido.1 = -0.2544<br>CALC: −φ = -0.2544 | verificado |
| `1.0000` | dato | RD: directo_cap4.json › m1.raices.0 = 1 | verificado |
| `3.9308` | dato | RD: directo_cap4.json › m1.raices.1 = 3.9308<br>CALC: 1/φ = 3.930818 | verificado |

### En el Nilo, diferenciar una vez casi no reduce la varianza

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1871` | documentación | RD: directo_cap4.json › datos.nilo_inicio = 1871<br>DOC: documentación de R (doc.nile) contiene «1871-1970» | verificado |
| `1970` | documentación | RD: directo_cap4.json › datos.nilo_fin = 1970<br>DOC: documentación de R (doc.nile) contiene «1871-1970» | verificado |
| `10` | documentación | DOC: documentación de R (doc.nile) contiene «10^8 m^3» | verificado |
| `100` | dato | RD: directo_cap4.json › m1.d0.n = 100<br>J: cap4_arima.json › nilo.varianzas.0.n_efectivo = 100 | verificado |
| `99` | dato | RD: directo_cap4.json › m1.d1.n = 99<br>J: cap4_arima.json › nilo.varianzas.1.n_efectivo = 99 | verificado |
| `98` | dato | RD: directo_cap4.json › m1.d2.n = 98<br>J: cap4_arima.json › nilo.varianzas.2.n_efectivo = 98 | verificado |
| `919.35` | dato | RD: directo_cap4.json › m1.d0.media = 919.35 | verificado |
| `-3.84` | dato | RD: directo_cap4.json › m1.d1.media = -3.84 | verificado |
| `-0.14` | dato | RD: directo_cap4.json › m1.d2.media = -0.14 | verificado |
| `28638` | dato | RD: directo_cap4.json › m1.d0.var = 28637.95<br>J: cap4_arima.json › nilo.varianzas.0.varianza = 28637.95<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.0.varianza = 28637.95 | verificado |
| `28268` | dato | RD: directo_cap4.json › m1.d1.var = 28268.34<br>J: cap4_arima.json › nilo.varianzas.1.varianza = 28268.34<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.1.varianza = 28268.34 | verificado |
| `80055` | dato | RD: directo_cap4.json › m1.d2.var = 80055.01<br>J: cap4_arima.json › nilo.varianzas.2.varianza = 80055.01<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.2.varianza = 80055.01 | verificado |
| `28268.34` | dato | RD: directo_cap4.json › m1.d1.var = 28268.34<br>J: cap4_arima.json › nilo.varianzas.1.varianza = 28268.34<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.1.varianza = 28268.34 | verificado |
| `28637.95` | dato | RD: directo_cap4.json › m1.d0.var = 28637.95<br>J: cap4_arima.json › nilo.varianzas.0.varianza = 28637.95<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.0.varianza = 28637.95 | verificado |
| `0.50` | dato | RD: directo_cap4.json › m1.d0.rho1 = 0.4984<br>J: cap4_arima.json › nilo.identificacion.cruda.acf.0 = 0.4984<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.0 = 0.4984 | verificado |
| `-0.40` | dato | RD: directo_cap4.json › m1.d1.rho1 = -0.402<br>J: cap4_arima.json › nilo.identificacion.d1.acf.0 = -0.402<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.acf.0 = -0.402 | verificado |
| `-0.63` | dato | RD: directo_cap4.json › m1.d2.rho1 = -0.6264<br>J: cap4_arima.json › nilo.identificacion.d2.acf.0 = -0.6264<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d2.acf.0 = -0.6264 | verificado |
| `1.3` | aritmética | CALC: reducción de la varianza de d=0 a d=1, en % = 1.29063 | verificado |
| `-1.3` | aritmética | CALC: variación de la varianza de d=0 a d=1, en % = -1.29063 | verificado |
| `-0.5` | definición | DEF: definición: ρ₁ de la diferencia de un ruido blanco es −1/2 | definición (no se mide) |
| `1899` | dato | CALC: año de la observación 29 (1871 + 29 − 1) = 1899 | verificado |

### Box y Jenkins aportaron el método, no el modelo: un ciclo con vueltas atrás

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1976` | documentación | DOC: documentación de R (doc.bjsales) contiene «Box & Jenkins (1976)» | verificado |
| `1970` | sin verificar | — (sin fuente en esta sesión) | SIN VERIFICAR |

### El ciclo completo cabe en un esqueleto corto de R {columnas=3:2}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.800` | dato | RD: directo_cap4.json › m2.lb20_p = 0.799737<br>J: cap4_arima.json › nilo.diagnostico.ljung_box_20.p = 0.7997<br>RJ: regenerado (R 4.3.3) › nilo.diagnostico.ljung_box_20.p = 0.7997 | verificado |
| `0.05` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `816.18` | dato | RD: directo_cap4.json › m2.pron_1a3.0 = 816.18 | verificado |
| `835.56` | dato | RD: directo_cap4.json › m2.pron_1a3.1 = 835.56 | verificado |
| `840.49` | dato | RD: directo_cap4.json › m2.pron_1a3.2 = 840.49 | verificado |
| `0.761` | dato | PY: directo_python_cap4.json › m2.lb20_statsmodels = 0.761 | verificado |

### Tres evidencias miran la serie desde ángulos distintos

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1899` | dato | CALC: año de la observación 29 (1871 + 29 − 1) = 1899 | verificado |
| `28638` | dato | RD: directo_cap4.json › m3.var_d0a3.0 = 28637.95<br>J: cap4_arima.json › nilo.varianzas.0.varianza = 28637.95<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.0.varianza = 28637.95 | verificado |
| `28268` | dato | RD: directo_cap4.json › m3.var_d0a3.1 = 28268.34<br>J: cap4_arima.json › nilo.varianzas.1.varianza = 28268.34<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.1.varianza = 28268.34 | verificado |
| `80055` | dato | RD: directo_cap4.json › m3.var_d0a3.2 = 80055.01<br>J: cap4_arima.json › nilo.varianzas.2.varianza = 80055.01<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.2.varianza = 80055.01 | verificado |
| `262507` | dato | RD: directo_cap4.json › m3.var_d0a3.3 = 262507.29<br>J: cap4_arima.json › nilo.varianzas.3.varianza = 262507.29<br>RJ: regenerado (R 4.3.3) › nilo.varianzas.3.varianza = 262507.29 | verificado |
| `-3.366` | dato | RD: directo_cap4.json › m3.adf_stat = -3.3657<br>J: cap4_arima.json › nilo.pruebas.adf_nivel.estadistico = -3.3657<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.adf_nivel.estadistico = -3.3657 | verificado |
| `0.064` | dato | RD: directo_cap4.json › m3.adf_p = 0.0642<br>J: cap4_arima.json › nilo.pruebas.adf_nivel.p = 0.0642<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.adf_nivel.p = 0.0642 | verificado |
| `0.965` | dato | RD: directo_cap4.json › m3.kpss_stat = 0.9654<br>J: cap4_arima.json › nilo.pruebas.kpss_nivel.estadistico = 0.9654<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.kpss_nivel.estadistico = 0.9654 | verificado |
| `0.01` (cota de la tabla: R imprime «p-value smaller than printed p-value» (p < 0.01)) | dato | RD: directo_cap4.json › m3.kpss_p = 0.01<br>J: cap4_arima.json › nilo.pruebas.kpss_nivel.p = 0.01<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.kpss_nivel.p = 0.01<br>RD: directo_cap4.json › m3.pp_p = 0.01<br>J: cap4_arima.json › nilo.pruebas.pp_nivel.p = 0.01<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.pp_nivel.p = 0.01 | verificado |
| `-6.690` | dato | RD: directo_cap4.json › m3.pp_stat = -6.6901<br>J: cap4_arima.json › nilo.pruebas.pp_nivel.estadistico = -6.6901<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.pp_nivel.estadistico = -6.6901 | verificado |
| `1.3` | aritmética | CALC: reducción de la varianza de d=0 a d=1, en % = 1.29063 | verificado |

### Las tres versiones de `ndiffs` no coinciden en el Nilo {columnas=1:1}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-4.05` | dato | RD: directo_cap4.json › m3.urdf_tau = -4.05 | verificado |
| `-2.89` | dato | RD: directo_cap4.json › m3.urdf_crit5 = -2.89 | verificado |
| `5` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `0.9654` | dato | RD: directo_cap4.json › m3.kpss_stat = 0.9654<br>J: cap4_arima.json › nilo.pruebas.kpss_nivel.estadistico = 0.9654<br>RJ: regenerado (R 4.3.3) › nilo.pruebas.kpss_nivel.estadistico = 0.9654 | verificado |
| `0.8691` | dato | PY: directo_python_cap4.json › m3.kpss_auto = 0.8691 | verificado |
| `0.5497` | dato | PY: directo_python_cap4.json › m3.kpss_legacy = 0.5497 | verificado |

### Ruido blanco puro con un escalón en 1899: ¿con qué frecuencia rechaza KPSS? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1899` | dato | CALC: año de la observación 29 (1871 + 29 − 1) = 1899 | verificado |
| `1000` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.n_replicas = 1000<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.n_replicas = 1000 | verificado |
| `100` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.n = 100<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.n = 100 | verificado |
| `127.03` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.sigma = 127.03<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.sigma = 127.03 | verificado |
| `29` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.posicion_escalon = 29<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.posicion_escalon = 29<br>RD: directo_cap4.json › m8.posicion_1899 = 29 | verificado |
| `5` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `2026` (semilla del experimento) | dato | RS: precalculo/genera_cap4.R contiene set.seed(2026) | verificado |
| `400` | dato | J: cap4_arima.json › nilo.cambio_nivel.malla_delta.n_replicas = 400<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.malla_delta.n_replicas = 400 | verificado |
| `4.8` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.sin_escalon.kpss_rechaza = 4.8<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.sin_escalon.kpss_rechaza = 4.8 | verificado |
| `247.8` | dato | J: cap4_arima.json › nilo.cambio_nivel.malla_delta.delta_del_nilo = 247.78<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.malla_delta.delta_del_nilo = 247.78 | verificado |
| `247.78` | dato | CALC: |δ| del Monte Carlo = 247.78<br>RD: directo_cap4.json › m8.escalon_coef = 247.78 | verificado |
| `1.95` | aritmética | CALC: |β|/σ = 247.78/127.03 = 1.950563 | verificado |
| `100` | dato | J: cap4_arima.json › nilo.cambio_nivel.malla_delta.puntos.4.delta = 100 | verificado |
| `100%` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.con_escalon.kpss_rechaza = 100<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.con_escalon.kpss_rechaza = 100 | verificado |
| `0.79` | aritmética | CALC: 100/σ = 100/127.03 = 0.787216<br>J: cap4_arima.json › nilo.cambio_nivel.malla_delta.puntos.4.salto_en_sigmas = 0.787 | verificado |
| `70.8` | dato | J: cap4_arima.json › nilo.cambio_nivel.malla_delta.puntos.4.kpss_rechaza = 70.75<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.malla_delta.puntos.4.kpss_rechaza = 70.75 | verificado |

### KPSS no distingue una raíz unitaria de un cambio de nivel {.idea etiqueta="Interpretación"}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `86.4` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.con_escalon.adf_test_no_rechaza = 86.4<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.con_escalon.adf_test_no_rechaza = 86.4 | verificado |
| `5.4` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.sin_escalon.adf_test_no_rechaza = 5.4<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.monte_carlo.sin_escalon.adf_test_no_rechaza = 5.4 | verificado |

### La ACF del Nilo sin diferenciar decae despacio: ¿qué se concluye sobre p y q? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.498` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.0 = 0.4984<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.0 = 0.4984<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.0 = 0.4984 | verificado |
| `0.385` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.1 = 0.3846<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.1 = 0.3846<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.1 = 0.3846 | verificado |
| `0.328` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.2 = 0.3279<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.2 = 0.3279<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.2 = 0.3279 | verificado |
| `0.239` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.3 = 0.2392<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.3 = 0.2392<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.3 = 0.2392 | verificado |
| `0.4984` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.0 = 0.4984<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.0 = 0.4984<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.0 = 0.4984 | verificado |
| `0.3846` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.1 = 0.3846<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.1 = 0.3846<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.1 = 0.3846 | verificado |
| `0.3279` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.2 = 0.3279<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.2 = 0.3279<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.2 = 0.3279 | verificado |
| `0.2392` | dato | J: cap4_arima.json › nilo.identificacion.cruda.acf.3 = 0.2392<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.acf.3 = 0.2392<br>RD: directo_cap4.json › m4.acf_sin_dif_1a4.3 = 0.2392 | verificado |
| `0.196` | dato | J: cap4_arima.json › nilo.identificacion.cruda.banda = 0.196<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.cruda.banda = 0.196 | verificado |
| `0.25` | aritmética | RD: directo_cap4.json › m4.ar1_phi05_rezagos2y3.0 = 0.25<br>CALC: φ² con φ = 0.5 = 0.25 | verificado |
| `0.125` | aritmética | RD: directo_cap4.json › m4.ar1_phi05_rezagos2y3.1 = 0.125<br>CALC: φ³ con φ = 0.5 = 0.125 | verificado |
| `0.5` | aritmética | CALC: ρ̂₁ ≈ 0.5 ⇒ φ ≈ 0.5 = 0.4984 | verificado |

### Sobre ∇Nilo la ACF corta en 1 y la PACF decae: la firma de un MA(1)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1.96` | definición | CALC: z de 0.975 = 1.959964 | verificado |
| `0.197` | dato | J: cap4_arima.json › nilo.identificacion.d1.banda = 0.197<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.banda = 0.197<br>RD: directo_cap4.json › m4.banda = 0.197 | verificado |
| `-0.402` | dato | J: cap4_arima.json › nilo.identificacion.d1.acf.0 = -0.402<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.acf.0 = -0.402<br>RD: directo_cap4.json › m4.acf_1a6.0 = -0.402 | verificado |
| `0.231` | dato | J: cap4_arima.json › nilo.identificacion.d1.acf.7 = 0.2312<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.acf.7 = 0.2312 | verificado |
| `0.2312` | dato | J: cap4_arima.json › nilo.identificacion.d1.acf.7 = 0.2312<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.acf.7 = 0.2312 | verificado |
| `-0.246` | dato | J: cap4_arima.json › nilo.identificacion.d1.pacf.1 = -0.2456<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.pacf.1 = -0.2456<br>RD: directo_cap4.json › m4.pacf_1a3.1 = -0.2456 | verificado |
| `-0.119` | dato | J: cap4_arima.json › nilo.identificacion.d1.pacf.2 = -0.1187<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.pacf.2 = -0.1187<br>RD: directo_cap4.json › m4.pacf_1a3.2 = -0.1187 | verificado |
| `20` | dato | J: cap4_arima.json › max_rezago = 20 | verificado |
| `5` | definición | DEF: nivel nominal convencional | definición (no se mide) |

### La tabla propone un ARIMA(0,1,1), pero se llevan varios candidatos, no uno

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-0.402` | dato | J: cap4_arima.json › nilo.identificacion.d1.acf.0 = -0.402<br>RJ: regenerado (R 4.3.3) › nilo.identificacion.d1.acf.0 = -0.402 | verificado |
| `-0.7329` | dato | RD: directo_cap4.json › m4.theta = -0.7329<br>J: cap4_arima.json › nilo.rejilla.011.coeficientes.0.valor = -0.7329<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.011.coeficientes.0.valor = -0.7329 | verificado |
| `0.1143` | dato | RD: directo_cap4.json › m4.theta_ee = 0.1143<br>J: cap4_arima.json › nilo.rejilla.011.coeficientes.0.ee = 0.1143<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.011.coeficientes.0.ee = 0.1143 | verificado |
| `-6.41` | dato | RD: directo_cap4.json › m4.theta_t = -6.41<br>CALC: θ̂/e.e. = -6.412073 | verificado |
| `0.674` | dato | RD: directo_cap4.json › m4.lb20_p = 0.673664<br>J: cap4_arima.json › nilo.rejilla.011.ljung_box_p = 0.6737<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.011.ljung_box_p = 0.6737 | verificado |
| `1.71` | aritmética | CALC: AICc(0,1,1) − AICc(1,1,1) en la búsqueda exhaustiva = 1.709 | verificado |
| `99` | dato | RD: directo_cap4.json › m1.d1.n = 99 | verificado |
| `el AICc prefiere (1,1,1) y el BIC (0,1,1)` (afirmación sin cifra) | dato | J: cap4_arima.json › nilo.mejor_por_d.d1 (AICc→111, BIC→011) | verificado |

### La constante \(c\) significa cosas distintas según \(d\)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `intercept` (afirmación sin cifra: R llama intercept a la media con d = 0) | dato | J: cap4_arima.json › nilo.rejilla.101.coeficientes contiene «intercept» | verificado |

### Cada programa trata la constante a su manera

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `4.3.3` | versión | RD: directo_cap4.json › entorno.R | verificado |
| `8.21.1` | versión | RD: directo_cap4.json › entorno.forecast | verificado |
| `0.14.6` | versión | PY: directo_python_cap4.json › entorno.statsmodels | verificado |
| `4.6` | versión | A: PLAN_Auditoria_Cap4.md contiene «R 4.6» | verificado |
| `9.0.2` | versión | A: PLAN_Auditoria_Cap4.md contiene «forecast 9.0.2» | verificado |
| `arima ignora include.mean con d ≥ 1` | comportamiento | RD: directo_cap4.json › m5.arima_d1_include_mean_coef == [ar1, ma1] | verificado |
| `Arima con d = 2 avisa y no ajusta deriva` | comportamiento | RD: directo_cap4.json › m5.d2_aviso, m5.d2_tiene_deriva | verificado |
| `auto.arima prueba con y sin deriva si d = 1` | comportamiento | RD: directo_cap4.json › m5.auto_d1_traza_* | verificado |
| `auto.arima con d = 2 nunca incluye deriva` | comportamiento | RD: directo_cap4.json › m5.auto_d2_* | verificado |
| `statsmodels: trend = c si d = 0, n si d > 0; t da deriva con d = 1; d ≥ 2 con t lanza ValueError` | comportamiento | PY: directo_python_cap4.json › m5.* | verificado |

### El Nilo no lleva deriva: no es significativa y el AICc empeora

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `-2.883` | dato | RD: directo_cap4.json › m5.deriva = -2.8827<br>J: cap4_arima.json › nilo.formas_pronostico.d1_deriva.coeficientes.2.valor = -2.8827<br>RJ: regenerado (R 4.3.3) › nilo.formas_pronostico.d1_deriva.coeficientes.2.valor = -2.8827 | verificado |
| `2.017` | dato | RD: directo_cap4.json › m5.deriva_ee = 2.0167<br>J: cap4_arima.json › nilo.formas_pronostico.d1_deriva.coeficientes.2.ee = 2.0167<br>RJ: regenerado (R 4.3.3) › nilo.formas_pronostico.d1_deriva.coeficientes.2.ee = 2.0167 | verificado |
| `-1.43` | dato | RD: directo_cap4.json › m5.deriva_t = -1.429<br>CALC: δ̂/e.e. (J) = -1.429414 | verificado |
| `1268.06` | dato | RD: directo_cap4.json › m5.aicc_con = 1268.063<br>J: cap4_arima.json › nilo.formas_pronostico.d1_deriva.aicc = 1268.06<br>RJ: regenerado (R 4.3.3) › nilo.formas_pronostico.d1_deriva.aicc = 1268.06 | verificado |
| `1267.51` | dato | RD: directo_cap4.json › m5.aicc_sin = 1267.507<br>J: cap4_arima.json › nilo.formas_pronostico.d1.aicc = 1267.51<br>RJ: regenerado (R 4.3.3) › nilo.formas_pronostico.d1.aicc = 1267.51 | verificado |
| `8.00` | dato | RD: directo_cap4.json › m5.trm_deriva = 8.0009<br>J: cap4_arima.json › trm.deriva.valor = 8.0009<br>RJ: regenerado (R 4.3.3) › trm.deriva.valor = 8.0009 | verificado |
| `10.36` | dato | RD: directo_cap4.json › m5.trm_deriva_ee = 10.3559<br>J: cap4_arima.json › trm.deriva.ee = 10.3559<br>RJ: regenerado (R 4.3.3) › trm.deriva.ee = 10.3559 | verificado |
| `0.77` | dato | RD: directo_cap4.json › m5.trm_deriva_t = 0.773<br>J: cap4_arima.json › trm.deriva.t = 0.7726<br>RJ: regenerado (R 4.3.3) › trm.deriva.t = 0.7726 | verificado |
| `1707.41` | dato | RD: directo_cap4.json › m5.trm_aicc_con = 1707.41<br>J: cap4_arima.json › trm.deriva.aicc = 1707.41<br>RJ: regenerado (R 4.3.3) › trm.deriva.aicc = 1707.41 | verificado |
| `1705.94` | dato | RD: directo_cap4.json › m5.trm_aicc_sin = 1705.94<br>J: cap4_arima.json › trm.caminata.aicc = 1705.94<br>RJ: regenerado (R 4.3.3) › trm.caminata.aicc = 1705.94 | verificado |
| `740` | dato | RD: directo_cap4.json › m5.nilo_1970 = 740<br>CALC: último dato del Nilo (datos_series.json) = 740 | verificado |
| `1120` | dato | RD: directo_cap4.json › m5.nilo_1871 = 1120<br>CALC: primer dato del Nilo (datos_series.json) = 1120 | verificado |
| `99` | dato | RD: directo_cap4.json › m1.d1.n = 99 | verificado |
| `-3.84` | aritmética | RD: directo_cap4.json › m5.media_dif = -3.84<br>CALC: (740 − 1120)/99 = -3.838384 | verificado |
| `247.8` | dato | RD: directo_cap4.json › m8.escalon_coef = 247.78 | verificado |
| `247.78` | dato | RD: directo_cap4.json › m8.escalon_coef = 247.78 | verificado |
| `-247.78` | dato | RD: directo_cap4.json › m8.escalon_coef = -247.78 | verificado |
| `-2.50` | aritmética | RD: directo_cap4.json › m5.aporte_escalon = -2.5<br>CALC: β̂/99 = -2.502828 | verificado |
| `2.9` | aritmética | CALC: |δ̂| = 2.8827 | verificado |
| `1899` | dato | CALC: año de la observación 29 (1871 + 29 − 1) = 1899 | verificado |
| `10` | documentación | DOC: documentación de R (doc.nile) contiene «10^8 m^3» | verificado |
| `138` | dato | J: cap4_arima.json › trm.n = 138 | verificado |
| `-2.8827` | dato | RD: directo_cap4.json › m5.deriva = -2.8827 | verificado |
| `2.0167` | dato | RD: directo_cap4.json › m5.deriva_ee = 2.0167 | verificado |
| `-1.429` | dato | RD: directo_cap4.json › m5.deriva_t = -1.429 | verificado |
| `8.0009` | dato | RD: directo_cap4.json › m5.trm_deriva = 8.0009<br>RD: directo_cap4.json › m5.trm_media_dif = 8.0009<br>CALC: (y_n − y_1)/(n − 1) sobre la TRM = 8.000876<br>J: cap4_arima.json › trm.deriva.valor = 8.0009<br>RJ: regenerado (R 4.3.3) › trm.deriva.valor = 8.0009 | verificado |
| `10.3559` | dato | RD: directo_cap4.json › m5.trm_deriva_ee = 10.3559<br>J: cap4_arima.json › trm.deriva.ee = 10.3559<br>RJ: regenerado (R 4.3.3) › trm.deriva.ee = 10.3559 | verificado |
| `0.773` | dato | RD: directo_cap4.json › m5.trm_deriva_t = 0.773 | verificado |

### El AICc solo compara modelos con el mismo d

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `99` | dato | J: cap4_arima.json › nilo.varianzas.1.n_efectivo = 99<br>RD: directo_cap4.json › m1.d1.n = 99 | verificado |
| `98` | dato | J: cap4_arima.json › nilo.varianzas.2.n_efectivo = 98<br>RD: directo_cap4.json › m1.d2.n = 98 | verificado |
| `100` | dato | J: cap4_arima.json › nilo.varianzas.0.n_efectivo = 100<br>RD: directo_cap4.json › m1.d0.n = 100 | verificado |

### AICc 1267.51 con un ARIMA(1,1,1) y 1264.60 con un ARIMA(1,2,2): ¿cuál eliges? {.pregunta}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1267.51` | dato | J: cap4_arima.json › nilo.rejilla.111.aicc = 1267.51<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.111.aicc = 1267.51 | verificado |
| `1264.60` | dato | J: cap4_arima.json › nilo.rejilla.122.aicc = 1264.6<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.122.aicc = 1264.6 | verificado |
| `100` | dato | RD: directo_cap4.json › m1.d0.n = 100 | verificado |
| `99` | dato | J: cap4_arima.json › nilo.rejilla.111.n_efectivo = 99 | verificado |
| `98` | dato | J: cap4_arima.json › nilo.rejilla.122.n_efectivo = 98 | verificado |
| `1.03` | dato | J: cap4_arima.json › nilo.rejilla.122.raices.min_ma = 1.0316<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.122.raices.min_ma = 1.0316 | verificado |
| `1.0316` | dato | J: cap4_arima.json › nilo.rejilla.122.raices.min_ma = 1.0316<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.122.raices.min_ma = 1.0316 | verificado |
| `27` | dato | CALC: número de modelos de la rejilla del Nilo = 27<br>CALC: ídem (regenerado) = 27 | verificado |

### Cada d se compara solo consigo mismo: el mínimo global es una trampa

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `100` | dato | J: cap4_arima.json › nilo.mejor_por_d.d0.n_efectivo = 100 | verificado |
| `99` | dato | J: cap4_arima.json › nilo.mejor_por_d.d1.n_efectivo = 99 | verificado |
| `98` | dato | J: cap4_arima.json › nilo.mejor_por_d.d2.n_efectivo = 98 | verificado |
| `1282.50` | dato | J: cap4_arima.json › nilo.mejor_por_d.d0.valor_aicc = 1282.5<br>RJ: regenerado (R 4.3.3) › nilo.mejor_por_d.d0.valor_aicc = 1282.5 | verificado |
| `1292.50` | dato | J: cap4_arima.json › nilo.mejor_por_d.d0.valor_bic = 1292.5<br>RJ: regenerado (R 4.3.3) › nilo.mejor_por_d.d0.valor_bic = 1292.5 | verificado |
| `1267.51` | dato | J: cap4_arima.json › nilo.mejor_por_d.d1.valor_aicc = 1267.51<br>RJ: regenerado (R 4.3.3) › nilo.mejor_por_d.d1.valor_aicc = 1267.51 | verificado |
| `1274.28` | dato | J: cap4_arima.json › nilo.mejor_por_d.d1.valor_bic = 1274.28<br>RJ: regenerado (R 4.3.3) › nilo.mejor_por_d.d1.valor_bic = 1274.28 | verificado |
| `1264.60` | dato | J: cap4_arima.json › nilo.mejor_por_d.d2.valor_aicc = 1264.6<br>RJ: regenerado (R 4.3.3) › nilo.mejor_por_d.d2.valor_aicc = 1264.6 | verificado |
| `1273.50` | dato | J: cap4_arima.json › nilo.mejor_por_d.d2.valor_bic = 1273.5<br>RJ: regenerado (R 4.3.3) › nilo.mejor_por_d.d2.valor_bic = 1273.5 | verificado |
| `1.000` | dato | J: cap4_arima.json › nilo.rejilla.022.raices.min_ma = 1<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.022.raices.min_ma = 1 | verificado |
| `1.0000` | dato | J: cap4_arima.json › nilo.rejilla.022.raices.min_ma = 1<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.022.raices.min_ma = 1 | verificado |
| `27` | dato | CALC: número de modelos de la rejilla del Nilo = 27 | verificado |
| `4.6` | aritmética | CALC: log 99 = 4.59512 | verificado |
| `modelos ganadores por d: (1,0,1)/(1,0,1), (1,1,1)/(0,1,1), (1,2,2)/(0,2,2)` (afirmación sin cifra) | dato | J: cap4_arima.json › nilo.mejor_por_d<br>RJ: regenerado › nilo.mejor_por_d | verificado |
| `cuatro modelos a menos de 2 puntos del mejor de d = 1` (afirmación en el pie de figura) | dato | J: cap4_arima.json › nilo.rejilla (d = 1, ΔAICc < 2 → 4 modelos) | verificado |

### `auto.arima` es un algoritmo con reglas explícitas, no una caja negra

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1.01` | documentación | RD: directo_cap4.json › m7.regla_raiz_1_01 (myarima: minroot < 1 + 0.01) | verificado |
| `1.001` (≈ 1.001: 1.0008 sin deriva, 1.0005 con deriva (Arima, CSS-ML); con arima(ML) sale 2.24) | dato | RD: directo_cap4.json › m7.raiz_ar_212_sin_deriva = 1.0008 | verificado |
| `1.0008` | dato | RD: directo_cap4.json › m7.raiz_ar_212_sin_deriva = 1.0008 | verificado |
| `1.0005` | dato | RD: directo_cap4.json › m7.raiz_ar_212_con_deriva = 1.0005 | verificado |
| `2.24` | dato | RD: directo_cap4.json › m7.raiz_ar_212_arima_ml = 2.2407<br>J: cap4_arima.json › nilo.rejilla.212.raices.min_ar = 2.2407 | verificado |
| `18` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.escalonada.n_modelos = 18<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.escalonada.n_modelos = 18 | verificado |
| `42` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.exhaustiva.n_modelos = 42<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.exhaustiva.n_modelos = 42 | verificado |
| `2008` | documentación | DOC: documentación de R (doc.citation_forecast) contiene «(2008)» | verificado |
| `150` | documentación | RD: directo_cap4.json › m7.regla_approximation | verificado |
| `12` | documentación | RD: directo_cap4.json › m7.regla_approximation | verificado |
| `100` | dato | J: cap4_arima.json › nilo.n = 100 | verificado |
| `10.18637` | documentación | DOC: documentación de R (doc.citation_forecast) contiene «10.18637/jss.v027.i03» | verificado |
| `26` (R imprime el volumen 26; el DOI corresponde al 27) | documentación | DOC: documentación de R (doc.citation_forecast) contiene «*26*(3)» | verificado |
| `27` | documentación | DOC: documentación de R (doc.citation_forecast) contiene «v027» | verificado |

### Cinco modelos quedan a 1.71 puntos de AICc: el ganador no está solo

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1267.507` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.exhaustiva.ranking.0.aicc = 1267.507<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.exhaustiva.ranking.0.aicc = 1267.507 | verificado |
| `1268.063` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.exhaustiva.ranking.1.aicc = 1268.063<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.exhaustiva.ranking.1.aicc = 1268.063 | verificado |
| `1268.210` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.exhaustiva.ranking.2.aicc = 1268.21<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.exhaustiva.ranking.2.aicc = 1268.21 | verificado |
| `1268.969` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.exhaustiva.ranking.3.aicc = 1268.969<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.exhaustiva.ranking.3.aicc = 1268.969 | verificado |
| `1269.216` | dato | J: cap4_arima.json › nilo.hyndman_khandakar.exhaustiva.ranking.4.aicc = 1269.216<br>RJ: regenerado (R 4.3.3) › nilo.hyndman_khandakar.exhaustiva.ranking.4.aicc = 1269.216 | verificado |
| `0.56` | aritmética | CALC: AICc del puesto 2 − AICc del puesto 1 = 0.556 | verificado |
| `0.70` | aritmética | CALC: AICc del puesto 3 − AICc del puesto 1 = 0.703 | verificado |
| `1.46` | aritmética | CALC: AICc del puesto 4 − AICc del puesto 1 = 1.462 | verificado |
| `1.71` | aritmética | CALC: AICc del puesto 5 − AICc del puesto 1 = 1.709 | verificado |
| `2` | opinión | DEF: regla de referencia habitual (opinión del capítulo) | definición (no se mide) |

### Módulos 8–9 · Diagnóstico y pronóstico {seccion=modulo-8}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.800` | dato | J: cap4_arima.json › nilo.diagnostico.ljung_box_20.p = 0.7997<br>RD: directo_cap4.json › m2.lb20_p = 0.799737 | verificado |
| `0.731` | dato | J: cap4_arima.json › nilo.diagnostico.shapiro_p = 0.7312<br>RJ: regenerado (R 4.3.3) › nilo.diagnostico.shapiro_p = 0.7312 | verificado |

### Diferenciar de más deja una firma exacta en el MA

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `28638` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.0.varianza = 28637.95<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.0.varianza = 28637.95 | verificado |
| `0.498` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.0.acf1 = 0.4984<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.0.acf1 = 0.4984 | verificado |
| `0.378` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.0.theta_ma1 = 0.3783<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.0.theta_ma1 = 0.3783 | verificado |
| `28268` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.1.varianza = 28268.34<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.1.varianza = 28268.34 | verificado |
| `-0.402` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.1.acf1 = -0.402<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.1.acf1 = -0.402 | verificado |
| `-0.733` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.1.theta_ma1 = -0.7329<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.1.theta_ma1 = -0.7329 | verificado |
| `80055` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.2.varianza = 80055.01<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.2.varianza = 80055.01 | verificado |
| `-0.626` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.2.acf1 = -0.6264<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.2.acf1 = -0.6264 | verificado |
| `-1.000` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.2.theta_ma1 = -1<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.2.theta_ma1 = -1 | verificado |
| `262507` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.3.varianza = 262507.29<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.3.varianza = 262507.29 | verificado |
| `-0.719` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.3.acf1 = -0.7188<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.3.acf1 = -0.7188 | verificado |
| `-1.000` | dato | J: cap4_arima.json › nilo.sobrediferenciacion.3.theta_ma1 = -1<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.3.theta_ma1 = -1 | verificado |
| `1.000` (los cuatro modelos degenerados con d = 2: (0,2,1), (0,2,2), (1,2,1), (2,2,1)) | dato | J: cap4_arima.json › nilo.rejilla.021.raices.min_ma = 1<br>J: cap4_arima.json › nilo.rejilla.022.raices.min_ma = 1<br>J: cap4_arima.json › nilo.rejilla.121.raices.min_ma = 1<br>J: cap4_arima.json › nilo.rejilla.221.raices.min_ma = 1<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.021.raices.min_ma = 1<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.022.raices.min_ma = 1<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.121.raices.min_ma = 1<br>RJ: regenerado (R 4.3.3) › nilo.rejilla.221.raices.min_ma = 1 | verificado |
| `28268.34` (σ̂² del MA(1) con d=2 = Var(∇y)) | dato | J: cap4_arima.json › nilo.sobrediferenciacion.2.sigma2_ma1 = 28268.34<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.2.sigma2_ma1 = 28268.34<br>J: cap4_arima.json › nilo.sobrediferenciacion.1.varianza = 28268.34<br>RJ: regenerado (R 4.3.3) › nilo.sobrediferenciacion.1.varianza = 28268.34 | verificado |
| `solo esos cuatro de los nueve modelos con d = 2 son degenerados` | dato | J: cap4_arima.json › nilo.rejilla (d = 2, degenerado)<br>RJ: regenerado › nilo.rejilla (d = 2, degenerado)<br>J: cap4_arima.json › nueve modelos con d = 2 | verificado |

### La regla de la varianza es un aviso, no un teorema: en log(lynx) falla

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1.653` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3.0 = 1.6532 | verificado |
| `0.687` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3.1 = 0.6871 | verificado |
| `0.603` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3.2 = 0.6026 | verificado |
| `1.153` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3.3 = 1.1532 | verificado |
| `58` | dato | RD: directo_cap4.json › m8.lynx_reduccion_pct = 58.4 | verificado |
| `1.653` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3.0 = 1.6532 | verificado |
| `0.687` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3.1 = 0.6871 | verificado |
| `0.10` | dato | RD: directo_cap4.json › m8.lynx_kpss_p = 0.1 | verificado |
| `0.01` | dato | RD: directo_cap4.json › m8.lynx_adf_p = 0.01 | verificado |
| `1.000` | dato | RD: directo_cap4.json › m8.lynx_211_raiz_ma = 1 | verificado |
| `1.0000` | dato | RD: directo_cap4.json › m8.lynx_211_raiz_ma = 1 | verificado |
| `1821` | documentación | RD: directo_cap4.json › datos.lynx_inicio = 1821<br>DOC: documentación de R (doc.lynx) contiene «1821-1934» | verificado |
| `1934` | documentación | RD: directo_cap4.json › datos.lynx_fin = 1934<br>DOC: documentación de R (doc.lynx) contiene «1821-1934» | verificado |
| `114` | dato | RD: directo_cap4.json › datos.lynx_n = 114 | verificado |
| `10` (ciclo de unos 10 años: el AR(2) da un periodo de 9.78) | dato | RD: directo_cap4.json › m8.lynx_ar2.3 = 9.7839 | verificado |
| `1991` | documentación | DOC: documentación de R (doc.lynx) contiene «Brockwell & Davis (1991)» | verificado |
| `0.0094` | dato | RD: directo_cap4.json › m8.lynx_ar2_lb20_p = 0.009434 | verificado |
| `9.78` | dato | RD: directo_cap4.json › m8.lynx_ar2.3 = 9.7839 | verificado |
| `el mínimo de la varianza de log(lynx) está en d = 2; ndiffs kpss y adf dan 0` | dato | RD: directo_cap4.json › m8.lynx_var_d0a3, m8.lynx_ndiffs | verificado |
| `el AR(2) sin diferenciar no pasa Ljung–Box y auto.arima propone un ARMA(2,3)` | dato | RD: directo_cap4.json › m8.lynx_ar2_lb20_p, m8.lynx_auto | verificado |

### El caso del Nilo, cerrado: un escalón en 1899 explica más que una raíz unitaria

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1899` | dato | CALC: año de la observación 29 (1871 + 29 − 1) = 1899 | verificado |
| `-247.78` | dato | J: cap4_arima.json › nilo.cambio_nivel.escalon.coef = -247.78<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.escalon.coef = -247.78<br>RD: directo_cap4.json › m8.escalon_coef = -247.78 | verificado |
| `28.15` | dato | J: cap4_arima.json › nilo.cambio_nivel.escalon.ee = 28.15<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.escalon.ee = 28.15<br>RD: directo_cap4.json › m8.escalon_ee = 28.15 | verificado |
| `-8.80` | dato | J: cap4_arima.json › nilo.cambio_nivel.escalon.t = -8.8<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.escalon.t = -8.8<br>RD: directo_cap4.json › m8.escalon_t = -8.8 | verificado |
| `1097.75` | dato | J: cap4_arima.json › nilo.cambio_nivel.media_antes = 1097.75<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.media_antes = 1097.75<br>RD: directo_cap4.json › m8.media_antes_1899 = 1097.75 | verificado |
| `849.97` | dato | J: cap4_arima.json › nilo.cambio_nivel.media_despues = 849.97<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.media_despues = 849.97<br>RD: directo_cap4.json › m8.media_desde_1899 = 849.97 | verificado |
| `1257.91` | dato | J: cap4_arima.json › nilo.cambio_nivel.escalon.aicc = 1257.91<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.escalon.aicc = 1257.91 | verificado |
| `1282.50` | dato | J: cap4_arima.json › nilo.cambio_nivel.mejor_d0_rejilla = 1282.5<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.mejor_d0_rejilla = 1282.5 | verificado |
| `25` | aritmética | CALC: 1282.50 − 1257.91 = 24.59 («casi 25») = 24.59 | verificado |
| `0.812` | dato | J: cap4_arima.json › nilo.cambio_nivel.escalon.ljung_box_20_p = 0.8124<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.escalon.ljung_box_20_p = 0.8124<br>RD: directo_cap4.json › m8.escalon_lb20_p = 0.8124 | verificado |
| `-0.874` | dato | J: cap4_arima.json › nilo.diagnostico.coeficientes.1.valor = -0.8741<br>RJ: regenerado (R 4.3.3) › nilo.diagnostico.coeficientes.1.valor = -0.8741 | verificado |
| `1978` | documentación | DOC: documentación de R (doc.nile) contiene «Cobb(1978)» | verificado |
| `1898` | documentación | DOC: documentación de R (doc.nile) contiene «changepoint near 1898» | verificado |
| `1.006` | dato | RD: directo_cap4.json › m1.razon = 1.006 | verificado |
| `32.8` | dato | RD: directo_cap4.json › m1.razon_sin_ma = 32.8 | verificado |
| `100` | dato | J: cap4_arima.json › nilo.cambio_nivel.monte_carlo.con_escalon.kpss_rechaza = 100 | verificado |
| `29` | dato | RD: directo_cap4.json › m8.posicion_1899 = 29 | verificado |

### Fuera de muestra el escalón no pronostica mejor: gana el naïve

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `123.06` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.3.rmse = 123.06<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.3.rmse = 123.06 | verificado |
| `101.95` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.3.mae = 101.95<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.3.mae = 101.95 | verificado |
| `125.05` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.0.rmse = 125.05<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.0.rmse = 125.05 | verificado |
| `106.16` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.0.mae = 106.16<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.0.mae = 106.16 | verificado |
| `127.99` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.1.rmse = 127.99<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.1.rmse = 127.99 | verificado |
| `106.99` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.1.mae = 106.99<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.1.mae = 106.99 | verificado |
| `128.31` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.2.rmse = 128.31<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.2.rmse = 128.31 | verificado |
| `107.40` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.2.mae = 107.4<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.2.mae = 107.4 | verificado |
| `133.31` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.4.rmse = 133.31<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.4.rmse = 133.31 | verificado |
| `108.01` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos.4.mae = 108.01<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.modelos.4.mae = 108.01 | verificado |
| `orden de la tabla: naïve, ARIMA(1,1,1), escalón, escalón + AR(1), media` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.modelos (etiquetas) | verificado |
| `1899` | dato | CALC: año de la observación 29 (1871 + 29 − 1) = 1899 | verificado |
| `1871` | dato | RD: directo_cap4.json › datos.nilo_inicio = 1871 | verificado |
| `1950` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.corte = 1950<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.corte = 1950 | verificado |
| `80` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.n_entrenamiento = 80<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.n_entrenamiento = 80<br>CALC: 1950 − 1871 + 1 = 80 | verificado |
| `20` | dato | J: cap4_arima.json › nilo.cambio_nivel.fuera_muestra.h = 20<br>RJ: regenerado (R 4.3.3) › nilo.cambio_nivel.fuera_muestra.h = 20 | verificado |
| `123` | aritmética | CALC: RMSE mínimo = 123.06 | verificado |
| `133` | aritmética | CALC: RMSE máximo = 133.31 | verificado |
| `139.67` | dato | RD: directo_cap4.json › m8.sd_res_111_todos = 139.67 | verificado |
| `25` | aritmética | CALC: 1282.50 − 1257.91 = 24.59 = 24.59 | verificado |
| `100` | dato | RD: directo_cap4.json › datos.nilo_n = 100 | verificado |

### La forma del pronóstico a largo plazo la deciden d y la constante

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `95` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `0.25` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d0.primera_dif_h30 = 0.2535<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d0.primera_dif_h30 = 0.2535 | verificado |
| `561` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d0.ancho95_h1 = 561.34<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d0.ancho95_h1 = 561.34 | verificado |
| `677` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d0.ancho95_h30 = 677.33<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d0.ancho95_h30 = 677.33 | verificado |
| `0.00` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1.primera_dif_h30 = 0<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1.primera_dif_h30 = 0 | verificado |
| `557` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1.ancho95_h1 = 556.81<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1.ancho95_h1 = 556.81 | verificado |
| `781` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1.ancho95_h30 = 781.49<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1.ancho95_h30 = 781.49 | verificado |
| `-2.88` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1_deriva.primera_dif_h30 = -2.8827<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1_deriva.primera_dif_h30 = -2.8827 | verificado |
| `555` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1_deriva.ancho95_h1 = 554.53<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1_deriva.ancho95_h1 = 554.53 | verificado |
| `708` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1_deriva.ancho95_h30 = 708.25<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1_deriva.ancho95_h30 = 708.25 | verificado |
| `-4.05` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d2.primera_dif_h30 = -4.0493<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d2.primera_dif_h30 = -4.0493 | verificado |
| `613` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d2.ancho95_h1 = 612.78<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d2.ancho95_h1 = 612.78 | verificado |
| `2771` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d2.ancho95_h30 = 2771.45<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d2.ancho95_h30 = 2771.45 | verificado |
| `3.5` | aritmética | CALC: ancho(d=2)/ancho(d=1) en h = 30 = 3.546367 | verificado |
| `3.55` | aritmética | CALC: ancho(d=2)/ancho(d=1) en h = 30 = 3.546367 | verificado |
| `2771` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d2.ancho95_h30 = 2771.45<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d2.ancho95_h30 = 2771.45 | verificado |
| `781` | dato | J: cap4_arima.json › nilo.intervalos.forma_medida.d1.ancho95_h30 = 781.49<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.forma_medida.d1.ancho95_h30 = 781.49 | verificado |
| `30` | dato | J: cap4_arima.json › horizonte = 30 | verificado |
| `-0.39` (φ̂ del ARIMA(1,2,1)) | dato | J: cap4_arima.json › nilo.formas_pronostico.d2.coeficientes.0.valor = -0.3924 | verificado |

### El ancho del intervalo sale de los pesos ψ de la representación MA(∞)

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.1688` | dato | J: cap4_arima.json › nilo.intervalos.psi_limite = 0.1688<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.psi_limite = 0.1688 | verificado |
| `9.08` (9.078 × 10⁻¹¹) | dato | J: cap4_arima.json › nilo.intervalos.error_maximo_verificacion = 9.078 | verificado |
| `error de reconstrucción del orden de 10⁻¹⁰ (< 1e-10)` | dato | J: cap4_arima.json › nilo.intervalos.error_maximo_verificacion < 1e-10 | verificado |

### En el Nilo la incertidumbre crece casi cuatro veces menos que en una caminata aleatoria

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.169` | dato | J: cap4_arima.json › nilo.intervalos.psi_limite = 0.1688<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.psi_limite = 0.1688 | verificado |
| `30` | dato | J: cap4_arima.json › horizonte = 30 | verificado |
| `199.4` | dato | J: cap4_arima.json › nilo.intervalos.sigma_h.29 = 199.363<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.sigma_h.29 = 199.363<br>RD: directo_cap4.json › m9.nilo_sigma30 = 199.363 | verificado |
| `778.0` | aritmética | RD: directo_cap4.json › m9.nilo_caminata30 = 778<br>CALC: σ̂·√30 = 778.012507 | verificado |
| `2.99` | dato | RD: directo_cap4.json › m9.bj_psi_limite = 2.9883 | verificado |
| `12` | definición | DEF: horizonte h = 12 del ejercicio 3 | definición (no se mide) |
| `1.96` | dato | RD: directo_cap4.json › m9.bj_sigma12_sobre_caminata = 1.9619 | verificado |
| `-0.874` | dato | J: cap4_arima.json › nilo.diagnostico.coeficientes.1.valor = -0.8741<br>RJ: regenerado (R 4.3.3) › nilo.diagnostico.coeficientes.1.valor = -0.8741 | verificado |
| `150` | documentación | RD: directo_cap4.json › datos.bjsales_n = 150<br>DOC: documentación de R (doc.bjsales) contiene «150 observations» | verificado |
| `142.045` | dato | J: cap4_arima.json › nilo.intervalos.sigma = 142.045<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.sigma = 142.045<br>RD: directo_cap4.json › m9.nilo_sigma = 142.045 | verificado |
| `2.56` | dato | RD: directo_cap4.json › m9.bj_psi12 = 2.5593 | verificado |
| `casi cuatro veces menos: 778.0/199.4 ≈ 3.9` | aritmética | CALC: 778.0/199.4 = 3.90 | verificado |

### Módulo 10 · Caso TRM, puente y cierre {seccion=modulo-10}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `2015` | dato | CALC: directo_cap4.json › datos.trm_inicio = 2015 | verificado |
| `2026` | dato | CALC: directo_cap4.json › datos.trm_fin = 2026 | verificado |
| `138` | dato | J: cap4_arima.json › trm.n = 138<br>RD: directo_cap4.json › datos.trm_n = 138 | verificado |

### Sobre la TRM, las cuatro pruebas dicen d = 1

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `2015` | dato | CALC: directo_cap4.json › datos.trm_inicio = 2015 | verificado |
| `2026` | dato | CALC: directo_cap4.json › datos.trm_fin = 2026 | verificado |
| `138` | dato | J: cap4_arima.json › trm.n = 138<br>RD: directo_cap4.json › datos.trm_n = 138 | verificado |
| `26` | dato | RD: datos_series.json › trm.fuente («consulta: 2026-07-26») | verificado |
| `-1.978` | dato | J: cap4_arima.json › trm.pruebas.adf_nivel.estadistico = -1.9783<br>RJ: regenerado (R 4.3.3) › trm.pruebas.adf_nivel.estadistico = -1.9783 | verificado |
| `0.586` | dato | J: cap4_arima.json › trm.pruebas.adf_nivel.p = 0.5855<br>RJ: regenerado (R 4.3.3) › trm.pruebas.adf_nivel.p = 0.5855 | verificado |
| `-3.880` | dato | J: cap4_arima.json › trm.pruebas.adf_d1.estadistico = -3.8801<br>RJ: regenerado (R 4.3.3) › trm.pruebas.adf_d1.estadistico = -3.8801 | verificado |
| `0.017` | dato | J: cap4_arima.json › trm.pruebas.adf_d1.p = 0.0172<br>RJ: regenerado (R 4.3.3) › trm.pruebas.adf_d1.p = 0.0172 | verificado |
| `2.243` | dato | J: cap4_arima.json › trm.pruebas.kpss_nivel.estadistico = 2.2427<br>RJ: regenerado (R 4.3.3) › trm.pruebas.kpss_nivel.estadistico = 2.2427 | verificado |
| `0.01` (cota de la tabla (p < 0.01)) | dato | J: cap4_arima.json › trm.pruebas.kpss_nivel.p = 0.01<br>RJ: regenerado (R 4.3.3) › trm.pruebas.kpss_nivel.p = 0.01 | verificado |
| `0.242` | dato | J: cap4_arima.json › trm.pruebas.kpss_d1.estadistico = 0.2415<br>RJ: regenerado (R 4.3.3) › trm.pruebas.kpss_d1.estadistico = 0.2415 | verificado |
| `0.10` (cota de la tabla (p > 0.10)) | dato | J: cap4_arima.json › trm.pruebas.kpss_d1.p = 0.1<br>RJ: regenerado (R 4.3.3) › trm.pruebas.kpss_d1.p = 0.1 | verificado |
| `0.088` | dato | J: cap4_arima.json › trm.identificacion.d1.acf.0 = 0.0876<br>RJ: regenerado (R 4.3.3) › trm.identificacion.d1.acf.0 = 0.0876 | verificado |
| `0.0876` | dato | J: cap4_arima.json › trm.identificacion.d1.acf.0 = 0.0876<br>RJ: regenerado (R 4.3.3) › trm.identificacion.d1.acf.0 = 0.0876<br>RD: directo_cap4.json › m10.acf_dif_rezago1 = 0.0876 | verificado |
| `0.167` | aritmética | CALC: 1.96/√137 (sin doble redondeo) = 0.167454 | verificado |
| `0.1675` | dato | J: cap4_arima.json › trm.identificacion.d1.banda = 0.1675<br>RJ: regenerado (R 4.3.3) › trm.identificacion.d1.banda = 0.1675 | verificado |
| `-0.190` | dato | J: cap4_arima.json › trm.identificacion.d1.acf.7 = -0.1903<br>RJ: regenerado (R 4.3.3) › trm.identificacion.d1.acf.7 = -0.1903 | verificado |
| `-0.1903` | dato | J: cap4_arima.json › trm.identificacion.d1.acf.7 = -0.1903<br>RJ: regenerado (R 4.3.3) › trm.identificacion.d1.acf.7 = -0.1903 | verificado |
| `0.964` | dato | J: cap4_arima.json › trm.identificacion.cruda.acf.0 = 0.9637<br>RJ: regenerado (R 4.3.3) › trm.identificacion.cruda.acf.0 = 0.9637 | verificado |
| `5` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `nsdiffs = 0` | dato | J: cap4_arima.json › trm.pruebas.nsdiffs == 0<br>RJ: regenerado › trm.pruebas.nsdiffs == 0 | verificado |
| `las cuatro pruebas coinciden en d = 1` | dato | J: cap4_arima.json › trm.pruebas (4 pruebas) | verificado |

### El mínimo de AICc es un modelo degenerado, y `auto.arima` elige la caminata aleatoria {columnas=1:1}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1703.38` | dato | J: cap4_arima.json › trm.minimo_degenerado.aicc = 1703.38<br>RJ: regenerado (R 4.3.3) › trm.minimo_degenerado.aicc = 1703.38<br>J: cap4_arima.json › trm.rejilla.212.aicc = 1703.38<br>RJ: regenerado (R 4.3.3) › trm.rejilla.212.aicc = 1703.38 | verificado |
| `2.56` | aritmética | CALC: −ventaja_aicc = 2.56<br>CALC: AICc(0,1,0) − AICc(2,1,2) = 2.56 | verificado |
| `1708.83` | dato | J: cap4_arima.json › trm.rejilla.010.bic = 1708.83<br>RJ: regenerado (R 4.3.3) › trm.rejilla.010.bic = 1708.83<br>J: cap4_arima.json › trm.caminata.bic = 1708.83<br>RJ: regenerado (R 4.3.3) › trm.caminata.bic = 1708.83 | verificado |
| `1.0042` | dato | J: cap4_arima.json › trm.minimo_degenerado.raices_ar.0 = 1.0042<br>RJ: regenerado (R 4.3.3) › trm.minimo_degenerado.raices_ar.0 = 1.0042 | verificado |
| `1.0000` (modelo degenerado: 1 en R 4.6 y 1.0001 en R 4.3.3) | dato | J: cap4_arima.json › trm.minimo_degenerado.raices_ma.0 = 1<br>RJ: regenerado (R 4.3.3) › trm.minimo_degenerado.raices_ma.0 = 1.0001 | verificado |
| `192` | dato | J: cap4_arima.json › trm.auto_arima.n_modelos = 192<br>RJ: regenerado (R 4.3.3) › trm.auto_arima.n_modelos = 192 | verificado |
| `0.189` | dato | J: cap4_arima.json › trm.caminata.ljung_box_20_p = 0.189<br>RJ: regenerado (R 4.3.3) › trm.caminata.ljung_box_20_p = 0.189 | verificado |
| `0.206` | dato | J: cap4_arima.json › trm.caminata.ljung_box_12_p = 0.2059<br>RJ: regenerado (R 4.3.3) › trm.caminata.ljung_box_12_p = 0.2059 | verificado |
| `0.0006` | dato | J: cap4_arima.json › trm.caminata.shapiro_p = 0.0006<br>RJ: regenerado (R 4.3.3) › trm.caminata.shapiro_p = 0.0006 | verificado |
| `8.00` | dato | J: cap4_arima.json › trm.deriva.valor = 8.0009<br>RJ: regenerado (R 4.3.3) › trm.deriva.valor = 8.0009<br>RD: directo_cap4.json › m5.trm_deriva = 8.0009 | verificado |
| `10.36` | dato | J: cap4_arima.json › trm.deriva.ee = 10.3559<br>RJ: regenerado (R 4.3.3) › trm.deriva.ee = 10.3559<br>RD: directo_cap4.json › m5.trm_deriva_ee = 10.3559 | verificado |
| `0.77` | dato | J: cap4_arima.json › trm.deriva.t = 0.7726<br>RJ: regenerado (R 4.3.3) › trm.deriva.t = 0.7726<br>RD: directo_cap4.json › m5.trm_deriva_t = 0.773 | verificado |
| `0.661` | dato | CALC: φ̂₁ del (2,1,2) = 0.6612<br>CALC: φ̂₁ (regenerado) = 0.6612 | verificado |
| `0.992` | dato | CALC: −φ̂₂ del (2,1,2) = 0.9917<br>CALC: −φ̂₂ (regenerado) = 0.9917 | verificado |
| `0.623` | dato | CALC: −θ̂₁ del (2,1,2) = 0.6226<br>CALC: −θ̂₁ (regenerado) = 0.6226 | verificado |
| `1.000` | dato | CALC: θ̂₂ del (2,1,2) = 1<br>CALC: θ̂₂ (regenerado) = 0.9998 | verificado |
| `1.01` | documentación | RD: directo_cap4.json › m7.regla_raiz_1_01 (myarima: minroot < 1 + 0.01) | verificado |
| `el mínimo de AICc es el (2,1,2) y el de BIC el (0,1,0); auto.arima elige (0,1,0)` | dato | J: cap4_arima.json › trm.mejor_aicc, trm.mejor_bic, trm.auto_arima<br>RJ: regenerado › ídem | verificado |

### A dos años, el intervalo del 95 % abarca un tercio del nivel

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `95` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `80` | definición | DEF: nivel nominal convencional | definición (no se mide) |
| `2026` | dato | CALC: año del mes h = 1 desde jun 2026 = 2026 | verificado |
| `2027` | dato | CALC: año del mes h = 12 desde jun 2026 = 2027 | verificado |
| `2028` | dato | CALC: año del mes h = 24 desde jun 2026 = 2028 | verificado |
| `238.09` | dato | RD: directo_cap4.json › m10.tabla.0.semiancho = 238.09<br>CALC: z·σ̂ = 238.088274 | verificado |
| `3259.00` | dato | RD: directo_cap4.json › m10.tabla.0.lo = 3259 | verificado |
| `3735.18` | dato | RD: directo_cap4.json › m10.tabla.0.hi = 3735.18 | verificado |
| `6.8` | dato | RD: directo_cap4.json › m10.tabla.0.pct = 6.8 | verificado |
| `824.76` | dato | RD: directo_cap4.json › m10.tabla.3.semiancho = 824.76<br>CALC: z·σ̂·√12 = 824.761974 | verificado |
| `2672.33` | dato | RD: directo_cap4.json › m10.tabla.3.lo = 2672.33 | verificado |
| `4321.85` | dato | RD: directo_cap4.json › m10.tabla.3.hi = 4321.85 | verificado |
| `23.6` | dato | RD: directo_cap4.json › m10.tabla.3.pct = 23.6 | verificado |
| `1166.39` | dato | RD: directo_cap4.json › m10.tabla.4.semiancho = 1166.39<br>CALC: z·σ̂·√24 = 1166.389569 | verificado |
| `2330.70` | dato | RD: directo_cap4.json › m10.tabla.4.lo = 2330.7 | verificado |
| `4663.48` | dato | RD: directo_cap4.json › m10.tabla.4.hi = 4663.48 | verificado |
| `33.4` | dato | RD: directo_cap4.json › m10.tabla.4.pct = 33.4 | verificado |
| `3497.09` | dato | RD: directo_cap4.json › datos.trm_ultimo = 3497.09<br>CALC: último dato de la TRM (datos_series.json) = 3497.09 | verificado |
| `121.48` | dato | RD: directo_cap4.json › m10.sigma = 121.48<br>CALC: √σ̂² (J trm.caminata.sigma2) = 121.475841 | verificado |
| `4.90` | aritmética | CALC: σ₂₄/σ₁ = √24 = 4.898979 | verificado |
| `1.40` | dato | J: cap4_arima.json › nilo.intervalos.razon_h1_h30 = 1.404<br>RJ: regenerado (R 4.3.3) › nilo.intervalos.razon_h1_h30 = 1.404 | verificado |
| `30` | dato | J: cap4_arima.json › horizonte = 30 | verificado |
| `5.48` | aritmética | CALC: √30 = 5.477226 | verificado |
| `137` | dato | RD: directo_cap4.json › m10.n_cambios_1m = 137<br>CALC: n − 1 = 137 | verificado |
| `4.4` | aritmética | CALC: 6/137 en % = 4.379562 | verificado |
| `11` | dato | RD: directo_cap4.json › m10.fuera_12m = 11 | verificado |
| `126` | dato | RD: directo_cap4.json › m10.n_cambios_12m = 126<br>CALC: n − 12 = 126 | verificado |
| `8.7` | aritmética | CALC: 11/126 en % = 8.730159 | verificado |
| `1.959964` | definición | CALC: cuantil 0.975 de la normal = 1.959964 | verificado |
| `6 de 137 cambios mensuales caen fuera del 95 %, 5 de ellos por arriba` | dato | RD: directo_cap4.json › m10.fuera_1m, m10.fuera_1m_arriba | verificado |

### Sin estacionalidad el diagnóstico rechaza: el puente al Capítulo 5

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `0.7245` | dato | J: cap4_arima.json › puente_estacional.no_estacional.acf_12 = 0.7245<br>RJ: regenerado (R 4.3.3) › puente_estacional.no_estacional.acf_12 = 0.7245 | verificado |
| `0.6727` | dato | J: cap4_arima.json › puente_estacional.no_estacional.acf_24 = 0.6727<br>RJ: regenerado (R 4.3.3) › puente_estacional.no_estacional.acf_24 = 0.6727 | verificado |
| `0.1633` | dato | J: cap4_arima.json › puente_estacional.no_estacional.banda = 0.1633<br>RJ: regenerado (R 4.3.3) › puente_estacional.no_estacional.banda = 0.1633 | verificado |
| `222.4` | dato | J: cap4_arima.json › puente_estacional.no_estacional.ljung_box_24.Q = 222.398<br>RJ: regenerado (R 4.3.3) › puente_estacional.no_estacional.ljung_box_24.Q = 222.398 | verificado |
| `-0.0515` | dato | J: cap4_arima.json › puente_estacional.estacional.acf_residuales.11 = -0.0515<br>RJ: regenerado (R 4.3.3) › puente_estacional.estacional.acf_residuales.11 = -0.0515 | verificado |
| `0.233` | dato | J: cap4_arima.json › puente_estacional.estacional.ljung_box_24_p = 0.233<br>RJ: regenerado (R 4.3.3) › puente_estacional.estacional.ljung_box_24_p = 0.233 | verificado |
| `143` | dato | CALC: n − d = 144 − 1 = 143<br>J: cap4_arima.json › puente_estacional.advertencia_aicc | verificado |
| `131` | dato | CALC: n − d − D·12 = 144 − 1 − 12 = 131<br>J: cap4_arima.json › puente_estacional.advertencia_aicc | verificado |
| `144` | dato | J: cap4_arima.json › puente_estacional.n = 144<br>RD: directo_cap4.json › datos.ap_n = 144 | verificado |
| `p < 10⁻⁶ en Ljung–Box(24) del ARIMA(0,1,5)` | dato | CALC: χ²(19) con Q = 222.398: p < 1e-6 (df = 24 − 5) | verificado |
| `el mejor no estacional es ARIMA(0,1,5) y el airline ARIMA(0,1,1)(0,1,1)[12]` | dato | J: cap4_arima.json › puente_estacional | verificado |

### Para seguir: tres ejercicios y las lecturas del capítulo {columnas=1:1}

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `2008` | documentación | DOC: documentación de R (doc.citation_forecast) contiene «(2008)» | verificado |
| `27` | documentación | DOC: documentación de R (doc.citation_forecast) contiene «v027» | verificado |
| `1978` | documentación | DOC: documentación de R (doc.nile) contiene «Cobb(1978)» | verificado |
| `65` | documentación | DOC: documentación de R (doc.nile) contiene «*65*, 243-51» | verificado |
| `243` | documentación | DOC: documentación de R (doc.nile) contiene «*65*, 243-51» | verificado |
| `251` (?Nile da páginas 243-51) | documentación | DOC: documentación de R (doc.nile) contiene «*65*, 243-51» | verificado |
| `4.1` | capítulo | C: capítulo 4 contiene «módulos 4.1 a 4.4» | verificado |
| `4.4` | capítulo | C: capítulo 4 contiene «módulos 4.1 a 4.4» | verificado |
| `11` | capítulo | C: capítulo 4 contiene «Simulacro del quiz» | verificado |
| `9.5` | sin verificar | — (sin fuente en esta sesión) | SIN VERIFICAR |
| `9.8` | sin verificar | — (sin fuente en esta sesión) | SIN VERIFICAR |
| `2017` | sin verificar | — (sin fuente en esta sesión) | SIN VERIFICAR |
| `2015` | sin verificar | — (sin fuente en esta sesión) | SIN VERIFICAR |

### Cada cifra remite a una fuente; lo que no se pudo contrastar queda marcado

| Cifra o afirmación | Tipo | Fuentes y valor | Estado |
|---|---|---|---|
| `1970` | sin verificar | — (sin fuente en esta sesión) | SIN VERIFICAR |
