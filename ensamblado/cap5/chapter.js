    // ================================================================
    // Datos y ayudantes del capítulo, tomados del precálculo en R
    // ================================================================
    const AP = DATOS_CAP5.airpassengers;
    const UAD = DATOS_CAP5.usaccdeaths;
    const CONTRA = DATOS_CAP5.trm_contraejemplo;
    const CO2 = DATOS_CAP5.co2;
    const TEORICAS = DATOS_CAP5.teoricas;
    const M_EST = DATOS_CAP5.m;
    const REZAGOS = etiquetasRezago(DATOS_CAP5.max_rezago);
    const REZAGOS24 = etiquetasRezago(24);
    const MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                   'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

    function banda(n) { return 1.96 / Math.sqrt(n); }

    function lineasBanda(n) {
      const b = banda(n);
      return [
        { valor: b, etiqueta: 'Banda ±1.96/√n' },
        { valor: -b, etiqueta: '' }
      ];
    }

    // Etiquetas mensuales AAAA-MM.
    function mesesDesde(anio, mes, n) {
      const salida = [];
      let a = anio, m = mes;
      for (let i = 0; i < n; i++) {
        salida.push(`${a}-${String(m).padStart(2, '0')}`);
        m += 1;
        if (m > 12) { m = 1; a += 1; }
      }
      return salida;
    }

    // Diferencia estacional de periodo m, aplicada D veces. Ojo: NO es
    // `diferenciar(y, m)`, que sería la diferencia regular m veces.
    function diferenciarEstacional(y, D, m = M_EST) {
      let x = y.slice();
      for (let k = 0; k < D; k++) {
        const z = [];
        for (let t = m; t < x.length; t++) z.push(x[t] - x[t - m]);
        x = z;
      }
      return x;
    }

    function media(x) { return x.reduce((a, b) => a + b, 0) / x.length; }

    function varianzaDe(x) {
      const m = media(x);
      return x.reduce((a, b) => a + (b - m) * (b - m), 0) / (x.length - 1);
    }

    // Defensiva ante null: jsonlite escribe los valores infinitos como null y
    // Number(null) es 0, que en pantalla se leería como un cero legítimo.
    function fmt(x, d = 2) {
      if (x === null || x === undefined || !Number.isFinite(Number(x))) return '—';
      return Number(x).toLocaleString('es-CO', {
        minimumFractionDigits: d, maximumFractionDigits: d
      });
    }

    // Casi todos los simuladores de este capítulo destruyen y recrean sus
    // gráficos al repintar. `graficosActivos` guarda referencias fijas, así que
    // hay que devolver un objeto estable que destruya el gráfico VIGENTE.
    function manejador(dame) {
      return { destroy() { const g = dame(); if (g) g.destroy(); } };
    }

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

    // ---- Álgebra de polinomios estacionales --------------------------------
    // Convención: el vector guarda los coeficientes de 1, B, B^2, ... con el 1
    // incluido, igual que en el precálculo de R.
    function multPoli(a, b) {
      const r = new Array(a.length + b.length - 1).fill(0);
      for (let i = 0; i < a.length; i++)
        for (let j = 0; j < b.length; j++) r[i + j] += a[i] * b[j];
      return r;
    }

    function poliEstacional(coef, m = M_EST) {
      const v = new Array(m + 1).fill(0);
      v[0] = 1; v[m] = coef;
      return v;
    }

    function recortaCeros(v) {
      let ultimo = -1;
      for (let i = 0; i < v.length; i++) if (Math.abs(v[i]) > 1e-12) ultimo = i;
      return v.slice(0, ultimo + 1);
    }

    // Pesos psi de la representación MA(infinito): psi_j = ma_j + sum ar_i psi_{j-i}
    // `ar` son los coeficientes del lado derecho (y_t = ar_1 y_{t-1} + ...),
    // `ma` los de los choques rezagados.
    function pesosPsi(ar, ma, n) {
      const psi = [1];
      for (let j = 1; j < n; j++) {
        let v = j <= ma.length ? ma[j - 1] : 0;
        for (let i = 1; i <= Math.min(j, ar.length); i++) v += ar[i - 1] * psi[j - i];
        psi.push(v);
      }
      return psi;
    }

    // ACF teórica a partir de los pesos psi: gamma_k = sigma^2 * sum psi_j psi_{j+k}.
    // Con procesos estacionarios y psi suficientemente largo, coincide con
    // ARMAacf de R (verificado a 4 decimales en los seis procesos del Módulo 4).
    function acfDesdePsi(psi, maxLag) {
      const g = [];
      for (let k = 0; k <= maxLag; k++) {
        let s = 0;
        for (let j = 0; j + k < psi.length; j++) s += psi[j] * psi[j + k];
        g.push(s);
      }
      return g.slice(1).map(v => v / g[0]);
    }

    // `matrizMesAnio` vive en el componente .mapa-estacional (región compartida),
    // no aquí: la usan también el capítulo 1 y la plantilla.

    // Series del capítulo, con su punto de arranque, para las transformaciones
    // que se calculan en el navegador.
    const SERIES_MAPA = {
      airpassengers: { nombre: 'AirPassengers (pasajeros/mes)', datos: SERIES_CAP5.airpassengers, admiteLog: true },
      usaccdeaths: { nombre: 'USAccDeaths (muertes/mes)', datos: SERIES_CAP5.usaccdeaths, admiteLog: true },
      co2: { nombre: 'co2 de Mauna Loa (ppm)', datos: SERIES_CAP5.co2, admiteLog: true },
      trm: { nombre: 'TRM (COP por USD)', datos: SERIES_CAP5.trm, admiteLog: true }
    };

    // ================================================================
    // Módulo 1 · Mapa estacional y correlograma en paralelo
    // ================================================================
    SIMULADORES['mapa-firma'] = function (raiz) {
      // El logaritmo va en un interruptor aparte de las diferencias: con los dos
      // combinados en un solo selector no se podía reproducir la fila de la TRM
      // de la tabla siguiente, que se calcula SIN logaritmo.
      const params = { serie: 'airpassengers', dif: 'ninguna', log: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const mapa = raiz.querySelector('.mapa-estacional');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const DIFERENCIAS = {
        ninguna: { texto: 'Sin diferenciar', d: 0, D: 0 },
        d1: { texto: 'Regular ∇', d: 1, D: 0 },
        D1: { texto: 'Estacional ∇₁₂', d: 0, D: 1 },
        d1D1: { texto: 'Ambas: ∇ ∇₁₂', d: 1, D: 1 }
      };

      function pintar() {
        const info = SERIES_MAPA[params.serie];
        const t = DIFERENCIAS[params.dif];
        let y = info.datos.valores.slice();
        if (params.log) y = y.map(v => Math.log(v));
        // El orden importa para el número de observaciones que se pierden:
        // primero la estacional, después la regular (Módulo 3).
        if (t.D > 0) y = diferenciarEstacional(y, t.D);
        if (t.d > 0) y = diferenciar(y, t.d);

        const perdidas = info.datos.valores.length - y.length;
        let anio = info.datos.inicio[0], mes = info.datos.inicio[1] + perdidas;
        anio += Math.floor((mes - 1) / 12); mes = ((mes - 1) % 12) + 1;

        const diferenciada = t.d + t.D > 0;
        const decimales = params.log ? (diferenciada ? 3 : 2) : (diferenciada ? 1 : 0);
        const etiquetaTrans = (params.log ? 'log · ' : '') + t.texto;
        pintarMapaEstacional(mapa, Object.assign(
          matrizMesAnio(y, anio, mes),
          {
            escala: diferenciada ? 'divergente' : 'secuencial',
            decimales: decimales,
            unidad: '',
            nota: `<strong>${info.nombre}</strong> · ${etiquetaTrans}. ` +
              (diferenciada
                ? 'Escala divergente centrada en cero: naranja por debajo, verde por encima.'
                : 'Escala secuencial: cuanto más oscuro, más alto.')
          }));

        const maxLag = Math.min(DATOS_CAP5.max_rezago, y.length - 2);
        const acf = calcularACF(y, maxLag);
        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetasRezago(maxLag), acf, {
          etiqueta: 'ACF muestral',
          lineas: lineasBanda(y.length),
          tituloX: 'Rezago'
        });

        const b = banda(y.length);
        const fuera = [12, 24, 36].filter(k => k <= maxLag && Math.abs(acf[k - 1]) > b);
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'ρ̂₁', valor: fmt(acf[0], 4) },
          { etiqueta: 'ρ̂₁₂', valor: maxLag >= 12 ? fmt(acf[11], 4) : '—' },
          { etiqueta: 'ρ̂₂₄', valor: maxLag >= 24 ? fmt(acf[23], 4) : '—' },
          { etiqueta: 'banda', valor: '±' + fmt(b, 4) },
          {
            etiqueta: 'rezagos estacionales fuera de banda',
            valor: fuera.length ? fuera.join(', ') : 'ninguno'
          }
        ]);
      }

      crearSelector(controles, {
        clave: 'serie', etiqueta: 'Serie',
        opciones: Object.keys(SERIES_MAPA).map(k => ({ valor: k, texto: SERIES_MAPA[k].nombre }))
      }, params, pintar);
      crearSelector(controles, {
        clave: 'dif', etiqueta: 'Diferenciación',
        opciones: Object.keys(DIFERENCIAS).map(k => ({ valor: k, texto: DIFERENCIAS[k].texto }))
      }, params, pintar);
      crearInterruptores(controles, [
        { clave: 'log', etiqueta: 'Tomar logaritmo' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 2 · Constructor de polinomios SARIMA
    // ================================================================
    SIMULADORES['constructor-polinomio'] = function (raiz) {
      const params = { p: 1, d: 1, q: 1, P: 1, D: 1, Q: 1 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        // Polinomio AR completo: phi(B) * Phi(B^m) * (1-B)^d * (1-B^m)^D.
        // Se usan coeficientes de ejemplo, porque lo que se quiere ver es la
        // ESTRUCTURA de rezagos, no unos valores concretos.
        let poli = [1];
        for (let i = 1; i <= params.p; i++) poli = multPoli(poli, [1, -0.5 / i]);
        for (let i = 1; i <= params.P; i++) poli = multPoli(poli, poliEstacional(-0.6 / i));
        for (let i = 0; i < params.d; i++) poli = multPoli(poli, [1, -1]);
        for (let i = 0; i < params.D; i++) poli = multPoli(poli, poliEstacional(-1));

        const coefs = poli.slice(1).map(v => -v);   // lado derecho de la ecuación
        const etiquetas = coefs.map((_, i) => String(i + 1));
        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetas, coefs, {
          etiqueta: 'Coeficiente del rezago',
          tituloX: 'Rezago',
          min: Math.min(-1.2, ...coefs) - 0.1,
          max: Math.max(1.2, ...coefs) + 0.1
        });

        const libres = params.p + params.q + params.P + params.Q;
        const rezagoMax = coefs.length;
        const noNulos = coefs.filter(v => Math.abs(v) > 1e-12).length;
        const perdidas = params.d + params.D * M_EST;
        actualizarLectura(lectura, [
          { etiqueta: 'modelo', valor: `(${params.p},${params.d},${params.q})(${params.P},${params.D},${params.Q})[12]` },
          { etiqueta: 'parámetros libres', valor: libres },
          { etiqueta: 'rezago más lejano del polinomio AR', valor: rezagoMax },
          { etiqueta: 'rezagos AR no nulos', valor: noNulos },
          { etiqueta: 'observaciones que cuestan las diferencias', valor: perdidas },
          { etiqueta: 'quedan de las 144', valor: 144 - perdidas }
        ]);
      }

      [['p', 'p (AR regular)'], ['d', 'd (dif. regular)'], ['q', 'q (MA regular)'],
       ['P', 'P (AR estacional)'], ['D', 'D (dif. estacional)'], ['Q', 'Q (MA estacional)']]
        .forEach(([clave, etiqueta]) => {
          crearControles(controles, [{
            clave: clave, etiqueta: etiqueta, min: 0, max: 2, paso: 1, decimales: 0
          }], params, pintar);
        });

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 3 · Las cuatro combinaciones (d, D)
    // ================================================================
    SIMULADORES['cuatro-combinaciones'] = function (raiz) {
      const params = { regular: true, estacional: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelectorAll('canvas');
      let serie = null, correlograma = null;

      function pintar() {
        const clave = `d${params.regular ? 1 : 0}_D${params.estacional ? 1 : 0}`;
        const c = AP.combinaciones[clave];
        if (serie) serie.destroy();
        serie = lineaSimple(canvas[0], c.fechas, c.valores, c.etiqueta,
          COLORES_GRAFICO.primario, { plugins: { legend: { display: true } } });

        if (correlograma) correlograma.destroy();
        correlograma = crearGraficoBarras(canvas[1], REZAGOS, c.acf, {
          etiqueta: 'ACF muestral',
          lineas: lineasBanda(c.n),
          tituloX: 'Rezago'
        });

        actualizarLectura(lectura, [
          { etiqueta: 'd', valor: c.d },
          { etiqueta: 'D', valor: c.D },
          { etiqueta: 'n', valor: c.n },
          { etiqueta: 'varianza', valor: fmt(c.varianza, 6) },
          { etiqueta: 'ρ̂₁', valor: fmt(c.acf1, 4) },
          { etiqueta: 'ρ̂₁₂', valor: fmt(c.acf12, 4) }
        ]);
      }

      crearInterruptores(controles, [
        { clave: 'regular', etiqueta: 'Diferencia regular ∇' },
        { clave: 'estacional', etiqueta: 'Diferencia estacional ∇₁₂' }
      ], params, pintar);

      pintar();
      return [manejador(() => serie), manejador(() => correlograma)];
    };

    // ================================================================
    // Módulo 3 · Sobrediferenciación estacional
    // ================================================================
    SIMULADORES['sobrediferenciacion-estacional'] = function (raiz) {
      const params = { D: 1 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const D = Math.round(params.D);
        const info = AP.sobrediferenciacion_estacional[D];
        let y = SERIES_CAP5.airpassengers.valores.map(v => Math.log(v));
        y = diferenciar(diferenciarEstacional(y, D), 1);
        const perdidas = 144 - y.length;
        const etiquetas = mesesDesde(
          SERIES_CAP5.airpassengers.inicio[0] + Math.floor(perdidas / 12),
          ((SERIES_CAP5.airpassengers.inicio[1] - 1 + perdidas) % 12) + 1, y.length);

        if (grafico) grafico.destroy();
        grafico = lineaSimple(canvas, etiquetas, y,
          `∇ ∇₁₂^${D} log(AirPassengers)`, COLORES_GRAFICO.primario,
          { plugins: { legend: { display: true } } });

        const alarma = Math.abs(info.raiz_ma) > 0.99;
        actualizarLectura(lectura, [
          { etiqueta: 'D', valor: D },
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'varianza (R)', valor: fmt(info.varianza, 6) },
          { etiqueta: 'varianza (calculada aquí)', valor: fmt(varianzaDe(y), 6) },
          { etiqueta: 'Θ̂', valor: fmt(info.theta_est, 4) },
          { etiqueta: '|raíz MA|⁻¹', valor: fmt(info.raiz_ma, 4) },
          { etiqueta: 'diagnóstico', valor: alarma ? '⚠ raíz sobre el círculo: sobrediferenciada' : 'invertible' }
        ]);
      }

      crearControles(controles, [{
        clave: 'D', etiqueta: 'Diferencias estacionales D', min: 0, max: 2, paso: 1, decimales: 0
      }], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 4 · Laboratorio de firmas estacionales
    // ================================================================
    SIMULADORES['firma-teorica'] = function (raiz) {
      const params = { phi: 0, theta: 0, Phi: 0.7, Theta: 0 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelectorAll('canvas');
      let gAcf = null, gPacf = null;

      function pintar() {
        const polAr = multPoli([1, -params.phi], poliEstacional(-params.Phi));
        const polMa = multPoli([1, params.theta], poliEstacional(params.Theta));
        const ar = recortaCeros(polAr.slice(1).map(v => -v));
        const ma = recortaCeros(polMa.slice(1));
        const psi = pesosPsi(ar, ma, 1500);
        const acf = acfDesdePsi(psi, DATOS_CAP5.max_rezago);
        const pacf = calcularPACF(acf, DATOS_CAP5.max_rezago);

        if (gAcf) gAcf.destroy();
        gAcf = crearGraficoBarras(canvas[0], REZAGOS, acf,
          { etiqueta: 'ACF teórica', tituloX: 'Rezago' });
        if (gPacf) gPacf.destroy();
        gPacf = crearGraficoBarras(canvas[1], REZAGOS, pacf,
          { etiqueta: 'PACF teórica', color: COLORES_GRAFICO.secundario, tituloX: 'Rezago' });

        const satelite = (Math.abs(acf[10]) + Math.abs(acf[12])) / 2;
        actualizarLectura(lectura, [
          { etiqueta: 'ρ₁', valor: fmt(acf[0], 4) },
          { etiqueta: 'ρ₁₁', valor: fmt(acf[10], 4) },
          { etiqueta: 'ρ₁₂', valor: fmt(acf[11], 4) },
          { etiqueta: 'ρ₁₃', valor: fmt(acf[12], 4) },
          { etiqueta: 'ρ₂₄', valor: fmt(acf[23], 4) },
          { etiqueta: 'ρ₁·ρ₁₂', valor: fmt(acf[0] * acf[11], 4) },
          { etiqueta: 'satélites (media de |ρ₁₁|,|ρ₁₃|)', valor: fmt(satelite, 4) }
        ]);
      }

      crearControles(controles, [
        { clave: 'phi', etiqueta: 'φ₁ (AR regular)', min: -0.85, max: 0.85, paso: 0.05, decimales: 2 },
        { clave: 'theta', etiqueta: 'θ₁ (MA regular)', min: -0.85, max: 0.85, paso: 0.05, decimales: 2 },
        { clave: 'Phi', etiqueta: 'Φ₁ (AR estacional, m=12)', min: -0.85, max: 0.85, paso: 0.05, decimales: 2 },
        { clave: 'Theta', etiqueta: 'Θ₁ (MA estacional, m=12)', min: -0.85, max: 0.85, paso: 0.05, decimales: 2 }
      ], params, pintar);

      pintar();
      return [manejador(() => gAcf), manejador(() => gPacf)];
    };

    // ================================================================
    // Módulo 5 · Los pesos psi del modelo airline
    // ================================================================
    SIMULADORES['airline-pesos'] = function (raiz) {
      const params = { theta: -0.40, Theta: -0.56 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelectorAll('canvas');
      const sigma2 = AP.airline.sigma2;
      const H = 36;
      let gPsi = null, gSigma = null;

      function pintar() {
        // (1-B)(1-B^12) en el lado AR; (1+theta B)(1+Theta B^12) en el MA.
        const polAr = multPoli([1, -1], poliEstacional(-1));
        const polMa = multPoli([1, params.theta], poliEstacional(params.Theta));
        const ar = polAr.slice(1).map(v => -v);
        const ma = polMa.slice(1);
        const psi = pesosPsi(ar, ma, H + 1);
        const sigmaH = [];
        let acumulado = 0;
        for (let h = 1; h <= H; h++) {
          acumulado += psi[h - 1] * psi[h - 1];
          sigmaH.push(Math.sqrt(acumulado * sigma2));
        }

        const etiquetas = Array.from({ length: H }, (_, i) => String(i));
        if (gPsi) gPsi.destroy();
        gPsi = crearGraficoBarras(canvas[0], etiquetas, psi.slice(0, H), {
          etiqueta: 'ψⱼ', tituloX: 'j', min: -0.2, max: 1.4
        });
        if (gSigma) gSigma.destroy();
        gSigma = lineaSimple(canvas[1], Array.from({ length: H }, (_, i) => String(i + 1)),
          sigmaH, 'σₕ', COLORES_GRAFICO.secundario,
          { plugins: { legend: { display: true } } });

        actualizarLectura(lectura, [
          { etiqueta: 'ψ₁ = 1+θ', valor: fmt(psi[1], 4) },
          { etiqueta: 'ψ₁₂', valor: fmt(psi[12], 4) },
          { etiqueta: 'ψ₁₃', valor: fmt(psi[13], 4) },
          { etiqueta: 'σ₁', valor: fmt(sigmaH[0], 6) },
          { etiqueta: 'σ₁₂', valor: fmt(sigmaH[11], 6) },
          { etiqueta: 'σ₂₄', valor: fmt(sigmaH[23], 6) },
          { etiqueta: 'σ₁₂/σ₁', valor: fmt(sigmaH[11] / sigmaH[0], 3) + ' (caminata: 3.464)' }
        ]);
      }

      crearControles(controles, [
        { clave: 'theta', etiqueta: 'θ (MA regular)', min: -0.95, max: 0.5, paso: 0.01, decimales: 2 },
        { clave: 'Theta', etiqueta: 'Θ (MA estacional)', min: -0.95, max: 0.5, paso: 0.01, decimales: 2 }
      ], params, pintar);

      pintar();
      return [manejador(() => gPsi), manejador(() => gSigma)];
    };

    // ================================================================
    // Módulo 6 · Explorador de modelos SARIMA
    // ================================================================
    SIMULADORES['explorador-sarima'] = function (raiz) {
      const params = { p: '0', q: '1', P: '0', Q: '1' };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      const mejorAicc = AP.rejilla[AP.mejores_aicc[0]].aicc;
      let grafico = null;

      function pintar() {
        const clave = `(${params.p},1,${params.q})(${params.P},1,${params.Q})[12]`;
        const m = AP.rejilla[clave];
        if (!m) {
          actualizarLectura(lectura, [{ etiqueta: 'modelo', valor: clave + ' — no convergió' }]);
          return;
        }
        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, REZAGOS24, m.acf, {
          etiqueta: 'ACF de los residuales',
          lineas: lineasBanda(144),
          tituloX: 'Rezago'
        });

        const esMejor = clave === AP.mejores_aicc[0];
        actualizarLectura(lectura, [
          { etiqueta: 'modelo', valor: clave + (esMejor ? '  ★ mínimo AICc y BIC' : '') },
          { etiqueta: 'parámetros', valor: m.n_par },
          { etiqueta: 'n efectivo', valor: m.nobs },
          { etiqueta: 'AICc', valor: fmt(m.aicc, 4) },
          { etiqueta: 'diferencia con el mejor', valor: fmt(m.aicc - mejorAicc, 4) },
          { etiqueta: 'BIC', valor: fmt(m.bic, 4) },
          { etiqueta: 'Ljung–Box(24) p', valor: fmt(m.lb_p, 4) + (m.lb_p < 0.05 ? '  ⚠ rechaza' : '') },
          { etiqueta: 'ρ̂₁₂ residual', valor: fmt(m.acf12, 4) },
          { etiqueta: '|raíz MA|⁻¹', valor: m.raiz_ma === null ? '—' : fmt(m.raiz_ma, 4) }
        ]);
      }

      [['p', 'p'], ['q', 'q']].forEach(([clave, etiqueta]) => {
        crearSelector(controles, {
          clave: clave, etiqueta: `${etiqueta} (regular)`,
          opciones: ['0', '1', '2'].map(v => ({ valor: v, texto: v }))
        }, params, pintar);
      });
      [['P', 'P'], ['Q', 'Q']].forEach(([clave, etiqueta]) => {
        crearSelector(controles, {
          clave: clave, etiqueta: `${etiqueta} (estacional)`,
          opciones: ['0', '1'].map(v => ({ valor: v, texto: v }))
        }, params, pintar);
      });

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 7 · Pronóstico estacional con bandas
    // ================================================================
    SIMULADORES['pronostico-estacional'] = function (raiz) {
      const params = { h: 24, original: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      const pron = AP.pronostico;
      let grafico = null;

      function pintar() {
        const h = Math.round(params.h);
        const esc = params.original ? pron.original : pron.log;
        const observado = params.original
          ? SERIES_CAP5.airpassengers.valores
          : AP.log;
        // Se muestran los últimos 4 años de historia para que el abanico se vea.
        const corte = observado.length - 48;
        const historia = observado.slice(corte);
        const etiquetasHist = AP.fechas.slice(corte);
        const etiquetas = etiquetasHist.concat(pron.fechas.slice(0, h));
        const relleno = new Array(historia.length - 1).fill(null);

        const serie = historia.concat(new Array(h).fill(null));
        const union = relleno.concat([historia[historia.length - 1]]);
        const datos = campo => union.concat(esc[campo].slice(0, h));

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, etiquetas, [
          { label: 'Observado', data: serie, borderColor: COLORES_GRAFICO.primario, borderWidth: 1.8, pointRadius: 0 },
          { label: 'IC 95 %', data: datos('hi95'), borderColor: 'rgba(255,102,0,0.25)', backgroundColor: 'rgba(255,102,0,0.12)', borderWidth: 1, pointRadius: 0, fill: '+1' },
          { label: '', data: datos('lo95'), borderColor: 'rgba(255,102,0,0.25)', borderWidth: 1, pointRadius: 0, fill: false },
          { label: 'IC 80 %', data: datos('hi80'), borderColor: 'rgba(255,102,0,0.45)', backgroundColor: 'rgba(255,102,0,0.22)', borderWidth: 1, pointRadius: 0, fill: '+1' },
          { label: '', data: datos('lo80'), borderColor: 'rgba(255,102,0,0.45)', borderWidth: 1, pointRadius: 0, fill: false },
          { label: 'Pronóstico', data: datos('media'), borderColor: COLORES_GRAFICO.secundario, borderWidth: 2, pointRadius: 0, borderDash: [6, 3] }
        ], { plugins: { legend: { display: true } } });

        const i = h - 1;
        const ancho = esc.hi95[i] - esc.lo95[i];
        const abajo = esc.media[i] - esc.lo95[i];
        const arriba = esc.hi95[i] - esc.media[i];
        actualizarLectura(lectura, [
          { etiqueta: 'horizonte h', valor: h + ' meses (' + pron.fechas[i] + ')' },
          { etiqueta: 'escala', valor: params.original ? 'original (pasajeros)' : 'logarítmica' },
          { etiqueta: 'pronóstico', valor: fmt(esc.media[i], params.original ? 2 : 4) },
          { etiqueta: 'IC 95 %', valor: `[${fmt(esc.lo95[i], params.original ? 2 : 4)}, ${fmt(esc.hi95[i], params.original ? 2 : 4)}]` },
          { etiqueta: 'ancho del IC', valor: fmt(ancho, params.original ? 2 : 4) },
          { etiqueta: 'asimetría (abajo / arriba)', valor: `${fmt(abajo, 2)} / ${fmt(arriba, 2)}` },
          { etiqueta: 'σₕ (escala log)', valor: fmt(pron.sigma_h[i], 6) }
        ]);
      }

      crearControles(controles, [{
        clave: 'h', etiqueta: 'Horizonte h (meses)', min: 1, max: 24, paso: 1, decimales: 0
      }], params, pintar);
      crearInterruptores(controles, [
        { clave: 'original', etiqueta: 'Escala original (en vez de logarítmica)' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 8 · El contraejemplo: con estacionalidad y sin ella
    // ================================================================
    SIMULADORES['contraejemplo-trm'] = function (raiz) {
      const params = { serie: 'ap' };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const CASOS = {
        ap: {
          texto: '∇ log(AirPassengers)',
          acf: AP.combinaciones.d1_D0.acf,
          n: AP.combinaciones.d1_D0.n,
          veredicto: 'Estacional: los tres múltiplos de 12 salen de la banda.'
        },
        trm: {
          texto: '∇ TRM',
          acf: CONTRA.correlogramas.acf,
          n: CONTRA.correlogramas.n,
          veredicto: 'No estacional: ninguno de los tres se acerca a la banda.'
        }
      };

      function pintar() {
        const c = CASOS[params.serie];
        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, REZAGOS, c.acf, {
          etiqueta: 'ACF de la serie diferenciada',
          color: params.serie === 'ap' ? COLORES_GRAFICO.primario : COLORES_GRAFICO.terciario,
          lineas: lineasBanda(c.n),
          tituloX: 'Rezago'
        });
        const b = banda(c.n);
        const fuera = [12, 24, 36].filter(k => Math.abs(c.acf[k - 1]) > b);
        actualizarLectura(lectura, [
          { etiqueta: 'serie', valor: c.texto },
          { etiqueta: 'n', valor: c.n },
          { etiqueta: 'ρ̂₁₂', valor: fmt(c.acf[11], 4) },
          { etiqueta: 'ρ̂₂₄', valor: fmt(c.acf[23], 4) },
          { etiqueta: 'ρ̂₃₆', valor: fmt(c.acf[35], 4) },
          { etiqueta: 'banda', valor: '±' + fmt(b, 4) },
          { etiqueta: 'fuera de banda', valor: fuera.length ? fuera.join(', ') : 'ninguno' },
          { etiqueta: 'veredicto', valor: c.veredicto }
        ]);
      }

      crearSelector(controles, {
        clave: 'serie', etiqueta: 'Serie (ya diferenciada)',
        opciones: [{ valor: 'ap', texto: CASOS.ap.texto }, { valor: 'trm', texto: CASOS.trm.texto }]
      }, params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 9 · Regresores de calendario
    // ================================================================
    SIMULADORES['calendario-regresores'] = function (raiz) {
      const params = { dias: true, pascua: false };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      const cal = AP.calendario;
      const baseAicc = cal.modelos.sin_regresores.aicc;
      // Indicadora de Semana Santa reconstruida desde las fechas del precálculo.
      const esPascua = cal.fechas.map(f => {
        const anio = f.slice(0, 4), mes = f.slice(5, 7);
        const p = cal.pascuas[anio];
        return p && p.slice(5, 7) === mes ? 1 : 0;
      });
      let grafico = null;

      function pintar() {
        const clave = params.dias && params.pascua ? 'con_dias_pascua'
          : params.dias ? 'con_dias'
            : params.pascua ? 'con_dias_pascua' : 'sin_regresores';
        // La Semana Santa sola no se precalculó: si se pide sin los días, se
        // avisa en vez de mostrar un ajuste que no existe.
        const soloPascua = params.pascua && !params.dias;
        const m = cal.modelos[clave];

        const datasets = [{
          label: 'log(AirPassengers)',
          data: AP.log, borderColor: COLORES_GRAFICO.gris,
          borderWidth: 1.2, pointRadius: 0, yAxisID: 'y'
        }];
        if (params.dias) datasets.push({
          label: 'Días del mes', data: cal.dias_mes,
          borderColor: COLORES_GRAFICO.primario, borderWidth: 1.6,
          pointRadius: 0, yAxisID: 'y2'
        });
        if (params.pascua) datasets.push({
          label: 'Mes con Domingo de Pascua', data: esPascua.map(v => v ? 31 : null),
          borderColor: COLORES_GRAFICO.secundario, backgroundColor: COLORES_GRAFICO.secundario,
          borderWidth: 0, pointRadius: 3, showLine: false, yAxisID: 'y2'
        });

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, cal.fechas, datasets, {
          plugins: { legend: { display: true } },
          scales: {
            x: { ticks: { font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 12, maxRotation: 0 }, grid: { display: false } },
            y: { position: 'left', ticks: { font: { family: 'Fira Code', size: 11 } }, grid: { color: 'rgba(148,163,184,0.2)' } },
            y2: { position: 'right', min: 26, max: 33, ticks: { font: { family: 'Fira Code', size: 11 } }, grid: { display: false } }
          }
        });

        const campos = [
          { etiqueta: 'modelo', valor: soloPascua ? 'Semana Santa sola: no precalculada' : m.nombre },
          { etiqueta: 'AICc', valor: fmt(m.aicc, 4) },
          { etiqueta: 'mejora sobre el airline', valor: fmt(baseAicc - m.aicc, 4) + ' puntos' },
          { etiqueta: 'BIC', valor: fmt(m.bic, 4) }
        ];
        m.coeficientes.forEach(c => {
          if (c.nombre === 'log_dias' || c.nombre === 'pascua') {
            campos.push({
              etiqueta: c.nombre === 'log_dias' ? 'β̂ log(días)' : 'β̂ Semana Santa',
              valor: `${fmt(c.valor, 4)} (e.e. ${fmt(c.ee, 4)}, t = ${fmt(c.t, 2)})`
            });
          }
        });
        campos.push({ etiqueta: 'meses con Pascua en marzo', valor: `${cal.meses_pascua_marzo} de 12` });
        actualizarLectura(lectura, campos);
      }

      crearInterruptores(controles, [
        { clave: 'dias', etiqueta: 'log(días del mes)' },
        { clave: 'pascua', etiqueta: 'Semana Santa' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 10 · ¿Cuántos armónicos hacen falta?
    // ================================================================
    SIMULADORES['armonicos-K'] = function (raiz) {
      const params = { K: 3 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      const fou = AP.fourier;
      let grafico = null;

      function pintar() {
        const K = Math.round(params.K);
        const curva = fou.curvas[K - 1];
        const r = fou.resultados[K - 1];
        // Solo los dos primeros ciclos: la curva es periódica y así se ve la forma.
        const n = 24;
        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, AP.fechas.slice(0, n), [
          { label: `K = ${K} (${r.n_terminos} términos)`, data: curva.slice(0, n),
            borderColor: COLORES_GRAFICO.secundario, borderWidth: 2, pointRadius: 0 },
          { label: 'K = 6 (saturado)', data: fou.curvas[5].slice(0, n),
            borderColor: COLORES_GRAFICO.gris, borderWidth: 1.2, pointRadius: 0, borderDash: [4, 3] }
        ], { plugins: { legend: { display: true } } });

        actualizarLectura(lectura, [
          { etiqueta: 'K', valor: K },
          { etiqueta: 'términos de Fourier', valor: r.n_terminos },
          { etiqueta: 'parámetros totales', valor: r.n_par_total },
          { etiqueta: 'errores', valor: r.modelo_errores },
          { etiqueta: 'AICc (solo comparable dentro de esta familia)', valor: fmt(r.aicc, 4) },
          { etiqueta: 'n efectivo', valor: r.nobs + '  (el airline usa ' + fou.comparabilidad.nobs_airline + ')' },
          { etiqueta: 'Ljung–Box(24) p', valor: fmt(r.lb24_p, 4) + (r.lb24_p < 0.05 ? '  ⚠ rechaza' : '') },
          { etiqueta: 'ρ̂₁₂ residual', valor: fmt(r.acf12, 4) }
        ]);
      }

      crearControles(controles, [{
        clave: 'K', etiqueta: 'Armónicos K', min: 1, max: 6, paso: 1, decimales: 0
      }], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 11 · La comparativa sobre una sola partición
    // ================================================================
    SIMULADORES['comparativa-particion'] = function (raiz) {
      const comp = AP.comparativa;
      const claves = comp.orden_rmse;
      const params = { metrica: 'rmse' };
      claves.forEach((k, i) => { params['m_' + k] = i < 3 || k === 'sarima'; });
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      const COLORES = [COLORES_GRAFICO.secundario, COLORES_GRAFICO.terciario, '#7c3aed',
                       '#be123c', '#0f766e', '#a16207', '#9333ea', '#475569'];
      let grafico = null;

      function pintar() {
        const datasets = [{
          label: 'Observado', data: comp.observado,
          borderColor: COLORES_GRAFICO.primario, borderWidth: 2.4, pointRadius: 0
        }];
        claves.forEach((k, i) => {
          if (!params['m_' + k]) return;
          datasets.push({
            label: comp.modelos[k].nombre.slice(0, 34),
            data: comp.modelos[k].pronostico,
            borderColor: COLORES[i % COLORES.length],
            borderWidth: 1.5, pointRadius: 0, borderDash: [5, 3]
          });
        });

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, comp.fechas_prueba, datasets,
          { plugins: { legend: { display: true } } });

        const met = params.metrica;
        const orden = claves.slice().sort((a, b) => comp.modelos[a][met] - comp.modelos[b][met]);
        const campos = [
          { etiqueta: 'entrena hasta', valor: comp.corte + ` (n = ${comp.n_entrenamiento})` },
          { etiqueta: 'prueba', valor: comp.n_prueba + ' meses' }
        ];
        orden.forEach((k, i) => campos.push({
          etiqueta: `${i + 1}. ${comp.modelos[k].nombre.slice(0, 38)}`,
          valor: fmt(comp.modelos[k][met], 3) + (k === 'sarima' ? '  ← el SARIMA' : '')
        }));
        actualizarLectura(lectura, campos);
      }

      crearSelector(controles, {
        clave: 'metrica', etiqueta: 'Métrica del ranking',
        opciones: [
          { valor: 'rmse', texto: 'RMSE' },
          { valor: 'mae', texto: 'MAE' },
          { valor: 'mape', texto: 'MAPE (%)' }
        ]
      }, params, pintar);
      crearInterruptores(controles,
        claves.map(k => ({ clave: 'm_' + k, etiqueta: comp.modelos[k].nombre.slice(0, 26) })),
        params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Autoevaluación del capítulo
    // ================================================================
    // Tabla ordenable de la comparativa sobre UNA partición. El pie recuerda que
    // este ranking se desmiente en el capítulo 6 con 61 orígenes.
    TABLAS_RANKING['comparativa'] = function () {
      const claves = AP.comparativa.orden_rmse;
      return {
        descripcion: 'Los seis métodos sobre los últimos ' + AP.comparativa.n_prueba +
          ' meses, una sola partición. Pulsa las cabeceras: las tres métricas coinciden ' +
          'en el orden, lo que da una falsa sensación de solidez.',
        columnas: [
          { clave: 'modelo', titulo: 'Método', tipo: 'texto' },
          { clave: 'rmse', titulo: 'RMSE', decimales: 2, mejor: 'menor' },
          { clave: 'mae', titulo: 'MAE', decimales: 2, mejor: 'menor' },
          { clave: 'mape', titulo: 'MAPE', decimales: 2, sufijo: ' %', mejor: 'menor' }
        ],
        filas: claves.map(k => ({
          modelo: AP.comparativa.modelos[k].nombre,
          rmse: AP.comparativa.modelos[k].rmse,
          mae: AP.comparativa.modelos[k].mae,
          mape: AP.comparativa.modelos[k].mape
        })),
        inicial: 'rmse',
        pie: 'Las tres columnas dan el mismo orden y aun así el orden es engañoso: ' +
          'sobre 61 orígenes en vez de uno, el SARIMA pasa de cuarto a primero. ' +
          'El Capítulo 6 construye esa evaluación.'
      };
    };

    AUTOEVALUACIONES['cap5'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'La TRM mensual en niveles tiene $\\hat\\rho_{12} = 0.637$, muy por encima de su banda de $0.167$. ¿Qué se concluye?',
        pista: 'Fíjate en qué vale $\\hat\\rho_1$ en esa misma serie, y en qué le pasa a la ACF de cualquier serie con tendencia.',
        opciones: [
          {
            texto: 'Nada todavía: en niveles la tendencia infla <em>todos</em> los $\\hat\\rho_k$, así que el diagnóstico hay que hacerlo sobre la serie ya diferenciada.',
            correcta: true,
            retro: 'Exacto. En esa misma serie $\\hat\\rho_1 = 0.964$ y $\\hat\\rho_{36} = 0.225$: es el decaimiento lento típico de una tendencia, no un pico estacional. Sobre $\\nabla$TRM los tres múltiplos de $12$ valen $-0.0025$, $-0.067$ y $0.071$, todos dentro de la banda.'
          },
          {
            texto: 'Que la TRM tiene estacionalidad anual, porque $0.637$ supera claramente la banda.',
            correcta: false,
            retro: 'Es la conclusión que el módulo está diseñado para evitar. Una serie con tendencia da autocorrelaciones grandes en <em>todos</em> los rezagos, incluidos los múltiplos de $12$. Cuatro evidencias independientes (Módulo 8) muestran que esta serie no tiene estacionalidad.'
          },
          {
            texto: 'Que hace falta una diferencia estacional, porque $\\hat\\rho_{12}$ está fuera de banda.',
            correcta: false,
            retro: 'Sería una lectura razonable si la serie estuviera sin tendencia, pero no lo está. De hecho <code>nsdiffs()</code> devuelve $0$ con las dos pruebas disponibles: no hay ninguna raíz unitaria estacional que quitar.'
          },
          {
            texto: 'Que la banda está mal calculada, porque con $n = 138$ debería ser mayor.',
            correcta: false,
            retro: 'La banda es $1.96/\\sqrt{n} = 1.96/\\sqrt{138} = 0.1668$, correcta. El problema no está en la banda sino en aplicarla a una serie no estacionaria: bajo tendencia, la distribución de referencia de $\\hat\\rho_k$ ya no es la que justifica esa banda.'
          }
        ]
      },
      {
        tipo: 'multiple',
        modulo: 2,
        pregunta: 'En un SARIMA($1,0,0$)($1,0,0$)$_{12}$, ¿cuáles de estas afirmaciones son ciertas?',
        pista: 'Expande $(1-\\phi B)(1-\\Phi B^{12})$ y cuenta: cuántos coeficientes distintos de cero salen, y cuántos de ellos se estiman.',
        opciones: [
          {
            texto: 'El modelo toca el rezago $13$ aunque nadie haya puesto un parámetro ahí.',
            correcta: true,
            retro: 'Sí: el término cruzado $\\phi\\Phi B^{13}$ aparece al multiplicar los polinomios.'
          },
          {
            texto: 'Tiene $2$ parámetros libres.',
            correcta: true,
            retro: 'Correcto: $\\phi$ y $\\Phi$. El coeficiente del rezago $13$ es su producto, no un tercer parámetro.'
          },
          {
            texto: 'Su ACF teórica es cero en los rezagos $2$ a $11$.',
            correcta: false,
            retro: 'No: con $\\phi = 0.6$ y $\\Phi = 0.7$, $\\rho_2 = \\rho_1^2 \\approx 0.36$ y así sucesivamente. La parte AR regular llena los rezagos bajos con una geométrica. Los rezagos intermedios sí son cero cuando <strong>solo</strong> hay parte estacional ($\\phi = 0$).'
          },
          {
            texto: 'Escrito como AR no estacional, es un AR($13$).',
            correcta: true,
            retro: 'Correcto: el polinomio completo tiene grado $13$, con solo tres coeficientes no nulos ($1$, $12$ y $13$).'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 2,
        unidad: '',
        pregunta: 'Un SARIMA($0,1,1$)($0,1,1$)$_{12}$ se ajusta a una serie mensual de $n = 96$ observaciones. ¿Cuántas observaciones quedan tras aplicar las dos diferencias?',
        pista: 'La diferencia regular cuesta $d = 1$ observación; la estacional cuesta $D \\times m$, no $D$.',
        respuesta: 83,
        tolerancia: 0.5,
        retroAcierto: 'Correcto: $96 - d - D\\,m = 96 - 1 - 12 = 83$. Ese es el $n$ efectivo con el que se evalúa la verosimilitud, y por eso el AICc de un modelo con $D=1$ no se puede comparar con el de uno con $D=0$, que tendría $95$.',
        retroFallo: 'La diferencia estacional cuesta $m = 12$ observaciones, no una: $96 - 1 - 12 = 83$. Si respondiste $94$, restaste $d + D = 2$; si respondiste $84$, olvidaste la diferencia regular. Esa cuenta es justamente la que hace incomparables los AICc entre distintos $D$.'
      },
      {
        tipo: 'opcion',
        modulo: 3,
        pregunta: 'Sobre <code>USAccDeaths</code>, <code>ndiffs()</code> devuelve $0$ en la serie cruda y $1$ tras aplicar $\\nabla_{12}$. ¿Qué significa?',
        pista: 'Los operadores $\\nabla$ y $\\nabla_{12}$ conmutan. Piensa entonces qué es lo que cambia entre las dos llamadas.',
        opciones: [
          {
            texto: 'Que la estacionalidad domina la varianza y tapa la tendencia, así que $D$ se decide antes que $d$.',
            correcta: true,
            retro: 'Eso es. Los <em>operadores</em> conmutan —la serie $\\nabla\\nabla_{12}y$ es idéntica en cualquier orden, diferencia máxima medida $0$—, pero las <em>pruebas</em> no: aplicadas a la serie cruda, la varianza estacional impide ver la raíz unitaria regular. En Python pasa igual: KPSS sobre $\\nabla_{12}y$ da $0.8672$ y rechaza.'
          },
          {
            texto: 'Que <code>ndiffs()</code> tiene un error, porque el resultado debería ser el mismo.',
            correcta: false,
            retro: 'No hay error: son dos series de entrada distintas. La primera llamada recibe $y_t$ y la segunda $\\nabla_{12}y_t$. Que dos entradas distintas den salidas distintas es lo esperable; lo interesante es <em>por qué</em>.'
          },
          {
            texto: 'Que la serie está sobrediferenciada tras aplicar $\\nabla_{12}$.',
            correcta: false,
            retro: 'Al revés: tras $\\nabla_{12}$ todavía falta una diferencia, y por eso <code>ndiffs()</code> devuelve $1$. La firma de la sobrediferenciación sería un $\\hat\\theta$ pegado a $-1$ con la raíz MA sobre el círculo unitario, y aquí el modelo final da $\\hat\\theta = -0.4303$.'
          },
          {
            texto: 'Que hay que aplicar $\\nabla$ dos veces, una por cada resultado.',
            correcta: false,
            retro: 'No: el $1$ de la segunda llamada <em>es</em> la respuesta, no un añadido al $0$ de la primera. El modelo final es $(0,1,1)(0,1,1)_{12}$, con $d = 1$. Con $d = 2$ aparecería la firma de la sobrediferenciación.'
          }
        ]
      },
      {
        tipo: 'grafico',
        modulo: 4,
        pregunta: 'La ACF teórica del gráfico corresponde a un proceso estacional puro con $m = 12$. ¿Qué modelo es?',
        pista: 'Mira si los picos en $12, 24, 36$ decaen o se cortan de golpe, y compara con la tabla de identificación del Módulo 4.',
        dibujar: function (canvas) {
          const ar = new Array(12).fill(0); ar[11] = 0.7;
          const psi = pesosPsi(ar, [], 1500);
          const acf = acfDesdePsi(psi, 36);
          return crearGraficoBarras(canvas, etiquetasRezago(36), acf, {
            etiqueta: 'ACF teórica', tituloX: 'Rezago'
          });
        },
        opciones: [
          {
            texto: 'Un SAR($1$)$_{12}$ con $\\Phi > 0$: los picos decaen geométricamente ($0.70$, $0.49$, $0.34$).',
            correcta: true,
            retro: 'Correcto. Los tres picos son $\\Phi$, $\\Phi^2$ y $\\Phi^3$ con $\\Phi = 0.7$, y todos los rezagos intermedios valen exactamente cero porque no hay parte regular. La PACF de este proceso se cortaría tras el rezago $12$.'
          },
          {
            texto: 'Un SMA($1$)$_{12}$: hay un pico en el rezago $12$ y estacionalidad clara.',
            correcta: false,
            retro: 'Un SMA($1$)$_{12}$ se <strong>corta</strong>: tendría un pico en el $12$ y exactamente $0$ en el $24$ y el $36$. Aquí los tres picos están presentes y decaen, que es la firma del SAR.'
          },
          {
            texto: 'Un modelo <em>airline</em>, por los picos en los múltiplos de $12$.',
            correcta: false,
            retro: 'El <em>airline</em> tiene además parte regular, así que su ACF sería distinta de cero en el rezago $1$ y en los satélites $11$ y $13$. Aquí esos rezagos valen cero, así que no hay componente regular.'
          },
          {
            texto: 'Un AR($1$)$\\times$SAR($1$): se ven los satélites alrededor de los picos.',
            correcta: false,
            retro: 'Justamente lo contrario: <strong>no</strong> hay satélites. Los rezagos $11$ y $13$ valen cero. Con un AR($1$) regular multiplicando, $\\rho_{11}$ y $\\rho_{13}$ serían del orden de $\\rho_1\\rho_{12}$ y se verían con claridad.'
          }
        ]
      },
      {
        tipo: 'opcion',
        modulo: 6,
        pregunta: 'Ajustas dos modelos a la misma serie mensual: una regresión armónica ($D = 0$, AICc $= -521.2$) y un SARIMA <em>airline</em> ($D = 1$, AICc $= -483.2$). ¿Cuál eliges?',
        pista: 'Antes de comparar dos AICc, pregúntate sobre cuántas observaciones se ha evaluado la verosimilitud de cada uno.',
        opciones: [
          {
            texto: 'Ninguno con esa información: los AICc no son comparables porque se calculan sobre $143$ y $131$ observaciones.',
            correcta: true,
            retro: 'Correcto, y es la lección central del Módulo 10. Es la misma trampa que el Capítulo 4 documentó con $d$, agravada porque cada $D$ cuesta $m = 12$ observaciones en vez de una. Entre familias solo se puede comparar fuera de muestra.'
          },
          {
            texto: 'La armónica, que gana por $38$ puntos de AICc, que es una diferencia enorme.',
            correcta: false,
            retro: 'La diferencia es enorme precisamente porque los dos números no viven en la misma escala: doce observaciones menos cambian la log-verosimilitud mucho más que cualquier parámetro. Comparar esos AICc es el error que el módulo señala.'
          },
          {
            texto: 'El <em>airline</em>, porque tiene $2$ parámetros frente a $16$ y la parsimonia desempata.',
            correcta: false,
            retro: 'La conclusión final del capítulo es en efecto favorable al <em>airline</em>, pero por otra razón: gana fuera de muestra sobre $61$ orígenes. Invocar la parsimonia aquí es aceptar la comparación de AICc y luego corregirla a mano; lo correcto es rechazarla.'
          },
          {
            texto: 'La armónica, porque su Ljung–Box no rechaza y eso es lo que decide.',
            correcta: false,
            retro: 'El diagnóstico sí es comparable entre familias —no depende del $n$ efectivo de la verosimilitud—, así que el razonamiento va por buen camino. Pero los dos pasan Ljung–Box ($0.1341$ y $0.2330$), así que no desempata; y el <em>airline</em> lo pasa con más holgura.'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 9,
        unidad: '',
        pregunta: 'El coeficiente de $\\log(\\text{días del mes})$ vale $\\hat\\beta = 1.0840$ con error estándar $0.4462$. ¿Cuál es el estadístico $t$ para contrastar $H_0: \\beta = 1$? Da cuatro decimales.',
        pista: 'El estadístico no es $\\hat\\beta / \\text{e.e.}$, que contrastaría $\\beta = 0$. Aquí el valor bajo la hipótesis nula es $1$.',
        respuesta: 0.1883,
        tolerancia: 0.005,
        retroAcierto: '$t = (1.0840 - 1)/0.4462 = 0.1883$: no se rechaza. Los pasajeros son compatibles con ser <strong>exactamente proporcionales</strong> a los días del mes, que es lo que predice la aritmética del calendario. Un coeficiente significativo y además igual a su valor teórico es una confirmación fuerte.',
        retroFallo: 'El contraste de $\\beta = 1$ usa $t = (\\hat\\beta - 1)/\\text{e.e.} = (1.0840-1)/0.4462 = 0.1883$. Si respondiste $2.4291$, contrastaste $\\beta = 0$ —que también es informativo: el regresor <em>sí</em> aporta—, pero la pregunta interesante aquí es si el efecto es exactamente proporcional.'
      },
      {
        tipo: 'opcion',
        modulo: 11,
        pregunta: 'Sobre los últimos $24$ meses el SARIMA queda cuarto (RMSE $43.18$) y la regresión armónica primera ($19.51$). Sobre $61$ orígenes el SARIMA es primero ($16.81$) y la armónica cuarta ($22.39$). ¿Qué explica esto?',
        pista: 'Pregúntate cuántos números independientes hay realmente detrás de cada una de las dos comparaciones.',
        opciones: [
          {
            texto: 'Una sola partición mide el comportamiento en <em>un</em> tramo concreto; con $24$ puntos, qué tramo toque pesa más que la diferencia entre métodos.',
            correcta: true,
            retro: 'Eso es. 1959–1960 tuvieron un crecimiento especialmente regular y ahí una estacionalidad determinista extrapola mejor. Promediando sobre $61$ orígenes el efecto del tramo se diluye y el SARIMA le gana a cada rival en más del $85\\,\\%$ de ellos. Construir esa evaluación es el contenido del Capítulo 6.'
          },
          {
            texto: 'Que el RMSE no sirve para comparar métodos y hay que usar MAPE.',
            correcta: false,
            retro: 'Las tres métricas de la tabla —RMSE, MAE y MAPE— dan el mismo orden en la partición única. El problema no es la métrica sino el número de particiones sobre las que se calcula.'
          },
          {
            texto: 'Que el SARIMA está mal especificado y por eso falla en la partición corta.',
            correcta: false,
            retro: 'El SARIMA pasa todos los diagnósticos (Ljung–Box $0.2330$, Shapiro $0.1674$, raíces invertibles) y es el mínimo de AICc y de BIC dentro de su familia. Un modelo bien especificado también puede quedar mal en un tramo concreto: eso es varianza, no sesgo.'
          },
          {
            texto: 'Que los $61$ orígenes se solapan entre sí, así que ese resultado no vale.',
            correcta: false,
            retro: 'Es cierto que las ventanas se solapan y que por eso los $61$ errores no son independientes —conviene saberlo al poner barras de error—. Pero eso afecta a la <em>precisión</em> de la estimación, no la invalida: una diferencia de $16.81$ frente a $22.39$ con victoria en el $90\\,\\%$ de los orígenes no se explica por el solape.'
          }
        ]
      }
    ];
