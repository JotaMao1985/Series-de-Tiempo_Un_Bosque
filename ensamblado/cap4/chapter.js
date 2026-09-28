    // ================================================================
    // Datos y ayudantes del capítulo, tomados del precálculo en R
    // ================================================================
    const NILO = DATOS_CAP4.nilo;
    const TRM = DATOS_CAP4.trm;
    const PUENTE = DATOS_CAP4.puente_estacional;
    const REJILLA = NILO.rejilla;
    const HK = NILO.hyndman_khandakar;
    const REZAGOS = etiquetasRezago(DATOS_CAP4.max_rezago);

    function banda(n) { return 1.96 / Math.sqrt(n); }

    function lineasBanda(n) {
      const b = banda(n);
      return [
        { valor: b, etiqueta: 'Banda ±1.96/√n' },
        { valor: -b, etiqueta: '' }
      ];
    }

    // Etiquetas de año para una serie anual que empieza en `inicio` y a la que
    // se le han quitado `perdidas` observaciones por diferenciar.
    function aniosDesde(inicio, n, perdidas = 0) {
      return Array.from({ length: n }, (_, i) => String(inicio + perdidas + i));
    }

    // Etiquetas mensuales AAAA-MM para la TRM. `mes` puede pasar de 12 (el
    // abanico arranca en el mes 1 + 90 de la serie): se normaliza a la entrada,
    // o las etiquetas saldrían «2015-91» y todo el eje correría siete años.
    function mesesDesde(anio, mes, n) {
      const salida = [];
      let a = anio + Math.floor((mes - 1) / 12), m = ((mes - 1) % 12) + 1;
      for (let i = 0; i < n; i++) {
        salida.push(`${a}-${String(m).padStart(2, '0')}`);
        m += 1;
        if (m > 12) { m = 1; a += 1; }
      }
      return salida;
    }

    // Diferenciación en JS, para las series que se dibujan sin precalcular.
    function diferenciarVeces(y, d) {
      let x = y.slice();
      for (let k = 0; k < d; k++) {
        const z = [];
        for (let i = 1; i < x.length; i++) z.push(x[i] - x[i - 1]);
        x = z;
      }
      return x;
    }

    function media(x) { return x.reduce((a, b) => a + b, 0) / x.length; }

    function varianzaDe(x) {
      const m = media(x);
      return x.reduce((a, b) => a + (b - m) * (b - m), 0) / (x.length - 1);
    }

    // Devuelve un guion cuando el valor no es un numero finito. Hace falta:
    // jsonlite escribe los AICc infinitos de la traza de auto.arima como null,
    // y Number(null) es 0, que en pantalla se leeria como un AICc de 0.000.
    //
    // Punto decimal, como la prosa del capítulo. Los miles se agrupan con un
    // espacio fino solo desde cinco cifras enteras (80 055.01); con cuatro van
    // juntos (1267.51), como los escribe el texto. Con coma de miles, un
    // intervalo de la TRM se leía «[3,797.12, 4,213.40]».
    function fmt(x, d = 2) {
      if (x === null || x === undefined || !Number.isFinite(Number(x))) return '—';
      return agrupaMiles(Number(x).toLocaleString('en-US', {
        minimumFractionDigits: d, maximumFractionDigits: d
      }));
    }

    // Convierte los miles de una cifra ya formateada en en-US («28,637.95»)
    // a la convención de fmt(). Solo toca comas entre dígitos seguidas de
    // grupos de tres, así que «ARIMA(1,1,1)» o «(3, 5)» pasan intactos.
    function agrupaMiles(s) {
      return String(s).replace(/\d{1,3}(?:,\d{3})+/g,
        m => m.replace(/,/g, m.replace(/,/g, '').length >= 5 ? '\u202F' : ''));
    }

    // Los ejes y los tooltips de Chart.js formatean con el idioma del
    // navegador: «1,400» en uno en inglés y «1.400» en uno en español, que es
    // mil cuatrocientos o uno coma cuatro según quién lo lea. Se fija en-US y
    // se pasa por agrupaMiles(), para que digan lo mismo que las lecturas.
    Chart.defaults.locale = 'en-US';
    (function () {
      const tickLineal = Chart.defaults.scales.linear.ticks.callback;
      Chart.defaults.scales.linear.ticks.callback = function (valor, i, ticks) {
        return agrupaMiles(tickLineal.call(this, valor, i, ticks));
      };
      const cb = Chart.defaults.plugins.tooltip.callbacks;
      const etiqueta = cb.label, titulo = cb.title;
      cb.label = function (item) {
        return etiqueta.call(this, Object.assign({}, item,
          { formattedValue: agrupaMiles(item.formattedValue) }));
      };
      cb.title = function (items) {
        return titulo.call(this, items.map(it =>
          Object.assign({}, it, { label: agrupaMiles(it.label) })));
      };
    })();

    // Varios simuladores de este capítulo DESTRUYEN y vuelven a crear sus
    // gráficos al repintar (el de pronóstico, por ejemplo, cambia el número de
    // series según se pidan bandas o no). `graficosActivos` guarda referencias
    // fijas, así que devolver el objeto Chart inicial dejaría una referencia
    // obsoleta y `destruirSimuladores()` liberaría el gráfico equivocado.
    // Este manejador devuelve un objeto estable que destruye el gráfico VIGENTE.
    function manejador(dame) {
      return { destroy() { const g = dame(); if (g) g.destroy(); } };
    }

    // Un gráfico de línea sencillo, reutilizado por varios simuladores.
    function lineaSimple(canvas, etiquetas, valores, etiqueta, color, opciones = {}) {
      return crearGraficoLinea(canvas, etiquetas, [{
        label: etiqueta,
        data: valores,
        borderColor: color || COLORES_GRAFICO.primario,
        backgroundColor: color || COLORES_GRAFICO.primario,
        borderWidth: 1.8,
        pointRadius: 0
      }], opciones);
    }

    // Escalas completas de un gráfico de línea con título en el eje y.
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
    }

    // Título del eje y de un gráfico ya creado (crearGraficoBarras no lo admite).
    function tituloEjeY(grafico, texto) {
      grafico.options.scales.y.title = {
        display: true, text: texto, font: { family: 'Montserrat', size: 11 }
      };
      grafico.update('none');
    }

    // En un teléfono los lienzos miden unos 240 px de ancho y la leyenda de
    // escritorio se come el gráfico: en el M3, las cinco entradas de la tasa
    // ocupaban cuatro filas y dejaban ~40 px a las curvas; en el M4, las dos de
    // la ACF ocupaban dos filas y dejaban 56 px a las barras. Por debajo de
    // 420 px la leyenda se compacta y, si se le pasan `altos`, el marco crece;
    // onResize lo reajusta si cambia el ancho.
    const ESTRECHO = 420;
    function compactar(grafico, ancho, altos) {
      const chico = ancho < ESTRECHO;
      Object.assign(grafico.options.plugins.legend.labels, {
        font: { family: 'Montserrat', size: chico ? 10 : 12 },
        boxWidth: chico ? 12 : 24,
        padding: chico ? 6 : 10
      });
      if (altos) grafico.canvas.parentNode.style.height = chico ? altos.estrecho : altos.ancho;
    }

    // Lo mismo para un gráfico de barras (M4, M6): crearGraficoBarras no
    // admite onResize, así que se le añade ya creado.
    function barrasCompactas(g, altos) {
      g.options.onResize = (gr, t) => compactar(gr, t.width, altos);
      compactar(g, g.width, altos);
      g.update('none');
      return g;
    }

    // ∇, ∇², ∇³: el orden como exponente, igual que en la prosa.
    function nabla(d) { return ['', '∇', '∇²', '∇³'][d]; }

    const UNIDAD_NILO = '10⁸ m³';

    // ================================================================
    // Módulo 1 · La serie del Nilo y sus diferencias
    // ================================================================
    SIMULADORES['nilo-y-diferencia'] = function (raiz) {
      const serie = SERIES_CAP4.nilo.valores;
      const inicio = SERIES_CAP4.nilo.inicio[0];
      const params = { d: '0' };
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const d = parseInt(params.d, 10);
        const y = diferenciarVeces(serie, d);
        const etiquetas = aniosDesde(inicio, y.length, d);
        const titulo = d === 0 ? 'Caudal del Nilo' : `${nabla(d)} caudal del Nilo`;
        if (grafico) grafico.destroy();
        grafico = lineaSimple(canvas, etiquetas, y, titulo,
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario,
          { scales: escalasLinea(d === 0 ? `Caudal (${UNIDAD_NILO})` : `Diferencia (${UNIDAD_NILO})`) });
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'media', valor: fmt(media(y)) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) },
          { etiqueta: 'ρ̂₁', valor: fmt(calcularACF(y, 1)[0], 4) }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'd', etiqueta: 'Orden de diferenciación d',
        opciones: [
          { valor: '0', texto: 'd = 0 — la serie original' },
          { valor: '1', texto: 'd = 1 — primera diferencia' },
          { valor: '2', texto: 'd = 2 — segunda diferencia' }
        ]
      }, params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 3 · Un escalón disfrazado de raíz unitaria
    // ================================================================
    SIMULADORES['escalon-vs-raiz'] = function (raiz) {
      const malla = NILO.cambio_nivel.malla_delta;
      const puntos = malla.puntos;
      const betas = puntos.map(p => p.delta);
      const params = { beta: 100 };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cSerie, cCurva] = raiz.querySelectorAll('canvas');
      let gSerie = null, gCurva = null;

      // Ruido con semilla fija: la realización no cambia al mover el deslizador,
      // así que lo único que se mueve en el gráfico es el escalón.
      const ruido = generarRuidoNormal(malla.n, 20260726).map(z => 1000 + malla.sigma * z);
      const etiquetas = aniosDesde(1871, malla.n, 0);

      // Interpolación lineal sobre la malla precalculada en R.
      function interpolar(beta, campo) {
        if (beta <= betas[0]) return puntos[0][campo];
        for (let i = 1; i < betas.length; i++) {
          if (beta <= betas[i]) {
            const t = (beta - betas[i - 1]) / (betas[i] - betas[i - 1]);
            return puntos[i - 1][campo] + t * (puntos[i][campo] - puntos[i - 1][campo]);
          }
        }
        return puntos[puntos.length - 1][campo];
      }

      // La malla no es uniforme (0, 25, …, 100, 150, …, 300): el eje x tiene
      // que ser numérico, o el tramo 100→150 ocuparía lo mismo que 0→25.
      const curva = campo => puntos.map(p => ({ x: p.delta, y: 100 * p[campo] }));

      // El marco de la tasa crece en el teléfono (véase compactar, arriba).
      const ALTOS_CURVA = { estrecho: '280px', ancho: '200px' };

      function pintar() {
        const b = params.beta;
        const y = ruido.map((v, i) => v - (i + 1 >= malla.posicion ? b : 0));
        if (gSerie) gSerie.destroy();
        // El rótulo de encima ya dice «ruido blanco + escalón»: la leyenda solo
        // nombra el descenso, y así cabe en un teléfono.
        gSerie = lineaSimple(cSerie, etiquetas, y,
          b === 0 ? 'Sin escalón' : `Descenso de ${fmt(b, 0)} en 1899`,
          COLORES_GRAFICO.primario, {
            scales: escalasLinea('Nivel simulado'),
            onResize: (g, t) => compactar(g, t.width)
          });
        compactar(gSerie, gSerie.width);
        gSerie.update('none');

        const tasa = interpolar(b, 'kpss_rechaza');
        const tasa12 = interpolar(b, 'kpss_rechaza_l12');
        if (!gCurva) {
          gCurva = crearGraficoLinea(cCurva, [], [
            {
              label: 'KPSS con ℓ = 4 (R)',
              data: curva('kpss_rechaza'),
              borderColor: COLORES_GRAFICO.secundario,
              backgroundColor: 'rgba(255, 102, 0, 0.12)',
              borderWidth: 2, pointRadius: 3, fill: true
            },
            {
              label: 'KPSS con ℓ = 12',
              data: curva('kpss_rechaza_l12'),
              borderColor: COLORES_GRAFICO.terciario,
              borderWidth: 1.8, pointRadius: 2, fill: false
            },
            {
              label: 'Nivel nominal 5 %',
              data: [{ x: 0, y: 5 }, { x: 300, y: 5 }],
              borderColor: COLORES_GRAFICO.gris,
              borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, fill: false
            },
            {
              label: 'β elegido',
              data: [],
              borderColor: COLORES_GRAFICO.primario,
              backgroundColor: COLORES_GRAFICO.primario,
              pointRadius: 6, pointHoverRadius: 7, showLine: false
            },
            {
              label: `Nilo (${fmt(malla.delta_del_nilo, 1)})`,
              data: [{ x: malla.delta_del_nilo, y: 0 }, { x: malla.delta_del_nilo, y: 100 }],
              borderColor: COLORES_GRAFICO.primario,
              borderDash: [2, 3], borderWidth: 1.5, pointRadius: 0, pointHitRadius: 0, fill: false
            }
          ], {
            scales: {
              x: { type: 'linear', min: 0, max: 300,
                   title: { display: true, text: 'Tamaño del descenso |β|' },
                   ticks: { font: { family: 'Fira Code', size: 10 }, stepSize: 50 },
                   grid: { display: false } },
              y: { min: 0, max: 100,
                   title: { display: true, text: '% de réplicas que rechazan',
                            font: { family: 'Montserrat', size: 11 } },
                   ticks: { font: { family: 'Fira Code', size: 11 },
                            callback: v => v + ' %' } }
            },
            onResize: (g, t) => compactar(g, t.width, ALTOS_CURVA)
          });
          compactar(gCurva, gCurva.width, ALTOS_CURVA);
          // La línea del Nilo es una referencia, no una tasa: con la interacción
          // por índice, sus dos puntos (0 y 100) saldrían en el tooltip junto a
          // los de las curvas.
          gCurva.options.plugins.tooltip.filter = item => item.datasetIndex !== 4;
        }
        // El β elegido se marca sobre la curva de R, en su valor interpolado.
        gCurva.data.datasets[3].data = [{ x: b, y: 100 * tasa }];
        gCurva.update('none');

        actualizarLectura(lectura, [
          { etiqueta: 'descenso |β|', valor: b === 0 ? 'sin escalón' : fmt(b, 0) },
          { etiqueta: 'en desv. típicas', valor: fmt(b / malla.sigma, 2) },
          { etiqueta: 'KPSS medio', valor: fmt(interpolar(b, 'kpss_medio'), 3) },
          { etiqueta: 'rechaza (ℓ = 4)', valor: `${fmt(100 * tasa, 1)} %` },
          { etiqueta: 'rechaza (ℓ = 12)', valor: `${fmt(100 * tasa12, 1)} %` },
          { etiqueta: 'ndiffs medio', valor: fmt(interpolar(b, 'ndiffs_medio'), 2) }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'beta', etiqueta: 'Tamaño del descenso |β| ', min: 0, max: 300, paso: 5, decimales: 0 }
      ], params, pintar);

      pintar();
      return [manejador(() => gSerie), manejador(() => gCurva)];
    };

    // ================================================================
    // Módulo 4 · Identificación sobre el Nilo
    // ================================================================
    SIMULADORES['identificacion-nilo'] = function (raiz) {
      const ident = NILO.identificacion;
      const claves = { '0': 'cruda', '1': 'd1', '2': 'd2' };
      const params = { d: '1' };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cSerie, cAcf, cPacf] = raiz.querySelectorAll('canvas');
      let gSerie = null, gAcf = null, gPacf = null;

      // La ACF y la PACF crecen en el teléfono (véase compactar, arriba).
      const ALTOS_BARRAS = { estrecho: '240px', ancho: '180px' };

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = ident[claves[params.d]];
        const y = diferenciarVeces(SERIES_CAP4.nilo.valores, d);
        [gSerie, gAcf, gPacf].forEach(g => { if (g) g.destroy(); });
        gSerie = lineaSimple(cSerie, aniosDesde(SERIES_CAP4.nilo.inicio[0], y.length, d), y,
          `${nabla(d)}Nilo`,
          d === 1 ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.primario,
          { scales: escalasLinea(d === 0 ? UNIDAD_NILO : `Diferencia (${UNIDAD_NILO})`) });
        gAcf = barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS);
        gPacf = barrasCompactas(crearGraficoBarras(cPacf, REZAGOS, info.pacf, {
          etiqueta: 'PACF muestral', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS);
        // Contar solo la ACF no distingue d = 1 de d = 2 (2 de 20 en ambos); la
        // PACF sí (4 frente a 7), y en d = 0 su «1 de 20» es la trampa del AR(1).
        const fuera = r => `${r.filter(v => Math.abs(v) > info.banda).length} de ${r.length}`;
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'banda', valor: `±${fmt(info.banda, 4)}` },
          { etiqueta: 'ρ̂₁', valor: fmt(info.acf[0], 4) },
          { etiqueta: 'ACF fuera de banda', valor: fuera(info.acf) },
          { etiqueta: 'PACF fuera de banda', valor: fuera(info.pacf) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'd', etiqueta: 'Serie sobre la que se lee',
        opciones: [
          { valor: '0', texto: 'd = 0 — sin diferenciar' },
          { valor: '1', texto: 'd = 1 — ∇Nilo (la de trabajo)' },
          { valor: '2', texto: 'd = 2 — ∇²Nilo (una de más)' }
        ]
      }, params, pintar);

      pintar();
      return [manejador(() => gSerie), manejador(() => gAcf), manejador(() => gPacf)];
    };

    // ================================================================
    // Módulo 6 · Explorador de la rejilla ARIMA(p,d,q)
    // ================================================================
    SIMULADORES['explorador-modelos'] = function (raiz) {
      const params = { p: 1, d: 1, q: 1 };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cAcf, cAicc] = raiz.querySelectorAll('canvas');
      let gAcf = null, gAicc = null;

      // Los dos gráficos crecen en el teléfono (véase compactar, arriba).
      const ALTOS_RESIDUALES = { estrecho: '250px', ancho: '210px' };
      const ALTOS_AICC = { estrecho: '240px', ancho: '200px' };

      function pintar() {
        const clave = `${params.p}${params.d}${params.q}`;
        const m = REJILLA[clave];
        const mejor = NILO.mejor_por_d[`d${params.d}`];
        // Ordenados por p y luego por q, para que la rejilla se lea en orden.
        const hermanos = Object.values(REJILLA)
          .filter(x => x.d === params.d && x.convergio)
          .sort((a, b) => a.p - b.p || a.q - b.q);

        [gAcf, gAicc].forEach(g => { if (g) g.destroy(); });

        if (!m || !m.convergio) {
          gAcf = crearGraficoBarras(cAcf, REZAGOS, REZAGOS.map(() => 0), {
            etiqueta: 'sin ajuste', color: COLORES_GRAFICO.gris, tituloX: 'Rezago k'
          });
          gAicc = crearGraficoBarras(cAicc, hermanos.map(x => x.etiqueta.slice(6, -1)),
            hermanos.map(x => x.aicc), { etiqueta: 'AICc', color: COLORES_GRAFICO.gris });
          actualizarLectura(lectura, [{ etiqueta: 'Modelo', valor: `ARIMA(${params.p},${params.d},${params.q}) no converge` }]);
          return;
        }

        const nEf = m.n_efectivo;
        gAcf = barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, m.acf_residuales, {
          etiqueta: 'ACF de los residuales',
          color: m.ljung_box_p > 0.05 ? COLORES_GRAFICO.primario : '#b91c1c',
          lineas: lineasBanda(nEf), tituloX: 'Rezago k'
        }), ALTOS_RESIDUALES);

        const esteEs = clave;
        // Con d = 2 el ARIMA(0,2,0) queda a +121 y aplastaría las diferencias
        // de uno o dos puntos, que son las que importan: el eje se corta en 20
        // y la barra recortada lleva su valor en la etiqueta.
        const TOPE = 20;
        const deltas = hermanos.map(x => x.aicc - mejor.valor_aicc);
        const maxEje = Math.min(TOPE, Math.max(6, ...deltas));
        gAicc = crearGraficoBarras(cAicc,
          hermanos.map((x, i) => `(${x.p},${x.d},${x.q})${deltas[i] > TOPE ? ` ↑${fmt(deltas[i], 0)}` : ''}`),
          deltas.map(v => Math.min(v, TOPE)), {
            etiqueta: `ΔAICc sobre el mejor de d = ${params.d}`,
            color: COLORES_GRAFICO.gris,
            min: 0, max: maxEje
          });
        // En un teléfono los nueve rótulos no caben bajo las barras y Chart.js
        // se saltaba siete, el tope incluido; inclinados, los de dos líneas
        // chocaban. Por debajo de ESTRECHO las barras se tumban y los rótulos
        // pasan al eje vertical, donde caben enteros. Si el ancho cruza el
        // umbral (al girar el teléfono), se repinta con la otra orientación.
        const tumbado = gAicc.width < ESTRECHO;
        if (tumbado) {
          gAicc.options.indexAxis = 'y';
          gAicc.options.scales = {
            x: { suggestedMin: 0, suggestedMax: maxEje,
                 title: { display: true, text: 'ΔAICc', font: { family: 'Montserrat', size: 11 } },
                 ticks: { font: { family: 'Fira Code', size: 10 } },
                 grid: { color: 'rgba(148, 163, 184, 0.2)' } },
            y: { ticks: { font: { family: 'Fira Code', size: 10 }, autoSkip: false },
                 grid: { display: false } }
          };
        }
        gAicc.options.onResize = (g, t) => {
          compactar(g, t.width, ALTOS_AICC);
          if ((t.width < ESTRECHO) !== tumbado) setTimeout(pintar);
        };
        compactar(gAicc, gAicc.width, ALTOS_AICC);
        // El tooltip nombra el modelo y da el ΔAICc real: la barra del (0,2,0)
        // mide 20 pero el modelo está a +121.
        Object.assign(gAicc.options.plugins.tooltip.callbacks, {
          title: items => hermanos[items[0].dataIndex].etiqueta,
          label: item => `ΔAICc: +${fmt(deltas[item.dataIndex])}`
        });
        // Naranja el seleccionado, verde oscuro el mejor de su d. El mejor está
        // en 0 por definición: minBarLength le da una barra visible.
        gAicc.data.datasets[0].backgroundColor = hermanos.map((x, i) =>
          `${x.p}${x.d}${x.q}` === esteEs ? COLORES_GRAFICO.secundario
            : deltas[i] === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.gris);
        gAicc.data.datasets[0].minBarLength = 3;
        if (tumbado) gAicc.update('none');
        else tituloEjeY(gAicc, 'ΔAICc');

        const campos = [
          { etiqueta: 'Modelo', valor: m.etiqueta },
          { etiqueta: 'n efectivo', valor: `${nEf} (= 100 − ${params.d})` },
          { etiqueta: 'AICc', valor: fmt(m.aicc) },
          { etiqueta: 'BIC', valor: fmt(m.bic) },
          { etiqueta: 'Ljung–Box(20)', valor: `p = ${fmt(m.ljung_box_p, 4)}` },
          { etiqueta: `mejor AICc de d = ${params.d}`, valor: fmt(mejor.valor_aicc) },
          { etiqueta: 'diferencia', valor: `+${fmt(m.aicc - mejor.valor_aicc)}` }
        ];
        // Las raíces van siempre, no solo cuando caen sobre el círculo: la que lo
        // roza es la que cuenta el d del Nilo (AR en 1.161 con d = 0, MA en 1.144
        // con d = 1, MA en 1.032 en el mínimo de d = 2, que parecía impecable).
        const r = m.raices || {};
        campos.push(
          { etiqueta: '|raíz AR| mín.', valor: r.min_ar == null ? '— (sin AR)' : fmt(r.min_ar, 3) },
          r.degenerado
            ? { etiqueta: '⚠ |raíz MA| mín.', valor: `${fmt(r.min_ma, 3)}, sobre el círculo` }
            : { etiqueta: '|raíz MA| mín.', valor: r.min_ma == null ? '— (sin MA)' : fmt(r.min_ma, 3) }
        );
        actualizarLectura(lectura, campos);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'p', etiqueta: 'Orden autorregresivo p ', min: 0, max: 2, paso: 1, decimales: 0 },
        { clave: 'd', etiqueta: 'Orden de diferenciación d ', min: 0, max: 2, paso: 1, decimales: 0 },
        { clave: 'q', etiqueta: 'Orden de medias móviles q ', min: 0, max: 2, paso: 1, decimales: 0 }
      ], params, pintar);

      pintar();
      return [manejador(() => gAcf), manejador(() => gAicc)];
    };

    // ================================================================
    // Módulo 7 · La traza de auto.arima, paso a paso
    // ================================================================
    SIMULADORES['traza-auto-arima'] = function (raiz) {
      const params = { paso: 1, exhaustiva: false };
      const lectura = raiz.querySelector('.simulador-lectura');
      const lista = raiz.querySelector('[data-lista-traza]');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;
      let inputPaso = null;

      function pasosActuales() {
        return params.exhaustiva ? HK.exhaustiva.pasos : HK.escalonada.pasos;
      }

      // Los AICc infinitos (modelos descartados por raíces junto al círculo
      // unitario) llegan como null y no se dibujan; se marcan aparte, con una
      // cruz en el borde superior del gráfico.
      const TECHO = 1302;
      function serieAicc(pasos) {
        return pasos.map(p => (p.infinito ? null : p.aicc));
      }

      function pintar() {
        const pasos = pasosActuales();
        const hasta = Math.min(Math.max(1, Math.round(params.paso)), pasos.length);
        const visibles = pasos.slice(0, hasta);
        const actual = pasos[hasta - 1];

        if (grafico) grafico.destroy();
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

        const mejorados = visibles.filter(p => p.mejora).length;
        actualizarLectura(lectura, [
          { etiqueta: 'Paso', valor: `${hasta} de ${pasos.length}` },
          { etiqueta: 'Modelo evaluado', valor: actual.etiqueta },
          { etiqueta: 'AICc', valor: actual.infinito ? '∞ (descartado)' : fmt(actual.aicc, 3) },
          { etiqueta: '¿mejora?', valor: !actual.mejora ? 'no'
              : params.exhaustiva ? 'sí, nuevo mejor' : 'sí, pasa a ser el actual' },
          { etiqueta: 'Mejor hasta aquí',
            valor: actual.mejor_hasta_aqui === null ? 'aún ninguno'
                                                    : fmt(actual.mejor_hasta_aqui, 3) },
          { etiqueta: 'Mejoras acumuladas', valor: mejorados }
        ]);

        lista.innerHTML = visibles.map((p, i) => {
          const marca = p.mejora ? '<strong style="color:#FF6600;">◆</strong>' : '·';
          const valor = p.infinito ? '∞' : fmt(p.aicc, 3);
          const fuerte = i === hasta - 1 ? ' style="background:rgba(255,102,0,0.10);"' : '';
          return `<div${fuerte}><code>${marca} ${p.etiqueta}</code> — AICc ${valor}</div>`;
        }).join('');
      }

      const controles = raiz.querySelector('.simulador-controles');
      const inputs = crearControles(controles, [
        { clave: 'paso', etiqueta: 'Paso de la búsqueda ', min: 1, max: HK.escalonada.pasos.length, paso: 1, decimales: 0 }
      ], params, pintar);
      inputPaso = inputs.paso;

      crearInterruptores(controles, [
        { clave: 'exhaustiva', etiqueta: 'Búsqueda exhaustiva (42 modelos)' }
      ], params, () => {
        const n = pasosActuales().length;
        inputPaso.max = n;
        params.paso = Math.min(params.paso, n);
        inputPaso.value = params.paso;
        inputPaso.parentElement.querySelector('output').textContent = String(params.paso);
        pintar();
      });

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 8 · La firma de la sobrediferenciación
    // ================================================================
    SIMULADORES['sobrediferenciacion'] = function (raiz) {
      const tabla = NILO.sobrediferenciacion;
      const params = { d: 1 };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cSerie, cVar] = raiz.querySelectorAll('canvas');
      let gSerie = null, gVar = null;

      function pintar() {
        const d = Math.round(params.d);
        const fila = tabla[d];
        const y = diferenciarVeces(SERIES_CAP4.nilo.valores, d);

        [gSerie, gVar].forEach(g => { if (g) g.destroy(); });
        gSerie = lineaSimple(cSerie, aniosDesde(SERIES_CAP4.nilo.inicio[0], y.length, d), y,
          `${nabla(d)}Nilo`,
          d <= 1 ? COLORES_GRAFICO.primario : '#b91c1c',
          { scales: escalasLinea(d === 0 ? UNIDAD_NILO : `Diferencia (${UNIDAD_NILO})`) });

        // La varianza real sobre un eje logarítmico: las marcas se leen en
        // unidades de varianza y la razón entre barras es la que se ve.
        gVar = crearGraficoBarras(cVar, tabla.map(f => `d = ${f.d}`),
          tabla.map(f => f.varianza), {
            etiqueta: 'Varianza de la serie diferenciada', color: COLORES_GRAFICO.gris
          });
        gVar.data.datasets[0].backgroundColor = tabla.map(
          f => f.d === d ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        gVar.options.scales.y = {
          type: 'logarithmic', min: 10000, max: 400000,
          title: { display: true, text: 'Varianza (log)',
                   font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 11 },
                   callback: v => [10000, 20000, 50000, 100000, 200000].includes(v) ? fmt(v, 0) : '' },
          grid: { color: 'rgba(148, 163, 184, 0.2)' }
        };
        gVar.update('none');

        const degenerado = Math.abs(fila.theta_ma1 + 1) < 0.005;
        const campos = [
          { etiqueta: 'd', valor: d },
          { etiqueta: 'n', valor: fila.n },
          { etiqueta: 'varianza', valor: fmt(fila.varianza) },
          { etiqueta: 'ρ̂₁', valor: fmt(fila.acf1, 4) },
          { etiqueta: 'θ̂ de un MA(1)', valor: fmt(fila.theta_ma1, 4) },
          { etiqueta: '|raíz MA|', valor: fmt(1 / Math.abs(fila.theta_ma1), 4) }
        ];
        campos.push(degenerado
          ? { etiqueta: '⚠ diagnóstico', valor: 'raíz unitaria en el MA: sobrediferenciado' }
          : { etiqueta: 'diagnóstico', valor: d === 1 ? 'mínimo de varianza' : 'sin diferenciar' });
        actualizarLectura(lectura, campos);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'd', etiqueta: 'Número de diferencias d ', min: 0, max: 3, paso: 1, decimales: 0 }
      ], params, pintar);

      pintar();
      return [manejador(() => gSerie), manejador(() => gVar)];
    };

    // ================================================================
    // Módulo 9 · La forma del pronóstico según d
    // ================================================================
    SIMULADORES['forma-pronostico'] = function (raiz) {
      const formas = NILO.formas_pronostico;
      const serie = SERIES_CAP4.nilo.valores;
      const inicio = SERIES_CAP4.nilo.inicio[0];
      const H = DATOS_CAP4.horizonte;
      const params = { modelo: 'd1', bandas: true };
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const etiquetas = aniosDesde(inicio, serie.length + H, 0);
      const nulos = serie.map(() => null);

      function pintar() {
        const f = formas[params.modelo];
        if (grafico) grafico.destroy();

        const datasets = [{
          label: 'Caudal observado',
          data: serie.concat(Array(H).fill(null)),
          borderColor: COLORES_GRAFICO.primario,
          borderWidth: 1.6, pointRadius: 0, fill: false
        }];

        if (params.bandas) {
          datasets.push(
            {
              label: 'Intervalo 95 %',
              data: nulos.concat(f.hi95),
              borderColor: 'rgba(255, 102, 0, 0.28)', backgroundColor: 'rgba(255, 102, 0, 0.10)',
              borderWidth: 1, pointRadius: 0, fill: '+3'
            },
            {
              label: 'Intervalo 80 %',
              data: nulos.concat(f.hi80),
              borderColor: 'rgba(255, 102, 0, 0.45)', backgroundColor: 'rgba(255, 102, 0, 0.18)',
              borderWidth: 1, pointRadius: 0, fill: '+1'
            },
            {
              label: '', data: nulos.concat(f.lo80),
              borderColor: 'rgba(255, 102, 0, 0.45)', borderWidth: 1, pointRadius: 0, fill: false
            },
            {
              label: '', data: nulos.concat(f.lo95),
              borderColor: 'rgba(255, 102, 0, 0.28)', borderWidth: 1, pointRadius: 0, fill: false
            });
        }

        // El pronóstico arranca enganchado al último observado, como en el
        // abanico de la TRM, para que la línea no salga flotando.
        const enganche = nulos.slice();
        enganche[enganche.length - 1] = serie[serie.length - 1];
        datasets.push({
          label: 'Pronóstico',
          data: enganche.concat(f.media),
          borderColor: COLORES_GRAFICO.secundario,
          borderWidth: 2.4, pointRadius: 0, fill: false
        });

        grafico = crearGraficoLinea(canvas, etiquetas, datasets, {
          plugins: {
            legend: { labels: { font: { family: 'Montserrat', size: 12 }, boxWidth: 24,
                                filter: item => item.text !== '' } },
            tooltip: { backgroundColor: '#012820', titleFont: { family: 'Montserrat' },
                       bodyFont: { family: 'Fira Code' },
                       filter: item => item.dataset.label !== '' }
          },
          scales: escalasLinea(`Caudal (${UNIDAD_NILO})`,
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
        ]);
      }

      const controles = raiz.querySelector('.simulador-controles');
      crearSelector(controles, {
        clave: 'modelo', etiqueta: 'Modelo',
        opciones: [
          { valor: 'd0', texto: 'ARIMA(1,0,1) con media — vuelve a la media' },
          { valor: 'd1', texto: 'ARIMA(1,1,1) sin constante — se queda plano' },
          { valor: 'd1_deriva', texto: 'ARIMA(1,1,1) con deriva — recta' },
          { valor: 'd2', texto: 'ARIMA(1,2,1) — recta, e intervalo enorme' }
        ]
      }, params, pintar);
      crearInterruptores(controles, [
        { clave: 'bandas', etiqueta: 'Mostrar intervalos 80 % y 95 %' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 9 · Pesos psi y anchura del intervalo
    // ================================================================
    SIMULADORES['pesos-psi-sigma'] = function (raiz) {
      const inter = NILO.intervalos;
      const H = inter.sigma_h.length;
      const params = { h: 10 };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cPsi, cSigma] = raiz.querySelectorAll('canvas');
      let gPsi = null, gSigma = null;

      const etiquetasH = Array.from({ length: H }, (_, i) => String(i + 1));
      const raizH = Array.from({ length: H }, (_, i) => inter.sigma * Math.sqrt(i + 1));

      function pintar() {
        const h = Math.round(params.h);

        if (gPsi) gPsi.destroy();
        gPsi = crearGraficoBarras(cPsi,
          inter.psi.map((_, i) => String(i)), inter.psi, {
            etiqueta: 'Peso ψⱼ', color: COLORES_GRAFICO.primario,
            tituloX: 'j', min: 0, max: 1.05
          });
        gPsi.data.datasets[0].backgroundColor = inter.psi.map(
          (_, i) => i < h ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        gPsi.update('none');

        if (!gSigma) {
          gSigma = crearGraficoLinea(cSigma, etiquetasH, [
            {
              label: 'σₕ del ARIMA(1,1,1)',
              data: inter.sigma_h, borderColor: COLORES_GRAFICO.secundario,
              borderWidth: 2.2, pointRadius: 0, fill: false
            },
            {
              label: 'σ√h — caminata aleatoria con la misma σ',
              data: raizH, borderColor: COLORES_GRAFICO.terciario,
              borderDash: [6, 4], borderWidth: 1.8, pointRadius: 0, fill: false
            },
            {
              // Los dos puntos del horizonte elegido: la distancia entre ellos
              // es lo que la intro pide mirar.
              label: '', data: [], showLine: false, pointRadius: 5,
              borderColor: COLORES_GRAFICO.secundario, backgroundColor: COLORES_GRAFICO.secundario
            },
            {
              label: '', data: [], showLine: false, pointRadius: 5,
              borderColor: COLORES_GRAFICO.terciario, backgroundColor: COLORES_GRAFICO.terciario
            }
          ], {
            plugins: {
              legend: { labels: { font: { family: 'Montserrat', size: 12 }, boxWidth: 24,
                                  filter: item => item.text !== '' } },
              tooltip: { backgroundColor: '#012820', titleFont: { family: 'Montserrat' },
                         bodyFont: { family: 'Fira Code' },
                         filter: item => item.dataset.label !== '' }
            },
            scales: {
              x: { title: { display: true, text: 'Horizonte h' },
                   ticks: { font: { family: 'Fira Code', size: 10 }, maxTicksLimit: 10 },
                   grid: { display: false } },
              y: { min: 0,
                   title: { display: true, text: `σ (${UNIDAD_NILO})`,
                            font: { family: 'Montserrat', size: 11 } },
                   ticks: { font: { family: 'Fira Code', size: 11 } } }
            }
          });
        }
        gSigma.data.datasets[2].data = inter.sigma_h.map((v, i) => (i === h - 1 ? v : null));
        gSigma.data.datasets[3].data = raizH.map((v, i) => (i === h - 1 ? v : null));
        gSigma.update('none');

        actualizarLectura(lectura, [
          { etiqueta: 'h', valor: h },
          { etiqueta: 'ψₕ₋₁', valor: fmt(inter.psi[h - 1], 4) },
          { etiqueta: 'σ', valor: fmt(inter.sigma, 3) },
          { etiqueta: 'σₕ', valor: fmt(inter.sigma_h[h - 1], 3) },
          { etiqueta: 'σ√h', valor: fmt(inter.sigma * Math.sqrt(h), 3) },
          { etiqueta: 'semiancho 95 %', valor: fmt(inter.z95 * inter.sigma_h[h - 1], 2) },
          { etiqueta: 'σₕ / σ', valor: fmt(inter.sigma_h[h - 1] / inter.sigma, 3) },
          { etiqueta: 'frente a la caminata',
            valor: `×${fmt(inter.sigma_h[h - 1] / (inter.sigma * Math.sqrt(h)), 3)}` }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'h', etiqueta: 'Horizonte h ', min: 1, max: H, paso: 1, decimales: 0 }
      ], params, pintar);

      pintar();
      return [manejador(() => gPsi), manejador(() => gSigma)];
    };

    // ================================================================
    // Módulo 10 · La TRM
    // ================================================================
    SIMULADORES['trm-identificacion'] = function (raiz) {
      const params = { d: '0' };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cSerie, cAcf] = raiz.querySelectorAll('canvas');
      let gSerie = null, gAcf = null;

      const inicio = SERIES_CAP4.trm.inicio;

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = d === 0 ? TRM.identificacion.cruda : TRM.identificacion.d1;
        const y = diferenciarVeces(SERIES_CAP4.trm.valores, d);

        [gSerie, gAcf].forEach(g => { if (g) g.destroy(); });
        gSerie = lineaSimple(cSerie, mesesDesde(inicio[0], inicio[1] + d, y.length), y,
          d === 0 ? 'TRM mensual (COP/USD)' : '∇TRM',
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario,
          { scales: escalasLinea(d === 0 ? 'COP por USD' : 'Cambio mensual (COP por USD)') });
        gAcf = crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        });

        const fuera = info.acf.filter(v => Math.abs(v) > info.banda).length;
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'banda', valor: `±${fmt(info.banda, 4)}` },
          { etiqueta: 'ρ̂₁', valor: fmt(info.acf[0], 4) },
          { etiqueta: 'ACF fuera de banda', valor: `${fuera} de ${info.acf.length}` },
          { etiqueta: d === 0 ? 'ADF (nivel)' : 'ADF (∇)',
            valor: `p = ${fmt(d === 0 ? TRM.pruebas.adf_nivel.p : TRM.pruebas.adf_d1.p, 4)}` },
          // tseries acota el p-valor de KPSS a [0.01, 0.10]: se dice como cota.
          { etiqueta: d === 0 ? 'KPSS (nivel)' : 'KPSS (∇)',
            valor: (() => {
              const k = d === 0 ? TRM.pruebas.kpss_nivel : TRM.pruebas.kpss_d1;
              const pv = k.p <= 0.01 ? 'p < 0.01' : k.p >= 0.1 ? 'p > 0.10' : `p = ${fmt(k.p, 4)}`;
              return `${fmt(k.estadistico, 4)} (${pv})`;
            })() }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'd', etiqueta: 'Serie',
        opciones: [
          { valor: '0', texto: 'TRM en niveles' },
          { valor: '1', texto: '∇TRM — primera diferencia' }
        ]
      }, params, pintar);

      pintar();
      return [manejador(() => gSerie), manejador(() => gAcf)];
    };

    // ================================================================
    // Módulo 10 · El abanico de la caminata aleatoria
    // ================================================================
    // Aquí no hay nada precalculado: con sigma^2 del ajuste y el último valor
    // observado, las bandas salen de la fórmula del Módulo 9 con psi_j = 1,
    // que es lo que hace que se reduzca a sigma*sqrt(h) EXACTAMENTE.
    SIMULADORES['trm-abanico'] = function (raiz) {
      const serie = SERIES_CAP4.trm.valores;
      const inicio = SERIES_CAP4.trm.inicio;
      const sigma = Math.sqrt(TRM.caminata.sigma2);
      const ultimo = serie[serie.length - 1];
      const VISIBLES = 48;                 // meses de historia a la vista
      const H_MAX = 36;
      const Z80 = 1.281552, Z95 = 1.959964;
      const params = { h: 24 };
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const historia = serie.slice(-VISIBLES);
      // El primer mes visible, para que las etiquetas cuadren con el recorte.
      const saltados = serie.length - historia.length;
      const mesInicial = inicio[1] + saltados;

      function pintar() {
        const H = Math.round(params.h);
        if (grafico) grafico.destroy();
        const etiquetas = mesesDesde(inicio[0], mesInicial, historia.length + H);
        // El pronóstico arranca enganchado al último observado, para que la
        // línea no salga flotando: por eso el relleno empieza en ese punto.
        const previos = historia.map(() => null);
        previos[previos.length - 1] = ultimo;
        const borde = z => previos.concat(
          Array.from({ length: H }, (_, j) => ultimo + z * sigma * Math.sqrt(j + 1)));

        const datasets = [
          {
            label: 'TRM observada',
            data: historia.concat(Array(H).fill(null)),
            borderColor: COLORES_GRAFICO.primario,
            borderWidth: 1.6, pointRadius: 0, fill: false
          },
          {
            label: 'Intervalo 95 %', data: borde(Z95),
            borderColor: 'rgba(255, 102, 0, 0.28)', backgroundColor: 'rgba(255, 102, 0, 0.10)',
            borderWidth: 1, pointRadius: 0, fill: '+3'
          },
          {
            label: 'Intervalo 80 %', data: borde(Z80),
            borderColor: 'rgba(255, 102, 0, 0.45)', backgroundColor: 'rgba(255, 102, 0, 0.18)',
            borderWidth: 1, pointRadius: 0, fill: '+1'
          },
          {
            label: '', data: borde(-Z80),
            borderColor: 'rgba(255, 102, 0, 0.45)', borderWidth: 1, pointRadius: 0, fill: false
          },
          {
            label: '', data: borde(-Z95),
            borderColor: 'rgba(255, 102, 0, 0.28)', borderWidth: 1, pointRadius: 0, fill: false
          },
          {
            label: 'Pronóstico', data: borde(0),
            borderColor: COLORES_GRAFICO.secundario,
            borderWidth: 2.4, pointRadius: 0, fill: false
          }
        ];

        grafico = crearGraficoLinea(canvas, etiquetas, datasets, {
          plugins: {
            legend: { labels: { font: { family: 'Montserrat', size: 12 }, boxWidth: 24,
                                filter: item => item.text !== '' } },
            tooltip: { backgroundColor: '#012820', titleFont: { family: 'Montserrat' },
                       bodyFont: { family: 'Fira Code' },
                       filter: item => item.dataset.label !== '' }
          },
          scales: escalasLinea('COP por USD',
            { ticks: { font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 10, maxRotation: 0 } })
        });

        const semi = Z95 * sigma * Math.sqrt(H);
        actualizarLectura(lectura, [
          { etiqueta: 'σ̂', valor: fmt(sigma) },
          { etiqueta: 'Pronóstico', valor: `${fmt(ultimo)} — el último observado, a cualquier horizonte` },
          { etiqueta: `σ a ${H} meses`, valor: `${fmt(sigma * Math.sqrt(H))} = σ̂·√${H}` },
          { etiqueta: 'Intervalo 95 %', valor: `[${fmt(ultimo - semi)}, ${fmt(ultimo + semi)}]` },
          { etiqueta: 'Semiancho sobre el nivel', valor: `±${fmt(100 * semi / ultimo, 1)} %` },
          { etiqueta: 'Frente al horizonte a un mes', valor: `×${fmt(Math.sqrt(H), 2)} — y sin techo` }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'h', etiqueta: 'Horizonte h (meses) ', min: 1, max: H_MAX, paso: 1, decimales: 0 }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 10 · El puente al Capítulo 5
    // ================================================================
    SIMULADORES['puente-estacional'] = function (raiz) {
      const params = { modelo: 'no' };
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const etiquetas = etiquetasRezago(PUENTE.no_estacional.acf_residuales.length);

      function pintar() {
        const esNo = params.modelo === 'no';
        const info = esNo ? PUENTE.no_estacional : PUENTE.estacional;
        const acf = info.acf_residuales;

        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetas, acf, {
          etiqueta: esNo ? `ACF residual · ${PUENTE.no_estacional.resultado}`
                         : `ACF residual · ${PUENTE.estacional.etiqueta}`,
          color: esNo ? '#b91c1c' : COLORES_GRAFICO.primario,
          lineas: lineasBanda(PUENTE.n), tituloX: 'Rezago k'
        });

        const p = esNo ? PUENTE.no_estacional.ljung_box_24.p : PUENTE.estacional.ljung_box_24_p;
        actualizarLectura(lectura, [
          { etiqueta: 'Modelo', valor: esNo ? PUENTE.no_estacional.resultado : PUENTE.estacional.etiqueta },
          { etiqueta: 'ρ̂₁₂', valor: fmt(acf[11], 4) },
          { etiqueta: 'ρ̂₂₄', valor: fmt(acf[23], 4) },
          { etiqueta: 'banda', valor: `±${fmt(PUENTE.no_estacional.banda, 4)}` },
          { etiqueta: 'Ljung–Box(24)', valor: p < 1e-6 ? 'p < 0.000001' : `p = ${fmt(p, 4)}` },
          { etiqueta: 'veredicto', valor: p < 0.05 ? 'RECHAZA: falta estructura' : 'pasa el diagnóstico' }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'modelo', etiqueta: 'Modelo ajustado a log(AirPassengers)',
        opciones: [
          { valor: 'no', texto: 'El mejor ARIMA NO estacional (este capítulo)' },
          { valor: 'si', texto: 'El modelo airline estacional (Capítulo 5)' }
        ]
      }, params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Autoevaluación del capítulo
    // ================================================================
    // Tabla ordenable de la rejilla del Nilo. Se incluye a propósito la columna
    // del n efectivo: ordenar por AICc con modelos de distinto d es el error que
    // este capítulo enseña a no cometer, y aquí queda a la vista.
    TABLAS_RANKING['rejilla-nilo'] = function () {
      const filas = Object.keys(NILO.rejilla).map(k => {
        const m = NILO.rejilla[k];
        return {
          modelo: m.etiqueta, d: m.d, n: m.n_efectivo, k: m.k,
          aicc: m.aicc, bic: m.bic, lb: m.ljung_box_p
        };
      });
      return {
        descripcion: 'Los 27 modelos ARIMA($p,d,q$) sobre el Nilo. Ordena por AICc y ' +
          'mira la columna <strong>n efectivo</strong>: el «mejor» tiene $d = 2$ y se ' +
          'evalúa sobre 98 observaciones, no sobre 100. <strong>Esa ordenación no es ' +
          'válida.</strong>',
        columnas: [
          { clave: 'modelo', titulo: 'Modelo', tipo: 'texto' },
          { clave: 'd', titulo: 'd', decimales: 0, mejor: 'menor' },
          { clave: 'n', titulo: 'n efectivo', tituloLargo: 'número de observaciones efectivas', decimales: 0, mejor: 'mayor' },
          { clave: 'k', titulo: 'k', tituloLargo: 'parámetros estimados, incluida la varianza σ²', decimales: 0, mejor: 'menor' },
          { clave: 'aicc', titulo: 'AICc', decimales: 2, mejor: 'menor' },
          { clave: 'bic', titulo: 'BIC', decimales: 2, mejor: 'menor' },
          { clave: 'lb', titulo: 'Ljung–Box(20) p', tituloLargo: 'p-valor de Ljung–Box con 20 rezagos', decimales: 4, mejor: 'mayor' }
        ],
        filas: filas,
        formato: fmt,
        inicial: 'd',
        destacada: 'ARIMA(1,1,1)',
        pie: 'Ordena primero por <em>d</em> y compara dentro de cada grupo; solo así ' +
          'la comparación es legítima. Los mejores por AICc son $(1,0,1)$, $(1,1,1)$ y ' +
          '$(1,2,2)$, uno por cada $d$, y no se pueden poner en la misma lista.'
      };
    };

    AUTOEVALUACIONES['cap4'] = [
      {
        tipo: 'opcion',
        modulo: 6,
        pregunta: 'Sobre la misma serie de $n = 100$ obtienes AICc $= 1267.51$ para un ARIMA($1,1,1$) y AICc $= 1264.60$ para un ARIMA($1,2,2$). ¿Cuál eliges?',
        pista: 'Antes de comparar dos números, pregúntate si están calculados sobre los mismos datos. ¿Cuántas observaciones entran en la verosimilitud de cada uno?',
        opciones: [
          {
            texto: 'El ARIMA($1,2,2$), porque $1264.60 < 1267.51$.',
            correcta: false,
            retro: 'Es la trampa central del capítulo. Un AICc menor con más diferencias no significa un modelo mejor: es la verosimilitud de <strong>otros datos</strong>, con una observación menos. Y en el Nilo ese modelo concreto tiene además una raíz MA en $1.03$, casi sobre el círculo unitario.'
          },
          {
            texto: 'Ninguno de los dos por esta comparación: no son comparables, porque tienen distinto $d$.',
            correcta: true,
            retro: 'El primero se calcula sobre $n^{*} = 99$ diferencias y el segundo sobre $98$ segundas diferencias: <strong>datos distintos</strong>. La comparación por AICc solo vale dentro de un mismo $d$. Para decidir entre distintos $d$ hay que usar las pruebas de raíz unitaria, el gráfico, o una evaluación fuera de muestra.'
          },
          {
            texto: 'El ARIMA($1,1,1$), porque menos diferencias es siempre mejor por parsimonia.',
            correcta: false,
            retro: 'La conclusión acierta por casualidad pero el razonamiento no sirve. La parsimonia es un criterio para $p$ y $q$ una vez fijado $d$; el orden de diferenciación no se elige por parsimonia sino por si la serie tiene o no raíz unitaria.'
          },
          {
            texto: 'El que tenga mejor BIC, que sí es comparable entre distintos $d$.',
            correcta: false,
            retro: 'El BIC tiene exactamente el mismo problema: también parte de $-2\\log L$, y esa verosimilitud está calculada sobre $n^{*} = n - d$ observaciones. Cambiar de criterio no arregla el que los datos sean distintos.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 9,
        pregunta: 'Para el ARIMA($1,1,1$) del Nilo, $\\hat\\sigma = 142.045$ y el primer peso es $\\psi_1 = 0.3802$ (con $\\psi_0 = 1$). ¿Cuánto vale $\\sigma_2$, la desviación del error de pronóstico a dos pasos? Da dos decimales.',
        pista: 'La fórmula es $\\sigma_h = \\sigma\\sqrt{\\sum_{j=0}^{h-1}\\psi_j^2}$. Con $h = 2$ entran solo dos términos: $\\psi_0 = 1$ y $\\psi_1$.',
        respuesta: 151.97,
        tolerancia: 0.4,
        retroAcierto: '$142.045 \\times \\sqrt{1 + 0.3802^2} = 142.045 \\times 1.0699 = 151.97$. Fíjate en que crece poco: el intervalo a dos pasos es apenas un $7\\,\\%$ más ancho que a uno.',
        retroFallo: 'Es $\\sigma_2 = \\sigma\\sqrt{\\psi_0^2 + \\psi_1^2} = 142.045\\sqrt{1 + 0.1445} = 151.97$. Los dos errores frecuentes: olvidar el término $\\psi_0 = 1$ (daría $54.0$), o sumar los $\\psi$ sin elevarlos al cuadrado. El $\\psi_0$ está siempre, y por eso $\\sigma_1 = \\sigma$ exactamente.'
      },
      {
        tipo: 'grafico',
        modulo: 10,
        alto: 200,
        descripcionGrafico: 'Correlograma de residuales con barras muy altas en los rezagos 12 y 24, y pequeñas en el resto',
        pregunta: 'Esta es la ACF de los residuales de un ARIMA ajustado a una serie <strong>mensual</strong>. ¿Qué hay que hacer?',
        pista: 'No mires solo si hay barras fuera de la banda: mira <em>en qué rezagos</em> están. ¿Tienen algo en común los números 12 y 24 en una serie mensual?',
        dibujar: canvas => crearGraficoBarras(canvas,
          etiquetasRezago(PUENTE.no_estacional.acf_residuales.length),
          PUENTE.no_estacional.acf_residuales, {
            etiqueta: 'ACF de los residuales', color: '#b91c1c',
            lineas: lineasBanda(PUENTE.n), tituloX: 'Rezago k'
          }),
        opciones: [
          {
            texto: 'Aumentar $q$ hasta que las barras entren en la banda.',
            correcta: false,
            retro: 'Funcionaría en el sentido técnico, pero necesitarías $q = 24$ para alcanzar el rezago 24, es decir veinticuatro parámetros para describir un patrón que se repite cada doce meses. Un modelo estacional captura lo mismo con dos.'
          },
          {
            texto: 'Diferenciar una vez más: la autocorrelación alta indica no estacionariedad.',
            correcta: false,
            retro: 'Diferenciar de nuevo en el rezago 1 no toca el patrón de los rezagos 12 y 24, y además introduciría la raíz unitaria en el MA que estudió el Módulo 8. Lo que hace falta aquí es una diferencia <strong>estacional</strong> $\\nabla_{12}$, que es otra cosa.'
          },
          {
            texto: 'Pasar a un modelo estacional: el patrón está en los múltiplos del período $m = 12$.',
            correcta: true,
            retro: '$\\hat\\rho_{12} = 0.72$ y $\\hat\\rho_{24} = 0.67$ frente a una banda de $0.163$: la estructura sobrante es exactamente estacional. Subir $q$ hasta 24 lo cubriría con dos docenas de parámetros; un SARIMA lo hace con dos. Es el Capítulo 5.'
          },
          {
            texto: 'Nada: la mayoría de las barras están dentro de la banda, así que el modelo es adecuado.',
            correcta: false,
            retro: 'Contar cuántas barras se salen no basta, y aquí las que se salen lo hacen por un factor de cuatro. Ljung–Box(24) da $Q = 222.4$ con $p < 10^{-6}$: el rechazo es rotundo. Un patrón sistemático en pocos rezagos es peor señal que ruido repartido en muchos.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 5,
        pregunta: 'Marca <strong>todas</strong> las afirmaciones correctas sobre la constante en un modelo ARIMA.',
        pista: 'Son tres. Piensa en: qué significa la constante cuando $d = 1$, qué hace <code>stats::arima</code> con <code>include.mean</code> si $d \\ge 1$, y qué grado de tendencia genera cada $d$.',
        opciones: [
          { texto: 'Con $d = 1$ la constante es la media de las <em>diferencias</em>, es decir una tendencia lineal en la serie original.', correcta: true },
          { texto: 'Con $d \\ge 1$, <code>stats::arima</code> ignora <code>include.mean</code> sin avisar.', correcta: true },
          { texto: 'Sin constante, un modelo con $d = 2$ pronostica una parábola.', correcta: false },
          { texto: 'Con $d \\ge 2$, <code>forecast::Arima</code> avisa y no ajusta la deriva.', correcta: true },
          { texto: 'La constante de un ARIMA($p,0,q$) es la ordenada al origen de una regresión, no la media del proceso.', correcta: false }
        ],
        retroAcierto: 'Las tres. Y las dos falsas son justo las que el capítulo desmiente midiendo: con $d = 2$ y sin constante la segunda diferencia del pronóstico tiende a cero ($\\nabla^2\\hat y \\to 0$), es decir a largo plazo sale una <strong>recta</strong>; y el <code>intercept</code> que devuelve R para un ARIMA($p,0,q$) <strong>es</strong> la media del proceso, $920.70$ en el Nilo, pese al nombre.',
        retroFallo: 'Las tres correctas son las que hablan de la constante con $d = 1$, de <code>include.mean</code> con $d \\ge 1$ y de la deriva con $d \\ge 2$. Sobre las falsas: la parábola necesitaría constante <em>con</em> $d = 2$, y <code>forecast</code> se niega precisamente a eso; sin constante, el pronóstico con $d = 2$ es una recta (lo verifica el Módulo 9 midiendo $\\nabla^2\\hat y$). Y el <code>intercept</code> de R en un modelo con $d = 0$ es la media, no una ordenada al origen: el nombre despista.'
      },
      {
        tipo: 'opcion',
        modulo: 3,
        pregunta: 'Simulas $1000$ series de ruido blanco puro de longitud $100$ y les añades a todas un escalón en la posición $29$ (la de 1899 en el Nilo). ¿Con qué frecuencia rechaza KPSS la hipótesis de estacionariedad?',
        pista: 'Recuerda cómo se construye el estadístico: sobre las <em>sumas parciales</em> de los residuales respecto de la media global. ¿Qué le pasa a esas sumas cuando todos los residuales de un tramo tienen el mismo signo?',
        opciones: [
          {
            texto: 'Prácticamente siempre, si el escalón es apreciable: con el del Nilo, el $100\\,\\%$ de las veces.',
            correcta: true,
            retro: 'Es el experimento del Módulo 3. Sin escalón rechaza el $4.8\\,\\%$ —su tamaño nominal—, y con el escalón real del Nilo ($1.95$ desviaciones típicas) el $100\\,\\%$. Basta un escalón de $0.79$ desviaciones para llegar al $70.8\\,\\%$. KPSS no distingue una raíz unitaria de un cambio de nivel.'
          },
          {
            texto: 'Alrededor del $5\\,\\%$, porque las series son estacionarias por construcción.',
            correcta: false,
            retro: 'Eso es lo que ocurre <strong>sin</strong> el escalón, y confirma que la prueba está bien calibrada: $4.8\\,\\%$ frente al $5\\,\\%$ nominal. Con el escalón la cosa cambia por completo, porque las sumas parciales dejan de compensarse y el estadístico se dispara.'
          },
          {
            texto: 'Nunca, porque KPSS solo detecta raíces unitarias y aquí no hay ninguna.',
            correcta: false,
            retro: 'KPSS no prueba "hay raíz unitaria": su hipótesis nula es <strong>la serie es estacionaria alrededor de una media constante</strong>. Una serie con un escalón no lo es, así que la prueba rechaza con toda la razón. El error está en traducir su rechazo por "hay que diferenciar".'
          },
          {
            texto: 'Depende del tamaño de la muestra, pero no del tamaño del escalón.',
            correcta: false,
            retro: 'Depende de los dos, y la simulación lo muestra: con $n$ fijo en 100, la tasa de rechazo pasa de alrededor del $5\\,\\%$ al $100\\,\\%$ solo moviendo el tamaño del escalón $\\beta$. Mientras el escalón es pequeño, el estadístico crece aproximadamente como $n\\beta^2/\\hat\\sigma^2_{LP}$.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 4,
        alto: 200,
        descripcionGrafico: 'Correlograma cuyas barras decaen despacio desde 0.50 sin llegar a cortarse en veinte rezagos',
        pregunta: 'Esta es la ACF de una serie <strong>sin diferenciar</strong>. ¿Qué se puede concluir sobre $p$ y $q$?',
        pista: 'Antes de leer $p$ y $q$ en un correlograma hay que estar seguro de una cosa. ¿Qué condición exige la tabla de identificación del Capítulo 3?',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS, NILO.identificacion.cruda.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(NILO.identificacion.cruda.n), tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Es un AR de orden alto, porque hay muchas barras fuera de la banda.',
            correcta: false,
            retro: 'Es el error de principiante más caro del capítulo. Un AR estacionario tiene una ACF que decae <strong>geométricamente</strong> y acaba entrando en la banda; esta lleva veinte rezagos sin acercarse a cero. Lo que ves no es memoria larga del proceso: es que el nivel de la serie está vagando.'
          },
          {
            texto: 'Es un MA($q$) con $q$ igual al número de barras significativas.',
            correcta: false,
            retro: 'Un MA($q$) tiene la ACF <strong>exactamente</strong> cero a partir del rezago $q$ — un corte limpio, no un descenso gradual. Aquí no hay corte por ninguna parte.'
          },
          {
            texto: 'Que $d = 1$, porque el primer valor es $0.498$, cercano a $0.5$.',
            correcta: false,
            retro: 'La conclusión sobre $d$ es correcta pero el argumento no: el valor de $\\hat\\rho_1$ no determina $d$. Lo que indica no estacionariedad es la <strong>forma</strong> del decaimiento —lento y sin cortar—, no la altura de la primera barra. Un AR(1) con $\\phi = 0.5$ tendría también $\\rho_1 = 0.5$ y sería perfectamente estacionario.'
          },
          {
            texto: 'Nada todavía: esa forma indica no estacionariedad, y hay que diferenciar antes de leer $p$ y $q$.',
            correcta: true,
            retro: 'Una ACF que decae despacio y no corta —aquí $0.498,\\ 0.385,\\ 0.328,\\ 0.239,\\dots$— es el retrato de una serie no estacionaria. La tabla de identificación presupone estacionariedad; aplicarla aquí no informa de nada. Tras diferenciar, la ACF corta: solo destacan el rezago 1 ($-0.402$) y, aislado, el 8 ($0.231$).'
          }
        ]
      },
      {
        tipo: 'opcion',
        modulo: 7,
        pregunta: '<code>auto.arima</code> devuelve un ARIMA($1,1,1$) con AICc $1267.507$. La búsqueda exhaustiva confirma que es el mínimo, y el quinto clasificado tiene $1269.216$. ¿Qué se concluye?',
        pista: '¿Cuánta diferencia de AICc hace falta para distinguir dos modelos? Compara ese umbral con la distancia entre el primero y el quinto.',
        opciones: [
          {
            texto: 'Que el ARIMA($1,1,1$) es el modelo verdadero, ya que lo confirman las dos búsquedas.',
            correcta: false,
            retro: 'Que dos búsquedas coincidan dice que el <em>algoritmo</em> es consistente, no que el modelo sea verdadero. Ambas optimizan el mismo criterio sobre los mismos datos, así que coincidir es lo esperable. Y con cinco candidatos en $1.71$ puntos, el criterio apenas los separa.'
          },
          {
            texto: 'Que la búsqueda escalonada es innecesaria, porque la exhaustiva llega al mismo sitio.',
            correcta: false,
            retro: 'Aquí llegaron al mismo sitio, pero eso no está garantizado: la escalonada explora un vecindario y puede quedarse en un óptimo local. Es la escalonada la que existe por eficiencia ($18$ modelos frente a $42$); precisamente por eso conviene contrastar con la completa en casos difíciles.'
          },
          {
            texto: 'Que hay cinco modelos prácticamente indistinguibles, y conviene decirlo en vez de presentar un único ganador.',
            correcta: true,
            retro: 'La diferencia entre el primero y el quinto es de $1.71$ puntos, por debajo del umbral habitual de $2$. Entre esos cinco está el ARIMA($0,1,1$) que proponía el correlograma. <code>auto.arima</code> no miente, pero su salida de una línea no comunica esa incertidumbre; <code>trace = TRUE</code> sí.'
          },
          {
            texto: 'Que como la diferencia es menor que $2$, hay que elegir el modelo con menos parámetros de los cinco.',
            correcta: false,
            retro: 'La parsimonia es un criterio razonable para desempatar y llevaría al ARIMA($0,1,1$), que es defendible. Pero la conclusión que pide la pregunta es previa: lo primero es <strong>reconocer que hay un empate</strong>. Elegir por parsimonia sin decir que había cinco candidatos oculta la misma incertidumbre.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 8,
        unidad: '',
        pregunta: 'Ajustas un MA($1$) a $\\nabla^2$Nilo y obtienes $\\hat\\theta = -1.0000$. ¿Cuál es el módulo de la raíz del polinomio $\\theta(B) = 1 + \\hat\\theta B$? Da cuatro decimales.',
        pista: 'La raíz de $1 + \\theta B = 0$ es $B = -1/\\theta$. Sustituye $\\theta = -1$ y toma el valor absoluto.',
        respuesta: 1.0,
        tolerancia: 0.002,
        retroAcierto: 'La raíz es $B = -1/(-1) = 1$, de módulo $1.0000$: cae <strong>exactamente sobre el círculo unitario</strong>. Eso significa que $\\theta(B) = 1 - B$, el mismo operador de diferencia, así que el término MA está deshaciendo la segunda diferencia. Es la firma algebraica de la sobrediferenciación.',
        retroFallo: 'La raíz de $1 + \\theta B$ es $B = -1/\\theta$, y con $\\theta = -1$ da $B = 1$, módulo $1.0000$. Si respondiste $-1$, te faltó el módulo; si respondiste $0$, quizá resolviste $\\theta B = 0$. Lo importante es la lectura: módulo exactamente $1$ significa no invertible, y aquí es porque $(1+\\theta B) = (1-B)$ cancela la diferencia que acabas de imponer.'
      }
    ];

    // ================================================================
    // Simulacro del quiz (Módulo 11)
    //
    // Se responde y se cronometra, pero NO se corrige: en la página no hay
    // clave, ni retroalimentación, ni nada de donde deducirlas. Es lo que
    // lo distingue de la autoevaluación del Módulo 10, que sí las lleva: un
    // examen de práctica cuyas preguntas se van a aplicar no puede publicar
    // su clave, porque viajaría en el HTML de un capítulo público.
    //
    // Es el motor del Módulo 11 del capítulo 3 (injertado a su vez del
    // Módulo 13 del capítulo 4 de Estadística Espacial), con una diferencia:
    // aquel solo sabía de preguntas de opción, y el quiz de este capítulo
    // tiene cinco formas, las mismas que en Brightspace:
    //   · 'opcion'        una marca                 (Multiple Choice)
    //   · 'multiple'      varias marcas             (Multi-Select)
    //   · 'coincidencia'  un desplegable por fila   (Matching)
    //   · 'orden'         un puesto por elemento    (Ordering)
    //   · 'numero'        una cifra                 (Arithmetic)
    // Cada forma sabe construir sus controles, repintarlos desde el estado y
    // resumir lo respondido (FORMAS_SIMULACRO, abajo). Lo demás es lo del
    // capítulo 3:
    //   · se engancha al registro SIMULADORES, que loadModule() ya recorre;
    //   · lo respondido y el reloj viven en ESTADO_SIMULACRO, fuera del
    //     renderizado, para que salir a otro módulo y volver no borre veinte
    //     minutos de trabajo. El reloj sigue corriendo mientras tanto: se
    //     guarda la hora de final, no los segundos que quedan.
    //
    // El CSS gemelo está en ensamblado/componentes/simulacro.css (heredado del
    // capítulo 3) y en simulacro_respuestas.css (los desplegables y la casilla
    // numérica), que instala ensambla_cap4.py.
    //
    // SIMULACROS['id'] = { minutos, variante, preguntas: [{ n, etiqueta,
    // tipo, enunciado, y opciones | filas y respuestas | elementos }] } lo
    // escribe exporta_simulacro.py desde el banco del quiz, fuera del
    // repositorio.
    // ================================================================
    const SIMULACROS = {};
    const ESTADO_SIMULACRO = {};
    const LETRAS_SIMULACRO = 'abcdefghijklmnop'.split('');
    const LETRAS_ORDEN = 'ABCDEFGH'.split('');

    function escapaSimulacro(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // Una fila con su etiqueta y su control. El id enlaza la etiqueta con el
    // control, para el lector de pantalla y para que tocar el texto lo active.
    function filaSimulacro(zona, clase, idControl, marca, texto) {
      const caja = document.createElement('div');
      caja.className = clase;
      const etiqueta = document.createElement('label');
      etiqueta.className = 'simulacro-fila-texto';
      etiqueta.htmlFor = idControl;
      if (marca) {
        const m = document.createElement('span');
        m.className = 'simulacro-letra';
        m.textContent = marca;
        etiqueta.append(m, ' ');
      }
      etiqueta.append(texto);
      caja.appendChild(etiqueta);
      zona.appendChild(caja);
      return caja;
    }

    const FORMAS_SIMULACRO = {
      opcion: {
        rotulo: '',
        vacia: () => [],
        respondida: r => r.length > 0,
        resumen: r => r.map(j => LETRAS_SIMULACRO[j]).join('') || '—',
        construye(zona, pr, leer, escribir) {
          const varias = pr.tipo === 'multiple';
          zona.className = 'simulacro-opciones';
          zona.setAttribute('role', 'group');
          zona.setAttribute('aria-label', `Opciones de la pregunta ${pr.n}`);
          const botones = pr.opciones.map((texto, j) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.className = 'simulacro-opcion';
            b.innerHTML = `<span class="simulacro-letra">${LETRAS_SIMULACRO[j]})</span><span>${texto}</span>`;
            b.onclick = () => {
              const r = leer();
              const puesta = r.includes(j);
              escribir(varias
                ? (puesta ? r.filter(x => x !== j) : r.concat(j).sort((a, b) => a - b))
                : (puesta ? [] : [j]));
            };
            zona.appendChild(b);
            return b;
          });
          return () => botones.forEach((b, j) => {
            const marcada = leer().includes(j);
            b.classList.toggle('marcada', marcada);
            b.setAttribute('aria-pressed', marcada ? 'true' : 'false');
          });
        }
      },

      coincidencia: {
        rotulo: ' · emparejar',
        vacia: pr => pr.filas.map(() => null),
        respondida: r => r.every(x => x !== null),
        resumen: r => r.every(x => x === null) ? '—'
          : r.map((x, f) => `${f + 1}${x === null ? '—' : LETRAS_SIMULACRO[x]}`).join(' '),
        construye(zona, pr, leer, escribir, prefijo) {
          zona.className = 'simulacro-filas';
          const selectores = pr.filas.map((fila, f) => {
            const id = `${prefijo}-${f + 1}`;
            const caja = filaSimulacro(zona, 'simulacro-fila', id, `${f + 1}.`, fila);
            const sel = document.createElement('select');
            sel.id = id;
            sel.className = 'simulacro-desplegable';
            sel.add(new Option('— Elegir —', ''));
            pr.respuestas.forEach((t, j) => sel.add(new Option(`${LETRAS_SIMULACRO[j]}) ${t}`, String(j))));
            sel.onchange = () => {
              const r = leer().slice();
              r[f] = sel.value === '' ? null : Number(sel.value);
              escribir(r);
            };
            caja.appendChild(sel);
            return sel;
          });
          return () => selectores.forEach((s, f) => {
            const x = leer()[f];
            s.value = x === null ? '' : String(x);
          });
        }
      },

      orden: {
        rotulo: ' · ordenar',
        vacia: pr => pr.elementos.map(() => null),
        respondida: r => r.every(x => x !== null),
        // El orden que sale de los puestos elegidos, de arriba abajo; «?» donde
        // un puesto está vacío o repetido.
        resumen: r => r.every(x => x === null) ? '—' : r.map((_, p) => {
          const en = r.map((x, e) => x === p + 1 ? e : -1).filter(e => e >= 0);
          return en.length === 1 ? LETRAS_ORDEN[en[0]] : '?';
        }).join(''),
        construye(zona, pr, leer, escribir, prefijo) {
          zona.className = 'simulacro-filas';
          const nota = document.createElement('p');
          nota.className = 'simulacro-nota';
          nota.textContent = `Elige el puesto de cada uno: 1.º es el de arriba y ${pr.elementos.length}.º el de abajo.`;
          zona.appendChild(nota);
          const selectores = pr.elementos.map((el, e) => {
            const id = `${prefijo}-${LETRAS_ORDEN[e]}`;
            const caja = filaSimulacro(zona, 'simulacro-fila simulacro-fila-orden', id, `${LETRAS_ORDEN[e]}.`, el);
            const sel = document.createElement('select');
            sel.id = id;
            sel.className = 'simulacro-desplegable simulacro-puesto';
            sel.add(new Option('—', ''));
            pr.elementos.forEach((_, p) => sel.add(new Option(`${p + 1}.º`, String(p + 1))));
            sel.onchange = () => {
              const r = leer().slice();
              r[e] = sel.value === '' ? null : Number(sel.value);
              escribir(r);
            };
            caja.prepend(sel);
            return sel;
          });
          return () => selectores.forEach((s, e) => {
            const x = leer()[e];
            s.value = x === null ? '' : String(x);
          });
        }
      },

      numero: {
        rotulo: ' · respuesta numérica',
        vacia: () => '',
        respondida: r => r.trim() !== '',
        resumen: r => r.trim() ? escapaSimulacro(r.trim()) : '—',
        construye(zona, pr, leer, escribir, prefijo) {
          zona.className = 'simulacro-filas';
          const id = `${prefijo}-cifra`;
          const caja = filaSimulacro(zona, 'simulacro-fila simulacro-fila-numero', id, '', 'Tu respuesta');
          const casilla = document.createElement('input');
          casilla.type = 'text';
          casilla.id = id;
          casilla.className = 'simulacro-numero';
          casilla.inputMode = 'decimal';
          casilla.autocomplete = 'off';
          casilla.spellcheck = false;
          // sin repintar mientras se escribe: repintar movería el cursor
          casilla.oninput = () => escribir(casilla.value, false);
          caja.appendChild(casilla);
          return () => { casilla.value = leer(); };
        }
      }
    };
    FORMAS_SIMULACRO.multiple = Object.assign({}, FORMAS_SIMULACRO.opcion, { rotulo: ' · varias respuestas' });

    SIMULADORES['cap4-simulacro'] = function (raiz) {
      const id = raiz.dataset.simulador;
      const sim = SIMULACROS[id];
      if (!sim) {
        console.warn(`Simulacro no registrado: ${id}`);
        return [];
      }
      if (!ESTADO_SIMULACRO[id]) {
        ESTADO_SIMULACRO[id] = {
          respuestas: sim.preguntas.map(pr => FORMAS_SIMULACRO[pr.tipo].vacia(pr)),
          finAt: null,
          restante: sim.minutos * 60
        };
      }
      return pintarSimulacro(raiz, sim, ESTADO_SIMULACRO[id]);
    };

    function pintarSimulacro(raiz, sim, estado) {
      const contenedor = raiz.querySelector('.simulacro-preguntas');
      const conteo = raiz.querySelector('.simulacro-conteo');
      const resumen = raiz.querySelector('.simulacro-resumen');
      const reloj = raiz.querySelector('.simulacro-reloj');
      const empezar = raiz.querySelector('.simulacro-empezar');
      const borrar = raiz.querySelector('.simulacro-borrar');
      const repintores = [];
      contenedor.innerHTML = '';

      sim.preguntas.forEach((pr, i) => {
        const forma = FORMAS_SIMULACRO[pr.tipo];
        const caja = document.createElement('div');
        caja.className = 'simulacro-pregunta';
        caja.innerHTML = `<span class="simulacro-etiqueta">${pr.n}. ${pr.etiqueta}${forma.rotulo}</span>` +
          `<div class="simulacro-enunciado">${pr.enunciado}</div>`;
        const zona = document.createElement('div');
        caja.appendChild(zona);
        contenedor.appendChild(caja);
        const leer = () => estado.respuestas[i];
        const escribir = (r, repintar = true) => {
          estado.respuestas[i] = r;
          if (repintar) repintores[i]();
          pintaMarcador();
        };
        repintores.push(forma.construye(zona, pr, leer, escribir, `${raiz.dataset.simulador}-${pr.n}`));
        repintores[i]();
      });

      function pintaMarcador() {
        const hechas = sim.preguntas.filter((pr, i) => FORMAS_SIMULACRO[pr.tipo].respondida(estado.respuestas[i])).length;
        conteo.textContent = `${hechas} de ${sim.preguntas.length} respondidas`;
        resumen.innerHTML = 'Tus respuestas: ' + sim.preguntas.map((pr, i) =>
          `<b>${pr.n}:</b> ${FORMAS_SIMULACRO[pr.tipo].resumen(estado.respuestas[i])}`
        ).join(' · ') + '. No se corrigen aquí.';
      }

      // El reloj: `finAt` es la hora en que se acaba y manda mientras corre;
      // `restante` solo guarda los segundos cuando está pausado.
      let tic = null;
      function para() {
        if (tic !== null) { clearInterval(tic); tic = null; }
      }
      function segundos() {
        return estado.finAt === null
          ? estado.restante
          : Math.max(0, Math.round((estado.finAt - Date.now()) / 1000));
      }
      function pintaReloj() {
        const s = segundos();
        reloj.textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
        reloj.classList.toggle('acabado', s === 0);
        empezar.textContent = estado.finAt !== null ? 'Pausar'
          : (s === sim.minutos * 60 ? `Empezar los ${sim.minutos} minutos` : 'Seguir');
      }
      function arranca() {
        para();
        tic = setInterval(() => {
          if (segundos() === 0) {
            estado.finAt = null;
            estado.restante = 0;
            para();
          }
          pintaReloj();
        }, 250);
      }
      empezar.onclick = () => {
        if (estado.finAt !== null) {          // corriendo: se pausa
          estado.restante = segundos();
          estado.finAt = null;
          para();
        } else {
          if (estado.restante === 0) estado.restante = sim.minutos * 60;
          estado.finAt = Date.now() + estado.restante * 1000;
          arranca();
        }
        pintaReloj();
      };
      borrar.onclick = () => {
        para();
        estado.respuestas = sim.preguntas.map(pr => FORMAS_SIMULACRO[pr.tipo].vacia(pr));
        estado.finAt = null;
        estado.restante = sim.minutos * 60;
        repintores.forEach(r => r());
        pintaMarcador();
        pintaReloj();
      };

      if (estado.finAt !== null) arranca();
      pintaReloj();
      pintaMarcador();
      // Lo que devuelve un simulador son los objetos que destruirSimuladores()
      // apaga al cambiar de módulo. Aquí no hay gráficos: lo que hay que apagar
      // es el intervalo, que si no seguiría pintando sobre nodos que ya no
      // están en el documento.
      return [{ destroy: para }];
    }

    // [inicio · simulacro del quiz]
    // ================================================================
    // Simulacro del quiz (Módulo 11) · variante 9, SIN CLAVE
    //
    // NO SE EDITA A MANO: lo escribe exporta_simulacro.py, fuera del
    // repositorio, desde el mismo banco que arma los paquetes de
    // Brightspace. Aquí solo viajan enunciados, opciones, filas y
    // respuestas posibles: la clave y la retroalimentación se quedan
    // fuera, porque este capítulo es público.
    //
    // La variante 9 no entra en el banco, a propósito: publicar una de las
    // ocho le daría a uno de cada ocho estudiantes las preguntas que va a
    // ver en el quiz, con tiempo ilimitado para estudiarlas.
    // ================================================================
    SIMULACROS['cap4-simulacro'] = {
      minutos: 40,
      variante: 9,
      preguntas: [
        {
          n: 1,
          etiqueta: 'cap. 3 · mód. 3.5 · autocorrelación de un ARMA(1,1)',
          tipo: 'numero',
          enunciado: '<p>Un proceso ARMA(1,1) estacionario e invertible sigue yₜ = 0.57 yₜ₋₁ + εₜ + 0.25 εₜ₋₁, con εₜ ruido blanco de varianza σ² (convenio de R: el θ suma). ¿Cuánto vale su autocorrelación en el rezago 2, ρ₂? Responde con cuatro decimales, escritos con punto decimal (no con coma).</p>'
        },
        {
          n: 2,
          etiqueta: 'cap. 3 · mód. 3.10 · revisar un informe de ajuste',
          tipo: 'multiple',
          enunciado: '<p>Un asistente de IA recibió una serie de n = 120 observaciones y entregó el informe de abajo. Revísalo paso por paso.</p><ol><li><strong>Identificación.</strong> «La ACF se corta después del rezago 2 y la PACF decae: propongo un AR(2).»</li><li><strong>Ajuste.</strong><pre style="white-space:pre;overflow-x:auto;font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; fit &lt;- arima(y, order = c(2, 0, 0))\n&gt; fit\nCoefficients:\n         ar1      ar2  intercept\n      1.2254  -0.3688    67.1246\ns.e.  0.0853   0.0902     0.9829</pre></li><li><strong>Constante.</strong> «La media del proceso es el intercept que imprime arima(), \\(\\hat\\mu = 67.1246\\), y la constante es \\(c = \\hat\\mu(1 - \\hat\\phi_1 - \\hat\\phi_2) = 9.63\\).»</li><li><strong>Comparación.</strong> «Comparé con <code>arima(y, order = c(1, 1, 1))</code>: su AICc es 461.51, frente a 459.67 del AR(2). Me quedo con el AR(2).»</li><li><strong>Diagnóstico.</strong><pre style="white-space:pre;overflow-x:auto;font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; Box.test(residuals(fit), lag = 10, type = &quot;Ljung-Box&quot;, fitdf = 2)$p.value\n[1] 0.8784271</pre>«p > 0.05: no hay evidencia de estructura sobrante en los residuales.»</li><li><strong>Estacionariedad.</strong><pre style="white-space:pre;overflow-x:auto;font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; round(Mod(polyroot(c(67.1246, -1.2254, 0.3688))), 4)\n[1] 13.4910 13.4910</pre>«Las dos raíces quedan fuera del círculo unitario: el AR(2) estimado es estacionario.»</li></ol><p>¿Cuáles de estas afirmaciones son correctas?</p><p><em>Marca todas las que correspondan. Cada casilla bien resuelta suma y cada una mal resuelta resta, con piso en cero.</em></p>',
          opciones: [
            'Error en el paso 1: si la ACF se corta en 2 y la PACF decae, lo que se sugiere es un MA(2), no un AR(2).',
            'Error en el paso 3: la media no es el intercept; faltó dividirlo por (1 − φ̂₁ − φ̂₂), porque arima() llama intercept a la constante.',
            'Error en el paso 4: el AICc de un ARIMA(1,1,1) no se compara con el de un AR(2), porque uno se ajusta a ∇y y el otro a y.',
            'Error en el paso 5: sobró fitdf = 2; en un AR puro no se descuenta nada de los grados de libertad.',
            'Error en el paso 6: sobró la media; el polinomio AR que recibe polyroot() empieza en 1, no en μ̂.'
          ]
        },
        {
          n: 3,
          etiqueta: 'cap. 3 · mód. 3.5-3.6 · correlogramas muestrales',
          tipo: 'coincidencia',
          enunciado: '<p>Cuatro series estacionarias de n = 300 observaciones. La tabla da sus autocorrelaciones muestrales simples (ACF) y parciales (PACF) en los rezagos 1 a 6; la banda al 95 % es ±0.113.</p><div style="overflow-x:auto; max-width:100%;"><table style="border-collapse:collapse; margin:6px 0;"><thead><tr><th style="border:1px solid #999; padding:3px 7px; text-align:center">Serie</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">Función</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">k = 1</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">k = 2</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">k = 3</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">k = 4</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">k = 5</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">k = 6</th></tr></thead><tbody><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">A</td><td style="border:1px solid #999; padding:3px 7px; text-align:left">ACF (r<sub>k</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.286</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.412</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.184</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.207</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.069</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.097</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left"></td><td style="border:1px solid #999; padding:3px 7px; text-align:left">PACF (φ̂<sub>kk</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.286</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.360</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.008</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.029</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.053</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.009</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">B</td><td style="border:1px solid #999; padding:3px 7px; text-align:left">ACF (r<sub>k</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.819</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.551</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.384</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.276</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.203</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.169</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left"></td><td style="border:1px solid #999; padding:3px 7px; text-align:left">PACF (φ̂<sub>kk</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.819</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.363</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.234</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.123</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.089</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.015</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">C</td><td style="border:1px solid #999; padding:3px 7px; text-align:left">ACF (r<sub>k</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.605</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.246</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.011</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.022</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.024</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.017</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left"></td><td style="border:1px solid #999; padding:3px 7px; text-align:left">PACF (φ̂<sub>kk</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.605</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.190</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.084</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.160</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.066</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.070</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">D</td><td style="border:1px solid #999; padding:3px 7px; text-align:left">ACF (r<sub>k</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.653</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.468</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.355</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.230</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.159</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.134</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left"></td><td style="border:1px solid #999; padding:3px 7px; text-align:left">PACF (φ̂<sub>kk</sub>)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.653</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.073</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.041</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.058</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.007</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.041</td></tr></tbody></table></div><p>Asocia cada serie con el modelo que sugiere su correlograma (módulos 3.5 y 3.6). Sobran dos modelos.</p>',
          filas: [
            'Serie A',
            'Serie B',
            'Serie C',
            'Serie D'
          ],
          respuestas: [
            'AR(1)',
            'AR(2)',
            'ARMA(1,1)',
            'MA(1)',
            'MA(2)',
            'Ruido blanco'
          ]
        },
        {
          n: 4,
          etiqueta: 'cap. 3 · mód. 3.7 · Yule-Walker',
          tipo: 'opcion',
          enunciado: '<p>De una serie de n = 90 observaciones se obtuvieron las autocovarianzas muestrales (con divisor n, como las calcula <code>acf()</code> de R) \\(\\hat\\gamma_0 = 16.0539\\), \\(\\hat\\gamma_1 = 11.8658\\) y \\(\\hat\\gamma_2 = 4.9091\\). Se quiere un AR(2).</p><p>¿Qué estimaciones da el método de Yule–Walker?</p>',
          opciones: [
            '\\(\\hat\\phi_1 = 1.2692,\\ \\hat\\phi_2 = −0.5301\\)',
            '\\(\\hat\\phi_1 = 0.9169,\\ \\hat\\phi_2 = −0.2405\\)',
            '\\(\\hat\\phi_1 = 1.1309,\\ \\hat\\phi_2 = −0.5301\\)',
            '\\(\\hat\\phi_1 = 0.9796,\\ \\hat\\phi_2 = −0.2405\\)'
          ]
        },
        {
          n: 5,
          etiqueta: 'cap. 3 · mód. 3.8 · criterios de información',
          tipo: 'orden',
          enunciado: '<p>Se ajustaron por máxima verosimilitud, todos con media, cuatro modelos a la misma serie de n = 40 observaciones. Sus log-verosimilitudes:</p><div style="overflow-x:auto; max-width:100%;"><table style="border-collapse:collapse; margin:6px 0;"><thead><tr><th style="border:1px solid #999; padding:3px 7px; text-align:center">Modelo</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">log L</th></tr></thead><tbody><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">MA(1)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−54.460</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">AR(1)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−59.190</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">MA(2)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−52.821</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">ARMA(1,1)</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−53.428</td></tr></tbody></table></div><p>Ordénalos por el AICc, del mejor (arriba) al peor (módulo 3.8). Solo puntúa el orden completo.</p>',
          elementos: [
            'MA(1)',
            'AR(1)',
            'MA(2)',
            'ARMA(1,1)'
          ]
        },
        {
          n: 6,
          etiqueta: 'cap. 3 · mód. 3.9 · intervalo en la escala original',
          tipo: 'numero',
          enunciado: '<p>Una serie anual de conteos tiene una amplitud que crece con su nivel. Como en el caso de las manchas solares (módulo 3.9), se ajustó un AR(2) a xₜ = √yₜ y se obtuvo φ̂₁ = 1.22, φ̂₂ = −0.58 y σ̂² = 2.14 (la varianza de las innovaciones, en la escala de la raíz). El pronóstico puntual a dos pasos en esa escala es x̂ = 5.83. ¿Cuál es el límite superior del intervalo de predicción al 95 % para y a dos pasos, en la escala original de la serie? Usa 1.96. Responde con dos decimales, escritos con punto decimal (no con coma).</p>'
        },
        {
          n: 7,
          etiqueta: 'cap. 4 · mód. 4.1 · el modelo escrito con B',
          tipo: 'coincidencia',
          enunciado: '<p>Cada fila es un modelo escrito con el operador de rezago B, con el convenio de R (los θ suman: (1 + θB)εₜ). φ₁* y φ₂* son los coeficientes del modelo escrito en niveles, yₜ = φ₁* yₜ₋₁ + φ₂* yₜ₋₂ + εₜ. Asocia cada modelo con lo que es (módulo 4.1). Sobran cinco respuestas.</p>',
          filas: [
            '(1 − B) yₜ = (1 − 0.32B) εₜ',
            '(1 + 0.25B)(1 − B) yₜ = (1 − 0.96B) εₜ',
            '(1 − 0.65B)(1 − B) yₜ = εₜ',
            '(1 − B) yₜ = 1.4 + εₜ',
            '(1 − B)² yₜ = (1 − 1.25B + 0.45B²) εₜ'
          ],
          respuestas: [
            'Un MA con raíz en B = 1.042, fuera del círculo unitario: no sobra nada',
            'Un ruido blanco con media fija de 1.4',
            'Un AR(2) en niveles con φ₁* = 1.65 y φ₂* = −0.65',
            'Equivale al método de Holt con tendencia',
            'Una caminata aleatoria con deriva 1.4',
            'Equivale al suavizamiento exponencial simple',
            'Equivale a una caminata aleatoria sin deriva',
            'Un MA con raíz en B = 1.042, casi igual a (1 − B): sobra la diferencia',
            'Un AR(2) en niveles con φ₁* = 0.35 y φ₂* = −0.65',
            'Equivale a una recta más un ruido blanco'
          ]
        },
        {
          n: 8,
          etiqueta: 'cap. 4 · mód. 4.2 y 3.8 · Ljung-Box y grados de libertad',
          tipo: 'opcion',
          enunciado: '<p>Se ajustó un ARIMA(2,1,1) por máxima verosimilitud a una serie de n = 150 observaciones y se corrió Ljung–Box sobre sus residuales, sin más argumentos (R llama X-squared al estadístico Q):</p><pre style="white-space:pre;overflow-x:auto;font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; fit &lt;- arima(y, order = c(2, 1, 1), method = &quot;ML&quot;)\n&gt; Box.test(residuals(fit), lag = 16, type = &quot;Ljung-Box&quot;)\n\n    Box-Ljung test\n\ndata:  residuals(fit)\nX-squared = 23.329, df = 16, p-value = 0.1052</pre><p>Algunos cuantiles 0.95 de la distribución χ²:</p><div style="overflow-x:auto; max-width:100%;"><table style="border-collapse:collapse; margin:6px 0;"><thead><tr><th style="border:1px solid #999; padding:3px 7px; text-align:center">gl</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">6</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">7</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">8</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">9</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">10</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">11</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">12</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">13</th></tr></thead><tbody><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">χ²<sub>0.95</sub></td><td style="border:1px solid #999; padding:3px 7px; text-align:right">12.59</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">14.07</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">15.51</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">16.92</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">18.31</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">19.68</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">21.03</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">22.36</td></tr></tbody></table></div><div style="overflow-x:auto; max-width:100%;"><table style="border-collapse:collapse; margin:6px 0;"><thead><tr><th style="border:1px solid #999; padding:3px 7px; text-align:center">gl</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">14</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">15</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">16</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">17</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">18</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">19</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">20</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">21</th></tr></thead><tbody><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">χ²<sub>0.95</sub></td><td style="border:1px solid #999; padding:3px 7px; text-align:right">23.68</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">25.00</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">26.30</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">27.59</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">28.87</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">30.14</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">31.41</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">32.67</td></tr></tbody></table></div><p>¿Qué afirmación es correcta, al 5 %?</p>',
          opciones: [
            'Con 13 grados de libertad, Q = 23.329 supera el valor crítico: se rechaza que los residuales sean ruido blanco.',
            'Con 12 grados de libertad, Q = 23.329 supera el valor crítico: se rechaza que los residuales sean ruido blanco.',
            'Con 15 grados de libertad, Q = 23.329 no llega al valor crítico: no se rechaza que los residuales sean ruido blanco.',
            'Con 16 grados de libertad, Q = 23.329 no llega al valor crítico: no se rechaza que los residuales sean ruido blanco.'
          ]
        },
        {
          n: 9,
          etiqueta: 'cap. 4 · mód. 4.3 · ADF, PP y KPSS',
          tipo: 'multiple',
          enunciado: '<p>Para decidir el orden de diferenciación d de una serie de n = 120 observaciones se corrieron en R las tres pruebas del módulo 4.3 (paquete <code>tseries</code>):</p><pre style="white-space:pre;overflow-x:auto;font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; adf.test(y)\n\n    Augmented Dickey-Fuller Test\n\ndata:  y\nDickey-Fuller = -2.7522, Lag order = 4, p-value = 0.2642\nalternative hypothesis: stationary\n\n\n&gt; pp.test(y)\n\n    Phillips-Perron Unit Root Test\n\ndata:  y\nDickey-Fuller Z(alpha) = -50.66, Truncation lag parameter = 4, p-value = 0.01\nalternative hypothesis: stationary\n\nWarning message:\nIn pp.test(y) : p-value smaller than printed p-value\n\n&gt; kpss.test(y)\n\n    KPSS Test for Level Stationarity\n\ndata:  y\nKPSS Level = 1.5885, Truncation lag parameter = 4, p-value = 0.01\n\nWarning message:\nIn kpss.test(y) : p-value smaller than printed p-value</pre><p>Al 5 %, ¿qué afirmaciones son correctas?</p><p><em>Marca todas las que correspondan. Cada casilla bien resuelta suma y cada una mal resuelta resta, con piso en cero.</em></p>',
          opciones: [
            'ADF apunta a diferenciar la serie.',
            'KPSS apunta a no diferenciar la serie.',
            'PP apunta a diferenciar la serie.',
            'ADF y KPSS apuntan a la misma decisión sobre d.',
            'PP y KPSS apuntan a decisiones opuestas sobre d.'
          ]
        },
        {
          n: 10,
          etiqueta: 'cap. 4 · mód. 4.3-4.4 · elegir d, p y q',
          tipo: 'opcion',
          enunciado: '<p>Para una serie de n = 151 observaciones se calcularon, para d = 0, 1 y 2, la varianza de \\(\\nabla^d y_t\\), sus autocorrelaciones simples \\(r_k\\) (ACF) y parciales \\(\\hat\\phi_{kk}\\) (PACF) en los rezagos 1 a 4, y la banda \\(\\pm 1.96/\\sqrt{n}\\):</p><div style="overflow-x:auto; max-width:100%;"><table style="border-collapse:collapse; margin:6px 0;"><thead><tr><th style="border:1px solid #999; padding:3px 7px; text-align:center">d</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">n</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">varianza</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">banda</th><th style="border:1px solid #999; padding:3px 7px; text-align:center">r<sub>1</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">r<sub>2</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">r<sub>3</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">r<sub>4</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">φ̂<sub>11</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">φ̂<sub>22</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">φ̂<sub>33</sub></th><th style="border:1px solid #999; padding:3px 7px; text-align:center">φ̂<sub>44</sub></th></tr></thead><tbody><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">0</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">151</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">67.21</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">±0.160</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.962</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.912</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.862</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.811</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.962</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.169</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.012</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.043</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">1</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">150</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">1.70</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">±0.160</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.411</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.025</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.011</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.013</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.411</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.172</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">0.086</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.028</td></tr><tr><td style="border:1px solid #999; padding:3px 7px; text-align:left">2</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">149</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">2.01</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">±0.161</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.172</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.315</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.015</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.019</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.172</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.355</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.177</td><td style="border:1px solid #999; padding:3px 7px; text-align:right">−0.217</td></tr></tbody></table></div><p>Siguiendo los módulos 4.3 y 4.4, ¿qué modelo se propone como punto de partida?</p>',
          opciones: [
            'ARIMA(1,0,0)',
            'ARIMA(0,0,1)',
            'ARIMA(1,1,0)',
            'ARIMA(0,1,1)'
          ]
        }
      ]
    };
    // [fin · simulacro del quiz]
