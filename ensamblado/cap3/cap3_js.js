    // ================================================================
    // Datos y ayudantes del capítulo, tomados del precálculo en R
    // ================================================================
    const PROCESOS = DATOS_CAP3.procesos;
    const MANCHAS = DATOS_CAP3.manchas;
    const RETORNOS = DATOS_CAP3.retornos_trm;
    const TRANSF = DATOS_CAP3.manchas.transformacion;
    const REZAGOS = etiquetasRezago(DATOS_CAP3.max_rezago);
    const REZAGOS_T = etiquetasRezago(DATOS_CAP3.max_rezago_teorico);

    // Cifras con punto decimal, como la prosa. Las lecturas del capítulo
    // usan toFixed(), que ya escribe punto; fmt() hace falta para la tabla
    // ordenable, cuyo componente formatea en es-CO si no se le pasa otro.
    // Los miles se agrupan con un espacio fino solo desde cinco cifras
    // enteras (80 055.01); con cuatro van juntos (1267.51).
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

    function banda(n) { return 1.96 / Math.sqrt(n); }

    function lineasBanda(n) {
      const b = banda(n);
      return [
        { valor: b, etiqueta: 'Banda ±1.96/√T' },
        { valor: -b, etiqueta: '' }
      ];
    }

    // Rojo de lo que no cumple (no estacionario, no invertible, p < 0.05)
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
    // Álgebra de procesos ARMA en el navegador.
    //
    // Son las mismas fórmulas que implementa precalculo/genera_cap3.R.
    // La ACF teórica se obtiene de los pesos psi truncados; contrastada
    // contra ARMAacf() de R sobre los ocho procesos del capítulo, el
    // error máximo es 6.7e-16.
    // ---------------------------------------------------------------

    // psi_j = theta_j + sum_i phi_i psi_{j-i},  psi_0 = 1
    function pesosPsi(ar, ma, n) {
      const psi = new Array(n + 1).fill(0);
      psi[0] = 1;
      for (let j = 1; j <= n; j++) {
        let v = j <= ma.length ? ma[j - 1] : 0;
        for (let i = 1; i <= ar.length; i++) {
          if (j - i >= 0) v += ar[i - 1] * psi[j - i];
        }
        psi[j] = v;
      }
      return psi;
    }

    // pi_j = -phi_j - sum_i theta_i pi_{j-i},  pi_0 = 1
    function pesosPi(ar, ma, n) {
      const pp = new Array(n + 1).fill(0);
      pp[0] = 1;
      for (let j = 1; j <= n; j++) {
        let v = j <= ar.length ? -ar[j - 1] : 0;
        for (let i = 1; i <= ma.length; i++) {
          if (j - i >= 0) v -= ma[i - 1] * pp[j - i];
        }
        pp[j] = v;
      }
      return pp;
    }

    // gamma_k = sum_j psi_j psi_{j+k}  ->  rho_k = gamma_k / gamma_0
    function acfTeorica(ar, ma, maxLag, terminos = 600) {
      const psi = pesosPsi(ar, ma, terminos);
      const g = [];
      for (let k = 0; k <= maxLag; k++) {
        let s = 0;
        for (let j = 0; j + k <= terminos; j++) s += psi[j] * psi[j + k];
        g.push(s);
      }
      return g.slice(1).map(v => v / g[0]);
    }

    // Raíces de phi(B) = 1 - phi1 B - phi2 B^2 (p = 1 o 2). Devuelve el módulo
    // mínimo, si las raíces son complejas y, en ese caso, el pseudo-periodo.
    // Con raíces complejas |B| = 1/sqrt(-phi2), de modo que la condición de
    // estacionariedad se reduce a phi2 > -1.
    function analizarAR(phi1, phi2) {
      if (Math.abs(phi2) < 1e-9) {
        if (Math.abs(phi1) < 1e-9) return { estacionario: true, modulo: Infinity, complejas: false };
        return { estacionario: Math.abs(phi1) < 1, modulo: Math.abs(1 / phi1), complejas: false };
      }
      const disc = phi1 * phi1 + 4 * phi2;
      if (disc < 0) {
        const coseno = Math.min(1, Math.max(-1, phi1 / (2 * Math.sqrt(-phi2))));
        return {
          estacionario: phi2 > -1,
          modulo: 1 / Math.sqrt(-phi2),
          complejas: true,
          periodo: 2 * Math.PI / Math.acos(coseno)
        };
      }
      const r = Math.sqrt(disc);
      const modulo = Math.min(Math.abs((-phi1 + r) / (2 * phi2)),
        Math.abs((-phi1 - r) / (2 * phi2)));
      // Tolerancia: en el borde del triángulo la raíz unitaria sale como
      // 1.0000000000000002 y, sin ella, un proceso con raíz unitaria pasaba por estacionario.
      return { estacionario: modulo > 1 + 1e-9, modulo: modulo, complejas: false };
    }

    // Invertibilidad de theta(B) = 1 + t1 B + t2 B^2. Mismo razonamiento que
    // analizarAR, con los signos del polinomio de medias móviles: con raíces
    // complejas |B| = 1/sqrt(t2), luego basta t2 < 1.
    function esInvertible(t1, t2) {
      if (Math.abs(t2) < 1e-9) return Math.abs(t1) < 1;
      const disc = t1 * t1 - 4 * t2;
      if (disc < 0) return t2 < 1;
      const r = Math.sqrt(disc);
      return Math.min(Math.abs((-t1 + r) / (2 * t2)),
        Math.abs((-t1 - r) / (2 * t2))) > 1 + 1e-9;   // misma tolerancia que analizarAR
    }

    // Simula un ARMA con ruido de semilla fija. Si el proceso es estacionario
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
    // varianzaMuestral(), del armazón heredado del capítulo 2.)

    // Serie a partir de un array simple
    function serieSimple(canvas, valores, etiqueta, color, etiquetasX) {
      const etiq = etiquetasX || valores.map((_, i) => String(i + 1));
      return crearGraficoLinea(canvas, etiq, [{
        label: etiqueta,
        data: valores,
        borderColor: color || COLORES_GRAFICO.primario,
        backgroundColor: color || COLORES_GRAFICO.primario,
        borderWidth: 1.8,
        pointRadius: 0
      }]);
    }

    // Correlograma con dos juegos de barras: teórico (oscuro) y muestral (gris).
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
    }

    // ================================================================
    // M2 · Las cuatro firmas del AR (ACF y PACF teóricas)
    // ================================================================
    SIMULADORES['panel-ar-teorico'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { proceso: 'ar1_pos' };

      const gAcf = crearGraficoBarras(c[0], REZAGOS_T, PROCESOS.ar1_pos.acf_teorica,
        { etiqueta: 'ACF teórica', color: COLORES_GRAFICO.primario, tituloX: 'Rezago k' });
      const gPacf = crearGraficoBarras(c[1], REZAGOS_T, PROCESOS.ar1_pos.pacf_teorica,
        { etiqueta: 'PACF teórica', color: COLORES_GRAFICO.terciario, tituloX: 'Rezago k' });

      function pintar() {
        const p = PROCESOS[params.proceso];
        gAcf.data.datasets[0].data = p.acf_teorica;
        gAcf.update('none');
        gPacf.data.datasets[0].data = p.pacf_teorica;
        gPacf.update('none');
        c[0].setAttribute('aria-label',
          describirBarras(`ACF teórica del ${nombreProceso(p)}, rezagos`, p.acf_teorica));
        c[1].setAttribute('aria-label',
          describirBarras(`PACF teórica del ${nombreProceso(p)}, rezagos`, p.pacf_teorica));

        const filas = [
          { etiqueta: 'Proceso:', valor: `AR(${p.p})` },
          { etiqueta: `PACF en el rezago ${p.p + 1}:`, valor: p.pacf_teorica[p.p].toFixed(4) },
          { etiqueta: 'ρ₁:', valor: p.acf_teorica[0].toFixed(4) },
          { etiqueta: '|raíz| mínima:', valor: p.raices.modulo_min.toFixed(4) },
          { etiqueta: 'raíces:', valor: p.raices.complejas ? 'complejas' : 'reales' }
        ];
        if (p.raices.periodo) {
          filas.push({ etiqueta: 'pseudo-periodo:', valor: `${p.raices.periodo.toFixed(2)} periodos` });
        }
        actualizarLectura(lectura, filas);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'proceso',
        etiqueta: 'Proceso',
        opciones: [
          { valor: 'ar1_pos', texto: 'AR(1), φ = 0.8' },
          { valor: 'ar1_neg', texto: 'AR(1), φ = −0.7' },
          { valor: 'ar2_real', texto: 'AR(2), φ = (0.5, 0.3) — raíces reales' },
          { valor: 'ar2_comp', texto: 'AR(2), φ = (1.4, −0.75) — raíces complejas' }
        ]
      }, params, pintar);

      pintar();
      return [gAcf, gPacf];
    };

    // ================================================================
    // M2 · Triángulo de estacionariedad del AR(2)
    // ================================================================
    SIMULADORES['triangulo-ar2'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      // Valor inicial: el AR(2) de las manchas solares (Módulo 9) redondeado
      // al paso de 0.01 de los deslizadores.
      const params = { phi1: 1.40, phi2: -0.69 };

      // Parábola phi1^2 + 4*phi2 = 0: por debajo, las raíces son complejas
      const parabola = [];
      for (let x = -2.2; x <= 2.201; x += 0.05) {
        parabola.push({ x: +x.toFixed(3), y: -(x * x) / 4 });
      }

      altoEnEstrecho(c[0], 300);
      const gTriangulo = new Chart(c[0], {
        type: 'scatter',
        data: {
          datasets: [
            {
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
        'Realización simulada', COLORES_GRAFICO.primario);

      function pintar() {
        const a = analizarAR(params.phi1, params.phi2);
        const color = a.estacionario ? COLORES_GRAFICO.secundario : ROJO_GRAFICO;

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

        const s1 = params.phi1 + params.phi2;
        const s2 = params.phi2 - params.phi1;
        const filas = [
          { etiqueta: 'φ₁ + φ₂ =', valor: `${s1.toFixed(3)} ${s1 < 1 ? '< 1 ✓' : '≥ 1 ✗'}` },
          { etiqueta: 'φ₂ − φ₁ =', valor: `${s2.toFixed(3)} ${s2 < 1 ? '< 1 ✓' : '≥ 1 ✗'}` },
          { etiqueta: '−1 < φ₂ < 1:', valor: Math.abs(params.phi2) < 1 ? '✓' : '✗' },
          { etiqueta: 'Estacionario:', valor: a.estacionario ? 'SÍ' : 'NO' },
          { etiqueta: 'Raíces:', valor: a.complejas ? 'complejas' : 'reales' }
        ];
        if (isFinite(a.modulo)) {
          filas.push({ etiqueta: '|raíz| mínima:', valor: a.modulo.toFixed(4) });
        }
        if (a.complejas && a.estacionario) {
          filas.push({ etiqueta: 'Pseudo-periodo:', valor: `${a.periodo.toFixed(2)} periodos` });
        }
        if (cortada) filas.push({ etiqueta: 'La serie', valor: avisoDeCorte(y) });
        actualizarLectura(lectura, filas);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi1', etiqueta: 'φ₁ = ', min: -2.2, max: 2.2, paso: 0.01 },
        { clave: 'phi2', etiqueta: 'φ₂ = ', min: -1.2, max: 1.2, paso: 0.01 }
      ], params, pintar);

      pintar();
      return [gTriangulo, gSerie];
    };

    // ================================================================
    // M3 · Las firmas del MA (ACF y PACF teóricas)
    // ================================================================
    SIMULADORES['panel-ma-teorico'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { proceso: 'ma1_pos' };

      const gAcf = crearGraficoBarras(c[0], REZAGOS_T, PROCESOS.ma1_pos.acf_teorica,
        { etiqueta: 'ACF teórica', color: COLORES_GRAFICO.primario, tituloX: 'Rezago k' });
      const gPacf = crearGraficoBarras(c[1], REZAGOS_T, PROCESOS.ma1_pos.pacf_teorica,
        { etiqueta: 'PACF teórica', color: COLORES_GRAFICO.terciario, tituloX: 'Rezago k' });

      function pintar() {
        const p = PROCESOS[params.proceso];
        gAcf.data.datasets[0].data = p.acf_teorica;
        gAcf.update('none');
        gPacf.data.datasets[0].data = p.pacf_teorica;
        gPacf.update('none');
        c[0].setAttribute('aria-label',
          describirBarras(`ACF teórica del ${nombreProceso(p)}, rezagos`, p.acf_teorica));
        c[1].setAttribute('aria-label',
          describirBarras(`PACF teórica del ${nombreProceso(p)}, rezagos`, p.pacf_teorica));
        actualizarLectura(lectura, [
          { etiqueta: 'Proceso:', valor: `MA(${p.q})` },
          { etiqueta: `ACF en el rezago ${p.q + 1}:`, valor: p.acf_teorica[p.q].toFixed(4) },
          { etiqueta: 'ρ₁:', valor: p.acf_teorica[0].toFixed(4) },
          { etiqueta: 'γ₀ (con σ² = 1):', valor: p.var_proceso.toFixed(4) }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'proceso',
        etiqueta: 'Proceso',
        opciones: [
          { valor: 'ma1_pos', texto: 'MA(1), θ = 0.8' },
          { valor: 'ma1_neg', texto: 'MA(1), θ = −0.8' },
          { valor: 'ma2', texto: 'MA(2), θ = (0.6, 0.4)' }
        ]
      }, params, pintar);

      pintar();
      return [gAcf, gPacf];
    };

    // ================================================================
    // M3 · rho_1 de un MA(1) en función de theta: theta y 1/theta
    // ================================================================
    SIMULADORES['rho1-theta-ma1'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      // Valor inicial: el theta = 2 que simula el código de R del módulo
      const params = { theta: 2 };
      const X_MAX = 5;
      const ROJO = ROJO_GRAFICO;
      const rho1 = t => t / (1 + t * t);

      const curva = [];
      for (let x = -X_MAX; x <= X_MAX + 1e-9; x += 0.02) {
        curva.push({ x: +x.toFixed(2), y: rho1(+x.toFixed(2)) });
      }
      const linea = y => [{ x: -X_MAX, y: y }, { x: X_MAX, y: y }];

      altoEnEstrecho(c[0], 290);
      const gCurva = new Chart(c[0], {
        type: 'scatter',
        data: {
          datasets: [
            {
              label: 'ρ₁ = θ / (1 + θ²)',
              data: curva, showLine: true, fill: false, pointStyle: 'line',
              borderColor: COLORES_GRAFICO.primario, borderWidth: 2, pointRadius: 0, order: 5
            },
            {
              label: 'Cota |ρ₁| = 0.5',
              data: linea(0.5), showLine: true, pointStyle: 'line',
              borderColor: COLORES_GRAFICO.gris, borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, order: 6
            },
            {
              label: '',
              data: linea(-0.5), showLine: true, pointStyle: 'line',
              borderColor: COLORES_GRAFICO.gris, borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, order: 6
            },
            {
              // Segmento entre theta y 1/theta: la «misma altura» hecha visible
              label: '',
              data: [], showLine: true,
              borderColor: COLORES_GRAFICO.secundario, borderDash: [3, 3], borderWidth: 1.5, pointRadius: 0, order: 4
            },
            {
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
          },
          plugins: {
            legend: {
              labels: {
                font: { family: 'Montserrat', size: 11 }, boxWidth: 20, usePointStyle: true,
                filter: item => item.text !== ''
              }
            },
            tooltip: { backgroundColor: '#012820', bodyFont: { family: 'Fira Code' } }
          }
        }
      });

      function pintar() {
        const t = params.theta;
        const r = rho1(t);
        const cero = Math.abs(t) < 1e-9;
        const frontera = Math.abs(Math.abs(t) - 1) < 1e-9;
        const invertible = Math.abs(t) < 1 && !frontera;
        const inv = cero ? null : 1 / t;
        // En la frontera |theta| = 1 los dos puntos coinciden y ninguno es invertible
        const colorT = frontera ? COLORES_GRAFICO.secundario : (invertible ? COLORES_GRAFICO.terciario : ROJO);
        const colorInv = frontera ? COLORES_GRAFICO.secundario : (invertible ? ROJO : COLORES_GRAFICO.terciario);

        gCurva.data.datasets[3].data = cero ? [] : [{ x: t, y: r }, { x: inv, y: r }];
        gCurva.data.datasets[4].data = [{ x: t, y: r }];
        gCurva.data.datasets[4].backgroundColor = colorT;
        gCurva.data.datasets[5].data = cero ? [] : [{ x: inv, y: r }];
        gCurva.data.datasets[5].backgroundColor = colorInv;
        gCurva.update('none');
        c[0].setAttribute('aria-label',
          `Curva de ρ₁ = θ/(1 + θ²) de un MA(1), con θ = ${cifra(t, 2)} marcado a la altura ` +
          `ρ₁ = ${cifra(r, 4)}` + (cero ? '; el recíproco 1/θ no existe'
            : ` y su recíproco 1/θ = ${cifra(inv, 4)} a la misma altura` +
              (Math.abs(inv) > X_MAX ? ', fuera de la gráfica' : '')) +
          `; ${invertible ? 'θ es el invertible de la pareja' : (frontera ? 'frontera, no invertible' : 'θ no es invertible')}`);

        const filas = [
          { etiqueta: 'ρ₁ =', valor: r.toFixed(4) },
          { etiqueta: 'Invertible (|θ| < 1):', valor: frontera ? 'NO — frontera, |θ| = 1' : (invertible ? 'SÍ' : 'NO') }
        ];
        if (cero) {
          filas.push({ etiqueta: '1/θ:', valor: 'no existe; con θ = 0 el proceso es ruido blanco' });
        } else {
          filas.push({
            etiqueta: '1/θ =',
            valor: inv.toFixed(4) + (Math.abs(inv) > X_MAX ? ' (fuera de la gráfica)' : '')
          });
          filas.push({ etiqueta: 'ρ₁ con 1/θ =', valor: rho1(inv).toFixed(4) });
          filas.push({
            etiqueta: 'Mismo proceso:',
            valor: `θ = ${t.toFixed(2)} con σ², o θ = ${inv.toFixed(4)} con ${(t * t).toFixed(4)}·σ²`
          });
        }
        actualizarLectura(lectura, filas);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'theta', etiqueta: 'θ = ', min: -X_MAX, max: X_MAX, paso: 0.05 }
      ], params, pintar);

      pintar();
      return [gCurva];
    };

    // ================================================================
    // M4 · Pesos psi y pi de un ARMA(1,1)
    // ================================================================
    SIMULADORES['dualidad-psi-pi'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { phi: 0.8, theta: 0, h: 4 };
      const N = 12;
      // Términos para el límite sum psi_j^2 = gamma_0 / sigma^2. Con |phi| <= 0.95
      // la cola que queda fuera de 600 términos no llega a la decimosexta cifra.
      const N_LIMITE = 600;
      const etiquetas = Array.from({ length: N + 1 }, (_, j) => String(j));
      // Los psi que entran en la varianza del pronóstico a h pasos (j < h) van en
      // el color principal; el resto, en gris.
      const coloresPsi = h => etiquetas.map((_, j) => j < h ? COLORES_GRAFICO.primario : COLORES_GRAFICO.gris);

      const gPsi = crearGraficoBarras(c[0], etiquetas, pesosPsi([params.phi], [params.theta], N),
        { etiqueta: 'ψⱼ', color: COLORES_GRAFICO.primario, tituloX: 'j' });
      const gPi = crearGraficoBarras(c[1], etiquetas, pesosPi([params.phi], [params.theta], N),
        { etiqueta: 'πⱼ', color: COLORES_GRAFICO.terciario, tituloX: 'j' });

      function pintar() {
        const ar = [params.phi], ma = [params.theta];
        const psi = pesosPsi(ar, ma, N);
        const pi = pesosPi(ar, ma, N);
        // En la frontera |θ| = 1 el MA tampoco es invertible, pero sus π no
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
          { etiqueta: 'Var(e) a h pasos ÷ σ² = Σ ψⱼ², j < h (barras oscuras):', valor: varH.toFixed(4) },
          { etiqueta: 'Límite, h → ∞ (γ₀/σ²):', valor: varLimite.toFixed(4) }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi', etiqueta: 'φ = ', min: -0.95, max: 0.95, paso: 0.05 },
        { clave: 'theta', etiqueta: 'θ = ', min: -2, max: 2, paso: 0.05 },
        { clave: 'h', etiqueta: 'h = ', min: 1, max: 12, paso: 1, decimales: 0 }
      ], params, pintar);

      pintar();
      return [gPsi, gPi];
    };

    // ================================================================
    // M5 · Laboratorio ARMA: teórica frente a muestral
    // ================================================================
    SIMULADORES['laboratorio-arma'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { phi1: 0.7, phi2: 0, theta1: 0.5, theta2: 0, T: 200 };
      const MAX = 16;
      const etiquetas = etiquetasRezago(MAX);
      // La realización 1 usa la semilla de siempre; «Otra realización» avanza de
      // uno en uno. mulberry32 da secuencias independientes para semillas vecinas.
      const SEMILLA_BASE = 987654321;
      let realizacion = 1;

      altoEnEstrecho(c[1], 240);
      altoEnEstrecho(c[2], 240);
      const gSerie = serieSimple(c[0], simularARMA([0.7, 0], [0.5, 0], 200, SEMILLA_BASE),
        'Realización simulada', COLORES_GRAFICO.primario);
      const gAcf = correlogramaDoble(c[1], etiquetas, new Array(MAX).fill(0),
        new Array(MAX).fill(0), 200, 'ACF', COLORES_GRAFICO.primario);
      const gPacf = correlogramaDoble(c[2], etiquetas, new Array(MAX).fill(0),
        new Array(MAX).fill(0), 200, 'PACF', COLORES_GRAFICO.terciario);

      function pintar() {
        const ar = [params.phi1, params.phi2];
        const ma = [params.theta1, params.theta2];
        const a = analizarAR(params.phi1, params.phi2);
        const invertible = esInvertible(params.theta1, params.theta2);
        const T = Math.round(params.T);

        // Un proceso explosivo se corta al pasar de ±10⁶ (simularARMA): la
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
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi1', etiqueta: 'φ₁ = ', min: -1.5, max: 1.5, paso: 0.05 },
        { clave: 'phi2', etiqueta: 'φ₂ = ', min: -0.95, max: 0.95, paso: 0.05 },
        { clave: 'theta1', etiqueta: 'θ₁ = ', min: -1.5, max: 1.5, paso: 0.05 },
        { clave: 'theta2', etiqueta: 'θ₂ = ', min: -0.95, max: 0.95, paso: 0.05 },
        { clave: 'T', etiqueta: 'T = ', min: 60, max: 1000, paso: 20, decimales: 0 }
      ], params, pintar);

      // Misma teoría, otra muestra: la varianza del estimador de la que habla la
      // nota. Usa el estilo del botón de la autoevaluación para no añadir CSS,
      // que en este capítulo se hereda del capítulo 2 al reensamblar.
      const accion = document.createElement('div');
      accion.style.alignSelf = 'end';
      const botonRealizacion = document.createElement('button');
      botonRealizacion.type = 'button';
      botonRealizacion.className = 'quiz-comprobar';
      botonRealizacion.textContent = 'Otra realización';
      botonRealizacion.addEventListener('click', () => {
        realizacion += 1;
        pintar();
      });
      accion.appendChild(botonRealizacion);
      raiz.querySelector('.simulador-controles').appendChild(accion);

      pintar();
      return [gSerie, gAcf, gPacf];
    };

    // ================================================================
    // M6 · Teórica frente a muestral, T = 200 (realizaciones de R)
    // ================================================================
    SIMULADORES['teorica-vs-muestral'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { proceso: 'ar1_pos' };

      altoEnEstrecho(c[0], 250);
      altoEnEstrecho(c[1], 250);
      const gAcf = correlogramaDoble(c[0], REZAGOS_T, PROCESOS.ar1_pos.acf_teorica,
        DATOS_CAP3.realizaciones.ar1_pos.acf, DATOS_CAP3.realizaciones.ar1_pos.n,
        'ACF', COLORES_GRAFICO.primario);
      const gPacf = correlogramaDoble(c[1], REZAGOS_T, PROCESOS.ar1_pos.pacf_teorica,
        DATOS_CAP3.realizaciones.ar1_pos.pacf, DATOS_CAP3.realizaciones.ar1_pos.n,
        'PACF', COLORES_GRAFICO.terciario);

      function pintar() {
        const p = PROCESOS[params.proceso];
        const r = DATOS_CAP3.realizaciones[params.proceso];
        const b = banda(r.n);
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
              : `del ${corte[tipo] + 1} al ${muestral.length} (${ceros} rezagos), y ${lista.length} de ellos se salen de la banda en la muestra` +
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
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'proceso',
        etiqueta: 'Proceso simulado',
        opciones: [
          { valor: 'ar1_pos', texto: 'AR(1), φ = 0.8' },
          { valor: 'ma1_pos', texto: 'MA(1), θ = 0.8' },
          { valor: 'arma11', texto: 'ARMA(1,1), φ = 0.7, θ = 0.5' }
        ]
      }, params, pintar);

      pintar();
      return [gAcf, gPacf];
    };

    // ================================================================
    // M7 · Manchas solares: serie y correlogramas
    // ================================================================
    SIMULADORES['manchas-identificacion'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const anios = MANCHAS.anios.map(String);
      actualizarLectura(raiz.querySelector('.simulador-lectura'), [
        { etiqueta: 'n =', valor: MANCHAS.n },
        { etiqueta: 'banda =', valor: `±${MANCHAS.banda.toFixed(4)}` },
        { etiqueta: 'PACF(1), PACF(2):', valor: `${MANCHAS.pacf[0].toFixed(3)}, ${MANCHAS.pacf[1].toFixed(3)}` },
        { etiqueta: 'PACF(3):', valor: `${MANCHAS.pacf[2].toFixed(3)} — dentro de la banda, luego p = 2` }
      ]);
      return [
        serieSimple(c[0], MANCHAS.valores, 'Manchas solares (número anual)',
          COLORES_GRAFICO.primario, anios),
        crearGraficoBarras(c[1], REZAGOS, MANCHAS.acf, {
          etiqueta: 'ACF', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        }),
        crearGraficoBarras(c[2], REZAGOS, MANCHAS.pacf, {
          etiqueta: 'PACF', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        })
      ];
    };

    // ================================================================
    // M8 · Diagnóstico de residuales de cuatro candidatos
    // ================================================================
    SIMULADORES['diagnostico-residuales'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { modelo: 'arma10' };
      const anios = MANCHAS.anios.map(String);
      const inicial = MANCHAS.diagnosticos.arma10;

      altoEnEstrecho(c[1], 220);
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

      function pintar() {
        const d = MANCHAS.diagnosticos[params.modelo];
        gResid.data.datasets[0].data = d.residuales;
        gResid.data.datasets[0].label = `Residuales de ${d.etiqueta}`;
        gResid.update('none');

        const b = banda(MANCHAS.n);
        // Las barras no cambian de color con el veredicto de Ljung–Box: iban
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
          },
          { etiqueta: 'Shapiro–Wilk:', valor: `p = ${d.shapiro_p.toFixed(4)}` }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'modelo',
        etiqueta: 'Modelo ajustado',
        opciones: [
          { valor: 'arma10', texto: 'AR(1) — insuficiente' },
          { valor: 'arma20', texto: 'AR(2) — el de la identificación' },
          { valor: 'arma30', texto: 'AR(3)' },
          { valor: 'arma21', texto: 'ARMA(2,1) — el de menor AICc' }
        ]
      }, params, pintar);

      pintar();
      return [gResid, gAcf, gLb];
    };

    // ================================================================
    // M9 · Manchas solares: escala original frente a raíz cuadrada
    // ================================================================
    SIMULADORES['manchas-transformada'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { escala: 'cruda' };
      const anios = MANCHAS.anios.map(String);

      const gSerie = serieSimple(c[0], MANCHAS.valores, 'Manchas solares',
        COLORES_GRAFICO.primario, anios);
      const gPacf = crearGraficoBarras(c[1], REZAGOS, MANCHAS.pacf, {
        etiqueta: 'PACF', color: COLORES_GRAFICO.primario,
        lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
      });

      function pintar() {
        const esRaiz = params.escala === 'raiz';
        const color = esRaiz ? COLORES_GRAFICO.terciario : COLORES_GRAFICO.primario;

        gSerie.data.datasets[0].data = esRaiz ? TRANSF.sqrt.valores : MANCHAS.valores;
        gSerie.data.datasets[0].label = esRaiz ? '√(manchas solares)' : 'Manchas solares';
        gSerie.data.datasets[0].borderColor = color;
        gSerie.data.datasets[0].backgroundColor = color;
        gSerie.update('none');

        gPacf.data.datasets[0].data = esRaiz ? TRANSF.sqrt.pacf : MANCHAS.pacf;
        gPacf.data.datasets[0].backgroundColor = color;
        gPacf.update('none');
        const serie = esRaiz ? 'la raíz cuadrada de las manchas solares' : 'las manchas solares en su escala original';
        c[0].setAttribute('aria-label', `Serie anual de ${serie}, ${MANCHAS.n} observaciones`);
        c[1].setAttribute('aria-label', descripcionCorrelograma('PACF', serie,
          esRaiz ? TRANSF.sqrt.pacf : MANCHAS.pacf, banda(MANCHAS.n)));

        actualizarLectura(lectura, esRaiz ? [
          { etiqueta: 'Escala:', valor: 'raíz cuadrada' },
          { etiqueta: 'PACF(3), PACF(4):', valor: `${TRANSF.sqrt.pacf[2].toFixed(4)}, ${TRANSF.sqrt.pacf[3].toFixed(4)}` },
          { etiqueta: 'AR(2) — AICc / BIC:', valor: `${TRANSF.sqrt.aicc.toFixed(2)} / ${TRANSF.sqrt.bic.toFixed(2)} — los dos, mínimos de la rejilla` },
          { etiqueta: 'Ljung–Box(12):', valor: `p = ${TRANSF.sqrt.lb12_p.toFixed(4)} ✓` },
          { etiqueta: 'Pseudo-periodo:', valor: `${TRANSF.sqrt.periodo.toFixed(2)} años (ciclo solar ≈ 11)` }
        ] : [
          { etiqueta: 'Escala:', valor: 'original (número anual)' },
          { etiqueta: 'PACF(3), PACF(4):', valor: `${MANCHAS.pacf[2].toFixed(4)}, ${MANCHAS.pacf[3].toFixed(4)}` },
          { etiqueta: 'AR(2) — AICc / BIC:', valor: `${MANCHAS.diagnosticos.arma20.aicc.toFixed(2)} / ${MANCHAS.diagnosticos.arma20.bic.toFixed(2)} — no son los mínimos` },
          { etiqueta: 'Ljung–Box(12):', valor: `p = ${MANCHAS.diagnosticos.arma20.lb12_p.toFixed(4)} ✗` },
          { etiqueta: 'Pseudo-periodo:', valor: `${MANCHAS.raices.periodo.toFixed(2)} años` }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'escala',
        etiqueta: 'Escala de la serie',
        opciones: [
          { valor: 'cruda', texto: 'Original (número de manchas)' },
          { valor: 'raiz', texto: 'Raíz cuadrada' }
        ]
      }, params, pintar);

      pintar();
      return [gSerie, gPacf];
    };

    // ================================================================
    // M9 · Respuesta al impulso del AR(2) ajustado sobre la raíz
    // ================================================================
    // Aquí no hay nada precalculado: con phi1, phi2 y sigma^2 del ajuste, el
    // navegador vuelve a recorrer la recursión del Módulo 4 y reconstruye las
    // bandas que imprime forecast(). Los psi salen de pesosPsi(), la misma
    // función que usan el simulador de la dualidad y la ACF teórica.
    SIMULADORES['manchas-impulso'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { h: 6 };
      const N = 24;                       // rezagos de la respuesta al impulso
      const H = 24;                       // horizonte del abanico
      const ar = [TRANSF.sqrt.phi1, TRANSF.sqrt.phi2];
      const sigma2 = TRANSF.sqrt.sigma2;
      const z = 1.959964;                 // qnorm(0.975)
      const psi = pesosPsi(ar, [], N);
      // R = sqrt(-phi2) es el inverso del módulo de la raíz y manda en la
      // amortiguación. La envolvente de psi_j = R^j sin((j+1)w)/sin(w) no es
      // ±R^j sino ±R^j/sin(w): con el w de este ajuste, 1.88 veces mayor.
      const R = Math.sqrt(-TRANSF.sqrt.phi2);
      const omega = Math.acos(TRANSF.sqrt.phi1 / (2 * R));   // ángulo de la raíz
      const factor = 1 / Math.sin(omega);
      const etiquetas = Array.from({ length: N + 1 }, (_, j) => String(j));
      const envolvente = etiquetas.map((_, j) => factor * Math.pow(R, j));

      // Cola larga para el límite sum psi_j^2 = gamma_0 / sigma^2: con |B| =
      // 1.21 lo que queda fuera de 600 términos no llega a la decimosexta cifra.
      const psiLargo = pesosPsi(ar, [], 600);
      const sumaLimite = psiLargo.reduce((s, v) => s + v * v, 0);
      const semiTecho = z * Math.sqrt(sigma2 * sumaLimite);
      const sumaHasta = h => psiLargo.slice(0, h).reduce((s, v) => s + v * v, 0);
      const horizontes = Array.from({ length: H }, (_, k) => String(k + 1));
      const semianchos = horizontes.map((_, k) => z * Math.sqrt(sigma2 * sumaHasta(k + 1)));

      altoEnEstrecho(c[0], 240);
      altoEnEstrecho(c[1], 240);
      const gPsi = crearGraficoBarras(c[0], etiquetas, psi, {
        etiqueta: 'ψⱼ', color: COLORES_GRAFICO.primario, tituloX: 'j (años desde el choque)'
      });
      // La envolvente no es una recta, así que no cabe en la opción `lineas`
      // de crearGraficoBarras: se añade como dos datasets de línea. El negativo
      // va sin etiqueta para que no salga dos veces en la leyenda.
      [[`±${factor.toFixed(2)} × ${R.toFixed(2)}ʲ — envolvente`, envolvente],
        ['', envolvente.map(v => -v)]].forEach(
        ([etiqueta, datos]) => gPsi.data.datasets.push({
          type: 'line', label: etiqueta, data: datos,
          borderColor: COLORES_GRAFICO.secundario, borderDash: [5, 4], borderWidth: 1.5,
          pointRadius: 0, fill: false, order: 1
        }));
      gPsi.update('none');

      const gAbanico = crearGraficoBarras(c[1], horizontes, semianchos, {
        etiqueta: 'Semiancho del 95 %', color: COLORES_GRAFICO.terciario,
        tituloX: 'h (años de pronóstico)', min: 0, max: 6,
        lineas: [{ valor: semiTecho, etiqueta: 'Techo del abanico' }]
      });

      function pintar() {
        const h = Math.round(params.h);
        // En negro los psi que entran en la varianza a h pasos (j < h).
        gPsi.data.datasets[0].backgroundColor = etiquetas.map(
          (_, j) => j < h ? COLORES_GRAFICO.primario : COLORES_GRAFICO.gris);
        gPsi.update('none');
        // La barra del horizonte elegido va en el color oscuro: en naranja se
        // confundía con la recta del techo.
        gAbanico.data.datasets[0].backgroundColor = horizontes.map(
          (_, k) => k + 1 === h ? COLORES_GRAFICO.primario : COLORES_GRAFICO.terciario);
        gAbanico.update('none');

        const ee = Math.sqrt(sigma2 * sumaHasta(h));
        c[0].setAttribute('aria-label', describirBarras(
          'Pesos ψ del AR(2) ajustado a la raíz de las manchas solares, j de', psi, 0) +
          `, dentro de la envolvente ±${factor.toFixed(2)} × ${R.toFixed(4)}ʲ; en color oscuro, ` +
          `${h === 1 ? 'el único que entra' : `los ${h} que entran`} en la varianza del pronóstico a ` +
          `${h} ${h === 1 ? 'año' : 'años'}`);
        c[1].setAttribute('aria-label',
          `Semiancho del intervalo de pronóstico del 95 % para horizontes de 1 a ${H} años: ` +
          `±${(z * ee).toFixed(2)} a ${h} ${h === 1 ? 'año' : 'años'}, destacado, frente a un techo de ±${semiTecho.toFixed(2)}`);
        actualizarLectura(lectura, [
          {
            etiqueta: 'Envolvente ±Rʲ/sin ω:',
            valor: `R = √(−φ₂) = ${R.toFixed(4)} y 1/sin ω = ${factor.toFixed(3)} — se reduce a la mitad cada ${(Math.log(0.5) / Math.log(R)).toFixed(2)} años`
          },
          {
            etiqueta: 'Periodo de la oscilación:',
            valor: `${TRANSF.sqrt.periodo.toFixed(2)} años — el mismo pseudo-periodo de la serie`
          },
          { etiqueta: `Error estándar del pronóstico a ${h} año(s):`, valor: ee.toFixed(2) },
          { etiqueta: 'Semiancho del intervalo del 95 %:', valor: `±${(z * ee).toFixed(2)}` },
          {
            etiqueta: 'Techo, h → ∞:',
            valor: `±${semiTecho.toFixed(2)} — el ${(100 * z * ee / semiTecho).toFixed(0)} % ya está recorrido`
          }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'h', etiqueta: 'h = ', min: 1, max: 24, paso: 1, decimales: 0 }
      ], params, pintar);

      pintar();
      return [gPsi, gAbanico];
    };

    // ================================================================
    // M9 · Log-retornos de la TRM
    // ================================================================
    SIMULADORES['trm-retornos'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const fuera = RETORNOS.acf.filter(r => Math.abs(r) > RETORNOS.banda).length;
      actualizarLectura(raiz.querySelector('.simulador-lectura'), [
        { etiqueta: 'n =', valor: RETORNOS.n },
        { etiqueta: 'banda =', valor: `±${RETORNOS.banda.toFixed(4)}` },
        { etiqueta: 'rezagos de la ACF fuera de la banda:', valor: `${fuera} de ${RETORNOS.acf.length}` },
        { etiqueta: 'Ljung–Box(12):', valor: `p = ${RETORNOS.ljung_box[1].p.toFixed(4)}` },
        {
          etiqueta: 'AICc sin media, MA(1) vs. ruido blanco:',
          valor: `${RETORNOS.sin_media.ma1_aicc.toFixed(3)} vs. ${RETORNOS.sin_media.ruido_blanco_aicc.toFixed(3)}`
        }
      ]);
      return [
        serieSimple(c[0], RETORNOS.valores, 'Log-retorno mensual (%)',
          COLORES_GRAFICO.secundario, RETORNOS.fechas),
        crearGraficoBarras(c[1], REZAGOS, RETORNOS.acf, {
          etiqueta: 'ACF', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(RETORNOS.n), tituloX: 'Rezago k'
        }),
        crearGraficoBarras(c[2], REZAGOS, RETORNOS.pacf, {
          etiqueta: 'PACF', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(RETORNOS.n), tituloX: 'Rezago k'
        })
      ];
    };

    // ================================================================
    // Autoevaluación del capítulo
    // ================================================================
    // Tabla ordenable de los criterios de información: los once modelos
    // comparten $d = 0$, así que aquí el AICc SÍ es comparable entre todos.
    TABLAS_RANKING['criterios'] = function () {
      return {
        descripcion: 'Los once candidatos ARMA sobre las manchas solares crudas. ' +
          'Los once comparten $d = 0$ y el mismo $T$, así que sus criterios son ' +
          'comparables entre sí. Pulsa una cabecera para reordenar.',
        columnas: [
          { clave: 'modelo', titulo: 'Modelo', tipo: 'texto' },
          { clave: 'k', titulo: 'Coeficientes', decimales: 0, mejor: 'menor' },
          { clave: 'aicc', titulo: 'AICc', decimales: 2, mejor: 'menor' },
          { clave: 'bic', titulo: 'BIC', decimales: 2, mejor: 'menor' },
          { clave: 'sigma2', titulo: 'σ²', decimales: 1, mejor: 'menor' },
          { clave: 'lb', titulo: 'Ljung–Box p', tituloLargo: 'p-valor de Ljung-Box', decimales: 4, mejor: 'mayor' }
        ],
        filas: MANCHAS.rejilla.map(m => ({
          modelo: m.etiqueta, k: m.n_coef, aicc: m.aicc, bic: m.bic,
          sigma2: m.sigma2, lb: m.lb12_p
        })),
        formato: fmt,
        inicial: 'aicc',
        destacada: 'ARMA(2,0)',
        pie: 'El AR($2$) —la fila marcada, el que proponía la identificación— no es el mínimo de ninguno de los ' +
          'dos criterios sobre la serie cruda, y ordenando por Ljung–Box se ve además ' +
          'que no pasa el diagnóstico. Sobre $\\sqrt{\\text{manchas}}$ la conclusión cambia.'
      };
    };

    // R5 (2026-11-21). De dónde sale cada cifra que no está bajo un `#>` del capítulo
    // (etiquetas de diagnostico/cap3/comprobaciones/r5_cifras.out):
    //   P1 [Q1-01] · P2 [Q2-01] a [Q2-03] · P4 [Q4-01], [Q4-02] · P5 [Q5-01] a [Q5-03]
    //   P6 [Q6-01] a [Q6-04]: la salida es real, set.seed(329) y
    //      arima(rnorm(100), order = c(1, 0, 1), method = "ML")
    //   P7 [Q7-01], [Q7-02] · P9 [Q9-01]
    // El motor no baraja las opciones: la posición de la correcta la vigila
    // precalculo/audita_posicion_correcta.py.
    AUTOEVALUACIONES['cap3'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'Un AR(2) tiene $\\phi(B) = 1 - 1.2B + 0.9B^2$ y sus raíces tienen módulo $1.054$. ¿Es estacionario?',
        pista: 'Sitúa un número de módulo $1.054$ respecto del círculo unitario. Después relee, en la definición del Módulo 1, a qué lado del círculo tienen que quedar las raíces de $\\phi(B)$, y por qué ese lado sorprende la primera vez.',
        opciones: [
          {
            texto: 'No: para ser estacionario, sus raíces tendrían que caer dentro del círculo unitario.',
            correcta: false,
            retro: 'Es al revés, y es la confusión más común del capítulo. El polinomio está escrito en $B$, no en $1/B$: para el AR(1) la raíz es $1/\\phi$, así que $|\\phi| < 1$ equivale a $|1/\\phi| > 1$, es decir, raíz <strong>fuera</strong> del círculo.'
          },
          {
            texto: 'No: $\\phi_1 + \\phi_2 = -0.3$ es negativo, y con esa suma el proceso no puede ser estable.',
            correcta: false,
            retro: 'Cuidado con los signos del convenio: en $\\phi(B) = 1 - \\phi_1 B - \\phi_2 B^2$ los coeficientes van restando, así que aquí $\\phi_1 = 1.2$ y $\\phi_2 = -0.9$, y su suma es $0.3$. Además, el signo de esa suma no decide nada por sí solo.'
          },
          {
            texto: 'No se puede saber: falta conocer $\\sigma^2$, la varianza del ruido blanco que lo alimenta.',
            correcta: false,
            retro: 'La varianza del ruido no interviene: escala la serie, pero no cambia si el proceso olvida o no su pasado. Eso lo deciden únicamente las raíces de $\\phi(B)$.'
          },
          {
            texto: 'Sí: el módulo es mayor que 1, así que las raíces caen fuera del círculo unitario.',
            correcta: true,
            retro: 'La condición es $|B_i| > 1$ para todas las raíces. $1.054 > 1$, aunque por poco: es un proceso muy persistente, cerca de la frontera de la no estacionariedad.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 3,
        pregunta: 'Un MA(2) es $y_t = \\varepsilon_t + 0.6\\,\\varepsilon_{t-1} - 0.3\\,\\varepsilon_{t-2}$, con $\\sigma^2 = 4$. ¿Cuánto vale su autocovarianza de orden 1, $\\gamma_1 = \\operatorname{Cov}(y_t,\\,y_{t-1})$? Da dos decimales.',
        pista: 'Escribe $y_t$ e $y_{t-1}$ una debajo de la otra, cada una con sus tres choques, y marca los que aparecen en las dos: solo esos aportan a la covarianza. Vigila el signo de cada peso y no olvides $\\sigma^2$.',
        respuesta: 1.68,
        tolerancia: 0.006,
        retroAcierto: '$y_t$ e $y_{t-1}$ comparten dos choques: $\\varepsilon_{t-1}$, con pesos $0.6$ y $1$, y $\\varepsilon_{t-2}$, con pesos $-0.3$ y $0.6$. Entonces $\\gamma_1 = 4\\,(0.6 - 0.18) = 1.68$.',
        retroFallo: 'Es $\\gamma_1 = \\sigma^2(\\theta_1 + \\theta_1\\theta_2) = 4\\,(0.6 - 0.18) = 1.68$: $y_t$ e $y_{t-1}$ comparten los choques $\\varepsilon_{t-1}$ y $\\varepsilon_{t-2}$, y cada uno aporta el producto de sus dos pesos por $\\sigma^2$. Cada tropiezo habitual deja una cifra distinta: $2.40$ es contar solo el choque $\\varepsilon_{t-1}$; $0.42$, olvidar $\\sigma^2$; $3.12$, perder el signo de $\\theta_2$; $0.29$ es $\\rho_1$, la autocorrelación y no la autocovarianza; y $-1.20$ es $\\gamma_2$.'
      },
      {
        tipo: 'grafico',
        modulo: 5,
        alto: 200,
        descripcionGrafico: describirBarrasQuiz('Función de autocorrelación teórica de un proceso',
          PROCESOS.ma2.acf_teorica),
        pregunta: 'Esta es la ACF <strong>teórica</strong> de un proceso, y su PACF (no mostrada) decae sin cortarse. ¿De qué proceso se trata?',
        pista: 'Describe cada función con una frase: ¿termina de golpe o se va apagando? Con esas dos frases delante, busca la fila que les corresponde en la tabla del Módulo 5.',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS_T, PROCESOS.ma2.acf_teorica, {
          etiqueta: 'ACF teórica', color: COLORES_GRAFICO.primario, tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Un AR(2): hay dos barras distintas de cero, así que $p = 2$.',
            correcta: false,
            retro: 'Contar barras no basta: hay que mirar cuál de las dos funciones se corta. En un AR(2) es la <strong>PACF</strong> la que cae a cero tras el rezago 2, mientras la ACF decae sin cortarse nunca. Aquí ocurre justo lo contrario.'
          },
          {
            texto: 'Un MA(2): la ACF se corta tras el rezago 2 y la PACF decae.',
            correcta: true,
            retro: 'En un MA($q$), dos observaciones separadas por más de $q$ periodos no comparten ningún choque: por eso la ACF vale <strong>exactamente</strong> cero desde el rezago 3, y el corte en el rezago 2 da $q = 2$. La PACF, en cambio, decae sin cortarse.'
          },
          {
            texto: 'Un ARMA(2,2): hay dos rezagos activos en cada una de las dos.',
            correcta: false,
            retro: 'En un ARMA mixto <strong>ninguna</strong> de las dos funciones se corta: las dos decaen. Un corte limpio y exacto como este descarta precisamente el modelo mixto.'
          },
          {
            texto: 'Ruido blanco con dos autocorrelaciones altas por puro azar.',
            correcta: false,
            retro: 'Es una ACF <strong>teórica</strong>, calculada con <code>ARMAacf()</code>: no hay azar en ella. Y el ruido blanco tendría todas las autocorrelaciones nulas, incluidas las dos primeras.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 4,
        pregunta: 'Un ARMA(1,1) tiene $\\phi = 0.6$, $\\theta = -0.2$ y $\\sigma^2 = 5$. ¿Cuánto vale la varianza del error de pronóstico a dos pasos, $\\operatorname{Var}(e_{T+2})$? Da dos decimales.',
        pista: 'Calcula primero los pesos $\\psi$ que hacen falta con la recursión del Módulo 4, vigilando el signo de $\\theta$. Después decide cuántos pesos entran en la suma cuando $h = 2$ y qué factor la multiplica.',
        respuesta: 5.80,
        tolerancia: 0.006,
        retroAcierto: '$\\psi_1 = \\theta + \\phi = 0.4$, así que $\\operatorname{Var}(e_{T+2}) = 5\\,(1 + 0.4^2) = 5 \\times 1.16 = 5.80$. A un paso sería solo $\\sigma^2 = 5$: el pronóstico a dos pasos arrastra además el choque de $T+1$, que aquí pesa poco porque $\\phi$ y $\\theta$ tienen signos opuestos.',
        retroFallo: 'Es $\\sigma^2(\\psi_0^2 + \\psi_1^2) = 5\\,(1 + 0.4^2) = 5.80$, con $\\psi_1 = \\theta + \\phi = 0.4$. Cada tropiezo habitual deja una cifra distinta: $1.16$ es olvidar $\\sigma^2$; $0.80$, olvidar $\\psi_0 = 1$; $6.80$, tomar $\\psi_1 = \\phi$ como si fuera un AR(1); $8.20$, perder el signo de $\\theta$ y tomar $\\psi_1 = 0.8$; $7.00$, sumar los $\\psi$ sin elevarlos al cuadrado; y $6.09$, sumar hasta $j = h$ en vez de hasta $h - 1$.'
      },
      {
        tipo: 'multiple',
        modulo: 3,
        pregunta: 'Se simula una serie larga de un MA(1) con $\\theta = -2.5$ y $\\sigma^2 = 1$, y se le ajusta un MA(1) con <code>arima()</code>. Marca <strong>todas</strong> las afirmaciones correctas.',
        pista: 'Separa las dos propiedades del capítulo y qué polinomio responde por cada una. Después escribe $\\gamma_0$ y $\\gamma_1$ del proceso simulado y busca qué otro par $(\\theta,\\ \\sigma^2)$ da exactamente las mismas.',
        opciones: [
          {
            texto: 'La serie simulada no es estacionaria, porque $|\\theta|$ es mayor que 1.',
            correcta: false,
            retro: 'Un MA($q$) es estacionario para cualquier valor de sus $\\theta$: es una suma finita de ruido blanco. Lo que $|\\theta| > 1$ estropea es la invertibilidad, que se lee en $\\theta(B)$ —su raíz, $0.4$, cae dentro del círculo unitario—, no la estacionariedad.'
          },
          {
            texto: 'Su $\\rho_1$ coincide con la de otro MA(1), el que tiene $\\theta = -0.4$.',
            correcta: true,
            retro: '$-2.5/(1 + 2.5^2) = -0.4/(1 + 0.4^2) = -0.3448$: $\\theta$ y $1/\\theta$ comparten ACF, así que ningún correlograma los distingue.'
          },
          {
            texto: 'Sus pesos $\\pi$ se apagan con el rezago, porque $|\\rho_1|$ no llega a $0.5$.',
            correcta: false,
            retro: 'Con $\\theta = -2.5$ los pesos son $\\pi_j = (-\\theta)^j$: $2.5$, $6.25$, $15.625$… Crecen sin límite, que es lo que significa no ser invertible. Que $|\\rho_1|$ quede por debajo de $0.5$ no dice nada: le pasa a todo MA(1) con $|\\theta| \\ne 1$.'
          },
          {
            texto: 'Con sus opciones por defecto, <code>arima()</code> devolverá un $\\hat\\theta$ cercano a $-0.4$.',
            correcta: true,
            retro: 'Por defecto el software devuelve el MA(1) invertible, el de $|\\theta| < 1$, que aquí es $1/(-2.5) = -0.4$. Simulando 2000 valores sale $\\hat\\theta = -0.405$.'
          },
          {
            texto: 'El $\\hat\\sigma^2$ de ese ajuste quedará cerca de $1$, la varianza con que se simuló.',
            correcta: false,
            retro: 'Para describir el mismo proceso con $\\theta = -0.4$ hace falta $\\sigma^2 = 2.5^2 = 6.25$: así salen la misma $\\gamma_0 = 7.25$ y la misma $\\gamma_1 = -2.5$. En la simulación de 2000 valores, $\\hat\\sigma^2 = 6.58$.'
          }
        ],
        retroAcierto: 'Las dos son caras del mismo hecho: $(\\theta,\\ \\sigma^2) = (-2.5,\\ 1)$ y $(-0.4,\\ 6.25)$ dan las mismas autocovarianzas, de modo que $\\theta$ no es identificable, y el software resuelve el empate devolviendo por defecto el invertible.',
        retroFallo: 'Las correctas son la que compara la $\\rho_1$ de los dos MA(1) y la que dice qué $\\hat\\theta$ devuelve <code>arima()</code>: $(\\theta,\\ \\sigma^2) = (-2.5,\\ 1)$ y $(-0.4,\\ 6.25)$ dan las mismas autocovarianzas, $\\theta$ no es identificable y el software devuelve por defecto el invertible. Las otras tres confunden la estacionariedad con la invertibilidad, leen en la cota $0.5$ algo que no dice, u olvidan que al cambiar $\\theta$ cambia también $\\sigma^2$.'
      },
      {
        tipo: 'opcion',
        modulo: 5,
        pregunta: 'Ajustas un ARMA(1,1) a una serie de 100 datos y <code>arima()</code> devuelve $\\hat\\phi_1 = -0.60$ (error estándar $0.38$) y $\\hat\\theta_1 = 0.67$ (error estándar $0.35$). ¿Qué haces?',
        pista: 'Divide cada coeficiente entre su error estándar y, aparte, suma los dos coeficientes. Con esas tres cifras delante, pregúntate qué ha quedado bien determinado por los datos y qué no.',
        opciones: [
          {
            texto: 'Me quedo con el ARMA(1,1): los dos coeficientes son grandes en valor absoluto y los dos importan.',
            correcta: false,
            retro: 'El tamaño no basta. Ninguno de los dos coeficientes llega a $1.96$ veces su error estándar, y lo que el ajuste fija de verdad es su suma, $0.07$, no cada uno por separado. Dos parámetros que casi se cancelan no describen estructura: la esconden.'
          },
          {
            texto: 'Paso a un ARMA(2,2): con errores estándar tan grandes, al modelo le hacen falta más parámetros.',
            correcta: false,
            retro: 'Es justo al revés. Los errores estándar son grandes porque sobra un factor, no porque falte: la verosimilitud es casi plana en la dirección $\\phi_1 \\approx -\\theta_1$. Añadir parámetros abre la puerta a más factores casi comunes y la aplana todavía más.'
          },
          {
            texto: 'Diferencio la serie: unos coeficientes tan mal determinados indican que no es estacionaria.',
            correcta: false,
            retro: 'Nada apunta a una raíz unitaria: $|\\hat\\phi_1| = 0.60$ está lejos de 1. La imprecisión no es de la serie sino de la parametrización, porque muchas parejas $(\\phi_1, \\theta_1)$ con $\\phi_1 \\approx -\\theta_1$ dan casi la misma verosimilitud.'
          },
          {
            texto: 'Pruebo AR(1), MA(1) y ruido blanco, y los comparo por AICc antes de interpretar coeficientes.',
            correcta: true,
            retro: '$\\phi(B) = 1 + 0.60B$ y $\\theta(B) = 1 + 0.67B$ casi coinciden, así que el factor casi se cancela y el modelo es más pequeño de lo que aparenta. La serie era ruido blanco simulado, y el AICc lo recoge: $270.43$ para el ruido blanco, $272.43$ y $272.46$ para el MA(1) y el AR(1), y $273.88$ para el ARMA(1,1). Es la situación del ejemplo de R del Módulo 5.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 2,
        unidad: 'periodos',
        pregunta: 'Un AR(2) tiene $\\phi_1 = 0.9$ y $\\phi_2 = -0.5$. Sus raíces son complejas, así que su ACF oscila. ¿Cuánto vale su pseudo-periodo? Da dos decimales.',
        pista: 'La fórmula está en la nota «Raíces complejas y ciclos» del Módulo 2. Ve por partes —primero la raíz cuadrada, después el cociente, después el arcocoseno—, conserva cuatro decimales en cada paso y comprueba que la calculadora trabaja en <strong>radianes</strong>.',
        respuesta: 7.13,
        tolerancia: 0.006,
        retroAcierto: '$\\sqrt{0.5} = 0.7071$, el argumento del arcocoseno es $0.9/(2 \\times 0.7071) = 0.6364$, su arcocoseno vale $0.8810$ radianes y $2\\pi/0.8810 = 7.13$ periodos. Es el ángulo de la raíz de $\\phi(B)$: la misma cuenta que el Módulo 9 hace con el AR(2) de las manchas solares.',
        retroFallo: 'El cálculo es $2\\pi/\\arccos\\big(0.9/(2\\sqrt{0.5})\\big) = 2\\pi/\\arccos(0.6364) = 2\\pi/0.8810 = 7.13$ periodos. Los tropiezos habituales: dejar la calculadora en grados (sale $0.12$), olvidar la raíz cuadrada del denominador (sale $13.93$) o usar la otra fórmula, la del periodo medio de los ciclos, que el Módulo 9 distingue de esta (sale $7.57$). Si sale $7.06$, $7.10$ o $7.17$, se redondeó un paso intermedio a dos decimales. Y hace falta la precisión pedida: $7.1$ no basta.'
      },
      {
        tipo: 'opcion',
        modulo: 8,
        pregunta: 'Ajustas un ARMA(2,1) y evalúas Ljung–Box con <code>Box.test(residuals(m), lag = 12, type = "Ljung-Box")</code>, sin más argumentos. ¿Qué problema tiene esa llamada?',
        pista: 'Escribe los grados de libertad que usa la prueba tal como está llamada y los que corresponden a los residuales de un modelo con tres coeficientes estimados. Después piensa qué le pasa al $p$-valor al pasar de unos a otros.',
        opciones: [
          {
            texto: 'Ninguno: <code>Box.test()</code> descuenta por sí sola los parámetros del modelo ajustado.',
            correcta: false,
            retro: 'No lo hace. <code>fitdf</code> vale $0$ por defecto, porque la función no sabe de dónde vienen los residuales que recibe: podrían ser datos crudos. Hay que indicárselo siempre.'
          },
          {
            texto: 'Falta <code>fitdf = 3</code>: sin él la prueba es demasiado severa y rechaza de más.',
            correcta: false,
            retro: 'El argumento que falta es ese, pero la dirección del error es la contraria. Con más grados de libertad de los debidos el valor crítico es más alto y el $p$-valor, mayor: la prueba rechaza <em>menos</em>, y aprueba modelos que debería suspender.'
          },
          {
            texto: 'Falta <code>fitdf = 3</code>: sin él la prueba es demasiado indulgente y rechaza de menos.',
            correcta: true,
            retro: 'Con $p+q = 3$ parámetros estimados, el estadístico se distribuye $\\chi^2_{12-3}$, no $\\chi^2_{12}$. El caso más elocuente es el AR(2) de las manchas, donde $p+q = 2$: omitir <code>fitdf</code> cambia su $p$-valor de $0.0461$ (se rechaza) a $0.0996$ (no se rechaza). La conclusión se invierte por omitir un argumento.'
          },
          {
            texto: 'El problema es <code>lag = 12</code>: con un $h$ tan alto la prueba ya no puede detectar nada.',
            correcta: false,
            retro: 'La elección de $h$ admite discusión, pero no es el error de esta llamada: el capítulo evalúa en el rezago 12 las manchas solares. El problema está en otro argumento, y es uno que puede invertir la conclusión.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 8,
        alto: 200,
        descripcionGrafico: describirBarrasQuiz(
          'Función de autocorrelación de los residuales de un AR(1) ajustado a las manchas solares',
          MANCHAS.diagnosticos.arma10.acf_resid, banda(MANCHAS.n)),
        pregunta: 'Esta es la ACF de los residuales de un AR(1) ajustado a las manchas solares. ¿Qué haces?',
        pista: 'Mide antes de decidir: cuántas barras salen de la banda, en qué rezagos, y cuántas veces la supera la más alta. Compáralo con lo que el Módulo 6 dice que produce el azar.',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS, MANCHAS.diagnosticos.arma10.acf_resid, {
          etiqueta: 'ACF de los residuales', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Rechazo el modelo: quedan autocorrelaciones grandes y hay que aumentar el orden.',
            correcta: true,
            retro: '$r_1 = 0.556$ frente a una banda de $\\pm 0.196$, y no está sola: salen ocho de las veinte barras. Eso no es azar, es estructura sin modelar, y Ljung–Box da $p < 0.0001$. Subiendo a AR(2), las dos primeras autocorrelaciones residuales bajan a $0.1297$ y $-0.1477$.'
          },
          {
            texto: 'Lo acepto: con 20 rezagos, una o dos barras fuera de la banda son lo esperable.',
            correcta: false,
            retro: 'Esa regla vale para picos <em>pequeños y aislados</em>, apenas asomados. Aquí $r_1 = 0.556$ casi triplica la banda y salen ocho barras de veinte. La regla del 5 % explica ruido, no una señal así.'
          },
          {
            texto: 'Diferencio la serie: la ACF de los residuales decae despacio, como en una caminata.',
            correcta: false,
            retro: 'Diferenciar es la respuesta a una raíz unitaria en la <em>serie</em>, no a un mal ajuste. Estos residuales vienen de un modelo insuficiente sobre una serie que ya es estacionaria; diferenciar aquí sobrediferenciaría e introduciría un MA(1) espurio.'
          },
          {
            texto: 'Aplico el logaritmo: barras tan altas indican una varianza que crece con el nivel.',
            correcta: false,
            retro: 'La transformación resuelve problemas de <em>escala</em>, que se ven en la serie (amplitud que crece con el nivel), no en la ACF de los residuales. Y en esta serie el logaritmo es además imposible: hay un año con cero manchas.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 7,
        pregunta: 'Marca <strong>todas</strong> las afirmaciones correctas sobre los métodos de estimación.',
        pista: 'Para cada afirmación, localiza en el Módulo 7 la frase de la definición de los tres métodos, o la cifra de la tabla de las manchas, que la respalda o la desmiente.',
        opciones: [
          {
            texto: 'Yule–Walker estima bastante bien un AR puro y es muy ineficiente si hay parte MA.',
            correcta: true,
            retro: 'Es lo que el módulo dice de este método, que sale de las ecuaciones de momentos del AR: funciona bien en un AR puro y pierde mucha eficiencia en cuanto el modelo tiene parte MA.'
          },
          {
            texto: 'Con la misma serie y el mismo modelo, los tres métodos dan lo mismo, salvo diferencias de redondeo.',
            correcta: false,
            retro: 'No coinciden: sobre las manchas solares, Yule–Walker quedó a $1.26$ y $1.10$ errores estándar de máxima verosimilitud. CSS y máxima verosimilitud sí quedaron muy cerca, pero eso depende de $T$ y de lo cerca que esté $\\phi$ de la frontera.'
          },
          {
            texto: 'CSS condiciona en las primeras observaciones e ignora su aporte a la verosimilitud.',
            correcta: true,
            retro: 'Minimiza la suma de cuadrados condicionando en los primeros valores. La verosimilitud exacta añade la densidad de esas primeras observaciones, que es el término que penaliza los $\\phi$ cercanos a la frontera.'
          },
          {
            texto: 'El $\\hat\\sigma^2$ que devuelve <code>ar()</code> y el de <code>arima()</code> son intercambiables para calcular un AIC.',
            correcta: false,
            retro: 'No salen del mismo cálculo: en las manchas fueron $298.96$ y $229.43$. Los criterios de información se construyen sobre la verosimilitud, así que solo tienen sentido con ajustes de <code>arima()</code>.'
          },
          {
            texto: 'Sin indicar método, <code>arima()</code> usa <code>"CSS-ML"</code>: empieza con CSS y acaba con la verosimilitud exacta.',
            correcta: true,
            retro: 'Es su valor por defecto: CSS da los valores iniciales y la estimación final maximiza la verosimilitud exacta.'
          }
        ],
        retroAcierto: 'Son las tres que describen lo que hace cada método. Las dos falsas las desmiente el propio módulo con las manchas solares: Yule–Walker y máxima verosimilitud se separaron $1.26$ y $1.10$ errores estándar, y sus $\\hat\\sigma^2$ fueron $298.96$ y $229.43$.',
        retroFallo: 'Las correctas son las que dicen para qué modelos funciona bien Yule–Walker, qué deja fuera CSS y qué hace <code>arima()</code> por defecto. Las dos falsas son lo que el módulo desmiente con números: los métodos <strong>no</strong> coinciden —Yule–Walker quedó a más de un error estándar de máxima verosimilitud— y sus $\\hat\\sigma^2$ no miden lo mismo, así que mezclar salidas de <code>ar()</code> y <code>arima()</code> para comparar criterios de información no tiene sentido.'
      }
    ];

    // [inicio · actividad preparatoria del Parcial 2]
    // ================================================================
    // Actividad preparatoria del Parcial 2 (final del Módulo 10)
    //
    // Diez preguntas sobre el capítulo 2 y los módulos 3.1-3.4. NO SE EDITA A
    // MANO: lo escribe exporta_actividad.py, fuera del repositorio, desde un
    // banco cuyas cifras calcula R y rehace statsmodels. Para cambiar una
    // pregunta se cambia allí y se vuelve a instalar.
    //
    // Las preguntas no declaran `modulo` y su contenedor no tiene
    // `.quiz-resumen`, a propósito: el resumen final nombra módulos de ESTE
    // capítulo, y varias preguntas son del capítulo 2. Cada retroalimentación
    // cita su módulo, p. ej. (2.6) o (3.2).
    // ================================================================
    AUTOEVALUACIONES['parcial2'] = [
      {
        tipo: 'multiple',
        pregunta: 'Sea $\\{\\varepsilon_t\\}$ una sucesión i.i.d. $\\mathrm{N}(0,\\sigma^2)$ definida para todo entero $t$. Cada proceso se observa en $t = 1, 2, \\ldots$; en los autorregresivos sin valor inicial, $y_t$ depende solo de los choques hasta $t$ y la serie lleva mucho tiempo en marcha.<br>Marca <strong>todos</strong> los procesos que son débilmente estacionarios.',
        pista: 'Comprueba en cada proceso las tres condiciones —media constante, varianza constante y covarianza que solo depende del rezago— sin fiarte de si $t$ aparece o no en la fórmula. Y no mezcles estacionariedad con invertibilidad: son dos propiedades distintas.',
        opciones: [
          {
            texto: '$y_t = \\cos(\\pi t)\\,\\varepsilon_t$.',
            correcta: true,
            retro: 'Sí. Para $t$ entero, $\\cos(\\pi t) = (-1)^t$ solo vale $\\pm 1$: media 0, varianza $\\sigma^2$ y $\\operatorname{Cov}(y_t, y_{t+k}) = \\cos(\\pi t)\\cos(\\pi(t+k))\\,E[\\varepsilon_t\\varepsilon_{t+k}] = 0$ para $k \\ne 0$. Es ruido blanco aunque $t$ aparezca en la fórmula (2.1, 2.2).'
          },
          {
            texto: '$y_t = 1.05\\,y_{t-1} + \\varepsilon_t$.',
            correcta: false,
            retro: 'No. Con $|\\phi| = 1.05 \\gt  1$ la raíz $B = 1/\\phi$ cae dentro del círculo unitario: si la serie depende solo de los choques pasados, cada choque se amplifica y la varianza crece sin límite (2.5, 3.1).'
          },
          {
            texto: '$y_t = \\varepsilon_t + 1.6\\,\\varepsilon_{t-1}$.',
            correcta: true,
            retro: 'Sí. Un MA finito es estacionario para cualquier $\\theta$: media 0, varianza $\\sigma^2(1+\\theta^2)$ y una autocovarianza que solo depende del rezago. Con $|\\theta| = 1.6 \\gt  1$ no es invertible, pero la invertibilidad es otra propiedad: la estacionariedad no la exige (3.3).'
          },
          {
            texto: '$y_t = \\sqrt{t}\\;\\varepsilon_t$.',
            correcta: false,
            retro: 'No. La media es 0 y las covarianzas son nulas, pero $\\operatorname{Var}(y_t) = t\\sigma^2$ crece con $t$: falla la segunda condición. Mirar solo las autocorrelaciones no lo delataría (2.1, 2.3).'
          },
          {
            texto: '$y_t = y_{t-1} + \\varepsilon_t$.',
            correcta: false,
            retro: 'No. Si fuera estacionaria, $\\operatorname{Var}(y_t) = \\operatorname{Var}(y_{t-1}) + \\sigma^2$ obligaría a $\\sigma^2 = 0$: la varianza crece un $\\sigma^2$ en cada periodo. Es la caminata aleatoria, con raíz unitaria $B = 1$ (2.5, 3.1).'
          }
        ],
        retroFallo: 'Son dos: $y_t = \\cos(\\pi t)\\,\\varepsilon_t$ y $y_t = \\varepsilon_t + 1.6\\,\\varepsilon_{t-1}$. Debajo, la explicación de cada opción en la que fallaste.'
      },
      {
        tipo: 'opcion',
        pregunta: 'Una serie mensual de $T = 96$ observaciones tiene tendencia creciente y un patrón anual muy regular. Estas son cuatro salidas de R sobre ella, recortadas; <code>sa</code> es la serie sin su componente estacional, estimado con STL:<pre style="font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; adf.test(y)\nDickey-Fuller = -5.65, p-value = 0.01\nWarning message:\nIn adf.test(y) : p-value smaller than printed p-value\n\n&gt; adf.test(y, k = 12)\nDickey-Fuller = -2.22, p-value = 0.49\n\n&gt; adf.test(sa)\nDickey-Fuller = -2.73, p-value = 0.27\n\n&gt; kpss.test(sa, null = "Trend")\nKPSS Trend = 0.230, p-value = 0.01\nWarning message:\nIn kpss.test(sa, null = "Trend") : p-value smaller than printed p-value</pre>¿Qué se concluye, y por qué?',
        pista: 'Escribe primero la $H_0$ de cada prueba: la del ADF y la del KPSS son contrarias. Después compara los rezagos que usa el primer ADF con el periodo de la serie, y mira qué dicen las dos pruebas cuando ya no está el patrón anual.',
        opciones: [
          {
            texto: 'Es estacionaria. El primer ADF, con sus $k = \\lfloor (T-1)^{1/3} \\rfloor = 4$ rezagos, es el fiable: con 12 rezagos, o sin el patrón anual, la prueba pierde potencia y ya no puede rechazar.',
            correcta: false,
            retro: 'Es cierto que con 12 rezagos y $T = 96$ el ADF tiene poca potencia, así que su «no rechaza» solo no probaría nada. Pero la potencia no explica la cuarta salida: el KPSS, cuya hipótesis nula es la estacionariedad, la rechaza sobre la serie sin estacionalidad ($p \\lt 0.01$). Con la estacionalidad fuera, las dos pruebas coinciden en la raíz unitaria. Y sobre la serie sin estacionalidad el ADF usa los mismos $4$ rezagos que el primero, así que no ha perdido potencia: si la serie fuera estacionaria, lo esperable sería que rechazara. El rechazo con $4 \\lt 12$ rezagos es el artefacto que describe el 2.6.'
          },
          {
            texto: 'Hay raíz unitaria. El primer ADF no vale: su p-valor quedó fuera de la tabla, como avisa R, y un p-valor que no se conoce con exactitud no permite rechazar.',
            correcta: false,
            retro: 'La conclusión es la correcta, pero la razón no. El aviso dice que el p-valor real es todavía menor que 0.01: refuerza el rechazo, no lo invalida (2.6). Lo que invalida el primer ADF es que usa $k = 4$ rezagos, menos que el periodo 12, sobre una serie estacional.'
          },
          {
            texto: 'Es estacionaria. El KPSS sobre la serie sin estacionalidad da un p-valor pequeño, y eso respalda la estacionariedad que ya había encontrado el primer ADF.',
            correcta: false,
            retro: 'Es el error más común del capítulo: leer el KPSS como el ADF. La hipótesis nula del KPSS es la estacionariedad, así que un p-valor pequeño la <em>rechaza</em> (2.6). Sobre la serie sin estacionalidad, ADF y KPSS coinciden en que hay raíz unitaria; el rechazo del primer ADF es un artefacto de usar $4 \\lt 12$ rezagos.'
          },
          {
            texto: 'Hay raíz unitaria. El primer ADF usa $k = \\lfloor (T-1)^{1/3} \\rfloor = 4$ rezagos, menos que el periodo 12, y toma la oscilación anual por reversión a la media.',
            correcta: true,
            retro: '$(96-1)^{1/3} \\approx 4.56$, así que $k = 4$: la oscilación anual, que revierte a su media todo el tiempo, hace rechazar la raíz unitaria en falso. Con 12 rezagos el ADF ya no rechaza, aunque ese resultado solo, con poca potencia, no bastaría. Lo que decide es la serie sin estacionalidad: el ADF no rechaza ($p = 0.27$) y el KPSS, con la hipótesis nula contraria, rechaza la estacionariedad ($p \\lt 0.01$). Las dos coinciden. Es la regla del 2.6: tratar primero la estacionalidad.'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Los residuales de un modelo ya son ruido blanco: $\\varepsilon_t \\sim \\text{RB}(0,\\,\\sigma^2)$ con $\\sigma^2 = 0.25$. Por error se les aplica una diferencia regular, $w_t = \\nabla\\varepsilon_t = \\varepsilon_t - \\varepsilon_{t-1}$.<br>¿Cuál de estas descripciones de $w_t$ es correcta?',
        pista: 'Escribe $w_t$ y $w_{t-1}$ en función de los $\\varepsilon$: ¿qué choque comparten, y con qué signo entra en cada una? Para la invertibilidad, mira dónde cae la raíz de $1 - B$ respecto al círculo unitario.',
        opciones: [
          {
            texto: 'Un MA(1) con $\\theta = -1$: $\\operatorname{Var}(w_t) = 0.5$, $\\rho_1 = -0.5$, y no es invertible: la raíz de $1 - B$ es $B = 1$, sobre el círculo.',
            correcta: true,
            retro: '$\\operatorname{Var}(w_t) = \\sigma^2(1+\\theta^2) = 2\\sigma^2 = 0.5$ y $\\rho_1 = \\theta/(1+\\theta^2) = -0.5$, justo la cota del MA(1). Es el rastro de la sobrediferenciación (2.7) visto con las herramientas de 3.1 y 3.3: se fabricó un MA que no estaba en los datos, y además no invertible.'
          },
          {
            texto: 'Un MA(1) con $\\theta = -1$: $\\operatorname{Var}(w_t) = 0.25$, $\\rho_1 = -0.5$, y es invertible, porque $|\\theta| = 1$ no pasa de 1.',
            correcta: false,
            retro: 'Dos errores. La varianza sí cambia: $\\varepsilon_t$ y $\\varepsilon_{t-1}$ son incorrelados, así que sus varianzas se suman, $2\\sigma^2 = 0.5$; que suba es una de las señales de sobrediferenciación (2.7). Y la condición de invertibilidad es estricta: las raíces de $\\theta(B)$ tienen que estar fuera del círculo, y con $|\\theta| = 1$ la raíz $B = 1$ queda sobre él, no fuera (3.3).'
          },
          {
            texto: 'Ruido blanco, con $\\operatorname{Var}(w_t) = 0.5$ y $\\rho_1 = 0$: si los $\\varepsilon_t$ son incorrelados entre sí, sus diferencias también lo son.',
            correcta: false,
            retro: '$w_t = \\varepsilon_t - \\varepsilon_{t-1}$ y $w_{t-1} = \\varepsilon_{t-1} - \\varepsilon_{t-2}$ comparten un único choque, $\\varepsilon_{t-1}$, que entra en cada una con signo opuesto: $\\operatorname{Cov}(w_t, w_{t-1}) = (+1)(-1)\\sigma^2 = -\\sigma^2$, y $\\rho_1 = -0.5$. Diferenciar ruido blanco fabrica autocorrelación (2.7, 3.3).'
          },
          {
            texto: 'Ruido blanco, con la misma $\\operatorname{Var}(w_t) = 0.25$ y $\\rho_1 = 0$: restar el valor anterior no añade ni varianza ni autocorrelación.',
            correcta: false,
            retro: 'Dos errores. La varianza se duplica: $\\varepsilon_t$ y $\\varepsilon_{t-1}$ son incorrelados y sus varianzas se suman, $\\sigma^2 + \\sigma^2 = 0.5$. Y aparece autocorrelación: $w_t$ y $w_{t-1}$ comparten $\\varepsilon_{t-1}$ con signos opuestos, $\\rho_1 = -0.5$ (2.7, 3.3).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Una serie sigue una caminata aleatoria con deriva, $y_t = c + y_{t-1} + \\varepsilon_t$, con $c = 0.5$, $y_0 = 100$ y $\\varepsilon_t \\sim \\text{RB}(0,\\,\\sigma^2)$, $\\sigma = 2$.<br>¿Cuánto valen $E[y_{36}]$ y $\\operatorname{Var}(y_{36})$, y qué tratamiento necesita la serie para ser estacionaria, si necesita alguno?',
        pista: 'Desarrolla $y_t$ desde $y_0$: la deriva se suma una vez por periodo y los choques se van acumulando. Mira por separado qué le pasa a la media y qué a la varianza, y decide si la tendencia es determinista o estocástica antes de elegir el tratamiento.',
        opciones: [
          {
            texto: '$E[y_{36}] = 118$, $\\operatorname{Var}(y_{36}) = 4$. Se vuelve estacionaria restando la recta: $y_t - (y_0 + ct)$.',
            correcta: false,
            retro: 'La media está bien, pero $y_{36}$ acumula los choques $\\varepsilon_1, \\ldots, \\varepsilon_{36}$, incorrelados, y sus varianzas se suman: $36\\sigma^2 = 144$, no $\\sigma^2$. Por eso restar la recta no basta: deja $\\sum_{i=1}^{t}\\varepsilon_i$, una caminata cuya varianza sigue creciendo. A una serie con tendencia determinista se le resta la recta; a una con tendencia estocástica se la diferencia (2.5).'
          },
          {
            texto: '$E[y_{36}] = 118$, $\\operatorname{Var}(y_{36}) = 144$. Se vuelve estacionaria diferenciando: $\\nabla y_t = c + \\varepsilon_t$.',
            correcta: true,
            retro: '$y_{36} = y_0 + 36c + \\sum_{i=1}^{36}\\varepsilon_i$: la deriva se acumula en la media, y los choques $\\varepsilon_1, \\ldots, \\varepsilon_{36}$ en la varianza, $36\\sigma^2 = 144$. La tendencia es estocástica, y por eso se diferencia (2.5).'
          },
          {
            texto: '$E[y_{36}] = 100$, $\\operatorname{Var}(y_{36}) = 144$. Se vuelve estacionaria diferenciando: $\\nabla y_t = c + \\varepsilon_t$.',
            correcta: false,
            retro: 'La varianza y el tratamiento están bien, pero la media no. Los choques tienen media cero; la deriva $c$, no: se suma una vez por periodo, y en $36$ periodos desplaza la media en $36c$. $E[y_{36}] = y_0 + 36c = 118$ (2.5).'
          },
          {
            texto: '$E[y_{36}] = 100$, $\\operatorname{Var}(y_{36}) = 4$. Ya es estacionaria: no hace falta transformarla.',
            correcta: false,
            retro: 'Ninguna de las dos cifras: la deriva desplaza la media, $E[y_{36}] = y_0 + 36c = 118$, y los choques acumulados hacen crecer la varianza, $36\\sigma^2 = 144$. Una caminata con deriva no es estacionaria: hay que diferenciarla (2.5).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'El modelo $(1 - 0.3B)(1 - B)\\,y_t = \\varepsilon_t$ puede escribirse como un AR(2), $y_t = \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t$.<br>¿Cuánto valen $\\phi_1$ y $\\phi_2$, y es estacionario?',
        pista: 'Multiplica los dos factores y pasa al otro lado todo lo que no sea $y_t$: los signos cambian. Para la estacionariedad, mira la raíz de cada factor por separado; basta una que no caiga fuera del círculo unitario.',
        opciones: [
          {
            texto: '$\\phi_1 = 1.3$, $\\phi_2 = -0.3$. Es estacionario, porque la raíz de $(1 - 0.3B)$ es $B \\approx 3.33$, fuera del círculo unitario.',
            correcta: false,
            retro: 'Los coeficientes están bien; el veredicto, no. Las raíces de un producto son las de todos sus factores: la de $(1 - 0.3B)$ está fuera del círculo, pero la de $(1 - B)$, $B = 1$, está sobre el círculo, y basta una raíz con $|B| \\le 1$ para perder la estacionariedad (3.1).'
          },
          {
            texto: '$\\phi_1 = 0.7$, $\\phi_2 = 0.3$. No es estacionario: $\\phi_1 + \\phi_2 = 1 \\ge 1$.',
            correcta: false,
            retro: 'El veredicto está bien; los coeficientes, no. Esos son los de $(1 + 0.3B)(1 - B)$: se cambió el signo de $\\phi$ dentro del factor. Con $(1 - 0.3B)(1 - B) = 1 - 1.3B + 0.3B^2$ salen $\\phi_1 = 1.3$ y $\\phi_2 = -0.3$. El veredicto coincide porque los dos modelos llevan el factor $(1 - B)$ (3.1).'
          },
          {
            texto: '$\\phi_1 = 1.3$, $\\phi_2 = -0.3$. No es estacionario: $\\phi_1 + \\phi_2 = 1 \\ge 1$.',
            correcta: true,
            retro: '$(1 - 0.3B)(1 - B) = 1 - 1.3B + 0.3B^2$, y al despejar $y_t$ los coeficientes cambian de signo. El factor $(1 - B)$ aporta la raíz $B = 1$, sobre el círculo: $\\nabla y_t$ sigue un AR(1) con $\\phi = 0.3$, y la serie $y_t$ no es estacionaria (3.1; el triángulo, en 3.2; la diferenciación, en 2.7).'
          },
          {
            texto: '$\\phi_1 = 0.7$, $\\phi_2 = 0.3$. Es estacionario, porque la raíz de $(1 - 0.3B)$ es $B \\approx 3.33$, fuera del círculo unitario.',
            correcta: false,
            retro: 'Dos errores. Esos coeficientes son los de $(1 + 0.3B)(1 - B)$ —se cambió el signo de $\\phi$ dentro del factor—; con $(1 - 0.3B)(1 - B) = 1 - 1.3B + 0.3B^2$ salen $\\phi_1 = 1.3$ y $\\phi_2 = -0.3$. Y la raíz de $(1 - 0.3B)$ no decide sola: la de $(1 - B)$, $B = 1$, está sobre el círculo, y con ella el modelo no es estacionario (3.1).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Un AR(2), $y_t = \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t$, tiene $\\phi_1 = 1$ y $\\phi_2 = -0.5$.<br>¿Es estacionario, y cómo son las raíces de su polinomio autorregresivo $\\phi(B)$?',
        pista: '$|\\phi| \\lt 1$ es la condición del AR(1), no la del AR(2). Comprueba las tres desigualdades del triángulo, y deja que el signo de $\\phi_1^2 + 4\\phi_2$ decida el tipo de raíces.',
        opciones: [
          {
            texto: 'Estacionario, con raíces reales.',
            correcta: false,
            retro: 'El veredicto es correcto, pero no el tipo de raíz. El tipo de raíz lo decide $\\phi_1^2 + 4\\phi_2 = -1$, negativo: raíces complejas. Como además es estacionario, la ACF oscila con un pseudo-ciclo de unos $8$ periodos (3.1, 3.2).'
          },
          {
            texto: 'Estacionario, con raíces complejas.',
            correcta: true,
            retro: 'Las tres condiciones del triángulo: $\\phi_1 + \\phi_2 = 0.5 \\lt 1$, $\\phi_2 - \\phi_1 = -1.5 \\lt 1$ y $|\\phi_2| = 0.5 \\lt 1$. Se cumplen las tres: es estacionario. Que $|\\phi_1| = 1$ no sea menor que 1 no lo impide: $|\\phi| \\lt 1$ es la condición del AR(1), y la del AR(2) es el triángulo. Las raíces, conjugadas, tienen módulo $1.4142$: las dos fuera del círculo. El tipo de raíz lo decide $\\phi_1^2 + 4\\phi_2 = -1$, negativo: raíces complejas. Como además es estacionario, la ACF oscila con un pseudo-ciclo de unos $8$ periodos (3.1, 3.2).'
          },
          {
            texto: 'No estacionario, con raíces reales.',
            correcta: false,
            retro: 'Fallan las dos cosas. Las tres condiciones del triángulo: $\\phi_1 + \\phi_2 = 0.5 \\lt 1$, $\\phi_2 - \\phi_1 = -1.5 \\lt 1$ y $|\\phi_2| = 0.5 \\lt 1$. Se cumplen las tres: es estacionario. Que $|\\phi_1| = 1$ no sea menor que 1 no lo impide: $|\\phi| \\lt 1$ es la condición del AR(1), y la del AR(2) es el triángulo. Las raíces, conjugadas, tienen módulo $1.4142$: las dos fuera del círculo. El tipo de raíz lo decide $\\phi_1^2 + 4\\phi_2 = -1$, negativo: raíces complejas. Como además es estacionario, la ACF oscila con un pseudo-ciclo de unos $8$ periodos (3.1, 3.2).'
          },
          {
            texto: 'No estacionario, con raíces complejas.',
            correcta: false,
            retro: 'El tipo de raíz es el correcto, pero no el veredicto. Las tres condiciones del triángulo: $\\phi_1 + \\phi_2 = 0.5 \\lt 1$, $\\phi_2 - \\phi_1 = -1.5 \\lt 1$ y $|\\phi_2| = 0.5 \\lt 1$. Se cumplen las tres: es estacionario. Que $|\\phi_1| = 1$ no sea menor que 1 no lo impide: $|\\phi| \\lt 1$ es la condición del AR(1), y la del AR(2) es el triángulo. Las raíces, conjugadas, tienen módulo $1.4142$: las dos fuera del círculo (3.1, 3.2).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Se ajusta un AR(2) en R sobre una serie de 150 observaciones:<pre style="font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; arima(y, order = c(2, 0, 0))\n\nCall:\narima(x = y, order = c(2, 0, 0))\n\nCoefficients:\n         ar1     ar2  intercept\n      0.6256  0.1666    50.5900\ns.e.  0.0801  0.0827     0.8088\n\nsigma^2 estimated as 4.495:  log likelihood = -326.01,  aic = 660.02</pre>¿Cuánto vale la constante $c$ del modelo $y_t = c + \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t$?',
        pista: 'El <code>intercept</code> que imprime <code>arima()</code> no es la constante del modelo. Toma esperanzas a los dos lados de la ecuación del AR(2) y despeja $c$ en función de la media.',
        opciones: [
          {
            texto: '$c = 10.51$',
            correcta: true,
            retro: 'El <code>intercept</code> que imprime <code>arima()</code> es la media $\\mu$, no $c$. Tomando esperanzas en el modelo, $\\mu = c + (\\phi_1 + \\phi_2)\\mu$, de donde $c = \\mu(1 - \\phi_1 - \\phi_2) = 50.5900\\,(1 - 0.6256 - 0.1666) = 10.51$ (3.2).'
          },
          {
            texto: '$c = 50.59$',
            correcta: false,
            retro: 'Es la confusión que advierte el módulo 3.2: <code>intercept</code> es $\\hat\\mu$, no $\\hat c$. Usarlo como constante la sobrestima en $\\mu(\\phi_1 + \\phi_2) = 40.08$, y el pronóstico a un paso quedaría desplazado en esa misma cantidad. La relación es $c = \\mu(1 - \\phi_1 - \\phi_2) = 50.5900\\,(1 - 0.6256 - 0.1666) = 10.51$.'
          },
          {
            texto: '$c = 18.94$',
            correcta: false,
            retro: 'Faltó $\\phi_2$: esa cifra es $\\mu(1 - \\phi_1)$, la relación del AR(1). La media de un AR(2) descuenta los dos coeficientes, $\\mu = c/(1 - \\phi_1 - \\phi_2)$, así que $c = \\mu(1 - \\phi_1 - \\phi_2) = 50.5900\\,(1 - 0.6256 - 0.1666) = 10.51$ (3.2).'
          },
          {
            texto: '$c = 243.46$',
            correcta: false,
            retro: 'Esa cifra es $\\mu/(1 - \\phi_1 - \\phi_2)$, que invierte la relación. Tomando esperanzas, $\\mu = c + (\\phi_1 + \\phi_2)\\mu$, de donde $c = \\mu(1 - \\phi_1 - \\phi_2) = 50.5900\\,(1 - 0.6256 - 0.1666) = 10.51$: con $\\phi_1 + \\phi_2 \\gt  0$ la constante es menor que la media, no mayor (3.2).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Se quiere describir con un MA(1), $y_t = \\varepsilon_t + \\theta\\,\\varepsilon_{t-1}$ (el convenio de R), un proceso cuya autocorrelación de orden 1 es $\\rho_1 = 0.38$.<br>¿Cuál de estas afirmaciones sobre $\\theta$ es correcta?',
        pista: 'Plantea $\\theta/(1+\\theta^2) = \\rho_1$: es una ecuación de segundo grado, así que tiene dos soluciones. ¿Qué relación hay entre ellas, y cuál de las dos toma el convenio?',
        opciones: [
          {
            texto: '$\\theta = 2.1710$. También $\\theta = 0.4606$ da $\\rho_1 = 0.38$, pero se toma la de mayor $|\\theta|$, que da más dependencia.',
            correcta: false,
            retro: 'Las dos soluciones generan exactamente la misma dependencia: $\\rho_1(\\theta) = \\rho_1(1/\\theta)$. Ningún dato las distingue, y por eso se impone un convenio: la invertible. Con $\\theta = 2.1710$ la raíz de $1 + \\theta B$ es $B = -0.4606$, dentro del círculo unitario (3.3).'
          },
          {
            texto: '$\\theta = 0.4606$. También $\\theta = 2.1710$ da $\\rho_1 = 0.38$, pero se toma la solución invertible, la de $|\\theta| \\lt 1$.',
            correcta: true,
            retro: '$\\theta/(1+\\theta^2) = 0.38$ tiene dos soluciones, $\\theta = 0.4606$ y $\\theta = 2.1710$, con la misma ACF. La raíz de $1 + \\theta B$ es $B = -1/\\theta$: con $\\theta = 0.4606$ vale $B = -2.1710$, fuera del círculo, y con $\\theta = 2.1710$ vale $B = -0.4606$, dentro. Se toma la invertible, que es la que devuelve el software (3.3).'
          },
          {
            texto: '$\\theta = 0.3800$, porque en un MA(1) el coeficiente coincide con la autocorrelación de orden 1.',
            correcta: false,
            retro: 'Eso vale para el AR(1), donde $\\rho_1 = \\phi$. En el MA(1), $\\rho_1 = \\theta/(1+\\theta^2)$: con $\\theta = 0.3800$ sale $\\rho_1 = 0.3321$, no $0.38$ (3.3).'
          },
          {
            texto: 'Ningún valor de $\\theta$: como $\\theta$ y $1/\\theta$ dan la misma ACF, no hay forma de elegir entre ellos, y el MA(1) no sirve para este proceso.',
            correcta: false,
            retro: 'Que $\\theta$ y $1/\\theta$ den la misma ACF es cierto, pero no descarta el MA(1): se elige con un convenio, la solución invertible, $|\\theta| \\lt 1$. Aquí es $\\theta = 0.4606$ (3.3).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Un ARMA(1,1), $(1 - 0.65B)\\,y_t = (1 + 0.4B)\\,\\varepsilon_t$, tiene $\\sigma^2 = 1$.<br>¿Cuánto vale la varianza del error de pronóstico a tres pasos, $\\operatorname{Var}(e_{T+3})$?',
        pista: 'Lee $\\phi$ y $\\theta$ con cuidado con el signo de cada polinomio. A tres pasos, la suma $\\sigma^2\\sum_{j=0}^{h-1}\\psi_j^2$ tiene tres términos, y el primero es $\\psi_0 = 1$.',
        opciones: [
          {
            texto: '$\\operatorname{Var}(e_{T+3}) = 1.7651$',
            correcta: false,
            retro: 'Esa cifra es $\\sigma^2(\\psi_1^2 + \\psi_2^2 + \\psi_3^2)$, con $\\psi_3 = 0.4436$: la suma se corrió un índice. $\\operatorname{Var}(e_{T+h}) = \\sigma^2\\sum_{j=0}^{h-1}\\psi_j^2$ arranca en $\\psi_0 = 1$, así que le falta el término $\\sigma^2\\psi_0^2 = \\sigma^2$ —el error a un paso— y le sobra $\\sigma^2\\psi_3^2$, que solo entra a partir de cuatro pasos. Es el desfase que advierte el módulo 3.4: <code>ARMAtoMA()</code> no devuelve $\\psi_0$.'
          },
          {
            texto: '$\\operatorname{Var}(e_{T+3}) = 1.0889$',
            correcta: false,
            retro: 'Hubo un signo leído al revés en uno de los dos polinomios. Leer la parte MA como $(1 - 0.4B)$ (el convenio de resta) o la parte AR como $(1 + 0.65B)$ lleva a la misma varianza, porque los $\\psi_j^2$ coinciden. Pero la parte AR es $(1 - 0.65B)$, así que $\\phi = 0.65$; la MA es $(1 + 0.4B)$, así que $\\theta = 0.4$; y $\\psi_1 = \\phi + \\theta = 1.05$ (3.1, 3.4).'
          },
          {
            texto: '$\\operatorname{Var}(e_{T+3}) = 2.5683$',
            correcta: true,
            retro: 'La parte AR es $(1 - 0.65B)$ y la MA, $(1 + 0.4B)$, así que $\\phi = 0.65$ y $\\theta = 0.4$. Entonces $\\psi_1 = \\phi + \\theta = 1.05$ y $\\psi_2 = \\phi\\,\\psi_1 = 0.6825$. La varianza a tres pasos suma los tres primeros pesos al cuadrado, empezando en $\\psi_0 = 1$: $\\sigma^2(1 + \\psi_1^2 + \\psi_2^2) = 2.5683$ (3.4).'
          },
          {
            texto: '$\\operatorname{Var}(e_{T+3}) = 1.6010$',
            correcta: false,
            retro: 'Esa cifra usa los pesos del AR(1) solo, las potencias de $\\phi$ ($\\psi_1 = 0.65$, $\\psi_2 = 0.4225$): faltó la parte MA. En el ARMA(1,1), $\\psi_1 = \\phi + \\theta = 1.05$, y a partir de ahí cada peso es $\\phi$ veces el anterior (3.4).'
          }
        ]
      },
      {
        tipo: 'opcion',
        pregunta: 'Un AR(2) estacionario, $y_t = \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t$, tiene $\\phi_1 = 0.6$ y $\\phi_2 = 0.2$.<br>¿Cuánto valen sus autocorrelaciones teóricas $\\rho_1$ y $\\rho_2$, y sus autocorrelaciones parciales $\\phi_{22}$ y $\\phi_{33}$?',
        pista: 'En la ecuación de Yule–Walker para $k = 1$ aparece $\\rho_{-1}$: ¿cuánto vale? Y para la PACF, piensa en qué rezago se corta la de un AR(2).',
        opciones: [
          {
            texto: '$\\rho_1 = 0.7500$, $\\rho_2 = 0.6500$; $\\phi_{22} = 0.6500$, $\\phi_{33} = 0.5400$',
            correcta: false,
            retro: 'Las autocorrelaciones están bien, pero la PACF no es la ACF: descuenta los rezagos intermedios. En un AR(2), $\\phi_{22} = \\phi_2 = 0.2000$ y $\\phi_{kk} = 0$ para $k \\gt  2$: es la firma que identifica el orden (2.4, 3.2).'
          },
          {
            texto: '$\\rho_1 = 0.8000$, $\\rho_2 = 0.6800$; $\\phi_{22} = 0.2000$, $\\phi_{33} = 0.0000$',
            correcta: false,
            retro: 'La PACF está bien, pero la ACF no. En la ecuación de Yule–Walker para $k = 1$, $\\rho_1 = \\phi_1\\rho_0 + \\phi_2\\rho_{-1}$, se tomó $\\rho_{-1} = 1$; pero $\\rho_{-1} = \\rho_1$, así que $\\rho_1 = \\phi_1 + \\phi_2\\rho_1$ y $\\rho_1 = \\phi_1/(1 - \\phi_2) = 0.7500$ (3.2).'
          },
          {
            texto: '$\\rho_1 = 0.8000$, $\\rho_2 = 0.6800$; $\\phi_{22} = 0.6800$, $\\phi_{33} = 0.5680$',
            correcta: false,
            retro: 'Dos errores. En Yule–Walker se tomó $\\rho_{-1} = 1$ en vez de $\\rho_{-1} = \\rho_1$, y lo correcto es $\\rho_1 = \\phi_1/(1 - \\phi_2) = 0.7500$ (3.2). Y la PACF se confundió con la ACF: en un AR(2), $\\phi_{22} = \\phi_2$ y $\\phi_{33} = 0$ (2.4).'
          },
          {
            texto: '$\\rho_1 = 0.7500$, $\\rho_2 = 0.6500$; $\\phi_{22} = 0.2000$, $\\phi_{33} = 0.0000$',
            correcta: true,
            retro: 'De Yule–Walker, $\\rho_1 = \\phi_1 + \\phi_2\\rho_1$, de donde $\\rho_1 = \\phi_1/(1 - \\phi_2)$, y $\\rho_2 = \\phi_1\\rho_1 + \\phi_2$ (3.2). La PACF de un AR(2) vale $\\phi_{22} = (\\rho_2 - \\rho_1^2)/(1 - \\rho_1^2) = \\phi_2$ y exactamente 0 desde el rezago 3 (2.4, 3.2).'
          }
        ]
      }
    ];
    // [fin · actividad preparatoria del Parcial 2]

    // ================================================================
    // Simulacro del quiz (Módulo 11)
    //
    // Se marca y se cronometra, pero NO se corrige: en la página no hay
    // clave, ni retroalimentación, ni nada de donde deducirlas. Es lo que
    // lo distingue de la autoevaluación, que sí las lleva: un examen de
    // práctica cuyas preguntas se van a aplicar no puede publicar su clave,
    // porque viajaría en el HTML de un capítulo público.
    //
    // Injertado del Módulo 13 del capítulo 4 de Estadística Espacial
    // (2026-09-18), con dos cambios:
    //   · se engancha al registro SIMULADORES, que loadModule() ya recorre,
    //     en vez de pedir una llamada propia en el arranque de cada módulo.
    //     Así el andamiaje heredado del capítulo 2 no se toca, y el capítulo
    //     4 —que rehace esta región entera— no arrastra nada de esto;
    //   · lo marcado y el reloj viven en ESTADO_SIMULACRO, fuera del
    //     renderizado, para que salir al Módulo 9 y volver no borre veinte
    //     minutos de trabajo. El reloj sigue corriendo mientras tanto: se
    //     guarda la hora de final, no los segundos que quedan, igual que el
    //     reloj del salón no se para porque nadie lo mire.
    //
    // El CSS gemelo está en ensamblado/componentes/simulacro.css, y lo
    // instala ensambla_cap3.py.
    //
    // SIMULACROS['id'] = { minutos, variante, preguntas: [{ n, etiqueta,
    // tipo, enunciado, opciones }] } lo escribe exporta_simulacro.py desde
    // el banco del quiz, fuera del repositorio. `tipo` es 'opcion' (una
    // marca) o 'multiple' (varias).
    // ================================================================
    const SIMULACROS = {};
    const ESTADO_SIMULACRO = {};

    SIMULADORES['cap3-simulacro'] = function (raiz) {
      const id = raiz.dataset.simulador;
      const sim = SIMULACROS[id];
      if (!sim) {
        console.warn(`Simulacro no registrado: ${id}`);
        return [];
      }
      if (!ESTADO_SIMULACRO[id]) {
        ESTADO_SIMULACRO[id] = {
          marcadas: sim.preguntas.map(() => []),
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
      const listas = [];
      contenedor.innerHTML = '';

      sim.preguntas.forEach((pr, i) => {
        const caja = document.createElement('div');
        caja.className = 'simulacro-pregunta';
        const varias = pr.tipo === 'multiple';
        caja.innerHTML = `<span class="simulacro-etiqueta">${pr.n}. ${pr.etiqueta}` +
          `${varias ? ' · varias respuestas' : ''}</span>` +
          `<div class="simulacro-enunciado">${pr.enunciado}</div>` +
          `<div class="simulacro-opciones" role="group" ` +
          `aria-label="Opciones de la pregunta ${pr.n}"></div>`;
        const lista = caja.querySelector('.simulacro-opciones');
        listas.push(lista);
        pr.opciones.forEach((texto, j) => {
          const b = document.createElement('button');
          b.type = 'button';
          b.className = 'simulacro-opcion';
          b.innerHTML = `<span class="simulacro-letra">${LETRAS[j]})</span><span>${texto}</span>`;
          b.onclick = () => {
            const puesta = estado.marcadas[i].includes(j);
            if (varias) {
              estado.marcadas[i] = puesta
                ? estado.marcadas[i].filter(x => x !== j)
                : estado.marcadas[i].concat(j).sort((a, b) => a - b);
            } else {
              estado.marcadas[i] = puesta ? [] : [j];
            }
            pintaOpciones(i);
            pintaMarcador();
          };
          lista.appendChild(b);
        });
        contenedor.appendChild(caja);
        pintaOpciones(i);
      });

      function pintaOpciones(i) {
        listas[i].querySelectorAll('.simulacro-opcion').forEach((o, j) => {
          const marcada = estado.marcadas[i].includes(j);
          o.classList.toggle('marcada', marcada);
          o.setAttribute('aria-pressed', marcada ? 'true' : 'false');
        });
      }

      function pintaMarcador() {
        const hechas = estado.marcadas.filter(m => m.length > 0).length;
        conteo.textContent = `${hechas} de ${sim.preguntas.length} marcadas`;
        resumen.innerHTML = 'Tus respuestas: ' + sim.preguntas.map((pr, i) => {
          const letras = estado.marcadas[i].map(j => LETRAS[j]).join('');
          return `<b>${pr.n}${letras || '—'}</b>`;
        }).join(' · ') + '. No se corrigen aquí.';
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
        estado.marcadas = sim.preguntas.map(() => []);
        estado.finAt = null;
        estado.restante = sim.minutos * 60;
        sim.preguntas.forEach((_, i) => pintaOpciones(i));
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
    // Brightspace. Aquí solo viajan enunciados y opciones: la clave y la
    // retroalimentación se quedan fuera, porque este capítulo es público.
    //
    // La variante 9 no entra en el banco, a propósito: publicar una de las
    // ocho le daría a uno de cada ocho estudiantes las preguntas que va a
    // ver en el quiz, con tiempo ilimitado para estudiarlas.
    // ================================================================
    SIMULACROS['cap3-simulacro'] = {
      minutos: 30,
      variante: 9,
      preguntas: [
        {
          n: 1,
          etiqueta: 'cap. 2-3 · mód. 2.1-2.5 y 3.1-3.3 · estacionariedad débil',
          tipo: 'multiple',
          enunciado: '<p>Sea \\(\\{\\varepsilon_t\\}\\) una sucesión i.i.d. \\(\\mathrm{N}(0,\\sigma^2)\\) definida para todo entero \\(t\\). Cada proceso se observa en \\(t = 1, 2, \\ldots\\); en los autorregresivos sin valor inicial, \\(y_t\\) depende solo de los choques hasta \\(t\\) y la serie lleva mucho tiempo en marcha.</p><p>Marca <strong>todos</strong> los procesos que son débilmente estacionarios.</p>',
          opciones: [
            '\\(y_t = 1.25\\,y_{t-1} + \\varepsilon_t\\)',
            '\\(y_t = (-1)^t\\,\\varepsilon_t\\)',
            '\\(y_t = 10\\cos(2\\pi t/12) + \\varepsilon_t\\)',
            '\\(y_t = y_{t-1} + \\varepsilon_t\\)',
            '\\(y_t = 5 + 0.92\\,y_{t-1} + \\varepsilon_t\\)'
          ]
        },
        {
          n: 2,
          etiqueta: 'cap. 2 · mód. 2.6 · ADF, KPSS y estacionalidad',
          tipo: 'opcion',
          enunciado: '<p>Una serie mensual de \\(T = 116\\) observaciones tiene tendencia creciente y un patrón anual muy regular. Estas son cuatro salidas de R sobre ella, recortadas; <code>sa</code> es la serie sin su componente estacional, estimado con STL:</p><pre style="font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; adf.test(y)\nDickey-Fuller = -6.78, p-value = 0.01\nWarning message:\nIn adf.test(y) : p-value smaller than printed p-value\n\n&gt; adf.test(y, k = 12)\nDickey-Fuller = -1.84, p-value = 0.64\n\n&gt; adf.test(sa)\nDickey-Fuller = -2.61, p-value = 0.32\n\n&gt; kpss.test(sa, null = "Trend")\nKPSS Trend = 0.215, p-value = 0.010</pre><p>¿Qué se concluye, y por qué?</p>',
          opciones: [
            'Hay raíz unitaria. El primer ADF usa \\(k = \\lfloor (T-1)^{1/3} \\rfloor = 4\\) rezagos, menos que el periodo 12, y toma la oscilación anual por reversión a la media.',
            'Es estacionaria. El primer ADF, con sus \\(k = \\lfloor (T-1)^{1/3} \\rfloor = 4\\) rezagos, es el fiable: con 12 rezagos, o sin el patrón anual, la prueba pierde potencia y ya no puede rechazar.',
            'Hay raíz unitaria. El primer ADF no vale: su p-valor quedó fuera de la tabla, como avisa R, y un p-valor que no se conoce con exactitud no permite rechazar.',
            'Es estacionaria. El KPSS sobre la serie sin estacionalidad da un p-valor pequeño, y eso respalda la estacionariedad que ya había encontrado el primer ADF.'
          ]
        },
        {
          n: 3,
          etiqueta: 'cap. 2-3 · mód. 2.7 y 3.3 · sobrediferenciación',
          tipo: 'opcion',
          enunciado: '<p>Los residuales de un modelo ya son ruido blanco: \\(\\varepsilon_t \\sim \\text{RB}(0,\\,\\sigma^2)\\) con \\(\\sigma^2 = 0.81\\). Por error se les aplica una diferencia regular, \\(w_t = \\nabla\\varepsilon_t = \\varepsilon_t - \\varepsilon_{t-1}\\).</p><p>¿Cuál de estas descripciones de \\(w_t\\) es correcta?</p>',
          opciones: [
            'Un MA(1) con \\(\\theta = -1\\): \\(\\operatorname{Var}(w_t) = 0.81\\), \\(\\rho_1 = -0.5\\), y es invertible, porque \\(|\\theta| = 1\\) no pasa de 1.',
            'Un MA(1) con \\(\\theta = -1\\): \\(\\operatorname{Var}(w_t) = 1.62\\), \\(\\rho_1 = -0.5\\), y no es invertible: la raíz de \\(1 - B\\) es \\(B = 1\\), sobre el círculo.',
            'Ruido blanco, con \\(\\operatorname{Var}(w_t) = 1.62\\) y \\(\\rho_1 = 0\\): si los \\(\\varepsilon_t\\) son incorrelados entre sí, sus diferencias también lo son.',
            'Ruido blanco, con la misma \\(\\operatorname{Var}(w_t) = 0.81\\) y \\(\\rho_1 = 0\\): restar el valor anterior no añade ni varianza ni autocorrelación.'
          ]
        },
        {
          n: 4,
          etiqueta: 'cap. 2 · mód. 2.5 · caminata con deriva',
          tipo: 'opcion',
          enunciado: '<p>Una serie sigue una caminata aleatoria con deriva, \\(y_t = c + y_{t-1} + \\varepsilon_t\\), con \\(c = 1.1\\), \\(y_0 = 120\\) y \\(\\varepsilon_t \\sim \\text{RB}(0,\\,\\sigma^2)\\), \\(\\sigma = 2.2\\).</p><p>¿Cuánto valen \\(E[y_{40}]\\) y \\(\\operatorname{Var}(y_{40})\\), y qué tratamiento necesita la serie para ser estacionaria, si necesita alguno?</p>',
          opciones: [
            '\\(E[y_{40}] = 164\\), \\(\\operatorname{Var}(y_{40}) = 4.84\\). Se vuelve estacionaria restando la recta: \\(y_t - (y_0 + ct)\\).',
            '\\(E[y_{40}] = 120\\), \\(\\operatorname{Var}(y_{40}) = 193.6\\). Se vuelve estacionaria diferenciando: \\(\\nabla y_t = c + \\varepsilon_t\\).',
            '\\(E[y_{40}] = 164\\), \\(\\operatorname{Var}(y_{40}) = 193.6\\). Se vuelve estacionaria diferenciando: \\(\\nabla y_t = c + \\varepsilon_t\\).',
            '\\(E[y_{40}] = 120\\), \\(\\operatorname{Var}(y_{40}) = 4.84\\). Ya es estacionaria: no hace falta transformarla.'
          ]
        },
        {
          n: 5,
          etiqueta: 'cap. 3 · mód. 3.1 · operador de rezago',
          tipo: 'opcion',
          enunciado: '<p>El modelo \\((1 + 0.6B)(1 - B)\\,y_t = \\varepsilon_t\\) puede escribirse como un AR(2), \\(y_t = \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t\\).</p><p>¿Cuánto valen \\(\\phi_1\\) y \\(\\phi_2\\), y es estacionario?</p>',
          opciones: [
            '\\(\\phi_1 = 0.4\\), \\(\\phi_2 = 0.6\\). Es estacionario, porque la raíz de \\((1 + 0.6B)\\) es \\(B \\approx -1.67\\), fuera del círculo unitario.',
            '\\(\\phi_1 = 1.6\\), \\(\\phi_2 = -0.6\\). No es estacionario: \\(\\phi_1 + \\phi_2 = 1 \\ge 1\\).',
            '\\(\\phi_1 = 1.6\\), \\(\\phi_2 = -0.6\\). Es estacionario, porque la raíz de \\((1 + 0.6B)\\) es \\(B \\approx -1.67\\), fuera del círculo unitario.',
            '\\(\\phi_1 = 0.4\\), \\(\\phi_2 = 0.6\\). No es estacionario: \\(\\phi_1 + \\phi_2 = 1 \\ge 1\\).'
          ]
        },
        {
          n: 6,
          etiqueta: 'cap. 3 · mód. 3.1-3.2 · triángulo del AR(2)',
          tipo: 'opcion',
          enunciado: '<p>Un AR(2), \\(y_t = \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t\\), tiene \\(\\phi_1 = 1.4\\) y \\(\\phi_2 = -0.45\\).</p><p>¿Es estacionario, y cómo son las raíces de su polinomio autorregresivo \\(\\phi(B)\\)?</p>',
          opciones: [
            'Estacionario, con raíces reales.',
            'Estacionario, con raíces complejas.',
            'No estacionario, con raíces reales.',
            'No estacionario, con raíces complejas.'
          ]
        },
        {
          n: 7,
          etiqueta: 'cap. 3 · mód. 3.2 · intercept y constante',
          tipo: 'opcion',
          enunciado: '<p>Se ajusta un AR(2) en R sobre una serie de 150 observaciones:</p><pre style="font-weight:400;font-size:0.78rem;line-height:1.45;margin:0.6rem 0;max-height:none;padding:0.8rem 1rem !important;">&gt; arima(y, order = c(2, 0, 0))\n\nCall:\narima(x = y, order = c(2, 0, 0))\n\nCoefficients:\n         ar1      ar2  intercept\n      0.7579  -0.2327    59.9161\ns.e.  0.0797   0.0797     0.1879\n\nsigma^2 estimated as 1.203:  log likelihood = -226.99,  aic = 461.98</pre><p>¿Cuánto vale la constante \\(c\\) del modelo \\(y_t = c + \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t\\)?</p>',
          opciones: [
            '\\(c = 59.92\\)',
            '\\(c = 28.45\\)',
            '\\(c = 14.51\\)',
            '\\(c = 126.19\\)'
          ]
        },
        {
          n: 8,
          etiqueta: 'cap. 3 · mód. 3.3 · MA(1) e invertibilidad',
          tipo: 'opcion',
          enunciado: '<p>Se quiere describir con un MA(1), \\(y_t = \\varepsilon_t + \\theta\\,\\varepsilon_{t-1}\\) (el convenio de R), un proceso cuya autocorrelación de orden 1 es \\(\\rho_1 = 0.44\\).</p><p>¿Cuál de estas afirmaciones sobre \\(\\theta\\) es correcta?</p>',
          opciones: [
            '\\(\\theta = 1.6761\\). También \\(\\theta = 0.5966\\) da \\(\\rho_1 = 0.44\\), pero se toma la de mayor \\(|\\theta|\\), que da más dependencia.',
            '\\(\\theta = 0.4400\\), porque en un MA(1) el coeficiente coincide con la autocorrelación de orden 1.',
            '\\(\\theta = 0.5966\\). También \\(\\theta = 1.6761\\) da \\(\\rho_1 = 0.44\\), pero se toma la solución invertible, la de \\(|\\theta| \\lt 1\\).',
            'Ningún valor de \\(\\theta\\): como \\(\\theta\\) y \\(1/\\theta\\) dan la misma ACF, no hay forma de elegir entre ellos, y el MA(1) no sirve para este proceso.'
          ]
        },
        {
          n: 9,
          etiqueta: 'cap. 3 · mód. 3.4 · pesos psi y varianza del pronóstico',
          tipo: 'opcion',
          enunciado: '<p>Un ARMA(1,1), \\((1 - 0.93B)\\,y_t = (1 - 0.12B)\\,\\varepsilon_t\\), tiene \\(\\sigma^2 = 2.2\\).</p><p>¿Cuánto vale la varianza del error de pronóstico a tres pasos, \\(\\operatorname{Var}(e_{T+3})\\)?</p>',
          opciones: [
            '\\(\\operatorname{Var}(e_{T+3}) = 3.7716\\)',
            '\\(\\operatorname{Var}(e_{T+3}) = 6.7233\\)',
            '\\(\\operatorname{Var}(e_{T+3}) = 5.7485\\)',
            '\\(\\operatorname{Var}(e_{T+3}) = 4.8918\\)'
          ]
        },
        {
          n: 10,
          etiqueta: 'cap. 3 · mód. 3.2 y 2.4 · Yule-Walker y PACF',
          tipo: 'opcion',
          enunciado: '<p>Un AR(2) estacionario, \\(y_t = \\phi_1 y_{t-1} + \\phi_2 y_{t-2} + \\varepsilon_t\\), tiene \\(\\phi_1 = 0.5\\) y \\(\\phi_2 = 0.3\\).</p><p>¿Cuánto valen sus autocorrelaciones teóricas \\(\\rho_1\\) y \\(\\rho_2\\), y sus autocorrelaciones parciales \\(\\phi_{22}\\) y \\(\\phi_{33}\\)?</p>',
          opciones: [
            '\\(\\rho_1 = 0.7143\\), \\(\\rho_2 = 0.6571\\); \\(\\phi_{22} = 0.3000\\), \\(\\phi_{33} = 0.0000\\)',
            '\\(\\rho_1 = 0.7143\\), \\(\\rho_2 = 0.6571\\); \\(\\phi_{22} = 0.6571\\), \\(\\phi_{33} = 0.5429\\)',
            '\\(\\rho_1 = 0.8000\\), \\(\\rho_2 = 0.7000\\); \\(\\phi_{22} = 0.3000\\), \\(\\phi_{33} = 0.0000\\)',
            '\\(\\rho_1 = 0.8000\\), \\(\\rho_2 = 0.7000\\); \\(\\phi_{22} = 0.7000\\), \\(\\phi_{33} = 0.5900\\)'
          ]
        }
      ]
    };
    // [fin · simulacro del quiz]
