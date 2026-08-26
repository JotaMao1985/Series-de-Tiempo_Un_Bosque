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

    // Etiquetas mensuales AAAA-MM para la TRM.
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
    function fmt(x, d = 2) {
      if (x === null || x === undefined || !Number.isFinite(Number(x))) return '—';
      return Number(x).toLocaleString('es-CO', {
        minimumFractionDigits: d, maximumFractionDigits: d
      });
    }

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
        const titulo = d === 0 ? 'Caudal del Nilo' : `∇${d > 1 ? d : ''} Caudal del Nilo`;
        if (grafico) grafico.destroy();
        grafico = lineaSimple(canvas, etiquetas, y, titulo,
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario);
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'media', valor: fmt(media(y)) },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) },
          { etiqueta: 'ACF(1)', valor: fmt(calcularACF(y, 1)[0], 4) }
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
      const deltas = puntos.map(p => p.delta);
      const params = { delta: 100 };
      const lectura = raiz.querySelector('.simulador-lectura');
      const [cSerie, cCurva] = raiz.querySelectorAll('canvas');
      let gSerie = null, gCurva = null;

      // Ruido con semilla fija: la realización no cambia al mover el deslizador,
      // así que lo único que se mueve en el gráfico es el escalón.
      const ruido = generarRuidoNormal(malla.n, 20260726).map(z => 1000 + malla.sigma * z);
      const etiquetas = aniosDesde(1871, malla.n, 0);

      // Interpolación lineal sobre la malla precalculada en R.
      function interpolar(delta, campo) {
        if (delta <= deltas[0]) return puntos[0][campo];
        for (let i = 1; i < deltas.length; i++) {
          if (delta <= deltas[i]) {
            const t = (delta - deltas[i - 1]) / (deltas[i] - deltas[i - 1]);
            return puntos[i - 1][campo] + t * (puntos[i][campo] - puntos[i - 1][campo]);
          }
        }
        return puntos[puntos.length - 1][campo];
      }

      function pintar() {
        const d = params.delta;
        const y = ruido.map((v, i) => v - (i + 1 >= malla.posicion ? d : 0));
        if (gSerie) gSerie.destroy();
        gSerie = lineaSimple(cSerie, etiquetas, y,
          d === 0 ? 'Ruido blanco puro (sin escalón)' : `Ruido blanco + escalón de −${fmt(d, 0)}`,
          COLORES_GRAFICO.primario);

        const tasa = interpolar(d, 'kpss_rechaza');
        if (!gCurva) {
          gCurva = crearGraficoLinea(cCurva, deltas.map(String), [
            {
              label: 'Tasa de rechazo de KPSS',
              data: puntos.map(p => 100 * p.kpss_rechaza),
              borderColor: COLORES_GRAFICO.secundario,
              backgroundColor: 'rgba(255, 102, 0, 0.12)',
              borderWidth: 2, pointRadius: 3, fill: true
            },
            {
              label: 'Nivel nominal 5 %',
              data: puntos.map(() => 5),
              borderColor: COLORES_GRAFICO.gris,
              borderDash: [5, 4], borderWidth: 1.5, pointRadius: 0, fill: false
            },
            {
              label: 'δ elegido',
              data: puntos.map(() => null),
              borderColor: COLORES_GRAFICO.primario,
              borderWidth: 2, pointRadius: 0, fill: false
            }
          ], {
            scales: {
              x: { title: { display: true, text: 'Tamaño del escalón δ' },
                   ticks: { font: { family: 'Fira Code', size: 10 } }, grid: { display: false } },
              y: { min: 0, max: 105, ticks: { font: { family: 'Fira Code', size: 11 },
                   callback: v => v + ' %' } }
            }
          });
        }
        // La tercera serie marca con una barra vertical el delta elegido
        gCurva.data.datasets[2].data = deltas.map(v => (v === deltas.reduce(
          (mejor, cand) => Math.abs(cand - d) < Math.abs(mejor - d) ? cand : mejor,
          deltas[0]) ? 100 : null));
        gCurva.update('none');

        actualizarLectura(lectura, [
          { etiqueta: 'escalón δ', valor: d === 0 ? 'sin escalón' : `−${fmt(d, 0)}` },
          { etiqueta: 'en desv. típicas', valor: fmt(d / malla.sigma, 2) },
          { etiqueta: 'KPSS medio', valor: fmt(interpolar(d, 'kpss_medio'), 3) },
          { etiqueta: 'rechaza el', valor: `${fmt(100 * tasa, 1)} %` },
          { etiqueta: 'ndiffs medio', valor: fmt(interpolar(d, 'ndiffs_medio'), 2) }
        ]);
      }

      crearControles(raiz.querySelector('.simulador-controles'), [
        { clave: 'delta', etiqueta: 'Tamaño del escalón δ ', min: 0, max: 300, paso: 5, decimales: 0 }
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

      function pintar() {
        const d = parseInt(params.d, 10);
        const info = ident[claves[params.d]];
        const y = diferenciarVeces(SERIES_CAP4.nilo.valores, d);
        [gSerie, gAcf, gPacf].forEach(g => { if (g) g.destroy(); });
        gSerie = lineaSimple(cSerie, aniosDesde(SERIES_CAP4.nilo.inicio[0], y.length, d), y,
          d === 0 ? 'Nilo' : `∇${d > 1 ? d : ''} Nilo`,
          d === 1 ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.primario);
        gAcf = crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        });
        gPacf = crearGraficoBarras(cPacf, REZAGOS, info.pacf, {
          etiqueta: 'PACF muestral', color: COLORES_GRAFICO.terciario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        });
        const fuera = info.acf.filter(v => Math.abs(v) > info.banda).length;
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'banda', valor: `±${fmt(info.banda, 4)}` },
          { etiqueta: 'ρ₁', valor: fmt(info.acf[0], 4) },
          { etiqueta: 'ACF fuera de banda', valor: `${fuera} de ${info.acf.length}` },
          { etiqueta: 'varianza', valor: fmt(varianzaDe(y)) }
        ]);
      }

      crearSelector(raiz.querySelector('.simulador-controles'), {
        clave: 'd', etiqueta: 'Serie sobre la que se lee',
        opciones: [
          { valor: '0', texto: 'd = 0 — sin diferenciar' },
          { valor: '1', texto: 'd = 1 — ∇Nilo (la correcta)' },
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

      function pintar() {
        const clave = `${params.p}${params.d}${params.q}`;
        const m = REJILLA[clave];
        const mejor = NILO.mejor_por_d[`d${params.d}`];
        const hermanos = Object.values(REJILLA)
          .filter(x => x.d === params.d && x.convergio);

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
        gAcf = crearGraficoBarras(cAcf, REZAGOS, m.acf_residuales, {
          etiqueta: 'ACF de los residuales',
          color: m.ljung_box_p > 0.05 ? COLORES_GRAFICO.primario : '#b91c1c',
          lineas: lineasBanda(nEf), tituloX: 'Rezago k'
        });

        const esteEs = clave;
        gAicc = crearGraficoBarras(cAicc,
          hermanos.map(x => `(${x.p},${x.d},${x.q})`),
          hermanos.map(x => x.aicc - mejor.valor_aicc), {
            etiqueta: `AICc − mejor de d = ${params.d}`,
            color: COLORES_GRAFICO.gris,
            min: 0, max: Math.max(6, ...hermanos.map(x => x.aicc - mejor.valor_aicc))
          });
        // Se repinta en naranja la barra del modelo seleccionado
        gAicc.data.datasets[0].backgroundColor = hermanos.map(
          x => `${x.p}${x.d}${x.q}` === esteEs ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        gAicc.update('none');

        const campos = [
          { etiqueta: 'Modelo', valor: m.etiqueta },
          { etiqueta: 'n efectivo', valor: `${nEf} (= 100 − ${params.d})` },
          { etiqueta: 'AICc', valor: fmt(m.aicc) },
          { etiqueta: 'BIC', valor: fmt(m.bic) },
          { etiqueta: 'Ljung–Box(20)', valor: `p = ${fmt(m.ljung_box_p, 4)}` },
          { etiqueta: `mejor AICc de d = ${params.d}`, valor: fmt(mejor.valor_aicc) },
          { etiqueta: 'diferencia', valor: `+${fmt(m.aicc - mejor.valor_aicc)}` }
        ];
        if (m.raices && m.raices.degenerado) {
          campos.push({ etiqueta: '⚠ raíz sobre el círculo', valor: `|raíz MA| = ${fmt(m.raices.min_ma, 4)}` });
        }
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

      // La búsqueda exhaustiva no guarda la traza completa en el JSON (son 42
      // líneas); se reconstruye el ranking, que es lo que interesa de ella.
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
            }
          ], {
            scales: {
              x: { title: { display: true, text: 'Orden de evaluación' },
                   ticks: { font: { family: 'Fira Code', size: 10 } }, grid: { display: false } },
              y: { suggestedMin: 1265, suggestedMax: 1302,
                   ticks: { font: { family: 'Fira Code', size: 11 } } }
            }
          });

        const mejorados = visibles.filter(p => p.mejora).length;
        actualizarLectura(lectura, [
          { etiqueta: 'Paso', valor: `${hasta} de ${pasos.length}` },
          { etiqueta: 'Modelo evaluado', valor: actual.etiqueta },
          { etiqueta: 'AICc', valor: actual.infinito ? '∞ (descartado)' : fmt(actual.aicc, 3) },
          { etiqueta: '¿mejora?', valor: actual.mejora ? 'sí, pasa a ser el actual' : 'no' },
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
          d === 0 ? 'Nilo' : `∇${d > 1 ? d : ''} Nilo`,
          d <= 1 ? COLORES_GRAFICO.primario : '#b91c1c');

        gVar = crearGraficoBarras(cVar, tabla.map(f => `d = ${f.d}`),
          tabla.map(f => Math.log10(f.varianza)), {
            etiqueta: 'log₁₀ de la varianza', color: COLORES_GRAFICO.gris,
            min: 4, max: 5.6
          });
        gVar.data.datasets[0].backgroundColor = tabla.map(
          f => f.d === d ? COLORES_GRAFICO.secundario : COLORES_GRAFICO.gris);
        gVar.update('none');

        const degenerado = Math.abs(fila.theta_ma1 + 1) < 0.005;
        const campos = [
          { etiqueta: 'd', valor: d },
          { etiqueta: 'n', valor: fila.n },
          { etiqueta: 'varianza', valor: fmt(fila.varianza) },
          { etiqueta: 'ρ₁', valor: fmt(fila.acf1, 4) },
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

        datasets.push({
          label: 'Pronóstico',
          data: nulos.concat(f.media),
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
          scales: {
            x: { ticks: { font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 10, maxRotation: 0 },
                 grid: { display: false } },
            y: { ticks: { font: { family: 'Fira Code', size: 11 } },
                 grid: { color: 'rgba(148, 163, 184, 0.2)' } }
          }
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
              label: 'σ_h del ARIMA(1,1,1)',
              data: inter.sigma_h, borderColor: COLORES_GRAFICO.secundario,
              borderWidth: 2.2, pointRadius: 0, fill: false
            },
            {
              label: 'σ√h — lo que daría una caminata aleatoria',
              data: raizH, borderColor: COLORES_GRAFICO.terciario,
              borderDash: [6, 4], borderWidth: 1.8, pointRadius: 0, fill: false
            }
          ], {
            scales: {
              x: { title: { display: true, text: 'Horizonte h' },
                   ticks: { font: { family: 'Fira Code', size: 10 }, maxTicksLimit: 10 },
                   grid: { display: false } },
              y: { ticks: { font: { family: 'Fira Code', size: 11 } } }
            }
          });
        }

        actualizarLectura(lectura, [
          { etiqueta: 'h', valor: h },
          { etiqueta: 'ψ_{h−1}', valor: fmt(inter.psi[h - 1], 4) },
          { etiqueta: 'σ', valor: fmt(inter.sigma, 3) },
          { etiqueta: 'σ_h', valor: fmt(inter.sigma_h[h - 1], 3) },
          { etiqueta: 'σ√h', valor: fmt(inter.sigma * Math.sqrt(h), 3) },
          { etiqueta: 'semiancho 95 %', valor: fmt(inter.z95 * inter.sigma_h[h - 1], 2) },
          { etiqueta: 'σ_h / σ', valor: fmt(inter.sigma_h[h - 1] / inter.sigma, 3) },
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
          d === 0 ? COLORES_GRAFICO.primario : COLORES_GRAFICO.secundario);
        gAcf = crearGraficoBarras(cAcf, REZAGOS, info.acf, {
          etiqueta: 'ACF muestral', color: COLORES_GRAFICO.primario,
          lineas: lineasBanda(info.n), tituloX: 'Rezago k'
        });

        const fuera = info.acf.filter(v => Math.abs(v) > info.banda).length;
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'banda', valor: `±${fmt(info.banda, 4)}` },
          { etiqueta: 'ρ₁', valor: fmt(info.acf[0], 4) },
          { etiqueta: 'ACF fuera de banda', valor: `${fuera} de ${info.acf.length}` },
          { etiqueta: d === 0 ? 'ADF (nivel)' : 'ADF (∇)',
            valor: `p = ${fmt(d === 0 ? TRM.pruebas.adf_nivel.p : TRM.pruebas.adf_d1.p, 4)}` },
          { etiqueta: d === 0 ? 'KPSS (nivel)' : 'KPSS (∇)',
            valor: fmt(d === 0 ? TRM.pruebas.kpss_nivel.estadistico : TRM.pruebas.kpss_d1.estadistico, 4) }
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
          aicc: m.aicc, bic: m.bic, lb: m.ljung_box_12_p
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
          { clave: 'k', titulo: 'Coeficientes', decimales: 0, mejor: 'menor' },
          { clave: 'aicc', titulo: 'AICc', decimales: 2, mejor: 'menor' },
          { clave: 'bic', titulo: 'BIC', decimales: 2, mejor: 'menor' },
          { clave: 'lb', titulo: 'Ljung–Box p', tituloLargo: 'p-valor de Ljung-Box', decimales: 4, mejor: 'mayor' }
        ],
        filas: filas,
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
            retro: 'Es la trampa central del capítulo. Un AICc menor con más diferencias no significa un modelo mejor: significa, en buena parte, <strong>menos observaciones que explicar</strong>. Y en el Nilo ese modelo concreto tiene además una raíz MA en $1.03$, casi sobre el círculo unitario.'
          },
          {
            texto: 'Ninguno de los dos por esta comparación: no son comparables, porque tienen distinto $d$.',
            correcta: true,
            retro: 'Exacto. El primero se calcula sobre $n^{*} = 99$ diferencias y el segundo sobre $98$ segundas diferencias: <strong>datos distintos</strong>. La comparación por AICc solo vale dentro de un mismo $d$. Para decidir entre distintos $d$ hay que usar las pruebas de raíz unitaria, el gráfico, o una evaluación fuera de muestra.'
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
            retro: 'Correcto. $\\hat\\rho_{12} = 0.72$ y $\\hat\\rho_{24} = 0.67$ frente a una banda de $0.163$: la estructura sobrante es exactamente estacional. Subir $q$ hasta 24 lo cubriría con dos docenas de parámetros; un SARIMA lo hace con dos. Es el Capítulo 5.'
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
          { texto: 'Con $d \\ge 2$, <code>forecast::Arima</code> avisa y no ajusta la deriva.', correcta: true },
          { texto: 'Sin constante, un modelo con $d = 2$ pronostica una parábola.', correcta: false },
          { texto: 'La constante de un ARIMA($p,0,q$) es la ordenada al origen de una regresión, no la media del proceso.', correcta: false }
        ],
        retroAcierto: 'Las tres primeras. Y las dos falsas son justo las que el capítulo desmiente midiendo: con $d = 2$ y sin constante la segunda diferencia del pronóstico se anula ($\\Delta^2 = 0$), es decir sale una <strong>recta</strong>; y el <code>intercept</code> que devuelve R para un ARIMA($p,0,q$) <strong>es</strong> la media del proceso, $920.70$ en el Nilo, pese al nombre.',
        retroFallo: 'Las correctas son las tres primeras. Sobre las falsas: la parábola necesitaría constante <em>con</em> $d = 2$, y <code>forecast</code> se niega precisamente a eso; sin constante, el pronóstico con $d = 2$ es una recta (lo verifica el Módulo 9 midiendo $\\Delta^2 = 0$). Y el <code>intercept</code> de R en un modelo con $d = 0$ es la media, no una ordenada al origen: el nombre despista.'
      },
      {
        tipo: 'opcion',
        modulo: 3,
        pregunta: 'Simulas $1000$ series de ruido blanco puro y les añades a todas un escalón en la mitad. ¿Con qué frecuencia rechaza KPSS la hipótesis de estacionariedad?',
        pista: 'Recuerda cómo se construye el estadístico: sobre las <em>sumas parciales</em> de los residuales respecto de la media global. ¿Qué le pasa a esas sumas cuando todos los residuales de un tramo tienen el mismo signo?',
        opciones: [
          {
            texto: 'Prácticamente siempre, si el escalón es apreciable: con el del Nilo, el $100\\,\\%$ de las veces.',
            correcta: true,
            retro: 'Correcto, y es el experimento del Módulo 3. Sin escalón rechaza el $4.8\\,\\%$ —su tamaño nominal—, y con el escalón real del Nilo ($1.95$ desviaciones típicas) el $100\\,\\%$. Basta un escalón de $0.79$ desviaciones para llegar al $70.8\\,\\%$. KPSS no distingue una raíz unitaria de un cambio de nivel.'
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
            retro: 'Depende de los dos, y la simulación lo muestra: con $n$ fijo en 100, la tasa de rechazo pasa del $4.5\\,\\%$ al $100\\,\\%$ solo moviendo $\\delta$. El estadístico crece aproximadamente como $n\\delta^2/\\hat\\sigma^2_{LP}$.'
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
            retro: 'Es el error de principiante más caro del capítulo. Un AR estacionario tiene una ACF que decae <strong>geométricamente</strong>, es decir, deprisa; ésta lleva veinte rezagos sin acercarse a cero. Lo que ves no es memoria larga del proceso: es que el nivel de la serie está vagando.'
          },
          {
            texto: 'Es un MA($q$) con $q$ igual al número de barras significativas.',
            correcta: false,
            retro: 'Un MA($q$) tiene la ACF <strong>exactamente</strong> cero a partir del rezago $q$ — un corte limpio, no un descenso gradual. Aquí no hay corte por ninguna parte.'
          },
          {
            texto: 'Que $d = 1$, porque el primer valor es $0.498$, cercano a $0.5$.',
            correcta: false,
            retro: 'La conclusión sobre $d$ es correcta pero el argumento no: el valor de $\\rho_1$ no determina $d$. Lo que indica no estacionariedad es la <strong>forma</strong> del decaimiento —lento y sin cortar—, no la altura de la primera barra. Un AR(1) con $\\phi = 0.5$ tendría también $\\rho_1 = 0.5$ y sería perfectamente estacionario.'
          },
          {
            texto: 'Nada todavía: esa forma indica no estacionariedad, y hay que diferenciar antes de leer $p$ y $q$.',
            correcta: true,
            retro: 'Exacto. Una ACF que decae despacio y no corta —aquí $0.498,\\ 0.385,\\ 0.328,\\ 0.239,\\dots$— es el retrato de una serie no estacionaria. La tabla de identificación presupone estacionariedad; aplicarla aquí no informa de nada. Tras diferenciar, la misma serie tiene una sola barra fuera de la banda.'
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
            retro: 'Correcto. La diferencia entre el primero y el quinto es de $1.71$ puntos, por debajo del umbral habitual de $2$. Entre esos cinco está el ARIMA($0,1,1$) que proponía el correlograma. <code>auto.arima</code> no miente, pero su salida de una línea no comunica esa incertidumbre; <code>trace = TRUE</code> sí.'
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
