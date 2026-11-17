// Diagnóstico cap. 2 · prueba de «la más larga».
// node diagnostico/cap2/diag/longitud_opciones.js Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html
// Extrae AUTOEVALUACIONES['cap2'] del HTML, lo evalúa con stubs y cuenta los
// caracteres de cada opción de dos maneras: «crudo» (la cadena tal cual) y
// «visible» (sin etiquetas HTML ni delimitadores $ y con los comandos de LaTeX
// reducidos a su símbolo, que es lo que el estudiante ve en pantalla).
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const ini = html.indexOf("AUTOEVALUACIONES['cap2'] = [");
const fin = html.indexOf('];', ini) + 2;
const codigo = html.slice(ini, fin).replace("AUTOEVALUACIONES['cap2'] =", 'const Q =');
const Q = new Function('correlogramaDe', codigo + '; return Q;')(() => null);

const visible = s => s
  .replace(/<[^>]+>/g, '')
  .replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
  .replace(/\\(nabla|theta|lambda|phi|varepsilon|mu|approx|sigma)/g, 'x')
  .replace(/\\[a-zA-Z]+/g, '')
  .replace(/[${}_^\\]/g, '');

let aciertosLarga = 0, conUna = 0;
Q.forEach((p, i) => {
  const tipo = p.tipo || 'opcion';
  console.log(`\nQ${i + 1} · ${tipo} · módulo ${p.modulo}`);
  if (!p.opciones) { console.log(`  respuesta ${p.respuesta}, tolerancia ${p.tolerancia}`); return; }
  const L = p.opciones.map(o => visible(o.texto).length);
  const C = p.opciones.map(o => o.texto.length);
  p.opciones.forEach((o, j) => console.log(
    `  ${'abcde'[j]}) ${o.correcta ? '*' : ' '} visible ${String(L[j]).padStart(3)} · crudo ${String(C[j]).padStart(3)} · retro ${o.retro ? 'sí' : 'NO'} · ${visible(o.texto).slice(0, 70)}`));
  if (tipo !== 'multiple') {
    conUna++;
    const max = Math.max(...L), jmax = L.indexOf(max);
    const correcta = p.opciones.findIndex(o => o.correcta);
    const otras = L.filter((_, j) => j !== correcta);
    const ok = jmax === correcta && L.filter(x => x === max).length === 1;
    if (ok) aciertosLarga++;
    console.log(`  -> la más larga es ${'abcde'[jmax]}; correcta ${'abcde'[correcta]} (${L[correcta]} vs máx. de las otras ${Math.max(...otras)}) ${ok ? 'ACIERTA' : 'falla'}`);
  } else {
    const correctas = p.opciones.map((o, j) => o.correcta ? L[j] : null).filter(x => x !== null);
    const malas = p.opciones.map((o, j) => !o.correcta ? L[j] : null).filter(x => x !== null);
    const orden = L.map((x, j) => [x, j]).sort((a, b) => b[0] - a[0]).map(([, j]) => 'abcde'[j]);
    const media = a => (a.reduce((s, x) => s + x, 0) / a.length).toFixed(1);
    console.log(`  -> media correctas ${media(correctas)} vs incorrectas ${media(malas)}; orden por longitud ${orden.join(' ')}; marcar las ${correctas.length} más largas: ` +
      (orden.slice(0, correctas.length).every(l => p.opciones['abcde'.indexOf(l)].correcta) ? 'ACIERTA' : 'falla'));
  }
});
console.log(`\nEstrategia «la más larga» en ítems de una sola correcta: ${aciertosLarga} de ${conUna}`);
