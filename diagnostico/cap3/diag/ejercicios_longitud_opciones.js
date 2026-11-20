// Diagnóstico cap. 3 · prueba de «la más larga / la más corta» y tolerancias.
// node diagnostico/cap3/diag/ejercicios_longitud_opciones.js Htmls_Series/capitulo-3-modelos-ar-ma-arma.html
// Extrae AUTOEVALUACIONES['cap3'], AUTOEVALUACIONES['parcial2'] y
// SIMULACROS['cap3-simulacro'] del HTML, los evalúa con stubs y cuenta los
// caracteres visibles de cada opción (sin etiquetas, sin $ ni \( \), con los
// comandos de LaTeX reducidos a su símbolo). El simulacro no trae clave: se
// usan las claves calculadas en ejercicios_cap3.R.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');

function extrae(marca, cierre) {
  const ini = html.indexOf(marca);
  const fin = html.indexOf(cierre, ini) + cierre.length;
  return 'const Q = ' + html.slice(ini + marca.length - 1, fin);
}
const stubs = ['crearGraficoBarras', 'REZAGOS_T', 'PROCESOS', 'COLORES_GRAFICO', 'REZAGOS', 'MANCHAS', 'lineasBanda'];
const evalua = codigo => new Function(...stubs, codigo + '; return Q;')(...stubs.map(() => null));

const cap3 = evalua(extrae("AUTOEVALUACIONES['cap3'] = [", '\n    ];'));
const parcial2 = evalua(extrae("AUTOEVALUACIONES['parcial2'] = [", '\n    ];'));
const simul = evalua(extrae("SIMULACROS['cap3-simulacro'] = {", '\n    };'));
// Claves del simulacro calculadas en R (índices desde 0)
const CLAVES_SIM = [[1, 4], 0, 1, 2, 3, 0, 1, 2, 3, 0];
simul.preguntas.forEach((p, i) => {
  const k = CLAVES_SIM[i];
  p.opciones = p.opciones.map((t, j) => ({ texto: t, correcta: Array.isArray(k) ? k.includes(j) : k === j }));
});

const visible = s => s
  .replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
  .replace(/\\\(|\\\)/g, '')
  .replace(/\\(nabla|theta|lambda|phi|varepsilon|mu|approx|sigma|pi|rho|psi|ge|le|lt|gt|infty)/g, 'x')
  .replace(/\\[a-zA-Z]+/g, '')
  .replace(/[${}_^\\]/g, '');

function analiza(nombre, Q) {
  console.log(`\n######## ${nombre} (${Q.length} preguntas)`);
  let larga = 0, corta = 0, conUna = 0;
  Q.forEach((p, i) => {
    const tipo = p.tipo || 'opcion';
    if (!p.opciones) {
      console.log(`\nQ${i + 1} · ${tipo} · módulo ${p.modulo} · respuesta ${p.respuesta}, tolerancia ${p.tolerancia}`);
      return;
    }
    console.log(`\nQ${i + 1} · ${tipo}${p.modulo ? ' · módulo ' + p.modulo : ''}`);
    const L = p.opciones.map(o => visible(o.texto).length);
    p.opciones.forEach((o, j) => console.log(
      `  ${'abcde'[j]}) ${o.correcta ? '*' : ' '} ${String(L[j]).padStart(3)} · retro ${o.retro ? 'sí' : (nombre === 'simulacro' ? '—' : 'NO')} · ${visible(o.texto).slice(0, 80)}`));
    if (tipo !== 'multiple') {
      conUna++;
      const max = Math.max(...L), min = Math.min(...L);
      const c = p.opciones.findIndex(o => o.correcta);
      const esLarga = L[c] === max && L.filter(x => x === max).length === 1;
      const esCorta = L[c] === min && L.filter(x => x === min).length === 1;
      if (esLarga) larga++;
      if (esCorta) corta++;
      const otras = L.filter((_, j) => j !== c);
      console.log(`  -> correcta ${'abcde'[c]} (${L[c]}); otras ${Math.min(...otras)}–${Math.max(...otras)}; ` +
        `${esLarga ? 'ES LA MÁS LARGA' : esCorta ? 'ES LA MÁS CORTA' : 'ni la más larga ni la más corta'}; posición ${c + 1}`);
    } else {
      const orden = L.map((x, j) => [x, j]).sort((a, b) => b[0] - a[0]).map(([, j]) => j);
      const nC = p.opciones.filter(o => o.correcta).length;
      const top = orden.slice(0, nC).every(j => p.opciones[j].correcta);
      const bot = orden.slice(-nC).every(j => p.opciones[j].correcta);
      console.log(`  -> ${nC} correctas en ${p.opciones.map((o, j) => o.correcta ? 'abcde'[j] : '').join('')}; ` +
        `marcar las ${nC} más largas: ${top ? 'ACIERTA' : 'falla'}; las ${nC} más cortas: ${bot ? 'ACIERTA' : 'falla'}`);
    }
  });
  console.log(`\n${nombre}: «la más larga» acierta ${larga} de ${conUna}; «la más corta», ${corta} de ${conUna}`);
}
analiza('cap3', cap3);
analiza('parcial2', parcial2);
analiza('simulacro', simul.preguntas);

// Posición de la correcta en el simulacro (el auditor no lo ve: no hay `correcta`)
console.log('\nSimulacro, posición de la correcta en las de una sola: ' +
  CLAVES_SIM.filter(k => !Array.isArray(k)).map(k => k + 1).join(' '));

// Tolerancias de las numéricas, con la comparación exacta del motor
console.log('\n######## Tolerancias (motor: Math.abs(dada - respuesta) <= tolerancia)');
cap3.forEach((p, i) => {
  if (p.tipo !== 'numerica') return;
  const pruebas = {
    1: [0.4878, 0.488, 0.4872, 0.4884, 0.487, 0.49, 0.48, 0.8, 0.4444, 0.6098],
    3: [4.88, 4.9, 4.874, 4.886, 4.87, 4.89, 2.44, 2.88, 2.98, 4.4, 6.29, 3.44],
    6: [11.22, 11.2, 11.3, 11.16, 11.28, 11.15, 11.29, 11.0, 11.218, 10.74, 0.196]
  }[i] || [];
  console.log(`Q${i + 1} (respuesta ${p.respuesta}, tol ${p.tolerancia}): ` +
    pruebas.map(x => `${x}→${Math.abs(x - p.respuesta) <= p.tolerancia ? 'acepta' : 'rechaza'}`).join('  '));
});
