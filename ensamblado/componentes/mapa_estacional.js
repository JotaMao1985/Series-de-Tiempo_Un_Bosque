    // ================================================================
    // Componente .mapa-estacional — mapa de calor mes x año
    // ================================================================
    // Registro `MAPAS_ESTACIONALES['id']` sobre un contenedor
    // `<div class="mapa-estacional" data-mapa="id">`, igual que SIMULADORES
    // y AUTOEVALUACIONES. El valor de cada registro es un objeto
    //   { anios, filas, minimo, maximo, escala, decimales, unidad, nota, descripcion }
    // o una FUNCIÓN que devuelve uno, para los mapas que dependen de un
    // control. Un simulador puede repintar el suyo llamando directamente a
    // pintarMapaEstacional(raiz, datos). `descripcion` (opcional) dice qué
    // serie y qué transformación se ven; sin ella, el nombre accesible de la
    // rejilla usa el título visible del mapa.
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

    // Luminancia relativa y razón de contraste de las WCAG 2.
    function luminanciaRelativa(color) {
      const m = /rgb\((\d+),\s*(\d+),\s*(\d+)\)/.exec(color);
      if (!m) return null;
      const [r, g, b] = [1, 2, 3].map(i => Number(m[i]) / 255)
        .map(v => (v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)));
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    function razonContraste(a, b) {
      const la = luminanciaRelativa(a), lb = luminanciaRelativa(b);
      return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
    }

    // Color del número sobre una celda, en dos tonos: blanco o negro, el que
    // dé más contraste. El peor caso de los dos es 4.58:1, así que siempre se
    // pasa de 4.5:1. Con un umbral de luminancia fijo (antes, 0.42) los fondos
    // medios —gris verdoso, naranja claro— se quedaban en 2.2–2.9:1; y con
    // tres tonos (pizarra, negro y blanco) dos celdas vecinas de color
    // parecido podían llevar la cifra de dos colores distintos.
    function textoSobre(color) {
      if (luminanciaRelativa(color) === null) return '#000000';
      return razonContraste(color, 'rgb(255,255,255)') >= razonContraste(color, 'rgb(0,0,0)')
        ? '#ffffff' : '#000000';
    }

    // Cifra de una celda o de la leyenda: signo menos tipográfico, como en las
    // tablas y en los ejes, y sin «−0.000» cuando el redondeo da cero.
    function cifraMapa(valor, dec) {
      const texto = Math.abs(valor).toFixed(dec);
      return (valor < 0 && Number(texto) !== 0 ? '−' : '') + texto;
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

      // Cada fila de la rejilla va en un `role="row"` sin caja propia (así la
      // rejilla CSS no cambia): sin filas, un lector de pantalla no
      // puede recorrer el mapa como una tabla.
      const partes = ['<div class="mapa-estacional-fila" role="row">',
        '<div class="mapa-estacional-cabecera" role="columnheader" aria-label="Año"></div>'];
      MESES_CORTOS.forEach(mes => {
        partes.push('<div class="mapa-estacional-cabecera" role="columnheader" aria-label="' + mes + '">'
          + '<span class="mapa-estacional-mes" aria-hidden="true">' + mes + '</span></div>');
      });
      partes.push('</div>');

      datos.filas.forEach((fila, i) => {
        partes.push('<div class="mapa-estacional-fila" role="row">');
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
          const texto = cifraMapa(valor, dec);
          const titulo = etiqueta + ': ' + texto + (unidad ? ' ' + unidad : '');
          partes.push('<div class="mapa-estacional-celda" role="cell" style="background:' + color
            + ';color:' + textoSobre(color) + '" aria-label="' + titulo + '" title="' + titulo + '">'
            + (conNumero ? '<span aria-hidden="true">' + texto + '</span>' : '') + '</div>');
        });
        partes.push('</div>');
      });

      rejilla.innerHTML = partes.join('');

      const tope = Math.max(Math.abs(datos.minimo), Math.abs(datos.maximo));
      const extremos = datos.escala === 'divergente'
        ? [cifraMapa(-tope, dec), cifraMapa(tope, dec)]
        : [cifraMapa(datos.minimo, dec), cifraMapa(datos.maximo, dec)];

      // Nombre accesible: qué serie y qué transformación, cuántos años y el
      // rango de los valores. Se reescribe en cada repintado.
      const titulo = raiz.querySelector('.mapa-estacional-titulo');
      const quien = datos.descripcion
        || (titulo ? titulo.textContent.trim() : 'Mapa estacional, mes × año');
      const n = datos.anios.length;
      rejilla.setAttribute('aria-label', quien + ': ' + n + (n === 1 ? ' año' : ' años')
        + ' (' + datos.anios[0] + (n > 1 ? '–' + datos.anios[n - 1] : '') + ') en filas y 12 meses en columnas; valores de '
        + cifraMapa(datos.minimo, dec) + ' a ' + cifraMapa(datos.maximo, dec) + (unidad ? ' ' + unidad : '')
        + (datos.escala === 'divergente' ? '; escala de color centrada en cero' : ''));

      if (leyenda) {
        const izq = datos.escala === 'divergente'
          ? 'rgb(255,102,0)' : 'rgb(238,245,242)';
        const der = 'rgb(1,40,32)';
        const centro = datos.escala === 'divergente'
          ? ', rgb(248,250,252) 50%' : '';
        leyenda.innerHTML = '<span>' + extremos[0] + '</span>'
          + '<span class="mapa-estacional-barra" aria-hidden="true" style="background:linear-gradient(90deg,'
          + izq + centro + ',' + der + ')"></span>'
          + '<span>' + extremos[1] + (unidad ? ' ' + unidad : '') + '</span>';
      }

      const nota = raiz.querySelector('.mapa-estacional-nota');
      if (nota && datos.nota !== undefined) nota.innerHTML = datos.nota;

      prepararLecturaMapa(raiz);
      ajustarMapaEstacional(raiz);
    }

    // Los doce meses se ven siempre, sin desplazar la rejilla: lo que el mapa
    // enseña son las bandas verticales, y con la rejilla cortada en junio (a
    // 800 y a 375 px) la mitad quedaba fuera sin ningún aviso. Si la cifra no
    // cabe en su celda, el mapa se queda con el color, y hay dos maneras de
    // leer los valores:
    //   · la línea del valor, bajo la rejilla, da el de la celda que se toca,
    //     se señala o se recorre con las flechas (la rejilla es una sola
    //     parada del tabulador);
    //   · el botón «Ver las cifras» pasa a la rejilla con cifras, más ancha
    //     que su caja y desplazable, con un degradado y una flecha en el
    //     borde derecho mientras quedan meses por ver; pulsado otra vez, vuelve.
    // Los meses de la cabecera pasan a su inicial si la abreviatura no cabe.
    function ajustarMapaEstacional(raiz) {
      const rejilla = raiz.querySelector('.mapa-estacional-rejilla');
      if (!rejilla || !rejilla.clientWidth) return;
      raiz.classList.remove('mapa-estacional--sin-cifras', 'mapa-estacional--desplazable');
      rejilla.removeAttribute('tabindex');
      const meses = Array.from(rejilla.querySelectorAll('.mapa-estacional-mes'));
      meses.forEach((s, j) => { s.textContent = MESES_CORTOS[j]; });
      const cifras = Array.from(rejilla.querySelectorAll('.mapa-estacional-celda > span'));
      const noCabe = cifras.some(s => s.offsetWidth > s.parentNode.clientWidth - 2);
      const boton = raiz.querySelector('.mapa-estacional-boton');
      if (boton) boton.hidden = !noCabe;
      if (noCabe && raiz.dataset.verCifras === 'si') {
        const ancho = Math.max.apply(null, cifras.map(s => s.offsetWidth));
        rejilla.style.setProperty('--mapa-celda-min', Math.ceil(ancho + 8) + 'px');
        raiz.classList.add('mapa-estacional--desplazable');
      } else if (noCabe) {
        raiz.classList.add('mapa-estacional--sin-cifras');
      }
      if (noCabe) rejilla.setAttribute('tabindex', '0');
      if (boton) boton.setAttribute('aria-pressed', raiz.dataset.verCifras === 'si' ? 'true' : 'false');
      if (meses.some(s => s.offsetWidth > s.parentNode.clientWidth)) {
        meses.forEach((s, j) => { s.textContent = MESES_CORTOS[j].charAt(0); });
      }
      senalarDesplazamiento(raiz);
    }

    // El degradado y la flecha del borde derecho: solo con la rejilla más
    // ancha que su caja y mientras queden meses a la derecha.
    function senalarDesplazamiento(raiz) {
      const marco = raiz.querySelector('.mapa-estacional-marco');
      const mas = raiz.querySelector('.mapa-estacional-mas');
      if (!marco || !mas) return;
      mas.hidden = !(raiz.classList.contains('mapa-estacional--desplazable')
        && marco.scrollLeft + marco.clientWidth < marco.scrollWidth - 2);
    }

    // Línea del valor señalado, botón de las cifras, señal de desplazamiento,
    // teclado y el observador que reajusta el mapa si cambia su ancho. Se
    // montan una vez por mapa.
    function prepararLecturaMapa(raiz) {
      if (raiz.dataset.mapaListo) return;
      raiz.dataset.mapaListo = 'si';
      const marco = raiz.querySelector('.mapa-estacional-marco');
      const rejilla = raiz.querySelector('.mapa-estacional-rejilla');
      if (!marco || !rejilla) return;

      const ventana = document.createElement('div');
      ventana.className = 'mapa-estacional-ventana';
      marco.parentNode.insertBefore(ventana, marco);
      ventana.appendChild(marco);
      const mas = document.createElement('div');
      mas.className = 'mapa-estacional-mas';
      mas.setAttribute('aria-hidden', 'true');
      mas.textContent = '›';
      mas.hidden = true;
      ventana.appendChild(mas);
      marco.addEventListener('scroll', () => senalarDesplazamiento(raiz));

      const valor = document.createElement('p');
      valor.className = 'mapa-estacional-valor';
      valor.setAttribute('aria-hidden', 'true');
      const aviso = 'A este ancho las celdas llevan solo el color: toca o señala una, o recórrelas con las flechas, para leer su valor.';
      valor.textContent = aviso;
      ventana.insertAdjacentElement('afterend', valor);

      const boton = document.createElement('button');
      boton.type = 'button';
      boton.className = 'mapa-estacional-boton';
      boton.textContent = 'Ver las cifras';
      boton.setAttribute('aria-pressed', 'false');
      boton.hidden = true;
      valor.insertAdjacentElement('afterend', boton);
      boton.addEventListener('click', () => {
        raiz.dataset.verCifras = raiz.dataset.verCifras === 'si' ? 'no' : 'si';
        valor.textContent = aviso;
        ajustarMapaEstacional(raiz);
      });

      // Celda señalada: la que se toca, se señala o se alcanza con las flechas.
      const senalar = celda => {
        raiz.querySelectorAll('.mapa-estacional-activa').forEach(c => c.classList.remove('mapa-estacional-activa'));
        if (!celda) return;
        celda.classList.add('mapa-estacional-activa');
        valor.textContent = celda.getAttribute('aria-label');
        if (raiz.classList.contains('mapa-estacional--desplazable')) {
          // Que la celda señalada quede dentro de la caja desplazable.
          const izq = celda.offsetLeft, der = izq + celda.offsetWidth;
          if (izq < marco.scrollLeft + 40) marco.scrollLeft = Math.max(0, izq - 48);
          else if (der > marco.scrollLeft + marco.clientWidth) marco.scrollLeft = der - marco.clientWidth + 4;
        }
      };
      const muestra = ev => {
        const celda = ev.target.closest && ev.target.closest('.mapa-estacional-celda');
        if (celda && raiz.contains(celda)) valor.textContent = celda.getAttribute('aria-label');
      };
      raiz.addEventListener('pointerover', muestra);
      // Con las cifras a la vista, un clic no deja marcada la celda.
      raiz.addEventListener('click', ev => {
        const celda = ev.target.closest && ev.target.closest('.mapa-estacional-celda');
        if (celda && raiz.contains(celda) && rejilla.hasAttribute('tabindex')) senalar(celda);
      });

      // Teclado: con la rejilla enfocada, las flechas mueven la celda
      // señalada; Inicio y Fin van al primer y al último mes de la fila.
      const filas = () => Array.from(rejilla.querySelectorAll('.mapa-estacional-fila'))
        .map(f => Array.from(f.querySelectorAll('.mapa-estacional-celda'))).filter(f => f.length);
      const posicion = () => {
        const activa = rejilla.querySelector('.mapa-estacional-activa');
        const f = filas();
        for (let i = 0; i < f.length; i++) {
          const j = f[i].indexOf(activa);
          if (j >= 0) return [i, j];
        }
        return null;
      };
      rejilla.addEventListener('focus', () => {
        if (!rejilla.hasAttribute('tabindex')) return;
        if (!posicion()) { const f = filas(); if (f.length) senalar(f[0][0]); }
        else valor.textContent = rejilla.querySelector('.mapa-estacional-activa').getAttribute('aria-label');
      });
      rejilla.addEventListener('blur', () => senalar(null));
      rejilla.addEventListener('keydown', ev => {
        if (!rejilla.hasAttribute('tabindex')) return;
        const f = filas();
        if (!f.length) return;
        let [i, j] = posicion() || [0, 0];
        const paso = { ArrowRight: [0, 1], ArrowLeft: [0, -1], ArrowDown: [1, 0], ArrowUp: [-1, 0] }[ev.key];
        if (paso) { i += paso[0]; j += paso[1]; }
        else if (ev.key === 'Home') j = 0;
        else if (ev.key === 'End') j = f[i].length - 1;
        else return;
        ev.preventDefault();
        i = Math.max(0, Math.min(f.length - 1, i));
        j = Math.max(0, Math.min(f[i].length - 1, j));
        senalar(f[i][j]);
      });

      if (typeof ResizeObserver === 'function') {
        let ancho = ventana.clientWidth;
        new ResizeObserver(() => {
          if (ventana.clientWidth === ancho) return;
          ancho = ventana.clientWidth;
          valor.textContent = aviso;
          ajustarMapaEstacional(raiz);
        }).observe(ventana);
      }
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
