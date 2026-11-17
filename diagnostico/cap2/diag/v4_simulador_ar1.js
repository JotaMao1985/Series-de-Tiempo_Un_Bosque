// diag/v4_simulador_ar1.js — reproduce el simulador «El deslizador de φ» (M5) fuera del navegador.
// Uso (desde la raíz del repo): node diagnostico/cap2/diag/v4_simulador_ar1.js
// Extrae del HTML las funciones generarRuidoNormal, calcularACF, diferenciar y varianzaMuestral
// y aplica la misma lógica que SIMULADORES['ar1-phi'] (n = 200, semilla 20260726).
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
const banda = 1.96 / Math.sqrt(n - 1);
console.log('phi | con nabla: r1  teórico -(1-phi)/2 | rezagos fuera de banda | var(nabla y)/var(y)');
for (const phi of [0, 0.3, 0.5, 0.7, 0.95, 1, 1.05]) {
  const d = simular(phi, true), y = simular(phi, false), a = calcularACF(d, 24);
  console.log(phi.toFixed(2), a[0].toFixed(3), (phi <= 1 ? (-(1 - phi) / 2).toFixed(3) : '  — '),
    a.filter(r => Math.abs(r) > banda).length, (varianzaMuestral(d) / varianzaMuestral(y)).toFixed(3));
}
const d105 = simular(1.05, true);
console.log('phi = 1.05, nabla y: primeros y últimos valores', d105.slice(0, 3).map(v => v.toFixed(2)), d105.slice(-3).map(v => v.toExponential(2)));
