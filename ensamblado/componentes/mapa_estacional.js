    // ================================================================
    // Componente .mapa-estacional — mapa de calor mes x año
    // ================================================================
    // Registro `MAPAS_ESTACIONALES['id']` sobre un contenedor
    // `<div class="mapa-estacional" data-mapa="id">`, igual que SIMULADORES
    // y AUTOEVALUACIONES. El valor de cada registro es un objeto
    //   { anios, filas, minimo, maximo, escala, decimales, unidad, nota }
    // o una FUNCIÓN que devuelve uno, para los mapas que dependen de un
    // control. Un simulador puede repintar el suyo llamando directamente a
    // pintarMapaEstacional(raiz, datos).
    const MAPAS_ESTACIONALES = {};

    const MESES_CORTOS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                          'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

    // Interpolación lineal entre dos colores dados como [r, g, b].
    function mezclarColor(a, b, t) {
      const c = t < 0 ? 0 : t > 1 ? 1 : t;
      return 'rgb(' + [0, 1, 2].map(i => Math.round(a[i] + (b[i] - a[i]) * c)).join(',') + ')';
    }

    // Secuencial: verde de la paleta, de muy claro a muy oscuro. Para niveles.
    const VERDE_CLARO = [238, 245, 242];
    const VERDE_OSCURO = [1, 40, 32];
    // Divergente: naranja (negativo) - gris muy claro (cero) - verde (positivo).
    // Para series ya diferenciadas, donde el cero es el valor con significado.
    const NARANJA = [255, 102, 0];
    const NEUTRO = [248, 250, 252];

    function colorMapa(valor, datos) {
      if (valor === null || valor === undefined || !isFinite(valor)) return null;
      if (datos.escala === 'divergente') {
        const tope = Math.max(Math.abs(datos.minimo), Math.abs(datos.maximo)) || 1;
        const t = Math.abs(valor) / tope;
        return valor < 0 ? mezclarColor(NEUTRO, NARANJA, t) : mezclarColor(NEUTRO, VERDE_OSCURO, t);
      }
      const rango = (datos.maximo - datos.minimo) || 1;
      return mezclarColor(VERDE_CLARO, VERDE_OSCURO, (valor - datos.minimo) / rango);
    }

    // Sobre fondo oscuro el número tiene que ir en blanco o no se lee. El
    // umbral se decide con la luminancia relativa, no a ojo.
    function textoSobre(color) {
      const m = /rgb\((\d+),(\d+),(\d+)\)/.exec(color);
      if (!m) return '#1e293b';
      const [r, g, b] = [1, 2, 3].map(i => Number(m[i]) / 255)
        .map(v => (v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)));
      return (0.2126 * r + 0.7152 * g + 0.0722 * b) > 0.42 ? '#1e293b' : '#ffffff';
    }

    function pintarMapaEstacional(raiz, datos) {
      const rejilla = raiz.querySelector('.mapa-estacional-rejilla');
      const leyenda = raiz.querySelector('.mapa-estacional-leyenda');
      if (!rejilla || !datos) return;

      const dec = datos.decimales === undefined ? 0 : datos.decimales;
      const unidad = datos.unidad || '';
      // Con muchos años la cifra no cabe: se deja solo el color, y el valor
      // sigue disponible en el nombre accesible y en el tooltip.
      const conNumero = datos.filas.length <= 20;

      const partes = ['<div class="mapa-estacional-cabecera" aria-hidden="true"></div>'];
      MESES_CORTOS.forEach(mes => {
        partes.push('<div class="mapa-estacional-cabecera" role="columnheader">' + mes + '</div>');
      });

      datos.filas.forEach((fila, i) => {
        partes.push('<div class="mapa-estacional-anio" role="rowheader">' + datos.anios[i] + '</div>');
        fila.forEach((valor, j) => {
          const vacia = valor === null || valor === undefined || !isFinite(valor);
          const etiqueta = MESES_CORTOS[j] + ' ' + datos.anios[i];
          if (vacia) {
            partes.push('<div class="mapa-estacional-celda mapa-estacional-vacia" role="cell"'
              + ' aria-label="' + etiqueta + ': sin dato" title="' + etiqueta + ': sin dato">·</div>');
            return;
          }
          const color = colorMapa(valor, datos);
          const texto = valor.toFixed(dec);
          const titulo = etiqueta + ': ' + texto + (unidad ? ' ' + unidad : '');
          partes.push('<div class="mapa-estacional-celda" role="cell" style="background:' + color
            + ';color:' + textoSobre(color) + '" aria-label="' + titulo + '" title="' + titulo + '">'
            + (conNumero ? texto : '') + '</div>');
        });
      });

      rejilla.innerHTML = partes.join('');

      if (leyenda) {
        const izq = datos.escala === 'divergente'
          ? 'rgb(255,102,0)' : 'rgb(238,245,242)';
        const der = 'rgb(1,40,32)';
        const centro = datos.escala === 'divergente'
          ? ', rgb(248,250,252) 50%' : '';
        const tope = Math.max(Math.abs(datos.minimo), Math.abs(datos.maximo));
        const extremos = datos.escala === 'divergente'
          ? [(-tope).toFixed(dec), tope.toFixed(dec)]
          : [datos.minimo.toFixed(dec), datos.maximo.toFixed(dec)];
        leyenda.innerHTML = '<span>' + extremos[0] + '</span>'
          + '<span class="mapa-estacional-barra" aria-hidden="true" style="background:linear-gradient(90deg,'
          + izq + centro + ',' + der + ')"></span>'
          + '<span>' + extremos[1] + (unidad ? ' ' + unidad : '') + '</span>';
      }

      const nota = raiz.querySelector('.mapa-estacional-nota');
      if (nota && datos.nota !== undefined) nota.innerHTML = datos.nota;
    }

    // Construye la matriz año x mes que espera pintarMapaEstacional a partir de
    // una serie y del mes en que empieza. Vive aquí, y no en el JavaScript de
    // un capítulo, para que todas las instancias del proyecto la compartan.
    function matrizMesAnio(valores, anioInicio, mesInicio) {
      const filas = [], anios = [];
      let a = anioInicio, m = mesInicio;
      let fila = new Array(12).fill(null);
      anios.push(a);
      for (let i = 0; i < valores.length; i++) {
        fila[m - 1] = valores[i];
        m += 1;
        if (m > 12 && i < valores.length - 1) {
          filas.push(fila); fila = new Array(12).fill(null);
          m = 1; a += 1; anios.push(a);
        }
      }
      filas.push(fila);
      const planos = valores.filter(v => v !== null && v !== undefined && isFinite(v));
      return {
        anios: anios, filas: filas,
        minimo: Math.min.apply(null, planos), maximo: Math.max.apply(null, planos)
      };
    }

    function iniciarMapasEstacionales() {
      mainContent.querySelectorAll('.mapa-estacional[data-mapa]').forEach(raiz => {
        const registro = MAPAS_ESTACIONALES[raiz.dataset.mapa];
        if (!registro) return;
        pintarMapaEstacional(raiz, typeof registro === 'function' ? registro() : registro);
      });
    }

