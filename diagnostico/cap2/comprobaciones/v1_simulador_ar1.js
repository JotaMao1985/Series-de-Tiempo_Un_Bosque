// Verificador independiente R1 · simulador «El deslizador de φ» (M5).
// Extrae del HTML las funciones que usa el simulador y lo reproduce.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
function extrae(nombre) {
  const i = html.indexOf('function ' + nombre + '(');
  let j = html.indexOf('{', i), prof = 0, k = j;
  for (; k < html.length; k++) { if (html[k] === '{') prof++; else if (html[k] === '}') { prof--; if (prof === 0) break; } }
  return html.slice(i, k + 1);
}
eval([extrae('generarRuidoNormal'), extrae('calcularACF'), extrae('diferenciar'), extrae('varianzaMuestral')].join('\n'));
const semilla = Number(html.match(/generarRuidoNormal\(n, (\d+)\)/)[1]);
const n = 200, ruido = generarRuidoNormal(n, semilla);
console.log('semilla del simulador:', semilla);
function sim(phi, dif) { const y = [ruido[0]]; for (let t = 1; t < n; t++) y.push(phi * y[t - 1] + ruido[t]); return dif ? diferenciar(y, 1) : y; }
const b = (m) => 1.96 / Math.sqrt(m);
for (const [phi, dif] of [[0, true], [0.5, true], [0.7, true], [0.95, true], [1, true], [1.05, true], [0.5, false], [0.7, false], [0.8, false], [0.8, true]]) {
  const y = sim(phi, dif), a = calcularACF(y, 24);
  const fuera = a.filter(v => Math.abs(v) > b(y.length)).length;
  console.log(`phi=${phi} dif=${dif}: r1..r5 = ${a.slice(0,5).map(v=>v.toFixed(3)).join(' ')}; fuera=${fuera}/24; var=${varianzaMuestral(y).toFixed(3)}`);
}
// var(∇y)/var(y) con el φ inicial (0.7)
console.log('var ratio phi=0.7:', (varianzaMuestral(sim(0.7,true))/varianzaMuestral(sim(0.7,false))).toFixed(3));
