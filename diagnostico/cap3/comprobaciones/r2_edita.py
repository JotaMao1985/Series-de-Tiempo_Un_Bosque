#!/usr/bin/env python3
"""R2 del capítulo 3 · reaplica sobre HEAD las ediciones de la ronda de gráficas.

Tres archivos: el capítulo 2 (armazón que heredan los capítulos 3 a 6), y las dos
fuentes del capítulo 3 (`ensamblado/cap3/cap3_modulos.html` y `cap3_js.js`). Parte del
contenido de cada uno en el commit base (por defecto HEAD), aplica cada sustitución
—que debe aparecer exactamente una vez— y escribe el resultado. Es reejecutable:
siempre parte del commit, no del archivo de trabajo.

Uso (desde la raíz del repo):
    python3 diagnostico/cap3/comprobaciones/r2_edita.py              # escribe
    python3 diagnostico/cap3/comprobaciones/r2_edita.py --comprobar  # solo compara
    python3 diagnostico/cap3/comprobaciones/r2_edita.py --base 5e082d2

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
MOD = "ensamblado/cap3/cap3_modulos.html"
JS = "ensamblado/cap3/cap3_js.js"

C = []  # (clave, archivo, antes, después)
MOVER = []  # (clave, archivo, inicio, fin, destino): el bloque [inicio, fin) pasa a ir antes de `destino`


def c(clave, archivo, antes, despues):
    C.append((clave, archivo, antes, despues))


# =====================================================================================
# ARMAZÓN · capítulo 2 (lo heredan los capítulos 3, 4, 5 y 6)
# =====================================================================================
c("armazón · marcasLegibles: el rezago 1, siempre", C2,
  r'''      for (const p of candidatos) {
        if (p < h * (1 - 1e-6) || !multiplo(p, h)) continue;
        const marcas = elegidas(p);
        if (marcas.length <= caben) {
          if (marcas.length < 2) return false;
          // El primer valor de un eje de rezagos (el rezago o el horizonte
          // 1), si no es ya una marca y hay sitio hasta la siguiente
          if (cuentaRezagos && marcas[0] > desde && marcas.length < caben &&
              (marcas[0] - desde) * (eje.width / (hasta - desde + 1)) >= ancho) {
            marcas.unshift(desde);
          }
          eje.ticks = marcas.map(i => ({ value: i }));
          return true;
        }
      }
      return false;
    }''',
  r'''      const paso = eje.width / (hasta - desde + 1);
      const texto = t => Math.max(1, t.length) * fuente * 0.62;
      for (const p of candidatos) {
        if (p < h * (1 - 1e-6) || !multiplo(p, h)) continue;
        let marcas = elegidas(p);
        if (marcas.length <= caben) {
          // Si del paso elegido no salen dos marcas, el eje es demasiado
          // estrecho para rotularlo aquí: se deja a Chart.js, como siempre.
          if (marcas.length < 2) return false;
          if (cuentaRezagos && valores[0] === 1 && marcas[0] > desde) {
            // El rezago 1 (o el horizonte 1) lleva siempre su número: es donde
            // se lee un AR(1) frente a un AR(2), o dónde se corta un MA. Antes
            // solo se rotulaba si sobraba sitio, y a 800 y 375 px no sobraba
            // nunca. Ahora se antepone al paso ya elegido —que no cambia—, y
            // se quitan las marcas que se le montarían (la del 2 o la del 3,
            // según el ancho). El 1 cuenta para el tope de marcas del eje
            // (`maxMarcas`): si con él se pasa, se quita la marca siguiente,
            // y no una de cada dos, que es lo que haría Chart.js. Un múltiplo
            // de 12 no se quita nunca; si no hay otra que quitar, el eje se
            // queda sin el 1.
            const fija = i => multiplo(valores[i - desde], 12);
            const junto = i => (i - desde) * paso <
              (texto(etiquetas[desde]) + texto(etiquetas[i])) / 2 + 4;
            const resto = marcas.filter(i => !junto(i) || fija(i));
            while (resto.length + 1 > tope) {
              const k = resto.findIndex(i => !fija(i));
              if (k < 0) break;
              resto.splice(k, 1);
            }
            if (resto.length + 1 <= tope) marcas = [desde].concat(resto);
          } else if (cuentaRezagos && marcas[0] > desde &&
              marcas.length < caben && (marcas[0] - desde) * paso >= ancho) {
            // Otro primer valor (un eje que empieza en 2 o en 3), si hay sitio
            marcas.unshift(desde);
          }
          eje.ticks = marcas.map(i => ({ value: i }));
          return true;
        }
      }
      return false;
    }''')

c("armazón · comentario de marcasLegibles", C2,
  r'''    //     24…), de modo que el 12 y el 24 salgan siempre que el eje llegue a
    //     ellos; y el primer valor, si cabe (el horizonte 1). Lo decide la''',
  r'''    //     24…), de modo que el 12 y el 24 salgan siempre que el eje llegue a
    //     ellos; y el 1 (el rezago o el horizonte 1), siempre. Lo decide la''')

c("armazón · actualizarLectura con el signo menos", C2,
  r'''    function actualizarLectura(elemento, campos) {
      elemento.innerHTML = campos
        .map(c => `<span><b>${c.etiqueta}</b> ${c.valor}</span>`)
        .join('');''',
  r'''    function actualizarLectura(elemento, campos) {
      elemento.innerHTML = campos
        .map(c => `<span><b>${conSignoMenos(c.etiqueta)}</b> ${conSignoMenos(c.valor)}</span>`)
        .join('');''')

c("armazón · conSignoMenos", C2,
  r'''    // Escribe una lectura numérica bajo un simulador. Lo que se ve cambia al''',
  r'''    // Signo menos tipográfico en las cifras de un texto: «-0.634» pasa a
    // «−0.634», como en las tablas y en los ejes. Solo toca el guion que abre
    // una cifra (al principio, o tras un espacio, un paréntesis, un igual, una
    // coma…): «1770-1869», «2015-01», «AR(1)-GARCH» o «e-05» quedan como están,
    // y lo que va dentro de una etiqueta HTML no se mira.
    function conSignoMenos(texto) {
      return String(texto).split(/(<[^>]*>)/).map((trozo, i) => i % 2 ? trozo
        : trozo.replace(/(^|[\s(\[=:,;±×|])-(?=\.?\d)/g, '$1−')).join('');
    }

    // Escribe una lectura numérica bajo un simulador. Lo que se ve cambia al''')

c("armazón · nota de dónde viven cifra() y descripcionCorrelograma()", C2,
  r'''    // Símbolo de d diferencias regulares para un rótulo del lienzo, que no
    // pasa por KaTeX: ∇, ∇², ∇³.''',
  r'''    // cifra() y descripcionCorrelograma() están más arriba, con
    // actualizarLectura(): los heredan los capítulos 3 a 6.

    // Símbolo de d diferencias regulares para un rótulo del lienzo, que no
    // pasa por KaTeX: ∇, ∇², ∇³.''')

# cifra() y descripcionCorrelograma() eran del JS propio del capítulo 2 (lo que queda
# bajo «Series de trabajo del capítulo», que cada capítulo sustituye). Pasan a la región
# heredada, delante de la autoevaluación, para que los simuladores de los capítulos 3 a
# 6 puedan escribir cifras con el signo menos y reescribir el `aria-label` de sus lienzos.
MOVER.append(("armazón · cifra() a la región heredada", C2,
              "    // Cifra de una lectura, escrita como en las tablas y en los ejes: punto\n",
              "    // cifra() y descripcionCorrelograma() están más arriba, con\n",
              "    // ================================================================\n"
              "    // Autoevaluación (v2)\n"))
MOVER.append(("armazón · descripcionCorrelograma() a la región heredada", C2,
              "    // Lo que un correlograma muestra, para el `aria-label` de su lienzo:\n",
              "    // Descripción del gráfico de una pregunta: da los datos que se ven —las\n",
              "    // ================================================================\n"
              "    // Autoevaluación (v2)\n"))


# =====================================================================================
# cap3_js.js · ayudantes
# =====================================================================================
c("JS · ayudantes de la ronda (nombres, descripciones, alto, ejes de dispersión)", JS,
  r'''    // ---------------------------------------------------------------
    // Álgebra de procesos ARMA en el navegador.''',
  r'''    // Rojo de lo que no cumple (no estacionario, no invertible, p < 0.05)
    const ROJO_GRAFICO = '#dc2626';

    // Nombre de un proceso del precálculo con letras griegas, como en los
    // selectores: «AR(1), phi = -0.7» -> «AR(1), φ = −0.7».
    function nombreProceso(p) {
      return p.nombre.replace(/phi/g, 'φ').replace(/theta/g, 'θ').replace(/-(?=\d)/g, '−');
    }

    // Texto de un `aria-label` para un panel de barras sin banda (ACF y PACF
    // teóricas, pesos ψ y π): qué es, cuántas barras hay, cuántas son
    // distintas de cero y cuánto valen las tres primeras. Se reescribe en cada
    // pintar(), para que el lienzo diga lo que dibuja en ese momento.
    function describirBarras(que, valores, primero = 1) {
      const noNulas = valores.filter(v => Math.abs(v) > 5e-5).length;
      return `${que} ${primero} a ${primero + valores.length - 1}: ` +
        `${noNulas} de ${valores.length} barras distintas de cero; las tres primeras valen ` +
        valores.slice(0, 3).map(v => cifra(v, 3)).join(', ');
    }

    // Descripción del gráfico de una pregunta: da los datos que se ven —todas
    // las barras, en orden, y la banda si la hay—, no lo que la pregunta pide
    // deducir de ellos.
    function describirBarrasQuiz(que, valores, b) {
      return `${que}. Valores de los rezagos 1 a ${valores.length}, en orden: ` +
        valores.map(v => cifra(v, 2)).join(', ') + '.' +
        (b ? ` Banda de referencia: ±${b.toFixed(3)}.` : '');
    }

    // Alto de un panel cuando el simulador es estrecho: el teléfono, o la
    // columna de 438 px que queda con la ventana a 800 px. Con la leyenda en
    // dos renglones y el título del eje, a los lienzos de 170-200 px les
    // quedaban 58-68 px de dibujo. En el escritorio no cambia nada. Hay que
    // llamarla antes de crear el gráfico.
    function altoEnEstrecho(canvas, alto) {
      const caja = canvas.parentNode;
      if (caja && caja.clientWidth && caja.clientWidth < 640) caja.style.height = `${alto}px`;
    }

    // Eje de un gráfico de dispersión con las marcas que tienen sentido en él
    // (los vértices ±2 del triángulo, la frontera ±1 de la invertibilidad, la
    // cota ±0.5), en vez de las que Chart.js deduce de los bordes (−2.4, 0,
    // 2.4). `marcas(eje)` devuelve la lista según el sitio que haya; las
    // cifras salen con cifra(), es decir, con el signo menos.
    function ejeDispersion(min, max, titulo, marcas) {
      return {
        type: 'linear', min: min, max: max,
        title: { display: true, text: titulo, font: { family: 'Montserrat', size: 12 } },
        ticks: {
          font: { family: 'Fira Code', size: 11 }, autoSkip: false, maxRotation: 0,
          callback: function (v) { return cifra(v, this.$decimales || 0); }
        },
        grid: { color: rejillaConCero },
        afterBuildTicks: eje => {
          const lista = marcas(eje);
          eje.$decimales = lista.every(v => Number.isInteger(v)) ? 0
            : (lista.every(v => Number.isInteger(v * 2)) ? 1 : 2);
          eje.ticks = lista.map(v => ({ value: v }));
        }
      };
    }

    // ---------------------------------------------------------------
    // Álgebra de procesos ARMA en el navegador.''')

c("JS · simularARMA sin aplanar lo explosivo", JS,
  r'''    // Simula un ARMA con ruido de semilla fija, descartando un tramo de
    // calentamiento para que la serie salga ya en régimen estacionario (es lo
    // que hace arima.sim() de R, y lo que generate_sample() de statsmodels
    // NO hace por defecto).
    function simularARMA(ar, ma, n, semilla, calentamiento = 200) {
      const total = n + calentamiento;
      const eps = generarRuidoNormal(total, semilla);
      const y = new Array(total).fill(0);
      for (let t = 0; t < total; t++) {
        let v = eps[t];
        for (let i = 1; i <= ar.length; i++) if (t - i >= 0) v += ar[i - 1] * y[t - i];
        for (let j = 1; j <= ma.length; j++) if (t - j >= 0) v += ma[j - 1] * eps[t - j];
        // Un proceso no estacionario diverge; se acota para que Chart.js pueda
        // dibujarlo sin romper la escala de los demás paneles.
        y[t] = Math.max(-1e6, Math.min(1e6, v));
      }
      return y.slice(calentamiento);
    }''',
  r'''    // Simula un ARMA con ruido de semilla fija. Si el proceso es estacionario
    // se descarta un tramo de calentamiento para que la serie salga ya en
    // régimen (es lo que hace arima.sim() de R, y lo que generate_sample() de
    // statsmodels NO hace por defecto).
    //
    // Si no lo es, no hay régimen al que llegar: la serie arranca de cero, sin
    // calentamiento, para que se la vea despegar. Hasta el 2026-11-21 se
    // calentaba igual y se acotaba en ±10⁶: un proceso explosivo saturaba
    // durante los 200 pasos descartados y lo que se dibujaba era una recta (y
    // unos correlogramas vacíos, porque la ACF de una constante es 0/0). Ahora
    // la serie se corta en el primer valor que pasa de ±UMBRAL_EXPLOSION —ese
    // valor se conserva—, de modo que puede devolver menos de n valores: quien
    // la dibuja rotula el eje con los que haya y lo dice en la lectura.
    const UMBRAL_EXPLOSION = 1e6;
    function simularARMA(ar, ma, n, semilla, calentamiento = 200) {
      if (!analizarAR(ar[0] || 0, ar[1] || 0).estacionario) calentamiento = 0;
      const total = n + calentamiento;
      const eps = generarRuidoNormal(total, semilla);
      const y = [];
      for (let t = 0; t < total; t++) {
        let v = eps[t];
        for (let i = 1; i <= ar.length; i++) if (t - i >= 0) v += ar[i - 1] * y[t - i];
        for (let j = 1; j <= ma.length; j++) if (t - j >= 0) v += ma[j - 1] * eps[t - j];
        y.push(v);
        if (Math.abs(v) > UMBRAL_EXPLOSION) break;
      }
      return y.slice(calentamiento);
    }

    // Frase de la lectura cuando simularARMA() cortó la serie
    function avisoDeCorte(y) {
      return `pasa de ±${cifra(UMBRAL_EXPLOSION, 0)} en t = ${y.length} y se dibuja hasta ahí`;
    }

    // (La varianza muestral con la que se decide si hay ACF que calcular es
    // varianzaMuestral(), del armazón heredado del capítulo 2.)''')

c("JS · correlogramaDoble: color de la muestral, leyenda corta, conjuntos que se ocultan", JS,
  r'''    // Correlograma con dos juegos de barras: teórico (sólido) y muestral (claro)
    function correlogramaDoble(canvas, etiquetas, teorica, muestral, n, etiquetaTipo, color) {
      return crearGraficoBarras(canvas, etiquetas, teorica, {
        etiqueta: `${etiquetaTipo} teórica`,
        color: color,
        barrasExtra: [{
          etiqueta: `${etiquetaTipo} muestral`,
          valores: muestral,
          color: 'rgba(255, 102, 0, 0.5)'
        }],
        lineas: lineasBanda(n),
        tituloX: 'Rezago k'
      });
    }

    // Índices de los datasets de un gráfico de barras creado con barrasExtra:
    // 0 = barras principales, 1 = barras extra, 2 y 3 = las dos rectas de banda.
    function actualizarDoble(grafico, teorica, muestral, n) {
      const largo = grafico.data.labels.length;
      grafico.data.datasets[0].data = teorica;
      grafico.data.datasets[1].data = muestral;
      const b = banda(n);
      grafico.data.datasets[2].data = Array(largo).fill(b);
      grafico.data.datasets[3].data = Array(largo).fill(-b);
      grafico.update('none');
    }''',
  r'''    // Correlograma con dos juegos de barras: teórico (oscuro) y muestral (gris).
    //
    // La muestral iba en el naranja de marca al 50 % (1.75:1 sobre blanco, y de
    // la misma familia que la banda): ahora va en el gris de la paleta, que
    // llega a 3:1 y no se confunde ni con la banda naranja ni con la teórica.
    // La leyenda dice «Teórica · Muestral · Banda» —cuál de las dos funciones
    // es lo dice la etiqueta del panel—, para que quepa en un renglón en el
    // teléfono. `etiquetaTipo` se conserva en la firma por quien la llama.
    const COLOR_MUESTRAL = COLORES_GRAFICO.gris;
    function correlogramaDoble(canvas, etiquetas, teorica, muestral, n, etiquetaTipo, color) {
      const b = banda(n);
      const grafico = crearGraficoBarras(canvas, etiquetas, teorica, {
        etiqueta: 'Teórica',
        color: color,
        barrasExtra: [{
          etiqueta: 'Muestral',
          valores: muestral,
          color: COLOR_MUESTRAL
        }],
        lineas: [{ valor: b, etiqueta: 'Banda' }, { valor: -b, etiqueta: '' }],
        tituloX: 'Rezago k'
      });
      // Quinto conjunto: un rombo sobre las barras muestrales que se quieran
      // señalar (actualizarDoble). Va además del color, para que la señal no
      // dependa de distinguir el rojo del gris.
      grafico.data.datasets.push({
        type: 'line', label: '', data: [], showLine: false, $marcador: true,
        pointStyle: 'rectRot', pointRadius: 5, pointHoverRadius: 5, clip: false,
        borderColor: ROJO_GRAFICO, backgroundColor: '#ffffff', borderWidth: 2, order: 0
      });
      const rotulos = grafico.options.plugins.legend.labels;
      rotulos.generateLabels = chart => etiquetasDeLeyendaBarras(chart).map(item => {
        if (chart.data.datasets[item.datasetIndex].$marcador) {
          Object.assign(item, {
            pointStyle: 'rectRot', fillStyle: '#ffffff', strokeStyle: ROJO_GRAFICO,
            lineWidth: 2, lineDash: []
          });
        }
        return item;
      });
      grafico.options.plugins.tooltip.filter =
        item => item.dataset.label !== '' && !item.dataset.$marcador;
      grafico.update('none');
      return grafico;
    }

    // Índices de los datasets de un gráfico de barras creado con barrasExtra:
    // 0 = barras principales, 1 = barras extra, 2 y 3 = las dos rectas de banda.
    //
    // `teorica` o `muestral` pueden ser null: ese juego no existe (la ACF
    // teórica de un proceso no estacionario, la muestral de una serie sin
    // varianza finita) y entonces no se dibuja ni sale en la leyenda, que
    // filtra las entradas sin texto. Antes se dibujaban ceros bajo el rótulo
    // «ACF teórica»: el gráfico decía «ruido blanco». `senalados` es la lista
    // de rezagos (1, 2…) cuya barra muestral se destaca: va en rojo y con un
    // rombo en la punta (dataset 4), y la leyenda gana la entrada «Se asoma».
    function actualizarDoble(grafico, teorica, muestral, n, senalados = []) {
      const largo = grafico.data.labels.length;
      const coloresMuestral = senalados.length && muestral
        ? muestral.map((_, k) => senalados.includes(k + 1) ? ROJO_GRAFICO : COLOR_MUESTRAL) : null;
      const alto = grafico.options.scales.y.max || grafico.options.scales.y.suggestedMax || 1;
      grafico.data.datasets[4].data = muestral && senalados.length
        ? muestral.map((v, k) => senalados.includes(k + 1) ? v + Math.sign(v) * 0.09 * alto : null) : [];
      grafico.data.datasets[4].label = senalados.length ? 'Se asoma' : '';
      grafico.data.datasets[0].data = teorica || [];
      grafico.data.datasets[0].label = teorica ? 'Teórica' : '';
      grafico.data.datasets[1].data = muestral || [];
      grafico.data.datasets[1].label = muestral ? 'Muestral' : '';
      grafico.data.datasets[1].backgroundColor = coloresMuestral || COLOR_MUESTRAL;
      const b = banda(n);
      grafico.data.datasets[2].data = Array(largo).fill(b);
      grafico.data.datasets[3].data = Array(largo).fill(-b);
      grafico.update('none');
    }''')

# -------------------------------------------------------------------------------------
# M2 · panel AR
# -------------------------------------------------------------------------------------
c("JS · M2 panel AR: aria-label con el proceso", JS,
  r'''        gPacf.data.datasets[0].data = p.pacf_teorica;
        gPacf.update('none');

        const filas = [
          { etiqueta: 'Proceso:', valor: `AR(${p.p})` },''',
  r'''        gPacf.data.datasets[0].data = p.pacf_teorica;
        gPacf.update('none');
        c[0].setAttribute('aria-label',
          describirBarras(`ACF teórica del ${nombreProceso(p)}, rezagos`, p.acf_teorica));
        c[1].setAttribute('aria-label',
          describirBarras(`PACF teórica del ${nombreProceso(p)}, rezagos`, p.pacf_teorica));

        const filas = [
          { etiqueta: 'Proceso:', valor: `AR(${p.p})` },''')

# -------------------------------------------------------------------------------------
# M2 · triángulo
# -------------------------------------------------------------------------------------
c("JS · M2 triángulo: leyenda con cada cosa dibujada como es", JS,
  r'''            {
              label: 'Región estacionaria',
              data: [{ x: -2, y: -1 }, { x: 2, y: -1 }, { x: 0, y: 1 }, { x: -2, y: -1 }],
              showLine: true, fill: true,
              backgroundColor: 'rgba(1, 40, 32, 0.08)',
              borderColor: COLORES_GRAFICO.primario,
              borderWidth: 1.5, pointRadius: 0, order: 3
            },
            {
              label: 'Bajo la curva: raíces complejas',
              data: parabola,
              showLine: true, fill: false,
              borderColor: COLORES_GRAFICO.terciario,
              borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, order: 2
            },
            {
              label: '(φ₁, φ₂)',
              data: [{ x: params.phi1, y: params.phi2 }],
              backgroundColor: COLORES_GRAFICO.secundario,
              borderColor: '#ffffff', borderWidth: 2,
              pointRadius: 8, pointHoverRadius: 9, order: 1
            }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false, animation: false,
          scales: {
            x: {
              min: -2.4, max: 2.4,
              title: { display: true, text: 'φ₁', font: { family: 'Montserrat', size: 12 } },
              ticks: { font: { family: 'Fira Code', size: 11 } },
              grid: { color: 'rgba(148, 163, 184, 0.2)' }
            },
            y: {
              min: -1.3, max: 1.3,
              title: { display: true, text: 'φ₂', font: { family: 'Montserrat', size: 12 } },
              ticks: { font: { family: 'Fira Code', size: 11 } },
              grid: { color: 'rgba(148, 163, 184, 0.2)' }
            }
          },
          plugins: {
            legend: { labels: { font: { family: 'Montserrat', size: 11 }, boxWidth: 20 } },
            tooltip: { backgroundColor: '#012820', bodyFont: { family: 'Fira Code' } }
          }
        }
      });

      const gSerie = serieSimple(c[1],
        simularARMA([params.phi1, params.phi2], [], 160, 20260726),
        'Realización simulada', COLORES_GRAFICO.primario);''',
  r'''            {
              label: 'Estacionario',
              data: [{ x: -2, y: -1 }, { x: 2, y: -1 }, { x: 0, y: 1 }, { x: -2, y: -1 }],
              showLine: true, fill: true, pointStyle: 'rect',
              backgroundColor: 'rgba(1, 40, 32, 0.08)',
              borderColor: COLORES_GRAFICO.primario,
              borderWidth: 1.5, pointRadius: 0, order: 3
            },
            {
              label: 'Debajo: raíces complejas',
              data: parabola,
              showLine: true, fill: false, pointStyle: 'line',
              borderColor: COLORES_GRAFICO.terciario,
              borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, order: 2
            },
            {
              // clip: false para que el punto se vea entero en los extremos
              // de los deslizadores, (±2.2, ±1.2), pegados al borde del área
              label: '(φ₁, φ₂)',
              data: [{ x: params.phi1, y: params.phi2 }],
              backgroundColor: COLORES_GRAFICO.secundario, pointStyle: 'circle',
              borderColor: '#ffffff', borderWidth: 2, clip: false,
              pointRadius: 8, pointHoverRadius: 9, order: 1
            }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false, animation: false,
          scales: {
            // Los vértices del triángulo están en φ₁ = ±2 y φ₂ = ±1: son las
            // marcas que tienen que llevar número, a cualquier ancho.
            x: ejeDispersion(-2.4, 2.4, 'φ₁', eje => eje.width >= 380
              ? [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2] : [-2, -1, 0, 1, 2]),
            y: ejeDispersion(-1.3, 1.3, 'φ₂', eje => eje.height >= 110
              ? [-1, -0.5, 0, 0.5, 1] : [-1, 0, 1])
          },
          plugins: {
            legend: {
              labels: {
                font: { family: 'Montserrat', size: 11 }, boxWidth: 18, boxHeight: 8,
                usePointStyle: true
              }
            },
            tooltip: { backgroundColor: '#012820', bodyFont: { family: 'Fira Code' } }
          }
        }
      });

      const gSerie = serieSimple(c[1],
        simularARMA([params.phi1, params.phi2], [], 160, 20260726),
        'Realización simulada', COLORES_GRAFICO.primario);''')

c("JS · M2 triángulo: alto en estrecho", JS,
  r'''      const gTriangulo = new Chart(c[0], {
        type: 'scatter',''',
  r'''      altoEnEstrecho(c[0], 300);
      const gTriangulo = new Chart(c[0], {
        type: 'scatter',''')

c("JS · M2 triángulo: la serie despega, aviso y aria-label", JS,
  r'''        const color = a.estacionario ? COLORES_GRAFICO.secundario : '#dc2626';

        gTriangulo.data.datasets[2].data = [{ x: params.phi1, y: params.phi2 }];
        gTriangulo.data.datasets[2].backgroundColor = color;
        gTriangulo.update('none');

        // Un proceso no estacionario explota: verlo explotar es la lección
        gSerie.data.datasets[0].data = simularARMA([params.phi1, params.phi2], [], 160, 20260726);
        gSerie.data.datasets[0].borderColor = a.estacionario ? COLORES_GRAFICO.primario : '#dc2626';
        gSerie.data.datasets[0].backgroundColor = gSerie.data.datasets[0].borderColor;
        gSerie.update('none');
''',
  r'''        const color = a.estacionario ? COLORES_GRAFICO.secundario : ROJO_GRAFICO;

        gTriangulo.data.datasets[2].data = [{ x: params.phi1, y: params.phi2 }];
        gTriangulo.data.datasets[2].backgroundColor = color;
        gTriangulo.update('none');

        // Un proceso no estacionario explota: verlo explotar es la lección.
        // simularARMA() lo arranca de cero y lo corta al pasar de ±10⁶, así
        // que el eje se rotula con los valores que haya.
        const N_SERIE = 160;
        const y = simularARMA([params.phi1, params.phi2], [], N_SERIE, 20260726);
        const cortada = y.length < N_SERIE;
        gSerie.data.labels = y.map((_, i) => String(i + 1));
        gSerie.data.datasets[0].data = y;
        gSerie.data.datasets[0].borderColor = a.estacionario ? COLORES_GRAFICO.primario : ROJO_GRAFICO;
        gSerie.data.datasets[0].backgroundColor = gSerie.data.datasets[0].borderColor;
        gSerie.update('none');

        const punto = `φ₁ = ${cifra(params.phi1, 2)}, φ₂ = ${cifra(params.phi2, 2)}`;
        c[0].setAttribute('aria-label',
          `Triángulo de estacionariedad del AR(2) con el punto ${punto} marcado: ` +
          `${a.estacionario ? 'dentro' : 'fuera'} de la región estacionaria, raíces ` +
          `${a.complejas ? 'complejas' : 'reales'}`);
        c[1].setAttribute('aria-label',
          `Realización simulada del AR(2) con ${punto}: ` +
          (cortada ? `no estacionaria; ${avisoDeCorte(y)}`
            : `${y.length} valores, ${a.estacionario ? 'estacionaria' : 'no estacionaria'}`));
''')

c("JS · M2 triángulo: fila del corte en la lectura", JS,
  r'''        if (a.complejas && a.estacionario) {
          filas.push({ etiqueta: 'Pseudo-periodo:', valor: `${a.periodo.toFixed(2)} periodos` });
        }
        actualizarLectura(lectura, filas);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi1', etiqueta: 'φ₁ = ', min: -2.2, max: 2.2, paso: 0.01 },''',
  r'''        if (a.complejas && a.estacionario) {
          filas.push({ etiqueta: 'Pseudo-periodo:', valor: `${a.periodo.toFixed(2)} periodos` });
        }
        if (cortada) filas.push({ etiqueta: 'La serie', valor: avisoDeCorte(y) });
        actualizarLectura(lectura, filas);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi1', etiqueta: 'φ₁ = ', min: -2.2, max: 2.2, paso: 0.01 },''')

# -------------------------------------------------------------------------------------
# M3 · panel MA y curva rho1(theta)
# -------------------------------------------------------------------------------------
c("JS · M3 panel MA: aria-label con el proceso", JS,
  r'''        gPacf.data.datasets[0].data = p.pacf_teorica;
        gPacf.update('none');
        actualizarLectura(lectura, [
          { etiqueta: 'Proceso:', valor: `MA(${p.q})` },''',
  r'''        gPacf.data.datasets[0].data = p.pacf_teorica;
        gPacf.update('none');
        c[0].setAttribute('aria-label',
          describirBarras(`ACF teórica del ${nombreProceso(p)}, rezagos`, p.acf_teorica));
        c[1].setAttribute('aria-label',
          describirBarras(`PACF teórica del ${nombreProceso(p)}, rezagos`, p.pacf_teorica));
        actualizarLectura(lectura, [
          { etiqueta: 'Proceso:', valor: `MA(${p.q})` },''')

c("JS · M3 rho1: constante de rojo", JS,
  r'''      const X_MAX = 5;
      const ROJO = '#dc2626';
      const rho1 = t => t / (1 + t * t);''',
  r'''      const X_MAX = 5;
      const ROJO = ROJO_GRAFICO;
      const rho1 = t => t / (1 + t * t);''')

c("JS · M3 rho1: puntos enteros en los bordes", JS,
  r'''            {
              label: 'θ',
              data: [], pointStyle: 'circle',
              borderColor: '#ffffff', borderWidth: 2, pointRadius: 8, pointHoverRadius: 9, order: 1
            },
            {
              label: '1/θ',
              data: [], pointStyle: 'rectRot',
              borderColor: '#ffffff', borderWidth: 2, pointRadius: 9, pointHoverRadius: 10, order: 2
            }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false, animation: false,
          scales: {
            x: {
              min: -X_MAX, max: X_MAX,
              title: { display: true, text: 'θ', font: { family: 'Montserrat', size: 12 } },
              ticks: { font: { family: 'Fira Code', size: 11 } },
              grid: { color: 'rgba(148, 163, 184, 0.2)' }
            },
            y: {
              min: -0.7, max: 0.7,
              title: { display: true, text: 'ρ₁', font: { family: 'Montserrat', size: 12 } },
              ticks: { font: { family: 'Fira Code', size: 11 } },
              grid: { color: 'rgba(148, 163, 184, 0.2)' }
            }
          },''',
  r'''            {
              // clip: false para que con θ = ±5 el círculo no salga cortado
              label: 'θ',
              data: [], pointStyle: 'circle', clip: false,
              borderColor: '#ffffff', borderWidth: 2, pointRadius: 8, pointHoverRadius: 9, order: 1
            },
            {
              label: '1/θ',
              data: [], pointStyle: 'rectRot', clip: false,
              borderColor: '#ffffff', borderWidth: 2, pointRadius: 9, pointHoverRadius: 10, order: 2
            }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false, animation: false,
          scales: {
            // θ = ±1 es la frontera de la invertibilidad y ±0.5 la cota de ρ₁:
            // las dos llevan número a cualquier ancho.
            x: ejeDispersion(-X_MAX, X_MAX, 'θ', eje => eje.width >= 380
              ? [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5] : [-5, -3, -1, 1, 3, 5]),
            y: ejeDispersion(-0.7, 0.7, 'ρ₁', eje => eje.height >= 130
              ? [-0.5, -0.25, 0, 0.25, 0.5] : [-0.5, 0, 0.5])
          },''')

c("JS · M3 rho1: alto en estrecho", JS,
  r'''      const gCurva = new Chart(c[0], {
        type: 'scatter',''',
  r'''      altoEnEstrecho(c[0], 290);
      const gCurva = new Chart(c[0], {
        type: 'scatter',''')

c("JS · M3 rho1: aria-label con θ", JS,
  r'''        gCurva.data.datasets[5].backgroundColor = colorInv;
        gCurva.update('none');
''',
  r'''        gCurva.data.datasets[5].backgroundColor = colorInv;
        gCurva.update('none');
        c[0].setAttribute('aria-label',
          `Curva de ρ₁ = θ/(1 + θ²) de un MA(1), con θ = ${cifra(t, 2)} marcado a la altura ` +
          `ρ₁ = ${cifra(r, 4)}` + (cero ? '; el recíproco 1/θ no existe'
            : ` y su recíproco 1/θ = ${cifra(inv, 4)} a la misma altura` +
              (Math.abs(inv) > X_MAX ? ', fuera de la gráfica' : '')) +
          `; ${invertible ? 'θ es el invertible de la pareja' : (frontera ? 'frontera, no invertible' : 'θ no es invertible')}`);
''')

# -------------------------------------------------------------------------------------
# M4 · dualidad
# -------------------------------------------------------------------------------------
c("JS · M4: frontera, escala de los π y aria-label", JS,
  r'''        const invertible = Math.abs(params.theta) < 1;
        const h = Math.round(params.h);
        const varH = psi.slice(0, h).reduce((s, v) => s + v * v, 0);
        const varLimite = pesosPsi(ar, ma, N_LIMITE).reduce((s, v) => s + v * v, 0);

        gPsi.data.datasets[0].data = psi;
        gPsi.data.datasets[0].backgroundColor = coloresPsi(h);
        gPsi.update('none');
        gPi.data.datasets[0].data = pi;
        gPi.data.datasets[0].backgroundColor = invertible ? COLORES_GRAFICO.terciario : '#dc2626';
        // Los pesos no invertibles se salen de [-1, 1]: se deja que la escala
        // crezca para que la divergencia se vea.
        gPi.options.scales.y.suggestedMax = invertible ? 1 : Math.max(...pi.map(Math.abs));
        gPi.options.scales.y.suggestedMin = invertible ? -1 : -Math.max(...pi.map(Math.abs));
        gPi.update('none');

        const maxPi = Math.max(...pi.map(Math.abs));
        actualizarLectura(lectura, [
          { etiqueta: 'Estacionario (|φ| < 1):', valor: Math.abs(params.phi) < 1 ? 'SÍ' : 'NO' },
          { etiqueta: 'Invertible (|θ| < 1):', valor: invertible ? 'SÍ' : 'NO' },
          { etiqueta: 'ψ₁₂ =', valor: psi[N].toFixed(4) },
          { etiqueta: 'π₁₂ =', valor: pi[N].toFixed(4) },
          {
            etiqueta: 'máx |πⱼ| =',
            valor: maxPi.toFixed(4) + (invertible ? '' : ' — los pesos crecen: no invertible')
          },
          { etiqueta: 'Var(e) a h pasos ÷ σ² = Σ ψⱼ², j < h:', valor: varH.toFixed(4) },''',
  r'''        // En la frontera |θ| = 1 el MA tampoco es invertible, pero sus π no
        // crecen: se quedan con la misma magnitud. Son tres casos, no dos.
        const frontera = Math.abs(Math.abs(params.theta) - 1) < 1e-9;
        const invertible = Math.abs(params.theta) < 1 && !frontera;
        const h = Math.round(params.h);
        const varH = psi.slice(0, h).reduce((s, v) => s + v * v, 0);
        const varLimite = pesosPsi(ar, ma, N_LIMITE).reduce((s, v) => s + v * v, 0);
        const maxPi = Math.max(...pi.map(Math.abs));

        gPsi.data.datasets[0].data = psi;
        gPsi.data.datasets[0].backgroundColor = coloresPsi(h);
        gPsi.update('none');

        // Los pesos no invertibles se salen de [-1, 1]. Mientras el mayor no
        // pase de TOPE_LINEAL la escala crece con ellos. Más allá (θ = 2 lleva
        // π₁₂ a 6 041.6) una escala lineal la fija el último peso y los once
        // primeros no se ven: se pasa a una escala logarítmica con signo,
        // s(π) = signo(π)·log₁₀(1 + |π|), rotulada con los valores de π (±10,
        // ±100, ±1 000…). En ella un crecimiento geométrico sube a paso casi
        // constante (exacto solo en el límite, por el 1 que se suma).
        const TOPE_LINEAL = 20;
        const logaritmica = !invertible && maxPi > TOPE_LINEAL;
        const s = v => Math.sign(v) * Math.log10(1 + Math.abs(v));
        const ejePi = gPi.options.scales.y;
        gPi.data.datasets[0].data = logaritmica ? pi.map(s) : pi;
        gPi.data.datasets[0].label = logaritmica ? 'πⱼ (eje logarítmico)' : 'πⱼ';
        gPi.data.datasets[0].backgroundColor = invertible ? COLORES_GRAFICO.terciario : ROJO_GRAFICO;
        if (logaritmica) {
          const decadas = Math.ceil(Math.log10(maxPi));
          const tope = s(Math.pow(10, decadas));
          ejePi.min = -tope;
          ejePi.max = tope;
          ejePi.afterBuildTicks = eje => {
            // Una marca (y su línea de rejilla) por década, de ±10 en adelante:
            // el ±1 queda a 3 px del 0 y se montaría. Si no caben todos los
            // números, se rotula una década sí y otra no, contando desde la
            // mayor; la rejilla se queda en todas.
            eje.$cada = eje.height >= 15 * (2 * decadas + 1) ? 1 : 2;
            const lista = [0];
            for (let k = decadas; k >= 1; k--) lista.push(s(Math.pow(10, k)), -s(Math.pow(10, k)));
            eje.ticks = lista.sort((a, b) => a - b).map(v => ({ value: v }));
          };
          ejePi.ticks.callback = function (v) {
            if (v === 0) return '0';
            const k = Math.round(Math.log10(Math.pow(10, Math.abs(v)) - 1));
            return (decadas - k) % (this.$cada || 1) ? ''
              : cifra(Math.sign(v) * Math.pow(10, k), 0);
          };
        } else {
          delete ejePi.min;
          delete ejePi.max;
          ejePi.suggestedMax = invertible ? 1 : maxPi;
          ejePi.suggestedMin = invertible ? -1 : -maxPi;
          ejePi.afterBuildTicks = marcasVerticales;
          ejePi.ticks.callback = rotuloVertical;
        }
        gPi.options.plugins.tooltip.callbacks.label = item =>
          `πⱼ: ${cifra(pi[item.dataIndex], 4)}`;
        gPi.update('none');

        const proceso = `φ = ${cifra(params.phi, 2)} y θ = ${cifra(params.theta, 2)}`;
        c[0].setAttribute('aria-label', describirBarras(
          `Pesos ψ de la representación de medias móviles infinita con ${proceso}, j de`, psi, 0) +
          `; en color oscuro, ${h === 1 ? 'el único que entra' : `los ${h} que entran`} en la varianza ` +
          `del pronóstico a ${h} ${h === 1 ? 'paso' : 'pasos'}`);
        c[1].setAttribute('aria-label', describirBarras(
          `Pesos π de la representación autorregresiva infinita con ${proceso}, j de`, pi, 0) +
          `; el mayor en valor absoluto, ${cifra(maxPi, 4)}` +
          (logaritmica ? '; dibujados en escala logarítmica' : ''));

        actualizarLectura(lectura, [
          { etiqueta: 'Estacionario (|φ| < 1):', valor: Math.abs(params.phi) < 1 ? 'SÍ' : 'NO' },
          { etiqueta: 'Invertible (|θ| < 1):', valor: invertible ? 'SÍ' : (frontera ? 'NO — frontera, |θ| = 1' : 'NO') },
          { etiqueta: 'ψ₁₂ =', valor: psi[N].toFixed(4) },
          { etiqueta: 'π₁₂ =', valor: pi[N].toFixed(4) },
          {
            etiqueta: 'máx |πⱼ| =',
            valor: maxPi.toFixed(4) + (invertible ? ''
              : (frontera ? ' — los pesos no decaen: no invertible'
                : ' — los pesos crecen: no invertible' +
                  (logaritmica ? ' (eje logarítmico)' : '')))
          },
          { etiqueta: 'Var(e) a h pasos ÷ σ² = Σ ψⱼ², j < h (barras oscuras):', valor: varH.toFixed(4) },''')

# -------------------------------------------------------------------------------------
# M5 · laboratorio
# -------------------------------------------------------------------------------------
c("JS · M5 laboratorio: alto en estrecho", JS,
  r'''      const gSerie = serieSimple(c[0], simularARMA([0.7, 0], [0.5, 0], 200, SEMILLA_BASE),
        'Realización simulada', COLORES_GRAFICO.primario);''',
  r'''      altoEnEstrecho(c[1], 240);
      altoEnEstrecho(c[2], 240);
      const gSerie = serieSimple(c[0], simularARMA([0.7, 0], [0.5, 0], 200, SEMILLA_BASE),
        'Realización simulada', COLORES_GRAFICO.primario);''')

c("JS · M5 laboratorio: lo explosivo se ve, la teórica se oculta, la muestral avisa", JS,
  r'''        const y = simularARMA(ar, ma, T, SEMILLA_BASE + realizacion - 1);
        const acfM = calcularACF(y, MAX);
        const pacfM = calcularPACF(acfM, MAX);
        // Si el proceso no es estacionario la ACF teórica sencillamente no
        // existe: se dibujan ceros y se avisa en la lectura.
        const acfT = a.estacionario ? acfTeorica(ar, ma, MAX) : new Array(MAX).fill(0);
        const pacfT = a.estacionario ? calcularPACF(acfT, MAX) : new Array(MAX).fill(0);

        gSerie.data.labels = y.map((_, i) => String(i + 1));
        gSerie.data.datasets[0].data = y;
        gSerie.data.datasets[0].label = `Realización, T = ${T}`;
        gSerie.data.datasets[0].borderColor = a.estacionario ? COLORES_GRAFICO.primario : '#dc2626';
        gSerie.update('none');

        actualizarDoble(gAcf, acfT, acfM, T);
        actualizarDoble(gPacf, pacfT, pacfM, T);

        const p = params.phi2 !== 0 ? 2 : (params.phi1 !== 0 ? 1 : 0);
        const q = params.theta2 !== 0 ? 2 : (params.theta1 !== 0 ? 1 : 0);
        let dif = 0;
        if (a.estacionario) {
          for (let k = 0; k < MAX; k++) dif += Math.abs(acfT[k] - acfM[k]);
          dif /= MAX;
        }
        actualizarLectura(lectura, [
          { etiqueta: 'Modelo:', valor: `ARMA(${p}, ${q})` },
          { etiqueta: 'Estacionario:', valor: a.estacionario ? 'SÍ' : 'NO — la ACF teórica no existe' },
          { etiqueta: 'Invertible:', valor: invertible ? 'SÍ' : 'NO' },
          { etiqueta: 'banda =', valor: `±${banda(T).toFixed(4)}` },
          { etiqueta: 'Realización:', valor: `n.º ${realizacion}` },
          {
            etiqueta: 'distancia media |teórica − muestral|:',
            valor: a.estacionario ? dif.toFixed(4) : '—'
          }
        ]);
      }''',
  r'''        // Un proceso explosivo se corta al pasar de ±10⁶ (simularARMA): la
        // serie puede tener menos de T valores, y la banda y los correlogramas
        // muestrales se calculan con los que hay.
        const y = simularARMA(ar, ma, T, SEMILLA_BASE + realizacion - 1);
        const n = y.length;
        const cortada = n < T;
        // La ACF muestral necesita más valores que rezagos y una varianza
        // finita y positiva; si no, no se dibuja y la lectura dice por qué.
        const varianza = varianzaMuestral(y);
        let acfM = null, pacfM = null, motivo = '';
        if (n < MAX + 2) {
          motivo = `no se calculan: la serie se queda en ${n} valores y harían falta más de ${MAX + 1}`;
        } else if (!Number.isFinite(varianza) || !(varianza > 0)) {
          motivo = 'no se calculan: la varianza muestral no es finita';
        } else {
          acfM = calcularACF(y, MAX);
          pacfM = calcularPACF(acfM, MAX);
          if (!acfM.every(Number.isFinite) || !pacfM.every(Number.isFinite)) {
            acfM = pacfM = null;
            motivo = 'no se calculan: la varianza muestral no es finita';
          }
        }
        // Si el proceso no es estacionario la ACF teórica sencillamente no
        // existe: no se dibuja (antes se dibujaban ceros) y se avisa en la lectura.
        const acfT = a.estacionario ? acfTeorica(ar, ma, MAX) : null;
        const pacfT = a.estacionario ? calcularPACF(acfT, MAX) : null;
        const colorSerie = a.estacionario ? COLORES_GRAFICO.primario : ROJO_GRAFICO;

        gSerie.data.labels = y.map((_, i) => String(i + 1));
        gSerie.data.datasets[0].data = y;
        gSerie.data.datasets[0].label = cortada ? `Realización: ${n} de T = ${T}` : `Realización, T = ${T}`;
        gSerie.data.datasets[0].borderColor = colorSerie;
        gSerie.data.datasets[0].backgroundColor = colorSerie;
        gSerie.update('none');

        actualizarDoble(gAcf, acfT, acfM, n);
        actualizarDoble(gPacf, pacfT, pacfM, n);

        const p = params.phi2 !== 0 ? 2 : (params.phi1 !== 0 ? 1 : 0);
        const q = params.theta2 !== 0 ? 2 : (params.theta1 !== 0 ? 1 : 0);
        let dif = 0;
        if (a.estacionario && acfM) {
          for (let k = 0; k < MAX; k++) dif += Math.abs(acfT[k] - acfM[k]);
          dif /= MAX;
        }

        const nombre = `ARMA(${p}, ${q}) con φ = (${cifra(params.phi1, 2)}, ${cifra(params.phi2, 2)}) ` +
          `y θ = (${cifra(params.theta1, 2)}, ${cifra(params.theta2, 2)})`;
        const b = banda(n);
        c[0].setAttribute('aria-label', `Realización n.º ${realizacion} del ${nombre}: ` +
          (cortada ? `no estacionaria; ${avisoDeCorte(y)}`
            : `${n} valores, ${a.estacionario ? 'estacionaria' : 'no estacionaria'}`));
        [[c[1], 'ACF', acfM, acfT], [c[2], 'PACF', pacfM, pacfT]].forEach(([lienzo, tipo, muestral, teorica]) => {
          lienzo.setAttribute('aria-label',
            (muestral ? descripcionCorrelograma(`${tipo} muestral`, `una realización del ${nombre}`, muestral, b)
              : `${tipo} muestral del ${nombre}: no se dibuja`) +
            (teorica ? `; la teórica vale ${cifra(teorica[0], 3)} en el rezago 1`
              : `; la ${tipo} teórica no existe`));
        });

        const filas = [
          { etiqueta: 'Modelo:', valor: `ARMA(${p}, ${q})` },
          { etiqueta: 'Estacionario:', valor: a.estacionario ? 'SÍ' : 'NO — la ACF teórica no existe y no se dibuja' },
          { etiqueta: 'Invertible:', valor: invertible ? 'SÍ' : 'NO' },
          { etiqueta: 'banda =', valor: `±${b.toFixed(4)}` },
          { etiqueta: 'Realización:', valor: `n.º ${realizacion}` },
          {
            etiqueta: 'distancia media |teórica − muestral|:',
            valor: a.estacionario && acfM ? dif.toFixed(4) : '—'
          }
        ];
        if (cortada) filas.push({ etiqueta: 'La serie', valor: avisoDeCorte(y) });
        if (motivo) filas.push({ etiqueta: 'ACF y PACF muestrales:', valor: motivo });
        actualizarLectura(lectura, filas);
      }''')

# -------------------------------------------------------------------------------------
# M6 · teórica frente a muestral
# -------------------------------------------------------------------------------------
c("JS · M6: alto en estrecho", JS,
  r'''      const gAcf = correlogramaDoble(c[0], REZAGOS_T, PROCESOS.ar1_pos.acf_teorica,
        DATOS_CAP3.realizaciones.ar1_pos.acf, DATOS_CAP3.realizaciones.ar1_pos.n,
        'ACF', COLORES_GRAFICO.primario);''',
  r'''      altoEnEstrecho(c[0], 250);
      altoEnEstrecho(c[1], 250);
      const gAcf = correlogramaDoble(c[0], REZAGOS_T, PROCESOS.ar1_pos.acf_teorica,
        DATOS_CAP3.realizaciones.ar1_pos.acf, DATOS_CAP3.realizaciones.ar1_pos.n,
        'ACF', COLORES_GRAFICO.primario);''')

c("JS · M6: escala, barras que se asoman en rojo, lectura y aria-label", JS,
  r'''        actualizarDoble(gAcf, p.acf_teorica, r.acf, r.n);
        actualizarDoble(gPacf, p.pacf_teorica, r.pacf, r.n);

        // Rezagos donde la teoría dice exactamente cero y la muestra no lo dice
        let ceros = 0, fuera = 0;
        p.acf_teorica.forEach((v, k) => {
          if (Math.abs(v) < 1e-9) { ceros++; if (Math.abs(r.acf[k]) > banda(r.n)) fuera++; }
        });
        actualizarLectura(lectura, [
          { etiqueta: 'Proceso:', valor: p.nombre },
          { etiqueta: 'T =', valor: r.n },
          { etiqueta: 'banda =', valor: `±${banda(r.n).toFixed(4)}` },
          {
            etiqueta: 'rezagos con ACF teórica nula:',
            valor: ceros === 0
              ? 'ninguno — esta ACF nunca se corta'
              : `${ceros}, y ${fuera} de ellos se salen de la banda en la muestra`
          }
        ]);
      }''',
  r'''        const b = banda(r.n);
        // Rezagos donde la teoría dice exactamente cero y la muestra se sale
        // de la banda: es lo que la intro manda mirar, y con la escala fija de
        // −1 a 1 esas barras asomaban menos de un píxel. Van en rojo y con un
        // rombo, y el eje se ajusta a lo que se dibuja (±0.5 si nada pasa de
        // ahí, ±1 si no; el mismo en los dos paneles).
        //
        // Cuáles son nulos lo decide el MODELO, no el dato: la ACF de un MA(q)
        // puro después de q y la PACF de un AR(p) puro después de p. En un
        // ARMA mixto ninguna de las dos se corta, aunque el precálculo, que
        // redondea a cuatro decimales, deje en 0.0000 los últimos rezagos de
        // la PACF del ARMA(1,1) (valen 4.07e-5 y −2.03e-5).
        const corte = { ACF: p.p === 0 && p.q > 0 ? p.q : null, PACF: p.q === 0 && p.p > 0 ? p.p : null };
        const asoman = (tipo, muestral) => corte[tipo] === null ? []
          : muestral.map((v, k) => k + 1 > corte[tipo] && Math.abs(v) > b ? k + 1 : 0).filter(k => k > 0);
        const mayor = Math.max(...[p.acf_teorica, r.acf, p.pacf_teorica, r.pacf]
          .map(v => Math.max(...v.map(Math.abs))));
        const tope = mayor <= 0.5 ? 0.5 : 1;
        [gAcf, gPacf].forEach(g => {
          const eje = g.options.scales.y;
          eje.min = -tope;
          eje.max = tope;
          // Con ±1, las marcas de siempre; con ±0.5, que el ±0.5 lleve número
          eje.afterBuildTicks = tope === 1 ? marcasVerticales : e => {
            e.ticks = (e.height >= 90 ? [-0.5, -0.25, 0, 0.25, 0.5] : [-0.5, 0, 0.5]).map(v => ({ value: v }));
          };
          // Dos decimales con ±0.5: el formato de la casa escribiría «0.3» en el 0.25
          eje.ticks.callback = tope === 1 ? rotuloVertical : v => cifra(v, 2);
        });
        const fueraAcf = asoman('ACF', r.acf);
        const fueraPacf = asoman('PACF', r.pacf);
        actualizarDoble(gAcf, p.acf_teorica, r.acf, r.n, fueraAcf);
        actualizarDoble(gPacf, p.pacf_teorica, r.pacf, r.n, fueraPacf);

        const nombre = nombreProceso(p);
        const fila = (tipo, muestral, lista) => {
          const ceros = corte[tipo] === null ? 0 : muestral.length - corte[tipo];
          return {
            etiqueta: `rezagos con ${tipo} teórica nula:`,
            valor: ceros === 0
              ? `ninguno — esta ${tipo} nunca se corta`
              : `${ceros}, y ${lista.length} de ellos se salen de la banda en la muestra` +
                (lista.length ? ` (en rojo y con un rombo: ${lista.join(', ')})` : '')
          };
        };
        [[c[0], 'ACF', r.acf, fueraAcf], [c[1], 'PACF', r.pacf, fueraPacf]].forEach(([lienzo, tipo, muestral, lista]) => {
          lienzo.setAttribute('aria-label',
            descripcionCorrelograma(`${tipo} muestral`, `una realización de ${r.n} valores del ${nombre}`, muestral, b) +
            `, junto a la ${tipo} teórica` +
            (lista.length ? `; donde la teórica es cero se salen de la banda los rezagos ${lista.join(', ')}` : ''));
        });
        actualizarLectura(lectura, [
          { etiqueta: 'Proceso:', valor: nombre },
          { etiqueta: 'T =', valor: r.n },
          { etiqueta: 'banda =', valor: `±${b.toFixed(4)}` },
          fila('ACF', r.acf, fueraAcf),
          fila('PACF', r.pacf, fueraPacf)
        ]);
      }''')

# -------------------------------------------------------------------------------------
# M8 · diagnóstico
# -------------------------------------------------------------------------------------
c("JS · M8: panel de Ljung–Box en un eje de 0 a 0.10, con puntos", JS,
  r'''      const gResid = serieSimple(c[0], inicial.residuales, 'Residuales',
        COLORES_GRAFICO.gris, anios);
      const gAcf = crearGraficoBarras(c[1], REZAGOS, inicial.acf_resid, {
        etiqueta: 'ACF de los residuales', color: COLORES_GRAFICO.primario,
        lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
      });
      // El eje del p-valor va de 0 a 1 y la referencia es el nivel 0.05
      const gLb = crearGraficoBarras(c[2], inicial.ljung_box.map(f => String(f.rezago)),
        inicial.ljung_box.map(f => f.p), {
        etiqueta: 'p-valor de Ljung–Box', color: COLORES_GRAFICO.terciario,
        lineas: [{ valor: 0.05, etiqueta: 'Nivel 0.05', color: '#dc2626' }],
        tituloX: 'Rezago h', min: 0, max: 1
      });
''',
  r'''      altoEnEstrecho(c[1], 220);
      altoEnEstrecho(c[2], 250);
      const gResid = serieSimple(c[0], inicial.residuales, 'Residuales',
        COLORES_GRAFICO.gris, anios);
      const gAcf = crearGraficoBarras(c[1], REZAGOS, inicial.acf_resid, {
        etiqueta: 'ACF de los residuales', color: COLORES_GRAFICO.primario,
        lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
      });

      // Panel de Ljung–Box. Contesta una sola pregunta —¿queda el p-valor por
      // debajo de 0.05?— y con barras en un eje de 0 a 1 no la dejaba ver: el
      // 0.0461 del AR(2) caía a 0.3 px de la recta, y el AR(1), con todos sus
      // p-valores en 0.0000, salía vacío. Ahora:
      //   · el eje se amplía: va de 0 a TOPE_P = 0.10, con el 0.05 rotulado;
      //   · cada p-valor es un punto, como en tsdiag() de R, y un 0.0000 se ve
      //     sobre el eje; en rojo los que quedan bajo 0.05;
      //   · lo que pasa de 0.10 se marca con un triángulo en el borde superior
      //     y la leyenda dice que está fuera de la escala. El valor exacto
      //     sigue en el tooltip y, el del rezago 12, en la lectura.
      const NIVEL = 0.05, TOPE_P = 0.10;
      let pActuales = inicial.ljung_box.map(f => f.p);
      const partesLb = ps => [
        ps.map(v => v < NIVEL ? v : null),
        ps.map(v => v >= NIVEL && v <= TOPE_P ? v : null),
        ps.map(v => v > TOPE_P ? TOPE_P : null)
      ];
      const puntosLb = (etiqueta, color, estilo) => ({
        label: etiqueta, data: [], showLine: false, clip: false,
        borderColor: color, backgroundColor: color,
        pointStyle: estilo, pointRadius: 4, pointHoverRadius: 5
      });
      const gLb = crearGraficoLinea(c[2], inicial.ljung_box.map(f => String(f.rezago)), [
        puntosLb('p < 0.05', ROJO_GRAFICO, 'circle'),
        puntosLb('p ≥ 0.05', COLORES_GRAFICO.terciario, 'circle'),
        puntosLb('p > 0.10, fuera de la escala', COLORES_GRAFICO.terciario, 'triangle'),
        {
          label: 'Nivel 0.05', data: [], pointStyle: 'line',
          borderColor: COLORES_GRAFICO.primario, borderDash: [5, 4], borderWidth: 1.5,
          pointRadius: 0, fill: false
        }
      ], { tituloX: 'Rezago h', tituloY: 'p-valor' });
      Object.assign(gLb.options.scales.y, {
        min: 0, max: TOPE_P,
        afterBuildTicks: eje => { eje.ticks = [0, NIVEL, TOPE_P].map(v => ({ value: v })); }
      });
      gLb.options.scales.y.ticks.callback = v => v.toFixed(2);
      // El eje de rezagos, como el de los correlogramas de barras (misma
      // letra, sin el tope de 12 marcas de los gráficos de líneas): que el
      // panel no rotule menos rezagos que cuando era de barras.
      Object.assign(gLb.options.scales.x.ticks, {
        font: { family: 'Fira Code', size: 10 }, autoSkip: false, maxTicksLimit: 40
      });
      gLb.options.scales.x.afterBuildTicks =
        eje => { marcasLegibles(eje, { barras: true, aire: 0.9 }); };
      gLb.options.plugins.legend.labels.usePointStyle = true;
      gLb.options.plugins.legend.labels.boxHeight = 7;
      gLb.options.plugins.legend.labels.filter = item => item.text !== '';
      const NOMBRES_LB = gLb.data.datasets.slice(0, 3).map(ds => ds.label);
      gLb.options.plugins.tooltip.filter = item => item.datasetIndex < 3;
      gLb.options.plugins.tooltip.callbacks.label = item =>
        `p = ${pActuales[item.dataIndex].toFixed(4)}`;
''')

c("JS · M8: pintar (ACF sin el rojo que nadie explicaba, puntos de Ljung–Box, aria-label)", JS,
  r'''        gAcf.data.datasets[0].data = d.acf_resid;
        gAcf.data.datasets[0].backgroundColor =
          d.lb12_p < 0.05 ? '#dc2626' : COLORES_GRAFICO.primario;
        gAcf.data.datasets[1].data = Array(REZAGOS.length).fill(b);
        gAcf.data.datasets[2].data = Array(REZAGOS.length).fill(-b);
        gAcf.update('none');

        gLb.data.labels = d.ljung_box.map(f => String(f.rezago));
        gLb.data.datasets[0].data = d.ljung_box.map(f => f.p);
        gLb.data.datasets[1].data = Array(d.ljung_box.length).fill(0.05);
        gLb.update('none');

        const fuera = d.acf_resid.filter(r => Math.abs(r) > b).length;
        actualizarLectura(lectura, [
          { etiqueta: 'Modelo:', valor: d.etiqueta },
          { etiqueta: 'AICc / BIC:', valor: `${d.aicc.toFixed(2)} / ${d.bic.toFixed(2)}` },
          { etiqueta: 'ACF de residuales fuera de la banda:', valor: `${fuera} de ${d.acf_resid.length}` },
          {
            etiqueta: `Ljung–Box(12), fitdf = ${d.p + d.q}:`,
            valor: `p = ${d.lb12_p.toFixed(4)} ${d.lb12_p < 0.05 ? '✗ se rechaza' : '✓ no se rechaza'}`
          },''',
  r'''        // Las barras no cambian de color con el veredicto de Ljung–Box: iban
        // todas en rojo cuando la prueba rechazaba, también las que quedaban
        // dentro de la banda, y nada decía qué significaba ese rojo.
        gAcf.data.datasets[0].data = d.acf_resid;
        gAcf.data.datasets[1].data = Array(REZAGOS.length).fill(b);
        gAcf.data.datasets[2].data = Array(REZAGOS.length).fill(-b);
        gAcf.update('none');

        pActuales = d.ljung_box.map(f => f.p);
        gLb.data.labels = d.ljung_box.map(f => String(f.rezago));
        partesLb(pActuales).forEach((datos, k) => {
          gLb.data.datasets[k].data = datos;
          // Un conjunto sin puntos no sale en la leyenda
          gLb.data.datasets[k].label = datos.every(v => v === null) ? '' : NOMBRES_LB[k];
        });
        gLb.data.datasets[3].data = Array(pActuales.length).fill(NIVEL);
        gLb.update('none');

        const fuera = d.acf_resid.filter(r => Math.abs(r) > b).length;
        const bajoNivel = pActuales.filter(v => v < NIVEL).length;
        const h0 = d.ljung_box[0].rezago, h1 = d.ljung_box[d.ljung_box.length - 1].rezago;
        c[0].setAttribute('aria-label', `Residuales del ${d.etiqueta} ajustado a las manchas solares`);
        c[1].setAttribute('aria-label',
          descripcionCorrelograma('ACF', `los residuales del ${d.etiqueta}`, d.acf_resid, b));
        c[2].setAttribute('aria-label',
          `p-valores de Ljung–Box de los residuales del ${d.etiqueta}, rezagos ${h0} a ${h1}, en un eje de 0 a ` +
          `${TOPE_P.toFixed(2)}: ${bajoNivel} de ${pActuales.length} por debajo de ${NIVEL.toFixed(2)}; ` +
          `en el rezago 12, p = ${d.lb12_p.toFixed(4)}`);
        actualizarLectura(lectura, [
          { etiqueta: 'Modelo:', valor: d.etiqueta },
          { etiqueta: 'AICc / BIC:', valor: `${d.aicc.toFixed(2)} / ${d.bic.toFixed(2)}` },
          { etiqueta: 'ACF de residuales fuera de la banda:', valor: `${fuera} de ${d.acf_resid.length}` },
          {
            etiqueta: `Ljung–Box(12), fitdf = ${d.p + d.q}:`,
            valor: `p = ${d.lb12_p.toFixed(4)} ${d.lb12_p < 0.05 ? '✗ se rechaza' : '✓ no se rechaza'}`
          },
          {
            etiqueta: `p-valores de Ljung–Box bajo ${NIVEL.toFixed(2)} (rezagos ${h0} a ${h1}):`,
            valor: `${bajoNivel} de ${pActuales.length}`
          },''')

c("JS · M8: textos del selector que caben en el teléfono", JS,
  r'''          { valor: 'arma10', texto: 'AR(1) — claramente insuficiente' },
          { valor: 'arma20', texto: 'AR(2) — el que propone la identificación' },
          { valor: 'arma30', texto: 'AR(3)' },
          { valor: 'arma21', texto: 'ARMA(2,1) — mejor AICc sobre la serie cruda' }''',
  r'''          { valor: 'arma10', texto: 'AR(1) — insuficiente' },
          { valor: 'arma20', texto: 'AR(2) — el de la identificación' },
          { valor: 'arma30', texto: 'AR(3)' },
          { valor: 'arma21', texto: 'ARMA(2,1) — el de menor AICc' }''')

# -------------------------------------------------------------------------------------
# M9 · transformada e impulso
# -------------------------------------------------------------------------------------
c("JS · M9 transformada: aria-label con la escala", JS,
  r'''        gPacf.data.datasets[0].data = esRaiz ? TRANSF.sqrt.pacf : MANCHAS.pacf;
        gPacf.data.datasets[0].backgroundColor = color;
        gPacf.update('none');
''',
  r'''        gPacf.data.datasets[0].data = esRaiz ? TRANSF.sqrt.pacf : MANCHAS.pacf;
        gPacf.data.datasets[0].backgroundColor = color;
        gPacf.update('none');
        const serie = esRaiz ? 'la raíz cuadrada de las manchas solares' : 'las manchas solares en su escala original';
        c[0].setAttribute('aria-label', `Serie anual de ${serie}, ${MANCHAS.n} observaciones`);
        c[1].setAttribute('aria-label', descripcionCorrelograma('PACF', serie,
          esRaiz ? TRANSF.sqrt.pacf : MANCHAS.pacf, banda(MANCHAS.n)));
''')

c("JS · M9 impulso: alto en estrecho", JS,
  r'''      const gPsi = crearGraficoBarras(c[0], etiquetas, psi, {
        etiqueta: 'ψⱼ', color: COLORES_GRAFICO.primario, tituloX: 'j (años desde el choque)'
      });''',
  r'''      altoEnEstrecho(c[0], 240);
      altoEnEstrecho(c[1], 240);
      const gPsi = crearGraficoBarras(c[0], etiquetas, psi, {
        etiqueta: 'ψⱼ', color: COLORES_GRAFICO.primario, tituloX: 'j (años desde el choque)'
      });''')

c("JS · M9 impulso: la barra del horizonte no va en el color del techo; aria-label", JS,
  r'''        gAbanico.data.datasets[0].backgroundColor = horizontes.map(
          (_, k) => k + 1 === h ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.terciario);
        gAbanico.update('none');

        const ee = Math.sqrt(sigma2 * sumaHasta(h));''',
  r'''        // La barra del horizonte elegido va en el color oscuro: en naranja se
        // confundía con la recta del techo.
        gAbanico.data.datasets[0].backgroundColor = horizontes.map(
          (_, k) => k + 1 === h ? COLORES_GRAFICO.primario : COLORES_GRAFICO.terciario);
        gAbanico.update('none');

        const ee = Math.sqrt(sigma2 * sumaHasta(h));
        c[0].setAttribute('aria-label', describirBarras(
          'Pesos ψ del AR(2) ajustado a la raíz de las manchas solares, j de', psi, 0) +
          `, dentro del envolvente ±${factor.toFixed(2)} × ${R.toFixed(4)}ʲ; en color oscuro, ` +
          `${h === 1 ? 'el único que entra' : `los ${h} que entran`} en la varianza del pronóstico a ` +
          `${h} ${h === 1 ? 'año' : 'años'}`);
        c[1].setAttribute('aria-label',
          `Semiancho del intervalo de pronóstico del 95 % para horizontes de 1 a ${H} años: ` +
          `±${(z * ee).toFixed(2)} a ${h} ${h === 1 ? 'año' : 'años'}, destacado, frente a un techo de ±${semiTecho.toFixed(2)}`);''')

# -------------------------------------------------------------------------------------
# Quiz: descripciones que no responden; el segundo gráfico, sin el rojo
# -------------------------------------------------------------------------------------
c("JS · quiz P3: el aria-label da las barras, no el corte", JS,
  r'''        descripcionGrafico: 'Función de autocorrelación teórica que vale 0.5526 y 0.2632 y después es exactamente cero',''',
  r'''        descripcionGrafico: describirBarrasQuiz('Función de autocorrelación teórica de un proceso',
          PROCESOS.ma2.acf_teorica),''')

c("JS · quiz P9: el aria-label da las barras y la banda, no el veredicto", JS,
  r'''        descripcionGrafico: 'ACF de los residuales de un AR(1) ajustado a las manchas solares, con varias barras muy fuera de la banda',''',
  r'''        descripcionGrafico: describirBarrasQuiz(
          'Función de autocorrelación de los residuales de un AR(1) ajustado a las manchas solares',
          MANCHAS.diagnosticos.arma10.acf_resid, banda(MANCHAS.n)),''')

c("JS · quiz P9: barras en el color de siempre, no en rojo", JS,
  r'''          etiqueta: 'ACF de los residuales', color: '#dc2626',
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        }),''',
  r'''          etiqueta: 'ACF de los residuales', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        }),''')


# =====================================================================================
# cap3_modulos.html
# =====================================================================================
c("MOD · M2: la PACF cae a cero después del rezago p", MOD,
  r'''          simuladas— de cuatro procesos autorregresivos. Fíjate en que la PACF cae a cero de golpe en el rezago $p$
          y se queda ahí, mientras la ACF nunca termina de cortarse.</p>''',
  r'''          simuladas— de cuatro procesos autorregresivos. Fíjate en que la PACF cae a cero de golpe después del
          rezago $p$ —la barra de $p$ es la última distinta de cero— y se queda ahí, mientras la ACF nunca termina
          de cortarse.</p>''')

c("MOD · M2: aria-label del triángulo sin ASCII", MOD,
  r'''<canvas aria-label="Triángulo de estacionariedad del AR(2) con el punto (phi1, phi2) marcado" role="img"></canvas>''',
  r'''<canvas aria-label="Triángulo de estacionariedad del AR(2) con el punto (φ₁, φ₂) marcado" role="img"></canvas>''')

c("MOD · M4: la frontera no crece", MOD,
  r'''        <p><strong>Lo que acabas de ver con $|\theta| > 1$.</strong> Los pesos $\pi$ crecen sin límite en vez de
          desvanecerse. Eso significa''',
  r'''        <p><strong>Lo que acabas de ver con $|\theta| > 1$.</strong> Los pesos $\pi$ crecen sin límite en vez de
          desvanecerse (en la frontera, $|\theta| = 1$, ni crecen ni se desvanecen: conservan su magnitud, y el
          proceso tampoco es invertible). Cuando el mayor pasa de 20 en valor absoluto, el simulador los dibuja en
          un eje logarítmico, que deja ver los doce a la vez. Eso significa''')

c("MOD · M5: las barras de la muestral ya no son «claras»", MOD,
  r'''          sólidas) con la <strong>muestral</strong> de una realización de longitud $T$ (barras claras). Cambia $T$ y''',
  r'''          oscuras) con la <strong>muestral</strong> de una realización de longitud $T$ (barras grises). Cambia $T$ y''')

c("MOD · M6: las barras que se asoman, en rojo", MOD,
  r'''          dice <strong>exactamente cero</strong>: la muestra pone ahí valores pequeños pero no nulos, y alguno se
          asoma fuera de la banda. Eso, y no otra cosa, es lo que ves en un correlograma real.</p>''',
  r'''          dice <strong>exactamente cero</strong>: la muestra pone ahí valores pequeños pero no nulos, y alguno se
          asoma fuera de la banda (va en rojo y con un rombo, y la lectura dice en qué rezago). Eso, y no otra
          cosa, es lo que ves en un correlograma real.</p>''')

c("MOD · M8: el panel de Ljung–Box dice qué eje tiene", MOD,
  r'''        <p class="grafico-etiqueta">$p$-valor de Ljung–Box por rezago</p>
        <div class="grafico-wrapper" style="height:180px;">
          <canvas aria-label="p-valor de la prueba de Ljung-Box acumulada por rezago" role="img"></canvas>''',
  r'''        <p class="grafico-etiqueta">$p$-valor de Ljung–Box por rezago (eje ampliado: de $0$ a $0.10$)</p>
        <div class="grafico-wrapper" style="height:230px;">
          <canvas aria-label="p-valor de la prueba de Ljung-Box acumulada por rezago" role="img"></canvas>''')

c("MOD · M8: algo más de alto para la ACF de los residuales", MOD,
  r'''        <p class="grafico-etiqueta">ACF de los residuales</p>
        <div class="grafico-wrapper" style="height:180px;">''',
  r'''        <p class="grafico-etiqueta">ACF de los residuales</p>
        <div class="grafico-wrapper" style="height:200px;">''')

c("MOD · M4: más alto para el panel de los π (caben las marcas de cada década)", MOD,
  r'''        <div class="grafico-wrapper" style="height:190px;">
          <canvas aria-label="Pesos pi de la representación autorregresiva infinita" role="img"></canvas>''',
  r'''        <div class="grafico-wrapper" style="height:250px;">
          <canvas aria-label="Pesos pi de la representación autorregresiva infinita" role="img"></canvas>''')


# =====================================================================================
def base(archivo, rev):
    return subprocess.run(["git", "show", f"{rev}:{archivo}"], cwd=RAIZ, capture_output=True,
                          text=True, check=True).stdout


def main():
    rev = "HEAD"
    if "--base" in sys.argv:
        rev = sys.argv[sys.argv.index("--base") + 1]
    comprobar = "--comprobar" in sys.argv
    archivos = (C2, MOD, JS)
    textos = {a: base(a, rev) for a in archivos}
    fallos = 0
    for clave, archivo, antes, despues in C:
        n = textos[archivo].count(antes)
        if n != 1:
            print(f"FALLA · {clave}: el texto original aparece {n} veces en {archivo} (se esperaba 1)")
            fallos += 1
            continue
        textos[archivo] = textos[archivo].replace(antes, despues)
    for clave, archivo, inicio, fin, destino in MOVER:
        t = textos[archivo]
        cuenta = [t.count(m) for m in (inicio, fin, destino)]
        if cuenta != [1, 1, 1]:
            print(f"FALLA · {clave}: los marcadores aparecen {cuenta} veces en {archivo} (se esperaba 1, 1, 1)")
            fallos += 1
            continue
        i, j = t.index(inicio), t.index(fin)
        if not i < j:
            print(f"FALLA · {clave}: los marcadores están en orden inverso")
            fallos += 1
            continue
        bloque = t[i:j]
        t = t[:i] + t[j:]
        k = t.index(destino)
        textos[archivo] = t[:k] + bloque + t[k:]
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
    print(f"{len(C)} sustituciones y {len(MOVER)} traslados sobre {rev}: "
          + ", ".join(f"{sum(1 for x in C if x[1] == a) + sum(1 for x in MOVER if x[1] == a)} en {a.split('/')[-1]}"
                      for a in archivos))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()

