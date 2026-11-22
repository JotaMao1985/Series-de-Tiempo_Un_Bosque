// Diagnóstico cap. 4 · «la más larga / la más corta», posición de la correcta,
// pistas, retros por opción y tolerancias, sobre los cuatro instrumentos.
//   node diagnostico/cap4/diag/ejercicios_vuelca.js > diagnostico/cap4/diag/ejercicios_vuelca.json
//   node diagnostico/cap4/diag/ejercicios_longitud_opciones.js > diagnostico/cap4/diag/ejercicios_longitud_opciones.out
// Adaptado de diagnostico/cap3/diag/ejercicios_longitud_opciones.js. Longitud =
// caracteres visibles (sin etiquetas, sin $, comandos de LaTeX reducidos).
// El simulacro del M11 no trae clave: se usan las calculadas en ejercicios_cap4.R.
const fs = require('fs');
const path = require('path');
const J = JSON.parse(fs.readFileSync(path.join(__dirname, 'ejercicios_vuelca.json'), 'utf8'));

// Claves del simulacro (índices desde 0), de ejercicios_cap4.out
const CLAVES_SIM = { 2: [0, 2, 4], 4: 2, 8: 0, 9: [0, 3, 4], 10: 3 };
J.simulacro.forEach(p => {
  const k = CLAVES_SIM[p.n];
  if (k === undefined) return;
  p.opciones.forEach((o, j) => { o.correcta = Array.isArray(k) ? k.includes(j) : k === j; });
});

const L = 'abcde';
function analiza(nombre, Q) {
  console.log(`\n######## ${nombre} (${Q.length} preguntas)`);
  let larga = 0, corta = 0, conUna = 0, sinRetro = 0, totOp = 0;
  const pos = [];
  Q.forEach(p => {
    if (!p.opciones.length) {
      console.log(`\n${p.n} · ${p.tipo} · ${p.modulo ?? ''} · respuesta ${p.respuesta} · tolerancia ${p.tolerancia}` +
        (p.pista ? '' : ' · SIN PISTA'));
      return;
    }
    console.log(`\n${p.n} · ${p.tipo} · ${p.modulo ?? ''}${p.pista ? '' : ' · SIN PISTA'}`);
    p.opciones.forEach((o, j) => {
      totOp++; if (!o.retro) sinRetro++;
      console.log(`  ${L[j]}) ${o.correcta ? '*' : ' '} ${String(o.largo).padStart(3)} · retro ${o.retro ? 'sí' : 'NO'} · ${o.texto.slice(0, 80)}`);
    });
    const nC = p.opciones.filter(o => o.correcta).length;
    const Ls = p.opciones.map(o => o.largo);
    if (nC === 1) {
      conUna++;
      const c = p.opciones.findIndex(o => o.correcta);
      pos.push(c + 1);
      const max = Math.max(...Ls), min = Math.min(...Ls);
      const esLarga = Ls[c] === max && Ls.filter(x => x === max).length === 1;
      const esCorta = Ls[c] === min && Ls.filter(x => x === min).length === 1;
      if (esLarga) larga++; if (esCorta) corta++;
      const otras = Ls.filter((_, j) => j !== c);
      console.log(`  -> correcta ${L[c]} (${Ls[c]}); otras ${Math.min(...otras)}–${Math.max(...otras)}; ` +
        `${esLarga ? 'ES LA MÁS LARGA' : esCorta ? 'ES LA MÁS CORTA' : 'ni la más larga ni la más corta'}; posición ${c + 1}`);
    } else if (nC > 1) {
      const orden = Ls.map((x, j) => [x, j]).sort((a, b) => b[0] - a[0]).map(([, j]) => j);
      const top = orden.slice(0, nC).every(j => p.opciones[j].correcta);
      const bot = orden.slice(-nC).every(j => p.opciones[j].correcta);
      console.log(`  -> ${nC} correctas en ${p.opciones.map((o, j) => o.correcta ? L[j] : '').join('')}; ` +
        `marcar las ${nC} más largas: ${top ? 'ACIERTA' : 'falla'}; las ${nC} más cortas: ${bot ? 'ACIERTA' : 'falla'}`);
    }
    if (p.pista && /\b(son|hay) (dos|tres|cuatro)\b/i.test(p.pista)) console.log('  !! la pista anuncia cuántas son correctas');
  });
  console.log(`\n${nombre}: «la más larga» acierta ${larga} de ${conUna}; «la más corta», ${corta} de ${conUna}; ` +
    `posiciones de la correcta: ${pos.join(' ')}; opciones sin retro: ${sinRetro} de ${totOp}`);
  return pos;
}
const posiciones = {};
for (const k of ['cap4', 'simulacro', 'bloque-a', 'bloque-c', 'bloque-d', 'prep-simulacro']) posiciones[k] = analiza(k, J[k]);
analiza('bloque-b', J['bloque-b']);

// Reparto de posiciones del preparcial entero (bloques A, C, D y su simulacro)
const prepPos = [].concat(posiciones['bloque-a'], posiciones['bloque-c'], posiciones['bloque-d'], posiciones['prep-simulacro']);
const reparto = pos => [1, 2, 3, 4].map(k => `${k}→${pos.filter(x => x === k).length}`).join(', ');
console.log('\nReparto cap4: ' + reparto(posiciones.cap4));
console.log('Reparto simulacro M11: ' + reparto(posiciones.simulacro));
console.log('Reparto preparcial (A, C, D y simulacro): ' + reparto(prepPos) + ` (n = ${prepPos.length})`);
const racha = pos => pos.reduce((a, x, i) => (i && x === pos[i - 1] ? [Math.max(a[0], a[1] + 1), a[1] + 1] : [a[0], 1]), [1, 1])[0];
console.log('Racha máxima de la misma posición, preparcial por bloque: ' +
  ['bloque-a', 'bloque-c', 'bloque-d'].map(b => `${b} ${racha(posiciones[b])}`).join(', '));

// Tolerancias: la comparación exacta del motor, Math.abs(dada - respuesta) <= tolerancia
console.log('\n######## Tolerancias (motor: Math.abs(dada - respuesta) <= tolerancia)');
const pruebas = {
  'cap4-2': [151.97, 152, 151.99, 151.66, 151.6, 152.4, 151.5, 54.0, 166.88, 200.88],
  'cap4-8': [1, 1.0, 0.999, 1.002, 1.003, -1, 0],
  'bloque-b-1': [0.4, -0.4, 0.3], 'bloque-b-2': [-0.4851, -0.485, -0.49, -0.3731, -0.52],
  'bloque-b-3': [4.19, 4.18, 4.2, 4.12, 5.9, 8.94], 'bloque-b-4': [-0.7, 0.9, 0.2, 0.7],
  'bloque-b-5': [9.03, 9.02, 9.04, 9.05, 9.24, 5.53, 6.01], 'bloque-b-6': [7.49, 7.48, 7.5, 7.16],
  'bloque-b-7': [281.63, 281.62, 281.6, 280.1], 'bloque-b-8': [3.6559, 3.656, 3.66, 3.595],
  'bloque-b-9': [1253.51, 1253.5, 1253.16, 1251.37], 'bloque-b-10': [99.33, 99.32, 99.34, 98.96, 98.57],
  'bloque-b-11': [6.26, 6.25, 6.24, 6.27, 6.28, 8.77, 3.68], 'bloque-b-12': [83.1, 83.08, 83.05, 127.05, 166.2],
  'prep-simulacro-1': [2.8402, 2.84, 3.125], 'prep-simulacro-4': [73.12, 73.11, 73.13, 73.1159, 26.59],
  'prep-simulacro-5': [395.67, 395.68, 395.66, 395.69, 395.7, 391.07], 'prep-simulacro-6': [9.1, 9.10, 9.12, 4.27, 6.79]
};
for (const k of ['cap4', 'bloque-b', 'prep-simulacro']) J[k].forEach(p => {
  if (p.tipo !== 'numerica') return;
  const pr = pruebas[`${k}-${p.n}`] || [];
  console.log(`${k} ${p.n} (respuesta ${p.respuesta}, tol ${p.tolerancia}): ` +
    pr.map(x => `${x}→${Math.abs(x - p.respuesta) <= p.tolerancia ? 'acepta' : 'rechaza'}`).join('  '));
});
