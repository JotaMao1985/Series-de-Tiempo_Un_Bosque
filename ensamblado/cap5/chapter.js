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

    // Defensiva ante null: jsonlite escribe los valores infinitos como null y
    // Number(null) es 0, que en pantalla se leería como un cero legítimo.
    //
    // Punto decimal, como la prosa. Los miles se agrupan con un espacio fino
    // solo desde cinco cifras enteras (80 055.01); con cuatro van juntos
    // (1267.51), como los escribe el texto.
    //
    // Signo menos tipográfico (−0.42), como en las lecturas y en los ejes: la
    // tabla de la receta del Módulo 2 escribía «× -0.42 = -6.30» debajo de una
    // lectura que daba «−0.42». Un cero redondeado no lleva signo.
    function fmt(x, d = 2) {
      if (x === null || x === undefined || !Number.isFinite(Number(x))) return '—';
      const texto = agrupaMiles(Number(x).toLocaleString('en-US', {
        minimumFractionDigits: d, maximumFractionDigits: d
      }));
      return /^-0(\.0+)?$/.test(texto) ? texto.slice(1) : texto.replace(/^-/, '−');
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

    // Escalas completas de un gráfico de línea con título en el eje y (del
    // capítulo 4). crearGraficoLinea fusiona sus opciones con Object.assign,
    // que es superficial: quien pasa `scales` reemplaza x e y enteras, y con
    // ellas los ayudantes del armazón. Aquí van los dos ejes con la tipografía
    // de siempre y los ayudantes puestos otra vez: el x con marcasLegibles() y
    // rotuloLegible() (en las fechas AAAA-MM, los eneros con su año, sin que
    // se pisen) y el y con marcasVerticales() y rotuloVertical() (signo menos
    // tipográfico) y la línea del 0 más oscura. `x` y `y` se mezclan con sus
    // ejes, y sus `ticks`, clave a clave.
    function escalasLinea(tituloY, x = {}, y = {}) {
      const ticksX = Object.assign({
        font: { family: 'Montserrat', size: 11 }, maxTicksLimit: 12, maxRotation: 0,
        callback: rotuloLegible
      }, x.ticks);
      const ticksY = Object.assign({
        font: { family: 'Fira Code', size: 11 }, autoSkip: false, callback: rotuloVertical
      }, y.ticks);
      return {
        x: Object.assign({
          grid: { display: false },
          afterBuildTicks: eje => { marcasLegibles(eje, { maxMarcas: ticksX.maxTicksLimit }); }
        }, x, { ticks: ticksX }),
        y: Object.assign({
          title: { display: !!tituloY, text: tituloY, font: { family: 'Montserrat', size: 11 } },
          grid: { color: rejillaConCero },
          afterBuildTicks: marcasVerticales
        }, y, { ticks: ticksY })
      };
    }

    // Marcos y leyendas a la medida del ancho (del capítulo 4). Con el alto
    // fijo del HTML, la leyenda y los ejes dejaban áreas de dibujo de 85 a
    // 110 px (M4, M5, M6, M8 y la comparativa del M11). Por debajo de 420 px
    // la leyenda se compacta y el marco toma su alto de teléfono; onResize lo
    // reajusta si cambia el ancho.
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

    function barrasCompactas(g, altos) {
      g.options.onResize = (gr, t) => compactar(gr, t.width, altos);
      compactar(g, g.width, altos);
      g.update('none');
      return g;
    }

    function lineaCompacta(g, altos) { return barrasCompactas(g, altos); }

    // `aria-label` de un lienzo, con el signo menos tipográfico. Se llama en
    // cada pintar(): el lienzo dice lo que dibuja en ese momento, no lo que
    // dibujaba al abrir el módulo.
    function ariaLienzo(canvas, texto) {
      canvas.setAttribute('aria-label', conSignoMenos(texto));
    }

    // Un número en subíndice (ψ₃₅), para los rótulos que se componen en JS.
    function sub(n) {
      return String(n).replace(/\d/g, c => '₀₁₂₃₄₅₆₇₈₉'[Number(c)]);
    }

    // Mínimo y máximo de una serie, para los `aria-label`.
    function rangoDe(x) {
      const v = x.filter(z => z !== null && z !== undefined && Number.isFinite(z));
      return [Math.min(...v), Math.max(...v)];
    }

    // Rezagos (1, 2…) fuera de la banda ±b, separados en múltiplos de m y resto.
    function fueraDeBanda(acf, b, m = M_EST) {
      const fuera = acf.map((r, i) => (Math.abs(r) > b ? i + 1 : 0)).filter(k => k);
      return { estacionales: fuera.filter(k => k % m === 0), otros: fuera.filter(k => k % m !== 0) };
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
        ninguna: { texto: 'Sin diferenciar', d: 0, D: 0, aria: 'sin diferenciar' },
        d1: { texto: 'Regular ∇', d: 1, D: 0, aria: 'con la diferencia regular ∇' },
        D1: { texto: 'Estacional ∇₁₂', d: 0, D: 1, aria: 'con la diferencia estacional ∇₁₂' },
        d1D1: { texto: 'Ambas: ∇ ∇₁₂', d: 1, D: 1, aria: 'con las dos diferencias, ∇ ∇₁₂' }
      };
      const ALTOS = { estrecho: '260px', ancho: '250px' };

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
        const queSerie = info.nombre + (params.log ? ' en logaritmos' : '') + ', ' + t.aria;
        pintarMapaEstacional(mapa, Object.assign(
          matrizMesAnio(y, anio, mes),
          {
            escala: diferenciada ? 'divergente' : 'secuencial',
            decimales: decimales,
            unidad: '',
            descripcion: 'Mapa mes × año de ' + queSerie,
            nota: `<strong>${info.nombre}</strong> · ${etiquetaTrans}. ` +
              (diferenciada
                ? 'Escala divergente centrada en cero: naranja por debajo, verde por encima.'
                : 'Escala secuencial: cuanto más oscuro, más alto.')
          }));

        const maxLag = Math.min(DATOS_CAP5.max_rezago, y.length - 2);
        const acf = calcularACF(y, maxLag);
        if (grafico) grafico.destroy();
        grafico = barrasCompactas(crearGraficoBarras(canvas, etiquetasRezago(maxLag), acf, {
          etiqueta: 'ACF muestral',
          lineas: lineasBanda(y.length),
          tituloX: 'Rezago'
        }), ALTOS);

        const b = banda(y.length);
        ariaLienzo(canvas, descripcionCorrelograma('ACF muestral', queSerie, acf, b));
        // «Fuera de banda» separa los múltiplos de 12 del resto: el renglón solo
        // miraba 12, 24 y 36 y se leía como si no hubiera más barras fuera. La
        // lectura da las cifras; qué significa un ρ̂₁₂ negativo tras ∇₁₂ lo
        // discute la prosa (Módulos 3, 4 y 7).
        const fuera = fueraDeBanda(acf, b);
        actualizarLectura(lectura, [
          { etiqueta: 'n', valor: y.length },
          { etiqueta: 'ρ̂₁', valor: fmt(acf[0], 4) },
          { etiqueta: 'ρ̂₁₂', valor: maxLag >= 12 ? fmt(acf[11], 4) : '—' },
          { etiqueta: 'ρ̂₂₄', valor: maxLag >= 24 ? fmt(acf[23], 4) : '—' },
          { etiqueta: 'ρ̂₃₆', valor: maxLag >= 36 ? fmt(acf[35], 4) : '—' },
          { etiqueta: 'banda', valor: '±' + fmt(b, 4) },
          {
            etiqueta: 'múltiplos de 12 fuera de banda',
            valor: fuera.estacionales.length ? fuera.estacionales.join(', ') : 'ninguno'
          },
          {
            etiqueta: 'otros rezagos fuera de banda',
            valor: fuera.otros.length ? fuera.otros.join(', ') : 'ninguno'
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
    // Módulo 2 · La receta de un mes: el satélite con tres números
    // ================================================================
    // Heladería inventada, en desvíos de su promedio: febrero y marzo de 2024
    // y febrero de 2025 son conocidos; se pronostica marzo de 2025 con un
    // SARIMA(1,0,0)(1,0,0)₁₂. Los tres valores son fijos para que cada aporte
    // se compruebe de cabeza; los deslizadores solo mueven φ y Φ.
    const RECETA = { feb24: 15, mar24: 20, feb25: 10 };

    SIMULADORES['receta-mes'] = function (raiz) {
      const params = { phi: 0.6, Phi: 0.7 };
      const controles = raiz.querySelector('.simulador-controles');
      const cuadrado = raiz.querySelector('.receta-cuadrado');
      const lectura = raiz.querySelector('.simulador-lectura');

      function celda(valor, peso) {
        return `${valor}<br><small>× ${fmt(peso, 2)} = ${fmt(valor * peso, 2)}</small>`;
      }

      function modelo(phi, Phi) {
        if (phi === 0 && Phi === 0) return 'ruido blanco: se pronostica el promedio';
        if (Phi === 0) return 'AR(1) del Capítulo 3: sin satélite';
        if (phi === 0) return 'solo el mismo mes del año anterior: sin satélite';
        if (phi === 1 && Phi === 1) return '∇∇₁₂ del Módulo 3: pesos +1, +1 y −1';
        // Solo un factor que vale +1 es una diferencia: (1 − B) o (1 − B¹²).
        // Con −1 el factor es (1 + B) o (1 + B¹²), que tiene sus raíces sobre el
        // círculo unitario sin ser una diferencia.
        if (phi === 1 || Phi === 1) {
          return 'un factor vale 1: es una diferencia y el proceso ya no es estacionario';
        }
        if (phi === -1 || Phi === -1) {
          return 'un factor vale −1: no es una diferencia, pero su raíz cae sobre el círculo unitario y el proceso ya no es estacionario';
        }
        return 'SARIMA(1,0,0)(1,0,0)₁₂';
      }

      function pintar() {
        const { phi, Phi } = params;
        const { feb24, mar24, feb25 } = RECETA;
        const satelite = -phi * Phi + 0;   // + 0: sin él, φ = 0 se lee «-0.00»
        const directo = phi * feb25 + Phi * mar24 + satelite * feb24;
        // La ruta de las dos preguntas: primero la sorpresa regular de marzo
        // de 2024, después la estacional sobre esa sorpresa.
        const sorpresa = mar24 - phi * feb24;
        const esperada = Phi * sorpresa;
        const sumado = phi * feb25 + Phi * mar24;

        // Relleno de celda menor que el de `.diagram`: dentro del simulador, con
        // el de la caja y el de las celdas, a 375 px «Febrero» no cabía.
        const c = ' style="padding:0.45rem 0.4rem"';
        cuadrado.innerHTML = `<table style="width:100%"><thead><tr><th${c}></th><th${c}>Febrero</th>`
          + `<th${c}>Marzo</th></tr></thead><tbody>`
          + `<tr><td${c}>2024</td><td${c}>${celda(feb24, satelite)}</td><td${c}>${celda(mar24, Phi)}</td></tr>`
          + `<tr><td${c}>2025</td><td${c}>${celda(feb25, phi)}</td>`
          + `<td${c}><strong>${fmt(directo, 2)}</strong><br><small>pronóstico</small></td></tr>`
          + '</tbody></table>';

        actualizarLectura(lectura, [
          { etiqueta: 'pronóstico', valor: fmt(directo, 2) },
          {
            etiqueta: 'por sorpresas',
            valor: `${fmt(sorpresa, 2)} → ${fmt(esperada, 2)} → ${fmt(phi * feb25 + esperada, 2)}`
          },
          { etiqueta: 'peso del rezago 13', valor: fmt(satelite, 2) },
          { etiqueta: 'si se sumaran', valor: fmt(sumado, 2) },
          { etiqueta: 'modelo', valor: modelo(phi, Phi) }
        ]);
      }

      crearControles(controles, [
        { clave: 'phi', etiqueta: 'φ (regular)', min: -1, max: 1, paso: 0.1, decimales: 1 },
        { clave: 'Phi', etiqueta: 'Φ (estacional)', min: -1, max: 1, paso: 0.1, decimales: 1 }
      ], params, pintar);

      pintar();
      return [];
    };

    // ================================================================
    // Módulo 2 · Constructor de polinomios SARIMA
    // ================================================================
    SIMULADORES['constructor-polinomio'] = function (raiz) {
      const params = { p: 1, d: 1, q: 1, P: 1, D: 1, Q: 1 };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelector('canvas');
      const ALTOS = { estrecho: '260px', ancho: '250px' };
      // Con p = d = P = D = 0 el polinomio AR es 1 y no hay barras que dibujar:
      // el lienzo quedaba en blanco, sin ejes ni explicación.
      const vacio = document.createElement('p');
      vacio.className = 'grafico-etiqueta';
      vacio.hidden = true;
      canvas.parentNode.insertAdjacentElement('afterend', vacio);
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
        const nulo = v => Math.abs(v) <= 1e-12;
        if (grafico) grafico.destroy();
        grafico = barrasCompactas(crearGraficoBarras(canvas, etiquetas,
          // Los ceros exactos no llevan barra, y las demás miden al menos 3 px:
          // con todos los órdenes en 2 la escala llega a ±10 y los coeficientes
          // pequeños de los rezagos 37–52 no se veían (la lectura contaba 24
          // no nulos y el dibujo enseñaba unos 14).
          coefs.map(v => (nulo(v) ? null : v)), {
            etiqueta: 'Coeficiente del rezago',
            tituloX: 'Rezago',
            min: Math.min(-1.2, ...coefs) - 0.1,
            max: Math.max(1.2, ...coefs) + 0.1
          }), ALTOS);
        grafico.data.datasets[0].minBarLength = 3;
        grafico.update('none');

        const libres = params.p + params.q + params.P + params.Q;
        const rezagoMax = coefs.length;
        const noNulos = coefs.filter(v => !nulo(v)).length;
        const perdidas = params.d + params.D * M_EST;
        const modelo = `(${params.p},${params.d},${params.q})(${params.P},${params.D},${params.Q})₁₂`;
        vacio.hidden = rezagoMax > 0;
        vacio.textContent = rezagoMax > 0 ? '' :
          'Con p = d = P = D = 0 el polinomio autorregresivo es 1: no toca ningún rezago y no hay barras que dibujar.';
        if (rezagoMax === 0) {
          ariaLienzo(canvas, `Polinomio autorregresivo del SARIMA${modelo}: vale 1, sin ningún rezago`);
        } else {
          const iMax = coefs.reduce((m, v, i) => (Math.abs(v) > Math.abs(coefs[m]) ? i : m), 0);
          const cuales = coefs.map((v, i) => (nulo(v) ? 0 : i + 1)).filter(k => k);
          ariaLienzo(canvas, `Coeficientes del polinomio autorregresivo completo del SARIMA${modelo}, ` +
            `rezagos 1 a ${rezagoMax}: ${noNulos} no nulos` +
            (noNulos <= 12 ? ` (rezagos ${cuales.join(', ')})` : '') +
            `; el mayor en valor absoluto, ${cifra(coefs[iMax], 2)}, en el rezago ${iMax + 1}`);
        }
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
    // Módulo 3 · La tienda inventada: cada diferencia, celda a celda
    // ================================================================
    // Serie construida, no medida: 100 unidades al empezar, una más cada mes y
    // un patrón anual que suma cero. En el escenario «acelera», desde enero de
    // 2024 crece tres unidades al mes. Todo son enteros a propósito, para que
    // cada celda se compruebe de cabeza; el bloque de R del módulo imprime las
    // mismas cuadrículas.
    const PATRON_TIENDA = [-6, -8, -4, -2, 0, 4, 6, 4, 0, -2, 2, 6];

    function tendenciaTienda(t, acelera) {
      return acelera && t > 24 ? 23 + 3 * (t - 24) : t - 1;
    }

    SIMULADORES['tienda-cuadricula'] = function (raiz) {
      const params = { escenario: 'fijo', resta: 'ninguna' };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const mapa = raiz.querySelector('.mapa-estacional');

      const ESCENARIOS = {
        fijo: 'Crece una unidad al mes',
        acelera: 'Desde 2024 crece tres al mes'
      };
      const RESTAS = {
        ninguna: { texto: 'Nada: la serie tal cual', d: 0, D: 0 },
        d1: { texto: '∇: la celda de la izquierda', d: 1, D: 0 },
        D1: { texto: '∇₁₂: la celda de arriba', d: 0, D: 1 },
        d1D1: { texto: '∇∇₁₂: las dos', d: 1, D: 1 }
      };
      // Marzo de 2024 (t = 27) es la celda de la cuenta de ejemplo. Cae en el
      // año en que la tienda acelera, así que la cuenta cambia con el escenario.
      const T_EJEMPLO = 27;

      function pintar() {
        const acelera = params.escenario === 'acelera';
        const serie = [];
        for (let t = 1; t <= 48; t++) {
          serie.push(100 + tendenciaTienda(t, acelera) + PATRON_TIENDA[(t - 1) % 12]);
        }
        const r = RESTAS[params.resta];
        // Primero la estacional, después la regular, como en el Módulo 1; el
        // resultado es el mismo en cualquier orden, no así el mes de arranque.
        let y = serie.slice();
        if (r.D > 0) y = diferenciarEstacional(y, r.D);
        if (r.d > 0) y = diferenciar(y, r.d);

        const perdidas = serie.length - y.length;
        let anio = 2022, mes = 1 + perdidas;
        anio += Math.floor((mes - 1) / 12); mes = ((mes - 1) % 12) + 1;
        const diferenciada = r.d + r.D > 0;
        pintarMapaEstacional(mapa, Object.assign(matrizMesAnio(y, anio, mes), {
          escala: diferenciada ? 'divergente' : 'secuencial',
          decimales: 0,
          unidad: '',
          descripcion: `La tienda inventada (${ESCENARIOS[params.escenario].toLowerCase()}), mes × año; ` +
            `se resta ${r.texto.charAt(0).toLowerCase() + r.texto.slice(1)}`,
          nota: `<strong>Tienda inventada</strong> · ${ESCENARIOS[params.escenario]} · ${r.texto}. ` +
            (diferenciada
              ? 'Escala divergente centrada en cero: naranja por debajo, verde por encima.'
              : 'Escala secuencial: cuanto más oscuro, más alto.')
        }));

        // La cuenta se hace con los números de la serie sin diferenciar:
        // v(0) es marzo de 2024, v(1) febrero de 2024, v(12) marzo de 2023.
        const v = k => serie[T_EJEMPLO - 1 - k];
        const p = PATRON_TIENDA[2];
        const cuentas = {
          ninguna: `100 + ${tendenciaTienda(T_EJEMPLO, acelera)} ${p < 0 ? '−' : '+'} ${Math.abs(p)} = ${v(0)}`,
          d1: `${v(0)} − ${v(1)} = ${v(0) - v(1)}`,
          D1: `${v(0)} − ${v(12)} = ${v(0) - v(12)}`,
          d1D1: `${v(0)} − ${v(1)} − ${v(12)} + ${v(13)} = ${v(0) - v(1) - v(12) + v(13)}`
        };
        const distintos = [...new Set(y)].sort((a, b) => a - b);
        actualizarLectura(lectura, [
          { etiqueta: 'marzo de 2024', valor: cuentas[params.resta] },
          { etiqueta: 'celdas', valor: y.length },
          {
            etiqueta: 'valores distintos',
            valor: distintos.length <= 3 ? `${distintos.length} (${distintos.join(', ')})` : distintos.length
          }
        ]);
      }

      crearSelector(controles, {
        clave: 'escenario', etiqueta: 'La tienda',
        opciones: Object.keys(ESCENARIOS).map(k => ({ valor: k, texto: ESCENARIOS[k] }))
      }, params, pintar);
      crearSelector(controles, {
        clave: 'resta', etiqueta: 'Qué se resta',
        opciones: Object.keys(RESTAS).map(k => ({ valor: k, texto: RESTAS[k].texto }))
      }, params, pintar);

      pintar();
      return [];
    };

    // ================================================================
    // Módulo 3 · Las cuatro combinaciones (d, D)
    // ================================================================
    SIMULADORES['cuatro-combinaciones'] = function (raiz) {
      const params = { regular: true, estacional: true };
      const controles = raiz.querySelector('.simulador-controles');
      const lectura = raiz.querySelector('.simulador-lectura');
      const canvas = raiz.querySelectorAll('canvas');
      const ALTOS_SERIE = { estrecho: '240px', ancho: '240px' };
      const ALTOS_ACF = { estrecho: '260px', ancho: '250px' };
      let serie = null, correlograma = null;

      function pintar() {
        const clave = `d${params.regular ? 1 : 0}_D${params.estacional ? 1 : 0}`;
        const c = AP.combinaciones[clave];
        if (serie) serie.destroy();
        serie = lineaCompacta(lineaSimple(canvas[0], c.fechas, c.valores, c.etiqueta,
          COLORES_GRAFICO.primario, { plugins: { legend: { display: true } } }), ALTOS_SERIE);

        if (correlograma) correlograma.destroy();
        correlograma = barrasCompactas(crearGraficoBarras(canvas[1], REZAGOS, c.acf, {
          etiqueta: 'ACF muestral',
          lineas: lineasBanda(c.n),
          tituloX: 'Rezago'
        }), ALTOS_ACF);

        // Lo que se dibuja, con su operador: la etiqueta de los datos («Ambas
        // diferencias») no dice de qué serie ni con qué diferencias.
        const nombre = (c.d ? '∇ ' : '') + (c.D ? '∇₁₂ ' : '') + 'log(AirPassengers)';
        const [lo, hi] = rangoDe(c.valores);
        ariaLienzo(canvas[0], `Serie ${nombre}, de ${c.fechas[0]} a ${c.fechas[c.fechas.length - 1]} ` +
          `(n = ${c.n}): valores entre ${cifra(lo, 3)} y ${cifra(hi, 3)}`);
        ariaLienzo(canvas[1], descripcionCorrelograma('ACF muestral', nombre, c.acf, banda(c.n)));

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
      const ALTOS = { estrecho: '240px', ancho: '240px' };
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

        // El exponente como en la prosa: ∇₁₂² y no «∇₁₂^2»; con D = 0 no hay ∇₁₂.
        const nombre = ['∇ log(AirPassengers)', '∇ ∇₁₂ log(AirPassengers)', '∇ ∇₁₂² log(AirPassengers)'][D];
        if (grafico) grafico.destroy();
        grafico = lineaCompacta(lineaSimple(canvas, etiquetas, y, nombre, COLORES_GRAFICO.primario,
          { plugins: { legend: { display: true } } }), ALTOS);
        const [lo, hi] = rangoDe(y);
        ariaLienzo(canvas, `Serie ${nombre}, de ${etiquetas[0]} a ${etiquetas[etiquetas.length - 1]} ` +
          `(n = ${y.length}): valores entre ${cifra(lo, 3)} y ${cifra(hi, 3)}`);

        // La firma se lee en la escala de Θ: −1 dentro de Θ̂ ± 1.96·e.e. No en
        // |raíz MA|⁻¹ = |Θ̂|^(1/12), que se acerca a 1 con casi cualquier Θ.
        const alarma = info.a_menos_1_en_ee < 1.96;
        actualizarLectura(lectura, [
          { etiqueta: 'D', valor: D },
          { etiqueta: 'n', valor: info.n },
          { etiqueta: 'Θ̂', valor: `${fmt(info.theta_est, 4)} (e.e. ${fmt(info.ee, 4)})` },
          { etiqueta: 'distancia a −1', valor: `${fmt(info.a_menos_1_en_ee, 2)} e.e.` },
          { etiqueta: 'diagnóstico', valor: alarma ? '⚠ −1 dentro de Θ̂ ± 1.96 e.e.: señal de que puede sobrar una diferencia estacional; vuelve a mirar D'
            : (D === 0 ? 'Θ̂ lejos de −1: no sobra nada, pero falta ∇₁₂ (la estacionalidad sigue en la serie)'
                       : 'Θ̂ lejos de −1: ninguna señal de diferencia de más') }
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
      const ALTOS = { estrecho: '260px', ancho: '250px' };
      let gAcf = null, gPacf = null;

      // Lo que dibuja un correlograma teórico, para su `aria-label`: los
      // valores de los rezagos que la intro manda mirar y cuántos no son cero
      // a la vista (|valor| ≥ 0.05).
      function describeTeorica(tipo, v) {
        const rezagos = [1, 11, 12, 13, 24, 36];
        const visibles = v.filter(r => Math.abs(r) >= 0.05).length;
        return `${tipo} del modelo con φ₁ = ${cifra(params.phi, 2)}, θ₁ = ${cifra(params.theta, 2)}, ` +
          `Φ₁ = ${cifra(params.Phi, 2)} y Θ₁ = ${cifra(params.Theta, 2)}, rezagos 1 a ${v.length}: ` +
          rezagos.map(k => `rezago ${k}, ${cifra(v[k - 1], 3)}`).join('; ') +
          `; ${visibles} de ${v.length} barras miden 0.05 o más en valor absoluto`;
      }

      function pintar() {
        const polAr = multPoli([1, -params.phi], poliEstacional(-params.Phi));
        const polMa = multPoli([1, params.theta], poliEstacional(params.Theta));
        const ar = recortaCeros(polAr.slice(1).map(v => -v));
        const ma = recortaCeros(polMa.slice(1));
        const psi = pesosPsi(ar, ma, 1500);
        const acf = acfDesdePsi(psi, DATOS_CAP5.max_rezago);
        const pacf = calcularPACF(acf, DATOS_CAP5.max_rezago);

        if (gAcf) gAcf.destroy();
        gAcf = barrasCompactas(crearGraficoBarras(canvas[0], REZAGOS, acf,
          { etiqueta: 'ACF teórica', tituloX: 'Rezago' }), ALTOS);
        if (gPacf) gPacf.destroy();
        gPacf = barrasCompactas(crearGraficoBarras(canvas[1], REZAGOS, pacf,
          { etiqueta: 'PACF teórica', color: COLORES_GRAFICO.secundario, tituloX: 'Rezago' }), ALTOS);
        ariaLienzo(canvas[0], describeTeorica('ACF teórica', acf));
        ariaLienzo(canvas[1], describeTeorica('PACF teórica', pacf));

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
      const ALTOS_PSI = { estrecho: '260px', ancho: '250px' };
      const ALTOS_SIGMA = { estrecho: '250px', ancho: '240px' };
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
        gPsi = barrasCompactas(crearGraficoBarras(canvas[0], etiquetas, psi.slice(0, H), {
          etiqueta: 'ψⱼ', tituloX: 'j', min: -0.2, max: 1.4
        }), ALTOS_PSI);
        if (gSigma) gSigma.destroy();
        // El eje de σₕ arranca en 0: reescalado a su propio rango, con
        // θ = Θ = −0.95 (σₕ de 0.0370 a 0.0390) se dibujaba como una rampa tan
        // empinada como la del estado inicial, y el «se aplanan» no se veía.
        gSigma = lineaCompacta(lineaSimple(canvas[1], Array.from({ length: H }, (_, i) => String(i + 1)),
          sigmaH, 'σₕ', COLORES_GRAFICO.secundario,
          { plugins: { legend: { display: true } },
            scales: escalasLinea('', {}, { min: 0 }) }), ALTOS_SIGMA);
        ariaLienzo(canvas[0], `Pesos ψ₀ a ψ${sub(H - 1)} del airline con θ = ${cifra(params.theta, 2)} y ` +
          `Θ = ${cifra(params.Theta, 2)}: ψ₁ = ${cifra(psi[1], 3)}, ψ₁₁ = ${cifra(psi[11], 3)}, ` +
          `ψ₁₂ = ${cifra(psi[12], 3)} (salto de ${cifra(psi[12] - psi[11], 3)}), ψ₂₄ = ${cifra(psi[24], 3)} ` +
          `y ψ${sub(H - 1)} = ${cifra(psi[H - 1], 3)}`);
        ariaLienzo(canvas[1], `Desviación del error de pronóstico σₕ, de h = 1 a ${H}, sobre el logaritmo, ` +
          `con el eje desde 0: σ₁ = ${cifra(sigmaH[0], 4)}, σ₁₂ = ${cifra(sigmaH[11], 4)}, ` +
          `σ₂₄ = ${cifra(sigmaH[23], 4)} y σ${sub(H)} = ${cifra(sigmaH[H - 1], 4)}`);

        actualizarLectura(lectura, [
          { etiqueta: 'ψ₁ = 1+θ', valor: fmt(psi[1], 4) },
          { etiqueta: 'ψ₁₂', valor: fmt(psi[12], 4) },
          { etiqueta: 'ψ₁₃', valor: fmt(psi[13], 4) },
          { etiqueta: 'salto ψ₁₂ − ψ₁₁ = 1+Θ', valor: fmt(psi[12] - psi[11], 4) },
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
      const ALTOS = { estrecho: '260px', ancho: '250px' };
      let grafico = null;

      function pintar() {
        const clave = `(${params.p},1,${params.q})(${params.P},1,${params.Q})[12]`;
        const m = AP.rejilla[clave];
        if (!m) {
          actualizarLectura(lectura, [{ etiqueta: 'modelo', valor: clave + ' — no convergió' }]);
          return;
        }
        if (grafico) grafico.destroy();
        grafico = barrasCompactas(crearGraficoBarras(canvas, REZAGOS24, m.acf, {
          etiqueta: 'ACF de los residuales',
          lineas: lineasBanda(144),
          tituloX: 'Rezago'
        }), ALTOS);
        ariaLienzo(canvas, descripcionCorrelograma('ACF', 'los residuales del SARIMA' +
          clave.replace('[12]', '₁₂'), m.acf, banda(144)));

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
      const ALTOS = { estrecho: '300px', ancho: '280px' };
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
        grafico = lineaCompacta(crearGraficoLinea(canvas, etiquetas, [
          { label: 'Observado', data: serie, borderColor: COLORES_GRAFICO.primario, borderWidth: 1.8, pointRadius: 0 },
          { label: 'IC 95 %', data: datos('hi95'), borderColor: 'rgba(255,102,0,0.25)', backgroundColor: 'rgba(255,102,0,0.12)', borderWidth: 1, pointRadius: 0, fill: '+1' },
          { label: '', data: datos('lo95'), borderColor: 'rgba(255,102,0,0.25)', borderWidth: 1, pointRadius: 0, fill: false },
          { label: 'IC 80 %', data: datos('hi80'), borderColor: 'rgba(255,102,0,0.45)', backgroundColor: 'rgba(255,102,0,0.22)', borderWidth: 1, pointRadius: 0, fill: '+1' },
          { label: '', data: datos('lo80'), borderColor: 'rgba(255,102,0,0.45)', borderWidth: 1, pointRadius: 0, fill: false },
          { label: 'Pronóstico', data: datos('media'), borderColor: COLORES_GRAFICO.secundario, borderWidth: 2, pointRadius: 0, borderDash: [6, 3] }
          // Los bordes inferiores de las bandas no llevan rótulo: sin el filtro,
          // la leyenda los pintaba como dos recuadros vacíos.
        ], { plugins: { legend: { display: true, labels: { filter: it => !!(it.text && it.text.trim()) } } } }), ALTOS);

        const i = h - 1;
        const dd = params.original ? 2 : 4;
        ariaLienzo(canvas, `Últimos 48 meses de ${params.original ? 'AirPassengers' : 'log(AirPassengers)'} ` +
          `(${etiquetasHist[0]} a ${etiquetasHist[etiquetasHist.length - 1]}) y pronóstico del airline a ${h} ` +
          `${h === 1 ? 'mes' : 'meses'}, hasta ${pron.fechas[i]}, con bandas del 80 y del 95 %: en ${pron.fechas[i]}, ` +
          `${cifra(esc.media[i], dd)}, con IC 95 % de ${cifra(esc.lo95[i], dd)} a ${cifra(esc.hi95[i], dd)}`);
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
      const ALTOS = { estrecho: '260px', ancho: '250px' };

      function pintar() {
        const c = CASOS[params.serie];
        if (grafico) grafico.destroy();
        grafico = barrasCompactas(crearGraficoBarras(canvas, REZAGOS, c.acf, {
          etiqueta: 'ACF de la serie diferenciada',
          color: params.serie === 'ap' ? COLORES_GRAFICO.primario : COLORES_GRAFICO.terciario,
          lineas: lineasBanda(c.n),
          tituloX: 'Rezago'
        }), ALTOS);
        const b = banda(c.n);
        ariaLienzo(canvas, descripcionCorrelograma('ACF muestral', c.texto, c.acf, b));
        // El renglón dice qué mira: los múltiplos de 12. Los demás rezagos que
        // salen de la banda van en su propio renglón.
        const fuera = fueraDeBanda(c.acf, b);
        actualizarLectura(lectura, [
          { etiqueta: 'serie', valor: c.texto },
          { etiqueta: 'n', valor: c.n },
          { etiqueta: 'ρ̂₁₂', valor: fmt(c.acf[11], 4) },
          { etiqueta: 'ρ̂₂₄', valor: fmt(c.acf[23], 4) },
          { etiqueta: 'ρ̂₃₆', valor: fmt(c.acf[35], 4) },
          { etiqueta: 'banda', valor: '±' + fmt(b, 4) },
          { etiqueta: 'múltiplos de 12 fuera de banda', valor: fuera.estacionales.length ? fuera.estacionales.join(', ') : 'ninguno' },
          { etiqueta: 'otros rezagos fuera de banda', valor: fuera.otros.length ? fuera.otros.join(', ') : 'ninguno' },
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
      // Años con el Domingo de Pascua en marzo, contados desde las fechas.
      const anios = Object.keys(cal.pascuas);
      const pascuaMarzo = anios.filter(a => cal.pascuas[a].slice(5, 7) === '03').length;
      const ALTOS = { estrecho: '290px', ancho: '260px' };
      let grafico = null;

      function pintar() {
        // Cada combinación de interruptores lee su propio ajuste de R: la Semana
        // Santa sola también está precalculada (con_pascua).
        const clave = params.dias && params.pascua ? 'con_dias_pascua'
          : params.dias ? 'con_dias'
            : params.pascua ? 'con_pascua' : 'sin_regresores';
        const m = cal.modelos[clave];

        const datasets = [{
          label: 'log(AirPassengers)',
          data: AP.log, borderColor: COLORES_GRAFICO.gris,
          borderWidth: 1.2, pointRadius: 0, yAxisID: 'y'
        }];
        if (params.dias) datasets.push({
          label: 'Días del mes (eje derecho)', data: cal.dias_mes,
          borderColor: COLORES_GRAFICO.primario, borderWidth: 1.6,
          pointRadius: 0, yAxisID: 'y2'
        });
        // Los meses con Pascua se marcan SOBRE la serie, en su valor: antes se
        // dibujaban en el «31» del eje de días, y un abril con Pascua parecía
        // un mes de 31 días.
        if (params.pascua) datasets.push({
          label: 'Mes con Domingo de Pascua', data: esPascua.map((v, i) => v ? AP.log[i] : null),
          borderColor: COLORES_GRAFICO.secundario, backgroundColor: COLORES_GRAFICO.secundario,
          borderWidth: 0, pointRadius: 3.5, showLine: false, clip: false, yAxisID: 'y'
        });

        // Escalas propias (hay un segundo eje), pero con los ayudantes del
        // armazón: sin ellos el eje x rotulaba «1949-01, 1951-06…» y se pisaba a
        // 800 y 375 px.
        // Títulos de eje cortos, a todo ancho: con los largos, en un marco
        // estrecho quedaban 132 px de área para 144 meses. La leyenda dice
        // además qué serie va en el eje derecho.
        const escalas = escalasLinea('log', {}, { position: 'left' });
        escalas.y2 = {
          display: params.dias, position: 'right', min: 26, max: 33,
          title: { display: true, text: 'días', font: { family: 'Montserrat', size: 11 } },
          ticks: { font: { family: 'Fira Code', size: 11 }, stepSize: 1 },
          grid: { display: false }
        };
        if (grafico) grafico.destroy();
        grafico = lineaCompacta(crearGraficoLinea(canvas, cal.fechas, datasets, {
          plugins: { legend: { display: true } },
          scales: escalas
        }), ALTOS);
        const [lo, hi] = rangoDe(AP.log);
        const [dMin, dMax] = rangoDe(cal.dias_mes);
        ariaLienzo(canvas, `log(AirPassengers) de ${cal.fechas[0]} a ${cal.fechas[cal.fechas.length - 1]}, ` +
          `entre ${cifra(lo, 2)} y ${cifra(hi, 2)}` +
          (params.dias ? `, con los días de cada mes (de ${dMin} a ${dMax}) en el eje derecho` : '') +
          (params.pascua ? `, y los ${esPascua.reduce((a, v) => a + v, 0)} meses con Domingo de Pascua marcados sobre la serie` : '') +
          (!params.dias && !params.pascua ? ', sin ningún regresor activo' : ''));

        const campos = [
          { etiqueta: 'modelo', valor: m.nombre },
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
        campos.push({ etiqueta: 'años con Pascua en marzo', valor: `${pascuaMarzo} de ${anios.length}` });
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
      const ALTOS = { estrecho: '260px', ancho: '240px' };
      let grafico = null;

      function pintar() {
        const K = Math.round(params.K);
        const curva = fou.curvas[K - 1];
        const r = fou.resultados[K - 1];
        // Solo los dos primeros ciclos: la curva es periódica y así se ve la forma.
        const n = 24;
        if (grafico) grafico.destroy();
        grafico = lineaCompacta(crearGraficoLinea(canvas, AP.fechas.slice(0, n), [
          { label: `K = ${K} (${r.n_terminos} términos)`, data: curva.slice(0, n),
            borderColor: COLORES_GRAFICO.secundario, borderWidth: 2, pointRadius: 0 },
          { label: 'K = 6 (saturado)', data: fou.curvas[5].slice(0, n),
            borderColor: COLORES_GRAFICO.gris, borderWidth: 1.2, pointRadius: 0, borderDash: [4, 3] }
        ], { plugins: { legend: { display: true } } }), ALTOS);
        const [lo, hi] = rangoDe(curva.slice(0, n));
        const [lo6, hi6] = rangoDe(fou.curvas[5].slice(0, n));
        ariaLienzo(canvas, `Componente estacional con K = ${K} (${r.n_terminos} términos de Fourier), ` +
          `de ${AP.fechas[0]} a ${AP.fechas[n - 1]}: entre ${cifra(lo, 3)} y ${cifra(hi, 3)}; ` +
          `la de K = ${fou.resultados[5].K}, de referencia, entre ${cifra(lo6, 3)} y ${cifra(hi6, 3)}`);

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
      // Ocho colores de tono distinto y cuatro trazos que se alternan: con los
      // ocho encendidos había dos verdes azulados, dos violetas y dos ocres con
      // la misma raya discontinua, y no se sabía qué línea era cuál.
      const COLORES = [COLORES_GRAFICO.secundario, '#1d4ed8', '#7c3aed', '#be123c',
                       '#0f766e', '#a16207', '#db2777', '#475569'];
      const TRAZOS = [[6, 3], [], [2, 3], [9, 3, 2, 3]];
      // Rótulo de la leyenda: el método sin la especificación que sigue a «:»
      // y sin los errores de la armónica. En el teléfono, una forma corta para
      // que las nueve entradas quepan sin que Chart.js las corte.
      const CORTOS = { ets_log: 'ETS (log)', stl_arima: 'STL + ARIMA', sarima: 'SARIMA',
                       auto_arima: 'auto.arima', sarima_calendario: 'SARIMA + cal.',
                       ets: 'ETS (cruda)', snaive: 'Naive est.' };
      const metodo = k => comp.modelos[k].nombre.split(':')[0].replace(/ \+ errores ARIMA$/, '');
      const corto = k => CORTOS[k] || ('Armónica ' + (comp.modelos[k].nombre.match(/K = \d+/) || [''])[0]).trim();
      // Dos métodos con el mismo pronóstico se tapan: la leyenda lo dice.
      const igualA = k => claves.find(o => o !== k && claves.indexOf(o) < claves.indexOf(k) &&
        comp.modelos[o].pronostico.every((v, j) => v === comp.modelos[k].pronostico[j]));
      const ALTOS = { estrecho: '400px', ancho: '320px' };
      let grafico = null;

      function pintar() {
        const estrecho = canvas.parentNode.clientWidth < ESTRECHO;
        const datasets = [{
          label: 'Observado', data: comp.observado,
          borderColor: COLORES_GRAFICO.primario, borderWidth: 2.4, pointRadius: 0
        }];
        claves.forEach((k, i) => {
          if (!params['m_' + k]) return;
          const gemelo = igualA(k);
          datasets.push({
            label: (estrecho ? corto(k) : metodo(k)) +
              (gemelo ? ` (= ${estrecho ? corto(gemelo) : metodo(gemelo)})` : ''),
            data: comp.modelos[k].pronostico,
            borderColor: COLORES[i % COLORES.length],
            // El gemelo va más grueso y punteado, para asomar bajo el otro.
            borderWidth: gemelo ? 3 : 1.6, pointRadius: 0,
            borderDash: gemelo ? [1, 4] : TRAZOS[i % TRAZOS.length]
          });
        });

        if (grafico) grafico.destroy();
        grafico = lineaCompacta(crearGraficoLinea(canvas, comp.fechas_prueba, datasets,
          { plugins: { legend: { display: true } } }), ALTOS);
        const encendidos = claves.filter(k => params['m_' + k]);
        ariaLienzo(canvas, `Observado frente a los pronósticos sobre los ${comp.n_prueba} meses de prueba ` +
          `(${comp.fechas_prueba[0]} a ${comp.fechas_prueba[comp.fechas_prueba.length - 1]}), entrenando hasta ` +
          `${comp.corte}: ` + (encendidos.length
            ? `${encendidos.length} ${encendidos.length === 1 ? 'método' : 'métodos'}, ` + encendidos.map(metodo).join(', ')
            : 'ningún método encendido'));

        const met = params.metrica;
        const orden = claves.slice().sort((a, b) => comp.modelos[a][met] - comp.modelos[b][met]);
        const campos = [
          { etiqueta: 'entrena hasta', valor: comp.corte + ` (n = ${comp.n_entrenamiento})` },
          { etiqueta: 'prueba', valor: comp.n_prueba + ' meses' }
        ];
        orden.forEach((k, i) => campos.push({
          etiqueta: `${i + 1}. ${comp.modelos[k].nombre}`,
          valor: fmt(comp.modelos[k][met], 3) + (met === 'mape' ? '\u00a0%' : '') + (k === 'sarima' ? '  ← el SARIMA' : '')
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
        claves.map(k => ({ clave: 'm_' + k, etiqueta: comp.modelos[k].nombre })),
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
        descripcion: 'Los ocho métodos sobre los últimos ' + AP.comparativa.n_prueba +
          ' meses, una sola partición. Pulsa las cabeceras: por RMSE gana el ETS sobre el ' +
          'logaritmo y por MAE y MAPE la regresión armónica, pero las tres dejan al SARIMA cuarto.',
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
        formato: fmt,
        inicial: 'rmse',
        pie: 'Las tres métricas coinciden en el cuarto puesto y aun así es engañoso: sobre ' +
          '61 orígenes, midiendo los 12 meses siguientes a cada corte, el SARIMA pasa a primero. ' +
          'El Capítulo 6 construye esa evaluación.'
      };
    };

    // ACF teórica del gráfico de la pregunta 5 del quiz (un SAR(1) de periodo 12).
    function acfQuiz() {
      const ar = new Array(12).fill(0); ar[11] = 0.7;
      return acfDesdePsi(pesosPsi(ar, [], 1500), 36);
    }

    AUTOEVALUACIONES['cap5'] = [
      {
        tipo: 'opcion',
        modulo: 1,
        pregunta: 'La TRM mensual en niveles tiene $\\hat\\rho_{12} = 0.636$, muy por encima de su banda de $0.167$. ¿Qué se concluye?',
        pista: 'Fíjate en qué vale $\\hat\\rho_1$ en esa misma serie, y en qué le pasa a la ACF de cualquier serie con tendencia.',
        opciones: [
          {
            texto: 'Que la TRM tiene estacionalidad anual, porque $0.636$ supera claramente la banda.',
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
          },
          {
            texto: 'Nada todavía: en niveles la tendencia infla <em>todos</em> los $\\hat\\rho_k$, así que el diagnóstico hay que hacerlo sobre la serie ya diferenciada.',
            correcta: true,
            retro: 'En esa misma serie $\\hat\\rho_1 = 0.964$ y $\\hat\\rho_{36} = 0.225$: es el decaimiento lento típico de una tendencia, no un pico estacional. Sobre $\\nabla$TRM los tres múltiplos de $12$ valen $-0.0025$, $-0.067$ y $0.071$, todos dentro de la banda.'
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
            retro: 'Son $\\phi$ y $\\Phi$. El coeficiente del rezago $13$ es su producto, no un tercer parámetro.'
          },
          {
            texto: 'Su ACF teórica es cero en los rezagos $2$ a $11$.',
            correcta: false,
            retro: 'No: con $\\phi = 0.6$ y $\\Phi = 0.7$, $\\rho_2 = \\rho_1^2 \\approx 0.36$ y así sucesivamente. La parte AR regular llena los rezagos bajos con una geométrica. Los rezagos intermedios sí son cero cuando <strong>solo</strong> hay parte estacional ($\\phi = 0$).'
          },
          {
            texto: 'Escrito como AR no estacional, es un AR($13$).',
            correcta: true,
            retro: 'El polinomio completo tiene grado $13$, con solo tres coeficientes no nulos ($1$, $12$ y $13$).'
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
        retroAcierto: '$96 - d - D\\,m = 96 - 1 - 12 = 83$. Ese es el $n$ efectivo con el que se evalúa la verosimilitud, y por eso el AICc de un modelo con $D=1$ no se puede comparar con el de uno con $D=0$, que tendría $95$.',
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
            retro: 'Los <em>operadores</em> conmutan —la serie $\\nabla\\nabla_{12}y$ es idéntica en cualquier orden, diferencia máxima medida $0$—, pero las <em>pruebas</em> no: aplicadas a la serie cruda, la varianza estacional impide ver la raíz unitaria regular. En Python pasa igual: KPSS sobre $\\nabla_{12}y$ da $0.8672$ y rechaza.'
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
        alto: 250,
        // Lo que se ve, no lo que hay que deducir: los valores de las barras,
        // calculados igual que el dibujo.
        descripcionGrafico: (function () {
          const acf = acfQuiz();
          const picos = acf.map((v, i) => (Math.abs(v) >= 0.005 ? i + 1 : 0)).filter(k => k);
          return 'Función de autocorrelación teórica, rezagos 1 a ' + acf.length + ': ' +
            picos.map(k => `rezago ${k}, ${cifra(acf[k - 1], 2)}`).join('; ') +
            `; los otros ${acf.length - picos.length} rezagos valen 0.00.`;
        })(),
        dibujar: function (canvas) {
          return crearGraficoBarras(canvas, etiquetasRezago(36), acfQuiz(), {
            etiqueta: 'ACF teórica', tituloX: 'Rezago'
          });
        },
        opciones: [
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
            texto: 'Un SAR($1$)$_{12}$ con $\\Phi > 0$: los picos decaen geométricamente ($0.70$, $0.49$, $0.34$).',
            correcta: true,
            retro: 'Los tres picos son $\\Phi$, $\\Phi^2$ y $\\Phi^3$ con $\\Phi = 0.7$, y todos los rezagos intermedios valen exactamente cero porque no hay parte regular. La PACF de este proceso se cortaría tras el rezago $12$.'
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
            texto: 'La armónica, que gana por $38$ puntos de AICc, que es una diferencia enorme.',
            correcta: false,
            retro: 'La diferencia es enorme precisamente porque los dos números no viven en la misma escala: doce observaciones menos cambian la log-verosimilitud mucho más que cualquier parámetro. Comparar esos AICc es el error que el módulo señala.'
          },
          {
            texto: 'Ninguno con esa información: los AICc no son comparables porque se calculan sobre $143$ y $131$ observaciones.',
            correcta: true,
            retro: 'Es la lección central del Módulo 10: la misma trampa que el Capítulo 4 documentó con $d$, agravada porque cada $D$ cuesta $m = 12$ observaciones en vez de una. Entre familias solo se puede comparar fuera de muestra.'
          },
          {
            texto: 'El <em>airline</em>, porque tiene $2$ parámetros frente a $15$ y la parsimonia desempata.',
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
        pregunta: 'Sobre los últimos $24$ meses el SARIMA queda cuarto (RMSE $43.18$) y la regresión armónica, segunda por RMSE ($19.51$, a $0.08$ del ETS sobre el logaritmo), es la primera por MAE y por MAPE. Sobre $61$ orígenes el SARIMA es primero ($16.81$) y la armónica cuarta ($22.38$). ¿Qué explica esto?',
        pista: 'Pregúntate cuántos números independientes hay realmente detrás de cada una de las dos comparaciones.',
        opciones: [
          {
            texto: 'Una sola partición mide el comportamiento en <em>un</em> tramo concreto; con $24$ puntos, qué tramo toque pesa más que la diferencia entre métodos.',
            correcta: true,
            retro: 'El corte cae justo detrás de 1958, el único año en que el tráfico casi no creció: el SARIMA ajusta su pendiente a ese frenazo y se queda corto en 1959–1960, y la armónica lo arrastra menos. Promediando sobre $61$ orígenes el efecto del tramo se diluye y el SARIMA le gana a cada rival en más del $85\\,\\%$ de ellos. Construir esa evaluación es el contenido del Capítulo 6.'
          },
          {
            texto: 'Que el RMSE no sirve para comparar métodos y hay que usar MAPE.',
            correcta: false,
            retro: 'Con cualquiera de las tres métricas de la tabla —RMSE, MAE o MAPE— el SARIMA queda cuarto en la partición única; solo cambia quién va primero: el ETS sobre el logaritmo por RMSE y la armónica por MAE y por MAPE. El problema no es la métrica sino el número de particiones sobre las que se calcula.'
          },
          {
            texto: 'Que el SARIMA está mal especificado y por eso falla en la partición corta.',
            correcta: false,
            retro: 'El SARIMA pasa todos los diagnósticos (Ljung–Box $0.2330$, Shapiro $0.1674$, raíces invertibles) y es el mínimo de AICc y de BIC dentro de su familia. Un modelo bien especificado también puede quedar mal en un tramo concreto: el sesgo que el Módulo 11 mide en esos $24$ meses es del tramo, no de la especificación.'
          },
          {
            texto: 'Que los $61$ orígenes se solapan entre sí, así que ese resultado no vale.',
            correcta: false,
            retro: 'Es cierto que las ventanas se solapan y que por eso los $61$ errores no son independientes —conviene saberlo al poner barras de error—. Pero eso afecta a la <em>precisión</em> de la estimación, no la invalida: una diferencia de $16.81$ frente a $22.38$ con victoria en el $90\\,\\%$ de los orígenes no se explica por el solape.'
          }
        ]
      }
    ];
