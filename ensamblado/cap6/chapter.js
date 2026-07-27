    // ================================================================
    // Datos y ayudantes del capítulo, tomados del precálculo en R
    // ================================================================
    const EV = DATOS_CAP6;
    const RVE = EV.residual_vs_error;
    const BENCH = EV.benchmarks.airpassengers;
    const CONTRA6 = EV.contraejemplos;
    const FUGA = EV.fuga;
    const OM = EV.origen_movil;
    const ANIM = OM.animacion;
    const BT = EV.backtest;
    const INTER = EV.intervalos;
    const CASOS = EV.casos;
    const H6 = EV.h;

    const PALETA6 = [COLORES_GRAFICO.primario, COLORES_GRAFICO.secundario,
                     COLORES_GRAFICO.terciario, '#7c3aed', '#be123c',
                     '#0f766e', '#a16207', '#475569'];

    // Etiquetas h=1..h para los ejes de horizonte
    const HORIZONTES = Array.from({ length: H6 }, (_, i) => 'h=' + (i + 1));

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

    function porId(lista, id) { return lista.find(z => z.id === id); }

    // Ranking de un conjunto de filas por un campo, con el criterio de la
    // columna: 'menor', 'mayor' o 'cerca' de un objetivo.
    function ordenarPor(filas, campo, modo, objetivo) {
      const dist = f => {
        const v = Number(f[campo]);
        if (!Number.isFinite(v)) return Number.POSITIVE_INFINITY;
        if (modo === 'mayor') return -v;
        if (modo === 'cerca') return Math.abs(v - objetivo);
        return v;
      };
      return filas.slice().sort((a, b) => dist(a) - dist(b));
    }

    // ================================================================
    // Módulo 1 — Residual frente a error de pronóstico
    // ================================================================
    SIMULADORES['residual-vs-error'] = function (raiz) {
      const cortes = RVE.cortes;
      const params = { i: Math.floor(cortes.length / 2) };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const c = cortes[params.i];
        const origen = ANIM.origenes.find(o => o.T === c.T);
        const n = ANIM.serie.length;

        const entrenamiento = ANIM.serie.map((v, k) => (k <= c.T - 1 ? v : null));
        const futuro = ANIM.serie.map((v, k) => (k >= c.T - 1 ? v : null));
        const pron = Array(n).fill(null);
        if (origen) {
          // el pronóstico arranca en el propio origen para que la línea enlace
          pron[c.T - 1] = ANIM.serie[c.T - 1];
          origen.sarima.forEach((v, j) => { if (c.T + j < n) pron[c.T + j] = v; });
        }

        const datasets = [
          {
            label: 'Entrenamiento (el modelo vio estos datos)', data: entrenamiento,
            borderColor: COLORES_GRAFICO.primario, borderWidth: 2.2, pointRadius: 0
          },
          {
            label: 'Futuro (no participó en la estimación)', data: futuro,
            borderColor: COLORES_GRAFICO.gris, borderWidth: 2.2, pointRadius: 0
          },
          {
            label: 'Pronóstico a 12 meses', data: pron,
            borderColor: COLORES_GRAFICO.secundario, borderWidth: 2,
            borderDash: [5, 3], pointRadius: 0
          }
        ];

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, ANIM.fechas, datasets, {
          plugins: { legend: { display: true } },
          scales: { x: { ticks: { maxTicksLimit: 12 } } }
        });

        actualizarLectura(lectura, [
          { etiqueta: 'corte', valor: c.fecha + ` (T = ${c.T})` },
          { etiqueta: 'RMSE dentro de muestra (residuales)', valor: fmt(c.rmse_dentro, 2) },
          { etiqueta: 'RMSE fuera de muestra (pronóstico)', valor: fmt(c.rmse_fuera, 2) },
          {
            etiqueta: 'razón fuera / dentro',
            valor: fmt(c.razon, 2) + (c.razon < 1 ? '  ← aquí el pronóstico salió mejor' : '')
          }
        ]);
      }

      crearControles(controles, [{
        clave: 'i', etiqueta: 'Corte de entrenamiento  ', min: 0,
        max: cortes.length - 1, paso: 1, decimales: 0
      }], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 2 — Los cuatro métodos de referencia
    // ================================================================
    SIMULADORES['benchmarks'] = function (raiz) {
      const metodos = BENCH.metodos;
      const params = { metrica: 'rmse', banda: false };
      metodos.forEach(m => { params['m_' + m.metodo] = true; });
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const NOMBRES = { rmse: 'RMSE', mae: 'MAE', mape: 'MAPE (%)', mase: 'MASE' };

      function pintar() {
        const datasets = [{
          label: 'Observado', data: BENCH.observado,
          borderColor: COLORES_GRAFICO.primario, borderWidth: 2.6, pointRadius: 0
        }];
        metodos.forEach((m, i) => {
          if (!params['m_' + m.metodo]) return;
          datasets.push({
            label: m.metodo, data: m.pronostico,
            borderColor: PALETA6[(i + 1) % PALETA6.length],
            borderWidth: 1.8, pointRadius: 0, borderDash: [5, 3]
          });
          if (params.banda) {
            datasets.push({
              label: '', data: m.li95, borderColor: PALETA6[(i + 1) % PALETA6.length],
              borderWidth: 0.8, pointRadius: 0, borderDash: [2, 3]
            });
            datasets.push({
              label: '', data: m.ls95, borderColor: PALETA6[(i + 1) % PALETA6.length],
              borderWidth: 0.8, pointRadius: 0, borderDash: [2, 3]
            });
          }
        });

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, BENCH.fechas, datasets, {
          plugins: { legend: { display: true, labels: { filter: it => it.text !== '' } } }
        });

        const orden = ordenarPor(metodos, params.metrica, 'menor');
        const campos = [
          { etiqueta: 'entrena hasta', valor: BENCH.corte + ` (n = ${BENCH.n_entrena})` },
          { etiqueta: 'prueba', valor: BENCH.n_prueba + ' meses' }
        ];
        orden.forEach((m, i) => campos.push({
          etiqueta: `${i + 1}. ${m.metodo}`,
          valor: fmt(m[params.metrica], params.metrica === 'mase' ? 3 : 2)
        }));
        actualizarLectura(lectura, campos);
      }

      crearSelector(controles, {
        clave: 'metrica', etiqueta: 'Métrica del ranking',
        opciones: Object.keys(NOMBRES).map(k => ({ valor: k, texto: NOMBRES[k] }))
      }, params, pintar);
      crearInterruptores(controles,
        metodos.map(m => ({ clave: 'm_' + m.metodo, etiqueta: m.metodo }))
          .concat([{ clave: 'banda', etiqueta: 'Bandas del 95 %' }]),
        params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 3 — RMSE y MAE pueden dar ganadores distintos
    // ================================================================
    SIMULADORES['rmse-vs-mae'] = function (raiz) {
      const todos = CONTRA6.rmse_vs_mae.por_origen;
      const conflictos = todos.filter(o => o.conflicto);
      const params = { i: 0, soloConflictos: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;
      let deslizador = null;

      function lista() { return params.soloConflictos ? conflictos : todos; }

      function pintar() {
        const L = lista();
        const o = L[Math.min(Math.round(params.i), L.length - 1)];

        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, HORIZONTES, o.snaive, {
          etiqueta: 'Naive estacional', color: COLORES_GRAFICO.primario,
          barrasExtra: [{ etiqueta: 'Deriva', valores: o.deriva, color: COLORES_GRAFICO.secundario }],
          lineas: [{ valor: 0, etiqueta: '' }],
          tituloX: 'Horizonte de pronóstico', min: -140, max: 140
        });

        const ganaR = o.snaive_rmse < o.deriva_rmse ? 'Naive estacional' : 'Deriva';
        const ganaM = o.snaive_mae < o.deriva_mae ? 'Naive estacional' : 'Deriva';
        actualizarLectura(lectura, [
          { etiqueta: 'origen', valor: `${o.fecha} (T = ${o.T})` },
          { etiqueta: 'RMSE', valor: `${fmt(o.snaive_rmse, 2)} vs ${fmt(o.deriva_rmse, 2)} → ${ganaR}` },
          { etiqueta: 'MAE', valor: `${fmt(o.snaive_mae, 2)} vs ${fmt(o.deriva_mae, 2)} → ${ganaM}` },
          {
            etiqueta: 'veredicto',
            valor: ganaR === ganaM ? 'las dos métricas coinciden'
              : '⚠ las dos métricas se contradicen'
          },
          { etiqueta: 'orígenes en conflicto', valor: `${conflictos.length} de ${todos.length}` }
        ]);
      }

      deslizador = crearControles(controles, [{
        clave: 'i', etiqueta: 'Origen  ', min: 0, max: conflictos.length - 1,
        paso: 1, decimales: 0
      }], params, pintar);

      crearInterruptores(controles, [
        { clave: 'soloConflictos', etiqueta: 'Solo los orígenes en conflicto' }
      ], params, () => {
        const L = lista();
        // el rango del deslizador cambia con el interruptor
        deslizador.i.max = L.length - 1;
        if (params.i > L.length - 1) { params.i = L.length - 1; deslizador.i.value = params.i; }
        pintar();
      });

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 4 — El MAPE empuja el pronóstico hacia abajo
    // ================================================================
    SIMULADORES['sesgo-mape'] = function (raiz) {
      const S = CONTRA6.sesgo_mape;
      const params = { f: 150 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      // Cada curva dividida por su propio mínimo: así las tres caben en el
      // mismo eje y lo que se compara es DÓNDE está el mínimo, no su altura.
      const norm = arr => { const m = Math.min.apply(null, arr); return arr.map(v => v / m); };
      const curvas = { mape: norm(S.mape), mae: norm(S.mae), rmse: norm(S.rmse) };

      function pintar() {
        const j = S.f.reduce((mejor, v, k) =>
          Math.abs(v - params.f) < Math.abs(S.f[mejor] - params.f) ? k : mejor, 0);
        const marca = S.f.map((v, k) => (k === j ? 2.2 : null));

        const datasets = [
          { label: 'MAPE esperado', data: curvas.mape, borderColor: COLORES_GRAFICO.secundario, borderWidth: 2.4, pointRadius: 0 },
          { label: 'MAE esperado', data: curvas.mae, borderColor: COLORES_GRAFICO.terciario, borderWidth: 2, pointRadius: 0 },
          { label: 'RMSE esperado', data: curvas.rmse, borderColor: COLORES_GRAFICO.primario, borderWidth: 2, pointRadius: 0 },
          { label: '', data: marca, borderColor: 'rgba(1,40,32,0.35)', borderWidth: 1.5, pointRadius: 0, spanGaps: false }
        ];

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, S.f.map(String), datasets, {
          plugins: { legend: { display: true, labels: { filter: it => it.text !== '' } } },
          scales: {
            x: { title: { display: true, text: 'Pronóstico f', font: { family: 'Montserrat', size: 11 } },
                 ticks: { maxTicksLimit: 10 } },
            y: { title: { display: true, text: 'métrica / su mínimo', font: { family: 'Montserrat', size: 11 } } }
          }
        });

        actualizarLectura(lectura, [
          { etiqueta: 'pronóstico f', valor: fmt(S.f[j], 0) },
          { etiqueta: 'MAPE esperado', valor: fmt(S.mape[j], 2) + ' %' },
          { etiqueta: 'MAE esperado', valor: fmt(S.mae[j], 2) },
          { etiqueta: 'RMSE esperado', valor: fmt(S.rmse[j], 2) },
          { etiqueta: 'mínimo del MAPE en', valor: fmt(S.f_optimo_mape, 0) + '  (el valor bajo)' },
          { etiqueta: 'mínimo del RMSE en', valor: fmt(S.f_optimo_rmse, 0) + '  (la media)' }
        ]);
      }

      crearControles(controles, [{
        clave: 'f', etiqueta: 'Pronóstico f  ', min: 80, max: 220, paso: 2, decimales: 0
      }], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 4 — El MAPE sobre una serie que cruza el cero
    // ================================================================
    SIMULADORES['mape-cero'] = function (raiz) {
      const MC = CONTRA6.mape_cero;
      const params = { tope: 400 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const etiquetas = MC.ape.map((_, i) => 'mes ' + (i + 1));

      function pintar() {
        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetas, MC.ape, {
          etiqueta: 'Error porcentual absoluto (%)', color: COLORES_GRAFICO.secundario,
          lineas: [{ valor: MC.mape_mediano, etiqueta: 'Mediana de los |pᵢ|' }],
          tituloX: 'Mes del conjunto de prueba', min: 0, max: params.tope
        });

        const cortadas = MC.ape.filter(v => v > params.tope).length;
        actualizarLectura(lectura, [
          { etiqueta: 'tope de la escala', valor: fmt(params.tope, 0) + ' %' },
          { etiqueta: 'barras que se salen del gráfico', valor: String(cortadas) },
          { etiqueta: 'MAPE', valor: fmt(MC.mape, 2) + ' %' },
          { etiqueta: 'mediana de los |pᵢ|', valor: fmt(MC.mape_mediano, 2) + ' %' },
          { etiqueta: 'mayor |pᵢ|', valor: fmt(MC.ape_maximo, 2) + ' %' },
          { etiqueta: 'el mes culpable observó', valor: fmt(MC.observado_del_maximo, 4) + ' %' },
          { etiqueta: 'MASE (misma predicción)', valor: fmt(MC.mase, 4) }
        ]);
      }

      crearControles(controles, [{
        clave: 'tope', etiqueta: 'Tope de la escala vertical (%)  ',
        min: 100, max: 16200, paso: 100, decimales: 0
      }], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 5 — Qué métricas sobreviven a un cambio de unidades
    // ================================================================
    SIMULADORES['cambio-escala'] = function (raiz) {
      const base = CONTRA6.cambio_escala.original;
      const params = { exp: 3 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      // Sólo RMSE y MAE llevan unidades de la serie; el resto son razones y
      // el factor se cancela. No hace falta recalcular: se sabe exactamente.
      const CLAVES = ['rmse', 'mae', 'mape', 'smape', 'mase', 'rmsse'];
      const ETIQ = { rmse: 'RMSE', mae: 'MAE', mape: 'MAPE', smape: 'sMAPE', mase: 'MASE', rmsse: 'RMSSE' };
      const CON_UNIDADES = { rmse: true, mae: true, mape: false, smape: false, mase: false, rmsse: false };

      function pintar() {
        const factor = Math.pow(10, params.exp);
        const razones = CLAVES.map(k => (CON_UNIDADES[k] ? factor : 1));

        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, CLAVES.map(k => ETIQ[k]),
          razones.map(r => Math.log10(r)), {
            etiqueta: 'log₁₀(métrica con el factor / métrica original)',
            color: COLORES_GRAFICO.primario,
            lineas: [{ valor: 0, etiqueta: 'Sin cambio (razón = 1)' }],
            min: -3.4, max: 3.4
          });

        const campos = [{ etiqueta: 'factor de escala', valor: '×' + fmt(factor, factor < 1 ? 3 : 0) }];
        CLAVES.forEach((k, i) => campos.push({
          etiqueta: ETIQ[k],
          valor: fmt(base[k] * razones[i], 4) + (CON_UNIDADES[k] ? '  ← cambia' : '  ← intacta')
        }));
        actualizarLectura(lectura, campos);
      }

      crearControles(controles, [{
        clave: 'exp', etiqueta: 'Factor de escala, 10^  ', min: -3, max: 3, paso: 1, decimales: 0
      }], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 6 — Cuándo miente el k-fold aleatorio
    // ================================================================
    SIMULADORES['fuga-cv'] = function (raiz) {
      const M = FUGA.cv.montajes;
      const params = { log: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const t = v => (params.log ? Math.log10(v) : v);
        const etiquetas = M.map(m => m.id);

        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetas, M.map(m => t(m.rmse_kfold)), {
          etiqueta: 'k-fold aleatorio', color: COLORES_GRAFICO.secundario,
          barrasExtra: [
            { etiqueta: 'Origen móvil', valores: M.map(m => t(m.rmse_origen_movil)), color: COLORES_GRAFICO.terciario },
            { etiqueta: 'Bloque final (el error real)', valores: M.map(m => t(m.rmse_bloque_final)), color: COLORES_GRAFICO.primario }
          ],
          tituloX: 'Modelo',
          min: params.log ? -1.7 : 0, max: params.log ? 1.3 : 13.5
        });

        const campos = [{
          etiqueta: 'escala',
          valor: params.log ? 'log₁₀ del RMSE (si no, el polinomio aplasta el resto)' : 'RMSE en logaritmos de la serie'
        }];
        M.forEach(m => campos.push({
          etiqueta: m.nombre,
          valor: `k-fold ${fmt(m.rmse_kfold, 4)} · real ${fmt(m.rmse_bloque_final, 4)} · ` +
            `optimismo ${m.optimismo_kfold > 0 ? '+' : ''}${fmt(m.optimismo_kfold, 1)} %` +
            (m.optimismo_kfold > 30 ? '  ⚠' : '')
        }));
        actualizarLectura(lectura, campos);
      }

      crearInterruptores(controles, [
        { clave: 'log', etiqueta: 'Escala logarítmica' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 6 — Elegir el modelo mirando el conjunto de prueba
    // ================================================================
    SIMULADORES['seleccion-prueba'] = function (raiz) {
      const S = FUGA.seleccion;
      const params = { marcarAicc: false };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const puntos = S.modelos.filter(m => m.rmse_prueba !== null);
      const ganadorVal = S.mejor_por_validacion;
      const ganadorAicc = S.mejor_por_aicc;
      const maxEje = Math.max.apply(null,
        puntos.map(m => Math.max(m.rmse_validacion, m.rmse_prueba))) * 1.05;

      function pintar() {
        const resto = puntos.filter(m => m.modelo !== ganadorVal && m.modelo !== ganadorAicc);
        const datasets = [
          {
            type: 'scatter', label: 'Los 36 modelos',
            data: resto.map(m => ({ x: m.rmse_validacion, y: m.rmse_prueba })),
            backgroundColor: 'rgba(71,85,105,0.55)', pointRadius: 4
          },
          {
            type: 'line', label: 'Diagonal: si la validación sirviera',
            data: [{ x: 0, y: 0 }, { x: maxEje, y: maxEje }],
            borderColor: COLORES_GRAFICO.gris, borderWidth: 1.2,
            borderDash: [5, 4], pointRadius: 0
          },
          {
            type: 'scatter', label: 'Ganador por validación',
            data: puntos.filter(m => m.modelo === ganadorVal)
              .map(m => ({ x: m.rmse_validacion, y: m.rmse_prueba })),
            backgroundColor: COLORES_GRAFICO.secundario, pointRadius: 8
          }
        ];
        if (params.marcarAicc) {
          datasets.push({
            type: 'scatter', label: 'Ganador por AICc',
            data: puntos.filter(m => m.modelo === ganadorAicc)
              .map(m => ({ x: m.rmse_validacion, y: m.rmse_prueba })),
            backgroundColor: COLORES_GRAFICO.primario, pointRadius: 8
          });
        }

        if (grafico) grafico.destroy();
        grafico = new Chart(canvas, {
          data: { datasets: datasets },
          options: {
            responsive: true, maintainAspectRatio: false, animation: false,
            plugins: {
              legend: { labels: { font: { family: 'Montserrat', size: 12 }, boxWidth: 24 } },
              tooltip: {
                backgroundColor: '#012820',
                titleFont: { family: 'Montserrat' }, bodyFont: { family: 'Fira Code' }
              }
            },
            scales: {
              x: {
                type: 'linear', min: 0, max: maxEje,
                title: { display: true, text: 'RMSE en el conjunto con el que se eligió', font: { family: 'Montserrat', size: 11 } },
                ticks: { font: { family: 'Fira Code', size: 10 } },
                grid: { color: 'rgba(148, 163, 184, 0.2)' }
              },
              y: {
                type: 'linear', min: 0, max: maxEje,
                title: { display: true, text: 'RMSE sobre un bloque nuevo', font: { family: 'Montserrat', size: 11 } },
                ticks: { font: { family: 'Fira Code', size: 10 } },
                grid: { color: 'rgba(148, 163, 184, 0.2)' }
              }
            }
          }
        });

        actualizarLectura(lectura, [
          { etiqueta: 'modelos comparados', valor: String(S.n_modelos) },
          { etiqueta: 'ganador por validación', valor: ganadorVal },
          { etiqueta: 'RMSE que se reportaría', valor: fmt(S.rmse_que_se_reporta, 2) },
          { etiqueta: 'RMSE real de ese mismo modelo', valor: fmt(S.rmse_real_del_mismo, 2) },
          { etiqueta: 'optimismo', valor: '+' + fmt(S.optimismo, 1) + ' %' },
          { etiqueta: 'ganador por AICc', valor: `${ganadorAicc} → RMSE real ${fmt(S.rmse_real_del_aicc, 2)}` },
          { etiqueta: 'RMSE real medio de los 36', valor: fmt(S.rmse_medio_prueba, 2) }
        ]);
      }

      crearInterruptores(controles, [
        { clave: 'marcarAicc', etiqueta: 'Marcar el ganador por AICc' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 7 — Recorrido de los orígenes
    // ================================================================
    SIMULADORES['origen-movil'] = function (raiz) {
      const O = ANIM.origenes;
      const params = { i: 0, deslizante: false, banda: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const o = O[Math.min(Math.round(params.i), O.length - 1)];
        const n = ANIM.serie.length;
        const desde = params.deslizante ? Math.max(0, o.T - o.ventana_desl) : 0;

        const usados = ANIM.serie.map((v, k) => (k >= desde && k <= o.T - 1 ? v : null));
        const ignorados = ANIM.serie.map((v, k) => (k < desde ? v : null));
        const futuro = ANIM.serie.map((v, k) => (k >= o.T - 1 ? v : null));

        const pon = (valores) => {
          const a = Array(n).fill(null);
          a[o.T - 1] = ANIM.serie[o.T - 1];
          valores.forEach((v, j) => { if (o.T + j < n) a[o.T + j] = v; });
          return a;
        };

        const sarima = params.deslizante ? o.sarima_desl : o.sarima;
        const datasets = [
          { label: 'Entrenamiento de este origen', data: usados, borderColor: COLORES_GRAFICO.primario, borderWidth: 2.2, pointRadius: 0 },
          { label: params.deslizante ? 'Descartado por la ventana' : '', data: ignorados, borderColor: 'rgba(148,163,184,0.55)', borderWidth: 1.6, pointRadius: 0 },
          { label: 'Observado después del origen', data: futuro, borderColor: COLORES_GRAFICO.gris, borderWidth: 2.2, pointRadius: 0 },
          { label: 'SARIMA', data: pon(sarima), borderColor: COLORES_GRAFICO.secundario, borderWidth: 2, borderDash: [5, 3], pointRadius: 0 },
          { label: 'Naive estacional', data: pon(o.snaive), borderColor: '#7c3aed', borderWidth: 1.5, borderDash: [3, 3], pointRadius: 0 },
          { label: 'ETS sobre log', data: pon(o.ets), borderColor: COLORES_GRAFICO.terciario, borderWidth: 1.5, borderDash: [3, 3], pointRadius: 0 }
        ];
        if (params.banda && !params.deslizante) {
          datasets.push({ label: '', data: pon(o.sarima_li95), borderColor: 'rgba(255,102,0,0.45)', borderWidth: 1, pointRadius: 0 });
          datasets.push({ label: '', data: pon(o.sarima_ls95), borderColor: 'rgba(255,102,0,0.45)', borderWidth: 1, pointRadius: 0 });
        }

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, ANIM.fechas, datasets, {
          plugins: { legend: { display: true, labels: { filter: it => it.text !== '' } } },
          scales: { x: { ticks: { maxTicksLimit: 12 } } }
        });

        const err = o.reales.map((r, j) => r - sarima[j]);
        const rmse = Math.sqrt(err.reduce((a, b) => a + b * b, 0) / err.length);
        const V = params.deslizante ? OM.ventanas.deslizante_72 : OM.ventanas.expansiva;
        actualizarLectura(lectura, [
          { etiqueta: 'origen', valor: `${o.fecha}  (${Math.round(params.i) + 1} de ${O.length})` },
          { etiqueta: 'ventana', valor: params.deslizante ? `deslizante de ${o.ventana_desl} meses` : `expansiva (${o.T} meses)` },
          { etiqueta: 'RMSE del SARIMA en este origen', valor: fmt(rmse, 2) },
          { etiqueta: 'RMSE sobre los 61 orígenes', valor: fmt(V.rmse, 2) },
          { etiqueta: 'MASE sobre los 61 orígenes', valor: fmt(V.mase, 3) }
        ]);
      }

      crearControles(controles, [{
        clave: 'i', etiqueta: 'Origen  ', min: 0, max: O.length - 1, paso: 1, decimales: 0
      }], params, pintar);
      crearInterruptores(controles, [
        { clave: 'deslizante', etiqueta: 'Ventana deslizante (72 meses)' },
        { clave: 'banda', etiqueta: 'Banda del 95 %' }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 7 — El error crece con el horizonte
    // ================================================================
    SIMULADORES['error-por-horizonte'] = function (raiz) {
      const filas = BT.tabla;
      const params = {};
      ['sarima', 'snaive', 'ets', 'auto'].forEach(id => { params['m_' + id] = true; });
      filas.forEach(f => { if (params['m_' + f.id] === undefined) params['m_' + f.id] = false; });
      params.deslizante = false;
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const datasets = [];
        filas.forEach((f, i) => {
          if (!params['m_' + f.id]) return;
          datasets.push({
            label: f.metodo, data: f.rmse_h,
            borderColor: PALETA6[i % PALETA6.length], borderWidth: 2, pointRadius: 2
          });
        });
        if (params.deslizante) {
          datasets.push({
            label: 'SARIMA, ventana deslizante', data: OM.ventanas.deslizante_72.rmse_h,
            borderColor: COLORES_GRAFICO.secundario, borderWidth: 1.6,
            borderDash: [4, 3], pointRadius: 2
          });
        }

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, HORIZONTES, datasets, {
          plugins: { legend: { display: true } },
          scales: {
            x: { title: { display: true, text: 'Horizonte', font: { family: 'Montserrat', size: 11 } } },
            y: { title: { display: true, text: 'RMSE', font: { family: 'Montserrat', size: 11 } }, beginAtZero: true }
          }
        });

        const campos = [];
        filas.forEach(f => {
          if (!params['m_' + f.id]) return;
          campos.push({
            etiqueta: f.metodo,
            valor: `h=1: ${fmt(f.rmse_h[0], 2)}  →  h=12: ${fmt(f.rmse_h[H6 - 1], 2)} ` +
              `(×${fmt(f.rmse_h[H6 - 1] / f.rmse_h[0], 2)})`
          });
        });
        actualizarLectura(lectura, campos);
      }

      crearInterruptores(controles,
        filas.map(f => ({ clave: 'm_' + f.id, etiqueta: f.metodo }))
          .concat([{ clave: 'deslizante', etiqueta: 'SARIMA con ventana deslizante' }]),
        params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 8 — Diebold–Mariano
    // ================================================================
    SIMULADORES['diebold-mariano'] = function (raiz) {
      const D = BT.dm_diferencias;
      const params = { rival: 'auto', h: 12 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const bloque = porId(D, params.rival);
        const serie = bloque.h.find(z => z.h === Number(params.h));
        const prueba = BT.dm.find(z => z.b === params.rival && z.h === Number(params.h));
        const etiquetas = serie.d.map((_, i) => String(i + 1));
        const tope = Math.max.apply(null, serie.d.map(Math.abs)) * 1.1;

        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, etiquetas, serie.d, {
          etiqueta: 'dᵢ = e²(SARIMA) − e²(rival)', color: COLORES_GRAFICO.terciario,
          lineas: [{ valor: 0, etiqueta: '' }],
          tituloX: 'Origen', min: -tope, max: tope
        });

        const aFavor = serie.d.filter(v => v < 0).length;
        actualizarLectura(lectura, [
          { etiqueta: 'rival', valor: bloque.nombre },
          { etiqueta: 'horizonte', valor: 'h = ' + params.h },
          { etiqueta: 'RMSE SARIMA / rival', valor: `${fmt(prueba.rmse_a, 2)} / ${fmt(prueba.rmse_b, 2)}` },
          { etiqueta: 'orígenes con dᵢ < 0 (gana el SARIMA)', valor: `${aFavor} de ${serie.d.length}` },
          { etiqueta: 'estadístico DM', valor: fmt(prueba.estadistico, 4) },
          {
            etiqueta: 'p-valor',
            valor: fmt(prueba.p, 4) + (prueba.significativo
              ? (prueba.estadistico < 0 ? '  ← el SARIMA gana, y es significativo'
                                        : '  ← el SARIMA PIERDE, y es significativo')
              : '  ← no se distingue del azar')
          }
        ]);
      }

      crearSelector(controles, {
        clave: 'rival', etiqueta: 'Rival del SARIMA',
        opciones: D.map(z => ({ valor: z.id, texto: z.nombre }))
      }, params, pintar);
      crearSelector(controles, {
        clave: 'h', etiqueta: 'Horizonte',
        opciones: [{ valor: 1, texto: 'h = 1' }, { valor: 6, texto: 'h = 6' }, { valor: 12, texto: 'h = 12' }]
      }, params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 9 — El puntaje de Winkler
    // ================================================================
    SIMULADORES['winkler'] = function (raiz) {
      const W = EV.winkler_demo;
      const params = { centro: 100, ancho: 40 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const cerca = (arr, v) => arr.reduce((m, x, k) =>
        Math.abs(x - v) < Math.abs(arr[m] - v) ? k : m, 0);

      function pintar() {
        const ic = cerca(W.centros, params.centro);
        const ia = cerca(W.anchos, params.ancho);
        const curva = W.puntaje[ic];
        const marca = W.anchos.map((_, k) => (k === ia ? curva[k] : null));

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, W.anchos.map(String), [
          { label: `Puntaje con el intervalo centrado en ${W.centros[ic]}`, data: curva, borderColor: COLORES_GRAFICO.primario, borderWidth: 2.4, pointRadius: 0 },
          { label: '', data: marca, borderColor: COLORES_GRAFICO.secundario, borderWidth: 0, pointRadius: 6, pointBackgroundColor: COLORES_GRAFICO.secundario }
        ], {
          plugins: { legend: { display: true, labels: { filter: it => it.text !== '' } } },
          scales: {
            x: { title: { display: true, text: 'Ancho del intervalo', font: { family: 'Montserrat', size: 11 } } },
            y: { title: { display: true, text: 'Puntaje de Winkler (menor es mejor)', font: { family: 'Montserrat', size: 11 } }, beginAtZero: true }
          }
        });

        const c = W.centros[ic], a = W.anchos[ia];
        const li = c - a / 2, ls = c + a / 2;
        const dentro = W.real >= li && W.real <= ls;
        const mejorAncho = W.anchos[curva.indexOf(Math.min.apply(null, curva))];
        actualizarLectura(lectura, [
          { etiqueta: 'valor observado', valor: fmt(W.real, 0) },
          { etiqueta: 'intervalo', valor: `[${fmt(li, 1)}, ${fmt(ls, 1)}]  (ancho ${fmt(a, 0)})` },
          { etiqueta: '¿lo cubre?', valor: dentro ? 'sí' : 'NO' },
          { etiqueta: 'puntaje', valor: fmt(curva[ia], 2) + (dentro ? '  = el ancho' : '  = ancho + penalización') },
          { etiqueta: 'ancho óptimo con este centro', valor: fmt(mejorAncho, 0) },
          { etiqueta: 'penalización por salirse', valor: '2/α = ' + fmt(2 / (1 - W.nivel / 100), 0) + ' por unidad' }
        ]);
      }

      crearControles(controles, [
        { clave: 'centro', etiqueta: 'Centro del intervalo  ', min: 60, max: 140, paso: 5, decimales: 0 },
        { clave: 'ancho', etiqueta: 'Ancho del intervalo  ', min: 4, max: 120, paso: 4, decimales: 0 }
      ], params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 9 — Cobertura empírica frente a la nominal
    // ================================================================
    SIMULADORES['cobertura'] = function (raiz) {
      const M = INTER.metodos;
      const params = { nivel: '95' };
      ['sarima', 'ets', 'auto', 'snaive'].forEach(id => { params['m_' + id] = true; });
      M.forEach(m => { if (params['m_' + m.id] === undefined) params['m_' + m.id] = false; });
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      function pintar() {
        const nominal = Number(params.nivel);
        const campo = nominal === 80 ? 'cob80_h' : 'cob95_h';
        const total = nominal === 80 ? 'cob80' : 'cob95';

        const datasets = [{
          label: `Nivel nominal (${nominal} %)`, data: Array(H6).fill(nominal),
          borderColor: COLORES_GRAFICO.gris, borderWidth: 1.6,
          borderDash: [6, 4], pointRadius: 0
        }];
        M.forEach((m, i) => {
          if (!params['m_' + m.id]) return;
          datasets.push({
            label: m.metodo, data: m[campo],
            borderColor: PALETA6[i % PALETA6.length], borderWidth: 2, pointRadius: 2
          });
        });

        if (grafico) grafico.destroy();
        grafico = crearGraficoLinea(canvas, HORIZONTES, datasets, {
          plugins: { legend: { display: true } },
          scales: {
            x: { title: { display: true, text: 'Horizonte', font: { family: 'Montserrat', size: 11 } } },
            y: { min: 0, max: 105, title: { display: true, text: 'Cobertura empírica (%)', font: { family: 'Montserrat', size: 11 } } }
          }
        });

        const campos = [{ etiqueta: 'nivel nominal', valor: nominal + ' %' }];
        M.forEach(m => {
          if (!params['m_' + m.id]) return;
          const d = m[total] - nominal;
          campos.push({
            etiqueta: m.metodo,
            valor: fmt(m[total], 1) + ' %  (' + (d >= 0 ? '+' : '') + fmt(d, 1) + ')' +
              (Math.abs(d) > 8 ? '  ⚠' : '')
          });
        });
        actualizarLectura(lectura, campos);
      }

      crearSelector(controles, {
        clave: 'nivel', etiqueta: 'Nivel nominal',
        opciones: [{ valor: '80', texto: '80 %' }, { valor: '95', texto: '95 %' }]
      }, params, pintar);
      crearInterruptores(controles, M.map(m => ({ clave: 'm_' + m.id, etiqueta: m.metodo })),
        params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 10 — Los tres casos
    // ================================================================
    SIMULADORES['tres-casos'] = function (raiz) {
      const SERIES = {
        airpassengers: {
          nombre: 'AirPassengers (61 orígenes, h = 12)', filas: BT.tabla,
          nota: 'Gana el modelo: el SARIMA es primero en las cinco métricas puntuales.'
        },
        trm: {
          nombre: 'TRM (37 orígenes, h = 12)', filas: CASOS.trm.tabla,
          nota: 'Nadie vence al naive: no hay estructura que explotar.'
        },
        nilo: {
          nombre: 'Nilo (36 orígenes, h = 5)', filas: CASOS.nilo.tabla,
          nota: 'La partición única del Capítulo 4 coronaba a la deriva, que aquí es la última.'
        }
      };
      const params = { serie: 'airpassengers', metrica: 'rmse' };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      let grafico = null;

      const NOMBRES = { rmse: 'RMSE', mae: 'MAE', mape: 'MAPE (%)', mase: 'MASE' };

      function pintar() {
        const S = SERIES[params.serie];
        const orden = ordenarPor(S.filas, params.metrica, 'menor');
        const valores = orden.map(f => f[params.metrica]);
        const tope = Math.max.apply(null, valores) * 1.12;

        if (grafico) grafico.destroy();
        grafico = crearGraficoBarras(canvas, orden.map(f => f.metodo), valores, {
          etiqueta: NOMBRES[params.metrica], color: COLORES_GRAFICO.primario,
          lineas: params.metrica === 'mase' ? [{ valor: 1, etiqueta: 'MASE = 1' }] : [],
          tituloX: 'Método, ordenado de mejor a peor', min: 0, max: tope
        });

        const campos = [
          { etiqueta: 'serie', valor: S.nombre },
          { etiqueta: 'lectura', valor: S.nota }
        ];
        orden.forEach((f, i) => campos.push({
          etiqueta: `${i + 1}. ${f.metodo}`,
          valor: fmt(f[params.metrica], params.metrica === 'mase' ? 3 : 2)
        }));
        actualizarLectura(lectura, campos);
      }

      crearSelector(controles, {
        clave: 'serie', etiqueta: 'Serie',
        opciones: Object.keys(SERIES).map(k => ({ valor: k, texto: SERIES[k].nombre }))
      }, params, pintar);
      crearSelector(controles, {
        clave: 'metrica', etiqueta: 'Métrica',
        opciones: Object.keys(NOMBRES).map(k => ({ valor: k, texto: NOMBRES[k] }))
      }, params, pintar);

      pintar();
      return [manejador(() => grafico)];
    };

    // ================================================================
    // Módulo 11 — Auditoría de un análisis asistido por IA
    //
    // No estrena componente: es una pregunta de seleccion multiple del
    // componente `.quiz`, que ya corrige parcialmente y da retroalimentacion
    // por opcion. Vive en su propio contenedor data-quiz="auditoria" para no
    // mezclarse con la autoevaluacion del capitulo.
    // ================================================================
    AUTOEVALUACIONES['auditoria'] = [
      {
        tipo: 'multiple',
        modulo: 11,
        pregunta: 'Los diez pasos de este flujo se ejecutan sin errores ni avisos. ¿Cuáles producen un número engañoso?',
        pista: 'Ninguno falla al ejecutarse. Pregúntate en cada uno: ¿qué datos vio el modelo?, ¿son comparables las cantidades que se ponen en la misma tabla?, ¿tiene sentido el denominador?',
        retroAcierto: 'Los seis son <strong>2</strong> (AICc entre distintos $d$: el $n$ efectivo baja de $100$ a $98$), ' +
          '<strong>3</strong> (ADF con $k = 5 < m = 12$: el $p$-valor pasa de $0.01$ a $0.7711$), ' +
          '<strong>5</strong> (residuales presentados como pronóstico: $10.155$ frente a $18.92$), ' +
          '<strong>6</strong> (validación cruzada aleatoria: $0.1351$ prometido frente a $12.8984$ real), ' +
          '<strong>8</strong> (<code>as.numeric()</code> cambia la escala del MASE: $2.4935$ frente a $3.2153$) y ' +
          '<strong>9</strong> (MAPE sobre una serie que cruza el cero: $1093\\,\\%$ mientras el MASE dice $0.6062$). ' +
          'Los cuatro restantes son correctos; el <strong>10</strong> está incompleto —falta medir la cobertura— ' +
          'pero no engaña.',
        opciones: [
          {
            texto: '<strong>1.</strong> <code>plot(nilo); acf(nilo, lag.max = 24)</code> — mirar la serie y su correlograma antes de ajustar nada.',
            correcta: false,
            retro: 'Correcto tal cual está: es el primer paso del ciclo de Box–Jenkins del Capítulo 4, y no produce ninguna cifra que se pueda malinterpretar.'
          },
          {
            texto: '<strong>2.</strong> Ajustar la rejilla <code>expand.grid(p = 0:2, d = 0:2, q = 0:2)</code> y quedarse con el mínimo de AICc, que resulta ser un $(1,2,2)$.',
            correcta: true,
            retro: 'Fallo. El AICc <strong>no es comparable entre modelos con distinto $d$</strong>: cada diferencia cuesta una observación y el $n$ efectivo baja de $100$ a $99$ y a $98$. El «mejor» global tiene AICc $1264.60$ sobre $98$ observaciones y el mejor con $d=1$ tiene $1267.51$ sobre $99$. Hay que agrupar por $d$.'
          },
          {
            texto: '<strong>3.</strong> <code>adf.test(log(ap))</code> devuelve $p = 0.01$ y se concluye que la serie es estacionaria.',
            correcta: true,
            retro: 'Fallo. <code>adf.test</code> usa por defecto $k = \\lfloor(n-1)^{1/3}\\rfloor = 5$ rezagos, <strong>menos que el periodo estacional $m = 12$</strong>, y por eso rechaza la raíz unitaria en una serie con tendencia y estacionalidad evidentes. Con $k = 12$ el $p$-valor pasa a $0.7711$.'
          },
          {
            texto: '<strong>4.</strong> <code>checkresiduals(fit)</code> para comprobar que los residuales son ruido blanco.',
            correcta: false,
            retro: 'Correcto. Aquí los residuales sí sirven, que es exactamente para lo que valen: diagnosticar si el modelo dejó estructura sin capturar (tabla del Módulo 1).'
          },
          {
            texto: '<strong>5.</strong> <code>accuracy(fit)[, "RMSE"]</code> da $10.155$ y se reporta como «el modelo pronostica con un error de unos 10 pasajeros».',
            correcta: true,
            retro: 'Fallo. Eso son <strong>residuales</strong>: el modelo se estimó con esos mismos datos. Evaluado por origen móvil el RMSE real es $18.92$, casi el doble. La fila <code>Training set</code> nunca habla de pronóstico.'
          },
          {
            texto: '<strong>6.</strong> <code>pliegues &lt;- sample(rep(1:5, length.out = nrow(X)))</code> para validar de forma cruzada la matriz de rezagos.',
            correcta: true,
            retro: 'Fallo. El reparto aleatorio deja los vecinos temporales de cada punto de prueba dentro del entrenamiento. Con un modelo que interpole en el tiempo el optimismo es enorme: un polinomio de grado $8$ prometía $0.1351$ y su error real era $12.8984$.'
          },
          {
            texto: '<strong>7.</strong> Partir con <code>window(ap, end = c(1958,12))</code> y reajustar el modelo usando solo el entrenamiento.',
            correcta: false,
            retro: 'Correcto. Partición temporal, sin mezclar, y el modelo no ve el conjunto de prueba. Es el mínimo honesto del Módulo 6.'
          },
          {
            texto: '<strong>8.</strong> <code>accuracy(fc, as.numeric(te))[, "MASE"]</code> para obtener el MASE del conjunto de prueba.',
            correcta: true,
            retro: 'Fallo. <code>as.numeric()</code> le quita la frecuencia al conjunto de prueba y entonces <code>accuracy</code> escala el MASE con el naïve <em>simple</em> en vez del estacional. Sobre el naïve estacional el mismo cambio lleva el MASE de $2.4935$ a $3.2153$, un $28.9\\,\\%$ de diferencia sin ningún aviso.'
          },
          {
            texto: '<strong>9.</strong> El MAPE sobre los log-retornos de la TRM da $1093\\,\\%$ y se concluye que el modelo no sirve.',
            correcta: true,
            retro: 'Fallo. La serie de retornos <strong>cruza el cero</strong>: un mes con retorno $-0.0029\\,\\%$ aporta él solo un error porcentual de $16\\,092\\,\\%$. El MASE del mismo pronóstico es $0.6062$, es decir, mejor que la referencia.'
          },
          {
            texto: '<strong>10.</strong> <code>forecast(fit, h = 12, level = c(80, 95))</code> y dibujar el abanico en el informe.',
            correcta: false,
            retro: 'Correcto en lo que hace. Está <em>incompleto</em> —falta comprobar la cobertura empírica del Módulo 9—, pero el número que produce no engaña a nadie. Es el paso que casi nadie da, no un error.'
          }
        ]
      }
    ];

    // ================================================================
    // Tablas ordenables (.tabla-ranking)
    // ================================================================
    TABLAS_RANKING['backtest'] = function () {
      return {
        descripcion: 'Ocho métodos evaluados sobre los mismos <strong>61 orígenes</strong> de ' +
          'AirPassengers con $h = 12$. Pulsa la cabecera de cualquier columna para reordenar: ' +
          'las cinco métricas puntuales dan el mismo orden, y la cobertura y el tiempo lo cambian.',
        columnas: [
          { clave: 'metodo', titulo: 'Método', tipo: 'texto' },
          { clave: 'rmse', titulo: 'RMSE', tituloLargo: 'RMSE', decimales: 2, mejor: 'menor' },
          { clave: 'mae', titulo: 'MAE', decimales: 2, mejor: 'menor' },
          { clave: 'mape', titulo: 'MAPE', decimales: 2, sufijo: ' %', mejor: 'menor' },
          { clave: 'mase', titulo: 'MASE', decimales: 3, mejor: 'menor' },
          { clave: 'cob95', titulo: 'Cob. 95 %', tituloLargo: 'cobertura del 95 %', decimales: 1, sufijo: ' %', mejor: 'cerca', objetivo: 95 },
          { clave: 'winkler95', titulo: 'Winkler', tituloLargo: 'puntaje de Winkler al 95 %', decimales: 1, mejor: 'menor' },
          { clave: 'segundos', titulo: 'Segundos', tituloLargo: 'segundos de cómputo', decimales: 2, mejor: 'menor' }
        ],
        filas: BT.tabla.map(f => ({
          metodo: f.metodo, rmse: f.rmse, mae: f.mae, mape: f.mape, mase: f.mase,
          cob95: f.cob95, winkler95: f.winkler95, segundos: f.segundos
        })),
        inicial: 'rmse',
        destacada: 'SARIMA airline',
        pie: 'El MASE del SARIMA, $0.621$, dice que comete un $38\\,\\%$ menos de error que el ' +
          'naive estacional de referencia. Ordenando por <em>cobertura</em> cae al quinto puesto y ' +
          'ordenando por <em>segundos</em>, <code>auto.arima</code> se hunde al último.'
      };
    };

    TABLAS_RANKING['nilo'] = function () {
      const P = {}; CASOS.nilo.particion.forEach(z => { P[z.id] = z; });
      return {
        descripcion: 'El Nilo evaluado de las dos maneras: la <strong>partición única</strong> del ' +
          'Capítulo 4 (entrenamiento hasta 1950, prueba de 20 años) y el <strong>origen móvil</strong> ' +
          'sobre 36 orígenes con $h = 5$. Pulsa una y otra columna.',
        columnas: [
          { clave: 'metodo', titulo: 'Método', tipo: 'texto' },
          { clave: 'particion', titulo: 'RMSE partición', tituloLargo: 'RMSE con una sola partición', decimales: 2, mejor: 'menor' },
          { clave: 'movil', titulo: 'RMSE origen móvil', tituloLargo: 'RMSE por origen móvil', decimales: 2, mejor: 'menor' },
          { clave: 'mase', titulo: 'MASE móvil', decimales: 3, mejor: 'menor' },
          { clave: 'cob95', titulo: 'Cob. 95 %', decimales: 1, sufijo: ' %', mejor: 'cerca', objetivo: 95 }
        ],
        filas: CASOS.nilo.tabla.map(f => ({
          metodo: f.metodo,
          particion: P[f.id] ? P[f.id].rmse : null,
          movil: f.rmse, mase: f.mase, cob95: f.cob95
        })),
        inicial: 'particion',
        destacada: 'Deriva',
        pie: 'La <strong>deriva</strong> es primera con una partición y última con treinta y seis. ' +
          'Es el mismo código, los mismos datos y dos veredictos opuestos.'
      };
    };

    // ================================================================
    // Autoevaluación
    // ================================================================
    AUTOEVALUACIONES['cap6'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'Un informe dice: «el modelo pronostica con un RMSE de $10.16$ pasajeros», y ese número viene de <code>accuracy(fit)</code> sobre el modelo ajustado con toda la serie. ¿Qué hay que responder?',
        pista: 'Pregúntate qué datos vio el modelo cuando produjo las predicciones que entran en ese número.',
        opciones: [
          {
            texto: 'Que ese número son residuales y no dice nada sobre pronóstico: evaluado fuera de muestra, el mismo modelo da $18.92$.',
            correcta: true,
            retro: 'Exacto. <code>accuracy()</code> con un solo argumento devuelve la fila <code>Training set</code>, calculada sobre datos que el modelo usó para estimarse. La razón entre los dos números es $1.86$ en este caso, y depende del tramo: en los once cortes medidos va de $0.85$ a $4.07$.'
          },
          {
            texto: 'Que el RMSE no es la métrica adecuada y habría que usar MASE.',
            correcta: false,
            retro: 'Cambiar de métrica no arregla nada: el MASE de esos mismos residuales es $0.2297$ y es igual de engañoso. El problema no es qué se mide sino <em>sobre qué datos</em> se mide.'
          },
          {
            texto: 'Que falta indicar el horizonte al que se pronostica.',
            correcta: false,
            retro: 'Es una observación correcta y aparte —el error sí depende de $h$, y por eso el Módulo 7 insiste en declararlo—, pero aquí el problema es anterior: ese número no corresponde a ningún horizonte de pronóstico, son ajustes de un paso dentro de la muestra.'
          },
          {
            texto: 'Que hay que comprobar antes que los residuales pasen Ljung–Box.',
            correcta: false,
            retro: 'También es buena práctica, y de hecho este modelo la pasa. Pero un modelo puede tener residuales perfectamente blancos y pronosticar mal: el diagnóstico y la evaluación responden preguntas distintas (tabla del Módulo 1).'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 5,
        unidad: '',
        pregunta: 'Una serie mensual tiene, en su conjunto de entrenamiento, un MAE del naïve estacional de $Q = 25$. Un modelo comete un MAE de $20$ sobre el conjunto de prueba. ¿Cuánto vale su MASE?',
        pista: 'El MASE es el MAE del método dividido por la escala $Q$, que se calcula sobre el entrenamiento y no sobre la prueba.',
        respuesta: 0.8,
        tolerancia: 0.01,
        retroAcierto: 'Correcto: $20/25 = 0.8$. Al ser menor que $1$, el modelo comete menos error pronosticando que el naïve estacional prediciendo un paso dentro del entrenamiento. Es la única de las métricas del capítulo cuyo valor se puede leer sin saber nada de las unidades de la serie.',
        retroFallo: 'El MASE es $\\text{MAE}/Q = 20/25 = 0.8$. Cuidado con invertir la división: $25/20 = 1.25$ diría lo contrario. Y cuidado también con calcular $Q$ sobre el conjunto de prueba, que es el error que hace que el MASE deje de ser comparable entre particiones.'
      },
      {
        tipo: 'multiple',
        modulo: 4,
        pregunta: 'Sobre los log-retornos de la TRM, el MAPE de un pronóstico da $1093\\,\\%$ y su MASE $0.6062$. ¿Cuáles de estas afirmaciones son ciertas?',
        pista: 'Mira qué hay en el denominador de cada métrica y qué le pasa a ese denominador en una serie de retornos.',
        opciones: [
          {
            texto: 'El $1093\\,\\%$ no mide la calidad del pronóstico sino la cercanía de la serie al cero.',
            correcta: true,
            retro: 'Sí. Un solo mes con retorno $-0.0029\\,\\%$ aporta un error porcentual de $16\\,092\\,\\%$; la mediana de los $|p_i|$ es $116.73\\,\\%$, diez veces menor que la media.'
          },
          {
            texto: 'El MASE $< 1$ indica que el pronóstico le gana al método de referencia.',
            correcta: true,
            retro: 'Correcto, y es la conclusión útil: la misma predicción que el MAPE declara catastrófica es mejor que la referencia.'
          },
          {
            texto: 'Bastaría con quitar los meses cercanos a cero para que el MAPE fuera válido.',
            correcta: false,
            retro: 'No: eso es elegir qué observaciones entran en la evaluación según su valor, que sesga la métrica y la vuelve incomparable. Además hay $6$ meses con $|{\\cdot}| < 0.1\\,\\%$ en esta serie, y el problema reaparecería con cualquier corte.'
          },
          {
            texto: 'El sMAPE resolvería el problema porque su denominador es simétrico.',
            correcta: false,
            retro: 'No lo resuelve. Sobre estos mismos datos el sMAPE da $121.80\\,\\%$: un número más cómodo pero igual de arbitrario, porque su denominador $|y|+|\\hat y|$ también se acerca a cero.'
          }
        ]
      },
      {
        tipo: 'opcion',
        modulo: 6,
        pregunta: 'Un compañero aplica validación cruzada de $5$ pliegues aleatorios a una regresión sobre los rezagos $1$ a $13$ de una serie, y obtiene un RMSE de $0.0476$. Sobre un bloque final intacto el error real es $0.0391$. ¿Qué se concluye?',
        pista: 'Compara la dirección del error: ¿el procedimiento prometió más o menos error del que hubo?',
        opciones: [
          {
            texto: 'Que en este montaje concreto el $k$-fold aleatorio no sobrestimó el desempeño: se quedó corto, que es el lado seguro.',
            correcta: true,
            retro: 'Exacto, y es la parte del eslogan que conviene matizar. Con rezagos como únicos predictores, el reparto al azar no regala información porque los rezagos ya contienen a los vecinos. El optimismo aparece cuando el modelo <em>interpola en el tiempo</em>: con $3$ vecinos más cercanos sube al $58\\,\\%$ y con un polinomio de grado $8$ al $99\\,\\%$.'
          },
          {
            texto: 'Que la validación cruzada aleatoria siempre sobrestima el desempeño en series de tiempo, y aquí hay un error de cálculo.',
            correcta: false,
            retro: 'La afirmación «siempre» es la que este módulo desmiente midiendo. No hay error de cálculo: los cinco montajes del simulador se evalúan con el mismo código y solo tres de los cinco muestran optimismo.'
          },
          {
            texto: 'Que el bloque final es demasiado pequeño para concluir nada.',
            correcta: false,
            retro: 'Son $24$ observaciones, pocas para una estimación precisa, pero el fenómeno que se está comparando es de otro orden: en el montaje del polinomio la diferencia es de $0.1351$ frente a $12.8984$, un factor de $95$ que ningún tamaño de muestra razonable explicaría.'
          },
          {
            texto: 'Que hay que usar <code>TimeSeriesSplit</code> de sklearn, que sí respeta el orden.',
            correcta: false,
            retro: 'Respeta el orden, sí, y es preferible al $k$-fold aleatorio. Pero su ventana de prueba crece de tamaño y no fija el horizonte $h$, así que no responde «¿cuánto me equivoco a 12 meses vista?». Para eso hay que construir el origen móvil (Módulo 7).'
          }
        ]
      },
      {
        tipo: 'numerica',
        modulo: 7,
        unidad: 'orígenes',
        pregunta: 'Una serie mensual tiene $n = 144$ observaciones. Se evalúa por origen móvil con ventana expansiva, primer origen $T_0 = 72$ y horizonte $h = 12$, exigiendo que todos los orígenes tengan los $12$ horizontes completos. ¿Cuántos orígenes salen?',
        pista: 'El último origen válido es aquel al que todavía le quedan $h$ observaciones por delante.',
        respuesta: 61,
        tolerancia: 0.5,
        retroAcierto: 'Correcto: los orígenes van de $T_0 = 72$ a $n - h = 132$, es decir $132 - 72 + 1 = 61$, y producen $61 \\times 12 = 732$ errores de pronóstico frente a los $24$ de una partición única.',
        retroFallo: 'Los orígenes van de $T_0$ a $n - h$, ambos incluidos: $132 - 72 + 1 = 61$. Si te salió $60$, probablemente olvidaste incluir uno de los extremos —es el mismo desfase por el que <code>tsCV</code> con <code>initial = 72</code> empieza en el origen $73$ y con <code>window = 72</code> empieza en el $72$—.'
      },
      {
        tipo: 'grafico',
        modulo: 9,
        pregunta: 'El gráfico muestra la cobertura empírica del intervalo del naïve estacional en los doce horizontes, con el nivel nominal del $80\\,\\%$ marcado. Sabiendo que al $95\\,\\%$ ese mismo método cubre un correcto $93.4\\,\\%$, ¿cuál es el diagnóstico?',
        pista: 'Un intervalo demasiado estrecho fallaría en los dos niveles. Piensa qué otra cosa puede desplazar sistemáticamente el intervalo respecto del valor observado.',
        opciones: [
          {
            texto: 'El pronóstico está <strong>sesgado</strong>: su centro está desplazado casi una desviación típica, así que la banda estrecha se queda del lado equivocado y la ancha todavía alcanza.',
            correcta: true,
            retro: 'Eso es. El sesgo medio del naïve estacional en estos orígenes es $+38.68$ frente a un RMSE de $42.55$: una razón de $0.909$. La banda de $\\pm 1.28\\sigma$ no llega y la de $\\pm 1.96\\sigma$ sí. Comprobar solo el $95\\,\\%$ habría dado el intervalo por bueno.'
          },
          {
            texto: 'El intervalo es demasiado estrecho y hay que ensancharlo.',
            correcta: false,
            retro: 'Si fuera demasiado estrecho fallaría también al $95\\,\\%$, y ahí cubre $93.4\\,\\%$, prácticamente lo prometido. El problema no es el ancho sino dónde está el centro.'
          },
          {
            texto: 'Los residuales no son normales y por eso los cuantiles están mal.',
            correcta: false,
            retro: 'La no normalidad afectaría sobre todo a los niveles <em>altos</em>, que son los que dependen de las colas, y aquí el $95\\,\\%$ es el que funciona. Además el patrón es plano en los doce horizontes, lo que apunta a un desplazamiento constante y no a la forma de la distribución.'
          },
          {
            texto: 'Con $61$ orígenes solapados la cobertura no se puede estimar.',
            correcta: false,
            retro: 'El solape afecta a la <em>precisión</em> de la estimación, no la invalida. Una cobertura del $46\\,\\%$ frente a un $80\\,\\%$ nominal, sostenida en los doce horizontes, no se explica por el solape.'
          }
        ],
        dibujar: function (canvas) {
          const snaive = INTER.metodos.find(m => m.id === 'snaive');
          return crearGraficoLinea(canvas, HORIZONTES, [
            {
              label: 'Nivel nominal (80 %)', data: Array(H6).fill(80),
              borderColor: COLORES_GRAFICO.gris, borderWidth: 1.6,
              borderDash: [6, 4], pointRadius: 0
            },
            {
              label: 'Naive estacional', data: snaive.cob80_h,
              borderColor: COLORES_GRAFICO.secundario, borderWidth: 2.4, pointRadius: 3
            }
          ], {
            plugins: { legend: { display: true } },
            scales: { y: { min: 0, max: 100, title: { display: true, text: 'Cobertura empírica (%)', font: { family: 'Montserrat', size: 11 } } } }
          });
        }
      },
      {
        tipo: 'opcion',
        modulo: 8,
        pregunta: 'En la tabla de backtesting, el SARIMA tiene un RMSE de $18.92$ y <code>auto.arima</code> de $20.63$. La prueba de Diebold–Mariano entre los dos da $p = 0.9662$, $0.4245$ y $0.2744$ en $h = 1, 6$ y $12$, y el SARIMA gana solo en el $45.9\\,\\%$ de los orígenes. ¿Qué se reporta?',
        pista: 'Fíjate en que el porcentaje de orígenes ganados está por debajo del $50\\,\\%$ y que la tabla agregada dice lo contrario.',
        opciones: [
          {
            texto: 'Que los dos son indistinguibles, y entonces se elige por otro criterio: aquí, que uno tarda $0.44$ s y el otro $118.61$.',
            correcta: true,
            retro: 'Correcto. La diferencia de $1.71$ en el RMSE agregado cabe dentro del ruido, y de hecho <code>auto.arima</code> gana en más orígenes de los que pierde. Cuando dos métodos empatan estadísticamente, deciden el costo, la simplicidad y la interpretabilidad.'
          },
          {
            texto: 'Que el SARIMA es mejor, porque su RMSE es menor sobre los mismos 61 orígenes.',
            correcta: false,
            retro: 'Es lo que dice el agregado y es justo lo que el contraste desmiente. Con errores tan correlacionados entre métodos —los dos se equivocan en los mismos tramos difíciles— una diferencia de RMSE puede venir de unos pocos orígenes.'
          },
          {
            texto: 'Que hay que aumentar el número de orígenes hasta que el $p$-valor baje de $0.05$.',
            correcta: false,
            retro: 'Eso es buscar la significancia hasta encontrarla, y sobre esta serie ni siquiera es posible: los $61$ orígenes son todos los que caben con $T_0 = 72$ y $h = 12$. Un $p$ alto es un resultado, no un problema que arreglar.'
          },
          {
            texto: 'Que el contraste no es aplicable porque los orígenes se solapan.',
            correcta: false,
            retro: 'Diebold–Mariano está diseñado precisamente para errores autocorrelacionados: por eso lleva el argumento $h$ y la corrección de Harvey–Leybourne–Newbold. Lo que sí hay que vigilar es que el estimador de varianza por defecto no salga negativo.'
          }
        ]
      },
      {
        tipo: 'opcion',
        modulo: 10,
        pregunta: 'Sobre el Nilo, la partición única del Capítulo 4 ordena deriva $(122.28) <$ naïve $(123.06) <$ ARIMA$(1,1,1)$ $(125.05)$; con $36$ orígenes el orden es ARIMA $(121.37) <$ media $(132.51) <$ naïve $(157.69) <$ deriva $(161.27)$. ¿Qué explica la inversión?',
        pista: 'Piensa cuántos números independientes hay detrás de cada una de las dos evaluaciones, y qué tramo concreto de la serie cubre la primera.',
        opciones: [
          {
            texto: 'Que la partición mide el comportamiento en <em>un</em> tramo, y ese tramo empieza justo después del escalón de 1899, donde una recta descendente parece razonable.',
            correcta: true,
            retro: 'Eso es. Con $20$ observaciones de un solo tramo, qué tramo toque pesa más que la diferencia entre métodos. Promediando sobre $36$ orígenes el efecto se diluye y aparece lo que el Capítulo 4 ya había concluido por otras vías: la caída del caudal fue un cambio de nivel, no una pendiente.'
          },
          {
            texto: 'Que el horizonte cambia de $20$ a $5$, y la deriva empeora con horizontes cortos.',
            correcta: false,
            retro: 'El horizonte sí cambia y sí influye, pero en la dirección contraria: extrapolar una tendencia se vuelve <em>más</em> arriesgado cuanto más lejos se mira, no menos. Si el horizonte fuera la explicación, la deriva debería salir mejor con $h = 5$.'
          },
          {
            texto: 'Que el ARIMA$(1,1,1)$ está sobreajustado y por eso gana en la evaluación con más datos.',
            correcta: false,
            retro: 'Un modelo sobreajustado gana <em>dentro</em> de la muestra y pierde fuera; aquí pasa lo contrario. Además el origen móvil reajusta el modelo en cada origen, así que un sobreajuste se penalizaría, no se premiaría.'
          },
          {
            texto: 'Que hay un error en una de las dos evaluaciones, porque el mismo código no puede dar órdenes opuestos.',
            correcta: false,
            retro: 'Sí puede, y ese es el punto del módulo. Las dos evaluaciones están bien calculadas: responden preguntas distintas. La primera dice «qué pasó en 1951–1970» y la segunda «qué pasa en promedio», y solo la segunda sirve para elegir un método.'
          }
        ]
      }
    ];
