// Diagnóstico cap. 5 · «la más larga / la más corta», posición de la correcta,
// pistas, retros por opción y tolerancias, sobre el quiz cap5 y el simulacro.
//   node diagnostico/cap5/diag/ejercicios_vuelca.js > diagnostico/cap5/diag/ejercicios_vuelca.json
//   Rscript diagnostico/cap5/diag/ejercicios_comprueba.R   (escribe ejercicios_variantes.json)
//   node diagnostico/cap5/diag/ejercicios_longitud_opciones.js > diagnostico/cap5/diag/ejercicios_longitud_opciones.out
// Adaptado de diagnostico/cap4/diag/ejercicios_longitud_opciones.js. Longitud =
// caracteres visibles (sin etiquetas, sin $, comandos de LaTeX reducidos a una letra).
const fs = require('fs');
const path = require('path');
const J = JSON.parse(fs.readFileSync(path.join(__dirname, 'ejercicios_vuelca.json'), 'utf8'));
const L = 'abcde';
function analiza(nombre, Q) {
  console.log(`\n######## ${nombre} (${Q.length} preguntas)`);
  let larga = 0, corta = 0, conUna = 0, sinRetro = 0, totOp = 0;
  const pos = [];
  Q.forEach(p => {
    if (!p.opciones.length) {
      const k = p.respuesta ?? (p.clave && p.clave.valor), t = p.tolerancia ?? (p.clave && p.clave.tol);
      console.log(`\n${p.n} · ${p.tipo} · ${p.modulo ?? p.etiqueta ?? ''} · respuesta ${k} · tolerancia ${t}` +
        (t && k ? ` (${(100 * t / Math.abs(k)).toFixed(2)} % de la clave)` : '') + (p.pista || nombre !== 'cap5' ? '' : ' · SIN PISTA'));
      return;
    }
    console.log(`\n${p.n} · ${p.tipo} · ${p.modulo ?? p.etiqueta ?? ''}${p.pista || nombre !== 'cap5' ? '' : ' · SIN PISTA'}`);
    p.opciones.forEach((o, j) => {
      totOp++; if (!o.retro) sinRetro++;
      console.log(`  ${L[j]}) ${o.correcta ? '*' : ' '} ${String(o.largo).padStart(3)} · retro ${o.retro ? 'sí' : 'NO'} · ${o.texto.slice(0, 90)}`);
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
        `${esLarga ? 'ES LA MÁS LARGA' : esCorta ? 'ES LA MÁS CORTA' : 'ni la más larga ni la más corta'}; ` +
        `razón correcta / media de las otras ${(Ls[c] / (otras.reduce((a, b) => a + b, 0) / otras.length)).toFixed(2)}; posición ${c + 1}`);
    } else if (nC > 1) {
      const orden = Ls.map((x, j) => [x, j]).sort((a, b) => b[0] - a[0]).map(([, j]) => j);
      const top = orden.slice(0, nC).every(j => p.opciones[j].correcta);
      const bot = orden.slice(-nC).every(j => p.opciones[j].correcta);
      console.log(`  -> ${nC} correctas de ${p.opciones.length} en ${p.opciones.map((o, j) => o.correcta ? L[j] : '').join('')}; ` +
        `marcar las ${nC} más largas: ${top ? 'ACIERTA' : 'falla'}; las ${nC} más cortas: ${bot ? 'ACIERTA' : 'falla'}; ` +
        `marcarlas todas: ${nC === p.opciones.length ? 'ACIERTA' : 'falla'}`);
    }
    if (p.pista && /\b(son|hay) (dos|tres|cuatro)\b/i.test(p.pista)) console.log('  !! la pista anuncia cuántas son correctas');
  });
  console.log(`\n${nombre}: «la más larga» acierta ${larga} de ${conUna}; «la más corta», ${corta} de ${conUna}; ` +
    `posiciones de la correcta: ${pos.join(' ')}; opciones sin retro: ${sinRetro} de ${totOp}`);
  const reparto = [1, 2, 3, 4].map(k => `${k}→${pos.filter(x => x === k).length}`).join(', ');
  console.log(`Reparto de posiciones: ${reparto}`);
}
analiza('cap5', J.cap5);
analiza('simulacro', J.simulacro);

console.log('\n######## Pistas del quiz (texto visible)');
J.cap5.forEach(p => console.log(`Q${p.n} (M${p.modulo}): ${p.pista}`));

console.log('\n######## Tolerancias del quiz (motor: Math.abs(dada - respuesta) <= tolerancia)');
const prQ = { 3: [83, 83.4, 82.6, 84, 94, 95, 82], 7: [0.1883, 0.188, 0.19, 0.185, 0.1926, 0.18, 0.2, (1.08 - 1) / 0.45, 1.0840 / 0.4462, -(1.0840 - 1) / 0.4462] };  // sondas: respuestas posibles, las tres últimas calculadas aquí
J.cap5.forEach(p => {
  if (p.tipo !== 'numerica') return;
  console.log(`Q${p.n} (respuesta ${p.respuesta}, tol ${p.tolerancia}): ` +
    (prQ[p.n] || []).map(x => `${x}→${Math.abs(x - p.respuesta) <= p.tolerancia ? 'acepta' : 'rechaza'}`).join('  '));
});

console.log('\n######## Tolerancias del simulacro (motor: Math.abs(x - clave.valor) <= clave.tol; ruta si |x - ruta| <= clave.tol)');
// Variantes calculadas en ejercicios_comprueba.R (redondeos honestos y errores sin ruta).
const prS = JSON.parse(fs.readFileSync(path.join(__dirname, 'ejercicios_variantes.json'), 'utf8'));
J.simulacro.forEach(p => {
  if (p.tipo !== 'numero') return;
  const k = p.clave.valor, t = p.clave.tol;
  console.log(`\nN${p.n} (clave ${k}, tol ${t} = ${(100 * t / Math.abs(k)).toFixed(2)} %)`);
  p.rutas.forEach(r => console.log(`  ruta ${r.valor} (${r.texto}): |ruta − clave| = ${Math.abs(r.valor - k).toFixed(6)} → ${Math.abs(r.valor - k) <= t ? 'ACEPTADA COMO CORRECTA' : 'separada'}`));
  Object.entries(prS[p.n] || {}).forEach(([nom, x]) => {
    const ok = Math.abs(x - k) <= t;
    const ruta = p.rutas.find(r => Math.abs(x - r.valor) <= t);
    console.log(`  variante «${nom}» ${x}: ${ok ? 'ACEPTA' : 'rechaza'}${!ok && ruta ? ' (nombra la ruta: ' + ruta.texto + ')' : !ok ? ' (sin ruta que la nombre)' : ''}`);
  });
});
console.log('\n######## Textos de las rutas (lo que ve el estudiante tras entregar)');
J.simulacro.forEach(p => p.rutas.forEach(r => console.log(`N${p.n}: si obtuviste ${r.cifra}, ${r.texto}`)));
