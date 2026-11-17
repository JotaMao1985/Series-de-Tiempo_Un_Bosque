// R2 del capítulo 2 · el simulador «El deslizador de φ» (M5) y la nota de al lado.
// (1) Las dos cifras que la nota cita (−0.252 y −0.506) siguen saliendo: la R2 no tocó el
//     ruido ni el cálculo, solo el formato de la lectura (signo menos tipográfico).
// (2) Lo que la nota dice ahora del caso φ = 0.95: con el ruido del simulador (n = 200) el
//     correlograma SÍ se distingue del de φ = 1; y la frase general —con muestras más cortas
//     se distinguen menos— se comprueba aquí con otras semillas y otros tamaños (no hay
//     ninguna cifra de esto en la prosa).
// Desde la raíz del repo: node diagnostico/cap2/comprobaciones/r2_simulador_ar1.js
const fs = require('fs');
const html = fs.readFileSync('Htmls_Series/capitulo-2-estacionariedad-acf-pacf.html', 'utf8');
function extrae(nombre) {
  const i = html.indexOf(`function ${nombre}(`);
  let j = html.indexOf('{', i), prof = 0, k = j;
  for (; k < html.length; k++) { if (html[k] === '{') prof++; else if (html[k] === '}') { prof--; if (prof === 0) break; } }
  return html.slice(i, k + 1);
}
eval(['generarRuidoNormal', 'calcularACF', 'diferenciar', 'varianzaMuestral', 'cifra'].map(extrae).join('\n'));
function serie(phi, ruido) { const y = [ruido[0]]; for (let t = 1; t < ruido.length; t++) y.push(phi * y[t - 1] + ruido[t]); return y; }
const ruido = generarRuidoNormal(200, 20260726);

console.log('(1) lectura con ∇ (formato de la R2):');
for (const phi of [0, 0.5]) console.log('   φ =', phi.toFixed(2), '→ r₁ =', cifra(calcularACF(diferenciar(serie(phi, ruido), 1), 24)[0], 4));

console.log('(2) ruido del simulador, n = 200:');
for (const phi of [0.5, 0.95, 1]) {
  const a = calcularACF(serie(phi, ruido), 24), b = 1.96 / Math.sqrt(200);
  console.log('   φ =', phi.toFixed(2), '· r₁ =', cifra(a[0], 4), '· r₁₀ =', cifra(a[9], 4), '· r₂₄ =', cifra(a[23], 4),
    '· fuera de la banda:', a.filter(r => Math.abs(r) > b).length, 'de 24');
}

console.log('(3) otras muestras: |r₁₀(φ=1) − r₁₀(φ=0.95)|, mediana y cuartiles sobre 400 semillas');
function cuantil(v, q) { const s = v.slice().sort((a, b) => a - b); return s[Math.floor(q * (s.length - 1))]; }
for (const n of [25, 50, 100, 200, 400]) {
  const dif = [], cerca = [];
  for (let s = 1; s <= 400; s++) {
    const e = generarRuidoNormal(n, 1000 + s);
    const a95 = calcularACF(serie(0.95, e), 10), a1 = calcularACF(serie(1, e), 10);
    dif.push(Math.abs(a1[9] - a95[9]));
  }
  console.log('   n =', String(n).padStart(3), '· Q1', cuantil(dif, 0.25).toFixed(3), '· mediana', cuantil(dif, 0.5).toFixed(3), '· Q3', cuantil(dif, 0.75).toFixed(3));
}
console.log('(4) y φ más cerca de 1, con el ruido del simulador: r₁₀');
for (const phi of [0.9, 0.95, 0.98, 0.99, 1]) console.log('   φ =', phi.toFixed(2), '· r₁₀ =', cifra(calcularACF(serie(phi, ruido), 24)[9], 4));
