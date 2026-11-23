// par_simuladores.js — ejecuta con node las funciones numéricas del JS del
// capítulo 5 (copiadas del HTML de f807b40 por su texto, sin tocarlas) y
// reproduce lo que muestran firma-teorica y airline-pesos, para cruzarlo con
// par_verifica2.out (R: ARMAacf / ARMAtoMA).
const fs = require('fs'), { execSync } = require('child_process');
const html = execSync('git show f807b40:Htmls_Series/capitulo-5-sarima.html', { cwd: __dirname, maxBuffer: 1 << 26 }).toString();
function extrae(nombre) {
  const i = html.indexOf('function ' + nombre + '(');
  let j = html.indexOf('{', i), prof = 0, k = j;
  for (; k < html.length; k++) { if (html[k] === '{') prof++; else if (html[k] === '}' && --prof === 0) break; }
  return html.slice(i, k + 1);
}
const M_EST = 12;
eval(['multPoli', 'poliEstacional', 'recortaCeros', 'pesosPsi', 'acfDesdePsi', 'calcularPACF', 'calcularACF'].map(extrae).join('\n'));
const f4 = v => v.toFixed(4);
function firma(phi, theta, Phi, Theta) {   // misma secuencia que SIMULADORES['firma-teorica']
  const polAr = multPoli([1, -phi], poliEstacional(-Phi));
  const polMa = multPoli([1, theta], poliEstacional(Theta));
  const ar = recortaCeros(polAr.slice(1).map(v => -v));
  const ma = recortaCeros(polMa.slice(1));
  const acf = acfDesdePsi(pesosPsi(ar, ma, 1500), 36);
  const pacf = calcularPACF(acf, 36);
  return `ACF[1,11,12,13,24,36] = ${[1,11,12,13,24,36].map(k => f4(acf[k-1])).join(' ')} | PACF[1,2,12,13,24] = ${[1,2,12,13,24].map(k => f4(pacf[k-1])).join(' ')}`;
}
console.log('sar     ', firma(0, 0, 0.7, 0));
console.log('ar1sar1 ', firma(0.6, 0, 0.7, 0));
console.log('extremo ', firma(0.85, 0, 0.85, 0));
console.log('mixto   ', firma(0.5, 0.4, -0.3, -0.6));
// airline-pesos, con el sigma2 del precálculo (AP.airline.sigma2 = 0.001371)
function airline(theta, Theta, sigma2) {
  const polAr = multPoli([1, -1], poliEstacional(-1));
  const polMa = multPoli([1, theta], poliEstacional(Theta));
  const psi = pesosPsi(polAr.slice(1).map(v => -v), polMa.slice(1), 37);
  const s = []; let a = 0;
  for (let h = 1; h <= 36; h++) { a += psi[h-1] ** 2; s.push(Math.sqrt(a * sigma2)); }
  return `theta=${theta} Theta=${Theta} psi1=${f4(psi[1])} psi12=${f4(psi[12])} psi13=${f4(psi[13])} s1=${s[0].toFixed(6)} s12=${s[11].toFixed(6)} s24=${s[23].toFixed(6)} s12/s1=${(s[11]/s[0]).toFixed(3)}`;
}
console.log(airline(-0.40, -0.56, 0.001371));
console.log(airline(-0.4018, -0.5569, 0.001371));
// calcularACF frente a R sobre nabla nabla_12 log(AirPassengers) (n = 131)
const datos = JSON.parse(html.match(/const SERIES_CAP5 = (\{.*?\});\n/)[1]);
let y = datos.airpassengers.valores.map(Math.log);
y = y.slice(12).map((v, i) => v - y[i]); y = y.slice(1).map((v, i) => v - y[i]);
const a = calcularACF(y, 36);
console.log('calcularACF nabla nabla12 logAP n =', y.length, ' r1,r3,r9,r12,r23,r32 =', [1,3,9,12,23,32].map(k => f4(a[k-1])).join(' '),
  ' fuera de banda:', a.map((v, i) => Math.abs(v) > 1.96 / Math.sqrt(y.length) ? i + 1 : null).filter(v => v).join(','));
