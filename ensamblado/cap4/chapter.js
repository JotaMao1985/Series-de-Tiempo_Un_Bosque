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

    // Lo mismo para un gráfico de barras (M4, M6, M10): crearGraficoBarras no
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

    // ∇, ∇², ∇³: el orden como exponente, igual que en la prosa.
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

    // Correlogramas de identificación (M4, M10): las barras que salen de la
    // banda van en el color de la serie y las de dentro en gris. Con el eje en
    // ±1, las barras de 0.21–0.24 del Nilo y el ρ̂₈ = −0.190 de la TRM quedan a
    // 1–3 px de la banda: el color dice cuáles salen sin medir píxeles, con el
    // mismo criterio que la cuenta de la lectura (|ρ̂| > banda).
    function resaltarFueraDeBanda(grafico, valores, b, color, nombre) {
      grafico.data.datasets[0].backgroundColor =
        valores.map(v => (Math.abs(v) > b ? color : COLORES_GRAFICO.gris));
      const etiquetas = grafico.options.plugins.legend.labels;
      const base = etiquetas.generateLabels;
      etiquetas.generateLabels = chart => base(chart).flatMap(item => (item.datasetIndex !== 0 ? [item] : [
        Object.assign({}, item, { text: `${nombre} fuera de la banda`, fillStyle: color, strokeStyle: color }),
        Object.assign({}, item, { text: 'Dentro', fillStyle: COLORES_GRAFICO.gris,
                                  strokeStyle: COLORES_GRAFICO.gris })
      ]));
      grafico.update('none');
      return grafico;
    }

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
        const rho1 = calcularACF(y, 1)[0];
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'media', valor: fmt(media(y)) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) },
          { etiqueta: 'ρ̂₁', valor: fmt(rho1, 4) }
        ]);
        ariaLienzo(canvas, `Caudal del Nilo ${diferencias(d)}, de ${etiquetas[0]} a ` +
          `${etiquetas[etiquetas.length - 1]}: ${y.length} valores, media ${fmt(media(y))}, ` +
          `varianza ${fmt(varianzaDe(y))}, autocorrelación del rezago 1 ${fmt(rho1, 4)}`);
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
      const etiquetas = aniosDesde(SERIES_CAP4.nilo.inicio[0], malla.n, 0);

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
      // En el escritorio el área de la tasa medía 94 px y la recta del 5 %
      // quedaba a 4.7 px del 0: ahora 150 o más, como en el teléfono.
      const ALTOS_CURVA = { estrecho: '280px', ancho: '260px' };

      function pintar() {
        const b = params.beta;
        const y = ruido.map((v, i) => v - (i + 1 >= malla.posicion ? b : 0));
        if (gSerie) gSerie.destroy();
        // El rótulo de encima ya dice «ruido blanco + escalón»: la leyenda solo
        // nombra el descenso, y así cabe en un teléfono.
        gSerie = lineaSimple(cSerie, etiquetas, y,
          b === 0 ? 'Sin escalón' : `Descenso de ${fmt(b, 0)} en ${etiquetas[malla.posicion - 1]}`,
          COLORES_GRAFICO.primario, {
            scales: escalasLinea('Nivel simulado'),
            onResize: (g, t) => compactar(g, t.width)
          });
        compactar(gSerie, gSerie.width);
        gSerie.update('none');
        ariaLienzo(cSerie, `Ruido blanco simulado, de ${etiquetas[0]} a ${etiquetas[etiquetas.length - 1]}, ` +
          (b === 0 ? 'sin escalón' : `con un descenso de ${fmt(b, 0)} desde ${etiquetas[malla.posicion - 1]}`) +
          `: ${y.length} valores, media ${fmt(media(y))}`);

        const tasa = interpolar(b, 'kpss_rechaza');
        const tasa12 = interpolar(b, 'kpss_rechaza_l12');
        if (!gCurva) {
          // En el teléfono las cinco entradas ocupaban tres renglones: sin el
          // «con» y con los rótulos de las dos rectas más cortos caben en dos.
          const corto = cCurva.parentNode.clientWidth < ESTRECHO;
          gCurva = crearGraficoLinea(cCurva, [], [
            {
              label: corto ? 'KPSS ℓ = 4 (R)' : 'KPSS con ℓ = 4 (R)',
              data: curva('kpss_rechaza'),
              borderColor: COLORES_GRAFICO.secundario,
              backgroundColor: 'rgba(255, 102, 0, 0.12)',
              borderWidth: 2, pointRadius: 3, fill: true
            },
            {
              label: corto ? 'KPSS ℓ = 12' : 'KPSS con ℓ = 12',
              data: curva('kpss_rechaza_l12'),
              borderColor: COLORES_GRAFICO.terciario,
              borderWidth: 1.8, pointRadius: 2, fill: false
            },
            {
              label: corto ? '5 % nominal' : 'Nivel nominal 5 %',
              data: [{ x: 0, y: 5 }, { x: 300, y: 5 }],
              borderColor: COLORES_GRAFICO.gris,
              borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, fill: false
            },
            {
              label: 'β elegido',
              data: [],
              borderColor: COLORES_GRAFICO.primario,
              backgroundColor: COLORES_GRAFICO.primario,
              // clip: false: en β = 0 y en β ≥ 200 el marcador cae sobre el
              // borde del área (el 0 % del eje, el 100 %) y salía cortado.
              pointRadius: 6, pointHoverRadius: 7, showLine: false, clip: false
            },
            {
              label: corto ? `Nilo ${fmt(malla.delta_del_nilo, 1)}` : `Nilo (${fmt(malla.delta_del_nilo, 1)})`,
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
        ariaLienzo(cCurva, `Tasa de rechazo de KPSS al 5 % frente al tamaño del descenso, de ` +
          `${fmt(betas[0], 0)} a ${fmt(betas[betas.length - 1], 0)}: ` +
          `con |β| = ${fmt(b, 0)} rechaza el ${fmt(100 * tasa, 1)} % de las réplicas con ℓ = 4 y el ` +
          `${fmt(100 * tasa12, 1)} % con ℓ = 12; el descenso del Nilo está en ${fmt(malla.delta_del_nilo, 1)}`);

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
      // En el escritorio la ACF y la PACF medían 75 px de dibujo y las barras de
      // 0.21 a 0.24 quedaban a 1–2 px de la banda: ahora, 145.
      const ALTOS_BARRAS = { estrecho: '240px', ancho: '250px' };

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = ident[claves[params.d]];
        const y = diferenciarVeces(SERIES_CAP4.nilo.valores, d);
        [gSerie, gAcf, gPacf].forEach(g => { if (g) g.destroy(); });
        gSerie = lineaSimple(cSerie, aniosDesde(SERIES_CAP4.nilo.inicio[0], y.length, d), y,
          `${nabla(d)}Nilo`,
          d === 1 ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.primario,
          { scales: escalasLinea(d === 0 ? UNIDAD_NILO : `Diferencia (${UNIDAD_NILO})`) });
        gAcf = resaltarFueraDeBanda(barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS), info.acf, info.banda, COLORES_GRAFICO.primario, 'ACF');
        gPacf = resaltarFueraDeBanda(barrasCompactas(crearGraficoBarras(cPacf, REZAGOS, info.pacf, {
          etiqueta: 'PACF muestral', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_BARRAS), info.pacf, info.banda, COLORES_GRAFICO.terciario, 'PACF');
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
        const cual = `la serie del Nilo ${diferencias(d)}`;
        ariaLienzo(cSerie, `Serie del Nilo ${diferencias(d)}: ${y.length} valores, de ${fmt(Math.min(...y), 0)} a ` +
          `${fmt(Math.max(...y), 0)}, media ${fmt(media(y))}`);
        ariaLienzo(cAcf, descripcionCorrelograma('ACF muestral', cual, info.acf, info.banda));
        ariaLienzo(cPacf, descripcionCorrelograma('PACF muestral', cual, info.pacf, info.banda));
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
      // En el escritorio la ACF de residuales medía 105 px de dibujo; el ΔAICc
      // gana además un renglón, porque los rótulos con «↑74» van en dos.
      const ALTOS_RESIDUALES = { estrecho: '250px', ancho: '240px' };
      const ALTOS_AICC = { estrecho: '240px', ancho: '250px' };

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
          ariaLienzo(cAcf, `Sin gráfico de residuales: el ARIMA(${params.p},${params.d},${params.q}) no converge`);
          ariaLienzo(cAicc, `AICc de los ${hermanos.length} modelos con d = ${params.d} que sí convergen; ` +
            `el ARIMA(${params.p},${params.d},${params.q}) elegido no converge`);
          return;
        }

        const nEf = m.n_efectivo;
        gAcf = barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, m.acf_residuales, {
          etiqueta: 'ACF de los residuales',
          color: m.ljung_box_p > 0.05 ? COLORES_GRAFICO.primario : '#b91c1c',
          lineas: lineasBanda(nEf), tituloX: 'Rezago k'
        }), ALTOS_RESIDUALES);
        ariaLienzo(cAcf, descripcionCorrelograma('ACF', `los residuales del ${m.etiqueta}`,
          m.acf_residuales, banda(nEf)));

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
        // Erguido, los nueve rótulos de siete caracteres necesitan ~460 px: entre
        // 421 y 455 se tocaban (hueco de −1 px a 421).
        const tumbado = gAicc.width < 460;
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

      function pintar() {
        const pasos = pasosActuales();
        const hasta = Math.min(Math.max(1, Math.round(params.paso)), pasos.length);
        const visibles = pasos.slice(0, hasta);
        const actual = pasos[hasta - 1];

        if (grafico) grafico.destroy();
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
        // La cruz se dibuja en TECHO, que no es un AICc: su tooltip dice solo «∞».
        const tt = grafico.options.plugins.tooltip;
        const etiquetaPorDefecto = Chart.defaults.plugins.tooltip.callbacks.label;
        tt.callbacks = Object.assign({}, tt.callbacks, {
          label(item) {
            return item.dataset.pointStyle === 'crossRot' ? 'AICc = ∞ (descartado)'
                                                          : etiquetaPorDefecto.call(this, item);
          }
        });
        lineaCompacta(grafico, ALTOS_TRAZA);

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
        ariaLienzo(canvas, `AICc de los modelos que evalúa la búsqueda ` +
          `${params.exhaustiva ? 'exhaustiva' : 'escalonada'}, hasta el paso ${hasta} de ${pasos.length}. ` +
          `Mejoras del mejor AICc: ${mejorados}. Descartados con AICc infinito: ` +
          `${visibles.filter(p => p.infinito).length}. Mejor AICc hasta aquí: ` +
          (actual.mejor_hasta_aqui === null ? 'ninguno todavía' : fmt(actual.mejor_hasta_aqui, 3)));

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
        ariaLienzo(cSerie, `Serie del Nilo ${diferencias(d)}: ${y.length} valores, de ` +
          `${fmt(Math.min(...y), 0)} a ${fmt(Math.max(...y), 0)}, varianza ${fmt(fila.varianza)}`);

        // La varianza real sobre un eje logarítmico: las marcas se leen en
        // unidades de varianza y la razón entre barras es la que se ve.
        gVar = crearGraficoBarras(cVar, tabla.map(f => `d = ${f.d}`),
          tabla.map(f => f.varianza), {
            etiqueta: 'Varianza de la serie diferenciada', color: COLORES_GRAFICO.gris
          });
        gVar.data.datasets[0].backgroundColor = tabla.map(
          f => f.d === d ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        // Las marcas, en 1 y 3 por potencia de diez (10 000, 30 000, 100 000,
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
          : { etiqueta: 'diagnóstico', valor: d === 1 ? 'raíz MA fuera del círculo' : 'sin diferenciar' });
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
      // En el teléfono la leyenda ocupaba cuatro renglones (98 px) de un lienzo de
      // 257: con la tipografía compacta y un rótulo más corto caben en dos.
      const ALTOS_FORMA = { estrecho: '300px', ancho: '280px' };

      function pintar() {
        const f = formas[params.modelo];
        if (grafico) grafico.destroy();

        const corto = canvas.parentNode.clientWidth < ESTRECHO;
        const datasets = [{
          label: corto ? 'Observado' : 'Caudal observado',
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
          scales: escalasLinea(`Caudal (${UNIDAD_NILO})`)
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
          (params.bandas ? `; el intervalo del 95 % va de ${fmt(f.lo95[H - 1])} a ${fmt(f.hi95[H - 1])} en el último año` : ''));
      }

      const controles = raiz.querySelector('.simulador-controles');
      crearSelector(controles, {
        clave: 'modelo', etiqueta: 'Modelo',
        opciones: [
          { valor: 'd0', texto: 'ARIMA(1,0,1) con media — vuelve a la media' },
          { valor: 'd1', texto: 'ARIMA(1,1,1) sin constante — se aplana' },
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
      // El gráfico de σ_h medía 74 px de dibujo a 1200 px y 52 a 800: la curva
      // que hay que comparar con la discontinua ocupaba una franja de 20 px.
      const ALTOS_PSI = { estrecho: '240px', ancho: '240px' };
      const ALTOS_SIGMA = { estrecho: '260px', ancho: '240px' };

      function pintar() {
        const h = Math.round(params.h);

        if (gPsi) gPsi.destroy();
        gPsi = barrasCompactas(crearGraficoBarras(cPsi,
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
          `${fmt(inter.psi[inter.psi.length - 1], 3)}; ` +
          (h === 1 ? 'el primero, en naranja, entra en σₕ' : `los ${h} primeros, en naranja, entran en σₕ`));

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
              // clip: false: en h = 1 y h = 30 el marcador cae sobre el borde del
              // área y salía cortado.
              label: '', data: [], showLine: false, pointRadius: 5, clip: false,
              borderColor: COLORES_GRAFICO.secundario, backgroundColor: COLORES_GRAFICO.secundario
            },
            {
              label: '', data: [], showLine: false, pointRadius: 5, clip: false,
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
            scales: escalasLinea(`σ (${UNIDAD_NILO})`, {
              offset: true,
              afterBuildTicks: eje => { marcasConUltimo(eje, { maxMarcas: 12 }); },
              title: { display: true, text: 'Horizonte h', font: { family: 'Montserrat', size: 11 } },
              ticks: { font: { family: 'Fira Code', size: 10 } }
            }),
            onResize: (g, t) => compactar(g, t.width, ALTOS_SIGMA)
          });
          gSigma.options.scales.y.min = 0;
          compactar(gSigma, gSigma.width, ALTOS_SIGMA);
        }
        gSigma.data.datasets[2].data = inter.sigma_h.map((v, i) => (i === h - 1 ? v : null));
        gSigma.data.datasets[3].data = raizH.map((v, i) => (i === h - 1 ? v : null));
        gSigma.update('none');
        ariaLienzo(cSigma, `Desviación del error de pronóstico σₕ frente al horizonte, de h = 1 a ${H}, y ` +
          `la de una caminata aleatoria con la misma σ: con h = ${h}, σₕ = ${fmt(inter.sigma_h[h - 1], 3)} ` +
          `y σ√h = ${fmt(inter.sigma * Math.sqrt(h), 1)}`);

        actualizarLectura(lectura, [
          { etiqueta: 'h', valor: h },
          { etiqueta: 'ψₕ₋₁', valor: fmt(inter.psi[h - 1], 4) },
          { etiqueta: 'σ', valor: fmt(inter.sigma, 3) },
          { etiqueta: 'σₕ', valor: fmt(inter.sigma_h[h - 1], 3) },
          // σ llega redondeada a tres decimales: σ√h, a uno (a h = 30, 778.0, como la prosa).
          { etiqueta: 'σ√h', valor: fmt(inter.sigma * Math.sqrt(h), 1) },
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
      // La ACF medía 75 px de dibujo a 1200 px: el «por poco» del ρ̂₈ frente a la
      // banda eran ~1 px.
      const ALTOS_ACF = { estrecho: '240px', ancho: '250px' };

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = d === 0 ? TRM.identificacion.cruda : TRM.identificacion.d1;
        const y = diferenciarVeces(SERIES_CAP4.trm.valores, d);

        [gSerie, gAcf].forEach(g => { if (g) g.destroy(); });
        const meses = mesesDesde(inicio[0], inicio[1] + d, y.length);
        gSerie = lineaSimple(cSerie, meses, y,
          d === 0 ? 'TRM mensual (COP/USD)' : '∇TRM',
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario,
          { scales: escalasLinea(d === 0 ? 'COP por USD' : 'Cambio mensual (COP por USD)') });
        gAcf = resaltarFueraDeBanda(barrasCompactas(crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        }), ALTOS_ACF), info.acf, info.banda, COLORES_GRAFICO.primario, 'ACF');
        const cual = d === 0 ? 'la TRM en niveles' : 'la TRM diferenciada una vez';
        ariaLienzo(cSerie, `Serie de ${cual}, de ${meses[0]} a ${meses[meses.length - 1]}: ${y.length} meses, ` +
          `de ${fmt(Math.min(...y))} a ${fmt(Math.max(...y))} pesos por dólar`);
        ariaLienzo(cAcf, descripcionCorrelograma('ACF muestral', cual, info.acf, banda(info.n)));

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

      // En el teléfono la leyenda ocupaba cuatro renglones (98 px) y quedaban 112
      // px de dibujo: con la tipografía compacta caben en dos.
      const ALTOS_ABANICO = { estrecho: '300px', ancho: '280px' };

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
          scales: escalasLinea('COP por USD')
        });
        lineaCompacta(grafico, ALTOS_ABANICO);

        const semi = Z95 * sigma * Math.sqrt(H);
        actualizarLectura(lectura, [
          { etiqueta: 'σ̂', valor: fmt(sigma) },
          { etiqueta: 'Pronóstico', valor: `${fmt(ultimo)} — el último observado, a cualquier horizonte` },
          { etiqueta: `σ a ${H} ${H === 1 ? 'mes' : 'meses'}`, valor: `${fmt(sigma * Math.sqrt(H))} = σ̂·√${H}` },
          { etiqueta: 'Intervalo 95 %', valor: `[${fmt(ultimo - semi)}, ${fmt(ultimo + semi)}]` },
          { etiqueta: 'Semiancho sobre el nivel', valor: `±${fmt(100 * semi / ultimo, 1)} %` },
          { etiqueta: 'Frente al horizonte a un mes', valor: `×${fmt(Math.sqrt(H), 2)} — y sin techo` }
        ]);
        ariaLienzo(canvas, `Últimos ${VISIBLES} meses de la TRM y pronóstico de caminata aleatoria a ${H} ` +
          `${H === 1 ? 'mes' : 'meses'}: ` +
          `recta horizontal en ${fmt(ultimo)} con un intervalo del 95 % de ${fmt(ultimo - semi)} a ` +
          `${fmt(ultimo + semi)} que se abre como la raíz del horizonte`);
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
      const ALTOS_PUENTE = { estrecho: '240px', ancho: '240px' };

      function pintar() {
        const esNo = params.modelo === 'no';
        const info = esNo ? PUENTE.no_estacional : PUENTE.estacional;
        const acf = info.acf_residuales;

        if (grafico) grafico.destroy();
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

    // ACF de la pregunta 6 de la autoevaluación: exportaciones de bienes y servicios de Chile
    // (% del PIB, 1960-2017; tsibbledata::global_economy), sin diferenciar, rezagos 1 a 20.
    // Salen de diagnostico/cap4/comprobaciones/r5_cifras.R, etiqueta [P6-01].
    const ACF_P6 = [0.946, 0.868, 0.802, 0.734, 0.662, 0.593, 0.526, 0.469, 0.429, 0.392,
      0.344, 0.291, 0.238, 0.198, 0.178, 0.164, 0.137, 0.100, 0.070, 0.039];
    const N_P6 = 58;

    // Autoevaluación del capítulo (ronda R5, 2026-11-23). Procedencia de las cifras, en
    // diagnostico/cap4/comprobaciones/r5_cifras.out: P1, etiquetas P1-01 a P1-03 (pasajeros aéreos
    // de Australia, fpp3::aus_airpassengers); P2, P2-01 a P2-03; P5, P5-01 a P5-04 (datasets::beaver2);
    // P6 y P7, P6-01 a P7-03 (exportaciones de Chile); P8, P8-01 a P8-04 (importaciones de Perú).
    // Las de la P3 son las del puente al Capítulo 5 y las del Nilo de la P4, las del Módulo 9.
    AUTOEVALUACIONES['cap4'] = [
      {
        tipo: 'opcion',
        modulo: 6,
        pregunta: 'Sobre los pasajeros aéreos anuales de Australia entre 1970 y 2016 ($n = 47$), el mejor ARIMA sin constante de la rejilla con $d = 1$ tiene AICc $= 204.28$, y el mejor con $d = 2$, AICc $= 198.32$. ¿Qué dice esa comparación sobre $d$?',
        pista: 'Mira de dónde sale un AICc: vuelve a su fórmula en el Módulo 6 y sigue qué cambia en ella al pasar de $d = 1$ a $d = 2$.',
        opciones: [
          {
            texto: 'Que conviene $d = 2$: seis puntos de AICc son una diferencia clara entre dos modelos.',
            correcta: false,
            retro: 'Seis puntos serían una diferencia clara dentro de un mismo $d$. Aquí no: el segundo AICc es la verosimilitud de <strong>otros datos</strong>, con una observación menos, y un valor menor no significa un modelo mejor.'
          },
          {
            texto: 'Nada: cada AICc se calcula sobre datos distintos, y solo se comparan con un mismo $d$.',
            correcta: true,
            retro: 'El primero se calcula sobre $n^{*} = 46$ diferencias y el segundo sobre $45$ segundas diferencias: <strong>datos distintos</strong>. En esta serie la duda sobre $d$ es real —KPSS pide dos diferencias, y ADF y PP, una—, pero no se resuelve restando dos AICc.'
          },
          {
            texto: 'Que conviene $d = 1$: a igualdad de ajuste, se prefiere el modelo con menos diferencias.',
            correcta: false,
            retro: 'No diferenciar más de lo necesario es una cautela razonable, y el Módulo 8 explica por qué. Pero no sale de esta comparación: aquí no hay «igualdad de ajuste» que valorar, porque los dos AICc no miden lo mismo.'
          },
          {
            texto: 'Que hay que decidir con el BIC, que penaliza más y sí se compara entre distintos $d$.',
            correcta: false,
            retro: 'El BIC tiene el mismo problema: también parte de $-2\\log L$, y esa verosimilitud se calcula sobre $n^{*} = n - d$ observaciones. Cambiar de criterio no arregla que los datos sean distintos.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 9,
        pregunta: 'Un ARIMA($1,1,0$) tiene $\\phi = 0.5$ y $\\sigma = 2$. ¿Cuánto vale $\\sigma_3$, la desviación típica del error de pronóstico a tres pasos? Da dos decimales.',
        pista: 'Para los pesos $\\psi$, escribe primero el modelo sobre $y_t$, como en el desarrollo del Módulo 1, y cuenta cuántos pesos entran en $\\sigma_3$. Conserva al menos tres decimales en los pasos intermedios.',
        respuesta: 5.02,
        tolerancia: 0.011,
        retroAcierto: 'Sobre $y_t$ el modelo es un AR(2) con $\\phi^{*} = (1.5,\\ -0.5)$, así que $\\psi_0 = 1$, $\\psi_1 = 1.5$ y $\\psi_2 = 1.5 \\times 1.5 - 0.5 = 1.75$. Entonces $\\sigma_3 = 2\\sqrt{1 + 1.5^2 + 1.75^2} = 2\\sqrt{6.3125} = 5.02$.',
        retroFallo: 'Sobre $y_t$ el modelo es un AR(2) con $\\phi^{*} = (1.5,\\ -0.5)$: $\\psi_0 = 1$, $\\psi_1 = 1.5$ y $\\psi_2 = 1.75$, y $\\sigma_3 = 2\\sqrt{1 + 2.25 + 3.0625} = 5.02$. Si te salió $2.29$, usaste $\\psi_j = \\phi^{\\,j}$, los pesos del AR(1) sin la diferencia; $3.46$ es tomar todos los pesos iguales a $1$; $4.61$, olvidar $\\psi_0$; $4.12$, sumar los pesos sin elevarlos al cuadrado; $6.27$, sumar un peso de más, $\\psi_3$; $2.51$, olvidar $\\sigma$; y $5.00$, redondear la raíz a $2.5$ antes de multiplicar.'
      },
      {
        tipo: 'grafico',
        modulo: 10,
        alto: 250,
        descripcionGrafico: describirBarrasQuiz(
          'Función de autocorrelación de los residuales de un ARIMA ajustado a una serie mensual',
          PUENTE.no_estacional.acf_residuales, PUENTE.no_estacional.banda),
        pregunta: 'Esta es la ACF de los residuales de un ARIMA ajustado a una serie mensual. ¿Qué hay que hacer?',
        pista: 'No te quedes en cuántas barras salen de la banda: fíjate en cuáles son.',
        dibujar: canvas => crearGraficoBarras(canvas,
          etiquetasRezago(PUENTE.no_estacional.acf_residuales.length),
          PUENTE.no_estacional.acf_residuales, {
            etiqueta: 'ACF de los residuales', color: '#b91c1c',
            lineas: lineasBanda(PUENTE.n), tituloX: 'Rezago k'
          }),
        opciones: [
          {
            texto: 'Aumentar $q$ hasta que todas las barras queden dentro de la banda de confianza.',
            correcta: false,
            retro: 'Funcionaría en el sentido técnico, pero haría falta $q = 24$ para alcanzar el rezago 24: veinticuatro parámetros para describir un patrón que se repite cada doce meses. Un modelo estacional recoge lo mismo con dos.'
          },
          {
            texto: 'Diferenciar una vez más: una autocorrelación tan alta indica no estacionariedad.',
            correcta: false,
            retro: 'Diferenciar de nuevo en el rezago 1 no toca el patrón de los rezagos 12 y 24, y además puede dejar en el MA la raíz unitaria que estudió el Módulo 8. Lo que hace falta aquí es una diferencia <strong>estacional</strong>, $\\nabla_{12}$, que es otra cosa.'
          },
          {
            texto: 'Pasar a un modelo estacional: lo que sobra está en los rezagos múltiplos de 12.',
            correcta: true,
            retro: '$\\hat\\rho_{12} = 0.72$ y $\\hat\\rho_{24} = 0.67$, frente a una banda de $0.163$: la estructura que sobra es estacional. Subir $q$ hasta 24 la cubriría con dos docenas de parámetros; un SARIMA lo hace con dos. Es el Capítulo 5.'
          },
          {
            texto: 'Nada: casi todas las barras están dentro de la banda, y el modelo es adecuado.',
            correcta: false,
            retro: 'Contar cuántas barras se salen no basta, y aquí las que se salen lo hacen por un factor de cuatro. Ljung–Box(24) da $Q = 222.4$ con $p < 10^{-6}$: el rechazo es rotundo. Un patrón sistemático en pocos rezagos es peor señal que ruido repartido en muchos.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 5,
        pregunta: 'Marca <strong>todas</strong> las afirmaciones correctas sobre la constante de un modelo ARIMA.',
        pista: 'Para cada afirmación, piensa qué grado tiene la tendencia que genera la constante con ese $d$, y qué le pasa al pronóstico cuando la constante no está.',
        opciones: [
          {
            texto: 'Con $d = 1$, la deriva $\\mu_w = c/\\phi(1)$ es el incremento medio por período: una tendencia lineal.',
            correcta: true,
            retro: 'Tomando esperanzas en la ecuación, $\\mu_w = c/\\phi(1)$ es la media de $\\nabla y_t$: lo que la serie sube o baja en promedio cada período, es decir, una pendiente. Es lo que <code>forecast</code> llama deriva.'
          },
          {
            texto: 'Sin constante, un modelo con $d = 2$ pronostica a largo plazo una parábola, no una línea recta.',
            correcta: false,
            retro: 'Sin constante, con $d = 2$ el pronóstico acaba en una recta: la segunda diferencia del pronóstico tiende a cero. La parábola necesitaría una constante con $d = 2$.'
          },
          {
            texto: 'Con $d = 1$ y sin deriva, el pronóstico se aplana en un nivel, que puede no ser el último dato.',
            correcta: true,
            retro: 'Sin deriva no hay pendiente a largo plazo y el pronóstico se aplana; pero la parte ARMA lo mueve durante unos pasos, y el nivel al que llega no es, en general, el último dato. En el Nilo parte de $740$ y se aplana en $842.17$.'
          },
          {
            texto: 'Con $d \\ge 2$, <code>forecast::Arima</code> avisa y no ajusta la deriva, aunque se le pida.',
            correcta: true,
            retro: 'Es lo que hace: avisa de que no ajusta la deriva con dos o más diferencias. Una constante con $d = 2$ generaría una tendencia cuadrática, y el Módulo 5 explica por qué no conviene extrapolarla.'
          },
          {
            texto: 'En un ARIMA($p,0,q$), el <code>intercept</code> que da R es la constante $c$ de la ecuación, no la media.',
            correcta: false,
            retro: 'Es al revés: lo que R llama <code>intercept</code> en un modelo con $d = 0$ es la media $\\mu$ del proceso. La constante de la ecuación es $c = \\mu\\,\\phi(1)$, y solo coinciden si $p = 0$.'
          }
        ],
        retroAcierto: 'Las que hablan de la deriva con $d = 1$, del pronóstico que se aplana y de lo que hace <code>forecast::Arima</code> con $d \\ge 2$. Las dos falsas son las que el capítulo desmiente midiendo: con $d = 2$ y sin constante el pronóstico termina en una <strong>recta</strong>, y el <code>intercept</code> de R <strong>es</strong> la media del proceso, pese al nombre.',
        retroFallo: 'Las correctas son las que hablan de la deriva con $d = 1$, del pronóstico que se aplana cuando no hay deriva y de lo que hace <code>forecast::Arima</code> con $d \\ge 2$. Abajo va la explicación de cada opción que quedó mal juzgada.'
      },
      {
        tipo: 'opcion',
        modulo: 3,
        pregunta: '<code>beaver2</code> trae la temperatura corporal de un castor medida cada 10 minutos (100 lecturas). Desde la lectura 39, cuando el animal sale de su refugio, la media sube unos $0.8$ °C. Sobre la serie completa, KPSS rechaza la estacionariedad ($p < 0.01$) y ADF no rechaza la raíz unitaria ($p = 0.57$). ¿Qué conviene hacer antes de fijar $d$?',
        pista: 'Repasa en el Módulo 3 qué contrasta cada prueba y qué le pasó a cada una en el experimento del cambio de nivel.',
        opciones: [
          {
            texto: 'Diferenciar una vez: las dos pruebas coinciden, y eso cierra la discusión sobre $d$.',
            correcta: false,
            retro: 'Que coincidan no las hace fiables aquí. El experimento del Módulo 3 mostró que un escalón hace rechazar a KPSS y también impide rechazar al ADF de <code>adf.test</code>: con el salto dentro, las dos pueden estar respondiendo al escalón y no a una raíz unitaria.'
          },
          {
            texto: 'Ajustar el salto como un escalón y volver a examinar lo que queda de la serie.',
            correcta: true,
            retro: 'Con el salto dentro, las pruebas no separan una raíz unitaria de un cambio de nivel (Módulo 3). Quitado el escalón ($0.81$ °C), lo que queda sigue muy autocorrelacionado ($r_1 = 0.78$), y probadas en cada tramo, a un lado y otro de la lectura 39, las tres pruebas siguen pidiendo una diferencia: la discusión sobre $d$ no termina ahí, pero ya es sobre la serie, y no sobre el salto.'
          },
          {
            texto: 'Diferenciar dos veces: una diferencia para la raíz unitaria y otra para el salto.',
            correcta: false,
            retro: 'Una sola diferencia ya convierte un escalón en un único valor atípico: no hace falta otra para «quitarlo». Y diferenciar de más deja una raíz unitaria en la parte MA (Módulo 8). Antes de subir $d$ conviene volver al gráfico.'
          },
          {
            texto: 'No diferenciar: un salto con causa conocida prueba que no hay raíz unitaria.',
            correcta: false,
            retro: 'El salto puede bastar para que KPSS rechace, pero no dice nada de lo que hay a cada lado: quitado el escalón, lo que queda tiene $r_1 = 0.78$ y hay que examinarlo. Fijar $d = 0$ sin mirarlo es el mismo error que diferenciar sin mirar el gráfico, en sentido contrario.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 4,
        alto: 250,
        descripcionGrafico: describirBarrasQuiz('Función de autocorrelación muestral de una serie anual sin diferenciar',
          ACF_P6, banda(N_P6)),
        pregunta: 'Esta es la ACF de las exportaciones de bienes y servicios de Chile, en porcentaje del PIB (58 datos anuales, de 1960 a 2017), <strong>sin diferenciar</strong>. ¿Qué se puede concluir sobre $p$ y $q$?',
        pista: 'Antes de contar barras, mira la forma en que bajan.',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS, ACF_P6, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(N_P6), tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Que es un AR de orden alto, porque hay muchas barras fuera de la banda.',
            correcta: false,
            retro: 'Un AR estacionario tiene una ACF que decae, de forma exponencial u oscilante (Capítulo 3), y esa lectura presupone que la serie es estacionaria. Con una caída tan lenta, lo primero es preguntarse si el nivel de la serie se mueve: leer órdenes aquí es confundir la no estacionariedad con dinámica.'
          },
          {
            texto: 'Que es un MA($q$), con $q$ igual al número de barras fuera de la banda.',
            correcta: false,
            retro: 'Un MA($q$) tiene la ACF teórica nula después del rezago $q$: un corte, no un descenso gradual. Aquí no hay corte por ninguna parte.'
          },
          {
            texto: 'Que hace falta $d = 2$, porque las barras tardan más de diez rezagos en entrar.',
            correcta: false,
            retro: 'Que la serie no parezca estacionaria es razonable, pero la ACF no dice cuántas diferencias hacen falta: la lentitud de la caída no mide $d$. Eso lo deciden el gráfico, las pruebas y los síntomas de haber diferenciado de más (Módulo 3).'
          },
          {
            texto: 'Nada todavía: una caída tan lenta obliga a decidir $d$ antes de leer $p$ y $q$.',
            correcta: true,
            retro: 'Una ACF que baja despacio y sin cortar —aquí $0.946,\\ 0.868,\\ 0.802,\\dots$, fuera de la banda hasta el rezago 12— es compatible con una serie no estacionaria. La tabla de identificación se lee sobre la serie ya estacionaria: primero se decide $d$, y después se leen $p$ y $q$ en la ACF y la PACF de la serie diferenciada. Con $d = 1$, en esta serie solo sale de la banda el rezago 1 ($0.270$).'
          }
        ]
      },
      {
        tipo: 'opcion',
        modulo: 7,
        pregunta: 'Sobre esa misma serie de exportaciones de Chile, <code>auto.arima</code> devuelve un ARIMA($0,1,2$) con deriva, AICc $265.85$. La búsqueda exhaustiva encuentra un ARIMA($0,1,1$) sin deriva con AICc $264.32$, y su tercer clasificado tiene $266.26$. ¿Qué se concluye?',
        pista: 'Mide primero cuánto separa el AICc a esos tres modelos, y busca en el Módulo 7 qué hace el capítulo con distancias de ese tamaño.',
        opciones: [
          {
            texto: 'Que la búsqueda escalonada falló, y su modelo debe sustituirse por el de la exhaustiva.',
            correcta: false,
            retro: 'La escalonada explora un vecindario y no garantiza el mínimo: aquí se quedó a $1.53$ puntos de él, y por eso conviene contrastarla con la exhaustiva. Pero una distancia así no descarta a nadie: este capítulo toma por convención que diferencias menores que $2$ puntos no distinguen modelos.'
          },
          {
            texto: 'Que el ARIMA($0,1,1$) es el modelo verdadero, porque es el mínimo de la búsqueda completa.',
            correcta: false,
            retro: 'Ser el mínimo de la búsqueda completa dice que es el mejor según el AICc de los que la búsqueda pudo ajustar, no que sea el verdadero. Y hay otro modelo a $1.53$ puntos y otro a $1.94$: el criterio apenas los separa.'
          },
          {
            texto: 'Que hay tres modelos que el AICc apenas separa, y conviene decirlo al dar el resultado.',
            correcta: true,
            retro: 'Del primero al tercero hay $1.94$ puntos, menos de los $2$ que este capítulo toma por convención como indistinguibles. La salida de una línea de <code>auto.arima</code> no comunica esa incertidumbre; <code>trace = TRUE</code> sí.'
          },
          {
            texto: 'Que, con menos de $2$ puntos entre ellos, se elige sin más el de menos parámetros de los tres.',
            correcta: false,
            retro: 'La parsimonia es un criterio razonable para desempatar, y llevaría al ARIMA($0,1,1$), que es defendible. Pero lo primero es <strong>reconocer que hay un empate</strong>: elegir por parsimonia sin decir que había tres candidatos oculta la misma incertidumbre.'
          }
        ]
      },
      {
        tipo: 'opcion',
        modulo: 8,
        pregunta: 'Importaciones de bienes y servicios de Perú, en porcentaje del PIB (58 datos anuales). Un MA(1) sin media ajustado a $\\nabla y_t$ da $\\hat\\theta = -0.288$ y pasa Ljung–Box(10) ($p = 0.43$). Ajustado a $\\nabla^2 y_t$ da $\\hat\\theta = -1.000$ y también lo pasa ($p = 0.17$). La varianza de $\\nabla y_t$ es $5.12$, y la de $\\nabla^2 y_t$, $13.18$. ¿Qué se concluye sobre $d$?',
        pista: 'Los dos modelos pasan Ljung–Box. Repasa todo lo que el Módulo 8 enseña a mirar en un modelo ajustado.',
        opciones: [
          {
            texto: 'Que $d = 2$ sobra: con $\\hat\\theta = -1$, la raíz MA cae sobre el círculo y deshace la diferencia.',
            correcta: true,
            retro: 'La raíz de $1 + \\hat\\theta B$ es $-1/\\hat\\theta$, de módulo $1.000$ con tres decimales: el polinomio MA es, en la práctica, $(1 - B)$, el mismo operador de diferencia, y cancela la segunda. Hay una comprobación: el $\\hat\\sigma^2$ de ese MA(1) es $5.12$, la varianza de $\\nabla y_t$. El modelo ha vuelto a la serie diferenciada una sola vez.'
          },
          {
            texto: 'Que $d = 2$ también es válido: sus residuales pasan Ljung–Box, igual que los de $d = 1$.',
            correcta: false,
            retro: 'Pasar Ljung–Box no basta: un modelo con una diferencia de más puede dejar residuales sin estructura, porque su parte MA deshace la diferencia que sobra. El diagnóstico incluye las raíces, y la de este MA(1) tiene módulo $1.000$.'
          },
          {
            texto: 'Que $d = 1$ es mejor, porque con la segunda diferencia la varianza sube de $5.12$ a $13.18$.',
            correcta: false,
            retro: 'La conclusión es la buena y el argumento no sirve. Que la varianza suba o baje al diferenciar repite lo que dice $r_1$ (Módulo 2.7) y no decide $d$: hay series estacionarias en las que diferenciar reduce la varianza. Lo que delata la diferencia sobrante es la raíz MA sobre el círculo.'
          },
          {
            texto: 'Que hay que comparar el AICc de los dos modelos y quedarse con el $d$ del menor.',
            correcta: false,
            retro: 'Los AICc de modelos con distinto $d$ no se comparan: uno se calcula sobre $57$ observaciones y el otro sobre $56$ (Módulo 6). Y aquí no hace falta ningún criterio: $\\hat\\theta = -1$ ya dice que la segunda diferencia sobra.'
          }
        ]
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
