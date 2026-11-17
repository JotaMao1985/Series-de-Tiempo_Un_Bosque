// R1 del capítulo 2 · las dos cifras del simulador «El deslizador de φ» (M5) que cita la
// nota de al lado, con las funciones extraídas del propio HTML (mismo ruido: n = 200,
// semilla 20260726) y el formato de su lectura (toFixed(4)).
// Desde la raíz del repo: node diagnostico/cap2/comprobaciones/r1_simulador_ar1.js
const fs = require('fs');
const html = fs.readFileSync('Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html', 'utf8');
function extrae(nombre) {
  const i = html.indexOf(`function ${nombre}(`);
  let j = html.indexOf('{', i), prof = 0, k = j;
  for (; k < html.length; k++) { if (html[k] === '{') prof++; else if (html[k] === '}') { prof--; if (prof === 0) break; } }
  return html.slice(i, k + 1);
}
eval(['generarRuidoNormal', 'calcularACF', 'diferenciar', 'varianzaMuestral'].map(extrae).join('\n'));
const n = 200, ruido = generarRuidoNormal(n, 20260726);
function simular(phi, dif) {
  const y = [ruido[0]];
  for (let t = 1; t < n; t++) y.push(phi * y[t - 1] + ruido[t]);
  return dif ? diferenciar(y, 1) : y;
}
console.log('phi  | con ∇: r1 (lectura) | teórico -(1-phi)/2 | varianza sin ∇ -> con ∇');
for (const phi of [0, 0.5, 0.7, 0.8, 1, 1.05]) {
  const d = simular(phi, true), y = simular(phi, false);
  console.log(phi.toFixed(2), '|', calcularACF(d, 24)[0].toFixed(4), '|', phi <= 1 ? (-(1 - phi) / 2).toFixed(3) : '—', '|',
    varianzaMuestral(y).toFixed(3), '->', varianzaMuestral(d).toFixed(3));
}
const d105 = simular(1.05, true);
console.log('phi = 1.05 con ∇: últimos valores', d105.slice(-3).map(v => v.toFixed(1)).join(' '), '· rezagos fuera de banda:',
  calcularACF(d105, 24).filter(r => Math.abs(r) > 1.96 / Math.sqrt(d105.length)).length, 'de 24');
