#!/usr/bin/env python3
"""R2 del capítulo 4 · reaplica sobre HEAD las ediciones de la ronda de gráficas y simuladores.

Seis archivos: el capítulo 2 (armazón que heredan los capítulos 3 a 6) y las cinco fuentes del
capítulo 4 (`ensamblado/cap4/chapter.js` y las cuatro plantillas de módulo que llevan lienzos o
iconos). Parte del contenido de cada uno en el commit base (por defecto HEAD), aplica cada
sustitución —que debe aparecer exactamente una vez— y escribe el resultado. Es reejecutable:
siempre parte del commit, no del archivo de trabajo.

Uso (desde la raíz del repo):
    python3 diagnostico/cap4/comprobaciones/r2_edita.py              # escribe
    python3 diagnostico/cap4/comprobaciones/r2_edita.py --comprobar  # solo compara
    python3 diagnostico/cap4/comprobaciones/r2_edita.py --base b3e9042

Después, en este orden:
    python3 ensamblado/ensambla_cap3.py --escribir
    python3 ensamblado/ensambla_cap4.py
    python3 ensamblado/ensambla_cap5.py
    python3 ensamblado/ensambla_cap6.py
"""
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
C2 = "Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html"
JS = "ensamblado/cap4/chapter.js"
T13 = "ensamblado/cap4/templates_1_3.html"
T46 = "ensamblado/cap4/templates_4_6.html"
T79 = "ensamblado/cap4/templates_7_9.html"
T10 = "ensamblado/cap4/templates_10.html"

C = []  # (clave, archivo, antes, después)


def c(clave, archivo, antes, despues):
    C.append((clave, archivo, antes, despues))


# =====================================================================================
# ARMAZÓN · capítulo 2 (lo heredan los capítulos 3, 4, 5 y 6)
# =====================================================================================
c("armazón · crearGraficoLinea: comentario", C2,
  r'''    // `opciones` se mezcla con Object.assign, que es superficial: quien pasa
    // `scales` sustituye los dos ejes enteros (y con ellos las marcas
    // legibles y la línea del 0, que son de los ejes por defecto). `tituloX` y
    // `tituloY` rotulan los ejes sin tener que pasar `scales`.
    function crearGraficoLinea(canvas, etiquetas, datasets, opciones = {}) {
      const estrecho = !!canvas.parentNode && canvas.parentNode.clientWidth < 420;
      const propias = Object.assign({}, opciones);
      delete propias.tituloX;
      delete propias.tituloY;
      return new Chart(canvas, {
        type: 'line',
        data: { labels: etiquetas, datasets: datasets },
        options: Object.assign({''',
  r'''    // `opciones` se mezcla con Object.assign, que es superficial: quien pasa
    // `scales` sustituye los dos ejes enteros (y con ellos las marcas
    // legibles y la línea del 0, que son de los ejes por defecto). `tituloX` y
    // `tituloY` rotulan los ejes sin tener que pasar `scales`. Quien pasa
    // `plugins` sustituye también los de aquí (la leyenda y el tooltip), pero
    // no la muestra de la leyenda, que es del armazón: la dibuja
    // etiquetasDeLeyendaLinea() aunque el capítulo traiga su propio `legend`
    // (salvo que traiga también su propio `generateLabels`).
    function crearGraficoLinea(canvas, etiquetas, datasets, opciones = {}) {
      const estrecho = !!canvas.parentNode && canvas.parentNode.clientWidth < 420;
      const propias = Object.assign({}, opciones);
      delete propias.tituloX;
      delete propias.tituloY;
      const opts = Object.assign({''')

c("armazón · crearGraficoLinea: la muestra de la leyenda", C2,
  r'''              afterBuildTicks: marcasVerticales
            }
          }
        }, propias)
      });
    }

    // Generador congruencial mulberry32 + Box-Muller: ruido N(0,1)''',
  r'''              afterBuildTicks: marcasVerticales
            }
          }
        }, propias);
      // La muestra de cada entrada de la leyenda es del armazón: se mezcla con
      // lo que el capítulo haya pasado en `plugins.legend.labels` (fuente,
      // ancho de la muestra, filtro), que gana si repite alguna de estas claves.
      const plugins = opts.plugins || {};
      const leyenda = plugins.legend || {};
      opts.plugins = Object.assign({}, plugins, {
        legend: Object.assign({}, leyenda, {
          labels: Object.assign({
            usePointStyle: true, boxHeight: 8, generateLabels: etiquetasDeLeyendaLinea
          }, leyenda.labels)
        })
      });
      return new Chart(canvas, {
        type: 'line',
        data: { labels: etiquetas, datasets: datasets },
        options: opts,
        // La raya y la caja miden lo que diga `boxWidth` (también si un
        // capítulo lo cambia después de crear el gráfico: el 4 lo reduce en el
        // teléfono). Con un punto suelto en la leyenda (un círculo, una cruz)
        // la muestra mide lo de siempre: con un ancho fijo Chart.js lo
        // estira hasta hacer un óvalo.
        plugins: [{
          id: 'anchoDeLaMuestra',
          beforeUpdate: chart => {
            const rotulos = chart.options.plugins.legend.labels;
            const hayPuntos = chart.data.datasets.some(ds => ds.showLine === false && ds.label);
            rotulos.pointStyleWidth = hayPuntos ? undefined : rotulos.boxWidth;
          }
        }]
      });
    }

    // Generador congruencial mulberry32 + Box-Muller: ruido N(0,1)''')

c("armazón · etiquetasDeLeyendaLinea", C2,
  r'''    // Gráfico de barras para correlogramas. `opciones.lineas` dibuja rectas de
    // referencia horizontales (la banda ±1.96/√T, el nivel nominal de una''',
  r'''    // Leyenda de crearGraficoLinea: cada entrada se dibuja como lo que es.
    // Las series y las rectas de referencia, con un trozo de su trazo (con su
    // discontinuidad, si la tienen), y no con la caja gris de borde de color
    // que salía por defecto; las bandas (un `fill` hacia otra serie: '+1',
    // '-1', un índice), con una caja de su color y de su borde; los puntos
    // sueltos (`showLine: false`), con su marca (círculo, cruz…).
    function etiquetasDeLeyendaLinea(chart) {
      return Chart.defaults.plugins.legend.labels.generateLabels(chart).map(item => {
        const ds = chart.data.datasets[item.datasetIndex];
        if (!ds) return item;
        const cadena = v => typeof v === 'string';
        const banda = typeof ds.fill === 'number' || (cadena(ds.fill) && /^[+-]\d+$/.test(ds.fill)) ||
          (!!ds.fill && typeof ds.fill === 'object');
        if (banda) {
          item.pointStyle = 'rect';
          item.lineWidth = typeof ds.borderWidth === 'number' ? ds.borderWidth : 1;
        } else if (ds.showLine === false) {
          item.pointStyle = ds.pointStyle || 'circle';
          if (cadena(ds.backgroundColor)) item.fillStyle = ds.backgroundColor;
          if (cadena(ds.borderColor)) item.strokeStyle = ds.borderColor;
          item.lineWidth = typeof ds.pointBorderWidth === 'number' ? ds.pointBorderWidth : 1.5;
        } else {
          item.pointStyle = 'line';
          if (cadena(ds.borderColor)) item.strokeStyle = ds.borderColor;
          item.lineWidth = typeof ds.borderWidth === 'number'
            ? Math.min(3, Math.max(1.5, ds.borderWidth)) : 2;
          item.lineDash = ds.borderDash || [];
        }
        return item;
      });
    }

    // Gráfico de barras para correlogramas. `opciones.lineas` dibuja rectas de
    // referencia horizontales (la banda ±1.96/√T, el nivel nominal de una''')


# =====================================================================================
# Iconos de Font Awesome 6.0.0 (los de 6.1 en adelante salen vacíos)
# =====================================================================================
c("icono · M4: fa-magnifying-glass-chart (6.1) → fa-chart-column (6.0)", T46,
  r'''<h4><i class="fas fa-magnifying-glass-chart" aria-hidden="true"></i> ACF y PACF por orden de diferenciación</h4>''',
  r'''<h4><i class="fas fa-chart-column" aria-hidden="true"></i> ACF y PACF por orden de diferenciación</h4>''')

c("icono · M9: fa-arrows-left-right-to-line (6.1) → fa-arrows-left-right (6.0)", T79,
  r'''<h4><i class="fas fa-arrows-left-right-to-line" aria-hidden="true"></i> Los pesos $\psi$ y el ancho del''',
  r'''<h4><i class="fas fa-arrows-left-right" aria-hidden="true"></i> Los pesos $\psi$ y el ancho del''')


# =====================================================================================
# chapter.js · ayudantes comunes
# =====================================================================================
c("JS · escalasLinea reinstala los ayudantes del armazón (causa A)", JS,
  r'''    // Escalas completas de un gráfico de línea con título en el eje y.
    // crearGraficoLinea fusiona sus opciones con Object.assign, que es
    // superficial: quien pasa `scales` reemplaza x e y enteras, así que aquí
    // van las dos con la tipografía de siempre.
    function escalasLinea(tituloY, x = {}) {
      return {
        x: Object.assign({
          ticks: { font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 12, maxRotation: 0 },
          grid: { display: false }
        }, x),
        y: {
          title: { display: !!tituloY, text: tituloY, font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 11 } },
          grid: { color: 'rgba(148, 163, 184, 0.2)' }
        }
      };
    }''',
  r'''    // Escalas completas de un gráfico de línea con título en el eje y.
    // crearGraficoLinea fusiona sus opciones con Object.assign, que es
    // superficial: quien pasa `scales` reemplaza x e y enteras, y con ellas los
    // ayudantes del armazón. Aquí van los dos ejes con la tipografía de
    // siempre y los ayudantes puestos otra vez: el x con marcasLegibles() y
    // rotuloLegible() (años redondos que no se pisan; en las fechas AAAA-MM,
    // los eneros con su año) y el y con marcasVerticales() y rotuloVertical()
    // (signo menos tipográfico) y la línea del 0 más oscura donde hay valores
    // negativos. `x` se mezcla con el eje x, y sus `ticks`, clave a clave.
    function escalasLinea(tituloY, x = {}) {
      const ticksX = Object.assign({
        font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 12, maxRotation: 0,
        callback: rotuloLegible
      }, x.ticks);
      return {
        x: Object.assign({
          grid: { display: false },
          afterBuildTicks: eje => { marcasLegibles(eje, { maxMarcas: ticksX.maxTicksLimit }); }
        }, x, { ticks: ticksX }),
        y: {
          title: { display: !!tituloY, text: tituloY, font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 11 }, autoSkip: false, callback: rotuloVertical },
          grid: { color: rejillaConCero },
          afterBuildTicks: marcasVerticales
        }
      };
    }''')

c("JS · lineaCompacta: lo mismo para un gráfico de línea", JS,
  r'''    // Lo mismo para un gráfico de barras (M4, M6): crearGraficoBarras no
    // admite onResize, así que se le añade ya creado.
    function barrasCompactas(g, altos) {
      g.options.onResize = (gr, t) => compactar(gr, t.width, altos);
      compactar(g, g.width, altos);
      g.update('none');
      return g;
    }
''',
  r'''    // Lo mismo para un gráfico de barras (M4, M6, M10): crearGraficoBarras no
    // admite onResize, así que se le añade ya creado.
    function barrasCompactas(g, altos) {
      g.options.onResize = (gr, t) => compactar(gr, t.width, altos);
      compactar(g, g.width, altos);
      g.update('none');
      return g;
    }

    // Y para uno de línea (M7, M9, M10): con la leyenda a la medida del ancho
    // y el marco del alto que le toca, que no es el mismo en el escritorio que
    // en el teléfono.
    function lineaCompacta(g, altos) { return barrasCompactas(g, altos); }
''')

c("JS · ayudantes: aria, diferencias(), describirBarrasQuiz(), leyendaDeColores()", JS,
  r'''    // ∇, ∇², ∇³: el orden como exponente, igual que en la prosa.
    function nabla(d) { return ['', '∇', '∇²', '∇³'][d]; }
''',
  r'''    // ∇, ∇², ∇³: el orden como exponente, igual que en la prosa.
    function nabla(d) { return ['', '∇', '∇²', '∇³'][d]; }

    // «sin diferenciar», «con una diferencia», «con dos diferencias»…: el orden
    // con palabras, para los `aria-label`.
    function diferencias(d) {
      return ['sin diferenciar', 'con una diferencia', 'con dos diferencias', 'con tres diferencias'][d];
    }

    // Escribe el `aria-label` de un lienzo, con el signo menos tipográfico. Se
    // llama en cada pintar(): el lienzo dice lo que dibuja en ese momento, no lo
    // que dibujaba al abrir el módulo.
    function ariaLienzo(canvas, texto) {
      canvas.setAttribute('aria-label', conSignoMenos(texto));
    }

    // Descripción del gráfico de una pregunta del quiz: da los datos que se
    // ven —todas las barras, en orden, y la banda si la hay—, no lo que la
    // pregunta pide deducir de ellos.
    function describirBarrasQuiz(que, valores, b) {
      return `${que}. Valores de los rezagos 1 a ${valores.length}, en orden: ` +
        valores.map(v => cifra(v, 2)).join(', ') + '.' +
        (b ? ` Banda de referencia: ±${b.toFixed(3)}.` : '');
    }

    // Las marcas de marcasLegibles() y, siempre, la última categoría del eje (el
    // horizonte máximo): en σ_h, a 800 px el paso de 4 dejaba el eje en 28 y
    // sin el 30, que es el extremo del deslizador. Si la marca anterior queda
    // pegada a la última (menos de 24 px entre sus centros), se quita.
    function marcasConUltimo(eje, opciones) {
      marcasLegibles(eje, opciones);
      const ultimo = eje.getLabels().length - 1;
      if (eje.type !== 'category' || !eje.ticks.length || eje.ticks[eje.ticks.length - 1].value >= ultimo) return;
      const pxPorCategoria = eje.width / (ultimo - Math.ceil(eje.min) + 1);
      if ((ultimo - eje.ticks[eje.ticks.length - 1].value) * pxPorCategoria < 24) eje.ticks.pop();
      eje.ticks.push({ value: ultimo });
    }

    // Leyenda de un gráfico de barras con un color por barra. Chart.js dibuja
    // una sola muestra, la de la primera barra, y esa cambia con el estado del
    // simulador: no explica nada. Aquí la leyenda es el código de colores,
    // [{ texto, color }], y no depende de qué barra venga primero. Una entrada
    // no corresponde a un conjunto de datos, así que pulsarla no hace nada.
    function leyendaDeColores(grafico, entradas) {
      const leyenda = grafico.options.plugins.legend;
      leyenda.onClick = () => {};
      leyenda.labels.generateLabels = () => entradas.map(e => ({
        text: e.texto, fillStyle: e.color, strokeStyle: e.color, lineWidth: 0,
        pointStyle: 'rect', hidden: false, datasetIndex: 0
      }));
    }
''')


# =====================================================================================
# chapter.js · M1, M3 y M4
# =====================================================================================
c("JS · M1: aria-label con la serie que se ve", JS,
  r'''        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'media', valor: fmt(media(y)) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) },
          { etiqueta: 'ρ̂₁', valor: fmt(calcularACF(y, 1)[0], 4) }
        ]);''',
  r'''        const rho1 = calcularACF(y, 1)[0];
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'media', valor: fmt(media(y)) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) },
          { etiqueta: 'ρ̂₁', valor: fmt(rho1, 4) }
        ]);
        ariaLienzo(canvas, `Caudal del Nilo ${diferencias(d)}, de ${etiquetas[0]} a ` +
          `${etiquetas[etiquetas.length - 1]}: ${y.length} valores, media ${fmt(media(y))}, ` +
          `varianza ${fmt(varianzaDe(y))}, autocorrelación del rezago 1 ${fmt(rho1, 4)}`);''')

c("JS · M3: marcos de la tasa (D)", JS,
  r'''      const ALTOS_CURVA = { estrecho: '280px', ancho: '200px' };''',
  r'''      // En el escritorio el área de la tasa medía 94 px y la recta del 5 %
      // quedaba a 4.7 px del 0: ahora 150 o más, como en el teléfono.
      const ALTOS_CURVA = { estrecho: '280px', ancho: '260px' };''')

c("JS · M3: aria-label de la serie", JS,
  r'''        gSerie = lineaSimple(cSerie, etiquetas, y,
          b === 0 ? 'Sin escalón' : `Descenso de ${fmt(b, 0)} en 1899`,
          COLORES_GRAFICO.primario, {
            scales: escalasLinea('Nivel simulado'),
            onResize: (g, t) => compactar(g, t.width)
          });
        compactar(gSerie, gSerie.width);
        gSerie.update('none');
''',
  r'''        gSerie = lineaSimple(cSerie, etiquetas, y,
          b === 0 ? 'Sin escalón' : `Descenso de ${fmt(b, 0)} en 1899`,
          COLORES_GRAFICO.primario, {
            scales: escalasLinea('Nivel simulado'),
            onResize: (g, t) => compactar(g, t.width)
          });
        compactar(gSerie, gSerie.width);
        gSerie.update('none');
        ariaLienzo(cSerie, `Ruido blanco simulado, de ${etiquetas[0]} a ${etiquetas[etiquetas.length - 1]}, ` +
          (b === 0 ? 'sin escalón' : `con un descenso de ${fmt(b, 0)} desde 1899`) +
          `: ${y.length} valores, media ${fmt(media(y))}`);
''')

c("JS · M3: leyenda corta en el teléfono (C) y marcador sin recorte (E)", JS,
  r'''        if (!gCurva) {
          gCurva = crearGraficoLinea(cCurva, [], [
            {
              label: 'KPSS con ℓ = 4 (R)',''',
  r'''        if (!gCurva) {
          // En el teléfono las cinco entradas ocupaban tres renglones: sin el
          // «con» y con los rótulos de las dos rectas más cortos caben en dos.
          const corto = cCurva.parentNode.clientWidth < ESTRECHO;
          gCurva = crearGraficoLinea(cCurva, [], [
            {
              label: corto ? 'KPSS ℓ = 4 (R)' : 'KPSS con ℓ = 4 (R)',''')

c("JS · M3: rótulos cortos de las otras tres entradas", JS,
  r'''              label: 'KPSS con ℓ = 12',
              data: curva('kpss_rechaza_l12'),''',
  r'''              label: corto ? 'KPSS ℓ = 12' : 'KPSS con ℓ = 12',
              data: curva('kpss_rechaza_l12'),''')

c("JS · M3: nominal 5 % corto", JS,
  r'''              label: 'Nivel nominal 5 %',
              data: [{ x: 0, y: 5 }, { x: 300, y: 5 }],''',
  r'''              label: corto ? '5 % nominal' : 'Nivel nominal 5 %',
              data: [{ x: 0, y: 5 }, { x: 300, y: 5 }],''')

c("JS · M3: el marcador β no se recorta en el borde (E)", JS,
  r'''              borderColor: COLORES_GRAFICO.primario,
              backgroundColor: COLORES_GRAFICO.primario,
              pointRadius: 6, pointHoverRadius: 7, showLine: false
            },
            {
              label: `Nilo (${fmt(malla.delta_del_nilo, 1)})`,''',
  r'''              borderColor: COLORES_GRAFICO.primario,
              backgroundColor: COLORES_GRAFICO.primario,
              // clip: false: en β = 0 y en β ≥ 200 el marcador cae sobre el
              // borde del área (el 0 % del eje, el 100 %) y salía cortado.
              pointRadius: 6, pointHoverRadius: 7, showLine: false, clip: false
            },
            {
              label: corto ? `Nilo ${fmt(malla.delta_del_nilo, 1)}` : `Nilo (${fmt(malla.delta_del_nilo, 1)})`,''')

c("JS · M3: aria-label de la tasa", JS,
  r'''        gCurva.data.datasets[3].data = [{ x: b, y: 100 * tasa }];
        gCurva.update('none');
''',
  r'''        gCurva.data.datasets[3].data = [{ x: b, y: 100 * tasa }];
        gCurva.update('none');
        ariaLienzo(cCurva, `Tasa de rechazo de KPSS al 5 % frente al tamaño del descenso, de 0 a 300: ` +
          `con |β| = ${fmt(b, 0)} rechaza el ${fmt(100 * tasa, 1)} % de las réplicas con ℓ = 4 y el ` +
          `${fmt(100 * tasa12, 1)} % con ℓ = 12; el descenso del Nilo está en ${fmt(malla.delta_del_nilo, 1)}`);
''')

c("JS · M4: marcos de la ACF y la PACF (D)", JS,
  r'''      const ALTOS_BARRAS = { estrecho: '240px', ancho: '180px' };''',
  r'''      // En el escritorio la ACF y la PACF medían 75 px de dibujo y las barras de
      // 0.21 a 0.24 quedaban a 1–2 px de la banda: ahora, 145.
      const ALTOS_BARRAS = { estrecho: '240px', ancho: '250px' };''')

c("JS · M4: aria-label de la serie, la ACF y la PACF", JS,
  r'''        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'banda', valor: `±${fmt(info.banda, 4)}` },
          { etiqueta: 'ρ̂₁', valor: fmt(info.acf[0], 4) },
          { etiqueta: 'ACF fuera de banda', valor: fuera(info.acf) },
          { etiqueta: 'PACF fuera de banda', valor: fuera(info.pacf) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) }
        ]);''',
  r'''        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'banda', valor: `±${fmt(info.banda, 4)}` },
          { etiqueta: 'ρ̂₁', valor: fmt(info.acf[0], 4) },
          { etiqueta: 'ACF fuera de banda', valor: fuera(info.acf) },
          { etiqueta: 'PACF fuera de banda', valor: fuera(info.pacf) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) }
        ]);
        const cual = `la serie del Nilo ${diferencias(d)}`;
        ariaLienzo(cSerie, `Serie del Nilo ${diferencias(d)}: ${y.length} valores, de ${fmt(Math.min(...y), 0)} a ` +
          `${fmt(Math.max(...y), 0)}, media ${fmt(media(y))}`);
        ariaLienzo(cAcf, descripcionCorrelograma('ACF muestral', cual, info.acf, info.banda));
        ariaLienzo(cPacf, descripcionCorrelograma('PACF muestral', cual, info.pacf, info.banda));''')


# =====================================================================================
# chapter.js · M6
# =====================================================================================
c("JS · M6: marcos de la ACF de residuales y del ΔAICc (D)", JS,
  r'''      const ALTOS_RESIDUALES = { estrecho: '250px', ancho: '210px' };
      const ALTOS_AICC = { estrecho: '240px', ancho: '200px' };''',
  r'''      // En el escritorio la ACF de residuales medía 105 px de dibujo; el ΔAICc
      // gana además un renglón, porque los rótulos con «↑74» van en dos.
      const ALTOS_RESIDUALES = { estrecho: '250px', ancho: '240px' };
      const ALTOS_AICC = { estrecho: '240px', ancho: '250px' };''')

c("JS · M6: aria-label cuando el modelo no converge", JS,
  r'''          actualizarLectura(lectura, [{ etiqueta: 'Modelo', valor: `ARIMA(${params.p},${params.d},${params.q}) no converge` }]);
          return;''',
  r'''          actualizarLectura(lectura, [{ etiqueta: 'Modelo', valor: `ARIMA(${params.p},${params.d},${params.q}) no converge` }]);
          ariaLienzo(cAcf, `Sin gráfico de residuales: el ARIMA(${params.p},${params.d},${params.q}) no converge`);
          ariaLienzo(cAicc, `AICc de los ${hermanos.length} modelos con d = ${params.d} que sí convergen; ` +
            `el ARIMA(${params.p},${params.d},${params.q}) elegido no converge`);
          return;''')

c("JS · M6: aria-label de la ACF de residuales", JS,
  r'''          lineas: lineasBanda(nEf), tituloX: 'Rezago k'
        }), ALTOS_RESIDUALES);
''',
  r'''          lineas: lineasBanda(nEf), tituloX: 'Rezago k'
        }), ALTOS_RESIDUALES);
        ariaLienzo(cAcf, descripcionCorrelograma('ACF', `los residuales del ${m.etiqueta}`,
          m.acf_residuales, banda(nEf)));
''')

c("JS · M6: los nueve rótulos a cualquier ancho, la leyenda explica los colores y el aria-label (A, F)", JS,
  r'''        gAicc.data.datasets[0].minBarLength = 3;
        if (tumbado) gAicc.update('none');
        else tituloEjeY(gAicc, 'ΔAICc');
''',
  r'''        gAicc.data.datasets[0].minBarLength = 3;
        // A 1200 px Chart.js rotulaba una barra de cada dos (cinco de nueve):
        // faltaban modelos con nombre, el mejor de d = 2 entre ellos, y el «↑74»
        // de la barra recortada. Sin salto automático y, si el rótulo lleva la
        // flecha, en dos renglones (el modelo y debajo la flecha), que es lo que
        // cabe en 69 px de barra.
        if (!tumbado) {
          Object.assign(gAicc.options.scales.x.ticks, {
            autoSkip: false,
            callback: function (v) { return String(this.getLabelForValue(v)).split(' '); }
          });
        }
        // La muestra única de Chart.js era la de la primera barra (naranja si el
        // elegido es el (0,d,0), gris en los demás): la leyenda es ahora el código.
        leyendaDeColores(gAicc, [
          { texto: 'Elegido', color: COLORES_GRAFICO.secundario },
          { texto: 'Mejor de su d', color: COLORES_GRAFICO.primario },
          { texto: 'Los demás', color: COLORES_GRAFICO.gris }
        ]);
        const cortadas = deltas.filter(v => v > TOPE).length;
        ariaLienzo(cAicc, `ΔAICc de los ${hermanos.length} modelos con d = ${params.d} sobre el mejor de ese d, ` +
          `de ${fmt(Math.min(...deltas))} a ${fmt(Math.max(...deltas))}; el elegido, ${m.etiqueta}, está a ` +
          `+${fmt(m.aicc - mejor.valor_aicc)}` +
          (cortadas ? `; ${cortadas === 1 ? 'una barra se corta' : `${cortadas} barras se cortan`} en ${TOPE} ` +
            `y ${cortadas === 1 ? 'lleva' : 'llevan'} su valor en el rótulo` : ''));
        if (tumbado) gAicc.update('none');
        else tituloEjeY(gAicc, 'ΔAICc');
''')


# =====================================================================================
# chapter.js · M7
# =====================================================================================
c("JS · M7: cotas del eje y fila del ∞ (E)", JS,
  r'''      // Los AICc infinitos (modelos descartados por raíces junto al círculo
      // unitario) llegan como null y no se dibujan; se marcan aparte, con una
      // cruz en el borde superior del gráfico.
      const TECHO = 1302;
      function serieAicc(pasos) {
        return pasos.map(p => (p.infinito ? null : p.aicc));
      }
''',
  r'''      // Los AICc infinitos (modelos descartados por raíces junto al círculo
      // unitario) llegan como null y no se dibujan; se marcan aparte, con una
      // cruz en una fila propia encima de los AICc finitos, que el eje rotula
      // «∞». Antes la cruz iba en el máximo del eje (1302) y el recorte del
      // área se comía su mitad de arriba. Las cotas salen de los AICc finitos
      // de las dos búsquedas, para que el eje no cambie al cambiar de modo.
      const FINITOS = HK.escalonada.pasos.concat(HK.exhaustiva.pasos)
        .filter(p => !p.infinito).map(p => p.aicc);
      const SUELO = Math.floor(Math.min(...FINITOS) / 5) * 5;
      const CIMA = Math.ceil(Math.max(...FINITOS) / 5) * 5;
      const TECHO = CIMA + 5;
      // El AICc, de 5 en 5 si caben (15 px por marca), si no de 10 en 10; y
      // el ∞ en la fila de arriba. Chart.js saltaba de 1295 a 1302.
      function marcasTraza(eje) {
        const alto = eje.height || eje.maxHeight;
        const paso = alto / 15 >= (CIMA - SUELO) / 5 + 2 ? 5 : 10;
        const marcas = [];
        for (let v = Math.ceil(SUELO / paso) * paso; v <= CIMA; v += paso) marcas.push(v);
        marcas.push(TECHO);
        eje.ticks = marcas.map(v => ({ value: v }));
      }
      const ALTOS_TRAZA = { estrecho: '290px', ancho: '260px' };
''')

c("JS · M7: puntos y cruces, leyenda y ejes (A, D, E, F)", JS,
  r'''        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas,
          pasos.map((_, i) => String(i + 1)), [
            {
              label: 'AICc del modelo evaluado',
              data: serieAicc(pasos).map((v, i) => (i < hasta ? v : null)),
              borderColor: 'rgba(1, 40, 32, 0.25)',
              backgroundColor: pasos.map((p, i) =>
                i < hasta && p.mejora ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.primario),
              borderWidth: 1, pointRadius: pasos.map((p, i) =>
                i < hasta ? (p.mejora ? 6 : 3) : 0), showLine: false
            },
            {
              label: 'Mejor AICc hasta ese paso',
              data: pasos.map((p, i) => (i < hasta ? p.mejor_hasta_aqui : null)),
              borderColor: '#15803d', borderWidth: 2, pointRadius: 0,
              stepped: true, fill: false
            },
            {
              label: 'AICc = ∞ (descartado)',
              data: pasos.map((p, i) => (i < hasta && p.infinito ? TECHO : null)),
              borderColor: '#b91c1c', backgroundColor: '#b91c1c',
              pointStyle: 'crossRot', pointRadius: 7, pointBorderWidth: 2, showLine: false
            }
          ], {
            scales: {
              x: { title: { display: true, text: 'Orden de evaluación' },
                   ticks: { font: { family: 'Fira Code', size: 10 } }, grid: { display: false } },
              y: { suggestedMin: 1265, max: TECHO,
                   title: { display: true, text: 'AICc', font: { family: 'Montserrat', size: 11 } },
                   ticks: { font: { family: 'Fira Code', size: 11 } } }
            }
          });
''',
  r'''        if (grafico) grafico.destroy();
        // El color del punto es el código, y cada color tiene su entrada en la
        // leyenda: antes era un solo conjunto de datos con un color por punto y la
        // muestra tomaba el del primero (naranja en la exhaustiva, verde en la
        // escalonada). En el teléfono, rótulos más cortos: caben en dos renglones.
        const corto = canvas.parentNode.clientWidth < ESTRECHO;
        const escalas = escalasLinea('AICc', {
          offset: true,
          title: { display: true, text: 'Orden de evaluación', font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 10 } }
        });
        Object.assign(escalas.y, {
          min: SUELO, max: TECHO, afterBuildTicks: marcasTraza,
          ticks: {
            font: { family: 'Fira Code', size: 11 }, autoSkip: false,
            callback: function (v, i, marcas) { return v === TECHO ? '∞' : rotuloVertical.call(this, v, i, marcas); }
          }
        });
        grafico = crearGraficoLinea(canvas,
          pasos.map((_, i) => String(i + 1)), [
            {
              label: corto ? 'Evaluado' : 'Modelo evaluado',
              data: pasos.map((p, i) => (i < hasta && !p.infinito && !p.mejora ? p.aicc : null)),
              borderColor: 'rgba(1, 40, 32, 0.25)', backgroundColor: COLORES_GRAFICO.primario,
              borderWidth: 1, pointRadius: 3, showLine: false, clip: false
            },
            {
              label: corto ? 'Mejora' : 'Mejora del mejor AICc',
              data: pasos.map((p, i) => (i < hasta && p.mejora ? p.aicc : null)),
              borderColor: 'rgba(1, 40, 32, 0.25)', backgroundColor: COLORES_GRAFICO.secundario,
              borderWidth: 1, pointRadius: 6, showLine: false, clip: false
            },
            {
              label: corto ? 'Mejor hasta aquí' : 'Mejor AICc hasta aquí',
              data: pasos.map((p, i) => (i < hasta ? p.mejor_hasta_aqui : null)),
              borderColor: '#15803d', borderWidth: 2, pointRadius: 0,
              stepped: true, fill: false
            },
            {
              label: corto ? '∞ (descartado)' : 'AICc = ∞ (descartado)',
              data: pasos.map((p, i) => (i < hasta && p.infinito ? TECHO : null)),
              borderColor: '#b91c1c', backgroundColor: '#b91c1c',
              pointStyle: 'crossRot', pointRadius: 7, pointBorderWidth: 2, showLine: false,
              clip: false
            }
          ], { scales: escalas });
        lineaCompacta(grafico, ALTOS_TRAZA);
''')

c("JS · M7: aria-label", JS,
  r'''          { etiqueta: 'Mejoras acumuladas', valor: mejorados }
        ]);
''',
  r'''          { etiqueta: 'Mejoras acumuladas', valor: mejorados }
        ]);
        ariaLienzo(canvas, `AICc de los modelos que evalúa la búsqueda ` +
          `${params.exhaustiva ? 'exhaustiva' : 'escalonada'}, hasta el paso ${hasta} de ${pasos.length}. ` +
          `Mejoras del mejor AICc: ${mejorados}. Descartados con AICc infinito: ` +
          `${visibles.filter(p => p.infinito).length}. Mejor AICc hasta aquí: ` +
          (actual.mejor_hasta_aqui === null ? 'ninguno todavía' : fmt(actual.mejor_hasta_aqui, 3)));
''')


# =====================================================================================
# chapter.js · M8
# =====================================================================================
c("JS · M8: aria-label de la serie", JS,
  r'''          d <= 1 ? COLORES_GRAFICO.primario : '#b91c1c',
          { scales: escalasLinea(d === 0 ? UNIDAD_NILO : `Diferencia (${UNIDAD_NILO})`) });
''',
  r'''          d <= 1 ? COLORES_GRAFICO.primario : '#b91c1c',
          { scales: escalasLinea(d === 0 ? UNIDAD_NILO : `Diferencia (${UNIDAD_NILO})`) });
        ariaLienzo(cSerie, `Serie del Nilo ${diferencias(d)}: ${y.length} valores, de ` +
          `${fmt(Math.min(...y), 0)} a ${fmt(Math.max(...y), 0)}, varianza ${fmt(fila.varianza)}`);
''')

c("JS · M8: eje logarítmico con rótulos donde caen las barras, leyenda de colores y aria-label (A, F)", JS,
  r'''        gVar.options.scales.y = {
          type: 'logarithmic', min: 10000, max: 400000,
          title: { display: true, text: 'Varianza (log)',
                   font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 11 },
                   callback: v => [10000, 20000, 50000, 100000, 200000].includes(v) ? fmt(v, 0) : '' },
          grid: { color: 'rgba(148, 163, 184, 0.2)' }
        };
        gVar.update('none');
''',
  r'''        // Las marcas, en 1 y 3 por potencia de diez (10 000, 30 000, 100 000,
        // 300 000): las barras de d = 0 y d = 1 (≈ 28 000) caen casi sobre el
        // 30 000. El callback pedía también 20 000 y 50 000, pero Chart.js no
        // generaba esas marcas y las barras quedaban entre rejillas sin número.
        gVar.options.scales.y = {
          type: 'logarithmic', min: 10000, max: 400000,
          title: { display: true, text: 'Varianza (log)',
                   font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 11 }, autoSkip: false, callback: v => fmt(v, 0) },
          grid: { color: 'rgba(148, 163, 184, 0.2)' },
          afterBuildTicks: eje => {
            const marcas = [];
            for (let e = Math.floor(Math.log10(eje.min)); e <= Math.ceil(Math.log10(eje.max)); e++) {
              [1, 3].forEach(m => {
                const v = m * Math.pow(10, e);
                if (v >= eje.min && v <= eje.max) marcas.push(v);
              });
            }
            eje.ticks = marcas.map(v => ({ value: v }));
          }
        };
        leyendaDeColores(gVar, [
          { texto: 'Orden elegido', color: COLORES_GRAFICO.secundario },
          { texto: 'Los demás', color: COLORES_GRAFICO.gris }
        ]);
        gVar.update('none');
        ariaLienzo(cVar, 'Varianza de la serie del Nilo según el número de diferencias, en escala logarítmica: ' +
          tabla.map(f => `d = ${f.d}, ${fmt(f.varianza, 0)}`).join('; ') + `. Elegido: d = ${d}`);
''')


# =====================================================================================
# chapter.js · M9
# =====================================================================================
c("JS · M9 forma: marcos y leyenda a la medida del ancho (C, D)", JS,
  r'''      const etiquetas = aniosDesde(inicio, serie.length + H, 0);
      const nulos = serie.map(() => null);
''',
  r'''      const etiquetas = aniosDesde(inicio, serie.length + H, 0);
      const nulos = serie.map(() => null);
      // En el teléfono la leyenda ocupaba cuatro renglones (98 px) de un lienzo de
      // 257: con la tipografía compacta y un rótulo más corto caben en dos.
      const ALTOS_FORMA = { estrecho: '300px', ancho: '280px' };
''')

c("JS · M9 forma: rótulo corto de la serie observada", JS,
  r'''        const datasets = [{
          label: 'Caudal observado',
          data: serie.concat(Array(H).fill(null)),''',
  r'''        const corto = canvas.parentNode.clientWidth < ESTRECHO;
        const datasets = [{
          label: corto ? 'Observado' : 'Caudal observado',
          data: serie.concat(Array(H).fill(null)),''')

c("JS · M9 forma: ejes del armazón y compactar (A, C)", JS,
  r'''          scales: escalasLinea(`Caudal (${UNIDAD_NILO})`,
            { ticks: { font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 10, maxRotation: 0 } })
        });

        const medida = NILO.intervalos.forma_medida[params.modelo];
        actualizarLectura(lectura, [
          { etiqueta: 'Modelo', valor: f.etiqueta },
          { etiqueta: 'ŷ a 1 año', valor: fmt(f.media[0]) },
          { etiqueta: `ŷ a ${H} años`, valor: fmt(f.media[H - 1]) },
          { etiqueta: 'pendiente final', valor: fmt(medida.primera_dif_h30, 3) },
          { etiqueta: 'curvatura final', valor: fmt(medida.segunda_dif_h30, 4) },
          { etiqueta: 'ancho 95 % (h=1)', valor: fmt(medida.ancho95_h1) },
          { etiqueta: `ancho 95 % (h=${H})`, valor: fmt(medida.ancho95_h30) }
        ]);''',
  r'''          scales: escalasLinea(`Caudal (${UNIDAD_NILO})`)
        });
        lineaCompacta(grafico, ALTOS_FORMA);

        const medida = NILO.intervalos.forma_medida[params.modelo];
        const campos = [
          { etiqueta: 'Modelo', valor: f.etiqueta },
          { etiqueta: 'ŷ a 1 año', valor: fmt(f.media[0]) },
          { etiqueta: `ŷ a ${H} años`, valor: fmt(f.media[H - 1]) },
          { etiqueta: 'pendiente final', valor: fmt(medida.primera_dif_h30, 3) },
          { etiqueta: 'curvatura final', valor: fmt(medida.segunda_dif_h30, 4) },
          { etiqueta: 'ancho 95 % (h=1)', valor: fmt(medida.ancho95_h1) },
          { etiqueta: `ancho 95 % (h=${H})`, valor: fmt(medida.ancho95_h30) }
        ];
        // Con d = 2 la banda baja de 0: el intervalo no sabe que un caudal no
        // puede ser negativo, y el dibujo (que se estira hasta ahí) lo muestra.
        const piso = Math.min(...f.lo95);
        if (params.bandas && piso < 0) {
          campos.push({ etiqueta: `límite inferior 95 % (h=${H})`,
            valor: `${fmt(f.lo95[H - 1])} — por debajo de 0, y un caudal no puede ser negativo` });
        }
        actualizarLectura(lectura, campos);
        ariaLienzo(canvas, `Serie del Nilo hasta ${inicio + serie.length - 1} y pronóstico a ${H} años con el ` +
          `${f.etiqueta}: de ${fmt(f.media[0])} el primer año a ${fmt(f.media[H - 1])} el último` +
          (params.bandas ? `; el intervalo del 95 % va de ${fmt(f.lo95[H - 1])} a ${fmt(f.hi95[H - 1])} en el último año` : ''));''')

c("JS · M9 ψ y σ: marcos (D)", JS,
  r'''      const etiquetasH = Array.from({ length: H }, (_, i) => String(i + 1));
      const raizH = Array.from({ length: H }, (_, i) => inter.sigma * Math.sqrt(i + 1));
''',
  r'''      const etiquetasH = Array.from({ length: H }, (_, i) => String(i + 1));
      const raizH = Array.from({ length: H }, (_, i) => inter.sigma * Math.sqrt(i + 1));
      // El gráfico de σ_h medía 74 px de dibujo a 1200 px y 52 a 800: la curva
      // que hay que comparar con la discontinua ocupaba una franja de 20 px.
      const ALTOS_PSI = { estrecho: '240px', ancho: '240px' };
      const ALTOS_SIGMA = { estrecho: '260px', ancho: '240px' };
''')

c("JS · M9 ψ: eje hasta el máximo de los datos y leyenda de colores (F)", JS,
  r'''        gPsi = crearGraficoBarras(cPsi,
          inter.psi.map((_, i) => String(i)), inter.psi, {
            etiqueta: 'Peso ψⱼ', color: COLORES_GRAFICO.primario,
            tituloX: 'j', min: 0, max: 1.05
          });
        gPsi.data.datasets[0].backgroundColor = inter.psi.map(
          (_, i) => i < h ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        gPsi.update('none');
''',
  r'''        gPsi = barrasCompactas(crearGraficoBarras(cPsi,
          inter.psi.map((_, i) => String(i)), inter.psi, {
            etiqueta: 'Peso ψⱼ', color: COLORES_GRAFICO.primario,
            tituloX: 'j', min: 0, max: 1.05
          }), ALTOS_PSI);
        gPsi.data.datasets[0].backgroundColor = inter.psi.map(
          (_, i) => i < h ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        // `min` y `max` de crearGraficoBarras solo sugieren: con datos ≤ 1 el eje
        // llegaba a 1.5 y un tercio del área quedaba vacío. Aquí el máximo es el
        // de los datos.
        Object.assign(gPsi.options.scales.y, { min: 0, max: Math.max(...inter.psi) });
        leyendaDeColores(gPsi, [
          { texto: 'Entran en σₕ (j < h)', color: COLORES_GRAFICO.secundario },
          { texto: 'No entran', color: COLORES_GRAFICO.gris }
        ]);
        gPsi.update('none');
        ariaLienzo(cPsi, `Pesos ψⱼ del ARIMA(1,1,1) del Nilo, de j = 0 a ${inter.psi.length - 1}: ψ₀ = ` +
          `${fmt(inter.psi[0], 3)}, ψ₁ = ${fmt(inter.psi[1], 3)}, ψ${inter.psi.length - 1} = ` +
          `${fmt(inter.psi[inter.psi.length - 1], 3)}; los ${h} primeros, en naranja, entran en σₕ`);
''')

c("JS · M9 σ: escalas del armazón, marcadores sin recorte y marco (A, D, E)", JS,
  r'''              label: '', data: [], showLine: false, pointRadius: 5,
              borderColor: COLORES_GRAFICO.secundario, backgroundColor: COLORES_GRAFICO.secundario
            },
            {
              label: '', data: [], showLine: false, pointRadius: 5,
              borderColor: COLORES_GRAFICO.terciario, backgroundColor: COLORES_GRAFICO.terciario
            }
          ], {''',
  r'''              // clip: false: en h = 1 y h = 30 el marcador cae sobre el borde del
              // área y salía cortado.
              label: '', data: [], showLine: false, pointRadius: 5, clip: false,
              borderColor: COLORES_GRAFICO.secundario, backgroundColor: COLORES_GRAFICO.secundario
            },
            {
              label: '', data: [], showLine: false, pointRadius: 5, clip: false,
              borderColor: COLORES_GRAFICO.terciario, backgroundColor: COLORES_GRAFICO.terciario
            }
          ], {''')

c("JS · M9 σ: x con marcasLegibles (que llegue el 30) e y desde 0", JS,
  r'''            scales: {
              x: { title: { display: true, text: 'Horizonte h' },
                   ticks: { font: { family: 'Fira Code', size: 10 }, maxTicksLimit: 10 },
                   grid: { display: false } },
              y: { min: 0,
                   title: { display: true, text: `σ (${UNIDAD_NILO})`,
                            font: { family: 'Montserrat', size: 11 } },
                   ticks: { font: { family: 'Fira Code', size: 11 } } }
            }
          });
        }''',
  r'''            scales: escalasLinea(`σ (${UNIDAD_NILO})`, {
              offset: true,
              afterBuildTicks: eje => { marcasConUltimo(eje, { maxMarcas: 12 }); },
              title: { display: true, text: 'Horizonte h', font: { family: 'Montserrat', size: 11 } },
              ticks: { font: { family: 'Fira Code', size: 10 } }
            }),
            onResize: (g, t) => compactar(g, t.width, ALTOS_SIGMA)
          });
          gSigma.options.scales.y.min = 0;
          compactar(gSigma, gSigma.width, ALTOS_SIGMA);
        }''')

c("JS · M9 σ: aria-label", JS,
  r'''        gSigma.data.datasets[3].data = raizH.map((v, i) => (i === h - 1 ? v : null));
        gSigma.update('none');
''',
  r'''        gSigma.data.datasets[3].data = raizH.map((v, i) => (i === h - 1 ? v : null));
        gSigma.update('none');
        ariaLienzo(cSigma, `Desviación del error de pronóstico σₕ frente al horizonte, de h = 1 a ${H}, y ` +
          `la de una caminata aleatoria con la misma σ: con h = ${h}, σₕ = ${fmt(inter.sigma_h[h - 1], 3)} ` +
          `y σ√h = ${fmt(inter.sigma * Math.sqrt(h), 3)}`);
''')


# =====================================================================================
# chapter.js · M10
# =====================================================================================
c("JS · M10 TRM: marcos y aria-label de la serie y de la ACF (A, B, D)", JS,
  r'''        [gSerie, gAcf].forEach(g => { if (g) g.destroy(); });
        gSerie = lineaSimple(cSerie, mesesDesde(inicio[0], inicio[1] + d, y.length), y,
          d === 0 ? 'TRM mensual (COP/USD)' : '∇TRM',
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario,
          { scales: escalasLinea(d === 0 ? 'COP por USD' : 'Cambio mensual (COP por USD)') });
        gAcf = crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        });
''',
  r'''        [gSerie, gAcf].forEach(g => { if (g) g.destroy(); });
        const meses = mesesDesde(inicio[0], inicio[1] + d, y.length);
        gSerie = lineaSimple(cSerie, meses, y,
          d === 0 ? 'TRM mensual (COP/USD)' : '∇TRM',
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario,
          { scales: escalasLinea(d === 0 ? 'COP por USD' : 'Cambio mensual (COP por USD)') });
        gAcf = barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_ACF);
        const cual = d === 0 ? 'la TRM en niveles' : 'la TRM diferenciada una vez';
        ariaLienzo(cSerie, `Serie de ${cual}, de ${meses[0]} a ${meses[meses.length - 1]}: ${y.length} meses, ` +
          `de ${fmt(Math.min(...y))} a ${fmt(Math.max(...y))} pesos por dólar`);
        ariaLienzo(cAcf, descripcionCorrelograma('ACF muestral', cual, info.acf, info.banda));
''')

c("JS · M10 TRM: marco de la ACF (D)", JS,
  r'''      const inicio = SERIES_CAP4.trm.inicio;

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = d === 0 ? TRM.identificacion.cruda : TRM.identificacion.d1;''',
  r'''      const inicio = SERIES_CAP4.trm.inicio;
      // La ACF medía 75 px de dibujo a 1200 px: el «por poco» del ρ̂₈ frente a la
      // banda eran ~1 px.
      const ALTOS_ACF = { estrecho: '240px', ancho: '250px' };

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = d === 0 ? TRM.identificacion.cruda : TRM.identificacion.d1;''')

c("JS · M10 abanico: ejes del armazón, leyenda compacta y aria-label (A, C, D)", JS,
  r'''          scales: escalasLinea('COP por USD',
            { ticks: { font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 10, maxRotation: 0 } })
        });

        const semi = Z95 * sigma * Math.sqrt(H);''',
  r'''          scales: escalasLinea('COP por USD')
        });
        lineaCompacta(grafico, ALTOS_ABANICO);

        const semi = Z95 * sigma * Math.sqrt(H);''')

c("JS · M10 abanico: aria-label", JS,
  r'''          { etiqueta: 'Frente al horizonte a un mes', valor: `×${fmt(Math.sqrt(H), 2)} — y sin techo` }
        ]);''',
  r'''          { etiqueta: 'Frente al horizonte a un mes', valor: `×${fmt(Math.sqrt(H), 2)} — y sin techo` }
        ]);
        ariaLienzo(canvas, `Últimos ${VISIBLES} meses de la TRM y pronóstico de caminata aleatoria a ${H} meses: ` +
          `recta horizontal en ${fmt(ultimo)} con un intervalo del 95 % de ${fmt(ultimo - semi)} a ` +
          `${fmt(ultimo + semi)} que se abre como la raíz del horizonte`);''')

c("JS · M10 abanico: marcos (D)", JS,
  r'''      const historia = serie.slice(-VISIBLES);
      // El primer mes visible, para que las etiquetas cuadren con el recorte.''',
  r'''      // En el teléfono la leyenda ocupaba cuatro renglones (98 px) y quedaban 112
      // px de dibujo: con la tipografía compacta caben en dos.
      const ALTOS_ABANICO = { estrecho: '300px', ancho: '280px' };

      const historia = serie.slice(-VISIBLES);
      // El primer mes visible, para que las etiquetas cuadren con el recorte.''')

c("JS · M10 puente: rótulo corto en el teléfono, marco y aria-label (C, D, B)", JS,
  r'''        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetas, acf, {
          etiqueta: esNo ? `ACF residual · ${PUENTE.no_estacional.resultado}`
                         : `ACF residual · ${PUENTE.estacional.etiqueta}`,
          color: esNo ? '#b91c1c' : COLORES_GRAFICO.primario,
          lineas: lineasBanda(PUENTE.n), tituloX: 'Rezago k'
        });
''',
  r'''        if (grafico) grafico.destroy();
        // El modelo ya está en el selector y en la lectura: en el teléfono el
        // rótulo largo pasaba la leyenda a dos renglones.
        const corto = canvas.parentNode.clientWidth < ESTRECHO;
        const modelo = esNo ? PUENTE.no_estacional.resultado : PUENTE.estacional.etiqueta;
        grafico = barrasCompactas(crearGraficoBarras(canvas, etiquetas, acf, {
          etiqueta: corto ? 'ACF residual' : `ACF residual · ${modelo}`,
          color: esNo ? '#b91c1c' : COLORES_GRAFICO.primario,
          lineas: lineasBanda(PUENTE.n), tituloX: 'Rezago k'
        }), ALTOS_PUENTE);
        ariaLienzo(canvas, descripcionCorrelograma('ACF', `los residuales del modelo ${modelo} sobre ` +
          'log(AirPassengers)', acf, PUENTE.no_estacional.banda));
''')

c("JS · M10 puente: marco", JS,
  r'''      const etiquetas = etiquetasRezago(PUENTE.no_estacional.acf_residuales.length);
''',
  r'''      const etiquetas = etiquetasRezago(PUENTE.no_estacional.acf_residuales.length);
      const ALTOS_PUENTE = { estrecho: '240px', ancho: '240px' };
''')


# =====================================================================================
# chapter.js · quiz del M10
# =====================================================================================
c("JS · quiz: la descripción de la ACF del correlograma mensual", JS,
  r'''        alto: 200,
        descripcionGrafico: 'Correlograma de residuales con barras muy altas en los rezagos 12 y 24, y pequeñas en el resto',''',
  r'''        alto: 250,
        descripcionGrafico: describirBarrasQuiz(
          'Función de autocorrelación de los residuales de un ARIMA ajustado a una serie mensual',
          PUENTE.no_estacional.acf_residuales, PUENTE.no_estacional.banda),''')

c("JS · quiz: la descripción de la ACF del Nilo sin diferenciar", JS,
  r'''        alto: 200,
        descripcionGrafico: 'Correlograma cuyas barras decaen despacio desde 0.50 sin llegar a cortarse en veinte rezagos',''',
  r'''        alto: 250,
        descripcionGrafico: describirBarrasQuiz('Función de autocorrelación muestral de una serie sin diferenciar',
          NILO.identificacion.cruda.acf, NILO.identificacion.cruda.banda),''')


# =====================================================================================
# plantillas · alto inicial de los marcos (el JS lo reajusta con compactar en los que lo usan)
# =====================================================================================
c("T13 · M3: marco de la tasa", T13,
  r'''        <div class="grafico-wrapper" style="height:200px;">
          <canvas aria-label="Tasa de rechazo de KPSS frente al tamaño del escalón" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:260px;">
          <canvas aria-label="Tasa de rechazo de KPSS frente al tamaño del escalón" role="img"></canvas>''')

c("T13 · M3: marco de la serie (en el escritorio medía 115 px de dibujo)", T13,
  r'''        <div class="grafico-wrapper" style="height:200px;">
          <canvas aria-label="Serie simulada de ruido blanco con un escalón" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:230px;">
          <canvas aria-label="Serie simulada de ruido blanco con un escalón" role="img"></canvas>''')

c("T46 · M4: marco de la serie", T46,
  r'''        <div class="grafico-wrapper" style="height:170px;">
          <canvas aria-label="Serie del Nilo en el orden de diferenciación seleccionado" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:230px;">
          <canvas aria-label="Serie del Nilo en el orden de diferenciación seleccionado" role="img"></canvas>''')

c("T46 · M4: marco de la ACF", T46,
  r'''        <div class="grafico-wrapper" style="height:180px;">
          <canvas aria-label="Función de autocorrelación de la serie seleccionada" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:250px;">
          <canvas aria-label="Función de autocorrelación de la serie seleccionada" role="img"></canvas>''')

c("T46 · M4: marco de la PACF", T46,
  r'''        <div class="grafico-wrapper" style="height:180px;">
          <canvas aria-label="Función de autocorrelación parcial de la serie seleccionada" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:250px;">
          <canvas aria-label="Función de autocorrelación parcial de la serie seleccionada" role="img"></canvas>''')

c("T46 · M6: marco de la ACF de residuales", T46,
  r'''        <div class="grafico-wrapper" style="height:210px;">
          <canvas aria-label="Autocorrelación de los residuales del modelo seleccionado" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:240px;">
          <canvas aria-label="Autocorrelación de los residuales del modelo seleccionado" role="img"></canvas>''')

c("T46 · M6: marco del ΔAICc", T46,
  r'''        <div class="grafico-wrapper" style="height:200px;">
          <canvas aria-label="AICc de los nueve modelos con el mismo orden de diferenciación" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:250px;">
          <canvas aria-label="ΔAICc de los nueve modelos con el mismo orden de diferenciación" role="img"></canvas>''')

c("T79 · M7: marco de la traza", T79,
  r'''        <div class="grafico-wrapper" style="height:230px;">
          <canvas aria-label="AICc de cada modelo evaluado por la búsqueda, en orden" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:260px;">
          <canvas aria-label="AICc de cada modelo evaluado por la búsqueda, en orden" role="img"></canvas>''')

c("T79 · M8: marco de la serie", T79,
  r'''        <div class="grafico-wrapper" style="height:190px;">
          <canvas aria-label="Serie del Nilo diferenciada d veces" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:220px;">
          <canvas aria-label="Serie del Nilo diferenciada d veces" role="img"></canvas>''')

c("T79 · M8: marco de la varianza", T79,
  r'''        <div class="grafico-wrapper" style="height:190px;">
          <canvas aria-label="Varianza de la serie según el orden de diferenciación" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:220px;">
          <canvas aria-label="Varianza de la serie según el orden de diferenciación" role="img"></canvas>''')

c("T79 · M9: marco de los ψ", T79,
  r'''        <div class="grafico-wrapper" style="height:180px;">
          <canvas aria-label="Pesos psi de la representación MA infinita" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:240px;">
          <canvas aria-label="Pesos psi de la representación MA infinita" role="img"></canvas>''')

c("T79 · M9: marco de σ_h", T79,
  r'''        <div class="grafico-wrapper" style="height:180px;">
          <canvas aria-label="Desviación del error de pronóstico frente al horizonte" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:240px;">
          <canvas aria-label="Desviación del error de pronóstico frente al horizonte" role="img"></canvas>''')

c("T10 · M10: marco de la serie de la TRM", T10,
  r'''        <div class="grafico-wrapper" style="height:190px;">
          <canvas aria-label="TRM mensual en el nivel de diferenciación seleccionado" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:230px;">
          <canvas aria-label="TRM mensual en el nivel de diferenciación seleccionado" role="img"></canvas>''')

c("T10 · M10: marco de la ACF de la TRM", T10,
  r'''        <div class="grafico-wrapper" style="height:180px;">
          <canvas aria-label="Autocorrelación de la TRM en el nivel seleccionado" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:250px;">
          <canvas aria-label="Autocorrelación de la TRM en el nivel seleccionado" role="img"></canvas>''')

c("T10 · M10: marco del abanico", T10,
  r'''        <div class="grafico-wrapper" style="height:260px;">
          <canvas aria-label="TRM observada y pronóstico de caminata aleatoria con sus intervalos" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:280px;">
          <canvas aria-label="TRM observada y pronóstico de caminata aleatoria con sus intervalos" role="img"></canvas>''')

c("T10 · M10: marco del puente", T10,
  r'''        <div class="grafico-wrapper" style="height:220px;">
          <canvas aria-label="ACF de los residuales del modelo seleccionado sobre log(AirPassengers)" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:240px;">
          <canvas aria-label="ACF de los residuales del modelo seleccionado sobre log(AirPassengers)" role="img"></canvas>''')


# =====================================================================================
def base(archivo, rev):
    return subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def main():
    rev = "HEAD"
    if "--base" in sys.argv:
        rev = sys.argv[sys.argv.index("--base") + 1]
    comprobar = "--comprobar" in sys.argv
    archivos = (C2, JS, T13, T46, T79, T10)
    textos = {a: base(a, rev) for a in archivos}
    fallos = 0
    for clave, archivo, antes, despues in C:
        n = textos[archivo].count(antes)
        if n != 1:
            print(f"FALLA · {clave}: el texto original aparece {n} veces en {archivo} (se esperaba 1)")
            fallos += 1
            continue
        textos[archivo] = textos[archivo].replace(antes, despues)
    if fallos:
        sys.exit(f"{fallos} sustituciones no aplicadas; no se escribe nada")
    for archivo, texto in textos.items():
        ruta = RAIZ / archivo
        if comprobar:
            igual = ruta.read_text(encoding="utf-8") == texto
            print(f"{archivo}: {'idéntico a ' + rev + ' + ediciones' if igual else 'DIFIERE de ' + rev + ' + ediciones'}")
            fallos += 0 if igual else 1
        else:
            ruta.write_text(texto, encoding="utf-8")
    print(f"{len(C)} sustituciones sobre {rev}: "
          + ", ".join(f"{sum(1 for x in C if x[1] == a)} en {a.split('/')[-1]}" for a in archivos))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
