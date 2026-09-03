    // ================================================================
    // Datos y ayudantes del capítulo, tomados del precálculo en R
    // ================================================================
    const PROCESOS = DATOS_CAP3.procesos;
    const MANCHAS = DATOS_CAP3.manchas;
    const RETORNOS = DATOS_CAP3.retornos_trm;
    const TRANSF = DATOS_CAP3.manchas.transformacion;
    const REZAGOS = etiquetasRezago(DATOS_CAP3.max_rezago);
    const REZAGOS_T = etiquetasRezago(DATOS_CAP3.max_rezago_teorico);

    function banda(n) { return 1.96 / Math.sqrt(n); }

    function lineasBanda(n) {
      const b = banda(n);
      return [
        { valor: b, etiqueta: 'Banda ±1.96/√T' },
        { valor: -b, etiqueta: '' }
      ];
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
      return { estacionario: modulo > 1, modulo: modulo, complejas: false };
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
        Math.abs((-t1 - r) / (2 * t2))) > 1;
    }

    // Simula un ARMA con ruido de semilla fija, descartando un tramo de
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
    }

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

    // Correlograma con dos juegos de barras: teórico (sólido) y muestral (claro)
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

      const gTriangulo = new Chart(c[0], {
        type: 'scatter',
        data: {
          datasets: [
            {
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
        'Realización simulada', COLORES_GRAFICO.primario);

      function pintar() {
        const a = analizarAR(params.phi1, params.phi2);
        const color = a.estacionario ? COLORES_GRAFICO.secundario : '#dc2626';

        gTriangulo.data.datasets[2].data = [{ x: params.phi1, y: params.phi2 }];
        gTriangulo.data.datasets[2].backgroundColor = color;
        gTriangulo.update('none');

        // Un proceso no estacionario explota: verlo explotar es la lección
        gSerie.data.datasets[0].data = simularARMA([params.phi1, params.phi2], [], 160, 20260726);
        gSerie.data.datasets[0].borderColor = a.estacionario ? COLORES_GRAFICO.primario : '#dc2626';
        gSerie.data.datasets[0].backgroundColor = gSerie.data.datasets[0].borderColor;
        gSerie.update('none');

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
    // M4 · Pesos psi y pi de un ARMA(1,1)
    // ================================================================
    SIMULADORES['dualidad-psi-pi'] = function (raiz) {
      const c = raiz.querySelectorAll('canvas');
      const lectura = raiz.querySelector('.simulador-lectura');
      const params = { phi: 0.8, theta: 0 };
      const N = 12;
      const etiquetas = Array.from({ length: N + 1 }, (_, j) => String(j));

      const gPsi = crearGraficoBarras(c[0], etiquetas, pesosPsi([params.phi], [params.theta], N),
        { etiqueta: 'ψⱼ', color: COLORES_GRAFICO.primario, tituloX: 'j' });
      const gPi = crearGraficoBarras(c[1], etiquetas, pesosPi([params.phi], [params.theta], N),
        { etiqueta: 'πⱼ', color: COLORES_GRAFICO.terciario, tituloX: 'j' });

      function pintar() {
        const ar = [params.phi], ma = [params.theta];
        const psi = pesosPsi(ar, ma, N);
        const pi = pesosPi(ar, ma, N);
        const invertible = Math.abs(params.theta) < 1;

        gPsi.data.datasets[0].data = psi;
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
          }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi', etiqueta: 'φ = ', min: -0.95, max: 0.95, paso: 0.05 },
        { clave: 'theta', etiqueta: 'θ = ', min: -2, max: 2, paso: 0.05 }
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

      const gSerie = serieSimple(c[0], simularARMA([0.7, 0], [0.5, 0], 200, 987654321),
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

        const y = simularARMA(ar, ma, T, 987654321);
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
          {
            etiqueta: 'distancia media |teórica − muestral|:',
            valor: a.estacionario ? dif.toFixed(4) : '—'
          }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'phi1', etiqueta: 'φ₁ = ', min: -1.5, max: 1.5, paso: 0.05 },
        { clave: 'phi2', etiqueta: 'φ₂ = ', min: -0.95, max: 0.95, paso: 0.05 },
        { clave: 'theta1', etiqueta: 'θ₁ = ', min: -1.5, max: 1.5, paso: 0.05 },
        { clave: 'theta2', etiqueta: 'θ₂ = ', min: -0.95, max: 0.95, paso: 0.05 },
        { clave: 'T', etiqueta: 'T = ', min: 60, max: 1000, paso: 20, decimales: 0 }
      ], params, pintar);

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

      const gAcf = correlogramaDoble(c[0], REZAGOS_T, PROCESOS.ar1_pos.acf_teorica,
        DATOS_CAP3.realizaciones.ar1_pos.acf, DATOS_CAP3.realizaciones.ar1_pos.n,
        'ACF', COLORES_GRAFICO.primario);
      const gPacf = correlogramaDoble(c[1], REZAGOS_T, PROCESOS.ar1_pos.pacf_teorica,
        DATOS_CAP3.realizaciones.ar1_pos.pacf, DATOS_CAP3.realizaciones.ar1_pos.n,
        'PACF', COLORES_GRAFICO.terciario);

      function pintar() {
        const p = PROCESOS[params.proceso];
        const r = DATOS_CAP3.realizaciones[params.proceso];
        actualizarDoble(gAcf, p.acf_teorica, r.acf, r.n);
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
        serieSimple(c[0], MANCHAS.valores, 'Manchas solares (número de Wolf)',
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

      const gResid = serieSimple(c[0], inicial.residuales, 'Residuales',
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

      function pintar() {
        const d = MANCHAS.diagnosticos[params.modelo];
        gResid.data.datasets[0].data = d.residuales;
        gResid.data.datasets[0].label = `Residuales de ${d.etiqueta}`;
        gResid.update('none');

        const b = banda(MANCHAS.n);
        gAcf.data.datasets[0].data = d.acf_resid;
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
          },
          { etiqueta: 'Shapiro–Wilk:', valor: `p = ${d.shapiro_p.toFixed(4)}` }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'modelo',
        etiqueta: 'Modelo ajustado',
        opciones: [
          { valor: 'arma10', texto: 'AR(1) — claramente insuficiente' },
          { valor: 'arma20', texto: 'AR(2) — el que propone la identificación' },
          { valor: 'arma30', texto: 'AR(3)' },
          { valor: 'arma21', texto: 'ARMA(2,1) — mejor AICc sobre la serie cruda' }
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

        actualizarLectura(lectura, esRaiz ? [
          { etiqueta: 'Escala:', valor: 'raíz cuadrada' },
          { etiqueta: 'PACF(3), PACF(4):', valor: `${TRANSF.sqrt.pacf[2].toFixed(4)}, ${TRANSF.sqrt.pacf[3].toFixed(4)}` },
          { etiqueta: 'AR(2) — AICc / BIC:', valor: `${TRANSF.sqrt.aicc.toFixed(2)} / ${TRANSF.sqrt.bic.toFixed(2)} — los dos, mínimos de la rejilla` },
          { etiqueta: 'Ljung–Box(12):', valor: `p = ${TRANSF.sqrt.lb12_p.toFixed(4)} ✓` },
          { etiqueta: 'Pseudo-periodo:', valor: `${TRANSF.sqrt.periodo.toFixed(2)} años (ciclo solar ≈ 11)` }
        ] : [
          { etiqueta: 'Escala:', valor: 'original (número de Wolf)' },
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
          'Los once comparten $d = 0$ y el mismo $n$, así que sus criterios son ' +
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
        inicial: 'aicc',
        destacada: 'ARMA(2,0)',
        pie: 'El AR($2$) de Yule —la fila marcada— no es el mínimo de ninguno de los ' +
          'dos criterios sobre la serie cruda, y ordenando por Ljung–Box se ve además ' +
          'que no pasa el diagnóstico. Sobre $\\sqrt{\\text{manchas}}$ la conclusión cambia.'
      };
    };

    AUTOEVALUACIONES['cap3'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'Un AR(2) tiene $\\phi(B) = 1 - 1.2B + 0.9B^2$ y sus raíces tienen módulo $1.054$. ¿Es estacionario?',
        pista: 'La condición no es sobre los coeficientes, es sobre las <em>raíces</em>. Y fíjate bien en la dirección de la desigualdad: ¿dentro o fuera del círculo unitario?',
        opciones: [
          {
            texto: 'No, porque las raíces deberían estar dentro del círculo unitario.',
            correcta: false,
            retro: 'Es al revés, y es la confusión más común del capítulo. El polinomio está escrito en $B$, no en $1/B$: para el AR(1) la raíz es $1/\\phi$, así que $|\\phi| < 1$ equivale a $|1/\\phi| > 1$, es decir, raíz <strong>fuera</strong> del círculo.'
          },
          {
            texto: 'No, porque $\\phi_1 + \\phi_2 = -0.3$ es negativo.',
            correcta: false,
            retro: 'Cuidado con los signos del convenio: en $\\phi(B) = 1 - \\phi_1 B - \\phi_2 B^2$ los coeficientes van restando, así que aquí $\\phi_1 = 1.2$ y $\\phi_2 = -0.9$, y su suma es $0.3$. Además, el signo de esa suma no decide nada por sí solo.'
          },
          {
            texto: 'No se puede saber sin conocer $\\sigma^2$.',
            correcta: false,
            retro: 'La varianza del ruido no interviene: escala la serie, pero no cambia si el proceso olvida o no su pasado. Eso lo deciden únicamente las raíces de $\\phi(B)$.'
          },
          {
            texto: 'Sí, porque el módulo es mayor que 1: las raíces caen fuera del círculo unitario.',
            correcta: true,
            retro: 'Correcto. La condición es $|B_i| > 1$ para todas las raíces. $1.054 > 1$, aunque por poco: es un proceso muy persistente, cerca de la frontera de la no estacionariedad.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 3,
        pregunta: 'Un proceso MA(1) tiene $\\theta = 0.8$. ¿Cuánto vale $\\rho_1$? Da cuatro decimales.',
        pista: 'La fórmula es $\\rho_1 = \\theta/(1+\\theta^2)$. Calcula primero el denominador: $1 + 0.8^2$.',
        respuesta: 0.4878,
        tolerancia: 0.0006,
        retroAcierto: '$0.8/(1+0.64) = 0.8/1.64 = 0.4878$. Fíjate en que se queda por debajo de $0.5$, como tiene que ser: esa es la cota máxima de $|\\rho_1|$ para cualquier MA(1).',
        retroFallo: 'Es $\\rho_1 = \\theta/(1+\\theta^2) = 0.8/1.64 = 0.4878$. Un error frecuente es responder $0.8$, confundiendo el coeficiente con la autocorrelación. En un AR(1) sí coinciden ($\\rho_1 = \\phi$); en un MA, no.'
      },
      {
        tipo: 'grafico',
        modulo: 3,
        alto: 200,
        descripcionGrafico: 'Función de autocorrelación teórica que vale 0.5526 y 0.2632 y después es exactamente cero',
        pregunta: 'Esta es la ACF <strong>teórica</strong> de un proceso, y su PACF (no mostrada) decae sin cortarse. ¿De qué proceso se trata?',
        pista: 'Cuenta cuántas barras hay antes de que la función se haga exactamente cero y se quede ahí. Después mira la tabla del Módulo 5 y fíjate en <em>cuál</em> de las dos funciones es la que se corta.',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS_T, PROCESOS.ma2.acf_teorica, {
          etiqueta: 'ACF teórica', color: COLORES_GRAFICO.primario, tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Un AR(2): tiene dos barras significativas, luego $p = 2$.',
            correcta: false,
            retro: 'Contar barras no basta: hay que mirar cuál de las dos funciones se corta. En un AR(2) es la <strong>PACF</strong> la que cae a cero tras el rezago 2, mientras la ACF decae sin cortarse nunca. Aquí ocurre justo lo contrario.'
          },
          {
            texto: 'Un MA(2): la ACF se corta tras el rezago 2 y la PACF decae.',
            correcta: true,
            retro: 'Exacto. Es el MA(2) con $\\theta = (0.6,\\ 0.4)$: $\\rho_1 = 0.5526$, $\\rho_2 = 0.2632$ y a partir de ahí <strong>exactamente</strong> cero, porque dos observaciones separadas por más de $q = 2$ periodos no comparten ningún choque.'
          },
          {
            texto: 'Un ARMA(2,2), porque hay dos rezagos en cada función.',
            correcta: false,
            retro: 'En un ARMA mixto <strong>ninguna</strong> de las dos funciones se corta: las dos decaen. Un corte limpio y exacto como este descarta precisamente el modelo mixto.'
          },
          {
            texto: 'Ruido blanco con dos valores atípicos.',
            correcta: false,
            retro: 'Es una ACF <strong>teórica</strong>, calculada con <code>ARMAacf()</code>: no hay azar ni atípicos en ella. Y el ruido blanco tendría todas las autocorrelaciones nulas, incluidas las dos primeras.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 4,
        pregunta: 'Marca <strong>todas</strong> las afirmaciones correctas sobre la invertibilidad de un MA.',
        pista: 'Son tres. Piensa en: qué les pasa a los pesos $\\pi$, si los datos pueden distinguir el modelo, y qué hace el software cuando le pides ajustar un MA.',
        opciones: [
          { texto: 'Un MA no invertible tampoco es estacionario.', correcta: false },
          { texto: 'Si $|\\theta| > 1$ en un MA(1), los pesos $\\pi$ de la representación AR($\\infty$) crecen sin límite.', correcta: true },
          { texto: 'La invertibilidad se comprueba con las raíces de $\\phi(B)$.', correcta: false },
          { texto: 'Los valores $\\theta$ y $1/\\theta$ producen exactamente la misma ACF, así que ningún dato los distingue.', correcta: true },
          { texto: '<code>arima()</code> devuelve siempre la solución invertible, aunque hayas simulado la otra.', correcta: true }
        ],
        retroAcierto: 'Las tres describen el mismo hecho desde tres ángulos: la representación AR($\\infty$) diverge, el modelo no queda identificado, y por eso el software impone el convenio $|\\theta| < 1$. Puedes verlo en el simulador del Módulo 4 llevando $\\theta$ más allá de 1.',
        retroFallo: 'Las tres correctas son las que hablan de los pesos de la representación AR($\\infty$), de la identificación del modelo y del convenio que impone el software. Las dos falsas confunden los dos polinomios: un MA($q$) es <strong>siempre estacionario</strong> —es una suma finita de ruido blanco, sin condición alguna— y la invertibilidad se lee en las raíces de $\\theta(B)$, no de $\\phi(B)$. Cada polinomio responde por lo suyo.'
      },
      {
        tipo: 'numerica',
        modulo: 9,
        unidad: 'años',
        pregunta: 'El AR(2) ajustado a $\\sqrt{\\text{manchas}}$ tiene $\\phi_1 = 1.4027$ y $\\phi_2 = -0.6853$. Calcula su pseudo-periodo con $2\\pi/\\arccos\\!\\big(\\phi_1/(2\\sqrt{-\\phi_2})\\big)$. Da dos decimales.',
        pista: 'Ve por partes: $\\sqrt{0.6853} = 0.8278$, y el argumento del arcocoseno es $1.4027/(2 \\times 0.8278)$. Asegúrate de que tu calculadora trabaja en <strong>radianes</strong>.',
        respuesta: 11.22,
        tolerancia: 0.06,
        retroAcierto: 'El argumento es $0.8472$, su arcocoseno $0.5601$ radianes y $2\\pi/0.5601 = 11.22$ años. El ciclo solar documentado por los astrónomos es de unos 11 años: el modelo lo recupera de los datos, sin que se le haya dicho nada de astronomía.',
        retroFallo: 'El cálculo es $2\\pi/\\arccos(1.4027/(2\\sqrt{0.6853})) = 2\\pi/\\arccos(0.8472) = 2\\pi/0.5601 = 11.22$ años. Los dos tropiezos habituales: usar grados en vez de radianes, u olvidar el signo menos dentro de la raíz — $\\phi_2$ es negativo, y $\\sqrt{-\\phi_2}$ es un número real precisamente por eso.'
      },
      {
        tipo: 'opcion',
        modulo: 8,
        pregunta: 'Ajustas un ARMA(2,1) y evalúas Ljung–Box con <code>Box.test(residuals(m), lag = 12, type = "Ljung-Box")</code>, sin más argumentos. ¿Qué problema tiene esa llamada?',
        pista: 'Compara los grados de libertad que usa la prueba por defecto con los que debería usar cuando los residuales vienen de un modelo <em>estimado</em>. ¿En qué dirección se equivoca?',
        opciones: [
          {
            texto: 'Ninguno: <code>Box.test()</code> descuenta los parámetros automáticamente.',
            correcta: false,
            retro: 'No lo hace. <code>fitdf</code> vale $0$ por defecto, porque la función no sabe de dónde vienen los residuales que le pasas: podrían ser datos crudos. Hay que decírselo siempre.'
          },
          {
            texto: 'Falta <code>fitdf = 3</code>, y sin él la prueba rechaza demasiado a menudo.',
            correcta: false,
            retro: 'El argumento que falta es el correcto, pero la dirección del error es la contraria. Más grados de libertad significa un valor crítico más alto y por tanto un $p$-valor mayor: la prueba rechaza <em>menos</em>, y aprueba modelos que debería suspender.'
          },
          {
            texto: 'Falta <code>fitdf = 3</code>: sin él la prueba usa demasiados grados de libertad y se vuelve demasiado indulgente.',
            correcta: true,
            retro: 'Correcto. Con $p+q = 3$ parámetros estimados, el estadístico se distribuye $\\chi^2_{12-3}$, no $\\chi^2_{12}$. El caso más elocuente es el AR(2) de las manchas, donde $p+q = 2$: omitir <code>fitdf</code> cambia su $p$-valor de $0.0461$ (se rechaza) a $0.0996$ (no se rechaza). La conclusión se invierte por omitir un argumento.'
          },
          {
            texto: 'El rezago 12 es demasiado alto para una serie anual.',
            correcta: false,
            retro: 'La elección de $h$ admite discusión —lo habitual es $h \\approx 10$ o $\\min(10,\\ T/5)$— pero no es un error. El problema está en otro sitio, y es uno que invierte la conclusión.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 8,
        alto: 200,
        descripcionGrafico: 'ACF de los residuales de un AR(1) ajustado a las manchas solares, con varias barras muy fuera de la banda',
        pregunta: 'Esta es la ACF de los residuales de un AR(1) ajustado a las manchas solares. ¿Qué haces?',
        pista: 'Antes de decidir, mira <em>cuánto</em> se salen las barras de la banda y en qué rezagos. ¿Es un pico aislado y pequeño —compatible con el azar— o hay estructura de verdad?',
        dibujar: canvas => crearGraficoBarras(canvas, REZAGOS, MANCHAS.diagnosticos.arma10.acf_resid, {
          etiqueta: 'ACF de los residuales', color: '#dc2626',
          lineas: lineasBanda(MANCHAS.n), tituloX: 'Rezago k'
        }),
        opciones: [
          {
            texto: 'Rechazo el modelo: quedan autocorrelaciones grandes, hay que aumentar el orden.',
            correcta: true,
            retro: 'Correcto. $r_1 = 0.556$ frente a una banda de $\\pm 0.196$, y no está sola: eso no es azar, es estructura sin modelar. Ljung–Box da $p < 0.0001$. Subiendo a AR(2), esas autocorrelaciones bajan a $0.1297$ y $-0.1477$.'
          },
          {
            texto: 'Lo acepto: uno o dos picos fuera de la banda son normales con 20 rezagos.',
            correcta: false,
            retro: 'Esa regla es buena, pero se aplica a picos <em>pequeños y aislados</em>, apenas asomados. Aquí $r_1 = 0.556$ casi triplica la banda y hay más barras fuera. La regla del 5 % explica ruido, no una señal así.'
          },
          {
            texto: 'Diferencio la serie, porque la ACF de los residuales decae despacio.',
            correcta: false,
            retro: 'Diferenciar es la respuesta a una raíz unitaria en la <em>serie</em>, no a un mal ajuste. Estos residuales vienen de un modelo insuficiente sobre una serie que ya es estacionaria; diferenciar aquí sobrediferenciaría e introduciría un MA(1) espurio.'
          },
          {
            texto: 'Aplico una transformación logarítmica para estabilizar la varianza.',
            correcta: false,
            retro: 'La transformación resuelve problemas de <em>escala</em>, que se ven en la serie (amplitud que crece con el nivel), no en la ACF de los residuales. Y en esta serie el logaritmo es además imposible: hay un año con cero manchas.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 7,
        pregunta: 'Marca <strong>todas</strong> las afirmaciones correctas sobre los métodos de estimación.',
        pista: 'Son tres. Piensa en: para qué modelos sirve Yule–Walker, qué ignora exactamente CSS, y qué hace <code>arima()</code> cuando no le indicas ningún método.',
        opciones: [
          { texto: 'Yule–Walker solo sirve para modelos AR puros, porque parte de las ecuaciones de momentos del AR.', correcta: true },
          { texto: 'Los tres métodos dan siempre las mismas estimaciones salvo por errores de redondeo.', correcta: false },
          { texto: 'CSS ignora la contribución de las primeras observaciones a la verosimilitud.', correcta: true },
          { texto: 'El $\\hat\\sigma^2$ de Yule–Walker es comparable con el de máxima verosimilitud para calcular el AIC.', correcta: false },
          { texto: 'Por defecto <code>arima()</code> usa <code>"CSS-ML"</code>: arranca con CSS y termina maximizando la verosimilitud exacta.', correcta: true }
        ],
        retroAcierto: 'Las tres. Y el contraejemplo de las dos falsas está en el propio capítulo: sobre las manchas solares, Yule–Walker y ML se separaron $1.26$ y $1.10$ errores estándar, y sus $\\hat\\sigma^2$ fueron $298.96$ frente a $229.43$.',
        retroFallo: 'Las tres correctas son las que hablan de Yule–Walker, de lo que ignora CSS y del <code>"CSS-ML"</code> por defecto. Las dos falsas son justo lo que el módulo desmiente con números: los métodos <strong>no</strong> coinciden —YW quedó a más de un error estándar de ML— y sus $\\hat\\sigma^2$ no miden lo mismo, así que mezclar salidas de <code>ar()</code> y <code>arima()</code> para comparar criterios de información no tiene sentido.'
      }
    ];
