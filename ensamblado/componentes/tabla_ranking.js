
    // ================================================================
    // Componente .tabla-ranking — tabla comparativa ordenable
    //
    // TABLAS_RANKING['id'] = {
    //   columnas: [
    //     { clave: 'metodo',  titulo: 'Método',  tipo: 'texto' },
    //     { clave: 'rmse',    titulo: 'RMSE',    decimales: 2, mejor: 'menor' },
    //     { clave: 'cob95',   titulo: 'Cob. 95%', decimales: 1,
    //       mejor: 'cerca', objetivo: 95, sufijo: ' %' }
    //   ],
    //   filas: [ { metodo: 'SARIMA', rmse: 18.92, cob95: 98.4 }, ... ],
    //   inicial: 'rmse',            // columna por la que se ordena al abrir
    //   destacada: 'SARIMA',        // valor de la 1ª columna que va marcado
    //   pie: 'texto bajo la tabla'
    // }
    //
    // El registro admite una FUNCIÓN además de un objeto, igual que
    // MAPAS_ESTACIONALES, para que una tabla pueda leer datos definidos más
    // abajo en el archivo o depender de un control.
    //
    // `mejor` decide qué celda se marca y en qué sentido ordena:
    //   'menor'  — gana el más pequeño (RMSE, MAE, segundos)
    //   'mayor'  — gana el más grande
    //   'cerca'  — gana el más cercano a `objetivo` (la cobertura nominal:
    //              quedarse corto y pasarse son igual de malos, y ninguna
    //              ordenación por menor o mayor sabe expresar eso)
    // ================================================================
    const TABLAS_RANKING = {};

    function distanciaRanking(columna, valor) {
      if (valor === null || valor === undefined || !Number.isFinite(Number(valor))) {
        return Number.POSITIVE_INFINITY;
      }
      const v = Number(valor);
      if (columna.mejor === 'mayor') return -v;
      if (columna.mejor === 'cerca') return Math.abs(v - Number(columna.objetivo));
      return v;
    }

    function pintarTablaRanking(raiz, spec) {
      const marco = raiz.querySelector('.tabla-ranking-marco');
      const pie = raiz.querySelector('.tabla-ranking-pie');
      const estado = raiz.querySelector('.tabla-ranking-estado');
      if (!marco) return;

      const columnas = spec.columnas || [];
      const ordenables = columnas.filter(c => c.tipo !== 'texto');
      if (!columnas.length || !ordenables.length) return;
      let claveOrden = spec.inicial || ordenables[0].clave;

      function columnaDe(clave) {
        return columnas.find(c => c.clave === clave) || ordenables[0];
      }

      function formatea(columna, valor) {
        if (columna.tipo === 'texto') return valor === undefined ? '' : String(valor);
        if (valor === null || valor === undefined || !Number.isFinite(Number(valor))) return '—';
        const d = columna.decimales === undefined ? 2 : columna.decimales;
        return Number(valor).toLocaleString('es-CO', {
          minimumFractionDigits: d, maximumFractionDigits: d
        }) + (columna.sufijo || '');
      }

      function dibuja() {
        const columna = columnaDe(claveOrden);
        const filas = spec.filas.slice().sort(
          (a, b) => distanciaRanking(columna, a[claveOrden]) -
                    distanciaRanking(columna, b[claveOrden]));
        const mejorValor = Math.min.apply(null,
          spec.filas.map(f => distanciaRanking(columna, f[claveOrden])));

        const tabla = document.createElement('table');

        if (spec.descripcion) {
          const caption = document.createElement('caption');
          caption.innerHTML = spec.descripcion;
          tabla.appendChild(caption);
        }

        const thead = document.createElement('thead');
        const trh = document.createElement('tr');
        const thPuesto = document.createElement('th');
        thPuesto.scope = 'col';
        thPuesto.className = 'tabla-ranking-puesto';
        thPuesto.textContent = '#';
        trh.appendChild(thPuesto);

        columnas.forEach(c => {
          const th = document.createElement('th');
          th.scope = 'col';
          if (c.tipo === 'texto') {
            th.innerHTML = `<span class="tabla-ranking-boton">${c.titulo}</span>`;
            th.setAttribute('aria-sort', 'none');
          } else {
            const activa = c.clave === claveOrden;
            // Toda columna ordenable ordena de "mejor" a "peor", así que el
            // sentido depende de `mejor` y no del signo del número.
            th.setAttribute('aria-sort', activa
              ? (c.mejor === 'mayor' ? 'descending' : 'ascending')
              : 'none');
            const boton = document.createElement('button');
            boton.type = 'button';
            boton.className = 'tabla-ranking-boton';
            boton.innerHTML = `${c.titulo}<span class="tabla-ranking-flecha" ` +
              `aria-hidden="true">${activa ? '▲' : '⇅'}</span>`;
            boton.setAttribute('aria-label',
              `Ordenar por ${c.tituloLargo || c.titulo}` +
              (c.mejor === 'cerca' ? `, mejor cuanto más cerca de ${c.objetivo}`
                : c.mejor === 'mayor' ? ', mejor cuanto mayor' : ', mejor cuanto menor'));
            boton.addEventListener('click', () => {
              claveOrden = c.clave;
              dibuja();
              const nuevo = marco.querySelector(
                `th[data-clave="${c.clave}"] .tabla-ranking-boton`);
              if (nuevo) nuevo.focus();
              if (estado) {
                const primera = spec.filas.slice().sort(
                  (a, b) => distanciaRanking(c, a[c.clave]) -
                            distanciaRanking(c, b[c.clave]))[0];
                estado.textContent = `Ordenado por ${c.tituloLargo || c.titulo}: ` +
                  `primero ${primera[columnas[0].clave]} ` +
                  `(${formatea(c, primera[c.clave])}).`;
              }
            });
            th.appendChild(boton);
          }
          th.setAttribute('data-clave', c.clave);
          trh.appendChild(th);
        });
        thead.appendChild(trh);
        tabla.appendChild(thead);

        const tbody = document.createElement('tbody');
        filas.forEach((fila, i) => {
          const tr = document.createElement('tr');
          if (i === 0) tr.className = 'ganadora';
          if (spec.destacada && fila[columnas[0].clave] === spec.destacada) {
            tr.className = (tr.className + ' destacada').trim();
          }
          const tdPuesto = document.createElement('td');
          tdPuesto.className = 'tabla-ranking-puesto';
          tdPuesto.textContent = String(i + 1);
          tr.appendChild(tdPuesto);

          columnas.forEach((c, j) => {
            const celda = document.createElement(j === 0 ? 'th' : 'td');
            if (j === 0) celda.scope = 'row';
            celda.innerHTML = formatea(c, fila[c.clave]);
            if (c.tipo !== 'texto') celda.classList.add('numero');
            if (c.clave === claveOrden) {
              celda.classList.add('columna-activa');
              if (distanciaRanking(c, fila[c.clave]) === mejorValor) {
                celda.classList.add('mejor');
              }
            }
            tr.appendChild(celda);
          });
          tbody.appendChild(tr);
        });
        tabla.appendChild(tbody);

        marco.innerHTML = '';
        marco.appendChild(tabla);
      }

      dibuja();
      if (pie && spec.pie) pie.innerHTML = spec.pie;
    }

    function iniciarTablasRanking() {
      mainContent.querySelectorAll('.tabla-ranking[data-ranking]').forEach(raiz => {
        const registro = TABLAS_RANKING[raiz.dataset.ranking];
        if (!registro) return;
        pintarTablaRanking(raiz, typeof registro === 'function' ? registro() : registro);
      });
    }
